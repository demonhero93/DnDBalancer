"""Subclase Rune Knight (Caballero de las Runas, TCE) del Guerrero.

Rasgos por nivel (Fighter 3 / 7 / 10 / 15 / 18):

- **Bonus Proficiencies** (3): herramientas de herrero e idioma
  gigante → dato sin efecto (el modelo no lleva herramientas ni
  idiomas).
- **Rune Carver** (3): runas conocidas — ``sample`` del pool ``RUNES``
  (2/3/4/5 según nivel; tabla ``runes_known_count``), kwarg explícito
  ``runes`` validado (patrón maniobras de Battle Master) y ``rng`` por
  defecto con semilla 0. Cada runa se invoca **una vez por combate**
  (``rune_uses``: 1; 2 con Master of Runes, 15+). CD de runas y de
  Fire/Stone: 8 + PB + mod CON.
- **Giant's Might** (3): acción adicional; durante 1 minuto (= todo el
  combate) te vuelves Grande (patrón Giant Stature, ``size_base``),
  ventaja en pruebas y salvaciones de FUE (consulta de A3) y daño
  extra 1d6 (d8 desde 10, d10 desde 18; ``giants_might_die_sides``)
  una vez por turno. Usos = PB (``giants_might_uses``).
- **Runic Shield** (7): reacción que fuerza al atacante de un aliado
  impactado a repetir el d20. Usos = PB (``runic_shield_uses``).
- **Great Stature** (10): crecer 3d4 pulgadas → dato sin efecto; solo
  sube el dado de Giant's Might a d8.
- **Master of Runes** (15): dos invocaciones por runa.
- **Runic Juggernaut** (18): tamaño Enorme y alcance +5 ft (dato sin
  efecto), dado d10.

Runas con efecto (A7-A11): **frost** (+2 a pruebas/salvaciones de
FUE y CON), **hill** (resistencias temporales a F/P/C + resistencia
pasiva a veneno), **fire** (daño extra y Restringido), **stone**
(Hechizado al terminar su turno), **storm** (ventaja/desventaja) y
**cloud** (redirige el golpe). Los pasivos de las runas (salvo la
resistencia a veneno de Hill), Bonus Proficiencies, el crecimiento de
Great Stature, el alcance extra, la velocidad 0 de Stone y el
despertar de un tercero son datos sin efecto.

Registro: clave ``"rune_knight"`` en ``fighter/__init__.py``. Ver
``TODO.md`` (plan «Rune Knight») y las entradas de
``PASOS-ANTERIORES.txt``.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from .....core.classes import (
    MAX_LEVEL,
    MIN_LEVEL,
    RUNES,
    giants_might_die_sides,
    giants_might_uses,
    rune_uses,
    runes_known_count,
    runic_shield_uses,
)
from .....core.dice import RollMode, roll_d20, roll_dice
from .....core.enums import DamageType
from .....core.log import log_line as _log_line
from .....core.randomness import pick, sample
from .....model.actions import ActionType, CombatAction
from ....roll_modifiers import evaluar_d20
from ....traits.base import Trait
from ..features import FighterFeatures, _contexto

#: Creación reproducible (patrón de todas las subclases de Fighter).
_RNG_CREACION = random.Random(0)


def _de(actor: Any, clase: type) -> Any:
    """Primer trait de ``clase`` que lleve ``actor`` (o ``None``)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


#: Orden PHB de los tamaños (patrón ``giant.py``).
_TAMANOS = ("tiny", "small", "medium", "large", "huge", "gargantuan")


def _orden_tamano(valor: Any) -> int:
    """Orden PHB de un tamaño (acepta combatiente o cadena de tamaño)."""
    tamaño = str(getattr(valor, "size", valor) or "medium").strip().lower()
    if tamaño not in _TAMANOS:
        return _TAMANOS.index("medium")
    return _TAMANOS.index(tamaño)

#: Resistencias temporales de Hill (patrón Bear: lista de fuente propia,
#: solo se concede lo que falte y se revoca solo lo concedido).
_HILL_RESISTENCIAS: frozenset = frozenset({
    DamageType.BLUDGEONING,
    DamageType.PIERCING,
    DamageType.SLASHING,
})


@dataclass
class RuneKnightFeatures(Trait):
    """Rasgos, runas y estados de Rune Knight.

    Sin RNG en los guards: los ``pick`` de invocación de runas se
    deciden en sus puntos de consulta con el ``rng`` del combate.
    """

    # Nivel del personaje (manda en las tablas de rasgos).
    level: int = MIN_LEVEL
    # Runas conocidas (2/3/4/5 según nivel; pool ``RUNES``).
    runas: list[str] = field(default_factory=list, repr=False,
                             compare=False)
    # Usos restantes por runa (1; 2 con Master of Runes, 15+).
    usos_runa: dict = field(default_factory=dict, repr=False,
                            compare=False)
    # Giant's Might (3): usos por descanso largo + «una vez por turno»
    # del daño extra (flag se reinicia en ``on_turn_start``).
    giants_might_usos: int = 0
    giants_might_used_this_turn: bool = False
    # Giant's Might activo (dura todo el combate; lo pone la acción).
    giants_might_activo: bool = False
    # Runic Shield (7): usos por descanso largo; la reacción compartida
    # vive en ``state.reaction_used``.
    runic_shield_usos: int = 0
    # Estados activos de runas (duración = combate; los limpia
    # ``reset``). Fire/Stone marcan objetivos en ``CombatState`` (A8/A9).
    frost_activo: bool = False
    hill_activo: bool = False
    # Resistencias B/P/C que Hill concedió (para revocarlas en reset).
    hill_concedidas: list = field(default_factory=list, repr=False,
                                  compare=False)
    storm_activo: bool = False
    # Datos sin efecto congelados (decisión del maintainer): pasivos de
    # las runas (salvo la resistencia a veneno de Hill, A7) y Bonus
    # Proficiencies (herramientas de herrero e idioma gigante).
    pasivos_runas: bool = True
    bonus_proficiencies: bool = True
    # Dueño (guards de hooks y despacho de ``on_turn_start``).
    owner: Any = field(default=None, repr=False, compare=False)

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        # «Una vez por turno» de Giant's Might (A4): se reinicia al
        # empezar el turno.
        self.giants_might_used_this_turn = False

    def reset(self) -> None:
        """Un combate nuevo = un día descansado: usos restaurados."""
        self.usos_runa = {r: rune_uses(self.level) for r in self.runas}
        self.giants_might_usos = giants_might_uses(self.level)
        self.giants_might_used_this_turn = False
        self.giants_might_activo = False
        self.runic_shield_usos = runic_shield_uses(self.level)
        self.frost_activo = False
        self._revocar_hill()
        self.hill_activo = False
        self.storm_activo = False

    # --- Giant's Might (3) ---------------------------------------------------
    def _fue_giants_might(self, habilidad: Any, sujeto: Any) -> bool:
        """¿La consulta es una prueba/salvación de FUE del dueño activo?"""
        if not self.giants_might_activo or sujeto is not self.owner:
            return False
        return str(habilidad or "").strip().lower() in ("str", "strength")

    def _bonus_frost(self, habilidad: Any, sujeto: Any) -> int:
        """Frost: +2 a pruebas y salvaciones de FUE/CON del dueño."""
        if not self.frost_activo or sujeto is not self.owner:
            return 0
        if str(habilidad or "").strip().lower() in (
                "str", "strength", "con", "constitution"):
            return 2
        return 0

    def modificar_salvacion(self, habilidad: Any, sujeto: Any,
                            ctx: Any = None) -> tuple[bool, bool, int]:
        """Giant's Might (ventaja FUE) + Frost (+2 FUE/CON), consulta A3."""
        return (self._fue_giants_might(habilidad, sujeto), False,
                self._bonus_frost(habilidad, sujeto))

    def modificar_prueba(self, habilidad: Any, sujeto: Any,
                         ctx: Any = None) -> tuple[bool, bool, int]:
        """Giant's Might (ventaja FUE) + Frost (+2 FUE/CON), consulta A3."""
        return (self._fue_giants_might(habilidad, sujeto), False,
                self._bonus_frost(habilidad, sujeto))

    def repetir_d20(self, target: Any, attacker: Any, rango: Any, *,
                    bonus: int, ctx: Any = None, rng: Any = None,
                    atk: Any = None, log: Any = None) -> Any:
        """Runic Shield (7): fuerza al atacante a repetir el d20.

        Se decide tras acertar y antes del daño (mismo punto que
        Warding Maneuver). Solo contra OTRA criatura aliada viva del
        dueño (no el propio dueño ni un enemigo), con usos y reacción
        libre; sin RNG el rasgo se abstiene. La decisión es un
        ``pick`` «no»/«sí». La repetición es UN solo d20 en modo
        normal (sin conservar la ventaja original): el motor recibe
        ``(roll, total, crit, fallo_natural)`` y reevalúa el impacto
        con la CA; el crítico y el 1 natural salen del umbral del
        atacante (``evaluar_d20``, Champion). Guard de reentrada: el
        motor la consulta una sola vez por ataque.
        """
        owner = self.owner
        if (
            self.level < 7
            or owner is None
            or target is None
            or target is owner
            or int(self.runic_shield_usos) <= 0
            or not getattr(owner, "alive", True)
            or not getattr(owner, "can_react", True)
            or getattr(getattr(owner, "state", None), "reaction_used", True)
            or rng is None
        ):
            return None
        hostil = getattr(owner, "is_hostile_to", None)
        if hostil is not None and hostil(target):
            return None
        if pick(rng, ("no", "si")) == "no":
            return None
        self.runic_shield_usos -= 1
        owner.state.reaction_used = True
        nuevo = roll_d20(rng, RollMode.NORMAL)
        roll = int(nuevo.value)
        crit, fallo_natural = evaluar_d20(roll, attacker, atk)
        total = roll + int(bonus)
        if log is not None:
            log.append(
                f"  {owner.name} hace repetir el ataque a "
                f"{getattr(attacker, 'name', attacker)} (Runic Shield): "
                f"nuevo d20 {roll} -> {total}"
            )
        return roll, total, crit, fallo_natural

    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            *, crit: bool = False, ctx: Any = None,
                            rng: Any = None, atk: Any = None) -> int:
        """Giant's Might: 1d6 (d8 con 10, d10 con 18) una vez por turno.

        El motor lo suma al bruto del arma, así que el daño extra es
        del mismo tipo que el ataque. Sin ``rng`` o sin ataque no se
        consume la vez del turno (no hay dados que tirar).
        """
        if (not self.giants_might_activo or attacker is not self.owner
                or self.giants_might_used_this_turn or atk is None
                or rng is None or getattr(atk, "spell_attack", False)):
            return 0
        self.giants_might_used_this_turn = True
        lados = giants_might_die_sides(self.level)
        return int(roll_dice(f"1d{lados}", rng, crit=crit))

    # --- Runas Hill y Frost (A7) ----------------------------------------------
    def _otorgar_hill(self, actor: Any, ctx: Any) -> None:
        """Hill: resistencias temporales B/P/C (patrón Bear)."""
        previas = set(getattr(actor, "resistances", None) or set())
        nuevas = [t for t in sorted(_HILL_RESISTENCIAS, key=lambda t: t.value)
                  if t not in previas]
        if not nuevas:
            return
        actor.resistances = previas | set(nuevas)
        for tipo in nuevas:
            self.hill_concedidas.append((actor, tipo))
        _log_line(ctx, f"  {getattr(actor, 'name', actor)} gana "
                       f"resistencia a "
                       f"{', '.join(t.value for t in nuevas)} (Hill)")

    def _revocar_hill(self) -> None:
        """Retira SOLO las resistencias que Hill concedió."""
        for objeto, tipo in self.hill_concedidas:
            resis = getattr(objeto, "resistances", None)
            if resis is not None:
                resis.discard(tipo)
        self.hill_concedidas.clear()


class GiantsMightAction(CombatAction):
    """Giant's Might (3, acción adicional): tamaño, FUE y daño extra.

    Elegible sin RNG (nivel >= 3, sin activar y con usos); el ``pick``
    del encuentro decide entre las acciones candidatas. Una vez
    activo dura todo el combate y no se vuelve a activar; el uso se
    gasta al ejecutar y el tamaño lo restaura ``Combatant.reset``.
    """

    def __init__(self) -> None:
        self.name = "Giant's Might"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # los usos viven en el rasgo

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        trait = _de(actor, RuneKnightFeatures)
        if trait is None or trait.level < 3:
            return False
        if trait.giants_might_activo:
            return False
        return int(trait.giants_might_usos) > 0

    def execute(self, context: Any) -> None:
        actor = context.actor
        trait = _de(actor, RuneKnightFeatures)
        if (trait is None or trait.giants_might_activo
                or int(trait.giants_might_usos) <= 0):
            return  # sin usos o ya activo: se abstiene
        trait.giants_might_usos -= 1
        trait.giants_might_activo = True
        nuevo = "huge" if trait.level >= 18 else "large"
        if _orden_tamano(actor) < _orden_tamano(nuevo):
            actor.size = nuevo
            _log_line(context, f"{getattr(actor, 'name', actor)} crece a "
                               f"{nuevo} (Giant's Might)")
        _log_line(context, f"{getattr(actor, 'name', actor)} activa "
                           f"Giant's Might")


#: Nombres de las runas para la acción y el log.
_NOMBRES_RUNA = {
    "cloud": "Cloud Rune",
    "fire": "Fire Rune",
    "frost": "Frost Rune",
    "hill": "Hill Rune",
    "stone": "Stone Rune",
    "storm": "Storm Rune",
}


class RuneInvokeAction(CombatAction):
    """Invocación de una runa (acción bonus; A7: Frost y Hill).

    Una instancia por runa conocida: la elegibilidad no consume RNG
    (runa conocida, usos restantes, sin invocar y acción bonus libre;
    el ``pick`` del encuentro decide entre las acciones candidatas).
    Una vez invocada, la runa dura todo el combate y no se vuelve a
    invocar: los usos extra de Master of Runes quedan para las runas
    de efecto por invocación (Fire/Stone, A8/A9).
    """

    def __init__(self, runa: str) -> None:
        self.runa = runa
        self.name = _NOMBRES_RUNA.get(runa, f"Rune ({runa})")
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # los usos viven en el rasgo

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        trait = _de(actor, RuneKnightFeatures)
        if trait is None or self.runa not in trait.runas:
            return False
        if int(trait.usos_runa.get(self.runa, 0)) <= 0:
            return False
        return not getattr(trait, f"{self.runa}_activo", False)

    def execute(self, context: Any) -> None:
        actor = context.actor
        trait = _de(actor, RuneKnightFeatures)
        if (trait is None or self.runa not in trait.runas
                or int(trait.usos_runa.get(self.runa, 0)) <= 0
                or getattr(trait, f"{self.runa}_activo", False)):
            return
        if self.runa not in ("frost", "hill"):
            return  # runas de reacción: A8-A11 las añaden
        trait.usos_runa[self.runa] = int(trait.usos_runa[self.runa]) - 1
        if self.runa == "frost":
            trait.frost_activo = True
            _log_line(context, f"{actor.name} invoca Frost Rune: +2 a "
                               f"pruebas y salvaciones de FUE y CON")
        else:
            trait.hill_activo = True
            trait._otorgar_hill(actor, context)
            _log_line(context, f"{actor.name} invoca Hill Rune: "
                               f"resistencia a B/P/C durante el combate")


def apply_rune_knight(pj: Any, level: int | None = None,
                      runes: tuple[str, ...] | None = None,
                      rng: random.Random | None = None
                      ) -> RuneKnightFeatures:
    """Aplica la subclase Rune Knight a un PJ Guerrero.

    Exige que ``pj`` ya tenga :class:`FighterFeatures`
    (:func:`apply_fighter`) y nivel >= 3. Elige las runas conocidas
    con ``sample`` del pool ``RUNES`` (o las explícitas del kwarg
    ``runes``, validadas por nombre y recuento). ``rng`` por defecto
    con semilla 0 (patrón de las demás subclases): la creación es
    reproducible.
    """
    if _de(pj, FighterFeatures) is None:
        raise ValueError(
            "Primero aplica la clase guerrero con apply_fighter(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    if lvl < 3:
        raise ValueError(
            f"Rune Knight requiere nivel >= 3: llegó {lvl}."
        )
    generador = rng if rng is not None else _RNG_CREACION

    # Runas conocidas: N del pool (sample) o las explícitas.
    n = runes_known_count(lvl)
    if runes is None:
        elegidas = list(sample(generador, RUNES, n))
    else:
        elegidas = list(runes)
        invalidas = [r for r in elegidas if r not in RUNES]
        if invalidas:
            raise ValueError(
                f"{invalidas!r} no es una runa de Rune Knight: "
                f"opciones {sorted(RUNES)}."
            )
        if len(elegidas) != n:
            raise ValueError(
                f"se esperaban {n} runas para el nivel {lvl} y "
                f"llegaron {len(elegidas)}."
            )

    # Pasivo de Hill: resistencia permanente a veneno (solo si se
    # conoce la runa; sin acumular si ya la tenía, patrón Guarded
    # Mind). La ventaja en salvaciones contra veneno NO se modela: el
    # motor no distingue «salvación contra veneno» (dato sin efecto).
    if "hill" in elegidas and DamageType.POISON not in pj.resistances:
        pj.resistances = set(pj.resistances) | {DamageType.POISON}

    trait = RuneKnightFeatures(
        name="Rune Knight",
        level=lvl,
        runas=elegidas,
        usos_runa={r: rune_uses(lvl) for r in elegidas},
        giants_might_usos=giants_might_uses(lvl),
        runic_shield_usos=runic_shield_uses(lvl),
    )
    trait.owner = pj
    pj.traits.append(trait)
    # Acción adicional de Giant's Might (elegibilidad sin RNG).
    pj.actions.append(GiantsMightAction())
    # Invocaciones de runa (A7): una acción bonus por runa de efecto
    # continuo conocida (Fire/Stone/Cloud son reacciones, A8/A9/A11).
    for runa in ("frost", "hill"):
        if runa in elegidas:
            pj.actions.append(RuneInvokeAction(runa))
    return trait


__all__ = ["GiantsMightAction", "RuneInvokeAction", "RuneKnightFeatures",
           "apply_rune_knight"]

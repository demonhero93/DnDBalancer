"""Subclase Path of the Giant del bárbaro (Camino del Gigante).

Fuente: reglas resueltas en el enunciado de la tarea (la subclase no
está en el SRD 2014 ni en la API, así que la tabla de features va
hardcodeada en :data:`GIANT_FEATURES`).

Decisiones de simulación documentadas:

- **Giant's Power** (3): truco Druidcraft o Thaumaturgy (característica
  de lanzamiento CON): solo dato informativo en :data:`GIANT_FEATURES`;
  el simulador no lanza trucos utilitarios fuera de combate, así que no
  tiene efecto mecánico.
  # TODO: sin efecto mecánico (trucos fuera de combate no modelados).
- **Giant's Havoc** (3):
  - *Crushing Throw*: en un ataque **arrojadizo** con FUE que acierta,
    suma ``rage_damage(level)`` (mismo paquete de daño = mismo tipo que
    el arma). La Furia base solo suma en cuerpo a cuerpo (guardia de
    rango en ``BarbarianFeatures.extra_attack_damage``), así que no se
    duplica.
  - *Giant Stature*: con Furia activa ``size`` pasa a ``large`` (si es
    menor) y vuelve al original al terminar la Furia y en ``reset()``
    (campo ``Combatant.size_base``). El alcance +5 pies no tiene
    efecto sin sistema de movimiento: no se modela.
    # TODO: alcance +5 ft no modelado (sin posiciones/velocidad).
- **Elemental Cleaver** (6): al entrar en Furia elige **un** tipo
  (ácido/frío/fuego/relámpago/trueno) con ``pick`` uniforme y **un**
  arma de sus ataques con ``pick`` (una sola opción = sin RNG); mientras
  dure la Furia el arma cambia a ese tipo de daño, hace +1d6 de ese
  tipo al impactar (2d6 desde el nivel 14) y gana la propiedad
  arrojadiza (``range_type`` MELEE → MELEE_OR_RANGED; se recoge sola al
  acertar o fallar, no se modela). El tipo **no** se cambia después de
  impactar ni como acción adicional.
  # TODO: cambiar el tipo al impactar/como acción adicional no implementado.
- **Mighty Impel** (10): acción bonus en Furia contra un enemigo con
  GRAPPLED (fuente = bárbaro) de tamaño Mediano o menor: PRONE, 3d6
  contundente de lanzamiento y el agarre termina. La decisión de
  usarla o no la toma el encuentro con ``pick`` entre las acciones
  candidatas (mismo patrón que Intimidating Presence).
  # TODO: alcance 9 m y «o criatura voluntaria» no modelados (sin
  posiciones; solo agarrado).
- **Demiurgic Colossus** (14): con Furia activa ``size`` pasa a
  ``huge`` (si es menor) y Elemental Cleaver sube a 2d6. El alcance
  +10 ft no se modela (mismo motivo que Giant Stature).
  # TODO: alcance +10 ft no modelado.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .....core.classes import MAX_LEVEL, MIN_LEVEL, rage_damage
from .....core.dice import roll_dice
from .....core.enums import AttackRange, parse_damage_type
from .....core.log import log_line as _log_line
from .....core.randomness import pick
from .....model.actions import ActionType, CombatAction
from ....conditions import Condition, EscapeCheck, apply_condition
from ....damage import inflict_damage
from ....traits.base import Trait
from ....utility import _TAMANOS
from ..features import BarbarianFeatures, _contexto

#: Features de subclase por nivel (nombres en inglés como la API).
GIANT_FEATURES: dict[int, tuple[str, ...]] = {
    3: ("Giant's Power", "Giant's Havoc"),
    6: ("Elemental Cleaver",),
    10: ("Mighty Impel",),
    14: ("Demiurgic Colossus",),
}

#: Tipos elementales de Elemental Cleaver (PHB: ácido, frío, fuego,
#: relámpago y trueno; elección uniforme con ``pick``).
_ELEMENTALES = ("acid", "cold", "fire", "lightning", "thunder")


def _de(actor: Any, clase: type) -> Any:
    """Primer rasgo de ``actor`` que sea instancia de ``clase`` (o None)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


def _orden_de(valor: Any) -> int:
    """Orden PHB de un tamaño (acepta combatiente o cadena de tamaño)."""
    tamaño = str(getattr(valor, "size", valor) or "medium").strip().lower()
    if tamaño not in _TAMANOS:
        return _TAMANOS.index("medium")
    return _TAMANOS.index(tamaño)


def _objetivos_impel(actor: Any, ctx: Any) -> list:
    """Enemigos vivos, Medianos o menos, agarrados por ``actor``."""
    maximo = _orden_de("medium")
    out = []
    for c in getattr(ctx, "combatants", None) or []:
        if c is actor or not getattr(c, "alive", True):
            continue
        hostil = getattr(actor, "is_hostile_to", None)
        if hostil is not None and not hostil(c):
            continue
        if _orden_de(c) > maximo:
            continue
        tracker = getattr(c, "conditions", None)
        if tracker is None:
            continue
        if any(getattr(i, "condition", None) is Condition.GRAPPLED
               and getattr(i, "source", None) is actor
               for i in getattr(tracker, "instances", []) or []):
            out.append(c)
    return out


@dataclass
class GiantFeatures(Trait):
    """Features de la subclase y estado de tamaño/arma elemental."""

    level: int = MIN_LEVEL
    #: Tipo elemental elegido al entrar en Furia (None sin imbuir).
    elemental_tipo: str | None = None
    #: Arma imbuyida (el objeto Attack; None sin imbuir).
    elemental_arma: Any = field(default=None, repr=False, compare=False)
    #: Estado previo del arma para restaurarla al terminar la Furia.
    arma_previo_tipo: Any = field(default=None, repr=False, compare=False)
    arma_previo_rango: Any = field(default=None, repr=False, compare=False)
    owner: Any = field(default=None, repr=False, compare=False)

    # --- Ciclo de Furia ------------------------------------------------------
    def on_rage_start(self, actor: Any, ctx: Any = None) -> None:
        """Giant Stature/Demiurgic Colossus (tamaño) y Elemental Cleaver."""
        if self.level < 3:
            return
        nuevo = "huge" if self.level >= 14 else "large"
        if _orden_de(actor) < _orden_de(nuevo):
            actor.size = nuevo
            _log_line(ctx, f"{getattr(actor, 'name', actor)} crece a "
                           f"{nuevo} (Giant Stature)")
        if self.level >= 6:
            self._imbuir(actor, ctx)

    def on_rage_end(self, actor: Any, ctx: Any = None) -> None:
        self._restaurar(actor)

    def _imbuir(self, actor: Any, ctx: Any) -> None:
        """Elemental Cleaver: elige tipo y arma al entrar en Furia."""
        if self.elemental_arma is not None:
            return  # ya imbuido (reentrada)
        pool = [a for a in (getattr(actor, "attacks", None) or [])
                if str(getattr(a, "damage", "") or "").strip()]
        if not pool:
            return  # sin arma: nada que imbuir (y sin RNG)
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return  # sin RNG el rasgo se abstiene (no inventa dados)
        self.elemental_tipo = pick(rng, _ELEMENTALES)  # 5 opciones: 1 rng
        arma = pick(rng, pool)                        # 1 opción: sin rng
        self.elemental_arma = arma
        self.arma_previo_tipo = arma.damage_type
        self.arma_previo_rango = arma.range_type
        arma.damage_type = parse_damage_type(self.elemental_tipo)
        if arma.range_type is AttackRange.MELEE:
            arma.range_type = AttackRange.MELEE_OR_RANGED
        _log_line(ctx, f"{getattr(actor, 'name', actor)} imbuye {arma.name} "
                       f"con energía {self.elemental_tipo} "
                       f"(Elemental Cleaver)")

    def _restaurar(self, actor: Any) -> None:
        """Tamaño original y arma previa (al terminar la Furia y en reset)."""
        if actor is None:
            return
        base = getattr(actor, "size_base", None)
        if base:
            actor.size = base
        arma = self.elemental_arma
        if arma is not None:
            if self.arma_previo_tipo is not None:
                arma.damage_type = self.arma_previo_tipo
            if self.arma_previo_rango is not None:
                arma.range_type = self.arma_previo_rango
        self.elemental_arma = None
        self.elemental_tipo = None
        self.arma_previo_tipo = None
        self.arma_previo_rango = None

    # --- Daño extra: Crushing Throw (3) y Elemental Cleaver (6) ---------------
    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            crit: bool = False, ctx: Any = None,
                            rng: Any = None, atk: Any = None) -> int:
        """Crushing Throw: ``rage_damage`` en arrojadiza con FUE que acierta.

        El hook solo se invoca al impactar, así que «solo si acierta»
        lo garantiza el motor. Elemental Cleaver suma +1d6 (2d6 desde
        el 14) solo con el arma imbuyida mientras dura la Furia; sin
        ``rng`` no tira dados. Cada rasgo usa su propio estado, sin
        pisar el «primera acertada» de Frenzy.
        """
        if self.level < 3 or attacker is not self.owner or atk is None:
            return 0
        barb = _de(attacker, BarbarianFeatures)
        if barb is None or not barb.rage_active:
            return 0
        bonus = 0
        if (rango is AttackRange.RANGED
                and BarbarianFeatures._es_fue(atk)):
            bonus += rage_damage(self.level)
        if (self.level >= 6 and self.elemental_arma is not None
                and atk is self.elemental_arma):
            if rng is None:
                return bonus  # sin RNG el rasgo se abstiene (no inventa)
            dados = "2d6" if self.level >= 14 else "1d6"
            bonus += int(roll_dice(dados, rng, crit=crit))
        return bonus

    # --- Reinicio ------------------------------------------------------------
    def reset(self) -> None:
        self._restaurar(self.owner)


class MightyImpelAction(CombatAction):
    """Lanzamiento potente (Mighty Impel): bonus action, nivel ≥10 en Furia."""

    def __init__(self) -> None:
        self.name = "Lanzamiento potente"
        self.action_type = ActionType.BONUS_ACTION
        # Sin uso limitado: el límite es la Furia activa y el agarrado.
        self.usage = None

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        giant = _de(actor, GiantFeatures)
        if giant is None or giant.level < 10:
            return False
        barb = _de(actor, BarbarianFeatures)
        if barb is None or not barb.rage_active:
            return False
        return bool(_objetivos_impel(actor, ctx))

    def execute(self, context: Any) -> None:
        actor = getattr(context, "actor", None)
        giant = _de(actor, GiantFeatures) if actor is not None else None
        if giant is None or giant.level < 10:
            return
        barb = _de(actor, BarbarianFeatures)
        if barb is None or not barb.rage_active:
            return
        rng = getattr(context, "rng", None)
        if rng is None:
            return  # sin RNG no se tira nada (y no se paga nada)
        objetivos = _objetivos_impel(actor, context)
        if not objetivos:
            return
        objetivo = pick(rng, objetivos)  # 1 sola opción: sin RNG
        _log_line(context, f"{actor.name} lanza a {objetivo.name} "
                           f"(Lanzamiento potente)")
        # Sin sistema de movimiento: ponerse en pie = escape libre CD 10
        # (mismo patrón que Empujar en rules/utility.py).
        apply_condition(
            objetivo, Condition.PRONE, context, source=actor,
            escape=EscapeCheck(abilities=("str", "dex"), dc=10,
                               consumes_action=False),
        )
        dmg = int(roll_dice("3d6", rng))
        _log_line(context, f"  {dmg} daño contundente de lanzamiento")
        inflict_damage(objetivo, dmg, "bludgeoning", source=actor,
                       ctx=context, rng=rng)
        # El agarre del bárbaro termina (las instancias de otros, no).
        quitado = False
        for inst in list(getattr(objetivo.conditions, "instances", []) or []):
            if inst.condition is Condition.GRAPPLED and inst.source is actor:
                objetivo.conditions.remove_instance(inst)
                quitado = True
        if quitado:
            _log_line(context, f"  el agarre sobre {objetivo.name} termina")


def apply_giant(pj: Any, level: int | None = None) -> GiantFeatures:
    """Aplica la subclase Path of the Giant a un PJ bárbaro.

    Exige que ``pj`` ya tenga :class:`BarbarianFeatures`
    (:func:`apply_barbarian`). Añade el trait de subclase y la acción
    bonus de Lanzamiento potente.
    """
    if _de(pj, BarbarianFeatures) is None:
        raise ValueError(
            "Primero aplica la clase bárbaro con apply_barbarian(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    trait = GiantFeatures(name="Giant", level=lvl)
    trait.owner = pj
    pj.traits.append(trait)
    pj.actions.append(MightyImpelAction())
    return trait


__all__ = ["GIANT_FEATURES", "GiantFeatures", "MightyImpelAction",
           "apply_giant"]

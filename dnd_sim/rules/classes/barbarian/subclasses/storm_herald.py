"""Subclase Path of the Storm Herald del bárbaro (XGE 2014).

Fuente: *Xanathar's Guide to Everything* — Path of the Storm Herald
(features en niveles 3, 6, 10 y 14). No está ni en el SRD 2014 ni en la
API, así que la tabla va hardcodeada en :data:`STORM_HERALD_FEATURES`.
Aplica sobre la Furia del proyecto (reglas 2024).

Decisiones de simulación documentadas:

- **Elección de entorno**: el PJ elige ``desert``, ``sea`` o ``tundra``
  al tomar el camino; los PJ se definen en código, así que el entorno es
  un parámetro fijo de :func:`apply_storm_herald`. ``apply_class`` solo
  pasa ``level``, así que el registro da tres claves
  (``storm_herald_desert/sea/tundra``) que comparten el mismo trait.
- **Storm Aura** (3): mientras dura la Furia, aura de 10 pies. La
  primera activación es automática al entrar en Furia
  (``on_rage_start``); las siguientes se hacen con una acción adicional
  (:class:`StormAuraAction`, bonus action): el motor solo ejecuta una
  ACTION y una BONUS_ACTION por turno, así que la «acción adicional»
  se modela como bonus y la decisión de usarla la toma el ``pick`` del
  encuentro entre candidatas (patrón Intimidating Presence / Mighty
  Impel). CD 8 + PB + mod CON; efectos mágicos (``magical=True``).
  - Desert: daño de fuego plano sin salvación a cada otra criatura
    enemiga: 2 (3), 3 (5), 4 (10), 5 (15), 6 (20).
  - Sea: UNA criatura enemiga que se elige del aura; salvación de DES,
    mitad si acierta; 1d6 de rayo (10: 2d6, 15: 3d6, 20: 4d6). «Que
    vea» no está modelado: cualquier enemigo del aura vale (# TODO).
  - Tundra: PV temporales a cada criatura aliada del aura (el propio
    bárbaro incluido): 2/3/4/5/6; no se acumulan (se queda el mayor).
- **Sin posiciones**: quién está en el aura usa el mismo criterio que
  :mod:`rules.area` (convención: sin geometría, todo el mundo cuenta)
  filtrado por :func:`valid_targets` (enemigos) o por bandos (aliados),
  con :data:`STORM_AURA_COVERAGE_PROBABILITY` como cobertura por
  criatura: 1.0/0.0 no consumen RNG; en medio, UNA tirada por criatura
  (# TODO: por defecto 1.0 = aura de 10 ft sin geometría).
- **Storm Soul** (6): PERMANENTE, se añade la resistencia al aplicar la
  subclase (sobrevive a ``Combatant.reset``, igual que la ficha).
  Los efectos de exploración no se modelan (# TODO).
- **Shielding Storm** (10): en cada activación del aura, los aliados
  dentro ganan la resistencia de Storm Soul mientras dure la Furia.
  Solo se retira lo que este rasgo añadió (lista ``_concedidas``): una
  resistencia que el aliado ya tuviera no se toca. «Aliados elegidos»
  sin posiciones = todos los aliados del aura (# TODO).
- **Raging Storm** (14): patrón de reacción de Retaliation (guardas de
  vida/hostilidad/can_act, una por ronda vía ``state.reaction_used``,
  sin RNG se abstiene) pero SIN limitar a cuerpo a cuerpo: cualquier
  atacante en el aura vale. Decisión usar/no con ``pick`` (50/50).
  - Desert: reacción tras recibir impacto; salvación de DES, fallo =
    daño de fuego = nivel de bárbaro // 2.
  - Sea: reacción idéntica; salvación de FUE, fallo → PRONE.
  - Tundra: sin reacción; al activar el aura se elige UNA criatura,
    salvación de FUE, fallo → velocidad 0 hasta el inicio del
    siguiente turno del bárbaro: sin sistema de movimiento se guarda
    como dato en ``velocidad_cero`` y se limpia en ``on_turn_start``/
    ``on_rage_end``/``reset`` (# TODO).
  # TODO: alcance real del aura (10 ft) y «que vea» no modelados.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .....core.classes import MAX_LEVEL, MIN_LEVEL
from .....core.dice import roll_dice
from .....core.enums import parse_damage_type
from .....core.log import log_line as _log_line
from .....core.randomness import pick
from .....core.targeting import valid_targets
from .....model.actions import ActionType, CombatAction
from ....conditions import Condition, apply_condition
from ....damage import inflict_damage
from ....saves import (SaveDamage, apply_save_damage, registrar_resistencia,
                       saving_throw)
from ....traits.base import Trait
from .._util import _de
from ..features import BarbarianFeatures, _contexto

#: Features de subclase por nivel (XGE 2014; nombres en inglés).
STORM_HERALD_FEATURES: dict[int, tuple[str, ...]] = {
    3: ("Storm Aura",),
    6: ("Storm Soul",),
    10: ("Shielding Storm",),
    14: ("Raging Storm",),
}

#: Entornos posibles (elegidos al tomar el camino; fijos por PJ).
ENTORNOS: tuple[str, ...] = ("desert", "sea", "tundra")

#: Tipo de daño de la resistencia de Storm Soul por entorno.
_TIPO_POR_ENTORNO: dict[str, str] = {
    "desert": "fire",
    "sea": "lightning",
    "tundra": "cold",
}

#: Daño de fuego del aura del desierto y PV temporales de la tundra.
_ESCALADO_AURA: dict[int, int] = {3: 2, 5: 3, 10: 4, 15: 5, 20: 6}

#: Dados de rayo del aura del mar por nivel (mayor primero).
_DADOS_MAR: tuple[tuple[int, str], ...] = (
    (20, "4d6"), (15, "3d6"), (10, "2d6"), (3, "1d6"),
)

#: Probabilidad por criatura de estar dentro del aura (sin posiciones).
#: 1.0/0.0 no consumen RNG; en medio, UNA tirada por criatura.
STORM_AURA_COVERAGE_PROBABILITY: float = 1.0


def _escalado(level: int) -> int:
    """Valor de la tabla :data:`_ESCALADO_AURA` para ``level``."""
    for minimo in sorted(_ESCALADO_AURA, reverse=True):
        if level >= minimo:
            return _ESCALADO_AURA[minimo]
    return _ESCALADO_AURA[3]


def _dado_mar(level: int) -> str:
    """Expresión de dados del aura del mar para ``level``."""
    for minimo, expr in _DADOS_MAR:
        if level >= minimo:
            return expr
    return _DADOS_MAR[-1][1]


def _cd(actor: Any) -> int:
    """CD de las salvaciones del aura: 8 + competencia + mod CON."""
    con = 0
    try:
        con = actor.abilities.mod("con")
    except Exception:
        pass
    return 8 + int(getattr(actor, "proficiency", 0) or 0) + int(con)


def _en_aura(rng: Any) -> bool:
    """¿Está una criatura en el aura? (cobertura, sin posiciones)."""
    p = float(STORM_AURA_COVERAGE_PROBABILITY)
    if p <= 0.0:
        return False
    if p >= 1.0:
        return True
    if rng is None:
        return True  # sin RNG: cobertura completa (no inventa tiradas)
    return rng.random() < p


def _enemigos_en_aura(actor: Any, ctx: Any) -> list:
    """Enemigos vivos dentro del aura (criterio de rules/area)."""
    rng = getattr(ctx, "rng", None)
    return [c for c in valid_targets(actor, ctx) if _en_aura(rng)]


def _aliados_en_aura(actor: Any, ctx: Any, *,
                     incluye_actor: bool = False) -> list:
    """Aliados vivos dentro del aura (sin posiciones: todos)."""
    rng = getattr(ctx, "rng", None)
    pool: list = []
    for c in getattr(ctx, "combatants", None) or []:
        if c is actor:
            if not incluye_actor:
                continue
        elif not getattr(c, "alive", True):
            continue
        else:
            hostil = getattr(actor, "is_hostile_to", None)
            if hostil is not None and hostil(c):
                continue
        if _en_aura(rng):
            pool.append(c)
    return pool


@dataclass
class StormHeraldFeatures(Trait):
    """Features de la subclase y estado del aura/concesiones."""

    level: int = MIN_LEVEL
    #: Entorno elegido al tomar el camino: ``desert``/``sea``/``tundra``.
    entorno: str = "desert"
    #: Resistencias concedidas por Shielding Storm: solo las que ESTE
    #: rasgo añadió (si el aliado ya la tenía, no se registra ni se
    #: retira al terminar la Furia).
    _concedidas: list = field(default_factory=list, repr=False,
                              compare=False)
    #: Raging Storm tundra: criatura con velocidad 0 (dato; sin
    #: sistema de movimiento no tiene efecto mecánico).
    velocidad_cero: Any = field(default=None, repr=False, compare=False)
    owner: Any = field(default=None, repr=False, compare=False)

    @property
    def _furiosa(self) -> bool:
        barb = _de(self.owner, BarbarianFeatures)
        return bool(barb and barb.rage_active)

    @property
    def _tipo_alma(self) -> str:
        return _TIPO_POR_ENTORNO.get(self.entorno, "fire")

    # --- Storm Aura (3) ------------------------------------------------------
    def activar_aura(self, actor: Any, ctx: Any = None) -> None:
        """Efecto del aura al activarse (entrada en Furia o acción).

        Sin ``ctx`` o sin Furia no hace nada. El orden de RNG es
        estable: enemigos (sin RNG) -> tira/daño del mar, aliados
        (cobertura), Shielding Storm, Raging Storm tundra.
        """
        if self.level < 3 or ctx is None or not self._furiosa:
            return
        rng = getattr(ctx, "rng", None)
        _log_line(ctx, f"{getattr(actor, 'name', actor)} activa su Aura "
                       f"de Tormenta ({self.entorno})")
        if self.entorno == "desert":
            cantidad = _escalado(self.level)
            for objetivo in _enemigos_en_aura(actor, ctx):
                _log_line(ctx, f"  {getattr(objetivo, 'name', objetivo)}: "
                               f"{cantidad} de daño de fuego (aura)")
                inflict_damage(objetivo, cantidad, "fire", source=actor,
                               ctx=ctx, magical=True)
        elif self.entorno == "sea":
            pool = _enemigos_en_aura(actor, ctx)
            if pool and rng is not None:
                objetivo = pick(rng, pool)
                dado = _dado_mar(self.level)
                bruto = roll_dice(dado, rng)
                efecto = SaveDamage(
                    ability="dex", dc=_cd(actor), damage=dado,
                    damage_type="lightning", on_success="half",
                    magical=True,
                )
                r = apply_save_damage(actor, objetivo, efecto, bruto, ctx)
                _log_line(ctx, f"  {getattr(objetivo, 'name', objetivo)}: "
                               f"{r.final_damage} de daño de rayo (aura, "
                               f"{'éxito' if r.save.success else 'fallo'} "
                               f"de salvación)")
        else:  # tundra
            cantidad = _escalado(self.level)
            for objetivo in _aliados_en_aura(actor, ctx,
                                             incluye_actor=True):
                actual = int(getattr(objetivo, "temp_hp", 0) or 0)
                objetivo.temp_hp = max(actual, cantidad)  # no se acumula
                _log_line(ctx, f"  {getattr(objetivo, 'name', objetivo)}: "
                               f"{cantidad} PV temporales (aura)")
        # Shielding Storm (10) y Raging Storm tundra (14).
        if self.level >= 10:
            self._otorgar_resistencia(actor, ctx)
        if self.level >= 14 and self.entorno == "tundra":
            self._elegir_velocidad_cero(actor, ctx)

    def on_rage_start(self, actor: Any, ctx: Any = None) -> None:
        """Entrar en Furia activa el aura por primera vez."""
        self.activar_aura(actor, ctx)

    # --- Storm Soul (6) + Shielding Storm (10) --------------------------------
    def _otorgar_resistencia(self, actor: Any, ctx: Any) -> None:
        """Concede a los aliados la resistencia de Storm Soul (temporal)."""
        tipo = parse_damage_type(self._tipo_alma)
        for aliado in _aliados_en_aura(actor, ctx):
            if tipo in (getattr(aliado, "resistances", None) or set()):
                continue  # ya la tiene por otro origen: no se toca
            aliado.resistances = set(aliado.resistances or set()) | {tipo}
            self._concedidas.append((aliado, tipo))
            _log_line(ctx, f"  {getattr(aliado, 'name', aliado)} gana "
                           f"resistencia a {tipo.value} (Shielding Storm)")

    def _revocar(self) -> None:
        """Retira SOLO las resistencias que este rasgo concedió."""
        for aliado, tipo in self._concedidas:
            resis = getattr(aliado, "resistances", None)
            if resis is not None:
                resis.discard(tipo)
        self._concedidas.clear()

    # --- Raging Storm (14) ---------------------------------------------------
    def after_being_hit(self, target: Any, attacker: Any, rango: Any,
                        ctx: Any = None) -> None:
        """Reacción tras recibir un impacto de un atacante en el aura."""
        if self.level < 14 or target is not self.owner or attacker is None:
            return
        if self.entorno == "tundra":  # sin reacción: solo al activar
            return
        if not self._furiosa:
            return
        if not getattr(self.owner, "alive", True):
            return
        if not getattr(attacker, "alive", True):
            return
        if not getattr(self.owner, "can_act", True):
            return
        hostil = getattr(self.owner, "is_hostile_to", None)
        if hostil is not None and not hostil(attacker):
            return
        estado = getattr(self.owner, "state", None)
        if estado is not None and getattr(estado, "reaction_used", False):
            return
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return  # sin RNG el rasgo se abstiene (no tira ni gasta)
        if not _en_aura(rng):  # el atacante tiene que estar en el aura
            return
        if pick(rng, ("no", "si")) == "no":
            return  # decisión aleatoria de usar la reacción
        if estado is not None:
            estado.reaction_used = True
        dc = _cd(self.owner)
        _log_line(ctx, f"{getattr(self.owner, 'name', self.owner)} usa su "
                       f"reacción (Raging Storm)")
        if self.entorno == "desert":
            sr = saving_throw(attacker, "dex", dc, rng, magical=True)
            registrar_resistencia(ctx, attacker, sr)
            if not sr.success:
                cantidad = int(self.level) // 2
                _log_line(ctx, f"  {getattr(attacker, 'name', attacker)}: "
                               f"{cantidad} de daño de fuego (fallo de "
                               f"salvación)")
                inflict_damage(attacker, cantidad, "fire",
                               source=self.owner, ctx=ctx, magical=True)
        else:  # sea
            sr = saving_throw(attacker, "str", dc, rng, magical=True)
            registrar_resistencia(ctx, attacker, sr)
            if not sr.success:
                apply_condition(attacker, Condition.PRONE, ctx,
                                source=self.owner, magical=True)

    def _elegir_velocidad_cero(self, actor: Any, ctx: Any) -> None:
        """Raging Storm tundra: UNA criatura, salvación de FUE, dato."""
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return
        pool = _enemigos_en_aura(actor, ctx)
        if not pool:
            return
        objetivo = pick(rng, pool)
        sr = saving_throw(objetivo, "str", _cd(actor), rng, magical=True)
        registrar_resistencia(ctx, objetivo, sr)
        if not sr.success:
            self.velocidad_cero = objetivo
            _log_line(ctx, f"  {getattr(objetivo, 'name', objetivo)}: "
                           f"velocidad 0 hasta el próximo turno del "
                           f"bárbaro (Raging Storm; dato, sin sistema "
                           f"de movimiento)")

    # --- Ciclo de turno ------------------------------------------------------
    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        """La velocidad 0 dura hasta el inicio del turno del bárbaro."""
        self.velocidad_cero = None

    def on_rage_end(self, actor: Any, ctx: Any = None) -> None:
        """El aura desaparece: se revocan las resistencias concedidas."""
        self._revocar()
        self.velocidad_cero = None

    def reset(self) -> None:
        self._revocar()
        self.velocidad_cero = None


class StormAuraAction(CombatAction):
    """Activar el aura de nuevo: bonus action (nivel ≥ 3, en Furia).

    La «acción adicional» se modela como bonus action (el motor solo
    ejecuta una ACTION y una BONUS_ACTION por turno); la decisión de
    usarla la toma el ``pick`` del encuentro entre candidatas.
    """

    def __init__(self) -> None:
        self.name = "Activar Aura de Tormenta"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # el límite es la Furia, no un recuento

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        herald = _de(actor, StormHeraldFeatures)
        if herald is None or herald.level < 3:
            return False
        if not herald._furiosa:
            return False
        # Desert/sea sin enemigos no hay nada que hacer; tundra siempre
        # (al menos el propio bárbaro está en su aura).
        if herald.entorno in ("desert", "sea"):
            return bool(valid_targets(actor, ctx))
        return True

    def execute(self, context: Any) -> None:
        actor = getattr(context, "actor", None)
        herald = _de(actor, StormHeraldFeatures) if actor is not None else None
        if herald is None:
            return
        herald.activar_aura(actor, context)


def apply_storm_herald(pj: Any, level: int | None = None,
                       entorno: str = "desert") -> StormHeraldFeatures:
    """Aplica la subclase Path of the Storm Herald a un PJ bárbaro.

    Exige que ``pj`` ya tenga :class:`BarbarianFeatures`
    (:func:`apply_barbarian`). ``entorno`` es la elección fija del PJ
    (``desert``/``sea``/``tundra``). En nivel ≥ 6 la resistencia de
    Storm Soul se añade ya (es permanente: sobrevive a ``reset``).
    """
    if _de(pj, BarbarianFeatures) is None:
        raise ValueError(
            "Primero aplica la clase bárbaro con apply_barbarian(pj)."
        )
    if entorno not in ENTORNOS:
        raise ValueError(
            f"Entorno desconocido {entorno!r}: válidos {list(ENTORNOS)}."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    trait = StormHeraldFeatures(name="Storm Herald", level=lvl,
                                entorno=entorno)
    trait.owner = pj
    pj.traits.append(trait)
    pj.actions.append(StormAuraAction())
    if lvl >= 6:
        # Storm Soul (6): permanente, como los datos de la ficha.
        tipo = parse_damage_type(_TIPO_POR_ENTORNO[entorno])
        pj.resistances = set(pj.resistances or set()) | {tipo}
    return trait


__all__ = ["ENTORNOS", "STORM_HERALD_FEATURES", "StormAuraAction",
           "StormHeraldFeatures", "apply_storm_herald"]

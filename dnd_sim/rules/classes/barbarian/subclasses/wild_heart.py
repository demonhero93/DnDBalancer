"""Subclase Path of the Wild Heart del bárbaro (PHB 2024).

Fuente: *Player's Handbook 2024* — Path of the Wild Heart (features en
niveles 3, 6, 10 y 14). No está ni en el SRD 2014 ni en la API, así que
la tabla va hardcodeada en :data:`WILD_HEART_FEATURES`. Aplica sobre la
Furia del proyecto (reglas 2024). Una sola clave de registro:
``wild_heart``.

Decisiones de simulación documentadas:

- **Elección por activación**: Rage of the Wilds (3) y Power of the
  Wilds (14) se eligen en CADA entrada en Furia con ``pick`` uniforme
  (un ``pick`` por opción) y se olvidan al terminar (``on_rage_end`` /
  ``reset``). Sin ``rng`` no se elige opción (el rasgo se abstiene).
  Falcon (14, velocidad de vuelo) queda FUERA del pick por no tener
  efecto mecánico sin posiciones (# TODO).
- **Animal Speaker** (3), **Aspect of the Wilds** (6: Owl/Panther/
  Salmon, un parámetro fijo del PJ, no aleatorio por activación) y
  **Nature Speaker** (10): rituales sin efecto en combate — solo dato
  del rasgo (# TODO).
- **Bear**: resistencia a todos los tipos salvo fuerza, necrótico,
  psíquico y radiante mientras dure la Furia, concedida con lista de
  fuente propia (``_concedidas``): al terminar se retira SOLO lo que
  este rasgo añadió, nunca una resistencia previa ajena. Los B/P/S no
  se añaden al set: ya los recorta la Furia base
  (``modify_incoming_damage``) durante la MISMA ventana y duplicarlos
  recortaría el daño a un cuarto (mismo efecto efectivo) (# TODO).
- **Eagle** (3): Disengage y Dash como acción adicional; sin sistema
  de movimiento no tienen efecto mecánico (# TODO), solo dato y log.
- **Wolf** (3): ventaja de los aliados del bárbaro (no de él mismo)
  al atacar a cualquier enemigo del bárbaro a 5 pies de él, cuerpo a
  cuerpo y a distancia, vía hook nuevo ``grant_attack_modifiers``
  (despachado desde ``attack_modifiers`` sobre los rasgos del resto de
  combatientes). Fuente «Lobo (Corazón Salvaje)».
- **Lion** (14): desventaja de los enemigos a 5 pies del bárbaro al
  atacar a otros objetivos; «este mismo beneficio» = un Wild Heart en
  Furia con la propia opción León (# TODO interpretación). Fuente
  «León (Corazón Salvaje)».
- **Sin posiciones**: «a 5 pies» usa
  :data:`WILD_HEART_COVERAGE_PROBABILITY` (mismo criterio que el aura
  del Storm Herald): 1.0/0.0 no consumen RNG; en medio, UNA tirada por
  criatura (# TODO).
- **Ram** (14): al acertar un ataque cuerpo a cuerpo con la opción
  activa contra una criatura Large o menor, ``pick`` de usarlo y PRONE
  sin salvación con el mismo ``EscapeCheck`` de Empujar (FUE/DES
  CD 10, sin gastar acción). Hook ``extra_attack_damage`` (el motor
  solo lo invoca en el golpe); sin ``rng`` no derriba. No se aplica a
  distancia (# TODO: alcance/«voluntaria» no modelados).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .....core.classes import MAX_LEVEL, MIN_LEVEL
from .....core.enums import AttackRange, DamageType
from .....core.log import log_line as _log_line
from .....core.randomness import pick
from ....conditions import Condition, EscapeCheck, apply_condition
from ....traits.base import Trait
from .._util import _de, _orden_de
from ..features import BarbarianFeatures

#: Features de subclase por nivel (PHB 2024; nombres en inglés).
WILD_HEART_FEATURES: dict[int, tuple[str, ...]] = {
    3: ("Animal Speaker", "Rage of the Wilds"),
    6: ("Aspect of the Wilds",),
    10: ("Nature Speaker",),
    14: ("Power of the Wilds",),
}

#: Opciones de Rage of the Wilds (nivel 3), elegidas en cada Furia.
RAGE_OPTIONS: tuple[str, ...] = ("bear", "eagle", "wolf")

#: Opciones de Power of the Wilds (nivel 14). Falcon queda fuera: sin
#: posiciones la velocidad de vuelo no tiene efecto mecánico (# TODO).
POWER_OPTIONS: tuple[str, ...] = ("lion", "ram")

#: Aspectos permanentes de Aspect of the Wilds (nivel 6): elección fija
#: del PJ al tomar el camino, no aleatoria por activación.
ASPECTOS: tuple[str, ...] = ("owl", "panther", "salmon")

#: Probabilidad por criatura de estar «a 5 pies» del bárbaro (sin
#: posiciones; mismo criterio que STORM_AURA_COVERAGE_PROBABILITY).
#: 1.0/0.0 no consumen RNG; en medio, UNA tirada por criatura.
WILD_HEART_COVERAGE_PROBABILITY: float = 1.0

#: Resistencias que concede Bear: todos los tipos salvo los 4
#: excluidos y los B/P/S (ver docstring: ya los da la Furia base).
_BEAR_EXCEPTO = frozenset({
    DamageType.FORCE, DamageType.NECROTIC,
    DamageType.PSYCHIC, DamageType.RADIANT,
    DamageType.BLUDGEONING, DamageType.PIERCING, DamageType.SLASHING,
})
_BEAR_RESISTENCIAS: frozenset[DamageType] = (
    frozenset(DamageType) - _BEAR_EXCEPTO
)

#: Fuentes de ventaja/desventaja en el log.
_FUENTE_LOBO = "Lobo (Corazón Salvaje)"
_FUENTE_LEON = "León (Corazón Salvaje)"


def _hostil(de: Any, contra: Any) -> bool:
    """¿``de`` es hostil a ``contra``? (sin función hostil: nunca)."""
    fn = getattr(de, "is_hostile_to", None)
    return bool(fn is not None and fn(contra))


def _en_5_pies(rng: Any) -> bool:
    """¿Está a 5 pies del bárbaro? (cobertura, sin posiciones)."""
    p = float(WILD_HEART_COVERAGE_PROBABILITY)
    if p <= 0.0:
        return False
    if p >= 1.0:
        return True
    if rng is None:
        return True  # sin RNG: cobertura completa (no inventa tiradas)
    return rng.random() < p


def _con_beneficio(combatiente: Any) -> bool:
    """¿Tiene el beneficio de protección de León (Wild Heart en Furia)?"""
    tr = _de(combatiente, WildHeartFeatures)
    return bool(tr is not None and tr.level >= 14 and tr._furiosa
                and tr.opcion_power == "lion")


@dataclass
class WildHeartFeatures(Trait):
    """Features de la subclase y estado de las opciones por Furia."""

    level: int = MIN_LEVEL
    #: Elección permanente de Aspect of the Wilds (nivel 6): dato.
    aspecto: str = "owl"
    #: Opción de Rage of the Wilds de la activación actual (o None).
    opcion_rage: str | None = None
    #: Opción de Power of the Wilds de la activación actual (o None).
    opcion_power: str | None = None
    #: Resistencias concedidas por Bear: solo las que ESTE rasgo añadió
    #: (si el PJ ya la tenía, no se registra ni se retira al terminar).
    _concedidas: list = field(default_factory=list, repr=False,
                              compare=False)
    owner: Any = field(default=None, repr=False, compare=False)

    @property
    def _furiosa(self) -> bool:
        barb = _de(self.owner, BarbarianFeatures)
        return bool(barb and barb.rage_active)

    # --- Rage of the Wilds (3) + Power of the Wilds (14) ----------------------
    def on_rage_start(self, actor: Any, ctx: Any = None) -> None:
        """Cada activación elige sus opciones con ``pick`` uniforme."""
        if self.level < 3 or ctx is None:
            return
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return  # sin RNG no se elige opción (no inventa)
        nombre = getattr(actor, "name", actor)
        self.opcion_rage = pick(rng, RAGE_OPTIONS)
        _log_line(ctx, f"{nombre} elige {self.opcion_rage} "
                       f"(Rage of the Wilds)")
        if self.opcion_rage == "bear":
            self._otorgar_bear(actor, ctx)
        elif self.opcion_rage == "eagle":
            _log_line(ctx, "  Águila: Disengage/Dash sin efecto "
                           "(sin sistema de movimiento)")
        if self.level >= 14:
            self.opcion_power = pick(rng, POWER_OPTIONS)
            _log_line(ctx, f"{nombre} elige {self.opcion_power} "
                           f"(Power of the Wilds)")

    def _otorgar_bear(self, actor: Any, ctx: Any) -> None:
        """Bear: resistencias temporales con lista de fuente propia."""
        previas = set(getattr(actor, "resistances", None) or set())
        nuevas = [t for t in sorted(_BEAR_RESISTENCIAS, key=lambda t: t.value)
                  if t not in previas]
        if not nuevas:
            return
        actor.resistances = previas | set(nuevas)
        for tipo in nuevas:
            self._concedidas.append((actor, tipo))
        _log_line(ctx, f"  {getattr(actor, 'name', actor)} gana "
                       f"resistencia a "
                       f"{', '.join(t.value for t in nuevas)} (Bear)")

    def _revocar(self) -> None:
        """Retira SOLO las resistencias que este rasgo concedió."""
        for objeto, tipo in self._concedidas:
            resis = getattr(objeto, "resistances", None)
            if resis is not None:
                resis.discard(tipo)
        self._concedidas.clear()

    # --- Wolf/Lion: ventaja/desventaja a ataques de terceros ------------------
    def grant_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                               rango: Any, ctx: Any = None,
                               rng: Any = None, atk: Any = None) -> None:
        """Wolf: ventaja de aliados; Lion: desventaja de enemigos a 5 pies."""
        if (self.level < 3 or self.owner is None or attacker is None
                or target is None or attacker is self.owner):
            return
        if not self._furiosa:
            return
        owner = self.owner
        if not _hostil(owner, attacker):
            # Wolf: aliado del bárbaro ataca a un enemigo del bárbaro.
            if (self.opcion_rage == "wolf" and _hostil(owner, target)
                    and _en_5_pies(rng)):
                mods.advantage_sources.append(_FUENTE_LOBO)
        elif (self.level >= 14 and self.opcion_power == "lion"
              and target is not owner and not _con_beneficio(target)
              and _en_5_pies(rng)):
            # Lion: enemigo a 5 pies ataca a otro objetivo.
            mods.disadvantage_sources.append(_FUENTE_LEON)

    # --- Ram (14): derribar al acertar ---------------------------------------
    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            crit: bool = False, ctx: Any = None,
                            rng: Any = None, atk: Any = None) -> int:
        """PRONE sin salvación al acertar en cuerpo a cuerpo (opción Ram).

        Devuelve siempre 0 (no añade daño): el efecto es la condición.
        El motor solo invoca este hook en el golpe, así que «solo si
        acierta» está garantizado; sin ``rng`` el rasgo se abstiene.
        """
        if (self.level < 14 or attacker is not self.owner
                or target is None or not self._furiosa):
            return 0
        if self.opcion_power != "ram":
            return 0
        if rango is not AttackRange.MELEE:
            return 0
        if _orden_de(target) > _orden_de("large"):
            return 0
        if rng is None:
            return 0  # sin RNG el rasgo se abstiene
        if pick(rng, ("no", "si")) == "no":
            return 0  # decisión aleatoria de usarlo
        apply_condition(target, Condition.PRONE, ctx, source=self.owner,
                        escape=EscapeCheck(abilities=("str", "dex"), dc=10,
                                           consumes_action=False))
        _log_line(ctx, f"{getattr(target, 'name', target)} cae derribado "
                       f"(Ram, Corazón Salvaje)")
        return 0

    # --- Ciclo de vida --------------------------------------------------------
    def on_rage_end(self, actor: Any, ctx: Any = None) -> None:
        """Termina la Furia: se olvidan las opciones y se revoca Bear."""
        self._revocar()
        self.opcion_rage = None
        self.opcion_power = None

    def reset(self) -> None:
        self._revocar()
        self.opcion_rage = None
        self.opcion_power = None


def apply_wild_heart(pj: Any, level: int | None = None,
                     aspecto: str = "owl") -> WildHeartFeatures:
    """Aplica la subclase Path of the Wild Heart a un PJ bárbaro.

    Exige que ``pj`` ya tenga :class:`BarbarianFeatures`
    (:func:`apply_barbarian`). ``aspecto`` es la elección permanente de
    Aspect of the Wilds (nivel 6): ``owl``/``panther``/``salmon``.
    """
    if _de(pj, BarbarianFeatures) is None:
        raise ValueError(
            "Primero aplica la clase bárbaro con apply_barbarian(pj)."
        )
    if aspecto not in ASPECTOS:
        raise ValueError(
            f"Aspecto desconocido {aspecto!r}: válidos {list(ASPECTOS)}."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    trait = WildHeartFeatures(name="Wild Heart", level=lvl,
                              aspecto=aspecto)
    trait.owner = pj
    pj.traits.append(trait)
    return trait


__all__ = ["ASPECTOS", "POWER_OPTIONS", "RAGE_OPTIONS",
           "WILD_HEART_COVERAGE_PROBABILITY", "WILD_HEART_FEATURES",
           "WildHeartFeatures", "apply_wild_heart"]

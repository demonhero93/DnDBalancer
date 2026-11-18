"""Subclase Path of Wild Magic del bárbaro (TCE 2020).

Fuente: *Tasha's Cauldron of Everything* — Path of Wild Magic (features
en niveles 3, 6, 10 y 14). No está ni en el SRD 2014 ni en la API, así
que la tabla va hardcodeada en :data:`WILD_MAGIC_FEATURES` y
:data:`WILD_SURGE_TABLE`. Aplica sobre la Furia del proyecto (reglas
2024). Una sola clave de registro: ``wild_magic``.

Decisiones de simulación documentadas:

- **Wild Surge** (3): al entrar en Furia se tira en la tabla de 8
  efectos con ``pick`` uniforme (el número de la tabla no importa) y la
  elección se renueva en cada activación. La tabla va como constante
  editable :data:`WILD_SURGE_TABLE` (nombre + función); la entrada 8
  está PENDIENTE de texto oficial (# TODO).
  - Shadowy Tendrils: instantáneo; enemigos a 30 pies hacen salvación
    de CON (CD 8 + PB + mod CON) y sufren 1d12 necrótico al fallar
    (``magical=True``); el bárbaro gana 1d12 PV temporales (no se
    acumulan: se queda el mayor; los PV temporales no se revocan al
    terminar la Furia, igual que el aura de tundra del Storm Herald).
  - Teleport, Flowers and Vines y la entrada 8: sin efecto mecánico
    (sin posiciones / pendiente), solo dato y log (# TODO).
  - Intangible Spirit: el efecto queda activo y la bonus action
    :class:`WildSurgeAction` (usage=None, patrón StormAuraAction)
    detona el espíritu contra UN enemigo elegido con ``pick``:
    salvación de DES, fallo = 1d6 de fuerza. La explosión de área de 5
    pies se resuelve en el acto sobre un solo objetivo (simplificación
    del enunciado, # TODO).
  - Magic Infusion: TODAS las armas del bárbaro pasan a ser mágicas
    mientras dure la Furia (``Attack.magical``), con lista de valores
    previos para restaurarlas (# TODO: la regla dice «un arma»).
  - Retribution: tras recibir un impacto de un enemigo, la criatura
    sufre daño de fuerza = ``rage_damage(level)`` (mágico), sin
    reacción ni límite por ronda; decisión con ``pick``; alcance no
    modelado (# TODO).
  - Bolstering Magic: sin efecto mecánico (no hay hook de bono plano a
    la tirada de ataque y no se crea uno solo por esto; # TODO).
- **Controlled Surge** (14): al tirar en la tabla (entrada en Furia y
  re-tiras de Unstable Backlash) se tiran DOS efectos y se elige uno con
  ``pick``.
- **Unstable Backlash** (10): patrón de reacción de Raging Storm
  (guardas de vida/hostilidad/can_act, una reacción por ronda vía
  ``state.reaction_used``, sin RNG se abstiene, decisión con ``pick``)
  tras recibir un impacto (hook ``after_being_hit``) o fallar una
  salvación (hook nuevo ``after_failed_save``, despachado desde
  ``registrar_resistencia``): revoca el efecto actual (los
  instantáneos ya se aplicaron) y vuelve a tirar en la tabla.
- **Magic Awareness** (3), **Bolstering Magic** (6, acción adicional
  con usos por descanso) y los efectos de exploración: sin efecto en
  combate, solo dato del rasgo (# TODO).
- **Sin posiciones**: «a 30 pies» usa
  :data:`WILD_MAGIC_COVERAGE_PROBABILITY` (mismo criterio que el aura
  del Storm Herald): 1.0/0.0 no consumen RNG; en medio, UNA tirada por
  criatura (# TODO).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .....core.classes import MAX_LEVEL, MIN_LEVEL, rage_damage
from .....core.dice import roll_dice
from .....core.log import log_line as _log_line
from .....core.randomness import pick
from .....core.targeting import valid_targets
from .....model.actions import ActionType, CombatAction
from ....damage import inflict_damage
from ....saves import registrar_resistencia, saving_throw
from ....traits.base import Trait
from .._util import _de
from ..features import BarbarianFeatures, _contexto

#: Features de subclase por nivel (TCE 2020; nombres en inglés).
WILD_MAGIC_FEATURES: dict[int, tuple[str, ...]] = {
    3: ("Magic Awareness", "Wild Surge"),
    6: ("Bolstering Magic",),
    10: ("Unstable Backlash",),
    14: ("Controlled Surge",),
}

#: Probabilidad por criatura de estar «a 30 pies» (sin posiciones;
#: mismo criterio que STORM_AURA_COVERAGE_PROBABILITY). 1.0/0.0 no
#: consumen RNG; en medio, UNA tirada por criatura.
WILD_MAGIC_COVERAGE_PROBABILITY: float = 1.0

#: Nombres de efecto que necesitan estado (no son instantáneos).
_ESPIRITU = "Intangible Spirit"
_INFUSION = "Magic Infusion"
_RETRIBUCION = "Retribution"


def _cd(actor: Any) -> int:
    """CD de las salvaciones de la subclase: 8 + competencia + mod CON."""
    con = 0
    try:
        con = actor.abilities.mod("con")
    except Exception:
        pass
    return 8 + int(getattr(actor, "proficiency", 0) or 0) + int(con)


def _en_30_pies(rng: Any) -> bool:
    """¿Está a 30 pies del bárbaro? (cobertura, sin posiciones)."""
    p = float(WILD_MAGIC_COVERAGE_PROBABILITY)
    if p <= 0.0:
        return False
    if p >= 1.0:
        return True
    if rng is None:
        return True  # sin RNG: cobertura completa (no inventa tiradas)
    return rng.random() < p


def _enemigos(actor: Any, ctx: Any) -> list:
    """Enemigos vivos a 30 pies (criterio de rules/area)."""
    rng = getattr(ctx, "rng", None)
    return [c for c in valid_targets(actor, ctx) if _en_30_pies(rng)]


# --- Efectos de la tabla Wild Surge ------------------------------------------

def _sombra(trait: Any, actor: Any, ctx: Any) -> None:
    """Shadowy Tendrils: salvación CON o 1d12 necrótico; 1d12 PV temp."""
    rng = getattr(ctx, "rng", None)
    if rng is None:
        return
    dc = _cd(actor)
    for objetivo in _enemigos(actor, ctx):
        sr = saving_throw(objetivo, "con", dc, rng, magical=True)
        registrar_resistencia(ctx, objetivo, sr)
        if not sr.success:
            bruto = roll_dice("1d12", rng)
            _log_line(ctx, f"  {getattr(objetivo, 'name', objetivo)}: "
                           f"{bruto} de daño necrótico (fallo de salvación)")
            inflict_damage(objetivo, bruto, "necrotic", source=actor,
                           ctx=ctx, magical=True)
    curados = roll_dice("1d12", rng)
    actual = int(getattr(actor, "temp_hp", 0) or 0)
    actor.temp_hp = max(actual, curados)  # no se acumula
    _log_line(ctx, f"  {getattr(actor, 'name', actor)}: {curados} PV "
                   f"temporales (Shadowy Tendrils)")


def _teletransporte(trait: Any, actor: Any, ctx: Any) -> None:
    """Teleport: sin posiciones no tiene efecto mecánico."""
    _log_line(ctx, "  Teleport: sin efecto (sin sistema de movimiento)")


def _espiritu(trait: Any, actor: Any, ctx: Any) -> None:
    """Intangible Spirit: el efecto queda activo para la bonus action."""
    _log_line(ctx, "  Espíritu intangible: usa la acción adicional para "
                   "detonarlo")


def _infusion(trait: Any, actor: Any, ctx: Any) -> None:
    """Magic Infusion: las armas del bárbaro son mágicas (temporal)."""
    previas = [(atk, bool(getattr(atk, "magical", False)))
               for atk in (getattr(actor, "attacks", None) or [])]
    trait._armas_previas = previas
    for atk, _ in previas:
        atk.magical = True
    _log_line(ctx, "  Magic Infusion: las armas del bárbaro son mágicas")


def _retribucion(trait: Any, actor: Any, ctx: Any) -> None:
    """Retribution: estado que revisa ``after_being_hit``."""
    _log_line(ctx, "  Retribution: daño de fuerza tras recibir un impacto")


def _bolstering(trait: Any, actor: Any, ctx: Any) -> None:
    """Bolstering Magic: sin bono plano a la tirada, sin efecto."""
    _log_line(ctx, "  Bolstering Magic: sin efecto (1d3 a ataques no "
                   "modelado)")


def _flores(trait: Any, actor: Any, ctx: Any) -> None:
    """Flowers and Vines: terreno difícil sin posiciones, sin efecto."""
    _log_line(ctx, "  Flowers and Vines: terreno difícil sin efecto "
                   "(sin posiciones)")


def _pendiente(trait: Any, actor: Any, ctx: Any) -> None:
    """Octava entrada: pendiente de texto oficial."""
    _log_line(ctx, "  Wild Surge pendiente: sin efecto mecánico (pendiente)")


#: Tabla Wild Surge de 8 efectos (nombre + función de activación).
#: La entrada 8 está PENDIENTE de texto oficial (# TODO).
WILD_SURGE_TABLE: tuple[tuple[str, Any], ...] = (
    ("Shadowy Tendrils", _sombra),
    ("Teleport", _teletransporte),
    ("Intangible Spirit", _espiritu),
    ("Magic Infusion", _infusion),
    ("Retribution", _retribucion),
    ("Bolstering Magic", _bolstering),
    ("Flowers and Vines", _flores),
    ("Pendiente", _pendiente),
)


@dataclass
class WildMagicFeatures(Trait):
    """Features de la subclase y estado del efecto de Wild Surge."""

    level: int = MIN_LEVEL
    #: Efecto activo de Wild Surge de la Furia actual (o None).
    efecto: str | None = None
    #: ``(arma, magical_previo)`` de Magic Infusion: para restaurar.
    _armas_previas: list = field(default_factory=list, repr=False,
                                 compare=False)
    owner: Any = field(default=None, repr=False, compare=False)

    @property
    def _furiosa(self) -> bool:
        barb = _de(self.owner, BarbarianFeatures)
        return bool(barb and barb.rage_active)

    # --- Wild Surge (3) + Controlled Surge (14) -------------------------------
    def on_rage_start(self, actor: Any, ctx: Any = None) -> None:
        """Entrar en Furia tira en la tabla de Wild Surge."""
        if self.level < 3 or ctx is None:
            return
        if getattr(ctx, "rng", None) is None:
            return  # sin RNG no se tira (no inventa)
        self._tirar_surge(actor, ctx)

    def _tirar_surge(self, actor: Any, ctx: Any) -> None:
        """Tira en la tabla (dos veces en 14) y aplica el efecto."""
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return
        entradas = [pick(rng, WILD_SURGE_TABLE)]
        if self.level >= 14:  # Controlled Surge: dos, se queda con una
            entradas.append(pick(rng, WILD_SURGE_TABLE))
            entradas = [pick(rng, entradas)]
        self._revocar()  # el efecto anterior termina (los instantáneos no)
        nombre, funcion = entradas[0]
        self.efecto = nombre
        _log_line(ctx, f"{getattr(actor, 'name', actor)} tira en Wild "
                       f"Surge: {nombre}")
        funcion(self, actor, ctx)

    def _revocar(self) -> None:
        """Termina el efecto actual: restaura las armas y limpia."""
        for atk, previo in self._armas_previas:
            atk.magical = previo
        self._armas_previas.clear()
        self.efecto = None

    # --- Retribution (5) + Unstable Backlash (10) -----------------------------
    def after_being_hit(self, target: Any, attacker: Any, rango: Any,
                        ctx: Any = None) -> None:
        """Retribution al impactar y Unstable Backlash como reacción."""
        if self.level < 3 or target is not self.owner or attacker is None:
            return
        if not self._furiosa:
            return
        owner = self.owner
        if not getattr(owner, "alive", True):
            return
        if not getattr(attacker, "alive", True):
            return
        if not getattr(owner, "can_act", True):
            return
        hostil = getattr(owner, "is_hostile_to", None)
        if hostil is not None and not hostil(attacker):
            return
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return  # sin RNG el rasgo se abstiene
        # Retribution: daño de fuerza = daño de Furia, sin reacción.
        if self.efecto == _RETRIBUCION:
            if pick(rng, ("no", "si")) != "no":
                cantidad = rage_damage(self.level)
                _log_line(ctx, f"  {getattr(attacker, 'name', attacker)}: "
                               f"{cantidad} de daño de fuerza (Retribution)")
                inflict_damage(attacker, cantidad, "force", source=owner,
                               ctx=ctx, magical=True)
        # Unstable Backlash (10): reacción, una por ronda.
        self._backlash(ctx, rng)

    def after_failed_save(self, target: Any, ability: str, result: Any,
                          ctx: Any = None) -> None:
        """Unstable Backlash también tras fallar una salvación."""
        if self.level < 10 or target is not self.owner or ctx is None:
            return
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return
        self._backlash(ctx, rng)

    def _backlash(self, ctx: Any, rng: Any) -> None:
        """Reacción Unstable Backlash: revoca y vuelve a tirar."""
        if self.level < 10 or not self._furiosa:
            return
        owner = self.owner
        if not getattr(owner, "alive", True):
            return
        if not getattr(owner, "can_act", True):
            return
        estado = getattr(owner, "state", None)
        if estado is not None and getattr(estado, "reaction_used", False):
            return
        if pick(rng, ("no", "si")) == "no":
            return  # decisión aleatoria de usar la reacción
        if estado is not None:
            estado.reaction_used = True
        _log_line(ctx, f"{getattr(owner, 'name', owner)} usa su reacción "
                       f"(Unstable Backlash)")
        self._tirar_surge(owner, ctx)

    # --- Ciclo de vida --------------------------------------------------------
    def on_rage_end(self, actor: Any, ctx: Any = None) -> None:
        """Termina la Furia: el efecto activo se revoca."""
        self._revocar()

    def reset(self) -> None:
        self._revocar()


class WildSurgeAction(CombatAction):
    """Detonar el espíritu intangible: bonus action (nivel ≥ 3, en Furia).

    Solo está disponible si el efecto activo es Intangible Spirit. La
    «acción adicional» se modela como bonus action (patrón
    StormAuraAction); la decisión de usarla la toma el ``pick`` del
    encuentro entre candidatas.
    """

    def __init__(self) -> None:
        self.name = "Espíritu intangible"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # el límite es la Furia, no un recuento

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        magia = _de(actor, WildMagicFeatures)
        if magia is None or magia.level < 3:
            return False
        if not magia._furiosa:
            return False
        if magia.efecto != _ESPIRITU:
            return False
        return bool(valid_targets(actor, ctx))

    def execute(self, context: Any) -> None:
        actor = getattr(context, "actor", None)
        magia = _de(actor, WildMagicFeatures) if actor is not None else None
        if magia is None:
            return
        rng = getattr(context, "rng", None)
        if rng is None:
            return
        pool = _enemigos(actor, context)
        if not pool:
            return
        objetivo = pick(rng, pool)  # UN enemigo (sin explosión de área)
        sr = saving_throw(objetivo, "dex", _cd(actor), rng, magical=True)
        registrar_resistencia(context, objetivo, sr)
        if sr.success:
            _log_line(context, f"  {getattr(objetivo, 'name', objetivo)}: "
                               f"salvación DES exitosa (espíritu)")
            return
        bruto = roll_dice("1d6", rng)
        _log_line(context, f"  {getattr(objetivo, 'name', objetivo)}: "
                           f"{bruto} de daño de fuerza (fallo de salvación)")
        inflict_damage(objetivo, bruto, "force", source=actor,
                       ctx=context, magical=True)


def apply_wild_magic(pj: Any, level: int | None = None) -> WildMagicFeatures:
    """Aplica la subclase Path of Wild Magic a un PJ bárbaro.

    Exige que ``pj`` ya tenga :class:`BarbarianFeatures`
    (:func:`apply_barbarian`).
    """
    if _de(pj, BarbarianFeatures) is None:
        raise ValueError(
            "Primero aplica la clase bárbaro con apply_barbarian(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    trait = WildMagicFeatures(name="Wild Magic", level=lvl)
    trait.owner = pj
    pj.traits.append(trait)
    pj.actions.append(WildSurgeAction())
    return trait


__all__ = ["WILD_MAGIC_COVERAGE_PROBABILITY", "WILD_MAGIC_FEATURES",
           "WILD_SURGE_TABLE", "WildMagicFeatures", "WildSurgeAction",
           "apply_wild_magic"]

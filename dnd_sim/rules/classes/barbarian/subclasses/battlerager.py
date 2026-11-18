"""Subclase Battlerager del bárbaro (SCAG).

Fuente: *Sword Coast Adventurer's Guide* — Path of the Battlerager
(features en niveles 3, 6, 10 y 14, mismos huecos que el bárbaro PHB).
No está ni en el SRD 2014 ni en la API 2024, así que la tabla de
features va hardcodeada en :data:`BATTLERAGER_FEATURES`.

Decisiones de simulación documentadas:

- **Battlerager Armor** (3): el ataque de púas es una acción bonus
  (:class:`SpikedArmorAction`, un :class:`AttackAction` con
  ``action_type=BONUS_ACTION``) solo disponible con Furia: tira 1d4 +
  mod FUE y recibe el daño de Furia por ser un ataque de FUE. El daño
  extra de 3 al agarrar (grapple) **no está modelado**: el simulador no
  tiene acciones de agarrar.
- **Reckless Abandon** (6): mientras dure la Furia, cada ataque de FUE
  (política de simulación: siempre con Ataque Temerario) concede PV
  temporales iguales al mod de CON (mínimo 1); como en 5e no apilan,
  solo se reemplazan si la cantidad es mayor. Son PV temporales de
  verdad (:attr:`dnd_sim.model.combatant.Combatant.temp_hp`, fase 1c de
  :func:`dnd_sim.rules.damage.inflict_damage`) y desaparecen cuando la
  Furia termina (limpieza en ``on_turn_start``/``on_turn_end``, después
  del bárbaro en la lista de rasgos, que es quien desactiva la Furia).
- **Battlerager Charge** (10): Dash como acción bonus con Furia — no
  modelado (no hay sistema de movimiento).
- **Spiked Retribution** (14): con Furia, un acierto cuerpo a cuerpo
  contra el bárbaro devuelve 3 perforante fijos al atacante
  (``after_being_hit``, patrón Heated Body). «Wearing spiked armor» se
  da por supuesto (no hay sistema de armaduras).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .....core.classes import MAX_LEVEL, MIN_LEVEL
from .....core.enums import AttackRange
from .....core.log import log_line as _log_line
from .....model.actions import ActionType, AttackAction
from .....model.attack import Attack
from ....damage import apply_damage_modifiers, inflict_damage
from ....traits.base import Trait
from .._util import _de
from ..features import BarbarianFeatures, _contexto

#: Features de subclase por nivel (SCAG; nombres en inglés como la API).
BATTLERAGER_FEATURES: dict[int, tuple[str, ...]] = {
    3: ("Battlerager Armor",),
    6: ("Reckless Abandon",),
    10: ("Battlerager Charge",),
    14: ("Spiked Retribution",),
}


def _nuevo_ataque() -> Attack:
    """Ataque con las púas de la armadura (1d4 perforante de FUE)."""
    return Attack("Armadura con púas", "1d4", ability="str",
                  damage_type="piercing")


@dataclass
class BattleragerFeatures(Trait):
    """Features de la subclase y estado de los PV temporales."""

    level: int = MIN_LEVEL
    #: ¿Concedimos nosotros los PV temporales (para anularlos con la Furia)?
    abandono_temp: bool = field(default=False, repr=False, compare=False)
    owner: Any = field(default=None, repr=False, compare=False)

    @property
    def _furiosa(self) -> bool:
        barb = _de(self.owner, BarbarianFeatures)
        return bool(barb and barb.rage_active)

    def _limpiar_si_no_furia(self) -> None:
        """Anula los PV temporales concedidos si la Furia ya no está."""
        if not self.abandono_temp or self.owner is None:
            return
        barb = _de(self.owner, BarbarianFeatures)
        if barb is None or not barb.rage_active:
            try:
                self.owner.temp_hp = 0
            except Exception:
                pass
            self.abandono_temp = False

    # --- Reckless Abandon (6) -------------------------------------------------
    def modify_attack_modifiers(self, mods: Any, attacker: Any,
                                target: Any, rango: Any, ctx: Any = None,
                                rng: Any = None, atk: Any = None) -> None:
        """Cada ataque de FUE con Furia concede PV temporales (CON, mín. 1)."""
        if self.level < 6 or self.owner is None or attacker is not self.owner:
            return
        barb = _de(self.owner, BarbarianFeatures)
        if barb is None or not barb.rage_active:
            return
        if atk is not None and not BarbarianFeatures._es_fue(atk):
            return  # solo los ataques de FUE usan Ataque Temerario
        try:
            con = int(self.owner.abilities.mod("con"))
        except Exception:
            con = 0
        valor = max(1, con)
        try:
            actual = int(getattr(self.owner, "temp_hp", 0) or 0)
        except Exception:
            actual = 0
        # Regla 5e de PV temporales: no apilan; manda la mayor cantidad.
        if valor > actual:
            self.owner.temp_hp = valor
            self.abandono_temp = True
            _log_line(
                ctx,
                f"{getattr(self.owner, 'name', self.owner)} gana "
                f"{valor} PV temporales (Abandono Temerario)",
            )

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        """Si la Furia terminó por Incapacitado, los temporales caen ya."""
        self._limpiar_si_no_furia()

    def on_turn_end(self, actor: Any, ctx: Any = None) -> None:
        """«They vanish if any of them are left when your rage ends.»"""
        self._limpiar_si_no_furia()

    def reset(self) -> None:
        self.abandono_temp = False

    # --- Spiked Retribution (14) ---------------------------------------------
    def after_being_hit(self, target: Any, attacker: Any, rango: Any,
                        ctx: Any = None) -> None:
        """3 perforante fijos al atacante cuerpo a cuerpo, con Furia."""
        if self.level < 14 or target is not self.owner or attacker is None:
            return
        if rango is not AttackRange.MELEE:
            return
        if not self._furiosa:
            return
        cantidad = apply_damage_modifiers(3, "piercing", attacker)
        inflict_damage(attacker, cantidad, "piercing",
                       source=self.owner, ctx=ctx)
        _log_line(
            ctx,
            f"{getattr(target, 'name', target)} clava sus púas a "
            f"{getattr(attacker, 'name', attacker)}: {cantidad} "
            f"daño de perforante (Retribución de Púas)",
        )


@dataclass
class SpikedArmorAction(AttackAction):
    """Ataque con las púas: acción bonus, solo con Furia (nivel ≥ 3)."""

    action_type: ActionType = ActionType.BONUS_ACTION

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        context = _contexto(args, kwargs)
        actor = getattr(context, "actor", None)
        if actor is None:
            return False
        brazo = _de(actor, BattleragerFeatures)
        barb = _de(actor, BarbarianFeatures)
        if brazo is None or brazo.level < 3 or barb is None:
            return False
        return bool(barb.rage_active)


def apply_battlerager(pj: Any, level: int | None = None) -> BattleragerFeatures:
    """Aplica la subclase Path of the Battlerager a un PJ bárbaro.

    Exige que ``pj`` ya tenga :class:`BarbarianFeatures`
    (:func:`apply_barbarian`). Añade el trait de subclase y la acción
    bonus de la armadura con púas.
    """
    if _de(pj, BarbarianFeatures) is None:
        raise ValueError(
            "Primero aplica la clase bárbaro con apply_barbarian(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    trait = BattleragerFeatures(name="Battlerager", level=lvl)
    trait.owner = pj
    pj.traits.append(trait)
    pj.actions.append(SpikedArmorAction(_nuevo_ataque()))
    return trait


__all__ = ["BATTLERAGER_FEATURES", "BattleragerFeatures",
           "SpikedArmorAction", "apply_battlerager"]

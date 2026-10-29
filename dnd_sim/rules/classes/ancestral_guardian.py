"""Subclase Guardián Ancestral del bárbaro (XGtE).

Fuente: *Xanathar's Guide to Everything* — Path of the Ancestral Guardian
(features en niveles 3, 6, 10 y 14, mismos huecos que el bárbaro PHB).
No está en el SRD que sirve la API (solo Path of the Berserker), así que
la tabla de features va hardcodeada en :data:`ANCESTRAL_FEATURES`.

Decisiones de simulación documentadas:

- **Ancestral Protectors** (3): la marca vive en ``state.marked_by`` del
  marcado. ``attack_modifiers`` resta ventaja al marcado salvo contra su
  marcador y ``attack_roll`` reduce a la mitad su daño principal contra
  otros (como resistencia, una sola vez). Solo marca la primera criatura
  golpeada en el turno, solo mientras dure la Furia, y el efecto muere
  con la Furia o al empezar el siguiente turno del bárbaro.
- **Distancia y visión**: «within 30 feet» y «you can see» se dan por
  ciertos (no hay sistema de distancia/visión).
- **Spirit Shield** (6): reacción que usa ``state.reaction_used`` igual
  que Parry. Cualquier daño de otro combatiente con contexto puede
  reducirse (:func:`dnd_sim.rules.damage.inflict_damage`, fase 1b sobre
  ``ctx.combatants``); solo con Furia activa y sin gastar la reacción.
- **Consult the Spirits** (10): Augury/Clairvoyance de utilidad con
  descanso corto — no está modelado.
- **Vengeful Ancestors** (14): el atacante recibe como daño de fuerza
  lo que el escudo acaba de evitar.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ...core.classes import MAX_LEVEL, MIN_LEVEL
from ...core.dice import roll_dice
from ...core.enums import parse_damage_type
from ...core.log import log_line as _log_line
from ..traits.base import Trait
from .barbarian import BarbarianFeatures

#: Features de subclase por nivel (XGtE; nombres en inglés como la API).
ANCESTRAL_FEATURES: dict[int, tuple[str, ...]] = {
    3: ("Ancestral Protectors",),
    6: ("Spirit Shield",),
    10: ("Consult the Spirits",),
    14: ("Vengeful Ancestors",),
}


@dataclass
class AncestralGuardianFeatures(Trait):
    """Features de la subclase y estado de la marca ancestral."""

    level: int = MIN_LEVEL
    #: Primera criatura golpeada en el turno (None = sin marca).
    marked: Any = field(default=None, repr=False, compare=False)
    #: Ronda en la que ya se marcó (para respetar «la primera» del turno).
    mark_hit_round: int = -1

    @staticmethod
    def _barbaro(actor: Any) -> BarbarianFeatures | None:
        """Rasgo de clase (Furia) de ``actor``, si lo lleva."""
        for trait in getattr(actor, "traits", None) or []:
            if isinstance(trait, BarbarianFeatures):
                return trait
        return None

    @property
    def _furiosa(self) -> bool:
        barb = self._barbaro(self.owner)
        return bool(barb and barb.rage_active)

    def _limpiar_marca(self) -> None:
        """Quita la marca del combatiente que la llevaba (si aún existe)."""
        marcado = self.marked
        self.marked = None
        if marcado is None:
            return
        try:
            marcado.state.marked_by = None
        except Exception:
            pass

    # --- Ancestral Protectors (3) -------------------------------------------
    def after_dealing_hit(self, target: Any, attacker: Any, rango: Any,
                          ctx: Any = None) -> None:
        """Marca a la primera criatura golpeada en el turno, con Furia."""
        if self.level < 3:
            return
        barb = self._barbaro(attacker)
        if barb is None or not barb.rage_active:
            return
        round_ = int(getattr(ctx, "round", 0) or 0)
        if self.mark_hit_round == round_:
            return  # «the first creature you hit on your turn»
        self.mark_hit_round = round_
        self._limpiar_marca()
        self.marked = target
        estado = getattr(target, "state", None)
        if estado is not None:
            estado.marked_by = attacker
        _log_line(ctx, f"{getattr(attacker, 'name', attacker)} marca con "
                       f"los espíritus a {getattr(target, 'name', target)}")

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        """La marca dura hasta el inicio del siguiente turno del bárbaro."""
        self._limpiar_marca()
        self.mark_hit_round = -1

    def on_turn_end(self, actor: Any, ctx: Any = None) -> None:
        """Si la Furia termina, la marca termina con ella."""
        if self.marked is not None and not self._furiosa:
            self._limpiar_marca()

    # --- Spirit Shield (6) + Vengeful Ancestors (14) -------------------------
    def reduce_damage_to_allies(self, target: Any, amount: int,
                                damage_type: Any = None,
                                source: Any = None,
                                ctx: Any = None) -> int | None:
        """Reacción: reduce el daño que recibe otro combatiente."""
        if self.level < 6 or self.owner is None:
            return None
        if target is self.owner:
            return None  # «another creature you can see»
        if not self._furiosa:
            return None  # «If you are raging»
        estado = getattr(self.owner, "state", None)
        if estado is not None and getattr(estado, "reaction_used", False):
            return None  # su reacción de este turno ya está gastada
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return None  # sin generador no se tira: se abstiene
        dados = "2d6" if self.level < 10 else ("3d6" if self.level < 14
                                               else "4d6")
        reducido = min(int(amount), int(roll_dice(dados, rng)))
        if reducido <= 0:
            return None
        if estado is not None:
            estado.reaction_used = True
        _log_line(ctx, f"Espíritu Guardián de "
                       f"{getattr(self.owner, 'name', self.owner)} reduce "
                       f"{reducido} de daño a {getattr(target, 'name', target)}")
        if self.level >= 14 and source is not None:
            # Vengeful Ancestors: lo evitado vuelve al atacante como
            # fuerza. La reacción ya está gastada, así que este daño no
            # vuelve a entrar por esta misma vía.
            from ..damage import inflict_damage
            inflict_damage(source, reducido, parse_damage_type("force"),
                           source=self.owner, ctx=ctx, rng=rng)
        return max(0, int(amount) - reducido)

    def reset(self) -> None:
        """Limpia la marca al empezar un combate nuevo."""
        self._limpiar_marca()
        self.mark_hit_round = -1


def apply_ancestral_guardian(pj: Any, level: int | None = None,
                             ) -> AncestralGuardianFeatures:
    """Añade la subclase Guardián Ancestral a un PJ bárbaro.

    Requiere :func:`dnd_sim.rules.classes.barbarian.apply_barbarian` ya
    aplicado (la Furia es la base de casi todas sus features). El nivel
    por defecto es el del PJ (o 1, como en la clase); por debajo de 3 la
    marca no se aplica, igual que en la mesa.
    """
    if AncestralGuardianFeatures._barbaro(pj) is None:
        raise ValueError(
            "Primero aplica la clase bárbaro con apply_barbarian(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    if lvl is None:
        lvl = MIN_LEVEL
    lvl = max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    trait = AncestralGuardianFeatures(name="Guardian Ancestral", level=lvl)
    trait.owner = pj
    pj.traits.append(trait)
    return trait


__all__ = ["ANCESTRAL_FEATURES", "AncestralGuardianFeatures",
           "apply_ancestral_guardian"]

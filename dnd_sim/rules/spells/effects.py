"""Efectos que aplican los hechizos: curaciones, estados y
su mantenimiento (concentración)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..conditions import Condition, apply_condition
from ...core.dice import roll_dice


@dataclass
class HealEffect:
    """Curación de un hechizo (dados ya resueltos: "1d8 + 5")."""

    heal: str = "1d8"

    def amount(self, rng) -> int:
        """Puntos de vida curados."""
        try:
            return int(roll_dice(self.heal, rng))
        except Exception:
            return 0


@dataclass
class StateEffect:
    """Estado que aplica un hechizo (sin salvación: el hechizo lo decide).

    ``target``: ``"self"`` (el lanzador) o ``"ally"`` (un aliado).
    ``break_on_attack``: si el estado termina al atacar o al lanzar un
    hechizo (la invisibilidad estándar). La Superior Invisibility de la
    pixie, que dura lo que su concentración, lo pone a ``False``.
    """

    condition: Any = None
    duration_rounds: int | None = None
    target: str = "self"
    break_on_attack: bool = True


def _tiene_estado(actor: Any, condition: Any) -> bool:
    """¿Ya tiene ``actor`` la condición ``condition``? (sin excepciones)."""
    if actor is None or condition is None:
        return False
    try:
        return bool(actor.conditions.has(condition))
    except Exception:
        return False


def apply_concentration(caster: Any, ctx: Any,
                        duration_rounds: int | None = None) -> None:
    """Concentra: termina la concentración anterior y aplica la nueva.

    Solo se puede mantener una concentración por lanzador (lanzar otro
    hechizo concentrado termina el anterior).
    """
    tracker = getattr(caster, "conditions", None)
    if tracker is None:
        return
    try:
        for instance in list(getattr(tracker, "instances", []) or []):
            if instance.condition is Condition.CONCENTRATION:
                tracker.remove_instance(instance)
    except Exception:
        pass
    try:
        apply_condition(caster, Condition.CONCENTRATION, ctx, source=caster,
                        duration_rounds=duration_rounds)
    except Exception:
        pass

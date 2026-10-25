"""Pruebas de característica de D&D 5e.

Regla 5e: en una prueba de característica el **20 natural NO es éxito
automático** y el **1 natural NO es fallo automático**: el éxito depende
solo de ``total >= cd``.

Estas pruebas permiten escapar de estados (por ejemplo, liberarse de la
telaraña de la araña gigante). Se tiran al **inicio del turno** del
afectado: no son una elección, son automáticas.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from .dice import RollMode, roll_d20
from .roll_modifiers import check_modifiers

from .saves import normalize_ability


@dataclass
class CheckResult:
    """Resultado de una prueba de característica."""

    ability: str
    dc: int
    rolls: list[int]
    bonus: int
    total: int
    success: bool
    mode: RollMode


def ability_check_bonus(target: Any, ability: str) -> int:
    """Modificador de la característica para una prueba.

    # TODO: competencia en habilidades (no modelada).
    """
    try:
        return int(target.abilities.mod(ability))
    except Exception:
        return 0


def _guia(target: Any, rng: Any) -> int:
    """Bonus de la guía (+1d4) y consumo del estado, si lo hay.

    El hechizo de guía da +1d4 a **una** prueba de característica: al
    usarla, la guía se consume (el hechizo termina).
    """
    try:
        from .conditions import Condition
        tracker = getattr(target, "conditions", None)
        if tracker is None or not tracker.has(Condition.GUIDED):
            return 0
    except Exception:
        return 0
    total = 0
    if rng is not None:
        try:
            total = int(rng.randint(1, 4))
        except Exception:
            total = 0
    # La guía se consume: el hechizo termina tras la prueba.
    try:
        from .conditions import Condition
        tracker = getattr(target, "conditions", None)
        for instance in list(getattr(tracker, "instances", []) or []):
            if instance.condition is Condition.GUIDED:
                tracker.remove_instance(instance)
    except Exception:
        pass
    return total


def ability_check(target: Any, ability: str, dc: int, rng: random.Random,
                  mode: Any = None) -> CheckResult:
    """Tira una prueba de característica.

    Usa ventaja/desventaja según :func:`check_modifiers` (y no el 20 natural
    como éxito automático).
    """
    ab = normalize_ability(ability)
    if mode is None:
        mode = check_modifiers(target, ab).mode
    else:
        text = str(mode).strip().lower()
        mode = RollMode(text) if text in {m.value for m in RollMode} else RollMode.NORMAL
    bonus = ability_check_bonus(target, ab)
    # El hechizo de guía añade +1d4 a una prueba (y se consume).
    bonus += _guia(target, rng)
    result = roll_d20(rng, mode)
    total = result.value + bonus
    success = total >= int(dc)
    return CheckResult(
        ability=ab,
        dc=int(dc),
        rolls=list(result.rolls),
        bonus=int(bonus),
        total=int(total),
        success=bool(success),
        mode=mode,
    )


__all__ = ["CheckResult", "ability_check", "ability_check_bonus"]

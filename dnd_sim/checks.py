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

try:
    from .dice import RollMode, roll_d20
    from .roll_modifiers import check_modifiers
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from dice import RollMode, roll_d20
        from roll_modifiers import check_modifiers
    except ImportError:
        from dnd_sim.dice import RollMode, roll_d20
        from dnd_sim.roll_modifiers import check_modifiers

try:
    from .saves import normalize_ability
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from saves import normalize_ability
    except ImportError:
        from dnd_sim.saves import normalize_ability


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

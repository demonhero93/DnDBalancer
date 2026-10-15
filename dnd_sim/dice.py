"""Tiradas de dados."""
import random
import re

_DICE_RE = re.compile(r"^\s*(\d+)d(\d+)\s*([+-]\s*\d+)?\s*$")


def roll_dice(expr: str, rng: random.Random, crit: bool = False) -> int:
    """Tira una expresión tipo '2d6+3'. En crítico se duplican los dados (no el bonus)."""
    m = _DICE_RE.match(expr)
    if not m:
        raise ValueError(f"Expresión de dados inválida: {expr!r}")
    n, faces = int(m.group(1)), int(m.group(2))
    bonus = int(m.group(3).replace(" ", "")) if m.group(3) else 0
    if crit:
        n *= 2
    return sum(rng.randint(1, faces) for _ in range(n)) + bonus


def d20(rng: random.Random) -> int:
    return rng.randint(1, 20)

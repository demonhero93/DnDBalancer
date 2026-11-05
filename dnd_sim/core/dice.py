"""Tiradas de dados."""
from __future__ import annotations

import random
import re
from dataclasses import dataclass
from enum import Enum

_DICE_RE = re.compile(r"^\s*(\d+)d(\d+)\s*([+-]\s*\d+)?\s*$")


class RollMode(Enum):
    NORMAL = "normal"
    ADVANTAGE = "advantage"
    DISADVANTAGE = "disadvantage"


@dataclass
class D20Result:
    value: int
    rolls: list[int]
    mode: RollMode


def roll_dice(expr: str, rng: random.Random, crit: bool = False,
              floor: int | None = None) -> int:
    """Tira una expresión tipo '2d6+3'. En crítico se duplican los dados (no el bonus).

    ``floor`` (opcional): piso por dado — Great Weapon Fighting cuenta
    los dados que salgan por debajo de ese valor como el propio piso
    (1 o 2 → 3). No cambia el número de llamadas al RNG.
    """
    m = _DICE_RE.match(expr)
    if not m:
        raise ValueError(f"Expresión de dados inválida: {expr!r}")
    n, faces = int(m.group(1)), int(m.group(2))
    bonus = int(m.group(3).replace(" ", "")) if m.group(3) else 0
    if crit:
        n *= 2
    valores = [rng.randint(1, faces) for _ in range(n)]
    if floor:
        valores = [v if v >= floor else floor for v in valores]
    return sum(valores) + bonus


_DICE_DOBLAR_RE = re.compile(r"(\d+)d(\d+)")


def doblar_dados(expr: str) -> str:
    """Duplica los dados de una expresión de daño («doubles its damage dice»).

    «1d8+2» -> «2d8+2»: se duplican todos los términos «NdM», no el bonus
    fijo. Si la expresión no contiene dados reconocibles, se devuelve tal
    cual.
    """
    expr = str(expr or "").strip()
    return _DICE_DOBLAR_RE.sub(
        lambda m: f"{int(m.group(1)) * 2}d{m.group(2)}", expr)


def roll_d20(rng: random.Random, mode: RollMode = RollMode.NORMAL) -> D20Result:
    """Tira un d20 aplicando ventaja/desventaja.

    NORMAL consume una sola llamada al RNG (compatibilidad con el código
    anterior). VENTAJA/DESVENTAJA tiran dos dados y conservan el mayor/menor.
    """
    if mode == RollMode.NORMAL:
        roll = rng.randint(1, 20)
        return D20Result(value=roll, rolls=[roll], mode=mode)
    first = rng.randint(1, 20)
    second = rng.randint(1, 20)
    if mode == RollMode.ADVANTAGE:
        value = max(first, second)
    else:
        value = min(first, second)
    return D20Result(value=value, rolls=[first, second], mode=mode)


def d20(rng: random.Random) -> int:
    """Compatibilidad: devuelve solo el valor."""
    return roll_d20(rng, RollMode.NORMAL).value

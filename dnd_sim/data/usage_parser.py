"""Convierte el campo ``usage`` de la API de dnd5eapi en ``ActionUsage``.

Formatos reales verificados en la SRD 2014 (334 monstruos):

- ``{"type": "per day", "times": 3}`` (a veces con ``"rest_types": []``)
- ``{"type": "recharge on roll", "dice": "1d6", "min_value": 5}``
- ``{"type": "recharge after rest", "rest_types": ["short", "long"]}``

Cualquier otro tipo se avisa con ``warnings.warn`` y la acción se omite.
"""
from __future__ import annotations

import warnings

from ..rules.usage import ActionUsage, UsageKind


class UnknownUsageError(ValueError):
    """El tipo de ``usage`` de la API no está soportado."""


def _warn(monster_name: str, action_name: str, raw_usage) -> None:
    warnings.warn(
        f"Tipo de 'usage' desconocido en la acción {action_name!r} de "
        f"{monster_name!r}: {raw_usage!r}. Se omite la acción. "
        f"# TODO: soportar más tipos de uso.",
        stacklevel=3,
    )


def parse_usage(raw_usage, monster_name: str = "", action_name: str = "") -> ActionUsage | None:
    """Devuelve el ``ActionUsage`` de la acción.

    - ``None`` si la acción es "at will" (no tiene uso limitado).
    - Lanza :class:`UnknownUsageError` (tras avisar) si el tipo no es
      conocido: en ese caso la acción se omite.
    """
    if not raw_usage:
        return None
    if not isinstance(raw_usage, dict):
        _warn(monster_name, action_name, raw_usage)
        raise UnknownUsageError(f"usage inválido: {raw_usage!r}")

    kind = str(raw_usage.get("type") or "").strip().lower()

    if kind in ("at will", "at-will", ""):
        return None

    if kind == "per day":
        times = raw_usage.get("times")
        if not isinstance(times, int) or isinstance(times, bool) or times < 1:
            _warn(monster_name, action_name, raw_usage)
            raise UnknownUsageError(f"'per day' sin 'times' válido: {raw_usage!r}")
        return ActionUsage(kind=UsageKind.PER_DAY, uses_max=times, uses_left=times)

    if kind == "recharge on roll":
        dice = raw_usage.get("dice")
        min_value = raw_usage.get("min_value")
        if not dice or min_value is None:
            _warn(monster_name, action_name, raw_usage)
            raise UnknownUsageError(f"'recharge on roll' incompleto: {raw_usage!r}")
        return ActionUsage(
            kind=UsageKind.RECHARGE_ROLL,
            recharge_dice=str(dice),
            recharge_min=int(min_value),
            charged=True,
        )

    if kind == "recharge after rest":
        # TODO: no se modelan los descansos (corto/largo): se trata como un
        # uso por combate, igual que "per day" (un combate = un día con
        # descansos hechos).
        return ActionUsage(kind=UsageKind.PER_DAY, uses_max=1, uses_left=1)

    _warn(monster_name, action_name, raw_usage)
    raise UnknownUsageError(f"tipo de usage desconocido: {kind!r}")


__all__ = ["UnknownUsageError", "parse_usage"]

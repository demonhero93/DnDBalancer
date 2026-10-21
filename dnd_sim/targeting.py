"""Selección de objetivos: hostiles vivos (fuente única de verdad).

Todo el simulador elige objetivos con :func:`valid_targets`:

- acciones (``dnd_sim.actions``),
- áreas (``dnd_sim.area``),
- condiciones (``dnd_sim.conditions``),
- acciones legendarias (``dnd_sim.legendary``).

Vive en un módulo **sin dependencias** para que todos esos módulos puedan
importarla sin ciclos de importación. ``dnd_sim.combatant`` la reexporta
como ``valid_targets`` (API pública histórica).

Reglas: nunca el propio actor, nunca los aliados, nunca los muertos.
"""
from __future__ import annotations

from typing import Any


def valid_targets(actor: Any, ctx: Any = None, combatants: Any = None,
                  enemies: Any = None) -> list:
    """Objetivos hostiles vivos de ``actor``.

    Parámetros
    ----------
    actor:
        Combatiente que ataca (el que busca objetivos hostiles).
    ctx:
        Contexto de combate: se usa para obtener la lista de combatientes
        (``ctx.combatants`` o ``ctx.enemies``) si no se pasan explícitamente.
    combatants:
        Lista explícita de combatientes (tiene prioridad sobre ``ctx``).
    enemies:
        Alias de ``combatants`` (compatibilidad).

    No consume RNG.
    """
    if combatants is None:
        if enemies is not None:
            combatants = enemies
        elif ctx is not None:
            combatants = getattr(ctx, "combatants", None)
            if combatants is None:
                combatants = getattr(ctx, "enemies", None)
        else:
            combatants = None
    if combatants is None:
        return []
    result = []
    for c in combatants:
        if c is actor:
            continue
        if not getattr(c, "alive", True):
            continue
        try:
            if actor.is_hostile_to(c):
                result.append(c)
        except Exception:
            pass
    return result


__all__ = ["valid_targets"]

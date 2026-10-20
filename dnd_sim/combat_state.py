"""Estado de combate de un combatiente (posiciones y cobertura).

Solo se modela lo que afecta a las tiradas: si un combatiente está "a
distancia" de su objetivo actual, su CA efectiva sube 2 (cobertura
simulada).

# TODO: cobertura real (obstrucciones, medio cuerpo), movimiento y
distancia entre varios combatientes.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CombatState:
    """Estado de combate de un combatiente.

    ``at_range``: el combatiente ataca a distancia (y queda "a distancia"
    respecto a quien le ataca). Todos empiezan cuerpo a cuerpo.
    """

    at_range: bool = False


__all__ = ["CombatState"]

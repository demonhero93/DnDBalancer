"""Pool de hechizos soportado para un PJ lanzador.

Un hechizo solo entra en el pool si el motor sabe ejecutarlo con las
acciones de hechizo ya existentes (ataque, salvación con daño, área,
condición, curación, estado o daño fijo) y si su tiempo de lanzamiento
es la acción Magia. El resto (ritual, utilidad, buffs sin efecto
modelable, reacciones de hechizo como Shield o Absorb Elements,
hechizos de acción bonus) queda FUERA: ver «Hechizos de PJ: pendientes
reales» en ``TODO.md``.
"""
from __future__ import annotations

from typing import Any

from ...model.actions import ActionType
from .casting import Spell


def hechizo_soportado(spell: Any) -> bool:
    """¿Puede el motor lanzar ``spell`` como acción de un PJ?

    ``False`` si es ``None``, si el parser lo marcó ``ignored`` (ritual,
    utilidad, 1 minuto...), si no tiene ``kind`` (sin efecto modelable)
    o si no se lanza con la acción Magia (acción bonus o reacción: la
    acción bonus bloquearía el resto del turno y la reacción no es una
    decisión de turno; ambas aplazadas en TODO.md).
    """
    if spell is None:
        return False
    if str(getattr(spell, "ignored", "") or ""):
        return False
    if not str(getattr(spell, "kind", "") or ""):
        return False
    tipo = getattr(spell, "action_type", ActionType.ACTION)
    return tipo is ActionType.ACTION


__all__ = ["hechizo_soportado"]

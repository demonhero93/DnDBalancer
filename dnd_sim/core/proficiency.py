"""Bonificación de competencia (proficiency bonus) según el nivel.

Primitiva de la **capa core**: la tabla es una función pura del nivel del
personaje, sin dependencias internas, así que ``model``, ``rules`` y
``data`` pueden importarla sin riesgo de ciclo de importación.

Regla 5e (PHB, «Using Ability Scores»): el bono de competencia de un PJ
depende **solo** de su nivel total; el de un monstruo, de su CR (y lo
trae la ficha en ``proficiency_bonus``).
"""
from __future__ import annotations

# Nivel mínimo y máximo admitidos para un PJ (la tabla no sale de 1..20).
MIN_LEVEL = 1
MAX_LEVEL = 20


def proficiency_bonus(level: int) -> int:
    """Bonificación de competencia de un PJ según su nivel.

    Tabla PHB 5e: +2 (niveles 1-4), +3 (5-8), +4 (9-12), +5 (13-16) y
    +6 (17-20). El nivel se recorta al rango 1..20.
    """
    try:
        nivel = int(level)
    except (TypeError, ValueError):
        nivel = MIN_LEVEL
    nivel = max(MIN_LEVEL, min(MAX_LEVEL, nivel))
    return 2 + (nivel - 1) // 4


__all__ = ["MIN_LEVEL", "MAX_LEVEL", "proficiency_bonus"]

"""Clasificador heurístico: ¿una acción con ``dc`` + daño es de área?

Decide si una acción de la API afecta a **varios** objetivos (área) o a
**uno** (objetivo único). La heurística es conservadora: se apoya solo en el
texto de la acción (``desc``), nunca en el nombre del monstruo.

Validado contra las 36 acciones con ``dc`` + daño de la SRD 2014 (barrido de
los 334 monstruos). Los casos reales se reparten así:

- **Área** (33): ``Each creature in that area must make...`` (alientos en cono
  o línea), ``Each creature within 10 ft. of the dragon must...`` (ala),
  ``Each creature of its choice in a 10-foot radius...`` (sol),
  ``Each living creature within 20 feet of the lich...`` (lich).
- **Objetivo único** (3): ``kraken``/Lightning Storm (``A target must make...``),
  ``gelatinous-cube``/Engulf (``the creature must make...``),
  ``aboleth``/Tentacle (``If the target is a creature, it must succeed...``).

# TODO: tabla de excepciones si algún monstruo se clasifica mal. Es frágil
por naturaleza: el texto de la API no describe la geometría de forma
estructurada.
"""
from __future__ import annotations

import re

# Palabras clave que delatan un área en el texto de la acción.
# "cube" y "line" (en solitario) quedan fuera a propósito: "cube" aparecería
# en el Engulf del gelatinous-cube (objetivo único) y "line" es demasiado
# genérica ("line of sight"). No se amplían sin un fixture que lo justifique.
AREA_KEYWORDS: tuple[str, ...] = (
    "in that area",
    "in that line",
    "cone",
    "radius",
    "sphere",
)

# "Each creature", "Each living creature", "Each of ... creature".
AREA_PATTERN = re.compile(r"\beach\s+(?:\w+\s+){0,2}creature\b", re.IGNORECASE)


def is_area_action(action: dict) -> bool:
    """¿La acción del payload de la API es de área?"""
    if not isinstance(action, dict):
        return False
    text = str(action.get("desc") or "").lower()
    if not text:
        return False
    if AREA_PATTERN.search(text):
        return True
    return any(keyword in text for keyword in AREA_KEYWORDS)


__all__ = ["AREA_KEYWORDS", "AREA_PATTERN", "is_area_action"]

"""Constantes puras de clase (PHB 2024).

Primitivas de la **capa core**: tablas que dependen solo del nivel, sin
dependencias internas, para que ``model``, ``rules`` y ``data`` puedan
importarlas sin riesgo de ciclo de importación. Hoy solo el bárbaro;
el resto de clases se irá añadiendo aquí.

Los nombres de ``BARBARIAN_FEATURES`` son los de la API 5e (SRD) para
poder contrastarlos con ``tests/fixtures/barbarian_levels.json``.
"""
from __future__ import annotations

MIN_LEVEL = 1
MAX_LEVEL = 20


def _clamp(level: int) -> int:
    try:
        value = int(level)
    except (TypeError, ValueError):
        value = MIN_LEVEL
    return max(MIN_LEVEL, min(MAX_LEVEL, value))


def rage_uses(level: int) -> int:
    """Usos de Furia (Rage) por descanso según el nivel (tabla PHB 2024)."""
    lvl = _clamp(level)
    if lvl <= 2:
        return 2
    if lvl <= 5:
        return 3
    if lvl <= 11:
        return 4
    if lvl <= 16:
        return 5
    return 6


def rage_damage(level: int) -> int:
    """Daño extra de Furia en ataques con FUE (tabla PHB 2024)."""
    lvl = _clamp(level)
    if lvl <= 8:
        return 2
    if lvl <= 15:
        return 3
    return 4


def extra_attacks_for(level: int) -> int:
    """Golpes de la acción Atacar (1 en niveles 1-4, 2 desde el 5)."""
    return 2 if _clamp(level) >= 5 else 1


#: Nivel en el que el bárbaro gana cada feature (PHB 2024, vía API).
#: Solo documentación/paridad: la simulación consulta el ``level`` directo.
BARBARIAN_FEATURES: dict[int, tuple[str, ...]] = {
    1: ("Rage", "Unarmored Defense", "Weapon Mastery"),
    2: ("Danger Sense", "Reckless Attack"),
    3: ("Barbarian Subclass", "Primal Knowledge"),
    4: ("Ability Score Improvement",),
    5: ("Extra Attack", "Fast Movement"),
    6: ("Barbarian Subclass",),
    7: ("Feral Instinct", "Instinctive Pounce"),
    8: ("Ability Score Improvement",),
    9: ("Brutal Strike",),
    10: ("Barbarian Subclass",),
    11: ("Relentless Rage",),
    12: ("Ability Score Improvement",),
    13: ("Improved Brutal Strike",),
    14: ("Barbarian Subclass",),
    15: ("Persistent Rage",),
    16: ("Ability Score Improvement",),
    17: ("Improved Brutal Strike",),
    18: ("Indomitable Might",),
    19: ("Epic Boon",),
    20: ("Primal Champion",),
}

#: Habilidades de la clase (PHB 2024), en inglés normalizado.
BARBARIAN_SKILLS: tuple[str, ...] = (
    "athletics",
    "intimidation",
    "nature",
    "perception",
    "survival",
)

#: Habilidades que Primal Knowledge (nivel 3) permite tirar como FUE
#: mientras dura Furia (PHB 2024).
BARBARIAN_PRIMAL_SKILLS: tuple[str, ...] = (
    "acrobatics",
    "intimidation",
    "perception",
    "stealth",
    "survival",
)

__all__ = [
    "BARBARIAN_FEATURES",
    "BARBARIAN_PRIMAL_SKILLS",
    "BARBARIAN_SKILLS",
    "MAX_LEVEL",
    "MIN_LEVEL",
    "extra_attacks_for",
    "rage_damage",
    "rage_uses",
]

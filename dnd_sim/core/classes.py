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


def action_surge_uses(level: int) -> int:
    """Usos de Oleada de Acción (Action Surge) por descanso según el nivel."""
    return 2 if _clamp(level) >= 17 else 1


def second_wind_uses(level: int) -> int:
    """Usos de Tomar Aliento (Second Wind) por descanso según el nivel."""
    lvl = _clamp(level)
    if lvl <= 3:
        return 2
    if lvl <= 9:
        return 3
    return 4


def indomitable_uses(level: int) -> int:
    """Usos de Indomitable por descanso (0 por debajo del nivel 9)."""
    lvl = _clamp(level)
    if lvl < 9:
        return 0
    if lvl <= 12:
        return 1
    if lvl <= 16:
        return 2
    return 3


def weapon_mastery_count(level: int) -> int:
    """Armas con Maestría elegibles (3/4/5/6 en los niveles 1/4/10/16)."""
    lvl = _clamp(level)
    if lvl >= 16:
        return 6
    if lvl >= 10:
        return 5
    if lvl >= 4:
        return 4
    return 3


def arcane_shot_options_known(level: int) -> int:
    """Opciones de Arcane Shot conocidas (0/2/3/4/5/6 en <3/3/7/10/15/18)."""
    lvl = _clamp(level)
    if lvl >= 18:
        return 6
    if lvl >= 15:
        return 5
    if lvl >= 10:
        return 4
    if lvl >= 7:
        return 3
    if lvl >= 3:
        return 2
    return 0


def arcane_shot_uses(level: int) -> int:
    """Usos de Arcane Shot por descanso (0 <3, 2 en 3-14, 3 en 15+)."""
    lvl = _clamp(level)
    if lvl < 3:
        return 0
    return 3 if lvl >= 15 else 2


def superiority_dice_count(level: int) -> int:
    """Dados de superioridad de Combat Superiority (0/4/5/6 en <3/3-6/7-14/15+)."""
    lvl = _clamp(level)
    if lvl < 3:
        return 0
    if lvl < 7:
        return 4
    if lvl < 15:
        return 5
    return 6


def superiority_die_sides(level: int) -> int:
    """Caras del dado de superioridad (d8/d10/d12 en <10/10-17/18+)."""
    lvl = _clamp(level)
    if lvl >= 18:
        return 12
    if lvl >= 10:
        return 10
    return 8


def maneuvers_known_count(level: int) -> int:
    """Maniobras conocidas (0/3/5/7/9 en <3/3-6/7-9/10-14/15+)."""
    lvl = _clamp(level)
    if lvl < 3:
        return 0
    if lvl < 7:
        return 3
    if lvl < 10:
        return 5
    if lvl < 15:
        return 7
    return 9


def cavalier_mark_uses(str_mod: int) -> int:
    """Usos de Unwavering Mark por descanso (mínimo 1, mod FUE)."""
    return max(1, str_mod)


def warding_maneuver_uses(con_mod: int) -> int:
    """Usos de Warding Maneuver por descanso (mínimo 1, mod CON)."""
    return max(1, con_mod)


def cavalier_mark_extra_damage(level: int) -> int:
    """Daño extra del ataque especial de Unwavering Mark (nivel // 2)."""
    return _clamp(level) // 2


def fighter_extra_attacks_for(level: int) -> int:
    """Golpes de la acción Atacar del Fighter (1/2/3/4 en 1/5/11/20).

    Aparte de :func:`extra_attacks_for` (bárbaro): el bárbaro no pasa
    nunca de 2 y esa tabla no debe cambiar.
    """
    lvl = _clamp(level)
    if lvl >= 20:
        return 4
    if lvl >= 11:
        return 3
    if lvl >= 5:
        return 2
    return 1


#: Nivel en el que el Fighter gana cada feature (PHB 2024).
#: Solo documentación/paridad: la simulación consulta el ``level`` directo.
FIGHTER_FEATURES: dict[int, tuple[str, ...]] = {
    1: ("Fighting Style", "Second Wind", "Weapon Mastery"),
    2: ("Action Surge", "Tactical Mind"),
    3: ("Fighter Subclass",),
    4: ("Ability Score Improvement",),
    5: ("Extra Attack", "Tactical Shift"),
    6: ("Fighter Subclass",),
    7: ("Fighter Subclass",),
    8: ("Ability Score Improvement",),
    9: ("Indomitable", "Tactical Master"),
    10: ("Fighter Subclass",),
    11: ("Two Extra Attacks",),
    12: ("Ability Score Improvement",),
    13: ("Studied Attacks", "Indomitable"),
    14: ("Fighter Subclass",),
    15: ("Fighter Subclass",),
    16: ("Ability Score Improvement",),
    17: ("Action Surge", "Indomitable"),
    18: ("Fighter Subclass",),
    19: ("Epic Boon",),
    20: ("Three Extra Attacks",),
}


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

#: Habilidades de la clase bárbaro (PHB 2024), en inglés normalizado.
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

#: Habilidades de la clase Fighter/Guerrero (PHB 2024): elige 2.
#: Normalizadas con el formato guion (``core.skills``).
FIGHTER_SKILLS: tuple[str, ...] = (
    "acrobatics",
    "animal-handling",
    "athletics",
    "history",
    "insight",
    "intimidation",
    "perception",
    "persuasion",
    "survival",
)

#: Estilos de combate del Fighter con efecto en la simulación (PHB 2024).
#: Protection e Interception usan la reacción del guardián; el resto
#: (Blind Fighting, Unarmed Fighting, Two-Weapon Fighting) queda como
#: dato sin efecto (ver TODO.md).
FIGHTER_STYLES: tuple[str, ...] = (
    "Archery",
    "Defense",
    "Dueling",
    "Great Weapon Fighting",
    "Interception",
    "Protection",
    "Thrown Weapon Fighting",
)

#: Pool de maniobras de Battle Master implementadas (PHB 2024): 16
#: (11 de la sesión 1 + Parry, Riposte y Commander's Strike de la
#: sesión 2 + Rally de B1 + Ambush de B3). Cambiar el pool cambia el
#: ``sample`` de PJ con semilla fija (tests reseedados, ver PASOS).
BATTLE_MASTER_MANEUVERS: tuple[str, ...] = (
    "Ambush",
    "Commander's Strike",
    "Disarming Attack",
    "Distracting Strike",
    "Feinting Attack",
    "Goading Attack",
    "Lunging Attack",
    "Maneuvering Attack",
    "Menacing Attack",
    "Parry",
    "Precision Attack",
    "Pushing Attack",
    "Rally",
    "Riposte",
    "Sweeping Attack",
    "Trip Attack",
)

#: Habilidades candidatas a Bonus Proficiency (Cavalier, XGE): Trato con
#: animales, Historia, Perspicacia, Interpretación y Persuasión. Todas
#: existen en :data:`dnd_sim.core.skills.SKILL_ABILITIES` (claves en
#: inglés); el idioma del rasgo es dato sin efecto (sin modelo).
CAVALIER_BONUS_SKILLS: tuple[str, ...] = (
    "animal-handling",
    "history",
    "insight",
    "performance",
    "persuasion",
)

#: Probabilidad de simular un movimiento de carga de al menos 10 pies
#: hacia la criatura en Ferocious Charger (Cavalier). Se evalúa una vez
#: por turno en el primer impacto cuerpo a cuerpo (patrón
#: ``RECKLESS_USE_PROBABILITY``): con 0 la carga nunca ocurre y no se
#: consume RNG. CLI ``--charge-p`` en main.py.
CHARGE_MOVE_PROBABILITY: float = 0.5

__all__ = [
    "BARBARIAN_FEATURES",
    "BARBARIAN_PRIMAL_SKILLS",
    "BARBARIAN_SKILLS",
    "BATTLE_MASTER_MANEUVERS",
    "CAVALIER_BONUS_SKILLS",
    "CHARGE_MOVE_PROBABILITY",
    "FIGHTER_FEATURES",
    "FIGHTER_SKILLS",
    "FIGHTER_STYLES",
    "MAX_LEVEL",
    "MIN_LEVEL",
    "action_surge_uses",
    "arcane_shot_options_known",
    "arcane_shot_uses",
    "cavalier_mark_extra_damage",
    "cavalier_mark_uses",
    "extra_attacks_for",
    "fighter_extra_attacks_for",
    "indomitable_uses",
    "maneuvers_known_count",
    "rage_damage",
    "rage_uses",
    "second_wind_uses",
    "superiority_die_sides",
    "superiority_dice_count",
    "warding_maneuver_uses",
    "weapon_mastery_count",
]

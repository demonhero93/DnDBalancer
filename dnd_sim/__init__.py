"""Simulador de combate D&D 5e."""
try:
    from .abilities import Abilities, ability_mod
    from .attack import Attack
    from .combatant import Combatant
    from .damage import DamageType, apply_damage_modifiers, parse_damage_type
    from .combat import CombatResult, run_combat
    from .stats import simulate, print_report
    from .data.loader import load_monster
except ImportError:
    from abilities import Abilities, ability_mod
    from attack import Attack
    from combatant import Combatant
    from damage import DamageType, apply_damage_modifiers, parse_damage_type
    from combat import CombatResult, run_combat
    from stats import simulate, print_report
    try:
        from data.loader import load_monster
    except ImportError:
        from loader import load_monster

__all__ = [
    "Abilities", "ability_mod", "Attack", "Combatant",
    "DamageType", "apply_damage_modifiers", "parse_damage_type",
    "CombatResult", "run_combat", "simulate", "print_report",
    "load_monster",
]

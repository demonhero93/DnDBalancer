"""Simulador de combate D&D 5e."""
try:
    from .abilities import Abilities, ability_mod
    from .actions import (
        ActionType, AttackAction, CombatAction, CombatContext, MultiattackAction,
        SaveAction, TurnResources, WeaponAttackAction, AttackEntry,
    )
    from .attack import Attack
    from .combatant import (
        Combatant, CombatantType, Monster, PlayerCharacter, valid_targets,
    )
    from .damage import DamageType, apply_damage_modifiers, inflict_damage, parse_damage_type
    from .combat import CombatResult, resolve_roll_mode, run_combat, valid_targets
    from .saves import (
        SaveDamage, SaveResult, normalize_ability, resolve_save_damage, saving_throw,
    )
    from .dice import D20Result, RollMode, roll_d20, roll_dice, d20
    from .randomness import pick
    from .stats import simulate, print_report
    from .tactics import first_target_policy, random_policy
    from .data.loader import load_monster
except ImportError:
    from abilities import Abilities, ability_mod
    from actions import (
        ActionType, AttackAction, CombatAction, CombatContext, MultiattackAction,
        SaveAction, TurnResources, WeaponAttackAction, AttackEntry,
    )
    from attack import Attack
    from combatant import (
        Combatant, CombatantType, Monster, PlayerCharacter, valid_targets,
    )
    from damage import DamageType, apply_damage_modifiers, inflict_damage, parse_damage_type
    from combat import CombatResult, resolve_roll_mode, run_combat, valid_targets
    try:
        from saves import SaveDamage, SaveResult, normalize_ability, resolve_save_damage, saving_throw
    except Exception:
        pass
    from dice import D20Result, RollMode, roll_d20, roll_dice, d20
    from randomness import pick
    from stats import simulate, print_report
    from tactics import first_target_policy, random_policy
    try:
        from data.loader import load_monster
    except ImportError:
        from loader import load_monster

__all__ = [
    "Abilities", "ability_mod", "ActionType", "Attack", "AttackAction", "AttackEntry",
    "CombatAction", "CombatContext", "Combatant", "CombatResult",
    "D20Result", "DamageType", "MultiattackAction", "RollMode", "SaveAction",
    "SaveDamage", "SaveResult", "TurnResources", "WeaponAttackAction",
    "apply_damage_modifiers", "d20", "first_target_policy", "inflict_damage",
    "normalize_ability", "parse_damage_type", "pick", "print_report",
    "random_policy", "resolve_roll_mode", "resolve_save_damage", "roll_d20",
    "roll_dice", "run_combat", "saving_throw", "simulate", "load_monster",
]

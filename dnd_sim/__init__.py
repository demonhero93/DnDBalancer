"""Simulador de combate D&D 5e."""
from .core.abilities import Abilities, ability_mod
from .model.actions import (
    ActionType, AttackAction, CombatAction, CombatContext, MultiattackAction, SaveAction, TurnResources, WeaponAttackAction, AttackEntry
)
from .rules.area import AreaSaveAction, AreaTargeting, select_area_targets
from .model.attack import Attack
from .rules.attach import Attach, AttachOnHitEffect, desenganchar, intentar_desenganche
from .rules.checks import CheckResult, ability_check, ability_check_bonus
from .core.combat_state import CombatState
from .model.combatant import (
    Combatant, CombatantType, Monster, PlayerCharacter, valid_targets
)
from .rules.conditions import (
    Condition, ConditionAction, ConditionEffect, ConditionInstance, ConditionTracker, EXCLUDED_CONDITIONS, EscapeCheck, RepeatSave, apply_condition, attempt_escapes, end_turn
)
from .rules.damage import (
    DamageType, apply_damage_modifiers, inflict_damage, parse_damage_type
)
from .rules.legendary import (
    DEFAULT_LEGENDARY_POINTS, LegendaryAction, LegendaryState, legendary_phase, legendary_resistance
)
from .engine.combat import CombatResult, resolve_roll_mode, run_combat, valid_targets
from .rules.roll_modifiers import (
    AttackModifiers, AttackRange, CheckModifiers, RANGED_COVER_AC_BONUS, SaveModifiers, attack_modifiers, check_modifiers, effective_ac, resolve_attack_range, save_modifiers
)
from .rules.saves import (
    SaveDamage, SaveDamageOutcome, SaveResult, apply_save_damage, normalize_ability, resolve_save_damage, saving_throw
)
from .rules.spells import (
    HealAction, HealEffect, Spell, SpellAction, SpellAttackAction, SpellFixedDamageAction, SpellStateAction, Spellcasting, StateEffect, spell_action
)
from .rules.traits import (
    BloodFrenzy, DamageTransfer, HeatedBody, MartialAdvantage, PackTactics, Parry, Regeneration, Relentless, SuperiorInvisibility, Trait, TurnResistance, UndeadFortitude
)
from .core.dice import D20Result, RollMode, roll_d20, roll_dice, d20
from .core.randomness import pick, sample
from .engine.stats import simulate, print_report
from .engine.tactics import first_target_policy, random_policy
from .rules.usage import ActionUsage, UsageKind, begin_turn
from .data.loader import load_monster
from .core.targeting import valid_targets

__all__ = [
    "Abilities", "ability_mod", "ActionType", "ActionUsage", "AreaSaveAction",
    "AreaTargeting", "Attack", "AttackAction", "AttackEntry", "AttackModifiers",
    "AttackRange", "Attach", "AttachOnHitEffect", "BloodFrenzy", "CheckModifiers",
    "CheckResult", "CombatAction",
    "CombatContext", "Combatant", "CombatResult", "CombatState", "Condition",
    "ConditionAction", "ConditionEffect", "ConditionInstance",
    "ConditionTracker", "D20Result", "DamageType", "DamageTransfer",
    "EXCLUDED_CONDITIONS", "HeatedBody",
    "EscapeCheck", "MultiattackAction", "RANGED_COVER_AC_BONUS", "RepeatSave",
    "MartialAdvantage", "PackTactics", "Parry",
    "RollMode", "SaveAction", "SaveDamage", "SaveDamageOutcome", "SaveModifiers",
    "SaveResult", "Trait", "TurnResistance", "TurnResources", "UsageKind",
    "WeaponAttackAction", "Relentless", "SuperiorInvisibility",
    "UndeadFortitude",
    "ability_check", "ability_check_bonus", "apply_condition",
    "apply_damage_modifiers", "apply_save_damage", "attack_modifiers",
    "attempt_escapes", "begin_turn", "check_modifiers", "d20", "desenganchar",
    "effective_ac",
    "end_turn", "first_target_policy", "inflict_damage",
    "intentar_desenganche", "normalize_ability",
    "parse_damage_type", "pick", "print_report", "random_policy",
    "resolve_attack_range", "resolve_roll_mode", "resolve_save_damage",
    "roll_d20", "roll_dice", "run_combat", "sample", "save_modifiers",
    "saving_throw", "select_area_targets", "simulate", "load_monster",
    "HealAction", "HealEffect", "Spell", "SpellAction", "SpellAttackAction",
    "SpellFixedDamageAction", "SpellStateAction", "Spellcasting",
    "StateEffect", "spell_action", "Regeneration",
    "DEFAULT_LEGENDARY_POINTS", "LegendaryAction", "LegendaryState",
    "legendary_phase", "legendary_resistance",
]

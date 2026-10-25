"""Simulador de combate D&D 5e.

Fachada pública: reexporta todo lo que un usuario necesita, ordenado por
capa (``core`` -> ``model`` -> ``rules`` -> ``engine``/``data``). Dentro
del paquete cada módulo solo importa de su capa o de una inferior; las
reglas completas están en ``ARCHITECTURE.md``.
"""

# core: dados, habilidades, estado de combate y apuntado
from .core.abilities import Abilities, ability_mod
from .core.combat_state import CombatState
from .core.dice import D20Result, RollMode, d20, roll_d20, roll_dice
from .core.randomness import pick, sample
from .core.targeting import valid_targets

# model: combatientes, ataques y acciones
from .model.actions import (
    ActionType, AttackAction, AttackEntry, CombatAction, CombatContext,
    MultiattackAction, SaveAction, TurnResources, WeaponAttackAction,
)
from .model.attack import Attack
from .model.combatant import (
    Combatant, CombatantType, Monster, PlayerCharacter,
)

# rules: reglas 5e (condiciones, daño, salvaciones, hechizos, rasgos)
from .rules.area import AreaSaveAction, AreaTargeting, select_area_targets
from .rules.attach import (
    Attach, AttachOnHitEffect, desenganchar, intentar_desenganche,
)
from .rules.checks import CheckResult, ability_check, ability_check_bonus
from .rules.conditions import (
    Condition, ConditionAction, ConditionEffect, ConditionInstance,
    ConditionTracker, EXCLUDED_CONDITIONS, EscapeCheck, RepeatSave,
    apply_condition, attempt_escapes, end_turn,
)
from .rules.damage import (
    DamageType, apply_damage_modifiers, inflict_damage, parse_damage_type,
)
from .rules.legendary import (
    DEFAULT_LEGENDARY_POINTS, LegendaryAction, LegendaryState,
    legendary_phase, legendary_resistance,
)
from .rules.roll_modifiers import (
    AttackModifiers, AttackRange, CheckModifiers, RANGED_COVER_AC_BONUS,
    SaveModifiers, attack_modifiers, check_modifiers, effective_ac,
    resolve_attack_range, save_modifiers,
)
from .rules.saves import (
    SaveDamage, SaveDamageOutcome, SaveResult, apply_save_damage,
    normalize_ability, resolve_save_damage, saving_throw,
)
from .rules.spells import (
    HealAction, HealEffect, Spell, SpellAction, SpellAttackAction,
    SpellFixedDamageAction, SpellStateAction, Spellcasting, StateEffect,
    spell_action,
)
from .rules.traits import (
    BloodFrenzy, DamageTransfer, HeatedBody, MartialAdvantage, PackTactics,
    Parry, Regeneration, Relentless, SuperiorInvisibility, Trait,
    TurnResistance, UndeadFortitude,
)
from .rules.usage import ActionUsage, UsageKind, begin_turn

# engine: motor de combate (ataques, rondas, informes, políticas)
from .engine.combat import CombatResult, resolve_roll_mode, run_combat
from .engine.stats import print_report, simulate
from .engine.tactics import first_target_policy, random_policy

# data: carga de fichas de la API
from .data.loader import load_monster

__all__ = [
    "Abilities", "ActionType", "ActionUsage", "AreaSaveAction",
    "AreaTargeting", "Attach", "AttachOnHitEffect", "Attack", "AttackAction",
    "AttackEntry", "AttackModifiers", "AttackRange", "BloodFrenzy",
    "CheckModifiers", "CheckResult", "CombatAction", "CombatContext",
    "CombatResult", "CombatState", "Combatant", "CombatantType", "Condition",
    "ConditionAction", "ConditionEffect", "ConditionInstance",
    "ConditionTracker", "D20Result", "DEFAULT_LEGENDARY_POINTS",
    "DamageTransfer", "DamageType", "EXCLUDED_CONDITIONS", "EscapeCheck",
    "HealAction", "HealEffect", "HeatedBody", "LegendaryAction",
    "LegendaryState", "MartialAdvantage", "Monster", "MultiattackAction",
    "PackTactics", "Parry", "PlayerCharacter", "RANGED_COVER_AC_BONUS",
    "Regeneration", "Relentless", "RepeatSave", "RollMode", "SaveAction",
    "SaveDamage", "SaveDamageOutcome", "SaveModifiers", "SaveResult", "Spell",
    "SpellAction", "SpellAttackAction", "SpellFixedDamageAction",
    "SpellStateAction", "Spellcasting", "StateEffect", "SuperiorInvisibility",
    "Trait", "TurnResistance", "TurnResources", "UndeadFortitude",
    "UsageKind", "WeaponAttackAction", "ability_check", "ability_check_bonus",
    "ability_mod", "apply_condition", "apply_damage_modifiers",
    "apply_save_damage", "attack_modifiers", "attempt_escapes", "begin_turn",
    "check_modifiers", "d20", "desenganchar", "effective_ac", "end_turn",
    "first_target_policy", "inflict_damage", "intentar_desenganche",
    "legendary_phase", "legendary_resistance", "load_monster",
    "normalize_ability", "parse_damage_type", "pick", "print_report",
    "random_policy", "resolve_attack_range", "resolve_roll_mode",
    "resolve_save_damage", "roll_d20", "roll_dice", "run_combat", "sample",
    "save_modifiers", "saving_throw", "select_area_targets", "simulate",
    "spell_action", "valid_targets",
]

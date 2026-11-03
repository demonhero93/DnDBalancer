"""Simulador de combate D&D 5e.

Fachada pública: reexporta todo lo que un usuario necesita, ordenado por
capa (``core`` -> ``model`` -> ``rules`` -> ``engine``/``data``). Dentro
del paquete cada módulo solo importa de su capa o de una inferior; las
reglas completas están en ``ARCHITECTURE.md``.
"""

# core: dados, habilidades, estado de combate y apuntado
from .core.abilities import Abilities, ability_mod
from .core.classes import rage_damage, rage_uses
from .core.proficiency import proficiency_bonus
from .core.backgrounds import Background
from .core.races import Race
from .core.skills import normalize_skill, skill_ability
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
from .rules.classes.barbarian.subclasses.ancestral_guardian import (
    AncestralGuardianFeatures, apply_ancestral_guardian,
)
from .rules.classes.barbarian import (
    BarbarianFeatures, ExtendRageAction, RageAction, apply_barbarian,
)
from .rules.classes.barbarian.subclasses.battlerager import (
    BattleragerFeatures, SpikedArmorAction, apply_battlerager,
)
from .rules.classes.barbarian.subclasses.beast import (
    BeastFeatures, FormOfTheBeast, NaturalWeapon, apply_beast,
)
from .rules.classes.barbarian.subclasses.berserker import (
    BerserkerFeatures, IntimidatingPresenceAction, apply_berserker,
)
from .rules.classes.barbarian.subclasses.giant import (
    GiantFeatures, MightyImpelAction, apply_giant,
)
from .rules.classes.barbarian.subclasses.storm_herald import (
    StormAuraAction, StormHeraldFeatures, apply_storm_herald,
)
from .rules.classes.base import apply_class
from .rules.checks import (CheckResult, ability_check, ability_check_bonus,
                           skill_bonus, skill_check)
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
from .data.background_parser import load_background, parse_background
from .data.race_parser import load_race, parse_race

__all__ = [
    "Abilities", "ActionType", "ActionUsage", "AncestralGuardianFeatures",
    "AreaSaveAction",
    "AreaTargeting", "Attach", "AttachOnHitEffect", "Attack", "AttackAction",
    "AttackEntry", "AttackModifiers", "AttackRange", "Background",
    "BarbarianFeatures", "BattleragerFeatures", "BeastFeatures",
    "BerserkerFeatures",
    "BloodFrenzy",
    "CheckModifiers", "CheckResult", "CombatAction", "CombatContext",
    "CombatResult", "CombatState", "Combatant", "CombatantType", "Condition",
    "ConditionAction", "ConditionEffect", "ConditionInstance",
    "ConditionTracker", "D20Result", "DEFAULT_LEGENDARY_POINTS",
    "DamageTransfer", "DamageType", "EXCLUDED_CONDITIONS", "EscapeCheck",
    "ExtendRageAction", "FormOfTheBeast", "GiantFeatures", "HealAction",
    "HealEffect",
    "HeatedBody",
    "IntimidatingPresenceAction",
    "LegendaryAction",
    "LegendaryState", "MartialAdvantage", "MightyImpelAction", "Monster",
    "MultiattackAction",
    "NaturalWeapon", "PackTactics", "Parry", "PlayerCharacter",
    "RANGED_COVER_AC_BONUS",
    "Race", "RageAction", "Regeneration", "Relentless", "RepeatSave",
    "RollMode", "SaveAction",
    "SaveDamage", "SaveDamageOutcome", "SaveModifiers", "SaveResult", "Spell",
    "SpellAction", "SpellAttackAction", "SpellFixedDamageAction",
    "SpellStateAction", "Spellcasting", "SpikedArmorAction", "StateEffect",
    "StormAuraAction", "StormHeraldFeatures",
    "SuperiorInvisibility",
    "Trait", "TurnResistance", "TurnResources", "UndeadFortitude",
    "UsageKind", "WeaponAttackAction", "ability_check", "ability_check_bonus",
    "ability_mod", "apply_ancestral_guardian", "apply_barbarian",
    "apply_battlerager", "apply_beast", "apply_berserker", "apply_class",
    "apply_condition", "apply_giant", "apply_storm_herald",
    "apply_damage_modifiers", "apply_save_damage", "attack_modifiers",
    "attempt_escapes", "begin_turn",
    "check_modifiers", "d20", "desenganchar", "effective_ac", "end_turn",
    "first_target_policy", "inflict_damage", "intentar_desenganche",
    "legendary_phase", "legendary_resistance", "load_background",
    "load_monster", "load_race",
    "normalize_ability", "normalize_skill", "parse_background",
    "parse_damage_type", "parse_race", "pick",
    "print_report",
    "proficiency_bonus", "rage_damage", "rage_uses", "random_policy",
    "resolve_attack_range", "resolve_roll_mode",
    "resolve_save_damage", "roll_d20", "roll_dice", "run_combat", "sample",
    "save_modifiers", "saving_throw", "select_area_targets", "skill_ability",
    "skill_bonus", "skill_check", "simulate",
    "spell_action", "valid_targets",
]

"""Clases jugables (PHB 2024): registro genérico + clases con fachada.

Reexporta todo lo de siempre (los imports de fuera no cambian) más el
registro de :mod:`~dnd_sim.rules.classes.base`.
"""
from __future__ import annotations

from .base import (
    CLASSES,
    ClassDef,
    SubclassDef,
    apply_class,
    normalize_class_name,
    register_class,
)
from .barbarian import BarbarianFeatures, ExtendRageAction, RageAction, apply_barbarian
from .barbarian.subclasses import (
    ANCESTRAL_FEATURES,
    BATTLERAGER_FEATURES,
    AncestralGuardianFeatures,
    BattleragerFeatures,
    BeastFeatures,
    FormOfTheBeast,
    NaturalWeapon,
    SpikedArmorAction,
    apply_ancestral_guardian,
    apply_battlerager,
    apply_beast,
)
from .fighter import FighterFeatures, SecondWindAction, apply_fighter

__all__ = ["ANCESTRAL_FEATURES", "AncestralGuardianFeatures",
           "BATTLERAGER_FEATURES", "CLASSES", "ClassDef",
           "BarbarianFeatures", "BeastFeatures", "BattleragerFeatures",
           "FighterFeatures",
           "SubclassDef", "ExtendRageAction", "FormOfTheBeast",
           "NaturalWeapon", "RageAction", "SecondWindAction",
           "SpikedArmorAction",
           "apply_ancestral_guardian", "apply_barbarian", "apply_battlerager",
           "apply_beast", "apply_class", "apply_fighter", "normalize_class_name",
           "register_class"]

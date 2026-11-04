"""Paquete de la clase bárbaro: código base + registro de sus subclases.

:mod:`features` concentra el código base (Furia, Ataque Extra...). Este
``__init__`` reexporta la API de siempre (``from
dnd_sim.rules.classes.barbarian import apply_barbarian`` sigue igual) y
declara la clase en el registro genérico de
:mod:`dnd_sim.rules.classes.base`.
"""
from __future__ import annotations

from ..base import ClassDef, SubclassDef, register_class
from .features import BarbarianFeatures, ExtendRageAction, RageAction, apply_barbarian
from .subclasses import (
    ANCESTRAL_FEATURES,
    BATTLERAGER_FEATURES,
    BERSERKER_FEATURES,
    ENTORNOS,
    GIANT_FEATURES,
    STORM_HERALD_FEATURES,
    WILD_HEART_FEATURES,
    WILD_MAGIC_FEATURES,
    WILD_SURGE_TABLE,
    AncestralGuardianFeatures,
    BattleragerFeatures,
    BeastFeatures,
    BerserkerFeatures,
    FormOfTheBeast,
    GiantFeatures,
    IntimidatingPresenceAction,
    MightyImpelAction,
    NaturalWeapon,
    SpikedArmorAction,
    StormAuraAction,
    StormHeraldFeatures,
    WildHeartFeatures,
    WildMagicFeatures,
    WildSurgeAction,
    apply_ancestral_guardian,
    apply_battlerager,
    apply_beast,
    apply_berserker,
    apply_giant,
    apply_storm_herald,
    apply_wild_heart,
    apply_wild_magic,
)

#: Registro de la clase bárbaro con sus subclases (claves normalizadas).
BARBARIAN_CLASS = register_class(ClassDef(
    name="barbarian",
    apply=apply_barbarian,
    subclasses={
        "ancestral_guardian": SubclassDef(
            name="Ancestral Guardian", class_name="barbarian",
            min_level=3, apply=apply_ancestral_guardian,
        ),
        "battlerager": SubclassDef(
            name="Battlerager", class_name="barbarian",
            min_level=3, apply=apply_battlerager,
        ),
        "beast": SubclassDef(
            name="Path of the Beast", class_name="barbarian",
            min_level=3, apply=apply_beast,
        ),
        "berserker": SubclassDef(
            name="Path of the Berserker", class_name="barbarian",
            min_level=3, apply=apply_berserker,
        ),
        "giant": SubclassDef(
            name="Path of the Giant", class_name="barbarian",
            min_level=3, apply=apply_giant,
        ),
        # apply_class solo pasa `level`: el entorno va en el closure.
        "storm_herald_desert": SubclassDef(
            name="Path of the Storm Herald (Desert)", class_name="barbarian",
            min_level=3,
            apply=lambda pj, level=None: apply_storm_herald(
                pj, level=level, entorno="desert"),
        ),
        "storm_herald_sea": SubclassDef(
            name="Path of the Storm Herald (Sea)", class_name="barbarian",
            min_level=3,
            apply=lambda pj, level=None: apply_storm_herald(
                pj, level=level, entorno="sea"),
        ),
        "storm_herald_tundra": SubclassDef(
            name="Path of the Storm Herald (Tundra)", class_name="barbarian",
            min_level=3,
            apply=lambda pj, level=None: apply_storm_herald(
                pj, level=level, entorno="tundra"),
        ),
        "wild_heart": SubclassDef(
            name="Path of the Wild Heart", class_name="barbarian",
            min_level=3, apply=apply_wild_heart,
        ),
        "wild_magic": SubclassDef(
            name="Path of Wild Magic", class_name="barbarian",
            min_level=3, apply=apply_wild_magic,
        ),
    },
))

__all__ = ["BARBARIAN_CLASS", "BarbarianFeatures", "ExtendRageAction",
           "RageAction", "apply_barbarian"]

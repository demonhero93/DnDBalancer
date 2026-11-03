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
    GIANT_FEATURES,
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
    apply_ancestral_guardian,
    apply_battlerager,
    apply_beast,
    apply_berserker,
    apply_giant,
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
    },
))

__all__ = ["BARBARIAN_CLASS", "BarbarianFeatures", "ExtendRageAction",
           "RageAction", "apply_barbarian"]

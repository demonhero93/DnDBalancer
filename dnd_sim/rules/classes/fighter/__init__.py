"""Paquete de la clase Fighter (Guerrero): código base + sus subclases.

:mod:`features` concentra el código base (Second Wind, Action Surge,
Extra Attack...). Este ``__init__`` reexporta la API (``from
dnd_sim.rules.classes.fighter import apply_fighter``) y declara la
clase en el registro genérico de :mod:`dnd_sim.rules.classes.base` con
su tabla de subclases (Arcane Archer, Battle Master, Cavalier y
Champion; ver ``TODO.md`` para la receta).
"""
from __future__ import annotations

from ..base import ClassDef, SubclassDef, register_class
from .features import ActionSurgeAction, FighterFeatures, SecondWindAction, apply_fighter
from .subclasses import (
    ARCANE_SHOTS,
    ArcaneArcherFeatures,
    BattleMasterFeatures,
    CavalierFeatures,
    ChampionFeatures,
    apply_arcane_archer,
    apply_battle_master,
    apply_cavalier,
    apply_champion,
)

#: Registro de la clase Fighter con sus subclases (claves normalizadas).
FIGHTER_CLASS = register_class(ClassDef(
    name="fighter",
    apply=apply_fighter,
    subclasses={
        "arcane_archer": SubclassDef(
            name="Arcane Archer", class_name="fighter",
            min_level=3, apply=apply_arcane_archer,
        ),
        "battle_master": SubclassDef(
            name="Battle Master", class_name="fighter",
            min_level=3, apply=apply_battle_master,
        ),
        "cavalier": SubclassDef(
            name="Cavalier", class_name="fighter",
            min_level=3, apply=apply_cavalier,
        ),
        "champion": SubclassDef(
            name="Champion", class_name="fighter",
            min_level=3, apply=apply_champion,
        ),
    },
))

__all__ = ["ActionSurgeAction", "ARCANE_SHOTS", "ArcaneArcherFeatures",
           "BattleMasterFeatures", "CavalierFeatures", "ChampionFeatures",
           "FIGHTER_CLASS", "FighterFeatures", "SecondWindAction",
           "apply_arcane_archer", "apply_battle_master", "apply_cavalier",
           "apply_champion", "apply_fighter"]

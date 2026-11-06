"""Paquete de la clase Fighter (Guerrero): código base + sus subclases.

:mod:`features` concentra el código base (Second Wind, Action Surge,
Extra Attack...). Este ``__init__`` reexporta la API (``from
dnd_sim.rules.classes.fighter import apply_fighter``) y declara la
clase en el registro genérico de :mod:`dnd_sim.rules.classes.base` con
su tabla de subclases (Arcane Archer; ver ``TODO.md`` para la receta).
"""
from __future__ import annotations

from ..base import ClassDef, SubclassDef, register_class
from .features import ActionSurgeAction, FighterFeatures, SecondWindAction, apply_fighter
from .subclasses import ARCANE_SHOTS, ArcaneArcherFeatures, apply_arcane_archer

#: Registro de la clase Fighter con sus subclases (claves normalizadas).
FIGHTER_CLASS = register_class(ClassDef(
    name="fighter",
    apply=apply_fighter,
    subclasses={
        "arcane_archer": SubclassDef(
            name="Arcane Archer", class_name="fighter",
            min_level=3, apply=apply_arcane_archer,
        ),
    },
))

__all__ = ["ActionSurgeAction", "ARCANE_SHOTS", "ArcaneArcherFeatures",
           "FIGHTER_CLASS", "FighterFeatures", "SecondWindAction",
           "apply_arcane_archer", "apply_fighter"]

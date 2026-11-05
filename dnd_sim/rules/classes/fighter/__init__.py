"""Paquete de la clase Fighter (Guerrero): registro sin subclases aún.

:mod:`features` concentra el código base (Second Wind, Action Surge,
Extra Attack...). Este ``__init__`` reexporta la API (``from
dnd_sim.rules.classes.fighter import apply_fighter``) y declara la
clase en el registro genérico de :mod:`dnd_sim.rules.classes.base` con
la tabla de subclases vacía, lista para crecer.
"""
from __future__ import annotations

from ..base import ClassDef, register_class
from .features import FighterFeatures, SecondWindAction, apply_fighter

#: Registro de la clase Fighter (la tabla de subclases queda vacía por
#: ahora; cada subclase añade aquí su ``SubclassDef``).
FIGHTER_CLASS = register_class(ClassDef(
    name="fighter",
    apply=apply_fighter,
    subclasses={},
))

__all__ = ["FIGHTER_CLASS", "FighterFeatures", "SecondWindAction",
           "apply_fighter"]

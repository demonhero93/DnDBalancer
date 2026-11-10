"""Subclases del Fighter: Arcane Archer, Battle Master y Cavalier.

La receta para añadir otra está en ``TODO.md`` (sección «Fighter: cómo
añadir una subclase»): un módulo por subclase con su ``SubclassDef``,
registro en ``..__init__`` y reexport en la fachada.
"""
from __future__ import annotations

from .arcane_archer import ARCANE_SHOTS, ArcaneArcherFeatures, apply_arcane_archer
from .battle_master import BattleMasterFeatures, apply_battle_master
from .cavalier import CavalierFeatures, apply_cavalier

__all__ = ["ARCANE_SHOTS", "ArcaneArcherFeatures", "BattleMasterFeatures",
           "CavalierFeatures", "apply_arcane_archer", "apply_battle_master",
           "apply_cavalier"]

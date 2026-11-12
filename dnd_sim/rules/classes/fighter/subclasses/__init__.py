"""Subclases del Fighter: Arcane Archer, Battle Master, Cavalier,
Champion y Psi Warrior.

La receta para añadir otra está en ``TODO.md`` (sección «Fighter: cómo
añadir una subclase»): un módulo por subclase con su ``SubclassDef``,
registro en ``..__init__`` y reexport en la fachada.
"""
from __future__ import annotations

from .arcane_archer import ARCANE_SHOTS, ArcaneArcherFeatures, apply_arcane_archer
from .battle_master import BattleMasterFeatures, apply_battle_master
from .cavalier import CavalierFeatures, apply_cavalier
from .champion import ChampionFeatures, apply_champion
from .psi_warrior import PsiWarriorFeatures, apply_psi_warrior

__all__ = ["ARCANE_SHOTS", "ArcaneArcherFeatures", "BattleMasterFeatures",
           "CavalierFeatures", "ChampionFeatures", "PsiWarriorFeatures",
           "apply_arcane_archer", "apply_battle_master", "apply_cavalier",
           "apply_champion", "apply_psi_warrior"]

"""Subclases del Fighter: Arcane Archer, Battle Master, Cavalier,
Champion, Eldritch Knight, Psi Warrior, Rune Knight y Samurai.

La receta para añadir otra está en ``TODO.md`` (sección «Fighter: cómo
añadir una subclase»): un módulo por subclase con su ``SubclassDef``,
registro en ``..__init__`` y reexport en la fachada.
"""
from __future__ import annotations

from .arcane_archer import ARCANE_SHOTS, ArcaneArcherFeatures, apply_arcane_archer
from .battle_master import BattleMasterFeatures, apply_battle_master
from .cavalier import CavalierFeatures, apply_cavalier
from .champion import ChampionFeatures, apply_champion
from .eldritch_knight import (
    ELDRITCH_KNIGHT_SPELLS,
    EldritchKnightFeatures,
    apply_eldritch_knight,
)
from .psi_warrior import PsiWarriorFeatures, apply_psi_warrior
from .rune_knight import RuneKnightFeatures, apply_rune_knight
from .samurai import SamuraiFeatures, apply_samurai

__all__ = ["ARCANE_SHOTS", "ArcaneArcherFeatures", "BattleMasterFeatures",
           "CavalierFeatures", "ChampionFeatures", "ELDRITCH_KNIGHT_SPELLS",
           "EldritchKnightFeatures", "PsiWarriorFeatures",
           "RuneKnightFeatures", "SamuraiFeatures", "apply_arcane_archer",
           "apply_battle_master",
           "apply_cavalier", "apply_champion", "apply_eldritch_knight",
           "apply_psi_warrior",
           "apply_rune_knight", "apply_samurai"]

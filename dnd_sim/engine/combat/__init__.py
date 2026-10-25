"""Motor de combate: ataques, iniciativa y bucle de rondas."""

from __future__ import annotations

from .attack import resolve_roll_mode, attack_roll, _tag_modificadores
from .encounter import CombatResult, roll_initiative, run_combat, _invoke_policy
from ...model.combatant import valid_targets  # noqa: F401  (reexport)

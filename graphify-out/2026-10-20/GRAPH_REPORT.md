# Graph Report - DnDBalancer  (2026-10-20)

## Corpus Check
- 34 files · ~18,640 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 419 nodes · 1288 edges · 10 communities (9 shown, 1 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 101 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2b5d6b37`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_area.py
- save_builder.py
- loader.py
- test_usage.py
- dnd_sim/__init__.py
- combatant.py
- combat.py
- test_multiattack.py
- test_loader_actions.py

## God Nodes (most connected - your core abstractions)
1. `load_monster()` - 42 edges
2. `run_combat()` - 33 edges
3. `Combatant` - 33 edges
4. `ActionUsage` - 27 edges
5. `UsageKind` - 24 edges
6. `CombatContext` - 23 edges
7. `Abilities` - 22 edges
8. `PlayerCharacter` - 22 edges
9. `SaveDamage` - 22 edges
10. `AreaTargeting` - 19 edges

## Surprising Connections (you probably didn't know these)
- `_area_action()` --uses--> `ActionType`  [INFERRED]
  tests/test_area.py → dnd_sim/actions.py
- `test_ataque_con_usage_conserva_el_actionusage()` --uses--> `AttackAction`  [INFERRED]
  tests/test_loader_actions.py → dnd_sim/actions.py
- `test_multiattack_del_owlbear_no_cambia()` --uses--> `AttackAction`  [INFERRED]
  tests/test_multiattack.py → dnd_sim/actions.py
- `test_multiattack_de_la_quimera_se_parsea_desde_action_options()` --uses--> `MultiattackAction`  [INFERRED]
  tests/test_multiattack.py → dnd_sim/actions.py
- `test_aliento_mapeado_a_area_con_recarga()` --uses--> `AreaTargeting`  [INFERRED]
  tests/test_loader_actions.py → dnd_sim/area.py

## Import Cycles
- None detected.

## Communities (10 total, 1 thin omitted)

### Community 0 - "test_area.py"
Cohesion: 0.21
Nodes (24): AreaTargeting, select_area_targets(), sample(), SaveDamage, SaveResult, _area_action(), _ctx(), _npc() (+16 more)

### Community 1 - "save_builder.py"
Cohesion: 0.12
Nodes (7): ActionType, AreaSaveAction, build_save_action(), build_save_effect(), damage_dice_of(), damage_options(), damage_type_of()

### Community 2 - "loader.py"
Cohesion: 0.05
Nodes (24): AttackEntry, MultiattackAction, CombatantType, _cache_path(), get_monster(), MonsterNotFoundError, NetworkError, _armor_class_value() (+16 more)

### Community 3 - "test_usage.py"
Cohesion: 0.10
Nodes (26): TurnResources, ActionUsage, begin_turn(), UsageKind, _breath(), _eventos(), _FixedRandom, _load_fixture() (+18 more)

### Community 4 - "dnd_sim/__init__.py"
Cohesion: 0.10
Nodes (21): ability_mod(), _log_target(), _log_line(), d20(), D20Result, roll_d20(), roll_dice(), RollMode (+13 more)

### Community 5 - "combatant.py"
Cohesion: 0.06
Nodes (38): Abilities, Attack, attack_roll(), resolve_roll_mode(), Combatant, Monster, normalize_ability(), PlayerCharacter (+30 more)

### Community 6 - "combat.py"
Cohesion: 0.07
Nodes (21): AttackAction, CombatAction, CombatContext, _living_enemies(), _log(), SaveAction, _valid_targets(), WeaponAttackAction (+13 more)

### Community 8 - "test_multiattack.py"
Cohesion: 0.19
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 10 - "test_loader_actions.py"
Cohesion: 0.08
Nodes (18): is_area_action(), parse_usage(), UnknownUsageError, _warn(), _log_line(), _area_action(), _data(), _load() (+10 more)

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `loader.py` to `test_area.py`, `save_builder.py`, `test_usage.py`, `dnd_sim/__init__.py`, `combatant.py`, `test_multiattack.py`, `test_loader_actions.py`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `Combatant` (e.g. with `attack_roll()` and `resolve_roll_mode()`) actually correct?**
  _`Combatant` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Should `save_builder.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11857707509881422 - nodes in this community are weakly interconnected._
- **Why does `run_combat()` connect `combat.py` to `loader.py`, `test_usage.py`, `dnd_sim/__init__.py`, `combatant.py`, `test_multiattack.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `ActionUsage` (e.g. with `AttackAction` and `CombatAction`) actually correct?**
  _`ActionUsage` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `loader.py` be split into smaller, more focused modules?**
  _Cohesion score 0.050595238095238096 - nodes in this community are weakly interconnected._
- **Why does `ActionUsage` connect `test_usage.py` to `test_loader_actions.py`, `dnd_sim/__init__.py`, `combatant.py`, `combat.py`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
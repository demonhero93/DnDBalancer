# Graph Report - DnDBalancer  (2026-10-20)

## Corpus Check
- 41 files · ~25,852 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 591 nodes · 1857 edges · 16 communities (13 shown, 3 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 133 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `74211423`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_area.py
- test_conditions.py
- api_client.py
- test_usage.py
- dnd_sim/__init__.py
- Combatant
- DamageRecorder
- test_multiattack.py
- load_monster
- test_loader_actions.py
- multiattack_parser.py
- loader.py
- roll_modifiers.py
- condition_parser.py
- test_cache_avoids_second_network

## God Nodes (most connected - your core abstractions)
1. `load_monster()` - 46 edges
2. `apply_condition()` - 41 edges
3. `Combatant` - 38 edges
4. `run_combat()` - 37 edges
5. `Abilities` - 33 edges
6. `_ctx()` - 33 edges
7. `attack_roll()` - 28 edges
8. `ActionUsage` - 27 edges
9. `CombatContext` - 25 edges
10. `PlayerCharacter` - 24 edges

## Surprising Connections (you probably didn't know these)
- `_build_party()` --uses--> `Abilities`  [INFERRED]
  main.py → dnd_sim/abilities.py
- `_area_action()` --uses--> `ActionType`  [INFERRED]
  tests/test_area.py → dnd_sim/actions.py
- `test_ataque_con_usage_conserva_el_actionusage()` --uses--> `AttackAction`  [INFERRED]
  tests/test_loader_actions.py → dnd_sim/actions.py
- `test_load_monster_maps_owlbear_multiattack()` --uses--> `MultiattackAction`  [INFERRED]
  tests/test_loader.py → dnd_sim/actions.py
- `test_aliento_mapeado_a_area_con_recarga()` --uses--> `AreaTargeting`  [INFERRED]
  tests/test_loader_actions.py → dnd_sim/area.py

## Import Cycles
- None detected.

## Communities (16 total, 3 thin omitted)

### Community 0 - "test_area.py"
Cohesion: 0.09
Nodes (32): SaveAction, AreaSaveAction, AreaTargeting, select_area_targets(), _valid_targets(), _default_targeting(), build_condition_action(), build_save_action() (+24 more)

### Community 1 - "test_conditions.py"
Cohesion: 0.06
Nodes (67): Abilities, _apply_condition_riders(), Monster, apply_condition(), _as_condition(), ConditionAction, ConditionEffect, end_turn() (+59 more)

### Community 2 - "api_client.py"
Cohesion: 0.17
Nodes (4): _cache_path(), get_monster(), MonsterNotFoundError, NetworkError

### Community 3 - "test_usage.py"
Cohesion: 0.07
Nodes (35): ActionType, CombatContext, _living_enemies(), _log(), TurnResources, _valid_targets(), run_combat(), _summarize_damage() (+27 more)

### Community 4 - "dnd_sim/__init__.py"
Cohesion: 0.05
Nodes (38): ability_mod(), _log_target(), _log_line(), CombatResult, _invoke_policy(), _mode_tag(), resolve_roll_mode(), roll_initiative() (+30 more)

### Community 5 - "Combatant"
Cohesion: 0.07
Nodes (26): WeaponAttackAction, Attack, attack_roll(), Combatant, normalize_ability(), apply_damage_modifiers(), DamageType, print_report() (+18 more)

### Community 8 - "test_multiattack.py"
Cohesion: 0.10
Nodes (15): AttackAction, CombatAction, MultiattackAction, _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta() (+7 more)

### Community 9 - "load_monster"
Cohesion: 0.20
Nodes (12): _armor_class_value(), load_monster(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper(), test_load_monster_maps_ogre() (+4 more)

### Community 10 - "test_loader_actions.py"
Cohesion: 0.11
Nodes (19): PlayerCharacter, is_area_action(), parse_usage(), UnknownUsageError, _area_action(), _data(), _load(), _raw_action() (+11 more)

### Community 11 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (6): AttackEntry, _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 13 - "loader.py"
Cohesion: 0.15
Nodes (3): _damage_type(), _simple_damage_modifiers(), _warn()

### Community 14 - "roll_modifiers.py"
Cohesion: 0.06
Nodes (13): ConditionTracker, Condition, ConditionInstance, ConditionTracker, _is_petrified(), attack_modifiers(), AttackModifiers, _condiciones() (+5 more)

### Community 15 - "condition_parser.py"
Cohesion: 0.18
Nodes (5): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with()

## Knowledge Gaps
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `load_monster` to `test_area.py`, `test_conditions.py`, `api_client.py`, `test_usage.py`, `dnd_sim/__init__.py`, `Combatant`, `test_multiattack.py`, `test_loader_actions.py`, `multiattack_parser.py`, `loader.py`, `condition_parser.py`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Combatant` (e.g. with `attack_roll()` and `resolve_roll_mode()`) actually correct?**
  _`Combatant` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_area.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08834586466165413 - nodes in this community are weakly interconnected._
- **Why does `run_combat()` connect `test_usage.py` to `test_conditions.py`, `dnd_sim/__init__.py`, `Combatant`, `DamageRecorder`, `test_multiattack.py`, `load_monster`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Abilities` (e.g. with `Combatant` and `_build_party()`) actually correct?**
  _`Abilities` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_conditions.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06382978723404255 - nodes in this community are weakly interconnected._
- **Why does `Combatant` connect `Combatant` to `test_conditions.py`, `test_usage.py`, `dnd_sim/__init__.py`, `test_multiattack.py`, `load_monster`, `test_loader_actions.py`, `roll_modifiers.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
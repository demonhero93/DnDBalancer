# Graph Report - DnDBalancer  (2026-10-20)

## Corpus Check
- 35 files · ~18,808 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 427 nodes · 1304 edges · 14 communities (12 shown, 2 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 101 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2b5d6b37`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_area.py
- combat.py
- api_client.py
- test_usage.py
- dnd_sim/__init__.py
- combatant.py
- actions.py
- run_combat
- load_monster
- test_loader_actions.py
- multiattack_parser.py
- usage_parser.py
- loader.py

## God Nodes (most connected - your core abstractions)
1. `load_monster()` - 41 edges
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
- `test_multiattack_del_owlbear_no_cambia()` --uses--> `AttackAction`  [INFERRED]
  tests/test_multiattack.py → dnd_sim/actions.py
- `test_load_monster_maps_owlbear_multiattack()` --uses--> `MultiattackAction`  [INFERRED]
  tests/test_loader.py → dnd_sim/actions.py
- `test_multiattack_de_la_quimera_se_parsea_desde_action_options()` --uses--> `MultiattackAction`  [INFERRED]
  tests/test_multiattack.py → dnd_sim/actions.py
- `test_aliento_mapeado_a_area_con_recarga()` --uses--> `AreaTargeting`  [INFERRED]
  tests/test_loader_actions.py → dnd_sim/area.py
- `_area_action()` --uses--> `AreaSaveAction`  [INFERRED]
  tests/test_loader_actions.py → dnd_sim/area.py

## Import Cycles
- None detected.

## Communities (14 total, 2 thin omitted)

### Community 0 - "test_area.py"
Cohesion: 0.10
Nodes (28): ActionType, SaveAction, TurnResources, AreaSaveAction, AreaTargeting, select_area_targets(), build_save_action(), build_save_effect() (+20 more)

### Community 1 - "combat.py"
Cohesion: 0.14
Nodes (9): CombatResult, _invoke_policy(), roll_initiative(), _run_combat(), _summarize_damage(), DamageRecorder, _extract(), first_target_policy() (+1 more)

### Community 2 - "api_client.py"
Cohesion: 0.12
Nodes (5): _cache_path(), get_monster(), MonsterNotFoundError, NetworkError, test_cache_avoids_second_network()

### Community 3 - "test_usage.py"
Cohesion: 0.08
Nodes (26): ActionUsage, begin_turn(), _log_line(), UsageKind, _breath(), _eventos(), _FixedRandom, _load_fixture() (+18 more)

### Community 4 - "dnd_sim/__init__.py"
Cohesion: 0.08
Nodes (28): ability_mod(), _log_target(), _log_line(), _valid_targets(), d20(), D20Result, roll_d20(), roll_dice() (+20 more)

### Community 5 - "combatant.py"
Cohesion: 0.08
Nodes (21): Attack, attack_roll(), resolve_roll_mode(), Combatant, CombatantType, Monster, normalize_ability(), apply_damage_modifiers() (+13 more)

### Community 6 - "actions.py"
Cohesion: 0.11
Nodes (8): CombatAction, CombatContext, _living_enemies(), _log(), MultiattackAction, _valid_targets(), WeaponAttackAction, valid_targets()

### Community 8 - "run_combat"
Cohesion: 0.09
Nodes (29): Abilities, run_combat(), PlayerCharacter, print_report(), simulate(), build_parser(), _build_party(), _load_party() (+21 more)

### Community 9 - "load_monster"
Cohesion: 0.21
Nodes (11): _armor_class_value(), load_monster(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper(), test_load_monster_maps_ogre() (+3 more)

### Community 10 - "test_loader_actions.py"
Cohesion: 0.13
Nodes (15): AttackAction, is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite() (+7 more)

### Community 11 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (6): AttackEntry, _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 12 - "usage_parser.py"
Cohesion: 0.19
Nodes (6): _simple_damage_modifiers(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

## Knowledge Gaps
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `load_monster` to `test_area.py`, `api_client.py`, `test_usage.py`, `dnd_sim/__init__.py`, `combatant.py`, `actions.py`, `run_combat`, `test_loader_actions.py`, `multiattack_parser.py`, `usage_parser.py`, `loader.py`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `Combatant` (e.g. with `attack_roll()` and `resolve_roll_mode()`) actually correct?**
  _`Combatant` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_area.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10407239819004525 - nodes in this community are weakly interconnected._
- **Why does `run_combat()` connect `run_combat` to `combat.py`, `test_usage.py`, `dnd_sim/__init__.py`, `combatant.py`, `actions.py`, `load_monster`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `ActionUsage` (e.g. with `AttackAction` and `CombatAction`) actually correct?**
  _`ActionUsage` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `combat.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._
- **Why does `ActionUsage` connect `test_usage.py` to `test_area.py`, `dnd_sim/__init__.py`, `combatant.py`, `actions.py`, `test_loader_actions.py`, `usage_parser.py`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
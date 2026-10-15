# Graph Report - DnDBalancer  (2026-10-15)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 109 nodes · 275 edges · 8 communities (7 shown, 1 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- loader.py
- dnd_sim/__init__.py
- load_monster
- api_client.py
- combat.py
- Combatant
- test_damage.py

## God Nodes (most connected - your core abstractions)
1. `Combatant` - 24 edges
2. `load_monster()` - 18 edges
3. `Attack` - 16 edges
4. `DamageType` - 14 edges
5. `apply_damage_modifiers()` - 14 edges
6. `run_combat()` - 12 edges
7. `get_monster()` - 11 edges
8. `Abilities` - 10 edges
9. `simulate()` - 10 edges
10. `attack_roll()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `test_invalid_damage_type_raises()` --calls--> `DamageType`  [EXTRACTED]
  tests/test_damage.py → dnd_sim/damage.py
- `_target()` --references--> `Combatant`  [EXTRACTED]
  tests/test_damage.py → dnd_sim/combatant.py
- `test_immune_target_takes_zero_damage()` --calls--> `simulate()`  [EXTRACTED]
  tests/test_damage.py → dnd_sim/stats.py
- `test_regression_guerrero_vs_ogro()` --calls--> `simulate()`  [EXTRACTED]
  tests/test_damage.py → dnd_sim/stats.py
- `test_armor_class_helper()` --calls--> `_armor_class_value()`  [EXTRACTED]
  tests/test_loader.py → dnd_sim/data/loader.py

## Import Cycles
- None detected.

## Communities (8 total, 1 thin omitted)

### Community 0 - "loader.py"
Cohesion: 0.13
Nodes (4): DamageType, parse_damage_type(), _damage_type(), _simple_damage_modifiers()

### Community 1 - "dnd_sim/__init__.py"
Cohesion: 0.20
Nodes (3): ability_mod(), print_report(), simulate()

### Community 2 - "load_monster"
Cohesion: 0.20
Nodes (9): _armor_class_value(), load_monster(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper(), test_cache_avoids_second_network(), test_load_monster_maps_ogre() (+1 more)

### Community 3 - "api_client.py"
Cohesion: 0.17
Nodes (4): _cache_path(), get_monster(), MonsterNotFoundError, NetworkError

### Community 4 - "combat.py"
Cohesion: 0.32
Nodes (6): attack_roll(), CombatResult, roll_initiative(), run_combat(), d20(), roll_dice()

### Community 5 - "Combatant"
Cohesion: 0.30
Nodes (7): Abilities, Attack, Combatant, test_attack_roll_log_modifier(), test_immune_target_takes_zero_damage(), test_regression_guerrero_vs_ogro(), test_strings_are_converted()

### Community 6 - "test_damage.py"
Cohesion: 0.47
Nodes (8): apply_damage_modifiers(), _target(), test_immunity_zero(), test_invalid_damage_type_raises(), test_no_modifiers_unchanged(), test_resistance_halves_damage_floor(), test_resistance_then_vulnerability_same_type(), test_vulnerability_doubles_damage()

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `load_monster` to `loader.py`, `dnd_sim/__init__.py`, `api_client.py`, `Combatant`, `test_damage.py`?**
  _High betweenness centrality (0.158) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Combatant` (e.g. with `attack_roll()` and `roll_initiative()`) actually correct?**
  _`Combatant` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Should `loader.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Why does `get_monster()` connect `api_client.py` to `loader.py`, `load_monster`?**
  _High betweenness centrality (0.141) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Attack` (e.g. with `DamageType` and `attack_roll()`) actually correct?**
  _`Attack` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Why does `Combatant` connect `Combatant` to `loader.py`, `dnd_sim/__init__.py`, `load_monster`, `combat.py`, `test_damage.py`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `DamageType` (e.g. with `Attack` and `Combatant`) actually correct?**
  _`DamageType` has 2 INFERRED edges - model-reasoned connections that need verification._
# Graph Report - DnDBalancer  (2026-10-15)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 184 nodes · 521 edges · 8 communities (7 shown, 1 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 33 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- dnd_sim/__init__.py
- Combatant
- test_loader.py
- api_client.py
- combatant.py
- main.py
- test_damage.py

## God Nodes (most connected - your core abstractions)
1. `Combatant` - 28 edges
2. `load_monster()` - 26 edges
3. `run_combat()` - 23 edges
4. `Attack` - 17 edges
5. `attack_roll()` - 16 edges
6. `apply_damage_modifiers()` - 14 edges
7. `CombatContext` - 12 edges
8. `Abilities` - 12 edges
9. `DamageType` - 12 edges
10. `PlayerCharacter` - 12 edges

## Surprising Connections (you probably didn't know these)
- `main()` --uses--> `Attack`  [INFERRED]
  main.py → dnd_sim/attack.py
- `_load_fixture()` --uses--> `Combatant`  [INFERRED]
  tests/test_loader.py → dnd_sim/combatant.py
- `test_attack_roll_log_modifier()` --calls--> `Attack`  [EXTRACTED]
  tests/test_damage.py → dnd_sim/attack.py
- `test_immune_target_takes_zero_damage()` --calls--> `Attack`  [EXTRACTED]
  tests/test_damage.py → dnd_sim/attack.py
- `test_regression_guerrero_vs_ogro()` --calls--> `Attack`  [EXTRACTED]
  tests/test_damage.py → dnd_sim/attack.py

## Import Cycles
- None detected.

## Communities (8 total, 1 thin omitted)

### Community 0 - "dnd_sim/__init__.py"
Cohesion: 0.11
Nodes (15): ActionType, TurnResources, CombatResult, _invoke_policy(), roll_initiative(), run_combat(), d20(), D20Result (+7 more)

### Community 1 - "Combatant"
Cohesion: 0.11
Nodes (12): AttackAction, CombatAction, CombatContext, _living_enemies(), _log(), _valid_targets(), WeaponAttackAction, Attack (+4 more)

### Community 2 - "test_loader.py"
Cohesion: 0.13
Nodes (18): Abilities, AttackEntry, MultiattackAction, _armor_class_value(), _damage_type(), _extract_multiattack_alternatives(), load_monster(), _norm_name() (+10 more)

### Community 3 - "api_client.py"
Cohesion: 0.12
Nodes (5): _cache_path(), get_monster(), MonsterNotFoundError, NetworkError, test_cache_avoids_second_network()

### Community 4 - "combatant.py"
Cohesion: 0.17
Nodes (4): ability_mod(), CombatantType, DamageType, parse_damage_type()

### Community 5 - "main.py"
Cohesion: 0.21
Nodes (8): PlayerCharacter, print_report(), simulate(), build_parser(), _load_party(), main(), _parse_monster_token(), test_regression_guerrero_vs_ogro()

### Community 6 - "test_damage.py"
Cohesion: 0.29
Nodes (12): Monster, apply_damage_modifiers(), _target(), test_attack_roll_log_modifier(), test_immune_target_takes_zero_damage(), test_immunity_zero(), test_invalid_damage_type_raises(), test_no_modifiers_unchanged() (+4 more)

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `test_loader.py` to `dnd_sim/__init__.py`, `Combatant`, `api_client.py`, `combatant.py`, `main.py`, `test_damage.py`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Combatant` (e.g. with `attack_roll()` and `resolve_roll_mode()`) actually correct?**
  _`Combatant` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `dnd_sim/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11341463414634147 - nodes in this community are weakly interconnected._
- **Why does `Combatant` connect `Combatant` to `dnd_sim/__init__.py`, `test_loader.py`, `combatant.py`, `main.py`, `test_damage.py`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `run_combat()` (e.g. with `ActionType` and `.use()`) actually correct?**
  _`run_combat()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `Combatant` be split into smaller, more focused modules?**
  _Cohesion score 0.10810810810810811 - nodes in this community are weakly interconnected._
- **Why does `get_monster()` connect `api_client.py` to `test_loader.py`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
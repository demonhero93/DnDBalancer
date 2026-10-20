# Graph Report - DnDBalancer  (2026-10-20)

## Corpus Check
- 47 files · ~31,197 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 703 nodes · 2245 edges · 28 communities (24 shown, 4 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 154 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `74211423`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- loader.py
- test_conditions.py
- api_client.py
- test_usage.py
- saves.py
- actions.py
- apply_condition
- test_multiattack.py
- load_monster
- test_loader_actions.py
- multiattack_parser.py
- _pj
- test_damage.py
- roll_modifiers.py
- condition_parser.py
- combatant.py
- combat.py
- test_checks_escapes.py
- test_cache_avoids_second_network
- ConditionTracker
- dnd_sim/__init__.py
- conditions.py
- SaveResult
- _duelo
- MultiattackAction
- CheckResult
- escape_parser.py

## God Nodes (most connected - your core abstractions)
1. `apply_condition()` - 58 edges
2. `load_monster()` - 49 edges
3. `Abilities` - 39 edges
4. `run_combat()` - 39 edges
5. `Combatant` - 39 edges
6. `attack_roll()` - 38 edges
7. `AttackRange` - 34 edges
8. `_pj()` - 33 edges
9. `_ctx()` - 32 edges
10. `CombatContext` - 27 edges

## Surprising Connections (you probably didn't know these)
- `test_consumes_action_gasta_la_accion_del_turno()` --uses--> `ActionType`  [INFERRED]
  tests/test_checks_escapes.py → dnd_sim/actions.py
- `test_sin_consumes_action_conserva_la_accion()` --uses--> `ActionType`  [INFERRED]
  tests/test_checks_escapes.py → dnd_sim/actions.py
- `test_ataque_con_usage_conserva_el_actionusage()` --uses--> `AttackAction`  [INFERRED]
  tests/test_loader_actions.py → dnd_sim/actions.py
- `test_multiattack_del_owlbear_no_cambia()` --uses--> `AttackAction`  [INFERRED]
  tests/test_multiattack.py → dnd_sim/actions.py
- `test_load_monster_maps_owlbear_multiattack()` --uses--> `MultiattackAction`  [INFERRED]
  tests/test_loader.py → dnd_sim/actions.py

## Import Cycles
- None detected.

## Communities (28 total, 4 thin omitted)

### Community 0 - "loader.py"
Cohesion: 0.07
Nodes (36): ActionType, SaveAction, AreaSaveAction, AreaTargeting, _log_line(), select_area_targets(), _valid_targets(), ConditionAction (+28 more)

### Community 1 - "test_conditions.py"
Cohesion: 0.05
Nodes (69): Abilities, Monster, end_turn(), RepeatSave, parse_range_type(), AttackRange, resolve_attack_range(), print_report() (+61 more)

### Community 2 - "api_client.py"
Cohesion: 0.17
Nodes (4): _cache_path(), get_monster(), MonsterNotFoundError, NetworkError

### Community 3 - "test_usage.py"
Cohesion: 0.07
Nodes (29): TurnResources, run_combat(), _summarize_damage(), DamageRecorder, ActionUsage, _log_line(), UsageKind, _breath() (+21 more)

### Community 4 - "saves.py"
Cohesion: 0.13
Nodes (12): inflict_damage(), _notify_damage_dealt(), _notify_damage_taken(), parse_damage_type(), apply_save_damage(), _as_combat_context(), _inflict_for_save(), normalize_ability() (+4 more)

### Community 5 - "actions.py"
Cohesion: 0.07
Nodes (14): AttackAction, CombatAction, CombatContext, _living_enemies(), _log(), _valid_targets(), WeaponAttackAction, Attack (+6 more)

### Community 6 - "apply_condition"
Cohesion: 0.18
Nodes (16): apply_condition(), attempt_escapes(), EscapeCheck, _log_line(), begin_turn(), _ctx(), test_con_dos_caracteristicas_se_elige_una_al_azar(), test_con_una_sola_caracteristica_no_consume_rng() (+8 more)

### Community 8 - "test_multiattack.py"
Cohesion: 0.20
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 9 - "load_monster"
Cohesion: 0.20
Nodes (12): _armor_class_value(), load_monster(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper(), test_load_monster_maps_ogre() (+4 more)

### Community 10 - "test_loader_actions.py"
Cohesion: 0.09
Nodes (20): PlayerCharacter, is_area_action(), parse_usage(), UnknownUsageError, _warn(), _area_action(), _data(), _load() (+12 more)

### Community 11 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (6): AttackEntry, _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 12 - "_pj"
Cohesion: 0.13
Nodes (15): ability_check(), ability_check_bonus(), check_modifiers(), _pj(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_el_escape_con_ventaja_condicionada_por_envenenamiento(), test_el_estado_de_distancia_inicial_y_el_reset(), test_la_cobertura_no_cambia_las_salvaciones() (+7 more)

### Community 13 - "test_damage.py"
Cohesion: 0.14
Nodes (16): apply_damage_modifiers(), DamageType, _is_petrified(), _simple_damage_modifiers(), _guerrero_y_ogro(), _target(), test_danio_medio_por_combatiente_y_equipo(), test_immunity_zero() (+8 more)

### Community 14 - "roll_modifiers.py"
Cohesion: 0.08
Nodes (9): _mode_tag(), resolve_roll_mode(), RollMode, attack_modifiers(), AttackModifiers, CheckModifiers, _condiciones(), save_modifiers() (+1 more)

### Community 15 - "condition_parser.py"
Cohesion: 0.14
Nodes (7): ConditionEffect, _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), test_una_condicion_sin_salvacion_ni_escape_lanza_value_error()

### Community 16 - "combatant.py"
Cohesion: 0.13
Nodes (5): ability_mod(), CombatState, CombatantType, CombatState, Condition

### Community 17 - "combat.py"
Cohesion: 0.18
Nodes (8): _apply_condition_riders(), CombatResult, _invoke_policy(), roll_initiative(), _run_combat(), _extract(), first_target_policy(), random_policy()

### Community 18 - "test_checks_escapes.py"
Cohesion: 0.16
Nodes (13): parse_escape(), effective_ac(), _data(), _load(), test_el_estado_cambia_ataque_a_ataque_en_un_multiataque(), test_el_fixture_de_la_constriccion_tiene_escape_y_avisa_de_grappled(), test_el_fixture_de_la_telaraña_carga_restrained_con_escape(), test_en_un_combate_la_telaraña_inmoviliza_y_el_pj_intenta_escapar() (+5 more)

### Community 20 - "ConditionTracker"
Cohesion: 0.12
Nodes (4): ConditionTracker, ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 21 - "dnd_sim/__init__.py"
Cohesion: 0.24
Nodes (4): d20(), D20Result, roll_d20(), roll_dice()

### Community 22 - "conditions.py"
Cohesion: 0.20
Nodes (6): _as_condition(), Condition, _contar(), _label(), _queda_accion(), test_el_enum_no_contiene_condiciones_excluidas()

### Community 23 - "SaveResult"
Cohesion: 0.28
Nodes (7): _log_target(), _log_line(), _mode_tag(), _outcome_tag(), _log_line_outcome(), SaveResult, fake_saving_throw()

### Community 24 - "_duelo"
Cohesion: 0.31
Nodes (7): _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

### Community 26 - "CheckResult"
Cohesion: 0.33
Nodes (5): CheckResult, _check_fijo(), _fake(), test_escape_con_exito_elimina_la_condicion(), test_escape_con_fallo_la_condicion_sigue()

## Knowledge Gaps
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `load_monster` to `loader.py`, `test_conditions.py`, `api_client.py`, `test_usage.py`, `saves.py`, `actions.py`, `test_multiattack.py`, `test_loader_actions.py`, `multiattack_parser.py`, `test_damage.py`, `condition_parser.py`, `combatant.py`, `test_checks_escapes.py`, `dnd_sim/__init__.py`, `MultiattackAction`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Abilities` (e.g. with `Combatant` and `_build_party()`) actually correct?**
  _`Abilities` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `loader.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06738245094409478 - nodes in this community are weakly interconnected._
- **Why does `run_combat()` connect `test_usage.py` to `test_conditions.py`, `actions.py`, `apply_condition`, `test_multiattack.py`, `load_monster`, `test_damage.py`, `combat.py`, `test_checks_escapes.py`, `dnd_sim/__init__.py`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `Combatant` (e.g. with `attack_roll()` and `resolve_roll_mode()`) actually correct?**
  _`Combatant` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_conditions.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05386138613861386 - nodes in this community are weakly interconnected._
- **Why does `Combatant` connect `actions.py` to `loader.py`, `test_conditions.py`, `test_usage.py`, `saves.py`, `apply_condition`, `load_monster`, `test_loader_actions.py`, `test_damage.py`, `roll_modifiers.py`, `combatant.py`, `combat.py`, `ConditionTracker`, `dnd_sim/__init__.py`, `conditions.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
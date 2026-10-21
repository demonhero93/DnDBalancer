# Graph Report - DnDBalancer  (2026-10-21)

## Corpus Check
- 98 files · ~52,402 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 991 nodes · 3271 edges · 39 communities (32 shown, 7 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 210 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5dceefea`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_area.py
- actions.py
- test_legendary.py
- test_usage.py
- saves.py
- Combatant
- spell_parser.py
- legendary_parser.py
- Condition
- test_loader_actions.py
- loader.py
- test_checks_escapes.py
- combatant.py
- test_multiattack.py
- condition_parser.py
- CombatContext
- combat.py
- LegendaryState
- damage.py
- simulate
- roll_modifiers.py
- ConditionTracker
- test_conditions.py
- spell_action
- area.py
- AttackModifiers
- test_spells.py
- Attack
- Spell
- parse_spell
- test_damage.py
- AreaSaveAction
- warnings
- multiattack_parser.py
- roll_dice
- dnd_sim/__init__.py
- ConditionEffect
- usage.py

## God Nodes (most connected - your core abstractions)
1. `apply_condition()` - 75 edges
2. `load_monster()` - 61 edges
3. `_load()` - 48 edges
4. `Abilities` - 47 edges
5. `CombatContext` - 46 edges
6. `parse_spell()` - 45 edges
7. `attack_roll()` - 44 edges
8. `run_combat()` - 44 edges
9. `Combatant` - 41 edges
10. `ActionType` - 40 edges

## Surprising Connections (you probably didn't know these)
- `_build_party()` --uses--> `Abilities`  [INFERRED]
  main.py → dnd_sim/abilities.py
- `_area_action()` --uses--> `ActionType`  [INFERRED]
  tests/test_area.py → dnd_sim/actions.py
- `test_consumes_action_gasta_la_accion_del_turno()` --uses--> `ActionType`  [INFERRED]
  tests/test_checks_escapes.py → dnd_sim/actions.py
- `test_sin_consumes_action_conserva_la_accion()` --uses--> `ActionType`  [INFERRED]
  tests/test_checks_escapes.py → dnd_sim/actions.py
- `test_el_tiempo_de_casteo_marca_el_tipo_de_accion()` --uses--> `ActionType`  [INFERRED]
  tests/test_spells.py → dnd_sim/actions.py

## Import Cycles
- None detected.

## Communities (39 total, 7 thin omitted)

### Community 0 - "test_area.py"
Cohesion: 0.29
Nodes (18): AreaTargeting, select_area_targets(), _area_action(), _ctx(), _npc(), _pj(), _save_forzado(), test_cada_pj_es_elegido_aproximadamente_el_62_5_por_ciento() (+10 more)

### Community 1 - "actions.py"
Cohesion: 0.12
Nodes (6): ActionType, CombatAction, _log(), WeaponAttackAction, ConditionAction, _default_targeting()

### Community 2 - "test_legendary.py"
Cohesion: 0.05
Nodes (68): _accion_utilizable(), _acciones_asequibles(), _combate_terminado(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), legendary_phase() (+60 more)

### Community 3 - "test_usage.py"
Cohesion: 0.08
Nodes (28): TurnResources, run_combat(), _summarize_damage(), ActionUsage, UsageKind, _breath(), _eventos(), _FixedRandom (+20 more)

### Community 4 - "saves.py"
Cohesion: 0.11
Nodes (19): _log_target(), _apply_condition_riders(), legendary_resistance(), registrar_resistencia_legendaria(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save() (+11 more)

### Community 6 - "spell_parser.py"
Cohesion: 0.07
Nodes (12): _afecta_movimiento(), _crea_objetos(), _dado_por_nivel(), _dados_de_dano(), _dc_ability(), _elementos_totales(), _es_ilusion(), _numero_elementos() (+4 more)

### Community 8 - "legendary_parser.py"
Cohesion: 0.09
Nodes (16): _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary(), _por_datos() (+8 more)

### Community 9 - "Condition"
Cohesion: 0.22
Nodes (14): Condition, _ctx(), _npc(), _pj(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizado_invierte_los_objetivos_de_ataque(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado(), test_el_hechizo_verdadero_da_ventaja_en_los_ataques() (+6 more)

### Community 10 - "test_loader_actions.py"
Cohesion: 0.13
Nodes (15): AttackAction, is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite() (+7 more)

### Community 11 - "loader.py"
Cohesion: 0.12
Nodes (7): parse_range_type(), _damage_type(), _extract_multiattack_alternatives(), load_monster(), _simple_damage_modifiers(), build_condition_action(), build_spell_actions()

### Community 12 - "test_checks_escapes.py"
Cohesion: 0.06
Nodes (53): ability_check(), ability_check_bonus(), _guia(), apply_condition(), _as_condition(), attempt_escapes(), _contar(), EscapeCheck (+45 more)

### Community 13 - "combatant.py"
Cohesion: 0.16
Nodes (4): CombatState, CombatantType, CombatState, Condition

### Community 14 - "test_multiattack.py"
Cohesion: 0.05
Nodes (29): MultiattackAction, _cache_path(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError, _armor_class_value(), _load_fixture() (+21 more)

### Community 15 - "condition_parser.py"
Cohesion: 0.15
Nodes (6): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), normalize_ability()

### Community 16 - "CombatContext"
Cohesion: 0.14
Nodes (6): CombatContext, _living_enemies(), _equipos_vivos(), HealAction, SpellStateAction, valid_targets()

### Community 17 - "combat.py"
Cohesion: 0.21
Nodes (8): CombatResult, _invoke_policy(), _mode_tag(), roll_initiative(), _run_combat(), _extract(), first_target_policy(), random_policy()

### Community 19 - "damage.py"
Cohesion: 0.16
Nodes (5): DamageRecorder, inflict_damage(), _notify_damage_dealt(), _notify_damage_taken(), parse_damage_type()

### Community 20 - "simulate"
Cohesion: 0.19
Nodes (8): print_report(), simulate(), build_parser(), _build_party(), _load_party(), main(), _parse_monster_token(), test_informe_final_con_apartados_de_pj_y_monstruros()

### Community 21 - "roll_modifiers.py"
Cohesion: 0.15
Nodes (6): attack_modifiers(), check_modifiers(), CheckModifiers, _condiciones(), effective_ac(), save_modifiers()

### Community 22 - "ConditionTracker"
Cohesion: 0.12
Nodes (4): ConditionTracker, ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 23 - "test_conditions.py"
Cohesion: 0.06
Nodes (68): Abilities, _actualizar_distancia(), attack_roll(), Monster, end_turn(), AttackRange, resolve_attack_range(), _ataque() (+60 more)

### Community 24 - "spell_action"
Cohesion: 0.13
Nodes (7): apply_concentration(), duracion_en_rondas(), spell_action(), SpellAction, SpellAttackAction, SpellFixedDamageAction, test_un_cantrip_de_ataque_se_convierte_en_accion_de_ataque()

### Community 25 - "area.py"
Cohesion: 0.18
Nodes (5): _log_line(), pick(), sample(), test_sample_devuelve_todos_sin_consumir_rng(), test_sample_k_menor_devuelve_distintos_y_uniformes()

### Community 27 - "test_spells.py"
Cohesion: 0.16
Nodes (9): parse_spellcasting(), Spellcasting, test_el_lanzador_se_lee_de_los_special_abilities(), test_el_lich_carga_su_cantrip_utile(), test_el_ogre_no_carga_hechizos(), test_los_hechizos_de_nivel_1_consumen_slots(), test_un_cantrip_se_puede_lanzar_en_cada_turno(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado() (+1 more)

### Community 28 - "Attack"
Cohesion: 0.17
Nodes (9): Attack, PlayerCharacter, _guerrero_y_ogro(), test_attack_roll_log_modifier(), test_danio_medio_por_combatiente_y_equipo(), test_immune_target_takes_zero_damage(), test_regression_guerrero_vs_ogro(), test_regression_guerrero_vs_owlbear() (+1 more)

### Community 30 - "parse_spell"
Cohesion: 0.20
Nodes (17): parse_spell(), _spell_data(), _spellcasting(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_proyectil_magico_es_dano_automatico(), test_el_tiempo_de_casteo_marca_el_tipo_de_accion(), test_las_ilusiones_sin_estado_en_el_rival_se_ignoran() (+9 more)

### Community 31 - "test_damage.py"
Cohesion: 0.27
Nodes (10): apply_damage_modifiers(), DamageType, _is_petrified(), _target(), test_immunity_zero(), test_invalid_damage_type_raises(), test_no_modifiers_unchanged(), test_resistance_halves_damage_floor() (+2 more)

### Community 32 - "AreaSaveAction"
Cohesion: 0.16
Nodes (6): SaveAction, AreaSaveAction, RepeatSave, build_save_action(), SaveDamage, test_la_resistencia_funciona_en_todas_las_rutas()

### Community 33 - "warnings"
Cohesion: 0.21
Nodes (6): _resistencia_legendaria(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 34 - "multiattack_parser.py"
Cohesion: 0.21
Nodes (5): AttackEntry, extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 36 - "dnd_sim/__init__.py"
Cohesion: 0.18
Nodes (7): CheckResult, resolve_roll_mode(), d20(), D20Result, roll_d20(), RollMode, SaveModifiers

### Community 37 - "ConditionEffect"
Cohesion: 0.33
Nodes (3): ConditionEffect, _condicion_con_salvacion(), test_una_condicion_sin_salvacion_ni_escape_lanza_value_error()

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `loader.py` to `AreaSaveAction`, `actions.py`, `multiattack_parser.py`, `warnings`, `dnd_sim/__init__.py`, `test_legendary.py`, `test_usage.py`, `legendary_parser.py`, `test_loader_actions.py`, `test_checks_escapes.py`, `combatant.py`, `test_multiattack.py`, `condition_parser.py`, `simulate`, `test_conditions.py`, `test_spells.py`, `Attack`, `test_damage.py`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `ActionType` and `UnknownUsageError`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `actions.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12307692307692308 - nodes in this community are weakly interconnected._
- **Why does `apply_condition()` connect `test_checks_escapes.py` to `AreaSaveAction`, `actions.py`, `test_legendary.py`, `saves.py`, `dnd_sim/__init__.py`, `Condition`, `CombatContext`, `combat.py`, `ConditionTracker`, `test_conditions.py`, `spell_action`, `area.py`, `test_spells.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Abilities` (e.g. with `Combatant` and `_build_party()`) actually correct?**
  _`Abilities` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_legendary.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0509020618556701 - nodes in this community are weakly interconnected._
- **Why does `run_combat()` connect `test_usage.py` to `test_legendary.py`, `dnd_sim/__init__.py`, `Combatant`, `test_checks_escapes.py`, `test_multiattack.py`, `CombatContext`, `combat.py`, `damage.py`, `simulate`, `test_conditions.py`, `area.py`, `test_spells.py`, `Attack`, `test_damage.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
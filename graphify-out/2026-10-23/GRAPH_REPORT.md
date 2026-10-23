# Graph Report - DnDBalancer  (2026-10-23)

## Corpus Check
- 115 files · ~67,122 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 1201 nodes · 4154 edges · 46 communities (38 shown, 8 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 294 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `516290b7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_area.py
- test_attach.py
- test_legendary.py
- run_combat
- saves.py
- Condition
- parse_spell
- test_loader_actions.py
- test_spells.py
- PlayerCharacter
- AttackRange
- test_conditions.py
- parse_usage
- conditions.py
- escape_parser.py
- CombatContext
- combat.py
- legendary.py
- combatant.py
- json
- attack_roll
- ConditionTracker
- test_invisibility.py
- traits.py
- MultiattackAction
- begin_turn
- build_spell_actions
- dnd_sim/__init__.py
- test_checks_escapes.py
- _spell_data
- test_damage.py
- spell_action
- _pj
- loader.py
- Combatant
- ability_check
- attack.py
- AttackModifiers
- AreaSaveAction
- test_cache_avoids_second_network
- normalize_ability
- load_monster
- _build_party
- legendary_parser.py
- test_prueba_con_envenenado_o_aterrorizado_da_desventaja

## God Nodes (most connected - your core abstractions)
1. `apply_condition()` - 88 edges
2. `load_monster()` - 81 edges
3. `attack_roll()` - 70 edges
4. `Condition` - 69 edges
5. `CombatContext` - 58 edges
6. `parse_spell()` - 56 edges
7. `Abilities` - 52 edges
8. `run_combat()` - 52 edges
9. `AttackRange` - 51 edges
10. `Attack` - 50 edges

## Surprising Connections (you probably didn't know these)
- `test_invisible_es_una_condicion_modelada()` --uses--> `Condition`  [INFERRED]
  tests/test_invisibility.py → dnd_sim/conditions.py
- `_build_party()` --uses--> `Abilities`  [INFERRED]
  main.py → dnd_sim/abilities.py
- `_area_action()` --uses--> `ActionType`  [INFERRED]
  tests/test_area.py → dnd_sim/actions.py
- `test_el_desenganche_es_una_prueba_de_fuerza_cd_16_que_gasta_la_accion()` --uses--> `ActionType`  [INFERRED]
  tests/test_attach.py → dnd_sim/actions.py
- `test_sin_accion_disponible_no_intenta_desengancharse()` --uses--> `ActionType`  [INFERRED]
  tests/test_attach.py → dnd_sim/actions.py

## Import Cycles
- None detected.

## Communities (46 total, 8 thin omitted)

### Community 0 - "test_area.py"
Cohesion: 0.20
Nodes (23): AreaTargeting, select_area_targets(), _default_targeting(), build_save_action(), SaveDamage, _area_action(), _ctx(), _npc() (+15 more)

### Community 1 - "test_attach.py"
Cohesion: 0.08
Nodes (34): Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _log_line(), _ya_cegado_por(), inflict_damage() (+26 more)

### Community 2 - "test_legendary.py"
Cohesion: 0.07
Nodes (60): legendary_phase(), saving_throw(), _contexto(), _data(), _estado(), _legendaria(), _load(), _pj() (+52 more)

### Community 3 - "run_combat"
Cohesion: 0.05
Nodes (39): run_combat(), _summarize_damage(), DamageRecorder, _log_line(), UsageKind, _data(), _load(), _pj() (+31 more)

### Community 4 - "saves.py"
Cohesion: 0.12
Nodes (16): _log_target(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save(), _log_line(), _mode_tag(), _outcome_tag() (+8 more)

### Community 5 - "Condition"
Cohesion: 0.08
Nodes (32): Condition, doblar_dados(), check_modifiers(), CheckModifiers, _condiciones(), save_modifiers(), SaveModifiers, test_el_enum_no_contiene_condiciones_excluidas() (+24 more)

### Community 6 - "parse_spell"
Cohesion: 0.08
Nodes (17): _afecta_movimiento(), _condicion_con_salvacion(), _crea_objetos(), _dados_de_dano(), _dc_ability(), _elementos_totales(), _es_ilusion(), _numero_elementos() (+9 more)

### Community 8 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (14): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+6 more)

### Community 9 - "test_spells.py"
Cohesion: 0.17
Nodes (16): TurnResources, apply_concentration(), _ctx(), _npc(), _pj(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado(), test_el_hechizo_verdadero_da_ventaja_en_los_ataques() (+8 more)

### Community 10 - "PlayerCharacter"
Cohesion: 0.14
Nodes (13): PlayerCharacter, print_report(), simulate(), build_parser(), _load_party(), main(), _parse_monster_token(), _guerrero_y_ogro() (+5 more)

### Community 11 - "AttackRange"
Cohesion: 0.19
Nodes (20): parse_traits(), RollMode, attack_modifiers(), AttackRange, _ataque_melee(), _datos(), _pj(), _sahuagin() (+12 more)

### Community 12 - "test_conditions.py"
Cohesion: 0.07
Nodes (64): Abilities, _apply_condition_riders(), Monster, apply_condition(), end_turn(), RepeatSave, parse_range_type(), resolve_attack_range() (+56 more)

### Community 13 - "parse_usage"
Cohesion: 0.24
Nodes (5): parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 14 - "conditions.py"
Cohesion: 0.21
Nodes (6): _as_condition(), _contar(), _label(), _log_line(), _queda_accion(), remove_condition()

### Community 15 - "escape_parser.py"
Cohesion: 0.18
Nodes (5): has_escape_text(), parse_escape(), _data(), test_el_fixture_de_la_constriccion_tiene_escape_y_avisa_de_grappled(), test_el_fixture_de_la_telaraña_carga_restrained_con_escape()

### Community 16 - "CombatContext"
Cohesion: 0.10
Nodes (9): CombatContext, _living_enemies(), _log(), _contexto_de_reaccion(), HealAction, SpellStateAction, trigger_reaction(), _objetivo_enganche() (+1 more)

### Community 17 - "combat.py"
Cohesion: 0.10
Nodes (16): _agrandado(), _bonus_de_tamano(), CombatResult, _dados_de_ataque(), _invoke_policy(), _reaccion_si_procede(), resolve_roll_mode(), roll_initiative() (+8 more)

### Community 18 - "legendary.py"
Cohesion: 0.08
Nodes (14): _accion_utilizable(), _acciones_asequibles(), _combate_terminado(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), _equipos_vivos() (+6 more)

### Community 19 - "combatant.py"
Cohesion: 0.13
Nodes (5): ability_mod(), CombatState, CombatantType, CombatState, Condition

### Community 20 - "json"
Cohesion: 0.17
Nodes (5): _cache_path(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError

### Community 21 - "attack_roll"
Cohesion: 0.19
Nodes (17): Attack, _actualizar_distancia(), attack_roll(), _mode_tag(), _ataque_melee(), _ataque_ranged(), _azer(), _ctx() (+9 more)

### Community 22 - "ConditionTracker"
Cohesion: 0.12
Nodes (4): ConditionTracker, ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 23 - "test_invisibility.py"
Cohesion: 0.28
Nodes (15): _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj(), test_atacar_a_un_invisible_tiene_desventaja(), test_atacar_deja_de_ser_invisible() (+7 more)

### Community 24 - "traits.py"
Cohesion: 0.11
Nodes (5): BloodFrenzy, DamageTransfer, HeatedBody, _log_line(), Trait

### Community 26 - "begin_turn"
Cohesion: 0.19
Nodes (16): attempt_escapes(), EscapeCheck, begin_turn(), _check_fijo(), _ctx(), test_con_dos_caracteristicas_se_elige_una_al_azar(), test_con_una_sola_caracteristica_no_consume_rng(), test_consumes_action_gasta_la_accion_del_turno() (+8 more)

### Community 27 - "build_spell_actions"
Cohesion: 0.39
Nodes (7): build_spell_actions(), _desde_fixture(), _monstruo_lanzador(), test_gastar_un_slot_no_afecta_a_los_otros_niveles(), test_la_reaccion_gasta_el_slot_de_su_nivel(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_un_pool_por_nivel()

### Community 28 - "dnd_sim/__init__.py"
Cohesion: 0.09
Nodes (13): ActionType, AttackAction, CombatAction, SaveAction, WeaponAttackAction, D20Result, roll_d20(), roll_dice() (+5 more)

### Community 29 - "test_checks_escapes.py"
Cohesion: 0.25
Nodes (9): effective_ac(), _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_la_ca_efectiva_sube_dos_a_distancia(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo() (+1 more)

### Community 30 - "_spell_data"
Cohesion: 0.11
Nodes (21): _spell_data(), _spellcasting(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_lich_carga_su_cantrip_utile(), test_el_tiempo_de_casteo_marca_el_tipo_de_accion(), test_las_ilusiones_sin_estado_en_el_rival_se_ignoran(), test_los_hechizos_de_movimiento_se_ignoran() (+13 more)

### Community 31 - "test_damage.py"
Cohesion: 0.40
Nodes (9): apply_damage_modifiers(), _target(), test_immunity_zero(), test_invalid_damage_type_raises(), test_no_modifiers_unchanged(), test_resistance_halves_damage_floor(), test_resistance_then_vulnerability_same_type(), test_strings_are_converted() (+1 more)

### Community 32 - "spell_action"
Cohesion: 0.11
Nodes (11): parse_spellcasting(), dado_por_nivel(), Spell, spell_action(), Spellcasting, test_el_lanzador_se_lee_de_los_special_abilities(), test_el_upcast_reescala_el_dano_y_la_curacion(), test_initialize_slots_usa_la_tabla_real_de_un_lanzador_completo() (+3 more)

### Community 33 - "_pj"
Cohesion: 0.19
Nodes (13): _load(), _pj(), test_el_escape_se_intenta_al_inicio_del_turno(), test_el_estado_cambia_ataque_a_ataque_en_un_multiataque(), test_el_estado_de_distancia_inicial_y_el_reset(), test_en_un_combate_la_telaraña_inmoviliza_y_el_pj_intenta_escapar(), test_la_cobertura_no_cambia_las_salvaciones(), test_la_telaraña_aplica_inmovilizado_sin_salvacion() (+5 more)

### Community 34 - "loader.py"
Cohesion: 0.11
Nodes (8): AttackEntry, _extract_multiattack_alternatives(), _norm_name(), _simple_damage_modifiers(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 36 - "ability_check"
Cohesion: 0.11
Nodes (11): ability_check(), ability_check_bonus(), CheckResult, _guia(), _fake(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_probabilidad_de_liberarse_con_cd_12(), test_prueba_con_ventaja_da_75_por_ciento() (+3 more)

### Community 37 - "attack.py"
Cohesion: 0.23
Nodes (3): DamageType, _is_petrified(), parse_damage_type()

### Community 39 - "AreaSaveAction"
Cohesion: 0.13
Nodes (4): AreaSaveAction, _log_line(), ConditionAction, build_condition_action()

### Community 42 - "load_monster"
Cohesion: 0.17
Nodes (14): _armor_class_value(), _damage_type(), load_monster(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper() (+6 more)

### Community 44 - "legendary_parser.py"
Cohesion: 0.06
Nodes (24): ConditionEffect, _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), _coincide_nombre(), _con_nombre_limpio() (+16 more)

## Knowledge Gaps
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `load_monster` to `test_area.py`, `test_attach.py`, `test_legendary.py`, `run_combat`, `Condition`, `parse_spell`, `test_loader_actions.py`, `test_spells.py`, `PlayerCharacter`, `AttackRange`, `test_conditions.py`, `parse_usage`, `CombatContext`, `combatant.py`, `json`, `attack_roll`, `test_invisibility.py`, `MultiattackAction`, `build_spell_actions`, `dnd_sim/__init__.py`, `test_checks_escapes.py`, `_spell_data`, `test_damage.py`, `_pj`, `loader.py`, `AreaSaveAction`, `normalize_ability`, `legendary_parser.py`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `ActionType` and `UnknownUsageError`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08166969147005444 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `test_legendary.py`, `parse_spell`, `test_spells.py`, `AttackRange`, `test_conditions.py`, `conditions.py`, `combat.py`, `combatant.py`, `attack_roll`, `ConditionTracker`, `test_invisibility.py`, `dnd_sim/__init__.py`, `test_checks_escapes.py`, `_spell_data`, `loader.py`, `Combatant`, `ability_check`, `attack.py`, `legendary_parser.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `attack_roll()` (e.g. with `Attack` and `Combatant`) actually correct?**
  _`attack_roll()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_legendary.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0695970695970696 - nodes in this community are weakly interconnected._
- **Why does `CombatContext` connect `CombatContext` to `test_area.py`, `test_attach.py`, `test_legendary.py`, `run_combat`, `Condition`, `AreaSaveAction`, `test_spells.py`, `test_conditions.py`, `combat.py`, `legendary.py`, `attack_roll`, `test_invisibility.py`, `begin_turn`, `build_spell_actions`, `dnd_sim/__init__.py`, `test_checks_escapes.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
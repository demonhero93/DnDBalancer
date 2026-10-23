# Graph Report - DnDBalancer  (2026-10-23)

## Corpus Check
- 116 files · ~68,794 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 1230 nodes · 4291 edges · 48 communities (41 shown, 7 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 314 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `af5c4e08`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_area.py
- test_attach.py
- test_legendary.py
- ActionUsage
- saves.py
- Condition
- spell_parser.py
- load_monster
- _pj
- main.py
- test_invisibility.py
- test_conditions.py
- test_loader_actions.py
- apply_condition
- condition_parser.py
- CombatContext
- combat.py
- legendary.py
- combatant.py
- test_multiattack.py
- run_combat
- ConditionTracker
- json
- MultiattackAction
- attack_roll
- begin_turn
- test_spells.py
- Spellcasting
- PlayerCharacter
- parse_spell
- test_damage.py
- spell_action
- test_checks_escapes.py
- loader.py
- parse_usage
- ability_check
- DamageRecorder
- usage.py
- CheckResult
- escape_parser.py
- dnd_sim/__init__.py
- TurnResources
- AttackRange
- legendary_parser.py
- LegendaryState
- ConditionAction
- ConditionEffect

## God Nodes (most connected - your core abstractions)
1. `apply_condition()` - 92 edges
2. `load_monster()` - 86 edges
3. `attack_roll()` - 79 edges
4. `Condition` - 73 edges
5. `CombatContext` - 60 edges
6. `Attack` - 56 edges
7. `parse_spell()` - 56 edges
8. `Abilities` - 53 edges
9. `run_combat()` - 52 edges
10. `AttackRange` - 51 edges

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

## Communities (48 total, 7 thin omitted)

### Community 0 - "test_area.py"
Cohesion: 0.20
Nodes (22): AreaTargeting, select_area_targets(), _default_targeting(), sample(), _area_action(), _ctx(), _npc(), _pj() (+14 more)

### Community 1 - "test_attach.py"
Cohesion: 0.06
Nodes (37): Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _log_line(), _ya_cegado_por(), inflict_damage() (+29 more)

### Community 2 - "test_legendary.py"
Cohesion: 0.07
Nodes (60): legendary_phase(), LegendaryAction, saving_throw(), _contexto(), _data(), _estado(), _legendaria(), _load() (+52 more)

### Community 3 - "ActionUsage"
Cohesion: 0.21
Nodes (11): ActionUsage, UsageKind, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar(), test_per_day_dos_usos_y_luego_can_use_falso(), test_per_day_no_tira_recarga(), test_per_day_reset_restaura_todos_los_usos(), test_recharge_5_6_porcentaje_de_exito() (+3 more)

### Community 4 - "saves.py"
Cohesion: 0.11
Nodes (17): _log_target(), _log_line(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save(), _log_line(), _mode_tag() (+9 more)

### Community 5 - "Condition"
Cohesion: 0.09
Nodes (32): Condition, doblar_dados(), check_modifiers(), _condiciones(), save_modifiers(), apply_concentration(), SpellAction, test_el_enum_no_contiene_condiciones_excluidas() (+24 more)

### Community 6 - "spell_parser.py"
Cohesion: 0.07
Nodes (12): _afecta_movimiento(), _condicion_con_salvacion(), _crea_objetos(), _dados_de_dano(), _dc_ability(), _elementos_totales(), _es_ilusion(), _numero_elementos() (+4 more)

### Community 8 - "load_monster"
Cohesion: 0.13
Nodes (15): _armor_class_value(), load_monster(), _norm_name(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper() (+7 more)

### Community 9 - "_pj"
Cohesion: 0.19
Nodes (15): _ctx(), _npc(), _pj(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizado_invierte_los_objetivos_de_ataque(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado(), test_el_hechizo_verdadero_da_ventaja_en_los_ataques() (+7 more)

### Community 10 - "main.py"
Cohesion: 0.21
Nodes (6): print_report(), build_parser(), _build_party(), _load_party(), main(), _parse_monster_token()

### Community 11 - "test_invisibility.py"
Cohesion: 0.07
Nodes (44): resolve_roll_mode(), parse_traits(), RollMode, attack_modifiers(), AttackModifiers, CheckModifiers, SaveModifiers, BloodFrenzy (+36 more)

### Community 12 - "test_conditions.py"
Cohesion: 0.08
Nodes (56): Abilities, Monster, end_turn(), parse_range_type(), _ataque(), _ctx(), _data(), _duelo() (+48 more)

### Community 13 - "test_loader_actions.py"
Cohesion: 0.18
Nodes (13): _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga(), test_ataque_con_usage_conserva_el_actionusage() (+5 more)

### Community 14 - "apply_condition"
Cohesion: 0.13
Nodes (11): _apply_condition_riders(), apply_condition(), _as_condition(), attempt_escapes(), _contar(), _label(), _log_line(), _queda_accion() (+3 more)

### Community 15 - "condition_parser.py"
Cohesion: 0.15
Nodes (6): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), normalize_ability()

### Community 16 - "CombatContext"
Cohesion: 0.07
Nodes (15): ActionType, AttackAction, CombatAction, CombatContext, _living_enemies(), _log(), WeaponAttackAction, _contexto_de_reaccion() (+7 more)

### Community 17 - "combat.py"
Cohesion: 0.19
Nodes (8): CombatResult, _invoke_policy(), roll_initiative(), _run_combat(), pick(), _extract(), first_target_policy(), random_policy()

### Community 18 - "legendary.py"
Cohesion: 0.13
Nodes (10): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), legendary_resistance(), _log_line() (+2 more)

### Community 19 - "combatant.py"
Cohesion: 0.11
Nodes (4): CombatState, CombatantType, CombatState, Condition

### Community 20 - "test_multiattack.py"
Cohesion: 0.20
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 21 - "run_combat"
Cohesion: 0.25
Nodes (11): run_combat(), _summarize_damage(), _eventos(), _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(), test_dos_combates_seguidos_empiezan_con_el_aliento_cargado(), test_dragon_nunca_usa_el_aliento_dos_turnos_seguidos_sin_recarga() (+3 more)

### Community 22 - "ConditionTracker"
Cohesion: 0.12
Nodes (4): ConditionTracker, ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 23 - "json"
Cohesion: 0.17
Nodes (5): _cache_path(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError

### Community 24 - "MultiattackAction"
Cohesion: 0.19
Nodes (3): MultiattackAction, _combate_terminado(), _equipos_vivos()

### Community 25 - "attack_roll"
Cohesion: 0.06
Nodes (43): Attack, ExtraDamage, _agrandado(), attack_roll(), _bonus_de_tamano(), _dados_de_ataque(), _mode_tag(), _reaccion_si_procede() (+35 more)

### Community 26 - "begin_turn"
Cohesion: 0.26
Nodes (16): EscapeCheck, begin_turn(), _ctx(), _pj(), test_con_dos_caracteristicas_se_elige_una_al_azar(), test_con_una_sola_caracteristica_no_consume_rng(), test_consumes_action_gasta_la_accion_del_turno(), test_dos_instancias_consumes_action_solo_intenta_la_primera() (+8 more)

### Community 27 - "test_spells.py"
Cohesion: 0.23
Nodes (10): build_spell_actions(), _desde_fixture(), _monstruo_lanzador(), test_el_lich_carga_su_cantrip_utile(), test_gastar_un_slot_no_afecta_a_los_otros_niveles(), test_la_reaccion_gasta_el_slot_de_su_nivel(), test_los_hechizos_de_nivel_1_consumen_slots(), test_max_spell_level_limita_el_nivel_cargado() (+2 more)

### Community 28 - "Spellcasting"
Cohesion: 0.19
Nodes (7): parse_spellcasting(), Spellcasting, test_el_lanzador_se_lee_de_los_special_abilities(), test_el_upcast_reescala_el_dano_y_la_curacion(), test_initialize_slots_usa_la_tabla_real_de_un_lanzador_completo(), test_la_curacion_usa_el_modificador_de_caracteristica_no_el_bono_completo(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 29 - "PlayerCharacter"
Cohesion: 0.23
Nodes (8): PlayerCharacter, simulate(), _guerrero_y_ogro(), test_danio_medio_por_combatiente_y_equipo(), test_immune_target_takes_zero_damage(), test_informe_final_con_apartados_de_pj_y_monstruros(), test_regression_guerrero_vs_ogro(), test_regression_guerrero_vs_owlbear()

### Community 30 - "parse_spell"
Cohesion: 0.19
Nodes (20): parse_spell(), _spell_data(), _spellcasting(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_proyectil_magico_es_dano_automatico(), test_el_tiempo_de_casteo_marca_el_tipo_de_accion(), test_las_ilusiones_sin_estado_en_el_rival_se_ignoran() (+12 more)

### Community 31 - "test_damage.py"
Cohesion: 0.27
Nodes (10): apply_damage_modifiers(), _is_petrified(), _target(), test_immunity_zero(), test_invalid_damage_type_raises(), test_no_modifiers_unchanged(), test_resistance_halves_damage_floor(), test_resistance_then_vulnerability_same_type() (+2 more)

### Community 32 - "spell_action"
Cohesion: 0.14
Nodes (8): dado_por_nivel(), duracion_en_rondas(), Spell, spell_action(), SpellAttackAction, test_un_ataque_de_hechizo_de_nivel_2_se_interpreta_desde_el_texto(), test_un_cantrip_con_varios_elementos_hace_un_ataque_por_elemento(), test_un_hechizo_de_accion_bonus_se_comprueba_en_su_fase()

### Community 33 - "test_checks_escapes.py"
Cohesion: 0.11
Nodes (22): parse_escape(), _ataque(), _data(), _duelo(), _load(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_el_estado_cambia_ataque_a_ataque_en_un_multiataque() (+14 more)

### Community 34 - "loader.py"
Cohesion: 0.10
Nodes (9): AttackEntry, _damage_type(), _extract_multiattack_alternatives(), _simple_damage_modifiers(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack() (+1 more)

### Community 35 - "parse_usage"
Cohesion: 0.24
Nodes (5): parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 36 - "ability_check"
Cohesion: 0.12
Nodes (10): ability_check(), ability_check_bonus(), _guia(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_probabilidad_de_liberarse_con_cd_12(), test_prueba_con_envenenado_o_aterrorizado_da_desventaja(), test_prueba_con_ventaja_da_75_por_ciento(), test_prueba_de_caracteristica_con_bonus_0_da_50_por_ciento() (+2 more)

### Community 39 - "CheckResult"
Cohesion: 0.50
Nodes (3): CheckResult, _check_fijo(), _fake()

### Community 41 - "dnd_sim/__init__.py"
Cohesion: 0.16
Nodes (6): ability_mod(), d20(), D20Result, roll_d20(), roll_dice(), HealEffect

### Community 42 - "TurnResources"
Cohesion: 0.18
Nodes (5): TurnResources, _breath(), _FixedRandom, test_begin_turn_no_tira_nada_si_estan_cargadas(), test_begin_turn_reinicia_recursos_y_tira_una_recarga_por_accion()

### Community 43 - "AttackRange"
Cohesion: 0.14
Nodes (6): _actualizar_distancia(), AttackRange, effective_ac(), resolve_attack_range(), test_melee_or_ranged_consume_rng_siempre(), test_melee_or_ranged_elige_uno_de_los_dos_modos()

### Community 44 - "legendary_parser.py"
Cohesion: 0.06
Nodes (23): SaveAction, AreaSaveAction, is_area_action(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision() (+15 more)

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `load_monster` to `test_attach.py`, `test_legendary.py`, `Condition`, `_pj`, `main.py`, `test_invisibility.py`, `test_conditions.py`, `test_loader_actions.py`, `condition_parser.py`, `CombatContext`, `combatant.py`, `test_multiattack.py`, `run_combat`, `json`, `MultiattackAction`, `attack_roll`, `test_spells.py`, `PlayerCharacter`, `test_damage.py`, `test_checks_escapes.py`, `loader.py`, `parse_usage`, `dnd_sim/__init__.py`, `legendary_parser.py`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `ActionType` and `UnknownUsageError`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05760905760905761 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `test_legendary.py`, `spell_parser.py`, `_pj`, `test_invisibility.py`, `test_conditions.py`, `apply_condition`, `condition_parser.py`, `CombatContext`, `combat.py`, `combatant.py`, `ConditionTracker`, `attack_roll`, `test_spells.py`, `parse_spell`, `test_damage.py`, `test_checks_escapes.py`, `loader.py`, `ability_check`, `dnd_sim/__init__.py`, `AttackRange`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `attack_roll()` (e.g. with `Attack` and `Combatant`) actually correct?**
  _`attack_roll()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_legendary.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07006151742993848 - nodes in this community are weakly interconnected._
- **Why does `attack_roll()` connect `attack_roll` to `test_attach.py`, `test_checks_escapes.py`, `test_legendary.py`, `saves.py`, `Condition`, `dnd_sim/__init__.py`, `_pj`, `AttackRange`, `test_invisibility.py`, `test_conditions.py`, `apply_condition`, `legendary_parser.py`, `CombatContext`, `combat.py`, `MultiattackAction`, `test_spells.py`, `test_damage.py`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
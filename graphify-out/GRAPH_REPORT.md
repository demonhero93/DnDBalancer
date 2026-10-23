# Graph Report - DnDBalancer  (2026-10-23)

## Corpus Check
- 116 files · ~69,181 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 1236 nodes · 4325 edges · 48 communities (42 shown, 6 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 319 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `af5c4e08`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- area.py
- test_attach.py
- test_legendary.py
- UsageKind
- saves.py
- test_enlarge.py
- spell_parser.py
- load_monster
- _pj
- main.py
- Condition
- test_conditions.py
- test_loader_actions.py
- actions.py
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
- spell_action
- Attack
- parse_spell
- test_damage.py
- save_builder.py
- test_checks_escapes.py
- loader.py
- parse_usage
- _pj
- DamageRecorder
- test_extra_damage.py
- DamageType
- escape_parser.py
- dnd_sim/__init__.py
- TurnResources
- roll_modifiers.py
- legendary_parser.py
- AttackRange
- trigger_reaction
- simulate

## God Nodes (most connected - your core abstractions)
1. `apply_condition()` - 95 edges
2. `load_monster()` - 86 edges
3. `attack_roll()` - 79 edges
4. `Condition` - 77 edges
5. `CombatContext` - 61 edges
6. `Attack` - 56 edges
7. `parse_spell()` - 56 edges
8. `Abilities` - 53 edges
9. `run_combat()` - 52 edges
10. `AttackRange` - 51 edges

## Surprising Connections (you probably didn't know these)
- `_build_party()` --uses--> `Abilities`  [INFERRED]
  main.py → dnd_sim/abilities.py
- `_area_action()` --uses--> `ActionType`  [INFERRED]
  tests/test_area.py → dnd_sim/actions.py
- `test_el_desenganche_es_una_prueba_de_fuerza_cd_16_que_gasta_la_accion()` --uses--> `ActionType`  [INFERRED]
  tests/test_attach.py → dnd_sim/actions.py
- `test_sin_accion_disponible_no_intenta_desengancharse()` --uses--> `ActionType`  [INFERRED]
  tests/test_attach.py → dnd_sim/actions.py
- `test_consumes_action_gasta_la_accion_del_turno()` --uses--> `ActionType`  [INFERRED]
  tests/test_checks_escapes.py → dnd_sim/actions.py

## Import Cycles
- None detected.

## Communities (48 total, 6 thin omitted)

### Community 0 - "area.py"
Cohesion: 0.17
Nodes (4): AreaSaveAction, _log_line(), pick(), sample()

### Community 1 - "test_attach.py"
Cohesion: 0.05
Nodes (37): Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _log_line(), _ya_cegado_por(), inflict_damage() (+29 more)

### Community 2 - "test_legendary.py"
Cohesion: 0.06
Nodes (64): ConditionEffect, legendary_phase(), LegendaryAction, saving_throw(), test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _contexto(), _data(), _estado() (+56 more)

### Community 3 - "UsageKind"
Cohesion: 0.17
Nodes (10): UsageKind, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar(), test_per_day_dos_usos_y_luego_can_use_falso(), test_per_day_no_tira_recarga(), test_per_day_reset_restaura_todos_los_usos(), test_recharge_5_6_porcentaje_de_exito(), test_recharge_mientras_esta_cargada_no_consume_rng() (+2 more)

### Community 4 - "saves.py"
Cohesion: 0.06
Nodes (45): ability_mod(), _log_target(), AreaTargeting, select_area_targets(), _default_targeting(), _contar_accion(), _contar_puntos(), _contar_resistencia() (+37 more)

### Community 5 - "test_enlarge.py"
Cohesion: 0.20
Nodes (19): _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj(), _spy_roll_dice() (+11 more)

### Community 6 - "spell_parser.py"
Cohesion: 0.06
Nodes (15): _afecta_movimiento(), _condicion_con_salvacion(), _crea_objetos(), _dados_de_dano(), _dc_ability(), _elementos_totales(), _es_ilusion(), _numero_elementos() (+7 more)

### Community 8 - "load_monster"
Cohesion: 0.13
Nodes (14): _armor_class_value(), load_monster(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper(), test_cache_avoids_second_network() (+6 more)

### Community 9 - "_pj"
Cohesion: 0.18
Nodes (15): apply_concentration(), _ctx(), _npc(), _pj(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado(), test_el_hechizo_verdadero_da_ventaja_en_los_ataques(), test_la_curacion_solo_se_lanza_contra_un_aliado_herido() (+7 more)

### Community 10 - "main.py"
Cohesion: 0.31
Nodes (3): build_parser(), _load_party(), _parse_monster_token()

### Community 11 - "Condition"
Cohesion: 0.07
Nodes (49): Condition, Condition, parse_traits(), RollMode, attack_modifiers(), AttackModifiers, CheckModifiers, SaveModifiers (+41 more)

### Community 12 - "test_conditions.py"
Cohesion: 0.06
Nodes (64): Abilities, _apply_condition_riders(), Monster, apply_condition(), _as_condition(), end_turn(), _label(), _log_line() (+56 more)

### Community 13 - "test_loader_actions.py"
Cohesion: 0.18
Nodes (13): _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga(), test_ataque_con_usage_conserva_el_actionusage() (+5 more)

### Community 14 - "actions.py"
Cohesion: 0.11
Nodes (8): ActionType, AttackAction, CombatAction, SaveAction, ConditionAction, _queda_accion(), SpellAction, ActionUsage

### Community 15 - "condition_parser.py"
Cohesion: 0.16
Nodes (6): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), normalize_ability()

### Community 16 - "CombatContext"
Cohesion: 0.09
Nodes (10): CombatContext, _living_enemies(), _log(), HealAction, _romper_invisibilidad_al_lanzar(), SpellAttackAction, SpellFixedDamageAction, SpellStateAction (+2 more)

### Community 17 - "combat.py"
Cohesion: 0.11
Nodes (14): _agrandado(), _bonus_de_tamano(), CombatResult, _dados_de_ataque(), _invoke_policy(), _reaccion_si_procede(), resolve_roll_mode(), roll_initiative() (+6 more)

### Community 18 - "legendary.py"
Cohesion: 0.11
Nodes (7): _accion_utilizable(), _acciones_asequibles(), _combate_terminado(), _contexto_de(), _equipos_vivos(), LegendaryState, _presupuesto()

### Community 19 - "combatant.py"
Cohesion: 0.10
Nodes (5): WeaponAttackAction, CombatState, Combatant, CombatState, normalize_ability()

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
Cohesion: 0.18
Nodes (5): _cache_path(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError

### Community 25 - "attack_roll"
Cohesion: 0.19
Nodes (17): _actualizar_distancia(), attack_roll(), _mode_tag(), HeatedBody, _ataque_melee(), _ataque_ranged(), _azer(), _ctx() (+9 more)

### Community 26 - "begin_turn"
Cohesion: 0.14
Nodes (18): attempt_escapes(), _contar(), EscapeCheck, begin_turn(), _log_line(), _check_fijo(), _ctx(), test_con_dos_caracteristicas_se_elige_una_al_azar() (+10 more)

### Community 27 - "test_spells.py"
Cohesion: 0.15
Nodes (16): build_spell_actions(), parse_spellcasting(), test_un_lanzador_carga_el_hechizo_con_su_pool_de_slots(), _desde_fixture(), _monstruo_lanzador(), test_el_lanzador_se_lee_de_los_special_abilities(), test_el_lich_carga_su_cantrip_utile(), test_gastar_un_slot_no_afecta_a_los_otros_niveles() (+8 more)

### Community 28 - "spell_action"
Cohesion: 0.16
Nodes (8): Spell, spell_action(), Spellcasting, _spell_data(), test_el_hechizo_enlarge_es_un_estado_self(), test_lanzar_el_hechizo_agranda_al_lanzador(), test_el_upcast_reescala_el_dano_y_la_curacion(), test_un_hechizo_de_accion_bonus_se_comprueba_en_su_fase()

### Community 29 - "Attack"
Cohesion: 0.16
Nodes (9): Attack, PlayerCharacter, _build_party(), test_attack_roll_log_modifier(), test_immune_target_takes_zero_damage(), test_regression_guerrero_vs_ogro(), test_regression_guerrero_vs_owlbear(), test_strings_are_converted() (+1 more)

### Community 30 - "parse_spell"
Cohesion: 0.16
Nodes (21): parse_spell(), _spell_data(), _spellcasting(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_proyectil_magico_es_dano_automatico(), test_el_tiempo_de_casteo_marca_el_tipo_de_accion(), test_las_ilusiones_sin_estado_en_el_rival_se_ignoran() (+13 more)

### Community 31 - "test_damage.py"
Cohesion: 0.31
Nodes (12): apply_damage_modifiers(), print_report(), _guerrero_y_ogro(), _target(), test_danio_medio_por_combatiente_y_equipo(), test_immunity_zero(), test_informe_final_con_apartados_de_pj_y_monstruros(), test_invalid_damage_type_raises() (+4 more)

### Community 32 - "save_builder.py"
Cohesion: 0.12
Nodes (8): is_area_action(), _damage_type(), build_condition_action(), build_save_action(), build_save_effect(), damage_dice_of(), damage_options(), damage_type_of()

### Community 33 - "test_checks_escapes.py"
Cohesion: 0.19
Nodes (12): parse_escape(), _data(), _load(), test_el_escape_se_intenta_al_inicio_del_turno(), test_el_estado_cambia_ataque_a_ataque_en_un_multiataque(), test_el_fixture_de_la_constriccion_tiene_escape_y_avisa_de_grappled(), test_el_fixture_de_la_telaraña_carga_restrained_con_escape(), test_en_un_combate_la_telaraña_inmoviliza_y_el_pj_intenta_escapar() (+4 more)

### Community 34 - "loader.py"
Cohesion: 0.09
Nodes (11): AttackEntry, parse_attach_effects(), _extract_multiattack_alternatives(), _norm_name(), _simple_damage_modifiers(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada() (+3 more)

### Community 35 - "parse_usage"
Cohesion: 0.24
Nodes (5): parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 36 - "_pj"
Cohesion: 0.10
Nodes (16): ability_check(), ability_check_bonus(), CheckResult, _guia(), _fake(), _pj(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_el_escape_con_ventaja_condicionada_por_envenenamiento() (+8 more)

### Community 38 - "test_extra_damage.py"
Cohesion: 0.27
Nodes (15): _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional(), test_ataque_sin_extra_no_llama_al_bucle() (+7 more)

### Community 39 - "DamageType"
Cohesion: 0.18
Nodes (4): ExtraDamage, DamageType, _is_petrified(), parse_damage_type()

### Community 41 - "dnd_sim/__init__.py"
Cohesion: 0.21
Nodes (5): d20(), D20Result, roll_d20(), roll_dice(), HealEffect

### Community 42 - "TurnResources"
Cohesion: 0.18
Nodes (5): TurnResources, _breath(), _FixedRandom, test_begin_turn_no_tira_nada_si_estan_cargadas(), test_begin_turn_reinicia_recursos_y_tira_una_recarga_por_accion()

### Community 43 - "roll_modifiers.py"
Cohesion: 0.17
Nodes (6): check_modifiers(), _condiciones(), effective_ac(), save_modifiers(), test_la_ca_efectiva_sube_dos_a_distancia(), test_los_flags_de_prueba_son_por_caracteristica()

### Community 44 - "legendary_parser.py"
Cohesion: 0.10
Nodes (14): parse_range_type(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary() (+6 more)

### Community 45 - "AttackRange"
Cohesion: 0.24
Nodes (9): AttackRange, resolve_attack_range(), _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo() (+1 more)

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `load_monster` to `test_attach.py`, `test_legendary.py`, `saves.py`, `test_enlarge.py`, `spell_parser.py`, `_pj`, `main.py`, `Condition`, `test_conditions.py`, `test_loader_actions.py`, `actions.py`, `condition_parser.py`, `CombatContext`, `combat.py`, `test_multiattack.py`, `run_combat`, `json`, `MultiattackAction`, `attack_roll`, `test_spells.py`, `Attack`, `test_damage.py`, `save_builder.py`, `test_checks_escapes.py`, `loader.py`, `parse_usage`, `test_extra_damage.py`, `DamageType`, `dnd_sim/__init__.py`, `legendary_parser.py`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `ActionType` and `UnknownUsageError`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05493827160493827 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `test_legendary.py`, `test_enlarge.py`, `spell_parser.py`, `_pj`, `test_conditions.py`, `actions.py`, `condition_parser.py`, `CombatContext`, `combat.py`, `combatant.py`, `ConditionTracker`, `attack_roll`, `test_spells.py`, `spell_action`, `parse_spell`, `test_checks_escapes.py`, `loader.py`, `_pj`, `DamageType`, `dnd_sim/__init__.py`, `roll_modifiers.py`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `attack_roll()` (e.g. with `Attack` and `Combatant`) actually correct?**
  _`attack_roll()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_legendary.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06106442577030812 - nodes in this community are weakly interconnected._
- **Why does `attack_roll()` connect `attack_roll` to `test_attach.py`, `test_legendary.py`, `saves.py`, `test_enlarge.py`, `_pj`, `Condition`, `test_conditions.py`, `actions.py`, `CombatContext`, `combat.py`, `combatant.py`, `MultiattackAction`, `test_spells.py`, `Attack`, `test_damage.py`, `test_checks_escapes.py`, `test_extra_damage.py`, `dnd_sim/__init__.py`, `roll_modifiers.py`, `AttackRange`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
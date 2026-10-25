# Graph Report - DnDBalancer  (2026-10-25)

## Corpus Check
- 123 files · ~77,280 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 1386 nodes · 4883 edges · 58 communities (53 shown, 5 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 358 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a1a436e2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- saves.py
- test_attach.py
- load_monster
- usage.py
- test_area.py
- test_enlarge.py
- parse_spell
- test_loader.py
- _pj
- test_traits.py
- Condition
- test_conditions.py
- test_loader_actions.py
- actions.py
- spell_parser.py
- CombatContext
- combat.py
- LegendaryState
- combatant.py
- test_legendary.py
- attach.py
- ConditionTracker
- area.py
- MultiattackAction
- Trait
- test_checks_escapes.py
- test_spells.py
- _ctx
- RollMode
- spell_action
- PlayerCharacter
- apply_condition
- run_combat
- multiattack_parser.py
- warnings
- ability_check
- test_pack_tactics.py
- attack_roll
- test_multiattack.py
- test_los_hechizos_de_nivel_1_consumen_slots
- dnd_sim/__init__.py
- test_martial_advantage.py
- roll_modifiers.py
- legendary_parser.py
- conditions.py
- traits.py
- begin_turn
- Combatant
- Abilities
- AttackRange
- inflict_damage
- apply_damage_modifiers
- TurnResources
- parse_traits
- SpellFixedDamageAction
- escape_parser.py
- test_un_cantrip_se_puede_lanzar_en_cada_turno

## God Nodes (most connected - your core abstractions)
1. `apply_condition()` - 101 edges
2. `load_monster()` - 94 edges
3. `attack_roll()` - 87 edges
4. `Condition` - 83 edges
5. `CombatContext` - 69 edges
6. `AttackRange` - 63 edges
7. `Abilities` - 62 edges
8. `Attack` - 61 edges
9. `run_combat()` - 58 edges
10. `parse_spell()` - 56 edges

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

## Communities (58 total, 5 thin omitted)

### Community 0 - "saves.py"
Cohesion: 0.10
Nodes (17): _log_target(), _contar_resistencia(), legendary_resistance(), registrar_resistencia_legendaria(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save() (+9 more)

### Community 1 - "test_attach.py"
Cohesion: 0.18
Nodes (25): _atacar(), _bite(), _cloaker(), _ctx(), _datos(), _pj(), test_con_ventaja_el_enganche_es_a_la_cabeza_y_ciega(), test_damage_transfer_no_aplica_sin_enganche() (+17 more)

### Community 2 - "load_monster"
Cohesion: 0.10
Nodes (13): _damage_type(), _extract_multiattack_alternatives(), load_monster(), _norm_name(), _simple_damage_modifiers(), build_condition_action(), build_save_effect(), damage_dice_of() (+5 more)

### Community 3 - "usage.py"
Cohesion: 0.11
Nodes (11): UsageKind, _FixedRandom, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar(), test_per_day_dos_usos_y_luego_can_use_falso(), test_per_day_no_tira_recarga(), test_per_day_reset_restaura_todos_los_usos(), test_recharge_5_6_porcentaje_de_exito() (+3 more)

### Community 4 - "test_area.py"
Cohesion: 0.19
Nodes (22): AreaTargeting, select_area_targets(), _default_targeting(), _area_action(), _ctx(), _npc(), _pj(), _save_forzado() (+14 more)

### Community 5 - "test_enlarge.py"
Cohesion: 0.15
Nodes (24): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+16 more)

### Community 6 - "parse_spell"
Cohesion: 0.09
Nodes (11): _afecta_movimiento(), _crea_objetos(), _dados_de_dano(), _elementos_totales(), _es_ilusion(), _numero_elementos(), _opciones_de_dano(), parse_spell() (+3 more)

### Community 8 - "test_loader.py"
Cohesion: 0.06
Nodes (25): _cache_path(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError, _armor_class_value(), save_modifiers(), _load_fixture() (+17 more)

### Community 9 - "_pj"
Cohesion: 0.18
Nodes (16): apply_concentration(), _ctx(), _npc(), _pj(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizado_invierte_los_objetivos_de_ataque(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado() (+8 more)

### Community 10 - "test_traits.py"
Cohesion: 0.12
Nodes (23): attack_modifiers(), _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _RasgoDeSalvacion, _sahuagin() (+15 more)

### Community 11 - "Condition"
Cohesion: 0.21
Nodes (25): Condition, _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj(), test_atacar_a_un_invisible_tiene_desventaja() (+17 more)

### Community 12 - "test_conditions.py"
Cohesion: 0.12
Nodes (28): end_turn(), _data(), _load(), _pj(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente(), test_can_act_y_can_react(), test_condicion_fuera_del_enum_lanza_value_error(), test_dos_instancias_de_la_misma_condicion_de_fuentes_distintas() (+20 more)

### Community 13 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (14): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+6 more)

### Community 14 - "actions.py"
Cohesion: 0.08
Nodes (15): ActionType, AttackAction, CombatAction, SaveAction, WeaponAttackAction, AreaSaveAction, ConditionAction, SaveDamage (+7 more)

### Community 15 - "spell_parser.py"
Cohesion: 0.09
Nodes (11): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), _condicion_con_salvacion(), _dc_ability(), _warn() (+3 more)

### Community 16 - "CombatContext"
Cohesion: 0.09
Nodes (9): CombatContext, _living_enemies(), _log(), _equipos_vivos(), _contexto_de_reaccion(), _romper_invisibilidad_al_lanzar(), trigger_reaction(), _objetivo_enganche() (+1 more)

### Community 17 - "combat.py"
Cohesion: 0.25
Nodes (7): CombatResult, _invoke_policy(), roll_initiative(), _run_combat(), _extract(), first_target_policy(), random_policy()

### Community 18 - "LegendaryState"
Cohesion: 0.13
Nodes (5): _accion_utilizable(), _acciones_asequibles(), LegendaryAction, LegendaryState, _presupuesto()

### Community 19 - "combatant.py"
Cohesion: 0.13
Nodes (5): ability_mod(), CombatState, CombatantType, CombatState, Condition

### Community 20 - "test_legendary.py"
Cohesion: 0.06
Nodes (65): _apply_condition_riders(), ConditionEffect, RepeatSave, _combate_terminado(), legendary_phase(), saving_throw(), test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _contexto() (+57 more)

### Community 21 - "attach.py"
Cohesion: 0.13
Nodes (7): Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), parse_attach_effects()

### Community 22 - "ConditionTracker"
Cohesion: 0.12
Nodes (4): ConditionTracker, ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 23 - "area.py"
Cohesion: 0.11
Nodes (6): _contar_accion(), _contar_puntos(), _contexto_de(), log_line(), pick(), sample()

### Community 25 - "Trait"
Cohesion: 0.06
Nodes (9): BloodFrenzy, DamageTransfer, hooks(), Regeneration, Trait, TurnResistance, test_el_catalogo_cubre_hooks_que_los_rasgos_aun_no_usan(), test_hooks_con_un_nombre_fuera_del_catalogo_lanza_error() (+1 more)

### Community 26 - "test_checks_escapes.py"
Cohesion: 0.17
Nodes (16): parse_escape(), _data(), _load(), _pj(), test_el_escape_se_intenta_al_inicio_del_turno(), test_el_estado_cambia_ataque_a_ataque_en_un_multiataque(), test_el_estado_de_distancia_inicial_y_el_reset(), test_el_fixture_de_la_constriccion_tiene_escape_y_avisa_de_grappled() (+8 more)

### Community 27 - "test_spells.py"
Cohesion: 0.16
Nodes (14): parse_spellcasting(), Spellcasting, _desde_fixture(), _monstruo_lanzador(), test_el_lanzador_se_lee_de_los_special_abilities(), test_el_upcast_reescala_el_dano_y_la_curacion(), test_gastar_un_slot_no_afecta_a_los_otros_niveles(), test_initialize_slots_usa_la_tabla_real_de_un_lanzador_completo() (+6 more)

### Community 28 - "_ctx"
Cohesion: 0.18
Nodes (18): _ataque(), _ctx(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja(), test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_las_condiciones_incapacitantes_fallan_fue_y_des_sin_tirar_dados() (+10 more)

### Community 29 - "RollMode"
Cohesion: 0.16
Nodes (4): RollMode, AttackModifiers, SaveModifiers, test_el_tipo_de_efecto_kind_llega_a_los_rasgos()

### Community 30 - "spell_action"
Cohesion: 0.13
Nodes (22): spell_action(), test_el_hechizo_enlarge_es_un_estado_self(), _spell_data(), _spellcasting(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_lich_carga_su_cantrip_utile(), test_el_tiempo_de_casteo_marca_el_tipo_de_accion() (+14 more)

### Community 31 - "PlayerCharacter"
Cohesion: 0.11
Nodes (18): _tag_modificadores(), PlayerCharacter, print_report(), simulate(), build_parser(), _build_party(), _load_party(), main() (+10 more)

### Community 32 - "apply_condition"
Cohesion: 0.19
Nodes (15): apply_condition(), EscapeCheck, _check_fijo(), _ctx(), test_consumes_action_gasta_la_accion_del_turno(), test_dos_instancias_consumes_action_solo_intenta_la_primera(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_el_escape_con_ventaja_condicionada_por_envenenamiento() (+7 more)

### Community 33 - "run_combat"
Cohesion: 0.22
Nodes (12): run_combat(), _summarize_damage(), _eventos(), _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(), test_copias_de_un_monstruo_tienen_estado_independiente(), test_dos_combates_seguidos_empiezan_con_el_aliento_cargado() (+4 more)

### Community 34 - "multiattack_parser.py"
Cohesion: 0.21
Nodes (5): AttackEntry, extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 35 - "warnings"
Cohesion: 0.21
Nodes (6): _resistencia_legendaria(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 36 - "ability_check"
Cohesion: 0.14
Nodes (9): ability_check(), ability_check_bonus(), CheckResult, _guia(), _fake(), test_prueba_con_ventaja_da_75_por_ciento(), test_prueba_de_caracteristica_con_bonus_0_da_50_por_ciento(), test_sin_autoexito_ni_autofallo_en_pruebas() (+1 more)

### Community 37 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 38 - "attack_roll"
Cohesion: 0.06
Nodes (51): Attack, ExtraDamage, _actualizar_distancia(), _agrandado(), attack_roll(), _bonus_de_rasgos(), _bonus_de_tamano(), _dados_de_ataque() (+43 more)

### Community 39 - "test_multiattack.py"
Cohesion: 0.20
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 41 - "dnd_sim/__init__.py"
Cohesion: 0.24
Nodes (4): d20(), D20Result, roll_d20(), roll_dice()

### Community 42 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 43 - "roll_modifiers.py"
Cohesion: 0.13
Nodes (7): check_modifiers(), CheckModifiers, _condiciones(), effective_ac(), _hooks(), test_la_ca_efectiva_sube_dos_a_distancia(), test_los_flags_de_prueba_son_por_caracteristica()

### Community 44 - "legendary_parser.py"
Cohesion: 0.09
Nodes (14): parse_range_type(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary() (+6 more)

### Community 45 - "conditions.py"
Cohesion: 0.17
Nodes (9): _as_condition(), attempt_escapes(), _contar(), _label(), _queda_accion(), remove_condition(), test_con_dos_caracteristicas_se_elige_una_al_azar(), test_con_una_sola_caracteristica_no_consume_rng() (+1 more)

### Community 46 - "traits.py"
Cohesion: 0.14
Nodes (4): aliados_capaces(), _condicion_posicional(), MartialAdvantage, PackTactics

### Community 47 - "begin_turn"
Cohesion: 0.30
Nodes (14): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_carga_su_regeneracion() (+6 more)

### Community 48 - "Combatant"
Cohesion: 0.15
Nodes (3): resolve_roll_mode(), Combatant, normalize_ability()

### Community 49 - "Abilities"
Cohesion: 0.22
Nodes (12): Abilities, Monster, test_dos_combates_seguidos_empiezan_sin_condiciones(), test_inmovilizado_da_desventaja_solo_en_des(), test_la_politica_no_se_invoca_para_un_incapacitado(), test_las_condiciones_incapacitantes_no_fallan_automaticamente_la_con(), test_petrificado_tiene_resistencia_a_todo(), test_sin_condiciones_el_dano_no_cambia() (+4 more)

### Community 50 - "AttackRange"
Cohesion: 0.25
Nodes (10): AttackRange, resolve_attack_range(), _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo() (+2 more)

### Community 51 - "inflict_damage"
Cohesion: 0.25
Nodes (3): _hooks(), inflict_damage(), _notify_damage_taken()

### Community 52 - "apply_damage_modifiers"
Cohesion: 0.36
Nodes (8): apply_damage_modifiers(), _target(), test_immunity_zero(), test_invalid_damage_type_raises(), test_no_modifiers_unchanged(), test_resistance_halves_damage_floor(), test_resistance_then_vulnerability_same_type(), test_vulnerability_doubles_damage()

### Community 53 - "TurnResources"
Cohesion: 0.32
Nodes (4): TurnResources, _breath(), test_begin_turn_no_tira_nada_si_estan_cargadas(), test_begin_turn_reinicia_recursos_y_tira_una_recarga_por_accion()

### Community 54 - "parse_traits"
Cohesion: 0.33
Nodes (3): parse_traits(), test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad(), test_parse_traits_ignora_entradas_malformadas()

### Community 55 - "SpellFixedDamageAction"
Cohesion: 0.40
Nodes (4): SpellFixedDamageAction, test_el_proyectil_magico_es_dano_automatico(), test_el_proyectil_magico_pasa_por_los_modificadores_de_dano(), lanzar()

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `load_monster` to `test_attach.py`, `test_enlarge.py`, `test_loader.py`, `test_traits.py`, `Condition`, `test_conditions.py`, `test_loader_actions.py`, `actions.py`, `spell_parser.py`, `combatant.py`, `test_legendary.py`, `attach.py`, `MultiattackAction`, `test_checks_escapes.py`, `test_spells.py`, `spell_action`, `PlayerCharacter`, `run_combat`, `multiattack_parser.py`, `warnings`, `test_pack_tactics.py`, `attack_roll`, `test_multiattack.py`, `test_los_hechizos_de_nivel_1_consumen_slots`, `dnd_sim/__init__.py`, `test_martial_advantage.py`, `legendary_parser.py`, `begin_turn`, `Abilities`, `parse_traits`, `test_un_cantrip_se_puede_lanzar_en_cada_turno`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `ActionType` and `UnknownUsageError`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `saves.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09915966386554621 - nodes in this community are weakly interconnected._
- **Why does `CombatContext` connect `CombatContext` to `saves.py`, `test_attach.py`, `usage.py`, `test_area.py`, `test_enlarge.py`, `_pj`, `test_traits.py`, `Condition`, `test_conditions.py`, `actions.py`, `combat.py`, `test_legendary.py`, `area.py`, `MultiattackAction`, `test_checks_escapes.py`, `test_spells.py`, `_ctx`, `apply_condition`, `run_combat`, `test_pack_tactics.py`, `attack_roll`, `dnd_sim/__init__.py`, `test_martial_advantage.py`, `begin_turn`, `TurnResources`, `SpellFixedDamageAction`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `attack_roll()` (e.g. with `Attack` and `Combatant`) actually correct?**
  _`attack_roll()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `load_monster` be split into smaller, more focused modules?**
  _Cohesion score 0.09848484848484848 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `load_monster`, `test_enlarge.py`, `parse_spell`, `test_loader.py`, `_pj`, `test_traits.py`, `test_conditions.py`, `actions.py`, `spell_parser.py`, `CombatContext`, `combat.py`, `combatant.py`, `test_legendary.py`, `attach.py`, `ConditionTracker`, `test_checks_escapes.py`, `test_spells.py`, `spell_action`, `PlayerCharacter`, `ability_check`, `test_pack_tactics.py`, `attack_roll`, `dnd_sim/__init__.py`, `roll_modifiers.py`, `conditions.py`, `Combatant`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
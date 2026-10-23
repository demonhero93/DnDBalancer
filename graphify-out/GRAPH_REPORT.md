# Graph Report - DnDBalancer  (2026-10-23)

## Corpus Check
- 116 files · ~68,409 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 1225 nodes · 4257 edges · 50 communities (44 shown, 6 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 304 edges (avg confidence: 0.92)
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
- save_builder.py
- test_spells.py
- PlayerCharacter
- test_traits.py
- test_conditions.py
- legendary_phase
- apply_condition
- condition_parser.py
- CombatContext
- pick
- legendary.py
- combatant.py
- test_multiattack.py
- test_azer.py
- ConditionTracker
- _ctx
- traits.py
- test_extra_damage.py
- begin_turn
- build_spell_actions
- actions.py
- AttackRange
- _spell_data
- test_damage.py
- spell_action
- test_checks_escapes.py
- load_monster
- attack_roll
- ability_check
- damage.py
- AttackModifiers
- area.py
- combat.py
- dnd_sim/__init__.py
- ActionType
- roll_modifiers.py
- legendary_parser.py
- Abilities
- LegendaryState
- ConditionTracker
- ConditionAction
- ConditionEffect

## God Nodes (most connected - your core abstractions)
1. `apply_condition()` - 88 edges
2. `load_monster()` - 86 edges
3. `attack_roll()` - 77 edges
4. `Condition` - 69 edges
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

## Communities (50 total, 6 thin omitted)

### Community 0 - "test_area.py"
Cohesion: 0.25
Nodes (20): AreaTargeting, select_area_targets(), _default_targeting(), SaveDamage, _area_action(), _ctx(), _npc(), _pj() (+12 more)

### Community 1 - "test_attach.py"
Cohesion: 0.06
Nodes (34): AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _log_line(), _ya_cegado_por(), inflict_damage(), _notify_damage_dealt() (+26 more)

### Community 2 - "test_legendary.py"
Cohesion: 0.10
Nodes (28): saving_throw(), _data(), _estado(), _load(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_con_use_probability_uno_el_danio_es_mayor_que_con_cero(), test_el_ala_que_mezcla_movimiento_avisa() (+20 more)

### Community 3 - "run_combat"
Cohesion: 0.06
Nodes (41): run_combat(), _summarize_damage(), ActionUsage, UsageKind, _area_action(), _data(), _load(), _raw_action() (+33 more)

### Community 4 - "saves.py"
Cohesion: 0.12
Nodes (16): legendary_resistance(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save(), _log_line(), _mode_tag(), _outcome_tag() (+8 more)

### Community 5 - "Condition"
Cohesion: 0.11
Nodes (27): Condition, doblar_dados(), save_modifiers(), test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos() (+19 more)

### Community 6 - "parse_spell"
Cohesion: 0.07
Nodes (22): _afecta_movimiento(), _condicion_con_salvacion(), _crea_objetos(), _dados_de_dano(), _dc_ability(), _elementos_totales(), _es_ilusion(), _numero_elementos() (+14 more)

### Community 8 - "save_builder.py"
Cohesion: 0.12
Nodes (8): is_area_action(), _damage_type(), build_condition_action(), build_save_action(), build_save_effect(), damage_dice_of(), damage_options(), damage_type_of()

### Community 9 - "test_spells.py"
Cohesion: 0.24
Nodes (14): _ctx(), _npc(), _pj(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado(), test_el_hechizo_verdadero_da_ventaja_en_los_ataques(), test_la_curacion_solo_se_lanza_contra_un_aliado_herido() (+6 more)

### Community 10 - "PlayerCharacter"
Cohesion: 0.13
Nodes (14): PlayerCharacter, print_report(), simulate(), build_parser(), _build_party(), _load_party(), main(), _parse_monster_token() (+6 more)

### Community 11 - "test_traits.py"
Cohesion: 0.16
Nodes (20): parse_traits(), RollMode, attack_modifiers(), SaveModifiers, _ataque_melee(), _datos(), _pj(), _sahuagin() (+12 more)

### Community 12 - "test_conditions.py"
Cohesion: 0.16
Nodes (20): _data(), _load(), _pj(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente(), test_can_act_y_can_react(), test_condicion_fuera_del_enum_lanza_value_error(), test_el_ghoul_paraliza_con_diez_rondas_y_salvacion_de_repeticion(), test_el_hechizado_ahora_si_se_aplica() (+12 more)

### Community 13 - "legendary_phase"
Cohesion: 0.13
Nodes (27): legendary_phase(), _contexto(), _pj(), test_con_una_sola_accion_asequible_pick_no_consume_rng(), test_dos_duenos_legendarios_actuan_cada_uno_una_vez(), test_el_combate_termina_en_medio_de_la_fase(), test_el_dragon_contra_un_grupo_usa_acciones_legendarias(), test_la_fase_ocurre_despues_del_end_turn() (+19 more)

### Community 14 - "apply_condition"
Cohesion: 0.11
Nodes (20): _apply_condition_riders(), apply_condition(), _as_condition(), attempt_escapes(), _contar(), end_turn(), _label(), _log_line() (+12 more)

### Community 15 - "condition_parser.py"
Cohesion: 0.12
Nodes (8): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), has_escape_text(), parse_escape(), normalize_ability()

### Community 16 - "CombatContext"
Cohesion: 0.10
Nodes (20): CombatContext, _living_enemies(), _log(), HealAction, SpellStateAction, _accion(), _ataque(), _ctx() (+12 more)

### Community 17 - "pick"
Cohesion: 0.14
Nodes (10): CombatResult, roll_initiative(), _run_combat(), pick(), sample(), _extract(), first_target_policy(), random_policy() (+2 more)

### Community 18 - "legendary.py"
Cohesion: 0.10
Nodes (13): _accion_utilizable(), _acciones_asequibles(), _combate_terminado(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), _equipos_vivos() (+5 more)

### Community 19 - "combatant.py"
Cohesion: 0.09
Nodes (7): ability_mod(), WeaponAttackAction, CombatState, CombatantType, CombatState, Condition, normalize_ability()

### Community 20 - "test_multiattack.py"
Cohesion: 0.05
Nodes (29): MultiattackAction, _cache_path(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError, _armor_class_value(), _load_fixture() (+21 more)

### Community 21 - "test_azer.py"
Cohesion: 0.27
Nodes (14): HeatedBody, _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), test_ataque_a_distancia_no_dispara_la_represalia() (+6 more)

### Community 22 - "ConditionTracker"
Cohesion: 0.28
Nodes (3): ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 23 - "_ctx"
Cohesion: 0.18
Nodes (18): _ataque(), _ctx(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja(), test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_los_indicadores_estaticos_siguen_funcionando_y_se_combinan() (+10 more)

### Community 24 - "traits.py"
Cohesion: 0.22
Nodes (3): Attach, BloodFrenzy, Trait

### Community 25 - "test_extra_damage.py"
Cohesion: 0.26
Nodes (16): DamageType, _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional() (+8 more)

### Community 26 - "begin_turn"
Cohesion: 0.25
Nodes (4): begin_turn(), _log_line(), test_los_puntos_se_rellenan_al_inicio_del_turno_y_no_se_acumulan(), test_los_puntos_se_rellenan_evenco_el_dueno_est_a_incapacitado()

### Community 27 - "build_spell_actions"
Cohesion: 0.39
Nodes (7): build_spell_actions(), _desde_fixture(), _monstruo_lanzador(), test_gastar_un_slot_no_afecta_a_los_otros_niveles(), test_la_reaccion_gasta_el_slot_de_su_nivel(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_un_pool_por_nivel()

### Community 28 - "actions.py"
Cohesion: 0.15
Nodes (5): AttackAction, CombatAction, SaveAction, _objetivo_enganche(), valid_targets()

### Community 29 - "AttackRange"
Cohesion: 0.27
Nodes (9): AttackRange, resolve_attack_range(), _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo() (+1 more)

### Community 30 - "_spell_data"
Cohesion: 0.13
Nodes (17): _spell_data(), _spellcasting(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_lich_carga_su_cantrip_utile(), test_el_tiempo_de_casteo_marca_el_tipo_de_accion(), test_las_ilusiones_sin_estado_en_el_rival_se_ignoran(), test_los_hechizos_de_movimiento_se_ignoran() (+9 more)

### Community 31 - "test_damage.py"
Cohesion: 0.40
Nodes (9): apply_damage_modifiers(), _target(), test_immunity_zero(), test_invalid_damage_type_raises(), test_no_modifiers_unchanged(), test_resistance_halves_damage_floor(), test_resistance_then_vulnerability_same_type(), test_strings_are_converted() (+1 more)

### Community 32 - "spell_action"
Cohesion: 0.14
Nodes (9): dado_por_nivel(), spell_action(), SpellAttackAction, SpellFixedDamageAction, test_el_proyectil_magico_es_dano_automatico(), test_los_cantrips_no_gastan_usos_ni_slots(), test_un_ataque_de_hechizo_de_nivel_2_se_interpreta_desde_el_texto(), test_un_cantrip_con_salvacion_usa_la_cd_del_lanzador() (+1 more)

### Community 33 - "test_checks_escapes.py"
Cohesion: 0.12
Nodes (32): EscapeCheck, _ctx(), _data(), _load(), _pj(), test_consumes_action_gasta_la_accion_del_turno(), test_dos_instancias_consumes_action_solo_intenta_la_primera(), test_dos_ventajas_y_una_desventaja_se_anulan() (+24 more)

### Community 34 - "load_monster"
Cohesion: 0.09
Nodes (12): AttackEntry, parse_attach_effects(), parse_range_type(), _extract_multiattack_alternatives(), load_monster(), _norm_name(), _simple_damage_modifiers(), extract_multiattack_alternatives() (+4 more)

### Community 35 - "attack_roll"
Cohesion: 0.19
Nodes (5): Attack, attack_roll(), Combatant, test_extra_damage_estructura_por_defecto_vacia(), test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio()

### Community 36 - "ability_check"
Cohesion: 0.13
Nodes (8): ability_check(), ability_check_bonus(), CheckResult, _guia(), _check_fijo(), _fake(), test_probabilidad_de_liberarse_con_cd_12(), test_sin_autoexito_ni_autofallo_en_pruebas()

### Community 37 - "damage.py"
Cohesion: 0.12
Nodes (4): ExtraDamage, DamageRecorder, _is_petrified(), parse_damage_type()

### Community 39 - "area.py"
Cohesion: 0.24
Nodes (3): AreaSaveAction, _log_target(), _log_line()

### Community 40 - "combat.py"
Cohesion: 0.13
Nodes (9): _actualizar_distancia(), _agrandado(), _bonus_de_tamano(), _dados_de_ataque(), _invoke_policy(), _mode_tag(), _reaccion_si_procede(), resolve_roll_mode() (+1 more)

### Community 41 - "dnd_sim/__init__.py"
Cohesion: 0.15
Nodes (6): d20(), D20Result, roll_d20(), roll_dice(), HealEffect, StateEffect

### Community 42 - "ActionType"
Cohesion: 0.13
Nodes (11): ActionType, TurnResources, apply_concentration(), _contexto_de_reaccion(), Spell, SpellAction, trigger_reaction(), test_el_ogre_no_carga_hechizos() (+3 more)

### Community 43 - "roll_modifiers.py"
Cohesion: 0.13
Nodes (4): check_modifiers(), CheckModifiers, _condiciones(), effective_ac()

### Community 44 - "legendary_parser.py"
Cohesion: 0.09
Nodes (16): _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary(), _por_datos() (+8 more)

### Community 45 - "Abilities"
Cohesion: 0.23
Nodes (13): Abilities, Monster, test_dos_combates_seguidos_empiezan_sin_condiciones(), test_inmovilizado_da_desventaja_solo_en_des(), test_la_politica_no_se_invoca_para_un_incapacitado(), test_las_condiciones_incapacitantes_fallan_fue_y_des_sin_tirar_dados(), test_las_condiciones_incapacitantes_no_fallan_automaticamente_la_con(), test_petrificado_tiene_resistencia_a_todo() (+5 more)

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `load_monster` to `test_area.py`, `test_attach.py`, `test_legendary.py`, `run_combat`, `Condition`, `save_builder.py`, `test_spells.py`, `PlayerCharacter`, `test_traits.py`, `test_conditions.py`, `condition_parser.py`, `CombatContext`, `combatant.py`, `test_multiattack.py`, `test_azer.py`, `traits.py`, `test_extra_damage.py`, `build_spell_actions`, `actions.py`, `_spell_data`, `test_damage.py`, `test_checks_escapes.py`, `attack_roll`, `damage.py`, `dnd_sim/__init__.py`, `ActionType`, `legendary_parser.py`, `Abilities`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `ActionType` and `UnknownUsageError`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06277665995975855 - nodes in this community are weakly interconnected._
- **Why does `attack_roll()` connect `attack_roll` to `test_attach.py`, `test_legendary.py`, `saves.py`, `Condition`, `test_spells.py`, `test_traits.py`, `test_conditions.py`, `legendary_phase`, `apply_condition`, `CombatContext`, `pick`, `test_multiattack.py`, `test_azer.py`, `_ctx`, `test_extra_damage.py`, `actions.py`, `AttackRange`, `test_damage.py`, `test_checks_escapes.py`, `combat.py`, `dnd_sim/__init__.py`, `roll_modifiers.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `attack_roll()` (e.g. with `Attack` and `Combatant`) actually correct?**
  _`attack_roll()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_legendary.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1036036036036036 - nodes in this community are weakly interconnected._
- **Why does `apply_condition()` connect `apply_condition` to `test_attach.py`, `test_checks_escapes.py`, `test_legendary.py`, `Condition`, `area.py`, `combat.py`, `dnd_sim/__init__.py`, `ActionType`, `test_spells.py`, `test_conditions.py`, `Abilities`, `legendary_phase`, `CombatContext`, `ConditionTracker`, `_ctx`, `begin_turn`, `actions.py`, `AttackRange`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
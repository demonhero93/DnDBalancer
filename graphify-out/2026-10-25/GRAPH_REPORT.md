# Graph Report - DnDBalancer  (2026-10-25)

## Corpus Check
- 130 files · ~85,526 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 1510 nodes · 5365 edges · 60 communities (49 shown, 11 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 386 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `93645a74`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- dnd_sim/__init__.py
- test_attach.py
- load_monster
- run_combat
- test_area.py
- test_enlarge.py
- spell_parser.py
- test_martial_advantage.py
- test_spells.py
- test_traits.py
- Condition
- apply_condition
- test_loader_actions.py
- TurnResources
- condition_parser.py
- CombatContext
- attack_roll
- LegendaryState
- combatant.py
- test_legendary.py
- legendary_phase
- ConditionTracker
- legendary.py
- test_azer.py
- Trait
- escape_parser.py
- Spellcasting
- _duelo
- AttackModifiers
- parse_spell
- random
- test_checks_escapes.py
- RollMode
- area.py
- warnings
- ability_check
- test_pack_tactics.py
- test_extra_damage.py
- test_la_resistencia_funciona_en_todas_las_rutas
- hooks
- test_parry.py
- AreaSaveAction
- roll_modifiers.py
- legendary_parser.py
- conditions.py
- traits.py
- PlayerCharacter
- Attack
- Parry
- AttackRange
- Any
- Abilities
- DamageTransfer
- CheckResult
- StateEffect
- Relentless
- effective_ac
- TurnResistance
- UndeadFortitude

## God Nodes (most connected - your core abstractions)
1. `apply_condition()` - 105 edges
2. `load_monster()` - 100 edges
3. `attack_roll()` - 99 edges
4. `Condition` - 92 edges
5. `CombatContext` - 77 edges
6. `Attack` - 73 edges
7. `Abilities` - 69 edges
8. `AttackRange` - 69 edges
9. `run_combat()` - 66 edges
10. `Monster` - 64 edges

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

## Communities (60 total, 11 thin omitted)

### Community 0 - "dnd_sim/__init__.py"
Cohesion: 0.09
Nodes (13): ability_mod(), d20(), roll_d20(), roll_dice(), legendary_resistance(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria() (+5 more)

### Community 1 - "test_attach.py"
Cohesion: 0.09
Nodes (32): Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), parse_attach_effects(), _atacar() (+24 more)

### Community 2 - "load_monster"
Cohesion: 0.08
Nodes (16): AttackEntry, parse_range_type(), _damage_type(), _extract_multiattack_alternatives(), load_monster(), _norm_name(), _simple_damage_modifiers(), extract_multiattack_alternatives() (+8 more)

### Community 3 - "run_combat"
Cohesion: 0.06
Nodes (35): run_combat(), _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno() (+27 more)

### Community 4 - "test_area.py"
Cohesion: 0.26
Nodes (21): AreaTargeting, select_area_targets(), SaveDamage, SaveResult, _area_action(), _ctx(), _npc(), _pj() (+13 more)

### Community 5 - "test_enlarge.py"
Cohesion: 0.15
Nodes (24): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+16 more)

### Community 6 - "spell_parser.py"
Cohesion: 0.06
Nodes (14): _afecta_movimiento(), _condicion_con_salvacion(), _crea_objetos(), _dados_de_dano(), _dc_ability(), _elementos_totales(), _es_ilusion(), _numero_elementos() (+6 more)

### Community 8 - "test_martial_advantage.py"
Cohesion: 0.06
Nodes (31): MultiattackAction, _cache_path(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError, _armor_class_value(), _load_fixture() (+23 more)

### Community 9 - "test_spells.py"
Cohesion: 0.12
Nodes (25): build_spell_actions(), SpellFixedDamageAction, _ctx(), _desde_fixture(), _monstruo_lanzador(), _npc(), _pj(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado() (+17 more)

### Community 10 - "test_traits.py"
Cohesion: 0.11
Nodes (23): _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _RasgoDeSalvacion, _sahuagin(), _sahuagin_con_rasgo() (+15 more)

### Community 11 - "Condition"
Cohesion: 0.19
Nodes (26): Condition, test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+18 more)

### Community 12 - "apply_condition"
Cohesion: 0.12
Nodes (35): apply_condition(), _ctx(), _data(), _load(), _pj(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente(), test_can_act_y_can_react(), test_condicion_fuera_del_enum_lanza_value_error() (+27 more)

### Community 13 - "test_loader_actions.py"
Cohesion: 0.13
Nodes (16): is_area_action(), UsageKind, _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite() (+8 more)

### Community 14 - "TurnResources"
Cohesion: 0.21
Nodes (5): ActionType, TurnResources, Spell, SpellAction, test_un_hechizo_de_accion_bonus_se_comprueba_en_su_fase()

### Community 15 - "condition_parser.py"
Cohesion: 0.15
Nodes (6): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), normalize_ability()

### Community 16 - "CombatContext"
Cohesion: 0.07
Nodes (19): AttackAction, CombatAction, CombatContext, _living_enemies(), _log(), SaveAction, pick(), apply_concentration() (+11 more)

### Community 17 - "attack_roll"
Cohesion: 0.09
Nodes (19): _actualizar_distancia(), _agrandado(), attack_roll(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), CombatResult, _dados_de_ataque() (+11 more)

### Community 18 - "LegendaryState"
Cohesion: 0.17
Nodes (4): LegendaryState, _estado(), test_el_estado_legendario_rellena_gasta_y_reinicia(), test_use_probability_medio_se_usa_about_50_por_ciento()

### Community 19 - "combatant.py"
Cohesion: 0.08
Nodes (11): WeaponAttackAction, ExtraDamage, CombatState, CombatantType, CombatState, Condition, normalize_ability(), DamageType (+3 more)

### Community 20 - "test_legendary.py"
Cohesion: 0.11
Nodes (26): saving_throw(), _data(), _load(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_con_use_probability_uno_el_danio_es_mayor_que_con_cero(), test_el_ala_que_mezcla_movimiento_avisa(), test_el_cantrip_del_lich_se_omite_con_aviso() (+18 more)

### Community 21 - "legendary_phase"
Cohesion: 0.13
Nodes (28): legendary_phase(), _contexto(), _pj(), test_con_una_sola_accion_asequible_pick_no_consume_rng(), test_dos_duenos_legendarios_actuan_cada_uno_una_vez(), test_el_combate_termina_en_medio_de_la_fase(), test_el_dragon_contra_un_grupo_usa_acciones_legendarias(), test_la_fase_ocurre_despues_del_end_turn() (+20 more)

### Community 22 - "ConditionTracker"
Cohesion: 0.12
Nodes (4): ConditionTracker, ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 23 - "legendary.py"
Cohesion: 0.11
Nodes (11): _accion_utilizable(), _acciones_asequibles(), _combate_terminado(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), _equipos_vivos() (+3 more)

### Community 24 - "test_azer.py"
Cohesion: 0.23
Nodes (18): HeatedBody, _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), _rasgo() (+10 more)

### Community 26 - "escape_parser.py"
Cohesion: 0.18
Nodes (5): has_escape_text(), parse_escape(), _data(), test_el_fixture_de_la_constriccion_tiene_escape_y_avisa_de_grappled(), test_el_fixture_de_la_telaraña_carga_restrained_con_escape()

### Community 27 - "Spellcasting"
Cohesion: 0.19
Nodes (7): parse_spellcasting(), Spellcasting, test_el_hechizo_enlarge_es_un_estado_self(), test_el_lanzador_se_lee_de_los_special_abilities(), test_initialize_slots_usa_la_tabla_real_de_un_lanzador_completo(), test_la_curacion_usa_el_modificador_de_caracteristica_no_el_bono_completo(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 28 - "_duelo"
Cohesion: 0.18
Nodes (15): _ataque(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja(), test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_los_indicadores_estaticos_siguen_funcionando_y_se_combinan(), test_melee_or_ranged_elige_uno_de_los_dos_modos() (+7 more)

### Community 30 - "parse_spell"
Cohesion: 0.14
Nodes (27): parse_spell(), HealEffect, spell_action(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador() (+19 more)

### Community 31 - "random"
Cohesion: 0.19
Nodes (8): print_report(), simulate(), build_parser(), _build_party(), _load_party(), main(), _parse_monster_token(), test_informe_final_con_apartados_de_pj_y_monstruros()

### Community 32 - "test_checks_escapes.py"
Cohesion: 0.16
Nodes (29): EscapeCheck, begin_turn(), _ctx(), _load(), _pj(), test_con_dos_caracteristicas_se_elige_una_al_azar(), test_con_una_sola_caracteristica_no_consume_rng(), test_consumes_action_gasta_la_accion_del_turno() (+21 more)

### Community 33 - "RollMode"
Cohesion: 0.16
Nodes (12): RollMode, CheckModifiers, save_modifiers(), SaveModifiers, _datos(), _lich(), _pj(), test_con_ventaja_acierta_mas_que_sin_ella() (+4 more)

### Community 34 - "area.py"
Cohesion: 0.16
Nodes (7): _log_target(), sample(), _mode_tag(), _outcome_tag(), _log_line_outcome(), test_sample_devuelve_todos_sin_consumir_rng(), test_sample_k_menor_devuelve_distintos_y_uniformes()

### Community 35 - "warnings"
Cohesion: 0.16
Nodes (7): _resistencia_legendaria(), _declara_uso(), _usage(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_tipo_desconocido_avisa()

### Community 36 - "ability_check"
Cohesion: 0.12
Nodes (9): ability_check(), ability_check_bonus(), _guia(), test_probabilidad_de_liberarse_con_cd_12(), test_prueba_con_envenenado_o_aterrorizado_da_desventaja(), test_prueba_con_ventaja_da_75_por_ciento(), test_prueba_de_caracteristica_con_bonus_0_da_50_por_ciento(), test_sin_autoexito_ni_autofallo_en_pruebas() (+1 more)

### Community 37 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 38 - "test_extra_damage.py"
Cohesion: 0.18
Nodes (17): DamageRecorder, _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional() (+9 more)

### Community 39 - "test_la_resistencia_funciona_en_todas_las_rutas"
Cohesion: 0.15
Nodes (6): _apply_condition_riders(), ConditionAction, ConditionEffect, RepeatSave, test_la_resistencia_funciona_en_todas_las_rutas(), test_un_pj_con_ataque_con_rider_no_aplica_la_condicion_mientras_queden_usos()

### Community 40 - "hooks"
Cohesion: 0.22
Nodes (5): BloodFrenzy, hooks(), test_el_catalogo_cubre_hooks_que_los_rasgos_aun_no_usan(), test_hooks_con_un_nombre_fuera_del_catalogo_lanza_error(), test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 41 - "test_parry.py"
Cohesion: 0.26
Nodes (21): D20Result, _arquero_parry(), _ataque(), _ctx(), _datos(), _fijar_d20(), espia(), _gladiador() (+13 more)

### Community 43 - "roll_modifiers.py"
Cohesion: 0.17
Nodes (5): resolve_roll_mode(), attack_modifiers(), check_modifiers(), _condiciones(), _hooks()

### Community 44 - "legendary_parser.py"
Cohesion: 0.11
Nodes (12): _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary(), _por_datos() (+4 more)

### Community 45 - "conditions.py"
Cohesion: 0.11
Nodes (11): _as_condition(), attempt_escapes(), _contar(), _default_targeting(), end_turn(), _label(), _queda_accion(), remove_condition() (+3 more)

### Community 46 - "traits.py"
Cohesion: 0.12
Nodes (4): aliados_capaces(), _condicion_posicional(), MartialAdvantage, PackTactics

### Community 47 - "PlayerCharacter"
Cohesion: 0.05
Nodes (65): PlayerCharacter, remove_invisibility_on_action(), _hooks(), inflict_damage(), _notify_damage_dealt(), _salvar_a_cero(), _entradas(), parse_traits() (+57 more)

### Community 48 - "Attack"
Cohesion: 0.14
Nodes (5): Attack, Combatant, _notify_damage_taken(), test_extra_damage_estructura_por_defecto_vacia(), test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio()

### Community 49 - "Parry"
Cohesion: 0.25
Nodes (3): _empuna_arma_melee(), Parry, _ve_al_atacante()

### Community 50 - "AttackRange"
Cohesion: 0.22
Nodes (11): AttackRange, resolve_attack_range(), _ataque(), _duelo(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia() (+3 more)

### Community 52 - "Abilities"
Cohesion: 0.11
Nodes (23): Abilities, _tag_modificadores(), Monster, apply_damage_modifiers(), test_sin_condiciones_el_dano_no_cambia(), _guerrero_y_ogro(), _target(), test_attack_roll_log_modifier() (+15 more)

### Community 54 - "CheckResult"
Cohesion: 0.50
Nodes (3): CheckResult, _check_fijo(), _fake()

## Knowledge Gaps
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `load_monster` to `dnd_sim/__init__.py`, `test_attach.py`, `run_combat`, `test_area.py`, `test_enlarge.py`, `test_martial_advantage.py`, `test_spells.py`, `test_traits.py`, `Condition`, `apply_condition`, `test_loader_actions.py`, `TurnResources`, `condition_parser.py`, `CombatContext`, `combatant.py`, `test_legendary.py`, `test_azer.py`, `random`, `test_checks_escapes.py`, `RollMode`, `warnings`, `test_pack_tactics.py`, `test_extra_damage.py`, `test_parry.py`, `legendary_parser.py`, `PlayerCharacter`, `Attack`, `Abilities`, `StateEffect`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `ActionType` and `UnknownUsageError`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `dnd_sim/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09146341463414634 - nodes in this community are weakly interconnected._
- **Why does `attack_roll()` connect `attack_roll` to `dnd_sim/__init__.py`, `test_attach.py`, `test_enlarge.py`, `test_martial_advantage.py`, `test_spells.py`, `test_traits.py`, `Condition`, `apply_condition`, `CombatContext`, `test_legendary.py`, `legendary_phase`, `test_azer.py`, `_duelo`, `parse_spell`, `test_checks_escapes.py`, `test_extra_damage.py`, `test_la_resistencia_funciona_en_todas_las_rutas`, `test_parry.py`, `roll_modifiers.py`, `PlayerCharacter`, `Attack`, `AttackRange`, `Abilities`, `effective_ac`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `attack_roll()` (e.g. with `Attack` and `Combatant`) actually correct?**
  _`attack_roll()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09288824383164006 - nodes in this community are weakly interconnected._
- **Why does `CombatContext` connect `CombatContext` to `dnd_sim/__init__.py`, `test_attach.py`, `run_combat`, `test_area.py`, `test_enlarge.py`, `test_martial_advantage.py`, `test_spells.py`, `test_traits.py`, `Condition`, `apply_condition`, `TurnResources`, `attack_roll`, `test_legendary.py`, `legendary_phase`, `legendary.py`, `test_azer.py`, `parse_spell`, `test_checks_escapes.py`, `area.py`, `test_pack_tactics.py`, `test_extra_damage.py`, `test_parry.py`, `AreaSaveAction`, `PlayerCharacter`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
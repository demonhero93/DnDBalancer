# Graph Report - DnDBalancer  (2026-11-02)

## Corpus Check
- 200 files · ~133,499 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 2505 nodes · 8935 edges · 88 communities (77 shown, 11 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 519 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4fed66e2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- load_monster
- test_attach.py
- test_berserker.py
- run_combat
- test_area.py
- test_enlarge.py
- test_magical.py
- test_legendary.py
- test_beast.py
- test_spells.py
- RollMode
- Condition
- test_utility.py
- PlayerCharacter
- Trait
- spell_parser.py
- DamageTransfer
- test_damage.py
- BarbarianFeatures
- test_loader_actions.py
- CombatContext
- _estado
- ActionUsage
- test_barbarian.py
- barbarian/__init__.py
- saves.py
- multiattack_parser.py
- test_death.py
- json
- test_parry.py
- inflict_damage
- MultiattackAction
- test_backgrounds.py
- BeastFeatures
- test_skills.py
- warnings
- test_lair.py
- test_proficiency.py
- encounter.py
- Regeneration
- saving_throw
- Attack
- Abilities
- model/actions.py
- test_condition_immunities.py
- TurnResources
- Attach
- ability_check
- legendary.py
- pytest
- apply_condition
- test_loader.py
- test_pack_tactics.py
- _pj
- parse_escape
- dnd_sim/__init__.py
- test_ancestral_guardian.py
- test_magic_resistance.py
- begin_turn
- _duelo
- random
- legendary_parser.py
- AncestralGuardianFeatures
- Any
- AreaSaveAction
- condition_parser.py
- test_superior_invisibility.py
- test_undead_fortitude.py
- build_spell_actions
- Spellcasting
- roll_modifiers.py
- test_azer.py
- race_parser.py
- ConditionTracker
- test_races.py
- test_multiattack.py
- parse_legendary
- conditions.py
- normalize_ability
- load_race
- spells/__init__.py
- DamageRecorder
- TODO — DnDBalancer / dnd_sim
- test_sin_autoexito_ni_autofallo_en_pruebas
- test_el_cli_tiene_las_opciones_legendarias

## God Nodes (most connected - your core abstractions)
1. `load_monster()` - 135 edges
2. `Attack` - 135 edges
3. `apply_condition()` - 133 edges
4. `Condition` - 129 edges
5. `Abilities` - 127 edges
6. `attack_roll()` - 126 edges
7. `PlayerCharacter` - 104 edges
8. `Monster` - 99 edges
9. `run_combat()` - 93 edges
10. `CombatContext` - 92 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `valid_targets()`  [INFERRED]
  TODO.md → dnd_sim/core/targeting.py
- `Paquetes con fachada` --references--> `CombatResult`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/engine/combat/encounter.py

## Import Cycles
- None detected.

## Communities (88 total, 11 thin omitted)

### Community 0 - "load_monster"
Cohesion: 0.08
Nodes (15): parse_attach_effects(), _damage_type(), load_monster(), _norm_name(), _parse_condition_immunities(), _parse_damage_modifiers(), build_save_effect(), damage_dice_of() (+7 more)

### Community 1 - "test_attach.py"
Cohesion: 0.08
Nodes (39): Arquitectura de `dnd_sim`, Carpetas, Cómo comprobar que todo sigue en orden, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, AttachOnHitEffect (+31 more)

### Community 2 - "test_berserker.py"
Cohesion: 0.07
Nodes (56): AttackRange, apply_berserker(), _armas_melee_de(), BerserkerFeatures, _de(), _furia_de(), _golpe_sin_armas(), IntimidatingPresenceAction (+48 more)

### Community 3 - "run_combat"
Cohesion: 0.13
Nodes (17): run_combat(), _breath(), _eventos(), _FixedRandom, _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(), test_begin_turn_no_tira_nada_si_estan_cargadas() (+9 more)

### Community 4 - "test_area.py"
Cohesion: 0.11
Nodes (27): AreaTargeting, select_area_targets(), _default_targeting(), SaveDamage, _area_action(), _ctx(), _npc(), _pj() (+19 more)

### Community 5 - "test_enlarge.py"
Cohesion: 0.14
Nodes (25): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+17 more)

### Community 6 - "test_magical.py"
Cohesion: 0.13
Nodes (19): apply_beast(), _ctx(), _pj(), _spell_data(), _spellcasting(), test_ataque_con_magical_true_dana_completo_al_ghost(), test_ataque_magico_contra_un_bárbaro_en_furia_se_reduce_a_la_mitad(), test_bestial_solo_marca_las_armas_magicas_desde_el_nivel_6() (+11 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.10
Nodes (47): legendary_phase(), _contexto(), _data(), _load(), _pj(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_con_una_sola_accion_asequible_pick_no_consume_rng() (+39 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (65): WeaponAttackAction, _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll(), spy() (+57 more)

### Community 9 - "test_spells.py"
Cohesion: 0.14
Nodes (31): parse_spell(), spell_action(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_daño_extra_del_hechizo_verdadero_no_baja_de_cinco() (+23 more)

### Community 10 - "RollMode"
Cohesion: 0.10
Nodes (24): RollMode, _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _RasgoDeSalvacion, _sahuagin() (+16 more)

### Community 11 - "Condition"
Cohesion: 0.19
Nodes (26): Condition, test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+18 more)

### Community 12 - "test_utility.py"
Cohesion: 0.15
Nodes (23): _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), _abilities(), _ctx(), _mon(), _pj() (+15 more)

### Community 13 - "PlayerCharacter"
Cohesion: 0.13
Nodes (14): print_report(), simulate(), PlayerCharacter, build_parser(), _build_party(), _load_party(), main(), _parse_monster_token() (+6 more)

### Community 14 - "Trait"
Cohesion: 0.04
Nodes (11): hooks(), Trait, aliados_capaces(), BloodFrenzy, _condicion_posicional(), MartialAdvantage, PackTactics, SuperiorInvisibility (+3 more)

### Community 15 - "spell_parser.py"
Cohesion: 0.10
Nodes (12): _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla(), _frases() (+4 more)

### Community 16 - "DamageTransfer"
Cohesion: 0.12
Nodes (6): DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante()

### Community 17 - "test_damage.py"
Cohesion: 0.13
Nodes (17): _tag_modificadores(), apply_damage_modifiers(), _is_petrified(), _target(), test_etiqueta_de_modificadores_se_deriva_del_dano_final(), test_immunity_zero(), test_invalid_damage_type_raises(), test_no_modifiers_unchanged() (+9 more)

### Community 18 - "BarbarianFeatures"
Cohesion: 0.10
Nodes (5): BarbarianFeatures, _contexto(), _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 19 - "test_loader_actions.py"
Cohesion: 0.17
Nodes (14): _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga(), test_ataque_con_usage_conserva_el_actionusage() (+6 more)

### Community 20 - "CombatContext"
Cohesion: 0.09
Nodes (13): pick(), _objetivo_enganche(), valid_targets(), actor_is_alive(), CombatContext, _en_accion_de_ataque(), _living_enemies(), _log() (+5 more)

### Community 21 - "_estado"
Cohesion: 0.50
Nodes (3): _estado(), test_el_estado_legendario_rellena_gasta_y_reinicia(), test_use_probability_medio_se_usa_about_50_por_ciento()

### Community 22 - "ActionUsage"
Cohesion: 0.14
Nodes (12): RageAction, ActionUsage, UsageKind, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar(), test_per_day_dos_usos_y_luego_can_use_falso(), test_per_day_no_tira_recarga(), test_per_day_reset_restaura_todos_los_usos() (+4 more)

### Community 23 - "test_barbarian.py"
Cohesion: 0.09
Nodes (48): rage_uses(), apply_barbarian(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj(), _resultado() (+40 more)

### Community 24 - "barbarian/__init__.py"
Cohesion: 0.07
Nodes (12): ExtendRageAction, apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), SpikedArmorAction, FormOfTheBeast, NaturalWeapon (+4 more)

### Community 25 - "saves.py"
Cohesion: 0.16
Nodes (11): _log_target(), apply_save_damage(), _as_combat_context(), _inflict_for_save(), _mode_tag(), _outcome_tag(), _reaccion_si_procede(), _resolve_mode_str() (+3 more)

### Community 26 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (5): _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 27 - "test_death.py"
Cohesion: 0.13
Nodes (18): combat_finished(), living_teams(), _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero() (+10 more)

### Community 28 - "json"
Cohesion: 0.15
Nodes (9): _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError (+1 more)

### Community 29 - "test_parry.py"
Cohesion: 0.26
Nodes (21): D20Result, _arquero_parry(), _ataque(), _ctx(), _datos(), _fijar_d20(), espia(), _gladiador() (+13 more)

### Community 30 - "inflict_damage"
Cohesion: 0.12
Nodes (18): _absorber_pv_temporales(), _hooks(), inflict_damage(), _mitigacion_de_otros(), _notify_damage_dealt(), _salvar_a_cero(), _ctx(), _datos() (+10 more)

### Community 31 - "MultiattackAction"
Cohesion: 0.14
Nodes (5): _clamp(), extra_attacks_for(), rage_damage(), MultiattackAction, _habilitar_armas_naturales()

### Community 32 - "test_backgrounds.py"
Cohesion: 0.11
Nodes (19): Background, normalize_tool(), _add(), load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias() (+11 more)

### Community 34 - "test_skills.py"
Cohesion: 0.13
Nodes (21): _abilities(), _ctx(), _load_fixture(), _pj(), _SoloMod, test_ability_check_no_suma_competencia_de_habilidad(), test_attempt_escapes_tira_la_habilidad(), test_caracteristica_asociada() (+13 more)

### Community 35 - "warnings"
Cohesion: 0.16
Nodes (7): _resistencia_legendaria(), _declara_uso(), _usage(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_tipo_desconocido_avisa()

### Community 36 - "test_lair.py"
Cohesion: 0.07
Nodes (35): load_lair(), lair_phase(), LairAction, LegendaryState, _ctx(), _dragon(), _enemigo(), lairs_dir() (+27 more)

### Community 37 - "test_proficiency.py"
Cohesion: 0.15
Nodes (21): proficiency_bonus(), ability_check_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia() (+13 more)

### Community 38 - "encounter.py"
Cohesion: 0.13
Nodes (12): d20(), roll_d20(), CombatResult, _invoke_policy(), roll_initiative(), _run_combat(), _nuevo_ctx(), _summarize_damage() (+4 more)

### Community 39 - "Regeneration"
Cohesion: 0.11
Nodes (5): _es_radiante(), _guardar_salvacion(), Regeneration, Relentless, UndeadFortitude

### Community 40 - "saving_throw"
Cohesion: 0.11
Nodes (19): save_modifiers(), _con_resistencia_legendaria(), SaveResult, saving_throw(), fake_saving_throw(), test_resistance_probability_cero_nunca_convierte(), test_resistance_probability_medio_convierte_about_50_por_ciento(), test_resistance_probability_uno_no_consume_rng() (+11 more)

### Community 41 - "Attack"
Cohesion: 0.15
Nodes (22): _actualizar_distancia(), attack_roll(), _mode_tag(), Attack, test_alma_bestial_flag_magical_existe(), _azer(), _ctx(), _datos() (+14 more)

### Community 42 - "Abilities"
Cohesion: 0.05
Nodes (72): Abilities, Monster, resolve_attack_range(), _ataque(), _ctx(), _data(), _duelo(), _load() (+64 more)

### Community 43 - "model/actions.py"
Cohesion: 0.06
Nodes (13): roll_dice(), log_line(), sample(), ActionType, AttackEntry, CombatAction, desenganchar(), intentar_desenganche() (+5 more)

### Community 44 - "test_condition_immunities.py"
Cohesion: 0.12
Nodes (16): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+8 more)

### Community 45 - "TurnResources"
Cohesion: 0.16
Nodes (32): TurnResources, AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer(), _bj() (+24 more)

### Community 47 - "ability_check"
Cohesion: 0.10
Nodes (15): _clean(), normalize_skill(), skill_ability(), ability_check(), CheckResult, _finish_check(), _guia(), _resolve_mods() (+7 more)

### Community 48 - "legendary.py"
Cohesion: 0.12
Nodes (11): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), legendary_resistance(), LegendaryAction (+3 more)

### Community 49 - "pytest"
Cohesion: 0.21
Nodes (15): apply_ancestral_guardian(), apply_class(), _abilities(), _firmas(), _pj(), test_apply_class_ancestral_equivalente_a_los_apply_suelto(), test_apply_class_battlerager_equivalente_a_los_apply_suelto(), test_apply_class_normaliza_el_nombre() (+7 more)

### Community 50 - "apply_condition"
Cohesion: 0.10
Nodes (41): apply_condition(), attempt_escapes(), EscapeCheck, effective_ac(), _ctx(), _data(), _load(), _pj() (+33 more)

### Community 51 - "test_loader.py"
Cohesion: 0.16
Nodes (11): _armor_class_value(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper(), test_cache_avoids_second_network(), test_load_monster_maps_ogre() (+3 more)

### Community 52 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 53 - "_pj"
Cohesion: 0.17
Nodes (14): _ctx(), _npc(), _pj(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizado_invierte_los_objetivos_de_ataque(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado(), test_el_hechizo_verdadero_es_un_ataque_real_con_dano_extra(), test_el_proyectil_magico_pasa_por_los_modificadores_de_dano() (+6 more)

### Community 54 - "parse_escape"
Cohesion: 0.22
Nodes (5): has_escape_text(), parse_escape(), _skills_for(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 57 - "dnd_sim/__init__.py"
Cohesion: 0.08
Nodes (9): ability_mod(), CombatState, DamageType, parse_damage_type(), AttackAction, Combatant, CombatantType, _mark_dead_if_down() (+1 more)

### Community 59 - "test_ancestral_guardian.py"
Cohesion: 0.18
Nodes (26): _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado(), _escudo(), _esperado() (+18 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.13
Nodes (22): ConditionInstance, _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab() (+14 more)

### Community 61 - "begin_turn"
Cohesion: 0.23
Nodes (15): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+7 more)

### Community 62 - "_duelo"
Cohesion: 0.31
Nodes (7): _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

### Community 63 - "random"
Cohesion: 0.26
Nodes (18): _abilities(), _ctx(), _decide(), _pj(), test_antes_del_nivel_2_no_hay_decision_ni_rng(), test_en_turno_ajeno_no_decide(), test_frecuencia_0_5_es_aproximadamente_la_mitad_de_los_turnos(), test_las_reacciones_no_deciden_ni_reciben() (+10 more)

### Community 64 - "legendary_parser.py"
Cohesion: 0.10
Nodes (11): is_area_action(), parse_range_type(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _nombres_candidatas(), _por_datos(), _por_referencia() (+3 more)

### Community 66 - "Any"
Cohesion: 0.12
Nodes (9): _agrandado(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), _reaccion_si_procede(), _trigger_after_attack_roll(), _trigger_after_being_hit() (+1 more)

### Community 67 - "AreaSaveAction"
Cohesion: 0.12
Nodes (9): _check_fields(), _construir(), _error(), SaveAction, AreaSaveAction, ConditionAction, ConditionEffect, RepeatSave (+1 more)

### Community 68 - "condition_parser.py"
Cohesion: 0.18
Nodes (5): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with()

### Community 69 - "test_superior_invisibility.py"
Cohesion: 0.16
Nodes (19): _entradas(), parse_traits(), remove_invisibility_on_action(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd(), test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad(), test_el_umbral_se_saca_de_cada_descripcion(), _accion(), _ctx() (+11 more)

### Community 70 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 71 - "build_spell_actions"
Cohesion: 0.29
Nodes (8): build_spell_actions(), _desde_fixture(), _monstruo_lanzador(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_la_reaccion_gasta_su_uso_propio(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_uso_propio(), test_un_hechizo_a_voluntad_se_puede_lanzar_en_cada_turno()

### Community 72 - "Spellcasting"
Cohesion: 0.11
Nodes (9): Paquetes con fachada, parse_spellcasting(), _uso_de_entrada(), Spell, Spellcasting, test_el_lanzador_se_lee_de_los_actions(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_un_hechizo_de_accion_bonus_se_comprueba_en_su_fase() (+1 more)

### Community 73 - "roll_modifiers.py"
Cohesion: 0.17
Nodes (5): resolve_roll_mode(), attack_modifiers(), _condiciones(), _hooks(), _instancias()

### Community 74 - "test_azer.py"
Cohesion: 0.26
Nodes (17): _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), _rasgo(), test_ataque_a_distancia_no_dispara_la_represalia() (+9 more)

### Community 75 - "race_parser.py"
Cohesion: 0.13
Nodes (9): parse_race(), _skill_name(), _spells_from_description(), _trait_skills(), _keen_senses(), test_parse_competencias_fijas_de_la_raza(), test_parse_descripcion_sin_hechizos_da_vacio(), test_parse_elfo_linaje_hechizos_sin_duplicados() (+1 more)

### Community 77 - "test_races.py"
Cohesion: 0.22
Nodes (12): Race, _abilities(), _fiendish_legacy(), _pj(), test_apply_race_añade_competencias_fijas(), test_apply_race_con_habilidad_pedida(), test_apply_race_habilidad_fuera_de_las_opciones_es_error(), test_apply_race_no_duplica_competencias_existentes() (+4 more)

### Community 78 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 79 - "parse_legendary"
Cohesion: 0.20
Nodes (5): _coste_y_nombre(), _motivo_omision(), parse_legendary(), _warn(), test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio()

### Community 80 - "conditions.py"
Cohesion: 0.15
Nodes (9): _apply_condition_riders(), _as_condition(), _condicion_bloqueada(), _contar(), end_turn(), _label(), _queda_accion(), remove_condition() (+1 more)

### Community 82 - "load_race"
Cohesion: 0.33
Nodes (5): load_race(), test_load_race_descarga_la_raza_y_sus_rasgos(), _rasgo(), _raza(), test_load_race_propaga_el_error_de_la_api()

### Community 83 - "spells/__init__.py"
Cohesion: 0.13
Nodes (5): dado_por_nivel(), duracion_en_rondas(), apply_concentration(), HealEffect, StateEffect

### Community 85 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.40
Nodes (4): Bloque 2026-10-30 (commiteado), Grafo y verificación, Rutina sugerida al abrir sesión, TODO — DnDBalancer / dnd_sim

## Knowledge Gaps
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `load_monster`, `test_attach.py`, `test_berserker.py`, `test_enlarge.py`, `test_magical.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `RollMode`, `Condition`, `test_utility.py`, `PlayerCharacter`, `test_damage.py`, `test_barbarian.py`, `barbarian/__init__.py`, `test_death.py`, `test_parry.py`, `inflict_damage`, `test_proficiency.py`, `Abilities`, `model/actions.py`, `TurnResources`, `pytest`, `apply_condition`, `test_pack_tactics.py`, `_pj`, `dnd_sim/__init__.py`, `test_ancestral_guardian.py`, `test_magic_resistance.py`, `begin_turn`, `_duelo`, `random`, `legendary_parser.py`, `AreaSaveAction`, `test_superior_invisibility.py`, `test_undead_fortitude.py`, `test_azer.py`, `parse_legendary`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `UnknownUsageError` and `ActionType`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `load_monster` be split into smaller, more focused modules?**
  _Cohesion score 0.08235294117647059 - nodes in this community are weakly interconnected._
- **Why does `load_monster()` connect `load_monster` to `test_attach.py`, `run_combat`, `test_area.py`, `test_enlarge.py`, `test_magical.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `RollMode`, `Condition`, `PlayerCharacter`, `test_damage.py`, `test_loader_actions.py`, `CombatContext`, `multiattack_parser.py`, `test_death.py`, `json`, `test_parry.py`, `inflict_damage`, `MultiattackAction`, `test_skills.py`, `warnings`, `test_lair.py`, `saving_throw`, `Attack`, `Abilities`, `model/actions.py`, `test_condition_immunities.py`, `Attach`, `ability_check`, `apply_condition`, `test_loader.py`, `test_pack_tactics.py`, `dnd_sim/__init__.py`, `test_magic_resistance.py`, `begin_turn`, `legendary_parser.py`, `condition_parser.py`, `test_superior_invisibility.py`, `test_undead_fortitude.py`, `build_spell_actions`, `test_azer.py`, `test_multiattack.py`, `parse_legendary`, `normalize_ability`, `spells/__init__.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `AttackRange`) actually correct?**
  _`Attack` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07744107744107744 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `load_monster`, `test_attach.py`, `test_berserker.py`, `test_enlarge.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `RollMode`, `test_utility.py`, `Trait`, `spell_parser.py`, `DamageTransfer`, `test_damage.py`, `BarbarianFeatures`, `test_parry.py`, `test_skills.py`, `test_lair.py`, `saving_throw`, `Abilities`, `model/actions.py`, `test_condition_immunities.py`, `Attach`, `ability_check`, `apply_condition`, `test_pack_tactics.py`, `_pj`, `dnd_sim/__init__.py`, `test_magic_resistance.py`, `Any`, `condition_parser.py`, `test_superior_invisibility.py`, `roll_modifiers.py`, `ConditionTracker`, `conditions.py`, `spells/__init__.py`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
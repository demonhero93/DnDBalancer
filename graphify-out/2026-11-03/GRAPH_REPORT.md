# Graph Report - DnDBalancer  (2026-11-02)

## Corpus Check
- 200 files · ~133,530 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 2512 nodes · 8952 edges · 86 communities (81 shown, 5 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 517 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4fed66e2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- loader.py
- test_attach.py
- test_berserker.py
- test_usage.py
- ActionType
- test_enlarge.py
- load_monster
- test_legendary.py
- test_beast.py
- parse_spell
- test_traits.py
- Condition
- test_utility.py
- main.py
- Trait
- spell_parser.py
- DamageTransfer
- Abilities
- BarbarianFeatures
- test_loader_actions.py
- CombatContext
- berserker.py
- ActionUsage
- Attack
- barbarian/__init__.py
- saves.py
- traits/__init__.py
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
- legendary_phase
- test_conditions.py
- model/actions.py
- test_condition_immunities.py
- TurnResources
- intentar_desenganche
- CheckResult
- dnd_sim/__init__.py
- _duelo
- test_checks_escapes.py
- test_loader.py
- test_pack_tactics.py
- SpellFixedDamageAction
- parse_escape
- Combatant
- test_ancestral_guardian.py
- test_magic_resistance.py
- begin_turn
- _duelo
- spell_action
- legendary_parser.py
- test_martial_advantage.py
- attack_roll
- ConditionEffect
- condition_parser.py
- capas.py
- test_undead_fortitude.py
- test_spells.py
- Spellcasting
- RollMode
- test_azer.py
- race_parser.py
- pathlib
- PlayerCharacter
- run_combat
- background_parser.py
- apply_condition
- normalize_ability
- load_race
- spells/__init__.py
- _hooks
- TODO — DnDBalancer / dnd_sim

## God Nodes (most connected - your core abstractions)
1. `load_monster()` - 135 edges
2. `Attack` - 135 edges
3. `apply_condition()` - 134 edges
4. `Condition` - 130 edges
5. `Abilities` - 127 edges
6. `attack_roll()` - 126 edges
7. `PlayerCharacter` - 104 edges
8. `Monster` - 99 edges
9. `run_combat()` - 93 edges
10. `CombatContext` - 92 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `Paquetes con fachada` --references--> `CombatResult`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/engine/combat/encounter.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Carpetas` --references--> `PlayerCharacter`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Carpetas` --references--> `Monster`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py

## Import Cycles
- None detected.

## Communities (86 total, 5 thin omitted)

### Community 0 - "loader.py"
Cohesion: 0.08
Nodes (11): parse_range_type(), _damage_type(), _extract_multiattack_alternatives(), _norm_name(), _parse_condition_immunities(), _parse_damage_modifiers(), extract_multiattack_alternatives(), _norm_name() (+3 more)

### Community 1 - "test_attach.py"
Cohesion: 0.18
Nodes (25): _atacar(), _bite(), _cloaker(), _ctx(), _datos(), _pj(), test_con_ventaja_el_enganche_es_a_la_cabeza_y_ciega(), test_damage_transfer_no_aplica_sin_enganche() (+17 more)

### Community 2 - "test_berserker.py"
Cohesion: 0.16
Nodes (37): AttackRange, _abilities(), _barbaro(), _berserker(), _ctx(), _furia_lista(), _monstruo(), _pj() (+29 more)

### Community 3 - "test_usage.py"
Cohesion: 0.16
Nodes (13): _breath(), _eventos(), _FixedRandom, _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(), test_begin_turn_no_tira_nada_si_estan_cargadas(), test_begin_turn_reinicia_recursos_y_tira_una_recarga_por_accion() (+5 more)

### Community 4 - "ActionType"
Cohesion: 0.05
Nodes (44): _check_fields(), _construir(), _error(), build_condition_action(), build_save_action(), ActionType, actor_is_alive(), AttackAction (+36 more)

### Community 5 - "test_enlarge.py"
Cohesion: 0.17
Nodes (21): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+13 more)

### Community 6 - "load_monster"
Cohesion: 0.08
Nodes (27): load_monster(), apply_beast(), test_una_condicion_desconocida_de_la_api_avisa(), test_fixture_sintetica_carga(), test_monstruo_no_legendario_no_carga_guaridas(), test_monstruo_sin_fichero_no_avisa(), test_el_aliento_del_dragon_no_es_magico(), test_el_loader_fija_magic_resistance() (+19 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.09
Nodes (35): simulate(), _data(), _estado(), _legendaria(), _load(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_con_use_probability_uno_el_danio_es_mayor_que_con_cero() (+27 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (66): WeaponAttackAction, FormOfTheBeast, _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll() (+58 more)

### Community 9 - "parse_spell"
Cohesion: 0.15
Nodes (23): parse_spell(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_daño_extra_del_hechizo_verdadero_no_baja_de_cinco(), test_el_proyectil_magico_es_dano_automatico() (+15 more)

### Community 10 - "test_traits.py"
Cohesion: 0.11
Nodes (24): attack_modifiers(), _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDeSalvacion, _sahuagin(), _sahuagin_con_rasgo() (+16 more)

### Community 11 - "Condition"
Cohesion: 0.20
Nodes (25): Condition, _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj(), test_atacar_a_un_invisible_tiene_desventaja() (+17 more)

### Community 12 - "test_utility.py"
Cohesion: 0.07
Nodes (36): ConditionInstance, ConditionTracker, registrar_resistencia(), SaveResult, _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria() (+28 more)

### Community 13 - "main.py"
Cohesion: 0.27
Nodes (6): print_report(), build_parser(), _build_party(), _load_party(), main(), _parse_monster_token()

### Community 14 - "Trait"
Cohesion: 0.06
Nodes (4): Attach, Trait, BloodFrenzy, test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 15 - "spell_parser.py"
Cohesion: 0.10
Nodes (13): _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla(), _frases() (+5 more)

### Community 16 - "DamageTransfer"
Cohesion: 0.14
Nodes (5): DamageTransfer, _empuna_arma_melee(), Parry, TurnResistance, _ve_al_atacante()

### Community 17 - "Abilities"
Cohesion: 0.09
Nodes (28): Abilities, Monster, apply_damage_modifiers(), _is_petrified(), test_inmovilizado_da_desventaja_solo_en_des(), test_las_condiciones_incapacitantes_fallan_fue_y_des_sin_tirar_dados(), test_las_condiciones_incapacitantes_no_fallan_automaticamente_la_con(), test_petrificado_tiene_resistencia_a_todo() (+20 more)

### Community 18 - "BarbarianFeatures"
Cohesion: 0.09
Nodes (6): BarbarianFeatures, _contexto(), ExtendRageAction, _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 19 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (14): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+6 more)

### Community 20 - "CombatContext"
Cohesion: 0.11
Nodes (9): _objetivo_enganche(), valid_targets(), CombatContext, _living_enemies(), _log(), HealAction, _romper_invisibilidad_al_lanzar(), SpellStateAction (+1 more)

### Community 21 - "berserker.py"
Cohesion: 0.10
Nodes (6): _armas_melee_de(), BerserkerFeatures, _de(), _furia_de(), _golpe_sin_armas(), test_golpe_sin_armas_unidad()

### Community 22 - "ActionUsage"
Cohesion: 0.15
Nodes (11): ActionUsage, UsageKind, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar(), test_per_day_dos_usos_y_luego_can_use_falso(), test_per_day_no_tira_recarga(), test_per_day_reset_restaura_todos_los_usos(), test_recharge_5_6_porcentaje_de_exito() (+3 more)

### Community 23 - "Attack"
Cohesion: 0.06
Nodes (68): Attack, apply_barbarian(), _nuevo_ataque(), DamageRecorder, SaveModifiers, _abilities(), _ctx(), _pj() (+60 more)

### Community 24 - "barbarian/__init__.py"
Cohesion: 0.14
Nodes (15): RageAction, NaturalWeapon, apply_berserker(), IntimidatingPresenceAction, _presencia_ctx(), test_apply_anade_trait_y_accion(), test_presencia_afecta_a_un_numero_aleatorio_de_enemigos(), test_presencia_requiere_nivel_14() (+7 more)

### Community 25 - "saves.py"
Cohesion: 0.13
Nodes (9): roll_d20(), roll_dice(), _finish_check(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save(), _reaccion_si_procede(), _resolve_mode_str() (+1 more)

### Community 26 - "traits/__init__.py"
Cohesion: 0.10
Nodes (6): StateEffect, aliados_capaces(), _condicion_posicional(), MartialAdvantage, PackTactics, SuperiorInvisibility

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 28 - "json"
Cohesion: 0.15
Nodes (9): _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError (+1 more)

### Community 29 - "test_parry.py"
Cohesion: 0.11
Nodes (39): D20Result, _entradas(), parse_traits(), _arquero_parry(), _ataque(), _ctx(), _datos(), _fijar_d20() (+31 more)

### Community 30 - "inflict_damage"
Cohesion: 0.19
Nodes (15): _absorber_pv_temporales(), inflict_damage(), _notify_damage_dealt(), _ctx(), _datos(), _jabali(), _pj(), test_el_jabali_carga_su_relentless_con_umbral_y_uso() (+7 more)

### Community 31 - "MultiattackAction"
Cohesion: 0.14
Nodes (6): _clamp(), extra_attacks_for(), rage_damage(), rage_uses(), MultiattackAction, _habilitar_armas_naturales()

### Community 32 - "test_backgrounds.py"
Cohesion: 0.16
Nodes (17): Background, load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes(), test_apply_background_sin_competencias_es_inofensivo() (+9 more)

### Community 33 - "BeastFeatures"
Cohesion: 0.08
Nodes (4): BeastFeatures, CallTheHuntBonus, _mark_dead_if_down(), _notify_damage_taken()

### Community 34 - "test_skills.py"
Cohesion: 0.07
Nodes (30): _clean(), normalize_skill(), skill_ability(), ability_check_bonus(), _guia(), skill_bonus(), skill_check(), _abilities() (+22 more)

### Community 35 - "warnings"
Cohesion: 0.15
Nodes (8): _resistencia_legendaria(), _declara_uso(), _usage(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 36 - "test_lair.py"
Cohesion: 0.07
Nodes (32): load_lair(), lair_phase(), LairAction, LegendaryState, _ctx(), _dragon(), _enemigo(), lairs_dir() (+24 more)

### Community 37 - "test_proficiency.py"
Cohesion: 0.15
Nodes (20): proficiency_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia() (+12 more)

### Community 38 - "encounter.py"
Cohesion: 0.16
Nodes (9): d20(), combat_finished(), living_teams(), CombatResult, _invoke_policy(), roll_initiative(), _run_combat(), _nuevo_ctx() (+1 more)

### Community 39 - "Regeneration"
Cohesion: 0.11
Nodes (5): _es_radiante(), _guardar_salvacion(), Regeneration, Relentless, UndeadFortitude

### Community 40 - "saving_throw"
Cohesion: 0.20
Nodes (11): save_modifiers(), saving_throw(), test_resistance_probability_medio_convierte_about_50_por_ciento(), _datos(), _lich(), _pj(), test_con_ventaja_acierta_mas_que_sin_ella(), test_da_ventaja_si_la_salvacion_es_de_conversion() (+3 more)

### Community 41 - "legendary_phase"
Cohesion: 0.17
Nodes (22): legendary_phase(), _contexto(), _pj(), test_con_una_sola_accion_asequible_pick_no_consume_rng(), test_dos_duenos_legendarios_actuan_cada_uno_una_vez(), test_el_combate_termina_en_medio_de_la_fase(), test_la_fase_ocurre_despues_del_end_turn(), test_no_actua_si_el_combate_ya_terminado() (+14 more)

### Community 42 - "test_conditions.py"
Cohesion: 0.12
Nodes (32): end_turn(), _ctx(), _data(), _load(), _pj(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente(), test_can_act_y_can_react(), test_condicion_fuera_del_enum_lanza_value_error() (+24 more)

### Community 43 - "model/actions.py"
Cohesion: 0.07
Nodes (7): CombatState, DamageType, parse_damage_type(), log_line(), AttackEntry, ExtraDamage, desenganchar()

### Community 44 - "test_condition_immunities.py"
Cohesion: 0.14
Nodes (15): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+7 more)

### Community 45 - "TurnResources"
Cohesion: 0.07
Nodes (54): TurnResources, apply_battlerager(), BattleragerFeatures, _de(), SpikedArmorAction, AttackModifiers, _abilities(), _accion_puas() (+46 more)

### Community 46 - "intentar_desenganche"
Cohesion: 0.28
Nodes (3): enganchador_de(), intentar_desenganche(), _ya_cegado_por()

### Community 47 - "CheckResult"
Cohesion: 0.33
Nodes (5): CheckResult, _check_fijo(), _fake(), test_escape_con_exito_elimina_la_condicion(), test_escape_con_fallo_la_condicion_sigue()

### Community 48 - "dnd_sim/__init__.py"
Cohesion: 0.08
Nodes (17): ability_mod(), pick(), sample(), _extract(), first_target_policy(), random_policy(), CombatantType, _accion_utilizable() (+9 more)

### Community 49 - "_duelo"
Cohesion: 0.15
Nodes (17): _ataque(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja(), test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_los_indicadores_estaticos_siguen_funcionando_y_se_combinan(), test_melee_or_ranged_consume_rng_siempre() (+9 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.11
Nodes (25): ability_check(), _data(), _load(), _pj(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_el_escape_se_intenta_al_inicio_del_turno(), test_el_estado_cambia_ataque_a_ataque_en_un_multiataque(), test_el_estado_de_distancia_inicial_y_el_reset() (+17 more)

### Community 51 - "test_loader.py"
Cohesion: 0.16
Nodes (12): _armor_class_value(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper(), test_cache_avoids_second_network(), test_load_monster_maps_ogre() (+4 more)

### Community 52 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 53 - "SpellFixedDamageAction"
Cohesion: 0.14
Nodes (17): SpellFixedDamageAction, _ctx(), _npc(), _pj(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizado_invierte_los_objetivos_de_ataque(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado(), test_el_hechizo_verdadero_es_un_ataque_real_con_dano_extra() (+9 more)

### Community 54 - "parse_escape"
Cohesion: 0.33
Nodes (4): parse_escape(), _skills_for(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 57 - "Combatant"
Cohesion: 0.12
Nodes (7): Arquitectura de `dnd_sim`, Carpetas, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, Combatant

### Community 59 - "test_ancestral_guardian.py"
Cohesion: 0.06
Nodes (46): AncestralGuardianFeatures, apply_ancestral_guardian(), apply_class(), ClassDef, normalize_class_name(), register_class(), SubclassDef, _abilities() (+38 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.12
Nodes (21): _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab(), test_condition_action_de_hechizo_pasa_magical() (+13 more)

### Community 61 - "begin_turn"
Cohesion: 0.27
Nodes (15): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+7 more)

### Community 62 - "_duelo"
Cohesion: 0.31
Nodes (7): _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

### Community 63 - "spell_action"
Cohesion: 0.14
Nodes (13): Paquetes con fachada, Spell, spell_action(), _spell_data(), test_el_hechizo_enlarge_es_un_estado_self(), test_lanzar_el_hechizo_agranda_al_lanzador(), test_un_lanzador_carga_el_hechizo_con_su_uso_propio(), _spell_data() (+5 more)

### Community 64 - "legendary_parser.py"
Cohesion: 0.09
Nodes (15): _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary(), _por_datos() (+7 more)

### Community 65 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 66 - "attack_roll"
Cohesion: 0.09
Nodes (18): _actualizar_distancia(), _agrandado(), _apply_condition_riders(), attack_roll(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque() (+10 more)

### Community 67 - "ConditionEffect"
Cohesion: 0.40
Nodes (3): ConditionEffect, test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), test_un_pj_con_ataque_con_rider_no_aplica_la_condicion_mientras_queden_usos()

### Community 68 - "condition_parser.py"
Cohesion: 0.10
Nodes (8): parse_attach_effects(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), has_escape_text(), AttachOnHitEffect

### Community 69 - "capas.py"
Cohesion: 0.20
Nodes (5): capa_de(), main(), visit_ImportFrom(), modulo_de(), resolver()

### Community 70 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 71 - "test_spells.py"
Cohesion: 0.19
Nodes (11): build_spell_actions(), _desde_fixture(), _monstruo_lanzador(), test_el_lich_carga_sus_hechizos_utiles(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_la_reaccion_gasta_su_uso_propio(), test_los_hechizos_con_uso_limitado_tienen_uso_propio(), test_max_spell_level_limita_el_nivel_cargado() (+3 more)

### Community 72 - "Spellcasting"
Cohesion: 0.16
Nodes (7): parse_spellcasting(), Spellcasting, test_el_lanzador_se_lee_de_los_actions(), test_el_upcast_reescala_el_dano_y_la_curacion(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_la_curacion_usa_el_modificador_de_caracteristica_no_el_bono_completo(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 73 - "RollMode"
Cohesion: 0.12
Nodes (9): RollMode, _resolve_mods(), check_modifiers(), CheckModifiers, _condiciones(), _hooks(), _instancias(), _RasgoDePrueba (+1 more)

### Community 74 - "test_azer.py"
Cohesion: 0.23
Nodes (18): HeatedBody, _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), _rasgo() (+10 more)

### Community 75 - "race_parser.py"
Cohesion: 0.15
Nodes (9): parse_race(), _skill_name(), _spells_from_description(), _trait_skills(), _keen_senses(), test_parse_competencias_fijas_de_la_raza(), test_parse_descripcion_sin_hechizos_da_vacio(), test_parse_elfo_linaje_hechizos_sin_duplicados() (+1 more)

### Community 76 - "pathlib"
Cohesion: 0.19
Nodes (6): Cómo comprobar que todo sigue en orden, _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api()

### Community 77 - "PlayerCharacter"
Cohesion: 0.22
Nodes (13): Race, PlayerCharacter, _abilities(), _fiendish_legacy(), _pj(), test_apply_race_añade_competencias_fijas(), test_apply_race_con_habilidad_pedida(), test_apply_race_habilidad_fuera_de_las_opciones_es_error() (+5 more)

### Community 78 - "run_combat"
Cohesion: 0.21
Nodes (13): run_combat(), _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno() (+5 more)

### Community 80 - "apply_condition"
Cohesion: 0.12
Nodes (20): apply_condition(), _as_condition(), attempt_escapes(), _condicion_bloqueada(), _contar(), EscapeCheck, _label(), _queda_accion() (+12 more)

### Community 82 - "load_race"
Cohesion: 0.33
Nodes (5): load_race(), test_load_race_descarga_la_raza_y_sus_rasgos(), _rasgo(), _raza(), test_load_race_propaga_el_error_de_la_api()

### Community 83 - "spells/__init__.py"
Cohesion: 0.11
Nodes (7): SpellAttackAction, dado_por_nivel(), duracion_en_rondas(), apply_concentration(), HealEffect, _contexto_de_reaccion(), trigger_reaction()

### Community 84 - "_hooks"
Cohesion: 0.38
Nodes (3): _hooks(), _mitigacion_de_otros(), _salvar_a_cero()

### Community 85 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.33
Nodes (5): Bloque 2026-10-30 (commiteado), Grafo y verificación, Rutina sugerida al abrir sesión, TODO — DnDBalancer / dnd_sim, TODOs en código (marcados `# TODO`)

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `loader.py`, `test_attach.py`, `test_berserker.py`, `ActionType`, `test_enlarge.py`, `load_monster`, `test_legendary.py`, `test_beast.py`, `parse_spell`, `test_traits.py`, `Condition`, `test_utility.py`, `main.py`, `Abilities`, `berserker.py`, `barbarian/__init__.py`, `test_death.py`, `test_parry.py`, `inflict_damage`, `test_proficiency.py`, `test_conditions.py`, `model/actions.py`, `TurnResources`, `dnd_sim/__init__.py`, `_duelo`, `test_checks_escapes.py`, `test_pack_tactics.py`, `SpellFixedDamageAction`, `Combatant`, `test_ancestral_guardian.py`, `test_magic_resistance.py`, `begin_turn`, `_duelo`, `spell_action`, `legendary_parser.py`, `attack_roll`, `ConditionEffect`, `test_undead_fortitude.py`, `test_spells.py`, `test_azer.py`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `UnknownUsageError` and `ActionType`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `loader.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07816091954022988 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `loader.py`, `test_attach.py`, `test_berserker.py`, `test_enlarge.py`, `test_legendary.py`, `test_beast.py`, `parse_spell`, `test_traits.py`, `test_utility.py`, `spell_parser.py`, `DamageTransfer`, `Abilities`, `BarbarianFeatures`, `berserker.py`, `barbarian/__init__.py`, `saves.py`, `traits/__init__.py`, `test_parry.py`, `test_skills.py`, `test_lair.py`, `test_proficiency.py`, `saving_throw`, `test_conditions.py`, `model/actions.py`, `test_condition_immunities.py`, `intentar_desenganche`, `dnd_sim/__init__.py`, `test_checks_escapes.py`, `test_pack_tactics.py`, `SpellFixedDamageAction`, `Combatant`, `test_magic_resistance.py`, `spell_action`, `attack_roll`, `condition_parser.py`, `test_spells.py`, `RollMode`, `apply_condition`, `spells/__init__.py`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `AttackRange`) actually correct?**
  _`Attack` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Should `ActionType` be split into smaller, more focused modules?**
  _Cohesion score 0.05154639175257732 - nodes in this community are weakly interconnected._
- **Why does `apply_condition()` connect `apply_condition` to `test_attach.py`, `test_berserker.py`, `ActionType`, `test_enlarge.py`, `test_legendary.py`, `test_beast.py`, `test_traits.py`, `Condition`, `test_utility.py`, `Abilities`, `CombatContext`, `berserker.py`, `saves.py`, `test_parry.py`, `test_skills.py`, `test_lair.py`, `legendary_phase`, `test_conditions.py`, `model/actions.py`, `test_condition_immunities.py`, `intentar_desenganche`, `CheckResult`, `dnd_sim/__init__.py`, `_duelo`, `test_checks_escapes.py`, `test_pack_tactics.py`, `SpellFixedDamageAction`, `_duelo`, `attack_roll`, `test_spells.py`, `spells/__init__.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
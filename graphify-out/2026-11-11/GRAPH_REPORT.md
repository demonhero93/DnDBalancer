# Graph Report - DnDBalancer  (2026-11-10)

## Corpus Check
- 225 files · ~203,284 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 3825 nodes · 13931 edges · 123 communities (107 shown, 16 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 922 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f1130584`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_fighter.py
- test_attach.py
- AttackRange
- test_giant.py
- test_world_tree.py
- test_wild_heart.py
- test_proficiency.py
- test_legendary.py
- test_beast.py
- test_spells.py
- test_traits.py
- _arquero
- test_utility.py
- test_wild_magic.py
- spell_parser.py
- _trait
- test_battle_master.py
- _ejecuta
- test_loader_actions.py
- Any
- ArcaneArcherFeatures
- ActionUsage
- apply_barbarian
- test_martial_advantage.py
- ZealotFeatures
- test_zealot.py
- test_death.py
- Monster
- load_monster
- test_parry.py
- test_superior_invisibility.py
- FighterFeatures
- _ExplotaSiUsaRng
- test_skills.py
- test_undead_fortitude.py
- test_arcane_archer.py
- run_combat
- dnd_sim/__init__.py
- test_relentless.py
- test_mastery.py
- BarbarianFeatures
- apply_condition
- Trait
- test_area.py
- TurnResources
- Condition
- BattleMasterFeatures
- _atacado
- main.py
- test_checks_escapes.py
- test_loader.py
- _con_estilo
- Any
- test_condition_immunities.py
- hooks
- simulate
- Abilities
- begin_turn
- parse_usage
- traits/__init__.py
- loader.py
- test_storm_herald.py
- roll_modifiers.py
- test_backgrounds.py
- _pj
- apply_fighter
- legendary_phase
- ability_check
- GiantFeatures
- test_pack_tactics.py
- test_lair.py
- ConditionInstance
- api_client.py
- test_races.py
- test_enlarge.py
- Spellcasting
- Any
- test_usage.py
- .alive
- pick
- PlayerCharacter
- build_spell_actions
- _RngMax
- test_azer.py
- _zeal
- test_extra_damage.py
- AtaqueSustituido
- _RngSi
- inflict_damage
- test_ancestral_guardian.py
- race_parser.py
- SaveDamage
- pathlib
- _clamp
- parse_traits
- SaveResult
- barbarian/__init__.py
- _RngExplota
- test_el_gancho_after_failed_check_desde_ability_check_con_ctx
- Arquitectura de `dnd_sim`
- _FixedRandom
- .enfeeble_mitiga
- Attack
- background_parser.py
- attack_roll
- normalize_skill
- roll_initiative
- spells/__init__.py
- .sustituir_ataque
- load_race
- Any
- DamageRecorder
- test_piercing_k_uniforme_y_atacante_nunca_es_objetivo
- test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque
- test_tactical_master_nivel_9_elige_entre_original_push_sap_slow
- _estado
- test_sustitucion_hace_un_solo_par_de_picks
- test_resistance_probability_medio_convierte_about_50_por_ciento
- test_el_cli_tiene_las_opciones_legendarias

## God Nodes (most connected - your core abstractions)
1. `Attack` - 236 edges
2. `Condition` - 182 edges
3. `Monster` - 181 edges
4. `AttackRange` - 176 edges
5. `attack_roll()` - 164 edges
6. `apply_condition()` - 154 edges
7. `Abilities` - 151 edges
8. `load_monster()` - 136 edges
9. `PlayerCharacter` - 134 edges
10. `pick()` - 107 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Battle Master: plan de sesión 1` --references--> `CombatState`  [INFERRED]
  TODO.md → dnd_sim/core/combat_state.py
- `Arcane Archer (XGE)` --references--> `roll_dice()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/dice.py

## Import Cycles
- None detected.

## Communities (123 total, 16 thin omitted)

### Community 0 - "test_fighter.py"
Cohesion: 0.13
Nodes (16): second_wind_uses(), _action_surge(), _ctx_recursos(), _RngBajo, _second_wind(), test_action_surge_como_maximo_un_vez_por_turno(), test_action_surge_ejecutada_restaura_la_accion_y_gasta_un_uso(), test_action_surge_no_es_elegible_si_la_accion_no_se_ha_gastado() (+8 more)

### Community 1 - "test_attach.py"
Cohesion: 0.15
Nodes (27): AttachOnHitEffect, enganchador_de(), _atacar(), _bite(), _cloaker(), _ctx(), _datos(), _pj() (+19 more)

### Community 2 - "AttackRange"
Cohesion: 0.07
Nodes (56): AttackRange, RageAction, apply_berserker(), BerserkerFeatures, _de(), _furia_de(), _golpe_sin_armas(), IntimidatingPresenceAction (+48 more)

### Community 3 - "test_giant.py"
Cohesion: 0.13
Nodes (33): apply_giant(), MightyImpelAction, _abilities(), _barbaro(), _ctx(), _furia(), _giant(), _mon() (+25 more)

### Community 4 - "test_world_tree.py"
Cohesion: 0.09
Nodes (41): apply_world_tree(), _de(), WorldTreeFeatures, _abilities(), _aliado(), _barbaro(), _ctx(), _decision() (+33 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.08
Nodes (49): apply_wild_heart(), _con_beneficio(), _de(), _en_5_pies(), _hostil(), _orden_de(), WildHeartFeatures, _abilities() (+41 more)

### Community 6 - "test_proficiency.py"
Cohesion: 0.18
Nodes (20): ability_check_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia() (+12 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.12
Nodes (28): _data(), _legendaria(), _load(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_el_ala_que_mezcla_movimiento_avisa(), test_el_cantrip_del_lich_se_omite_con_aviso(), test_el_detect_del_dragon_se_omite_con_aviso() (+20 more)

### Community 8 - "test_beast.py"
Cohesion: 0.05
Nodes (71): WeaponAttackAction, apply_beast(), BeastFeatures, CallTheHuntBonus, FormOfTheBeast, _habilitar_armas_naturales(), _abilities(), _barb() (+63 more)

### Community 9 - "test_spells.py"
Cohesion: 0.12
Nodes (39): parse_spell(), spell_action(), _ctx(), _npc(), _pj(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion() (+31 more)

### Community 10 - "test_traits.py"
Cohesion: 0.09
Nodes (26): BloodFrenzy, _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _RasgoDeSalvacion, _sahuagin() (+18 more)

### Community 11 - "_arquero"
Cohesion: 0.10
Nodes (31): _arco(), _arquero(), _ctx_curving(), _curving(), _RngExplota, _RngNo, test_accion_curving_se_anade_desde_el_nivel_7(), test_arcane_shot_crea_usos_por_nivel() (+23 more)

### Community 12 - "test_utility.py"
Cohesion: 0.13
Nodes (29): _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), hay_utilitaria_accion(), _orden_tamano(), _abilities(), _ctx() (+21 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.12
Nodes (39): apply_wild_magic(), _abilities(), _barbaro(), _con_cola(), _con_efecto(), espia(), _ctx(), _furia() (+31 more)

### Community 15 - "spell_parser.py"
Cohesion: 0.07
Nodes (16): Paquetes con fachada, _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla() (+8 more)

### Community 16 - "_trait"
Cohesion: 0.16
Nodes (31): _check_fallada(), _ctx(), _fighter(), _objetivo(), _save_fallada(), _saving_nueva(), test_action_surge_no_existe_en_nivel_1(), test_ataques_estudiados_caduca_al_final_del_siguiente_turno() (+23 more)

### Community 17 - "test_battle_master.py"
Cohesion: 0.08
Nodes (41): maneuvers_known_count(), superiority_dice_count(), superiority_die_sides(), apply_battle_master(), _abilities(), _atacado_dos_enemigos(), _atacado_fijo(), _bm() (+33 more)

### Community 18 - "_ejecuta"
Cohesion: 0.14
Nodes (18): _ejecuta(), _mods(), _RngFalla, test_disarming_attack_no_altera_el_combate_mas_que_el_dano(), test_distracting_da_ventaja_a_un_tercero_y_se_consume(), test_distracting_no_concede_ventaja_si_ya_caduco(), test_distracting_no_da_ventaja_al_marcador_ni_se_consume(), test_efectos_sin_implementacion_no_alteran_el_combate() (+10 more)

### Community 19 - "test_loader_actions.py"
Cohesion: 0.18
Nodes (13): _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga(), test_ataque_con_usage_conserva_el_actionusage() (+5 more)

### Community 20 - "Any"
Cohesion: 0.17
Nodes (6): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _presupuesto()

### Community 21 - "ArcaneArcherFeatures"
Cohesion: 0.08
Nodes (6): ArcaneArcherFeatures, _ctx_con_rng(), _CtxConRng, CurvingShotAction, _de(), _otros_enemigos()

### Community 22 - "ActionUsage"
Cohesion: 0.15
Nodes (10): ActionUsage, UsageKind, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar(), test_per_day_dos_usos_y_luego_can_use_falso(), test_per_day_reset_restaura_todos_los_usos(), test_recharge_5_6_porcentaje_de_exito(), test_recharge_mientras_esta_cargada_no_consume_rng() (+2 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.08
Nodes (53): extra_attacks_for(), rage_uses(), apply_barbarian(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj() (+45 more)

### Community 24 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 25 - "ZealotFeatures"
Cohesion: 0.09
Nodes (8): _de(), _en_60_pies(), _es_aliado(), _furia_de(), ZealotFeatures, test_apply_class_por_clave_aplica_zealot(), test_clave_de_registro_zealot_en_barbarian(), _trait()

### Community 26 - "test_zealot.py"
Cohesion: 0.11
Nodes (34): _abilities(), _aliado(), _decision(), _fallos(), _forma(), _guarda_con(), _presencia(), test_fanatical_decision_negativa_no_repiten() (+26 more)

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 28 - "Monster"
Cohesion: 0.09
Nodes (35): Monster, _abilities(), _disparo(), _RngFalla, _RngSi, test_arcane_shot_se_aplica_una_sola_vez_por_turno(), test_arcane_shot_se_gasta_un_uso_al_aplicar(), test_banishing_arrow_falla_la_salvacion_y_deja_incapacitado() (+27 more)

### Community 29 - "load_monster"
Cohesion: 0.06
Nodes (35): get_spell(), load_monster(), _norm_name(), _tag_modificadores(), test_una_condicion_desconocida_de_la_api_avisa(), test_fixture_sintetica_carga(), test_monstruo_no_legendario_no_carga_guaridas(), test_monstruo_sin_fichero_no_avisa() (+27 more)

### Community 30 - "test_parry.py"
Cohesion: 0.27
Nodes (20): _arquero_parry(), _ataque(), _ctx(), _datos(), _fijar_d20(), espia(), _gladiador(), _pj() (+12 more)

### Community 31 - "test_superior_invisibility.py"
Cohesion: 0.36
Nodes (11): _accion(), _ctx(), _pixie(), _pj(), test_atacar_con_ventaja_y_no_pierde_la_invisibilidad(), test_ejecutarla_aplica_el_estado(), test_el_monstruo_recibe_su_accion_al_construirse(), test_lanzar_un_hechizo_tampoco_la_pierde() (+3 more)

### Community 32 - "FighterFeatures"
Cohesion: 0.06
Nodes (10): ActionSurgeAction, _contexto(), _en_5_pies(), FighterFeatures, _rasgo(), SecondWindAction, _aliados(), BattleMasterRallyAction (+2 more)

### Community 33 - "_ExplotaSiUsaRng"
Cohesion: 0.13
Nodes (25): _accion_rally(), _commanda(), _ExplotaSiUsaRng, _ripostea_directa(), _sustituye(), test_commanders_strike_cede_el_ataque_si_hay_feinting_encolado(), test_commanders_strike_no_se_decide_si_el_aliado_no_tiene_armas(), test_commanders_strike_no_se_decide_si_el_aliado_ya_uso_su_reaccion() (+17 more)

### Community 34 - "test_skills.py"
Cohesion: 0.13
Nodes (22): _abilities(), _ctx(), _load_fixture(), _pj(), _SoloMod, test_ability_check_no_suma_competencia_de_habilidad(), test_attempt_escapes_tira_la_habilidad(), test_check_modifiers_pasa_la_habilidad_a_los_rasgos() (+14 more)

### Community 35 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 36 - "test_arcane_archer.py"
Cohesion: 0.11
Nodes (21): arcane_shot_options_known(), arcane_shot_uses(), apply_arcane_archer(), _firmas(), _pj(), test_apply_arcane_archer_exige_la_clase_fighter(), test_apply_class_equivalente_a_apply_arcane_archer(), test_arcane_archer_lore_da_competencia() (+13 more)

### Community 37 - "run_combat"
Cohesion: 0.18
Nodes (14): run_combat(), _summarize_damage(), _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso() (+6 more)

### Community 38 - "dnd_sim/__init__.py"
Cohesion: 0.05
Nodes (12): ability_mod(), normalize_ability(), proficiency_bonus(), resolve_roll_mode(), _extract(), first_target_policy(), random_policy(), MultiattackAction (+4 more)

### Community 39 - "test_relentless.py"
Cohesion: 0.27
Nodes (12): _ctx(), _datos(), _jabali(), _pj(), test_el_jabali_carga_su_relentless_con_umbral_y_uso(), test_relentless_no_necesita_contexto_ni_rng(), test_reset_reestablece_el_umbral_y_los_usos(), test_solo_puede_salvarse_una_vez_por_combate() (+4 more)

### Community 40 - "test_mastery.py"
Cohesion: 0.09
Nodes (29): al_acertar(), al_fallar(), _cd_topple(), consumir_marcas(), _log(), _nombre(), resolver_maestria(), _arma() (+21 more)

### Community 41 - "BarbarianFeatures"
Cohesion: 0.10
Nodes (5): BarbarianFeatures, ExtendRageAction, _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 42 - "apply_condition"
Cohesion: 0.08
Nodes (56): parse_range_type(), apply_condition(), end_turn(), resolve_attack_range(), _ataque(), _ctx(), _data(), _duelo() (+48 more)

### Community 43 - "Trait"
Cohesion: 0.05
Nodes (32): rage_damage(), d20(), roll_d20(), roll_dice(), DamageType, parse_damage_type(), log_line(), sample() (+24 more)

### Community 44 - "test_area.py"
Cohesion: 0.12
Nodes (27): AreaTargeting, select_area_targets(), _default_targeting(), _area_action(), _ctx(), _npc(), _pj(), _save_forzado() (+19 more)

### Community 45 - "TurnResources"
Cohesion: 0.07
Nodes (55): TurnResources, apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), SpikedArmorAction, AttackModifiers, _abilities() (+47 more)

### Community 46 - "Condition"
Cohesion: 0.18
Nodes (27): Condition, attack_modifiers(), test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar() (+19 more)

### Community 47 - "BattleMasterFeatures"
Cohesion: 0.10
Nodes (5): Battle Master (PHB 2024), _armas_melee_propias(), BattleMasterFeatures, _orden_tamano(), Battle Master: plan de sesión 2

### Community 48 - "_atacado"
Cohesion: 0.14
Nodes (22): _atacado(), _conoce_sweeping(), _decide(), _RngIdx, test_el_ataque_de_reaccion_no_activa_maniobras_de_sesion_1(), test_el_uso_no_se_gasta_si_no_se_ejecuta(), test_en_un_fallo_sin_precision_cero_rng(), test_feinting_sin_impacto_no_gasta_el_dado() (+14 more)

### Community 49 - "main.py"
Cohesion: 0.10
Nodes (23): CLI del simulador: `build_parser()`, Detalle por flag, Ejemplos, Flujo de `main()`, `--legendary-p`, `--legendary-points`, `--monster` / `-m`, Observaciones (para humanos y IA) (+15 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.06
Nodes (48): has_escape_text(), parse_escape(), _skills_for(), attempt_escapes(), EscapeCheck, _ataque(), _check_fijo(), _ctx() (+40 more)

### Community 51 - "test_loader.py"
Cohesion: 0.16
Nodes (12): _armor_class_value(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper(), test_cache_avoids_second_network(), test_load_monster_maps_ogre() (+4 more)

### Community 52 - "_con_estilo"
Cohesion: 0.23
Nodes (16): _aliado(), _con_estilo(), _enemigo(), _mods(), _RngSi, test_interception_con_un_aliado_no_baja_de_cero_el_daño(), test_interception_no_actúa_con_la_reacción_gastada(), test_interception_no_actúa_contra_un_no_aliado_ni_con_el_mismo_pj() (+8 more)

### Community 53 - "Any"
Cohesion: 0.10
Nodes (6): _cd(), _de(), _en_30_pies(), _enemigos(), WildMagicFeatures, WildSurgeAction

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.13
Nodes (15): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+7 more)

### Community 57 - "hooks"
Cohesion: 0.06
Nodes (22): _agrandado(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), daño_base_arma(), _decidir_maniobra(), _piso_dados_rasgos() (+14 more)

### Community 59 - "simulate"
Cohesion: 0.29
Nodes (4): simulate(), test_con_use_probability_uno_el_danio_es_mayor_que_con_cero(), test_el_dragon_contra_un_grupo_usa_acciones_legendarias(), test_reproducibilidad_con_leyendas_y_resistencia()

### Community 60 - "Abilities"
Cohesion: 0.10
Nodes (24): Abilities, ConditionEffect, test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting() (+16 more)

### Community 61 - "begin_turn"
Cohesion: 0.30
Nodes (14): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+6 more)

### Community 62 - "parse_usage"
Cohesion: 0.16
Nodes (7): _declara_uso(), _usage(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 63 - "traits/__init__.py"
Cohesion: 0.04
Nodes (16): DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante(), aliados_capaces(), _condicion_posicional() (+8 more)

### Community 64 - "loader.py"
Cohesion: 0.04
Nodes (36): is_area_action(), parse_attach_effects(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), _coincide_nombre() (+28 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.12
Nodes (40): apply_storm_herald(), _abilities(), _aliado(), _barbaro(), _ctx(), _fijar_fallo_reaccion(), falla(), _fijar_salvacion() (+32 more)

### Community 66 - "roll_modifiers.py"
Cohesion: 0.11
Nodes (14): _condiciones(), effective_ac(), _hooks(), _instancias(), save_modifiers(), test_la_ca_efectiva_sube_dos_a_distancia(), _datos(), _lich() (+6 more)

### Community 67 - "test_backgrounds.py"
Cohesion: 0.16
Nodes (17): Background, load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes(), test_apply_background_sin_competencias_es_inofensivo() (+9 more)

### Community 68 - "_pj"
Cohesion: 0.22
Nodes (19): espia(), _espiar_divine(), _furia(), _mon(), _pj(), test_determinismo_misma_semilla_mismos_resultados(), corrida(), test_divine_fury_elige_radiante_con_pick() (+11 more)

### Community 69 - "apply_fighter"
Cohesion: 0.08
Nodes (35): apply_fighter(), maestria_de(), _abilities(), _firmas(), _pj(), _pj_con_armas(), test_apply_class_fighter_sin_subclase_equivalente_a_apply_fighter(), test_apply_class_reenvía_el_estilo_de_combate() (+27 more)

### Community 70 - "legendary_phase"
Cohesion: 0.17
Nodes (22): legendary_phase(), _contexto(), _pj(), test_con_una_sola_accion_asequible_pick_no_consume_rng(), test_dos_duenos_legendarios_actuan_cada_uno_una_vez(), test_el_combate_termina_en_medio_de_la_fase(), test_la_fase_ocurre_despues_del_end_turn(), test_no_actua_si_el_combate_ya_terminado() (+14 more)

### Community 71 - "ability_check"
Cohesion: 0.14
Nodes (12): skill_ability(), ability_check(), _avisar_fallo_prueba(), CheckResult, _finish_check(), _guia(), _resolve_mods(), skill_bonus() (+4 more)

### Community 72 - "GiantFeatures"
Cohesion: 0.16
Nodes (4): _de(), GiantFeatures, _objetivos_impel(), _orden_de()

### Community 73 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 74 - "test_lair.py"
Cohesion: 0.07
Nodes (32): load_lair(), lair_phase(), LairAction, LegendaryState, _ctx(), _dragon(), _enemigo(), lairs_dir() (+24 more)

### Community 75 - "ConditionInstance"
Cohesion: 0.22
Nodes (3): ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 76 - "api_client.py"
Cohesion: 0.15
Nodes (8): _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_trait(), MonsterNotFoundError, NetworkError

### Community 77 - "test_races.py"
Cohesion: 0.15
Nodes (18): Race, parse_race(), _abilities(), _fiendish_legacy(), _keen_senses(), _pj(), test_apply_race_añade_competencias_fijas(), test_apply_race_con_habilidad_pedida() (+10 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.14
Nodes (25): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+17 more)

### Community 79 - "Spellcasting"
Cohesion: 0.15
Nodes (7): parse_spellcasting(), Spellcasting, test_el_lanzador_se_lee_de_los_actions(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_la_curacion_usa_el_modificador_de_caracteristica_no_el_bono_completo(), test_un_hechizo_de_accion_bonus_se_comprueba_en_su_fase(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 80 - "Any"
Cohesion: 0.18
Nodes (6): _as_condition(), _condicion_bloqueada(), _contar(), _label(), _queda_accion(), remove_condition()

### Community 81 - "test_usage.py"
Cohesion: 0.26
Nodes (10): _eventos(), _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(), test_copias_de_un_monstruo_tienen_estado_independiente(), test_dos_combates_seguidos_empiezan_con_el_aliento_cargado(), test_dragon_nunca_usa_el_aliento_dos_turnos_seguidos_sin_recarga(), test_politica_elige_el_aliento_aproximadamente_el_50_cuando_esta_cargado() (+2 more)

### Community 82 - ".alive"
Cohesion: 0.05
Nodes (14): _armas_melee_de(), _aliados_en_aura(), _cd(), _dado_mar(), _de(), _en_aura(), _enemigos_en_aura(), _escalado() (+6 more)

### Community 83 - "pick"
Cohesion: 0.05
Nodes (32): CombatState, pick(), combat_finished(), living_teams(), _objetivo_enganche(), valid_targets(), _reaccion_si_procede(), CombatResult (+24 more)

### Community 84 - "PlayerCharacter"
Cohesion: 0.10
Nodes (23): PlayerCharacter, apply_damage_modifiers(), _is_petrified(), test_sin_condiciones_el_dano_no_cambia(), _guerrero_y_ogro(), _target(), test_attack_roll_log_modifier(), test_danio_medio_por_combatiente_y_equipo() (+15 more)

### Community 85 - "build_spell_actions"
Cohesion: 0.29
Nodes (8): build_spell_actions(), _desde_fixture(), _monstruo_lanzador(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_la_reaccion_gasta_su_uso_propio(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_uso_propio(), test_un_hechizo_a_voluntad_se_puede_lanzar_en_cada_turno()

### Community 87 - "test_azer.py"
Cohesion: 0.26
Nodes (17): _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), _rasgo(), test_ataque_a_distancia_no_dispara_la_represalia() (+9 more)

### Community 88 - "_zeal"
Cohesion: 0.23
Nodes (16): _accion(), _barbaro(), _ctx(), test_after_failed_save_sin_zealot_devuelve_el_mismo_resultado(), test_fanatical_no_activo_sin_furia(), test_nivel_3_no_recibe_rasgos_superiores(), test_warrior_curacion_gasta_un_dado_y_suma_pv(), test_warrior_curacion_no_supera_el_maximo() (+8 more)

### Community 89 - "test_extra_damage.py"
Cohesion: 0.23
Nodes (17): _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional(), test_ataque_sin_extra_no_llama_al_bucle() (+9 more)

### Community 90 - "AtaqueSustituido"
Cohesion: 0.16
Nodes (11): _sustituir_ataque(), AtaqueSustituido, _abilities(), _blanco(), _pj(), _RasgoQueSustituye, _RasgoSinSustitucion, _RngExplota (+3 more)

### Community 91 - "_RngSi"
Cohesion: 0.09
Nodes (19): _accion_feinting(), _parry(), _RngNo, _RngSi, test_feinting_encola_la_ventaja_y_el_dado_si_impacta(), test_feinting_es_elegible_con_bonus_libre_y_decision_aleatoria(), test_feinting_sin_datos_es_inelegible_sin_rng(), test_goading_attack_no_marca_si_pasa_la_salvacion() (+11 more)

### Community 92 - "inflict_damage"
Cohesion: 0.17
Nodes (8): _absorber_pv_temporales(), _hooks(), inflict_damage(), _mark_dead_if_down(), _mitigacion_de_otros(), _notify_damage_dealt(), _salvar_a_cero(), test_inflict_damage_registra_la_bandera_magical()

### Community 93 - "test_ancestral_guardian.py"
Cohesion: 0.06
Nodes (47): AncestralGuardianFeatures, apply_ancestral_guardian(), apply_class(), ClassDef, normalize_class_name(), register_class(), SubclassDef, _abilities() (+39 more)

### Community 94 - "race_parser.py"
Cohesion: 0.20
Nodes (3): _skill_name(), _spells_from_description(), _trait_skills()

### Community 95 - "SaveDamage"
Cohesion: 0.10
Nodes (13): _check_fields(), _construir(), _error(), SaveAction, AreaSaveAction, _log_target(), ConditionAction, RepeatSave (+5 more)

### Community 96 - "pathlib"
Cohesion: 0.21
Nodes (5): _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api()

### Community 97 - "_clamp"
Cohesion: 0.15
Nodes (9): action_surge_uses(), _clamp(), fighter_extra_attacks_for(), indomitable_uses(), weapon_mastery_count(), test_action_surge_usos_por_nivel_son_1_y_2(), test_indomitable_usos_por_nivel_son_1_2_y_3(), test_los_golpes_del_guerrero_suben_en_5_11_y_20() (+1 more)

### Community 98 - "parse_traits"
Cohesion: 0.22
Nodes (7): _entradas(), parse_traits(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd(), test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad(), test_el_umbral_se_saca_de_cada_descripcion(), test_el_rasgo_se_parsea_desde_el_srd(), test_parse_traits_ignora_entradas_malformadas()

### Community 99 - "SaveResult"
Cohesion: 0.48
Nodes (7): SaveResult, stub(), stub(), stub(), test_revivificacion_no_roba_el_gasto_de_furia_inaguantable(), falla(), salva()

### Community 100 - "barbarian/__init__.py"
Cohesion: 0.14
Nodes (7): NaturalWeapon, apply_zealot(), _reserva_dados(), WarriorHealAction, ZealousPresenceAction, test_apply_anade_trait_y_dos_acciones_bonus(), test_apply_requiere_clase_barbara()

### Community 101 - "_RngExplota"
Cohesion: 0.25
Nodes (4): _RngExplota, test_interception_sin_arma_ni_escudo_no_actúa_y_no_consume_rng(), test_resolver_maestria_sin_maestria_no_consulta_tactical_master(), test_tactical_master_no_sustituye_bajo_el_nivel_9()

### Community 103 - "Arquitectura de `dnd_sim`"
Cohesion: 0.17
Nodes (10): Arcane Archer (XGE), Arquitectura de `dnd_sim`, Carpetas, Cómo comprobar que todo sigue en orden, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia (+2 more)

### Community 104 - "_FixedRandom"
Cohesion: 0.20
Nodes (5): _breath(), _FixedRandom, test_begin_turn_no_tira_nada_si_estan_cargadas(), test_begin_turn_reinicia_recursos_y_tira_una_recarga_por_accion(), test_per_day_no_tira_recarga()

### Community 106 - "Attack"
Cohesion: 0.17
Nodes (24): D20Result, RollMode, Attack, test_commanders_strike_con_relentless_no_gasta_dado(), test_commanders_strike_el_dueño_nunca_es_el_aliado_elegido(), test_commanders_strike_sustituye_el_ataque_y_el_aliado_gasta_su_reaccion(), _d20(), test_el_ataque_del_aliado_no_reentra_en_commanders_strike() (+16 more)

### Community 108 - "attack_roll"
Cohesion: 0.20
Nodes (3): _actualizar_distancia(), attack_roll(), _mode_tag()

### Community 109 - "normalize_skill"
Cohesion: 0.28
Nodes (4): _clean(), normalize_skill(), test_normalize_skill_acepta_espacios_y_spanish(), test_normalize_skill_desconocida_lanza_value_error()

### Community 110 - "roll_initiative"
Cohesion: 0.36
Nodes (8): roll_initiative(), _d20_fijo(), test_ambush_con_la_decision_no_no_gasta_nada(), test_ambush_con_relentless_no_gasta_dado(), test_ambush_sin_dados_no_consume_rng(), test_ambush_sin_la_maniobra_no_consume_rng(), test_ambush_suma_un_dado_a_la_tirada_de_iniciativa(), test_sin_subclase_roll_initiative_no_consulta_bonus()

### Community 111 - "spells/__init__.py"
Cohesion: 0.11
Nodes (8): SpellFixedDamageAction, dado_por_nivel(), duracion_en_rondas(), apply_concentration(), HealEffect, StateEffect, test_el_proyectil_magico_pasa_por_los_modificadores_de_dano(), lanzar()

### Community 112 - ".sustituir_ataque"
Cohesion: 0.25
Nodes (3): _aliados_elegibles(), _armas_propias(), _notify_damage_taken()

### Community 113 - "load_race"
Cohesion: 0.33
Nodes (5): load_race(), test_load_race_descarga_la_raza_y_sus_rasgos(), _rasgo(), _raza(), test_load_race_propaga_el_error_de_la_api()

### Community 119 - "_estado"
Cohesion: 0.50
Nodes (3): _estado(), test_el_estado_legendario_rellena_gasta_y_reinicia(), test_use_probability_medio_se_usa_about_50_por_ciento()

## Knowledge Gaps
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `test_fighter.py`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `test_traits.py`, `_arquero`, `test_utility.py`, `test_wild_magic.py`, `_trait`, `test_battle_master.py`, `_ejecuta`, `apply_barbarian`, `test_zealot.py`, `test_death.py`, `Monster`, `load_monster`, `test_parry.py`, `test_superior_invisibility.py`, `_ExplotaSiUsaRng`, `test_undead_fortitude.py`, `test_arcane_archer.py`, `dnd_sim/__init__.py`, `test_relentless.py`, `test_mastery.py`, `apply_condition`, `Trait`, `TurnResources`, `Condition`, `_atacado`, `main.py`, `test_checks_escapes.py`, `hooks`, `Abilities`, `begin_turn`, `loader.py`, `test_storm_herald.py`, `_pj`, `apply_fighter`, `test_pack_tactics.py`, `test_enlarge.py`, `pick`, `PlayerCharacter`, `test_azer.py`, `test_extra_damage.py`, `AtaqueSustituido`, `_RngSi`, `test_ancestral_guardian.py`, `SaveDamage`, `barbarian/__init__.py`, `_RngExplota`, `attack_roll`, `test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque`, `test_sustitucion_hace_un_solo_par_de_picks`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `daño_base_arma()`) actually correct?**
  _`Attack` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_fighter.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12923076923076923 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `test_traits.py`, `test_utility.py`, `spell_parser.py`, `test_battle_master.py`, `_ejecuta`, `ArcaneArcherFeatures`, `Monster`, `test_parry.py`, `test_superior_invisibility.py`, `test_skills.py`, `test_arcane_archer.py`, `dnd_sim/__init__.py`, `test_mastery.py`, `BarbarianFeatures`, `apply_condition`, `Trait`, `BattleMasterFeatures`, `test_checks_escapes.py`, `test_condition_immunities.py`, `hooks`, `Abilities`, `traits/__init__.py`, `loader.py`, `test_storm_herald.py`, `roll_modifiers.py`, `ability_check`, `GiantFeatures`, `test_pack_tactics.py`, `test_lair.py`, `ConditionInstance`, `test_enlarge.py`, `Any`, `.alive`, `pick`, `PlayerCharacter`, `Attack`, `spells/__init__.py`, `Any`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Are the 119 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 119 INFERRED edges - model-reasoned connections that need verification._
- **Should `AttackRange` be split into smaller, more focused modules?**
  _Cohesion score 0.07110398289227479 - nodes in this community are weakly interconnected._
- **Why does `Monster` connect `Monster` to `test_fighter.py`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `test_traits.py`, `_arquero`, `test_utility.py`, `test_wild_magic.py`, `test_battle_master.py`, `_ejecuta`, `test_martial_advantage.py`, `test_zealot.py`, `test_death.py`, `load_monster`, `test_parry.py`, `test_superior_invisibility.py`, `_ExplotaSiUsaRng`, `test_undead_fortitude.py`, `test_arcane_archer.py`, `dnd_sim/__init__.py`, `test_relentless.py`, `test_mastery.py`, `apply_condition`, `test_area.py`, `TurnResources`, `Condition`, `_atacado`, `test_checks_escapes.py`, `test_condition_immunities.py`, `Abilities`, `loader.py`, `test_storm_herald.py`, `_pj`, `apply_fighter`, `test_pack_tactics.py`, `test_lair.py`, `test_enlarge.py`, `pick`, `PlayerCharacter`, `build_spell_actions`, `test_azer.py`, `AtaqueSustituido`, `_RngSi`, `inflict_damage`, `test_ancestral_guardian.py`, `Arquitectura de `dnd_sim``, `Attack`, `roll_initiative`, `test_piercing_k_uniforme_y_atacante_nunca_es_objetivo`, `test_sustitucion_hace_un_solo_par_de_picks`, `test_resistance_probability_medio_convierte_about_50_por_ciento`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
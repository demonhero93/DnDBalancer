# Graph Report - DnDBalancer  (2026-11-14)

## Corpus Check
- 233 files · ~245,954 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 4538 nodes · 16593 edges · 142 communities (129 shown, 13 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 1257 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c6f88cd2`
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
- spell_parser.py
- test_traits.py
- _arco
- test_utility.py
- test_wild_magic.py
- loader.py
- Regeneration
- _ctx
- test_battle_master.py
- consumir_marcas
- test_loader_actions.py
- apply_class
- saving_throw
- ActionUsage
- apply_barbarian
- test_superior_invisibility.py
- ZealotFeatures
- barbarian/__init__.py
- test_death.py
- Monster
- load_monster
- test_parry.py
- RuneKnightFeatures
- FighterFeatures
- _ExplotaSiUsaRng
- test_skills.py
- traits/__init__.py
- test_arcane_archer.py
- test_multiattack.py
- dnd_sim/__init__.py
- test_relentless.py
- test_mastery.py
- BarbarianFeatures
- apply_condition
- pick
- test_area.py
- TelekineticMasterAction
- Condition
- BattleMasterFeatures
- _atacado
- main.py
- test_checks_escapes.py
- test_loader.py
- _trait
- legendary_phase
- test_condition_immunities.py
- Any
- _champion
- test_magic_resistance.py
- PlayerCharacter
- .alive
- ActionType
- test_storm_herald.py
- save_modifiers
- test_backgrounds.py
- test_rune_knight.py
- apply_fighter
- apply_cavalier
- test_lair.py
- test_psi_warrior.py
- test_pack_tactics.py
- _parchea_campo
- ConditionTracker
- _pj
- json
- test_enlarge.py
- Spellcasting
- PsiBulwarkAction
- run_combat
- test_arquitectura.py
- CombatContext
- test_damage.py
- test_spells.py
- attack_roll
- test_azer.py
- GiantFeatures
- test_extra_damage.py
- test_sustituir_ataque.py
- _carga
- psionic_dice_count
- test_ancestral_guardian.py
- test_cavalier.py
- StormHeraldFeatures
- _abilities
- _clamp
- .on_turn_start
- test_zealot.py
- TurnResources
- _RngSi
- test_el_gancho_after_failed_check_desde_ability_check_con_ctx
- fighter/__init__.py
- Any
- PsiWarriorFeatures
- D20Result
- BeastFeatures
- wild_magic.py
- inflict_damage
- roll_initiative
- _arquero
- pathlib
- _RngExplota
- RuneInvokeAction
- CombatState
- ability_check
- GiantsMightAction
- test_tactical_master_nivel_9_elige_entre_original_push_sap_slow
- RageAction
- ChampionFeatures
- build_spell_actions
- _fighter
- SaveResult
- parse_escape
- apply_champion
- Attack
- .execute
- test_champion.py
- _RngSi
- WildMagicFeatures
- Arquitectura de `dnd_sim`
- Any
- _abilities
- LegendaryState
- _duelo
- test_la_desventaja_de_iniciativa_tira_dos_d20_y_toma_el_menor
- modificar_salvacion
- TODO — DnDBalancer / dnd_sim
- superiority_dice_count
- _clean
- _golpe_sin_armas

## God Nodes (most connected - your core abstractions)
1. `Attack` - 274 edges
2. `Monster` - 229 edges
3. `Condition` - 229 edges
4. `attack_roll()` - 221 edges
5. `AttackRange` - 199 edges
6. `apply_condition()` - 186 edges
7. `Abilities` - 160 edges
8. `apply_fighter()` - 144 edges
9. `PlayerCharacter` - 142 edges
10. `load_monster()` - 136 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Champion: plan de sesión` --references--> `_clamp()`  [INFERRED]
  TODO.md → dnd_sim/core/classes.py
- `Psi Warrior (PHB 2024)` --references--> `psionic_dice_count()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/classes.py

## Import Cycles
- None detected.

## Communities (142 total, 13 thin omitted)

### Community 0 - "test_fighter.py"
Cohesion: 0.08
Nodes (17): action_surge_uses(), fighter_extra_attacks_for(), indomitable_uses(), second_wind_uses(), weapon_mastery_count(), _firmas(), _pj_con_armas(), _RngBajo (+9 more)

### Community 1 - "test_attach.py"
Cohesion: 0.10
Nodes (31): Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), _atacar(), _bite() (+23 more)

### Community 2 - "AttackRange"
Cohesion: 0.16
Nodes (37): AttackRange, _abilities(), _barbaro(), _berserker(), _ctx(), _furia_lista(), _monstruo(), _pj() (+29 more)

### Community 3 - "test_giant.py"
Cohesion: 0.13
Nodes (32): rage_damage(), apply_giant(), MightyImpelAction, _abilities(), _barbaro(), _ctx(), _furia(), _giant() (+24 more)

### Community 4 - "test_world_tree.py"
Cohesion: 0.12
Nodes (38): _abilities(), _aliado(), _barbaro(), _ctx(), _decision(), _elige_candidato(), espia(), _furia() (+30 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.08
Nodes (48): apply_wild_heart(), _con_beneficio(), _de(), _en_5_pies(), _hostil(), _orden_de(), WildHeartFeatures, _abilities() (+40 more)

### Community 6 - "test_proficiency.py"
Cohesion: 0.15
Nodes (21): ability_check_bonus(), test_sin_autoexito_ni_autofallo_en_pruebas(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia() (+13 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.10
Nodes (27): _data(), _estado(), _legendaria(), _load(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_el_ala_que_mezcla_movimiento_avisa(), test_el_cantrip_del_lich_se_omite_con_aviso() (+19 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (65): _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll(), spy(), _forma() (+57 more)

### Community 9 - "spell_parser.py"
Cohesion: 0.06
Nodes (21): Paquetes con fachada, _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla() (+13 more)

### Community 10 - "test_traits.py"
Cohesion: 0.07
Nodes (34): _avisar_ganchos_de_turno(), hooks(), BloodFrenzy, _atacante(), _ataque_melee(), _ctx(), _datos(), _pj() (+26 more)

### Community 11 - "_arco"
Cohesion: 0.17
Nodes (15): _arco(), _ctx_curving(), _curving(), _RngNo, test_curving_can_use_requiere_bonus_libre(), test_curving_can_use_si_con_la_decision_si(), test_curving_decision_no_no_re_tira(), test_curving_execute_sin_otro_enemigo_no_llama_nada() (+7 more)

### Community 12 - "test_utility.py"
Cohesion: 0.12
Nodes (30): ConditionInstance, _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), hay_utilitaria_accion(), _orden_tamano(), _abilities() (+22 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.12
Nodes (40): _sombra(), _abilities(), _barbaro(), _con_cola(), _con_efecto(), espia(), _ctx(), _furia() (+32 more)

### Community 14 - "loader.py"
Cohesion: 0.04
Nodes (33): parse_attach_effects(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), _coincide_nombre(), _con_nombre_limpio() (+25 more)

### Community 15 - "Regeneration"
Cohesion: 0.13
Nodes (4): _es_radiante(), _guardar_salvacion(), Regeneration, UndeadFortitude

### Community 16 - "_ctx"
Cohesion: 0.16
Nodes (14): _ctx(), _RngMax, _save_fallada(), _saving_nueva(), _second_wind(), test_indomitable_no_actua_bajo_el_nivel_9(), test_indomitable_repite_la_salvacion_con_bonificador_igual_al_nivel(), test_indomitable_sin_usos_no_repites_y_no_consume_rng() (+6 more)

### Community 17 - "test_battle_master.py"
Cohesion: 0.08
Nodes (40): maneuvers_known_count(), superiority_die_sides(), apply_battle_master(), _abilities(), _atacado_dos_enemigos(), _atacado_fijo(), _bm(), _completa() (+32 more)

### Community 18 - "consumir_marcas"
Cohesion: 0.13
Nodes (20): consumir_marcas(), _ejecuta(), _mods(), _RngFalla, test_disarming_attack_no_altera_el_combate_mas_que_el_dano(), test_distracting_da_ventaja_a_un_tercero_y_se_consume(), test_distracting_no_concede_ventaja_si_ya_caduco(), test_distracting_no_da_ventaja_al_marcador_ni_se_consume() (+12 more)

### Community 19 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (14): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+6 more)

### Community 20 - "apply_class"
Cohesion: 0.16
Nodes (17): apply_class(), ClassDef, normalize_class_name(), register_class(), _abilities(), _firmas(), _pj(), test_apply_class_ancestral_equivalente_a_los_apply_suelto() (+9 more)

### Community 21 - "saving_throw"
Cohesion: 0.04
Nodes (24): parse_damage_type(), _apply_condition_riders(), _log_target(), ArcaneArcherFeatures, _ctx_con_rng(), _CtxConRng, _de(), _otros_enemigos() (+16 more)

### Community 22 - "ActionUsage"
Cohesion: 0.15
Nodes (11): ActionUsage, UsageKind, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar(), test_per_day_dos_usos_y_luego_can_use_falso(), test_per_day_no_tira_recarga(), test_per_day_reset_restaura_todos_los_usos(), test_recharge_5_6_porcentaje_de_exito() (+3 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.08
Nodes (53): extra_attacks_for(), rage_uses(), apply_barbarian(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj() (+45 more)

### Community 24 - "test_superior_invisibility.py"
Cohesion: 0.36
Nodes (11): _accion(), _ctx(), _pixie(), _pj(), test_atacar_con_ventaja_y_no_pierde_la_invisibilidad(), test_ejecutarla_aplica_el_estado(), test_el_monstruo_recibe_su_accion_al_construirse(), test_lanzar_un_hechizo_tampoco_la_pierde() (+3 more)

### Community 25 - "ZealotFeatures"
Cohesion: 0.09
Nodes (9): _de(), _en_60_pies(), _es_aliado(), _furia_de(), _reserva_dados(), ZealotFeatures, test_apply_class_por_clave_aplica_zealot(), test_clave_de_registro_zealot_en_barbarian() (+1 more)

### Community 26 - "barbarian/__init__.py"
Cohesion: 0.05
Nodes (18): AncestralGuardianFeatures, apply_ancestral_guardian(), apply_battlerager(), BattleragerFeatures, _de(), SpikedArmorAction, FormOfTheBeast, NaturalWeapon (+10 more)

### Community 27 - "test_death.py"
Cohesion: 0.13
Nodes (18): combat_finished(), living_teams(), _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero() (+10 more)

### Community 28 - "Monster"
Cohesion: 0.13
Nodes (25): Monster, _abilities(), _disparo(), _RngFalla, test_banishing_arrow_falla_la_salvacion_y_deja_incapacitado(), test_banishing_arrow_salvacion_exitosa_no_aplica_condicion(), test_beguiling_arrow_hechiza_y_termina_si_el_aliado_ataca(), test_beguiling_sin_aliados_no_tira_salvacion() (+17 more)

### Community 29 - "load_monster"
Cohesion: 0.07
Nodes (35): load_monster(), _norm_name(), apply_beast(), test_una_condicion_desconocida_de_la_api_avisa(), test_fixture_sintetica_carga(), test_monstruo_no_legendario_no_carga_guaridas(), test_monstruo_sin_fichero_no_avisa(), test_el_aliento_del_dragon_no_es_magico() (+27 more)

### Community 30 - "test_parry.py"
Cohesion: 0.09
Nodes (42): _declara_uso(), _entradas(), parse_traits(), _usage(), _aliado(), _ctx(), _datos(), _espada() (+34 more)

### Community 31 - "RuneKnightFeatures"
Cohesion: 0.07
Nodes (5): Rune Knight (TCE), _redirigir_del_bando(), RuneKnightFeatures, fusionar_modo(), Rune Knight: plan de sesión

### Community 32 - "FighterFeatures"
Cohesion: 0.08
Nodes (5): ActionSurgeAction, _en_5_pies(), FighterFeatures, _rasgo(), SecondWindAction

### Community 33 - "_ExplotaSiUsaRng"
Cohesion: 0.12
Nodes (27): _accion_rally(), _commanda(), _ExplotaSiUsaRng, _ripostea_directa(), _sustituye(), test_commanders_strike_cede_el_ataque_si_hay_feinting_encolado(), test_commanders_strike_con_relentless_no_gasta_dado(), test_commanders_strike_no_se_decide_si_el_aliado_no_tiene_armas() (+19 more)

### Community 34 - "test_skills.py"
Cohesion: 0.09
Nodes (27): normalize_skill(), skill_ability(), skill_bonus(), skill_check(), _abilities(), _ctx(), _load_fixture(), _pj() (+19 more)

### Community 35 - "traits/__init__.py"
Cohesion: 0.06
Nodes (12): StateEffect, DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante(), aliados_capaces() (+4 more)

### Community 36 - "test_arcane_archer.py"
Cohesion: 0.11
Nodes (22): arcane_shot_options_known(), arcane_shot_uses(), apply_arcane_archer(), CurvingShotAction, _firmas(), _pj(), test_apply_arcane_archer_exige_la_clase_fighter(), test_apply_class_equivalente_a_apply_arcane_archer() (+14 more)

### Community 37 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 38 - "dnd_sim/__init__.py"
Cohesion: 0.06
Nodes (16): Champion (PHB 2024), ability_mod(), normalize_tool(), d20(), roll_d20(), _add(), _invoke_policy(), _run_combat() (+8 more)

### Community 39 - "test_relentless.py"
Cohesion: 0.17
Nodes (13): Relentless, _ctx(), _datos(), _jabali(), _pj(), test_el_jabali_carga_su_relentless_con_umbral_y_uso(), test_relentless_no_necesita_contexto_ni_rng(), test_reset_reestablece_el_umbral_y_los_usos() (+5 more)

### Community 40 - "test_mastery.py"
Cohesion: 0.10
Nodes (28): al_acertar(), al_fallar(), _cd_topple(), _log(), _nombre(), resolver_maestria(), _arma(), _atacante() (+20 more)

### Community 41 - "BarbarianFeatures"
Cohesion: 0.08
Nodes (5): BarbarianFeatures, _rasgo(), BerserkerFeatures, test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 42 - "apply_condition"
Cohesion: 0.06
Nodes (65): Abilities, parse_range_type(), apply_condition(), _as_condition(), _condicion_bloqueada(), _contar(), end_turn(), _label() (+57 more)

### Community 43 - "pick"
Cohesion: 0.06
Nodes (13): roll_dice(), DamageType, log_line(), proficiency_bonus(), pick(), sample(), _contexto(), _contexto() (+5 more)

### Community 44 - "test_area.py"
Cohesion: 0.25
Nodes (20): AreaTargeting, select_area_targets(), _area_action(), _ctx(), _npc(), _pj(), _save_forzado(), test_cada_pj_es_elegido_aproximadamente_el_62_5_por_ciento() (+12 more)

### Community 45 - "TelekineticMasterAction"
Cohesion: 0.11
Nodes (17): _armas_de(), _de(), _telekinetic_master_vigente(), TelekineticMasterAction, TelekineticMasterAttackAction, _abilities(), _master(), test_el_ataque_adicional_exige_efecto_activo_y_bonus_libre() (+9 more)

### Community 46 - "Condition"
Cohesion: 0.17
Nodes (28): RollMode, resolve_roll_mode(), Condition, attack_modifiers(), _accion(), _ataque(), _ctx(), _datos() (+20 more)

### Community 47 - "BattleMasterFeatures"
Cohesion: 0.08
Nodes (7): Battle Master (PHB 2024), _aliados(), BattleMasterFeatures, BattleMasterRallyAction, _de(), FeintingAttackAction, _orden_tamano()

### Community 48 - "_atacado"
Cohesion: 0.07
Nodes (39): _accion_feinting(), _atacado(), _conoce_sweeping(), _decide(), _parry(), _RngIdx, _RngNo, _RngSi (+31 more)

### Community 49 - "main.py"
Cohesion: 0.11
Nodes (22): CLI del simulador: `build_parser()`, Detalle por flag, Ejemplos, Flujo de `main()`, `--legendary-p`, `--legendary-points`, `--monster` / `-m`, Observaciones (para humanos y IA) (+14 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.10
Nodes (37): attempt_escapes(), EscapeCheck, _ctx(), _data(), _load(), _pj(), test_con_dos_caracteristicas_se_elige_una_al_azar(), test_con_una_sola_caracteristica_no_consume_rng() (+29 more)

### Community 51 - "test_loader.py"
Cohesion: 0.16
Nodes (12): _armor_class_value(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper(), test_cache_avoids_second_network(), test_load_monster_maps_ogre() (+4 more)

### Community 52 - "_trait"
Cohesion: 0.26
Nodes (21): _aliado(), _con_estilo(), _enemigo(), _mods(), test_ataques_estudiados_caduca_al_final_del_siguiente_turno(), test_ataques_estudiados_da_ventaja_contra_el_objetivo_tras_un_fallo(), test_ataques_estudiados_es_por_objetivo(), test_ataques_estudiados_no_actua_bajo_el_nivel_13() (+13 more)

### Community 53 - "legendary_phase"
Cohesion: 0.13
Nodes (28): legendary_phase(), _contexto(), _pj(), test_con_una_sola_accion_asequible_pick_no_consume_rng(), test_dos_duenos_legendarios_actuan_cada_uno_una_vez(), test_el_combate_termina_en_medio_de_la_fase(), test_la_fase_ocurre_despues_del_end_turn(), test_la_resistencia_convierte_fallos_automaticos() (+20 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.13
Nodes (15): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+7 more)

### Community 57 - "Any"
Cohesion: 0.07
Nodes (18): Cavalier (XGE), _agrandado(), _bando_del(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), daño_base_arma() (+10 more)

### Community 59 - "_champion"
Cohesion: 0.11
Nodes (17): _champion(), _fighter(), test_atletismo_recibe_ventaja_para_el_champion(), test_defense_como_primero_no_duplica_la_ca(), test_defy_death_es_dato_sin_efecto(), test_el_segundo_estilo_difiere_del_primero_y_esta_en_el_pool(), test_heroic_warrior_es_dato_sin_efecto(), test_kwarg_estilo_inventado_da_value_error() (+9 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.11
Nodes (23): ConditionEffect, test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa() (+15 more)

### Community 61 - "PlayerCharacter"
Cohesion: 0.22
Nodes (16): PlayerCharacter, begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate() (+8 more)

### Community 62 - ".alive"
Cohesion: 0.09
Nodes (5): _es_aliado(), _armas_melee_de(), CavalierFeatures, _de(), _avisar_ataque_especial_marca()

### Community 64 - "ActionType"
Cohesion: 0.06
Nodes (23): normalize_ability(), _check_fields(), _construir(), _error(), _por_datos(), build_condition_action(), build_save_action(), build_save_effect() (+15 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.13
Nodes (37): _abilities(), _aliado(), _barbaro(), _ctx(), _fijar_fallo_reaccion(), _fijar_salvacion(), _furia(), _herald() (+29 more)

### Community 66 - "save_modifiers"
Cohesion: 0.17
Nodes (11): _condiciones(), _hooks(), save_modifiers(), _datos(), _lich(), _pj(), test_con_ventaja_acierta_mas_que_sin_ella(), test_da_ventaja_si_la_salvacion_es_de_conversion() (+3 more)

### Community 67 - "test_backgrounds.py"
Cohesion: 0.16
Nodes (17): Background, load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes(), test_apply_background_sin_competencias_es_inofensivo() (+9 more)

### Community 68 - "test_rune_knight.py"
Cohesion: 0.08
Nodes (29): _fuego(), _parchea_fuego(), _piedra(), test_activar_storm_gasta_un_uso_y_levanta_el_estado(), test_fire_rune_al_fallar_la_salvacion_restringe_con_dano_extra(), test_fire_rune_dania_2d6_al_inicio_del_turno_del_objetivo(), test_fire_rune_dos_invocaciones_dejan_una_sola_marca(), test_fire_rune_el_objetivo_muerto_limpia_la_marca() (+21 more)

### Community 69 - "apply_fighter"
Cohesion: 0.09
Nodes (35): apply_fighter(), _abilities(), _objetivo(), _pj(), test_apply_class_reenvía_el_estilo_de_combate(), test_apply_fighter_acepta_las_habilidades_de_la_lista(), test_apply_fighter_anade_el_rasgo_guerrero(), test_apply_fighter_asigna_salvaciones_de_fue_y_con() (+27 more)

### Community 70 - "apply_cavalier"
Cohesion: 0.10
Nodes (19): cavalier_mark_uses(), warding_maneuver_uses(), apply_cavalier(), CavalierMarkAttackAction, _cavalier(), _firmas(), _pj(), test_apply_cavalier_exige_la_clase_fighter() (+11 more)

### Community 71 - "test_lair.py"
Cohesion: 0.11
Nodes (18): load_lair(), _dragon(), lairs_dir(), _orden_con(), _pj(), _spy_turnos(), spy(), test_esquema_invalido() (+10 more)

### Community 72 - "test_psi_warrior.py"
Cohesion: 0.19
Nodes (19): _ataca(), _bajo_golpe(), _parchea_golpe(), _salvacion(), test_el_ataque_adicional_no_activa_psionic_strike_mas_de_una_vez(), test_el_dado_del_psionic_strike_sigue_la_regla_de_criticos_del_motor(), test_el_empuje_de_10_ft_de_telekinetic_thrust_es_dato_sin_efecto(), test_el_flag_de_psionic_strike_se_reinicia_cada_turno() (+11 more)

### Community 73 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 74 - "_parchea_campo"
Cohesion: 0.14
Nodes (16): _amiga(), _parchea_campo(), _recibe(), test_el_protective_field_comparte_la_reaccion_del_turno(), test_el_protective_field_no_actua_con_cero_de_dano(), test_el_protective_field_no_actua_por_debajo_del_nivel_tres(), test_el_protective_field_no_baja_el_daño_de_cero(), test_el_protective_field_no_protege_a_un_enemigo() (+8 more)

### Community 76 - "_pj"
Cohesion: 0.08
Nodes (29): apply_rune_knight(), _ctx(), _EspiaPrueba, _EspiaSalvacion, _pj(), _rune(), test_aplicar_con_nivel_inferior_a_tres_da_error(), test_aplicar_sin_clase_guerrero_da_error() (+21 more)

### Community 77 - "json"
Cohesion: 0.06
Nodes (35): Race, _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait() (+27 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.14
Nodes (25): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+17 more)

### Community 79 - "Spellcasting"
Cohesion: 0.15
Nodes (6): parse_spellcasting(), Spellcasting, test_el_lanzador_se_lee_de_los_actions(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_un_hechizo_de_accion_bonus_se_comprueba_en_su_fase(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 80 - "PsiBulwarkAction"
Cohesion: 0.16
Nodes (15): bulwark_targets(), _elegibles_bulwark(), PsiBulwarkAction, effective_ac(), _bulwark(), test_bulwark_targets_es_el_mod_de_int_con_minimo_uno(), test_el_bulwark_bonifica_las_salvaciones_de_des_pero_no_las_otras(), test_el_bulwark_concede_media_cobertura_al_dueno_y_a_los_aliados() (+7 more)

### Community 81 - "run_combat"
Cohesion: 0.13
Nodes (16): CombatResult, run_combat(), _summarize_damage(), _breath(), _eventos(), _FixedRandom, _load_fixture(), _player() (+8 more)

### Community 82 - "test_arquitectura.py"
Cohesion: 0.21
Nodes (6): Cómo comprobar que todo sigue en orden, _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api()

### Community 83 - "CombatContext"
Cohesion: 0.05
Nodes (23): _objetivo_enganche(), valid_targets(), _reaccion_si_procede(), _tag_modificadores(), actor_is_alive(), CombatContext, _en_accion_de_ataque(), _living_enemies() (+15 more)

### Community 84 - "test_damage.py"
Cohesion: 0.11
Nodes (20): simulate(), _guerrero_y_ogro(), _target(), test_attack_roll_log_modifier(), test_danio_medio_por_combatiente_y_equipo(), test_etiqueta_de_modificadores_se_deriva_del_dano_final(), test_immune_target_takes_zero_damage(), test_immunity_zero() (+12 more)

### Community 85 - "test_spells.py"
Cohesion: 0.11
Nodes (43): parse_spell(), spell_action(), _ctx(), _npc(), _pj(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion() (+35 more)

### Community 86 - "attack_roll"
Cohesion: 0.09
Nodes (24): _actualizar_distancia(), attack_roll(), _mode_tag(), _abilities(), _escudo_partida(), _parchea_escudo(), test_cloud_rune_sin_otro_enemigo_no_consulta_pick(), test_giant_might_el_daño_extra_es_del_tipo_del_arma() (+16 more)

### Community 87 - "test_azer.py"
Cohesion: 0.26
Nodes (17): _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), _rasgo(), test_ataque_a_distancia_no_dispara_la_represalia() (+9 more)

### Community 88 - "GiantFeatures"
Cohesion: 0.18
Nodes (4): _de(), GiantFeatures, _objetivos_impel(), _orden_de()

### Community 89 - "test_extra_damage.py"
Cohesion: 0.17
Nodes (18): DamageRecorder, _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional() (+10 more)

### Community 90 - "test_sustituir_ataque.py"
Cohesion: 0.16
Nodes (11): _sustituir_ataque(), AtaqueSustituido, _abilities(), _blanco(), _pj(), _RasgoQueSustituye, _RasgoSinSustitucion, _RngExplota (+3 more)

### Community 91 - "_carga"
Cohesion: 0.16
Nodes (14): _ataque_carga(), _carga(), _salvacion(), test_ferocious_charger_cd_es_ocho_mas_pb_mas_fuerza(), test_ferocious_charger_con_p_medio_tira_un_random(), test_ferocious_charger_el_flag_se_reinicia_cada_turno(), test_ferocious_charger_nivel_14_no_actua_sin_rng(), test_ferocious_charger_p_cero_no_carga_sin_rng() (+6 more)

### Community 92 - "psionic_dice_count"
Cohesion: 0.11
Nodes (14): psionic_dice_count(), _guardado(), _psi(), test_guarded_mind_con_pick_no_no_purga_ni_gasta(), test_guarded_mind_concede_resistencia_psiquica_a_partir_del_nivel_10(), test_guarded_mind_purga_charmed_y_frightened_gastando_un_dado(), test_guarded_mind_sin_condicion_no_consulta_pick(), test_guarded_mind_sin_ctx_rng_no_purga() (+6 more)

### Community 93 - "test_ancestral_guardian.py"
Cohesion: 0.18
Nodes (26): _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado(), _escudo(), _esperado() (+18 more)

### Community 94 - "test_cavalier.py"
Cohesion: 0.09
Nodes (44): cavalier_mark_extra_damage(), _accion_marca(), _bajo_ataque(), _cargar_main(), _defiende(), _especial(), _parchea_ataque(), _pick_sin_decision() (+36 more)

### Community 95 - "StormHeraldFeatures"
Cohesion: 0.09
Nodes (8): _aliados_en_aura(), _cd(), _dado_mar(), _de(), _en_aura(), _enemigos_en_aura(), _escalado(), StormHeraldFeatures

### Community 96 - "_abilities"
Cohesion: 0.20
Nodes (17): _abilities(), _marca_con(), _marcado(), _mods(), _RngSi, test_incapacitado_el_marcador_anula_la_marca(), test_la_marca_caduca_en_la_ronda_indicada(), test_la_marca_no_se_consume_y_no_aplica_al_atacar_al_marcador() (+9 more)

### Community 97 - "_clamp"
Cohesion: 0.08
Nodes (19): _clamp(), giants_might_die_sides(), rune_uses(), runes_known_count(), runic_shield_uses(), _nube_partida(), _pick(), _parchea_nube() (+11 more)

### Community 98 - ".on_turn_start"
Cohesion: 0.16
Nodes (4): _aliados_heridos(), _cd_ataque(), _de(), _en_10_pies()

### Community 99 - "test_zealot.py"
Cohesion: 0.08
Nodes (71): WarriorHealAction, _abilities(), _accion(), _aliado(), _barbaro(), _ctx(), _decision(), espia() (+63 more)

### Community 100 - "TurnResources"
Cohesion: 0.07
Nodes (65): TurnResources, AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer(), _bj() (+57 more)

### Community 101 - "_RngSi"
Cohesion: 0.12
Nodes (11): _RngSi, test_arcane_shot_se_aplica_una_sola_vez_por_turno(), test_arcane_shot_se_gasta_un_uso_al_aplicar(), test_daño_de_arcane_shot_es_2d6_antes_del_18(), _dado(), test_daño_de_arcane_shot_es_4d6_desde_el_18(), test_decision_de_impacto_no_gasta_el_uso_hasta_impactar(), test_piercing_gasta_el_uso_al_sustituir() (+3 more)

### Community 103 - "fighter/__init__.py"
Cohesion: 0.12
Nodes (11): apply_psi_warrior(), _firmas(), _pj(), test_apply_class_equivalente_a_apply_psi_warrior(), test_apply_psi_warrior_por_debajo_del_nivel_3_da_value_error(), test_apply_psi_warrior_sin_clase_guerrero_da_value_error(), test_guarded_mind_no_acumula_la_resistencia_si_ya_la_tenia(), test_sin_subclase_el_walker_del_motor_no_consulta_ni_tira_rng() (+3 more)

### Community 104 - "Any"
Cohesion: 0.17
Nodes (6): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contexto_de(), _presupuesto()

### Community 105 - "PsiWarriorFeatures"
Cohesion: 0.10
Nodes (10): Psi Warrior (PHB 2024), psionic_die_sides(), _dano_extra_de_rasgo(), PsiWarriorFeatures, remove_condition(), _proteccion_psionica(), cobertura_bulwark_activa(), test_el_bulwark_se_ignora_con_dueno_incapacitado_y_se_reanuda() (+2 more)

### Community 106 - "D20Result"
Cohesion: 0.10
Nodes (25): D20Result, test_commanders_strike_sustituye_el_ataque_y_el_aliado_gasta_su_reaccion(), _d20(), test_el_dado_de_reaccion_no_se_duplica_en_critico(), _d20(), test_el_motor_decide_y_gasta_el_dado_en_el_ataque(), test_parry_no_actua_cuando_el_battle_master_es_el_atacante(), test_parry_no_se_consulta_si_el_ataque_falla() (+17 more)

### Community 108 - "wild_magic.py"
Cohesion: 0.11
Nodes (12): _bolstering(), _cd(), _de(), _en_30_pies(), _enemigos(), _espiritu(), _flores(), _infusion() (+4 more)

### Community 109 - "inflict_damage"
Cohesion: 0.13
Nodes (10): _absorber_pv_temporales(), _hooks(), inflict_damage(), _is_petrified(), _mark_dead_if_down(), _mitigacion_de_otros(), _notify_damage_dealt(), _notify_damage_taken() (+2 more)

### Community 110 - "roll_initiative"
Cohesion: 0.36
Nodes (8): roll_initiative(), _d20_fijo(), test_ambush_con_la_decision_no_no_gasta_nada(), test_ambush_con_relentless_no_gasta_dado(), test_ambush_sin_dados_no_consume_rng(), test_ambush_sin_la_maniobra_no_consume_rng(), test_ambush_suma_un_dado_a_la_tirada_de_iniciativa(), test_sin_subclase_roll_initiative_no_consulta_bonus()

### Community 111 - "_arquero"
Cohesion: 0.11
Nodes (17): _arquero(), _RngExplota, test_accion_curving_se_anade_desde_el_nivel_7(), test_arcane_shot_crea_usos_por_nivel(), test_arcane_shot_se_reinicia_en_on_turn_start(), test_arcane_shot_sin_rng_no_actua(), test_arcane_shot_sin_usos_cero_rng(), test_ataque_cuerpo_a_cuerpo_cero_rng() (+9 more)

### Community 112 - "pathlib"
Cohesion: 0.18
Nodes (5): capa_de(), main(), visit_ImportFrom(), modulo_de(), resolver()

### Community 113 - "_RngExplota"
Cohesion: 0.25
Nodes (4): _RngExplota, test_interception_sin_arma_ni_escudo_no_actúa_y_no_consume_rng(), test_resolver_maestria_sin_maestria_no_consulta_tactical_master(), test_tactical_master_no_sustituye_bajo_el_nivel_9()

### Community 114 - "RuneInvokeAction"
Cohesion: 0.12
Nodes (15): RuneInvokeAction, _accion_storm(), _invocada(), test_frost_invocado_suma_dos_a_fue_y_con_en_pruebas_y_salvaciones(), _sal(), test_hill_concede_resistencia_bpc_no_acumula_y_se_revoca_al_reset(), test_la_storm_rune_registra_su_accion_de_invocacion(), test_las_distancias_de_las_runas_son_dato_sin_efecto() (+7 more)

### Community 116 - "ability_check"
Cohesion: 0.14
Nodes (11): ability_check(), _avisar_fallo_prueba(), CheckResult, _finish_check(), _guia(), _resolve_mods(), check_modifiers(), modificar_prueba() (+3 more)

### Community 117 - "GiantsMightAction"
Cohesion: 0.13
Nodes (13): giants_might_uses(), _de(), GiantsMightAction, _orden_tamano(), _giant_pj(), test_giant_might_da_ventaja_solo_en_fuerza(), test_giant_might_daño_extra_una_vez_por_turno(), test_giant_might_el_tamano_vuelve_al_original_en_reset() (+5 more)

### Community 119 - "RageAction"
Cohesion: 0.18
Nodes (13): RageAction, apply_berserker(), IntimidatingPresenceAction, _presencia_ctx(), test_apply_anade_trait_y_accion(), test_presencia_afecta_a_un_numero_aleatorio_de_enemigos(), test_presencia_requiere_nivel_14(), test_presencia_sin_rng_no_paga() (+5 more)

### Community 120 - "ChampionFeatures"
Cohesion: 0.14
Nodes (6): champion_crit_threshold(), heroic_rally_amount(), ChampionFeatures, test_el_rango_critico_de_champion_es_20_19_o_18_segun_el_nivel(), test_la_cura_de_heroic_rally_es_5_mas_el_mod_de_con_sin_bajar_de_cero(), Champion: plan de sesión

### Community 121 - "build_spell_actions"
Cohesion: 0.29
Nodes (8): build_spell_actions(), _desde_fixture(), _monstruo_lanzador(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_la_reaccion_gasta_su_uso_propio(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_uso_propio(), test_un_hechizo_a_voluntad_se_puede_lanzar_en_cada_turno()

### Community 122 - "_fighter"
Cohesion: 0.16
Nodes (14): _action_surge(), _ctx_recursos(), _fighter(), test_action_surge_como_maximo_un_vez_por_turno(), test_action_surge_ejecutada_restaura_la_accion_y_gasta_un_uso(), test_action_surge_no_es_elegible_si_la_accion_no_se_ha_gastado(), test_action_surge_no_es_elegible_si_la_bonus_ya_se_gasto(), test_action_surge_no_es_elegible_sin_usos() (+6 more)

### Community 123 - "SaveResult"
Cohesion: 0.25
Nodes (11): SaveResult, fake_saving_throw(), _fake(), falla(), espia(), stub(), stub(), stub() (+3 more)

### Community 124 - "parse_escape"
Cohesion: 0.22
Nodes (5): has_escape_text(), parse_escape(), _skills_for(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 125 - "apply_champion"
Cohesion: 0.13
Nodes (12): apply_champion(), _de(), _firmas(), _pj(), test_apply_champion_por_debajo_del_nivel_3_da_value_error(), test_apply_champion_sin_clase_guerrero_da_value_error(), test_apply_class_equivalente_a_apply_champion(), test_remarkable_athlete_no_concede_competencia_en_atletismo() (+4 more)

### Community 126 - "Attack"
Cohesion: 0.17
Nodes (9): Attack, _nuevo_ataque(), _parchea_warding(), test_marca_al_impactar_con_ataque_cuerpo_a_cuerpo(), test_warding_convierte_el_impacto_en_fallo(), test_warding_no_convierte_un_critico_natural_y_aun_asi_resiste(), test_warding_no_se_acumula_con_la_resistencia_previa(), test_warding_protege_al_aliado_del_cavalier() (+1 more)

### Community 127 - ".execute"
Cohesion: 0.22
Nodes (3): _armas_melee_de(), _de(), _furia_de()

### Community 128 - "test_champion.py"
Cohesion: 0.26
Nodes (9): _rally(), test_con_muy_baja_heroic_rally_da_cero_y_no_cura(), test_heroic_rally_cura_si_esta_bloodied_con_al_menos_1_pg(), test_heroic_rally_no_cura_si_tiene_0_pg(), test_heroic_rally_recorta_la_curacion_a_los_pg_maximos(), test_la_mitad_exacta_de_los_pg_maximos_cuenta_como_bloodied(), test_no_cura_por_encima_de_la_mitad_de_los_pg_maximos(), test_por_debajo_del_nivel_18_heroic_rally_no_actua() (+1 more)

### Community 129 - "_RngSi"
Cohesion: 0.22
Nodes (6): _check_fallada(), _RngSi, test_tactical_mind_no_gasta_el_uso_si_aun_asi_falla(), test_tactical_mind_sin_ctx_no_actua(), test_tactical_mind_sin_usos_no_actua_y_no_consume_rng(), test_tactical_mind_suma_d10_y_gasta_un_uso_si_la_tirada_final_pasa()

### Community 131 - "Arquitectura de `dnd_sim`"
Cohesion: 0.20
Nodes (8): Arcane Archer (XGE), Arquitectura de `dnd_sim`, Carpetas, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, test_ever_ready_shot_no_cambia_los_usos_al_empezar_un_combate()

### Community 132 - "Any"
Cohesion: 0.28
Nodes (5): evaluar_d20(), _instancias(), umbral_critico(), test_el_umbral_del_rasgo_es_19_o_18_y_20_para_hechizos(), test_sin_subclase_el_umbral_de_critico_es_20_sin_rng()

### Community 133 - "_abilities"
Cohesion: 0.33
Nodes (9): _abilities(), _parchea_d20(), test_ataque_de_hechizo_no_usa_el_umbral_de_champion(), test_el_critico_con_19_impacta_aunque_no_alcance_la_ca(), test_el_rango_ampliado_a_18_solo_funciona_desde_el_nivel_15(), test_el_un_natural_sigue_fallen_do_para_un_champion(), test_los_dos_estilos_funcionan_a_la_ves(), test_un_no_champion_con_19_falla_contra_la_misma_ca() (+1 more)

### Community 134 - "LegendaryState"
Cohesion: 0.14
Nodes (15): lair_phase(), LairAction, LegendaryState, _ctx(), _enemigo(), _Stub, test_dos_acciones_uniformes(), test_no_actua_si_el_combate_cae_en_medio() (+7 more)

### Community 135 - "_duelo"
Cohesion: 0.31
Nodes (7): _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

### Community 136 - "test_la_desventaja_de_iniciativa_tira_dos_d20_y_toma_el_menor"
Cohesion: 0.25
Nodes (4): test_la_desventaja_de_iniciativa_tira_dos_d20_y_toma_el_menor(), test_la_iniciativa_tira_dos_d20_y_toma_el_mayor_solo_para_el_champion(), test_los_dados_del_critico_se_doblan_con_el_rango_ampliado(), espia()

### Community 137 - "modificar_salvacion"
Cohesion: 0.29
Nodes (3): modificar_salvacion(), _modificar_tirada(), test_la_ventaja_de_hill_en_salvaciones_de_veneno_es_dato_sin_efecto()

### Community 138 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.33
Nodes (5): Grafo y verificación, Pendientes generales, Rutina sugerida al abrir sesión, TODO — DnDBalancer / dnd_sim, TODOs en código (marcados `# TODO`)

## Knowledge Gaps
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `test_champion.py`, `test_attach.py`, `AttackRange`, `test_fighter.py`, `Any`, `_abilities`, `test_giant.py`, `_duelo`, `test_beast.py`, `test_la_desventaja_de_iniciativa_tira_dos_d20_y_toma_el_menor`, `test_legendary.py`, `_arco`, `test_proficiency.py`, `_golpe_sin_armas`, `loader.py`, `test_traits.py`, `test_utility.py`, `test_battle_master.py`, `consumir_marcas`, `test_wild_magic.py`, `apply_class`, `saving_throw`, `test_world_tree.py`, `apply_barbarian`, `test_superior_invisibility.py`, `barbarian/__init__.py`, `test_death.py`, `Monster`, `load_monster`, `test_parry.py`, `test_wild_heart.py`, `_ExplotaSiUsaRng`, `test_arcane_archer.py`, `dnd_sim/__init__.py`, `test_relentless.py`, `test_mastery.py`, `apply_condition`, `pick`, `Condition`, `_atacado`, `main.py`, `test_checks_escapes.py`, `legendary_phase`, `Any`, `test_magic_resistance.py`, `PlayerCharacter`, `ActionType`, `test_storm_herald.py`, `test_rune_knight.py`, `apply_fighter`, `apply_cavalier`, `test_psi_warrior.py`, `test_pack_tactics.py`, `_pj`, `test_enlarge.py`, `test_damage.py`, `test_spells.py`, `attack_roll`, `test_azer.py`, `test_extra_damage.py`, `test_sustituir_ataque.py`, `_carga`, `test_ancestral_guardian.py`, `test_cavalier.py`, `_abilities`, `_clamp`, `test_zealot.py`, `TurnResources`, `_RngSi`, `fighter/__init__.py`, `D20Result`, `_arquero`, `_RngExplota`, `_fighter`, `apply_champion`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `daño_base_arma()`) actually correct?**
  _`Attack` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_fighter.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08064516129032258 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_champion.py`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `LegendaryState`, `test_legendary.py`, `test_beast.py`, `spell_parser.py`, `test_traits.py`, `test_utility.py`, `loader.py`, `test_battle_master.py`, `consumir_marcas`, `saving_throw`, `test_superior_invisibility.py`, `barbarian/__init__.py`, `Monster`, `test_parry.py`, `RuneKnightFeatures`, `test_skills.py`, `traits/__init__.py`, `test_arcane_archer.py`, `dnd_sim/__init__.py`, `test_mastery.py`, `BarbarianFeatures`, `apply_condition`, `pick`, `TelekineticMasterAction`, `BattleMasterFeatures`, `test_checks_escapes.py`, `test_condition_immunities.py`, `Any`, `_champion`, `test_magic_resistance.py`, `.alive`, `ActionType`, `test_storm_herald.py`, `save_modifiers`, `test_rune_knight.py`, `test_lair.py`, `test_psi_warrior.py`, `test_pack_tactics.py`, `_parchea_campo`, `ConditionTracker`, `_pj`, `test_enlarge.py`, `CombatContext`, `test_damage.py`, `test_spells.py`, `GiantFeatures`, `_carga`, `psionic_dice_count`, `test_cavalier.py`, `StormHeraldFeatures`, `_abilities`, `PsiWarriorFeatures`, `inflict_damage`, `ability_check`, `RageAction`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Monster` (e.g. with `Carpetas` and `_cloaker()`) actually correct?**
  _`Monster` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10374149659863946 - nodes in this community are weakly interconnected._
- **Why does `Monster` connect `Monster` to `test_champion.py`, `test_attach.py`, `AttackRange`, `Arquitectura de `dnd_sim``, `test_fighter.py`, `_abilities`, `test_giant.py`, `_duelo`, `test_beast.py`, `test_la_desventaja_de_iniciativa_tira_dos_d20_y_toma_el_menor`, `LegendaryState`, `_arco`, `test_legendary.py`, `test_proficiency.py`, `loader.py`, `test_traits.py`, `test_utility.py`, `test_battle_master.py`, `consumir_marcas`, `test_wild_magic.py`, `test_world_tree.py`, `test_superior_invisibility.py`, `test_wild_heart.py`, `test_death.py`, `load_monster`, `test_parry.py`, `_ExplotaSiUsaRng`, `test_arcane_archer.py`, `dnd_sim/__init__.py`, `test_relentless.py`, `test_mastery.py`, `apply_condition`, `test_area.py`, `TelekineticMasterAction`, `Condition`, `_atacado`, `test_checks_escapes.py`, `test_condition_immunities.py`, `test_magic_resistance.py`, `ActionType`, `test_storm_herald.py`, `test_rune_knight.py`, `apply_fighter`, `apply_cavalier`, `test_lair.py`, `test_psi_warrior.py`, `test_pack_tactics.py`, `_parchea_campo`, `_pj`, `test_enlarge.py`, `PsiBulwarkAction`, `test_damage.py`, `test_spells.py`, `attack_roll`, `test_azer.py`, `test_sustituir_ataque.py`, `_carga`, `test_ancestral_guardian.py`, `test_cavalier.py`, `_abilities`, `_clamp`, `test_zealot.py`, `TurnResources`, `_RngSi`, `fighter/__init__.py`, `roll_initiative`, `_arquero`, `RuneInvokeAction`, `build_spell_actions`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
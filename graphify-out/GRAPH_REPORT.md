# Graph Report - DnDBalancer  (2026-11-16)

## Corpus Check
- 241 files · ~242,442 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 4782 nodes · 17478 edges · 165 communities (120 shown, 45 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 1346 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d4367c93`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- _ctx_recursos
- test_attach.py
- AttackRange
- test_giant.py
- test_world_tree.py
- test_wild_heart.py
- test_proficiency.py
- test_legendary.py
- test_beast.py
- spell_parser.py
- RollMode
- test_hechizos_pj.py
- test_utility.py
- test_wild_magic.py
- loader.py
- SamuraiFeatures
- _fighter
- test_battle_master.py
- _samurai
- trait_parser.py
- apply_class
- inflict_damage
- ActionUsage
- apply_barbarian
- test_superior_invisibility.py
- ZealotFeatures
- CavalierFeatures
- test_death.py
- Monster
- load_monster
- test_zealot.py
- RuneKnightFeatures
- FighterFeatures
- _ExplotaSiUsaRng
- test_skills.py
- dnd_sim/__init__.py
- test_arcane_archer.py
- test_multiattack.py
- SpellSlots
- test_relentless.py
- test_mastery.py
- BarbarianFeatures
- apply_condition
- pick
- test_area.py
- .can_act
- test_invisibility.py
- BattleMasterFeatures
- _atacado
- main.py
- test_checks_escapes.py
- test_samurai.py
- _trait
- GiantFeatures
- test_condition_immunities.py
- _abilities
- test_champion.py
- saving_throw
- begin_turn
- _ejecuta
- race_parser.py
- test_storm_herald.py
- aplicar_lanzamiento
- test_backgrounds.py
- Condition
- apply_fighter
- apply_cavalier
- _pj
- psionic_dice_count
- attack_modifiers
- _parchea_campo
- ConditionTracker
- test_rune_knight.py
- test_races.py
- test_enlarge.py
- ataque_utilitario
- PsiBulwarkAction
- run_combat
- test_arquitectura.py
- SpellStateAction
- Abilities
- test_spells.py
- PsiWarriorFeatures
- .spend
- json
- attack_roll
- test_sustituir_ataque.py
- _carga
- TurnResources
- test_ancestral_guardian.py
- _especial
- StormHeraldFeatures
- _abilities
- Regeneration
- CombatContext
- _decision
- test_battlerager.py
- _RngSi
- _pj
- test_psi_warrior.py
- legendary_phase
- test_la_lista_se_guarda_en_cache_y_la_segunda_vez_no_toca_la_red
- Attack
- test_martial_advantage.py
- PJSpellAction
- test_undead_fortitude.py
- roll_initiative
- _arquero
- _revienta
- _RngExplota
- _RngBajo
- CombatState
- test_el_gancho_after_failed_check_desde_ability_check_con_ctx
- _atacante
- test_tactical_master_nivel_9_elige_entre_original_push_sap_slow
- BerserkerFeatures
- _estado
- Spellcasting
- test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque
- SaveResult
- test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio
- WarriorHealAction
- test_cavalier.py
- test_el_cli_tiene_las_opciones_legendarias
- random
- test_el_cuerpo_de_turno_extraido_no_cambia_run_combat
- test_sin_salvaciones_de_muerte_sbd_es_la_aproximacion
- Arquitectura de `dnd_sim`
- _clamp
- multiattack_parser.py
- test_lair.py
- SpellcastingDef
- normalize_skill
- parse_race
- test_piercing_k_uniforme_y_atacante_nunca_es_objetivo
- _RngMax
- test_sustitucion_hace_un_solo_par_de_picks

## God Nodes (most connected - your core abstractions)
1. `Attack` - 282 edges
2. `Condition` - 240 edges
3. `attack_roll()` - 235 edges
4. `Monster` - 235 edges
5. `AttackRange` - 201 edges
6. `apply_condition()` - 191 edges
7. `Abilities` - 171 edges
8. `apply_fighter()` - 158 edges
9. `PlayerCharacter` - 152 edges
10. `RollMode` - 145 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Psi Warrior (PHB 2024)` --references--> `psionic_dice_count()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/classes.py
- `Psi Warrior (PHB 2024)` --references--> `psionic_die_sides()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/classes.py

## Import Cycles
- None detected.

## Communities (165 total, 45 thin omitted)

### Community 0 - "_ctx_recursos"
Cohesion: 0.48
Nodes (7): _action_surge(), _ctx_recursos(), test_action_surge_como_maximo_un_vez_por_turno(), test_action_surge_ejecutada_restaura_la_accion_y_gasta_un_uso(), test_action_surge_no_es_elegible_si_la_accion_no_se_ha_gastado(), test_action_surge_no_es_elegible_si_la_bonus_ya_se_gasto(), test_action_surge_no_es_elegible_sin_usos()

### Community 1 - "test_attach.py"
Cohesion: 0.11
Nodes (31): Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), _atacar(), _bite() (+23 more)

### Community 2 - "AttackRange"
Cohesion: 0.11
Nodes (50): AttackRange, RageAction, apply_berserker(), IntimidatingPresenceAction, _abilities(), _barbaro(), _berserker(), _ctx() (+42 more)

### Community 3 - "test_giant.py"
Cohesion: 0.12
Nodes (33): apply_giant(), MightyImpelAction, _abilities(), _barbaro(), _ctx(), _furia(), _giant(), _mon() (+25 more)

### Community 4 - "test_world_tree.py"
Cohesion: 0.08
Nodes (43): _aliados_heridos(), apply_world_tree(), _de(), _en_10_pies(), WorldTreeFeatures, _abilities(), _aliado(), _barbaro() (+35 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.07
Nodes (49): apply_wild_heart(), _con_beneficio(), _de(), _en_5_pies(), _hostil(), _orden_de(), WildHeartFeatures, _abilities() (+41 more)

### Community 6 - "test_proficiency.py"
Cohesion: 0.14
Nodes (21): ability_check_bonus(), test_sin_autoexito_ni_autofallo_en_pruebas(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia() (+13 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.09
Nodes (51): _contexto(), _data(), _load(), _pj(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_con_una_sola_accion_asequible_pick_no_consume_rng(), test_con_use_probability_uno_el_danio_es_mayor_que_con_cero() (+43 more)

### Community 8 - "test_beast.py"
Cohesion: 0.06
Nodes (70): WeaponAttackAction, apply_beast(), BeastFeatures, CallTheHuntBonus, _habilitar_armas_naturales(), _abilities(), _barb(), _beast() (+62 more)

### Community 9 - "spell_parser.py"
Cohesion: 0.05
Nodes (20): has_escape_text(), _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla() (+12 more)

### Community 10 - "RollMode"
Cohesion: 0.05
Nodes (39): RollMode, _mode_tag(), _avisar_ganchos_de_turno(), check_modifiers(), cobertura_bulwark_activa(), _condiciones(), fusionar_modo(), _hooks() (+31 more)

### Community 11 - "test_hechizos_pj.py"
Cohesion: 0.15
Nodes (19): hechizo_soportado(), preparar_hechizos(), _legal(), _muestrear(), _def_a5(), _hechizo(), _lista(), test_exceder_el_conteo_de_la_tabla_es_un_value_error() (+11 more)

### Community 12 - "test_utility.py"
Cohesion: 0.20
Nodes (22): ConditionInstance, _abilities(), _ctx(), _mon(), _pj(), _siempre_falla(), test_actor_no_disponible_no_consulta_la_probabilidad(), test_agarrar_admite_hasta_un_tamano_mayor() (+14 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.06
Nodes (46): apply_wild_magic(), _cd(), _de(), _en_30_pies(), _enemigos(), WildMagicFeatures, WildSurgeAction, _abilities() (+38 more)

### Community 14 - "loader.py"
Cohesion: 0.03
Nodes (46): normalize_ability(), is_area_action(), parse_attach_effects(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), parse_range_type() (+38 more)

### Community 15 - "SamuraiFeatures"
Cohesion: 0.10
Nodes (9): Samurai (XGE), fighting_spirit_temp_hp(), fighting_spirit_uses(), _procesar_turnos_extra(), _de(), SamuraiFeatures, test_tabla_fighting_spirit_temp_hp_por_nivel(), test_tabla_fighting_spirit_uses_por_nivel() (+1 more)

### Community 16 - "_fighter"
Cohesion: 0.13
Nodes (24): _check_fallada(), _ctx(), _fighter(), _save_fallada(), _saving_nueva(), _second_wind(), test_action_surge_no_existe_en_nivel_1(), test_indomitable_no_actua_bajo_el_nivel_9() (+16 more)

### Community 17 - "test_battle_master.py"
Cohesion: 0.08
Nodes (35): maneuvers_known_count(), superiority_dice_count(), superiority_die_sides(), apply_battle_master(), _atacado_dos_enemigos(), _bm(), _completa(), _firmas() (+27 more)

### Community 18 - "_samurai"
Cohesion: 0.15
Nodes (25): _capturador(), _contador_pick(), _ctx(), _ctx_ataque(), _enemigo(), _samurai(), _si(), test_con_el_pick_no_la_muerte_sigue_normal() (+17 more)

### Community 19 - "trait_parser.py"
Cohesion: 0.16
Nodes (7): _declara_uso(), _usage(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 20 - "apply_class"
Cohesion: 0.06
Nodes (25): apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), SpikedArmorAction, FormOfTheBeast, NaturalWeapon, apply_class() (+17 more)

### Community 21 - "inflict_damage"
Cohesion: 0.02
Nodes (52): Cavalier (XGE), Paquetes con fachada, DamageType, parse_damage_type(), proficiency_bonus(), skill_ability(), _objetivo_enganche(), valid_targets() (+44 more)

### Community 22 - "ActionUsage"
Cohesion: 0.11
Nodes (15): ActionUsage, UsageKind, _breath(), _FixedRandom, test_at_will_nunca_se_agota(), test_begin_turn_no_tira_nada_si_estan_cargadas(), test_begin_turn_reinicia_recursos_y_tira_una_recarga_por_accion(), test_media_de_turnos_hasta_recargar() (+7 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.08
Nodes (53): extra_attacks_for(), rage_uses(), apply_barbarian(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj() (+45 more)

### Community 24 - "test_superior_invisibility.py"
Cohesion: 0.17
Nodes (18): _entradas(), parse_traits(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd(), test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad(), test_el_umbral_se_saca_de_cada_descripcion(), _accion(), _ctx(), _pixie() (+10 more)

### Community 25 - "ZealotFeatures"
Cohesion: 0.08
Nodes (12): apply_zealot(), _de(), _en_60_pies(), _es_aliado(), _furia_de(), _reserva_dados(), ZealotFeatures, test_apply_anade_trait_y_dos_acciones_bonus() (+4 more)

### Community 26 - "CavalierFeatures"
Cohesion: 0.12
Nodes (6): cavalier_mark_extra_damage(), _armas_melee_de(), CavalierFeatures, CavalierMarkAttackAction, _de(), test_daño_extra_del_ataque_especial_es_el_nivel_entre_dos()

### Community 27 - "test_death.py"
Cohesion: 0.13
Nodes (18): combat_finished(), living_teams(), _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero() (+10 more)

### Community 28 - "Monster"
Cohesion: 0.12
Nodes (28): Monster, _abilities(), _disparo(), _RngFalla, test_banishing_arrow_falla_la_salvacion_y_deja_incapacitado(), test_banishing_arrow_salvacion_exitosa_no_aplica_condicion(), test_beguiling_arrow_hechiza_y_termina_si_el_aliado_ataca(), test_beguiling_sin_aliados_no_tira_salvacion() (+20 more)

### Community 29 - "load_monster"
Cohesion: 0.05
Nodes (42): _armor_class_value(), load_monster(), CombatantType, test_una_condicion_desconocida_de_la_api_avisa(), test_fixture_sintetica_carga(), test_monstruo_no_legendario_no_carga_guaridas(), test_monstruo_sin_fichero_no_avisa(), _load_fixture() (+34 more)

### Community 30 - "test_zealot.py"
Cohesion: 0.17
Nodes (17): ZealousPresenceAction, _abilities(), _aliado(), _barbaro(), _presencia(), test_nivel_3_no_recibe_rasgos_superiores(), test_presencia_con_cobertura_uno_no_consume_rng(), test_presencia_da_ventaja_en_ataques_a_aliados() (+9 more)

### Community 31 - "RuneKnightFeatures"
Cohesion: 0.08
Nodes (3): _de(), _orden_tamano(), RuneKnightFeatures

### Community 32 - "FighterFeatures"
Cohesion: 0.07
Nodes (7): ActionSurgeAction, _contexto(), _en_5_pies(), _es_aliado(), FighterFeatures, _rasgo(), SecondWindAction

### Community 33 - "_ExplotaSiUsaRng"
Cohesion: 0.13
Nodes (25): _accion_rally(), _commanda(), _ExplotaSiUsaRng, _ripostea_directa(), _sustituye(), test_commanders_strike_cede_el_ataque_si_hay_feinting_encolado(), test_commanders_strike_no_se_decide_si_el_aliado_no_tiene_armas(), test_commanders_strike_no_se_decide_si_el_aliado_ya_uso_su_reaccion() (+17 more)

### Community 34 - "test_skills.py"
Cohesion: 0.08
Nodes (30): ability_check(), _avisar_fallo_prueba(), CheckResult, _finish_check(), _guia(), _resolve_mods(), skill_bonus(), skill_check() (+22 more)

### Community 35 - "dnd_sim/__init__.py"
Cohesion: 0.04
Nodes (22): Champion (PHB 2024), ability_mod(), d20(), roll_d20(), _extract(), first_target_policy(), random_policy(), apply_champion() (+14 more)

### Community 36 - "test_arcane_archer.py"
Cohesion: 0.11
Nodes (22): arcane_shot_options_known(), arcane_shot_uses(), apply_arcane_archer(), CurvingShotAction, _firmas(), _pj(), test_apply_arcane_archer_exige_la_clase_fighter(), test_apply_class_equivalente_a_apply_arcane_archer() (+14 more)

### Community 37 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 38 - "SpellSlots"
Cohesion: 0.29
Nodes (16): SpellSlots, construir_acciones(), _caster(), _ctx(), _enemigo(), _pj_lanzador(), test_la_cd_del_pj_es_8_mas_pb_mas_mod_y_el_ataque_pb_mas_mod(), test_la_concentracion_se_pierde_al_morir() (+8 more)

### Community 39 - "test_relentless.py"
Cohesion: 0.17
Nodes (13): Relentless, _ctx(), _datos(), _jabali(), _pj(), test_el_jabali_carga_su_relentless_con_umbral_y_uso(), test_relentless_no_necesita_contexto_ni_rng(), test_reset_reestablece_el_umbral_y_los_usos() (+5 more)

### Community 40 - "test_mastery.py"
Cohesion: 0.10
Nodes (29): al_acertar(), al_fallar(), _cd_topple(), consumir_marcas(), _log(), _nombre(), resolver_maestria(), _arma() (+21 more)

### Community 41 - "BarbarianFeatures"
Cohesion: 0.09
Nodes (6): BarbarianFeatures, _contexto(), ExtendRageAction, _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 42 - "apply_condition"
Cohesion: 0.09
Nodes (52): apply_condition(), _ataque(), _ctx(), _data(), _duelo(), _load(), _pj(), _tasa_de_impacto() (+44 more)

### Community 43 - "pick"
Cohesion: 0.04
Nodes (27): rage_damage(), roll_dice(), log_line(), pick(), sample(), ActionType, AttackEntry, CombatAction (+19 more)

### Community 44 - "test_area.py"
Cohesion: 0.12
Nodes (27): AreaTargeting, select_area_targets(), _default_targeting(), _area_action(), _ctx(), _npc(), _pj(), _save_forzado() (+19 more)

### Community 45 - ".can_act"
Cohesion: 0.10
Nodes (17): _armas_de(), _de(), _elegibles_bulwark(), _telekinetic_master_vigente(), TelekineticMasterAction, TelekineticMasterAttackAction, _master(), test_el_ataque_adicional_exige_efecto_activo_y_bonus_libre() (+9 more)

### Community 46 - "test_invisibility.py"
Cohesion: 0.22
Nodes (23): _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj(), test_atacar_a_un_invisible_tiene_desventaja(), test_atacar_deja_de_ser_invisible() (+15 more)

### Community 47 - "BattleMasterFeatures"
Cohesion: 0.07
Nodes (10): Battle Master (PHB 2024), _aliados(), _aliados_elegibles(), _armas_melee_propias(), _armas_propias(), BattleMasterFeatures, BattleMasterRallyAction, _de() (+2 more)

### Community 48 - "_atacado"
Cohesion: 0.07
Nodes (40): _accion_feinting(), _atacado(), _conoce_sweeping(), _decide(), _parry(), _RngIdx, _RngNo, _RngSi (+32 more)

### Community 49 - "main.py"
Cohesion: 0.11
Nodes (22): CLI del simulador: `build_parser()`, Detalle por flag, Ejemplos, Flujo de `main()`, `--legendary-p`, `--legendary-points`, `--monster` / `-m`, Observaciones (para humanos y IA) (+14 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.07
Nodes (50): parse_escape(), _skills_for(), EscapeCheck, resolve_attack_range(), _ataque(), _check_fijo(), _ctx(), _data() (+42 more)

### Community 51 - "test_samurai.py"
Cohesion: 0.16
Nodes (14): apply_samurai(), _abilities(), _pj(), test_apply_class_y_apply_samurai_son_equivalentes(), test_apply_samurai_exige_la_clase_guerrero(), test_apply_samurai_exige_nivel_minimo_tres(), test_el_bonus_proficiency_anade_una_habilidad_nueva(), test_el_elegant_courtier_concede_sab_desde_el_nivel_siete() (+6 more)

### Community 52 - "_trait"
Cohesion: 0.20
Nodes (22): _aliado(), _con_estilo(), _enemigo(), _mods(), _RngSi, test_ataques_estudiados_caduca_al_final_del_siguiente_turno(), test_ataques_estudiados_da_ventaja_contra_el_objetivo_tras_un_fallo(), test_ataques_estudiados_es_por_objetivo() (+14 more)

### Community 53 - "GiantFeatures"
Cohesion: 0.16
Nodes (4): _de(), GiantFeatures, _objetivos_impel(), _orden_de()

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.13
Nodes (15): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+7 more)

### Community 57 - "_abilities"
Cohesion: 0.15
Nodes (12): _decidir_maniobra(), _reaccionar_al_fallo(), _reducir_dano_recibido(), _abilities(), _mods(), test_distracting_da_ventaja_a_un_tercero_y_se_consume(), test_distracting_no_concede_ventaja_si_ya_caduco(), test_goading_caduca_en_la_ronda_indicada() (+4 more)

### Community 59 - "test_champion.py"
Cohesion: 0.06
Nodes (56): champion_crit_threshold(), heroic_rally_amount(), umbral_critico(), _abilities(), _champion(), _fighter(), _firmas(), _parchea_d20() (+48 more)

### Community 60 - "saving_throw"
Cohesion: 0.03
Nodes (60): _check_fields(), _construir(), _error(), _apply_condition_riders(), SaveAction, AreaSaveAction, _log_target(), _sombra() (+52 more)

### Community 61 - "begin_turn"
Cohesion: 0.30
Nodes (14): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+6 more)

### Community 62 - "_ejecuta"
Cohesion: 0.17
Nodes (14): _ejecuta(), _RngFalla, test_disarming_attack_no_altera_el_combate_mas_que_el_dano(), test_distracting_no_da_ventaja_al_marcador_ni_se_consume(), test_efectos_sin_implementacion_no_alteran_el_combate(), test_el_dano_de_la_maniobra_se_suma_una_sola_vez(), test_goading_attack_marca_al_objetivo_si_falla_la_salvacion(), test_goading_attack_no_marca_si_pasa_la_salvacion() (+6 more)

### Community 64 - "race_parser.py"
Cohesion: 0.13
Nodes (8): get_race(), get_trait(), load_race(), _spells_from_description(), test_load_race_descarga_la_raza_y_sus_rasgos(), _rasgo(), _raza(), test_load_race_propaga_el_error_de_la_api()

### Community 65 - "test_storm_herald.py"
Cohesion: 0.10
Nodes (42): apply_storm_herald(), _de(), StormAuraAction, _abilities(), _aliado(), _barbaro(), _ctx(), _fijar_fallo_reaccion() (+34 more)

### Community 66 - "aplicar_lanzamiento"
Cohesion: 0.19
Nodes (12): aplicar_lanzamiento(), _def_mago_falso(), _lista_a6(), _oleada(), _registrar_mago_falso(), _apply(), test_apply_class_con_la_clase_falsa_crea_espacios_y_acciones(), test_en_run_combat_el_pj_lanzador_gasta_espacios_sin_excederlos() (+4 more)

### Community 67 - "test_backgrounds.py"
Cohesion: 0.16
Nodes (17): Background, load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes(), test_apply_background_sin_competencias_es_inofensivo() (+9 more)

### Community 68 - "Condition"
Cohesion: 0.09
Nodes (26): Condition, test_el_enum_no_contiene_condiciones_excluidas(), test_invisible_es_una_condicion_modelada(), _fuego(), _pick(), _parchea_fuego(), _d20(), _piedra() (+18 more)

### Community 69 - "apply_fighter"
Cohesion: 0.09
Nodes (41): apply_fighter(), maestria_de(), _abilities(), _firmas(), _objetivo(), _pj(), _pj_con_armas(), test_apply_class_fighter_sin_subclase_equivalente_a_apply_fighter() (+33 more)

### Community 70 - "apply_cavalier"
Cohesion: 0.10
Nodes (21): cavalier_mark_uses(), warding_maneuver_uses(), apply_cavalier(), _cavalier(), _firmas(), _pj(), test_apply_cavalier_exige_la_clase_fighter(), test_apply_cavalier_requiere_nivel_3() (+13 more)

### Community 71 - "_pj"
Cohesion: 0.18
Nodes (14): _dragon(), _orden_con(), _pj(), _spy_turnos(), spy(), test_guarida_pasa_magical_a_las_salvaciones(), test_puntos_siempre_incluyen_bonus_de_guarida(), test_reproducibilidad_con_guarida() (+6 more)

### Community 72 - "psionic_dice_count"
Cohesion: 0.18
Nodes (19): psionic_dice_count(), _ataca(), _bajo_golpe(), _parchea_golpe(), _salvacion(), test_el_ataque_adicional_no_activa_psionic_strike_mas_de_una_vez(), test_el_dado_del_psionic_strike_sigue_la_regla_de_criticos_del_motor(), test_el_empuje_de_10_ft_de_telekinetic_thrust_es_dato_sin_efecto() (+11 more)

### Community 73 - "attack_modifiers"
Cohesion: 0.21
Nodes (15): attack_modifiers(), _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj() (+7 more)

### Community 74 - "_parchea_campo"
Cohesion: 0.09
Nodes (24): _amiga(), _guardado(), _parchea_campo(), _recibe(), test_el_protective_field_comparte_la_reaccion_del_turno(), test_el_protective_field_no_actua_con_cero_de_dano(), test_el_protective_field_no_actua_por_debajo_del_nivel_tres(), test_el_protective_field_no_baja_el_daño_de_cero() (+16 more)

### Community 76 - "test_rune_knight.py"
Cohesion: 0.03
Nodes (94): Rune Knight (TCE), giants_might_die_sides(), giants_might_uses(), rune_uses(), runes_known_count(), runic_shield_uses(), apply_rune_knight(), GiantsMightAction (+86 more)

### Community 77 - "test_races.py"
Cohesion: 0.27
Nodes (12): Race, _abilities(), _fiendish_legacy(), _pj(), test_apply_race_añade_competencias_fijas(), test_apply_race_con_habilidad_pedida(), test_apply_race_habilidad_fuera_de_las_opciones_es_error(), test_apply_race_no_duplica_competencias_existentes() (+4 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.14
Nodes (25): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+17 more)

### Community 79 - "ataque_utilitario"
Cohesion: 0.20
Nodes (8): _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), hay_utilitaria_accion(), _orden_tamano(), test_p_medio_usa_utilitaria_a_la_frecuencia_configurada(), test_p_uno_siempre_decide_sin_consumir_rng()

### Community 80 - "PsiBulwarkAction"
Cohesion: 0.16
Nodes (17): Psi Warrior (PHB 2024), bulwark_targets(), PsiBulwarkAction, effective_ac(), _bulwark(), test_bulwark_targets_es_el_mod_de_int_con_minimo_uno(), test_el_bulwark_bonifica_las_salvaciones_de_des_pero_no_las_otras(), _d20() (+9 more)

### Community 81 - "run_combat"
Cohesion: 0.15
Nodes (15): CombatResult, _invoke_policy(), run_combat(), _run_combat(), _nuevo_ctx(), _summarize_damage(), _eventos(), _load_fixture() (+7 more)

### Community 82 - "test_arquitectura.py"
Cohesion: 0.24
Nodes (5): _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api()

### Community 83 - "SpellStateAction"
Cohesion: 0.09
Nodes (7): actor_is_alive(), HealAction, _romper_invisibilidad_al_lanzar(), SpellStateAction, chequeo_concentracion_al_danio(), _tiene_estado(), SuperiorInvisibility

### Community 84 - "Abilities"
Cohesion: 0.08
Nodes (27): Abilities, simulate(), Combatant, PlayerCharacter, test_sin_condiciones_el_dano_no_cambia(), _guerrero_y_ogro(), _target(), test_attack_roll_log_modifier() (+19 more)

### Community 85 - "test_spells.py"
Cohesion: 0.08
Nodes (53): build_spell_actions(), parse_spell(), SpellFixedDamageAction, spell_action(), _ctx(), _desde_fixture(), _monstruo_lanzador(), _npc() (+45 more)

### Community 87 - ".spend"
Cohesion: 0.20
Nodes (4): test_al_agotar_un_nivel_las_ofertas_superiores_siguen_disponibles(), test_gastar_un_espacio_agotado_es_un_value_error(), test_reset_rellena_los_espacios_igual_que_al_crearlos(), test_un_truco_no_gasta_espacio_y_un_hechizo_de_nivel_1_si()

### Community 88 - "json"
Cohesion: 0.12
Nodes (11): _cache_path(), get_background(), _get_entry(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError, _fetch_class_spells() (+3 more)

### Community 89 - "attack_roll"
Cohesion: 0.06
Nodes (69): _actualizar_distancia(), attack_roll(), DamageRecorder, _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos() (+61 more)

### Community 90 - "test_sustituir_ataque.py"
Cohesion: 0.16
Nodes (11): _sustituir_ataque(), AtaqueSustituido, _abilities(), _blanco(), _pj(), _RasgoQueSustituye, _RasgoSinSustitucion, _RngExplota (+3 more)

### Community 91 - "_carga"
Cohesion: 0.16
Nodes (14): _ataque_carga(), _carga(), _salvacion(), test_ferocious_charger_cd_es_ocho_mas_pb_mas_fuerza(), test_ferocious_charger_con_p_medio_tira_un_random(), test_ferocious_charger_el_flag_se_reinicia_cada_turno(), test_ferocious_charger_nivel_14_no_actua_sin_rng(), test_ferocious_charger_p_cero_no_carga_sin_rng() (+6 more)

### Community 92 - "TurnResources"
Cohesion: 0.18
Nodes (4): TurnResources, SpellAction, apply_concentration(), test_un_hechizo_de_accion_bonus_se_comprueba_en_su_fase()

### Community 93 - "test_ancestral_guardian.py"
Cohesion: 0.10
Nodes (28): AncestralGuardianFeatures, apply_ancestral_guardian(), _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado() (+20 more)

### Community 94 - "_especial"
Cohesion: 0.26
Nodes (11): _accion_marca(), _especial(), _pick_sin_decision(), test_el_ataque_especial_no_gasta_un_uso_ni_la_reaccion(), test_el_ataque_especial_no_suma_dano_extra_si_falla(), test_el_ataque_especial_se_arma_cuando_el_marcado_dana_a_un_tercero(), test_el_ataque_especial_solo_vale_en_el_siguiente_turno(), test_el_ataque_especial_suma_el_dano_extra_si_impacta() (+3 more)

### Community 95 - "StormHeraldFeatures"
Cohesion: 0.10
Nodes (7): _aliados_en_aura(), _cd(), _dado_mar(), _en_aura(), _enemigos_en_aura(), _escalado(), StormHeraldFeatures

### Community 96 - "_abilities"
Cohesion: 0.19
Nodes (18): _abilities(), _marca_con(), _marcado(), _mods(), _RngSi, test_incapacitado_el_marcador_anula_la_marca(), test_la_marca_caduca_en_la_ronda_indicada(), test_la_marca_no_se_consume_y_no_aplica_al_atacar_al_marcador() (+10 more)

### Community 98 - "CombatContext"
Cohesion: 0.17
Nodes (4): CombatContext, _en_accion_de_ataque(), _living_enemies(), _log()

### Community 99 - "_decision"
Cohesion: 0.15
Nodes (20): _decision(), _fallos(), _forma(), _guarda_con(), test_fanatical_decision_negativa_no_repiten(), test_fanatical_el_resultado_nuevo_sustituye_al_original(), test_fanatical_no_se_ofrece_en_auto_fallo(), test_fanatical_no_se_ofrece_en_salvacion_superada() (+12 more)

### Community 100 - "test_battlerager.py"
Cohesion: 0.18
Nodes (31): AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer(), _bj(), _ctx() (+23 more)

### Community 101 - "_RngSi"
Cohesion: 0.12
Nodes (11): _RngSi, test_arcane_shot_se_aplica_una_sola_vez_por_turno(), test_arcane_shot_se_gasta_un_uso_al_aplicar(), test_daño_de_arcane_shot_es_2d6_antes_del_18(), _dado(), test_daño_de_arcane_shot_es_4d6_desde_el_18(), test_decision_de_impacto_no_gasta_el_uso_hasta_impactar(), test_piercing_gasta_el_uso_al_sustituir() (+3 more)

### Community 102 - "_pj"
Cohesion: 0.22
Nodes (19): espia(), _espiar_divine(), _furia(), _mon(), _pj(), test_determinismo_misma_semilla_mismos_resultados(), corrida(), test_divine_fury_elige_radiante_con_pick() (+11 more)

### Community 103 - "test_psi_warrior.py"
Cohesion: 0.12
Nodes (20): psionic_die_sides(), apply_psi_warrior(), _abilities(), _firmas(), _pj(), _psi(), test_apply_class_equivalente_a_apply_psi_warrior(), test_apply_psi_warrior_por_debajo_del_nivel_3_da_value_error() (+12 more)

### Community 104 - "legendary_phase"
Cohesion: 0.14
Nodes (11): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), legendary_phase(), LegendaryAction (+3 more)

### Community 105 - "test_la_lista_se_guarda_en_cache_y_la_segunda_vez_no_toca_la_red"
Cohesion: 0.20
Nodes (3): _get_spell_fixture(), test_la_lista_de_clase_se_parsea_con_nivel_y_escuela(), test_la_lista_se_guarda_en_cache_y_la_segunda_vez_no_toca_la_red()

### Community 106 - "Attack"
Cohesion: 0.13
Nodes (25): D20Result, Attack, _atacado_fijo(), test_commanders_strike_con_relentless_no_gasta_dado(), test_commanders_strike_el_dueño_nunca_es_el_aliado_elegido(), test_commanders_strike_sustituye_el_ataque_y_el_aliado_gasta_su_reaccion(), _d20(), test_el_ataque_del_aliado_no_reentra_en_commanders_strike() (+17 more)

### Community 107 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 109 - "test_undead_fortitude.py"
Cohesion: 0.21
Nodes (14): _ctx(), _datos(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido(), test_la_salvacion_puede_salvarlo_o_no() (+6 more)

### Community 110 - "roll_initiative"
Cohesion: 0.27
Nodes (8): roll_initiative(), _d20_fijo(), test_ambush_con_la_decision_no_no_gasta_nada(), test_ambush_con_relentless_no_gasta_dado(), test_ambush_sin_dados_no_consume_rng(), test_ambush_sin_la_maniobra_no_consume_rng(), test_ambush_suma_un_dado_a_la_tirada_de_iniciativa(), test_sin_subclase_roll_initiative_no_consulta_bonus()

### Community 111 - "_arquero"
Cohesion: 0.10
Nodes (31): _arco(), _arquero(), _ctx_curving(), _curving(), _RngExplota, _RngNo, test_accion_curving_se_anade_desde_el_nivel_7(), test_arcane_shot_crea_usos_por_nivel() (+23 more)

### Community 112 - "_revienta"
Cohesion: 0.22
Nodes (6): test_no_es_elegible_sin_nivel_sin_uso_sin_reaccion_sin_contexto(), _crear(), test_no_se_activa_si_la_accion_adicional_ya_gasto(), test_sin_candidatas_el_bonus_proficiency_no_cambia_nada(), _revienta(), test_sin_la_subclase_los_ataques_no_consumen_rng_de_samurai()

### Community 113 - "_RngExplota"
Cohesion: 0.25
Nodes (4): _RngExplota, test_interception_sin_arma_ni_escudo_no_actúa_y_no_consume_rng(), test_resolver_maestria_sin_maestria_no_consulta_tactical_master(), test_tactical_master_no_sustituye_bajo_el_nivel_9()

### Community 119 - "BerserkerFeatures"
Cohesion: 0.12
Nodes (6): _armas_melee_de(), BerserkerFeatures, _de(), _furia_de(), _golpe_sin_armas(), test_golpe_sin_armas_unidad()

### Community 120 - "_estado"
Cohesion: 0.50
Nodes (3): _estado(), test_el_estado_legendario_rellena_gasta_y_reinicia(), test_use_probability_medio_se_usa_about_50_por_ciento()

### Community 121 - "Spellcasting"
Cohesion: 0.10
Nodes (12): Hechizos de PJ (PHB 2024), parse_spellcasting(), estadisticas_lanzador(), PCSpellcasting, Spellcasting, _spell_data(), _spellcasting(), test_un_truco_de_hechizo_pasa_magical_a_su_salvacion() (+4 more)

### Community 123 - "SaveResult"
Cohesion: 0.33
Nodes (9): SaveResult, _fake(), stub(), stub(), stub(), test_fanatical_no_activo_sin_furia(), test_revivificacion_no_roba_el_gasto_de_furia_inaguantable(), falla() (+1 more)

### Community 125 - "WarriorHealAction"
Cohesion: 0.25
Nodes (14): WarriorHealAction, _accion(), _ctx(), test_after_failed_save_sin_zealot_devuelve_el_mismo_resultado(), test_warrior_curacion_gasta_un_dado_y_suma_pv(), test_warrior_curacion_no_supera_el_maximo(), test_warrior_de_los_dioses_reserva_por_nivel(), test_warrior_ejecucion_determinista_con_misma_semilla() (+6 more)

### Community 126 - "test_cavalier.py"
Cohesion: 0.11
Nodes (33): _bajo_ataque(), _cargar_main(), _defiende(), _parchea_ataque(), _parchea_warding(), _RngExplota, test_el_flag_charge_p_llega_al_rasgo(), test_flag_charge_p_en_el_cli() (+25 more)

### Community 128 - "random"
Cohesion: 0.26
Nodes (18): _abilities(), _ctx(), _decide(), _pj(), test_antes_del_nivel_2_no_hay_decision_ni_rng(), test_en_turno_ajeno_no_decide(), test_frecuencia_0_5_es_aproximadamente_la_mitad_de_los_turnos(), test_las_reacciones_no_deciden_ni_reciben() (+10 more)

### Community 131 - "Arquitectura de `dnd_sim`"
Cohesion: 0.18
Nodes (9): Arcane Archer (XGE), Arquitectura de `dnd_sim`, Carpetas, Cómo comprobar que todo sigue en orden, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia (+1 more)

### Community 132 - "_clamp"
Cohesion: 0.12
Nodes (11): action_surge_uses(), _clamp(), fighter_extra_attacks_for(), indomitable_uses(), second_wind_uses(), weapon_mastery_count(), test_action_surge_usos_por_nivel_son_1_y_2(), test_indomitable_usos_por_nivel_son_1_2_y_3() (+3 more)

### Community 133 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (5): _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 134 - "test_lair.py"
Cohesion: 0.09
Nodes (19): load_lair(), lair_phase(), LairAction, LegendaryState, _ctx(), _enemigo(), lairs_dir(), _Stub (+11 more)

### Community 138 - "SpellcastingDef"
Cohesion: 0.10
Nodes (15): spell_slots_for(), SpellcastingDef, SubclassDef, test_spell_slots_for_con_progresión_desconocida_es_un_value_error(), test_spell_slots_for_devuelve_la_tupla_sin_ceros_finales(), test_spell_slots_for_sin_espacios_por_debajo_del_minimo(), test_spellcastingdef_valida_la_progresión_y_expone_espacios(), Fighter: cómo añadir una subclase (+7 more)

### Community 140 - "normalize_skill"
Cohesion: 0.11
Nodes (6): normalize_tool(), _clean(), normalize_skill(), _add(), test_normalize_skill_acepta_espacios_y_spanish(), test_normalize_skill_desconocida_lanza_value_error()

### Community 141 - "parse_race"
Cohesion: 0.20
Nodes (8): parse_race(), _skill_name(), _trait_skills(), _keen_senses(), test_parse_competencias_fijas_de_la_raza(), test_parse_descripcion_sin_hechizos_da_vacio(), test_parse_elfo_linaje_hechizos_sin_duplicados(), test_parse_habilidades_a_elegir_de_los_rasgos()

## Knowledge Gaps
- **45 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `random`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_el_cuerpo_de_turno_extraido_no_cambia_run_combat`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_world_tree.py`, `RollMode`, `test_hechizos_pj.py`, `test_utility.py`, `test_wild_magic.py`, `loader.py`, `test_battle_master.py`, `_samurai`, `apply_class`, `inflict_damage`, `test_sustitucion_hace_un_solo_par_de_picks`, `apply_barbarian`, `test_superior_invisibility.py`, `test_death.py`, `Monster`, `load_monster`, `test_zealot.py`, `_ExplotaSiUsaRng`, `dnd_sim/__init__.py`, `test_arcane_archer.py`, `test_relentless.py`, `test_mastery.py`, `apply_condition`, `pick`, `test_invisibility.py`, `_atacado`, `main.py`, `test_checks_escapes.py`, `test_samurai.py`, `_abilities`, `test_champion.py`, `saving_throw`, `begin_turn`, `_ejecuta`, `test_storm_herald.py`, `apply_fighter`, `apply_cavalier`, `psionic_dice_count`, `attack_modifiers`, `test_rune_knight.py`, `test_enlarge.py`, `Abilities`, `test_spells.py`, `attack_roll`, `test_sustituir_ataque.py`, `_carga`, `test_ancestral_guardian.py`, `_abilities`, `test_battlerager.py`, `_RngSi`, `_pj`, `test_psi_warrior.py`, `test_undead_fortitude.py`, `_arquero`, `_RngExplota`, `_atacante`, `BerserkerFeatures`, `test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque`, `test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio`, `test_cavalier.py`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `daño_base_arma()`) actually correct?**
  _`Attack` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10917874396135266 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_lair.py`, `test_legendary.py`, `test_beast.py`, `spell_parser.py`, `RollMode`, `test_hechizos_pj.py`, `normalize_skill`, `test_utility.py`, `loader.py`, `SamuraiFeatures`, `test_battle_master.py`, `_samurai`, `inflict_damage`, `test_superior_invisibility.py`, `CavalierFeatures`, `Monster`, `RuneKnightFeatures`, `test_skills.py`, `dnd_sim/__init__.py`, `test_arcane_archer.py`, `SpellSlots`, `test_mastery.py`, `BarbarianFeatures`, `apply_condition`, `pick`, `.can_act`, `test_invisibility.py`, `BattleMasterFeatures`, `test_checks_escapes.py`, `test_samurai.py`, `GiantFeatures`, `test_condition_immunities.py`, `test_champion.py`, `saving_throw`, `_ejecuta`, `test_storm_herald.py`, `psionic_dice_count`, `attack_modifiers`, `_parchea_campo`, `ConditionTracker`, `test_rune_knight.py`, `test_enlarge.py`, `ataque_utilitario`, `PsiBulwarkAction`, `SpellStateAction`, `Abilities`, `test_spells.py`, `PsiWarriorFeatures`, `attack_roll`, `_carga`, `TurnResources`, `StormHeraldFeatures`, `_abilities`, `test_psi_warrior.py`, `Attack`, `_revienta`, `BerserkerFeatures`, `test_cavalier.py`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Are the 167 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 167 INFERRED edges - model-reasoned connections that need verification._
- **Should `AttackRange` be split into smaller, more focused modules?**
  _Cohesion score 0.10582750582750583 - nodes in this community are weakly interconnected._
- **Why does `Trait` connect `pick` to `test_attach.py`, `.reduce_damage_to_allies`, `test_world_tree.py`, `test_wild_heart.py`, `test_beast.py`, `RollMode`, `.modify_save_modifiers`, `test_wild_magic.py`, `SamuraiFeatures`, `trait_parser.py`, `apply_class`, `inflict_damage`, `.on_rage_start`, `test_superior_invisibility.py`, `ZealotFeatures`, `CavalierFeatures`, `.damage_dice_upgrades`, `.modify_attack_modifiers`, `.grant_save_modifiers`, `.after_failed_save`, `RuneKnightFeatures`, `FighterFeatures`, `.after_failed_check`, `.blocks_condition`, `dnd_sim/__init__.py`, `.modify_check_modifiers`, `.on_any_turn_start`, `.on_reduced_to_zero_hp`, `.extra_actions`, `.defensive_ac_bonus`, `BarbarianFeatures`, `.defensa_ante_ataque`, `.grant_attack_modifiers`, `.after_damage_taken`, `.after_being_hit`, `.after_dealing_hit`, `BattleMasterFeatures`, `.modify_incoming_damage`, `.on_turn_start`, `GiantFeatures`, `.on_turn_end`, `test_condition_immunities.py`, `Any`, `.survives_at_zero_hp`, `test_relentless.py`, `test_rune_knight.py`, `SpellStateAction`, `PsiWarriorFeatures`, `test_sustituir_ataque.py`, `test_ancestral_guardian.py`, `StormHeraldFeatures`, `Regeneration`, `BerserkerFeatures`, `.on_rage_end`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
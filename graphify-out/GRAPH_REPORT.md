# Graph Report - DnDBalancer  (2026-11-17)

## Corpus Check
- 243 files · ~250,014 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 4882 nodes · 17868 edges · 150 communities (132 shown, 18 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 1380 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0a7ad6d4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- _fighter
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
- test_hechizos_pj.py
- test_utility.py
- test_wild_magic.py
- legendary_parser.py
- test_eldritch_knight.py
- _ctx
- test_battle_master.py
- test_samurai.py
- test_loader_actions.py
- apply_class
- attack_roll
- ActionUsage
- apply_barbarian
- test_parry.py
- Any
- .can_act
- test_death.py
- Monster
- load_monster
- RollMode
- RuneKnightFeatures
- FighterFeatures
- _ExplotaSiUsaRng
- test_skills.py
- roll_dice
- test_arcane_archer.py
- test_multiattack.py
- SpellSlots
- saving_throw
- test_mastery.py
- BarbarianFeatures
- apply_condition
- ActionType
- test_area.py
- TelekineticMasterAction
- Condition
- BattleMasterFeatures
- _atacado
- main.py
- test_checks_escapes.py
- valid_targets
- _trait
- BeastFeatures
- test_condition_immunities.py
- TurnResources
- test_champion.py
- saves.py
- begin_turn
- test_magic_resistance.py
- Trait
- inflict_damage
- test_storm_herald.py
- _registrar_mago_falso
- test_backgrounds.py
- _decide
- apply_fighter
- apply_cavalier
- test_azer.py
- psionic_dice_count
- test_pack_tactics.py
- _parchea_campo
- ConditionTracker
- test_rune_knight.py
- test_races.py
- test_enlarge.py
- RageAction
- PsiBulwarkAction
- run_combat
- test_arquitectura.py
- SpellStateAction
- Abilities
- test_spells.py
- pick
- Hechizos de PJ: plan de sesión 1
- json
- test_extra_damage.py
- test_sustituir_ataque.py
- _carga
- spell_action
- test_ancestral_guardian.py
- _especial
- barbarian/__init__.py
- _abilities
- survival.py
- CombatContext
- test_zealot.py
- test_battlerager.py
- AtaqueSustituido
- _pj
- test_psi_warrior.py
- legendary.py
- load_class_spell_list
- Attack
- test_martial_advantage.py
- _escudo_partida
- test_undead_fortitude.py
- roll_initiative
- _arco
- _arquero
- _RngExplota
- _RngBajo
- CombatState
- condition_parser.py
- apply_champion
- _champion
- BerserkerFeatures
- _estado
- build_spell_actions
- _guardado
- SaveResult
- test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio
- WarriorHealAction
- test_cavalier.py
- test_el_cli_tiene_las_opciones_legendarias
- random
- .on_turn_start
- ConditionAction
- Combatant
- _clamp
- classes/__init__.py
- test_lair.py
- _RngSi
- _abilities
- test_la_desventaja_de_iniciativa_tira_dos_d20_y_toma_el_menor
- caster.py
- Any
- dnd_sim/__init__.py
- champion_crit_threshold
- heroic_rally_amount
- superiority_dice_count
- test_apply_class_equivalente_a_apply_champion
- test_piercing_k_uniforme_y_atacante_nunca_es_objetivo
- _golpe_sin_armas
- test_ventaja_y_desventaja_de_iniciativa_se_anulan
- test_sustitucion_hace_un_solo_par_de_picks

## God Nodes (most connected - your core abstractions)
1. `Attack` - 286 edges
2. `Condition` - 242 edges
3. `Monster` - 240 edges
4. `attack_roll()` - 235 edges
5. `AttackRange` - 201 edges
6. `apply_condition()` - 191 edges
7. `Abilities` - 177 edges
8. `apply_fighter()` - 168 edges
9. `PlayerCharacter` - 154 edges
10. `RollMode` - 145 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Psi Warrior (PHB 2024)` --references--> `psionic_dice_count()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/classes.py
- `Rune Knight (TCE)` --references--> `runes_known_count()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/classes.py
- `Rune Knight (TCE)` --references--> `giants_might_die_sides()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/classes.py

## Import Cycles
- None detected.

## Communities (150 total, 18 thin omitted)

### Community 0 - "_fighter"
Cohesion: 0.13
Nodes (15): _action_surge(), _ctx_recursos(), _fighter(), test_action_surge_como_maximo_un_vez_por_turno(), test_action_surge_ejecutada_restaura_la_accion_y_gasta_un_uso(), test_action_surge_no_es_elegible_si_la_accion_no_se_ha_gastado(), test_action_surge_no_es_elegible_si_la_bonus_ya_se_gasto(), test_action_surge_no_es_elegible_sin_usos() (+7 more)

### Community 1 - "test_attach.py"
Cohesion: 0.12
Nodes (30): AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), _atacar(), _bite(), _cloaker() (+22 more)

### Community 2 - "AttackRange"
Cohesion: 0.16
Nodes (37): AttackRange, _abilities(), _barbaro(), _berserker(), _ctx(), _furia_lista(), _monstruo(), _pj() (+29 more)

### Community 3 - "test_giant.py"
Cohesion: 0.08
Nodes (37): apply_giant(), _de(), GiantFeatures, MightyImpelAction, _objetivos_impel(), _orden_de(), _abilities(), _barbaro() (+29 more)

### Community 4 - "test_world_tree.py"
Cohesion: 0.12
Nodes (38): _abilities(), _aliado(), _barbaro(), _ctx(), _decision(), _elige_candidato(), espia(), _furia() (+30 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.08
Nodes (48): apply_wild_heart(), _con_beneficio(), _de(), _en_5_pies(), _hostil(), _orden_de(), WildHeartFeatures, _abilities() (+40 more)

### Community 6 - "test_proficiency.py"
Cohesion: 0.20
Nodes (19): _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia(), test_level_manda_sobre_el_proficiency_explicito() (+11 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.09
Nodes (53): legendary_phase(), _contexto(), _data(), _load(), _pj(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_con_una_sola_accion_asequible_pick_no_consume_rng() (+45 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (65): _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll(), spy(), _forma() (+57 more)

### Community 9 - "spell_parser.py"
Cohesion: 0.09
Nodes (13): _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla(), _frases() (+5 more)

### Community 10 - "test_traits.py"
Cohesion: 0.07
Nodes (31): check_modifiers(), _atacante(), _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _RasgoDeSalvacion (+23 more)

### Community 11 - "test_hechizos_pj.py"
Cohesion: 0.15
Nodes (19): preparar_hechizos(), _muestrear(), _def_a5(), _hechizo(), _lista(), test_combatant_reset_restaura_los_espacios_del_pj_lanzador(), test_exceder_el_conteo_de_la_tabla_es_un_value_error(), test_la_preparacion_alcanza_los_conteos_de_la_tabla() (+11 more)

### Community 12 - "test_utility.py"
Cohesion: 0.12
Nodes (29): ConditionInstance, _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), _orden_tamano(), _abilities(), _ctx() (+21 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.11
Nodes (41): apply_wild_magic(), WildSurgeAction, _abilities(), _barbaro(), _con_cola(), _con_efecto(), espia(), _ctx() (+33 more)

### Community 14 - "legendary_parser.py"
Cohesion: 0.06
Nodes (25): is_area_action(), parse_condition_effects(), parse_range_type(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision() (+17 more)

### Community 15 - "test_eldritch_knight.py"
Cohesion: 0.06
Nodes (58): eldritch_knight_cantrips(), eldritch_knight_prepared(), _sustituir_ataque_por_hechizo(), apply_eldritch_knight(), _de(), _ctx(), _ek(), _lista() (+50 more)

### Community 16 - "_ctx"
Cohesion: 0.11
Nodes (15): _ctx(), _RngMax, _save_fallada(), _saving_nueva(), _second_wind(), test_el_gancho_after_failed_check_desde_ability_check_con_ctx(), test_indomitable_no_actua_bajo_el_nivel_9(), test_indomitable_repite_la_salvacion_con_bonificador_igual_al_nivel() (+7 more)

### Community 17 - "test_battle_master.py"
Cohesion: 0.09
Nodes (39): maneuvers_known_count(), superiority_die_sides(), apply_battle_master(), _abilities(), _atacado_dos_enemigos(), _atacado_fijo(), _bm(), _completa() (+31 more)

### Community 18 - "test_samurai.py"
Cohesion: 0.05
Nodes (53): fighting_spirit_temp_hp(), fighting_spirit_uses(), apply_samurai(), _de(), SamuraiFeatures, _abilities(), _capturador(), _contador_pick() (+45 more)

### Community 19 - "test_loader_actions.py"
Cohesion: 0.16
Nodes (15): simulate(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+7 more)

### Community 20 - "apply_class"
Cohesion: 0.14
Nodes (19): apply_class(), ClassDef, normalize_class_name(), _params_de(), register_class(), _abilities(), _firmas(), _pj() (+11 more)

### Community 21 - "attack_roll"
Cohesion: 0.06
Nodes (30): Cavalier (XGE), Rune Knight (TCE), _actualizar_distancia(), _agrandado(), _apply_condition_riders(), attack_roll(), _bando_del(), _bonus_de_rasgos() (+22 more)

### Community 22 - "ActionUsage"
Cohesion: 0.08
Nodes (26): _uso_de_entrada(), ActionUsage, UsageKind, _breath(), _eventos(), _FixedRandom, _load_fixture(), _player() (+18 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.09
Nodes (51): rage_uses(), apply_barbarian(), SaveModifiers, _abilities(), _ctx(), _pj(), _resultado(), test_apply_anade_acciones_de_furia() (+43 more)

### Community 24 - "test_parry.py"
Cohesion: 0.07
Nodes (52): _declara_uso(), _entradas(), parse_traits(), _usage(), remove_invisibility_on_action(), _arquero_parry(), _ataque(), _ctx() (+44 more)

### Community 25 - "Any"
Cohesion: 0.10
Nodes (7): apply_zealot(), _de(), _en_60_pies(), _es_aliado(), _furia_de(), _reserva_dados(), test_apply_requiere_clase_barbara()

### Community 26 - ".can_act"
Cohesion: 0.12
Nodes (4): _armas_melee_de(), CavalierFeatures, CavalierMarkAttackAction, _de()

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 28 - "Monster"
Cohesion: 0.14
Nodes (25): Monster, _abilities(), _disparo(), _RngFalla, test_banishing_arrow_falla_la_salvacion_y_deja_incapacitado(), test_banishing_arrow_salvacion_exitosa_no_aplica_condicion(), test_beguiling_arrow_hechiza_y_termina_si_el_aliado_ataca(), test_beguiling_sin_aliados_no_tira_salvacion() (+17 more)

### Community 29 - "load_monster"
Cohesion: 0.07
Nodes (26): _armor_class_value(), _damage_type(), load_monster(), _norm_name(), _parse_condition_immunities(), test_una_condicion_desconocida_de_la_api_avisa(), test_fixture_sintetica_carga(), test_monstruo_no_legendario_no_carga_guaridas() (+18 more)

### Community 30 - "RollMode"
Cohesion: 0.05
Nodes (32): Champion (PHB 2024), d20(), roll_d20(), RollMode, ability_check(), ability_check_bonus(), _avisar_fallo_prueba(), CheckResult (+24 more)

### Community 31 - "RuneKnightFeatures"
Cohesion: 0.06
Nodes (6): giants_might_die_sides(), _de(), _orden_tamano(), RuneKnightFeatures, _rune(), test_tabla_giants_might_die_sides_por_nivel()

### Community 32 - "FighterFeatures"
Cohesion: 0.10
Nodes (4): _contexto(), _en_5_pies(), FighterFeatures, _rasgo()

### Community 33 - "_ExplotaSiUsaRng"
Cohesion: 0.13
Nodes (25): _accion_rally(), _commanda(), _ExplotaSiUsaRng, _ripostea_directa(), _sustituye(), test_commanders_strike_cede_el_ataque_si_hay_feinting_encolado(), test_commanders_strike_no_se_decide_si_el_aliado_no_tiene_armas(), test_commanders_strike_no_se_decide_si_el_aliado_ya_uso_su_reaccion() (+17 more)

### Community 34 - "test_skills.py"
Cohesion: 0.08
Nodes (29): skill_ability(), parse_escape(), _skills_for(), skill_bonus(), _abilities(), _ctx(), _load_fixture(), _pj() (+21 more)

### Community 35 - "roll_dice"
Cohesion: 0.07
Nodes (12): roll_dice(), DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante(), aliados_capaces() (+4 more)

### Community 36 - "test_arcane_archer.py"
Cohesion: 0.11
Nodes (23): arcane_shot_options_known(), arcane_shot_uses(), apply_arcane_archer(), CurvingShotAction, _firmas(), _pj(), test_accion_curving_se_anade_desde_el_nivel_7(), test_apply_arcane_archer_exige_la_clase_fighter() (+15 more)

### Community 37 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 38 - "SpellSlots"
Cohesion: 0.20
Nodes (19): SpellSlots, construir_acciones(), _caster(), _ctx(), _enemigo(), _pj_lanzador(), test_gastar_un_espacio_agotado_es_un_value_error(), test_la_cd_del_pj_es_8_mas_pb_mas_mod_y_el_ataque_pb_mas_mod() (+11 more)

### Community 39 - "saving_throw"
Cohesion: 0.06
Nodes (36): giants_might_uses(), GiantsMightAction, save_modifiers(), _resolve_mode_str(), saving_throw(), _ctx(), _EspiaSalvacion, _giant_pj() (+28 more)

### Community 40 - "test_mastery.py"
Cohesion: 0.10
Nodes (29): al_acertar(), al_fallar(), _cd_topple(), consumir_marcas(), _log(), _nombre(), resolver_maestria(), _arma() (+21 more)

### Community 41 - "BarbarianFeatures"
Cohesion: 0.09
Nodes (5): BarbarianFeatures, ExtendRageAction, _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 42 - "apply_condition"
Cohesion: 0.07
Nodes (57): apply_condition(), end_turn(), _label(), RepeatSave, resolve_attack_range(), _ataque(), _ctx(), _data() (+49 more)

### Community 43 - "ActionType"
Cohesion: 0.05
Nodes (18): Eldritch Knight (PHB 2024), extra_attacks_for(), rage_damage(), DamageType, log_line(), proficiency_bonus(), sample(), ActionType (+10 more)

### Community 44 - "test_area.py"
Cohesion: 0.12
Nodes (26): AreaTargeting, select_area_targets(), _default_targeting(), _area_action(), _ctx(), _npc(), _pj(), _save_forzado() (+18 more)

### Community 45 - "TelekineticMasterAction"
Cohesion: 0.11
Nodes (16): _armas_de(), _de(), _telekinetic_master_vigente(), TelekineticMasterAction, TelekineticMasterAttackAction, _master(), test_el_ataque_adicional_exige_efecto_activo_y_bonus_libre(), test_el_ataque_adicional_usa_el_helper_de_ataque_del_motor() (+8 more)

### Community 46 - "Condition"
Cohesion: 0.18
Nodes (27): Condition, attack_modifiers(), test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar() (+19 more)

### Community 47 - "BattleMasterFeatures"
Cohesion: 0.07
Nodes (11): Battle Master (PHB 2024), _aliados(), _aliados_elegibles(), _armas_melee_propias(), _armas_propias(), BattleMasterFeatures, BattleMasterRallyAction, _de() (+3 more)

### Community 48 - "_atacado"
Cohesion: 0.07
Nodes (40): _accion_feinting(), _atacado(), _ejecuta(), _mods(), _parry(), _RngFalla, _RngNo, _RngSi (+32 more)

### Community 49 - "main.py"
Cohesion: 0.10
Nodes (23): CLI del simulador: `build_parser()`, Detalle por flag, Ejemplos, Flujo de `main()`, `--legendary-p`, `--legendary-points`, `--monster` / `-m`, Observaciones (para humanos y IA) (+15 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.07
Nodes (48): attempt_escapes(), EscapeCheck, _ataque(), _check_fijo(), _fake(), _ctx(), _data(), _duelo() (+40 more)

### Community 51 - "valid_targets"
Cohesion: 0.07
Nodes (14): valid_targets(), _bolstering(), _cd(), _de(), _en_30_pies(), _enemigos(), _espiritu(), _flores() (+6 more)

### Community 52 - "_trait"
Cohesion: 0.23
Nodes (24): _aliado(), _con_estilo(), _enemigo(), _mods(), _objetivo(), test_ataques_estudiados_caduca_al_final_del_siguiente_turno(), test_ataques_estudiados_da_ventaja_contra_el_objetivo_tras_un_fallo(), test_ataques_estudiados_es_por_objetivo() (+16 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.13
Nodes (15): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+7 more)

### Community 57 - "TurnResources"
Cohesion: 0.11
Nodes (19): TurnResources, _contexto_de_reaccion(), trigger_reaction(), _ctx(), _pj(), _spell_data(), _spellcasting(), test_ataque_con_magical_true_dana_completo_al_ghost() (+11 more)

### Community 59 - "test_champion.py"
Cohesion: 0.19
Nodes (12): umbral_critico(), _rally(), test_con_muy_baja_heroic_rally_da_cero_y_no_cura(), test_el_umbral_del_rasgo_es_19_o_18_y_20_para_hechizos(), test_heroic_rally_cura_si_esta_bloodied_con_al_menos_1_pg(), test_heroic_rally_no_cura_si_tiene_0_pg(), test_heroic_rally_recorta_la_curacion_a_los_pg_maximos(), test_la_mitad_exacta_de_los_pg_maximos_cuenta_como_bloodied() (+4 more)

### Community 60 - "saves.py"
Cohesion: 0.04
Nodes (22): parse_damage_type(), _log_target(), ArcaneArcherFeatures, _ctx_con_rng(), _CtxConRng, _de(), _otros_enemigos(), apply_damage_modifiers() (+14 more)

### Community 61 - "begin_turn"
Cohesion: 0.33
Nodes (13): begin_turn(), _ctx(), _datos(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno(), test_el_troll_carga_su_regeneracion() (+5 more)

### Community 62 - "test_magic_resistance.py"
Cohesion: 0.14
Nodes (21): _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab(), test_condition_action_de_hechizo_pasa_magical() (+13 more)

### Community 63 - "Trait"
Cohesion: 0.05
Nodes (3): Trait, BloodFrenzy, test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 64 - "inflict_damage"
Cohesion: 0.12
Nodes (13): _absorber_pv_temporales(), _avisar_ataque_especial_marca(), _hooks(), inflict_damage(), _is_petrified(), _liberar_turno_extra(), _mark_dead_if_down(), _mitigacion_de_otros() (+5 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.14
Nodes (36): _abilities(), _aliado(), _barbaro(), _ctx(), _fijar_fallo_reaccion(), _furia(), _herald(), _mon() (+28 more)

### Community 66 - "_registrar_mago_falso"
Cohesion: 0.19
Nodes (12): _def_mago_falso(), _guerrero(), _lista_a6(), _oleada(), _registrar_mago_falso(), _apply(), test_apply_class_con_la_clase_falsa_crea_espacios_y_acciones(), test_en_run_combat_el_pj_lanzador_gasta_espacios_sin_excederlos() (+4 more)

### Community 67 - "test_backgrounds.py"
Cohesion: 0.14
Nodes (18): Background, _add(), load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes() (+10 more)

### Community 68 - "_decide"
Cohesion: 0.12
Nodes (19): _conoce_sweeping(), _decide(), _RngIdx, test_el_ataque_de_reaccion_no_activa_maniobras_de_sesion_1(), test_el_uso_no_se_gasta_si_no_se_ejecuta(), test_en_un_fallo_sin_precision_cero_rng(), test_feinting_sin_impacto_no_gasta_el_dado(), test_la_decision_es_un_solo_par_de_picks() (+11 more)

### Community 69 - "apply_fighter"
Cohesion: 0.10
Nodes (38): apply_fighter(), maestria_de(), _abilities(), _firmas(), _pj(), _pj_con_armas(), test_apply_class_fighter_sin_subclase_equivalente_a_apply_fighter(), test_apply_class_reenvía_el_estilo_de_combate() (+30 more)

### Community 70 - "apply_cavalier"
Cohesion: 0.10
Nodes (21): cavalier_mark_uses(), warding_maneuver_uses(), apply_cavalier(), _cavalier(), _firmas(), _pj(), test_apply_cavalier_exige_la_clase_fighter(), test_apply_cavalier_requiere_nivel_3() (+13 more)

### Community 71 - "test_azer.py"
Cohesion: 0.26
Nodes (17): _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), _rasgo(), test_ataque_a_distancia_no_dispara_la_represalia() (+9 more)

### Community 72 - "psionic_dice_count"
Cohesion: 0.16
Nodes (19): psionic_dice_count(), _ataca(), _bajo_golpe(), _parchea_golpe(), _salvacion(), test_el_ataque_adicional_no_activa_psionic_strike_mas_de_una_vez(), test_el_dado_del_psionic_strike_sigue_la_regla_de_criticos_del_motor(), test_el_empuje_de_10_ft_de_telekinetic_thrust_es_dato_sin_efecto() (+11 more)

### Community 73 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 74 - "_parchea_campo"
Cohesion: 0.15
Nodes (16): _amiga(), _parchea_campo(), _recibe(), test_el_protective_field_comparte_la_reaccion_del_turno(), test_el_protective_field_no_actua_con_cero_de_dano(), test_el_protective_field_no_actua_por_debajo_del_nivel_tres(), test_el_protective_field_no_baja_el_daño_de_cero(), test_el_protective_field_no_protege_a_un_enemigo() (+8 more)

### Community 76 - "test_rune_knight.py"
Cohesion: 0.04
Nodes (78): rune_uses(), runes_known_count(), apply_rune_knight(), RuneInvokeAction, AttackModifiers, _abilities(), _accion_storm(), _fuego() (+70 more)

### Community 77 - "test_races.py"
Cohesion: 0.09
Nodes (26): Race, load_race(), parse_race(), _skill_name(), _spells_from_description(), _trait_skills(), _abilities(), _fiendish_legacy() (+18 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.14
Nodes (25): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+17 more)

### Community 79 - "RageAction"
Cohesion: 0.18
Nodes (13): RageAction, apply_berserker(), IntimidatingPresenceAction, _presencia_ctx(), test_apply_anade_trait_y_accion(), test_presencia_afecta_a_un_numero_aleatorio_de_enemigos(), test_presencia_requiere_nivel_14(), test_presencia_sin_rng_no_paga() (+5 more)

### Community 80 - "PsiBulwarkAction"
Cohesion: 0.13
Nodes (19): Psi Warrior (PHB 2024), bulwark_targets(), psionic_die_sides(), _elegibles_bulwark(), PsiBulwarkAction, effective_ac(), _bulwark(), test_bulwark_targets_es_el_mod_de_int_con_minimo_uno() (+11 more)

### Community 81 - "run_combat"
Cohesion: 0.10
Nodes (19): Samurai (XGE), combat_finished(), living_teams(), _objetivo_enganche(), _avisar_ganchos_de_turno(), CombatResult, _invoke_policy(), run_combat() (+11 more)

### Community 82 - "test_arquitectura.py"
Cohesion: 0.21
Nodes (6): Cómo comprobar que todo sigue en orden, _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api()

### Community 83 - "SpellStateAction"
Cohesion: 0.15
Nodes (3): SpellStateAction, _tiene_estado(), SuperiorInvisibility

### Community 84 - "Abilities"
Cohesion: 0.10
Nodes (25): Abilities, _tag_modificadores(), PlayerCharacter, test_sin_condiciones_el_dano_no_cambia(), _guerrero_y_ogro(), _target(), test_attack_roll_log_modifier(), test_danio_medio_por_combatiente_y_equipo() (+17 more)

### Community 85 - "test_spells.py"
Cohesion: 0.10
Nodes (41): parse_spell(), _ctx(), _npc(), _pj(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot() (+33 more)

### Community 86 - "pick"
Cohesion: 0.06
Nodes (8): pick(), actor_is_alive(), _en_accion_de_ataque(), _cd_ataque(), ZealotFeatures, EldritchKnightFeatures, PsiWarriorFeatures, _romper_invisibilidad_al_lanzar()

### Community 87 - "Hechizos de PJ: plan de sesión 1"
Cohesion: 0.12
Nodes (13): SubclassDef, hechizo_soportado(), _legal(), test_al_agotar_un_nivel_las_ofertas_superiores_siguen_disponibles(), Fighter: cómo añadir una subclase, Grafo y verificación, Hechizos de PJ: cómo añadir una clase lanzadora, Hechizos de PJ: pendientes reales (+5 more)

### Community 88 - "json"
Cohesion: 0.14
Nodes (10): _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError (+2 more)

### Community 89 - "test_extra_damage.py"
Cohesion: 0.17
Nodes (18): DamageRecorder, _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional() (+10 more)

### Community 90 - "test_sustituir_ataque.py"
Cohesion: 0.17
Nodes (10): _sustituir_ataque(), _abilities(), _blanco(), _pj(), _RasgoQueSustituye, _RasgoSinSustitucion, _RngExplota, test_rasgo_que_devuelve_none_conserva_el_flujo_y_las_semillas() (+2 more)

### Community 91 - "_carga"
Cohesion: 0.16
Nodes (14): _ataque_carga(), _carga(), _salvacion(), test_ferocious_charger_cd_es_ocho_mas_pb_mas_fuerza(), test_ferocious_charger_con_p_medio_tira_un_random(), test_ferocious_charger_el_flag_se_reinicia_cada_turno(), test_ferocious_charger_nivel_14_no_actua_sin_rng(), test_ferocious_charger_p_cero_no_carga_sin_rng() (+6 more)

### Community 92 - "spell_action"
Cohesion: 0.07
Nodes (17): Paquetes con fachada, AreaSaveAction, HealAction, SpellAction, SpellAttackAction, SpellFixedDamageAction, dado_por_nivel(), duracion_en_rondas() (+9 more)

### Community 93 - "test_ancestral_guardian.py"
Cohesion: 0.10
Nodes (28): AncestralGuardianFeatures, apply_ancestral_guardian(), _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado() (+20 more)

### Community 94 - "_especial"
Cohesion: 0.26
Nodes (11): _accion_marca(), _especial(), _pick_sin_decision(), test_el_ataque_especial_no_gasta_un_uso_ni_la_reaccion(), test_el_ataque_especial_no_suma_dano_extra_si_falla(), test_el_ataque_especial_se_arma_cuando_el_marcado_dana_a_un_tercero(), test_el_ataque_especial_solo_vale_en_el_siguiente_turno(), test_el_ataque_especial_suma_el_dano_extra_si_impacta() (+3 more)

### Community 95 - "barbarian/__init__.py"
Cohesion: 0.07
Nodes (12): _aliados_en_aura(), apply_storm_herald(), _cd(), _dado_mar(), _de(), _en_aura(), _enemigos_en_aura(), _escalado() (+4 more)

### Community 96 - "_abilities"
Cohesion: 0.19
Nodes (18): _abilities(), _marca_con(), _marcado(), _mods(), _RngSi, test_incapacitado_el_marcador_anula_la_marca(), test_la_marca_caduca_en_la_ronda_indicada(), test_la_marca_no_se_consume_y_no_aplica_al_atacar_al_marcador() (+10 more)

### Community 97 - "survival.py"
Cohesion: 0.11
Nodes (5): _es_radiante(), _guardar_salvacion(), Regeneration, Relentless, UndeadFortitude

### Community 98 - "CombatContext"
Cohesion: 0.17
Nodes (3): CombatContext, _living_enemies(), _log()

### Community 99 - "test_zealot.py"
Cohesion: 0.09
Nodes (40): ZealousPresenceAction, _abilities(), _aliado(), _barbaro(), _decision(), _fallos(), _forma(), _guarda_con() (+32 more)

### Community 100 - "test_battlerager.py"
Cohesion: 0.11
Nodes (34): apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), _abilities(), _accion_puas(), _ataque(), _barb() (+26 more)

### Community 101 - "AtaqueSustituido"
Cohesion: 0.11
Nodes (14): Arcane Archer (XGE), AtaqueSustituido, _RngSi, test_arcane_shot_se_aplica_una_sola_vez_por_turno(), test_arcane_shot_se_gasta_un_uso_al_aplicar(), test_daño_de_arcane_shot_es_2d6_antes_del_18(), _dado(), test_daño_de_arcane_shot_es_4d6_desde_el_18() (+6 more)

### Community 102 - "_pj"
Cohesion: 0.22
Nodes (19): espia(), _espiar_divine(), _furia(), _mon(), _pj(), test_determinismo_misma_semilla_mismos_resultados(), corrida(), test_divine_fury_elige_radiante_con_pick() (+11 more)

### Community 103 - "test_psi_warrior.py"
Cohesion: 0.13
Nodes (18): apply_psi_warrior(), _abilities(), _firmas(), _pj(), _psi(), test_apply_class_equivalente_a_apply_psi_warrior(), test_apply_psi_warrior_por_debajo_del_nivel_3_da_value_error(), test_apply_psi_warrior_sin_clase_guerrero_da_value_error() (+10 more)

### Community 104 - "legendary.py"
Cohesion: 0.09
Nodes (12): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), LegendaryAction, LegendaryState (+4 more)

### Community 105 - "load_class_spell_list"
Cohesion: 0.15
Nodes (6): load_class_spell_list(), _get_spell_fixture(), test_la_lista_de_clase_se_parsea_con_nivel_y_escuela(), test_la_lista_se_guarda_en_cache_y_la_segunda_vez_no_toca_la_red(), test_un_hechizo_que_no_existe_se_omite_sin_romper_la_lista(), _get()

### Community 106 - "Attack"
Cohesion: 0.13
Nodes (25): D20Result, Attack, test_commanders_strike_con_relentless_no_gasta_dado(), test_commanders_strike_sustituye_el_ataque_y_el_aliado_gasta_su_reaccion(), _d20(), test_el_dado_de_reaccion_no_se_duplica_en_critico(), _d20(), test_el_motor_decide_y_gasta_el_dado_en_el_ataque() (+17 more)

### Community 107 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 108 - "_escudo_partida"
Cohesion: 0.15
Nodes (13): runic_shield_uses(), _escudo_partida(), _parchea_escudo(), test_cloud_rune_sin_otro_enemigo_no_consulta_pick(), test_runic_shield_convierte_un_impacto_en_fallo(), test_runic_shield_gasta_la_reaccion_compartida(), test_runic_shield_no_actua_por_debajo_del_nivel_siete(), test_runic_shield_no_actua_si_el_golpe_original_falla() (+5 more)

### Community 109 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 110 - "roll_initiative"
Cohesion: 0.27
Nodes (8): roll_initiative(), _d20_fijo(), test_ambush_con_la_decision_no_no_gasta_nada(), test_ambush_con_relentless_no_gasta_dado(), test_ambush_sin_dados_no_consume_rng(), test_ambush_sin_la_maniobra_no_consume_rng(), test_ambush_suma_un_dado_a_la_tirada_de_iniciativa(), test_sin_subclase_roll_initiative_no_consulta_bonus()

### Community 111 - "_arco"
Cohesion: 0.17
Nodes (15): _arco(), _ctx_curving(), _curving(), _RngNo, test_curving_can_use_requiere_bonus_libre(), test_curving_can_use_si_con_la_decision_si(), test_curving_decision_no_no_re_tira(), test_curving_execute_sin_otro_enemigo_no_llama_nada() (+7 more)

### Community 112 - "_arquero"
Cohesion: 0.14
Nodes (15): _arquero(), _RngExplota, test_arcane_shot_crea_usos_por_nivel(), test_arcane_shot_se_reinicia_en_on_turn_start(), test_arcane_shot_sin_rng_no_actua(), test_arcane_shot_sin_usos_cero_rng(), test_ataque_cuerpo_a_cuerpo_cero_rng(), test_cd_de_arcane_shot_es_8_mas_pb_mas_int() (+7 more)

### Community 113 - "_RngExplota"
Cohesion: 0.25
Nodes (4): _RngExplota, test_interception_sin_arma_ni_escudo_no_actúa_y_no_consume_rng(), test_resolver_maestria_sin_maestria_no_consulta_tactical_master(), test_tactical_master_no_sustituye_bajo_el_nivel_9()

### Community 116 - "condition_parser.py"
Cohesion: 0.13
Nodes (5): _condition_from_phrase(), _duration_rounds(), has_condition_text(), _sentence_with(), ConditionEffect

### Community 117 - "apply_champion"
Cohesion: 0.15
Nodes (9): apply_champion(), _de(), _pj(), test_apply_champion_por_debajo_del_nivel_3_da_value_error(), test_apply_champion_sin_clase_guerrero_da_value_error(), test_remarkable_athlete_no_concede_competencia_en_atletismo(), test_sin_champion_la_iniciativa_consume_un_d20_por_combatiente(), test_sin_subclase_no_hay_estilos_extra() (+1 more)

### Community 118 - "_champion"
Cohesion: 0.18
Nodes (13): _champion(), _fighter(), test_defense_como_primero_no_duplica_la_ca(), test_defy_death_es_dato_sin_efecto(), test_el_segundo_estilo_difiere_del_primero_y_esta_en_el_pool(), test_heroic_warrior_es_dato_sin_efecto(), test_kwarg_estilo_inventado_da_value_error(), test_kwarg_explicito_de_estilo_adicional_valido() (+5 more)

### Community 119 - "BerserkerFeatures"
Cohesion: 0.15
Nodes (4): _armas_melee_de(), BerserkerFeatures, _de(), _furia_de()

### Community 120 - "_estado"
Cohesion: 0.50
Nodes (3): _estado(), test_el_estado_legendario_rellena_gasta_y_reinicia(), test_use_probability_medio_se_usa_about_50_por_ciento()

### Community 121 - "build_spell_actions"
Cohesion: 0.18
Nodes (11): build_spell_actions(), parse_spellcasting(), _desde_fixture(), _monstruo_lanzador(), test_el_lanzador_se_lee_de_los_actions(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_la_reaccion_gasta_su_uso_propio(), test_max_spell_level_limita_el_nivel_cargado() (+3 more)

### Community 122 - "_guardado"
Cohesion: 0.15
Nodes (8): _guardado(), test_guarded_mind_con_pick_no_no_purga_ni_gasta(), test_guarded_mind_concede_resistencia_psiquica_a_partir_del_nivel_10(), test_guarded_mind_no_actua_por_debajo_del_nivel_diez(), test_guarded_mind_purga_charmed_y_frightened_gastando_un_dado(), test_guarded_mind_sin_condicion_no_consulta_pick(), test_guarded_mind_sin_ctx_rng_no_purga(), test_guarded_mind_sin_dados_no_purga()

### Community 123 - "SaveResult"
Cohesion: 0.20
Nodes (13): SaveResult, fake_saving_throw(), _fake(), falla(), _fijar_salvacion(), espia(), stub(), stub() (+5 more)

### Community 125 - "WarriorHealAction"
Cohesion: 0.25
Nodes (15): WarriorHealAction, _accion(), _ctx(), test_fanatical_no_activo_sin_furia(), test_nivel_3_no_recibe_rasgos_superiores(), test_warrior_curacion_gasta_un_dado_y_suma_pv(), test_warrior_curacion_no_supera_el_maximo(), test_warrior_de_los_dioses_reserva_por_nivel() (+7 more)

### Community 126 - "test_cavalier.py"
Cohesion: 0.10
Nodes (36): cavalier_mark_extra_damage(), _bajo_ataque(), _cargar_main(), _defiende(), _parchea_ataque(), _parchea_warding(), _RngExplota, test_daño_extra_del_ataque_especial_es_el_nivel_entre_dos() (+28 more)

### Community 128 - "random"
Cohesion: 0.26
Nodes (18): _abilities(), _ctx(), _decide(), _pj(), test_antes_del_nivel_2_no_hay_decision_ni_rng(), test_en_turno_ajeno_no_decide(), test_frecuencia_0_5_es_aproximadamente_la_mitad_de_los_turnos(), test_las_reacciones_no_deciden_ni_reciben() (+10 more)

### Community 129 - ".on_turn_start"
Cohesion: 0.21
Nodes (3): _aliados_heridos(), _de(), _en_10_pies()

### Community 130 - "ConditionAction"
Cohesion: 0.24
Nodes (5): _check_fields(), _construir(), _error(), SaveAction, ConditionAction

### Community 131 - "Combatant"
Cohesion: 0.11
Nodes (7): Arquitectura de `dnd_sim`, Carpetas, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, Combatant

### Community 132 - "_clamp"
Cohesion: 0.12
Nodes (11): action_surge_uses(), _clamp(), fighter_extra_attacks_for(), indomitable_uses(), second_wind_uses(), weapon_mastery_count(), test_action_surge_usos_por_nivel_son_1_y_2(), test_indomitable_usos_por_nivel_son_1_2_y_3() (+3 more)

### Community 134 - "test_lair.py"
Cohesion: 0.09
Nodes (30): load_lair(), lair_phase(), LairAction, _ctx(), _dragon(), _enemigo(), lairs_dir(), _orden_con() (+22 more)

### Community 135 - "_RngSi"
Cohesion: 0.24
Nodes (6): _check_fallada(), _RngSi, test_tactical_mind_no_gasta_el_uso_si_aun_asi_falla(), test_tactical_mind_sin_ctx_no_actua(), test_tactical_mind_sin_usos_no_actua_y_no_consume_rng(), test_tactical_mind_suma_d10_y_gasta_un_uso_si_la_tirada_final_pasa()

### Community 136 - "_abilities"
Cohesion: 0.39
Nodes (8): _abilities(), _parchea_d20(), test_ataque_de_hechizo_no_usa_el_umbral_de_champion(), test_el_critico_con_19_impacta_aunque_no_alcance_la_ca(), test_el_rango_ampliado_a_18_solo_funciona_desde_el_nivel_15(), test_el_un_natural_sigue_fallen_do_para_un_champion(), test_un_no_champion_con_19_falla_contra_la_misma_ca(), test_warding_no_convierte_en_fallo_un_critico_por_rango_ampliado()

### Community 137 - "test_la_desventaja_de_iniciativa_tira_dos_d20_y_toma_el_menor"
Cohesion: 0.25
Nodes (4): test_la_desventaja_de_iniciativa_tira_dos_d20_y_toma_el_menor(), test_la_iniciativa_tira_dos_d20_y_toma_el_mayor_solo_para_el_champion(), test_los_dados_del_critico_se_doblan_con_el_rango_ampliado(), espia()

### Community 138 - "caster.py"
Cohesion: 0.10
Nodes (11): Hechizos de PJ (PHB 2024), spell_slots_for(), SpellcastingDef, aplicar_lanzamiento(), estadisticas_lanzador(), PCSpellcasting, PJSpellAction, test_spell_slots_for_con_progresión_desconocida_es_un_value_error() (+3 more)

### Community 139 - "Any"
Cohesion: 0.29
Nodes (3): _as_condition(), _condicion_bloqueada(), _contar()

### Community 140 - "dnd_sim/__init__.py"
Cohesion: 0.03
Nodes (26): ability_mod(), normalize_ability(), normalize_tool(), _clean(), normalize_skill(), parse_attach_effects(), has_escape_text(), _extract_multiattack_alternatives() (+18 more)

### Community 144 - "test_apply_class_equivalente_a_apply_champion"
Cohesion: 0.40
Nodes (3): _firmas(), test_apply_class_equivalente_a_apply_champion(), _trait()

## Knowledge Gaps
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Condition` connect `Condition` to `test_attach.py`, `AttackRange`, `Combatant`, `test_giant.py`, `test_wild_heart.py`, `test_lair.py`, `test_legendary.py`, `test_beast.py`, `spell_parser.py`, `test_traits.py`, `Any`, `dnd_sim/__init__.py`, `test_utility.py`, `legendary_parser.py`, `test_eldritch_knight.py`, `test_hechizos_pj.py`, `test_battle_master.py`, `test_samurai.py`, `attack_roll`, `test_world_tree.py`, `test_parry.py`, `.can_act`, `Monster`, `load_monster`, `RollMode`, `RuneKnightFeatures`, `test_skills.py`, `roll_dice`, `test_arcane_archer.py`, `SpellSlots`, `saving_throw`, `test_mastery.py`, `BarbarianFeatures`, `apply_condition`, `ActionType`, `TelekineticMasterAction`, `BattleMasterFeatures`, `_atacado`, `test_checks_escapes.py`, `test_condition_immunities.py`, `test_champion.py`, `saves.py`, `test_magic_resistance.py`, `inflict_damage`, `test_storm_herald.py`, `psionic_dice_count`, `test_pack_tactics.py`, `ConditionTracker`, `test_rune_knight.py`, `test_enlarge.py`, `RageAction`, `PsiBulwarkAction`, `SpellStateAction`, `Abilities`, `test_spells.py`, `pick`, `_carga`, `spell_action`, `barbarian/__init__.py`, `_abilities`, `test_psi_warrior.py`, `condition_parser.py`, `BerserkerFeatures`, `_guardado`, `test_cavalier.py`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `daño_base_arma()`) actually correct?**
  _`Attack` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `_fighter` be split into smaller, more focused modules?**
  _Cohesion score 0.12554112554112554 - nodes in this community are weakly interconnected._
- **Why does `Attack` connect `Attack` to `_fighter`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_traits.py`, `test_hechizos_pj.py`, `test_utility.py`, `test_wild_magic.py`, `legendary_parser.py`, `test_eldritch_knight.py`, `test_battle_master.py`, `test_samurai.py`, `apply_class`, `attack_roll`, `apply_barbarian`, `test_parry.py`, `test_death.py`, `Monster`, `load_monster`, `_ExplotaSiUsaRng`, `test_arcane_archer.py`, `test_mastery.py`, `apply_condition`, `ActionType`, `Condition`, `_atacado`, `main.py`, `test_checks_escapes.py`, `TurnResources`, `test_champion.py`, `begin_turn`, `test_magic_resistance.py`, `test_storm_herald.py`, `_registrar_mago_falso`, `_decide`, `apply_fighter`, `apply_cavalier`, `test_azer.py`, `psionic_dice_count`, `test_pack_tactics.py`, `test_rune_knight.py`, `test_enlarge.py`, `Abilities`, `test_spells.py`, `test_extra_damage.py`, `test_sustituir_ataque.py`, `_carga`, `spell_action`, `test_ancestral_guardian.py`, `_abilities`, `test_zealot.py`, `test_battlerager.py`, `AtaqueSustituido`, `_pj`, `test_psi_warrior.py`, `_escudo_partida`, `test_undead_fortitude.py`, `_arco`, `_arquero`, `_RngExplota`, `apply_champion`, `_champion`, `test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio`, `test_cavalier.py`, `random`, `ConditionAction`, `Combatant`, `_abilities`, `test_la_desventaja_de_iniciativa_tira_dos_d20_y_toma_el_menor`, `dnd_sim/__init__.py`, `_golpe_sin_armas`, `test_sustitucion_hace_un_solo_par_de_picks`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Are the 168 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 168 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11627906976744186 - nodes in this community are weakly interconnected._
- **Why does `Trait` connect `Trait` to `test_giant.py`, `test_wild_heart.py`, `test_traits.py`, `dnd_sim/__init__.py`, `test_samurai.py`, `attack_roll`, `test_parry.py`, `.can_act`, `RuneKnightFeatures`, `FighterFeatures`, `roll_dice`, `BarbarianFeatures`, `ActionType`, `BattleMasterFeatures`, `valid_targets`, `BeastFeatures`, `test_condition_immunities.py`, `saves.py`, `SpellStateAction`, `pick`, `test_sustituir_ataque.py`, `spell_action`, `test_ancestral_guardian.py`, `barbarian/__init__.py`, `survival.py`, `test_battlerager.py`, `BerserkerFeatures`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
# Graph Report - DnDBalancer  (2026-11-13)

## Corpus Check
- 232 files · ~232,800 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 4262 nodes · 15557 edges · 136 communities (118 shown, 18 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 1104 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4b94abca`
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
- _fighter
- test_battle_master.py
- _ejecuta
- test_loader_actions.py
- apply_class
- ArcaneArcherFeatures
- ActionUsage
- apply_barbarian
- Abilities
- ZealotFeatures
- WarriorHealAction
- test_death.py
- Monster
- TurnResources
- test_parry.py
- saves.py
- FighterFeatures
- _ExplotaSiUsaRng
- test_skills.py
- test_undead_fortitude.py
- test_arcane_archer.py
- test_multiattack.py
- dnd_sim/__init__.py
- inflict_damage
- test_mastery.py
- BarbarianFeatures
- test_conditions.py
- roll_dice
- test_area.py
- TelekineticMasterAction
- Condition
- BattleMasterFeatures
- _atacado
- main.py
- test_checks_escapes.py
- load_monster
- _trait
- legendary_phase
- apply_condition
- combat/attack.py
- test_champion.py
- test_magic_resistance.py
- begin_turn
- .ataque_de_oportunidad
- Trait
- legendary_parser.py
- test_storm_herald.py
- roll_modifiers.py
- test_backgrounds.py
- _pj
- apply_fighter
- apply_cavalier
- test_lair.py
- test_psi_warrior.py
- test_pack_tactics.py
- _parchea_campo
- ConditionInstance
- json
- PlayerCharacter
- test_enlarge.py
- parse_spellcasting
- PsiBulwarkAction
- run_combat
- Arquitectura de `dnd_sim`
- CombatContext
- combat/__init__.py
- test_spells.py
- _RngMax
- test_azer.py
- GiantFeatures
- test_extra_damage.py
- test_sustituir_ataque.py
- _carga
- psionic_dice_count
- test_ancestral_guardian.py
- test_cavalier.py
- lair_loader.py
- _abilities
- _clamp
- WorldTreeFeatures
- test_zealot.py
- random
- AtaqueSustituido
- test_el_gancho_after_failed_check_desde_ability_check_con_ctx
- apply_psi_warrior
- Any
- PsiWarriorFeatures
- Attack
- _especial
- condition_parser.py
- .alive
- roll_initiative
- _arquero
- capas.py
- _RngExplota
- attach.py
- CombatState
- test_piercing_k_uniforme_y_atacante_nunca_es_objetivo
- simulate
- test_tactical_master_nivel_9_elige_entre_original_push_sap_slow
- ataque_utilitario
- test_sustitucion_hace_un_solo_par_de_picks
- build_spell_actions
- spell_action
- SaveResult
- parse_escape
- _FixedRandom
- .proteccion_psionica
- _estado
- extra_attacks_for
- LegendaryAction
- test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio
- test_la_resistencia_funciona_en_todas_las_rutas
- test_resistance_probability_medio_convierte_about_50_por_ciento
- test_el_cli_tiene_las_opciones_legendarias

## God Nodes (most connected - your core abstractions)
1. `Attack` - 266 edges
2. `Monster` - 212 edges
3. `Condition` - 206 edges
4. `attack_roll()` - 191 edges
5. `AttackRange` - 188 edges
6. `apply_condition()` - 170 edges
7. `Abilities` - 157 edges
8. `PlayerCharacter` - 140 edges
9. `load_monster()` - 136 edges
10. `pick()` - 125 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Fighter: cómo añadir una subclase` --references--> `SubclassDef`  [INFERRED]
  TODO.md → dnd_sim/rules/classes/base.py
- `Champion: plan de sesión` --references--> `_clamp()`  [INFERRED]
  TODO.md → dnd_sim/core/classes.py

## Import Cycles
- None detected.

## Communities (136 total, 18 thin omitted)

### Community 0 - "test_fighter.py"
Cohesion: 0.12
Nodes (16): _abilities(), _action_surge(), _ctx_recursos(), _firmas(), _pj_con_armas(), _RngBajo, test_action_surge_como_maximo_un_vez_por_turno(), test_action_surge_ejecutada_restaura_la_accion_y_gasta_un_uso() (+8 more)

### Community 1 - "test_attach.py"
Cohesion: 0.18
Nodes (25): _atacar(), _bite(), _cloaker(), _ctx(), _datos(), _pj(), test_con_ventaja_el_enganche_es_a_la_cabeza_y_ciega(), test_damage_transfer_no_aplica_sin_enganche() (+17 more)

### Community 2 - "AttackRange"
Cohesion: 0.08
Nodes (54): AttackRange, apply_berserker(), _armas_melee_de(), BerserkerFeatures, _de(), _golpe_sin_armas(), IntimidatingPresenceAction, _abilities() (+46 more)

### Community 3 - "test_giant.py"
Cohesion: 0.13
Nodes (33): apply_giant(), MightyImpelAction, _abilities(), _barbaro(), _ctx(), _furia(), _giant(), _mon() (+25 more)

### Community 4 - "test_world_tree.py"
Cohesion: 0.11
Nodes (39): apply_world_tree(), _abilities(), _aliado(), _barbaro(), _ctx(), _decision(), _elige_candidato(), espia() (+31 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.07
Nodes (49): apply_wild_heart(), _con_beneficio(), _de(), _en_5_pies(), _hostil(), _orden_de(), WildHeartFeatures, _abilities() (+41 more)

### Community 6 - "test_proficiency.py"
Cohesion: 0.18
Nodes (20): ability_check_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia() (+12 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.12
Nodes (27): _data(), _load(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_el_ala_que_mezcla_movimiento_avisa(), test_el_cantrip_del_lich_se_omite_con_aviso(), test_el_detect_del_dragon_se_omite_con_aviso(), test_el_dragon_carga_sus_acciones_legendarias() (+19 more)

### Community 8 - "test_beast.py"
Cohesion: 0.06
Nodes (70): WeaponAttackAction, apply_beast(), BeastFeatures, CallTheHuntBonus, _habilitar_armas_naturales(), _abilities(), _barb(), _beast() (+62 more)

### Community 9 - "spell_parser.py"
Cohesion: 0.08
Nodes (13): _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla(), _frases() (+5 more)

### Community 10 - "test_traits.py"
Cohesion: 0.05
Nodes (50): _declara_uso(), _entradas(), parse_traits(), _usage(), BloodFrenzy, _aliado(), _ctx(), _datos() (+42 more)

### Community 11 - "_arco"
Cohesion: 0.17
Nodes (15): _arco(), _ctx_curving(), _curving(), _RngNo, test_curving_can_use_requiere_bonus_libre(), test_curving_can_use_si_con_la_decision_si(), test_curving_decision_no_no_re_tira(), test_curving_execute_sin_otro_enemigo_no_llama_nada() (+7 more)

### Community 12 - "test_utility.py"
Cohesion: 0.22
Nodes (21): _abilities(), _ctx(), _mon(), _pj(), _siempre_falla(), test_actor_no_disponible_no_consulta_la_probabilidad(), test_agarrar_admite_hasta_un_tamano_mayor(), test_agarrar_aplica_agarrado_con_escape_de_acción() (+13 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.07
Nodes (43): apply_wild_magic(), _sombra(), WildMagicFeatures, WildSurgeAction, _abilities(), _barbaro(), _con_cola(), _con_efecto() (+35 more)

### Community 14 - "loader.py"
Cohesion: 0.07
Nodes (16): parse_range_type(), _resistencia_legendaria(), _extract_multiattack_alternatives(), _norm_name(), _parse_condition_immunities(), _parse_damage_modifiers(), extract_multiattack_alternatives(), _norm_name() (+8 more)

### Community 15 - "Regeneration"
Cohesion: 0.11
Nodes (5): _es_radiante(), _guardar_salvacion(), Regeneration, Relentless, UndeadFortitude

### Community 16 - "_fighter"
Cohesion: 0.12
Nodes (26): _ctx(), _fighter(), _mods(), _save_fallada(), _saving_nueva(), _second_wind(), test_action_surge_no_existe_en_nivel_1(), test_ataques_estudiados_caduca_al_final_del_siguiente_turno() (+18 more)

### Community 17 - "test_battle_master.py"
Cohesion: 0.07
Nodes (42): maneuvers_known_count(), superiority_dice_count(), superiority_die_sides(), apply_battle_master(), _abilities(), _atacado_dos_enemigos(), _atacado_fijo(), _bm() (+34 more)

### Community 18 - "_ejecuta"
Cohesion: 0.14
Nodes (18): _ejecuta(), _mods(), _RngFalla, test_disarming_attack_no_altera_el_combate_mas_que_el_dano(), test_distracting_da_ventaja_a_un_tercero_y_se_consume(), test_distracting_no_concede_ventaja_si_ya_caduco(), test_distracting_no_da_ventaja_al_marcador_ni_se_consume(), test_efectos_sin_implementacion_no_alteran_el_combate() (+10 more)

### Community 19 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (14): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+6 more)

### Community 20 - "apply_class"
Cohesion: 0.12
Nodes (19): apply_class(), ClassDef, normalize_class_name(), register_class(), SubclassDef, _abilities(), _firmas(), _pj() (+11 more)

### Community 21 - "ArcaneArcherFeatures"
Cohesion: 0.09
Nodes (5): ArcaneArcherFeatures, _ctx_con_rng(), _CtxConRng, _de(), _otros_enemigos()

### Community 22 - "ActionUsage"
Cohesion: 0.09
Nodes (15): ExtendRageAction, RageAction, _rasgo(), _furia_de(), ActionUsage, UsageKind, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar() (+7 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.08
Nodes (52): rage_uses(), apply_barbarian(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj(), _resultado() (+44 more)

### Community 24 - "Abilities"
Cohesion: 0.19
Nodes (17): Abilities, remove_invisibility_on_action(), test_las_condiciones_incapacitantes_no_fallan_automaticamente_la_con(), test_petrificado_tiene_resistencia_a_todo(), test_sin_condiciones_el_dano_no_cambia(), test_un_petrificado_resiste_y_el_log_lo_dice(), _accion(), _ctx() (+9 more)

### Community 25 - "ZealotFeatures"
Cohesion: 0.08
Nodes (13): apply_zealot(), _de(), _en_60_pies(), _es_aliado(), _furia_de(), _reserva_dados(), ZealotFeatures, ZealousPresenceAction (+5 more)

### Community 26 - "WarriorHealAction"
Cohesion: 0.25
Nodes (15): WarriorHealAction, _accion(), _ctx(), test_fanatical_no_activo_sin_furia(), test_nivel_3_no_recibe_rasgos_superiores(), test_warrior_curacion_gasta_un_dado_y_suma_pv(), test_warrior_curacion_no_supera_el_maximo(), test_warrior_de_los_dioses_reserva_por_nivel() (+7 more)

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 28 - "Monster"
Cohesion: 0.13
Nodes (26): Monster, _abilities(), _disparo(), _RngFalla, test_banishing_arrow_falla_la_salvacion_y_deja_incapacitado(), test_banishing_arrow_salvacion_exitosa_no_aplica_condicion(), test_beguiling_arrow_hechiza_y_termina_si_el_aliado_ataca(), test_beguiling_sin_aliados_no_tira_salvacion() (+18 more)

### Community 29 - "TurnResources"
Cohesion: 0.16
Nodes (10): AttackAction, TurnResources, _contexto_de_reaccion(), _ctx(), _spell_data(), _spellcasting(), test_el_proyectil_magico_dana_completo_al_ghost(), test_las_armas_dinamicas_de_la_furia_heredan_el_flag() (+2 more)

### Community 30 - "test_parry.py"
Cohesion: 0.27
Nodes (20): _arquero_parry(), _ataque(), _ctx(), _datos(), _fijar_d20(), espia(), _gladiador(), _pj() (+12 more)

### Community 31 - "saves.py"
Cohesion: 0.08
Nodes (19): ability_mod(), _log_target(), apply_damage_modifiers(), _is_petrified(), legendary_resistance(), apply_save_damage(), _as_combat_context(), _avisar_fallo_salvacion() (+11 more)

### Community 32 - "FighterFeatures"
Cohesion: 0.06
Nodes (11): Champion (PHB 2024), champion_crit_threshold(), heroic_rally_amount(), ActionSurgeAction, _en_5_pies(), FighterFeatures, _rasgo(), apply_champion() (+3 more)

### Community 33 - "_ExplotaSiUsaRng"
Cohesion: 0.13
Nodes (25): _accion_rally(), _commanda(), _ExplotaSiUsaRng, _ripostea_directa(), _sustituye(), test_commanders_strike_cede_el_ataque_si_hay_feinting_encolado(), test_commanders_strike_no_se_decide_si_el_aliado_no_tiene_armas(), test_commanders_strike_no_se_decide_si_el_aliado_ya_uso_su_reaccion() (+17 more)

### Community 34 - "test_skills.py"
Cohesion: 0.06
Nodes (34): _clean(), normalize_skill(), skill_ability(), _avisar_fallo_prueba(), CheckResult, _finish_check(), _guia(), _resolve_mods() (+26 more)

### Community 35 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 36 - "test_arcane_archer.py"
Cohesion: 0.11
Nodes (23): arcane_shot_options_known(), arcane_shot_uses(), apply_arcane_archer(), CurvingShotAction, _firmas(), _pj(), test_accion_curving_se_anade_desde_el_nivel_7(), test_apply_arcane_archer_exige_la_clase_fighter() (+15 more)

### Community 37 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 38 - "dnd_sim/__init__.py"
Cohesion: 0.05
Nodes (27): proficiency_bonus(), pick(), sample(), combat_finished(), living_teams(), _objetivo_enganche(), valid_targets(), CombatResult (+19 more)

### Community 39 - "inflict_damage"
Cohesion: 0.12
Nodes (20): _absorber_pv_temporales(), _hooks(), inflict_damage(), _mitigacion_de_otros(), _notify_damage_dealt(), _salvar_a_cero(), test_inflict_damage_registra_la_bandera_magical(), test_un_pj_beast_nivel_6_dana_completo_al_ghost() (+12 more)

### Community 40 - "test_mastery.py"
Cohesion: 0.09
Nodes (30): al_acertar(), al_fallar(), _cd_topple(), consumir_marcas(), _log(), maestria_de(), _nombre(), resolver_maestria() (+22 more)

### Community 41 - "BarbarianFeatures"
Cohesion: 0.12
Nodes (3): BarbarianFeatures, test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 42 - "test_conditions.py"
Cohesion: 0.07
Nodes (53): end_turn(), _label(), RepeatSave, resolve_attack_range(), _ataque(), _ctx(), _data(), _duelo() (+45 more)

### Community 43 - "roll_dice"
Cohesion: 0.05
Nodes (20): rage_damage(), roll_dice(), DamageType, parse_damage_type(), log_line(), _contexto(), FormOfTheBeast, NaturalWeapon (+12 more)

### Community 44 - "test_area.py"
Cohesion: 0.17
Nodes (23): AreaSaveAction, AreaTargeting, select_area_targets(), _default_targeting(), SaveDamage, _area_action(), _ctx(), _npc() (+15 more)

### Community 45 - "TelekineticMasterAction"
Cohesion: 0.11
Nodes (16): _armas_de(), _de(), _telekinetic_master_vigente(), TelekineticMasterAction, TelekineticMasterAttackAction, _master(), test_el_ataque_adicional_exige_efecto_activo_y_bonus_libre(), test_el_ataque_adicional_usa_el_helper_de_ataque_del_motor() (+8 more)

### Community 46 - "Condition"
Cohesion: 0.19
Nodes (26): Condition, attack_modifiers(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+18 more)

### Community 47 - "BattleMasterFeatures"
Cohesion: 0.06
Nodes (10): Battle Master (PHB 2024), StormAuraAction, _aliados(), _aliados_elegibles(), _armas_melee_propias(), _armas_propias(), BattleMasterFeatures, BattleMasterRallyAction (+2 more)

### Community 48 - "_atacado"
Cohesion: 0.06
Nodes (42): FeintingAttackAction, _accion_feinting(), _atacado(), _conoce_sweeping(), _decide(), _parry(), _RngIdx, _RngNo (+34 more)

### Community 49 - "main.py"
Cohesion: 0.10
Nodes (23): CLI del simulador: `build_parser()`, Detalle por flag, Ejemplos, Flujo de `main()`, `--legendary-p`, `--legendary-points`, `--monster` / `-m`, Observaciones (para humanos y IA) (+15 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.08
Nodes (47): ability_check(), EscapeCheck, _ataque(), _check_fijo(), _fake(), _ctx(), _data(), _duelo() (+39 more)

### Community 51 - "load_monster"
Cohesion: 0.07
Nodes (23): _armor_class_value(), _damage_type(), load_monster(), ExtraDamage, CombatantType, test_una_condicion_desconocida_de_la_api_avisa(), _load_fixture(), _ogre_data() (+15 more)

### Community 52 - "_trait"
Cohesion: 0.18
Nodes (21): _aliado(), _check_fallada(), _con_estilo(), _enemigo(), _RngSi, test_interception_con_un_aliado_no_baja_de_cero_el_daño(), test_interception_no_actúa_con_la_reacción_gastada(), test_interception_no_actúa_contra_un_no_aliado_ni_con_el_mismo_pj() (+13 more)

### Community 53 - "legendary_phase"
Cohesion: 0.17
Nodes (22): legendary_phase(), _contexto(), _pj(), test_con_una_sola_accion_asequible_pick_no_consume_rng(), test_dos_duenos_legendarios_actuan_cada_uno_una_vez(), test_el_combate_termina_en_medio_de_la_fase(), test_la_fase_ocurre_despues_del_end_turn(), test_no_actua_si_el_combate_ya_terminado() (+14 more)

### Community 54 - "apply_condition"
Cohesion: 0.08
Nodes (20): _apply_condition_riders(), apply_condition(), _as_condition(), _condicion_bloqueada(), ConditionAction, _ctx(), _ghoul(), _InmuneMientrasActivo (+12 more)

### Community 57 - "combat/attack.py"
Cohesion: 0.07
Nodes (21): Cavalier (XGE), _actualizar_distancia(), _agrandado(), _bando_del(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque() (+13 more)

### Community 59 - "test_champion.py"
Cohesion: 0.06
Nodes (52): _abilities(), _champion(), _fighter(), _firmas(), _parchea_d20(), _pj(), _rally(), test_apply_champion_por_debajo_del_nivel_3_da_value_error() (+44 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.11
Nodes (23): _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_condition_action_de_hechizo_pasa_magical(), spy() (+15 more)

### Community 61 - "begin_turn"
Cohesion: 0.27
Nodes (15): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+7 more)

### Community 62 - ".ataque_de_oportunidad"
Cohesion: 0.18
Nodes (3): _armas_melee_de(), CavalierMarkAttackAction, _de()

### Community 63 - "Trait"
Cohesion: 0.03
Nodes (11): Trait, DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, aliados_capaces(), _condicion_posicional() (+3 more)

### Community 64 - "legendary_parser.py"
Cohesion: 0.08
Nodes (17): _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary(), _por_datos() (+9 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.05
Nodes (46): _aliados_en_aura(), apply_storm_herald(), _cd(), _dado_mar(), _de(), _en_aura(), _enemigos_en_aura(), _escalado() (+38 more)

### Community 66 - "roll_modifiers.py"
Cohesion: 0.10
Nodes (16): _condiciones(), evaluar_d20(), _hooks(), _instancias(), save_modifiers(), umbral_critico(), test_sin_subclase_el_umbral_de_critico_es_20_sin_rng(), test_inmovilizado_da_desventaja_solo_en_des() (+8 more)

### Community 67 - "test_backgrounds.py"
Cohesion: 0.10
Nodes (20): Background, normalize_tool(), get_background(), _add(), load_background(), parse_background(), _abilities(), _pj() (+12 more)

### Community 68 - "_pj"
Cohesion: 0.22
Nodes (19): espia(), _espiar_divine(), _furia(), _mon(), _pj(), test_determinismo_misma_semilla_mismos_resultados(), corrida(), test_divine_fury_elige_radiante_con_pick() (+11 more)

### Community 69 - "apply_fighter"
Cohesion: 0.11
Nodes (31): apply_fighter(), _objetivo(), _pj(), test_apply_class_reenvía_el_estilo_de_combate(), test_apply_fighter_acepta_las_habilidades_de_la_lista(), test_apply_fighter_anade_el_rasgo_guerrero(), test_apply_fighter_asigna_salvaciones_de_fue_y_con(), test_apply_fighter_rechaza_habilidades_fuera_de_la_lista() (+23 more)

### Community 70 - "apply_cavalier"
Cohesion: 0.10
Nodes (19): cavalier_mark_uses(), warding_maneuver_uses(), apply_cavalier(), CavalierFeatures, _cavalier(), _firmas(), _pj(), test_apply_cavalier_exige_la_clase_fighter() (+11 more)

### Community 71 - "test_lair.py"
Cohesion: 0.07
Nodes (32): lair_phase(), LairAction, LegendaryState, _ctx(), _dragon(), _enemigo(), lairs_dir(), _orden_con() (+24 more)

### Community 72 - "test_psi_warrior.py"
Cohesion: 0.19
Nodes (19): _ataca(), _bajo_golpe(), _parchea_golpe(), _salvacion(), test_el_ataque_adicional_no_activa_psionic_strike_mas_de_una_vez(), test_el_dado_del_psionic_strike_sigue_la_regla_de_criticos_del_motor(), test_el_empuje_de_10_ft_de_telekinetic_thrust_es_dato_sin_efecto(), test_el_flag_de_psionic_strike_se_reinicia_cada_turno() (+11 more)

### Community 73 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 74 - "_parchea_campo"
Cohesion: 0.14
Nodes (16): _amiga(), _parchea_campo(), _recibe(), test_el_protective_field_comparte_la_reaccion_del_turno(), test_el_protective_field_no_actua_con_cero_de_dano(), test_el_protective_field_no_actua_por_debajo_del_nivel_tres(), test_el_protective_field_no_baja_el_daño_de_cero(), test_el_protective_field_no_protege_a_un_enemigo() (+8 more)

### Community 75 - "ConditionInstance"
Cohesion: 0.20
Nodes (4): ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab()

### Community 76 - "json"
Cohesion: 0.15
Nodes (5): _cache_path(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError

### Community 77 - "PlayerCharacter"
Cohesion: 0.08
Nodes (30): Race, _get_entry(), get_race(), get_trait(), load_race(), parse_race(), _skill_name(), _spells_from_description() (+22 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.14
Nodes (25): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+17 more)

### Community 79 - "parse_spellcasting"
Cohesion: 0.22
Nodes (4): parse_spellcasting(), test_el_lanzador_se_lee_de_los_actions(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 80 - "PsiBulwarkAction"
Cohesion: 0.12
Nodes (20): Psi Warrior (PHB 2024), bulwark_targets(), _dano_extra_de_rasgo(), _elegibles_bulwark(), PsiBulwarkAction, remove_condition(), effective_ac(), _bulwark() (+12 more)

### Community 81 - "run_combat"
Cohesion: 0.22
Nodes (12): run_combat(), _summarize_damage(), _eventos(), _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(), test_copias_de_un_monstruo_tienen_estado_independiente(), test_dos_combates_seguidos_empiezan_con_el_aliento_cargado() (+4 more)

### Community 82 - "Arquitectura de `dnd_sim`"
Cohesion: 0.12
Nodes (12): Arquitectura de `dnd_sim`, Carpetas, Cómo comprobar que todo sigue en orden, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, _capa() (+4 more)

### Community 83 - "CombatContext"
Cohesion: 0.08
Nodes (12): _nuevo_ctx(), actor_is_alive(), CombatContext, _en_accion_de_ataque(), _living_enemies(), _log(), HealAction, _romper_invisibilidad_al_lanzar() (+4 more)

### Community 84 - "combat/__init__.py"
Cohesion: 0.16
Nodes (14): _tag_modificadores(), _guerrero_y_ogro(), _target(), test_attack_roll_log_modifier(), test_danio_medio_por_combatiente_y_equipo(), test_etiqueta_de_modificadores_se_deriva_del_dano_final(), test_immunity_zero(), test_invalid_damage_type_raises() (+6 more)

### Community 85 - "test_spells.py"
Cohesion: 0.10
Nodes (42): parse_spell(), _ctx(), _npc(), _pj(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot() (+34 more)

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
Cohesion: 0.17
Nodes (10): _sustituir_ataque(), _abilities(), _blanco(), _pj(), _RasgoQueSustituye, _RasgoSinSustitucion, _RngExplota, test_rasgo_que_devuelve_none_conserva_el_flujo_y_las_semillas() (+2 more)

### Community 91 - "_carga"
Cohesion: 0.18
Nodes (13): _ataque_carga(), _carga(), _salvacion(), test_ferocious_charger_cd_es_ocho_mas_pb_mas_fuerza(), test_ferocious_charger_con_p_medio_tira_un_random(), test_ferocious_charger_el_flag_se_reinicia_cada_turno(), test_ferocious_charger_nivel_14_no_actua_sin_rng(), test_ferocious_charger_p_cero_no_carga_sin_rng() (+5 more)

### Community 92 - "psionic_dice_count"
Cohesion: 0.14
Nodes (12): psionic_dice_count(), _guardado(), _psi(), test_guarded_mind_con_pick_no_no_purga_ni_gasta(), test_guarded_mind_purga_charmed_y_frightened_gastando_un_dado(), test_guarded_mind_sin_condicion_no_consulta_pick(), test_guarded_mind_sin_ctx_rng_no_purga(), test_guarded_mind_sin_dados_no_purga() (+4 more)

### Community 93 - "test_ancestral_guardian.py"
Cohesion: 0.10
Nodes (28): AncestralGuardianFeatures, apply_ancestral_guardian(), _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado() (+20 more)

### Community 94 - "test_cavalier.py"
Cohesion: 0.11
Nodes (29): cavalier_mark_extra_damage(), _bajo_ataque(), _cargar_main(), _defiende(), _RngExplota, test_daño_extra_del_ataque_especial_es_el_nivel_entre_dos(), test_el_flag_charge_p_llega_al_rasgo(), test_flag_charge_p_en_el_cli() (+21 more)

### Community 95 - "lair_loader.py"
Cohesion: 0.17
Nodes (8): _check_fields(), _construir(), _error(), load_lair(), ConditionEffect, test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), test_esquema_invalido(), test_targeting_fuera_de_rango()

### Community 96 - "_abilities"
Cohesion: 0.20
Nodes (17): _abilities(), _marca_con(), _marcado(), _mods(), _RngSi, test_incapacitado_el_marcador_anula_la_marca(), test_la_marca_caduca_en_la_ronda_indicada(), test_la_marca_no_se_consume_y_no_aplica_al_atacar_al_marcador() (+9 more)

### Community 97 - "_clamp"
Cohesion: 0.12
Nodes (11): action_surge_uses(), _clamp(), fighter_extra_attacks_for(), indomitable_uses(), second_wind_uses(), weapon_mastery_count(), test_action_surge_usos_por_nivel_son_1_y_2(), test_indomitable_usos_por_nivel_son_1_2_y_3() (+3 more)

### Community 98 - "WorldTreeFeatures"
Cohesion: 0.16
Nodes (5): _aliados_heridos(), _cd_ataque(), _de(), _en_10_pies(), WorldTreeFeatures

### Community 99 - "test_zealot.py"
Cohesion: 0.11
Nodes (35): _abilities(), _aliado(), _barbaro(), _decision(), _fallos(), _forma(), _guarda_con(), _presencia() (+27 more)

### Community 100 - "random"
Cohesion: 0.07
Nodes (54): apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), SpikedArmorAction, AttackModifiers, _abilities(), _accion_puas() (+46 more)

### Community 101 - "AtaqueSustituido"
Cohesion: 0.10
Nodes (15): Arcane Archer (XGE), AtaqueSustituido, _RngSi, test_arcane_shot_se_aplica_una_sola_vez_por_turno(), test_arcane_shot_se_gasta_un_uso_al_aplicar(), test_daño_de_arcane_shot_es_2d6_antes_del_18(), _dado(), test_daño_de_arcane_shot_es_4d6_desde_el_18() (+7 more)

### Community 103 - "apply_psi_warrior"
Cohesion: 0.13
Nodes (13): apply_psi_warrior(), _abilities(), _firmas(), _pj(), test_apply_class_equivalente_a_apply_psi_warrior(), test_apply_psi_warrior_por_debajo_del_nivel_3_da_value_error(), test_apply_psi_warrior_sin_clase_guerrero_da_value_error(), test_guarded_mind_no_acumula_la_resistencia_si_ya_la_tenia() (+5 more)

### Community 104 - "Any"
Cohesion: 0.13
Nodes (8): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), _presupuesto(), registrar_resistencia_legendaria()

### Community 105 - "PsiWarriorFeatures"
Cohesion: 0.11
Nodes (10): psionic_die_sides(), PsiWarriorFeatures, test_el_tamano_del_dado_psionico_es_d6_d8_d10_o_d12_segun_el_nivel(), Fighter: cómo añadir una subclase, Grafo y verificación, Pendientes generales, Psi Warrior: plan de sesión, Rutina sugerida al abrir sesión (+2 more)

### Community 106 - "Attack"
Cohesion: 0.09
Nodes (44): D20Result, roll_d20(), RollMode, attack_roll(), _mode_tag(), Attack, test_commanders_strike_con_relentless_no_gasta_dado(), test_commanders_strike_sustituye_el_ataque_y_el_aliado_gasta_su_reaccion() (+36 more)

### Community 107 - "_especial"
Cohesion: 0.26
Nodes (11): _accion_marca(), _especial(), _pick_sin_decision(), test_el_ataque_especial_no_gasta_un_uso_ni_la_reaccion(), test_el_ataque_especial_no_suma_dano_extra_si_falla(), test_el_ataque_especial_se_arma_cuando_el_marcado_dana_a_un_tercero(), test_el_ataque_especial_solo_vale_en_el_siguiente_turno(), test_el_ataque_especial_suma_el_dano_extra_si_impacta() (+3 more)

### Community 108 - "condition_parser.py"
Cohesion: 0.13
Nodes (6): normalize_ability(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with()

### Community 109 - ".alive"
Cohesion: 0.10
Nodes (5): Combatant, _avisar_ataque_especial_marca(), _mark_dead_if_down(), _notify_damage_taken(), cobertura_bulwark_activa()

### Community 110 - "roll_initiative"
Cohesion: 0.21
Nodes (8): d20(), roll_initiative(), _d20_fijo(), test_ambush_con_la_decision_no_no_gasta_nada(), test_ambush_con_relentless_no_gasta_dado(), test_ambush_sin_dados_no_consume_rng(), test_ambush_sin_la_maniobra_no_consume_rng(), test_ambush_suma_un_dado_a_la_tirada_de_iniciativa()

### Community 111 - "_arquero"
Cohesion: 0.14
Nodes (15): _arquero(), _RngExplota, test_arcane_shot_crea_usos_por_nivel(), test_arcane_shot_se_reinicia_en_on_turn_start(), test_arcane_shot_sin_rng_no_actua(), test_arcane_shot_sin_usos_cero_rng(), test_ataque_cuerpo_a_cuerpo_cero_rng(), test_cd_de_arcane_shot_es_8_mas_pb_mas_int() (+7 more)

### Community 112 - "capas.py"
Cohesion: 0.20
Nodes (5): capa_de(), main(), visit_ImportFrom(), modulo_de(), resolver()

### Community 113 - "_RngExplota"
Cohesion: 0.25
Nodes (4): _RngExplota, test_interception_sin_arma_ni_escudo_no_actúa_y_no_consume_rng(), test_resolver_maestria_sin_maestria_no_consulta_tactical_master(), test_tactical_master_no_sustituye_bajo_el_nivel_9()

### Community 114 - "attach.py"
Cohesion: 0.13
Nodes (7): parse_attach_effects(), Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por()

### Community 117 - "simulate"
Cohesion: 0.15
Nodes (7): simulate(), test_immune_target_takes_zero_damage(), test_regression_guerrero_vs_ogro(), test_regression_guerrero_vs_owlbear(), test_con_use_probability_uno_el_danio_es_mayor_que_con_cero(), test_el_dragon_contra_un_grupo_usa_acciones_legendarias(), test_reproducibilidad_con_leyendas_y_resistencia()

### Community 119 - "ataque_utilitario"
Cohesion: 0.20
Nodes (8): _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), hay_utilitaria_accion(), _orden_tamano(), test_p_medio_usa_utilitaria_a_la_frecuencia_configurada(), test_p_uno_siempre_decide_sin_consumir_rng()

### Community 121 - "build_spell_actions"
Cohesion: 0.29
Nodes (8): build_spell_actions(), _desde_fixture(), _monstruo_lanzador(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_la_reaccion_gasta_su_uso_propio(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_uso_propio(), test_un_hechizo_a_voluntad_se_puede_lanzar_en_cada_turno()

### Community 122 - "spell_action"
Cohesion: 0.09
Nodes (15): Paquetes con fachada, _uso_de_entrada(), SaveAction, SpellAction, SpellAttackAction, SpellFixedDamageAction, dado_por_nivel(), duracion_en_rondas() (+7 more)

### Community 123 - "SaveResult"
Cohesion: 0.23
Nodes (12): SaveResult, fake_saving_throw(), _fake(), falla(), espia(), stub(), stub(), stub() (+4 more)

### Community 124 - "parse_escape"
Cohesion: 0.22
Nodes (5): has_escape_text(), parse_escape(), _skills_for(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 125 - "_FixedRandom"
Cohesion: 0.22
Nodes (4): _breath(), _FixedRandom, test_begin_turn_no_tira_nada_si_estan_cargadas(), test_begin_turn_reinicia_recursos_y_tira_una_recarga_por_accion()

### Community 127 - "_estado"
Cohesion: 0.50
Nodes (3): _estado(), test_el_estado_legendario_rellena_gasta_y_reinicia(), test_use_probability_medio_se_usa_about_50_por_ciento()

## Knowledge Gaps
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `test_fighter.py`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio`, `test_la_resistencia_funciona_en_todas_las_rutas`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_wild_heart.py`, `test_traits.py`, `_arco`, `test_utility.py`, `test_wild_magic.py`, `loader.py`, `_fighter`, `test_battle_master.py`, `_ejecuta`, `apply_class`, `test_world_tree.py`, `apply_barbarian`, `Abilities`, `test_death.py`, `Monster`, `TurnResources`, `test_parry.py`, `_ExplotaSiUsaRng`, `test_undead_fortitude.py`, `test_arcane_archer.py`, `dnd_sim/__init__.py`, `inflict_damage`, `test_mastery.py`, `test_conditions.py`, `roll_dice`, `Condition`, `_atacado`, `main.py`, `test_checks_escapes.py`, `load_monster`, `combat/attack.py`, `test_champion.py`, `test_magic_resistance.py`, `begin_turn`, `legendary_parser.py`, `test_storm_herald.py`, `roll_modifiers.py`, `_pj`, `apply_fighter`, `apply_cavalier`, `test_psi_warrior.py`, `test_pack_tactics.py`, `test_enlarge.py`, `combat/__init__.py`, `test_spells.py`, `test_azer.py`, `test_extra_damage.py`, `test_sustituir_ataque.py`, `_carga`, `test_ancestral_guardian.py`, `test_cavalier.py`, `lair_loader.py`, `_abilities`, `test_zealot.py`, `random`, `AtaqueSustituido`, `apply_psi_warrior`, `.alive`, `_arquero`, `_RngExplota`, `simulate`, `test_sustitucion_hace_un_solo_par_de_picks`, `spell_action`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `daño_base_arma()`) actually correct?**
  _`Attack` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_fighter.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12307692307692308 - nodes in this community are weakly interconnected._
- **Why does `Monster` connect `Monster` to `test_fighter.py`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_resistance_probability_medio_convierte_about_50_por_ciento`, `test_legendary.py`, `test_beast.py`, `test_proficiency.py`, `test_traits.py`, `_arco`, `test_utility.py`, `test_wild_magic.py`, `loader.py`, `test_battle_master.py`, `_ejecuta`, `Abilities`, `test_death.py`, `TurnResources`, `test_parry.py`, `_ExplotaSiUsaRng`, `test_undead_fortitude.py`, `test_arcane_archer.py`, `dnd_sim/__init__.py`, `inflict_damage`, `test_mastery.py`, `test_conditions.py`, `test_area.py`, `TelekineticMasterAction`, `Condition`, `_atacado`, `test_checks_escapes.py`, `load_monster`, `apply_condition`, `test_champion.py`, `test_magic_resistance.py`, `test_storm_herald.py`, `roll_modifiers.py`, `_pj`, `apply_cavalier`, `test_lair.py`, `test_psi_warrior.py`, `test_pack_tactics.py`, `_parchea_campo`, `test_enlarge.py`, `PsiBulwarkAction`, `Arquitectura de `dnd_sim``, `combat/__init__.py`, `test_spells.py`, `test_azer.py`, `test_sustituir_ataque.py`, `_carga`, `test_ancestral_guardian.py`, `test_cavalier.py`, `_abilities`, `test_zealot.py`, `random`, `AtaqueSustituido`, `apply_psi_warrior`, `Attack`, `_especial`, `.alive`, `_arquero`, `test_piercing_k_uniforme_y_atacante_nunca_es_objetivo`, `simulate`, `test_sustitucion_hace_un_solo_par_de_picks`, `build_spell_actions`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Monster` (e.g. with `Carpetas` and `_cloaker()`) actually correct?**
  _`Monster` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `AttackRange` be split into smaller, more focused modules?**
  _Cohesion score 0.07527853056308341 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_legendary.py`, `test_beast.py`, `spell_parser.py`, `test_traits.py`, `test_utility.py`, `loader.py`, `test_battle_master.py`, `_ejecuta`, `ArcaneArcherFeatures`, `Abilities`, `Monster`, `test_parry.py`, `saves.py`, `test_skills.py`, `test_arcane_archer.py`, `dnd_sim/__init__.py`, `test_mastery.py`, `BarbarianFeatures`, `test_conditions.py`, `roll_dice`, `TelekineticMasterAction`, `BattleMasterFeatures`, `test_checks_escapes.py`, `apply_condition`, `combat/attack.py`, `test_champion.py`, `test_magic_resistance.py`, `Trait`, `test_storm_herald.py`, `roll_modifiers.py`, `apply_cavalier`, `test_lair.py`, `test_psi_warrior.py`, `test_pack_tactics.py`, `_parchea_campo`, `ConditionInstance`, `test_enlarge.py`, `PsiBulwarkAction`, `CombatContext`, `combat/__init__.py`, `test_spells.py`, `GiantFeatures`, `_carga`, `psionic_dice_count`, `test_cavalier.py`, `_abilities`, `WorldTreeFeatures`, `PsiWarriorFeatures`, `Attack`, `condition_parser.py`, `.alive`, `attach.py`, `ataque_utilitario`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
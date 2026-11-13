# Graph Report - DnDBalancer  (2026-11-12)

## Corpus Check
- 229 files · ~220,586 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 4087 nodes · 14882 edges · 123 communities (107 shown, 16 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 1004 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `814fa5b2`
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
- _arquero
- test_utility.py
- test_wild_magic.py
- loader.py
- survival.py
- _trait
- test_battle_master.py
- _atacado
- test_loader_actions.py
- barbarian/__init__.py
- saving_throw
- ActionUsage
- TurnResources
- test_superior_invisibility.py
- ZealotFeatures
- test_zealot.py
- test_death.py
- Monster
- test_magical.py
- test_parry.py
- ability_check
- pick
- _commanda
- test_skills.py
- test_undead_fortitude.py
- test_arcane_archer.py
- test_multiattack.py
- encounter.py
- inflict_damage
- test_mastery.py
- BarbarianFeatures
- apply_condition
- dnd_sim/__init__.py
- test_area.py
- random
- Condition
- BattleMasterFeatures
- _ExplotaSiUsaRng
- main.py
- test_checks_escapes.py
- load_monster
- _con_estilo
- log_line
- test_condition_immunities.py
- combat/attack.py
- test_champion.py
- test_magic_resistance.py
- begin_turn
- CavalierMarkAttackAction
- Trait
- legendary_parser.py
- test_storm_herald.py
- roll_modifiers.py
- test_backgrounds.py
- _pj
- apply_fighter
- apply_cavalier
- test_lair.py
- normalize_skill
- test_pack_tactics.py
- _pj
- ConditionTracker
- json
- PlayerCharacter
- test_enlarge.py
- Spellcasting
- conditions.py
- run_combat
- _pj
- CombatContext
- apply_damage_modifiers
- test_spells.py
- _RngMax
- test_azer.py
- AncestralGuardianFeatures
- test_extra_damage.py
- test_sustituir_ataque.py
- _carga
- damage.py
- test_ancestral_guardian.py
- test_cavalier.py
- AreaSaveAction
- consumir_marcas
- _clamp
- warnings
- _decision
- BattleragerFeatures
- test_piercing_los_dados_extra_se_tiran_una_sola_vez
- test_el_gancho_after_failed_check_desde_ability_check_con_ctx
- BerserkerFeatures
- legendary.py
- TODO — DnDBalancer / dnd_sim
- Attack
- _especial
- condition_parser.py
- .alive
- roll_initiative
- IntimidatingPresenceAction
- Abilities
- _RngExplota
- AttachOnHitEffect
- CombatState
- test_piercing_k_uniforme_y_atacante_nunca_es_objetivo
- test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque
- test_tactical_master_nivel_9_elige_entre_original_push_sap_slow
- test_sustitucion_hace_un_solo_par_de_picks
- _golpe_sin_armas
- test_el_proyectil_magico_pasa_por_los_modificadores_de_dano

## God Nodes (most connected - your core abstractions)
1. `Attack` - 262 edges
2. `Monster` - 205 edges
3. `Condition` - 191 edges
4. `AttackRange` - 188 edges
5. `attack_roll()` - 187 edges
6. `apply_condition()` - 160 edges
7. `Abilities` - 155 edges
8. `PlayerCharacter` - 138 edges
9. `load_monster()` - 136 edges
10. `pick()` - 117 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Fighter: cómo añadir una subclase` --references--> `SubclassDef`  [INFERRED]
  TODO.md → dnd_sim/rules/classes/base.py
- `Champion: plan de sesión` --references--> `_clamp()`  [INFERRED]
  TODO.md → dnd_sim/core/classes.py
- `Arcane Archer (XGE)` --references--> `roll_dice()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/dice.py

## Import Cycles
- None detected.

## Communities (123 total, 16 thin omitted)

### Community 0 - "test_fighter.py"
Cohesion: 0.13
Nodes (16): second_wind_uses(), _action_surge(), _ctx_recursos(), _RngBajo, _second_wind(), test_action_surge_como_maximo_un_vez_por_turno(), test_action_surge_ejecutada_restaura_la_accion_y_gasta_un_uso(), test_action_surge_no_es_elegible_si_la_accion_no_se_ha_gastado() (+8 more)

### Community 1 - "test_attach.py"
Cohesion: 0.17
Nodes (26): enganchador_de(), _atacar(), _bite(), _cloaker(), _ctx(), _datos(), _pj(), test_con_ventaja_el_enganche_es_a_la_cabeza_y_ciega() (+18 more)

### Community 2 - "AttackRange"
Cohesion: 0.16
Nodes (37): AttackRange, _abilities(), _barbaro(), _berserker(), _ctx(), _furia_lista(), _monstruo(), _pj() (+29 more)

### Community 3 - "test_giant.py"
Cohesion: 0.09
Nodes (36): apply_giant(), _de(), MightyImpelAction, _objetivos_impel(), _orden_de(), _abilities(), _barbaro(), _ctx() (+28 more)

### Community 4 - "test_world_tree.py"
Cohesion: 0.12
Nodes (38): _abilities(), _aliado(), _barbaro(), _ctx(), _decision(), _elige_candidato(), espia(), _furia() (+30 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.08
Nodes (48): apply_wild_heart(), _con_beneficio(), _de(), _en_5_pies(), _hostil(), _orden_de(), _abilities(), _aliado() (+40 more)

### Community 6 - "test_proficiency.py"
Cohesion: 0.16
Nodes (20): ability_check_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia() (+12 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.06
Nodes (64): simulate(), legendary_phase(), LegendaryAction, test_immune_target_takes_zero_damage(), test_regression_guerrero_vs_ogro(), test_regression_guerrero_vs_owlbear(), _contexto(), _data() (+56 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (66): WeaponAttackAction, _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll(), spy() (+58 more)

### Community 9 - "spell_parser.py"
Cohesion: 0.08
Nodes (16): Paquetes con fachada, _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla() (+8 more)

### Community 10 - "test_traits.py"
Cohesion: 0.10
Nodes (26): attack_modifiers(), BloodFrenzy, _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDeSalvacion, _sahuagin() (+18 more)

### Community 11 - "_arquero"
Cohesion: 0.09
Nodes (31): _arco(), _arquero(), _ctx_curving(), _curving(), _RngExplota, _RngNo, test_arcane_shot_crea_usos_por_nivel(), test_arcane_shot_se_aplica_una_sola_vez_por_turno() (+23 more)

### Community 12 - "test_utility.py"
Cohesion: 0.12
Nodes (30): ConditionInstance, _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), hay_utilitaria_accion(), _orden_tamano(), _abilities() (+22 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.09
Nodes (49): _log_target(), _avisar_fallo_salvacion(), _mode_tag(), _outcome_tag(), _log_line_outcome(), SaveResult, hooks(), fake_saving_throw() (+41 more)

### Community 14 - "loader.py"
Cohesion: 0.06
Nodes (13): doblar_dados(), parse_attach_effects(), _extract_multiattack_alternatives(), _norm_name(), _parse_condition_immunities(), _parse_damage_modifiers(), extract_multiattack_alternatives(), _norm_name() (+5 more)

### Community 15 - "survival.py"
Cohesion: 0.11
Nodes (5): _es_radiante(), _guardar_salvacion(), Regeneration, Relentless, UndeadFortitude

### Community 16 - "_trait"
Cohesion: 0.16
Nodes (31): _check_fallada(), _ctx(), _fighter(), _objetivo(), _save_fallada(), _saving_nueva(), test_action_surge_no_existe_en_nivel_1(), test_ataques_estudiados_caduca_al_final_del_siguiente_turno() (+23 more)

### Community 17 - "test_battle_master.py"
Cohesion: 0.06
Nodes (40): maneuvers_known_count(), superiority_dice_count(), superiority_die_sides(), apply_battle_master(), BattleMasterRallyAction, FeintingAttackAction, _atacado_fijo(), _bm() (+32 more)

### Community 18 - "_atacado"
Cohesion: 0.08
Nodes (39): _abilities(), _atacado(), _atacado_dos_enemigos(), _completa(), _ejecuta(), _mods(), _parry(), _RngFalla (+31 more)

### Community 19 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (14): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+6 more)

### Community 20 - "barbarian/__init__.py"
Cohesion: 0.04
Nodes (19): apply_beast(), BeastFeatures, CallTheHuntBonus, FormOfTheBeast, NaturalWeapon, GiantFeatures, apply_storm_herald(), StormAuraAction (+11 more)

### Community 21 - "saving_throw"
Cohesion: 0.05
Nodes (17): roll_dice(), _apply_condition_riders(), ArcaneArcherFeatures, _ctx_con_rng(), _CtxConRng, RepeatSave, legendary_resistance(), apply_save_damage() (+9 more)

### Community 22 - "ActionUsage"
Cohesion: 0.15
Nodes (9): ActionUsage, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar(), test_per_day_dos_usos_y_luego_can_use_falso(), test_per_day_reset_restaura_todos_los_usos(), test_recharge_5_6_porcentaje_de_exito(), test_recharge_mientras_esta_cargada_no_consume_rng(), test_recharge_recarga_con_5_o_mas_y_falla_con_4() (+1 more)

### Community 23 - "TurnResources"
Cohesion: 0.06
Nodes (84): rage_uses(), TurnResources, apply_barbarian(), AttackModifiers, CheckModifiers, SaveModifiers, _abilities(), _ctx() (+76 more)

### Community 24 - "test_superior_invisibility.py"
Cohesion: 0.10
Nodes (33): _entradas(), parse_traits(), remove_invisibility_on_action(), _aliado(), _ctx(), _datos(), _espada(), _hobgoblin() (+25 more)

### Community 25 - "ZealotFeatures"
Cohesion: 0.08
Nodes (9): apply_zealot(), _de(), _en_60_pies(), _es_aliado(), _furia_de(), _reserva_dados(), ZealotFeatures, ZealousPresenceAction (+1 more)

### Community 26 - "test_zealot.py"
Cohesion: 0.11
Nodes (34): WarriorHealAction, _abilities(), _accion(), _aliado(), _ctx(), _presencia(), test_after_failed_save_sin_zealot_devuelve_el_mismo_resultado(), test_apply_class_por_clave_aplica_zealot() (+26 more)

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 28 - "Monster"
Cohesion: 0.13
Nodes (29): Monster, _abilities(), _disparo(), _RngFalla, _RngSi, test_banishing_arrow_falla_la_salvacion_y_deja_incapacitado(), test_banishing_arrow_salvacion_exitosa_no_aplica_condicion(), test_beguiling_arrow_hechiza_y_termina_si_el_aliado_ataca() (+21 more)

### Community 29 - "test_magical.py"
Cohesion: 0.10
Nodes (22): _tag_modificadores(), _ctx(), _pj(), _spell_data(), _spellcasting(), test_ataque_con_magical_true_dana_completo_al_ghost(), test_ataque_magico_contra_un_bárbaro_en_furia_se_reduce_a_la_mitad(), test_bestial_solo_marca_las_armas_magicas_desde_el_nivel_6() (+14 more)

### Community 30 - "test_parry.py"
Cohesion: 0.27
Nodes (20): _arquero_parry(), _ataque(), _ctx(), _datos(), _fijar_d20(), espia(), _gladiador(), _pj() (+12 more)

### Community 31 - "ability_check"
Cohesion: 0.16
Nodes (10): ability_check(), _avisar_fallo_prueba(), CheckResult, _finish_check(), _guia(), _resolve_mods(), skill_check(), check_modifiers() (+2 more)

### Community 32 - "pick"
Cohesion: 0.04
Nodes (21): champion_crit_threshold(), heroic_rally_amount(), proficiency_bonus(), pick(), sample(), ActionSurgeAction, _contexto(), _en_5_pies() (+13 more)

### Community 33 - "_commanda"
Cohesion: 0.13
Nodes (20): _accion_rally(), _commanda(), _RngNo, _sustituye(), test_commanders_strike_cede_el_ataque_si_hay_feinting_encolado(), test_commanders_strike_no_se_decide_si_el_aliado_no_tiene_armas(), test_commanders_strike_no_se_decide_si_el_aliado_ya_uso_su_reaccion(), test_commanders_strike_no_se_decide_sin_aliados_elegibles() (+12 more)

### Community 34 - "test_skills.py"
Cohesion: 0.11
Nodes (23): skill_ability(), skill_bonus(), _abilities(), _ctx(), _load_fixture(), _pj(), _SoloMod, test_ability_check_no_suma_competencia_de_habilidad() (+15 more)

### Community 35 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 36 - "test_arcane_archer.py"
Cohesion: 0.11
Nodes (23): arcane_shot_options_known(), arcane_shot_uses(), apply_arcane_archer(), CurvingShotAction, _firmas(), _pj(), test_accion_curving_se_anade_desde_el_nivel_7(), test_apply_arcane_archer_exige_la_clase_fighter() (+15 more)

### Community 37 - "test_multiattack.py"
Cohesion: 0.12
Nodes (14): _en_accion_de_ataque(), MultiattackAction, _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso() (+6 more)

### Community 38 - "encounter.py"
Cohesion: 0.11
Nodes (12): combat_finished(), living_teams(), CombatResult, _invoke_policy(), _run_combat(), _nuevo_ctx(), _pasada(), _summarize_damage() (+4 more)

### Community 39 - "inflict_damage"
Cohesion: 0.26
Nodes (13): inflict_damage(), _ctx(), _datos(), _jabali(), _pj(), test_el_jabali_carga_su_relentless_con_umbral_y_uso(), test_relentless_no_necesita_contexto_ni_rng(), test_reset_reestablece_el_umbral_y_los_usos() (+5 more)

### Community 40 - "test_mastery.py"
Cohesion: 0.10
Nodes (28): al_acertar(), al_fallar(), _cd_topple(), _log(), _nombre(), resolver_maestria(), _arma(), _atacante() (+20 more)

### Community 41 - "BarbarianFeatures"
Cohesion: 0.10
Nodes (5): BarbarianFeatures, _contexto(), _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 42 - "apply_condition"
Cohesion: 0.12
Nodes (38): apply_condition(), end_turn(), resolve_attack_range(), _ataque(), _ctx(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja() (+30 more)

### Community 43 - "dnd_sim/__init__.py"
Cohesion: 0.06
Nodes (16): ability_mod(), extra_attacks_for(), rage_damage(), DamageType, parse_damage_type(), ActionType, AttackAction, AttackEntry (+8 more)

### Community 44 - "test_area.py"
Cohesion: 0.22
Nodes (22): AreaTargeting, select_area_targets(), _default_targeting(), SaveDamage, _area_action(), _ctx(), _npc(), _pj() (+14 more)

### Community 45 - "random"
Cohesion: 0.26
Nodes (18): _abilities(), _ctx(), _decide(), _pj(), test_antes_del_nivel_2_no_hay_decision_ni_rng(), test_en_turno_ajeno_no_decide(), test_frecuencia_0_5_es_aproximadamente_la_mitad_de_los_turnos(), test_las_reacciones_no_deciden_ni_reciben() (+10 more)

### Community 46 - "Condition"
Cohesion: 0.19
Nodes (26): Condition, test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+18 more)

### Community 47 - "BattleMasterFeatures"
Cohesion: 0.09
Nodes (6): Battle Master (PHB 2024), _aliados_elegibles(), _armas_melee_propias(), _armas_propias(), BattleMasterFeatures, _orden_tamano()

### Community 48 - "_ExplotaSiUsaRng"
Cohesion: 0.12
Nodes (23): _accion_feinting(), _conoce_sweeping(), _decide(), _ExplotaSiUsaRng, _RngIdx, test_el_ataque_de_reaccion_no_activa_maniobras_de_sesion_1(), test_el_uso_no_se_gasta_si_no_se_ejecuta(), test_en_un_fallo_sin_precision_cero_rng() (+15 more)

### Community 49 - "main.py"
Cohesion: 0.11
Nodes (22): CLI del simulador: `build_parser()`, Detalle por flag, Ejemplos, Flujo de `main()`, `--legendary-p`, `--legendary-points`, `--monster` / `-m`, Observaciones (para humanos y IA) (+14 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.08
Nodes (47): EscapeCheck, effective_ac(), _ataque(), _check_fijo(), _fake(), _ctx(), _data(), _duelo() (+39 more)

### Community 51 - "load_monster"
Cohesion: 0.13
Nodes (15): _armor_class_value(), load_monster(), test_una_condicion_desconocida_de_la_api_avisa(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper() (+7 more)

### Community 52 - "_con_estilo"
Cohesion: 0.23
Nodes (16): _aliado(), _con_estilo(), _enemigo(), _mods(), _RngSi, test_interception_con_un_aliado_no_baja_de_cero_el_daño(), test_interception_no_actúa_con_la_reacción_gastada(), test_interception_no_actúa_contra_un_no_aliado_ni_con_el_mismo_pj() (+8 more)

### Community 53 - "log_line"
Cohesion: 0.06
Nodes (19): log_line(), _objetivo_enganche(), valid_targets(), apply_wild_magic(), _bolstering(), _cd(), _de(), _en_30_pies() (+11 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.13
Nodes (15): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+7 more)

### Community 57 - "combat/attack.py"
Cohesion: 0.06
Nodes (25): Cavalier (XGE), _actualizar_distancia(), _agrandado(), _bando_del(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque() (+17 more)

### Community 59 - "test_champion.py"
Cohesion: 0.05
Nodes (66): apply_class(), _abilities(), _champion(), _fighter(), _firmas(), _parchea_d20(), _pj(), _rally() (+58 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.12
Nodes (24): _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab(), test_condition_action_de_hechizo_pasa_magical() (+16 more)

### Community 61 - "begin_turn"
Cohesion: 0.30
Nodes (14): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+6 more)

### Community 62 - "CavalierMarkAttackAction"
Cohesion: 0.18
Nodes (5): cavalier_mark_extra_damage(), _armas_melee_de(), CavalierMarkAttackAction, _de(), test_daño_extra_del_ataque_especial_es_el_nivel_entre_dos()

### Community 63 - "Trait"
Cohesion: 0.03
Nodes (12): Trait, DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante(), aliados_capaces() (+4 more)

### Community 64 - "legendary_parser.py"
Cohesion: 0.08
Nodes (18): parse_range_type(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary() (+10 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.06
Nodes (47): _aliados_en_aura(), _cd(), _dado_mar(), _de(), _en_aura(), _enemigos_en_aura(), _escalado(), StormHeraldFeatures (+39 more)

### Community 66 - "roll_modifiers.py"
Cohesion: 0.11
Nodes (15): _condiciones(), evaluar_d20(), _hooks(), _instancias(), save_modifiers(), umbral_critico(), test_sin_subclase_el_umbral_de_critico_es_20_sin_rng(), _datos() (+7 more)

### Community 67 - "test_backgrounds.py"
Cohesion: 0.10
Nodes (20): Background, normalize_tool(), get_background(), _add(), load_background(), parse_background(), _abilities(), _pj() (+12 more)

### Community 68 - "_pj"
Cohesion: 0.22
Nodes (19): espia(), _espiar_divine(), _furia(), _mon(), _pj(), test_determinismo_misma_semilla_mismos_resultados(), corrida(), test_divine_fury_elige_radiante_con_pick() (+11 more)

### Community 69 - "apply_fighter"
Cohesion: 0.08
Nodes (35): apply_fighter(), maestria_de(), _abilities(), _firmas(), _pj(), _pj_con_armas(), test_apply_class_fighter_sin_subclase_equivalente_a_apply_fighter(), test_apply_class_reenvía_el_estilo_de_combate() (+27 more)

### Community 70 - "apply_cavalier"
Cohesion: 0.10
Nodes (20): cavalier_mark_uses(), warding_maneuver_uses(), apply_cavalier(), _cavalier(), _firmas(), _pj(), test_apply_cavalier_exige_la_clase_fighter(), test_apply_cavalier_requiere_nivel_3() (+12 more)

### Community 71 - "test_lair.py"
Cohesion: 0.10
Nodes (19): lair_phase(), LairAction, LegendaryState, _ctx(), _enemigo(), lairs_dir(), _Stub, test_dos_acciones_uniformes() (+11 more)

### Community 72 - "normalize_skill"
Cohesion: 0.11
Nodes (7): _clean(), normalize_skill(), _skill_name(), _spells_from_description(), _trait_skills(), test_normalize_skill_acepta_espacios_y_spanish(), test_normalize_skill_desconocida_lanza_value_error()

### Community 73 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 74 - "_pj"
Cohesion: 0.18
Nodes (14): _dragon(), _orden_con(), _pj(), _spy_turnos(), spy(), test_guarida_pasa_magical_a_las_salvaciones(), test_puntos_siempre_incluyen_bonus_de_guarida(), test_reproducibilidad_con_guarida() (+6 more)

### Community 76 - "json"
Cohesion: 0.15
Nodes (8): _cache_path(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError, NetworkError

### Community 77 - "PlayerCharacter"
Cohesion: 0.12
Nodes (24): Race, load_race(), parse_race(), PlayerCharacter, _abilities(), _fiendish_legacy(), _keen_senses(), _pj() (+16 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.16
Nodes (23): _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj(), _spell_data() (+15 more)

### Community 79 - "Spellcasting"
Cohesion: 0.18
Nodes (6): parse_spellcasting(), Spellcasting, test_el_lanzador_se_lee_de_los_actions(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_la_curacion_usa_el_modificador_de_caracteristica_no_el_bono_completo(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 80 - "conditions.py"
Cohesion: 0.21
Nodes (7): _as_condition(), attempt_escapes(), _condicion_bloqueada(), _contar(), _label(), _queda_accion(), remove_condition()

### Community 81 - "run_combat"
Cohesion: 0.13
Nodes (15): run_combat(), _breath(), _eventos(), _FixedRandom, _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(), test_begin_turn_no_tira_nada_si_estan_cargadas() (+7 more)

### Community 82 - "_pj"
Cohesion: 0.13
Nodes (17): _data(), _load(), _pj(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente(), test_el_ghoul_paraliza_con_diez_rondas_y_salvacion_de_repeticion(), test_el_hechizado_ahora_si_se_aplica(), test_el_lobo_derriba_con_la_salvacion_del_json(), test_el_lobo_no_derriba_si_el_ataque_falla() (+9 more)

### Community 83 - "CombatContext"
Cohesion: 0.06
Nodes (18): actor_is_alive(), CombatContext, _living_enemies(), _log(), HealAction, _romper_invisibilidad_al_lanzar(), SpellAction, SpellAttackAction (+10 more)

### Community 84 - "apply_damage_modifiers"
Cohesion: 0.15
Nodes (17): apply_damage_modifiers(), _is_petrified(), _guerrero_y_ogro(), _target(), test_attack_roll_log_modifier(), test_danio_medio_por_combatiente_y_equipo(), test_etiqueta_de_modificadores_se_deriva_del_dano_final(), test_immunity_zero() (+9 more)

### Community 85 - "test_spells.py"
Cohesion: 0.09
Nodes (51): build_spell_actions(), parse_spell(), spell_action(), _ctx(), _desde_fixture(), _monstruo_lanzador(), _npc(), _pj() (+43 more)

### Community 87 - "test_azer.py"
Cohesion: 0.08
Nodes (28): Cómo comprobar que todo sigue en orden, _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api(), _ataque_melee(), _ataque_ranged() (+20 more)

### Community 89 - "test_extra_damage.py"
Cohesion: 0.17
Nodes (18): DamageRecorder, _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional() (+10 more)

### Community 90 - "test_sustituir_ataque.py"
Cohesion: 0.18
Nodes (10): AtaqueSustituido, _abilities(), _blanco(), _pj(), _RasgoQueSustituye, _RasgoSinSustitucion, _RngExplota, test_rasgo_que_devuelve_none_conserva_el_flujo_y_las_semillas() (+2 more)

### Community 91 - "_carga"
Cohesion: 0.18
Nodes (13): _ataque_carga(), _carga(), _salvacion(), test_ferocious_charger_cd_es_ocho_mas_pb_mas_fuerza(), test_ferocious_charger_con_p_medio_tira_un_random(), test_ferocious_charger_el_flag_se_reinicia_cada_turno(), test_ferocious_charger_nivel_14_no_actua_sin_rng(), test_ferocious_charger_p_cero_no_carga_sin_rng() (+5 more)

### Community 92 - "damage.py"
Cohesion: 0.11
Nodes (8): _absorber_pv_temporales(), _avisar_ataque_especial_marca(), _hooks(), _mark_dead_if_down(), _mitigacion_de_otros(), _notify_damage_dealt(), _notify_damage_taken(), _salvar_a_cero()

### Community 93 - "test_ancestral_guardian.py"
Cohesion: 0.18
Nodes (26): _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado(), _escudo(), _esperado() (+18 more)

### Community 94 - "test_cavalier.py"
Cohesion: 0.13
Nodes (25): _bajo_ataque(), _cargar_main(), _defiende(), _RngExplota, test_el_flag_charge_p_llega_al_rasgo(), test_flag_charge_p_en_el_cli(), test_hold_the_line_con_decision_negativa_no_gasta_nada(), test_hold_the_line_exige_nivel_10() (+17 more)

### Community 95 - "AreaSaveAction"
Cohesion: 0.09
Nodes (11): _check_fields(), _construir(), _error(), load_lair(), build_save_action(), SaveAction, AreaSaveAction, ConditionAction (+3 more)

### Community 96 - "consumir_marcas"
Cohesion: 0.19
Nodes (18): consumir_marcas(), _abilities(), _marca_con(), _marcado(), _mods(), _RngSi, test_incapacitado_el_marcador_anula_la_marca(), test_la_marca_caduca_en_la_ronda_indicada() (+10 more)

### Community 97 - "_clamp"
Cohesion: 0.15
Nodes (9): action_surge_uses(), _clamp(), fighter_extra_attacks_for(), indomitable_uses(), weapon_mastery_count(), test_action_surge_usos_por_nivel_son_1_y_2(), test_indomitable_usos_por_nivel_son_1_2_y_3(), test_los_golpes_del_guerrero_suben_en_5_11_y_20() (+1 more)

### Community 98 - "warnings"
Cohesion: 0.15
Nodes (8): _resistencia_legendaria(), _declara_uso(), _usage(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 99 - "_decision"
Cohesion: 0.12
Nodes (24): _barbaro(), _decision(), _fallos(), _forma(), _guarda_con(), stub(), test_fanatical_decision_negativa_no_repiten(), test_fanatical_el_resultado_nuevo_sustituye_al_original() (+16 more)

### Community 100 - "BattleragerFeatures"
Cohesion: 0.13
Nodes (5): apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), SpikedArmorAction

### Community 101 - "test_piercing_los_dados_extra_se_tiran_una_sola_vez"
Cohesion: 0.25
Nodes (5): test_daño_de_arcane_shot_es_2d6_antes_del_18(), _dado(), test_daño_de_arcane_shot_es_4d6_desde_el_18(), test_piercing_los_dados_extra_se_tiran_una_sola_vez(), test_seeking_2d6_de_extra_desde_el_18()

### Community 103 - "BerserkerFeatures"
Cohesion: 0.15
Nodes (4): _armas_melee_de(), BerserkerFeatures, _de(), _furia_de()

### Community 104 - "legendary.py"
Cohesion: 0.16
Nodes (8): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), _presupuesto(), registrar_resistencia_legendaria()

### Community 105 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.20
Nodes (8): test_ever_ready_shot_no_cambia_los_usos_al_empezar_un_combate(), Fighter: cómo añadir una subclase, Fighter: pendientes reales, Grafo y verificación, Pendientes generales, Rutina sugerida al abrir sesión, TODO — DnDBalancer / dnd_sim, TODOs en código (marcados `# TODO`)

### Community 106 - "Attack"
Cohesion: 0.11
Nodes (38): D20Result, RollMode, attack_roll(), _mode_tag(), Attack, test_commanders_strike_con_relentless_no_gasta_dado(), test_commanders_strike_el_dueño_nunca_es_el_aliado_elegido(), test_commanders_strike_sustituye_el_ataque_y_el_aliado_gasta_su_reaccion() (+30 more)

### Community 107 - "_especial"
Cohesion: 0.26
Nodes (11): _accion_marca(), _especial(), _pick_sin_decision(), test_el_ataque_especial_no_gasta_un_uso_ni_la_reaccion(), test_el_ataque_especial_no_suma_dano_extra_si_falla(), test_el_ataque_especial_se_arma_cuando_el_marcado_dana_a_un_tercero(), test_el_ataque_especial_solo_vale_en_el_siguiente_turno(), test_el_ataque_especial_suma_el_dano_extra_si_impacta() (+3 more)

### Community 108 - "condition_parser.py"
Cohesion: 0.09
Nodes (11): normalize_ability(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), has_escape_text(), parse_escape() (+3 more)

### Community 109 - ".alive"
Cohesion: 0.13
Nodes (3): Excepción única admitida, Reglas de dependencia, Combatant

### Community 110 - "roll_initiative"
Cohesion: 0.12
Nodes (16): Arcane Archer (XGE), Arquitectura de `dnd_sim`, Carpetas, Champion (PHB 2024), Guaridas: política fija, Imports diferidos, d20(), roll_d20() (+8 more)

### Community 111 - "IntimidatingPresenceAction"
Cohesion: 0.20
Nodes (13): apply_berserker(), IntimidatingPresenceAction, _presencia_ctx(), test_apply_anade_trait_y_accion(), test_presencia_afecta_a_un_numero_aleatorio_de_enemigos(), test_presencia_requiere_nivel_14(), test_presencia_sin_rng_no_paga(), test_presencia_sin_usos_no_esta_disponible() (+5 more)

### Community 112 - "Abilities"
Cohesion: 0.22
Nodes (5): Abilities, test_sin_autoexito_ni_autofallo_en_pruebas(), test_sin_condiciones_el_dano_no_cambia(), test_un_petrificado_resiste_y_el_log_lo_dice(), test_una_criatura_sin_regeneracion_muere_al_llegar_a_cero()

### Community 113 - "_RngExplota"
Cohesion: 0.25
Nodes (4): _RngExplota, test_interception_sin_arma_ni_escudo_no_actúa_y_no_consume_rng(), test_resolver_maestria_sin_maestria_no_consulta_tactical_master(), test_tactical_master_no_sustituye_bajo_el_nivel_9()

## Knowledge Gaps
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `test_fighter.py`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_traits.py`, `_arquero`, `test_utility.py`, `test_wild_magic.py`, `loader.py`, `_trait`, `test_battle_master.py`, `_atacado`, `barbarian/__init__.py`, `TurnResources`, `test_superior_invisibility.py`, `test_zealot.py`, `test_death.py`, `Monster`, `test_magical.py`, `test_parry.py`, `_commanda`, `test_undead_fortitude.py`, `test_arcane_archer.py`, `inflict_damage`, `test_mastery.py`, `apply_condition`, `dnd_sim/__init__.py`, `random`, `Condition`, `_ExplotaSiUsaRng`, `main.py`, `test_checks_escapes.py`, `load_monster`, `combat/attack.py`, `test_champion.py`, `test_magic_resistance.py`, `begin_turn`, `legendary_parser.py`, `test_storm_herald.py`, `roll_modifiers.py`, `_pj`, `apply_fighter`, `apply_cavalier`, `test_pack_tactics.py`, `test_enlarge.py`, `CombatContext`, `apply_damage_modifiers`, `test_spells.py`, `test_azer.py`, `test_extra_damage.py`, `test_sustituir_ataque.py`, `_carga`, `test_ancestral_guardian.py`, `test_cavalier.py`, `AreaSaveAction`, `consumir_marcas`, `BattleragerFeatures`, `.alive`, `Abilities`, `_RngExplota`, `test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque`, `test_sustitucion_hace_un_solo_par_de_picks`, `_golpe_sin_armas`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `daño_base_arma()`) actually correct?**
  _`Attack` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_fighter.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12923076923076923 - nodes in this community are weakly interconnected._
- **Why does `attack_roll()` connect `Attack` to `test_attach.py`, `test_giant.py`, `test_wild_heart.py`, `test_legendary.py`, `test_beast.py`, `test_traits.py`, `barbarian/__init__.py`, `saving_throw`, `test_superior_invisibility.py`, `test_zealot.py`, `test_death.py`, `test_magical.py`, `test_parry.py`, `pick`, `test_arcane_archer.py`, `test_multiattack.py`, `encounter.py`, `inflict_damage`, `test_mastery.py`, `apply_condition`, `dnd_sim/__init__.py`, `Condition`, `BattleMasterFeatures`, `test_checks_escapes.py`, `combat/attack.py`, `test_champion.py`, `test_magic_resistance.py`, `CavalierMarkAttackAction`, `roll_modifiers.py`, `_pj`, `apply_fighter`, `test_enlarge.py`, `_pj`, `CombatContext`, `apply_damage_modifiers`, `test_spells.py`, `test_azer.py`, `test_extra_damage.py`, `test_sustituir_ataque.py`, `test_ancestral_guardian.py`, `AreaSaveAction`, `.alive`, `roll_initiative`, `Abilities`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Monster` (e.g. with `Carpetas` and `_cloaker()`) actually correct?**
  _`Monster` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_giant.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08583959899749373 - nodes in this community are weakly interconnected._
- **Why does `Trait` connect `Trait` to `spell_parser.py`, `test_traits.py`, `survival.py`, `barbarian/__init__.py`, `saving_throw`, `test_superior_invisibility.py`, `ZealotFeatures`, `ability_check`, `pick`, `BarbarianFeatures`, `dnd_sim/__init__.py`, `BattleMasterFeatures`, `log_line`, `test_condition_immunities.py`, `test_storm_herald.py`, `AncestralGuardianFeatures`, `test_sustituir_ataque.py`, `warnings`, `BattleragerFeatures`, `BerserkerFeatures`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
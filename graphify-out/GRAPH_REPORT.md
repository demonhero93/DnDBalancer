# Graph Report - DnDBalancer  (2026-11-16)

## Corpus Check
- 235 files · ~233,964 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 4639 nodes · 16949 edges · 175 communities (131 shown, 44 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 1267 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cf3187c1`
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
- SamuraiFeatures
- _fighter
- apply_battle_master
- _samurai
- AttackAction
- apply_class
- inflict_damage
- ActionUsage
- apply_barbarian
- test_superior_invisibility.py
- ZealotFeatures
- BattleragerFeatures
- test_death.py
- Monster
- load_monster
- test_parry.py
- .alive
- FighterFeatures
- _ExplotaSiUsaRng
- test_skills.py
- traits/__init__.py
- test_arcane_archer.py
- test_multiattack.py
- casting.py
- test_relentless.py
- test_mastery.py
- BarbarianFeatures
- Abilities
- dnd_sim/__init__.py
- test_area.py
- TelekineticMasterAction
- test_invisibility.py
- BattleMasterFeatures
- test_battle_master.py
- main.py
- apply_condition
- PlayerCharacter
- _con_estilo
- legendary_phase
- test_condition_immunities.py
- attack_roll
- test_champion.py
- test_magic_resistance.py
- begin_turn
- WildHeartFeatures
- lair_loader.py
- test_storm_herald.py
- save_modifiers
- test_backgrounds.py
- Condition
- apply_fighter
- apply_cavalier
- test_lair.py
- _bajo_golpe
- test_pack_tactics.py
- psionic_dice_count
- ConditionTracker
- _ctx
- test_races.py
- test_enlarge.py
- _ctx
- test_psi_warrior.py
- run_combat
- test_arquitectura.py
- pick
- test_damage.py
- test_spells.py
- test_rune_knight.py
- test_azer.py
- json
- test_extra_damage.py
- test_sustituir_ataque.py
- _carga
- _psi
- test_ancestral_guardian.py
- test_cavalier.py
- StormHeraldFeatures
- consumir_marcas
- _nube_partida
- CombatContext
- test_zealot.py
- TurnResources
- AtaqueSustituido
- _pj
- apply_psi_warrior
- Any
- _pj
- Attack
- test_martial_advantage.py
- valid_targets
- test_undead_fortitude.py
- roll_initiative
- _arquero
- capas.py
- _RngExplota
- RuneInvokeAction
- .enfeeble_mitiga
- Any
- GiantsMightAction
- test_tactical_master_nivel_9_elige_entre_original_push_sap_slow
- RageAction
- ChampionFeatures
- build_spell_actions
- test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque
- SaveResult
- parse_escape
- WarriorHealAction
- _bajo_ataque
- _abilities
- random
- attack_modifiers
- barbarian/__init__.py
- Combatant
- _clamp
- multiattack_parser.py
- LegendaryState
- _avisar_ganchos_de_turno
- normalize_ability
- _run_combat
- TODO — DnDBalancer / dnd_sim
- MultiattackAction
- normalize_skill
- _skill_name
- combat/__init__.py
- _RngNo
- test_piercing_k_uniforme_y_atacante_nunca_es_objetivo
- _RngMax
- SecondWindAction
- LegendaryAction
- test_sustitucion_hace_un_solo_par_de_picks
- _default_targeting

## God Nodes (most connected - your core abstractions)
1. `Attack` - 280 edges
2. `attack_roll()` - 235 edges
3. `Condition` - 234 edges
4. `Monster` - 233 edges
5. `AttackRange` - 201 edges
6. `apply_condition()` - 189 edges
7. `Abilities` - 164 edges
8. `apply_fighter()` - 156 edges
9. `PlayerCharacter` - 148 edges
10. `RollMode` - 145 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Psi Warrior (PHB 2024)` --references--> `psionic_dice_count()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/classes.py
- `Psi Warrior (PHB 2024)` --references--> `psionic_die_sides()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/classes.py
- `Psi Warrior (PHB 2024)` --references--> `bulwark_targets()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/classes.py

## Import Cycles
- None detected.

## Communities (175 total, 44 thin omitted)

### Community 0 - "test_fighter.py"
Cohesion: 0.10
Nodes (18): fighter_extra_attacks_for(), _abilities(), _action_surge(), _ctx_recursos(), _firmas(), _RngBajo, test_action_surge_como_maximo_un_vez_por_turno(), test_action_surge_ejecutada_restaura_la_accion_y_gasta_un_uso() (+10 more)

### Community 1 - "test_attach.py"
Cohesion: 0.12
Nodes (29): Attach, AttachOnHitEffect, enganchador_de(), _ya_cegado_por(), _atacar(), _bite(), _cloaker(), _ctx() (+21 more)

### Community 2 - "AttackRange"
Cohesion: 0.14
Nodes (40): AttackRange, _golpe_sin_armas(), _abilities(), _barbaro(), _berserker(), _ctx(), _furia_lista(), _monstruo() (+32 more)

### Community 3 - "test_giant.py"
Cohesion: 0.08
Nodes (37): apply_giant(), _de(), GiantFeatures, MightyImpelAction, _objetivos_impel(), _orden_de(), _abilities(), _barbaro() (+29 more)

### Community 4 - "test_world_tree.py"
Cohesion: 0.11
Nodes (39): apply_world_tree(), _abilities(), _aliado(), _barbaro(), _ctx(), _decision(), _elige_candidato(), espia() (+31 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.14
Nodes (43): apply_wild_heart(), _abilities(), _aliado(), _barbaro(), _ctx(), _furia(), _mods(), _mon() (+35 more)

### Community 6 - "test_proficiency.py"
Cohesion: 0.16
Nodes (20): ability_check_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia() (+12 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.09
Nodes (33): _data(), _estado(), _load(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_el_ala_que_mezcla_movimiento_avisa(), test_el_cantrip_del_lich_se_omite_con_aviso(), test_el_cli_tiene_las_opciones_legendarias() (+25 more)

### Community 8 - "test_beast.py"
Cohesion: 0.05
Nodes (71): WeaponAttackAction, apply_beast(), BeastFeatures, CallTheHuntBonus, FormOfTheBeast, _habilitar_armas_naturales(), _abilities(), _barb() (+63 more)

### Community 9 - "spell_parser.py"
Cohesion: 0.06
Nodes (18): Paquetes con fachada, _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla() (+10 more)

### Community 10 - "test_traits.py"
Cohesion: 0.10
Nodes (17): BloodFrenzy, _atacante(), _datos(), _RasgoDePrueba, _RasgoDeSalvacion, _sahuagin(), test_blood_frenzy_actua_durante_el_combate_completo(), test_el_catalogo_cubre_hooks_que_los_rasgos_aun_no_usan() (+9 more)

### Community 11 - "_arco"
Cohesion: 0.33
Nodes (10): _arco(), _ctx_curving(), _curving(), test_curving_can_use_requiere_bonus_libre(), test_curving_can_use_si_con_la_decision_si(), test_curving_decision_no_no_re_tira(), test_curving_execute_sin_otro_enemigo_no_llama_nada(), test_curving_re_tira_contra_otro_enemigo() (+2 more)

### Community 12 - "test_utility.py"
Cohesion: 0.12
Nodes (30): ConditionInstance, _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), hay_utilitaria_accion(), _orden_tamano(), _abilities() (+22 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.13
Nodes (38): _abilities(), _barbaro(), _con_cola(), _con_efecto(), espia(), _ctx(), _furia(), _mon() (+30 more)

### Community 14 - "loader.py"
Cohesion: 0.04
Nodes (30): is_area_action(), parse_attach_effects(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), parse_range_type(), _sentence_with() (+22 more)

### Community 15 - "SamuraiFeatures"
Cohesion: 0.10
Nodes (9): Samurai (XGE), fighting_spirit_temp_hp(), fighting_spirit_uses(), _procesar_turnos_extra(), _de(), SamuraiFeatures, test_tabla_fighting_spirit_temp_hp_por_nivel(), test_tabla_fighting_spirit_uses_por_nivel() (+1 more)

### Community 16 - "_fighter"
Cohesion: 0.10
Nodes (31): _check_fallada(), _ctx(), _fighter(), _objetivo(), _save_fallada(), _saving_nueva(), _second_wind(), test_action_surge_no_existe_en_nivel_1() (+23 more)

### Community 17 - "apply_battle_master"
Cohesion: 0.05
Nodes (42): maneuvers_known_count(), superiority_dice_count(), superiority_die_sides(), apply_battle_master(), BattleMasterRallyAction, FeintingAttackAction, _abilities(), _atacado_dos_enemigos() (+34 more)

### Community 18 - "_samurai"
Cohesion: 0.12
Nodes (30): _capturador(), _contador_pick(), _ctx(), _ctx_ataque(), _enemigo(), _samurai(), _si(), test_con_el_pick_no_la_muerte_sigue_normal() (+22 more)

### Community 19 - "AttackAction"
Cohesion: 0.09
Nodes (21): _declara_uso(), _usage(), parse_usage(), UnknownUsageError, _warn(), AttackAction, _area_action(), _data() (+13 more)

### Community 20 - "apply_class"
Cohesion: 0.13
Nodes (19): apply_class(), ClassDef, normalize_class_name(), register_class(), SubclassDef, _abilities(), _firmas(), _pj() (+11 more)

### Community 21 - "inflict_damage"
Cohesion: 0.03
Nodes (38): Psi Warrior (PHB 2024), roll_dice(), DamageType, parse_damage_type(), proficiency_bonus(), sample(), _apply_condition_riders(), ArcaneArcherFeatures (+30 more)

### Community 22 - "ActionUsage"
Cohesion: 0.15
Nodes (11): ActionUsage, UsageKind, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar(), test_per_day_dos_usos_y_luego_can_use_falso(), test_per_day_no_tira_recarga(), test_per_day_reset_restaura_todos_los_usos(), test_recharge_5_6_porcentaje_de_exito() (+3 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.08
Nodes (53): extra_attacks_for(), rage_uses(), apply_barbarian(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj() (+45 more)

### Community 24 - "test_superior_invisibility.py"
Cohesion: 0.30
Nodes (12): remove_invisibility_on_action(), _accion(), _ctx(), _pixie(), _pj(), test_atacar_con_ventaja_y_no_pierde_la_invisibilidad(), test_ejecutarla_aplica_el_estado(), test_el_monstruo_recibe_su_accion_al_construirse() (+4 more)

### Community 25 - "ZealotFeatures"
Cohesion: 0.09
Nodes (10): apply_zealot(), _de(), _en_60_pies(), _es_aliado(), _furia_de(), _reserva_dados(), ZealotFeatures, test_apply_class_por_clave_aplica_zealot() (+2 more)

### Community 26 - "BattleragerFeatures"
Cohesion: 0.12
Nodes (6): apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), SpikedArmorAction, test_apply_exige_clase_barbaro()

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 28 - "Monster"
Cohesion: 0.13
Nodes (26): Monster, _abilities(), _disparo(), _RngFalla, test_banishing_arrow_falla_la_salvacion_y_deja_incapacitado(), test_banishing_arrow_salvacion_exitosa_no_aplica_condicion(), test_beguiling_arrow_hechiza_y_termina_si_el_aliado_ataca(), test_beguiling_sin_aliados_no_tira_salvacion() (+18 more)

### Community 29 - "load_monster"
Cohesion: 0.06
Nodes (37): _armor_class_value(), load_monster(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper(), test_cache_avoids_second_network() (+29 more)

### Community 30 - "test_parry.py"
Cohesion: 0.27
Nodes (20): _arquero_parry(), _ataque(), _ctx(), _datos(), _fijar_d20(), espia(), _gladiador(), _pj() (+12 more)

### Community 31 - ".alive"
Cohesion: 0.03
Nodes (20): _armas_melee_de(), _aliados_en_aura(), _en_aura(), _aliados_heridos(), _de(), _en_10_pies(), _es_aliado(), _armas_melee_de() (+12 more)

### Community 32 - "FighterFeatures"
Cohesion: 0.09
Nodes (5): ActionSurgeAction, _contexto(), _en_5_pies(), FighterFeatures, _rasgo()

### Community 33 - "_ExplotaSiUsaRng"
Cohesion: 0.17
Nodes (20): _accion_rally(), _commanda(), _ExplotaSiUsaRng, _sustituye(), test_commanders_strike_cede_el_ataque_si_hay_feinting_encolado(), test_commanders_strike_no_se_decide_si_el_aliado_no_tiene_armas(), test_commanders_strike_no_se_decide_si_el_aliado_ya_uso_su_reaccion(), test_commanders_strike_no_se_decide_sin_aliados_elegibles() (+12 more)

### Community 34 - "test_skills.py"
Cohesion: 0.11
Nodes (24): skill_ability(), skill_bonus(), skill_check(), _abilities(), _ctx(), _load_fixture(), _pj(), _SoloMod (+16 more)

### Community 35 - "traits/__init__.py"
Cohesion: 0.06
Nodes (13): DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante(), aliados_capaces(), _condicion_posicional() (+5 more)

### Community 36 - "test_arcane_archer.py"
Cohesion: 0.11
Nodes (23): arcane_shot_options_known(), arcane_shot_uses(), apply_arcane_archer(), CurvingShotAction, _firmas(), _pj(), test_accion_curving_se_anade_desde_el_nivel_7(), test_apply_arcane_archer_exige_la_clase_fighter() (+15 more)

### Community 37 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 38 - "casting.py"
Cohesion: 0.12
Nodes (5): SaveAction, HealAction, dado_por_nivel(), duracion_en_rondas(), HealEffect

### Community 39 - "test_relentless.py"
Cohesion: 0.11
Nodes (20): _entradas(), parse_traits(), Relentless, test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd(), test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad(), _ctx(), _datos(), _jabali() (+12 more)

### Community 40 - "test_mastery.py"
Cohesion: 0.10
Nodes (28): al_acertar(), al_fallar(), _cd_topple(), _log(), _nombre(), resolver_maestria(), _arma(), _atacante() (+20 more)

### Community 41 - "BarbarianFeatures"
Cohesion: 0.10
Nodes (5): BarbarianFeatures, ExtendRageAction, _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 42 - "Abilities"
Cohesion: 0.09
Nodes (37): Abilities, end_turn(), _data(), _load(), _pj(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente(), test_can_act_y_can_react(), test_condicion_fuera_del_enum_lanza_value_error() (+29 more)

### Community 43 - "dnd_sim/__init__.py"
Cohesion: 0.05
Nodes (18): ability_mod(), rage_damage(), CombatState, d20(), roll_d20(), ActionType, AttackEntry, CombatAction (+10 more)

### Community 44 - "test_area.py"
Cohesion: 0.24
Nodes (22): AreaTargeting, select_area_targets(), SaveDamage, _area_action(), _ctx(), _npc(), _pj(), _save_forzado() (+14 more)

### Community 45 - "TelekineticMasterAction"
Cohesion: 0.11
Nodes (16): _armas_de(), _de(), _telekinetic_master_vigente(), TelekineticMasterAction, TelekineticMasterAttackAction, _master(), test_el_ataque_adicional_exige_efecto_activo_y_bonus_libre(), test_el_ataque_adicional_usa_el_helper_de_ataque_del_motor() (+8 more)

### Community 46 - "test_invisibility.py"
Cohesion: 0.21
Nodes (24): _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj(), test_atacar_a_un_invisible_tiene_desventaja(), test_atacar_deja_de_ser_invisible() (+16 more)

### Community 47 - "BattleMasterFeatures"
Cohesion: 0.08
Nodes (7): Battle Master (PHB 2024), _aliados(), _aliados_elegibles(), _armas_melee_propias(), _armas_propias(), BattleMasterFeatures, _de()

### Community 48 - "test_battle_master.py"
Cohesion: 0.06
Nodes (64): _accion_feinting(), _atacado(), _conoce_sweeping(), _decide(), _ejecuta(), _mods(), _parry(), _ripostea_directa() (+56 more)

### Community 49 - "main.py"
Cohesion: 0.11
Nodes (22): CLI del simulador: `build_parser()`, Detalle por flag, Ejemplos, Flujo de `main()`, `--legendary-p`, `--legendary-points`, `--monster` / `-m`, Observaciones (para humanos y IA) (+14 more)

### Community 50 - "apply_condition"
Cohesion: 0.05
Nodes (58): has_escape_text(), ability_check(), CheckResult, _cd_ataque(), apply_condition(), attempt_escapes(), _condicion_bloqueada(), _contar() (+50 more)

### Community 51 - "PlayerCharacter"
Cohesion: 0.12
Nodes (18): PlayerCharacter, apply_samurai(), _abilities(), _pj(), test_apply_class_y_apply_samurai_son_equivalentes(), test_apply_samurai_exige_la_clase_guerrero(), test_apply_samurai_exige_nivel_minimo_tres(), test_el_bonus_proficiency_anade_una_habilidad_nueva() (+10 more)

### Community 52 - "_con_estilo"
Cohesion: 0.21
Nodes (17): _aliado(), _con_estilo(), _enemigo(), _mods(), _RngSi, test_interception_con_un_aliado_no_baja_de_cero_el_daño(), test_interception_no_actúa_con_la_reacción_gastada(), test_interception_no_actúa_contra_un_no_aliado_ni_con_el_mismo_pj() (+9 more)

### Community 53 - "legendary_phase"
Cohesion: 0.17
Nodes (22): legendary_phase(), _contexto(), _pj(), test_con_una_sola_accion_asequible_pick_no_consume_rng(), test_dos_duenos_legendarios_actuan_cada_uno_una_vez(), test_el_combate_termina_en_medio_de_la_fase(), test_la_fase_ocurre_despues_del_end_turn(), test_la_resistencia_funciona_en_todas_las_rutas() (+14 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.12
Nodes (16): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+8 more)

### Community 57 - "attack_roll"
Cohesion: 0.07
Nodes (28): Arcane Archer (XGE), Cavalier (XGE), _actualizar_distancia(), _agrandado(), attack_roll(), _bando_del(), _bonus_de_rasgos(), _bonus_de_tamano() (+20 more)

### Community 59 - "test_champion.py"
Cohesion: 0.06
Nodes (56): champion_crit_threshold(), heroic_rally_amount(), apply_champion(), evaluar_d20(), umbral_critico(), _abilities(), _champion(), _fighter() (+48 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.09
Nodes (26): ConditionEffect, test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa() (+18 more)

### Community 61 - "begin_turn"
Cohesion: 0.27
Nodes (15): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+7 more)

### Community 62 - "WildHeartFeatures"
Cohesion: 0.12
Nodes (6): _con_beneficio(), _de(), _en_5_pies(), _hostil(), _orden_de(), WildHeartFeatures

### Community 64 - "lair_loader.py"
Cohesion: 0.23
Nodes (6): _check_fields(), _construir(), _error(), load_lair(), test_esquema_invalido(), test_targeting_fuera_de_rango()

### Community 65 - "test_storm_herald.py"
Cohesion: 0.12
Nodes (40): apply_storm_herald(), _abilities(), _aliado(), _barbaro(), _ctx(), _fijar_fallo_reaccion(), falla(), _fijar_salvacion() (+32 more)

### Community 66 - "save_modifiers"
Cohesion: 0.24
Nodes (9): save_modifiers(), _datos(), _lich(), _pj(), test_con_ventaja_acierta_mas_que_sin_ella(), test_da_ventaja_si_la_salvacion_es_de_conversion(), test_el_lich_carga_su_turn_resistance(), test_sin_el_tipo_de_efecto_no_aplica() (+1 more)

### Community 67 - "test_backgrounds.py"
Cohesion: 0.12
Nodes (20): Background, normalize_tool(), get_background(), _add(), load_background(), parse_background(), _abilities(), _pj() (+12 more)

### Community 68 - "Condition"
Cohesion: 0.08
Nodes (31): Condition, _fuego(), _parchea_fuego(), _d20(), _piedra(), test_fire_rune_al_fallar_la_salvacion_restringe_con_dano_extra(), test_fire_rune_dania_2d6_al_inicio_del_turno_del_objetivo(), test_fire_rune_dos_invocaciones_dejan_una_sola_marca() (+23 more)

### Community 69 - "apply_fighter"
Cohesion: 0.13
Nodes (32): apply_fighter(), _pj(), _pj_con_armas(), test_apply_class_reenvía_el_estilo_de_combate(), test_apply_fighter_acepta_las_habilidades_de_la_lista(), test_apply_fighter_anade_el_rasgo_guerrero(), test_apply_fighter_asigna_salvaciones_de_fue_y_con(), test_apply_fighter_rechaza_habilidades_fuera_de_la_lista() (+24 more)

### Community 70 - "apply_cavalier"
Cohesion: 0.10
Nodes (19): cavalier_mark_uses(), warding_maneuver_uses(), apply_cavalier(), CavalierMarkAttackAction, _cavalier(), _firmas(), _pj(), test_apply_cavalier_exige_la_clase_fighter() (+11 more)

### Community 71 - "test_lair.py"
Cohesion: 0.11
Nodes (18): _dragon(), lairs_dir(), _orden_con(), _pj(), _spy_turnos(), spy(), test_fixture_sintetica_carga(), test_guarida_pasa_magical_a_las_salvaciones() (+10 more)

### Community 72 - "_bajo_golpe"
Cohesion: 0.18
Nodes (18): _ataca(), _bajo_golpe(), _parchea_golpe(), _salvacion(), test_el_ataque_adicional_no_activa_psionic_strike_mas_de_una_vez(), test_el_dado_del_psionic_strike_sigue_la_regla_de_criticos_del_motor(), test_el_empuje_de_10_ft_de_telekinetic_thrust_es_dato_sin_efecto(), test_el_flag_de_psionic_strike_se_reinicia_cada_turno() (+10 more)

### Community 73 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 74 - "psionic_dice_count"
Cohesion: 0.11
Nodes (20): psionic_dice_count(), _amiga(), _parchea_campo(), _recibe(), test_el_protective_field_comparte_la_reaccion_del_turno(), test_el_protective_field_no_actua_con_cero_de_dano(), test_el_protective_field_no_actua_por_debajo_del_nivel_tres(), test_el_protective_field_no_baja_el_daño_de_cero() (+12 more)

### Community 76 - "_ctx"
Cohesion: 0.12
Nodes (14): _ctx(), _EspiaPrueba, _EspiaSalvacion, test_el_bonificador_de_la_consulta_se_suma_a_la_prueba(), test_el_bonificador_de_la_consulta_se_suma_a_la_salvacion(), _d20_fijo(), test_en_pruebas_de_habilidad_se_pasa_la_caracteristica_efectiva(), test_la_consulta_mira_a_los_otros_vivos_y_no_a_muertos_o_incapacitados() (+6 more)

### Community 77 - "test_races.py"
Cohesion: 0.10
Nodes (24): Race, load_race(), parse_race(), _spells_from_description(), _abilities(), _fiendish_legacy(), _keen_senses(), _pj() (+16 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.09
Nodes (28): doblar_dados(), SpellAction, Spellcasting, _accion(), _ataque(), _ctx(), _datos(), _duergar() (+20 more)

### Community 79 - "_ctx"
Cohesion: 0.17
Nodes (19): _ataque(), _ctx(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja(), test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_las_condiciones_incapacitantes_fallan_fue_y_des_sin_tirar_dados() (+11 more)

### Community 80 - "test_psi_warrior.py"
Cohesion: 0.12
Nodes (25): bulwark_targets(), _elegibles_bulwark(), PsiBulwarkAction, effective_ac(), _abilities(), _bulwark(), _pj(), test_apply_psi_warrior_por_debajo_del_nivel_3_da_value_error() (+17 more)

### Community 81 - "run_combat"
Cohesion: 0.25
Nodes (11): run_combat(), _summarize_damage(), _eventos(), _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(), test_dos_combates_seguidos_empiezan_con_el_aliento_cargado(), test_dragon_nunca_usa_el_aliento_dos_turnos_seguidos_sin_recarga() (+3 more)

### Community 82 - "test_arquitectura.py"
Cohesion: 0.24
Nodes (5): _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api()

### Community 83 - "pick"
Cohesion: 0.06
Nodes (12): pick(), _extract(), first_target_policy(), random_policy(), actor_is_alive(), _en_accion_de_ataque(), ConditionAction, _romper_invisibilidad_al_lanzar() (+4 more)

### Community 84 - "test_damage.py"
Cohesion: 0.10
Nodes (21): simulate(), _guerrero_y_ogro(), _target(), test_attack_roll_log_modifier(), test_danio_medio_por_combatiente_y_equipo(), test_etiqueta_de_modificadores_se_deriva_del_dano_final(), test_immune_target_takes_zero_damage(), test_immunity_zero() (+13 more)

### Community 85 - "test_spells.py"
Cohesion: 0.09
Nodes (49): parse_spell(), SpellAttackAction, SpellFixedDamageAction, spell_action(), apply_concentration(), _ctx(), _npc(), _pj() (+41 more)

### Community 86 - "test_rune_knight.py"
Cohesion: 0.11
Nodes (19): Rune Knight (TCE), giants_might_die_sides(), runes_known_count(), runic_shield_uses(), _escudo_partida(), _parchea_escudo(), _runas_sin_fuego(), test_cloud_rune_sin_otro_enemigo_no_consulta_pick() (+11 more)

### Community 87 - "test_azer.py"
Cohesion: 0.26
Nodes (17): _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), _rasgo(), test_ataque_a_distancia_no_dispara_la_represalia() (+9 more)

### Community 88 - "json"
Cohesion: 0.14
Nodes (8): _cache_path(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError, NetworkError

### Community 89 - "test_extra_damage.py"
Cohesion: 0.17
Nodes (18): DamageRecorder, _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional() (+10 more)

### Community 90 - "test_sustituir_ataque.py"
Cohesion: 0.17
Nodes (10): _sustituir_ataque(), _abilities(), _blanco(), _pj(), _RasgoQueSustituye, _RasgoSinSustitucion, _RngExplota, test_rasgo_que_devuelve_none_conserva_el_flujo_y_las_semillas() (+2 more)

### Community 91 - "_carga"
Cohesion: 0.16
Nodes (14): _ataque_carga(), _carga(), _salvacion(), test_ferocious_charger_cd_es_ocho_mas_pb_mas_fuerza(), test_ferocious_charger_con_p_medio_tira_un_random(), test_ferocious_charger_el_flag_se_reinicia_cada_turno(), test_ferocious_charger_nivel_14_no_actua_sin_rng(), test_ferocious_charger_p_cero_no_carga_sin_rng() (+6 more)

### Community 92 - "_psi"
Cohesion: 0.14
Nodes (9): _guardado(), _psi(), test_guarded_mind_concede_resistencia_psiquica_a_partir_del_nivel_10(), test_guarded_mind_no_actua_por_debajo_del_nivel_diez(), test_guarded_mind_sin_ctx_rng_no_purga(), test_guarded_mind_sin_dados_no_purga(), test_los_dados_y_el_tamano_segun_el_nivel_se_rellenan_al_aplicar(), test_reset_rellena_la_reserva_completa() (+1 more)

### Community 93 - "test_ancestral_guardian.py"
Cohesion: 0.10
Nodes (28): AncestralGuardianFeatures, apply_ancestral_guardian(), _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado() (+20 more)

### Community 94 - "test_cavalier.py"
Cohesion: 0.14
Nodes (23): cavalier_mark_extra_damage(), _accion_marca(), _cargar_main(), _especial(), _parchea_ataque(), _pick_sin_decision(), test_daño_extra_del_ataque_especial_es_el_nivel_entre_dos(), test_el_ataque_especial_no_gasta_un_uso_ni_la_reaccion() (+15 more)

### Community 95 - "StormHeraldFeatures"
Cohesion: 0.09
Nodes (7): _cd(), _dado_mar(), _de(), _enemigos_en_aura(), _escalado(), StormAuraAction, StormHeraldFeatures

### Community 96 - "consumir_marcas"
Cohesion: 0.17
Nodes (20): consumir_marcas(), _abilities(), _marca_con(), _marcado(), _mods(), _RngSi, test_incapacitado_el_marcador_anula_la_marca(), test_la_marca_caduca_en_la_ronda_indicada() (+12 more)

### Community 97 - "_nube_partida"
Cohesion: 0.13
Nodes (12): rune_uses(), _nube_partida(), _pick(), _parchea_nube(), test_cloud_rune_con_pick_no_no_redirige(), test_cloud_rune_conserva_el_critico_sobre_el_nuevo_objetivo(), test_cloud_rune_el_reset_de_combate_deja_todo_limpio(), test_cloud_rune_gasta_la_reaccion_en_el_primer_golpe() (+4 more)

### Community 98 - "CombatContext"
Cohesion: 0.11
Nodes (8): CombatContext, _living_enemies(), _log(), AreaSaveAction, _breath(), _FixedRandom, test_begin_turn_no_tira_nada_si_estan_cargadas(), test_begin_turn_reinicia_recursos_y_tira_una_recarga_por_accion()

### Community 99 - "test_zealot.py"
Cohesion: 0.10
Nodes (38): ZealousPresenceAction, _abilities(), _aliado(), _barbaro(), _decision(), _fallos(), _forma(), _guarda_con() (+30 more)

### Community 100 - "TurnResources"
Cohesion: 0.19
Nodes (31): TurnResources, AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer(), _bj() (+23 more)

### Community 101 - "AtaqueSustituido"
Cohesion: 0.12
Nodes (12): AtaqueSustituido, _RngSi, test_arcane_shot_se_aplica_una_sola_vez_por_turno(), test_arcane_shot_se_gasta_un_uso_al_aplicar(), test_daño_de_arcane_shot_es_2d6_antes_del_18(), _dado(), test_daño_de_arcane_shot_es_4d6_desde_el_18(), test_decision_de_impacto_no_gasta_el_uso_hasta_impactar() (+4 more)

### Community 102 - "_pj"
Cohesion: 0.22
Nodes (19): espia(), _espiar_divine(), _furia(), _mon(), _pj(), test_determinismo_misma_semilla_mismos_resultados(), corrida(), test_divine_fury_elige_radiante_con_pick() (+11 more)

### Community 103 - "apply_psi_warrior"
Cohesion: 0.15
Nodes (8): psionic_die_sides(), apply_psi_warrior(), _firmas(), test_apply_class_equivalente_a_apply_psi_warrior(), test_apply_psi_warrior_sin_clase_guerrero_da_value_error(), test_el_tamano_del_dado_psionico_es_d6_d8_d10_o_d12_segun_el_nivel(), test_guarded_mind_no_acumula_la_resistencia_si_ya_la_tenia(), _trait()

### Community 104 - "Any"
Cohesion: 0.13
Nodes (8): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), _presupuesto(), registrar_resistencia_legendaria()

### Community 105 - "_pj"
Cohesion: 0.16
Nodes (15): apply_rune_knight(), _pj(), _rune(), test_aplicar_con_nivel_inferior_a_tres_da_error(), test_aplicar_sin_clase_guerrero_da_error(), test_apply_class_y_apply_rune_knight_son_equivalentes(), test_karg_runas_invalido_da_error(), test_master_of_runes_registra_las_tres_acciones_de_invocacion() (+7 more)

### Community 106 - "Attack"
Cohesion: 0.17
Nodes (25): D20Result, RollMode, Attack, test_commanders_strike_con_relentless_no_gasta_dado(), test_commanders_strike_el_dueño_nunca_es_el_aliado_elegido(), test_commanders_strike_sustituye_el_ataque_y_el_aliado_gasta_su_reaccion(), _d20(), test_el_ataque_del_aliado_no_reentra_en_commanders_strike() (+17 more)

### Community 107 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 108 - "valid_targets"
Cohesion: 0.05
Nodes (22): log_line(), _objetivo_enganche(), valid_targets(), _invoke_policy(), _pasada(), _bolstering(), _cd(), _de() (+14 more)

### Community 109 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 110 - "roll_initiative"
Cohesion: 0.18
Nodes (10): roll_initiative(), _d20_fijo(), test_ambush_con_la_decision_no_no_gasta_nada(), test_ambush_con_relentless_no_gasta_dado(), test_ambush_sin_dados_no_consume_rng(), test_ambush_sin_la_maniobra_no_consume_rng(), test_ambush_suma_un_dado_a_la_tirada_de_iniciativa(), test_sin_subclase_roll_initiative_no_consulta_bonus() (+2 more)

### Community 111 - "_arquero"
Cohesion: 0.11
Nodes (18): _arquero(), _RngExplota, test_arcane_shot_crea_usos_por_nivel(), test_arcane_shot_se_reinicia_en_on_turn_start(), test_arcane_shot_sin_rng_no_actua(), test_arcane_shot_sin_usos_cero_rng(), test_ataque_cuerpo_a_cuerpo_cero_rng(), test_cd_de_arcane_shot_es_8_mas_pb_mas_int() (+10 more)

### Community 112 - "capas.py"
Cohesion: 0.20
Nodes (5): capa_de(), main(), visit_ImportFrom(), modulo_de(), resolver()

### Community 113 - "_RngExplota"
Cohesion: 0.29
Nodes (3): _RngExplota, test_resolver_maestria_sin_maestria_no_consulta_tactical_master(), test_tactical_master_no_sustituye_bajo_el_nivel_9()

### Community 114 - "RuneInvokeAction"
Cohesion: 0.13
Nodes (15): RuneInvokeAction, _accion_storm(), _invocada(), test_activar_storm_gasta_un_uso_y_levanta_el_estado(), test_frost_invocado_suma_dos_a_fue_y_con_en_pruebas_y_salvaciones(), _prueba(), _sal(), test_hill_concede_resistencia_bpc_no_acumula_y_se_revoca_al_reset() (+7 more)

### Community 116 - "Any"
Cohesion: 0.29
Nodes (3): _avisar_fallo_prueba(), _guia(), _resolve_mods()

### Community 117 - "GiantsMightAction"
Cohesion: 0.13
Nodes (13): giants_might_uses(), _de(), GiantsMightAction, _giant_pj(), test_giant_might_da_ventaja_solo_en_fuerza(), test_giant_might_daño_extra_una_vez_por_turno(), test_giant_might_el_dado_de_daño_sube_con_el_nivel(), test_giant_might_el_tamano_vuelve_al_original_en_reset() (+5 more)

### Community 119 - "RageAction"
Cohesion: 0.10
Nodes (15): RageAction, apply_berserker(), BerserkerFeatures, _de(), _furia_de(), IntimidatingPresenceAction, _presencia_ctx(), test_apply_anade_trait_y_accion() (+7 more)

### Community 120 - "ChampionFeatures"
Cohesion: 0.21
Nodes (3): Champion (PHB 2024), ChampionFeatures, _de()

### Community 121 - "build_spell_actions"
Cohesion: 0.17
Nodes (10): build_spell_actions(), parse_spellcasting(), _desde_fixture(), _monstruo_lanzador(), test_el_lanzador_se_lee_de_los_actions(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_uso_propio() (+2 more)

### Community 123 - "SaveResult"
Cohesion: 0.19
Nodes (13): _log_target(), _mode_tag(), _outcome_tag(), _log_line_outcome(), SaveResult, _fake(), stub(), stub() (+5 more)

### Community 124 - "parse_escape"
Cohesion: 0.33
Nodes (4): parse_escape(), _skills_for(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 125 - "WarriorHealAction"
Cohesion: 0.25
Nodes (15): WarriorHealAction, _accion(), _ctx(), test_fanatical_no_activo_sin_furia(), test_nivel_3_no_recibe_rasgos_superiores(), test_warrior_curacion_gasta_un_dado_y_suma_pv(), test_warrior_curacion_no_supera_el_maximo(), test_warrior_de_los_dioses_reserva_por_nivel() (+7 more)

### Community 126 - "_bajo_ataque"
Cohesion: 0.12
Nodes (25): _bajo_ataque(), _defiende(), _parchea_warding(), _RngExplota, test_hold_the_line_con_decision_negativa_no_gasta_nada(), test_hold_the_line_exige_nivel_10(), test_hold_the_line_no_contra_un_atacante_muerto_o_no_enemigo(), test_hold_the_line_no_reentra_con_un_ataque_de_reacción() (+17 more)

### Community 127 - "_abilities"
Cohesion: 0.12
Nodes (10): _abilities(), test_giant_might_el_daño_extra_es_del_tipo_del_arma(), test_las_distancias_de_las_runas_son_dato_sin_efecto(), test_rune_knight_integra_en_run_combat_con_semilla_fija(), test_sin_subclase_giant_might_no_consulta_rng(), test_sin_subclase_la_cloud_rune_no_consulta_rng(), test_sin_subclase_la_fire_rune_no_consulta_rng(), test_sin_subclase_la_stone_rune_no_consulta_rng() (+2 more)

### Community 128 - "random"
Cohesion: 0.25
Nodes (18): _abilities(), _ctx(), _decide(), _pj(), test_antes_del_nivel_2_no_hay_decision_ni_rng(), test_en_turno_ajeno_no_decide(), test_frecuencia_0_5_es_aproximadamente_la_mitad_de_los_turnos(), test_las_reacciones_no_deciden_ni_reciben() (+10 more)

### Community 129 - "attack_modifiers"
Cohesion: 0.23
Nodes (11): attack_modifiers(), _ataque_melee(), _pj(), _sahuagin_con_rasgo(), test_blood_frenzy_aparece_en_el_log_del_ataque(), test_blood_frenzy_da_ventaja_contra_un_objetivo_herido(), test_blood_frenzy_no_aplica_a_criaturas_sin_el_rasgo(), test_blood_frenzy_no_aplica_a_un_objetivo_a_toda_vida() (+3 more)

### Community 130 - "barbarian/__init__.py"
Cohesion: 0.12
Nodes (5): NaturalWeapon, apply_wild_magic(), WildMagicFeatures, WildSurgeAction, test_apply_anade_trait_y_accion()

### Community 131 - "Combatant"
Cohesion: 0.12
Nodes (8): Arquitectura de `dnd_sim`, Carpetas, Cómo comprobar que todo sigue en orden, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, Combatant

### Community 132 - "_clamp"
Cohesion: 0.14
Nodes (10): action_surge_uses(), _clamp(), indomitable_uses(), second_wind_uses(), weapon_mastery_count(), test_action_surge_usos_por_nivel_son_1_y_2(), test_indomitable_usos_por_nivel_son_1_2_y_3(), test_maestria_con_armas_cuenta_segun_el_nivel() (+2 more)

### Community 133 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (5): _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 134 - "LegendaryState"
Cohesion: 0.14
Nodes (15): lair_phase(), LairAction, LegendaryState, _ctx(), _enemigo(), _Stub, test_dos_acciones_uniformes(), test_no_actua_si_el_combate_cae_en_medio() (+7 more)

### Community 135 - "_avisar_ganchos_de_turno"
Cohesion: 0.18
Nodes (6): _avisar_ganchos_de_turno(), _ctx(), test_ganchos_de_turno_ajeno_estan_en_el_catalogo_y_sin_override_no_llaman(), test_ganchos_de_turno_ajeno_no_se_llaman_para_combatientes_muertos(), test_on_turn_start_se_dispara_al_inicio_del_turno(), test_on_turn_start_tambien_se_dispara_estando_incapacitado()

### Community 137 - "_run_combat"
Cohesion: 0.29
Nodes (6): combat_finished(), living_teams(), CombatResult, _run_combat(), _nuevo_ctx(), _turno()

### Community 138 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.33
Nodes (5): Grafo y verificación, Pendientes generales, Rutina sugerida al abrir sesión, TODO — DnDBalancer / dnd_sim, TODOs en código (marcados `# TODO`)

### Community 140 - "normalize_skill"
Cohesion: 0.18
Nodes (4): _clean(), normalize_skill(), test_normalize_skill_acepta_espacios_y_spanish(), test_normalize_skill_desconocida_lanza_value_error()

## Knowledge Gaps
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `test_fighter.py`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_traits.py`, `_arco`, `test_utility.py`, `test_wild_magic.py`, `loader.py`, `apply_battle_master`, `_samurai`, `apply_class`, `inflict_damage`, `apply_barbarian`, `test_superior_invisibility.py`, `BattleragerFeatures`, `test_death.py`, `Monster`, `load_monster`, `test_parry.py`, `_ExplotaSiUsaRng`, `test_arcane_archer.py`, `casting.py`, `test_relentless.py`, `test_mastery.py`, `Abilities`, `dnd_sim/__init__.py`, `test_invisibility.py`, `test_battle_master.py`, `main.py`, `apply_condition`, `PlayerCharacter`, `legendary_phase`, `attack_roll`, `test_champion.py`, `test_magic_resistance.py`, `begin_turn`, `lair_loader.py`, `test_storm_herald.py`, `apply_fighter`, `apply_cavalier`, `_bajo_golpe`, `test_pack_tactics.py`, `test_enlarge.py`, `_ctx`, `test_psi_warrior.py`, `test_damage.py`, `test_spells.py`, `test_rune_knight.py`, `test_azer.py`, `test_extra_damage.py`, `test_sustituir_ataque.py`, `_carga`, `test_ancestral_guardian.py`, `test_cavalier.py`, `consumir_marcas`, `_nube_partida`, `test_zealot.py`, `TurnResources`, `AtaqueSustituido`, `_pj`, `_pj`, `test_undead_fortitude.py`, `_arquero`, `_RngExplota`, `test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque`, `_bajo_ataque`, `_abilities`, `random`, `attack_modifiers`, `barbarian/__init__.py`, `Combatant`, `test_sustitucion_hace_un_solo_par_de_picks`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `daño_base_arma()`) actually correct?**
  _`Attack` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_fighter.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0989247311827957 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `attack_modifiers`, `Combatant`, `test_giant.py`, `AttackRange`, `LegendaryState`, `test_legendary.py`, `normalize_ability`, `spell_parser.py`, `test_beast.py`, `test_traits.py`, `test_utility.py`, `_avisar_ganchos_de_turno`, `loader.py`, `SamuraiFeatures`, `_samurai`, `inflict_damage`, `test_world_tree.py`, `test_superior_invisibility.py`, `test_wild_heart.py`, `Monster`, `test_parry.py`, `.alive`, `test_skills.py`, `traits/__init__.py`, `test_arcane_archer.py`, `test_mastery.py`, `BarbarianFeatures`, `Abilities`, `dnd_sim/__init__.py`, `TelekineticMasterAction`, `test_invisibility.py`, `BattleMasterFeatures`, `test_battle_master.py`, `apply_condition`, `PlayerCharacter`, `test_condition_immunities.py`, `attack_roll`, `test_champion.py`, `test_magic_resistance.py`, `WildHeartFeatures`, `test_storm_herald.py`, `save_modifiers`, `test_lair.py`, `_bajo_golpe`, `test_pack_tactics.py`, `psionic_dice_count`, `ConditionTracker`, `_ctx`, `test_enlarge.py`, `test_psi_warrior.py`, `test_damage.py`, `test_spells.py`, `test_rune_knight.py`, `_carga`, `_psi`, `test_cavalier.py`, `StormHeraldFeatures`, `consumir_marcas`, `_nube_partida`, `Attack`, `Any`, `RageAction`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `attack_roll()` (e.g. with `Arcane Archer (XGE)` and `Cavalier (XGE)`) actually correct?**
  _`attack_roll()` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11846689895470383 - nodes in this community are weakly interconnected._
- **Why does `PlayerCharacter` connect `PlayerCharacter` to `test_fighter.py`, `test_attach.py`, `AttackRange`, `Combatant`, `test_giant.py`, `random`, `LegendaryState`, `test_legendary.py`, `normalize_ability`, `test_beast.py`, `test_proficiency.py`, `test_traits.py`, `normalize_skill`, `attack_modifiers`, `test_utility.py`, `test_wild_magic.py`, `apply_battle_master`, `_samurai`, `AttackAction`, `apply_class`, `test_world_tree.py`, `apply_barbarian`, `test_superior_invisibility.py`, `test_wild_heart.py`, `test_death.py`, `load_monster`, `test_parry.py`, `test_skills.py`, `test_arcane_archer.py`, `test_multiattack.py`, `test_relentless.py`, `test_mastery.py`, `BarbarianFeatures`, `Abilities`, `dnd_sim/__init__.py`, `test_area.py`, `test_invisibility.py`, `test_battle_master.py`, `main.py`, `apply_condition`, `_con_estilo`, `legendary_phase`, `test_condition_immunities.py`, `test_champion.py`, `test_magic_resistance.py`, `begin_turn`, `test_storm_herald.py`, `save_modifiers`, `test_backgrounds.py`, `apply_fighter`, `apply_cavalier`, `test_lair.py`, `test_pack_tactics.py`, `test_races.py`, `test_enlarge.py`, `test_psi_warrior.py`, `run_combat`, `test_damage.py`, `test_spells.py`, `test_rune_knight.py`, `test_azer.py`, `test_extra_damage.py`, `test_sustituir_ataque.py`, `test_ancestral_guardian.py`, `test_cavalier.py`, `test_zealot.py`, `TurnResources`, `_pj`, `_pj`, `test_martial_advantage.py`, `test_undead_fortitude.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
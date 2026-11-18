# Graph Report - DnDBalancer  (2026-11-18)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 4866 nodes · 17869 edges · 175 communities (132 shown, 43 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 1338 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d1e2fa86`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_world_tree.py
- intentar_desenganche
- AttackRange
- _de
- test_wild_magic.py
- test_wild_heart.py
- test_rune_knight.py
- legendary_phase
- RuneKnightFeatures
- parse_spell
- test_legendary.py
- test_giant.py
- test_utility.py
- _arquero
- legendary_parser.py
- test_eldritch_knight.py
- run_combat
- test_battle_master.py
- test_samurai.py
- test_races.py
- apply_class
- combat/attack.py
- ActionUsage
- apply_barbarian
- test_parry.py
- ZealotFeatures
- test_attach.py
- test_ancestral_guardian.py
- Monster
- load_monster
- ability_check
- _clamp
- fighter/actions.py
- test_lair.py
- normalize_ability
- traits/__init__.py
- test_arcane_archer.py
- test_skills.py
- test_hechizos_pj.py
- test_magic_resistance.py
- test_mastery.py
- BarbarianFeatures
- apply_condition
- saving_throw
- capas.py
- TelekineticMasterAction
- Condition
- BattleMasterFeatures
- RollMode
- simulate
- test_checks_escapes.py
- barbarian/__init__.py
- test_area.py
- test_beast.py
- test_condition_immunities.py
- TurnResources
- test_champion.py
- pick
- begin_turn
- test_loader_actions.py
- _avisar_ataque_especial_marca
- _RngSi
- _atacado
- test_backgrounds.py
- _ejecuta
- apply_fighter
- apply_cavalier
- _fighter
- psionic_dice_count
- _parchea_campo
- test_death.py
- ConditionTracker
- _pj
- race_parser.py
- test_enlarge.py
- IntimidatingPresenceAction
- .can_act
- _run_combat
- pathlib
- test_proficiency.py
- _trait
- consumir_marcas
- PsiWarriorFeatures
- preparar_hechizos
- json
- test_extra_damage.py
- _ExplotaSiUsaRng
- _pj
- ActionType
- AncestralGuardianFeatures
- PlayerCharacter
- test_storm_herald.py
- inflict_damage
- _carga
- test_azer.py
- test_zealot.py
- BattleragerFeatures
- test_sustituir_ataque.py
- GiantsMightAction
- test_psi_warrior.py
- dnd_sim/__init__.py
- load_class_spell_list
- Attack
- _pj
- attack_roll
- _abilities
- roll_initiative
- test_pack_tactics.py
- test_loader.py
- _invocada
- _RngSi
- CombatState
- condition_parser.py
- test_undead_fortitude.py
- test_multiattack.py
- _decision
- Spellcasting
- test_spells.py
- test_superior_invisibility.py
- SaveResult
- _especial
- WarriorHealAction
- test_cavalier.py
- _guardado
- test_turn_resistance.py
- .on_turn_start
- _fallos
- Combatant
- test_fighter.py
- normalize_skill
- LegendaryState
- _RngExplota
- _duelo
- ConditionEffect
- aplicar_lanzamiento
- load_lair
- multiattack_parser.py
- maestria_de
- test_el_gancho_after_failed_check_desde_ability_check_con_ctx
- test_piercing_k_uniforme_y_atacante_nunca_es_objetivo
- _RngMax
- test_tactical_master_nivel_9_elige_entre_original_push_sap_slow
- _declara_uso
- LegendaryAction
- test_sustitucion_hace_un_solo_par_de_picks
- test_sin_autoexito_ni_autofallo_en_pruebas
- test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio

## God Nodes (most connected - your core abstractions)
1. `Attack` - 286 edges
2. `Condition` - 242 edges
3. `Monster` - 240 edges
4. `attack_roll()` - 234 edges
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
- `Rune Knight (TCE)` --references--> `GiantsMightAction`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/rules/classes/fighter/subclasses/rune_knight/actions.py
- `Rune Knight (TCE)` --references--> `RuneInvokeAction`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/rules/classes/fighter/subclasses/rune_knight/actions.py
- `Psi Warrior (PHB 2024)` --references--> `CombatState`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/combat_state.py

## Import Cycles
- None detected.

## Communities (175 total, 43 thin omitted)

### Community 0 - "test_world_tree.py"
Cohesion: 0.10
Nodes (40): apply_world_tree(), WorldTreeFeatures, _abilities(), _aliado(), _barbaro(), _ctx(), _decision(), _elige_candidato() (+32 more)

### Community 1 - "intentar_desenganche"
Cohesion: 0.24
Nodes (4): desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por()

### Community 2 - "AttackRange"
Cohesion: 0.14
Nodes (39): AttackRange, _golpe_sin_armas(), _abilities(), _barbaro(), _berserker(), _ctx(), _furia_lista(), _monstruo() (+31 more)

### Community 3 - "_de"
Cohesion: 0.06
Nodes (10): _contexto(), RageAction, _rasgo(), _armas_melee_de(), BerserkerFeatures, GiantFeatures, _objetivos_impel(), _de() (+2 more)

### Community 4 - "test_wild_magic.py"
Cohesion: 0.13
Nodes (38): _abilities(), _barbaro(), _con_cola(), _con_efecto(), espia(), _ctx(), _furia(), _mon() (+30 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.08
Nodes (46): apply_wild_heart(), _con_beneficio(), _en_5_pies(), _hostil(), WildHeartFeatures, _abilities(), _aliado(), _barbaro() (+38 more)

### Community 6 - "test_rune_knight.py"
Cohesion: 0.08
Nodes (32): _accion_storm(), _fuego(), _pick(), _parchea_fuego(), _piedra(), test_activar_storm_gasta_un_uso_y_levanta_el_estado(), test_fire_rune_al_fallar_la_salvacion_restringe_con_dano_extra(), test_fire_rune_dania_2d6_al_inicio_del_turno_del_objetivo() (+24 more)

### Community 7 - "legendary_phase"
Cohesion: 0.17
Nodes (22): legendary_phase(), _contexto(), _pj(), test_con_una_sola_accion_asequible_pick_no_consume_rng(), test_dos_duenos_legendarios_actuan_cada_uno_una_vez(), test_el_combate_termina_en_medio_de_la_fase(), test_la_fase_ocurre_despues_del_end_turn(), test_no_actua_si_el_combate_ya_terminado() (+14 more)

### Community 9 - "parse_spell"
Cohesion: 0.10
Nodes (33): _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), parse_spell(), _slot_table(), _tabla_cantrip(), _tipo_de_dano(), spell_action() (+25 more)

### Community 10 - "test_legendary.py"
Cohesion: 0.08
Nodes (34): _data(), _estado(), _load(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_con_use_probability_uno_el_danio_es_mayor_que_con_cero(), test_el_ala_que_mezcla_movimiento_avisa(), test_el_cantrip_del_lich_se_omite_con_aviso() (+26 more)

### Community 11 - "test_giant.py"
Cohesion: 0.13
Nodes (33): apply_giant(), MightyImpelAction, _abilities(), _barbaro(), _ctx(), _furia(), _giant(), _mon() (+25 more)

### Community 12 - "test_utility.py"
Cohesion: 0.13
Nodes (29): ConditionInstance, _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), _orden_tamano(), _abilities(), _ctx() (+21 more)

### Community 13 - "_arquero"
Cohesion: 0.10
Nodes (31): _arco(), _arquero(), _ctx_curving(), _curving(), _RngExplota, _RngNo, test_accion_curving_se_anade_desde_el_nivel_7(), test_arcane_shot_crea_usos_por_nivel() (+23 more)

### Community 14 - "legendary_parser.py"
Cohesion: 0.06
Nodes (26): parse_condition_effects(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary() (+18 more)

### Community 15 - "test_eldritch_knight.py"
Cohesion: 0.06
Nodes (56): eldritch_knight_cantrips(), eldritch_knight_prepared(), apply_eldritch_knight(), modificar_salvacion(), _ctx(), _ek(), _lista(), _orco() (+48 more)

### Community 16 - "run_combat"
Cohesion: 0.11
Nodes (17): CombatResult, run_combat(), _summarize_damage(), _breath(), _eventos(), _FixedRandom, _load_fixture(), _player() (+9 more)

### Community 17 - "test_battle_master.py"
Cohesion: 0.07
Nodes (46): maneuvers_known_count(), superiority_dice_count(), superiority_die_sides(), apply_battle_master(), _abilities(), _atacado_dos_enemigos(), _atacado_fijo(), _bm() (+38 more)

### Community 18 - "test_samurai.py"
Cohesion: 0.07
Nodes (52): Samurai (XGE), fighting_spirit_temp_hp(), fighting_spirit_uses(), _procesar_turnos_extra(), apply_samurai(), _abilities(), _capturador(), _contador_pick() (+44 more)

### Community 19 - "test_races.py"
Cohesion: 0.12
Nodes (23): Race, load_race(), parse_race(), _abilities(), _fiendish_legacy(), _keen_senses(), _pj(), test_apply_race_añade_competencias_fijas() (+15 more)

### Community 20 - "apply_class"
Cohesion: 0.11
Nodes (22): apply_ancestral_guardian(), apply_battlerager(), _nuevo_ataque(), apply_class(), ClassDef, normalize_class_name(), _params_de(), register_class() (+14 more)

### Community 21 - "combat/attack.py"
Cohesion: 0.05
Nodes (40): Cavalier (XGE), Paquetes con fachada, _agrandado(), _bando_del(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque() (+32 more)

### Community 22 - "ActionUsage"
Cohesion: 0.08
Nodes (18): _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _extender_tabla(), _frases(), _sumar_dados(), _uso_de_entrada(), ActionUsage (+10 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.08
Nodes (53): extra_attacks_for(), rage_uses(), apply_barbarian(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj() (+45 more)

### Community 24 - "test_parry.py"
Cohesion: 0.10
Nodes (40): _entradas(), parse_traits(), _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj() (+32 more)

### Community 25 - "ZealotFeatures"
Cohesion: 0.08
Nodes (10): apply_zealot(), _en_60_pies(), _es_aliado(), _reserva_dados(), ZealotFeatures, test_apply_anade_trait_y_dos_acciones_bonus(), test_apply_class_por_clave_aplica_zealot(), test_apply_requiere_clase_barbara() (+2 more)

### Community 26 - "test_attach.py"
Cohesion: 0.17
Nodes (26): AttachOnHitEffect, _atacar(), _bite(), _cloaker(), _ctx(), _datos(), _pj(), test_con_ventaja_el_enganche_es_a_la_cabeza_y_ciega() (+18 more)

### Community 27 - "test_ancestral_guardian.py"
Cohesion: 0.18
Nodes (26): _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado(), _escudo(), _esperado() (+18 more)

### Community 28 - "Monster"
Cohesion: 0.14
Nodes (25): Monster, _abilities(), _disparo(), _RngFalla, test_banishing_arrow_falla_la_salvacion_y_deja_incapacitado(), test_banishing_arrow_salvacion_exitosa_no_aplica_condicion(), test_beguiling_arrow_hechiza_y_termina_si_el_aliado_ataca(), test_beguiling_sin_aliados_no_tira_salvacion() (+17 more)

### Community 29 - "load_monster"
Cohesion: 0.07
Nodes (31): load_monster(), _norm_name(), ExtraDamage, apply_beast(), test_una_condicion_desconocida_de_la_api_avisa(), _ctx(), _pj(), _spell_data() (+23 more)

### Community 30 - "ability_check"
Cohesion: 0.09
Nodes (18): skill_ability(), ability_check(), _avisar_fallo_prueba(), CheckResult, _finish_check(), _guia(), _resolve_mods(), skill_bonus() (+10 more)

### Community 31 - "_clamp"
Cohesion: 0.11
Nodes (10): Rune Knight (TCE), _clamp(), giants_might_die_sides(), runes_known_count(), _redirigir_del_bando(), _repetir_d20_del_bando(), _modificar_tirada(), _runas_sin_fuego() (+2 more)

### Community 32 - "fighter/actions.py"
Cohesion: 0.22
Nodes (3): ActionSurgeAction, SecondWindAction, _rasgo()

### Community 33 - "test_lair.py"
Cohesion: 0.11
Nodes (18): _dragon(), lairs_dir(), _orden_con(), _pj(), _spy_turnos(), spy(), test_fixture_sintetica_carga(), test_guarida_pasa_magical_a_las_salvaciones() (+10 more)

### Community 34 - "normalize_ability"
Cohesion: 0.14
Nodes (5): normalize_ability(), parse_escape(), _skills_for(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 35 - "traits/__init__.py"
Cohesion: 0.04
Nodes (16): DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante(), aliados_capaces(), _condicion_posicional() (+8 more)

### Community 36 - "test_arcane_archer.py"
Cohesion: 0.11
Nodes (22): arcane_shot_options_known(), arcane_shot_uses(), apply_arcane_archer(), CurvingShotAction, _firmas(), _pj(), test_apply_arcane_archer_exige_la_clase_fighter(), test_apply_class_equivalente_a_apply_arcane_archer() (+14 more)

### Community 37 - "test_skills.py"
Cohesion: 0.13
Nodes (21): _abilities(), _ctx(), _load_fixture(), _pj(), _SoloMod, test_ability_check_no_suma_competencia_de_habilidad(), test_attempt_escapes_tira_la_habilidad(), test_caracteristica_asociada() (+13 more)

### Community 38 - "test_hechizos_pj.py"
Cohesion: 0.10
Nodes (34): SpellSlots, construir_acciones(), _caster(), _ctx(), _def_mago_falso(), _enemigo(), _guerrero(), _hechizo() (+26 more)

### Community 39 - "test_magic_resistance.py"
Cohesion: 0.10
Nodes (25): save_modifiers(), _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab() (+17 more)

### Community 40 - "test_mastery.py"
Cohesion: 0.10
Nodes (28): al_acertar(), al_fallar(), _cd_topple(), _log(), _nombre(), resolver_maestria(), _arma(), _atacante() (+20 more)

### Community 41 - "BarbarianFeatures"
Cohesion: 0.10
Nodes (4): BarbarianFeatures, ExtendRageAction, test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 42 - "apply_condition"
Cohesion: 0.06
Nodes (64): Abilities, _apply_condition_riders(), apply_condition(), _as_condition(), _condicion_bloqueada(), end_turn(), _label(), RepeatSave (+56 more)

### Community 43 - "saving_throw"
Cohesion: 0.04
Nodes (37): rage_damage(), roll_dice(), parse_damage_type(), log_line(), sample(), has_escape_text(), AttackEntry, _bolstering() (+29 more)

### Community 44 - "capas.py"
Cohesion: 0.20
Nodes (5): capa_de(), main(), visit_ImportFrom(), modulo_de(), resolver()

### Community 45 - "TelekineticMasterAction"
Cohesion: 0.11
Nodes (15): _armas_de(), _telekinetic_master_vigente(), TelekineticMasterAction, TelekineticMasterAttackAction, _master(), test_el_ataque_adicional_exige_efecto_activo_y_bonus_libre(), test_el_ataque_adicional_usa_el_helper_de_ataque_del_motor(), test_el_efecto_de_telekinesis_solo_concede_el_ataque_adicional() (+7 more)

### Community 46 - "Condition"
Cohesion: 0.19
Nodes (26): Condition, attack_modifiers(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+18 more)

### Community 47 - "BattleMasterFeatures"
Cohesion: 0.08
Nodes (6): Battle Master (PHB 2024), _aliados_elegibles(), _armas_melee_propias(), _armas_propias(), BattleMasterFeatures, _orden_tamano()

### Community 48 - "RollMode"
Cohesion: 0.11
Nodes (18): RollMode, _ctx(), _EspiaPrueba, _EspiaSalvacion, test_el_bonificador_de_la_consulta_se_suma_a_la_prueba(), test_el_bonificador_de_la_consulta_se_suma_a_la_salvacion(), _d20_fijo(), test_en_pruebas_de_habilidad_se_pasa_la_caracteristica_efectiva() (+10 more)

### Community 49 - "simulate"
Cohesion: 0.10
Nodes (24): CLI del simulador: `build_parser()`, Detalle por flag, Ejemplos, Flujo de `main()`, `--legendary-p`, `--legendary-points`, `--monster` / `-m`, Observaciones (para humanos y IA) (+16 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.10
Nodes (38): EscapeCheck, _check_fijo(), _fake(), _ctx(), _data(), _load(), _pj(), test_con_dos_caracteristicas_se_elige_una_al_azar() (+30 more)

### Community 51 - "barbarian/__init__.py"
Cohesion: 0.08
Nodes (7): SpikedArmorAction, FormOfTheBeast, NaturalWeapon, apply_wild_magic(), WildMagicFeatures, WildSurgeAction, test_apply_anade_trait_y_accion()

### Community 52 - "test_area.py"
Cohesion: 0.22
Nodes (21): AreaTargeting, select_area_targets(), _default_targeting(), _area_action(), _ctx(), _npc(), _pj(), _save_forzado() (+13 more)

### Community 53 - "test_beast.py"
Cohesion: 0.06
Nodes (69): WeaponAttackAction, BeastFeatures, CallTheHuntBonus, _habilitar_armas_naturales(), _abilities(), _barb(), _beast(), _ctx() (+61 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.13
Nodes (15): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+7 more)

### Community 57 - "TurnResources"
Cohesion: 0.10
Nodes (50): TurnResources, AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer(), _bj() (+42 more)

### Community 59 - "test_champion.py"
Cohesion: 0.06
Nodes (57): champion_crit_threshold(), heroic_rally_amount(), evaluar_d20(), umbral_critico(), _abilities(), _champion(), _fighter(), _firmas() (+49 more)

### Community 60 - "pick"
Cohesion: 0.03
Nodes (21): Champion (PHB 2024), pick(), _contexto(), _en_5_pies(), _es_aliado(), FighterFeatures, ArcaneArcherFeatures, _ctx_con_rng() (+13 more)

### Community 61 - "begin_turn"
Cohesion: 0.27
Nodes (15): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+7 more)

### Community 62 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (14): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+6 more)

### Community 64 - "_avisar_ataque_especial_marca"
Cohesion: 0.15
Nodes (6): _avisar_ataque_especial_marca(), _hooks(), _liberar_turno_extra(), _mitigacion_de_otros(), _proteccion_psionica(), _salvar_a_cero()

### Community 65 - "_RngSi"
Cohesion: 0.09
Nodes (19): _accion_feinting(), _parry(), _RngNo, _RngSi, test_feinting_encola_la_ventaja_y_el_dado_si_impacta(), test_feinting_es_elegible_con_bonus_libre_y_decision_aleatoria(), test_feinting_sin_datos_es_inelegible_sin_rng(), test_parry_con_relentless_no_gasta_el_dado() (+11 more)

### Community 66 - "_atacado"
Cohesion: 0.14
Nodes (21): _atacado(), _conoce_sweeping(), _decide(), _RngIdx, test_el_ataque_de_reaccion_no_activa_maniobras_de_sesion_1(), test_el_uso_no_se_gasta_si_no_se_ejecuta(), test_en_un_fallo_sin_precision_cero_rng(), test_feinting_sin_impacto_no_gasta_el_dado() (+13 more)

### Community 67 - "test_backgrounds.py"
Cohesion: 0.11
Nodes (19): Background, normalize_tool(), _add(), load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias() (+11 more)

### Community 68 - "_ejecuta"
Cohesion: 0.13
Nodes (19): _ejecuta(), _mods(), _RngFalla, test_disarming_attack_no_altera_el_combate_mas_que_el_dano(), test_distracting_da_ventaja_a_un_tercero_y_se_consume(), test_distracting_no_concede_ventaja_si_ya_caduco(), test_distracting_no_da_ventaja_al_marcador_ni_se_consume(), test_efectos_sin_implementacion_no_alteran_el_combate() (+11 more)

### Community 69 - "apply_fighter"
Cohesion: 0.10
Nodes (34): apply_fighter(), _abilities(), _objetivo(), _pj(), test_apply_class_reenvía_el_estilo_de_combate(), test_apply_fighter_acepta_las_habilidades_de_la_lista(), test_apply_fighter_anade_el_rasgo_guerrero(), test_apply_fighter_asigna_salvaciones_de_fue_y_con() (+26 more)

### Community 70 - "apply_cavalier"
Cohesion: 0.10
Nodes (19): cavalier_mark_uses(), warding_maneuver_uses(), apply_cavalier(), CavalierMarkAttackAction, _cavalier(), _firmas(), _pj(), test_apply_cavalier_exige_la_clase_fighter() (+11 more)

### Community 71 - "_fighter"
Cohesion: 0.12
Nodes (20): _action_surge(), _ctx_recursos(), _fighter(), _save_fallada(), _saving_nueva(), test_action_surge_como_maximo_un_vez_por_turno(), test_action_surge_ejecutada_restaura_la_accion_y_gasta_un_uso(), test_action_surge_no_es_elegible_si_la_accion_no_se_ha_gastado() (+12 more)

### Community 72 - "psionic_dice_count"
Cohesion: 0.16
Nodes (19): psionic_dice_count(), _ataca(), _bajo_golpe(), _parchea_golpe(), _salvacion(), test_el_ataque_adicional_no_activa_psionic_strike_mas_de_una_vez(), test_el_dado_del_psionic_strike_sigue_la_regla_de_criticos_del_motor(), test_el_empuje_de_10_ft_de_telekinetic_thrust_es_dato_sin_efecto() (+11 more)

### Community 73 - "_parchea_campo"
Cohesion: 0.15
Nodes (16): _amiga(), _parchea_campo(), _recibe(), test_el_protective_field_comparte_la_reaccion_del_turno(), test_el_protective_field_no_actua_con_cero_de_dano(), test_el_protective_field_no_actua_por_debajo_del_nivel_tres(), test_el_protective_field_no_baja_el_daño_de_cero(), test_el_protective_field_no_protege_a_un_enemigo() (+8 more)

### Community 74 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 76 - "_pj"
Cohesion: 0.10
Nodes (24): rune_uses(), DamageType, apply_rune_knight(), _nube_partida(), _parchea_nube(), _pj(), test_aplicar_con_nivel_inferior_a_tres_da_error(), test_aplicar_sin_clase_guerrero_da_error() (+16 more)

### Community 77 - "race_parser.py"
Cohesion: 0.25
Nodes (3): _skill_name(), _spells_from_description(), _trait_skills()

### Community 78 - "test_enlarge.py"
Cohesion: 0.14
Nodes (25): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+17 more)

### Community 79 - "IntimidatingPresenceAction"
Cohesion: 0.20
Nodes (12): apply_berserker(), IntimidatingPresenceAction, _presencia_ctx(), test_apply_anade_trait_y_accion(), test_presencia_afecta_a_un_numero_aleatorio_de_enemigos(), test_presencia_requiere_nivel_14(), test_presencia_sin_rng_no_paga(), test_presencia_sin_usos_no_esta_disponible() (+4 more)

### Community 80 - ".can_act"
Cohesion: 0.14
Nodes (17): Psi Warrior (PHB 2024), bulwark_targets(), _elegibles_bulwark(), PsiBulwarkAction, effective_ac(), _bulwark(), test_bulwark_targets_es_el_mod_de_int_con_minimo_uno(), test_el_bulwark_bonifica_las_salvaciones_de_des_pero_no_las_otras() (+9 more)

### Community 81 - "_run_combat"
Cohesion: 0.33
Nodes (5): combat_finished(), living_teams(), _run_combat(), _nuevo_ctx(), _turno()

### Community 82 - "pathlib"
Cohesion: 0.21
Nodes (5): _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api()

### Community 83 - "test_proficiency.py"
Cohesion: 0.18
Nodes (20): ability_check_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia() (+12 more)

### Community 84 - "_trait"
Cohesion: 0.15
Nodes (30): _aliado(), _check_fallada(), _con_estilo(), _ctx(), _enemigo(), _mods(), _RngSi, test_ataques_estudiados_caduca_al_final_del_siguiente_turno() (+22 more)

### Community 85 - "consumir_marcas"
Cohesion: 0.18
Nodes (19): consumir_marcas(), _abilities(), _marca_con(), _marcado(), _mods(), _RngSi, test_incapacitado_el_marcador_anula_la_marca(), test_la_marca_caduca_en_la_ronda_indicada() (+11 more)

### Community 87 - "preparar_hechizos"
Cohesion: 0.09
Nodes (26): SubclassDef, hechizo_soportado(), preparar_hechizos(), _legal(), _muestrear(), _def_a5(), _lista(), test_exceder_el_conteo_de_la_tabla_es_un_value_error() (+18 more)

### Community 88 - "json"
Cohesion: 0.14
Nodes (10): _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError (+2 more)

### Community 89 - "test_extra_damage.py"
Cohesion: 0.17
Nodes (18): DamageRecorder, _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional() (+10 more)

### Community 90 - "_ExplotaSiUsaRng"
Cohesion: 0.17
Nodes (20): _accion_rally(), _commanda(), _ExplotaSiUsaRng, _sustituye(), test_commanders_strike_cede_el_ataque_si_hay_feinting_encolado(), test_commanders_strike_no_se_decide_si_el_aliado_no_tiene_armas(), test_commanders_strike_no_se_decide_si_el_aliado_ya_uso_su_reaccion(), test_commanders_strike_no_se_decide_sin_aliados_elegibles() (+12 more)

### Community 91 - "_pj"
Cohesion: 0.12
Nodes (14): _atacante(), _ataque_melee(), _pj(), _sahuagin_con_rasgo(), test_blood_frenzy_aparece_en_el_log_del_ataque(), test_blood_frenzy_da_ventaja_contra_un_objetivo_herido(), test_blood_frenzy_no_aplica_a_criaturas_sin_el_rasgo(), test_blood_frenzy_no_aplica_a_un_objetivo_a_toda_vida() (+6 more)

### Community 92 - "ActionType"
Cohesion: 0.03
Nodes (40): Eldritch Knight (PHB 2024), valid_targets(), parse_attach_effects(), _check_fields(), _construir(), _error(), build_condition_action(), build_save_action() (+32 more)

### Community 94 - "PlayerCharacter"
Cohesion: 0.14
Nodes (17): PlayerCharacter, _guerrero_y_ogro(), _target(), test_attack_roll_log_modifier(), test_danio_medio_por_combatiente_y_equipo(), test_etiqueta_de_modificadores_se_deriva_del_dano_final(), test_immune_target_takes_zero_damage(), test_immunity_zero() (+9 more)

### Community 95 - "test_storm_herald.py"
Cohesion: 0.06
Nodes (46): _aliados_en_aura(), apply_storm_herald(), _cd(), _dado_mar(), _en_aura(), _enemigos_en_aura(), _escalado(), StormAuraAction (+38 more)

### Community 96 - "inflict_damage"
Cohesion: 0.18
Nodes (16): _absorber_pv_temporales(), inflict_damage(), _notify_damage_dealt(), _notify_damage_taken(), _ctx(), _datos(), _jabali(), _pj() (+8 more)

### Community 97 - "_carga"
Cohesion: 0.16
Nodes (14): _ataque_carga(), _carga(), _salvacion(), test_ferocious_charger_cd_es_ocho_mas_pb_mas_fuerza(), test_ferocious_charger_con_p_medio_tira_un_random(), test_ferocious_charger_el_flag_se_reinicia_cada_turno(), test_ferocious_charger_nivel_14_no_actua_sin_rng(), test_ferocious_charger_p_cero_no_carga_sin_rng() (+6 more)

### Community 98 - "test_azer.py"
Cohesion: 0.26
Nodes (17): _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), _rasgo(), test_ataque_a_distancia_no_dispara_la_represalia() (+9 more)

### Community 99 - "test_zealot.py"
Cohesion: 0.18
Nodes (15): ZealousPresenceAction, _abilities(), _aliado(), _presencia(), test_presencia_con_cobertura_uno_no_consume_rng(), test_presencia_da_ventaja_en_ataques_a_aliados(), test_presencia_da_ventaja_en_salvaciones_a_aliados(), test_presencia_gasta_una_furia_y_restaura_el_uso_gratis() (+7 more)

### Community 101 - "test_sustituir_ataque.py"
Cohesion: 0.13
Nodes (14): Arcane Archer (XGE), _sustituir_ataque(), AtaqueSustituido, test_ever_ready_shot_no_cambia_los_usos_al_empezar_un_combate(), _abilities(), _blanco(), _pj(), _RasgoQueSustituye (+6 more)

### Community 102 - "GiantsMightAction"
Cohesion: 0.15
Nodes (11): giants_might_uses(), GiantsMightAction, _giant_pj(), test_giant_might_daño_extra_una_vez_por_turno(), test_giant_might_el_dado_de_daño_sube_con_el_nivel(), test_giant_might_el_tamano_vuelve_al_original_en_reset(), test_giant_might_en_nivel_dieciocho_el_tamano_es_enorme(), test_giant_might_no_es_elegible_sin_usos_ni_con_la_accion_gastada() (+3 more)

### Community 103 - "test_psi_warrior.py"
Cohesion: 0.12
Nodes (20): psionic_die_sides(), apply_psi_warrior(), _abilities(), _firmas(), _pj(), _psi(), test_apply_class_equivalente_a_apply_psi_warrior(), test_apply_psi_warrior_por_debajo_del_nivel_3_da_value_error() (+12 more)

### Community 104 - "dnd_sim/__init__.py"
Cohesion: 0.05
Nodes (23): ability_mod(), d20(), roll_d20(), proficiency_bonus(), _objetivo_enganche(), _invoke_policy(), _pasada(), _extract() (+15 more)

### Community 105 - "load_class_spell_list"
Cohesion: 0.15
Nodes (6): load_class_spell_list(), _get_spell_fixture(), test_la_lista_de_clase_se_parsea_con_nivel_y_escuela(), test_la_lista_se_guarda_en_cache_y_la_segunda_vez_no_toca_la_red(), test_un_hechizo_que_no_existe_se_omite_sin_romper_la_lista(), _get()

### Community 106 - "Attack"
Cohesion: 0.13
Nodes (26): D20Result, Attack, espia(), test_commanders_strike_con_relentless_no_gasta_dado(), test_commanders_strike_sustituye_el_ataque_y_el_aliado_gasta_su_reaccion(), _d20(), test_el_ataque_del_aliado_no_reentra_en_commanders_strike(), test_el_dado_de_reaccion_no_se_duplica_en_critico() (+18 more)

### Community 107 - "_pj"
Cohesion: 0.26
Nodes (17): _espiar_divine(), _furia(), _mon(), _pj(), corrida(), test_divine_fury_elige_radiante_con_pick(), test_divine_fury_funciona_a_distancia(), test_divine_fury_no_paga_en_reacciones() (+9 more)

### Community 108 - "attack_roll"
Cohesion: 0.11
Nodes (16): runic_shield_uses(), _actualizar_distancia(), attack_roll(), _mode_tag(), _escudo_partida(), _parchea_escudo(), test_cloud_rune_sin_otro_enemigo_no_consulta_pick(), test_runic_shield_convierte_un_impacto_en_fallo() (+8 more)

### Community 109 - "_abilities"
Cohesion: 0.12
Nodes (12): _abilities(), test_las_distancias_de_las_runas_son_dato_sin_efecto(), test_rune_knight_integra_en_run_combat_con_semilla_fija(), test_sin_la_subclase_rune_knight_no_se_consume_rng(), _revienta(), test_sin_subclase_cero_rng_en_invocacion_y_consultas(), test_sin_subclase_giant_might_no_consulta_rng(), test_sin_subclase_la_cloud_rune_no_consulta_rng() (+4 more)

### Community 110 - "roll_initiative"
Cohesion: 0.27
Nodes (8): roll_initiative(), _d20_fijo(), test_ambush_con_la_decision_no_no_gasta_nada(), test_ambush_con_relentless_no_gasta_dado(), test_ambush_sin_dados_no_consume_rng(), test_ambush_sin_la_maniobra_no_consume_rng(), test_ambush_suma_un_dado_a_la_tirada_de_iniciativa(), test_sin_subclase_roll_initiative_no_consulta_bonus()

### Community 111 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 112 - "test_loader.py"
Cohesion: 0.16
Nodes (12): _armor_class_value(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper(), test_cache_avoids_second_network(), test_load_monster_maps_ogre() (+4 more)

### Community 113 - "_invocada"
Cohesion: 0.16
Nodes (10): RuneInvokeAction, _invocada(), test_frost_invocado_suma_dos_a_fue_y_con_en_pruebas_y_salvaciones(), _sal(), test_hill_concede_resistencia_bpc_no_acumula_y_se_revoca_al_reset(), test_las_pruebas_caracteristicas_de_storm_son_dato_sin_efecto(), test_las_runas_despertadas_son_dato_sin_efecto(), test_master_of_runes_da_cinco_runas_y_dos_usos_desde_el_nivel_15() (+2 more)

### Community 114 - "_RngSi"
Cohesion: 0.12
Nodes (11): _RngSi, test_arcane_shot_se_aplica_una_sola_vez_por_turno(), test_arcane_shot_se_gasta_un_uso_al_aplicar(), test_daño_de_arcane_shot_es_2d6_antes_del_18(), _dado(), test_daño_de_arcane_shot_es_4d6_desde_el_18(), test_decision_de_impacto_no_gasta_el_uso_hasta_impactar(), test_piercing_gasta_el_uso_al_sustituir() (+3 more)

### Community 116 - "condition_parser.py"
Cohesion: 0.13
Nodes (6): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_range_type(), _sentence_with(), test_el_tipo_de_ataque_coincide_con_el_texto()

### Community 117 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 118 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 119 - "_decision"
Cohesion: 0.17
Nodes (14): _barbaro(), _decision(), espia(), _forma(), test_determinismo_misma_semilla_mismos_resultados(), test_forma_divina_concede_las_tres_resistencias(), test_forma_no_quita_resistencias_de_otro_origen(), test_forma_revocada_al_terminar_la_furia() (+6 more)

### Community 120 - "Spellcasting"
Cohesion: 0.15
Nodes (7): parse_spellcasting(), Spellcasting, test_el_lanzador_se_lee_de_los_actions(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_la_curacion_usa_el_modificador_de_caracteristica_no_el_bono_completo(), test_un_hechizo_de_accion_bonus_se_comprueba_en_su_fase(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 121 - "test_spells.py"
Cohesion: 0.13
Nodes (22): build_spell_actions(), _ctx(), _desde_fixture(), _monstruo_lanzador(), _npc(), _pj(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizado_invierte_los_objetivos_de_ataque() (+14 more)

### Community 122 - "test_superior_invisibility.py"
Cohesion: 0.36
Nodes (11): _accion(), _ctx(), _pixie(), _pj(), test_atacar_con_ventaja_y_no_pierde_la_invisibilidad(), test_ejecutarla_aplica_el_estado(), test_el_monstruo_recibe_su_accion_al_construirse(), test_lanzar_un_hechizo_tampoco_la_pierde() (+3 more)

### Community 123 - "SaveResult"
Cohesion: 0.16
Nodes (15): _log_target(), _mode_tag(), _outcome_tag(), _log_line_outcome(), SaveResult, falla(), espia(), stub() (+7 more)

### Community 124 - "_especial"
Cohesion: 0.26
Nodes (11): _accion_marca(), _especial(), _pick_sin_decision(), test_el_ataque_especial_no_gasta_un_uso_ni_la_reaccion(), test_el_ataque_especial_no_suma_dano_extra_si_falla(), test_el_ataque_especial_se_arma_cuando_el_marcado_dana_a_un_tercero(), test_el_ataque_especial_solo_vale_en_el_siguiente_turno(), test_el_ataque_especial_suma_el_dano_extra_si_impacta() (+3 more)

### Community 125 - "WarriorHealAction"
Cohesion: 0.25
Nodes (15): WarriorHealAction, _accion(), _ctx(), test_fanatical_no_activo_sin_furia(), test_nivel_3_no_recibe_rasgos_superiores(), test_warrior_curacion_gasta_un_dado_y_suma_pv(), test_warrior_curacion_no_supera_el_maximo(), test_warrior_de_los_dioses_reserva_por_nivel() (+7 more)

### Community 126 - "test_cavalier.py"
Cohesion: 0.10
Nodes (39): cavalier_mark_extra_damage(), _bajo_ataque(), _cargar_main(), _defiende(), _parchea_ataque(), _parchea_warding(), _RngExplota, test_daño_extra_del_ataque_especial_es_el_nivel_entre_dos() (+31 more)

### Community 127 - "_guardado"
Cohesion: 0.15
Nodes (8): _guardado(), test_guarded_mind_con_pick_no_no_purga_ni_gasta(), test_guarded_mind_concede_resistencia_psiquica_a_partir_del_nivel_10(), test_guarded_mind_no_actua_por_debajo_del_nivel_diez(), test_guarded_mind_purga_charmed_y_frightened_gastando_un_dado(), test_guarded_mind_sin_condicion_no_consulta_pick(), test_guarded_mind_sin_ctx_rng_no_purga(), test_guarded_mind_sin_dados_no_purga()

### Community 128 - "test_turn_resistance.py"
Cohesion: 0.26
Nodes (8): _datos(), _lich(), _pj(), test_con_ventaja_acierta_mas_que_sin_ella(), test_da_ventaja_si_la_salvacion_es_de_conversion(), test_el_lich_carga_su_turn_resistance(), test_sin_el_tipo_de_efecto_no_aplica(), test_solo_afecta_a_las_criaturas_con_el_rasgo()

### Community 129 - ".on_turn_start"
Cohesion: 0.21
Nodes (3): _aliados_heridos(), _cd_ataque(), _en_10_pies()

### Community 130 - "_fallos"
Cohesion: 0.27
Nodes (10): _fallos(), _guarda_con(), stub(), test_fanatical_decision_negativa_no_repiten(), test_fanatical_el_resultado_nuevo_sustituye_al_original(), test_fanatical_no_se_ofrece_en_auto_fallo(), test_fanatical_no_se_ofrece_en_salvacion_superada(), test_fanatical_repite_la_salvacion_con_bonificador_de_furia() (+2 more)

### Community 131 - "Combatant"
Cohesion: 0.10
Nodes (11): Arquitectura de `dnd_sim`, Carpetas, Cómo comprobar que todo sigue en orden, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, resolve_roll_mode() (+3 more)

### Community 132 - "test_fighter.py"
Cohesion: 0.07
Nodes (20): action_surge_uses(), fighter_extra_attacks_for(), indomitable_uses(), second_wind_uses(), weapon_mastery_count(), _firmas(), _RngBajo, _second_wind() (+12 more)

### Community 133 - "normalize_skill"
Cohesion: 0.28
Nodes (4): _clean(), normalize_skill(), test_normalize_skill_acepta_espacios_y_spanish(), test_normalize_skill_desconocida_lanza_value_error()

### Community 134 - "LegendaryState"
Cohesion: 0.15
Nodes (14): lair_phase(), LairAction, LegendaryState, _ctx(), _enemigo(), _Stub, test_dos_acciones_uniformes(), test_no_actua_si_el_combate_cae_en_medio() (+6 more)

### Community 135 - "_RngExplota"
Cohesion: 0.25
Nodes (4): _RngExplota, test_interception_sin_arma_ni_escudo_no_actúa_y_no_consume_rng(), test_resolver_maestria_sin_maestria_no_consulta_tactical_master(), test_tactical_master_no_sustituye_bajo_el_nivel_9()

### Community 136 - "_duelo"
Cohesion: 0.32
Nodes (6): _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

### Community 137 - "ConditionEffect"
Cohesion: 0.29
Nodes (4): ConditionEffect, test_la_resistencia_funciona_en_todas_las_rutas(), test_un_pj_con_ataque_con_rider_no_aplica_la_condicion_mientras_queden_usos(), test_una_condicion_sin_salvacion_ni_escape_lanza_value_error()

### Community 138 - "aplicar_lanzamiento"
Cohesion: 0.11
Nodes (10): Hechizos de PJ (PHB 2024), spell_slots_for(), SpellcastingDef, aplicar_lanzamiento(), estadisticas_lanzador(), PCSpellcasting, test_spell_slots_for_con_progresión_desconocida_es_un_value_error(), test_spell_slots_for_devuelve_la_tupla_sin_ceros_finales() (+2 more)

### Community 139 - "load_lair"
Cohesion: 0.40
Nodes (3): load_lair(), test_esquema_invalido(), test_targeting_fuera_de_rango()

### Community 140 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (5): _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 141 - "maestria_de"
Cohesion: 0.40
Nodes (4): maestria_de(), _pj_con_armas(), test_maestria_asignada_cuenta_3_4_5_6_segun_el_nivel(), test_maestria_no_eligida_no_recibe_clave()

## Knowledge Gaps
- **43 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `test_world_tree.py`, `AttackRange`, `test_wild_magic.py`, `test_wild_heart.py`, `test_rune_knight.py`, `parse_spell`, `test_legendary.py`, `test_giant.py`, `test_utility.py`, `_arquero`, `legendary_parser.py`, `test_eldritch_knight.py`, `test_battle_master.py`, `test_samurai.py`, `apply_class`, `combat/attack.py`, `apply_barbarian`, `test_parry.py`, `test_attach.py`, `test_ancestral_guardian.py`, `Monster`, `load_monster`, `test_arcane_archer.py`, `test_hechizos_pj.py`, `test_magic_resistance.py`, `test_mastery.py`, `apply_condition`, `saving_throw`, `Condition`, `RollMode`, `simulate`, `test_checks_escapes.py`, `barbarian/__init__.py`, `test_beast.py`, `TurnResources`, `test_champion.py`, `begin_turn`, `_RngSi`, `_atacado`, `_ejecuta`, `apply_fighter`, `apply_cavalier`, `_fighter`, `psionic_dice_count`, `test_death.py`, `_pj`, `test_enlarge.py`, `test_proficiency.py`, `consumir_marcas`, `test_extra_damage.py`, `_ExplotaSiUsaRng`, `_pj`, `ActionType`, `PlayerCharacter`, `test_storm_herald.py`, `inflict_damage`, `_carga`, `test_azer.py`, `test_zealot.py`, `test_sustituir_ataque.py`, `test_psi_warrior.py`, `dnd_sim/__init__.py`, `_pj`, `attack_roll`, `_abilities`, `test_pack_tactics.py`, `_RngSi`, `test_undead_fortitude.py`, `test_spells.py`, `test_superior_invisibility.py`, `test_cavalier.py`, `Combatant`, `test_fighter.py`, `_RngExplota`, `_duelo`, `ConditionEffect`, `maestria_de`, `test_sustitucion_hace_un_solo_par_de_picks`, `test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `daño_base_arma()`) actually correct?**
  _`Attack` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_world_tree.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10213032581453634 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_world_tree.py`, `intentar_desenganche`, `AttackRange`, `Combatant`, `_de`, `test_wild_heart.py`, `test_rune_knight.py`, `LegendaryState`, `RuneKnightFeatures`, `parse_spell`, `test_legendary.py`, `test_giant.py`, `test_utility.py`, `legendary_parser.py`, `test_eldritch_knight.py`, `test_battle_master.py`, `test_samurai.py`, `combat/attack.py`, `ActionUsage`, `test_parry.py`, `test_attach.py`, `Monster`, `ability_check`, `test_lair.py`, `traits/__init__.py`, `test_arcane_archer.py`, `test_skills.py`, `test_hechizos_pj.py`, `test_magic_resistance.py`, `test_mastery.py`, `BarbarianFeatures`, `apply_condition`, `saving_throw`, `TelekineticMasterAction`, `BattleMasterFeatures`, `RollMode`, `test_checks_escapes.py`, `test_beast.py`, `test_condition_immunities.py`, `test_champion.py`, `pick`, `_ejecuta`, `psionic_dice_count`, `ConditionTracker`, `_pj`, `test_enlarge.py`, `IntimidatingPresenceAction`, `.can_act`, `consumir_marcas`, `PsiWarriorFeatures`, `_pj`, `ActionType`, `PlayerCharacter`, `test_storm_herald.py`, `_carga`, `test_psi_warrior.py`, `dnd_sim/__init__.py`, `Attack`, `_abilities`, `test_pack_tactics.py`, `condition_parser.py`, `test_spells.py`, `test_superior_invisibility.py`, `test_cavalier.py`, `_guardado`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Are the 168 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 168 INFERRED edges - model-reasoned connections that need verification._
- **Should `AttackRange` be split into smaller, more focused modules?**
  _Cohesion score 0.1363265306122449 - nodes in this community are weakly interconnected._
- **Why does `attack_roll()` connect `attack_roll` to `Combatant`, `test_wild_heart.py`, `test_rune_knight.py`, `_duelo`, `ConditionEffect`, `test_legendary.py`, `test_giant.py`, `parse_spell`, `run_combat`, `test_battle_master.py`, `test_samurai.py`, `combat/attack.py`, `test_parry.py`, `test_attach.py`, `test_ancestral_guardian.py`, `load_monster`, `_clamp`, `test_arcane_archer.py`, `test_magic_resistance.py`, `test_mastery.py`, `apply_condition`, `saving_throw`, `TelekineticMasterAction`, `Condition`, `BattleMasterFeatures`, `RollMode`, `test_checks_escapes.py`, `test_beast.py`, `test_champion.py`, `pick`, `apply_fighter`, `test_death.py`, `_pj`, `test_enlarge.py`, `.can_act`, `consumir_marcas`, `test_extra_damage.py`, `_pj`, `ActionType`, `PlayerCharacter`, `inflict_damage`, `test_azer.py`, `test_zealot.py`, `test_sustituir_ataque.py`, `dnd_sim/__init__.py`, `Attack`, `_pj`, `_abilities`, `test_spells.py`, `test_superior_invisibility.py`, `test_cavalier.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
# Graph Report - DnDBalancer  (2026-11-09)

## Corpus Check
- 225 files · ~195,559 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 3720 nodes · 13481 edges · 112 communities (96 shown, 16 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 865 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `77ca9b04`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- _fighter
- test_attach.py
- AttackRange
- test_giant.py
- test_world_tree.py
- test_wild_heart.py
- ability_check
- test_legendary.py
- test_beast.py
- test_spells.py
- RollMode
- _arquero
- test_utility.py
- test_wild_magic.py
- Trait
- spell_parser.py
- parse_damage_type
- test_battle_master.py
- _atacado
- test_loader_actions.py
- combatant.py
- ArcaneArcherFeatures
- ActionUsage
- apply_barbarian
- test_martial_advantage.py
- ZealotFeatures
- test_zealot.py
- TurnResources
- Monster
- load_monster
- attack_roll
- test_superior_invisibility.py
- FighterFeatures
- BeastFeatures
- test_skills.py
- test_undead_fortitude.py
- test_arcane_archer.py
- test_multiattack.py
- MultiattackAction
- inflict_damage
- test_mastery.py
- BarbarianFeatures
- apply_condition
- pick
- test_area.py
- random
- Condition
- BattleMasterFeatures
- _decide
- main.py
- test_checks_escapes.py
- PlayerCharacter
- _trait
- Any
- test_condition_immunities.py
- combat/attack.py
- run_combat
- test_magic_resistance.py
- begin_turn
- loader.py
- traits/__init__.py
- legendary_parser.py
- test_storm_herald.py
- saving_throw
- test_backgrounds.py
- _pj
- Attack
- WorldTreeFeatures
- BerserkerFeatures
- Regeneration
- test_pack_tactics.py
- test_lair.py
- ConditionTracker
- json
- test_races.py
- test_enlarge.py
- _pj
- conditions.py
- _RngBajo
- Combatant
- dnd_sim/__init__.py
- apply_damage_modifiers
- TODO — DnDBalancer / dnd_sim
- _RngMax
- test_azer.py
- WarriorHealAction
- test_extra_damage.py
- test_sustituir_ataque.py
- _RngSi
- damage.py
- test_ancestral_guardian.py
- normalize_skill
- lair_loader.py
- _RngSi
- _clamp
- parse_traits
- SaveResult
- ZealousPresenceAction
- _RngExplota
- test_el_gancho_after_failed_check_desde_ability_check_con_ctx
- Arquitectura de `dnd_sim`
- resolve_save_damage
- CombatState
- D20Result
- _RngNo
- _atacado_dos_enemigos

## God Nodes (most connected - your core abstractions)
1. `Attack` - 222 edges
2. `Condition` - 181 edges
3. `Monster` - 170 edges
4. `AttackRange` - 167 edges
5. `apply_condition()` - 154 edges
6. `Abilities` - 151 edges
7. `attack_roll()` - 146 edges
8. `load_monster()` - 136 edges
9. `PlayerCharacter` - 134 edges
10. `pick()` - 100 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Fighter: cómo añadir una subclase` --references--> `SubclassDef`  [INFERRED]
  TODO.md → dnd_sim/rules/classes/base.py
- `Battle Master: plan de sesión 1` --references--> `CombatState`  [INFERRED]
  TODO.md → dnd_sim/core/combat_state.py

## Import Cycles
- None detected.

## Communities (112 total, 16 thin omitted)

### Community 0 - "_fighter"
Cohesion: 0.09
Nodes (27): second_wind_uses(), _action_surge(), _ctx_recursos(), _fighter(), _save_fallada(), _saving_nueva(), _second_wind(), test_action_surge_como_maximo_un_vez_por_turno() (+19 more)

### Community 1 - "test_attach.py"
Cohesion: 0.07
Nodes (37): Cómo comprobar que todo sigue en orden, parse_attach_effects(), AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), _capa() (+29 more)

### Community 2 - "AttackRange"
Cohesion: 0.10
Nodes (52): AttackRange, RageAction, apply_berserker(), _golpe_sin_armas(), IntimidatingPresenceAction, _abilities(), _barbaro(), _berserker() (+44 more)

### Community 3 - "test_giant.py"
Cohesion: 0.07
Nodes (37): apply_giant(), _de(), GiantFeatures, MightyImpelAction, _objetivos_impel(), _orden_de(), _abilities(), _barbaro() (+29 more)

### Community 4 - "test_world_tree.py"
Cohesion: 0.12
Nodes (37): _abilities(), _aliado(), _barbaro(), _ctx(), _decision(), _elige_candidato(), espia(), _furia() (+29 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.08
Nodes (48): apply_wild_heart(), _con_beneficio(), _de(), _en_5_pies(), _hostil(), _orden_de(), WildHeartFeatures, _abilities() (+40 more)

### Community 6 - "ability_check"
Cohesion: 0.09
Nodes (28): ability_check(), ability_check_bonus(), _avisar_fallo_prueba(), CheckResult, _finish_check(), _guia(), _resolve_mods(), skill_check() (+20 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.07
Nodes (59): simulate(), legendary_phase(), _contexto(), _data(), _estado(), _legendaria(), _load(), _pj() (+51 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (65): WeaponAttackAction, _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll(), spy() (+57 more)

### Community 9 - "test_spells.py"
Cohesion: 0.08
Nodes (49): Paquetes con fachada, parse_spell(), parse_spellcasting(), spell_action(), Spellcasting, _ctx(), _npc(), _pj() (+41 more)

### Community 10 - "RollMode"
Cohesion: 0.09
Nodes (28): RollMode, BloodFrenzy, _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _RasgoDeSalvacion (+20 more)

### Community 11 - "_arquero"
Cohesion: 0.12
Nodes (27): _arco(), _arquero(), _ctx_curving(), _curving(), _RngExplota, test_accion_curving_se_anade_desde_el_nivel_7(), test_arcane_shot_crea_usos_por_nivel(), test_arcane_shot_se_reinicia_en_on_turn_start() (+19 more)

### Community 12 - "test_utility.py"
Cohesion: 0.13
Nodes (29): ConditionInstance, _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), _orden_tamano(), _abilities(), _ctx() (+21 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.13
Nodes (38): _abilities(), _barbaro(), _con_cola(), _con_efecto(), espia(), _ctx(), _furia(), _mon() (+30 more)

### Community 15 - "spell_parser.py"
Cohesion: 0.06
Nodes (22): _avisar(), build_spell_actions(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla() (+14 more)

### Community 17 - "test_battle_master.py"
Cohesion: 0.13
Nodes (22): apply_battle_master(), _bm(), _firmas(), _pj(), test_apply_battle_master_exige_la_clase_fighter(), test_apply_battle_master_requiere_nivel_3(), test_apply_class_equivalente_a_apply_battle_master(), test_know_your_enemy_es_un_dato_desde_el_nivel_7() (+14 more)

### Community 18 - "_atacado"
Cohesion: 0.15
Nodes (22): consumir_marcas(), _abilities(), _atacado(), _ejecuta(), _mods(), _RngFalla, test_disarming_attack_no_altera_el_combate_mas_que_el_dano(), test_distracting_da_ventaja_a_un_tercero_y_se_consume() (+14 more)

### Community 19 - "test_loader_actions.py"
Cohesion: 0.17
Nodes (14): _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga(), test_ataque_con_usage_conserva_el_actionusage() (+6 more)

### Community 20 - "combatant.py"
Cohesion: 0.09
Nodes (11): _objetivo_enganche(), valid_targets(), _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de() (+3 more)

### Community 21 - "ArcaneArcherFeatures"
Cohesion: 0.08
Nodes (5): ArcaneArcherFeatures, _ctx_con_rng(), _CtxConRng, _de(), _otros_enemigos()

### Community 22 - "ActionUsage"
Cohesion: 0.08
Nodes (25): ActionUsage, UsageKind, _breath(), _eventos(), _FixedRandom, _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos() (+17 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.09
Nodes (51): rage_uses(), apply_barbarian(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj(), _resultado() (+43 more)

### Community 24 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 25 - "ZealotFeatures"
Cohesion: 0.08
Nodes (10): _de(), _en_60_pies(), _es_aliado(), _furia_de(), ZealotFeatures, test_apply_class_por_clave_aplica_zealot(), test_clave_de_registro_zealot_en_barbarian(), test_revivificacion_sin_usos_de_furia_no_activa() (+2 more)

### Community 26 - "test_zealot.py"
Cohesion: 0.12
Nodes (33): _abilities(), _aliado(), _barbaro(), _decision(), _fallos(), _forma(), _guarda_con(), _presencia() (+25 more)

### Community 27 - "TurnResources"
Cohesion: 0.09
Nodes (22): ActionType, TurnResources, Spell, _contexto_de_reaccion(), trigger_reaction(), _BonusQueAnota, _ctx(), _npc() (+14 more)

### Community 28 - "Monster"
Cohesion: 0.11
Nodes (28): Monster, _abilities(), _disparo(), _RngFalla, test_banishing_arrow_falla_la_salvacion_y_deja_incapacitado(), test_banishing_arrow_salvacion_exitosa_no_aplica_condicion(), test_beguiling_arrow_hechiza_y_termina_si_el_aliado_ataca(), test_beguiling_sin_aliados_no_tira_salvacion() (+20 more)

### Community 29 - "load_monster"
Cohesion: 0.10
Nodes (26): load_monster(), _tag_modificadores(), AttackAction, apply_beast(), _habilitar_armas_naturales(), _ctx(), _pj(), _spell_data() (+18 more)

### Community 30 - "attack_roll"
Cohesion: 0.30
Nodes (19): attack_roll(), _ataque(), _ctx(), _datos(), _fijar_d20(), _gladiador(), _pj(), test_el_gladiador_carga_su_parry_desde_las_reacciones() (+11 more)

### Community 31 - "test_superior_invisibility.py"
Cohesion: 0.30
Nodes (12): remove_invisibility_on_action(), _accion(), _ctx(), _pixie(), _pj(), test_atacar_con_ventaja_y_no_pierde_la_invisibilidad(), test_ejecutarla_aplica_el_estado(), test_el_monstruo_recibe_su_accion_al_construirse() (+4 more)

### Community 32 - "FighterFeatures"
Cohesion: 0.09
Nodes (5): ActionSurgeAction, _contexto(), _en_5_pies(), FighterFeatures, _rasgo()

### Community 34 - "test_skills.py"
Cohesion: 0.07
Nodes (32): skill_ability(), has_escape_text(), parse_escape(), _skills_for(), skill_bonus(), check_modifiers(), test_los_flags_de_prueba_son_por_caracteristica(), _abilities() (+24 more)

### Community 35 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 36 - "test_arcane_archer.py"
Cohesion: 0.13
Nodes (20): arcane_shot_options_known(), apply_arcane_archer(), CurvingShotAction, _firmas(), _pj(), test_apply_arcane_archer_exige_la_clase_fighter(), test_apply_class_equivalente_a_apply_arcane_archer(), test_arcane_archer_lore_da_competencia() (+12 more)

### Community 37 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 38 - "MultiattackAction"
Cohesion: 0.16
Nodes (3): _en_accion_de_ataque(), _living_enemies(), MultiattackAction

### Community 39 - "inflict_damage"
Cohesion: 0.24
Nodes (14): inflict_damage(), test_inflict_damage_registra_la_bandera_magical(), _ctx(), _datos(), _jabali(), _pj(), test_el_jabali_carga_su_relentless_con_umbral_y_uso(), test_relentless_no_necesita_contexto_ni_rng() (+6 more)

### Community 40 - "test_mastery.py"
Cohesion: 0.10
Nodes (28): al_acertar(), al_fallar(), _cd_topple(), _log(), _nombre(), resolver_maestria(), _arma(), _atacante() (+20 more)

### Community 41 - "BarbarianFeatures"
Cohesion: 0.10
Nodes (5): BarbarianFeatures, _contexto(), _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 42 - "apply_condition"
Cohesion: 0.07
Nodes (60): Abilities, _apply_condition_riders(), apply_condition(), end_turn(), RepeatSave, _ataque(), _ctx(), _data() (+52 more)

### Community 43 - "pick"
Cohesion: 0.06
Nodes (11): rage_damage(), roll_dice(), DamageType, log_line(), proficiency_bonus(), pick(), sample(), FormOfTheBeast (+3 more)

### Community 44 - "test_area.py"
Cohesion: 0.12
Nodes (26): AreaTargeting, select_area_targets(), _default_targeting(), _area_action(), _ctx(), _npc(), _pj(), _save_forzado() (+18 more)

### Community 45 - "random"
Cohesion: 0.07
Nodes (54): apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), SpikedArmorAction, AttackModifiers, _abilities(), _accion_puas() (+46 more)

### Community 46 - "Condition"
Cohesion: 0.14
Nodes (30): Condition, attack_modifiers(), _condiciones(), _hooks(), _instancias(), test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque() (+22 more)

### Community 47 - "BattleMasterFeatures"
Cohesion: 0.11
Nodes (4): BattleMasterFeatures, _de(), FeintingAttackAction, _orden_tamano()

### Community 48 - "_decide"
Cohesion: 0.13
Nodes (19): _conoce_sweeping(), _decide(), _ExplotaSiUsaRng, _RngIdx, test_el_uso_no_se_gasta_si_no_se_ejecuta(), test_en_un_fallo_sin_precision_cero_rng(), test_feinting_sin_impacto_no_gasta_el_dado(), test_la_decision_es_un_solo_par_de_picks() (+11 more)

### Community 49 - "main.py"
Cohesion: 0.11
Nodes (22): CLI del simulador: `build_parser()`, Detalle por flag, Ejemplos, Flujo de `main()`, `--legendary-p`, `--legendary-points`, `--monster` / `-m`, Observaciones (para humanos y IA) (+14 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.07
Nodes (46): EscapeCheck, resolve_attack_range(), _ataque(), _check_fijo(), _fake(), _ctx(), _data(), _duelo() (+38 more)

### Community 51 - "PlayerCharacter"
Cohesion: 0.12
Nodes (14): _armor_class_value(), PlayerCharacter, test_attack_roll_log_modifier(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper() (+6 more)

### Community 52 - "_trait"
Cohesion: 0.14
Nodes (32): ability_mod(), _aliado(), _check_fallada(), _con_estilo(), _ctx(), _enemigo(), _mods(), _RngSi (+24 more)

### Community 53 - "Any"
Cohesion: 0.06
Nodes (16): apply_wild_magic(), _bolstering(), _cd(), _de(), _en_30_pies(), _enemigos(), _espiritu(), _flores() (+8 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.12
Nodes (16): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+8 more)

### Community 57 - "combat/attack.py"
Cohesion: 0.09
Nodes (15): _actualizar_distancia(), _agrandado(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), daño_base_arma(), _decidir_maniobra() (+7 more)

### Community 59 - "run_combat"
Cohesion: 0.10
Nodes (17): d20(), roll_d20(), combat_finished(), living_teams(), CombatResult, _invoke_policy(), roll_initiative(), run_combat() (+9 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.12
Nodes (24): _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab(), test_condition_action_de_hechizo_pasa_magical() (+16 more)

### Community 61 - "begin_turn"
Cohesion: 0.30
Nodes (14): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+6 more)

### Community 62 - "loader.py"
Cohesion: 0.06
Nodes (19): parse_range_type(), _resistencia_legendaria(), _damage_type(), _extract_multiattack_alternatives(), _norm_name(), _parse_condition_immunities(), _parse_damage_modifiers(), extract_multiattack_alternatives() (+11 more)

### Community 63 - "traits/__init__.py"
Cohesion: 0.05
Nodes (12): DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante(), aliados_capaces(), _condicion_posicional() (+4 more)

### Community 64 - "legendary_parser.py"
Cohesion: 0.06
Nodes (18): normalize_ability(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), _coincide_nombre(), _con_nombre_limpio() (+10 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.06
Nodes (46): _aliados_en_aura(), apply_storm_herald(), _cd(), _dado_mar(), _de(), _en_aura(), _enemigos_en_aura(), _escalado() (+38 more)

### Community 66 - "saving_throw"
Cohesion: 0.11
Nodes (17): save_modifiers(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save(), _resolve_mode_str(), SaveDamageOutcome, saving_throw() (+9 more)

### Community 67 - "test_backgrounds.py"
Cohesion: 0.16
Nodes (17): Background, load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes(), test_apply_background_sin_competencias_es_inofensivo() (+9 more)

### Community 68 - "_pj"
Cohesion: 0.22
Nodes (19): espia(), _espiar_divine(), _furia(), _mon(), _pj(), test_determinismo_misma_semilla_mismos_resultados(), corrida(), test_divine_fury_elige_radiante_con_pick() (+11 more)

### Community 69 - "Attack"
Cohesion: 0.10
Nodes (42): Attack, apply_fighter(), maestria_de(), test_alma_bestial_flag_magical_existe(), _abilities(), _firmas(), _objetivo(), _pj() (+34 more)

### Community 70 - "WorldTreeFeatures"
Cohesion: 0.24
Nodes (4): apply_world_tree(), _de(), WorldTreeFeatures, test_apply_anade_trait_sin_accion_propia()

### Community 71 - "BerserkerFeatures"
Cohesion: 0.15
Nodes (4): _armas_melee_de(), BerserkerFeatures, _de(), _furia_de()

### Community 72 - "Regeneration"
Cohesion: 0.14
Nodes (4): _mark_dead_if_down(), _es_radiante(), _guardar_salvacion(), Regeneration

### Community 73 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 74 - "test_lair.py"
Cohesion: 0.10
Nodes (20): lair_phase(), LairAction, LegendaryState, _ctx(), _enemigo(), lairs_dir(), _Stub, test_dos_acciones_uniformes() (+12 more)

### Community 76 - "json"
Cohesion: 0.15
Nodes (9): _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError (+1 more)

### Community 77 - "test_races.py"
Cohesion: 0.13
Nodes (23): Race, load_race(), parse_race(), _abilities(), _fiendish_legacy(), _keen_senses(), _pj(), test_apply_race_añade_competencias_fijas() (+15 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.14
Nodes (25): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+17 more)

### Community 79 - "_pj"
Cohesion: 0.18
Nodes (14): _dragon(), _orden_con(), _pj(), _spy_turnos(), spy(), test_guarida_pasa_magical_a_las_salvaciones(), test_puntos_siempre_incluyen_bonus_de_guarida(), test_reproducibilidad_con_guarida() (+6 more)

### Community 80 - "conditions.py"
Cohesion: 0.21
Nodes (7): _as_condition(), attempt_escapes(), _condicion_bloqueada(), _contar(), _label(), _queda_accion(), remove_condition()

### Community 82 - "Combatant"
Cohesion: 0.09
Nodes (5): Combatant, _aliados_heridos(), _cd_ataque(), _en_10_pies(), _es_aliado()

### Community 83 - "dnd_sim/__init__.py"
Cohesion: 0.04
Nodes (36): is_area_action(), _por_datos(), build_condition_action(), build_save_action(), build_save_effect(), damage_dice_of(), damage_options(), damage_type_of() (+28 more)

### Community 84 - "apply_damage_modifiers"
Cohesion: 0.12
Nodes (19): apply_damage_modifiers(), _is_petrified(), _guerrero_y_ogro(), _target(), test_danio_medio_por_combatiente_y_equipo(), test_etiqueta_de_modificadores_se_deriva_del_dano_final(), test_immune_target_takes_zero_damage(), test_immunity_zero() (+11 more)

### Community 85 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.15
Nodes (11): Arcane Archer (XGE), test_ever_ready_shot_no_cambia_los_usos_al_empezar_un_combate(), Arcane Archer: Piercing y Seeking, Battle Master: sesión 2 (pendiente), Fighter: cómo añadir una subclase, Fighter: pendientes reales, Grafo y verificación, Pendientes generales (+3 more)

### Community 87 - "test_azer.py"
Cohesion: 0.26
Nodes (17): _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), _rasgo(), test_ataque_a_distancia_no_dispara_la_represalia() (+9 more)

### Community 88 - "WarriorHealAction"
Cohesion: 0.25
Nodes (15): WarriorHealAction, _accion(), _ctx(), test_fanatical_no_activo_sin_furia(), test_nivel_3_no_recibe_rasgos_superiores(), test_warrior_curacion_gasta_un_dado_y_suma_pv(), test_warrior_curacion_no_supera_el_maximo(), test_warrior_de_los_dioses_reserva_por_nivel() (+7 more)

### Community 89 - "test_extra_damage.py"
Cohesion: 0.17
Nodes (18): DamageRecorder, _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional() (+10 more)

### Community 90 - "test_sustituir_ataque.py"
Cohesion: 0.16
Nodes (11): _sustituir_ataque(), AtaqueSustituido, _abilities(), _blanco(), _pj(), _RasgoQueSustituye, _RasgoSinSustitucion, _RngExplota (+3 more)

### Community 91 - "_RngSi"
Cohesion: 0.12
Nodes (10): _accion_feinting(), _RngNo, _RngSi, test_feinting_encola_la_ventaja_y_el_dado_si_impacta(), test_feinting_es_elegible_con_bonus_libre_y_decision_aleatoria(), test_feinting_sin_datos_es_inelegible_sin_rng(), test_goading_attack_no_marca_si_pasa_la_salvacion(), test_precision_con_relevelless_no_gasta_el_dado() (+2 more)

### Community 92 - "damage.py"
Cohesion: 0.17
Nodes (7): _absorber_pv_temporales(), _hooks(), _mitigacion_de_otros(), _notify_damage_dealt(), _notify_damage_taken(), _salvar_a_cero(), hooks()

### Community 93 - "test_ancestral_guardian.py"
Cohesion: 0.06
Nodes (46): AncestralGuardianFeatures, apply_ancestral_guardian(), apply_class(), ClassDef, normalize_class_name(), register_class(), SubclassDef, _abilities() (+38 more)

### Community 94 - "normalize_skill"
Cohesion: 0.10
Nodes (7): normalize_tool(), _clean(), normalize_skill(), _add(), _skill_name(), _spells_from_description(), _trait_skills()

### Community 95 - "lair_loader.py"
Cohesion: 0.24
Nodes (5): _check_fields(), _construir(), _error(), load_lair(), ConditionEffect

### Community 96 - "_RngSi"
Cohesion: 0.12
Nodes (11): _RngSi, test_arcane_shot_se_aplica_una_sola_vez_por_turno(), test_arcane_shot_se_gasta_un_uso_al_aplicar(), test_daño_de_arcane_shot_es_2d6_antes_del_18(), _dado(), test_daño_de_arcane_shot_es_4d6_desde_el_18(), test_decision_de_impacto_no_gasta_el_uso_hasta_impactar(), test_piercing_gasta_el_uso_al_sustituir() (+3 more)

### Community 97 - "_clamp"
Cohesion: 0.07
Nodes (20): action_surge_uses(), arcane_shot_uses(), _clamp(), extra_attacks_for(), fighter_extra_attacks_for(), indomitable_uses(), maneuvers_known_count(), superiority_dice_count() (+12 more)

### Community 98 - "parse_traits"
Cohesion: 0.18
Nodes (8): _entradas(), parse_traits(), _arquero_parry(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd(), test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad(), test_el_umbral_se_saca_de_cada_descripcion(), test_el_rasgo_se_parsea_desde_el_srd(), test_parse_traits_ignora_entradas_malformadas()

### Community 99 - "SaveResult"
Cohesion: 0.25
Nodes (11): SaveResult, fake_saving_throw(), falla(), espia(), stub(), stub(), stub(), test_after_failed_save_sin_zealot_devuelve_el_mismo_resultado() (+3 more)

### Community 100 - "ZealousPresenceAction"
Cohesion: 0.25
Nodes (5): apply_zealot(), _reserva_dados(), ZealousPresenceAction, test_apply_anade_trait_y_dos_acciones_bonus(), test_apply_requiere_clase_barbara()

### Community 101 - "_RngExplota"
Cohesion: 0.29
Nodes (3): _RngExplota, test_resolver_maestria_sin_maestria_no_consulta_tactical_master(), test_tactical_master_no_sustituye_bajo_el_nivel_9()

### Community 103 - "Arquitectura de `dnd_sim`"
Cohesion: 0.29
Nodes (6): Arquitectura de `dnd_sim`, Carpetas, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia

### Community 104 - "resolve_save_damage"
Cohesion: 0.22
Nodes (6): _log_target(), _mode_tag(), _outcome_tag(), _reaccion_si_procede(), resolve_save_damage(), _log_line_outcome()

### Community 106 - "D20Result"
Cohesion: 0.40
Nodes (5): D20Result, test_el_motor_decide_y_gasta_el_dado_en_el_ataque(), test_precision_actua_en_el_motor_tras_un_fallo(), espia(), espia()

## Knowledge Gaps
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `_fighter`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `ability_check`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `RollMode`, `_arquero`, `test_utility.py`, `test_wild_magic.py`, `parse_damage_type`, `test_battle_master.py`, `_atacado`, `combatant.py`, `apply_barbarian`, `test_zealot.py`, `TurnResources`, `Monster`, `load_monster`, `attack_roll`, `test_superior_invisibility.py`, `test_undead_fortitude.py`, `test_arcane_archer.py`, `inflict_damage`, `test_mastery.py`, `apply_condition`, `pick`, `random`, `Condition`, `_decide`, `main.py`, `test_checks_escapes.py`, `PlayerCharacter`, `combat/attack.py`, `test_magic_resistance.py`, `begin_turn`, `loader.py`, `legendary_parser.py`, `test_storm_herald.py`, `_pj`, `test_pack_tactics.py`, `test_enlarge.py`, `Combatant`, `dnd_sim/__init__.py`, `apply_damage_modifiers`, `test_azer.py`, `test_extra_damage.py`, `test_sustituir_ataque.py`, `_RngSi`, `test_ancestral_guardian.py`, `lair_loader.py`, `_RngSi`, `parse_traits`, `_RngExplota`, `D20Result`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `daño_base_arma()`) actually correct?**
  _`Attack` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `_fighter` be split into smaller, more focused modules?**
  _Cohesion score 0.09090909090909091 - nodes in this community are weakly interconnected._
- **Why does `Trait` connect `Trait` to `test_attach.py`, `test_giant.py`, `test_wild_heart.py`, `test_spells.py`, `RollMode`, `ArcaneArcherFeatures`, `ZealotFeatures`, `FighterFeatures`, `BeastFeatures`, `BarbarianFeatures`, `pick`, `random`, `BattleMasterFeatures`, `Any`, `test_condition_immunities.py`, `loader.py`, `traits/__init__.py`, `test_storm_herald.py`, `WorldTreeFeatures`, `BerserkerFeatures`, `Regeneration`, `dnd_sim/__init__.py`, `test_sustituir_ataque.py`, `test_ancestral_guardian.py`, `parse_traits`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 118 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 118 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06944444444444445 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `ability_check`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `RollMode`, `test_utility.py`, `spell_parser.py`, `test_battle_master.py`, `_atacado`, `combatant.py`, `ArcaneArcherFeatures`, `Monster`, `attack_roll`, `test_superior_invisibility.py`, `test_skills.py`, `test_arcane_archer.py`, `test_mastery.py`, `BarbarianFeatures`, `apply_condition`, `pick`, `BattleMasterFeatures`, `test_checks_escapes.py`, `test_condition_immunities.py`, `combat/attack.py`, `test_magic_resistance.py`, `loader.py`, `traits/__init__.py`, `legendary_parser.py`, `test_storm_herald.py`, `saving_throw`, `WorldTreeFeatures`, `BerserkerFeatures`, `test_pack_tactics.py`, `test_lair.py`, `ConditionTracker`, `test_enlarge.py`, `conditions.py`, `Combatant`, `dnd_sim/__init__.py`, `apply_damage_modifiers`, `damage.py`, `normalize_skill`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
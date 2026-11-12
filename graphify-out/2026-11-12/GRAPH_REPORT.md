# Graph Report - DnDBalancer  (2026-11-11)

## Corpus Check
- 227 files · ~216,153 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 3994 nodes · 14584 edges · 143 communities (101 shown, 42 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 1004 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8af6f297`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- _trait
- test_attach.py
- AttackRange
- test_giant.py
- test_world_tree.py
- test_wild_heart.py
- test_proficiency.py
- test_legendary.py
- test_beast.py
- parse_spell
- test_traits.py
- _arquero
- test_utility.py
- test_wild_magic.py
- _avisar
- _ctx
- apply_battle_master
- consumir_marcas
- test_loader_actions.py
- BeastFeatures
- ArcaneArcherFeatures
- ActionUsage
- apply_barbarian
- test_martial_advantage.py
- Any
- test_zealot.py
- test_death.py
- Monster
- test_magical.py
- test_parry.py
- test_superior_invisibility.py
- FighterFeatures
- _ExplotaSiUsaRng
- test_skills.py
- test_undead_fortitude.py
- test_arcane_archer.py
- test_multiattack.py
- encounter.py
- inflict_damage
- test_mastery.py
- BarbarianFeatures
- apply_condition
- pick
- test_area.py
- TurnResources
- Condition
- BattleMasterFeatures
- test_battle_master.py
- main.py
- test_checks_escapes.py
- load_monster
- _con_estilo
- _enemigos
- test_condition_immunities.py
- hooks
- apply_class
- test_magic_resistance.py
- begin_turn
- .alive
- traits/__init__.py
- loader.py
- test_storm_herald.py
- save_modifiers
- test_backgrounds.py
- _mon
- test_fighter.py
- apply_cavalier
- LegendaryState
- GiantFeatures
- test_pack_tactics.py
- test_lair.py
- ConditionTracker
- json
- test_races.py
- test_enlarge.py
- parse_spellcasting
- Any
- run_combat
- .on_turn_start
- dnd_sim/__init__.py
- PlayerCharacter
- test_spells.py
- _RngMax
- test_azer.py
- test_cavalier.py
- test_extra_damage.py
- AtaqueSustituido
- _carga
- _mark_dead_if_down
- test_ancestral_guardian.py
- _bajo_ataque
- SaveDamage
- _abilities
- _clamp
- parse_traits
- _decision
- barbarian/__init__.py
- _RngSi
- test_el_gancho_after_failed_check_desde_ability_check_con_ctx
- Combatant
- Any
- TODO — DnDBalancer / dnd_sim
- Attack
- _especial
- parse_escape
- roll_initiative
- apply_beast
- load_lair
- test_apply_class_equivalente_a_apply_cavalier
- AttachOnHitEffect
- _RngBajo
- _RngNo
- test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque
- test_sustitucion_hace_un_solo_par_de_picks

## God Nodes (most connected - your core abstractions)
1. `Attack` - 250 edges
2. `Monster` - 197 edges
3. `Condition` - 189 edges
4. `AttackRange` - 186 edges
5. `attack_roll()` - 181 edges
6. `apply_condition()` - 158 edges
7. `Abilities` - 153 edges
8. `load_monster()` - 136 edges
9. `PlayerCharacter` - 136 edges
10. `pick()` - 116 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Battle Master: plan de sesión 1` --references--> `superiority_dice_count()`  [INFERRED]
  TODO.md → dnd_sim/core/classes.py
- `Battle Master: plan de sesión 1` --references--> `superiority_die_sides()`  [INFERRED]
  TODO.md → dnd_sim/core/classes.py
- `Battle Master: plan de sesión 1` --references--> `maneuvers_known_count()`  [INFERRED]
  TODO.md → dnd_sim/core/classes.py

## Import Cycles
- None detected.

## Communities (143 total, 42 thin omitted)

### Community 0 - "_trait"
Cohesion: 0.11
Nodes (28): second_wind_uses(), _action_surge(), _check_fallada(), _ctx_recursos(), _fighter(), _second_wind(), test_action_surge_como_maximo_un_vez_por_turno(), test_action_surge_ejecutada_restaura_la_accion_y_gasta_un_uso() (+20 more)

### Community 1 - "test_attach.py"
Cohesion: 0.15
Nodes (28): desenganchar(), enganchador_de(), intentar_desenganche(), _atacar(), _bite(), _cloaker(), _ctx(), _datos() (+20 more)

### Community 2 - "AttackRange"
Cohesion: 0.07
Nodes (57): AttackRange, RageAction, apply_berserker(), _armas_melee_de(), BerserkerFeatures, _de(), _furia_de(), _golpe_sin_armas() (+49 more)

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
Cohesion: 0.20
Nodes (19): _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia(), test_level_manda_sobre_el_proficiency_explicito() (+11 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.05
Nodes (67): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), legendary_phase(), legendary_resistance() (+59 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (66): WeaponAttackAction, _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll(), spy() (+58 more)

### Community 9 - "parse_spell"
Cohesion: 0.08
Nodes (31): _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), parse_spell(), _slot_table(), _tabla_cantrip(), _tipo_de_dano(), _spell_data() (+23 more)

### Community 10 - "test_traits.py"
Cohesion: 0.08
Nodes (28): resolve_roll_mode(), attack_modifiers(), BloodFrenzy, _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba (+20 more)

### Community 11 - "_arquero"
Cohesion: 0.12
Nodes (27): _arco(), _arquero(), _ctx_curving(), _curving(), _RngExplota, test_accion_curving_se_anade_desde_el_nivel_7(), test_arcane_shot_crea_usos_por_nivel(), test_arcane_shot_se_reinicia_en_on_turn_start() (+19 more)

### Community 12 - "test_utility.py"
Cohesion: 0.13
Nodes (29): _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), hay_utilitaria_accion(), _orden_tamano(), _abilities(), _ctx() (+21 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.06
Nodes (54): _log_target(), apply_wild_magic(), _de(), _sombra(), WildMagicFeatures, WildSurgeAction, _mode_tag(), _outcome_tag() (+46 more)

### Community 15 - "_avisar"
Cohesion: 0.40
Nodes (3): _avisar(), _extender_tabla(), _sumar_dados()

### Community 16 - "_ctx"
Cohesion: 0.22
Nodes (16): _ctx(), _mods(), _objetivo(), _save_fallada(), _saving_nueva(), test_ataques_estudiados_caduca_al_final_del_siguiente_turno(), test_ataques_estudiados_da_ventaja_contra_el_objetivo_tras_un_fallo(), test_ataques_estudiados_es_por_objetivo() (+8 more)

### Community 17 - "apply_battle_master"
Cohesion: 0.07
Nodes (29): maneuvers_known_count(), superiority_dice_count(), superiority_die_sides(), apply_battle_master(), BattleMasterRallyAction, _atacado_fijo(), _completa(), _firmas() (+21 more)

### Community 18 - "consumir_marcas"
Cohesion: 0.10
Nodes (24): _reaccionar_al_fallo(), _reducir_dano_recibido(), consumir_marcas(), _abilities(), _ejecuta(), _mods(), _RngFalla, test_disarming_attack_no_altera_el_combate_mas_que_el_dano() (+16 more)

### Community 19 - "test_loader_actions.py"
Cohesion: 0.19
Nodes (11): _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga(), test_ataque_con_usage_conserva_el_actionusage() (+3 more)

### Community 21 - "ArcaneArcherFeatures"
Cohesion: 0.09
Nodes (6): ArcaneArcherFeatures, _ctx_con_rng(), _CtxConRng, CurvingShotAction, _de(), _otros_enemigos()

### Community 22 - "ActionUsage"
Cohesion: 0.10
Nodes (17): _usage(), parse_usage(), UnknownUsageError, _warn(), ActionUsage, UsageKind, test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa() (+9 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.08
Nodes (52): rage_uses(), apply_barbarian(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj(), _resultado() (+44 more)

### Community 24 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 25 - "Any"
Cohesion: 0.12
Nodes (3): _de(), _en_60_pies(), _es_aliado()

### Community 26 - "test_zealot.py"
Cohesion: 0.11
Nodes (45): _abilities(), _accion(), _aliado(), _barbaro(), _ctx(), _fallos(), _guarda_con(), _pj() (+37 more)

### Community 27 - "test_death.py"
Cohesion: 0.13
Nodes (18): combat_finished(), living_teams(), _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero() (+10 more)

### Community 28 - "Monster"
Cohesion: 0.12
Nodes (27): Monster, _abilities(), _disparo(), _RngFalla, test_banishing_arrow_falla_la_salvacion_y_deja_incapacitado(), test_banishing_arrow_salvacion_exitosa_no_aplica_condicion(), test_beguiling_arrow_hechiza_y_termina_si_el_aliado_ataca(), test_beguiling_sin_aliados_no_tira_salvacion() (+19 more)

### Community 29 - "test_magical.py"
Cohesion: 0.12
Nodes (16): Paquetes con fachada, _uso_de_entrada(), Spell, spell_action(), Spellcasting, _spell_data(), _spellcasting(), test_el_log_del_ataque_dice_dano_no_magico() (+8 more)

### Community 30 - "test_parry.py"
Cohesion: 0.27
Nodes (20): _arquero_parry(), _ataque(), _ctx(), _datos(), _fijar_d20(), espia(), _gladiador(), _pj() (+12 more)

### Community 31 - "test_superior_invisibility.py"
Cohesion: 0.30
Nodes (12): remove_invisibility_on_action(), _accion(), _ctx(), _pixie(), _pj(), test_atacar_con_ventaja_y_no_pierde_la_invisibilidad(), test_ejecutarla_aplica_el_estado(), test_el_monstruo_recibe_su_accion_al_construirse() (+4 more)

### Community 32 - "FighterFeatures"
Cohesion: 0.07
Nodes (7): ActionSurgeAction, _contexto(), _en_5_pies(), FighterFeatures, _rasgo(), SecondWindAction, FeintingAttackAction

### Community 33 - "_ExplotaSiUsaRng"
Cohesion: 0.13
Nodes (24): _accion_rally(), _commanda(), _ExplotaSiUsaRng, _ripostea_directa(), _sustituye(), test_commanders_strike_cede_el_ataque_si_hay_feinting_encolado(), test_commanders_strike_no_se_decide_si_el_aliado_no_tiene_armas(), test_commanders_strike_no_se_decide_si_el_aliado_ya_uso_su_reaccion() (+16 more)

### Community 34 - "test_skills.py"
Cohesion: 0.07
Nodes (34): _clean(), normalize_skill(), skill_ability(), ability_check_bonus(), _avisar_fallo_prueba(), _finish_check(), _guia(), _resolve_mods() (+26 more)

### Community 35 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 36 - "test_arcane_archer.py"
Cohesion: 0.11
Nodes (21): arcane_shot_options_known(), arcane_shot_uses(), apply_arcane_archer(), _firmas(), _pj(), test_apply_arcane_archer_exige_la_clase_fighter(), test_apply_class_equivalente_a_apply_arcane_archer(), test_arcane_archer_lore_da_competencia() (+13 more)

### Community 37 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 38 - "encounter.py"
Cohesion: 0.12
Nodes (11): d20(), roll_d20(), _invoke_policy(), _run_combat(), _nuevo_ctx(), _pasada(), _extract(), first_target_policy() (+3 more)

### Community 39 - "inflict_damage"
Cohesion: 0.14
Nodes (18): _absorber_pv_temporales(), _hooks(), inflict_damage(), _mitigacion_de_otros(), _notify_damage_dealt(), _salvar_a_cero(), _ctx(), _datos() (+10 more)

### Community 40 - "test_mastery.py"
Cohesion: 0.10
Nodes (28): al_acertar(), al_fallar(), _cd_topple(), _log(), _nombre(), resolver_maestria(), _arma(), _atacante() (+20 more)

### Community 41 - "BarbarianFeatures"
Cohesion: 0.10
Nodes (5): BarbarianFeatures, ExtendRageAction, _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 42 - "apply_condition"
Cohesion: 0.08
Nodes (57): Abilities, parse_range_type(), apply_condition(), resolve_attack_range(), _ataque(), _ctx(), _data(), _duelo() (+49 more)

### Community 43 - "pick"
Cohesion: 0.04
Nodes (34): extra_attacks_for(), rage_damage(), roll_dice(), DamageType, parse_damage_type(), log_line(), proficiency_bonus(), pick() (+26 more)

### Community 44 - "test_area.py"
Cohesion: 0.21
Nodes (22): AreaTargeting, select_area_targets(), _default_targeting(), _area_action(), _ctx(), _npc(), _pj(), _save_forzado() (+14 more)

### Community 45 - "TurnResources"
Cohesion: 0.10
Nodes (49): TurnResources, AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer(), _bj() (+41 more)

### Community 46 - "Condition"
Cohesion: 0.19
Nodes (26): Condition, test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+18 more)

### Community 47 - "BattleMasterFeatures"
Cohesion: 0.07
Nodes (10): Battle Master (PHB 2024), _aliados(), _aliados_elegibles(), _armas_melee_propias(), _armas_propias(), BattleMasterFeatures, _de(), _orden_tamano() (+2 more)

### Community 48 - "test_battle_master.py"
Cohesion: 0.07
Nodes (50): _accion_feinting(), _atacado(), _atacado_dos_enemigos(), _bm(), _conoce_sweeping(), _decide(), _parry(), _RngIdx (+42 more)

### Community 49 - "main.py"
Cohesion: 0.09
Nodes (22): CLI del simulador: `build_parser()`, Detalle por flag, Ejemplos, Flujo de `main()`, `--legendary-p`, `--legendary-points`, `--monster` / `-m`, Observaciones (para humanos y IA) (+14 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.06
Nodes (50): ability_check(), CheckResult, attempt_escapes(), EscapeCheck, _ataque(), _check_fijo(), _fake(), _ctx() (+42 more)

### Community 51 - "load_monster"
Cohesion: 0.07
Nodes (24): _armor_class_value(), load_monster(), _norm_name(), _parse_condition_immunities(), test_una_condicion_desconocida_de_la_api_avisa(), test_fixture_sintetica_carga(), test_monstruo_no_legendario_no_carga_guaridas(), test_monstruo_sin_fichero_no_avisa() (+16 more)

### Community 52 - "_con_estilo"
Cohesion: 0.14
Nodes (19): _aliado(), _con_estilo(), _enemigo(), _RngExplota, _RngSi, test_interception_con_un_aliado_no_baja_de_cero_el_daño(), test_interception_no_actúa_con_la_reacción_gastada(), test_interception_no_actúa_contra_un_no_aliado_ni_con_el_mismo_pj() (+11 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.13
Nodes (15): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+7 more)

### Community 57 - "hooks"
Cohesion: 0.08
Nodes (16): Cavalier (XGE), _agrandado(), _bando_del(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), daño_base_arma() (+8 more)

### Community 59 - "apply_class"
Cohesion: 0.15
Nodes (18): apply_class(), ClassDef, normalize_class_name(), register_class(), test_apply_exige_clase_barbaro(), _abilities(), _firmas(), _pj() (+10 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.10
Nodes (25): ConditionInstance, _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab() (+17 more)

### Community 61 - "begin_turn"
Cohesion: 0.27
Nodes (15): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+7 more)

### Community 62 - ".alive"
Cohesion: 0.14
Nodes (5): _es_aliado(), _armas_melee_de(), CavalierFeatures, _de(), _avisar_ataque_especial_marca()

### Community 63 - "traits/__init__.py"
Cohesion: 0.05
Nodes (13): DamageTransfer, HeatedBody, Parry, TurnResistance, aliados_capaces(), _condicion_posicional(), MartialAdvantage, PackTactics (+5 more)

### Community 64 - "loader.py"
Cohesion: 0.03
Nodes (44): ability_mod(), normalize_ability(), is_area_action(), parse_attach_effects(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects() (+36 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.05
Nodes (49): _aliados_en_aura(), apply_storm_herald(), _cd(), _dado_mar(), _de(), _en_aura(), _enemigos_en_aura(), _escalado() (+41 more)

### Community 66 - "save_modifiers"
Cohesion: 0.15
Nodes (12): _condiciones(), _hooks(), _instancias(), save_modifiers(), _datos(), _lich(), _pj(), test_con_ventaja_acierta_mas_que_sin_ella() (+4 more)

### Community 67 - "test_backgrounds.py"
Cohesion: 0.10
Nodes (20): Background, normalize_tool(), get_background(), _add(), load_background(), parse_background(), _abilities(), _pj() (+12 more)

### Community 68 - "_mon"
Cohesion: 0.21
Nodes (16): espia(), _espiar_divine(), _furia(), _mon(), test_determinismo_misma_semilla_mismos_resultados(), corrida(), test_divine_fury_elige_radiante_con_pick(), test_divine_fury_funciona_a_distancia() (+8 more)

### Community 69 - "test_fighter.py"
Cohesion: 0.10
Nodes (37): apply_fighter(), maestria_de(), _abilities(), _firmas(), _pj(), _pj_con_armas(), test_apply_class_fighter_sin_subclase_equivalente_a_apply_fighter(), test_apply_class_reenvía_el_estilo_de_combate() (+29 more)

### Community 70 - "apply_cavalier"
Cohesion: 0.11
Nodes (20): cavalier_mark_uses(), warding_maneuver_uses(), apply_cavalier(), CavalierMarkAttackAction, _cavalier(), _pj(), test_apply_cavalier_exige_la_clase_fighter(), test_apply_cavalier_requiere_nivel_3() (+12 more)

### Community 71 - "LegendaryState"
Cohesion: 0.15
Nodes (12): lair_phase(), LairAction, LegendaryState, _enemigo(), _Stub, test_dos_acciones_uniformes(), test_no_actua_si_el_combate_cae_en_medio(), test_no_actua_si_el_dueno_cae_o_no_puede_actuar() (+4 more)

### Community 72 - "GiantFeatures"
Cohesion: 0.16
Nodes (4): _de(), GiantFeatures, _objetivos_impel(), _orden_de()

### Community 73 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 74 - "test_lair.py"
Cohesion: 0.13
Nodes (17): _ctx(), _dragon(), lairs_dir(), _orden_con(), _pj(), _spy_turnos(), spy(), test_guarida_pasa_magical_a_las_salvaciones() (+9 more)

### Community 76 - "json"
Cohesion: 0.18
Nodes (5): _cache_path(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError

### Community 77 - "test_races.py"
Cohesion: 0.08
Nodes (29): Race, _get_entry(), get_race(), get_trait(), load_race(), parse_race(), _skill_name(), _spells_from_description() (+21 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.14
Nodes (25): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+17 more)

### Community 79 - "parse_spellcasting"
Cohesion: 0.20
Nodes (5): parse_spellcasting(), test_el_lanzador_se_lee_de_los_actions(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_la_curacion_usa_el_modificador_de_caracteristica_no_el_bono_completo(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 80 - "Any"
Cohesion: 0.18
Nodes (6): _as_condition(), _condicion_bloqueada(), _contar(), _label(), _queda_accion(), remove_condition()

### Community 81 - "run_combat"
Cohesion: 0.13
Nodes (16): CombatResult, run_combat(), _summarize_damage(), _breath(), _eventos(), _FixedRandom, _load_fixture(), _player() (+8 more)

### Community 83 - "dnd_sim/__init__.py"
Cohesion: 0.05
Nodes (27): _objetivo_enganche(), valid_targets(), _reaccion_si_procede(), _tag_modificadores(), ActionType, actor_is_alive(), CombatAction, CombatContext (+19 more)

### Community 84 - "PlayerCharacter"
Cohesion: 0.10
Nodes (25): simulate(), PlayerCharacter, apply_damage_modifiers(), _is_petrified(), _guerrero_y_ogro(), _target(), test_attack_roll_log_modifier(), test_danio_medio_por_combatiente_y_equipo() (+17 more)

### Community 85 - "test_spells.py"
Cohesion: 0.12
Nodes (25): build_spell_actions(), _ctx(), _desde_fixture(), _monstruo_lanzador(), _npc(), _pj(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_hechizado_ataca_a_los_de_su_propio_bando() (+17 more)

### Community 87 - "test_azer.py"
Cohesion: 0.08
Nodes (28): Cómo comprobar que todo sigue en orden, _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api(), _ataque_melee(), _ataque_ranged() (+20 more)

### Community 88 - "test_cavalier.py"
Cohesion: 0.13
Nodes (19): cavalier_mark_extra_damage(), _cargar_main(), _parchea_ataque(), _parchea_warding(), test_daño_extra_del_ataque_especial_es_el_nivel_entre_dos(), test_el_flag_charge_p_llega_al_rasgo(), test_flag_charge_p_en_el_cli(), test_hold_the_line_con_decision_negativa_no_gasta_nada() (+11 more)

### Community 89 - "test_extra_damage.py"
Cohesion: 0.17
Nodes (18): DamageRecorder, _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional() (+10 more)

### Community 90 - "AtaqueSustituido"
Cohesion: 0.16
Nodes (11): _sustituir_ataque(), AtaqueSustituido, _abilities(), _blanco(), _pj(), _RasgoQueSustituye, _RasgoSinSustitucion, _RngExplota (+3 more)

### Community 91 - "_carga"
Cohesion: 0.16
Nodes (14): _ataque_carga(), _carga(), _salvacion(), test_ferocious_charger_cd_es_ocho_mas_pb_mas_fuerza(), test_ferocious_charger_con_p_medio_tira_un_random(), test_ferocious_charger_el_flag_se_reinicia_cada_turno(), test_ferocious_charger_nivel_14_no_actua_sin_rng(), test_ferocious_charger_p_cero_no_carga_sin_rng() (+6 more)

### Community 93 - "test_ancestral_guardian.py"
Cohesion: 0.10
Nodes (28): AncestralGuardianFeatures, apply_ancestral_guardian(), _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado() (+20 more)

### Community 94 - "_bajo_ataque"
Cohesion: 0.17
Nodes (18): _bajo_ataque(), _defiende(), _RngExplota, test_hold_the_line_exige_nivel_10(), test_hold_the_line_no_contra_un_atacante_muerto_o_no_enemigo(), test_hold_the_line_no_reentra_con_un_ataque_de_reacción(), test_hold_the_line_no_se_usa_sin_reacción_o_sin_ataque_cuerpo_a_cuerpo(), test_vigilant_defender_no_tiene_reacción_especial_por_debajo_del_nivel_18() (+10 more)

### Community 95 - "SaveDamage"
Cohesion: 0.11
Nodes (10): _check_fields(), _construir(), _error(), SaveAction, AreaSaveAction, ConditionAction, ConditionEffect, RepeatSave (+2 more)

### Community 96 - "_abilities"
Cohesion: 0.20
Nodes (17): _abilities(), _marca_con(), _marcado(), _mods(), _RngSi, test_incapacitado_el_marcador_anula_la_marca(), test_la_marca_caduca_en_la_ronda_indicada(), test_la_marca_no_se_consume_y_no_aplica_al_atacar_al_marcador() (+9 more)

### Community 97 - "_clamp"
Cohesion: 0.15
Nodes (9): action_surge_uses(), _clamp(), fighter_extra_attacks_for(), indomitable_uses(), weapon_mastery_count(), test_action_surge_usos_por_nivel_son_1_y_2(), test_indomitable_usos_por_nivel_son_1_2_y_3(), test_los_golpes_del_guerrero_suben_en_5_11_y_20() (+1 more)

### Community 98 - "parse_traits"
Cohesion: 0.17
Nodes (8): _declara_uso(), _entradas(), parse_traits(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd(), test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad(), test_el_umbral_se_saca_de_cada_descripcion(), test_el_rasgo_se_parsea_desde_el_srd(), test_parse_traits_ignora_entradas_malformadas()

### Community 99 - "_decision"
Cohesion: 0.19
Nodes (14): _furia_de(), _decision(), _forma(), test_forma_divina_concede_las_tres_resistencias(), test_forma_no_quita_resistencias_de_otro_origen(), test_forma_revocada_al_terminar_la_furia(), test_forma_se_vuelve_a_ofrecer_si_dice_que_no(), test_forma_una_vez_por_combate() (+6 more)

### Community 100 - "barbarian/__init__.py"
Cohesion: 0.06
Nodes (15): apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), SpikedArmorAction, FormOfTheBeast, NaturalWeapon, apply_zealot() (+7 more)

### Community 101 - "_RngSi"
Cohesion: 0.12
Nodes (11): _RngSi, test_arcane_shot_se_aplica_una_sola_vez_por_turno(), test_arcane_shot_se_gasta_un_uso_al_aplicar(), test_daño_de_arcane_shot_es_2d6_antes_del_18(), _dado(), test_daño_de_arcane_shot_es_4d6_desde_el_18(), test_decision_de_impacto_no_gasta_el_uso_hasta_impactar(), test_piercing_gasta_el_uso_al_sustituir() (+3 more)

### Community 103 - "Combatant"
Cohesion: 0.18
Nodes (7): Arquitectura de `dnd_sim`, Carpetas, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, Combatant

### Community 105 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.12
Nodes (12): Arcane Archer (XGE), CombatState, test_ever_ready_shot_no_cambia_los_usos_al_empezar_un_combate(), test_la_marca_de_enfeebling_mitiga_por_ronda(), Arcane Archer: Piercing y Seeking, Battle Master: plan de sesión 1, Fighter: pendientes reales, Grafo y verificación (+4 more)

### Community 106 - "Attack"
Cohesion: 0.10
Nodes (35): D20Result, RollMode, _actualizar_distancia(), attack_roll(), _decidir_maniobra(), _mode_tag(), Attack, test_commanders_strike_con_relentless_no_gasta_dado() (+27 more)

### Community 107 - "_especial"
Cohesion: 0.29
Nodes (10): _accion_marca(), _especial(), _pick_sin_decision(), test_el_ataque_especial_no_gasta_un_uso_ni_la_reaccion(), test_el_ataque_especial_no_suma_dano_extra_si_falla(), test_el_ataque_especial_se_arma_cuando_el_marcado_dana_a_un_tercero(), test_el_ataque_especial_solo_vale_en_el_siguiente_turno(), test_el_ataque_especial_suma_el_dano_extra_si_impacta() (+2 more)

### Community 108 - "parse_escape"
Cohesion: 0.22
Nodes (5): has_escape_text(), parse_escape(), _skills_for(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 110 - "roll_initiative"
Cohesion: 0.36
Nodes (8): roll_initiative(), _d20_fijo(), test_ambush_con_la_decision_no_no_gasta_nada(), test_ambush_con_relentless_no_gasta_dado(), test_ambush_sin_dados_no_consume_rng(), test_ambush_sin_la_maniobra_no_consume_rng(), test_ambush_suma_un_dado_a_la_tirada_de_iniciativa(), test_sin_subclase_roll_initiative_no_consulta_bonus()

### Community 111 - "apply_beast"
Cohesion: 0.25
Nodes (6): apply_beast(), _ctx(), test_bestial_solo_marca_las_armas_magicas_desde_el_nivel_6(), test_las_armas_dinamicas_de_la_furia_heredan_el_flag(), test_un_pj_beast_nivel_5_no_supera_la_resistencia(), test_un_pj_beast_nivel_6_dana_completo_al_ghost()

### Community 112 - "load_lair"
Cohesion: 0.40
Nodes (3): load_lair(), test_esquema_invalido(), test_targeting_fuera_de_rango()

### Community 113 - "test_apply_class_equivalente_a_apply_cavalier"
Cohesion: 0.40
Nodes (3): _firmas(), test_apply_class_equivalente_a_apply_cavalier(), _trait()

## Knowledge Gaps
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Condition` connect `Condition` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_legendary.py`, `test_beast.py`, `parse_spell`, `test_traits.py`, `test_utility.py`, `consumir_marcas`, `ArcaneArcherFeatures`, `Monster`, `test_parry.py`, `test_superior_invisibility.py`, `test_skills.py`, `test_arcane_archer.py`, `test_mastery.py`, `BarbarianFeatures`, `apply_condition`, `pick`, `BattleMasterFeatures`, `test_battle_master.py`, `test_checks_escapes.py`, `load_monster`, `test_condition_immunities.py`, `hooks`, `test_magic_resistance.py`, `.alive`, `traits/__init__.py`, `loader.py`, `test_storm_herald.py`, `save_modifiers`, `LegendaryState`, `GiantFeatures`, `test_pack_tactics.py`, `test_lair.py`, `ConditionTracker`, `test_enlarge.py`, `Any`, `dnd_sim/__init__.py`, `PlayerCharacter`, `test_spells.py`, `test_cavalier.py`, `_carga`, `_abilities`, `Combatant`, `Any`, `Attack`, `AttachOnHitEffect`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `daño_base_arma()`) actually correct?**
  _`Attack` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `_trait` be split into smaller, more focused modules?**
  _Cohesion score 0.1140819964349376 - nodes in this community are weakly interconnected._
- **Why does `Monster` connect `Monster` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_traits.py`, `_arquero`, `test_utility.py`, `test_wild_magic.py`, `apply_battle_master`, `consumir_marcas`, `test_martial_advantage.py`, `test_zealot.py`, `test_death.py`, `test_magical.py`, `test_parry.py`, `test_superior_invisibility.py`, `_ExplotaSiUsaRng`, `test_undead_fortitude.py`, `test_arcane_archer.py`, `inflict_damage`, `test_mastery.py`, `apply_condition`, `pick`, `test_area.py`, `TurnResources`, `Condition`, `test_battle_master.py`, `test_checks_escapes.py`, `load_monster`, `test_condition_immunities.py`, `test_magic_resistance.py`, `loader.py`, `test_storm_herald.py`, `_mon`, `test_fighter.py`, `apply_cavalier`, `LegendaryState`, `test_pack_tactics.py`, `test_lair.py`, `test_enlarge.py`, `dnd_sim/__init__.py`, `PlayerCharacter`, `test_spells.py`, `test_azer.py`, `test_cavalier.py`, `AtaqueSustituido`, `_carga`, `test_ancestral_guardian.py`, `_bajo_ataque`, `_abilities`, `_RngSi`, `Combatant`, `Attack`, `_especial`, `roll_initiative`, `test_sustitucion_hace_un_solo_par_de_picks`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Monster` (e.g. with `Carpetas` and `_cloaker()`) actually correct?**
  _`Monster` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14714714714714713 - nodes in this community are weakly interconnected._
- **Why does `Attack` connect `Attack` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_traits.py`, `_arquero`, `test_utility.py`, `test_wild_magic.py`, `apply_battle_master`, `consumir_marcas`, `apply_barbarian`, `test_zealot.py`, `test_death.py`, `Monster`, `test_magical.py`, `test_parry.py`, `test_superior_invisibility.py`, `_ExplotaSiUsaRng`, `test_undead_fortitude.py`, `test_arcane_archer.py`, `inflict_damage`, `test_mastery.py`, `apply_condition`, `pick`, `TurnResources`, `Condition`, `test_battle_master.py`, `main.py`, `test_checks_escapes.py`, `load_monster`, `_con_estilo`, `hooks`, `apply_class`, `test_magic_resistance.py`, `begin_turn`, `loader.py`, `test_storm_herald.py`, `test_fighter.py`, `apply_cavalier`, `test_pack_tactics.py`, `test_enlarge.py`, `dnd_sim/__init__.py`, `PlayerCharacter`, `test_spells.py`, `test_azer.py`, `test_cavalier.py`, `test_extra_damage.py`, `AtaqueSustituido`, `_carga`, `test_ancestral_guardian.py`, `SaveDamage`, `_abilities`, `barbarian/__init__.py`, `_RngSi`, `Combatant`, `test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque`, `test_sustitucion_hace_un_solo_par_de_picks`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
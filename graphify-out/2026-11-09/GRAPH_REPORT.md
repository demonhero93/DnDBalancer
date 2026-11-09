# Graph Report - DnDBalancer  (2026-11-09)

## Corpus Check
- 223 files · ~186,612 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 3563 nodes · 12939 edges · 110 communities (96 shown, 14 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 829 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `02ee0528`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- _trait
- inflict_damage
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
- Trait
- spell_parser.py
- DamageTransfer
- .activar_aura
- test_ancestral_guardian.py
- test_loader_actions.py
- model/actions.py
- ArcaneArcherFeatures
- ActionUsage
- apply_barbarian
- test_martial_advantage.py
- ZealotFeatures
- test_zealot.py
- test_death.py
- Monster
- test_magical.py
- test_parry.py
- test_superior_invisibility.py
- FighterFeatures
- BeastFeatures
- test_skills.py
- test_undead_fortitude.py
- test_arcane_archer.py
- test_multiattack.py
- TurnResources
- test_relentless.py
- test_mastery.py
- BarbarianFeatures
- apply_condition
- saves.py
- test_area.py
- random
- Condition
- ability_check
- build_spell_actions
- main.py
- test_checks_escapes.py
- load_monster
- _con_estilo
- saving_throw
- test_condition_immunities.py
- Combatant
- run_combat
- test_magic_resistance.py
- test_regeneration.py
- loader.py
- traits/__init__.py
- legendary_parser.py
- test_storm_herald.py
- RollMode
- test_backgrounds.py
- SpellFixedDamageAction
- Attack
- dnd_sim/__init__.py
- pathlib
- BattleragerFeatures
- test_pack_tactics.py
- test_lair.py
- ConditionInstance
- json
- test_races.py
- test_enlarge.py
- WildHeartFeatures
- attempt_escapes
- test_fighter.py
- pick
- spell_action
- PlayerCharacter
- AtaqueSustituido
- _RngMax
- test_azer.py
- test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque
- test_extra_damage.py
- test_sustituir_ataque.py
- condition_parser.py
- multiattack_parser.py
- apply_class
- race_parser.py
- background_parser.py
- _RngSi
- _clamp
- AncestralGuardianFeatures
- _por_datos
- attack_roll
- _RngExplota
- test_el_gancho_after_failed_check_desde_ability_check_con_ctx
- load_race
- _mode_tag
- CombatState
- DamageRecorder
- test_tactical_master_nivel_9_elige_entre_original_push_sap_slow
- test_sustitucion_hace_un_solo_par_de_picks

## God Nodes (most connected - your core abstractions)
1. `Attack` - 207 edges
2. `Condition` - 173 edges
3. `Monster` - 162 edges
4. `apply_condition()` - 152 edges
5. `AttackRange` - 151 edges
6. `Abilities` - 149 edges
7. `attack_roll()` - 143 edges
8. `load_monster()` - 136 edges
9. `PlayerCharacter` - 132 edges
10. `run_combat()` - 98 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Fighter: cómo añadir una subclase` --references--> `SubclassDef`  [INFERRED]
  TODO.md → dnd_sim/rules/classes/base.py
- `Arcane Archer (XGE)` --references--> `roll_dice()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/dice.py

## Import Cycles
- None detected.

## Communities (110 total, 14 thin omitted)

### Community 0 - "_trait"
Cohesion: 0.14
Nodes (33): ability_mod(), _check_fallada(), _ctx(), _fighter(), _objetivo(), _save_fallada(), _saving_nueva(), test_action_surge_no_existe_en_nivel_1() (+25 more)

### Community 1 - "inflict_damage"
Cohesion: 0.08
Nodes (35): desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), _absorber_pv_temporales(), _hooks(), inflict_damage(), _mitigacion_de_otros() (+27 more)

### Community 2 - "AttackRange"
Cohesion: 0.07
Nodes (55): AttackRange, RageAction, apply_berserker(), _de(), _furia_de(), _golpe_sin_armas(), IntimidatingPresenceAction, _abilities() (+47 more)

### Community 3 - "test_giant.py"
Cohesion: 0.09
Nodes (36): apply_giant(), _de(), MightyImpelAction, _objetivos_impel(), _orden_de(), _abilities(), _barbaro(), _ctx() (+28 more)

### Community 4 - "test_world_tree.py"
Cohesion: 0.12
Nodes (38): _abilities(), _aliado(), _barbaro(), _ctx(), _decision(), _elige_candidato(), espia(), _furia() (+30 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.15
Nodes (41): _abilities(), _aliado(), _barbaro(), _ctx(), _furia(), _mods(), _mon(), _pick_fijo() (+33 more)

### Community 6 - "test_proficiency.py"
Cohesion: 0.15
Nodes (21): ability_check_bonus(), test_sin_autoexito_ni_autofallo_en_pruebas(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia() (+13 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.07
Nodes (62): simulate(), legendary_phase(), LegendaryAction, _contexto(), _data(), _estado(), _legendaria(), _load() (+54 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (65): WeaponAttackAction, _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll(), spy() (+57 more)

### Community 9 - "test_spells.py"
Cohesion: 0.10
Nodes (42): parse_spell(), _ctx(), _npc(), _pj(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot() (+34 more)

### Community 10 - "test_traits.py"
Cohesion: 0.10
Nodes (25): attack_modifiers(), _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _RasgoDeSalvacion, _sahuagin() (+17 more)

### Community 11 - "_arquero"
Cohesion: 0.10
Nodes (30): _arco(), _arquero(), _ctx_curving(), _curving(), _RngExplota, _RngNo, test_arcane_shot_crea_usos_por_nivel(), test_arcane_shot_se_reinicia_en_on_turn_start() (+22 more)

### Community 12 - "test_utility.py"
Cohesion: 0.19
Nodes (23): _abilities(), _ctx(), _mon(), _pj(), _siempre_falla(), test_actor_no_disponible_no_consulta_la_probabilidad(), test_agarrar_admite_hasta_un_tamano_mayor(), test_agarrar_aplica_agarrado_con_escape_de_acción() (+15 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.13
Nodes (38): _abilities(), _barbaro(), _con_cola(), _con_efecto(), espia(), _ctx(), _furia(), _mon() (+30 more)

### Community 14 - "Trait"
Cohesion: 0.05
Nodes (5): Attach, Trait, BloodFrenzy, test_hooks_con_un_nombre_fuera_del_catalogo_lanza_error(), test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 15 - "spell_parser.py"
Cohesion: 0.09
Nodes (13): _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla(), _frases() (+5 more)

### Community 16 - "DamageTransfer"
Cohesion: 0.23
Nodes (3): DamageTransfer, _empuna_arma_melee(), _ve_al_atacante()

### Community 17 - ".activar_aura"
Cohesion: 0.12
Nodes (7): _aliados_en_aura(), _cd(), _dado_mar(), _de(), _en_aura(), _enemigos_en_aura(), _escalado()

### Community 18 - "test_ancestral_guardian.py"
Cohesion: 0.17
Nodes (26): _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado(), _escudo(), _esperado() (+18 more)

### Community 19 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (14): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+6 more)

### Community 20 - "model/actions.py"
Cohesion: 0.04
Nodes (37): combat_finished(), living_teams(), _objetivo_enganche(), valid_targets(), build_condition_action(), _invoke_policy(), roll_initiative(), _run_combat() (+29 more)

### Community 21 - "ArcaneArcherFeatures"
Cohesion: 0.08
Nodes (5): ArcaneArcherFeatures, _ctx_con_rng(), _CtxConRng, _de(), _otros_enemigos()

### Community 22 - "ActionUsage"
Cohesion: 0.11
Nodes (11): ActionUsage, UsageKind, _FixedRandom, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar(), test_per_day_no_tira_recarga(), test_per_day_reset_restaura_todos_los_usos(), test_recharge_5_6_porcentaje_de_exito() (+3 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.08
Nodes (51): rage_uses(), apply_barbarian(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj(), _resultado() (+43 more)

### Community 24 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 25 - "ZealotFeatures"
Cohesion: 0.10
Nodes (7): _de(), _en_60_pies(), _es_aliado(), _furia_de(), _reserva_dados(), ZealotFeatures, test_apply_class_por_clave_aplica_zealot()

### Community 26 - "test_zealot.py"
Cohesion: 0.06
Nodes (83): WarriorHealAction, SaveResult, fake_saving_throw(), falla(), espia(), stub(), stub(), _abilities() (+75 more)

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 28 - "Monster"
Cohesion: 0.13
Nodes (25): Monster, _abilities(), _disparo(), _RngFalla, test_banishing_arrow_falla_la_salvacion_y_deja_incapacitado(), test_banishing_arrow_salvacion_exitosa_no_aplica_condicion(), test_beguiling_arrow_hechiza_y_termina_si_el_aliado_ataca(), test_beguiling_sin_aliados_no_tira_salvacion() (+17 more)

### Community 29 - "test_magical.py"
Cohesion: 0.10
Nodes (19): apply_beast(), _ctx(), _pj(), test_ataque_con_magical_true_dana_completo_al_ghost(), test_ataque_magico_contra_un_bárbaro_en_furia_se_reduce_a_la_mitad(), test_bestial_solo_marca_las_armas_magicas_desde_el_nivel_6(), test_el_log_del_ataque_dice_dano_no_magico(), test_inflict_damage_registra_la_bandera_magical() (+11 more)

### Community 30 - "test_parry.py"
Cohesion: 0.24
Nodes (22): D20Result, _arquero_parry(), _ataque(), _ctx(), _datos(), _fijar_d20(), espia(), _gladiador() (+14 more)

### Community 31 - "test_superior_invisibility.py"
Cohesion: 0.13
Nodes (20): _declara_uso(), _entradas(), parse_traits(), _usage(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd(), test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad(), test_el_umbral_se_saca_de_cada_descripcion(), _accion() (+12 more)

### Community 32 - "FighterFeatures"
Cohesion: 0.11
Nodes (5): ActionSurgeAction, _contexto(), FighterFeatures, _rasgo(), SecondWindAction

### Community 34 - "test_skills.py"
Cohesion: 0.09
Nodes (26): has_escape_text(), parse_escape(), _skills_for(), check_modifiers(), _abilities(), _load_fixture(), _pj(), _SoloMod (+18 more)

### Community 35 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 36 - "test_arcane_archer.py"
Cohesion: 0.11
Nodes (23): arcane_shot_options_known(), arcane_shot_uses(), apply_arcane_archer(), CurvingShotAction, _firmas(), _pj(), test_accion_curving_se_anade_desde_el_nivel_7(), test_apply_arcane_archer_exige_la_clase_fighter() (+15 more)

### Community 37 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 38 - "TurnResources"
Cohesion: 0.10
Nodes (12): _nuevo_ctx(), CombatContext, _log(), TurnResources, AreaSaveAction, SpellStateAction, _contexto_de_reaccion(), _ctx() (+4 more)

### Community 39 - "test_relentless.py"
Cohesion: 0.27
Nodes (12): _ctx(), _datos(), _jabali(), _pj(), test_el_jabali_carga_su_relentless_con_umbral_y_uso(), test_relentless_no_necesita_contexto_ni_rng(), test_reset_reestablece_el_umbral_y_los_usos(), test_solo_puede_salvarse_una_vez_por_combate() (+4 more)

### Community 40 - "test_mastery.py"
Cohesion: 0.10
Nodes (29): al_acertar(), al_fallar(), _cd_topple(), consumir_marcas(), _log(), _nombre(), resolver_maestria(), _arma() (+21 more)

### Community 41 - "BarbarianFeatures"
Cohesion: 0.09
Nodes (5): BarbarianFeatures, ExtendRageAction, _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 42 - "apply_condition"
Cohesion: 0.08
Nodes (57): Abilities, apply_condition(), end_turn(), resolve_attack_range(), _ataque(), _ctx(), _data(), _duelo() (+49 more)

### Community 43 - "saves.py"
Cohesion: 0.05
Nodes (19): rage_damage(), d20(), roll_d20(), roll_dice(), DamageType, parse_damage_type(), sample(), _bonus_de_tamano() (+11 more)

### Community 44 - "test_area.py"
Cohesion: 0.09
Nodes (31): _check_fields(), _construir(), _error(), build_save_action(), AreaTargeting, select_area_targets(), _default_targeting(), SaveDamage (+23 more)

### Community 45 - "random"
Cohesion: 0.11
Nodes (49): AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer(), _bj(), _ctx() (+41 more)

### Community 46 - "Condition"
Cohesion: 0.20
Nodes (25): Condition, _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj(), test_atacar_a_un_invisible_tiene_desventaja() (+17 more)

### Community 47 - "ability_check"
Cohesion: 0.12
Nodes (13): _clean(), normalize_skill(), skill_ability(), ability_check(), _avisar_fallo_prueba(), CheckResult, _finish_check(), _guia() (+5 more)

### Community 48 - "build_spell_actions"
Cohesion: 0.13
Nodes (12): build_spell_actions(), parse_spellcasting(), _desde_fixture(), _monstruo_lanzador(), test_el_lanzador_se_lee_de_los_actions(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_la_reaccion_gasta_su_uso_propio() (+4 more)

### Community 49 - "main.py"
Cohesion: 0.11
Nodes (22): CLI del simulador: `build_parser()`, Detalle por flag, Ejemplos, Flujo de `main()`, `--legendary-p`, `--legendary-points`, `--monster` / `-m`, Observaciones (para humanos y IA) (+14 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.08
Nodes (47): EscapeCheck, effective_ac(), begin_turn(), _ataque(), _check_fijo(), _fake(), _ctx(), _data() (+39 more)

### Community 51 - "load_monster"
Cohesion: 0.14
Nodes (15): _armor_class_value(), load_monster(), test_una_condicion_desconocida_de_la_api_avisa(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper() (+7 more)

### Community 52 - "_con_estilo"
Cohesion: 0.23
Nodes (16): _aliado(), _con_estilo(), _enemigo(), _mods(), _RngSi, test_interception_con_un_aliado_no_baja_de_cero_el_daño(), test_interception_no_actúa_con_la_reacción_gastada(), test_interception_no_actúa_contra_un_no_aliado_ni_con_el_mismo_pj() (+8 more)

### Community 53 - "saving_throw"
Cohesion: 0.06
Nodes (24): log_line(), _apply_condition_riders(), _bolstering(), _cd(), _de(), _en_30_pies(), _enemigos(), _espiritu() (+16 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.11
Nodes (17): ConditionEffect, test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats() (+9 more)

### Community 57 - "Combatant"
Cohesion: 0.04
Nodes (16): normalize_ability(), proficiency_bonus(), _agrandado(), _bonus_de_rasgos(), _bonus_defensivo(), _dados_de_ataque(), daño_base_arma(), _piso_dados_rasgos() (+8 more)

### Community 59 - "run_combat"
Cohesion: 0.16
Nodes (13): CombatResult, run_combat(), _summarize_damage(), _eventos(), _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(), test_copias_de_un_monstruo_tienen_estado_independiente() (+5 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.12
Nodes (20): _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_condition_action_de_hechizo_pasa_magical(), spy() (+12 more)

### Community 61 - "test_regeneration.py"
Cohesion: 0.30
Nodes (13): _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno(), test_el_troll_carga_su_regeneracion() (+5 more)

### Community 62 - "loader.py"
Cohesion: 0.08
Nodes (8): doblar_dados(), parse_attach_effects(), _norm_name(), _parse_condition_immunities(), _parse_damage_modifiers(), ExtraDamage, CombatantType, test_doblar_dados_duplica_los_dados_y_no_el_bonus()

### Community 63 - "traits/__init__.py"
Cohesion: 0.05
Nodes (11): Parry, TurnResistance, aliados_capaces(), _condicion_posicional(), MartialAdvantage, PackTactics, SuperiorInvisibility, _es_radiante() (+3 more)

### Community 64 - "legendary_parser.py"
Cohesion: 0.08
Nodes (16): _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary(), _por_referencia() (+8 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.13
Nodes (37): _abilities(), _aliado(), _barbaro(), _ctx(), _fijar_fallo_reaccion(), _fijar_salvacion(), _furia(), _herald() (+29 more)

### Community 66 - "RollMode"
Cohesion: 0.12
Nodes (17): RollMode, AttachOnHitEffect, _condiciones(), _hooks(), _instancias(), save_modifiers(), test_el_rasgo_anade_la_fuente_resistencia_magica(), test_sin_efecto_magico_o_sin_rasgo_no_anade_ventaja() (+9 more)

### Community 67 - "test_backgrounds.py"
Cohesion: 0.16
Nodes (17): Background, load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes(), test_apply_background_sin_competencias_es_inofensivo() (+9 more)

### Community 68 - "SpellFixedDamageAction"
Cohesion: 0.50
Nodes (3): SpellFixedDamageAction, test_el_proyectil_magico_pasa_por_los_modificadores_de_dano(), lanzar()

### Community 69 - "Attack"
Cohesion: 0.09
Nodes (35): Attack, _nuevo_ataque(), apply_fighter(), maestria_de(), test_alma_bestial_flag_magical_existe(), _abilities(), _pj(), _pj_con_armas() (+27 more)

### Community 70 - "dnd_sim/__init__.py"
Cohesion: 0.06
Nodes (17): FormOfTheBeast, NaturalWeapon, BerserkerFeatures, GiantFeatures, apply_storm_herald(), StormAuraAction, StormHeraldFeatures, apply_wild_heart() (+9 more)

### Community 71 - "pathlib"
Cohesion: 0.19
Nodes (6): Cómo comprobar que todo sigue en orden, _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api()

### Community 72 - "BattleragerFeatures"
Cohesion: 0.15
Nodes (4): apply_battlerager(), BattleragerFeatures, _de(), SpikedArmorAction

### Community 73 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 74 - "test_lair.py"
Cohesion: 0.07
Nodes (35): load_lair(), lair_phase(), LairAction, LegendaryState, _ctx(), _dragon(), _enemigo(), lairs_dir() (+27 more)

### Community 75 - "ConditionInstance"
Cohesion: 0.20
Nodes (3): ConditionInstance, test_implicaciones_de_las_condiciones(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab()

### Community 76 - "json"
Cohesion: 0.15
Nodes (9): _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError (+1 more)

### Community 77 - "test_races.py"
Cohesion: 0.22
Nodes (12): Race, _abilities(), _fiendish_legacy(), _pj(), test_apply_race_añade_competencias_fijas(), test_apply_race_con_habilidad_pedida(), test_apply_race_habilidad_fuera_de_las_opciones_es_error(), test_apply_race_no_duplica_competencias_existentes() (+4 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.16
Nodes (23): _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj(), _spell_data() (+15 more)

### Community 79 - "WildHeartFeatures"
Cohesion: 0.13
Nodes (5): _con_beneficio(), _de(), _en_5_pies(), _orden_de(), WildHeartFeatures

### Community 80 - "attempt_escapes"
Cohesion: 0.21
Nodes (6): _as_condition(), attempt_escapes(), _condicion_bloqueada(), _contar(), _label(), remove_condition()

### Community 81 - "test_fighter.py"
Cohesion: 0.11
Nodes (18): second_wind_uses(), _action_surge(), _ctx_recursos(), _firmas(), _RngBajo, _second_wind(), test_action_surge_como_maximo_un_vez_por_turno(), test_action_surge_ejecutada_restaura_la_accion_y_gasta_un_uso() (+10 more)

### Community 82 - "pick"
Cohesion: 0.05
Nodes (12): pick(), _extract(), first_target_policy(), random_policy(), _armas_melee_de(), _hostil(), _aliados_heridos(), _cd_ataque() (+4 more)

### Community 83 - "spell_action"
Cohesion: 0.07
Nodes (20): Paquetes con fachada, _uso_de_entrada(), SaveAction, HealAction, SpellAction, SpellAttackAction, dado_por_nivel(), duracion_en_rondas() (+12 more)

### Community 84 - "PlayerCharacter"
Cohesion: 0.13
Nodes (19): PlayerCharacter, _guerrero_y_ogro(), _target(), test_attack_roll_log_modifier(), test_danio_medio_por_combatiente_y_equipo(), test_etiqueta_de_modificadores_se_deriva_del_dano_final(), test_immune_target_takes_zero_damage(), test_immunity_zero() (+11 more)

### Community 85 - "AtaqueSustituido"
Cohesion: 0.09
Nodes (18): Arcane Archer (XGE), Arquitectura de `dnd_sim`, Carpetas, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, AtaqueSustituido (+10 more)

### Community 87 - "test_azer.py"
Cohesion: 0.23
Nodes (18): HeatedBody, _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), _rasgo() (+10 more)

### Community 89 - "test_extra_damage.py"
Cohesion: 0.23
Nodes (17): _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional(), test_ataque_sin_extra_no_llama_al_bucle() (+9 more)

### Community 90 - "test_sustituir_ataque.py"
Cohesion: 0.17
Nodes (10): _sustituir_ataque(), _abilities(), _blanco(), _pj(), _RasgoQueSustituye, _RasgoSinSustitucion, _RngExplota, test_rasgo_que_devuelve_none_conserva_el_flujo_y_las_semillas() (+2 more)

### Community 91 - "condition_parser.py"
Cohesion: 0.14
Nodes (7): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), parse_range_type(), _sentence_with(), test_el_tipo_de_ataque_coincide_con_el_texto()

### Community 92 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (5): _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 93 - "apply_class"
Cohesion: 0.13
Nodes (19): apply_ancestral_guardian(), apply_class(), ClassDef, normalize_class_name(), register_class(), SubclassDef, _abilities(), _firmas() (+11 more)

### Community 94 - "race_parser.py"
Cohesion: 0.15
Nodes (9): parse_race(), _skill_name(), _spells_from_description(), _trait_skills(), _keen_senses(), test_parse_competencias_fijas_de_la_raza(), test_parse_descripcion_sin_hechizos_da_vacio(), test_parse_elfo_linaje_hechizos_sin_duplicados() (+1 more)

### Community 96 - "_RngSi"
Cohesion: 0.14
Nodes (10): _RngSi, test_arcane_shot_se_aplica_una_sola_vez_por_turno(), test_arcane_shot_se_gasta_un_uso_al_aplicar(), test_daño_de_arcane_shot_es_2d6_antes_del_18(), _dado(), test_daño_de_arcane_shot_es_4d6_desde_el_18(), test_decision_de_impacto_no_gasta_el_uso_hasta_impactar(), test_piercing_gasta_el_uso_al_sustituir() (+2 more)

### Community 97 - "_clamp"
Cohesion: 0.12
Nodes (11): action_surge_uses(), _clamp(), extra_attacks_for(), fighter_extra_attacks_for(), indomitable_uses(), weapon_mastery_count(), test_extra_attacks_desde_nivel_5(), test_action_surge_usos_por_nivel_son_1_y_2() (+3 more)

### Community 99 - "_por_datos"
Cohesion: 0.21
Nodes (6): _por_datos(), _damage_type(), build_save_effect(), damage_dice_of(), damage_options(), damage_type_of()

### Community 100 - "attack_roll"
Cohesion: 0.25
Nodes (3): _actualizar_distancia(), attack_roll(), _mode_tag()

### Community 101 - "_RngExplota"
Cohesion: 0.25
Nodes (4): _RngExplota, test_interception_sin_arma_ni_escudo_no_actúa_y_no_consume_rng(), test_resolver_maestria_sin_maestria_no_consulta_tactical_master(), test_tactical_master_no_sustituye_bajo_el_nivel_9()

### Community 103 - "load_race"
Cohesion: 0.33
Nodes (5): load_race(), test_load_race_descarga_la_raza_y_sus_rasgos(), _rasgo(), _raza(), test_load_race_propaga_el_error_de_la_api()

### Community 104 - "_mode_tag"
Cohesion: 0.40
Nodes (4): _log_target(), _mode_tag(), _outcome_tag(), _log_line_outcome()

## Knowledge Gaps
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `_trait`, `inflict_damage`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `test_traits.py`, `_arquero`, `test_utility.py`, `test_wild_magic.py`, `test_ancestral_guardian.py`, `model/actions.py`, `apply_barbarian`, `test_zealot.py`, `test_death.py`, `Monster`, `test_magical.py`, `test_parry.py`, `test_superior_invisibility.py`, `test_undead_fortitude.py`, `test_arcane_archer.py`, `test_relentless.py`, `test_mastery.py`, `apply_condition`, `saves.py`, `test_area.py`, `random`, `Condition`, `main.py`, `test_checks_escapes.py`, `load_monster`, `Combatant`, `test_magic_resistance.py`, `test_regeneration.py`, `loader.py`, `legendary_parser.py`, `test_storm_herald.py`, `dnd_sim/__init__.py`, `test_pack_tactics.py`, `test_enlarge.py`, `test_fighter.py`, `spell_action`, `PlayerCharacter`, `AtaqueSustituido`, `test_azer.py`, `test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque`, `test_extra_damage.py`, `test_sustituir_ataque.py`, `apply_class`, `_RngSi`, `_por_datos`, `attack_roll`, `_RngExplota`, `test_sustitucion_hace_un_solo_par_de_picks`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `daño_base_arma()`) actually correct?**
  _`Attack` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `_trait` be split into smaller, more focused modules?**
  _Cohesion score 0.1380952380952381 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `inflict_damage`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `test_traits.py`, `test_utility.py`, `spell_parser.py`, `DamageTransfer`, `model/actions.py`, `ArcaneArcherFeatures`, `Monster`, `test_parry.py`, `test_superior_invisibility.py`, `test_skills.py`, `test_arcane_archer.py`, `test_mastery.py`, `BarbarianFeatures`, `apply_condition`, `saves.py`, `ability_check`, `test_checks_escapes.py`, `test_condition_immunities.py`, `Combatant`, `test_magic_resistance.py`, `loader.py`, `traits/__init__.py`, `test_storm_herald.py`, `RollMode`, `dnd_sim/__init__.py`, `test_pack_tactics.py`, `test_lair.py`, `ConditionInstance`, `test_enlarge.py`, `WildHeartFeatures`, `attempt_escapes`, `spell_action`, `PlayerCharacter`, `condition_parser.py`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 112 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 112 INFERRED edges - model-reasoned connections that need verification._
- **Should `inflict_damage` be split into smaller, more focused modules?**
  _Cohesion score 0.07853107344632769 - nodes in this community are weakly interconnected._
- **Why does `Abilities` connect `apply_condition` to `_trait`, `inflict_damage`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `test_traits.py`, `test_utility.py`, `test_wild_magic.py`, `test_ancestral_guardian.py`, `model/actions.py`, `apply_barbarian`, `test_martial_advantage.py`, `test_zealot.py`, `test_death.py`, `Monster`, `test_magical.py`, `test_parry.py`, `test_superior_invisibility.py`, `test_skills.py`, `test_undead_fortitude.py`, `test_arcane_archer.py`, `test_multiattack.py`, `test_relentless.py`, `test_mastery.py`, `saves.py`, `test_area.py`, `random`, `Condition`, `build_spell_actions`, `main.py`, `test_checks_escapes.py`, `load_monster`, `test_condition_immunities.py`, `Combatant`, `run_combat`, `test_magic_resistance.py`, `test_regeneration.py`, `loader.py`, `test_storm_herald.py`, `RollMode`, `test_backgrounds.py`, `Attack`, `dnd_sim/__init__.py`, `test_pack_tactics.py`, `test_races.py`, `test_enlarge.py`, `test_fighter.py`, `spell_action`, `PlayerCharacter`, `test_azer.py`, `test_extra_damage.py`, `test_sustituir_ataque.py`, `apply_class`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
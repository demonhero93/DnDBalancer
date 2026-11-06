# Graph Report - DnDBalancer  (2026-11-06)

## Corpus Check
- 219 files · ~175,074 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 3348 nodes · 12141 edges · 100 communities (87 shown, 13 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 749 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c88079c0`
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
- parse_spell
- test_traits.py
- combat/attack.py
- test_utility.py
- test_wild_magic.py
- Trait
- spell_parser.py
- Combatant
- simulate
- test_ancestral_guardian.py
- test_loader_actions.py
- CombatContext
- run_combat
- ActionUsage
- apply_barbarian
- test_martial_advantage.py
- ZealotFeatures
- test_zealot.py
- test_death.py
- json
- TurnResources
- attack_roll
- test_superior_invisibility.py
- fighter/features.py
- BeastFeatures
- test_skills.py
- trait_parser.py
- area.py
- test_multiattack.py
- valid_targets
- _duelo
- test_mastery.py
- BarbarianFeatures
- apply_condition
- conditions.py
- test_area.py
- random
- Condition
- dnd_sim/__init__.py
- _pj
- Regeneration
- test_checks_escapes.py
- load_monster
- _con_estilo
- saving_throw
- test_condition_immunities.py
- SaveResult
- WarriorHealAction
- test_magic_resistance.py
- begin_turn
- parse_escape
- traits/__init__.py
- legendary_parser.py
- test_storm_herald.py
- save_modifiers
- test_backgrounds.py
- test_spells.py
- Attack
- .on_turn_start
- pathlib
- BattleragerFeatures
- RollMode
- test_lair.py
- ConditionTracker
- tactics.py
- test_races.py
- test_enlarge.py
- loader.py
- Any
- _ctx_recursos
- Any
- casting.py
- Abilities
- TODO — DnDBalancer / dnd_sim
- _RngBajo
- AttackAction
- test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque
- condition_parser.py
- resolve_attack_range
- multiattack_parser.py
- race_parser.py
- background_parser.py
- Spellcasting
- load_race
- test_el_gancho_after_failed_check_desde_ability_check_con_ctx
- test_tactical_master_nivel_9_elige_entre_original_push_sap_slow
- test_sin_autoexito_ni_autofallo_en_pruebas

## God Nodes (most connected - your core abstractions)
1. `Attack` - 187 edges
2. `Condition` - 167 edges
3. `apply_condition()` - 150 edges
4. `Abilities` - 145 edges
5. `attack_roll()` - 138 edges
6. `load_monster()` - 135 edges
7. `AttackRange` - 131 edges
8. `PlayerCharacter` - 128 edges
9. `Monster` - 117 edges
10. `apply_barbarian()` - 96 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Fighter: cómo añadir una subclase` --references--> `SubclassDef`  [INFERRED]
  TODO.md → dnd_sim/rules/classes/base.py
- `Paquetes con fachada` --references--> `CombatResult`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/engine/combat/encounter.py
- `Carpetas` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py

## Import Cycles
- None detected.

## Communities (100 total, 13 thin omitted)

### Community 0 - "_trait"
Cohesion: 0.10
Nodes (39): second_wind_uses(), _check_fallada(), _ctx(), _fighter(), _objetivo(), _RngMax, _save_fallada(), _saving_nueva() (+31 more)

### Community 1 - "inflict_damage"
Cohesion: 0.05
Nodes (63): AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), _absorber_pv_temporales(), _hooks(), inflict_damage() (+55 more)

### Community 2 - "AttackRange"
Cohesion: 0.07
Nodes (56): AttackRange, RageAction, apply_berserker(), _armas_melee_de(), _de(), _furia_de(), _golpe_sin_armas(), IntimidatingPresenceAction (+48 more)

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
Cohesion: 0.16
Nodes (20): ability_check_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia() (+12 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.07
Nodes (59): legendary_phase(), LegendaryAction, _contexto(), _data(), _estado(), _legendaria(), _load(), _pj() (+51 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (66): WeaponAttackAction, _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll(), spy() (+58 more)

### Community 9 - "parse_spell"
Cohesion: 0.14
Nodes (27): parse_spell(), spell_action(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_daño_extra_del_hechizo_verdadero_no_baja_de_cinco() (+19 more)

### Community 10 - "test_traits.py"
Cohesion: 0.11
Nodes (24): attack_modifiers(), _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _RasgoDeSalvacion, _sahuagin() (+16 more)

### Community 11 - "combat/attack.py"
Cohesion: 0.08
Nodes (14): _agrandado(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), _piso_dados_rasgos(), _trigger_after_attack_roll(), _trigger_after_being_hit() (+6 more)

### Community 12 - "test_utility.py"
Cohesion: 0.18
Nodes (24): ConditionInstance, _abilities(), _ctx(), _mon(), _pj(), _siempre_falla(), test_actor_no_disponible_no_consulta_la_probabilidad(), test_agarrar_admite_hasta_un_tamano_mayor() (+16 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.13
Nodes (38): _abilities(), _barbaro(), _con_cola(), _con_efecto(), espia(), _ctx(), _furia(), _mon() (+30 more)

### Community 14 - "Trait"
Cohesion: 0.05
Nodes (5): Trait, BloodFrenzy, test_el_catalogo_cubre_hooks_que_los_rasgos_aun_no_usan(), test_hooks_con_un_nombre_fuera_del_catalogo_lanza_error(), test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 15 - "spell_parser.py"
Cohesion: 0.07
Nodes (16): Paquetes con fachada, _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla() (+8 more)

### Community 16 - "Combatant"
Cohesion: 0.07
Nodes (9): Arquitectura de `dnd_sim`, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, resolve_roll_mode(), Combatant, _mark_dead_if_down() (+1 more)

### Community 17 - "simulate"
Cohesion: 0.21
Nodes (9): print_report(), simulate(), build_parser(), _load_party(), main(), _parse_monster_token(), _guerrero_y_ogro(), test_danio_medio_por_combatiente_y_equipo() (+1 more)

### Community 18 - "test_ancestral_guardian.py"
Cohesion: 0.18
Nodes (26): _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado(), _escudo(), _esperado() (+18 more)

### Community 19 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (14): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+6 more)

### Community 20 - "CombatContext"
Cohesion: 0.08
Nodes (13): pick(), _reaccion_si_procede(), _tag_modificadores(), _nuevo_ctx(), actor_is_alive(), CombatContext, _en_accion_de_ataque(), _living_enemies() (+5 more)

### Community 21 - "run_combat"
Cohesion: 0.14
Nodes (14): CombatResult, _invoke_policy(), roll_initiative(), run_combat(), _run_combat(), _pasada(), _summarize_damage(), _agarrando() (+6 more)

### Community 22 - "ActionUsage"
Cohesion: 0.08
Nodes (25): ActionUsage, UsageKind, _breath(), _eventos(), _FixedRandom, _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos() (+17 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.06
Nodes (66): apply_barbarian(), apply_class(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj(), _resultado() (+58 more)

### Community 24 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 25 - "ZealotFeatures"
Cohesion: 0.07
Nodes (12): apply_zealot(), _de(), _en_60_pies(), _es_aliado(), _reserva_dados(), ZealotFeatures, ZealousPresenceAction, test_apply_anade_trait_y_dos_acciones_bonus() (+4 more)

### Community 26 - "test_zealot.py"
Cohesion: 0.12
Nodes (28): _furia_de(), _abilities(), _aliado(), _barbaro(), _decision(), _forma(), _presencia(), test_fanatical_decision_negativa_no_repiten() (+20 more)

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 28 - "json"
Cohesion: 0.15
Nodes (9): _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError (+1 more)

### Community 29 - "TurnResources"
Cohesion: 0.10
Nodes (20): TurnResources, _ctx(), _pj(), _spell_data(), _spellcasting(), test_ataque_con_magical_true_dana_completo_al_ghost(), test_bestial_solo_marca_las_armas_magicas_desde_el_nivel_6(), test_el_log_del_ataque_dice_dano_no_magico() (+12 more)

### Community 30 - "attack_roll"
Cohesion: 0.07
Nodes (60): D20Result, _actualizar_distancia(), attack_roll(), _mode_tag(), DamageRecorder, _ataque_melee(), _ataque_ranged(), _azer() (+52 more)

### Community 31 - "test_superior_invisibility.py"
Cohesion: 0.16
Nodes (19): _entradas(), parse_traits(), remove_invisibility_on_action(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd(), test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad(), test_el_umbral_se_saca_de_cada_descripcion(), _accion(), _ctx() (+11 more)

### Community 32 - "fighter/features.py"
Cohesion: 0.05
Nodes (17): action_surge_uses(), _clamp(), extra_attacks_for(), fighter_extra_attacks_for(), indomitable_uses(), rage_uses(), weapon_mastery_count(), AttackEntry (+9 more)

### Community 34 - "test_skills.py"
Cohesion: 0.11
Nodes (24): skill_bonus(), _abilities(), _ctx(), _load_fixture(), _pj(), _SoloMod, test_ability_check_no_suma_competencia_de_habilidad(), test_attempt_escapes_tira_la_habilidad() (+16 more)

### Community 35 - "trait_parser.py"
Cohesion: 0.20
Nodes (6): _declara_uso(), _usage(), parse_usage(), UnknownUsageError, test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 36 - "area.py"
Cohesion: 0.11
Nodes (8): AreaSaveAction, _log_target(), ConditionAction, RepeatSave, _mode_tag(), _outcome_tag(), _log_line_outcome(), test_la_resistencia_funciona_en_todas_las_rutas()

### Community 37 - "test_multiattack.py"
Cohesion: 0.11
Nodes (17): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+9 more)

### Community 38 - "valid_targets"
Cohesion: 0.10
Nodes (13): combat_finished(), living_teams(), _objetivo_enganche(), valid_targets(), _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos() (+5 more)

### Community 39 - "_duelo"
Cohesion: 0.15
Nodes (17): _ataque(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja(), test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_los_indicadores_estaticos_siguen_funcionando_y_se_combinan(), test_melee_or_ranged_consume_rng_siempre() (+9 more)

### Community 40 - "test_mastery.py"
Cohesion: 0.09
Nodes (29): al_acertar(), al_fallar(), _cd_topple(), consumir_marcas(), _log(), _nombre(), resolver_maestria(), _arma() (+21 more)

### Community 41 - "BarbarianFeatures"
Cohesion: 0.04
Nodes (22): BarbarianFeatures, ExtendRageAction, _rasgo(), AncestralGuardianFeatures, apply_ancestral_guardian(), apply_battlerager(), _nuevo_ataque(), SpikedArmorAction (+14 more)

### Community 42 - "apply_condition"
Cohesion: 0.11
Nodes (38): apply_condition(), end_turn(), _label(), _ctx(), _data(), _load(), _pj(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente() (+30 more)

### Community 43 - "conditions.py"
Cohesion: 0.06
Nodes (14): rage_damage(), roll_dice(), DamageType, parse_damage_type(), log_line(), CombatAction, _contexto(), _bolstering() (+6 more)

### Community 44 - "test_area.py"
Cohesion: 0.19
Nodes (23): sample(), AreaTargeting, select_area_targets(), _default_targeting(), SaveDamage, _area_action(), _ctx(), _npc() (+15 more)

### Community 45 - "random"
Cohesion: 0.11
Nodes (49): AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer(), _bj(), _ctx() (+41 more)

### Community 46 - "Condition"
Cohesion: 0.19
Nodes (26): Condition, test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+18 more)

### Community 47 - "dnd_sim/__init__.py"
Cohesion: 0.06
Nodes (18): ability_mod(), normalize_ability(), CombatState, d20(), roll_d20(), proficiency_bonus(), _clean(), normalize_skill() (+10 more)

### Community 48 - "_pj"
Cohesion: 0.22
Nodes (19): espia(), _espiar_divine(), _furia(), _mon(), _pj(), test_determinismo_misma_semilla_mismos_resultados(), corrida(), test_divine_fury_elige_radiante_con_pick() (+11 more)

### Community 49 - "Regeneration"
Cohesion: 0.13
Nodes (4): _es_radiante(), _guardar_salvacion(), Regeneration, Relentless

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.11
Nodes (38): ability_check(), attempt_escapes(), EscapeCheck, _check_fijo(), _fake(), _ctx(), _load(), _pj() (+30 more)

### Community 51 - "load_monster"
Cohesion: 0.10
Nodes (19): _armor_class_value(), load_monster(), _norm_name(), _parse_condition_immunities(), _parse_damage_modifiers(), test_una_condicion_desconocida_de_la_api_avisa(), test_fixture_sintetica_carga(), test_monstruo_no_legendario_no_carga_guaridas() (+11 more)

### Community 52 - "_con_estilo"
Cohesion: 0.15
Nodes (19): _aliado(), _con_estilo(), _enemigo(), _mods(), _RngExplota, _RngSi, test_interception_con_un_aliado_no_baja_de_cero_el_daño(), test_interception_no_actúa_con_la_reacción_gastada() (+11 more)

### Community 53 - "saving_throw"
Cohesion: 0.13
Nodes (12): _apply_condition_riders(), apply_save_damage(), _as_combat_context(), _avisar_fallo_salvacion(), _con_resistencia_legendaria(), _inflict_for_save(), _reaccion_si_procede(), registrar_resistencia() (+4 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.13
Nodes (15): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+7 more)

### Community 57 - "SaveResult"
Cohesion: 0.16
Nodes (19): SaveResult, fake_saving_throw(), falla(), espia(), stub(), stub(), _fallos(), _guarda_con() (+11 more)

### Community 59 - "WarriorHealAction"
Cohesion: 0.25
Nodes (15): WarriorHealAction, _accion(), _ctx(), test_fanatical_no_activo_sin_furia(), test_nivel_3_no_recibe_rasgos_superiores(), test_warrior_curacion_gasta_un_dado_y_suma_pv(), test_warrior_curacion_no_supera_el_maximo(), test_warrior_de_los_dioses_reserva_por_nivel() (+7 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.11
Nodes (24): _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab(), test_condition_action_de_hechizo_pasa_magical() (+16 more)

### Community 61 - "begin_turn"
Cohesion: 0.30
Nodes (14): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+6 more)

### Community 62 - "parse_escape"
Cohesion: 0.15
Nodes (8): has_escape_text(), parse_escape(), _skills_for(), _data(), test_el_fixture_de_la_constriccion_tiene_escape_y_avisa_de_grappled(), test_el_fixture_de_la_telaraña_carga_restrained_con_escape(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 63 - "traits/__init__.py"
Cohesion: 0.06
Nodes (12): DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante(), aliados_capaces(), _condicion_posicional() (+4 more)

### Community 64 - "legendary_parser.py"
Cohesion: 0.09
Nodes (14): parse_range_type(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary() (+6 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.06
Nodes (46): _aliados_en_aura(), apply_storm_herald(), _cd(), _dado_mar(), _de(), _en_aura(), _enemigos_en_aura(), _escalado() (+38 more)

### Community 66 - "save_modifiers"
Cohesion: 0.24
Nodes (9): save_modifiers(), _datos(), _lich(), _pj(), test_con_ventaja_acierta_mas_que_sin_ella(), test_da_ventaja_si_la_salvacion_es_de_conversion(), test_el_lich_carga_su_turn_resistance(), test_sin_el_tipo_de_efecto_no_aplica() (+1 more)

### Community 67 - "test_backgrounds.py"
Cohesion: 0.16
Nodes (17): Background, load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes(), test_apply_background_sin_competencias_es_inofensivo() (+9 more)

### Community 68 - "test_spells.py"
Cohesion: 0.10
Nodes (27): build_spell_actions(), SpellFixedDamageAction, _ctx(), _desde_fixture(), _monstruo_lanzador(), _npc(), _pj(), test_el_hechizado_ataca_a_los_de_su_propio_bando() (+19 more)

### Community 69 - "Attack"
Cohesion: 0.09
Nodes (41): Attack, apply_fighter(), maestria_de(), _abilities(), _firmas(), _pj(), _pj_con_armas(), test_apply_class_fighter_sin_subclase_equivalente_a_apply_fighter() (+33 more)

### Community 70 - ".on_turn_start"
Cohesion: 0.19
Nodes (3): _aliados_heridos(), _cd_ataque(), _en_10_pies()

### Community 71 - "pathlib"
Cohesion: 0.19
Nodes (6): Cómo comprobar que todo sigue en orden, _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api()

### Community 73 - "RollMode"
Cohesion: 0.19
Nodes (15): RollMode, _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj() (+7 more)

### Community 74 - "test_lair.py"
Cohesion: 0.08
Nodes (29): lair_phase(), LairAction, LegendaryState, _ctx(), _dragon(), _enemigo(), lairs_dir(), _orden_con() (+21 more)

### Community 76 - "tactics.py"
Cohesion: 0.38
Nodes (3): _extract(), first_target_policy(), random_policy()

### Community 77 - "test_races.py"
Cohesion: 0.15
Nodes (18): Race, parse_race(), _abilities(), _fiendish_legacy(), _keen_senses(), _pj(), test_apply_race_añade_competencias_fijas(), test_apply_race_con_habilidad_pedida() (+10 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.14
Nodes (25): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+17 more)

### Community 79 - "loader.py"
Cohesion: 0.10
Nodes (9): parse_attach_effects(), _damage_type(), build_condition_action(), build_save_action(), build_save_effect(), damage_dice_of(), damage_options(), damage_type_of() (+1 more)

### Community 80 - "Any"
Cohesion: 0.20
Nodes (5): _as_condition(), _condicion_bloqueada(), _contar(), _queda_accion(), remove_condition()

### Community 81 - "_ctx_recursos"
Cohesion: 0.48
Nodes (7): _action_surge(), _ctx_recursos(), test_action_surge_como_maximo_un_vez_por_turno(), test_action_surge_ejecutada_restaura_la_accion_y_gasta_un_uso(), test_action_surge_no_es_elegible_si_la_accion_no_se_ha_gastado(), test_action_surge_no_es_elegible_si_la_bonus_ya_se_gasto(), test_action_surge_no_es_elegible_sin_usos()

### Community 82 - "Any"
Cohesion: 0.11
Nodes (9): apply_wild_magic(), _cd(), _de(), _en_30_pies(), _enemigos(), _sombra(), WildMagicFeatures, WildSurgeAction (+1 more)

### Community 83 - "casting.py"
Cohesion: 0.09
Nodes (9): HealAction, SpellAction, SpellAttackAction, dado_por_nivel(), duracion_en_rondas(), apply_concentration(), HealEffect, StateEffect (+1 more)

### Community 84 - "Abilities"
Cohesion: 0.11
Nodes (27): Carpetas, Abilities, Monster, PlayerCharacter, apply_damage_modifiers(), _is_petrified(), _build_party(), test_sin_condiciones_el_dano_no_cambia() (+19 more)

### Community 85 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.25
Nodes (7): Fighter: cómo añadir una subclase, Fighter: pendientes reales, Grafo y verificación, Pendientes generales, Rutina sugerida al abrir sesión, TODO — DnDBalancer / dnd_sim, TODOs en código (marcados `# TODO`)

### Community 87 - "AttackAction"
Cohesion: 0.15
Nodes (9): _check_fields(), _construir(), _error(), load_lair(), AttackAction, SaveAction, test_esquema_invalido(), test_targeting_fuera_de_rango() (+1 more)

### Community 89 - "condition_parser.py"
Cohesion: 0.15
Nodes (6): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), ConditionEffect

### Community 90 - "resolve_attack_range"
Cohesion: 0.25
Nodes (8): resolve_attack_range(), _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

### Community 92 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (5): _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 94 - "race_parser.py"
Cohesion: 0.20
Nodes (3): _skill_name(), _spells_from_description(), _trait_skills()

### Community 96 - "Spellcasting"
Cohesion: 0.15
Nodes (7): parse_spellcasting(), Spellcasting, test_el_lanzador_se_lee_de_los_actions(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_la_curacion_usa_el_modificador_de_caracteristica_no_el_bono_completo(), test_un_hechizo_de_accion_bonus_se_comprueba_en_su_fase(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 99 - "load_race"
Cohesion: 0.33
Nodes (5): load_race(), test_load_race_descarga_la_raza_y_sus_rasgos(), _rasgo(), _raza(), test_load_race_propaga_el_error_de_la_api()

## Knowledge Gaps
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `inflict_damage`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `parse_spell`, `test_traits.py`, `combat/attack.py`, `test_utility.py`, `test_wild_magic.py`, `Combatant`, `simulate`, `test_ancestral_guardian.py`, `CombatContext`, `apply_barbarian`, `test_zealot.py`, `test_death.py`, `TurnResources`, `attack_roll`, `test_superior_invisibility.py`, `area.py`, `_duelo`, `test_mastery.py`, `BarbarianFeatures`, `apply_condition`, `conditions.py`, `random`, `Condition`, `dnd_sim/__init__.py`, `_pj`, `test_checks_escapes.py`, `load_monster`, `_con_estilo`, `test_magic_resistance.py`, `begin_turn`, `legendary_parser.py`, `test_storm_herald.py`, `test_spells.py`, `RollMode`, `test_enlarge.py`, `loader.py`, `casting.py`, `Abilities`, `AttackAction`, `test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque`, `resolve_attack_range`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `AttackRange`) actually correct?**
  _`Attack` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Should `_trait` be split into smaller, more focused modules?**
  _Cohesion score 0.10241545893719807 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `inflict_damage`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_legendary.py`, `test_beast.py`, `parse_spell`, `test_traits.py`, `combat/attack.py`, `test_utility.py`, `spell_parser.py`, `Combatant`, `run_combat`, `attack_roll`, `test_superior_invisibility.py`, `test_skills.py`, `test_mastery.py`, `BarbarianFeatures`, `apply_condition`, `conditions.py`, `dnd_sim/__init__.py`, `test_checks_escapes.py`, `load_monster`, `test_condition_immunities.py`, `test_magic_resistance.py`, `traits/__init__.py`, `test_storm_herald.py`, `save_modifiers`, `test_spells.py`, `RollMode`, `test_lair.py`, `ConditionTracker`, `test_enlarge.py`, `loader.py`, `Any`, `casting.py`, `Abilities`, `condition_parser.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 108 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 108 INFERRED edges - model-reasoned connections that need verification._
- **Should `inflict_damage` be split into smaller, more focused modules?**
  _Cohesion score 0.050793650793650794 - nodes in this community are weakly interconnected._
- **Why does `attack_roll()` connect `attack_roll` to `inflict_damage`, `test_giant.py`, `test_wild_heart.py`, `test_legendary.py`, `test_beast.py`, `parse_spell`, `test_traits.py`, `combat/attack.py`, `Combatant`, `test_ancestral_guardian.py`, `CombatContext`, `run_combat`, `test_martial_advantage.py`, `test_zealot.py`, `test_death.py`, `TurnResources`, `test_superior_invisibility.py`, `BeastFeatures`, `area.py`, `_duelo`, `test_mastery.py`, `apply_condition`, `conditions.py`, `Condition`, `dnd_sim/__init__.py`, `_pj`, `test_checks_escapes.py`, `saving_throw`, `test_magic_resistance.py`, `test_spells.py`, `Attack`, `test_enlarge.py`, `Abilities`, `resolve_attack_range`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
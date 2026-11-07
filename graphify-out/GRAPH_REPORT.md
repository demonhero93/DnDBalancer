# Graph Report - DnDBalancer  (2026-11-07)

## Corpus Check
- 221 files · ~181,669 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 3475 nodes · 12639 edges · 101 communities (82 shown, 19 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 788 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b5468875`
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
- test_spells.py
- RollMode
- Monster
- test_utility.py
- test_wild_magic.py
- Trait
- _elementos_por_nivel
- inflict_damage
- StormHeraldFeatures
- test_ancestral_guardian.py
- PlayerCharacter
- dnd_sim/__init__.py
- ArcaneArcherFeatures
- ActionUsage
- apply_barbarian
- test_martial_advantage.py
- ZealotFeatures
- test_zealot.py
- test_death.py
- _trait
- test_magical.py
- attack_roll
- test_superior_invisibility.py
- FighterFeatures
- BeastFeatures
- test_skills.py
- test_undead_fortitude.py
- ConditionAction
- test_multiattack.py
- _load
- test_relentless.py
- test_mastery.py
- BarbarianFeatures
- apply_condition
- pick
- test_area.py
- random
- Condition
- CheckResult
- build_spell_actions
- Regeneration
- test_checks_escapes.py
- load_monster
- _con_estilo
- saving_throw
- test_condition_immunities.py
- normalize_ability
- _ctx
- test_magic_resistance.py
- begin_turn
- parse_escape
- traits/__init__.py
- loader.py
- test_storm_herald.py
- save_modifiers
- test_backgrounds.py
- SpellFixedDamageAction
- Attack
- WorldTreeFeatures
- test_arquitectura.py
- barbarian/subclasses/__init__.py
- test_pack_tactics.py
- test_lair.py
- ConditionInstance
- tactics.py
- test_races.py
- test_enlarge.py
- _condicion_posicional
- Any
- test_fighter.py
- .alive
- spell_action
- apply_damage_modifiers
- NaturalWeapon
- _RngMax
- _estado
- test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque
- _dados_hasta
- check_modifiers
- _slot_table
- multiattack_parser.py
- barbarian/__init__.py
- _tabla_cantrip
- Background
- Spellcasting
- _contar
- test_resistance_probability_medio_convierte_about_50_por_ciento
- test_el_cli_tiene_las_opciones_legendarias
- test_el_gancho_after_failed_check_desde_ability_check_con_ctx

## God Nodes (most connected - your core abstractions)
1. `Attack` - 195 edges
2. `Condition` - 173 edges
3. `apply_condition()` - 152 edges
4. `Abilities` - 147 edges
5. `attack_roll()` - 142 edges
6. `Monster` - 141 edges
7. `AttackRange` - 139 edges
8. `load_monster()` - 135 edges
9. `PlayerCharacter` - 130 edges
10. `run_combat()` - 99 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Fighter: cómo añadir una subclase` --references--> `SubclassDef`  [INFERRED]
  TODO.md → dnd_sim/rules/classes/base.py
- `Fighter: pendientes reales` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py

## Import Cycles
- None detected.

## Communities (101 total, 19 thin omitted)

### Community 0 - "_trait"
Cohesion: 0.12
Nodes (34): second_wind_uses(), _check_fallada(), _ctx(), _fighter(), _mods(), _save_fallada(), _saving_nueva(), _second_wind() (+26 more)

### Community 1 - "test_attach.py"
Cohesion: 0.09
Nodes (32): parse_attach_effects(), Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), _atacar() (+24 more)

### Community 2 - "AttackRange"
Cohesion: 0.07
Nodes (55): AttackRange, RageAction, apply_berserker(), _de(), _furia_de(), _golpe_sin_armas(), IntimidatingPresenceAction, _abilities() (+47 more)

### Community 3 - "test_giant.py"
Cohesion: 0.08
Nodes (37): apply_giant(), _de(), GiantFeatures, MightyImpelAction, _objetivos_impel(), _orden_de(), _abilities(), _barbaro() (+29 more)

### Community 4 - "test_world_tree.py"
Cohesion: 0.11
Nodes (39): apply_world_tree(), _abilities(), _aliado(), _barbaro(), _ctx(), _decision(), _elige_candidato(), espia() (+31 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.08
Nodes (48): apply_wild_heart(), _con_beneficio(), _de(), _en_5_pies(), _hostil(), _orden_de(), WildHeartFeatures, _abilities() (+40 more)

### Community 6 - "test_proficiency.py"
Cohesion: 0.18
Nodes (20): ability_check_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia() (+12 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.09
Nodes (53): legendary_phase(), _contexto(), _data(), _legendaria(), _load(), _pj(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno() (+45 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (65): _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll(), spy(), _forma() (+57 more)

### Community 9 - "test_spells.py"
Cohesion: 0.13
Nodes (31): parse_spell(), _tipo_de_dano(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_daño_extra_del_hechizo_verdadero_no_baja_de_cinco() (+23 more)

### Community 10 - "RollMode"
Cohesion: 0.09
Nodes (26): RollMode, attack_modifiers(), _instancias(), _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba (+18 more)

### Community 11 - "Monster"
Cohesion: 0.05
Nodes (72): CombatState, TurnResources, Monster, apply_arcane_archer(), CurvingShotAction, _abilities(), _arco(), _arquero() (+64 more)

### Community 12 - "test_utility.py"
Cohesion: 0.13
Nodes (29): _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), hay_utilitaria_accion(), _orden_tamano(), _abilities(), _ctx() (+21 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.11
Nodes (42): apply_wild_magic(), _sombra(), WildSurgeAction, _abilities(), _barbaro(), _con_cola(), _con_efecto(), espia() (+34 more)

### Community 14 - "Trait"
Cohesion: 0.05
Nodes (3): Trait, BloodFrenzy, test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 16 - "inflict_damage"
Cohesion: 0.07
Nodes (13): parse_damage_type(), _absorber_pv_temporales(), _hooks(), inflict_damage(), _mark_dead_if_down(), _mitigacion_de_otros(), _notify_damage_dealt(), _notify_damage_taken() (+5 more)

### Community 17 - "StormHeraldFeatures"
Cohesion: 0.09
Nodes (8): _aliados_en_aura(), _cd(), _dado_mar(), _de(), _en_aura(), _enemigos_en_aura(), _escalado(), StormHeraldFeatures

### Community 18 - "test_ancestral_guardian.py"
Cohesion: 0.10
Nodes (28): AncestralGuardianFeatures, apply_ancestral_guardian(), _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado() (+20 more)

### Community 19 - "PlayerCharacter"
Cohesion: 0.07
Nodes (33): Carpetas, _tag_modificadores(), print_report(), simulate(), PlayerCharacter, build_parser(), _build_party(), _load_party() (+25 more)

### Community 20 - "dnd_sim/__init__.py"
Cohesion: 0.04
Nodes (39): DamageType, combat_finished(), living_teams(), _objetivo_enganche(), valid_targets(), resolve_roll_mode(), CombatResult, _invoke_policy() (+31 more)

### Community 21 - "ArcaneArcherFeatures"
Cohesion: 0.11
Nodes (4): proficiency_bonus(), ArcaneArcherFeatures, _de(), _otros_enemigos()

### Community 22 - "ActionUsage"
Cohesion: 0.08
Nodes (25): ActionUsage, UsageKind, _breath(), _eventos(), _FixedRandom, _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos() (+17 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.14
Nodes (28): rage_uses(), apply_barbarian(), _pj(), test_apply_anade_acciones_de_furia(), test_apply_extra_attack_sin_ataques_no_explota(), test_apply_extra_attack_sustituye_ataques_por_multiataque(), test_apply_feral_instinct_nivel_7(), test_apply_habilidad_fuera_de_lista_lanza_error() (+20 more)

### Community 24 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 25 - "ZealotFeatures"
Cohesion: 0.09
Nodes (9): apply_zealot(), _de(), _en_60_pies(), _es_aliado(), _reserva_dados(), ZealotFeatures, ZealousPresenceAction, test_apply_anade_trait_y_dos_acciones_bonus() (+1 more)

### Community 26 - "test_zealot.py"
Cohesion: 0.07
Nodes (77): _furia_de(), WarriorHealAction, _abilities(), _accion(), _aliado(), _barbaro(), _ctx(), _decision() (+69 more)

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 28 - "_trait"
Cohesion: 0.14
Nodes (15): CheckModifiers, SaveModifiers, _abilities(), test_brutal_strike_2d10_desde_nivel_17(), test_brutal_strike_renuncia_a_la_ventaja_y_paga_1d10(), test_brutal_strike_sin_fue_no_aplica(), test_danger_sense_da_ventaja_en_salvaciones_de_des(), test_danger_sense_no_funciona_incapacitado() (+7 more)

### Community 29 - "test_magical.py"
Cohesion: 0.16
Nodes (14): apply_beast(), _ctx(), _pj(), test_ataque_con_magical_true_dana_completo_al_ghost(), test_ataque_magico_contra_un_bárbaro_en_furia_se_reduce_a_la_mitad(), test_bestial_solo_marca_las_armas_magicas_desde_el_nivel_6(), test_inflict_damage_registra_la_bandera_magical(), test_las_armas_dinamicas_de_la_furia_heredan_el_flag() (+6 more)

### Community 30 - "attack_roll"
Cohesion: 0.06
Nodes (68): D20Result, _actualizar_distancia(), attack_roll(), _mode_tag(), DamageRecorder, HeatedBody, _ataque_melee(), _ataque_ranged() (+60 more)

### Community 31 - "test_superior_invisibility.py"
Cohesion: 0.16
Nodes (19): _entradas(), parse_traits(), remove_invisibility_on_action(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd(), test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad(), test_el_umbral_se_saca_de_cada_descripcion(), _accion(), _ctx() (+11 more)

### Community 32 - "FighterFeatures"
Cohesion: 0.09
Nodes (6): ActionSurgeAction, _contexto(), _en_5_pies(), FighterFeatures, _rasgo(), SecondWindAction

### Community 34 - "test_skills.py"
Cohesion: 0.08
Nodes (28): _clean(), normalize_skill(), skill_ability(), skill_bonus(), skill_check(), _abilities(), _ctx(), _load_fixture() (+20 more)

### Community 35 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 37 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 38 - "_load"
Cohesion: 0.15
Nodes (13): _data(), _load(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente(), test_el_ghoul_paraliza_con_diez_rondas_y_salvacion_de_repeticion(), test_el_hechizado_ahora_si_se_aplica(), test_el_lobo_derriba_con_la_salvacion_del_json(), test_el_lobo_no_derriba_si_el_ataque_falla(), test_el_lobo_solo_derriba_si_falla_la_salvacion() (+5 more)

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
Cohesion: 0.10
Nodes (46): Abilities, _apply_condition_riders(), apply_condition(), end_turn(), RepeatSave, _ataque(), _ctx(), _duelo() (+38 more)

### Community 43 - "pick"
Cohesion: 0.06
Nodes (14): arcane_shot_options_known(), arcane_shot_uses(), _clamp(), extra_attacks_for(), fighter_extra_attacks_for(), rage_damage(), weapon_mastery_count(), roll_dice() (+6 more)

### Community 44 - "test_area.py"
Cohesion: 0.08
Nodes (32): _check_fields(), _construir(), _error(), AreaSaveAction, AreaTargeting, select_area_targets(), _default_targeting(), SaveDamage (+24 more)

### Community 45 - "random"
Cohesion: 0.11
Nodes (49): AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer(), _bj(), _ctx() (+41 more)

### Community 46 - "Condition"
Cohesion: 0.19
Nodes (26): Condition, test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+18 more)

### Community 47 - "CheckResult"
Cohesion: 0.20
Nodes (6): _avisar_fallo_prueba(), CheckResult, _finish_check(), _guia(), _check_fijo(), _fake()

### Community 48 - "build_spell_actions"
Cohesion: 0.26
Nodes (8): _avisar(), build_spell_actions(), _desde_fixture(), _monstruo_lanzador(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_uso_propio(), test_un_hechizo_a_voluntad_se_puede_lanzar_en_cada_turno()

### Community 49 - "Regeneration"
Cohesion: 0.13
Nodes (3): _es_radiante(), Regeneration, Relentless

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.10
Nodes (38): ability_check(), attempt_escapes(), EscapeCheck, _ctx(), _data(), _load(), _pj(), test_con_dos_caracteristicas_se_elige_una_al_azar() (+30 more)

### Community 51 - "load_monster"
Cohesion: 0.06
Nodes (24): doblar_dados(), _cache_path(), get_background(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError, load_lair() (+16 more)

### Community 52 - "_con_estilo"
Cohesion: 0.14
Nodes (19): _aliado(), _con_estilo(), _enemigo(), _RngExplota, _RngSi, test_interception_con_un_aliado_no_baja_de_cero_el_daño(), test_interception_no_actúa_con_la_reacción_gastada(), test_interception_no_actúa_contra_un_no_aliado_ni_con_el_mismo_pj() (+11 more)

### Community 53 - "saving_throw"
Cohesion: 0.04
Nodes (39): d20(), roll_d20(), _agrandado(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), _piso_dados_rasgos() (+31 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.10
Nodes (18): ConditionEffect, test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats() (+10 more)

### Community 59 - "_ctx"
Cohesion: 0.22
Nodes (9): _ctx(), _resultado(), test_furia_persistente_15_no_decae_ni_termina_por_incapacitado(), test_furia_se_extiende_sola_si_forzo_salvacion(), test_furia_se_extiende_sola_si_hubo_ataque(), test_furia_termina_si_no_se_extendio(), test_relentless_rage_fallo_y_sin_furia(), test_relentless_rage_sube_pv_y_sube_el_cd() (+1 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.12
Nodes (24): _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab(), test_condition_action_de_hechizo_pasa_magical() (+16 more)

### Community 61 - "begin_turn"
Cohesion: 0.27
Nodes (15): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+7 more)

### Community 62 - "parse_escape"
Cohesion: 0.33
Nodes (4): parse_escape(), _skills_for(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 63 - "traits/__init__.py"
Cohesion: 0.09
Nodes (6): StateEffect, TurnResistance, MartialAdvantage, PackTactics, SuperiorInvisibility, UndeadFortitude

### Community 64 - "loader.py"
Cohesion: 0.03
Nodes (43): is_area_action(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), parse_range_type(), _sentence_with(), has_escape_text() (+35 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.12
Nodes (40): apply_storm_herald(), _abilities(), _aliado(), _barbaro(), _ctx(), _fijar_fallo_reaccion(), falla(), _fijar_salvacion() (+32 more)

### Community 66 - "save_modifiers"
Cohesion: 0.20
Nodes (10): _condiciones(), save_modifiers(), _datos(), _lich(), _pj(), test_con_ventaja_acierta_mas_que_sin_ella(), test_da_ventaja_si_la_salvacion_es_de_conversion(), test_el_lich_carga_su_turn_resistance() (+2 more)

### Community 67 - "test_backgrounds.py"
Cohesion: 0.16
Nodes (16): load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes(), test_apply_background_sin_competencias_es_inofensivo(), test_el_transfondo_no_toca_las_salvaciones() (+8 more)

### Community 68 - "SpellFixedDamageAction"
Cohesion: 0.15
Nodes (16): SpellFixedDamageAction, _ctx(), _npc(), _pj(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizado_invierte_los_objetivos_de_ataque(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado(), test_el_hechizo_verdadero_es_un_ataque_real_con_dano_extra() (+8 more)

### Community 69 - "Attack"
Cohesion: 0.10
Nodes (39): Attack, apply_fighter(), maestria_de(), _abilities(), _objetivo(), _pj(), _pj_con_armas(), test_apply_class_reenvía_el_estilo_de_combate() (+31 more)

### Community 71 - "test_arquitectura.py"
Cohesion: 0.13
Nodes (11): Arquitectura de `dnd_sim`, Cómo comprobar que todo sigue en orden, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, _capa(), _modulo_y_paquete() (+3 more)

### Community 72 - "barbarian/subclasses/__init__.py"
Cohesion: 0.09
Nodes (7): apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), SpikedArmorAction, BerserkerFeatures, StormAuraAction

### Community 73 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 74 - "test_lair.py"
Cohesion: 0.07
Nodes (33): lair_phase(), LairAction, LegendaryState, _ctx(), _dragon(), _enemigo(), lairs_dir(), _orden_con() (+25 more)

### Community 75 - "ConditionInstance"
Cohesion: 0.22
Nodes (3): ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 76 - "tactics.py"
Cohesion: 0.38
Nodes (3): _extract(), first_target_policy(), random_policy()

### Community 77 - "test_races.py"
Cohesion: 0.08
Nodes (29): Race, _get_entry(), get_race(), get_trait(), load_race(), parse_race(), _skill_name(), _spells_from_description() (+21 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.15
Nodes (24): _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj(), _spell_data() (+16 more)

### Community 80 - "Any"
Cohesion: 0.29
Nodes (4): _as_condition(), _condicion_bloqueada(), _label(), remove_condition()

### Community 81 - "test_fighter.py"
Cohesion: 0.09
Nodes (18): action_surge_uses(), indomitable_uses(), _action_surge(), _ctx_recursos(), _firmas(), _RngBajo, test_action_surge_como_maximo_un_vez_por_turno(), test_action_surge_ejecutada_restaura_la_accion_y_gasta_un_uso() (+10 more)

### Community 82 - ".alive"
Cohesion: 0.04
Nodes (18): _armas_melee_de(), _bolstering(), _cd(), _de(), _en_30_pies(), _enemigos(), _espiritu(), _flores() (+10 more)

### Community 83 - "spell_action"
Cohesion: 0.08
Nodes (17): Paquetes con fachada, _uso_de_entrada(), SaveAction, HealAction, SpellAttackAction, dado_por_nivel(), duracion_en_rondas(), Spell (+9 more)

### Community 84 - "apply_damage_modifiers"
Cohesion: 0.14
Nodes (13): apply_damage_modifiers(), _is_petrified(), _target(), test_immunity_zero(), test_invalid_damage_type_raises(), test_no_modifiers_unchanged(), test_resistance_halves_damage_floor(), test_resistance_then_vulnerability_same_type() (+5 more)

### Community 87 - "_estado"
Cohesion: 0.50
Nodes (3): _estado(), test_el_estado_legendario_rellena_gasta_y_reinicia(), test_use_probability_medio_se_usa_about_50_por_ciento()

### Community 90 - "check_modifiers"
Cohesion: 0.13
Nodes (12): _resolve_mods(), check_modifiers(), effective_ac(), resolve_attack_range(), _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto() (+4 more)

### Community 92 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (6): _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack(), AttackEntry

### Community 93 - "barbarian/__init__.py"
Cohesion: 0.11
Nodes (19): FormOfTheBeast, apply_class(), ClassDef, normalize_class_name(), register_class(), SubclassDef, _abilities(), _firmas() (+11 more)

### Community 95 - "Background"
Cohesion: 0.23
Nodes (3): Background, normalize_tool(), _add()

### Community 96 - "Spellcasting"
Cohesion: 0.18
Nodes (6): parse_spellcasting(), Spellcasting, test_el_lanzador_se_lee_de_los_actions(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_la_curacion_usa_el_modificador_de_caracteristica_no_el_bono_completo(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

## Knowledge Gaps
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `RollMode`, `Monster`, `test_utility.py`, `test_wild_magic.py`, `test_ancestral_guardian.py`, `PlayerCharacter`, `dnd_sim/__init__.py`, `apply_barbarian`, `test_zealot.py`, `test_death.py`, `_trait`, `test_magical.py`, `attack_roll`, `test_superior_invisibility.py`, `test_undead_fortitude.py`, `ConditionAction`, `test_relentless.py`, `test_mastery.py`, `apply_condition`, `pick`, `test_area.py`, `random`, `Condition`, `test_checks_escapes.py`, `load_monster`, `_con_estilo`, `saving_throw`, `test_magic_resistance.py`, `begin_turn`, `loader.py`, `test_storm_herald.py`, `SpellFixedDamageAction`, `barbarian/subclasses/__init__.py`, `test_pack_tactics.py`, `test_enlarge.py`, `test_fighter.py`, `spell_action`, `NaturalWeapon`, `test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque`, `check_modifiers`, `barbarian/__init__.py`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `AttackRange`) actually correct?**
  _`Attack` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Should `_trait` be split into smaller, more focused modules?**
  _Cohesion score 0.11794871794871795 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `RollMode`, `Monster`, `test_utility.py`, `inflict_damage`, `StormHeraldFeatures`, `PlayerCharacter`, `dnd_sim/__init__.py`, `ArcaneArcherFeatures`, `attack_roll`, `test_superior_invisibility.py`, `test_skills.py`, `test_mastery.py`, `BarbarianFeatures`, `apply_condition`, `pick`, `CheckResult`, `test_checks_escapes.py`, `saving_throw`, `test_condition_immunities.py`, `test_magic_resistance.py`, `traits/__init__.py`, `loader.py`, `test_storm_herald.py`, `save_modifiers`, `SpellFixedDamageAction`, `WorldTreeFeatures`, `barbarian/subclasses/__init__.py`, `test_pack_tactics.py`, `test_lair.py`, `ConditionInstance`, `test_enlarge.py`, `Any`, `spell_action`, `apply_damage_modifiers`, `check_modifiers`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Are the 112 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 112 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09288824383164006 - nodes in this community are weakly interconnected._
- **Why does `PlayerCharacter` connect `PlayerCharacter` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `RollMode`, `Monster`, `test_utility.py`, `test_wild_magic.py`, `test_ancestral_guardian.py`, `dnd_sim/__init__.py`, `ActionUsage`, `apply_barbarian`, `test_martial_advantage.py`, `test_zealot.py`, `test_death.py`, `test_magical.py`, `attack_roll`, `test_superior_invisibility.py`, `test_skills.py`, `test_undead_fortitude.py`, `test_multiattack.py`, `test_relentless.py`, `test_mastery.py`, `BarbarianFeatures`, `apply_condition`, `test_area.py`, `random`, `Condition`, `test_checks_escapes.py`, `load_monster`, `_con_estilo`, `test_condition_immunities.py`, `test_magic_resistance.py`, `begin_turn`, `test_storm_herald.py`, `save_modifiers`, `test_backgrounds.py`, `SpellFixedDamageAction`, `Attack`, `test_pack_tactics.py`, `test_lair.py`, `test_races.py`, `test_enlarge.py`, `test_fighter.py`, `spell_action`, `barbarian/__init__.py`, `Background`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
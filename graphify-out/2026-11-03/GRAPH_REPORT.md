# Graph Report - DnDBalancer  (2026-11-03)

## Corpus Check
- 204 files · ~141,841 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 2676 nodes · 9598 edges · 96 communities (85 shown, 11 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 570 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `371e9a44`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- loader.py
- test_attach.py
- AttackRange
- test_giant.py
- test_area.py
- test_enlarge.py
- TurnResources
- test_legendary.py
- test_beast.py
- test_spells.py
- RollMode
- test_parry.py
- test_utility.py
- main.py
- Trait
- spell_parser.py
- traits/__init__.py
- Abilities
- BarbarianFeatures
- test_loader_actions.py
- CombatContext
- ActionUsage
- test_barbarian.py
- AncestralGuardianFeatures
- saves.py
- stealth.py
- test_death.py
- json
- test_superior_invisibility.py
- Attack
- Combatant
- test_backgrounds.py
- BeastFeatures
- test_skills.py
- warnings
- test_lair.py
- StormHeraldFeatures
- dnd_sim/__init__.py
- Regeneration
- saving_throw
- barbarian/__init__.py
- test_conditions.py
- conditions.py
- pytest
- random
- Condition
- ability_check
- legendary.py
- ConditionInstance
- test_checks_escapes.py
- load_monster
- lair_loader.py
- SpellFixedDamageAction
- test_condition_immunities.py
- inflict_damage
- test_ancestral_guardian.py
- test_magic_resistance.py
- PlayerCharacter
- parse_escape
- Spellcasting
- ActionType
- test_storm_herald.py
- attack_roll
- legendary_phase
- condition_parser.py
- _duelo
- attach.py
- build_spell_actions
- run_combat
- test_pack_tactics.py
- _pj
- race_parser.py
- test_undead_fortitude.py
- test_races.py
- pathlib
- test_multiattack.py
- apply_condition
- roll_modifiers.py
- load_race
- spell_action
- normalize_skill
- TODO — DnDBalancer / dnd_sim
- background_parser.py
- _herald
- _FixedRandom
- SaveResult
- _duelo
- simulate
- ConditionAction
- apply_storm_herald
- HealEffect
- CheckModifiers

## God Nodes (most connected - your core abstractions)
1. `Attack` - 144 edges
2. `apply_condition()` - 144 edges
3. `Condition` - 143 edges
4. `load_monster()` - 135 edges
5. `Abilities` - 131 edges
6. `attack_roll()` - 128 edges
7. `PlayerCharacter` - 109 edges
8. `Monster` - 103 edges
9. `run_combat()` - 93 edges
10. `CombatContext` - 92 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Paquetes con fachada` --references--> `CombatResult`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/engine/combat/encounter.py
- `Carpetas` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py

## Import Cycles
- None detected.

## Communities (96 total, 11 thin omitted)

### Community 0 - "loader.py"
Cohesion: 0.08
Nodes (11): doblar_dados(), _damage_type(), _extract_multiattack_alternatives(), _norm_name(), _parse_condition_immunities(), _parse_damage_modifiers(), extract_multiattack_alternatives(), _norm_name() (+3 more)

### Community 1 - "test_attach.py"
Cohesion: 0.18
Nodes (25): _atacar(), _bite(), _cloaker(), _ctx(), _datos(), _pj(), test_con_ventaja_el_enganche_es_a_la_cabeza_y_ciega(), test_damage_transfer_no_aplica_sin_enganche() (+17 more)

### Community 2 - "AttackRange"
Cohesion: 0.07
Nodes (57): AttackRange, RageAction, apply_berserker(), _armas_melee_de(), BerserkerFeatures, _de(), _furia_de(), _golpe_sin_armas() (+49 more)

### Community 3 - "test_giant.py"
Cohesion: 0.08
Nodes (37): rage_damage(), apply_giant(), _de(), GiantFeatures, MightyImpelAction, _objetivos_impel(), _orden_de(), test_rage_damage_tabla_phb() (+29 more)

### Community 4 - "test_area.py"
Cohesion: 0.22
Nodes (22): AreaTargeting, select_area_targets(), _default_targeting(), SaveDamage, _area_action(), _ctx(), _npc(), _pj() (+14 more)

### Community 5 - "test_enlarge.py"
Cohesion: 0.17
Nodes (22): _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj(), _spell_data() (+14 more)

### Community 6 - "TurnResources"
Cohesion: 0.17
Nodes (14): TurnResources, _ctx(), _pj(), _spell_data(), _spellcasting(), test_ataque_con_magical_true_dana_completo_al_ghost(), test_bestial_solo_marca_las_armas_magicas_desde_el_nivel_6(), test_el_proyectil_magico_dana_completo_al_ghost() (+6 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.09
Nodes (32): _data(), _estado(), _legendaria(), _load(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_el_ala_que_mezcla_movimiento_avisa(), test_el_cantrip_del_lich_se_omite_con_aviso() (+24 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (67): WeaponAttackAction, apply_beast(), _habilitar_armas_naturales(), _abilities(), _barb(), _beast(), _ctx(), _en_furia() (+59 more)

### Community 9 - "test_spells.py"
Cohesion: 0.13
Nodes (30): parse_spell(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_daño_extra_del_hechizo_verdadero_no_baja_de_cinco(), test_el_lich_carga_sus_hechizos_utiles() (+22 more)

### Community 10 - "RollMode"
Cohesion: 0.10
Nodes (26): RollMode, _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _RasgoDeSalvacion, _sahuagin() (+18 more)

### Community 11 - "test_parry.py"
Cohesion: 0.15
Nodes (30): D20Result, _entradas(), parse_traits(), fijar(), espia(), _arquero_parry(), _ataque(), _ctx() (+22 more)

### Community 12 - "test_utility.py"
Cohesion: 0.12
Nodes (29): _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), hay_utilitaria_accion(), _orden_tamano(), _abilities(), _ctx() (+21 more)

### Community 13 - "main.py"
Cohesion: 0.27
Nodes (6): print_report(), build_parser(), _build_party(), _load_party(), main(), _parse_monster_token()

### Community 14 - "Trait"
Cohesion: 0.06
Nodes (3): Trait, BloodFrenzy, test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 15 - "spell_parser.py"
Cohesion: 0.09
Nodes (13): _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla(), _frases() (+5 more)

### Community 16 - "traits/__init__.py"
Cohesion: 0.07
Nodes (10): DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante(), aliados_capaces(), _condicion_posicional() (+2 more)

### Community 17 - "Abilities"
Cohesion: 0.08
Nodes (32): Abilities, Monster, apply_damage_modifiers(), _is_petrified(), test_inmovilizado_da_desventaja_solo_en_des(), test_las_condiciones_incapacitantes_fallan_fue_y_des_sin_tirar_dados(), test_las_condiciones_incapacitantes_no_fallan_automaticamente_la_con(), test_petrificado_tiene_resistencia_a_todo() (+24 more)

### Community 18 - "BarbarianFeatures"
Cohesion: 0.09
Nodes (5): BarbarianFeatures, ExtendRageAction, _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 19 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (14): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+6 more)

### Community 20 - "CombatContext"
Cohesion: 0.08
Nodes (14): pick(), valid_targets(), actor_is_alive(), CombatContext, _en_accion_de_ataque(), _living_enemies(), _log(), MultiattackAction (+6 more)

### Community 22 - "ActionUsage"
Cohesion: 0.15
Nodes (11): ActionUsage, UsageKind, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar(), test_per_day_dos_usos_y_luego_can_use_falso(), test_per_day_no_tira_recarga(), test_per_day_reset_restaura_todos_los_usos(), test_recharge_5_6_porcentaje_de_exito() (+3 more)

### Community 23 - "test_barbarian.py"
Cohesion: 0.09
Nodes (48): _clamp(), extra_attacks_for(), rage_uses(), apply_barbarian(), SaveModifiers, _abilities(), _ctx(), _pj() (+40 more)

### Community 25 - "saves.py"
Cohesion: 0.11
Nodes (14): _log_target(), registrar_resistencia_legendaria(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save(), _mode_tag(), _outcome_tag() (+6 more)

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 28 - "json"
Cohesion: 0.15
Nodes (9): _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError (+1 more)

### Community 29 - "test_superior_invisibility.py"
Cohesion: 0.36
Nodes (11): _accion(), _ctx(), _pixie(), _pj(), test_atacar_con_ventaja_y_no_pierde_la_invisibilidad(), test_ejecutarla_aplica_el_estado(), test_el_monstruo_recibe_su_accion_al_construirse(), test_lanzar_un_hechizo_tampoco_la_pierde() (+3 more)

### Community 30 - "Attack"
Cohesion: 0.05
Nodes (58): proficiency_bonus(), Attack, DamageRecorder, _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos() (+50 more)

### Community 31 - "Combatant"
Cohesion: 0.11
Nodes (4): CombatState, Combatant, _mark_dead_if_down(), _notify_damage_taken()

### Community 32 - "test_backgrounds.py"
Cohesion: 0.16
Nodes (17): Background, load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes(), test_apply_background_sin_competencias_es_inofensivo() (+9 more)

### Community 34 - "test_skills.py"
Cohesion: 0.13
Nodes (21): _abilities(), _ctx(), _load_fixture(), _pj(), _SoloMod, test_ability_check_no_suma_competencia_de_habilidad(), test_attempt_escapes_tira_la_habilidad(), test_caracteristica_asociada() (+13 more)

### Community 35 - "warnings"
Cohesion: 0.15
Nodes (8): _resistencia_legendaria(), _declara_uso(), _usage(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 36 - "test_lair.py"
Cohesion: 0.11
Nodes (16): lair_phase(), LairAction, LegendaryState, _ctx(), _enemigo(), lairs_dir(), _Stub, test_dos_acciones_uniformes() (+8 more)

### Community 37 - "StormHeraldFeatures"
Cohesion: 0.09
Nodes (8): _aliados_en_aura(), _cd(), _dado_mar(), _de(), _en_aura(), _enemigos_en_aura(), _escalado(), StormHeraldFeatures

### Community 38 - "dnd_sim/__init__.py"
Cohesion: 0.07
Nodes (18): ability_mod(), d20(), roll_d20(), sample(), combat_finished(), living_teams(), _objetivo_enganche(), CombatResult (+10 more)

### Community 39 - "Regeneration"
Cohesion: 0.11
Nodes (5): _es_radiante(), _guardar_salvacion(), Regeneration, Relentless, UndeadFortitude

### Community 40 - "saving_throw"
Cohesion: 0.20
Nodes (11): save_modifiers(), saving_throw(), test_resistance_probability_medio_convierte_about_50_por_ciento(), _datos(), _lich(), _pj(), test_con_ventaja_acierta_mas_que_sin_ella(), test_da_ventaja_si_la_salvacion_es_de_conversion() (+3 more)

### Community 41 - "barbarian/__init__.py"
Cohesion: 0.08
Nodes (10): apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), SpikedArmorAction, FormOfTheBeast, NaturalWeapon, ClassDef (+2 more)

### Community 42 - "test_conditions.py"
Cohesion: 0.13
Nodes (31): end_turn(), _ctx(), _data(), _load(), _pj(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente(), test_can_act_y_can_react(), test_condicion_fuera_del_enum_lanza_value_error() (+23 more)

### Community 43 - "conditions.py"
Cohesion: 0.09
Nodes (5): roll_dice(), DamageType, parse_damage_type(), log_line(), _contexto()

### Community 44 - "pytest"
Cohesion: 0.18
Nodes (16): apply_class(), normalize_class_name(), _abilities(), _firmas(), _pj(), test_apply_class_ancestral_equivalente_a_los_apply_suelto(), test_apply_class_battlerager_equivalente_a_los_apply_suelto(), test_apply_class_normaliza_el_nombre() (+8 more)

### Community 45 - "random"
Cohesion: 0.11
Nodes (49): AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer(), _bj(), _ctx() (+41 more)

### Community 46 - "Condition"
Cohesion: 0.19
Nodes (26): Condition, test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+18 more)

### Community 47 - "ability_check"
Cohesion: 0.12
Nodes (12): skill_ability(), ability_check(), ability_check_bonus(), CheckResult, _finish_check(), _guia(), _resolve_mods(), skill_bonus() (+4 more)

### Community 48 - "legendary.py"
Cohesion: 0.14
Nodes (9): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), legendary_resistance(), LegendaryAction (+1 more)

### Community 49 - "ConditionInstance"
Cohesion: 0.22
Nodes (3): ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.11
Nodes (37): attempt_escapes(), EscapeCheck, begin_turn(), _ctx(), _data(), _load(), _pj(), test_con_dos_caracteristicas_se_elige_una_al_azar() (+29 more)

### Community 51 - "load_monster"
Cohesion: 0.10
Nodes (23): _armor_class_value(), load_monster(), test_fixture_sintetica_carga(), test_monstruo_no_legendario_no_carga_guaridas(), test_monstruo_sin_fichero_no_avisa(), _load_fixture(), _ogre_data(), test_armor_class_as_list() (+15 more)

### Community 52 - "lair_loader.py"
Cohesion: 0.29
Nodes (5): _check_fields(), _construir(), _error(), load_lair(), test_targeting_fuera_de_rango()

### Community 53 - "SpellFixedDamageAction"
Cohesion: 0.16
Nodes (15): SpellFixedDamageAction, _ctx(), _npc(), _pj(), test_el_hechizado_invierte_los_objetivos_de_ataque(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado(), test_el_hechizo_verdadero_es_un_ataque_real_con_dano_extra(), test_el_proyectil_magico_pasa_por_los_modificadores_de_dano() (+7 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.12
Nodes (16): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+8 more)

### Community 57 - "inflict_damage"
Cohesion: 0.13
Nodes (19): _absorber_pv_temporales(), _hooks(), inflict_damage(), _mitigacion_de_otros(), _notify_damage_dealt(), _salvar_a_cero(), test_inflict_damage_registra_la_bandera_magical(), _ctx() (+11 more)

### Community 59 - "test_ancestral_guardian.py"
Cohesion: 0.18
Nodes (26): _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado(), _escudo(), _esperado() (+18 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.12
Nodes (23): ConditionEffect, test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa() (+15 more)

### Community 61 - "PlayerCharacter"
Cohesion: 0.26
Nodes (15): PlayerCharacter, _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+7 more)

### Community 62 - "parse_escape"
Cohesion: 0.25
Nodes (5): parse_escape(), _skills_for(), test_el_fixture_de_la_constriccion_tiene_escape_y_avisa_de_grappled(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 63 - "Spellcasting"
Cohesion: 0.16
Nodes (6): parse_spellcasting(), Spellcasting, test_el_hechizo_enlarge_es_un_estado_self(), test_el_lanzador_se_lee_de_los_actions(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 64 - "ActionType"
Cohesion: 0.06
Nodes (20): normalize_ability(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary() (+12 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.20
Nodes (23): _abilities(), _aliado(), _furia(), _mon(), _pj(), test_apply_class_registra_los_tres_entornos(), test_el_aura_de_la_tundra_da_pv_temporales_al_barbaro_y_aliados(), test_el_aura_del_desierto_escala_con_el_nivel() (+15 more)

### Community 66 - "attack_roll"
Cohesion: 0.10
Nodes (17): _actualizar_distancia(), _agrandado(), attack_roll(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), _mode_tag() (+9 more)

### Community 67 - "legendary_phase"
Cohesion: 0.17
Nodes (22): legendary_phase(), _contexto(), _pj(), test_con_una_sola_accion_asequible_pick_no_consume_rng(), test_dos_duenos_legendarios_actuan_cada_uno_una_vez(), test_el_combate_termina_en_medio_de_la_fase(), test_la_fase_ocurre_despues_del_end_turn(), test_no_actua_si_el_combate_ya_terminado() (+14 more)

### Community 68 - "condition_parser.py"
Cohesion: 0.12
Nodes (8): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), parse_range_type(), _sentence_with(), has_escape_text(), test_el_tipo_de_ataque_coincide_con_el_texto()

### Community 69 - "_duelo"
Cohesion: 0.14
Nodes (18): resolve_attack_range(), _ataque(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja(), test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_los_indicadores_estaticos_siguen_funcionando_y_se_combinan() (+10 more)

### Community 70 - "attach.py"
Cohesion: 0.13
Nodes (7): parse_attach_effects(), Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por()

### Community 71 - "build_spell_actions"
Cohesion: 0.29
Nodes (7): build_spell_actions(), _desde_fixture(), _monstruo_lanzador(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_uso_propio(), test_un_hechizo_a_voluntad_se_puede_lanzar_en_cada_turno()

### Community 72 - "run_combat"
Cohesion: 0.22
Nodes (12): run_combat(), _summarize_damage(), _eventos(), _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(), test_copias_de_un_monstruo_tienen_estado_independiente(), test_dos_combates_seguidos_empiezan_con_el_aliento_cargado() (+4 more)

### Community 73 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 74 - "_pj"
Cohesion: 0.18
Nodes (14): _dragon(), _orden_con(), _pj(), _spy_turnos(), spy(), test_guarida_pasa_magical_a_las_salvaciones(), test_puntos_siempre_incluyen_bonus_de_guarida(), test_reproducibilidad_con_guarida() (+6 more)

### Community 75 - "race_parser.py"
Cohesion: 0.20
Nodes (3): _skill_name(), _spells_from_description(), _trait_skills()

### Community 76 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 77 - "test_races.py"
Cohesion: 0.15
Nodes (18): Race, parse_race(), _abilities(), _fiendish_legacy(), _keen_senses(), _pj(), test_apply_race_añade_competencias_fijas(), test_apply_race_con_habilidad_pedida() (+10 more)

### Community 78 - "pathlib"
Cohesion: 0.06
Nodes (31): Arquitectura de `dnd_sim`, Carpetas, Cómo comprobar que todo sigue en orden, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, _capa() (+23 more)

### Community 79 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 80 - "apply_condition"
Cohesion: 0.13
Nodes (9): _apply_condition_riders(), apply_condition(), _as_condition(), _condicion_bloqueada(), _contar(), _label(), _queda_accion(), remove_condition() (+1 more)

### Community 81 - "roll_modifiers.py"
Cohesion: 0.20
Nodes (5): attack_modifiers(), check_modifiers(), _condiciones(), _hooks(), _instancias()

### Community 82 - "load_race"
Cohesion: 0.33
Nodes (5): load_race(), test_load_race_descarga_la_raza_y_sus_rasgos(), _rasgo(), _raza(), test_load_race_propaga_el_error_de_la_api()

### Community 83 - "spell_action"
Cohesion: 0.10
Nodes (13): Paquetes con fachada, _uso_de_entrada(), AttackAction, CombatAction, SaveAction, HealAction, SpellAction, SpellAttackAction (+5 more)

### Community 84 - "normalize_skill"
Cohesion: 0.22
Nodes (4): _clean(), normalize_skill(), test_normalize_skill_acepta_espacios_y_spanish(), test_normalize_skill_desconocida_lanza_value_error()

### Community 85 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.33
Nodes (5): Bloque 2026-10-30 (commiteado), Grafo y verificación, Rutina sugerida al abrir sesión, TODO — DnDBalancer / dnd_sim, TODOs en código (marcados `# TODO`)

### Community 87 - "_herald"
Cohesion: 0.29
Nodes (9): _barbaro(), _ctx(), _herald(), test_apply_anade_trait_y_accion(), test_el_aura_del_desierto_hace_dano_de_fuego_al_activarse(), test_el_aura_se_reactiva_con_la_accion_adicional(), test_la_accion_de_aura_no_esta_disponible_sin_enemigos(), test_storm_soul_da_la_resistencia_de_su_entorno() (+1 more)

### Community 88 - "_FixedRandom"
Cohesion: 0.22
Nodes (4): _breath(), _FixedRandom, test_begin_turn_no_tira_nada_si_estan_cargadas(), test_begin_turn_reinicia_recursos_y_tira_una_recarga_por_accion()

### Community 89 - "SaveResult"
Cohesion: 0.28
Nodes (7): SaveResult, fake_saving_throw(), _fijar_fallo_reaccion(), falla(), _fijar_salvacion(), espia(), test_raging_storm_no_dispara_sin_furia()

### Community 90 - "_duelo"
Cohesion: 0.31
Nodes (7): _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

### Community 91 - "simulate"
Cohesion: 0.29
Nodes (4): simulate(), test_con_use_probability_uno_el_danio_es_mayor_que_con_cero(), test_el_dragon_contra_un_grupo_usa_acciones_legendarias(), test_reproducibilidad_con_leyendas_y_resistencia()

### Community 93 - "apply_storm_herald"
Cohesion: 0.29
Nodes (4): apply_storm_herald(), StormAuraAction, test_apply_rechaza_entorno_desconocido(), test_apply_requiere_clase_barbara()

## Knowledge Gaps
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `loader.py`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_enlarge.py`, `TurnResources`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `RollMode`, `test_parry.py`, `test_utility.py`, `main.py`, `Abilities`, `CombatContext`, `test_barbarian.py`, `test_death.py`, `test_superior_invisibility.py`, `Combatant`, `dnd_sim/__init__.py`, `barbarian/__init__.py`, `test_conditions.py`, `conditions.py`, `pytest`, `random`, `Condition`, `test_checks_escapes.py`, `load_monster`, `lair_loader.py`, `SpellFixedDamageAction`, `inflict_damage`, `test_ancestral_guardian.py`, `test_magic_resistance.py`, `PlayerCharacter`, `ActionType`, `test_storm_herald.py`, `attack_roll`, `_duelo`, `test_pack_tactics.py`, `test_undead_fortitude.py`, `spell_action`, `_duelo`, `ConditionAction`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `AttackRange`) actually correct?**
  _`Attack` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Should `loader.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07816091954022988 - nodes in this community are weakly interconnected._
- **Why does `Abilities` connect `Abilities` to `loader.py`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_area.py`, `test_enlarge.py`, `TurnResources`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `RollMode`, `test_parry.py`, `test_utility.py`, `main.py`, `test_barbarian.py`, `test_death.py`, `test_superior_invisibility.py`, `Attack`, `Combatant`, `test_backgrounds.py`, `test_skills.py`, `dnd_sim/__init__.py`, `saving_throw`, `test_conditions.py`, `conditions.py`, `pytest`, `random`, `Condition`, `ability_check`, `test_checks_escapes.py`, `load_monster`, `SpellFixedDamageAction`, `test_condition_immunities.py`, `inflict_damage`, `test_ancestral_guardian.py`, `test_magic_resistance.py`, `PlayerCharacter`, `test_storm_herald.py`, `legendary_phase`, `_duelo`, `build_spell_actions`, `run_combat`, `test_pack_tactics.py`, `test_undead_fortitude.py`, `test_races.py`, `pathlib`, `test_multiattack.py`, `_duelo`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 90 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 90 INFERRED edges - model-reasoned connections that need verification._
- **Should `AttackRange` be split into smaller, more focused modules?**
  _Cohesion score 0.06869254341164453 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `loader.py`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_enlarge.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `RollMode`, `test_parry.py`, `test_utility.py`, `spell_parser.py`, `traits/__init__.py`, `Abilities`, `BarbarianFeatures`, `CombatContext`, `stealth.py`, `test_superior_invisibility.py`, `Attack`, `Combatant`, `test_skills.py`, `test_lair.py`, `StormHeraldFeatures`, `dnd_sim/__init__.py`, `saving_throw`, `test_conditions.py`, `conditions.py`, `ability_check`, `ConditionInstance`, `test_checks_escapes.py`, `SpellFixedDamageAction`, `test_condition_immunities.py`, `test_magic_resistance.py`, `Spellcasting`, `test_storm_herald.py`, `attack_roll`, `condition_parser.py`, `attach.py`, `test_pack_tactics.py`, `apply_condition`, `roll_modifiers.py`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
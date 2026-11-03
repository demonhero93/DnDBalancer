# Graph Report - DnDBalancer  (2026-11-03)

## Corpus Check
- 206 files · ~145,967 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 2758 nodes · 9940 edges · 87 communities (76 shown, 11 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 597 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1df57f09`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- multiattack_parser.py
- test_attach.py
- AttackRange
- test_giant.py
- test_area.py
- test_wild_heart.py
- test_proficiency.py
- test_legendary.py
- test_beast.py
- test_spells.py
- test_traits.py
- wild_heart.py
- test_utility.py
- main.py
- Trait
- spell_parser.py
- traits/__init__.py
- Abilities
- BarbarianFeatures
- test_loader_actions.py
- CombatContext
- BerserkerFeatures
- ActionUsage
- Attack
- test_martial_advantage.py
- saves.py
- _de
- test_death.py
- json
- utility.py
- attack_roll
- _mark_dead_if_down
- test_backgrounds.py
- BeastFeatures
- test_skills.py
- trait_parser.py
- LegendaryState
- StormHeraldFeatures
- Combatant
- Regeneration
- saving_throw
- dnd_sim/__init__.py
- apply_condition
- conditions.py
- _hooks
- random
- Condition
- ability_check
- legendary.py
- ConditionTracker
- test_checks_escapes.py
- load_monster
- AttackAction
- test_cache_avoids_second_network
- test_condition_immunities.py
- inflict_damage
- test_ancestral_guardian.py
- test_magic_resistance.py
- begin_turn
- parse_escape
- .can_react
- loader.py
- test_storm_herald.py
- roll_modifiers.py
- legendary_phase
- _ctx
- intentar_desenganche
- build_spell_actions
- test_usage.py
- RollMode
- test_lair.py
- race_parser.py
- test_undead_fortitude.py
- test_races.py
- test_arquitectura.py
- run_combat
- Any
- load_race
- spell_action
- TODO — DnDBalancer / dnd_sim
- background_parser.py
- _FixedRandom
- _duelo

## God Nodes (most connected - your core abstractions)
1. `Condition` - 153 edges
2. `Attack` - 149 edges
3. `apply_condition()` - 146 edges
4. `load_monster()` - 135 edges
5. `Abilities` - 133 edges
6. `attack_roll()` - 130 edges
7. `PlayerCharacter` - 113 edges
8. `Monster` - 105 edges
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

## Communities (87 total, 11 thin omitted)

### Community 0 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (6): _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack(), AttackEntry

### Community 1 - "test_attach.py"
Cohesion: 0.18
Nodes (25): _atacar(), _bite(), _cloaker(), _ctx(), _datos(), _pj(), test_con_ventaja_el_enganche_es_a_la_cabeza_y_ciega(), test_damage_transfer_no_aplica_sin_enganche() (+17 more)

### Community 2 - "AttackRange"
Cohesion: 0.10
Nodes (52): AttackRange, apply_berserker(), _golpe_sin_armas(), IntimidatingPresenceAction, _abilities(), _barbaro(), _berserker(), _ctx() (+44 more)

### Community 3 - "test_giant.py"
Cohesion: 0.07
Nodes (39): D20Result, apply_giant(), _de(), MightyImpelAction, _objetivos_impel(), _orden_de(), _abilities(), _barbaro() (+31 more)

### Community 4 - "test_area.py"
Cohesion: 0.11
Nodes (27): sample(), AreaTargeting, select_area_targets(), _default_targeting(), _area_action(), _ctx(), _npc(), _pj() (+19 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.15
Nodes (41): _abilities(), _aliado(), _barbaro(), _ctx(), _furia(), _mods(), _mon(), _pick_fijo() (+33 more)

### Community 6 - "test_proficiency.py"
Cohesion: 0.14
Nodes (20): proficiency_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia() (+12 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.09
Nodes (35): simulate(), _data(), _estado(), _load(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_con_use_probability_uno_el_danio_es_mayor_que_con_cero(), test_el_ala_que_mezcla_movimiento_avisa() (+27 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (67): WeaponAttackAction, apply_beast(), _habilitar_armas_naturales(), _abilities(), _barb(), _beast(), _ctx(), _en_furia() (+59 more)

### Community 9 - "test_spells.py"
Cohesion: 0.10
Nodes (44): parse_spell(), _ctx(), _npc(), _pj(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot() (+36 more)

### Community 10 - "test_traits.py"
Cohesion: 0.12
Nodes (22): attack_modifiers(), _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _sahuagin(), _sahuagin_con_rasgo() (+14 more)

### Community 11 - "wild_heart.py"
Cohesion: 0.12
Nodes (7): apply_wild_heart(), _con_beneficio(), _de(), _en_5_pies(), _hostil(), _orden_de(), WildHeartFeatures

### Community 12 - "test_utility.py"
Cohesion: 0.20
Nodes (23): ConditionInstance, ataque_utilitario(), _abilities(), _ctx(), _mon(), _pj(), _siempre_falla(), test_actor_no_disponible_no_consulta_la_probabilidad() (+15 more)

### Community 13 - "main.py"
Cohesion: 0.23
Nodes (6): print_report(), build_parser(), _build_party(), _load_party(), main(), _parse_monster_token()

### Community 14 - "Trait"
Cohesion: 0.05
Nodes (6): Attach, Trait, BloodFrenzy, test_el_catalogo_cubre_hooks_que_los_rasgos_aun_no_usan(), test_hooks_con_un_nombre_fuera_del_catalogo_lanza_error(), test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 15 - "spell_parser.py"
Cohesion: 0.09
Nodes (13): _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla(), _frases() (+5 more)

### Community 16 - "traits/__init__.py"
Cohesion: 0.06
Nodes (11): DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante(), aliados_capaces(), _condicion_posicional() (+3 more)

### Community 17 - "Abilities"
Cohesion: 0.10
Nodes (31): Abilities, Monster, PlayerCharacter, apply_damage_modifiers(), _is_petrified(), test_dos_combates_seguidos_empiezan_sin_condiciones(), test_inmovilizado_da_desventaja_solo_en_des(), test_la_politica_no_se_invoca_para_un_incapacitado() (+23 more)

### Community 18 - "BarbarianFeatures"
Cohesion: 0.09
Nodes (5): BarbarianFeatures, _contexto(), _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 19 - "test_loader_actions.py"
Cohesion: 0.18
Nodes (13): _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga(), test_ataque_con_usage_conserva_el_actionusage() (+5 more)

### Community 20 - "CombatContext"
Cohesion: 0.09
Nodes (14): pick(), _objetivo_enganche(), valid_targets(), ActionType, actor_is_alive(), CombatContext, _en_accion_de_ataque(), _living_enemies() (+6 more)

### Community 21 - "BerserkerFeatures"
Cohesion: 0.14
Nodes (4): _armas_melee_de(), BerserkerFeatures, _de(), _furia_de()

### Community 22 - "ActionUsage"
Cohesion: 0.15
Nodes (10): ActionUsage, UsageKind, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar(), test_per_day_dos_usos_y_luego_can_use_falso(), test_per_day_no_tira_recarga(), test_per_day_reset_restaura_todos_los_usos(), test_recharge_5_6_porcentaje_de_exito() (+2 more)

### Community 23 - "Attack"
Cohesion: 0.06
Nodes (70): Attack, apply_barbarian(), apply_class(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj() (+62 more)

### Community 24 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 25 - "saves.py"
Cohesion: 0.11
Nodes (15): _apply_condition_riders(), _log_target(), registrar_resistencia_legendaria(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save(), _mode_tag() (+7 more)

### Community 27 - "test_death.py"
Cohesion: 0.13
Nodes (18): combat_finished(), living_teams(), _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero() (+10 more)

### Community 28 - "json"
Cohesion: 0.15
Nodes (9): _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError (+1 more)

### Community 29 - "utility.py"
Cohesion: 0.17
Nodes (7): _agarrando(), _condiciones(), debe_usar_utilitaria(), DodgeAction, _orden_tamano(), test_p_medio_usa_utilitaria_a_la_frecuencia_configurada(), test_p_uno_siempre_decide_sin_consumir_rng()

### Community 30 - "attack_roll"
Cohesion: 0.05
Nodes (75): parse_traits(), _actualizar_distancia(), attack_roll(), _mode_tag(), remove_invisibility_on_action(), DamageRecorder, _ataque_melee(), _ataque_ranged() (+67 more)

### Community 32 - "test_backgrounds.py"
Cohesion: 0.16
Nodes (17): Background, load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes(), test_apply_background_sin_competencias_es_inofensivo() (+9 more)

### Community 34 - "test_skills.py"
Cohesion: 0.09
Nodes (27): normalize_skill(), skill_ability(), skill_bonus(), skill_check(), _abilities(), _ctx(), _load_fixture(), _pj() (+19 more)

### Community 35 - "trait_parser.py"
Cohesion: 0.13
Nodes (9): _resistencia_legendaria(), _declara_uso(), _entradas(), _usage(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo() (+1 more)

### Community 36 - "LegendaryState"
Cohesion: 0.14
Nodes (15): lair_phase(), LairAction, LegendaryState, _ctx(), _enemigo(), _Stub, test_dos_acciones_uniformes(), test_no_actua_si_el_combate_cae_en_medio() (+7 more)

### Community 37 - "StormHeraldFeatures"
Cohesion: 0.09
Nodes (7): _aliados_en_aura(), _cd(), _dado_mar(), _en_aura(), _enemigos_en_aura(), _escalado(), StormHeraldFeatures

### Community 38 - "Combatant"
Cohesion: 0.11
Nodes (11): resolve_roll_mode(), CombatResult, _invoke_policy(), roll_initiative(), _run_combat(), _nuevo_ctx(), _extract(), first_target_policy() (+3 more)

### Community 39 - "Regeneration"
Cohesion: 0.11
Nodes (5): _es_radiante(), _guardar_salvacion(), Regeneration, Relentless, UndeadFortitude

### Community 40 - "saving_throw"
Cohesion: 0.13
Nodes (14): _condiciones(), _instancias(), save_modifiers(), saving_throw(), _RasgoDeSalvacion, test_el_hook_de_salvaciones_alimenta_save_modifiers(), _datos(), _lich() (+6 more)

### Community 41 - "dnd_sim/__init__.py"
Cohesion: 0.05
Nodes (18): ExtendRageAction, RageAction, AncestralGuardianFeatures, apply_ancestral_guardian(), apply_battlerager(), BattleragerFeatures, _nuevo_ataque(), SpikedArmorAction (+10 more)

### Community 42 - "apply_condition"
Cohesion: 0.12
Nodes (29): apply_condition(), end_turn(), _label(), RepeatSave, _data(), _load(), _pj(), test_can_act_y_can_react() (+21 more)

### Community 43 - "conditions.py"
Cohesion: 0.06
Nodes (12): ability_mod(), _clamp(), extra_attacks_for(), rage_damage(), rage_uses(), CombatState, DamageType, parse_damage_type() (+4 more)

### Community 44 - "_hooks"
Cohesion: 0.38
Nodes (3): _hooks(), _mitigacion_de_otros(), _salvar_a_cero()

### Community 45 - "random"
Cohesion: 0.11
Nodes (49): AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer(), _bj(), _ctx() (+41 more)

### Community 46 - "Condition"
Cohesion: 0.08
Nodes (52): doblar_dados(), Condition, check_modifiers(), test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos() (+44 more)

### Community 47 - "ability_check"
Cohesion: 0.10
Nodes (14): ability_check(), ability_check_bonus(), CheckResult, _finish_check(), _guia(), _resolve_mods(), _check_fijo(), _fake() (+6 more)

### Community 48 - "legendary.py"
Cohesion: 0.13
Nodes (10): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), legendary_resistance(), LegendaryAction (+2 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.11
Nodes (34): attempt_escapes(), EscapeCheck, effective_ac(), _ctx(), _data(), _load(), _pj(), test_con_dos_caracteristicas_se_elige_una_al_azar() (+26 more)

### Community 51 - "load_monster"
Cohesion: 0.06
Nodes (35): _armor_class_value(), load_monster(), _norm_name(), _tag_modificadores(), MultiattackAction, test_fixture_sintetica_carga(), test_monstruo_no_legendario_no_carga_guaridas(), test_monstruo_sin_fichero_no_avisa() (+27 more)

### Community 52 - "AttackAction"
Cohesion: 0.10
Nodes (11): _check_fields(), _construir(), _error(), AttackAction, SaveAction, AreaSaveAction, ConditionAction, ConditionEffect (+3 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.12
Nodes (16): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+8 more)

### Community 57 - "inflict_damage"
Cohesion: 0.18
Nodes (16): _absorber_pv_temporales(), inflict_damage(), _notify_damage_dealt(), test_inflict_damage_registra_la_bandera_magical(), _ctx(), _datos(), _jabali(), _pj() (+8 more)

### Community 59 - "test_ancestral_guardian.py"
Cohesion: 0.18
Nodes (26): _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado(), _escudo(), _esperado() (+18 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.14
Nodes (21): _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab(), test_condition_action_de_hechizo_pasa_magical() (+13 more)

### Community 61 - "begin_turn"
Cohesion: 0.27
Nodes (15): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+7 more)

### Community 62 - "parse_escape"
Cohesion: 0.15
Nodes (6): _clean(), has_escape_text(), parse_escape(), _skills_for(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 64 - "loader.py"
Cohesion: 0.04
Nodes (31): normalize_ability(), is_area_action(), parse_attach_effects(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), parse_range_type() (+23 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.12
Nodes (41): SaveResult, fake_saving_throw(), _abilities(), _aliado(), _barbaro(), _ctx(), _fijar_fallo_reaccion(), falla() (+33 more)

### Community 66 - "roll_modifiers.py"
Cohesion: 0.08
Nodes (14): d20(), roll_d20(), roll_dice(), _agrandado(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque() (+6 more)

### Community 67 - "legendary_phase"
Cohesion: 0.17
Nodes (22): legendary_phase(), _contexto(), _pj(), test_con_una_sola_accion_asequible_pick_no_consume_rng(), test_dos_duenos_legendarios_actuan_cada_uno_una_vez(), test_el_combate_termina_en_medio_de_la_fase(), test_la_fase_ocurre_despues_del_end_turn(), test_no_actua_si_el_combate_ya_terminado() (+14 more)

### Community 69 - "_ctx"
Cohesion: 0.16
Nodes (20): resolve_attack_range(), _ataque(), _ctx(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja(), test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo(), test_dos_ventajas_y_una_desventaja_se_anulan() (+12 more)

### Community 70 - "intentar_desenganche"
Cohesion: 0.19
Nodes (5): AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por()

### Community 71 - "build_spell_actions"
Cohesion: 0.13
Nodes (11): build_spell_actions(), parse_spellcasting(), _desde_fixture(), _monstruo_lanzador(), test_el_lanzador_se_lee_de_los_actions(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_max_spell_level_limita_el_nivel_cargado() (+3 more)

### Community 72 - "test_usage.py"
Cohesion: 0.24
Nodes (10): _eventos(), _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(), test_copias_de_un_monstruo_tienen_estado_independiente(), test_dos_combates_seguidos_empiezan_con_el_aliento_cargado(), test_dragon_nunca_usa_el_aliento_dos_turnos_seguidos_sin_recarga(), test_politica_elige_el_aliento_aproximadamente_el_50_cuando_esta_cargado() (+2 more)

### Community 73 - "RollMode"
Cohesion: 0.19
Nodes (15): RollMode, _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj() (+7 more)

### Community 74 - "test_lair.py"
Cohesion: 0.11
Nodes (18): load_lair(), _dragon(), lairs_dir(), _orden_con(), _pj(), _spy_turnos(), spy(), test_esquema_invalido() (+10 more)

### Community 75 - "race_parser.py"
Cohesion: 0.20
Nodes (3): _skill_name(), _spells_from_description(), _trait_skills()

### Community 76 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 77 - "test_races.py"
Cohesion: 0.15
Nodes (18): Race, parse_race(), _abilities(), _fiendish_legacy(), _keen_senses(), _pj(), test_apply_race_añade_competencias_fijas(), test_apply_race_con_habilidad_pedida() (+10 more)

### Community 78 - "test_arquitectura.py"
Cohesion: 0.12
Nodes (12): Arquitectura de `dnd_sim`, Carpetas, Cómo comprobar que todo sigue en orden, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, _capa() (+4 more)

### Community 79 - "run_combat"
Cohesion: 0.18
Nodes (14): run_combat(), _summarize_damage(), _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso() (+6 more)

### Community 80 - "Any"
Cohesion: 0.29
Nodes (3): _condicion_bloqueada(), _contar(), _queda_accion()

### Community 82 - "load_race"
Cohesion: 0.33
Nodes (5): load_race(), test_load_race_descarga_la_raza_y_sus_rasgos(), _rasgo(), _raza(), test_load_race_propaga_el_error_de_la_api()

### Community 83 - "spell_action"
Cohesion: 0.08
Nodes (18): Paquetes con fachada, _uso_de_entrada(), CombatAction, HealAction, SpellAction, SpellAttackAction, SpellFixedDamageAction, SpellStateAction (+10 more)

### Community 85 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.33
Nodes (5): Bloque 2026-10-30 (commiteado), Grafo y verificación, Rutina sugerida al abrir sesión, TODO — DnDBalancer / dnd_sim, TODOs en código (marcados `# TODO`)

### Community 88 - "_FixedRandom"
Cohesion: 0.20
Nodes (5): _breath(), _FixedRandom, test_begin_turn_no_tira_nada_si_estan_cargadas(), test_begin_turn_reinicia_recursos_y_tira_una_recarga_por_accion(), test_recharge_recarga_con_5_o_mas_y_falla_con_4()

### Community 90 - "_duelo"
Cohesion: 0.31
Nodes (7): _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

## Knowledge Gaps
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Condition` connect `Condition` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `test_traits.py`, `wild_heart.py`, `test_utility.py`, `spell_parser.py`, `traits/__init__.py`, `Abilities`, `BarbarianFeatures`, `BerserkerFeatures`, `utility.py`, `attack_roll`, `test_skills.py`, `LegendaryState`, `StormHeraldFeatures`, `Combatant`, `saving_throw`, `dnd_sim/__init__.py`, `apply_condition`, `conditions.py`, `ability_check`, `ConditionTracker`, `test_checks_escapes.py`, `test_condition_immunities.py`, `test_magic_resistance.py`, `loader.py`, `test_storm_herald.py`, `roll_modifiers.py`, `intentar_desenganche`, `RollMode`, `test_lair.py`, `Any`, `spell_action`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 98 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 98 INFERRED edges - model-reasoned connections that need verification._
- **Should `AttackRange` be split into smaller, more focused modules?**
  _Cohesion score 0.1013116236996834 - nodes in this community are weakly interconnected._
- **Why does `Trait` connect `Trait` to `BeastFeatures`, `trait_parser.py`, `StormHeraldFeatures`, `Regeneration`, `saving_throw`, `dnd_sim/__init__.py`, `test_traits.py`, `conditions.py`, `wild_heart.py`, `traits/__init__.py`, `BarbarianFeatures`, `spell_action`, `BerserkerFeatures`, `test_condition_immunities.py`, `attack_roll`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `AttackRange`) actually correct?**
  _`Attack` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_giant.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07291666666666667 - nodes in this community are weakly interconnected._
- **Why does `Attack` connect `Attack` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `test_traits.py`, `test_utility.py`, `main.py`, `Abilities`, `CombatContext`, `test_death.py`, `attack_roll`, `Combatant`, `dnd_sim/__init__.py`, `apply_condition`, `conditions.py`, `random`, `Condition`, `test_checks_escapes.py`, `load_monster`, `AttackAction`, `inflict_damage`, `test_ancestral_guardian.py`, `test_magic_resistance.py`, `begin_turn`, `loader.py`, `test_storm_herald.py`, `roll_modifiers.py`, `_ctx`, `RollMode`, `test_undead_fortitude.py`, `spell_action`, `_duelo`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
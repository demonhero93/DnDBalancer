# Graph Report - DnDBalancer  (2026-11-04)

## Corpus Check
- 208 files · ~151,012 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 2864 nodes · 10333 edges · 92 communities (81 shown, 11 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 630 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5adca98c`
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
- WildHeartFeatures
- test_utility.py
- test_wild_magic.py
- Trait
- spell_parser.py
- traits/__init__.py
- Attack
- BarbarianFeatures
- test_loader_actions.py
- CombatContext
- wild_magic.py
- test_usage.py
- apply_barbarian
- Abilities
- saves.py
- subclasses/__init__.py
- test_death.py
- json
- test_magical.py
- attack_roll
- test_superior_invisibility.py
- test_backgrounds.py
- BeastFeatures
- test_skills.py
- warnings
- LegendaryState
- StormHeraldFeatures
- run_combat
- survival.py
- pathlib
- barbarian/__init__.py
- apply_condition
- model/actions.py
- loader.py
- TurnResources
- Condition
- ability_check
- legendary.py
- ConditionInstance
- test_checks_escapes.py
- load_monster
- lair_loader.py
- test_conditions.py
- test_condition_immunities.py
- inflict_damage
- test_ancestral_guardian.py
- test_magic_resistance.py
- test_regeneration.py
- parse_escape
- DamageTransfer
- legendary_parser.py
- test_storm_herald.py
- dnd_sim/__init__.py
- condition_parser.py
- Spellcasting
- _duelo
- AncestralGuardianFeatures
- build_spell_actions
- Arquitectura de `dnd_sim`
- RollMode
- test_lair.py
- race_parser.py
- test_undead_fortitude.py
- test_races.py
- test_enlarge.py
- test_multiattack.py
- Any
- ConditionAction
- load_race
- ActionType
- TODO — DnDBalancer / dnd_sim
- background_parser.py
- _estado
- test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio
- test_el_cli_tiene_las_opciones_legendarias
- _duelo
- test_orden_inmunidad_resistencia_vulnerabilidad_con_nonmagical

## God Nodes (most connected - your core abstractions)
1. `Condition` - 153 edges
2. `Attack` - 151 edges
3. `apply_condition()` - 146 edges
4. `Abilities` - 135 edges
5. `load_monster()` - 135 edges
6. `attack_roll()` - 130 edges
7. `PlayerCharacter` - 115 edges
8. `Monster` - 107 edges
9. `AttackRange` - 96 edges
10. `run_combat()` - 93 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Paquetes con fachada` --references--> `CombatResult`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/engine/combat/encounter.py
- `Carpetas` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py

## Import Cycles
- None detected.

## Communities (92 total, 11 thin omitted)

### Community 0 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (5): _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 1 - "test_attach.py"
Cohesion: 0.09
Nodes (32): parse_attach_effects(), Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), _atacar() (+24 more)

### Community 2 - "AttackRange"
Cohesion: 0.07
Nodes (55): AttackRange, RageAction, apply_berserker(), BerserkerFeatures, _de(), _furia_de(), _golpe_sin_armas(), IntimidatingPresenceAction (+47 more)

### Community 3 - "test_giant.py"
Cohesion: 0.07
Nodes (42): rage_damage(), D20Result, apply_giant(), _de(), GiantFeatures, MightyImpelAction, _objetivos_impel(), _orden_de() (+34 more)

### Community 4 - "test_area.py"
Cohesion: 0.22
Nodes (22): AreaTargeting, select_area_targets(), _default_targeting(), SaveDamage, _area_action(), _ctx(), _npc(), _pj() (+14 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.16
Nodes (39): _abilities(), _aliado(), _barbaro(), _ctx(), _furia(), _mods(), _mon(), _pick_fijo() (+31 more)

### Community 6 - "test_proficiency.py"
Cohesion: 0.14
Nodes (21): proficiency_bonus(), ability_check_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia() (+13 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.09
Nodes (53): legendary_phase(), _contexto(), _data(), _load(), _pj(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_con_una_sola_accion_asequible_pick_no_consume_rng() (+45 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (66): WeaponAttackAction, FormOfTheBeast, _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll() (+58 more)

### Community 9 - "test_spells.py"
Cohesion: 0.10
Nodes (44): parse_spell(), spell_action(), _ctx(), _npc(), _pj(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion() (+36 more)

### Community 10 - "test_traits.py"
Cohesion: 0.08
Nodes (27): attack_modifiers(), _condiciones(), _hooks(), _instancias(), _ataque_melee(), _ctx(), _datos(), _pj() (+19 more)

### Community 11 - "WildHeartFeatures"
Cohesion: 0.11
Nodes (9): apply_wild_heart(), _con_beneficio(), _de(), _en_5_pies(), _hostil(), _orden_de(), WildHeartFeatures, test_apply_anade_trait_sin_acciones() (+1 more)

### Community 12 - "test_utility.py"
Cohesion: 0.13
Nodes (28): _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), _orden_tamano(), _abilities(), _ctx(), _mon() (+20 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.09
Nodes (48): _log_target(), apply_wild_magic(), WildSurgeAction, _mode_tag(), _outcome_tag(), _log_line_outcome(), SaveResult, fake_saving_throw() (+40 more)

### Community 14 - "Trait"
Cohesion: 0.05
Nodes (6): hooks(), Trait, BloodFrenzy, test_el_catalogo_cubre_hooks_que_los_rasgos_aun_no_usan(), test_hooks_con_un_nombre_fuera_del_catalogo_lanza_error(), test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 15 - "spell_parser.py"
Cohesion: 0.08
Nodes (15): Paquetes con fachada, _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla() (+7 more)

### Community 16 - "traits/__init__.py"
Cohesion: 0.11
Nodes (5): aliados_capaces(), _condicion_posicional(), MartialAdvantage, PackTactics, SuperiorInvisibility

### Community 17 - "Attack"
Cohesion: 0.08
Nodes (33): print_report(), simulate(), Attack, PlayerCharacter, apply_damage_modifiers(), _is_petrified(), build_parser(), _build_party() (+25 more)

### Community 18 - "BarbarianFeatures"
Cohesion: 0.09
Nodes (5): BarbarianFeatures, ExtendRageAction, _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 19 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (14): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+6 more)

### Community 20 - "CombatContext"
Cohesion: 0.09
Nodes (11): _nuevo_ctx(), actor_is_alive(), CombatContext, _en_accion_de_ataque(), _living_enemies(), _log(), AreaSaveAction, HealAction (+3 more)

### Community 21 - "wild_magic.py"
Cohesion: 0.07
Nodes (13): _bolstering(), _cd(), _de(), _en_30_pies(), _enemigos(), _espiritu(), _flores(), _infusion() (+5 more)

### Community 22 - "test_usage.py"
Cohesion: 0.08
Nodes (25): ActionUsage, UsageKind, _breath(), _eventos(), _FixedRandom, _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos() (+17 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.07
Nodes (51): _clamp(), extra_attacks_for(), rage_uses(), MultiattackAction, apply_barbarian(), _habilitar_armas_naturales(), CheckModifiers, SaveModifiers (+43 more)

### Community 24 - "Abilities"
Cohesion: 0.23
Nodes (15): Abilities, _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio() (+7 more)

### Community 25 - "saves.py"
Cohesion: 0.12
Nodes (13): d20(), roll_d20(), roll_dice(), registrar_resistencia_legendaria(), apply_save_damage(), _as_combat_context(), _avisar_fallo_salvacion(), _inflict_for_save() (+5 more)

### Community 26 - "subclasses/__init__.py"
Cohesion: 0.12
Nodes (5): apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), SpikedArmorAction

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (15): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_daño_no_deja_los_pv_por_debajo_de_cero() (+7 more)

### Community 28 - "json"
Cohesion: 0.15
Nodes (9): _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError (+1 more)

### Community 29 - "test_magical.py"
Cohesion: 0.11
Nodes (21): _tag_modificadores(), AttackAction, SaveAction, apply_beast(), _ctx(), _pj(), _spell_data(), _spellcasting() (+13 more)

### Community 30 - "attack_roll"
Cohesion: 0.05
Nodes (66): _actualizar_distancia(), _agrandado(), attack_roll(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), _mode_tag() (+58 more)

### Community 31 - "test_superior_invisibility.py"
Cohesion: 0.16
Nodes (19): _entradas(), parse_traits(), remove_invisibility_on_action(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd(), test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad(), test_el_umbral_se_saca_de_cada_descripcion(), _accion(), _ctx() (+11 more)

### Community 32 - "test_backgrounds.py"
Cohesion: 0.16
Nodes (17): Background, load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes(), test_apply_background_sin_competencias_es_inofensivo() (+9 more)

### Community 34 - "test_skills.py"
Cohesion: 0.13
Nodes (21): _abilities(), _ctx(), _load_fixture(), _pj(), _SoloMod, test_ability_check_no_suma_competencia_de_habilidad(), test_attempt_escapes_tira_la_habilidad(), test_caracteristica_asociada() (+13 more)

### Community 35 - "warnings"
Cohesion: 0.12
Nodes (10): _resistencia_legendaria(), _parse_condition_immunities(), _parse_damage_modifiers(), _declara_uso(), _usage(), parse_usage(), UnknownUsageError, _warn() (+2 more)

### Community 36 - "LegendaryState"
Cohesion: 0.14
Nodes (14): lair_phase(), LairAction, LegendaryState, _ctx(), _enemigo(), _Stub, test_dos_acciones_uniformes(), test_no_actua_si_el_combate_cae_en_medio() (+6 more)

### Community 37 - "StormHeraldFeatures"
Cohesion: 0.07
Nodes (11): _armas_melee_de(), _aliados_en_aura(), apply_storm_herald(), _cd(), _dado_mar(), _de(), _en_aura(), _enemigos_en_aura() (+3 more)

### Community 38 - "run_combat"
Cohesion: 0.10
Nodes (13): combat_finished(), living_teams(), resolve_roll_mode(), CombatResult, _invoke_policy(), roll_initiative(), run_combat(), _run_combat() (+5 more)

### Community 39 - "survival.py"
Cohesion: 0.11
Nodes (5): _es_radiante(), _guardar_salvacion(), Regeneration, Relentless, UndeadFortitude

### Community 40 - "pathlib"
Cohesion: 0.18
Nodes (5): capa_de(), main(), visit_ImportFrom(), modulo_de(), resolver()

### Community 41 - "barbarian/__init__.py"
Cohesion: 0.11
Nodes (20): apply_ancestral_guardian(), NaturalWeapon, apply_class(), ClassDef, normalize_class_name(), register_class(), SubclassDef, _abilities() (+12 more)

### Community 42 - "apply_condition"
Cohesion: 0.14
Nodes (25): _apply_condition_riders(), Monster, apply_condition(), end_turn(), _label(), RepeatSave, _ctx(), _pj() (+17 more)

### Community 43 - "model/actions.py"
Cohesion: 0.08
Nodes (7): DamageType, parse_damage_type(), log_line(), _objetivo_enganche(), valid_targets(), AttackEntry, _contexto()

### Community 44 - "loader.py"
Cohesion: 0.13
Nodes (7): _damage_type(), _norm_name(), build_condition_action(), build_save_effect(), damage_dice_of(), damage_options(), damage_type_of()

### Community 45 - "TurnResources"
Cohesion: 0.10
Nodes (50): TurnResources, AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer(), _bj() (+42 more)

### Community 46 - "Condition"
Cohesion: 0.19
Nodes (26): Condition, test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+18 more)

### Community 47 - "ability_check"
Cohesion: 0.12
Nodes (12): _clean(), normalize_skill(), skill_ability(), ability_check(), CheckResult, _finish_check(), _guia(), _resolve_mods() (+4 more)

### Community 48 - "legendary.py"
Cohesion: 0.13
Nodes (10): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), legendary_resistance(), LegendaryAction (+2 more)

### Community 49 - "ConditionInstance"
Cohesion: 0.22
Nodes (3): ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.08
Nodes (42): attempt_escapes(), EscapeCheck, check_modifiers(), begin_turn(), _check_fijo(), _fake(), _ctx(), _data() (+34 more)

### Community 51 - "load_monster"
Cohesion: 0.10
Nodes (18): _armor_class_value(), load_monster(), ExtraDamage, _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper() (+10 more)

### Community 52 - "lair_loader.py"
Cohesion: 0.17
Nodes (8): _check_fields(), _construir(), _error(), load_lair(), ConditionEffect, test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), test_esquema_invalido(), test_targeting_fuera_de_rango()

### Community 53 - "test_conditions.py"
Cohesion: 0.16
Nodes (17): _data(), _load(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente(), test_el_ghoul_paraliza_con_diez_rondas_y_salvacion_de_repeticion(), test_el_hechizado_ahora_si_se_aplica(), test_el_lobo_derriba_con_la_salvacion_del_json(), test_el_lobo_no_derriba_si_el_ataque_falla(), test_el_lobo_solo_derriba_si_falla_la_salvacion() (+9 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.12
Nodes (16): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+8 more)

### Community 57 - "inflict_damage"
Cohesion: 0.10
Nodes (20): _absorber_pv_temporales(), _hooks(), inflict_damage(), _mark_dead_if_down(), _mitigacion_de_otros(), _notify_damage_dealt(), _notify_damage_taken(), _salvar_a_cero() (+12 more)

### Community 59 - "test_ancestral_guardian.py"
Cohesion: 0.18
Nodes (26): _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado(), _escudo(), _esperado() (+18 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.08
Nodes (34): save_modifiers(), _con_resistencia_legendaria(), saving_throw(), _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting() (+26 more)

### Community 61 - "test_regeneration.py"
Cohesion: 0.30
Nodes (13): _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno(), test_el_troll_carga_su_regeneracion() (+5 more)

### Community 62 - "parse_escape"
Cohesion: 0.22
Nodes (5): has_escape_text(), parse_escape(), _skills_for(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 63 - "DamageTransfer"
Cohesion: 0.12
Nodes (6): DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante()

### Community 64 - "legendary_parser.py"
Cohesion: 0.10
Nodes (13): parse_range_type(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary() (+5 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.12
Nodes (39): _abilities(), _aliado(), _barbaro(), _ctx(), _fijar_fallo_reaccion(), falla(), _fijar_salvacion(), espia() (+31 more)

### Community 66 - "dnd_sim/__init__.py"
Cohesion: 0.07
Nodes (9): ability_mod(), CombatState, pick(), sample(), _extract(), first_target_policy(), random_policy(), CombatantType (+1 more)

### Community 67 - "condition_parser.py"
Cohesion: 0.13
Nodes (6): normalize_ability(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with()

### Community 68 - "Spellcasting"
Cohesion: 0.13
Nodes (10): parse_spellcasting(), Spellcasting, _spell_data(), test_el_hechizo_enlarge_es_un_estado_self(), test_lanzar_el_hechizo_agranda_al_lanzador(), test_el_lanzador_se_lee_de_los_actions(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_la_curacion_usa_el_modificador_de_caracteristica_no_el_bono_completo() (+2 more)

### Community 69 - "_duelo"
Cohesion: 0.14
Nodes (18): resolve_attack_range(), _ataque(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja(), test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_los_indicadores_estaticos_siguen_funcionando_y_se_combinan() (+10 more)

### Community 71 - "build_spell_actions"
Cohesion: 0.23
Nodes (9): build_spell_actions(), test_un_lanzador_carga_el_hechizo_con_su_uso_propio(), _desde_fixture(), _monstruo_lanzador(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_la_reaccion_gasta_su_uso_propio(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_uso_propio() (+1 more)

### Community 72 - "Arquitectura de `dnd_sim`"
Cohesion: 0.25
Nodes (7): Arquitectura de `dnd_sim`, Carpetas, Cómo comprobar que todo sigue en orden, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia

### Community 73 - "RollMode"
Cohesion: 0.19
Nodes (15): RollMode, _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj() (+7 more)

### Community 74 - "test_lair.py"
Cohesion: 0.11
Nodes (19): _dragon(), lairs_dir(), _orden_con(), _pj(), _spy_turnos(), spy(), test_fixture_sintetica_carga(), test_guarida_pasa_magical_a_las_salvaciones() (+11 more)

### Community 75 - "race_parser.py"
Cohesion: 0.15
Nodes (9): parse_race(), _skill_name(), _spells_from_description(), _trait_skills(), _keen_senses(), test_parse_competencias_fijas_de_la_raza(), test_parse_descripcion_sin_hechizos_da_vacio(), test_parse_elfo_linaje_hechizos_sin_duplicados() (+1 more)

### Community 76 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 77 - "test_races.py"
Cohesion: 0.22
Nodes (12): Race, _abilities(), _fiendish_legacy(), _pj(), test_apply_race_añade_competencias_fijas(), test_apply_race_con_habilidad_pedida(), test_apply_race_habilidad_fuera_de_las_opciones_es_error(), test_apply_race_no_duplica_competencias_existentes() (+4 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.11
Nodes (26): doblar_dados(), _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api(), _accion(), _ataque() (+18 more)

### Community 79 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 80 - "Any"
Cohesion: 0.20
Nodes (5): _as_condition(), _condicion_bloqueada(), _contar(), _queda_accion(), remove_condition()

### Community 82 - "load_race"
Cohesion: 0.33
Nodes (5): load_race(), test_load_race_descarga_la_raza_y_sus_rasgos(), _rasgo(), _raza(), test_load_race_propaga_el_error_de_la_api()

### Community 83 - "ActionType"
Cohesion: 0.09
Nodes (13): ActionType, CombatAction, SpellAction, SpellAttackAction, SpellFixedDamageAction, dado_por_nivel(), duracion_en_rondas(), apply_concentration() (+5 more)

### Community 85 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.33
Nodes (5): Bloque 2026-10-30 (commiteado), Grafo y verificación, Rutina sugerida al abrir sesión, TODO — DnDBalancer / dnd_sim, TODOs en código (marcados `# TODO`)

### Community 87 - "_estado"
Cohesion: 0.50
Nodes (3): _estado(), test_el_estado_legendario_rellena_gasta_y_reinicia(), test_use_probability_medio_se_usa_about_50_por_ciento()

### Community 90 - "_duelo"
Cohesion: 0.31
Nodes (7): _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

## Knowledge Gaps
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Condition` connect `Condition` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_wild_heart.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `test_traits.py`, `WildHeartFeatures`, `test_utility.py`, `spell_parser.py`, `traits/__init__.py`, `Attack`, `BarbarianFeatures`, `saves.py`, `attack_roll`, `test_superior_invisibility.py`, `test_skills.py`, `warnings`, `LegendaryState`, `StormHeraldFeatures`, `run_combat`, `apply_condition`, `model/actions.py`, `loader.py`, `ability_check`, `ConditionInstance`, `test_checks_escapes.py`, `test_conditions.py`, `test_condition_immunities.py`, `test_magic_resistance.py`, `DamageTransfer`, `test_storm_herald.py`, `dnd_sim/__init__.py`, `condition_parser.py`, `Spellcasting`, `RollMode`, `test_lair.py`, `test_enlarge.py`, `Any`, `ActionType`, `.__post_init__`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 98 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 98 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09288824383164006 - nodes in this community are weakly interconnected._
- **Why does `Attack` connect `Attack` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `test_traits.py`, `test_utility.py`, `test_wild_magic.py`, `apply_barbarian`, `saves.py`, `subclasses/__init__.py`, `test_death.py`, `test_magical.py`, `attack_roll`, `test_superior_invisibility.py`, `run_combat`, `barbarian/__init__.py`, `model/actions.py`, `loader.py`, `TurnResources`, `Condition`, `test_checks_escapes.py`, `load_monster`, `lair_loader.py`, `test_conditions.py`, `inflict_damage`, `test_ancestral_guardian.py`, `test_magic_resistance.py`, `test_regeneration.py`, `legendary_parser.py`, `test_storm_herald.py`, `dnd_sim/__init__.py`, `_duelo`, `RollMode`, `test_undead_fortitude.py`, `test_enlarge.py`, `ActionType`, `test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio`, `_duelo`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `AttackRange`) actually correct?**
  _`Attack` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Should `AttackRange` be split into smaller, more focused modules?**
  _Cohesion score 0.07250341997264022 - nodes in this community are weakly interconnected._
- **Why does `Trait` connect `Trait` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_traits.py`, `WildHeartFeatures`, `spell_parser.py`, `traits/__init__.py`, `BarbarianFeatures`, `wild_magic.py`, `subclasses/__init__.py`, `test_superior_invisibility.py`, `BeastFeatures`, `warnings`, `StormHeraldFeatures`, `survival.py`, `model/actions.py`, `test_condition_immunities.py`, `DamageTransfer`, `dnd_sim/__init__.py`, `AncestralGuardianFeatures`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
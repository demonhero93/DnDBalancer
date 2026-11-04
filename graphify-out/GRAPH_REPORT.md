# Graph Report - DnDBalancer  (2026-11-04)

## Corpus Check
- 210 files · ~154,727 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 2938 nodes · 10633 edges · 102 communities (89 shown, 13 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 661 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `06ab7045`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- multiattack_parser.py
- test_attach.py
- AttackRange
- test_giant.py
- test_world_tree.py
- test_wild_heart.py
- test_proficiency.py
- test_legendary.py
- test_beast.py
- _spell_data
- RollMode
- combat/attack.py
- test_utility.py
- test_wild_magic.py
- Trait
- parse_spell
- traits/__init__.py
- Abilities
- BarbarianFeatures
- test_loader_actions.py
- CombatContext
- wild_magic.py
- run_combat
- apply_barbarian
- test_martial_advantage.py
- saves.py
- BattleragerFeatures
- test_death.py
- api_client.py
- spell_action
- test_extra_damage.py
- test_superior_invisibility.py
- test_backgrounds.py
- BeastFeatures
- test_skills.py
- trait_parser.py
- attack_roll
- test_area.py
- pick
- Regeneration
- random
- pytest
- test_conditions.py
- berserker.py
- loader.py
- test_battlerager.py
- Condition
- ability_check
- dnd_sim/__init__.py
- _pj
- test_checks_escapes.py
- load_monster
- model/actions.py
- warnings
- test_condition_immunities.py
- inflict_damage
- test_ancestral_guardian.py
- test_magic_resistance.py
- test_regeneration.py
- parse_escape
- DamageTransfer
- legendary_parser.py
- test_storm_herald.py
- roll_modifiers.py
- condition_parser.py
- test_spells.py
- Attack
- AncestralGuardianFeatures
- build_spell_actions
- pathlib
- test_pack_tactics.py
- test_lair.py
- race_parser.py
- test_undead_fortitude.py
- test_races.py
- test_enlarge.py
- test_azer.py
- conditions.py
- WildMagicFeatures
- load_race
- TurnResources
- Monster
- TODO — DnDBalancer / dnd_sim
- background_parser.py
- Combatant
- barbarian/__init__.py
- _trait
- _duelo
- test_relentless.py
- normalize_skill
- .on_turn_start
- WorldTreeFeatures
- roll_d20
- AreaSaveAction
- Spell
- normalize_ability
- SaveModifiers
- CheckModifiers

## God Nodes (most connected - your core abstractions)
1. `Attack` - 162 edges
2. `Condition` - 160 edges
3. `apply_condition()` - 148 edges
4. `Abilities` - 137 edges
5. `load_monster()` - 135 edges
6. `attack_roll()` - 130 edges
7. `PlayerCharacter` - 118 edges
8. `Monster` - 109 edges
9. `AttackRange` - 107 edges
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

## Communities (102 total, 13 thin omitted)

### Community 0 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (6): _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack(), AttackEntry

### Community 1 - "test_attach.py"
Cohesion: 0.09
Nodes (32): parse_attach_effects(), Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), _atacar() (+24 more)

### Community 2 - "AttackRange"
Cohesion: 0.07
Nodes (57): AttackRange, RageAction, apply_berserker(), _armas_melee_de(), BerserkerFeatures, _de(), _furia_de(), _golpe_sin_armas() (+49 more)

### Community 3 - "test_giant.py"
Cohesion: 0.08
Nodes (37): apply_giant(), _de(), GiantFeatures, MightyImpelAction, _objetivos_impel(), _orden_de(), _abilities(), _barbaro() (+29 more)

### Community 4 - "test_world_tree.py"
Cohesion: 0.14
Nodes (26): _abilities(), _aliado(), _barbaro(), _ctx(), _elige_candidato(), espia(), _furia(), _pj() (+18 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.08
Nodes (48): apply_wild_heart(), _con_beneficio(), _de(), _en_5_pies(), _hostil(), _orden_de(), WildHeartFeatures, _abilities() (+40 more)

### Community 6 - "test_proficiency.py"
Cohesion: 0.17
Nodes (20): proficiency_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia() (+12 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.05
Nodes (70): ConditionAction, legendary_phase(), saving_throw(), _contexto(), _data(), _estado(), _legendaria(), _load() (+62 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (65): WeaponAttackAction, _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll(), spy() (+57 more)

### Community 9 - "_spell_data"
Cohesion: 0.12
Nodes (18): _spell_data(), _spellcasting(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_daño_extra_del_hechizo_verdadero_no_baja_de_cinco(), test_el_lich_carga_sus_hechizos_utiles(), test_el_tiempo_de_casteo_marca_el_tipo_de_accion(), test_las_ilusiones_sin_estado_en_el_rival_se_ignoran() (+10 more)

### Community 10 - "RollMode"
Cohesion: 0.10
Nodes (26): RollMode, resolve_roll_mode(), attack_modifiers(), _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba (+18 more)

### Community 11 - "combat/attack.py"
Cohesion: 0.10
Nodes (15): _actualizar_distancia(), _agrandado(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), _mode_tag(), _reaccion_si_procede() (+7 more)

### Community 12 - "test_utility.py"
Cohesion: 0.08
Nodes (31): ConditionInstance, ConditionTracker, _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), hay_utilitaria_accion(), _orden_tamano() (+23 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.10
Nodes (47): _log_target(), _mode_tag(), _outcome_tag(), _log_line_outcome(), SaveResult, fake_saving_throw(), _abilities(), _barbaro() (+39 more)

### Community 15 - "parse_spell"
Cohesion: 0.09
Nodes (16): _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla(), _frases() (+8 more)

### Community 16 - "traits/__init__.py"
Cohesion: 0.11
Nodes (6): aliados_capaces(), BloodFrenzy, _condicion_posicional(), MartialAdvantage, PackTactics, SuperiorInvisibility

### Community 17 - "Abilities"
Cohesion: 0.10
Nodes (21): Abilities, print_report(), simulate(), PlayerCharacter, build_parser(), _build_party(), _load_party(), main() (+13 more)

### Community 18 - "BarbarianFeatures"
Cohesion: 0.10
Nodes (5): BarbarianFeatures, ExtendRageAction, _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 19 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (14): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+6 more)

### Community 20 - "CombatContext"
Cohesion: 0.13
Nodes (8): _objetivo_enganche(), valid_targets(), _nuevo_ctx(), actor_is_alive(), CombatContext, HealAction, _romper_invisibilidad_al_lanzar(), SpellStateAction

### Community 21 - "wild_magic.py"
Cohesion: 0.10
Nodes (15): log_line(), apply_wild_magic(), _bolstering(), _cd(), _de(), _en_30_pies(), _enemigos(), _espiritu() (+7 more)

### Community 22 - "run_combat"
Cohesion: 0.06
Nodes (39): run_combat(), _summarize_damage(), ActionUsage, UsageKind, _data(), _load(), _pj(), _raw_multiattack() (+31 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.14
Nodes (31): rage_uses(), apply_barbarian(), _ctx(), _pj(), _resultado(), test_apply_anade_acciones_de_furia(), test_apply_extra_attack_sin_ataques_no_explota(), test_apply_extra_attack_sustituye_ataques_por_multiataque() (+23 more)

### Community 24 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 25 - "saves.py"
Cohesion: 0.15
Nodes (11): registrar_resistencia_legendaria(), apply_save_damage(), _as_combat_context(), _avisar_fallo_salvacion(), _con_resistencia_legendaria(), _inflict_for_save(), _reaccion_si_procede(), registrar_resistencia() (+3 more)

### Community 26 - "BattleragerFeatures"
Cohesion: 0.14
Nodes (5): apply_battlerager(), BattleragerFeatures, _de(), SpikedArmorAction, test_apply_exige_clase_barbaro()

### Community 27 - "test_death.py"
Cohesion: 0.14
Nodes (18): CombatAction, SpellFixedDamageAction, _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero() (+10 more)

### Community 28 - "api_client.py"
Cohesion: 0.14
Nodes (9): _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError (+1 more)

### Community 29 - "spell_action"
Cohesion: 0.16
Nodes (14): AttackAction, SaveAction, spell_action(), _spell_data(), test_el_hechizo_enlarge_es_un_estado_self(), test_lanzar_el_hechizo_agranda_al_lanzador(), _spellcasting(), test_un_cantrip_de_ataque_construye_un_ataque_magico() (+6 more)

### Community 30 - "test_extra_damage.py"
Cohesion: 0.18
Nodes (17): DamageRecorder, _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional() (+9 more)

### Community 31 - "test_superior_invisibility.py"
Cohesion: 0.20
Nodes (17): parse_traits(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd(), test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad(), test_el_umbral_se_saca_de_cada_descripcion(), _accion(), _ctx(), _pixie(), _pj() (+9 more)

### Community 32 - "test_backgrounds.py"
Cohesion: 0.16
Nodes (17): Background, load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes(), test_apply_background_sin_competencias_es_inofensivo() (+9 more)

### Community 34 - "test_skills.py"
Cohesion: 0.13
Nodes (21): _abilities(), _ctx(), _load_fixture(), _pj(), _SoloMod, test_ability_check_no_suma_competencia_de_habilidad(), test_attempt_escapes_tira_la_habilidad(), test_caracteristica_asociada() (+13 more)

### Community 35 - "trait_parser.py"
Cohesion: 0.15
Nodes (8): _resistencia_legendaria(), _declara_uso(), _entradas(), _usage(), parse_usage(), UnknownUsageError, test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 36 - "attack_roll"
Cohesion: 0.28
Nodes (20): attack_roll(), _arquero_parry(), _ataque(), _ctx(), _datos(), _fijar_d20(), _gladiador(), _pj() (+12 more)

### Community 37 - "test_area.py"
Cohesion: 0.05
Nodes (36): sample(), AreaTargeting, select_area_targets(), _aliados_en_aura(), _cd(), _dado_mar(), _de(), _en_aura() (+28 more)

### Community 38 - "pick"
Cohesion: 0.13
Nodes (11): pick(), combat_finished(), living_teams(), CombatResult, _invoke_policy(), roll_initiative(), _run_combat(), _extract() (+3 more)

### Community 39 - "Regeneration"
Cohesion: 0.10
Nodes (5): _es_radiante(), _guardar_salvacion(), Regeneration, Relentless, UndeadFortitude

### Community 40 - "random"
Cohesion: 0.25
Nodes (18): _abilities(), _ctx(), _decide(), _pj(), test_antes_del_nivel_2_no_hay_decision_ni_rng(), test_en_turno_ajeno_no_decide(), test_frecuencia_0_5_es_aproximadamente_la_mitad_de_los_turnos(), test_las_reacciones_no_deciden_ni_reciben() (+10 more)

### Community 41 - "pytest"
Cohesion: 0.22
Nodes (15): apply_ancestral_guardian(), apply_class(), _abilities(), _firmas(), _pj(), test_apply_class_ancestral_equivalente_a_los_apply_suelto(), test_apply_class_battlerager_equivalente_a_los_apply_suelto(), test_apply_class_normaliza_el_nombre() (+7 more)

### Community 42 - "test_conditions.py"
Cohesion: 0.08
Nodes (52): end_turn(), _ataque(), _ctx(), _data(), _duelo(), _load(), _pj(), _tasa_de_impacto() (+44 more)

### Community 43 - "berserker.py"
Cohesion: 0.07
Nodes (9): _clamp(), extra_attacks_for(), rage_damage(), roll_dice(), DamageType, parse_damage_type(), _contexto(), FormOfTheBeast (+1 more)

### Community 44 - "loader.py"
Cohesion: 0.13
Nodes (6): _damage_type(), build_condition_action(), build_save_effect(), damage_dice_of(), damage_options(), damage_type_of()

### Community 45 - "test_battlerager.py"
Cohesion: 0.22
Nodes (30): AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer(), _bj(), _ctx() (+22 more)

### Community 46 - "Condition"
Cohesion: 0.20
Nodes (27): apply_condition(), Condition, _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+19 more)

### Community 47 - "ability_check"
Cohesion: 0.12
Nodes (13): skill_ability(), ability_check(), ability_check_bonus(), CheckResult, _finish_check(), _guia(), _resolve_mods(), skill_bonus() (+5 more)

### Community 48 - "dnd_sim/__init__.py"
Cohesion: 0.08
Nodes (12): ability_mod(), CombatState, CombatantType, _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia() (+4 more)

### Community 49 - "_pj"
Cohesion: 0.15
Nodes (17): _ctx(), _npc(), _pj(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizado_invierte_los_objetivos_de_ataque(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado(), test_el_hechizo_verdadero_es_un_ataque_real_con_dano_extra() (+9 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.11
Nodes (37): attempt_escapes(), EscapeCheck, begin_turn(), _ctx(), _data(), _load(), _pj(), test_con_dos_caracteristicas_se_elige_una_al_azar() (+29 more)

### Community 51 - "load_monster"
Cohesion: 0.07
Nodes (35): _armor_class_value(), load_monster(), _norm_name(), _tag_modificadores(), apply_beast(), _load_fixture(), _ogre_data(), test_armor_class_as_list() (+27 more)

### Community 52 - "model/actions.py"
Cohesion: 0.13
Nodes (4): _en_accion_de_ataque(), _living_enemies(), _log(), MultiattackAction

### Community 53 - "warnings"
Cohesion: 0.18
Nodes (5): parse_range_type(), _parse_condition_immunities(), _parse_damage_modifiers(), _warn(), test_el_tipo_de_ataque_coincide_con_el_texto()

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.12
Nodes (16): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+8 more)

### Community 57 - "inflict_damage"
Cohesion: 0.19
Nodes (8): _absorber_pv_temporales(), _hooks(), inflict_damage(), _mark_dead_if_down(), _mitigacion_de_otros(), _notify_damage_dealt(), _notify_damage_taken(), _salvar_a_cero()

### Community 59 - "test_ancestral_guardian.py"
Cohesion: 0.18
Nodes (26): _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado(), _escudo(), _esperado() (+18 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.12
Nodes (23): ConditionEffect, test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa() (+15 more)

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
Cohesion: 0.11
Nodes (12): _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary(), _por_datos() (+4 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.11
Nodes (41): apply_storm_herald(), StormAuraAction, _abilities(), _aliado(), _barbaro(), _ctx(), _fijar_fallo_reaccion(), falla() (+33 more)

### Community 66 - "roll_modifiers.py"
Cohesion: 0.13
Nodes (9): check_modifiers(), _condiciones(), effective_ac(), _hooks(), _instancias(), resolve_attack_range(), save_modifiers(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo() (+1 more)

### Community 67 - "condition_parser.py"
Cohesion: 0.18
Nodes (5): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with()

### Community 68 - "test_spells.py"
Cohesion: 0.13
Nodes (9): parse_spellcasting(), Spellcasting, test_el_lanzador_se_lee_de_los_actions(), test_el_upcast_reescala_el_dano_y_la_curacion(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_la_curacion_usa_el_modificador_de_caracteristica_no_el_bono_completo(), test_los_hechizos_con_uso_limitado_tienen_uso_propio(), test_un_hechizo_de_accion_bonus_se_comprueba_en_su_fase() (+1 more)

### Community 69 - "Attack"
Cohesion: 0.20
Nodes (15): Attack, _nuevo_ataque(), test_alma_bestial_flag_magical_existe(), test_extra_damage_estructura_por_defecto_vacia(), _decision(), _mon(), _salvacion(), test_topple_derriba_si_falla_la_salvacion_de_con() (+7 more)

### Community 71 - "build_spell_actions"
Cohesion: 0.23
Nodes (9): build_spell_actions(), test_un_lanzador_carga_el_hechizo_con_su_uso_propio(), _desde_fixture(), _monstruo_lanzador(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_la_reaccion_gasta_su_uso_propio(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_uso_propio() (+1 more)

### Community 72 - "pathlib"
Cohesion: 0.12
Nodes (11): Arquitectura de `dnd_sim`, Cómo comprobar que todo sigue en orden, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, _capa(), _modulo_y_paquete() (+3 more)

### Community 73 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 74 - "test_lair.py"
Cohesion: 0.06
Nodes (38): _check_fields(), _construir(), _error(), load_lair(), lair_phase(), LairAction, LegendaryState, _ctx() (+30 more)

### Community 75 - "race_parser.py"
Cohesion: 0.25
Nodes (3): _skill_name(), _spells_from_description(), _trait_skills()

### Community 76 - "test_undead_fortitude.py"
Cohesion: 0.21
Nodes (14): _ctx(), _datos(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido(), test_la_salvacion_puede_salvarlo_o_no() (+6 more)

### Community 77 - "test_races.py"
Cohesion: 0.15
Nodes (18): Race, parse_race(), _abilities(), _fiendish_legacy(), _keen_senses(), _pj(), test_apply_race_añade_competencias_fijas(), test_apply_race_con_habilidad_pedida() (+10 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.17
Nodes (21): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+13 more)

### Community 79 - "test_azer.py"
Cohesion: 0.26
Nodes (17): _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), _rasgo(), test_ataque_a_distancia_no_dispara_la_represalia() (+9 more)

### Community 80 - "conditions.py"
Cohesion: 0.13
Nodes (9): _apply_condition_riders(), _as_condition(), _condicion_bloqueada(), _contar(), _label(), _queda_accion(), remove_condition(), remove_invisibility_on_action() (+1 more)

### Community 82 - "load_race"
Cohesion: 0.33
Nodes (5): load_race(), test_load_race_descarga_la_raza_y_sus_rasgos(), _rasgo(), _raza(), test_load_race_propaga_el_error_de_la_api()

### Community 83 - "TurnResources"
Cohesion: 0.10
Nodes (10): ActionType, TurnResources, SpellAction, SpellAttackAction, apply_concentration(), HealEffect, StateEffect, _tiene_estado() (+2 more)

### Community 84 - "Monster"
Cohesion: 0.13
Nodes (17): Carpetas, Monster, apply_damage_modifiers(), _is_petrified(), test_sin_condiciones_el_dano_no_cambia(), _target(), test_etiqueta_de_modificadores_se_deriva_del_dano_final(), test_immunity_zero() (+9 more)

### Community 85 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.33
Nodes (5): Bloque 2026-10-30 (commiteado), Grafo y verificación, Rutina sugerida al abrir sesión, TODO — DnDBalancer / dnd_sim, TODOs en código (marcados `# TODO`)

### Community 88 - "barbarian/__init__.py"
Cohesion: 0.20
Nodes (5): NaturalWeapon, ClassDef, normalize_class_name(), register_class(), SubclassDef

### Community 89 - "_trait"
Cohesion: 0.18
Nodes (13): _abilities(), test_brutal_strike_2d10_desde_nivel_17(), test_brutal_strike_renuncia_a_la_ventaja_y_paga_1d10(), test_brutal_strike_sin_fue_no_aplica(), test_furia_bonus_de_dano_solo_con_fue(), test_furia_persistente_termina_con_unconscious(), test_furia_resistencia_bps_y_no_fuego(), test_furia_sin_activa_no_resiste() (+5 more)

### Community 90 - "_duelo"
Cohesion: 0.32
Nodes (6): _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

### Community 91 - "test_relentless.py"
Cohesion: 0.27
Nodes (12): _ctx(), _datos(), _jabali(), _pj(), test_el_jabali_carga_su_relentless_con_umbral_y_uso(), test_relentless_no_necesita_contexto_ni_rng(), test_reset_reestablece_el_umbral_y_los_usos(), test_solo_puede_salvarse_una_vez_por_combate() (+4 more)

### Community 92 - "normalize_skill"
Cohesion: 0.22
Nodes (4): _clean(), normalize_skill(), test_normalize_skill_acepta_espacios_y_spanish(), test_normalize_skill_desconocida_lanza_value_error()

### Community 93 - ".on_turn_start"
Cohesion: 0.24
Nodes (3): _aliados_heridos(), _cd_ataque(), _en_10_pies()

### Community 94 - "WorldTreeFeatures"
Cohesion: 0.24
Nodes (4): apply_world_tree(), _de(), WorldTreeFeatures, test_apply_anade_trait_sin_accion_propia()

### Community 95 - "roll_d20"
Cohesion: 0.29
Nodes (5): d20(), D20Result, roll_d20(), espia(), espia()

### Community 97 - "Spell"
Cohesion: 0.33
Nodes (3): Paquetes con fachada, _uso_de_entrada(), Spell

### Community 99 - "SaveModifiers"
Cohesion: 0.33
Nodes (3): SaveModifiers, test_danger_sense_da_ventaja_en_salvaciones_de_des(), test_danger_sense_no_funciona_incapacitado()

## Knowledge Gaps
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `RollMode`, `combat/attack.py`, `test_utility.py`, `test_wild_magic.py`, `Abilities`, `apply_barbarian`, `test_death.py`, `spell_action`, `test_extra_damage.py`, `test_superior_invisibility.py`, `attack_roll`, `random`, `pytest`, `test_conditions.py`, `berserker.py`, `loader.py`, `test_battlerager.py`, `Condition`, `dnd_sim/__init__.py`, `_pj`, `test_checks_escapes.py`, `load_monster`, `model/actions.py`, `test_ancestral_guardian.py`, `test_magic_resistance.py`, `test_regeneration.py`, `legendary_parser.py`, `test_storm_herald.py`, `test_spells.py`, `test_pack_tactics.py`, `test_lair.py`, `test_undead_fortitude.py`, `test_enlarge.py`, `test_azer.py`, `TurnResources`, `Monster`, `Combatant`, `barbarian/__init__.py`, `_trait`, `_duelo`, `test_relentless.py`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `AttackRange`) actually correct?**
  _`Attack` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09288824383164006 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_legendary.py`, `test_beast.py`, `_spell_data`, `RollMode`, `combat/attack.py`, `test_utility.py`, `parse_spell`, `traits/__init__.py`, `Abilities`, `BarbarianFeatures`, `spell_action`, `test_superior_invisibility.py`, `test_skills.py`, `attack_roll`, `test_area.py`, `test_conditions.py`, `berserker.py`, `loader.py`, `ability_check`, `dnd_sim/__init__.py`, `_pj`, `test_checks_escapes.py`, `warnings`, `test_condition_immunities.py`, `inflict_damage`, `test_magic_resistance.py`, `DamageTransfer`, `test_storm_herald.py`, `roll_modifiers.py`, `condition_parser.py`, `test_spells.py`, `Attack`, `test_pack_tactics.py`, `test_lair.py`, `test_enlarge.py`, `conditions.py`, `TurnResources`, `Monster`, `Combatant`, `WorldTreeFeatures`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 103 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 103 INFERRED edges - model-reasoned connections that need verification._
- **Should `AttackRange` be split into smaller, more focused modules?**
  _Cohesion score 0.06869254341164453 - nodes in this community are weakly interconnected._
- **Why does `PlayerCharacter` connect `Abilities` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `RollMode`, `test_utility.py`, `test_wild_magic.py`, `BarbarianFeatures`, `test_loader_actions.py`, `run_combat`, `apply_barbarian`, `test_martial_advantage.py`, `test_death.py`, `test_extra_damage.py`, `test_superior_invisibility.py`, `test_backgrounds.py`, `test_skills.py`, `attack_roll`, `test_area.py`, `random`, `pytest`, `test_conditions.py`, `test_battlerager.py`, `Condition`, `dnd_sim/__init__.py`, `_pj`, `test_checks_escapes.py`, `load_monster`, `test_condition_immunities.py`, `test_ancestral_guardian.py`, `test_magic_resistance.py`, `test_regeneration.py`, `test_storm_herald.py`, `test_spells.py`, `test_pack_tactics.py`, `test_lair.py`, `test_undead_fortitude.py`, `test_races.py`, `test_enlarge.py`, `test_azer.py`, `Monster`, `background_parser.py`, `Combatant`, `test_relentless.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
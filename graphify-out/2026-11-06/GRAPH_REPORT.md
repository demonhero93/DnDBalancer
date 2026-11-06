# Graph Report - DnDBalancer  (2026-11-05)

## Corpus Check
- 217 files · ~168,590 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 3219 nodes · 11681 edges · 96 communities (83 shown, 13 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 742 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `27532b9c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_fighter.py
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
- attack_roll
- test_utility.py
- test_wild_magic.py
- _dados_hasta
- hooks
- main.py
- BarbarianFeatures
- test_loader_actions.py
- CombatContext
- storm_herald.py
- run_combat
- apply_barbarian
- test_martial_advantage.py
- ZealotFeatures
- test_zealot.py
- test_death.py
- json
- test_magical.py
- test_extra_damage.py
- test_superior_invisibility.py
- FighterFeatures
- BeastFeatures
- test_skills.py
- parse_traits
- test_parry.py
- test_area.py
- Combatant
- LegendaryState
- random
- apply_class
- Abilities
- Trait
- _ctx
- TurnResources
- Condition
- checks.py
- combatant.py
- _pj
- test_checks_escapes.py
- load_monster
- _decision
- _pj
- test_condition_immunities.py
- inflict_damage
- test_ancestral_guardian.py
- test_magic_resistance.py
- PlayerCharacter
- parse_escape
- DamageTransfer
- loader.py
- test_storm_herald.py
- saving_throw
- test_multiattack.py
- test_spells.py
- Attack
- barbarian/__init__.py
- attach.py
- WarriorHealAction
- RollMode
- test_lair.py
- ConditionTracker
- test_undead_fortitude.py
- test_races.py
- test_enlarge.py
- test_azer.py
- apply_condition
- load_lair
- DamageRecorder
- dnd_sim/__init__.py
- test_damage.py
- weapon_mastery_count
- _RngBajo
- espia
- _RngMax
- _SoloMod
- resolve_attack_range
- test_relentless.py
- normalize_skill
- ActionUsage
- ability_check_bonus

## God Nodes (most connected - your core abstractions)
1. `Attack` - 177 edges
2. `Condition` - 160 edges
3. `apply_condition()` - 148 edges
4. `Abilities` - 141 edges
5. `load_monster()` - 135 edges
6. `attack_roll()` - 135 edges
7. `AttackRange` - 131 edges
8. `PlayerCharacter` - 123 edges
9. `Monster` - 115 edges
10. `run_combat()` - 95 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Fighter: datos sin efecto` --references--> `sample()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Paquetes con fachada` --references--> `CombatResult`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/engine/combat/encounter.py

## Import Cycles
- None detected.

## Communities (96 total, 13 thin omitted)

### Community 0 - "test_fighter.py"
Cohesion: 0.12
Nodes (42): _action_surge(), _ctx(), _ctx_recursos(), _fighter(), _mods(), _objetivo(), _save_fallada(), _saving_nueva() (+34 more)

### Community 1 - "test_attach.py"
Cohesion: 0.18
Nodes (25): _atacar(), _bite(), _cloaker(), _ctx(), _datos(), _pj(), test_con_ventaja_el_enganche_es_a_la_cabeza_y_ciega(), test_damage_transfer_no_aplica_sin_enganche() (+17 more)

### Community 2 - "AttackRange"
Cohesion: 0.07
Nodes (55): AttackRange, apply_berserker(), BerserkerFeatures, _de(), _furia_de(), _golpe_sin_armas(), IntimidatingPresenceAction, _abilities() (+47 more)

### Community 3 - "test_giant.py"
Cohesion: 0.08
Nodes (37): apply_giant(), _de(), GiantFeatures, MightyImpelAction, _objetivos_impel(), _orden_de(), _abilities(), _barbaro() (+29 more)

### Community 4 - "test_world_tree.py"
Cohesion: 0.11
Nodes (39): apply_world_tree(), _abilities(), _aliado(), _barbaro(), _ctx(), _decision(), _elige_candidato(), espia() (+31 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.06
Nodes (52): parse_damage_type(), apply_wild_heart(), _con_beneficio(), _de(), _en_5_pies(), _hostil(), _orden_de(), WildHeartFeatures (+44 more)

### Community 6 - "test_proficiency.py"
Cohesion: 0.19
Nodes (19): proficiency_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia(), test_level_manda_sobre_el_proficiency_explicito() (+11 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.07
Nodes (60): simulate(), legendary_phase(), _contexto(), _data(), _estado(), _legendaria(), _load(), _pj() (+52 more)

### Community 8 - "test_beast.py"
Cohesion: 0.11
Nodes (64): _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll(), spy(), _forma() (+56 more)

### Community 9 - "parse_spell"
Cohesion: 0.10
Nodes (30): _elementos_por_nivel(), _elementos_totales(), parse_spell(), _slot_table(), _tabla_cantrip(), _tipo_de_dano(), spell_action(), _spell_data() (+22 more)

### Community 10 - "test_traits.py"
Cohesion: 0.11
Nodes (23): resolve_roll_mode(), attack_modifiers(), _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _sahuagin() (+15 more)

### Community 11 - "attack_roll"
Cohesion: 0.09
Nodes (13): _actualizar_distancia(), _agrandado(), attack_roll(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), _mode_tag() (+5 more)

### Community 12 - "test_utility.py"
Cohesion: 0.13
Nodes (29): ConditionInstance, _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), _orden_tamano(), _abilities(), _ctx() (+21 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.07
Nodes (53): _log_target(), apply_wild_magic(), _sombra(), WildMagicFeatures, WildSurgeAction, _mode_tag(), _outcome_tag(), _log_line_outcome() (+45 more)

### Community 16 - "hooks"
Cohesion: 0.06
Nodes (15): Paquetes con fachada, hooks(), HeatedBody, Parry, TurnResistance, aliados_capaces(), BloodFrenzy, _condicion_posicional() (+7 more)

### Community 17 - "main.py"
Cohesion: 0.27
Nodes (6): print_report(), build_parser(), _build_party(), _load_party(), main(), _parse_monster_token()

### Community 18 - "BarbarianFeatures"
Cohesion: 0.09
Nodes (5): BarbarianFeatures, ExtendRageAction, _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 19 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (16): parse_usage(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+8 more)

### Community 20 - "CombatContext"
Cohesion: 0.05
Nodes (21): pick(), sample(), _objetivo_enganche(), valid_targets(), actor_is_alive(), CombatContext, _en_accion_de_ataque(), _living_enemies() (+13 more)

### Community 21 - "storm_herald.py"
Cohesion: 0.08
Nodes (9): _aliados_en_aura(), _cd(), _dado_mar(), _de(), _en_aura(), _enemigos_en_aura(), _escalado(), StormAuraAction (+1 more)

### Community 22 - "run_combat"
Cohesion: 0.12
Nodes (16): run_combat(), _summarize_damage(), _breath(), _eventos(), _FixedRandom, _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos() (+8 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.09
Nodes (48): rage_uses(), apply_barbarian(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj(), _resultado() (+40 more)

### Community 24 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 25 - "ZealotFeatures"
Cohesion: 0.09
Nodes (7): _de(), _en_60_pies(), _es_aliado(), ZealotFeatures, test_apply_class_por_clave_aplica_zealot(), test_clave_de_registro_zealot_en_barbarian(), _trait()

### Community 26 - "test_zealot.py"
Cohesion: 0.14
Nodes (30): _abilities(), _accion(), _aliado(), _barbaro(), _ctx(), _presencia(), test_after_failed_save_sin_zealot_devuelve_el_mismo_resultado(), test_fanatical_no_activo_sin_furia() (+22 more)

### Community 27 - "test_death.py"
Cohesion: 0.14
Nodes (18): combat_finished(), living_teams(), _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero() (+10 more)

### Community 28 - "json"
Cohesion: 0.06
Nodes (28): Background, normalize_tool(), _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell() (+20 more)

### Community 29 - "test_magical.py"
Cohesion: 0.16
Nodes (16): apply_beast(), _ctx(), _pj(), _spell_data(), _spellcasting(), test_ataque_con_magical_true_dana_completo_al_ghost(), test_ataque_magico_contra_un_bárbaro_en_furia_se_reduce_a_la_mitad(), test_bestial_solo_marca_las_armas_magicas_desde_el_nivel_6() (+8 more)

### Community 30 - "test_extra_damage.py"
Cohesion: 0.23
Nodes (17): _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional(), test_ataque_sin_extra_no_llama_al_bucle() (+9 more)

### Community 31 - "test_superior_invisibility.py"
Cohesion: 0.30
Nodes (12): remove_invisibility_on_action(), _accion(), _ctx(), _pixie(), _pj(), test_atacar_con_ventaja_y_no_pierde_la_invisibilidad(), test_ejecutarla_aplica_el_estado(), test_el_monstruo_recibe_su_accion_al_construirse() (+4 more)

### Community 32 - "FighterFeatures"
Cohesion: 0.10
Nodes (5): ActionSurgeAction, _contexto(), FighterFeatures, _rasgo(), SecondWindAction

### Community 34 - "test_skills.py"
Cohesion: 0.15
Nodes (20): _abilities(), _ctx(), _load_fixture(), _pj(), test_ability_check_no_suma_competencia_de_habilidad(), test_attempt_escapes_tira_la_habilidad(), test_check_modifiers_pasa_la_habilidad_a_los_rasgos(), test_escape_con_competencia_en_atletismo_sube_el_bono() (+12 more)

### Community 35 - "parse_traits"
Cohesion: 0.10
Nodes (12): _resistencia_legendaria(), _declara_uso(), _entradas(), parse_traits(), _usage(), UnknownUsageError, _warn(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd() (+4 more)

### Community 36 - "test_parry.py"
Cohesion: 0.24
Nodes (22): D20Result, _arquero_parry(), _ataque(), _ctx(), _datos(), _fijar_d20(), espia(), _gladiador() (+14 more)

### Community 37 - "test_area.py"
Cohesion: 0.07
Nodes (39): Arquitectura de `dnd_sim`, Carpetas, Cómo comprobar que todo sigue en orden, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, AreaTargeting (+31 more)

### Community 38 - "Combatant"
Cohesion: 0.06
Nodes (17): d20(), roll_d20(), CombatResult, _invoke_policy(), roll_initiative(), _run_combat(), _nuevo_ctx(), _pasada() (+9 more)

### Community 39 - "LegendaryState"
Cohesion: 0.13
Nodes (15): lair_phase(), LairAction, LegendaryState, _presupuesto(), _ctx(), _enemigo(), _Stub, test_dos_acciones_uniformes() (+7 more)

### Community 40 - "random"
Cohesion: 0.25
Nodes (18): _abilities(), _ctx(), _decide(), _pj(), test_antes_del_nivel_2_no_hay_decision_ni_rng(), test_en_turno_ajeno_no_decide(), test_frecuencia_0_5_es_aproximadamente_la_mitad_de_los_turnos(), test_las_reacciones_no_deciden_ni_reciben() (+10 more)

### Community 41 - "apply_class"
Cohesion: 0.13
Nodes (19): apply_class(), ClassDef, normalize_class_name(), register_class(), SubclassDef, _abilities(), _firmas(), _pj() (+11 more)

### Community 42 - "Abilities"
Cohesion: 0.09
Nodes (34): Abilities, Monster, _data(), _load(), _pj(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente(), test_can_act_y_can_react(), test_condicion_fuera_del_enum_lanza_value_error() (+26 more)

### Community 43 - "Trait"
Cohesion: 0.04
Nodes (34): action_surge_uses(), _clamp(), extra_attacks_for(), indomitable_uses(), rage_damage(), second_wind_uses(), roll_dice(), DamageType (+26 more)

### Community 44 - "_ctx"
Cohesion: 0.17
Nodes (19): _ataque(), _ctx(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja(), test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_las_condiciones_incapacitantes_fallan_fue_y_des_sin_tirar_dados() (+11 more)

### Community 45 - "TurnResources"
Cohesion: 0.08
Nodes (37): TurnResources, apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), SpikedArmorAction, AttackModifiers, _abilities() (+29 more)

### Community 46 - "Condition"
Cohesion: 0.17
Nodes (27): _parse_condition_immunities(), Condition, test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar() (+19 more)

### Community 47 - "checks.py"
Cohesion: 0.16
Nodes (8): skill_ability(), _finish_check(), _guia(), _resolve_mods(), skill_bonus(), skill_check(), check_modifiers(), test_caracteristica_asociada()

### Community 48 - "combatant.py"
Cohesion: 0.09
Nodes (4): ability_mod(), normalize_ability(), CombatState, CombatantType

### Community 49 - "_pj"
Cohesion: 0.15
Nodes (17): _ctx(), _npc(), _pj(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizado_invierte_los_objetivos_de_ataque(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado(), test_el_hechizo_verdadero_es_un_ataque_real_con_dano_extra() (+9 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.09
Nodes (41): ability_check(), CheckResult, attempt_escapes(), EscapeCheck, effective_ac(), begin_turn(), _check_fijo(), _fake() (+33 more)

### Community 51 - "load_monster"
Cohesion: 0.12
Nodes (18): _armor_class_value(), load_monster(), _norm_name(), test_una_condicion_desconocida_de_la_api_avisa(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number() (+10 more)

### Community 52 - "_decision"
Cohesion: 0.14
Nodes (21): _furia_de(), _decision(), _fallos(), _forma(), _guarda_con(), stub(), test_fanatical_decision_negativa_no_repiten(), test_fanatical_el_resultado_nuevo_sustituye_al_original() (+13 more)

### Community 53 - "_pj"
Cohesion: 0.26
Nodes (17): _espiar_divine(), _furia(), _mon(), _pj(), corrida(), test_divine_fury_elige_radiante_con_pick(), test_divine_fury_funciona_a_distancia(), test_divine_fury_no_paga_en_reacciones() (+9 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.11
Nodes (17): ConditionEffect, test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats() (+9 more)

### Community 57 - "inflict_damage"
Cohesion: 0.18
Nodes (7): _absorber_pv_temporales(), _hooks(), inflict_damage(), _mitigacion_de_otros(), _notify_damage_dealt(), _salvar_a_cero(), test_inflict_damage_registra_la_bandera_magical()

### Community 59 - "test_ancestral_guardian.py"
Cohesion: 0.18
Nodes (26): _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado(), _escudo(), _esperado() (+18 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.11
Nodes (24): _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab(), test_condition_action_de_hechizo_pasa_magical() (+16 more)

### Community 61 - "PlayerCharacter"
Cohesion: 0.19
Nodes (17): PlayerCharacter, test_regression_guerrero_vs_ogro(), test_regression_guerrero_vs_owlbear(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion() (+9 more)

### Community 62 - "parse_escape"
Cohesion: 0.25
Nodes (5): parse_escape(), _skills_for(), _data(), test_el_fixture_de_la_constriccion_tiene_escape_y_avisa_de_grappled(), test_el_fixture_de_la_telaraña_carga_restrained_con_escape()

### Community 63 - "DamageTransfer"
Cohesion: 0.23
Nodes (3): DamageTransfer, _empuna_arma_melee(), _ve_al_atacante()

### Community 64 - "loader.py"
Cohesion: 0.03
Nodes (43): is_area_action(), parse_attach_effects(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), parse_range_type(), _sentence_with() (+35 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.12
Nodes (40): apply_storm_herald(), _abilities(), _aliado(), _barbaro(), _ctx(), _fijar_fallo_reaccion(), falla(), _fijar_salvacion() (+32 more)

### Community 66 - "saving_throw"
Cohesion: 0.09
Nodes (16): _condiciones(), _hooks(), _instancias(), save_modifiers(), _con_resistencia_legendaria(), saving_throw(), _RasgoDeSalvacion, test_el_hook_de_salvaciones_alimenta_save_modifiers() (+8 more)

### Community 67 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 68 - "test_spells.py"
Cohesion: 0.11
Nodes (17): build_spell_actions(), parse_spellcasting(), Spellcasting, _desde_fixture(), _monstruo_lanzador(), test_el_lanzador_se_lee_de_los_actions(), test_el_upcast_reescala_el_dano_y_la_curacion(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos() (+9 more)

### Community 69 - "Attack"
Cohesion: 0.12
Nodes (28): Attack, apply_fighter(), test_alma_bestial_flag_magical_existe(), _abilities(), _firmas(), _pj(), test_apply_class_fighter_sin_subclase_equivalente_a_apply_fighter(), test_apply_fighter_acepta_las_habilidades_de_la_lista() (+20 more)

### Community 70 - "barbarian/__init__.py"
Cohesion: 0.09
Nodes (6): AncestralGuardianFeatures, apply_ancestral_guardian(), FormOfTheBeast, NaturalWeapon, _de(), WorldTreeFeatures

### Community 71 - "attach.py"
Cohesion: 0.18
Nodes (5): Attach, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por()

### Community 72 - "WarriorHealAction"
Cohesion: 0.20
Nodes (6): apply_zealot(), _reserva_dados(), WarriorHealAction, ZealousPresenceAction, test_apply_anade_trait_y_dos_acciones_bonus(), test_apply_requiere_clase_barbara()

### Community 73 - "RollMode"
Cohesion: 0.19
Nodes (15): RollMode, _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj() (+7 more)

### Community 74 - "test_lair.py"
Cohesion: 0.11
Nodes (19): _dragon(), lairs_dir(), _orden_con(), _pj(), _spy_turnos(), spy(), test_fixture_sintetica_carga(), test_guarida_pasa_magical_a_las_salvaciones() (+11 more)

### Community 76 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 77 - "test_races.py"
Cohesion: 0.09
Nodes (26): Race, load_race(), parse_race(), _skill_name(), _spells_from_description(), _trait_skills(), _abilities(), _fiendish_legacy() (+18 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.14
Nodes (25): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+17 more)

### Community 79 - "test_azer.py"
Cohesion: 0.26
Nodes (17): _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), _rasgo(), test_ataque_a_distancia_no_dispara_la_represalia() (+9 more)

### Community 80 - "apply_condition"
Cohesion: 0.10
Nodes (15): _apply_condition_riders(), apply_condition(), _as_condition(), _condicion_bloqueada(), _contar(), end_turn(), _label(), _queda_accion() (+7 more)

### Community 81 - "load_lair"
Cohesion: 0.40
Nodes (3): load_lair(), test_esquema_invalido(), test_targeting_fuera_de_rango()

### Community 83 - "dnd_sim/__init__.py"
Cohesion: 0.05
Nodes (25): _check_fields(), _construir(), _error(), ActionType, AttackAction, CombatAction, SaveAction, WeaponAttackAction (+17 more)

### Community 84 - "test_damage.py"
Cohesion: 0.11
Nodes (20): _tag_modificadores(), apply_damage_modifiers(), _is_petrified(), _guerrero_y_ogro(), _target(), test_danio_medio_por_combatiente_y_equipo(), test_etiqueta_de_modificadores_se_deriva_del_dano_final(), test_immunity_zero() (+12 more)

### Community 85 - "weapon_mastery_count"
Cohesion: 0.15
Nodes (11): fighter_extra_attacks_for(), weapon_mastery_count(), test_los_golpes_del_guerrero_suben_en_5_11_y_20(), test_maestria_con_armas_cuenta_segun_el_nivel(), Bloque 2026-10-30 (commiteado), Fighter: datos sin efecto, Fighter: plan de sesión, Grafo y verificación (+3 more)

### Community 87 - "espia"
Cohesion: 0.40
Nodes (3): espia(), test_determinismo_misma_semilla_mismos_resultados(), test_forma_se_vuelve_a_ofrecer_si_dice_que_no()

### Community 90 - "resolve_attack_range"
Cohesion: 0.25
Nodes (8): resolve_attack_range(), _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

### Community 91 - "test_relentless.py"
Cohesion: 0.27
Nodes (12): _ctx(), _datos(), _jabali(), _pj(), test_el_jabali_carga_su_relentless_con_umbral_y_uso(), test_relentless_no_necesita_contexto_ni_rng(), test_reset_reestablece_el_umbral_y_los_usos(), test_solo_puede_salvarse_una_vez_por_combate() (+4 more)

### Community 92 - "normalize_skill"
Cohesion: 0.22
Nodes (4): _clean(), normalize_skill(), test_normalize_skill_acepta_espacios_y_spanish(), test_normalize_skill_desconocida_lanza_value_error()

### Community 97 - "ActionUsage"
Cohesion: 0.12
Nodes (13): _uso_de_entrada(), RageAction, ActionUsage, UsageKind, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar(), test_per_day_dos_usos_y_luego_can_use_falso(), test_per_day_no_tira_recarga() (+5 more)

## Knowledge Gaps
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PlayerCharacter` connect `PlayerCharacter` to `test_fighter.py`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_traits.py`, `test_utility.py`, `test_wild_magic.py`, `main.py`, `BarbarianFeatures`, `test_loader_actions.py`, `run_combat`, `apply_barbarian`, `test_martial_advantage.py`, `test_zealot.py`, `test_death.py`, `json`, `test_magical.py`, `test_extra_damage.py`, `test_superior_invisibility.py`, `test_skills.py`, `test_parry.py`, `test_area.py`, `Combatant`, `LegendaryState`, `random`, `apply_class`, `Abilities`, `TurnResources`, `Condition`, `combatant.py`, `_pj`, `test_checks_escapes.py`, `load_monster`, `_pj`, `test_condition_immunities.py`, `test_ancestral_guardian.py`, `test_magic_resistance.py`, `test_storm_herald.py`, `saving_throw`, `test_multiattack.py`, `test_spells.py`, `Attack`, `RollMode`, `test_lair.py`, `test_undead_fortitude.py`, `test_races.py`, `test_enlarge.py`, `test_azer.py`, `dnd_sim/__init__.py`, `test_damage.py`, `test_relentless.py`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `AttackRange`) actually correct?**
  _`Attack` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_fighter.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12326530612244897 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_legendary.py`, `test_beast.py`, `parse_spell`, `test_traits.py`, `attack_roll`, `test_utility.py`, `BarbarianFeatures`, `CombatContext`, `storm_herald.py`, `json`, `test_superior_invisibility.py`, `test_skills.py`, `test_parry.py`, `Combatant`, `LegendaryState`, `Abilities`, `Trait`, `checks.py`, `combatant.py`, `_pj`, `test_checks_escapes.py`, `test_condition_immunities.py`, `test_magic_resistance.py`, `DamageTransfer`, `loader.py`, `test_storm_herald.py`, `saving_throw`, `test_spells.py`, `barbarian/__init__.py`, `attach.py`, `RollMode`, `test_lair.py`, `ConditionTracker`, `test_enlarge.py`, `apply_condition`, `dnd_sim/__init__.py`, `test_damage.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 103 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 103 INFERRED edges - model-reasoned connections that need verification._
- **Should `AttackRange` be split into smaller, more focused modules?**
  _Cohesion score 0.07226890756302522 - nodes in this community are weakly interconnected._
- **Why does `Attack` connect `Attack` to `test_fighter.py`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `parse_spell`, `test_traits.py`, `attack_roll`, `test_utility.py`, `test_wild_magic.py`, `main.py`, `CombatContext`, `apply_barbarian`, `test_zealot.py`, `test_death.py`, `test_magical.py`, `test_extra_damage.py`, `test_superior_invisibility.py`, `test_parry.py`, `Combatant`, `random`, `apply_class`, `Abilities`, `Trait`, `_ctx`, `TurnResources`, `Condition`, `combatant.py`, `_pj`, `test_checks_escapes.py`, `load_monster`, `_pj`, `test_ancestral_guardian.py`, `test_magic_resistance.py`, `PlayerCharacter`, `loader.py`, `test_storm_herald.py`, `test_spells.py`, `barbarian/__init__.py`, `RollMode`, `test_undead_fortitude.py`, `test_enlarge.py`, `test_azer.py`, `dnd_sim/__init__.py`, `test_damage.py`, `resolve_attack_range`, `test_relentless.py`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
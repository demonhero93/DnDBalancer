# Graph Report - DnDBalancer  (2026-11-06)

## Corpus Check
- 219 files · ~175,272 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 3346 nodes · 12135 edges · 106 communities (91 shown, 15 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 762 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `66f49400`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- _fighter
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
- attack_roll
- test_utility.py
- test_wild_magic.py
- Trait
- spell_parser.py
- Combatant
- main.py
- BarbarianFeatures
- test_loader_actions.py
- CombatContext
- StormHeraldFeatures
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
- warnings
- test_parry.py
- test_azer.py
- ActionType
- LegendaryState
- test_mastery.py
- test_ancestral_guardian.py
- apply_condition
- dnd_sim/__init__.py
- test_area.py
- random
- Condition
- ability_check
- normalize_ability
- SpellFixedDamageAction
- test_checks_escapes.py
- load_monster
- _trait
- saves.py
- test_condition_immunities.py
- inflict_damage
- BerserkerFeatures
- test_magic_resistance.py
- test_regeneration.py
- parse_escape
- DamageTransfer
- legendary_parser.py
- test_storm_herald.py
- saving_throw
- test_backgrounds.py
- build_spell_actions
- Attack
- barbarian/__init__.py
- intentar_desenganche
- BattleragerFeatures
- test_pack_tactics.py
- test_lair.py
- ConditionTracker
- test_undead_fortitude.py
- test_races.py
- test_enlarge.py
- loader.py
- Any
- load_lair
- Any
- spell_action
- PlayerCharacter
- TODO — DnDBalancer / dnd_sim
- _RngBajo
- conditions.py
- _RngMax
- condition_parser.py
- _duelo
- test_relentless.py
- multiattack_parser.py
- race_parser.py
- background_parser.py
- parse_spellcasting
- attach.py
- TurnResources
- load_race
- _RngExplota
- _save_fallada
- test_el_gancho_after_failed_check_desde_ability_check_con_ctx
- test_tactical_master_nivel_9_elige_entre_original_push_sap_slow
- indomitable_uses
- test_sin_autoexito_ni_autofallo_en_pruebas

## God Nodes (most connected - your core abstractions)
1. `Attack` - 185 edges
2. `Condition` - 167 edges
3. `apply_condition()` - 150 edges
4. `Abilities` - 145 edges
5. `attack_roll()` - 138 edges
6. `load_monster()` - 135 edges
7. `AttackRange` - 131 edges
8. `PlayerCharacter` - 128 edges
9. `Monster` - 117 edges
10. `run_combat()` - 95 edges

## Surprising Connections (you probably didn't know these)
- `Guaridas: política fija` --references--> `pick()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/core/randomness.py
- `TODOs en código (marcados `# TODO`)` --references--> `pick()`  [INFERRED]
  TODO.md → dnd_sim/core/randomness.py
- `Fighter: pendientes reales` --references--> `apply_fighter()`  [INFERRED]
  TODO.md → dnd_sim/rules/classes/fighter/features.py
- `Fighter: plan de sesión` --references--> `weapon_mastery_count()`  [INFERRED]
  TODO.md → dnd_sim/core/classes.py
- `Fighter: cierre de pendientes` --references--> `CombatState`  [INFERRED]
  TODO.md → dnd_sim/core/combat_state.py

## Import Cycles
- None detected.

## Communities (106 total, 15 thin omitted)

### Community 0 - "_fighter"
Cohesion: 0.11
Nodes (21): second_wind_uses(), _action_surge(), _ctx_recursos(), _fighter(), _second_wind(), test_action_surge_como_maximo_un_vez_por_turno(), test_action_surge_ejecutada_restaura_la_accion_y_gasta_un_uso(), test_action_surge_no_es_elegible_si_la_accion_no_se_ha_gastado() (+13 more)

### Community 1 - "test_attach.py"
Cohesion: 0.18
Nodes (25): _atacar(), _bite(), _cloaker(), _ctx(), _datos(), _pj(), test_con_ventaja_el_enganche_es_a_la_cabeza_y_ciega(), test_damage_transfer_no_aplica_sin_enganche() (+17 more)

### Community 2 - "AttackRange"
Cohesion: 0.11
Nodes (50): AttackRange, RageAction, apply_berserker(), IntimidatingPresenceAction, _abilities(), _barbaro(), _berserker(), _ctx() (+42 more)

### Community 3 - "test_giant.py"
Cohesion: 0.08
Nodes (35): apply_giant(), _de(), GiantFeatures, MightyImpelAction, _objetivos_impel(), _orden_de(), _abilities(), _barbaro() (+27 more)

### Community 4 - "test_world_tree.py"
Cohesion: 0.12
Nodes (38): _abilities(), _aliado(), _barbaro(), _ctx(), _decision(), _elige_candidato(), espia(), _furia() (+30 more)

### Community 5 - "test_wild_heart.py"
Cohesion: 0.06
Nodes (51): parse_damage_type(), apply_wild_heart(), _con_beneficio(), _de(), _en_5_pies(), _hostil(), _orden_de(), _es_radiante() (+43 more)

### Community 6 - "test_proficiency.py"
Cohesion: 0.17
Nodes (21): proficiency_bonus(), ability_check_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia() (+13 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.06
Nodes (63): simulate(), ConditionEffect, legendary_phase(), LegendaryAction, test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _contexto(), _data(), _estado() (+55 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (66): WeaponAttackAction, _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll(), spy() (+58 more)

### Community 9 - "test_spells.py"
Cohesion: 0.10
Nodes (41): parse_spell(), _ctx(), _npc(), _pj(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot() (+33 more)

### Community 10 - "RollMode"
Cohesion: 0.07
Nodes (31): RollMode, attack_modifiers(), _condiciones(), _hooks(), _instancias(), resolve_attack_range(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo(), _ataque_melee() (+23 more)

### Community 11 - "attack_roll"
Cohesion: 0.08
Nodes (20): d20(), roll_d20(), _actualizar_distancia(), _agrandado(), _apply_condition_riders(), attack_roll(), _bonus_de_rasgos(), _bonus_de_tamano() (+12 more)

### Community 12 - "test_utility.py"
Cohesion: 0.11
Nodes (30): ConditionInstance, _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), hay_utilitaria_accion(), _orden_tamano(), _abilities() (+22 more)

### Community 13 - "test_wild_magic.py"
Cohesion: 0.07
Nodes (41): _sombra(), WildMagicFeatures, _abilities(), _barbaro(), _con_cola(), _con_efecto(), espia(), _ctx() (+33 more)

### Community 14 - "Trait"
Cohesion: 0.03
Nodes (12): Attach, Trait, aliados_capaces(), BloodFrenzy, _condicion_posicional(), MartialAdvantage, PackTactics, SuperiorInvisibility (+4 more)

### Community 15 - "spell_parser.py"
Cohesion: 0.10
Nodes (12): _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla(), _frases() (+4 more)

### Community 16 - "Combatant"
Cohesion: 0.10
Nodes (9): Arquitectura de `dnd_sim`, Carpetas, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, Combatant, _mark_dead_if_down() (+1 more)

### Community 17 - "main.py"
Cohesion: 0.27
Nodes (6): print_report(), build_parser(), _build_party(), _load_party(), main(), _parse_monster_token()

### Community 18 - "BarbarianFeatures"
Cohesion: 0.09
Nodes (5): BarbarianFeatures, ExtendRageAction, _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 19 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (14): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+6 more)

### Community 20 - "CombatContext"
Cohesion: 0.10
Nodes (9): pick(), valid_targets(), actor_is_alive(), CombatContext, _en_accion_de_ataque(), _living_enemies(), _log(), _romper_invisibilidad_al_lanzar() (+1 more)

### Community 21 - "StormHeraldFeatures"
Cohesion: 0.09
Nodes (7): _aliados_en_aura(), _cd(), _dado_mar(), _en_aura(), _enemigos_en_aura(), _escalado(), StormHeraldFeatures

### Community 22 - "run_combat"
Cohesion: 0.06
Nodes (39): run_combat(), _summarize_damage(), ActionUsage, UsageKind, _data(), _load(), _pj(), _raw_multiattack() (+31 more)

### Community 23 - "apply_barbarian"
Cohesion: 0.09
Nodes (47): apply_barbarian(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj(), _resultado(), test_apply_anade_acciones_de_furia() (+39 more)

### Community 24 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 25 - "ZealotFeatures"
Cohesion: 0.08
Nodes (8): apply_zealot(), _de(), _en_60_pies(), _es_aliado(), _furia_de(), _reserva_dados(), ZealotFeatures, ZealousPresenceAction

### Community 26 - "test_zealot.py"
Cohesion: 0.06
Nodes (85): WarriorHealAction, SaveResult, fake_saving_throw(), falla(), espia(), stub(), stub(), _abilities() (+77 more)

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 28 - "json"
Cohesion: 0.15
Nodes (9): _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError (+1 more)

### Community 29 - "test_magical.py"
Cohesion: 0.13
Nodes (20): SaveAction, apply_beast(), _ctx(), _pj(), _spell_data(), _spellcasting(), test_ataque_con_magical_true_dana_completo_al_ghost(), test_ataque_magico_contra_un_bárbaro_en_furia_se_reduce_a_la_mitad() (+12 more)

### Community 30 - "test_extra_damage.py"
Cohesion: 0.17
Nodes (18): DamageRecorder, _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional() (+10 more)

### Community 31 - "test_superior_invisibility.py"
Cohesion: 0.30
Nodes (12): remove_invisibility_on_action(), _accion(), _ctx(), _pixie(), _pj(), test_atacar_con_ventaja_y_no_pierde_la_invisibilidad(), test_ejecutarla_aplica_el_estado(), test_el_monstruo_recibe_su_accion_al_construirse() (+4 more)

### Community 32 - "FighterFeatures"
Cohesion: 0.08
Nodes (8): CheckResult, ActionSurgeAction, _contexto(), _en_5_pies(), _es_aliado(), FighterFeatures, _rasgo(), SecondWindAction

### Community 34 - "test_skills.py"
Cohesion: 0.13
Nodes (21): _abilities(), _ctx(), _load_fixture(), _pj(), _SoloMod, test_ability_check_no_suma_competencia_de_habilidad(), test_attempt_escapes_tira_la_habilidad(), test_caracteristica_asociada() (+13 more)

### Community 35 - "warnings"
Cohesion: 0.12
Nodes (10): _resistencia_legendaria(), _parse_condition_immunities(), _parse_damage_modifiers(), _declara_uso(), _usage(), parse_usage(), UnknownUsageError, _warn() (+2 more)

### Community 36 - "test_parry.py"
Cohesion: 0.14
Nodes (31): D20Result, _entradas(), parse_traits(), fijar(), espia(), _arquero_parry(), _ataque(), _ctx() (+23 more)

### Community 37 - "test_azer.py"
Cohesion: 0.08
Nodes (29): Cómo comprobar que todo sigue en orden, HeatedBody, _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api(), _ataque_melee() (+21 more)

### Community 38 - "ActionType"
Cohesion: 0.06
Nodes (22): combat_finished(), living_teams(), _objetivo_enganche(), CombatResult, _invoke_policy(), roll_initiative(), _run_combat(), _nuevo_ctx() (+14 more)

### Community 39 - "LegendaryState"
Cohesion: 0.14
Nodes (14): lair_phase(), LairAction, LegendaryState, _ctx(), _enemigo(), _Stub, test_dos_acciones_uniformes(), test_no_actua_si_el_combate_cae_en_medio() (+6 more)

### Community 40 - "test_mastery.py"
Cohesion: 0.09
Nodes (30): al_acertar(), al_fallar(), _cd_topple(), consumir_marcas(), _log(), _nombre(), resolver_maestria(), _arma() (+22 more)

### Community 41 - "test_ancestral_guardian.py"
Cohesion: 0.05
Nodes (48): AncestralGuardianFeatures, apply_ancestral_guardian(), apply_class(), ClassDef, normalize_class_name(), register_class(), SubclassDef, _abilities() (+40 more)

### Community 42 - "apply_condition"
Cohesion: 0.07
Nodes (58): Abilities, apply_condition(), end_turn(), RepeatSave, _ataque(), _ctx(), _data(), _duelo() (+50 more)

### Community 43 - "dnd_sim/__init__.py"
Cohesion: 0.06
Nodes (20): ability_mod(), _clamp(), extra_attacks_for(), rage_damage(), rage_uses(), weapon_mastery_count(), CombatState, roll_dice() (+12 more)

### Community 44 - "test_area.py"
Cohesion: 0.16
Nodes (23): sample(), AreaSaveAction, AreaTargeting, select_area_targets(), SaveDamage, _area_action(), _ctx(), _npc() (+15 more)

### Community 45 - "random"
Cohesion: 0.11
Nodes (49): AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer(), _bj(), _ctx() (+41 more)

### Community 46 - "Condition"
Cohesion: 0.20
Nodes (26): Condition, test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+18 more)

### Community 47 - "ability_check"
Cohesion: 0.11
Nodes (13): _clean(), normalize_skill(), skill_ability(), ability_check(), _avisar_fallo_prueba(), _finish_check(), _guia(), _resolve_mods() (+5 more)

### Community 49 - "SpellFixedDamageAction"
Cohesion: 0.50
Nodes (3): SpellFixedDamageAction, test_el_proyectil_magico_pasa_por_los_modificadores_de_dano(), lanzar()

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.11
Nodes (37): attempt_escapes(), EscapeCheck, begin_turn(), _check_fijo(), _fake(), _ctx(), _load(), _pj() (+29 more)

### Community 51 - "load_monster"
Cohesion: 0.11
Nodes (17): doblar_dados(), _armor_class_value(), load_monster(), ExtraDamage, test_doblar_dados_duplica_los_dados_y_no_el_bonus(), _load_fixture(), _ogre_data(), test_armor_class_as_list() (+9 more)

### Community 52 - "_trait"
Cohesion: 0.15
Nodes (33): _aliado(), _check_fallada(), _con_estilo(), _ctx(), _enemigo(), _mods(), _objetivo(), _RngSi (+25 more)

### Community 53 - "saves.py"
Cohesion: 0.13
Nodes (14): _log_target(), registrar_resistencia_legendaria(), apply_save_damage(), _as_combat_context(), _avisar_fallo_salvacion(), _inflict_for_save(), _mode_tag(), _outcome_tag() (+6 more)

### Community 54 - "test_condition_immunities.py"
Cohesion: 0.12
Nodes (16): _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(), test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(), test_el_bando_pj_tambien_puede_ser_inmune(), test_el_cargador_carga_las_inmunidades_del_fixture() (+8 more)

### Community 57 - "inflict_damage"
Cohesion: 0.22
Nodes (6): _absorber_pv_temporales(), _hooks(), inflict_damage(), _mitigacion_de_otros(), _notify_damage_dealt(), _salvar_a_cero()

### Community 59 - "BerserkerFeatures"
Cohesion: 0.12
Nodes (6): _armas_melee_de(), BerserkerFeatures, _de(), _furia_de(), _golpe_sin_armas(), test_golpe_sin_armas_unidad()

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.12
Nodes (22): _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab(), test_condition_action_de_hechizo_pasa_magical() (+14 more)

### Community 61 - "test_regeneration.py"
Cohesion: 0.30
Nodes (13): _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno(), test_el_troll_carga_su_regeneracion() (+5 more)

### Community 62 - "parse_escape"
Cohesion: 0.15
Nodes (8): has_escape_text(), parse_escape(), _skills_for(), _data(), test_el_fixture_de_la_constriccion_tiene_escape_y_avisa_de_grappled(), test_el_fixture_de_la_telaraña_carga_restrained_con_escape(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 63 - "DamageTransfer"
Cohesion: 0.14
Nodes (5): DamageTransfer, _empuna_arma_melee(), Parry, TurnResistance, _ve_al_atacante()

### Community 64 - "legendary_parser.py"
Cohesion: 0.10
Nodes (13): parse_range_type(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary() (+5 more)

### Community 65 - "test_storm_herald.py"
Cohesion: 0.13
Nodes (37): _abilities(), _aliado(), _barbaro(), _ctx(), _fijar_fallo_reaccion(), _fijar_salvacion(), _furia(), _herald() (+29 more)

### Community 66 - "saving_throw"
Cohesion: 0.17
Nodes (13): save_modifiers(), _con_resistencia_legendaria(), saving_throw(), test_el_rasgo_anade_la_fuente_resistencia_magica(), test_sin_efecto_magico_o_sin_rasgo_no_anade_ventaja(), _datos(), _lich(), _pj() (+5 more)

### Community 67 - "test_backgrounds.py"
Cohesion: 0.16
Nodes (17): Background, load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes(), test_apply_background_sin_competencias_es_inofensivo() (+9 more)

### Community 68 - "build_spell_actions"
Cohesion: 0.29
Nodes (8): build_spell_actions(), _desde_fixture(), _monstruo_lanzador(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_la_reaccion_gasta_su_uso_propio(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_uso_propio(), test_un_hechizo_a_voluntad_se_puede_lanzar_en_cada_turno()

### Community 69 - "Attack"
Cohesion: 0.09
Nodes (42): action_surge_uses(), Attack, apply_fighter(), maestria_de(), _abilities(), _firmas(), _pj(), _pj_con_armas() (+34 more)

### Community 70 - "barbarian/__init__.py"
Cohesion: 0.07
Nodes (12): FormOfTheBeast, NaturalWeapon, apply_storm_herald(), _de(), StormAuraAction, WildHeartFeatures, _aliados_heridos(), apply_world_tree() (+4 more)

### Community 71 - "intentar_desenganche"
Cohesion: 0.24
Nodes (4): desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por()

### Community 72 - "BattleragerFeatures"
Cohesion: 0.13
Nodes (5): apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), SpikedArmorAction

### Community 73 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 74 - "test_lair.py"
Cohesion: 0.11
Nodes (19): _dragon(), lairs_dir(), _orden_con(), _pj(), _spy_turnos(), spy(), test_fixture_sintetica_carga(), test_guarida_pasa_magical_a_las_salvaciones() (+11 more)

### Community 76 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 77 - "test_races.py"
Cohesion: 0.15
Nodes (18): Race, parse_race(), _abilities(), _fiendish_legacy(), _keen_senses(), _pj(), test_apply_race_añade_competencias_fijas(), test_apply_race_con_habilidad_pedida() (+10 more)

### Community 78 - "test_enlarge.py"
Cohesion: 0.17
Nodes (22): _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj(), _spell_data() (+14 more)

### Community 79 - "loader.py"
Cohesion: 0.13
Nodes (7): _damage_type(), _norm_name(), build_condition_action(), build_save_effect(), damage_dice_of(), damage_options(), damage_type_of()

### Community 80 - "Any"
Cohesion: 0.18
Nodes (6): _as_condition(), _condicion_bloqueada(), _contar(), _label(), _queda_accion(), remove_condition()

### Community 81 - "load_lair"
Cohesion: 0.40
Nodes (3): load_lair(), test_esquema_invalido(), test_targeting_fuera_de_rango()

### Community 82 - "Any"
Cohesion: 0.13
Nodes (9): apply_wild_magic(), _bolstering(), _cd(), _de(), _en_30_pies(), _enemigos(), _flores(), _infusion() (+1 more)

### Community 83 - "spell_action"
Cohesion: 0.07
Nodes (17): Paquetes con fachada, _uso_de_entrada(), HealAction, SpellAction, SpellAttackAction, SpellStateAction, dado_por_nivel(), duracion_en_rondas() (+9 more)

### Community 84 - "PlayerCharacter"
Cohesion: 0.09
Nodes (25): Monster, PlayerCharacter, apply_damage_modifiers(), _is_petrified(), _guerrero_y_ogro(), _target(), test_attack_roll_log_modifier(), test_danio_medio_por_combatiente_y_equipo() (+17 more)

### Community 85 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.18
Nodes (9): fighter_extra_attacks_for(), test_los_golpes_del_guerrero_suben_en_5_11_y_20(), Bloque 2026-10-30 (commiteado), Fighter: pendientes reales, Fighter: plan de sesión, Grafo y verificación, Rutina sugerida al abrir sesión, TODO — DnDBalancer / dnd_sim (+1 more)

### Community 87 - "conditions.py"
Cohesion: 0.15
Nodes (5): _check_fields(), _construir(), _error(), ConditionAction, _default_targeting()

### Community 89 - "condition_parser.py"
Cohesion: 0.18
Nodes (5): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with()

### Community 90 - "_duelo"
Cohesion: 0.32
Nodes (6): _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

### Community 91 - "test_relentless.py"
Cohesion: 0.27
Nodes (12): _ctx(), _datos(), _jabali(), _pj(), test_el_jabali_carga_su_relentless_con_umbral_y_uso(), test_relentless_no_necesita_contexto_ni_rng(), test_reset_reestablece_el_umbral_y_los_usos(), test_solo_puede_salvarse_una_vez_por_combate() (+4 more)

### Community 92 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (5): _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 94 - "race_parser.py"
Cohesion: 0.20
Nodes (3): _skill_name(), _spells_from_description(), _trait_skills()

### Community 96 - "parse_spellcasting"
Cohesion: 0.20
Nodes (5): parse_spellcasting(), test_el_lanzador_se_lee_de_los_actions(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_la_curacion_usa_el_modificador_de_caracteristica_no_el_bono_completo(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 98 - "TurnResources"
Cohesion: 0.36
Nodes (3): TurnResources, _contexto_de_reaccion(), trigger_reaction()

### Community 99 - "load_race"
Cohesion: 0.33
Nodes (5): load_race(), test_load_race_descarga_la_raza_y_sus_rasgos(), _rasgo(), _raza(), test_load_race_propaga_el_error_de_la_api()

### Community 100 - "_RngExplota"
Cohesion: 0.29
Nodes (3): _RngExplota, test_resolver_maestria_sin_maestria_no_consulta_tactical_master(), test_tactical_master_no_sustituye_bajo_el_nivel_9()

### Community 101 - "_save_fallada"
Cohesion: 0.33
Nodes (6): _save_fallada(), _saving_nueva(), test_indomitable_no_actua_bajo_el_nivel_9(), test_indomitable_repite_la_salvacion_con_bonificador_igual_al_nivel(), test_indomitable_sin_usos_no_repites_y_no_consume_rng(), test_indomitable_usa_la_nueva_tirada_incluso_si_vuelve_a_fallar()

## Knowledge Gaps
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `_fighter`, `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `RollMode`, `attack_roll`, `test_utility.py`, `test_wild_magic.py`, `Combatant`, `main.py`, `CombatContext`, `apply_barbarian`, `test_zealot.py`, `test_death.py`, `test_magical.py`, `test_extra_damage.py`, `test_superior_invisibility.py`, `test_parry.py`, `test_azer.py`, `ActionType`, `test_mastery.py`, `test_ancestral_guardian.py`, `apply_condition`, `dnd_sim/__init__.py`, `random`, `Condition`, `test_checks_escapes.py`, `load_monster`, `BerserkerFeatures`, `test_magic_resistance.py`, `test_regeneration.py`, `legendary_parser.py`, `test_storm_herald.py`, `barbarian/__init__.py`, `BattleragerFeatures`, `test_pack_tactics.py`, `test_undead_fortitude.py`, `test_enlarge.py`, `loader.py`, `spell_action`, `PlayerCharacter`, `conditions.py`, `_duelo`, `test_relentless.py`, `_RngExplota`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `AttackRange`) actually correct?**
  _`Attack` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Should `_fighter` be split into smaller, more focused modules?**
  _Cohesion score 0.11384615384615385 - nodes in this community are weakly interconnected._
- **Why does `Abilities` connect `apply_condition` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_proficiency.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `RollMode`, `test_utility.py`, `test_wild_magic.py`, `Combatant`, `main.py`, `run_combat`, `apply_barbarian`, `test_martial_advantage.py`, `test_zealot.py`, `test_death.py`, `test_magical.py`, `test_extra_damage.py`, `test_superior_invisibility.py`, `test_skills.py`, `test_parry.py`, `test_azer.py`, `ActionType`, `test_mastery.py`, `test_ancestral_guardian.py`, `dnd_sim/__init__.py`, `test_area.py`, `random`, `Condition`, `test_checks_escapes.py`, `load_monster`, `test_condition_immunities.py`, `test_magic_resistance.py`, `test_regeneration.py`, `test_storm_herald.py`, `saving_throw`, `test_backgrounds.py`, `build_spell_actions`, `Attack`, `test_pack_tactics.py`, `test_undead_fortitude.py`, `test_races.py`, `test_enlarge.py`, `loader.py`, `PlayerCharacter`, `_duelo`, `test_relentless.py`, `test_sin_autoexito_ni_autofallo_en_pruebas`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 108 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 108 INFERRED edges - model-reasoned connections that need verification._
- **Should `AttackRange` be split into smaller, more focused modules?**
  _Cohesion score 0.10865384615384616 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `AttackRange`, `test_giant.py`, `test_world_tree.py`, `test_wild_heart.py`, `test_legendary.py`, `test_beast.py`, `test_spells.py`, `RollMode`, `attack_roll`, `test_utility.py`, `Trait`, `spell_parser.py`, `Combatant`, `BarbarianFeatures`, `StormHeraldFeatures`, `test_superior_invisibility.py`, `test_skills.py`, `warnings`, `test_parry.py`, `ActionType`, `LegendaryState`, `test_mastery.py`, `apply_condition`, `dnd_sim/__init__.py`, `ability_check`, `normalize_ability`, `test_checks_escapes.py`, `test_condition_immunities.py`, `BerserkerFeatures`, `test_magic_resistance.py`, `DamageTransfer`, `test_storm_herald.py`, `saving_throw`, `barbarian/__init__.py`, `intentar_desenganche`, `test_pack_tactics.py`, `test_lair.py`, `ConditionTracker`, `test_enlarge.py`, `loader.py`, `Any`, `spell_action`, `PlayerCharacter`, `conditions.py`, `condition_parser.py`, `attach.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
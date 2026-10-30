# Graph Report - DnDBalancer  (2026-10-30)

## Corpus Check
- 182 files · ~109,868 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 1998 nodes · 6871 edges · 69 communities (62 shown, 7 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 378 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `99ebee77`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ActionType
- test_attach.py
- test_ancestral_guardian.py
- test_usage.py
- test_area.py
- load_monster
- CombatContext
- test_conditions.py
- spell_action
- test_traits.py
- Condition
- _ctx
- random
- Trait
- parse_spell
- DamageTransfer
- test_damage.py
- build_spell_actions
- test_loader_actions.py
- test_multiattack.py
- test_legendary.py
- inflict_damage
- Attack
- TurnResources
- saves.py
- loader.py
- test_death.py
- json
- traits/__init__.py
- test_undead_fortitude.py
- test_azer.py
- apply_condition
- saving_throw
- test_skills.py
- test_backgrounds.py
- legendary.py
- test_proficiency.py
- run_combat
- parse_damage_type
- roll_modifiers.py
- attack_roll
- begin_turn
- dnd_sim/__init__.py
- legendary_parser.py
- test_spells.py
- PlayerCharacter
- normalize_skill
- attempt_escapes
- intentar_desenganche
- test_checks_escapes.py
- MultiattackAction
- Abilities
- test_relentless.py
- parse_escape
- ability_check
- Spell
- Spellcasting
- _duelo
- ConditionTracker
- SaveResult
- combat/attack.py
- tactics.py
- CheckResult
- effective_ac

## God Nodes (most connected - your core abstractions)
1. `attack_roll()` - 108 edges
2. `apply_condition()` - 107 edges
3. `Abilities` - 106 edges
4. `load_monster()` - 104 edges
5. `Attack` - 99 edges
6. `Condition` - 95 edges
7. `PlayerCharacter` - 83 edges
8. `CombatContext` - 82 edges
9. `Monster` - 74 edges
10. `run_combat()` - 73 edges

## Surprising Connections (you probably didn't know these)
- `Paquetes con fachada` --references--> `CombatResult`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/engine/combat/encounter.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Carpetas` --references--> `Monster`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Paquetes con fachada` --references--> `Spellcasting`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/rules/spells/casting.py
- `Paquetes con fachada` --references--> `spell_action()`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/rules/spells/casting.py

## Import Cycles
- None detected.

## Communities (69 total, 7 thin omitted)

### Community 0 - "ActionType"
Cohesion: 0.11
Nodes (8): ActionType, AttackAction, _contexto(), ExtendRageAction, RageAction, SpikedArmorAction, _queda_accion(), test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio()

### Community 1 - "test_attach.py"
Cohesion: 0.18
Nodes (25): _atacar(), _bite(), _cloaker(), _ctx(), _datos(), _pj(), test_con_ventaja_el_enganche_es_a_la_cabeza_y_ciega(), test_damage_transfer_no_aplica_sin_enganche() (+17 more)

### Community 2 - "test_ancestral_guardian.py"
Cohesion: 0.06
Nodes (30): AncestralGuardianFeatures, apply_ancestral_guardian(), BarbarianFeatures, _rasgo(), _abilities(), _aliado(), _ataque_fijo(), _barbaro() (+22 more)

### Community 3 - "test_usage.py"
Cohesion: 0.09
Nodes (23): UsageKind, _breath(), _eventos(), _FixedRandom, _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(), test_at_will_nunca_se_agota() (+15 more)

### Community 4 - "test_area.py"
Cohesion: 0.14
Nodes (24): sample(), AreaSaveAction, AreaTargeting, select_area_targets(), _default_targeting(), SaveDamage, _area_action(), _ctx() (+16 more)

### Community 5 - "load_monster"
Cohesion: 0.06
Nodes (51): doblar_dados(), _armor_class_value(), load_monster(), _norm_name(), ExtraDamage, _accion(), _ataque(), _ctx() (+43 more)

### Community 6 - "CombatContext"
Cohesion: 0.06
Nodes (21): pick(), _objetivo_enganche(), valid_targets(), actor_is_alive(), CombatAction, CombatContext, _living_enemies(), HealAction (+13 more)

### Community 8 - "test_conditions.py"
Cohesion: 0.17
Nodes (16): _data(), _load(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente(), test_el_ghoul_paraliza_con_diez_rondas_y_salvacion_de_repeticion(), test_el_hechizado_ahora_si_se_aplica(), test_el_lobo_derriba_con_la_salvacion_del_json(), test_el_lobo_no_derriba_si_el_ataque_falla(), test_el_lobo_solo_derriba_si_falla_la_salvacion() (+8 more)

### Community 9 - "spell_action"
Cohesion: 0.13
Nodes (23): spell_action(), _spell_data(), _spellcasting(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_lich_carga_sus_hechizos_utiles(), test_el_proyectil_magico_es_dano_automatico(), test_el_tiempo_de_casteo_marca_el_tipo_de_accion() (+15 more)

### Community 10 - "test_traits.py"
Cohesion: 0.11
Nodes (24): RollMode, _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _RasgoDeSalvacion, _sahuagin() (+16 more)

### Community 11 - "Condition"
Cohesion: 0.11
Nodes (41): Condition, attack_modifiers(), test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar() (+33 more)

### Community 12 - "_ctx"
Cohesion: 0.16
Nodes (19): resolve_attack_range(), _ataque(), _ctx(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja(), test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo(), test_dos_ventajas_y_una_desventaja_se_anulan() (+11 more)

### Community 13 - "random"
Cohesion: 0.21
Nodes (8): print_report(), simulate(), build_parser(), _build_party(), _load_party(), main(), _parse_monster_token(), test_informe_final_con_apartados_de_pj_y_monstruros()

### Community 14 - "Trait"
Cohesion: 0.07
Nodes (3): Trait, BloodFrenzy, test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 15 - "parse_spell"
Cohesion: 0.12
Nodes (11): _avisar(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla(), parse_spell(), _slot_table(), _sumar_dados() (+3 more)

### Community 16 - "DamageTransfer"
Cohesion: 0.15
Nodes (5): DamageTransfer, _empuna_arma_melee(), Parry, TurnResistance, _ve_al_atacante()

### Community 17 - "test_damage.py"
Cohesion: 0.27
Nodes (12): apply_damage_modifiers(), _guerrero_y_ogro(), _target(), test_danio_medio_por_combatiente_y_equipo(), test_etiqueta_de_modificadores_se_deriva_del_dano_final(), test_immunity_zero(), test_invalid_damage_type_raises(), test_no_modifiers_unchanged() (+4 more)

### Community 18 - "build_spell_actions"
Cohesion: 0.23
Nodes (9): build_spell_actions(), test_un_lanzador_carga_el_hechizo_con_su_uso_propio(), _desde_fixture(), _monstruo_lanzador(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_la_reaccion_gasta_su_uso_propio(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_uso_propio() (+1 more)

### Community 19 - "test_loader_actions.py"
Cohesion: 0.08
Nodes (21): _declara_uso(), _entradas(), _usage(), parse_usage(), UnknownUsageError, _warn(), _area_action(), _data() (+13 more)

### Community 20 - "test_multiattack.py"
Cohesion: 0.22
Nodes (12): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+4 more)

### Community 21 - "test_legendary.py"
Cohesion: 0.07
Nodes (61): ConditionEffect, legendary_phase(), test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _contexto(), _data(), _estado(), _legendaria(), _load() (+53 more)

### Community 22 - "inflict_damage"
Cohesion: 0.14
Nodes (9): _absorber_pv_temporales(), _hooks(), inflict_damage(), _is_petrified(), _mark_dead_if_down(), _mitigacion_de_otros(), _notify_damage_dealt(), _notify_damage_taken() (+1 more)

### Community 23 - "Attack"
Cohesion: 0.08
Nodes (51): _clamp(), extra_attacks_for(), rage_damage(), rage_uses(), Attack, apply_barbarian(), SaveModifiers, _abilities() (+43 more)

### Community 24 - "TurnResources"
Cohesion: 0.09
Nodes (37): AttackRange, TurnResources, apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), AttackModifiers, _abilities() (+29 more)

### Community 25 - "saves.py"
Cohesion: 0.08
Nodes (11): d20(), roll_d20(), roll_dice(), _finish_check(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save() (+3 more)

### Community 26 - "loader.py"
Cohesion: 0.05
Nodes (18): parse_attach_effects(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), parse_range_type(), _sentence_with(), _extract_multiattack_alternatives() (+10 more)

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 28 - "json"
Cohesion: 0.06
Nodes (35): Race, _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait() (+27 more)

### Community 29 - "traits/__init__.py"
Cohesion: 0.11
Nodes (5): aliados_capaces(), _condicion_posicional(), MartialAdvantage, PackTactics, SuperiorInvisibility

### Community 30 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 31 - "test_azer.py"
Cohesion: 0.08
Nodes (28): Cómo comprobar que todo sigue en orden, _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api(), _ataque_melee(), _ataque_ranged() (+20 more)

### Community 32 - "apply_condition"
Cohesion: 0.12
Nodes (18): _apply_condition_riders(), apply_condition(), _as_condition(), end_turn(), _label(), remove_condition(), RepeatSave, registrar_resistencia() (+10 more)

### Community 33 - "saving_throw"
Cohesion: 0.24
Nodes (10): save_modifiers(), saving_throw(), _datos(), _lich(), _pj(), test_con_ventaja_acierta_mas_que_sin_ella(), test_da_ventaja_si_la_salvacion_es_de_conversion(), test_el_lich_carga_su_turn_resistance() (+2 more)

### Community 34 - "test_skills.py"
Cohesion: 0.10
Nodes (25): _guia(), skill_bonus(), skill_check(), _abilities(), _ctx(), _load_fixture(), _pj(), _SoloMod (+17 more)

### Community 35 - "test_backgrounds.py"
Cohesion: 0.11
Nodes (19): Background, normalize_tool(), _add(), load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias() (+11 more)

### Community 36 - "legendary.py"
Cohesion: 0.09
Nodes (11): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), legendary_resistance(), LegendaryAction (+3 more)

### Community 37 - "test_proficiency.py"
Cohesion: 0.17
Nodes (21): proficiency_bonus(), ability_check_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia() (+13 more)

### Community 38 - "run_combat"
Cohesion: 0.16
Nodes (9): combat_finished(), living_teams(), CombatResult, _invoke_policy(), roll_initiative(), run_combat(), _run_combat(), _summarize_damage() (+1 more)

### Community 39 - "parse_damage_type"
Cohesion: 0.08
Nodes (7): DamageType, parse_damage_type(), _es_radiante(), _guardar_salvacion(), Regeneration, Relentless, UndeadFortitude

### Community 40 - "roll_modifiers.py"
Cohesion: 0.16
Nodes (5): _resolve_mods(), check_modifiers(), CheckModifiers, _condiciones(), _hooks()

### Community 41 - "attack_roll"
Cohesion: 0.07
Nodes (58): D20Result, parse_traits(), _actualizar_distancia(), attack_roll(), remove_invisibility_on_action(), _azer(), _ctx(), _datos() (+50 more)

### Community 42 - "begin_turn"
Cohesion: 0.27
Nodes (15): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+7 more)

### Community 43 - "dnd_sim/__init__.py"
Cohesion: 0.07
Nodes (10): ability_mod(), CombatState, log_line(), build_save_action(), _log(), SaveAction, WeaponAttackAction, CombatantType (+2 more)

### Community 44 - "legendary_parser.py"
Cohesion: 0.07
Nodes (20): is_area_action(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary() (+12 more)

### Community 45 - "test_spells.py"
Cohesion: 0.17
Nodes (17): _ctx(), _npc(), _pj(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado(), test_el_hechizo_verdadero_es_un_ataque_real_con_dano_extra(), test_el_proyectil_magico_pasa_por_los_modificadores_de_dano() (+9 more)

### Community 46 - "PlayerCharacter"
Cohesion: 0.08
Nodes (8): Arquitectura de `dnd_sim`, Carpetas, Excepción única admitida, Imports diferidos, Reglas de dependencia, normalize_ability(), Combatant, PlayerCharacter

### Community 47 - "normalize_skill"
Cohesion: 0.17
Nodes (6): _clean(), normalize_skill(), skill_ability(), test_caracteristica_asociada(), test_normalize_skill_acepta_espacios_y_spanish(), test_normalize_skill_desconocida_lanza_value_error()

### Community 48 - "attempt_escapes"
Cohesion: 0.29
Nodes (3): attempt_escapes(), _contar(), test_una_condicion_sin_escape_no_genera_intentos()

### Community 49 - "intentar_desenganche"
Cohesion: 0.16
Nodes (6): Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por()

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.18
Nodes (25): EscapeCheck, _ctx(), _load(), _pj(), test_con_dos_caracteristicas_se_elige_una_al_azar(), test_con_una_sola_caracteristica_no_consume_rng(), test_consumes_action_gasta_la_accion_del_turno(), test_dos_instancias_consumes_action_solo_intenta_la_primera() (+17 more)

### Community 52 - "Abilities"
Cohesion: 0.11
Nodes (17): Abilities, Monster, test_dos_combates_seguidos_empiezan_sin_condiciones(), test_inmovilizado_da_desventaja_solo_en_des(), test_la_politica_no_se_invoca_para_un_incapacitado(), test_las_condiciones_incapacitantes_fallan_fue_y_des_sin_tirar_dados(), test_las_condiciones_incapacitantes_no_fallan_automaticamente_la_con(), test_petrificado_tiene_resistencia_a_todo() (+9 more)

### Community 53 - "test_relentless.py"
Cohesion: 0.27
Nodes (12): _ctx(), _datos(), _jabali(), _pj(), test_el_jabali_carga_su_relentless_con_umbral_y_uso(), test_relentless_no_necesita_contexto_ni_rng(), test_reset_reestablece_el_umbral_y_los_usos(), test_solo_puede_salvarse_una_vez_por_combate() (+4 more)

### Community 54 - "parse_escape"
Cohesion: 0.18
Nodes (6): has_escape_text(), parse_escape(), _skills_for(), _data(), test_el_fixture_de_la_constriccion_tiene_escape_y_avisa_de_grappled(), test_el_fixture_de_la_telaraña_carga_restrained_con_escape()

### Community 57 - "ability_check"
Cohesion: 0.15
Nodes (8): ability_check(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_probabilidad_de_liberarse_con_cd_12(), test_prueba_con_envenenado_o_aterrorizado_da_desventaja(), test_prueba_con_ventaja_da_75_por_ciento(), test_prueba_de_caracteristica_con_bonus_0_da_50_por_ciento(), test_sin_autoexito_ni_autofallo_en_pruebas(), test_ventaja_y_desventaja_se_anulan()

### Community 59 - "Spell"
Cohesion: 0.25
Nodes (4): Paquetes con fachada, _uso_de_entrada(), Spell, test_un_hechizo_de_accion_bonus_se_comprueba_en_su_fase()

### Community 61 - "Spellcasting"
Cohesion: 0.14
Nodes (10): parse_spellcasting(), Spellcasting, _spell_data(), test_el_hechizo_enlarge_es_un_estado_self(), test_lanzar_el_hechizo_agranda_al_lanzador(), test_el_lanzador_se_lee_de_los_actions(), test_el_upcast_reescala_el_dano_y_la_curacion(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo() (+2 more)

### Community 62 - "_duelo"
Cohesion: 0.31
Nodes (7): _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

### Community 63 - "ConditionTracker"
Cohesion: 0.22
Nodes (3): ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 64 - "SaveResult"
Cohesion: 0.32
Nodes (6): _log_target(), _mode_tag(), _outcome_tag(), _log_line_outcome(), SaveResult, fake_saving_throw()

### Community 65 - "combat/attack.py"
Cohesion: 0.11
Nodes (14): _agrandado(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), _mode_tag(), _reaccion_si_procede(), resolve_roll_mode() (+6 more)

### Community 66 - "tactics.py"
Cohesion: 0.38
Nodes (3): _extract(), first_target_policy(), random_policy()

### Community 67 - "CheckResult"
Cohesion: 0.50
Nodes (3): CheckResult, _check_fijo(), _fake()

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Trait` connect `Trait` to `ActionType`, `combat/attack.py`, `test_ancestral_guardian.py`, `parse_damage_type`, `attack_roll`, `test_traits.py`, `dnd_sim/__init__.py`, `DamageTransfer`, `intentar_desenganche`, `test_loader_actions.py`, `TurnResources`, `saves.py`, `Spell`, `traits/__init__.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `attack_roll()` (e.g. with `Attack` and `Combatant`) actually correct?**
  _`attack_roll()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `ActionType` be split into smaller, more focused modules?**
  _Cohesion score 0.11375661375661375 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `ActionType`, `test_attach.py`, `test_ancestral_guardian.py`, `load_monster`, `CombatContext`, `test_conditions.py`, `spell_action`, `test_traits.py`, `parse_spell`, `DamageTransfer`, `test_damage.py`, `test_legendary.py`, `inflict_damage`, `saves.py`, `loader.py`, `traits/__init__.py`, `apply_condition`, `saving_throw`, `test_skills.py`, `roll_modifiers.py`, `attack_roll`, `dnd_sim/__init__.py`, `test_spells.py`, `PlayerCharacter`, `intentar_desenganche`, `test_checks_escapes.py`, `Abilities`, `Spellcasting`, `ConditionTracker`, `combat/attack.py`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `UnknownUsageError` and `ActionType`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_ancestral_guardian.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06127206127206127 - nodes in this community are weakly interconnected._
- **Why does `load_monster()` connect `load_monster` to `ActionType`, `test_attach.py`, `test_usage.py`, `test_area.py`, `CombatContext`, `test_conditions.py`, `spell_action`, `test_traits.py`, `Condition`, `random`, `test_damage.py`, `build_spell_actions`, `test_loader_actions.py`, `test_multiattack.py`, `test_legendary.py`, `Attack`, `loader.py`, `test_death.py`, `json`, `test_undead_fortitude.py`, `test_azer.py`, `saving_throw`, `test_skills.py`, `attack_roll`, `begin_turn`, `dnd_sim/__init__.py`, `legendary_parser.py`, `test_spells.py`, `PlayerCharacter`, `normalize_skill`, `intentar_desenganche`, `test_checks_escapes.py`, `MultiattackAction`, `Abilities`, `test_relentless.py`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
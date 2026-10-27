# Graph Report - DnDBalancer  (2026-10-27)

## Corpus Check
- 150 files · ~87,138 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 1600 nodes · 5531 edges · 58 communities (49 shown, 9 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 332 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8d4e31e3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CombatContext
- test_attach.py
- trait_parser.py
- ActionUsage
- test_area.py
- test_enlarge.py
- spell_action
- test_conditions.py
- test_spells.py
- test_traits.py
- Condition
- _ctx
- PlayerCharacter
- Trait
- spell_parser.py
- DamageTransfer
- test_damage.py
- build_spell_actions
- test_loader_actions.py
- parse_traits
- test_legendary.py
- model/attack.py
- LegendaryState
- AttackModifiers
- saves.py
- normalize_ability
- run_combat
- test_loader.py
- dnd_sim/__init__.py
- test_undead_fortitude.py
- test_martial_advantage.py
- apply_condition
- RollMode
- test_pack_tactics.py
- Regeneration
- attack_modifiers
- attack_roll
- inflict_damage
- conditions.py
- load_monster
- damage.py
- test_superior_invisibility.py
- test_checks_escapes.py
- Abilities
- test_usage.py
- multiattack_parser.py
- Spellcasting
- test_regeneration.py
- ConditionTracker
- ConditionAction
- roll_modifiers.py
- TurnResources

## God Nodes (most connected - your core abstractions)
1. `apply_condition()` - 106 edges
2. `attack_roll()` - 103 edges
3. `load_monster()` - 102 edges
4. `Condition` - 92 edges
5. `Abilities` - 91 edges
6. `CombatContext` - 80 edges
7. `Attack` - 79 edges
8. `run_combat()` - 73 edges
9. `Monster` - 67 edges
10. `PlayerCharacter` - 64 edges

## Surprising Connections (you probably didn't know these)
- `Paquetes con fachada` --references--> `CombatResult`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/engine/combat/encounter.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Carpetas` --references--> `PlayerCharacter`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Carpetas` --references--> `Monster`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Paquetes con fachada` --references--> `Spellcasting`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/rules/spells/casting.py

## Import Cycles
- None detected.

## Communities (58 total, 9 thin omitted)

### Community 0 - "CombatContext"
Cohesion: 0.09
Nodes (13): pick(), valid_targets(), actor_is_alive(), AttackEntry, CombatContext, _living_enemies(), _log(), WeaponAttackAction (+5 more)

### Community 1 - "test_attach.py"
Cohesion: 0.09
Nodes (32): parse_attach_effects(), Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), _atacar() (+24 more)

### Community 2 - "trait_parser.py"
Cohesion: 0.15
Nodes (8): _resistencia_legendaria(), _declara_uso(), _usage(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 3 - "ActionUsage"
Cohesion: 0.21
Nodes (11): ActionUsage, UsageKind, test_at_will_nunca_se_agota(), test_media_de_turnos_hasta_recargar(), test_per_day_dos_usos_y_luego_can_use_falso(), test_per_day_no_tira_recarga(), test_per_day_reset_restaura_todos_los_usos(), test_recharge_5_6_porcentaje_de_exito() (+3 more)

### Community 4 - "test_area.py"
Cohesion: 0.16
Nodes (22): sample(), AreaTargeting, select_area_targets(), SaveDamage, _area_action(), _ctx(), _npc(), _pj() (+14 more)

### Community 5 - "test_enlarge.py"
Cohesion: 0.15
Nodes (24): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+16 more)

### Community 6 - "spell_action"
Cohesion: 0.09
Nodes (15): Paquetes con fachada, AttackAction, CombatAction, SaveAction, HealAction, SpellAction, SpellAttackAction, SpellFixedDamageAction (+7 more)

### Community 8 - "test_conditions.py"
Cohesion: 0.15
Nodes (22): _data(), _load(), _pj(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente(), test_can_act_y_can_react(), test_condicion_fuera_del_enum_lanza_value_error(), test_el_ghoul_paraliza_con_diez_rondas_y_salvacion_de_repeticion(), test_el_hechizado_ahora_si_se_aplica() (+14 more)

### Community 9 - "test_spells.py"
Cohesion: 0.10
Nodes (44): parse_spell(), apply_concentration(), _ctx(), _npc(), _pj(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion() (+36 more)

### Community 10 - "test_traits.py"
Cohesion: 0.12
Nodes (21): _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _sahuagin(), _sahuagin_con_rasgo(), test_blood_frenzy_actua_durante_el_combate_completo() (+13 more)

### Community 11 - "Condition"
Cohesion: 0.19
Nodes (26): Condition, test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+18 more)

### Community 12 - "_ctx"
Cohesion: 0.16
Nodes (20): resolve_attack_range(), _ataque(), _ctx(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja(), test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo(), test_dos_ventajas_y_una_desventaja_se_anulan() (+12 more)

### Community 13 - "PlayerCharacter"
Cohesion: 0.13
Nodes (15): print_report(), simulate(), PlayerCharacter, build_parser(), _build_party(), _load_party(), main(), _parse_monster_token() (+7 more)

### Community 14 - "Trait"
Cohesion: 0.09
Nodes (3): Trait, BloodFrenzy, test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 15 - "spell_parser.py"
Cohesion: 0.07
Nodes (12): _afecta_movimiento(), _condicion_con_salvacion(), _crea_objetos(), _dados_de_dano(), _elementos_totales(), _es_ilusion(), _numero_elementos(), _opciones_de_dano() (+4 more)

### Community 16 - "DamageTransfer"
Cohesion: 0.23
Nodes (3): DamageTransfer, _empuna_arma_melee(), _ve_al_atacante()

### Community 17 - "test_damage.py"
Cohesion: 0.29
Nodes (10): apply_damage_modifiers(), _is_petrified(), _target(), test_etiqueta_de_modificadores_se_deriva_del_dano_final(), test_immunity_zero(), test_invalid_damage_type_raises(), test_no_modifiers_unchanged(), test_resistance_halves_damage_floor() (+2 more)

### Community 18 - "build_spell_actions"
Cohesion: 0.39
Nodes (7): build_spell_actions(), _desde_fixture(), _monstruo_lanzador(), test_gastar_un_slot_no_afecta_a_los_otros_niveles(), test_la_reaccion_gasta_el_slot_de_su_nivel(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_un_pool_por_nivel()

### Community 19 - "test_loader_actions.py"
Cohesion: 0.18
Nodes (13): _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga(), test_ataque_con_usage_conserva_el_actionusage() (+5 more)

### Community 20 - "parse_traits"
Cohesion: 0.22
Nodes (7): _entradas(), parse_traits(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd(), test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad(), test_el_umbral_se_saca_de_cada_descripcion(), test_el_rasgo_se_parsea_desde_el_srd(), test_parse_traits_ignora_entradas_malformadas()

### Community 21 - "test_legendary.py"
Cohesion: 0.07
Nodes (60): ConditionEffect, legendary_phase(), test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _contexto(), _data(), _estado(), _legendaria(), _load() (+52 more)

### Community 22 - "model/attack.py"
Cohesion: 0.21
Nodes (4): AttackRange, DamageType, parse_damage_type(), ExtraDamage

### Community 23 - "LegendaryState"
Cohesion: 0.12
Nodes (6): _accion_utilizable(), _acciones_asequibles(), LegendaryAction, LegendaryState, _presupuesto(), test_resistance_probability_medio_convierte_about_50_por_ciento()

### Community 25 - "saves.py"
Cohesion: 0.08
Nodes (23): _apply_condition_riders(), _log_target(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), legendary_resistance(), registrar_resistencia_legendaria() (+15 more)

### Community 27 - "run_combat"
Cohesion: 0.05
Nodes (41): combat_finished(), living_teams(), _objetivo_enganche(), CombatResult, _invoke_policy(), roll_initiative(), run_combat(), _run_combat() (+33 more)

### Community 28 - "test_loader.py"
Cohesion: 0.07
Nodes (17): _cache_path(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError, _armor_class_value(), MultiattackAction, _load_fixture() (+9 more)

### Community 29 - "dnd_sim/__init__.py"
Cohesion: 0.06
Nodes (16): ability_mod(), d20(), D20Result, roll_d20(), roll_dice(), HeatedBody, Parry, TurnResistance (+8 more)

### Community 30 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 31 - "test_martial_advantage.py"
Cohesion: 0.08
Nodes (25): Cómo comprobar que todo sigue en orden, _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api(), _aliado(), _ctx() (+17 more)

### Community 32 - "apply_condition"
Cohesion: 0.23
Nodes (9): apply_condition(), end_turn(), _label(), RepeatSave, test_dos_instancias_de_la_misma_condicion_de_fuentes_distintas(), test_repeat_save_con_exito_elimina_la_condicion_al_final_del_turno(), test_repeat_save_con_fallo_la_condicion_sigue_y_la_duracion_baja(), test_una_condicion_de_2_rondas_termina_al_final_del_segundo_turno() (+1 more)

### Community 33 - "RollMode"
Cohesion: 0.13
Nodes (14): RollMode, CheckModifiers, save_modifiers(), SaveModifiers, _RasgoDeSalvacion, test_el_hook_de_salvaciones_alimenta_save_modifiers(), _datos(), _lich() (+6 more)

### Community 37 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 39 - "Regeneration"
Cohesion: 0.19
Nodes (3): _es_radiante(), _guardar_salvacion(), Regeneration

### Community 40 - "attack_modifiers"
Cohesion: 0.33
Nodes (4): attack_modifiers(), check_modifiers(), _condiciones(), _hooks()

### Community 41 - "attack_roll"
Cohesion: 0.07
Nodes (63): Arquitectura de `dnd_sim`, Carpetas, Excepción única admitida, Imports diferidos, Reglas de dependencia, _actualizar_distancia(), attack_roll(), _mode_tag() (+55 more)

### Community 42 - "inflict_damage"
Cohesion: 0.26
Nodes (13): inflict_damage(), _ctx(), _datos(), _jabali(), _pj(), test_el_jabali_carga_su_relentless_con_umbral_y_uso(), test_relentless_no_necesita_contexto_ni_rng(), test_reset_reestablece_el_umbral_y_los_usos() (+5 more)

### Community 43 - "conditions.py"
Cohesion: 0.08
Nodes (4): CombatState, log_line(), CombatantType, _default_targeting()

### Community 44 - "load_monster"
Cohesion: 0.05
Nodes (33): is_area_action(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), parse_range_type(), _sentence_with(), _coincide_nombre() (+25 more)

### Community 46 - "damage.py"
Cohesion: 0.14
Nodes (5): _hooks(), _mark_dead_if_down(), _notify_damage_dealt(), _notify_damage_taken(), _salvar_a_cero()

### Community 47 - "test_superior_invisibility.py"
Cohesion: 0.15
Nodes (16): _as_condition(), _contar(), _queda_accion(), remove_condition(), remove_invisibility_on_action(), _accion(), _ctx(), _pixie() (+8 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.06
Nodes (54): has_escape_text(), parse_escape(), ability_check(), ability_check_bonus(), CheckResult, _guia(), attempt_escapes(), EscapeCheck (+46 more)

### Community 52 - "Abilities"
Cohesion: 0.13
Nodes (13): Abilities, Monster, test_dos_combates_seguidos_empiezan_sin_condiciones(), test_inmovilizado_da_desventaja_solo_en_des(), test_la_politica_no_se_invoca_para_un_incapacitado(), test_las_condiciones_incapacitantes_no_fallan_automaticamente_la_con(), test_petrificado_tiene_resistencia_a_todo(), test_sin_condiciones_el_dano_no_cambia() (+5 more)

### Community 53 - "test_usage.py"
Cohesion: 0.24
Nodes (10): _eventos(), _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(), test_copias_de_un_monstruo_tienen_estado_independiente(), test_dos_combates_seguidos_empiezan_con_el_aliento_cargado(), test_dragon_nunca_usa_el_aliento_dos_turnos_seguidos_sin_recarga(), test_politica_elige_el_aliento_aproximadamente_el_50_cuando_esta_cargado() (+2 more)

### Community 57 - "multiattack_parser.py"
Cohesion: 0.25
Nodes (3): extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada()

### Community 61 - "Spellcasting"
Cohesion: 0.20
Nodes (6): parse_spellcasting(), Spellcasting, test_el_hechizo_enlarge_es_un_estado_self(), test_el_lanzador_se_lee_de_los_special_abilities(), test_initialize_slots_usa_la_tabla_real_de_un_lanzador_completo(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 62 - "test_regeneration.py"
Cohesion: 0.30
Nodes (13): _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno(), test_el_troll_carga_su_regeneracion() (+5 more)

### Community 63 - "ConditionTracker"
Cohesion: 0.22
Nodes (3): ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 65 - "roll_modifiers.py"
Cohesion: 0.08
Nodes (13): _agrandado(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), _reaccion_si_procede(), resolve_roll_mode(), _tag_modificadores() (+5 more)

### Community 66 - "TurnResources"
Cohesion: 0.18
Nodes (5): TurnResources, _breath(), _FixedRandom, test_begin_turn_no_tira_nada_si_estan_cargadas(), test_begin_turn_reinicia_recursos_y_tira_una_recarga_por_accion()

## Knowledge Gaps
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `load_monster` to `CombatContext`, `test_attach.py`, `trait_parser.py`, `test_area.py`, `test_enlarge.py`, `spell_action`, `test_conditions.py`, `test_spells.py`, `test_traits.py`, `Condition`, `PlayerCharacter`, `spell_parser.py`, `test_damage.py`, `build_spell_actions`, `test_loader_actions.py`, `parse_traits`, `test_legendary.py`, `model/attack.py`, `normalize_ability`, `run_combat`, `test_loader.py`, `dnd_sim/__init__.py`, `test_undead_fortitude.py`, `test_martial_advantage.py`, `RollMode`, `test_pack_tactics.py`, `attack_roll`, `inflict_damage`, `conditions.py`, `test_checks_escapes.py`, `Abilities`, `test_usage.py`, `test_regeneration.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `attack_roll()` (e.g. with `Attack` and `Combatant`) actually correct?**
  _`attack_roll()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `CombatContext` be split into smaller, more focused modules?**
  _Cohesion score 0.08708272859216255 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `test_enlarge.py`, `test_conditions.py`, `test_spells.py`, `test_traits.py`, `spell_parser.py`, `DamageTransfer`, `test_damage.py`, `test_legendary.py`, `dnd_sim/__init__.py`, `apply_condition`, `RollMode`, `test_pack_tactics.py`, `attack_modifiers`, `attack_roll`, `conditions.py`, `load_monster`, `damage.py`, `test_superior_invisibility.py`, `test_checks_escapes.py`, `Abilities`, `Spellcasting`, `ConditionTracker`, `roll_modifiers.py`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `UnknownUsageError` and `ActionType`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09288824383164006 - nodes in this community are weakly interconnected._
- **Why does `run_combat()` connect `run_combat` to `CombatContext`, `test_attach.py`, `test_enlarge.py`, `test_conditions.py`, `test_spells.py`, `test_traits.py`, `Condition`, `PlayerCharacter`, `test_damage.py`, `test_legendary.py`, `test_loader.py`, `dnd_sim/__init__.py`, `test_undead_fortitude.py`, `test_martial_advantage.py`, `apply_condition`, `test_pack_tactics.py`, `attack_roll`, `inflict_damage`, `test_superior_invisibility.py`, `test_checks_escapes.py`, `Abilities`, `test_usage.py`, `test_regeneration.py`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
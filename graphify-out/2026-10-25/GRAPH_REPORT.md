# Graph Report - DnDBalancer  (2026-10-25)

## Corpus Check
- 149 files · ~85,032 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 1568 nodes · 5395 edges · 62 communities (50 shown, 12 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 325 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6cc4368b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CombatContext
- test_attach.py
- loader.py
- run_combat
- test_area.py
- test_enlarge.py
- dnd_sim/__init__.py
- json
- test_spells.py
- test_traits.py
- Condition
- apply_condition
- PlayerCharacter
- Trait
- usage.py
- defense.py
- combat/__init__.py
- LegendaryState
- combat/attack.py
- test_legendary.py
- legendary_phase
- SaveDamage
- legendary.py
- RollMode
- saves.py
- condition_parser.py
- combatant.py
- load_monster
- traits/__init__.py
- test_undead_fortitude.py
- test_martial_advantage.py
- begin_turn
- saving_throw
- area.py
- typing
- ability_check
- test_pack_tactics.py
- conditions.py
- Regeneration
- roll_modifiers.py
- attack_roll
- inflict_damage
- Combatant
- legendary_parser.py
- intentar_desenganche
- damage.py
- test_superior_invisibility.py
- roll_dice
- AreaSaveAction
- test_checks_escapes.py
- registrar_resistencia
- SaveResult
- trigger_reaction
- _default_targeting

## God Nodes (most connected - your core abstractions)
1. `apply_condition()` - 106 edges
2. `load_monster()` - 100 edges
3. `attack_roll()` - 100 edges
4. `Condition` - 92 edges
5. `Abilities` - 88 edges
6. `CombatContext` - 78 edges
7. `Attack` - 77 edges
8. `run_combat()` - 67 edges
9. `Monster` - 65 edges
10. `PlayerCharacter` - 62 edges

## Surprising Connections (you probably didn't know these)
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Paquetes con fachada` --references--> `CombatResult`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/engine/combat/encounter.py
- `Carpetas` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Carpetas` --references--> `PlayerCharacter`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Carpetas` --references--> `Monster`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py

## Import Cycles
- None detected.

## Communities (62 total, 12 thin omitted)

### Community 0 - "CombatContext"
Cohesion: 0.10
Nodes (8): pick(), _objetivo_enganche(), valid_targets(), CombatContext, _living_enemies(), _log(), _equipos_vivos(), _romper_invisibilidad_al_lanzar()

### Community 1 - "test_attach.py"
Cohesion: 0.18
Nodes (25): _atacar(), _bite(), _cloaker(), _ctx(), _datos(), _pj(), test_con_ventaja_el_enganche_es_a_la_cabeza_y_ciega(), test_damage_transfer_no_aplica_sin_enganche() (+17 more)

### Community 2 - "loader.py"
Cohesion: 0.07
Nodes (16): parse_attach_effects(), _resistencia_legendaria(), _extract_multiattack_alternatives(), _norm_name(), _simple_damage_modifiers(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada() (+8 more)

### Community 3 - "run_combat"
Cohesion: 0.06
Nodes (39): run_combat(), TurnResources, ActionUsage, UsageKind, _data(), _load(), _pj(), _raw_multiattack() (+31 more)

### Community 4 - "test_area.py"
Cohesion: 0.27
Nodes (19): AreaTargeting, select_area_targets(), _area_action(), _ctx(), _npc(), _pj(), _save_forzado(), fake_saving_throw() (+11 more)

### Community 5 - "test_enlarge.py"
Cohesion: 0.15
Nodes (25): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+17 more)

### Community 6 - "dnd_sim/__init__.py"
Cohesion: 0.07
Nodes (20): Paquetes con fachada, ActionType, CombatAction, SaveAction, ConditionAction, HealAction, SpellAction, SpellAttackAction (+12 more)

### Community 8 - "json"
Cohesion: 0.13
Nodes (6): _cache_path(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError, test_cache_avoids_second_network()

### Community 9 - "test_spells.py"
Cohesion: 0.05
Nodes (64): _afecta_movimiento(), build_spell_actions(), _crea_objetos(), _dados_de_dano(), _elementos_totales(), _es_ilusion(), _numero_elementos(), _opciones_de_dano() (+56 more)

### Community 10 - "test_traits.py"
Cohesion: 0.12
Nodes (23): attack_modifiers(), _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _RasgoDeSalvacion, _sahuagin() (+15 more)

### Community 11 - "Condition"
Cohesion: 0.19
Nodes (26): Condition, test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+18 more)

### Community 12 - "apply_condition"
Cohesion: 0.06
Nodes (65): Abilities, parse_range_type(), Monster, apply_condition(), ConditionInstance, ConditionTracker, end_turn(), RepeatSave (+57 more)

### Community 13 - "PlayerCharacter"
Cohesion: 0.07
Nodes (37): _tag_modificadores(), print_report(), simulate(), PlayerCharacter, apply_damage_modifiers(), build_parser(), _build_party(), _load_party() (+29 more)

### Community 14 - "Trait"
Cohesion: 0.09
Nodes (3): Trait, BloodFrenzy, test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 15 - "usage.py"
Cohesion: 0.11
Nodes (3): log_line(), has_condition_text(), UndeadFortitude

### Community 16 - "defense.py"
Cohesion: 0.13
Nodes (6): DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante()

### Community 17 - "combat/__init__.py"
Cohesion: 0.18
Nodes (8): CombatResult, _invoke_policy(), roll_initiative(), _run_combat(), _summarize_damage(), _extract(), first_target_policy(), random_policy()

### Community 18 - "LegendaryState"
Cohesion: 0.14
Nodes (5): LegendaryState, _estado(), test_el_estado_legendario_rellena_gasta_y_reinicia(), test_resistance_probability_medio_convierte_about_50_por_ciento(), test_use_probability_medio_se_usa_about_50_por_ciento()

### Community 19 - "combat/attack.py"
Cohesion: 0.13
Nodes (9): _actualizar_distancia(), _agrandado(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), _mode_tag(), _reaccion_si_procede() (+1 more)

### Community 20 - "test_legendary.py"
Cohesion: 0.10
Nodes (25): _data(), _load(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_con_use_probability_uno_el_danio_es_mayor_que_con_cero(), test_el_ala_que_mezcla_movimiento_avisa(), test_el_cantrip_del_lich_se_omite_con_aviso(), test_el_cli_tiene_las_opciones_legendarias() (+17 more)

### Community 21 - "legendary_phase"
Cohesion: 0.12
Nodes (30): legendary_phase(), _contexto(), _pj(), test_con_una_sola_accion_asequible_pick_no_consume_rng(), test_dos_duenos_legendarios_actuan_cada_uno_una_vez(), test_el_combate_termina_en_medio_de_la_fase(), test_el_dragon_contra_un_grupo_usa_acciones_legendarias(), test_la_fase_ocurre_despues_del_end_turn() (+22 more)

### Community 22 - "SaveDamage"
Cohesion: 0.12
Nodes (8): normalize_ability(), _damage_type(), build_save_effect(), damage_dice_of(), damage_options(), damage_type_of(), _dc_ability(), SaveDamage

### Community 23 - "legendary.py"
Cohesion: 0.12
Nodes (10): _accion_utilizable(), _acciones_asequibles(), _combate_terminado(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), LegendaryAction (+2 more)

### Community 24 - "RollMode"
Cohesion: 0.11
Nodes (6): RollMode, resolve_roll_mode(), AttackModifiers, CheckModifiers, SaveModifiers, test_el_tipo_de_efecto_kind_llega_a_los_rasgos()

### Community 25 - "saves.py"
Cohesion: 0.16
Nodes (9): legendary_resistance(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save(), _reaccion_si_procede(), _resolve_mode_str(), resolve_save_damage() (+1 more)

### Community 26 - "condition_parser.py"
Cohesion: 0.08
Nodes (11): _condition_from_phrase(), _duration_rounds(), _sentence_with(), has_escape_text(), parse_escape(), _condicion_con_salvacion(), ConditionEffect, _data() (+3 more)

### Community 27 - "combatant.py"
Cohesion: 0.17
Nodes (4): AttackRange, DamageType, parse_damage_type(), ExtraDamage

### Community 28 - "load_monster"
Cohesion: 0.19
Nodes (13): _armor_class_value(), load_monster(), MultiattackAction, _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper() (+5 more)

### Community 29 - "traits/__init__.py"
Cohesion: 0.16
Nodes (4): aliados_capaces(), _condicion_posicional(), MartialAdvantage, PackTactics

### Community 30 - "test_undead_fortitude.py"
Cohesion: 0.20
Nodes (15): _ctx(), _datos(), _pj(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido() (+7 more)

### Community 31 - "test_martial_advantage.py"
Cohesion: 0.06
Nodes (30): Arquitectura de `dnd_sim`, Carpetas, Cómo comprobar que todo sigue en orden, Excepción única admitida, Imports diferidos, Reglas de dependencia, _capa(), _modulo_y_paquete() (+22 more)

### Community 32 - "begin_turn"
Cohesion: 0.13
Nodes (27): EscapeCheck, begin_turn(), _check_fijo(), _ctx(), _load(), _pj(), test_con_dos_caracteristicas_se_elige_una_al_azar(), test_con_una_sola_caracteristica_no_consume_rng() (+19 more)

### Community 33 - "saving_throw"
Cohesion: 0.24
Nodes (10): save_modifiers(), saving_throw(), _datos(), _lich(), _pj(), test_con_ventaja_acierta_mas_que_sin_ella(), test_da_ventaja_si_la_salvacion_es_de_conversion(), test_el_lich_carga_su_turn_resistance() (+2 more)

### Community 34 - "area.py"
Cohesion: 0.24
Nodes (3): sample(), test_sample_devuelve_todos_sin_consumir_rng(), test_sample_k_menor_devuelve_distintos_y_uniformes()

### Community 36 - "ability_check"
Cohesion: 0.10
Nodes (12): ability_check(), ability_check_bonus(), CheckResult, _guia(), _fake(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_probabilidad_de_liberarse_con_cd_12(), test_prueba_con_envenenado_o_aterrorizado_da_desventaja() (+4 more)

### Community 37 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 38 - "conditions.py"
Cohesion: 0.18
Nodes (7): _as_condition(), attempt_escapes(), _contar(), _label(), _queda_accion(), remove_condition(), remove_invisibility_on_action()

### Community 39 - "Regeneration"
Cohesion: 0.14
Nodes (4): _es_radiante(), _guardar_salvacion(), Regeneration, Relentless

### Community 40 - "roll_modifiers.py"
Cohesion: 0.18
Nodes (4): _hooks(), hooks(), test_el_catalogo_cubre_hooks_que_los_rasgos_aun_no_usan(), test_hooks_con_un_nombre_fuera_del_catalogo_lanza_error()

### Community 41 - "attack_roll"
Cohesion: 0.08
Nodes (58): D20Result, attack_roll(), Attack, DamageRecorder, _ataque_melee(), _ataque_ranged(), _azer(), _ctx() (+50 more)

### Community 42 - "inflict_damage"
Cohesion: 0.26
Nodes (13): inflict_damage(), _ctx(), _datos(), _jabali(), _pj(), test_el_jabali_carga_su_relentless_con_umbral_y_uso(), test_relentless_no_necesita_contexto_ni_rng(), test_reset_reestablece_el_umbral_y_los_usos() (+5 more)

### Community 43 - "Combatant"
Cohesion: 0.16
Nodes (5): CombatState, AttackAction, WeaponAttackAction, Combatant, CombatantType

### Community 44 - "legendary_parser.py"
Cohesion: 0.09
Nodes (15): is_area_action(), parse_condition_effects(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas() (+7 more)

### Community 45 - "intentar_desenganche"
Cohesion: 0.16
Nodes (6): Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por()

### Community 46 - "damage.py"
Cohesion: 0.16
Nodes (5): _hooks(), _is_petrified(), _notify_damage_dealt(), _notify_damage_taken(), _salvar_a_cero()

### Community 47 - "test_superior_invisibility.py"
Cohesion: 0.09
Nodes (34): _declara_uso(), _entradas(), parse_traits(), _usage(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd(), _ctx(), _datos(), _pj() (+26 more)

### Community 48 - "roll_dice"
Cohesion: 0.25
Nodes (3): d20(), roll_d20(), roll_dice()

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.16
Nodes (13): check_modifiers(), _condiciones(), effective_ac(), resolve_attack_range(), _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto() (+5 more)

### Community 51 - "registrar_resistencia"
Cohesion: 0.29
Nodes (3): _apply_condition_riders(), registrar_resistencia_legendaria(), registrar_resistencia()

### Community 52 - "SaveResult"
Cohesion: 0.38
Nodes (5): _log_target(), _mode_tag(), _outcome_tag(), _log_line_outcome(), SaveResult

## Knowledge Gaps
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `load_monster` to `test_attach.py`, `loader.py`, `run_combat`, `test_enlarge.py`, `dnd_sim/__init__.py`, `json`, `test_spells.py`, `test_traits.py`, `Condition`, `apply_condition`, `PlayerCharacter`, `usage.py`, `test_legendary.py`, `SaveDamage`, `combatant.py`, `test_undead_fortitude.py`, `test_martial_advantage.py`, `begin_turn`, `saving_throw`, `test_pack_tactics.py`, `attack_roll`, `inflict_damage`, `Combatant`, `legendary_parser.py`, `intentar_desenganche`, `test_superior_invisibility.py`, `test_checks_escapes.py`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `UnknownUsageError` and `ActionType`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `CombatContext` be split into smaller, more focused modules?**
  _Cohesion score 0.09957325746799431 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `loader.py`, `test_enlarge.py`, `dnd_sim/__init__.py`, `test_spells.py`, `test_traits.py`, `apply_condition`, `PlayerCharacter`, `usage.py`, `defense.py`, `combat/attack.py`, `test_legendary.py`, `condition_parser.py`, `combatant.py`, `saving_throw`, `typing`, `ability_check`, `test_pack_tactics.py`, `conditions.py`, `roll_modifiers.py`, `attack_roll`, `Combatant`, `legendary_parser.py`, `intentar_desenganche`, `damage.py`, `test_superior_invisibility.py`, `test_checks_escapes.py`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `attack_roll()` (e.g. with `Attack` and `Combatant`) actually correct?**
  _`attack_roll()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `loader.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07073170731707316 - nodes in this community are weakly interconnected._
- **Why does `attack_roll()` connect `attack_roll` to `CombatContext`, `test_attach.py`, `test_enlarge.py`, `dnd_sim/__init__.py`, `test_spells.py`, `test_traits.py`, `Condition`, `apply_condition`, `PlayerCharacter`, `combat/__init__.py`, `combat/attack.py`, `test_legendary.py`, `legendary_phase`, `saves.py`, `test_martial_advantage.py`, `begin_turn`, `conditions.py`, `inflict_damage`, `Combatant`, `test_superior_invisibility.py`, `roll_dice`, `test_checks_escapes.py`, `registrar_resistencia`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
# Graph Report - DnDBalancer  (2026-10-21)

## Corpus Check
- 68 files · ~45,920 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 967 nodes · 3175 edges · 40 communities (34 shown, 6 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 202 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5dceefea`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_area.py
- spells.py
- test_legendary.py
- test_usage.py
- saves.py
- Combatant
- spell_parser.py
- legendary_parser.py
- test_spells.py
- test_loader_actions.py
- loader.py
- ability_check
- actions.py
- test_loader.py
- condition_parser.py
- CombatContext
- dnd_sim/__init__.py
- legendary.py
- attack.py
- save_builder.py
- roll_modifiers.py
- ConditionTracker
- test_conditions.py
- MultiattackAction
- begin_turn
- AttackModifiers
- Spellcasting
- test_checks_escapes.py
- Spell
- parse_spell
- _pj
- ActionType
- Any
- escape_parser.py
- attempt_escapes
- dice.py
- RollMode
- abilities.py

## God Nodes (most connected - your core abstractions)
1. `apply_condition()` - 74 edges
2. `load_monster()` - 59 edges
3. `_load()` - 48 edges
4. `Abilities` - 47 edges
5. `CombatContext` - 44 edges
6. `attack_roll()` - 44 edges
7. `run_combat()` - 44 edges
8. `Combatant` - 41 edges
9. `Condition` - 39 edges
10. `AttackRange` - 38 edges

## Surprising Connections (you probably didn't know these)
- `_build_party()` --uses--> `Abilities`  [INFERRED]
  main.py → dnd_sim/abilities.py
- `_area_action()` --uses--> `ActionType`  [INFERRED]
  tests/test_area.py → dnd_sim/actions.py
- `test_consumes_action_gasta_la_accion_del_turno()` --uses--> `ActionType`  [INFERRED]
  tests/test_checks_escapes.py → dnd_sim/actions.py
- `test_sin_consumes_action_conserva_la_accion()` --uses--> `ActionType`  [INFERRED]
  tests/test_checks_escapes.py → dnd_sim/actions.py
- `test_ataque_con_usage_conserva_el_actionusage()` --uses--> `AttackAction`  [INFERRED]
  tests/test_loader_actions.py → dnd_sim/actions.py

## Import Cycles
- None detected.

## Communities (40 total, 6 thin omitted)

### Community 0 - "test_area.py"
Cohesion: 0.29
Nodes (19): AreaTargeting, select_area_targets(), SaveDamage, _area_action(), _ctx(), _npc(), _pj(), _save_forzado() (+11 more)

### Community 1 - "spells.py"
Cohesion: 0.11
Nodes (9): CombatAction, SaveAction, duracion_en_rondas(), HealAction, HealEffect, spell_action(), SpellAction, SpellAttackAction (+1 more)

### Community 2 - "test_legendary.py"
Cohesion: 0.07
Nodes (61): ConditionEffect, legendary_phase(), saving_throw(), test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _contexto(), _data(), _estado(), _legendaria() (+53 more)

### Community 3 - "test_usage.py"
Cohesion: 0.06
Nodes (41): TurnResources, run_combat(), _summarize_damage(), ActionUsage, _log_line(), UsageKind, _data(), _load() (+33 more)

### Community 4 - "saves.py"
Cohesion: 0.13
Nodes (15): _log_target(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save(), _log_line(), _mode_tag(), _outcome_tag() (+7 more)

### Community 5 - "Combatant"
Cohesion: 0.13
Nodes (6): AttackAction, WeaponAttackAction, Attack, Combatant, normalize_ability(), test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio()

### Community 6 - "spell_parser.py"
Cohesion: 0.09
Nodes (10): _afecta_movimiento(), _condicion_con_salvacion(), _dado_por_nivel(), _dados_de_dano(), _dc_ability(), _numero_elementos(), _opciones_de_dano(), _tipo_de_dano() (+2 more)

### Community 8 - "legendary_parser.py"
Cohesion: 0.12
Nodes (10): _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary(), _por_referencia() (+2 more)

### Community 9 - "test_spells.py"
Cohesion: 0.19
Nodes (16): Condition, apply_concentration(), test_el_enum_no_contiene_condiciones_excluidas(), _ctx(), _npc(), _pj(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizado_invierte_los_objetivos_de_ataque() (+8 more)

### Community 10 - "test_loader_actions.py"
Cohesion: 0.07
Nodes (37): PlayerCharacter, apply_damage_modifiers(), _is_petrified(), print_report(), simulate(), build_parser(), _build_party(), _load_party() (+29 more)

### Community 11 - "loader.py"
Cohesion: 0.08
Nodes (15): AttackEntry, parse_range_type(), _resistencia_legendaria(), _damage_type(), _extract_multiattack_alternatives(), load_monster(), _simple_damage_modifiers(), extract_multiattack_alternatives() (+7 more)

### Community 12 - "ability_check"
Cohesion: 0.12
Nodes (11): ability_check(), ability_check_bonus(), CheckResult, _guia(), check_modifiers(), _fake(), test_los_flags_de_prueba_son_por_caracteristica(), test_prueba_con_ventaja_da_75_por_ciento() (+3 more)

### Community 13 - "actions.py"
Cohesion: 0.11
Nodes (6): _log(), CombatState, CombatantType, CombatState, Condition, _default_targeting()

### Community 14 - "test_loader.py"
Cohesion: 0.09
Nodes (16): _cache_path(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError, _armor_class_value(), _load_fixture(), _ogre_data() (+8 more)

### Community 15 - "condition_parser.py"
Cohesion: 0.15
Nodes (6): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), normalize_ability()

### Community 16 - "CombatContext"
Cohesion: 0.16
Nodes (4): CombatContext, _living_enemies(), SpellStateAction, valid_targets()

### Community 17 - "dnd_sim/__init__.py"
Cohesion: 0.14
Nodes (12): CombatResult, _invoke_policy(), resolve_roll_mode(), roll_initiative(), _run_combat(), pick(), sample(), _extract() (+4 more)

### Community 18 - "legendary.py"
Cohesion: 0.10
Nodes (8): _accion_utilizable(), _acciones_asequibles(), _combate_terminado(), _contexto_de(), _equipos_vivos(), LegendaryAction, LegendaryState, _presupuesto()

### Community 19 - "attack.py"
Cohesion: 0.12
Nodes (6): DamageRecorder, DamageType, inflict_damage(), _notify_damage_dealt(), _notify_damage_taken(), parse_damage_type()

### Community 20 - "save_builder.py"
Cohesion: 0.14
Nodes (8): is_area_action(), _por_datos(), build_condition_action(), build_save_action(), build_save_effect(), damage_dice_of(), damage_options(), damage_type_of()

### Community 21 - "roll_modifiers.py"
Cohesion: 0.21
Nodes (3): attack_modifiers(), _condiciones(), save_modifiers()

### Community 22 - "ConditionTracker"
Cohesion: 0.15
Nodes (4): ConditionTracker, ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 23 - "test_conditions.py"
Cohesion: 0.06
Nodes (70): Abilities, _actualizar_distancia(), _apply_condition_riders(), attack_roll(), Monster, apply_condition(), _as_condition(), ConditionAction (+62 more)

### Community 25 - "begin_turn"
Cohesion: 0.22
Nodes (13): EscapeCheck, begin_turn(), _check_fijo(), _ctx(), test_consumes_action_gasta_la_accion_del_turno(), test_dos_instancias_consumes_action_solo_intenta_la_primera(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_el_escape_con_ventaja_condicionada_por_envenenamiento() (+5 more)

### Community 27 - "Spellcasting"
Cohesion: 0.25
Nodes (5): build_spell_actions(), parse_spellcasting(), Spellcasting, test_el_lanzador_se_lee_de_los_special_abilities(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 28 - "test_checks_escapes.py"
Cohesion: 0.19
Nodes (12): effective_ac(), _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_el_estado_de_distancia_inicial_y_el_reset(), test_la_ca_efectiva_sube_dos_a_distancia(), test_la_cobertura_no_cambia_las_salvaciones() (+4 more)

### Community 30 - "parse_spell"
Cohesion: 0.27
Nodes (12): parse_spell(), _spell_data(), _spellcasting(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_lich_carga_su_cantrip_utile(), test_los_cantrips_no_gastan_usos_ni_slots(), test_los_hechizos_de_un_minuto_o_mas_se_ignoran(), test_los_hechizos_de_utilidad_se_ignoran_pero_no_por_movimiento() (+4 more)

### Community 31 - "_pj"
Cohesion: 0.19
Nodes (11): _load(), _pj(), test_el_escape_se_intenta_al_inicio_del_turno(), test_el_estado_cambia_ataque_a_ataque_en_un_multiataque(), test_en_un_combate_la_telaraña_inmoviliza_y_el_pj_intenta_escapar(), test_la_telaraña_deja_a_la_araña_a_distancia(), test_la_telaraña_no_aplica_la_condicion_si_falla_el_ataque(), test_probabilidad_de_liberarse_con_cd_12() (+3 more)

### Community 32 - "ActionType"
Cohesion: 0.21
Nodes (3): ActionType, AreaSaveAction, _log_line()

### Community 33 - "Any"
Cohesion: 0.18
Nodes (6): _contar_accion(), _contar_puntos(), _contar_resistencia(), legendary_resistance(), _log_line(), registrar_resistencia_legendaria()

### Community 34 - "escape_parser.py"
Cohesion: 0.18
Nodes (5): has_escape_text(), parse_escape(), _data(), test_el_fixture_de_la_constriccion_tiene_escape_y_avisa_de_grappled(), test_el_fixture_de_la_telaraña_carga_restrained_con_escape()

### Community 35 - "attempt_escapes"
Cohesion: 0.18
Nodes (6): attempt_escapes(), _contar(), _queda_accion(), test_con_dos_caracteristicas_se_elige_una_al_azar(), test_con_una_sola_caracteristica_no_consume_rng(), test_una_condicion_sin_escape_no_genera_intentos()

### Community 36 - "dice.py"
Cohesion: 0.27
Nodes (4): d20(), D20Result, roll_d20(), roll_dice()

### Community 37 - "RollMode"
Cohesion: 0.24
Nodes (4): _mode_tag(), RollMode, CheckModifiers, SaveModifiers

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `loader.py` to `test_area.py`, `spells.py`, `test_legendary.py`, `test_usage.py`, `Combatant`, `legendary_parser.py`, `test_spells.py`, `test_loader_actions.py`, `actions.py`, `test_loader.py`, `condition_parser.py`, `dnd_sim/__init__.py`, `save_builder.py`, `test_conditions.py`, `MultiattackAction`, `Spellcasting`, `test_checks_escapes.py`, `parse_spell`, `_pj`, `ActionType`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `ActionType` and `UnknownUsageError`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `spells.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11076923076923077 - nodes in this community are weakly interconnected._
- **Why does `apply_condition()` connect `test_conditions.py` to `ActionType`, `spells.py`, `test_legendary.py`, `attempt_escapes`, `test_spells.py`, `actions.py`, `CombatContext`, `dnd_sim/__init__.py`, `ConditionTracker`, `begin_turn`, `test_checks_escapes.py`, `_pj`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Abilities` (e.g. with `Combatant` and `_build_party()`) actually correct?**
  _`Abilities` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_legendary.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06718597857838364 - nodes in this community are weakly interconnected._
- **Why does `run_combat()` connect `test_usage.py` to `test_legendary.py`, `Combatant`, `test_spells.py`, `test_loader_actions.py`, `test_loader.py`, `CombatContext`, `dnd_sim/__init__.py`, `attack.py`, `test_conditions.py`, `begin_turn`, `test_checks_escapes.py`, `_pj`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
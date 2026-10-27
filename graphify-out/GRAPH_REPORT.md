# Graph Report - DnDBalancer  (2026-10-27)

## Corpus Check
- 163 files · ~92,420 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 1607 nodes · 5566 edges · 64 communities (53 shown, 11 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 336 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8d4e31e3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CombatContext
- test_attach.py
- warnings
- TurnResources
- test_area.py
- test_enlarge.py
- ActionType
- test_conditions.py
- test_spells.py
- test_traits.py
- Condition
- _duelo
- random
- Trait
- spell_parser.py
- traits/__init__.py
- test_damage.py
- build_spell_actions
- test_loader_actions.py
- test_multiattack.py
- test_legendary.py
- combatant.py
- LegendaryState
- AttackModifiers
- saves.py
- condition_parser.py
- test_death.py
- load_monster
- _condicion_posicional
- inflict_damage
- test_martial_advantage.py
- test_la_resistencia_funciona_en_todas_las_rutas
- saving_throw
- legendary_phase
- model/actions.py
- legendary.py
- test_pack_tactics.py
- run_combat
- survival.py
- attack_modifiers
- attack_roll
- loader.py
- dnd_sim/__init__.py
- legendary_parser.py
- _pj
- Combatant
- test_superior_invisibility.py
- conditions.py
- stealth.py
- apply_condition
- Abilities
- DamageRecorder
- test_el_cli_tiene_las_opciones_legendarias
- multiattack_parser.py
- spell_action
- ConditionTracker
- ConditionAction
- combat/attack.py

## God Nodes (most connected - your core abstractions)
1. `attack_roll()` - 105 edges
2. `apply_condition()` - 105 edges
3. `load_monster()` - 101 edges
4. `Abilities` - 92 edges
5. `Condition` - 92 edges
6. `CombatContext` - 80 edges
7. `Attack` - 78 edges
8. `run_combat()` - 73 edges
9. `Monster` - 68 edges
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
- `Paquetes con fachada` --references--> `Trait`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/rules/traits/base.py

## Import Cycles
- None detected.

## Communities (64 total, 11 thin omitted)

### Community 0 - "CombatContext"
Cohesion: 0.14
Nodes (6): valid_targets(), actor_is_alive(), CombatContext, _living_enemies(), _log(), _romper_invisibilidad_al_lanzar()

### Community 1 - "test_attach.py"
Cohesion: 0.09
Nodes (32): parse_attach_effects(), Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), _atacar() (+24 more)

### Community 2 - "warnings"
Cohesion: 0.13
Nodes (9): _resistencia_legendaria(), _simple_damage_modifiers(), _declara_uso(), _usage(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo() (+1 more)

### Community 3 - "TurnResources"
Cohesion: 0.08
Nodes (26): TurnResources, ActionUsage, UsageKind, _breath(), _eventos(), _FixedRandom, _load_fixture(), _player() (+18 more)

### Community 4 - "test_area.py"
Cohesion: 0.18
Nodes (22): AreaTargeting, select_area_targets(), _default_targeting(), SaveDamage, _area_action(), _ctx(), _npc(), _pj() (+14 more)

### Community 5 - "test_enlarge.py"
Cohesion: 0.15
Nodes (24): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+16 more)

### Community 6 - "ActionType"
Cohesion: 0.08
Nodes (16): ActionType, CombatAction, SaveAction, AreaSaveAction, HealAction, SpellAction, SpellAttackAction, SpellFixedDamageAction (+8 more)

### Community 8 - "test_conditions.py"
Cohesion: 0.12
Nodes (32): _ctx(), _data(), _load(), _pj(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente(), test_can_act_y_can_react(), test_condicion_fuera_del_enum_lanza_value_error(), test_dos_combates_seguidos_empiezan_sin_condiciones() (+24 more)

### Community 9 - "test_spells.py"
Cohesion: 0.14
Nodes (28): parse_spell(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_daño_extra_del_hechizo_verdadero_no_baja_de_cinco(), test_el_lich_carga_sus_hechizos_utiles() (+20 more)

### Community 10 - "test_traits.py"
Cohesion: 0.11
Nodes (24): RollMode, _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _RasgoDeSalvacion, _sahuagin() (+16 more)

### Community 11 - "Condition"
Cohesion: 0.21
Nodes (25): Condition, _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj(), test_atacar_a_un_invisible_tiene_desventaja() (+17 more)

### Community 12 - "_duelo"
Cohesion: 0.15
Nodes (17): _ataque(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja(), test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_los_indicadores_estaticos_siguen_funcionando_y_se_combinan(), test_melee_or_ranged_consume_rng_siempre() (+9 more)

### Community 13 - "random"
Cohesion: 0.21
Nodes (8): print_report(), simulate(), build_parser(), _build_party(), _load_party(), main(), _parse_monster_token(), test_informe_final_con_apartados_de_pj_y_monstruros()

### Community 14 - "Trait"
Cohesion: 0.08
Nodes (6): hooks(), Trait, BloodFrenzy, test_el_catalogo_cubre_hooks_que_los_rasgos_aun_no_usan(), test_hooks_con_un_nombre_fuera_del_catalogo_lanza_error(), test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 15 - "spell_parser.py"
Cohesion: 0.09
Nodes (13): _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla(), _frases() (+5 more)

### Community 16 - "traits/__init__.py"
Cohesion: 0.12
Nodes (6): DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante()

### Community 17 - "test_damage.py"
Cohesion: 0.21
Nodes (13): _tag_modificadores(), apply_damage_modifiers(), _is_petrified(), _guerrero_y_ogro(), _target(), test_danio_medio_por_combatiente_y_equipo(), test_etiqueta_de_modificadores_se_deriva_del_dano_final(), test_immunity_zero() (+5 more)

### Community 18 - "build_spell_actions"
Cohesion: 0.18
Nodes (11): build_spell_actions(), parse_spellcasting(), _desde_fixture(), _monstruo_lanzador(), test_el_lanzador_se_lee_de_los_actions(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_la_reaccion_gasta_su_uso_propio(), test_max_spell_level_limita_el_nivel_cargado() (+3 more)

### Community 19 - "test_loader_actions.py"
Cohesion: 0.14
Nodes (14): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+6 more)

### Community 20 - "test_multiattack.py"
Cohesion: 0.11
Nodes (17): _data(), _load(), _pj(), _raw_multiattack(), test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(), test_el_aliento_dentro_del_multiataque_gasta_su_uso(), test_el_dragon_hace_tres_ataques_por_turno(), test_la_quimera_hace_tres_ataques_por_turno() (+9 more)

### Community 21 - "test_legendary.py"
Cohesion: 0.11
Nodes (30): _data(), _load(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_con_use_probability_uno_el_danio_es_mayor_que_con_cero(), test_el_ala_que_mezcla_movimiento_avisa(), test_el_cantrip_del_lich_se_omite_con_aviso(), test_el_detect_del_dragon_se_omite_con_aviso() (+22 more)

### Community 22 - "combatant.py"
Cohesion: 0.12
Nodes (6): AttackRange, DamageType, parse_damage_type(), WeaponAttackAction, ExtraDamage, CombatantType

### Community 23 - "LegendaryState"
Cohesion: 0.14
Nodes (5): LegendaryState, _estado(), test_el_estado_legendario_rellena_gasta_y_reinicia(), test_resistance_probability_medio_convierte_about_50_por_ciento(), test_use_probability_medio_se_usa_about_50_por_ciento()

### Community 25 - "saves.py"
Cohesion: 0.11
Nodes (16): _log_target(), legendary_resistance(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save(), _mode_tag(), _outcome_tag() (+8 more)

### Community 26 - "condition_parser.py"
Cohesion: 0.13
Nodes (6): normalize_ability(), _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with()

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 28 - "load_monster"
Cohesion: 0.08
Nodes (19): _cache_path(), get_monster(), get_spell(), MonsterNotFoundError, NetworkError, _armor_class_value(), load_monster(), MultiattackAction (+11 more)

### Community 29 - "_condicion_posicional"
Cohesion: 0.19
Nodes (4): aliados_capaces(), _condicion_posicional(), MartialAdvantage, PackTactics

### Community 30 - "inflict_damage"
Cohesion: 0.06
Nodes (52): _entradas(), parse_traits(), _hooks(), inflict_damage(), _notify_damage_dealt(), _salvar_a_cero(), begin_turn(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd() (+44 more)

### Community 31 - "test_martial_advantage.py"
Cohesion: 0.12
Nodes (20): Cómo comprobar que todo sigue en orden, _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba(), test_las_excepciones_siguen_existiendo(), test_los_paquetes_con_fachada_reexportan_su_api(), _aliado(), _ctx() (+12 more)

### Community 32 - "test_la_resistencia_funciona_en_todas_las_rutas"
Cohesion: 0.25
Nodes (3): _apply_condition_riders(), RepeatSave, test_la_resistencia_funciona_en_todas_las_rutas()

### Community 33 - "saving_throw"
Cohesion: 0.25
Nodes (9): saving_throw(), _datos(), _lich(), _pj(), test_con_ventaja_acierta_mas_que_sin_ella(), test_da_ventaja_si_la_salvacion_es_de_conversion(), test_el_lich_carga_su_turn_resistance(), test_sin_el_tipo_de_efecto_no_aplica() (+1 more)

### Community 34 - "legendary_phase"
Cohesion: 0.16
Nodes (22): legendary_phase(), _contexto(), _pj(), test_con_una_sola_accion_asequible_pick_no_consume_rng(), test_dos_duenos_legendarios_actuan_cada_uno_una_vez(), test_el_combate_termina_en_medio_de_la_fase(), test_la_fase_ocurre_despues_del_end_turn(), test_no_actua_si_el_combate_ya_terminado() (+14 more)

### Community 35 - "model/actions.py"
Cohesion: 0.12
Nodes (3): pick(), sample(), resolve_attack_range()

### Community 36 - "legendary.py"
Cohesion: 0.11
Nodes (11): log_line(), _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), LegendaryAction (+3 more)

### Community 37 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 38 - "run_combat"
Cohesion: 0.16
Nodes (10): combat_finished(), living_teams(), _objetivo_enganche(), CombatResult, _invoke_policy(), roll_initiative(), run_combat(), _run_combat() (+2 more)

### Community 39 - "survival.py"
Cohesion: 0.11
Nodes (5): _es_radiante(), _guardar_salvacion(), Regeneration, Relentless, UndeadFortitude

### Community 40 - "attack_modifiers"
Cohesion: 0.15
Nodes (8): attack_modifiers(), check_modifiers(), CheckModifiers, _condiciones(), _hooks(), save_modifiers(), SaveModifiers, test_inmovilizado_da_desventaja_solo_en_des()

### Community 41 - "attack_roll"
Cohesion: 0.09
Nodes (57): D20Result, attack_roll(), Attack, _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos() (+49 more)

### Community 42 - "loader.py"
Cohesion: 0.13
Nodes (7): _damage_type(), _norm_name(), build_condition_action(), build_save_effect(), damage_dice_of(), damage_options(), damage_type_of()

### Community 43 - "dnd_sim/__init__.py"
Cohesion: 0.16
Nodes (5): ability_mod(), CombatState, _extract(), first_target_policy(), AttackEntry

### Community 44 - "legendary_parser.py"
Cohesion: 0.09
Nodes (15): parse_range_type(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary() (+7 more)

### Community 45 - "_pj"
Cohesion: 0.17
Nodes (15): _ctx(), _npc(), _pj(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizado_invierte_los_objetivos_de_ataque(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado(), test_el_hechizo_verdadero_es_un_ataque_real_con_dano_extra(), test_el_proyectil_magico_pasa_por_los_modificadores_de_dano() (+7 more)

### Community 46 - "Combatant"
Cohesion: 0.09
Nodes (8): Arquitectura de `dnd_sim`, Carpetas, Excepción única admitida, Imports diferidos, Reglas de dependencia, Combatant, _mark_dead_if_down(), _notify_damage_taken()

### Community 47 - "test_superior_invisibility.py"
Cohesion: 0.36
Nodes (11): _accion(), _ctx(), _pixie(), _pj(), test_atacar_con_ventaja_y_no_pierde_la_invisibilidad(), test_ejecutarla_aplica_el_estado(), test_el_monstruo_recibe_su_accion_al_construirse(), test_lanzar_un_hechizo_tampoco_la_pierde() (+3 more)

### Community 48 - "conditions.py"
Cohesion: 0.18
Nodes (8): _as_condition(), attempt_escapes(), _contar(), end_turn(), _label(), _queda_accion(), remove_condition(), remove_invisibility_on_action()

### Community 50 - "apply_condition"
Cohesion: 0.05
Nodes (56): has_escape_text(), parse_escape(), ability_check(), ability_check_bonus(), CheckResult, _guia(), apply_condition(), ConditionEffect (+48 more)

### Community 52 - "Abilities"
Cohesion: 0.14
Nodes (14): Abilities, Monster, PlayerCharacter, test_las_condiciones_incapacitantes_fallan_fue_y_des_sin_tirar_dados(), test_las_condiciones_incapacitantes_no_fallan_automaticamente_la_con(), test_petrificado_tiene_resistencia_a_todo(), test_sin_condiciones_el_dano_no_cambia(), test_attack_roll_log_modifier() (+6 more)

### Community 57 - "multiattack_parser.py"
Cohesion: 0.18
Nodes (5): _extract_multiattack_alternatives(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack()

### Community 61 - "spell_action"
Cohesion: 0.14
Nodes (9): Paquetes con fachada, _uso_de_entrada(), Spell, spell_action(), Spellcasting, test_el_hechizo_enlarge_es_un_estado_self(), test_el_upcast_reescala_el_dano_y_la_curacion(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo() (+1 more)

### Community 63 - "ConditionTracker"
Cohesion: 0.22
Nodes (3): ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 65 - "combat/attack.py"
Cohesion: 0.09
Nodes (13): d20(), roll_d20(), roll_dice(), _actualizar_distancia(), _agrandado(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo() (+5 more)

## Knowledge Gaps
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `load_monster` to `test_attach.py`, `warnings`, `TurnResources`, `test_area.py`, `test_enlarge.py`, `ActionType`, `test_conditions.py`, `test_spells.py`, `test_traits.py`, `Condition`, `random`, `test_damage.py`, `build_spell_actions`, `test_loader_actions.py`, `test_multiattack.py`, `test_legendary.py`, `combatant.py`, `condition_parser.py`, `test_death.py`, `inflict_damage`, `test_martial_advantage.py`, `saving_throw`, `test_pack_tactics.py`, `attack_roll`, `loader.py`, `dnd_sim/__init__.py`, `legendary_parser.py`, `apply_condition`, `Abilities`, `multiattack_parser.py`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `attack_roll()` (e.g. with `Attack` and `Combatant`) actually correct?**
  _`attack_roll()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `CombatContext` be split into smaller, more focused modules?**
  _Cohesion score 0.13793103448275862 - nodes in this community are weakly interconnected._
- **Why does `Condition` connect `Condition` to `test_attach.py`, `test_enlarge.py`, `ActionType`, `test_conditions.py`, `test_spells.py`, `test_traits.py`, `spell_parser.py`, `traits/__init__.py`, `test_damage.py`, `test_legendary.py`, `combatant.py`, `condition_parser.py`, `model/actions.py`, `test_pack_tactics.py`, `attack_modifiers`, `attack_roll`, `loader.py`, `dnd_sim/__init__.py`, `_pj`, `Combatant`, `test_superior_invisibility.py`, `conditions.py`, `stealth.py`, `apply_condition`, `Abilities`, `spell_action`, `ConditionTracker`, `combat/attack.py`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `UnknownUsageError` and `ActionType`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09288824383164006 - nodes in this community are weakly interconnected._
- **Why does `attack_roll()` connect `attack_roll` to `CombatContext`, `test_attach.py`, `test_enlarge.py`, `ActionType`, `test_conditions.py`, `test_spells.py`, `test_traits.py`, `Condition`, `_duelo`, `test_damage.py`, `test_legendary.py`, `combatant.py`, `saves.py`, `test_death.py`, `inflict_damage`, `test_martial_advantage.py`, `test_la_resistencia_funciona_en_todas_las_rutas`, `model/actions.py`, `run_combat`, `attack_modifiers`, `_pj`, `Combatant`, `test_superior_invisibility.py`, `conditions.py`, `apply_condition`, `.execute`, `Abilities`, `combat/attack.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
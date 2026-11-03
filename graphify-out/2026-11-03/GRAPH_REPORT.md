# Graph Report - DnDBalancer  (2026-11-03)

## Corpus Check
- 202 files · ~137,190 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 2582 nodes · 9252 edges · 79 communities (73 shown, 6 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 551 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0baf26e4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- loader.py
- inflict_damage
- test_berserker.py
- test_giant.py
- test_area.py
- test_enlarge.py
- test_magical.py
- test_legendary.py
- test_beast.py
- parse_spell
- RollMode
- attack_roll
- test_utility.py
- simulate
- Trait
- _avisar
- DamageTransfer
- PlayerCharacter
- BarbarianFeatures
- test_loader_actions.py
- CombatContext
- ataque_utilitario
- test_usage.py
- test_barbarian.py
- barbarian/__init__.py
- saving_throw
- traits/__init__.py
- run_combat
- json
- test_superior_invisibility.py
- test_extra_damage.py
- dnd_sim/__init__.py
- test_backgrounds.py
- BeastFeatures
- test_skills.py
- warnings
- Monster
- test_proficiency.py
- encounter.py
- Regeneration
- roll_modifiers.py
- BattleragerFeatures
- apply_condition
- model/actions.py
- pytest
- random
- GiantFeatures
- ability_check
- legendary.py
- ConditionInstance
- test_checks_escapes.py
- load_monster
- lair_loader.py
- SpellFixedDamageAction
- sample
- Attack
- test_ancestral_guardian.py
- test_magic_resistance.py
- begin_turn
- _data
- spell_action
- legendary_parser.py
- D20Result
- combatant.py
- AreaSaveAction
- spell_parser.py
- test_sin_autoexito_ni_autofallo_en_pruebas
- test_spells.py
- test_azer.py
- race_parser.py
- test_races.py
- pathlib
- Condition
- load_race
- TurnResources
- TODO — DnDBalancer / dnd_sim

## God Nodes (most connected - your core abstractions)
1. `apply_condition()` - 142 edges
2. `Attack` - 141 edges
3. `Condition` - 139 edges
4. `load_monster()` - 135 edges
5. `Abilities` - 129 edges
6. `attack_roll()` - 128 edges
7. `PlayerCharacter` - 106 edges
8. `Monster` - 101 edges
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

## Communities (79 total, 6 thin omitted)

### Community 0 - "loader.py"
Cohesion: 0.07
Nodes (12): doblar_dados(), parse_attach_effects(), parse_range_type(), _damage_type(), _extract_multiattack_alternatives(), _parse_condition_immunities(), _parse_damage_modifiers(), extract_multiattack_alternatives() (+4 more)

### Community 1 - "inflict_damage"
Cohesion: 0.05
Nodes (63): AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), _absorber_pv_temporales(), _hooks(), inflict_damage() (+55 more)

### Community 2 - "test_berserker.py"
Cohesion: 0.07
Nodes (56): AttackRange, RageAction, apply_berserker(), _armas_melee_de(), BerserkerFeatures, _de(), _furia_de(), _golpe_sin_armas() (+48 more)

### Community 3 - "test_giant.py"
Cohesion: 0.14
Nodes (31): apply_giant(), MightyImpelAction, _abilities(), _barbaro(), _ctx(), _furia(), _giant(), _mon() (+23 more)

### Community 4 - "test_area.py"
Cohesion: 0.21
Nodes (21): AreaTargeting, select_area_targets(), _default_targeting(), SaveDamage, _area_action(), _ctx(), _npc(), _pj() (+13 more)

### Community 5 - "test_enlarge.py"
Cohesion: 0.17
Nodes (22): _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj(), _spell_data() (+14 more)

### Community 6 - "test_magical.py"
Cohesion: 0.11
Nodes (19): _tag_modificadores(), apply_beast(), _ctx(), _pj(), test_ataque_con_magical_true_dana_completo_al_ghost(), test_ataque_magico_contra_un_bárbaro_en_furia_se_reduce_a_la_mitad(), test_bestial_solo_marca_las_armas_magicas_desde_el_nivel_6(), test_el_log_del_ataque_dice_dano_no_magico() (+11 more)

### Community 7 - "test_legendary.py"
Cohesion: 0.06
Nodes (62): _apply_condition_riders(), ConditionAction, RepeatSave, legendary_phase(), _contexto(), _data(), _estado(), _legendaria() (+54 more)

### Community 8 - "test_beast.py"
Cohesion: 0.11
Nodes (64): _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll(), spy(), _forma() (+56 more)

### Community 9 - "parse_spell"
Cohesion: 0.08
Nodes (35): _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), parse_spell(), _slot_table(), _tabla_cantrip(), _tipo_de_dano(), _npc() (+27 more)

### Community 10 - "RollMode"
Cohesion: 0.06
Nodes (63): RollMode, attack_modifiers(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+55 more)

### Community 11 - "attack_roll"
Cohesion: 0.23
Nodes (21): _actualizar_distancia(), attack_roll(), _mode_tag(), _ataque(), _ctx(), _datos(), _fijar_d20(), _gladiador() (+13 more)

### Community 12 - "test_utility.py"
Cohesion: 0.22
Nodes (21): _abilities(), _ctx(), _mon(), _pj(), _siempre_falla(), test_actor_no_disponible_no_consulta_la_probabilidad(), test_agarrar_admite_hasta_un_tamano_mayor(), test_agarrar_aplica_agarrado_con_escape_de_acción() (+13 more)

### Community 13 - "simulate"
Cohesion: 0.22
Nodes (7): print_report(), simulate(), build_parser(), _build_party(), _load_party(), main(), _parse_monster_token()

### Community 14 - "Trait"
Cohesion: 0.06
Nodes (4): CallTheHuntBonus, Trait, BloodFrenzy, test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 15 - "_avisar"
Cohesion: 0.40
Nodes (3): _avisar(), _extender_tabla(), _sumar_dados()

### Community 16 - "DamageTransfer"
Cohesion: 0.12
Nodes (6): DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante()

### Community 17 - "PlayerCharacter"
Cohesion: 0.14
Nodes (19): PlayerCharacter, apply_damage_modifiers(), _is_petrified(), _guerrero_y_ogro(), _target(), test_attack_roll_log_modifier(), test_danio_medio_por_combatiente_y_equipo(), test_etiqueta_de_modificadores_se_deriva_del_dano_final() (+11 more)

### Community 18 - "BarbarianFeatures"
Cohesion: 0.09
Nodes (5): BarbarianFeatures, ExtendRageAction, _rasgo(), test_reckless_active_this_turn_refleja_el_estado(), test_las_armas_de_furia_no_distinguen_magical()

### Community 19 - "test_loader_actions.py"
Cohesion: 0.18
Nodes (13): _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga(), test_ataque_con_usage_conserva_el_actionusage() (+5 more)

### Community 20 - "CombatContext"
Cohesion: 0.10
Nodes (11): pick(), _objetivo_enganche(), valid_targets(), actor_is_alive(), CombatContext, _en_accion_de_ataque(), _living_enemies(), _log() (+3 more)

### Community 21 - "ataque_utilitario"
Cohesion: 0.14
Nodes (8): _agarrando(), ataque_utilitario(), _condiciones(), debe_usar_utilitaria(), hay_utilitaria_accion(), _orden_tamano(), test_p_medio_usa_utilitaria_a_la_frecuencia_configurada(), test_p_uno_siempre_decide_sin_consumir_rng()

### Community 22 - "test_usage.py"
Cohesion: 0.08
Nodes (26): _uso_de_entrada(), ActionUsage, UsageKind, _breath(), _eventos(), _FixedRandom, _load_fixture(), _player() (+18 more)

### Community 23 - "test_barbarian.py"
Cohesion: 0.06
Nodes (78): apply_barbarian(), AttackModifiers, CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj(), _resultado() (+70 more)

### Community 24 - "barbarian/__init__.py"
Cohesion: 0.08
Nodes (9): AncestralGuardianFeatures, apply_ancestral_guardian(), SpikedArmorAction, FormOfTheBeast, NaturalWeapon, ClassDef, normalize_class_name(), register_class() (+1 more)

### Community 25 - "saving_throw"
Cohesion: 0.14
Nodes (15): _log_target(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save(), _mode_tag(), _outcome_tag(), _reaccion_si_procede() (+7 more)

### Community 26 - "traits/__init__.py"
Cohesion: 0.12
Nodes (5): aliados_capaces(), _condicion_posicional(), MartialAdvantage, PackTactics, SuperiorInvisibility

### Community 27 - "run_combat"
Cohesion: 0.13
Nodes (19): combat_finished(), living_teams(), run_combat(), _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal (+11 more)

### Community 28 - "json"
Cohesion: 0.15
Nodes (9): _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait(), MonsterNotFoundError (+1 more)

### Community 29 - "test_superior_invisibility.py"
Cohesion: 0.10
Nodes (33): _entradas(), parse_traits(), remove_invisibility_on_action(), _aliado(), _ctx(), _datos(), _espada(), _hobgoblin() (+25 more)

### Community 30 - "test_extra_damage.py"
Cohesion: 0.18
Nodes (17): DamageRecorder, _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional() (+9 more)

### Community 31 - "dnd_sim/__init__.py"
Cohesion: 0.10
Nodes (8): ability_mod(), CombatState, d20(), roll_d20(), proficiency_bonus(), Attach, test_nivel_recortado_al_rango_1_20(), test_tabla_niveles()

### Community 32 - "test_backgrounds.py"
Cohesion: 0.12
Nodes (18): Background, _add(), load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias(), test_apply_background_no_duplica_competencias_existentes() (+10 more)

### Community 34 - "test_skills.py"
Cohesion: 0.11
Nodes (23): _abilities(), _ctx(), _load_fixture(), _pj(), _SoloMod, test_ability_check_no_suma_competencia_de_habilidad(), test_attempt_escapes_tira_la_habilidad(), test_caracteristica_asociada() (+15 more)

### Community 35 - "warnings"
Cohesion: 0.15
Nodes (8): _resistencia_legendaria(), _declara_uso(), _usage(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 36 - "Monster"
Cohesion: 0.06
Nodes (35): Monster, lair_phase(), LairAction, LegendaryState, _ctx(), _dragon(), _enemigo(), lairs_dir() (+27 more)

### Community 37 - "test_proficiency.py"
Cohesion: 0.21
Nodes (18): ability_check_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia() (+10 more)

### Community 38 - "encounter.py"
Cohesion: 0.14
Nodes (10): CombatResult, _invoke_policy(), roll_initiative(), _run_combat(), _nuevo_ctx(), _summarize_damage(), _extract(), first_target_policy() (+2 more)

### Community 39 - "Regeneration"
Cohesion: 0.09
Nodes (6): _mark_dead_if_down(), _es_radiante(), _guardar_salvacion(), Regeneration, Relentless, UndeadFortitude

### Community 40 - "roll_modifiers.py"
Cohesion: 0.12
Nodes (13): check_modifiers(), _condiciones(), _hooks(), _instancias(), save_modifiers(), _datos(), _lich(), _pj() (+5 more)

### Community 41 - "BattleragerFeatures"
Cohesion: 0.14
Nodes (4): apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque()

### Community 42 - "apply_condition"
Cohesion: 0.05
Nodes (74): Abilities, apply_condition(), resolve_attack_range(), _ctx(), _ghoul(), _InmuneMientrasActivo, _pj(), test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune() (+66 more)

### Community 43 - "model/actions.py"
Cohesion: 0.07
Nodes (13): _clamp(), extra_attacks_for(), rage_damage(), rage_uses(), roll_dice(), log_line(), AttackAction, AttackEntry (+5 more)

### Community 44 - "pytest"
Cohesion: 0.21
Nodes (15): apply_class(), _abilities(), _firmas(), _pj(), test_apply_class_ancestral_equivalente_a_los_apply_suelto(), test_apply_class_battlerager_equivalente_a_los_apply_suelto(), test_apply_class_normaliza_el_nombre(), test_apply_class_reenvia_kwargs_a_la_clase() (+7 more)

### Community 45 - "random"
Cohesion: 0.25
Nodes (18): _abilities(), _ctx(), _decide(), _pj(), test_antes_del_nivel_2_no_hay_decision_ni_rng(), test_en_turno_ajeno_no_decide(), test_frecuencia_0_5_es_aproximadamente_la_mitad_de_los_turnos(), test_las_reacciones_no_deciden_ni_reciben() (+10 more)

### Community 46 - "GiantFeatures"
Cohesion: 0.16
Nodes (4): _de(), GiantFeatures, _objetivos_impel(), _orden_de()

### Community 47 - "ability_check"
Cohesion: 0.11
Nodes (14): _clean(), normalize_skill(), skill_ability(), ability_check(), CheckResult, _finish_check(), _guia(), _resolve_mods() (+6 more)

### Community 48 - "legendary.py"
Cohesion: 0.13
Nodes (10): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), legendary_resistance(), LegendaryAction (+2 more)

### Community 49 - "ConditionInstance"
Cohesion: 0.22
Nodes (3): ConditionInstance, ConditionTracker, test_implicaciones_de_las_condiciones()

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.09
Nodes (43): attempt_escapes(), EscapeCheck, effective_ac(), _ataque(), _ctx(), _duelo(), _load(), _pj() (+35 more)

### Community 51 - "load_monster"
Cohesion: 0.12
Nodes (18): _armor_class_value(), load_monster(), _norm_name(), _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper() (+10 more)

### Community 52 - "lair_loader.py"
Cohesion: 0.29
Nodes (5): _check_fields(), _construir(), _error(), load_lair(), test_targeting_fuera_de_rango()

### Community 53 - "SpellFixedDamageAction"
Cohesion: 0.21
Nodes (10): SpellFixedDamageAction, _ctx(), _pj(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizado_invierte_los_objetivos_de_ataque(), test_el_proyectil_magico_pasa_por_los_modificadores_de_dano(), lanzar(), test_la_curacion_solo_se_lanza_contra_un_aliado_herido() (+2 more)

### Community 54 - "sample"
Cohesion: 0.40
Nodes (3): sample(), test_sample_devuelve_todos_sin_consumir_rng(), test_sample_k_menor_devuelve_distintos_y_uniformes()

### Community 57 - "Attack"
Cohesion: 0.25
Nodes (4): Attack, test_alma_bestial_flag_magical_existe(), test_extra_damage_estructura_por_defecto_vacia(), _arquero_parry()

### Community 59 - "test_ancestral_guardian.py"
Cohesion: 0.18
Nodes (26): _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado(), _escudo(), _esperado() (+18 more)

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.14
Nodes (21): _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa(), test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab(), test_condition_action_de_hechizo_pasa_magical() (+13 more)

### Community 61 - "begin_turn"
Cohesion: 0.27
Nodes (15): begin_turn(), _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno() (+7 more)

### Community 62 - "_data"
Cohesion: 0.40
Nodes (3): _data(), test_el_fixture_de_la_constriccion_tiene_escape_y_avisa_de_grappled(), test_el_fixture_de_la_telaraña_carga_restrained_con_escape()

### Community 63 - "spell_action"
Cohesion: 0.11
Nodes (14): Paquetes con fachada, SaveAction, Spell, spell_action(), Spellcasting, test_el_hechizo_enlarge_es_un_estado_self(), _spell_data(), _spellcasting() (+6 more)

### Community 64 - "legendary_parser.py"
Cohesion: 0.08
Nodes (18): is_area_action(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary() (+10 more)

### Community 65 - "D20Result"
Cohesion: 0.50
Nodes (4): D20Result, fijar(), espia(), espia()

### Community 66 - "combatant.py"
Cohesion: 0.05
Nodes (21): normalize_ability(), normalize_tool(), DamageType, parse_damage_type(), _agrandado(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo() (+13 more)

### Community 68 - "spell_parser.py"
Cohesion: 0.09
Nodes (12): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), _sentence_with(), has_escape_text(), parse_escape(), _skills_for() (+4 more)

### Community 71 - "test_spells.py"
Cohesion: 0.14
Nodes (15): build_spell_actions(), parse_spellcasting(), _desde_fixture(), _monstruo_lanzador(), test_el_lanzador_se_lee_de_los_actions(), test_el_lich_carga_sus_hechizos_utiles(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_la_curacion_usa_el_modificador_de_caracteristica_no_el_bono_completo() (+7 more)

### Community 74 - "test_azer.py"
Cohesion: 0.26
Nodes (17): _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), _rasgo(), test_ataque_a_distancia_no_dispara_la_represalia() (+9 more)

### Community 75 - "race_parser.py"
Cohesion: 0.15
Nodes (9): parse_race(), _skill_name(), _spells_from_description(), _trait_skills(), _keen_senses(), test_parse_competencias_fijas_de_la_raza(), test_parse_descripcion_sin_hechizos_da_vacio(), test_parse_elfo_linaje_hechizos_sin_duplicados() (+1 more)

### Community 77 - "test_races.py"
Cohesion: 0.22
Nodes (12): Race, _abilities(), _fiendish_legacy(), _pj(), test_apply_race_añade_competencias_fijas(), test_apply_race_con_habilidad_pedida(), test_apply_race_habilidad_fuera_de_las_opciones_es_error(), test_apply_race_no_duplica_competencias_existentes() (+4 more)

### Community 78 - "pathlib"
Cohesion: 0.06
Nodes (29): Arquitectura de `dnd_sim`, Carpetas, Cómo comprobar que todo sigue en orden, Excepción única admitida, Guaridas: política fija, Imports diferidos, Reglas de dependencia, _capa() (+21 more)

### Community 80 - "Condition"
Cohesion: 0.18
Nodes (8): _as_condition(), _condicion_bloqueada(), Condition, _contar(), end_turn(), _label(), _queda_accion(), remove_condition()

### Community 82 - "load_race"
Cohesion: 0.33
Nodes (5): load_race(), test_load_race_descarga_la_raza_y_sus_rasgos(), _rasgo(), _raza(), test_load_race_propaga_el_error_de_la_api()

### Community 83 - "TurnResources"
Cohesion: 0.08
Nodes (14): ActionType, TurnResources, HealAction, SpellAction, SpellAttackAction, dado_por_nivel(), duracion_en_rondas(), apply_concentration() (+6 more)

### Community 85 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.33
Nodes (5): Bloque 2026-10-30 (commiteado), Grafo y verificación, Rutina sugerida al abrir sesión, TODO — DnDBalancer / dnd_sim, TODOs en código (marcados `# TODO`)

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Attack` connect `Attack` to `loader.py`, `inflict_damage`, `test_berserker.py`, `test_giant.py`, `test_enlarge.py`, `test_magical.py`, `test_legendary.py`, `test_beast.py`, `parse_spell`, `RollMode`, `attack_roll`, `test_utility.py`, `simulate`, `PlayerCharacter`, `test_barbarian.py`, `barbarian/__init__.py`, `run_combat`, `test_superior_invisibility.py`, `test_extra_damage.py`, `dnd_sim/__init__.py`, `test_proficiency.py`, `BattleragerFeatures`, `apply_condition`, `model/actions.py`, `pytest`, `random`, `test_checks_escapes.py`, `load_monster`, `lair_loader.py`, `test_ancestral_guardian.py`, `test_magic_resistance.py`, `begin_turn`, `spell_action`, `legendary_parser.py`, `combatant.py`, `test_spells.py`, `test_azer.py`, `TurnResources`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `AttackRange`) actually correct?**
  _`Attack` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Should `loader.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06722689075630252 - nodes in this community are weakly interconnected._
- **Why does `load_monster()` connect `load_monster` to `loader.py`, `inflict_damage`, `test_area.py`, `test_enlarge.py`, `test_magical.py`, `test_legendary.py`, `test_beast.py`, `RollMode`, `attack_roll`, `simulate`, `PlayerCharacter`, `test_loader_actions.py`, `CombatContext`, `test_usage.py`, `run_combat`, `json`, `test_superior_invisibility.py`, `test_extra_damage.py`, `dnd_sim/__init__.py`, `test_skills.py`, `warnings`, `Monster`, `roll_modifiers.py`, `apply_condition`, `model/actions.py`, `pytest`, `ability_check`, `test_checks_escapes.py`, `lair_loader.py`, `Attack`, `test_magic_resistance.py`, `begin_turn`, `spell_action`, `legendary_parser.py`, `combatant.py`, `spell_parser.py`, `test_spells.py`, `test_azer.py`, `pathlib`, `TurnResources`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 88 inferred relationships involving `Condition` (e.g. with `_condition_from_phrase()` and `parse_condition_effects()`) actually correct?**
  _`Condition` has 88 INFERRED edges - model-reasoned connections that need verification._
- **Should `inflict_damage` be split into smaller, more focused modules?**
  _Cohesion score 0.050793650793650794 - nodes in this community are weakly interconnected._
- **Why does `Trait` connect `Trait` to `BeastFeatures`, `test_berserker.py`, `warnings`, `combatant.py`, `Regeneration`, `BattleragerFeatures`, `apply_condition`, `model/actions.py`, `RollMode`, `GiantFeatures`, `DamageTransfer`, `spell_action`, `BarbarianFeatures`, `barbarian/__init__.py`, `traits/__init__.py`, `test_superior_invisibility.py`, `dnd_sim/__init__.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
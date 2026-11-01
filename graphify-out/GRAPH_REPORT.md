# Graph Report - DnDBalancer  (2026-10-31)

## Corpus Check
- 194 files · ~124,325 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 2303 nodes · 8104 edges · 75 communities (68 shown, 7 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 429 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fa1a882b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- battlerager.py
- test_attach.py
- test_ancestral_guardian.py
- test_usage.py
- test_area.py
- test_enlarge.py
- spell_action
- legendary_phase
- test_beast.py
- test_spells.py
- test_traits.py
- Condition
- test_conditions.py
- Abilities
- Trait
- spell_parser.py
- DamageTransfer
- Monster
- BarbarianFeatures
- test_loader_actions.py
- CombatContext
- test_legendary.py
- Attack
- test_barbarian.py
- TurnResources
- dnd_sim/__init__.py
- loader.py
- ActionType
- test_races.py
- traits/__init__.py
- inflict_damage
- pathlib
- conditions.py
- BeastFeatures
- test_skills.py
- json
- test_lair.py
- test_proficiency.py
- run_combat
- Regeneration
- RollMode
- attack_roll
- _duelo
- combat/attack.py
- legendary_parser.py
- SpellFixedDamageAction
- pick
- ability_check
- attach.py
- test_pack_tactics.py
- apply_condition
- load_monster
- pytest
- test_martial_advantage.py
- parse_escape
- AttackAction
- AncestralGuardianFeatures
- test_magic_resistance.py
- parse_spellcasting
- _duelo
- normalize_skill
- AreaSaveAction
- classes.py
- combatant.py
- ConditionAction
- condition_parser.py
- test_superior_invisibility.py
- warnings
- build_spell_actions
- TODO — DnDBalancer / dnd_sim
- _estado
- test_sin_autoexito_ni_autofallo_en_pruebas

## God Nodes (most connected - your core abstractions)
1. `load_monster()` - 129 edges
2. `attack_roll()` - 124 edges
3. `Attack` - 121 edges
4. `Abilities` - 119 edges
5. `apply_condition()` - 111 edges
6. `Condition` - 103 edges
7. `PlayerCharacter` - 96 edges
8. `Monster` - 93 edges
9. `CombatContext` - 90 edges
10. `run_combat()` - 85 edges

## Surprising Connections (you probably didn't know these)
- `TODOs en código (marcados `# TODO`)` --references--> `Attack`  [INFERRED]
  TODO.md → dnd_sim/model/attack.py
- `Excepción única admitida` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Paquetes con fachada` --references--> `CombatResult`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/engine/combat/encounter.py
- `Carpetas` --references--> `Combatant`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py
- `Carpetas` --references--> `PlayerCharacter`  [INFERRED]
  ARCHITECTURE.md → dnd_sim/model/combatant.py

## Import Cycles
- None detected.

## Communities (75 total, 7 thin omitted)

### Community 0 - "battlerager.py"
Cohesion: 0.08
Nodes (11): apply_battlerager(), BattleragerFeatures, _de(), _nuevo_ataque(), SpikedArmorAction, FormOfTheBeast, NaturalWeapon, ClassDef (+3 more)

### Community 1 - "test_attach.py"
Cohesion: 0.18
Nodes (25): _atacar(), _bite(), _cloaker(), _ctx(), _datos(), _pj(), test_con_ventaja_el_enganche_es_a_la_cabeza_y_ciega(), test_damage_transfer_no_aplica_sin_enganche() (+17 more)

### Community 2 - "test_ancestral_guardian.py"
Cohesion: 0.17
Nodes (26): _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado(), _escudo(), _esperado() (+18 more)

### Community 3 - "test_usage.py"
Cohesion: 0.09
Nodes (25): ActionUsage, UsageKind, _breath(), _eventos(), _FixedRandom, _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos() (+17 more)

### Community 4 - "test_area.py"
Cohesion: 0.12
Nodes (29): sample(), _check_fields(), _construir(), _error(), load_lair(), AreaTargeting, select_area_targets(), _default_targeting() (+21 more)

### Community 5 - "test_enlarge.py"
Cohesion: 0.15
Nodes (24): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+16 more)

### Community 6 - "spell_action"
Cohesion: 0.07
Nodes (19): Paquetes con fachada, SaveAction, SpellAction, dado_por_nivel(), duracion_en_rondas(), Spell, spell_action(), Spellcasting (+11 more)

### Community 7 - "legendary_phase"
Cohesion: 0.13
Nodes (28): legendary_phase(), _contexto(), _pj(), test_con_una_sola_accion_asequible_pick_no_consume_rng(), test_dos_duenos_legendarios_actuan_cada_uno_una_vez(), test_el_combate_termina_en_medio_de_la_fase(), test_el_dragon_contra_un_grupo_usa_acciones_legendarias(), test_la_fase_ocurre_despues_del_end_turn() (+20 more)

### Community 8 - "test_beast.py"
Cohesion: 0.11
Nodes (64): _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll(), spy(), _forma() (+56 more)

### Community 9 - "test_spells.py"
Cohesion: 0.13
Nodes (30): parse_spell(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_daño_extra_del_hechizo_verdadero_no_baja_de_cinco(), test_el_lich_carga_sus_hechizos_utiles() (+22 more)

### Community 10 - "test_traits.py"
Cohesion: 0.11
Nodes (24): attack_modifiers(), _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _RasgoDeSalvacion, _sahuagin() (+16 more)

### Community 11 - "Condition"
Cohesion: 0.17
Nodes (25): Condition, _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj(), test_atacar_a_un_invisible_tiene_desventaja() (+17 more)

### Community 12 - "test_conditions.py"
Cohesion: 0.10
Nodes (34): _apply_condition_riders(), RepeatSave, _ctx(), _data(), _load(), _pj(), test_cada_fixture_tiene_un_tipo_de_ataque_coherente(), test_can_act_y_can_react() (+26 more)

### Community 13 - "Abilities"
Cohesion: 0.11
Nodes (22): Abilities, print_report(), simulate(), PlayerCharacter, build_parser(), _build_party(), _load_party(), main() (+14 more)

### Community 15 - "spell_parser.py"
Cohesion: 0.10
Nodes (13): _avisar(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla(), _frases() (+5 more)

### Community 16 - "DamageTransfer"
Cohesion: 0.15
Nodes (4): DamageTransfer, _empuna_arma_melee(), Parry, TurnResistance

### Community 17 - "Monster"
Cohesion: 0.14
Nodes (19): Carpetas, Monster, apply_damage_modifiers(), test_inmovilizado_da_desventaja_solo_en_des(), test_las_condiciones_incapacitantes_fallan_fue_y_des_sin_tirar_dados(), test_las_condiciones_incapacitantes_no_fallan_automaticamente_la_con(), test_petrificado_tiene_resistencia_a_todo(), test_sin_condiciones_el_dano_no_cambia() (+11 more)

### Community 18 - "BarbarianFeatures"
Cohesion: 0.10
Nodes (6): BarbarianFeatures, _contexto(), ExtendRageAction, RageAction, _rasgo(), test_las_armas_de_furia_no_distinguen_magical()

### Community 19 - "test_loader_actions.py"
Cohesion: 0.15
Nodes (12): is_area_action(), _area_action(), _data(), _load(), _raw_action(), test_accion_con_dc_sin_dano_sigue_ignorada(), test_accion_con_usage_desconocido_se_omite(), test_aliento_mapeado_a_area_con_recarga() (+4 more)

### Community 20 - "CombatContext"
Cohesion: 0.07
Nodes (15): _nuevo_ctx(), actor_is_alive(), AttackEntry, CombatAction, CombatContext, _en_accion_de_ataque(), _living_enemies(), _log() (+7 more)

### Community 21 - "test_legendary.py"
Cohesion: 0.10
Nodes (28): LegendaryAction, saving_throw(), _data(), _legendaria(), _load(), test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(), test_con_un_punto_solo_son_asequibles_las_de_coste_uno(), test_con_use_probability_uno_el_danio_es_mayor_que_con_cero() (+20 more)

### Community 22 - "Attack"
Cohesion: 0.12
Nodes (18): Attack, apply_beast(), test_alma_bestial_flag_magical_existe(), _ctx(), _pj(), test_ataque_con_magical_true_dana_completo_al_ghost(), test_ataque_magico_contra_un_bárbaro_en_furia_se_reduce_a_la_mitad(), test_bestial_solo_marca_las_armas_magicas_desde_el_nivel_6() (+10 more)

### Community 23 - "test_barbarian.py"
Cohesion: 0.10
Nodes (44): apply_barbarian(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj(), _resultado(), test_apply_anade_acciones_de_furia() (+36 more)

### Community 24 - "TurnResources"
Cohesion: 0.16
Nodes (33): AttackRange, TurnResources, AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer() (+25 more)

### Community 25 - "dnd_sim/__init__.py"
Cohesion: 0.09
Nodes (19): ability_mod(), _log_target(), legendary_resistance(), registrar_resistencia_legendaria(), apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save() (+11 more)

### Community 26 - "loader.py"
Cohesion: 0.09
Nodes (8): _damage_type(), _extract_multiattack_alternatives(), _parse_damage_modifiers(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada(), resolve_multiattack(), ExtraDamage

### Community 27 - "ActionType"
Cohesion: 0.16
Nodes (17): ActionType, _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo() (+9 more)

### Community 28 - "test_races.py"
Cohesion: 0.10
Nodes (24): Race, load_race(), parse_race(), _spells_from_description(), _abilities(), _fiendish_legacy(), _keen_senses(), _pj() (+16 more)

### Community 29 - "traits/__init__.py"
Cohesion: 0.14
Nodes (6): aliados_capaces(), BloodFrenzy, _condicion_posicional(), MartialAdvantage, test_hooks_con_un_nombre_fuera_del_catalogo_lanza_error(), test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 30 - "inflict_damage"
Cohesion: 0.05
Nodes (57): _entradas(), parse_traits(), _absorber_pv_temporales(), _hooks(), inflict_damage(), _is_petrified(), _mark_dead_if_down(), _mitigacion_de_otros() (+49 more)

### Community 31 - "pathlib"
Cohesion: 0.06
Nodes (27): Arquitectura de `dnd_sim`, Cómo comprobar que todo sigue en orden, Excepción única admitida, Imports diferidos, Reglas de dependencia, _capa(), _modulo_y_paquete(), test_las_capas_no_se_miran_hacia_arriba() (+19 more)

### Community 32 - "conditions.py"
Cohesion: 0.19
Nodes (8): _as_condition(), attempt_escapes(), _contar(), end_turn(), _label(), _queda_accion(), remove_condition(), remove_invisibility_on_action()

### Community 34 - "test_skills.py"
Cohesion: 0.14
Nodes (20): _abilities(), _ctx(), _load_fixture(), _pj(), _SoloMod, test_ability_check_no_suma_competencia_de_habilidad(), test_attempt_escapes_tira_la_habilidad(), test_check_modifiers_pasa_la_habilidad_a_los_rasgos() (+12 more)

### Community 35 - "json"
Cohesion: 0.06
Nodes (28): Background, normalize_tool(), _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell() (+20 more)

### Community 36 - "test_lair.py"
Cohesion: 0.09
Nodes (26): LairAction, LegendaryState, _ctx(), _dragon(), _enemigo(), lairs_dir(), _orden_con(), _pj() (+18 more)

### Community 37 - "test_proficiency.py"
Cohesion: 0.15
Nodes (21): proficiency_bonus(), ability_check_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia() (+13 more)

### Community 38 - "run_combat"
Cohesion: 0.06
Nodes (20): combat_finished(), living_teams(), _objetivo_enganche(), valid_targets(), resolve_roll_mode(), CombatResult, _invoke_policy(), roll_initiative() (+12 more)

### Community 39 - "Regeneration"
Cohesion: 0.10
Nodes (5): _es_radiante(), _guardar_salvacion(), Regeneration, Relentless, UndeadFortitude

### Community 40 - "RollMode"
Cohesion: 0.11
Nodes (13): RollMode, check_modifiers(), _condiciones(), _hooks(), save_modifiers(), _datos(), _lich(), _pj() (+5 more)

### Community 41 - "attack_roll"
Cohesion: 0.07
Nodes (60): D20Result, _actualizar_distancia(), attack_roll(), _mode_tag(), DamageRecorder, HeatedBody, _ataque_melee(), _ataque_ranged() (+52 more)

### Community 42 - "_duelo"
Cohesion: 0.14
Nodes (18): resolve_attack_range(), _ataque(), _duelo(), _tasa_de_impacto(), test_atacante_afectado_tiene_desventaja(), test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo(), test_dos_ventajas_y_una_desventaja_se_anulan(), test_los_indicadores_estaticos_siguen_funcionando_y_se_combinan() (+10 more)

### Community 43 - "combat/attack.py"
Cohesion: 0.06
Nodes (16): d20(), roll_d20(), roll_dice(), log_line(), _agrandado(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo() (+8 more)

### Community 44 - "legendary_parser.py"
Cohesion: 0.12
Nodes (10): _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision(), _nombres_candidatas(), parse_legendary(), _por_referencia() (+2 more)

### Community 45 - "SpellFixedDamageAction"
Cohesion: 0.15
Nodes (16): SpellFixedDamageAction, _ctx(), _npc(), _pj(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizado_invierte_los_objetivos_de_ataque(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado(), test_el_hechizo_verdadero_es_un_ataque_real_con_dano_extra() (+8 more)

### Community 46 - "pick"
Cohesion: 0.14
Nodes (6): pick(), _extract(), first_target_policy(), random_policy(), _contexto_de_reaccion(), trigger_reaction()

### Community 47 - "ability_check"
Cohesion: 0.15
Nodes (11): skill_ability(), ability_check(), CheckResult, _finish_check(), _guia(), _resolve_mods(), skill_bonus(), skill_check() (+3 more)

### Community 48 - "attach.py"
Cohesion: 0.13
Nodes (7): parse_attach_effects(), Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por()

### Community 49 - "test_pack_tactics.py"
Cohesion: 0.23
Nodes (14): _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj(), test_con_aliados_la_ventaja_se_sortea() (+6 more)

### Community 50 - "apply_condition"
Cohesion: 0.12
Nodes (36): apply_condition(), EscapeCheck, effective_ac(), _ctx(), _load(), _pj(), test_con_dos_caracteristicas_se_elige_una_al_azar(), test_con_una_sola_caracteristica_no_consume_rng() (+28 more)

### Community 51 - "load_monster"
Cohesion: 0.13
Nodes (16): _armor_class_value(), load_monster(), _norm_name(), test_fixture_sintetica_carga(), test_monstruo_no_legendario_no_carga_guaridas(), test_monstruo_sin_fichero_no_avisa(), _load_fixture(), _ogre_data() (+8 more)

### Community 52 - "pytest"
Cohesion: 0.22
Nodes (15): apply_ancestral_guardian(), apply_class(), _abilities(), _firmas(), _pj(), test_apply_class_ancestral_equivalente_a_los_apply_suelto(), test_apply_class_battlerager_equivalente_a_los_apply_suelto(), test_apply_class_normaliza_el_nombre() (+7 more)

### Community 53 - "test_martial_advantage.py"
Cohesion: 0.26
Nodes (14): _aliado(), _ctx(), _datos(), _espada(), _hobgoblin(), _pj(), test_con_aliados_el_daño_extra_es_aleatorio(), test_el_daño_extra_aparece_en_el_log_del_ataque() (+6 more)

### Community 54 - "parse_escape"
Cohesion: 0.15
Nodes (8): has_escape_text(), parse_escape(), _skills_for(), _data(), test_el_fixture_de_la_constriccion_tiene_escape_y_avisa_de_grappled(), test_el_fixture_de_la_telaraña_carga_restrained_con_escape(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 57 - "AttackAction"
Cohesion: 0.14
Nodes (4): normalize_ability(), AttackAction, CombatantType, test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio()

### Community 60 - "test_magic_resistance.py"
Cohesion: 0.09
Nodes (25): ConditionInstance, test_implicaciones_de_las_condiciones(), _ctx(), _objetivo(), _pj(), _spell_data(), _spellcasting(), _tasa() (+17 more)

### Community 61 - "parse_spellcasting"
Cohesion: 0.22
Nodes (4): parse_spellcasting(), test_el_lanzador_se_lee_de_los_actions(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 62 - "_duelo"
Cohesion: 0.32
Nodes (6): _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

### Community 63 - "normalize_skill"
Cohesion: 0.15
Nodes (6): _clean(), normalize_skill(), _skill_name(), _trait_skills(), test_normalize_skill_acepta_espacios_y_spanish(), test_normalize_skill_desconocida_lanza_value_error()

### Community 64 - "AreaSaveAction"
Cohesion: 0.13
Nodes (8): _por_datos(), build_condition_action(), build_save_action(), build_save_effect(), damage_dice_of(), damage_options(), damage_type_of(), AreaSaveAction

### Community 65 - "classes.py"
Cohesion: 0.19
Nodes (7): _clamp(), extra_attacks_for(), rage_damage(), rage_uses(), test_extra_attacks_desde_nivel_5(), test_rage_damage_tabla_phb(), test_rage_uses_tabla_phb()

### Community 66 - "combatant.py"
Cohesion: 0.11
Nodes (4): CombatState, DamageType, parse_damage_type(), ConditionTracker

### Community 67 - "ConditionAction"
Cohesion: 0.19
Nodes (6): ConditionAction, ConditionEffect, test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), test_la_resistencia_funciona_en_todas_las_rutas(), test_un_pj_con_ataque_con_rider_no_aplica_la_condicion_mientras_queden_usos(), test_condition_action_de_hechizo_pasa_magical()

### Community 68 - "condition_parser.py"
Cohesion: 0.15
Nodes (6): _condition_from_phrase(), _duration_rounds(), has_condition_text(), parse_condition_effects(), parse_range_type(), _sentence_with()

### Community 69 - "test_superior_invisibility.py"
Cohesion: 0.24
Nodes (12): SuperiorInvisibility, _accion(), _ctx(), _pixie(), _pj(), test_atacar_con_ventaja_y_no_pierde_la_invisibilidad(), test_ejecutarla_aplica_el_estado(), test_el_monstruo_recibe_su_accion_al_construirse() (+4 more)

### Community 70 - "warnings"
Cohesion: 0.15
Nodes (8): _resistencia_legendaria(), _declara_uso(), _usage(), parse_usage(), UnknownUsageError, _warn(), test_usage_parser_cada_tipo(), test_usage_parser_tipo_desconocido_avisa()

### Community 71 - "build_spell_actions"
Cohesion: 0.29
Nodes (7): build_spell_actions(), _desde_fixture(), _monstruo_lanzador(), test_gastar_un_uso_no_afecta_a_los_otros_hechizos(), test_max_spell_level_limita_el_nivel_cargado(), test_se_cargan_hechizos_de_todos_los_niveles_con_uso_propio(), test_un_hechizo_a_voluntad_se_puede_lanzar_en_cada_turno()

### Community 72 - "TODO — DnDBalancer / dnd_sim"
Cohesion: 0.33
Nodes (5): Bloque 2026-10-30 (commiteado), Grafo y verificación, Rutina sugerida al abrir sesión, TODO — DnDBalancer / dnd_sim, TODOs en código (marcados `# TODO`)

### Community 73 - "_estado"
Cohesion: 0.50
Nodes (3): _estado(), test_el_estado_legendario_rellena_gasta_y_reinicia(), test_use_probability_medio_se_usa_about_50_por_ciento()

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `attack_roll()` connect `attack_roll` to `test_attach.py`, `test_ancestral_guardian.py`, `test_enlarge.py`, `legendary_phase`, `test_beast.py`, `test_spells.py`, `test_traits.py`, `Condition`, `test_conditions.py`, `Abilities`, `Monster`, `CombatContext`, `test_legendary.py`, `Attack`, `dnd_sim/__init__.py`, `ActionType`, `inflict_damage`, `conditions.py`, `BeastFeatures`, `run_combat`, `_duelo`, `combat/attack.py`, `SpellFixedDamageAction`, `apply_condition`, `test_martial_advantage.py`, `test_magic_resistance.py`, `_duelo`, `combatant.py`, `ConditionAction`, `test_superior_invisibility.py`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `load_monster()` (e.g. with `UnknownUsageError` and `ActionType`) actually correct?**
  _`load_monster()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `battlerager.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07801418439716312 - nodes in this community are weakly interconnected._
- **Why does `Trait` connect `Trait` to `battlerager.py`, `BeastFeatures`, `test_superior_invisibility.py`, `warnings`, `spell_action`, `Regeneration`, `attack_roll`, `test_traits.py`, `combat/attack.py`, `attach.py`, `DamageTransfer`, `BarbarianFeatures`, `dnd_sim/__init__.py`, `AncestralGuardianFeatures`, `traits/__init__.py`, `inflict_damage`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `attack_roll()` (e.g. with `Attack` and `Combatant`) actually correct?**
  _`attack_roll()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_usage.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08672699849170437 - nodes in this community are weakly interconnected._
- **Why does `load_monster()` connect `load_monster` to `test_attach.py`, `test_usage.py`, `test_area.py`, `test_enlarge.py`, `spell_action`, `test_beast.py`, `test_spells.py`, `test_traits.py`, `Condition`, `test_conditions.py`, `Abilities`, `Monster`, `test_loader_actions.py`, `CombatContext`, `test_legendary.py`, `Attack`, `dnd_sim/__init__.py`, `loader.py`, `ActionType`, `inflict_damage`, `pathlib`, `test_skills.py`, `json`, `test_lair.py`, `RollMode`, `attack_roll`, `legendary_parser.py`, `attach.py`, `test_pack_tactics.py`, `apply_condition`, `test_martial_advantage.py`, `AttackAction`, `test_magic_resistance.py`, `normalize_skill`, `AreaSaveAction`, `condition_parser.py`, `warnings`, `build_spell_actions`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
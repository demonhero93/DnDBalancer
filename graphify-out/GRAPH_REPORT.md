# Graph Report - DnDBalancer  (2026-10-30)

## Corpus Check
- 188 files · ~117,847 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 1, .ini 1)

## Summary
- 2172 nodes · 7580 edges · 74 communities (62 shown, 12 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 402 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `99ebee77`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_clases.py
- test_attach.py
- test_ancestral_guardian.py
- test_usage.py
- test_area.py
- test_enlarge.py
- ActionType
- test_beast.py
- parse_spell
- test_traits.py
- Condition
- Abilities
- Attack
- Trait
- spell_parser.py
- DamageTransfer
- apply_damage_modifiers
- BarbarianFeatures
- test_loader_actions.py
- CombatContext
- test_legendary.py
- inflict_damage
- test_barbarian.py
- TurnResources
- apply_save_damage
- loader.py
- test_death.py
- json
- traits/__init__.py
- test_undead_fortitude.py
- test_multiattack.py
- apply_condition
- BeastFeatures
- test_skills.py
- test_backgrounds.py
- legendary.py
- test_proficiency.py
- run_combat
- Regeneration
- roll_modifiers.py
- attack_roll
- test_regeneration.py
- saves.py
- legendary_parser.py
- test_spells.py
- Combatant
- ability_check
- test_extra_damage.py
- RollMode
- test_checks_escapes.py
- load_monster
- test_azer.py
- test_relentless.py
- parse_escape
- AttackAction
- AncestralGuardianFeatures
- parse_spellcasting
- resolve_attack_range
- AreaSaveAction
- combat/attack.py
- dnd_sim/__init__.py
- BattleragerFeatures
- condition_parser.py
- test_superior_invisibility.py
- parse_traits
- StateEffect
- CallTheHuntBonus

## God Nodes (most connected - your core abstractions)
1. `attack_roll()` - 118 edges
2. `Attack` - 111 edges
3. `Abilities` - 110 edges
4. `apply_condition()` - 109 edges
5. `load_monster()` - 107 edges
6. `Condition` - 96 edges
7. `PlayerCharacter` - 87 edges
8. `CombatContext` - 82 edges
9. `run_combat()` - 76 edges
10. `Monster` - 76 edges

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

## Communities (74 total, 12 thin omitted)

### Community 0 - "test_clases.py"
Cohesion: 0.10
Nodes (24): apply_ancestral_guardian(), apply_battlerager(), SpikedArmorAction, FormOfTheBeast, NaturalWeapon, apply_class(), ClassDef, normalize_class_name() (+16 more)

### Community 1 - "test_attach.py"
Cohesion: 0.11
Nodes (31): Attach, AttachOnHitEffect, desenganchar(), enganchador_de(), intentar_desenganche(), _ya_cegado_por(), _atacar(), _bite() (+23 more)

### Community 2 - "test_ancestral_guardian.py"
Cohesion: 0.17
Nodes (26): _abilities(), _aliado(), _ataque_fijo(), _barbaro(), _ctx(), _danio_al_aliado(), _escudo(), _esperado() (+18 more)

### Community 3 - "test_usage.py"
Cohesion: 0.08
Nodes (22): _breath(), _eventos(), _FixedRandom, _load_fixture(), _player(), test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(), test_at_will_nunca_se_agota(), test_begin_turn_no_tira_nada_si_estan_cargadas() (+14 more)

### Community 4 - "test_area.py"
Cohesion: 0.22
Nodes (21): sample(), AreaTargeting, select_area_targets(), SaveDamage, _area_action(), _ctx(), _npc(), _pj() (+13 more)

### Community 5 - "test_enlarge.py"
Cohesion: 0.14
Nodes (25): doblar_dados(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _ogro(), _pj() (+17 more)

### Community 6 - "ActionType"
Cohesion: 0.08
Nodes (20): Paquetes con fachada, ActionType, CombatAction, SaveAction, ConditionAction, SpellAction, SpellAttackAction, SpellFixedDamageAction (+12 more)

### Community 8 - "test_beast.py"
Cohesion: 0.10
Nodes (66): WeaponAttackAction, apply_beast(), _abilities(), _barb(), _beast(), _ctx(), _en_furia(), _espiar_attack_roll() (+58 more)

### Community 9 - "parse_spell"
Cohesion: 0.13
Nodes (25): parse_spell(), _spell_data(), _spellcasting(), test_al_recibir_dano_en_un_ataque_se_dispara_la_reaccion(), test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot(), test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador(), test_el_daño_extra_del_hechizo_verdadero_no_baja_de_cinco(), test_el_proyectil_magico_es_dano_automatico() (+17 more)

### Community 10 - "test_traits.py"
Cohesion: 0.10
Nodes (25): attack_modifiers(), _ataque_melee(), _ctx(), _datos(), _pj(), _RasgoDePrueba, _RasgoDeSalvacion, _sahuagin() (+17 more)

### Community 11 - "Condition"
Cohesion: 0.19
Nodes (26): Condition, test_el_enum_no_contiene_condiciones_excluidas(), _accion(), _ataque(), _ctx(), _datos(), _duergar(), _pj() (+18 more)

### Community 12 - "Abilities"
Cohesion: 0.05
Nodes (74): Abilities, ability_mod(), Monster, ConditionInstance, end_turn(), RepeatSave, _ataque(), _ctx() (+66 more)

### Community 13 - "Attack"
Cohesion: 0.10
Nodes (23): print_report(), simulate(), Attack, PlayerCharacter, _nuevo_ataque(), build_parser(), _build_party(), _load_party() (+15 more)

### Community 14 - "Trait"
Cohesion: 0.06
Nodes (4): Trait, BloodFrenzy, test_hooks_con_un_nombre_fuera_del_catalogo_lanza_error(), test_hooks_solo_devuelve_los_que_sobrescriben_el_hook()

### Community 15 - "spell_parser.py"
Cohesion: 0.09
Nodes (14): _avisar(), build_spell_actions(), _condicion_con_salvacion(), _condiciones_de_frase(), _dados_hasta(), _elementos_por_nivel(), _elementos_totales(), _extender_tabla() (+6 more)

### Community 16 - "DamageTransfer"
Cohesion: 0.12
Nodes (6): DamageTransfer, _empuna_arma_melee(), HeatedBody, Parry, TurnResistance, _ve_al_atacante()

### Community 17 - "apply_damage_modifiers"
Cohesion: 0.22
Nodes (10): _tag_modificadores(), apply_damage_modifiers(), _target(), test_etiqueta_de_modificadores_se_deriva_del_dano_final(), test_immunity_zero(), test_invalid_damage_type_raises(), test_no_modifiers_unchanged(), test_resistance_halves_damage_floor() (+2 more)

### Community 18 - "BarbarianFeatures"
Cohesion: 0.10
Nodes (5): BarbarianFeatures, _contexto(), ExtendRageAction, RageAction, _rasgo()

### Community 19 - "test_loader_actions.py"
Cohesion: 0.11
Nodes (19): _usage(), parse_usage(), UnknownUsageError, UsageKind, _area_action(), _data(), _load(), _raw_action() (+11 more)

### Community 20 - "CombatContext"
Cohesion: 0.12
Nodes (7): actor_is_alive(), CombatContext, _en_accion_de_ataque(), _living_enemies(), _log(), HealAction, _romper_invisibilidad_al_lanzar()

### Community 21 - "test_legendary.py"
Cohesion: 0.05
Nodes (72): _apply_condition_riders(), ConditionEffect, legendary_phase(), save_modifiers(), saving_throw(), test_una_condicion_sin_salvacion_ni_escape_lanza_value_error(), _contexto(), _data() (+64 more)

### Community 22 - "inflict_damage"
Cohesion: 0.14
Nodes (9): _absorber_pv_temporales(), _hooks(), inflict_damage(), _is_petrified(), _mark_dead_if_down(), _mitigacion_de_otros(), _notify_damage_dealt(), _notify_damage_taken() (+1 more)

### Community 23 - "test_barbarian.py"
Cohesion: 0.09
Nodes (48): rage_uses(), apply_barbarian(), CheckModifiers, SaveModifiers, _abilities(), _ctx(), _pj(), _resultado() (+40 more)

### Community 24 - "TurnResources"
Cohesion: 0.16
Nodes (32): AttackRange, TurnResources, AttackModifiers, _abilities(), _accion_puas(), _ataque(), _barb(), _barrer() (+24 more)

### Community 25 - "apply_save_damage"
Cohesion: 0.15
Nodes (8): apply_save_damage(), _as_combat_context(), _con_resistencia_legendaria(), _inflict_for_save(), _reaccion_si_procede(), registrar_resistencia(), _resolve_mode_str(), SaveDamageOutcome

### Community 26 - "loader.py"
Cohesion: 0.09
Nodes (10): parse_attach_effects(), _damage_type(), _extract_multiattack_alternatives(), _norm_name(), _simple_damage_modifiers(), extract_multiattack_alternatives(), _norm_name(), _opcion_a_entrada() (+2 more)

### Community 27 - "test_death.py"
Cohesion: 0.16
Nodes (16): _BonusQueAnota, _ctx(), _npc(), _pj(), _RepresaliaMortal, test_el_ataque_que_remata_deja_el_objetivo_a_cero(), test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo(), test_el_combate_terminado_se_detecta_al_momento() (+8 more)

### Community 28 - "json"
Cohesion: 0.06
Nodes (35): Race, _cache_path(), get_background(), _get_entry(), get_monster(), get_race(), get_spell(), get_trait() (+27 more)

### Community 29 - "traits/__init__.py"
Cohesion: 0.10
Nodes (5): aliados_capaces(), _condicion_posicional(), MartialAdvantage, PackTactics, SuperiorInvisibility

### Community 30 - "test_undead_fortitude.py"
Cohesion: 0.21
Nodes (14): _ctx(), _datos(), _salva(), test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(), test_el_danyo_radiante_no_da_salvacion(), test_el_zombi_carga_su_undead_fortitude_con_su_dc(), test_la_cd_es_cinco_mas_el_danyo_recibido(), test_la_salvacion_puede_salvarlo_o_no() (+6 more)

### Community 31 - "test_multiattack.py"
Cohesion: 0.06
Nodes (28): Arquitectura de `dnd_sim`, Carpetas, Cómo comprobar que todo sigue en orden, Excepción única admitida, Imports diferidos, Reglas de dependencia, _capa(), _modulo_y_paquete() (+20 more)

### Community 32 - "apply_condition"
Cohesion: 0.16
Nodes (8): apply_condition(), _as_condition(), _contar(), _default_targeting(), _label(), _queda_accion(), remove_condition(), test_prueba_con_envenenado_o_aterrorizado_da_desventaja()

### Community 34 - "test_skills.py"
Cohesion: 0.13
Nodes (21): _abilities(), _ctx(), _load_fixture(), _pj(), _SoloMod, test_ability_check_no_suma_competencia_de_habilidad(), test_attempt_escapes_tira_la_habilidad(), test_caracteristica_asociada() (+13 more)

### Community 35 - "test_backgrounds.py"
Cohesion: 0.11
Nodes (19): Background, normalize_tool(), _add(), load_background(), parse_background(), _abilities(), _pj(), test_apply_background_añade_las_competencias() (+11 more)

### Community 36 - "legendary.py"
Cohesion: 0.09
Nodes (11): _accion_utilizable(), _acciones_asequibles(), _contar_accion(), _contar_puntos(), _contar_resistencia(), _contexto_de(), legendary_resistance(), LegendaryAction (+3 more)

### Community 37 - "test_proficiency.py"
Cohesion: 0.17
Nodes (20): proficiency_bonus(), _abilities(), _pj(), test_ability_check_bonus_delega_en_check_bonus(), test_ability_check_bonus_sin_metodo_check_bonus(), test_ability_check_usa_el_bono_completo(), test_check_bonus_con_competencia(), test_check_bonus_sin_competencia() (+12 more)

### Community 38 - "run_combat"
Cohesion: 0.12
Nodes (12): d20(), roll_d20(), combat_finished(), living_teams(), _objetivo_enganche(), valid_targets(), CombatResult, _invoke_policy() (+4 more)

### Community 39 - "Regeneration"
Cohesion: 0.11
Nodes (5): _es_radiante(), _guardar_salvacion(), Regeneration, Relentless, UndeadFortitude

### Community 40 - "roll_modifiers.py"
Cohesion: 0.17
Nodes (6): check_modifiers(), _condiciones(), effective_ac(), _hooks(), test_la_ca_efectiva_sube_dos_a_distancia(), test_los_flags_de_prueba_son_por_caracteristica()

### Community 41 - "attack_roll"
Cohesion: 0.17
Nodes (24): D20Result, _actualizar_distancia(), attack_roll(), _mode_tag(), _arquero_parry(), _ataque(), _ctx(), _datos() (+16 more)

### Community 42 - "test_regeneration.py"
Cohesion: 0.28
Nodes (14): _ctx(), _datos(), _pj(), test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(), test_el_daño_normal_no_bloquea_la_regeneracion(), test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(), test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno(), test_el_troll_carga_su_regeneracion() (+6 more)

### Community 43 - "saves.py"
Cohesion: 0.10
Nodes (7): _clamp(), extra_attacks_for(), rage_damage(), roll_dice(), log_line(), _habilitar_armas_naturales(), resolve_save_damage()

### Community 44 - "legendary_parser.py"
Cohesion: 0.07
Nodes (22): is_area_action(), parse_condition_effects(), parse_range_type(), _coincide_nombre(), _con_nombre_limpio(), _condicion_de(), _coste_y_nombre(), _motivo_omision() (+14 more)

### Community 45 - "test_spells.py"
Cohesion: 0.12
Nodes (25): _ctx(), _desde_fixture(), _monstruo_lanzador(), _npc(), _pj(), test_el_hechizado_ataca_a_los_de_su_propio_bando(), test_el_hechizado_invierte_los_objetivos_de_ataque(), test_el_hechizo_de_hechizar_deja_el_estado_hechizado() (+17 more)

### Community 46 - "Combatant"
Cohesion: 0.13
Nodes (3): Combatant, _contexto_de_reaccion(), trigger_reaction()

### Community 47 - "ability_check"
Cohesion: 0.10
Nodes (14): _clean(), normalize_skill(), skill_ability(), ability_check(), ability_check_bonus(), CheckResult, _finish_check(), _guia() (+6 more)

### Community 48 - "test_extra_damage.py"
Cohesion: 0.18
Nodes (17): DamageRecorder, _azer(), _ctx(), _datos(), _dragon(), _espiar_inflict(), _pj(), test_al_impactar_se_infinge_tambien_el_daño_adicional() (+9 more)

### Community 49 - "RollMode"
Cohesion: 0.19
Nodes (15): RollMode, _aliado(), _ctx(), _datos(), _lobo(), _mods_con_estado(), _mordisco(), _pj() (+7 more)

### Community 50 - "test_checks_escapes.py"
Cohesion: 0.11
Nodes (37): attempt_escapes(), EscapeCheck, begin_turn(), _check_fijo(), _fake(), _ctx(), _data(), _load() (+29 more)

### Community 51 - "load_monster"
Cohesion: 0.12
Nodes (14): _armor_class_value(), load_monster(), MultiattackAction, _load_fixture(), _ogre_data(), test_armor_class_as_list(), test_armor_class_as_number(), test_armor_class_helper() (+6 more)

### Community 52 - "test_azer.py"
Cohesion: 0.26
Nodes (17): _ataque_melee(), _ataque_ranged(), _azer(), _ctx(), _datos(), _pj(), _rasgo(), test_ataque_a_distancia_no_dispara_la_represalia() (+9 more)

### Community 53 - "test_relentless.py"
Cohesion: 0.27
Nodes (12): _ctx(), _datos(), _jabali(), _pj(), test_el_jabali_carga_su_relentless_con_umbral_y_uso(), test_relentless_no_necesita_contexto_ni_rng(), test_reset_reestablece_el_umbral_y_los_usos(), test_solo_puede_salvarse_una_vez_por_combate() (+4 more)

### Community 54 - "parse_escape"
Cohesion: 0.22
Nodes (5): has_escape_text(), parse_escape(), _skills_for(), test_escape_de_telaraña_usa_atletismo(), test_escape_sin_caracteristica_usa_atletismo_y_acrobacias()

### Community 57 - "AttackAction"
Cohesion: 0.14
Nodes (5): normalize_ability(), DamageType, parse_damage_type(), AttackAction, ExtraDamage

### Community 61 - "parse_spellcasting"
Cohesion: 0.20
Nodes (5): parse_spellcasting(), test_el_lanzador_se_lee_de_los_actions(), test_initialize_slots_usa_la_tabla_local_de_un_lanzador_completo(), test_la_curacion_usa_el_modificador_de_caracteristica_no_el_bono_completo(), test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado()

### Community 62 - "resolve_attack_range"
Cohesion: 0.25
Nodes (8): resolve_attack_range(), _ataque(), _duelo(), _tasa_de_impacto(), test_contra_un_objetivo_a_distancia_baja_el_impacto(), test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue(), test_objetivo_derribado_y_melee_or_ranged_depende_del_modo(), test_un_ataque_a_distancia_pone_al_atacante_a_distancia()

### Community 64 - "AreaSaveAction"
Cohesion: 0.14
Nodes (8): AreaSaveAction, _log_target(), _mode_tag(), _outcome_tag(), _log_line_outcome(), SaveResult, _save_forzado(), fake_saving_throw()

### Community 65 - "combat/attack.py"
Cohesion: 0.13
Nodes (11): _agrandado(), _bonus_de_rasgos(), _bonus_de_tamano(), _bonus_defensivo(), _dados_de_ataque(), _reaccion_si_procede(), resolve_roll_mode(), _trigger_after_attack_roll() (+3 more)

### Community 66 - "dnd_sim/__init__.py"
Cohesion: 0.10
Nodes (7): CombatState, pick(), _extract(), first_target_policy(), random_policy(), CombatantType, ConditionTracker

### Community 68 - "condition_parser.py"
Cohesion: 0.13
Nodes (4): _condition_from_phrase(), _duration_rounds(), has_condition_text(), _sentence_with()

### Community 69 - "test_superior_invisibility.py"
Cohesion: 0.30
Nodes (12): remove_invisibility_on_action(), _accion(), _ctx(), _pixie(), _pj(), test_atacar_con_ventaja_y_no_pierde_la_invisibilidad(), test_ejecutarla_aplica_el_estado(), test_el_monstruo_recibe_su_accion_al_construirse() (+4 more)

### Community 70 - "parse_traits"
Cohesion: 0.17
Nodes (8): _declara_uso(), _entradas(), parse_traits(), test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd(), test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad(), test_el_umbral_se_saca_de_cada_descripcion(), test_el_rasgo_se_parsea_desde_el_srd(), test_parse_traits_ignora_entradas_malformadas()

## Knowledge Gaps
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_monster()` connect `load_monster` to `test_attach.py`, `test_usage.py`, `test_area.py`, `test_enlarge.py`, `ActionType`, `test_beast.py`, `test_traits.py`, `Condition`, `Abilities`, `Attack`, `spell_parser.py`, `test_loader_actions.py`, `test_legendary.py`, `loader.py`, `test_death.py`, `json`, `test_undead_fortitude.py`, `test_multiattack.py`, `test_skills.py`, `attack_roll`, `test_regeneration.py`, `legendary_parser.py`, `test_spells.py`, `ability_check`, `test_extra_damage.py`, `RollMode`, `test_checks_escapes.py`, `test_azer.py`, `test_relentless.py`, `AttackAction`, `dnd_sim/__init__.py`, `condition_parser.py`, `parse_traits`, `StateEffect`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `attack_roll()` (e.g. with `Attack` and `Combatant`) actually correct?**
  _`attack_roll()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_clases.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09608843537414966 - nodes in this community are weakly interconnected._
- **Why does `attack_roll()` connect `attack_roll` to `test_attach.py`, `test_ancestral_guardian.py`, `test_enlarge.py`, `ActionType`, `test_beast.py`, `parse_spell`, `test_traits.py`, `Condition`, `Abilities`, `Attack`, `apply_damage_modifiers`, `CombatContext`, `test_legendary.py`, `inflict_damage`, `test_death.py`, `BeastFeatures`, `run_combat`, `roll_modifiers.py`, `saves.py`, `test_spells.py`, `Combatant`, `test_extra_damage.py`, `test_checks_escapes.py`, `test_azer.py`, `AttackAction`, `resolve_attack_range`, `combat/attack.py`, `test_superior_invisibility.py`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Attack` (e.g. with `attack_roll()` and `AttackRange`) actually correct?**
  _`Attack` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_attach.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10917874396135266 - nodes in this community are weakly interconnected._
- **Why does `Trait` connect `Trait` to `test_attach.py`, `dnd_sim/__init__.py`, `BattleragerFeatures`, `BeastFeatures`, `parse_traits`, `ActionType`, `CallTheHuntBonus`, `Regeneration`, `test_traits.py`, `saves.py`, `DamageTransfer`, `BarbarianFeatures`, `AncestralGuardianFeatures`, `traits/__init__.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
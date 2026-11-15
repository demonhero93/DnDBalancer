"""Tests de la subclase Samurai (XGE, Guerrero).

Solo cubren lo que existe: en A1, las tablas de ``core/classes.py``; en
A2, el esqueleto, el registro y los datos sin efecto; en A3, Fighting
Spirit; en A4, Rapid Strike; en A5, la función de turno reutilizable y
en A6, Strength Before Death.
"""

from __future__ import annotations

import random

import pytest

from dnd_sim import Abilities, Attack, Monster, PlayerCharacter, apply_class
from dnd_sim.core.classes import (
    SAMURAI_BONUS_SKILLS,
    fighting_spirit_temp_hp,
    fighting_spirit_uses,
)
from dnd_sim.core.dice import RollMode
from dnd_sim.core.enums import AttackRange
from dnd_sim.core.skills import SKILL_ABILITIES
from dnd_sim.engine.combat import attack as attack_mod
from dnd_sim.engine.combat.attack import attack_roll
from dnd_sim.engine.combat.encounter import roll_initiative, run_combat
from dnd_sim.model.actions import (
    ActionType,
    MultiattackAction,
    TurnResources,
)
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import SamuraiFeatures, apply_samurai
from dnd_sim.rules.conditions import Condition, apply_condition
from dnd_sim.rules.roll_modifiers import AttackModifiers, attack_modifiers


# --- A1: tablas --------------------------------------------------------------


def test_tabla_fighting_spirit_uses_por_nivel():
    assert fighting_spirit_uses(1) == 0
    assert fighting_spirit_uses(2) == 0
    assert fighting_spirit_uses(3) == 3
    assert fighting_spirit_uses(10) == 3
    assert fighting_spirit_uses(20) == 3


def test_tabla_fighting_spirit_temp_hp_por_nivel():
    assert fighting_spirit_temp_hp(1) == 0
    assert fighting_spirit_temp_hp(2) == 0
    assert fighting_spirit_temp_hp(3) == 5
    assert fighting_spirit_temp_hp(9) == 5
    assert fighting_spirit_temp_hp(10) == 10
    assert fighting_spirit_temp_hp(14) == 10
    assert fighting_spirit_temp_hp(15) == 15
    assert fighting_spirit_temp_hp(20) == 15


def test_pool_samurai_bonus_skills_son_las_cuatro_de_xge():
    assert SAMURAI_BONUS_SKILLS == (
        "history", "insight", "performance", "persuasion")
    # Las cuatro existen en la tabla de habilidades del proyecto
    # (Interpretación = "performance").
    for skill in SAMURAI_BONUS_SKILLS:
        assert skill in SKILL_ABILITIES


# --- A2: esqueleto, registro y datos sin efecto ------------------------------


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=14, wis=12, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Camila", max_hp=70, ac=15, level=5, abilities=_abilities(),
        attacks=[Attack("Espada larga", "1d8", ability="str")],
    )
    defaults.update(kwargs)
    return PlayerCharacter(**defaults)


def test_samurai_registrada_en_la_tabla_de_subclases():
    assert "samurai" in CLASSES["fighter"].subclasses
    sub = CLASSES["fighter"].subclasses["samurai"]
    assert sub.name == "Samurai"
    assert sub.class_name == "fighter"
    assert sub.min_level == 3


def test_apply_class_y_apply_samurai_son_equivalentes(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod

    a = _pj(level=3)
    apply_fighter(a, level=3, fighting_style="Archery")
    monkeypatch.setattr(sm_mod, "_RNG_CREACION", random.Random(0))
    t1 = apply_samurai(a, level=3)

    b = _pj(level=3)
    monkeypatch.setattr(sm_mod, "_RNG_CREACION", random.Random(0))
    apply_class(b, "fighter", subclass_name="samurai", level=3,
                fighting_style="Archery")
    t2 = [x for x in b.traits if isinstance(x, SamuraiFeatures)][0]

    assert (t1.name, t1.level, t1.competencia, t1.courtier_save) == (
        t2.name, t2.level, t2.competencia, t2.courtier_save)
    assert set(a.skill_proficiencies) == set(b.skill_proficiencies)
    assert t1.spirit_uses.uses_max == t2.spirit_uses.uses_max == 3
    assert t1.sbd_uses.uses_max == t2.sbd_uses.uses_max == 1


def test_apply_samurai_exige_la_clase_guerrero():
    pj = _pj(level=3)
    with pytest.raises(ValueError, match="Primero aplica la clase guerrero"):
        apply_samurai(pj, level=3)


def test_apply_samurai_exige_nivel_minimo_tres():
    pj = _pj(level=3)
    apply_fighter(pj, level=3, fighting_style="Archery")
    with pytest.raises(ValueError, match="nivel >= 3"):
        apply_samurai(pj, level=2)


def test_el_bonus_proficiency_anade_una_habilidad_nueva():
    pj = _pj(level=3)
    apply_fighter(pj, level=3, fighting_style="Archery")
    antes = set(pj.skill_proficiencies or set())
    trait = apply_samurai(pj, level=3)
    assert trait.competencia in SAMURAI_BONUS_SKILLS
    assert trait.competencia not in antes
    assert set(pj.skill_proficiencies) == antes | {trait.competencia}


def test_sin_candidatas_el_bonus_proficiency_no_cambia_nada(monkeypatch):
    def _revienta(rng, seq):
        raise AssertionError("sin candidatas no se consulta el pick")

    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod

    pj = _pj(level=3)
    pj.skill_proficiencies = set(SAMURAI_BONUS_SKILLS)
    apply_fighter(pj, level=3, fighting_style="Archery")
    antes = set(pj.skill_proficiencies)
    monkeypatch.setattr(sm_mod, "pick", _revienta)
    trait = apply_samurai(pj, level=3)
    assert trait.competencia == ""
    assert set(pj.skill_proficiencies) == antes


def test_el_elegant_courtier_concede_sab_desde_el_nivel_siete():
    pj5 = _pj(level=5)
    apply_fighter(pj5, level=5, fighting_style="Archery")
    t5 = apply_samurai(pj5, level=5)
    assert "wis" not in set(pj5.save_proficiencies)
    assert t5.courtier_save == ""

    pj7 = _pj(level=7)
    apply_fighter(pj7, level=7, fighting_style="Archery")
    t7 = apply_samurai(pj7, level=7)
    assert "wis" in set(pj7.save_proficiencies)
    assert t7.courtier_save == "wis"


def test_el_elegant_courtier_elige_int_o_cha_si_ya_tiene_sab():
    pj = _pj(level=7)
    apply_fighter(pj, level=7, fighting_style="Archery")
    pj.save_proficiencies = set(pj.save_proficiencies) | {"wis"}
    trait = apply_samurai(pj, level=7)
    assert trait.courtier_save in ("int", "cha")
    # Sin duplicados: la salvación concedida es la nueva y solo una.
    assert set(pj.save_proficiencies) == {
        "str", "con", "wis", trait.courtier_save}


def test_tireless_spirit_no_recupera_usos_al_tirar_iniciativa():
    # Dato sin efecto por diseño: cada combate empieza con los 3 usos
    # completos (mismo criterio que Ever-Ready Shot del Arcane Archer).
    pj = _pj(level=10)
    apply_fighter(pj, level=10, fighting_style="Archery")
    trait = apply_samurai(pj, level=10)
    roll_initiative([pj, _pj(name="Otra")], random.Random(1))
    assert trait.spirit_uses.uses_left == 3
    assert trait.spirit_uses.available


def test_el_bonificador_social_de_elegant_courtier_es_dato_sin_efecto():
    # El rasgo no sobrescribe modify_check_modifiers: Perspicacia y
    # Persuasión no reciben bono del mod SAB en el sim (sin
    # pruebas sociales en combate).
    assert "modify_check_modifiers" not in SamuraiFeatures.__dict__


def test_sin_la_subclase_no_hay_ni_rasgo_ni_rng(monkeypatch):
    def _revienta(rng, seq):
        raise AssertionError("sin la subclase no hay decisiones")

    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod

    monkeypatch.setattr(sm_mod, "pick", _revienta)
    pj = _pj(level=3)
    apply_class(pj, "fighter", level=3, fighting_style="Archery")
    assert not any(isinstance(x, SamuraiFeatures) for x in pj.traits)


# --- A3: Fighting Spirit -----------------------------------------------------


def _samurai(level: int = 3) -> tuple[PlayerCharacter, SamuraiFeatures]:
    pj = _pj(level=level)
    apply_fighter(pj, level=level, fighting_style="Archery")
    trait = apply_samurai(pj, level=level)
    # Sin maestría en el arma de test: Sap marcaría desventaja tras un
    # impacto y contaminaría el estado de ventaja del ataque adicional.
    for ataque in pj.attacks:
        ataque.mastery = ""
    return pj, trait


def _ctx(pj: PlayerCharacter, *otros: PlayerCharacter):
    from types import SimpleNamespace

    return SimpleNamespace(
        round=1, actor=pj, rng=random.Random(1),
        combatants=[pj, *otros], log=[], verbose=False,
        resources=TurnResources(), is_reaction=False, skip_turn=False,
    )


def _si(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod

    monkeypatch.setattr(sm_mod, "pick", lambda rng, seq: "sí")


def _enemigo() -> Monster:
    return Monster("Orco", max_hp=60, ac=10, abilities=_abilities())


def test_la_ventaja_de_fighting_spirit_se_aplica_a_los_ataques_del_mismo_turno(
        monkeypatch):
    pj, trait = _samurai(3)
    otro = _enemigo()
    ctx = _ctx(pj, otro)
    _si(monkeypatch)
    trait.on_turn_start(pj, ctx)
    assert trait.spirit_activo
    assert pj.temp_hp == 5

    capturados = []
    real_roll_d20 = attack_mod.roll_d20

    def _cap(rng, mode=RollMode.NORMAL, **kw):
        capturados.append(mode)
        return real_roll_d20(rng, mode)

    monkeypatch.setattr(attack_mod, "roll_d20", _cap)
    attack_roll(pj, otro, pj.attacks[0], random.Random(2), ctx=ctx)
    assert capturados == [RollMode.ADVANTAGE]


def test_fighting_spirit_no_da_ventaja_en_ataques_de_hechizo():
    pj, trait = _samurai(3)
    otro = _pj(name="Otra")
    trait.spirit_activo = True
    mods = AttackModifiers()
    hechizo = Attack("Destello", "1d8", ability="int")
    hechizo.spell_attack = True
    trait.modify_attack_modifiers(
        mods, pj, otro, AttackRange.MELEE, atk=hechizo)
    trait.modify_attack_modifiers(
        mods, pj, otro, AttackRange.MELEE, atk=None)
    assert mods.advantage_sources == []


def test_fighting_spirit_con_ventaja_se_anula_con_desventaja(monkeypatch):
    pj, trait = _samurai(3)
    otro = _pj(name="Otra")
    ctx = _ctx(pj, otro)
    _si(monkeypatch)
    trait.on_turn_start(pj, ctx)
    apply_condition(pj, Condition.BLINDED, ctx)
    mods = attack_modifiers(pj, otro, pj.attacks[0], rng=random.Random(1))
    assert "Fighting Spirit" in mods.advantage_sources
    assert "atacante cegado" in mods.disadvantage_sources
    assert mods.mode is RollMode.NORMAL


def test_los_pv_temporales_son_5_10_15_segun_nivel_sin_acumulacion(monkeypatch):
    for nivel, esperado in ((3, 5), (10, 10), (15, 15)):
        pj, trait = _samurai(nivel)
        _si(monkeypatch)
        trait.on_turn_start(pj, _ctx(pj))
        assert pj.temp_hp == esperado
        assert trait.spirit_activo
    # Sin acumulación: se queda el mayor (patrón Vitality Surge).
    pj, trait = _samurai(3)
    pj.temp_hp = 12
    _si(monkeypatch)
    trait.on_turn_start(pj, _ctx(pj))
    assert pj.temp_hp == 12
    pj2, trait2 = _samurai(15)
    pj2.temp_hp = 20
    trait2.on_turn_start(pj2, _ctx(pj2))
    assert pj2.temp_hp == 20


def test_fighting_spirit_tiene_tres_usos_y_gasta_la_accion_adicional(
        monkeypatch):
    pj, trait = _samurai(3)
    _si(monkeypatch)
    ctx = _ctx(pj)
    trait.on_turn_start(pj, ctx)
    assert trait.spirit_uses.uses_left == 2
    assert ctx.resources.bonus_action_used  # es el coste: acción bonus
    trait.on_any_turn_end(pj, ctx)
    trait.on_turn_start(pj, _ctx(pj))
    trait.on_any_turn_end(pj, _ctx(pj))
    trait.on_turn_start(pj, _ctx(pj))
    assert trait.spirit_uses.uses_left == 0
    trait.on_any_turn_end(pj, _ctx(pj))

    def _revienta(rng, seq):
        raise AssertionError("sin usos no se consulta el pick")

    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod
    monkeypatch.setattr(sm_mod, "pick", _revienta)
    trait.on_turn_start(pj, _ctx(pj))
    assert not trait.spirit_activo


def test_no_se_activa_si_la_accion_adicional_ya_gasto(monkeypatch):
    pj, trait = _samurai(3)

    def _revienta(rng, seq):
        raise AssertionError("con la acción gastada no hay pick")

    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod
    monkeypatch.setattr(sm_mod, "pick", _revienta)
    ctx = _ctx(pj)
    ctx.resources.use(ActionType.BONUS_ACTION)
    trait.on_turn_start(pj, ctx)
    assert trait.spirit_uses.uses_left == 3
    assert not trait.spirit_activo


def test_no_se_reactiva_en_el_mismo_turno(monkeypatch):
    pj, trait = _samurai(3)
    _si(monkeypatch)
    trait.on_turn_start(pj, _ctx(pj))
    assert trait.spirit_uses.uses_left == 2

    def _revienta(rng, seq):
        raise AssertionError("ya activo en este turno no hay pick")

    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod
    monkeypatch.setattr(sm_mod, "pick", _revienta)
    trait.on_turn_start(pj, _ctx(pj))
    assert trait.spirit_uses.uses_left == 2
    assert trait.spirit_activo


def test_el_flag_se_apaga_al_final_del_turno_y_puede_volver(monkeypatch):
    pj, trait = _samurai(3)
    _si(monkeypatch)
    ctx = _ctx(pj)
    trait.on_turn_start(pj, ctx)
    assert trait.spirit_activo
    trait.on_any_turn_end(pj, ctx)
    assert not trait.spirit_activo
    trait.on_turn_start(pj, _ctx(pj))
    assert trait.spirit_activo
    assert trait.spirit_uses.uses_left == 1


def test_en_run_combat_fighting_spirit_se_activa_y_da_ventaja(monkeypatch):
    pj, trait = _samurai(3)
    otro = _enemigo()
    _si(monkeypatch)
    capturados = []
    real_roll_d20 = attack_mod.roll_d20

    def _cap(rng, mode=RollMode.NORMAL, **kw):
        capturados.append(mode)
        return real_roll_d20(rng, mode)

    monkeypatch.setattr(attack_mod, "roll_d20", _cap)
    run_combat([pj, otro], random.Random(7), max_rounds=6)
    # Se activó en los tres primeros turnos del dueño (pick siempre
    # «sí») y sus ataques rindieron con ventaja en el mismo turno.
    assert trait.spirit_uses.uses_left == 0
    assert RollMode.ADVANTAGE in capturados


def test_sin_la_subclase_los_ataques_no_consumen_rng_de_samurai(
        monkeypatch):
    def _revienta(rng, seq):
        raise AssertionError("sin la subclase no hay decisiones")

    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod
    monkeypatch.setattr(sm_mod, "pick", _revienta)
    pj = _pj(level=3)
    apply_class(pj, "fighter", level=3, fighting_style="Archery")
    otro = _enemigo()
    attack_roll(pj, otro, pj.attacks[0], random.Random(2),
                ctx=_ctx(pj, otro))
    assert not any(isinstance(x, SamuraiFeatures) for x in pj.traits)


# --- A4: Rapid Strike --------------------------------------------------------


def _ctx_ataque(pj, *otros):
    ctx = _ctx(pj, *otros)
    ctx.in_attack_action = True
    return ctx


def _capturador(monkeypatch):
    capturados = []
    real_roll_d20 = attack_mod.roll_d20

    def _cap(rng, mode=RollMode.NORMAL, **kw):
        capturados.append(mode)
        return real_roll_d20(rng, mode)

    monkeypatch.setattr(attack_mod, "roll_d20", _cap)
    return capturados


def _contador_pick(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod

    llamadas = []

    def _cuenta(rng, seq):
        llamadas.append(tuple(seq))
        return "sí"

    monkeypatch.setattr(sm_mod, "pick", _cuenta)
    return llamadas


def test_con_ventaja_puede_renunciar_y_hace_un_ataque_adicional(
        monkeypatch):
    pj, trait = _samurai(15)
    orco = _enemigo()
    ctx = _ctx_ataque(pj, orco)
    _si(monkeypatch)
    trait.on_turn_start(pj, ctx)  # Fighting Spirit da la ventaja
    assert trait.spirit_activo
    capturados = _capturador(monkeypatch)
    llamadas = _contador_pick(monkeypatch)  # solo cuenta las de ataque
    objetivos = []
    real_am = attack_mod.attack_modifiers

    def _cap_am(attacker, target, attack, rango=None, **kw):
        objetivos.append(target)
        return real_am(attacker, target, attack, rango, **kw)

    monkeypatch.setattr(attack_mod, "attack_modifiers", _cap_am)
    attack_roll(pj, orco, pj.attacks[0], random.Random(2), ctx=ctx)
    # La principal renunció (modo normal); el adicional corre su propio
    # estado de ventaja (Fighting Spirit sigue activo) contra el mismo
    # objetivo. Un solo pick: el de la renuncia.
    assert capturados == [RollMode.NORMAL, RollMode.ADVANTAGE]
    assert objetivos == [orco, orco]
    assert llamadas == [("no", "sí")]
    assert trait.rapid_strike_used


def test_sin_ventaja_neta_no_es_elegible_y_no_consume_rng(monkeypatch):
    pj, trait = _samurai(15)  # sin Fighting Spirit activo

    def _revienta(rng, seq):
        raise AssertionError("sin ventaja neta no hay consulta al pick")

    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod
    monkeypatch.setattr(sm_mod, "pick", _revienta)
    orco = _enemigo()
    capturados = _capturador(monkeypatch)
    attack_roll(pj, orco, pj.attacks[0], random.Random(2),
                ctx=_ctx_ataque(pj, orco))
    assert capturados == [RollMode.NORMAL]
    assert not trait.rapid_strike_used


def test_rapid_strike_se_usa_una_vez_por_turno_y_el_flag_se_reinicia(
        monkeypatch):
    pj, trait = _samurai(15)
    orco = _enemigo()
    ctx = _ctx_ataque(pj, orco)
    _si(monkeypatch)
    trait.on_turn_start(pj, ctx)
    capturados = _capturador(monkeypatch)
    llamadas = _contador_pick(monkeypatch)
    attack_roll(pj, orco, pj.attacks[0], random.Random(2), ctx=ctx)
    # Mismo turno, segundo ataque: el flag bloquea otra renuncia.
    attack_roll(pj, orco, pj.attacks[0], random.Random(3), ctx=ctx)
    assert llamadas == [("no", "sí")]
    assert capturados == [RollMode.NORMAL, RollMode.ADVANTAGE,
                          RollMode.ADVANTAGE]
    # Nuevo turno: on_turn_start limpia el flag y vuelve a poder.
    trait.on_turn_start(pj, _ctx_ataque(pj, orco))
    attack_roll(pj, orco, pj.attacks[0], random.Random(4), ctx=ctx)
    assert llamadas == [("no", "sí"), ("no", "sí")]


def test_no_vale_para_ataques_de_reaccion_ni_con_hechizos(monkeypatch):
    pj, trait = _samurai(15)
    orco = _enemigo()
    _si(monkeypatch)
    ctx_r = _ctx_ataque(pj, orco)
    ctx_r.is_reaction = True
    trait.on_turn_start(pj, ctx_r)  # Fighting Spirit activo

    def _revienta(rng, seq):
        raise AssertionError("reacciones y hechizos no consultan el pick")

    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod
    monkeypatch.setattr(sm_mod, "pick", _revienta)
    capturados = _capturador(monkeypatch)
    # Reacción: ctx.is_reaction corta antes del pick (tira con la
    # ventaja que ya tiene, sin renunciar).
    attack_roll(pj, orco, pj.attacks[0], random.Random(2), ctx=ctx_r)
    # Hechizo: con ventaja (attacks_with_advantage) el rasgo rechaza el
    # ataque mágico antes del pick: una sola tirada, sin renuncia.
    pj.attacks_with_advantage = True
    hechizo = Attack("Destello", "1d8", ability="int")
    hechizo.spell_attack = True
    attack_roll(pj, orco, hechizo, random.Random(3), ctx=ctx_r)
    assert capturados == [RollMode.ADVANTAGE, RollMode.ADVANTAGE]
    assert not trait.rapid_strike_used


def test_el_ataque_adicional_no_gasta_los_ataques_de_la_accion(
        monkeypatch):
    pj, trait = _samurai(15)
    orco = _enemigo()
    ctx = _ctx(pj, orco)
    _si(monkeypatch)
    trait.on_turn_start(pj, ctx)  # ventaja de Fighting Spirit

    import dnd_sim.rules.utility as util_mod
    monkeypatch.setattr(
        util_mod, "ataque_utilitario", lambda *a, **k: False)
    llamadas = _contador_pick(monkeypatch)
    capturados = _capturador(monkeypatch)
    multi = [a for a in pj.actions
             if isinstance(a, MultiattackAction)][0]
    multi.execute(ctx)
    # Nivel 15: 3 golpes de la acción + 1 adicional = 4 tiradas, y una
    # sola renuncia (flag por turno): la acción no pierde golpes.
    assert len(capturados) == 4
    assert llamadas == [("no", "sí")]


def test_en_nivel_catorce_no_actua(monkeypatch):
    pj, trait = _samurai(14)
    orco = _enemigo()
    _si(monkeypatch)  # Fighting Spirit sí (nivel 14)
    trait.on_turn_start(pj, _ctx_ataque(pj, orco))

    def _revienta(rng, seq):
        raise AssertionError("el nivel 14 no tiene Rapid Strike")

    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod
    monkeypatch.setattr(sm_mod, "pick", _revienta)
    capturados = _capturador(monkeypatch)
    attack_roll(pj, orco, pj.attacks[0], random.Random(2),
                ctx=_ctx_ataque(pj, orco))
    assert capturados == [RollMode.ADVANTAGE]
    assert not trait.rapid_strike_used


# --- A5: cuerpo de turno extraíble ------------------------------------------


def test_el_cuerpo_de_turno_extraido_no_cambia_run_combat():
    """Equivalencia A5: misma semilla → mismo combate, byte a byte.

    El cuerpo del turno pasó de estar inline en el bucle de rondas a
    ``_turno()`` (mismo orden, mismas llamadas, cero RNG nuevo). El
    snapshot de abajo es el que daba el código ANTES del refactor; si
    este test falla, el orden de RNG cambió.
    """
    habilidades = Abilities(str=16, dex=14, con=16, int=14, wis=12,
                            cha=10)
    camila = PlayerCharacter(name="Camila", max_hp=70, ac=15, level=5,
                             abilities=habilidades,
                             attacks=[Attack("Espada larga", "1d8",
                                             ability="str")])
    apply_fighter(camila, level=5, fighting_style="Archery")
    orco = Monster("Orco", max_hp=60, ac=10, abilities=habilidades)
    res = run_combat([camila, orco], random.Random(42))
    assert res.winner == "PJ"
    assert res.rounds == 6
    assert res.survivors == {"Camila": 70, "Orco": 0}
    assert dict(res.action_uses) == {"Multiattack": 7,
                                     "Oleada de Acción": 1}
    assert res.damage_dealt == {"Camila": 61}
    assert res.damage_received == {"Orco": 61}


# --- A6: Strength Before Death ------------------------------------------------


def test_strength_before_death_encola_un_turno_extra(monkeypatch):
    pj, trait = _samurai(18)
    orco = _enemigo()
    ctx = _ctx(pj, orco)
    pj.hp = 0  # el drop ya ocurrió (como en _salvar_a_cero)
    _si(monkeypatch)
    res = trait.on_reduced_to_zero_hp(
        pj, 10, "slashing", orco, crit=False, ctx=ctx, rng=ctx.rng)
    assert res is None  # queda a 0 PV (versión diferida)
    assert pj.en_pie_pendiente
    assert pj.state.turnos_extra_pendientes == [pj]
    assert pj.alive  # 0 PV pero «en pie»: lo cubre alive
    assert trait.sbd_uses.uses_left == 0
    assert pj.state.reaction_used  # el rasgo gasta la reacción


def test_con_el_pick_no_la_muerte_sigue_normal(monkeypatch):
    pj, trait = _samurai(18)
    orco = _enemigo()
    ctx = _ctx(pj, orco)

    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod
    monkeypatch.setattr(sm_mod, "pick", lambda rng, seq: "no")
    pj.hp = 0  # el drop ya ocurrió
    trait.on_reduced_to_zero_hp(
        pj, 10, "slashing", orco, crit=False, ctx=ctx, rng=ctx.rng)
    assert not pj.en_pie_pendiente
    assert pj.state.turnos_extra_pendientes == []
    assert trait.sbd_uses.uses_left == 1
    assert not pj.alive and not pj.dead  # 0 PV sin flag: no está en pie
    assert not pj.state.reaction_used  # sin elección no gasta reacción


def test_no_es_elegible_sin_nivel_sin_uso_sin_reaccion_sin_contexto(
        monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod

    def _revienta(rng, seq):
        raise AssertionError("elegibilidad sin RNG: no hay pick")

    def _crear(nivel):
        # Crear siempre con pick «sí» (Bonus Proficiency lo usa al
        # aplicar); el pick que revienta se pone DESPUÉS, en cada sonda.
        monkeypatch.setattr(sm_mod, "pick", lambda rng, seq: "sí")
        return _samurai(nivel)

    # Nivel 17: ni se consulta.
    pj, trait = _crear(17)
    orco = _enemigo()
    ctx = _ctx(pj, orco)
    monkeypatch.setattr(sm_mod, "pick", _revienta)
    trait.on_reduced_to_zero_hp(
        pj, 10, "slashing", orco, crit=False, ctx=ctx, rng=ctx.rng)
    assert not pj.en_pie_pendiente and trait.sbd_uses.uses_left == 1

    # Nivel 18 sin usos: gastado el único con una activación previa.
    pj, trait = _crear(18)
    orco = _enemigo()
    ctx = _ctx(pj, orco)
    trait.on_reduced_to_zero_hp(
        pj, 10, "slashing", orco, crit=False, ctx=ctx, rng=ctx.rng)
    monkeypatch.setattr(sm_mod, "pick", _revienta)
    pj.en_pie_pendiente = False
    pj.state.turnos_extra_pendientes.clear()
    trait.on_reduced_to_zero_hp(
        pj, 10, "slashing", orco, crit=False, ctx=ctx, rng=ctx.rng)
    assert not pj.en_pie_pendiente and trait.sbd_uses.uses_left == 0

    # Reacción ya usada / incapacitado: cortan antes del pick.
    for prepara in (
            lambda p, c: setattr(p.state, "reaction_used", True),
            lambda p, c: apply_condition(p, Condition.INCAPACITATED, c),
    ):
        pj, trait = _crear(18)
        orco = _enemigo()
        ctx = _ctx(pj, orco)
        prepara(pj, ctx)
        monkeypatch.setattr(sm_mod, "pick", _revienta)
        trait.on_reduced_to_zero_hp(
            pj, 10, "slashing", orco, crit=False, ctx=ctx, rng=ctx.rng)
        assert not pj.en_pie_pendiente
        assert trait.sbd_uses.uses_left == 1

    # Sin ctx o sin rng: sin contexto no se aplica (y sin RNG).
    pj, trait = _crear(18)
    orco = _enemigo()
    ctx = _ctx(pj, orco)
    monkeypatch.setattr(sm_mod, "pick", _revienta)
    trait.on_reduced_to_zero_hp(
        pj, 10, "slashing", orco, crit=False, ctx=None, rng=ctx.rng)
    trait.on_reduced_to_zero_hp(
        pj, 10, "slashing", orco, crit=False, ctx=ctx, rng=None)
    assert not pj.en_pie_pendiente
    assert trait.sbd_uses.uses_left == 1


def test_el_dano_adicional_remata_a_un_pendiente(monkeypatch):
    from dnd_sim.rules.damage import inflict_damage

    pj, trait = _samurai(18)
    orco = _enemigo()
    ctx = _ctx(pj, orco)
    pj.hp = 0  # el drop ya ocurrió
    _si(monkeypatch)
    trait.on_reduced_to_zero_hp(
        pj, 10, "slashing", orco, crit=False, ctx=ctx, rng=ctx.rng)
    assert pj.en_pie_pendiente
    # Otro golpe con los PV ya a 0: cancela el turno extra y muere.
    inflict_damage(pj, 5, damage_type="bludgeoning", source=orco,
                   ctx=ctx, rng=ctx.rng)
    assert not pj.en_pie_pendiente
    assert pj.state.turnos_extra_pendientes == []
    assert pj.dead and not pj.alive


def test_el_dano_desde_pv_positivos_libera_el_flag_obsoleto(monkeypatch):
    from dnd_sim.rules.damage import inflict_damage

    pj, trait = _samurai(18)
    orco = _enemigo()
    ctx = _ctx(pj, orco)
    pj.hp = 0  # el drop ya ocurrió
    _si(monkeypatch)
    trait.on_reduced_to_zero_hp(
        pj, 10, "slashing", orco, crit=False, ctx=ctx, rng=ctx.rng)
    # Cura entre medias (resolución perezosa): el flag queda obsoleto
    # y el siguiente daño lo limpia sin matar.
    pj.hp = 20
    inflict_damage(pj, 3, damage_type="bludgeoning", source=orco,
                   ctx=ctx, rng=ctx.rng)
    assert not pj.en_pie_pendiente
    assert pj.state.turnos_extra_pendientes == []
    assert not pj.dead and pj.alive and pj.hp == 17


def test_en_run_combat_strength_before_death_da_un_turno_extra(monkeypatch):
    import dnd_sim.engine.combat.encounter as enc
    import dnd_sim.rules.classes.fighter.subclasses.samurai as sm_mod

    habilidades = Abilities(str=16, dex=14, con=16, int=14, wis=12,
                            cha=10)
    camila = PlayerCharacter(
        name="Camila", max_hp=1, ac=10, level=18, abilities=habilidades,
        attacks=[Attack("Espada larga", "1d8", ability="str")])
    apply_fighter(camila, level=18, fighting_style="Archery")
    trait = apply_samurai(camila, level=18)
    for a in camila.attacks:
        a.mastery = ""
    # Nota: run_combat llama a reset() al empezar, que restaura los usos
    # (los `uses_left` manuales no sobreviven); el orco va a 200 PV para
    # que NO muera antes: las 3 cargas de Fighting Spirit cubren las
    # rondas 1-3 con PV temporales y el drop llegue en la 4.
    orco = Monster("Orco", max_hp=200, ac=10, abilities=habilidades,
                   attacks=[Attack("Hacha", "1d8", ability="str")])
    monkeypatch.setattr(sm_mod, "pick", lambda rng, seq: "sí")

    def _orden_fijo(cs, rng):
        for i, c in enumerate(cs):
            c.initiative = 20 - i  # Camila primero; sin fase de guarida
        return list(cs)

    monkeypatch.setattr(enc, "roll_initiative", _orden_fijo)
    # verbose=True: solo así el motor llena el log (sin RNG de más).
    res = run_combat([camila, orco], random.Random(2), verbose=True)
    texto = "\n".join(res.log)
    assert "Strength Before Death" in texto
    # La marca está en el turno del ORCO y, tras ella, el turno extra
    # de Camila ataca antes de morir: los ataques de Camila posteriores
    # a la marca prueban que el turno extra se ejecutó.
    marca = texto.index("Strength Before Death")
    assert "Camila ->" in texto[marca:]
    assert res.survivors.get("Camila", 0) == 0
    assert res.survivors.get("Orco", 0) > 0

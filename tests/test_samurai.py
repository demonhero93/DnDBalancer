"""Tests de la subclase Samurai (XGE, Guerrero).

Solo cubren lo que existe: en A1, las tablas de ``core/classes.py``; en
A2, el esqueleto, el registro y los datos sin efecto; en A3, Fighting
Spirit; en A4, Rapid Strike; en A5, la función de turno reutilizable y
en A6, Strength Before Death.
"""

from __future__ import annotations

import random

import pytest

from dnd_sim import Abilities, Attack, PlayerCharacter, apply_class
from dnd_sim.core.classes import (
    SAMURAI_BONUS_SKILLS,
    fighting_spirit_temp_hp,
    fighting_spirit_uses,
)
from dnd_sim.core.skills import SKILL_ABILITIES
from dnd_sim.engine.combat.encounter import roll_initiative
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import SamuraiFeatures, apply_samurai


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

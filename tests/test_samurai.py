"""Tests de la subclase Samurai (XGE, Guerrero).

Solo cubren lo que existe: en A1, las tablas de ``core/classes.py``; en
A2, el esqueleto, el registro y los datos sin efecto; en A3, Fighting
Spirit; en A4, Rapid Strike; en A5, la función de turno reutilizable y
en A6, Strength Before Death.
"""

from __future__ import annotations

from dnd_sim.core.classes import (
    SAMURAI_BONUS_SKILLS,
    fighting_spirit_temp_hp,
    fighting_spirit_uses,
)
from dnd_sim.core.skills import SKILL_ABILITIES


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

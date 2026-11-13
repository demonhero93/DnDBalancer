"""Tests de la subclase Rune Knight (TCE, PHB 2024).

Solo cubren lo que existe: en A1, las tablas de ``core/classes.py``.
El resto de casillas (esqueleto, runas, reacciones) se añade aquí.
"""

from dnd_sim.core.classes import (
    RUNES,
    giants_might_die_sides,
    giants_might_uses,
    rune_uses,
    runes_known_count,
    runic_shield_uses,
)


# --- A1: tablas --------------------------------------------------------------


def test_tabla_runes_known_count_por_nivel():
    assert runes_known_count(1) == 0
    assert runes_known_count(2) == 0
    assert runes_known_count(3) == 2
    assert runes_known_count(6) == 2
    assert runes_known_count(7) == 3
    assert runes_known_count(9) == 3
    assert runes_known_count(10) == 4
    assert runes_known_count(14) == 4
    assert runes_known_count(15) == 5
    assert runes_known_count(20) == 5


def test_tabla_giants_might_die_sides_por_nivel():
    assert giants_might_die_sides(3) == 6
    assert giants_might_die_sides(9) == 6
    assert giants_might_die_sides(10) == 8
    assert giants_might_die_sides(17) == 8
    assert giants_might_die_sides(18) == 10
    assert giants_might_die_sides(20) == 10


def test_tabla_rune_uses_por_nivel():
    assert rune_uses(3) == 1
    assert rune_uses(14) == 1
    assert rune_uses(15) == 2
    assert rune_uses(20) == 2


def test_tabla_runic_shield_uses_es_el_bonificador_de_competencia():
    assert runic_shield_uses(3) == 2
    assert runic_shield_uses(7) == 3
    assert runic_shield_uses(15) == 5
    assert runic_shield_uses(20) == 6


def test_tabla_giants_might_uses_es_el_bonificador_de_competencia():
    assert giants_might_uses(3) == 2
    assert giants_might_uses(7) == 3
    assert giants_might_uses(15) == 5
    assert giants_might_uses(20) == 6


def test_pool_runas_tiene_las_seis_claves():
    assert RUNES == ("cloud", "fire", "frost", "hill", "stone", "storm")

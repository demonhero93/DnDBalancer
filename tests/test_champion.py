"""Tests de tablas y registro de Champion (Campeón, PHB 2024).

Las tablas viven en A1; el registro y ``apply_champion`` en A2; el
rango crítico ampliado en A3; Remarkable Athlete en A4; Additional
Fighting Style en A5 y Heroic Rally en A6. Los rasgos sin modelo
(Heroic Warrior, Defy Death, movimiento tras crítico) se congelan como
dato sin efecto.
"""

from __future__ import annotations

from dnd_sim.core.classes import (
    champion_crit_threshold,
    heroic_rally_amount,
)


def test_el_rango_critico_de_champion_es_20_19_o_18_segun_el_nivel():
    assert champion_crit_threshold(1) == 20
    assert champion_crit_threshold(2) == 20
    assert champion_crit_threshold(3) == 19
    assert champion_crit_threshold(14) == 19
    assert champion_crit_threshold(15) == 18
    assert champion_crit_threshold(18) == 18
    assert champion_crit_threshold(20) == 18


def test_la_cura_de_heroic_rally_es_5_mas_el_mod_de_con_sin_bajar_de_cero():
    assert heroic_rally_amount(5) == 10
    assert heroic_rally_amount(3) == 8
    assert heroic_rally_amount(0) == 5
    assert heroic_rally_amount(-5) == 0
    assert heroic_rally_amount(-9) == 0

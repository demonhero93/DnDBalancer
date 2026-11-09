"""Subclase Battle Master (Maestro de Batalla, PHB 2024): tablas y registro."""
from __future__ import annotations

from dnd_sim.core.classes import (
    BATTLE_MASTER_MANEUVERS,
    maneuvers_known_count,
    superiority_die_sides,
    superiority_dice_count,
)


def test_tabla_de_dados_de_superioridad_por_nivel():
    esperado = {1: 0, 2: 0, 3: 4, 6: 4, 7: 5, 14: 5, 15: 6, 20: 6}
    assert {lvl: superiority_dice_count(lvl) for lvl in esperado} == esperado


def test_tabla_de_caras_del_dado_por_nivel():
    esperado = {1: 8, 9: 8, 10: 10, 17: 10, 18: 12, 20: 12}
    assert {lvl: superiority_die_sides(lvl) for lvl in esperado} == esperado


def test_tabla_de_maniobras_conocidas_por_nivel():
    esperado = {1: 0, 2: 0, 3: 3, 6: 3, 7: 5, 9: 5, 10: 7, 14: 7,
                15: 9, 20: 9}
    assert {lvl: maneuvers_known_count(lvl) for lvl in esperado} == esperado


def test_el_pool_solo_contiene_las_maniobras_implementadas():
    assert len(BATTLE_MASTER_MANEUVERS) == 11
    assert "Precision Attack" in BATTLE_MASTER_MANEUVERS
    assert "Feinting Attack" in BATTLE_MASTER_MANEUVERS
    assert "Parry" not in BATTLE_MASTER_MANEUVERS  # sesión 2
    assert len(set(BATTLE_MASTER_MANEUVERS)) == len(BATTLE_MASTER_MANEUVERS)

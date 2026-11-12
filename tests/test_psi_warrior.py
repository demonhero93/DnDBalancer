"""Tests de tablas y registro de Psi Warrior (Guerrero Psiónico, PHB 2024).

Las tablas viven en A1; el registro y ``apply_psi_warrior`` en A2;
Psionic Strike en A3; Telekinetic Thrust en A4; Protective Field en A5;
Guarded Mind en A6; Bulwark of Force en A7 y Telekinetic Master en A8.
Los rasgos sin modelo (Telekinetic Movement, Psi-Powered Leap, empuje
de 10 ft, distancias de 30 ft) se congelan como dato sin efecto.
"""

from __future__ import annotations

from dnd_sim.core.classes import (
    bulwark_targets,
    psionic_dice_count,
    psionic_die_sides,
)


def test_los_dados_psionicos_son_doble_del_bonificador_de_competencia():
    assert psionic_dice_count(1) == 0
    assert psionic_dice_count(2) == 0
    assert psionic_dice_count(3) == 4
    assert psionic_dice_count(4) == 4
    assert psionic_dice_count(5) == 6
    assert psionic_dice_count(8) == 6
    assert psionic_dice_count(9) == 8
    assert psionic_dice_count(12) == 8
    assert psionic_dice_count(13) == 10
    assert psionic_dice_count(16) == 10
    assert psionic_dice_count(17) == 12
    assert psionic_dice_count(20) == 12


def test_el_tamano_del_dado_psionico_es_d6_d8_d10_o_d12_segun_el_nivel():
    assert psionic_die_sides(1) == 6
    assert psionic_die_sides(4) == 6
    assert psionic_die_sides(5) == 8
    assert psionic_die_sides(10) == 8
    assert psionic_die_sides(11) == 10
    assert psionic_die_sides(16) == 10
    assert psionic_die_sides(17) == 12
    assert psionic_die_sides(20) == 12


def test_bulwark_targets_es_el_mod_de_int_con_minimo_uno():
    assert bulwark_targets(5) == 5
    assert bulwark_targets(3) == 3
    assert bulwark_targets(1) == 1
    assert bulwark_targets(0) == 1
    assert bulwark_targets(-2) == 1

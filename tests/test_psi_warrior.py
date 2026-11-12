"""Tests de tablas y registro de Psi Warrior (Guerrero Psiónico, PHB 2024).

Las tablas viven en A1; el registro y ``apply_psi_warrior`` en A2;
Psionic Strike en A3; Telekinetic Thrust en A4; Protective Field en A5;
Guarded Mind en A6; Bulwark of Force en A7 y Telekinetic Master en A8.
Los rasgos sin modelo (Telekinetic Movement, Psi-Powered Leap, empuje
de 10 ft, distancias de 30 ft) se congelan como dato sin efecto.
"""

from __future__ import annotations

import random

import pytest

from dnd_sim import Abilities, Attack, PlayerCharacter, apply_class
from dnd_sim.core.classes import (
    bulwark_targets,
    psionic_dice_count,
    psionic_die_sides,
)
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import (
    PsiWarriorFeatures,
    apply_psi_warrior,
)


# --- A1: tablas --------------------------------------------------------------


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


def _trait(pj) -> PsiWarriorFeatures:
    for trait in pj.traits:
        if isinstance(trait, PsiWarriorFeatures):
            return trait
    raise AssertionError("falta PsiWarriorFeatures")


def _psi(level: int = 5, fighting_style: str | None = None,
         **kwargs) -> tuple:
    pj = _pj(level=level)
    apply_fighter(pj, level=level, fighting_style=fighting_style)
    trait = apply_psi_warrior(pj, level=level, **kwargs)
    return pj, trait


def _firmas(pj) -> tuple:
    """(rasgos, acciones, salvaciones, habilidades, CA) para comparar."""
    return (
        [type(t).__name__ for t in pj.traits],
        [type(a).__name__ for a in pj.actions],
        set(pj.save_proficiencies),
        set(pj.skill_proficiencies),
        pj.ac,
    )


def test_registro_psi_warrior_bajo_fighter():
    subclases = CLASSES["fighter"].subclasses
    assert "psi_warrior" in subclases
    sub = subclases["psi_warrior"]
    assert sub.class_name == "fighter"
    assert sub.min_level == 3


def test_apply_class_equivalente_a_apply_psi_warrior(monkeypatch):
    """Misma semilla en el RNG de creación: resultados idénticos."""
    import dnd_sim.rules.classes.fighter.features as fighter_mod

    a, b = _pj(), _pj()
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    apply_class(a, "fighter", "psi_warrior", level=5)
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    apply_fighter(b)
    apply_psi_warrior(b, level=5)
    assert _firmas(a) == _firmas(b)
    assert isinstance(_trait(a), PsiWarriorFeatures)
    assert isinstance(_trait(b), PsiWarriorFeatures)


def test_apply_psi_warrior_sin_clase_guerrero_da_value_error():
    with pytest.raises(ValueError, match="Primero aplica la clase guerrero"):
        apply_psi_warrior(_pj(), level=5)


def test_apply_psi_warrior_por_debajo_del_nivel_3_da_value_error():
    with pytest.raises(ValueError, match=">= 3"):
        apply_class(_pj(level=2), "fighter", "psi_warrior")


def test_los_dados_y_el_tamano_segun_el_nivel_se_rellenan_al_aplicar():
    pj3, t3 = _psi(level=3)
    assert (t3.dados_restantes, t3.dados_lados) == (4, 6)
    pj5, t5 = _psi(level=5)
    assert (t5.dados_restantes, t5.dados_lados) == (6, 8)
    pj11, t11 = _psi(level=11)
    assert (t11.dados_restantes, t11.dados_lados) == (8, 10)
    pj17, t17 = _psi(level=17)
    assert (t17.dados_restantes, t17.dados_lados) == (12, 12)


def test_reset_rellena_la_reserva_completa():
    pj, trait = _psi(level=5)
    trait.dados_restantes = 0
    trait.psionic_strike_used_this_turn = True
    trait.bulwark_uso_gratuito = False
    trait.telekinetic_master_uso_gratuito = False
    trait.bulwark_activo = True
    trait.telekinetic_master_activo = True
    trait.reset()
    assert trait.dados_restantes == psionic_dice_count(5)
    assert trait.psionic_strike_used_this_turn is False
    assert trait.bulwark_uso_gratuito is True
    assert trait.telekinetic_master_uso_gratuito is True
    assert trait.bulwark_activo is False
    assert trait.telekinetic_master_activo is False


def test_telekinetic_movement_y_psi_powered_leap_son_dato_sin_efecto():
    """Sin movimiento ni vuelo en el modelo: ni dados ni RNG."""
    pj, trait = _psi(level=7)
    assert trait.telekinetic_movement is True
    assert trait.psi_powered_leap is True
    # Sin gastar dados ni cambiar la ficha al aplicarlos.
    assert trait.dados_restantes == psionic_dice_count(7)
    assert not hasattr(pj, "speed")


def test_sin_subclase_no_hay_rasgo_ni_datos_de_psi_warrior():
    pj = _pj()
    apply_fighter(pj, level=5, fighting_style="Archery")
    assert not any(isinstance(t, PsiWarriorFeatures) for t in pj.traits)
    # Cero consulta: sin el rasgo nadie tiene la reserva de dados.
    assert not any(hasattr(t, "dados_restantes") for t in pj.traits)

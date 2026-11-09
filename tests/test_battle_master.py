"""Subclase Battle Master (Maestro de Batalla, PHB 2024): tablas y registro."""
from __future__ import annotations

import random

import pytest

from dnd_sim import Abilities, Attack, PlayerCharacter, apply_class
from dnd_sim.core.classes import (
    BATTLE_MASTER_MANEUVERS,
    FIGHTER_SKILLS,
    maneuvers_known_count,
    superiority_die_sides,
    superiority_dice_count,
)
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import (
    BattleMasterFeatures,
    apply_battle_master,
)


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=10, wis=12, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Rolando", max_hp=70, ac=15, level=5, abilities=_abilities(),
        attacks=[Attack("Espada larga", "1d8", ability="str")],
    )
    defaults.update(kwargs)
    return PlayerCharacter(**defaults)


def _firmas(pj) -> tuple:
    """(rasgos, acciones, salvaciones, habilidades, CA) para comparar."""
    return (
        [type(t).__name__ for t in pj.traits],
        [type(a).__name__ for a in pj.actions],
        set(pj.save_proficiencies),
        set(pj.skill_proficiencies),
        pj.ac,
    )


def _trait(pj) -> BattleMasterFeatures:
    for trait in pj.traits:
        if isinstance(trait, BattleMasterFeatures):
            return trait
    raise AssertionError("falta BattleMasterFeatures")


def _bm(level: int = 5, **kwargs) -> tuple:
    pj = _pj(level=level)
    apply_fighter(pj, level=level)
    trait = apply_battle_master(pj, level=level, **kwargs)
    return pj, trait


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


# --- Registro y equivalencia --------------------------------------------------

def test_registro_battle_master_bajo_fighter():
    subclases = CLASSES["fighter"].subclasses
    assert set(subclases) == {"arcane_archer", "battle_master"}
    sub = subclases["battle_master"]
    assert sub.class_name == "fighter"
    assert sub.min_level == 3


def test_apply_class_equivalente_a_apply_battle_master(monkeypatch):
    """Misma semilla en los dos RNG de creación: resultados idénticos."""
    import dnd_sim.rules.classes.fighter.features as fighter_mod
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod

    a = _pj()
    b = _pj()
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    monkeypatch.setattr(bm_mod, "_RNG_CREACION", random.Random(0))
    apply_class(a, "fighter", "battle_master", level=5)
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    monkeypatch.setattr(bm_mod, "_RNG_CREACION", random.Random(0))
    apply_fighter(b, level=5)
    apply_battle_master(b, level=5)
    assert _firmas(a) == _firmas(b)
    assert _trait(a).maneuvers == _trait(b).maneuvers
    assert _trait(a).competencia == _trait(b).competencia


def test_apply_battle_master_exige_la_clase_fighter():
    with pytest.raises(ValueError, match="Primero aplica la clase guerrero"):
        apply_battle_master(_pj())


def test_apply_battle_master_requiere_nivel_3():
    pj = _pj(level=2)
    apply_fighter(pj, level=2)
    with pytest.raises(ValueError, match=">= 3"):
        apply_battle_master(pj, level=2)


def test_registro_de_subclase_requiere_nivel_3():
    with pytest.raises(ValueError, match=">= 3"):
        apply_class(_pj(level=2), "fighter", "battle_master")


# --- Maniobras conocidas -------------------------------------------------------

def test_maniobras_conocidas_segun_nivel():
    casos = {3: 3, 6: 3, 7: 5, 10: 7, 15: 9}
    for nivel, cuenta in casos.items():
        pj = _pj(level=nivel)
        apply_fighter(pj, level=nivel)
        trait = apply_battle_master(pj, level=nivel)
        assert len(trait.maneuvers) == cuenta
        assert len(set(trait.maneuvers)) == cuenta
        assert set(trait.maneuvers) <= set(BATTLE_MASTER_MANEUVERS)


def test_kwarg_de_maniobras_explicitas_valido():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    elegidas = ("Menacing Attack", "Trip Attack", "Precision Attack")
    trait = apply_battle_master(pj, level=3, maneuvers=elegidas)
    assert trait.maneuvers == list(elegidas)


def test_kwarg_de_maniobras_invalidas_da_value_error():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    with pytest.raises(ValueError, match="no es una maniobra de Battle Master"):
        apply_battle_master(
            pj, level=3,
            maneuvers=("Maniobra inventada", "Trip Attack", "Precision Attack"))


def test_kwarg_con_recuento_equivocado_da_value_error():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    with pytest.raises(ValueError, match="se esperaban 3 maniobras"):
        apply_battle_master(pj, level=3, maneuvers=("Trip Attack",))


# --- Student of War y Know Your Enemy -----------------------------------------

def test_student_of_war_anade_una_habilidad_que_no_tenia():
    pj = _pj(level=3)
    apply_fighter(pj, level=3, skills=("athletics",))
    trait = apply_battle_master(pj, level=3)
    assert trait.competencia in FIGHTER_SKILLS
    assert trait.competencia in pj.skill_proficiencies
    assert trait.competencia != "athletics"  # no repite la existente


def test_student_of_war_sin_candidatas_no_cambia_nada():
    pj = _pj(level=3)
    apply_fighter(pj, level=3, skills=tuple(FIGHTER_SKILLS))
    antes = set(pj.skill_proficiencies)
    trait = apply_battle_master(
        pj, level=3, rng=_ExplotaSiUsaRng(),
        maneuvers=("Menacing Attack", "Trip Attack", "Precision Attack"))
    assert trait.competencia == ""
    assert set(pj.skill_proficiencies) == antes


def test_student_of_war_guarda_las_herramientas_como_dato():
    _, trait = _bm(level=3)
    assert trait.herramientas == "herramientas de artesano"


def test_know_your_enemy_es_un_dato_desde_el_nivel_7():
    assert _bm(level=3)[1].know_your_enemy is False
    assert _bm(level=7)[1].know_your_enemy is True


# --- Dados de superioridad -----------------------------------------------------

def test_los_dados_y_su_tamano_siguen_las_tablas():
    assert _bm(level=3)[1].dados_restantes == 4
    assert _bm(level=7)[1].dados_restantes == 5
    assert _bm(level=15)[1].dados_restantes == 6
    assert _bm(level=3)[1].dados_lados == 8
    assert _bm(level=10)[1].dados_lados == 10
    assert _bm(level=18)[1].dados_lados == 12


def test_reset_rellena_los_dados_y_limpia_estado():
    _, trait = _bm(level=3)
    trait.dados_restantes = 0
    trait.relentless_used_this_turn = True
    trait.feinting_pendiente = True
    trait.maniobra_pendiente = "Trip Attack"
    trait.reset()
    assert trait.dados_restantes == 4
    assert trait.relentless_used_this_turn is False
    assert trait.feinting_pendiente is False
    assert trait.maniobra_pendiente is None


def test_on_turn_start_reinicia_sin_rng():
    _, trait = _bm(level=15)
    trait.relentless_used_this_turn = True
    trait.feinting_pendiente = True
    trait.maniobra_pendiente = "Feinting Attack"
    trait.on_turn_start(trait.owner)
    assert trait.relentless_used_this_turn is False
    assert trait.feinting_pendiente is False
    assert trait.maniobra_pendiente is None


class _ExplotaSiUsaRng:
    """Cualquier acceso a RNG hace fallar el test."""

    def __getattr__(self, name: str):
        raise AssertionError(f"RNG no debería usarse: {name}")

"""Clase Fighter (Guerrero): registro, apply y validaciones de base."""
from __future__ import annotations

import pytest

from dnd_sim import Abilities, Attack, PlayerCharacter, apply_class
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import FighterFeatures


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=10, wis=12, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Thor", max_hp=80, ac=12, level=5, abilities=_abilities(),
        attacks=[Attack("Hacha de batalla", "1d12", ability="str")],
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


def test_clase_fighter_esta_registrada_sin_subclases():
    assert "fighter" in CLASSES
    assert CLASSES["fighter"].subclasses == {}


def test_apply_class_fighter_sin_subclase_equivalente_a_apply_fighter():
    a = _pj()
    b = _pj()
    apply_class(a, "fighter")
    apply_fighter(b)
    assert _firmas(a) == _firmas(b)


def test_apply_fighter_anade_el_rasgo_guerrero():
    pj = _pj()
    trait = apply_fighter(pj)
    assert isinstance(trait, FighterFeatures)
    assert trait.level == 5
    assert trait in pj.traits


def test_apply_fighter_asigna_salvaciones_de_fue_y_con():
    pj = _pj()
    apply_fighter(pj)
    assert pj.save_proficiencies == {"str", "con"}


def test_apply_fighter_acepta_las_habilidades_de_la_lista():
    pj = _pj()
    apply_fighter(pj, skills=("Athletics", "perception"))
    assert {"athletics", "perception"} <= pj.skill_proficiencies


def test_apply_fighter_rechaza_habilidades_fuera_de_la_lista():
    with pytest.raises(ValueError, match="no es una habilidad"):
        apply_fighter(_pj(), skills=("stealth",))


def test_subclase_de_fighter_inexistente_da_value_error():
    """La tabla de subclases de fighter está vacía: cualquier clave falla."""
    with pytest.raises(ValueError, match="no es una subclase"):
        apply_class(_pj(), "fighter", "champion")


def test_los_golpes_del_guerrero_suben_en_5_11_y_20():
    from dnd_sim.core.classes import fighter_extra_attacks_for

    esperado = {1: 1, 4: 1, 5: 2, 10: 2, 11: 3, 19: 3, 20: 4}
    assert {lvl: fighter_extra_attacks_for(lvl) for lvl in esperado} == esperado


def test_fighter_features_cubre_los_niveles_1_a_20():
    from dnd_sim.core.classes import FIGHTER_FEATURES

    assert sorted(FIGHTER_FEATURES) == list(range(1, 21))
    assert "Second Wind" in FIGHTER_FEATURES[1]
    assert FIGHTER_FEATURES[20] == ("Three Extra Attacks",)

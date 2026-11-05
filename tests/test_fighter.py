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


class _RngMax:
    """RNG de test: siempre el máximo (1d10 → 10)."""

    def randint(self, a: int, b: int) -> int:
        return b

    def random(self) -> float:
        return 1.0


def _ctx(pj, rng=None):
    from types import SimpleNamespace

    return SimpleNamespace(actor=pj, rng=rng or _RngMax(), round=1,
                           resources=None)


def _second_wind(pj):
    from dnd_sim.rules.classes.fighter import SecondWindAction

    return next(a for a in pj.actions
                if isinstance(a, SecondWindAction))


def _trait(pj):
    from dnd_sim.rules.classes.fighter import FighterFeatures

    return next(t for t in pj.traits if isinstance(t, FighterFeatures))


def _fighter(**kwargs):
    """PJ con la clase aplicada (y sin curar por defecto)."""
    pj = _pj(**kwargs)
    apply_fighter(pj)
    return pj


def test_second_wind_cura_d10_mas_nivel_de_guerrero():
    from dnd_sim.core.classes import second_wind_uses

    pj = _fighter(level=5)
    pj.hp = 40
    accion = _second_wind(pj)
    assert accion.can_use(_ctx(pj))
    accion.execute(_ctx(pj))
    assert pj.hp == 40 + 10 + 5  # 1d10 máx + nivel
    uso = _trait(pj).second_wind_usage
    assert uso.uses_max == second_wind_uses(5) == 3
    assert uso.uses_left == 2


def test_second_wind_no_pasa_de_los_pv_maximos():
    pj = _fighter(level=1)
    pj.hp = 75  # 1d10(10) + 1 = 11 > 5 disponibles
    _second_wind(pj).execute(_ctx(pj))
    assert pj.hp == pj.max_hp


def test_second_wind_usos_por_nivel_son_2_3_y_4():
    from dnd_sim.core.classes import second_wind_uses

    assert [second_wind_uses(l) for l in (1, 3, 4, 9, 10, 20)] == [2, 2, 3, 3, 4, 4]
    for lvl, usos in ((1, 2), (5, 3), (12, 4)):
        pj = _fighter(level=lvl)
        pj.hp = 10
        assert _trait(pj).second_wind_usage.uses_max == usos


def test_second_wind_no_es_elegible_a_pg_completos():
    pj = _fighter(level=3)  # a tope: no se ofrece (sin RNG)
    assert not _second_wind(pj).can_use(_ctx(pj))


def test_second_wind_no_es_elegible_sin_usos():
    pj = _fighter(level=1)
    pj.hp = 40
    uso = _trait(pj).second_wind_usage
    uso.spend()
    uso.spend()
    assert not _second_wind(pj).can_use(_ctx(pj))

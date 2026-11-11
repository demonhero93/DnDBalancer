"""Tests de tablas y registro de Champion (Campeón, PHB 2024).

Las tablas viven en A1; el registro y ``apply_champion`` en A2; el
rango crítico ampliado en A3; Remarkable Athlete en A4; Additional
Fighting Style en A5 y Heroic Rally en A6. Los rasgos sin modelo
(Heroic Warrior, Defy Death, movimiento tras crítico) se congelan como
dato sin efecto.
"""

from __future__ import annotations

import random

import pytest

from dnd_sim import Abilities, Attack, PlayerCharacter, apply_class
from dnd_sim.core.classes import (
    champion_crit_threshold,
    heroic_rally_amount,
)
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import ChampionFeatures, apply_champion

# --- A1: tablas --------------------------------------------------------------


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


# --- A2: esqueleto, registro y datos sin efecto ------------------------------

def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=10, wis=12, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Camila", max_hp=70, ac=15, level=5, abilities=_abilities(),
        attacks=[Attack("Espada larga", "1d8", ability="str")],
    )
    defaults.update(kwargs)
    return PlayerCharacter(**defaults)


def _trait(pj) -> ChampionFeatures:
    for trait in pj.traits:
        if isinstance(trait, ChampionFeatures):
            return trait
    raise AssertionError("falta ChampionFeatures")


def _champion(level: int = 5, fighting_style: str | None = None,
              **kwargs) -> tuple:
    pj = _pj(level=level)
    apply_fighter(pj, level=level, fighting_style=fighting_style)
    trait = apply_champion(pj, level=level, **kwargs)
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


def test_registro_champion_bajo_fighter():
    subclases = CLASSES["fighter"].subclasses
    assert "champion" in subclases
    sub = subclases["champion"]
    assert sub.class_name == "fighter"
    assert sub.min_level == 3


def test_apply_class_equivalente_a_apply_champion(monkeypatch):
    """Misma semilla en los dos RNG de creación: resultados idénticos."""
    import dnd_sim.rules.classes.fighter.features as fighter_mod
    import dnd_sim.rules.classes.fighter.subclasses.champion as champ_mod

    a, b = _pj(), _pj()
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    monkeypatch.setattr(champ_mod, "_RNG_CREACION", random.Random(0))
    apply_class(a, "fighter", "champion", level=5)
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    monkeypatch.setattr(champ_mod, "_RNG_CREACION", random.Random(0))
    apply_fighter(b)
    apply_champion(b, level=5)
    assert _firmas(a) == _firmas(b)
    assert isinstance(_trait(a), ChampionFeatures)
    assert isinstance(_trait(b), ChampionFeatures)


def test_apply_champion_sin_clase_guerrero_da_value_error():
    with pytest.raises(ValueError, match="Primero aplica la clase guerrero"):
        apply_champion(_pj(), level=5)


def test_apply_champion_por_debajo_del_nivel_3_da_value_error():
    with pytest.raises(ValueError, match=">= 3"):
        apply_class(_pj(level=2), "fighter", "champion")


def test_heroic_warrior_es_dato_sin_efecto():
    """Sin Inspiración Heroica en el modelo: solo el dato congelado."""
    pj, trait = _champion(level=10)
    assert trait.heroic_warrior is True
    # Ni salvaciones, habilidades ni CA cambian; no hay inspiración.
    assert not hasattr(pj, "inspiration")


def test_defy_death_es_dato_sin_efecto():
    """Sin salvaciones de muerte en el modelo: solo el dato congelado."""
    pj, trait = _champion(level=18)
    assert trait.defy_death is True
    # Un PJ a 0 PG muere o queda fuera: no existe el atributo.
    assert not hasattr(pj, "death_saves")


def test_sin_subclase_no_hay_rasgo_ni_datos_de_champion():
    pj = _pj()
    apply_fighter(pj, level=5)
    assert not any(isinstance(t, ChampionFeatures) for t in pj.traits)
    # Cero consulta: sin el rasgo nadie lleva los datos congelados.
    assert not any(hasattr(t, "heroic_warrior") for t in pj.traits)
    assert not any(hasattr(t, "defy_death") for t in pj.traits)

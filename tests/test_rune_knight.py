"""Tests de la subclase Rune Knight (TCE, PHB 2024).

Solo cubren lo que existe: en A1, las tablas de ``core/classes.py``;
en A2, el esqueleto, el registro y los datos sin efecto. El resto de
casillas (runas, reacciones, ganchos de turno) se añade aquí.
"""

from __future__ import annotations

import random

import pytest

from dnd_sim import Abilities, Attack, PlayerCharacter, apply_class
from dnd_sim.core.classes import (
    RUNES,
    giants_might_die_sides,
    giants_might_uses,
    rune_uses,
    runes_known_count,
    runic_shield_uses,
)
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import (
    RuneKnightFeatures,
    apply_champion,
    apply_rune_knight,
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


def _rune(pj) -> RuneKnightFeatures:
    for trait in pj.traits:
        if isinstance(trait, RuneKnightFeatures):
            return trait
    raise AssertionError("el PJ no tiene RuneKnightFeatures")


def test_rune_knight_registrada_en_la_tabla_de_subclases():
    assert "rune_knight" in CLASSES["fighter"].subclasses
    sub = CLASSES["fighter"].subclasses["rune_knight"]
    assert sub.name == "Rune Knight"
    assert sub.class_name == "fighter"
    assert sub.min_level == 3


def test_apply_class_y_apply_rune_knight_son_equivalentes(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.rune_knight as rk_mod

    a = _pj(level=3)
    apply_fighter(a, level=3, fighting_style="Archery")
    monkeypatch.setattr(rk_mod, "_RNG_CREACION", random.Random(0))
    t1 = apply_rune_knight(a, level=3)

    b = _pj(level=3)
    apply_fighter(b, level=3, fighting_style="Archery")
    monkeypatch.setattr(rk_mod, "_RNG_CREACION", random.Random(0))
    apply_class(b, "fighter", "rune_knight", level=3,
                fighting_style="Archery")
    t2 = _rune(b)

    assert t1.runas == t2.runas
    assert t1.usos_runa == t2.usos_runa
    assert t1.giants_might_usos == t2.giants_might_usos
    assert t1.runic_shield_usos == t2.runic_shield_usos


def test_aplicar_sin_clase_guerrero_da_error():
    pj = _pj()
    with pytest.raises(ValueError, match="apply_fighter"):
        apply_rune_knight(pj, level=3)


def test_aplicar_con_nivel_inferior_a_tres_da_error():
    pj = _pj()
    apply_fighter(pj, level=1, fighting_style="Archery")
    with pytest.raises(ValueError, match="nivel >= 3"):
        apply_rune_knight(pj, level=2)


def test_runas_conocidas_segun_el_nivel():
    for level, n in ((3, 2), (7, 3), (10, 4), (15, 5)):
        pj = _pj(level=level)
        apply_fighter(pj, level=level, fighting_style="Archery")
        trait = apply_rune_knight(pj, level=level)
        assert len(trait.runas) == n
        assert set(trait.runas) <= set(RUNES)
        assert set(trait.usos_runa) == set(trait.runas)
        assert all(trait.usos_runa[r] == rune_uses(level)
                   for r in trait.runas)


def test_karg_runas_invalido_da_error():
    pj = _pj()
    apply_fighter(pj, level=3, fighting_style="Archery")
    with pytest.raises(ValueError, match="no es una runa"):
        apply_rune_knight(pj, level=3, runes=("fire", "volcano"))
    with pytest.raises(ValueError, match="se esperaban 2"):
        apply_rune_knight(pj, level=3, runes=("fire",))


def test_pasivos_y_bonus_proficiencies_congelados_sin_efecto():
    pj = _pj(level=10)
    apply_fighter(pj, level=10, fighting_style="Archery")
    antes = set(pj.skill_proficiencies or set())
    trait = apply_rune_knight(
        pj, level=10, runes=("cloud", "fire", "frost", "hill"))
    # Datos sin efecto: ni herramientas ni idiomas se añaden.
    assert trait.pasivos_runas is True
    assert trait.bonus_proficiencies is True
    assert set(pj.skill_proficiencies or set()) == antes


def test_sin_la_subclase_rune_knight_no_se_consume_rng(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("sin la subclase no se consulta el módulo")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight as rk_mod

    monkeypatch.setattr(rk_mod, "sample", _revienta)
    pj = _pj(level=3)
    apply_fighter(pj, level=3, fighting_style="Archery")
    apply_champion(pj, level=3)
    otro = _pj(level=3)
    apply_class(otro, "fighter", level=3, fighting_style="Archery")

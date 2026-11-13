"""Tests de la subclase Rune Knight (TCE, PHB 2024).

Solo cubren lo que existe: en A1, las tablas de ``core/classes.py``; en
A2, el esqueleto, el registro y los datos sin efecto; en A3, la consulta
perezosa ``modificar_salvacion``/``modificar_prueba``. El resto de
casillas (runas, reacciones, ganchos de turno) se añade aquí.
"""

from __future__ import annotations

import random
from types import SimpleNamespace

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
from dnd_sim.core.dice import RollMode
from dnd_sim.rules.checks import ability_check, ability_check_bonus, skill_check
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import (
    RuneKnightFeatures,
    apply_champion,
    apply_rune_knight,
)
from dnd_sim.rules.conditions import Condition, apply_condition
from dnd_sim.rules.saves import saving_throw


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


# --- A3: consulta perezosa de salvaciones y pruebas --------------------------


def _ctx(*combatantes) -> SimpleNamespace:
    """Contexto mínimo con ``combatants`` para la consulta."""
    return SimpleNamespace(round=1, actor=combatantes[0],
                           rng=random.Random(1),
                           combatants=list(combatantes), log=[])


class _EspiaSalvacion:
    """Rasgo espía con el método ``modificar_salvacion`` (A3)."""

    def __init__(self, ventaja: bool = True, desventaja: bool = False,
                 bonus: int = 0) -> None:
        self.ventaja = ventaja
        self.desventaja = desventaja
        self.bonus = bonus
        self.llamadas: list = []

    def modificar_salvacion(self, habilidad, sujeto, ctx):
        self.llamadas.append((habilidad, sujeto, ctx))
        return self.ventaja, self.desventaja, self.bonus


class _EspiaPrueba:
    """Rasgo espía con el método ``modificar_prueba`` (A3)."""

    def __init__(self, ventaja: bool = True, desventaja: bool = False,
                 bonus: int = 0) -> None:
        self.ventaja = ventaja
        self.desventaja = desventaja
        self.bonus = bonus
        self.llamadas: list = []

    def modificar_prueba(self, habilidad, sujeto, ctx):
        self.llamadas.append((habilidad, sujeto, ctx))
        return self.ventaja, self.desventaja, self.bonus


def test_sin_rasgos_que_definan_la_consulta_no_consume_rng():
    pj = _pj()
    ctx = _ctx(pj)
    rng1 = random.Random(7)
    sr1 = saving_throw(pj, "str", 12, rng1, ctx=ctx)
    rng2 = random.Random(7)
    sr2 = saving_throw(pj, "str", 12, rng2, ctx=ctx)
    assert sr1 == sr2
    assert rng1.getstate() == rng2.getstate()
    # Sin ``ctx`` la consulta no se hace ni siquiera con un rasgo espía.
    espia = _EspiaSalvacion()
    pj.traits.append(espia)
    saving_throw(pj, "str", 12, random.Random(3), ctx=None)
    assert espia.llamadas == []


def test_un_rasgo_espia_de_salvacion_confirma_la_consulta():
    pj = _pj()
    espia = _EspiaSalvacion()
    pj.traits.append(espia)
    ctx = _ctx(pj)
    sr = saving_throw(pj, "str", 20, random.Random(1), ctx=ctx)
    assert espia.llamadas == [("str", pj, ctx)]
    assert sr.mode == RollMode.ADVANTAGE


def test_ventaja_y_desventaja_se_anulan_en_la_consulta_de_salvacion():
    pj = _pj()
    pj.traits.append(_EspiaSalvacion(ventaja=True, desventaja=True))
    sr = saving_throw(pj, "str", 12, random.Random(1), ctx=_ctx(pj))
    assert sr.mode == RollMode.NORMAL


def test_el_bonificador_de_la_consulta_se_suma_a_la_salvacion(monkeypatch):
    import dnd_sim.rules.saves as saves_mod

    def _d20_fijo(rng, mode=None):
        return SimpleNamespace(value=10, rolls=[10])

    monkeypatch.setattr(saves_mod, "roll_d20", _d20_fijo)
    pj = _pj()
    pj.traits.append(_EspiaSalvacion(ventaja=False, bonus=5))
    sr = saving_throw(pj, "str", 12, random.Random(1), ctx=_ctx(pj))
    assert sr.total == 10 + pj.saving_throw_bonus("str") + 5


def test_un_rasgo_espia_de_prueba_confirma_la_consulta():
    pj = _pj()
    espia = _EspiaPrueba()
    pj.traits.append(espia)
    ctx = _ctx(pj)
    res = ability_check(pj, "con", 20, random.Random(1), ctx=ctx)
    assert espia.llamadas == [("con", pj, ctx)]
    assert res.mode == RollMode.ADVANTAGE


def test_ventaja_y_desventaja_se_anulan_en_la_consulta_de_prueba():
    pj = _pj()
    pj.traits.append(_EspiaPrueba(ventaja=True, desventaja=True))
    res = ability_check(pj, "str", 12, random.Random(1), ctx=_ctx(pj))
    assert res.mode == RollMode.NORMAL


def test_el_bonificador_de_la_consulta_se_suma_a_la_prueba(monkeypatch):
    import dnd_sim.rules.checks as checks_mod

    def _d20_fijo(rng, mode=None):
        return SimpleNamespace(value=10, rolls=[10])

    monkeypatch.setattr(checks_mod, "roll_d20", _d20_fijo)
    pj = _pj()
    pj.traits.append(_EspiaPrueba(ventaja=False, bonus=4))
    res = ability_check(pj, "str", 12, random.Random(1), ctx=_ctx(pj))
    assert res.total == 10 + ability_check_bonus(pj, "str") + 4


def test_en_pruebas_de_habilidad_se_pasa_la_caracteristica_efectiva():
    pj = _pj()
    espia = _EspiaPrueba()
    pj.traits.append(espia)
    skill_check(pj, "athletics", 20, random.Random(1), ctx=_ctx(pj))
    assert espia.llamadas[-1][0] == "str"


def test_la_consulta_mira_a_los_otros_vivos_y_no_a_muertos_o_incapacitados():
    pj = _pj()
    vivo, muerto, incapaz = _pj(), _pj(), _pj()
    muerto.hp = 0
    ctx0 = _ctx(pj)
    apply_condition(incapaz, Condition.INCAPACITATED, ctx0)
    espia_vivo = _EspiaSalvacion(ventaja=True)
    # Si muerto o incapaz se consultaran, su (ventaja y desventaja) anularía
    # la ventaja del espía vivo y el modo final sería NORMAL.
    espia_muerto = _EspiaSalvacion(ventaja=True, desventaja=True)
    espia_incapaz = _EspiaSalvacion(ventaja=True, desventaja=True)
    vivo.traits.append(espia_vivo)
    muerto.traits.append(espia_muerto)
    incapaz.traits.append(espia_incapaz)
    ctx = _ctx(pj, vivo, muerto, incapaz)
    sr = saving_throw(pj, "str", 12, random.Random(1), ctx=ctx)
    assert espia_vivo.llamadas
    assert espia_muerto.llamadas == []
    assert espia_incapaz.llamadas == []
    assert sr.mode == RollMode.ADVANTAGE

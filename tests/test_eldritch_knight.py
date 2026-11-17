"""Tests de la subclase Eldritch Knight (Caballero Sobrenatural, PHB 2024).

Solo cubren lo que existe: en A1, las tablas de ``core/classes.py``; en
A2, el esqueleto, el registro, la equivalencia de vías y los datos sin
efecto; el resto de pasos se van añadiendo aquí.
"""

from __future__ import annotations

import json
from pathlib import Path

from dnd_sim import Abilities, Attack, PlayerCharacter, apply_class
from dnd_sim.core.classes import (
    eldritch_knight_cantrips,
    eldritch_knight_prepared,
)
from dnd_sim.data.spell_parser import parse_spell
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import (
    ELDRITCH_KNIGHT_SPELLS,
    EldritchKnightFeatures,
    apply_eldritch_knight,
)
from dnd_sim.rules.spells import Spellcasting, hechizo_soportado

SPELLS = Path(__file__).parent / "fixtures" / "spells"


# --- A1: tablas --------------------------------------------------------------


def test_la_tabla_de_hechizos_preparados_coincide_con_el_phb():
    esperado = {
        3: 3, 4: 4, 5: 4, 6: 4, 7: 5, 8: 6, 9: 6, 10: 7, 11: 8,
        12: 8, 13: 9, 14: 10, 15: 10, 16: 11, 17: 11, 18: 11,
        19: 12, 20: 13,
    }
    for nivel, valor in esperado.items():
        assert eldritch_knight_prepared(nivel) == valor, nivel


def test_eldritch_knight_prepared_es_cero_por_debajo_del_nivel_3():
    assert eldritch_knight_prepared(1) == 0
    assert eldritch_knight_prepared(2) == 0


def test_eldritch_knight_cantrips_es_cero_dos_o_tres():
    assert eldritch_knight_cantrips(1) == 0
    assert eldritch_knight_cantrips(2) == 0
    assert eldritch_knight_cantrips(3) == 2
    assert eldritch_knight_cantrips(9) == 2
    assert eldritch_knight_cantrips(10) == 3
    assert eldritch_knight_cantrips(20) == 3


# --- A2: esqueleto, registro y vías ------------------------------------------ #


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Aldric", max_hp=30, ac=16, level=3,
        abilities=Abilities(str=16, dex=14, con=16, int=16, wis=12, cha=10),
        attacks=[Attack("Espada larga", "1d8", ability="str")],
    )
    defaults.update(kwargs)
    return PlayerCharacter(**defaults)


def _lista():
    """Pool de prueba: todas las fixtures soportadas por el motor (sin red)."""
    out = []
    for ruta in sorted(SPELLS.glob("*.json")):
        spell = parse_spell(json.loads(ruta.read_text(encoding="utf-8")),
                            "EK", Spellcasting(level=5))
        if spell is not None and hechizo_soportado(spell):
            out.append(spell)
    return out


def test_eldritch_knight_esta_registrado_con_tercio_int_y_lista_wizard():
    sub = CLASSES["fighter"].subclasses.get("eldritch_knight")
    assert sub is not None
    assert sub.class_name == "fighter"
    assert sub.min_level == 3
    assert sub.spellcasting is ELDRITCH_KNIGHT_SPELLS
    assert ELDRITCH_KNIGHT_SPELLS.progresion == "third"
    assert ELDRITCH_KNIGHT_SPELLS.caracteristica == "int"
    assert ELDRITCH_KNIGHT_SPELLS.lista_clase == "wizard"
    assert ELDRITCH_KNIGHT_SPELLS.escuelas is None
    from dnd_sim import EldritchKnightFeatures as Facade
    assert Facade is EldritchKnightFeatures


def test_apply_class_y_apply_eldritch_knight_construyen_el_mismo_lanzador():
    lista = _lista()
    pj1 = _pj()
    apply_class(pj1, "fighter", "eldritch_knight", level=3, lista=lista)
    pj2 = _pj()
    apply_fighter(pj2, level=3)
    apply_eldritch_knight(pj2, level=3, lista=lista)
    assert pj1.spell_slots.maximos == pj2.spell_slots.maximos == (2,)
    assert pj1.spellcasting_pc.trucos == pj2.spellcasting_pc.trucos
    assert pj1.spellcasting_pc.preparados == pj2.spellcasting_pc.preparados
    assert len(pj1.spellcasting_pc.preparados) == 3
    assert len(pj1.spellcasting_pc.trucos) == 2
    assert any(isinstance(t, EldritchKnightFeatures) for t in pj1.traits)
    assert any(isinstance(t, EldritchKnightFeatures) for t in pj2.traits)
    assert len(pj1.actions) == len(pj2.actions)


def test_aplicar_sin_guerrero_o_con_nivel_inferior_a_3_es_error():
    import pytest

    with pytest.raises(ValueError):
        apply_eldritch_knight(_pj(), level=3, lista=_lista())
    pj = _pj()
    apply_fighter(pj, level=3)
    with pytest.raises(ValueError):
        apply_eldritch_knight(pj, level=2, lista=_lista())


def test_espacios_y_conteos_de_hechizos_por_nivel_3_7_y_19():
    for nivel, espacios, preparados, trucos in (
        (3, (2,), 3, 2),
        (7, (4, 2), 5, 2),
        (19, (4, 3, 3, 1), 12, 3),
    ):
        pj = _pj(level=nivel)
        apply_fighter(pj, level=nivel)
        apply_eldritch_knight(pj, level=nivel, lista=_lista())
        assert pj.spell_slots.maximos == espacios, nivel
        assert len(pj.spellcasting_pc.preparados) == preparados, nivel
        assert len(pj.spellcasting_pc.trucos) == trucos, nivel


def test_kwargs_de_preparacion_invalidos_son_error():
    import pytest

    pj = _pj()
    apply_fighter(pj, level=3)
    with pytest.raises(ValueError):
        # Truco: magic-missile no está en el pool de trucos.
        apply_eldritch_knight(pj, level=3, lista=_lista(),
                              cantrips=["magic-missile"])
    pj2 = _pj()
    apply_fighter(pj2, level=3)
    with pytest.raises(ValueError):
        # Nivel 3 solo tiene espacio de nivel 1: fireball es inalcanzable.
        apply_eldritch_knight(pj2, level=3, lista=_lista(),
                              spells=["fireball"])


def test_war_bond_y_arcane_charge_son_datos_sin_efecto():
    pj = _pj()
    apply_fighter(pj, level=3)
    trait = apply_eldritch_knight(pj, level=3, lista=_lista())
    assert trait.war_bond is True
    assert trait.arcane_charge is True


def test_sin_la_subclase_no_hay_espacios_ni_acciones_de_hechizo():
    pj = _pj()
    apply_fighter(pj, level=3)
    assert pj.spell_slots is None
    assert getattr(pj, "spellcasting_pc", None) is None
    assert not any(isinstance(t, EldritchKnightFeatures) for t in pj.traits)
    assert not any(getattr(a, "es_accion_magia", False) for a in pj.actions)

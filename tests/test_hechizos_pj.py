"""Hechizos de PJ: espacios, preparación y lanzamiento (sesión 1).

Los datos de hechizos salen de fixtures JSON (sin red); los PJ de prueba
se construyen a mano. Una clase falsa SOLO de test ejercita el registro.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import pytest

from dnd_sim.core.spellcasting import (
    FULL_SLOTS, HALF_SLOTS, THIRD_SLOTS, SpellcastingDef, spell_slots_for,
)

FIXTURES = Path(__file__).parent / "fixtures"
SPELLS = FIXTURES / "spells"


# --- A1: tablas de espacios ------------------------------------------------ #

def test_la_tabla_de_lanzador_total_coincide_con_el_phb():
    assert FULL_SLOTS[1] == (2,)
    assert FULL_SLOTS[3] == (4, 2)
    assert FULL_SLOTS[7] == (4, 3, 3, 1)
    assert FULL_SLOTS[17] == (4, 3, 3, 3, 2, 1, 1, 1, 1)
    assert FULL_SLOTS[18] == (4, 3, 3, 3, 3, 1, 1, 1, 1)
    assert FULL_SLOTS[20] == (4, 3, 3, 3, 3, 2, 2, 1, 1)
    assert len(FULL_SLOTS) == 20


def test_la_tabla_de_semilanzador_coincide_con_el_phb():
    assert HALF_SLOTS[1] == (2,)
    assert HALF_SLOTS[5] == (4, 2)
    assert HALF_SLOTS[9] == (4, 3, 2)
    assert HALF_SLOTS[13] == (4, 3, 3, 1)
    assert HALF_SLOTS[20] == (4, 3, 3, 3, 2)
    assert len(HALF_SLOTS) == 20


def test_la_tabla_de_tercio_empieza_en_el_nivel_3():
    assert 1 not in THIRD_SLOTS
    assert 2 not in THIRD_SLOTS
    assert THIRD_SLOTS[3] == (2,)
    assert THIRD_SLOTS[7] == (4, 2)
    assert THIRD_SLOTS[16] == (4, 3, 3)
    assert THIRD_SLOTS[20] == (4, 3, 3, 1)
    assert len(THIRD_SLOTS) == 18


def test_spell_slots_for_devuelve_la_tupla_sin_ceros_finales():
    assert spell_slots_for("full", 3) == (4, 2)
    assert spell_slots_for("half", 5) == (4, 2)
    assert spell_slots_for("third", 19) == (4, 3, 3, 1)


def test_spell_slots_for_sin_espacios_por_debajo_del_minimo():
    assert spell_slots_for("third", 1) == ()
    assert spell_slots_for("third", 2) == ()


def test_spell_slots_for_con_progresión_desconocida_es_un_value_error():
    with pytest.raises(ValueError):
        spell_slots_for("pact", 5)


def test_spellcastingdef_valida_la_progresión_y_expone_espacios():
    d = SpellcastingDef(progresion="THIRD", caracteristica="Int",
                        lista_clase="wizard", min_level=3)
    assert d.progresion == "third"
    assert d.caracteristica == "int"
    assert d.escuelas is None
    assert d.espacios(2) == ()          # por debajo de min_level
    assert d.espacios(3) == (2,)
    with pytest.raises(ValueError):
        SpellcastingDef(progresion="pact", caracteristica="cha",
                        lista_clase="warlock")

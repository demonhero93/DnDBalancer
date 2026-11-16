"""Tests de la subclase Eldritch Knight (Caballero Sobrenatural, PHB 2024).

Solo cubren lo que existe: en A1, las tablas de ``core/classes.py``; el
resto de pasos se van añadiendo aquí.
"""

from __future__ import annotations

from dnd_sim.core.classes import (
    eldritch_knight_cantrips,
    eldritch_knight_prepared,
)


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

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
    FULL_SLOTS, HALF_SLOTS, THIRD_SLOTS, SpellSlots, SpellcastingDef,
    spell_slots_for,
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


# --- A2: SpellSlots en el combatiente --------------------------------------- #

def test_un_truco_no_gasta_espacio_y_un_hechizo_de_nivel_1_si():
    slots = SpellSlots((4, 2))
    assert slots.can_cast(0)             # truco: siempre
    slots.spend(1)
    assert slots.actuales == [3, 2]
    assert slots.can_cast(0)             # seguir lanzando trucos: sin gasto
    assert slots.can_cast(1)


def test_al_agotar_un_nivel_las_ofertas_superiores_siguen_disponibles():
    slots = SpellSlots((4, 3, 2))
    for _ in range(4):
        slots.spend(1)
    assert slots.actuales == [0, 3, 2]
    # Sobrecarga: un hechizo de nivel 1 sigue siendo lanzable con un
    # espacio de nivel >= 1, y la oferta son los niveles superiores.
    assert slots.can_cast(1)
    assert slots.niveles_disponibles(1) == [2, 3]
    for _ in range(3):
        slots.spend(2)
    for _ in range(2):
        slots.spend(3)
    assert not slots.can_cast(1)
    assert slots.niveles_disponibles(1) == []


def test_gastar_un_espacio_agotado_es_un_value_error():
    slots = SpellSlots((1,))
    slots.spend(1)
    with pytest.raises(ValueError):
        slots.spend(1)


def test_reset_rellena_los_espacios_igual_que_al_crearlos():
    slots = SpellSlots((4, 2))
    slots.spend(1)
    slots.spend(1)
    slots.spend(2)
    slots.reset()
    assert slots.actuales == [4, 2]


def test_un_combatiente_sin_lanzamiento_no_tiene_espacios_y_reset_es_inofensivo():
    from dnd_sim import Abilities, Combatant
    c = Combatant(name="Pij", max_hp=10, ac=10, abilities=Abilities(),
                  attacks=[])
    assert c.spell_slots is None
    c.reset()                            # no debe fallar ni tocar nada


def test_combatant_reset_restaura_los_espacios_del_pj_lanzador():
    from dnd_sim import Abilities, Combatant
    c = Combatant(name="Mago", max_hp=10, ac=10, abilities=Abilities(),
                  attacks=[])
    c.spell_slots = SpellSlots((4, 2))
    c.spell_slots.spend(1)
    c.hp = 3
    c.reset()
    assert c.spell_slots.actuales == [4, 2]
    assert c.hp == 10


# --- A3: lista de hechizos de clase (capa data) ----------------------------- #

def _get_spell_fixture(index: str) -> dict:
    """Cargador de hechizos sin red: lee la fixture JSON del índice."""
    ruta = SPELLS / f"{index}.json"
    if not ruta.exists():
        raise FileNotFoundError(index)
    return json.loads(ruta.read_text(encoding="utf-8"))


def test_la_lista_de_clase_se_parsea_con_nivel_y_escuela():
    from dnd_sim.data.class_spells import load_class_spell_list
    lista = load_class_spell_list("wizard", cache_dir=FIXTURES / "classes",
                                  get_spell=_get_spell_fixture)
    por_indice = {s.index: s for s in lista}
    fireball = por_indice["fireball"]
    assert (fireball.level, fireball.school) == (3, "evocation")
    assert por_indice["ray-of-frost"].level == 0
    assert por_indice["hold-person"].level == 2
    # No modelados (utilidad, PV temporales) y el inexistente: fuera.
    for fuera in ("shield", "mage-hand", "jump", "false-life",
                  "nonexistent-spell"):
        assert fuera not in por_indice


def test_un_hechizo_que_no_existe_se_omite_sin_romper_la_lista():
    from dnd_sim.data.class_spells import load_class_spell_list

    def _get(index: str) -> dict:
        if index == "fireball":
            raise FileNotFoundError(index)
        return _get_spell_fixture(index)

    lista = load_class_spell_list("wizard", cache_dir=FIXTURES / "classes",
                                  get_spell=_get)
    indices = {s.index for s in lista}
    assert "fireball" not in indices
    assert "magic-missile" in indices


def test_la_lista_se_guarda_en_cache_y_la_segunda_vez_no_toca_la_red(
        tmp_path, monkeypatch):
    import urllib.request
    from dnd_sim.data.class_spells import load_class_spell_list

    fixture = json.loads(
        (FIXTURES / "classes" / "wizard.json").read_text(
            encoding="utf-8"))

    class _Respuesta:
        def __init__(self, data):
            self._d = data

        def read(self):
            return json.dumps(self._d).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    llamadas: list[str] = []

    def _falsa_red(url, timeout=None):
        llamadas.append(str(url))
        return _Respuesta(fixture)

    monkeypatch.setattr(urllib.request, "urlopen", _falsa_red)
    lista1 = load_class_spell_list("wizard", cache_dir=tmp_path,
                                   get_spell=_get_spell_fixture)
    assert llamadas and (tmp_path / "wizard.json").exists()

    def _sin_red(*args, **kwargs):
        raise AssertionError("no debe tocar la red")

    monkeypatch.setattr(urllib.request, "urlopen", _sin_red)
    lista2 = load_class_spell_list("wizard", cache_dir=tmp_path,
                                   get_spell=_get_spell_fixture)
    assert [s.index for s in lista1] == [s.index for s in lista2]

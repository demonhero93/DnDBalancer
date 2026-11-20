"""Turn Resistance del lich (ventaja en las salvaciones de conversión).

El rasgo solo sabe una cosa: «advantage on saving throws against any effect
that turns undead». Por eso la salvación llega marcada con ``kind="turn"``,
que es como se distingue ese efecto de cualquier otro. Hoy ningún efecto del
motor convierte (# TODO: Turn Undead), así que el rasgo está cableado de
punta a punta y probado, pero en reposo.
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, PlayerCharacter
from dnd_sim.data.loader import load_monster
from dnd_sim.core.dice import RollMode
from dnd_sim.rules.roll_modifiers import save_modifiers
from dnd_sim.rules.saves import saving_throw

FIXTURES = Path(__file__).parents[2] / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _datos(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _lich(monkeypatch):
    data = _datos("lich")
    # El fixture 2024 ya no trae «Turn Resistance»: se añade data sintética
    # (SRD 2014) para seguir cubriendo el rasgo de punta a punta.
    data["special_abilities"] = list(data.get("special_abilities") or []) + [{
        "name": "Turn Resistance",
        "desc": ("The lich has advantage on saving throws against any effect "
                 "that turns undead."),
        "damage": [],
    }]
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("lich")


def _pj() -> PlayerCharacter:
    return PlayerCharacter(
        name="Clerigo", max_hp=30, ac=15, proficiency=2,
        abilities=Abilities(str=12, dex=12, con=12, int=10, wis=16, cha=14),
        attacks=[],
    )


# --- Carga de la ficha ------------------------------------------------------ #

def test_el_lich_carga_su_turn_resistance(monkeypatch):
    lich = _lich(monkeypatch)
    # Spellcasting, Legendary Resistance y Rejuvenation ya los gestionan
    # otros parsers: solo Turn Resistance es un rasgo para este módulo.
    assert [type(t).__name__ for t in lich.traits] == ["TurnResistance"]
    assert lich.traits[0].name == "Turn Resistance"
    assert "turns" in lich.traits[0].desc


# --- Reglas ----------------------------------------------------------------- #

def test_da_ventaja_si_la_salvacion_es_de_conversion(monkeypatch):
    lich = _lich(monkeypatch)
    mods = save_modifiers(lich, "wis", kind="turn")
    assert mods.mode is RollMode.ADVANTAGE
    assert mods.advantage_sources == ["Turn Resistance"]
    # La ventaja llega a la tirada real.
    resultado = saving_throw(lich, "wis", 30, random.Random(1), kind="turn")
    assert resultado.mode is RollMode.ADVANTAGE
    assert len(resultado.rolls) == 2


def test_sin_el_tipo_de_efecto_no_aplica(monkeypatch):
    """Un daño de fuego o un hechizo cualquiera no son «turn undead»."""
    lich = _lich(monkeypatch)
    assert save_modifiers(lich, "wis").mode is RollMode.NORMAL
    assert save_modifiers(lich, "wis", kind=None).mode is RollMode.NORMAL
    assert save_modifiers(lich, "wis", kind="spell").mode is RollMode.NORMAL
    assert save_modifiers(lich, "wis", kind="fire").mode is RollMode.NORMAL
    assert saving_throw(lich, "wis", 30, random.Random(2)).mode is RollMode.NORMAL


def test_solo_afecta_a_las_criaturas_con_el_rasgo():
    # Un PJ sin el rasgo tira igual con el mismo tipo de efecto.
    assert save_modifiers(_pj(), "wis", kind="turn").mode is RollMode.NORMAL
    assert saving_throw(_pj(), "wis", 30, random.Random(3),
                        kind="turn").mode is RollMode.NORMAL


def test_con_ventaja_acierta_mas_que_sin_ella(monkeypatch):
    """La ventaja se nota en el resultado, no solo en la etiqueta."""
    lich = _lich(monkeypatch)
    dc = 25
    aciertos_ventaja = sum(
        saving_throw(lich, "wis", dc, random.Random(s), kind="turn").success
        for s in range(300))
    aciertos_normal = sum(
        saving_throw(lich, "wis", dc, random.Random(s)).success
        for s in range(300))
    assert aciertos_ventaja > aciertos_normal, (
        f"ventaja: {aciertos_ventaja} vs normal: {aciertos_normal}")

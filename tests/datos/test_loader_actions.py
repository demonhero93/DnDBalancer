"""Carga de acciones con uso limitado y clasificación de áreas (loader)."""
import json
import random
import warnings
from pathlib import Path

import pytest

from dnd_sim.model.actions import AttackAction
from dnd_sim.rules.area import AreaSaveAction
from dnd_sim.rules.area import AreaTargeting
from dnd_sim.rules.conditions import Condition, ConditionAction
from dnd_sim.model.combatant import PlayerCharacter
from dnd_sim.data.area_classifier import is_area_action
from dnd_sim.data.loader import load_monster
from dnd_sim.data.usage_parser import UnknownUsageError, parse_usage
from dnd_sim.engine.stats import simulate
from dnd_sim.rules.usage import ActionUsage, UsageKind

FIXTURES = Path(__file__).parents[1] / "fixtures"


def _data(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _load(monkeypatch, index: str, data=None):
    payload = data if data is not None else _data(index)
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: payload)
    return load_monster(index)


def _raw_action(data: dict, name: str) -> dict:
    return next(a for a in data["actions"] if a.get("name") == name)


def _area_action(monster):
    """Acción de área del monstruo (suelta o dentro del multiataque)."""
    for action in monster.actions:
        if isinstance(action, AreaSaveAction):
            return action
    multiattack = getattr(monster, "multiattack", None)
    for action in (getattr(multiattack, "action_entries", None) or {}).values():
        if isinstance(action, AreaSaveAction):
            return action
    return None


# --- Mapeo del Aliento de fuego de los fixtures ---------------------------- #

@pytest.mark.parametrize("index,nombre", [("adult-red-dragon", "Fire Breath"),
                                           ("chimera", "Fire Breath")])
def test_aliento_mapeado_a_area_con_recarga(monkeypatch, index, nombre):
    """Los datos se leen del JSON del fixture, no de memoria."""
    data = _data(index)
    bruto = _raw_action(data, nombre)
    usage_raw = bruto["usage"]
    dc = bruto["dc"]
    damage = bruto["damage"][0]

    monster = _load(monkeypatch, index)
    accion = _area_action(monster)

    assert accion is not None, "el aliento debe cargarse como acción de área"
    assert accion.name == nombre
    assert isinstance(accion.targeting, AreaTargeting)

    # Uso limitado.
    assert accion.usage is not None
    assert accion.usage.kind is UsageKind.RECHARGE_ROLL
    assert accion.usage.recharge_dice == usage_raw["dice"]
    assert accion.usage.recharge_min == usage_raw["min_value"]
    assert accion.usage.charged is True

    # Efecto: CD, característica de salvación y daño.
    assert accion.effect.dc == dc["dc_value"]
    assert accion.effect.ability == dc["dc_type"]["index"]
    assert accion.effect.damage == damage["damage_dice"]
    assert accion.effect.damage_type.value == damage["damage_type"]["index"]
    esperado = "half" if dc["success_type"] == "half" else "none"
    assert accion.effect.on_success == esperado


def test_accion_con_dc_sin_dano_carga_como_condition_action(monkeypatch):
    """'Web' (dc sin daño) ahora carga: salvación DES 13 + condición + recarga."""
    data = _data("giant-spider")
    bruto = _raw_action(data, "Web")
    assert bruto.get("dc") and bruto.get("damage") == []

    monster = _load(monkeypatch, "giant-spider")
    web = next(a for a in monster.actions if getattr(a, "name", "") == "Web")
    assert isinstance(web, ConditionAction)
    assert web.effect.condition is Condition.RESTRAINED
    assert web.effect.save_ability == "dex"
    assert web.effect.dc == bruto["dc"]["dc_value"]
    assert web.effect.duration_rounds is None  # hasta destruir la telaraña
    assert web.usage.kind is UsageKind.RECHARGE_ROLL
    # 'Bite' sigue cargando como ataque normal.
    nombres = [getattr(a, "name", "") for a in monster.actions]
    assert "Bite" in nombres


# --- Parser de usos -------------------------------------------------------- #

def test_usage_parser_cada_tipo():
    assert parse_usage(None, "Monstruo", "Acción") is None
    assert parse_usage({"type": "at will"}, "Monstruo", "Acción") is None

    per_day = parse_usage({"type": "per day", "times": 3}, "Monstruo", "Acción")
    assert per_day.kind is UsageKind.PER_DAY
    assert per_day.uses_max == 3
    assert per_day.uses_left == 3

    recharge = parse_usage({"type": "recharge on roll", "dice": "1d6", "min_value": 5},
                            "Monstruo", "Acción")
    assert recharge.kind is UsageKind.RECHARGE_ROLL
    assert recharge.recharge_dice == "1d6"
    assert recharge.recharge_min == 5
    assert recharge.charged is True

    # "recharge after rest" se trata como un uso por combate (# TODO).
    after_rest = parse_usage({"type": "recharge after rest", "rest_types": ["short", "long"]},
                             "Monstruo", "Acción")
    assert after_rest.kind is UsageKind.PER_DAY
    assert after_rest.uses_max == 1


def test_usage_parser_tipo_desconocido_avisa():
    with pytest.warns(UserWarning, match="desconocido"):
        with pytest.raises(UnknownUsageError):
            parse_usage({"type": "inventado", "times": 1}, "Monstruo", "Acción")


def test_accion_con_usage_desconocido_se_omite(monkeypatch):
    data = _data("ogre")
    data["actions"].append({
        "name": "Acción rara",
        "desc": "x",
        "attack_bonus": 6,
        "usage": {"type": "inventado", "times": 1},
        "damage": [{"damage_type": {"index": "fire"}, "damage_dice": "1d6"}],
    })
    with pytest.warns(UserWarning, match="desconocido"):
        monster = _load(monkeypatch, "ogre", data)
    nombres = [getattr(a, "name", "") for a in monster.attacks]
    assert "Acción rara" not in nombres


# --- Clasificador de áreas ------------------------------------------------- #

def test_clasificador_el_aliento_del_fixture_es_area():
    data = _data("adult-red-dragon")
    assert is_area_action(_raw_action(data, "Fire Breath")) is True
    data_chimera = _data("chimera")
    assert is_area_action(_raw_action(data_chimera, "Fire Breath")) is True


def test_clasificador_accion_de_objetivo_unico():
    """No hay ninguna acción de objetivo único con dc+daño en los fixtures.

    Se prueba con un dict sintético cuyo texto es el real de la API
    (gelatinous-cube / "Engulf", objetivo único).
    """
    objetivo_unico = {
        "name": "Engulf",
        "desc": (
            "The cube moves up to its speed. While doing so, it can enter Large or "
            "smaller creatures' spaces. Whenever the cube enters a creature's space, "
            "the creature must make a DC 12 Dexterity saving throw, taking 3d6 (3d6) "
            "acid damage if it fails the save, or half as much damage (1d6 1d6) if it "
            "succeeds. The cube can engulf a creature of the appropriate size or "
            "smaller. While a creature is engulfed, it takes 3d6 (3d6) acid damage at "
            "the start of each of the cube's turns."
        ),
    }
    assert is_area_action(objetivo_unico) is False

    # Y el resto de fixtures con dc+daño son de área.
    for index in ("adult-red-dragon", "chimera"):
        data = _data(index)
        for action in data["actions"]:
            if action.get("dc") and action.get("damage"):
                assert is_area_action(action) is True, f"{index}: {action['name']}"


# --- Ataques con uso limitado --------------------------------------------- #

def test_damage_con_formato_de_opciones_se_parsea(monkeypatch):
    """La API también usa {"choose": n, "from": {"options": [...]}} en el daño.

    Con este formato el ataque se perdía (y el monstruo no cargaba).
    """
    data = _data("ogre")
    data["actions"][0]["damage"] = [{
        "choose": 1,
        "type": "damage",
        "from": {
            "option_set_type": "options_array",
            "options": [{
                "option_type": "damage",
                "damage_type": {"index": "piercing"},
                "damage_dice": "1d8+2",
            }],
        },
    }]
    monster = _load(monkeypatch, "ogre", data)
    atk = monster.attacks[0]
    assert atk.damage == "1d8+2"
    assert atk.damage_type.value == "piercing"


def test_ataque_con_usage_conserva_el_actionusage(monkeypatch):
    """En la SRD no hay ataques con usage y daño (el 'Web' no inflige daño).

    Se parte de un monstruo real del fixture y se le añade el uso por código.
    """
    data = _data("ogre")
    _raw_action(data, "Greatclub")["usage"] = {
        "type": "recharge on roll", "dice": "1d6", "min_value": 5,
    }
    monster = _load(monkeypatch, "ogre", data)

    ataque = next(a for a in monster.attacks if a.name == "Greatclub")
    assert ataque.usage is not None
    assert ataque.usage.kind is UsageKind.RECHARGE_ROLL
    assert ataque.usage.recharge_dice == "1d6"
    assert ataque.usage.recharge_min == 5

    accion = next(a for a in monster.actions if isinstance(a, AttackAction)
                  and a.name == "Greatclub")
    assert accion.usage is ataque.usage, "el AttackAction hereda el uso del ataque"


# --- Integración ----------------------------------------------------------- #

def test_simulate_con_dragon_reporta_usos_y_areas(monkeypatch):
    monster = _load(monkeypatch, "adult-red-dragon")
    heroe = PlayerCharacter(
        name="Guerrero", max_hp=28, ac=18, proficiency=2,
        attacks=[],
    )
    stats = simulate([heroe, monster], n=50, seed=1)
    assert "Fire Breath" in stats["action_uses_avg"]
    assert stats["action_uses_avg"]["Fire Breath"] > 0
    assert stats["area_uses_total"] > 0
    assert 1.0 <= stats["area_targets_avg"] <= 2.0


def test_simulate_es_reproducible_con_recarga_y_area(monkeypatch):
    monster = _load(monkeypatch, "adult-red-dragon")
    heroe = PlayerCharacter(name="Guerrero", max_hp=28, ac=18, attacks=[])
    a = simulate([heroe, monster], n=20, seed=7)
    b = simulate([heroe, monster], n=20, seed=7)
    assert a["win_rate"] == b["win_rate"]
    assert a["rounds_avg"] == b["rounds_avg"]
    assert a["action_uses_avg"] == b["action_uses_avg"]
    assert a["area_targets_avg"] == b["area_targets_avg"]

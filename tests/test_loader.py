import json
from pathlib import Path

import pytest

import dnd_sim.data.api_client as api_client_mod
from dnd_sim.data.api_client import get_monster
from dnd_sim.data.loader import _armor_class_value, load_monster

FIXTURE = Path(__file__).parent / "fixtures" / "ogre.json"


def _ogre_data() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_load_monster_maps_ogre(monkeypatch):
    data = _ogre_data()
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)

    c = load_monster("ogre", team="NPC")
    assert c.name == "Ogre"
    assert c.max_hp == 59
    assert c.ac == 11
    assert c.abilities.str == 19
    assert c.abilities.dex == 8
    assert c.abilities.con == 16
    assert c.abilities.int == 5
    assert c.abilities.wis == 7
    assert c.abilities.cha == 7
    assert c.attacks, "debe tener al menos un ataque"
    atk = c.attacks[0]
    assert atk.attack_bonus == 6
    assert atk.damage_bonus == 0
    assert atk.damage == "2d8+4"


def test_armor_class_as_number(monkeypatch):
    data = _ogre_data()
    data["armor_class"] = 13
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)

    c = load_monster("ogre")
    assert c.ac == 13


def test_armor_class_as_list(monkeypatch):
    data = _ogre_data()
    data["armor_class"] = [{"type": "armor", "value": 14}]
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)

    c = load_monster("ogre")
    assert c.ac == 14


def test_armor_class_helper():
    assert _armor_class_value(11) == 11
    assert _armor_class_value([{"value": 12}]) == 12
    assert _armor_class_value([13]) == 13


def test_cache_avoids_second_network(monkeypatch, tmp_path):
    data = _ogre_data()
    cache_dir = tmp_path / "cache" / "monsters"
    monkeypatch.setattr(api_client_mod, "CACHE_DIR", cache_dir)

    payload = json.dumps(data).encode("utf-8")

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return payload

    calls = {"count": 0}

    def fake_urlopen(url, timeout=None):
        calls["count"] += 1
        return FakeResponse()

    monkeypatch.setattr(api_client_mod.urllib.request, "urlopen", fake_urlopen)

    first = get_monster("ogre")
    second = get_monster("ogre")

    assert first == second == data
    assert calls["count"] == 1, "la caché debe evitar la segunda petición de red"


def test_monster_without_valid_attacks_raises(monkeypatch):
    data = _ogre_data()
    data["actions"] = [{"name": "Multiattack", "desc": "x"}]
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)

    with pytest.raises(ValueError):
        load_monster("ogre")
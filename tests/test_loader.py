import json
import random
from pathlib import Path

import pytest

from dnd_sim.model.actions import AttackEntry, MultiattackAction
from dnd_sim.engine.combat import run_combat
from dnd_sim.model.combatant import Combatant, PlayerCharacter

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


FIXTURES = Path(__file__).parent / "fixtures"


def _load_fixture(monkeypatch, index: str) -> Combatant:
    data = json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: data)
    return load_monster(index)


def test_load_monster_maps_owlbear_multiattack(monkeypatch):
    c = _load_fixture(monkeypatch, "owlbear")
    assert isinstance(c.multiattack, MultiattackAction)
    assert len(c.multiattack.options) == 1
    assert [(e.attack_name, e.count) for e in c.multiattack.options[0]] == [
        ("Beak", 1), ("Claws", 1)
    ]
    # Los ataques referenciados no compiten como acciones sueltas.
    assert all(getattr(a, "only_in_multiattack", False) for a in c.attacks
               if a.name in ("Beak", "Claws"))


def test_owlbear_multiattack_exact_counts(monkeypatch):
    owlbear = _load_fixture(monkeypatch, "owlbear")
    # Un objetivo inmortal para que se ejecuten muchos ataques.
    from dnd_sim.core.abilities import Abilities
    objetivo = PlayerCharacter(name="Objetivo", max_hp=100000, ac=30,
                              abilities=Abilities(), attacks=[])
    res = run_combat([objetivo, owlbear], random.Random(3), verbose=True)
    beak = sum(" con Beak:" in line for line in res.log)
    claws = sum(" con Claws:" in line for line in res.log)
    assert beak == claws
    assert beak + claws > 0


def test_no_handcrafted_monsters_in_source():
    root = Path(__file__).resolve().parents[1]
    files = list((root / "dnd_sim").rglob("*.py")) + [root / "main.py"]
    forbidden = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        if 'team="NPC"' in text or "team='NPC'" in text:
            forbidden.append(str(path))
    assert not forbidden, f"Monstruos a mano en código fuente: {forbidden}"

import json
import random
from pathlib import Path

import pytest

from dnd_sim import Abilities, Attack, Combatant, DamageType, apply_damage_modifiers, simulate
from dnd_sim import Monster, PlayerCharacter
from dnd_sim.combat import run_combat
from dnd_sim.data.loader import load_monster

FIXTURE = Path(__file__).parent / "fixtures" / "ogre.json"


def _target(resistances=(), vulnerabilities=(), immunities=()) -> Combatant:
    return Monster(
        name="Objetivo",
        max_hp=20,
        ac=10,
        resistances=set(resistances),
        vulnerabilities=set(vulnerabilities),
        immunities=set(immunities),
    )


def test_resistance_halves_damage_floor():
    t = _target(resistances={"bludgeoning"})
    assert apply_damage_modifiers(7, "bludgeoning", t) == 3


def test_vulnerability_doubles_damage():
    t = _target(vulnerabilities={"fire"})
    assert apply_damage_modifiers(7, "fire", t) == 14


def test_immunity_zero():
    t = _target(immunities={"poison"})
    assert apply_damage_modifiers(7, "poison", t) == 0


def test_resistance_then_vulnerability_same_type():
    t = _target(resistances={"acid"}, vulnerabilities={"acid"})
    # 7 -> 3 (resistencia) -> 6 (vulnerabilidad)
    assert apply_damage_modifiers(7, "acid", t) == 6


def test_no_modifiers_unchanged():
    t = _target()
    assert apply_damage_modifiers(7, "thunder", t) == 7


def test_strings_are_converted():
    # Combatant normaliza strings a DamageType.
    t = Monster(name="T", max_hp=10, ac=10, resistances={"fire"})
    assert DamageType.FIRE in t.resistances
    # Attack también acepta str.
    atk = Attack("Golpe", "1d8", damage_type="fire")
    assert atk.damage_type == DamageType.FIRE


def test_invalid_damage_type_raises():
    with pytest.raises(ValueError):
        DamageType("fuego")
    with pytest.raises(ValueError):
        apply_damage_modifiers(5, "nope", _target())


def test_immune_target_takes_zero_damage(monkeypatch):
    """Con semilla fija, un inmune al tipo del ataque recibe 0 en cada impacto."""
    atk = Attack("Espada", "1d6", ability="str", damage_type="slashing")
    attacker = PlayerCharacter(
        name="Atacante", max_hp=20, ac=10,
        abilities=Abilities(str=16),
        attacks=[atk],
    )
    target = Monster(
        name="Inmune", max_hp=20, ac=5,
        immunities={"slashing"},
    )
    stats = simulate([attacker, target], n=20, seed=1)
    assert stats["hp_left_avg"]["Inmune"] == 20.0


def test_regression_guerrero_vs_ogro(monkeypatch):
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)

    guerrero = PlayerCharacter(
        name="Guerrero", max_hp=28, ac=18, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[Attack("Espada larga", "1d8", ability="str")],
    )
    ogro = load_monster("ogre")

    stats = simulate([guerrero, ogro], n=1000, seed=1)
    assert stats["win_rate"]["PJ"] == pytest.approx(0.108, abs=1e-9)
    assert stats["win_rate"]["NPC"] == pytest.approx(0.892, abs=1e-9)
    assert stats["rounds_avg"] == pytest.approx(5.881, abs=1e-9)
    assert stats["hp_left_avg"]["Guerrero"] == pytest.approx(1.073, abs=1e-9)
    assert stats["hp_left_avg"]["Ogre"] == pytest.approx(27.503, abs=1e-9)


def test_attack_roll_log_modifier(monkeypatch, capsys):
    # Smoke: el motor no explota con modificadores y registra el modificador en el log.
    a = PlayerCharacter(
        name="A", max_hp=10, ac=5,
        abilities=Abilities(str=16), attacks=[Attack("Golpe", "1d8", ability="str", damage_type="fire")],
    )
    b = Monster(name="B", max_hp=20, ac=5, vulnerabilities={"fire"})
    res = run_combat([a, b], random.Random(1), verbose=True)
    assert any("(vulnerable:" in line for line in res.log)


def _guerrero_y_ogro(monkeypatch):
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    guerrero = PlayerCharacter(
        name="Guerrero", max_hp=28, ac=18, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[Attack("Espada larga", "1d8", ability="str")],
    )
    return guerrero, load_monster("ogre")


def test_danio_medio_por_combatiente_y_equipo(monkeypatch):
    guerrero, ogro = _guerrero_y_ogro(monkeypatch)
    stats = simulate([guerrero, ogro], n=50, seed=1)

    assert stats["teams"]["Guerrero"] == "PJ"
    assert stats["teams"]["Ogre"] == "NPC"

    # El ogre inflige y recibe daño; el PJ recibe (y a veces inflige).
    assert stats["damage_dealt_avg"]["Ogre"] > 0
    assert stats["damage_received_avg"]["Guerrero"] > 0
    assert stats["damage_received_avg"]["Ogre"] > 0

    # El daño infligido por el ogre es el que recibe el PJ (y viceversa).
    assert stats["damage_dealt_avg"]["Ogre"] == pytest.approx(
        stats["damage_received_avg"]["Guerrero"], rel=1e-9)


def test_informe_final_con_apartados_de_pj_y_monstruros(monkeypatch, capsys):
    from dnd_sim.stats import print_report

    guerrero, ogro = _guerrero_y_ogro(monkeypatch)
    stats = simulate([guerrero, ogro], n=20, seed=1)
    print_report(stats)
    salida = capsys.readouterr().out

    assert "Daño medio de combate:" in salida
    assert "PJ:" in salida
    assert "Monstruos:" in salida
    assert "Guerrero:" in salida
    assert "Ogre:" in salida
    # Los usos medios por combate se han sustituido por el daño medio.
    assert "Usos medios por combate" not in salida
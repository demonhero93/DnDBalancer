"""Multiataque: opciones de la API, alternativas y número de ataques por turno."""
import json
import random
from collections import Counter
from pathlib import Path

import pytest

from dnd_sim.model.actions import AttackAction, MultiattackAction
from dnd_sim.engine.combat import run_combat
from dnd_sim.model.combatant import PlayerCharacter
from dnd_sim.data.loader import load_monster
from dnd_sim.rules.usage import UsageKind

FIXTURES = Path(__file__).parents[1] / "fixtures"


def _data(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _load(monkeypatch, index: str, data=None):
    payload = data if data is not None else _data(index)
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: payload)
    return load_monster(index)


def _pj(name: str = "Guerrero", hp: int = 900) -> PlayerCharacter:
    from dnd_sim.core.abilities import Abilities
    return PlayerCharacter(
        name=name, max_hp=hp, ac=15, proficiency=2,
        abilities=Abilities(str=14, dex=14, con=14, int=10, wis=10, cha=10),
        attacks=[],
    )


def _raw_multiattack(data: dict) -> dict:
    return next(a for a in data["actions"] if a.get("name") == "Multiattack")


def _chimera_con_alternativas_sinteticas() -> dict:
    """Fixture 2024 reconstruido con las alternativas anidadas de la ficha.

    El fixture reparte los ataques base en ``actions`` y la opción del
    aliento en ``action_options`` (opciones planas). Aquí se reescribe la
    estructura anidada ``items[]`` que sí agrupa los tres ataques por
    alternativa: Ram + Bite + Claw, con Claw sustituible por Fire Breath.
    """
    data = _data("chimera")
    _raw_multiattack(data)["action_options"] = {
        "choose": 1,
        "type": "action",
        "from": {
            "option_set_type": "options_array",
            "options": [
                {"option_type": "multiple", "items": [
                    {"action_name": "Ram", "count": 1, "type": "melee"},
                    {"action_name": "Bite", "count": 1, "type": "melee"},
                    {"action_name": "Claw", "count": 1, "type": "melee"},
                ]},
                {"option_type": "multiple", "items": [
                    {"action_name": "Ram", "count": 1, "type": "melee"},
                    {"action_name": "Bite", "count": 1, "type": "melee"},
                    {"action_name": "Fire Breath", "count": 1, "type": "special"},
                ]},
            ],
        },
    }
    return data


# --- La quimera: la API trae el multiataque en "action_options" ------------ #

def test_multiattack_de_la_quimera_se_parsea_desde_action_options(monkeypatch):
    """La API 2024 trae action_options con opciones planas (action_name/count)."""
    data = _data("chimera")
    bruto = _raw_multiattack(data)
    opciones = bruto["action_options"]["from"]["options"]
    assert len(opciones) == 2

    chimera = _load(monkeypatch, "chimera")
    assert isinstance(chimera.multiattack, MultiattackAction)
    assert len(chimera.multiattack.options) == 2

    # Cada opción plana se resuelve en una entrada (Garras o el Aliento).
    esperadas = [[opcion["action_name"]] for opcion in opciones]
    obtenidas = [
        [e.attack_name for e in alt] for alt in chimera.multiattack.options
    ]
    assert obtenidas == esperadas
    for alternativa in chimera.multiattack.options:
        assert len(alternativa) == 1


def test_el_aliento_de_la_quimera_no_compite_como_accion_suelta(monkeypatch):
    """El aliento sustituye a un ataque DENTRO del multiataque."""
    chimera = _load(monkeypatch, "chimera")
    nombres = [getattr(a, "name", "") for a in chimera.actions]
    assert nombres == ["Multiattack"]
    # ...pero sigue disponible dentro del multiataque.
    assert "Fire Breath" in chimera.multiattack.action_entries


def test_la_quimera_hace_tres_ataques_por_turno(monkeypatch):
    # Sin utilitarias (p=0): un Agarrar sustituiría un ataque del conteo.
    monkeypatch.setattr("dnd_sim.rules.utility.UTILITY_ACTION_PROBABILITY", 0.0)
    quimera = _load(monkeypatch, "chimera", _chimera_con_alternativas_sinteticas())
    jugador = _pj()
    res = run_combat([jugador, quimera], random.Random(5), verbose=True, max_rounds=12)

    rondas = {}
    ronda = None
    for line in res.log:
        if line.startswith("-- Ronda"):
            ronda = line
            rondas[ronda] = 0
        elif "Chimera ->" in line or "Chimera usa Fire Breath" in line:
            rondas[ronda] += 1

    assert rondas, "debe haber rondas con ataques"
    assert all(n == 3 for n in rondas.values()), rondas

def test_el_aliento_dentro_del_multiataque_gasta_su_uso(monkeypatch):
    quimera = _load(monkeypatch, "chimera")
    usage = quimera.multiattack.action_entries["Fire Breath"].usage
    assert usage is not None
    assert usage.kind is UsageKind.RECHARGE_ROLL
    assert usage.charged is True

    jugador = _pj()
    res = run_combat([jugador, quimera], random.Random(5), verbose=True, max_rounds=12)
    if any("Chimera usa Fire Breath" in line for line in res.log):
        assert not usage.charged, "el aliento se descarga al usarlo en el multiataque"


def test_las_alternativas_con_el_aliento_descargado_no_son_viables(monkeypatch):
    """La ficha dice: 'cuando su aliento está disponible puede usarlo'."""
    # Sin utilitarias (p=0): el stream de RNG es el original.
    monkeypatch.setattr("dnd_sim.rules.utility.UTILITY_ACTION_PROBABILITY", 0.0)
    quimera = _load(monkeypatch, "chimera", _chimera_con_alternativas_sinteticas())
    usage = quimera.multiattack.action_entries["Fire Breath"].usage
    usage.spend()  # aliento descargado

    jugador = _pj()
    res = run_combat([jugador, quimera], random.Random(5), verbose=True, max_rounds=12)
    assert not any("Chimera usa Fire Breath" in line for line in res.log)
    # Sigue haciendo 3 ataques por turno (solo de mordida/cuernos/garras).
    rondas = {}
    ronda = None
    for line in res.log:
        if line.startswith("-- Ronda"):
            ronda = line
            rondas[ronda] = 0
        elif "Chimera ->" in line:
            rondas[ronda] += 1
    assert rondas and all(n == 3 for n in rondas.values()), rondas


# --- El dragón rojo: formato "actions" (sin cambios) ---------------------- #

def test_multiattack_del_dragon_sigue_igual(monkeypatch):
    data = _data("adult-red-dragon")
    bruto = _raw_multiattack(data)
    assert bruto["multiattack_type"] == "actions"

    dragon = _load(monkeypatch, "adult-red-dragon")
    alternativas = [[(e.attack_name, e.count) for e in alt]
                    for alt in dragon.multiattack.options]
    # El fixture 2024 añade action_options (Rend o Scorching Ray) y solo la
    # opción que es ataque del monstruo se conserva: un Rend.
    assert alternativas == [[("Rend", 1)]]
    # El aliento del dragón sí es una acción aparte (no va en su multiataque).
    nombres = [getattr(a, "name", "") for a in dragon.actions]
    assert "Fire Breath" in nombres


def test_el_dragon_hace_tres_ataques_por_turno(monkeypatch):
    """El dragón tiene dos acciones: multiataque (3 golpes) o aliento.

    Los ataques **legendarios** (el Pounce) van aparte: no cuentan como
    parte del multiataque.
    """
    data = _data("adult-red-dragon")
    # El fixture 2024 reparte el multiataque entre "actions" (Rend x2) y
    # "action_options" (Rend o Scorching Ray); aquí se reconstruye la lista
    # plana de tres Rend que dicta la ficha.
    bruto = _raw_multiattack(data)
    bruto.pop("action_options", None)
    bruto["actions"] = [{"action_name": "Rend", "count": "3", "type": "melee"}]
    dragon = _load(monkeypatch, "adult-red-dragon", data)
    # Sin utilitarias (p=0): el conteo de 3 ataques fija el stream original.
    monkeypatch.setattr("dnd_sim.rules.utility.UTILITY_ACTION_PROBABILITY", 0.0)
    jugador = _pj()
    res = run_combat([jugador, dragon], random.Random(3), verbose=True, max_rounds=10)

    rondas = {}
    ronda = None
    en_legendaria = False
    for line in res.log:
        if line.startswith("-- Ronda"):
            ronda = line
            rondas[ronda] = {"ataques": 0, "aliento": 0, "legendarias": 0,
                             "hechizo": 0}
            en_legendaria = False
        elif line.startswith("[Legendaria]"):
            en_legendaria = True
        elif "Adult Red Dragon ->" in line:
            if en_legendaria:
                rondas[ronda]["legendarias"] += 1
                en_legendaria = False
            elif " con Rend:" in line:
                rondas[ronda]["ataques"] += 1
            else:
                # Hechizo con varias líneas de ataque (Scorching Ray).
                rondas[ronda]["hechizo"] += 1
        elif "Adult Red Dragon usa " in line:
            # El turno se consumió en el aliento o en un hechizo de la
            # Spellcasting (Fireball).
            if "Fire Breath" in line:
                rondas[ronda]["aliento"] += 1
            else:
                rondas[ronda]["hechizo"] += 1
            en_legendaria = False
        # Movimientos y recargas no alteran la bandera legendaria.

    assert rondas
    for ronda, cuenta in rondas.items():
        if cuenta["aliento"]:
            # El turno se consumió en el aliento: no hay ataques ese turno.
            assert cuenta["ataques"] == 0, ronda
        elif cuenta["ataques"]:
            assert cuenta["ataques"] == 3, ronda
        else:
            # Turno de hechizo: ni ataques ni aliento.
            assert cuenta["hechizo"] >= 1, ronda

# --- El búho: formato "actions" con un solo ataque (Rend x2) --------------- #

def test_multiattack_del_owlbear_no_cambia(monkeypatch):
    from dnd_sim.model.actions import AttackEntry

    owlbear = _load(monkeypatch, "owlbear")
    entradas = [[(e.attack_name, e.count) for e in alt]
                for alt in owlbear.multiattack.options]
    assert entradas == [[("Rend", 2)]]
    assert all(getattr(a, "only_in_multiattack", False) for a in owlbear.attacks
               if a.name == "Rend")
    # Los ataques del multiataque no compiten como acciones sueltas.
    assert not [a for a in owlbear.actions if isinstance(a, AttackAction)]

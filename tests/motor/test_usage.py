"""Usos limitados y recarga de acciones."""
import json
import random
import statistics
from pathlib import Path

import pytest

from dnd_sim.core.abilities import Abilities
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.rules.area import AreaSaveAction
from dnd_sim.engine.combat import run_combat
from dnd_sim.model.combatant import PlayerCharacter
from dnd_sim.data.loader import load_monster
from dnd_sim.rules.usage import ActionUsage, UsageKind, begin_turn

FIXTURES = Path(__file__).parents[1] / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _load_fixture(monkeypatch, index: str):
    data = json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: data)
    return load_monster(index)


def _breath(monkeypatch, index: str = "adult-red-dragon"):
    """Monstruo del fixture + su acción de Aliento de fuego."""
    monster = _load_fixture(monkeypatch, index)
    for action in monster.actions:
        if isinstance(action, AreaSaveAction) and action.name == "Fire Breath":
            return monster, action
    raise AssertionError(f"El fixture {index!r} no tiene Aliento de fuego")


def _player(name: str = "Guerrero", hp: int = 100000) -> PlayerCharacter:
    return PlayerCharacter(
        name=name, max_hp=hp, ac=18, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[],
    )


class _FixedRandom:
    """RNG de mentira que siempre devuelve el mismo valor (y cuenta llamadas)."""

    def __init__(self, value: int):
        self.value = value
        self.calls = 0

    def randint(self, a, b):
        self.calls += 1
        return self.value

    def getstate(self):
        return ("fixed", self.calls)

    def setstate(self, state):
        pass


# --- PER_DAY --------------------------------------------------------------- #

def test_per_day_dos_usos_y_luego_can_use_falso(monkeypatch):
    monster, breath = _breath(monkeypatch)
    usage = ActionUsage(kind=UsageKind.PER_DAY, uses_max=2)
    breath.usage = usage

    ctx = CombatContext(rng=random.Random(1), actor=monster, combatants=[monster],
                        round=1, resources=TurnResources())

    assert usage.available
    assert breath.can_use(ctx.resources, ctx)

    usage.spend()
    assert usage.available
    assert breath.can_use(ctx.resources, ctx)

    usage.spend()
    assert not usage.available
    assert not breath.can_use(ctx.resources, ctx)


def test_per_day_reset_restaura_todos_los_usos(monkeypatch):
    monster, breath = _breath(monkeypatch)
    usage = ActionUsage(kind=UsageKind.PER_DAY, uses_max=3)
    breath.usage = usage

    usage.spend()
    usage.spend()
    assert usage.uses_left == 1

    usage.reset()
    assert usage.uses_left == 3
    assert usage.available


def test_at_will_nunca_se_agota():
    usage = ActionUsage(kind=UsageKind.AT_WILL)
    for _ in range(10):
        usage.spend()
    assert usage.available
    usage.reset()
    assert usage.available


# --- RECHARGE_ROLL --------------------------------------------------------- #

def test_recharge_roll_al_gastarse_queda_descargada():
    usage = ActionUsage(kind=UsageKind.RECHARGE_ROLL, recharge_dice="1d6", recharge_min=5)
    assert usage.available
    usage.spend()
    assert not usage.available
    assert not usage.charged


def test_recharge_mientras_esta_cargada_no_consume_rng():
    rng = random.Random(1)
    usage = ActionUsage(kind=UsageKind.RECHARGE_ROLL, recharge_dice="1d6", recharge_min=5)
    estado = rng.getstate()
    assert usage.try_recharge(rng) is False
    assert rng.getstate() == estado, "no debe gastarse RNG si ya está cargada"


def test_recharge_recarga_con_5_o_mas_y_falla_con_4():
    usage = ActionUsage(kind=UsageKind.RECHARGE_ROLL, recharge_dice="1d6", recharge_min=5)

    usage.spend()
    rng = _FixedRandom(5)
    assert usage.try_recharge(rng) is True
    assert usage.charged
    assert rng.calls == 1

    usage.spend()
    rng = _FixedRandom(4)
    assert usage.try_recharge(rng) is False
    assert not usage.charged
    assert rng.calls == 1


def test_recharge_5_6_porcentaje_de_exito():
    rng = random.Random(20260120)
    intentos = 20000
    ok = 0
    for _ in range(intentos):
        usage = ActionUsage(kind=UsageKind.RECHARGE_ROLL, recharge_dice="1d6", recharge_min=5)
        usage.spend()
        if usage.try_recharge(rng):
            ok += 1
    assert abs(ok / intentos - 1 / 3) <= 0.015


def test_media_de_turnos_hasta_recargar():
    rng = random.Random(4242)
    turnos = []
    for _ in range(2000):
        usage = ActionUsage(kind=UsageKind.RECHARGE_ROLL, recharge_dice="1d6", recharge_min=5)
        usage.spend()
        n = 1
        while not usage.try_recharge(rng):
            n += 1
        turnos.append(n)
    # Geométrica con p = 1/3 -> media 3 turnos.
    assert abs(statistics.mean(turnos) - 3.0) < 0.15


def test_per_day_no_tira_recarga():
    usage = ActionUsage(kind=UsageKind.PER_DAY, uses_max=1)
    usage.spend()
    rng = _FixedRandom(6)
    assert usage.try_recharge(rng) is False
    assert rng.calls == 0


# --- begin_turn ------------------------------------------------------------ #

def test_begin_turn_reinicia_recursos_y_tira_una_recarga_por_accion(monkeypatch):
    monster, breath = _breath(monkeypatch)
    usage = breath.usage
    usage.spend()  # queda descargada

    rng = _FixedRandom(5)
    ctx = CombatContext(rng=rng, actor=monster, combatants=[monster], round=1,
                        resources=TurnResources())
    ctx.resources.action_used = True
    ctx.resources.bonus_action_used = True

    begin_turn(monster, ctx)

    assert isinstance(ctx.resources, TurnResources)
    assert not ctx.resources.action_used
    assert not ctx.resources.bonus_action_used
    assert rng.calls == 1, "una tirada por acción descargada"
    assert usage.charged


def test_begin_turn_no_tira_nada_si_estan_cargadas(monkeypatch):
    monster, breath = _breath(monkeypatch)
    rng = _FixedRandom(5)
    ctx = CombatContext(rng=rng, actor=monster, combatants=[monster], round=1,
                        resources=TurnResources())
    begin_turn(monster, ctx)
    assert rng.calls == 0


# --- Comportamiento en combate --------------------------------------------- #

def _eventos(log):
    """Extrae del log los eventos de aliento y de recarga."""
    usa = []
    recarga = []
    for i, line in enumerate(log):
        if " usa Fire Breath sobre " in line:
            usa.append(i)
        elif ": recarga Fire Breath" in line and "-> recargado" in line:
            recarga.append(i)
    return usa, recarga


def test_dragon_nunca_usa_el_aliento_dos_turnos_seguidos_sin_recarga(monkeypatch):
    monster = _load_fixture(monkeypatch, "adult-red-dragon")
    jugador = _player()
    rng = random.Random(31)
    for _ in range(40):
        res = run_combat([jugador, monster], rng, verbose=True, max_rounds=30)
        usa, recarga = _eventos(res.log)
        for i, j in zip(usa, usa[1:]):
            assert any(i < r < j for r in recarga), (
                "dos usos de aliento sin recarga entre medias:\n" + "\n".join(res.log)
            )


def test_aliento_se_usa_en_una_fraccion_plausible_de_turnos(monkeypatch):
    monster = _load_fixture(monkeypatch, "adult-red-dragon")
    jugador = _player()
    rng = random.Random(77)
    usos = 0
    turnos = 0
    for _ in range(200):
        res = run_combat([jugador, monster], rng, verbose=True, max_rounds=40)
        usa, _ = _eventos(res.log)
        usos += len(usa)
        turnos += sum(1 for line in res.log if line.strip().startswith("Adult Red Dragon ->"))
    assert turnos > 0
    fraccion = usos / turnos
    assert 0.05 < fraccion < 0.60, f"fracción de turnos con aliento: {fraccion}"


def test_politica_elige_el_aliento_aproximadamente_el_50_cuando_esta_cargado(monkeypatch):
    import dnd_sim.engine.combat.encounter as combat_mod

    monster = _load_fixture(monkeypatch, "adult-red-dragon")
    jugador = _player()
    original = combat_mod._invoke_policy
    conteo = {"cargado_aliento": 0, "cargado_multi": 0, "elegido_aliento": 0}

    def spy(policy, ctx, candidates):
        elegido = original(policy, ctx, candidates)
        nombres = [getattr(a, "name", "") for a in candidates]
        if "Fire Breath" in nombres:
            conteo["cargado_aliento"] += 1
            if getattr(elegido, "name", "") == "Fire Breath":
                conteo["elegido_aliento"] += 1
            else:
                conteo["cargado_multi"] += 1
        return elegido

    monkeypatch.setattr(combat_mod, "_invoke_policy", spy)
    rng = random.Random(5)
    for _ in range(150):
        run_combat([jugador, monster], rng, verbose=False, max_rounds=40)

    total = conteo["cargado_aliento"]
    assert total > 100
    prob = conteo["elegido_aliento"] / total
    assert 0.45 < prob < 0.55, f"probabilidad de elegir el aliento cargado: {prob}"


def test_dos_combates_seguidos_empiezan_con_el_aliento_cargado(monkeypatch):
    monster = _load_fixture(monkeypatch, "adult-red-dragon")
    jugador = _player()

    def _breath_first(ctx):
        for a in ctx.available_actions:
            if getattr(a, "name", "") == "Fire Breath":
                return a
        return ctx.available_actions[0]

    # El primer combate gasta el aliento.
    res = run_combat([jugador, monster], random.Random(4), verbose=True, max_rounds=10,
                     policy=_breath_first)
    usa, _ = _eventos(res.log)
    assert usa, "el primer combate debería usar el aliento"

    # El segundo combate empieza con el aliento cargado (reset).
    res2 = run_combat([jugador, monster], random.Random(4), verbose=True, max_rounds=10,
                      policy=_breath_first)
    usa2, _ = _eventos(res2.log)
    assert usa2, "el segundo combate debería poder usar el aliento (reset)"


def test_copias_de_un_monstruo_tienen_estado_independiente(monkeypatch):
    data = json.loads((FIXTURES / "adult-red-dragon.json").read_text(encoding="utf-8"))
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: data)
    dragon_a = load_monster("adult-red-dragon")
    dragon_b = load_monster("adult-red-dragon")

    def _usage(monster):
        return next(a.usage for a in monster.actions if a.name == "Fire Breath")

    _usage(dragon_a).spend()
    assert not _usage(dragon_a).available
    assert _usage(dragon_b).available, "cada copia tiene su propio estado de uso"


def test_random_policy_no_elige_una_accion_agotada(monkeypatch):
    monster = _load_fixture(monkeypatch, "adult-red-dragon")
    jugador = _player()
    for action in monster.actions:
        if action.name == "Fire Breath":
            action.usage = ActionUsage(kind=UsageKind.PER_DAY, uses_max=1)

    rng = random.Random(13)
    for _ in range(50):
        res = run_combat([jugador, monster], rng, verbose=True, max_rounds=30)
        usa, _ = _eventos(res.log)
        assert len(usa) <= 1, "un uso por día no puede repetirse en el mismo combate"


def test_reproducibilidad_con_recarga_y_area(monkeypatch):
    monster = _load_fixture(monkeypatch, "adult-red-dragon")
    jugador = _player()
    a = run_combat([jugador, monster], random.Random(123), verbose=True, max_rounds=30)
    b = run_combat([jugador, monster], random.Random(123), verbose=True, max_rounds=30)
    assert a.log == b.log
    assert a.action_uses == b.action_uses
    assert a.area_targets_hit == b.area_targets_hit

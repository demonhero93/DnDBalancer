# -*- coding: utf-8 -*-
"""Acciones de guarida: esquema, temporización y semántica (bloque C).

Se asume **siempre** la guarida: la fase corre en cada combate para el
dueño legendario con ``data/lairs/<index>.json`` válido (sin fichero: ni
fase, ni aviso, ni RNG) y ``points_max`` incluye ``LEGENDARY_LAIR_BONUS``.

El fichero de guaridas del test es **sintético** y vive solo en
``tests/fixtures/lairs/``: los datos reales de ``data/lairs/`` los aporta
el maintainer después (el test guardián verifica que el repo está vacío).
"""
from __future__ import annotations

import json
import random
import warnings
from pathlib import Path

import pytest

import dnd_sim.data as data_pkg
from dnd_sim import load_monster
from dnd_sim.data import lair_loader
from dnd_sim.engine.combat import encounter as encounter_mod
from dnd_sim.engine.combat import run_combat
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.model.combatant import Monster, PlayerCharacter
from dnd_sim.rules import saves as saves_mod
from dnd_sim.rules.legendary import LairAction, LegendaryState, lair_phase

FIXTURES = Path(__file__).parent / "fixtures" / "lairs"


@pytest.fixture
def lairs_dir(monkeypatch):
    monkeypatch.setattr(lair_loader, "LAIR_DIR", FIXTURES)
    return FIXTURES


def _dragon(**kwargs):
    m = load_monster("adult-red-dragon")
    for k, v in kwargs.items():
        setattr(m, k, v)
    return m


def _enemigo(name="Blanco", hp=100):
    # OJO: Monster.__post_init__ fuerza combatant_type=NPC, así que el
    # bando "PJ" solo lo da PlayerCharacter.
    return PlayerCharacter(name=name, max_hp=hp, ac=10)


def _pj(name, hp=100, ac=10):
    """PJ sintético para los tests de temporización y semántica."""
    return PlayerCharacter(name=name, max_hp=hp, ac=ac)


def _ctx(owner, combatants, rng=None, round=1, log=None, resources=None):
    return CombatContext(
        rng=rng or random.Random(1), actor=owner, combatants=combatants,
        round=round, log=log, verbose=False, resources=resources)


class _Stub:
    """Acción de guarida que solo registra su uso."""

    def __init__(self, nombre, efecto=None):
        self.nombre = nombre
        self.efecto = efecto

    def execute(self, ctx):
        if self.efecto is not None:
            self.efecto(ctx)


def _orden_con(inits):
    """Sustituto de roll_initiative con iniciativas forzadas."""

    def fake(combatants, rng):
        for c in combatants:
            c.initiative = inits[c.name]
        return sorted(combatants, key=lambda c: c.initiative,
                      reverse=True)

    return fake


# ---------------------------------------------------------------- esquema

def test_fixture_sintetica_carga(lairs_dir):
    m = load_monster("adult-red-dragon")
    assert m.legendary is not None
    assert [a.name for a in m.legendary.lair_actions] == [
        "Fuego de guarida", "Golpe de guarida"]
    fuego = m.legendary.lair_actions[0].action
    golpe = m.legendary.lair_actions[1].action
    assert fuego.effect.magical is True
    assert golpe.effect.magical is False


def test_monstruo_sin_fichero_no_avisa(lairs_dir):
    with warnings.catch_warnings(record=True) as wlist:
        warnings.simplefilter("always")
        m = load_monster("lich")
    assert m.legendary is not None
    assert m.legendary.lair_actions == []
    assert not [w for w in wlist if "uarida" in str(w.message)]


def test_monstruo_no_legendario_no_carga_guaridas(lairs_dir):
    m = load_monster("ogre")
    assert m.legendary is None


@pytest.mark.parametrize("datos,esperado", [
    ([{"name": "X", "kind": "boom"}], "kind inválido"),
    ([{"name": "X", "kind": "save_damage",
       "save": {"ability": "dex", "dc": 10, "damage": "1d6",
                "damage_type": "fire"},
       "hp": 1}], "desconocido"),
    ([{"name": "X", "kind": "save_damage",
       "save": {"ability": "dex", "dc": 0, "damage": "1d6",
                "damage_type": "fire"}}], "save.dc"),
    ([{"name": "", "kind": "save_damage",
       "save": {"ability": "dex", "dc": 10, "damage": "1d6",
                "damage_type": "fire"}}], "'name'"),
    ({"no": "lista"}, "lista"),
])
def test_esquema_invalido(tmp_path, monkeypatch, datos, esperado):
    (tmp_path / "ogre.json").write_text(json.dumps(datos), encoding="utf-8")
    monkeypatch.setattr(lair_loader, "LAIR_DIR", tmp_path)
    with pytest.raises(ValueError, match=esperado):
        lair_loader.load_lair("ogre")


def test_targeting_fuera_de_rango(tmp_path, monkeypatch):
    datos = [{"name": "X", "kind": "area_save_damage",
              "save": {"ability": "dex", "dc": 10, "damage": "1d6",
                       "damage_type": "fire"},
              "targeting": {"min_targets": 0}}]
    (tmp_path / "ogre.json").write_text(json.dumps(datos), encoding="utf-8")
    monkeypatch.setattr(lair_loader, "LAIR_DIR", tmp_path)
    with pytest.raises(ValueError, match="min_targets"):
        lair_loader.load_lair("ogre")


# ----------------------------------------------------------- semántica

def test_sin_fichero_no_actua_ni_loguea(lairs_dir):
    # lich tiene fase legendaria pero no fichero en data/lairs/: la fase
    # corre siempre, pero sin acciones no hay nada que ejecutar ni log.
    m = load_monster("lich")
    assert m.legendary is not None
    assert m.legendary.lair_actions == []
    pj = _pj("Pj", hp=60)
    resultado = run_combat([pj, m], random.Random(1), verbose=True)
    assert not any("[Guarida]" in linea for linea in resultado.log)


def test_una_por_ronda_y_rondas_alternas():
    usos: list[str] = []
    acciones = [LairAction("Única",
                           _Stub("Única", lambda ctx: usos.append("Única")))]
    owner = Monster(name="Dueño", max_hp=50, ac=10,
                    legendary=LegendaryState(lair_actions=acciones))
    enemigo = _enemigo()
    ctx = _ctx(owner, [owner, enemigo])
    for _ in range(4):
        lair_phase(ctx)
        ctx.round += 1
    # Una sola acción: ronda 1 sí, 2 no, 3 sí, 4 no.
    assert usos == ["Única", "Única"]


def test_salto_de_ronda_alternada_no_consume_rng():
    acciones = [LairAction("Única", _Stub("Única"))]
    owner = Monster(name="Dueño", max_hp=50, ac=10,
                    legendary=LegendaryState(lair_actions=acciones))
    enemigo = _enemigo()
    ctx = _ctx(owner, [owner, enemigo], rng=random.Random(5))
    lair_phase(ctx)                       # ronda 1: usa (1 opción, sin RNG)
    estado = ctx.rng.getstate()
    ctx.round += 1
    lair_phase(ctx)                       # ronda 2: sin elegibles, sin RNG
    assert ctx.rng.getstate() == estado


def test_dos_acciones_uniformes():
    conteo = {"A": 0, "B": 0}

    def _cuenta(nombre):
        return lambda ctx: conteo.__setitem__(nombre, conteo[nombre] + 1)

    acciones = [LairAction("A", _Stub("A", _cuenta("A"))),
                LairAction("B", _Stub("B", _cuenta("B")))]
    owner = Monster(name="Dueño", max_hp=50, ac=10,
                    legendary=LegendaryState(lair_actions=acciones))
    enemigo = _enemigo()
    ctx = _ctx(owner, [owner, enemigo], rng=random.Random(9))
    for _ in range(10000):
        lair_phase(ctx)
        ctx.round += 1
    assert abs(conteo["A"] - 5000) < 300  # ~50% ±3%


def test_no_repite_en_rondas_consecutivas():
    usos: list[str] = []
    acciones = [LairAction("A", _Stub("A", lambda ctx: usos.append("A"))),
                LairAction("B", _Stub("B", lambda ctx: usos.append("B")))]
    owner = Monster(name="Dueño", max_hp=50, ac=10,
                    legendary=LegendaryState(lair_actions=acciones))
    enemigo = _enemigo()
    ctx = _ctx(owner, [owner, enemigo], rng=random.Random(2))
    for _ in range(20):
        lair_phase(ctx)
        ctx.round += 1
    assert all(a != b for a, b in zip(usos, usos[1:]))


def test_no_actua_si_el_combate_cae_en_medio():
    enemigo = _enemigo()
    usos: list[str] = []

    def _mata(ctx):
        usos.append("Mata")
        enemigo.hp = 0

    acciones = [LairAction("Mata", _Stub("Mata", _mata)),
                LairAction("Extra", _Stub("Extra",
                                          lambda ctx: usos.append("Extra")))]
    owner = Monster(name="Dueño", max_hp=50, ac=10,
                    legendary=LegendaryState(lair_actions=acciones))
    ctx = _ctx(owner, [owner, enemigo])
    lair_phase(ctx)
    assert usos == ["Mata"]  # la segunda no corre: el combate terminó


def test_no_actua_si_el_dueno_cae_o_no_puede_actuar():
    from dnd_sim.rules.conditions import Condition, apply_condition
    usos: list[str] = []
    acciones = [LairAction("A", _Stub("A", lambda ctx: usos.append("A")))]
    owner = Monster(name="Dueño", max_hp=50, ac=10,
                    legendary=LegendaryState(lair_actions=acciones))
    enemigo = _enemigo()
    ctx = _ctx(owner, [owner, enemigo])
    # can_act es property: la única forma de apagarla es incapacitar.
    apply_condition(owner, Condition.INCAPACITATED, ctx)
    lair_phase(ctx)
    assert usos == []
    owner.conditions.clear()
    owner.hp = 0                          # alive es property de hp
    lair_phase(ctx)
    assert usos == []


def test_no_gasta_recursos_ni_puntos_legendarios():
    recursos = TurnResources()
    acciones = [LairAction("A", _Stub("A"))]
    owner = Monster(
        name="Dueño", max_hp=50, ac=10,
        legendary=LegendaryState(lair_actions=acciones,
                                 points_max=3, points_left=3))
    enemigo = _enemigo()
    ctx = _ctx(owner, [owner, enemigo], resources=recursos)
    lair_phase(ctx)
    # Explícito 3 (no el default 4): la fase no toca los puntos.
    assert owner.legendary.points_left == 3
    assert not recursos.action_used
    assert not recursos.bonus_action_used


# --------------------------------------------------------- temporización

def _spy_turnos(monkeypatch, eventos: list[str]):
    """Registra cada turno en ``eventos`` vía el begin_turn del bucle."""
    original = encounter_mod.begin_turn

    def spy(actor, ctx):
        eventos.append(actor.name)
        return original(actor, ctx)

    monkeypatch.setattr(encounter_mod, "begin_turn", spy)


def test_timing_mezclado_tras_mayores_de_20(lairs_dir, monkeypatch):
    dragon = _dragon()
    pj1 = _pj("Pj1", hp=200, ac=30)
    pj2 = _pj("Pj2", hp=200, ac=30)
    eventos: list[str] = []
    monkeypatch.setattr(
        encounter_mod, "roll_initiative",
        _orden_con({pj1.name: 25, dragon.name: 20, pj2.name: 15}))
    monkeypatch.setattr(encounter_mod, "lair_phase",
                        lambda ctx: eventos.append("LAIR"))
    _spy_turnos(monkeypatch, eventos)

    run_combat([pj1, pj2, dragon], random.Random(3))
    # Iniciativa 20: tras todos los >= 20 y antes del primero con < 20.
    assert eventos[:4] == [pj1.name, dragon.name, "LAIR", pj2.name]


def test_timing_empate_en_20_es_perdido(lairs_dir, monkeypatch):
    dragon = _dragon()
    pj1 = _pj("Pj1", hp=200, ac=30)
    pj2 = _pj("Pj2", hp=200, ac=30)
    pj3 = _pj("Pj3", hp=200, ac=30)
    eventos: list[str] = []
    monkeypatch.setattr(
        encounter_mod, "roll_initiative",
        _orden_con({pj1.name: 25, dragon.name: 20, pj3.name: 20,
                    pj2.name: 15}))
    monkeypatch.setattr(encounter_mod, "lair_phase",
                        lambda ctx: eventos.append("LAIR"))
    _spy_turnos(monkeypatch, eventos)

    run_combat([pj1, pj2, pj3, dragon], random.Random(3))
    # Los dos empatados en 20 actúan ANTES que la guarida. El orden entre
    # ellos lo fija el fake (sorted estable: pj3 antes que dragon); lo que
    # garantiza la regla es que la guarida va tras AMBOS.
    assert eventos[:5] == [pj1.name, pj3.name, dragon.name, "LAIR",
                           pj2.name]


def test_timing_todas_las_iniciativas_menores_de_20(lairs_dir, monkeypatch):
    dragon = _dragon()
    pj1 = _pj("Pj1", hp=200, ac=30)
    pj2 = _pj("Pj2", hp=200, ac=30)
    eventos: list[str] = []
    monkeypatch.setattr(
        encounter_mod, "roll_initiative",
        _orden_con({pj1.name: 18, dragon.name: 12, pj2.name: 5}))
    monkeypatch.setattr(encounter_mod, "lair_phase",
                        lambda ctx: eventos.append("LAIR"))
    _spy_turnos(monkeypatch, eventos)

    run_combat([pj1, pj2, dragon], random.Random(3))
    # Ninguno llega a 20: la guarida abre la ronda.
    assert eventos[0] == "LAIR"


def test_timing_todas_las_iniciativas_de_20_o_mas(lairs_dir, monkeypatch):
    dragon = _dragon()
    pj1 = _pj("Pj1", hp=200, ac=30)
    pj2 = _pj("Pj2", hp=200, ac=30)
    eventos: list[str] = []
    monkeypatch.setattr(
        encounter_mod, "roll_initiative",
        _orden_con({pj1.name: 28, dragon.name: 22, pj2.name: 20}))
    monkeypatch.setattr(encounter_mod, "lair_phase",
                        lambda ctx: eventos.append("LAIR"))
    _spy_turnos(monkeypatch, eventos)

    run_combat([pj1, pj2, dragon], random.Random(3))
    # Todos >= 20: la guarida cierra la ronda.
    assert eventos[:4] == [pj1.name, dragon.name, pj2.name, "LAIR"]


# ------------------------------------------------------- magical y RNG

def test_guarida_pasa_magical_a_las_salvaciones(lairs_dir, monkeypatch):
    dragon = _dragon()
    llamadas: list[bool] = []
    original = saves_mod.saving_throw

    def spy(target, ability, dc, rng, mode=None, *, kind=None,
            magical=False, **kw):
        llamadas.append(bool(magical))
        return original(target, ability, dc, rng, mode, kind=kind,
                        magical=magical)

    monkeypatch.setattr(saves_mod, "saving_throw", spy)
    objetivo = _pj("Deva", hp=200, ac=30)
    ctx = _ctx(dragon, [dragon, objetivo])
    dragon.legendary.lair_actions[0].action.execute(ctx)   # magical: true
    assert llamadas and llamadas[-1] is True
    llamadas.clear()
    dragon.legendary.lair_actions[1].action.execute(ctx)   # magical: false
    assert llamadas and llamadas[-1] is False


def test_reproducibilidad_con_guarida(lairs_dir):
    def combate():
        dragon = _dragon()
        pj = _pj("Pj", hp=60)
        r = run_combat([pj, dragon], random.Random(42))
        return (r.winner, r.rounds, tuple(sorted(r.survivors.items())))

    assert combate() == combate()


# ----------------------------------------------------------- guardián

def test_puntos_siempre_incluyen_bonus_de_guarida(lairs_dir):
    # Política: siempre en guarida → points_max = base + 1.
    m = _dragon()
    assert m.legendary.points_max == 4
    m.legendary.points_left = 0
    m.legendary.refill_points()
    assert m.legendary.points_left == 4


def test_legendary_points_cli_fija_valor_final(lairs_dir):
    # --legendary-points N fija el valor final (sin sumar el bonus).
    import importlib.util
    raiz = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "main_cli_mod", raiz / "main.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    monstruos = mod._load_party(["adult-red-dragon"], legendary_points=7)
    assert monstruos[0].legendary.points_max == 7
    assert monstruos[0].legendary.points_left == 7


def test_sin_fichero_no_consume_rng(lairs_dir):
    # lich legendario sin data/lairs/lich.json: la fase corre pero no
    # elige nada y no gasta RNG.
    m = load_monster("lich")
    pj = _pj("Pj")
    rng = random.Random(3)
    ctx = _ctx(m, [m, pj], rng=rng)
    antes = rng.getstate()
    lair_phase(ctx)
    assert rng.getstate() == antes


def test_guardian_sin_interruptor_in_lair():
    # Nada en el repo (código y docs) puede hablar del interruptor.
    # Los patrones se construyen en tiempo de ejecución para que este
    # test no se encuentre a sí mismo.
    raiz = Path(__file__).resolve().parents[1]
    excl = ("graphify-out", ".venv", "cache", "__pycache__", ".git")
    patrones = ("in" + "_lair", "--" + "lair")
    hallados = []
    for path in raiz.rglob("*"):
        if path.suffix not in {".py", ".md", ".txt"}:
            continue
        if any(e in path.parts for e in excl):
            continue
        if path == Path(__file__):
            continue
        texto = path.read_text(encoding="utf-8", errors="ignore")
        for patron in patrones:
            if patron in texto:
                hallados.append(
                    f"{path.relative_to(raiz)}: contiene {patron!r}")
    assert not hallados, hallados


def test_guardian_sintetica_en_tests_y_repo_sin_datos():
    # El fichero sintético vive solo en tests/.
    assert (FIXTURES / "adult-red-dragon.json").exists()
    # El repo no tiene datos reales de guaridas todavía (los aporta el
    # maintainer en data/lairs/ y NO cuentan como monstruo definido a mano).
    repo_lairs = Path(data_pkg.__file__).parent / "lairs"
    assert not repo_lairs.exists() or not any(repo_lairs.glob("*.json"))
    # El loader de guaridas no define estadísticas de monstruos.
    fuente = Path(lair_loader.__file__).read_text(encoding="utf-8")
    assert "max_hp" not in fuente
    assert "hit_points" not in fuente

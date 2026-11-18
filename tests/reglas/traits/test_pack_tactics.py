"""Pack Tactics del lobo (rasgo con condición de posición).

La ficha pide «aliado no incapacitado a menos de 5 pies del objetivo», y el
motor no modela la posición: **si el atacante tiene aliados capaces** se
sortea al azar si se cumple (50 %), y **si no tiene ninguno nunca aplica**.
Además, sin contexto (o sin RNG) el rasgo no decide nada, así que una
llamada directa a ``attack_modifiers`` no altera ninguna tirada.
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, Monster, PlayerCharacter
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.model.attack import Attack
from dnd_sim.engine.combat import run_combat
from dnd_sim.rules.conditions import Condition, apply_condition
from dnd_sim.data.loader import load_monster
from dnd_sim.core.dice import RollMode
from dnd_sim.rules.roll_modifiers import AttackRange, attack_modifiers

FIXTURES = Path(__file__).parents[2] / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _datos(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _lobo(monkeypatch):
    data = _datos("wolf")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("wolf")


def _mordisco(lobo) -> Attack:
    return next(a for a in lobo.attacks if a.name == "Bite")


def _pj(hp: int = 40) -> PlayerCharacter:
    return PlayerCharacter(
        name="Guerrero", max_hp=hp, ac=15, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[],
    )


def _aliado() -> Monster:
    """Otro NPC vivo: aliado del lobo y no hostil para él."""
    return Monster(name="Compañero", max_hp=20, ac=12,
                   abilities=Abilities(), attacks=[])


def _ctx(actor, combatantes, semilla: int = 1) -> CombatContext:
    return CombatContext(rng=random.Random(semilla), actor=actor,
                         combatants=list(combatantes), round=1,
                         log=[], verbose=True, resources=TurnResources())


def _mods_con_estado(lobo, objetivo, aliados, semilla: int = 1):
    """Modo del ataque y si la llamada ha consumido RNG.

    Comprueba las dos cosas que definen a estos rasgos: qué modo salen y
    si el sorteo de la posición se ha llevado por delante dados.
    """
    ctx = _ctx(lobo, [lobo, *aliados, objetivo], semilla)
    rng = ctx.rng
    antes = rng.getstate()
    mods = attack_modifiers(lobo, objetivo, _mordisco(lobo), AttackRange.MELEE,
                            ctx=ctx, rng=rng)
    return mods, rng.getstate() != antes


# --- Carga de la ficha ------------------------------------------------------ #

def test_el_lobo_carga_su_pack_tactics(monkeypatch):
    lobo = _lobo(monkeypatch)
    # Keen Hearing and Smell se ignora por decisión (no entra en la simulación).
    assert [type(t).__name__ for t in lobo.traits] == ["PackTactics"]
    assert lobo.traits[0].name == "Pack Tactics"
    assert "allies" in lobo.traits[0].desc


# --- Reglas ----------------------------------------------------------------- #

def test_con_aliados_la_ventaja_se_sortea(monkeypatch):
    lobo = _lobo(monkeypatch)
    objetivo = _pj()
    aliado = _aliado()
    ventajas = 0
    fuentes: set = set()
    se_sortea = False
    for semilla in range(40):
        mods, consumo = _mods_con_estado(lobo, objetivo, [aliado], semilla)
        se_sortea = se_sortea or consumo
        if mods.mode is RollMode.ADVANTAGE:
            ventajas += 1
            fuentes.update(mods.advantage_sources)
    # 50 % con aliados: en 40 tiradas tienen que salir ambas cosas.
    assert 0 < ventajas < 40, f"se esperaban resultados mixtos: {ventajas}"
    assert fuentes == {"Pack Tactics"}
    assert se_sortea, "con aliados la posición se sortea (consume RNG)"


def test_sin_aliados_no_hay_sorteo_ni_ventaja(monkeypatch):
    lobo = _lobo(monkeypatch)
    objetivo = _pj()
    # Solo el objetivo en el combate: el lobo va solo.
    mods, consumo = _mods_con_estado(lobo, objetivo, [], semilla=3)
    assert mods.mode is RollMode.NORMAL
    assert mods.advantage_sources == []
    assert not consumo, "sin aliados no se consume RNG"


def test_un_aliado_incapacitado_no_cuenta(monkeypatch):
    """La ficha exige «the ally isn't incapacitated»."""
    lobo = _lobo(monkeypatch)
    objetivo = _pj()
    aliado = _aliado()
    ctx = _ctx(lobo, [lobo, aliado, objetivo], 5)
    apply_condition(aliado, Condition.INCAPACITATED, ctx)
    rng = ctx.rng
    antes = rng.getstate()
    mods = attack_modifiers(lobo, objetivo, _mordisco(lobo), AttackRange.MELEE,
                            ctx=ctx, rng=rng)
    assert mods.mode is RollMode.NORMAL
    assert rng.getstate() == antes


def test_un_aliado_muerto_no_cuenta(monkeypatch):
    lobo = _lobo(monkeypatch)
    objetivo = _pj()
    aliado = _aliado()
    aliado.hp = 0
    mods, consumo = _mods_con_estado(lobo, objetivo, [aliado], semilla=7)
    assert mods.mode is RollMode.NORMAL
    assert not consumo


def test_sin_contexto_el_rasgo_no_decide_nada(monkeypatch):
    """Llamar a attack_modifiers sin ctx/rng no altera la tirada."""
    lobo = _lobo(monkeypatch)
    objetivo = _pj()
    objetivo.hp = 20                 # herido: si hubiera otros rasgos, veríamos
    mods = attack_modifiers(lobo, objetivo, _mordisco(lobo), AttackRange.MELEE)
    assert mods.mode is RollMode.NORMAL
    assert mods.advantage_sources == []


# --- Integración con el motor ----------------------------------------------- #

def test_pack_tactics_actua_en_un_combate_completo(monkeypatch):
    lobo = _lobo(monkeypatch)
    lobo2 = _lobo(monkeypatch)
    objetivo = _pj(hp=200)
    res = run_combat([lobo, lobo2, objetivo], random.Random(4), verbose=True,
                     max_rounds=6)
    assert any("Pack Tactics" in linea for linea in res.log), \
        "con dos lobos, alguno de sus ataques debe ser con ventaja"

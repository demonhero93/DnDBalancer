"""Invisibility del duergar: invisible = desventaja al ser atacado.

La condición «invisible» salió del catálogo de no modeladas (ocultación)
y pasa a modelarse como desventaja para quien ataque al invisible
(adaptación de la mecánica al simulador; la ventaja propia del invisible
al atacar aún no se modela). El estado termina cuando el invisible ataca
(«until it attacks») y la acción es de uso limitado (1 por combate).

Todas las fichas salen de fixtures reales de la API.
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, PlayerCharacter
from dnd_sim.actions import CombatContext, TurnResources
from dnd_sim.attack import Attack
from dnd_sim.combat import attack_roll, run_combat
from dnd_sim.combatant import Monster
from dnd_sim.conditions import (CONDITION_LABELS, EXCLUDED_CONDITIONS,
                                Condition, apply_condition)
from dnd_sim.data.loader import load_monster
from dnd_sim.dice import RollMode
from dnd_sim.roll_modifiers import attack_modifiers
from dnd_sim.spells import SpellStateAction
from dnd_sim.usage import UsageKind

FIXTURES = Path(__file__).parent / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _datos(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _duergar(monkeypatch) -> Monster:
    data = _datos("duergar")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("duergar")


def _pj(name: str = "Guerrero", hp: int = 60, ac: int = 15) -> PlayerCharacter:
    return PlayerCharacter(
        name=name, max_hp=hp, ac=ac, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[Attack(name="Espada", damage="1d8", ability="str",
                        attack_bonus=5, damage_bonus=3)],
    )


def _ctx(actor, combatants, rng=None, log=None) -> CombatContext:
    return CombatContext(rng=rng or random.Random(1), actor=actor,
                         combatants=list(combatants), round=1,
                         log=log if log is not None else [], verbose=True,
                         resources=TurnResources())


def _accion(m, nombre):
    return next(a for a in m.actions if getattr(a, "name", "") == nombre)


def _ataque(m, nombre):
    return next(a for a in m.attacks if a.name == nombre)


# --- Carga del duergar ------------------------------------------------------ #

def test_el_duergar_carga_su_invisibility_como_accion_de_estado(monkeypatch):
    duergar = _duergar(monkeypatch)
    invis = _accion(duergar, "Invisibility")
    assert isinstance(invis, SpellStateAction)
    assert invis.effect.condition is Condition.INVISIBLE
    # «Until it attacks»: duración por evento, no por rondas.
    assert invis.effect.duration_rounds is None
    assert invis.effect.target == "self"
    # «recharge after rest»: un uso por combate.
    assert invis.usage.kind is UsageKind.PER_DAY
    assert invis.usage.uses_left == 1


def test_invisible_es_una_condicion_modelada():
    assert Condition.INVISIBLE.value == "invisible"
    assert "invisible" not in EXCLUDED_CONDITIONS
    assert CONDITION_LABELS[Condition.INVISIBLE] == "invisible"


# --- El estado -------------------------------------------------------------- #

def test_ejecutar_invisibility_aplica_el_estado(monkeypatch):
    duergar = _duergar(monkeypatch)
    objetivo = _pj()
    ctx = _ctx(duergar, [duergar, objetivo])
    _accion(duergar, "Invisibility").execute(ctx)
    assert duergar.conditions.has(Condition.INVISIBLE)
    assert any("queda invisible" in l for l in ctx.log)


# --- Desventaja al ser atacado ---------------------------------------------- #

def test_atacar_a_un_invisible_tiene_desventaja():
    atacante = _pj(name="Atacante")
    invisible = _pj(name="Invisible")
    apply_condition(invisible, Condition.INVISIBLE, _ctx(invisible, []),
                    duration_rounds=None)
    mods = attack_modifiers(atacante, invisible, atacante.attacks[0])
    assert mods.mode is RollMode.DISADVANTAGE
    assert "objetivo invisible" in mods.disadvantage_sources


def test_sin_invisible_no_hay_desventaja():
    atacante = _pj(name="Atacante")
    objetivo = _pj(name="Objetivo")
    mods = attack_modifiers(atacante, objetivo, atacante.attacks[0])
    assert mods.mode is RollMode.NORMAL


def test_ventaja_y_desventaja_de_invisible_y_derribado_se_cancelan():
    atacante = _pj(name="Atacante")
    objetivo = _pj(name="Objetivo")
    ctx = _ctx(objetivo, [atacante, objetivo])
    apply_condition(objetivo, Condition.INVISIBLE, ctx, duration_rounds=None)
    apply_condition(objetivo, Condition.PRONE, ctx, duration_rounds=None)
    # Derribado a cuerpo a cuerpo da ventaja; invisible, desventaja.
    mods = attack_modifiers(atacante, objetivo, atacante.attacks[0])
    assert mods.mode is RollMode.NORMAL


# --- Termina al atacar ------------------------------------------------------ #

def test_atacar_deja_de_ser_invisible(monkeypatch):
    duergar = _duergar(monkeypatch)
    objetivo = _pj()
    ctx = _ctx(duergar, [duergar, objetivo])
    apply_condition(duergar, Condition.INVISIBLE, ctx, duration_rounds=None)
    ctx.log.clear()
    # Semilla 5: primer d20 = 20 (impacto garantizado; da igual: «until it
    # attacks» lo pierde aunque falle).
    attack_roll(duergar, objetivo, _ataque(duergar, "War Pick"),
                random.Random(5), ctx.log, ctx=ctx)
    assert not duergar.conditions.has(Condition.INVISIBLE)
    assert any("deja de estar invisible (ataca)" in l for l in ctx.log)


def test_el_duergar_visible_no_pierde_nada_al_atacar(monkeypatch):
    duergar = _duergar(monkeypatch)
    objetivo = _pj()
    ctx = _ctx(duergar, [duergar, objetivo])
    attack_roll(duergar, objetivo, _ataque(duergar, "War Pick"),
                random.Random(5), ctx.log, ctx=ctx)
    assert not any("invisible" in l for l in ctx.log)


# --- Integración con el motor ----------------------------------------------- #

def test_un_combate_completo_usa_invisibility(monkeypatch):
    duergar = _duergar(monkeypatch)
    pjs = [_pj(name="A"), _pj(name="B")]
    res = run_combat([*pjs, duergar], random.Random(5), verbose=True,
                     max_rounds=20)
    assert any("queda invisible" in l for l in res.log), \
        "el duergar debe poder volverse invisible en combate"

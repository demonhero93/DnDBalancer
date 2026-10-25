"""Invisibility del duergar: invisible = ventaja al atacar y desventaja al ser atacado.

La condición «invisible» salió del catálogo de no modeladas (ocultación)
y pasa a modelarse en los dos sentidos de la 5e: da **ventaja** al propio
invisible cuando ataca y **desventaja** a quien lo ataca. El estado
termina cuando el invisible ataca («until it attacks») o cuando lanza un
hechizo —incluido su propio Enlarge/Reduce—, pero ese primer ataque ya se
resuelve con ventaja (en attack_roll la invisibilidad se quita después de
calcular el modo). La acción es de uso limitado (1 por combate).

Todas las fichas salen de fixtures reales de la API.
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, PlayerCharacter
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.model.attack import Attack
from dnd_sim.engine.combat import attack_roll, run_combat
from dnd_sim.model.combatant import Monster
from dnd_sim.rules.conditions import (
    CONDITION_LABELS, EXCLUDED_CONDITIONS, Condition, apply_condition
)
from dnd_sim.data.loader import load_monster
from dnd_sim.core.dice import RollMode
from dnd_sim.rules.roll_modifiers import attack_modifiers
from dnd_sim.rules.spells import SpellFixedDamageAction, SpellStateAction
from dnd_sim.rules.usage import UsageKind

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


# --- Ventaja al atacar ------------------------------------------------------ #

def test_atacar_siendo_invisible_da_ventaja():
    atacante = _pj(name="Atacante")
    objetivo = _pj(name="Objetivo")
    apply_condition(atacante, Condition.INVISIBLE, _ctx(atacante, []),
                    duration_rounds=None)
    mods = attack_modifiers(atacante, objetivo, atacante.attacks[0])
    assert mods.mode is RollMode.ADVANTAGE
    assert "atacante invisible" in mods.advantage_sources


def test_dos_invisibles_se_atacan_con_normalidad():
    # El atacante invisible tiene ventaja; el objetivo invisible da
    # desventaja. Los dos efectos se anulan -> tirada normal.
    atacante = _pj(name="Atacante")
    objetivo = _pj(name="Objetivo")
    ctx = _ctx(objetivo, [atacante, objetivo])
    apply_condition(atacante, Condition.INVISIBLE, ctx, duration_rounds=None)
    apply_condition(objetivo, Condition.INVISIBLE, ctx, duration_rounds=None)
    mods = attack_modifiers(atacante, objetivo, atacante.attacks[0])
    assert mods.mode is RollMode.NORMAL


def test_el_primer_ataque_del_invisible_usa_ventaja_y_luego_pierde_la_invisibilidad(monkeypatch):
    # El ataque que rompe la invisibilidad se resuelve con ventaja y, tras
    # él, el atacante ya no está invisible.
    duergar = _duergar(monkeypatch)
    objetivo = _pj()
    ctx = _ctx(duergar, [duergar, objetivo])
    apply_condition(duergar, Condition.INVISIBLE, ctx, duration_rounds=None)

    import dnd_sim.engine.combat as combat_mod
    original = combat_mod.roll_d20
    modos = []

    def espia(rng, mode=RollMode.NORMAL, **kw):
        modos.append(mode)
        return original(rng, mode, **kw)

    monkeypatch.setattr(combat_mod, "roll_d20", espia)
    ctx.log.clear()
    attack_roll(duergar, objetivo, _ataque(duergar, "War Pick"),
                random.Random(5), ctx.log, ctx=ctx)
    # El modo de la tirada fue de ventaja...
    assert modos and modos[0] is RollMode.ADVANTAGE
    # ...y tras el ataque dejó de estar invisible.
    assert not duergar.conditions.has(Condition.INVISIBLE)


def test_el_segundo_ataque_del_duergar_ya_no_tiene_ventaja(monkeypatch):
    # Rompida la invisibilidad, un ataque posterior es normal.
    duergar = _duergar(monkeypatch)
    objetivo = _pj(hp=200)
    ctx = _ctx(duergar, [duergar, objetivo])
    apply_condition(duergar, Condition.INVISIBLE, ctx, duration_rounds=None)

    import dnd_sim.engine.combat as combat_mod
    original = combat_mod.roll_d20
    modos = []

    def espia(rng, mode=RollMode.NORMAL, **kw):
        modos.append(mode)
        return original(rng, mode, **kw)

    monkeypatch.setattr(combat_mod, "roll_d20", espia)
    atk = _ataque(duergar, "War Pick")
    attack_roll(duergar, objetivo, atk, random.Random(5), ctx.log, ctx=ctx)
    attack_roll(duergar, objetivo, atk, random.Random(9), ctx.log, ctx=ctx)
    assert modos[0] is RollMode.ADVANTAGE   # el que rompió la invisibilidad
    assert modos[1] is RollMode.NORMAL      # el siguiente, ya visible


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


# --- Termina al lanzar un hechizo ------------------------------------------- #

def test_usar_enlarge_rompe_la_invisibilidad(monkeypatch):
    # «[Invisibility] ends if ... the duergar uses its Enlarge/Reduce
    # ability»: al agrandarse pierde la invisibilidad.
    duergar = _duergar(monkeypatch)
    ctx = _ctx(duergar, [duergar])
    apply_condition(duergar, Condition.INVISIBLE, ctx, duration_rounds=None)
    ctx.log.clear()
    _accion(duergar, "Enlarge").execute(ctx)
    assert not duergar.conditions.has(Condition.INVISIBLE)
    assert duergar.conditions.has(Condition.ENLARGED)
    assert any("deja de estar invisible (lanza un hechizo)" in l
               for l in ctx.log)


def test_refrescar_invisibility_no_deja_al_duergar_visible(monkeypatch):
    # Lanzar Invisibility estando ya invisible lo refresca: termina la
    # anterior y aplica la nueva, así que sigue invisible.
    duergar = _duergar(monkeypatch)
    ctx = _ctx(duergar, [duergar])
    apply_condition(duergar, Condition.INVISIBLE, ctx, duration_rounds=None)
    _accion(duergar, "Invisibility").execute(ctx)
    assert duergar.conditions.has(Condition.INVISIBLE)


def test_lanzar_un_hechizo_de_dano_rompe_la_invisibilidad():
    # La regla es general a toda acción de hechizo, no solo a Enlarge:
    # un hechizo de daño también rompe la invisibilidad del lanzador.
    lanzador = _pj(name="Lanzador")
    objetivo = _pj(name="Objetivo")
    ctx = _ctx(lanzador, [lanzador, objetivo])
    apply_condition(lanzador, Condition.INVISIBLE, ctx, duration_rounds=None)
    ctx.log.clear()
    SpellFixedDamageAction(name="Proyectil Mágico", damage="1d4",
                           elements=1).execute(ctx)
    assert not lanzador.conditions.has(Condition.INVISIBLE)
    assert any("deja de estar invisible (lanza un hechizo)" in l
               for l in ctx.log)


def test_lanzar_un_hechizo_sin_invisibilidad_no_registra_nada(monkeypatch):
    duergar = _duergar(monkeypatch)
    ctx = _ctx(duergar, [duergar])
    ctx.log.clear()
    _accion(duergar, "Enlarge").execute(ctx)
    # No estaba invisible: no debe aparecer ninguna línea al respecto.
    assert not any("invisible" in l for l in ctx.log)


# --- Integración con el motor ----------------------------------------------- #

def test_un_combate_completo_usa_invisibility(monkeypatch):
    duergar = _duergar(monkeypatch)
    pjs = [_pj(name="A"), _pj(name="B")]
    res = run_combat([*pjs, duergar], random.Random(5), verbose=True,
                     max_rounds=20)
    assert any("queda invisible" in l for l in res.log), \
        "el duergar debe poder volverse invisible en combate"

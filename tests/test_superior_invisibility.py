"""Superior Invisibility de la pixie: invisible que no se pierde al atacar.

La ficha de la pixie no está ni en la caché de la API ni en dnd5eapi.co, así
que el rasgo se prueba con el texto del SRD. Difiere del hechizo
Invisibility en lo importante: «until its concentration ends», no «until it
attacks or casts a spell». Por eso la condición se aplica con
``break_on_attack=False`` y sobrevive a un ataque y a lanzar hechizos.

Como la ficha la trae como acción de la criatura (el motor solo construye
acciones desde el campo ``actions``), el rasgo la aporta con el hook
``extra_actions``, que ``Monster`` consulta al construirse.
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, Monster, PlayerCharacter
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.model.attack import Attack
from dnd_sim.engine.combat import attack_roll, run_combat
from dnd_sim.rules.conditions import (
    Condition, apply_condition, remove_invisibility_on_action
)
from dnd_sim.data.trait_parser import parse_traits
from dnd_sim.core.dice import RollMode
from dnd_sim.rules.spells import SpellFixedDamageAction, SpellStateAction
from dnd_sim.rules.traits import SuperiorInvisibility

# Texto real del SRD (la API no sirve «pixie»).
PIXIE_SRD = (
    "The pixie magically turns invisible until its concentration ends (as "
    "if concentrating on a spell). Any equipment the pixie wears or carries "
    "is invisible with it."
)


# --- Utilidades ------------------------------------------------------------- #

def _pixie() -> Monster:
    rasgo = parse_traits({"special_abilities": [
        {"name": "Superior Invisibility", "desc": PIXIE_SRD},
    ]})[0]
    return Monster(
        name="Pixie", max_hp=5, ac=14, proficiency=2,
        abilities=Abilities(str=3, dex=18, con=10, int=12, wis=15, cha=14),
        attacks=[Attack(name="Daga", damage="1d4", ability="dex",
                        attack_bonus=6, damage_bonus=4)],
        traits=[rasgo],
    )


def _pj() -> PlayerCharacter:
    return PlayerCharacter(
        name="Guerrero", max_hp=60, ac=15, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[Attack(name="Espada", damage="1d8", ability="str",
                        attack_bonus=5, damage_bonus=3)],
    )


def _ctx(actor, combatantes, semilla: int = 1) -> CombatContext:
    return CombatContext(rng=random.Random(semilla), actor=actor,
                         combatants=list(combatantes), round=1, log=[],
                         verbose=True, resources=TurnResources())


def _accion(monstruo, nombre: str):
    return next(a for a in monstruo.actions
                if getattr(a, "name", "") == nombre)


# --- Carga y acción --------------------------------------------------------- #

def test_el_rasgo_se_parsea_desde_el_srd():
    rasgo = parse_traits({"special_abilities": [
        {"name": "Superior Invisibility", "desc": PIXIE_SRD},
    ]})[0]
    assert isinstance(rasgo, SuperiorInvisibility)
    assert rasgo.name == "Superior Invisibility"


def test_el_monstruo_recibe_su_accion_al_construirse():
    pixie = _pixie()
    accion = _accion(pixie, "Superior Invisibility")
    assert isinstance(accion, SpellStateAction)
    assert accion.effect.condition is Condition.INVISIBLE
    # Hasta que acabe la concentración: duración por evento, no por rondas.
    assert accion.effect.duration_rounds is None
    assert accion.effect.target == "self"
    # «ends if the target attacks or casts a spell» NO aplica aquí.
    assert accion.effect.break_on_attack is False
    # Es una acción a voluntad, como en la ficha.
    assert accion.usage is None


def test_ejecutarla_aplica_el_estado():
    pixie = _pixie()
    ctx = _ctx(pixie, [pixie])
    _accion(pixie, "Superior Invisibility").execute(ctx)
    assert pixie.conditions.has(Condition.INVISIBLE)
    assert any("queda invisible" in l for l in ctx.log)


# --- Diferencia con el hechizo Invisibility --------------------------------- #

def test_atacar_con_ventaja_y_no_pierde_la_invisibilidad(monkeypatch):
    # El ataque sale con ventaja y, a diferencia del duergar, la
    # invisibilidad se queda: «until its concentration ends».
    pixie = _pixie()
    objetivo = _pj()
    ctx = _ctx(pixie, [pixie, objetivo])
    _accion(pixie, "Superior Invisibility").execute(ctx)

    import dnd_sim.engine.combat as combat_mod
    original = combat_mod.roll_d20
    modos = []

    def espia(rng, mode=RollMode.NORMAL, **kw):
        modos.append(mode)
        return original(rng, mode, **kw)

    monkeypatch.setattr(combat_mod, "roll_d20", espia)
    ctx.log.clear()
    attack_roll(pixie, objetivo, pixie.attacks[0], random.Random(5),
                ctx.log, ctx=ctx)
    assert modos and modos[0] is RollMode.ADVANTAGE
    assert pixie.conditions.has(Condition.INVISIBLE)
    assert not any("deja de estar invisible" in l for l in ctx.log)


def test_lanzar_un_hechizo_tampoco_la_pierde():
    pixie = _pixie()
    objetivo = _pj()
    ctx = _ctx(pixie, [pixie, objetivo])
    _accion(pixie, "Superior Invisibility").execute(ctx)
    ctx.log.clear()
    SpellFixedDamageAction(name="Proyectil Mágico", damage="1d4",
                           elements=1).execute(ctx)
    assert pixie.conditions.has(Condition.INVISIBLE)
    assert not any("deja de estar invisible" in l for l in ctx.log)


def test_no_se_ofrece_si_ya_es_invisible():
    # Una vez invisible ya no se pierde, así que re-aplicarla no haría nada
    # y solo gastaría la acción: can_use deja de ofrecerla.
    pixie = _pixie()
    ctx = _ctx(pixie, [pixie])
    accion = _accion(pixie, "Superior Invisibility")
    resources = TurnResources()
    assert accion.can_use(resources, ctx)
    accion.execute(ctx)
    assert not accion.can_use(resources, ctx)


def test_remove_invisibility_on_action_respeta_el_flag():
    objetivo = _pj()
    ctx = _ctx(objetivo, [objetivo])
    # La estándar (por defecto) sí termina al atacar...
    apply_condition(objetivo, Condition.INVISIBLE, ctx, duration_rounds=None)
    assert remove_invisibility_on_action(objetivo) is True
    assert not objetivo.conditions.has(Condition.INVISIBLE)
    # ...la Superior, no.
    apply_condition(objetivo, Condition.INVISIBLE, ctx, duration_rounds=None,
                    break_on_attack=False)
    assert remove_invisibility_on_action(objetivo) is False
    assert objetivo.conditions.has(Condition.INVISIBLE)


# --- Integración con el motor ----------------------------------------------- #

def test_un_combate_completo_puede_volverse_invisible():
    # Política aleatoria: se prueban semillas hasta que elige la acción.
    for semilla in range(1, 21):
        pixie = _pixie()
        res = run_combat([_pj(), pixie], random.Random(semilla), verbose=True,
                         max_rounds=20)
        if any("queda invisible" in l for l in res.log):
            return
    raise AssertionError(
        "en algún combate debe elegir su acción de invisibilidad")

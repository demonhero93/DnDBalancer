"""Relentless del jabalí: un daño pequeño no lo deja caer.

La ficha (fixture real de la API) dice dos cosas: si el daño que lo dejaría
a 0 no pasa de 7, queda a 1 PV; y lo trae con ``usage`` «recharge after
rest», que en el motor (sin descansos) es un **uso por combate**. A
diferencia de Regeneration no decide en su propio turno: el daño se
resuelve al instante (hook ``on_reduced_to_zero_hp``).
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, Monster, PlayerCharacter
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.model.attack import Attack
from dnd_sim.engine.combat import run_combat
from dnd_sim.data.loader import load_monster
from dnd_sim.data.trait_parser import parse_traits
from dnd_sim.rules.damage import inflict_damage
from dnd_sim.rules.traits import Relentless
from dnd_sim.rules.usage import UsageKind

FIXTURES = Path(__file__).parent / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _datos(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _jabali(monkeypatch) -> Monster:
    data = _datos("boar")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("boar")


def _ctx(actor, combatantes, semilla: int = 1) -> CombatContext:
    return CombatContext(rng=random.Random(semilla), actor=actor,
                         combatants=list(combatantes), round=1, log=[],
                         verbose=True, resources=TurnResources())


def _pj() -> PlayerCharacter:
    """Con 1d4 de daño nunca supera el umbral de 7."""
    return PlayerCharacter(
        name="Guerrero", max_hp=60, ac=15, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[Attack(name="Daga", damage="1d4", ability="str",
                        attack_bonus=5, damage_bonus=0)],
    )


# --- Carga de la ficha ------------------------------------------------------ #

def test_el_jabali_carga_su_relentless_con_umbral_y_uso(monkeypatch):
    jabali = _jabali(monkeypatch)
    # Charge no está modelado: solo Relentless.
    assert [type(t).__name__ for t in jabali.traits] == ["Relentless"]
    rasgo = jabali.traits[0]
    assert rasgo.name == "Relentless"
    # «takes 7 damage or less» sale de la descripción...
    assert rasgo.threshold == 7
    # ...y «recharge after rest» es un uso por combate.
    assert rasgo.usage.kind is UsageKind.PER_DAY
    assert rasgo.usage.uses_max == 1
    assert rasgo.usage.uses_left == 1


def test_el_umbral_se_saca_de_cada_descripcion():
    # El jabalí gigante declara 10: el rasgo no trae el número escrito.
    rasgo = parse_traits({"special_abilities": [{
        "name": "Relentless",
        "desc": ("If the boar takes 10 damage or less that would reduce it "
                 "to 0 hit points, it is reduced to 1 hit point instead."),
    }]})[0]
    assert isinstance(rasgo, Relentless)
    assert rasgo.threshold == 10


def test_una_descripcion_no_interpretable_no_hace_nada():
    rasgo = parse_traits({"special_abilities": [
        {"name": "Relentless", "desc": "Se resiste con orgullo."},
    ]})[0]
    assert rasgo.threshold == 0
    jabali = Monster(name="Jabalí", max_hp=11, ac=11, attacks=[],
                     abilities=Abilities(str=13), traits=[rasgo])
    jabali.hp = 7
    ctx = _ctx(jabali, [jabali])
    ctx.log.clear()
    inflict_damage(jabali, 7, "piercing", ctx=ctx)
    assert jabali.hp == 0, "sin umbral legible el rasgo no hace nada"
    assert not jabali.alive
    assert not any("se mantiene en pie" in l for l in ctx.log)


# --- Reglas ----------------------------------------------------------------- #

def test_un_danyo_dentro_del_umbral_lo_deja_a_un_pv(monkeypatch):
    jabali = _jabali(monkeypatch)
    jabali.hp = 7
    ctx = _ctx(jabali, [jabali])
    ctx.log.clear()
    inflict_damage(jabali, 7, "piercing", ctx=ctx)
    assert jabali.hp == 1, "7 daño no lo deja caer"
    assert jabali.alive
    assert any("se mantiene en pie" in l and "Relentless" in l
               for l in ctx.log)
    assert not jabali.traits[0].usage.available, "gasta su único uso"


def test_un_danyo_que_supera_el_umbral_lo_mata(monkeypatch):
    jabali = _jabali(monkeypatch)
    jabali.hp = 7
    ctx = _ctx(jabali, [jabali])
    ctx.log.clear()
    inflict_damage(jabali, 8, "piercing", ctx=ctx)
    assert jabali.hp == -1
    assert not jabali.alive
    assert not any("se mantiene en pie" in l for l in ctx.log)


def test_solo_puede_salvarse_una_vez_por_combate(monkeypatch):
    jabali = _jabali(monkeypatch)
    ctx = _ctx(jabali, [jabali])
    jabali.hp = 7
    inflict_damage(jabali, 7, "piercing", ctx=ctx)
    assert jabali.hp == 1
    # El uso ya está gastado: la siguiente caída sí lo mata.
    inflict_damage(jabali, 1, "piercing", ctx=ctx)
    assert jabali.hp == 0
    assert not jabali.alive


def test_reset_reestablece_el_umbral_y_los_usos(monkeypatch):
    jabali = _jabali(monkeypatch)
    ctx = _ctx(jabali, [jabali])
    jabali.hp = 7
    inflict_damage(jabali, 7, "piercing", ctx=ctx)
    assert not jabali.traits[0].usage.available
    jabali.reset()
    assert jabali.hp == jabali.max_hp
    assert jabali.traits[0].usage.available, "cada combate empieza con su uso"


def test_relentless_no_necesita_contexto_ni_rng(monkeypatch):
    # Relentless no necesita tiradas: funciona también sin ctx (a diferencia
    # de Undead Fortitude, que se abstendría sin generador).
    jabali = _jabali(monkeypatch)
    jabali.hp = 7
    inflict_damage(jabali, 7, "piercing")
    assert jabali.hp == 1


# --- Integración con el motor ----------------------------------------------- #

def test_un_combate_completo_usa_relentless(monkeypatch):
    jabali = _jabali(monkeypatch)
    pj = _pj()
    res = run_combat([pj, jabali], random.Random(3), verbose=True,
                     max_rounds=30)
    assert not jabali.alive, "el jabalí debe acabar muriendo"
    assert any("se mantiene en pie" in l for l in res.log), \
        "su primer golpe letal debe quedar en 1 PV"

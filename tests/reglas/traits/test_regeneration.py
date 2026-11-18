"""Regeneration del troll (rasgo de ficha con estado por turno).

La ficha (fixture real de la API) dice tres cosas: recupera 10 PV al
inicio de su turno, no lo hace si ha recibido ácido o fuego, y muere si
empieza su turno con 0 PV (a 0 PV no se regenera). Cada frase es un hook
distinto de :mod:`dnd_sim.rules.traits`.
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, PlayerCharacter
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.model.attack import Attack
from dnd_sim.engine.combat import run_combat
from dnd_sim.data.loader import load_monster
from dnd_sim.rules.damage import inflict_damage
from dnd_sim.rules.usage import begin_turn

FIXTURES = Path(__file__).parents[2] / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _datos(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _troll(monkeypatch):
    data = _datos("troll")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("troll")


def _pj(hp: int = 300) -> PlayerCharacter:
    return PlayerCharacter(
        name="Guerrero", max_hp=hp, ac=16, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[Attack(name="Espada", damage="1d8", ability="str",
                        attack_bonus=5, damage_bonus=3)],
    )


def _ctx(actor, combatantes) -> CombatContext:
    return CombatContext(rng=random.Random(1), actor=actor,
                         combatants=list(combatantes), round=1,
                         log=[], verbose=True, resources=TurnResources())


# --- Carga de la ficha ------------------------------------------------------ #

def test_el_troll_carga_su_regeneracion(monkeypatch):
    troll = _troll(monkeypatch)
    assert [type(t).__name__ for t in troll.traits] == ["Regeneration"]
    rasgo = troll.traits[0]
    assert rasgo.name == "Regeneration"
    # La cantidad sale de la descripción («regains 10 hit points»).
    assert rasgo.amount == 10


def test_otros_monstruos_con_regeneracion_usan_su_propia_cantidad():
    # El parser es el mismo para todos: lo que cambia es la descripción.
    from dnd_sim.data.trait_parser import parse_traits
    oni = parse_traits({"special_abilities": [
        {"name": "Regeneration",
         "desc": "The oni regains 10 hit points at the start of its turn."},
    ]})
    assert oni[0].amount == 10
    otro = parse_traits({"special_abilities": [
        {"name": "Regeneration",
         "desc": "The creature regains 5 hit points at the start of its turn."},
    ]})
    assert otro[0].amount == 5
    # Sin texto interpretable el rasgo no cura (pero no rompe nada).
    sin_texto = parse_traits({"special_abilities": [
        {"name": "Regeneration", "desc": "Se cura."},
    ]})
    assert sin_texto[0].amount == 0


# --- Reglas ----------------------------------------------------------------- #

def test_la_regeneracion_cura_10_pv_al_inicio_del_turno(monkeypatch):
    troll = _troll(monkeypatch)
    troll.hp = 20
    ctx = _ctx(troll, [troll])
    begin_turn(troll, ctx)
    assert troll.hp == 30
    assert any("regenera 10 PV" in linea for linea in ctx.log)


def test_la_regeneracion_no_pasa_de_los_pv_maximos(monkeypatch):
    troll = _troll(monkeypatch)
    troll.hp = troll.max_hp - 3
    ctx = _ctx(troll, [troll])
    begin_turn(troll, ctx)
    assert troll.hp == troll.max_hp
    # Sin heridas no hay línea de regeneración (no hay nada que curar).
    begin_turn(troll, _ctx(troll, [troll]))
    assert troll.hp == troll.max_hp


def test_el_acido_o_el_fuego_bloquea_un_solo_inicio_de_turno(monkeypatch):
    troll = _troll(monkeypatch)
    troll.hp = 50
    ctx = _ctx(troll, [troll])
    begin_turn(troll, ctx)
    assert troll.hp == 60
    inflict_damage(troll, 5, "fire", ctx=ctx)
    assert troll.hp == 55
    # Bloqueado: no cura en el próximo inicio de turno...
    begin_turn(troll, ctx)
    assert troll.hp == 55
    assert any("no regenera" in linea for linea in ctx.log)
    # ...y al turno siguiente vuelve a funcionar.
    begin_turn(troll, ctx)
    assert troll.hp == 65


def test_el_daño_normal_no_bloquea_la_regeneracion(monkeypatch):
    troll = _troll(monkeypatch)
    troll.hp = 50
    inflict_damage(troll, 5, "slashing")
    assert troll.hp == 45
    ctx = _ctx(troll, [troll])
    begin_turn(troll, ctx)
    assert troll.hp == 45 + 10
    assert not any("no regenera" in linea for linea in ctx.log)


def test_el_troll_a_0_pv_no_regenera_y_muere_en_su_turno(monkeypatch):
    troll = _troll(monkeypatch)
    troll.hp = 0
    assert troll.alive, "a 0 PV sigue en pie hasta su próximo turno"
    ctx = _ctx(troll, [troll])
    begin_turn(troll, ctx)
    # A 0 PV no se regenera (si no, el troll se salvaría siempre).
    assert troll.hp == 0
    assert not troll.alive
    assert troll.dead
    assert ctx.skip_turn, "su turno queda anulado"
    assert any("muere" in linea for linea in ctx.log)


def test_el_troll_muere_en_su_turno_si_no_puede_regenerarse(monkeypatch):
    troll = _troll(monkeypatch)
    troll.hp = 0
    inflict_damage(troll, 1, "fire")          # bloquea la curación
    assert troll.alive, "muere en su turno, no al recibir el golpe"
    ctx = _ctx(troll, [troll])
    begin_turn(troll, ctx)
    assert not troll.alive
    assert ctx.skip_turn, "su turno queda anulado"
    assert any("muere" in linea for linea in ctx.log)


def test_una_criatura_sin_regeneracion_muere_al_llegar_a_cero():
    # El cambio de 0 PV solo afecta a quien tiene el rasgo.
    pj = PlayerCharacter(name="PJ", max_hp=10, ac=10, abilities=Abilities(),
                         attacks=[])
    pj.hp = 0
    assert not pj.alive


def test_el_estado_de_la_regeneracion_se_reinicia_en_cada_combate(monkeypatch):
    # simulate() reutiliza los mismos objetos: el reset limpia bloqueo y muerte.
    troll = _troll(monkeypatch)
    troll.hp = 0
    inflict_damage(troll, 1, "fire")
    begin_turn(troll, _ctx(troll, [troll]))
    assert not troll.alive
    troll.reset()
    assert troll.alive
    assert troll.hp == troll.max_hp


# --- Integración con el motor ----------------------------------------------- #

def test_la_regeneracion_aparece_en_un_combate_completo(monkeypatch):
    troll = _troll(monkeypatch)
    objetivo = _pj(hp=300)
    res = run_combat([objetivo, troll], random.Random(7), verbose=True,
                     max_rounds=6)
    assert any("regenera" in linea for linea in res.log), \
        "el troll debe curarse al menos una vez en su turno"
    assert any("Regeneration" in linea for linea in res.log)
    # Sigue en pie y sigue peleando (si hubiera muerto, no inflige nada).
    assert res.damage_dealt.get("Troll", 0) > 0

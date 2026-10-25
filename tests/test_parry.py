"""Parry del gladiador (y del hobgoblin warlord): +N de CA contra un golpe.

La ficha del gladiador (fixture real de la API) trae Parry en sus
**reactions**, no en ``special_abilities``: por eso ``parse_traits`` mira
las dos secciones. El rasgo es una reacción (``state.reaction_used``, que
se recarga al empezar su turno) y solo se gasta si con el bonificador el
ataque deja de entrar: nadie para con la reacción un golpe que igual entra.

Para que las tiradas sean deterministas se fija el d20; el resto del
ataque (bonificador del atacante y CA del defensor) es constante.
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, Monster, PlayerCharacter
from dnd_sim.actions import CombatContext, TurnResources
from dnd_sim.attack import Attack
from dnd_sim.combat import attack_roll, run_combat
from dnd_sim.conditions import Condition, apply_condition
from dnd_sim.data.loader import load_monster
from dnd_sim.data.trait_parser import parse_traits
from dnd_sim.dice import D20Result, RollMode
from dnd_sim.roll_modifiers import AttackRange
from dnd_sim.traits import Parry
from dnd_sim.usage import begin_turn

FIXTURES = Path(__file__).parent / "fixtures"

# Texto real del SRD: la API no sirve «hobgoblin-warlord», así que su Parry
# se prueba con la descripción tal cual.
PARRY_SRD = (
    "The hobgoblin adds 3 to its AC against one melee attack that would hit "
    "it. To do so, the hobgoblin must see the attacker and be wielding a "
    "melee weapon."
)

# Con CA 16 y bonificador de ataque +5: la tirada 12 entra (17 >= 16) y con
# el parry +3 deja de entrar (17 < 19); la tirada 15 entra con o sin parry
# (20 >= 19).
D20_QUE_EL_PARRY_ATAJA = 12
D20_QUE_EL_PARRY_NO_ATAJA = 15


# --- Utilidades ------------------------------------------------------------- #

def _datos(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _gladiador(monkeypatch) -> Monster:
    data = _datos("gladiator")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("gladiator")


def _pj(ataques: list[Attack] | None = None) -> PlayerCharacter:
    return PlayerCharacter(
        name="Guerrero", max_hp=60, ac=15, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=ataques if ataques is not None else [
            Attack(name="Espada", damage="1d8", ability="str",
                   attack_bonus=5, damage_bonus=3)],
    )


def _arquero_parry() -> Monster:
    """Defensor con Parry pero **sin** arma cuerpo a cuerpo."""
    rasgo = parse_traits({"reactions": [
        {"name": "Parry", "desc": PARRY_SRD.replace("hobgoblin", "arquero")},
    ]})[0]
    return Monster(
        name="Arquero", max_hp=30, ac=15, proficiency=2,
        abilities=Abilities(str=10, dex=16, con=12, int=10, wis=12, cha=8),
        attacks=[Attack(name="Arco", damage="1d8", ability="dex",
                        attack_bonus=5, range_type=AttackRange.RANGED)],
        traits=[rasgo],
    )


def _ctx(actor, combatantes, semilla: int = 1) -> CombatContext:
    return CombatContext(rng=random.Random(semilla), actor=actor,
                         combatants=list(combatantes), round=1, log=[],
                         verbose=True, resources=TurnResources())


def _fijar_d20(monkeypatch, valor: int) -> None:
    """Fija la tirada del d20 (el resto del ataque ya es determinista)."""
    import dnd_sim.combat as combat_mod

    def espia(rng, mode=RollMode.NORMAL, **kw):
        return D20Result(value=valor, rolls=[valor, valor], mode=mode)

    monkeypatch.setattr(combat_mod, "roll_d20", espia)


def _ataque(monstruo) -> Attack:
    return monstruo.attacks[0]


# --- Carga de la ficha ------------------------------------------------------ #

def test_el_gladiador_carga_su_parry_desde_las_reacciones(monkeypatch):
    gladiador = _gladiador(monkeypatch)
    # Brave y Brute no están modelados: solo el Parry.
    assert [type(t).__name__ for t in gladiador.traits] == ["Parry"]
    rasgo = gladiador.traits[0]
    assert rasgo.name == "Parry"
    # El número sale de la descripción («adds 3 to its AC»).
    assert rasgo.bonus == 3


def test_el_parry_de_una_ficha_sin_api_se_parsea_desde_el_srd():
    # El hobgoblin warlord no está en la API: su texto del SRD basta.
    rasgo = parse_traits({"reactions": [
        {"name": "Parry", "desc": PARRY_SRD},
    ]})[0]
    assert isinstance(rasgo, Parry)
    assert rasgo.bonus == 3


def test_una_descripcion_no_interpretable_no_paria(monkeypatch):
    rasgo = parse_traits({"reactions": [
        {"name": "Parry", "desc": "Se defiende con decisión."},
    ]})[0]
    assert rasgo.bonus == 0
    gladiador = _gladiador(monkeypatch)
    pj = _pj()
    ctx = _ctx(pj, [pj, gladiador])
    assert rasgo.defensive_ac_bonus(gladiador, pj, AttackRange.MELEE,
                                    total=17, ca=16, ctx=ctx,
                                    rng=ctx.rng) == 0
    assert not gladiador.state.reaction_used


# --- Reglas del parry ------------------------------------------------------- #

def test_el_parry_convierte_un_impacto_en_fallo(monkeypatch):
    gladiador = _gladiador(monkeypatch)
    pj = _pj()
    ctx = _ctx(pj, [pj, gladiador])
    ctx.log.clear()
    _fijar_d20(monkeypatch, D20_QUE_EL_PARRY_ATAJA)
    antes = gladiador.hp
    attack_roll(pj, gladiador, _ataque(pj), random.Random(1), ctx.log, ctx=ctx)
    assert gladiador.hp == antes, "el golpe 17 no llega a la CA 19"
    assert gladiador.state.reaction_used, "parar es gastar la reacción"
    assert any("usa Parry" in l and "+3 CA" in l for l in ctx.log)


def test_el_parry_no_aplica_a_un_ataque_a_distancia(monkeypatch):
    gladiador = _gladiador(monkeypatch)
    pj = _pj(ataques=[Attack(name="Dardo", damage="1d4", ability="dex",
                             attack_bonus=5, range_type=AttackRange.RANGED)])
    ctx = _ctx(pj, [pj, gladiador])
    ctx.log.clear()
    _fijar_d20(monkeypatch, D20_QUE_EL_PARRY_ATAJA)
    antes = gladiador.hp
    attack_roll(pj, gladiador, _ataque(pj), random.Random(1), ctx.log, ctx=ctx)
    assert gladiador.hp < antes, "«against one melee attack»: a distancia no"
    assert not gladiador.state.reaction_used
    assert not any("usa Parry" in l for l in ctx.log)


def test_no_se_gasta_la_reaccion_si_igual_no_compensa(monkeypatch):
    # 15 + 5 = 20 >= 19: ni con el +3 el golpe cae, así que no se parryea.
    gladiador = _gladiador(monkeypatch)
    pj = _pj()
    ctx = _ctx(pj, [pj, gladiador])
    ctx.log.clear()
    _fijar_d20(monkeypatch, D20_QUE_EL_PARRY_NO_ATAJA)
    antes = gladiador.hp
    attack_roll(pj, gladiador, _ataque(pj), random.Random(1), ctx.log, ctx=ctx)
    assert gladiador.hp < antes, "el golpe entra: el parry no lo salvaría"
    assert not gladiador.state.reaction_used, "la reacción no se gasta en vano"
    assert not any("usa Parry" in l for l in ctx.log)


def test_no_paria_si_ya_gasto_su_reaccion(monkeypatch):
    gladiador = _gladiador(monkeypatch)
    pj = _pj()
    ctx = _ctx(pj, [pj, gladiador])
    ctx.log.clear()
    gladiador.state.reaction_used = True
    _fijar_d20(monkeypatch, D20_QUE_EL_PARRY_ATAJA)
    antes = gladiador.hp
    attack_roll(pj, gladiador, _ataque(pj), random.Random(1), ctx.log, ctx=ctx)
    assert gladiador.hp < antes
    assert not any("usa Parry" in l for l in ctx.log)


def test_la_reaccion_se_recarga_al_empezar_su_turno(monkeypatch):
    gladiador = _gladiador(monkeypatch)
    pj = _pj()
    ctx = _ctx(pj, [pj, gladiador])
    ctx.log.clear()
    _fijar_d20(monkeypatch, D20_QUE_EL_PARRY_ATAJA)
    attack_roll(pj, gladiador, _ataque(pj), random.Random(1), ctx.log, ctx=ctx)
    assert gladiador.state.reaction_used
    begin_turn(gladiador, ctx)
    assert not gladiador.state.reaction_used, "la reacción se recarga al turno"


def test_no_paria_a_un_atacante_invisible(monkeypatch):
    gladiador = _gladiador(monkeypatch)
    pj = _pj()
    ctx = _ctx(pj, [pj, gladiador])
    apply_condition(pj, Condition.INVISIBLE, ctx, duration_rounds=None)
    ctx.log.clear()
    _fijar_d20(monkeypatch, D20_QUE_EL_PARRY_ATAJA)
    antes = gladiador.hp
    attack_roll(pj, gladiador, _ataque(pj), random.Random(1), ctx.log, ctx=ctx)
    assert gladiador.hp < antes, "«must see the attacker»: no ve al invisible"
    assert not gladiador.state.reaction_used
    assert not any("usa Parry" in l for l in ctx.log)


def test_no_paria_sin_arma_cuerpo_a_cuerpo(monkeypatch):
    # «and be wielding a melee weapon»: un arquero no tiene con qué parar.
    arquero = _arquero_parry()
    pj = _pj()
    ctx = _ctx(pj, [pj, arquero])
    ctx.log.clear()
    _fijar_d20(monkeypatch, D20_QUE_EL_PARRY_ATAJA)
    antes = arquero.hp
    attack_roll(pj, arquero, _ataque(pj), random.Random(1), ctx.log, ctx=ctx)
    assert arquero.hp < antes
    assert not arquero.state.reaction_used
    assert not any("usa Parry" in l for l in ctx.log)


def test_un_critico_acierta_aunque_haya_parry(monkeypatch):
    gladiador = _gladiador(monkeypatch)
    pj = _pj()
    ctx = _ctx(pj, [pj, gladiador])
    ctx.log.clear()
    _fijar_d20(monkeypatch, 20)
    antes = gladiador.hp
    attack_roll(pj, gladiador, _ataque(pj), random.Random(1), ctx.log, ctx=ctx)
    assert gladiador.hp < antes, "un 20 natural da igual la CA"
    assert not gladiador.state.reaction_used, "el parry ni se consulta"
    assert not any("usa Parry" in l for l in ctx.log)


def test_un_fallo_natural_tampoco_llega_al_parry(monkeypatch):
    gladiador = _gladiador(monkeypatch)
    pj = _pj()
    ctx = _ctx(pj, [pj, gladiador])
    ctx.log.clear()
    _fijar_d20(monkeypatch, 1)
    antes = gladiador.hp
    attack_roll(pj, gladiador, _ataque(pj), random.Random(1), ctx.log, ctx=ctx)
    assert gladiador.hp == antes
    assert not gladiador.state.reaction_used


# --- Integración con el motor ----------------------------------------------- #

def test_un_combate_completo_usa_parry(monkeypatch):
    gladiador = _gladiador(monkeypatch)
    pj = _pj()
    res = run_combat([pj, gladiador], random.Random(5), verbose=True,
                     max_rounds=50)
    assert any("usa Parry" in l for l in res.log), \
        "el gladiador debe poder parar en combate"

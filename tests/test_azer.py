"""Heated Body (azer): daño de fuego a quien lo golpea cuerpo a cuerpo.

El rasgo se parsea de ``special_abilities`` (fixture real de la API) y su
hook ``after_being_hit`` se dispara en :func:`dnd_sim.combat.attack_roll`
tras el daño, en cada impacto (aunque el daño sea 0 por inmunidad), porque
el trigger de la ficha es el impacto, no el daño recibido.
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, Monster, PlayerCharacter
from dnd_sim.actions import CombatContext, TurnResources
from dnd_sim.attack import Attack
from dnd_sim.combat import attack_roll
from dnd_sim.data.loader import load_monster
from dnd_sim.damage import DamageType
from dnd_sim.roll_modifiers import AttackRange
from dnd_sim.traits import HeatedBody

FIXTURES = Path(__file__).parent / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _datos(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _azer(monkeypatch) -> Monster:
    data = _datos("azer")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("azer")


def _pj(name: str = "Guerrero", hp: int = 40) -> PlayerCharacter:
    return PlayerCharacter(
        name=name, max_hp=hp, ac=15, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[Attack(name="Espada", damage="1d8", ability="str",
                        attack_bonus=5, damage_bonus=3)],
    )


def _ctx(actor, combatants, rng=None, log=None) -> CombatContext:
    return CombatContext(rng=rng or random.Random(1), actor=actor,
                         combatants=list(combatants), round=1,
                         log=log if log is not None else [], verbose=True,
                         resources=TurnResources())


def _ataque_melee() -> Attack:
    return Attack(name="Espada", damage="1d8", ability="str",
                  attack_bonus=5, damage_bonus=3)


def _ataque_ranged() -> Attack:
    return Attack(name="Dardo", damage="1d4", ability="dex",
                  attack_bonus=6, damage_bonus=2, range_type=AttackRange.RANGED)


# --- Carga del rasgo -------------------------------------------------------- #

def test_el_azer_carga_su_rasgo_heated_body(monkeypatch):
    azer = _azer(monkeypatch)
    assert any(isinstance(t, HeatedBody) for t in azer.traits)
    hb = next(t for t in azer.traits if isinstance(t, HeatedBody))
    assert hb.damage == "1d10"
    assert hb.damage_type == "fire"


def test_heated_body_no_es_accion(monkeypatch):
    # El Heated Body es pasivo: no debe colarse como acción suelta.
    azer = _azer(monkeypatch)
    nombres = [getattr(a, "name", "") for a in azer.actions]
    assert "Heated Body" not in nombres


# --- El hook after_being_hit ------------------------------------------------ #

def test_golpear_cuerpo_a_cuerpo_al_azer_quema_al_atacante(monkeypatch):
    azer = _azer(monkeypatch)
    pj = _pj()
    ctx = _ctx(azer, [azer, pj])
    hp_antes = pj.hp
    # Impacto garantizado (semilla 5: primer d20 = 20).
    attack_roll(pj, azer, _ataque_melee(), random.Random(5), ctx.log, ctx=ctx)
    assert pj.hp < hp_antes, "el atacante debe recibir daño por el cuerpo ardiente"
    assert any("cuerpo ardiente" in l for l in ctx.log)


def test_el_daño_de_la_represalia_es_de_fuego(monkeypatch):
    azer = _azer(monkeypatch)
    azer.immunities = set()
    pj = _pj()
    ctx = _ctx(azer, [azer, pj])
    hp_antes = pj.hp
    attack_roll(pj, azer, _ataque_melee(), random.Random(5), ctx.log, ctx=ctx)
    # 1d10 de fuego: el PJ no tiene resistencias, así que el daño es > 0.
    assert pj.hp < hp_antes


def test_ataque_a_distancia_no_dispara_la_represalia(monkeypatch):
    azer = _azer(monkeypatch)
    pj = _pj()
    ctx = _ctx(azer, [azer, pj])
    hp_antes = pj.hp
    # A distancia el azer no quema (el trigger es el contacto / melee).
    attack_roll(pj, azer, _ataque_ranged(), random.Random(5), ctx.log, ctx=ctx)
    # Solo el daño del dardo (el PJ está a distancia, la CA sube +2).
    assert not any("cuerpo ardiente" in l for l in ctx.log)


def test_impacto_aunque_el_atacante_es_inmune_al_fuego(monkeypatch):
    # El trigger es el impacto, no el daño: aunque el atacante sea inmune
    # al fuego, el hook se dispara (el daño de la represalia es 0 y no le
    # baja PV por ese motivo). aislando la llamada de fuego con un espía.
    import dnd_sim.traits as traits_mod
    azer = _azer(monkeypatch)
    azero_inmune = _pj()
    azero_inmune.immunities = {DamageType.FIRE}
    llamadas = []

    def espia(target, amount, damage_type, source=None, ctx=None):
        llamadas.append((damage_type, amount))
        return None  # no inflige nada: el atacante es inmune

    monkeypatch.setattr(traits_mod, "inflict_damage", espia)
    ctx = _ctx(azer, [azer, azero_inmune])
    attack_roll(azero_inmune, azer, _ataque_melee(), random.Random(5),
                ctx.log, ctx=ctx)
    assert llamadas and llamadas[0][0] in ("fire", DamageType.FIRE), \
        "la represalia debe intentar daño de fuego aunque no surta efecto"
    assert any("cuerpo ardiente" in l for l in ctx.log)


# --- Repetición en cada impacto ---------------------------------------------- #

def test_cada_impacto_dispara_su_propia_represalia(monkeypatch):
    azer = _azer(monkeypatch)
    pj = _pj(hp=100)
    ctx = _ctx(azer, [azer, pj])
    hp1 = pj.hp
    attack_roll(pj, azer, _ataque_melee(), random.Random(5), ctx.log, ctx=ctx)
    hp2 = pj.hp
    attack_roll(pj, azer, _ataque_melee(), random.Random(9), ctx.log, ctx=ctx)
    hp3 = pj.hp
    assert hp2 < hp1 and hp3 < hp2, "cada impacto debe quemar por separado"
    assert sum("cuerpo ardiente" in l for l in ctx.log) == 2

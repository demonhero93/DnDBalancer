"""Daño adicional de armas (``Attack.extra_damage``).

Muchas fichas declaran, tras el daño principal, una o más entradas
**adicionales** de distinto tipo («plus 7 (2d6) fire damage»): el
Warhammer del azer (1d8+3 contundente + 1d6 fuego, Heated Weapons) o el
mordisco de un dragón (perforante + fuego/ácido). El parser las acumula
al daño principal; cada entrada resuelve su resistencia/inmunidad con su
**propio** tipo y se duplican los dados extra en crítico.
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, PlayerCharacter
from dnd_sim.actions import CombatContext, TurnResources
from dnd_sim.attack import Attack, ExtraDamage
from dnd_sim.combat import attack_roll
from dnd_sim.data.loader import load_monster
from dnd_sim.damage import DamageRecorder, DamageType

FIXTURES = Path(__file__).parent / "fixtures"

# Semillas con primer d20 conocido: 6 -> 19 (impacto, no crítico);
# 5 -> 20 (crítico).
SEED_GOLPE = 6
SEED_CRITICO = 5


# --- Utilidades ------------------------------------------------------------- #

def _datos(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _azer(monkeypatch) -> object:
    data = _datos("azer")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("azer")


def _dragon(monkeypatch) -> object:
    data = _datos("adult-red-dragon")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("adult-red-dragon")


def _pj(hp: int = 200) -> PlayerCharacter:
    return PlayerCharacter(
        name="Guerrero", max_hp=hp, ac=10, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[Attack(name="Espada", damage="1d8", ability="str",
                        attack_bonus=5, damage_bonus=3)],
    )


def _ctx(actor, combatants, rng=None, log=None) -> CombatContext:
    return CombatContext(rng=rng or random.Random(SEED_GOLPE), actor=actor,
                         combatants=list(combatants), round=1,
                         log=log if log is not None else [], verbose=True,
                         resources=TurnResources())


def _warhammer(azer) -> Attack:
    return next(a for a in azer.attacks if a.name == "Warhammer")


def _espiar_inflict(monkeypatch):
    """Sustituye ``combat.inflict_damage`` por un espía que registra
    (objetivo, cantidad, tipo) y no inflige nada.

    Acepta ``**kw`` porque la función real también recibe ``crit`` y
    ``rng`` (los usan los rasgos que se salvan a 0 PV).
    """
    llamadas = []

    def espia(target, amount, damage_type=None, source=None, ctx=None, **kw):
        llamadas.append((target, amount, damage_type))
        return 0

    monkeypatch.setattr("dnd_sim.combat.inflict_damage", espia)
    return llamadas


# --- El parser acumula el daño adicional ------------------------------------ #

def test_el_warhammer_del_azer_lleva_1d6_de_fuego(monkeypatch):
    azer = _azer(monkeypatch)
    wh = _warhammer(azer)
    assert wh.damage == "1d8+3"
    assert wh.damage_type == DamageType.BLUDGEONING
    assert len(wh.extra_damage) == 1
    extra = wh.extra_damage[0]
    assert extra.damage == "1d6"
    assert extra.damage_type == DamageType.FIRE


def test_el_mordisco_del_dragon_lleva_fuego_adicional(monkeypatch):
    dragon = _dragon(monkeypatch)
    bite = next(a for a in dragon.attacks if a.name == "Bite")
    assert bite.damage_type == DamageType.PIERCING
    assert [(e.damage, e.damage_type) for e in bite.extra_damage] == [
        ("2d6", DamageType.FIRE)
    ]


# --- Se aplica en el impacto, con su propio tipo ---------------------------- #

def test_al_impactar_se_infinge_tambien_el_daño_adicional(monkeypatch):
    azer = _azer(monkeypatch)
    pj = _pj()
    llamadas = _espiar_inflict(monkeypatch)
    ctx = _ctx(azer, [azer, pj])
    attack_roll(azer, pj, _warhammer(azer), random.Random(SEED_GOLPE), ctx.log,
                ctx=ctx)
    tipos = [dt for (_t, _amt, dt) in llamadas]
    # Daño principal (contundente) + adicional (fuego), cada uno aparte.
    assert DamageType.BLUDGEONING in tipos
    assert DamageType.FIRE in tipos
    fire = [amt for (_t, amt, dt) in llamadas if dt == DamageType.FIRE]
    assert 1 <= fire[0] <= 6, "el 1d6 de fuego debe estar en su rango"


def test_los_pv_bajan_mas_que_solo_el_daño_principal(monkeypatch):
    # Misma semilla, mismo ataque con y sin el daño adicional: la única
    # diferencia debe ser el 1d6 de fuego (entre 1 y 6).
    azer = _azer(monkeypatch)
    wh_con = _warhammer(azer)
    wh_sin = Attack(name=wh_con.name, damage=wh_con.damage,
                    ability=wh_con.ability, attack_bonus=wh_con.attack_bonus,
                    damage_bonus=wh_con.damage_bonus,
                    damage_type=wh_con.damage_type)  # sin extra_damage
    pj1 = _pj()
    ctx1 = _ctx(azer, [azer, pj1])
    attack_roll(azer, pj1, wh_con, random.Random(SEED_GOLPE), ctx1.log, ctx=ctx1)
    perdida_con = pj1.max_hp - pj1.hp

    pj2 = _pj()
    ctx2 = _ctx(azer, [azer, pj2])
    attack_roll(azer, pj2, wh_sin, random.Random(SEED_GOLPE), ctx2.log, ctx=ctx2)
    perdida_sin = pj2.max_hp - pj2.hp

    diferencia = perdida_con - perdida_sin
    assert 1 <= diferencia <= 6, (f"el extra (1d6) debe sumar entre 1 y 6, "
                                  f"sumó {diferencia}")


# --- Resistencia / inmunidad por tipo --------------------------------------- #

def test_resistencia_al_fuego_reduce_solo_el_extra(monkeypatch):
    azer = _azer(monkeypatch)
    wh = _warhammer(azer)
    # Misma semilla en dos objetivos idénticos, salvo la resistencia al
    # fuego: el daño de fuego debe quedar a la mitad (redondeo hacia abajo).
    neutral = _espiar_inflict(monkeypatch)
    pj1 = _pj()
    ctx1 = _ctx(azer, [azer, pj1], rng=random.Random(SEED_GOLPE))
    attack_roll(azer, pj1, wh, random.Random(SEED_GOLPE), ctx1.log, ctx=ctx1)
    fire1 = [amt for (_t, amt, dt) in neutral if dt == DamageType.FIRE][0]

    resistente = _espiar_inflict(monkeypatch)
    pj2 = _pj()
    pj2.resistances = {DamageType.FIRE}
    ctx2 = _ctx(azer, [azer, pj2], rng=random.Random(SEED_GOLPE))
    attack_roll(azer, pj2, wh, random.Random(SEED_GOLPE), ctx2.log, ctx=ctx2)
    fire2 = [amt for (_t, amt, dt) in resistente if dt == DamageType.FIRE][0]

    assert fire2 == fire1 // 2, (f"fuego sin resistencia {fire1}, con "
                                 f"resistencia {fire2}")


def test_inmune_al_fuego_el_extra_no_dania_pero_el_principal_si(monkeypatch):
    azer = _azer(monkeypatch)
    pj = _pj()
    pj.immunities = {DamageType.FIRE}
    llamadas = _espiar_inflict(monkeypatch)
    ctx = _ctx(azer, [azer, pj])
    attack_roll(azer, pj, _warhammer(azer), random.Random(SEED_GOLPE), ctx.log,
                ctx=ctx)
    # Inmune: el extra de fuego se resuelve igual que el daño principal, es
    # decir, se llama a inflict_damage con 0 (el registro ve el impacto, pero
    # no baja PV ni suma daño); el contundente principal sí daña.
    fire = [amt for (_t, amt, dt) in llamadas if dt == DamageType.FIRE]
    assert fire == [0], f"el fuego debe infligirse con 0, llamadas: {fire}"
    blud = [amt for (_t, amt, dt) in llamadas if dt == DamageType.BLUDGEONING]
    assert blud and blud[0] > 0


def test_el_extra_inmune_queda_registrado_con_cero(monkeypatch):
    """El registro de daño también ve los impactos que no hacen daño (0)."""
    azer = _azer(monkeypatch)
    pj = _pj()
    pj.immunities = {DamageType.FIRE}
    ctx = _ctx(azer, [azer, pj])
    with DamageRecorder() as recorder:
        attack_roll(azer, pj, _warhammer(azer), random.Random(SEED_GOLPE),
                    ctx.log, ctx=ctx)
    fuego = [r["amount"] for r in recorder.records
             if r["damage_type"] == DamageType.FIRE]
    assert fuego == [0], f"el extra inmune debe registrarse con 0: {fuego}"


# --- Crítico: los dados extra también se duplican --------------------------- #

def test_en_critico_roll_dice_recibe_crit_para_el_extra(monkeypatch):
    azer = _azer(monkeypatch)
    pj = _pj()
    _espiar_inflict(monkeypatch)
    llamadas_dice = []

    import dnd_sim.combat as combat_mod
    original = combat_mod.roll_dice

    def espia_dice(dados, rng=None, crit=False, **kw):
        llamadas_dice.append((str(dados), bool(crit)))
        return original(dados, rng, crit=crit, **kw)

    monkeypatch.setattr(combat_mod, "roll_dice", espia_dice)
    ctx = _ctx(azer, [azer, pj], rng=random.Random(SEED_CRITICO))
    attack_roll(azer, pj, _warhammer(azer), random.Random(SEED_CRITICO),
                ctx.log, ctx=ctx)
    # El extra (1d6 de fuego) se tira con crit=True, como el principal.
    assert ("1d6", True) in llamadas_dice, llamadas_dice


# --- Ataques sin daño adicional no cambian ---------------------------------- #

def test_ataque_sin_extra_no_llama_al_bucle(monkeypatch):
    # Un ataque con extra_damage vacío no genera llamadas de fuego.
    azer = _azer(monkeypatch)
    pj = _pj()
    llamadas = _espiar_inflict(monkeypatch)
    atk = Attack(name="Simple", damage="1d8", ability="str",
                 attack_bonus=5, damage_bonus=3,
                 damage_type=DamageType.PIERCING)
    ctx = _ctx(azer, [azer, pj])
    attack_roll(azer, pj, atk, random.Random(SEED_GOLPE), ctx.log, ctx=ctx)
    tipos = {dt for (_t, _amt, dt) in llamadas}
    assert tipos == {DamageType.PIERCING}


def test_extra_damage_estructura_por_defecto_vacia():
    atk = Attack(name="X", damage="1d6")
    assert atk.extra_damage == []

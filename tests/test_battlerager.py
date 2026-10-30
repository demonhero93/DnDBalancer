"""Tests de la subclase Battlerager del bárbaro (SCAG)."""
from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from dnd_sim import (
    Abilities,
    Attack,
    Monster,
    PlayerCharacter,
    apply_barbarian,
    apply_battlerager,
)
from dnd_sim.core.enums import AttackRange
from dnd_sim.model.actions import ActionType, TurnResources
from dnd_sim.rules.classes.barbarian import BarbarianFeatures
from dnd_sim.rules.classes.barbarian.subclasses.battlerager import (
    BATTLERAGER_FEATURES,
    BattleragerFeatures,
    SpikedArmorAction,
)
from dnd_sim.rules.damage import inflict_damage
from dnd_sim.rules.roll_modifiers import AttackModifiers


def _abilities(**kwargs):
    scores = dict(str=10, dex=10, con=10, int=10, wis=10, cha=10)
    scores.update(kwargs)
    return Abilities(**scores)


def _pj(**kwargs):
    kwargs.setdefault("name", "Thor")
    kwargs.setdefault("max_hp", 300)
    kwargs.setdefault("ac", 15)
    kwargs.setdefault("level", 5)
    kwargs.setdefault("abilities", _abilities(str=16, dex=14, con=16))
    kwargs.setdefault(
        "attacks", [Attack("Hacha de batalla", "1d12", ability="str")]
    )
    return PlayerCharacter(**kwargs)


def _monstruo(**kwargs):
    kwargs.setdefault("name", "Orco")
    kwargs.setdefault("max_hp", 300)
    kwargs.setdefault("ac", 10)
    kwargs.setdefault("abilities", _abilities(str=13))
    kwargs.setdefault("attacks", [Attack("Hacha orca", "1d6", ability="str")])
    return Monster(**kwargs)


def _barrer(pj, level=None):
    apply_barbarian(pj, level=level)
    return apply_battlerager(pj, level=level)


def _bj(pj):
    return next(t for t in pj.traits if isinstance(t, BattleragerFeatures))


def _barb(pj):
    return next(t for t in pj.traits if isinstance(t, BarbarianFeatures))


def _ataque(ability="str"):
    return Attack("Hacha de batalla", "1d12", ability=ability)


def _ctx(actor, combatants=None, round_=1, seed=0):
    return SimpleNamespace(
        actor=actor,
        combatants=combatants if combatants is not None else [actor],
        round=round_,
        rng=random.Random(seed),
        log=[],
        resources=TurnResources(),
        verbose=False,
    )


# --- Tabla y aplicación -------------------------------------------------------

def test_tabla_features():
    assert BATTLERAGER_FEATURES == {
        3: ("Battlerager Armor",),
        6: ("Reckless Abandon",),
        10: ("Battlerager Charge",),
        14: ("Spiked Retribution",),
    }


def test_apply_exige_clase_barbaro():
    pj = _pj()
    with pytest.raises(ValueError, match="apply_barbarian"):
        apply_battlerager(pj)


def test_apply_anade_trait_y_accion_bonus():
    pj = _pj()
    _barrer(pj, level=5)
    trait = _bj(pj)
    assert trait.level == 5
    assert trait.owner is pj
    acciones = [a for a in pj.actions if isinstance(a, SpikedArmorAction)]
    assert len(acciones) == 1
    assert acciones[0].action_type == ActionType.BONUS_ACTION
    assert acciones[0].attack.ability == "str"
    assert acciones[0].attack.damage == "1d4"


def test_apply_nivel_explicito_manda():
    pj = _pj(level=8)
    _barrer(pj, level=3)
    assert _bj(pj).level == 3


# --- PV temporales (sistema nuevo) -------------------------------------------

def test_temp_hp_por_defecto_y_reset():
    pj = _pj()
    assert pj.temp_hp == 0
    pj.temp_hp = 7
    pj.reset()
    assert pj.temp_hp == 0


def test_inflict_damage_absorbe_antes_que_los_pv():
    pj = _pj()
    pj.temp_hp = 5
    inflict_damage(pj, 10, "bludgeoning")
    assert pj.hp == 295          # solo 5 bajan de los PV
    assert pj.temp_hp == 0       # los temporales quedan gastados


def test_inflict_damage_temporales_de_reposo():
    pj = _pj()
    pj.temp_hp = 10
    inflict_damage(pj, 4, "bludgeoning")
    assert pj.hp == 300          # nada baja de los PV
    assert pj.temp_hp == 6       # sobran 6


def test_temporales_no_dejan_a_cero():
    pj = _pj(max_hp=5)
    pj.temp_hp = 10
    inflict_damage(pj, 7, "piercing")
    assert pj.hp == 5
    assert not pj.dead


# --- Reckless Abandon (6) -----------------------------------------------------

def test_reckless_abandon_concede_pv_temporales():
    pj = _pj()                   # CON 16 → +3
    _barrer(pj, level=6)
    barb = _barb(pj)
    barb.rage_active = True
    _bj(pj).modify_attack_modifiers(
        AttackModifiers(), pj, None, AttackRange.MELEE, atk=_ataque()
    )
    assert pj.temp_hp == 3
    assert _bj(pj).abandono_temp


def test_reckless_abandon_minimo_uno():
    pj = _pj(abilities=_abilities(str=16, con=10))
    _barrer(pj, level=6)
    _barb(pj).rage_active = True
    _bj(pj).modify_attack_modifiers(
        AttackModifiers(), pj, None, AttackRange.MELEE, atk=_ataque()
    )
    assert pj.temp_hp == 1


def test_reckless_abandon_condiciones():
    # Sin Furia no concede.
    pj = _pj()
    _barrer(pj, level=6)
    _bj(pj).modify_attack_modifiers(
        AttackModifiers(), pj, None, AttackRange.MELEE, atk=_ataque()
    )
    assert pj.temp_hp == 0
    # Nivel < 6 tampoco.
    pj2 = _pj()
    _barrer(pj2, level=5)
    _barb(pj2).rage_active = True
    _bj(pj2).modify_attack_modifiers(
        AttackModifiers(), pj2, None, AttackRange.MELEE, atk=_ataque()
    )
    assert pj2.temp_hp == 0
    # Los ataques de DES no son de Reckless.
    pj3 = _pj()
    _barrer(pj3, level=6)
    _barb(pj3).rage_active = True
    _bj(pj3).modify_attack_modifiers(
        AttackModifiers(), pj3, None, AttackRange.MELEE, atk=_ataque("dex")
    )
    assert pj3.temp_hp == 0


def test_reckless_abandon_no_apila():
    pj = _pj()                   # concesión +3
    _barrer(pj, level=6)
    _barb(pj).rage_active = True
    pj.temp_hp = 9               # más que la concesión → se queda el mayor
    _bj(pj).modify_attack_modifiers(
        AttackModifiers(), pj, None, AttackRange.MELEE, atk=_ataque()
    )
    assert pj.temp_hp == 9
    assert not _bj(pj).abandono_temp


def test_temporales_desaparecen_al_terminar_furia():
    pj = _pj()
    _barrer(pj, level=6)
    barb = _barb(pj)
    barb.rage_active = True
    _bj(pj).modify_attack_modifiers(
        AttackModifiers(), pj, None, AttackRange.MELEE, atk=_ataque()
    )
    assert pj.temp_hp == 3
    # Con Furia activa, los temporales aguantan.
    _bj(pj).on_turn_end(pj, None)
    assert pj.temp_hp == 3
    # La Furia termina → caen.
    barb.rage_active = False
    _bj(pj).on_turn_end(pj, None)
    assert pj.temp_hp == 0
    assert not _bj(pj).abandono_temp


def test_temporales_desaparecen_en_el_siguiente_inicio():
    pj = _pj()
    _barrer(pj, level=6)
    barb = _barb(pj)
    barb.rage_active = True
    _bj(pj).modify_attack_modifiers(
        AttackModifiers(), pj, None, AttackRange.MELEE, atk=_ataque()
    )
    barb.rage_active = False     # p. ej. terminó por Incapacitado
    _bj(pj).on_turn_start(pj, None)
    assert pj.temp_hp == 0


# --- Battlerager Armor (3) ----------------------------------------------------

def _accion_puas(pj):
    return next(a for a in pj.actions if isinstance(a, SpikedArmorAction))


def test_spike_action_can_use_solo_con_furia():
    pj = _pj()
    _barrer(pj, level=5)
    accion = _accion_puas(pj)
    ctx = _ctx(pj, [])
    recursos = TurnResources()
    assert not accion.can_use(recursos, ctx)      # sin Furia
    _barb(pj).rage_active = True
    assert accion.can_use(recursos, ctx)
    recursos.bonus_action_used = True
    assert not accion.can_use(recursos, ctx)      # acción bonus gastada


def test_spike_action_can_use_requiere_nivel_3():
    pj = _pj()
    _barrer(pj, level=2)
    _barb(pj).rage_active = True
    accion = _accion_puas(pj)
    assert not accion.can_use(TurnResources(), _ctx(pj, []))


def test_spike_action_execute_con_dano_de_furia():
    pj = _pj()
    orco = _monstruo()
    _barrer(pj, level=5)
    _barb(pj).rage_active = True
    ctx = _ctx(pj, [pj, orco])
    antes = orco.hp
    _accion_puas(pj).execute(ctx)
    perdido = antes - orco.hp
    # Mínimo: 1 (dado) + 3 (FUE 16) + 2 (daño de Furia, nivel 5).
    assert perdido >= 6
    assert pj.state.attacked_this_turn  # extiende la Furia al acabar el turno


def test_sin_furia_la_accion_no_se_ofrece():
    pj = _pj()
    _barrer(pj, level=5)
    assert not _accion_puas(pj).can_use(TurnResources(), _ctx(pj, []))


# --- Spiked Retribution (14) --------------------------------------------------

def test_retribucion_melee_devuelve_tres():
    pj = _pj()
    orco = _monstruo()
    _barrer(pj, level=14)
    _barb(pj).rage_active = True
    antes = orco.hp
    _bj(pj).after_being_hit(pj, orco, AttackRange.MELEE, _ctx(pj))
    assert antes - orco.hp == 3


def test_retribucion_condiciones():
    # Sin Furia.
    pj = _pj()
    orco = _monstruo()
    _barrer(pj, level=14)
    _bj(pj).after_being_hit(pj, orco, AttackRange.MELEE, _ctx(pj))
    assert orco.hp == orco.max_hp
    # Nivel < 14 con Furia.
    pj2 = _pj()
    orco2 = _monstruo()
    _barrer(pj2, level=13)
    _barb(pj2).rage_active = True
    _bj(pj2).after_being_hit(pj2, orco2, AttackRange.MELEE, _ctx(pj2))
    assert orco2.hp == orco2.max_hp
    # A distancia no.
    pj3 = _pj()
    orco3 = _monstruo()
    _barrer(pj3, level=14)
    _barb(pj3).rage_active = True
    _bj(pj3).after_being_hit(pj3, orco3, AttackRange.RANGED, _ctx(pj3))
    assert orco3.hp == orco3.max_hp


def test_retribucion_no_actua_sobre_terceros():
    pj = _pj()
    orco = _monstruo()
    otro = _pj(name="Aliado")
    _barrer(pj, level=14)
    _barb(pj).rage_active = True
    _bj(pj).after_being_hit(otro, orco, AttackRange.MELEE, _ctx(pj))
    assert orco.hp == orco.max_hp


def test_retribucion_respeta_resistencia_a_perforante():
    pj = _pj()
    orco = _monstruo(resistances={"piercing"})
    _barrer(pj, level=14)
    _barb(pj).rage_active = True
    antes = orco.hp
    _bj(pj).after_being_hit(pj, orco, AttackRange.MELEE, _ctx(pj))
    assert antes - orco.hp == 1    # 3 → resistencia → 1

"""Features de la subclase Path of the Berserker del bárbaro (PHB 2024).

Cubre la tabla de features, Frenzy (daño extra), Mindless Rage
(inmunidad + purga), Retaliation (reacción) e Intimidating Presence
(uso gratis diario + pago con Furia).
"""
from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from dnd_sim import (
    Abilities,
    Attack,
    BarbarianFeatures,
    BerserkerFeatures,
    Monster,
    PlayerCharacter,
    apply_barbarian,
    apply_berserker,
)
from dnd_sim.core.enums import AttackRange
from dnd_sim.model.actions import ActionType
from dnd_sim.rules.classes.barbarian import BARBARIAN_CLASS
from dnd_sim.rules.classes.barbarian.features import RageAction
from dnd_sim.rules.classes.barbarian.subclasses.berserker import (
    BERSERKER_FEATURES,
    IntimidatingPresenceAction,
    _golpe_sin_armas,
)
from dnd_sim.rules.conditions import Condition, apply_condition


def _abilities(**kwargs) -> Abilities:
    base = dict(str=10, dex=10, con=10, int=10, wis=10, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    kwargs.setdefault("name", "Thor")
    kwargs.setdefault("max_hp", 500)
    kwargs.setdefault("ac", 15)
    kwargs.setdefault("level", 5)
    kwargs.setdefault("abilities", _abilities())
    kwargs.setdefault("attacks", [Attack("Hacha de batalla", "1d12",
                                         ability="str")])
    return PlayerCharacter(**kwargs)


def _monstruo(**kwargs) -> Monster:
    kwargs.setdefault("name", "Orco")
    kwargs.setdefault("max_hp", 500)
    kwargs.setdefault("ac", 12)
    kwargs.setdefault("abilities", _abilities())
    kwargs.setdefault("attacks", [Attack("Hacha orca", "1d6", ability="str",
                                         attack_bonus=30)])
    return Monster(**kwargs)


def _berserker(pj, level):
    """Aplica clase + subclase y devuelve el rasgo de la subclase."""
    apply_barbarian(pj, level=level)
    return apply_berserker(pj, level=level)


def _barbaro(pj) -> BarbarianFeatures:
    return next(t for t in pj.traits if isinstance(t, BarbarianFeatures))


def _ctx(combatants, round_=1, seed=0, actor=None):
    return SimpleNamespace(combatants=list(combatants), round=round_,
                           rng=random.Random(seed), log=[],
                           **({"actor": actor} if actor is not None else {}))


def _furia_lista(pj, level=5):
    """Subclase aplicada con Furia activa y Ataque Temerario usado."""
    sub = _berserker(pj, level)
    barb = _barbaro(pj)
    barb.activate(1)
    barb.reckless_active = True
    return sub, barb


# --- Tabla y aplicación ------------------------------------------------------

def test_berserker_features_por_nivel():
    assert BERSERKER_FEATURES == {
        3: ("Frenzy",),
        6: ("Mindless Rage",),
        10: ("Retaliation",),
        14: ("Intimidating Presence",),
    }


def test_apply_requiere_clase_barbara():
    with pytest.raises(ValueError, match="apply_barbarian"):
        apply_berserker(_pj())


def test_apply_anade_trait_y_accion():
    pj = _pj(level=5)
    trait = apply_barbarian(pj, level=5)
    sub = apply_berserker(pj)  # nivel por defecto = el del PJ
    assert isinstance(sub, BerserkerFeatures)
    assert sub.level == 5
    assert sub in pj.traits and trait in pj.traits
    accion = next(a for a in pj.actions
                  if isinstance(a, IntimidatingPresenceAction))
    assert accion.action_type is ActionType.BONUS_ACTION
    assert accion.name == "Presencia intimidante"
    assert accion.usage is None  # el límite diario vive en el trait


def test_subclase_registrada_con_min_level_3():
    defs = BARBARIAN_CLASS.subclasses
    assert "berserker" in defs
    assert defs["berserker"].min_level == 3
    assert defs["berserker"].apply is apply_berserker


def test_reset_recupera_uso_diario_y_frenzy():
    pj = _pj()
    sub, _ = _furia_lista(pj)
    sub.presence_usage.spend()
    sub.frenzy_pagado = True
    sub.reset()
    assert sub.presence_usage.available
    assert not sub.frenzy_pagado


# --- Frenzy (3) --------------------------------------------------------------

def test_frenzy_paga_bonus_de_furia():
    pj = _pj()
    monstruo = _monstruo()
    sub, _ = _furia_lista(pj, level=5)
    bonus = sub.extra_attack_damage(pj, monstruo, AttackRange.MELEE,
                                    rng=random.Random(0), atk=pj.attacks[0])
    # rage_damage(5) = 2 → 2d6 (2..12).
    assert isinstance(bonus, int)
    assert 2 <= bonus <= 12


def test_frenzy_solo_primera_acertada_del_turno():
    pj = _pj()
    monstruo = _monstruo()
    sub, _ = _furia_lista(pj, level=5)
    primera = sub.extra_attack_damage(pj, monstruo, AttackRange.MELEE,
                                      rng=random.Random(0), atk=pj.attacks[0])
    segunda = sub.extra_attack_damage(pj, monstruo, AttackRange.MELEE,
                                      rng=random.Random(1), atk=pj.attacks[0])
    assert primera > 0
    assert segunda == 0


def test_frenzy_sin_furia_no_paga():
    pj = _pj()
    monstruo = _monstruo()
    sub = _berserker(pj, level=5)
    bonus = sub.extra_attack_damage(pj, monstruo, AttackRange.MELEE,
                                    rng=random.Random(0), atk=pj.attacks[0])
    assert bonus == 0


def test_frenzy_sin_ataque_temerario_no_paga():
    pj = _pj()
    monstruo = _monstruo()
    sub = _berserker(pj, level=5)
    _barbaro(pj).activate(1)  # Furia sí, Ataque Temerario no
    bonus = sub.extra_attack_damage(pj, monstruo, AttackRange.MELEE,
                                    rng=random.Random(0), atk=pj.attacks[0])
    assert bonus == 0


def test_frenzy_se_paga_en_la_primera_acertada_que_cualifica():
    """Si la primera acertada no cualifica, el siguiente del turno sí paga."""
    pj = _pj()
    monstruo = _monstruo()
    sub = _berserker(pj, level=5)
    barb = _barbaro(pj)
    # 1ª acertada sin Furia: no paga y NO consume el turno…
    assert sub.extra_attack_damage(pj, monstruo, AttackRange.MELEE,
                                   rng=random.Random(0),
                                   atk=pj.attacks[0]) == 0
    # …y con Furia y Temerario activados después, esa misma acertada
    # posterior del turno sí paga.
    barb.activate(1)
    barb.reckless_active = True
    assert sub.extra_attack_damage(pj, monstruo, AttackRange.MELEE,
                                   rng=random.Random(1),
                                   atk=pj.attacks[0]) > 0
    # Una vez pagada, el resto del turno no vuelve a pagar.
    assert sub.extra_attack_damage(pj, monstruo, AttackRange.MELEE,
                                   rng=random.Random(2),
                                   atk=pj.attacks[0]) == 0
    # Al empezar el turno vuelve a evaluar.
    sub.on_turn_start(pj)
    assert sub.extra_attack_damage(pj, monstruo, AttackRange.MELEE,
                                   rng=random.Random(3),
                                   atk=pj.attacks[0]) > 0


def test_frenzy_no_paga_fuera_de_su_turno_ni_en_reacciones():
    pj = _pj()
    monstruo = _monstruo()
    sub, _ = _furia_lista(pj, level=5)
    # Turno ajeno (el ctx lo lleva otro actor).
    assert sub.extra_attack_damage(
        pj, monstruo, AttackRange.MELEE, ctx=SimpleNamespace(actor=monstruo),
        rng=random.Random(0), atk=pj.attacks[0]) == 0
    # Reacción (marcada is_reaction).
    assert sub.extra_attack_damage(
        pj, monstruo, AttackRange.MELEE,
        ctx=SimpleNamespace(actor=pj, is_reaction=True),
        rng=random.Random(1), atk=pj.attacks[0]) == 0
    # Sin pago, el turno sigue disponible para un ataque propio.
    assert sub.extra_attack_damage(pj, monstruo, AttackRange.MELEE,
                                   rng=random.Random(2),
                                   atk=pj.attacks[0]) > 0


def test_frenzy_critico_duplica_dados():
    pj = _pj()
    monstruo = _monstruo()
    sub, _ = _furia_lista(pj, level=5)
    bonus = sub.extra_attack_damage(pj, monstruo, AttackRange.MELEE, crit=True,
                                    rng=random.Random(0), atk=pj.attacks[0])
    assert 4 <= bonus <= 24  # 4d6


def test_frenzy_sin_rng_se_abstiene():
    pj = _pj()
    monstruo = _monstruo()
    sub, _ = _furia_lista(pj, level=5)
    assert sub.extra_attack_damage(pj, monstruo, AttackRange.MELEE, rng=None,
                                   atk=pj.attacks[0]) == 0


def test_frenzy_solo_ataques_de_fuerza():
    pj = _pj()
    monstruo = _monstruo()
    sub, _ = _furia_lista(pj, level=5)
    daga = Attack("Daga", "1d4", ability="dex")
    bonus = sub.extra_attack_damage(pj, monstruo, AttackRange.MELEE,
                                    rng=random.Random(0), atk=daga)
    assert bonus == 0


def test_frenzy_no_paga_en_nivel_minimo_de_subclase():
    # apply_berserker con level explícito por debajo de 3 se recorta a 3;
    # el gate de nivel usa el nivel del trait, no el del PJ.
    pj = _pj(level=1)
    monstruo = _monstruo()
    sub, _ = _furia_lista(pj, level=3)
    bonus = sub.extra_attack_damage(pj, monstruo, AttackRange.MELEE,
                                    rng=random.Random(0), atk=pj.attacks[0])
    assert 2 <= bonus <= 12


# --- Mindless Rage (6) -------------------------------------------------------

def test_mindless_bloquea_charmed_y_frightened_con_furia():
    pj = _pj()
    sub = _berserker(pj, level=6)
    _barbaro(pj).activate(1)
    assert sub.blocks_condition(Condition.CHARMED)
    assert sub.blocks_condition(Condition.FRIGHTENED)
    assert not sub.blocks_condition(Condition.POISONED)


def test_mindless_no_bloquea_sin_furia():
    pj = _pj()
    sub = _berserker(pj, level=6)
    assert not sub.blocks_condition(Condition.CHARMED)
    assert not sub.blocks_condition(Condition.FRIGHTENED)


def test_mindless_no_bloquea_por_debajo_del_nivel_6():
    pj = _pj()
    sub = _berserker(pj, level=3)
    _barbaro(pj).activate(1)
    assert not sub.blocks_condition(Condition.CHARMED)


def test_mindless_purga_al_entrar_en_furia():
    pj = _pj()
    sub = _berserker(pj, level=6)
    ctx = _ctx([pj])
    apply_condition(pj, Condition.CHARMED, ctx)
    apply_condition(pj, Condition.FRIGHTENED, ctx)
    assert pj.conditions.has(Condition.CHARMED)
    sub.on_rage_start(pj, ctx)
    assert not pj.conditions.has(Condition.CHARMED)
    assert not pj.conditions.has(Condition.FRIGHTENED)


def test_furia_via_accion_purga_hechizado():
    pj = _pj()
    _berserker(pj, level=6)
    ctx = _ctx([pj], actor=pj)
    apply_condition(pj, Condition.CHARMED, ctx)
    rage = next(a for a in pj.actions if isinstance(a, RageAction))
    rage.execute(ctx)
    assert _barbaro(pj).rage_active
    assert not pj.conditions.has(Condition.CHARMED)


# --- Retaliation (10) --------------------------------------------------------

def test_retaliation_contraataca_tras_golpe_melee():
    pj = _pj()
    monstruo = _monstruo()
    sub = _berserker(pj, level=10)
    ctx = _ctx([pj, monstruo])
    sub.after_being_hit(pj, monstruo, AttackRange.MELEE, ctx)
    assert pj.state.reaction_used
    assert any("Retaliation" in line for line in ctx.log)


def test_retaliation_una_sola_vez_por_ronda():
    pj = _pj()
    monstruo = _monstruo()
    sub = _berserker(pj, level=10)
    ctx = _ctx([pj, monstruo])
    sub.after_being_hit(pj, monstruo, AttackRange.MELEE, ctx)
    n_logs = len(ctx.log)
    sub.after_being_hit(pj, monstruo, AttackRange.MELEE, ctx)
    assert len(ctx.log) == n_logs  # la reacción ya está gastada


def test_retaliation_ignora_ataques_a_distancia():
    pj = _pj()
    monstruo = _monstruo()
    sub = _berserker(pj, level=10)
    ctx = _ctx([pj, monstruo])
    sub.after_being_hit(pj, monstruo, AttackRange.RANGED, ctx)
    assert not pj.state.reaction_used
    assert not any("Retaliation" in line for line in ctx.log)


def test_retaliation_no_gasta_si_reaccion_ya_usada():
    pj = _pj()
    monstruo = _monstruo()
    sub = _berserker(pj, level=10)
    pj.state.reaction_used = True
    ctx = _ctx([pj, monstruo])
    sub.after_being_hit(pj, monstruo, AttackRange.MELEE, ctx)
    assert not any("Retaliation" in line for line in ctx.log)


def test_golpe_sin_armas_unidad():
    arma = _golpe_sin_armas()
    assert arma.name == "Golpe sin armas"
    assert arma.damage == "1"
    assert arma.ability == "str"
    assert arma.damage_type.value == "bludgeoning"


def test_retaliation_sin_armas_usa_golpe_sin_armas(monkeypatch):
    pj = _pj(attacks=[])
    monstruo = _monstruo()
    sub = _berserker(pj, level=10)
    ctx = _ctx([pj, monstruo])
    capturado = {}

    def _falso_ataque(attacker, target, atk, rng, **kwargs):
        capturado["atk"] = atk

    monkeypatch.setattr("dnd_sim.engine.combat.attack_roll", _falso_ataque)
    sub.after_being_hit(pj, monstruo, AttackRange.MELEE, ctx)
    assert capturado["atk"].name == "Golpe sin armas"
    assert capturado["atk"].damage == "1"


def test_retaliation_sin_rng_no_gasta():
    pj = _pj()
    monstruo = _monstruo()
    sub = _berserker(pj, level=10)
    ctx = SimpleNamespace(combatants=[pj, monstruo], round=1, log=[])
    sub.after_being_hit(pj, monstruo, AttackRange.MELEE, ctx)
    assert not pj.state.reaction_used


# --- Intimidating Presence (14) ----------------------------------------------

def _presencia_ctx(pj, monstruo, seed=0, **kwargs):
    return SimpleNamespace(actor=pj, combatants=[pj, monstruo], round=1,
                           rng=random.Random(seed), log=[], **kwargs)


def test_presencia_requiere_nivel_14():
    pj13 = _pj(level=13)
    apply_barbarian(pj13, level=13)
    acc13 = apply_berserker(pj13, level=13)
    acc13 = next(a for a in pj13.actions
                 if isinstance(a, IntimidatingPresenceAction))
    assert not acc13.can_use(_presencia_ctx(pj13, _monstruo()))

    pj14 = _pj(level=14)
    apply_barbarian(pj14, level=14)
    apply_berserker(pj14, level=14)
    acc14 = next(a for a in pj14.actions
                 if isinstance(a, IntimidatingPresenceAction))
    assert acc14.can_use(_presencia_ctx(pj14, _monstruo()))


def test_presencia_uso_gratis_no_toca_furia(monkeypatch):
    pj = _pj(level=14)
    monstruo = _monstruo()
    apply_barbarian(pj, level=14)
    sub = apply_berserker(pj, level=14)
    ctx = _presencia_ctx(pj, monstruo)
    furia = next(a for a in pj.actions if isinstance(a, RageAction))
    usos_furia_antes = furia.usage.uses_left
    capturado = {}

    def _salvacion_fallida(target, ability, dc, rng, mode=None, **kwargs):
        capturado.update(ability=ability, dc=dc,
                         magical=kwargs.get("magical"))
        return SimpleNamespace(success=False)

    monkeypatch.setattr(
        "dnd_sim.rules.classes.barbarian.subclasses.berserker.saving_throw",
        _salvacion_fallida)
    # Variante gratis forzada (con ambas disponibles compiten con pick).
    monkeypatch.setattr(
        "dnd_sim.rules.classes.barbarian.subclasses.berserker.pick",
        lambda rng, opciones: "gratis")
    accion = next(a for a in pj.actions
                  if isinstance(a, IntimidatingPresenceAction))
    accion.execute(ctx)

    dc_esperado = (8 + pj.abilities.mod("str")
                   + int(getattr(pj, "proficiency", 0) or 0))
    assert capturado == {"ability": "wis", "dc": dc_esperado,
                         "magical": False}
    assert not sub.presence_usage.available  # uso diario gastado
    assert furia.usage.uses_left == usos_furia_antes  # Furia intacta
    assert monstruo.conditions.has(Condition.FRIGHTENED)
    assert any("Presencia intimidante" in line for line in ctx.log)


def test_presencia_uso_adicional_gasta_un_uso_de_furia(monkeypatch):
    pj = _pj(level=14)
    monstruo = _monstruo()
    apply_barbarian(pj, level=14)
    sub = apply_berserker(pj, level=14)
    sub.presence_usage.spend()  # el gratis ya se usó hoy
    ctx = _presencia_ctx(pj, monstruo)
    furia = next(a for a in pj.actions if isinstance(a, RageAction))
    usos_antes = furia.usage.uses_left

    def _salvacion(target, ability, dc, rng, mode=None, **kwargs):
        return SimpleNamespace(success=True)

    monkeypatch.setattr(
        "dnd_sim.rules.classes.barbarian.subclasses.berserker.saving_throw",
        _salvacion)
    accion = next(a for a in pj.actions
                  if isinstance(a, IntimidatingPresenceAction))
    accion.execute(ctx)
    assert furia.usage.uses_left == usos_antes - 1
    # La variante de Furia restaura el uso gratis diario.
    assert sub.presence_usage.available


def test_presencia_sin_usos_no_esta_disponible():
    pj = _pj(level=14)
    monstruo = _monstruo()
    apply_barbarian(pj, level=14)
    sub = apply_berserker(pj, level=14)
    sub.presence_usage.spend()
    furia = next(a for a in pj.actions if isinstance(a, RageAction))
    while furia.usage.available:
        furia.usage.spend()
    accion = next(a for a in pj.actions
                  if isinstance(a, IntimidatingPresenceAction))
    ctx = _presencia_ctx(pj, monstruo)
    assert not accion.can_use(ctx)
    # execute tampoco paga ni loguea (red de seguridad).
    accion.execute(ctx)
    assert not any("Presencia intimidante" in line for line in ctx.log)


def test_presencia_sin_rng_no_paga():
    pj = _pj(level=14)
    monstruo = _monstruo()
    apply_barbarian(pj, level=14)
    sub = apply_berserker(pj, level=14)
    ctx = SimpleNamespace(actor=pj, combatants=[pj, monstruo], round=1,
                          log=[])  # sin rng
    accion = next(a for a in pj.actions
                  if isinstance(a, IntimidatingPresenceAction))
    accion.execute(ctx)
    assert sub.presence_usage.available  # no se pagó nada


def test_presencia_variantes_compiten_con_pick(monkeypatch):
    pj = _pj(level=14)
    monstruo = _monstruo()
    apply_barbarian(pj, level=14)
    sub = apply_berserker(pj, level=14)
    ctx = _presencia_ctx(pj, monstruo)
    capturado = {}

    def _pick(rng, opciones):
        capturado["opciones"] = list(opciones)
        return "furia"  # fuerza la variante que gasta Furia

    monkeypatch.setattr(
        "dnd_sim.rules.classes.barbarian.subclasses.berserker.pick", _pick)
    monkeypatch.setattr(
        "dnd_sim.rules.classes.barbarian.subclasses.berserker.saving_throw",
        lambda *a, **k: SimpleNamespace(success=True))
    furia = next(a for a in pj.actions if isinstance(a, RageAction))
    usos_furia = furia.usage.uses_left
    accion = next(a for a in pj.actions
                  if isinstance(a, IntimidatingPresenceAction))
    accion.execute(ctx)
    assert capturado["opciones"] == ["gratis", "furia"]  # ambas compiten
    assert furia.usage.uses_left == usos_furia - 1
    assert sub.presence_usage.available  # el uso gratis se restaura


def test_presencia_afecta_a_un_numero_aleatorio_de_enemigos(monkeypatch):
    monkeypatch.setattr(
        "dnd_sim.rules.classes.barbarian.subclasses.berserker.pick",
        lambda rng, opciones: "gratis")
    vistos = set()
    for seed in range(30):
        pj = _pj(level=14)
        m1 = _monstruo(name="Orco 1")
        m2 = _monstruo(name="Orco 2")
        apply_barbarian(pj, level=14)
        apply_berserker(pj, level=14)
        ctx = SimpleNamespace(actor=pj, combatants=[pj, m1, m2], round=1,
                              rng=random.Random(seed), log=[])
        accion = next(a for a in pj.actions
                      if isinstance(a, IntimidatingPresenceAction))
        cuentas = []

        def _salvacion(target, ability, dc, rng, mode=None, **kwargs):
            cuentas.append(target)
            return SimpleNamespace(success=True)

        monkeypatch.setattr(
            "dnd_sim.rules.classes.barbarian.subclasses.berserker"
            ".saving_throw", _salvacion)
        accion.execute(ctx)
        vistos.add(len(cuentas))
    assert vistos == {1, 2}, vistos


# --- Nuevos requisitos de Retaliation ---------------------------------------

def test_retaliation_no_contraataca_si_ha_caido():
    pj = _pj()
    monstruo = _monstruo()
    sub = _berserker(pj, level=10)
    ctx = _ctx([pj, monstruo])
    pj.hp = 0
    sub.after_being_hit(pj, monstruo, AttackRange.MELEE, ctx)
    assert not pj.state.reaction_used
    assert not any("Retaliation" in line for line in ctx.log)


def test_retaliation_no_contraataca_a_un_atacante_muerto():
    pj = _pj()
    monstruo = _monstruo()
    sub = _berserker(pj, level=10)
    ctx = _ctx([pj, monstruo])
    monstruo.hp = 0
    sub.after_being_hit(pj, monstruo, AttackRange.MELEE, ctx)
    assert not pj.state.reaction_used


def test_retaliation_ignora_atacante_a_distancia():
    pj = _pj()
    monstruo = _monstruo()
    sub = _berserker(pj, level=10)
    ctx = _ctx([pj, monstruo])
    monstruo.state.at_range = True
    sub.after_being_hit(pj, monstruo, AttackRange.MELEE, ctx)
    assert not pj.state.reaction_used


def test_retaliation_elige_entre_las_armas_dinamicas(monkeypatch):
    pj = _pj(attacks=[])
    monstruo = _monstruo()
    sub = _berserker(pj, level=10)
    pj.dynamic_weapons = [Attack("Cola bestial", "1d6", ability="str")]
    ctx = _ctx([pj, monstruo])
    capturado = {}

    def _falso_ataque(attacker, target, atk, rng, **kwargs):
        capturado["atk"] = atk

    monkeypatch.setattr("dnd_sim.engine.combat.attack_roll", _falso_ataque)
    sub.after_being_hit(pj, monstruo, AttackRange.MELEE, ctx)
    assert capturado["atk"].name == "Cola bestial"


# --- Nuevos requisitos de Mindless Rage -------------------------------------

def test_mindless_purga_todas_las_instancias_de_aterrorizado():
    pj = _pj()
    sub = _berserker(pj, level=6)
    ctx = _ctx([pj])
    apply_condition(pj, Condition.FRIGHTENED, ctx, source="fuente1",
                    duration_rounds=10)
    apply_condition(pj, Condition.FRIGHTENED, ctx, source="fuente2",
                    duration_rounds=3)
    apply_condition(pj, Condition.CHARMED, ctx, source="fuente3")
    aterrorizados = [i for i in pj.conditions.instances
                     if i.condition is Condition.FRIGHTENED]
    assert len(aterrorizados) == 2
    sub.on_rage_start(pj, ctx)
    assert not pj.conditions.has(Condition.FRIGHTENED)
    assert not pj.conditions.has(Condition.CHARMED)
    assert not [i for i in pj.conditions.instances
                if i.condition in (Condition.FRIGHTENED, Condition.CHARMED)]

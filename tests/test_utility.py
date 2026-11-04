"""Utilitarias de combate (UTILITY_ACTION_PROBABILITY): Esquivar, Agarrar y Empujar.

Cubre la puerta de decisión (disponibilidad primero, probabilidad después),
el consumo de RNG (ninguno en 0.0 y en 1.0), la frecuencia configurada, el
efecto de cada utilitaria, su pérdida al incapacitarse y la reproducibilidad.
"""
from __future__ import annotations

import random
from types import SimpleNamespace

from dnd_sim import (
    Abilities, Attack, Monster, PlayerCharacter, RollMode, run_combat,
)
from dnd_sim.core.enums import AttackRange
from dnd_sim.rules import utility
from dnd_sim.rules.conditions import (
    Condition, ConditionInstance, apply_condition,
)
from dnd_sim.rules.roll_modifiers import attack_modifiers, save_modifiers
from dnd_sim.rules.saves import SaveResult
from dnd_sim.rules.usage import begin_turn


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=10, con=14, int=10, wis=10, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(name: str = "Thor") -> PlayerCharacter:
    return PlayerCharacter(
        name=name, max_hp=50, ac=12, level=2, abilities=_abilities(),
        attacks=[Attack("Hacha", "1d12", ability="str")],
    )


def _mon(name: str = "Goblin") -> Monster:
    return Monster(name=name, max_hp=30, ac=12, abilities=_abilities())


def _ctx(actor, combatants, rng):
    return SimpleNamespace(actor=actor, combatants=combatants, rng=rng, log=[])


def _siempre_falla(target, ability, dc, rng, mode=None, *, kind=None,
                   magical=False, **kw) -> SaveResult:
    # Salvación determinista: el resultado no depende de los dados.
    return SaveResult(ability=ability, dc=dc, rolls=[1], bonus=0, total=1,
                      success=False, mode=RollMode.NORMAL)


# --- Puerta de decisión ------------------------------------------------------ #

def test_p_cero_no_consume_rng_ni_sustituye_el_ataque(monkeypatch):
    monkeypatch.setattr(utility, "UTILITY_ACTION_PROBABILITY", 0.0)
    rng = random.Random(7)
    estado = rng.getstate()
    assert utility.debe_usar_utilitaria(rng) is False
    assert rng.getstate() == estado
    pj, mon = _pj(), _mon()
    ctx = _ctx(pj, [pj, mon], rng)
    assert utility.ataque_utilitario(pj, ctx, rng) is False
    assert rng.getstate() == estado
    assert ctx.log == []


def test_p_medio_usa_utilitaria_a_la_frecuencia_configurada(monkeypatch):
    monkeypatch.setattr(utility, "UTILITY_ACTION_PROBABILITY", 0.5)
    rng = random.Random(1)
    aciertos = sum(utility.debe_usar_utilitaria(rng) for _ in range(10_000))
    assert abs(aciertos / 10_000 - 0.5) < 0.03


def test_p_uno_siempre_decide_sin_consumir_rng(monkeypatch):
    monkeypatch.setattr(utility, "UTILITY_ACTION_PROBABILITY", 1.0)
    rng = random.Random(3)
    estado = rng.getstate()
    assert all(utility.debe_usar_utilitaria(rng) for _ in range(50))
    assert rng.getstate() == estado


def test_actor_no_disponible_no_consulta_la_probabilidad(monkeypatch):
    # Disponibilidad primero: muerto no llega a la tirada de decisión.
    monkeypatch.setattr(utility, "UTILITY_ACTION_PROBABILITY", 0.5)
    rng = random.Random(11)
    pj, mon = _pj(), _mon()
    pj.hp = 0
    ctx = _ctx(pj, [pj, mon], rng)
    estado = rng.getstate()
    assert utility.ataque_utilitario(pj, ctx, rng) is False
    assert rng.getstate() == estado
    assert ctx.log == []


# --- Agarrar / Empujar -------------------------------------------------------- #

def test_agarrar_aplica_agarrado_con_escape_de_acción(monkeypatch):
    monkeypatch.setattr(utility, "UTILITY_ACTION_PROBABILITY", 1.0)
    monkeypatch.setattr(utility, "saving_throw", _siempre_falla)
    rng = random.Random(5)
    pj, mon = _pj(), _mon()
    # Derribado: vacía el pool de empujar y fija el tipo «agarrar».
    apply_condition(mon, Condition.PRONE, None)
    ctx = _ctx(pj, [pj, mon], rng)
    assert utility.ataque_utilitario(pj, ctx, rng) is True
    instancias = [i for i in mon.conditions.instances
                  if i.condition is Condition.GRAPPLED]
    assert len(instancias) == 1
    inst = instancias[0]
    assert inst.source is pj
    assert inst.escape.abilities == ("str", "dex")
    assert inst.escape.dc == 8 + pj.abilities.mod("str") + pj.proficiency
    assert inst.escape.consumes_action is True
    assert any("intenta agarrar" in linea for linea in ctx.log)


def test_quien_ya_agarra_no_agarra_de_nuevo_y_empuja(monkeypatch):
    monkeypatch.setattr(utility, "UTILITY_ACTION_PROBABILITY", 1.0)
    monkeypatch.setattr(utility, "saving_throw", _siempre_falla)
    rng = random.Random(9)
    pj, mon = _pj(), _mon()
    # Ya tiene agarrada a esta criatura: el pool de agarrar queda vacío.
    mon.conditions.add(ConditionInstance(Condition.GRAPPLED, source=pj))
    ctx = _ctx(pj, [pj, mon], rng)
    assert utility.ataque_utilitario(pj, ctx, rng) is True
    assert any("intenta empujar" in linea for linea in ctx.log)
    assert Condition.PRONE in mon.conditions.active()
    instancias = [i for i in mon.conditions.instances
                  if i.condition is Condition.GRAPPLED]
    assert len(instancias) == 1  # no se aplica una segunda instancia
    empujado = [i for i in mon.conditions.instances
                if i.condition is Condition.PRONE][0]
    assert empujado.source is pj
    assert empujado.escape.dc == 10
    assert empujado.escape.consumes_action is False


def test_sin_pools_disponibles_no_consume_rng(monkeypatch):
    # Ya agarrando + objetivo derribado: no hay nada que hacer.
    monkeypatch.setattr(utility, "UTILITY_ACTION_PROBABILITY", 1.0)
    rng = random.Random(13)
    pj, mon = _pj(), _mon()
    mon.conditions.add(ConditionInstance(Condition.GRAPPLED, source=pj))
    apply_condition(mon, Condition.PRONE, None)
    ctx = _ctx(pj, [pj, mon], rng)
    estado = rng.getstate()
    assert utility.ataque_utilitario(pj, ctx, rng) is False
    assert rng.getstate() == estado
    assert ctx.log == []


def test_ataque_a_distancia_no_se_sustituye(monkeypatch):
    monkeypatch.setattr(utility, "UTILITY_ACTION_PROBABILITY", 1.0)
    rng = random.Random(17)
    pj, mon = _pj(), _mon()
    ctx = _ctx(pj, [pj, mon], rng)
    arco = Attack("Arco", "1d8", ability="dex", range_type=AttackRange.RANGED)
    estado = rng.getstate()
    assert utility.ataque_utilitario(pj, ctx, rng, atk=arco) is False
    assert rng.getstate() == estado
    assert ctx.log == []


def test_agarrar_admite_hasta_un_tamano_mayor(monkeypatch):
    """Un objetivo un tamaño mayor (medium → large) sí se puede agarrar."""
    monkeypatch.setattr(utility, "UTILITY_ACTION_PROBABILITY", 1.0)
    monkeypatch.setattr(utility, "saving_throw", _siempre_falla)
    rng = random.Random(21)
    pj = _pj()
    ogro = _mon("Ogro")
    ogro.size = "large"
    # Derribado: vacía pool_empujar y fuerza la vía Agarrar.
    apply_condition(ogro, Condition.PRONE, None)
    ctx = _ctx(pj, [pj, ogro], rng)
    assert utility.ataque_utilitario(pj, ctx, rng) is True
    assert any("intenta agarrar a Ogro" in l for l in ctx.log)
    assert any(i.condition is Condition.GRAPPLED
               for i in ogro.conditions.instances)


def test_agarrar_no_alcanza_dos_tamanos_mayores(monkeypatch):
    """medium no agarra a huge (dos tamaños más grande): solo Empujar."""
    monkeypatch.setattr(utility, "UTILITY_ACTION_PROBABILITY", 1.0)
    monkeypatch.setattr(utility, "saving_throw", _siempre_falla)
    rng = random.Random(23)
    pj = _pj()
    dragon = _mon("Dragón")
    dragon.size = "huge"
    ctx = _ctx(pj, [pj, dragon], rng)
    assert utility.ataque_utilitario(pj, ctx, rng) is True
    assert any("intenta empujar a Dragón" in l for l in ctx.log)
    assert not any(i.condition is Condition.GRAPPLED
                   for i in dragon.conditions.instances)
    assert Condition.PRONE in dragon.conditions.active()


# --- Esquivar ----------------------------------------------------------------- #

def test_esquivar_activa_el_estado_y_bloquea_la_siguiente_utilitaria():
    pj = _pj()
    ctx = SimpleNamespace(actor=pj, log=[])
    utility.DodgeAction().execute(ctx)
    assert pj.state.dodging is True
    assert any("esquiva" in linea for linea in ctx.log)
    # Ya esquivando: no se vuelve a ofrecer hasta su próximo turno.
    assert utility.hay_utilitaria_accion(pj) is False


def test_esquivar_da_desventaja_ataques_y_ventaja_en_destreza():
    atacante, objetivo = _pj(), _mon()
    atk = Attack("Hacha", "1d12", ability="str")
    objetivo.state.dodging = True
    mods = attack_modifiers(atacante, objetivo, atk, AttackRange.MELEE)
    assert "Esquivar" in mods.disadvantage_sources
    assert "Esquivar" in save_modifiers(objetivo, "dex").advantage_sources
    assert "Esquivar" not in save_modifiers(objetivo, "str").advantage_sources
    # Incapacitado: la esquiva se pierde al instante.
    apply_condition(objetivo, Condition.INCAPACITATED, None)
    mods2 = attack_modifiers(atacante, objetivo, atk, AttackRange.MELEE)
    assert "Esquivar" not in mods2.disadvantage_sources
    assert "Esquivar" not in save_modifiers(
        objetivo, "dex").advantage_sources


def test_esquiva_se_limpia_al_inicio_del_turno_y_en_reset():
    pj = _pj()
    pj.state.dodging = True
    pj.reset()
    assert pj.state.dodging is False
    pj.state.dodging = True
    ctx = SimpleNamespace(rng=random.Random(1), log=[], round=1)
    begin_turn(pj, ctx)
    assert pj.state.dodging is False


# --- Regla PHB 2024 de Agarrado ----------------------------------------------- #

def test_atacante_agarrado_tiene_desventaja_salvo_contra_su_agarrador():
    atacante = _pj()
    agarrador, otro = _mon("Agarrador"), _mon("Otro")
    atacante.conditions.add(
        ConditionInstance(Condition.GRAPPLED, source=agarrador))
    atk = Attack("Hacha", "1d12", ability="str")
    mods_otro = attack_modifiers(atacante, otro, atk, AttackRange.MELEE)
    assert "atacante agarrado" in mods_otro.disadvantage_sources
    mods_agarrador = attack_modifiers(
        atacante, agarrador, atk, AttackRange.MELEE)
    assert "atacante agarrado" not in mods_agarrador.disadvantage_sources


# --- Integración -------------------------------------------------------------- #

def test_combate_con_p_cero_no_usa_utilitarias(monkeypatch):
    monkeypatch.setattr(utility, "UTILITY_ACTION_PROBABILITY", 0.0)
    resultado = run_combat([_pj(), _mon()], random.Random(42),
                           verbose=True, max_rounds=5)
    assert "Esquivar" not in resultado.action_uses
    assert not any("esquiva" in linea or "intenta agarrar" in linea
                   or "intenta empujar" in linea
                   for linea in resultado.log)


def test_combate_con_p_uno_esquiva_como_accion(monkeypatch):
    monkeypatch.setattr(utility, "UTILITY_ACTION_PROBABILITY", 1.0)
    resultado = run_combat([_pj(), _mon()], random.Random(42),
                           verbose=True, max_rounds=5)
    assert resultado.action_uses.get("Esquivar", 0) > 0
    assert any("esquiva" in linea for linea in resultado.log)


def test_reproducibilidad_con_utilitarias(monkeypatch):
    monkeypatch.setattr(utility, "UTILITY_ACTION_PROBABILITY", 0.3)

    def _correr():
        return run_combat([_pj(), _mon()], random.Random(99),
                          verbose=True, max_rounds=6)

    a, b = _correr(), _correr()
    assert a.log == b.log
    assert a.action_uses == b.action_uses
    assert a.survivors == b.survivors

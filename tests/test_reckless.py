"""Ataque Temerario: decisión aleatoria por turno (RECKLESS_USE_PROBABILITY).

Cubre la frecuencia configurada, el consumo de RNG (uno por turno, ninguno
en 0.0/1.0), una sola decisión por turno, la exclusión de reacciones y
turnos ajenos, el efecto sobre las tiradas y la reproducibilidad.
"""
from __future__ import annotations

import random
from types import SimpleNamespace

from dnd_sim import (
    Abilities, Attack, AttackModifiers, BarbarianFeatures, PlayerCharacter,
    RollMode,
)
from dnd_sim.core.dice import roll_d20


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=10, con=14, int=10, wis=10, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj() -> PlayerCharacter:
    return PlayerCharacter(
        name="Thor", max_hp=50, ac=12, level=2, abilities=_abilities(),
        attacks=[Attack("Hacha", "1d12", ability="str")],
    )


def _trait(level: int = 2, probability: float | None = None):
    pj = _pj()
    trait = BarbarianFeatures(name="Bárbaro", level=level)
    if probability is not None:
        trait.reckless_probability = probability
    trait.owner = pj
    pj.traits.append(trait)
    return trait, pj


def _ctx(pj, rng, actor=None):
    return SimpleNamespace(actor=pj if actor is None else actor, round=1,
                           rng=rng, log=[])


def _decide(trait, pj, rng, atk=None):
    mods = AttackModifiers()
    trait.modify_attack_modifiers(
        mods, pj, _pj(), "melee", ctx=_ctx(pj, rng), rng=rng,
        atk=atk or pj.attacks[0],
    )
    return mods


def _turno(trait, pj):
    """Simula el inicio del turno propio (resetea la decisión)."""
    trait.on_turn_start(pj)


# --- Frecuencia --------------------------------------------------------------

def test_frecuencia_0_5_es_aproximadamente_la_mitad_de_los_turnos():
    trait, pj = _trait(probability=0.5)
    rng = random.Random(42)
    positivas = 0
    for _ in range(10000):
        _turno(trait, pj)
        _decide(trait, pj, rng)
        if trait.reckless_active:
            positivas += 1
    assert abs(positivas / 10000 - 0.5) <= 0.03, positivas


# --- Consumo de RNG ----------------------------------------------------------

def test_p_0_y_1_no_consumen_rng():
    for p in (0.0, 1.0):
        trait, pj = _trait(probability=p)
        rng = random.Random(7)
        _turno(trait, pj)
        antes = rng.getstate()
        _decide(trait, pj, rng)
        assert rng.getstate() == antes, f"p={p} consumió RNG"
        assert trait.reckless_decided is True
        assert trait.reckless_active is (p == 1.0)


def test_otra_probabilidad_consume_exactamente_una_tirada():
    trait, pj = _trait(probability=0.5)
    rng = random.Random(3)
    _turno(trait, pj)
    antes = rng.getstate()
    _decide(trait, pj, rng)
    despues = rng.getstate()
    esperado = random.Random()
    esperado.setstate(antes)
    esperado.random()  # exactamente UNA tirada
    assert despues == esperado.getstate()


def test_una_sola_decision_por_turno_con_extra_attack():
    trait, pj = _trait(probability=0.5)
    rng = random.Random(5)
    _turno(trait, pj)
    _decide(trait, pj, rng)          # primera tirada de FUE: decide
    estado = rng.getstate()
    primera = trait.reckless_active
    mods = _decide(trait, pj, rng)   # segunda tirada (Extra Attack)
    assert rng.getstate() == estado  # sin nueva tirada de azar
    assert trait.reckless_active is primera
    assert ("Ataque Temerario" in mods.advantage_sources) is primera


# --- Exclusiones -------------------------------------------------------------

def test_las_reacciones_no_deciden_ni_reciben():
    trait, pj = _trait(probability=1.0)
    rng = random.Random(1)
    mods = AttackModifiers()
    ctx = SimpleNamespace(actor=pj, round=1, rng=rng, log=[],
                          is_reaction=True)
    trait.modify_attack_modifiers(mods, pj, _pj(), "melee", ctx=ctx,
                                  rng=rng, atk=pj.attacks[0])
    assert trait.reckless_decided is False
    assert trait.reckless_active is False
    assert mods.advantage_sources == []
    # Tampoco recibe la ventaja si el turno propio la tiene activa.
    trait.reckless_active = True
    mods2 = AttackModifiers()
    trait.modify_attack_modifiers(mods2, pj, _pj(), "melee", ctx=ctx,
                                  rng=rng, atk=pj.attacks[0])
    assert mods2.advantage_sources == []


def test_en_turno_ajeno_no_decide():
    trait, pj = _trait(probability=1.0)
    rng = random.Random(1)
    otro = _pj()
    mods = AttackModifiers()
    trait.modify_attack_modifiers(mods, pj, _pj(), "melee",
                                  ctx=_ctx(pj, rng, actor=otro), rng=rng,
                                  atk=pj.attacks[0])
    assert trait.reckless_decided is False
    assert mods.advantage_sources == []


def test_antes_del_nivel_2_no_hay_decision_ni_rng():
    trait, pj = _trait(level=1, probability=1.0)
    rng = random.Random(1)
    antes = rng.getstate()
    mods = _decide(trait, pj, rng)
    assert rng.getstate() == antes
    assert trait.reckless_decided is False
    assert mods.advantage_sources == []


def test_sin_ataques_de_fue_no_decide():
    trait, pj = _trait(probability=1.0)
    rng = random.Random(1)
    mods = AttackModifiers()
    trait.modify_attack_modifiers(mods, pj, _pj(), "melee",
                                  ctx=_ctx(pj, rng), rng=rng,
                                  atk=Attack("Daga", "1d4", ability="dex"))
    assert trait.reckless_decided is False
    assert mods.advantage_sources == []


# --- Efecto sobre las tiradas ------------------------------------------------

def test_tasa_de_acierto_ventaja_75_y_normal_50():
    """Con AC equivalente a 50% normal: ventaja ≈ 75% (±2 puntos)."""
    trait, pj = _trait(probability=1.0)
    rng = random.Random(11)
    _turno(trait, pj)
    mods = _decide(trait, pj, rng)
    assert mods.mode is RollMode.ADVANTAGE
    ventaja = sum(
        roll_d20(rng, RollMode.ADVANTAGE).value >= 11 for _ in range(4000))
    assert abs(ventaja / 4000 - 0.75) <= 0.02, ventaja

    _turno(trait, pj)
    trait.reckless_probability = 0.0
    mods2 = _decide(trait, pj, rng)
    assert mods2.mode is RollMode.NORMAL
    normal = sum(
        roll_d20(rng, RollMode.NORMAL).value >= 11 for _ in range(4000))
    assert abs(normal / 4000 - 0.5) <= 0.02, normal


def test_los_ataques_contra_el_no_tienen_ventaja_sin_decision():
    trait, pj = _trait(probability=0.0)
    rng = random.Random(2)
    _turno(trait, pj)
    _decide(trait, pj, rng)
    assert pj.grants_advantage_to_attackers is False
    _turno(trait, pj)
    trait.reckless_probability = 1.0
    _decide(trait, pj, rng)
    assert pj.grants_advantage_to_attackers is True
    # Y se apaga al empezar el siguiente turno.
    _turno(trait, pj)
    assert pj.grants_advantage_to_attackers is False


# --- Reproducibilidad --------------------------------------------------------

def test_misma_semilla_produce_las_mismas_decisiones():
    def serie(semilla: int) -> list[bool]:
        trait, pj = _trait(probability=0.5)
        rng = random.Random(semilla)
        resultado = []
        for _ in range(200):
            _turno(trait, pj)
            _decide(trait, pj, rng)
            resultado.append(trait.reckless_active)
        return resultado

    assert serie(99) == serie(99)

"""Punto de sustitución del ataque: duck-typing ``sustituir_ataque``.

El motor consulta a los rasgos del atacante (patrón ``resolver_maestria``,
sin hook en HOOK_NAMES). Sin rasgos o con ``None`` el flujo es idéntico y
no consume RNG; un resultado no-None se devuelve sin tirar d20.
"""
from __future__ import annotations

import random

from dnd_sim import Abilities, Attack, Monster, PlayerCharacter
from dnd_sim.core.enums import AttackRange
from dnd_sim.engine.combat import attack_roll
from dnd_sim.engine.combat.attack import _sustituir_ataque
from dnd_sim.rules.traits.base import AtaqueSustituido, Trait


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=10, wis=12, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Legolas", max_hp=70, ac=15, level=5, abilities=_abilities(),
        attacks=[Attack("Arco corto", "1d6", ability="dex",
                        range_type=AttackRange.RANGED)],
    )
    defaults.update(kwargs)
    return PlayerCharacter(**defaults)


def _blanco() -> Monster:
    return Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())


class _RngExplota:
    """Cualquier consulta al RNG revienta el test."""

    def __getattr__(self, nombre: str):
        raise AssertionError(f"RNG consultado: {nombre}")


class _RasgoSinSustitucion(Trait):
    """Define el método pero devuelve None: flujo normal."""

    def sustituir_ataque(self, attacker, target, atk, rango, *,
                         ctx=None, rng=None):
        return None


class _RasgoQueSustituye(Trait):
    def __init__(self, motivo: str = "Prueba"):
        self.motivo = motivo

    def sustituir_ataque(self, attacker, target, atk, rango, *,
                         ctx=None, rng=None):
        return AtaqueSustituido(self.motivo)


def test_sin_rasgo_que_sustituya_devuelve_none_sin_rng():
    pj = _pj()
    assert not any(hasattr(t, "sustituir_ataque") for t in pj.traits)
    resultado = _sustituir_ataque(pj, _blanco(), pj.attacks[0],
                                  AttackRange.RANGED, None, _RngExplota())
    assert resultado is None


def test_rasgo_que_devuelve_none_conserva_el_flujo_y_las_semillas():
    """Sin sustitución real: mismo PV y mismo log con la misma semilla."""
    log_a: list[str] = []
    log_b: list[str] = []
    a = _pj()
    b = _pj()
    b.traits.append(_RasgoSinSustitucion())
    blanco_a, blanco_b = _blanco(), _blanco()

    attack_roll(a, blanco_a, a.attacks[0], random.Random(7), log=log_a)
    attack_roll(b, blanco_b, b.attacks[0], random.Random(7), log=log_b)

    assert blanco_a.hp == blanco_b.hp
    assert log_a == log_b


def test_resultado_sustituido_se_devuelve_sin_tirar_d20():
    pj = _pj()
    pj.traits.append(_RasgoQueSustituye("Piercing Arrow"))
    # RNG que revienta: la sustitución ocurre antes de tocar el d20.
    resultado = attack_roll(pj, _blanco(), pj.attacks[0], _RngExplota())
    assert isinstance(resultado, AtaqueSustituido)
    assert resultado.motivo == "Piercing Arrow"

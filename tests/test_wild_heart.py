"""Tests de la subclase Path of the Wild Heart del bárbaro (PHB 2024).

Cubre el hook ``grant_attack_modifiers`` (no regresión) y, en los
bloques siguientes, la tabla de rasgos, Bear/Eagle/Wolf (Rage of the
Wilds), Lion/Ram (Power of the Wilds), la renovación de opciones por
activación, los niveles inferiores y la reproducibilidad.
"""
from __future__ import annotations

import random
from types import SimpleNamespace

from dnd_sim import Abilities, Attack, PlayerCharacter, Monster
from dnd_sim.core.enums import AttackRange
from dnd_sim.rules.roll_modifiers import attack_modifiers
from dnd_sim.rules.traits import HOOK_NAMES, hooks


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=10, con=14, int=10, wis=10, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(level: int = 5) -> PlayerCharacter:
    return PlayerCharacter(
        name="Thor", max_hp=500, ac=15, level=level, abilities=_abilities(),
        attacks=[Attack("Hacha de batalla", "1d12", ability="str")],
    )


def _mon(name: str = "Orco") -> Monster:
    return Monster(name=name, max_hp=500, ac=12, abilities=_abilities())


def _aliado(name: str = "Aliado") -> PlayerCharacter:
    return PlayerCharacter(name=name, max_hp=400, ac=14, level=5,
                           abilities=_abilities(),
                           attacks=[Attack("Espada larga", "1d8",
                                           ability="str")])


def _ctx(actor, combatants, seed=0):
    return SimpleNamespace(actor=actor, combatants=list(combatants),
                           rng=random.Random(seed), log=[], round=1)


# --- No regresión del hook grant_attack_modifiers ----------------------------

def test_el_motor_reconoce_el_hook_grant_attack_modifiers():
    from dnd_sim import apply_barbarian
    assert "grant_attack_modifiers" in HOOK_NAMES
    pj = _pj()
    apply_barbarian(pj, level=5)
    # Sin subclase que lo sobrescriba, el despacho no devuelve rasgos.
    assert hooks(pj.traits, "grant_attack_modifiers") == []


def test_sin_subclase_los_ataques_no_consumen_rng_ni_cambian_el_modo():
    # PJ sin subclase ni rasgos que sobrescriban el hook.
    atacante = _aliado()
    objetivo = _mon()
    atk = atacante.attacks[0]
    ctx = _ctx(atacante, [atacante, objetivo])
    modo_directo = attack_modifiers(atacante, objetivo, atk,
                                    AttackRange.MELEE).mode
    rng = random.Random(7)
    esperado = random.Random(7)
    mods = attack_modifiers(atacante, objetivo, atk, AttackRange.MELEE,
                            ctx=ctx, rng=rng)
    # Mismo resultado que sin contexto y el RNG intacto.
    assert mods.mode is modo_directo
    assert rng.random() == esperado.random()

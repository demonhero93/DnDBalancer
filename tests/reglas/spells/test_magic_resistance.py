# -*- coding: utf-8 -*-
"""Resistencia mágica: ventaja en salvaciones contra hechizos (bloque B).

Sin red: monstruos de los fixtures de la caché y hechizos de
``tests/fixtures/spells/``. Los únicos objetos definidos a mano son los
combatientes de prueba.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import pytest

from dnd_sim import (Abilities, Attack, BarbarianFeatures, FormOfTheBeast,
                     Monster, PlayerCharacter, apply_barbarian, apply_beast,
                     load_monster)
from dnd_sim.core.dice import RollMode
from dnd_sim.data.spell_parser import parse_spell
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.rules import saves as saves_mod
from dnd_sim.rules.conditions import (Condition, ConditionEffect,
                                      ConditionInstance, end_turn)
from dnd_sim.rules.legendary import LegendaryState
from dnd_sim.rules.roll_modifiers import save_modifiers
from dnd_sim.rules.saves import SaveDamage, apply_save_damage, saving_throw
from dnd_sim.rules.spells.casting import Spellcasting, spell_action

CD = 11
N = 20_000
FIXTURES = Path(__file__).parents[2] / "fixtures" / "spells"


def _objetivo(**kwargs):
    return Monster(name="M", max_hp=50, ac=12, proficiency=2,
                   abilities=Abilities(dex=10, wis=10), **kwargs)


def _tasa(target, magical, n=N):
    rng = random.Random(1)
    exitos = sum(1 for _ in range(n)
                 if saving_throw(target, "dex", CD, rng, magical=magical).success)
    return exitos / n


def _pj(**kwargs):
    kwargs.setdefault("name", "PJ")
    kwargs.setdefault("max_hp", 50)
    kwargs.setdefault("ac", 10)
    return PlayerCharacter(**kwargs)


def _ctx(actor, combatants, rng=None):
    return CombatContext(rng=rng or random.Random(1), actor=actor,
                         combatants=list(combatants), round=1,
                         log=None, verbose=False, resources=TurnResources())


def _spell_data(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _spellcasting(level: int = 1) -> Spellcasting:
    return Spellcasting(ability="int", save_dc=20, attack_bonus=12, level=level)


# --- B1: mecánica ------------------------------------------------------------ #

def test_el_rasgo_anade_la_fuente_resistencia_magica():
    m = _objetivo(magic_resistance=True)
    mods = save_modifiers(m, "dex", magical=True)
    assert "Resistencia mágica" in mods.advantage_sources
    assert mods.mode is RollMode.ADVANTAGE


def test_sin_efecto_magico_o_sin_rasgo_no_anade_ventaja():
    con_rasgo = _objetivo(magic_resistance=True)
    mods = save_modifiers(con_rasgo, "dex", magical=False)
    assert "Resistencia mágica" not in mods.advantage_sources
    assert mods.mode is RollMode.NORMAL
    sin_rasgo = _objetivo()
    mods = save_modifiers(sin_rasgo, "dex", magical=True)
    assert "Resistencia mágica" not in mods.advantage_sources
    assert mods.mode is RollMode.NORMAL


def test_probabilidades_50_75_50():
    """CD 11 con bonus 0: ~50% normal; ~75% con ventaja de la Resistencia
    mágica; ~50% si la salvación no es mágica."""
    sin = _objetivo()
    con = _objetivo(magic_resistance=True)
    assert abs(_tasa(sin, True) - 0.50) < 0.015
    assert abs(_tasa(con, True) - 0.75) < 0.015
    assert abs(_tasa(con, False) - 0.50) < 0.015


def test_ventaja_y_desventaja_se_anulan():
    m = _objetivo(magic_resistance=True)
    m.saves_with_disadvantage.add("dex")  # efecto fijo de desventaja
    mods = save_modifiers(m, "dex", magical=True)
    assert mods.mode is RollMode.NORMAL
    assert abs(_tasa(m, True) - 0.50) < 0.015


def test_dos_ventajas_y_una_desventaja_tambien_se_anulan():
    """Regla clásica: ventaja y desventaja se cancelan sin contar fuentes."""
    m = _objetivo(magic_resistance=True)
    m.saves_with_advantage.add("dex")
    m.saves_with_disadvantage.add("dex")
    assert abs(_tasa(m, True) - 0.50) < 0.015


def test_aturdido_falla_fue_des_sin_tirar_dados_y_con_ventaja_en_sab():
    m = _objetivo(magic_resistance=True)
    m.conditions.add(ConditionInstance(condition=Condition.STUNNED))
    rng = random.Random(7)
    antes = rng.getstate()
    sr = saving_throw(m, "str", CD, rng, magical=True)
    assert sr.auto_fail and not sr.success
    assert rng.getstate() == antes  # ni un dado, ni un consumo de RNG
    sr_sab = saving_throw(m, "wis", CD, rng, magical=True)
    assert not sr_sab.auto_fail
    assert sr_sab.mode is RollMode.ADVANTAGE


def test_la_resistencia_legendaria_convierte_el_fallo_tras_la_ventaja():
    m = _objetivo(magic_resistance=True)
    m.legendary = LegendaryState(resistance_max=3, resistance_left=3,
                                 resistance_probability=1.0)
    sr = saving_throw(m, "dex", 30, random.Random(3), magical=True)
    assert sr.success and sr.legendary_resistance_used


def test_sin_magic_resistance_el_flag_no_cambia_el_rng():
    m = _objetivo()
    r1, r2 = random.Random(5), random.Random(5)
    sr1 = saving_throw(m, "dex", CD, r1)
    sr2 = saving_throw(m, "dex", CD, r2, magical=True)
    assert sr1.rolls == sr2.rolls and sr1.success == sr2.success
    assert r1.getstate() == r2.getstate()


# --- B2: cada camino pasa magical=True --------------------------------------- #

def test_save_damage_magical_da_ventaja_y_el_no_magical_no():
    objetivo = _objetivo(magic_resistance=True)
    efecto = SaveDamage(ability="dex", dc=CD, damage="2d6", damage_type="fire",
                        magical=True)
    out = apply_save_damage(None, objetivo, efecto, 7, _ctx(objetivo, [objetivo]))
    assert out.save.mode is RollMode.ADVANTAGE
    efecto_frio = SaveDamage(ability="dex", dc=CD, damage="2d6",
                             damage_type="cold", magical=False)
    out2 = apply_save_damage(None, objetivo, efecto_frio, 7,
                             _ctx(objetivo, [objetivo]))
    assert out2.save.mode is RollMode.NORMAL


def test_condition_action_de_hechizo_pasa_magical(monkeypatch):
    """La acción de condición (hechizo) pasa magical=True a la salvación y
    a la instancia que se queda (para sus repeticiones)."""
    registros = []
    real = saves_mod.saving_throw

    def spy(target, ability, dc, rng, mode=None, *, kind=None, magical=False, **kw):
        registros.append(magical)
        return real(target, ability, dc, rng, mode, kind=kind, magical=magical)

    monkeypatch.setattr(saves_mod, "saving_throw", spy)
    from dnd_sim.rules.conditions import ConditionAction
    actor = Monster(name="Lanzador", max_hp=50, ac=10, proficiency=2,
                    abilities=Abilities(int=16))
    objetivo = _pj()
    efecto = ConditionEffect(condition=Condition.RESTRAINED, save_ability="dex",
                             dc=30, duration_rounds=1, magical=True)
    accion = ConditionAction(effect=efecto, name="Cadena de hadas")
    accion.execute(_ctx(actor, [actor, objetivo]))
    assert registros == [True]
    inst = objetivo.conditions.instances[0]
    assert inst.magical is True


def test_end_turn_usa_el_magical_de_la_instancia(monkeypatch):
    registros = []
    real = saves_mod.saving_throw

    def spy(target, ability, dc, rng, mode=None, *, kind=None, magical=False, **kw):
        registros.append(magical)
        return real(target, ability, dc, rng, mode, kind=kind, magical=magical)

    monkeypatch.setattr(saves_mod, "saving_throw", spy)
    objetivo = _objetivo(magic_resistance=True)
    from dnd_sim.rules.conditions import RepeatSave
    objetivo.conditions.add(ConditionInstance(
        condition=Condition.POISONED,
        repeat_save=RepeatSave(ability="con", dc=CD),
        magical=True))
    end_turn(objetivo, _ctx(objetivo, [objetivo]))
    assert registros == [True]


def test_los_riders_de_ataque_pasan_magical(monkeypatch):
    registros = []
    real = saves_mod.saving_throw

    def spy(target, ability, dc, rng, mode=None, *, kind=None, magical=False, **kw):
        registros.append(magical)
        return real(target, ability, dc, rng, mode, kind=kind, magical=magical)

    monkeypatch.setattr(saves_mod, "saving_throw", spy)
    from dnd_sim.engine.combat import attack_roll
    rider = ConditionEffect(condition=Condition.POISONED, save_ability="con",
                            dc=30, duration_rounds=1, magical=True)
    atacante = Monster(
        name="Atacante", max_hp=50, ac=10, proficiency=2,
        abilities=Abilities(str=16),
        attacks=[Attack(
            "Rayo", "1d8", ability="str", damage_type="force",
            attack_bonus=30, magical=True, condition_riders=[rider])])
    objetivo = _pj()
    attack_roll(atacante, objetivo, atacante.attacks[0], random.Random(7),
                None, verbose=False)
    assert registros == [True]


def test_un_truco_de_hechizo_pasa_magical_a_su_salvacion(monkeypatch):
    registros = []
    real = saves_mod.saving_throw

    def spy(target, ability, dc, rng, mode=None, *, kind=None, magical=False, **kw):
        registros.append(magical)
        return real(target, ability, dc, rng, mode, kind=kind, magical=magical)

    monkeypatch.setattr(saves_mod, "saving_throw", spy)
    spell = parse_spell(_spell_data("vicious-mockery"), "Test",
                        _spellcasting(level=1))
    accion = spell_action(spell, _spellcasting(level=1))
    lanzador = _pj(name="Lanzador", abilities=Abilities(cha=16))
    objetivo = _objetivo(magic_resistance=True)
    accion.execute(_ctx(lanzador, [lanzador, objetivo]))
    assert registros == [True]


def test_fiereza_infecciosa_de_la_beast_no_activa_la_ventaja(monkeypatch):
    registros = []
    real = saves_mod.saving_throw

    def spy(target, ability, dc, rng, mode=None, *, kind=None, magical=False, **kw):
        registros.append(magical)
        return real(target, ability, dc, rng, mode, kind=kind, magical=magical)

    monkeypatch.setattr(saves_mod, "saving_throw", spy)
    import dnd_sim.rules.classes.barbarian.subclasses.beast as beast_mod
    monkeypatch.setattr(beast_mod, "saving_throw", spy)
    pj = _pj()
    apply_barbarian(pj, level=10)
    trait = apply_beast(pj, level=10)
    barb = next(t for t in pj.traits if isinstance(t, BarbarianFeatures))
    barb.rage_active = True
    objetivo = _objetivo(magic_resistance=True)
    ctx = _ctx(pj, [pj, objetivo])
    trait.on_rage_start(pj, ctx)
    trait.infectious_uses = 10 ** 9
    arma = trait.natural_attacks[FormOfTheBeast.CLAWS]
    from dnd_sim.core.enums import AttackRange
    trait.after_dealing_hit(objetivo, pj, AttackRange.MELEE, ctx, arma, 7)
    assert registros == [False]  # es un efecto NO mágico: sin ventaja


def test_el_aliento_del_dragon_no_es_magico():
    dragon = load_monster("adult-red-dragon")
    aliento = next(a for a in dragon.actions if "Fire" in getattr(a, "name", ""))
    assert getattr(aliento.effect, "magical", None) is False


# --- B3: loader -------------------------------------------------------------- #

def test_el_loader_fija_magic_resistance():
    assert load_monster("deva").magic_resistance is True
    assert load_monster("unicorn").magic_resistance is True
    assert load_monster("ogre").magic_resistance is False
    # 2024: el rasgo del rakshasa se renombró «Greater Magic Resistance».
    assert load_monster("rakshasa").magic_resistance is True


def test_limited_magic_immunity_solo_avisa(monkeypatch):
    data = json.loads(
        (Path(__file__).parents[3] / "cache" / "monsters" / "ogre.json")
        .read_text(encoding="utf-8"))
    data["special_abilities"] = [{"name": "Limited Magic Immunity"}]
    monkeypatch.setattr("dnd_sim.data.loader.get_monster",
                        lambda *args, **kwargs: data)
    with pytest.warns(UserWarning, match="Limited Magic Immunity"):
        m = load_monster("ogre")
    assert m.magic_resistance is False  # el rasgo no se modela


def test_rakshasa_2024_avisa_de_la_vulnerabilidad_compleja():
    """«piercing ... bless spell»: texto complejo de 2024, fuera de alcance."""
    with pytest.warns(UserWarning, match="complejo"):
        load_monster("rakshasa")

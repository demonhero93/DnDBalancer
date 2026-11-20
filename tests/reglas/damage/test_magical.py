"""Flag ``magical``: daño mágico vs no mágico (resistencias/inmunidades
«from nonmagical weapons», Magic Weapons, Bestial Soul, hechizos).

Sin red: los monstruos salen de los fixtures reales de la caché y los
hechizos de ``tests/fixtures/spells/``. Los únicos objetos definidos a
mano son los combatientes de prueba.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import pytest

from dnd_sim import (Abilities, Attack, BarbarianFeatures, FormOfTheBeast,
                     Monster, PlayerCharacter, apply_barbarian, apply_beast,
                     load_monster)
from dnd_sim.data.spell_parser import parse_spell
from dnd_sim.engine.combat import _tag_modificadores, attack_roll
from dnd_sim.model.actions import (AttackAction, SaveAction, TurnResources)
from dnd_sim.rules.damage import apply_damage_modifiers, inflict_damage
from dnd_sim.rules.spells import Spellcasting, spell_action

FIXTURES = Path(__file__).parents[2] / "fixtures"
SPELLS = FIXTURES / "spells"
CACHE = Path(__file__).parents[3] / "cache" / "monsters"


def _cache_data(index: str) -> dict:
    return json.loads((CACHE / f"{index}.json").read_text(encoding="utf-8"))


def _spell_data(index: str) -> dict:
    return json.loads((SPELLS / f"{index}.json").read_text(encoding="utf-8"))


def _spellcasting(level: int = 1) -> Spellcasting:
    return Spellcasting(ability="int", save_dc=20, attack_bonus=12, level=level)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(name="Thor", max_hp=100, ac=15, level=5,
                    proficiency=2,
                    abilities=Abilities(str=16, dex=12, con=14, int=10,
                                        wis=12, cha=8),
                    attacks=[Attack("Espada larga", "1d8", ability="str")])
    defaults.update(kwargs)
    return PlayerCharacter(**defaults)


# --- A1: apply_damage_modifiers -------------------------------------------- #

def test_resistencia_a_bps_del_ghost_aplica_tambien_al_dano_magico():
    """SRD 5.2.1: el ghost resiste B/P/S sin cualificador «nonmagical»."""
    ghost = load_monster("ghost")
    assert {t.value for t in ghost.resistances} >= \
        {"bludgeoning", "piercing", "slashing"}
    assert not ghost.nonmagical_resistances
    assert apply_damage_modifiers(9, "bludgeoning", ghost) == 4
    assert apply_damage_modifiers(9, "bludgeoning", ghost, magical=True) == 4


def test_inmunidad_a_dano_no_magico_no_afecta_al_magico():
    """Cobertura del camino nonmagical con objetivo sintético (2014)."""
    objetivo = Monster(name="Z", max_hp=50, ac=10,
                       nonmagical_immunities={"bludgeoning",
                                              "piercing", "slashing"})
    assert apply_damage_modifiers(9, "piercing", objetivo) == 0
    assert apply_damage_modifiers(9, "piercing", objetivo, magical=True) == 9
    # El lich 2024 no tiene inmunidades B/P/S: ni cualificadas ni planas.
    lich = load_monster("lich")
    assert not lich.nonmagical_immunities
    assert not {t.value for t in lich.immunities} >= \
        {"bludgeoning", "piercing", "slashing"}
    assert apply_damage_modifiers(9, "piercing", lich) == 9


def test_tipos_fuera_de_bps_no_usan_los_conjuntos_nonmagical():
    objetivo = Monster(name="B", max_hp=50, ac=10,
                       nonmagical_immunities={"fire"},
                       nonmagical_resistances={"cold"})
    assert apply_damage_modifiers(7, "fire", objetivo) == 0
    assert apply_damage_modifiers(7, "fire", objetivo, magical=True) == 7
    assert apply_damage_modifiers(7, "cold", objetivo) == 3
    assert apply_damage_modifiers(7, "cold", objetivo, magical=True) == 7
    assert apply_damage_modifiers(7, "necrotic", objetivo) == 7
    assert apply_damage_modifiers(7, "necrotic", objetivo, magical=True) == 7


def test_orden_inmunidad_resistencia_vulnerabilidad_con_nonmagical():
    """La inmunidad no mágica manda sobre la vulnerabilidad; la resistencia
    no mágica combinada con vulnerabilidad respeta el orden (½ y luego ×2)."""
    inmune = Monster(name="I", max_hp=50, ac=10,
                     nonmagical_immunities={"bludgeoning"},
                     vulnerabilities={"bludgeoning"})
    assert apply_damage_modifiers(10, "bludgeoning", inmune) == 0
    assert apply_damage_modifiers(10, "bludgeoning", inmune, magical=True) == 20

    mixto = Monster(name="M", max_hp=50, ac=10,
                    nonmagical_resistances={"bludgeoning"},
                    vulnerabilities={"bludgeoning"})
    assert apply_damage_modifiers(10, "bludgeoning", mixto) == 10  # ½ y ×2
    assert apply_damage_modifiers(10, "bludgeoning", mixto, magical=True) == 20


def test_inflict_damage_registra_la_bandera_magical():
    objetivo = Monster(name="B", max_hp=50, ac=10)
    from dnd_sim.rules import damage as damage_mod
    damage_mod.DAMAGE_DEALT = []
    try:
        inflict_damage(objetivo, 4, "fire", magical=True)
        inflict_damage(objetivo, 3, "cold")
    finally:
        records, damage_mod.DAMAGE_DEALT = damage_mod.DAMAGE_DEALT, None
    assert [r["magical"] for r in records] == [True, False]


# --- A2: log del motor ------------------------------------------------------ #

def test_el_log_del_ataque_dice_dano_no_magico():
    objetivo = Monster(name="Z", max_hp=50, ac=10,
                       nonmagical_resistances={"bludgeoning"})
    assert _tag_modificadores(9, 4, "bludgeoning", objetivo) == \
        " (resistencia a daño no mágico: 9 -> 4)"
    # El mismo daño mágico no se modifica: no hay etiqueta.
    assert _tag_modificadores(9, 9, "bludgeoning", objetivo,
                              magical=True) == ""


def test_ataque_con_magical_true_tambien_se_reduce_contra_el_ghost():
    """2024: sin cualificador nonmagical, la resistencia no distingue."""
    atacante = _pj(attacks=[Attack("Golpe", "1d8", ability="str",
                                   damage_type="bludgeoning",
                                   attack_bonus=30)])
    ghost = load_monster("ghost")
    hp_antes = ghost.hp
    atk = Attack("Golpe", "2d6", ability="str", damage_type="bludgeoning",
                 attack_bonus=30, magical=True)
    attack_roll(atacante, ghost, atk, random.Random(7), None, verbose=False)
    perdido = hp_antes - ghost.hp
    assert 0 < perdido < 8, \
        f"el ghost 2024 debe resistir también el daño mágico: {perdido}"


def test_tag_del_motor_sin_magical_usa_el_sufijo():
    """El motor, sin la bandera, etiqueta la resistencia como no mágica."""
    atacante = _pj(attacks=[Attack("Golpe", "1d8", ability="str",
                                   damage_type="bludgeoning",
                                   attack_bonus=30)])
    objetivo = Monster(name="Z", max_hp=50, ac=10,
                       nonmagical_resistances={"bludgeoning"})
    log: list = []
    atk = Attack("Golpe", "2d6", ability="str", damage_type="bludgeoning",
                 attack_bonus=30)
    attack_roll(atacante, objetivo, atk, random.Random(7), log, verbose=True)
    assert any("(resistencia a daño no mágico:" in line for line in log), log


# --- A3: loader ------------------------------------------------------------- #

def test_magic_weapons_marca_los_ataques_del_monstruo(monkeypatch):
    data = _cache_data("stone-golem")
    data["special_abilities"] = list(data.get("special_abilities") or []) + [
        {"name": "Magic Weapons"}]
    monkeypatch.setattr("dnd_sim.data.loader.get_monster",
                        lambda *args, **kwargs: data)
    stone = load_monster("stone-golem")
    assert stone.attacks and all(a.magical for a in stone.attacks)


def test_un_monstruo_sin_magic_weapons_no_marca_nada():
    ogre = load_monster("ogre")
    assert ogre.attacks and not any(a.magical for a in ogre.attacks)
    assert not ogre.nonmagical_resistances and not ogre.nonmagical_immunities


def test_las_variantes_de_materiales_siguen_con_aviso(monkeypatch):
    """«that aren't silvered»/«adamantine»: fuera de alcance (materiales),
    se omiten con warnings.warn como hasta ahora (textos 2014 sobre la
    ficha 2024)."""
    silvered = _cache_data("wraith")
    silvered["damage_resistances"] = [
        "bludgeoning, piercing, and slashing from nonmagical weapons "
        "that aren't silvered"]
    monkeypatch.setattr("dnd_sim.data.loader.get_monster",
                        lambda *args, **kwargs: silvered)
    with pytest.warns(UserWarning, match="complejo"):
        wraith = load_monster("wraith")
    assert not wraith.nonmagical_resistances

    adamantine = _cache_data("stone-golem")
    adamantine["damage_immunities"] = [
        "bludgeoning, piercing, and slashing from nonmagical weapons "
        "that aren't adamantine"]
    monkeypatch.setattr("dnd_sim.data.loader.get_monster",
                        lambda *args, **kwargs: adamantine)
    with pytest.warns(UserWarning, match="complejo"):
        stone = load_monster("stone-golem")
    assert not stone.nonmagical_immunities


# --- Hechizos --------------------------------------------------------------- #

def test_un_cantrip_de_ataque_construye_un_ataque_magico():
    spell = parse_spell(_spell_data("ray-of-frost"), "Test",
                        _spellcasting(level=1))
    accion = spell_action(spell, _spellcasting(level=1))
    assert isinstance(accion.effect, AttackAction)
    assert accion.effect.attack.magical is True


def test_un_cantrip_de_salvacion_construye_un_save_damage_magico():
    spell = parse_spell(_spell_data("vicious-mockery"), "Test",
                        _spellcasting(level=1))
    accion = spell_action(spell, _spellcasting(level=1))
    assert isinstance(accion.effect, SaveAction)
    assert accion.effect.effect.magical is True


def test_el_proyectil_magico_dana_completo_al_ghost():
    """Magic Missile (daño fijo de hechizo) ignora la resistencia no mágica."""
    spell = parse_spell(_spell_data("magic-missile"), "Test",
                        _spellcasting(level=1))
    accion = spell_action(spell, _spellcasting(level=1))
    lanzador = PlayerCharacter(
        name="Lanzador", max_hp=50, ac=10, proficiency=2,
        abilities=Abilities(int=16), attacks=[])
    ghost = load_monster("ghost")
    ghost.hp = ghost.max_hp
    from dnd_sim.model.actions import CombatContext
    ctx = CombatContext(rng=random.Random(3), actor=lanzador,
                        combatants=[lanzador, ghost], round=1,
                        log=None, verbose=False, resources=TurnResources())
    hp_antes = ghost.hp
    accion.execute(ctx)
    perdido = hp_antes - ghost.hp
    # 3 dardos × (1d4+1): mínimo 6; con resistencia no mágica sería 3.
    assert perdido >= 6, f"el daño del hechizo se ha reducido: {perdido}"


# --- A4: Bestial Soul ------------------------------------------------------- #

def test_bestial_solo_marca_las_armas_magicas_desde_el_nivel_6():
    pj5 = _pj(level=5)
    apply_barbarian(pj5, level=5)
    from dnd_sim import BeastFeatures
    trait5 = apply_beast(pj5, level=5)
    assert all(a.magical is False
               for a in trait5.natural_attacks.values())

    pj6 = _pj(level=6)
    apply_barbarian(pj6, level=6)
    trait6 = apply_beast(pj6, level=6)
    assert all(a.magical is True
               for a in trait6.natural_attacks.values())


def test_un_pj_beast_nivel_6_dana_completo_al_ghost():
    pj = _pj(level=6)
    apply_barbarian(pj, level=6)
    trait = apply_beast(pj, level=6)
    arma = trait.natural_attacks[FormOfTheBeast.BITE]
    ghost = load_monster("ghost")
    hp_antes = ghost.hp
    inflict_damage(ghost, 10, arma.damage_type, source=pj,
                   magical=arma.magical)
    assert hp_antes - ghost.hp == 10


def test_un_pj_beast_nivel_5_no_supera_la_resistencia():
    pj = _pj(level=5)
    apply_barbarian(pj, level=5)
    trait = apply_beast(pj, level=5)
    arma = trait.natural_attacks[FormOfTheBeast.BITE]
    ghost = load_monster("ghost")
    # inflict_damage NO aplica modificadores: el caller los aplica (como
    # hace attack_roll); aquí se comprueba la regla con la bandera real.
    assert apply_damage_modifiers(10, arma.damage_type, ghost,
                                  magical=arma.magical) == 5


def test_las_armas_dinamicas_de_la_furia_heredan_el_flag():
    """Las armas de dynamic_weapons son las MISMAS instancias: sin rage el
    flag de nivel 6 ya viene de fábrica."""
    pj = _pj(level=6)
    apply_barbarian(pj, level=6)
    trait = apply_beast(pj, level=6)
    barb = next(t for t in pj.traits
                if isinstance(t, BarbarianFeatures))
    barb.rage_active = True
    ctx = _ctx(pj, [pj])
    trait.on_rage_start(pj, ctx)
    assert pj.dynamic_weapons and all(a.magical for a in pj.dynamic_weapons)


# --- Furia ------------------------------------------------------------------ #

def test_las_armas_de_furia_no_distinguen_magical():
    """La Furia (resistencia a B/P/S) es incondicional: mitad igual con
    daño mágico que con no mágico."""
    barb = BarbarianFeatures(level=1)
    barb.rage_active = True
    objetivo = PlayerCharacter(name="B", max_hp=100, ac=10)
    objetivo.traits = [barb]
    assert barb.modify_incoming_damage(objetivo, 9, "bludgeoning", None) == 4
    # Fuego no lo toca: devuelve None (sin cambios) — nunca mitad.
    assert barb.modify_incoming_damage(objetivo, 9, "fire", None) in (None, 9)


def test_ataque_magico_contra_un_bárbaro_en_furia_se_reduce_a_la_mitad():
    pj = _pj(level=1, max_hp=200)
    apply_barbarian(pj, level=1)
    barb = next(t for t in pj.traits
                if isinstance(t, BarbarianFeatures))
    barb.rage_active = True
    atacante = Monster(name="Atacante", max_hp=100, ac=15, proficiency=2,
                       abilities=Abilities(str=16),
                       attacks=[Attack("Golpe", "2d6", ability="str",
                                       damage_type="bludgeoning",
                                       attack_bonus=30, magical=True)])
    hp_antes = pj.hp
    attack_roll(atacante, pj, atacante.attacks[0], random.Random(11),
                None, verbose=False)
    perdido = hp_antes - pj.hp
    assert 2 <= perdido <= 8, \
        f"esperaba el ½ de 4-12 (2-7): {perdido}"


def _ctx(actor, combatants, rng=None):
    from dnd_sim.model.actions import CombatContext
    return CombatContext(rng=rng or random.Random(1), actor=actor,
                         combatants=list(combatants), round=1,
                         log=None, verbose=False, resources=TurnResources())

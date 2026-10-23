"""Rasgos especiales de monstruos: Blood Frenzy del sahuagin.

Los rasgos se parsean de ``special_abilities`` (fixture real de la API) y se
aplican en la única fuente del modo de tirada:
:func:`dnd_sim.roll_modifiers.attack_modifiers`.
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, Monster, PlayerCharacter
from dnd_sim.attack import Attack
from dnd_sim.combat import attack_roll, run_combat
from dnd_sim.data.loader import load_monster
from dnd_sim.data.trait_parser import parse_traits
from dnd_sim.dice import RollMode
from dnd_sim.roll_modifiers import AttackRange, attack_modifiers
from dnd_sim.traits import BloodFrenzy, Trait

FIXTURES = Path(__file__).parent / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _datos(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _sahuagin(monkeypatch) -> Monster:
    data = _datos("sahuagin")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("sahuagin")


def _pj(name: str = "Guerrero", hp: int = 30) -> PlayerCharacter:
    return PlayerCharacter(
        name=name, max_hp=hp, ac=15, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[],
    )


def _ataque_melee() -> Attack:
    return Attack(name="Colmillo", damage="1d6", ability="str",
                  attack_bonus=3, damage_bonus=1)


def _sahuagin_con_rasgo(hp: int = 22) -> Monster:
    return Monster(name="Sahuagin", max_hp=hp, ac=12,
                   traits=[BloodFrenzy(name="Blood Frenzy")])


# --- Carga del rasgo -------------------------------------------------------- #

def test_el_sahuagin_carga_su_rasgo_blood_frenzy(monkeypatch):
    sahuagin = _sahuagin(monkeypatch)
    assert [type(t).__name__ for t in sahuagin.traits] == ["BloodFrenzy"]
    rasgo = sahuagin.traits[0]
    assert rasgo.name == "Blood Frenzy"
    assert "advantage" in rasgo.desc          # descripción de la API, de referencia
    # Los rasgos no combativos (Limited Amphibiousness, Shark Telepathy)
    # no se modelan.
    assert len(sahuagin.traits) == 1


def test_un_monstruo_sin_rasgos_modelables_no_tiene_traits(monkeypatch):
    data = _datos("ogre")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    assert load_monster("ogre").traits == []


def test_parse_traits_ignora_lo_gestionado_por_otro_parser():
    # El lich solo trae Spellcasting y Legendary Resistance: ya los gestionan
    # spell_parser y legendary_parser, aquí no deben aparecer.
    assert parse_traits(_datos("lich")) == []


def test_parse_traits_ignora_entradas_malformadas():
    assert parse_traits({}) == []
    assert parse_traits({"special_abilities": [None, 42, {"sin_nombre": 1}]}) == []


# --- Reglas de Blood Frenzy ------------------------------------------------- #

def test_blood_frenzy_da_ventaja_contra_un_objetivo_herido():
    sahuagin = _sahuagin_con_rasgo()
    herido = _pj()
    herido.hp = 17
    mods = attack_modifiers(sahuagin, herido, _ataque_melee(), AttackRange.MELEE)
    assert mods.mode is RollMode.ADVANTAGE
    assert mods.advantage_sources == ["Blood Frenzy"]
    assert "Blood Frenzy" in mods.reason()


def test_blood_frenzy_no_aplica_a_un_objetivo_a_toda_vida():
    sahuagin = _sahuagin_con_rasgo()
    a_toda_vida = _pj()                      # hp == max_hp
    mods = attack_modifiers(sahuagin, a_toda_vida, _ataque_melee(),
                            AttackRange.MELEE)
    assert mods.mode is RollMode.NORMAL
    assert mods.advantage_sources == []


def test_blood_frenzy_solo_es_en_ataques_cuerpo_a_cuerpo():
    """La SRD dice «melee attack rolls»: a distancia no aplica."""
    sahuagin = _sahuagin_con_rasgo()
    herido = _pj()
    herido.hp = 17
    mods = attack_modifiers(sahuagin, herido, _ataque_melee(), AttackRange.RANGED)
    assert mods.mode is RollMode.NORMAL
    assert mods.advantage_sources == []


def test_blood_frenzy_no_aplica_a_criaturas_sin_el_rasgo():
    herido = _pj()
    herido.hp = 17
    mods = attack_modifiers(_pj(name="Sin rasgo"), herido, _ataque_melee(),
                            AttackRange.MELEE)
    assert mods.mode is RollMode.NORMAL
    assert mods.advantage_sources == []


def test_blood_frenzy_se_anula_con_una_desventaja():
    """Ventaja y desventaja a la vez se anulan (regla 5e)."""
    sahuagin = _sahuagin_con_rasgo()
    sahuagin.attacks_with_disadvantage = True
    herido = _pj()
    herido.hp = 17
    mods = attack_modifiers(sahuagin, herido, _ataque_melee(), AttackRange.MELEE)
    assert mods.mode is RollMode.NORMAL
    assert mods.cancels is True
    assert mods.reason() == "ventaja y desventaja se anulan"


# --- Integración con el motor ----------------------------------------------- #

def test_blood_frenzy_aparece_en_el_log_del_ataque():
    sahuagin = _sahuagin_con_rasgo()
    objetivo = _pj(hp=30)
    objetivo.hp = 10
    log: list = []
    attack_roll(sahuagin, objetivo, _ataque_melee(), random.Random(7),
                log=log, verbose=True)
    assert log, "el ataque debe registrarse"
    # Impacte o falle, la tirada se resuelve con ventaja y el motivo va en el log.
    assert any("ventaja" in linea for linea in log)
    assert any("Blood Frenzy" in linea for linea in log)


def test_blood_frenzy_actua_durante_el_combate_completo(monkeypatch):
    sahuagin = _sahuagin(monkeypatch)
    objetivo = _pj(hp=100)
    res = run_combat([objetivo, sahuagin], random.Random(3), verbose=True,
                     max_rounds=8)
    # Tras la primera herida, los ataques del sahuagin van con ventaja.
    assert any("Blood Frenzy" in linea for linea in res.log), \
        "el sahuagin debe atacar con ventaja a un objetivo herido"
    assert objetivo.hp < 100, "el sahuagin debe llegar a herir al objetivo"

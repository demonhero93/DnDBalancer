"""Bono de competencia por nivel (proficiency bonus) de los PJ."""
import random

from dnd_sim import Abilities, Attack, Monster, PlayerCharacter
from dnd_sim.core.proficiency import MAX_LEVEL, MIN_LEVEL, proficiency_bonus
from dnd_sim.rules.checks import ability_check, ability_check_bonus


# --- Utilidades ------------------------------------------------------------- #

def _abilities(**kwargs) -> Abilities:
    base = dict(str=10, dex=10, con=10, int=10, wis=10, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    kwargs.setdefault("name", "Guerrero")
    kwargs.setdefault("max_hp", 50)
    kwargs.setdefault("ac", 11)
    kwargs.setdefault("abilities", _abilities())
    kwargs.setdefault("attacks", [])
    return PlayerCharacter(**kwargs)


# --- Tabla PHB -------------------------------------------------------------- #

def test_tabla_niveles():
    assert proficiency_bonus(1) == 2
    assert proficiency_bonus(4) == 2
    assert proficiency_bonus(5) == 3
    assert proficiency_bonus(8) == 3
    assert proficiency_bonus(9) == 4
    assert proficiency_bonus(12) == 4
    assert proficiency_bonus(13) == 5
    assert proficiency_bonus(16) == 5
    assert proficiency_bonus(17) == 6
    assert proficiency_bonus(20) == 6


def test_nivel_recortado_al_rango_1_20():
    assert MIN_LEVEL == 1
    assert MAX_LEVEL == 20
    assert proficiency_bonus(0) == 2
    assert proficiency_bonus(-5) == 2
    assert proficiency_bonus(99) == 6


# --- Campo level en PlayerCharacter ---------------------------------------- #

def test_level_recalcula_proficiency():
    pj = _pj(level=5)
    assert pj.proficiency == 3
    pj = _pj(level=17)
    assert pj.proficiency == 6


def test_level_manda_sobre_el_proficiency_explicito():
    pj = _pj(level=9, proficiency=2)
    assert pj.proficiency == 4


def test_sin_level_respeta_el_proficiency_explicito():
    assert _pj().proficiency == 2
    assert _pj(proficiency=3).proficiency == 3


def test_monstruo_no_tiene_level():
    monstruo = Monster(name="Goblin", max_hp=7, ac=15, abilities=_abilities())
    assert not hasattr(monstruo, "level")
    assert monstruo.proficiency == 2


# --- to_hit ----------------------------------------------------------------- #

def test_to_hit_suma_competencia_si_proficient():
    ataque = Attack("Espada larga", "1d8", ability="str")
    pj = _pj(level=5, abilities=_abilities(str=16))  # mod +3, PB +3
    assert pj.to_hit(ataque) == 6


def test_to_hit_sin_competencia():
    ataque = Attack("Daga arrojadiza", "1d4", ability="str", proficient=False)
    pj = _pj(level=5, abilities=_abilities(str=16))
    assert pj.to_hit(ataque) == 3


def test_to_hit_attack_bonus_fijo_manda():
    ataque = Attack("Rayo", "2d8", ability="int", attack_bonus=7)
    pj = _pj(level=17, abilities=_abilities(int=20))
    assert pj.to_hit(ataque) == 7


# --- Salvaciones ------------------------------------------------------------- #

def test_saving_throw_bonus_con_competencia():
    pj = _pj(level=5, abilities=_abilities(str=16),
             save_proficiencies={"str"})
    assert pj.saving_throw_bonus("str") == 6  # +3 mod, +3 PB


def test_saving_throw_bonus_sin_competencia():
    pj = _pj(level=5, abilities=_abilities(str=16),
             save_proficiencies={"dex"})
    assert pj.saving_throw_bonus("str") == 3


def test_saving_throw_override_fijo_manda():
    pj = _pj(level=5, abilities=_abilities(str=16),
             save_proficiencies={"str"}, save_overrides={"str": 9})
    assert pj.saving_throw_bonus("str") == 9


# --- Pruebas de característica ---------------------------------------------- #

def test_check_bonus_con_competencia():
    pj = _pj(level=5, abilities=_abilities(str=16),
             check_proficiencies={"str"})
    assert pj.check_bonus("str") == 6
    assert pj.check_bonus("dex") == 0  # sin competencia: solo el mod


def test_check_bonus_sin_competencia():
    pj = _pj(level=17, abilities=_abilities(str=16))
    assert pj.check_bonus("str") == 3


def test_ability_check_bonus_delega_en_check_bonus():
    pj = _pj(level=5, abilities=_abilities(str=16),
             check_proficiencies={"str"})
    assert ability_check_bonus(pj, "str") == 6
    assert ability_check_bonus(pj, "dex") == 0


def test_ability_check_bonus_sin_metodo_check_bonus():
    """Objetivos duck-typed sin ``check_bonus`` caen al mod puro."""

    class SoloMod:
        abilities = _abilities(str=16)

    assert ability_check_bonus(SoloMod(), "str") == 3


def test_ability_check_usa_el_bono_completo():
    pj = _pj(level=5, abilities=_abilities(str=16),
             check_proficiencies={"str"})
    rng = random.Random(0)
    resultado = ability_check(pj, "str", dc=10, rng=rng)
    assert resultado.bonus == 6
    assert resultado.total == resultado.rolls[0] + resultado.bonus

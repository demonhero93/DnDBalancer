"""Habilidades (Atletismo, Arcana...): registro, bonos y tiradas."""
import json
import random
from pathlib import Path

import pytest

from dnd_sim import (
    Abilities, Condition, EscapeCheck, PlayerCharacter, apply_condition,
    begin_turn, load_monster, normalize_skill, skill_ability, skill_check,
)
from dnd_sim.core.skills import SKILL_ABILITIES
from dnd_sim.data.escape_parser import parse_escape
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.rules.checks import ability_check_bonus, skill_bonus
from dnd_sim.rules.roll_modifiers import RollMode, check_modifiers

FIXTURES = Path(__file__).parents[2] / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _abilities(**kwargs) -> Abilities:
    base = dict(str=10, dex=10, con=10, int=10, wis=10, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    kwargs.setdefault("name", "Pícaro")
    kwargs.setdefault("max_hp", 50)
    kwargs.setdefault("ac", 11)
    kwargs.setdefault("abilities", _abilities())
    kwargs.setdefault("attacks", [])
    return PlayerCharacter(**kwargs)


def _ctx(actor=None, rng=None, log=None) -> CombatContext:
    return CombatContext(rng=rng or random.Random(1), actor=actor,
                         combatants=[actor] if actor else [], round=1,
                         log=log if log is not None else [],
                         verbose=True,
                         resources=TurnResources())


def _load_fixture(monkeypatch, index: str):
    data = json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: data)
    return load_monster(index)


# --- Registro de habilidades ------------------------------------------------ #

def test_las_18_habilidades_del_phb_estan_registradas():
    assert len(SKILL_ABILITIES) == 18


@pytest.mark.parametrize("skill,ability", [
    ("acrobatics", "dex"),
    ("animal-handling", "wis"),
    ("arcana", "int"),
    ("athletics", "str"),
    ("deception", "cha"),
    ("history", "int"),
    ("insight", "wis"),
    ("intimidation", "cha"),
    ("investigation", "int"),
    ("medicine", "wis"),
    ("nature", "int"),
    ("perception", "wis"),
    ("performance", "cha"),
    ("persuasion", "cha"),
    ("religion", "int"),
    ("sleight-of-hand", "dex"),
    ("stealth", "dex"),
    ("survival", "wis"),
])
def test_caracteristica_asociada(skill, ability):
    assert skill_ability(skill) == ability


def test_normalize_skill_acepta_espacios_y_spanish():
    assert normalize_skill("sleight of hand") == "sleight-of-hand"
    assert normalize_skill("Acrobacias") == "acrobatics"
    assert normalize_skill("Conocimiento arcano") == "arcana"
    assert normalize_skill("Atletismo") == "athletics"
    assert normalize_skill("Juego de Manos") == "sleight-of-hand"
    assert normalize_skill("Sigilo") == "stealth"


def test_normalize_skill_desconocida_lanza_value_error():
    with pytest.raises(ValueError):
        normalize_skill("volar")


# --- Bono de habilidad ------------------------------------------------------ #

def test_skill_bonus_sin_competencia_es_solo_el_mod():
    pj = _pj(level=5, abilities=_abilities(dex=16))
    assert pj.skill_bonus("acrobatics") == 3


def test_skill_bonus_con_competencia_suma_pb():
    pj = _pj(level=5, abilities=_abilities(str=16),
             skill_proficiencies={"athletics"})
    assert pj.skill_bonus("athletics") == 6  # +3 mod, +3 PB


def test_skill_bonus_con_expertise_duplica_pb():
    pj = _pj(level=5, abilities=_abilities(dex=16),
             skill_proficiencies={"stealth"},
             skill_expertise={"stealth"})
    assert pj.skill_bonus("stealth") == 9  # +3 mod, +6 PB


def test_skill_bonus_override_de_ficha_manda():
    pj = _pj(level=5, abilities=_abilities(int=20),
             skill_proficiencies={"arcana"}, skill_overrides={"arcana": 15})
    assert pj.skill_bonus("arcana") == 15


def test_las_competencias_de_habilidad_se_normalizan():
    pj = _pj(skill_proficiencies={"Acrobacias"}, skill_expertise={"Sigilo"})
    assert pj.skill_proficiencies == {"acrobatics"}
    assert pj.skill_expertise == {"stealth"}
    assert pj.skill_bonus("acrobatics") == 2  # mod dex 10 = 0, PB 2


def test_skill_bonus_delegado_por_rules_checks():
    pj = _pj(level=5, abilities=_abilities(str=16),
             skill_proficiencies={"athletics"})
    assert skill_bonus(pj, "athletics") == 6
    assert skill_bonus(pj, "Atletismo") == 6  # alias en la capa rules


class _SoloMod:
    """Objetivo duck-typed sin ``skill_bonus``."""

    abilities = _abilities(str=16)


def test_skill_bonus_sin_metodo_cae_al_mod_de_la_caracteristica():
    assert skill_bonus(_SoloMod(), "athletics") == 3


# --- Tiradas de habilidad --------------------------------------------------- #

def test_skill_check_usa_el_bono_completo():
    pj = _pj(level=5, abilities=_abilities(str=16),
             skill_proficiencies={"athletics"})
    rng = random.Random(0)
    resultado = skill_check(pj, "athletics", dc=10, rng=rng)
    assert resultado.bonus == 6
    assert resultado.skill == "athletics"
    assert resultado.ability == "str"
    assert resultado.total == resultado.rolls[0] + resultado.bonus


def test_skill_check_sin_competencia_usa_solo_el_mod():
    pj = _pj(level=5, abilities=_abilities(dex=16))
    rng = random.Random(0)
    resultado = skill_check(pj, "Acrobacias", dc=10, rng=rng)
    assert resultado.bonus == 3
    assert resultado.skill == "acrobatics"


def test_ability_check_no_suma_competencia_de_habilidad():
    """Una prueba de característica pura no hereda la de la habilidad."""
    pj = _pj(level=5, abilities=_abilities(str=16),
             skill_proficiencies={"athletics"})
    assert ability_check_bonus(pj, "str") == 3


def test_check_modifiers_pasa_la_habilidad_a_los_rasgos():
    class _Rasgo:
        def modify_check_modifiers(self, mods, target, ability, skill=None):
            if skill == "stealth":
                mods.advantage_sources.append("rasgo")

    pj = _pj()
    pj.traits = [_Rasgo()]
    assert check_modifiers(pj, "dex", skill="stealth").mode is RollMode.ADVANTAGE
    assert check_modifiers(pj, "dex").mode is RollMode.NORMAL


# --- Fichas de monstruos ---------------------------------------------------- #

def test_loader_parsea_las_habilidades_de_la_ficha(monkeypatch):
    gladiador = _load_fixture(monkeypatch, "gladiator")
    assert {"athletics", "intimidation"} <= gladiador.skill_proficiencies
    assert isinstance(gladiador.skill_overrides["athletics"], int)
    # El total de ficha manda sobre mod + competencia.
    assert (gladiador.skill_bonus("athletics")
            == gladiador.skill_overrides["athletics"])


def test_loader_lich_conoce_sus_habilidades(monkeypatch):
    lich = _load_fixture(monkeypatch, "lich")
    assert {"arcana", "history", "insight", "perception"} <= lich.skill_proficiencies
    assert lich.skill_bonus("arcana") == lich.skill_overrides["arcana"]


# --- Escapes con habilidades ------------------------------------------------ #

def test_escape_de_telaraña_usa_atletismo():
    desc = ("The target is restrained by webbing. As an action, the restrained "
            "target can make a DC 12 Strength check, bursting the webbing.")
    escape = parse_escape(desc, "Giant Spider", "Web")
    assert escape.skills == ("athletics",)
    assert escape.abilities == ("str",)


def test_escape_sin_caracteristica_usa_atletismo_y_acrobacias():
    escape = parse_escape("the target is grappled (escape DC 16).", "Snake",
                          "Constrict")
    assert escape.skills == ("athletics", "acrobatics")


def test_attempt_escapes_tira_la_habilidad():
    objetivo = _pj()
    escape = EscapeCheck(skills=("athletics",), dc=12, consumes_action=False)
    apply_condition(objetivo, Condition.RESTRAINED, _ctx(objetivo),
                    escape=escape)
    ctx = _ctx(objetivo, rng=random.Random(2))
    begin_turn(objetivo, ctx)
    assert any("prueba ATHLETICS" in line for line in ctx.log), ctx.log


def test_escape_con_competencia_en_atletismo_sube_el_bono():
    pj = _pj(level=5, abilities=_abilities(str=16),
             skill_proficiencies={"athletics"})
    rng = random.Random(7)
    assert skill_check(pj, "athletics", dc=12, rng=rng).bonus == 6


# --- Plantillas de main.py: salvaciones y habilidades por clase ------------- #

def test_las_salvaciones_de_los_pj_salen_de_la_clase():
    import main
    guerrero = main._build_party(1)[0]
    assert guerrero.save_proficiencies == {"str", "con"}
    # Nivel 5: PB +3. FUE 16: mod +3 -> salvación +6.
    assert guerrero.saving_throw_bonus("str") == 6
    # DES no es salvación de clase: solo el mod (dex 12 -> +1).
    assert guerrero.saving_throw_bonus("dex") == 1


def test_las_habilidades_de_los_pj_salen_de_la_clase():
    import main
    party = {p.name: p for p in main._build_party(5)}
    assert "athletics" in party["Guerrero"].skill_proficiencies
    assert "stealth" in party["Pícaro"].skill_proficiencies
    assert party["Pícaro"].skill_expertise == {"stealth", "sleight-of-hand"}
    # Expertise del Pícaro: dex 16 (mod +3) + 2xPB 3 -> +9.
    assert party["Pícaro"].skill_bonus("stealth") == 9
    assert party["Clérigo"].save_proficiencies == {"wis", "cha"}

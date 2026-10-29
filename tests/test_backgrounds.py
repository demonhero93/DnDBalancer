"""Transfondos: competencias parseadas y aplicadas al personaje."""
import pytest

from dnd_sim import (
    Abilities, Background, PlayerCharacter, load_background, parse_background,
)


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


# --- Parseo de la ficha ----------------------------------------------------- #

def test_parse_forma_2024_skills_e_idiomas():
    data = {
        "index": "acolyte",
        "name": "Acolyte",
        "proficiencies": [
            {"index": "skill-insight"},
            {"index": "skill-religion"},
            {"index": "language-celestial"},
        ],
    }
    bg = parse_background(data)
    assert bg.index == "acolyte"
    assert bg.name == "Acolyte"
    assert bg.skill_proficiencies == {"insight", "religion"}
    assert bg.languages == {"celestial"}
    assert bg.tool_proficiencies == set()


def test_parse_forma_anidada_como_las_fichas_de_monstruos():
    data = {
        "index": "test",
        "proficiencies": [
            {"value": 5, "proficiency": {"index": "skill-athletics"}},
            {"value": 3, "proficiency": {"index": "tool-thieves-tools"}},
        ],
    }
    bg = parse_background(data)
    assert bg.skill_proficiencies == {"athletics"}
    assert bg.tool_proficiencies == {"thieves-tools"}


def test_parse_forma_2014_nombres_libres():
    data = {
        "index": "criminal",
        "name": "Criminal",
        "starting_proficiencies": [
            "Stealth", "Deception", "Thieves' Tools",
            "Choose any two skills", "Common",
        ],
    }
    bg = parse_background(data)
    assert bg.skill_proficiencies == {"stealth", "deception"}
    assert bg.tool_proficiencies == {"thieves-tools"}


def test_parse_textos_de_eleccion_se_ignoran():
    data = {
        "index": "test",
        "proficiencies": ["Choose any two skills"],
        "starting_proficiencies": ["Choose a gaming set and one language"],
    }
    bg = parse_background(data)
    assert bg.skill_proficiencies == set()
    assert bg.tool_proficiencies == set()
    assert bg.languages == set()


def test_parse_sin_proficiencies_devuelve_vacío():
    bg = parse_background({})
    assert bg.index == ""
    assert bg.name == ""
    assert bg.skill_proficiencies == set()


# --- Descarga perezosa ------------------------------------------------------ #

def test_load_background_descarga_solo_el_pedido(monkeypatch):
    llamadas = []

    def _fake(index, **kwargs):
        llamadas.append(index)
        return {"index": index, "name": "Acolyte",
                "proficiencies": [{"index": "skill-insight"}]}

    monkeypatch.setattr("dnd_sim.data.background_parser.get_background", _fake)
    bg = load_background("acolyte")
    assert llamadas == ["acolyte"]
    assert bg.skill_proficiencies == {"insight"}


def test_load_background_propaga_el_error_de_la_api(monkeypatch):
    def _fake(index, **kwargs):
        raise ValueError(f"El transfondo {index!r} no existe en la API.")

    monkeypatch.setattr("dnd_sim.data.background_parser.get_background", _fake)
    with pytest.raises(ValueError):
        load_background("no-existe")


# --- Aplicación al personaje ------------------------------------------------ #

def test_apply_background_añade_las_competencias():
    pj = _pj(level=5, abilities=_abilities(str=16))
    assert pj.skill_bonus("athletics") == 3  # solo el mod

    bg = Background(index="outlander", name="Outlander",
                    skill_proficiencies={"Atletismo"},
                    tool_proficiencies={"Thieves' Tools"})
    pj.apply_background(bg)

    assert pj.skill_proficiencies == {"athletics"}
    assert pj.tool_proficiencies == {"thieves-tools"}
    assert pj.background is bg
    assert pj.skill_bonus("athletics") == 6  # mod +3, PB +3


def test_apply_background_no_duplica_competencias_existentes():
    pj = _pj(skill_proficiencies={"athletics"})
    pj.apply_background(Background(skill_proficiencies={"athletics"}))
    assert pj.skill_proficiencies == {"athletics"}
    assert pj.tool_proficiencies == set()


def test_apply_background_sin_competencias_es_inofensivo():
    pj = _pj()
    pj.apply_background(Background(index="vacío"))
    assert pj.background is not None
    assert pj.skill_proficiencies == set()


def test_el_transfondo_no_toca_las_salvaciones():
    """5e: las salvaciones salen de la clase, nunca del transfondo."""
    pj = _pj(level=5, abilities=_abilities(str=16))
    pj.apply_background(Background(skill_proficiencies={"athletics"},
                                   tool_proficiencies={"thieves-tools"}))
    assert pj.save_proficiencies == set()
    assert pj.saving_throw_bonus("str") == 3  # solo el mod

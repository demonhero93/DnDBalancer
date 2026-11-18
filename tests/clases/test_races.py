"""Razas: competencias y hechizos parseados y aplicados al personaje."""
import pytest

from dnd_sim import Abilities, PlayerCharacter, Race, load_race, parse_race


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


def _keen_senses() -> dict:
    """Rasgo real de la API: elfo, habilidad a elegir."""
    return {
        "index": "keen-senses",
        "name": "Keen Senses",
        "description": "You have proficiency in the Insight, Perception, or Survival skill.",
        "proficiency_choices": {
            "desc": "Choose one of the following skills: Insight, Perception, or Survival.",
            "choose": 1,
            "type": "proficiencies",
            "from": {
                "option_set_type": "options_array",
                "options": [
                    {"option_type": "reference",
                     "item": {"index": "insight", "name": "Insight"}},
                    {"option_type": "reference",
                     "item": {"index": "perception", "name": "Perception"}},
                    {"option_type": "reference",
                     "item": {"index": "survival", "name": "Survival"}},
                ],
            },
        },
    }


def _fiendish_legacy() -> dict:
    """Rasgo real de la API: tiefling, hechizos solo en la descripción."""
    return {
        "index": "fiendish-legacy",
        "name": "Fiendish Legacy",
        "description": (
            "You are the recipient of a legacy that grants you supernatural "
            "abilities. Choose a legacy from the Fiendish Legacies table. "
            "You gain the level 1 benefit of the chosen legacy.\n"
            "When you reach character levels 3 and 5, you learn a "
            "higher-level spell, as shown on the table.\n"
            "Fiendish Legacies\n"
            "Abyssal.\n"
            "Level 1. You have Resistance to Poison damage. You also know "
            "the Poison Spray cantrip.\n"
            "Level 3. Ray of Sickness\n"
            "Level 5. Hold Person\n"
            "Chthonic.\n"
            "Level 1. You have Resistance to Necrotic damage. You also know "
            "the Chill Touch cantrip.\n"
            "Level 3. False Life\n"
            "Level 5. Ray of Enfeeblement\n"
            "Infernal.\n"
            "Level 1. You have Resistance to Fire damage. You also know the "
            "Fire Bolt cantrip.\n"
            "Level 3. Hellish Rebuke\n"
            "Level 5. Darkness"
        ),
    }


# --- Parseo de la raza ------------------------------------------------------ #

def test_parse_competencias_fijas_de_la_raza():
    data = {
        "index": "test", "name": "Test",
        "starting_proficiencies": ["Perception", "stealth"],
        "proficiencies": [{"index": "skill-athletics"}],
    }
    race = parse_race(data)
    assert race.skill_proficiencies == ("perception", "stealth", "athletics")
    assert race.skill_choices == ()
    assert race.spells == ()


def test_parse_habilidades_a_elegir_de_los_rasgos():
    race = parse_race({"index": "elf", "name": "Elf"}, [_keen_senses()])
    assert race.skill_proficiencies == ()
    assert race.skill_choices == ("insight", "perception", "survival")


def test_parse_hechizos_de_la_descripcion_del_rasgo():
    race = parse_race({"index": "tiefling"}, [_fiendish_legacy()])
    assert race.spells == (
        "Poison Spray", "Chill Touch", "Fire Bolt",
        "Ray of Sickness", "Hold Person",
        "False Life", "Ray of Enfeeblement",
        "Hellish Rebuke", "Darkness",
    )


def test_parse_elfo_linaje_hechizos_sin_duplicados():
    lineage = {
        "index": "elven-lineage",
        "name": "Elven Lineage",
        "description": (
            "Elven Lineages\n"
            "Drow\n"
            "Level 1. The range of your Darkvision increases to 120 feet. "
            "You also know the Dancing Lights cantrip.\n"
            "Level 3. Faerie Fire\n"
            "Level 5. Darkness\n"
            "High Elf\n"
            "Level 1. You know the Prestidigitation cantrip. Whenever you "
            "finish a Long Rest, you can replace that cantrip.\n"
            "Level 3. Detect Magic\n"
            "Level 5. Misty Step\n"
            "Wood Elf\n"
            "Level 1. Your Speed increases to 35 feet. You also know the "
            "Druidcraft cantrip.\n"
            "Level 3. Longstrider\n"
            "Level 5. Pass without Trace"
        ),
    }
    race = parse_race({"index": "elf", "name": "Elf"},
                      [_keen_senses(), lineage])
    assert race.spells == (
        "Dancing Lights", "Prestidigitation", "Druidcraft",
        "Faerie Fire", "Darkness", "Detect Magic", "Misty Step",
        "Longstrider", "Pass without Trace",
    )
    assert race.skill_choices == ("insight", "perception", "survival")


def test_parse_descripcion_sin_hechizos_da_vacio():
    trait = {"index": "trance", "name": "Trance",
             "description": "You don't need to sleep."}
    race = parse_race({}, [trait])
    assert race.spells == ()
    assert race.skill_proficiencies == ()


# --- Descarga perezosa ------------------------------------------------------ #

def test_load_race_descarga_la_raza_y_sus_rasgos(monkeypatch):
    llamadas_rasgos = []

    def _raza(index, **kwargs):
        return {"index": index, "name": "Elf",
                "traits": [{"index": "keen-senses"}, {"index": "trance"}]}

    def _rasgo(index, **kwargs):
        llamadas_rasgos.append(index)
        if index == "keen-senses":
            return _keen_senses()
        return {"index": index, "name": "Trance",
                "description": "You don't need to sleep."}

    monkeypatch.setattr("dnd_sim.data.race_parser.get_race", _raza)
    monkeypatch.setattr("dnd_sim.data.race_parser.get_trait", _rasgo)

    race = load_race("elf")
    assert llamadas_rasgos == ["keen-senses", "trance"]
    assert race.index == "elf"
    assert race.skill_choices == ("insight", "perception", "survival")


def test_load_race_propaga_el_error_de_la_api(monkeypatch):
    def _raza(index, **kwargs):
        raise ValueError(f"El rasgo {index!r} no existe en la API.")

    monkeypatch.setattr("dnd_sim.data.race_parser.get_race", _raza)
    with pytest.raises(ValueError):
        load_race("no-existe")


# --- Aplicación al personaje ------------------------------------------------ #

def test_apply_race_añade_competencias_fijas():
    pj = _pj(level=5, abilities=_abilities())
    race = Race(index="orc", name="Orc",
                skill_proficiencies=("intimidation",))
    pj.apply_race(race)
    assert pj.skill_proficiencies == {"intimidation"}
    assert pj.race is race
    assert pj.skill_bonus("intimidation") == 3  # mod 0 + PB 3
    # La raza no toca salvaciones ni características.
    assert pj.save_proficiencies == set()
    assert pj.abilities.mod("str") == 0


def test_apply_race_toma_la_primera_opcion_por_defecto():
    pj = _pj()
    race = Race(index="elf", name="Elf",
                skill_choices=("insight", "perception", "survival"))
    pj.apply_race(race)
    assert pj.skill_proficiencies == {"insight"}


def test_apply_race_con_habilidad_pedida():
    pj = _pj()
    race = Race(index="elf", name="Elf",
                skill_choices=("insight", "perception", "survival"))
    pj.apply_race(race, skill="Perception")
    assert pj.skill_proficiencies == {"perception"}


def test_apply_race_habilidad_fuera_de_las_opciones_es_error():
    pj = _pj()
    race = Race(index="elf", name="Elf",
                skill_choices=("insight", "perception", "survival"))
    with pytest.raises(ValueError):
        pj.apply_race(race, skill="athletics")


def test_apply_race_sin_opciones_y_con_habilidad_fija_no_falla():
    pj = _pj()
    race = Race(index="orc", name="Orc",
                skill_proficiencies=("intimidation",))
    pj.apply_race(race, skill="intimidation")
    assert pj.skill_proficiencies == {"intimidation"}


def test_apply_race_no_duplica_competencias_existentes():
    pj = _pj(skill_proficiencies={"perception"})
    race = Race(index="elf", name="Elf",
                skill_proficiencies=("perception",),
                skill_choices=("perception", "survival"))
    pj.apply_race(race)
    assert pj.skill_proficiencies == {"perception"}


def test_apply_race_registra_los_hechizos_aprendidos():
    pj = _pj()
    race = Race(index="tiefling", name="Tiefling",
                spells=("Fire Bolt", "Hellish Rebuke"))
    pj.apply_race(race)
    assert pj.race is not None
    assert pj.race.spells == ("Fire Bolt", "Hellish Rebuke")

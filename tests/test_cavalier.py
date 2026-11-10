"""Tests de tablas, constantes y CLI de la subclase Cavalier (XGE).

Los tests de comportamiento del rasgo van en las secciones A2-A8 de la
misma sesión; aquí solo lo que vive en ``core/classes.py`` y en el
cableado de ``main.py``.
"""

from __future__ import annotations

import importlib.util
import pathlib

from dnd_sim.core.classes import (
    CAVALIER_BONUS_SKILLS,
    CHARGE_MOVE_PROBABILITY,
    cavalier_mark_extra_damage,
    cavalier_mark_uses,
    warding_maneuver_uses,
)
from dnd_sim.core.skills import SKILL_ABILITIES


def test_tablas_de_usos_de_cavalier():
    # Unwavering Mark: max(1, mod FUE); Warding Maneuver: max(1, mod CON).
    assert cavalier_mark_uses(5) == 5
    assert cavalier_mark_uses(0) == 1
    assert cavalier_mark_uses(-2) == 1
    assert warding_maneuver_uses(4) == 4
    assert warding_maneuver_uses(0) == 1
    assert warding_maneuver_uses(-1) == 1


def test_daño_extra_del_ataque_especial_es_el_nivel_entre_dos():
    assert cavalier_mark_extra_damage(3) == 1
    assert cavalier_mark_extra_damage(5) == 2
    assert cavalier_mark_extra_damage(15) == 7
    assert cavalier_mark_extra_damage(1) == 0


def test_pool_de_bonus_proficiency_son_habilidades_del_proyecto():
    assert len(set(CAVALIER_BONUS_SKILLS)) == len(CAVALIER_BONUS_SKILLS)
    assert set(CAVALIER_BONUS_SKILLS) <= set(SKILL_ABILITIES)
    assert CAVALIER_BONUS_SKILLS == (
        "animal-handling",
        "history",
        "insight",
        "performance",
        "persuasion",
    )


def test_constante_charge_move_probability_es_cero_punto_cinco():
    assert CHARGE_MOVE_PROBABILITY == 0.5


def test_flag_charge_p_en_el_cli():
    raiz = pathlib.Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "main_cli_cavalier", raiz / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    parser = module.build_parser()
    assert parser.parse_args(["--charge-p", "1"]).charge_p == 1.0
    # Sin flag: None (la constante manda hasta que el rasgo se fija).
    assert parser.parse_args([]).charge_p is None

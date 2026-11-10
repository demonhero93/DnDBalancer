"""Tests de tablas, constantes, CLI y registro de Cavalier (XGE).

Las tablas y la CLI viven en A1; el registro, ``apply_cavalier`` y
Bonus Proficiency en A2. El comportamiento de los rasgos entra en los
pasos A3-A8 de la misma sesión.
"""

from __future__ import annotations

import importlib.util
import pathlib
import random
from types import SimpleNamespace

import pytest

from dnd_sim import Abilities, Attack, Monster, PlayerCharacter, apply_class
from dnd_sim.core.classes import (
    CAVALIER_BONUS_SKILLS,
    CHARGE_MOVE_PROBABILITY,
    cavalier_mark_extra_damage,
    cavalier_mark_uses,
    warding_maneuver_uses,
)
from dnd_sim.core.enums import AttackRange
from dnd_sim.core.skills import SKILL_ABILITIES
from dnd_sim.rules.classes import apply_fighter
from dnd_sim.rules.classes.fighter import CavalierFeatures, apply_cavalier


class _RngExplota:
    """Cualquier acceso al RNG revienta el test (guards sin RNG)."""

    def __getattr__(self, nombre: str):
        raise AssertionError(f"RNG tocado: {nombre}")


def _cargar_main():
    raiz = pathlib.Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "main_cli_cavalier", raiz / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=10, wis=12, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Camila", max_hp=70, ac=15, level=5, abilities=_abilities(),
        attacks=[Attack("Espada larga", "1d8", ability="str")],
    )
    defaults.update(kwargs)
    return PlayerCharacter(**defaults)


def _firmas(pj) -> tuple:
    """(rasgos, acciones, salvaciones, habilidades, CA) para comparar."""
    return (
        [type(t).__name__ for t in pj.traits],
        [type(a).__name__ for a in pj.actions],
        set(pj.save_proficiencies),
        set(pj.skill_proficiencies),
        pj.ac,
    )


def _trait(pj) -> CavalierFeatures:
    for trait in pj.traits:
        if isinstance(trait, CavalierFeatures):
            return trait
    raise AssertionError("falta CavalierFeatures")


def _cavalier(level: int = 5, **kwargs) -> tuple:
    pj = _pj(level=level)
    apply_fighter(pj, level=level)
    trait = apply_cavalier(pj, level=level, **kwargs)
    return pj, trait


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
    module = _cargar_main()
    parser = module.build_parser()
    assert parser.parse_args(["--charge-p", "1"]).charge_p == 1.0
    # Sin flag: None (la constante manda hasta que el rasgo se fija).
    assert parser.parse_args([]).charge_p is None


# --- A2: esqueleto, registro y Bonus Proficiency -------------------------------


def test_apply_class_equivalente_a_apply_cavalier(monkeypatch):
    """Misma semilla en los dos RNG de creación: resultados idénticos."""
    import dnd_sim.rules.classes.fighter.features as fighter_mod
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod

    a = _pj()
    b = _pj()
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    monkeypatch.setattr(cav_mod, "_RNG_CREACION", random.Random(0))
    apply_class(a, "fighter", "cavalier", level=5)
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    monkeypatch.setattr(cav_mod, "_RNG_CREACION", random.Random(0))
    apply_fighter(b, level=5)
    apply_cavalier(b, level=5)
    assert _firmas(a) == _firmas(b)
    assert _trait(a).competencia == _trait(b).competencia
    assert _trait(a).marca_usos.uses_max == _trait(b).marca_usos.uses_max


def test_apply_cavalier_exige_la_clase_fighter():
    with pytest.raises(ValueError, match="Primero aplica la clase guerrero"):
        apply_cavalier(_pj())


def test_apply_cavalier_requiere_nivel_3():
    pj = _pj(level=2)
    apply_fighter(pj, level=2)
    with pytest.raises(ValueError, match=">= 3"):
        apply_cavalier(pj, level=2)


def test_registro_de_subclase_cavalier_requiere_nivel_3():
    with pytest.raises(ValueError, match=">= 3"):
        apply_class(_pj(level=2), "fighter", "cavalier")


def test_bonus_proficiency_anade_una_habilidad_no_conocida():
    pj = _pj(skill_proficiencies={"history"})
    apply_fighter(pj, level=5)
    trait = apply_cavalier(pj, level=5)
    assert trait.competencia in CAVALIER_BONUS_SKILLS
    assert trait.competencia != "history"
    assert set(pj.skill_proficiencies) == {"history", trait.competencia}


def test_bonus_proficiency_sin_candidatas_no_cambia_nada():
    pj = _pj(skill_proficiencies=set(CAVALIER_BONUS_SKILLS))
    apply_fighter(pj, level=5)
    conocidas = set(pj.skill_proficiencies)
    trait = apply_cavalier(pj, level=5, rng=_RngExplota())
    assert trait.competencia == ""
    assert set(pj.skill_proficiencies) == conocidas


def test_usos_de_marca_y_warding_segun_las_tablas():
    pj5, trait5 = _cavalier(level=5)
    # FUE 16 → mod 3 → máx(1, 3); Warding es de nivel 7.
    assert trait5.marca_usos.uses_max == cavalier_mark_uses(3) == 3
    assert trait5.warding_usos is None
    pj7, trait7 = _cavalier(level=7)
    # CON 16 → mod 3 → máx(1, 3).
    assert trait7.warding_usos.uses_max == warding_maneuver_uses(3) == 3


def test_born_to_the_saddle_es_dato_sin_efecto():
    pj = _pj()
    apply_fighter(pj, level=5)
    ac_antes, salv_antes = pj.ac, set(pj.save_proficiencies)
    trait = apply_cavalier(pj, level=5)
    assert trait.born_to_the_saddle is True
    # Sin monturas ni caídas en el modelo: ni CA ni salvaciones cambian.
    assert pj.ac == ac_antes
    assert set(pj.save_proficiencies) == salv_antes


def test_sin_subclase_no_hay_rasgo_ni_charge_probability():
    pj = _pj()
    apply_fighter(pj, level=5)
    assert not any(isinstance(t, CavalierFeatures) for t in pj.traits)
    # Cero consulta: sin el rasgo nadie tiene el atributo que lee --charge-p.
    assert not any(hasattr(t, "charge_probability") for t in pj.traits)


def test_el_flag_charge_p_llega_al_rasgo(monkeypatch):
    module = _cargar_main()
    plantillas = [dict(t) for t in module.PARTY_TEMPLATES]
    plantillas[0] = dict(plantillas[0], subclass_name="cavalier")
    monkeypatch.setattr(module, "PARTY_TEMPLATES", plantillas)
    party = module._build_party(1, charge_p=0.25)
    trait = next(t for t in party[0].traits
                 if isinstance(t, CavalierFeatures))
    assert trait.charge_probability == 0.25
    # Sin flag: la constante de core/classes.py.
    party2 = module._build_party(1)
    trait2 = next(t for t in party2[0].traits
                  if isinstance(t, CavalierFeatures))
    assert trait2.charge_probability == CHARGE_MOVE_PROBABILITY


# --- A3: Unwavering Mark (marca y desventaja) ---------------------------------


class _RngSi:
    """``randrange`` devuelve el último índice: ``pick`` elige «si»."""

    def randrange(self, n: int) -> int:
        return n - 1


def _marcado(**kwargs) -> tuple:
    """PJ Cavalier + objetivo, para probar Unwavering Mark."""
    pj, trait = _cavalier(**kwargs)
    objetivo = Monster("Muñeco", max_hp=60, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(round=1, combatants=[pj, objetivo])
    return pj, trait, objetivo, ctx


def _mods() -> SimpleNamespace:
    return SimpleNamespace(advantage_sources=[], disadvantage_sources=[])


def _marca_con(trait, target, ctx, rng, *, hit=True,
               rango=AttackRange.MELEE) -> None:
    atk = Attack("Espada larga", "1d8", ability="str", range_type=rango)
    trait.after_attack_roll(trait.owner, target, atk, hit, ctx=ctx, rng=rng)


def test_marca_al_impactar_con_ataque_cuerpo_a_cuerpo(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    monkeypatch.setattr(cav_mod, "pick", lambda rng, seq: seq[-1])
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=15, rolls=[15],
                                    mode=RollMode.NORMAL))
    pj, trait, objetivo, ctx = _marcado()
    atk = Attack("Espada larga", "1d8", ability="str")
    atk_mod.attack_roll(pj, objetivo, atk, random.Random(1), ctx=ctx)
    assert list(objetivo.state.marca_cavalier) == [pj.name]
    caduca, ref = objetivo.state.marca_cavalier[pj.name]
    assert caduca == 3  # ronda 1 + 2
    assert ref is pj
    # Se gasta un uso al marcar.
    assert trait.marca_usos.uses_left == trait.marca_usos.uses_max - 1


def test_no_marca_con_ataque_a_distancia():
    pj, trait, objetivo, ctx = _marcado()
    _marca_con(trait, objetivo, ctx, _RngExplota(),
               rango=AttackRange.RANGED)
    assert objetivo.state.marca_cavalier == {}
    assert trait.marca_usos.uses_left == trait.marca_usos.uses_max


def test_no_marca_si_el_ataque_falla():
    pj, trait, objetivo, ctx = _marcado()
    _marca_con(trait, objetivo, ctx, _RngExplota(), hit=False)
    assert objetivo.state.marca_cavalier == {}
    assert trait.marca_usos.uses_left == trait.marca_usos.uses_max


def test_la_marca_no_se_consume_y_no_aplica_al_atacar_al_marcador():
    from dnd_sim.rules.mastery import consumir_marcas

    pj, trait, objetivo, ctx = _marcado()
    _marca_con(trait, objetivo, ctx, _RngSi())
    assert list(objetivo.state.marca_cavalier) == [pj.name]
    tercero = Monster("Tercero", max_hp=40, ac=12, abilities=_abilities())
    mods = _mods()
    consumir_marcas(mods, objetivo, tercero, ctx)
    assert "Unwavering Mark" in mods.disadvantage_sources
    # NO se consume: sigue marcado tras la tirada.
    assert list(objetivo.state.marca_cavalier) == [pj.name]
    # Contra su propio marcador: sin desventaja y la marca sigue.
    mods2 = _mods()
    consumir_marcas(mods2, objetivo, pj, ctx)
    assert "Unwavering Mark" not in mods2.disadvantage_sources
    assert list(objetivo.state.marca_cavalier) == [pj.name]


def test_la_marca_caduca_en_la_ronda_indicada():
    from dnd_sim.rules.mastery import consumir_marcas

    pj, _, objetivo, _ = _marcado()
    objetivo.state.marca_cavalier[pj.name] = (3, pj)
    ctx = SimpleNamespace(round=3, combatants=[pj, objetivo])
    tercero = Monster("Tercero", max_hp=40, ac=12, abilities=_abilities())
    mods = _mods()
    consumir_marcas(mods, objetivo, tercero, ctx)
    assert mods.disadvantage_sources == []
    assert objetivo.state.marca_cavalier == {}


def test_muerto_el_marcador_anula_la_marca():
    from dnd_sim.rules.mastery import consumir_marcas

    pj, _, objetivo, ctx = _marcado()
    objetivo.state.marca_cavalier[pj.name] = (5, pj)
    pj.dead = True  # fin anticipado: el marcador murió
    tercero = Monster("Tercero", max_hp=40, ac=12, abilities=_abilities())
    mods = _mods()
    consumir_marcas(mods, objetivo, tercero, ctx)
    assert mods.disadvantage_sources == []
    assert objetivo.state.marca_cavalier == {}


def test_incapacitado_el_marcador_anula_la_marca():
    from dnd_sim.rules.conditions import Condition, apply_condition
    from dnd_sim.rules.mastery import consumir_marcas

    pj, _, objetivo, ctx = _marcado()
    objetivo.state.marca_cavalier[pj.name] = (5, pj)
    apply_condition(pj, Condition.INCAPACITATED, ctx)
    tercero = Monster("Tercero", max_hp=40, ac=12, abilities=_abilities())
    mods = _mods()
    consumir_marcas(mods, objetivo, tercero, ctx)
    assert mods.disadvantage_sources == []
    assert objetivo.state.marca_cavalier == {}


def test_remarcar_sustituye_a_la_anterior():
    pj, trait, objetivo, ctx = _marcado()
    intruso = Monster("Intruso", max_hp=40, ac=12, abilities=_abilities())
    objetivo.state.marca_cavalier[intruso.name] = (9, intruso)
    _marca_con(trait, objetivo, ctx, _RngSi())
    # La marca nueva sustituye a la anterior (un solo marcador).
    assert list(objetivo.state.marca_cavalier) == [pj.name]
    assert objetivo.state.marca_cavalier[pj.name][0] == 3


def test_sin_usos_no_hay_rng():
    pj, trait, objetivo, ctx = _marcado()
    for _ in range(trait.marca_usos.uses_max):
        trait.marca_usos.spend()
    _marca_con(trait, objetivo, ctx, _RngExplota())
    assert objetivo.state.marca_cavalier == {}
    assert trait.marca_usos.uses_left == 0


def test_las_marcas_de_goading_y_cavalier_no_se_pisan():
    from dnd_sim.rules.mastery import consumir_marcas

    pj, trait, objetivo, ctx = _marcado()
    # Goading de Battle Master sobre el MISMO sujeto, otro marcador.
    objetivo.state.goading["Maestro de Batalla"] = 3
    _marca_con(trait, objetivo, ctx, _RngSi())
    assert "Maestro de Batalla" in objetivo.state.goading
    assert list(objetivo.state.marca_cavalier) == [pj.name]
    tercero = Monster("Tercero", max_hp=40, ac=12, abilities=_abilities())
    mods = _mods()
    consumir_marcas(mods, objetivo, tercero, ctx)
    # Cada marca vive en su propio campo y ambas siguen vigentes.
    assert "Goading Attack" in mods.disadvantage_sources
    assert "Unwavering Mark" in mods.disadvantage_sources
    assert "Maestro de Batalla" in objetivo.state.goading
    assert list(objetivo.state.marca_cavalier) == [pj.name]


def test_reset_de_combate_limpia_la_marca_de_cavalier():
    pj, trait, objetivo, ctx = _marcado()
    _marca_con(trait, objetivo, ctx, _RngSi())
    assert objetivo.state.marca_cavalier
    objetivo.reset()
    assert objetivo.state.marca_cavalier == {}

"""Tests de tablas, constantes, CLI y registro de Cavalier (XGE).

Las tablas y la CLI viven en A1; el registro, ``apply_cavalier`` y
Bonus Proficiency en A2; Unwavering Mark (marca, desventaja y ataque
especial) en A3-A4. El resto de rasgos entra en los pasos A5-A8 de la
misma sesión.
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


def _cavalier(level: int = 5, fighting_style: str | None = None,
              **kwargs) -> tuple:
    pj = _pj(level=level)
    apply_fighter(pj, level=level, fighting_style=fighting_style)
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


# --- A4: Unwavering Mark (ataque especial) ------------------------------------


def _accion_marca(pj):
    from dnd_sim.rules.classes.fighter.subclasses.cavalier import (
        CavalierMarkAttackAction,
    )

    for accion in pj.actions:
        if isinstance(accion, CavalierMarkAttackAction):
            return accion
    raise AssertionError("falta CavalierMarkAttackAction")


def _especial(**kwargs) -> tuple:
    """PJ Cavalier + marcado + víctima, con el ataque especial armado."""
    from dnd_sim.rules.damage import inflict_damage

    pj, trait = _cavalier(**kwargs)
    marcado = Monster("Marcado", max_hp=60, ac=15, abilities=_abilities())
    victima = Monster("Víctima", max_hp=60, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(round=1, actor=pj, rng=random.Random(1),
                           combatants=[pj, marcado, victima], log=None)
    # Marca puesta directamente (el camino de marca ya está en A3).
    marcado.state.marca_cavalier[pj.name] = (int(ctx.round) + 2, pj)
    inflict_damage(victima, 5, source=marcado, ctx=ctx)
    return pj, trait, marcado, victima, ctx


def _pick_sin_decision(rng, seq):
    """«no»/«si» → «no» (decisiones); pools (armas) → último elemento."""
    return "no" if tuple(seq) == ("no", "si") else seq[-1]


def _parchea_ataque(monkeypatch, valor_d20=15, dados=1, modos=None):
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: (modos.append(mode) if modos is not None else None,
                           D20Result(value=valor_d20,
                                     rolls=[valor_d20, valor_d20],
                                     mode=mode))[1])
    monkeypatch.setattr(atk_mod, "roll_dice",
                        lambda expr, rng, crit=False: dados)


def test_el_ataque_especial_se_arma_cuando_el_marcado_dana_a_un_tercero():
    pj, trait, marcado, victima, ctx = _especial()
    assert trait.ataque_marca_pendiente == trait.turno_cavalier + 1
    assert trait.ataque_marca_objetivo is marcado
    # Y el daño a la víctima se aplicó con normalidad.
    assert victima.hp == 55


def test_no_se_arma_si_el_marcado_dana_al_cavalier():
    from dnd_sim.rules.damage import inflict_damage

    pj, trait, objetivo, ctx = _marcado()
    _marca_con(trait, objetivo, ctx, _RngSi())
    inflict_damage(pj, 5, source=objetivo, ctx=ctx)
    assert trait.ataque_marca_pendiente == 0
    assert trait.ataque_marca_objetivo is None


def test_no_se_arma_si_la_marca_ya_caduco():
    from dnd_sim.rules.damage import inflict_damage

    pj, trait, objetivo, ctx = _marcado()
    # Caducada: ronda 1 con caduca en la ronda 1.
    objetivo.state.marca_cavalier[pj.name] = (1, pj)
    tercero = Monster("Tercero", max_hp=40, ac=12, abilities=_abilities())
    ctx.combatants = [pj, objetivo, tercero]
    inflict_damage(tercero, 5, source=objetivo, ctx=ctx)
    assert trait.ataque_marca_pendiente == 0
    assert trait.ataque_marca_objetivo is None


def test_el_ataque_especial_solo_vale_en_el_siguiente_turno():
    from dnd_sim.model.actions import TurnResources

    pj, trait, _, _, ctx = _especial()
    accion = _accion_marca(pj)
    ctx.rng = _RngExplota()  # la elegibilidad no toca el RNG
    # Flag futuro (aún no es su turno): no elegible.
    assert not accion.can_use(TurnResources(), ctx)
    trait.on_turn_start(pj)  # turno 1 == flag
    assert accion.can_use(TurnResources(), ctx)
    trait.on_turn_start(pj)  # turno 2: caducó sin usarse
    assert not accion.can_use(TurnResources(), ctx)
    assert trait.ataque_marca_pendiente == 0
    assert trait.ataque_marca_objetivo is None


def test_no_es_elegible_sin_flag_sin_bonus_libre_sin_ataque_o_sin_marcado():
    from dnd_sim.model.actions import TurnResources

    pj, trait, marcado, _, ctx = _especial()
    accion = _accion_marca(pj)
    ctx.rng = _RngExplota()
    # Flag futuro → no elegible.
    assert not accion.can_use(TurnResources(), ctx)
    trait.on_turn_start(pj)
    # Control: con todo en orden sí.
    assert accion.can_use(TurnResources(), ctx)
    # Acción bonus ya gastada.
    assert not accion.can_use(TurnResources(bonus_action_used=True), ctx)
    # Sin ataque cuerpo a cuerpo.
    golpes = list(pj.attacks)
    pj.attacks = []
    pj.weapons = []
    pj.dynamic_weapons = []
    assert not accion.can_use(TurnResources(), ctx)
    pj.attacks = golpes
    # Marcado muerto.
    marcado.dead = True
    assert not accion.can_use(TurnResources(), ctx)


def test_el_ataque_especial_tira_con_ventaja(monkeypatch):
    from dnd_sim.core.dice import RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod

    monkeypatch.setattr(cav_mod, "pick", _pick_sin_decision)
    modos = []
    _parchea_ataque(monkeypatch, modos=modos)
    pj, trait, _, _, ctx = _especial()
    trait.on_turn_start(pj)
    _accion_marca(pj).execute(ctx)
    assert modos == [RollMode.ADVANTAGE]
    # Ataque único: el flag se consume al ejecutar.
    assert trait.ataque_marca_pendiente == 0
    assert trait.ataque_marca_objetivo is None


def test_el_ataque_especial_suma_el_dano_extra_si_impacta(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod

    monkeypatch.setattr(cav_mod, "pick", _pick_sin_decision)
    _parchea_ataque(monkeypatch, dados=1)
    # Estilo fijo sin bono de daño (el estilo por defecto es aleatorio).
    pj, trait, marcado, _, ctx = _especial(fighting_style="Archery")
    trait.on_turn_start(pj)
    _accion_marca(pj).execute(ctx)
    # 1 (arma) + 3 (FUE 16) + 2 (nivel 5 // 2) = 6 de daño.
    assert marcado.hp == 54


def test_el_ataque_especial_no_suma_dano_extra_si_falla(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod

    monkeypatch.setattr(cav_mod, "pick", _pick_sin_decision)
    _parchea_ataque(monkeypatch, valor_d20=1)
    pj, trait, marcado, _, ctx = _especial(fighting_style="Archery")
    trait.on_turn_start(pj)
    _accion_marca(pj).execute(ctx)
    assert marcado.hp == 60  # fallo: ni daño base ni extra


def test_el_ataque_especial_no_gasta_un_uso_ni_la_reaccion(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod

    monkeypatch.setattr(cav_mod, "pick", _pick_sin_decision)
    _parchea_ataque(monkeypatch)
    pj, trait, _, _, ctx = _especial(fighting_style="Archery")
    usos = trait.marca_usos.uses_left
    trait.on_turn_start(pj)
    _accion_marca(pj).execute(ctx)
    assert trait.marca_usos.uses_left == usos
    assert not pj.state.reaction_used  # es acción bonus, no reacción


def test_sin_subclase_el_dano_no_consulta_ataques_especiales():
    from dnd_sim.rules.damage import inflict_damage

    class _Espia:
        def marcar_ataque_especial(self, marcado, ctx):
            raise AssertionError("consulta de ataque especial sin subclase")

    pj = _pj()
    apply_fighter(pj, level=5)
    pj.traits.append(_Espia())  # el duck-typing lo vería si consultara
    victima = Monster("Víctima", max_hp=60, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(round=1, combatants=[pj, victima])
    inflict_damage(victima, 5, source=pj, ctx=ctx)
    assert victima.hp == 55  # el daño sigue su camino normal


def test_la_velocidad_cero_del_ataque_especial_es_dato_sin_efecto():
    # El modelo no tiene campo de velocidad: no hay nada que poner a 0.
    pj, trait, marcado, _, _ = _especial()
    assert not hasattr(pj, "speed")
    assert not hasattr(marcado, "speed")


# --- A5: Warding Maneuver -----------------------------------------------------


def _bajo_ataque(level: int = 7, **kwargs) -> tuple:
    """PJ Cavalier + aliado + enemigo, para Warding (7+) y Hold (10+)."""
    pj, trait = _cavalier(level=level, **kwargs)
    aliado = _pj(name="Alicia")
    enemigo = Monster("Enemigo", max_hp=60, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(round=1, actor=pj, rng=random.Random(1),
                           combatants=[pj, aliado, enemigo], log=None)
    return pj, trait, aliado, enemigo, ctx


def _defiende(trait, target, ctx, rng):
    """Consulta directa del hook con el dueño como atacante."""
    return trait.defensa_ante_ataque(
        target, trait.owner, AttackRange.MELEE, total=15, ca=15,
        ctx=ctx, rng=rng)


def _parchea_warding(monkeypatch, *, d20=10, dados=1, d8=8):
    """d20 y daño del arma (motor) + 1d8 y decisiones (Cavalier)."""
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod

    d8s = []
    monkeypatch.setattr(cav_mod, "pick", lambda rng, seq: seq[-1])
    monkeypatch.setattr(
        cav_mod, "roll_dice",
        lambda expr, rng, crit=False: (d8s.append(expr), d8)[1])
    _parchea_ataque(monkeypatch, valor_d20=d20, dados=dados)
    return d8s


def test_warding_convierte_el_impacto_en_fallo(monkeypatch):
    from dnd_sim.engine.combat import attack as atk_mod

    d8s = _parchea_warding(monkeypatch, d20=10, d8=8)
    pj, trait, _, enemigo, ctx = _bajo_ataque()
    # Sin Warding el golpe entraría (10 + 5 = CA 15); el 1d8 lo convierte.
    atk = Attack("Golpe", "1d6", ability="str")
    atk_mod.attack_roll(enemigo, pj, atk, random.Random(1), ctx=ctx)
    assert pj.hp == 70  # ni daño ni PV temporales: falló
    assert pj.state.reaction_used
    assert trait.warding_usos.uses_left == trait.warding_usos.uses_max - 1
    assert d8s == ["1d8"]  # UNA sola tirada


def test_warding_protege_al_aliado_del_cavalier(monkeypatch):
    from dnd_sim.engine.combat import attack as atk_mod

    _parchea_warding(monkeypatch, d20=10, d8=8)
    pj, trait, aliado, enemigo, ctx = _bajo_ataque()
    atk = Attack("Golpe", "1d6", ability="str")
    atk_mod.attack_roll(enemigo, aliado, atk, random.Random(1), ctx=ctx)
    assert aliado.hp == 70  # el 1d8 del Cavalier convirtió el golpe
    assert pj.state.reaction_used  # la reacción es del Cavalier
    assert not aliado.state.reaction_used
    assert trait.warding_usos.uses_left == trait.warding_usos.uses_max - 1


def test_warding_no_convierte_un_critico_natural_y_aun_asi_resiste(
        monkeypatch):
    from dnd_sim.engine.combat import attack as atk_mod

    _parchea_warding(monkeypatch, d20=20, dados=3, d8=8)
    pj, trait, _, enemigo, ctx = _bajo_ataque(fighting_style="Archery")
    atk = Attack("Golpe", "1d6", ability="str")
    atk_mod.attack_roll(enemigo, pj, atk, random.Random(1), ctx=ctx)
    # 20 natural: impacta pese al 1d8; resistencia 6 -> 3.
    assert pj.hp == 67
    assert pj.state.reaction_used


def test_warding_resiste_la_mitad_redondeando_hacia_abajo(monkeypatch):
    from dnd_sim.engine.combat import attack as atk_mod

    _parchea_warding(monkeypatch, d20=12, dados=2, d8=1)
    pj, trait, _, enemigo, ctx = _bajo_ataque(fighting_style="Archery")
    atk = Attack("Golpe", "1d6", ability="str")
    atk_mod.attack_roll(enemigo, pj, atk, random.Random(1), ctx=ctx)
    # 2 + 3 (FUE) = 5 -> resistencia -> 2 (suelo); golpe entra (17 >= 16).
    assert pj.hp == 68


def test_warding_no_se_acumula_con_la_resistencia_previa(monkeypatch):
    from dnd_sim.engine.combat import attack as atk_mod

    _parchea_warding(monkeypatch, d20=12, dados=2, d8=1)
    pj, trait, _, enemigo, ctx = _bajo_ataque(fighting_style="Archery")
    atk = Attack("Golpe", "1d6", ability="str")
    pj.resistances = {atk.damage_type}  # ya resistía por otro origen
    atk_mod.attack_roll(enemigo, pj, atk, random.Random(1), ctx=ctx)
    # 5 -> una sola mitad (2), no dos (1).
    assert pj.hp == 68
    # Y la resistencia propia sigue intacta tras el ataque.
    assert pj.resistances == {atk.damage_type}


def test_warding_gasta_la_reacción_y_un_uso_y_tira_el_d8_una_vez(
        monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod

    d8s = []
    monkeypatch.setattr(
        cav_mod, "roll_dice",
        lambda expr, rng, crit=False: (d8s.append(expr), 8)[1])
    pj, trait, _, _, ctx = _bajo_ataque()
    resultado = _defiende(trait, pj, ctx, _RngSi())
    assert resultado is not None
    assert resultado.ac_extra == 8
    assert resultado.resistencia is True
    assert pj.state.reaction_used
    assert trait.warding_usos.uses_left == trait.warding_usos.uses_max - 1
    assert d8s == ["1d8"]


def test_warding_no_se_pregunta_si_el_ataque_no_iba_a_entrar(monkeypatch):
    from dnd_sim.engine.combat import attack as atk_mod

    def _revienta(*args, **kwargs):
        raise AssertionError("consulta de defensa en un ataque que falla")

    monkeypatch.setattr(atk_mod, "_defensa_del_bando", _revienta)
    _parchea_ataque(monkeypatch, valor_d20=1)
    pj, trait, _, enemigo, ctx = _bajo_ataque()
    atk = Attack("Golpe", "1d6", ability="str")
    atk_mod.attack_roll(enemigo, pj, atk, random.Random(1), ctx=ctx)
    assert pj.hp == 70  # 1 natural: fallo sin consultar a nadie


def test_warding_no_se_usa_por_debajo_del_nivel_7():
    pj, trait, _, _, ctx = _bajo_ataque()
    trait.level = 6
    assert _defiende(trait, pj, ctx, _RngExplota()) is None


def test_warding_no_protege_a_un_enemigo():
    pj, trait, _, enemigo, ctx = _bajo_ataque()
    assert _defiende(trait, enemigo, ctx, _RngExplota()) is None


def test_warding_no_se_usa_sin_reacción_o_sin_usos():
    pj, trait, _, _, ctx = _bajo_ataque()
    pj.state.reaction_used = True
    assert _defiende(trait, pj, ctx, _RngExplota()) is None
    pj.state.reaction_used = False
    trait.warding_usos.uses_left = 0
    assert _defiende(trait, pj, ctx, _RngExplota()) is None
    assert trait.warding_usos.uses_left == 0  # ni un uso gastado


def test_warding_no_se_usa_sin_escudo_ni_arma_cuerpo_a_cuerpo():
    pj, trait, _, _, ctx = _bajo_ataque()
    # tiene_escudo ya es False (sin escudo en la plantilla).
    pj.attacks = []
    pj.weapons = []
    pj.dynamic_weapons = []
    assert _defiende(trait, pj, ctx, _RngExplota()) is None


def test_warding_comparte_la_reacción_con_las_demás_reacciones():
    # Parry/Riposte/Hold the Line usan el mismo reaction_used: una por
    # ronda para todo el bando de reacciones.
    pj, trait, _, _, ctx = _bajo_ataque()
    pj.state.reaction_used = True
    assert _defiende(trait, pj, ctx, _RngExplota()) is None
    assert trait.warding_usos.uses_left == trait.warding_usos.uses_max


def test_warding_con_decision_negativa_no_gasta_nada(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod

    monkeypatch.setattr(cav_mod, "pick", lambda rng, seq: "no")
    pj, trait, _, _, ctx = _bajo_ataque()
    assert _defiende(trait, pj, ctx, random.Random(1)) is None
    assert not pj.state.reaction_used
    assert trait.warding_usos.uses_left == trait.warding_usos.uses_max


def test_sin_subclase_la_defensa_ante_ataque_no_consulta_ni_toca_rng():
    from dnd_sim.engine.combat import attack as atk_mod

    pj = _pj()
    apply_fighter(pj, level=5)
    enemigo = Monster("Enemigo", max_hp=60, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(round=1, combatants=[pj, enemigo])
    resultado = atk_mod._defensa_del_bando(
        pj, enemigo, AttackRange.MELEE, total=15, ca=15,
        ctx=ctx, rng=_RngExplota())
    assert resultado is None  # sin rasgo que lo defina: ni RNG ni tiradas


# --- A6: Hold the Line --------------------------------------------------------


def test_hold_the_line_contraataca_al_que_ataca_a_un_aliado(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod
    from dnd_sim.engine.combat import attack as atk_mod

    monkeypatch.setattr(cav_mod, "pick", lambda rng, seq: seq[-1])
    _parchea_ataque(monkeypatch, valor_d20=15, dados=1)
    pj, trait, aliado, enemigo, ctx = _bajo_ataque(level=10)
    # Sin usos de Warding: la consulta de CA ocurre ANTES y gastaría la
    # reacción que Hold the Line necesita (una por ronda compartida).
    trait.warding_usos.uses_left = 0
    atk = Attack("Golpe", "1d6", ability="str")
    atk_mod.attack_roll(enemigo, aliado, atk, random.Random(1), ctx=ctx)
    assert aliado.hp == 66  # golpe enemigo entra (15 + 5 >= CA 15): 1+3
    assert pj.state.reaction_used  # la reacción es del Cavalier
    assert enemigo.hp == 56  # contraataque cuerpo a cuerpo: 1+3


def test_hold_the_line_no_se_dispara_si_el_objeto_es_el_dueño(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod
    from dnd_sim.engine.combat import attack as atk_mod

    monkeypatch.setattr(cav_mod, "pick", lambda rng, seq: seq[-1])
    _parchea_ataque(monkeypatch, valor_d20=15, dados=1)
    pj, trait, aliado, enemigo, ctx = _bajo_ataque(level=10)
    trait.warding_usos.uses_left = 0
    atk = Attack("Golpe", "1d6", ability="str")
    atk_mod.attack_roll(enemigo, pj, atk, random.Random(1), ctx=ctx)
    assert not pj.state.reaction_used  # el dueño no se contraataca a sí mismo
    assert enemigo.hp == 60  # nadie más contraataca


def test_hold_the_line_no_lo_dispara_un_hechizo_de_salvación(monkeypatch):
    from dnd_sim.engine.combat import attack as atk_mod
    from dnd_sim.rules.saves import SaveDamage, apply_save_damage

    def _revienta(*args, **kwargs):
        raise AssertionError("la oportunidad se consultó en una salvación")

    monkeypatch.setattr(atk_mod, "_oportunidad_contra_bando", _revienta)
    pj, trait, aliado, enemigo, ctx = _bajo_ataque(level=10)
    efecto = SaveDamage(ability="dex", dc=13, damage="2d6",
                        damage_type="fire", on_success="half")
    apply_save_damage(enemigo, aliado, efecto, 7, ctx)
    assert aliado.hp <= 70  # el daño de la salvación sigue su camino normal


def test_hold_the_line_no_se_usa_sin_reacción_o_sin_ataque_cuerpo_a_cuerpo():
    # La reacción es la misma que Parry/Warding/Riposte: una por ronda.
    pj, trait, aliado, enemigo, ctx = _bajo_ataque(level=10)
    pj.state.reaction_used = True
    assert trait.ataque_de_oportunidad(
        enemigo, aliado, ctx=ctx, rng=_RngExplota()) is None
    pj.state.reaction_used = False
    pj.attacks = []
    pj.weapons = []
    pj.dynamic_weapons = []
    assert trait.ataque_de_oportunidad(
        enemigo, aliado, ctx=ctx, rng=_RngExplota()) is None


def test_hold_the_line_no_reentra_con_un_ataque_de_reacción():
    pj, trait, aliado, enemigo, ctx = _bajo_ataque(level=10)
    ctx.is_reaction = True  # contraataque propio, Retaliation, Riposte…
    assert trait.ataque_de_oportunidad(
        enemigo, aliado, ctx=ctx, rng=_RngExplota()) is None


def test_hold_the_line_exige_nivel_10():
    pj, trait, aliado, enemigo, ctx = _bajo_ataque(level=10)
    trait.level = 9
    assert trait.ataque_de_oportunidad(
        enemigo, aliado, ctx=ctx, rng=_RngExplota()) is None


def test_hold_the_line_no_contra_un_atacante_muerto_o_no_enemigo():
    pj, trait, aliado, enemigo, ctx = _bajo_ataque(level=10)
    enemigo.dead = True
    assert trait.ataque_de_oportunidad(
        enemigo, aliado, ctx=ctx, rng=_RngExplota()) is None
    enemigo.dead = False
    otro_pj = _pj(name="Berto")  # mismo bando que el dueño: no es enemigo
    assert trait.ataque_de_oportunidad(
        otro_pj, aliado, ctx=ctx, rng=_RngExplota()) is None


def test_hold_the_line_con_decision_negativa_no_gasta_nada(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod

    monkeypatch.setattr(cav_mod, "pick", lambda rng, seq: "no")
    pj, trait, aliado, enemigo, ctx = _bajo_ataque(level=10)
    assert trait.ataque_de_oportunidad(
        enemigo, aliado, ctx=ctx, rng=random.Random(1)) is None
    assert not pj.state.reaction_used


def test_sin_subclase_la_oportunidad_no_consulta_ni_toca_rng():
    from dnd_sim.engine.combat import attack as atk_mod

    pj = _pj()
    apply_fighter(pj, level=10)
    aliado = _pj(name="Alicia")
    enemigo = Monster("Enemigo", max_hp=60, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(round=1, combatants=[pj, aliado, enemigo])
    # Sin rasgo con el método: ni consulta ni RNG (rng que revienta).
    atk_mod._oportunidad_contra_bando(aliado, enemigo, ctx=ctx,
                                      rng=_RngExplota())


# --- A7: Vigilant Defender ----------------------------------------------------


def test_vigilant_defender_no_tiene_reacción_especial_por_debajo_del_nivel_18():
    pj, trait, aliado, enemigo, ctx = _bajo_ataque(level=17)
    ctx.actor = enemigo
    pj.state.reaction_used = True  # sin especial y sin normal: nada
    assert trait.ataque_de_oportunidad(
        enemigo, aliado, ctx=ctx, rng=_RngExplota()) is None


def test_vigilant_defender_la_especial_se_consume_antes_que_la_normal(
        monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod

    monkeypatch.setattr(cav_mod, "pick", lambda rng, seq: seq[-1])
    _parchea_ataque(monkeypatch, valor_d20=15, dados=1)
    pj, trait, aliado, enemigo, ctx = _bajo_ataque(level=18)
    ctx.actor = enemigo  # turno del enemigo, no del Cavalier
    trait.ataque_de_oportunidad(enemigo, aliado, ctx=ctx,
                                rng=random.Random(1))
    assert trait.especial_usada_en_ronda == 1
    assert not pj.state.reaction_used  # la reacción normal queda intacta


def test_vigilant_defender_se_restablece_al_empezar_cada_ronda(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod

    monkeypatch.setattr(cav_mod, "pick", lambda rng, seq: seq[-1])
    _parchea_ataque(monkeypatch, valor_d20=15, dados=1)
    pj, trait, aliado, enemigo, ctx = _bajo_ataque(level=18)
    ctx.actor = enemigo
    # Ronda 1: gasta la especial.
    trait.ataque_de_oportunidad(enemigo, aliado, ctx=ctx,
                                rng=random.Random(1))
    assert trait.especial_usada_en_ronda == 1
    # Sigue en ronda 1: sin especial, cae a la reacción normal.
    trait.ataque_de_oportunidad(enemigo, aliado, ctx=ctx,
                                rng=random.Random(1))
    assert pj.state.reaction_used
    assert trait.especial_usada_en_ronda == 1  # la normal no la toca
    # Ronda 2: la especial vuelve a estar disponible.
    ctx.round = 2
    trait.ataque_de_oportunidad(enemigo, aliado, ctx=ctx,
                                rng=random.Random(1))
    assert trait.especial_usada_en_ronda == 2


def test_vigilant_defender_solo_sirve_para_hold_the_line():
    # Warding (y Parry/Riposte) siguen mirando SOLO la reacción normal.
    pj, trait, _, _, ctx = _bajo_ataque(level=18)
    pj.state.reaction_used = True
    assert _defiende(trait, pj, ctx, _RngExplota()) is None
    assert trait.especial_usada_en_ronda == 0  # la especial no se gastó


def test_vigilant_defender_dos_oportunidades_en_una_ronda_con_ambas_reacciones_libres(
        monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod
    from dnd_sim.engine.combat import attack as atk_mod

    monkeypatch.setattr(cav_mod, "pick", lambda rng, seq: seq[-1])
    _parchea_ataque(monkeypatch, valor_d20=15, dados=1)
    pj, trait, aliado, enemigo, ctx = _bajo_ataque(level=18)
    ctx.actor = enemigo
    trait.warding_usos.uses_left = 0  # que la consulta de CA no gaste reacción
    atk = Attack("Golpe", "1d6", ability="str")
    atk_mod.attack_roll(enemigo, aliado, atk, random.Random(1), ctx=ctx)
    assert trait.especial_usada_en_ronda == 1
    assert not pj.state.reaction_used
    atk_mod.attack_roll(enemigo, aliado, atk, random.Random(1), ctx=ctx)
    assert pj.state.reaction_used  # la segunda oportunidad usa la normal
    assert enemigo.hp == 52  # dos contraataques de 1 + 3
    assert aliado.hp == 62  # dos golpes enemigos de 1 + 3


def test_vigilant_defender_no_usa_la_especial_en_el_turno_propio():
    pj, trait, aliado, enemigo, ctx = _bajo_ataque(level=18)
    ctx.actor = pj  # turno del propio Cavalier: sin especial
    pj.state.reaction_used = True  # y la normal ya gastada
    assert trait.ataque_de_oportunidad(
        enemigo, aliado, ctx=ctx, rng=_RngExplota()) is None

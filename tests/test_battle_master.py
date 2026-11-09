"""Subclase Battle Master (Maestro de Batalla, PHB 2024): tablas y registro."""
from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from dnd_sim import Abilities, Attack, Monster, PlayerCharacter, apply_class
from dnd_sim.core.classes import (
    BATTLE_MASTER_MANEUVERS,
    FIGHTER_SKILLS,
    maneuvers_known_count,
    superiority_die_sides,
    superiority_dice_count,
)
from dnd_sim.core.enums import AttackRange
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import (
    BattleMasterFeatures,
    apply_battle_master,
)


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=10, wis=12, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Rolando", max_hp=70, ac=15, level=5, abilities=_abilities(),
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


def _trait(pj) -> BattleMasterFeatures:
    for trait in pj.traits:
        if isinstance(trait, BattleMasterFeatures):
            return trait
    raise AssertionError("falta BattleMasterFeatures")


def _bm(level: int = 5, **kwargs) -> tuple:
    pj = _pj(level=level)
    apply_fighter(pj, level=level)
    trait = apply_battle_master(pj, level=level, **kwargs)
    return pj, trait


def test_tabla_de_dados_de_superioridad_por_nivel():
    esperado = {1: 0, 2: 0, 3: 4, 6: 4, 7: 5, 14: 5, 15: 6, 20: 6}
    assert {lvl: superiority_dice_count(lvl) for lvl in esperado} == esperado


def test_tabla_de_caras_del_dado_por_nivel():
    esperado = {1: 8, 9: 8, 10: 10, 17: 10, 18: 12, 20: 12}
    assert {lvl: superiority_die_sides(lvl) for lvl in esperado} == esperado


def test_tabla_de_maniobras_conocidas_por_nivel():
    esperado = {1: 0, 2: 0, 3: 3, 6: 3, 7: 5, 9: 5, 10: 7, 14: 7,
                15: 9, 20: 9}
    assert {lvl: maneuvers_known_count(lvl) for lvl in esperado} == esperado


def test_el_pool_solo_contiene_las_maniobras_implementadas():
    assert len(BATTLE_MASTER_MANEUVERS) == 11
    assert "Precision Attack" in BATTLE_MASTER_MANEUVERS
    assert "Feinting Attack" in BATTLE_MASTER_MANEUVERS
    assert "Parry" not in BATTLE_MASTER_MANEUVERS  # sesión 2
    assert len(set(BATTLE_MASTER_MANEUVERS)) == len(BATTLE_MASTER_MANEUVERS)


# --- Registro y equivalencia --------------------------------------------------

def test_registro_battle_master_bajo_fighter():
    subclases = CLASSES["fighter"].subclasses
    assert set(subclases) == {"arcane_archer", "battle_master"}
    sub = subclases["battle_master"]
    assert sub.class_name == "fighter"
    assert sub.min_level == 3


def test_apply_class_equivalente_a_apply_battle_master(monkeypatch):
    """Misma semilla en los dos RNG de creación: resultados idénticos."""
    import dnd_sim.rules.classes.fighter.features as fighter_mod
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod

    a = _pj()
    b = _pj()
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    monkeypatch.setattr(bm_mod, "_RNG_CREACION", random.Random(0))
    apply_class(a, "fighter", "battle_master", level=5)
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    monkeypatch.setattr(bm_mod, "_RNG_CREACION", random.Random(0))
    apply_fighter(b, level=5)
    apply_battle_master(b, level=5)
    assert _firmas(a) == _firmas(b)
    assert _trait(a).maneuvers == _trait(b).maneuvers
    assert _trait(a).competencia == _trait(b).competencia


def test_apply_battle_master_exige_la_clase_fighter():
    with pytest.raises(ValueError, match="Primero aplica la clase guerrero"):
        apply_battle_master(_pj())


def test_apply_battle_master_requiere_nivel_3():
    pj = _pj(level=2)
    apply_fighter(pj, level=2)
    with pytest.raises(ValueError, match=">= 3"):
        apply_battle_master(pj, level=2)


def test_registro_de_subclase_requiere_nivel_3():
    with pytest.raises(ValueError, match=">= 3"):
        apply_class(_pj(level=2), "fighter", "battle_master")


# --- Maniobras conocidas -------------------------------------------------------

def test_maniobras_conocidas_segun_nivel():
    casos = {3: 3, 6: 3, 7: 5, 10: 7, 15: 9}
    for nivel, cuenta in casos.items():
        pj = _pj(level=nivel)
        apply_fighter(pj, level=nivel)
        trait = apply_battle_master(pj, level=nivel)
        assert len(trait.maneuvers) == cuenta
        assert len(set(trait.maneuvers)) == cuenta
        assert set(trait.maneuvers) <= set(BATTLE_MASTER_MANEUVERS)


def test_kwarg_de_maniobras_explicitas_valido():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    elegidas = ("Menacing Attack", "Trip Attack", "Precision Attack")
    trait = apply_battle_master(pj, level=3, maneuvers=elegidas)
    assert trait.maneuvers == list(elegidas)


def test_kwarg_de_maniobras_invalidas_da_value_error():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    with pytest.raises(ValueError, match="no es una maniobra de Battle Master"):
        apply_battle_master(
            pj, level=3,
            maneuvers=("Maniobra inventada", "Trip Attack", "Precision Attack"))


def test_kwarg_con_recuento_equivocado_da_value_error():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    with pytest.raises(ValueError, match="se esperaban 3 maniobras"):
        apply_battle_master(pj, level=3, maneuvers=("Trip Attack",))


# --- Student of War y Know Your Enemy -----------------------------------------

def test_student_of_war_anade_una_habilidad_que_no_tenia():
    pj = _pj(level=3)
    apply_fighter(pj, level=3, skills=("athletics",))
    trait = apply_battle_master(pj, level=3)
    assert trait.competencia in FIGHTER_SKILLS
    assert trait.competencia in pj.skill_proficiencies
    assert trait.competencia != "athletics"  # no repite la existente


def test_student_of_war_sin_candidatas_no_cambia_nada():
    pj = _pj(level=3)
    apply_fighter(pj, level=3, skills=tuple(FIGHTER_SKILLS))
    antes = set(pj.skill_proficiencies)
    trait = apply_battle_master(
        pj, level=3, rng=_ExplotaSiUsaRng(),
        maneuvers=("Menacing Attack", "Trip Attack", "Precision Attack"))
    assert trait.competencia == ""
    assert set(pj.skill_proficiencies) == antes


def test_student_of_war_guarda_las_herramientas_como_dato():
    _, trait = _bm(level=3)
    assert trait.herramientas == "herramientas de artesano"


def test_know_your_enemy_es_un_dato_desde_el_nivel_7():
    assert _bm(level=3)[1].know_your_enemy is False
    assert _bm(level=7)[1].know_your_enemy is True


# --- Dados de superioridad -----------------------------------------------------

def test_los_dados_y_su_tamano_siguen_las_tablas():
    assert _bm(level=3)[1].dados_restantes == 4
    assert _bm(level=7)[1].dados_restantes == 5
    assert _bm(level=15)[1].dados_restantes == 6
    assert _bm(level=3)[1].dados_lados == 8
    assert _bm(level=10)[1].dados_lados == 10
    assert _bm(level=18)[1].dados_lados == 12


def test_reset_rellena_los_dados_y_limpia_estado():
    _, trait = _bm(level=3)
    trait.dados_restantes = 0
    trait.relentless_used_this_turn = True
    trait.feinting_pendiente = True
    trait.maniobra_pendiente = "Trip Attack"
    trait.reset()
    assert trait.dados_restantes == 4
    assert trait.relentless_used_this_turn is False
    assert trait.feinting_pendiente is False
    assert trait.maniobra_pendiente is None


def test_on_turn_start_reinicia_sin_rng():
    _, trait = _bm(level=15)
    trait.relentless_used_this_turn = True
    trait.feinting_pendiente = True
    trait.maniobra_pendiente = "Feinting Attack"
    trait.on_turn_start(trait.owner)
    assert trait.relentless_used_this_turn is False
    assert trait.feinting_pendiente is False
    assert trait.maniobra_pendiente is None


class _ExplotaSiUsaRng:
    """Cualquier acceso a RNG hace fallar el test."""

    def __getattr__(self, name: str):
        raise AssertionError(f"RNG no debería usarse: {name}")


# --- Punto de decisión único y gasto del dado (A3) ----------------------------

class _RngSi:
    """randrange siempre el último elemento («si» / última opción)."""

    def randrange(self, n: int) -> int:
        return n - 1

    def random(self) -> float:
        return 1.0

    def randint(self, a: int, b: int) -> int:
        return b


class _RngIdx:
    """Devuelve los índices dados en orden (y «si» cuando se acaban)."""

    def __init__(self, *idxs: int) -> None:
        self.idxs = list(idxs)
        self.llamadas = 0

    def randrange(self, n: int) -> int:
        self.llamadas += 1
        if not self.idxs:
            return n - 1
        i = self.idxs.pop(0)
        return i if i < n else n - 1

    def random(self) -> float:
        return 1.0


def _completa(elegidas: tuple, level: int) -> tuple:
    """Rellena las maniobras pedidas hasta el recuento del nivel."""
    elegidas = list(elegidas)
    resto = [m for m in BATTLE_MASTER_MANEUVERS if m not in elegidas]
    falta = max(0, maneuvers_known_count(level) - len(elegidas))
    return tuple(elegidas + resto[:falta])


def _atacado(level: int = 5, **kwargs) -> tuple:
    """PJ Battle Master + objetivo, para probar la decisión."""
    if "maneuvers" in kwargs:
        kwargs["maneuvers"] = _completa(kwargs["maneuvers"], level)
    pj, trait = _bm(level=level, **kwargs)
    objetivo = Monster("Muñeco", max_hp=60, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(round=1, combatants=[pj, objetivo])
    return pj, trait, objetivo, ctx


def _decide(trait, target, ctx, rng, *, hit=True, total=15, ca=12,
            rango=AttackRange.MELEE):
    atk = Attack("Espada larga", "1d8", ability="str")
    return trait.decidir_maniobra(
        trait.owner, target, atk, rango, roll=10, total=total, ca=ca,
        hit=hit, ctx=ctx, rng=rng)


def test_la_decision_es_un_solo_par_de_picks():
    _, trait, objetivo, ctx = _atacado(
        maneuvers=("Disarming Attack", "Menacing Attack", "Trip Attack"))
    cuenta = _RngIdx(1, 2)
    hit, total = _decide(trait, objetivo, ctx, cuenta)
    assert (hit, total) == (True, 15)
    assert cuenta.llamadas == 2  # «no/sí» + elección uniforme
    assert trait.maniobra_pendiente == "Trip Attack"


def test_las_elegibles_son_equiprobables_con_rng_controlado():
    conocidas = ("Disarming Attack", "Menacing Attack", "Trip Attack")
    for i, esperada in enumerate(conocidas):
        _, trait, objetivo, ctx = _atacado(maneuvers=conocidas)
        _decide(trait, objetivo, ctx, _RngIdx(1, i))
        assert trait.maniobra_pendiente == esperada


def test_las_solo_cuerpo_a_cuerpo_no_son_elegibles_a_distancia():
    _, trait, objetivo, ctx = _atacado(
        maneuvers=("Lunging Attack", "Menacing Attack", "Trip Attack"))
    _decide(trait, objetivo, ctx, _RngIdx(1, 2), rango=AttackRange.RANGED)
    # Lunging filtra (rango a distancia): el pool de 2 → índice 1 final.
    assert trait.maniobra_pendiente == "Trip Attack"


def test_el_uso_no_se_gasta_si_no_se_ejecuta():
    # Solo Menacing es de impacto: Feinting es acción bonus y Precision es de fallo.
    _, trait, objetivo, ctx = _atacado(
        maneuvers=("Menacing Attack", "Feinting Attack", "Precision Attack"))
    _decide(trait, objetivo, ctx, _RngIdx(1, 0))
    assert trait.maniobra_pendiente == "Menacing Attack"
    assert trait.dados_restantes == 4  # elegida, no ejecutada
    daño = trait.extra_attack_damage(
        trait.owner, objetivo, AttackRange.MELEE, ctx=ctx,
        rng=random.Random(1), atk=Attack("Espada larga", "1d8", ability="str"))
    assert daño > 0
    assert trait.dados_restantes == 3  # ejecutada → gastada
    assert trait.maniobra_pendiente is None


def test_una_maniobra_por_ataque_como_maximo():
    _, trait, objetivo, ctx = _atacado(maneuvers=("Menacing Attack",))
    _decide(trait, objetivo, ctx, _RngIdx(1, 0))
    pendiente = trait.maniobra_pendiente
    _decide(trait, objetivo, ctx, _ExplotaSiUsaRng())  # ya hay pendiente
    assert trait.maniobra_pendiente == pendiente


def test_sin_datos_cero_rng_en_la_decision():
    _, trait, objetivo, ctx = _atacado(maneuvers=("Menacing Attack",))
    trait.dados_restantes = 0
    hit, total = _decide(trait, objetivo, ctx, _ExplotaSiUsaRng())
    assert (hit, total) == (True, 15)
    assert trait.maniobra_pendiente is None


def test_en_un_fallo_sin_precision_cero_rng():
    _, trait, objetivo, ctx = _atacado(maneuvers=("Menacing Attack",))
    hit, total = _decide(trait, objetivo, ctx, _ExplotaSiUsaRng(), hit=False)
    assert (hit, total) == (False, 15)
    assert trait.maniobra_pendiente is None


def test_sin_subclase_el_motor_no_consulta_ni_consume_rng():
    from dnd_sim.engine.combat import attack as atk_mod

    pj = _pj()
    apply_fighter(pj, level=5)
    resultado = atk_mod._decidir_maniobra(
        pj, Monster("Blanco", max_hp=10, ac=10, abilities=_abilities()),
        Attack("Espada larga", "1d8", ability="str"), AttackRange.MELEE,
        roll=10, total=17, ca=12, hit=True, ctx=None,
        rng=_ExplotaSiUsaRng(), log=None)
    assert resultado == (True, 17)


def test_el_motor_decide_y_gasta_el_dado_en_el_ataque(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    monkeypatch.setattr(bm_mod, "pick", lambda rng, seq: seq[-1])
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=15, rolls=[15],
                                    mode=RollMode.NORMAL))
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 1)
    pj, trait, objetivo, ctx = _atacado(
        maneuvers=("Disarming Attack", "Menacing Attack", "Trip Attack"))
    atk = Attack("Espada larga", "1d8", ability="str")
    atk_mod.attack_roll(pj, objetivo, atk, random.Random(1), ctx=ctx)
    assert trait.dados_restantes == 3  # la maniobra se decidió y ejecutó
    assert trait.maniobra_pendiente is None
    assert objetivo.hp < objetivo.max_hp


# --- Relentless (15) -----------------------------------------------------------

def test_relentless_tira_d8_sin_gastar_y_solo_una_vez_por_turno():
    _, trait, objetivo, ctx = _atacado(level=15, maneuvers=("Trip Attack",))
    trait.maniobra_pendiente = "Trip Attack"
    daño = trait.extra_attack_damage(
        trait.owner, objetivo, AttackRange.MELEE, ctx=ctx, rng=_RngSi(),
        atk=Attack("Espada larga", "1d8", ability="str"))
    assert daño >= 1
    assert trait.relentless_used_this_turn is True
    assert trait.dados_restantes == 6  # sin gastar el dado
    # Segundo uso en el MISMO turno: Relentless ya gastado → sí gasta.
    trait.maniobra_pendiente = "Trip Attack"
    trait.extra_attack_damage(
        trait.owner, objetivo, AttackRange.MELEE, ctx=ctx, rng=_RngSi(),
        atk=Attack("Espada larga", "1d8", ability="str"))
    assert trait.dados_restantes == 5


def test_relentless_no_consulta_pick_por_debajo_del_nivel_15(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod

    _, trait, objetivo, ctx = _atacado(level=14, maneuvers=("Trip Attack",))

    def _revienta(*args, **kwargs):
        raise AssertionError("Relentless no debe consultarse con < 15")

    monkeypatch.setattr(bm_mod, "pick", _revienta)
    trait.maniobra_pendiente = "Trip Attack"
    trait.extra_attack_damage(
        trait.owner, objetivo, AttackRange.MELEE, ctx=ctx,
        rng=random.Random(1), atk=Attack("Espada larga", "1d8", ability="str"))
    assert trait.dados_restantes == 4  # 5 dados en nivel 14 → 4 tras gastar


def test_relentless_el_dado_es_siempre_d8(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.core import dice

    vistas: list[str] = []
    real = dice.roll_dice

    def _espiar(expr, *args, **kwargs):
        vistas.append(expr)
        return real(expr, *args, **kwargs)

    monkeypatch.setattr(bm_mod, "roll_dice", _espiar)
    _, trait, objetivo, ctx = _atacado(level=18, maneuvers=("Trip Attack",))
    trait.maniobra_pendiente = "Trip Attack"
    trait.extra_attack_damage(
        trait.owner, objetivo, AttackRange.MELEE, ctx=ctx, rng=_RngSi(),
        atk=Attack("Espada larga", "1d8", ability="str"))
    assert vistas == ["1d8"]  # nivel 18: dado d12, Relentless tira d8


# --- Maniobras con salvación (A4) ----------------------------------------------

class _RngFalla:
    """«si» a la decisión, d20 siempre 1 (salvación fallida)."""

    def randrange(self, n: int) -> int:
        return n - 1

    def random(self) -> float:
        return 1.0

    def randint(self, a: int, b: int) -> int:
        return a


def _ejecuta(trait, target, ctx, rng, opcion,
             rango=AttackRange.MELEE) -> int:
    """Ejecuta ``opcion`` directamente (decisión ya tomada)."""
    trait.maniobra_pendiente = opcion
    return trait.extra_attack_damage(
        trait.owner, target, rango, ctx=ctx, rng=rng,
        atk=Attack("Espada larga", "1d8", ability="str"))


def _tiene(target, cond) -> bool:
    return bool(target.conditions.has(cond))


def test_menacing_attack_asusta_si_falla_la_salvacion_de_sabiduria():
    from dnd_sim.rules.conditions import Condition

    _, trait, objetivo, ctx = _atacado(maneuvers=("Menacing Attack",))
    daño = _ejecuta(trait, objetivo, ctx, _RngFalla(), "Menacing Attack")
    assert daño > 0
    assert _tiene(objetivo, Condition.FRIGHTENED)


def test_menacing_attack_no_asusta_si_pasa_la_salvacion():
    from dnd_sim.rules.conditions import Condition

    _, trait, objetivo, ctx = _atacado(maneuvers=("Menacing Attack",))
    daño = _ejecuta(trait, objetivo, ctx, _RngSi(), "Menacing Attack")
    assert daño > 0
    assert not _tiene(objetivo, Condition.FRIGHTENED)


def test_goading_attack_marca_al_objetivo_si_falla_la_salvacion():
    _, trait, objetivo, ctx = _atacado(maneuvers=("Goading Attack",))
    _ejecuta(trait, objetivo, ctx, _RngFalla(), "Goading Attack")
    assert objetivo.state.goading == {trait.owner.name: 3}  # ronda 1 + 2


def test_goading_attack_no_marca_si_pasa_la_salvacion():
    _, trait, objetivo, ctx = _atacado(maneuvers=("Goading Attack",))
    _ejecuta(trait, objetivo, ctx, _RngSi(), "Goading Attack")
    assert objetivo.state.goading == {}


def test_trip_attack_derriba_si_es_grande_o_menor():
    from dnd_sim.rules.conditions import Condition

    _, trait, objetivo, ctx = _atacado(maneuvers=("Trip Attack",))
    assert objetivo.size == "medium"
    daño = _ejecuta(trait, objetivo, ctx, _RngFalla(), "Trip Attack")
    assert daño > 0
    assert _tiene(objetivo, Condition.PRONE)


def test_trip_attack_no_derriba_si_pasa_la_salvacion():
    from dnd_sim.rules.conditions import Condition

    _, trait, objetivo, ctx = _atacado(maneuvers=("Trip Attack",))
    _ejecuta(trait, objetivo, ctx, _RngSi(), "Trip Attack")
    assert not _tiene(objetivo, Condition.PRONE)


def test_trip_attack_no_tira_salvacion_contra_un_objetivo_enorme():
    from dnd_sim.rules.conditions import Condition

    _, trait, objetivo, ctx = _atacado(maneuvers=("Trip Attack",))
    objetivo.size = "huge"
    daño = _ejecuta(trait, objetivo, ctx, _RngFalla(), "Trip Attack")
    # Con salvación, el d20=1 derribaría; sin ella no hay PRONE.
    assert daño > 0
    assert not _tiene(objetivo, Condition.PRONE)


def test_disarming_attack_no_altera_el_combate_mas_que_el_dano():
    _, trait, objetivo, ctx = _atacado(maneuvers=("Disarming Attack",))
    daño = _ejecuta(trait, objetivo, ctx, _RngFalla(), "Disarming Attack")
    assert daño > 0
    assert objetivo.hp == objetivo.max_hp  # el daño lo aplica el motor
    assert objetivo.conditions.instances == []
    assert objetivo.state.goading == {}


def test_efectos_sin_implementacion_no_alteran_el_combate():
    _, trait, objetivo, ctx = _atacado(
        level=7,
        maneuvers=("Disarming Attack", "Pushing Attack", "Maneuvering Attack",
                   "Lunging Attack"))
    total = 0
    for opcion in ("Disarming Attack", "Pushing Attack",
                   "Maneuvering Attack", "Lunging Attack"):
        total += _ejecuta(trait, objetivo, ctx, _RngFalla(), opcion)
    assert total > 0  # cada maniobra aporta su dado (el motor lo suma al golpe)
    assert objetivo.conditions.instances == []
    assert objetivo.state.goading == {}
    assert objetivo.state.at_range is False  # sin movimiento/empuje
    assert objetivo.alive
    assert trait.dados_restantes == 1  # 5 dados en nivel 7 → 4 gastos


def test_el_dano_de_la_maniobra_se_suma_una_sola_vez():
    _, trait, objetivo, ctx = _atacado(maneuvers=("Menacing Attack",))
    primera = _ejecuta(trait, objetivo, ctx, _RngFalla(), "Menacing Attack")
    assert primera > 0
    assert trait.dados_restantes == 3
    segunda = trait.extra_attack_damage(
        trait.owner, objetivo, AttackRange.MELEE, ctx=ctx,
        rng=_RngFalla(), atk=Attack("Espada larga", "1d8", ability="str"))
    assert segunda == 0  # sin pendiente: no se vuelve a aplicar
    assert trait.dados_restantes == 3

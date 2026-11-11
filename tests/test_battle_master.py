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
    assert len(BATTLE_MASTER_MANEUVERS) == 16
    assert "Precision Attack" in BATTLE_MASTER_MANEUVERS
    assert "Feinting Attack" in BATTLE_MASTER_MANEUVERS
    # Reacciones de la sesión 2.
    assert "Parry" in BATTLE_MASTER_MANEUVERS
    assert "Riposte" in BATTLE_MASTER_MANEUVERS
    assert "Commander's Strike" in BATTLE_MASTER_MANEUVERS
    # Rally (B1) y Ambush (B3).
    assert "Rally" in BATTLE_MASTER_MANEUVERS
    assert "Ambush" in BATTLE_MASTER_MANEUVERS
    assert len(set(BATTLE_MASTER_MANEUVERS)) == len(BATTLE_MASTER_MANEUVERS)


def test_bait_and_switch_y_evasive_footwork_quedan_fuera_del_pool():
    # Bait and Switch: exige un bonificador de CA temporal con caducidad y
    # el sim no tiene ninguno (solo defensive_ac_bonus instantáneo).
    # Evasive Footwork: exige modelo de movimiento (fuera de alcance).
    assert "Bait and Switch" not in BATTLE_MASTER_MANEUVERS
    assert "Evasive Footwork" not in BATTLE_MASTER_MANEUVERS


def test_commanding_presence_queda_fuera_del_pool():
    # Commanding Presence: el motor no tira Carisma (Intimidación/Persuasión)
    # en combate, así que el bonificador sería un dato sin efecto.
    assert "Commanding Presence" not in BATTLE_MASTER_MANEUVERS


# --- Registro y equivalencia --------------------------------------------------

def test_registro_battle_master_bajo_fighter():
    subclases = CLASSES["fighter"].subclasses
    # Cambio esperado con Cavalier (2026-11-10, explicado en PASOS).
    # Cambio esperado con Champion (2026-11-11, explicado en PASOS):
    # la clave "champion" se añade al registro.
    assert set(subclases) == {"arcane_archer", "battle_master",
                              "cavalier", "champion"}
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


def test_kwarg_con_las_maniobras_de_reaccion_de_sesion_2_es_valido():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    elegidas = ("Parry", "Riposte", "Commander's Strike")
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


class _RngNo:
    """randrange siempre 0 («no»)."""

    def randrange(self, n: int) -> int:
        return 0


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
            rango=AttackRange.MELEE, roll=10):
    atk = Attack("Espada larga", "1d8", ability="str")
    return trait.decidir_maniobra(
        trait.owner, target, atk, rango, roll=roll, total=total, ca=ca,
        hit=hit, ctx=ctx, rng=rng)


def _atacado_fijo(**kwargs) -> tuple:
    """Como ``_atacado`` pero con Estilo de Combate fijo (Archery).

    El estilo por defecto se elige con el ``_RNG_CREACION`` compartido
    de ``apply_fighter``: depende de cuántos PJ se crearon antes en el
    proceso. Archery no toca el daño cuerpo a cuerpo, así que los
    tests que afirman un número exacto de daño no cambian de orden de
    ejecución.
    """
    if "maneuvers" in kwargs:
        kwargs["maneuvers"] = _completa(kwargs["maneuvers"], 5)
    pj = _pj()
    apply_fighter(pj, level=5, fighting_style="Archery")
    trait = apply_battle_master(pj, level=5, **kwargs)
    objetivo = Monster("Muñeco", max_hp=60, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(round=1, combatants=[pj, objetivo])
    return pj, trait, objetivo, ctx


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


# --- Parry (reacción) (A2) ------------------------------------------------------

# Pool de 3 (recuento del nivel 5) sin maniobras de impacto: la decisión
# de sesión 1 no interviene y cada test de Parry ve solo su «no/sí».
_SOLO_REACCION = ("Commander's Strike", "Feinting Attack", "Parry")


def _parry(trait, rng, *, dmg=10, rango=AttackRange.MELEE):
    """Llama al hook de Parry con el dueño como objetivo (como el motor)."""
    agresor = Monster("Agresor", max_hp=40, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(round=1, combatants=[trait.owner, agresor])
    return trait.reducir_dano_recibido(
        agresor, rango, dmg, ctx=ctx, rng=rng, log=None)


def test_parry_reduce_el_daño_en_dado_mas_mod_fue_o_des():
    _, trait, _, _ = _atacado(maneuvers=_SOLO_REACCION)
    # _RngSi: «si» y d8 = 8; mod FUE +3 → −11 → 15 − 11 = 4.
    assert _parry(trait, _RngSi(), dmg=15) == 4


def test_parry_el_daño_no_baja_de_cero():
    _, trait, _, _ = _atacado(maneuvers=_SOLO_REACCION)
    assert _parry(trait, _RngSi(), dmg=6) == 0


def test_parry_solo_se_dispara_en_ataques_cuerpo_a_cuerpo():
    _, trait, _, _ = _atacado(maneuvers=_SOLO_REACCION)
    assert _parry(trait, _ExplotaSiUsaRng(),
                  rango=AttackRange.RANGED) == 10
    assert trait.owner.state.reaction_used is False


def test_parry_gasta_la_reaccion_y_el_dado():
    _, trait, _, _ = _atacado(maneuvers=_SOLO_REACCION)
    _parry(trait, _RngSi())
    assert trait.owner.state.reaction_used is True
    assert trait.dados_restantes == 3


def test_parry_sin_reaccion_libre_no_reduce_y_no_consume_rng():
    _, trait, _, _ = _atacado(maneuvers=_SOLO_REACCION)
    trait.owner.state.reaction_used = True
    assert _parry(trait, _ExplotaSiUsaRng()) == 10


def test_parry_sin_dados_y_sin_relentless_no_consume_rng():
    _, trait, _, _ = _atacado(maneuvers=_SOLO_REACCION)
    trait.dados_restantes = 0
    assert _parry(trait, _ExplotaSiUsaRng()) == 10


def test_parry_sin_la_maniobra_conocida_no_consume_rng():
    _, trait, _, _ = _atacado(maneuvers=("Feinting Attack", "Precision Attack",
                                         "Riposte"))
    assert _parry(trait, _ExplotaSiUsaRng()) == 10


def test_parry_solo_una_vez_por_ronda():
    _, trait, _, _ = _atacado(maneuvers=_SOLO_REACCION)
    assert _parry(trait, _RngSi(), dmg=15) == 4
    assert _parry(trait, _ExplotaSiUsaRng(), dmg=15) == 15


def test_parry_usa_el_mayor_de_mod_fue_y_des():
    pj = _pj(abilities=_abilities(str=10, dex=18))
    apply_fighter(pj, level=5)
    trait = apply_battle_master(pj, level=5,
                                maneuvers=_completa(("Parry",), 5))
    # mod FUE 0 < mod DES +4: la reducción usa +4 → 15 − (8 + 4) = 3.
    assert _parry(trait, _RngSi(), dmg=15) == 3


def test_parry_con_relentless_no_gasta_el_dado():
    _, trait, _, _ = _atacado(level=15, maneuvers=_SOLO_REACCION)
    # _RngSi: «si» en la decisión y «si» en Relentless → d8 sin gastar.
    assert _parry(trait, _RngSi(), dmg=15) == 4  # 15 − (8 + 3)
    assert trait.dados_restantes == 6  # nivel 15: ninguno gastado
    assert trait.relentless_used_this_turn is True
    assert trait.owner.state.reaction_used is True


def test_parry_se_aplica_en_el_motor_justo_antes_del_daño(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    pj, trait, agresor, ctx = _atacado(maneuvers=_SOLO_REACCION)
    monkeypatch.setattr(bm_mod, "pick", lambda rng, seq: seq[-1])  # «si»
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=15, rolls=[15],
                                    mode=RollMode.NORMAL))
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 1)
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 8)
    atk = Attack("Garra", "1d6", ability="str")
    atk_mod.attack_roll(agresor, pj, atk, random.Random(1), ctx=ctx)
    # daño del arma 1 + mod FUE 3 = 4; Parry: d8 = 8 + 3 → 4 − 11 → 0.
    assert pj.hp == pj.max_hp
    assert pj.state.reaction_used is True
    assert trait.dados_restantes == 3  # 4 iniciales − 1 de Parry


def test_parry_no_se_consulta_si_el_ataque_falla(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    pj, trait, agresor, ctx = _atacado(maneuvers=_SOLO_REACCION)

    def _revienta(*args, **kwargs):
        raise AssertionError("Parry no debe consultarse en un fallo")

    monkeypatch.setattr(bm_mod, "pick", _revienta)
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=1, rolls=[1],
                                    mode=RollMode.NORMAL))
    atk = Attack("Garra", "1d6", ability="str")
    atk_mod.attack_roll(agresor, pj, atk, random.Random(1), ctx=ctx)
    assert pj.hp == pj.max_hp
    assert pj.state.reaction_used is False


def test_parry_no_actua_cuando_el_battle_master_es_el_atacante(monkeypatch):
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=15, rolls=[15],
                                    mode=RollMode.NORMAL))
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 1)
    pj, trait, objetivo, ctx = _atacado(maneuvers=_SOLO_REACCION)
    atk = Attack("Espada larga", "1d8", ability="str")
    atk_mod.attack_roll(pj, objetivo, atk, random.Random(1), ctx=ctx)
    # El hook vive en los rasgos del OBJETIVO: el Monster no reduce nada
    # y la reacción/dados del atacante quedan intactos.
    assert objetivo.hp < objetivo.max_hp
    assert pj.state.reaction_used is False
    assert trait.dados_restantes == 4


def test_sin_subclase_el_motor_no_consulta_la_reduccion_de_dano():
    from dnd_sim.engine.combat import attack as atk_mod

    pj = _pj()
    apply_fighter(pj, level=5)
    resultado = atk_mod._reducir_dano_recibido(
        pj, Monster("Blanco", max_hp=10, ac=10, abilities=_abilities()),
        AttackRange.MELEE, 7, ctx=None, rng=_ExplotaSiUsaRng(), log=None)
    assert resultado == 7


# --- Riposte (reacción) (A3) ----------------------------------------------------

def _ripostea_directa(trait, agresor, rng, ctx, rango=AttackRange.MELEE):
    """Llama a la reacción de Riposte como el motor tras un fallo."""
    trait.reaccionar_al_fallo(agresor, rango, ctx=ctx, rng=rng, log=None)


def test_riposte_dispara_tras_un_fallo_cuerpo_a_cuerpo(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    pj, trait, agresor, ctx = _atacado_fijo(maneuvers=("Riposte",))
    d20s = iter([1, 15])  # enemigo: 1 natural; reacción: impacta

    def _d20(rng, mode):
        v = next(d20s)
        return D20Result(value=v, rolls=[v], mode=RollMode.NORMAL)

    monkeypatch.setattr(atk_mod, "roll_d20", _d20)
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 1)
    monkeypatch.setattr(bm_mod, "pick", lambda rng, seq: seq[-1])  # «si»
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 6)
    atk_ene = Attack("Garra", "1d6", ability="str")
    atk_mod.attack_roll(agresor, pj, atk_ene, random.Random(1), ctx=ctx)
    # daño de reacción: 1 (dados) + 3 (mod FUE) + 6 (dado Riposte) = 10
    assert agresor.hp == 50
    assert pj.state.reaction_used is True
    assert trait.dados_restantes == 3  # 4 iniciales − 1 de Riposte
    assert trait.maniobra_pendiente is None  # sin maniobras de sesión 1


def test_riposte_no_dispara_tras_un_acierto_enemigo(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    pj, trait, agresor, ctx = _atacado(maneuvers=("Riposte",))

    def _revienta(*args, **kwargs):
        raise AssertionError("Riposte no debe consultarse en un acierto")

    monkeypatch.setattr(bm_mod, "pick", _revienta)
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=15, rolls=[15],
                                    mode=RollMode.NORMAL))
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 1)
    atk_ene = Attack("Garra", "1d6", ability="str")
    atk_mod.attack_roll(agresor, pj, atk_ene, random.Random(1), ctx=ctx)
    assert pj.hp < pj.max_hp  # el enemigo impactó y causó daño
    assert pj.state.reaction_used is False
    assert trait.dados_restantes == 4


def test_riposte_no_dispara_a_distancia():
    _, trait, agresor, ctx = _atacado(maneuvers=("Riposte",))
    _ripostea_directa(trait, agresor, _ExplotaSiUsaRng(), ctx,
                      rango=AttackRange.RANGED)
    assert trait.owner.state.reaction_used is False
    assert trait.dados_restantes == 4


def test_riposte_suma_el_dado_solo_si_el_ataque_de_reaccion_impacta(
        monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    pj, trait, agresor, ctx = _atacado(maneuvers=("Riposte",))
    d20s = iter([1, 5])  # falla el enemigo; la reacción también falla

    def _d20(rng, mode):
        v = next(d20s)
        return D20Result(value=v, rolls=[v], mode=RollMode.NORMAL)

    monkeypatch.setattr(atk_mod, "roll_d20", _d20)
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 1)
    monkeypatch.setattr(bm_mod, "pick", lambda rng, seq: seq[-1])
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 6)
    atk_ene = Attack("Garra", "1d6", ability="str")
    atk_mod.attack_roll(agresor, pj, atk_ene, random.Random(1), ctx=ctx)
    assert agresor.hp == agresor.max_hp  # sin daño: el ataque falló
    assert pj.state.reaction_used is True
    assert trait.dados_restantes == 3  # el dado se gasta aunque falle


def test_el_dado_de_reaccion_no_se_duplica_en_critico(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    pj, trait, agresor, ctx = _atacado_fijo(maneuvers=("Riposte",))
    d20s = iter([1, 20])  # la reacción es crítico

    def _d20(rng, mode):
        v = next(d20s)
        return D20Result(value=v, rolls=[v], mode=RollMode.NORMAL)

    monkeypatch.setattr(atk_mod, "roll_d20", _d20)
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 1)
    monkeypatch.setattr(bm_mod, "pick", lambda rng, seq: seq[-1])
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 6)
    atk_ene = Attack("Garra", "1d6", ability="str")
    atk_mod.attack_roll(agresor, pj, atk_ene, random.Random(1), ctx=ctx)
    # plano: 1 + 3 + 6 = 10 (el dado NO se duplica con el crítico)
    assert agresor.hp == 50


def test_riposte_sin_ataques_cuerpo_a_cuerpo_no_consume_rng():
    pj = _pj(attacks=[])
    apply_fighter(pj, level=5)
    trait = apply_battle_master(pj, level=5,
                                maneuvers=_completa(("Riposte",), 5))
    ctx = SimpleNamespace(round=1, combatants=[pj])
    agresor = Monster("Agresor", max_hp=40, ac=15, abilities=_abilities())
    _ripostea_directa(trait, agresor, _ExplotaSiUsaRng(), ctx)
    assert not pj.state.reaction_used
    assert trait.dados_restantes == 4


def test_riposte_solo_una_vez_por_ronda(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    pj, trait, agresor, ctx = _atacado(maneuvers=("Riposte",))
    d20s = iter([1, 15])

    def _d20(rng, mode):
        v = next(d20s)
        return D20Result(value=v, rolls=[v], mode=RollMode.NORMAL)

    monkeypatch.setattr(atk_mod, "roll_d20", _d20)
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 1)
    monkeypatch.setattr(bm_mod, "pick", lambda rng, seq: seq[-1])
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 6)
    atk_ene = Attack("Garra", "1d6", ability="str")
    atk_mod.attack_roll(agresor, pj, atk_ene, random.Random(1), ctx=ctx)
    assert trait.dados_restantes == 3  # primer fallo: gastado
    _ripostea_directa(trait, agresor, _ExplotaSiUsaRng(), ctx)
    assert trait.dados_restantes == 3  # la reacción ya estaba usada
    assert pj.state.reaction_used is True


def test_riposte_sin_datos_no_consume_rng():
    pj, trait, agresor, ctx = _atacado(maneuvers=("Riposte",))
    trait.dados_restantes = 0
    _ripostea_directa(trait, agresor, _ExplotaSiUsaRng(), ctx)
    assert not pj.state.reaction_used


def test_riposte_sin_reaccion_libre_no_consume_rng():
    pj, trait, agresor, ctx = _atacado(maneuvers=("Riposte",))
    pj.state.reaction_used = True
    _ripostea_directa(trait, agresor, _ExplotaSiUsaRng(), ctx)
    assert trait.dados_restantes == 4


def test_riposte_al_atacante_muerto_no_responde():
    pj, trait, agresor, ctx = _atacado(maneuvers=("Riposte",))
    agresor.hp = 0
    agresor.dead = True
    _ripostea_directa(trait, agresor, _ExplotaSiUsaRng(), ctx)
    assert not pj.state.reaction_used
    assert trait.dados_restantes == 4


def test_el_ataque_de_reaccion_no_activa_maniobras_de_sesion_1():
    _, trait, objetivo, ctx = _atacado(maneuvers=("Trip Attack",))
    r_ctx = SimpleNamespace(round=1, combatants=[ctx.combatants],
                             is_reaction=True)
    hit, total = _decide(trait, objetivo, r_ctx, _ExplotaSiUsaRng())
    assert (hit, total) == (True, 15)
    assert trait.maniobra_pendiente is None


def test_sin_subclase_el_motor_no_consulta_la_reaccion_de_fallo():
    from dnd_sim.engine.combat import attack as atk_mod

    pj = _pj()
    apply_fighter(pj, level=5)
    atk_mod._reaccionar_al_fallo(
        pj, Monster("Blanco", max_hp=10, ac=10, abilities=_abilities()),
        AttackRange.MELEE, ctx=None, rng=_ExplotaSiUsaRng(), log=None)
    assert not pj.state.reaction_used


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


# --- Marcas: Distracting / Goading / Feinting (A5) -----------------------------

def _mods() -> SimpleNamespace:
    return SimpleNamespace(advantage_sources=[], disadvantage_sources=[])


def test_distracting_da_ventaja_a_un_tercero_y_se_consume():
    from dnd_sim.rules.mastery import consumir_marcas

    pj, trait, objetivo, ctx = _atacado(
        maneuvers=("Distracting Strike",))
    _ejecuta(trait, objetivo, ctx, _RngFalla(), "Distracting Strike")
    assert objetivo.state.distracting == {trait.owner.name: 2}  # ronda 1 + 1
    tercero = Monster("Tercero", max_hp=40, ac=12, abilities=_abilities())
    mods = _mods()
    consumir_marcas(mods, tercero, objetivo, ctx)
    assert "Distracting Strike" in mods.advantage_sources
    assert objetivo.state.distracting == {}  # consumida al concederse


def test_distracting_no_da_ventaja_al_marcador_ni_se_consume():
    from dnd_sim.rules.mastery import consumir_marcas

    pj, trait, objetivo, ctx = _atacado(
        maneuvers=("Distracting Strike",))
    _ejecuta(trait, objetivo, ctx, _RngFalla(), "Distracting Strike")
    mods = _mods()
    consumir_marcas(mods, pj, objetivo, ctx)
    assert mods.advantage_sources == []
    assert objetivo.state.distracting == {trait.owner.name: 2}  # intacta


def test_distracting_no_concede_ventaja_si_ya_caduco():
    from dnd_sim.rules.mastery import consumir_marcas

    pj, trait, objetivo, _ = _atacado(maneuvers=("Distracting Strike",))
    objetivo.state.distracting[trait.owner.name] = 2
    ctx = SimpleNamespace(round=2, combatants=[pj, objetivo])
    tercero = Monster("Tercero", max_hp=40, ac=12, abilities=_abilities())
    mods = _mods()
    consumir_marcas(mods, tercero, objetivo, ctx)
    assert mods.advantage_sources == []
    assert objetivo.state.distracting == {}


def test_goading_no_se_consume_y_no_aplica_al_atacar_al_marcador():
    from dnd_sim.rules.mastery import consumir_marcas

    pj, trait, objetivo, ctx = _atacado(maneuvers=("Goading Attack",))
    _ejecuta(trait, objetivo, ctx, _RngFalla(), "Goading Attack")
    assert objetivo.state.goading == {trait.owner.name: 3}
    otro = Monster("Otro", max_hp=40, ac=12, abilities=_abilities())
    mods = _mods()
    consumir_marcas(mods, objetivo, otro, ctx)
    assert "Goading Attack" in mods.disadvantage_sources
    assert objetivo.state.goading == {trait.owner.name: 3}  # NO consumida
    # Contra su propio marcador: sin desventaja y la marca sigue.
    mods2 = _mods()
    consumir_marcas(mods2, objetivo, pj, ctx)
    assert "Goading Attack" not in mods2.disadvantage_sources
    assert objetivo.state.goading == {trait.owner.name: 3}


def test_goading_caduca_en_la_ronda_indicada():
    from dnd_sim.rules.mastery import consumir_marcas

    pj, trait, objetivo, _ = _atacado(maneuvers=("Goading Attack",))
    objetivo.state.goading[trait.owner.name] = 3
    ctx = SimpleNamespace(round=3, combatants=[pj, objetivo])
    otro = Monster("Otro", max_hp=40, ac=12, abilities=_abilities())
    mods = _mods()
    consumir_marcas(mods, objetivo, otro, ctx)
    assert mods.disadvantage_sources == []
    assert objetivo.state.goading == {}


def test_reset_de_combate_limpia_las_marcas_de_battle_master():
    _, trait, _, _ = _atacado(maneuvers=("Goading Attack",))
    pj = trait.owner
    pj.state.distracting["Marcador"] = 5
    pj.state.goading["Marcador"] = 7
    pj.reset()
    assert pj.state.distracting == {}
    assert pj.state.goading == {}


# --- Feinting Attack (acción bonus) --------------------------------------------

def _accion_feinting(pj):
    from dnd_sim.rules.classes.fighter.subclasses.battle_master import (
        FeintingAttackAction,
    )

    for accion in pj.actions:
        if isinstance(accion, FeintingAttackAction):
            return accion
    raise AssertionError("falta FeintingAttackAction")


def test_feinting_es_elegible_con_bonus_libre_y_decision_aleatoria():
    from dnd_sim.model.actions import TurnResources

    pj, trait, objetivo, _ = _atacado(maneuvers=("Goading Attack",))
    accion = _accion_feinting(pj)
    ctx = SimpleNamespace(actor=pj, rng=_RngSi(),
                          combatants=[pj, objetivo])
    assert accion.can_use(TurnResources(), ctx) is True
    ctx_no = SimpleNamespace(actor=pj, rng=_RngNo(),
                             combatants=[pj, objetivo])
    assert accion.can_use(TurnResources(), ctx_no) is False


def test_feinting_sin_datos_es_inelegible_sin_rng():
    from dnd_sim.model.actions import TurnResources

    pj, trait, objetivo, _ = _atacado(maneuvers=("Goading Attack",))
    accion = _accion_feinting(pj)
    trait.dados_restantes = 0
    ctx = SimpleNamespace(actor=pj, rng=_ExplotaSiUsaRng(),
                          combatants=[pj, objetivo])
    assert accion.can_use(TurnResources(), ctx) is False


def test_feinting_encola_la_ventaja_y_el_dado_si_impacta():
    from dnd_sim.model.actions import TurnResources

    pj, trait, objetivo, ctx = _atacado(maneuvers=("Goading Attack",))
    accion = _accion_feinting(pj)
    ctx_ejec = SimpleNamespace(actor=pj, rng=_RngSi(),
                               combatants=[pj, objetivo], round=1)
    accion.execute(ctx_ejec)
    assert trait.feinting_pendiente is True
    # La ventaja se ve en la tirada...
    mods = _mods()
    trait.modify_attack_modifiers(mods, pj, objetivo, AttackRange.MELEE,
                                  ctx=ctx, rng=_RngSi())
    assert mods.advantage_sources == ["Feinting Attack"]
    # ...y la decisión de este ataque consume la ranura SIN RNG, aunque
    # haya otras maniobras conocidas (una por ataque).
    hit, total = _decide(trait, objetivo, ctx, _ExplotaSiUsaRng())
    assert trait.feinting_pendiente is False
    assert trait.maniobra_pendiente == "Feinting Attack"
    assert (hit, total) == (True, 15)
    # La ventaja NO se concede al siguiente ataque.
    mods2 = _mods()
    trait.modify_attack_modifiers(mods2, pj, objetivo, AttackRange.MELEE,
                                  ctx=ctx, rng=_ExplotaSiUsaRng())
    assert mods2.advantage_sources == []
    # El dado se gasta al impactar.
    daño = trait.extra_attack_damage(
        pj, objetivo, AttackRange.MELEE, ctx=ctx, rng=random.Random(1),
        atk=Attack("Espada larga", "1d8", ability="str"))
    assert daño > 0
    assert trait.dados_restantes == 3
    assert trait.maniobra_pendiente is None


def test_feinting_sin_impacto_no_gasta_el_dado():
    pj, trait, objetivo, ctx = _atacado(maneuvers=("Goading Attack",))
    trait.feinting_pendiente = True
    hit, _ = _decide(trait, objetivo, ctx, _ExplotaSiUsaRng(), hit=False)
    assert hit is False
    assert trait.feinting_pendiente is False
    assert trait.maniobra_pendiente is None
    assert trait.dados_restantes == 4


# --- Precision y Sweeping (A6) ------------------------------------------------

def test_precision_convierte_un_fallo_en_impacto(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod

    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 3)
    _, trait, objetivo, ctx = _atacado(
        maneuvers=("Precision Attack", "Feinting Attack", "Menacing Attack"))
    hit, total = _decide(trait, objetivo, ctx, _RngIdx(1, 0),
                         hit=False, total=10, ca=12)
    assert hit is True
    assert total == 13  # 10 + 3 del dado de superioridad
    assert trait.dados_restantes == 3  # Precision gasta su dado
    assert trait.maniobra_pendiente is None  # y no añade daño


def test_precision_no_actua_si_el_dado_maximo_no_alcanza_la_ca():
    _, trait, objetivo, ctx = _atacado(
        maneuvers=("Precision Attack", "Feinting Attack", "Menacing Attack"))
    hit, total = _decide(trait, objetivo, ctx, _ExplotaSiUsaRng(),
                         hit=False, total=1, ca=20)  # 1 + d8 máximo = 9
    assert (hit, total) == (False, 1)
    assert trait.dados_restantes == 4
    assert trait.maniobra_pendiente is None


def test_precision_no_actua_en_un_1_natural():
    _, trait, objetivo, ctx = _atacado(
        maneuvers=("Precision Attack", "Feinting Attack", "Menacing Attack"))
    hit, total = _decide(trait, objetivo, ctx, _ExplotaSiUsaRng(),
                         hit=False, total=10, ca=12, roll=1)
    assert (hit, total) == (False, 10)
    assert trait.dados_restantes == 4


def test_precision_con_relevelless_no_gasta_el_dado():
    _, trait, objetivo, ctx = _atacado(
        level=15,
        maneuvers=("Precision Attack", "Feinting Attack", "Menacing Attack"))
    hit, total = _decide(trait, objetivo, ctx, _RngSi(),
                         hit=False, total=10, ca=12)
    assert hit is True
    assert total >= 18  # 10 + 1d8 (Relentless)
    assert trait.dados_restantes == 6  # sin gastar el dado
    assert trait.relentless_used_this_turn is True


def test_precision_actua_en_el_motor_tras_un_fallo(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    # sin Precision: 9+3=12 < CA 14 → falla; con Precision: +5 → 17 ≥ 14.
    monkeypatch.setattr(bm_mod, "pick", lambda rng, seq: seq[-1])
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 5)
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=9, rolls=[9],
                                    mode=RollMode.NORMAL))
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 1)
    pj, trait, objetivo, _ = _atacado(
        maneuvers=("Precision Attack", "Feinting Attack", "Menacing Attack"))
    objetivo.ac = 14
    ctx = SimpleNamespace(round=1, combatants=[pj, objetivo])
    atk = Attack("Espada larga", "1d8", ability="str")
    atk_mod.attack_roll(pj, objetivo, atk, random.Random(1), ctx=ctx)
    assert trait.dados_restantes == 3
    assert objetivo.hp < objetivo.max_hp  # el fallo se convirtió en impacto


def _atacado_dos_enemigos(**kwargs) -> tuple:
    """PJ Battle Master con DOS enemigos (para Sweeping)."""
    if "maneuvers" in kwargs:
        kwargs["maneuvers"] = _completa(kwargs["maneuvers"], 5)
    pj, trait = _bm(**kwargs)
    objetivo = Monster("Muñeco", max_hp=60, ac=15, abilities=_abilities())
    segunda = Monster("Segunda", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(round=1, combatants=[pj, objetivo, segunda])
    return pj, trait, objetivo, segunda, ctx


def _conoce_sweeping() -> tuple:
    return _atacado_dos_enemigos(
        maneuvers=("Sweeping Attack", "Feinting Attack", "Precision Attack"))


def test_sweeping_dana_al_segundo_si_la_tirada_cubre_su_ca():
    _, trait, objetivo, segunda, ctx = _conoce_sweeping()
    hit, _ = _decide(trait, objetivo, ctx, _RngIdx(1, 0), total=20)
    assert hit is True
    assert trait.maniobra_pendiente == "Sweeping Attack"
    assert trait.maniobra_total == 20
    hp_primera = objetivo.hp
    daño = trait.extra_attack_damage(
        trait.owner, objetivo, AttackRange.MELEE, ctx=ctx, rng=_RngFalla(),
        atk=Attack("Espada larga", "1d8", ability="str"))
    assert daño == 0  # el dado NO se suma al golpe propio
    assert objetivo.hp == hp_primera
    assert segunda.hp < segunda.max_hp  # pero SÍ al segundo objetivo
    assert trait.dados_restantes == 3  # un solo gasto


def test_sweeping_no_dana_si_la_tirada_no_cubre_la_ca_del_segundo():
    _, trait, objetivo, segunda, ctx = _conoce_sweeping()
    hit, _ = _decide(trait, objetivo, ctx, _RngIdx(1, 0), total=5)
    assert hit is True
    daño = trait.extra_attack_damage(
        trait.owner, objetivo, AttackRange.MELEE, ctx=ctx, rng=_RngFalla(),
        atk=Attack("Espada larga", "1d8", ability="str"))
    assert daño == 0
    assert segunda.hp == segunda.max_hp
    assert trait.dados_restantes == 3  # el dado se gasta aunque falle la CA


def test_sweeping_no_es_elegible_sin_segundo_enemigo():
    _, trait, objetivo, ctx = _atacado(
        maneuvers=("Sweeping Attack", "Feinting Attack", "Precision Attack"))
    hit, _ = _decide(trait, objetivo, ctx, _ExplotaSiUsaRng(), hit=True)
    assert hit is True
    assert trait.maniobra_pendiente is None  # sin elegibles: cero RNG


def test_sweeping_no_es_elegible_a_distancia():
    _, trait, objetivo, _, ctx = _conoce_sweeping()
    hit, _ = _decide(trait, objetivo, ctx, _ExplotaSiUsaRng(),
                     hit=True, rango=AttackRange.RANGED)
    assert hit is True
    assert trait.maniobra_pendiente is None  # solo cuerpo a cuerpo: cero RNG


# --- Commander's Strike (reacción, sesión 2 A4) --------------------------------

def _commanda(level: int = 5, **kwargs) -> tuple:
    """PJ Battle Master + aliado PJ + enemigo, para Commander's Strike."""
    if "maneuvers" in kwargs:
        kwargs["maneuvers"] = _completa(kwargs["maneuvers"], level)
    pj, trait = _bm(level=level, **kwargs)
    aliado = _pj(name="Alicia")
    enemigo = Monster("Enemigo", max_hp=60, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(round=1, combatants=[pj, aliado, enemigo])
    return pj, trait, aliado, enemigo, ctx


def _sustituye(trait, pj, enemigo, ctx, rng) -> object:
    """Llama al hook como el motor en el paso 2b de ``attack_roll``."""
    atk = Attack("Espada larga", "1d8", ability="str")
    return trait.sustituir_ataque(pj, enemigo, atk, AttackRange.MELEE,
                                  ctx=ctx, rng=rng)


def test_commanders_strike_sustituye_el_ataque_y_el_aliado_gasta_su_reaccion(
        monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod
    from dnd_sim.rules.traits.base import AtaqueSustituido

    pj, trait, aliado, enemigo, ctx = _commanda(
        maneuvers=("Commander's Strike",))
    d20s = []

    def _d20(rng, mode):
        d20s.append(15)
        return D20Result(value=15, rolls=[15], mode=RollMode.NORMAL)

    monkeypatch.setattr(atk_mod, "roll_d20", _d20)
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 1)
    monkeypatch.setattr(bm_mod, "pick", lambda rng, seq: seq[-1])  # «si»
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 6)
    atk = Attack("Espada larga", "1d8", ability="str")
    res = atk_mod.attack_roll(pj, enemigo, atk, random.Random(1), ctx=ctx)
    assert isinstance(res, AtaqueSustituido)
    assert res.motivo == "Commander's Strike"
    assert len(d20s) == 1  # solo el aliado tira d20 (el dueño: 0)
    assert aliado.state.reaction_used is True
    assert pj.state.reaction_used is False  # el dueño solo gasta el dado
    assert trait.dados_restantes == 3  # 4 iniciales − 1
    assert enemigo.hp == 50  # 1 (arma) + 3 (FUE) + 6 (dado) = 10


def test_commanders_strike_no_se_decide_sin_aliados_elegibles():
    pj, trait, aliado, enemigo, ctx = _commanda(
        maneuvers=("Commander's Strike",))
    ctx.combatants = [pj, enemigo]  # el aliado no está en el encuentro
    assert _sustituye(trait, pj, enemigo, ctx, _ExplotaSiUsaRng()) is None
    assert trait.dados_restantes == 4
    assert not aliado.state.reaction_used


def test_commanders_strike_no_se_decide_si_el_aliado_ya_uso_su_reaccion():
    _, trait, aliado, enemigo, ctx = _commanda(
        maneuvers=("Commander's Strike",))
    aliado.state.reaction_used = True
    assert _sustituye(trait, trait.owner, enemigo, ctx,
                      _ExplotaSiUsaRng()) is None
    assert trait.dados_restantes == 4


def test_commanders_strike_no_se_decide_sin_dados():
    pj, trait, _, enemigo, ctx = _commanda(
        maneuvers=("Commander's Strike",))
    trait.dados_restantes = 0
    assert _sustituye(trait, pj, enemigo, ctx, _ExplotaSiUsaRng()) is None
    assert not trait.owner.state.reaction_used


def test_commanders_strike_no_se_decide_sin_la_maniobra_conocida():
    pj, trait, aliado, enemigo, ctx = _commanda(
        maneuvers=("Riposte", "Parry", "Trip Attack"))  # sin CS
    assert "Commander's Strike" not in trait.maneuvers
    assert _sustituye(trait, pj, enemigo, ctx, _ExplotaSiUsaRng()) is None
    assert trait.dados_restantes == 4
    assert not aliado.state.reaction_used


def test_commanders_strike_cede_el_ataque_si_hay_feinting_encolado():
    pj, trait, aliado, enemigo, ctx = _commanda(
        maneuvers=("Commander's Strike",))
    trait.feinting_pendiente = True
    assert _sustituye(trait, pj, enemigo, ctx, _ExplotaSiUsaRng()) is None
    assert trait.feinting_pendiente is True  # una maniobra por ataque
    assert not aliado.state.reaction_used


def test_commanders_strike_no_sustituye_un_ataque_de_reaccion():
    pj, trait, _, enemigo, ctx = _commanda(
        maneuvers=("Commander's Strike",))
    ctx.is_reaction = True
    assert _sustituye(trait, pj, enemigo, ctx, _ExplotaSiUsaRng()) is None
    assert trait.dados_restantes == 4


def test_commanders_strike_no_se_decide_si_el_aliado_no_tiene_armas():
    _, trait, aliado, enemigo, ctx = _commanda(
        maneuvers=("Commander's Strike",))
    aliado.attacks = []
    assert _sustituye(trait, trait.owner, enemigo, ctx,
                      _ExplotaSiUsaRng()) is None
    assert trait.dados_restantes == 4
    assert not aliado.state.reaction_used


def test_commanders_strike_el_dueño_nunca_es_el_aliado_elegido(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    pj, trait = _bm(maneuvers=_completa(("Commander's Strike",), 5))
    a1 = _pj(name="Alicia")
    a2 = _pj(name="Berta")
    enemigo = Monster("Enemigo", max_hp=60, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(round=1, combatants=[pj, a1, a2, enemigo])
    registradas = []

    def _spy(rng, seq):
        registradas.append(tuple(seq))
        return seq[-1]

    monkeypatch.setattr(bm_mod, "pick", _spy)
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=15, rolls=[15],
                                    mode=RollMode.NORMAL))
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 1)
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 6)
    atk = Attack("Espada larga", "1d8", ability="str")
    res = atk_mod.attack_roll(pj, enemigo, atk, random.Random(1), ctx=ctx)
    assert res is not None  # la sustitución se produjo
    assert any(any(x is a1 for x in s) for s in registradas)
    assert any(any(x is a2 for x in s) for s in registradas)
    assert all(not any(x is pj for x in s) for s in registradas)


def test_sin_subclase_el_motor_no_consulta_sustituir_ataque():
    from dnd_sim.engine.combat import attack as atk_mod

    pj = _pj()
    apply_fighter(pj, level=5)
    aliado = _pj(name="Alicia")
    enemigo = Monster("Blanco", max_hp=10, ac=10, abilities=_abilities())
    ctx = SimpleNamespace(round=1, combatants=[pj, aliado, enemigo])
    atk = Attack("Espada larga", "1d8", ability="str")
    res = atk_mod._sustituir_ataque(pj, enemigo, atk, AttackRange.MELEE,
                                    ctx, _ExplotaSiUsaRng())
    assert res is None  # sin subclase: cero RNG aunque haya aliado


def test_el_ataque_del_aliado_no_reentra_en_commanders_strike(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod
    from dnd_sim.rules.conditions import Condition
    from dnd_sim.rules.traits.base import AtaqueSustituido

    pj, trait = _bm(maneuvers=_completa(("Commander's Strike",), 5))
    aliado, aliado_trait = _bm(
        maneuvers=_completa(("Menacing Attack",), 5))  # con CS: reentrada
    aliado.name = "Alicia"
    enemigo = Monster("Enemigo", max_hp=60, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(round=1, combatants=[pj, aliado, enemigo])
    monkeypatch.setattr(bm_mod, "pick", lambda rng, seq: seq[-1])  # «si»
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=15, rolls=[15],
                                    mode=RollMode.NORMAL))
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 1)
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 6)
    atk = Attack("Espada larga", "1d8", ability="str")
    res = atk_mod.attack_roll(pj, enemigo, atk, random.Random(1), ctx=ctx)
    assert isinstance(res, AtaqueSustituido)  # el aliado atacó en su sitio
    assert aliado.state.reaction_used is True
    assert aliado_trait.maniobra_pendiente is None  # guard is_reaction
    assert not _tiene(enemigo, Condition.FRIGHTENED)  # ni Menacing ni recursión
    assert aliado_trait.dados_restantes == 4  # el aliado no gastó su dado
    assert trait.dados_restantes == 3  # un solo dado: el del dueño


def test_commanders_strike_con_relentless_no_gasta_dado(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod
    from dnd_sim.rules.traits.base import AtaqueSustituido

    pj, trait, aliado, enemigo, ctx = _commanda(
        level=15, maneuvers=("Commander's Strike",))
    monkeypatch.setattr(bm_mod, "pick", lambda rng, seq: seq[-1])  # «si»
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=15, rolls=[15],
                                    mode=RollMode.NORMAL))
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 1)
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 6)  # d8 Relentless
    atk = Attack("Espada larga", "1d8", ability="str")
    res = atk_mod.attack_roll(pj, enemigo, atk, random.Random(1), ctx=ctx)
    assert isinstance(res, AtaqueSustituido)
    assert trait.dados_restantes == 6  # Relentless: sin gastar
    assert aliado.state.reaction_used is True
    assert enemigo.hp == 50  # 1 + 3 + 6 (d8 de Relentless)


# --- Rally (acción bonus, sesión 2 B1) ----------------------------------------

def _accion_rally(pj):
    from dnd_sim.rules.classes.fighter.subclasses.battle_master import (
        BattleMasterRallyAction,
    )

    for accion in pj.actions:
        if isinstance(accion, BattleMasterRallyAction):
            return accion
    raise AssertionError("falta BattleMasterRallyAction")


def test_rally_es_elegible_con_bonus_libre_y_decision_aleatoria():
    from dnd_sim.model.actions import TurnResources

    pj, trait, aliado, _, ctx = _commanda(maneuvers=("Rally",))
    accion = _accion_rally(pj)
    ctx_si = SimpleNamespace(actor=pj, rng=_RngSi(),
                             combatants=ctx.combatants)
    assert accion.can_use(TurnResources(), ctx_si) is True
    ctx_no = SimpleNamespace(actor=pj, rng=_RngNo(),
                             combatants=ctx.combatants)
    assert accion.can_use(TurnResources(), ctx_no) is False


def test_rally_sin_la_maniobra_conocida_es_inelegible_sin_rng():
    from dnd_sim.model.actions import TurnResources

    pj, trait, aliado, _, _ = _commanda(maneuvers=("Parry",))
    accion = _accion_rally(pj)
    ctx = SimpleNamespace(actor=pj, rng=_ExplotaSiUsaRng(),
                          combatants=[pj, aliado])
    assert accion.can_use(TurnResources(), ctx) is False


def test_rally_sin_datos_es_inelegible_sin_rng():
    from dnd_sim.model.actions import TurnResources

    pj, trait, aliado, _, _ = _commanda(maneuvers=("Rally",))
    accion = _accion_rally(pj)
    trait.dados_restantes = 0
    ctx = SimpleNamespace(actor=pj, rng=_ExplotaSiUsaRng(),
                          combatants=[pj, aliado])
    assert accion.can_use(TurnResources(), ctx) is False


def test_rally_sin_aliados_es_inelegible_sin_rng():
    from dnd_sim.model.actions import TurnResources

    pj, trait, _, enemigo, _ = _commanda(maneuvers=("Rally",))
    accion = _accion_rally(pj)
    ctx = SimpleNamespace(actor=pj, rng=_ExplotaSiUsaRng(),
                          combatants=[pj, enemigo])
    assert accion.can_use(TurnResources(), ctx) is False


def test_rally_gasta_un_dado_y_concede_pv_temporales_sin_reaccion(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod

    pj, trait, aliado, _, _ = _commanda(maneuvers=("Rally",))
    pj.abilities.cha = 16  # mod CAR +3
    accion = _accion_rally(pj)
    ctx = SimpleNamespace(actor=pj, rng=random.Random(1), round=1,
                          combatants=[pj, aliado])
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 6)
    accion.execute(ctx)
    assert aliado.temp_hp == 9  # 6 (dado) + 3 (CAR)
    assert trait.dados_restantes == 3  # un dado gastado
    assert aliado.state.reaction_used is False  # Rally sin reacción
    assert pj.state.reaction_used is False


def test_rally_concede_al_menos_un_pv_temporal(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod

    pj, trait, aliado, _, _ = _commanda(maneuvers=("Rally",))
    pj.abilities.cha = 8  # mod CAR -1: 1 - 1 = 0 → mínimo 1
    accion = _accion_rally(pj)
    ctx = SimpleNamespace(actor=pj, rng=random.Random(1), round=1,
                          combatants=[pj, aliado])
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 1)
    accion.execute(ctx)
    assert aliado.temp_hp == 1


def test_los_pv_temporales_de_rally_no_se_acumulan(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod

    pj, trait, aliado, _, _ = _commanda(maneuvers=("Rally",))
    accion = _accion_rally(pj)
    ctx = SimpleNamespace(actor=pj, rng=random.Random(1), round=1,
                          combatants=[pj, aliado])
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 6)
    aliado.temp_hp = 20  # más que la concesión: se queda el mayor
    accion.execute(ctx)
    assert aliado.temp_hp == 20
    aliado.temp_hp = 2  # menos: sube al mayor, no suma 2+6
    accion.execute(ctx)
    assert aliado.temp_hp == 6


def test_rally_elige_un_aliado_distinto_del_dueno(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod

    pj, trait = _bm(maneuvers=_completa(("Rally",), 5))
    a1 = _pj(name="Alicia")
    a2 = _pj(name="Beatriz")
    enemigo = Monster("Enemigo", max_hp=60, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(actor=pj, rng=random.Random(1), round=1,
                          combatants=[pj, a1, a2, enemigo])
    registradas = []
    original = bm_mod.pick

    def _spy(rng, seq):
        registradas.append(tuple(seq))
        return original(rng, seq)

    monkeypatch.setattr(bm_mod, "pick", _spy)
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 6)
    accion = _accion_rally(pj)
    accion.execute(ctx)
    assert all(not any(x is pj for x in s) for s in registradas)
    assert a1.temp_hp + a2.temp_hp == 6  # solo uno la recibe


def test_rally_execute_sin_datos_no_concede_pv():
    pj, trait, aliado, _, _ = _commanda(maneuvers=("Rally",))
    accion = _accion_rally(pj)
    trait.dados_restantes = 0
    ctx = SimpleNamespace(actor=pj, rng=_ExplotaSiUsaRng(), round=1,
                          combatants=[pj, aliado])
    accion.execute(ctx)
    assert aliado.temp_hp == 0


def test_rally_con_relentless_no_gasta_dado(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod

    pj, trait, aliado, _, _ = _commanda(level=15, maneuvers=("Rally",))
    accion = _accion_rally(pj)
    ctx = SimpleNamespace(actor=pj, rng=_RngSi(), round=1,
                          combatants=[pj, aliado])
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 8)
    accion.execute(ctx)
    assert trait.dados_restantes == 6  # Relentless: sin gastar
    assert trait.relentless_used_this_turn is True
    assert aliado.temp_hp == 8  # 1d8 Relentless, CAR 0


def test_sin_subclase_no_se_registra_la_accion_rally():
    from dnd_sim.rules.classes.fighter.subclasses.battle_master import (
        BattleMasterRallyAction,
    )

    pj = _pj()
    apply_fighter(pj, level=5)
    assert not any(isinstance(a, BattleMasterRallyAction)
                   for a in pj.actions)


# --- Ambush (iniciativa, sesión 2 B3) ------------------------------------------

def _d20_fijo(monkeypatch, valor: int = 10) -> None:
    """d20 del motor siempre ``valor``: el RNG del rasgo se aísla."""
    import dnd_sim.engine.combat.encounter as enc_mod

    monkeypatch.setattr(enc_mod, "d20", lambda rng: valor)


def test_ambush_suma_un_dado_a_la_tirada_de_iniciativa(monkeypatch):
    import dnd_sim.engine.combat.encounter as enc_mod
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.engine.combat.encounter import roll_initiative

    pj, trait, enemigo, _ = _atacado(maneuvers=("Ambush",))
    _d20_fijo(monkeypatch)
    monkeypatch.setattr(bm_mod, "pick", lambda rng, seq: "si")
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 6)
    orden = roll_initiative([pj, enemigo], random.Random(1))
    # 10 (d20 parcheado) + 6 (dado) + 2 (DES 14) = 18; el enemigo: 12.
    assert pj.initiative == 18
    assert trait.dados_restantes == 3  # un dado gastado
    assert orden[0] is pj


def test_ambush_sin_la_maniobra_no_consume_rng(monkeypatch):
    from dnd_sim.engine.combat.encounter import roll_initiative

    pj, trait, enemigo, _ = _atacado(
        maneuvers=("Parry", "Riposte", "Trip Attack"))  # sin Ambush
    _d20_fijo(monkeypatch)
    roll_initiative([pj, enemigo], _ExplotaSiUsaRng())
    assert pj.initiative == 12  # 10 + DES: sin dado y sin RNG
    assert trait.dados_restantes == 4


def test_ambush_sin_dados_no_consume_rng(monkeypatch):
    from dnd_sim.engine.combat.encounter import roll_initiative

    pj, trait, enemigo, _ = _atacado(maneuvers=("Ambush",))
    trait.dados_restantes = 0
    _d20_fijo(monkeypatch)
    roll_initiative([pj, enemigo], _ExplotaSiUsaRng())
    assert pj.initiative == 12  # guard antes de todo RNG
    assert trait.dados_restantes == 0


def test_ambush_con_la_decision_no_no_gasta_nada(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.engine.combat.encounter import roll_initiative

    pj, trait, enemigo, _ = _atacado(maneuvers=("Ambush",))
    _d20_fijo(monkeypatch)
    monkeypatch.setattr(bm_mod, "pick", lambda rng, seq: "no")
    roll_initiative([pj, enemigo], random.Random(1))
    assert pj.initiative == 12  # sin el dado: solo el d20 y el DES
    assert trait.dados_restantes == 4  # «no» no gasta nada


def test_sin_subclase_roll_initiative_no_consulta_bonus(monkeypatch):
    from dnd_sim.engine.combat.encounter import roll_initiative

    pj = _pj()
    apply_fighter(pj, level=5)
    enemigo = Monster("Muñeco", max_hp=60, ac=15, abilities=_abilities())
    _d20_fijo(monkeypatch)
    roll_initiative([pj, enemigo], _ExplotaSiUsaRng())
    assert pj.initiative == 12  # nadie con bonus_iniciativa: cero RNG


def test_ambush_con_relentless_no_gasta_dado(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.battle_master as bm_mod
    from dnd_sim.engine.combat.encounter import roll_initiative

    pj, trait, enemigo, _ = _atacado(level=15, maneuvers=("Ambush",))
    _d20_fijo(monkeypatch)
    monkeypatch.setattr(bm_mod, "pick", lambda rng, seq: "si")
    monkeypatch.setattr(bm_mod, "roll_dice", lambda *a, **k: 8)
    roll_initiative([pj, enemigo], random.Random(1))
    assert pj.initiative == 20  # 10 + 8 (Relentless) + 2 (DES)
    assert trait.dados_restantes == 6  # sin gastar

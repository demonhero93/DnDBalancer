"""Subclase Arcane Archer (Arquero Arcano, XGE): registro, Lore y tablas."""
from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from dnd_sim import Abilities, Attack, Monster, PlayerCharacter, apply_class
from dnd_sim.core.classes import arcane_shot_options_known, arcane_shot_uses
from dnd_sim.core.enums import AttackRange
from dnd_sim.core.proficiency import proficiency_bonus
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import (
    ARCANE_SHOTS,
    ArcaneArcherFeatures,
    apply_arcane_archer,
)
from dnd_sim.rules.conditions import Condition


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=10, wis=12, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Legolas", max_hp=70, ac=15, level=5, abilities=_abilities(),
        attacks=[Attack("Arco corto", "1d6", ability="dex", range_type="ranged")],
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


def _trait(pj) -> ArcaneArcherFeatures:
    for trait in pj.traits:
        if isinstance(trait, ArcaneArcherFeatures):
            return trait
    raise AssertionError("falta ArcaneArcherFeatures")


# --- Registro y equivalencia --------------------------------------------------

def test_registro_arcane_archer_bajo_fighter():
    subclases = CLASSES["fighter"].subclasses
    assert set(subclases) == {"arcane_archer"}
    sub = subclases["arcane_archer"]
    assert sub.class_name == "fighter"
    assert sub.min_level == 3


def test_apply_class_equivalente_a_apply_arcane_archer(monkeypatch):
    """Misma semilla en los dos RNG de creación: resultados idénticos."""
    import dnd_sim.rules.classes.fighter.features as fighter_mod
    import dnd_sim.rules.classes.fighter.subclasses.arcane_archer as aa_mod

    a = _pj()
    b = _pj()
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    monkeypatch.setattr(aa_mod, "_RNG_CREACION", random.Random(0))
    apply_class(a, "fighter", "arcane_archer", level=5)
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    monkeypatch.setattr(aa_mod, "_RNG_CREACION", random.Random(0))
    apply_fighter(b)
    apply_arcane_archer(b, level=5)
    assert _firmas(a) == _firmas(b)
    assert _trait(a).opciones_conocidas == _trait(b).opciones_conocidas


def test_apply_arcane_archer_exige_la_clase_fighter():
    with pytest.raises(ValueError, match="Primero aplica la clase guerrero"):
        apply_arcane_archer(_pj())


def test_arcane_archer_requiere_nivel_3():
    with pytest.raises(ValueError, match=">= 3"):
        apply_class(_pj(level=2), "fighter", "arcane_archer")


# --- Tablas -------------------------------------------------------------------

def test_tabla_de_opciones_conocidas_por_nivel():
    esperado = {1: 0, 2: 0, 3: 2, 6: 2, 7: 3, 9: 3, 10: 4, 14: 4,
                15: 5, 17: 5, 18: 6, 20: 6}
    assert {lvl: arcane_shot_options_known(lvl) for lvl in esperado} == esperado


def test_tabla_de_usos_de_arcane_shot_por_nivel():
    esperado = {1: 0, 2: 0, 3: 2, 14: 2, 15: 3, 20: 3}
    assert {lvl: arcane_shot_uses(lvl) for lvl in esperado} == esperado


# --- Opciones conocidas -------------------------------------------------------

def test_opciones_conocidas_segun_nivel():
    casos = {3: 2, 10: 4, 18: 6}
    for nivel, cuenta in casos.items():
        pj = _pj(level=nivel)
        apply_fighter(pj, level=nivel)
        trait = apply_arcane_archer(pj, level=nivel)
        assert len(trait.opciones_conocidas) == cuenta
        assert len(set(trait.opciones_conocidas)) == cuenta
        assert set(trait.opciones_conocidas) <= set(ARCANE_SHOTS)


def test_kwarg_de_opciones_explicitas_valido():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    elegidas = ("Grasping Arrow", "Shadow Arrow")
    trait = apply_arcane_archer(pj, level=3, arcane_shots=elegidas)
    assert trait.opciones_conocidas == list(elegidas)


def test_kwarg_de_opciones_invalidas_da_value_error():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    with pytest.raises(ValueError, match="no es una opción de Arcane Shot"):
        apply_arcane_archer(pj, level=3,
                            arcane_shots=("Piercing Arrow", "Grasping Arrow"))


def test_kwarg_con_recuento_equivocado_da_value_error():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    with pytest.raises(ValueError, match="se esperaban 2 opciones"):
        apply_arcane_archer(pj, level=3, arcane_shots=("Grasping Arrow",))


# --- Arcane Archer Lore -------------------------------------------------------

def test_arcane_archer_lore_da_competencia():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    trait = apply_arcane_archer(pj, level=3)
    assert trait.competencia in ("arcana", "nature")
    assert trait.competencia in pj.skill_proficiencies


def test_arcane_archer_lore_guarda_el_truco_como_dato():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    trait = apply_arcane_archer(pj, level=3)
    assert trait.truco in ("Prestidigitación", "Druidismo")


# --- Arcane Shot: usos y decisión ---------------------------------------------

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


class _RngExplota:
    """Cualquier acceso a RNG hace fallar el test."""

    def __getattr__(self, name: str):
        raise AssertionError(f"RNG no debería usarse: {name}")


class _RngFalla:
    """«si» a la decisión, última opción conocida y d20 siempre 1."""

    def randrange(self, n: int) -> int:
        return n - 1

    def random(self) -> float:
        return 1.0

    def randint(self, a: int, b: int) -> int:
        return a


def _arquero(level: int = 5, **kwargs):
    pj = _pj(level=level)
    apply_fighter(pj, level=level)
    trait = apply_arcane_archer(pj, level=level, **kwargs)
    return pj, trait


def _disparo(trait, rng, rango=AttackRange.RANGED, target=None, ctx=None):
    if target is None:
        # Las opciones tiran salvaciones: hace falta un combatiente real.
        target = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    return trait.extra_attack_damage(
        trait.owner, target, rango, ctx=ctx, rng=rng,
        atk=Attack("Arco corto", "1d6", ability="dex", range_type="ranged"),
    )


def test_arcane_shot_crea_usos_por_nivel():
    assert _arquero(level=3)[1].arcane_shot_usage.uses_max == 2
    assert _arquero(level=15)[1].arcane_shot_usage.uses_max == 3


def test_arcane_shot_se_gasta_un_uso_al_aplicar():
    _, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                               "Shadow Arrow"))
    daño = _disparo(trait, _RngSi())
    assert daño > 0
    assert trait.arcane_shot_usage.uses_left == 1
    assert trait.shot_used_this_turn is True


def test_arcane_shot_se_aplica_una_sola_vez_por_turno():
    _, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                               "Shadow Arrow"))
    assert _disparo(trait, _RngSi()) > 0
    assert _disparo(trait, _RngSi()) == 0  # ya usado este turno
    assert trait.arcane_shot_usage.uses_left == 1  # solo un gasto


def test_arcane_shot_se_reinicia_en_on_turn_start():
    _, trait = _arquero(level=3)
    trait.shot_used_this_turn = True
    trait.on_turn_start(trait.owner)
    assert trait.shot_used_this_turn is False


def test_arcane_shot_sin_usos_cero_rng():
    _, trait = _arquero(level=3)
    trait.arcane_shot_usage.uses_left = 0
    assert _disparo(trait, _RngExplota()) == 0


def test_ataque_cuerpo_a_cuerpo_cero_rng():
    _, trait = _arquero(level=3)
    assert _disparo(trait, _RngExplota(), rango=AttackRange.MELEE) == 0


def test_arcane_shot_sin_rng_no_actua():
    _, trait = _arquero(level=3)
    assert _disparo(trait, None) == 0


def test_decision_no_no_gasta_uso():
    _, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                               "Shadow Arrow"))
    assert _disparo(trait, _RngNo()) == 0
    assert trait.arcane_shot_usage.uses_left == 2
    assert trait.shot_used_this_turn is False


def test_daño_de_arcane_shot_es_2d6_antes_del_18(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.arcane_archer as aa_mod

    vistas: list[str] = []

    def _dado(expr, rng, *args, **kwargs):
        vistas.append(expr)
        return 12

    monkeypatch.setattr(aa_mod, "roll_dice", _dado)
    _, trait = _arquero(level=5, arcane_shots=("Grasping Arrow",
                                               "Shadow Arrow"))
    assert _disparo(trait, _RngSi()) == 12
    assert vistas == ["2d6"]


def test_daño_de_arcane_shot_es_4d6_desde_el_18(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.arcane_archer as aa_mod

    vistas: list[str] = []

    def _dado(expr, rng, *args, **kwargs):
        vistas.append(expr)
        return 24

    monkeypatch.setattr(aa_mod, "roll_dice", _dado)
    _, trait = _arquero(level=18)  # pool completo: 6 opciones
    assert _disparo(trait, _RngSi()) == 24
    assert vistas == ["4d6"]


def test_reset_restaura_los_usos_de_arcane_shot():
    _, trait = _arquero(level=3)
    trait.arcane_shot_usage.spend()
    trait.shot_used_this_turn = True
    trait.reset()
    assert trait.arcane_shot_usage.uses_left == 2
    assert trait.shot_used_this_turn is False


# --- Efectos de las opciones (salvaciones y condiciones) ----------------------

def test_cd_de_arcane_shot_es_8_mas_pb_mas_int():
    _, trait = _arquero(level=3)
    assert trait._cd() == (8 + proficiency_bonus(3)
                            + trait.owner.abilities.mod("int"))


def test_banishing_arrow_falla_la_salvacion_y_deja_incapacitado():
    _, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                               "Banishing Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    assert _disparo(trait, _RngFalla(), target=objetivo) > 0
    assert objetivo.conditions.has(Condition.INCAPACITATED)
    assert trait.arcane_shot_usage.uses_left == 1


def test_banishing_arrow_salvacion_exitosa_no_aplica_condicion():
    _, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                               "Banishing Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    assert _disparo(trait, _RngSi(), target=objetivo) > 0  # d20 = 20
    assert not objetivo.conditions.has(Condition.INCAPACITATED)
    assert trait.arcane_shot_usage.uses_left == 1


def test_beguiling_arrow_hechiza_y_termina_si_el_aliado_ataca():
    pj, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                                "Beguiling Arrow"))
    aliado = _pj(name="Arwen")
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, aliado, objetivo], round=1)
    assert _disparo(trait, _RngFalla(), target=objetivo, ctx=ctx) > 0
    assert objetivo.conditions.has(Condition.CHARMED)
    assert trait.beguiling.get(objetivo.name) is aliado
    # El aliado ataca a la víctima: el hechizo termina y la marca cae.
    mods = SimpleNamespace(advantage_sources=[], disadvantage_sources=[])
    trait.grant_attack_modifiers(mods, aliado, objetivo,
                                 AttackRange.RANGED, ctx=ctx)
    assert not objetivo.conditions.has(Condition.CHARMED)
    assert trait.beguiling == {}


def test_beguiling_sin_aliados_no_tira_salvacion(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.arcane_archer as aa_mod

    pj, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                                "Beguiling Arrow"))
    enemigo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, enemigo], round=1)

    def _no_debe_llamarse(*args, **kwargs):
        raise AssertionError("sin aliados no se tira salvación")

    monkeypatch.setattr(aa_mod, "saving_throw", _no_debe_llamarse)
    assert _disparo(trait, _RngSi(), target=enemigo, ctx=ctx) > 0
    assert enemigo.conditions.instances == []
    assert trait.arcane_shot_usage.uses_left == 1  # el daño sí se aplicó


def test_enfeebling_arrow_marca_el_dano_mitigado():
    pj, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                                "Enfeebling Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, objetivo], round=3)
    assert _disparo(trait, _RngFalla(), target=objetivo, ctx=ctx) > 0
    assert objetivo.state.enfeeble_hasta_ronda == {pj.name: 4}


def test_enfeebling_salvacion_exitosa_no_marca():
    pj, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                                "Enfeebling Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, objetivo], round=3)
    assert _disparo(trait, _RngSi(), target=objetivo, ctx=ctx) > 0
    assert objetivo.state.enfeeble_hasta_ronda == {}


def test_shadow_arrow_solo_tira_salvacion_sin_condicion():
    _, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                               "Shadow Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    assert _disparo(trait, _RngFalla(), target=objetivo) > 0
    assert objetivo.conditions.instances == []
    assert trait.arcane_shot_usage.uses_left == 1


def test_bursting_arrow_dana_a_los_vecinos_sin_salvacion():
    pj, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                                "Bursting Arrow"))
    aliado = _pj(name="Arwen")
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    vecino = Monster("Vecino", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, aliado, objetivo, vecino],
                          round=1)
    assert _disparo(trait, _RngFalla(), target=objetivo, ctx=ctx) > 0
    # 2d6 con el RNG del test (siempre 1s) = 2 de fuerza al vecino.
    assert vecino.hp == vecino.max_hp - 2
    # Sin salvación ni condición; el aliado no recibe nada.
    assert objetivo.conditions.instances == []
    assert vecino.conditions.instances == []
    assert aliado.hp == aliado.max_hp
    assert trait.arcane_shot_usage.uses_left == 1


def test_bursting_sin_vecinos_no_tira_dados_extra(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.arcane_archer as aa_mod

    _, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                               "Bursting Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[_pj(), objetivo], round=1)
    vistas: list[str] = []
    original = aa_mod.roll_dice

    def _espia(expr, rng, *args, **kwargs):
        vistas.append(expr)
        return original(expr, rng, *args, **kwargs)

    monkeypatch.setattr(aa_mod, "roll_dice", _espia)
    assert _disparo(trait, _RngFalla(), target=objetivo, ctx=ctx) > 0
    # Solo el daño base del shot: sin vecinos no hay tirada de 2d6 extra.
    assert vistas == ["2d6"]


def test_reset_borra_las_marcas_de_beguiling():
    _, trait = _arquero(level=3)
    trait.beguiling["Blanco"] = object()
    trait.reset()
    assert trait.beguiling == {}


def test_la_marca_de_enfeebling_mitiga_por_ronda():
    from dnd_sim.core.combat_state import CombatState

    estado = CombatState()
    assert estado.enfeeble_mitiga(1) is False
    estado.enfeeble_hasta_ronda["Legolas"] = 4
    assert estado.enfeeble_mitiga(3) is True
    assert estado.enfeeble_mitiga(4) is True
    assert estado.enfeeble_mitiga(5) is False
    assert estado.enfeeble_mitiga(None) is False


def test_el_motor_mitiga_el_dano_con_la_marca_de_enfeebling(monkeypatch):
    import random

    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    atk = Attack("Hacha de batalla", "1d12", ability="str")
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=15, rolls=[15],
                                    mode=RollMode.NORMAL))
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 10)

    pj = _pj()
    sin_marca = Monster("Muñeco", max_hp=100, ac=10, abilities=_abilities(),
                        attacks=[])
    atk_mod.attack_roll(pj, sin_marca, atk, random.Random(1),
                        ctx=SimpleNamespace(round=1,
                                            combatants=[pj, sin_marca]))
    pj.state.enfeeble_hasta_ronda["Arquero"] = 99
    con_marca = Monster("Muñeco", max_hp=100, ac=10, abilities=_abilities(),
                        attacks=[])
    atk_mod.attack_roll(pj, con_marca, atk, random.Random(1),
                        ctx=SimpleNamespace(round=1,
                                            combatants=[pj, con_marca]))

    esperado = 10 + pj.abilities.mod("str")  # dado fijo + mod FUE
    assert sin_marca.hp == sin_marca.max_hp - esperado
    assert con_marca.hp == con_marca.max_hp - esperado // 2

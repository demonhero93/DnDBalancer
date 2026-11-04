"""Features de la subclase Path of la Giant del bárbaro (Camino del Gigante).

Cubre la tabla de features, Giant Stature/Demiurgic Colossus (tamaño),
Crushing Throw (arrojadiza con FUE), Elemental Cleaver (tipo +1d6/2d6,
arrojadiza, restauración), Mighty Impel (bonus action con agarrado), el
límite de tamaño de Agarrar y la reproducibilidad con semilla fija.
"""
from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from dnd_sim import (
    Abilities, Attack, BarbarianFeatures, GiantFeatures, Monster,
    PlayerCharacter, RollMode, D20Result, apply_barbarian, apply_class,
    rage_damage,
)
from dnd_sim.core.enums import AttackRange
from dnd_sim.model.actions import ActionType
from dnd_sim.rules import utility
from dnd_sim.rules.classes.barbarian import BARBARIAN_CLASS
from dnd_sim.rules.classes.barbarian.subclasses.giant import (
    GIANT_FEATURES, MightyImpelAction, apply_giant,
)
from dnd_sim.rules.conditions import Condition, apply_condition
from dnd_sim.rules.saves import SaveResult
from dnd_sim.engine.combat import attack_roll


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=10, con=14, int=10, wis=10, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(level: int = 5) -> PlayerCharacter:
    return PlayerCharacter(
        name="Thor", max_hp=500, ac=15, level=level, abilities=_abilities(),
        attacks=[Attack("Hacha de batalla", "1d12", ability="str")],
    )


def _mon(name: str = "Orco") -> Monster:
    return Monster(name=name, max_hp=500, ac=12, abilities=_abilities())


def _giant(pj, level):
    """Aplica clase + subclase y devuelve el rasgo de la subclase."""
    apply_barbarian(pj, level=level)
    return apply_giant(pj, level=level)


def _barbaro(pj) -> BarbarianFeatures:
    return next(t for t in pj.traits if isinstance(t, BarbarianFeatures))


def _ctx(actor, combatants, seed=0):
    return SimpleNamespace(actor=actor, combatants=list(combatants),
                           rng=random.Random(seed), log=[], round=1)


def _furia(pj, level, seed=0):
    """Giant aplicado, Furia activa y on_rage_start ejecutado."""
    giant = _giant(pj, level)
    barb = _barbaro(pj)
    barb.activate(1)
    ctx = _ctx(pj, [pj], seed)
    giant.on_rage_start(pj, ctx)
    return giant, barb, ctx


def _siempre_falla(target, ability, dc, rng, mode=None, *, kind=None,
                   magical=False, **kw) -> SaveResult:
    return SaveResult(ability=ability, dc=dc, rolls=[1], bonus=0, total=1,
                      success=False, mode=RollMode.NORMAL)


# --- Tabla y aplicación ------------------------------------------------------

def test_giant_features_por_nivel():
    assert GIANT_FEATURES == {
        3: ("Giant's Power", "Giant's Havoc"),
        6: ("Elemental Cleaver",),
        10: ("Mighty Impel",),
        14: ("Demiurgic Colossus",),
    }


def test_apply_requiere_clase_barbara():
    with pytest.raises(ValueError, match="apply_barbarian"):
        apply_giant(_pj())


def test_apply_anade_trait_y_accion():
    pj = _pj(level=5)
    apply_barbarian(pj, level=5)
    sub = apply_giant(pj)
    assert isinstance(sub, GiantFeatures)
    assert sub.level == 5
    assert sub in pj.traits
    accion = next(a for a in pj.actions
                  if isinstance(a, MightyImpelAction))
    assert accion.action_type is ActionType.BONUS_ACTION
    assert accion.name == "Lanzamiento potente"
    assert accion.usage is None  # el límite es la Furia y el agarrado


def test_apply_class_registra_giant():
    assert "giant" in BARBARIAN_CLASS.subclasses
    pj = _pj(level=5)
    apply_class(pj, "barbarian", "giant")
    assert any(isinstance(t, GiantFeatures) for t in pj.traits)


# --- Giant Stature / Demiurgic Colossus --------------------------------------

def test_giant_stature_hace_grande_al_barbaro_en_furia():
    pj = _pj(level=3)
    _furia(pj, 3, seed=5)
    assert pj.size == "large"
    assert pj.size_base == "medium"


def test_giant_stature_devuelve_el_tamano_al_terminar_la_furia():
    pj = _pj(level=3)
    giant, barb, ctx = _furia(pj, 3, seed=5)
    giant.on_rage_end(pj, ctx)
    assert pj.size == "medium"


def test_combatant_reset_restaura_el_tamano_tras_giant_stature():
    pj = _pj(level=3)
    _furia(pj, 3, seed=5)
    assert pj.size == "large"
    pj.reset()
    assert pj.size == "medium"


def test_demiurgic_colossus_pasa_a_huge_en_furia():
    pj = _pj(level=14)
    _furia(pj, 14, seed=5)
    assert pj.size == "huge"


def test_nivel_3_no_recibe_elemental_cleaver_ni_mighty_impel():
    pj = _pj(level=3)
    giant, _barb, ctx = _furia(pj, 3, seed=3)
    assert giant.elemental_tipo is None  # Elemental Cleaver es nivel 6
    objetivo = _mon()
    ctx.combatants = [pj, objetivo]
    apply_condition(objetivo, Condition.GRAPPLED, ctx, source=pj)
    accion = next(a for a in pj.actions
                  if isinstance(a, MightyImpelAction))
    assert accion.can_use(ctx) is False  # Mighty Impel es nivel 10


def test_nivel_6_no_recibe_mighty_impel_y_el_tamano_no_es_huge():
    pj = _pj(level=6)
    giant, _barb, ctx = _furia(pj, 6, seed=3)
    assert giant.elemental_tipo is not None  # Elemental Cleaver sí
    assert pj.size == "large"  # Huge es nivel 14
    objetivo = _mon()
    ctx.combatants = [pj, objetivo]
    apply_condition(objetivo, Condition.GRAPPLED, ctx, source=pj)
    accion = next(a for a in pj.actions
                  if isinstance(a, MightyImpelAction))
    assert accion.can_use(ctx) is False


# --- Crushing Throw ----------------------------------------------------------

def test_crushing_throw_solo_en_arrojadiza_con_fue():
    pj = _pj(level=5)
    giant, barb, _ctx_ = _furia(pj, 5, seed=1)
    lanzamiento = Attack("Jabalina", "1d6", ability="str",
                         range_type=AttackRange.RANGED)
    cuerpo = Attack("Hacha", "1d12", ability="str")
    dex = Attack("Daga", "1d4", ability="dex",
                 range_type=AttackRange.RANGED)
    esperado = rage_damage(5)
    # Arrojadiza con FUE: suma el daño de Furia (sin RNG: es un bono fijo).
    assert giant.extra_attack_damage(
        pj, _mon(), AttackRange.RANGED, atk=lanzamiento) == esperado
    # Solo arrojadiza: cuerpo a cuerpo y DEX no lo reciben del rasgo.
    assert giant.extra_attack_damage(
        pj, _mon(), AttackRange.MELEE, atk=cuerpo) == 0
    assert giant.extra_attack_damage(
        pj, _mon(), AttackRange.RANGED, atk=dex) == 0
    # Sin Furia no hay nada.
    barb.rage_active = False
    assert giant.extra_attack_damage(
        pj, _mon(), AttackRange.RANGED, atk=lanzamiento) == 0


def test_la_furia_base_no_suma_en_ataques_arrojadizos():
    # Guardia de rango en features.py: el daño de Furia de la clase es
    # cuerpo a cuerpo; lo arrojadizo lo cubre Crushing Throw (sin doble).
    pj = _pj(level=5)
    apply_barbarian(pj, level=5)
    barb = _barbaro(pj)
    barb.activate(1)
    lanzamiento = Attack("Jabalina", "1d6", ability="str",
                         range_type=AttackRange.RANGED)
    cuerpo = Attack("Hacha", "1d12", ability="str")
    assert barb.extra_attack_damage(
        pj, _mon(), AttackRange.RANGED, atk=lanzamiento) == 0
    assert barb.extra_attack_damage(
        pj, _mon(), AttackRange.MELEE, atk=cuerpo) == rage_damage(5)


def test_crushing_throw_no_se_paga_si_el_ataque_falla(monkeypatch):
    import dnd_sim.engine.combat.attack as combat_mod

    def fijar(valor):
        def espia(rng, mode=RollMode.NORMAL, **kw):
            return D20Result(value=valor, rolls=[valor, valor], mode=mode)
        monkeypatch.setattr(combat_mod, "roll_d20", espia)

    pj = _pj(level=5)
    _furia(pj, 5, seed=2)
    objetivo = _mon()
    ctx = _ctx(pj, [pj, objetivo], seed=3)
    ctx.combatants = [pj, objetivo]
    javalina = Attack("Jabalina", "1d6", ability="str",
                      range_type=AttackRange.RANGED)
    # Falla (d20 = 1): el hook no se invoca, no hay bonus de Giant.
    fijar(1)
    log = []
    attack_roll(pj, objetivo, javalina, random.Random(3), log=log, ctx=ctx)
    assert not any("de Giant" in linea for linea in log)
    # Acierta (d20 = 20): Crushing Throw suma el daño de Furia.
    fijar(20)
    log = []
    attack_roll(pj, objetivo, javalina, random.Random(3), log=log, ctx=ctx)
    assert any("de Giant" in linea for linea in log)


# --- Elemental Cleaver -------------------------------------------------------

def test_elemental_cleaver_imbuye_un_arma_al_entrar_en_furia():
    pj = _pj(level=6)
    giant, _barb, ctx = _furia(pj, 6, seed=11)
    assert giant.elemental_tipo in ("acid", "cold", "fire",
                                    "lightning", "thunder")
    arma = giant.elemental_arma
    assert arma is pj.attacks[0]
    assert arma.damage_type.value == giant.elemental_tipo
    assert arma.range_type is AttackRange.MELEE_OR_RANGED  # arrojadiza
    assert any("Elemental Cleaver" in linea for linea in ctx.log)


def test_elemental_cleaver_suma_1d6_al_impactar(monkeypatch):
    import dnd_sim.rules.classes.barbarian.subclasses.giant as giant_mod

    llamadas = []

    def fijo(expr, rng, crit=False):
        llamadas.append(expr)
        return 5

    monkeypatch.setattr(giant_mod, "roll_dice", fijo)
    pj = _pj(level=6)
    giant, _barb, ctx = _furia(pj, 6, seed=1)
    arma = giant.elemental_arma
    bonus = giant.extra_attack_damage(pj, _mon(), AttackRange.MELEE, False,
                                      ctx, ctx.rng, atk=arma)
    assert bonus == 5
    assert llamadas == ["1d6"]
    # Otra arma distinta de la imbuyida: sin extra elemental.
    otro = Attack("Daga", "1d4", ability="str")
    assert giant.extra_attack_damage(pj, _mon(), AttackRange.MELEE, False,
                                     ctx, ctx.rng, atk=otro) == 0


def test_elemental_cleaver_sube_a_2d6_en_el_nivel_14(monkeypatch):
    import dnd_sim.rules.classes.barbarian.subclasses.giant as giant_mod

    llamadas = []

    def fijo(expr, rng, crit=False):
        llamadas.append(expr)
        return 6

    monkeypatch.setattr(giant_mod, "roll_dice", fijo)
    pj = _pj(level=14)
    giant, _barb, ctx = _furia(pj, 14, seed=2)
    bonus = giant.extra_attack_damage(pj, _mon(), AttackRange.MELEE, False,
                                      ctx, ctx.rng,
                                      atk=giant.elemental_arma)
    assert bonus == 6
    assert llamadas == ["2d6"]


def test_elemental_cleaver_restaura_el_arma_al_terminar_la_furia():
    pj = _pj(level=6)
    tipo_previo = pj.attacks[0].damage_type
    rango_previo = pj.attacks[0].range_type
    giant, barb, ctx = _furia(pj, 6, seed=7)
    arma = giant.elemental_arma
    assert arma.damage_type != tipo_previo  # imbuyida
    giant.on_rage_end(pj, ctx)
    assert arma.damage_type == tipo_previo
    assert arma.range_type == rango_previo
    assert giant.elemental_arma is None
    assert giant.elemental_tipo is None
    assert pj.size == "medium"


# --- Mighty Impel ------------------------------------------------------------

def test_mighty_impel_lanza_al_agarrado(monkeypatch):
    import dnd_sim.rules.classes.barbarian.subclasses.giant as giant_mod

    monkeypatch.setattr(giant_mod, "roll_dice",
                        lambda expr, rng, crit=False: 10)
    pj = _pj(level=10)
    apply_barbarian(pj, level=10)
    giant = apply_giant(pj, level=10)
    _barbaro(pj).activate(1)
    objetivo = _mon()
    ctx = _ctx(pj, [pj, objetivo], seed=5)
    apply_condition(objetivo, Condition.GRAPPLED, ctx, source=pj)
    accion = next(a for a in pj.actions
                  if isinstance(a, MightyImpelAction))
    assert accion.can_use(ctx) is True
    hp_antes = objetivo.hp
    accion.execute(ctx)
    assert Condition.PRONE in objetivo.conditions.active()
    assert not any(i.condition is Condition.GRAPPLED and i.source is pj
                   for i in objetivo.conditions.instances)
    assert objetivo.hp == hp_antes - 10  # 3d6 fijado a 10
    assert any("Lanzamiento potente" in linea for linea in ctx.log)


def test_mighty_impel_no_disponible_sin_furia_sin_agarrado_o_en_grande():
    pj = _pj(level=10)
    apply_barbarian(pj, level=10)
    apply_giant(pj, level=10)
    barb = _barbaro(pj)
    objetivo = _mon()
    ctx = _ctx(pj, [pj, objetivo], seed=1)
    accion = next(a for a in pj.actions
                  if isinstance(a, MightyImpelAction))
    # Con agarrado pero sin Furia.
    apply_condition(objetivo, Condition.GRAPPLED, ctx, source=pj)
    assert accion.can_use(ctx) is False
    # Con Furia pero sin agarrado.
    barb.activate(1)
    objetivo2 = _mon(name="Orco 2")
    ctx.combatants = [pj, objetivo2]
    assert accion.can_use(ctx) is False
    # Con Furia y agarrado, pero el objetivo es Large (no Mediano o menor).
    ctx.combatants = [pj, objetivo]
    assert accion.can_use(ctx) is True
    objetivo.size = "large"
    assert accion.can_use(ctx) is False


# --- Interacción con el límite de Agarrar ------------------------------------

def test_giant_stature_amplia_el_limite_de_agarrar(monkeypatch):
    monkeypatch.setattr(utility, "UTILITY_ACTION_PROBABILITY", 1.0)
    monkeypatch.setattr(utility, "saving_throw", _siempre_falla)
    pj = _pj(level=3)
    giant = _giant(pj, 3)
    barb = _barbaro(pj)
    ctx = _ctx(pj, [pj], seed=4)
    dragon = _mon(name="Dragón")
    dragon.size = "huge"
    ctx.combatants = [pj, dragon]
    apply_condition(dragon, Condition.PRONE, ctx, source=pj)
    # Sin Furia (medium): huge queda fuera del pool de Agarrar y ya está
    # derribado (empujar tampoco), así que no hay utilitaria.
    assert utility.ataque_utilitario(pj, ctx, ctx.rng,
                                    atk=pj.attacks[0]) is False
    # En Furia (Giant Stature → large): huge entra en el pool.
    barb.activate(1)
    giant.on_rage_start(pj, ctx)
    assert pj.size == "large"
    assert utility.ataque_utilitario(pj, ctx, ctx.rng,
                                    atk=pj.attacks[0]) is True
    assert any(i.condition is Condition.GRAPPLED
               for i in dragon.conditions.instances)


# --- Determinismo -------------------------------------------------------------

def test_la_misma_semilla_elige_el_mismo_elemental():
    pj1 = _pj(level=6)
    giant1, _b1, ctx1 = _furia(pj1, 6, seed=42)
    pj2 = _pj(level=6)
    giant2, _b2, ctx2 = _furia(pj2, 6, seed=42)
    assert giant1.elemental_tipo == giant2.elemental_tipo
    # Mismo rng para el daño extra: mismo resultado.
    extra1 = giant1.extra_attack_damage(
        pj1, _mon(), AttackRange.MELEE, False, ctx1, random.Random(9),
        atk=giant1.elemental_arma)
    extra2 = giant2.extra_attack_damage(
        pj2, _mon(), AttackRange.MELEE, False, ctx2, random.Random(9),
        atk=giant2.elemental_arma)
    assert extra1 == extra2

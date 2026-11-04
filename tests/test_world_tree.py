"""Features de la subclase Path of the World Tree del bárbaro (PHB 2024).

Cubre la tabla de rasgos, Vitality Surge (PV temporales), Life-Giving
Force (curación con pick y sin candidatos sin RNG), Battering Roots
(Topple con armas Heavy/Versatile), Branches/Travel como datos, niveles
inferiores, los campos nuevos de Attack (no regresión) y la
reproducibilidad con semilla fija.
"""
from __future__ import annotations

import random
from types import SimpleNamespace

from dnd_sim import (
    Abilities, Attack, BarbarianFeatures, Monster, PlayerCharacter,
    RollMode, SaveResult, apply_barbarian, apply_class, rage_damage,
)
from dnd_sim.core.enums import AttackRange
from dnd_sim.core.randomness import pick as pick_real
from dnd_sim.rules.classes.barbarian import BARBARIAN_CLASS
from dnd_sim.rules.classes.barbarian.subclasses import world_tree as wt
from dnd_sim.rules.classes.barbarian.subclasses.world_tree import (
    WORLD_TREE_FEATURES, WorldTreeFeatures, apply_world_tree,
)
from dnd_sim.rules.conditions import Condition


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


def _aliado(level: int = 5, hp: int = 100) -> PlayerCharacter:
    aliado = PlayerCharacter(name="Aliado", max_hp=500, ac=15, level=level,
                             abilities=_abilities())
    aliado.hp = hp
    return aliado


def _wild(pj, level):
    """Aplica clase + subclase y devuelve el rasgo."""
    apply_barbarian(pj, level=level)
    return apply_world_tree(pj, level=level)


def _barbaro(pj) -> BarbarianFeatures:
    return next(t for t in pj.traits if isinstance(t, BarbarianFeatures))


def _ctx(actor, combatants, seed=0):
    return SimpleNamespace(actor=actor, combatants=list(combatants),
                           rng=random.Random(seed), log=[], round=1)


def _furia(pj, level, seed=0):
    """World Tree aplicado, Furia activa y on_rage_start ejecutado."""
    arbol = _wild(pj, level)
    barb = _barbaro(pj)
    barb.activate(1)
    ctx = _ctx(pj, [pj], seed)
    arbol.on_rage_start(pj, ctx)
    return arbol, barb, ctx


def _elige_candidato():
    """pick que devuelve el primer candidato no-None (para curar)."""
    def espia(rng, opciones):
        for opcion in opciones:
            if opcion is not None:
                return opcion
        return pick_real(rng, opciones)
    return espia


def _decision(valor):
    """pick forzado para la decisión ("no", "si")."""
    def espia(rng, opciones):
        if opciones == ("no", "si"):
            return valor
        return pick_real(rng, opciones)
    return espia


def _salvacion(salva: bool, llamadas=None):
    def stub(target, ability, dc, rng, mode=None, *, kind=None,
             magical=False):
        if llamadas is not None:
            llamadas.append((ability, dc))
        total = 30 if salva else 1
        return SaveResult(ability=ability, dc=dc, rolls=[total], bonus=0,
                          total=total, success=salva,
                          mode=RollMode.NORMAL)
    return stub


# --- Tabla y aplicación ------------------------------------------------------

def test_world_tree_features_por_nivel():
    assert WORLD_TREE_FEATURES == {
        3: ("Vitality of the Tree",),
        6: ("Branches of the Tree",),
        10: ("Battering Roots",),
        14: ("Travel Along the Tree",),
    }


def test_apply_requiere_clase_barbara():
    import pytest
    with pytest.raises(ValueError, match="apply_barbarian"):
        apply_world_tree(_pj())


def test_apply_anade_trait_sin_accion_propia():
    pj = _pj(level=5)
    apply_barbarian(pj, level=5)
    antes = len(pj.actions)
    sub = apply_world_tree(pj)
    assert isinstance(sub, WorldTreeFeatures)
    assert sub.level == 5
    assert sub in pj.traits
    assert len(pj.actions) == antes  # sin acción propia (Travel es dato)


def test_apply_class_registra_world_tree():
    assert "world_tree" in BARBARIAN_CLASS.subclasses
    # No confunde con las otras subclases de Bárbaro.
    for clave in ("wild_heart", "wild_magic", "beast", "giant"):
        assert clave in BARBARIAN_CLASS.subclasses
    pj = _pj(level=5)
    apply_class(pj, "barbarian", "world_tree")
    assert any(isinstance(t, WorldTreeFeatures) for t in pj.traits)


# --- Vitality Surge -------------------------------------------------------------

def test_vitality_surge_da_pv_temporales_iguales_al_nivel():
    pj = _pj(level=5)
    _furia(pj, 5, seed=1)
    assert pj.temp_hp == 5


def test_vitality_surge_no_se_acumulan_con_los_previos_mayores():
    pj = _pj(level=5)
    pj.temp_hp = 20
    _furia(pj, 5, seed=1)
    assert pj.temp_hp == 20  # se queda el mayor


def test_vitality_surge_no_se_revoca_al_terminar_la_furia():
    pj = _pj(level=5)
    arbol, _barb, ctx = _furia(pj, 5, seed=1)
    arbol.on_rage_end(pj, ctx)
    assert pj.temp_hp == 5  # política de la Furia base: no se retiran


def test_vitality_surge_no_se_activa_por_debajo_del_nivel_3():
    pj = _pj(level=5)
    arbol = _wild(pj, 5)
    arbol.level = 2  # por debajo del nivel de la feature
    barb = _barbaro(pj)
    barb.activate(1)
    arbol.on_rage_start(pj, _ctx(pj, [pj], seed=1))
    assert pj.temp_hp == 0


# --- Life-Giving Force ------------------------------------------------------------

def test_life_giving_cura_con_rage_damage_d6_y_loguea(monkeypatch):
    llamadas = []

    def roll_dice_espia(expr, rng, crit=False):
        llamadas.append(expr)
        return 9

    monkeypatch.setattr(wt, "pick", _elige_candidato())
    monkeypatch.setattr(wt, "roll_dice", roll_dice_espia)
    pj = _pj(level=5)
    aliado = _aliado(level=5, hp=100)
    arbol, _barb, ctx = _furia(pj, 5, seed=2)
    ctx.combatants = [pj, aliado]
    arbol.on_turn_start(pj, ctx)
    assert llamadas == [f"{rage_damage(5)}d6"]  # d6 = bonificador de Furia
    assert aliado.hp == 109
    assert any("Fuerza Vivificante (9 PG)" in line for line in ctx.log)


def test_life_giving_no_pasa_de_los_pv_maximos(monkeypatch):
    monkeypatch.setattr(wt, "pick", _elige_candidato())
    monkeypatch.setattr(wt, "roll_dice", lambda expr, rng, crit=False: 9)
    pj = _pj(level=5)
    aliado = _aliado(level=5, hp=497)
    arbol, _barb, ctx = _furia(pj, 5, seed=2)
    ctx.combatants = [pj, aliado]
    arbol.on_turn_start(pj, ctx)
    assert aliado.hp == 500  # nunca por encima del máximo


def test_life_giving_no_cura_al_propio_barbaro(monkeypatch):
    opciones = []

    def espia(rng, opts):
        opciones.append(list(opts))
        return None  # no curar

    monkeypatch.setattr(wt, "pick", espia)
    pj = _pj(level=5)
    pj.hp = 50  # el bárbaro también está herido
    aliado = _aliado(level=5, hp=100)
    arbol, _barb, ctx = _furia(pj, 5, seed=2)
    ctx.combatants = [pj, aliado]
    arbol.on_turn_start(pj, ctx)
    assert opciones and pj not in opciones[0]  # él nunca es candidato


def test_life_giving_solo_aliados_heridos(monkeypatch):
    opciones = []

    def espia(rng, opts):
        opciones.append(list(opts))
        return None

    monkeypatch.setattr(wt, "pick", espia)
    pj = _pj(level=5)
    herido = _aliado(level=5, hp=100)
    sano = _aliado(level=5, hp=500)
    arbol, _barb, ctx = _furia(pj, 5, seed=2)
    ctx.combatants = [pj, herido, sano]
    arbol.on_turn_start(pj, ctx)
    assert herido in opciones[0]
    assert sano not in opciones[0]  # a tope no se cura


def test_life_giving_sin_candidatos_no_consume_rng(monkeypatch):
    def espia(rng, opts):
        raise AssertionError("no debería haber pick sin candidatos")

    monkeypatch.setattr(wt, "pick", espia)
    monkeypatch.setattr(
        wt, "roll_dice",
        lambda expr, rng, crit=False: (_ for _ in ()).throw(
            AssertionError("no debería tirar dados sin candidatos")))
    pj = _pj(level=5)
    sano = _aliado(level=5, hp=500)
    arbol, _barb, ctx = _furia(pj, 5, seed=2)
    ctx.combatants = [pj, sano]
    arbol.on_turn_start(pj, ctx)  # sin candidatos: no falla


def test_life_giving_solo_con_furia_activa(monkeypatch):
    monkeypatch.setattr(wt, "pick",
                        lambda rng, opts: (_ for _ in ()).throw(
                            AssertionError("sin Furia no hay pick")))
    pj = _pj(level=5)
    aliado = _aliado(level=5, hp=100)
    arbol = _wild(pj, 5)  # sin activar Furia
    ctx = _ctx(pj, [pj, aliado], seed=2)
    arbol.on_turn_start(pj, ctx)
    assert aliado.hp == 100


def test_life_giving_solo_en_turno_propio(monkeypatch):
    monkeypatch.setattr(wt, "pick",
                        lambda rng, opts: (_ for _ in ()).throw(
                            AssertionError("turno ajeno no cura")))
    pj = _pj(level=5)
    aliado = _aliado(level=5, hp=100)
    arbol, _barb, _ctx_ = _furia(pj, 5, seed=2)
    enemigo = _mon()
    ctx = _ctx(enemigo, [pj, aliado, enemigo], seed=2)  # turno del enemigo
    arbol.on_turn_start(pj, ctx)
    assert aliado.hp == 100


def test_life_giving_respeta_la_decision_de_no_curar(monkeypatch):
    monkeypatch.setattr(wt, "pick", lambda rng, opts: None)
    pj = _pj(level=5)
    aliado = _aliado(level=5, hp=100)
    arbol, _barb, ctx = _furia(pj, 5, seed=2)
    ctx.combatants = [pj, aliado]
    arbol.on_turn_start(pj, ctx)
    assert aliado.hp == 100


# --- Battering Roots: Topple -------------------------------------------------------

def test_topple_derriba_si_falla_la_salvacion_de_con(monkeypatch):
    llamadas = []
    monkeypatch.setattr(wt, "pick", _decision("si"))
    monkeypatch.setattr(wt, "saving_throw", _salvacion(False, llamadas))
    pj = _pj(level=10)
    objetivo = _mon()
    atk = Attack("Maza pesada", "1d6", ability="str", properties={"heavy"})
    arbol, _barb, ctx = _furia(pj, 10, seed=3)
    ctx.combatants = [pj, objetivo]
    bonus = arbol.extra_attack_damage(pj, objetivo, AttackRange.MELEE,
                                      ctx=ctx, rng=ctx.rng, atk=atk)
    assert bonus == 0
    dc_esperada = 8 + pj.proficiency + pj.abilities.mod("str")
    assert llamadas == [("con", dc_esperada)]
    assert Condition.PRONE in objetivo.conditions.active()


def test_topple_no_derriba_si_supera_la_salvacion(monkeypatch):
    monkeypatch.setattr(wt, "pick", _decision("si"))
    monkeypatch.setattr(wt, "saving_throw", _salvacion(True))
    pj = _pj(level=10)
    objetivo = _mon()
    atk = Attack("Maza pesada", "1d6", ability="str", properties={"heavy"})
    arbol, _barb, ctx = _furia(pj, 10, seed=3)
    ctx.combatants = [pj, objetivo]
    arbol.extra_attack_damage(pj, objetivo, AttackRange.MELEE,
                              ctx=ctx, rng=ctx.rng, atk=atk)
    assert Condition.PRONE not in objetivo.conditions.active()


def test_topple_solo_con_armas_pesadas_o_versatiles(monkeypatch):
    llamadas = []
    monkeypatch.setattr(wt, "pick", _decision("si"))
    monkeypatch.setattr(wt, "saving_throw", _salvacion(False, llamadas))
    pj = _pj(level=10)
    objetivo = _mon()
    arbol, _barb, ctx = _furia(pj, 10, seed=3)
    ctx.combatants = [pj, objetivo]
    # Sin propiedades: no se activa.
    arbol.extra_attack_damage(
        pj, objetivo, AttackRange.MELEE, ctx=ctx, rng=ctx.rng,
        atk=Attack("Daga", "1d4", ability="str"))
    assert llamadas == []
    # Versatile: sí.
    arbol.extra_attack_damage(
        pj, objetivo, AttackRange.MELEE, ctx=ctx, rng=ctx.rng,
        atk=Attack("Lanza", "1d6", ability="str", properties={"versatile"}))
    assert len(llamadas) == 1
    assert Condition.PRONE in objetivo.conditions.active()


def test_topple_solo_en_cuerpo_a_cuerpo(monkeypatch):
    llamadas = []
    monkeypatch.setattr(wt, "pick", _decision("si"))
    monkeypatch.setattr(wt, "saving_throw", _salvacion(False, llamadas))
    pj = _pj(level=10)
    objetivo = _mon()
    atk = Attack("Jabalina", "1d6", ability="str", properties={"heavy"},
                 range_type=AttackRange.RANGED)
    arbol, _barb, ctx = _furia(pj, 10, seed=3)
    ctx.combatants = [pj, objetivo]
    arbol.extra_attack_damage(pj, objetivo, AttackRange.RANGED,
                              ctx=ctx, rng=ctx.rng, atk=atk)
    assert llamadas == []


def test_topple_solo_en_turno_propio(monkeypatch):
    llamadas = []
    monkeypatch.setattr(wt, "pick", _decision("si"))
    monkeypatch.setattr(wt, "saving_throw", _salvacion(False, llamadas))
    pj = _pj(level=10)
    objetivo = _mon()
    atk = Attack("Maza pesada", "1d6", ability="str", properties={"heavy"})
    arbol, _barb, ctx = _furia(pj, 10, seed=3)
    ctx.combatants = [pj, objetivo]
    # Reacción: no.
    ctx.is_reaction = True
    arbol.extra_attack_damage(pj, objetivo, AttackRange.MELEE,
                              ctx=ctx, rng=ctx.rng, atk=atk)
    ctx.is_reaction = False
    # Turno ajeno (ctx.actor != atacante): no.
    enemigo = _mon("Troll")
    ctx.actor = enemigo
    arbol.extra_attack_damage(pj, objetivo, AttackRange.MELEE,
                              ctx=ctx, rng=ctx.rng, atk=atk)
    assert llamadas == []


def test_topple_no_se_activa_si_el_arma_ya_tiene_topple(monkeypatch):
    llamadas = []
    monkeypatch.setattr(wt, "pick", _decision("si"))
    monkeypatch.setattr(wt, "saving_throw", _salvacion(False, llamadas))
    pj = _pj(level=10)
    objetivo = _mon()
    atk = Attack("Maza pesada", "1d6", ability="str",
                 properties={"heavy"}, mastery="topple")
    arbol, _barb, ctx = _furia(pj, 10, seed=3)
    ctx.combatants = [pj, objetivo]
    arbol.extra_attack_damage(pj, objetivo, AttackRange.MELEE,
                              ctx=ctx, rng=ctx.rng, atk=atk)
    assert llamadas == []  # no se duplica la maestría


def test_topple_no_exige_furia_activa(monkeypatch):
    llamadas = []
    monkeypatch.setattr(wt, "pick", _decision("si"))
    monkeypatch.setattr(wt, "saving_throw", _salvacion(False, llamadas))
    pj = _pj(level=10)
    objetivo = _mon()
    atk = Attack("Maza pesada", "1d6", ability="str", properties={"heavy"})
    arbol = _wild(pj, 10)  # SIN Furia
    ctx = _ctx(pj, [pj, objetivo], seed=3)
    arbol.extra_attack_damage(pj, objetivo, AttackRange.MELEE,
                              ctx=ctx, rng=ctx.rng, atk=atk)
    assert len(llamadas) == 1
    assert Condition.PRONE in objetivo.conditions.active()


def test_topple_no_se_activa_por_debajo_del_nivel_10(monkeypatch):
    llamadas = []
    monkeypatch.setattr(wt, "pick", _decision("si"))
    monkeypatch.setattr(wt, "saving_throw", _salvacion(False, llamadas))
    pj = _pj(level=6)
    objetivo = _mon()
    atk = Attack("Maza pesada", "1d6", ability="str", properties={"heavy"})
    arbol, _barb, ctx = _furia(pj, 6, seed=3)
    ctx.combatants = [pj, objetivo]
    arbol.extra_attack_damage(pj, objetivo, AttackRange.MELEE,
                              ctx=ctx, rng=ctx.rng, atk=atk)
    assert llamadas == []


# --- Branches y Travel: datos sin efecto -----------------------------------------

def test_branches_y_travel_no_consumen_rng_ni_cambian_estado(monkeypatch):
    def espia(rng, opciones):
        raise AssertionError("las features de datos no consumen RNG")

    monkeypatch.setattr(wt, "pick", espia)
    monkeypatch.setattr(
        wt, "roll_dice",
        lambda expr, rng, crit=False: (_ for _ in ()).throw(
            AssertionError("las features de datos no tiran dados")))
    pj = _pj(level=14)
    arbol, _barb, ctx = _furia(pj, 14, seed=4)  # on_rage_start: solo PV
    assert pj.temp_hp == 14  # Vitality Surge (automático) sí ocurre
    assert pj.state.reaction_used is False  # Branches no gasta reacción
    aliado = _aliado(level=14, hp=500)
    ctx.combatants = [pj, aliado]
    arbol.on_turn_start(pj, ctx)  # sin candidatos: sin RNG


# --- No regresión de los campos de Attack -----------------------------------------

def test_los_nuevos_campos_de_attack_no_cambian_las_fichas_existentes():
    atk = Attack("Hacha de batalla", "1d12", ability="str")
    assert atk.properties == set()
    assert atk.mastery == ""
    pj = _pj(level=5)
    assert pj.attacks[0].properties == set()
    assert pj.attacks[0].mastery == ""


# --- Determinismo -----------------------------------------------------------------

def test_la_misma_semilla_curra_lo_mismo(monkeypatch):
    # Sin monkeypatch: elección y dados reales con la misma semilla.
    pj1, aliado1 = _pj(level=5), _aliado(level=5, hp=100)
    arbol1, _b1, ctx1 = _furia(pj1, 5, seed=42)
    ctx1.combatants = [pj1, aliado1, _aliado(level=5, hp=200)]
    arbol1.on_turn_start(pj1, ctx1)

    pj2, aliado2 = _pj(level=5), _aliado(level=5, hp=100)
    arbol2, _b2, ctx2 = _furia(pj2, 5, seed=42)
    ctx2.combatants = [pj2, aliado2, _aliado(level=5, hp=200)]
    arbol2.on_turn_start(pj2, ctx2)

    assert aliado1.hp == aliado2.hp  # mismo objetivo y misma curación
    assert [line for line in ctx1.log] == [line for line in ctx2.log]

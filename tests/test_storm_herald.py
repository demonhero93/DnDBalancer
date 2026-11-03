"""Features de la subclase Path of the Storm Herald del bárbaro (XGE).

Cubre la tabla de features, los tres entornos (desierto/mar/tundra) con
sus escalados, activación por Furia y por acción adicional, Storm Soul
permanente, Shielding Storm con marca de fuente, Raging Storm con
reacción, niveles inferiores y reproducibilidad con semilla fija.
"""
from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from dnd_sim import (
    Abilities, Attack, BarbarianFeatures, Monster, PlayerCharacter,
    RollMode, StormAuraAction, StormHeraldFeatures, apply_barbarian,
    apply_class, apply_storm_herald,
)
from dnd_sim.core.enums import AttackRange, parse_damage_type
from dnd_sim.rules.classes.base import CLASSES
from dnd_sim.rules.classes.barbarian.subclasses.storm_herald import (
    STORM_HERALD_FEATURES, ENTORNOS,
)
from dnd_sim.rules.conditions import Condition
from dnd_sim.rules.saves import SaveResult


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=10, con=14, int=10, wis=10, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(level: int = 5) -> PlayerCharacter:
    return PlayerCharacter(
        name="Thor", max_hp=500, ac=15, level=level, abilities=_abilities(),
        attacks=[Attack("Hacha de batalla", "1d12", ability="str")],
    )


def _mon(name: str = "Orco", **kw) -> Monster:
    return Monster(name=name, max_hp=500, ac=12, abilities=_abilities(), **kw)


def _aliado(name: str = "Aliado") -> PlayerCharacter:
    """Aliado del bárbaro: mismo equipo, derivado del tipo de combatiente."""
    return PlayerCharacter(
        name=name, max_hp=500, ac=15, level=5, abilities=_abilities(),
        attacks=[Attack("Daga", "1d4", ability="str")],
    )


def _herald(pj, level, entorno="desert") -> StormHeraldFeatures:
    """Aplica clase + subclase y devuelve el rasgo."""
    apply_barbarian(pj, level=level)
    return apply_storm_herald(pj, level=level, entorno=entorno)


def _barbaro(pj) -> BarbarianFeatures:
    return next(t for t in pj.traits if isinstance(t, BarbarianFeatures))


def _ctx(actor, combatants, seed=0):
    return SimpleNamespace(actor=actor, combatants=list(combatants),
                           rng=random.Random(seed), log=[], round=1)


def _furia(pj, level, entorno="desert", seed=0, combatants=None):
    """Rasgo, bárbaro y ctx con Furia activa y aura ya activada."""
    herald = _herald(pj, level, entorno)
    barb = _barbaro(pj)
    barb.activate(1)
    ctx = _ctx(pj, combatants if combatants is not None else [pj], seed)
    herald.activar_aura(pj, ctx)
    return herald, barb, ctx


def _fijar_salvacion(monkeypatch, exito: bool) -> None:
    """saving_throw del módulo saves: resultado fijo (para apply_save_damage)."""
    import dnd_sim.rules.saves as saves_mod

    def espia(target, ability, dc, rng, mode=None, *, kind=None,
              magical=False):
        return SaveResult(ability=ability, dc=dc, rolls=[10], bonus=0,
                          total=10, success=exito, mode=RollMode.NORMAL)

    monkeypatch.setattr(saves_mod, "saving_throw", espia)


def _fijar_fallo_reaccion(monkeypatch) -> None:
    """saving_throw/pick del módulo storm_herald: falla + «sí»."""
    import dnd_sim.rules.classes.barbarian.subclasses.storm_herald as sh

    def falla(target, ability, dc, rng, mode=None, *, kind=None,
              magical=False):
        return SaveResult(ability=ability, dc=dc, rolls=[1], bonus=0,
                          total=1, success=False, mode=RollMode.NORMAL)

    monkeypatch.setattr(sh, "saving_throw", falla)
    monkeypatch.setattr(sh, "pick", lambda rng, opts: opts[-1])


# --- Tabla y aplicación ------------------------------------------------------

def test_storm_herald_features_por_nivel():
    assert STORM_HERALD_FEATURES == {
        3: ("Storm Aura",),
        6: ("Storm Soul",),
        10: ("Shielding Storm",),
        14: ("Raging Storm",),
    }


def test_apply_requiere_clase_barbara():
    with pytest.raises(ValueError, match="apply_barbarian"):
        apply_storm_herald(_pj())


def test_apply_rechaza_entorno_desconocido():
    pj = _pj()
    apply_barbarian(pj, level=5)
    with pytest.raises(ValueError, match="Entorno"):
        apply_storm_herald(pj, entorno="lluvia")


def test_apply_anade_trait_y_accion():
    pj = _pj(level=5)
    trait = _herald(pj, 5, entorno="sea")
    assert isinstance(trait, StormHeraldFeatures)
    assert trait.level == 5
    assert trait.entorno == "sea"
    assert trait in pj.traits
    accion = next(a for a in pj.actions if isinstance(a, StormAuraAction))
    assert accion.name == "Activar Aura de Tormenta"
    assert accion.action_type.value == "bonus_action"
    assert accion.usage is None  # el límite es la Furia, no un recuento


def test_apply_class_registra_los_tres_entornos():
    assert {"storm_herald_desert", "storm_herald_sea",
            "storm_herald_tundra"} <= set(CLASSES["barbarian"].subclasses)
    pj = _pj(level=5)
    apply_class(pj, "barbarian", "storm_herald_tundra")
    trait = next(t for t in pj.traits if isinstance(t, StormHeraldFeatures))
    assert trait.entorno == "tundra"
    with pytest.raises(ValueError, match="válidas"):
        apply_class(_pj(level=5), "barbarian", "storm_herald_mar")


# --- Storm Aura: desert ------------------------------------------------------

def test_el_aura_del_desierto_hace_dano_de_fuego_al_activarse():
    pj = _pj(level=3)
    enemigo = _mon()
    _herald(pj, 3, "desert")
    barb = _barbaro(pj)
    barb.activate(1)
    ctx = _ctx(pj, [pj, enemigo], seed=1)
    herald = next(t for t in pj.traits if isinstance(t, StormHeraldFeatures))
    herald.on_rage_start(pj, ctx)
    assert enemigo.hp == 500 - 2  # 2 de daño de fuego en nivel 3
    assert pj.hp == 500  # «otra criatura»: el bárbaro no se autohiere


def test_el_aura_del_desierto_escala_con_el_nivel():
    for nivel, esperado in ((5, 3), (10, 4), (15, 5), (20, 6)):
        pj = _pj(level=nivel)
        enemigo = _mon()
        _furia(pj, nivel, "desert", seed=2, combatants=[pj, enemigo])
        assert enemigo.hp == 500 - esperado, f"nivel {nivel}"


def test_el_dano_del_aura_es_magico_y_ignora_nonmagical_resistances():
    pj = _pj(level=3)
    enemigo = _mon(nonmagical_resistances={"fire"})
    _furia(pj, 3, "desert", seed=3, combatants=[pj, enemigo])
    assert enemigo.hp == 500 - 2  # daño mágico: la resistencia no mágica no cuenta


# --- Storm Aura: sea ---------------------------------------------------------

def test_el_aura_del_mar_tira_salvacion_de_des_con_mitad(monkeypatch):
    import dnd_sim.rules.classes.barbarian.subclasses.storm_herald as sh
    monkeypatch.setattr(sh, "roll_dice", lambda expr, rng, crit=False: 6)
    # Falla: daño completo.
    _fijar_salvacion(monkeypatch, exito=False)
    pj = _pj(level=3)
    enemigo = _mon()
    _furia(pj, 3, "sea", seed=4, combatants=[pj, enemigo])
    assert enemigo.hp == 500 - 6
    # Éxito: mitad.
    _fijar_salvacion(monkeypatch, exito=True)
    pj2 = _pj(level=3)
    enemigo2 = _mon()
    _furia(pj2, 3, "sea", seed=4, combatants=[pj2, enemigo2])
    assert enemigo2.hp == 500 - 3


def test_el_dado_del_mar_sube_con_el_nivel(monkeypatch):
    import dnd_sim.rules.classes.barbarian.subclasses.storm_herald as sh
    llamadas = []

    def fijo(expr, rng, crit=False):
        llamadas.append(expr)
        return 0  # 0 de daño: solo importa qué dado se tira

    monkeypatch.setattr(sh, "roll_dice", fijo)
    _fijar_salvacion(monkeypatch, exito=False)
    for nivel, esperado in ((3, "1d6"), (10, "2d6"), (15, "3d6"),
                            (20, "4d6")):
        pj = _pj(level=nivel)
        _furia(pj, nivel, "sea", seed=5, combatants=[pj, _mon()])
    assert llamadas == ["1d6", "2d6", "3d6", "4d6"]


# --- Storm Aura: tundra ------------------------------------------------------

def test_el_aura_de_la_tundra_da_pv_temporales_al_barbaro_y_aliados():
    pj = _pj(level=3)
    aliado = _aliado()
    _furia(pj, 3, "tundra", seed=6, combatants=[pj, aliado])
    assert pj.temp_hp == 2
    assert aliado.temp_hp == 2


def test_los_pv_temporales_de_la_tundra_no_se_acumulan():
    pj = _pj(level=3)
    herald, _barb, ctx = _furia(pj, 3, "tundra", seed=7)
    assert pj.temp_hp == 2
    pj.temp_hp = 1  # el aura ya se gastó parcialmente en combate
    accion = next(a for a in pj.actions if isinstance(a, StormAuraAction))
    accion.execute(ctx)
    assert pj.temp_hp == 2  # se queda el mayor: no suma 2+2


# --- Activación: Furia y acción adicional ------------------------------------

def test_el_aura_se_reactiva_con_la_accion_adicional():
    pj = _pj(level=3)
    enemigo = _mon()
    _herald(pj, 3, "desert")
    barb = _barbaro(pj)
    barb.activate(1)
    ctx = _ctx(pj, [pj, enemigo], seed=8)
    herald = next(t for t in pj.traits if isinstance(t, StormHeraldFeatures))
    herald.on_rage_start(pj, ctx)  # primera activación: al entrar en Furia
    assert enemigo.hp == 498
    accion = next(a for a in pj.actions if isinstance(a, StormAuraAction))
    assert accion.can_use(ctx) is True
    accion.execute(ctx)  # «acción adicional» en un turno posterior
    assert enemigo.hp == 496


def test_el_aura_no_funciona_fuera_de_la_furia():
    pj = _pj(level=3)
    enemigo = _mon()
    herald = _herald(pj, 3, "desert")
    ctx = _ctx(pj, [pj, enemigo], seed=9)
    accion = next(a for a in pj.actions if isinstance(a, StormAuraAction))
    assert accion.can_use(ctx) is False
    herald.activar_aura(pj, ctx)
    assert enemigo.hp == 500  # sin Furia: nada


def test_la_accion_de_aura_no_esta_disponible_sin_enemigos():
    pj = _pj(level=3)
    _herald(pj, 3, "sea")
    _barbaro(pj).activate(1)
    ctx = _ctx(pj, [pj], seed=10)  # solo el bárbaro: sin enemigos
    accion = next(a for a in pj.actions if isinstance(a, StormAuraAction))
    assert accion.can_use(ctx) is False


# --- Storm Soul (6) ----------------------------------------------------------

def test_storm_soul_es_permanente_aunque_no_haya_furia():
    pj = _pj(level=6)
    _herald(pj, 6, "desert")
    assert "fire" in {t.value for t in pj.resistances}
    pj.reset()  # un combate nuevo no lo quita: es dato permanente
    assert "fire" in {t.value for t in pj.resistances}


def test_storm_soul_da_la_resistencia_de_su_entorno():
    for entorno, tipo in (("sea", "lightning"), ("tundra", "cold")):
        pj = _pj(level=6)
        _herald(pj, 6, entorno)
        assert tipo in {t.value for t in pj.resistances}, entorno


# --- Shielding Storm (10) ----------------------------------------------------

def test_shielding_storm_otorga_la_resistencia_a_los_aliados():
    pj = _pj(level=10)
    aliado = _aliado()
    _furia(pj, 10, "desert", seed=11, combatants=[pj, aliado])
    assert "fire" in {t.value for t in aliado.resistances}
    assert "fire" in {t.value for t in pj.resistances}  # ya la tenía


def test_shielding_storm_no_quita_resistencias_ajenas():
    pj = _pj(level=10)
    con_fuego = _aliado(name="Con fuego")
    con_fuego.resistances = {parse_damage_type("fire")}  # ya la tenía
    sin_fuego = _aliado(name="Sin fuego")
    herald, _barb, ctx = _furia(
        pj, 10, "desert", seed=12,
        combatants=[pj, con_fuego, sin_fuego])
    assert "fire" in {t.value for t in sin_fuego.resistances}
    herald.on_rage_end(pj, ctx)
    # La suya (concedida por nosotros) se retira; la ajena se conserva.
    assert "fire" not in {t.value for t in sin_fuego.resistances}
    assert "fire" in {t.value for t in con_fuego.resistances}


def test_las_resistencias_concedidas_tambien_se_retiran_en_reset():
    pj = _pj(level=10)
    aliado = _aliado()
    _furia(pj, 10, "desert", seed=13, combatants=[pj, aliado])
    assert "fire" in {t.value for t in aliado.resistances}
    pj.reset()
    assert "fire" not in {t.value for t in aliado.resistances}


# --- Raging Storm (14) -------------------------------------------------------

def test_raging_storm_del_desierto_usa_la_reaccion_y_mata_con_mitad(monkeypatch):
    _fijar_fallo_reaccion(monkeypatch)
    pj = _pj(level=14)
    enemigo = _mon()
    herald, _barb, ctx = _furia(pj, 14, "desert", seed=14,
                                combatants=[pj, enemigo])
    hp_aura = enemigo.hp  # el aura del desierto ya le ha quitado PV
    herald.after_being_hit(pj, enemigo, AttackRange.MELEE, ctx)
    assert enemigo.hp == hp_aura - (14 // 2)  # mitad del nivel, hacia abajo
    hp_tras = enemigo.hp
    # Una reacción por ronda: el segundo impacto ya no dispara nada.
    herald.after_being_hit(pj, enemigo, AttackRange.MELEE, ctx)
    assert enemigo.hp == hp_tras


def test_raging_storm_del_mar_derriba_al_fallar(monkeypatch):
    _fijar_fallo_reaccion(monkeypatch)
    pj = _pj(level=14)
    enemigo = _mon()
    herald, _barb, ctx = _furia(pj, 14, "sea", seed=15,
                                combatants=[pj, enemigo])
    hp_aura = enemigo.hp  # la salvación del aura marina ya le ha tirado
    herald.after_being_hit(pj, enemigo, AttackRange.MELEE, ctx)
    assert Condition.PRONE in enemigo.conditions.active()
    assert enemigo.hp == hp_aura  # la salvación solo derriba, no daña


def test_raging_storm_no_dispara_sin_furia(monkeypatch):
    _fijar_fallo_reaccion(monkeypatch)
    pj = _pj(level=14)
    enemigo = _mon()
    herald = _herald(pj, 14, "desert")
    ctx = _ctx(pj, [pj, enemigo], seed=16)
    herald.after_being_hit(pj, enemigo, AttackRange.MELEE, ctx)
    assert enemigo.hp == 500
    assert pj.state.reaction_used is False  # ni siquiera se gasta


def test_raging_storm_tundra_registra_la_velocidad_cero_como_dato(monkeypatch):
    _fijar_fallo_reaccion(monkeypatch)
    pj = _pj(level=14)
    enemigo = _mon()
    herald, _barb, ctx = _furia(pj, 14, "tundra", seed=17,
                                combatants=[pj, enemigo])
    assert herald.velocidad_cero is enemigo
    assert any("velocidad 0" in linea for linea in ctx.log)
    herald.on_turn_start(pj, ctx)  # hasta el inicio del siguiente turno
    assert herald.velocidad_cero is None


# --- Niveles inferiores ------------------------------------------------------

def test_nivel_3_no_recibe_storm_soul_ni_shielding_ni_raging():
    pj = _pj(level=3)
    aliado = _aliado()
    enemigo = _mon()
    herald, _barb, ctx = _furia(pj, 3, "desert", seed=18,
                                combatants=[pj, aliado, enemigo])
    assert not pj.resistances  # Storm Soul es nivel 6
    assert not aliado.resistances  # Shielding Storm es nivel 10
    hp_aura = enemigo.hp  # el aura del desierto sí le ha quitado PV
    herald.after_being_hit(pj, enemigo, AttackRange.MELEE, ctx)
    assert enemigo.hp == hp_aura  # Raging Storm es nivel 14


def test_nivel_6_no_recibe_shielding_ni_raging():
    pj = _pj(level=6)
    aliado = _aliado()
    enemigo = _mon()
    herald, _barb, ctx = _furia(pj, 6, "desert", seed=19,
                                combatants=[pj, aliado, enemigo])
    assert pj.resistances  # Storm Soul sí
    assert not aliado.resistances  # Shielding no
    hp_aura = enemigo.hp
    herald.after_being_hit(pj, enemigo, AttackRange.MELEE, ctx)
    assert enemigo.hp == hp_aura  # Raging no


def test_nivel_10_no_recibe_raging_storm_tundra():
    pj = _pj(level=10)
    enemigo = _mon()
    herald, _barb, _ctx_ = _furia(pj, 10, "tundra", seed=20,
                                  combatants=[pj, enemigo])
    assert herald.velocidad_cero is None  # Raging Storm es nivel 14


# --- Determinismo ------------------------------------------------------------

def test_la_misma_semilla_produce_el_mismo_resultado_en_el_mar():
    pj1 = _pj(level=3)
    enemigo1 = _mon()
    _furia(pj1, 3, "sea", seed=42, combatants=[pj1, enemigo1])
    pj2 = _pj(level=3)
    enemigo2 = _mon()
    _furia(pj2, 3, "sea", seed=42, combatants=[pj2, enemigo2])
    assert enemigo1.hp == enemigo2.hp
    # Y con otra semilla distinta el resultado sigue siendo reproducible.
    pj3 = _pj(level=3)
    enemigo3 = _mon()
    _furia(pj3, 3, "sea", seed=42, combatants=[pj3, enemigo3])
    assert enemigo3.hp == enemigo1.hp

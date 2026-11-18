"""Tests de la subclase Path of the Wild Heart del bárbaro (PHB 2024).

Cubre el hook ``grant_attack_modifiers`` (no regresión), la tabla de
rasgos, Bear/Eagle/Wolf (Rage of the Wilds), Lion/Ram (Power of the
Wilds), la renovación de opciones por activación, los niveles
inferiores y la reproducibilidad.
"""
from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from dnd_sim import (
    Abilities, Attack, BarbarianFeatures, D20Result, Monster,
    PlayerCharacter, RollMode, apply_barbarian, apply_class,
    parse_damage_type,
)
from dnd_sim.core.enums import AttackRange
from dnd_sim.engine.combat import attack_roll
from dnd_sim.rules.classes.barbarian import BARBARIAN_CLASS
from dnd_sim.rules.classes.barbarian.subclasses import wild_heart as wh
from dnd_sim.rules.classes.barbarian.subclasses.wild_heart import (
    POWER_OPTIONS, RAGE_OPTIONS, WILD_HEART_FEATURES, WildHeartFeatures,
    apply_wild_heart,
)
from dnd_sim.rules.conditions import Condition
from dnd_sim.rules.roll_modifiers import attack_modifiers
from dnd_sim.rules.traits import HOOK_NAMES, hooks

_LOBO = "Lobo (Corazón Salvaje)"
_LEON = "León (Corazón Salvaje)"


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


def _aliado(name: str = "Aliado") -> PlayerCharacter:
    return PlayerCharacter(name=name, max_hp=400, ac=14, level=5,
                           abilities=_abilities(),
                           attacks=[Attack("Espada larga", "1d8",
                                           ability="str")])


def _ctx(actor, combatants, seed=0):
    return SimpleNamespace(actor=actor, combatants=list(combatants),
                           rng=random.Random(seed), log=[], round=1)


def _wild(pj, level):
    """Aplica clase + subclase y devuelve el rasgo."""
    apply_barbarian(pj, level=level)
    return apply_wild_heart(pj, level=level)


def _barbaro(pj) -> BarbarianFeatures:
    return next(t for t in pj.traits if isinstance(t, BarbarianFeatures))


def _furia(pj, level, seed=0):
    """Wild Heart aplicado, Furia activa y on_rage_start ejecutado."""
    trait = _wild(pj, level)
    barb = _barbaro(pj)
    barb.activate(1)
    ctx = _ctx(pj, [pj], seed)
    trait.on_rage_start(pj, ctx)
    return trait, barb, ctx


def _pick_fijo(rage="bear", power="ram", decision="si"):
    """Sustituye wild_heart.pick: opciones fijas y decisión «sí»."""
    def espia(rng, opciones):
        ops = tuple(opciones)
        if ops == ("no", "si"):
            return decision
        if any(o in RAGE_OPTIONS for o in ops):
            return rage
        if any(o in POWER_OPTIONS for o in ops):
            return power
        return ops[0]
    return espia


# --- No regresión del hook grant_attack_modifiers ----------------------------

def test_el_motor_reconoce_el_hook_grant_attack_modifiers():
    pj = _pj()
    apply_barbarian(pj, level=5)
    assert "grant_attack_modifiers" in HOOK_NAMES
    # Sin subclase que lo sobrescriba, el despacho no devuelve rasgos.
    assert hooks(pj.traits, "grant_attack_modifiers") == []


def test_sin_subclase_los_ataques_no_consumen_rng_ni_cambian_el_modo():
    # PJ sin subclase ni rasgos que sobrescriban el hook.
    atacante = _aliado()
    objetivo = _mon()
    atk = atacante.attacks[0]
    ctx = _ctx(atacante, [atacante, objetivo])
    modo_directo = attack_modifiers(atacante, objetivo, atk,
                                    AttackRange.MELEE).mode
    rng = random.Random(7)
    esperado = random.Random(7)
    mods = attack_modifiers(atacante, objetivo, atk, AttackRange.MELEE,
                            ctx=ctx, rng=rng)
    # Mismo resultado que sin contexto y el RNG intacto.
    assert mods.mode is modo_directo
    assert rng.random() == esperado.random()


# --- Tabla y aplicación ------------------------------------------------------

def test_tabla_de_rasgos_por_nivel():
    assert WILD_HEART_FEATURES == {
        3: ("Animal Speaker", "Rage of the Wilds"),
        6: ("Aspect of the Wilds",),
        10: ("Nature Speaker",),
        14: ("Power of the Wilds",),
    }


def test_apply_requiere_clase_barbara():
    with pytest.raises(ValueError, match="apply_barbarian"):
        apply_wild_heart(_pj())


def test_apply_anade_trait_sin_acciones():
    pj = _pj(level=5)
    apply_barbarian(pj, level=5)
    acciones_antes = len(pj.actions)
    trait = apply_wild_heart(pj)
    assert isinstance(trait, WildHeartFeatures)
    assert trait.level == 5
    assert trait in pj.traits
    assert trait.aspecto == "owl"  # elección por defecto de Aspect
    # Las opciones se eligen solas al entrar en Furia: no hay acción.
    assert len(pj.actions) == acciones_antes


def test_apply_class_registra_wild_heart():
    assert "wild_heart" in BARBARIAN_CLASS.subclasses
    pj = _pj(level=5)
    apply_class(pj, "barbarian", "wild_heart")
    assert any(isinstance(t, WildHeartFeatures) for t in pj.traits)


def test_apply_acepta_el_aspecto_de_nivel_6():
    pj = _pj(level=6)
    apply_barbarian(pj, level=6)
    trait = apply_wild_heart(pj, aspecto="panther")
    assert trait.aspecto == "panther"
    pj2 = _pj(level=6)
    apply_barbarian(pj2, level=6)
    with pytest.raises(ValueError, match="Aspecto"):
        apply_wild_heart(pj2, aspecto="dragon")


# --- Bear: Rage of the Wilds (3) --------------------------------------------

def test_bear_concede_las_resistencias_elementales_durante_la_furia(
        monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="bear"))
    pj = _pj(level=3)
    _furia(pj, 3, seed=1)
    for texto in ("acid", "cold", "fire", "lightning", "poison", "thunder"):
        assert parse_damage_type(texto) in pj.resistances


def test_bear_no_concede_los_tipos_excluidos_ni_los_fisicos(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="bear"))
    pj = _pj(level=3)
    _furia(pj, 3, seed=1)
    # Fuerza/necrótico/psíquico/radiante: excluidos por la regla.
    for texto in ("force", "necrotic", "psychic", "radiant"):
        assert parse_damage_type(texto) not in pj.resistances
    # B/P/S: ya los recorta la Furia base (misma ventana); añadirlos al
    # set duplicaría el recorte. No se tocan.
    for texto in ("bludgeoning", "piercing", "slashing"):
        assert parse_damage_type(texto) not in pj.resistances


def test_bear_retira_las_resistencias_al_terminar_la_furia(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="bear"))
    pj = _pj(level=3)
    trait, _barb, ctx = _furia(pj, 3, seed=1)
    assert parse_damage_type("fire") in pj.resistances
    trait.on_rage_end(pj, ctx)
    assert parse_damage_type("fire") not in pj.resistances


def test_bear_no_quita_una_resistencia_previa_del_pj(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="bear"))
    pj = _pj(level=3)
    pj.resistances = {parse_damage_type("fire")}  # ya la tenía
    trait, _barb, ctx = _furia(pj, 3, seed=1)
    assert parse_damage_type("cold") in pj.resistances  # sí concedida
    trait.on_rage_end(pj, ctx)
    assert parse_damage_type("fire") in pj.resistances  # previa intacta
    assert parse_damage_type("cold") not in pj.resistances


def test_bear_revoca_tambien_en_reset(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="bear"))
    pj = _pj(level=3)
    _furia(pj, 3, seed=1)
    assert parse_damage_type("fire") in pj.resistances
    pj.reset()
    assert parse_damage_type("fire") not in pj.resistances


# --- Eagle: sin efecto mecánico ---------------------------------------------

def test_eagle_no_tiene_efecto_mecanico(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="eagle"))
    pj = _pj(level=3)
    trait, _barb, _ctx_ = _furia(pj, 3, seed=1)
    assert trait.opcion_rage == "eagle"
    # Sin posiciones: Disengage/Dash no hacen nada; nada más cambia.
    assert pj.resistances == set()
    assert not pj.conditions.active()


# --- Wolf: ventaja a los aliados (3) ----------------------------------------

def _mods(atacante, objetivo, ctx, rango=AttackRange.MELEE):
    ataques = list(getattr(atacante, "attacks", None) or [])
    atk = ataques[0] if ataques else Attack("Golpe", "1d6", ability="str")
    return attack_modifiers(atacante, objetivo, atk, rango,
                            ctx=ctx, rng=ctx.rng)


def test_wolf_da_ventaja_a_los_aliados_contra_enemigos_cercanos(
        monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="wolf"))
    pj = _pj(level=3)
    _furia(pj, 3, seed=2)
    aliado, enemigo = _aliado(), _mon()
    ctx = _ctx(pj, [pj, aliado, enemigo], seed=2)
    mods = _mods(aliado, enemigo, ctx)
    assert _LOBO in mods.advantage_sources
    assert mods.mode is RollMode.ADVANTAGE


def test_wolf_no_da_ventaja_al_propio_barbaro(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="wolf"))
    pj = _pj(level=3)
    _furia(pj, 3, seed=2)
    enemigo = _mon()
    ctx = _ctx(pj, [pj, enemigo], seed=2)
    mods = _mods(pj, enemigo, ctx)
    assert _LOBO not in mods.advantage_sources


def test_wolf_no_da_ventaja_sin_furia(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="wolf"))
    pj = _pj(level=3)
    _wild(pj, 3)  # aplicado pero sin entrar en Furia
    aliado, enemigo = _aliado(), _mon()
    ctx = _ctx(pj, [pj, aliado, enemigo], seed=2)
    mods = _mods(aliado, enemigo, ctx)
    assert _LOBO not in mods.advantage_sources


def test_wolf_tambien_da_ventaja_en_ataques_a_distancia(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="wolf"))
    pj = _pj(level=3)
    _furia(pj, 3, seed=2)
    aliado, enemigo = _aliado(), _mon()
    ctx = _ctx(pj, [pj, aliado, enemigo], seed=2)
    mods = _mods(aliado, enemigo, ctx, rango=AttackRange.RANGED)
    assert _LOBO in mods.advantage_sources


def test_wolf_sin_enemigo_en_rango_no_da_ventaja(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="wolf"))
    monkeypatch.setattr(wh, "WILD_HEART_COVERAGE_PROBABILITY", 0.0)
    pj = _pj(level=3)
    _furia(pj, 3, seed=2)
    aliado, enemigo = _aliado(), _mon()
    ctx = _ctx(pj, [pj, aliado, enemigo], seed=2)
    mods = _mods(aliado, enemigo, ctx)
    assert _LOBO not in mods.advantage_sources


# --- Lion: desventaja de los enemigos (14) ----------------------------------

def test_leon_da_desventaja_a_los_enemigos_contra_otros_objetivos(
        monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="bear", power="lion"))
    pj = _pj(level=14)
    _furia(pj, 14, seed=3)
    aliado, enemigo = _aliado(), _mon()
    ctx = _ctx(pj, [pj, aliado, enemigo], seed=3)
    mods = _mods(enemigo, aliado, ctx)
    assert _LEON in mods.disadvantage_sources
    assert mods.mode is RollMode.DISADVANTAGE


def test_leon_no_da_desventaja_contra_el_propio_barbaro(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="bear", power="lion"))
    pj = _pj(level=14)
    _furia(pj, 14, seed=3)
    enemigo = _mon()
    ctx = _ctx(pj, [pj, enemigo], seed=3)
    mods = _mods(enemigo, pj, ctx)
    assert _LEON not in mods.disadvantage_sources


def test_leon_no_da_desventaja_contra_otro_con_el_mismo_beneficio(
        monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="bear", power="lion"))
    pj = _pj(level=14)
    _furia(pj, 14, seed=3)
    # Otro Wild Heart nivel 14 en Furia con opción León (protegido).
    otro = PlayerCharacter(name="Thor 2", max_hp=500, ac=15, level=14,
                           abilities=_abilities(),
                           attacks=[Attack("Hacha", "1d12", ability="str")])
    trait_otro = _wild(otro, 14)
    _barbaro(otro).activate(1)
    ctx_otro = _ctx(otro, [otro], seed=9)
    trait_otro.on_rage_start(otro, ctx_otro)
    assert trait_otro.opcion_power == "lion"
    enemigo = _mon()
    ctx = _ctx(pj, [pj, otro, enemigo], seed=3)
    mods = _mods(enemigo, otro, ctx)
    assert _LEON not in mods.disadvantage_sources
    # Mientras tanto, un aliado normal sí recibe la desventaja.
    aliado = _aliado()
    ctx2 = _ctx(pj, [pj, aliado, enemigo], seed=3)
    assert _LEON in _mods(enemigo, aliado, ctx2).disadvantage_sources


# --- Ram: derribar al acertar (14) ------------------------------------------

def test_ram_derriba_al_acertar_en_cuerpo_a_cuerpo(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="bear", power="ram"))
    pj = _pj(level=14)
    trait, _barb, ctx = _furia(pj, 14, seed=4)
    objetivo = _mon()
    bonus = trait.extra_attack_damage(pj, objetivo, AttackRange.MELEE,
                                      False, ctx, ctx.rng)
    assert bonus == 0  # no añade daño: el efecto es la condición
    assert Condition.PRONE in objetivo.conditions.active()


def test_ram_no_derriba_a_criaturas_de_tamano_huge(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="bear", power="ram"))
    pj = _pj(level=14)
    trait, _barb, ctx = _furia(pj, 14, seed=4)
    objetivo = _mon()
    objetivo.size = "huge"
    assert trait.extra_attack_damage(pj, objetivo, AttackRange.MELEE,
                                     False, ctx, ctx.rng) == 0
    assert Condition.PRONE not in objetivo.conditions.active()


def test_ram_no_derriba_en_ataques_a_distancia(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="bear", power="ram"))
    pj = _pj(level=14)
    trait, _barb, ctx = _furia(pj, 14, seed=4)
    objetivo = _mon()
    assert trait.extra_attack_damage(pj, objetivo, AttackRange.RANGED,
                                     False, ctx, ctx.rng) == 0
    assert Condition.PRONE not in objetivo.conditions.active()


def test_ram_no_derriba_sin_furia(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="bear", power="ram"))
    pj = _pj(level=14)
    trait, barb, ctx = _furia(pj, 14, seed=4)
    barb.rage_active = False
    objetivo = _mon()
    assert trait.extra_attack_damage(pj, objetivo, AttackRange.MELEE,
                                     False, ctx, ctx.rng) == 0
    assert Condition.PRONE not in objetivo.conditions.active()


def test_ram_no_derriba_si_el_ataque_falla(monkeypatch):
    import dnd_sim.engine.combat.attack as combat_mod

    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="bear", power="ram"))

    def fijar(valor):
        def espia(rng, mode=RollMode.NORMAL, **kw):
            return D20Result(value=valor, rolls=[valor, valor], mode=mode)
        monkeypatch.setattr(combat_mod, "roll_d20", espia)

    pj = _pj(level=14)
    _furia(pj, 14, seed=4)
    objetivo = _mon()
    ctx = _ctx(pj, [pj, objetivo], seed=4)
    # Falla (d20 = 1): no hay golpe, no hay Ram.
    fijar(1)
    attack_roll(pj, objetivo, pj.attacks[0], random.Random(5),
                log=[], ctx=ctx)
    assert Condition.PRONE not in objetivo.conditions.active()
    # Acierta (d20 = 20): Ram derriba.
    fijar(20)
    attack_roll(pj, objetivo, pj.attacks[0], random.Random(5),
                log=[], ctx=ctx)
    assert Condition.PRONE in objetivo.conditions.active()


# --- Ciclo de vida de las opciones ------------------------------------------

def test_las_opciones_se_eligen_de_nuevo_en_cada_activacion(
        monkeypatch):
    secuencia = iter(["wolf", "bear"])

    def espia(rng, opciones):
        ops = tuple(opciones)
        if ops == ("no", "si"):
            return "no"
        if any(o in RAGE_OPTIONS for o in ops):
            return next(secuencia)
        return ops[0]

    monkeypatch.setattr(wh, "pick", espia)
    pj = _pj(level=3)
    trait, barb, ctx = _furia(pj, 3, seed=5)
    assert trait.opcion_rage == "wolf"
    trait.on_rage_end(pj, ctx)
    assert trait.opcion_rage is None
    # Segunda activación: se vuelve a elegir (siguiente de la lista).
    barb.activate(1)
    ctx2 = _ctx(pj, [pj], seed=6)
    trait.on_rage_start(pj, ctx2)
    assert trait.opcion_rage == "bear"


def test_los_niveles_inferiores_no_reciben_power_of_the_wilds(monkeypatch):
    monkeypatch.setattr(wh, "pick", _pick_fijo(rage="bear", power="ram"))
    for nivel in (3, 6, 10):
        pj = _pj(level=nivel)
        trait, _barb, ctx = _furia(pj, nivel, seed=6)
        assert trait.opcion_power is None  # Power es nivel 14
        objetivo = _mon()
        assert trait.extra_attack_damage(pj, objetivo, AttackRange.MELEE,
                                         False, ctx, ctx.rng) == 0
        assert Condition.PRONE not in objetivo.conditions.active()


def test_la_misma_semilla_elige_las_mismas_opciones():
    pj1 = _pj(level=14)
    trait1, _b1, ctx1 = _furia(pj1, 14, seed=42)
    pj2 = _pj(level=14)
    trait2, _b2, ctx2 = _furia(pj2, 14, seed=42)
    assert trait1.opcion_rage == trait2.opcion_rage
    assert trait1.opcion_power == trait2.opcion_power
    # Misma tirada para la decisión de Ram: mismo resultado.
    obj1, obj2 = _mon(), _mon()
    trait1.extra_attack_damage(pj1, obj1, AttackRange.MELEE, False,
                               ctx1, random.Random(9))
    trait2.extra_attack_damage(pj2, obj2, AttackRange.MELEE, False,
                               ctx2, random.Random(9))
    derribado1 = Condition.PRONE in obj1.conditions.active()
    derribado2 = Condition.PRONE in obj2.conditions.active()
    assert derribado1 == derribado2


def test_aspect_of_the_wilds_no_tiene_efecto_mecanico():
    pj = _pj(level=6)
    trait = _wild(pj, 6)
    # Dato permanente: no añade resistencias, acciones ni condiciones.
    assert trait.aspecto == "owl"
    assert pj.resistances == set()
    assert not pj.conditions.active()

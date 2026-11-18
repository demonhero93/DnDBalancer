"""Features de la subclase Path of Wild Magic del bárbaro (TCE 2020).

Cubre la tabla de rasgos, la tabla Wild Surge (8 entradas), Shadowy
Tendrils, Intangible Spirit, Magic Infusion, Retribution, Unstable
Backlash (impacto y salvación fallida), Controlled Surge, niveles
inferiores, el hook after_failed_save (no regresión) y la
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
from dnd_sim.model.actions import ActionType
from dnd_sim.rules.classes.barbarian import BARBARIAN_CLASS
from dnd_sim.rules.classes.barbarian.subclasses import wild_magic as wm
from dnd_sim.rules.classes.barbarian.subclasses.wild_magic import (
    WILD_MAGIC_FEATURES, WILD_SURGE_TABLE, WildMagicFeatures,
    WildSurgeAction, apply_wild_magic,
)
from dnd_sim.rules.saves import registrar_resistencia, saving_throw
from dnd_sim.rules.traits.base import HOOK_NAMES, hooks


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


def _wild(pj, level):
    """Aplica clase + subclase y devuelve el rasgo."""
    apply_barbarian(pj, level=level)
    return apply_wild_magic(pj, level=level)


def _barbaro(pj) -> BarbarianFeatures:
    return next(t for t in pj.traits if isinstance(t, BarbarianFeatures))


def _ctx(actor, combatants, seed=0):
    return SimpleNamespace(actor=actor, combatants=list(combatants),
                           rng=random.Random(seed), log=[], round=1)


def _furia(pj, level, seed=0):
    """Wild Magic aplicado, Furia activa y on_rage_start ejecutado."""
    magia = _wild(pj, level)
    barb = _barbaro(pj)
    barb.activate(1)
    ctx = _ctx(pj, [pj], seed)
    magia.on_rage_start(pj, ctx)
    return magia, barb, ctx


def _con_efecto(nombre, decision=None, segunda=False):
    """pick que fuerza ``nombre`` en la tabla y ``decision`` en ("no","si").

    ``segunda=True`` fuerza la segunda entrada en la elección final de
    Controlled Surge (tupla de dos entradas de tabla).
    """
    def espia(rng, opciones):
        if opciones is wm.WILD_SURGE_TABLE:
            for entrada in opciones:
                if entrada[0] == nombre:
                    return entrada
        if decision is not None and opciones == ("no", "si"):
            return decision
        if (segunda and len(opciones) == 2
                and isinstance(opciones[0], tuple)):
            return opciones[1]
        return pick_real(rng, opciones)
    return espia


def _con_cola(efectos, decision=None, segunda=False):
    """pick que consume la cola de ``efectos`` en cada tirada de tabla."""
    cola = list(efectos)

    def espia(rng, opciones):
        if opciones is wm.WILD_SURGE_TABLE and cola:
            nombre = cola.pop(0)
            for entrada in opciones:
                if entrada[0] == nombre:
                    return entrada
        if decision is not None and opciones == ("no", "si"):
            return decision
        if (segunda and len(opciones) == 2
                and isinstance(opciones[0], tuple)):
            return opciones[1]
        return pick_real(rng, opciones)
    return espia


def _salvacion(salva: bool):
    def stub(target, ability, dc, rng, mode=None, *, kind=None,
             magical=False):
        total = 30 if salva else 1
        return SaveResult(ability=ability, dc=dc, rolls=[total], bonus=0,
                          total=total, success=salva,
                          mode=RollMode.NORMAL)
    return stub


# --- Tabla y aplicación ------------------------------------------------------

def test_wild_magic_features_por_nivel():
    assert WILD_MAGIC_FEATURES == {
        3: ("Magic Awareness", "Wild Surge"),
        6: ("Bolstering Magic",),
        10: ("Unstable Backlash",),
        14: ("Controlled Surge",),
    }


def test_las_ocho_entradas_de_la_tabla_tienen_nombre_y_funcion():
    assert len(WILD_SURGE_TABLE) == 8
    for nombre, funcion in WILD_SURGE_TABLE:
        assert isinstance(nombre, str) and nombre
        assert callable(funcion)


def test_apply_requiere_clase_barbara():
    import pytest
    with pytest.raises(ValueError, match="apply_barbarian"):
        apply_wild_magic(_pj())


def test_apply_anade_trait_y_accion():
    pj = _pj(level=5)
    apply_barbarian(pj, level=5)
    sub = apply_wild_magic(pj)
    assert isinstance(sub, WildMagicFeatures)
    assert sub.level == 5
    assert sub in pj.traits
    accion = next(a for a in pj.actions
                  if isinstance(a, WildSurgeAction))
    assert accion.action_type is ActionType.BONUS_ACTION
    assert accion.name == "Espíritu intangible"
    assert accion.usage is None


def test_apply_class_registra_wild_magic():
    assert "wild_magic" in BARBARIAN_CLASS.subclasses
    # No confunde con wild_heart ni beast.
    assert "wild_heart" in BARBARIAN_CLASS.subclasses
    assert "beast" in BARBARIAN_CLASS.subclasses
    pj = _pj(level=5)
    apply_class(pj, "barbarian", "wild_magic")
    assert any(isinstance(t, WildMagicFeatures) for t in pj.traits)


# --- Wild Surge: activación --------------------------------------------------

def test_al_entrar_en_furia_tira_en_la_tabla():
    pj = _pj(level=3)
    magia, _barb, _ctx_ = _furia(pj, 3, seed=11)
    nombres = {nombre for nombre, _ in WILD_SURGE_TABLE}
    assert magia.efecto in nombres


def test_el_efecto_se_renueva_en_cada_activacion(monkeypatch):
    monkeypatch.setattr(wm, "pick",
                        _con_cola(["Teleport", "Flowers and Vines"]))
    pj = _pj(level=3)
    magia, barb, ctx = _furia(pj, 3, seed=1)
    assert magia.efecto == "Teleport"
    magia.on_rage_end(pj, ctx)
    assert magia.efecto is None
    barb.activate(2)
    magia.on_rage_start(pj, ctx)
    assert magia.efecto == "Flowers and Vines"


def test_sin_rng_no_se_tira_en_la_tabla():
    pj = _pj(level=3)
    magia = _wild(pj, 3)
    barb = _barbaro(pj)
    barb.activate(1)
    ctx = SimpleNamespace(actor=pj, combatants=[pj], rng=None, log=[],
                          round=1)
    magia.on_rage_start(pj, ctx)
    assert magia.efecto is None


def test_solo_el_nivel_14_tira_dos_veces(monkeypatch):
    cont = {"n": 0}

    def espia(rng, opciones):
        if opciones is wm.WILD_SURGE_TABLE:
            cont["n"] += 1
        return pick_real(rng, opciones)

    monkeypatch.setattr(wm, "pick", espia)
    _pj10 = _pj(level=10)
    _furia(_pj10, 10, seed=1)
    assert cont["n"] == 1
    _pj14 = _pj(level=14)
    _furia(_pj14, 14, seed=1)
    assert cont["n"] == 3  # 1 en el nivel 10 + 2 en el nivel 14


# --- Shadowy Tendrils ---------------------------------------------------------

def test_shadowy_tendrils_dana_y_da_pv_temporales(monkeypatch):
    monkeypatch.setattr(wm, "saving_throw", _salvacion(salva=False))
    monkeypatch.setattr(wm, "roll_dice", lambda expr, rng, crit=False: 7)
    pj = _pj(level=3)
    objetivo = _mon()
    magia = _wild(pj, 3)
    barb = _barbaro(pj)
    barb.activate(1)
    ctx = _ctx(pj, [pj, objetivo], seed=2)
    wm._sombra(magia, pj, ctx)
    assert objetivo.hp == 500 - 7  # fallo: 1d12 fijado a 7 de necrótico
    assert pj.temp_hp == 7


def test_shadowy_tendrils_con_salvacion_exitosa_no_dana(monkeypatch):
    monkeypatch.setattr(wm, "saving_throw", _salvacion(salva=True))
    monkeypatch.setattr(wm, "roll_dice", lambda expr, rng, crit=False: 7)
    pj = _pj(level=3)
    objetivo = _mon()
    magia = _wild(pj, 3)
    barb = _barbaro(pj)
    barb.activate(1)
    ctx = _ctx(pj, [pj, objetivo], seed=3)
    wm._sombra(magia, pj, ctx)
    assert objetivo.hp == 500  # éxito: sin daño
    assert pj.temp_hp == 7     # los PV temporales se conceden igual


def test_los_pv_temporales_no_se_acumulan(monkeypatch):
    monkeypatch.setattr(wm, "saving_throw", _salvacion(salva=True))
    monkeypatch.setattr(wm, "roll_dice", lambda expr, rng, crit=False: 7)
    pj = _pj(level=3)
    pj.temp_hp = 20
    magia = _wild(pj, 3)
    barb = _barbaro(pj)
    barb.activate(1)
    ctx = _ctx(pj, [pj], seed=3)
    wm._sombra(magia, pj, ctx)
    assert pj.temp_hp == 20  # se queda el mayor


# --- Efectos sin efecto mecánico ---------------------------------------------

def test_los_efectos_sin_efecto_no_cambian_estado(monkeypatch):
    for nombre in ("Teleport", "Bolstering Magic", "Flowers and Vines",
                   "Pendiente"):
        monkeypatch.setattr(wm, "pick", _con_efecto(nombre))
        pj = _pj(level=3)
        objetivo = _mon()
        magia, _barb, ctx = _furia(pj, 3, seed=5)
        ctx.combatants = [pj, objetivo]
        magia.efecto = nombre
        assert magia.efecto == nombre
        assert objetivo.hp == 500
        assert pj.temp_hp == 0
        assert pj.resistances == set()
        magia.on_rage_end(pj, ctx)


# --- Intangible Spirit --------------------------------------------------------

def test_el_espiritu_solo_detona_con_ese_efecto():
    pj = _pj(level=3)
    magia, _barb, ctx = _furia(pj, 3, seed=4)
    objetivo = _mon()
    ctx.combatants = [pj, objetivo]
    accion = next(a for a in pj.actions
                  if isinstance(a, WildSurgeAction))
    # Sin el efecto activo (forzamos otro): no disponible.
    magia.efecto = "Teleport"
    assert accion.can_use(ctx) is False
    # Con el efecto y en Furia: disponible.
    magia.efecto = "Intangible Spirit"
    assert accion.can_use(ctx) is True
    # Fuera de Furia: no disponible.
    _barbaro_de_pj = _barbaro(pj)
    _barbaro_de_pj.rage_active = False
    assert accion.can_use(ctx) is False


def test_el_espiritu_detona_con_salvacion_de_des(monkeypatch):
    monkeypatch.setattr(wm, "saving_throw", _salvacion(salva=False))
    monkeypatch.setattr(wm, "roll_dice", lambda expr, rng, crit=False: 5)
    pj = _pj(level=3)
    objetivo = _mon()
    magia, _barb, ctx = _furia(pj, 3, seed=4)
    ctx.combatants = [pj, objetivo]
    magia.efecto = "Intangible Spirit"
    accion = next(a for a in pj.actions
                  if isinstance(a, WildSurgeAction))
    accion.execute(ctx)
    assert objetivo.hp == 500 - 5  # fallo: 1d6 de fuerza fijado a 5


# --- Magic Infusion ------------------------------------------------------------

def test_magic_infusion_marca_las_armas_como_magicas(monkeypatch):
    monkeypatch.setattr(wm, "pick", _con_efecto("Magic Infusion"))
    pj = _pj(level=3)
    _furia(pj, 3, seed=6)
    assert pj.attacks[0].magical is True


def test_magic_infusion_restaura_las_armas_al_terminar_la_furia(
        monkeypatch):
    monkeypatch.setattr(wm, "pick", _con_efecto("Magic Infusion"))
    pj = _pj(level=3)
    magia, _barb, ctx = _furia(pj, 3, seed=6)
    assert pj.attacks[0].magical is True
    magia.on_rage_end(pj, ctx)
    assert pj.attacks[0].magical is False


def test_magic_infusion_restaura_las_armas_en_reset(monkeypatch):
    monkeypatch.setattr(wm, "pick", _con_efecto("Magic Infusion"))
    pj = _pj(level=3)
    _furia(pj, 3, seed=6)
    assert pj.attacks[0].magical is True
    pj.reset()
    assert pj.attacks[0].magical is False


# --- Retribution ---------------------------------------------------------------

def test_retribucion_dania_al_atacante_con_el_dano_de_furia(monkeypatch):
    monkeypatch.setattr(wm, "pick",
                        _con_efecto("Retribution", decision="si"))
    pj = _pj(level=3)
    atacante = _mon()
    magia, _barb, ctx = _furia(pj, 3, seed=7)
    ctx.combatants = [pj, atacante]
    magia.after_being_hit(pj, atacante, AttackRange.MELEE, ctx)
    assert atacante.hp == 500 - rage_damage(3)


def test_retribucion_no_dania_sin_furia(monkeypatch):
    monkeypatch.setattr(wm, "pick",
                        _con_efecto("Retribution", decision="si"))
    pj = _pj(level=3)
    atacante = _mon()
    magia = _wild(pj, 3)  # sin activar Furia
    ctx = _ctx(pj, [pj, atacante], seed=7)
    magia.efecto = "Retribution"
    magia.after_being_hit(pj, atacante, AttackRange.MELEE, ctx)
    assert atacante.hp == 500


def test_retribucion_respeta_la_decision_de_no_usarla(monkeypatch):
    monkeypatch.setattr(wm, "pick",
                        _con_efecto("Retribution", decision="no"))
    pj = _pj(level=3)
    atacante = _mon()
    magia, _barb, ctx = _furia(pj, 3, seed=7)
    ctx.combatants = [pj, atacante]
    magia.after_being_hit(pj, atacante, AttackRange.MELEE, ctx)
    assert atacante.hp == 500


# --- Unstable Backlash ----------------------------------------------------------

def test_backlash_usa_la_reaccion_y_sustituye_el_efecto(monkeypatch):
    monkeypatch.setattr(wm, "pick",
                        _con_cola(["Retribution", "Teleport"],
                                  decision="si"))
    pj = _pj(level=10)
    atacante = _mon()
    magia, barb, ctx = _furia(pj, 10, seed=8)
    ctx.combatants = [pj, atacante]
    assert magia.efecto == "Retribution"
    magia.after_being_hit(pj, atacante, AttackRange.MELEE, ctx)
    assert pj.state.reaction_used is True
    assert magia.efecto == "Teleport"  # el efecto anterior terminó


def test_backlash_no_se_usa_sin_reaccion_disponible(monkeypatch):
    monkeypatch.setattr(wm, "pick",
                        _con_cola(["Retribution", "Teleport"],
                                  decision="si"))
    pj = _pj(level=10)
    atacante = _mon()
    magia, barb, ctx = _furia(pj, 10, seed=8)
    ctx.combatants = [pj, atacante]
    pj.state.reaction_used = True
    magia.after_being_hit(pj, atacante, AttackRange.MELEE, ctx)
    assert magia.efecto == "Retribution"  # sin reacción: no sustituye


def test_backlash_se_dispara_tras_fallar_una_salvacion(monkeypatch):
    monkeypatch.setattr(wm, "pick",
                        _con_cola(["Retribution", "Teleport"],
                                  decision="si"))
    pj = _pj(level=10)
    magia, _barb, ctx = _furia(pj, 10, seed=9)
    assert magia.efecto == "Retribution"
    fallo = SaveResult(ability="con", dc=13, rolls=[1], bonus=0, total=1,
                       success=False, mode=RollMode.NORMAL)
    magia.after_failed_save(pj, "con", fallo, ctx)
    assert pj.state.reaction_used is True
    assert magia.efecto == "Teleport"


def test_en_el_nivel_3_no_hay_backlash(monkeypatch):
    monkeypatch.setattr(wm, "pick",
                        _con_efecto("Retribution", decision="si"))
    pj = _pj(level=3)
    atacante = _mon()
    magia, _barb, ctx = _furia(pj, 3, seed=8)
    ctx.combatants = [pj, atacante]
    magia.after_being_hit(pj, atacante, AttackRange.MELEE, ctx)
    fallo = SaveResult(ability="con", dc=13, rolls=[1], bonus=0, total=1,
                       success=False, mode=RollMode.NORMAL)
    magia.after_failed_save(pj, "con", fallo, ctx)
    assert pj.state.reaction_used is False
    assert magia.efecto == "Retribution"  # sin re-tira (nivel < 10)


# --- Controlled Surge ------------------------------------------------------------

def test_controlled_surge_elige_uno_de_los_dos_efectos(monkeypatch):
    monkeypatch.setattr(wm, "pick",
                        _con_cola(["Shadowy Tendrils", "Teleport"],
                                  segunda=True))
    pj = _pj(level=14)
    magia, _barb, _ctx_ = _furia(pj, 14, seed=10)
    assert magia.efecto == "Teleport"  # se quedó con la segunda tirada


# --- Hook after_failed_save (no regresión) --------------------------------------

def test_el_hook_after_failed_save_esta_registrado():
    assert "after_failed_save" in HOOK_NAMES
    pj = _pj(level=3)
    apply_barbarian(pj)  # sin subclase
    assert hooks(pj.traits, "after_failed_save") == []


def test_sin_furia_el_backlash_no_consume_rng():
    pj_sin = _pj(level=3)
    apply_barbarian(pj_sin)
    pj_con = _pj(level=3)
    _wild(pj_con, 10)  # con Wild Magic pero SIN Furia
    rng1, rng2 = random.Random(3), random.Random(3)
    ctx1 = _ctx(pj_sin, [pj_sin], seed=3)
    ctx2 = _ctx(pj_con, [pj_con], seed=3)
    ctx1.rng, ctx2.rng = rng1, rng2
    for pj, ctx in ((pj_sin, ctx1), (pj_con, ctx2)):
        sr = saving_throw(pj, "dex", 40, ctx.rng)  # CD imposible: falla
        registrar_resistencia(ctx, pj, sr)
    assert rng1.getstate() == rng2.getstate()  # cero RNG nuevo


# --- Niveles inferiores ------------------------------------------------------------

def test_el_nivel_3_no_recibe_rasgos_superiores(monkeypatch):
    monkeypatch.setattr(wm, "pick", _con_efecto("Teleport"))
    pj = _pj(level=3)
    magia, _barb, ctx = _furia(pj, 3, seed=3)
    fallo = SaveResult(ability="con", dc=13, rolls=[1], bonus=0, total=1,
                       success=False, mode=RollMode.NORMAL)
    magia.after_failed_save(pj, "con", fallo, ctx)
    assert pj.state.reaction_used is False  # Unstable Backlash es nivel 10
    # Controlled Surge (14): una sola tirada ya comprobada arriba.


# --- Determinismo -------------------------------------------------------------------

def test_la_misma_semilla_elige_el_mismo_efecto():
    pj1 = _pj(level=3)
    objetivo1 = _mon()
    magia1, _b1, ctx1 = _furia(pj1, 3, seed=42)
    ctx1.combatants = [pj1, objetivo1]
    pj2 = _pj(level=3)
    objetivo2 = _mon()
    magia2, _b2, ctx2 = _furia(pj2, 3, seed=42)
    ctx2.combatants = [pj2, objetivo2]
    assert magia1.efecto == magia2.efecto
    # Misma semilla: mismo PV final del objetivo si el efecto hace daño.
    wm._sombra(magia1, pj1, ctx1)
    wm._sombra(magia2, pj2, ctx2)
    assert objetivo1.hp == objetivo2.hp
    assert pj1.temp_hp == pj2.temp_hp

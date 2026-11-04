"""Features de la subclase Path of the Zealot del bárbaro (PHB 2024).

Cubre la tabla de rasgos, Divine Fury (pago único por turno con
necrótico/radiante), Warrior of the Gods (reserva 4/5/6/7 y curación),
Fanatical Focus (repetición de salvación vía after_failed_save),
Zealous Presence (ventaja en ataques y salvaciones de aliados con el
hook nuevo grant_save_modifiers), Rage of the Gods (resistencias de la
forma y Revivification), niveles inferiores, la no regresión de los
hooks nuevos (consumo de RNG idéntico sin la subclase) y la
reproducibilidad con semilla fija.
"""
from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from dnd_sim import (
    Abilities, Attack, BarbarianFeatures, Monster, PlayerCharacter,
    RollMode, SaveResult, TurnResources, apply_barbarian, apply_class,
    attack_modifiers, rage_damage, saving_throw,
)
from dnd_sim.core.enums import AttackRange
from dnd_sim.engine.combat import attack_roll
from dnd_sim.rules.classes.barbarian import BARBARIAN_CLASS
from dnd_sim.rules.classes.barbarian.subclasses import zealot as ze
from dnd_sim.rules.classes.barbarian.subclasses.zealot import (
    ZEALOT_FEATURES, WarriorHealAction, ZealotFeatures,
    ZealousPresenceAction, apply_zealot,
)
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


def _aliado(level: int = 5, hp: int = 100) -> PlayerCharacter:
    aliado = PlayerCharacter(name="Aliado", max_hp=500, ac=15, level=level,
                             abilities=_abilities())
    aliado.hp = hp
    return aliado


def _zeal(pj, level):
    """Aplica clase + subclase y devuelve el rasgo."""
    apply_barbarian(pj, level=level)
    return apply_zealot(pj, level=level)


def _barbaro(pj) -> BarbarianFeatures:
    return next(t for t in pj.traits if isinstance(t, BarbarianFeatures))


def _trait(pj) -> ZealotFeatures:
    return next(t for t in pj.traits if isinstance(t, ZealotFeatures))


def _ctx(actor, combatants, seed=0):
    return SimpleNamespace(
        actor=actor,
        combatants=list(combatants),
        round=1, rng=random.Random(seed), log=[],
        resources=TurnResources(), verbose=False,
    )


def _furia(pj, level, seed=0):
    """Zealot aplicado, Furia activa y on_rage_start ejecutado."""
    zeal = _zeal(pj, level)
    barb = _barbaro(pj)
    barb.activate(1)
    ctx = _ctx(pj, [pj], seed)
    zeal.on_rage_start(pj, ctx)
    return zeal, barb, ctx


def _decision(valor):
    """pick forzado para la decisión ("no", "si") o pago ("gratis"/"furia")."""
    def espia(rng, opciones):
        if tuple(opciones) in (("no", "si"), ("gratis", "furia")):
            return valor
        return list(opciones)[0]
    return espia


def _guarda_con(total: int, success: bool):
    def stub(target, ability, dc, rng, mode=None, **kw):
        return SaveResult(ability=ability, dc=dc, rolls=[total], bonus=0,
                          total=total, success=success,
                          mode=RollMode.NORMAL)
    return stub


# --- Tabla y aplicación ------------------------------------------------------

def test_zealot_features_por_nivel():
    assert ZEALOT_FEATURES == {
        3: ("Divine Fury", "Warrior of the Gods"),
        6: ("Fanatical Focus",),
        10: ("Zealous Presence",),
        14: ("Rage of the Gods",),
    }


def test_clave_de_registro_zealot_en_barbarian():
    assert "zealot" in BARBARIAN_CLASS.subclasses
    sub = BARBARIAN_CLASS.subclasses["zealot"]
    assert sub.name == "Path of the Zealot"
    pj = _pj(3)
    apply_barbarian(pj, level=3)
    sub.apply(pj)
    assert any(isinstance(t, ZealotFeatures) for t in pj.traits)


def test_apply_requiere_clase_barbara():
    with pytest.raises(ValueError, match="apply_barbarian"):
        apply_zealot(_pj())


def test_apply_anade_trait_y_dos_acciones_bonus():
    pj = _pj(level=5)
    apply_barbarian(pj, level=5)
    zeal = apply_zealot(pj, level=5)
    assert isinstance(zeal, ZealotFeatures)
    assert zeal.name == "Zealot"
    assert zeal.dados_restantes == 4
    nombres = [a.name for a in pj.actions]
    assert "Guerrero de los Dioses" in nombres
    assert "Presencia ferviente" in nombres
    heal = next(a for a in pj.actions if isinstance(a, WarriorHealAction))
    pres = next(a for a in pj.actions if isinstance(a, ZealousPresenceAction))
    assert heal.usage is None and pres.usage is None


def test_apply_class_por_clave_aplica_zealot():
    pj = _pj(6)
    apply_class(pj, "barbarian", "zealot")
    assert any(isinstance(t, ZealotFeatures) for t in pj.traits)


# --- Divine Fury (3) ---------------------------------------------------------

def _espiar_divine(monkeypatch):
    llamadas = []
    def espia(target, amount, damage_type=None, source=None, ctx=None, **kw):
        llamadas.append({"amount": amount, "tipo": damage_type,
                         "magical": kw.get("magical")})
    monkeypatch.setattr(ze, "inflict_damage", espia)
    monkeypatch.setattr(ze, "roll_dice", lambda expr, rng, crit=False: 6)
    return llamadas


def test_divine_fury_paga_1d6_mas_mitad_del_nivel(monkeypatch):
    llamadas = _espiar_divine(monkeypatch)
    monkeypatch.setattr(ze, "pick", lambda rng, opciones: opciones[0])
    pj = _pj(5)
    zeal, barb, ctx = _furia(pj, 5)
    mon = _mon()
    extra = zeal.extra_attack_damage(pj, mon, AttackRange.MELEE,
                                     ctx=ctx, rng=ctx.rng)
    assert extra == 0  # el daño va aparte, no al paquete del golpe
    assert llamadas == [{"amount": 6 + 5 // 2, "tipo": "necrotic",
                         "magical": False}]
    assert any("daño divino (necrótico)" in line for line in ctx.log)


def test_divine_fury_elige_radiante_con_pick(monkeypatch):
    llamadas = _espiar_divine(monkeypatch)
    monkeypatch.setattr(ze, "pick", lambda rng, opciones: opciones[-1])
    pj = _pj(5)
    zeal, barb, ctx = _furia(pj, 5)
    zeal.extra_attack_damage(pj, _mon(), AttackRange.MELEE,
                             ctx=ctx, rng=ctx.rng)
    assert llamadas[0]["tipo"] == "radiante"
    assert any("daño divino (radiante)" in line for line in ctx.log)


def test_divine_fury_solo_paga_en_la_primera_criatura_del_turno(monkeypatch):
    llamadas = _espiar_divine(monkeypatch)
    monkeypatch.setattr(ze, "pick", lambda rng, opciones: opciones[0])
    pj = _pj(5)
    zeal, barb, ctx = _furia(pj, 5)
    zeal.extra_attack_damage(pj, _mon("A"), AttackRange.MELEE,
                             ctx=ctx, rng=ctx.rng)
    extra = zeal.extra_attack_damage(pj, _mon("B"), AttackRange.MELEE,
                                     ctx=ctx, rng=ctx.rng)
    assert len(llamadas) == 1
    assert extra == 0


def test_divine_fury_se_repone_al_empezar_el_turno(monkeypatch):
    llamadas = _espiar_divine(monkeypatch)
    monkeypatch.setattr(ze, "pick", lambda rng, opciones: opciones[0])
    pj = _pj(5)
    zeal, barb, ctx = _furia(pj, 5)
    zeal.extra_attack_damage(pj, _mon("A"), AttackRange.MELEE,
                             ctx=ctx, rng=ctx.rng)
    zeal.on_turn_start(pj, ctx)
    zeal.extra_attack_damage(pj, _mon("B"), AttackRange.MELEE,
                             ctx=ctx, rng=ctx.rng)
    assert len(llamadas) == 2


def test_divine_fury_no_paga_sin_furia(monkeypatch):
    llamadas = _espiar_divine(monkeypatch)
    monkeypatch.setattr(
        ze, "pick",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("pick")))
    pj = _pj(5)
    zeal = _zeal(pj, 5)
    ctx = _ctx(pj, [pj])
    zeal.extra_attack_damage(pj, _mon(), AttackRange.MELEE,
                             ctx=ctx, rng=ctx.rng)
    assert llamadas == []


def test_divine_fury_no_paga_en_reacciones(monkeypatch):
    llamadas = _espiar_divine(monkeypatch)
    monkeypatch.setattr(ze, "pick", lambda rng, opciones: opciones[0])
    pj = _pj(5)
    zeal, barb, ctx = _furia(pj, 5)
    ctx.is_reaction = True
    zeal.extra_attack_damage(pj, _mon(), AttackRange.MELEE,
                             ctx=ctx, rng=ctx.rng)
    assert llamadas == []


def test_divine_fury_no_paga_fuera_de_su_turno(monkeypatch):
    llamadas = _espiar_divine(monkeypatch)
    monkeypatch.setattr(ze, "pick", lambda rng, opciones: opciones[0])
    pj = _pj(5)
    zeal, barb, ctx = _furia(pj, 5)
    enemigo = _mon()
    ctx.actor = enemigo  # el turno es de otro
    zeal.extra_attack_damage(pj, _mon(), AttackRange.MELEE,
                             ctx=ctx, rng=ctx.rng)
    assert llamadas == []


def test_divine_fury_no_paga_sin_rng_y_no_se_marca(monkeypatch):
    llamadas = _espiar_divine(monkeypatch)
    monkeypatch.setattr(
        ze, "pick",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("pick")))
    pj = _pj(5)
    zeal, barb, ctx = _furia(pj, 5)
    zeal.extra_attack_damage(pj, _mon(), AttackRange.MELEE,
                             ctx=ctx, rng=None)
    assert llamadas == []
    assert zeal.divine_pagado is False  # sin pago no se marca el turno
    # con RNG después sí paga
    monkeypatch.setattr(ze, "pick", lambda rng, opciones: opciones[0])
    zeal.extra_attack_damage(pj, _mon(), AttackRange.MELEE,
                             ctx=ctx, rng=ctx.rng)
    assert len(llamadas) == 1


def test_divine_fury_funciona_a_distancia(monkeypatch):
    llamadas = _espiar_divine(monkeypatch)
    monkeypatch.setattr(ze, "pick", lambda rng, opciones: opciones[0])
    pj = _pj(5)
    zeal, barb, ctx = _furia(pj, 5)
    zeal.extra_attack_damage(pj, _mon(), AttackRange.RANGED,
                             ctx=ctx, rng=ctx.rng)
    assert len(llamadas) == 1


def test_divine_fury_reset_limpia_el_pago(monkeypatch):
    llamadas = _espiar_divine(monkeypatch)
    monkeypatch.setattr(ze, "pick", lambda rng, opciones: opciones[0])
    pj = _pj(5)
    zeal, barb, ctx = _furia(pj, 5)
    zeal.extra_attack_damage(pj, _mon("A"), AttackRange.MELEE,
                             ctx=ctx, rng=ctx.rng)
    zeal.reset()
    assert zeal.divine_pagado is False
    # la reset no toca la Furia (es de la clase): con el flag limpio
    # vuelve a pagar en el mismo turno
    zeal.extra_attack_damage(pj, _mon("B"), AttackRange.MELEE,
                             ctx=ctx, rng=ctx.rng)
    assert len(llamadas) == 2


def test_divine_fury_no_se_paga_en_fallo_de_ataque(monkeypatch):
    pj = _pj(5)
    zeal, barb, ctx = _furia(pj, 5)
    orco = _mon()
    llamadas = []
    def espia(*args, **kwargs):
        llamadas.append(1)
        return 0
    monkeypatch.setattr(zeal, "extra_attack_damage", espia)
    # Fallo seguro: el AC no se alcanza con la tirada fija.
    orco.ac = 99
    attack_roll(pj, orco, pj.attacks[0], ctx.rng, None, ctx=ctx)
    assert llamadas == []
    # Acierto seguro: el hook del motor sí se despacha.
    orco.ac = 1
    attack_roll(pj, orco, pj.attacks[0], ctx.rng, None, ctx=ctx)
    assert len(llamadas) == 1


# --- Warrior of the Gods (3) -------------------------------------------------

def _accion(pj, clase):
    return next(a for a in pj.actions if isinstance(a, clase))


def test_warrior_de_los_dioses_reserva_por_nivel():
    for nivel, esperados in ((3, 4), (6, 5), (12, 6), (17, 7)):
        pj = _pj(nivel)
        zeal = _zeal(pj, nivel)
        assert zeal.dados_restantes == esperados, nivel
        zeal.dados_restantes = 0
        zeal.reset()
        assert zeal.dados_restantes == esperados, f"reset nivel {nivel}"


def test_warrior_curacion_gasta_un_dado_y_suma_pv(monkeypatch):
    pj = _pj(5)
    zeal = _zeal(pj, 5)
    pj.hp = 90
    ctx = _ctx(pj, [pj], seed=4)
    monkeypatch.setattr(ze, "pick", lambda rng, opciones: list(opciones)[0])
    monkeypatch.setattr(ze, "roll_dice", lambda expr, rng, crit=False: 12)
    accion = _accion(pj, WarriorHealAction)
    accion.execute(ctx)
    assert pj.hp == 102
    assert zeal.dados_restantes == 3
    assert any("Guerrero de los Dioses" in line for line in ctx.log)


def test_warrior_curacion_no_supera_el_maximo(monkeypatch):
    pj = _pj(5)
    zeal = _zeal(pj, 5)
    pj.hp = 495
    ctx = _ctx(pj, [pj])
    monkeypatch.setattr(ze, "pick", lambda rng, opciones: list(opciones)[0])
    monkeypatch.setattr(ze, "roll_dice", lambda expr, rng, crit=False: 40)
    _accion(pj, WarriorHealAction).execute(ctx)
    assert pj.hp == 500


def test_warrior_solo_disponible_con_el_barbaro_herido():
    pj = _pj(5)
    _zeal(pj, 5)
    accion = _accion(pj, WarriorHealAction)
    assert not accion.can_use(None, _ctx(pj, [pj]))  # al máximo
    pj.hp = 499
    assert accion.can_use(None, _ctx(pj, [pj]))


def test_warrior_solo_disponible_con_dados_restantes():
    pj = _pj(5)
    zeal = _zeal(pj, 5)
    pj.hp = 100
    zeal.dados_restantes = 0
    accion = _accion(pj, WarriorHealAction)
    assert not accion.can_use(None, _ctx(pj, [pj]))


def test_warrior_ejecucion_sin_dados_no_gasta_rng(monkeypatch):
    pj = _pj(5)
    zeal = _zeal(pj, 5)
    zeal.dados_restantes = 0
    ctx = _ctx(pj, [pj])
    monkeypatch.setattr(
        ze, "pick",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("pick")))
    _accion(pj, WarriorHealAction).execute(ctx)
    assert pj.hp == 500


def test_warrior_no_exige_furia_para_curarse(monkeypatch):
    pj = _pj(5)
    _zeal(pj, 5)
    pj.hp = 100
    accion = _accion(pj, WarriorHealAction)
    assert accion.can_use(None, _ctx(pj, [pj]))  # sin Furia activada


def test_warrior_ejecucion_determinista_con_misma_semilla():
    def corrida():
        pj = _pj(5)
        zeal = _zeal(pj, 5)
        pj.hp = 90
        ctx = _ctx(pj, [pj], seed=9)
        _accion(pj, WarriorHealAction).execute(ctx)
        return pj.hp, zeal.dados_restantes, list(ctx.log)
    assert corrida() == corrida()


# --- Fanatical Focus (6) -----------------------------------------------------

def _fallos(pj, level, seed=0, dc=20):
    zeal, barb, ctx = _furia(pj, level, seed)
    sr = SaveResult(ability="dex", dc=dc, rolls=[1], bonus=0, total=1,
                    success=False, mode=RollMode.NORMAL)
    return zeal, ctx, sr


def test_fanatical_repite_la_salvacion_con_bonificador_de_furia(monkeypatch):
    pj = _pj(6)
    zeal, ctx, sr = _fallos(pj, 6)
    monkeypatch.setattr(ze, "pick", _decision("si"))
    monkeypatch.setattr(ze, "saving_throw", _guarda_con(10, False))
    salida = zeal.after_failed_save(pj, "dex", sr, ctx)
    esperado = 10 + rage_damage(6)
    assert salida is not None
    assert salida.total == esperado
    assert salida.bonus == rage_damage(6)
    assert salida.success == (esperado >= 20)
    assert zeal.fanatical_usado is True
    assert any("Fanatical Focus" in line for line in ctx.log)


def test_fanatical_el_resultado_nuevo_sustituye_al_original(monkeypatch):
    import dnd_sim.rules.saves as saves_mod
    pj = _pj(6)
    zeal, ctx, sr = _fallos(pj, 6)
    monkeypatch.setattr(ze, "pick", _decision("si"))
    monkeypatch.setattr(ze, "saving_throw", _guarda_con(30, True))
    salida = saves_mod.registrar_resistencia(ctx, pj, sr)
    assert salida is not sr
    assert salida.success is True
    assert salida.total == 30 + rage_damage(6)


def test_fanatical_solo_una_vez_por_furia(monkeypatch):
    pj = _pj(6)
    zeal, ctx, sr = _fallos(pj, 6)
    monkeypatch.setattr(ze, "pick", _decision("si"))
    monkeypatch.setattr(ze, "saving_throw", _guarda_con(10, False))
    assert zeal.after_failed_save(pj, "dex", sr, ctx) is not None
    # segunda salvación fallida en la misma Furia: ni pick ni repetición
    monkeypatch.setattr(
        ze, "pick",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("pick")))
    assert zeal.after_failed_save(pj, "dex", sr, ctx) is None


def test_fanatical_se_repone_al_activar_una_nueva_furia(monkeypatch):
    pj = _pj(6)
    zeal, ctx, sr = _fallos(pj, 6)
    monkeypatch.setattr(ze, "pick", _decision("si"))
    monkeypatch.setattr(ze, "saving_throw", _guarda_con(10, False))
    zeal.after_failed_save(pj, "dex", sr, ctx)
    zeal.on_rage_start(pj, ctx)
    assert zeal.fanatical_usado is False
    assert zeal.after_failed_save(pj, "dex", sr, ctx) is not None


def test_fanatical_no_activo_sin_furia(monkeypatch):
    pj = _pj(6)
    zeal = _zeal(pj, 6)
    ctx = _ctx(pj, [pj])
    sr = SaveResult(ability="con", dc=20, rolls=[1], bonus=0, total=1,
                    success=False, mode=RollMode.NORMAL)
    monkeypatch.setattr(
        ze, "pick",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("pick")))
    assert zeal.after_failed_save(pj, "con", sr, ctx) is None


def test_fanatical_no_se_ofrece_en_salvacion_superada(monkeypatch):
    import dnd_sim.rules.saves as saves_mod
    pj = _pj(6)
    zeal, ctx, sr = _fallos(pj, 6)
    sr.success = True
    monkeypatch.setattr(
        ze, "pick",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("pick")))
    salida = saves_mod.registrar_resistencia(ctx, pj, sr)
    assert salida is sr  # el despacho ni se consulta


def test_fanatical_decision_negativa_no_repiten(monkeypatch):
    pj = _pj(6)
    zeal, ctx, sr = _fallos(pj, 6)
    monkeypatch.setattr(ze, "pick", _decision("no"))
    monkeypatch.setattr(
        ze, "saving_throw",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("guarda")))
    assert zeal.after_failed_save(pj, "dex", sr, ctx) is None
    assert zeal.fanatical_usado is False


def test_fanatical_no_se_ofrece_en_auto_fallo(monkeypatch):
    pj = _pj(6)
    zeal, ctx, sr = _fallos(pj, 6)
    sr.auto_fail = True
    monkeypatch.setattr(
        ze, "pick",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("pick")))
    assert zeal.after_failed_save(pj, "dex", sr, ctx) is None


# --- Zealous Presence (10) ---------------------------------------------------

def _presencia(level=10, seed=0, aliados=True):
    pj = _pj(level)
    zeal = _zeal(pj, level)
    orco = _mon()
    enemigos = [orco] if not aliados else []
    aliado = _aliado(level) if aliados else None
    combatantes = [pj, orco] + ([aliado] if aliado else [])
    ctx = _ctx(pj, combatantes, seed)
    if aliado:
        ctx.actor = pj
    return pj, zeal, orco, aliado, ctx


def test_presencia_da_ventaja_en_ataques_a_aliados():
    pj, zeal, orco, aliado, ctx = _presencia()
    zeal.presencia_activa = True
    mods = attack_modifiers(aliado, orco, pj.attacks[0], AttackRange.MELEE,
                            ctx=ctx, rng=ctx.rng)
    assert "Presencia ferviente" in mods.advantage_sources


def test_presencia_no_da_ventaja_al_enemigo_ni_al_barbaro():
    pj, zeal, orco, aliado, ctx = _presencia()
    zeal.presencia_activa = True
    enemigo = attack_modifiers(orco, aliado or pj, pj.attacks[0],
                               AttackRange.MELEE, ctx=ctx, rng=ctx.rng)
    assert "Presencia ferviente" not in enemigo.advantage_sources
    propio = attack_modifiers(pj, orco, pj.attacks[0], AttackRange.MELEE,
                              ctx=ctx, rng=ctx.rng)
    assert "Presencia ferviente" not in propio.advantage_sources


def test_presencia_da_ventaja_en_salvaciones_a_aliados():
    pj, zeal, orco, aliado, ctx = _presencia()
    zeal.presencia_activa = True
    sr = saving_throw(aliado, "dex", 20, ctx.rng, ctx=ctx)
    assert sr.mode is RollMode.ADVANTAGE


def test_presencia_no_da_ventaja_en_salvaciones_al_barbaro():
    pj, zeal, orco, aliado, ctx = _presencia()
    zeal.presencia_activa = True
    sr = saving_throw(pj, "dex", 20, ctx.rng, ctx=ctx)
    assert sr.mode is RollMode.NORMAL


def test_presencia_sin_activa_no_da_ventaja():
    pj, zeal, orco, aliado, ctx = _presencia()
    assert zeal.presencia_activa is False
    sr = saving_throw(aliado, "dex", 20, ctx.rng, ctx=ctx)
    assert sr.mode is RollMode.NORMAL


def test_presencia_termina_al_empezar_el_siguiente_turno_del_barbaro():
    pj, zeal, orco, aliado, ctx = _presencia()
    zeal.presencia_activa = True
    zeal.on_turn_start(pj, ctx)
    assert zeal.presencia_activa is False
    sr = saving_throw(aliado, "dex", 20, ctx.rng, ctx=ctx)
    assert sr.mode is RollMode.NORMAL


def test_presencia_uso_gratis_gasta_el_uso(monkeypatch):
    pj, zeal, orco, aliado, ctx = _presencia()
    accion = _accion(pj, ZealousPresenceAction)
    assert accion.can_use(None, ctx)
    monkeypatch.setattr(ze, "pick", _decision("gratis"))
    accion.execute(ctx)
    assert zeal.presencia_activa is True
    assert not zeal.presence_usage.available


def test_presencia_gasta_una_furia_y_restaura_el_uso_gratis(monkeypatch):
    pj, zeal, orco, aliado, ctx = _presencia()
    zeal.presence_usage.spend()  # sin uso gratis: solo queda la Furia
    furia = ze._furia_de(pj)
    assert furia.usage.available
    antes = furia.usage.uses_left
    accion = _accion(pj, ZealousPresenceAction)
    assert accion.can_use(None, ctx)
    monkeypatch.setattr(ze, "pick", _decision("furia"))
    accion.execute(ctx)
    assert zeal.presencia_activa is True
    assert furia.usage.uses_left == antes - 1  # gastó una Furia...
    assert zeal.presence_usage.available  # ...y restauró el uso gratis


def test_presencia_sin_aliados_no_se_puede_activar():
    pj, zeal, orco, aliado, ctx = _presencia(aliados=False)
    accion = _accion(pj, ZealousPresenceAction)
    assert not accion.can_use(None, ctx)


def test_presencia_reset_restaura_todo():
    pj, zeal, orco, aliado, ctx = _presencia()
    zeal.presencia_activa = True
    zeal.presence_usage.spend()
    zeal.reset()
    assert zeal.presencia_activa is False
    assert zeal.presence_usage.available


def test_presencia_con_cobertura_uno_no_consume_rng():
    pj, zeal, orco, aliado, ctx = _presencia()
    zeal.presencia_activa = True
    antes = ctx.rng.getstate()
    attack_modifiers(aliado, orco, pj.attacks[0], AttackRange.MELEE,
                     ctx=ctx, rng=ctx.rng)
    assert ctx.rng.getstate() == antes  # cobertura 1.0: ni un draw


# --- Rage of the Gods (14) ---------------------------------------------------

def _forma(level=14, seed=0):
    pj = _pj(level)
    zeal = _zeal(pj, level)
    barb = _barbaro(pj)
    barb.activate(1)
    ctx = _ctx(pj, [pj], seed)
    return pj, zeal, barb, ctx


def test_forma_divina_concede_las_tres_resistencias(monkeypatch):
    from dnd_sim import DamageType
    pj, zeal, barb, ctx = _forma()
    monkeypatch.setattr(ze, "pick", _decision("si"))
    zeal.on_rage_start(pj, ctx)
    assert zeal.forma_activa is True
    assert zeal.forma_usada is True
    assert pj.resistances == {DamageType.NECROTIC, DamageType.PSYCHIC,
                              DamageType.RADIANT}
    assert any("forma divina" in line for line in ctx.log)


def test_forma_no_quita_resistencias_de_otro_origen(monkeypatch):
    from dnd_sim import DamageType
    pj, zeal, barb, ctx = _forma()
    pj.resistances.add(DamageType.PSYCHIC)  # ya la tenía por otro origen
    monkeypatch.setattr(ze, "pick", _decision("si"))
    zeal.on_rage_start(pj, ctx)
    assert DamageType.PSYCHIC not in zeal._forma_concedidas
    zeal.on_rage_end(pj, ctx)
    assert DamageType.PSYCHIC in pj.resistances  # sigue intacta
    assert DamageType.NECROTIC not in pj.resistances  # la nuestra, revocada
    assert zeal.forma_activa is False


def test_forma_una_vez_por_combate(monkeypatch):
    pj, zeal, barb, ctx = _forma()
    monkeypatch.setattr(ze, "pick", _decision("si"))
    zeal.on_rage_start(pj, ctx)
    # segunda Furia: no se vuelve a ofrecer (ni RNG)
    monkeypatch.setattr(
        ze, "pick",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("pick")))
    zeal.rage_expires_round = 0
    zeal.on_rage_start(pj, ctx)
    assert zeal.forma_usada is True


def test_forma_se_vuelve_a_ofrecer_si_dice_que_no(monkeypatch):
    pj, zeal, barb, ctx = _forma()
    llamadas = []
    real = ze.pick
    def espia(rng, opciones):
        llamadas.append(tuple(opciones))
        return "no"
    monkeypatch.setattr(ze, "pick", espia)
    zeal.on_rage_start(pj, ctx)
    assert llamadas == [("no", "si")]
    assert zeal.forma_usada is False
    assert zeal.forma_activa is False
    zeal.on_rage_start(pj, ctx)  # nueva Furia: se ofrece otra vez
    assert llamadas == [("no", "si"), ("no", "si")]


def test_forma_revocada_al_terminar_la_furia(monkeypatch):
    from dnd_sim import DamageType
    pj, zeal, barb, ctx = _forma()
    monkeypatch.setattr(ze, "pick", _decision("si"))
    zeal.on_rage_start(pj, ctx)
    barb.rage_active = False
    zeal.on_rage_end(pj, ctx)
    assert pj.resistances == set()
    assert zeal.forma_activa is False
    # forma_usada sigue gastada (una vez por combate)
    assert zeal.forma_usada is True


def test_revivification_gasta_un_uso_de_furia_y_sube_al_nivel(monkeypatch):
    pj, zeal, barb, ctx = _forma()
    monkeypatch.setattr(ze, "pick", _decision("si"))
    zeal.on_rage_start(pj, ctx)
    furia = ze._furia_de(pj)
    assert furia.usage.available
    antes = furia.usage.uses_left
    salida = zeal.on_reduced_to_zero_hp(pj, 999, "fire", _mon(),
                                        crit=False, ctx=ctx, rng=ctx.rng)
    assert salida == 14
    assert furia.usage.uses_left == antes - 1  # gastó un uso de Furia
    assert zeal.revivificada is True
    assert any("Revivification" in line for line in ctx.log)


def test_revivification_una_sola_vez_por_forma(monkeypatch):
    pj, zeal, barb, ctx = _forma()
    monkeypatch.setattr(ze, "pick", _decision("si"))
    zeal.on_rage_start(pj, ctx)
    assert zeal.on_reduced_to_zero_hp(pj, 999, "fire", _mon(),
                                      ctx=ctx, rng=ctx.rng) == 14
    assert zeal.on_reduced_to_zero_hp(pj, 999, "fire", _mon(),
                                      ctx=ctx, rng=ctx.rng) is None


def test_revivificacion_sin_usos_de_furia_no_activa(monkeypatch):
    pj, zeal, barb, ctx = _forma()
    monkeypatch.setattr(ze, "pick", _decision("si"))
    zeal.on_rage_start(pj, ctx)
    furia = ze._furia_de(pj)
    while furia.usage.available:  # agota todos los usos de Furia
        furia.usage.spend()
    assert zeal.on_reduced_to_zero_hp(pj, 999, "fire", _mon(),
                                      ctx=ctx, rng=ctx.rng) is None
    assert zeal.revivificada is False


def test_revivificacion_sin_forma_divina_no_activa():
    pj, zeal, barb, ctx = _forma()
    assert zeal.forma_activa is False
    assert zeal.on_reduced_to_zero_hp(pj, 999, "fire", _mon(),
                                      ctx=ctx, rng=ctx.rng) is None


def test_revivificacion_no_roba_el_gasto_de_furia_inaguantable(
        monkeypatch):
    import dnd_sim.rules.classes.barbarian.features as features_mod
    pj, zeal, barb, ctx = _forma(level=14)
    monkeypatch.setattr(ze, "pick", _decision("si"))
    zeal.on_rage_start(pj, ctx)
    orco = _mon()
    furia = ze._furia_de(pj)
    antes = furia.usage.uses_left

    # (a) Furia Inaguantable salva: el primer respondo gana y el uso de
    # Furia no se toca (el hook de Zealot ni se llama).
    def salva(*a, **k):
        return SaveResult(ability="con", dc=15, rolls=[20], bonus=0,
                          total=20, success=True, mode=RollMode.NORMAL)
    monkeypatch.setattr(features_mod, "saving_throw", salva)
    pj.hp = 10
    from dnd_sim import inflict_damage
    inflict_damage(pj, 999, "fire", source=orco, ctx=ctx, rng=ctx.rng)
    assert pj.hp == 28  # 2 * nivel
    assert furia.usage.uses_left == antes
    assert zeal.revivificada is False

    # (b) Furia Inaguantable falla: Zealot revivifica y gasta su uso.
    def falla(*a, **k):
        return SaveResult(ability="con", dc=15, rolls=[1], bonus=0,
                          total=1, success=False, mode=RollMode.NORMAL)
    monkeypatch.setattr(features_mod, "saving_throw", falla)
    pj.hp = 10
    zeal.revivificada = False
    inflict_damage(pj, 999, "fire", source=orco, ctx=ctx, rng=ctx.rng)
    assert pj.hp == 14  # nivel del bárbaro
    assert furia.usage.uses_left == antes - 1
    assert zeal.revivificada is True


# --- Niveles inferiores y no regresión --------------------------------------

def test_nivel_3_no_recibe_rasgos_superiores(monkeypatch):
    pj = _pj(3)
    zeal = _zeal(pj, 3)
    ctx = _ctx(pj, [pj])
    barb = _barbaro(pj)
    barb.activate(1)
    # Fanatical Focus (6): ni pick.
    monkeypatch.setattr(
        ze, "pick",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("pick")))
    sr = SaveResult(ability="con", dc=20, rolls=[1], bonus=0, total=1,
                    success=False, mode=RollMode.NORMAL)
    assert zeal.after_failed_save(pj, "con", sr, ctx) is None
    # Rage of the Gods (14): on_rage_start no ofrece la forma.
    zeal.on_rage_start(pj, ctx)
    assert zeal.forma_activa is False
    # Zealous Presence (10): la acción no está disponible.
    accion = _accion(pj, ZealousPresenceAction)
    aliado = _aliado(3)
    ctx.combatants.append(aliado)
    assert not accion.can_use(None, ctx)


def test_hooks_nuevos_sin_subclase_no_despachan_ni_consumen_rng():
    assert "grant_save_modifiers" in HOOK_NAMES
    pj = _pj(5)
    apply_barbarian(pj, level=5)  # sin subclase
    assert hooks(pj.traits, "grant_save_modifiers") == []
    # sin nadie que granta: el resultado y el RNG son idénticos con y
    # sin ctx
    orco = _mon()
    rng1 = random.Random(3)
    sr1 = saving_throw(orco, "dex", 15, rng1, ctx=_ctx(pj, [pj, orco], 3))
    estado1 = rng1.getstate()
    rng2 = random.Random(3)
    sr2 = saving_throw(orco, "dex", 15, rng2)
    assert (sr1.total, sr1.success) == (sr2.total, sr2.success)
    assert estado1 == rng2.getstate()


def test_after_failed_save_sin_zealot_devuelve_el_mismo_resultado():
    import dnd_sim.rules.saves as saves_mod
    pj = _pj(5)
    apply_barbarian(pj, level=5)
    ctx = _ctx(pj, [pj])
    sr = SaveResult(ability="con", dc=20, rolls=[1], bonus=0, total=1,
                    success=False, mode=RollMode.NORMAL)
    salida = saves_mod.registrar_resistencia(ctx, pj, sr)
    assert salida is sr  # identidad intacta: cero cambios sin la subclase


def test_determinismo_misma_semilla_mismos_resultados(monkeypatch):
    llamadas = []
    def espia(target, amount, damage_type=None, source=None, ctx=None, **kw):
        llamadas.append((amount, damage_type))
    monkeypatch.setattr(ze, "inflict_damage", espia)

    def corrida():
        llamadas.clear()
        pj = _pj(5)
        zeal, barb, ctx = _furia(pj, 5, seed=11)
        zeal.extra_attack_damage(pj, _mon(), AttackRange.MELEE,
                                 ctx=ctx, rng=ctx.rng)
        return list(llamadas), list(ctx.log)

    assert corrida() == corrida()

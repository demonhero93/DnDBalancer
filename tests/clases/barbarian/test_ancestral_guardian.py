"""Features de la subclase Guardián Ancestral del bárbaro (XGtE).

Cubre la marca (desventaja + resistencia), Espíritu Guardián con su
reacción y Vengeful Ancestors, además de la tabla de features y la
aplicación de la subclase.
"""
from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from dnd_sim import (
    Abilities,
    AncestralGuardianFeatures,
    Attack,
    BarbarianFeatures,
    Monster,
    PlayerCharacter,
    apply_ancestral_guardian,
    apply_barbarian,
    inflict_damage,
)
from dnd_sim.engine.combat.attack import attack_roll
from dnd_sim.rules.classes.barbarian.subclasses.ancestral_guardian import (
    ANCESTRAL_FEATURES,
)
from dnd_sim.rules.roll_modifiers import attack_modifiers
from dnd_sim.core.dice import roll_dice

import dnd_sim.engine.combat.attack as attack_mod


def _abilities(**kwargs) -> Abilities:
    base = dict(str=10, dex=10, con=10, int=10, wis=10, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    kwargs.setdefault("name", "Thor")
    kwargs.setdefault("max_hp", 500)
    kwargs.setdefault("ac", 15)
    kwargs.setdefault("level", 5)
    kwargs.setdefault("abilities", _abilities())
    kwargs.setdefault("attacks", [Attack("Hacha de batalla", "1d12",
                                         ability="str")])
    return PlayerCharacter(**kwargs)


def _aliado(**kwargs) -> PlayerCharacter:
    kwargs.setdefault("name", "Ally")
    return _pj(**kwargs)


def _monstruo(**kwargs) -> Monster:
    kwargs.setdefault("name", "Orco")
    kwargs.setdefault("max_hp", 500)
    kwargs.setdefault("ac", 12)
    kwargs.setdefault("abilities", _abilities())
    kwargs.setdefault("attacks", [Attack("Hacha orca", "1d6", ability="str",
                                         attack_bonus=30)])
    return Monster(**kwargs)


def _escudo(pj, level):
    """Aplica clase + subclase y devuelve el rasgo de la subclase."""
    apply_barbarian(pj, level=level)
    return apply_ancestral_guardian(pj, level=level)


def _barbaro(pj) -> BarbarianFeatures:
    return next(t for t in pj.traits if isinstance(t, BarbarianFeatures))


def _ctx(combatants, round_=1, seed=0):
    return SimpleNamespace(combatants=list(combatants), round=round_,
                           rng=random.Random(seed), log=[])


# --- Tabla y aplicación ------------------------------------------------------

def test_ancestral_features_por_nivel():
    assert ANCESTRAL_FEATURES == {
        3: ("Ancestral Protectors",),
        6: ("Spirit Shield",),
        10: ("Consult the Spirits",),
        14: ("Vengeful Ancestors",),
    }


def test_apply_requiere_clase_barbara():
    with pytest.raises(ValueError, match="apply_barbarian"):
        apply_ancestral_guardian(_pj())


def test_apply_anade_trait_con_nivel():
    pj = _pj(level=5)
    trait = apply_barbarian(pj, level=5)
    sub = apply_ancestral_guardian(pj)  # nivel por defecto = el del PJ
    assert isinstance(sub, AncestralGuardianFeatures)
    assert sub.level == 5
    assert sub in pj.traits and trait in pj.traits
    # Nivel explícito manda.
    otro_pj = _pj(level=9)
    apply_barbarian(otro_pj, level=9)
    sub2 = apply_ancestral_guardian(otro_pj, level=3)
    assert sub2.level == 3


# --- Ancestral Protectors: la marca -----------------------------------------

def test_marca_al_primer_golpe_del_turno():
    pj, enemigo, otro = _pj(), _monstruo(), _aliado(name="Otro")
    sub = _escudo(pj, level=5)
    _barbaro(pj).rage_active = True
    ctx = SimpleNamespace(round=4, rng=random.Random(0), log=[])

    sub.after_dealing_hit(enemigo, pj, None, ctx=ctx)
    assert sub.marked is enemigo
    assert enemigo.state.marked_by is pj
    assert sub.mark_hit_round == 4

    # Segundo golpe del mismo turno: sigue con la primera.
    sub.after_dealing_hit(otro, pj, None, ctx=ctx)
    assert sub.marked is enemigo

    # Turno siguiente: marca a la primera de ese turno y limpia la vieja.
    ctx.round = 5
    sub.after_dealing_hit(otro, pj, None, ctx=ctx)
    assert sub.marked is otro
    assert otro.state.marked_by is pj
    assert enemigo.state.marked_by is None


def test_marca_solo_con_furia_y_desde_nivel_3():
    pj, enemigo = _pj(), _monstruo()
    sub = _escudo(pj, level=5)
    ctx = SimpleNamespace(round=1, rng=random.Random(0), log=[])

    sub.after_dealing_hit(enemigo, pj, None, ctx=ctx)  # sin Furia
    assert sub.marked is None

    _barbaro(pj).rage_active = True
    sub.after_dealing_hit(enemigo, pj, None, ctx=ctx)
    assert sub.marked is enemigo

    sub.reset()
    sub.level = 1  # por debajo de 3 la marca no se aplica
    sub.after_dealing_hit(enemigo, pj, None, ctx=ctx)
    assert sub.marked is None


def test_marca_limpia_en_inicio_de_turno():
    pj, enemigo = _pj(), _monstruo()
    sub = _escudo(pj, level=5)
    _barbaro(pj).rage_active = True
    sub.after_dealing_hit(enemigo, pj, None,
                          ctx=SimpleNamespace(round=1, rng=None, log=[]))
    sub.on_turn_start(pj, ctx=None)
    assert sub.marked is None
    assert enemigo.state.marked_by is None
    assert sub.mark_hit_round == -1


def test_marca_muere_si_la_furia_termina():
    pj, enemigo = _pj(), _monstruo()
    sub = _escudo(pj, level=5)
    barb = _barbaro(pj)
    barb.rage_active = True
    sub.after_dealing_hit(enemigo, pj, None,
                          ctx=SimpleNamespace(round=1, rng=None, log=[]))

    sub.on_turn_end(pj, ctx=None)  # Furia sigue: la marca aguanta
    assert sub.marked is enemigo

    barb.rage_active = False
    sub.on_turn_end(pj, ctx=None)
    assert sub.marked is None
    assert enemigo.state.marked_by is None


def test_reset_limpia_la_marca():
    pj, enemigo = _pj(), _monstruo()
    sub = _escudo(pj, level=5)
    _barbaro(pj).rage_active = True
    sub.after_dealing_hit(enemigo, pj, None,
                          ctx=SimpleNamespace(round=1, rng=None, log=[]))
    pj.reset()
    assert sub.marked is None
    assert enemigo.state.marked_by is None


# --- Desventaja y resistencia por marca -------------------------------------

def test_desventaja_salvo_contra_el_marcador():
    pj, marcado = _pj(), _monstruo()
    tercero = _aliado()
    atk = Attack("Hacha", "1d6", ability="str")
    marcado.state.marked_by = pj

    mods_tercero = attack_modifiers(marcado, tercero, atk)
    assert "marca del defensor" in mods_tercero.disadvantage_sources

    mods_marcador = attack_modifiers(marcado, pj, atk)
    assert "marca del defensor" not in mods_marcador.disadvantage_sources

    marcado.state.marked_by = None
    sin_marca = attack_modifiers(marcado, tercero, atk)
    assert "marca del defensor" not in sin_marca.disadvantage_sources


def _ataque_fijo(monkeypatch):
    """Daño bruto siempre 100: el resto del flujo queda determinista."""
    monkeypatch.setattr(attack_mod, "roll_dice",
                        lambda expr, rng, crit=False: 100)


def _danio_al_aliado(monkeypatch, seed=0, marcado_a=None,
                     ataca_a=None) -> int:
    """Ataque del monstruo al aliado; devuelve el daño final recibido."""
    _ataque_fijo(monkeypatch)
    monstruo, aliado = _monstruo(), _aliado()
    pj = _pj()
    if marcado_a is not None:
        monstruo.state.marked_by = marcado_a(pj, monstruo, aliado)
    destino = ataca_a(pj, monstruo, aliado) if ataca_a else aliado
    rng = random.Random(seed)
    log = []
    ctx = SimpleNamespace(combatants=[pj, monstruo, aliado], round=1,
                          rng=rng, log=log)
    antes = destino.hp
    attack_roll(monstruo, destino, monstruo.attacks[0], rng, log=log,
                ctx=ctx)
    assert log, "el ataque no llegó a registrarse"
    return antes - destino.hp


def test_daño_del_marcado_a_terceros_se_resiste(monkeypatch):
    # La marca da desventaja (tira doble) y halva el daño principal.
    perdida = _danio_al_aliado(
        monkeypatch, seed=3,
        marcado_a=lambda pj, m, a: pj,
    )
    assert perdida == 50  # 100 // 2


def test_daño_del_marcado_contra_su_marcador_no_se_resiste(monkeypatch):
    perdida = _danio_al_aliado(
        monkeypatch, seed=3,
        marcado_a=lambda pj, m, a: pj,
        ataca_a=lambda pj, m, a: pj,
    )
    assert perdida == 100


def test_daño_sin_marca_no_cambia(monkeypatch):
    perdida = _danio_al_aliado(monkeypatch, seed=3)
    assert perdida == 100


# --- Spirit Shield (6) -------------------------------------------------------

def _esperado(expr: str, amount: int, seed: int) -> int:
    """Cantidad que queda tras la reducción, reproduciendo la misma tirada."""
    return max(0, amount - min(amount, int(roll_dice(expr,
                                                     random.Random(seed)))))


def test_spirit_shield_reduce_y_gasta_reaccion():
    pj, aliado = _pj(), _aliado()
    sub = _escudo(pj, level=5)
    _barbaro(pj).rage_active = True
    sub.level = 6
    ctx = _ctx([pj, aliado], seed=11)

    nuevo = sub.reduce_damage_to_allies(aliado, 10, ctx=ctx)
    assert nuevo == _esperado("2d6", 10, 11)
    assert pj.state.reaction_used is True

    # Reacción ya gastada: ya no reduce.
    assert sub.reduce_damage_to_allies(aliado, 10, ctx=ctx) is None


def test_spirit_shield_condiciones():
    pj, aliado = _pj(), _aliado()
    sub = _escudo(pj, level=6)
    barb = _barbaro(pj)
    ctx = _ctx([pj, aliado], seed=11)

    assert sub.reduce_damage_to_allies(aliado, 10, ctx=ctx) is None  # sin Furia
    barb.rage_active = True
    assert sub.reduce_damage_to_allies(pj, 10, ctx=ctx) is None  # a sí mismo
    assert sub.reduce_damage_to_allies(aliado, 10,
                                       ctx=SimpleNamespace(rng=None)) is None
    sub.level = 5  # sin Spirit Shield
    assert sub.reduce_damage_to_allies(aliado, 10, ctx=ctx) is None


def test_spirit_shield_escala_con_nivel():
    aliado = _aliado()
    for level, dados in ((10, "3d6"), (14, "4d6")):
        pj = _pj()
        sub = _escudo(pj, level=level)
        _barbaro(pj).rage_active = True
        ctx = _ctx([pj, aliado], seed=5)
        nuevo = sub.reduce_damage_to_allies(aliado, 100, ctx=ctx)
        assert nuevo == _esperado(dados, 100, 5)


# --- Fase 1b de inflict_damage + Vengeful Ancestors -------------------------

def test_inflict_damage_pasa_por_la_fase_1b():
    pj, aliado = _pj(), _aliado()
    sub = _escudo(pj, level=6)
    _barbaro(pj).rage_active = True
    ctx = _ctx([pj, aliado], seed=4)

    # Sin contexto no hay con quién consultar: daño completo.
    assert inflict_damage(aliado, 10, "force",
                          ctx=SimpleNamespace(rng=random.Random(4))) == 10
    aliado.hp = 500

    restante = inflict_damage(aliado, 10, "force", ctx=ctx)
    assert restante == _esperado("2d6", 10, 4)
    assert aliado.hp == 500 - restante


def test_vengeful_ancestors_devuelve_lo_evitado_al_atacante():
    pj, aliado = _pj(), _aliado()
    enemigo = _monstruo()
    sub = _escudo(pj, level=14)
    _barbaro(pj).rage_active = True
    ctx = _ctx([pj, aliado, enemigo], seed=9)

    restante = inflict_damage(aliado, 10, "bludgeoning", source=enemigo,
                              ctx=ctx)
    redicho = 10 - restante  # lo que el escudo acabó de evitar
    assert redicho >= 4  # 4d6 nunca baja de 4 (o de 10 si tiró más)
    assert aliado.hp == 500 - restante
    # El atacante lo recibe como daño de fuerza.
    assert enemigo.hp == 500 - redicho

    # La reacción ya está gastada: el siguiente daño entra entero.
    hp_antes = aliado.hp
    assert inflict_damage(aliado, 10, "bludgeoning", source=enemigo,
                          ctx=ctx) == 10
    assert aliado.hp == hp_antes - 10

"""Tests del motor de Maestría con Armas (rules/mastery.py)."""
from __future__ import annotations

import random
from types import SimpleNamespace

from dnd_sim import Abilities, Attack, Monster, PlayerCharacter
from dnd_sim.rules.conditions import Condition
from dnd_sim.rules.mastery import (
    al_acertar, al_fallar, consumir_marcas, maestria_de, resolver_maestria,
)


def _hab(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=10, wis=12, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _atacante() -> PlayerCharacter:
    return PlayerCharacter(
        name="Thor", max_hp=80, ac=12, level=5, abilities=_hab(),
        attacks=[Attack("Espada larga", "1d8", ability="str",
                        mastery="topple")],
    )


def _objetivo() -> Monster:
    # Monstruo sin salvaciones competentes: la tirada de CON es plana.
    return Monster(name="Muñeco", max_hp=100, ac=10,
                   abilities=Abilities(str=10, dex=10, con=10, int=10,
                                       wis=10, cha=10),
                   attacks=[])


def _arma(mastery: str, nombre: str = "Espada larga") -> Attack:
    return Attack(nombre, "1d8", ability="str", mastery=mastery)


def _ctx(rng=None, ronda=1, combatants=()):
    return SimpleNamespace(round=ronda, rng=rng or random.Random(1),
                           log=list(), combatants=list(combatants),
                           resources=None)


class _RngSiFalla:
    """pick → «si», d20 → 1 (la salvación de Topple falla)."""

    def __init__(self):
        self.llamadas = 0

    def randint(self, a: int, b: int) -> int:
        self.llamadas += 1
        return a

    def randrange(self, n: int) -> int:
        self.llamadas += 1
        return n - 1

    def random(self) -> float:
        self.llamadas += 1
        return 1.0


class _RngNo:
    """pick → «no» (decisión de no aplicar la maestría)."""

    def randint(self, a: int, b: int) -> int:
        return a

    def randrange(self, n: int) -> int:
        return 0

    def random(self) -> float:
        return 0.0


class _RngSinLlamadas:
    def randint(self, a: int, b: int) -> int:
        raise AssertionError("no debería consumir RNG")

    def randrange(self, n: int) -> int:
        raise AssertionError("no debería consumir RNG")

    def random(self) -> float:
        raise AssertionError("no debería consumir RNG")


def test_maestria_de_mapea_el_nombre_del_arma_en_ingles_y_espanol():
    assert maestria_de("Longsword") == "sap"
    assert maestria_de("Espada larga") == "sap"
    assert maestria_de("Hacha de batalla") == "topple"
    assert maestria_de("Arco corto") == "vex"
    assert maestria_de("  Greatsword ") == "graze"
    assert maestria_de("Espada de mentira") == ""


def test_topple_acertado_pide_salvacion_de_con_y_derriba_si_falla():
    atacante, objetivo = _atacante(), _objetivo()
    rng = _RngSiFalla()
    ctx = _ctx(rng, combatants=[atacante, objetivo])
    log: list[str] = []

    al_acertar(atacante, objetivo, _arma("topple"), damage=5,
               ctx=ctx, rng=rng, log=log)

    assert objetivo.conditions.has(Condition.PRONE)
    assert any("Topple" in line for line in log)


def test_topple_no_derriba_si_la_salvacion_pasa():
    class _RngSalva(_RngSiFalla):
        def randint(self, a: int, b: int) -> int:
            super().randint(a, b)
            return b  # d20 → 20: salva

    atacante, objetivo = _atacante(), _objetivo()
    rng = _RngSalva()
    ctx = _ctx(rng, combatants=[atacante, objetivo])

    al_acertar(atacante, objetivo, _arma("topple"), damage=5,
               ctx=ctx, rng=rng)

    assert not objetivo.conditions.has(Condition.PRONE)


def test_topple_con_decision_no_no_hace_nada():
    atacante, objetivo = _atacante(), _objetivo()
    rng = _RngNo()
    ctx = _ctx(rng, combatants=[atacante, objetivo])

    al_acertar(atacante, objetivo, _arma("topple"), damage=5,
               ctx=ctx, rng=rng)

    assert not objetivo.conditions.has(Condition.PRONE)


def test_vex_marca_ventaja_solo_si_hay_dano():
    atacante, objetivo = _atacante(), _objetivo()
    ctx = _ctx(ronda=3)

    al_acertar(atacante, objetivo, _arma("vex"), damage=4, ctx=ctx)
    assert atacante.state.maestria_ventaja["Muñeco"] == 5  # ronda + 2

    al_acertar(atacante, _objetivo(), _arma("vex"), damage=0, ctx=ctx)
    assert len(atacante.state.maestria_ventaja) == 1


def test_vex_concede_ventaja_y_se_consume_en_la_siguiente_tirada():
    atacante, objetivo = _atacante(), _objetivo()
    ctx = _ctx(ronda=1)
    al_acertar(atacante, objetivo, _arma("vex"), damage=4, ctx=ctx)

    mods = SimpleNamespace(advantage_sources=[], disadvantage_sources=[],
                           bonus=0)
    consumir_marcas(mods, atacante, objetivo, ctx)

    assert "Maestría Vex" in mods.advantage_sources
    assert atacante.state.maestria_ventaja == {}  # solo el siguiente ataque


def test_vex_caducada_no_concede_ventaja():
    atacante, objetivo = _atacante(), _objetivo()
    ctx = _ctx(ronda=1)
    al_acertar(atacante, objetivo, _arma("vex"), damage=4, ctx=ctx)

    mods = SimpleNamespace(advantage_sources=[], disadvantage_sources=[],
                           bonus=0)
    consumir_marcas(mods, atacante, objetivo, _ctx(ronda=3))  # caducada

    assert mods.advantage_sources == []
    assert atacante.state.maestria_ventaja == {}  # se limpia al caducar


def test_sap_marca_desventaja_en_el_objetivo_y_se_consume():
    atacante, objetivo = _atacante(), _objetivo()
    ctx = _ctx(ronda=1)
    al_acertar(atacante, objetivo, _arma("sap"), damage=4, ctx=ctx)
    assert objetivo.state.maestria_desventaja == {"Thor": 2}

    mods = SimpleNamespace(advantage_sources=[], disadvantage_sources=[],
                           bonus=0)
    consumir_marcas(mods, atacante, objetivo, ctx)

    assert "Maestría Sap" in mods.disadvantage_sources
    assert objetivo.state.maestria_desventaja == {}


def test_graze_aplica_el_modificador_de_caracteristica_al_fallar():
    atacante, objetivo = _atacante(), _objetivo()
    ctx = _ctx(combatants=[atacante, objetivo])
    antes = objetivo.hp

    al_fallar(atacante, objetivo, _arma("graze"), ctx=ctx,
              rng=random.Random(1))

    assert objetivo.hp == antes - 3  # mod FUE 16 = +3, sin armadura que restar


def test_graze_sin_modificador_positivo_no_hace_dano():
    atacante = PlayerCharacter(
        name="Plana", max_hp=30, ac=10, level=1,
        abilities=Abilities(str=10, dex=10, con=10, int=10, wis=10, cha=10),
        attacks=[Attack("Daga", "1d4", ability="str", mastery="graze")],
    )
    objetivo = _objetivo()
    antes = objetivo.hp

    al_fallar(atacante, objetivo, _arma("graze"), ctx=_ctx(),
              rng=random.Random(1))

    assert objetivo.hp == antes  # mod 0 → nada


def test_push_y_slow_no_alteran_el_combate():
    atacante, objetivo = _atacante(), _objetivo()
    ctx = _ctx(ronda=1)
    hp_antes = objetivo.hp

    for clave in ("push", "slow"):
        al_acertar(atacante, objetivo, _arma(clave), damage=6,
                   ctx=ctx, rng=_RngNo())

    assert objetivo.hp == hp_antes
    assert not objetivo.conditions.instances
    assert atacante.state.maestria_ventaja == {}
    assert objetivo.state.maestria_desventaja == {}


def test_sin_maestria_no_se_consume_rng_ni_se_resuelve():
    atacante, objetivo = _atacante(), _objetivo()
    arma = _arma("", nombre="Garrote")

    assert resolver_maestria(atacante, arma, _RngSinLlamadas()) == ""
    al_acertar(atacante, objetivo, arma, damage=5, ctx=_ctx(),
               rng=_RngSinLlamadas())
    al_fallar(atacante, objetivo, arma, ctx=_ctx(), rng=_RngSinLlamadas())


def test_el_motor_invoca_topple_al_acertar(monkeypatch):
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    # d20 del ataque → 10 (acierta); la salvación posterior tira con el
    # rng real del test (siempre 1) y falla → PRONE.
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=10, rolls=[10],
                                    mode=RollMode.NORMAL))

    class _RngBajo:
        def randint(self, a: int, b: int) -> int:
            return a

        def randrange(self, n: int) -> int:
            return n - 1

        def random(self) -> float:
            return 1.0

    atacante, objetivo = _atacante(), _objetivo()
    rng = _RngBajo()
    ctx = _ctx(rng, combatants=[atacante, objetivo])
    log: list[str] = []

    atk_mod.attack_roll(atacante, objetivo, atacante.attacks[0], rng, log,
                        ctx=ctx)

    assert any("Topple" in line for line in log), log
    assert objetivo.conditions.has(Condition.PRONE)

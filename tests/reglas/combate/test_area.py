"""Áreas de efecto: selección de objetivos y daño compartido."""
import json
import random
from collections import Counter
from pathlib import Path

import pytest

from dnd_sim.core.abilities import Abilities
from dnd_sim.model.actions import ActionType, CombatContext, TurnResources
from dnd_sim.rules.area import AreaSaveAction, AreaTargeting, select_area_targets
from dnd_sim.model.combatant import Monster, PlayerCharacter
from dnd_sim.core.randomness import sample
from dnd_sim.rules.saves import SaveDamage, SaveResult
from dnd_sim.core.dice import RollMode

FIXTURES = Path(__file__).parents[2] / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _pj(name: str, hp: int = 100, **kwargs) -> PlayerCharacter:
    return PlayerCharacter(
        name=name, max_hp=hp, ac=15, proficiency=2,
        abilities=Abilities(str=14, dex=14, con=14, int=10, wis=10, cha=10),
        attacks=[], **kwargs,
    )


def _npc(name: str = "Cebo", hp: int = 100) -> Monster:
    return Monster(name=name, max_hp=hp, ac=12, abilities=Abilities(), attacks=[])


def _ctx(actor, combatants, rng=None) -> CombatContext:
    return CombatContext(rng=rng or random.Random(1), actor=actor, combatants=list(combatants),
                         round=1, log=[], verbose=True, resources=TurnResources())


def _area_action(effect, targeting=None, name="Aliento de fuego") -> AreaSaveAction:
    return AreaSaveAction(
        name=name, effect=effect,
        targeting=targeting or AreaTargeting(),
        action_type=ActionType.ACTION,
    )


# --- randomness.sample ----------------------------------------------------- #

def test_sample_devuelve_todos_sin_consumir_rng():
    rng = random.Random(1)
    estado = rng.getstate()
    elementos = ["a", "b", "c"]
    assert sample(rng, elementos, 3) == elementos
    assert sample(rng, elementos, 5) == elementos
    assert rng.getstate() == estado, "k >= len(options) no debe consumir RNG"


def test_sample_k_menor_devuelve_distintos_y_uniformes():
    rng = random.Random(7)
    elementos = list(range(10))
    conteo = Counter()
    for _ in range(20000):
        elegidos = sample(rng, elementos, 3)
        assert len(elegidos) == 3
        assert len(set(elegidos)) == 3, "sin repetición"
        conteo.update(elegidos)
    # Uniforme: 0.3 de probabilidad por elemento (20000 * 3 / 10 = 6000).
    for elemento in elementos:
        assert abs(conteo[elemento] / 6000 - 1.0) < 0.03


# --- Selección de objetivos ------------------------------------------------ #

def test_k_uniforme_entre_1_y_el_numero_de_objetivos():
    rng = random.Random(11)
    pjs = [_pj(f"PJ{i}") for i in range(4)]
    actor = _npc()
    ctx = _ctx(actor, [actor] + pjs, rng)

    conteo = Counter()
    for _ in range(20000):
        objetivos = select_area_targets(actor, ctx, AreaTargeting())
        conteo[len(objetivos)] += 1
    for k in (1, 2, 3, 4):
        assert abs(conteo[k] / 20000 - 0.25) <= 0.015, f"k={k}: {conteo[k]}"


def test_cada_pj_es_elegido_aproximadamente_el_62_5_por_ciento():
    rng = random.Random(13)
    pjs = [_pj(f"PJ{i}") for i in range(4)]
    actor = _npc()
    ctx = _ctx(actor, [actor] + pjs, rng)

    conteo = Counter()
    for _ in range(20000):
        for objetivo in select_area_targets(actor, ctx, AreaTargeting()):
            conteo[objetivo.name] += 1
    for nombre in ("PJ0", "PJ1", "PJ2", "PJ3"):
        # media de k = 2.5 sobre 4 objetivos -> 62.5%.
        assert abs(conteo[nombre] / 20000 - 0.625) <= 0.02, f"{nombre}: {conteo[nombre]}"


def test_un_solo_objetivo_no_consume_rng():
    rng = random.Random(3)
    pj = _pj("PJ0")
    actor = _npc()
    ctx = _ctx(actor, [actor, pj], rng)
    estado = rng.getstate()
    objetivos = select_area_targets(actor, ctx, AreaTargeting())
    assert objetivos == [pj]
    assert rng.getstate() == estado, "con un solo objetivo no se sortea nada"


def test_min_y_max_targets_se_respetan():
    rng = random.Random(5)
    pjs = [_pj(f"PJ{i}") for i in range(4)]
    actor = _npc()
    ctx = _ctx(actor, [actor] + pjs, rng)

    for _ in range(500):
        objetivos = select_area_targets(actor, ctx, AreaTargeting(min_targets=2, max_targets=3))
        assert 2 <= len(objetivos) <= 3

    # Un máximo mayor que los objetivos disponibles se recorta.
    for _ in range(200):
        objetivos = select_area_targets(actor, ctx, AreaTargeting(min_targets=1, max_targets=99))
        assert 1 <= len(objetivos) <= 4


def test_min_targets_mayor_que_los_disponibles_afecta_a_todos():
    rng = random.Random(6)
    pjs = [_pj(f"PJ{i}") for i in range(2)]
    actor = _npc()
    ctx = _ctx(actor, [actor] + pjs, rng)
    for _ in range(100):
        objetivos = select_area_targets(actor, ctx, AreaTargeting(min_targets=5, max_targets=9))
        assert len(objetivos) == 2


def test_nunca_se_eligen_aliados_lanzador_ni_muertos():
    rng = random.Random(9)
    vivos = [_pj("PJ0"), _pj("PJ1")]
    muerto = _pj("PJ2")
    muerto.hp = 0
    aliado = _npc("Aliado")
    actor = _npc("Lanzador")

    ctx = _ctx(actor, [actor, aliado, muerto] + vivos, rng)
    for _ in range(2000):
        objetivos = select_area_targets(actor, ctx, AreaTargeting())
        assert objetivos, "debe haber objetivos vivos"
        for objetivo in objetivos:
            assert objetivo in vivos
            assert objetivo is not actor
            assert objetivo is not aliado
            assert objetivo is not muerto


# --- Daño compartido ------------------------------------------------------- #

def _save_forzado(monkeypatch, exitos):
    """Fuerza el resultado de las salvaciones en orden."""
    from dnd_sim.rules import saves as saves_mod

    llamadas = {"n": 0}

    def fake_saving_throw(target, ability, dc, rng, mode=None, *,
                          kind=None, magical=False, **kw):
        index = llamadas["n"]
        llamadas["n"] += 1
        exito = exitos[index] if index < len(exitos) else exitos[-1]
        return SaveResult(
            ability=ability, dc=dc, rolls=[10], bonus=0, total=10,
            success=exito, mode=RollMode.NORMAL,
        )

    monkeypatch.setattr(saves_mod, "saving_throw", fake_saving_throw)
    return llamadas


def test_el_dano_se_tira_una_sola_vez_y_se_comparte(monkeypatch):
    import dnd_sim.rules.area as area_mod

    pjs = [_pj("PJ0"), _pj("PJ1")]
    actor = _npc()
    ctx = _ctx(actor, [actor] + pjs, random.Random(2))
    accion = _area_action(SaveDamage(ability="dex", dc=10, damage="10",
                                     damage_type="fire", on_success="half"),
                          targeting=AreaTargeting(min_targets=2, max_targets=2))
    actor.actions = [accion]

    tiradas = {"n": 0}

    def fake_roll_dice(expr, rng, crit=False):
        tiradas["n"] += 1
        return 20

    monkeypatch.setattr(area_mod, "roll_dice", fake_roll_dice)
    # El primero supera la salvación (mitad), el segundo falla (completo).
    _save_forzado(monkeypatch, [True, False])

    accion.execute(ctx)

    assert tiradas["n"] == 1, "el daño se tira una sola vez para todo el área"
    assert pjs[0].hp == 100 - 10, "mitad de 20"
    assert pjs[1].hp == 100 - 20, "completo del mismo valor base (20)"


def test_la_resistencia_se_aplica_solo_a_quien_la_tiene(monkeypatch):
    import dnd_sim.rules.area as area_mod

    pjs = [_pj("PJ0"), _pj("PJ1", resistances={"fire"})]
    actor = _npc()
    ctx = _ctx(actor, [actor] + pjs, random.Random(2))
    accion = _area_action(SaveDamage(ability="dex", dc=10, damage="10",
                                     damage_type="fire", on_success="none"),
                          targeting=AreaTargeting(min_targets=2, max_targets=2))
    actor.actions = [accion]

    monkeypatch.setattr(area_mod, "roll_dice", lambda expr, rng, crit=False: 20)
    # El primero supera (0 daño), el segundo falla (daño completo).
    _save_forzado(monkeypatch, [True, False])

    accion.execute(ctx)

    assert pjs[0].hp == 100, "con on_success='none' el éxito no inflige daño"
    assert pjs[1].hp == 100 - 10, "la resistencia de fuego reduce el daño base de 20 a 10"


def test_damage_taken_se_dispara_una_vez_por_objetivo(monkeypatch):
    import dnd_sim.rules.area as area_mod
    import dnd_sim.rules.damage as damage_mod

    pjs = [_pj("PJ0"), _pj("PJ1")]
    actor = _npc()
    ctx = _ctx(actor, [actor] + pjs, random.Random(2))
    accion = _area_action(SaveDamage(ability="dex", dc=10, damage="10",
                                     damage_type="fire", on_success="none"),
                          targeting=AreaTargeting(min_targets=2, max_targets=2))
    actor.actions = [accion]

    monkeypatch.setattr(area_mod, "roll_dice", lambda expr, rng, crit=False: 10)
    _save_forzado(monkeypatch, [False, False])

    recibidos = []
    monkeypatch.setattr(damage_mod, "DAMAGE_TAKEN", [lambda **kw: recibidos.append(kw)])
    monkeypatch.setattr(damage_mod, "DAMAGE_TAKEN_CALLBACKS", [])
    monkeypatch.setattr(damage_mod, "DAMAGE_TAKEN_REACTIONS", [])

    accion.execute(ctx)

    assert len(recibidos) == 2, "una reacción por objetivo afectado"
    objetivos = [r["target"] for r in recibidos]
    assert objetivos == pjs


def test_el_orden_del_rng_es_estable_con_semilla():
    pjs = [_pj(f"PJ{i}") for i in range(3)]
    actor = _npc()
    accion = _area_action(SaveDamage(ability="dex", dc=10, damage="2d6",
                                     damage_type="fire", on_success="half"))

    def _correr():
        objetivos = [_pj(f"PJ{i}") for i in range(3)]
        act = _npc()
        ctx = _ctx(act, [act] + objetivos, random.Random(99))
        accion = _area_action(SaveDamage(ability="dex", dc=10, damage="2d6",
                                         damage_type="fire", on_success="half"))
        act.actions = [accion]
        accion.execute(ctx)
        return [o.hp for o in objetivos], list(ctx.log)

    a_hp, a_log = _correr()
    b_hp, b_log = _correr()
    assert a_hp == b_hp
    assert a_log == b_log

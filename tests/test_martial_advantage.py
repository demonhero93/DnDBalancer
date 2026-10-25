"""Martial Advantage del hobgoblin (daño extra con condición de posición).

La ficha (fixture real de la API) declara «an extra 7 (2d6) damage ... if
that creature is within 5 ft. of an ally ... that isn't incapacitated»: los
números se leen de la descripción, la posición no está modelada (se sortea,
igual que Pack Tactics) y el daño entra en el ataque **antes** de los
modificadores del objetivo.
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, Monster, PlayerCharacter
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.engine.combat import attack_roll, run_combat
from dnd_sim.data.loader import load_monster
from dnd_sim.rules.damage import DamageType
from dnd_sim.rules.roll_modifiers import AttackRange

FIXTURES = Path(__file__).parent / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _datos(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _hobgoblin(monkeypatch):
    data = _datos("hobgoblin")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("hobgoblin")


def _espada(hobgoblin):
    return next(a for a in hobgoblin.attacks if a.name == "Longsword")


def _pj(ac: int = 15) -> PlayerCharacter:
    return PlayerCharacter(
        name="Guerrero", max_hp=60, ac=ac, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[],
    )


def _aliado() -> Monster:
    """Otro NPC vivo: aliado del hobgoblin."""
    return Monster(name="Compañero", max_hp=20, ac=12,
                   abilities=Abilities(), attacks=[])


def _ctx(actor, combatantes, semilla: int = 1) -> CombatContext:
    return CombatContext(rng=random.Random(semilla), actor=actor,
                         combatants=list(combatantes), round=1,
                         log=[], verbose=True, resources=TurnResources())


# --- Carga de la ficha ------------------------------------------------------ #

def test_el_hobgoblin_carga_su_martial_advantage(monkeypatch):
    hobgoblin = _hobgoblin(monkeypatch)
    assert [type(t).__name__ for t in hobgoblin.traits] == ["MartialAdvantage"]
    rasgo = hobgoblin.traits[0]
    assert rasgo.name == "Martial Advantage"
    # Los números salen de la descripción («an extra 7 (2d6)»).
    assert rasgo.bonus == 7
    assert rasgo.dice == "2d6"


def test_una_descripcion_no_interpretable_no_aporta_daño():
    from dnd_sim.data.trait_parser import parse_traits
    rasgo = parse_traits({"special_abilities": [
        {"name": "Martial Advantage", "desc": "Hace daño extra."},
    ]})[0]
    assert rasgo.dice == ""
    atacante = Monster(name="A", max_hp=10, ac=10, abilities=Abilities(),
                       attacks=[])
    aliado = Monster(name="B", max_hp=10, ac=10, abilities=Abilities(),
                     attacks=[])
    objetivo = Monster(name="C", max_hp=10, ac=10, abilities=Abilities(),
                       attacks=[])
    ctx = _ctx(atacante, [atacante, aliado, objetivo], 1)
    # Con aliados el sorteo de posición se hace, pero sin dados no hay con
    # qué calcular el daño: el rasgo se abstiene.
    assert rasgo.extra_attack_damage(atacante, objetivo, AttackRange.MELEE,
                                     ctx=ctx, rng=ctx.rng) == 0


# --- Reglas ----------------------------------------------------------------- #

def test_sin_aliados_no_suma_daño_ni_consume_rng(monkeypatch):
    hobgoblin = _hobgoblin(monkeypatch)
    rasgo = hobgoblin.traits[0]
    objetivo = _pj()
    ctx = _ctx(hobgoblin, [hobgoblin, objetivo], 3)   # solo hostiles: sin aliados
    rng = ctx.rng
    antes = rng.getstate()
    assert rasgo.extra_attack_damage(hobgoblin, objetivo, AttackRange.MELEE,
                                     ctx=ctx, rng=rng) == 0
    assert rng.getstate() == antes, "sin aliados no se consume RNG"


def test_con_aliados_el_daño_extra_es_aleatorio(monkeypatch):
    hobgoblin = _hobgoblin(monkeypatch)
    rasgo = hobgoblin.traits[0]
    objetivo = _pj()
    aliado = _aliado()
    resultados = []
    for semilla in range(40):
        ctx = _ctx(hobgoblin, [hobgoblin, aliado, objetivo], semilla)
        resultados.append(rasgo.extra_attack_damage(
            hobgoblin, objetivo, AttackRange.MELEE, ctx=ctx, rng=ctx.rng))
    # 2d6 siempre está entre 2 y 12 y el sorteo es 50 %.
    assert 0 in resultados, "algún sorteo debe salir a la papeleta"
    assert any(r >= 2 for r in resultados), "algún sorteo debe aplicarse"
    assert all(r == 0 or 2 <= r <= 12 for r in resultados), resultados


def test_el_daño_extra_entra_en_el_ataque_y_se_resiste(monkeypatch):
    """Lo que suma el rasgo también lo resiste el objetivo."""
    hobgoblin = _hobgoblin(monkeypatch)
    aliado = _aliado()
    aplicado = 0
    for semilla in range(1, 21):
        normal = _pj(ac=1)                     # CA 1: siempre impacta
        resistente = _pj(ac=1)
        resistente.resistances = {DamageType.SLASHING}
        ctx1 = _ctx(hobgoblin, [hobgoblin, aliado, normal], semilla)
        attack_roll(hobgoblin, normal, _espada(hobgoblin), ctx1.rng, ctx1.log,
                    ctx=ctx1)
        if not any("daño extra" in linea for linea in ctx1.log):
            continue                           # ese sorteo no aplicó el rasgo
        ctx2 = _ctx(hobgoblin, [hobgoblin, aliado, resistente], semilla)
        attack_roll(hobgoblin, resistente, _espada(hobgoblin), ctx2.rng,
                    ctx2.log, ctx=ctx2)
        perdido = normal.max_hp - normal.hp
        assert perdido > 0
        assert resistente.max_hp - resistente.hp == perdido // 2, \
            f"semilla {semilla}: la resistencia debe cortar también el extra"
        aplicado += 1
    assert aplicado, "alguna semilla debe aplicar Martial Advantage"


def test_en_critico_los_dados_extra_llegan_con_crit(monkeypatch):
    hobgoblin = _hobgoblin(monkeypatch)
    rasgo = hobgoblin.traits[0]
    aliado = _aliado()
    objetivo = _pj()
    import dnd_sim.rules.traits as traits_mod
    original = traits_mod.roll_dice
    tiradas: list = []

    def espia(dados, rng=None, crit=False, **kw):
        tiradas.append((str(dados), bool(crit)))
        return original(dados, rng, crit=crit, **kw)

    monkeypatch.setattr(traits_mod, "roll_dice", espia)
    for semilla in range(1, 21):
        ctx = _ctx(hobgoblin, [hobgoblin, aliado, objetivo], semilla)
        rasgo.extra_attack_damage(hobgoblin, objetivo, AttackRange.MELEE,
                                  crit=True, ctx=ctx, rng=ctx.rng)
    assert ("2d6", True) in tiradas, \
        "los dados del extra deben tirarse con crit=True como el daño principal"


# --- Integración con el motor ----------------------------------------------- #

def test_el_daño_extra_aparece_en_el_log_del_ataque(monkeypatch):
    hobgoblin = _hobgoblin(monkeypatch)
    aliado = _aliado()
    objetivo = _pj(ac=1)
    for semilla in range(1, 21):
        ctx = _ctx(hobgoblin, [hobgoblin, aliado, objetivo], semilla)
        attack_roll(hobgoblin, objetivo, _espada(hobgoblin), ctx.rng, ctx.log,
                    ctx=ctx)
        if any("daño extra" in linea for linea in ctx.log):
            assert any("Martial Advantage" in linea for linea in ctx.log)
            return
    raise AssertionError("alguna semilla debe aplicar Martial Advantage")


def test_martial_advantage_actua_en_un_combate_completo(monkeypatch):
    hobgoblin = _hobgoblin(monkeypatch)
    hobgoblin2 = _hobgoblin(monkeypatch)
    objetivo = _pj(ac=15)
    objetivo.max_hp = 300
    objetivo.hp = 300
    res = run_combat([hobgoblin, hobgoblin2, objetivo], random.Random(4),
                     verbose=True, max_rounds=6)
    assert any("daño extra" in linea for linea in res.log), \
        "con dos hobgoblins, alguno de sus golpes debe llevar el extra"

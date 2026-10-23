"""Enlarge del duergar y hechizo Enlarge/Reduce (estado compartido).

Ambos comparten la condición ``ENLARGED`` (ventaja en pruebas y
salvaciones de Fuerza) y la misma máquina de estado
(``SpellStateAction`` + ``StateEffect``). El daño crece según la fuente:

- El rasgo del duergar dice «doubles its damage dice» y su ficha trae los
  dados duplicados («or 11 (2d8 + 2) ... while enlarged»): el loader los
  calcula en ``Attack.enlarged_damage``.
- El hechizo dice «deal 1d4 extra damage» con las armas agrandadas.

Todas las fichas salen de fixtures reales de la API.
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, PlayerCharacter
from dnd_sim.actions import CombatContext, TurnResources
from dnd_sim.attack import Attack
from dnd_sim.combat import attack_roll, run_combat
from dnd_sim.combatant import Monster
from dnd_sim.conditions import Condition, apply_condition, end_turn
from dnd_sim.data.loader import load_monster
from dnd_sim.data.spell_parser import build_spell_actions, parse_spell
from dnd_sim.dice import doblar_dados
from dnd_sim.roll_modifiers import check_modifiers, save_modifiers
from dnd_sim.spells import SpellAction, SpellStateAction, Spellcasting, spell_action
from dnd_sim.usage import UsageKind

FIXTURES = Path(__file__).parent / "fixtures"
SPELLS = FIXTURES / "spells"


# --- Utilidades ------------------------------------------------------------- #

def _datos(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _spell_data(index: str) -> dict:
    return json.loads((SPELLS / f"{index}.json").read_text(encoding="utf-8"))


def _duergar(monkeypatch) -> Monster:
    data = _datos("duergar")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("duergar")


def _pj(name: str = "Guerrero", hp: int = 60, ac: int = 15,
        ability: str = "str") -> PlayerCharacter:
    return PlayerCharacter(
        name=name, max_hp=hp, ac=ac, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[Attack(name="Espada", damage="1d8", ability=ability,
                        attack_bonus=5, damage_bonus=3)],
    )


def _ogro(monkeypatch) -> Monster:
    """Enemigo de prueba (los PJ son todos del mismo bando)."""
    data = _datos("ogre")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("ogre")


def _ctx(actor, combatants, rng=None, log=None) -> CombatContext:
    return CombatContext(rng=rng or random.Random(1), actor=actor,
                         combatants=list(combatants), round=1,
                         log=log if log is not None else [], verbose=True,
                         resources=TurnResources())


def _accion(m, nombre):
    return next(a for a in m.actions if getattr(a, "name", "") == nombre)


def _ataque(m, nombre):
    return next(a for a in m.attacks if a.name == nombre)


def _spy_roll_dice(monkeypatch) -> list:
    """Sustituye ``dnd_sim.combat.roll_dice`` por un espía que sí tira."""
    import dnd_sim.combat as combat
    llamadas = []
    original = combat.roll_dice

    def espia(expr, rng, crit=False):
        llamadas.append(expr)
        return original(expr, rng, crit=crit)

    monkeypatch.setattr(combat, "roll_dice", espia)
    return llamadas


# --- Carga del duergar ------------------------------------------------------ #

def test_el_duergar_carga_su_enlarge_como_accion_de_estado(monkeypatch):
    duergar = _duergar(monkeypatch)
    enlarge = _accion(duergar, "Enlarge")
    assert isinstance(enlarge, SpellStateAction)
    assert enlarge.effect.condition is Condition.ENLARGED
    assert enlarge.effect.duration_rounds == 10   # 1 minuto
    assert enlarge.effect.target == "self"
    # «recharge after rest»: un uso por combate (no se modelan descansos).
    assert enlarge.usage.kind is UsageKind.PER_DAY
    assert enlarge.usage.uses_left == 1


def test_los_ataques_del_duergar_traen_su_variante_agrandada(monkeypatch):
    duergar = _duergar(monkeypatch)
    # La ficha dice: «6 (1d8 + 2) ... or 11 (2d8 + 2) while enlarged».
    assert _ataque(duergar, "War Pick").damage == "1d8+2"
    assert _ataque(duergar, "War Pick").enlarged_damage == "2d8+2"
    # «5 (1d6 + 2) ... or 9 (2d6 + 2) while enlarged».
    assert _ataque(duergar, "Javelin").enlarged_damage == "2d6+2"


def test_doblar_dados_duplica_los_dados_y_no_el_bonus():
    assert doblar_dados("1d8+2") == "2d8+2"
    assert doblar_dados("1d6") == "2d6"
    assert doblar_dados("2d6+3") == "4d6+3"
    assert doblar_dados("0") == "0"


def test_solo_el_duergar_con_enlarge_declara_variante(monkeypatch):
    data = _datos("ogre")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    ogro = load_monster("ogre")
    # El ogre no tiene acción de tamaño: sus ataques no declaran variante.
    assert all(getattr(a, "enlarged_damage", None) is None
               for a in ogro.attacks)


# --- El estado ENLARGED ----------------------------------------------------- #

def test_enlarge_aplica_el_estado_durante_10_rondas(monkeypatch):
    duergar = _duergar(monkeypatch)
    objetivo = _pj()
    ctx = _ctx(duergar, [duergar, objetivo])
    _accion(duergar, "Enlarge").execute(ctx)
    assert duergar.conditions.has(Condition.ENLARGED)
    instancia = next(i for i in duergar.conditions.instances
                     if i.condition is Condition.ENLARGED)
    assert instancia.remaining_rounds == 10
    assert any("queda agrandado" in l for l in ctx.log)


def test_el_estado_caduca_tras_10_rondas(monkeypatch):
    duergar = _duergar(monkeypatch)
    objetivo = _pj()
    ctx = _ctx(duergar, [duergar, objetivo])
    _accion(duergar, "Enlarge").execute(ctx)
    for _ in range(10):
        end_turn(duergar, ctx)
    assert not duergar.conditions.has(Condition.ENLARGED)


def test_agrandado_da_ventaja_en_pruebas_y_salvaciones_de_fuerza():
    pj = _pj()
    apply_condition(pj, Condition.ENLARGED, _ctx(pj, [pj]), duration_rounds=10)
    for mods in (save_modifiers(pj, "str"), check_modifiers(pj, "str")):
        assert "agrandado" in mods.advantage_sources
    # Otras características: sin cambios.
    assert "agrandado" not in save_modifiers(pj, "dex").advantage_sources
    assert "agrandado" not in check_modifiers(pj, "dex").advantage_sources


# --- Daño agrandado --------------------------------------------------------- #

def test_el_duergar_agrandado_tira_sus_dados_duplicados(monkeypatch):
    duergar = _duergar(monkeypatch)
    objetivo = _pj()
    ctx = _ctx(duergar, [duergar, objetivo])
    apply_condition(duergar, Condition.ENLARGED, ctx, duration_rounds=10)
    llamadas = _spy_roll_dice(monkeypatch)
    # Semilla 5: primer d20 = 20 (impacto y crítico garantizados).
    attack_roll(duergar, objetivo, _ataque(duergar, "War Pick"),
                random.Random(5), ctx.log, ctx=ctx)
    assert llamadas == ["2d8+2"], "debe usar la variante de la ficha"
    # Los dados duplicados ya son la variante: no se suma el +1d4 del hechizo.
    assert "1d4" not in llamadas


def test_sin_agrandar_tira_los_dados_normales(monkeypatch):
    duergar = _duergar(monkeypatch)
    objetivo = _pj()
    ctx = _ctx(duergar, [duergar, objetivo])
    llamadas = _spy_roll_dice(monkeypatch)
    attack_roll(duergar, objetivo, _ataque(duergar, "War Pick"),
                random.Random(5), ctx.log, ctx=ctx)
    assert llamadas == ["1d8+2"]


def test_un_arma_gana_1d4_si_el_lanzador_fue_agrandado_por_el_hechizo(
        monkeypatch):
    pj = _pj()
    enemigo = _ogro(monkeypatch)
    ctx = _ctx(pj, [pj, enemigo])
    apply_condition(pj, Condition.ENLARGED, ctx, duration_rounds=10)
    llamadas = _spy_roll_dice(monkeypatch)
    arma = next(a for a in pj.attacks if a.name == "Espada")
    attack_roll(pj, enemigo, arma, random.Random(5), ctx.log, ctx=ctx)
    # Dados normales del arma + el extra de «deal 1d4 extra damage».
    assert llamadas == ["1d8", "1d4"]


def test_los_ataques_de_hechizo_no_reciben_el_1d4(monkeypatch):
    """«Attacks with them [weapons]»: los hechizos usan su característica
    de lanzamiento, no Fuerza."""
    pj = _pj(ability="int")
    enemigo = _ogro(monkeypatch)
    ctx = _ctx(pj, [pj, enemigo])
    apply_condition(pj, Condition.ENLARGED, ctx, duration_rounds=10)
    llamadas = _spy_roll_dice(monkeypatch)
    hechizo = Attack(name="Dardo mágico", damage="1d4", ability="int",
                     attack_bonus=6)
    attack_roll(pj, enemigo, hechizo, random.Random(5), ctx.log, ctx=ctx)
    assert llamadas == ["1d4"]


# --- El hechizo Enlarge/Reduce ---------------------------------------------- #

def test_el_hechizo_enlarge_es_un_estado_self():
    spell = parse_spell(_spell_data("enlarge-reduce"), "Test")
    assert spell.kind == "state"
    assert spell.state.condition is Condition.ENLARGED
    assert spell.state.duration_rounds == 10
    assert spell.state.target == "self"
    accion = spell_action(spell, Spellcasting(level=5, ability="int",
                                              attack_bonus=6, save_dc=14))
    assert isinstance(accion, SpellAction)
    assert isinstance(accion.effect, SpellStateAction)
    assert accion.concentration is True


def test_lanzar_el_hechizo_agranda_al_lanzador():
    spell = parse_spell(_spell_data("enlarge-reduce"), "Test")
    accion = spell_action(spell, Spellcasting(level=5, ability="int",
                                              attack_bonus=6, save_dc=14))
    lanzador = _pj(name="Lanzador")
    objetivo = _pj(name="Objetivo")
    ctx = _ctx(lanzador, [lanzador, objetivo])
    accion.effect.execute(ctx)
    assert lanzador.conditions.has(Condition.ENLARGED)
    assert not objetivo.conditions.has(Condition.ENLARGED)


def test_un_lanzador_carga_el_hechizo_con_su_pool_de_slots():
    data = {
        "name": "Lanzador",
        "proficiency_bonus": 4,
        "special_abilities": [{
            "name": "Spellcasting",
            "spellcasting": {
                "ability": {"index": "int"},
                "dc": 13,
                "modifier": 6,
                "level": 5,
                "slots": {"2": 3},
                "spells": [{"name": "Enlarge/Reduce", "level": 2,
                            "url": "/api/2014/spells/enlarge-reduce"}],
            },
        }],
    }
    acciones = build_spell_actions(
        data, "Test", get_spell=lambda indice, **k: _spell_data(indice))
    assert len(acciones) == 1
    assert acciones[0].name == "Enlarge/Reduce"
    assert acciones[0].usage.uses_left == 3


# --- Integración con el motor ----------------------------------------------- #

def test_un_combate_completo_con_duergar(monkeypatch):
    duergar = _duergar(monkeypatch)
    pjs = [_pj(name="A"), _pj(name="B")]
    res = run_combat([*pjs, duergar], random.Random(2), verbose=True,
                     max_rounds=20)
    assert any("queda agrandado" in l for l in res.log), \
        "el duergar debe poder agrandarse en combate"

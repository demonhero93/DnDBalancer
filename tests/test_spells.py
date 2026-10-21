"""Hechizos: estructura, reglas y estados nuevos (concentración, hechizado).

Los hechizos salen de la API (fixtures reales); los únicos objetos definidos a
mano son los PJ de prueba.
"""
import json
import random
import warnings
from pathlib import Path

import pytest

from dnd_sim import Abilities, Monster, PlayerCharacter
from dnd_sim.actions import AttackAction, CombatContext, SaveAction, TurnResources
from dnd_sim.checks import ability_check
from dnd_sim.area import AreaSaveAction
from dnd_sim.combat import run_combat
from dnd_sim.conditions import Condition, apply_condition
from dnd_sim.data.loader import load_monster
from dnd_sim.data.spell_parser import parse_spell, parse_spellcasting
from dnd_sim.roll_modifiers import AttackRange, attack_modifiers
from dnd_sim.spells import (
    HealAction, SpellAction, SpellAttackAction, SpellFixedDamageAction,
    Spellcasting, spell_action,
)

FIXTURES = Path(__file__).parent / "fixtures"
SPELLS = FIXTURES / "spells"


# --- Utilidades ------------------------------------------------------------- #

def _spell_data(index: str) -> dict:
    return json.loads((SPELLS / f"{index}.json").read_text(encoding="utf-8"))


def _pj(name: str = "Guerrero", hp: int = 100, ac: int = 15, **kwargs) -> PlayerCharacter:
    return PlayerCharacter(
        name=name, max_hp=hp, ac=ac, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[], **kwargs,
    )


def _npc(name: str = "Lanzador", hp: int = 100) -> Monster:
    return Monster(name=name, max_hp=hp, ac=12, abilities=Abilities(), attacks=[])


def _ctx(actor, combatants, rng=None, log=None) -> CombatContext:
    return CombatContext(rng=rng or random.Random(1), actor=actor,
                         combatants=list(combatants), round=1,
                         log=log if log is not None else [], verbose=True,
                         resources=TurnResources())


def _spellcasting(level: int = 18) -> Spellcasting:
    """Datos de un lanzador de nivel 18 (como el lich de la API)."""
    return Spellcasting(ability="int", save_dc=20, attack_bonus=12, level=level)


# --- Estructura ------------------------------------------------------------ #

def test_el_lanzador_se_lee_de_los_special_abilities():
    data = json.loads((FIXTURES / "lich.json").read_text(encoding="utf-8"))
    sc = parse_spellcasting(data)
    assert sc is not None
    assert sc.ability == "int"
    assert sc.save_dc == 20
    assert sc.attack_bonus == 12
    assert sc.level == 18
    cantrips = [s for s in sc.spells if s["level"] == 0]
    assert {s["name"] for s in cantrips} == {
        "Mage Hand", "Prestidigitation", "Ray of Frost"}


def test_un_monstruo_sin_lanzar_hechizos_no_tiene_estado():
    data = json.loads((FIXTURES / "ogre.json").read_text(encoding="utf-8"))
    assert parse_spellcasting(data) is None


def test_un_cantrip_de_ataque_se_convierte_en_accion_de_ataque():
    raw = _spell_data("ray-of-frost")
    spell = parse_spell(raw, "Test", _spellcasting(level=1))
    assert spell.kind == "attack"
    assert spell.damage == "1d8"       # nivel 1 del lanzador
    assert spell.damage_type == "cold"
    assert spell.attack_type == "ranged"

    accion = spell_action(spell, _spellcasting(level=1))
    assert isinstance(accion, SpellAction)
    assert isinstance(accion.effect, AttackAction)
    assert accion.effect.attack.range_type is AttackRange.RANGED
    assert accion.effect.usage is None, "los cantrips se lanzan a voluntad"


def test_el_dano_del_cantrip_escala_con_el_nivel_del_lanzador():
    raw = _spell_data("ray-of-frost")
    spell = parse_spell(raw, "Test", _spellcasting(level=18))
    assert spell.damage == "4d8"       # nivel 17+


def test_un_cantrip_con_salvacion_usa_la_cd_del_lanzador():
    raw = _spell_data("vicious-mockery")
    spell = parse_spell(raw, "Test", _spellcasting(level=1))
    assert spell.kind == "save"
    assert spell.dc_ability == "wis"
    assert spell.dc_success == "none"

    accion = spell_action(spell, _spellcasting(level=1))
    assert isinstance(accion.effect, SaveAction)
    assert accion.effect.effect.dc == 20      # la CD del lanzador
    assert accion.effect.effect.ability == "wis"
    assert accion.effect.effect.damage == "1d4"


def test_un_cantrip_con_varios_elementos_hace_un_ataque_por_elemento():
    """Eldritch Blast: un ataque independiente por rayo (nivel 11+: 4)."""
    raw = _spell_data("eldritch-blast")
    spell = parse_spell(raw, "Test", _spellcasting(level=18))
    assert spell.elements == 4
    accion = spell_action(spell, _spellcasting(level=18))
    assert isinstance(accion.effect, SpellAttackAction)
    assert len(accion.effect.attacks) == 4


def test_los_elementos_se_eligen_al_azar():
    raw = _spell_data("eldritch-blast")
    spell = parse_spell(raw, "Test", _spellcasting(level=18))
    accion = spell_action(spell, _spellcasting(level=18))
    lanzador = _npc()
    pjs = [_pj(f"PJ{i}") for i in range(3)]
    ctx = _ctx(lanzador, [lanzador] + pjs, rng=random.Random(4))
    ctx.combatants = [lanzador] + pjs
    accion.effect.execute(ctx)
    # 4 rayos a 3 objetivos: al menos dos han sido alcanzados.
    alcanzados = [p for p in pjs if p.hp < p.max_hp]
    assert len(alcanzados) >= 2


# --- Reglas de los hechizos ------------------------------------------------ #

def test_los_hechizos_de_un_minuto_o_mas_se_ignoran():
    raw = _spell_data("mending")
    with pytest.warns(UserWarning, match="1 minuto"):
        assert parse_spell(raw, "Test", _spellcasting()) is None


def test_los_hechizos_solo_de_movimiento_se_ignoran():
    raw = _spell_data("haste")
    with pytest.warns(UserWarning, match="movimiento"):
        assert parse_spell(raw, "Test", _spellcasting()) is None


def test_los_hechizos_de_utilidad_se_ignoran_pero_no_por_movimiento():
    raw = _spell_data("mage-hand")
    with pytest.warns(UserWarning, match="utilidad"):
        assert parse_spell(raw, "Test", _spellcasting()) is None


def test_la_curacion_solo_se_lanza_contra_un_aliado_herido():
    raw = _spell_data("cure-wounds")
    spell = parse_spell(raw, "Test", _spellcasting())
    assert spell.kind == "heal"
    accion = spell_action(spell, _spellcasting())
    assert isinstance(accion.effect, HealAction)

    lanzador = _npc()
    aliado = Monster(name="Aliado", max_hp=100, ac=12,
                     abilities=Abilities(), attacks=[])
    enemigo = _pj("Enemigo", hp=50)
    ctx = _ctx(lanzador, [lanzador, aliado, enemigo])

    # Sin aliados heridos: la acción no se puede usar.
    assert not accion.can_use(ctx)
    aliado.hp = 40
    assert accion.can_use(ctx)

    # La curación va a un aliado herido (nunca al enemigo).
    accion.execute(ctx)
    assert aliado.hp > 40
    assert enemigo.hp == 50


def test_los_cantrips_no_gastan_usos_ni_slots():
    raw = _spell_data("fire-bolt")
    spell = parse_spell(raw, "Test", _spellcasting())
    accion = spell_action(spell, _spellcasting())
    assert accion.usage is None
    assert accion.effect.usage is None


# --- Concentración --------------------------------------------------------- #

def test_los_hechizos_con_concentracion_crean_el_estado():
    raw = _spell_data("guidance")
    spell = parse_spell(raw, "Test", _spellcasting())
    assert spell.concentration is True
    assert spell.kind == "state"
    assert spell.state.condition is Condition.GUIDED
    assert spell.state.target == "ally"

    lanzador = _npc()
    aliado = Monster(name="Aliado", max_hp=100, ac=12,
                     abilities=Abilities(), attacks=[])
    ctx = _ctx(lanzador, [lanzador, aliado])
    accion = spell_action(spell, _spellcasting())
    accion.execute(ctx)
    assert lanzador.conditions.has(Condition.CONCENTRATION)
    assert aliado.conditions.has(Condition.GUIDED)


def test_solo_se_mantiene_una_concentracion():
    from dnd_sim.spells import apply_concentration
    lanzador = _npc()
    ctx = _ctx(lanzador, [lanzador])
    apply_concentration(lanzador, ctx, 10)
    assert lanzador.conditions.has(Condition.CONCENTRATION)
    apply_concentration(lanzador, ctx, 5)
    instancias = [i for i in lanzador.conditions.instances
                  if i.condition is Condition.CONCENTRATION]
    assert len(instancias) == 1
    assert instancias[0].remaining_rounds == 5


def test_el_hechizo_verdadero_da_ventaja_en_los_ataques():
    lanzador = _npc()
    objetivo = _pj("Objetivo")
    ctx = _ctx(lanzador, [lanzador, objetivo])
    from dnd_sim.attack import Attack
    ataque = Attack("Golpe", "1d6", ability="str", attack_bonus=5, damage_bonus=0)
    antes = attack_modifiers(lanzador, objetivo, ataque).mode
    apply_condition(lanzador, Condition.TRUE_STRUCK, ctx)
    despues = attack_modifiers(lanzador, objetivo, ataque).mode
    assert antes.value == "normal"
    assert despues.value == "advantage"


def test_la_guia_suma_un_d4_a_una_prueba_y_se_consume():
    objetivo = _pj("Objetivo")
    ctx = _ctx(objetivo, [objetivo])
    apply_condition(objetivo, Condition.GUIDED, ctx)
    rng = random.Random(7)
    resultado = ability_check(objetivo, "dex", 10, rng)
    assert 1 <= resultado.bonus - 3 <= 4   # +3 (DES) + 1..4 (la guía)
    assert not objetivo.conditions.has(Condition.GUIDED), "la guía se consume"


# --- Hechizado: los objetivos se invierten --------------------------------- #

def test_el_hechizo_de_hechizar_deja_el_estado_hechizado():
    """El hechizo de hechizar deja al objetivo CHARMED si falla la salvación."""
    raw = _spell_data("charm-person")
    spell = parse_spell(raw, "Test", _spellcasting())
    assert spell.kind == "condition"
    assert spell.condition.condition is Condition.CHARMED
    assert spell.condition.save_ability == "wis"
    assert spell.condition.dc == 20        # la CD del lanzador

    accion = spell_action(spell, _spellcasting())
    objetivo = _pj("Objetivo")
    objetivo.save_overrides["wis"] = -30  # falla la salvación siempre
    lanzador = _npc()
    ctx = _ctx(lanzador, [lanzador, objetivo])
    accion.execute(ctx)
    assert objetivo.conditions.has(Condition.CHARMED)
    assert objetivo.charmed_by is lanzador


# --- Hechizos de nivel 1 --------------------------------------------------- #

def test_el_tiempo_de_casteo_marca_el_tipo_de_accion():
    """1 action -> acción; 1 bonus action -> acción bonus; 1 reaction -> reacción."""
    from dnd_sim.actions import ActionType
    esperado = {
        "burning-hands": ActionType.ACTION,
        "healing-word": ActionType.BONUS_ACTION,
        "hellish-rebuke": ActionType.REACTION,
    }
    for indice, tipo in esperado.items():
        raw = _spell_data(indice)
        spell = parse_spell(raw, "Test", _spellcasting())
        assert spell is not None, indice
        assert spell.action_type is tipo, indice
        accion = spell_action(spell, _spellcasting())
        assert accion.action_type is tipo, indice


def test_los_rituales_se_ignoran():
    raw = _spell_data("detect-magic")
    assert raw.get("ritual") is True
    with pytest.warns(UserWarning, match="ritual"):
        assert parse_spell(raw, "Test", _spellcasting()) is None


def test_los_hechizos_de_movimiento_se_ignoran():
    for indice in ("longstrider", "jump", "feather-fall"):
        raw = _spell_data(indice)
        with pytest.warns(UserWarning, match="movimiento"):
            assert parse_spell(raw, "Test", _spellcasting()) is None


def test_los_hechizos_que_crean_objetos_sin_efecto_se_ignoran():
    for indice in ("create-or-destroy-water", "goodberry"):
        raw = _spell_data(indice)
        with pytest.warns(UserWarning, match="crea objetos"):
            assert parse_spell(raw, "Test", _spellcasting()) is None


def test_las_ilusiones_sin_estado_en_el_rival_se_ignoran():
    for indice in ("disguise-self", "silent-image"):
        raw = _spell_data(indice)
        with pytest.warns(UserWarning, match="ilusión"):
            assert parse_spell(raw, "Test", _spellcasting()) is None


def test_el_dano_de_un_hechizo_con_slot_escala_con_el_slot():
    """Con un slot de nivel 1, las Manos Ardientes hacen 3d6 (no 11d6)."""
    raw = _spell_data("burning-hands")
    spell = parse_spell(raw, "Test", _spellcasting(level=18))
    assert spell.damage == "3d6"
    assert spell.damage_type == "fire"
    assert spell.dc_ability == "dex"
    assert spell.area is True

    accion = spell_action(spell, _spellcasting(level=18))
    assert isinstance(accion.effect, AreaSaveAction)
    assert accion.effect.effect.dc == 20      # la CD del lanzador
    assert accion.effect.effect.damage == "3d6"


def test_los_hechizos_de_nivel_1_consumen_slots(monkeypatch):
    """Todos los hechizos de nivel 1 comparten el mismo pool de slots."""
    data = json.loads((FIXTURES / "lich.json").read_text(encoding="utf-8"))
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: data)
    monkeypatch.setattr("dnd_sim.data.api_client.get_spell",
                        lambda index, **kw: _spell_data(index))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        lich = load_monster("lich")
    con_slots = [a for a in lich.actions
                 if getattr(a, "usage", None) is not None]
    assert con_slots, "el lich debe cargar hechizos de nivel 1"
    usages = {id(a.usage) for a in con_slots}
    assert len(usages) == 1, "el pool de slots es compartido"
    pool = con_slots[0].usage
    assert pool.uses_max == 4                 # slots de nivel 1 del lich

    # Los cantrips no gastan slots.
    cantrips = [a for a in lich.actions
                if getattr(a, "name", "") == "Ray of Frost"]
    assert cantrips and cantrips[0].usage is None


def test_un_slot_gastado_impide_lanzar_mas_hechizos_de_nivel_1(monkeypatch):
    data = json.loads((FIXTURES / "lich.json").read_text(encoding="utf-8"))
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: data)
    monkeypatch.setattr("dnd_sim.data.api_client.get_spell",
                        lambda index, **kw: _spell_data(index))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        lich = load_monster("lich")
    con_slots = [a for a in lich.actions if getattr(a, "usage", None) is not None]
    pool = con_slots[0].usage
    for _ in range(pool.uses_max):
        pool.spend()
    assert not pool.available
    for accion in con_slots:
        assert not accion.can_use()


def test_el_proyectil_magico_es_dano_automatico():
    raw = _spell_data("magic-missile")
    spell = parse_spell(raw, "Test", _spellcasting(level=18))
    assert spell.kind == "fixed"
    assert spell.damage == "3d4+3"
    accion = spell_action(spell, _spellcasting(level=18))
    assert isinstance(accion.effect, SpellFixedDamageAction)


def test_la_luz_de_hadas_senala_al_objetivo():
    """Faerie Fire: el objetivo señalado otorga ventaja a los atacantes."""
    raw = _spell_data("faerie-fire")
    spell = parse_spell(raw, "Test", _spellcasting(level=18))
    assert spell.kind == "condition"
    assert spell.condition.condition is Condition.MARKED

    atacante = _npc()
    objetivo = _pj("Objetivo")
    ctx = _ctx(atacante, [atacante, objetivo])
    from dnd_sim.attack import Attack
    ataque = Attack("Golpe", "1d6", ability="str", attack_bonus=5, damage_bonus=0)
    assert attack_modifiers(atacante, objetivo, ataque).mode.value == "normal"
    apply_condition(objetivo, Condition.MARKED, ctx)
    assert attack_modifiers(atacante, objetivo, ataque).mode.value == "advantage"


def test_el_hechizado_invierte_los_objetivos_de_ataque():
    """Un combatiente hechizado ataca a los de su propio bando."""
    from dnd_sim.targeting import valid_targets

    heroe = _pj("Guerrero")
    dragon = Monster(name="Dragón", max_hp=100, ac=15,
                     abilities=Abilities(), attacks=[])
    ctx = _ctx(heroe, [heroe, dragon])

    # Sin hechizar: el héroe ataca al dragón.
    assert valid_targets(heroe, ctx=ctx) == [dragon]

    apply_condition(heroe, Condition.CHARMED, ctx, source=dragon)
    # Hechizado: el objetivo se invierte (ya no es el dragón).
    assert dragon not in valid_targets(heroe, ctx=ctx)


def test_el_hechizado_ataca_a_los_de_su_propio_bando():
    from dnd_sim.targeting import valid_targets

    heroe = _pj("Guerrero")
    mago = Monster(name="Mago", max_hp=100, ac=15, abilities=Abilities(), attacks=[])
    ctx = _ctx(heroe, [heroe, mago])
    apply_condition(heroe, Condition.CHARMED, ctx, source=mago)
    # El mago es ahora "aliado" del hechizado: no es un objetivo.
    assert mago not in valid_targets(heroe, ctx=ctx)


# --- Integración con los monstruos ----------------------------------------- #

def test_el_lich_carga_su_cantrip_utile(monkeypatch):
    data = json.loads((FIXTURES / "lich.json").read_text(encoding="utf-8"))
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: data)
    monkeypatch.setattr("dnd_sim.data.api_client.get_spell",
                        lambda index, **kw: _spell_data(index))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        lich = load_monster("lich")
    nombres = [getattr(a, "name", "") for a in lich.actions]
    assert "Ray of Frost" in nombres
    # Los cantrips inútiles se omiten con aviso.
    assert "Mage Hand" not in nombres
    assert "Prestidigitation" not in nombres


def test_el_ogre_no_carga_hechizos(monkeypatch):
    data = json.loads((FIXTURES / "ogre.json").read_text(encoding="utf-8"))
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: data)
    ogre = load_monster("ogre")
    assert not [a for a in ogre.actions if isinstance(a, SpellAction)]


def test_un_cantrip_se_puede_lanzar_en_cada_turno(monkeypatch):
    """Los cantrips no tienen límite de usos: se lanzan en cada turno."""
    data = json.loads((FIXTURES / "lich.json").read_text(encoding="utf-8"))
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: data)
    monkeypatch.setattr("dnd_sim.data.api_client.get_spell",
                        lambda index, **kw: _spell_data(index))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        lich = load_monster("lich")
    objetivo = _pj("Objetivo", hp=100000)
    res = run_combat([objetivo, lich], random.Random(3), verbose=True, max_rounds=6)
    lanzamientos = [l for l in res.log if "con Ray of Frost" in l]
    assert lanzamientos, "el lich debe lanzar su cantrip"
    assert len(lanzamientos) >= 2

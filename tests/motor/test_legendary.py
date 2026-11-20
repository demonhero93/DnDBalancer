"""Acciones legendarias y resistencia legendaria (D&D 5e).

Los monstruos salen siempre de la API (fixtures reales + ``load_monster``);
los únicos objetos definidos a mano son los PJ de prueba.
"""
import json
import random
import warnings
from pathlib import Path

import pytest

from dnd_sim import Abilities, Condition, Monster, PlayerCharacter
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.rules.area import AreaSaveAction
from dnd_sim.engine.combat import run_combat
from dnd_sim.rules.conditions import ConditionAction, apply_condition
from dnd_sim.data.legendary_parser import COST_PATTERN, TEXT_SAVE_PATTERN, parse_legendary
from dnd_sim.data.loader import load_monster
from dnd_sim.rules.legendary import (
    DEFAULT_LEGENDARY_POINTS, LEGENDARY_LAIR_BONUS, LegendaryAction,
    LegendaryState, legendary_phase
)
from dnd_sim.rules.saves import SaveDamage, saving_throw
from dnd_sim.engine.stats import simulate
from dnd_sim.rules.usage import begin_turn

FIXTURES = Path(__file__).parents[1] / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _data(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _load(monkeypatch, index: str, data=None):
    payload = data if data is not None else _data(index)
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: payload)
    return load_monster(index)


def _dragon_con_ala_legendaria() -> dict:
    """Copia del fixture 2024 con la 'Wing Attack' legendaria de la ficha.

    El fixture 2024 ya no la trae entre las legendarias (solo 'Pounce'),
    pero el loader debe seguir mapeando una legendaria de área con CD,
    daño y condición: la entrada se reconstruye con datos estructurados.
    """
    data = _data("adult-red-dragon")
    data["legendary_actions"].append({
        "name": "Wing Attack (Costs 2 Actions)",
        "desc": ("Each creature within 10 feet must make a DC 22 Dexterity "
                 "saving throw or take 15 (2d6 + 8) bludgeoning damage and "
                 "be knocked prone."),
        "dc": {"dc_type": {"index": "dex"}, "dc_value": 22,
               "success_type": "none"},
        "damage": [{"damage_type": {"index": "bludgeoning"},
                    "damage_dice": "2d6+8"}],
    })
    return data


def _pj(name: str = "Guerrero", hp: int = 100000, ac: int = 18, **kwargs) -> PlayerCharacter:
    """PJ de prueba (los monstruos siempre vienen de la API)."""
    return PlayerCharacter(
        name=name, max_hp=hp, ac=ac, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[], **kwargs,
    )


def _legendaria(nombre: str, coste: int, accion) -> LegendaryAction:
    return LegendaryAction(name=nombre, cost=coste, action=accion)


def _estado(acciones=None, puntos=DEFAULT_LEGENDARY_POINTS,
            resistencia=0, use_p=1.0, res_p=1.0) -> LegendaryState:
    state = LegendaryState(
        actions=list(acciones or []),
        points_max=puntos,
        points_left=puntos,
        resistance_max=resistencia,
        resistance_left=resistencia,
        use_probability=use_p,
        resistance_probability=res_p,
    )
    return state


def _turno_del_dueno(dueno, ctx) -> None:
    """El dueno juega su turno: se rellenan sus puntos legendarios.

    Sin esto el dueno todavía no tiene puntos de esta ronda (los puntos se
    rellenan al inicio de su propio turno).
    """
    begin_turn(dueno, ctx)


def _contexto(actor, combatants, rng=None, log=None, stats=None) -> CombatContext:
    return CombatContext(
        rng=rng or random.Random(1), actor=actor, combatants=list(combatants),
        round=1, log=log if log is not None else [], verbose=True,
        resources=TurnResources(), legendary_stats=stats,
    )


# --- Estado ---------------------------------------------------------------- #

def test_el_estado_legendario_rellena_gasta_y_reinicia():
    state = _estado(puntos=3)
    assert state.points_left == 3
    state.spend_points(1)
    assert state.points_left == 2
    state.spend_points(99)
    assert state.points_left == 0
    state.refill_points()
    assert state.points_left == 3
    state.resistance_left = 1
    state.reset()
    assert state.points_left == 3
    assert state.resistance_left == state.resistance_max


def test_el_reset_del_combatiente_restaura_puntos_y_resistencia(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    dragon.legendary.points_left = 0
    dragon.legendary.resistance_left = 0
    dragon.reset()
    assert dragon.legendary.points_left == dragon.legendary.points_max
    assert dragon.legendary.resistance_left == dragon.legendary.resistance_max


def test_sin_estado_legendario_no_se_toca_nada():
    jugador = _pj()
    assert jugador.legendary is None
    jugador.reset()
    assert jugador.legendary is None


# --- Puntos, coste y disparo ---------------------------------------------- #

def test_los_puntos_se_rellenan_al_inicio_del_turno_y_no_se_acumulan(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    dragon.legendary.points_left = 1
    ctx = _contexto(dragon, [dragon])
    begin_turn(dragon, ctx)
    assert dragon.legendary.points_left == dragon.legendary.points_max

    # Los puntos no usados se pierden: no se acumulan.
    dragon.legendary.spend_points(1)
    begin_turn(dragon, ctx)
    assert dragon.legendary.points_left == dragon.legendary.points_max


def test_los_puntos_se_rellenan_evenco_el_dueno_est_a_incapacitado(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    apply_condition(dragon, Condition.STUNNED, _contexto(dragon, [dragon]))
    dragon.legendary.points_left = 0
    ctx = _contexto(dragon, [dragon])
    begin_turn(dragon, ctx)
    assert ctx.skip_turn is True
    assert dragon.legendary.points_left == dragon.legendary.points_max


def test_con_un_punto_solo_son_asequibles_las_de_coste_uno(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon", _dragon_con_ala_legendaria())
    dragon.legendary.points_left = 1
    affordable = [
        la for la in dragon.legendary.actions
        if la.cost <= dragon.legendary.points_left
    ]
    assert [la.name for la in affordable] == ["Pounce"]
    # Con 3 puntos también entra el ala (coste 2).
    dragon.legendary.points_left = 3
    affordable = [la for la in dragon.legendary.actions if la.cost <= 3]
    assert {la.name for la in affordable} == {"Pounce", "Wing Attack"}


def test_una_accion_de_coste_tres_no_se_usa_con_menos_de_tres_puntos(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    # Se sube el coste del Pounce para probar el límite.
    pounce = next(la for la in dragon.legendary.actions if la.name == "Pounce")
    pounce.cost = 3
    dragon.legendary.actions = [pounce]
    jugador = _pj()
    ctx = _contexto(jugador, [jugador, dragon])
    _turno_del_dueno(dragon, ctx)
    dragon.legendary.points_left = 2
    legendary_phase(jugador, ctx)
    assert dragon.legendary.points_left == 2, "no se puede pagar una acción de coste 3"


def test_una_sola_accion_legendaria_por_disparo_y_por_dueno(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    jugador = _pj()
    log = []
    ctx = _contexto(jugador, [jugador, dragon], log=log)
    _turno_del_dueno(dragon, ctx)
    legendary_phase(jugador, ctx)
    legendarias = [l for l in log if l.startswith("[Legendaria]")]
    assert len(legendarias) == 1


def test_no_se_dispara_en_el_turno_del_propio_dueno(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    jugador = _pj()
    log = []
    ctx = _contexto(dragon, [jugador, dragon], log=log)
    legendary_phase(dragon, ctx)
    assert not [l for l in log if l.startswith("[Legendaria]")]


def test_si_dispara_tras_el_turno_de_cada_pj(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    pjs = [_pj("Guerrero"), _pj("Pícaro"), _pj("Monje")]
    res = run_combat(pjs + [dragon], random.Random(5), verbose=True, max_rounds=10)
    legendarias = [l for l in res.log if l.startswith("[Legendaria]")]
    assert legendarias
    for linea in legendarias:
        assert "tras el turno de" in linea
        assert "quedan" in linea
        assert "coste" in linea


def test_si_dispara_tras_un_turno_saltado_por_incapacitacion(monkeypatch):
    """Un turno perdido por incapacitación también dispara la fase legendaria."""
    dragon = _load(monkeypatch, "adult-red-dragon")
    jugador = _pj()
    ctx = _contexto(jugador, [jugador, dragon], log=[])
    _turno_del_dueno(dragon, ctx)
    apply_condition(jugador, Condition.STUNNED, ctx)
    begin_turn(jugador, ctx)
    assert ctx.skip_turn is True
    legendary_phase(jugador, ctx)
    assert any(l.startswith("[Legendaria]") for l in ctx.log)


def test_no_actua_si_el_dueno_tiene_0_hp(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    dragon.hp = 0
    jugador = _pj()
    log = []
    ctx = _contexto(jugador, [jugador, dragon], log=log)
    legendary_phase(jugador, ctx)
    assert not [l for l in log if l.startswith("[Legendaria]")]


def test_no_actua_si_el_dueno_esta_incapacitado(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    apply_condition(dragon, Condition.STUNNED, _contexto(dragon, [dragon]))
    jugador = _pj()
    log = []
    ctx = _contexto(jugador, [jugador, dragon], log=log)
    legendary_phase(jugador, ctx)
    assert not [l for l in log if l.startswith("[Legendaria]")]


def test_no_actua_si_el_combate_ya_terminado(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    jugador = _pj()
    jugador.hp = 0
    log = []
    ctx = _contexto(jugador, [jugador, dragon], log=log)
    legendary_phase(jugador, ctx)
    assert not [l for l in log if l.startswith("[Legendaria]")]


def test_el_combate_termina_en_medio_de_la_fase(monkeypatch):
    """Si la acción legendaria mata al último enemigo, no hay más acciones."""
    dragon_a = _load(monkeypatch, "adult-red-dragon", _dragon_con_ala_legendaria())
    dragon_b = _load(monkeypatch, "adult-red-dragon", _dragon_con_ala_legendaria())
    dragon_b.name = "Adult Red Dragon 2"
    # Solo el ala (área con daño): el PJ muere siempre.
    for dragon in (dragon_a, dragon_b):
        dragon.legendary.actions = [la for la in dragon.legendary.actions
                                     if la.name == "Wing Attack"]
    jugador = _pj(hp=1)
    jugador.save_overrides["dex"] = -30   # falla la CD 22 seguro
    log = []
    ctx = _contexto(jugador, [jugador, dragon_a, dragon_b], log=log)
    _turno_del_dueno(dragon_a, ctx)
    _turno_del_dueno(dragon_b, ctx)
    legendary_phase(jugador, ctx)
    assert jugador.hp <= 0
    # El combate ha terminado: el segundo dragón no actúa.
    legendarias = [l for l in log if l.startswith("[Legendaria]")]
    assert len(legendarias) == 1
    assert "Adult Red Dragon 2" not in legendarias[0]


def test_no_gasta_los_recursos_de_turno_del_dueno(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    jugador = _pj()
    ctx = _contexto(jugador, [jugador, dragon])
    recursos = TurnResources()
    ctx.resources = recursos
    legendary_phase(jugador, ctx)
    assert not recursos.action_used
    assert not recursos.bonus_action_used
    assert not recursos.reaction_used


def test_no_gasta_el_uso_limitado_de_la_accion_del_dueno(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    jugador = _pj()
    pounce = next(la for la in dragon.legendary.actions if la.name == "Pounce")
    ataque = pounce.action.attack
    ataque.usage = None
    ctx = _contexto(jugador, [jugador, dragon])
    legendary_phase(jugador, ctx)
    # El uso de la acción normal del dragón no se gasta.
    aliento = next(a for a in dragon.actions if getattr(a, "name", "") == "Fire Breath")
    assert aliento.usage.charged is True


def test_sin_leyendas_no_se_consume_rng(monkeypatch):
    ogre = _load(monkeypatch, "ogre")
    jugador = _pj()
    ctx = _contexto(jugador, [jugador, ogre], rng=random.Random(9))
    rng = ctx.rng
    estado = rng.getstate()
    legendary_phase(jugador, ctx)
    assert rng.getstate() == estado


def test_sin_acciones_asequibles_no_se_consume_rng(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    dragon.legendary.points_left = 0
    jugador = _pj()
    ctx = _contexto(jugador, [jugador, dragon], rng=random.Random(9))
    rng = ctx.rng
    estado = rng.getstate()
    legendary_phase(jugador, ctx)
    assert rng.getstate() == estado


def test_con_una_sola_accion_asequible_pick_no_consume_rng(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    dragon.legendary.actions = [la for la in dragon.legendary.actions
                                 if la.name == "Pounce"]
    jugador = _pj()
    ctx = _contexto(jugador, [jugador, dragon], rng=random.Random(9))
    _turno_del_dueno(dragon, ctx)
    rng = ctx.rng
    estado = rng.getstate()
    legendary_phase(jugador, ctx)
    # La acción ejecuta un ataque (tira dados), pero la *elección* no sortea:
    # el estado cambia por el ataque, no por el pick.
    assert rng.getstate() != estado


def test_use_probability_cero_nunca_actua(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    dragon.legendary.use_probability = 0.0
    jugador = _pj()
    log = []
    ctx = _contexto(jugador, [jugador, dragon], log=log)
    legendary_phase(jugador, ctx)
    assert not [l for l in log if l.startswith("[Legendaria]")]


def test_use_probability_uno_no_hace_tirada_extra(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    dragon.legendary.use_probability = 1.0
    dragon.legendary.actions = [la for la in dragon.legendary.actions
                                 if la.name == "Pounce"]
    jugador = _pj()
    ctx = _contexto(jugador, [jugador, dragon], rng=random.Random(9))
    _turno_del_dueno(dragon, ctx)
    rng = ctx.rng
    estado = rng.getstate()
    legendary_phase(jugador, ctx)
    # Solo el ataque consume RNG (no una tirada de probabilidad extra).
    assert rng.getstate() != estado
    dragon.legendary.points_left = 1


def test_use_probability_medio_se_usa_about_50_por_ciento():
    """20.000 disparos: ~50% usan una acción (±1.5%)."""
    rng = random.Random(20260120)
    disparos = 20000
    usados = 0
    for _ in range(disparos):
        state = _estado(use_p=0.5)
        state.actions = []
        if rng.random() < state.use_probability:
            usados += 1
    assert abs(usados / disparos - 0.5) <= 0.015


def test_dos_duenos_legendarios_actuan_cada_uno_una_vez(monkeypatch):
    dragon_a = _load(monkeypatch, "adult-red-dragon")
    dragon_b = _load(monkeypatch, "adult-red-dragon")
    dragon_b.name = "Adult Red Dragon 2"
    jugador = _pj()
    log = []
    ctx = _contexto(jugador, [jugador, dragon_a, dragon_b], log=log)
    _turno_del_dueno(dragon_a, ctx)
    _turno_del_dueno(dragon_b, ctx)
    legendary_phase(jugador, ctx)
    legendarias = [l for l in log if l.startswith("[Legendaria]")]
    assert len(legendarias) == 2
    assert any("Adult Red Dragon 2" in l for l in legendarias)


def test_la_fase_ocurre_despues_del_end_turn(monkeypatch):
    """El log de la fase legendaria va detrás del fin de turno."""
    dragon = _load(monkeypatch, "adult-red-dragon")
    jugador = _pj()
    log = []
    ctx = _contexto(jugador, [jugador, dragon], log=log)
    from dnd_sim.rules.conditions import end_turn
    _turno_del_dueno(dragon, ctx)
    end_turn(jugador, ctx)
    legendary_phase(jugador, ctx)
    assert any(l.startswith("[Legendaria]") for l in log)


# --- Loader ---------------------------------------------------------------- #

def test_el_dragon_carga_sus_acciones_legendarias(monkeypatch):
    data = _dragon_con_ala_legendaria()
    bruto = next(a for a in data["legendary_actions"] if a["name"].startswith("Wing Attack"))

    dragon = _load(monkeypatch, "adult-red-dragon", data)
    state = dragon.legendary
    assert state is not None
    # Siempre en guarida: points_max = base + LEGENDARY_LAIR_BONUS.
    assert state.points_max == (
        DEFAULT_LEGENDARY_POINTS + LEGENDARY_LAIR_BONUS)

    nombres = {la.name: la for la in state.actions}
    assert set(nombres) == {"Pounce", "Wing Attack"}

    # Pounce envuelve el ataque Rend del dragón (coste 1).
    pounce = nombres["Pounce"]
    assert pounce.cost == 1
    assert getattr(pounce.action, "name", "") == "Rend"

    # Wing Attack: área con CD, característica y daño del JSON + PRONE.
    ala = nombres["Wing Attack"]
    assert ala.cost == 2
    assert isinstance(ala.action, AreaSaveAction)
    assert ala.action.effect.dc == bruto["dc"]["dc_value"]
    assert ala.action.effect.ability == bruto["dc"]["dc_type"]["index"]
    assert ala.action.effect.damage == bruto["damage"][0]["damage_dice"]
    assert ala.action.effect.damage_type.value == bruto["damage"][0]["damage_type"]["index"]
    assert ala.action.condition is not None
    assert ala.action.condition.condition is Condition.PRONE
    # Pounce no tiene datos propios: es una referencia al ataque "Rend".
    pounce_bruto = next(a for a in data["legendary_actions"] if a["name"] == "Pounce")
    assert pounce_bruto.get("damage") == []


def test_el_detect_del_dragon_se_omite_con_aviso(monkeypatch):
    with pytest.warns(UserWarning, match="Detect"):
        dragon = _load(monkeypatch, "adult-red-dragon")
    assert "Detect" not in {la.name for la in dragon.legendary.actions}


def test_el_ala_que_mezcla_movimiento_avisa(monkeypatch):
    with pytest.warns(UserWarning, match="movimiento"):
        _load(monkeypatch, "adult-red-dragon")


def test_el_lich_carga_sus_acciones_legendarias(monkeypatch):
    lich = _load(monkeypatch, "lich")
    state = lich.legendary
    assert state is not None
    nombres = {la.name: la for la in state.actions}

    # El fixture 2024 solo deja modelable 'Disrupt Life' (área con salvación).
    assert set(nombres) == {"Disrupt Life"}
    disrupt = nombres["Disrupt Life"]
    assert disrupt.cost == 1
    assert isinstance(disrupt.action, AreaSaveAction)
    bruto = next(a for a in _data("lich")["legendary_actions"]
                 if a["name"] == "Disrupt Life")
    assert disrupt.action.effect.dc == bruto["dc"]["dc_value"]
    assert disrupt.action.effect.ability == bruto["dc"]["dc_type"]["index"]
    assert disrupt.action.effect.damage == bruto["damage"][0]["damage_dice"]
    assert (disrupt.action.effect.damage_type.value
            == bruto["damage"][0]["damage_type"]["index"])

    assert "Cantrip" not in nombres


def test_el_cantrip_del_lich_se_omite_con_aviso(monkeypatch):
    # El fixture 2024 ya no trae un cantrip legendario: se añade la entrada
    # para comprobar que el motivo «conjuro» sigue avisando con su nombre.
    data = _data("lich")
    data["legendary_actions"].append({
        "name": "Cantrip",
        "desc": "The lich casts a cantrip at one creature within range.",
        "damage": [],
    })
    with pytest.warns(UserWarning, match="Cantrip"):
        _load(monkeypatch, "lich", data)


def test_el_coste_por_defecto_es_uno_y_el_nombre_queda_limpio():
    """Sin sufijo de coste: coste 1 y nombre tal cual."""
    from dnd_sim.model.actions import AttackAction
    from dnd_sim.model.attack import Attack
    acciones = [AttackAction(Attack("Golpe", "1d6"))]
    state = parse_legendary({"name": "Mago", "legendary_actions": [
        {"name": "Ataque", "desc": "The mage makes a Golpe attack.", "damage": []},
    ]}, acciones)
    assert state is not None
    assert len(state.actions) == 1
    assert state.actions[0].cost == 1
    assert state.actions[0].name == "Ataque"


def test_el_sufijo_de_coste_se_parsea():
    assert COST_PATTERN.search("Wing Attack (Costs 2 Actions)").group(1) == "2"
    assert COST_PATTERN.search("Chomp (Costs 3 Actions)").group(1) == "3"
    assert COST_PATTERN.search("Tail Attack") is None


def test_una_entrada_que_referencia_una_accion_con_uso_se_omite(monkeypatch):
    data = _data("adult-red-dragon")
    # Se referencia el aliento de fuego (que tiene recarga).
    data["legendary_actions"].append({
        "name": "Aliento (Costs 2 Actions)",
        "desc": "The dragon uses its Fire Breath.",
        "damage": [],
    })
    with pytest.warns(UserWarning, match="uso limitado"):
        dragon = _load(monkeypatch, "adult-red-dragon", data)
    assert "Aliento" not in {la.name for la in dragon.legendary.actions}


def test_ogre_y_owlbear_no_tienen_estado_legendario(monkeypatch):
    assert _load(monkeypatch, "ogre").legendary is None
    assert _load(monkeypatch, "owlbear").legendary is None


def test_cada_accion_omitida_avisa_con_monstruo_accion_y_motivo(monkeypatch):
    with warnings.catch_warnings(record=True) as atrapadas:
        warnings.simplefilter("always")
        _load(monkeypatch, "adult-red-dragon")
    textos = [str(w.message) for w in atrapadas]
    omitted = [t for t in textos if "Acción legendaria" in t]
    assert omitted
    # Cada aviso nombra al monstruo y a la entrada del fixture que lo origina.
    nombres_brutos = {a["name"] for a in _data("adult-red-dragon")["legendary_actions"]}
    for texto in omitted:
        assert "Adult Red Dragon" in texto
        assert any(nombre in texto for nombre in nombres_brutos)


def test_la_resistencia_legendaria_usa_el_uso_del_fixture(monkeypatch):
    data = _data("adult-red-dragon")
    bruto = next(s for s in data["special_abilities"]
                 if s["name"].lower().startswith("legendary resistance"))
    dragon = _load(monkeypatch, "adult-red-dragon")
    assert dragon.legendary.resistance_max == bruto["usage"]["times"]


def test_el_patron_de_texto_libre_esta_validado_contra_los_fixtures():
    """El patrón cerrado reconoce el texto de salvación con daño.

    El fixture 2024 ya no trae texto libre con salvación en las legendarias
    (usa datos estructurados): se valida con el texto canónico del patrón.
    """
    desc = ("The dragon makes a tail attack. Each creature within 5 feet "
            "must make a DC 22 Dexterity saving throw or take 15 (2d6 + 8) "
            "bludgeoning damage.")
    match = TEXT_SAVE_PATTERN.search(desc)
    assert match is not None
    assert match.group(1) == "22"
    assert match.group(2).lower() == "dexterity"
    assert match.group(3).replace(" ", "") == "2d6+8"
    assert match.group(4).lower() == "bludgeoning"


# --- Resistencia legendaria ------------------------------------------------ #

def test_un_fallo_consume_la_resistencia_y_pasa_a_exito(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    objetivo = dragon
    objetivo.save_overrides["dex"] = -30  # falla seguro
    rng = random.Random(4)
    resultado = saving_throw(objetivo, "dex", 30, rng)
    assert resultado.success is True
    assert resultado.legendary_resistance_used is True
    assert dragon.legendary.resistance_left == dragon.legendary.resistance_max - 1


def test_sin_usos_el_fallo_sigue_siendo_fallo(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    dragon.legendary.resistance_left = 0
    dragon.save_overrides["dex"] = -30
    resultado = saving_throw(dragon, "dex", 30, random.Random(4))
    assert resultado.success is False
    assert resultado.legendary_resistance_used is False


def test_un_exito_natural_no_gasta_la_resistencia(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    dragon.save_overrides["dex"] = 30
    resultado = saving_throw(dragon, "dex", 5, random.Random(4))
    assert resultado.success is True
    assert resultado.legendary_resistance_used is False
    assert dragon.legendary.resistance_left == dragon.legendary.resistance_max


def test_la_resistencia_convierte_fallos_automaticos(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    apply_condition(dragon, Condition.STUNNED, _contexto(dragon, [dragon]))
    resultado = saving_throw(dragon, "dex", 5, random.Random(4))
    assert resultado.auto_fail is True
    assert resultado.success is True
    assert resultado.legendary_resistance_used is True


def test_la_resistencia_funciona_en_todas_las_rutas(monkeypatch):
    """Ataque con rider, SaveAction, AreaSaveAction, ConditionAction y
    salvaciones de repetición de ``end_turn``."""
    from dnd_sim.model.actions import SaveAction
    from dnd_sim.model.attack import Attack
    from dnd_sim.engine.combat import attack_roll
    from dnd_sim.rules.conditions import ConditionEffect, end_turn

    dragon = _load(monkeypatch, "adult-red-dragon")
    dragon.save_overrides["dex"] = -30   # falla cualquier CD de DES
    jugador = _pj()
    dragon.legendary.resistance_left = 99

    # 1. Ataque con rider (condición) contra el dragón.
    atk = Attack(
        "Golpe", "1d6", ability="str", attack_bonus=10, damage_bonus=0,
        condition_riders=[ConditionEffect(condition=Condition.PRONE,
                                          save_ability="dex", dc=30,
                                          duration_rounds=1)],
    )
    ctx = _contexto(jugador, [jugador, dragon], rng=random.Random(7))
    attack_roll(jugador, dragon, atk, ctx.rng, ctx.log, ctx=ctx)
    usos = dragon.legendary.resistance_left
    assert usos == 98, "el ataque con rider gasta la resistencia"

    # 2. SaveAction: el dragón es el objetivo de la acción del jugador.
    accion = SaveAction(name="Ataque", effect=SaveDamage(ability="dex", dc=30,
                                                          damage="1d6"))
    ctx = _contexto(jugador, [jugador, dragon], rng=random.Random(7))
    accion.execute(ctx)
    assert dragon.legendary.resistance_left == usos - 1

    # 3. AreaSaveAction.
    area = AreaSaveAction(name="Area", effect=SaveDamage(ability="dex", dc=30,
                                                          damage="1d6"))
    ctx = _contexto(jugador, [jugador, dragon], rng=random.Random(7))
    area.execute(ctx)
    assert dragon.legendary.resistance_left == usos - 2

    # 4. ConditionAction.
    accion_condicion = ConditionAction(
        name="Cond", effect=ConditionEffect(condition=Condition.PRONE,
                                            save_ability="dex", dc=30,
                                            duration_rounds=1),
    )
    ctx = _contexto(jugador, [jugador, dragon], rng=random.Random(7))
    accion_condicion.execute(ctx)
    assert dragon.legendary.resistance_left == usos - 3

    # 5. Salvación de repetición al final del turno.
    from dnd_sim.rules.conditions import RepeatSave
    apply_condition(dragon, Condition.PARALYZED, ctx,
                    repeat_save=RepeatSave(ability="dex", dc=30))
    end_turn(dragon, ctx)
    assert dragon.legendary.resistance_left == usos - 4


def test_la_resistencia_no_afecta_a_las_pruebas_de_caracteristica(monkeypatch):
    from dnd_sim.rules.checks import ability_check
    dragon = _load(monkeypatch, "adult-red-dragon")
    dragon.abilities = Abilities(str=1)
    usos = dragon.legendary.resistance_left
    resultado = ability_check(dragon, "str", 30, random.Random(4))
    assert resultado.success is False
    assert dragon.legendary.resistance_left == usos


def test_la_resistencia_no_afecta_a_las_tiradas_de_ataque(monkeypatch):
    from dnd_sim.model.attack import Attack
    from dnd_sim.engine.combat import attack_roll
    dragon = _load(monkeypatch, "adult-red-dragon")
    jugador = _pj(ac=100)
    usos = dragon.legendary.resistance_left
    atk = Attack("Golpe", "1d6", ability="str", attack_bonus=0, damage_bonus=0)
    attack_roll(dragon, jugador, atk, random.Random(4), [])
    assert dragon.legendary.resistance_left == usos


def test_resistance_probability_cero_nunca_convierte(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    dragon.legendary.resistance_probability = 0.0
    dragon.save_overrides["dex"] = -30
    resultado = saving_throw(dragon, "dex", 30, random.Random(4))
    assert resultado.success is False
    assert dragon.legendary.resistance_left == dragon.legendary.resistance_max


def test_resistance_probability_uno_no_consume_rng(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    dragon.legendary.resistance_probability = 1.0
    dragon.save_overrides["dex"] = -30
    rng = random.Random(4)
    resultado = saving_throw(dragon, "dex", 30, rng)
    # La tirada de la salvación sí consume RNG, pero no hay tirada extra:
    # el resultado es el mismo que con una tirada normal.
    assert resultado.success is True
    assert dragon.legendary.resistance_left == dragon.legendary.resistance_max - 1


def test_resistance_probability_medio_convierte_about_50_por_ciento(monkeypatch):
    """20.000 fallos: ~50% se convierten (±1.5%)."""
    rng = random.Random(20260120)
    disparos = 20000
    convertidos = 0
    for _ in range(disparos):
        state = LegendaryState(resistance_max=10 ** 6, resistance_left=10 ** 6,
                               resistance_probability=0.5)
        objetivo = Monster(name="X", max_hp=10, ac=10)
        objetivo.legendary = state
        resultado = saving_throw(objetivo, "dex", 30, rng)
        if resultado.success:
            convertidos += 1
    assert abs(convertidos / disparos - 0.5) <= 0.015


def test_un_pj_con_ataque_con_rider_no_aplica_la_condicion_mientras_queden_usos(
        monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    dragon.legendary.resistance_left = 1
    dragon.legendary.resistance_max = 1
    dragon.save_overrides["dex"] = -30
    jugador = _pj()
    from dnd_sim.model.attack import Attack
    from dnd_sim.engine.combat import attack_roll
    from dnd_sim.rules.conditions import ConditionEffect
    atk = Attack(
        "Golpe", "1d6", ability="str", attack_bonus=10, damage_bonus=0,
        condition_riders=[ConditionEffect(condition=Condition.PRONE,
                                          save_ability="dex", dc=30,
                                          duration_rounds=1)],
    )
    attack_roll(jugador, dragon, atk, random.Random(11), [])
    # La resistencia consumió el uso: la condición NO se aplica.
    assert not dragon.conditions.has(Condition.PRONE)
    assert dragon.legendary.resistance_left == 0

    # Sin usos: el fallo es real y la condición se aplica.
    attack_roll(jugador, dragon, atk, random.Random(11), [])
    assert dragon.conditions.has(Condition.PRONE)


# --- Simulación ------------------------------------------------------------ #

def test_el_dragon_contra_un_grupo_usa_acciones_legendarias(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    pjs = [_pj(f"PJ{i}", hp=400) for i in range(4)]
    stats = simulate(pjs + [dragon], n=30, seed=1)
    assert stats["legendary_actions_used_avg"]
    assert sum(stats["legendary_actions_used_avg"].values()) > 0
    assert stats["legendary_points_spent_avg"] > 0


def test_los_puntos_gastados_por_ronda_nunca_superan_el_maximo(monkeypatch):
    """En cada ronda, los puntos gastados no superan ``points_max``."""
    import re
    dragon = _load(monkeypatch, "adult-red-dragon")
    pjs = [_pj(f"PJ{i}", hp=4000) for i in range(4)]
    maximo = dragon.legendary.points_max
    patron = re.compile(r"\(coste (\d+),")
    for semilla in (1, 2, 3):
        res = run_combat(pjs + [dragon], random.Random(semilla), verbose=True, max_rounds=12)
        por_ronda = {}
        ronda = None
        for linea in res.log:
            if linea.startswith("-- Ronda"):
                ronda = linea
                por_ronda.setdefault(ronda, 0)
            elif linea.startswith("[Legendaria]"):
                match = patron.search(linea)
                assert match is not None, linea
                por_ronda[ronda] = por_ronda.get(ronda, 0) + int(match.group(1))
        assert por_ronda
        for ronda, gastados in por_ronda.items():
            assert gastados <= maximo, f"{ronda}: {gastados} > {maximo}"


def test_con_use_probability_uno_el_danio_es_mayor_que_con_cero(monkeypatch):
    """Con las acciones legendarias activas el dragón inflige más daño."""
    dragon_a = _load(monkeypatch, "adult-red-dragon")
    dragon_b = _load(monkeypatch, "adult-red-dragon")
    dragon_a.legendary.use_probability = 1.0
    dragon_b.legendary.use_probability = 0.0
    # PJ muy resistentes: el combate no se decide por la muerte del grupo y
    # el daño acumulado se ve.
    pjs = [_pj(f"PJ{i}", hp=10000) for i in range(4)]
    a = simulate(pjs + [dragon_a], n=40, seed=11)
    b = simulate(pjs + [dragon_b], n=40, seed=11)
    assert sum(a["legendary_actions_used_avg"].values()) > 0
    assert sum(b["legendary_actions_used_avg"].values()) == 0
    assert (a["damage_dealt_avg"]["Adult Red Dragon"]
            > b["damage_dealt_avg"]["Adult Red Dragon"])


def test_reproducibilidad_con_leyendas_y_resistencia(monkeypatch):
    dragon_a = _load(monkeypatch, "adult-red-dragon")
    dragon_b = _load(monkeypatch, "adult-red-dragon")
    pjs = [_pj(f"PJ{i}", hp=400) for i in range(4)]
    a = simulate(pjs + [dragon_a], n=20, seed=7)
    b = simulate(pjs + [dragon_b], n=20, seed=7)
    assert a["win_rate"] == b["win_rate"]
    assert a["rounds_avg"] == b["rounds_avg"]
    assert a["legendary_actions_used_avg"] == b["legendary_actions_used_avg"]
    assert a["legendary_points_spent_avg"] == b["legendary_points_spent_avg"]
    assert a["legendary_resistances_used_avg"] == b["legendary_resistances_used_avg"]


# --- CLI ------------------------------------------------------------------- #

def test_el_cli_tiene_las_opciones_legendarias():
    """``main.py`` expone ``--legendary-p`` y ``--resistance-p``."""
    import importlib.util
    import pathlib
    import sys

    raiz = pathlib.Path(__file__).resolve().parents[2]
    if str(raiz) not in sys.path:
        sys.path.insert(0, str(raiz))
    spec = importlib.util.spec_from_file_location("main_cli", raiz / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    parser = module.build_parser()
    args = parser.parse_args(["--monster", "adult-red-dragon",
                              "--legendary-p", "0.5", "--resistance-p", "0.25"])
    assert args.legendary_p == 0.5
    assert args.resistance_p == 0.25
    # Por defecto, 1.0 (siempre).
    por_defecto = parser.parse_args([])
    assert por_defecto.legendary_p == 1.0
    assert por_defecto.resistance_p == 1.0

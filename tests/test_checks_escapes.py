"""Pruebas de característica, escape de estados y distancia/cobertura."""
import json
import random
from collections import Counter
from pathlib import Path

import pytest

from dnd_sim import (
    Abilities, Attack, Condition, ConditionEffect, EscapeCheck, Monster,
    PlayerCharacter, RollMode, apply_condition, ability_check, attack_modifiers,
    effective_ac, load_monster, resolve_attack_range,
)
from dnd_sim.model.actions import ActionType, CombatContext, TurnResources
from dnd_sim.rules.checks import ability_check_bonus
from dnd_sim.engine.combat import attack_roll, run_combat
from dnd_sim.rules.conditions import ConditionInstance, attempt_escapes
from dnd_sim.data.escape_parser import parse_escape
from dnd_sim.rules.roll_modifiers import AttackRange, check_modifiers
from dnd_sim.engine.stats import simulate
from dnd_sim.rules.usage import begin_turn

FIXTURES = Path(__file__).parent / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _data(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _load(monkeypatch, index: str, data=None):
    payload = data if data is not None else _data(index)
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: payload)
    return load_monster(index)


def _pj(name: str = "Guerrero", hp: int = 500, ac: int = 11, **kwargs) -> PlayerCharacter:
    return PlayerCharacter(
        name=name, max_hp=hp, ac=ac, proficiency=2,
        abilities=Abilities(str=10, dex=10, con=10, int=10, wis=10, cha=10),
        attacks=[], **kwargs,
    )


def _ctx(actor=None, combatants=(), rng=None, log=None, resources=None) -> CombatContext:
    return CombatContext(rng=rng or random.Random(1), actor=actor,
                         combatants=list(combatants), round=1,
                         log=log if log is not None else [],
                         verbose=True,
                         resources=resources if resources is not None else TurnResources())


def _duelo(ac: int = 11):
    """Atacante NPC con +0 a impacto y objetivo PJ con CA 11 -> 50% normal."""
    atacante = Monster(name="Atacante", max_hp=500, ac=10, abilities=Abilities())
    objetivo = _pj("Objetivo", hp=500, ac=ac)
    return atacante, objetivo


def _ataque(rango: AttackRange = AttackRange.MELEE, damage: str = "1d6") -> Attack:
    return Attack("Golpe", damage, ability="str", attack_bonus=0, damage_bonus=0,
                  range_type=rango)


def _tasa_de_impacto(attacker, target, atk, n: int = 20000, seed: int = 99) -> float:
    rng = random.Random(seed)
    log: list[str] = []
    golpes = 0
    for _ in range(n):
        target.hp = target.max_hp
        log.clear()
        attack_roll(attacker, target, atk, rng, log)
        if log and "falla" not in log[0]:
            golpes += 1
    return golpes / n


# --- Pruebas de característica ---------------------------------------------- #

def test_prueba_de_caracteristica_con_bonus_0_da_50_por_ciento():
    objetivo = _pj()
    rng = random.Random(3)
    exitos = sum(1 for _ in range(20000)
                 if ability_check(objetivo, "str", 11, rng).success)
    assert abs(exitos / 20000 - 0.5) <= 0.015, exitos / 20000


@pytest.mark.parametrize("condition", [Condition.POISONED, Condition.FRIGHTENED])
def test_prueba_con_envenenado_o_aterrorizado_da_desventaja(condition):
    objetivo = _pj()
    apply_condition(objetivo, condition, _ctx())
    rng = random.Random(3)
    exitos = sum(1 for _ in range(20000)
                 if ability_check(objetivo, "str", 11, rng).success)
    assert abs(exitos / 20000 - 0.25) <= 0.015, exitos / 20000


def test_prueba_con_ventaja_da_75_por_ciento():
    objetivo = _pj()
    objetivo.checks_with_advantage = {"str"}
    rng = random.Random(3)
    exitos = sum(1 for _ in range(20000)
                 if ability_check(objetivo, "str", 11, rng).success)
    assert abs(exitos / 20000 - 0.75) <= 0.015, exitos / 20000


def test_ventaja_y_desventaja_se_anulan():
    objetivo = _pj()
    objetivo.checks_with_advantage = {"str"}
    objetivo.checks_with_disadvantage = {"str"}
    rng = random.Random(3)
    exitos = sum(1 for _ in range(20000)
                 if ability_check(objetivo, "str", 11, rng).success)
    assert abs(exitos / 20000 - 0.5) <= 0.015, exitos / 20000


def test_dos_ventajas_y_una_desventaja_se_anulan():
    objetivo = _pj()
    objetivo.checks_with_advantage = {"str"}
    apply_condition(objetivo, Condition.POISONED, _ctx())
    objetivo.checks_with_advantage = {"str", "dex"}
    rng = random.Random(3)
    exitos = sum(1 for _ in range(20000)
                 if ability_check(objetivo, "str", 11, rng).success)
    assert abs(exitos / 20000 - 0.5) <= 0.015, exitos / 20000


def test_sin_autoexito_ni_autofallo_en_pruebas():
    """Regla 5e: el 20 natural no es éxito automático ni el 1 fallo."""
    objetivo = _pj()
    objetivo.abilities = Abilities(str=10, dex=10, con=10, int=10, wis=10, cha=10)
    objetivo.save_overrides.clear()
    # Con bonus -30 y CD 15, un 20 natural (20-30 = -10) falla.
    objetivo.abilities = Abilities(str=10, dex=10, con=10, int=10, wis=10, cha=10)
    checks = []
    original = ability_check_bonus

    def _bonus(target, ability):
        return -30

    import dnd_sim.rules.checks as checks_mod
    monkey = checks_mod.ability_check_bonus
    checks_mod.ability_check_bonus = _bonus
    try:
        rng = random.Random(11)
        for _ in range(20000):
            resultado = ability_check(objetivo, "str", 15, rng)
            checks.append(resultado)
            if resultado.total == 20 - 30:
                assert not resultado.success, "el 20 natural no es éxito automático"
    finally:
        checks_mod.ability_check_bonus = monkey

    checks_mod.ability_check_bonus = _bonus
    try:
        rng = random.Random(11)
        for _ in range(20000):
            resultado = ability_check(objetivo, "str", 15, rng)
            if resultado.total == 1 + 30:
                assert resultado.success, "el 1 natural no es fallo automático"
    finally:
        checks_mod.ability_check_bonus = monkey


def test_los_flags_de_prueba_son_por_caracteristica():
    objetivo = _pj()
    objetivo.checks_with_advantage = {"dex"}
    assert check_modifiers(objetivo, "dex").mode is RollMode.ADVANTAGE
    assert check_modifiers(objetivo, "str").mode is RollMode.NORMAL


# --- Escape de estados ------------------------------------------------------ #

def test_el_fixture_de_la_telaraña_carga_restrained_con_escape(monkeypatch):
    """Valores leídos del JSON del fixture."""
    data = _data("giant-spider") if (FIXTURES / "giant-spider.json").exists() else None
    if data is None:
        pytest.skip("sin fixture de giant-spider")
    bruto = next(a for a in data["actions"] if a["name"] == "Web")
    assert "DC 12 Strength check" in bruto["desc"]
    assert "As an action" in bruto["desc"]
    escape = parse_escape(bruto["desc"], "Giant Spider", "Web")
    assert escape.abilities == ("str",)
    assert escape.dc == 12
    assert escape.consumes_action is True


def test_la_telaraña_aplica_inmovilizado_sin_salvacion(monkeypatch):
    araña = _load(monkeypatch, "giant-spider")
    telaraña = next(a for a in araña.attacks if a.name == "Web")
    rider = telaraña.condition_riders[0]
    assert rider.condition is Condition.RESTRAINED
    assert rider.save_ability is None
    assert rider.escape is not None
    assert rider.escape.dc == 12
    assert rider.escape.abilities == ("str",)
    assert rider.escape.consumes_action is True
    assert telaraña.range_type is AttackRange.RANGED


def test_la_telaraña_no_aplica_la_condicion_si_falla_el_ataque(monkeypatch):
    araña = _load(monkeypatch, "giant-spider")
    telaraña = next(a for a in araña.attacks if a.name == "Web")
    objetivo = _pj("Objetivo", hp=500, ac=100)  # solo el 20 natural impacta
    objetivo.abilities = Abilities(str=10, dex=10, con=10, int=10, wis=10, cha=10)
    rng = random.Random(4)
    log: list[str] = []
    for _ in range(50):
        objetivo.hp = objetivo.max_hp
        objetivo.conditions.clear()
        log.clear()
        attack_roll(araña, objetivo, telaraña, rng, log)
        if "falla" in log[0]:
            assert not objetivo.conditions.has(Condition.RESTRAINED)


def test_el_escape_se_intenta_al_inicio_del_turno(monkeypatch):
    araña = _load(monkeypatch, "giant-spider")
    objetivo = _pj("Objetivo", hp=500)
    escape = EscapeCheck(abilities=("str",), dc=12, consumes_action=False)
    apply_condition(objetivo, Condition.RESTRAINED, _ctx(), escape=escape)

    ctx = _ctx(actor=objetivo, combatants=[objetivo], rng=random.Random(2))
    # Fuera del turno no hay intentos.
    assert ctx.log == []
    # Al inicio del turno, se intenta (y se registra).
    begin_turn(objetivo, ctx)
    assert any("prueba STR" in line for line in ctx.log), ctx.log


def test_escape_con_exito_elimina_la_condicion(monkeypatch):
    import dnd_sim.rules.checks as checks_mod

    objetivo = _pj("Objetivo")
    escape = EscapeCheck(abilities=("str",), dc=12, consumes_action=False)
    apply_condition(objetivo, Condition.RESTRAINED, _ctx(), escape=escape)

    original = checks_mod.ability_check
    checks_mod.ability_check = lambda *a, **k: original(*a, **k)
    checks_mod.ability_check = _check_fijo(True)
    try:
        ctx = _ctx(actor=objetivo, combatants=[objetivo], rng=random.Random(2))
        begin_turn(objetivo, ctx)
    finally:
        checks_mod.ability_check = original
    assert not objetivo.conditions.has(Condition.RESTRAINED)


def test_escape_con_fallo_la_condicion_sigue(monkeypatch):
    import dnd_sim.rules.checks as checks_mod

    objetivo = _pj("Objetivo")
    escape = EscapeCheck(abilities=("str",), dc=12, consumes_action=False)
    apply_condition(objetivo, Condition.RESTRAINED, _ctx(), escape=escape)

    original = checks_mod.ability_check
    checks_mod.ability_check = _check_fijo(False)
    try:
        ctx = _ctx(actor=objetivo, combatants=[objetivo], rng=random.Random(2))
        begin_turn(objetivo, ctx)
    finally:
        checks_mod.ability_check = original
    assert objetivo.conditions.has(Condition.RESTRAINED)


def _check_fijo(exito: bool):
    """Devuelve una función ability_check con el resultado forzado."""
    from dnd_sim.rules.checks import CheckResult

    def _fake(target, ability, dc, rng, mode=None):
        return CheckResult(ability=ability, dc=dc, rolls=[10], bonus=0,
                           total=10, success=exito, mode=RollMode.NORMAL)
    return _fake


def test_probabilidad_de_liberarse_con_cd_12():
    """CD 12 con bonus +0 -> ~45% por intento; media ~2,2 intentos."""
    objetivo = _pj("Objetivo")
    intentos = 20000
    exitos = 0
    rng = random.Random(1234)
    for _ in range(intentos):
        if ability_check(objetivo, "str", 12, rng).success:
            exitos += 1
    assert abs(exitos / intentos - 0.45) <= 0.015, exitos / intentos

    # Media de intentos hasta liberarse (geométrica con p = 0,45).
    rng2 = random.Random(4321)
    rondas = []
    for _ in range(5000):
        n = 1
        while not ability_check(objetivo, "str", 12, rng2).success:
            n += 1
        rondas.append(n)
    media = sum(rondas) / len(rondas)
    assert abs(media - 1 / 0.45) < 0.05, media


def test_consumes_action_gasta_la_accion_del_turno(monkeypatch):
    objetivo = _pj("Objetivo")
    escape = EscapeCheck(abilities=("str",), dc=12, consumes_action=True)
    apply_condition(objetivo, Condition.RESTRAINED, _ctx(), escape=escape)
    ctx = _ctx(actor=objetivo, combatants=[objetivo], rng=random.Random(2))
    begin_turn(objetivo, ctx)
    assert not ctx.resources.can_use(ActionType.ACTION), "la acción se gastó"
    assert ctx.resources.can_use(ActionType.BONUS_ACTION), "la acción adicional sigue"
    assert ctx.resources.can_use(ActionType.REACTION), "la reacción sigue"


def test_sin_consumes_action_conserva_la_accion(monkeypatch):
    objetivo = _pj("Objetivo")
    escape = EscapeCheck(abilities=("str",), dc=12, consumes_action=False)
    apply_condition(objetivo, Condition.RESTRAINED, _ctx(), escape=escape)
    ctx = _ctx(actor=objetivo, combatants=[objetivo], rng=random.Random(2))
    begin_turn(objetivo, ctx)
    assert ctx.resources.can_use(ActionType.ACTION)


def test_un_incapacitado_no_intenta_escapar_ni_consume_rng():
    objetivo = _pj("Objetivo")
    escape = EscapeCheck(abilities=("str",), dc=12, consumes_action=False)
    apply_condition(objetivo, Condition.PARALYZED, _ctx(), escape=escape)
    ctx = _ctx(actor=objetivo, combatants=[objetivo], rng=random.Random(2))
    estado = ctx.rng.getstate()
    begin_turn(objetivo, ctx)
    assert ctx.rng.getstate() == estado, "no se consume RNG"
    assert ctx.skip_turn is True
    assert objetivo.conditions.has(Condition.PARALYZED)


def test_dos_instancias_consumes_action_solo_intenta_la_primera():
    objetivo = _pj("Objetivo")
    escape = EscapeCheck(abilities=("str",), dc=12, consumes_action=True)
    apply_condition(objetivo, Condition.RESTRAINED, _ctx(), escape=escape)
    apply_condition(objetivo, Condition.RESTRAINED, _ctx(), escape=escape)
    ctx = _ctx(actor=objetivo, combatants=[objetivo], rng=random.Random(2))
    intentos = {}
    ctx.escape_attempts = intentos
    begin_turn(objetivo, ctx)
    assert intentos.get("restrained") == 1, intentos
    # La condición sigue (el escape falló), pero solo se intentó una vez.
    assert objetivo.conditions.has(Condition.RESTRAINED)


def test_con_dos_caracteristicas_se_elige_una_al_azar():
    objetivo = _pj("Objetivo")
    escape = EscapeCheck(abilities=("str", "dex"), dc=12, consumes_action=False)
    apply_condition(objetivo, Condition.RESTRAINED, _ctx(), escape=escape)
    conteo = Counter()
    for _ in range(20000):
        ctx = _ctx(actor=objetivo, combatants=[objetivo], rng=random.Random(_))
        objetivo.conditions.clear()
        apply_condition(objetivo, Condition.RESTRAINED, ctx, escape=escape)
        intentos = {}
        ctx.escape_attempts = intentos
        attempt_escapes(objetivo, ctx)
        for linea in ctx.log:
            if "prueba" in linea:
                conteo[linea.split("prueba ")[1][0]] += 1
    total = sum(conteo.values())
    assert abs(conteo["S"] / total - 0.5) <= 0.03, conteo
    assert abs(conteo["D"] / total - 0.5) <= 0.03, conteo


def test_con_una_sola_caracteristica_no_consume_rng():
    objetivo = _pj("Objetivo")
    escape = EscapeCheck(abilities=("str",), dc=12, consumes_action=False)
    apply_condition(objetivo, Condition.RESTRAINED, _ctx(), escape=escape)
    ctx = _ctx(actor=objetivo, combatants=[objetivo], rng=random.Random(2))
    estado = ctx.rng.getstate()
    attempt_escapes(objetivo, ctx)
    # Solo consume el RNG de la propia prueba (un d20), no el de elegir.
    assert ctx.rng.getstate() != estado


def test_el_escape_con_ventaja_condicionada_por_envenenamiento():
    objetivo = _pj("Objetivo")
    apply_condition(objetivo, Condition.POISONED, _ctx())
    escape = EscapeCheck(abilities=("str",), dc=12, consumes_action=False)
    apply_condition(objetivo, Condition.RESTRAINED, _ctx(), escape=escape)
    ctx = _ctx(actor=objetivo, combatants=[objetivo], rng=random.Random(2))
    objetivo.checks_with_advantage = {"str"}   # ventaja + desventaja -> normal
    rng = random.Random(3)
    exitos = sum(1 for _ in range(20000)
                 if ability_check(objetivo, "str", 12, rng).success)
    assert abs(exitos / 20000 - 0.45) <= 0.02, exitos / 20000


def test_una_condicion_sin_escape_no_genera_intentos():
    objetivo = _pj("Objetivo")
    apply_condition(objetivo, Condition.POISONED, _ctx())
    ctx = _ctx(actor=objetivo, combatants=[objetivo], rng=random.Random(2))
    intentos = {}
    ctx.escape_attempts = intentos
    estado = ctx.rng.getstate()
    attempt_escapes(objetivo, ctx)
    assert intentos == {}
    assert ctx.rng.getstate() == estado


def test_una_condicion_sin_salvacion_ni_escape_lanza_value_error():
    with pytest.raises(ValueError):
        ConditionEffect(condition=Condition.RESTRAINED, save_ability=None)


def test_el_fixture_de_la_constriccion_tiene_escape_y_avisa_de_grappled(monkeypatch):
    """Valores leídos del JSON del fixture."""
    data = _data("giant-constrictor-snake") if (
        FIXTURES / "giant-constrictor-snake.json").exists() else None
    if data is None:
        pytest.skip("sin fixture de giant-constrictor-snake")
    bruto = next(a for a in data["actions"] if a["name"] == "Constrict")
    assert "escape DC 16" in bruto["desc"]
    escape = parse_escape(bruto["desc"], "Giant Constrictor Snake", "Constrict")
    assert escape.dc == 16
    assert escape.abilities == ("str", "dex")
    assert escape.consumes_action is False


def test_un_pj_restringido_intenta_escapar_igual_que_un_monstruo(monkeypatch):
    """Un PJ restringido por un monstruo intenta escapar en su turno."""
    araña = _load(monkeypatch, "giant-spider")
    objetivo = _pj("Objetivo", hp=500)
    escape = EscapeCheck(abilities=("str",), dc=12, consumes_action=False)
    apply_condition(objetivo, Condition.RESTRAINED, _ctx(), escape=escape)
    ctx = _ctx(actor=objetivo, combatants=[objetivo], rng=random.Random(2))
    begin_turn(objetivo, ctx)
    assert any("prueba STR" in line for line in ctx.log), ctx.log


def test_el_orden_de_begin_turn_recarga_escape_y_salto():
    """(1) recursos, (2) recarga, (3) escape, (4) salto de turno."""
    objetivo = _pj("Objetivo")
    escape = EscapeCheck(abilities=("str",), dc=12, consumes_action=False)
    apply_condition(objetivo, Condition.RESTRAINED, _ctx(), escape=escape)
    ctx = _ctx(actor=objetivo, combatants=[objetivo], rng=random.Random(2))
    begin_turn(objetivo, ctx)
    # El escape se registra antes de cualquier salto de turno.
    indice_escape = next(i for i, l in enumerate(ctx.log) if "prueba" in l)
    assert indice_escape >= 0


# --- Distancia y cobertura -------------------------------------------------- #

def test_el_estado_de_distancia_inicial_y_el_reset():
    objetivo = _pj()
    assert objetivo.state.at_range is False
    objetivo.state.at_range = True
    objetivo.reset()
    assert objetivo.state.at_range is False


def test_un_ataque_a_distancia_pone_al_atacante_a_distancia():
    atacante, objetivo = _duelo()
    rng = random.Random(2)
    log: list[str] = []
    attack_roll(atacante, objetivo, _ataque(AttackRange.RANGED), rng, log)
    assert atacante.state.at_range is True
    attack_roll(atacante, objetivo, _ataque(AttackRange.MELEE), rng, log)
    assert atacante.state.at_range is False


def test_la_ca_efectiva_sube_dos_a_distancia():
    objetivo = _pj(ac=15)
    assert effective_ac(objetivo) == 15
    objetivo.state.at_range = True
    assert effective_ac(objetivo) == 17


def test_contra_un_objetivo_a_distancia_baja_el_impacto():
    """CA 11 (+2 = 13) con +0 a impacto: 40% de impacto."""
    atacante, objetivo = _duelo()
    objetivo.state.at_range = True
    atk = _ataque(AttackRange.MELEE)
    tasa = _tasa_de_impacto(atacante, objetivo, atk)
    assert abs(tasa - 0.40) <= 0.015, tasa

    # También a distancia.
    atacante2, objetivo2 = _duelo()
    objetivo2.state.at_range = True
    atk2 = _ataque(AttackRange.RANGED)
    tasa2 = _tasa_de_impacto(atacante2, objetivo2, atk2)
    assert abs(tasa2 - 0.40) <= 0.015, tasa2


def test_melee_or_ranged_consume_rng_siempre_y_el_estado_lo_sigue():
    atacante, objetivo = _duelo()
    atk = _ataque(AttackRange.MELEE_OR_RANGED)
    rng = random.Random(5)
    modos = Counter()
    for _ in range(20000):
        rango = resolve_attack_range(atk, rng)
        modos[rango] += 1
        atacante.state.at_range = (rango is AttackRange.RANGED)
    assert abs(modos[AttackRange.MELEE] / 20000 - 0.5) <= 0.03, modos
    assert abs(modos[AttackRange.RANGED] / 20000 - 0.5) <= 0.03, modos


def test_el_estado_cambia_ataque_a_ataque_en_un_multiataque(monkeypatch):
    """Un multiataque que mezcla melee y ranged va alternando."""
    dragon = _load(monkeypatch, "adult-red-dragon")
    objetivo = _pj("Objetivo", hp=5000, ac=11)
    objetivo.state.at_range = False
    estados = []
    rng = random.Random(3)
    log: list[str] = []
    for _ in range(20):
        ataque = next(a for a in dragon.attacks if a.name == "Claw")
        ataque.range_type = AttackRange.RANGED
        attack_roll(dragon, objetivo, ataque, rng, log)
        estados.append(dragon.state.at_range)
    assert all(estados), "un ataque a distancia deja al atacante a distancia"


def test_objetivo_derribado_y_melee_or_ranged_depende_del_modo():
    atacante, objetivo = _duelo()
    apply_condition(objetivo, Condition.PRONE, _ctx())
    atk = _ataque(AttackRange.MELEE_OR_RANGED)
    rng = random.Random(5)
    modos = Counter()
    for _ in range(20000):
        rango = resolve_attack_range(atk, rng)
        modos[attack_modifiers(atacante, objetivo, atk, rango).mode] += 1
    # Cuerpo a cuerpo -> ventaja; a distancia -> desventaja.
    assert abs(modos[RollMode.ADVANTAGE] / 20000 - 0.5) <= 0.03, modos
    assert abs(modos[RollMode.DISADVANTAGE] / 20000 - 0.5) <= 0.03, modos


def test_la_telaraña_deja_a_la_araña_a_distancia(monkeypatch):
    araña = _load(monkeypatch, "giant-spider")
    telaraña = next(a for a in araña.attacks if a.name == "Web")
    objetivo = _pj("Objetivo", hp=500)
    rng = random.Random(2)
    log: list[str] = []
    attack_roll(araña, objetivo, telaraña, rng, log)
    assert araña.state.at_range is True
    assert any("pasa a distancia" in line for line in log), log


def test_la_cobertura_no_cambia_las_salvaciones():
    from dnd_sim.rules.saves import saving_throw

    objetivo = _pj("Objetivo", ac=15)
    objetivo.state.at_range = True
    rng = random.Random(4)
    resultado = saving_throw(objetivo, "dex", 10, rng)
    # La CA no afecta a la supervivencia; el bonus es el de la característica.
    assert resultado.bonus == objetivo.abilities.mod("dex")


# --- Integración ------------------------------------------------------------ #

def test_en_un_combate_la_telaraña_inmoviliza_y_el_pj_intenta_escapar(monkeypatch):
    araña = _load(monkeypatch, "giant-spider")
    objetivo = _pj("Objetivo", hp=500, ac=5)
    objetivo.abilities = Abilities(str=30, dex=30, con=30, int=30, wis=30, cha=30)
    res = run_combat([objetivo, araña], random.Random(3), verbose=True, max_rounds=6)
    log = "\n".join(res.log)
    assert "inmovilizado" in log, log
    assert "prueba ATHLETICS" in log, log
    assert res.escape_attempts, res.escape_attempts


def test_reproducibilidad_con_escape_y_distancia(monkeypatch):
    araña = _load(monkeypatch, "giant-spider")
    pjs = [_pj("Guerrero", hp=60), _pj("Pícaro", hp=60)]
    a = simulate(pjs + [araña], n=20, seed=7)
    b = simulate(pjs + [araña], n=20, seed=7)
    assert a["win_rate"] == b["win_rate"]
    assert a["escape_attempts_avg"] == b["escape_attempts_avg"]
    assert a["escape_successes_avg"] == b["escape_successes_avg"]
    assert a["attacks_vs_at_range_avg"] == b["attacks_vs_at_range_avg"]

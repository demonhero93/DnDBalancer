"""Condiciones de D&D 5e: reglas de tirada, duración, estado y aplicación."""
import json
import random
import warnings
from collections import Counter
from pathlib import Path

import pytest

from dnd_sim import (
    Abilities, Attack, Condition, ConditionTracker, Monster, PlayerCharacter,
    RollMode, apply_condition, attack_modifiers, load_monster,
)
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.rules.area import AreaTargeting
from dnd_sim.engine.combat import attack_roll, run_combat
from dnd_sim.rules.conditions import (
    ConditionAction, ConditionEffect, ConditionInstance, EXCLUDED_CONDITIONS, RepeatSave, end_turn
)
from dnd_sim.rules.damage import apply_damage_modifiers
from dnd_sim.data.condition_parser import parse_condition_effects, parse_range_type
from dnd_sim.rules.roll_modifiers import (
    AttackRange, resolve_attack_range, save_modifiers
)
from dnd_sim.rules.saves import saving_throw
from dnd_sim.engine.stats import simulate

FIXTURES = Path(__file__).parent / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _data(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _load(monkeypatch, index: str, data=None):
    payload = data if data is not None else _data(index)
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: payload)
    return load_monster(index)


def _pj(name: str = "Guerrero", hp: int = 500, ac: int = 11) -> PlayerCharacter:
    """PJ de prueba (no es un monstruo: los monstruos vienen de la API)."""
    return PlayerCharacter(
        name=name, max_hp=hp, ac=ac, proficiency=2,
        abilities=Abilities(str=10, dex=10, con=10, int=10, wis=10, cha=10),
        attacks=[],
    )


def _ctx(actor=None, combatants=(), rng=None, log=None) -> CombatContext:
    return CombatContext(rng=rng or random.Random(1), actor=actor,
                         combatants=list(combatants), round=1,
                         log=log if log is not None else [],
                         verbose=True, resources=TurnResources())


def _duelo(ac: int = 11):
    """Atacante NPC con +0 a impacto y objetivo PJ con CA 11 -> 50% normal."""
    atacante = Monster(name="Atacante", max_hp=500, ac=10, abilities=Abilities())
    objetivo = _pj("Objetivo", hp=500, ac=ac)
    return atacante, objetivo


def _ataque(rango: AttackRange = AttackRange.MELEE) -> Attack:
    return Attack("Golpe", "1d6", ability="str", attack_bonus=0, damage_bonus=0,
                  range_type=rango)


def _tasa_de_impacto(attacker, target, atk, n: int = 20000, seed: int = 99) -> float:
    """Proporción de impactos de un ataque (el objetivo no muere)."""
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


# --- Catálogo cerrado ------------------------------------------------------- #

def test_el_enum_no_contiene_condiciones_excluidas():
    for clave in EXCLUDED_CONDITIONS:
        with pytest.raises(ValueError):
            Condition(clave.upper())
        assert clave not in {c.value for c in Condition}


def test_condicion_fuera_del_enum_lanza_value_error():
    with pytest.raises(ValueError):
        apply_condition(_pj(), "DEAFENED", _ctx())


# --- Implicaciones y estado ------------------------------------------------- #

def test_implicaciones_de_las_condiciones():
    for condition in (Condition.STUNNED, Condition.PARALYZED,
                      Condition.PETRIFIED, Condition.UNCONSCIOUS):
        tracker = ConditionTracker()
        tracker.add(ConditionInstance(condition))
        assert tracker.has(Condition.INCAPACITATED), condition

    tracker = ConditionTracker()
    tracker.add(ConditionInstance(Condition.UNCONSCIOUS))
    assert tracker.has(Condition.PRONE)

    tracker = ConditionTracker()
    tracker.add(ConditionInstance(Condition.POISONED))
    assert not tracker.has(Condition.INCAPACITATED)
    assert not tracker.has(Condition.PRONE)


def test_can_act_y_can_react():
    pj = _pj()
    assert pj.can_act and pj.can_react
    apply_condition(pj, Condition.STUNNED, _ctx())
    assert not pj.can_act
    assert not pj.can_react

    pj2 = _pj()
    apply_condition(pj2, Condition.POISONED, _ctx())
    assert pj2.can_act and pj2.can_react


def test_un_combatiente_a_0_hp_no_puede_actuar_ni_reaccionar():
    pj = _pj()
    pj.hp = 0
    assert not pj.can_act
    assert not pj.can_react


# --- Reglas de tirada de ataque -------------------------------------------- #

def test_objetivo_derribado_ventaja_a_cuerpo_a_cuerpo():
    atacante, objetivo = _duelo()
    apply_condition(objetivo, Condition.PRONE, _ctx())
    tasa = _tasa_de_impacto(atacante, objetivo, _ataque(AttackRange.MELEE))
    assert abs(tasa - 0.75) <= 0.015, tasa


def test_objetivo_derribado_desventaja_a_distancia():
    atacante, objetivo = _duelo()
    apply_condition(objetivo, Condition.PRONE, _ctx())
    tasa = _tasa_de_impacto(atacante, objetivo, _ataque(AttackRange.RANGED))
    assert abs(tasa - 0.25) <= 0.015, tasa


@pytest.mark.parametrize("condition", [Condition.POISONED, Condition.FRIGHTENED,
                                       Condition.BLINDED, Condition.PRONE,
                                       Condition.RESTRAINED])
def test_atacante_afectado_tiene_desventaja(condition):
    atacante, objetivo = _duelo()
    apply_condition(atacante, condition, _ctx())
    tasa = _tasa_de_impacto(atacante, objetivo, _ataque())
    assert abs(tasa - 0.25) <= 0.015, f"{condition}: {tasa}"


@pytest.mark.parametrize("condition", [Condition.BLINDED, Condition.RESTRAINED,
                                       Condition.STUNNED, Condition.PARALYZED,
                                       Condition.UNCONSCIOUS, Condition.PETRIFIED])
def test_objetivo_afectado_da_ventaja(condition):
    atacante, objetivo = _duelo()
    apply_condition(objetivo, condition, _ctx())
    tasa = _tasa_de_impacto(atacante, objetivo, _ataque())
    assert abs(tasa - 0.75) <= 0.015, f"{condition}: {tasa}"


def test_ventaja_y_desventaja_se_anulan():
    atacante, objetivo = _duelo()
    apply_condition(atacante, Condition.POISONED, _ctx())
    apply_condition(objetivo, Condition.RESTRAINED, _ctx())
    tasa = _tasa_de_impacto(atacante, objetivo, _ataque())
    assert abs(tasa - 0.50) <= 0.015, tasa


def test_dos_ventajas_y_una_desventaja_se_anulan():
    atacante, objetivo = _duelo()
    atacante.attacks_with_advantage = True          # ventaja 1
    apply_condition(atacante, Condition.POISONED, _ctx())   # desventaja
    apply_condition(objetivo, Condition.RESTRAINED, _ctx())  # ventaja 2
    tasa = _tasa_de_impacto(atacante, objetivo, _ataque())
    assert abs(tasa - 0.50) <= 0.015, tasa


def test_melee_or_ranged_elige_uno_de_los_dos_modos():
    """El rango se decide con ``pick`` en cada ataque (50/50)."""
    atacante, objetivo = _duelo()
    apply_condition(objetivo, Condition.PRONE, _ctx())
    atk = _ataque(AttackRange.MELEE_OR_RANGED)
    rng = random.Random(5)
    modos = Counter()
    for _ in range(20000):
        rango = resolve_attack_range(atk, rng)
        modos[attack_modifiers(atacante, objetivo, atk, rango).mode] += 1
    assert abs(modos[RollMode.ADVANTAGE] / 20000 - 0.5) <= 0.03
    assert abs(modos[RollMode.DISADVANTAGE] / 20000 - 0.5) <= 0.03


def test_melee_or_ranged_consume_rng_siempre():
    """Ahora el rango se decide SIEMPRE: consume RNG en cada ataque."""
    atacante, objetivo = _duelo()
    atk = _ataque(AttackRange.MELEE_OR_RANGED)
    rng = random.Random(5)
    estado = rng.getstate()
    resolve_attack_range(atk, rng)
    assert rng.getstate() != estado, "el rango se decide siempre (consume RNG)"


def test_melee_or_ranged_no_consume_rng_para_un_ataque_fijo():
    atacante, objetivo = _duelo()
    atk = _ataque(AttackRange.MELEE)
    rng = random.Random(5)
    estado = rng.getstate()
    assert resolve_attack_range(atk, rng) is AttackRange.MELEE
    assert rng.getstate() == estado


def test_critico_automatico_contra_paralizado_a_cuerpo_a_cuerpo():
    atacante, objetivo = _duelo()
    apply_condition(objetivo, Condition.PARALYZED, _ctx())
    log: list[str] = []
    rng = random.Random(3)
    for _ in range(200):
        objetivo.hp = objetivo.max_hp
        log.clear()
        attack_roll(atacante, objetivo, _ataque(AttackRange.MELEE), rng, log)
        if log and "falla" not in log[0]:
            assert "CRÍTICO" in log[0], log[0]


def test_un_1_natural_sigue_fallando_contra_un_paralizado():
    """El 1 natural siempre falla (pifia); con ventaja, solo si ambos dados
    son 1 (0,25% en vez del 5% habitual)."""
    atacante, objetivo = _duelo(ac=1)  # CA 1: solo falla por pifia
    log: list[str] = []
    rng = random.Random(3)

    pifias = 0
    for _ in range(20000):
        objetivo.hp = objetivo.max_hp
        log.clear()
        attack_roll(atacante, objetivo, _ataque(AttackRange.MELEE), rng, log)
        if log and "falla" in log[0]:
            pifias += 1
    assert abs(pifias / 20000 - 0.05) <= 0.02, pifias / 20000

    # Con ventaja (objetivo paralizado) la pifia solo ocurre si ambos dados
    # son 1: 0,25%.
    apply_condition(objetivo, Condition.PARALYZED, _ctx())
    pifias = 0
    for _ in range(20000):
        objetivo.hp = objetivo.max_hp
        log.clear()
        attack_roll(atacante, objetivo, _ataque(AttackRange.MELEE), rng, log)
        if log and "falla" in log[0]:
            pifias += 1
    assert abs(pifias / 20000 - 0.0025) <= 0.002, pifias / 20000


def test_sin_critico_automatico_a_distancia():
    """A cuerpo a cuerpo todo impacto es crítico; a distancia, solo el natural."""
    atacante, objetivo = _duelo()
    apply_condition(objetivo, Condition.PARALYZED, _ctx())
    log: list[str] = []
    rng = random.Random(3)

    def _tasas(rango) -> tuple[float, float]:
        criticos = impactos = 0
        for _ in range(2000):
            objetivo.hp = objetivo.max_hp
            log.clear()
            attack_roll(atacante, objetivo, _ataque(rango), rng, log)
            if log and "falla" not in log[0]:
                impactos += 1
                if "CRÍTICO" in log[0]:
                    criticos += 1
        return criticos / 2000, impactos / 2000

    criticos_melee, impactos_melee = _tasas(AttackRange.MELEE)
    assert criticos_melee == impactos_melee, "todo impacto a cuerpo a cuerpo es crítico"

    criticos_ranged, impactos_ranged = _tasas(AttackRange.RANGED)
    assert criticos_ranged < impactos_ranged * 0.5, "a distancia no hay crítico automático"


def test_los_indicadores_estaticos_siguen_funcionando_y_se_combinan():
    atacante, objetivo = _duelo()
    atacante.attacks_with_advantage = True
    tasa = _tasa_de_impacto(atacante, objetivo, _ataque())
    assert abs(tasa - 0.75) <= 0.015, tasa

    # Con una condición que da desventaja, se anulan.
    apply_condition(atacante, Condition.POISONED, _ctx())
    tasa = _tasa_de_impacto(atacante, objetivo, _ataque())
    assert abs(tasa - 0.50) <= 0.015, tasa


# --- Salvaciones ------------------------------------------------------------ #

@pytest.mark.parametrize("condition", [Condition.STUNNED, Condition.PARALYZED,
                                       Condition.UNCONSCIOUS, Condition.PETRIFIED])
@pytest.mark.parametrize("ability", ["str", "dex"])
def test_las_condiciones_incapacitantes_fallan_fue_y_des_sin_tirar_dados(condition, ability):
    objetivo = Monster(name="Objetivo", max_hp=100, ac=10, abilities=Abilities(str=30, dex=30))
    apply_condition(objetivo, condition, _ctx())
    rng = random.Random(7)
    estado = rng.getstate()
    resultado = saving_throw(objetivo, ability, 5, rng)
    assert resultado.success is False
    assert resultado.auto_fail is True
    assert resultado.rolls == []
    assert rng.getstate() == estado, "un fallo automático no consume RNG"


def test_las_condiciones_incapacitantes_no_fallan_automaticamente_la_con():
    objetivo = Monster(name="Objetivo", max_hp=100, ac=10, abilities=Abilities(con=30))
    apply_condition(objetivo, Condition.STUNNED, _ctx())
    rng = random.Random(7)
    resultado = saving_throw(objetivo, "con", 5, rng)
    assert resultado.auto_fail is False
    assert resultado.success is True


def test_inmovilizado_da_desventaja_solo_en_des():
    objetivo = Monster(name="Objetivo", max_hp=100, ac=10, abilities=Abilities())
    apply_condition(objetivo, Condition.RESTRAINED, _ctx())
    assert save_modifiers(objetivo, "dex").mode is RollMode.DISADVANTAGE
    assert save_modifiers(objetivo, "con").mode is RollMode.NORMAL


# --- Daño con petrificado --------------------------------------------------- #

def test_petrificado_tiene_resistencia_a_todo():
    objetivo = Monster(name="Objetivo", max_hp=100, ac=10, abilities=Abilities())
    apply_condition(objetivo, Condition.PETRIFIED, _ctx())
    assert apply_damage_modifiers(9, "fire", objetivo) == 4

    inmune = Monster(name="Inmune", max_hp=100, ac=10, abilities=Abilities(),
                     immunities={"fire"})
    apply_condition(inmune, Condition.PETRIFIED, _ctx())
    assert apply_damage_modifiers(9, "fire", inmune) == 0

    # Orden implementado: inmunidad, resistencia, vulnerabilidad (9 -> 4 -> 8).
    vulnerable = Monster(name="Vulnerable", max_hp=100, ac=10, abilities=Abilities(),
                          vulnerabilities={"fire"})
    apply_condition(vulnerable, Condition.PETRIFIED, _ctx())
    assert apply_damage_modifiers(9, "fire", vulnerable) == 8


def test_sin_condiciones_el_dano_no_cambia():
    objetivo = Monster(name="Objetivo", max_hp=100, ac=10, abilities=Abilities())
    assert apply_damage_modifiers(9, "fire", objetivo) == 9


# --- Duración y estado ------------------------------------------------------ #

def test_una_condicion_de_2_rondas_termina_al_final_del_segundo_turno():
    pj = _pj()
    ctx = _ctx(actor=pj, combatants=[pj])
    apply_condition(pj, Condition.POISONED, ctx, duration_rounds=2)
    assert pj.conditions.has(Condition.POISONED)

    end_turn(pj, ctx)          # final del primer turno propio
    assert pj.conditions.has(Condition.POISONED), "no termina antes de tiempo"
    end_turn(pj, ctx)          # final del segundo turno propio
    assert not pj.conditions.has(Condition.POISONED)


def test_una_sin_duracion_dura_hasta_el_fin_del_combate():
    pj = _pj()
    ctx = _ctx(actor=pj, combatants=[pj])
    apply_condition(pj, Condition.FRIGHTENED, ctx, duration_rounds=None)
    for _ in range(20):
        end_turn(pj, ctx)
    assert pj.conditions.has(Condition.FRIGHTENED)


def test_repeat_save_con_exito_elimina_la_condicion_al_final_del_turno():
    pj = _pj()
    ctx = _ctx(actor=pj, combatants=[pj])
    apply_condition(pj, Condition.PARALYZED, ctx, duration_rounds=10,
                    repeat_save=RepeatSave(ability="con", dc=5))
    # Con un bonus alto, la repetición tiene éxito.
    pj.save_overrides["con"] = 30
    end_turn(pj, ctx)
    assert not pj.conditions.has(Condition.PARALYZED)


def test_repeat_save_con_fallo_la_condicion_sigue_y_la_duracion_baja():
    pj = _pj()
    ctx = _ctx(actor=pj, combatants=[pj])
    apply_condition(pj, Condition.PARALYZED, ctx, duration_rounds=10,
                    repeat_save=RepeatSave(ability="con", dc=99))
    end_turn(pj, ctx)
    assert pj.conditions.has(Condition.PARALYZED)
    assert pj.conditions.instances[0].remaining_rounds == 9


def test_dos_instancias_de_la_misma_condicion_de_fuentes_distintas():
    pj = _pj()
    ctx = _ctx(actor=pj, combatants=[pj])
    apply_condition(pj, Condition.PRONE, ctx, duration_rounds=1)
    apply_condition(pj, Condition.PRONE, ctx, duration_rounds=5)
    assert len(pj.conditions.instances) == 2
    end_turn(pj, ctx)
    assert pj.conditions.has(Condition.PRONE), "sigue la otra instancia"
    for _ in range(5):
        end_turn(pj, ctx)
    assert not pj.conditions.has(Condition.PRONE)


def test_reset_limpia_las_condiciones():
    pj = _pj()
    apply_condition(pj, Condition.STUNNED, _ctx())
    assert pj.conditions.has(Condition.STUNNED)
    pj.reset()
    assert not pj.conditions.has(Condition.STUNNED)


def test_dos_combates_seguidos_empiezan_sin_condiciones():
    pj = _pj()
    npc = Monster(name="Ogro", max_hp=100, ac=10, abilities=Abilities())
    apply_condition(pj, Condition.STUNNED, _ctx())
    run_combat([pj, npc], random.Random(1), max_rounds=2)
    assert not pj.conditions.has(Condition.STUNNED)


# --- Motor: turno perdido, reacciones y política ---------------------------- #

def test_un_incapacitado_pierde_el_turno_sin_consumir_rng():
    pj = _pj()
    npc = Monster(name="Ogro", max_hp=100, ac=10, abilities=Abilities())
    apply_condition(pj, Condition.STUNNED, _ctx())
    ctx = _ctx(actor=pj, combatants=[pj, npc], rng=random.Random(4))
    from dnd_sim.rules.usage import begin_turn
    rng = ctx.rng
    estado = rng.getstate()
    begin_turn(pj, ctx)
    assert ctx.skip_turn is True
    assert rng.getstate() == estado, "perder el turno no consume RNG"
    assert any("incapacitado" in line for line in ctx.log)


def test_la_politica_no_se_invoca_para_un_incapacitado(monkeypatch):
    import dnd_sim.engine.combat.encounter as combat_mod

    pj = _pj()
    npc = Monster(name="Ogro", max_hp=100, ac=10, abilities=Abilities())
    llamadas = {"n": 0}

    def spy(policy, ctx, candidates):
        llamadas["n"] += 1
        return candidates[0]

    monkeypatch.setattr(combat_mod, "_invoke_policy", spy)
    apply_condition(pj, Condition.STUNNED, _ctx())
    run_combat([pj, npc], random.Random(1), max_rounds=3)
    assert llamadas["n"] == 0


def test_una_reaccion_no_se_dispara_en_un_combatiente_incapacitado(monkeypatch):
    import dnd_sim.rules.damage as damage_mod

    pj = _pj()
    recibidos = []
    monkeypatch.setattr(damage_mod, "DAMAGE_TAKEN", [lambda **kw: recibidos.append(kw)])
    monkeypatch.setattr(damage_mod, "DAMAGE_TAKEN_CALLBACKS", [])
    monkeypatch.setattr(damage_mod, "DAMAGE_TAKEN_REACTIONS", [])

    apply_condition(pj, Condition.STUNNED, _ctx())
    damage_mod.inflict_damage(pj, 5, "fire", source=None)
    assert recibidos == []

    pj2 = _pj()
    damage_mod.inflict_damage(pj2, 5, "fire", source=None)
    assert len(recibidos) == 1


# --- Aplicación y loader ---------------------------------------------------- #

def test_el_lobo_derriba_con_la_salvacion_del_json(monkeypatch):
    lobo = _load(monkeypatch, "wolf")
    ataque = next(a for a in lobo.attacks if a.name == "Bite")
    rider = ataque.condition_riders[0]
    # Valores leídos del JSON del fixture.
    assert rider.condition is Condition.PRONE
    assert rider.save_ability == "str"
    assert rider.dc == 11
    assert rider.duration_rounds == 1
    assert ataque.range_type is AttackRange.MELEE


def test_el_lobo_solo_derriba_si_falla_la_salvacion(monkeypatch):
    lobo = _load(monkeypatch, "wolf")
    ataque = next(a for a in lobo.attacks if a.name == "Bite")
    objetivo = _pj("Objetivo", hp=500, ac=1)
    objetivo.save_overrides["str"] = 30   # supera la CD 11 con facilidad
    rng = random.Random(11)
    log: list[str] = []
    for _ in range(50):
        objetivo.hp = objetivo.max_hp
        log.clear()
        attack_roll(lobo, objetivo, ataque, rng, log)
    assert not objetivo.conditions.has(Condition.PRONE)

    # Con un bonus muy negativo, la一次次 Peer sale.
    objetivo2 = _pj("Objetivo2", hp=500, ac=1)
    objetivo2.save_overrides["str"] = -30
    for _ in range(50):
        objetivo2.hp = objetivo2.max_hp
        attack_roll(lobo, objetivo2, ataque, rng, log)
    assert objetivo2.conditions.has(Condition.PRONE)


def test_el_lobo_no_derriba_si_el_ataque_falla(monkeypatch):
    """La condición solo se aplica si el ataque impacta."""
    lobo = _load(monkeypatch, "wolf")
    ataque = next(a for a in lobo.attacks if a.name == "Bite")
    objetivo = _pj("Objetivo", hp=5000, ac=100)  # CA 100: solo el 20 natural impacta
    objetivo.save_overrides["str"] = -30
    rng = random.Random(11)
    log: list[str] = []
    impactos = 0
    for _ in range(200):
        objetivo.hp = objetivo.max_hp
        objetivo.conditions.clear()
        log.clear()
        attack_roll(lobo, objetivo, ataque, rng, log)
        if "falla" in log[0]:
            assert not objetivo.conditions.has(Condition.PRONE)
        else:
            impactos += 1
            assert objetivo.conditions.has(Condition.PRONE)
    assert impactos > 0


def test_el_ghoul_paraliza_con_diez_rondas_y_salvacion_de_repeticion(monkeypatch):
    ghoul = _load(monkeypatch, "ghoul")
    ataque = next(a for a in ghoul.attacks if a.name == "Claws")
    rider = ataque.condition_riders[0]
    assert rider.condition is Condition.PARALYZED
    assert rider.save_ability == "con"
    assert rider.dc == 10
    assert rider.duration_rounds == 10
    assert rider.repeat_save is True


def test_la_accion_de_condicion_del_dragon_es_un_condition_action(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    multiattack = dragon.multiattack
    assert multiattack is not None
    accion = multiattack.action_entries["Frightful Presence"]
    assert isinstance(accion, ConditionAction)
    efecto = accion.effect
    assert efecto.condition is Condition.FRIGHTENED
    assert efecto.save_ability == "wis"
    assert efecto.dc == 19
    assert efecto.duration_rounds == 10
    assert efecto.repeat_save is True


def test_una_condicion_excluida_avisa_y_no_se_aplica(monkeypatch):
    """'deafened' está en EXCLUDED_CONDITIONS: avisa y no la aplica."""
    data = _data("ogre")
    data["actions"].append({
        "name": "Mirada",
        "desc": ("The ogre stares. Each creature must succeed on a DC 12 Wisdom "
                 "saving throw or be deafened for 1 minute."),
        "dc": {"dc_type": {"index": "wis"}, "dc_value": 12, "success_type": "none"},
        "damage": [],
        "actions": [],
    })
    with pytest.warns(UserWarning, match="deafened"):
        monster = _load(monkeypatch, "ogre", data)
    nombres = [getattr(a, "name", "") for a in monster.actions]
    assert "Mirada" not in nombres


def test_el_hechizado_ahora_si_se_aplica(monkeypatch):
    """"charmed" ya no está excluida: se modela como condición."""
    data = _data("ogre")
    data["actions"].append({
        "name": "Mirada",
        "desc": ("The ogre stares. Each creature must succeed on a DC 12 Wisdom "
                 "saving throw or be charmed for 1 minute."),
        "dc": {"dc_type": {"index": "wis"}, "dc_value": 12, "success_type": "none"},
        "damage": [],
        "actions": [],
    })
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        monster = _load(monkeypatch, "ogre", data)
    accion = next(a for a in monster.actions if getattr(a, "name", "") == "Mirada")
    assert accion.effect.condition is Condition.CHARMED
    assert accion.effect.save_ability == "wis"
    assert accion.effect.dc == 12
    assert accion.effect.duration_rounds == 10


def test_una_duracion_no_reconocida_avisa_y_no_se_aplica(monkeypatch):
    data = _data("ogre")
    data["actions"].append({
        "name": "Gruñido",
        "desc": ("Each creature must succeed on a DC 12 Wisdom saving throw or be "
                 "frightened for a really long while."),
        "dc": {"dc_type": {"index": "wis"}, "dc_value": 12, "success_type": "none"},
        "damage": [],
        "actions": [],
    })
    with pytest.warns(UserWarning, match="Duración no reconocida"):
        monster = _load(monkeypatch, "ogre", data)
    nombres = [getattr(a, "name", "") for a in monster.actions]
    assert "Gruñido" not in nombres


def test_el_tipo_de_ataque_coincide_con_el_texto():
    assert parse_range_type("Melee Weapon Attack: +4 to hit", "Ogro", "Golpe") is AttackRange.MELEE
    assert parse_range_type("Ranged Weapon Attack: +4 to hit", "Ogro", "Dardo") is AttackRange.RANGED
    assert parse_range_type("Melee or Ranged Weapon Attack: +6 to hit", "Ogro", "Jabalina") is AttackRange.MELEE_OR_RANGED


def test_cada_fixture_tiene_un_tipo_de_ataque_coherente():
    for indice, esperado in (("ogre", {"Greatclub": AttackRange.MELEE,
                                       "Javelin": AttackRange.MELEE_OR_RANGED}),
                             ("chimera", {"Bite": AttackRange.MELEE}),
                             ("adult-red-dragon", {"Bite": AttackRange.MELEE})):
        data = _data(indice)
        for accion in data["actions"]:
            if accion.get("name") in esperado and accion.get("attack_bonus") is not None:
                assert parse_range_type(accion["desc"], indice, accion["name"]) is esperado[accion["name"]]


def test_un_condition_action_no_aplica_condiciones_a_aliados(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    accion = dragon.multiattack.action_entries["Frightful Presence"]
    aliado = Monster(name="Aliado", max_hp=100, ac=10, abilities=Abilities())
    enemigo = _pj("Enemigo", hp=200)
    dragon.combatant_type = dragon.combatant_type  # (NPC)
    ctx = _ctx(actor=dragon, combatants=[dragon, aliado, enemigo], rng=random.Random(2))
    accion.execute(ctx)
    assert not aliado.conditions.has(Condition.FRIGHTENED)
    assert enemigo.conditions.has(Condition.FRIGHTENED)


def test_un_condition_action_respeta_el_area_targeting(monkeypatch):
    dragon = _load(monkeypatch, "adult-red-dragon")
    accion = dragon.multiattack.action_entries["Frightful Presence"]
    enemigos = [_pj(f"Enemigo{i}", hp=200) for i in range(4)]
    for enemigo in enemigos:
        enemigo.save_overrides["wis"] = -30  # falla la CDL 19 seguro
    ctx = _ctx(actor=dragon, combatants=[dragon] + enemigos, rng=random.Random(3))
    accion.execute(ctx)
    afectados = [e for e in enemigos if e.conditions.has(Condition.FRIGHTENED)]
    assert 1 <= len(afectados) <= 4


# --- Simulación completa ---------------------------------------------------- #

def test_simulacion_con_ghoul_informa_de_turnos_perdidos(monkeypatch):
    ghoul = _load(monkeypatch, "ghoul")
    pjs = [_pj("Guerrero", hp=60), _pj("Pícaro", hp=60), _pj("Monje", hp=60)]
    stats = simulate(pjs + [ghoul], n=50, seed=1)
    assert stats["turns_lost_incapacitated_avg"]
    assert sum(stats["turns_lost_incapacitated_avg"].values()) > 0
    assert stats["conditions_applied_avg"].get("paralyzed", 0) > 0


def test_reproducibilidad_con_condiciones(monkeypatch):
    ghoul = _load(monkeypatch, "ghoul")
    pjs = [_pj("Guerrero", hp=60), _pj("Pícaro", hp=60)]
    a = simulate(pjs + [ghoul], n=20, seed=7)
    b = simulate(pjs + [ghoul], n=20, seed=7)
    assert a["win_rate"] == b["win_rate"]
    assert a["conditions_applied_avg"] == b["conditions_applied_avg"]
    assert a["turns_lost_incapacitated_avg"] == b["turns_lost_incapacitated_avg"]

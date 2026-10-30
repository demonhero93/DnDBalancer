"""Tests de la clase bárbaro (PHB 2024, sin subclases)."""
from __future__ import annotations

import json
import random
from pathlib import Path
from types import SimpleNamespace

import pytest

from dnd_sim import (
    Abilities, Attack, AttackModifiers, BarbarianFeatures, CheckModifiers,
    ExtendRageAction, PlayerCharacter, RageAction, RollMode, SaveModifiers,
    ability_check, apply_barbarian, rage_damage, rage_uses, saving_throw,
    skill_check,
)
from dnd_sim.core.classes import (
    BARBARIAN_FEATURES, extra_attacks_for,
)
from dnd_sim.rules.classes.barbarian import features as barb_mod

FIXTURES = Path(__file__).parent / "fixtures"


def _abilities(**kwargs) -> Abilities:
    base = dict(str=10, dex=10, con=10, int=10, wis=10, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    kwargs.setdefault("name", "Thor")
    kwargs.setdefault("max_hp", 80)
    kwargs.setdefault("ac", 12)
    kwargs.setdefault("abilities", _abilities())
    kwargs.setdefault(
        "attacks",
        [Attack("Hacha de batalla", "1d12", ability="str")],
    )
    return PlayerCharacter(**kwargs)


def _trait(pj, level: int) -> BarbarianFeatures:
    trait = BarbarianFeatures(name="Bárbaro", level=level)
    trait.owner = pj
    pj.traits.append(trait)
    return trait


def _ctx(actor, round_: int = 1, rng: random.Random | None = None):
    return SimpleNamespace(actor=actor, round=round_,
                           rng=rng or random.Random(1), log=[], resources=None)


# --- Tablas de clase ---------------------------------------------------------

def test_rage_uses_tabla_phb():
    casos = {1: 2, 2: 2, 3: 3, 5: 3, 6: 4, 11: 4, 12: 5, 16: 5,
             17: 6, 20: 6}
    for nivel, esperado in casos.items():
        assert rage_uses(nivel) == esperado


def test_rage_damage_tabla_phb():
    casos = {1: 2, 8: 2, 9: 3, 15: 3, 16: 4, 20: 4}
    for nivel, esperado in casos.items():
        assert rage_damage(nivel) == esperado


def test_extra_attacks_desde_nivel_5():
    assert extra_attacks_for(1) == 1
    assert extra_attacks_for(4) == 1
    assert extra_attacks_for(5) == 2
    assert extra_attacks_for(20) == 2


def test_features_de_clase_coinciden_con_la_api():
    datos = json.loads(
        (FIXTURES / "barbarian_levels.json").read_text(encoding="utf-8-sig")
    )
    for entrada in datos:
        nivel = int(entrada["level"])
        esperadas = tuple(f["name"] for f in entrada["features"])
        assert BARBARIAN_FEATURES[nivel] == esperadas, f"nivel {nivel}"


# --- apply_barbarian ---------------------------------------------------------

def test_apply_salvaciones_y_habilidades():
    pj = _pj(level=5)
    apply_barbarian(pj, skills=("athletics", "nature"))
    assert pj.save_proficiencies == {"str", "con"}
    assert {"athletics", "nature"} <= pj.skill_proficiencies


def test_apply_habilidad_fuera_de_lista_lanza_error():
    pj = _pj(level=5)
    with pytest.raises(ValueError):
        apply_barbarian(pj, skills=("stealth",))


def test_apply_unarmored_defense_sube_la_ca():
    pj = _pj(level=1, ac=13, abilities=_abilities(str=16, dex=14, con=16))
    apply_barbarian(pj)
    # 10 + DEX(+2) + CON(+3) = 15 > 13
    assert pj.ac == 15


def test_apply_unarmored_defense_no_baja_la_ca():
    pj = _pj(level=1, ac=18, abilities=_abilities(dex=10, con=10))
    apply_barbarian(pj)
    assert pj.ac == 18


def test_apply_sin_level_usa_nivel_1():
    pj = _pj()
    assert pj.level is None
    trait = apply_barbarian(pj)
    assert trait.level == 1
    rage = [a for a in pj.actions if isinstance(a, RageAction)][0]
    assert rage.usage.uses_max == rage_uses(1)


def test_apply_extra_attack_sustituye_ataques_por_multiataque():
    from dnd_sim import AttackAction, MultiattackAction
    pj = _pj(level=5)
    assert any(isinstance(a, AttackAction) for a in pj.actions)
    apply_barbarian(pj)
    multis = [a for a in pj.actions if isinstance(a, MultiattackAction)]
    assert len(multis) == 1
    assert not any(isinstance(a, AttackAction) for a in pj.actions)
    # El Multiattack tiene una alternativa con 2 golpes.
    assert sum(e.count for e in multis[0].options[0]) == 2


def test_apply_extra_attack_sin_ataques_no_explota():
    pj = _pj(level=5, attacks=[])
    apply_barbarian(pj)  # no lanza
    from dnd_sim import MultiattackAction
    assert not any(isinstance(a, MultiattackAction) for a in pj.actions)


def test_apply_feral_instinct_nivel_7():
    pj5 = _pj(level=5)
    apply_barbarian(pj5)
    assert pj5.initiative_with_advantage is False
    pj7 = _pj(level=7)
    apply_barbarian(pj7)
    assert pj7.initiative_with_advantage is True


def test_apply_anade_acciones_de_furia():
    pj = _pj(level=5)
    apply_barbarian(pj)
    assert any(isinstance(a, RageAction) for a in pj.actions)
    assert any(isinstance(a, ExtendRageAction) for a in pj.actions)
    assert any(isinstance(t, BarbarianFeatures) for t in pj.traits)


# --- Furia: activación y usos ------------------------------------------------

def test_rage_action_gasta_usos():
    pj = _pj(level=5)
    apply_barbarian(pj)
    rage = [a for a in pj.actions if isinstance(a, RageAction)][0]
    ctx = _ctx(pj, round_=1)
    assert rage.can_use(None, ctx) is True
    rage.execute(ctx)
    trait = [t for t in pj.traits if isinstance(t, BarbarianFeatures)][0]
    assert trait.rage_active is True
    assert trait.rage_expires_round == 2  # hasta el fin del siguiente turno
    # El motor gasta el uso; aquí lo simulamos igual que el engine.
    rage.usage.spend()
    assert rage.usage.uses_left == 2
    rage.usage.uses_left = 0
    assert rage.can_use(None, ctx) is False  # sin usos


def test_rage_action_no_disponible_si_ya_activa():
    pj = _pj(level=5)
    apply_barbarian(pj)
    trait = [t for t in pj.traits if isinstance(t, BarbarianFeatures)][0]
    trait.rage_active = True
    rage = [a for a in pj.actions if isinstance(a, RageAction)][0]
    assert rage.can_use(None, _ctx(pj)) is False


def test_extend_rage_action_usada_cuando_no_hubo_combate():
    pj = _pj(level=5)
    apply_barbarian(pj)
    trait = [t for t in pj.traits if isinstance(t, BarbarianFeatures)][0]
    trait.activate(round_=5)
    ext = [a for a in pj.actions if isinstance(a, ExtendRageAction)][0]
    # Ronda 5 (< expira en 6): aún no toca.
    assert ext.can_use(None, _ctx(pj, round_=5)) is False
    # Ronda 6 sin atacar ni forzar salvación: toca extender.
    ctx = _ctx(pj, round_=6)
    assert ext.can_use(None, ctx) is True
    ext.execute(ctx)
    assert trait.rage_expires_round == 7


def test_extend_rage_action_no_disponible_si_ya_se_extendio_sola():
    pj = _pj(level=5)
    apply_barbarian(pj)
    trait = [t for t in pj.traits if isinstance(t, BarbarianFeatures)][0]
    trait.activate(round_=5)
    ext = [a for a in pj.actions if isinstance(a, ExtendRageAction)][0]
    pj.state.attacked_this_turn = True
    assert ext.can_use(None, _ctx(pj, round_=6)) is False


# --- Furia: efectos ----------------------------------------------------------

def test_furia_resistencia_bps_y_no_fuego():
    from dnd_sim import inflict_damage
    pj = _pj(level=1)
    trait = _trait(pj, 1)
    trait.activate(round_=1)
    pj.hp = pj.max_hp
    inflict_damage(pj, 8, "bludgeoning")
    assert pj.hp == pj.max_hp - 4
    inflict_damage(pj, 8, "fire")
    assert pj.hp == pj.max_hp - 4 - 8


def test_furia_sin_activa_no_resiste():
    from dnd_sim import inflict_damage
    pj = _pj(level=1)
    _trait(pj, 1)
    pj.hp = pj.max_hp
    inflict_damage(pj, 8, "bludgeoning")
    assert pj.hp == pj.max_hp - 8


def test_furia_bonus_de_dano_solo_con_fue():
    pj = _pj(level=1, abilities=_abilities(str=16))
    trait = _trait(pj, 1)
    trait.activate(round_=1)
    target = _pj(name="Dummy", level=1)
    atk_fue = Attack("Hacha", "1d12", ability="str")
    atk_des = Attack("Daga", "1d4", ability="dex")
    assert trait.extra_attack_damage(pj, target, "melee", atk=atk_fue) == 2
    assert trait.extra_attack_damage(pj, target, "melee", atk=atk_des) == 0
    trait.rage_active = False
    assert trait.extra_attack_damage(pj, target, "melee", atk=atk_fue) == 0


def test_furia_ventaja_en_pruebas_y_salvaciones_de_fue():
    pj = _pj(level=1, abilities=_abilities(str=16))
    trait = _trait(pj, 1)
    trait.activate(round_=1)
    rng = random.Random(7)
    res = ability_check(pj, "str", 30, rng)
    assert len(res.rolls) == 2
    assert res.mode == RollMode.ADVANTAGE
    sr = saving_throw(pj, "str", 30, rng)
    assert len(sr.rolls) == 2
    assert sr.mode == RollMode.ADVANTAGE
    # Otras características no se ven.
    res_dex = ability_check(pj, "dex", 30, rng)
    assert len(res_dex.rolls) == 1
    assert res_dex.mode == RollMode.NORMAL


# --- Duración y extensión ----------------------------------------------------

def test_furia_termina_si_no_se_extendio():
    pj = _pj(level=1)
    trait = _trait(pj, 1)
    trait.activate(round_=1)  # expira al fin de la ronda 2
    trait.on_turn_end(pj, _ctx(pj, round_=1))
    assert trait.rage_active is True
    trait.on_turn_end(pj, _ctx(pj, round_=2))
    assert trait.rage_active is False


def test_furia_se_extiende_sola_si_hubo_ataque():
    pj = _pj(level=1)
    trait = _trait(pj, 1)
    trait.activate(round_=1)
    pj.state.attacked_this_turn = True  # atacó en la ronda 2
    trait.on_turn_end(pj, _ctx(pj, round_=2))
    assert trait.rage_active is True
    assert trait.rage_expires_round == 3
    # Ronda 3 sin nada: termina.
    pj.state.attacked_this_turn = False
    trait.on_turn_end(pj, _ctx(pj, round_=3))
    assert trait.rage_active is False


def test_furia_se_extiende_sola_si_forzo_salvacion():
    pj = _pj(level=1)
    trait = _trait(pj, 1)
    trait.activate(round_=1)
    pj.state.forced_save_this_turn = True
    trait.on_turn_end(pj, _ctx(pj, round_=2))
    assert trait.rage_active is True
    assert trait.rage_expires_round == 3


def test_furia_termina_con_incapacitado():
    actor = SimpleNamespace(can_act=False, name="Thor",
                            state=SimpleNamespace(attacked_this_turn=False,
                                                  forced_save_this_turn=False))
    pj = _pj(level=1)
    trait = _trait(pj, 1)
    trait.rage_active = True
    trait.on_turn_start(actor)
    assert trait.rage_active is False


def test_furia_persistente_15_no_decae_ni_termina_por_incapacitado():
    pj = _pj(level=15)
    trait = _trait(pj, 15)
    trait.activate(round_=1)
    # Muy pasadas las 600 rondas sigue activa (hasta 10 minutos).
    trait.on_turn_end(pj, _ctx(pj, round_=500))
    assert trait.rage_active is True
    actor = SimpleNamespace(can_act=False, name="Thor", state=pj.state)
    trait.on_turn_start(actor)
    assert trait.rage_active is True  # Incapacitado ya no la termina
    trait.on_turn_start(pj)  # sin condiciones reales: sigue
    assert trait.rage_active is True


def test_furia_persistente_termina_con_unconscious():
    pj = _pj(level=15)
    trait = _trait(pj, 15)
    trait.rage_active = True

    class _Tracker:
        def has(self, cond):
            return str(getattr(cond, "value", cond)) == "unconscious"

    actor = SimpleNamespace(can_act=True, name="Thor", conditions=_Tracker(),
                            state=pj.state)
    trait.on_turn_start(actor)
    assert trait.rage_active is False


# --- Reckless Attack ---------------------------------------------------------

def test_reckless_da_ventaja_y_expone_al_bárbaro():
    pj = _pj(level=2, abilities=_abilities(str=16))
    trait = _trait(pj, 2)
    mods = AttackModifiers()
    trait.modify_attack_modifiers(mods, pj, _pj(), "melee",
                                  atk=Attack("Hacha", "1d12", ability="str"))
    assert mods.mode == RollMode.ADVANTAGE
    assert trait.reckless_active is True
    assert pj.grants_advantage_to_attackers is True
    # Al empezar su turno caduca.
    trait.on_turn_start(pj)
    assert trait.reckless_active is False
    assert pj.grants_advantage_to_attackers is False


# --- Danger Sense -----------------------------------------------------------

def test_danger_sense_da_ventaja_en_salvaciones_de_des():
    pj = _pj(level=2)
    trait = _trait(pj, 2)
    trait.rage_active = True
    mods = SaveModifiers()
    trait.modify_save_modifiers(mods, pj, "dex")
    assert "Sentido del Peligro" in mods.advantage_sources
    mods_str = SaveModifiers()
    trait.modify_save_modifiers(mods_str, pj, "str")
    assert "Furia" in mods_str.advantage_sources
    assert "Sentido del Peligro" not in mods_str.advantage_sources


def test_danger_sense_no_funciona_incapacitado():
    pj = _pj(level=2)
    trait = _trait(pj, 2)
    trait.rage_active = True

    class _Tracker:
        def has(self, cond):
            return str(getattr(cond, "value", cond)) == "incapacitated"

    target = SimpleNamespace(conditions=_Tracker())
    mods = SaveModifiers()
    trait.modify_save_modifiers(mods, target, "dex")
    assert "Sentido del Peligro" not in mods.advantage_sources


# --- Relentless Rage (11) ----------------------------------------------------

def _resultado(success: bool):
    return SimpleNamespace(success=success)


def test_relentless_rage_sube_pv_y_sube_el_cd(monkeypatch):
    pj = _pj(level=11)
    trait = _trait(pj, 11)
    trait.rage_active = True
    llamadas = []

    def _falsa_salvacion(*args, **kwargs):
        llamadas.append(args)
        return _resultado(True)

    monkeypatch.setattr(barb_mod, "saving_throw", _falsa_salvacion)
    hp = trait.on_reduced_to_zero_hp(pj, 80, ctx=_ctx(pj), rng=random.Random(1))
    assert hp == 22  # 2 × 11
    assert llamadas[0][2] == 10  # CD de la primera salvación
    hp2 = trait.on_reduced_to_zero_hp(pj, 80, ctx=_ctx(pj), rng=random.Random(1))
    assert hp2 == 22
    assert llamadas[1][2] == 15  # +5 por el uso anterior


def test_relentless_rage_fallo_y_sin_furia(monkeypatch):
    pj = _pj(level=11)
    trait = _trait(pj, 11)
    monkeypatch.setattr(barb_mod, "saving_throw", lambda *a, **k: _resultado(False))
    trait.rage_active = True
    assert trait.on_reduced_to_zero_hp(pj, 80, ctx=_ctx(pj),
                                       rng=random.Random(1)) is None
    trait.rage_active = False
    assert trait.on_reduced_to_zero_hp(pj, 80, ctx=_ctx(pj),
                                       rng=random.Random(1)) is None
    # Antes del nivel 11 no existe.
    trait2 = _trait(_pj(level=10), 10)
    trait2.rage_active = True
    assert trait2.on_reduced_to_zero_hp(pj, 80, rng=random.Random(1)) is None


# --- Brutal Strike (9) -------------------------------------------------------

def test_brutal_strike_renuncia_a_la_ventaja_y_paga_1d10():
    pj = _pj(level=9, abilities=_abilities(str=16))
    trait = _trait(pj, 9)
    atk = Attack("Hacha", "1d12", ability="str")
    mods = AttackModifiers()
    trait.modify_attack_modifiers(mods, pj, _pj(), "melee", atk=atk)
    # Renunció: sin ventaja (aunque sigue estando en modo NORMAL, sin desv).
    assert mods.advantage_sources == []
    assert mods.mode == RollMode.NORMAL
    assert trait.brutal_pending is True
    dmg = trait.extra_attack_damage(pj, _pj(), "melee", atk=atk,
                                    rng=random.Random(1))
    assert 1 <= dmg <= 10
    assert trait.brutal_pending is False
    # Una sola vez por turno.
    mods2 = AttackModifiers()
    trait.modify_attack_modifiers(mods2, pj, _pj(), "melee", atk=atk)
    assert len(mods2.advantage_sources) == 1
    assert trait.brutal_pending is False


def test_brutal_strike_2d10_desde_nivel_17():
    pj = _pj(level=17, abilities=_abilities(str=16))
    trait = _trait(pj, 17)
    atk = Attack("Hacha", "1d12", ability="str")
    mods = AttackModifiers()
    trait.modify_attack_modifiers(mods, pj, _pj(), "melee", atk=atk)
    dmg = trait.extra_attack_damage(pj, _pj(), "melee", atk=atk,
                                    rng=random.Random(1))
    assert 2 <= dmg <= 20


def test_brutal_strike_sin_fue_no_aplica():
    pj = _pj(level=9, abilities=_abilities(str=16, dex=16))
    trait = _trait(pj, 9)
    mods = AttackModifiers()
    trait.modify_attack_modifiers(mods, pj, _pj(), "melee",
                                  atk=Attack("Daga", "1d4", ability="dex"))
    assert mods.advantage_sources == []
    assert trait.brutal_pending is False
    # La ventaja del Reckless solo se aplica a FUE.
    assert trait.reckless_active is False


# --- Indomitable Might (18) ---------------------------------------------------

def test_indomitable_might_usa_el_valor_de_fue():
    pj = _pj(level=18, abilities=_abilities(str=20))
    trait = _trait(pj, 18)
    mods = SaveModifiers()
    trait.modify_save_modifiers(mods, pj, "str")
    assert mods.minimum_total == 20
    sr = saving_throw(pj, "str", 19, random.Random(1))
    assert sr.success is True
    assert sr.total >= 20
    # En tiradas de característica también.
    checks = CheckModifiers()
    trait.modify_check_modifiers(checks, pj, "str")
    assert checks.minimum_total == 20
    # Solo FUE.
    dex = SaveModifiers()
    trait.modify_save_modifiers(dex, pj, "dex")
    assert dex.minimum_total is None


# --- Primal Knowledge (3) -----------------------------------------------------

def test_primal_knowledge_tira_intimidacion_como_fue():
    pj = _pj(level=5, abilities=_abilities(str=16, cha=8))
    apply_barbarian(pj, skills=("intimidation",), level=5)
    trait = [t for t in pj.traits if isinstance(t, BarbarianFeatures)][0]
    rng = random.Random(3)
    # Sin Furia: carisma, sin ventaja.
    res = skill_check(pj, "intimidation", 30, rng)
    assert res.ability == "cha"
    assert res.mode == RollMode.NORMAL
    # Con Furia: se tira como FUE con ventaja (mod 3 + PB 3 = 6).
    trait.activate(round_=1)
    res_rage = skill_check(pj, "intimidation", 30, rng)
    assert res_rage.ability == "str"
    assert res_rage.mode == RollMode.ADVANTAGE
    assert res_rage.bonus == 6


def test_primal_knowledge_no_activa_sin_furia():
    pj = _pj(level=3, abilities=_abilities(str=16))
    apply_barbarian(pj, skills=("survival",), level=3)
    trait = [t for t in pj.traits if isinstance(t, BarbarianFeatures)][0]
    mods = CheckModifiers()
    trait.modify_check_modifiers(mods, pj, "wis", skill="survival")
    assert mods.ability_override is None
    trait.rage_active = True
    trait.modify_check_modifiers(mods, pj, "wis", skill="survival")
    assert mods.ability_override == "str"


# --- Reinicio -----------------------------------------------------------------

def test_reset_limpia_el_estado():
    pj = _pj(level=5)
    trait = apply_barbarian(pj)
    trait.activate(round_=1)
    trait.reckless_active = True
    trait.relentless_uses = 2
    pj.grants_advantage_to_attackers = True
    trait.reset()
    assert trait.rage_active is False
    assert trait.reckless_active is False
    assert trait.relentless_uses == 0
    assert pj.grants_advantage_to_attackers is False

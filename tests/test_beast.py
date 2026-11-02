"""Path of the Beast: forma, mordisco, garras, cola, alma bestial,
fiereza infecciosa y Call the Hunt (Tasha's sobre reglas 2024)."""
from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from dnd_sim import (Abilities, Attack, AttackRange, BarbarianFeatures,
                     BeastFeatures, FormOfTheBeast, Monster,
                     PlayerCharacter, apply_barbarian, apply_beast,
                     apply_class, apply_condition, load_monster,
                     run_combat, Condition)
from dnd_sim.engine.combat import attack as attack_mod
from dnd_sim.engine.combat import attack_roll
from dnd_sim.model.actions import AttackAction, TurnResources, WeaponAttackAction
from dnd_sim.rules.classes.barbarian import features as barb_mod
from dnd_sim.rules.classes.barbarian.subclasses import beast as beast_mod
from dnd_sim.rules.roll_modifiers import AttackModifiers


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=10, wis=10, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Thor", max_hp=300, ac=15, level=5, abilities=_abilities(),
        attacks=[Attack("Hacha de batalla", "1d12", ability="str")],
    )
    defaults.update(kwargs)
    return PlayerCharacter(**defaults)


def _monstruo(**kwargs) -> Monster:
    bonus = kwargs.pop("attack_bonus", None)
    defaults = dict(
        name="Orco", max_hp=10_000_000, ac=10,
        abilities=_abilities(str=14, dex=12, con=14, int=8, wis=8, cha=8),
        attacks=[Attack("Hacha orca", "1d6", ability="str", attack_bonus=30)],
    )
    defaults.update(kwargs)
    if bonus is not None:
        from dataclasses import replace
        defaults["attacks"] = [replace(a, attack_bonus=bonus)
                               for a in defaults["attacks"]]
    return Monster(**defaults)


def _beast(pj, level=None) -> BeastFeatures:
    lvl = level if level is not None else pj.level
    apply_barbarian(pj, level=lvl)
    return apply_beast(pj, level=lvl)


def _trait(pj) -> BeastFeatures:
    return next(t for t in pj.traits if isinstance(t, BeastFeatures))


def _barb(pj) -> BarbarianFeatures:
    return next(t for t in pj.traits if isinstance(t, BarbarianFeatures))


def _ctx(actor, combatants=None, round_=1, seed=0):
    return SimpleNamespace(
        actor=actor,
        combatants=[actor] if combatants is None else combatants,
        round=round_, rng=random.Random(seed), log=[],
        resources=TurnResources(), verbose=False,
    )


def _forma(pj, form: FormOfTheBeast) -> Attack:
    """Fuerza la forma (sin tirada) y devuelve su arma natural."""
    trait = _trait(pj)
    trait.form = form
    arma = trait.natural_attacks[form]
    pj.dynamic_weapons = [arma]
    return arma


def _en_furia(pj, round_=1, seed=0):
    """Activa la Furia y dispara la elección de forma; devuelve el ctx."""
    ctx = _ctx(pj, round_=round_, seed=seed)
    _barb(pj).activate(round_)
    _trait(pj).on_rage_start(pj, ctx)
    return ctx


def _espiar_attack_roll(monkeypatch):
    """Sustituye attack_roll por un espía que registra y delega.

    Hay que parchear DOS bindings: el módulo ``engine.combat.attack`` y el
    re-export del paquete ``engine.combat`` (los import perezosos de
    actions.py/beast.py resuelven por el paquete)."""
    llamadas = []
    original = attack_mod.attack_roll

    def spy(attacker, target, atk, rng, log=None, verbose=False, ctx=None,
            allow_friendly=False):
        llamadas.append((attacker, target, atk, allow_friendly))
        return original(attacker, target, atk, rng, log, verbose, ctx,
                        allow_friendly)

    monkeypatch.setattr(attack_mod, "attack_roll", spy)
    import dnd_sim.engine.combat as _combat_pkg
    monkeypatch.setattr(_combat_pkg, "attack_roll", spy)
    return llamadas


# --- Gating y aplicación -----------------------------------------------------

def test_apply_beast_sin_clase_da_value_error():
    with pytest.raises(ValueError, match="apply_barbarian"):
        apply_beast(_pj())


def test_apply_class_nivel_2_da_value_error():
    from dnd_sim import PlayerCharacter  # noqa: F811
    pj = _pj(level=2)
    with pytest.raises(ValueError, match="nivel >= 3"):
        apply_class(pj, "barbarian", "beast")


def test_antes_del_nivel_3_no_hay_forma():
    pj = _pj(level=2)
    _beast(pj, level=2)
    ctx = _en_furia(pj)
    assert _trait(pj).form is None
    assert pj.dynamic_weapons == []
    # ...pero con nivel 3 sí.
    pj2 = _pj(level=3)
    _beast(pj2, level=3)
    _en_furia(pj2)
    assert _trait(pj2).form is not None
    assert pj2.dynamic_weapons


def test_nivel_13_no_elige_aliados_de_caza():
    pj = _pj(level=13, abilities=_abilities(con=18))
    _beast(pj, level=13)
    otro = _pj(name="Aliado")
    ctx = _ctx(pj, [pj, otro])
    _barb(pj).activate(1)
    _trait(pj).on_rage_start(pj, ctx)
    assert _trait(pj).hunt_allies == []
    assert _trait(pj).hunt_uses == _trait(pj).hunt_uses_max


def test_nivel_9_no_usa_fiereza_infecciosa():
    pj = _pj(level=9)
    _beast(pj, level=9)
    arma = _forma(pj, FormOfTheBeast.CLAWS)
    _en_furia(pj)
    objetivo = _monstruo()
    trait = _trait(pj)
    antes = trait.infectious_uses
    trait.after_dealing_hit(objetivo, pj, AttackRange.MELEE, _ctx(pj),
                            arma, 7)
    assert trait.infectious_uses == antes  # gate de nivel 10


def test_aplica_crea_armas_y_accion_de_atacar():
    pj = _pj()
    trait = _beast(pj)
    assert set(trait.natural_attacks) == set(FormOfTheBeast)
    assert trait.infectious_uses == pj.proficiency  # PB por día
    assert any(isinstance(a, WeaponAttackAction) for a in pj.actions)
    assert pj.weapons  # los ataques del PJ pasan a weapons


# --- Forma de la Bestia ------------------------------------------------------

def test_forma_uniforme_un_tercio():
    pj = _pj()
    _beast(pj)
    trait = _trait(pj)
    _barb(pj).activate(1)
    ctx = _ctx(pj, seed=42)
    cuenta = {f: 0 for f in FormOfTheBeast}
    for _ in range(10_000):
        trait.on_rage_start(pj, ctx)
        cuenta[trait.form] += 1
    for n in cuenta.values():
        assert abs(n - 10_000 / 3) <= 300  # ±3 puntos porcentuales


def test_fuera_de_furia_no_hay_arma_natural():
    pj = _pj()
    _beast(pj)
    assert pj.dynamic_weapons == []
    assert _trait(pj).form is None


def test_al_terminar_la_furia_quita_forma_y_arma():
    pj = _pj()
    _beast(pj)
    ctx = _en_furia(pj)
    assert pj.dynamic_weapons
    _trait(pj).on_rage_end(pj, ctx)
    assert _trait(pj).form is None
    assert pj.dynamic_weapons == []


def test_reset_quita_la_forma():
    pj = _pj()
    _beast(pj)
    _en_furia(pj)
    _trait(pj).reset()
    assert _trait(pj).form is None
    assert pj.dynamic_weapons == []


def test_rage_action_dispara_la_eleccion_de_forma():
    pj = _pj()
    _beast(pj)
    ctx = _ctx(pj, seed=3)
    rage = next(a for a in pj.actions if a.name == "Entrar en Furia")
    rage.execute(ctx)
    assert _barb(pj).rage_active
    assert _trait(pj).form is not None
    assert pj.dynamic_weapons


def test_extend_rage_no_reelige_forma():
    pj = _pj()
    _beast(pj)
    ctx = _en_furia(pj, round_=1, seed=9)
    forma = _trait(pj).form
    arma = list(pj.dynamic_weapons)
    ext = next(a for a in pj.actions if a.name == "Mantener la Furia")
    ctx2 = _ctx(pj, round_=2, seed=10)
    ext.execute(ctx2)
    assert _trait(pj).form == forma
    assert pj.dynamic_weapons == arma


def test_furia_extendida_conserve_la_forma_y_expirando_la_pierde():
    pj = _pj()
    _beast(pj)
    ctx1 = _en_furia(pj, round_=1, seed=1)
    barb, trait = _barb(pj), _trait(pj)
    # Ronda 2 con ataque: se extiende sola; la forma sigue.
    pj.state.attacked_this_turn = True
    ctx2 = _ctx(pj, round_=2, seed=2)
    barb.on_turn_end(pj, ctx2)
    assert barb.rage_active and trait.form is not None
    # Ronda 3 sin nada: expira y la forma desaparece.
    pj.state.attacked_this_turn = False
    ctx3 = _ctx(pj, round_=3, seed=3)
    barb.on_turn_end(pj, ctx3)
    assert not barb.rage_active
    assert trait.form is None
    assert pj.dynamic_weapons == []
    # Nueva Furia: forma nueva elegida de nuevo.
    _barb(pj).activate(4)
    trait.on_rage_start(pj, ctx1)
    assert trait.form is not None


def test_reproibilidad_misma_seed_misma_forma():
    def forma_con_semilla(seed):
        pj = _pj()
        _beast(pj)
        _barb(pj).activate(1)
        ctx = _ctx(pj, seed=seed)
        _trait(pj).on_rage_start(pj, ctx)
        return _trait(pj).form
    assert forma_con_semilla(77) == forma_con_semilla(77)


def test_sin_subclase_no_hay_hooks_de_furia():
    pj = _pj()
    apply_barbarian(pj)
    from dnd_sim.rules.traits import hooks
    assert hooks(pj.traits, "on_rage_start") == []
    assert hooks(pj.traits, "on_rage_end") == []


# --- Mordisco ----------------------------------------------------------------

def test_mordisco_dano_y_curacion_bajo_mitad():
    pj = _pj()
    _beast(pj)
    ctx = _en_furia(pj)  # la Furia elige forma al azar...
    arma = _forma(pj, FormOfTheBeast.BITE)  # ...y este test la fija
    objetivo = _monstruo()
    trait = _trait(pj)
    pb = pj.proficiency
    # Exactamente la mitad (300/2): no cura.
    pj.hp = 150
    trait.after_dealing_hit(objetivo, pj, AttackRange.MELEE, ctx, arma, 5)
    assert pj.hp == 150 and trait.bite_heal_round == -1
    # Por debajo de la mitad: cura el bono de competencia...
    pj.hp = 149
    trait.after_dealing_hit(objetivo, pj, AttackRange.MELEE, ctx, arma, 5)
    assert pj.hp == 149 + pb
    # ...pero solo una vez por turno.
    pj.hp = 100
    trait.after_dealing_hit(objetivo, pj, AttackRange.MELEE, ctx, arma, 5)
    assert pj.hp == 100


def test_mordisco_no_cura_con_dano_cero():
    pj = _pj()
    _beast(pj)
    ctx = _en_furia(pj)
    arma = _forma(pj, FormOfTheBeast.BITE)
    trait = _trait(pj)
    pj.hp = 100
    trait.after_dealing_hit(_monstruo(), pj, AttackRange.MELEE, ctx, arma, 0)
    assert pj.hp == 100 and trait.bite_heal_round == -1
    # Con daño real en el mismo turno sí cura (el 0 no gastó el turno).
    trait.after_dealing_hit(_monstruo(), pj, AttackRange.MELEE, ctx, arma, 5)
    assert pj.hp == 100 + pj.proficiency


def test_mordisco_no_sobrepasa_el_maximo():
    pj = _pj()
    _beast(pj)
    ctx = _en_furia(pj)
    arma = _forma(pj, FormOfTheBeast.BITE)
    pj.max_hp, pj.hp = 4, 1  # 1*2 < 4: cura, y la cura toca el tope
    _trait(pj).after_dealing_hit(_monstruo(), pj, AttackRange.MELEE, ctx,
                                 arma, 5)
    assert pj.hp == 4


def test_mordisco_solo_con_furia():
    pj = _pj()
    _beast(pj)
    arma = _forma(pj, FormOfTheBeast.BITE)
    pj.hp = 100  # < mitad
    _trait(pj).after_dealing_hit(_monstruo(), pj, AttackRange.MELEE,
                                 _ctx(pj), arma, 5)
    assert pj.hp == 100  # sin Furia no cura


# --- Garras ------------------------------------------------------------------

def _pj_con_garras(**kwargs):
    pj = _pj(**kwargs)
    _beast(pj)
    garras = _forma(pj, FormOfTheBeast.CLAWS)
    pj.weapons = [garras]  # pool solo con garras: determinista
    return pj, garras


def test_garras_ataque_extra_una_vez_por_turno(monkeypatch):
    pj, garras = _pj_con_garras()
    _barb(pj).activate(1)  # el extra de garras exige Furia activa
    objetivo = _monstruo(ac=10)
    ctx = _ctx(pj, [pj, objetivo], round_=1, seed=5)
    llamadas = _espiar_attack_roll(monkeypatch)
    accion = next(a for a in pj.actions if isinstance(a, WeaponAttackAction))
    accion.execute(ctx)
    # 2 golpes (Extra Attack) + 1 extra de garras = 3, sin recursión.
    assert len(llamadas) == 3
    assert all(atk is garras for _, _, atk, _ in llamadas)
    # Turno siguiente: otro tanto, otra vez solo 3.
    ctx2 = _ctx(pj, [pj, objetivo], round_=2, seed=6)
    accion.execute(ctx2)
    assert len(llamadas) == 6


def test_garras_extra_tambien_si_la_tirada_falla(monkeypatch):
    pj, garras = _pj_con_garras()
    _barb(pj).activate(1)  # el extra de garras exige Furia activa
    objetivo = _monstruo(ac=99)  # nunca impacta
    ctx = _ctx(pj, [pj, objetivo], round_=1, seed=5)
    llamadas = _espiar_attack_roll(monkeypatch)
    accion = next(a for a in pj.actions if isinstance(a, WeaponAttackAction))
    accion.execute(ctx)
    assert len(llamadas) == 3


def test_garras_no_extra_con_accion_bonus(monkeypatch):
    pj, garras = _pj_con_garras()
    objetivo = _monstruo(ac=10)
    ctx = _ctx(pj, [pj, objetivo], round_=1, seed=5)
    llamadas = _espiar_attack_roll(monkeypatch)
    from dnd_sim.model.actions import ActionType
    bonus = AttackAction(attack=garras, action_type=ActionType.BONUS_ACTION)
    bonus.execute(ctx)
    assert len(llamadas) == 1  # sin ataque extra: no es la acción de Atacar


def test_garras_dano_cortante_con_furia(monkeypatch):
    pj, garras = _pj_con_garras()
    objetivo = _monstruo(ac=10)
    ctx = _ctx(pj, [pj, objetivo], round_=1, seed=5)
    _barb(pj).activate(1)
    dados = []
    original = attack_mod.roll_dice

    def dados_fijos(expr, rng, crit=False):
        dados.append(expr)
        return 4

    monkeypatch.setattr(attack_mod, "roll_dice", dados_fijos)
    attack_roll(pj, objetivo, garras, ctx.rng, None, ctx=ctx)
    # 4 de dados + FUE (3) + Furia (2): el arma natural recibe el daño de
    # Furia por el mismo camino que cualquier arma de FUE.
    assert objetivo.max_hp - objetivo.hp == 4 + 3 + 2
    assert garras.damage_type.value == "slashing"
    monkeypatch.setattr(attack_mod, "roll_dice", original)


def test_garras_no_extra_sin_furia(monkeypatch):
    pj, garras = _pj_con_garras()  # sin activar la Furia
    objetivo = _monstruo(ac=10)
    ctx = _ctx(pj, [pj, objetivo], round_=1, seed=5)
    llamadas = _espiar_attack_roll(monkeypatch)
    accion = next(a for a in pj.actions if isinstance(a, WeaponAttackAction))
    accion.execute(ctx)
    assert len(llamadas) == 2  # solo los dos golpes normales


# --- Cola --------------------------------------------------------------------

def _pj_con_cola(**kwargs):
    pj = _pj(**kwargs)
    _beast(pj)
    cola = _forma(pj, FormOfTheBeast.TAIL)
    _barb(pj).activate(1)
    return pj, cola


def test_cola_reacciona_gasta_y_sube_la_ca(monkeypatch):
    pj, _ = _pj_con_cola()
    enemigo = _monstruo()
    ctx = _ctx(pj, [pj, enemigo])
    vistos = []
    monkeypatch.setattr(beast_mod, "roll_dice",
                        lambda expr, rng, crit=False: (vistos.append(expr), 8)[1])
    bonus = _trait(pj).defensive_ac_bonus(
        pj, enemigo, AttackRange.MELEE, total=20, ca=15, ctx=ctx, rng=ctx.rng)
    assert bonus == 8 and vistos == ["1d8"]
    assert pj.state.reaction_used  # gasta la reacción
    # Una sola vez: ya no puede reaccionar.
    assert _trait(pj).defensive_ac_bonus(
        pj, enemigo, AttackRange.MELEE, total=20, ca=15, ctx=ctx,
        rng=ctx.rng) == 0


def test_cola_no_gasta_si_ni_con_8_compensa(monkeypatch):
    pj, _ = _pj_con_cola()
    ctx = _ctx(pj)
    monkeypatch.setattr(beast_mod, "roll_dice",
                        lambda *a, **k: (_ for _ in ()).throw(
                            AssertionError("no debe tirar")))
    bonus = _trait(pj).defensive_ac_bonus(
        pj, _monstruo(), AttackRange.MELEE, total=24, ca=15, ctx=ctx,
        rng=ctx.rng)
    assert bonus == 0
    assert not pj.state.reaction_used


def test_cola_no_reacciona_a_distancia_ni_incapacitada():
    pj, _ = _pj_con_cola()
    enemigo = _monstruo()
    ctx = _ctx(pj, [pj, enemigo])
    trait = _trait(pj)
    assert trait.defensive_ac_bonus(
        pj, enemigo, AttackRange.RANGED, total=20, ca=15, ctx=ctx,
        rng=ctx.rng) == 0  # la cola solo ante cuerpo a cuerpo
    apply_condition(pj, Condition.INCAPACITATED, ctx)
    pj.state.reaction_used = False
    assert trait.defensive_ac_bonus(
        pj, enemigo, AttackRange.MELEE, total=20, ca=15, ctx=ctx,
        rng=ctx.rng) == 0  # incapacitado no reacciona


def test_cola_no_se_pregunta_si_el_ataque_ya_fallaba(monkeypatch):
    pj, _ = _pj_con_cola()
    atacante = _monstruo(attack_bonus=-15)
    objetivo = _monstruo()  # sufre el ataque... aquí el que recibe es el PJ
    ctx = _ctx(atacante, [atacante, pj])
    tiradas = []
    monkeypatch.setattr(beast_mod, "roll_dice",
                        lambda expr, rng, crit=False: tiradas.append(expr) or 1)
    attack_roll(atacante, pj, atacante.attacks[0], ctx.rng, None, ctx=ctx)
    assert tiradas == []  # la cola no se activa ante un golpe que ya falla


def test_cola_baja_la_tasa_efectiva():
    # CA 17 contra +6: 50% en crudo (d20 >= 11).
    pj, _ = _pj_con_cola(ac=17)

    def simular(con_cola, semilla, n=5000):
        atacante = _monstruo(attacks=[
            Attack("Filo", "1d4", ability="str", attack_bonus=6)])
        diana = pj if con_cola else _pj(ac=17)
        ctx = SimpleNamespace(actor=atacante, combatants=[atacante, diana],
                              round=1, rng=random.Random(semilla), log=[],
                              resources=TurnResources(), verbose=False)
        hits = 0
        for _ in range(n):
            diana.hp = diana.max_hp  # la diana no debe morir a mitad del muestreo
            if con_cola:
                diana.state.reaction_used = False  # una reacción por turno
            hp_antes = diana.hp
            attack_roll(atacante, diana, atacante.attacks[0], ctx.rng, None,
                        ctx=ctx)
            if diana.hp < hp_antes:
                hits += 1
        return hits / n
    tasa_crudo = simular(con_cola=False, semilla=11)
    tasa_cola = simular(con_cola=True, semilla=11)
    assert abs(tasa_crudo - 0.5) <= 0.05  # línea base ~50%
    assert tasa_cola < tasa_crudo
    assert 0.15 <= tasa_cola <= 0.40  # coherente con +1d8 de CA


# --- Alma bestial ------------------------------------------------------------

def test_alma_bestial_flag_magical_existe():
    # El flag ``magical`` existe y por defecto es False: lo consume
    # Bestial Soul (nivel >= 6) y los tests de magical.py.
    assert Attack("Garras", "1d6").magical is False


# --- Fiereza infecciosa ------------------------------------------------------

def _pj_fiereza(**kwargs):
    kwargs.setdefault("level", 10)  # Fiereza infecciosa es de nivel 10
    pj = _pj(**kwargs)
    _beast(pj)
    arma = _forma(pj, FormOfTheBeast.CLAWS)
    _barb(pj).activate(1)
    trait = _trait(pj)
    trait.infectious_uses = 10 ** 9  # para los tests de muestreo
    return pj, arma


def test_fiereza_cd_y_uso_por_impacto(monkeypatch):
    pj, arma = _pj_fiereza()
    objetivo = _monstruo()
    ctx = _ctx(pj, [pj, objetivo])
    registros = []
    real = beast_mod.saving_throw

    def spy(target, ability, dc, rng, mode=None, *, kind=None):
        registros.append((ability, dc))
        return real(target, ability, dc, rng, mode, kind=kind)

    monkeypatch.setattr(beast_mod, "saving_throw", spy)
    trait = _trait(pj)
    trait.infectious_uses = trait.infectious_uses_max  # 4 (PB nivel 10)
    # CD = 8 + mod CON (3) + competencia (4) = 15, y un uso gastado.
    trait.after_dealing_hit(objetivo, pj, AttackRange.MELEE, ctx, arma, 7)
    assert registros == [("wis", 15)]
    assert trait.infectious_uses == trait.infectious_uses_max - 1
    # Se agota: ``max`` impactos y ya no tira más.
    while trait.infectious_uses > 0:
        trait.after_dealing_hit(objetivo, pj, AttackRange.MELEE, ctx, arma, 7)
    assert len(registros) == trait.infectious_uses_max
    trait.after_dealing_hit(objetivo, pj, AttackRange.MELEE, ctx, arma, 7)
    assert len(registros) == trait.infectious_uses_max


def test_fiereza_solo_en_furia_y_con_arma_natural():
    pj, arma = _pj_fiereza()
    objetivo = _monstruo()
    ctx = _ctx(pj, [pj, objetivo])
    trait = _trait(pj)
    trait.infectious_uses = 5
    _barb(pj).rage_active = False
    trait.after_dealing_hit(objetivo, pj, AttackRange.MELEE, ctx, arma, 7)
    assert trait.infectious_uses == 5  # sin Furia no gasta
    _barb(pj).rage_active = True
    trait.after_dealing_hit(objetivo, pj, AttackRange.MELEE, ctx,
                            _pj().attacks[0], 7)  # arma no natural
    assert trait.infectious_uses == 5


def test_fiereza_resistencia_legendaria_anula(monkeypatch):
    pj, arma = _pj_fiereza()
    objetivo = _monstruo()
    ctx = _ctx(pj, [pj, objetivo])
    monkeypatch.setattr(beast_mod, "saving_throw",
                        lambda *a, **k: SimpleNamespace(success=True))
    infringido = []
    monkeypatch.setattr(beast_mod, "inflict_damage",
                        lambda *a, **k: infringido.append(a))
    trait = _trait(pj)
    trait.infectious_uses = 5
    trait.after_dealing_hit(objetivo, pj, AttackRange.MELEE, ctx, arma, 7)
    assert infringido == []  # la salvación (p. ej. legendaria) lo anula
    assert trait.infectious_uses == 4  # el uso se gasta igualmente


def test_fiereza_psiquico_resistido_y_sin_duplicar_critico(monkeypatch):
    pj, arma = _pj_fiereza()
    objetivo = _monstruo(resistances={"psychic"})
    ctx = _ctx(pj, [pj, objetivo])
    monkeypatch.setattr(beast_mod, "saving_throw",
                        lambda *a, **k: SimpleNamespace(success=False))
    dados = []
    monkeypatch.setattr(beast_mod, "roll_dice",
                        lambda expr, rng, crit=False: (dados.append((expr, crit)), 12)[1])
    trait = _trait(pj)
    hp_antes = objetivo.hp
    trait.after_dealing_hit(objetivo, pj, AttackRange.MELEE, ctx, arma, 7)
    # 12 de dados (nunca críticos) -> resistencia psíquica -> 6.
    assert dados == [("2d12", False)]
    assert objetivo.hp == hp_antes - 6


def test_fiereza_efectos_uniformes_con_aliado(monkeypatch):
    pj, arma = _pj_fiereza()
    victima = _monstruo()
    aliado_victima = _monstruo(name="Aliado del orco")
    ctx = _ctx(pj, [pj, victima, aliado_victima])
    monkeypatch.setattr(beast_mod, "saving_throw",
                        lambda *a, **k: SimpleNamespace(success=False))
    n_dano = [0]
    infr = beast_mod.inflict_damage

    def cuenta_dano(*a, **k):
        n_dano[0] += 1
        return infr(*a, **k)

    monkeypatch.setattr(beast_mod, "inflict_damage", cuenta_dano)
    llamadas = _espiar_attack_roll(monkeypatch)
    trait = _trait(pj)
    for i in range(10_000):
        victima.state.reaction_used = False
        trait.after_dealing_hit(victima, pj, AttackRange.MELEE, ctx, arma, 7)
    n_reaccion = sum(1 for *_ , friendly in llamadas if friendly)
    assert n_dano[0] + n_reaccion == 10_000
    assert abs(n_dano[0] - 5000) <= 300
    assert abs(n_reaccion - 5000) <= 300


def test_fiereza_sin_aliados_o_sin_reaccion_siempre_dano(monkeypatch):
    pj, arma = _pj_fiereza()
    monkeypatch.setattr(beast_mod, "saving_throw",
                        lambda *a, **k: SimpleNamespace(success=False))
    infr = beast_mod.inflict_damage
    cont = [0]

    def cuenta(*a, **k):
        cont[0] += 1
        return infr(*a, **k)

    monkeypatch.setattr(beast_mod, "inflict_damage", cuenta)
    llamadas = _espiar_attack_roll(monkeypatch)
    trait = _trait(pj)
    # Sin aliados de la víctima:
    victima = _monstruo()
    ctx = _ctx(pj, [pj, victima])
    for _ in range(50):
        victima.state.reaction_used = False
        trait.after_dealing_hit(victima, pj, AttackRange.MELEE, ctx, arma, 7)
    # Con reacción ya gastada:
    aliado = _monstruo(name="Aliado")
    ctx2 = _ctx(pj, [pj, victima, aliado])
    victima.state.reaction_used = True
    for _ in range(50):
        trait.after_dealing_hit(victima, pj, AttackRange.MELEE, ctx2, arma, 7)
    assert cont[0] == 100  # siempre daño
    assert not any(friendly for *_ , friendly in llamadas)


def test_fiereza_victima_contraataca_a_un_aliado_suyo(monkeypatch):
    pj, arma = _pj_fiereza()
    victima = _monstruo()
    aliado = _monstruo(name="Aliado del orco")
    ctx = _ctx(pj, [pj, victima, aliado])
    monkeypatch.setattr(beast_mod, "saving_throw",
                        lambda *a, **k: SimpleNamespace(success=False))
    # Fuerza la rama (b): pick devuelve la última opción.
    monkeypatch.setattr(beast_mod, "pick", lambda rng, options: options[-1])
    llamadas = _espiar_attack_roll(monkeypatch)
    _trait(pj).after_dealing_hit(victima, pj, AttackRange.MELEE, ctx, arma, 7)
    assert len(llamadas) == 1
    atacante, golpeado, _, friendly = llamadas[0]
    assert atacante is victima and golpeado is aliado and friendly
    assert victima.state.reaction_used  # gasta SU reacción


def test_fuego_amigo_sigue_protegido():
    """Sin la excepción explícita, atacar al propio bando sigue fallando."""
    a, b = _pj(name="A"), _pj(name="B")
    ctx = _ctx(a, [a, b])
    with pytest.raises(ValueError, match="fuego amigo"):
        attack_roll(a, b, a.attacks[0], ctx.rng, None, ctx=ctx)


# --- Call the Hunt -----------------------------------------------------------

def test_call_the_hunt_k_temporales_y_no_apilar():
    pj = _pj(level=14, abilities=_abilities(con=16))  # mod 3
    _beast(pj, level=14)
    aliados = [_pj(name="A1"), _pj(name="A2")]
    ctx = _ctx(pj, [pj, *aliados])
    _barb(pj).activate(1)
    trait = _trait(pj)
    trait.on_rage_start(pj, ctx)
    k = min(3, len(aliados))
    assert len(trait.hunt_allies) == k
    assert pj.temp_hp == 5 * k == 10
    assert trait.hunt_uses == trait.hunt_uses_max - 1
    # No apila con temporales mayores ya presentes.
    pj.temp_hp = 15
    trait.on_rage_end(pj, ctx)
    trait.reset()
    pj.temp_hp = 15
    trait.hunt_uses = trait.hunt_uses_max
    trait.on_rage_start(pj, ctx)
    assert pj.temp_hp == 15  # no suma: 10 < 15


def test_call_the_hunt_sin_aliados_no_gasta_el_uso():
    pj = _pj(level=14)
    _beast(pj, level=14)
    ctx = _ctx(pj)  # solo el bárbaro
    _barb(pj).activate(1)
    trait = _trait(pj)
    trait.on_rage_start(pj, ctx)
    assert trait.hunt_uses == trait.hunt_uses_max
    assert pj.temp_hp == 0


def test_call_the_hunt_bonus_una_vez_por_turno(monkeypatch):
    pj = _pj(level=14, abilities=_abilities(con=16))
    _beast(pj, level=14)
    aliado = _pj(name="A1")
    ctx = _ctx(pj, [pj, aliado])
    _barb(pj).activate(1)
    trait = _trait(pj)
    trait.on_rage_start(pj, ctx)
    bonus = next(t for t in aliado.traits if t.__class__.__name__ == "CallTheHuntBonus")
    monkeypatch.setattr(beast_mod, "roll_dice",
                        lambda expr, rng, crit=False: 6)
    objetivo = _monstruo()
    assert bonus.extra_attack_damage(aliado, objetivo, AttackRange.MELEE,
                                     False, ctx, ctx.rng) == 6
    # Una sola vez por turno del aliado.
    assert bonus.extra_attack_damage(aliado, objetivo, AttackRange.MELEE,
                                     False, ctx, ctx.rng) == 0
    # Turno siguiente (otra ronda): otra vez.
    ctx2 = _ctx(pj, [pj, aliado], round_=2)
    assert bonus.extra_attack_damage(aliado, objetivo, AttackRange.MELEE,
                                     False, ctx2, ctx2.rng) == 6
    # Sin Furia no da nada (y el rasgo ya se retira al terminar).
    _barb(pj).rage_active = False
    assert bonus.extra_attack_damage(aliado, objetivo, AttackRange.MELEE,
                                     False, ctx2, ctx2.rng) == 0


def test_call_the_hunt_termina_con_la_furia_y_en_reset():
    pj = _pj(level=14, abilities=_abilities(con=16))
    _beast(pj, level=14)
    aliado = _pj(name="A1")
    ctx = _ctx(pj, [pj, aliado])
    _barb(pj).activate(1)
    trait = _trait(pj)
    trait.on_rage_start(pj, ctx)
    assert any(t.__class__.__name__ == "CallTheHuntBonus"
               for t in aliado.traits)
    trait.on_rage_end(pj, ctx)
    assert not any(t.__class__.__name__ == "CallTheHuntBonus"
                   for t in aliado.traits)
    assert pj.temp_hp == 0
    # reset(): usos restaurados y bonus retirados si quedara alguno.
    trait.on_rage_start(pj, ctx)  # vuelve a elegir aliado
    trait.reset()
    assert trait.hunt_uses == trait.hunt_uses_max
    assert not any(t.__class__.__name__ == "CallTheHuntBonus"
                   for t in aliado.traits)


def test_call_the_hunt_no_se_apila():
    pj = _pj(level=14, abilities=_abilities(con=16))
    _beast(pj, level=14)
    aliado = _pj(name="A1")
    ctx = _ctx(pj, [pj, aliado])
    trait = _trait(pj)
    _barb(pj).activate(1)
    trait.on_rage_start(pj, ctx)
    trait.hunt_uses = 1  # allow a second call
    trait.on_rage_start(pj, ctx)  # sin limpiar (a mano): no debe duplicar
    bonuses = [t for t in aliado.traits
               if t.__class__.__name__ == "CallTheHuntBonus"]
    assert len(bonuses) == 1


def test_call_the_hunt_reparto_uniforme():
    pj = _pj(level=14, abilities=_abilities(con=12))  # mod 1 -> k=1
    _beast(pj, level=14)
    aliados = [_pj(name="A1"), _pj(name="A2")]
    ctx = _ctx(pj, [pj, *aliados], seed=99)
    barb, trait = _barb(pj), _trait(pj)
    cuenta = {"A1": 0, "A2": 0}
    for _ in range(10_000):
        trait.reset()
        barb.activate(1)
        trait.on_rage_start(pj, ctx)
        cuenta[trait.hunt_allies[0].name] += 1
    assert abs(cuenta["A1"] - 5000) <= 300
    assert abs(cuenta["A2"] - 5000) <= 300


def test_call_the_hunt_ordern_de_rng_forma_luego_aliados(monkeypatch):
    orden = []
    real_pick, real_sample = beast_mod.pick, beast_mod.sample

    def pick_spy(rng, options):
        orden.append("pick")
        return real_pick(rng, options)

    def sample_spy(rng, options, k):
        orden.append("sample")
        return real_sample(rng, options, k)

    monkeypatch.setattr(beast_mod, "pick", pick_spy)
    monkeypatch.setattr(beast_mod, "sample", sample_spy)
    pj = _pj(level=14, abilities=_abilities(con=16))
    _beast(pj, level=14)
    aliado = _pj(name="A1")
    ctx = _ctx(pj, [pj, aliado], seed=1)
    _barb(pj).activate(1)
    _trait(pj).on_rage_start(pj, ctx)
    assert orden[0] == "pick"       # forma
    assert orden[1] == "sample"     # aliados de Call the Hunt


# --- Interacción con el base y salidas ---------------------------------------

def test_ataque_natural_recibe_brutal_strike_como_cualquier_arma():
    pj = _pj()
    _beast(pj, level=9)  # Brutal Strike desde el 9
    garras = _forma(pj, FormOfTheBeast.CLAWS)
    _en_furia(pj)
    objetivo = _monstruo()
    ctx = _ctx(pj, [pj, objetivo])
    barb = _barb(pj)
    barb.reckless_probability = 1.0  # decisión forzada (sin azar)
    mods = AttackModifiers()
    barb.modify_attack_modifiers(mods, pj, objetivo, AttackRange.MELEE,
                                 ctx, ctx.rng, atk=garras)
    # Renuncia a la ventaja del Temerario -> Brutal pendiente, como con un
    # arma normal; el extra de daño se paga después por la vía genérica.
    assert barb.brutal_pending
    assert "Ataque Temerario" not in mods.advantage_sources
    assert barb.extra_attack_damage(
        pj, objetivo, AttackRange.MELEE, False, ctx, ctx.rng, atk=garras
    ) >= 0
    assert not barb.brutal_pending  # pagado y limpiado


def test_brutal_strike_da_el_d10_en_arma_natural(monkeypatch):
    pj = _pj()
    _beast(pj, level=9)
    garras = _forma(pj, FormOfTheBeast.CLAWS)
    _en_furia(pj)
    objetivo = _monstruo()
    ctx = _ctx(pj, [pj, objetivo])
    barb = _barb(pj)
    # El roll del Brutal vive en features.py (barb_mod), no en beast.py.
    monkeypatch.setattr(barb_mod, "roll_dice",
                        lambda expr, rng, crit=False: 7)
    # Fuerza el pendiente brutal (como en los tests del bárbaro base).
    barb.brutal_pending = True
    extra = barb.extra_attack_damage(pj, objetivo, AttackRange.MELEE, False,
                                     ctx, ctx.rng, atk=garras)
    # Daño de Furia (3 en nivel 9) + Brutal (7): vía el hook genérico.
    assert extra == 3 + 7


def test_integracion_un_pj_beast_contra_monstruo():
    pj = _pj()
    _beast(pj)
    mono = load_monster("gladiator")
    res = run_combat([pj, mono], random.Random(3), verbose=True, max_rounds=10)
    assert res.rounds >= 1
    assert isinstance(res.log, list)


def test_integracion_grupo_de_tres_pjs():
    beast_pj = _pj(name="Beast")
    _beast(beast_pj)
    party = [beast_pj, _pj(name="Mago"), _pj(name="Pícara")]
    mono = load_monster("gladiator")
    res = run_combat([*party, mono], random.Random(7), max_rounds=15)
    assert res.rounds >= 1
    assert isinstance(res.log, list)


def test_plantilla_barbaro_con_beast(monkeypatch):
    import main
    # PARTY_TEMPLATES es una lista: se reemplaza la entrada con setattr.
    plantillas = list(main.PARTY_TEMPLATES)
    plantilla = dict(plantillas[4])
    assert plantilla["class_name"] == "barbarian"
    plantilla["subclass_name"] = "beast"
    plantillas[4] = plantilla
    monkeypatch.setattr(main, "PARTY_TEMPLATES", plantillas)
    pj = main._build_party(5)[4]
    assert any(isinstance(t, BeastFeatures) for t in pj.traits)

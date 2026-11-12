"""Tests de tablas y registro de Psi Warrior (Guerrero Psiónico, PHB 2024).

Las tablas viven en A1; el registro y ``apply_psi_warrior`` en A2;
Psionic Strike en A3; Telekinetic Thrust en A4; Protective Field en A5;
Guarded Mind en A6; Bulwark of Force en A7 y Telekinetic Master en A8.
Los rasgos sin modelo (Telekinetic Movement, Psi-Powered Leap, empuje
de 10 ft, distancias de 30 ft) se congelan como dato sin efecto.
"""

from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from dnd_sim import Abilities, Attack, Monster, PlayerCharacter, apply_class
from dnd_sim.core.classes import (
    bulwark_targets,
    psionic_dice_count,
    psionic_die_sides,
)
from dnd_sim.core.dice import D20Result, RollMode
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import (
    PsiWarriorFeatures,
    apply_psi_warrior,
)
from dnd_sim.rules.conditions import Condition, apply_condition
from dnd_sim.rules.saves import SaveResult


# --- A1: tablas --------------------------------------------------------------


def test_los_dados_psionicos_son_doble_del_bonificador_de_competencia():
    assert psionic_dice_count(1) == 0
    assert psionic_dice_count(2) == 0
    assert psionic_dice_count(3) == 4
    assert psionic_dice_count(4) == 4
    assert psionic_dice_count(5) == 6
    assert psionic_dice_count(8) == 6
    assert psionic_dice_count(9) == 8
    assert psionic_dice_count(12) == 8
    assert psionic_dice_count(13) == 10
    assert psionic_dice_count(16) == 10
    assert psionic_dice_count(17) == 12
    assert psionic_dice_count(20) == 12


def test_el_tamano_del_dado_psionico_es_d6_d8_d10_o_d12_segun_el_nivel():
    assert psionic_die_sides(1) == 6
    assert psionic_die_sides(4) == 6
    assert psionic_die_sides(5) == 8
    assert psionic_die_sides(10) == 8
    assert psionic_die_sides(11) == 10
    assert psionic_die_sides(16) == 10
    assert psionic_die_sides(17) == 12
    assert psionic_die_sides(20) == 12


def test_bulwark_targets_es_el_mod_de_int_con_minimo_uno():
    assert bulwark_targets(5) == 5
    assert bulwark_targets(3) == 3
    assert bulwark_targets(1) == 1
    assert bulwark_targets(0) == 1
    assert bulwark_targets(-2) == 1


# --- A2: esqueleto, registro y datos sin efecto ------------------------------


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=14, wis=12, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Camila", max_hp=70, ac=15, level=5, abilities=_abilities(),
        attacks=[Attack("Espada larga", "1d8", ability="str")],
    )
    defaults.update(kwargs)
    return PlayerCharacter(**defaults)


def _trait(pj) -> PsiWarriorFeatures:
    for trait in pj.traits:
        if isinstance(trait, PsiWarriorFeatures):
            return trait
    raise AssertionError("falta PsiWarriorFeatures")


def _psi(level: int = 5, fighting_style: str | None = None,
         **kwargs) -> tuple:
    pj = _pj(level=level)
    apply_fighter(pj, level=level, fighting_style=fighting_style)
    trait = apply_psi_warrior(pj, level=level, **kwargs)
    return pj, trait


def _firmas(pj) -> tuple:
    """(rasgos, acciones, salvaciones, habilidades, CA) para comparar."""
    return (
        [type(t).__name__ for t in pj.traits],
        [type(a).__name__ for a in pj.actions],
        set(pj.save_proficiencies),
        set(pj.skill_proficiencies),
        pj.ac,
    )


def test_registro_psi_warrior_bajo_fighter():
    subclases = CLASSES["fighter"].subclasses
    assert "psi_warrior" in subclases
    sub = subclases["psi_warrior"]
    assert sub.class_name == "fighter"
    assert sub.min_level == 3


def test_apply_class_equivalente_a_apply_psi_warrior(monkeypatch):
    """Misma semilla en el RNG de creación: resultados idénticos."""
    import dnd_sim.rules.classes.fighter.features as fighter_mod

    a, b = _pj(), _pj()
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    apply_class(a, "fighter", "psi_warrior", level=5)
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    apply_fighter(b)
    apply_psi_warrior(b, level=5)
    assert _firmas(a) == _firmas(b)
    assert isinstance(_trait(a), PsiWarriorFeatures)
    assert isinstance(_trait(b), PsiWarriorFeatures)


def test_apply_psi_warrior_sin_clase_guerrero_da_value_error():
    with pytest.raises(ValueError, match="Primero aplica la clase guerrero"):
        apply_psi_warrior(_pj(), level=5)


def test_apply_psi_warrior_por_debajo_del_nivel_3_da_value_error():
    with pytest.raises(ValueError, match=">= 3"):
        apply_class(_pj(level=2), "fighter", "psi_warrior")


def test_los_dados_y_el_tamano_segun_el_nivel_se_rellenan_al_aplicar():
    pj3, t3 = _psi(level=3)
    assert (t3.dados_restantes, t3.dados_lados) == (4, 6)
    pj5, t5 = _psi(level=5)
    assert (t5.dados_restantes, t5.dados_lados) == (6, 8)
    pj11, t11 = _psi(level=11)
    assert (t11.dados_restantes, t11.dados_lados) == (8, 10)
    pj17, t17 = _psi(level=17)
    assert (t17.dados_restantes, t17.dados_lados) == (12, 12)


def test_reset_rellena_la_reserva_completa():
    pj, trait = _psi(level=5)
    trait.dados_restantes = 0
    trait.psionic_strike_used_this_turn = True
    trait.bulwark_uso_gratuito = False
    trait.telekinetic_master_uso_gratuito = False
    trait.bulwark_activo = True
    trait.telekinetic_master_activo = True
    trait.reset()
    assert trait.dados_restantes == psionic_dice_count(5)
    assert trait.psionic_strike_used_this_turn is False
    assert trait.bulwark_uso_gratuito is True
    assert trait.telekinetic_master_uso_gratuito is True
    assert trait.bulwark_activo is False
    assert trait.telekinetic_master_activo is False


def test_telekinetic_movement_y_psi_powered_leap_son_dato_sin_efecto():
    """Sin movimiento ni vuelo en el modelo: ni dados ni RNG."""
    pj, trait = _psi(level=7)
    assert trait.telekinetic_movement is True
    assert trait.psi_powered_leap is True
    # Sin gastar dados ni cambiar la ficha al aplicarlos.
    assert trait.dados_restantes == psionic_dice_count(7)
    assert not hasattr(pj, "speed")


def test_sin_subclase_no_hay_rasgo_ni_datos_de_psi_warrior():
    pj = _pj()
    apply_fighter(pj, level=5, fighting_style="Archery")
    assert not any(isinstance(t, PsiWarriorFeatures) for t in pj.traits)
    # Cero consulta: sin el rasgo nadie tiene la reserva de dados.
    assert not any(hasattr(t, "dados_restantes") for t in pj.traits)


# --- A3: Psionic Strike -------------------------------------------------------


def _bajo_golpe(**kwargs) -> tuple:
    """PJ Psi Warrior + enemigo y ctx de combate, para el walker del motor."""
    # Archery fijo: el estilo se elige con el RNG global de creación y
    # Dueling añadiría +2 al daño esperado.
    kwargs.setdefault("fighting_style", "Archery")
    pj, trait = _psi(**kwargs)
    enemigo = Monster("Orco", max_hp=60, ac=10, abilities=_abilities())
    ctx = SimpleNamespace(round=1, actor=pj, rng=random.Random(1),
                           combatants=[pj, enemigo], log=[])
    return pj, trait, enemigo, ctx


def _parchea_golpe(monkeypatch, *, valor_d20: int = 20, dado_arma: int = 5,
                   dado_psi: int = 4) -> list:
    """d20 fijo + daño del arma fijo + pick «sí» y dado psi fijo."""
    import dnd_sim.engine.combat.attack as atk_mod
    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    tiradas: list[str] = []
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode=None: D20Result(
            value=valor_d20, rolls=[valor_d20],
            mode=mode or RollMode.NORMAL))
    monkeypatch.setattr(atk_mod, "roll_dice",
                        lambda expr, rng, crit=False: dado_arma)
    monkeypatch.setattr(psi_mod, "pick",
                        lambda rng, seq: (tiradas.append(tuple(seq)),
                                          seq[-1])[1])
    monkeypatch.setattr(psi_mod, "roll_dice",
                        lambda expr, rng, crit=False: dado_psi)
    return tiradas


def _ataca(pj, enemigo, ctx, *, spell: bool = False):
    import dnd_sim.engine.combat.attack as atk_mod

    atk = Attack("Golpe", "1d6", ability="str", spell_attack=spell)
    atk_mod.attack_roll(pj, enemigo, atk, random.Random(1), log=ctx.log,
                        ctx=ctx)


def test_el_psionic_strike_suma_el_dado_mas_el_mod_de_int_como_fuerza(
        monkeypatch):
    _parchea_golpe(monkeypatch, dado_arma=5, dado_psi=4)
    pj, trait, enemigo, ctx = _bajo_golpe()
    _ataca(pj, enemigo, ctx)
    # Arma: 5 del dado + 3 de mod FUE. Fuerza: 4 del dado + 2 de mod INT.
    assert enemigo.hp == 60 - (5 + 3) - (4 + 2)
    assert trait.dados_restantes == psionic_dice_count(5) - 1
    assert any("Psionic Strike" in line for line in ctx.log)


def test_el_psionic_strike_gasta_un_solo_dado_por_turno(monkeypatch):
    _parchea_golpe(monkeypatch)
    pj, trait, enemigo, ctx = _bajo_golpe()
    _ataca(pj, enemigo, ctx)
    _ataca(pj, enemigo, ctx)  # mismo turno: el flag lo bloquea
    assert trait.psionic_strike_used_this_turn is True
    assert trait.dados_restantes == psionic_dice_count(5) - 1
    assert sum("Psionic Strike" in line for line in ctx.log) == 1


def test_el_psionic_strike_no_se_activa_en_ataques_de_hechizo(monkeypatch):
    tiradas = _parchea_golpe(monkeypatch)
    pj, trait, enemigo, ctx = _bajo_golpe()
    _ataca(pj, enemigo, ctx, spell=True)
    assert tiradas == []  # ni siquiera el pick se consulta
    assert trait.dados_restantes == psionic_dice_count(5)
    assert enemigo.hp == 60 - (5 + 3)  # solo el daño del arma


def test_el_psionic_strike_no_se_activa_si_el_golpe_no_causo_dano(
        monkeypatch):
    tiradas = _parchea_golpe(monkeypatch)
    pj, trait, enemigo, ctx = _bajo_golpe()
    import dnd_sim.engine.combat.attack as atk_mod

    # Daño principal 0 (p. ej. inmunidad): el walker no procede.
    monkeypatch.setattr(atk_mod, "apply_damage_modifiers",
                        lambda *args, **kwargs: 0)
    _ataca(pj, enemigo, ctx)
    assert tiradas == []
    assert trait.dados_restantes == psionic_dice_count(5)
    assert enemigo.hp == 60


def test_sin_dados_restantes_no_hay_pick_ni_rng(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    def _revienta(rng, seq):
        raise AssertionError("sin dados no se consulta el pick")

    pj, trait, enemigo, ctx = _bajo_golpe()
    trait.dados_restantes = 0
    monkeypatch.setattr(psi_mod, "pick", _revienta)
    _ataca(pj, enemigo, ctx)
    assert enemigo.hp == 60 - (5 + 3)  # solo el daño del arma


def test_el_flag_de_psionic_strike_se_reinicia_cada_turno(monkeypatch):
    _parchea_golpe(monkeypatch)
    pj, trait, enemigo, ctx = _bajo_golpe()
    _ataca(pj, enemigo, ctx)
    trait.on_turn_start(pj, ctx)
    assert trait.psionic_strike_used_this_turn is False
    _ataca(pj, enemigo, ctx)
    assert trait.dados_restantes == psionic_dice_count(5) - 2
    assert sum("Psionic Strike" in line for line in ctx.log) == 2


def test_la_resistencia_a_fuerza_del_objetivo_mitiga_el_psionic_strike(
        monkeypatch):
    _parchea_golpe(monkeypatch, dado_arma=5, dado_psi=4)
    pj, trait, enemigo, ctx = _bajo_golpe()
    enemigo.resistances = {"force"}
    _ataca(pj, enemigo, ctx)
    # Fuerza: 4+2 = 6 con resistencia → 3; el daño del arma no se toca.
    assert enemigo.hp == 60 - (5 + 3) - 3


def test_el_dado_del_psionic_strike_sigue_la_regla_de_criticos_del_motor(
        monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    criticos: list[bool] = []
    _parchea_golpe(monkeypatch, valor_d20=20)
    monkeypatch.setattr(
        psi_mod, "roll_dice",
        lambda expr, rng, crit=False: (criticos.append(crit), 4)[1])
    pj, trait, enemigo, ctx = _bajo_golpe()
    _ataca(pj, enemigo, ctx)
    assert criticos == [True]


def test_sin_subclase_el_walker_del_motor_no_consulta_ni_tira_rng(monkeypatch):
    import dnd_sim.engine.combat.attack as atk_mod
    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    def _revienta(rng, seq):
        raise AssertionError("sin la subclase no hay decisiones")

    _parchea_golpe(monkeypatch)
    monkeypatch.setattr(psi_mod, "pick", _revienta)
    pj = _pj()
    apply_fighter(pj, level=5, fighting_style="Archery")
    enemigo = Monster("Orco", max_hp=60, ac=10, abilities=_abilities())
    ctx = SimpleNamespace(round=1, actor=pj, rng=random.Random(1),
                           combatants=[pj, enemigo], log=[])
    atk = Attack("Golpe", "1d6", ability="str")
    atk_mod.attack_roll(pj, enemigo, atk, random.Random(1), log=ctx.log,
                        ctx=ctx)
    assert enemigo.hp == 60 - (5 + 3)
    assert not any("Psionic Strike" in line for line in ctx.log)


# --- A4: Telekinetic Thrust ---------------------------------------------------


def _salvacion(monkeypatch, llamadas: list, *, pasa: bool) -> None:
    """saving_throw parcheado en el módulo consumidor (psi_warrior)."""
    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    def _fake(target, ability, dc, rng, mode=None, **kwargs):
        llamadas.append((ability, dc))
        return SaveResult(ability=ability, dc=dc, rolls=[1], bonus=0,
                          total=1, success=pasa,
                          mode=mode or RollMode.NORMAL)

    monkeypatch.setattr(psi_mod, "saving_throw", _fake)


def test_el_telekinetic_thrust_pide_salvacion_de_fue_con_cd_8_mas_pb_mas_int(
        monkeypatch):
    llamadas: list = []
    _parchea_golpe(monkeypatch)
    _salvacion(monkeypatch, llamadas, pasa=False)
    pj, trait, enemigo, ctx = _bajo_golpe(level=7)
    _ataca(pj, enemigo, ctx)
    assert llamadas == [("str", 8 + pj.proficiency + 2)]  # mod INT = +2
    assert enemigo.conditions.has(Condition.PRONE)
    assert any("Telekinetic Thrust" in line for line in ctx.log)


def test_el_telekinetic_thrust_no_derriba_si_la_salvacion_pasa(monkeypatch):
    llamadas: list = []
    _parchea_golpe(monkeypatch)
    _salvacion(monkeypatch, llamadas, pasa=True)
    pj, trait, enemigo, ctx = _bajo_golpe(level=7)
    _ataca(pj, enemigo, ctx)
    assert len(llamadas) == 1
    assert not enemigo.conditions.has(Condition.PRONE)


def test_el_telekinetic_thrust_no_actua_por_debajo_del_nivel_siete(
        monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    def _revienta(*args, **kwargs):
        raise AssertionError("nivel < 7 no pide salvación")

    _parchea_golpe(monkeypatch)
    monkeypatch.setattr(psi_mod, "saving_throw", _revienta)
    pj, trait, enemigo, ctx = _bajo_golpe(level=5)
    _ataca(pj, enemigo, ctx)
    # Psionic Strike sí gasta el dado, pero Thrust no entra.
    assert trait.dados_restantes == psionic_dice_count(5) - 1
    assert not enemigo.conditions.has(Condition.PRONE)


def test_el_telekinetic_thrust_no_se_aplica_si_no_se_gasta_el_dado(
        monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    def _revienta(*args, **kwargs):
        raise AssertionError("sin gasto no hay salvación")

    _parchea_golpe(monkeypatch)
    monkeypatch.setattr(psi_mod, "pick", lambda rng, seq: "no")
    monkeypatch.setattr(psi_mod, "saving_throw", _revienta)
    pj, trait, enemigo, ctx = _bajo_golpe(level=7)
    _ataca(pj, enemigo, ctx)
    assert trait.dados_restantes == psionic_dice_count(7)
    assert not enemigo.conditions.has(Condition.PRONE)


# --- A5: Protective Field -----------------------------------------------------


def _parchea_campo(monkeypatch, *, dado: int = 4,
                   decide: str = "si") -> list:
    """pick y dado de Psi parcheados en el módulo consumidor."""
    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    llamadas: list[str] = []
    monkeypatch.setattr(
        psi_mod, "pick",
        lambda rng, seq: (llamadas.append(tuple(seq)), decide)[1])
    monkeypatch.setattr(psi_mod, "roll_dice",
                        lambda expr, rng, crit=False: dado)
    return llamadas


def _recibe(pj, objetivo, ctx, cantidad: int) -> int:
    """Daño central (fase 1a del pipeline) sobre ``objetivo``."""
    from dnd_sim.rules.damage import inflict_damage

    return inflict_damage(objetivo, cantidad, "slashing", source=pj,
                          ctx=ctx, rng=ctx.rng)


def test_el_protective_field_reduce_el_dado_mas_el_mod_de_int(monkeypatch):
    _parchea_campo(monkeypatch, dado=4)
    pj, trait, enemigo, ctx = _bajo_golpe(level=6)
    _recibe(pj, enemigo, ctx, 10)
    # 10 - (4 del dado + 2 de mod INT) = 4 aplicados.
    assert enemigo.hp == 60 - 4
    assert trait.dados_restantes == psionic_dice_count(6) - 1
    assert pj.state.reaction_used is True
    assert any("Protective Field" in line for line in ctx.log)


def test_el_protective_field_comparte_la_reaccion_del_turno(monkeypatch):
    llamadas = _parchea_campo(monkeypatch, dado=4)
    pj, trait, enemigo, ctx = _bajo_golpe(level=6)
    _recibe(pj, enemigo, ctx, 10)
    _recibe(pj, enemigo, ctx, 10)  # misma reacción ya gastada
    assert len(llamadas) == 1  # el segundo ni siquiera consulta el pick
    assert trait.dados_restantes == psionic_dice_count(6) - 1
    assert enemigo.hp == 60 - 4 - 10


def test_sin_dados_restantes_el_protective_field_no_consulta_pick(
        monkeypatch):
    def _revienta(rng, seq):
        raise AssertionError("sin dados no se consulta el pick")

    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    _parchea_campo(monkeypatch)
    pj, trait, enemigo, ctx = _bajo_golpe(level=6)
    trait.dados_restantes = 0
    monkeypatch.setattr(psi_mod, "pick", _revienta)
    _recibe(pj, enemigo, ctx, 10)
    assert enemigo.hp == 60 - 10
    assert pj.state.reaction_used is False


def test_el_protective_field_puede_proteger_al_propio_objetivo(monkeypatch):
    _parchea_campo(monkeypatch, dado=4)
    pj, trait, enemigo, ctx = _bajo_golpe(level=6)
    _recibe(pj, pj, ctx, 10)  # «tú u otra criatura»: se protege a sí mismo
    assert pj.hp == 70 - 4  # 10 - (4 + 2 de mod INT)


def test_el_protective_field_no_baja_el_daño_de_cero(monkeypatch):
    _parchea_campo(monkeypatch, dado=20)
    pj, trait, enemigo, ctx = _bajo_golpe(level=6)
    _recibe(pj, enemigo, ctx, 3)  # reducción 20+2 > 3 → 0 aplicado
    assert enemigo.hp == 60


def test_el_protective_field_no_se_activa_si_el_pick_dice_no(monkeypatch):
    llamadas = _parchea_campo(monkeypatch, decide="no")
    pj, trait, enemigo, ctx = _bajo_golpe(level=6)
    _recibe(pj, enemigo, ctx, 10)
    assert len(llamadas) == 1
    assert enemigo.hp == 60 - 10
    assert trait.dados_restantes == psionic_dice_count(6)
    assert pj.state.reaction_used is False


def test_el_protective_field_no_actua_por_debajo_del_nivel_seis(
        monkeypatch):
    def _revienta(rng, seq):
        raise AssertionError("nivel < 6 no consulta el pick")

    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    _parchea_campo(monkeypatch)
    pj, trait, enemigo, ctx = _bajo_golpe(level=5)
    monkeypatch.setattr(psi_mod, "pick", _revienta)
    _recibe(pj, enemigo, ctx, 10)
    assert enemigo.hp == 60 - 10


def test_sin_subclase_el_protective_field_no_consulta_ni_tira_rng(
        monkeypatch):
    def _revienta(rng, seq):
        raise AssertionError("sin la subclase no hay decisiones")

    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    _parchea_campo(monkeypatch)
    pj = _pj()
    apply_fighter(pj, level=5, fighting_style="Archery")
    enemigo = Monster("Orco", max_hp=60, ac=10, abilities=_abilities())
    ctx = SimpleNamespace(round=1, actor=pj, rng=random.Random(1),
                           combatants=[pj, enemigo], log=[])
    monkeypatch.setattr(psi_mod, "pick", _revienta)
    _recibe(pj, enemigo, ctx, 10)
    assert enemigo.hp == 60 - 10


# --- A6: Guarded Mind ---------------------------------------------------------


def _guardado(level: int = 15, **kwargs) -> tuple:
    """PJ Psi Warrior a nivel >= 15 con contexto de turno."""
    pj, trait = _psi(level=level, **kwargs)
    ctx = SimpleNamespace(round=1, actor=pj, rng=random.Random(1),
                           combatants=[pj], log=[])
    return pj, trait, ctx


def test_guarded_mind_concede_resistencia_psiquica_a_partir_del_nivel_15():
    from dnd_sim.core.enums import DamageType
    from dnd_sim.rules.damage import apply_damage_modifiers

    pj15, _, _ = _guardado(level=15)
    assert DamageType.PSYCHIC in pj15.resistances
    # La resistencia mitiga el daño psíquico redondeando hacia abajo.
    assert apply_damage_modifiers(10, DamageType.PSYCHIC, pj15) == 5
    pj14, _, _ = _guardado(level=14)
    assert DamageType.PSYCHIC not in pj14.resistances


def test_guarded_mind_no_acumula_la_resistencia_si_ya_la_tenia():
    from dnd_sim.core.enums import DamageType

    pj = _pj(level=15)
    pj.resistances = {DamageType.PSYCHIC}
    apply_fighter(pj, level=15, fighting_style="Archery")
    apply_psi_warrior(pj, level=15)
    assert pj.resistances == {DamageType.PSYCHIC}


def test_guarded_mind_purga_charmed_y_frightened_gastando_un_dado(
        monkeypatch):
    llamadas = _parchea_campo(monkeypatch, decide="si")
    pj, trait, ctx = _guardado()
    apply_condition(pj, Condition.CHARMED, ctx)
    apply_condition(pj, Condition.FRIGHTENED, ctx)
    trait.on_turn_start(pj, ctx)
    assert len(llamadas) == 1
    assert trait.dados_restantes == psionic_dice_count(15) - 1
    assert not pj.conditions.has(Condition.CHARMED)
    assert not pj.conditions.has(Condition.FRIGHTENED)
    assert any("Guarded Mind" in line for line in ctx.log)


def test_guarded_mind_con_pick_no_no_purga_ni_gasta(monkeypatch):
    llamadas = _parchea_campo(monkeypatch, decide="no")
    pj, trait, ctx = _guardado()
    apply_condition(pj, Condition.CHARMED, ctx)
    trait.on_turn_start(pj, ctx)
    assert len(llamadas) == 1
    assert trait.dados_restantes == psionic_dice_count(15)
    assert pj.conditions.has(Condition.CHARMED)


def test_guarded_mind_sin_condicion_no_consulta_pick(monkeypatch):
    def _revienta(rng, seq):
        raise AssertionError("sin condición no se consulta el pick")

    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    pj, trait, ctx = _guardado()
    monkeypatch.setattr(psi_mod, "pick", _revienta)
    trait.on_turn_start(pj, ctx)
    assert trait.dados_restantes == psionic_dice_count(15)


def test_guarded_mind_sin_dados_no_purga(monkeypatch):
    def _revienta(rng, seq):
        raise AssertionError("sin dados no se consulta el pick")

    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    pj, trait, ctx = _guardado()
    trait.dados_restantes = 0
    apply_condition(pj, Condition.CHARMED, ctx)
    monkeypatch.setattr(psi_mod, "pick", _revienta)
    trait.on_turn_start(pj, ctx)
    assert pj.conditions.has(Condition.CHARMED)


def test_guarded_mind_no_actua_por_debajo_del_nivel_quince(monkeypatch):
    def _revienta(rng, seq):
        raise AssertionError("nivel < 15 no se consulta el pick")

    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    pj, trait, ctx = _guardado(level=14)
    apply_condition(pj, Condition.CHARMED, ctx)
    monkeypatch.setattr(psi_mod, "pick", _revienta)
    trait.on_turn_start(pj, ctx)
    assert pj.conditions.has(Condition.CHARMED)


def test_guarded_mind_sin_ctx_rng_no_purga(monkeypatch):
    def _revienta(rng, seq):
        raise AssertionError("sin rng no se consulta el pick")

    import dnd_sim.rules.classes.fighter.subclasses.psi_warrior as psi_mod

    pj, trait, ctx = _guardado()
    apply_condition(pj, Condition.CHARMED, ctx)
    monkeypatch.setattr(psi_mod, "pick", _revienta)
    trait.on_turn_start(pj, None)
    assert pj.conditions.has(Condition.CHARMED)

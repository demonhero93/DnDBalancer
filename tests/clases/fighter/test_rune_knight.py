"""Tests de la subclase Rune Knight (TCE, PHB 2024).

Solo cubren lo que existe: en A1, las tablas de ``core/classes.py``; en
A2, el esqueleto, el registro y los datos sin efecto; en A3, la consulta
perezosa ``modificar_salvacion``/``modificar_prueba``; en A4, Giant's
Might; en A5, Runic Shield; en A6, los ganchos de turno; en A7, las
runas Hill y Frost; en A8-A11, Fire/Stone/Storm/Cloud; en A12, Master
of Runes y el cierre con integración ``run_combat``.
"""

from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from dnd_sim import Abilities, Attack, Monster, PlayerCharacter, apply_class
from dnd_sim.core.classes import (
    RUNES,
    giants_might_die_sides,
    giants_might_uses,
    rune_uses,
    runes_known_count,
    runic_shield_uses,
)
from dnd_sim.core.dice import D20Result, RollMode
from dnd_sim.core.enums import AttackRange, DamageType
from dnd_sim.engine.combat.attack import attack_roll
from dnd_sim.model.actions import TurnResources
from dnd_sim.rules.checks import ability_check, ability_check_bonus, skill_check
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import (
    RuneKnightFeatures,
    apply_champion,
    apply_rune_knight,
)
from dnd_sim.rules.classes.fighter.subclasses.rune_knight import (
    GiantsMightAction,
    RuneInvokeAction,
)
from dnd_sim.rules.conditions import Condition, apply_condition
from dnd_sim.rules.damage import apply_damage_modifiers
from dnd_sim.rules.roll_modifiers import AttackModifiers, attack_modifiers
from dnd_sim.rules.saves import saving_throw
from dnd_sim.rules.usage import begin_turn


# --- A1: tablas --------------------------------------------------------------


def test_tabla_runes_known_count_por_nivel():
    assert runes_known_count(1) == 0
    assert runes_known_count(2) == 0
    assert runes_known_count(3) == 2
    assert runes_known_count(6) == 2
    assert runes_known_count(7) == 3
    assert runes_known_count(9) == 3
    assert runes_known_count(10) == 4
    assert runes_known_count(14) == 4
    assert runes_known_count(15) == 5
    assert runes_known_count(20) == 5


def test_tabla_giants_might_die_sides_por_nivel():
    assert giants_might_die_sides(3) == 6
    assert giants_might_die_sides(9) == 6
    assert giants_might_die_sides(10) == 8
    assert giants_might_die_sides(17) == 8
    assert giants_might_die_sides(18) == 10
    assert giants_might_die_sides(20) == 10


def test_tabla_rune_uses_por_nivel():
    assert rune_uses(3) == 1
    assert rune_uses(14) == 1
    assert rune_uses(15) == 2
    assert rune_uses(20) == 2


def test_tabla_runic_shield_uses_es_el_bonificador_de_competencia():
    assert runic_shield_uses(3) == 2
    assert runic_shield_uses(7) == 3
    assert runic_shield_uses(15) == 5
    assert runic_shield_uses(20) == 6


def test_tabla_giants_might_uses_es_el_bonificador_de_competencia():
    assert giants_might_uses(3) == 2
    assert giants_might_uses(7) == 3
    assert giants_might_uses(15) == 5
    assert giants_might_uses(20) == 6


def test_pool_runas_tiene_las_seis_claves():
    assert RUNES == ("cloud", "fire", "frost", "hill", "stone", "storm")


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


def _rune(pj) -> RuneKnightFeatures:
    for trait in pj.traits:
        if isinstance(trait, RuneKnightFeatures):
            return trait
    raise AssertionError("el PJ no tiene RuneKnightFeatures")


def test_rune_knight_registrada_en_la_tabla_de_subclases():
    assert "rune_knight" in CLASSES["fighter"].subclasses
    sub = CLASSES["fighter"].subclasses["rune_knight"]
    assert sub.name == "Rune Knight"
    assert sub.class_name == "fighter"
    assert sub.min_level == 3


def test_apply_class_y_apply_rune_knight_son_equivalentes(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.rune_knight as rk_mod

    a = _pj(level=3)
    apply_fighter(a, level=3, fighting_style="Archery")
    monkeypatch.setattr(rk_mod, "_RNG_CREACION", random.Random(0))
    t1 = apply_rune_knight(a, level=3)

    b = _pj(level=3)
    apply_fighter(b, level=3, fighting_style="Archery")
    monkeypatch.setattr(rk_mod, "_RNG_CREACION", random.Random(0))
    apply_class(b, "fighter", "rune_knight", level=3,
                fighting_style="Archery")
    t2 = _rune(b)

    assert t1.runas == t2.runas
    assert t1.usos_runa == t2.usos_runa
    assert t1.giants_might_usos == t2.giants_might_usos
    assert t1.runic_shield_usos == t2.runic_shield_usos


def test_aplicar_sin_clase_guerrero_da_error():
    pj = _pj()
    with pytest.raises(ValueError, match="apply_fighter"):
        apply_rune_knight(pj, level=3)


def test_aplicar_con_nivel_inferior_a_tres_da_error():
    pj = _pj()
    apply_fighter(pj, level=1, fighting_style="Archery")
    with pytest.raises(ValueError, match="nivel >= 3"):
        apply_rune_knight(pj, level=2)


def test_runas_conocidas_segun_el_nivel():
    for level, n in ((3, 2), (7, 3), (10, 4), (15, 5)):
        pj = _pj(level=level)
        apply_fighter(pj, level=level, fighting_style="Archery")
        trait = apply_rune_knight(pj, level=level)
        assert len(trait.runas) == n
        assert set(trait.runas) <= set(RUNES)
        assert set(trait.usos_runa) == set(trait.runas)
        assert all(trait.usos_runa[r] == rune_uses(level)
                   for r in trait.runas)


def test_karg_runas_invalido_da_error():
    pj = _pj()
    apply_fighter(pj, level=3, fighting_style="Archery")
    with pytest.raises(ValueError, match="no es una runa"):
        apply_rune_knight(pj, level=3, runes=("fire", "volcano"))
    with pytest.raises(ValueError, match="se esperaban 2"):
        apply_rune_knight(pj, level=3, runes=("fire",))


def test_pasivos_y_bonus_proficiencies_congelados_sin_efecto():
    pj = _pj(level=10)
    apply_fighter(pj, level=10, fighting_style="Archery")
    antes = set(pj.skill_proficiencies or set())
    trait = apply_rune_knight(
        pj, level=10, runes=("cloud", "fire", "frost", "hill"))
    # Datos sin efecto: ni herramientas ni idiomas se añaden.
    assert trait.pasivos_runas is True
    assert trait.bonus_proficiencies is True
    assert set(pj.skill_proficiencies or set()) == antes


def test_sin_la_subclase_rune_knight_no_se_consume_rng(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("sin la subclase no se consulta el módulo")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight as rk_mod

    monkeypatch.setattr(rk_mod, "sample", _revienta)
    pj = _pj(level=3)
    apply_fighter(pj, level=3, fighting_style="Archery")
    apply_champion(pj, level=3)
    otro = _pj(level=3)
    apply_class(otro, "fighter", level=3, fighting_style="Archery")


# --- A3: consulta perezosa de salvaciones y pruebas --------------------------


def _ctx(*combatantes) -> SimpleNamespace:
    """Contexto mínimo con ``combatants`` para la consulta."""
    return SimpleNamespace(round=1, actor=combatantes[0],
                           rng=random.Random(1),
                           combatants=list(combatantes), log=[])


class _EspiaSalvacion:
    """Rasgo espía con el método ``modificar_salvacion`` (A3)."""

    def __init__(self, ventaja: bool = True, desventaja: bool = False,
                 bonus: int = 0) -> None:
        self.ventaja = ventaja
        self.desventaja = desventaja
        self.bonus = bonus
        self.llamadas: list = []

    def modificar_salvacion(self, habilidad, sujeto, ctx):
        self.llamadas.append((habilidad, sujeto, ctx))
        return self.ventaja, self.desventaja, self.bonus


class _EspiaPrueba:
    """Rasgo espía con el método ``modificar_prueba`` (A3)."""

    def __init__(self, ventaja: bool = True, desventaja: bool = False,
                 bonus: int = 0) -> None:
        self.ventaja = ventaja
        self.desventaja = desventaja
        self.bonus = bonus
        self.llamadas: list = []

    def modificar_prueba(self, habilidad, sujeto, ctx):
        self.llamadas.append((habilidad, sujeto, ctx))
        return self.ventaja, self.desventaja, self.bonus


def test_sin_rasgos_que_definan_la_consulta_no_consume_rng():
    pj = _pj()
    ctx = _ctx(pj)
    rng1 = random.Random(7)
    sr1 = saving_throw(pj, "str", 12, rng1, ctx=ctx)
    rng2 = random.Random(7)
    sr2 = saving_throw(pj, "str", 12, rng2, ctx=ctx)
    assert sr1 == sr2
    assert rng1.getstate() == rng2.getstate()
    # Sin ``ctx`` la consulta no se hace ni siquiera con un rasgo espía.
    espia = _EspiaSalvacion()
    pj.traits.append(espia)
    saving_throw(pj, "str", 12, random.Random(3), ctx=None)
    assert espia.llamadas == []


def test_un_rasgo_espia_de_salvacion_confirma_la_consulta():
    pj = _pj()
    espia = _EspiaSalvacion()
    pj.traits.append(espia)
    ctx = _ctx(pj)
    sr = saving_throw(pj, "str", 20, random.Random(1), ctx=ctx)
    assert espia.llamadas == [("str", pj, ctx)]
    assert sr.mode == RollMode.ADVANTAGE


def test_ventaja_y_desventaja_se_anulan_en_la_consulta_de_salvacion():
    pj = _pj()
    pj.traits.append(_EspiaSalvacion(ventaja=True, desventaja=True))
    sr = saving_throw(pj, "str", 12, random.Random(1), ctx=_ctx(pj))
    assert sr.mode == RollMode.NORMAL


def test_el_bonificador_de_la_consulta_se_suma_a_la_salvacion(monkeypatch):
    import dnd_sim.rules.saves as saves_mod

    def _d20_fijo(rng, mode=None):
        return SimpleNamespace(value=10, rolls=[10])

    monkeypatch.setattr(saves_mod, "roll_d20", _d20_fijo)
    pj = _pj()
    pj.traits.append(_EspiaSalvacion(ventaja=False, bonus=5))
    sr = saving_throw(pj, "str", 12, random.Random(1), ctx=_ctx(pj))
    assert sr.total == 10 + pj.saving_throw_bonus("str") + 5


def test_un_rasgo_espia_de_prueba_confirma_la_consulta():
    pj = _pj()
    espia = _EspiaPrueba()
    pj.traits.append(espia)
    ctx = _ctx(pj)
    res = ability_check(pj, "con", 20, random.Random(1), ctx=ctx)
    assert espia.llamadas == [("con", pj, ctx)]
    assert res.mode == RollMode.ADVANTAGE


def test_ventaja_y_desventaja_se_anulan_en_la_consulta_de_prueba():
    pj = _pj()
    pj.traits.append(_EspiaPrueba(ventaja=True, desventaja=True))
    res = ability_check(pj, "str", 12, random.Random(1), ctx=_ctx(pj))
    assert res.mode == RollMode.NORMAL


def test_el_bonificador_de_la_consulta_se_suma_a_la_prueba(monkeypatch):
    import dnd_sim.rules.checks as checks_mod

    def _d20_fijo(rng, mode=None):
        return SimpleNamespace(value=10, rolls=[10])

    monkeypatch.setattr(checks_mod, "roll_d20", _d20_fijo)
    pj = _pj()
    pj.traits.append(_EspiaPrueba(ventaja=False, bonus=4))
    res = ability_check(pj, "str", 12, random.Random(1), ctx=_ctx(pj))
    assert res.total == 10 + ability_check_bonus(pj, "str") + 4


def test_en_pruebas_de_habilidad_se_pasa_la_caracteristica_efectiva():
    pj = _pj()
    espia = _EspiaPrueba()
    pj.traits.append(espia)
    skill_check(pj, "athletics", 20, random.Random(1), ctx=_ctx(pj))
    assert espia.llamadas[-1][0] == "str"


def test_la_consulta_mira_a_los_otros_vivos_y_no_a_muertos_o_incapacitados():
    pj = _pj()
    vivo, muerto, incapaz = _pj(), _pj(), _pj()
    muerto.hp = 0
    ctx0 = _ctx(pj)
    apply_condition(incapaz, Condition.INCAPACITATED, ctx0)
    espia_vivo = _EspiaSalvacion(ventaja=True)
    # Si muerto o incapaz se consultaran, su (ventaja y desventaja) anularía
    # la ventaja del espía vivo y el modo final sería NORMAL.
    espia_muerto = _EspiaSalvacion(ventaja=True, desventaja=True)
    espia_incapaz = _EspiaSalvacion(ventaja=True, desventaja=True)
    vivo.traits.append(espia_vivo)
    muerto.traits.append(espia_muerto)
    incapaz.traits.append(espia_incapaz)
    ctx = _ctx(pj, vivo, muerto, incapaz)
    sr = saving_throw(pj, "str", 12, random.Random(1), ctx=ctx)
    assert espia_vivo.llamadas
    assert espia_muerto.llamadas == []
    assert espia_incapaz.llamadas == []
    assert sr.mode == RollMode.ADVANTAGE


# --- A4: Giant's Might -------------------------------------------------------


def _runas_sin_fuego(level: int) -> tuple:
    """Runas del pool sin Fire, con la cantidad que exige el nivel."""
    otras = [r for r in RUNES if r != "fire"]
    return tuple(otras[:runes_known_count(level)])


def _giant_pj(level: int = 5) -> tuple:
    """PJ con Fighter + Rune Knight (runas sin Fire: aíslan a Giant's)."""
    pj = _pj(level=level)
    apply_fighter(pj, level=level, fighting_style="Archery")
    trait = apply_rune_knight(pj, level=level, runes=_runas_sin_fuego(level))
    return pj, trait


def test_giant_might_se_activa_una_vez_y_gasta_un_uso():
    pj, trait = _giant_pj()
    accion = GiantsMightAction()
    ctx = _ctx(pj)
    assert accion.can_use(ctx) is True
    usos = trait.giants_might_usos
    accion.execute(ctx)
    assert trait.giants_might_activo is True
    assert trait.giants_might_usos == usos - 1
    assert any("Giant's Might" in line for line in ctx.log)
    # Una vez activo dura todo el combate y no se vuelve a activar.
    assert accion.can_use(ctx) is False


def test_giant_might_el_tamano_vuelve_al_original_en_reset():
    pj, trait = _giant_pj()
    assert pj.size == "medium"
    GiantsMightAction().execute(_ctx(pj))
    assert pj.size == "large"
    pj.reset()
    assert pj.size == pj.size_base == "medium"
    assert trait.giants_might_activo is False
    assert trait.giants_might_usos == giants_might_uses(5)


def test_giant_might_da_ventaja_solo_en_fuerza():
    pj, _ = _giant_pj()
    GiantsMightAction().execute(_ctx(pj))
    ctx = _ctx(pj)
    assert saving_throw(
        pj, "str", 15, random.Random(1), ctx=ctx).mode == RollMode.ADVANTAGE
    assert saving_throw(
        pj, "con", 15, random.Random(1), ctx=ctx).mode == RollMode.NORMAL
    assert saving_throw(
        pj, "dex", 15, random.Random(1), ctx=ctx).mode == RollMode.NORMAL
    assert ability_check(
        pj, "str", 15, random.Random(1), ctx=ctx).mode == RollMode.ADVANTAGE
    assert ability_check(
        pj, "int", 15, random.Random(1), ctx=ctx).mode == RollMode.NORMAL


def test_giant_might_daño_extra_una_vez_por_turno():
    pj, trait = _giant_pj()
    trait.giants_might_activo = True
    ctx = _ctx(pj)
    enemigo = _pj(name="Enemigo")
    arma = pj.attacks[0]
    rng = random.Random(3)
    v1 = trait.extra_attack_damage(pj, enemigo, AttackRange.MELEE,
                                   ctx=ctx, rng=rng, atk=arma)
    assert 1 <= v1 <= 6
    v2 = trait.extra_attack_damage(pj, enemigo, AttackRange.MELEE,
                                   ctx=ctx, rng=rng, atk=arma)
    assert v2 == 0
    # El flag «una vez por turno» se reinicia al empezar el turno.
    trait.on_turn_start(pj, ctx)
    v3 = trait.extra_attack_damage(pj, enemigo, AttackRange.MELEE,
                                   ctx=ctx, rng=rng, atk=arma)
    assert 1 <= v3 <= 6


def test_giant_might_el_daño_extra_es_del_tipo_del_arma(monkeypatch):
    import dnd_sim.engine.combat.attack as attack_mod
    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    monkeypatch.setattr(attack_mod, "roll_d20",
                        lambda rng, mode=None: D20Result(
                            value=15, rolls=[15],
                            mode=mode or RollMode.NORMAL))
    monkeypatch.setattr(attack_mod, "roll_dice",
                        lambda expr, rng, **kw: 5)
    monkeypatch.setattr(rk_mod, "roll_dice",
                        lambda expr, rng, **kw: 2)
    pj, trait = _giant_pj()
    trait.giants_might_activo = True
    enemigo = Monster("Orco", max_hp=60, ac=10, abilities=_abilities())
    enemigo.resistances = {"slashing"}
    attack_roll(pj, enemigo, pj.attacks[0], random.Random(1),
                log=[], ctx=_ctx(pj, enemigo))
    # Bruto = 5 (arma) + 3 (mod FUE) + 2 (extra) = 10; la resistencia a
    # cortante mitiga TODO el bruto → el extra viaja con el tipo del arma.
    assert enemigo.max_hp - enemigo.hp == 5


def test_giant_might_el_dado_de_daño_sube_con_el_nivel(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    exprs: list = []

    def _espia(expr, rng, **kwargs):
        exprs.append(expr)
        return 1

    monkeypatch.setattr(rk_mod, "roll_dice", _espia)
    for nivel, esperado in ((3, "1d6"), (10, "1d8"), (18, "1d10")):
        pj, trait = _giant_pj(level=nivel)
        trait.giants_might_activo = True
        trait.extra_attack_damage(pj, _pj(), AttackRange.MELEE,
                                  ctx=_ctx(pj), rng=random.Random(1),
                                  atk=pj.attacks[0])
    assert exprs == ["1d6", "1d8", "1d10"]


def test_giant_might_en_nivel_dieciocho_el_tamano_es_enorme():
    pj, _ = _giant_pj(level=18)
    GiantsMightAction().execute(_ctx(pj))
    assert pj.size == "huge"


def test_giant_might_no_es_elegible_sin_usos_ni_con_la_accion_gastada():
    pj, trait = _giant_pj()
    accion = GiantsMightAction()
    ctx = _ctx(pj)
    assert accion.can_use(ctx) is True
    trait.giants_might_usos = 0
    assert accion.can_use(ctx) is False
    trait.giants_might_usos = giants_might_uses(5)
    assert accion.can_use(
        ctx, resources=TurnResources(bonus_action_used=True)) is False


def test_sin_subclase_giant_might_no_consulta_rng(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("sin la subclase no hay Giant's Might")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    monkeypatch.setattr(rk_mod, "roll_dice", _revienta)
    pj = _pj()
    apply_fighter(pj, level=5, fighting_style="Archery")
    assert not any(isinstance(a, GiantsMightAction) for a in pj.actions)
    enemigo = Monster("Orco", max_hp=60, ac=10, abilities=_abilities())
    attack_roll(pj, enemigo, pj.attacks[0], random.Random(1),
                log=[], ctx=_ctx(pj, enemigo))


# --- A5: Runic Shield --------------------------------------------------------


def _escudo_partida(*, level: int = 7, ac_objetivo: int = 15) -> tuple:
    """Monstruo ataca a un aliado del Rune Knight (NPC hostil a PJ)."""
    atacante = Monster("Orco", max_hp=60, ac=10, abilities=_abilities(),
                       attacks=[Attack("Hacha", "1d8", ability="str")])
    guardia = _pj(level=level, name="Guardia")
    apply_fighter(guardia, level=level, fighting_style="Archery")
    # Runas sin Fire: el pick de Fire Rune ensuciaría los contadores.
    trait = apply_rune_knight(guardia, level=level,
                              runes=_runas_sin_fuego(level))
    aliado = _pj(name="Alicia", ac=ac_objetivo)
    ctx = _ctx(atacante, guardia, aliado)
    return atacante, guardia, aliado, trait, ctx


def _parchea_escudo(monkeypatch, *, roll_atacante: int = 15,
                    roll_repetido: int = 3, decide: str = "si") -> list:
    """Tiradas fijas: d20 del atacante, d20 de la repetición y pick."""
    import dnd_sim.engine.combat.attack as attack_mod
    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    llamadas_pick = []
    monkeypatch.setattr(
        attack_mod, "roll_d20",
        lambda rng, mode=None: D20Result(value=roll_atacante,
                                         rolls=[roll_atacante],
                                         mode=mode or RollMode.NORMAL))
    monkeypatch.setattr(
        rk_mod, "roll_d20",
        lambda rng, mode=None: D20Result(value=roll_repetido,
                                         rolls=[roll_repetido],
                                         mode=mode or RollMode.NORMAL))

    def _pick(rng, seq):
        llamadas_pick.append(tuple(seq))
        return decide

    monkeypatch.setattr(rk_mod, "pick", _pick)
    return llamadas_pick


def test_runic_shield_convierte_un_impacto_en_fallo(monkeypatch):
    atacante, guardia, aliado, trait, ctx = _escudo_partida()
    llamadas = _parchea_escudo(monkeypatch, roll_atacante=15,
                               roll_repetido=3, decide="si")
    usos = trait.runic_shield_usos
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    # El golpe original entraba (15 + bonus >= 15); el 3 repele.
    assert len(llamadas) == 1
    assert aliado.hp == 70
    assert trait.runic_shield_usos == usos - 1
    assert guardia.state.reaction_used is True
    assert any("Runic Shield" in line for line in ctx.log)


def test_runic_shield_no_actua_si_el_golpe_original_falla(monkeypatch):
    atacante, guardia, aliado, trait, ctx = _escudo_partida()

    def _revienta(rng, seq):
        raise AssertionError("un fallo original no consulta la repetición")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    _parchea_escudo(monkeypatch, roll_atacante=1, decide="si")
    monkeypatch.setattr(rk_mod, "pick", _revienta)
    usos = trait.runic_shield_usos
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert aliado.hp == 70
    assert trait.runic_shield_usos == usos
    assert guardia.state.reaction_used is False


def test_runic_shield_un_uno_natural_en_la_repeticion_falla_aunque_entre(
        monkeypatch):
    # CA del aliado en 2: el total nuevo (1 + bonus) entraría, pero el
    # 1 natural falla siempre.
    atacante, guardia, aliado, trait, ctx = _escudo_partida(ac_objetivo=2)
    _parchea_escudo(monkeypatch, roll_atacante=15, roll_repetido=1,
                    decide="si")
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert aliado.hp == 70


def test_runic_shield_un_veinte_natural_en_la_repeticion_es_critico(
        monkeypatch):
    atacante, guardia, aliado, trait, ctx = _escudo_partida()
    _parchea_escudo(monkeypatch, roll_atacante=15, roll_repetido=20,
                    decide="si")
    import dnd_sim.engine.combat.attack as attack_mod

    # Dado del arma: 5 normal y 10 crítico (el crítico lo duplica).
    monkeypatch.setattr(
        attack_mod, "roll_dice",
        lambda expr, rng, crit=False, **kw: 10 if crit else 5)
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    # Orco FUE 16 (+3): bruto 10 + 3 = 13 (sin crítico serían 8).
    assert aliado.hp == 70 - 13


def test_runic_shield_no_actua_sobre_el_dueno_ni_contra_enemigos(
        monkeypatch):
    atacante, guardia, aliado, trait, ctx = _escudo_partida()
    llamadas = _parchea_escudo(monkeypatch, roll_atacante=15, decide="si")
    usos = trait.runic_shield_usos
    # (a) «OTRA criatura»: el propio dueño como objetivo no se protege.
    attack_roll(atacante, guardia, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert llamadas == []
    # (b) el dueño ataca a un enemigo: su rasgo no está en ese bando.
    attack_roll(guardia, atacante, guardia.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert llamadas == []
    assert trait.runic_shield_usos == usos
    assert guardia.state.reaction_used is False


def test_runic_shield_gasta_la_reaccion_compartida(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    atacante, guardia, aliado, trait, ctx = _escudo_partida()
    _parchea_escudo(monkeypatch, decide="si")
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert guardia.state.reaction_used is True
    usos = trait.runic_shield_usos

    def _revienta(rng, seq):
        raise AssertionError("sin reacción no se consulta el pick")

    monkeypatch.setattr(rk_mod, "pick", _revienta)
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert trait.runic_shield_usos == usos


def test_runic_shield_sin_usos_no_consulta_rng(monkeypatch):
    atacante, guardia, aliado, trait, ctx = _escudo_partida()
    llamadas = _parchea_escudo(monkeypatch, decide="si")
    trait.runic_shield_usos = 0
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert llamadas == []
    assert guardia.state.reaction_used is False
    assert aliado.hp < 70  # el golpe entra sin repetición


def test_runic_shield_no_actua_por_debajo_del_nivel_siete(monkeypatch):
    atacante, guardia, aliado, trait, ctx = _escudo_partida(level=6)
    llamadas = _parchea_escudo(monkeypatch, decide="si")
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert llamadas == []
    assert trait.runic_shield_usos == runic_shield_uses(6)


def test_runic_shield_sin_reentrada_solo_una_repeticion_por_ataque(
        monkeypatch):
    atacante, guardia, aliado, trait, ctx = _escudo_partida()
    guardia2 = _pj(level=7, name="Guardia2")
    apply_fighter(guardia2, level=7, fighting_style="Archery")
    trait2 = apply_rune_knight(guardia2, level=7)
    ctx.combatants.append(guardia2)
    llamadas = []
    for t in (trait, trait2):
        original = t.repetir_d20

        def espia(*args, _orig=original, **kwargs):
            llamadas.append(1)
            return _orig(*args, **kwargs)

        t.repetir_d20 = espia
    _parchea_escudo(monkeypatch, decide="si")
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert len(llamadas) == 1


def test_sin_subclase_runic_shield_no_consulta_rng(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("sin la subclase no hay repetición")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    monkeypatch.setattr(rk_mod, "pick", _revienta)
    monkeypatch.setattr(rk_mod, "roll_d20", _revienta)
    import dnd_sim.engine.combat.attack as attack_mod

    monkeypatch.setattr(
        attack_mod, "roll_d20",
        lambda rng, mode=None: D20Result(value=15, rolls=[15],
                                         mode=mode or RollMode.NORMAL))
    atacante = Monster("Orco", max_hp=60, ac=10, abilities=_abilities(),
                       attacks=[Attack("Hacha", "1d8", ability="str")])
    aliado = _pj(name="Alicia")
    fighter = _pj(level=5, name="SinSubclase")
    apply_fighter(fighter, level=5, fighting_style="Archery")
    ctx = _ctx(atacante, fighter, aliado)
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert aliado.hp < 70  # el golpe entra sin repetición
    assert fighter.state.reaction_used is False


# --- A7: runas Hill y Frost --------------------------------------------------


def _invocada(runa: str = "frost", level: int = 5) -> tuple:
    """PJ con Fighter + Rune Knight y ``runa`` entre las conocidas."""
    pj = _pj(level=level)
    apply_fighter(pj, level=level, fighting_style="Archery")
    otras = [r for r in RUNES if r != runa]
    elegidas = ([runa] + otras)[:runes_known_count(level)]
    trait = apply_rune_knight(pj, level=level, runes=tuple(elegidas))
    return pj, trait


def test_rune_invoke_registrada_solo_para_runas_frost_y_hill():
    pj = _pj(level=5)
    apply_fighter(pj, level=5, fighting_style="Archery")
    apply_rune_knight(pj, level=5, runes=("frost", "hill"))
    runas = [a.runa for a in pj.actions if isinstance(a, RuneInvokeAction)]
    assert runas == ["frost", "hill"]
    otro = _pj(level=5)
    apply_fighter(otro, level=5, fighting_style="Archery")
    apply_rune_knight(otro, level=5, runes=("cloud", "fire"))
    assert not any(isinstance(a, RuneInvokeAction) for a in otro.actions)


def test_frost_invocado_suma_dos_a_fue_y_con_en_pruebas_y_salvaciones():
    pj, trait = _invocada("frost")
    accion = RuneInvokeAction("frost")
    ctx = _ctx(pj)
    assert accion.can_use(ctx) is True

    def _sal(abilidad):
        return saving_throw(pj, abilidad, 1, random.Random(3),
                            ctx=ctx).total

    def _prueba(abilidad):
        return ability_check(pj, abilidad, 1, random.Random(3),
                             ctx=ctx).total

    b_str, b_con, b_dex = _sal("str"), _sal("con"), _sal("dex")
    p_str, p_dex = _prueba("str"), _prueba("dex")
    accion.execute(ctx)
    assert trait.frost_activo is True
    assert _sal("str") == b_str + 2
    assert _sal("con") == b_con + 2
    assert _sal("dex") == b_dex
    assert _prueba("str") == p_str + 2
    assert _prueba("dex") == p_dex


def test_hill_concede_resistencia_bpc_no_acumula_y_se_revoca_al_reset():
    pj, trait = _invocada("hill")
    # Resistencia preexistente: Hill no debe duplicarla al revocar.
    pj.resistances = set(pj.resistances) | {"slashing"}
    accion = RuneInvokeAction("hill")
    ctx = _ctx(pj)
    accion.execute(ctx)
    assert trait.hill_activo is True
    tipos = {DamageType.BLUDGEONING, DamageType.PIERCING,
             DamageType.SLASHING}
    assert tipos <= set(pj.resistances)
    # No acumula: 10 de cortante se mitiga UNA sola vez (regla estándar).
    assert apply_damage_modifiers(10, "slashing", pj) == 5
    # Sin resistencia a fuego, el daño no cambia.
    assert apply_damage_modifiers(10, "fire", pj) == 10
    # El reset revoca SOLO lo que Hill concedió; la preexistente queda.
    pj.reset()
    assert DamageType.SLASHING in pj.resistances
    assert DamageType.BLUDGEONING not in pj.resistances
    assert trait.hill_activo is False


def test_pasivo_de_veneno_solo_si_conoces_hill():
    pj, _ = _invocada("hill")
    assert DamageType.POISON in pj.resistances
    otro = _pj(level=5)
    apply_fighter(otro, level=5, fighting_style="Archery")
    apply_rune_knight(otro, level=5, runes=("cloud", "fire"))
    assert DamageType.POISON not in otro.resistances


def test_una_invocacion_por_runa_aunque_en_nivel_15_haya_dos_usos():
    pj, trait = _invocada("frost", level=15)
    accion = RuneInvokeAction("frost")
    ctx = _ctx(pj)
    assert trait.usos_runa["frost"] == 2  # Master of Runes
    assert accion.can_use(ctx) is True
    accion.execute(ctx)
    assert trait.usos_runa["frost"] == 1  # gasta un uso
    assert accion.can_use(ctx) is False  # ya invocada: no se repite
    accion.execute(ctx)  # reentrada: no gasta el segundo uso
    assert trait.usos_runa["frost"] == 1


def test_rune_invoke_no_elegible_sin_accion_sin_usos_y_sin_runas():
    pj, trait = _invocada("frost")
    ctx = _ctx(pj)
    accion = RuneInvokeAction("frost")
    # Acción bonus ya gastada.
    assert accion.can_use(
        ctx, resources=TurnResources(bonus_action_used=True)) is False
    # Sin usos.
    trait.usos_runa["frost"] = 0
    assert accion.can_use(ctx) is False
    # Runa desconocida (solo se conocen frost/cloud).
    assert RuneInvokeAction("hill").can_use(ctx) is False


def test_sin_subclase_cero_rng_en_invocacion_y_consultas(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("sin la subclase no hay decisiones")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    monkeypatch.setattr(rk_mod, "pick", _revienta)
    monkeypatch.setattr(rk_mod, "roll_d20", _revienta)
    pj = _pj(level=5)
    apply_fighter(pj, level=5, fighting_style="Archery")
    assert not any(isinstance(a, RuneInvokeAction) for a in pj.actions)
    ctx = _ctx(pj)
    saving_throw(pj, "str", 15, random.Random(1), ctx=ctx)
    ability_check(pj, "str", 15, random.Random(1), ctx=ctx)


# --- A8: Fire Rune ------------------------------------------------------------


def _fuego(level: int = 5) -> tuple:
    """PJ con Fire Rune, enemigo y contexto de combate."""
    pj, trait = _invocada("fire", level=level)
    enemigo = Monster("Orco", max_hp=60, ac=10, abilities=_abilities())
    ctx = SimpleNamespace(round=1, actor=pj, rng=random.Random(1),
                           combatants=[pj, enemigo], log=[])
    return pj, trait, enemigo, ctx


def _parchea_fuego(monkeypatch, *, ataque=15, dado_arma=5, dado_fuego=6,
                   salva=1, decide="si") -> list:
    """Impacto y daños fijos, pick y salvación de FUE fijas."""
    import dnd_sim.engine.combat.attack as attack_mod
    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod
    import dnd_sim.rules.saves as saves_mod

    llamadas_pick = []
    # Restringido da ventaja al segundo ataque: el resultado fijo lleva
    # dos caras cuando el motor pide ADVANTAGE (log con rolls[1]).
    def _d20(rng, mode=None):
        m = mode or RollMode.NORMAL
        caras = [ataque] if m == RollMode.NORMAL else [ataque, ataque]
        return D20Result(value=ataque, rolls=caras, mode=m)

    monkeypatch.setattr(attack_mod, "roll_d20", _d20)
    monkeypatch.setattr(attack_mod, "roll_dice",
                        lambda expr, rng, **kw: dado_arma)
    monkeypatch.setattr(rk_mod, "roll_dice",
                        lambda expr, rng, **kw: dado_fuego)
    monkeypatch.setattr(
        saves_mod, "roll_d20",
        lambda rng, mode=None: D20Result(value=salva, rolls=[salva],
                                         mode=mode or RollMode.NORMAL))

    def _pick(rng, seq):
        llamadas_pick.append(tuple(seq))
        return decide

    monkeypatch.setattr(rk_mod, "pick", _pick)
    return llamadas_pick


def test_fire_rune_al_fallar_la_salvacion_restringe_con_dano_extra(
        monkeypatch):
    pj, trait, enemigo, ctx = _fuego()
    llamadas = _parchea_fuego(monkeypatch, decide="si", salva=1)
    usos = trait.usos_runa["fire"]
    attack_roll(pj, enemigo, pj.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    # Daño: 6 (fuego) + 5 (arma) + 3 (FUE) = 14; salvación 1+3 < 14
    # (CD 8+PB3+CON3).
    assert enemigo.max_hp - enemigo.hp == 6 + 5 + 3
    assert trait.usos_runa["fire"] == usos - 1
    assert len(llamadas) == 1
    assert enemigo.conditions.has(Condition.RESTRAINED)
    assert enemigo.state.fire_runa is pj
    assert enemigo.state.fire_runa_hasta > ctx.round
    assert any("Fire Rune" in line for line in ctx.log)


def test_fire_rune_si_supera_la_salvacion_solo_hay_dano(monkeypatch):
    pj, trait, enemigo, ctx = _fuego()
    llamadas = _parchea_fuego(monkeypatch, salva=20)
    attack_roll(pj, enemigo, pj.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert enemigo.max_hp - enemigo.hp == 6 + 5 + 3
    assert len(llamadas) == 1
    assert trait.usos_runa["fire"] == 0
    assert not enemigo.conditions.has(Condition.RESTRAINED)
    assert enemigo.state.fire_runa is None


def test_fire_rune_dania_2d6_al_inicio_del_turno_del_objetivo(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    pj, trait, enemigo, ctx = _fuego()
    monkeypatch.setattr(rk_mod, "roll_dice",
                        lambda expr, rng, **kw: 4)
    enemigo.state.fire_runa = pj
    enemigo.state.fire_runa_hasta = 101
    trait.on_any_turn_start(enemigo, ctx)
    assert enemigo.max_hp - enemigo.hp == 4
    assert any("Fire Rune" in line for line in ctx.log)
    # Sin marca no hay daño ni dados.
    enemigo.state.fire_runa = None
    trait.on_any_turn_start(enemigo, ctx)
    assert enemigo.max_hp - enemigo.hp == 4


def test_fire_rune_las_salvaciones_de_fin_de_turno(monkeypatch):
    import dnd_sim.rules.saves as saves_mod

    pj, trait, enemigo, ctx = _fuego()
    enemigo.state.fire_runa = pj
    enemigo.state.fire_runa_hasta = 101
    apply_condition(enemigo, Condition.RESTRAINED, ctx, source=pj)
    # Fallo: la marca y la condición siguen.
    monkeypatch.setattr(
        saves_mod, "roll_d20",
        lambda rng, mode=None: D20Result(value=1, rolls=[1],
                                         mode=mode or RollMode.NORMAL))
    trait.on_any_turn_end(enemigo, ctx)
    assert enemigo.state.fire_runa is pj
    assert enemigo.conditions.has(Condition.RESTRAINED)
    # Éxito: termina el efecto.
    monkeypatch.setattr(
        saves_mod, "roll_d20",
        lambda rng, mode=None: D20Result(value=20, rolls=[20],
                                         mode=mode or RollMode.NORMAL))
    trait.on_any_turn_end(enemigo, ctx)
    assert enemigo.state.fire_runa is None
    assert enemigo.state.fire_runa_hasta == 0
    assert not enemigo.conditions.has(Condition.RESTRAINED)
    assert any("supera la Fire Rune" in line for line in ctx.log)


def test_fire_rune_no_se_rompe_con_pruebas_de_escape(monkeypatch):
    pj, trait, enemigo, ctx = _fuego()
    _parchea_fuego(monkeypatch, salva=1)
    attack_roll(pj, enemigo, pj.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert enemigo.conditions.has(Condition.RESTRAINED)
    # Solo las condiciones con ``escape`` adjunto se intentan al turno.
    begin_turn(enemigo, ctx)
    assert not any("prueba STR" in line for line in ctx.log)
    assert enemigo.conditions.has(Condition.RESTRAINED)
    assert enemigo.state.fire_runa is pj


def test_fire_rune_dos_invocaciones_dejan_una_sola_marca(monkeypatch):
    pj, trait, enemigo, ctx = _fuego(level=15)
    llamadas = _parchea_fuego(monkeypatch, salva=1)
    assert trait.usos_runa["fire"] == 2  # Master of Runes
    attack_roll(pj, enemigo, pj.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert trait.usos_runa["fire"] == 1
    attack_roll(pj, enemigo, pj.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert trait.usos_runa["fire"] == 0
    assert len(llamadas) == 2
    assert enemigo.state.fire_runa is pj
    restringidos = [i for i in enemigo.conditions.instances
                    if i.condition is Condition.RESTRAINED]
    assert len(restringidos) == 1


def test_fire_rune_el_objetivo_muerto_limpia_la_marca(monkeypatch):
    pj, trait, enemigo, ctx = _fuego()
    enemigo.state.fire_runa = pj
    enemigo.state.fire_runa_hasta = 101
    apply_condition(enemigo, Condition.RESTRAINED, ctx, source=pj)
    enemigo.hp = 0
    enemigo.mark_dead()
    assert enemigo.alive is False
    # Los muertos no tienen turno: la barre el del dueño de la runa.
    trait.on_any_turn_start(pj, ctx)
    assert enemigo.state.fire_runa is None
    assert not enemigo.conditions.has(Condition.RESTRAINED)


def test_fire_rune_reset_limpia_la_marca():
    pj, trait, enemigo, ctx = _fuego()
    enemigo.state.fire_runa = pj
    enemigo.state.fire_runa_hasta = 101
    apply_condition(enemigo, Condition.RESTRAINED, ctx, source=pj)
    enemigo.reset()
    assert enemigo.state.fire_runa is None
    assert enemigo.state.fire_runa_hasta == 0
    assert not enemigo.conditions.has(Condition.RESTRAINED)


def test_fire_rune_guards_sin_rng_y_pick_no(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("sin elegibilidad no se consulta el pick")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    pj, trait, enemigo, ctx = _fuego()
    monkeypatch.setattr(rk_mod, "pick", _revienta)
    # Sin usos.
    trait.usos_runa["fire"] = 0
    trait.extra_attack_damage(pj, enemigo, AttackRange.MELEE,
                              ctx=ctx, rng=ctx.rng, atk=pj.attacks[0])
    assert enemigo.hp == 60
    # Dueño incapacitado.
    trait.usos_runa["fire"] = 1
    apply_condition(pj, Condition.INCAPACITATED, ctx)
    trait.extra_attack_damage(pj, enemigo, AttackRange.MELEE,
                              ctx=ctx, rng=ctx.rng, atk=pj.attacks[0])
    assert enemigo.hp == 60
    # Con elegibilidad y pick «no»: la runa no se gasta.
    pj.conditions.clear()
    llamadas = _parchea_fuego(monkeypatch, decide="no")
    attack_roll(pj, enemigo, pj.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert len(llamadas) == 1
    assert trait.usos_runa["fire"] == 1
    assert enemigo.max_hp - enemigo.hp == 5 + 3  # solo el arma
    assert not enemigo.conditions.has(Condition.RESTRAINED)


def test_sin_subclase_la_fire_rune_no_consulta_rng(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("sin la subclase no hay decisiones")

    import dnd_sim.engine.combat.attack as attack_mod
    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    monkeypatch.setattr(rk_mod, "pick", _revienta)
    monkeypatch.setattr(rk_mod, "roll_dice", _revienta)
    monkeypatch.setattr(
        attack_mod, "roll_d20",
        lambda rng, mode=None: D20Result(value=15, rolls=[15],
                                         mode=mode or RollMode.NORMAL))
    monkeypatch.setattr(attack_mod, "roll_dice",
                        lambda expr, rng, **kw: 5)
    pj = _pj(level=5)
    apply_fighter(pj, level=5, fighting_style="Archery")
    enemigo = Monster("Orco", max_hp=60, ac=10, abilities=_abilities())
    ctx = SimpleNamespace(round=1, actor=pj, rng=random.Random(1),
                           combatants=[pj, enemigo], log=[])
    attack_roll(pj, enemigo, pj.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert enemigo.max_hp - enemigo.hp == 5 + 3


# --- A9: Stone Rune ----------------------------------------------------------

def _piedra(level: int = 5) -> tuple:
    """PJ con Stone Rune, enemigo y contexto de combate."""
    pj, trait = _invocada("stone", level=level)
    enemigo = Monster("Orco", max_hp=60, ac=10, abilities=_abilities())
    ctx = SimpleNamespace(round=1, actor=pj, rng=random.Random(1),
                           combatants=[pj, enemigo], log=[])
    return pj, trait, enemigo, ctx


def test_stone_rune_al_fallar_hechiza_e_incapacita(monkeypatch):
    pj, trait, enemigo, ctx = _piedra()
    llamadas = _parchea_fuego(monkeypatch, salva=1)
    assert trait.usos_runa["stone"] == 1
    trait.on_any_turn_end(enemigo, ctx)
    assert len(llamadas) == 1
    assert trait.usos_runa["stone"] == 0
    assert enemigo.conditions.has(Condition.CHARMED)
    assert enemigo.conditions.has(Condition.INCAPACITATED)
    assert enemigo.state.stone_de is pj
    assert enemigo.state.stone_pg == 60
    assert any("Stone Rune" in line for line in ctx.log)


def test_stone_rune_con_salvacion_exitosa_no_hechiza(monkeypatch):
    pj, trait, enemigo, ctx = _piedra()
    _parchea_fuego(monkeypatch, salva=20)
    trait.on_any_turn_end(enemigo, ctx)
    assert trait.usos_runa["stone"] == 0  # el uso se gasta igual
    assert not enemigo.conditions.has(Condition.CHARMED)
    assert not enemigo.conditions.has(Condition.INCAPACITATED)
    assert enemigo.state.stone_de is None


def test_stone_rune_con_pick_no_no_gasta(monkeypatch):
    pj, trait, enemigo, ctx = _piedra()
    llamadas = _parchea_fuego(monkeypatch, decide="no")
    trait.on_any_turn_end(enemigo, ctx)
    assert len(llamadas) == 1
    assert trait.usos_runa["stone"] == 1
    assert not enemigo.conditions.has(Condition.CHARMED)
    assert enemigo.state.stone_de is None


def test_stone_rune_el_dano_retira_la_marca_al_empezar_el_turno():
    pj, trait, enemigo, ctx = _piedra()
    enemigo.state.stone_de = pj
    enemigo.state.stone_pg = 60
    apply_condition(enemigo, Condition.CHARMED, ctx, source=pj)
    apply_condition(enemigo, Condition.INCAPACITATED, ctx, source=pj)
    enemigo.hp = 55  # ha recibido daño desde la marca
    trait.on_any_turn_start(enemigo, ctx)
    assert enemigo.state.stone_de is None
    assert enemigo.state.stone_pg == 0
    assert not enemigo.conditions.has(Condition.CHARMED)
    assert not enemigo.conditions.has(Condition.INCAPACITATED)
    assert any("recupera el control" in line for line in ctx.log)


def test_stone_rune_sin_dano_no_retira_la_marca():
    pj, trait, enemigo, ctx = _piedra()
    enemigo.state.stone_de = pj
    enemigo.state.stone_pg = 60
    apply_condition(enemigo, Condition.CHARMED, ctx, source=pj)
    apply_condition(enemigo, Condition.INCAPACITATED, ctx, source=pj)
    trait.on_any_turn_start(enemigo, ctx)
    assert enemigo.state.stone_de is pj
    assert enemigo.conditions.has(Condition.CHARMED)


def test_stone_rune_no_invoca_sobre_un_aliado(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("sin hostilidad no se consulta el pick")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    pj, trait, enemigo, ctx = _piedra()
    monkeypatch.setattr(rk_mod, "pick", _revienta)
    aliado = _pj()
    trait.on_any_turn_end(aliado, ctx)
    assert trait.usos_runa["stone"] == 1
    assert not aliado.conditions.has(Condition.CHARMED)


def test_stone_rune_ya_hechizado_no_repite_la_invocacion(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("ya Hechizado no se consulta el pick")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    pj, trait, enemigo, ctx = _piedra()
    apply_condition(enemigo, Condition.CHARMED, ctx, source="otra")
    monkeypatch.setattr(rk_mod, "pick", _revienta)
    trait.on_any_turn_end(enemigo, ctx)
    assert trait.usos_runa["stone"] == 1


def test_stone_rune_guards_sin_rng(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("sin elegibilidad no se consulta el pick")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    # Sin la runa Stone.
    pj, trait, enemigo, ctx = _fuego()
    monkeypatch.setattr(rk_mod, "pick", _revienta)
    trait.on_any_turn_end(enemigo, ctx)
    assert trait.usos_runa.get("stone", 0) == 0  # ni siquiera existe
    # Sin usos.
    pj, trait, enemigo, ctx = _piedra()
    monkeypatch.setattr(rk_mod, "pick", _revienta)
    trait.usos_runa["stone"] = 0
    trait.on_any_turn_end(enemigo, ctx)
    assert not enemigo.conditions.has(Condition.CHARMED)
    # Dueño incapacitado.
    trait.usos_runa["stone"] = 1
    apply_condition(pj, Condition.INCAPACITATED, ctx)
    trait.on_any_turn_end(enemigo, ctx)
    assert not enemigo.conditions.has(Condition.CHARMED)


def test_stone_rune_reset_limpia_la_marca():
    pj, trait, enemigo, ctx = _piedra()
    enemigo.state.stone_de = pj
    enemigo.state.stone_pg = 60
    apply_condition(enemigo, Condition.CHARMED, ctx, source=pj)
    apply_condition(enemigo, Condition.INCAPACITATED, ctx, source=pj)
    enemigo.reset()
    assert enemigo.state.stone_de is None
    assert enemigo.state.stone_pg == 0
    assert not enemigo.conditions.has(Condition.CHARMED)
    assert not enemigo.conditions.has(Condition.INCAPACITATED)


def test_sin_subclase_la_stone_rune_no_consulta_rng(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("sin la subclase no hay decisiones")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    monkeypatch.setattr(rk_mod, "pick", _revienta)
    monkeypatch.setattr(rk_mod, "roll_dice", _revienta)
    pj = _pj(level=5)
    apply_fighter(pj, level=5, fighting_style="Archery")
    enemigo = Monster("Orco", max_hp=60, ac=10, abilities=_abilities())
    ctx = SimpleNamespace(round=1, actor=pj, rng=random.Random(1),
                           combatants=[pj, enemigo], log=[])
    from dnd_sim.rules.traits import hooks

    assert all(
        rasgo.__class__.__name__ != "RuneKnightFeatures"
        for rasgo in pj.traits)
    for rasgo in hooks(pj.traits, "on_any_turn_end"):
        rasgo.on_any_turn_end(enemigo, ctx)
    for rasgo in hooks(pj.traits, "on_any_turn_start"):
        rasgo.on_any_turn_start(enemigo, ctx)


# --- A10: Storm Rune ---------------------------------------------------------


def _tormenta(level: int = 5) -> tuple:
    """PJ con Storm Rune, aliado propio, enemigo y contexto."""
    pj, trait = _invocada("storm", level=level)
    aliado = _pj()
    enemigo = Monster("Orco", max_hp=60, ac=10, abilities=_abilities())
    ctx = SimpleNamespace(round=1, actor=pj, rng=random.Random(1),
                           combatants=[pj, aliado, enemigo], log=[])
    return pj, trait, aliado, enemigo, ctx


def _accion_storm(pj) -> RuneInvokeAction:
    return next(a for a in pj.actions
                if isinstance(a, RuneInvokeAction) and a.runa == "storm")


def test_la_storm_rune_registra_su_accion_de_invocacion():
    pj, _ = _invocada("storm")
    assert isinstance(_accion_storm(pj), RuneInvokeAction)
    otro, _ = _invocada("frost")
    assert not any(isinstance(a, RuneInvokeAction) and a.runa == "storm"
                   for a in otro.actions)


def test_activar_storm_gasta_un_uso_y_levanta_el_estado():
    pj, trait, aliado, enemigo, ctx = _tormenta()
    accion = _accion_storm(pj)
    assert accion.can_use(ctx)
    usos = trait.usos_runa["storm"]
    accion.execute(ctx)
    assert trait.storm_activo is True
    assert trait.usos_runa["storm"] == usos - 1
    assert any("Storm Rune" in line for line in ctx.log)
    assert not accion.can_use(ctx)  # ya invocada: no se vuelve a invocar


def test_storm_no_es_elegible_sin_usos_o_sin_runa_conocida():
    pj, trait, aliado, enemigo, ctx = _tormenta()
    trait.usos_runa["storm"] = 0
    assert not _accion_storm(pj).can_use(ctx)
    trait.usos_runa["storm"] = rune_uses(pj.level)
    assert not RuneInvokeAction("fire").can_use(ctx)  # fire no es conocida


def test_storm_concede_ventaja_a_aliados_y_desventaja_a_enemigos(
        monkeypatch):
    llamadas = _parchea_fuego(monkeypatch, decide="si")
    pj, trait, aliado, enemigo, ctx = _tormenta()
    trait.storm_activo = True

    mods = AttackModifiers()
    trait.grant_attack_modifiers(mods, aliado, enemigo, AttackRange.MELEE,
                                 ctx=ctx, rng=ctx.rng)
    assert mods.advantage_sources == ["Storm Rune"]
    assert mods.disadvantage_sources == []
    assert pj.state.reaction_used is True

    # Con la reacción ya gastada no se consulta azar.
    mods = AttackModifiers()
    trait.grant_attack_modifiers(mods, enemigo, pj, AttackRange.MELEE,
                                 ctx=ctx, rng=ctx.rng)
    assert mods.disadvantage_sources == []
    assert len(llamadas) == 1

    pj.state.reaction_used = False
    mods = AttackModifiers()
    trait.grant_attack_modifiers(mods, enemigo, pj, AttackRange.MELEE,
                                 ctx=ctx, rng=ctx.rng)
    assert mods.disadvantage_sources == ["Storm Rune"]
    assert pj.state.reaction_used is True
    assert len(llamadas) == 2


def test_storm_con_pick_no_no_gasta_la_reaccion(monkeypatch):
    llamadas = _parchea_fuego(monkeypatch, decide="no")
    pj, trait, aliado, enemigo, ctx = _tormenta()
    trait.storm_activo = True
    mods = AttackModifiers()
    trait.grant_attack_modifiers(mods, aliado, enemigo, AttackRange.MELEE,
                                 ctx=ctx, rng=ctx.rng)
    assert len(llamadas) == 1
    assert mods.advantage_sources == []
    assert mods.disadvantage_sources == []
    assert pj.state.reaction_used is False


def test_storm_sin_invocar_o_sin_runa_no_consulta_pick(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("sin runa activa no se consulta el pick")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    monkeypatch.setattr(rk_mod, "pick", _revienta)
    pj, trait, aliado, enemigo, ctx = _tormenta()
    trait.grant_attack_modifiers(AttackModifiers(), aliado, enemigo,
                                 AttackRange.MELEE, ctx=ctx, rng=ctx.rng)
    trait.storm_activo = True
    trait.runas = tuple(r for r in trait.runas if r != "storm")
    trait.grant_attack_modifiers(AttackModifiers(), aliado, enemigo,
                                 AttackRange.MELEE, ctx=ctx, rng=ctx.rng)


def test_storm_guards_sin_rng_no_consultan_pick(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("guard sin RNG no debe llegar al pick")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    monkeypatch.setattr(rk_mod, "pick", _revienta)
    pj, trait, aliado, enemigo, ctx = _tormenta()
    trait.storm_activo = True
    # Sin rng.
    trait.grant_attack_modifiers(AttackModifiers(), aliado, enemigo,
                                 AttackRange.MELEE, ctx=ctx, rng=None)
    # Reacción ya gastada.
    pj.state.reaction_used = True
    trait.grant_attack_modifiers(AttackModifiers(), aliado, enemigo,
                                 AttackRange.MELEE, ctx=ctx, rng=ctx.rng)
    # Dueño Incapacitado: la alianza queda sin efecto (can_react).
    pj.state.reaction_used = False
    apply_condition(pj, Condition.INCAPACITATED, ctx)
    trait.grant_attack_modifiers(AttackModifiers(), aliado, enemigo,
                                 AttackRange.MELEE, ctx=ctx, rng=ctx.rng)


def test_storm_integra_con_attack_modifiers_del_motor(monkeypatch):
    llamadas = _parchea_fuego(monkeypatch, decide="si")
    pj, trait, aliado, enemigo, ctx = _tormenta()
    trait.storm_activo = True
    mods = attack_modifiers(aliado, enemigo, aliado.attacks[0],
                            AttackRange.MELEE, ctx=ctx, rng=ctx.rng)
    assert "Storm Rune" in mods.advantage_sources
    assert len(llamadas) == 1


def test_sin_subclase_la_storm_rune_no_consulta_pick(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("sin la subclase no hay decisiones")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    monkeypatch.setattr(rk_mod, "pick", _revienta)
    pj = _pj(level=5)
    apply_fighter(pj, level=5, fighting_style="Archery")
    enemigo = Monster("Orco", max_hp=60, ac=10, abilities=_abilities())
    ctx = SimpleNamespace(round=1, actor=pj, rng=random.Random(1),
                           combatants=[pj, enemigo], log=[])
    from dnd_sim.rules.traits import hooks

    assert all(rasgo.__class__.__name__ != "RuneKnightFeatures"
               for rasgo in pj.traits)
    for rasgo in hooks(pj.traits, "grant_attack_modifiers"):
        rasgo.grant_attack_modifiers(AttackModifiers(), enemigo, pj,
                                     AttackRange.MELEE, ctx=ctx,
                                     rng=ctx.rng)


# --- A11: Cloud Rune ---------------------------------------------------------


def _nube_partida(*, level: int = 5, ac_refuerzo: int = 10) -> tuple:
    """Monstruo ataca a un aliado; hay OTRO enemigo para redirigir."""
    atacante = Monster("Orco", max_hp=60, ac=10, abilities=_abilities(),
                       attacks=[Attack("Hacha", "1d8", ability="str")])
    refuerzo = Monster("Goblin", max_hp=30, ac=ac_refuerzo,
                       abilities=_abilities())
    guardia = _pj(level=level, name="Guardia")
    apply_fighter(guardia, level=level, fighting_style="Archery")
    # Runas sin Fire (cloud primero): el pick de Fire ensuciaría contadores.
    trait = apply_rune_knight(guardia, level=level,
                              runes=_runas_sin_fuego(level))
    aliado = _pj(name="Alicia", ac=15)
    ctx = _ctx(atacante, guardia, aliado, refuerzo)
    return atacante, guardia, aliado, refuerzo, trait, ctx


def _parchea_nube(monkeypatch, *, roll_atacante: int = 15,
                  decide: str = "si", dado_arma: int = 5) -> list:
    """d20 del atacante, dado de arma y pick fijos (Cloud, A11)."""
    import dnd_sim.engine.combat.attack as attack_mod
    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    llamadas = []
    monkeypatch.setattr(
        attack_mod, "roll_d20",
        lambda rng, mode=None: D20Result(value=roll_atacante,
                                         rolls=[roll_atacante],
                                         mode=mode or RollMode.NORMAL))
    monkeypatch.setattr(
        attack_mod, "roll_dice",
        lambda expr, rng, crit=False, **kw: (2 * dado_arma) if crit
        else dado_arma)

    def _pick(rng, seq):
        llamadas.append(tuple(seq))
        if tuple(seq) == ("no", "si"):
            return decide
        return seq[0]  # pool de un solo elemento: uniformidad irrelevante

    monkeypatch.setattr(rk_mod, "pick", _pick)
    return llamadas


def test_cloud_rune_redirige_el_golpe_a_otro_enemigo(monkeypatch):
    atacante, guardia, aliado, refuerzo, trait, ctx = _nube_partida()
    _parchea_nube(monkeypatch, roll_atacante=15, decide="si")
    usos = trait.usos_runa["cloud"]
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    # El aliado no recibe nada; el refuerzo sí (15 + 3 >= 10).
    assert aliado.hp == 70
    assert refuerzo.hp == 30 - (5 + 3)
    assert trait.usos_runa["cloud"] == usos - 1
    assert guardia.state.reaction_used is True
    assert any("Cloud Rune" in line for line in ctx.log)


def test_cloud_rune_conserva_el_critico_sobre_el_nuevo_objetivo(monkeypatch):
    atacante, guardia, aliado, refuerzo, trait, ctx = _nube_partida()
    _parchea_nube(monkeypatch, roll_atacante=20, decide="si")
    usos = trait.usos_runa["cloud"]
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    # Doble dado (5 -> 10) + 3: el crítico viaja al nuevo objetivo.
    assert aliado.hp == 70
    assert refuerzo.hp == 30 - (10 + 3)
    assert trait.usos_runa["cloud"] == usos - 1


def test_cloud_rune_recalcula_la_ca_contra_el_nuevo_objetivo(monkeypatch):
    # CA 25 del refuerzo > total del ataque (15 + FUE + prof): se salva
    # el aliado y el golpe falla contra el nuevo objetivo (usos y
    # reacción sí gastados).
    atacante, guardia, aliado, refuerzo, trait, ctx = _nube_partida(
        ac_refuerzo=25)
    _parchea_nube(monkeypatch, roll_atacante=15, decide="si")
    usos = trait.usos_runa["cloud"]
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert aliado.hp == 70
    assert refuerzo.hp == 30
    assert trait.usos_runa["cloud"] == usos - 1
    assert guardia.state.reaction_used is True


def test_cloud_rune_sin_otro_enemigo_no_consulta_pick(monkeypatch):
    def _revienta(rng, seq):
        raise AssertionError("sin elegibles no se consulta el pick")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    # Solo hay un enemigo y es el atacante: pool vacío.
    atacante, guardia, aliado, trait, ctx = _escudo_partida(level=5)
    llamadas = _parchea_escudo(monkeypatch, roll_atacante=15, decide="si")
    monkeypatch.setattr(rk_mod, "pick", _revienta)
    usos = trait.usos_runa["cloud"]
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert aliado.hp < 70
    assert trait.usos_runa["cloud"] == usos
    assert llamadas == []


def test_cloud_rune_con_pick_no_no_redirige(monkeypatch):
    atacante, guardia, aliado, refuerzo, trait, ctx = _nube_partida()
    llamadas = _parchea_nube(monkeypatch, roll_atacante=15, decide="no")
    usos = trait.usos_runa["cloud"]
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert [s for s in llamadas if s == ("no", "si")] == [("no", "si")]
    assert aliado.hp < 70
    assert refuerzo.hp == 30
    assert trait.usos_runa["cloud"] == usos
    assert guardia.state.reaction_used is False


def test_cloud_rune_gasta_la_reaccion_en_el_primer_golpe(monkeypatch):
    atacante, guardia, aliado, refuerzo, trait, ctx = _nube_partida()
    llamadas = _parchea_nube(monkeypatch, roll_atacante=15, decide="si")
    usos = trait.usos_runa["cloud"]
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    aliado.hp = 70  # el segundo golpe vuelve a apuntar al aliado
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    # Reacción gastada: el segundo golpe no se consulta y entra.
    assert aliado.hp < 70
    assert trait.usos_runa["cloud"] == usos - 1
    assert len([s for s in llamadas if s == ("no", "si")]) == 1


def test_cloud_rune_guards_sin_rng(monkeypatch):
    def _revienta(rng, seq):
        raise AssertionError("el guard debe volver sin consultar el pick")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    # (a) usos agotados
    atacante, guardia, aliado, refuerzo, trait, ctx = _nube_partida()
    _parchea_nube(monkeypatch, decide="si")
    monkeypatch.setattr(rk_mod, "pick", _revienta)
    trait.usos_runa["cloud"] = 0
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert aliado.hp < 70
    assert refuerzo.hp == 30

    # (b) cloud sin conocer
    guardia2 = _pj(level=5, name="Guardia2")
    apply_fighter(guardia2, level=5, fighting_style="Archery")
    apply_rune_knight(guardia2, level=5, runes=("frost", "hill"))
    atacante2 = Monster("Orco", max_hp=60, ac=10, abilities=_abilities(),
                        attacks=[Attack("Hacha", "1d8", ability="str")])
    refuerzo2 = Monster("Goblin", max_hp=30, ac=10, abilities=_abilities())
    aliado2 = _pj(name="Berta")
    ctx2 = _ctx(atacante2, guardia2, aliado2, refuerzo2)
    attack_roll(atacante2, aliado2, atacante2.attacks[0], ctx2.rng,
                log=ctx2.log, ctx=ctx2)
    assert aliado2.hp < 70

    # (c) reacción ya gastada
    trait.usos_runa["cloud"] = rune_uses(5)
    guardia.state.reaction_used = True
    aliado.hp = 70
    refuerzo.hp = 30
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert aliado.hp < 70
    assert trait.usos_runa["cloud"] == rune_uses(5)

    # (d) dueño Incapacitado (sin reacción)
    guardia.state.reaction_used = False
    apply_condition(guardia, Condition.INCAPACITATED, ctx)
    aliado.hp = 70
    refuerzo.hp = 30
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert aliado.hp < 70
    assert trait.usos_runa["cloud"] == rune_uses(5)

    # (e) sin rng: el método se abstiene antes del pick
    assert trait.redirigir_ataque(aliado, atacante, AttackRange.MELEE,
                                  ctx=ctx, rng=None) is None


def test_cloud_rune_el_reset_de_combate_deja_todo_limpio(monkeypatch):
    atacante, guardia, aliado, refuerzo, trait, ctx = _nube_partida()
    _parchea_nube(monkeypatch, decide="si")
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert guardia.state.reaction_used is True
    assert trait.usos_runa["cloud"] == rune_uses(5) - 1
    guardia.reset()
    refuerzo.reset()
    assert guardia.state.reaction_used is False
    assert trait.usos_runa["cloud"] == rune_uses(5)


def test_sin_subclase_la_cloud_rune_no_consulta_rng(monkeypatch):
    def _revienta(*args, **kwargs):
        raise AssertionError("sin la subclase no hay decisiones")

    import dnd_sim.rules.classes.fighter.subclasses.rune_knight.features as rk_mod

    _parchea_nube(monkeypatch, roll_atacante=15)
    monkeypatch.setattr(rk_mod, "pick", _revienta)
    pj = _pj(level=5)
    apply_fighter(pj, level=5, fighting_style="Archery")
    atacante = Monster("Orco", max_hp=60, ac=10, abilities=_abilities(),
                       attacks=[Attack("Hacha", "1d8", ability="str")])
    refuerzo = Monster("Goblin", max_hp=30, ac=10, abilities=_abilities())
    aliado = _pj(name="Socio")
    ctx = _ctx(atacante, pj, aliado, refuerzo)
    assert all(rasgo.__class__.__name__ != "RuneKnightFeatures"
               for rasgo in pj.traits)
    # ``redirigir_ataque`` es walker (SIN entrada en HOOK_NAMES): se
    # comprueba por duck-typing y el motor no lo despacha sin rasgos.
    assert all(not callable(getattr(rasgo, "redirigir_ataque", None))
               for rasgo in pj.traits)
    attack_roll(atacante, aliado, atacante.attacks[0], ctx.rng,
                log=ctx.log, ctx=ctx)
    assert aliado.hp < 70


# --- A12: Master of Runes y cierre --------------------------------------------


def test_master_of_runes_da_cinco_runas_y_dos_usos_desde_el_nivel_15():
    """Master of Runes (15): quinta runa y doble invocación por runa."""
    pj15, trait15 = _invocada("frost", level=15)
    assert len(trait15.runas) == 5
    assert all(trait15.usos_runa[r] == 2 for r in trait15.runas)
    pj14, trait14 = _invocada("frost", level=14)
    assert len(trait14.runas) == 4
    assert all(trait14.usos_runa[r] == 1 for r in trait14.runas)


def test_master_of_runes_registra_las_tres_acciones_de_invocacion():
    pj = _pj(level=15)
    apply_fighter(pj, level=15, fighting_style="Archery")
    apply_rune_knight(pj, level=15,
                      runes=("frost", "hill", "storm", "fire", "cloud"))
    invocadas = [a.runa for a in pj.actions
                 if isinstance(a, RuneInvokeAction)]
    assert invocadas == ["frost", "hill", "storm"]


def test_stone_rune_consume_los_dos_usos_de_master_of_runes(monkeypatch):
    """Con Master of Runes, Stone puede marcar en dos turnos seguidos."""
    pj, trait, enemigo, ctx = _piedra(level=15)
    llamadas = _parchea_fuego(monkeypatch, salva=1)
    trait.on_any_turn_end(enemigo, ctx)
    assert trait.usos_runa["stone"] == 1
    # El daño retira la marca y el próximo turno vuelve a gastar el 2.º uso.
    enemigo.hp = 55
    trait.on_any_turn_start(enemigo, ctx)
    assert enemigo.state.stone_de is None
    trait.on_any_turn_end(enemigo, ctx)
    assert trait.usos_runa["stone"] == 0
    assert enemigo.state.stone_de is pj
    assert len(llamadas) == 2
    # Sin Master of Runes (nivel 5) solo hay una invocación: el segundo
    # turno se niega ANTES del pick.
    pj5, trait5, enemigo5, ctx5 = _piedra()
    llamadas5 = _parchea_fuego(monkeypatch, salva=1)
    trait5.on_any_turn_end(enemigo5, ctx5)
    enemigo5.hp = 55
    trait5.on_any_turn_start(enemigo5, ctx5)
    trait5.on_any_turn_end(enemigo5, ctx5)
    assert trait5.usos_runa["stone"] == 0
    assert len(llamadas5) == 1


def test_rune_knight_integra_en_run_combat_con_semilla_fija():
    from dnd_sim.engine.combat import run_combat

    pj, trait = _invocada("storm", level=15)
    muneco = Monster("Muñeco", max_hp=400, ac=16, abilities=_abilities())
    res = run_combat([pj, muneco], random.Random(7), verbose=True,
                     max_rounds=50)
    # La misma semilla sobre los mismos objetos repite el combate
    # (run_combat llama a reset() al empezar).
    res2 = run_combat([pj, muneco], random.Random(7), verbose=True,
                      max_rounds=50)
    assert res.winner == res2.winner
    assert res.rounds == res2.rounds
    assert res.rounds >= 1
    assert res.action_uses


# --- B: limites del modelo (dato sin efecto) ----------------------------------


def test_la_velocidad_y_el_alcance_son_dato_sin_efecto():
    """Ni Giant's Might ni las runas modelan velocidad ni alcance."""
    pj, trait = _giant_pj()
    GiantsMightAction().execute(_ctx(pj))
    assert trait.giants_might_activo is True
    # Sin sistema de movimiento no hay velocidad (ni velocidad 0).
    assert not hasattr(pj, "speed")
    # Sin reglas de alcance el crecimiento de tamaño no daña más lejos.
    assert all(not hasattr(ataque, "reach") for ataque in pj.attacks)


def test_las_distancias_de_las_runas_son_dato_sin_efecto():
    """Sin geometría los rangos (30 ft, 5 ft) se cumplen siempre."""
    from dnd_sim.core.targeting import valid_targets

    pj, trait = _invocada("cloud")
    enemigo = Monster("Orco", max_hp=60, ac=10, abilities=_abilities())
    ctx = _ctx(pj, enemigo)
    assert not hasattr(pj, "speed")
    assert enemigo in valid_targets(pj, ctx)


def test_las_pruebas_caracteristicas_de_storm_son_dato_sin_efecto():
    """Storm solo da ventaja en ATAQUES: ninguna prueba cambia."""
    from dnd_sim.rules.roll_modifiers import modificar_prueba

    pj, trait = _invocada("storm")
    ctx = _ctx(pj)
    RuneInvokeAction("storm").execute(ctx)
    assert trait.storm_activo is True
    assert modificar_prueba("cha", pj, ctx) == (False, False, 0)


def test_las_runas_despertadas_son_dato_sin_efecto():
    """Sin «runas despertadas» (fuera del sim): solo el pool base."""
    pj, trait = _invocada("frost")
    campos = set(trait.__dataclass_fields__)
    assert not any("despert" in campo for campo in campos)
    assert not any("awaken" in campo for campo in campos)


def test_la_ventaja_de_hill_en_salvaciones_de_veneno_es_dato_sin_efecto():
    """Hill solo da resistencia: la salvación de veneno no cambia."""
    from dnd_sim.rules.roll_modifiers import modificar_salvacion

    pj, trait = _invocada("hill")
    ctx = _ctx(pj)
    assert DamageType.POISON in pj.resistances
    # El motor no distingue el tipo de salvación: sin ventaja (A7).
    assert modificar_salvacion("con", pj, ctx) == (False, False, 0)

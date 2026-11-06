"""Clase Fighter (Guerrero): registro, apply y validaciones de base."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dnd_sim import Abilities, Attack, PlayerCharacter, apply_class
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import FighterFeatures

FIXTURES = Path(__file__).parent / "fixtures"


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=10, wis=12, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Thor", max_hp=80, ac=12, level=5, abilities=_abilities(),
        attacks=[Attack("Hacha de batalla", "1d12", ability="str")],
    )
    defaults.update(kwargs)
    return PlayerCharacter(**defaults)


def _firmas(pj) -> tuple:
    """(rasgos, acciones, salvaciones, habilidades, CA) para comparar."""
    return (
        [type(t).__name__ for t in pj.traits],
        [type(a).__name__ for a in pj.actions],
        set(pj.save_proficiencies),
        set(pj.skill_proficiencies),
        pj.ac,
    )


def test_clase_fighter_esta_registrada_sin_subclases():
    assert "fighter" in CLASSES
    assert CLASSES["fighter"].subclasses == {}


def test_apply_class_fighter_sin_subclase_equivalente_a_apply_fighter():
    a = _pj()
    b = _pj()
    apply_class(a, "fighter")
    apply_fighter(b)
    assert _firmas(a) == _firmas(b)


def test_apply_fighter_anade_el_rasgo_guerrero():
    pj = _pj()
    trait = apply_fighter(pj)
    assert isinstance(trait, FighterFeatures)
    assert trait.level == 5
    assert trait in pj.traits


def test_apply_fighter_asigna_salvaciones_de_fue_y_con():
    pj = _pj()
    apply_fighter(pj)
    assert pj.save_proficiencies == {"str", "con"}


def test_apply_fighter_acepta_las_habilidades_de_la_lista():
    pj = _pj()
    apply_fighter(pj, skills=("Athletics", "perception"))
    assert {"athletics", "perception"} <= pj.skill_proficiencies


def test_apply_fighter_rechaza_habilidades_fuera_de_la_lista():
    with pytest.raises(ValueError, match="no es una habilidad"):
        apply_fighter(_pj(), skills=("stealth",))


def test_subclase_de_fighter_inexistente_da_value_error():
    """La tabla de subclases de fighter está vacía: cualquier clave falla."""
    with pytest.raises(ValueError, match="no es una subclase"):
        apply_class(_pj(), "fighter", "champion")


def test_los_golpes_del_guerrero_suben_en_5_11_y_20():
    from dnd_sim.core.classes import fighter_extra_attacks_for

    esperado = {1: 1, 4: 1, 5: 2, 10: 2, 11: 3, 19: 3, 20: 4}
    assert {lvl: fighter_extra_attacks_for(lvl) for lvl in esperado} == esperado


def test_fighter_features_cubre_los_niveles_1_a_20():
    from dnd_sim.core.classes import FIGHTER_FEATURES

    assert sorted(FIGHTER_FEATURES) == list(range(1, 21))
    assert "Second Wind" in FIGHTER_FEATURES[1]
    assert FIGHTER_FEATURES[20] == ("Three Extra Attacks",)


def test_features_de_clase_coinciden_con_la_fixture():
    from dnd_sim.core.classes import FIGHTER_FEATURES

    datos = json.loads(
        (FIXTURES / "fighter_levels.json").read_text(encoding="utf-8-sig")
    )
    for entrada in datos:
        nivel = int(entrada["level"])
        esperadas = tuple(f["name"] for f in entrada["features"])
        assert FIGHTER_FEATURES[nivel] == esperadas, f"nivel {nivel}"


class _RngMax:
    """RNG de test: siempre el máximo (1d10 → 10)."""

    def randint(self, a: int, b: int) -> int:
        return b

    def random(self) -> float:
        return 1.0


def _ctx(pj, rng=None):
    from types import SimpleNamespace

    return SimpleNamespace(actor=pj, rng=rng or _RngMax(), round=1,
                           resources=None)


def _second_wind(pj):
    from dnd_sim.rules.classes.fighter import SecondWindAction

    return next(a for a in pj.actions
                if isinstance(a, SecondWindAction))


def _trait(pj):
    from dnd_sim.rules.classes.fighter import FighterFeatures

    return next(t for t in pj.traits if isinstance(t, FighterFeatures))


def _fighter(**kwargs):
    """PJ con la clase aplicada (y sin curar por defecto)."""
    pj = _pj(**kwargs)
    apply_fighter(pj)
    return pj


def test_second_wind_cura_d10_mas_nivel_de_guerrero():
    from dnd_sim.core.classes import second_wind_uses

    pj = _fighter(level=5)
    pj.hp = 40
    accion = _second_wind(pj)
    assert accion.can_use(_ctx(pj))
    accion.execute(_ctx(pj))
    assert pj.hp == 40 + 10 + 5  # 1d10 máx + nivel
    uso = _trait(pj).second_wind_usage
    assert uso.uses_max == second_wind_uses(5) == 3
    assert uso.uses_left == 2


def test_second_wind_no_pasa_de_los_pv_maximos():
    pj = _fighter(level=1)
    pj.hp = 75  # 1d10(10) + 1 = 11 > 5 disponibles
    _second_wind(pj).execute(_ctx(pj))
    assert pj.hp == pj.max_hp


def test_second_wind_usos_por_nivel_son_2_3_y_4():
    from dnd_sim.core.classes import second_wind_uses

    assert [second_wind_uses(l) for l in (1, 3, 4, 9, 10, 20)] == [2, 2, 3, 3, 4, 4]
    for lvl, usos in ((1, 2), (5, 3), (12, 4)):
        pj = _fighter(level=lvl)
        pj.hp = 10
        assert _trait(pj).second_wind_usage.uses_max == usos


def test_second_wind_no_es_elegible_a_pg_completos():
    pj = _fighter(level=3)  # a tope: no se ofrece (sin RNG)
    assert not _second_wind(pj).can_use(_ctx(pj))


def test_second_wind_no_es_elegible_sin_usos():
    pj = _fighter(level=1)
    pj.hp = 40
    uso = _trait(pj).second_wind_usage
    uso.spend()
    uso.spend()
    assert not _second_wind(pj).can_use(_ctx(pj))


# --- Oleada de Acción ---------------------------------------------------------

def _action_surge(pj):
    from dnd_sim.rules.classes.fighter import ActionSurgeAction

    return next(a for a in pj.actions
                if isinstance(a, ActionSurgeAction))


def _ctx_recursos(pj, **kwargs):
    from dnd_sim.model.actions import TurnResources

    ctx = _ctx(pj)
    ctx.resources = TurnResources(**kwargs)
    return ctx


def test_action_surge_usos_por_nivel_son_1_y_2():
    from dnd_sim.core.classes import action_surge_uses

    assert [action_surge_uses(l) for l in (1, 2, 16, 17, 20)] == [1, 1, 1, 2, 2]
    for lvl, usos in ((2, 1), (16, 1), (17, 2)):
        pj = _fighter(level=lvl)
        assert _trait(pj).action_surge_usage.uses_max == usos


def test_action_surge_no_existe_en_nivel_1():
    from dnd_sim.rules.classes.fighter import ActionSurgeAction

    pj = _fighter(level=1)
    assert not any(isinstance(a, ActionSurgeAction) for a in pj.actions)
    assert _trait(pj).action_surge_usage is None


def test_action_surge_ejecutada_restaura_la_accion_y_gasta_un_uso():
    pj = _fighter(level=2)
    accion = _action_surge(pj)
    ctx = _ctx_recursos(pj, action_used=True)
    assert accion.can_use(ctx.resources, ctx)
    accion.execute(ctx)
    assert ctx.resources.action_used is False
    assert _trait(pj).surge_used_this_turn is True
    uso = _trait(pj).action_surge_usage
    assert uso.uses_left == uso.uses_max - 1


def test_action_surge_como_maximo_un_vez_por_turno():
    pj = _fighter(level=17)  # 2 usos: así el segundo turno sigue disponible
    accion = _action_surge(pj)
    trait = _trait(pj)
    ctx = _ctx_recursos(pj, action_used=True)
    accion.execute(ctx)
    ctx.resources.action_used = True  # la acción extra del turno ya se gastó
    assert not accion.can_use(ctx.resources, ctx)
    trait.on_turn_start(pj, ctx)  # el límite es por turno, no por combate
    assert accion.can_use(ctx.resources, ctx)


def test_action_surge_no_es_elegible_si_la_accion_no_se_ha_gastado():
    pj = _fighter(level=2)
    ctx = _ctx_recursos(pj)  # action_used=False: nada que restaurar
    assert not _action_surge(pj).can_use(ctx.resources, ctx)


def test_action_surge_no_es_elegible_sin_usos():
    pj = _fighter(level=2)
    ctx = _ctx_recursos(pj, action_used=True)
    uso = _trait(pj).action_surge_usage
    uso.spend()
    assert not _action_surge(pj).can_use(ctx.resources, ctx)


def test_action_surge_no_es_elegible_si_la_bonus_ya_se_gasto():
    pj = _fighter(level=2)
    ctx = _ctx_recursos(pj, action_used=True, bonus_action_used=True)
    assert not _action_surge(pj).can_use(ctx.resources, ctx)


def test_el_encuentro_ejecuta_la_pasada_de_accion_extra_de_la_oleada():
    import random

    from dnd_sim import Monster
    from dnd_sim.engine.combat import run_combat

    pj = _fighter(level=2)  # a PG completos: Tomar Aliento no se ofrece
    enemigo = Monster(name="Muñeco", max_hp=200, ac=10,
                      abilities=_abilities(), attacks=[])
    res = run_combat([pj, enemigo], random.Random(1), verbose=True,
                     max_rounds=1)
    assert res.action_uses.get("Oleada de Acción") == 1
    assert res.action_uses.get("Hacha de batalla", 0) >= 2


# --- Extra Attack -------------------------------------------------------------

def test_extra_attack_sustituye_ataques_por_multiataque():
    from dnd_sim import AttackAction, MultiattackAction
    from dnd_sim.rules.classes.fighter import SecondWindAction

    for lvl, golpes in ((5, 2), (11, 3), (20, 4)):
        pj = _pj(level=lvl)
        assert any(isinstance(a, AttackAction) for a in pj.actions)
        apply_fighter(pj)
        multis = [a for a in pj.actions if isinstance(a, MultiattackAction)]
        assert len(multis) == 1
        assert not any(isinstance(a, AttackAction) for a in pj.actions)
        assert sum(e.count for e in multis[0].options[0]) == golpes
        # Las acciones de clase siguen ahí junto al multiataque.
        assert any(isinstance(a, SecondWindAction) for a in pj.actions)


def test_extra_attack_sin_ataques_no_explota():
    pj = _pj(level=5, attacks=[])
    apply_fighter(pj)  # no lanza
    from dnd_sim import MultiattackAction
    assert not any(isinstance(a, MultiattackAction) for a in pj.actions)


def test_extra_attack_usa_el_atributo_extra_attacks_si_hay_armas():
    pj = _pj(level=11)
    pj.weapons = [Attack("Espada larga", "1d8", ability="str")]
    apply_fighter(pj)
    from dnd_sim import MultiattackAction
    # Con armas equipadas el motor suma desde pj.extra_attacks (2 = 3-1).
    assert pj.extra_attacks == 2
    assert not any(isinstance(a, MultiattackAction) for a in pj.actions)


def test_extra_attack_bajo_el_nivel_5_no_hace_nada():
    from dnd_sim import MultiattackAction

    pj = _pj(level=4)
    apply_fighter(pj)
    assert pj.extra_attacks == 0
    assert not any(isinstance(a, MultiattackAction) for a in pj.actions)


# --- Indomitable ---------------------------------------------------------------

def _save_fallada(dc: int = 15):
    from dnd_sim.core.dice import RollMode
    from dnd_sim.rules.saves import SaveResult

    return SaveResult(ability="str", dc=dc, rolls=[3], bonus=3,
                      total=6, success=False, mode=RollMode.NORMAL)


def _saving_nueva(total: int, success: bool, dc: int):
    from dnd_sim.core.dice import RollMode
    from dnd_sim.rules.saves import SaveResult

    return SaveResult(ability="str", dc=dc, rolls=[total - 2], bonus=2,
                      total=total, success=success, mode=RollMode.NORMAL)


def test_indomitable_usos_por_nivel_son_1_2_y_3():
    from dnd_sim.core.classes import indomitable_uses

    assert [indomitable_uses(l) for l in (1, 8, 9, 12, 13, 16, 17, 20)] == \
        [0, 0, 1, 1, 2, 2, 3, 3]
    for lvl, usos in ((9, 1), (13, 2), (17, 3)):
        pj = _fighter(level=lvl)
        assert _trait(pj).indomitable_usage.uses_max == usos


def test_indomitable_no_existe_por_debajo_del_nivel_9():
    pj = _fighter(level=8)
    assert _trait(pj).indomitable_usage is None


def test_indomitable_repite_la_salvacion_con_bonificador_igual_al_nivel(
        monkeypatch):
    from dnd_sim.rules.classes.fighter import features as fighter_mod

    pj = _fighter(level=9)
    trait = _trait(pj)
    monkeypatch.setattr(fighter_mod, "pick", lambda rng, opciones: "si")
    monkeypatch.setattr(
        fighter_mod, "saving_throw",
        lambda target, ability, dc, rng: _saving_nueva(9, True, dc))
    salida = trait.after_failed_save(pj, "str", _save_fallada(dc=15),
                                     _ctx(pj))
    assert salida is not None
    assert salida.bonus == 2 + 9  # bono del personaje + nivel de Guerrero
    assert salida.total == 9 + 9
    assert salida.success is True
    uso = trait.indomitable_usage
    assert uso.uses_left == uso.uses_max - 1


def test_indomitable_usa_la_nueva_tirada_incluso_si_vuelve_a_fallar(
        monkeypatch):
    from dnd_sim.rules.classes.fighter import features as fighter_mod

    pj = _fighter(level=9)
    trait = _trait(pj)
    monkeypatch.setattr(fighter_mod, "pick", lambda rng, opciones: "si")
    monkeypatch.setattr(
        fighter_mod, "saving_throw",
        lambda target, ability, dc, rng: _saving_nueva(5, False, dc))
    salida = trait.after_failed_save(pj, "str", _save_fallada(dc=20),
                                     _ctx(pj))
    assert salida is not None
    assert salida.total == 5 + 9  # la nueva tirada manda, no la original
    assert salida.success is False
    uso = trait.indomitable_usage
    assert uso.uses_left == uso.uses_max - 1  # el uso se gasta igualmente


def test_indomitable_sin_usos_no_repites_y_no_consume_rng(monkeypatch):
    import random as _random

    from dnd_sim.rules.classes.fighter import features as fighter_mod

    pj = _fighter(level=9)
    trait = _trait(pj)
    trait.indomitable_usage.spend()  # único uso agotado
    llamadas = []

    def _cuenta(rng, opciones):
        llamadas.append(tuple(opciones))
        return "si"

    monkeypatch.setattr(fighter_mod, "pick", _cuenta)
    salida = trait.after_failed_save(pj, "str", _save_fallada(),
                                     _ctx(pj, rng=_random.Random(1)))
    assert salida is None
    assert llamadas == []


def test_indomitable_no_actua_bajo_el_nivel_9(monkeypatch):
    from dnd_sim.rules.classes.fighter import features as fighter_mod

    pj = _fighter(level=8)  # se crea ANTES de parchear pick (el estilo la usa)
    llamadas = []
    monkeypatch.setattr(
        fighter_mod, "pick", lambda rng, opciones: llamadas.append(1) or "si")
    assert _trait(pj).after_failed_save(pj, "str", _save_fallada(),
                                        _ctx(pj)) is None
    assert llamadas == []


def test_indomitable_reset_de_usos_en_combate_nuevo():
    pj = _fighter(level=13)
    trait = _trait(pj)
    trait.indomitable_usage.spend()
    trait.reset()
    assert trait.indomitable_usage.uses_left == 2


# --- Ataques Estudiados ---------------------------------------------------------

def _mods():
    from types import SimpleNamespace

    return SimpleNamespace(advantage_sources=[], disadvantage_sources=[])


def _objetivo(nombre: str):
    from types import SimpleNamespace

    return SimpleNamespace(name=nombre)


def test_ataques_estudiados_da_ventaja_contra_el_objetivo_tras_un_fallo():
    pj = _fighter(level=13)
    trait = _trait(pj)
    enemigo = _objetivo("Bribón")
    trait.after_attack_roll(pj, enemigo, None, False, ctx=_ctx(pj))
    mods = _mods()
    trait.modify_attack_modifiers(mods, pj, enemigo, None, ctx=_ctx(pj))
    assert mods.advantage_sources == ["Ataques Estudiados"]


def test_ataques_estudiados_es_por_objetivo():
    pj = _fighter(level=13)
    trait = _trait(pj)
    a, b = _objetivo("A"), _objetivo("B")
    trait.after_attack_roll(pj, a, None, False, ctx=_ctx(pj))
    mods = _mods()
    trait.modify_attack_modifiers(mods, pj, b, None, ctx=_ctx(pj))
    assert mods.advantage_sources == []


def test_ataques_estudiados_no_marca_si_el_ataque_acierta():
    pj = _fighter(level=13)
    trait = _trait(pj)
    trait.after_attack_roll(pj, _objetivo("A"), None, True, ctx=_ctx(pj))
    assert trait.ataques_estudiados == {}


def test_ataques_estudiados_solo_da_ventaja_en_el_siguiente_ataque():
    pj = _fighter(level=13)
    trait = _trait(pj)
    enemigo = _objetivo("A")
    trait.after_attack_roll(pj, enemigo, None, False, ctx=_ctx(pj))
    primero = _mods()
    trait.modify_attack_modifiers(primero, pj, enemigo, None, ctx=_ctx(pj))
    segundo = _mods()
    trait.modify_attack_modifiers(segundo, pj, enemigo, None, ctx=_ctx(pj))
    assert primero.advantage_sources == ["Ataques Estudiados"]
    assert segundo.advantage_sources == []


def test_ataques_estudiados_caduca_al_final_del_siguiente_turno():
    pj = _fighter(level=13)
    trait = _trait(pj)
    enemigo = _objetivo("A")
    trait.after_attack_roll(pj, enemigo, None, False, ctx=_ctx(pj))
    trait.on_turn_start(pj, _ctx(pj))  # turno propio siguiente: sigue
    mods = _mods()
    trait.modify_attack_modifiers(mods, pj, enemigo, None, ctx=_ctx(pj))
    assert mods.advantage_sources == ["Ataques Estudiados"]
    # Marca de nuevo y deja pasar dos turnos: caduca.
    trait.after_attack_roll(pj, enemigo, None, False, ctx=_ctx(pj))
    trait.on_turn_start(pj, _ctx(pj))
    trait.on_turn_start(pj, _ctx(pj))
    mods = _mods()
    trait.modify_attack_modifiers(mods, pj, enemigo, None, ctx=_ctx(pj))
    assert mods.advantage_sources == []


def test_ataques_estudiados_no_actua_bajo_el_nivel_13():
    pj = _fighter(level=12)
    trait = _trait(pj)
    enemigo = _objetivo("A")
    trait.after_attack_roll(pj, enemigo, None, False, ctx=_ctx(pj))
    assert trait.ataques_estudiados == {}
    mods = _mods()
    trait.modify_attack_modifiers(mods, pj, enemigo, None, ctx=_ctx(pj))
    assert mods.advantage_sources == []


def test_ataques_estudiados_no_actua_si_el_atacante_no_es_el_dueno():
    pj = _fighter(level=13)
    trait = _trait(pj)
    otro = _objetivo("Intruso")
    trait.after_attack_roll(otro, _objetivo("A"), None, False, ctx=_ctx(pj))
    assert trait.ataques_estudiados == {}


# --- Estilos de Combate --------------------------------------------------------

def test_estilo_de_combate_se_elige_con_pick_al_crear_el_pj():
    import random

    from dnd_sim.core.classes import FIGHTER_STYLES

    a = _pj()
    apply_fighter(a, rng=random.Random(7))
    assert _trait(a).estilo in FIGHTER_STYLES
    b = _pj()
    apply_fighter(b, rng=random.Random(7))
    assert _trait(b).estilo == _trait(a).estilo  # misma semilla = mismo estilo


def test_estilo_de_combate_explícito_se_respeta():
    pj = _pj()
    apply_fighter(pj, fighting_style="Dueling")
    assert _trait(pj).estilo == "Dueling"


def test_estilo_de_combate_invalido_da_value_error():
    # «Protection» es ahora un estilo válido (A5): se prueba con uno inventado.
    with pytest.raises(ValueError, match="no es un Estilo de Combate"):
        apply_fighter(_pj(), fighting_style="Estilo inventado")


def test_apply_class_reenvía_el_estilo_de_combate():
    pj = _pj()
    apply_class(pj, "fighter", fighting_style="Defense")
    assert _trait(pj).estilo == "Defense"
    assert pj.ac == 13  # 12 base +1 de Defense


def test_estilo_defense_sube_la_ca_en_uno():
    pj = _pj()
    assert pj.ac == 12
    apply_fighter(pj, fighting_style="Defense")
    assert pj.ac == 13


def test_estilo_dueling_suma_dos_daño_en_cuerpo_a_cuerpo():
    from dnd_sim.core.enums import AttackRange

    pj = _pj()
    apply_fighter(pj, fighting_style="Dueling")
    trait = _trait(pj)
    enemigo = _objetivo("A")
    one_handed = Attack("Espada corta", "1d6", ability="str")
    two_handed = Attack("Hacha a dos manos", "1d12", ability="str",
                        properties={"two-handed"})
    dano = trait.extra_attack_damage(pj, enemigo, AttackRange.MELEE,
                                     atk=one_handed)
    assert dano == 2
    # A distancia no aplica Dueling.
    assert trait.extra_attack_damage(pj, enemigo, AttackRange.RANGED,
                                     atk=one_handed) == 0
    # Con arma a dos manos no aplica.
    assert trait.extra_attack_damage(pj, enemigo, AttackRange.MELEE,
                                     atk=two_handed) == 0


def test_estilo_thrown_weapon_fighting_suma_dos_daño_con_arma_arrojadiza():
    from dnd_sim.core.enums import AttackRange

    pj = _pj()
    apply_fighter(pj, fighting_style="Thrown Weapon Fighting")
    trait = _trait(pj)
    enemigo = _objetivo("A")
    dardo = Attack("Dardo", "1d4", ability="str",
                   properties={"thrown", "range"})
    assert trait.extra_attack_damage(pj, enemigo, AttackRange.RANGED,
                                     atk=dardo) == 2
    assert trait.extra_attack_damage(pj, enemigo, AttackRange.RANGED,
                                     atk=Attack("Arco", "1d8",
                                                ability="dex")) == 0


def test_extra_attack_damage_no_actúa_si_el_atacante_no_es_el_dueno():
    pj = _pj()
    apply_fighter(pj, fighting_style="Dueling")
    trait = _trait(pj)
    otro = _objetivo("Intruso")
    atk = Attack("Espada corta", "1d6", ability="str")
    assert trait.extra_attack_damage(otro, _objetivo("A"), None, atk=atk) == 0


def test_archery_suma_dos_a_la_tirada_a_distancia():
    from dnd_sim.core.enums import AttackRange
    from dnd_sim.rules.roll_modifiers import attack_modifiers

    pj = _pj()
    apply_fighter(pj, fighting_style="Archery")
    enemigo = _objetivo("A")
    atk = Attack("Arco largo", "1d8", ability="dex")
    a_distancia = attack_modifiers(pj, enemigo, atk, AttackRange.RANGED)
    assert a_distancia.bonus == 2
    cuerpo_a_cuerpo = attack_modifiers(pj, enemigo, atk, AttackRange.MELEE)
    assert cuerpo_a_cuerpo.bonus == 0


def test_archery_no_aplica_a_otro_estilo():
    from dnd_sim.core.enums import AttackRange
    from dnd_sim.rules.roll_modifiers import attack_modifiers

    pj = _pj()
    apply_fighter(pj, fighting_style="Defense")
    mods = attack_modifiers(pj, _objetivo("A"),
                            Attack("Arco largo", "1d8", ability="dex"),
                            AttackRange.RANGED)
    assert mods.bonus == 0


def test_archery_permite_acertar_donde_sin_el_bonus_se_fallaria(monkeypatch):
    import random

    from dnd_sim import Monster
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.core.enums import AttackRange
    from dnd_sim.engine.combat import attack as atk_mod

    pj = _pj()
    apply_fighter(pj, fighting_style="Archery")
    atk = Attack("Arco largo", "1d8", ability="dex",
                 range_type=AttackRange.RANGED)
    # d20 fijo en 10: con +2 de Archery entra; sin él, no.
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=10, rolls=[10],
                                    mode=RollMode.NORMAL))
    bonus = pj.to_hit(atk)
    enemigo = Monster(name="Muñeco", max_hp=30, ac=bonus + 11,
                      abilities=_abilities(), attacks=[])
    atk_mod.attack_roll(pj, enemigo, atk, random.Random(1))
    assert enemigo.hp < enemigo.max_hp  # el +2 decidió el impacto


# --- Great Weapon Fighting -----------------------------------------------------

class _RngBajo:
    """RNG de test: siempre el mínimo (1d12 → 1)."""

    def randint(self, a: int, b: int) -> int:
        return a

    def random(self) -> float:
        return 0.0


def test_roll_dice_con_piso_cuenta_los_dados_bajos_como_el_piso():
    from dnd_sim.core.dice import roll_dice

    rng = _RngBajo()
    assert roll_dice("2d6", rng) == 2
    assert roll_dice("2d6", _RngBajo(), floor=3) == 6  # 1,1 → 3,3


def test_gwf_devuelve_tres_en_golpes_con_arma_a_dos_manos():
    from dnd_sim.core.enums import AttackRange

    pj = _pj()
    apply_fighter(pj, fighting_style="Great Weapon Fighting")
    trait = _trait(pj)
    dos_manos = Attack("Hacha a dos manos", "1d12", ability="str",
                       properties={"two-handed", "heavy"})
    assert trait.damage_dice_upgrades(pj, dos_manos,
                                      AttackRange.MELEE) == 3
    # No a distancia, ni con arma a una mano, ni con otro estilo.
    assert trait.damage_dice_upgrades(pj, dos_manos,
                                      AttackRange.RANGED) == 0
    assert trait.damage_dice_upgrades(
        pj, Attack("Espada corta", "1d6", ability="str"),
        AttackRange.MELEE) == 0
    otro = _pj()
    apply_fighter(otro, fighting_style="Defense")
    assert _trait(otro).damage_dice_upgrades(otro, dos_manos,
                                             AttackRange.MELEE) == 0


def test_el_motor_pasa_el_piso_de_gwf_a_roll_dice(monkeypatch):
    import random

    from dnd_sim import Monster
    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.core.enums import AttackRange
    from dnd_sim.engine.combat import attack as atk_mod

    pj = _pj()
    apply_fighter(pj, fighting_style="Great Weapon Fighting")
    atk = Attack("Hacha a dos manos", "1d12", ability="str",
                 properties={"two-handed", "heavy"})
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=15, rolls=[15],
                                    mode=RollMode.NORMAL))
    piso = []
    original = atk_mod.roll_dice

    def _espia(expr, rng, crit=False, floor=None):
        piso.append(floor)
        return original(expr, rng, crit=crit, floor=floor)

    monkeypatch.setattr(atk_mod, "roll_dice", _espia)
    enemigo = Monster(name="Muñeco", max_hp=60, ac=20,
                      abilities=_abilities(), attacks=[])
    atk_mod.attack_roll(pj, enemigo, atk, random.Random(1))
    assert piso == [3]  # 1d12 de un solo golpe, con el piso de GWF


# --- Maestría con Armas ---------------------------------------------------------

def test_maestria_con_armas_cuenta_segun_el_nivel():
    from dnd_sim.core.classes import weapon_mastery_count

    esperado = {1: 3, 3: 3, 4: 4, 9: 4, 10: 5, 15: 5, 16: 6, 20: 6}
    assert {lvl: weapon_mastery_count(lvl) for lvl in esperado} == esperado


def test_maestria_con_armas_elige_las_armas_del_pj_como_dato():
    pj = _pj()  # sin weapons: pool de ataques
    apply_fighter(pj)
    assert _trait(pj).maestrias == ["Hacha de batalla"]


def test_maestria_con_armas_elige_armas_distintas_hasta_el_maximo():
    pj = _pj()
    pj.weapons = [Attack(f"Arma{i}", "1d6", ability="str") for i in range(6)]
    apply_fighter(pj)  # nivel 5 → 4 elegibles de 6
    maestrias = _trait(pj).maestrias
    assert len(maestrias) == 4
    assert len(set(maestrias)) == 4
    assert set(maestrias) <= {a.name for a in pj.weapons}


def test_maestria_con_armas_con_menos_armas_que_el_maximo_elige_todas():
    pj = _pj()
    pj.weapons = [Attack("Daga", "1d4", ability="str"),
                  Attack("Espada larga", "1d8", ability="str")]
    apply_fighter(pj, level=1)  # 3 elegibles, solo 2 armas
    assert sorted(_trait(pj).maestrias) == ["Daga", "Espada larga"]


def test_maestria_con_armas_sin_armas_da_lista_vacia():
    pj = _pj(attacks=[])
    apply_fighter(pj)
    assert _trait(pj).maestrias == []


def test_plantilla_de_guerrero_de_main_usa_la_clase_fighter():
    import main

    guerrero = main._build_party(1)[0]
    assert any(isinstance(t, FighterFeatures) for t in guerrero.traits)
    assert guerrero.save_proficiencies == {"str", "con"}


# --- Tactical Mind (2) ----------------------------------------------------------

class _RngSi:
    """RNG de test: pick → última opción («si») y d10 → 10."""

    def randint(self, a: int, b: int) -> int:
        return b

    def randrange(self, n: int) -> int:
        return n - 1

    def random(self) -> float:
        return 1.0


def _check_fallada(dc: int = 15, total: int = 6, ability: str = "str"):
    from dnd_sim.core.dice import RollMode
    from dnd_sim.rules.checks import CheckResult

    return CheckResult(
        ability=ability, dc=dc, rolls=[total - 3], bonus=3, total=total,
        success=total >= dc, mode=RollMode.NORMAL, skill=None)


def test_tactical_mind_suma_d10_y_gasta_un_uso_si_la_tirada_final_pasa():
    pj = _fighter(level=2)
    pj.hp = 40
    rasgo = _trait(pj)
    usage = rasgo.second_wind_usage
    antes = usage.uses_left
    ctx = _ctx(pj, _RngSi())  # pick → «si», d10 → 10: 6+10=16 ≥ CD 15

    salida = rasgo.after_failed_check(pj, "str", _check_fallada(15, 6), ctx)

    assert salida.success and salida.total == 16
    assert 10 in salida.rolls
    assert usage.uses_left == antes - 1


def test_tactical_mind_no_gasta_el_uso_si_aun_asi_falla():
    pj = _fighter(level=2)
    pj.hp = 40
    rasgo = _trait(pj)
    usage = rasgo.second_wind_usage
    ctx = _ctx(pj, _RngSi())  # d10 → 10: 2+10=12 < CD 30

    salida = rasgo.after_failed_check(pj, "str", _check_fallada(30, 2), ctx)

    assert salida is not None and salida.total == 12
    assert not salida.success
    assert usage.uses_left == usage.uses_max


def test_tactical_mind_sin_usos_no_actua_y_no_consume_rng(monkeypatch):
    pj = _fighter(level=2)
    pj.hp = 40
    rasgo = _trait(pj)
    rasgo.second_wind_usage.uses_left = 0
    ctx = _ctx(pj, _RngSi())
    llamadas = []

    import dnd_sim.rules.classes.fighter.features as mod

    original = mod.pick
    monkeypatch.setattr(mod, "pick",
                        lambda *a, **k: (llamadas.append(1), original(*a, **k))[1])
    salida = rasgo.after_failed_check(pj, "str", _check_fallada(), ctx)

    assert salida is None
    assert llamadas == []


def test_tactical_mind_sin_ctx_no_actua():
    pj = _fighter(level=2)
    pj.hp = 40
    rasgo = _trait(pj)
    antes = rasgo.second_wind_usage.uses_left

    salida = rasgo.after_failed_check(pj, "str", _check_fallada(), None)

    assert salida is None
    assert rasgo.second_wind_usage.uses_left == antes


def test_tactical_mind_no_actua_en_salvaciones():
    import random

    from dnd_sim.rules.saves import saving_throw

    pj = _fighter(level=2)
    pj.hp = 40
    rasgo = _trait(pj)
    antes = rasgo.second_wind_usage.uses_left

    saving_throw(pj, "con", 30, random.Random(1), ctx=_ctx(pj))

    assert rasgo.second_wind_usage.uses_left == antes


def test_el_gancho_after_failed_check_desde_ability_check_con_ctx():
    from dnd_sim.rules.traits.base import hooks

    pj = _fighter(level=2)
    pj.hp = 40
    rasgo = _trait(pj)
    assert any(hooks(pj.traits, "after_failed_check"))
    assert rasgo.second_wind_usage.available

    class _RngSecuencia:
        """d20 → 1 (falla), pick → «si», d10 → 10."""

        def __init__(self):
            self._valores = [1, 10]
            self._i = 0

        def randint(self, a: int, b: int) -> int:
            v = self._valores[self._i] if self._i < len(self._valores) else b
            self._i += 1
            return v

        def randrange(self, n: int) -> int:
            return n - 1

        def random(self) -> float:
            return 1.0

    from dnd_sim.rules.checks import ability_check

    rng = _RngSecuencia()
    antes = rasgo.second_wind_usage.uses_left
    salida = ability_check(pj, "str", 20, rng, ctx=_ctx(pj, rng))
    # d20=1 (falla) → hook gana el +1d10=10; si aún así falla, no gasta.
    assert salida.rolls == [1, 10]
    assert salida.total == 1 + salida.bonus + 10
    assert not salida.success
    assert rasgo.second_wind_usage.uses_left == antes


# --- Maestría asignada a los ataques (A3) --------------------------------

_ARMAS_MAESTRIA = [
    "Espada larga", "Daga", "Arco corto", "Hacha de batalla",
    "Lanza", "Maza", "Martillo de guerra", "Estoque",
]


def _pj_con_armas(n: int = 8, **kwargs) -> PlayerCharacter:
    pj = _pj(**kwargs)
    pj.weapons = [Attack(nombre, "1d8", ability="str")
                  for nombre in _ARMAS_MAESTRIA[:n]]
    return pj


def test_maestria_asignada_al_ataque_elegido_recibe_su_clave():
    pj = _pj()
    apply_fighter(pj)  # "Hacha de batalla" es la única elección
    atk = pj.attacks[0]
    assert _trait(pj).maestrias == ["Hacha de batalla"]
    assert atk.mastery == "topple"


def test_maestria_no_eligida_no_recibe_clave():
    from dnd_sim.rules.mastery import maestria_de

    pj = _pj_con_armas()
    apply_fighter(pj, level=1)  # 3 de 8 armas
    elegidas = set(_trait(pj).maestrias)
    for atk in pj.weapons:
        esperada = maestria_de(atk.name) if atk.name in elegidas else ""
        assert atk.mastery == esperada, atk.name
    assert sum(1 for a in pj.weapons if a.mastery) == 3


def test_maestria_asignada_cuenta_3_4_5_6_segun_el_nivel():
    esperado = {1: 3, 4: 4, 10: 5, 16: 6}
    for nivel, cuenta in esperado.items():
        pj = _pj_con_armas()
        apply_fighter(pj, level=nivel)
        asignadas = sum(1 for a in pj.weapons if a.mastery)
        assert asignadas == cuenta, f"nivel {nivel}"
        assert len(_trait(pj).maestrias) == cuenta


def test_maestria_de_armas_sin_entrada_en_la_tabla_no_explota():
    pj = _pj(attacks=[Attack("Arma rara", "1d6", ability="str")])
    apply_fighter(pj, level=1)  # elegida (única) pero sin tabla
    assert _trait(pj).maestrias == ["Arma rara"]
    assert pj.attacks[0].mastery == ""


# --- Tactical Master (9) -------------------------------------------------------

class _RngExplota:
    """RNG que revienta si se consume (para probar «sin RNG»)."""

    def randint(self, a: int, b: int) -> int:
        raise AssertionError("no debería consumir RNG")

    def randrange(self, n: int) -> int:
        raise AssertionError("no debería consumir RNG")

    def random(self) -> float:
        raise AssertionError("no debería consumir RNG")


def test_tactical_master_no_sustituye_bajo_el_nivel_9():
    pj = _fighter(level=8)
    rasgo = _trait(pj)

    assert rasgo.sustituir_maestria("sap", _RngExplota()) == "sap"


def test_tactical_master_nivel_9_elige_entre_original_push_sap_slow():
    pj = _fighter(level=9)
    rasgo = _trait(pj)

    class _RngElegido:
        def randrange(self, n: int) -> int:
            return min(self.idx, n - 1)

        def randint(self, a: int, b: int) -> int:
            return b

        def random(self) -> float:
            return 1.0

    opciones = set()
    for idx in range(4):
        rng = _RngElegido()
        rng.idx = idx
        opciones.add(rasgo.sustituir_maestria("topple", rng))
    assert opciones == {"topple", "push", "sap", "slow"}


def test_tactical_master_sin_rng_devuelve_la_propiedad_original():
    pj = _fighter(level=20)
    rasgo = _trait(pj)

    assert rasgo.sustituir_maestria("vex", None) == "vex"


def test_resolver_maestria_sin_maestria_no_consulta_tactical_master():
    from dnd_sim.rules.mastery import resolver_maestria

    pj = _fighter(level=9)
    arma = Attack("Espada larga", "1d8", ability="str", mastery="")

    assert resolver_maestria(pj, arma, _RngExplota()) == ""


def test_la_sustitucion_de_tactical_master_solo_dura_ese_ataque():
    from dnd_sim.rules.mastery import resolver_maestria

    pj = _fighter(level=9)
    arma = Attack("Espada larga", "1d8", ability="str", mastery="sap")

    class _RngUltimo:
        def randrange(self, n: int) -> int:
            return n - 1

        def randint(self, a: int, b: int) -> int:
            return b

        def random(self) -> float:
            return 1.0

    assert resolver_maestria(pj, arma, _RngUltimo()) == "slow"
    assert arma.mastery == "sap"  # el objeto no cambia


# --- Protection / Interception (reacción) (A5) ---------------------------------

def _aliado(pj, nombre: str = "Aliado"):
    from types import SimpleNamespace

    return SimpleNamespace(name=nombre, alive=True,
                           combatant_type=pj.combatant_type)


def _enemigo(nombre: str = "Enemigo"):
    from types import SimpleNamespace

    # Sin combatant_type: is_hostile_to lo trata como bando distinto.
    return SimpleNamespace(name=nombre, alive=True)


def _con_estilo(estilo: str, **kwargs) -> PlayerCharacter:
    pj = _pj()
    apply_fighter(pj, fighting_style=estilo, **kwargs)
    return pj


def test_protection_impone_desventaja_al_atacante_contra_un_aliado():
    pj = _con_estilo("Protection", tiene_escudo=True)
    mods = _mods()

    _trait(pj).grant_attack_modifiers(
        mods, _enemigo(), _aliado(pj), None, ctx=None, rng=_RngSi())

    assert "Protección" in mods.disadvantage_sources
    assert pj.state.reaction_used


def test_protection_sin_escudo_no_actúa_y_no_consume_rng():
    pj = _con_estilo("Protection")  # tiene_escudo=False por defecto
    mods = _mods()

    _trait(pj).grant_attack_modifiers(
        mods, _enemigo(), _aliado(pj), None, ctx=None, rng=_RngExplota())

    assert mods.disadvantage_sources == []
    assert not pj.state.reaction_used


def test_protection_no_actúa_con_la_reacción_gastada():
    pj = _con_estilo("Protection", tiene_escudo=True)
    pj.state.reaction_used = True
    mods = _mods()

    _trait(pj).grant_attack_modifiers(
        mods, _enemigo(), _aliado(pj), None, ctx=None, rng=_RngSi())

    assert mods.disadvantage_sources == []


def test_protection_no_actúa_contra_un_no_aliado_ni_con_el_mismo_pj():
    pj = _con_estilo("Protection", tiene_escudo=True)
    mods = _mods()
    rasgo = _trait(pj)

    rasgo.grant_attack_modifiers(
        mods, _enemigo(), _enemigo("Bando distinto"), None,
        ctx=None, rng=_RngExplota())
    rasgo.grant_attack_modifiers(
        mods, _enemigo(), pj, None, ctx=None, rng=_RngExplota())

    assert mods.disadvantage_sources == []
    assert not pj.state.reaction_used


def test_protection_sin_rng_no_actúa():
    pj = _con_estilo("Protection", tiene_escudo=True)
    mods = _mods()

    _trait(pj).grant_attack_modifiers(
        mods, _enemigo(), _aliado(pj), None, ctx=None, rng=None)

    assert mods.disadvantage_sources == []
    assert not pj.state.reaction_used


def test_las_dos_reacciones_de_protection_no_se_acumulan_en_una_ronda():
    pj = _con_estilo("Protection", tiene_escudo=True)
    mods = _mods()
    rasgo = _trait(pj)
    kwargs = dict(ctx=None, rng=_RngSi())

    rasgo.grant_attack_modifiers(mods, _enemigo(), _aliado(pj), None, **kwargs)
    rasgo.grant_attack_modifiers(mods, _enemigo(), _aliado(pj), "B", **kwargs)

    assert mods.disadvantage_sources == ["Protección"]  # solo la primera
    assert pj.state.reaction_used


def test_interception_reduce_el_daño_al_aliado_con_1d10_mas_pb():
    pj = _con_estilo("Interception")  # sin escudo: bastan sus ataques
    ctx = _ctx(pj, _RngSi())  # pick → «si», d10 → 10; PB nivel 5 = 3 → 13

    restante = _trait(pj).reduce_damage_to_allies(
        _aliado(pj), 20, ctx=ctx)

    assert restante == 7  # 20 − (10 + 3)
    assert pj.state.reaction_used


def test_interception_con_un_aliado_no_baja_de_cero_el_daño():
    pj = _con_estilo("Interception")
    ctx = _ctx(pj, _RngSi())

    restante = _trait(pj).reduce_damage_to_allies(
        _aliado(pj), 5, ctx=ctx)

    assert restante == 0  # mínimo 0, aunque la reducción sea mayor
    assert pj.state.reaction_used


def test_interception_sin_arma_ni_escudo_no_actúa_y_no_consume_rng():
    pj = _pj(attacks=[])
    apply_fighter(pj, fighting_style="Interception")
    ctx = _ctx(pj, _RngExplota())

    restante = _trait(pj).reduce_damage_to_allies(
        _aliado(pj), 20, ctx=ctx)

    assert restante is None
    assert not pj.state.reaction_used


def test_interception_no_actúa_con_la_reacción_gastada():
    pj = _con_estilo("Interception")
    pj.state.reaction_used = True
    ctx = _ctx(pj, _RngSi())

    assert _trait(pj).reduce_damage_to_allies(_aliado(pj), 20, ctx=ctx) is None


def test_interception_no_actúa_contra_un_no_aliado_ni_con_el_mismo_pj():
    pj = _con_estilo("Interception")
    rasgo = _trait(pj)
    ctx = _ctx(pj, _RngExplota())

    assert rasgo.reduce_damage_to_allies(
        _enemigo("Bando distinto"), 20, ctx=ctx) is None
    assert rasgo.reduce_damage_to_allies(pj, 20, ctx=ctx) is None
    assert not pj.state.reaction_used


def test_interception_sin_rng_no_actúa():
    from types import SimpleNamespace

    pj = _con_estilo("Interception")
    ctx = SimpleNamespace(actor=pj, rng=None)

    assert _trait(pj).reduce_damage_to_allies(
        _aliado(pj), 20, ctx=ctx) is None
    assert not pj.state.reaction_used

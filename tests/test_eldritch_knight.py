"""Tests de la subclase Eldritch Knight (Caballero Sobrenatural, PHB 2024).

Solo cubren lo que existe: en A1, las tablas de ``core/classes.py``; en
A2, el esqueleto, el registro, la equivalencia de vías y los datos sin
efecto; el resto de pasos se van añadiendo aquí.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

from dnd_sim import Abilities, Attack, Monster, PlayerCharacter, apply_class
from dnd_sim.core.classes import (
    eldritch_knight_cantrips,
    eldritch_knight_prepared,
)
from dnd_sim.data.spell_parser import parse_spell
from dnd_sim.engine.combat import run_combat
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import (
    ELDRITCH_KNIGHT_SPELLS,
    EldritchKnightFeatures,
    apply_eldritch_knight,
)
from dnd_sim.rules.conditions import Condition
from dnd_sim.rules.spells import PJSpellAction, Spellcasting, hechizo_soportado

SPELLS = Path(__file__).parent / "fixtures" / "spells"


# --- A1: tablas --------------------------------------------------------------


def test_la_tabla_de_hechizos_preparados_coincide_con_el_phb():
    esperado = {
        3: 3, 4: 4, 5: 4, 6: 4, 7: 5, 8: 6, 9: 6, 10: 7, 11: 8,
        12: 8, 13: 9, 14: 10, 15: 10, 16: 11, 17: 11, 18: 11,
        19: 12, 20: 13,
    }
    for nivel, valor in esperado.items():
        assert eldritch_knight_prepared(nivel) == valor, nivel


def test_eldritch_knight_prepared_es_cero_por_debajo_del_nivel_3():
    assert eldritch_knight_prepared(1) == 0
    assert eldritch_knight_prepared(2) == 0


def test_eldritch_knight_cantrips_es_cero_dos_o_tres():
    assert eldritch_knight_cantrips(1) == 0
    assert eldritch_knight_cantrips(2) == 0
    assert eldritch_knight_cantrips(3) == 2
    assert eldritch_knight_cantrips(9) == 2
    assert eldritch_knight_cantrips(10) == 3
    assert eldritch_knight_cantrips(20) == 3


# --- A2: esqueleto, registro y vías ------------------------------------------ #


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Aldric", max_hp=30, ac=16, level=3,
        abilities=Abilities(str=16, dex=14, con=16, int=16, wis=12, cha=10),
        attacks=[Attack("Espada larga", "1d8", ability="str")],
    )
    defaults.update(kwargs)
    return PlayerCharacter(**defaults)


def _lista():
    """Pool de prueba: todas las fixtures soportadas por el motor (sin red)."""
    out = []
    for ruta in sorted(SPELLS.glob("*.json")):
        spell = parse_spell(json.loads(ruta.read_text(encoding="utf-8")),
                            "EK", Spellcasting(level=5))
        if spell is not None and hechizo_soportado(spell):
            out.append(spell)
    return out


def _spell(index: str):
    """Hechizo de fixture por índice (los kwargs explícitos quieren Spell)."""
    return next(s for s in _lista() if getattr(s, "index", None) == index)


def test_eldritch_knight_esta_registrado_con_tercio_int_y_lista_wizard():
    sub = CLASSES["fighter"].subclasses.get("eldritch_knight")
    assert sub is not None
    assert sub.class_name == "fighter"
    assert sub.min_level == 3
    assert sub.spellcasting is ELDRITCH_KNIGHT_SPELLS
    assert ELDRITCH_KNIGHT_SPELLS.progresion == "third"
    assert ELDRITCH_KNIGHT_SPELLS.caracteristica == "int"
    assert ELDRITCH_KNIGHT_SPELLS.lista_clase == "wizard"
    assert ELDRITCH_KNIGHT_SPELLS.escuelas is None
    from dnd_sim import EldritchKnightFeatures as Facade
    assert Facade is EldritchKnightFeatures


def test_apply_class_y_apply_eldritch_knight_construyen_el_mismo_lanzador():
    lista = _lista()
    pj1 = _pj()
    apply_class(pj1, "fighter", "eldritch_knight", level=3, lista=lista)
    pj2 = _pj()
    apply_fighter(pj2, level=3)
    apply_eldritch_knight(pj2, level=3, lista=lista)
    assert pj1.spell_slots.maximos == pj2.spell_slots.maximos == (2,)
    assert pj1.spellcasting_pc.trucos == pj2.spellcasting_pc.trucos
    assert pj1.spellcasting_pc.preparados == pj2.spellcasting_pc.preparados
    assert len(pj1.spellcasting_pc.preparados) == 3
    assert len(pj1.spellcasting_pc.trucos) == 2
    assert any(isinstance(t, EldritchKnightFeatures) for t in pj1.traits)
    assert any(isinstance(t, EldritchKnightFeatures) for t in pj2.traits)
    assert len(pj1.actions) == len(pj2.actions)


def test_aplicar_sin_guerrero_o_con_nivel_inferior_a_3_es_error():
    import pytest

    with pytest.raises(ValueError):
        apply_eldritch_knight(_pj(), level=3, lista=_lista())
    pj = _pj()
    apply_fighter(pj, level=3)
    with pytest.raises(ValueError):
        apply_eldritch_knight(pj, level=2, lista=_lista())


def test_espacios_y_conteos_de_hechizos_por_nivel_3_7_y_19():
    for nivel, espacios, preparados, trucos in (
        (3, (2,), 3, 2),
        (7, (4, 2), 5, 2),
        (19, (4, 3, 3, 1), 12, 3),
    ):
        pj = _pj(level=nivel)
        apply_fighter(pj, level=nivel)
        apply_eldritch_knight(pj, level=nivel, lista=_lista())
        assert pj.spell_slots.maximos == espacios, nivel
        assert len(pj.spellcasting_pc.preparados) == preparados, nivel
        assert len(pj.spellcasting_pc.trucos) == trucos, nivel


def test_kwargs_de_preparacion_invalidos_son_error():
    import pytest

    pj = _pj()
    apply_fighter(pj, level=3)
    with pytest.raises(ValueError):
        # Truco: magic-missile no está en el pool de trucos.
        apply_eldritch_knight(pj, level=3, lista=_lista(),
                              cantrips=[_spell("magic-missile")])
    pj2 = _pj()
    apply_fighter(pj2, level=3)
    with pytest.raises(ValueError):
        # Nivel 3 solo tiene espacio de nivel 1: fireball es inalcanzable.
        apply_eldritch_knight(pj2, level=3, lista=_lista(),
                              spells=[_spell("fireball")])


def test_war_bond_y_arcane_charge_son_datos_sin_efecto():
    pj = _pj()
    apply_fighter(pj, level=3)
    trait = apply_eldritch_knight(pj, level=3, lista=_lista())
    assert trait.war_bond is True
    assert trait.arcane_charge is True


def test_sin_la_subclase_no_hay_espacios_ni_acciones_de_hechizo():
    pj = _pj()
    apply_fighter(pj, level=3)
    assert pj.spell_slots is None
    assert getattr(pj, "spellcasting_pc", None) is None
    assert not any(isinstance(t, EldritchKnightFeatures) for t in pj.traits)
    assert not any(getattr(a, "es_accion_magia", False) for a in pj.actions)


# --- A3: lanzamiento extremo a extremo --------------------------------------- #


def _ek(nivel: int = 3, *, spells=(), cantrips=()):
    """EK de prueba: fighter + subclase con la lista de fixtures.

    ``spells``/``cantrips`` son índices de fixture (se parsean a Spell).
    """
    pj = _pj(level=nivel)
    apply_fighter(pj, level=nivel, rng=random.Random(0))
    apply_eldritch_knight(
        pj, level=nivel, lista=_lista(),
        spells=[_spell(i) for i in spells] or None,
        cantrips=[_spell(i) for i in cantrips] or None)
    return pj


def _orco(hp: int = 100) -> Monster:
    return Monster(name="Orco", max_hp=hp, ac=12, abilities=Abilities(),
                   attacks=[])


def _ctx(actor, otros=(), rng=None) -> CombatContext:
    return CombatContext(
        rng=rng if rng is not None else random.Random(1), actor=actor,
        combatants=[actor, *otros], round=1, log=[], verbose=False,
        resources=TurnResources())


def test_ek_nivel_3_lanza_un_hechizo_de_nivel_1_en_combate_y_gasta_un_espacio():
    ek = _ek(3, spells=["magic-missile"])
    hechizo = next(a for a in ek.actions
                   if isinstance(a, PJSpellAction) and a.spell.level > 0)
    vistas: list[list[str]] = []

    def policy(ctx):
        if ctx.actor is not ek:
            return ctx.available_actions[0] if ctx.available_actions else None
        vistas.append([a.name for a in ctx.available_actions])
        return hechizo if len(vistas) == 1 else ctx.available_actions[0]

    r = run_combat([ek, _orco()], random.Random(4), policy=policy)
    assert hechizo.name in vistas[0]
    assert hechizo.name in r.action_uses
    assert sum(r.spell_slots_spent.values()) == 1
    assert ek.spell_slots.actuales == [1]


def test_la_cd_y_el_ataque_de_hechizo_del_ek_usan_inteligencia():
    ek = _ek(3)
    sc = ek.spellcasting_pc.sc
    assert sc.ability_mod == 3          # INT 16 → +3
    assert sc.save_dc == 13             # 8 + PB 2 + 3
    assert sc.attack_bonus == 5         # PB 2 + 3


def test_un_ek_lanza_un_truco_sin_gastar_espacio_en_combate():
    ek = _ek(3, cantrips=["fire-bolt"])
    truco = next(a for a in ek.actions
                 if isinstance(a, PJSpellAction) and a.spell.level == 0)
    vistas: list[list[str]] = []

    def policy(ctx):
        if ctx.actor is not ek:
            return ctx.available_actions[0] if ctx.available_actions else None
        vistas.append([a.name for a in ctx.available_actions])
        return truco if len(vistas) == 1 else ctx.available_actions[0]

    r = run_combat([ek, _orco()], random.Random(4), policy=policy)
    assert truco.name in vistas[0]
    assert truco.name in r.action_uses
    assert sum(r.spell_slots_spent.values()) == 0
    assert sum(ek.spell_slots.actuales) == sum(ek.spell_slots.maximos)


def test_ek_nivel_10_con_sobrecarga_elige_espacio_sup_con_pick():
    ek = _ek(10, spells=["burning-hands"])
    accion = next(a for a in ek.actions
                  if isinstance(a, PJSpellAction) and a.spell.level > 0)
    rng = random.Random(0)
    gastados: set[int] = set()
    for _ in range(40):
        ek.spell_slots.reset()
        antes = list(ek.spell_slots.actuales)
        accion.execute(_ctx(ek, [_orco()], rng=rng))
        for nivel, (b, a) in enumerate(
                zip(antes, ek.spell_slots.actuales), start=1):
            if a < b:
                gastados.add(nivel)
    # Nivel 10: la tabla tercio da espacios de nivel 1-2; la sobrecarga
    # (pick uniforme) usa los dos con la semilla 0.
    assert gastados == {1, 2}
    # La sobrecarga escala el daño con la regla común (damage_at_slot_level).
    assert (accion.construir(2).effect.effect.damage
            != accion.construir(1).effect.effect.damage)


def test_ek_lanza_un_hechizo_de_concentracion_y_queda_concentrando():
    ek = _ek(3, spells=["faerie-fire"])
    conc = next(a for a in ek.actions
                if isinstance(a, PJSpellAction) and a.spell.concentration)
    vistas: list[list[str]] = []

    def policy(ctx):
        if ctx.actor is not ek:
            return ctx.available_actions[0] if ctx.available_actions else None
        vistas.append([a.name for a in ctx.available_actions])
        return conc if len(vistas) == 1 else ctx.available_actions[0]

    r = run_combat([ek, _orco(hp=10)], random.Random(4), policy=policy)
    assert conc.name in r.action_uses
    assert sum(r.spell_slots_spent.values()) == 1
    # Combate corto (<10 rondas): la concentración de faerie-fire (1 min)
    # sigue vigente al final.
    assert ek.conditions.has(Condition.CONCENTRATION)


def test_la_oleada_de_accion_del_ek_no_lanza_hechizos():
    ek = _ek(3, spells=["magic-missile"])
    hechizo = next(a for a in ek.actions
                   if isinstance(a, PJSpellAction) and a.spell.level > 0)
    oleada = next(a for a in ek.actions if a.name == "Oleada de Acción")
    vistas: list[list[str]] = []

    def policy(ctx):
        if ctx.actor is not ek:
            return ctx.available_actions[0] if ctx.available_actions else None
        vistas.append([a.name for a in ctx.available_actions])
        n = len(vistas)
        if n == 1:      # 1ª pasada (acción): lanzo el hechizo
            return hechizo
        if n == 2:      # bonus: la Oleada restaura la acción
            return oleada
        if n == 3:      # pasada extra: SIN hechizos de PJ
            assert hechizo not in ctx.available_actions
            assert all(not getattr(a, "es_accion_magia", False)
                       for a in ctx.available_actions)
        return ctx.available_actions[0]

    r = run_combat([ek, _orco()], random.Random(4), policy=policy)
    assert hechizo.name in vistas[0]
    assert "Oleada de Acción" in vistas[1]
    assert hechizo.name not in vistas[2]
    assert hechizo.name in vistas[3]     # la ronda 2 vuelve a verlo
    assert sum(r.spell_slots_spent.values()) == 1

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
from dnd_sim.model.actions import (
    CombatContext,
    MultiattackAction,
    TurnResources,
    _sustituir_ataque_por_hechizo,
)
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


def _ek(nivel: int = 3, *, spells=None, cantrips=None):
    """EK de prueba: fighter + subclase con la lista de fixtures.

    ``spells``/``cantrips`` son índices de fixture (se parsean a Spell).
    ``None`` = muestreo por defecto; lista vacía = sin hechizos/trucos.
    """
    pj = _pj(level=nivel)
    apply_fighter(pj, level=nivel, rng=random.Random(0))
    apply_eldritch_knight(
        pj, level=nivel, lista=_lista(),
        spells=None if spells is None else [_spell(i) for i in spells],
        cantrips=None if cantrips is None else [_spell(i) for i in cantrips])
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


# --- A4: War Magic ------------------------------------------------------------


class _RngEspia:
    """rng de test: guiona ``randrange`` y registra cada ``n`` visto.

    El resto es neutro: ``random()=1.0`` (fuera utilitaria y Temerario),
    ``randint(1, 20)=15`` (impacta) y ``randint(1, n)=1`` con n != 20
    (dados de daño bajos). Sin guion, ``randrange`` devuelve 0.
    """

    def __init__(self, guion=()):
        self._guion = list(guion)
        self.ns: list[int] = []

    def randrange(self, n):
        self.ns.append(n)
        if self._guion:
            valor = self._guion.pop(0)
            assert 0 <= valor < n, f"guion {valor} fuera de rango para {n}"
            return valor
        return 0

    def randint(self, a, b):
        return 15 if b == 20 else a

    def random(self):
        return 1.0


class _RngQueExplota:
    """Cualquier consumo de RNG revienta el test."""

    def __getattr__(self, nombre):
        raise AssertionError(f"no debía consumirse RNG: {nombre}")


def _trait(pj):
    return next(t for t in pj.traits if isinstance(t, EldritchKnightFeatures))


def test_war_magic_sustituye_un_ataque_por_un_truco_y_consume_ese_ataque():
    ek = _ek(7, cantrips=["fire-bolt"], spells=["magic-missile"])
    victima = _orco(hp=100)
    rng = _RngEspia(guion=[1, 0])   # 1er ataque: «sí»; 2º: «no»
    ctx = _ctx(ek, [victima], rng=rng)
    multi = next(a for a in ek.actions if isinstance(a, MultiattackAction))
    multi.execute(ctx)
    lineas = [str(l) for l in ctx.log]
    assert sum("con Fire Bolt" in l for l in lineas) == 1
    assert sum("con Espada larga" in l for l in lineas) == 1
    # El truco (nivel 0) no gasta espacio.
    assert tuple(ek.spell_slots.actuales) == ek.spell_slots.maximos


def test_war_magic_sin_trucos_no_es_elegible_y_no_consume_rng():
    ek = _ek(7, cantrips=[], spells=["magic-missile"])
    ctx = _ctx(ek, [_orco()], rng=_RngQueExplota())
    ctx.in_attack_action = True
    assert _trait(ek).sustituir_ataque_por_hechizo(2, ctx) is None


def test_war_magic_en_nivel_6_no_actua():
    ek = _ek(6, cantrips=["fire-bolt"])
    ctx = _ctx(ek, [_orco()], rng=_RngQueExplota())
    ctx.in_attack_action = True
    assert _trait(ek).sustituir_ataque_por_hechizo(2, ctx) is None


def test_war_magic_no_se_ofrece_en_reacciones_ni_fuera_de_la_accion_atacar():
    ek = _ek(7, cantrips=["fire-bolt"])
    ctx = _ctx(ek, [_orco()], rng=_RngQueExplota())
    ctx.in_attack_action = True
    ctx.is_reaction = True
    assert _trait(ek).sustituir_ataque_por_hechizo(2, ctx) is None
    ctx.is_reaction = False
    ctx.in_attack_action = False       # ataque adicional o bonus
    assert _trait(ek).sustituir_ataque_por_hechizo(2, ctx) is None


def test_el_truco_sustituido_usa_la_cd_y_el_escalado_del_pj():
    ek = _ek(7, cantrips=["fire-bolt"], spells=["magic-missile"])
    ctx = _ctx(ek, [_orco()], rng=_RngEspia(guion=[1]))
    ctx.in_attack_action = True
    accion, coste = _trait(ek).sustituir_ataque_por_hechizo(2, ctx)
    assert coste == 1
    assert accion.spell.name == "Fire Bolt"
    assert accion.caster.sc.attack_bonus == 6     # PB 3 (nivel 7) + INT 3
    assert accion.caster.sc.save_dc == 14
    interno = accion.construir(None)
    assert "2d10" in str(interno.effect.attack.damage)   # escala a nivel 7


def test_sin_la_subclase_el_punto_de_consulta_no_consume_rng():
    pj = _pj(level=7)
    apply_fighter(pj, level=7)
    ctx = _ctx(pj, [_orco()], rng=_RngQueExplota())
    ctx.in_attack_action = True
    assert _sustituir_ataque_por_hechizo(pj, 2, ctx) is None


# --- A5: Improved War Magic ---------------------------------------------------


def test_improved_war_magic_solo_es_elegible_con_dos_ataques_restantes():
    ek = _ek(18, cantrips=["fire-bolt"], spells=["magic-missile"])
    rng = _RngEspia(guion=[0])
    ctx = _ctx(ek, [_orco()], rng=rng)
    ctx.in_attack_action = True
    assert _trait(ek).sustituir_ataque_por_hechizo(1, ctx) is None
    assert rng.ns == [2]   # solo «no»/«truco»: sin opción de hechizo


def test_improved_war_magic_consume_dos_ataques_y_gasta_un_espacio():
    ek = _ek(18, cantrips=["fire-bolt"], spells=["magic-missile"])
    victima = _orco(hp=100)
    # Guion: consulta1 (n=3) elige «hechizo», la sobrecarga del PJ
    # elige slot 1 (n=3), consulta2 (n=2) «no». El 2º ataque lo
    # consume el coste 2 (sin consulta).
    rng = _RngEspia(guion=[2, 0, 0])
    ctx = _ctx(ek, [victima], rng=rng)
    multi = next(a for a in ek.actions if isinstance(a, MultiattackAction))
    multi.execute(ctx)
    lineas = [str(l) for l in ctx.log]
    assert sum("con Espada larga" in l for l in lineas) == 1
    assert sum(ek.spell_slots.maximos) - sum(ek.spell_slots.actuales) == 1
    assert any("Magic Missile" in l for l in lineas)


def test_improved_war_magic_no_ofrece_hechizos_de_nivel_3_o_superior():
    ek = _ek(18, cantrips=["fire-bolt"], spells=["fireball"])
    rng = _RngEspia(guion=[0])
    ctx = _ctx(ek, [_orco()], rng=rng)
    ctx.in_attack_action = True
    assert _trait(ek).sustituir_ataque_por_hechizo(3, ctx) is None
    assert rng.ns == [2]   # fireball (nivel 3) no entra en las opciones


def test_pick_unico_sobre_las_opciones_equiprobables():
    ek = _ek(18, cantrips=["fire-bolt"], spells=["magic-missile"])
    rng = _RngEspia(guion=[2])
    ctx = _ctx(ek, [_orco()], rng=rng)
    ctx.in_attack_action = True
    accion, coste = _trait(ek).sustituir_ataque_por_hechizo(3, ctx)
    # Un solo randrange(3): «no»/«truco»/«hechizo» equiprobables; el
    # grupo de hechizos tiene 1 → sin segundo RNG.
    assert rng.ns == [3]
    assert coste == 2
    assert accion.spell.name == "Magic Missile"


def test_sin_espacios_el_hechizo_no_es_elegible():
    ek = _ek(18, cantrips=["fire-bolt"], spells=["magic-missile"])
    ek.spell_slots.actuales[:] = [0] * len(ek.spell_slots.actuales)
    rng = _RngEspia(guion=[1])
    ctx = _ctx(ek, [_orco()], rng=rng)
    ctx.in_attack_action = True
    accion, coste = _trait(ek).sustituir_ataque_por_hechizo(3, ctx)
    assert coste == 1          # solo queda la opción de truco
    assert rng.ns == [2]
    assert accion.spell.level == 0


def test_en_nivel_17_improved_war_magic_no_actua():
    ek = _ek(17, cantrips=["fire-bolt"], spells=["magic-missile"])
    rng = _RngEspia(guion=[0])
    ctx = _ctx(ek, [_orco()], rng=rng)
    ctx.in_attack_action = True
    assert _trait(ek).sustituir_ataque_por_hechizo(3, ctx) is None
    assert rng.ns == [2]   # sin opción «hechizo» a nivel 17

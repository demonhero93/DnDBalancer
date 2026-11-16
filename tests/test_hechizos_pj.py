"""Hechizos de PJ: espacios, preparación y lanzamiento (sesión 1).

Los datos de hechizos salen de fixtures JSON (sin red); los PJ de prueba
se construyen a mano. Una clase falsa SOLO de test ejercita el registro.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import pytest

from dnd_sim import Abilities, Attack, Monster, PlayerCharacter
from dnd_sim.core.spellcasting import (
    FULL_SLOTS, HALF_SLOTS, THIRD_SLOTS, SpellSlots, SpellcastingDef,
    spell_slots_for,
)
from dnd_sim.data.spell_parser import parse_spell
from dnd_sim.model.actions import ActionType, CombatContext, TurnResources
from dnd_sim.rules.conditions import Condition, apply_condition
from dnd_sim.rules.spells import (
    PCSpellcasting, PJSpellAction, Spellcasting, aplicar_lanzamiento,
    construir_acciones, estadisticas_lanzador, hechizo_soportado,
    preparar_hechizos,
)

FIXTURES = Path(__file__).parent / "fixtures"
SPELLS = FIXTURES / "spells"


# --- A1: tablas de espacios ------------------------------------------------ #

def test_la_tabla_de_lanzador_total_coincide_con_el_phb():
    assert FULL_SLOTS[1] == (2,)
    assert FULL_SLOTS[3] == (4, 2)
    assert FULL_SLOTS[7] == (4, 3, 3, 1)
    assert FULL_SLOTS[17] == (4, 3, 3, 3, 2, 1, 1, 1, 1)
    assert FULL_SLOTS[18] == (4, 3, 3, 3, 3, 1, 1, 1, 1)
    assert FULL_SLOTS[20] == (4, 3, 3, 3, 3, 2, 2, 1, 1)
    assert len(FULL_SLOTS) == 20


def test_la_tabla_de_semilanzador_coincide_con_el_phb():
    assert HALF_SLOTS[1] == (2,)
    assert HALF_SLOTS[5] == (4, 2)
    assert HALF_SLOTS[9] == (4, 3, 2)
    assert HALF_SLOTS[13] == (4, 3, 3, 1)
    assert HALF_SLOTS[20] == (4, 3, 3, 3, 2)
    assert len(HALF_SLOTS) == 20


def test_la_tabla_de_tercio_empieza_en_el_nivel_3():
    assert 1 not in THIRD_SLOTS
    assert 2 not in THIRD_SLOTS
    assert THIRD_SLOTS[3] == (2,)
    assert THIRD_SLOTS[7] == (4, 2)
    assert THIRD_SLOTS[16] == (4, 3, 3)
    assert THIRD_SLOTS[20] == (4, 3, 3, 1)
    assert len(THIRD_SLOTS) == 18


def test_spell_slots_for_devuelve_la_tupla_sin_ceros_finales():
    assert spell_slots_for("full", 3) == (4, 2)
    assert spell_slots_for("half", 5) == (4, 2)
    assert spell_slots_for("third", 19) == (4, 3, 3, 1)


def test_spell_slots_for_sin_espacios_por_debajo_del_minimo():
    assert spell_slots_for("third", 1) == ()
    assert spell_slots_for("third", 2) == ()


def test_spell_slots_for_con_progresión_desconocida_es_un_value_error():
    with pytest.raises(ValueError):
        spell_slots_for("pact", 5)


def test_spellcastingdef_valida_la_progresión_y_expone_espacios():
    d = SpellcastingDef(progresion="THIRD", caracteristica="Int",
                        lista_clase="wizard", min_level=3)
    assert d.progresion == "third"
    assert d.caracteristica == "int"
    assert d.escuelas is None
    assert d.espacios(2) == ()          # por debajo de min_level
    assert d.espacios(3) == (2,)
    with pytest.raises(ValueError):
        SpellcastingDef(progresion="pact", caracteristica="cha",
                        lista_clase="warlock")


# --- A2: SpellSlots en el combatiente --------------------------------------- #

def test_un_truco_no_gasta_espacio_y_un_hechizo_de_nivel_1_si():
    slots = SpellSlots((4, 2))
    assert slots.can_cast(0)             # truco: siempre
    slots.spend(1)
    assert slots.actuales == [3, 2]
    assert slots.can_cast(0)             # seguir lanzando trucos: sin gasto
    assert slots.can_cast(1)


def test_al_agotar_un_nivel_las_ofertas_superiores_siguen_disponibles():
    slots = SpellSlots((4, 3, 2))
    for _ in range(4):
        slots.spend(1)
    assert slots.actuales == [0, 3, 2]
    # Sobrecarga: un hechizo de nivel 1 sigue siendo lanzable con un
    # espacio de nivel >= 1, y la oferta son los niveles superiores.
    assert slots.can_cast(1)
    assert slots.niveles_disponibles(1) == [2, 3]
    for _ in range(3):
        slots.spend(2)
    for _ in range(2):
        slots.spend(3)
    assert not slots.can_cast(1)
    assert slots.niveles_disponibles(1) == []


def test_gastar_un_espacio_agotado_es_un_value_error():
    slots = SpellSlots((1,))
    slots.spend(1)
    with pytest.raises(ValueError):
        slots.spend(1)


def test_reset_rellena_los_espacios_igual_que_al_crearlos():
    slots = SpellSlots((4, 2))
    slots.spend(1)
    slots.spend(1)
    slots.spend(2)
    slots.reset()
    assert slots.actuales == [4, 2]


def test_un_combatiente_sin_lanzamiento_no_tiene_espacios_y_reset_es_inofensivo():
    from dnd_sim import Abilities, Combatant
    c = Combatant(name="Pij", max_hp=10, ac=10, abilities=Abilities(),
                  attacks=[])
    assert c.spell_slots is None
    c.reset()                            # no debe fallar ni tocar nada


def test_combatant_reset_restaura_los_espacios_del_pj_lanzador():
    from dnd_sim import Abilities, Combatant
    c = Combatant(name="Mago", max_hp=10, ac=10, abilities=Abilities(),
                  attacks=[])
    c.spell_slots = SpellSlots((4, 2))
    c.spell_slots.spend(1)
    c.hp = 3
    c.reset()
    assert c.spell_slots.actuales == [4, 2]
    assert c.hp == 10


# --- A3: lista de hechizos de clase (capa data) ----------------------------- #

def _get_spell_fixture(index: str) -> dict:
    """Cargador de hechizos sin red: lee la fixture JSON del índice."""
    ruta = SPELLS / f"{index}.json"
    if not ruta.exists():
        raise FileNotFoundError(index)
    return json.loads(ruta.read_text(encoding="utf-8"))


def test_la_lista_de_clase_se_parsea_con_nivel_y_escuela():
    from dnd_sim.data.class_spells import load_class_spell_list
    lista = load_class_spell_list("wizard", cache_dir=FIXTURES / "classes",
                                  get_spell=_get_spell_fixture)
    por_indice = {s.index: s for s in lista}
    fireball = por_indice["fireball"]
    assert (fireball.level, fireball.school) == (3, "evocation")
    assert por_indice["ray-of-frost"].level == 0
    assert por_indice["hold-person"].level == 2
    # No modelados (utilidad, PV temporales) y el inexistente: fuera.
    for fuera in ("shield", "mage-hand", "jump", "false-life",
                  "nonexistent-spell"):
        assert fuera not in por_indice


def test_un_hechizo_que_no_existe_se_omite_sin_romper_la_lista():
    from dnd_sim.data.class_spells import load_class_spell_list

    def _get(index: str) -> dict:
        if index == "fireball":
            raise FileNotFoundError(index)
        return _get_spell_fixture(index)

    lista = load_class_spell_list("wizard", cache_dir=FIXTURES / "classes",
                                  get_spell=_get)
    indices = {s.index for s in lista}
    assert "fireball" not in indices
    assert "magic-missile" in indices


def test_la_lista_se_guarda_en_cache_y_la_segunda_vez_no_toca_la_red(
        tmp_path, monkeypatch):
    import urllib.request
    from dnd_sim.data.class_spells import load_class_spell_list

    fixture = json.loads(
        (FIXTURES / "classes" / "wizard.json").read_text(
            encoding="utf-8"))

    class _Respuesta:
        def __init__(self, data):
            self._d = data

        def read(self):
            return json.dumps(self._d).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    llamadas: list[str] = []

    def _falsa_red(url, timeout=None):
        llamadas.append(str(url))
        return _Respuesta(fixture)

    monkeypatch.setattr(urllib.request, "urlopen", _falsa_red)
    lista1 = load_class_spell_list("wizard", cache_dir=tmp_path,
                                   get_spell=_get_spell_fixture)
    assert llamadas and (tmp_path / "wizard.json").exists()

    def _sin_red(*args, **kwargs):
        raise AssertionError("no debe tocar la red")

    monkeypatch.setattr(urllib.request, "urlopen", _sin_red)
    lista2 = load_class_spell_list("wizard", cache_dir=tmp_path,
                                   get_spell=_get_spell_fixture)
    assert [s.index for s in lista1] == [s.index for s in lista2]


# --- A4: componente de lanzamiento de PJ ------------------------------------ #

def _pj_lanzador(hp: int = 200) -> PlayerCharacter:
    """INT 16 (+3) y PB 2 fijos (``level`` None: no se rederiva la PB)."""
    return PlayerCharacter(
        name="Mago", max_hp=hp, ac=12,
        abilities=Abilities(int=16, dex=14, con=12, wis=10, cha=8),
        proficiency=2, attacks=[])


def _enemigo(hp: int = 60) -> Monster:
    return Monster(name="Orco", max_hp=hp, ac=12, abilities=Abilities(),
                   attacks=[])


def _ctx(actor, otros=(), rng=None) -> CombatContext:
    return CombatContext(
        rng=rng if rng is not None else random.Random(1), actor=actor,
        combatants=[actor, *otros], round=1, log=[], verbose=False,
        resources=TurnResources())


def _hechizo(index: str, nivel_lanzador: int = 5):
    """Hechizo de fixture parseado como lo haría la lista de clase."""
    return parse_spell(_get_spell_fixture(index), "Test",
                       Spellcasting(level=nivel_lanzador))


def _caster(pj, slots, trucos=(), preparados=(), nivel: int = 5):
    return PCSpellcasting(
        ability="int", level=nivel,
        sc=estadisticas_lanzador(pj, "int", nivel), slots=slots,
        trucos=list(trucos), preparados=list(preparados))


def test_un_hechizo_de_nivel_1_gasta_un_espacio_y_el_truco_no():
    pj = _pj_lanzador()
    orco = _enemigo()
    slots = SpellSlots((2, 1))
    caster = _caster(pj, slots, trucos=[_hechizo("fire-bolt")],
                     preparados=[_hechizo("magic-missile")], nivel=3)
    truco, nivel1 = construir_acciones(caster)
    ctx = _ctx(pj, [orco])
    assert truco.can_use(ctx.resources, ctx)
    assert nivel1.can_use(ctx.resources, ctx)
    truco.execute(ctx)
    assert slots.actuales == [2, 1]          # el truco no gasta nada
    nivel1.execute(ctx)
    assert slots.actuales == [1, 1]          # el de nivel 1 sí


def test_la_sobrecarga_elige_entre_los_espacios_disponibles_con_pick():
    pj = _pj_lanzador()
    orco = _enemigo()
    slots = SpellSlots((1, 1))
    caster = _caster(pj, slots, preparados=[_hechizo("magic-missile")],
                     nivel=3)
    accion = construir_acciones(caster)[0]
    rng = random.Random(0)
    gastados: set[int] = set()
    for _ in range(40):
        slots.reset()
        antes = list(slots.actuales)
        accion.execute(_ctx(pj, [orco], rng=rng))
        for nivel, (b, a) in enumerate(zip(antes, slots.actuales), start=1):
            if a < b:
                gastados.add(nivel)
    # Con la semilla 0 los 40 repartos usan los DOS niveles disponibles.
    assert gastados == {1, 2}


def test_la_sobrecarga_con_un_espacio_superior_escalada_el_dano():
    pj = _pj_lanzador()
    slots = SpellSlots((2, 1))
    caster = _caster(pj, slots, preparados=[_hechizo("burning-hands")],
                     nivel=3)
    accion = construir_acciones(caster)[0]
    assert accion.construir().effect.effect.damage == "3d6"
    assert accion.construir(2).effect.effect.damage == "4d6"


def test_sin_espacios_no_es_elegible_y_no_toca_el_rng():
    class _RngExplota:
        def randrange(self, *args, **kwargs):
            raise AssertionError("no debe consumir RNG")

    pj = _pj_lanzador()
    orco = _enemigo()
    slots = SpellSlots((1,))
    slots.spend(1)
    caster = _caster(pj, slots, preparados=[_hechizo("magic-missile")],
                     nivel=3)
    accion = construir_acciones(caster)[0]
    ctx = _ctx(pj, [orco], rng=_RngExplota())
    assert accion.can_use(ctx.resources, ctx) is False
    accion.execute(ctx)                       # vuelve sin tocar el rng
    assert slots.actuales == [0]


def test_la_cd_del_pj_es_8_mas_pb_mas_mod_y_el_ataque_pb_mas_mod():
    pj = _pj_lanzador()                       # INT 16 (+3), PB 2
    sc = estadisticas_lanzador(pj, "int", 5)
    assert sc.save_dc == 13                   # 8 + 2 + 3
    assert sc.attack_bonus == 5               # 2 + 3
    assert sc.ability_mod == 3
    # La acción interna usa la CD/bonificador del PJ, no los del monstruo.
    slots = SpellSlots((2,))
    caster = _caster(pj, slots,
                     preparados=[_hechizo("burning-hands"),
                                 _hechizo("fire-bolt")], nivel=3)
    a_save, a_atk = construir_acciones(caster)
    assert a_save.construir().effect.effect.dc == 13
    assert a_atk.construir().effect.attack.attack_bonus == 5


def test_los_trucos_escalan_por_el_nivel_del_personaje():
    fire_bolt = _hechizo("fire-bolt", nivel_lanzador=5)
    assert fire_bolt.damage == "2d10"          # umbral 5 del nivel 1/5/11/17
    pj = _pj_lanzador()
    orco = _enemigo()
    slots = SpellSlots((2,))
    caster = _caster(pj, slots, trucos=[fire_bolt], nivel=5)
    accion = construir_acciones(caster)[0]
    ctx = _ctx(pj, [orco])
    assert accion.can_use(ctx.resources, ctx)
    accion.execute(ctx)
    assert slots.actuales == [2]              # el truco no gasta espacio
    assert accion.construir().effect.attack.damage == "2d10"


def test_un_hechizo_concentrado_solo_deja_una_concentracion_y_otro_la_termina():
    pj = _pj_lanzador()
    orco = _enemigo()
    slots = SpellSlots((4, 2))
    caster = _caster(pj, slots,
                     preparados=[_hechizo("faerie-fire"),
                                 _hechizo("hold-person")], nivel=3)
    primero, segundo = construir_acciones(caster)
    ctx = _ctx(pj, [orco])
    primero.execute(ctx)
    assert pj.conditions.has(Condition.CONCENTRATION)
    segundo.execute(ctx)                       # lanzar otro la termina
    conc = [i for i in pj.conditions.instances
            if i.condition is Condition.CONCENTRATION]
    assert len(conc) == 1


def test_la_salvacion_de_constitucion_al_recibir_dano_rompe_la_concentracion():
    pj = _pj_lanzador(hp=200)
    orco = _enemigo()
    slots = SpellSlots((4, 2))
    caster = _caster(pj, slots, preparados=[_hechizo("faerie-fire")],
                     nivel=3)
    accion = construir_acciones(caster)[0]
    ctx = _ctx(pj, [orco])
    accion.execute(ctx)
    assert pj.conditions.has(Condition.CONCENTRATION)
    # 60 de daño → CD 30: inalcanzable con CON +1, falla SIEMPRE.
    from dnd_sim.rules.damage import inflict_damage
    inflict_damage(pj, 60, "fire", source=orco, ctx=ctx, rng=ctx.rng,
                   magical=True)
    assert pj.hp == 140
    assert not pj.conditions.has(Condition.CONCENTRATION)


def test_la_concentracion_se_pierde_al_quedar_incapacitado():
    pj = _pj_lanzador()
    orco = _enemigo()
    slots = SpellSlots((4, 2))
    caster = _caster(pj, slots, preparados=[_hechizo("faerie-fire")],
                     nivel=3)
    accion = construir_acciones(caster)[0]
    ctx = _ctx(pj, [orco])
    accion.execute(ctx)
    assert pj.conditions.has(Condition.CONCENTRATION)
    apply_condition(pj, Condition.STUNNED, ctx, duration_rounds=10)
    assert not pj.conditions.has(Condition.CONCENTRATION)


def test_la_concentracion_se_pierde_al_morir():
    pj = _pj_lanzador()
    orco = _enemigo()
    slots = SpellSlots((4, 2))
    caster = _caster(pj, slots, preparados=[_hechizo("faerie-fire")],
                     nivel=3)
    accion = construir_acciones(caster)[0]
    accion.execute(_ctx(pj, [orco]))
    assert pj.conditions.has(Condition.CONCENTRATION)
    pj.mark_dead()
    assert not pj.conditions.has(Condition.CONCENTRATION)


def test_los_hechizos_de_bonus_action_y_reaccion_no_entran_en_el_pool():
    assert hechizo_soportado(_hechizo("fireball")) is True
    assert hechizo_soportado(_hechizo("hellish-rebuke")) is False  # reacción
    assert hechizo_soportado(_hechizo("healing-word")) is False    # bonus
    assert hechizo_soportado(_hechizo("shield")) is False          # sin efecto
    assert hechizo_soportado(_hechizo("jump")) is False            # movimiento
    assert hechizo_soportado(_hechizo("detect-magic")) is False    # ritual
    assert hechizo_soportado(None) is False


def test_un_monstruo_con_hechizos_conserva_sus_resultados_con_semilla_fija():
    """El camino de monstruo (CD/bonificador de ficha) queda intacto."""
    from dnd_sim.data.loader import load_monster
    from dnd_sim.engine.combat import run_combat
    lich = load_monster("lich")
    victima = PlayerCharacter(name="Victima", max_hp=60, ac=12,
                              abilities=Abilities(dex=10), attacks=[])
    r = run_combat([lich, victima], random.Random(3))
    assert r.winner == "NPC"
    assert r.rounds == 2
    assert r.survivors == {"Victima": 0, "Lich": 135}
    assert r.action_uses == {"Paralyzing Touch": 2}


# --- A5: preparación de hechizos -------------------------------------------- #

def _def_a5(**kwargs) -> SpellcastingDef:
    base = dict(progresion="third", caracteristica="int", lista_clase="wizard",
                trucos_conocidos={3: 2, 5: 3, 7: 3},
                preparados={3: 2, 5: 2, 7: 2}, min_level=3)
    base.update(kwargs)
    return SpellcastingDef(**base)


def _lista(*indices: str):
    return [_hechizo(i) for i in indices]


def test_la_preparacion_alcanza_los_conteos_de_la_tabla():
    lista = _lista("fire-bolt", "ray-of-frost", "guidance",
                   "magic-missile", "burning-hands", "thunderwave")
    trucos, hech = preparar_hechizos(lista, 5, _def_a5())
    assert len(trucos) == 3          # trucos_conocidos[5] = 3
    assert len(hech) == 2            # preparados[5] = 2
    assert all(s.level == 0 for s in trucos)
    assert all(s.level == 1 for s in hech)   # mayor espacio en nivel 5 = 1


def test_un_hechizo_sobre_el_mayor_espacio_no_es_preparable():
    lista = _lista("fireball", "hold-person", "magic-missile")
    _, hech5 = preparar_hechizos(lista, 5, _def_a5())   # espacios (3,): máx 1
    assert [s.index for s in hech5] == ["magic-missile"]
    _, hech7 = preparar_hechizos(lista, 7, _def_a5())   # espacios (4,2): máx 2
    assert {s.index for s in hech7} == {"hold-person", "magic-missile"}


def test_la_preparacion_es_determinista_con_la_semilla_por_defecto():
    lista = _lista("fire-bolt", "ray-of-frost", "guidance",
                   "magic-missile", "burning-hands", "thunderwave")
    a = preparar_hechizos(lista, 5, _def_a5())
    b = preparar_hechizos(lista, 5, _def_a5())
    assert [s.index for s in a[0]] == [s.index for s in b[0]]
    assert [s.index for s in a[1]] == [s.index for s in b[1]]


def test_un_hechizo_fuera_de_la_lista_es_un_value_error():
    lista = _lista("magic-missile")
    fuera = _hechizo("lightning-bolt")
    with pytest.raises(ValueError):
        preparar_hechizos(lista, 5, _def_a5(), hechizos=[fuera])


def test_un_hechizo_repetido_es_un_value_error():
    mm = _hechizo("magic-missile")
    with pytest.raises(ValueError):
        preparar_hechizos([mm], 5, _def_a5(), hechizos=[mm, mm])


def test_exceder_el_conteo_de_la_tabla_es_un_value_error():
    sel = [_hechizo("magic-missile"), _hechizo("burning-hands"),
           _hechizo("thunderwave")]          # preparados[5] = 2
    with pytest.raises(ValueError):
        preparar_hechizos(sel, 5, _def_a5(), hechizos=sel)


def test_un_truco_no_puede_prepararse_como_hechizo():
    fb = _hechizo("fire-bolt")
    with pytest.raises(ValueError):
        preparar_hechizos([fb], 5, _def_a5(), hechizos=[fb])


def test_un_hechizo_de_nivel_inalcanzable_es_un_value_error():
    fb = _hechizo("fireball")               # nivel 3 > mayor espacio (1)
    with pytest.raises(ValueError):
        preparar_hechizos([fb], 5, _def_a5(), hechizos=[fb])


def test_los_kwargs_explicitos_se_usan_tal_cual_sin_tocar_el_rng():
    fb, rf, mm = _hechizo("fire-bolt"), _hechizo("ray-of-frost"), \
        _hechizo("magic-missile")

    class _RngExplota:
        def randrange(self, *args, **kwargs):
            raise AssertionError("no debe tocar el rng")

    trucos, hech = preparar_hechizos([fb, rf, mm], 5, _def_a5(),
                                     trucos=[fb, rf], hechizos=[mm],
                                     rng=_RngExplota())
    assert trucos == [fb, rf] and hech == [mm]


def test_las_escuelas_restringidas_filtran_el_pool():
    defa = _def_a5(escuelas=("enchantment",), trucos_conocidos={7: 1},
                   preparados={7: 1})
    lista = _lista("fire-bolt", "ray-of-frost", "magic-missile",
                   "hold-person")
    trucos, hech = preparar_hechizos(lista, 7, defa)
    assert trucos == []                     # los trucos son evocation
    assert [s.index for s in hech] == ["hold-person"]


def test_sin_espacios_no_se_prepara_nada():
    trucos, hech = preparar_hechizos(
        _lista("fire-bolt", "magic-missile"), 1, _def_a5())  # min_level 3
    assert trucos == [] and hech == []


# --- A6: integración con el registro de clases ------------------------------ #

def _def_mago_falso() -> SpellcastingDef:
    return SpellcastingDef(
        progresion="third", caracteristica="int", lista_clase="wizard",
        trucos_conocidos={1: 2, 3: 2, 7: 3},
        preparados={1: 2, 3: 3, 7: 4}, min_level=1)


def _lista_a6():
    return _lista("fire-bolt", "ray-of-frost", "magic-missile",
                  "burning-hands", "thunderwave")


def _registrar_mago_falso():
    """Alta temporal de la clase falsa SOLO de test (como test_clases)."""
    from dnd_sim.rules.classes.base import CLASSES, ClassDef, register_class

    def _apply(pj, *, level=1, lista=None, rng=None, **kwargs):
        return aplicar_lanzamiento(
            pj, level, _def_mago_falso(),
            _lista_a6() if lista is None else lista, rng=rng)

    register_class(ClassDef(name="mago_falso", apply=_apply,
                            spellcasting=_def_mago_falso()))
    return CLASSES


def test_apply_class_con_la_clase_falsa_crea_espacios_y_acciones():
    from dnd_sim.rules.classes.base import apply_class
    registro = _registrar_mago_falso()
    try:
        pj = _pj_lanzador()
        caster = apply_class(pj, "mago_falso", level=3)
    finally:
        registro.pop("mago_falso", None)
    assert isinstance(caster, PCSpellcasting)
    assert pj.spell_slots is not None
    assert pj.spell_slots.maximos == THIRD_SLOTS[3]      # (2,)
    assert pj.spell_slots.actuales == [2]
    acciones = [a for a in pj.actions if isinstance(a, PJSpellAction)]
    assert len(acciones) == 5        # 2 trucos + 3 hechizos de nivel 1
    assert all(a.es_accion_magia for a in acciones)
    assert all(a.action_type is ActionType.ACTION for a in acciones)
    assert pj.spellcasting_pc is caster


def test_una_clase_sin_lanzamiento_no_cambia_al_combatiente():
    from dnd_sim.rules.classes.base import (
        CLASSES, ClassDef, apply_class, register_class,
    )
    register_class(ClassDef(name="clase_seca", apply=lambda pj, **kw: None))
    try:
        pj = _pj_lanzador()
        antes = list(pj.actions)
        apply_class(pj, "clase_seca", level=3)
    finally:
        CLASSES.pop("clase_seca", None)
    assert ClassDef(name="x", apply=lambda **kw: None).spellcasting is None
    assert pj.spell_slots is None
    assert getattr(pj, "spellcasting_pc", None) is None
    assert pj.actions == antes


def test_en_run_combat_el_pj_lanzador_gasta_espacios_sin_excederlos():
    from dnd_sim.engine.combat import run_combat
    from dnd_sim.rules.classes.base import apply_class
    registro = _registrar_mago_falso()
    try:
        pj = _pj_lanzador(hp=60)
        apply_class(pj, "mago_falso", level=7)
        enemigo = _enemigo(hp=80)
        r = run_combat([pj, enemigo], random.Random(5))
    finally:
        registro.pop("mago_falso", None)
    slots = pj.spell_slots
    assert r.winner in ("PJ", "NPC") and r.rounds >= 1   # combate termina
    assert all(a >= 0 for a in slots.actuales)           # no excede
    assert sum(slots.actuales) < sum(slots.maximos)      # gastó espacios


# --- A7: la Oleada de Acción no puede lanzar conjuros ---------------------- #

def _guerrero(hp: int = 80) -> PlayerCharacter:
    from dnd_sim.rules.classes.fighter.features import apply_fighter
    pj = PlayerCharacter(
        name="Thor", max_hp=hp, ac=16, level=3,
        abilities=Abilities(str=16, dex=14, con=14, wis=10, cha=8),
        attacks=[Attack("Hacha de batalla", "1d12", ability="str")])
    apply_fighter(pj, level=3, rng=random.Random(0))
    return pj


def _oleada(pj) -> object:
    return next(a for a in pj.actions if a.name == "Oleada de Acción")


def test_la_accion_extra_de_oleada_no_puede_lanzar_un_hechizo_del_pj():
    from dnd_sim.engine.combat import run_combat
    pj = _guerrero()
    aplicar_lanzamiento(pj, 3, _def_mago_falso(), _lista_a6(),
                        rng=random.Random(0))
    hechizo = next(a for a in pj.actions
                   if isinstance(a, PJSpellAction) and a.spell.level > 0)
    oleada = _oleada(pj)
    enemigo = _enemigo(hp=100)
    vistas: list[list[str]] = []

    def policy(ctx):
        if ctx.actor is not pj:
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

    r = run_combat([pj, enemigo], random.Random(4), policy=policy)
    assert hechizo.name in vistas[0]        # la primera pasada sí lo ve
    assert "Oleada de Acción" in vistas[1]
    assert hechizo.name not in vistas[2]    # la extra no lo ve
    assert hechizo.name in vistas[3]        # la de la ronda 2 vuelve a verlo
    slots = pj.spell_slots
    assert sum(slots.maximos) - sum(slots.actuales) == 1  # 1 espacio: 1 gasto
    assert r.winner == "PJ"


def test_sin_hechizos_la_pasada_extra_de_oleada_no_cambia_nada():
    from dnd_sim.engine.combat import run_combat
    pj = _guerrero()
    ataque = next(a for a in pj.actions if a.name == "Hacha de batalla")
    oleada = _oleada(pj)
    enemigo = _enemigo(hp=100)
    vistas: list[list[str]] = []

    def policy(ctx):
        if ctx.actor is not pj:
            return ctx.available_actions[0] if ctx.available_actions else None
        vistas.append([a.name for a in ctx.available_actions])
        n = len(vistas)
        if n == 1:
            return ataque
        if n == 2:
            return oleada
        return ctx.available_actions[0]

    r = run_combat([pj, enemigo], random.Random(4), policy=policy)
    assert vistas[2] == vistas[0]           # pasada extra: mismos candidatos
    assert r.action_uses["Hacha de batalla"] >= 2  # la extra atacó
    assert pj.spell_slots is None

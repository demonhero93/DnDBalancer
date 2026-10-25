"""Rasgos especiales de monstruos: Blood Frenzy del sahuagin.

Los rasgos se parsean de ``special_abilities`` (fixture real de la API) y se
aplican en la única fuente del modo de tirada:
:func:`dnd_sim.rules.roll_modifiers.attack_modifiers`.
"""
import json
import random
from pathlib import Path

import pytest

from dnd_sim import Abilities, Monster, PlayerCharacter
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.model.attack import Attack
from dnd_sim.engine.combat import attack_roll, run_combat
from dnd_sim.rules.conditions import Condition, apply_condition
from dnd_sim.rules.checks import ability_check
from dnd_sim.data.loader import load_monster
from dnd_sim.data.trait_parser import parse_traits
from dnd_sim.core.dice import RollMode
from dnd_sim.rules.roll_modifiers import (
    AttackRange, attack_modifiers, check_modifiers, save_modifiers
)
from dnd_sim.rules.saves import saving_throw
from dnd_sim.rules.traits import HOOK_NAMES, BloodFrenzy, Trait, hooks
from dnd_sim.rules.usage import begin_turn

FIXTURES = Path(__file__).parent / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _datos(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _sahuagin(monkeypatch) -> Monster:
    data = _datos("sahuagin")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("sahuagin")


def _pj(name: str = "Guerrero", hp: int = 30) -> PlayerCharacter:
    return PlayerCharacter(
        name=name, max_hp=hp, ac=15, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[],
    )


def _ctx(actor, combatantes, rng=None) -> CombatContext:
    return CombatContext(rng=rng or random.Random(1), actor=actor,
                         combatants=list(combatantes), round=1,
                         log=[], verbose=True, resources=TurnResources())


def _ataque_melee() -> Attack:
    return Attack(name="Colmillo", damage="1d6", ability="str",
                  attack_bonus=3, damage_bonus=1)


def _sahuagin_con_rasgo(hp: int = 22) -> Monster:
    return Monster(name="Sahuagin", max_hp=hp, ac=12,
                   traits=[BloodFrenzy(name="Blood Frenzy")])


# --- Carga del rasgo -------------------------------------------------------- #

def test_el_sahuagin_carga_su_rasgo_blood_frenzy(monkeypatch):
    sahuagin = _sahuagin(monkeypatch)
    assert [type(t).__name__ for t in sahuagin.traits] == ["BloodFrenzy"]
    rasgo = sahuagin.traits[0]
    assert rasgo.name == "Blood Frenzy"
    assert "advantage" in rasgo.desc          # descripción de la API, de referencia
    # Los rasgos no combativos (Limited Amphibiousness, Shark Telepathy)
    # no se modelan.
    assert len(sahuagin.traits) == 1


def test_un_monstruo_sin_rasgos_modelables_no_tiene_traits(monkeypatch):
    data = _datos("ogre")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    assert load_monster("ogre").traits == []


def test_parse_traits_solo_registra_lo_modelable():
    # Del lich solo se modela Turn Resistance: Spellcasting, Legendary
    # Resistance y Rejuvenation ya los gestiona otro parser (o no cambian
    # un combate).
    assert [type(t).__name__ for t in parse_traits(_datos("lich"))] == [
        "TurnResistance",
    ]


def test_parse_traits_ignora_entradas_malformadas():
    assert parse_traits({}) == []
    assert parse_traits({"special_abilities": [None, 42, {"sin_nombre": 1}]}) == []


# --- Reglas de Blood Frenzy ------------------------------------------------- #

def test_blood_frenzy_da_ventaja_contra_un_objetivo_herido():
    sahuagin = _sahuagin_con_rasgo()
    herido = _pj()
    herido.hp = 17
    mods = attack_modifiers(sahuagin, herido, _ataque_melee(), AttackRange.MELEE)
    assert mods.mode is RollMode.ADVANTAGE
    assert mods.advantage_sources == ["Blood Frenzy"]
    assert "Blood Frenzy" in mods.reason()


def test_blood_frenzy_no_aplica_a_un_objetivo_a_toda_vida():
    sahuagin = _sahuagin_con_rasgo()
    a_toda_vida = _pj()                      # hp == max_hp
    mods = attack_modifiers(sahuagin, a_toda_vida, _ataque_melee(),
                            AttackRange.MELEE)
    assert mods.mode is RollMode.NORMAL
    assert mods.advantage_sources == []


def test_blood_frenzy_solo_es_en_ataques_cuerpo_a_cuerpo():
    """La SRD dice «melee attack rolls»: a distancia no aplica."""
    sahuagin = _sahuagin_con_rasgo()
    herido = _pj()
    herido.hp = 17
    mods = attack_modifiers(sahuagin, herido, _ataque_melee(), AttackRange.RANGED)
    assert mods.mode is RollMode.NORMAL
    assert mods.advantage_sources == []


def test_blood_frenzy_no_aplica_a_criaturas_sin_el_rasgo():
    herido = _pj()
    herido.hp = 17
    mods = attack_modifiers(_pj(name="Sin rasgo"), herido, _ataque_melee(),
                            AttackRange.MELEE)
    assert mods.mode is RollMode.NORMAL
    assert mods.advantage_sources == []


def test_blood_frenzy_se_anula_con_una_desventaja():
    """Ventaja y desventaja a la vez se anulan (regla 5e)."""
    sahuagin = _sahuagin_con_rasgo()
    sahuagin.attacks_with_disadvantage = True
    herido = _pj()
    herido.hp = 17
    mods = attack_modifiers(sahuagin, herido, _ataque_melee(), AttackRange.MELEE)
    assert mods.mode is RollMode.NORMAL
    assert mods.cancels is True
    assert mods.reason() == "ventaja y desventaja se anulan"


# --- Integración con el motor ----------------------------------------------- #

def test_blood_frenzy_aparece_en_el_log_del_ataque():
    sahuagin = _sahuagin_con_rasgo()
    objetivo = _pj(hp=30)
    objetivo.hp = 10
    log: list = []
    attack_roll(sahuagin, objetivo, _ataque_melee(), random.Random(7),
                log=log, verbose=True)
    assert log, "el ataque debe registrarse"
    # Impacte o falle, la tirada se resuelve con ventaja y el motivo va en el log.
    assert any("ventaja" in linea for linea in log)
    assert any("Blood Frenzy" in linea for linea in log)


def test_blood_frenzy_actua_durante_el_combate_completo(monkeypatch):
    sahuagin = _sahuagin(monkeypatch)
    objetivo = _pj(hp=100)
    res = run_combat([objetivo, sahuagin], random.Random(3), verbose=True,
                     max_rounds=8)
    # Tras la primera herida, los ataques del sahuagin van con ventaja.
    assert any("Blood Frenzy" in linea for linea in res.log), \
        "el sahuagin debe atacar con ventaja a un objetivo herido"
    assert objetivo.hp < 100, "el sahuagin debe llegar a herir al objetivo"


# --- Despacho único de hooks (traits.hooks) --------------------------------- #

def test_hooks_solo_devuelve_los_que_sobrescriben_el_hook():
    base = Trait(name="Base")
    # Lista vacía/sin rasgos: nada que despachar.
    assert hooks(None, "modify_attack_modifiers") == []
    assert hooks([], "modify_attack_modifiers") == []
    # La implementación por defecto de Trait es no-op: no se llama nunca.
    assert hooks([base], "modify_attack_modifiers") == []
    activos = hooks([base, BloodFrenzy(name="Blood Frenzy")],
                    "modify_attack_modifiers")
    assert [type(t).__name__ for t in activos] == ["BloodFrenzy"]


def test_hooks_con_un_nombre_fuera_del_catalogo_lanza_error():
    # Un typo se detecta en la primera llamada, no a mitad de un combate.
    with pytest.raises(ValueError, match="Hook de rasgo desconocido"):
        hooks([BloodFrenzy(name="Blood Frenzy")], "modify_attack_modifierr")


def test_el_catalogo_cubre_hooks_que_los_rasgos_aun_no_usan():
    base = Trait(name="Base")
    for nombre in HOOK_NAMES:
        assert callable(getattr(Trait, nombre)), nombre
        assert hooks([base], nombre) == [], nombre


# --- Hooks nuevos: salvaciones, pruebas e inicio de turno ------------------- #

class _RasgoDeSalvacion(Trait):
    """Rasgo de prueba: ventaja en cualquier salvación."""

    def modify_save_modifiers(self, mods, target, ability, kind=None):
        mods.advantage_sources.append("rasgo de salvación")


class _RasgoDePrueba(Trait):
    """Rasgo de prueba: ventaja en cualquier prueba de característica."""

    def modify_check_modifiers(self, mods, target, ability, skill=None):
        mods.advantage_sources.append("rasgo de prueba")


def test_el_hook_de_salvaciones_alimenta_save_modifiers():
    pj = _pj()
    pj.traits = [_RasgoDeSalvacion(name="Prueba")]
    assert save_modifiers(pj, "dex").mode is RollMode.ADVANTAGE
    assert saving_throw(pj, "dex", 30, random.Random(1)).mode is RollMode.ADVANTAGE
    # Sin rasgo, la salvación sigue normal.
    assert save_modifiers(_pj(), "dex").mode is RollMode.NORMAL


def test_el_tipo_de_efecto_kind_llega_a_los_rasgos():
    """``saving_throw`` marca el tipo de efecto (p. ej. 'turn') para los
    rasgos: es por donde se cuela Turn Resistance en una salvación."""
    vistos: list = []

    class RasgoDeSalvacion(Trait):
        def modify_save_modifiers(self, mods, target, ability, kind=None):
            vistos.append(kind)

    pj = _pj()
    pj.traits = [RasgoDeSalvacion(name="Prueba")]
    saving_throw(pj, "dex", 12, random.Random(1))
    saving_throw(pj, "dex", 12, random.Random(1), kind="turn")
    assert vistos == [None, "turn"]
    # Un combatiente sin rasgos aguanta el parámetro sin más.
    assert saving_throw(_pj(), "wis", 12, random.Random(1),
                        kind="turn").mode is RollMode.NORMAL


def test_el_hook_de_pruebas_alimenta_check_modifiers():
    pj = _pj()
    pj.traits = [_RasgoDePrueba(name="Prueba")]
    assert check_modifiers(pj, "wis").mode is RollMode.ADVANTAGE
    assert ability_check(pj, "wis", 40, random.Random(2)).mode is RollMode.ADVANTAGE
    assert check_modifiers(_pj(), "wis").mode is RollMode.NORMAL


def test_on_turn_start_se_dispara_al_inicio_del_turno():
    llamadas: list = []

    class RasgoDeTurno(Trait):
        def on_turn_start(self, actor, ctx=None):
            llamadas.append(actor)

    pj = _pj()
    pj.traits = [RasgoDeTurno(name="Prueba")]
    begin_turn(pj, _ctx(pj, [pj]))
    assert llamadas == [pj]


def test_on_turn_start_tambien_se_dispara_estando_incapacitado():
    """Es un efecto automático de la ficha, no una acción."""
    llamadas: list = []

    class RasgoDeTurno(Trait):
        def on_turn_start(self, actor, ctx=None):
            llamadas.append(actor)

    pj = _pj()
    pj.traits = [RasgoDeTurno(name="Prueba")]
    ctx = _ctx(pj, [pj])
    apply_condition(pj, Condition.INCAPACITATED, ctx)
    begin_turn(pj, ctx)
    assert llamadas == [pj]
    assert any("incapacitado" in l for l in ctx.log)

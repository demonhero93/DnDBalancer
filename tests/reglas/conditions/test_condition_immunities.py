"""Inmunidades a condiciones: campo estático, hook blocks_condition y loader."""
import random
import warnings

from dnd_sim import (
    Abilities, Condition, Monster, PlayerCharacter, apply_condition, load_monster,
)
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.rules.conditions import ConditionAction, ConditionEffect
from dnd_sim.rules.traits import Trait


def _pj(name: str = "Guerrero", hp: int = 500) -> PlayerCharacter:
    return PlayerCharacter(
        name=name, max_hp=hp, ac=11, proficiency=2,
        abilities=Abilities(str=10, dex=10, con=10, int=10, wis=10, cha=10),
        attacks=[],
    )


def _ctx(actor=None, combatants=(), rng=None, log=None) -> CombatContext:
    return CombatContext(rng=rng or random.Random(1), actor=actor,
                         combatants=list(combatants), round=1,
                         log=log if log is not None else [],
                         verbose=True, resources=TurnResources())


def _ghoul(monkeypatch) -> Monster:
    import json
    from pathlib import Path

    datos = json.loads((Path(__file__).parents[2] / "fixtures" / "ghoul.json")
                       .read_text(encoding="utf-8"))
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: datos)
    return load_monster("ghoul")


# --- Estática --------------------------------------------------------------- #

def test_el_cargador_carga_las_inmunidades_del_fixture(monkeypatch):
    """El loader traduce condition_immunities de la API a Condition."""
    ghoul = _ghoul(monkeypatch)
    assert ghoul.condition_immunities == {Condition.POISONED, Condition.CHARMED}


def test_las_condiciones_no_modeladas_no_avisan_en_el_cargador(monkeypatch):
    """'exhaustion' de la API es la 'exhausted' excluida: silencio."""
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        ghoul = _ghoul(monkeypatch)
    assert Condition.POISONED in ghoul.condition_immunities


def test_una_condicion_desconocida_de_la_api_avisa(monkeypatch):
    """Una entrada fuera del catálogo emite warnings.warn y se ignora."""
    import json
    from pathlib import Path

    datos = json.loads((Path(__file__).parents[2] / "fixtures" / "ghoul.json")
                       .read_text(encoding="utf-8"))
    datos["condition_immunities"] = [{"index": "paralizado"}]
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda name: datos)
    with warnings.catch_warnings(record=True) as lista:
        warnings.simplefilter("always")
        monstruo = load_monster("ghoul")
    assert monstruo.condition_immunities == set()
    assert any("Condición inmune desconocida" in str(w.message)
               for w in lista)


def test_apply_condition_no_crea_instancia_si_el_objetivo_es_inmune(monkeypatch):
    """Estática: inmune -> None, sin instancia en el tracker, con log."""
    ghoul = _ghoul(monkeypatch)
    ctx = _ctx()
    assert apply_condition(ghoul, Condition.POISONED, ctx) is None
    assert not ghoul.conditions.has(Condition.POISONED)
    assert any("inmune a" in linea for linea in ctx.log)


def test_apply_condition_no_cuenta_la_condicion_bloqueada_en_stats(monkeypatch):
    """La inmunidad no registra el contador de condiciones aplicadas."""
    ghoul = _ghoul(monkeypatch)
    ctx = _ctx()
    ctx.conditions_applied = {}
    apply_condition(ghoul, Condition.POISONED, ctx)
    assert ctx.conditions_applied == {}


def test_una_condicion_no_inmune_se_aplica_con_normalidad(monkeypatch):
    """Control: frightened no está en la lista del ghoul."""
    ghoul = _ghoul(monkeypatch)
    ctx = _ctx()
    instancia = apply_condition(ghoul, Condition.FRIGHTENED, ctx)
    assert instancia is not None
    assert ghoul.conditions.has(Condition.FRIGHTENED)


def test_el_bando_pj_tambien_puede_ser_inmune():
    """El campo vive en Combatant: un PJ con la propiedad se comporta igual."""
    pj = _pj()
    pj.condition_immunities = {Condition.FRIGHTENED}
    ctx = _ctx()
    assert apply_condition(pj, Condition.FRIGHTENED, ctx) is None
    assert not pj.conditions.has(Condition.FRIGHTENED)


# --- Dinámica (hook blocks_condition) --------------------------------------- #

class _InmuneMientrasActivo(Trait):
    """Rasgo de prueba: bloquea una condición mientras ``activo``."""

    def __init__(self, condicion: Condition):
        super().__init__(name="Inmunidad temporal")
        self.condicion = condicion
        self.activo = True

    def blocks_condition(self, condition, ctx=None) -> bool:
        return self.activo and condition == self.condicion


def test_un_rasgo_bloquea_la_condicion_mientras_activo():
    pj = _pj()
    rasgo = _InmuneMientrasActivo(Condition.CHARMED)
    pj.traits = [rasgo]
    ctx = _ctx()
    assert apply_condition(pj, Condition.CHARMED, ctx) is None
    assert not pj.conditions.has(Condition.CHARMED)


def test_el_rasgo_deja_de_bloquear_al_desactivarse():
    pj = _pj()
    rasgo = _InmuneMientrasActivo(Condition.CHARMED)
    pj.traits = [rasgo]
    ctx = _ctx()
    rasgo.activo = False
    assert apply_condition(pj, Condition.CHARMED, ctx) is not None
    assert pj.conditions.has(Condition.CHARMED)


def test_sin_el_rasgo_la_condicion_no_bloquea():
    """Control: el mismo objetivo sin el rasgo recibe la condición."""
    pj = _pj()
    ctx = _ctx()
    assert apply_condition(pj, Condition.CHARMED, ctx) is not None


def test_el_rasgo_no_bloquea_condiciones_distintas():
    pj = _pj()
    pj.traits = [_InmuneMientrasActivo(Condition.CHARMED)]
    ctx = _ctx()
    assert apply_condition(pj, Condition.POISONED, ctx) is not None


# --- Caminos de aplicación (todos pasan por apply_condition) ---------------- #

def test_la_condicion_de_un_rider_no_se_aplica_si_el_objetivo_es_inmune(monkeypatch):
    """Rider de ataque: el rider llama a apply_condition y queda bloqueado."""
    ghoul = _ghoul(monkeypatch)
    atacante = _pj(name="Atacante")
    ctx = _ctx(actor=atacante, combatants=[atacante, ghoul])
    accion = ConditionAction(
        name="Mordida ponzoñosa",
        effect=ConditionEffect(condition=Condition.POISONED,
                               save_ability="con", dc=30),
    )
    accion.execute(ctx)
    assert not ghoul.conditions.has(Condition.POISONED)
    assert any("inmune a" in linea for linea in ctx.log)


# --- Ataque Temerario: propiedad expuesta ----------------------------------- #

def test_reckless_active_this_turn_refleja_el_estado():
    from dnd_sim.rules.classes.barbarian import BarbarianFeatures

    rasgo = BarbarianFeatures(level=3)
    assert rasgo.reckless_active_this_turn is False
    rasgo.reckless_active = True
    assert rasgo.reckless_active_this_turn is True

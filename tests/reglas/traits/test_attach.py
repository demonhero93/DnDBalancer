"""Enganche y Damage Transfer del cloaker (features especiales).

El enganche nace en el ataque (Bite) y vive en ``CombatState.attached_to``;
el reparto de daño es el rasgo ``Damage Transfer``. Todas las fichas salen
de fixtures reales de la API.
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, PlayerCharacter
from dnd_sim.model.actions import ActionType, CombatContext, TurnResources
from dnd_sim.rules.attach import (
    Attach, AttachOnHitEffect, desenganchar, enganchador_de, intentar_desenganche
)
from dnd_sim.model.attack import Attack
from dnd_sim.engine.combat import attack_roll, run_combat
from dnd_sim.model.combatant import Monster
from dnd_sim.rules.conditions import Condition, apply_condition
from dnd_sim.data.loader import load_monster
from dnd_sim.rules.damage import DamageType, inflict_damage
from dnd_sim.rules.roll_modifiers import AttackRange, attack_modifiers
from dnd_sim.core.targeting import valid_targets
from dnd_sim.rules.traits import DamageTransfer

FIXTURES = Path(__file__).parents[2] / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _datos(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _cloaker(monkeypatch) -> Monster:
    data = _datos("cloaker")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("cloaker")


def _pj(name: str = "Guerrero", hp: int = 60, ac: int = 15,
        con_ataque: bool = False) -> PlayerCharacter:
    ataques = []
    if con_ataque:
        ataques = [Attack(name="Espada", damage="1d8", ability="str",
                          attack_bonus=5, damage_bonus=3)]
    return PlayerCharacter(
        name=name, max_hp=hp, ac=ac, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=ataques,
    )


def _bite(cloaker) -> Attack:
    return next(a for a in cloaker.attacks if a.name == "Bite")


def _ctx(actor, combatants, seed: int = 1, log: list | None = None) -> CombatContext:
    return CombatContext(
        rng=random.Random(seed), actor=actor, combatants=list(combatants),
        round=1, log=log if log is not None else [], verbose=True,
        resources=TurnResources(),
    )


def _atacar(cloaker, objetivo, seed: int, con_ventaja: bool = False) -> list:
    """Un Bite con un log compartido entre el ataque y el enganche."""
    if con_ventaja:
        cloaker.attacks_with_advantage = True
    log: list = []
    ctx = _ctx(cloaker, [cloaker, objetivo], seed=seed, log=log)
    attack_roll(cloaker, objetivo, _bite(cloaker), ctx.rng, log=log,
                verbose=True, ctx=ctx)
    return log


# --- Carga de la ficha ------------------------------------------------------ #

def test_el_cloaker_carga_su_enganche_y_su_damage_transfer(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    assert [type(t).__name__ for t in cloaker.traits] == [
        "DamageTransfer", "Attach",
    ]
    assert cloaker.traits[0].name == "Damage Transfer"
    # El enganche lo declara el Bite (no el Tail) y sin riders genéricos:
    # dnd_sim.rules.attach es el único dueño de la ceguera y el desenganche.
    bite = _bite(cloaker)
    assert len(bite.on_hit_effects) == 1
    assert isinstance(bite.on_hit_effects[0], AttachOnHitEffect)
    assert bite.condition_riders == []
    tail = next(a for a in cloaker.attacks if a.name == "Tail")
    assert tail.on_hit_effects == []
    # Multiattack (Bite + Tail) y Moan siguen presentes.
    assert [a.name for a in cloaker.actions] == ["Multiattack", "Moan"]


# --- Engancharse ------------------------------------------------------------ #

def test_el_impacto_del_bite_engancha_al_objetivo(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    objetivo = _pj()
    log = _atacar(cloaker, objetivo, seed=6)
    assert cloaker.state.attached_to is objetivo
    assert any("se engancha a Guerrero" in linea for linea in log)
    # Sin ventaja en el impacto: enganche normal, no a la cabeza.
    assert not objetivo.conditions.has(Condition.BLINDED)
    assert not any("cabeza" in linea for linea in log)


def test_un_fallo_del_bite_no_engancha(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    objetivo = _pj()
    log = _atacar(cloaker, objetivo, seed=1)  # fallo (natural 1)
    assert cloaker.state.attached_to is None
    assert not any("engancha" in linea for linea in log)


def test_con_ventaja_el_enganche_es_a_la_cabeza_y_ciega(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    objetivo = _pj()
    log = _atacar(cloaker, objetivo, seed=6, con_ventaja=True)
    assert cloaker.state.attached_to is objetivo
    assert objetivo.conditions.has(Condition.BLINDED)
    assert any("se engancha a la cabeza" in linea for linea in log)
    assert any("queda cegado" in linea for linea in log)
    # Una sola instancia de ceguera (no se duplica en impactos posteriores).
    _atacar(cloaker, objetivo, seed=6, con_ventaja=True)
    instancias = [i for i in objetivo.conditions.instances
                  if i.condition is Condition.BLINDED]
    assert len(instancias) == 1


# --- Reglas mientras está enganchado ---------------------------------------- #

def test_mientras_enganchado_ataca_con_ventaja_a_su_objetivo(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    objetivo = _pj()
    otro = _pj(name="Otro")
    cloaker.state.attached_to = objetivo
    mods = attack_modifiers(cloaker, objetivo, _bite(cloaker), AttackRange.MELEE)
    assert mods.advantage_sources == ["Enganche"]
    # La ventaja es contra su objetivo enganchado, no contra los demás.
    otros = attack_modifiers(cloaker, otro, _bite(cloaker), AttackRange.MELEE)
    assert otros.advantage_sources == []


def test_mientras_enganchado_solo_puede_atacar_a_la_criatura_enganchada(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    objetivo, otro = _pj(name="A"), _pj(name="B")
    cloaker.state.attached_to = objetivo
    pool = [cloaker, objetivo, otro]
    # El ataque con enganche solo puede ir contra la criatura enganchada...
    assert valid_targets(cloaker, combatants=pool, atk=_bite(cloaker)) == [objetivo]
    # ...el Tail y cualquier otra acción (Moan, salvaciones) no se restringen.
    tail = next(a for a in cloaker.attacks if a.name == "Tail")
    assert valid_targets(cloaker, combatants=pool, atk=tail) == [objetivo, otro]
    assert valid_targets(cloaker, combatants=pool) == [objetivo, otro]


def test_la_restriccion_se_levanta_si_el_objetivo_enganchado_ha_muerto(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    objetivo = _pj(name="A")
    otro = _pj(name="B")
    objetivo.hp = 0
    pool = [cloaker, objetivo, otro]
    assert valid_targets(cloaker, combatants=pool, atk=_bite(cloaker)) == [otro]


# --- Damage Transfer -------------------------------------------------------- #

def test_damage_transfer_reparte_el_daño_mitad_y_mitad(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    objetivo = _pj(hp=60)
    cloaker.state.attached_to = objetivo
    log: list = []
    ctx = _ctx(cloaker, [cloaker, objetivo], log=log)
    # 15 -> él baja 7 (redondeado abajo) y el objetivo se lleva los otros 8.
    infligido = inflict_damage(cloaker, 15, "piercing", ctx=ctx)
    assert infligido == 7
    assert cloaker.hp == 78 - 7
    assert objetivo.hp == 60 - 8
    assert any("reparte el daño" in linea and "otros 8" in linea
               for linea in log)
    # 16 -> 8 y 8 (los dos números enteros de la mitad exacta).
    infligido = inflict_damage(cloaker, 16, "piercing", ctx=ctx)
    assert infligido == 8
    assert cloaker.hp == 78 - 7 - 8
    assert objetivo.hp == 60 - 8 - 8


def test_damage_transfer_no_aplica_sin_enganche(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    objetivo = _pj(hp=60)
    inflict_damage(cloaker, 15, "piercing")
    assert cloaker.hp == 78 - 15
    assert objetivo.hp == 60


def test_el_reparto_respeta_la_resistencia_del_receptor(monkeypatch):
    """La mitad que recibe la otra criatura es daño normal: se resiste."""
    cloaker = _cloaker(monkeypatch)
    objetivo = _pj(hp=60)
    objetivo.resistances = {DamageType.PIERCING}
    cloaker.state.attached_to = objetivo
    log: list = []
    ctx = _ctx(cloaker, [cloaker, objetivo], log=log)
    # 15 -> el cloaker baja 7 (su propia resistencia no está en la ficha) y
    # los otros 8 pasan por la resistencia del receptor: 4.
    infligido = inflict_damage(cloaker, 15, "piercing", ctx=ctx)
    assert infligido == 7
    assert cloaker.hp == 78 - 7
    assert objetivo.hp == 60 - 4
    assert any("reparte el daño" in linea and "otros 4" in linea
               and "resistencia" in linea for linea in log), log


def test_el_reparto_no_dania_a_un_receptor_inmune(monkeypatch):
    """Inmune: la llamada se hace con 0 (como el daño principal)."""
    cloaker = _cloaker(monkeypatch)
    objetivo = _pj(hp=60)
    objetivo.immunities = {DamageType.PIERCING}
    cloaker.state.attached_to = objetivo
    log: list = []
    ctx = _ctx(cloaker, [cloaker, objetivo], log=log)
    infligido = inflict_damage(cloaker, 16, "piercing", ctx=ctx)
    assert infligido == 8           # el cloaker sigue bajando su mitad
    assert cloaker.hp == 78 - 8
    assert objetivo.hp == 60        # el inmune no pierde PV
    assert any("reparte el daño" in linea and "inmune" in linea
               for linea in log), log


def test_el_daño_al_objetivo_enganchado_no_se_reparte(monkeypatch):
    """La ficha solo reparte el daño que recibe EL CLOAKER."""
    cloaker = _cloaker(monkeypatch)
    objetivo = _pj(hp=60)
    cloaker.state.attached_to = objetivo
    infligido = inflict_damage(objetivo, 15, "piercing")
    assert infligido == 15
    assert objetivo.hp == 60 - 15
    assert cloaker.hp == 78


def test_el_reparto_no_aplica_si_la_criatura_enganchada_ha_muerto(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    objetivo = _pj(hp=60)
    objetivo.hp = 0
    cloaker.state.attached_to = objetivo
    infligido = inflict_damage(cloaker, 10, "piercing")
    assert infligido == 10          # sin reparto: él baja todo
    assert cloaker.hp == 78 - 10
    assert objetivo.hp == 0


# --- Desengancharse --------------------------------------------------------- #

def test_enganchador_de_encuentra_al_que_engancha(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    objetivo, otro = _pj(), _pj(name="Otro")
    ctx = _ctx(objetivo, [cloaker, objetivo, otro])
    assert enganchador_de(objetivo, ctx) is None
    cloaker.state.attached_to = objetivo
    assert enganchador_de(objetivo, ctx) is cloaker
    # Solo hay referencia en el que engancha: los demás no saben nada.
    assert enganchador_de(otro, ctx) is None
    # Un enganchador muerto ya no engancha.
    cloaker.hp = 0
    assert enganchador_de(objetivo, ctx) is None


def test_el_desenganche_es_una_prueba_de_fuerza_cd_16_que_gasta_la_accion(monkeypatch):
    exitos = fallos = 0
    for semilla in range(1, 41):
        cloaker = _cloaker(monkeypatch)
        objetivo = _pj()
        cloaker.state.attached_to = objetivo
        log: list = []
        ctx = _ctx(objetivo, [cloaker, objetivo], seed=semilla, log=log)
        intentar_desenganche(objetivo, ctx)
        # Gasta la acción acierte o falle («can take its action»).
        assert not ctx.resources.can_use(ActionType.ACTION), semilla
        if cloaker.state.attached_to is None:
            exitos += 1
            assert any("se desengancha" in linea for linea in log), semilla
        else:
            fallos += 1
            assert any("no logra desengancharse" in linea for linea in log), semilla
    assert exitos >= 1 and fallos >= 1, "las dos salidas deben darse con la CD 16"


def test_sin_accion_disponible_no_intenta_desengancharse(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    objetivo = _pj()
    cloaker.state.attached_to = objetivo
    log: list = []
    ctx = _ctx(objetivo, [cloaker, objetivo], seed=5, log=log)  # semilla exitosa
    ctx.resources.use(ActionType.ACTION)
    intentar_desenganche(objetivo, ctx)
    assert cloaker.state.attached_to is objetivo  # sigue enganchado
    assert log == []                             # ni siquiera intenta


def test_desenganchar_quita_solo_la_ceguera_de_ese_enganche(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    objetivo = _pj()
    otra_fuente = _pj(name="Otra")
    log: list = []
    ctx = _ctx(cloaker, [cloaker, objetivo], log=log)
    # Cegado por otra fuente además del enganche.
    apply_condition(objetivo, Condition.BLINDED, ctx, source=otra_fuente)
    _atacar(cloaker, objetivo, seed=6, con_ventaja=True)
    assert objetivo.conditions.has(Condition.BLINDED)
    assert enganchador_de(objetivo, _ctx(objetivo, [cloaker, objetivo])) is cloaker
    desenganchar(cloaker, ctx)
    assert cloaker.state.attached_to is None
    # Se va la ceguera del enganche y se queda la de la otra fuente.
    fuentes = [i.source for i in objetivo.conditions.instances
               if i.condition is Condition.BLINDED]
    assert fuentes == [otra_fuente]
    assert any("se desengancha de Guerrero" in linea for linea in log)


def test_reset_limpia_el_enganche(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    objetivo = _pj()
    cloaker.state.attached_to = objetivo
    cloaker.reset()
    assert cloaker.state.attached_to is None


# --- Integración con el motor ----------------------------------------------- #

def test_un_combate_completo_con_cloaker(monkeypatch):
    cloaker = _cloaker(monkeypatch)
    pjs = [_pj(name="A", con_ataque=True), _pj(name="B", con_ataque=True)]
    res = run_combat([*pjs, cloaker], random.Random(3), verbose=True,
                     max_rounds=10)
    lineas = res.log
    assert any("se engancha" in l for l in lineas), "debe engancharse en combate"
    assert any("reparte el daño" in l for l in lineas), \
        "Damage Transfer debe partir el daño que recibe"
    assert any("desengancha" in l for l in lineas), \
        "el objetivo debe poder escapar del enganche"

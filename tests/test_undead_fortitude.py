"""Undead Fortitude del zombi: salvación para no caer a 0 PV.

La ficha (fixture real de la API) dice: si el daño lo deja a 0, tira
Constitución con CD 5 + daño recibido y, con éxito, queda a 1 PV; no hay
salvación si el daño es radiante o viene de un crítico. Es la primera
consumidora del hook ``on_reduced_to_zero_hp``, que se resuelve **al
aplicar el daño** (no en el turno) y tira con ``saving_throw`` de siempre.
"""
import json
import random
from pathlib import Path

from dnd_sim import Abilities, Monster, PlayerCharacter
from dnd_sim.model.actions import CombatContext, TurnResources
from dnd_sim.model.attack import Attack
from dnd_sim.engine.combat import run_combat
from dnd_sim.data.loader import load_monster
from dnd_sim.data.trait_parser import parse_traits
from dnd_sim.rules.damage import inflict_damage
from dnd_sim.rules.traits import UndeadFortitude

FIXTURES = Path(__file__).parent / "fixtures"


# --- Utilidades ------------------------------------------------------------- #

def _datos(index: str) -> dict:
    return json.loads((FIXTURES / f"{index}.json").read_text(encoding="utf-8"))


def _zombi(monkeypatch) -> Monster:
    data = _datos("zombie")
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: data)
    return load_monster("zombie")


def _ctx(actor, combatantes, semilla: int = 1) -> CombatContext:
    return CombatContext(rng=random.Random(semilla), actor=actor,
                         combatants=list(combatantes), round=1, log=[],
                         verbose=True, resources=TurnResources())


def _salva(monkeypatch, danyo: int, tipo: str = "slashing",
           semillas=range(40), **kw):
    """Prueba la salvación con varias semillas.

    Devuelve ``(veces_a_un_pv, veces_muerto, log_de_la_primera_salvacion)``.
    El zombi siempre empieza a 5 PV, así que cualquier daño lo deja a 0.
    """
    zombi = _zombi(monkeypatch)
    superado = caido = 0
    log_exito: list[str] = []
    for semilla in semillas:
        zombi.reset()
        zombi.hp = 5
        ctx = _ctx(zombi, [zombi], semilla)
        inflict_damage(zombi, danyo, tipo, ctx=ctx, **kw)
        if zombi.hp == 1:
            superado += 1
            if not log_exito:
                log_exito = list(ctx.log)
        elif zombi.hp < 0:
            caido += 1
        else:
            raise AssertionError(
                f"hp inesperado: {zombi.hp} (semilla {semilla})")
    return superado, caido, log_exito


def _pj() -> PlayerCharacter:
    return PlayerCharacter(
        name="Guerrero", max_hp=60, ac=15, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[Attack(name="Espada", damage="1d8", ability="str",
                        attack_bonus=5, damage_bonus=3)],
    )


# --- Carga de la ficha ------------------------------------------------------ #

def test_el_zombi_carga_su_undead_fortitude_con_su_dc(monkeypatch):
    zombi = _zombi(monkeypatch)
    assert [type(t).__name__ for t in zombi.traits] == ["UndeadFortitude"]
    rasgo = zombi.traits[0]
    assert rasgo.name == "Undead Fortitude"
    # «a DC of 5+the damage taken»: el 5 sale de la descripción.
    assert rasgo.dc_base == 5


def test_una_descripcion_no_interpretable_no_salva():
    rasgo = parse_traits({"special_abilities": [
        {"name": "Undead Fortitude", "desc": "Se resiste con uñas."},
    ]})[0]
    assert isinstance(rasgo, UndeadFortitude)
    assert rasgo.dc_base == 0
    ctx = _ctx(None, [])
    assert rasgo.on_reduced_to_zero_hp(None, 10, "slashing", ctx=ctx,
                                       rng=random.Random(1)) is None


# --- Reglas ----------------------------------------------------------------- #

def test_la_salvacion_puede_salvarlo_o_no(monkeypatch):
    superado, caido, _ = _salva(monkeypatch, danyo=10)
    # CD 15 con bonificador de Constitución modesto: hay semillas de ambos.
    assert superado > 0, "hay tiradas que superan la salvación"
    assert caido > 0, "y tiradas que la fallan"


def test_queda_a_un_pv_y_lo_registra_en_el_log(monkeypatch):
    _, _, log = _salva(monkeypatch, danyo=10, semillas=range(40))
    assert log, "alguna semilla debe superar la salvación"
    assert any("Undead Fortitude" in l and "DC 15" in l and "queda a 1 PV" in l
               for l in log), log


def test_la_cd_es_cinco_mas_el_danyo_recibido(monkeypatch):
    import dnd_sim.rules.saves as saves_mod
    original = saves_mod.saving_throw
    capturas = []

    def espia(target, ability, dc, rng, mode=None, **kw):
        capturas.append((ability, dc))
        return original(target, ability, dc, rng, mode, **kw)

    monkeypatch.setattr(saves_mod, "saving_throw", espia)
    zombi = _zombi(monkeypatch)
    zombi.hp = 5
    ctx = _ctx(zombi, [zombi], 7)
    inflict_damage(zombi, 10, "slashing", ctx=ctx)
    assert capturas == [("con", 15)], "CD 5 + 10 de daño, de Constitución"


def test_el_danyo_radiante_no_da_salvacion(monkeypatch):
    # El tipo de daño se llama como en la ficha («radiant»).
    superado, caido, _ = _salva(monkeypatch, danyo=10, tipo="radiant",
                                semillas=range(10))
    assert superado == 0, "«unless the damage is radiant»"
    assert caido > 0


def test_un_critico_no_da_salvacion(monkeypatch):
    superado, caido, _ = _salva(monkeypatch, danyo=10, crit=True,
                                semillas=range(10))
    assert superado == 0, "«unless ... from a critical hit»"
    assert caido > 0


def test_a_un_zombi_ya_caido_no_le_vuelven_a_salvar(monkeypatch):
    # Solo cuenta el daño que lo baja desde PV positivos: rematar un cuerpo
    # ya en el suelo no revive a nadie.
    zombi = _zombi(monkeypatch)
    zombi.hp = 0
    ctx = _ctx(zombi, [zombi])
    ctx.log.clear()
    inflict_damage(zombi, 10, "slashing", ctx=ctx)
    assert zombi.hp == -10
    assert not any("Undead Fortitude" in l for l in ctx.log)


def test_sin_rng_no_se_tira_la_salvacion(monkeypatch):
    # Sin generador el rasgo se abstiene en lugar de inventar el resultado.
    zombi = _zombi(monkeypatch)
    zombi.hp = 5
    inflict_damage(zombi, 10, "slashing")
    assert zombi.hp == -5


# --- Integración con el motor ----------------------------------------------- #

def test_un_combate_completo_usa_undead_fortitude(monkeypatch):
    # La salvación es aleatoria y la línea solo aparece con éxito: se
    # prueban varias semillas hasta que alguna la supera.
    for semilla in range(1, 12):
        zombi = _zombi(monkeypatch)
        res = run_combat([_pj(), zombi], random.Random(semilla), verbose=True,
                         max_rounds=30)
        assert not zombi.alive, "el zombi debe acabar muriendo"
        if any("Undead Fortitude" in l for l in res.log):
            return
    raise AssertionError("ningún combate superó la salvación")

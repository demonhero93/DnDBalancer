"""Muerte al instante: PV sin bajar de 0, estado de muerto y fin del combate.

Lo que cubre este archivo:

1. El daño **nunca** deja los PV por debajo de cero (la regla 5e no
   contempla PV negativos: el exceso solo sirve para rematar).
2. El daño igual o mayor que los PV restantes deja al objetivo a 0 PV
   **marcado como muerto** en ese mismo golpe (``Combatant.mark_dead``).
3. Una habilidad no se lanza si su propio actor ya ha caído.
4. En cuanto cae el último de un bando (PJ o NPC) el combate termina ahí
   mismo: no se ejecutan más habilidades ni siguen los turnos.
"""
import random

from dnd_sim import Abilities, Monster, PlayerCharacter
from dnd_sim.core.targeting import combat_finished, living_teams
from dnd_sim.engine.combat import attack_roll, run_combat
from dnd_sim.model.actions import ActionType, CombatAction, CombatContext, TurnResources
from dnd_sim.model.attack import Attack
from dnd_sim.rules.damage import inflict_damage


# --- Utilidades ------------------------------------------------------------- #

def _pj(hp: int = 50, golpe: int = 30) -> PlayerCharacter:
    """Golpe siempre certero (bono enorme) para que el desenlace sea fijo."""
    return PlayerCharacter(
        name="Guerrero", max_hp=hp, ac=18, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[Attack(name="Espada", damage="1d8", ability="str",
                        attack_bonus=golpe, damage_bonus=10)],
    )


def _npc(hp: int = 5, ac: int = 10, actions=()) -> Monster:
    return Monster(name="Goblin", max_hp=hp, ac=ac, attacks=[],
                   abilities=Abilities(str=10), actions=list(actions))


def _ctx(actor, combatantes, semilla: int = 1) -> CombatContext:
    return CombatContext(rng=random.Random(semilla), actor=actor,
                         combatants=list(combatantes), round=1, log=[],
                         verbose=True, resources=TurnResources())


class _BonusQueAnota(CombatAction):
    """Acción bonus de prueba: anota si llega a ejecutarse."""

    def __init__(self, lanzamientos: list) -> None:
        self.name = "Bonus de prueba"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None
        self.lanzamientos = lanzamientos

    def execute(self, context) -> None:
        self.lanzamientos.append(context.actor.name)


class _RepresaliaMortal(CombatAction):
    """Reacción de prueba: remata al atacante (lo deja a 0 PV y muerto)."""

    def __init__(self) -> None:
        self.name = "Represalia mortal"
        self.action_type = ActionType.REACTION
        self.usage = None

    def execute(self, context) -> None:
        for combatiente in context.combatants:
            if combatiente is context.actor:
                continue
            if context.actor.is_hostile_to(combatiente):
                inflict_damage(combatiente, 999, "necrotic",
                               source=context.actor, ctx=context)


# --- 1. Los PV no bajan de cero --------------------------------------------- #

def test_el_daño_no_deja_los_pv_por_debajo_de_cero():
    objetivo = _npc(hp=20)
    assert inflict_damage(objetivo, 45, "bludgeoning") == 45
    assert objetivo.hp == 0, "el exceso de daño no genera PV negativos"

    exacto = _npc(hp=20)
    inflict_damage(exacto, 20, "bludgeoning")
    assert exacto.hp == 0


def test_el_ataque_que_remata_deja_el_objetivo_a_cero():
    atacante = _pj()
    objetivo = _npc(hp=5)
    log: list[str] = []

    attack_roll(atacante, objetivo, atacante.attacks[0], random.Random(1),
                log, verbose=True)

    assert objetivo.hp == 0
    assert not objetivo.alive
    assert "(HP 0/" in log[-1], log


# --- 2. Estado de muerto al instante ---------------------------------------- #

def test_el_daño_que_supera_la_vida_lo_marca_muerto_al_instante():
    objetivo = _npc(hp=5)
    objetivo.hp = 1
    inflict_damage(objetivo, 30, "piercing")

    assert objetivo.hp == 0
    assert objetivo.dead, "el exceso debe dejarlo ya marcado como muerto"
    assert not objetivo.alive


def test_una_criatura_que_se_salva_no_queda_marcada_como_muerta(monkeypatch):
    # Relentless: 7 daño sobre 7 PV lo deja a 1 PV, sigue viva y sin marcar.
    # El fixture 2024 ya no declara Relentless (trae «Bloodied Fury»): se
    # inyecta la entrada sintética con el umbral de la ficha.
    import json
    from pathlib import Path

    from dnd_sim.data.loader import load_monster

    datos = json.loads((Path(__file__).parents[1] / "fixtures" / "boar.json")
                       .read_text(encoding="utf-8"))
    datos["special_abilities"] = list(datos.get("special_abilities") or []) + [
        {"name": "Relentless",
         "desc": ("If the boar takes 7 damage or less that would reduce it "
                  "to 0 hit points, it is reduced to 1 hit point instead."),
         "damage": [],
         "usage": {"type": "recharge after rest",
                   "rest_types": ["short", "long"]}},
    ]
    monkeypatch.setattr("dnd_sim.data.loader.get_monster", lambda index: datos)
    jabali = load_monster("boar")
    jabali.hp = 7

    inflict_damage(jabali, 7, "piercing", ctx=_ctx(jabali, [jabali]))

    assert jabali.hp == 1
    assert not jabali.dead
    assert jabali.alive


def test_el_estado_de_muerte_se_reinicia_al_empezar_un_combate_nuevo():
    objetivo = _npc(hp=5)
    inflict_damage(objetivo, 5, "piercing")
    assert objetivo.dead

    objetivo.reset()
    assert not objetivo.dead
    assert objetivo.alive
    assert objetivo.hp == objetivo.max_hp


def test_el_combate_terminado_se_detecta_al_momento():
    atacante = _pj()
    objetivo = _npc(hp=5)
    assert not combat_finished([atacante, objetivo])

    attack_roll(atacante, objetivo, atacante.attacks[0], random.Random(1))

    assert combat_finished([atacante, objetivo])
    assert living_teams([atacante, objetivo]) == {"PJ"}


# --- 3. Las habilidades no se lanzan con el actor caído --------------------- #

def test_una_habilidad_no_se_lanza_si_el_actor_ha_muerto():
    enemigo = _npc(hp=20)
    pj = _pj(hp=10)
    pj.hp = 0
    pj.mark_dead()
    ctx = _ctx(pj, [pj, enemigo])

    ataque = next(a for a in pj.actions
                  if getattr(a, "action_type", None) is ActionType.ACTION)
    ataque.execute(ctx)

    assert enemigo.hp == enemigo.max_hp, "un muerto no lanza su habilidad"


def test_una_habilidad_bonus_no_se_lanza_si_el_actor_ha_muerto():
    from dnd_sim.rules.spells.actions import SpellFixedDamageAction

    enemigo = _npc(hp=20)
    pj = _pj(hp=10)
    pj.mark_dead()
    ctx = _ctx(pj, [pj, enemigo])
    bonus = SpellFixedDamageAction(name="Proyectil mágico",
                                   action_type=ActionType.BONUS_ACTION,
                                   damage="1d4")

    # El filtro del motor la descarta...
    assert not bonus.can_use(TurnResources(), ctx)
    # ...y, aunque llegue a ejecutarse, no se lanza.
    bonus.execute(ctx)
    assert enemigo.hp == enemigo.max_hp


# --- 4. El combate termina al caer el último de un bando -------------------- #

def test_el_combate_termina_en_el_mismo_golpe_cuando_cae_el_ultimo_enemigo():
    pj = _pj()
    npc = _npc(hp=1)  # un solo golpe lo remata
    res = run_combat([pj, npc], random.Random(1), verbose=True, max_rounds=10)

    assert res.winner == "PJ"
    assert npc.dead and not npc.alive
    assert res.rounds == 1, "no hay ronda 2: el combate acabó con la muerte"
    assert not any("Ronda 2" in linea for linea in res.log)
    assert res.survivors[npc.name] == 0


def test_no_se_lanzan_mas_habilidades_cuando_el_bando_enemigo_ha_caido():
    # La acción bonus no debe ejecutarse (ni siquiera contarse) después de
    # que el ACTION haya dejado al último enemigo muerto.
    lanzamientos: list = []
    pj = _pj()
    pj.actions.append(_BonusQueAnota(lanzamientos))
    npc = _npc(hp=1)

    res = run_combat([pj, npc], random.Random(1), verbose=True, max_rounds=10)

    assert lanzamientos == [], "el combate ya había terminado"
    assert "Bonus de prueba" not in res.action_uses
    assert res.winner == "PJ"


def test_si_el_actor_muere_en_su_turno_no_sigue_actuando():
    # El PJ ataca, la reacción del enemigo lo remata y ahí mismo se acaba:
    # ni su acción bonus se lanza ni el combate continúa.
    lanzamientos: list = []
    pj = _pj(hp=20, golpe=30)          # golpe casi siempre certero (CA 10)
    pj.actions.append(_BonusQueAnota(lanzamientos))
    npc = _npc(hp=40, actions=[_RepresaliaMortal()])

    res = run_combat([pj, npc], random.Random(1), verbose=True, max_rounds=10)

    assert not pj.alive and pj.dead
    assert lanzamientos == [], "un PJ a 0 PV no lanza su acción bonus"
    assert "Bonus de prueba" not in res.action_uses
    assert res.winner == "NPC"

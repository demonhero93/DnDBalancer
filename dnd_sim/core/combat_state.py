"""Estado de combate de un combatiente (posiciones, cobertura y enganche).

Solo se modela lo que afecta a las tiradas: si un combatiente está "a
distancia" de su objetivo actual, su CA efectiva sube 2 (cobertura
simulada).

# TODO: cobertura real (obstrucciones, medio cuerpo), movimiento y
distancia entre varios combatientes.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class CombatState:
    """Estado de combate de un combatiente.

    ``at_range``: el combatiente ataca a distancia (y queda "a distancia"
    respecto a quien le ataca). Todos empiezan cuerpo a cuerpo.

    ``reaction_used``: ya ha gastado su reacción desde el inicio de su
    último turno (5e: la reacción se recarga al empezar tu turno; véase
    :func:`dnd_sim.rules.usage.begin_turn`). ``Combatant.reset()`` lo pone a
    ``False`` al empezar un combate nuevo.

    ``attached_to``: criatura sobre la que ESTE combatiente está enganchado
    (p. ej. el Bite del cloaker: «the cloaker attaches to it»). Solo lo
    rellena el que engancha; la criatura enganchada no guarda referencia
    (la búsqueda inversa la hace :func:`dnd_sim.rules.attach.enganchador_de`).
    Vive aquí (y no como condición) porque es una relación entre dos
    criaturas con reglas propias: reparto de daño, ventaja y desenganche.
    ``Combatant.reset()`` lo limpia al empezar un combate nuevo.
    """

    at_range: bool = False
    reaction_used: bool = False
    attached_to: Any = None
    # ¿Quién le ha marcado? (p. ej. Protectores Ancestrales: quien está
    # marcado tiene desventaja salvo al atacar contra su marcador y su
    # daño a otros se resiste). Lo marca el rasgo del marcador y lo
    # limpia el propio marcador al acabar el efecto (y Combatant.reset()).
    marked_by: Any = None
    # ¿Ha tirado un ataque en su propio turno? (Furia: extiende la duración.)
    # Lo pone el motor en ``attack_roll`` y lo limpia ``begin_turn``.
    attacked_this_turn: bool = False
    # ¿Ha obligado a un enemigo a tirar salvación en su propio turno?
    # (Furia: otra vía de extensión.) Lo pone ``resolve_save_damage`` y lo
    # limpia ``begin_turn``.
    forced_save_this_turn: bool = False


__all__ = ["CombatState"]

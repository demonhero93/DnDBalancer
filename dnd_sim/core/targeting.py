"""Selección de objetivos: hostiles vivos (fuente única de verdad).

Todo el simulador elige objetivos con :func:`valid_targets`:

- acciones (``dnd_sim.model.actions``),
- áreas (``dnd_sim.rules.area``),
- condiciones (``dnd_sim.rules.conditions``),
- acciones legendarias (``dnd_sim.rules.legendary``).

Vive en un módulo **sin dependencias** para que todos esos módulos puedan
importarla sin ciclos de importación. ``dnd_sim.model.combatant`` la reexporta
como ``valid_targets`` (API pública histórica).

Además centraliza quién sigue en pie: :func:`living_teams` (equipos con
algún combatiente vivo) y :func:`combat_finished` (solo queda un bando),
que usan el bucle del combate y la fase legendaria para dar el encuentro
por terminado en cuanto cae el último de un lado.

Reglas: nunca el propio actor, nunca los aliados, nunca los muertos.
"""
from __future__ import annotations

from typing import Any


def _objetivo_enganche(actor: Any, atk: Any) -> Any:
    """Criatura enganchada si ``atk`` queda restringido a ella (o ``None``).

    Lee ``CombatState.attached_to`` del atacante y los ``on_hit_effects``
    del ataque (duck-typing: este módulo no tiene dependencias).
    """
    enganchado = getattr(getattr(actor, "state", None), "attached_to", None)
    if enganchado is None or not getattr(enganchado, "alive", True):
        return None
    for efecto in getattr(atk, "on_hit_effects", None) or []:
        if getattr(efecto, "restringe_a_enganchado", False):
            return enganchado
    return None


def valid_targets(actor: Any, ctx: Any = None, combatants: Any = None,
                  enemies: Any = None, atk: Any = None) -> list:
    """Objetivos hostiles vivos de ``actor``.

    Parámetros
    ----------
    actor:
        Combatiente que ataca (el que busca objetivos hostiles).
    ctx:
        Contexto de combate: se usa para obtener la lista de combatientes
        (``ctx.combatants`` o ``ctx.enemies``) si no se pasan explícitamente.
    combatants:
        Lista explícita de combatientes (tiene prioridad sobre ``ctx``).
    enemies:
        Alias de ``combatants`` (compatibilidad).
    atk:
        Ataque concreto para el que se piden objetivos (opcional). Si el
        actor está enganchado y el ataque lleva enganche (Bite del
        cloaker), solo devuelve la criatura enganchada: «can make this
        attack only against the target». Las acciones que no son ese ataque
        (Moan, alientos, salvaciones, hechizos) no lo pasan y no se
        restringen.

    No consume RNG.
    """
    if combatants is None:
        if enemies is not None:
            combatants = enemies
        elif ctx is not None:
            combatants = getattr(ctx, "combatants", None)
            if combatants is None:
                combatants = getattr(ctx, "enemies", None)
        else:
            combatants = None
    if combatants is None:
        return []
    result = []
    for c in combatants:
        if c is actor:
            continue
        if not getattr(c, "alive", True):
            continue
        try:
            if actor.is_hostile_to(c):
                result.append(c)
        except Exception:
            pass
    # Restricción de enganche (solo con un ataque concreto que la declare).
    if atk is not None:
        restringido = _objetivo_enganche(actor, atk)
        if restringido is not None:
            filtrado = [c for c in result if c is restringido]
            if filtrado:
                result = filtrado
    return result


def living_teams(combatants: Any) -> set:
    """Equipos (``"PJ"``/``"NPC"``) con algún combatiente en pie.

    Como :func:`valid_targets`, es duck-typed y no consume RNG: lee
    ``alive`` y ``team`` de cada combatiente.
    """
    equipos: set = set()
    for c in combatants or []:
        if not getattr(c, "alive", False):
            continue
        equipo = getattr(c, "team", None)
        if equipo is not None:
            equipos.add(equipo)
    return equipos


def combat_finished(combatants: Any) -> bool:
    """¿Solo queda un equipo (o ninguno) en pie?

    Es el fin **inmediato** del combate: en cuanto el daño deja a 0 PV al
    último de un bando (PJ o NPC) y lo marca muerto, ni su bando ni el
    contrario vuelven a actuar.
    """
    return len(living_teams(combatants)) <= 1


__all__ = ["valid_targets", "living_teams", "combat_finished"]

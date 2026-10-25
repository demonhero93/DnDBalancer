"""Represalias del lanzador: cuando recibe daño mientras
sostiene un hechizo, la acción de reacción que puede usar."""

from __future__ import annotations

from typing import Any

from ...model.actions import ActionType, CombatContext, TurnResources
from ...core.randomness import pick


def _contexto_de_reaccion(victim: Any, ctx: Any) -> CombatContext:
    """Contexto de combate con ``victim`` como actor (para su reacción).

    Copia las estadísticas compartidas del combate para que el lanzamiento
    cuente en los mismos contadores. Los recursos llevan la reacción ya
    marcada como usada (evita reentrancias dentro de la propia reacción).
    """
    return CombatContext(
        rng=ctx.rng,
        actor=victim,
        combatants=list(getattr(ctx, "combatants", None) or []),
        round=int(getattr(ctx, "round", 0) or 0),
        log=getattr(ctx, "log", None),
        verbose=bool(getattr(ctx, "verbose", False)),
        resources=TurnResources(reaction_used=True),
        action_uses=getattr(ctx, "action_uses", None),
        area_targets_hit=getattr(ctx, "area_targets_hit", None),
        conditions_applied=getattr(ctx, "conditions_applied", None),
        escape_attempts=getattr(ctx, "escape_attempts", None),
        escape_successes=getattr(ctx, "escape_successes", None),
        attacks_at_range=getattr(ctx, "attacks_at_range", None),
        legendary_stats=getattr(ctx, "legendary_stats", None),
    )


def trigger_reaction(victim: Any, ctx: Any) -> bool:
    """Dispara una acción de reacción de ``victim`` si acaba de recibir daño.

    Aproximación de las reglas 5e: **una reacción por turno propio**. El
    indicador ``state.reaction_used`` se pone a ``False`` al inicio del turno
    (:func:`dnd_sim.rules.usage.begin_turn`) y se marca (antes de ejecutar) al
    usar la reacción, así que las cadenas de reacciones terminan siempre.

    Solo actúa si el combate sigue vivo (más de un bando), ``victim`` está
    vivo y puede actuar, y tiene una acción de reacción disponible; si esa
    acción tiene uso limitado, se gasta aquí (el motor de combate no la ve:
    ocurre fuera del turno de ``victim``). Devuelve True si se disparó.
    """
    if victim is None or ctx is None:
        return False
    if not getattr(victim, "alive", True):
        return False
    if not getattr(victim, "can_act", True):
        return False
    state = getattr(victim, "state", None)
    if state is not None and getattr(state, "reaction_used", False):
        return False
    combatants = list(getattr(ctx, "combatants", None) or [])
    if not combatants:
        # Contexto parcial (p. ej. riders de un ataque): no se modela.
        return False
    teams = {getattr(c, "team", None) for c in combatants
             if getattr(c, "alive", False)}
    if len(teams) <= 1:
        return False  # el combate ya está decidido: no hay reacciones.
    frescos = TurnResources()  # la reacción del victim está disponible
    candidatas = [
        a for a in getattr(victim, "actions", []) or []
        if getattr(a, "action_type", None) is ActionType.REACTION
        and a.can_use(frescos)
    ]
    if not candidatas:
        return False
    sub = _contexto_de_reaccion(victim, ctx)
    if state is not None:
        state.reaction_used = True
    elegida = pick(sub.rng, candidatas)
    log = sub.log
    if log is not None:
        log.append(f"  {getattr(victim, 'name', victim)} reacciona con "
                   f"{getattr(elegida, 'name', 'una acción de reacción')}")
    try:
        elegida.execute(sub)
    except Exception:
        return False
    usage = getattr(elegida, "usage", None)
    if usage is not None:
        usage.spend()
    acciones = getattr(ctx, "action_uses", None)
    if acciones is not None:
        nombre = getattr(elegida, "name", "") or type(elegida).__name__
        acciones[nombre] = acciones.get(nombre, 0) + 1
    return True

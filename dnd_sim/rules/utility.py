"""Utilitarias de combate: Esquivar, Agarrar y Empujar (PHB 2024).

Tres mecánicas con una misma puerta de decisión:

- **Disponibilidad primero, probabilidad después**: solo si la utilitaria
  se puede usar ahora (vivo, puede actuar, hay objetivos...) se consulta
  :func:`debe_usar_utilitaria`; sin disponibilidad no se consume RNG.
- ``UTILITY_ACTION_PROBABILITY`` (CLI ``--utility-p``) es la probabilidad
  de usarla en vez del ataque/acción previsto. ``p<=0`` y ``p>=1`` no
  consumen RNG; entre 0 y 1, un solo ``rng.random()`` por decisión.
- **Esquivar** sustituye la ACTION entera (la crea ``encounter.py``);
  **Agarrar/Empujar** sustituyen un ataque dentro del bucle de ataques
  (:mod:`dnd_sim.model.actions`).
"""
from __future__ import annotations

from typing import Any

from ..core.enums import AttackRange
from ..core.log import log_line
from ..core.randomness import pick
from ..core.targeting import valid_targets
from ..model.actions import ActionType, CombatAction
from .conditions import Condition, EscapeCheck, apply_condition
from .saves import registrar_resistencia, saving_throw

# Probabilidad de usar una utilitaria en vez de lo previsto. 0 = nunca
# (sin RNG), 1 = siempre (sin RNG). En entre 0 y 1 consume un random()
# por decisión con disponibilidad.
UTILITY_ACTION_PROBABILITY = 0.05

__all__ = [
    "UTILITY_ACTION_PROBABILITY",
    "debe_usar_utilitaria",
    "hay_utilitaria_accion",
    "DodgeAction",
    "ataque_utilitario",
]


def debe_usar_utilitaria(rng: Any) -> bool:
    """¿Toca usar una utilitaria? (probabilidad, con convención anti-RNG)

    ``p<=0`` → False sin consumir RNG; ``p>=1`` → True sin consumir RNG;
    si no, un único ``rng.random()``. ``rng=None`` nunca decide.
    """
    p = UTILITY_ACTION_PROBABILITY
    if p <= 0:
        return False
    if p >= 1:
        return True
    if rng is None:
        return False
    return rng.random() < p


def hay_utilitaria_accion(actor: Any) -> bool:
    """Disponibilidad estructural de una utilitaria de acción (sin RNG).

    Vivo, puede actuar y sin estar ya esquivando (la esquiva dura hasta el
    próximo turno propio).
    """
    if not getattr(actor, "alive", True):
        return False
    if not getattr(actor, "can_act", True):
        return False
    state = getattr(actor, "state", None)
    if state is not None and getattr(state, "dodging", False):
        return False
    return True


class DodgeAction(CombatAction):
    """Esquivar (ACTION): hasta el próximo turno propio, los ataques
    contra quien esquiva tienen desventaja y gana ventaja en salvaciones
    de Destreza (pérdida automática al quedar incapacitado)."""

    name = "Esquivar"
    action_type = ActionType.ACTION
    usage = None

    def execute(self, context: Any) -> None:
        actor = getattr(context, "actor", None)
        if actor is not None and not getattr(actor, "alive", True):
            return
        state = getattr(actor, "state", None)
        if state is None:
            return
        state.dodging = True
        log_line(context, f"{getattr(actor, 'name', actor)} esquiva")


def _condiciones(combatant: Any) -> set:
    tracker = getattr(combatant, "conditions", None)
    if tracker is None:
        return set()
    try:
        return set(tracker.active())
    except Exception:
        return set()


def _agarrando(actor: Any, combatants: Any) -> bool:
    """¿Tiene ya agarrada a alguna criatura? (instancia GRAPPLED con
    ``source == actor``: la condición vive en el objetivo, no en el que
    agarra)."""
    for c in combatants or []:
        tracker = getattr(c, "conditions", None)
        if tracker is None:
            continue
        for inst in getattr(tracker, "instances", []) or []:
            if inst.condition is Condition.GRAPPLED and inst.source is actor:
                return True
    return False


# Orden de tamaños PHB (solo para el límite de Agarrar).
_TAMANOS = ("tiny", "small", "medium", "large", "huge", "gargantuan")


def _orden_tamano(combatiente: Any) -> int:
    """Posición del tamaño del combatiente (desconocido = medium)."""
    tamaño = str(getattr(combatiente, "size", None) or "medium").strip().lower()
    if tamaño not in _TAMANOS:
        return _TAMANOS.index("medium")
    return _TAMANOS.index(tamaño)


# shortcut: Agarrar/Empujar sustituye cualquier ataque del bucle, no solo
# el Desarmado; si algún día hay decisión táctica, restringir aquí.
def ataque_utilitario(actor: Any, ctx: Any, rng: Any, atk: Any = None) -> bool:
    """Sustituye un ataque por Agarrar o Empujar si toca. Devuelve True si
    el ataque ha quedado sustituido (ya resuelto).

    Sin RNG hasta que hay disponibilidad: objetivos hostiles, actor sin
    nadie agarrado (para Agarrar), objetivo sin derribar (para Empujar) y
    tamaño del objetivo como máximo uno mayor que el actor (Agarrar).
    Un ataque a distancia nunca se sustituye.
    """
    if rng is None or ctx is None:
        return False
    if not hay_utilitaria_accion(actor):
        return False
    if (atk is not None
            and getattr(atk, "range_type", AttackRange.MELEE) is AttackRange.RANGED):
        return False
    combatants = getattr(ctx, "combatants", None) or []
    objetivos = valid_targets(actor, ctx=ctx)
    if not objetivos:
        return False
    if _agarrando(actor, combatants):
        pool_agarrar = []
    else:
        maximo = _orden_tamano(actor) + 1
        pool_agarrar = [t for t in objetivos if _orden_tamano(t) <= maximo]
    pool_empujar = [t for t in objetivos if Condition.PRONE not in _condiciones(t)]
    if not pool_agarrar and not pool_empujar:
        return False
    if not debe_usar_utilitaria(rng):
        return False
    if pool_agarrar and pool_empujar:
        tipo = pick(rng, ["agarrar", "empujar"])
    else:
        tipo = "agarrar" if pool_agarrar else "empujar"
    objetivo = pick(rng, pool_agarrar if tipo == "agarrar" else pool_empujar)

    dc = 8 + actor.abilities.mod("str") + int(getattr(actor, "proficiency", 2))
    nombre = getattr(actor, "name", actor)
    log_line(ctx, f"{nombre} intenta {tipo} a "
                  f"{getattr(objetivo, 'name', objetivo)}")
    habilidad = pick(rng, ["str", "dex"])
    sr = saving_throw(objetivo, habilidad, dc, rng, magical=False, ctx=ctx)
    sr = registrar_resistencia(ctx, objetivo, sr)
    if sr.success:
        log_line(ctx, f"  salvación {habilidad.upper()} {sr.total} vs CD {dc}: "
                      f"sin efecto")
        return True
    log_line(ctx, f"  falla la salvación {habilidad.upper()} "
                  f"({sr.total} vs CD {dc})")
    if tipo == "agarrar":
        apply_condition(
            objetivo, Condition.GRAPPLED, ctx, source=actor,
            escape=EscapeCheck(abilities=("str", "dex"), dc=dc,
                               consumes_action=True))
    else:
        # Sin sistema de movimiento: ponerse en pie se modela como prueba
        # automática de FUE/DES CD 10 al inicio del turno (attempt_escapes).
        apply_condition(
            objetivo, Condition.PRONE, ctx, source=actor,
            escape=EscapeCheck(abilities=("str", "dex"), dc=10,
                               consumes_action=False))
    return True

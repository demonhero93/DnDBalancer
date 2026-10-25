"""Políticas de decisión para el combate (aleatoria pura)."""
from __future__ import annotations

from ..core.randomness import pick


def _extract(args, kwargs):
    ctx = kwargs.get("ctx") or kwargs.get("context")
    choices = kwargs.get("choices") or kwargs.get("options") or kwargs.get("actions")
    rng = kwargs.get("rng")
    for arg in args:
        if hasattr(arg, "rng") and hasattr(arg, "actor"):
            ctx = arg
        elif isinstance(arg, (list, tuple)):
            choices = list(arg)
        elif hasattr(arg, "randint"):
            rng = arg
    if ctx is not None:
        if choices is None:
            choices = getattr(ctx, "available_actions", None)
        if rng is None:
            rng = getattr(ctx, "rng", None)
    return ctx, (list(choices) if choices is not None else None), rng


def random_policy(*args, **kwargs):
    """Elige uniformemente entre las opciones disponibles (si hay una sola,
    no consume el RNG gracias a :func:`pick`).

    Las opciones ya vienen filtradas por ``can_use`` (turno y uso limitado),
    así que una acción agotada (p. ej. un aliento descargado) nunca se elige.
    Un dragón con Multiataque y Aliento **cargado** elige entre ambos con
    ~50%: la política no es estratégica, es uniforme.
    """
    ctx, choices, rng = _extract(args, kwargs)
    if not choices:
        return None
    return pick(rng, choices)


def first_target_policy(*args, **kwargs):
    """Política anterior: siempre la primera opción disponible (determinista)."""
    ctx, choices, rng = _extract(args, kwargs)
    if not choices:
        return None
    return choices[0]


# Alias de compatibilidad con el nombre antiguo.
default_policy = random_policy

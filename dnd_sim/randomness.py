"""Utilidades de aleatoriedad reproducible (elección uniforme)."""
from __future__ import annotations

import random
from typing import TypeVar

T = TypeVar("T")


def pick(rng: random.Random, options):
    """Elige un elemento **uniformemente** de ``options``.

    Convención importante: si ``options`` tiene un único elemento, lo devuelve
    **sin consumir** el RNG. Esto permite que los combates con una sola
    opción real conserven exactamente la misma secuencia de tiradas que antes
    de introducir decisiones aleatorias.

    ``options`` puede ser cualquier secuencia (list, tuple, ...). Si está
    vacía se lanza ``IndexError``/``ValueError``.
    """
    seq = list(options)
    if not seq:
        raise ValueError("pick() necesita al menos una opción")
    if len(seq) == 1:
        return seq[0]
    return seq[rng.randrange(len(seq))]

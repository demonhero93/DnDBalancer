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


def sample(rng: random.Random, options, k: int):
    """Elige ``k`` elementos **distintos** de ``options`` sin reemplazo.

    Se apoya en :func:`pick`, así que si queda una sola opción disponible no
    se consume el RNG (misma convención que el resto del simulador).

    Si ``k >= len(options)`` devuelve **todos** los elementos **sin consumir
    el RNG** (no hace falta sortear nada).
    """
    pool = list(options)
    total = len(pool)
    count = int(k)
    if count >= total:
        return pool
    if count <= 0:
        return []
    chosen = []
    for _ in range(count):
        item = pick(rng, pool)
        chosen.append(item)
        # Se elimina por identidad para no confundir objetos iguales.
        for pos, candidate in enumerate(pool):
            if candidate is item:
                pool.pop(pos)
                break
    return chosen

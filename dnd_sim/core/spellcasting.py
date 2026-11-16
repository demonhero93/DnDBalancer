"""Espacios de conjuro y definición de lanzador de PJ (PHB 2024).

Datos puros de la **capa core**: las tres tablas de progresión de
espacios (lanzador total, media y tercio) y la definición de un
lanzador de PJ (:class:`SpellcastingDef`), sin dependencias internas.

Las tablas devuelven la tupla de espacios por nivel de hechizo 1..9
**sin ceros finales** (nivel 3 de lanzador total → ``(4, 2)``); un
nivel sin espacios (o por debajo del mínimo de la progresión) → ``()``.

El Brujo (Pact Magic) queda FUERA de alcance: su tabla es propia y no
es una de estas progresiones (ver TODO.md).
"""
from __future__ import annotations

from dataclasses import dataclass, field

#: Lanzador total (bardo, clérigo, druída, hechicero, mago; 2024).
FULL_SLOTS: dict[int, tuple[int, ...]] = {
     1: (2,), 2: (3,), 3: (4, 2), 4: (4, 3), 5: (4, 3, 2),
     6: (4, 3, 3), 7: (4, 3, 3, 1), 8: (4, 3, 3, 2),
     9: (4, 3, 3, 3, 1), 10: (4, 3, 3, 3, 2), 11: (4, 3, 3, 3, 2, 1),
    12: (4, 3, 3, 3, 2, 1), 13: (4, 3, 3, 3, 2, 1, 1),
    14: (4, 3, 3, 3, 2, 1, 1), 15: (4, 3, 3, 3, 2, 1, 1, 1),
    16: (4, 3, 3, 3, 2, 1, 1, 1), 17: (4, 3, 3, 3, 2, 1, 1, 1, 1),
    18: (4, 3, 3, 3, 3, 1, 1, 1, 1), 19: (4, 3, 3, 3, 3, 2, 1, 1, 1),
    20: (4, 3, 3, 3, 3, 2, 2, 1, 1),
}

#: Semilanzador 2024 (paladín, explorador).
HALF_SLOTS: dict[int, tuple[int, ...]] = {
     1: (2,), 2: (2,), 3: (3,), 4: (3,), 5: (4, 2), 6: (4, 2),
     7: (4, 3), 8: (4, 3), 9: (4, 3, 2), 10: (4, 3, 2),
    11: (4, 3, 3), 12: (4, 3, 3), 13: (4, 3, 3, 1), 14: (4, 3, 3, 1),
    15: (4, 3, 3, 2), 16: (4, 3, 3, 2), 17: (4, 3, 3, 3, 1),
    18: (4, 3, 3, 3, 1), 19: (4, 3, 3, 3, 2), 20: (4, 3, 3, 3, 2),
}

#: Tercio de lanzador (guerrero mágico, pícaro mágico): empieza en 3.
THIRD_SLOTS: dict[int, tuple[int, ...]] = {
     3: (2,), 4: (3,), 5: (3,), 6: (3,), 7: (4, 2), 8: (4, 2),
     9: (4, 2), 10: (4, 3), 11: (4, 3), 12: (4, 3), 13: (4, 3, 2),
    14: (4, 3, 2), 15: (4, 3, 2), 16: (4, 3, 3), 17: (4, 3, 3),
    18: (4, 3, 3), 19: (4, 3, 3, 1), 20: (4, 3, 3, 1),
}

#: Progresión → tabla de espacios por nivel de lanzador.
_TABLAS: dict[str, dict[int, tuple[int, ...]]] = {
    "full": FULL_SLOTS,
    "half": HALF_SLOTS,
    "third": THIRD_SLOTS,
}

#: Progresiones válidas (Pact Magic del brujo no está).
PROGRESIONES: tuple[str, ...] = ("full", "half", "third")


def spell_slots_for(progresion: str, nivel: int) -> tuple[int, ...]:
    """Espacios de conjuro de un lanzador (niveles de hechizo 1..9).

    ``progresion`` es ``"full"``, ``"half"`` o ``"third"``. Devuelve la
    tupla de la tabla **sin ceros finales**: nivel 1 de lanzador total
    → ``(2,)``; nivel 3 total → ``(4, 2)``. Un nivel por debajo del
    mínimo de la progresión (tercio: 1-2) → ``()``: sin espacios.

    Lanza ``ValueError`` con la progresión desconocida.
    """
    clave = str(progresion or "").strip().lower()
    tabla = _TABLAS.get(clave)
    if tabla is None:
        raise ValueError(
            f"Progresión de lanzamiento desconocida {progresion!r}: "
            f"válidas {sorted(_TABLAS)}."
        )
    try:
        lvl = int(nivel)
    except (TypeError, ValueError):
        return ()
    return tabla.get(lvl, ())


@dataclass
class SpellcastingDef:
    """Definición de lanzamiento de una clase jugable (datos puros).

    - ``progresion``: ``"full"`` / ``"half"`` / ``"third"`` (tabla de
      espacios; ver :func:`spell_slots_for`).
    - ``caracteristica``: clave de característica de lanzamiento
      (``"int"``, ``"wis"`` o ``"cha"``).
    - ``lista_clase``: índice de la clase en la API de donde se carga
      su lista de hechizos (capa ``data``).
    - ``trucos_conocidos`` / ``preparados``: conteos por **nivel de PJ**
      (trucos conocidos y hechizos preparados).
    - ``escuelas``: si no es ``None``, restringe el pool a esas escuelas
      (índices en inglés, p. ej. ``("evocation",)``).
    - ``min_level``: nivel mínimo de PJ con esta definición.
    """

    progresion: str
    caracteristica: str
    lista_clase: str
    trucos_conocidos: dict[int, int] = field(default_factory=dict)
    preparados: dict[int, int] = field(default_factory=dict)
    escuelas: tuple[str, ...] | None = None
    min_level: int = 1

    def __post_init__(self) -> None:
        clave = str(self.progresion or "").strip().lower()
        if clave not in _TABLAS:
            raise ValueError(
                f"Progresión de lanzamiento desconocida {self.progresion!r}: "
                f"válidas {sorted(_TABLAS)}."
            )
        self.progresion = clave
        self.caracteristica = str(self.caracteristica or "").strip().lower()
        self.min_level = max(1, int(self.min_level or 1))

    def espacios(self, nivel: int) -> tuple[int, ...]:
        """Espacios en ``nivel`` de PJ; ``()`` si no alcanza ``min_level``."""
        lvl = int(nivel or 0)
        if lvl < self.min_level:
            return ()
        return spell_slots_for(self.progresion, lvl)


__all__ = [
    "FULL_SLOTS",
    "HALF_SLOTS",
    "THIRD_SLOTS",
    "PROGRESIONES",
    "SpellcastingDef",
    "spell_slots_for",
]

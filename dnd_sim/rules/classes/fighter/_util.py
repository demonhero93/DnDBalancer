"""Utilidades compartidas de las subclases del Fighter.

``_de`` estaba duplicada (copia literal) en los ocho módulos de
subclase y ``_orden_tamano``/``_TAMANOS`` en dos (Battle Master y
Rune Knight): una sola definición aquí, importada desde cada subclase
(patrón ``_contexto``/``_es_aliado`` de :mod:`features`).
"""
from __future__ import annotations

from typing import Any

#: Orden de tamaños PHB (límite de Trip: Grande o menor; patrón utility).
_TAMANOS = ("tiny", "small", "medium", "large", "huge", "gargantuan")


def _de(actor: Any, clase: type) -> Any:
    """Primer trait de ``clase`` que lleve ``actor`` (o ``None``)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


def _orden_tamano(valor: Any) -> int:
    """Orden PHB de un tamaño (acepta combatiente o cadena de tamaño)."""
    tamaño = str(getattr(valor, "size", valor) or "medium").strip().lower()
    if tamaño not in _TAMANOS:
        return _TAMANOS.index("medium")
    return _TAMANOS.index(tamaño)


__all__ = ["_TAMANOS", "_de", "_orden_tamano"]

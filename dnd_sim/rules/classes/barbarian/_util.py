"""Utilidades compartidas de las subclases del Barbarian.

`_de` estaba duplicada (copia literal) en ocho módulos de subclase,
`_orden_de` en dos (giant y wild_heart) y `_furia_de` en dos
(berserker y zealot): una sola definición aquí, importada desde cada
subclase (patrón `_contexto`/`_rasgo` de :mod:`features`).
"""
from __future__ import annotations

from typing import Any

from ...utility import _TAMANOS
from .features import RageAction


def _de(actor: Any, clase: type) -> Any:
    """Primer rasgo de ``actor`` que sea instancia de ``clase`` (o None)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


def _orden_de(valor: Any) -> int:
    """Orden PHB de un tamaño (acepta combatiente o cadena de tamaño)."""
    tamaño = str(getattr(valor, "size", valor) or "medium").strip().lower()
    if tamaño not in _TAMANOS:
        return _TAMANOS.index("medium")
    return _TAMANOS.index(tamaño)


def _furia_de(actor: Any) -> RageAction | None:
    """La acción «Entrar en Furia» de ``actor`` (o None)."""
    for accion in getattr(actor, "actions", None) or []:
        if isinstance(accion, RageAction):
            return accion
    return None


__all__ = ["_de", "_furia_de", "_orden_de"]

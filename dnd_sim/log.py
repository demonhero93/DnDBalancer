"""Registro de líneas en el log del combate.

Función compartida por todos los módulos que añaden una línea al log del
contexto (``ctx.log``): antes estaba copiada como ``_log_line`` en siete
módulos (area, attach, conditions, legendary, saves, traits y usage).

Si el contexto no tiene log (combate no ``verbose``) no se hace nada y las
excepciones al escribir jamás interrumpen un combate.
"""
from __future__ import annotations

from typing import Any


def log_line(ctx: Any, line: str) -> None:
    """Añade ``line`` al log del combate si el contexto lo tiene."""
    log = getattr(ctx, "log", None)
    if log is None:
        return
    try:
        log.append(line)
    except Exception:
        pass


__all__ = ["log_line"]

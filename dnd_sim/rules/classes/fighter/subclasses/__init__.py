"""Subclases del Fighter: Arcane Archer (paquete listo para crecer).

La receta para añadir otra está en ``TODO.md`` (sección «Fighter: cómo
añadir una subclase»): un módulo por subclase con su ``SubclassDef``,
registro en ``..__init__`` y reexport en la fachada.
"""
from __future__ import annotations

from .arcane_archer import ARCANE_SHOTS, ArcaneArcherFeatures, apply_arcane_archer

__all__ = ["ARCANE_SHOTS", "ArcaneArcherFeatures", "apply_arcane_archer"]

"""Transfondos (backgrounds): datos puros de sus competencias.

Primitiva de la **capa core**: solo el resultado del parseo (skills,
herramientas e idiomas), sin red ni dependencias. La descarga y el
parseo del JSON viven en :mod:`dnd_sim.data.background_parser`.

Regla 5e: el transfondo aporta competencias de **habilidad** y de
**herramientas/idiomas**; las salvaciones salen solo de la clase.
"""
from __future__ import annotations

from dataclasses import dataclass, field


def normalize_tool(value) -> str:
    """Nombre canónico de una herramienta: minúsculas y guiones.

    ``"Thieves' Tools"`` -> ``"thieves-tools"``.
    """
    text = str(value).replace("'", "").strip().lower()
    return "-".join(text.replace("_", " ").split())


@dataclass
class Background:
    """Competencias que aporta un transfondo (antecedente)."""

    index: str = ""
    name: str = ""
    skill_proficiencies: set[str] = field(default_factory=set)
    tool_proficiencies: set[str] = field(default_factory=set)
    languages: set[str] = field(default_factory=set)


__all__ = ["Background", "normalize_tool"]

"""Razas (species en la API 2024): competencias y hechizos que aportan.

Primitiva de la **capa core**: solo el resultado del parseo. Los bonos de
carácter de la raza (fuerza/des/...) **no** se recogen aquí: se asumen ya
reflejados en las características del personaje.

Regla 5e: la raza aporta competencias de habilidad (fijas o a elegir) y
hechizos/cantrips que el personaje aprende (p. ej. el linaje del elfo).
Las salvaciones salen solo de la clase.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Race:
    """Competencias y hechizos que aporta una raza (species)."""

    index: str = ""
    name: str = ""
    # Competencias fijas de habilidad (ya normalizadas).
    skill_proficiencies: tuple[str, ...] = ()
    # Habilidades a elegir (en el orden que da la API; se toma la primera
    # al aplicar, salvo que se pida otra).
    skill_choices: tuple[str, ...] = ()
    # Hechizos/cantrips que aprende (nombres tal cual los trae la API).
    spells: tuple[str, ...] = ()


__all__ = ["Race"]

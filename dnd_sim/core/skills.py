"""Habilidades de D&D 5e: registro (habilidad -> característica) y alias.

Primitiva de la **capa core**: la tabla es pura (sin dependencias
internas), así que ``model``, ``rules`` y ``data`` pueden importarla sin
riesgo de ciclo de importación.

Las 18 habilidades del PHB se identifican por su nombre en inglés con
guiones (``"sleight-of-hand"``), el mismo formato que usa la API de
dnd5eapi.co (``skill-sleight-of-hand``).
"""
from __future__ import annotations

import unicodedata

# Habilidad -> característica asociada (18 habilidades del PHB).
SKILL_ABILITIES: dict[str, str] = {
    "acrobatics": "dex",
    "animal-handling": "wis",
    "arcana": "int",
    "athletics": "str",
    "deception": "cha",
    "history": "int",
    "insight": "wis",
    "intimidation": "cha",
    "investigation": "int",
    "medicine": "wis",
    "nature": "int",
    "perception": "wis",
    "performance": "cha",
    "persuasion": "cha",
    "religion": "int",
    "sleight-of-hand": "dex",
    "stealth": "dex",
    "survival": "wis",
}

# Característica -> habilidad por defecto. Solo FUE y DES tienen una
# habilidad directa (Atletismo y Acrobacias); las demás características no
# tienen par único en el PHB, así que no se mapean.
DEFAULT_SKILL_BY_ABILITY: dict[str, str] = {
    "str": "athletics",
    "dex": "acrobatics",
}

# Nombres en español (PHB) y variantes de texto libre -> clave canónica.
# Las claves ya van sin acentos ni mayúsculas (ver ``_clean``).
_SKILL_ALIASES: dict[str, str] = {
    "acrobacias": "acrobatics",
    "manejo-de-animales": "animal-handling",
    "arcano": "arcana",
    "conocimiento-arcano": "arcana",
    "atletismo": "athletics",
    "engano": "deception",
    "historia": "history",
    "intuicion": "insight",
    "intimidacion": "intimidation",
    "investigacion": "investigation",
    "medicina": "medicine",
    "naturaleza": "nature",
    "percepcion": "perception",
    "actuacion": "performance",
    "persuasion": "persuasion",
    "religion": "religion",
    "juego-de-manos": "sleight-of-hand",
    "sigilo": "stealth",
    "supervivencia": "survival",
}


def _clean(value) -> str:
    """Minúsculas, sin acentos, espacios/guiones bajos -> guiones."""
    text = unicodedata.normalize("NFD", str(value))
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = text.strip().lower().replace("_", " ")
    return "-".join(text.split())


def normalize_skill(value) -> str:
    """Nombre canónico de una habilidad (lanza ``ValueError`` si no existe).

    Acepta inglés con espacios o guiones (``"sleight of hand"``) y
    español con o sin acentos (``"Acrobacias"``, ``"Conocimiento arcano"``).
    """
    text = _clean(value)
    text = _SKILL_ALIASES.get(text, text)
    if text not in SKILL_ABILITIES:
        raise ValueError(f"habilidad desconocida: {value!r}")
    return text


def skill_ability(skill) -> str:
    """Característica asociada a una habilidad (``"stealth"`` -> ``"dex"``)."""
    return SKILL_ABILITIES[normalize_skill(skill)]


__all__ = ["DEFAULT_SKILL_BY_ABILITY", "SKILL_ABILITIES",
           "normalize_skill", "skill_ability"]

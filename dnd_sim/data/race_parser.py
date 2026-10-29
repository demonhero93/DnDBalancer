"""Parsea las razas (species) de la API de dnd5eapi.co.

Solo se descarga la raza que se pide (:func:`load_race`) y, de camino,
sus rasgos (``/traits/...`), que es donde viven las competencias y los
hechizos. De cada raza se quedan:

- habilidades fijas: ``starting_proficiencies``/``proficiencies`` de la
  raza y las fijas de sus rasgos;
- habilidades a elegir: ``proficiency_choices`` de cada rasgo (p. ej.
  Keen Senses), en el orden de la API;
- hechizos que aprende: se leen de la **descripción** del rasgo con
  frases fijas del SRD («know the X cantrip», «learn the X spell» y
  tablas «Level N. X»). No hay campo estructurado en la API.

Los bonos de carácter de la raza no se recogen: se asumen ya aplicados
en el personaje.
"""
from __future__ import annotations

import re
from typing import Iterable

from ..core.races import Race
from ..core.skills import normalize_skill
from .api_client import get_race, get_trait

# Frases fijas del SRD que otorgan un hechizo.
_CANTRIP_RE = re.compile(r"know the (.+?) cantrip", re.IGNORECASE)
_LEARN_RE = re.compile(r"learn the (.+?) spell", re.IGNORECASE)
# Filas de tabla «Level 3. Faerie Fire» al inicio de línea.
_LEVEL_RE = re.compile(r"^Level \d+\.\s*(.+)$", re.MULTILINE)


def _skill_name(raw) -> str | None:
    """Normaliza una habilidad venga como índice (``skill-*``) o nombre.

    Devuelve ``None`` si no es una habilidad conocida.
    """
    if isinstance(raw, dict):
        raw = raw.get("index") or raw.get("name")
    if not isinstance(raw, str) or not raw.strip():
        return None
    text = raw.strip()
    if text.lower().startswith("skill-"):
        text = text[len("skill-"):]
    try:
        return normalize_skill(text)
    except ValueError:
        return None


def _spells_from_description(text: str) -> list[str]:
    """Extrae los hechizos/cantrips de la descripción de un rasgo."""
    found: list[str] = []

    def _add(name: str) -> None:
        name = name.strip()
        if not name or not name[0].isupper() or len(name) > 40:
            return
        if name not in found:
            found.append(name)

    for match in _CANTRIP_RE.finditer(text):
        _add(match.group(1))
    for match in _LEARN_RE.finditer(text):
        _add(match.group(1))
    for match in _LEVEL_RE.finditer(text):
        rest = match.group(1).strip()
        # Líneas de tabla («Level 3. Faerie Fire»); la prosa de la tabla
        # («Level 1. You have Resistance...») se salta y su hechizo lo
        # recoge la frase de «know the ... cantrip».
        if "." in rest or rest.startswith("You"):
            continue
        _add(rest)
    return found


def _trait_skills(trait: dict) -> tuple[list[str], list[str]]:
    """Competencias de un rasgo: (fijas, a elegir) ya normalizadas."""
    fixed: list[str] = []
    for raw in trait.get("proficiencies") or []:
        name = _skill_name(raw)
        if name and name not in fixed:
            fixed.append(name)

    choices: list[str] = []
    spec = trait.get("proficiency_choices") or []
    if isinstance(spec, dict):
        spec = [spec]
    for block in spec:
        options = (block.get("from") or {}).get("options") or []
        for option in options:
            item = option.get("item") if isinstance(option, dict) else None
            name = _skill_name(item or option)
            if name and name not in choices:
                choices.append(name)
    return fixed, choices


def parse_race(data: dict, traits: Iterable[dict] = ()) -> Race:
    """Raza con sus competencias de habilidad y hechizos aprendidos.

    ``data`` es el JSON de la raza y ``traits`` los JSON de sus rasgos
    (ya descargados); sin rasgos solo se leen las competencias propias.
    """
    skills: list[str] = []
    choices: list[str] = []
    spells: list[str] = []

    for raw in (data.get("starting_proficiencies") or []) + (data.get("proficiencies") or []):
        name = _skill_name(raw)
        if name and name not in skills:
            skills.append(name)

    for trait in traits:
        fixed, trait_choices = _trait_skills(trait)
        for name in fixed:
            if name not in skills:
                skills.append(name)
        for name in trait_choices:
            if name not in choices:
                choices.append(name)
        for spell in _spells_from_description(str(trait.get("description") or "")):
            if spell not in spells:
                spells.append(spell)

    return Race(
        index=str(data.get("index") or ""),
        name=str(data.get("name") or ""),
        skill_proficiencies=tuple(skills),
        skill_choices=tuple(choices),
        spells=tuple(spells),
    )


def load_race(index: str) -> Race:
    """Descarga (o lee de caché) UNA raza y sus rasgos y devuelve la raza."""
    data = get_race(index)
    traits = []
    for ref in data.get("traits") or []:
        trait_index = ref.get("index") if isinstance(ref, dict) else ref
        if trait_index:
            traits.append(get_trait(str(trait_index)))
    return parse_race(data, traits)


__all__ = ["load_race", "parse_race"]

"""Parsea los transfondos (backgrounds) de la API de dnd5eapi.co.

Solo se descarga el transfondo que se pide (:func:`load_background`);
no hay catálogo local de todos. Del JSON se quedan **las competencias**:

- skills: índices ``skill-*`` (forma 2024) o nombres sueltos como
  ``"Insight"`` (forma 2014);
- herramientas: índices ``tool-*``/``instrument-*`` o nombres con
  «Tools»/«Kit»/«Gaming»/«Instrument»;
- idiomas: índices ``language-*``.

Los textos de elección («Choose any two skills...», ``language_options``,
``choices``) se ignoran: la elección ya la hizo el jugador al crear el
personaje, y aquí solo interesa lo que el transfondo da fijo.
"""
from __future__ import annotations

from ..core.backgrounds import Background, normalize_tool
from ..core.skills import normalize_skill
from .api_client import get_background


def _add(raw, skills: set[str], tools: set[str], languages: set[str]) -> None:
    """Clasifica una competencia suelta (índice o nombre)."""
    if not isinstance(raw, str) or not raw.strip():
        return
    text = raw.strip()
    low = text.lower()
    if low.startswith("choose"):
        return  # texto de elección, no una competencia fija.
    if low.startswith("skill-"):
        try:
            skills.add(normalize_skill(low[len("skill-"):]))
        except ValueError:
            pass
    elif low.startswith(("tool-", "instrument-", "gaming-set-")):
        tools.add(normalize_tool(low.split("-", 1)[1]))
    elif low.startswith("language-"):
        languages.add(low[len("language-"):])
    else:
        # Nombre libre (forma 2014): primero se intenta como habilidad.
        try:
            skills.add(normalize_skill(text))
        except ValueError:
            if any(word in low for word in ("tool", "kit", "gaming", "instrument")):
                tools.add(normalize_tool(text))


def parse_background(data: dict) -> Background:
    """Competencias de un transfondo (JSON de la API o de la caché)."""
    skills: set[str] = set()
    tools: set[str] = set()
    languages: set[str] = set()

    # Forma 2024: lista de referencias a proficiencies.
    for entry in data.get("proficiencies") or []:
        if isinstance(entry, str):
            _add(entry, skills, tools, languages)
            continue
        if not isinstance(entry, dict):
            continue
        ref = entry.get("proficiency") if isinstance(entry.get("proficiency"), dict) else entry
        candidate = ref.get("index") or ref.get("name")
        _add(candidate, skills, tools, languages)

    # Forma 2014: nombres libres en starting_proficiencies.
    for entry in data.get("starting_proficiencies") or []:
        _add(entry, skills, tools, languages)

    return Background(
        index=str(data.get("index") or ""),
        name=str(data.get("name") or ""),
        skill_proficiencies=skills,
        tool_proficiencies=tools,
        languages=languages,
    )


def load_background(index: str, **kwargs) -> Background:
    """Descarga (o lee de caché) UN transfondo y devuelve sus competencias."""
    return parse_background(get_background(index, **kwargs))


__all__ = ["load_background", "parse_background"]

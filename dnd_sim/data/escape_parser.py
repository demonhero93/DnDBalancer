"""Parsea las pruebas de escape de la API de dnd5eapi.co.

Formatos reales encontrados (SRD 2014):

- ``giant-spider`` / "Web"::

    "The target is restrained by webbing. As an action, the restrained target
     can make a DC 12 Strength check, bursting the webbing on a success."

  -> prueba de **FUE** con CD 12 y **consume acción** ("As an action").

- ``giant-constrictor-snake`` / "Constrict"::

    "the target is grappled (escape DC 16). Until this grapple ends, the
     creature is restrained"

  -> "escape DC 16" **sin característica**: se usa FUE o DES (a elegir al
  azar) y **no** consume acción.

Vocabulario cerrado (con #: TODO de fragilidad: es texto libre).
"""
from __future__ import annotations

import re
import warnings

try:
    from ..conditions import EscapeCheck
    from ..saves import normalize_ability
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from conditions import EscapeCheck
        from saves import normalize_ability
    except ImportError:
        from dnd_sim.conditions import EscapeCheck
        from dnd_sim.saves import normalize_ability


# "DC 12 Strength check" (prueba explícita con característica).
CHECK_RE = re.compile(r"DC\s*(\d+)\s+(\w+)\s+check", re.IGNORECASE)
# "escape DC 16" (sin característica: FUE o DES).
ESCAPE_DC_RE = re.compile(r"escape\s+DC\s*(\d+)", re.IGNORECASE)
# "As an action" (la prueba consume la acción del afectado).
AS_AN_ACTION_RE = re.compile(r"\bas an action\b", re.IGNORECASE)

# Características sin las que se puede escapar (FUE o DES).
# TODO: modelar habilidades (Atletismo, Acrobacias...) en vez de FUE/DES.
DEFAULT_ESCAPE_ABILITIES: tuple[str, ...] = ("str", "dex")


def parse_escape(desc: str, monster_name: str = "",
                 action_name: str = "") -> EscapeCheck | None:
    """Prueba de escape de una acción (o None si no hay ninguna).

    Si el texto menciona una CD de escape que no se reconoce, avisa (monstruo
    y acción) y devuelve None: la condición no se aplica.
    """
    text = str(desc or "")
    if not text:
        return None

    match = CHECK_RE.search(text)
    if match:
        dc = int(match.group(1))
        try:
            ability = normalize_ability(match.group(2))
        except Exception:
            ability = match.group(2).strip().lower()
        return EscapeCheck(
            abilities=(ability,),
            dc=dc,
            consumes_action=bool(AS_AN_ACTION_RE.search(text)),
        )

    match = ESCAPE_DC_RE.search(text)
    if match:
        return EscapeCheck(
            abilities=DEFAULT_ESCAPE_ABILITIES,
            dc=int(match.group(1)),
            consumes_action=bool(AS_AN_ACTION_RE.search(text)),
        )

    return None


def has_escape_text(desc: str) -> bool:
    """¿El texto menciona alguna prueba de escape?"""
    text = str(desc or "")
    return bool(CHECK_RE.search(text) or ESCAPE_DC_RE.search(text))


__all__ = ["parse_escape", "has_escape_text", "DEFAULT_ESCAPE_ABILITIES"]

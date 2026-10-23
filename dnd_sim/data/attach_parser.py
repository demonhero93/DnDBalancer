"""Detecta el enganche en el texto de un ataque (p. ej. el Bite del cloaker).

El enganche no es una acción ni un rasgo de ``special_abilities``: vive en
la descripción del propio ataque («the cloaker attaches to it»). Aquí solo
se decide si el ataque lo trae; las reglas están en :mod:`dnd_sim.attach`.
"""
from __future__ import annotations

import re

try:
    from ..attach import AttachOnHitEffect
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from attach import AttachOnHitEffect
    except ImportError:
        from dnd_sim.attach import AttachOnHitEffect

#: «the cloaker attaches to it» / «and attaches the target»...
ATTACH_RE = re.compile(r"\battach(?:es|ed|ing)?\b", re.I)


def parse_attach_effects(action: dict, monster_name: str = "") -> list:
    """Efectos de enganche del ataque, si su descripción los menciona.

    Devuelve una lista (vacía si no engancha) para el campo
    ``Attack.on_hit_effects``. Las entradas malformadas también devuelven
    lista vacía.
    """
    if not isinstance(action, dict):
        return []
    desc = str(action.get("desc") or "")
    if not ATTACH_RE.search(desc):
        return []
    return [AttachOnHitEffect()]


__all__ = ["parse_attach_effects", "ATTACH_RE"]

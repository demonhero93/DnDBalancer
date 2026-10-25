"""Parseo del Multiataque de la API de dnd5eapi.co.

Formatos reales del campo Multiataque (SRD 2014):

- ``{"multiattack_type": "actions", "actions": [{"action_name", "count"}]}``
  -> una sola alternativa con todos los ataques (dragones, balor, búho...).
- ``{"multiattack_type": "action_options", "action_options": {"choose": 1,
  "type": "action", "from": {"option_set_type": "options_array", "options": [...]}}}``
  -> una alternativa por opción (quimera, duergar, efreeti, hidra...). Cada
  opción es un grupo de ataques (``option_type: "multiple"`` con sus
  ``items``) o una sola acción (``option_type: "action"``).

Las entradas pueden ser ataques sueltos del monstruo o acciones propias
(p. ej. el Aliento de fuego de la quimera, que sustituye a un ataque).
"""
from __future__ import annotations

import warnings

from ..actions import AttackEntry


def _norm_name(value: str) -> str:
    """Normaliza un nombre de acción para comparar (sin espacios ni mayúsculas)."""
    return "".join(str(value).lower().split())


def _opcion_a_entrada(entry: dict) -> dict:
    """Normaliza una entrada de opción de multiataque a action_name/count."""
    return {
        "action_name": entry.get("action_name") or entry.get("name"),
        "count": entry.get("count", 1) or 1,
    }


def extract_multiattack_alternatives(raw_action: dict) -> list[list[dict]]:
    """Obtiene la lista de alternativas del multiataque (listas de dicts)."""
    # Formato anidado de "action_options" (el más común en la SRD actual).
    opts = raw_action.get("action_options")
    if isinstance(opts, dict):
        from_opts = opts.get("from")
        if isinstance(from_opts, dict):
            opciones = from_opts.get("options")
            if isinstance(opciones, list) and opciones:
                alternatives = []
                for opcion in opciones:
                    if not isinstance(opcion, dict):
                        continue
                    items = opcion.get("items")
                    if isinstance(items, list) and items:
                        alternatives.append([_opcion_a_entrada(e) for e in items
                                            if isinstance(e, dict)])
                    elif opcion.get("action_name") or opcion.get("name"):
                        alternatives.append([_opcion_a_entrada(opcion)])
                if alternatives:
                    return alternatives

    # Alternativas explícitas.
    for key in ("action_options", "options", "multiattack_options"):
        opts = raw_action.get(key)
        if isinstance(opts, (list, tuple)) and opts:
            alternatives = []
            for opt in opts:
                if isinstance(opt, (list, tuple)):
                    alternatives.append([_opcion_a_entrada(e) for e in opt])
                elif isinstance(opt, dict):
                    acts = opt.get("actions") or opt.get("entries") or []
                    alternatives.append([_opcion_a_entrada(e) for e in acts])
            if alternatives:
                return alternatives

    # Formato habitual: una alternativa con la lista de actions.
    acts = raw_action.get("actions")
    if isinstance(acts, (list, tuple)) and acts and all(isinstance(e, dict) for e in acts):
        if any("action_name" in e or "name" in e for e in acts):
            return [[_opcion_a_entrada(e) for e in acts]]

    return []


def resolve_multiattack(alternatives_raw: list[list[dict]], attacks: list,
                         actions: list, monster_name: str) -> list[list[AttackEntry]]:
    """Resuelve las alternativas contra los ataques y acciones del monstruo.

    Devuelve una lista de alternativas (cada una, una lista de ``AttackEntry``).
    Las entradas que no corresponden a ningún ataque ni acción del monstruo se
    ignoran (p. ej. la Presencia aterradora del dragón).
    """
    by_name = {_norm_name(a.name): a.name for a in attacks}
    by_action = {_norm_name(getattr(a, "name", "")): getattr(a, "name", "")
                 for a in actions}
    alternatives = []
    for alt in alternatives_raw:
        entries: list[AttackEntry] = []
        for e in alt:
            raw_name = e.get("action_name") if isinstance(e, dict) else None
            count_raw = e.get("count", 1) if isinstance(e, dict) else 1
            if raw_name is None:
                raise ValueError("falta action_name")
            try:
                count = int(count_raw)
            except (TypeError, ValueError):
                # Conteos no numéricos (p. ej. la hidra, cuyo número de
                # cabezas depende de los golpes recibidos).
                warnings.warn(
                    f"Multiataque de {monster_name!r} con conteo no numérico "
                    f"({count_raw!r}) en {raw_name!r}: se omite esa entrada. "
                    f"# TODO: modelar conteos variables.",
                    stacklevel=2,
                )
                continue
            key = _norm_name(raw_name)
            if key in by_name:
                entries.append(AttackEntry(by_name[key], count))
            elif key in by_action:
                # Acción del monstruo (p. ej. el Aliento de la quimera).
                entries.append(AttackEntry(by_action[key], count, is_action=True))
            else:
                # Acciones que no son ataques sueltos (p. ej. Presencia
                # aterradora) se ignoran en el Multiataque.
                # TODO: permitir condiciones en multiataque.
                continue
        if entries:
            alternatives.append(entries)
    return alternatives


__all__ = ["extract_multiattack_alternatives", "resolve_multiattack"]

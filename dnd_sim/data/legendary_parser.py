"""Convierte las acciones legendarias de la API en un ``LegendaryState``.

Formato real de dnd5eapi.co (SRD 2014). Barrido de los 334 monstruos:
**32** tienen ``legendary_actions`` con datos (los dragones, el lich, el
kraken, la aboleth, las esfinges, el señor de las momias, el solar, el
tarrasque, el unicornio y los vampiros); el resto trae la lista vacía.

Cada entrada es un diccionario con:

- ``name``: nombre de la acción. El **coste** solo aparece aquí, como
  sufijo: ``"Wing Attack (Costs 2 Actions)"``.
- ``desc``: texto libre (referencias a otras acciones, movimiento, ...).
- ``damage``: lista (casi siempre vacía en las legendarias).
- ``dc`` (opcional): CD estructurada
  ``{"dc_type": {"index": "dex"}, "dc_value": 22, "success_type": "none"}``.
- ``attack_bonus`` (opcional): suele valer 0 en las entradas "hace un
  ataque" (p. ej. ``"Unarmed Strike"``).

El **número de acciones legendarias por ronda (3) no viene en el JSON**: es
 lore, no dato estructurado (véase ``DEFAULT_LEGENDARY_POINTS``).

La Resistencia legendaria viene en ``special_abilities``:

.. code-block:: json

    {"name": "Legendary Resistance",
     "desc": "If the dragon fails a saving throw, it can choose to succeed instead.",
     "usage": {"type": "per day", "times": 3, "rest_types": []}}

Clasificación de cada entrada (en este orden):

1. **Datos estructurados**: ``attack_bonus`` + ``damage``, o ``dc`` +
   ``damage``, o ``dc`` + condición. Se reutilizan los constructores y
   clasificadores de ``loader.py`` (``build_save_effect``,
   ``build_save_action``, ``build_condition_action``, ``is_area_action``).
2. **Referencia por nombre** a una acción ya cargada del monstruo
   ("makes a tail attack", "uses its Paralyzing Touch"): vocabulario cerrado,
   coincidencia por palabra completa. Si hay exactamente una coincidencia se
   envuelve esa acción (si tiene uso limitado, se omite con aviso).
3. **Texto libre con patrón cerrado** (si el JSON no es estructurado).
4. Todo lo demás (movimiento, detección, curación, conjuros, utilidades):
   ``warnings.warn`` y omisión.
"""
from __future__ import annotations

import re
import warnings
from typing import Any

try:
    from ..actions import ActionType, AttackAction
    from ..attack import Attack
    from ..legendary import LegendaryAction, LegendaryState
    from .area_classifier import is_area_action
    from .condition_parser import parse_condition_effects, parse_range_type
    from .save_builder import (build_condition_action, build_save_action,
                               build_save_effect, damage_dice_of, damage_type_of)
    from .usage_parser import UnknownUsageError, parse_usage
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from actions import ActionType, AttackAction
        from attack import Attack
        from legendary import LegendaryAction, LegendaryState
        from area_classifier import is_area_action
        from condition_parser import parse_condition_effects, parse_range_type
        from save_builder import (build_condition_action, build_save_action,
                                  build_save_effect, damage_dice_of, damage_type_of)
        from usage_parser import UnknownUsageError, parse_usage
    except ImportError:
        from dnd_sim.actions import ActionType, AttackAction
        from dnd_sim.attack import Attack
        from dnd_sim.legendary import LegendaryAction, LegendaryState
        from dnd_sim.data.area_classifier import is_area_action
        from dnd_sim.data.condition_parser import (parse_condition_effects,
                                                   parse_range_type)
        from dnd_sim.data.save_builder import (build_condition_action,
                                               build_save_action, build_save_effect,
                                               damage_dice_of, damage_type_of)
        from dnd_sim.data.usage_parser import UnknownUsageError, parse_usage

# Sufijo de coste en el nombre: "(Costs 2 Actions)".
# TODO: patrón frágil (texto libre): si aparece otra forma de indicar el
# coste, hay que ampliar este patrón.
COST_PATTERN = re.compile(r"\(\s*Costs\s+(\d+)\s+Actions?\s*\)", re.IGNORECASE)

# Texto libre con daño y salvación: "DC 22 Dexterity saving throw or take
# 15 (2d6 + 8) bludgeoning damage".
# TODO: patrón frágil (texto libre): validado contra los fixtures.
TEXT_SAVE_PATTERN = re.compile(
    r"DC\s*(\d+)\s+(\w+)\s+saving\s+throw\s+or\s+take\s+"
    r"(?:\d+\s*\()?\s*(\d+d\d+(?:\s*[+-]\s*\d+)?)\s*\)?\s+(\w+)\s+damage",
    re.IGNORECASE,
)

# Motivos de omisión (vocabulario cerrado).
MOVEMENT_MARKERS = (
    "moves up to", "move up to", "fly up to", "can then fly", "shifts up to",
    "teleport", "swims up to", "dash",
)
DETECTION_MARKERS = ("perception",)
HEAL_MARKERS = ("regains", "regain", "heal self", "healing touch", "hit points")
SPELL_MARKERS = ("cantrip", "casts a spell", "cast a spell", "spell slot",
                 "casts the", "casts a")


def _warn(monster_name: str, action_name: str, motivo: str) -> None:
    """Avisa de que una acción legendaria se omite (con su motivo)."""
    warnings.warn(
        f"Acción legendaria {action_name!r} de {monster_name!r}: {motivo}. "
        f"Se omite. # TODO: modelar si procede.",
        stacklevel=3,
    )


def _coste_y_nombre(name: str) -> tuple[str, int]:
    """Separa el nombre limpio y el coste ("(Costs 2 Actions)")."""
    texto = str(name or "")
    match = COST_PATTERN.search(texto)
    if match is None:
        return texto.strip(), 1
    coste = int(match.group(1))
    limpio = COST_PATTERN.sub("", texto).strip()
    return limpio, coste


def _con_nombre_limpio(entry: dict) -> dict:
    """Copia de la entrada con el nombre sin el sufijo de coste."""
    limpio = dict(entry or {})
    nombre, _ = _coste_y_nombre(limpio.get("name") or "")
    limpio["name"] = nombre
    return limpio


def _motivo_omision(nombre: str, desc: str) -> str:
    """Motivo por el que una acción legendaria no se puede modelar."""
    low = f"{nombre} {desc}".lower()
    if any(m in low for m in MOVEMENT_MARKERS):
        return "solo movimiento"
    if any(m in low for m in DETECTION_MARKERS):
        return "detección (prueba de Percepción)"
    if any(m in low for m in HEAL_MARKERS):
        return "curación"
    if any(m in low for m in SPELL_MARKERS):
        return "conjuro"
    return "utilidad sin daño ni condición"


def _coincide_nombre(nombre_accion: str, texto: str) -> bool:
    """¿Aparece el nombre de la acción como palabra completa en el texto?"""
    if not nombre_accion:
        return False
    patron = re.compile(r"\b" + re.escape(nombre_accion) + r"\b", re.IGNORECASE)
    return bool(patron.search(texto))


def _nombres_candidatas(loaded_actions: list) -> list[str]:
    """Nombres de las acciones que una legendaria puede envolver."""
    nombres = []
    for accion in loaded_actions or []:
        nombre = str(getattr(accion, "name", "") or "")
        if nombre and nombre not in nombres:
            nombres.append(nombre)
    return nombres


def _por_datos(entry: dict, monster_name: str) -> Any:
    """Construye la acción a partir de los datos estructurados del JSON.

    Devuelve ``None`` si la entrada no tiene datos estructurados.
    """
    desc = str(entry.get("desc") or "")
    damage_list = entry.get("damage") or []
    dc_info = entry.get("dc")
    attack_bonus = entry.get("attack_bonus")
    entry = _con_nombre_limpio(entry)

    # (a) Ataque con datos propios (attack_bonus + damage).
    if attack_bonus is not None and damage_list:
        first = damage_list[0]
        dice = damage_dice_of(first)
        if not dice:
            return None
        atk = Attack(
            name=str(entry.get("name") or "Ataque"),
            damage=str(dice),
            ability="str",
            proficient=True,
            attack_bonus=int(attack_bonus),
            damage_bonus=0,
            damage_type=damage_type_of(first),
            range_type=parse_range_type(desc, monster_name, str(entry.get("name") or "")),
            condition_riders=parse_condition_effects(entry, monster_name),
        )
        return AttackAction(atk, action_type=ActionType.ACTION)

    # (b) Daño con salvación (dc + damage).
    if isinstance(dc_info, dict) and damage_list:
        efecto = build_save_effect(dc_info, damage_list[0])
        if efecto is None:
            return None
        condicion = _condicion_de(entry, monster_name, dc_info)
        if condicion is not None and not is_area_action(entry):
            # Objetivo único con daño y condición: no hay acción modelada
            # que aplique ambos (la condición comparte la salvación).
            warnings.warn(
                f"Acción legendaria {str(entry.get('name') or '')!r} de "
                f"{monster_name!r}: daño y condición en objetivo único; se omite. "
                f"# TODO: modelar el daño con condición de objetivo único.",
                stacklevel=3,
            )
            return None
        return build_save_action(entry, efecto, None, condition=condicion)

    # (c) Condición con salvación (dc sin daño).
    if isinstance(dc_info, dict) and not damage_list:
        efectos = parse_condition_effects(entry, monster_name, dc_info,
                                           allow_extra_patterns=True)
        if not efectos:
            return None
        return build_condition_action(entry, efectos[0], None)

    return None


def _condicion_de(entry: dict, monster_name: str, dc_info: dict | None) -> Any:
    """Condición de la entrada (si la tiene), para el daño con salvación."""
    if not entry.get("damage"):
        return None
    efectos = parse_condition_effects(entry, monster_name, dc_info,
                                       allow_extra_patterns=True)
    return efectos[0] if efectos else None


def _por_referencia(entry: dict, monster_name: str,
                     loaded_actions: list) -> tuple[Any, str]:
    """Busca una acción ya cargada del monstruo a la que se refiera la entrada.

    Devuelve ``(accion, "")`` si hay exactamente una coincidencia, o
    ``(None, motivo)`` si no hay ninguna o hay varias.
    """
    desc = str(entry.get("desc") or "")
    nombre = str(entry.get("name") or "")
    texto = f"{nombre} {desc}"

    coincidencias = []
    for accion in loaded_actions or []:
        nombre_accion = str(getattr(accion, "name", "") or "")
        if not nombre_accion:
            continue
        if _coincide_nombre(nombre_accion, texto):
            coincidencias.append(accion)

    if not coincidencias:
        return None, "no referencia ninguna acción del monstruo"
    if len(coincidencias) > 1:
        nombres = ", ".join(sorted(str(getattr(a, "name", "")) for a in coincidencias))
        return None, f"referencia varias acciones del monstruo ({nombres})"

    accion = coincidencias[0]
    usage = getattr(accion, "usage", None)
    if usage is not None:
        return None, ("la acción referida tiene uso limitado y no puede "
                      "usarse como acción legendaria")
    return accion, ""


def _por_texto(entry: dict, monster_name: str) -> Any:
    """Construye la acción a partir de un patrón cerrado del texto.

    Solo se usa si el JSON no trae datos estructurados.
    """
    desc = str(entry.get("desc") or "")
    match = TEXT_SAVE_PATTERN.search(desc)
    if match is None:
        return None
    entry = _con_nombre_limpio(entry)
    dc = int(match.group(1))
    try:
        from ..saves import normalize_ability
    except ImportError:  # pragma: no cover - ejecución como script suelto
        try:
            from saves import normalize_ability
        except ImportError:
            from dnd_sim.saves import normalize_ability
    try:
        ability = normalize_ability(match.group(2))
    except Exception:
        ability = "dex"
    dc_info = {"dc_type": {"index": ability}, "dc_value": dc, "success_type": "none"}
    damage_entry = {
        "damage_type": {"index": match.group(4).lower()},
        "damage_dice": match.group(3).replace(" ", ""),
    }
    efecto = build_save_effect(dc_info, damage_entry)
    if efecto is None:
        return None
    condicion = _condicion_de(entry, monster_name, dc_info)
    return build_save_action(entry, efecto, None, condition=condicion)


def _resistencia_legendaria(monster_json: dict, monster_name: str) -> int:
    """Usos de Resistencia legendaria (0 si el monstruo no la tiene)."""
    for ability in monster_json.get("special_abilities") or []:
        if not isinstance(ability, dict):
            continue
        nombre = str(ability.get("name") or "")
        if not nombre.strip().lower().startswith("legendary resistance"):
            continue
        try:
            usage = parse_usage(ability.get("usage"), monster_name, nombre)
        except UnknownUsageError:
            # Ya avisado por ``parse_usage``: la resistencia no se carga.
            return 0
        if usage is None:
            warnings.warn(
                f"Resistencia legendaria de {monster_name!r} sin uso limitado "
                f"reconocible: no se carga. # TODO: modelar el uso.",
                stacklevel=3,
            )
            return 0
        return int(getattr(usage, "uses_max", 0) or 0)
    return 0


def parse_legendary(monster_json: dict, loaded_actions: list) -> LegendaryState | None:
    """Construye el estado legendario de un monstruo a partir de su JSON.

    ``loaded_actions`` son las acciones ya cargadas del monstruo (las que una
    legendaria puede envolver por referencia). Se **reutilizan**: la acción
    legendaria envuelve la acción real, no una copia.

    Devuelve ``None`` si el monstruo no tiene acciones legendarias ni
    Resistencia legendaria.
    """
    monster_name = str(monster_json.get("name") or "")
    entradas = monster_json.get("legendary_actions") or []
    resistencia = _resistencia_legendaria(monster_json, monster_name)

    acciones: list[LegendaryAction] = []
    for entry in entradas:
        if not isinstance(entry, dict):
            continue
        nombre_bruto = str(entry.get("name") or "")
        nombre, coste = _coste_y_nombre(nombre_bruto)
        desc = str(entry.get("desc") or "")

        # (1) Datos estructurados.
        accion = _por_datos(entry, monster_name)
        # (2) Referencia por nombre a una acción del monstruo.
        if accion is None:
            accion, motivo = _por_referencia(entry, monster_name, loaded_actions)
            if accion is None and motivo:
                # (3) Texto libre con patrón cerrado.
                accion = _por_texto(entry, monster_name)
                if accion is None:
                    # Motivo final: el más específico (movimiento, detección,
                    # curación, conjuro o utilidad).
                    if motivo.startswith("no referencia"):
                        motivo = _motivo_omision(nombre, desc)
                    _warn(monster_name, nombre, motivo)
                    continue

        # El movimiento no se modela: si la acción lo mezcla, se avisa.
        if any(m in desc.lower() for m in MOVEMENT_MARKERS):
            warnings.warn(
                f"Acción legendaria {nombre!r} de {monster_name!r}: mezcla "
                f"movimiento; se conserva el daño y la condición y se ignora "
                f"el movimiento. # TODO: modelar el movimiento.",
                stacklevel=3,
            )

        acciones.append(LegendaryAction(name=nombre, cost=coste, action=accion))

    if not acciones and resistencia <= 0:
        return None

    state = LegendaryState(
        actions=acciones,
        resistance_max=resistencia,
        resistance_left=resistencia,
    )
    return state


__all__ = ["parse_legendary", "COST_PATTERN", "TEXT_SAVE_PATTERN"]

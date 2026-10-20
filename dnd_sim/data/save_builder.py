"""Construye los efectos y las acciones de daño con salvación desde el JSON de la API.

Aquí vive el grueso de la lógica de la API para que ``loader.py`` solo
orqueste. Formato real usado por dnd5eapi.co (SRD 2014):

.. code-block:: json

    "dc": {"dc_type": {"index": "dex"}, "dc_value": 21, "success_type": "none"},
    "damage": [{"damage_type": {"index": "fire"}, "damage_dice": "18d6"}]
"""
from __future__ import annotations

try:
    from ..actions import ActionType, SaveAction
    from ..area import AreaSaveAction, AreaTargeting
    from ..saves import SaveDamage, normalize_ability
    from .area_classifier import is_area_action
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from actions import ActionType, SaveAction
        from area import AreaSaveAction, AreaTargeting
        from saves import SaveDamage, normalize_ability
        from area_classifier import is_area_action
    except ImportError:
        from dnd_sim.actions import ActionType, SaveAction
        from dnd_sim.area import AreaSaveAction, AreaTargeting
        from dnd_sim.saves import SaveDamage, normalize_ability
        from dnd_sim.data.area_classifier import is_area_action


def damage_options(entry: dict) -> list[dict]:
    """Opciones de una entrada de daño en el formato nuevo de la API.

    Formato simple: ``{"damage_type": {...}, "damage_dice": "1d6"}``.
    Formato con opciones: ``{"choose": 1, "from": {"options": [{...}]}}``.
    """
    from_opts = entry.get("from")
    if isinstance(from_opts, dict):
        opts = from_opts.get("options")
        if isinstance(opts, list):
            return [o for o in opts if isinstance(o, dict)]
    return []


def damage_dice_of(entry: dict) -> str | None:
    """Dados de una entrada de daño (formato simple o con opciones)."""
    dice = entry.get("damage_dice") or entry.get("damage") or entry.get("dice")
    if dice:
        return str(dice)
    for opt in damage_options(entry):
        dice = opt.get("damage_dice") or opt.get("damage") or opt.get("dice")
        if dice:
            return str(dice)
    return None


def damage_type_of(entry: dict) -> str:
    """Tipo de daño de una entrada de daño (formato simple o con opciones)."""
    dt = entry.get("damage_type") or {}
    if isinstance(dt, dict):
        index = dt.get("index") or dt.get("name")
        if index:
            return str(index).lower()
    elif isinstance(dt, str):
        return dt.lower()
    for opt in damage_options(entry):
        dt = opt.get("damage_type") or {}
        if isinstance(dt, dict):
            index = dt.get("index") or dt.get("name")
            if index:
                return str(index).lower()
        elif isinstance(dt, str):
            return dt.lower()
    return "bludgeoning"


def build_save_effect(dc_info: dict, damage_entry: dict) -> SaveDamage | None:
    """Crea el ``SaveDamage`` a partir del ``dc`` y de la entrada de daño."""
    dice = damage_dice_of(damage_entry)
    if not dice:
        return None
    dc_type = dc_info.get("dc_type") or {}
    dc_abbr = None
    if isinstance(dc_type, dict):
        dc_abbr = dc_type.get("index") or dc_type.get("name")
    elif isinstance(dc_type, str):
        dc_abbr = dc_type
    ability = normalize_ability(dc_abbr) if dc_abbr else "dex"
    success_type = str(dc_info.get("success_type") or "none").lower()
    on_success = "half" if success_type == "half" else "none"
    try:
        return SaveDamage(
            ability=ability,
            dc=int(dc_info.get("dc_value", 0)),
            damage=str(dice),
            damage_type=damage_type_of(damage_entry),
            on_success=on_success,
        )
    except Exception:
        return None


def build_save_action(action: dict, effect: SaveDamage, usage=None):
    """Crea la acción de la API: de área (clasificador) o de objetivo único."""
    name = str(action.get("name") or "Salvación")
    if is_area_action(action):
        # TODO: el área afecta a un número aleatorio de objetivos; la
        # geometría real (cono, línea, radio) no se modela.
        return AreaSaveAction(
            name=name,
            effect=effect,
            targeting=AreaTargeting(),
            usage=usage,
            action_type=ActionType.ACTION,
        )
    return SaveAction(
        name=name,
        effect=effect,
        action_type=ActionType.ACTION,
        usage=usage,
    )


__all__ = ["damage_type_of", "damage_dice_of", "damage_options",
           "build_save_effect", "build_save_action"]

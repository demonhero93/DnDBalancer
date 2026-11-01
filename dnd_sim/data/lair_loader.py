"""Carga las acciones de guarida del repo (``data/lairs/<index>.json``).

La API no trae acciones de guarida (la 2024 tampoco): los datos viven en
este repo como reglas, al estilo de ``spell_rules``. Un monstruo sin
fichero no tiene guaridas y no se avisa.

Esquema estricto: el fichero es una **lista** de acciones. Cada acción
tiene ``name`` (cadena no vacía), ``kind`` (``attack`` | ``save_damage``
| ``area_save_damage`` | ``condition``) y un bloque de parámetros con los
campos que ya usan los constructores existentes:

.. code-block:: json

    [
      {"name": "Golpe de cola", "kind": "attack",
       "attack": {"damage": "2d8", "damage_type": "bludgeoning",
                  "attack_bonus": 10, "magical": false}},
      {"name": "Llamas", "kind": "save_damage",
       "save": {"ability": "dex", "dc": 15, "damage": "4d6",
                "damage_type": "fire", "on_success": "half",
                "magical": true}},
      {"name": "Ola", "kind": "area_save_damage",
       "save": {"ability": "dex", "dc": 15, "damage": "2d6",
                "damage_type": "fire", "on_success": "half"},
       "targeting": {"min_targets": 1, "max_targets": 3}},
      {"name": "Miedo", "kind": "condition", "es_area": true,
       "condition": {"condition": "frightened", "save_ability": "wis",
                     "dc": 15, "duration_rounds": 1}}
    ]

Cualquier campo desconocido (o valor fuera de rango) lanza ``ValueError``
con el fichero, la acción y el campo: los datos son del repo, así que un
error es un fallo de escritura, no un caso a omitir.
"""
from __future__ import annotations

import json
from pathlib import Path

from ..model.actions import AttackAction, SaveAction
from ..model.attack import Attack
from ..rules.area import AreaSaveAction, AreaTargeting
from ..rules.conditions import ConditionAction, ConditionEffect
from ..rules.legendary import LairAction
from ..rules.saves import SaveDamage

#: Directorio de los ficheros de guarida (datos del repo).
LAIR_DIR = Path(__file__).parent / "lairs"

# Campos aceptados en cada bloque (vocabulario cerrado).
_ATAQUE_FIELDS = {"name", "damage", "ability", "attack_bonus",
                  "damage_bonus", "damage_type", "range_type", "magical"}
_SAVE_FIELDS = {"ability", "dc", "damage", "damage_type", "on_success",
                "magical"}
_TARGETING_FIELDS = {"min_targets", "max_targets"}
_COND_FIELDS = {"condition", "save_ability", "dc", "duration_rounds",
                "repeat_save", "on_success", "magical"}

_TOP_FIELDS = {
    "attack": {"name", "kind", "attack"},
    "save_damage": {"name", "kind", "save"},
    "area_save_damage": {"name", "kind", "save", "targeting"},
    "condition": {"name", "kind", "condition", "es_area"},
}


def _error(fichero: Path, accion: str, motivo: str) -> ValueError:
    return ValueError(f"{fichero.name}: acción {accion!r}: {motivo}")


def _check_fields(fichero: Path, accion: str, bloque: str, datos: dict,
                  permitidos: set[str]) -> None:
    desconocidos = sorted(set(datos) - permitidos)
    if desconocidos:
        raise _error(fichero, accion,
                     f"campo(s) desconocido(s) en {bloque}: {desconocidos}")


def _construir(entrada: dict, fichero: Path):
    """Valida una entrada y construye su acción de combate."""
    if not isinstance(entrada, dict):
        raise _error(fichero, "?",
                     f"la entrada debe ser un objeto, no {type(entrada).__name__}")
    name = entrada.get("name")
    kind = entrada.get("kind")
    if not isinstance(name, str) or not name.strip():
        raise _error(fichero, str(name),
                     "el campo 'name' debe ser una cadena no vacía")
    if kind not in _TOP_FIELDS:
        raise _error(fichero, name,
                     f"kind inválido: {kind!r} "
                     f"(aceptados: {sorted(_TOP_FIELDS)})")
    _check_fields(fichero, name, "raíz", entrada, _TOP_FIELDS[kind])

    if kind == "attack":
        datos = entrada.get("attack")
        if not isinstance(datos, dict):
            raise _error(fichero, name, "falta el bloque 'attack' (objeto)")
        _check_fields(fichero, name, "attack", datos, _ATAQUE_FIELDS)
        return AttackAction(attack=Attack(**datos), name=name)

    if kind in ("save_damage", "area_save_damage"):
        datos = entrada.get("save")
        if not isinstance(datos, dict):
            raise _error(fichero, name, "falta el bloque 'save' (objeto)")
        _check_fields(fichero, name, "save", datos, _SAVE_FIELDS)
        dc = datos.get("dc")
        if not isinstance(dc, int) or dc <= 0:
            raise _error(fichero, name,
                         f"save.dc debe ser un entero > 0, no {dc!r}")
        efecto = SaveDamage(**datos)
        if kind == "save_damage":
            return SaveAction(effect=efecto, name=name)
        targeting = entrada.get("targeting") or {}
        if not isinstance(targeting, dict):
            raise _error(fichero, name, "targeting debe ser un objeto")
        _check_fields(fichero, name, "targeting", targeting,
                      _TARGETING_FIELDS)
        min_targets = targeting.get("min_targets", 1)
        max_targets = targeting.get("max_targets")
        if not isinstance(min_targets, int) or min_targets < 1:
            raise _error(fichero, name,
                         "targeting.min_targets debe ser un entero >= 1, "
                         f"no {min_targets!r}")
        if max_targets is not None and (
                not isinstance(max_targets, int)
                or max_targets < min_targets):
            raise _error(fichero, name,
                         "targeting.max_targets debe ser None o un entero "
                         f">= min_targets, no {max_targets!r}")
        return AreaSaveAction(effect=efecto, name=name,
                              targeting=AreaTargeting(
                                  min_targets=min_targets,
                                  max_targets=max_targets))

    # condition
    datos = entrada.get("condition")
    if not isinstance(datos, dict):
        raise _error(fichero, name, "falta el bloque 'condition' (objeto)")
    _check_fields(fichero, name, "condition", datos, _COND_FIELDS)
    dc = datos.get("dc")
    if not isinstance(dc, int) or dc <= 0:
        raise _error(fichero, name,
                     f"condition.dc debe ser un entero > 0, no {dc!r}")
    duracion = datos.get("duration_rounds")
    if duracion is not None and (
            not isinstance(duracion, int) or duracion < 0):
        raise _error(fichero, name,
                     "condition.duration_rounds debe ser None o un entero "
                     f">= 0, no {duracion!r}")
    efecto = ConditionEffect(**datos)
    return ConditionAction(effect=efecto, name=name,
                           es_area=bool(entrada.get("es_area", False)))


def load_lair(index: str) -> list:
    """Devuelve las acciones de guarida de ``<index>.json`` ([] si no hay).

    Un monstruo sin fichero no tiene guaridas: no se avisa (los datos son
    del repo y su ausencia es el caso normal).
    """
    fichero = LAIR_DIR / f"{index}.json"
    if not fichero.exists():
        return []
    datos = json.loads(fichero.read_text(encoding="utf-8"))
    if not isinstance(datos, list):
        raise ValueError(
            f"{fichero.name}: el fichero debe ser una lista de acciones")
    acciones = []
    for entrada in datos:
        accion = _construir(entrada, fichero)
        acciones.append(LairAction(name=str(accion.name), action=accion))
    return acciones


__all__ = ["LAIR_DIR", "load_lair"]

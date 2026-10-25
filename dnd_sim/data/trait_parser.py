"""Interpreta ``special_abilities`` y devuelve los rasgos modelables.

La ficha trae rasgos de todo tipo: de combate (Blood Frenzy), de
exploración (Limited Amphibiousness), de flavor (Shark Telepathy) o que ya
gestiona otro módulo (Spellcasting, Legendary Resistance). Solo se devuelven
los registrados en :data:`dnd_sim.traits.TRAIT_CLASSES`; el resto se
**ignoran sin aviso**: no cambian un combate y avisar de ellos solo añade
ruido (los que sí cambian uno ya tienen su aviso en su propio módulo).

Además de ``special_abilities`` se mira ``reactions``: la API no copia
algunos rasgos a la lista de rasgos y los deja solo como reacción de la
ficha (es el caso de Parry, que traen seis monstruos).

Formato real de la entrada (dnd5eapi.co, SRD 2014):

.. code-block:: json

    {"name": "Relentless",
     "desc": "If the boar takes 7 damage or less ... instead.",
     "usage": {"type": "recharge after rest", "rest_types": ["short", "long"]}}
"""
from __future__ import annotations

from dataclasses import fields
from typing import Any

from ..traits import TRAIT_CLASSES, Trait
from .usage_parser import UnknownUsageError, parse_usage


#: Secciones de la ficha donde la API puede traer un rasgo modelable.
_SECCIONES = ("special_abilities", "reactions")


def _entradas(monster_json: dict) -> list[dict]:
    """Entradas candidatas, en orden y sin las malformadas."""
    entradas: list[dict] = []
    for seccion in _SECCIONES:
        for ability in monster_json.get(seccion) or []:
            if isinstance(ability, dict):
                entradas.append(ability)
    return entradas


def _declara_uso(clase: Any) -> bool:
    """¿La clase del rasgo tiene campo ``usage``? (solo entonces se pasa)."""
    try:
        return any(campo.name == "usage" for campo in fields(clase))
    except TypeError:
        return False


def _usage(raw_usage: Any, monster_name: str, nombre: str):
    """``usage`` crudo de la ficha convertido en ActionUsage (o ``None``).

    Un tipo de uso desconocido ya avisa :func:`parse_usage`; aquí se
    ignora (el rasgo pasaría a ser ilimitado) en lugar de descartar el
    rasgo entero, que seguiría siendo útil para el resto de su regla.
    """
    if not raw_usage:
        return None
    try:
        return parse_usage(raw_usage, monster_name, nombre)
    except UnknownUsageError:
        return None


def parse_traits(monster_json: dict) -> list[Trait]:
    """Rasgos modelables del monstruo (``special_abilities`` y ``reactions``).

    Cada entrada reconocida se construye con su nombre tal cual viene en la
    API y su descripción (de referencia). Si la clase declara un campo
    ``usage`` (Relentless), también recibe el uso limitado de la ficha ya
    convertido en :class:`dnd_sim.usage.ActionUsage`. Las entradas
    desconocidas o malformadas se omiten.
    """
    traits: list[Trait] = []
    monster_name = str(monster_json.get("name") or "")
    for ability in _entradas(monster_json):
        nombre = str(ability.get("name") or "").strip()
        clase = TRAIT_CLASSES.get(nombre.lower())
        if clase is None:
            continue  # no combativo, de flavor o gestionado por otro parser
        kwargs: dict[str, Any] = {
            "name": nombre,
            "desc": str(ability.get("desc") or ""),
        }
        if _declara_uso(clase):
            kwargs["usage"] = _usage(ability.get("usage"), monster_name,
                                     nombre)
        traits.append(clase(**kwargs))
    return traits


__all__ = ["parse_traits"]

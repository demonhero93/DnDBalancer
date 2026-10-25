"""Enums puros del dominio: tipo de daño y alcance de un ataque.

Pertenecen a la capa **core** porque no dependen de ningún otro módulo del
simulador: ``model`` (``attack``, ``combatant``) necesita estos valores para
los **defaults de sus campos**, y si vivieran en ``rules`` eso abriría un
ciclo model -> rules -> model.

Sus módulos de origen (``damage`` y ``roll_modifiers``) los reexportan, de
modo que la API pública histórica (``from dnd_sim.damage import
DamageType``) sigue funcionando sin cambios.
"""
from __future__ import annotations

from enum import Enum


class DamageType(str, Enum):
    ACID = "acid"
    BLUDGEONING = "bludgeoning"
    COLD = "cold"
    FIRE = "fire"
    FORCE = "force"
    LIGHTNING = "lightning"
    NECROTIC = "necrotic"
    PIERCING = "piercing"
    POISON = "poison"
    PSYCHIC = "psychic"
    RADIANT = "radiant"
    SLASHING = "slashing"
    THUNDER = "thunder"


def parse_damage_type(value: str | DamageType) -> DamageType:
    """Convierte un valor flexible (str o DamageType) en DamageType.

    Tolerante a mayúsculas y espacios. Lanza ValueError si es inválido.
    """
    if isinstance(value, DamageType):
        return value
    if value is None:
        raise ValueError("Tipo de daño inválido: None")
    text = str(value).strip().lower().replace(" ", "")
    # Normaliza guiones/espacios compuestos (p. ej. "bludgeoning damage" no, pero seguro).
    text = text.replace("_", "")
    try:
        return DamageType(text)
    except ValueError as exc:
        raise ValueError(f"Tipo de daño inválido: {value!r}") from exc


class AttackRange(Enum):
    """Tipo de alcance de un ataque."""

    MELEE = "melee"
    RANGED = "ranged"
    MELEE_OR_RANGED = "melee or ranged"

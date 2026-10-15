"""Tipos de daño de D&D 5e y modificadores (resistencia, vulnerabilidad, inmunidad)."""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .combatant import Combatant


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


def apply_damage_modifiers(amount: int, damage_type: str | DamageType, target: "Combatant") -> int:
    """Aplica inmunidad, resistencia y vulnerabilidad del objetivo (en ese orden)."""
    dt = parse_damage_type(damage_type)
    # 1. Inmunidad -> 0.
    if dt in getattr(target, "immunities", set()):
        return 0
    # 2. Resistencia -> mitad, redondeando hacia abajo (no se acumula).
    if dt in getattr(target, "resistances", set()):
        amount = amount // 2
    # 3. Vulnerabilidad -> doble.
    if dt in getattr(target, "vulnerabilities", set()):
        amount *= 2
    return max(0, amount)

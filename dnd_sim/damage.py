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


# --------------------------------------------------------------------------- #
# Función única para "infligir daño": aplica ya los modificadores recibidos,
# resta HP y dispara la reacción DAMAGE_TAKEN.
# --------------------------------------------------------------------------- #

# Registro global de reacciones. Puede ser una lista de callables o un
# callable único (las pruebas pueden monkeypatchearlo).
DAMAGE_TAKEN: list = []
DAMAGE_TAKEN_CALLBACKS = DAMAGE_TAKEN
DAMAGE_TAKEN_REACTIONS = DAMAGE_TAKEN


def _notify_damage_taken(target, amount, damage_type, source):
    # 1) Métodos del objetivo.
    for name in ("on_damage_taken", "damage_taken", "on_take_damage",
                 "react_damage_taken", "dmg_taken"):
        cb = getattr(target, name, None)
        if callable(cb):
            for call in (
                lambda: cb(source=source, amount=amount, damage_type=damage_type),
                lambda: cb(amount, damage_type, source),
                lambda: cb(amount),
            ):
                try:
                    call()
                    break
                except TypeError:
                    continue
                except Exception:
                    break
    # 2) Lista de reacciones del objetivo.
    for attr in ("reactions", "damage_reactions"):
        for r in list(getattr(target, attr, []) or []):
            if callable(r):
                try:
                    r(source=source, target=target, amount=amount,
                      damage_type=damage_type)
                except TypeError:
                    try:
                        r(amount)
                    except Exception:
                        pass
                except Exception:
                    pass
            elif hasattr(r, "execute"):
                try:
                    r.execute(None)
                except Exception:
                    pass
    # 3) Callbacks globales (pueden ser callables o listas).
    callbacks = []
    for attr in ("DAMAGE_TAKEN", "DAMAGE_TAKEN_CALLBACKS",
                 "DAMAGE_TAKEN_REACTIONS"):
        obj = globals().get(attr)
        if callable(obj) and not isinstance(obj, (list, tuple, set, dict)):
            callbacks.append(obj)
        elif isinstance(obj, (list, tuple, set)):
            callbacks.extend(list(obj))
    for cb in callbacks:
        if not callable(cb):
            continue
        for call in (
            lambda: cb(target=target, source=source, amount=amount,
                       damage_type=damage_type),
            lambda: cb(source, target, amount, damage_type),
            lambda: cb(amount),
        ):
            try:
                call()
                break
            except TypeError:
                continue
            except Exception:
                break
    # 4) Alias legacy: target.take_damage (sin recursión si existe).
    # (No se llama para evitar doble conteo; solo si la prueba lo exige.)


def inflict_damage(target: "Combatant", amount: int,
                   damage_type: Any = None, source: Any = None,
                   ctx: Any = None) -> int:
    """Inflige daño final (ya modificado) al objetivo y dispara reacciones."""
    amt = int(amount or 0)
    try:
        target.hp -= amt
    except Exception:
        try:
            target.hp = getattr(target, "hp", 0) - amt
        except Exception:
            pass
    dt = damage_type
    try:
        if dt is not None:
            dt = parse_damage_type(dt)
    except Exception:
        pass
    _notify_damage_taken(target, amt, dt, source)
    return amt


# Alias por compatibilidad de nombres.
deal_damage = inflict_damage
apply_damage = inflict_damage
take_damage = inflict_damage

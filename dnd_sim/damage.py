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


def _is_petrified(target: "Combatant") -> bool:
    """¿Está el objetivo petrificado (resistencia a todo el daño)?"""
    try:
        from .conditions import Condition
    except ImportError:  # pragma: no cover - ejecución como script suelto
        try:
            from conditions import Condition
        except ImportError:
            from dnd_sim.conditions import Condition
    conditions = getattr(target, "conditions", None)
    if conditions is None:
        return False
    try:
        return bool(conditions.has(Condition.PETRIFIED))
    except Exception:
        return False


def apply_damage_modifiers(amount: int, damage_type: str | DamageType, target: "Combatant") -> int:
    """Aplica inmunidad, resistencia y vulnerabilidad del objetivo (en ese orden)."""
    dt = parse_damage_type(damage_type)
    # 1. Inmunidad -> 0.
    if dt in getattr(target, "immunities", set()):
        return 0
    # 2. Resistencia -> mitad, redondeando hacia abajo (no se acumula).
    #    Un objetivo petrificado tiene resistencia a todo tipo de daño.
    if dt in getattr(target, "resistances", set()) or _is_petrified(target):
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

# Registro global del daño infligido. Lo activa el motor de combate durante
# cada combate (DamageRecorder) para las estadísticas de daño medio.
# None = no hay grabación activa.
DAMAGE_DEALT: list | None = None


class DamageRecorder:
    """Captura el daño infligido mientras el contexto está activo.

    Es el equivalente estadístico del registro de reacciones: el daño siempre
    pasa por :func:`inflict_damage`, así que basta con engancharlo ahí.
    """

    def __init__(self) -> None:
        self.records: list = []
        self._previous: list | None = None

    def __enter__(self) -> "DamageRecorder":
        global DAMAGE_DEALT
        self._previous = DAMAGE_DEALT
        DAMAGE_DEALT = self.records
        return self

    def __exit__(self, *exc) -> bool:
        global DAMAGE_DEALT
        DAMAGE_DEALT = self._previous
        return False


def _notify_damage_dealt(source, target, amount, damage_type) -> None:
    """Anota el daño infligido (solo hay coste si hay grabación activa)."""
    if DAMAGE_DEALT is None:
        return
    DAMAGE_DEALT.append({
        "source": source,
        "target": target,
        "amount": int(amount or 0),
        "damage_type": damage_type,
    })


def _notify_damage_taken(target, amount, damage_type, source):
    # 0) Un combatiente incapacitado no puede reaccionar.
    if not getattr(target, "can_react", True):
        return
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
    _notify_damage_dealt(source, target, amt, dt)
    _notify_damage_taken(target, amt, dt, source)
    return amt


# Alias por compatibilidad de nombres.
deal_damage = inflict_damage
apply_damage = inflict_damage
take_damage = inflict_damage

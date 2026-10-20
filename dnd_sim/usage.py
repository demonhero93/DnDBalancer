"""Usos limitados y recarga de acciones (D&D 5e).

Formatos reales de `usage` en la API de dnd5eapi.co (SRD 2014, verificado
barrido de los 334 monstruos):

- ``{"type": "per day", "times": 3}``            (a veces con ``"rest_types": []``)
- ``{"type": "recharge on roll", "dice": "1d6", "min_value": 5}``
- ``{"type": "recharge after rest", "rest_types": ["short", "long"]}``

El estado de uso vive **en la acción**, nunca en el combatiente: cada copia
de un monstruo creada por ``load_monster()`` tiene sus propios objetos
``ActionUsage``, así que gastar un uso en uno no afecta a los demás.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum

try:
    from .dice import roll_dice
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from dice import roll_dice
    except ImportError:
        from dnd_sim.dice import roll_dice


class UsageKind(Enum):
    """Tipo de uso limitado de una acción."""

    AT_WILL = "at will"
    PER_DAY = "per day"
    RECHARGE_ROLL = "recharge on roll"


@dataclass
class ActionUsage:
    """Estado de uso de una acción (limitada por día, recarga con tirada...).

    - ``AT_WILL``: siempre disponible, no consume nada.
    - ``PER_DAY``: ``uses_max`` usos por combate. Cada combate simulado
      representa un día con descansos hechos, así que ``reset()`` los
      restaura todos.
      # TODO: modelar varios encuentros por día (descansos intermedios).
    - ``RECHARGE_ROLL``: empieza cargada; al gastarse queda descargada y se
      recarga al inicio de un turno propio si la tirada ``recharge_dice``
      saca ``recharge_min`` o más.
    """

    kind: UsageKind
    uses_max: int = 0
    uses_left: int = 0
    recharge_dice: str = ""
    recharge_min: int = 0
    charged: bool = True
    # Informativo: resultado de la última tirada de recarga (para el log).
    last_roll: int = 0

    def __post_init__(self) -> None:
        if self.kind is UsageKind.AT_WILL:
            self.uses_max = 0
            self.uses_left = 0
            self.charged = True
        elif self.kind is UsageKind.PER_DAY:
            self.uses_max = max(0, int(self.uses_max))
            if self.uses_left <= 0:
                self.uses_left = self.uses_max
            self.charged = False
        else:  # RECHARGE_ROLL
            self.uses_max = 0
            self.uses_left = 0
            self.charged = True

    @property
    def available(self) -> bool:
        """¿La acción puede usarse ahora mismo?"""
        if self.kind is UsageKind.AT_WILL:
            return True
        if self.kind is UsageKind.PER_DAY:
            return self.uses_left > 0
        return bool(self.charged)

    def spend(self) -> None:
        """Gasta un uso de la acción."""
        if self.kind is UsageKind.AT_WILL:
            return
        if self.kind is UsageKind.PER_DAY:
            if self.uses_left > 0:
                self.uses_left -= 1
            return
        self.charged = False

    def reset(self) -> None:
        """Restaura el estado inicial (nuevo combate / nuevo día)."""
        if self.kind is UsageKind.AT_WILL:
            return
        if self.kind is UsageKind.PER_DAY:
            self.uses_left = self.uses_max
            return
        self.charged = True
        self.last_roll = 0

    def try_recharge(self, rng: random.Random) -> bool:
        """Tira la recarga de la acción. Devuelve True si se ha recargado.

        No consume RNG si la acción ya está cargada o si no es de tipo
        ``RECHARGE_ROLL``.
        """
        if self.kind is not UsageKind.RECHARGE_ROLL:
            return False
        if self.charged:
            return False
        if not self.recharge_dice:
            return False
        total = int(roll_dice(str(self.recharge_dice), rng))
        self.last_roll = total
        if total >= int(self.recharge_min):
            self.charged = True
            return True
        return False


def _log_line(ctx, line: str) -> None:
    """Añade una línea al log del combate si el contexto lo tiene."""
    log = getattr(ctx, "log", None)
    if log is None:
        return
    try:
        log.append(line)
    except Exception:
        pass


def begin_turn(actor, ctx):
    """Prepara el turno de ``actor``: reinicia los recursos y tira recargas.

    Orden (documentado):

    1. Se crean unos ``TurnResources`` nuevos (``ctx.resources``).
    2. Tiradas de recarga de las acciones descargadas del actor.
    3. ``attempt_escapes``: intentos de liberarse de los estados con prueba
       de escape (automáticos, no son una elección).
    4. Si el actor está incapacitado, se salta el turno (sin política y
       sin consumir RNG).

    La tirada de recarga ocurre al inicio del turno propio del monstruo, así
    que la primera tirada de un aliento usado en el turno N es al inicio del
    turno N+1 (nunca en el mismo turno en que se usó).
    """
    try:
        from .actions import TurnResources
    except ImportError:  # pragma: no cover - ejecución como script suelto
        try:
            from actions import TurnResources
        except ImportError:
            from dnd_sim.actions import TurnResources

    resources = TurnResources()
    try:
        ctx.resources = resources
    except Exception:
        pass

    # (2) Recargas de las acciones descargadas.
    rng = getattr(ctx, "rng", None)
    for action in getattr(actor, "actions", []) or []:
        usage = getattr(action, "usage", None)
        if usage is None:
            continue
        if usage.kind is not UsageKind.RECHARGE_ROLL:
            continue
        if usage.available:
            # Está cargada: no se tira nada (no se consume RNG).
            continue
        recharged = usage.try_recharge(rng)
        name = getattr(action, "name", "") or "acción"
        actor_name = getattr(actor, "name", actor)
        resultado = "recargado" if recharged else "no recarga"
        _log_line(
            ctx,
            f"{actor_name}: recarga {name} ({usage.last_roll} en {usage.recharge_dice})"
            f" -> {resultado}",
        )

    # (3) Intentos de escape (automáticos).
    try:
        from .conditions import attempt_escapes
    except ImportError:  # pragma: no cover - ejecución como script suelto
        try:
            from conditions import attempt_escapes
        except ImportError:
            from dnd_sim.conditions import attempt_escapes
    try:
        attempt_escapes(actor, ctx)
    except Exception:
        pass

    # (4) Un combatiente incapacitado pierde el turno entero.
    if not getattr(actor, "can_act", True):
        try:
            ctx.skip_turn = True
        except Exception:
            pass
        _log_line(ctx, f"{getattr(actor, 'name', actor)} está incapacitado y pierde su turno")
        return resources

    return resources


__all__ = ["UsageKind", "ActionUsage", "begin_turn"]

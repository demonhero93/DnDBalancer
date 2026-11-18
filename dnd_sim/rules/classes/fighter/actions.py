"""Acciones bonus de la clase Fighter (Guerrero).

Separadas de :mod:`features` para que el módulo de la clase baje de
700 líneas (receta de ``TODO.md``). Importan ``FighterFeatures``,
``_contexto`` y ``_rasgo`` de ``features``; ``apply_fighter`` (en
``features``) las importa de forma diferida para no crear un ciclo.
"""
from __future__ import annotations

from typing import Any

from ....core.dice import roll_dice
from ....core.log import log_line as _log_line
from ....model.actions import ActionType, CombatAction, TurnResources
from .features import _contexto, _rasgo


class SecondWindAction(CombatAction):
    """Tomar Aliento (acción bonus): cura 1d10 + nivel gastando un uso.

    Solo es elegible si el combatiente está herido y quedan usos; la
    elegibilidad no consume RNG (el ``pick`` del encuentro decide entre
    las acciones candidatas de forma uniforme).
    """

    def __init__(self) -> None:
        self.name = "Tomar Aliento"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # los usos viven en el rasgo (comparten con Tactical Mind)

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        trait = _rasgo(actor)
        if trait is None or trait.second_wind_usage is None:
            return False
        if not trait.second_wind_usage.available:
            return False
        # Solo si está herido (a PG completos no se gasta el uso).
        try:
            return int(actor.hp) < int(actor.max_hp)
        except Exception:
            return False

    def execute(self, context: Any) -> None:
        actor = context.actor
        trait = _rasgo(actor)
        rng = getattr(context, "rng", None)
        if (trait is None or trait.second_wind_usage is None
                or not trait.second_wind_usage.available or rng is None):
            return  # sin usos o sin RNG el rasgo se abstiene
        curado = int(roll_dice("1d10", rng)) + trait.level
        antes = int(actor.hp)
        actor.hp = min(int(actor.max_hp), antes + curado)
        trait.second_wind_usage.spend()
        _log_line(
            context,
            f"{actor.name} usa Tomar Aliento: {actor.hp - antes} PV "
            f"({trait.second_wind_usage.uses_left} usos)",
        )


class ActionSurgeAction(CombatAction):
    """Oleada de Acción (acción bonus, nivel 2+): restaura la acción del turno.

    Solo es elegible si la acción ya se gastó este turno (así no se gasta
    un uso en vano) y no se ha usado Oleada antes en el mismo turno. Al
    ejecutarse pone ``resources.action_used = False``: el encuentro ve
    la acción libre y ejecuta UNA pasada de acción extra (ver
    ``engine/combat/encounter.py``) que EXCLUYE las acciones de hechizo
    de PJ (``es_accion_magia``): la Oleada no puede lanzar conjuros
    (PHB).
    """

    def __init__(self) -> None:
        self.name = "Oleada de Acción"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # los usos viven en el rasgo (se restablecen en reset)

    @staticmethod
    def _recursos(args: tuple, kwargs: dict, ctx: Any) -> Any:
        resources = kwargs.get("resources")
        if resources is None:
            for a in args:
                if isinstance(a, TurnResources):
                    resources = a
        if resources is None:
            resources = getattr(ctx, "resources", None)
        return resources

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        trait = _rasgo(actor)
        if (trait is None or trait.level < 2
                or trait.surge_used_this_turn
                or trait.action_surge_usage is None
                or not trait.action_surge_usage.available):
            return False
        resources = self._recursos(args, kwargs, ctx)
        if resources is None:
            return False
        # Solo si la acción de este turno ya se gastó (si no, no aporta).
        return bool(resources.action_used)

    def execute(self, context: Any) -> None:
        actor = context.actor
        trait = _rasgo(actor)
        resources = getattr(context, "resources", None)
        if (trait is None or trait.action_surge_usage is None
                or trait.surge_used_this_turn
                or not trait.action_surge_usage.available
                or resources is None or not resources.action_used):
            return
        trait.action_surge_usage.spend()
        trait.surge_used_this_turn = True
        resources.action_used = False  # el encuentro hará una pasada más
        _log_line(
            context,
            f"{actor.name} usa Oleada de Acción: acción restaurada "
            f"({trait.action_surge_usage.uses_left} usos)",
        )


__all__ = ["ActionSurgeAction", "SecondWindAction"]

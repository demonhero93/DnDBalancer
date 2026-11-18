"""Acciones bonus de Rune Knight (Giant's Might e invocación de runas).

Módulo interno del paquete ``rune_knight``: elegibilidad sin RNG (el
``pick`` del encuentro decide entre candidatas).
"""
from __future__ import annotations

from typing import Any

from ......core.log import log_line as _log_line
from ......model.actions import ActionType, CombatAction
from ..._util import _de, _orden_tamano
from ...features import _contexto
from .features import RuneKnightFeatures

class GiantsMightAction(CombatAction):
    """Giant's Might (3, acción adicional): tamaño, FUE y daño extra.

    Elegible sin RNG (nivel >= 3, sin activar y con usos); el ``pick``
    del encuentro decide entre las acciones candidatas. Una vez
    activo dura todo el combate y no se vuelve a activar; el uso se
    gasta al ejecutar y el tamaño lo restaura ``Combatant.reset``.
    """

    def __init__(self) -> None:
        self.name = "Giant's Might"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # los usos viven en el rasgo

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        trait = _de(actor, RuneKnightFeatures)
        if trait is None or trait.level < 3:
            return False
        if trait.giants_might_activo:
            return False
        return int(trait.giants_might_usos) > 0

    def execute(self, context: Any) -> None:
        actor = context.actor
        trait = _de(actor, RuneKnightFeatures)
        if (trait is None or trait.giants_might_activo
                or int(trait.giants_might_usos) <= 0):
            return  # sin usos o ya activo: se abstiene
        trait.giants_might_usos -= 1
        trait.giants_might_activo = True
        nuevo = "huge" if trait.level >= 18 else "large"
        if _orden_tamano(actor) < _orden_tamano(nuevo):
            actor.size = nuevo
            _log_line(context, f"{getattr(actor, 'name', actor)} crece a "
                               f"{nuevo} (Giant's Might)")
        _log_line(context, f"{getattr(actor, 'name', actor)} activa "
                           f"Giant's Might")


#: Nombres de las runas para la acción y el log.
_NOMBRES_RUNA = {
    "cloud": "Cloud Rune",
    "fire": "Fire Rune",
    "frost": "Frost Rune",
    "hill": "Hill Rune",
    "stone": "Stone Rune",
    "storm": "Storm Rune",
}


class RuneInvokeAction(CombatAction):
    """Invocación de una runa (acción bonus; A7: Frost y Hill, A10: Storm).

    Una instancia por runa conocida: la elegibilidad no consume RNG
    (runa conocida, usos restantes, sin invocar y acción bonus libre;
    el ``pick`` del encuentro decide entre las acciones candidatas).
    Una vez invocada, la runa dura todo el combate y no se vuelve a
    invocar: los usos extra de Master of Runes quedan para las runas
    de efecto por invocación (Fire/Stone, A8/A9).
    """

    def __init__(self, runa: str) -> None:
        self.runa = runa
        self.name = _NOMBRES_RUNA.get(runa, f"Rune ({runa})")
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # los usos viven en el rasgo

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        trait = _de(actor, RuneKnightFeatures)
        if trait is None or self.runa not in trait.runas:
            return False
        if int(trait.usos_runa.get(self.runa, 0)) <= 0:
            return False
        return not getattr(trait, f"{self.runa}_activo", False)

    def execute(self, context: Any) -> None:
        actor = context.actor
        trait = _de(actor, RuneKnightFeatures)
        if (trait is None or self.runa not in trait.runas
                or int(trait.usos_runa.get(self.runa, 0)) <= 0
                or getattr(trait, f"{self.runa}_activo", False)):
            return
        if self.runa not in ("frost", "hill", "storm"):
            return  # fire/stone se activan solos (A8/A9); cloud (A11) no
        trait.usos_runa[self.runa] = int(trait.usos_runa[self.runa]) - 1
        if self.runa == "frost":
            trait.frost_activo = True
            _log_line(context, f"{actor.name} invoca Frost Rune: +2 a "
                               f"pruebas y salvaciones de FUE y CON")
        elif self.runa == "storm":
            trait.storm_activo = True
            _log_line(context, f"{actor.name} invoca Storm Rune: ventaja "
                               f"a sus aliados, desventaja a sus enemigos")
        else:
            trait.hill_activo = True
            trait._otorgar_hill(actor, context)
            _log_line(context, f"{actor.name} invoca Hill Rune: "
                               f"resistencia a B/P/C durante el combate")


__all__ = ["GiantsMightAction", "RuneInvokeAction"]

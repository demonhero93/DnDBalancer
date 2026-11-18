"""Acciones bonus de Battle Master (Feinting y Rally).

Módulo interno del paquete ``battle_master``: la elegibilidad decide
con ``pick``; el dado de superioridad lo gasta ``trait._tirar_dado``.
"""
from __future__ import annotations

from typing import Any

from ......core.log import log_line as _log_line
from ......core.randomness import pick
from ......model.actions import ActionType, CombatAction
from ..._util import _de
from ...features import _contexto
from .features import BattleMasterFeatures, _aliados

class FeintingAttackAction(CombatAction):
    """Ataque de Engaño (acción bonus): ventaja en el siguiente ataque.

    Solo es elegible con bonus libre, dados de superioridad restantes y
    sin marca ya encolada; la decisión de usarlo es un ``pick``
    «no»/«sí» (cero RNG si no es elegible, patrón Disparo Curvo). Al
    ejecutar encola ``feinting_pendiente``: la ventaja la concede
    ``modify_attack_modifiers`` y el dado, si el ataque impacta, lo
    aplica ``extra_attack_damage`` (una maniobra como máximo por
    ataque). Sin marca al empezar el turno la decisión caduca.
    """

    def __init__(self) -> None:
        self.name = "Ataque de Engaño"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # sin usos limitados: el límite es el bonus

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        trait = _de(actor, BattleMasterFeatures)
        if (trait is None
                or trait.feinting_pendiente
                or trait.maniobra_pendiente is not None
                or trait.dados_restantes <= 0):
            return False  # sin datos o ya encolado: cero RNG
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return False  # sin RNG el rasgo se abstiene
        if pick(rng, ("no", "si")) == "no":
            return False  # decisión aleatoria de usar la acción bonus
        return True

    def execute(self, context: Any) -> None:
        actor = context.actor
        trait = _de(actor, BattleMasterFeatures)
        rng = getattr(context, "rng", None)
        if (trait is None or rng is None or trait.feinting_pendiente
                or trait.dados_restantes <= 0):
            return
        trait.feinting_pendiente = True
        _log_line(context, f"{getattr(actor, 'name', actor)} se prepara "
                           f"para un Ataque de Engaño")


class BattleMasterRallyAction(CombatAction):
    """Rally (acción bonus): PV temporales a un aliado con un dado.

    PHB 2024: gasta un dado de superioridad y otorga al aliado elegido
    PV temporales iguales al dado + mod CAR del dueño (mínimo 1; no se
    acumulan: se queda el mayor, patrón aura tundra). Solo es elegible
    con la maniobra conocida, bonus libre, dados restantes y algún
    aliado vivo distinto del dueño; la decisión de usarla es un
    ``pick`` «no»/«sí» (cero RNG si no es elegible, patrón Feinting).
    El dado se gasta en ``execute`` con ``_tirar_dado`` (Relentless
    incluido) y Rally no consume la reacción de nadie.
    """

    def __init__(self) -> None:
        self.name = "Rally"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # sin usos limitados: el límite es el bonus

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        trait = _de(actor, BattleMasterFeatures)
        if (trait is None
                or "Rally" not in trait.maneuvers
                or trait.dados_restantes <= 0
                or not _aliados(actor, ctx)):
            return False  # sin maniobra/datos/aliados: cero RNG
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return False  # sin RNG el rasgo se abstiene
        if pick(rng, ("no", "si")) == "no":
            return False  # decisión aleatoria de usar la acción bonus
        return True

    def execute(self, context: Any) -> None:
        actor = context.actor
        trait = _de(actor, BattleMasterFeatures)
        rng = getattr(context, "rng", None)
        if (trait is None or rng is None or "Rally" not in trait.maneuvers
                or trait.dados_restantes <= 0):
            return
        aliados = _aliados(actor, context)
        if not aliados:
            return  # sin aliados no se decide (no debería llegar)
        aliado = pick(rng, aliados)
        valor, _ = trait._tirar_dado(rng)
        cantidad = max(1, valor + int(actor.abilities.mod("cha")))
        actual = int(getattr(aliado, "temp_hp", 0) or 0)
        aliado.temp_hp = max(actual, cantidad)  # no se acumula
        _log_line(context, f"Rally: {getattr(aliado, 'name', aliado)} "
                           f"recibe {cantidad} PV temporales")


__all__ = ["BattleMasterRallyAction", "FeintingAttackAction"]

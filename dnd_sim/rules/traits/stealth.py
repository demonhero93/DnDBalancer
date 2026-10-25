"""Rasgos de sigilo: Superior Invisibility (pixie)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .base import Trait
from ..conditions import Condition

@dataclass
class SuperiorInvisibility(Trait):
    """Superior Invisibility (pixie): la acción de volverse invisible.

    «The pixie magically turns invisible until its concentration ends (as
    if concentrating on a spell).» (SRD 2014) A diferencia del hechizo
    Invisibility, **no** termina al atacar ni al lanzar un hechizo: por eso
    la condición se aplica con ``break_on_attack=False``
    (:class:`dnd_sim.rules.conditions.ConditionInstance`) y solo la quitan el
    reset y el final del combate.

    La ficha la trae como acción de la criatura y el motor solo construye
    acciones desde el campo ``actions`` de la ficha: por eso el rasgo la
    aporta con el hook ``extra_actions``, que :class:`dnd_sim.model.combatant.Monster`
    consulta una sola vez al construirse. Es una acción a voluntad; una vez
    invisible ya no se pierde, así que ``SpellStateAction.can_use`` deja de
    ofrecerla (no hay nada que refrescar).

    # TODO: la concentración no llega a consumirse en el motor (no hay
    # salvación por daño al concentrarse), así que en la práctica la
    # invisibilidad dura el combate.
    # TODO: la ficha del pixie no está ni en la caché ni en la API de
    # dnd5eapi.co (tampoco la del hobgoblin warlord), así que este rasgo se
    # prueba con el texto del SRD.
    """

    def extra_actions(self, owner: Any) -> list:
        from ..spells import SpellStateAction, StateEffect
        return [SpellStateAction(
            effect=StateEffect(condition=Condition.INVISIBLE,
                               duration_rounds=None, target="self",
                               break_on_attack=False),
            name=self.name or "Superior Invisibility",
        )]

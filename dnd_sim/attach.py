"""Enganche: una criatura se latcha sobre otra (cloaker).

Modela el texto del ataque **Bite** del cloaker (SRD 2014):

- «if the target is Large or smaller, the cloaker attaches to it» — los
  tamaños no se modelan, así que el enganche es siempre (# TODO: tamaño).
- «If the cloaker has advantage against the target, the cloaker attaches to
  the target's head, and the target is blinded and unable to breathe while
  the cloaker is attached.» — la ceguera sí se modela
  (:class:`dnd_sim.conditions.Condition` ``BLINDED``, puesta por el
  enganchador y retirada al desenganchar); «unable to breathe» queda como
  TODO (el motor no simula asfixia).
- «While attached, the cloaker can make this attack only against the target
  and has advantage on the attack roll.» — la ventaja la aporta el rasgo
  :class:`Attach` (via ``Combatant.traits``) y la restricción de objetivo
  la aplica :func:`dnd_sim.targeting.valid_targets` cuando recibe el
  ``atk`` concreto.
- «The cloaker can detach itself by spending 5 feet of its movement.» —
  # TODO: el movimiento no se modela, así que el que engancha no se suelta
  por su cuenta.
- «A creature, including the target, can take its action to detach the
  cloaker by succeeding on a DC 16 Strength check.» —
  :func:`intentar_desenganche`, automática al inicio del turno como
  :func:`dnd_sim.conditions.attempt_escapes` (gasta la acción acierte o
  falle).

El estado vive en :class:`dnd_sim.combat_state.CombatState`:
``attached_to`` solo lo guarda el que engancha; la criatura enganchada no
guarda referencia (la búsqueda inversa es :func:`enganchador_de`).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:
    from .actions import ActionType
    from .conditions import Condition, apply_condition
    from .dice import RollMode
    from .traits import Trait
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from actions import ActionType
        from conditions import Condition, apply_condition
        from dice import RollMode
        from traits import Trait
    except ImportError:
        from dnd_sim.actions import ActionType
        from dnd_sim.conditions import Condition, apply_condition
        from dnd_sim.dice import RollMode
        from dnd_sim.traits import Trait

#: CD de la prueba de Fuerza para desengancharse (ficha del cloaker).
DC_DESENGANCHE = 16


try:
    from .log import log_line as _log_line
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from log import log_line as _log_line
    except ImportError:
        from dnd_sim.log import log_line as _log_line


def _ya_cegado_por(target: Any, enganchador: Any) -> bool:
    """¿Ya está ``target`` cegado por esta misma fuente?"""
    try:
        for instance in target.conditions.instances:
            if instance.condition is Condition.BLINDED and instance.source is enganchador:
                return True
    except Exception:
        pass
    return False


@dataclass
class Attach(Trait):
    """Enganche: ventaja contra la criatura a la que te has enganchado.

    «While attached, the cloaker ... has advantage on the attack roll.» La
    otra parte de la regla (el ataque enganchado solo puede ir contra esa
    criatura) la aplica :func:`dnd_sim.targeting.valid_targets` con el
    ``atk`` concreto.
    """

    name: str = "Enganche"

    def modify_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                                rango: Any, ctx: Any = None,
                                rng: Any = None) -> None:
        enganchado = getattr(getattr(attacker, "state", None), "attached_to", None)
        if enganchado is target:
            mods.advantage_sources.append(self.name or "Enganche")


@dataclass
class AttachOnHitEffect:
    """Si el ataque impacta, el atacante se engancha al objetivo.

    Lo ejecuta ``attack_roll`` (:mod:`dnd_sim.combat`) tras el daño con la
    firma ``execute(attacker, target, ctx, modifiers)``; los modificadores
    hacen falta para el enganche a la cabeza (solo aplica si el ataque iba
    con ventaja).
    """

    #: El ataque con este efecto solo puede apuntar a la criatura enganchada.
    restringe_a_enganchado: bool = True
    #: Modelar el enganche a la cabeza (ventaja -> ceguera) de la ficha.
    cabeza: bool = True

    def execute(self, attacker: Any, target: Any, ctx: Any = None,
                modifiers: Any = None) -> None:
        state = getattr(attacker, "state", None)
        if state is None:
            return
        if not getattr(attacker, "alive", True) or not getattr(target, "alive", True):
            return
        if getattr(state, "attached_to", None) is not target:
            state.attached_to = target
            _log_line(
                ctx,
                f"{getattr(attacker, 'name', attacker)} se engancha a "
                f"{getattr(target, 'name', target)}",
            )
        # A la cabeza: con ventaja en el ataque, el objetivo queda cegado
        # mientras dure el enganche (sin repetir la instancia ya puesta).
        con_ventaja = (
            modifiers is not None
            and getattr(modifiers, "mode", None) is RollMode.ADVANTAGE
        )
        if self.cabeza and con_ventaja and not _ya_cegado_por(target, attacker):
            _log_line(
                ctx,
                f"{getattr(attacker, 'name', attacker)} se engancha a la cabeza de "
                f"{getattr(target, 'name', target)}",
            )
            apply_condition(target, Condition.BLINDED, ctx, source=attacker)


def enganchador_de(actor: Any, ctx: Any = None) -> Any:
    """Combatiente vivo enganchado a ``actor`` (o ``None``).

    El estado solo lo guarda el que engancha (``state.attached_to``), así
    que aquí se busca al revés por la lista de combatientes del contexto.
    """
    if not getattr(actor, "alive", True):
        return None
    for combatiente in getattr(ctx, "combatants", None) or []:
        if combatiente is actor:
            continue
        if not getattr(combatiente, "alive", True):
            continue
        if getattr(getattr(combatiente, "state", None), "attached_to", None) is actor:
            return combatiente
    return None


def desenganchar(enganchador: Any, ctx: Any = None, *, log: bool = True) -> Any:
    """Suelta a la criatura enganchada y retira su ceguera de enganche.

    Devuelve la criatura que estaba enganchada (o ``None``).
    """
    state = getattr(enganchador, "state", None)
    otro = getattr(state, "attached_to", None)
    if otro is None:
        return None
    state.attached_to = None
    # La ceguera del enganche a la cabeza se retira al soltar: solo las
    # instancias puestas por este enganchador (si otra fuente también lo
    # cegó, esa se queda).
    try:
        tracker = getattr(otro, "conditions", None)
        if tracker is not None:
            for instance in list(tracker.instances):
                if instance.condition is Condition.BLINDED and instance.source is enganchador:
                    tracker.remove_instance(instance)
    except Exception:
        pass
    if log:
        _log_line(
            ctx,
            f"{getattr(enganchador, 'name', enganchador)} se desengancha de "
            f"{getattr(otro, 'name', otro)}",
        )
    return otro


def intentar_desenganche(actor: Any, ctx: Any) -> None:
    """Prueba de Fuerza CD 16 para desengancharse (automática, gasta acción).

    Se llama al inicio del turno del afectado, junto a
    :func:`dnd_sim.conditions.attempt_escapes` y con su misma filosofía:

    - solo quien está enganchado por otro intenta algo (el que engancha se
      suelta solo con su movimiento: TODO de la ficha),
    - si está incapacitado no intenta nada (ni consume RNG),
    - si le queda la acción, la gasta acierte o falle («can take its
      action to detach the cloaker»); si ya la gastó, no intenta nada.
    """
    if not getattr(actor, "can_act", True):
        return
    enganchador = enganchador_de(actor, ctx)
    if enganchador is None:
        return
    recursos = getattr(ctx, "resources", None)
    if recursos is None:
        return
    try:
        if not recursos.can_use(ActionType.ACTION):
            return  # sin acción no puede intentarlo este turno
    except Exception:
        return

    try:
        from .checks import ability_check
    except ImportError:  # pragma: no cover - ejecución como script suelto
        try:
            from checks import ability_check
        except ImportError:
            from dnd_sim.checks import ability_check

    rng = getattr(ctx, "rng", None)
    resultado = ability_check(actor, "str", DC_DESENGANCHE, rng)
    nombre = getattr(actor, "name", actor)
    otro = getattr(enganchador, "name", enganchador)
    if resultado.success:
        desenganchar(enganchador, ctx, log=False)
        _log_line(
            ctx,
            f"{nombre} se desengancha de {otro} "
            f"(prueba FUE {resultado.total} vs CD {DC_DESENGANCHE})",
        )
    else:
        _log_line(
            ctx,
            f"{nombre} no logra desengancharse "
            f"(prueba FUE {resultado.total} vs CD {DC_DESENGANCHE})",
        )
    try:
        recursos.use(ActionType.ACTION)
    except Exception:
        pass


__all__ = [
    "DC_DESENGANCHE", "Attach", "AttachOnHitEffect",
    "enganchador_de", "desenganchar", "intentar_desenganche",
]

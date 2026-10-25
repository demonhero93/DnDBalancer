"""Acciones de hechizo que el motor ejecuta en un turno."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ...model.actions import ActionType, CombatAction, CombatContext, TurnResources
from ..conditions import apply_condition, remove_invisibility_on_action
from ...core.dice import roll_dice
from ...core.randomness import pick
from ...core.targeting import valid_targets
from ..usage import ActionUsage
from .effects import _tiene_estado, apply_concentration
from .reactions import trigger_reaction


def _romper_invisibilidad_al_lanzar(context: CombatContext) -> None:
    """Lanzar un hechizo termina la propia invisibilidad del lanzador.

    «[Invisibility] ends if the target attacks or casts a spell». El duergar
    lo declara además para su Enlarge/Reduce. Se ejecuta al **principio** de
    cada acción de hechizo, antes de que su efecto se resuelva: así el
    hechizo Invisibility se re-aplica después (quien lo refresca sigue
    invisible) pero Enlarge u otro hechizo dejan al lanzador visible.

    Solo quita la invisibilidad **estándar**
    (:func:`dnd_sim.rules.conditions.remove_invisibility_on_action`): la Superior
    Invisibility de la pixie, que dura lo que su concentración, no se toca.

    Es idempotente: si el lanzador no estaba invisible no hace nada ni
    registra nada en el log, por lo que llamarlo más de una vez (p. ej. un
    ``SpellAction`` que envuelve a otra acción de hechizo) es inofensivo.
    """
    actor = getattr(context, "actor", None)
    if actor is None:
        return
    # No se pasa ctx: aquí se añade la línea con el **motivo** («lanza un
    # hechizo»), igual que hace attack_roll con «(ataca)».
    if remove_invisibility_on_action(actor):
        log = getattr(context, "log", None)
        if log is not None:
            log.append(
                f"  {getattr(actor, 'name', actor)} deja de estar invisible "
                f"(lanza un hechizo)"
            )


@dataclass
class SpellAttackAction(CombatAction):
    """Ataque de hechizo con uno o varios elementos.

    Cada elemento es un ataque independiente contra un objetivo elegido al
    azar (p. ej. los cuatro rayos del hechizo de fuerza arcana).
    """

    spell: Any = None
    attacks: list = field(default_factory=list)
    damage_options: list = field(default_factory=list)
    action_type: ActionType = ActionType.ACTION
    name: str = "Hechizo"
    usage: ActionUsage | None = None

    def execute(self, context: CombatContext) -> None:
        _romper_invisibilidad_al_lanzar(context)
        from ...engine.combat import attack_roll
        ataques = self.attacks
        if self.damage_options:
            # Varias opciones de daño: se elige una al azar al lanzar.
            from dataclasses import replace
            dados = pick(context.rng, self.damage_options)
            ataques = [replace(a, damage=dados) for a in ataques]
        for atk in ataques:
            enemies = valid_targets(context.actor, ctx=context)
            if not enemies:
                return
            target = pick(context.rng, enemies)
            log = context.log if (context.log is not None) else None
            attack_roll(context.actor, target, atk, context.rng, log, ctx=context)


@dataclass
class SpellFixedDamageAction(CombatAction):
    """Daño automático: acierta siempre y sin tirada de ataque ni de
    salvación (p. ej. el Proyectil Mágico).

    El objetivo se elige al azar entre los hostiles vivos y el daño pasa por
    :func:`dnd_sim.rules.damage.apply_damage_modifiers` igual que el de un ataque
    (un inmune al tipo de daño no pierde PV).
    """

    damage: str = "1d4"
    damage_type: str = "force"
    elements: int = 1
    action_type: ActionType = ActionType.ACTION
    name: str = "Hechizo"
    usage: ActionUsage | None = None

    def execute(self, context: CombatContext) -> None:
        _romper_invisibilidad_al_lanzar(context)
        from ..damage import (apply_damage_modifiers, inflict_damage,
                             parse_damage_type)
        from ...engine.combat import _tag_modificadores
        alcanzados = []
        for _ in range(max(1, int(self.elements or 1))):
            targets = valid_targets(context.actor, ctx=context)
            if not targets:
                return
            target = pick(context.rng, targets)
            dt = parse_damage_type(self.damage_type)
            cantidad = roll_dice(self.damage, context.rng)
            # Como el daño de un ataque, la inmunidad/resistencia/
            # vulnerabilidad del objetivo se resuelve antes de infligir
            # (p. ej. un objetivo inmune al daño de fuerza no pierde PV
            # con el Proyectil Mágico).
            final = apply_damage_modifiers(cantidad, dt, target)
            inflict_damage(target, final, dt,
                           source=context.actor, ctx=context)
            alcanzados.append(target)
            log = context.log if (context.log is not None) else None
            if log is not None:
                tag = _tag_modificadores(cantidad, final, dt, target)
                log.append(f"  {getattr(context.actor, 'name', context.actor)} -> "
                           f"{getattr(target, 'name', target)} con {self.name}: "
                           f"{final} daño{tag} "
                           f"(HP {max(target.hp, 0)}/{target.max_hp})")
        # Reacciones de los objetivos heridos (una por turno propio cada uno).
        for objetivo in alcanzados:
            trigger_reaction(objetivo, context)


@dataclass
class HealAction(CombatAction):
    """Curación: solo se lanza contra un **aliado que ha perdido vida**."""

    effect: Any = None            # HealEffect
    action_type: ActionType = ActionType.ACTION
    name: str = "Curación"
    usage: ActionUsage | None = None

    def _aliados_heridos(self, context: CombatContext) -> list:
        """Aliados (mismo bando) que han perdido vida."""
        actor = context.actor
        enemigos = valid_targets(actor, ctx=context)
        aliados = []
        for c in getattr(context, "combatants", None) or []:
            if c is actor:
                continue
            if c in enemigos:
                continue
            if not getattr(c, "alive", False):
                continue
            if getattr(c, "hp", 0) >= getattr(c, "max_hp", 0):
                continue
            aliados.append(c)
        return aliados

    def can_use(self, *args, **kwargs) -> bool:
        usage = getattr(self, "usage", None)
        if usage is not None and not usage.available:
            return False
        context = None
        for arg in args:
            if hasattr(arg, "rng") and hasattr(arg, "actor"):
                context = arg
        context = context or kwargs.get("context") or kwargs.get("ctx")
        if context is None:
            return True
        return bool(self._aliados_heridos(context))

    def execute(self, context: CombatContext) -> None:
        _romper_invisibilidad_al_lanzar(context)
        objetivo = None
        aliados = self._aliados_heridos(context)
        if aliados:
            objetivo = pick(context.rng, aliados)
        if objetivo is None or self.effect is None:
            return
        cantidad = self.effect.amount(context.rng)
        antes = getattr(objetivo, "hp", 0)
        objetivo.hp = min(int(getattr(objetivo, "max_hp", 0)),
                          int(antes) + int(cantidad))
        log = context.log if (context.log is not None) else None
        if log is not None:
            log.append(f"  {getattr(context.actor, 'name', context.actor)} cura a "
                       f"{getattr(objetivo, 'name', objetivo)} con {self.name}: "
                       f"+{cantidad} HP (HP {objetivo.hp}/{objetivo.max_hp})")


@dataclass
class SpellStateAction(CombatAction):
    """Hechizo que deja un estado (guiado, marcado...).

    ``effect`` es un :class:`StateEffect`. El estado se aplica al lanzador
    (``target="self"``) o a un aliado (``target="ally"``).

    Si el estado dura hasta un evento y el actor ya lo tiene, la acción no
    se ofrece: re-aplicarlo no cambiaría nada y solo gastaría la acción
    (véase :meth:`can_use`). Por eso la Superior Invisibility de la pixie
    se ofrece una sola vez: una vez usada ya no se pierde.
    """

    effect: Any = None            # StateEffect
    action_type: ActionType = ActionType.ACTION
    name: str = "Hechizo"
    usage: ActionUsage | None = None

    def _aliados(self, context: CombatContext) -> list:
        actor = context.actor
        enemigos = valid_targets(actor, ctx=context)
        aliados = []
        for c in getattr(context, "combatants", None) or []:
            if c is actor or c in enemigos:
                continue
            if not getattr(c, "alive", False):
                continue
            aliados.append(c)
        return aliados

    def can_use(self, *args, **kwargs) -> bool:
        usage = getattr(self, "usage", None)
        if usage is not None and not usage.available:
            return False
        context = None
        for arg in args:
            if hasattr(arg, "rng") and hasattr(arg, "actor"):
                context = arg
        context = context or kwargs.get("context") or kwargs.get("ctx")
        if context is None:
            return True
        if getattr(self.effect, "target", "self") == "ally":
            return bool(self._aliados(context))
        # Un estado que dura hasta un evento (invisible: hasta atacar o
        # lanzar) no se «refresca»: si el actor ya lo tiene, aplicarlo otra
        # vez no cambiaría nada y solo gastaría la acción. Superior
        # Invisibility es at-will, así que aquí es donde se evita el gasto.
        condicion = getattr(self.effect, "condition", None)
        if (condicion is not None
                and getattr(self.effect, "duration_rounds", None) is None
                and _tiene_estado(getattr(context, "actor", None), condicion)):
            return False
        return True

    def execute(self, context: CombatContext) -> None:
        _romper_invisibilidad_al_lanzar(context)
        efecto = self.effect
        if efecto is None:
            return
        objetivo = context.actor
        if getattr(efecto, "target", "self") == "ally":
            aliados = self._aliados(context)
            if not aliados:
                return
            objetivo = pick(context.rng, aliados)
        try:
            apply_condition(
                objetivo, efecto.condition, context,
                source=context.actor,
                duration_rounds=getattr(efecto, "duration_rounds", None),
                break_on_attack=getattr(efecto, "break_on_attack", True),
            )
        except Exception:
            pass


@dataclass
class SpellAction(CombatAction):
    """Lanzamiento de un hechizo.

    Aplica la concentración (si el hechizo la requiere) y delega el efecto
    en ``effect``.
    """

    spell: Any = None             # Spell
    effect: Any = None            # CombatAction (el efecto real)
    concentration: bool = False
    duration_rounds: int | None = None
    action_type: ActionType = ActionType.ACTION
    name: str = "Hechizo"
    usage: ActionUsage | None = None

    def can_use(self, *args, **kwargs) -> bool:
        # 1. Uso limitado propio (el pool de slots del nivel del hechizo).
        usage = getattr(self, "usage", None)
        if usage is not None and not usage.available:
            return False
        # 2. Recurso de turno de **su** tipo de acción (acción, acción bonus
        #    o reacción). Se comprueba aquí porque algunos efectos sobrescriben
        #    can_use() sin mirar los recursos (p. ej. HealAction): sin esta
        #    comprobación, un hechizo de acción bonus se filtraría en su fase.
        resources = kwargs.get("resources")
        context = kwargs.get("context") or kwargs.get("ctx")
        for arg in args:
            if isinstance(arg, TurnResources):
                resources = arg
            elif hasattr(arg, "rng") and hasattr(arg, "actor"):
                context = arg
        if resources is None and context is not None:
            resources = getattr(context, "resources", None)
        if resources is not None:
            try:
                if not resources.can_use(self.action_type):
                    return False
            except Exception:
                pass
        # 3. Restricciones del efecto (aliado herido, objetivos, su propio
        #    uso limitado...). El efecto comparte action_type con este.
        if self.effect is None:
            return False
        try:
            return bool(self.effect.can_use(*args, **kwargs))
        except Exception:
            return False

    def execute(self, context: CombatContext) -> None:
        _romper_invisibilidad_al_lanzar(context)
        if self.concentration:
            apply_concentration(context.actor, context, self.duration_rounds)
        if self.effect is not None:
            self.effect.execute(context)

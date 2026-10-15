"""Economía de acciones y contexto de combate."""
from __future__ import annotations

import random
from dataclasses import dataclass, field


def _valid_targets(actor, ctx=None, combatants=None, enemies=None):
    try:
        from .combatant import valid_targets as _vt
    except ImportError:
        try:
            from combatant import valid_targets as _vt
        except ImportError:
            from dnd_sim.combatant import valid_targets as _vt
    return _vt(actor, ctx=ctx, combatants=combatants, enemies=enemies)
from enum import Enum
from typing import TYPE_CHECKING, Any, Iterable

if TYPE_CHECKING:
    from .combatant import Combatant
    from .attack import Attack


class ActionType(Enum):
    ACTION = "action"
    BONUS_ACTION = "bonus_action"
    REACTION = "reaction"
    MOVEMENT = "movement"


class CombatAction:
    """Acción genérica de combate."""

    name: str = ""
    action_type: ActionType = ActionType.ACTION

    def can_use(self, *args, **kwargs) -> bool:
        """Acepta (resources), (context) o ambos, de forma tolerante."""
        resources = kwargs.get("resources")
        context = kwargs.get("context") or kwargs.get("ctx")
        for arg in args:
            if isinstance(arg, TurnResources):
                resources = arg
            elif hasattr(arg, "rng") and hasattr(arg, "actor"):
                context = arg
        if resources is None and context is not None:
            resources = getattr(context, "resources", None)
        if resources is None:
            return True
        try:
            return bool(resources.can_use(self.action_type))
        except Exception:
            return True

    def execute(self, context: Any) -> None:
        raise NotImplementedError


@dataclass
class AttackEntry:
    attack_name: str
    count: int = 1


@dataclass
class TurnResources:
    action_used: bool = False
    bonus_action_used: bool = False
    reaction_used: bool = False
    movement_used: bool = False

    def can_use(self, action_type: ActionType) -> bool:
        if action_type == ActionType.ACTION:
            return not self.action_used
        if action_type == ActionType.BONUS_ACTION:
            return not self.bonus_action_used
        if action_type == ActionType.REACTION:
            return not self.reaction_used
        if action_type == ActionType.MOVEMENT:
            return not self.movement_used
        return True

    def use(self, action_type: ActionType) -> None:
        if action_type == ActionType.ACTION:
            self.action_used = True
        elif action_type == ActionType.BONUS_ACTION:
            self.bonus_action_used = True
        elif action_type == ActionType.REACTION:
            self.reaction_used = True
        elif action_type == ActionType.MOVEMENT:
            self.movement_used = True

    def spend(self, action_type: ActionType) -> None:
        self.use(action_type)


@dataclass
class CombatContext:
    rng: random.Random
    actor: "Combatant"
    combatants: list = field(default_factory=list)
    round: int = 0
    log: list[str] | None = None
    verbose: bool = False
    resources: TurnResources | None = None
    available_actions: list = field(default_factory=list)

    @property
    def enemies(self) -> list:
        return list(_valid_targets(self.actor, ctx=self))

    def living_enemies(self) -> list:
        return [c for c in (self.combatants or []) if getattr(c, "team", None) != self.actor.team and getattr(c, "alive", False)]


def _living_enemies(ctx: CombatContext) -> list:
    return list(_valid_targets(ctx.actor, ctx=ctx))


def _log(ctx: CombatContext):
    return ctx.log if (ctx.verbose or ctx.log is not None) else None


@dataclass
class AttackAction(CombatAction):
    attack: "Attack"
    action_type: ActionType = ActionType.ACTION
    name: str = ""

    def __post_init__(self):
        if not self.name:
            self.name = getattr(self.attack, "name", "Ataque")

    def execute(self, context: CombatContext) -> None:
        # Resolución real la hace attack_roll vía motor; aquí solo consumimos.
        # (Se espera que el motor invoque attack_roll por cada ataque.)
        from .combat import attack_roll  # local para evitar ciclos

        actor = context.actor
        enemies = _living_enemies(context)
        if not enemies:
            return
        # Un ataque suelto: objetivo aleatorio.
        from .randomness import pick

        target = pick(context.rng, enemies)
        log = context.log if (context.log is not None) else None
        # Log solo si verbose; mantenemos compatibilidad: attack_roll decide.
        attack_roll(actor, target, self.attack, context.rng, log)


class MultiattackAction(CombatAction):
    def __init__(self, options, action_type=ActionType.ACTION, name="Multiattack", combatant=None):
        self.options = options
        self.action_type = action_type
        self.name = name
        self.combatant = combatant

    def execute(self, context: CombatContext) -> None:
        from .combat import attack_roll
        from .randomness import pick

        actor = context.actor
        attacks_by_name = {getattr(a, "name", ""): a for a in getattr(actor, "attacks", [])}

        alternatives = self.options or []
        if not alternatives:
            return
        chosen = pick(context.rng, alternatives)
        for entry in chosen:
            attack_name = getattr(entry, "attack_name", None)
            count = getattr(entry, "count", 1) or 1
            atk = attacks_by_name.get(attack_name)
            if atk is None:
                raise ValueError(
                    f"El ataque {attack_name!r} no existe en {actor.name!r}.attacks"
                )
            for _ in range(count):
                enemies = _living_enemies(context)
                if not enemies:
                    return
                # Si el combate ya terminó (un solo equipo vivo), paramos.
                teams = {getattr(c, "team", None) for c in (context.combatants or []) if getattr(c, "alive", False)}
                if len(teams) <= 1:
                    return
                target = pick(context.rng, enemies)
                log = context.log
                attack_roll(actor, target, atk, context.rng, log)


class WeaponAttackAction(CombatAction):
    def __init__(self, name="Atacar", action_type=ActionType.ACTION):
        self.name = name
        self.action_type = action_type

    def execute(self, context: CombatContext) -> None:
        from .attack import Attack  # noqa: F401
        from .combat import attack_roll
        from .randomness import pick

        actor = context.actor
        weapons = list(getattr(actor, "weapons", []) or [])
        if not weapons:
            return
        total = 1 + int(getattr(actor, "extra_attacks", 0) or 0)
        for _ in range(total):
            enemies = _living_enemies(context)
            if not enemies:
                return
            teams = {getattr(c, "team", None) for c in (context.combatants or []) if getattr(c, "alive", False)}
            if len(teams) <= 1:
                return
            weapon = pick(context.rng, weapons)
            target = pick(context.rng, enemies)
            log = context.log
            attack_roll(actor, target, weapon, context.rng, log)


# Alias de coherencia por si algún código espera otro nombre.
WeaponAction = WeaponAttackAction
Multiattack = MultiattackAction


@dataclass
class SaveAction(CombatAction):
    effect: Any = None
    action_type: ActionType = ActionType.ACTION
    name: str = "Salvación"

    def __post_init__(self) -> None:
        if not getattr(self, "name", ""):
            self.name = "Salvación"

    def execute(self, context: CombatContext) -> None:
        try:
            from .saves import resolve_save_damage, SaveDamage
        except ImportError:
            try:
                from saves import resolve_save_damage, SaveDamage
            except ImportError:
                from dnd_sim.saves import resolve_save_damage, SaveDamage
        from .randomness import pick as _pick

        actor = context.actor
        targets = _valid_targets(actor, ctx=context)
        living = [t for t in targets if getattr(t, "alive", False)]
        if not living:
            return
        target = _pick(context.rng, living)
        effect = self.effect
        if not isinstance(effect, SaveDamage):
            try:
                effect = SaveDamage(
                    ability=getattr(effect, "ability", "dex"),
                    dc=getattr(effect, "dc", 0),
                    damage=getattr(effect, "damage", "1d6"),
                    damage_type=getattr(effect, "damage_type", "bludgeoning"),
                    on_success=getattr(effect, "on_success", "none"),
                )
            except Exception:
                return
        resolve_save_damage(actor, target, effect, context)

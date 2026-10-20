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

try:
    from .usage import ActionUsage, UsageKind
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from usage import ActionUsage, UsageKind
    except ImportError:
        from dnd_sim.usage import ActionUsage, UsageKind

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
    # Uso limitado opcional (dnd_sim.usage.ActionUsage). El estado de uso
    # vive en la acción, nunca en el combatiente.
    usage: ActionUsage | None = None

    def can_use(self, *args, **kwargs) -> bool:
        """Acepta (resources), (context) o ambos, de forma tolerante."""
        # 1. Uso limitado: si la acción está agotada o descargada, no se usa.
        usage = getattr(self, "usage", None)
        if usage is not None and not usage.available:
            return False
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
    # True si la entrada es una acción del monstruo (p. ej. el Aliento de fuego
    # de la quimera) y no un ataque suelto.
    is_action: bool = False


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
    # Estadísticas del combate en curso (compartidas por todos los contextos).
    action_uses: dict | None = None
    area_targets_hit: list | None = None
    conditions_applied: dict | None = None
    escape_attempts: dict | None = None
    escape_successes: dict | None = None
    attacks_at_range: list | None = None
    # El motor marca aquí los turnos que se pierden por incapacitación.
    skip_turn: bool = False

    @property
    def enemies(self) -> list:
        return list(_valid_targets(self.actor, ctx=self))

    def living_enemies(self) -> list:
        # Única fuente de verdad: valid_targets (hostiles vivos).
        return _living_enemies(self)


def _living_enemies(ctx: CombatContext) -> list:
    """Hostiles vivos del actor (alias de la fuente única ``valid_targets``)."""
    return list(_valid_targets(ctx.actor, ctx=ctx))


def _log(ctx: CombatContext):
    return ctx.log if (ctx.verbose or ctx.log is not None) else None


@dataclass
class AttackAction(CombatAction):
    attack: "Attack"
    action_type: ActionType = ActionType.ACTION
    name: str = ""
    usage: ActionUsage | None = None

    def __post_init__(self):
        if not self.name:
            self.name = getattr(self.attack, "name", "Ataque")
        if self.usage is None:
            # El ataque puede traer su propio uso limitado (p. ej. un
            # ataque con "recharge on roll" en la API).
            self.usage = getattr(self.attack, "usage", None)

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
        attack_roll(actor, target, self.attack, context.rng, log, ctx=context)


class MultiattackAction(CombatAction):
    """Acción de multiataque: elige una alternativa y ejecuta sus entradas.

    Una alternativa es una lista de entradas (ataques sueltos y/o acciones
    como un aliento). Las alternativas que incluyen una acción con uso
    limitado agotado (p. ej. un aliento descargado) no son viables: la ficha
    dice "cuando su aliento está disponible puede usarlo en lugar de X".
    """

    def __init__(self, options, action_type=ActionType.ACTION, name="Multiattack",
                 combatant=None, usage=None, action_entries=None):
        self.options = options
        self.action_type = action_type
        self.name = name
        self.combatant = combatant
        self.usage = usage
        # Acciones del monstruo incluidas en el multiataque (p. ej. el
        # Aliento de fuego de la quimera): nombre -> acción.
        self.action_entries = dict(action_entries or {})

    def _accion_por_nombre(self, actor, name):
        """Busca una acción del multiataque por nombre.

        Primero las acciones que el propio multiataque referencia (pueden no
        estar entre las acciones sueltas del combatiente) y después las del
        combatiente, excluyendo el propio multiataque y los ataques sueltos
        (que se resuelven aparte).
        """
        accion = self.action_entries.get(name)
        if accion is not None:
            return accion
        for accion in getattr(actor, "actions", []) or []:
            if accion is self:
                continue
            if isinstance(accion, AttackAction):
                continue
            if getattr(accion, "name", "") == name:
                return accion
        return None

    def _entrada_viable(self, entry, actor) -> bool:
        """¿Se puede usar esta entrada del multiataque ahora mismo?"""
        if not getattr(entry, "is_action", False):
            return True
        accion = self._accion_por_nombre(actor, getattr(entry, "attack_name", ""))
        if accion is None:
            return False
        usage = getattr(accion, "usage", None)
        return usage is None or usage.available

    def execute(self, context: CombatContext) -> None:
        from .combat import attack_roll
        from .randomness import pick

        actor = context.actor
        attacks_by_name = {getattr(a, "name", ""): a for a in getattr(actor, "attacks", [])}

        alternatives = self.options or []
        if not alternatives:
            return
        viables = [alt for alt in alternatives
                   if all(self._entrada_viable(e, actor) for e in alt)]
        if not viables:
            return
        chosen = pick(context.rng, viables)
        for entry in chosen:
            attack_name = getattr(entry, "attack_name", None)
            count = getattr(entry, "count", 1) or 1
            if getattr(entry, "is_action", False):
                # Acción del monstruo (p. ej. aliento de área).
                accion = self._accion_por_nombre(actor, attack_name)
                if accion is None:
                    continue
                for _ in range(count):
                    enemies = _living_enemies(context)
                    if not enemies:
                        return
                    accion.execute(context)
                    usage = getattr(accion, "usage", None)
                    if usage is not None:
                        usage.spend()
                continue
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
                attack_roll(actor, target, atk, context.rng, log, ctx=context)


class WeaponAttackAction(CombatAction):
    def __init__(self, name="Atacar", action_type=ActionType.ACTION, usage=None):
        self.name = name
        self.action_type = action_type
        self.usage = usage

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
            attack_roll(actor, target, weapon, context.rng, log, ctx=context)


# Alias de coherencia por si algún código espera otro nombre.
WeaponAction = WeaponAttackAction
Multiattack = MultiattackAction


@dataclass
class SaveAction(CombatAction):
    effect: Any = None
    action_type: ActionType = ActionType.ACTION
    name: str = "Salvación"
    usage: ActionUsage | None = None

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

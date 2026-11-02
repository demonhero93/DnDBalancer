"""Economía de acciones y contexto de combate."""
from __future__ import annotations

import random
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

from ..core.targeting import valid_targets

if TYPE_CHECKING:
    from .combatant import Combatant
    from .attack import Attack
    # Solo en anotaciones: traer ``usage`` a nivel de módulo convertiría
    # model -> rules en una dependencia de importación real.
    from ..rules.usage import ActionUsage, UsageKind


class ActionType(Enum):
    ACTION = "action"
    BONUS_ACTION = "bonus_action"
    REACTION = "reaction"
    MOVEMENT = "movement"


class CombatAction:
    """Acción genérica de combate."""

    name: str = ""
    action_type: ActionType = ActionType.ACTION
    # Uso limitado opcional (dnd_sim.rules.usage.ActionUsage). El estado de uso
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
        # 2. Un combatiente a 0 PV (o ya marcado muerto) no lanza nada: si
        #    llega el contexto, la habilidad se niega aquí mismo.
        if context is not None and not actor_is_alive(context):
            return False
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
    # Estadísticas legendarias del combate en curso (compartidas por todos
    # los contextos): {"actions": {nombre: veces}, "points": int,
    # "resistances": int}.
    legendary_stats: dict | None = None
    # El motor marca aquí los turnos que se pierden por incapacitación.
    skip_turn: bool = False
    # True solo en ataques de reacción (Retaliation, Fiereza infecciosa...):
    # los rasgos con decisión por turno (Ataque Temerario) no deciden ni
    # reciben su efecto fuera del turno propio. Lo ponen las llamadas de
    # reacción con una copia superficial del contexto.
    is_reaction: bool = False

    @property
    def enemies(self) -> list:
        return list(valid_targets(self.actor, ctx=self))

    def living_enemies(self) -> list:
        # Única fuente de verdad: valid_targets (hostiles vivos).
        return _living_enemies(self)


def _living_enemies(ctx: CombatContext, atk: Any = None) -> list:
    """Hostiles vivos del actor (alias de la fuente única ``valid_targets``).

    ``atk`` (opcional): ataque concreto que se va a resolver; si el actor
    está enganchado y el ataque lo declara, los objetivos se reducen a la
    criatura enganchada (véase :func:`dnd_sim.core.targeting.valid_targets`).
    """
    return list(valid_targets(ctx.actor, ctx=ctx, atk=atk))


def actor_is_alive(context: Any) -> bool:
    """¿Sigue vivo el actor? Una habilidad no se lanza con PV <= 0.

    El motor no da turnos a los muertos, pero una habilidad puede llegar a
    ejecutarse **después** de que su propio actor haya caído en mitad de su
    turno (represalias, daño transferido, multiataques): en ese caso no se
    lanza. Todas las ``execute()`` lo comprueban antes de gastar dados.
    """
    actor = getattr(context, "actor", None)
    if actor is None:
        return True
    try:
        return bool(getattr(actor, "alive", True))
    except Exception:
        return True


def _log(ctx: CombatContext):
    return ctx.log if (ctx.verbose or ctx.log is not None) else None


@contextmanager
def _en_accion_de_ataque(context: Any, action_type: ActionType) -> None:
    """Marca ``context.in_attack_action`` mientras se ejecuta un ataque.

    ``True`` solo si la acción es una acción **de Atacar** (no una bonus o
    reacción): los rasgos que se activan «al atacar con la acción de
    Atacar» (las Garras del Path of the Beast) lo comprueban. Se restaura
    el valor anterior, así que las acciones anidadas (un multiataque que
    ejecuta otra acción) no dejan la marca puesta.
    """
    previo = getattr(context, "in_attack_action", None)
    context.in_attack_action = action_type == ActionType.ACTION
    try:
        yield
    finally:
        context.in_attack_action = previo


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
        if not actor_is_alive(context):
            return  # el actor ya no está en pie: la habilidad no se lanza
        from ..engine.combat import attack_roll  # local para evitar ciclos

        actor = context.actor
        enemies = _living_enemies(context, self.attack)
        if not enemies:
            return
        # Utilitaria: Agarrar/Empujar puede sustituir este ataque (el módulo
        # decide solo; import diferido para no crear ciclo model -> rules).
        from ..rules.utility import ataque_utilitario
        if ataque_utilitario(actor, context, context.rng, self.attack):
            return
        # Un ataque suelto: objetivo aleatorio.
        from ..core.randomness import pick

        target = pick(context.rng, enemies)
        log = context.log if (context.log is not None) else None
        # Log solo si verbose; mantenemos compatibilidad: attack_roll decide.
        with _en_accion_de_ataque(context, self.action_type):
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
        if not actor_is_alive(context):
            return  # el actor ya no está en pie: la habilidad no se lanza
        from ..engine.combat import attack_roll
        from ..core.randomness import pick

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
                    # El actor puede caer en mitad del multiataque (p. ej.
                    # daño transferido o represalias): se corta el resto.
                    if not actor_is_alive(context):
                        return
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
                if not actor_is_alive(context):
                    return  # el actor ha muerto: no sigue pegando
                enemies = _living_enemies(context, atk)
                if not enemies:
                    return
                # Si el combate ya terminó (un solo equipo vivo), paramos.
                teams = {getattr(c, "team", None) for c in (context.combatants or []) if getattr(c, "alive", False)}
                if len(teams) <= 1:
                    return
                # Utilitaria: Agarrar/Empujar puede sustituir este ataque.
                from ..rules.utility import ataque_utilitario
                if ataque_utilitario(actor, context, context.rng, atk):
                    continue
                target = pick(context.rng, enemies)
                log = context.log
                with _en_accion_de_ataque(context, self.action_type):
                    attack_roll(actor, target, atk, context.rng, log, ctx=context)


class WeaponAttackAction(CombatAction):
    def __init__(self, name="Atacar", action_type=ActionType.ACTION, usage=None):
        self.name = name
        self.action_type = action_type
        self.usage = usage

    def execute(self, context: CombatContext) -> None:
        if not actor_is_alive(context):
            return  # el actor ya no está en pie: la habilidad no se lanza
        from .attack import Attack  # noqa: F401
        from ..engine.combat import attack_roll
        from ..core.randomness import pick

        actor = context.actor
        # ``weapons`` (ficha) + ``dynamic_weapons`` (p. ej. el arma natural
        # del Path of the Beast mientras dura la Furia): la lista de la
        # ficha no se muta.
        weapons = list(getattr(actor, "weapons", []) or [])
        weapons += list(getattr(actor, "dynamic_weapons", []) or [])
        if not weapons:
            return
        total = 1 + int(getattr(actor, "extra_attacks", 0) or 0)
        for _ in range(total):
            if not actor_is_alive(context):
                return  # el actor ha muerto: no sigue pegando
            enemies = _living_enemies(context)
            if not enemies:
                return
            teams = {getattr(c, "team", None) for c in (context.combatants or []) if getattr(c, "alive", False)}
            if len(teams) <= 1:
                return
            weapon = pick(context.rng, weapons)
            # Utilitaria: Agarrar/Empujar puede sustituir este ataque (con
            # el arma ya elegida: a distancia no se sustituye, sin RNG).
            from ..rules.utility import ataque_utilitario
            if ataque_utilitario(actor, context, context.rng, weapon):
                continue
            target = pick(context.rng, enemies)
            log = context.log
            with _en_accion_de_ataque(context, self.action_type):
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
        if not actor_is_alive(context):
            return  # el actor ya no está en pie: la habilidad no se lanza
        from ..rules.saves import resolve_save_damage, SaveDamage
        from ..core.randomness import pick as _pick

        actor = context.actor
        targets = valid_targets(actor, ctx=context)
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

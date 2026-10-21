"""Hechizos (D&D 5e): modelo, reglas y acciones de lanzamiento.

Estructura de los hechizos:

- :class:`Spell`: el hechizo con su efecto ya interpretado (datos de la API
  SRD 2014 + el efecto que el motor sabe aplicar).
- :class:`Spellcasting`: los datos del lanzador (característica, CD de
  salvación, bonificador y nivel), tal y como vienen en la API.
- :class:`SpellAction`: la acción de combate que lanza el hechizo: aplica la
  concentración (si el hechizo la requiere) y **delega** el efecto en las
  acciones que ya existen (``AttackAction``, ``SaveAction``,
  ``AreaSaveAction`` o ``ConditionAction``).
- :class:`HealAction`: la acción de curación.

Reglas implementadas:

- Los **cantrips** (nivel 0) se lanzan cuantas veces se quiera: no gastan
  slots ni usos por día. Los hechizos de nivel 1 o superior consumen un
  **slot** del nivel correspondiente (el pool se comparte entre los hechizos
  del mismo nivel).
- Se ignoran los hechizos con **tiempo de lanzamiento de 1 minuto o más**
  (no influyen en el combate).
- Se ignoran los hechizos que solo afectan al **movimiento** (propio o ajeno);
  si además hacen daño o dejan una condición, se conserva ese efecto y se
  ignora el movimiento (con aviso).
- Si el hechizo tiene **varias opciones o elementos**, se eligen al azar.
- Los hechizos de **curación** solo se lanzan contra un **aliado que ha
  perdido vida**.
- El **tiempo de casteo** marca el tipo de acción: "1 action" -> acción,
  "1 bonus action" -> acción bonus, "1 reaction" -> reacción.
- Los **rituales** se ignoran (no se pueden usar en combate).
- Los hechizos que requieren **concentración** crean el estado
  ``CONCENTRATION`` en el lanzador (solo se mantiene una concentración a la
  vez).

# TODO: los hechizos de nivel 1 o superior (y sus slots) todavia no se
cargan: solo los cantrips.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

try:
    from .actions import ActionType, CombatAction, CombatContext
    from .conditions import Condition, apply_condition
    from .dice import roll_dice
    from .randomness import pick
    from .targeting import valid_targets
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from actions import ActionType, CombatAction, CombatContext
        from conditions import Condition, apply_condition
        from dice import roll_dice
        from randomness import pick
        from targeting import valid_targets
    except ImportError:
        from dnd_sim.actions import ActionType, CombatAction, CombatContext
        from dnd_sim.conditions import Condition, apply_condition
        from dnd_sim.dice import roll_dice
        from dnd_sim.randomness import pick
        from dnd_sim.targeting import valid_targets

try:
    from .usage import ActionUsage
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from usage import ActionUsage
    except ImportError:
        from dnd_sim.usage import ActionUsage


@dataclass
class Spellcasting:
    """Datos de lanzamiento de un lanzador de hechizos (de la API)."""

    ability: str = "int"
    save_dc: int = 10
    attack_bonus: int = 0
    level: int = 5
    slots: dict = field(default_factory=dict)
    # Hechizos del lanzador: [{"name", "level", "url"}].
    spells: list = field(default_factory=list)


@dataclass
class HealEffect:
    """Curación de un hechizo (dados ya resueltos: "1d8 + 12")."""

    heal: str = "1d8"

    def amount(self, rng) -> int:
        """Puntos de vida curados."""
        try:
            return int(roll_dice(self.heal, rng))
        except Exception:
            return 0


@dataclass
class StateEffect:
    """Estado que aplica un hechizo (sin salvación: el hechizo lo decide).

    ``target``: ``"self"`` (el lanzador) o ``"ally"`` (un aliado).
    """

    condition: Any = None
    duration_rounds: int | None = None
    target: str = "self"


@dataclass
class Spell:
    """Hechizo de la SRD 2014 con su efecto interpretado.

    ``kind`` dice qué efecto tiene:

    - ``"attack"``: ataque de hechizo (con ``elements`` elementos, cada uno
      contra un objetivo elegido al azar).
    - ``"save"``: daño con salvación (de objetivo único o de área).
    - ``"condition"``: deja una condición si el objetivo falla la salvación.
    - ``"heal"``: cura a un aliado herido.
    - ``""``: sin efecto modelable (utilidad, movimiento, etc.).
    """

    name: str
    index: str = ""
    level: int = 0
    school: str = ""
    casting_time: str = "1 action"
    range: str = ""
    duration: str = "Instantaneous"
    concentration: bool = False
    desc: list[str] = field(default_factory=list)
    # Tiempo de casteo -> tipo de acción (acción, acción bonus o reacción).
    action_type: ActionType = ActionType.ACTION
    # Nivel del slot que consume (0 = cantrip: no consume slot).
    slot_level: int = 0
    # --- Efecto ---
    kind: str = ""
    attack_type: str = ""        # "ranged" | "melee"
    damage: str = ""             # dados de daño
    damage_type: str = "bludgeoning"
    elements: int = 1            # nº de elementos (rayos, dardos...)
    dc_ability: str = ""         # característica de la salvación
    dc_success: str = "none"     # "none" | "half"
    heal: str = ""               # dados de curación
    condition: Any = None        # ConditionEffect
    state: Any = None            # StateEffect (hechizos de estado)
    state_target: str = ""       # "self" | "ally"
    damage_options: list = field(default_factory=list)  # opciones de daño
    area: bool = False
    ignored: str = ""            # motivo por el que no se modela

    @property
    def is_cantrip(self) -> bool:
        """Los cantrips se lanzan cuantas veces se quiera."""
        return int(self.level) == 0


# --- Acciones -------------------------------------------------------------- #


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
        try:
            from .combat import attack_roll
        except ImportError:  # pragma: no cover - ejecución como script suelto
            try:
                from combat import attack_roll
            except ImportError:
                from dnd_sim.combat import attack_roll
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

    El objetivo se elige al azar entre los hostiles vivos.
    """

    damage: str = "1d4"
    damage_type: str = "force"
    elements: int = 1
    action_type: ActionType = ActionType.ACTION
    name: str = "Hechizo"
    usage: ActionUsage | None = None

    def execute(self, context: CombatContext) -> None:
        try:
            from .damage import inflict_damage
        except ImportError:  # pragma: no cover - ejecución como script suelto
            try:
                from damage import inflict_damage
            except ImportError:
                from dnd_sim.damage import inflict_damage
        for _ in range(max(1, int(self.elements or 1))):
            targets = valid_targets(context.actor, ctx=context)
            if not targets:
                return
            target = pick(context.rng, targets)
            cantidad = roll_dice(self.damage, context.rng)
            inflict_damage(target, cantidad, self.damage_type,
                           source=context.actor)
            log = context.log if (context.log is not None) else None
            if log is not None:
                log.append(f"  {getattr(context.actor, 'name', context.actor)} -> "
                           f"{getattr(target, 'name', target)} con {self.name}: "
                           f"{cantidad} daño (HP {max(target.hp, 0)}/{target.max_hp})")


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
        return True

    def execute(self, context: CombatContext) -> None:
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
        usage = getattr(self, "usage", None)
        if usage is not None and not usage.available:
            return False
        if self.effect is None:
            return False
        try:
            return bool(self.effect.can_use(*args, **kwargs))
        except Exception:
            return False

    def execute(self, context: CombatContext) -> None:
        if self.concentration:
            apply_concentration(context.actor, context, self.duration_rounds)
        if self.effect is not None:
            self.effect.execute(context)


def duracion_en_rondas(duracion: str) -> int | None:
    """Duración de un hechizo en rondas (None = hasta el fin del combate)."""
    import re
    texto = str(duracion or "").lower()
    if "dispelled" in texto:
        return None
    if "round" in texto:
        return 1
    match = re.search(r"(\d+)\s*minute", texto)
    if match:
        return int(match.group(1)) * 10
    if "minute" in texto:
        return 10
    return None


def spell_action(spell: Spell, spellcasting: Spellcasting | None = None) -> CombatAction | None:
    """Construye la acción de combate de un hechizo.

    Reutiliza las acciones que ya existen: ``AttackAction`` (ataque de
    hechizo), ``SaveAction``/``AreaSaveAction`` (daño con salvación) y
    ``ConditionAction`` (condición con salvación).
    """
    if spell is None:
        return None
    try:
        from .actions import AttackAction, SaveAction
        from .area import AreaSaveAction, AreaTargeting
        from .attack import Attack
        from .conditions import ConditionAction
        from .roll_modifiers import AttackRange
        from .saves import SaveDamage
    except ImportError:  # pragma: no cover - ejecución como script suelto
        try:
            from actions import AttackAction, SaveAction
            from area import AreaSaveAction, AreaTargeting
            from attack import Attack
            from conditions import ConditionAction
            from roll_modifiers import AttackRange
            from saves import SaveDamage
        except ImportError:
            from dnd_sim.actions import AttackAction, SaveAction
            from dnd_sim.area import AreaSaveAction, AreaTargeting
            from dnd_sim.attack import Attack
            from dnd_sim.conditions import ConditionAction
            from dnd_sim.roll_modifiers import AttackRange
            from dnd_sim.saves import SaveDamage

    sc = spellcasting or Spellcasting()
    nombre = spell.name
    efecto = None

    if spell.kind == "attack":
        rango = AttackRange.RANGED if spell.attack_type == "ranged" else AttackRange.MELEE
        atk = Attack(
            name=nombre,
            damage=spell.damage,
            ability=sc.ability,
            proficient=True,
            attack_bonus=int(sc.attack_bonus),
            damage_bonus=0,
            damage_type=spell.damage_type,
            range_type=rango,
        )
        elementos = max(1, int(spell.elements or 1))
        if elementos == 1 and not spell.damage_options:
            efecto = AttackAction(atk, action_type=ActionType.ACTION, name=nombre)
        else:
            efecto = SpellAttackAction(
                spell=spell,
                attacks=[atk] * elementos,
                name=nombre,
                damage_options=list(spell.damage_options or []),
            )
    elif spell.kind == "save":
        eff = SaveDamage(
            ability=spell.dc_ability or "dex",
            dc=int(sc.save_dc),
            damage=spell.damage,
            damage_type=spell.damage_type,
            on_success=spell.dc_success,
        )
        if spell.area:
            efecto = AreaSaveAction(
                name=nombre, effect=eff, targeting=AreaTargeting(),
                action_type=ActionType.ACTION,
            )
        else:
            efecto = SaveAction(
                name=nombre, effect=eff, action_type=ActionType.ACTION,
            )
    elif spell.kind == "condition":
        efecto = ConditionAction(
            name=nombre, effect=spell.condition,
            targeting=AreaTargeting(min_targets=1, max_targets=1),
            action_type=ActionType.ACTION,
        )
    elif spell.kind == "heal":
        efecto = HealAction(effect=HealEffect(spell.heal), name=nombre)
    elif spell.kind == "state":
        efecto = SpellStateAction(effect=spell.state, name=nombre)
    elif spell.kind == "fixed":
        efecto = SpellFixedDamageAction(
            damage=spell.damage, damage_type=spell.damage_type,
            elements=max(1, int(spell.elements or 1)), name=nombre,
        )

    if efecto is None:
        return None

    return SpellAction(
        spell=spell,
        effect=efecto,
        concentration=bool(spell.concentration),
        duration_rounds=duracion_en_rondas(spell.duration),
        action_type=spell.action_type,
        name=nombre,
    )


def apply_concentration(caster: Any, ctx: Any,
                        duration_rounds: int | None = None) -> None:
    """Concentra: termina la concentración anterior y aplica la nueva.

    Solo se puede mantener una concentración por lanzador (lanzar otro
    hechizo concentrado termina el anterior).
    """
    tracker = getattr(caster, "conditions", None)
    if tracker is None:
        return
    try:
        for instance in list(getattr(tracker, "instances", []) or []):
            if instance.condition is Condition.CONCENTRATION:
                tracker.remove_instance(instance)
    except Exception:
        pass
    try:
        apply_condition(caster, Condition.CONCENTRATION, ctx, source=caster,
                        duration_rounds=duration_rounds)
    except Exception:
        pass


__all__ = [
    "Spell",
    "Spellcasting",
    "HealEffect",
    "StateEffect",
    "duracion_en_rondas",
    "spell_action",
    "SpellAction",
    "SpellAttackAction",
    "SpellFixedDamageAction",
    "SpellStateAction",
    "HealAction",
    "apply_concentration",
]

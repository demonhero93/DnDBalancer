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
  slots ni usos por día y su daño escala con el **nivel del lanzador**.
- Los hechizos de nivel 1 o superior consumen un **slot** del nivel
  correspondiente **al lanzarse** (nunca al construir la acción): el pool de
  cada nivel se comparte entre los hechizos de ese nivel y lo gasta el motor
  de combate vía ``usage.spend()``. Se cargan hechizos de **todos los
  niveles** (0-9) que traiga la ficha.
- **Upcasting** (preparado): ``spell_action(spell, sc, slot_level=N)`` lanza
  el hechizo en un slot de nivel N (>= que el del hechizo); el daño y la
  curación se reescalan con la tabla del hechizo (``damage_at_slot_level`` /
  ``heal_at_slot_level``). Por defecto se lanza en su propio nivel.
- Se ignoran los hechizos con **tiempo de lanzamiento de 1 minuto o más**
  (no influyen en el combate).
- Se ignoran los hechizos que solo afectan al **movimiento** (propio o ajeno);
  si además hacen daño o dejan una condición, se conserva ese efecto y se
  ignora el movimiento (con aviso).
- Si el hechizo tiene **varias opciones o elementos**, se eligen al azar.
- Los hechizos de **curación** solo se lanzan contra un **aliado que ha
  perdido vida**, y su MOD usa el **modificador de característica** del
  lanzador (bono de ataque menos competencia), no el bono completo.
- El **tiempo de casteo** marca el tipo de acción: "1 action" -> acción,
  "1 bonus action" -> acción bonus, "1 reaction" -> reacción. El tipo de
  acción del hechizo se propaga al efecto interno, así que un hechizo de
  acción bonus o de reacción se comprueba (y se ejecuta) en su propia fase.
- Los **rituales** se ignoran (no se pueden usar en combate).
- Los hechizos que requieren **concentración** crean el estado
  ``CONCENTRATION`` en el lanzador (solo se mantiene una concentración a la
  vez).
- **Reacciones** (:func:`trigger_reaction`): cuando un combatiente recibe
  daño puede disparar una acción de reacción (p. ej. Hellish Rebuke). Como
  en las reglas, es **una reacción por turno propio**: se gasta al usarse y
  se recarga al inicio del turno (``begin_turn``).

# Reglas de slots (detalle):
# - El estado real de los slots vive en el pool ``ActionUsage`` por nivel que
#   construye ``build_spell_actions()`` (compartido por los hechizos de ese
#   nivel) y se gasta en ``run_combat`` con ``usage.spend()``.
# - ``Spellcasting.initialize_slots(nivel_de_lanzador)`` rellena
#   ``slots`` con la tabla real de un lanzador completo (útil para creadores
#   de monstruos/PJ sin datos de API); ``slots[0] = None`` = cantrips.
# - La recuperación de slots al descansar se modela con ``usage.reset()``,
#   que se llama en ``Combatant.reset()`` (un combate = un día descansado).
#
# __all__ actualizado abajo.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

try:
    from .actions import ActionType, CombatAction, CombatContext, TurnResources
    from .conditions import Condition, apply_condition, remove_condition
    from .dice import roll_dice
    from .randomness import pick
    from .targeting import valid_targets
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from actions import ActionType, CombatAction, CombatContext, TurnResources
        from conditions import Condition, apply_condition, remove_condition
        from dice import roll_dice
        from randomness import pick
        from targeting import valid_targets
    except ImportError:
        from dnd_sim.actions import ActionType, CombatAction, CombatContext, TurnResources
        from dnd_sim.conditions import Condition, apply_condition, remove_condition
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


# Tabla de slots real de un **lanzador completo** (bardo, clérigo, druída,
# hechicero o mago: tabla PHB p. 113; el brujo de pacto tiene tabla propia).
# Índice = nivel de lanzador; valores = slots por nivel de hechizo 1..9.
FULL_CASTER_SLOTS: dict[int, tuple[int, ...]] = {
     1: (2, 0, 0, 0, 0, 0, 0, 0, 0),
     2: (3, 0, 0, 0, 0, 0, 0, 0, 0),
     3: (4, 2, 0, 0, 0, 0, 0, 0, 0),
     4: (4, 3, 0, 0, 0, 0, 0, 0, 0),
     5: (4, 3, 2, 0, 0, 0, 0, 0, 0),
     6: (4, 3, 3, 0, 0, 0, 0, 0, 0),
     7: (4, 3, 3, 1, 0, 0, 0, 0, 0),
     8: (4, 3, 3, 2, 0, 0, 0, 0, 0),
     9: (4, 3, 3, 3, 1, 0, 0, 0, 0),
    10: (4, 3, 3, 3, 2, 0, 0, 0, 0),
    11: (4, 3, 3, 3, 2, 1, 0, 0, 0),
    12: (4, 3, 3, 3, 2, 1, 0, 0, 0),
    13: (4, 3, 3, 3, 2, 1, 1, 0, 0),
    14: (4, 3, 3, 3, 2, 1, 1, 0, 0),
    15: (4, 3, 3, 3, 2, 1, 1, 1, 0),
    16: (4, 3, 3, 3, 2, 1, 1, 1, 0),
    17: (4, 3, 3, 3, 2, 1, 1, 1, 1),
    18: (4, 3, 3, 3, 3, 1, 1, 1, 1),
    19: (4, 3, 3, 3, 3, 2, 1, 1, 1),
    20: (4, 3, 3, 3, 3, 3, 2, 1, 1),
}


@dataclass
class Spellcasting:
    """Datos de lanzamiento de un lanzador de hechizos (de la API).

    ``ability_mod``: **modificador de característica** de lanzamiento (p. ej.
    +6 de INT). La API solo da ``modifier`` (bono de ataque = característica
    + competencia), así que ``parse_spellcasting`` lo deriva restando la
    competencia. Es el valor que usa el marcador ``MOD`` de la curación.
    """

    ability: str = "int"
    save_dc: int = 10
    attack_bonus: int = 0
    level: int = 5
    slots: dict = field(default_factory=dict)
    # Hechizos del lanzador: [{"name", "level", "url"}].
    spells: list = field(default_factory=list)
    # Modificador de característica (None = desconocido: se usa attack_bonus).
    ability_mod: int | None = None

    @property
    def heal_modifier(self) -> int:
        """MOD de la curación: modificador de característica si se conoce."""
        if self.ability_mod is not None:
            return int(self.ability_mod)
        return int(self.attack_bonus)

    def initialize_slots(self, caster_level: int = 1) -> None:
        """Rellena ``slots`` con la tabla real de un lanzador completo.

        - Nivel 0 (cantrips): None = usos infinitos.
        - Niveles 1..9: los slots de la tabla PHB para ``caster_level``
          (véase :data:`FULL_CASTER_SLOTS`). Un nivel de hechizo sin slots
          no se incluye (no se puede lanzar).
        """
        nivel = max(1, min(20, int(caster_level or 1)))
        tabla = FULL_CASTER_SLOTS[nivel]
        s = {0: None}  # cantrips infinitos
        for indice, cantidad in enumerate(tabla, start=1):
            if cantidad > 0:
                s[indice] = cantidad
        self.slots = s


@dataclass
class HealEffect:
    """Curación de un hechizo (dados ya resueltos: "1d8 + 5")."""

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
    # Nivel de slot por defecto con el que se lanza (0 = cantrip).
    slot_level: int = 0
    # --- Efecto ---
    kind: str = ""
    attack_type: str = ""        # "ranged" | "melee"
    damage: str = ""             # dados de daño (resueltos en slot_level)
    damage_type: str = "bludgeoning"
    elements: int = 1            # nº de elementos (rayos, dardos...)
    dc_ability: str = ""         # característica de la salvación
    dc_success: str = "none"     # "none" | "half"
    heal: str = ""               # dados de curación (resueltos en slot_level)
    condition: Any = None        # ConditionEffect
    state: Any = None            # StateEffect (hechizos de estado)
    state_target: str = ""       # "self" | "ally"
    damage_options: list = field(default_factory=list)  # opciones de daño
    area: bool = False
    ignored: str = ""            # motivo por el que no se modela
    # Tablas de escalado crudas de la API (para upcasting): nivel -> dados.
    # ``damage_table`` usa ``damage_at_character_level`` (cantrips) o
    # ``damage_at_slot_level`` (hechizos con slot); ``heal_table`` usa
    # ``heal_at_slot_level`` con el marcador ``MOD``.
    damage_table: dict = field(default_factory=dict)
    heal_table: dict = field(default_factory=dict)

    @property
    def is_cantrip(self) -> bool:
        """Los cantrips se lanzan cuantas veces se quiera."""
        return int(self.level) == 0


# --- Acciones -------------------------------------------------------------- #


def _romper_invisibilidad_al_lanzar(context: CombatContext) -> None:
    """Lanzar un hechizo termina la propia invisibilidad del lanzador.

    «[Invisibility] ends if the target attacks or casts a spell». El duergar
    lo declara además para su Enlarge/Reduce. Se ejecuta al **principio** de
    cada acción de hechizo, antes de que su efecto se resuelva: así el
    hechizo Invisibility se re-aplica después (quien lo refresca sigue
    invisible) pero Enlarge u otro hechizo dejan al lanzador visible.

    Es idempotente: si el lanzador no estaba invisible no hace nada ni
    registra nada en el log, por lo que llamarlo más de una vez (p. ej. un
    ``SpellAction`` que envuelve a otra acción de hechizo) es inofensivo.
    """
    actor = getattr(context, "actor", None)
    if actor is None:
        return
    # ctx=None para que remove_condition no registre por su cuenta: aquí se
    # añade la línea con el **motivo** («lanza un hechizo»), igual que hace
    # attack_roll con «(ataca)».
    if remove_condition(actor, Condition.INVISIBLE, None):
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

    El objetivo se elige al azar entre los hostiles vivos y el daño pasa por
    :func:`dnd_sim.damage.apply_damage_modifiers` igual que el de un ataque
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
        try:
            from .damage import (apply_damage_modifiers, inflict_damage,
                                 parse_damage_type)
        except ImportError:  # pragma: no cover - ejecución como script suelto
            try:
                from damage import (apply_damage_modifiers, inflict_damage,
                                    parse_damage_type)
            except ImportError:
                from dnd_sim.damage import (apply_damage_modifiers,
                                            inflict_damage,
                                            parse_damage_type)
        try:
            from .combat import _tag_modificadores
        except ImportError:  # pragma: no cover - ejecución como script suelto
            try:
                from combat import _tag_modificadores
            except ImportError:
                from dnd_sim.combat import _tag_modificadores
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


def dado_por_nivel(niveles: dict, nivel: int, modificador: int = 0) -> str:
    """Dados según el nivel del slot (o del lanzador en los cantrips).

    ``niveles`` es la tabla cruda de la API (``damage_at_slot_level``,
    ``damage_at_character_level`` o ``heal_at_slot_level``). Se elige la
    clave más alta <= ``nivel``; ``MOD`` se sustituye por ``modificador``.
    """
    if not isinstance(niveles, dict) or not niveles:
        return ""
    try:
        claves = sorted(int(k) for k in niveles)
    except (TypeError, ValueError):
        return ""
    elegido = None
    for k in claves:
        if k <= nivel:
            elegido = niveles[str(k)]
    if elegido is None:
        elegido = niveles[str(claves[0])]
    texto = str(elegido).replace("MOD", str(int(modificador)))
    return texto.replace(" ", "")


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


def spell_action(spell: Spell, spellcasting: Spellcasting | None = None,
                 slot_level: int | None = None) -> CombatAction | None:
    """Construye la acción de combate de un hechizo.

    Reutiliza las acciones que ya existen: ``AttackAction`` (ataque de
    hechizo), ``SaveAction``/``AreaSaveAction`` (daño con salvación) y
    ``ConditionAction`` (condición con salvación).

    - El **tipo de acción** del hechizo (acción / acción bonus / reacción)
      se propaga al efecto interno, así que ambas capas coinciden y el
      hechizo se comprueba en su propia fase.
    - **No consume slots al construir**: el pool ``usage`` por nivel lo gasta
      el motor cuando el hechizo se lanza (``run_combat`` ->
      ``usage.spend()``).
    - ``slot_level`` prepara el **upcast**: se lanza en un slot de nivel >=
      que el del hechizo y el daño/la curación se reescalan con la tabla de
      la API. Por defecto se lanza en el nivel propio del hechizo.
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
    # Nivel de slot usado: el propio del hechizo (o su slot por defecto) o
    # el del upcast pedido.
    nivel_propio = int(spell.slot_level or spell.level or 0)
    slot = nivel_propio
    if not spell.is_cantrip and slot_level is not None:
        slot = max(nivel_propio, int(slot_level))
    # Daño y curación del hechizo, reescalados al slot si hace upcast.
    dano = spell.damage
    cura = spell.heal
    if slot != nivel_propio:
        if spell.damage_table:
            dano = dado_por_nivel(spell.damage_table, slot) or dano
        if spell.heal_table:
            cura = (dado_por_nivel(spell.heal_table, slot, sc.heal_modifier)
                    or cura)
    # El efecto interno comparte el tipo de acción del hechizo.
    tipo = spell.action_type
    efecto = None

    if spell.kind == "attack":
        rango = AttackRange.RANGED if spell.attack_type == "ranged" else AttackRange.MELEE
        atk = Attack(
            name=nombre,
            damage=dano,
            ability=sc.ability,
            proficient=True,
            attack_bonus=int(sc.attack_bonus),
            damage_bonus=0,
            damage_type=spell.damage_type,
            range_type=rango,
        )
        elementos = max(1, int(spell.elements or 1))
        if elementos == 1 and not spell.damage_options:
            efecto = AttackAction(atk, action_type=tipo, name=nombre)
        else:
            efecto = SpellAttackAction(
                spell=spell,
                attacks=[atk] * elementos,
                damage_options=list(spell.damage_options or []),
                action_type=tipo,
                name=nombre,
            )
    elif spell.kind == "save":
        eff = SaveDamage(
            ability=spell.dc_ability or "dex",
            dc=int(sc.save_dc),
            damage=dano,
            damage_type=spell.damage_type,
            on_success=spell.dc_success,
        )
        if spell.area:
            efecto = AreaSaveAction(
                name=nombre, effect=eff, targeting=AreaTargeting(),
                action_type=tipo,
            )
        else:
            efecto = SaveAction(
                name=nombre, effect=eff, action_type=tipo,
            )
    elif spell.kind == "condition":
        efecto = ConditionAction(
            name=nombre, effect=spell.condition,
            targeting=AreaTargeting(min_targets=1, max_targets=1),
            action_type=tipo,
        )
    elif spell.kind == "heal":
        efecto = HealAction(effect=HealEffect(cura), action_type=tipo,
                            name=nombre)
    elif spell.kind == "state":
        efecto = SpellStateAction(effect=spell.state, action_type=tipo,
                                  name=nombre)
    elif spell.kind == "fixed":
        efecto = SpellFixedDamageAction(
            damage=dano, damage_type=spell.damage_type,
            elements=max(1, int(spell.elements or 1)),
            action_type=tipo, name=nombre,
        )

    if efecto is None:
        return None

    return SpellAction(
        spell=spell,
        effect=efecto,
        concentration=bool(spell.concentration),
        duration_rounds=duracion_en_rondas(spell.duration),
        action_type=tipo,
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


def _contexto_de_reaccion(victim: Any, ctx: Any) -> CombatContext:
    """Contexto de combate con ``victim`` como actor (para su reacción).

    Copia las estadísticas compartidas del combate para que el lanzamiento
    cuente en los mismos contadores. Los recursos llevan la reacción ya
    marcada como usada (evita reentrancias dentro de la propia reacción).
    """
    return CombatContext(
        rng=ctx.rng,
        actor=victim,
        combatants=list(getattr(ctx, "combatants", None) or []),
        round=int(getattr(ctx, "round", 0) or 0),
        log=getattr(ctx, "log", None),
        verbose=bool(getattr(ctx, "verbose", False)),
        resources=TurnResources(reaction_used=True),
        action_uses=getattr(ctx, "action_uses", None),
        area_targets_hit=getattr(ctx, "area_targets_hit", None),
        conditions_applied=getattr(ctx, "conditions_applied", None),
        escape_attempts=getattr(ctx, "escape_attempts", None),
        escape_successes=getattr(ctx, "escape_successes", None),
        attacks_at_range=getattr(ctx, "attacks_at_range", None),
        legendary_stats=getattr(ctx, "legendary_stats", None),
    )


def trigger_reaction(victim: Any, ctx: Any) -> bool:
    """Dispara una acción de reacción de ``victim`` si acaba de recibir daño.

    Aproximación de las reglas 5e: **una reacción por turno propio**. El
    indicador ``state.reaction_used`` se pone a ``False`` al inicio del turno
    (:func:`dnd_sim.usage.begin_turn`) y se marca (antes de ejecutar) al
    usar la reacción, así que las cadenas de reacciones terminan siempre.

    Solo actúa si el combate sigue vivo (más de un bando), ``victim`` está
    vivo y puede actuar, y tiene una acción de reacción disponible; si esa
    acción tiene uso limitado, se gasta aquí (el motor de combate no la ve:
    ocurre fuera del turno de ``victim``). Devuelve True si se disparó.
    """
    if victim is None or ctx is None:
        return False
    if not getattr(victim, "alive", True):
        return False
    if not getattr(victim, "can_act", True):
        return False
    state = getattr(victim, "state", None)
    if state is not None and getattr(state, "reaction_used", False):
        return False
    combatants = list(getattr(ctx, "combatants", None) or [])
    if not combatants:
        # Contexto parcial (p. ej. riders de un ataque): no se modela.
        return False
    teams = {getattr(c, "team", None) for c in combatants
             if getattr(c, "alive", False)}
    if len(teams) <= 1:
        return False  # el combate ya está decidido: no hay reacciones.
    frescos = TurnResources()  # la reacción del victim está disponible
    candidatas = [
        a for a in getattr(victim, "actions", []) or []
        if getattr(a, "action_type", None) is ActionType.REACTION
        and a.can_use(frescos)
    ]
    if not candidatas:
        return False
    sub = _contexto_de_reaccion(victim, ctx)
    if state is not None:
        state.reaction_used = True
    elegida = pick(sub.rng, candidatas)
    log = sub.log
    if log is not None:
        log.append(f"  {getattr(victim, 'name', victim)} reacciona con "
                   f"{getattr(elegida, 'name', 'una acción de reacción')}")
    try:
        elegida.execute(sub)
    except Exception:
        return False
    usage = getattr(elegida, "usage", None)
    if usage is not None:
        usage.spend()
    acciones = getattr(ctx, "action_uses", None)
    if acciones is not None:
        nombre = getattr(elegida, "name", "") or type(elegida).__name__
        acciones[nombre] = acciones.get(nombre, 0) + 1
    return True


__all__ = [
    "Spell",
    "Spellcasting",
    "HealEffect",
    "StateEffect",
    "FULL_CASTER_SLOTS",
    "dado_por_nivel",
    "duracion_en_rondas",
    "spell_action",
    "SpellAction",
    "SpellAttackAction",
    "SpellFixedDamageAction",
    "SpellStateAction",
    "HealAction",
    "apply_concentration",
    "trigger_reaction",
]

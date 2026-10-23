"""Reglas centralizadas de ventaja/desventaja y fallos automáticos.

Este módulo es la **única fuente** donde se decide el modo de una tirada:

- Los cuatro indicadores estáticos que ya tenía ``Combatant``.
- Las condiciones de atacante y objetivo.
- Los rasgos especiales del atacante (``Combatant.traits``, véase
  :mod:`dnd_sim.traits`: Blood Frenzy...).

``resolve_roll_mode`` (en :mod:`dnd_sim.combat`) y ``saving_throw`` (en
:mod:`dnd_sim.saves`) delegan aquí.

Ninguna regla consume RNG salvo la elección de rango de un ataque "a cuerpo
a cuerpo o a distancia", y solo cuando el resultado depende de ella (el
objetivo está derribado, paralizado o inconsciente).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

try:
    from .conditions import Condition
    from .dice import RollMode
    from .randomness import pick
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from conditions import Condition
        from dice import RollMode
        from randomness import pick
    except ImportError:
        from dnd_sim.conditions import Condition
        from dnd_sim.dice import RollMode
        from dnd_sim.randomness import pick


class AttackRange(Enum):
    """Tipo de alcance de un ataque."""

    MELEE = "melee"
    RANGED = "ranged"
    MELEE_OR_RANGED = "melee or ranged"


# Bonus de CA para atacar a un objetivo que está a distancia (cobertura
# simulada). No afecta a las salvaciones.
# TODO: cobertura real (medio cuerpo, obstrucciones) y +2 a las salvaciones
# de DES por cobertura.
RANGED_COVER_AC_BONUS = 2


def effective_ac(target: Any) -> int:
    """CA efectiva de un objetivo (+2 si está a distancia)."""
    ac = int(getattr(target, "ac", 10) or 10)
    state = getattr(target, "state", None)
    if state is not None and getattr(state, "at_range", False):
        return ac + RANGED_COVER_AC_BONUS
    return ac


@dataclass
class AttackModifiers:
    """Modificadores de una tirada de ataque (reglas, no decisiones)."""

    advantage_sources: list[str] = field(default_factory=list)
    disadvantage_sources: list[str] = field(default_factory=list)
    # Crítico automático si el ataque impacta (objetivo paralizado/inconsciente).
    auto_crit_on_hit: bool = False

    @property
    def mode(self) -> RollMode:
        """Modo de la tirada: ventaja/desventaja se anulan entre sí."""
        if self.advantage_sources and self.disadvantage_sources:
            return RollMode.NORMAL
        if self.advantage_sources:
            return RollMode.ADVANTAGE
        if self.disadvantage_sources:
            return RollMode.DISADVANTAGE
        return RollMode.NORMAL

    @property
    def cancels(self) -> bool:
        """¿Hay ventaja y desventaja a la vez (se anulan)?"""
        return bool(self.advantage_sources and self.disadvantage_sources)

    def reason(self) -> str:
        """Motivo legible para el log."""
        if self.cancels:
            return "ventaja y desventaja se anulan"
        fuentes = self.advantage_sources or self.disadvantage_sources
        return ", ".join(fuentes)


@dataclass
class SaveModifiers:
    """Modificadores de una tirada de salvación."""

    auto_fail: bool = False
    advantage_sources: list[str] = field(default_factory=list)
    disadvantage_sources: list[str] = field(default_factory=list)

    @property
    def mode(self) -> RollMode:
        if self.advantage_sources and self.disadvantage_sources:
            return RollMode.NORMAL
        if self.advantage_sources:
            return RollMode.ADVANTAGE
        if self.disadvantage_sources:
            return RollMode.DISADVANTAGE
        return RollMode.NORMAL


@dataclass
class CheckModifiers:
    """Modificadores de una prueba de característica."""

    advantage_sources: list[str] = field(default_factory=list)
    disadvantage_sources: list[str] = field(default_factory=list)

    @property
    def mode(self) -> RollMode:
        if self.advantage_sources and self.disadvantage_sources:
            return RollMode.NORMAL
        if self.advantage_sources:
            return RollMode.ADVANTAGE
        if self.disadvantage_sources:
            return RollMode.DISADVANTAGE
        return RollMode.NORMAL


def _condiciones(combatant: Any) -> set:
    """Condiciones activas de un combatiente (conjunto vacío si no tiene)."""
    tracker = getattr(combatant, "conditions", None)
    if tracker is None:
        return set()
    try:
        return set(tracker.active())
    except Exception:
        return set()


def resolve_attack_range(attack: Any, rng: Any) -> AttackRange:
    """Rango efectivo del ataque.

    ``MELEE_OR_RANGED`` (arma cuerpo a cuerpo o a distancia) se decide
    **siempre** con ``pick`` en cada ataque: el modo define tanto la
    ventaja/desventaja como si el atacante queda a distancia. **Consume RNG
    en cada uno de esos ataques.**
    """
    rango = getattr(attack, "range_type", AttackRange.MELEE)
    if rango is AttackRange.MELEE_OR_RANGED:
        if rng is None:
            return AttackRange.MELEE
        return pick(rng, [AttackRange.MELEE, AttackRange.RANGED])
    return rango


def attack_modifiers(attacker: Any, target: Any, attack: Any,
                     rango: Any = None) -> AttackModifiers:
    """Reúne los modificadores de la tirada de ataque de ``attacker``.

    ``rango`` es el rango ya resuelto (:func:`resolve_attack_range`): si no
    se pasa, se usa el del ataque (sin decidir "cuerpo a cuerpo o a
    distancia").
    """
    mods = AttackModifiers()
    cond_atacante = _condiciones(attacker)
    cond_objetivo = _condiciones(target)
    if not isinstance(rango, AttackRange):
        # Rango no resuelto (None o un valor ajeno, p. ej. el rng que
        # resolve_roll_mode pasaba por compatibilidad): se usa el del ataque.
        rango = getattr(attack, "range_type", AttackRange.MELEE)

    # 1. Indicadores estáticos (efecto fijo).
    if getattr(attacker, "attacks_with_advantage", False):
        mods.advantage_sources.append("efecto fijo")
    if getattr(attacker, "attacks_with_disadvantage", False):
        mods.disadvantage_sources.append("efecto fijo")
    if getattr(target, "grants_advantage_to_attackers", False):
        mods.advantage_sources.append("efecto fijo del objetivo")
    if getattr(target, "grants_disadvantage_to_attackers", False):
        mods.disadvantage_sources.append("efecto fijo del objetivo")

    # 2. Hechizo verdadero: ventaja en los ataques mientras dure.
    if Condition.TRUE_STRUCK in cond_atacante:
        mods.advantage_sources.append("hechizo verdadero")

    # 3. Condiciones del atacante: desventaja en sus ataques.
    if Condition.BLINDED in cond_atacante:
        mods.disadvantage_sources.append("atacante cegado")
    if Condition.FRIGHTENED in cond_atacante:
        # TODO: línea de visión (se asume que la fuente está a la vista).
        mods.disadvantage_sources.append("atacante aterrorizado")
    if Condition.POISONED in cond_atacante:
        mods.disadvantage_sources.append("atacante envenenado")
    if Condition.PRONE in cond_atacante:
        mods.disadvantage_sources.append("atacante derribado")
    if Condition.RESTRAINED in cond_atacante:
        mods.disadvantage_sources.append("atacante inmovilizado")
    if Condition.INVISIBLE in cond_atacante:
        # «An invisible creature has advantage on attack rolls against
        # creatures that can't see it». Este ataque **sí** se resuelve con
        # ventaja: en attack_roll la invisibilidad se quita después de
        # calcular los modificadores (romperla es consecuencia de atacar).
        mods.advantage_sources.append("atacante invisible")

    # 4. Condiciones del objetivo.
    if Condition.BLINDED in cond_objetivo:
        mods.advantage_sources.append("objetivo cegado")
    if Condition.INVISIBLE in cond_objetivo:
        # Adaptación al simulador: invisible = desventaja al ser atacado.
        # (La ventaja del propio invisible al atacar va en el bloque 3.)
        mods.disadvantage_sources.append("objetivo invisible")
    if Condition.MARKED in cond_objetivo:
        mods.advantage_sources.append("objetivo señalado")
    if Condition.RESTRAINED in cond_objetivo:
        mods.advantage_sources.append("objetivo inmovilizado")
    if Condition.STUNNED in cond_objetivo:
        mods.advantage_sources.append("objetivo aturdido")
    if Condition.PARALYZED in cond_objetivo:
        mods.advantage_sources.append("objetivo paralizado")
    if Condition.UNCONSCIOUS in cond_objetivo:
        mods.advantage_sources.append("objetivo inconsciente")
    if Condition.PETRIFIED in cond_objetivo:
        mods.advantage_sources.append("objetivo petrificado")
    if Condition.PRONE in cond_objetivo:
        if rango is AttackRange.RANGED:
            mods.disadvantage_sources.append("objetivo derribado, a distancia")
        else:
            mods.advantage_sources.append("objetivo derribado, cuerpo a cuerpo")

    # 5. Rasgos especiales del atacante (p. ej. Blood Frenzy del sahuagin):
    #    cada rasgo decide por sí mismo si aplica (rango, objetivo herido...).
    for rasgo in getattr(attacker, "traits", []) or []:
        hook = getattr(rasgo, "modify_attack_modifiers", None)
        if hook is not None:
            hook(mods, attacker, target, rango)

    # 6. Crítico automático: contra un objetivo paralizado o inconsciente,
    #    todo ataque cuerpo a cuerpo que impacte es crítico.
    if rango is AttackRange.MELEE and (Condition.PARALYZED in cond_objetivo
                                       or Condition.UNCONSCIOUS in cond_objetivo):
        mods.auto_crit_on_hit = True

    return mods


def save_modifiers(target: Any, ability: str) -> SaveModifiers:
    """Reúne los modificadores de una tirada de salvación del objetivo."""
    mods = SaveModifiers()
    cond = _condiciones(target)

    # Fallo automático: aturdido/paralizado/inconsciente/petrificado fallan
    # siempre las salvaciones de FUE y DES.
    if (Condition.STUNNED in cond or Condition.PARALYZED in cond
            or Condition.UNCONSCIOUS in cond or Condition.PETRIFIED in cond):
        if str(ability).strip().lower() in ("str", "strength", "dex", "dexterity"):
            mods.auto_fail = True

    # Indicadores estáticos.
    ventaja = getattr(target, "saves_with_advantage", set()) or set()
    desventaja = getattr(target, "saves_with_disadvantage", set()) or set()
    if ability in ventaja:
        mods.advantage_sources.append("efecto fijo")
    if ability in desventaja:
        mods.disadvantage_sources.append("efecto fijo")
    if Condition.RESTRAINED in cond and str(ability).strip().lower() in ("dex", "dexterity"):
        mods.disadvantage_sources.append("inmovilizado")
    # Agrandado (Enlarge del duergar / hechizo Enlarge): ventaja en FUE.
    if (Condition.ENLARGED in cond
            and str(ability).strip().lower() in ("str", "strength")):
        mods.advantage_sources.append("agrandado")

    return mods


def check_modifiers(target: Any, ability: str) -> CheckModifiers:
    """Modificadores de una prueba de característica.

    - POISONED y FRIGHTENED dan desventaja en toda prueba.
      (FRIGHTENED mantiene la suposición de que la fuente está siempre a
      la vista.)
    - ENLARGED da ventaja en las pruebas de Fuerza.
    - Indicadores estáticos ``checks_with_advantage/disadvantage``.
    """
    mods = CheckModifiers()
    cond = _condiciones(target)

    if Condition.POISONED in cond:
        mods.disadvantage_sources.append("envenenado")
    if Condition.FRIGHTENED in cond:
        # TODO: línea de visión (se asume que la fuente está a la vista).
        mods.disadvantage_sources.append("aterrorizado")
    if (Condition.ENLARGED in cond
            and str(ability).strip().lower() in ("str", "strength")):
        mods.advantage_sources.append("agrandado")

    ventaja = getattr(target, "checks_with_advantage", set()) or set()
    desventaja = getattr(target, "checks_with_disadvantage", set()) or set()
    if ability in ventaja:
        mods.advantage_sources.append("efecto fijo")
    if ability in desventaja:
        mods.disadvantage_sources.append("efecto fijo")

    return mods


__all__ = ["AttackRange", "AttackModifiers", "SaveModifiers", "CheckModifiers",
           "attack_modifiers", "save_modifiers", "check_modifiers",
           "resolve_attack_range", "effective_ac", "RANGED_COVER_AC_BONUS"]

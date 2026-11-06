"""Reglas centralizadas de ventaja/desventaja y fallos automáticos.

Este módulo es la **única fuente** donde se decide el modo de una tirada:

- Los cuatro indicadores estáticos que ya tenía ``Combatant``.
- Las condiciones de atacante y objetivo.
- Los rasgos especiales del atacante (``Combatant.traits``, véase
  :mod:`dnd_sim.rules.traits`: Blood Frenzy...).

``resolve_roll_mode`` (en :mod:`dnd_sim.engine.combat`) y ``saving_throw`` (en
:mod:`dnd_sim.rules.saves`) delegan aquí.

Ninguna regla consume RNG salvo en dos casos, ambos documentados:

- la elección de rango de un ataque "a cuerpo a cuerpo o a distancia" (es
  decir, un arma ``MELEE_OR_RANGED``), y solo cuando el resultado depende
  de ella (el objetivo está derribado, paralizado o inconsciente);
- los rasgos con condición de **posición** (Pack Tactics, Martial
  Advantage), que sortean su resultado **solo** si el atacante tiene
  aliados y la llamada llega con ``ctx`` y ``rng``: una llamada directa
  sin contexto no consume nada.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .conditions import Condition
from ..core.enums import AttackRange  # noqa: F401  (reexport)
from ..core.dice import RollMode
from ..core.randomness import pick


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
    # Bonificador plano a la tirada (p. ej. Archery: +2 a distancia).
    bonus: int = 0

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
    # Suelo del total (Indomitable Might, nivel 18): si la tirada sale
    # más baja, se usa este valor. ``None`` = sin suelo.
    minimum_total: int | None = None

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
    # Suelo del total (Indomitable Might, nivel 18); ver SaveModifiers.
    minimum_total: int | None = None
    # Característica con la que se tira en lugar de la asociada a la
    # habilidad (Primal Knowledge: tirar Sigilo como FUE con Furia).
    ability_override: str | None = None

    @property
    def mode(self) -> RollMode:
        if self.advantage_sources and self.disadvantage_sources:
            return RollMode.NORMAL
        if self.advantage_sources:
            return RollMode.ADVANTAGE
        if self.disadvantage_sources:
            return RollMode.DISADVANTAGE
        return RollMode.NORMAL


def _hooks(traits: Any, nombre: str) -> list:
    """Rasgos que sobrescriben ``nombre`` (import perezoso: evita el ciclo
    ``roll_modifiers`` -> ``traits``, que importa AttackRange de aquí)."""
    from .traits import hooks
    return hooks(traits, nombre)


def _condiciones(combatant: Any) -> set:
    """Condiciones activas de un combatiente (conjunto vacío si no tiene)."""
    tracker = getattr(combatant, "conditions", None)
    if tracker is None:
        return set()
    try:
        return set(tracker.active())
    except Exception:
        return set()


def _instancias(combatant: Any, condition: Any) -> list:
    """Instancias concretas de ``condition`` en un combatiente (vacío si no).

    A diferencia de :func:`_condiciones` (que devuelve el conjunto de tipos
    activos), conserva cada instancia con su ``source``: la regla de
    Agarrado necesita saber QUIÉN agarra.
    """
    tracker = getattr(combatant, "conditions", None)
    if tracker is None:
        return []
    return [inst for inst in getattr(tracker, "instances", []) or []
            if inst.condition is condition]


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
                     rango: Any = None, *, ctx: Any = None,
                     rng: Any = None) -> AttackModifiers:
    """Reúne los modificadores de la tirada de ataque de ``attacker``.

    ``rango`` es el rango ya resuelto (:func:`resolve_attack_range`): si no
    se pasa, se usa el del ataque (sin decidir "cuerpo a cuerpo o a
    distancia").

    ``ctx`` y ``rng`` solo los usan los rasgos cuya condición no se puede
    comprobar (Pack Tactics): sin ellos esos rasgos no aplican y, muy
    importante, **no consumen RNG**, así que llamar a esta función sin
    contexto (como hacen las pruebas directas) no altera ninguna tirada.
    """
    mods = AttackModifiers()
    cond_atacante = _condiciones(attacker)
    cond_objetivo = _condiciones(target)
    if rng is None and ctx is not None:
        rng = getattr(ctx, "rng", None)
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

    # 1b. Marcas de defensor (p. ej. Protectores Ancestrales): quien está
    # marcado tiene desventaja salvo al atacar contra su marcador. El
    # estado lo lleva el marcado (``state.marked_by``) y lo limpia el
    # rasgo del marcador cuando el efecto termina.
    marcador = getattr(getattr(attacker, "state", None), "marked_by", None)
    if marcador is not None and target is not marcador:
        mods.disadvantage_sources.append("marca del defensor")

    # 2. Condiciones del atacante: desventaja en sus ataques.
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

    # 2b. Agarrado (PHB 2024): quien está agarrado ataca con desventaja
    # salvo contra la criatura que lo agarra (la instancia con ``source``).
    if Condition.GRAPPLED in cond_atacante and target is not None:
        agarradores = [inst.source for inst in
                       _instancias(attacker, Condition.GRAPPLED)
                       if inst.source is not None]
        if agarradores and all(target is not a for a in agarradores):
            mods.disadvantage_sources.append("atacante agarrado")

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
    # 4b. Esquivar: mientras el objetivo esquiva, sus atacantes tienen
    # desventaja (la esquiva se pierde al quedar incapacitado y
    # ``begin_turn`` la limpia al empezar su propio turno).
    if (getattr(getattr(target, "state", None), "dodging", False)
            and Condition.INCAPACITATED not in cond_objetivo):
        mods.disadvantage_sources.append("Esquivar")

    # 5. Rasgos especiales del atacante (Blood Frenzy, Pack Tactics...):
    #    cada rasgo decide por sí mismo si aplica (rango, objetivo herido,
    #    aliados cerca...). Solo los que sobrescriben el hook
    #    (traits.hooks). Reciben el contexto y el RNG por si su condición
    #    no es comprobable.
    traits_atacante = getattr(attacker, "traits", None)
    if traits_atacante:
        for rasgo in _hooks(traits_atacante, "modify_attack_modifiers"):
            rasgo.modify_attack_modifiers(mods, attacker, target, rango,
                                          ctx=ctx, rng=rng, atk=attack)

    # 5b. Rasgos de OTROS que grantan ventaja/desventaja a este ataque
    #     (p. ej. Lobo/León del Corazón Salvaje): mismo patrón que
    #     reduce_damage_to_allies en rules/damage — se recorren los
    #     combatientes del contexto y el atacante se salta (ya corrió
    #     en el bloque 5). Si ningún rasgo sobrescribe el hook no se
    #     consume RNG.
    if ctx is not None:
        for otro in getattr(ctx, "combatants", None) or []:
            if otro is attacker:
                continue
            traits_otro = getattr(otro, "traits", None)
            if not traits_otro:
                continue
            for rasgo in _hooks(traits_otro, "grant_attack_modifiers"):
                rasgo.grant_attack_modifiers(mods, attacker, target, rango,
                                             ctx=ctx, rng=rng, atk=attack)

    # 5c. Marcas de maestría (Vex/Sap) pendientes contra este objetivo:
    #     se consumen al concederse y sin marcas no se toca nada.
    if attack is not None:
        from .mastery import consumir_marcas
        consumir_marcas(mods, attacker, target, ctx)

    # 6. Crítico automático: contra un objetivo paralizado o inconsciente,
    #    todo ataque cuerpo a cuerpo que impacte es crítico.
    if rango is AttackRange.MELEE and (Condition.PARALYZED in cond_objetivo
                                       or Condition.UNCONSCIOUS in cond_objetivo):
        mods.auto_crit_on_hit = True

    return mods


def save_modifiers(target: Any, ability: str,
                   kind: str | None = None, *,
                   magical: bool = False,
                   ctx: Any = None) -> SaveModifiers:
    """Reúne los modificadores de una tirada de salvación del objetivo.

    Además de condiciones e indicadores estáticos, consulta los hooks
    ``modify_save_modifiers`` de los rasgos del objetivo
    (:mod:`dnd_sim.rules.traits`) y, si llega ``ctx``, los hooks
    ``grant_save_modifiers`` de los rasgos del **resto** de combatientes
    (p. ej. Zealous Presence: ventaja a aliados; el propio objetivo se
    salta). Sin ``ctx`` no se consulta a nadie (cero coste y cero RNG).

    ``kind`` identifica el tipo de efecto que provoca la salvación cuando
    quien la tira lo sabe (``"turn"`` = un efecto que convierte
    no-muertos); hoy solo lo usa Turn Resistance y todavía no lo pasa
    nadie (# TODO: Turn Undead).

    ``magical`` dice que la salvación la proviene de un efecto mágico
    (hechizo): con él, el rasgo ``magic_resistance`` del objetivo (la
    ventaja de la Resistencia mágica) se suma como fuente de ventaja.
    """
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
    # Esquivar: ventaja en salvaciones de Destreza mientras dure (mismo
    # criterio de incapacidad que en los ataques).
    if (str(ability).strip().lower() in ("dex", "dexterity")
            and getattr(getattr(target, "state", None), "dodging", False)
            and Condition.INCAPACITATED not in cond):
        mods.advantage_sources.append("Esquivar")

    # Rasgos especiales (Turn Resistance): cada rasgo decide por sí mismo si
    # aplica, según el tipo de efecto (``kind``) que provoca la salvación.
    # Solo los que sobrescriben el hook.
    traits = getattr(target, "traits", None)
    if traits:
        for rasgo in _hooks(traits, "modify_save_modifiers"):
            rasgo.modify_save_modifiers(mods, target, ability, kind)

    # Rasgos de OTROS que grantan ventaja/desventaja a esta salvación
    # (p. ej. Zealous Presence): mismo patrón que el bloque 5b de
    # attack_modifiers; el propio objetivo se salta (su trait ya corrió
    # en el bloque anterior). Si ningún rasgo sobrescribe el hook no se
    # consume RNG.
    if ctx is not None:
        for otro in getattr(ctx, "combatants", None) or []:
            if otro is target:
                continue
            traits_otro = getattr(otro, "traits", None)
            if not traits_otro:
                continue
            for rasgo in _hooks(traits_otro, "grant_save_modifiers"):
                rasgo.grant_save_modifiers(mods, target, ability, kind,
                                           ctx=ctx)

    # Resistencia mágica: ventaja solo si la salvación proviene de un
    # efecto mágico (``magical=True``) y el objetivo tiene el rasgo. Va
    # tras los hooks para que cualquier fuente existente conserve su
    # posición en la lista; ventaja y desventaja se siguen anulando en
    # el modo resuelto.
    if magical and getattr(target, "magic_resistance", False):
        mods.advantage_sources.append("Resistencia mágica")

    return mods


def check_modifiers(target: Any, ability: str,
                    skill: str | None = None) -> CheckModifiers:
    """Modificadores de una prueba de característica.

    - POISONED y FRIGHTENED dan desventaja en toda prueba.
      (FRIGHTENED mantiene la suposición de que la fuente está siempre a
      la vista.)
    - ENLARGED da ventaja en las pruebas de Fuerza.
    - Indicadores estáticos ``checks_with_advantage/disadvantage``.
    - Hooks ``modify_check_modifiers`` de los rasgos del objetivo
      (:mod:`dnd_sim.rules.traits`), con ``skill`` cuando la prueba es de
      habilidad (``"perception"``) o ``None`` en una prueba pura de
      característica.
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

    # Rasgos especiales (p. ej. Keen Senses): cada rasgo decide por sí mismo
    # si aplica. Solo los que sobrescriben el hook.
    traits = getattr(target, "traits", None)
    if traits:
        for rasgo in _hooks(traits, "modify_check_modifiers"):
            rasgo.modify_check_modifiers(mods, target, ability, skill=skill)

    return mods


__all__ = ["AttackRange", "AttackModifiers", "SaveModifiers", "CheckModifiers",
           "attack_modifiers", "save_modifiers", "check_modifiers",
           "resolve_attack_range", "effective_ac", "RANGED_COVER_AC_BONUS"]

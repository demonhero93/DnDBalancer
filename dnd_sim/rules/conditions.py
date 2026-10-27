"""Condiciones de D&D 5e: estado, duración e implicaciones.

Catálogo cerrado de condiciones (las que afectan a tiradas, acciones y daño).
El estado vive en :class:`ConditionTracker` (uno por combatiente); las reglas
de tiradas viven en :mod:`dnd_sim.rules.roll_modifiers`.

Ninguna mecánica de este módulo consume RNG por sí sola: solo las
salvaciones de repetición del final de turno (y solo si existen).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

from ..model.actions import ActionType, CombatAction, actor_is_alive
from ..core.targeting import valid_targets

if TYPE_CHECKING:
    from ..model.combatant import Combatant


class Condition(Enum):
    """Condiciones modeladas (catálogo cerrado)."""

    BLINDED = "blinded"
    # Hechizado: mientras lo esté, sus objetivos se invierten (ataca a los
    # de su propio bando).
    CHARMED = "charmed"
    # Concentración: solo se puede mantener una concentración por lanzador
    # (lanzar otro hechizo concentrado termina la anterior).
    CONCENTRATION = "concentration"
    # Agrandado: ventaja en pruebas y salvaciones de Fuerza (Enlarge del
    # duergar y el hechizo Enlarge/Reduce); el daño crece según la fuente.
    ENLARGED = "enlarged"
    FRIGHTENED = "frightened"
    # Guiado: +1d4 a una prueba de característica (PHB 2024: no se consume
    # al usarla, dura lo que el hechizo).
    GUIDED = "guided"
    # Señalado: el objetivo otorga ventaja a quien lo ataque (Luz de hadas,
    # Rayo guía).
    MARKED = "marked"
    INCAPACITATED = "incapacitated"
    # Invisible: adaptación al simulador, desventaja al ser atacado (el
    # invisible no se ve; su ventaja propia al atacar aún no se modela).
    INVISIBLE = "invisible"
    PARALYZED = "paralyzed"
    PETRIFIED = "petrified"
    POISONED = "poisoned"
    PRONE = "prone"
    RESTRAINED = "restrained"
    STUNNED = "stunned"
    UNCONSCIOUS = "unconscious"
    # Marca del cazador (PHB 2024): el **portador** inflige +1d6 Fuerza
    # con sus ataques (véase CONDITION_ATTACK_DAMAGE).
    HUNTERS_MARK = "hunters_mark"
    # Favor divino (PHB 2024): el **portador** inflige +1d4 Radiante.
    DIVINE_FAVOR = "divine_favor"


# Condiciones que NO se modelan, con el motivo (no son miembros del Enum).
EXCLUDED_CONDITIONS: dict[str, str] = {
    "deafened": "sentidos: no se modelan (no afectan a tiradas).",
    "grappled": "no da ventaja ni desventaja por sí sola.",
    "exhausted": "el agotamiento depende de la edición de reglas.",
}

# Condiciones que implican otras (5e): STUNNED/PARALYZED/PETRIFIED/UNCONSCIOUS
# incapacitan y UNCONSCIOUS además derriba.
IMPLIED_CONDITIONS: dict[Condition, tuple[Condition, ...]] = {
    Condition.STUNNED: (Condition.INCAPACITATED,),
    Condition.PARALYZED: (Condition.INCAPACITATED,),
    Condition.PETRIFIED: (Condition.INCAPACITATED,),
    Condition.UNCONSCIOUS: (Condition.INCAPACITATED, Condition.PRONE),
}

# Etiquetas en español para el log.
CONDITION_LABELS: dict[Condition, str] = {
    Condition.BLINDED: "cegado",
    Condition.CHARMED: "hechizado",
    Condition.CONCENTRATION: "concentrado",
    Condition.ENLARGED: "agrandado",
    Condition.FRIGHTENED: "aterrorizado",
    Condition.GUIDED: "guiado",
    Condition.INCAPACITATED: "incapacitado",
    Condition.INVISIBLE: "invisible",
    Condition.MARKED: "señalado",
    Condition.PARALYZED: "paralizado",
    Condition.PETRIFIED: "petrificado",
    Condition.POISONED: "envenenado",
    Condition.PRONE: "derribado",
    Condition.RESTRAINED: "inmovilizado",
    Condition.STUNNED: "aturdido",
    Condition.UNCONSCIOUS: "inconsciente",
    Condition.HUNTERS_MARK: "marcado por la caza",
    Condition.DIVINE_FAVOR: "bendecido",
}


# Daño extra que el **portador** de una condición inflige con sus ataques
# (PHB 2024): Marca del cazador (+1d6 Fuerza) y Favor divino (+1d4
# Radiante). Simplificación: se suma a todo acierto del portador (no solo
# al objetivo concreto que esté marcado). Véase el impacto en
# ``dnd_sim.engine.combat.attack_roll``.
CONDITION_ATTACK_DAMAGE: dict[Condition, tuple[str, Any]] = {
    Condition.HUNTERS_MARK: ("1d6", "force"),
    Condition.DIVINE_FAVOR: ("1d4", "radiant"),
}


@dataclass
class RepeatSave:
    """Salvación que el afectado puede repetir al final de cada turno suyo.

    ``escalate_to``/``escalate_rounds`` modelan el escalado del Sleep 2024:
    si la repetición falla, la condición «evoluciona» a otra más grave
    (Incapacitado → Inconsciente) durante la duración indicada.
    """

    ability: str
    dc: int
    escalate_to: Any = None      # Condition a la que escala al fallar
    escalate_rounds: int | None = None


@dataclass
class EscapeCheck:
    """Prueba de característica para liberarse de un estado.

    ``abilities``: características posibles (si hay más de una, se elige una
    al azar al intentar escapar). ``consumes_action``: la prueba gasta la
    acción del afectado (como "As an action" en las fichas).
    """

    abilities: tuple[str, ...] = ("str",)
    dc: int = 10
    consumes_action: bool = False


@dataclass
class ConditionInstance:
    """Una aplicación de una condición (una instancia por fuente)."""

    condition: Condition
    source: Any = None
    # Rondas que le quedan de duración (None = hasta el fin del combate).
    remaining_rounds: int | None = None
    repeat_save: RepeatSave | None = None
    # Prueba de escape (si la hay).
    escape: EscapeCheck | None = None
    # ¿Termina al atacar o al lanzar un hechizo? Es el caso de la
    # invisibilidad estándar («until it attacks or casts a spell»); la
    # Superior Invisibility de la pixie, que dura lo que su concentración,
    # se aplica con False y por eso sobrevive a un ataque.
    break_on_attack: bool = True


@dataclass
class ConditionTracker:
    """Estado de condiciones de un combatiente.

    Una misma condición puede tener varias instancias (cada fuente con su
    duración y su salvación de repetición): la condición sigue activa
    mientras quede al menos una instancia.
    """

    instances: list[ConditionInstance] = field(default_factory=list)

    def active(self) -> set[Condition]:
        """Condiciones activas, incluyendo las implicadas."""
        active = {inst.condition for inst in self.instances}
        for condition in list(active):
            active.update(IMPLIED_CONDITIONS.get(condition, ()))
        return active

    def has(self, condition: Condition) -> bool:
        """¿Está activa la condición (directa o implicada)?"""
        return condition in self.active()

    def add(self, instance: ConditionInstance) -> ConditionInstance:
        self.instances.append(instance)
        return instance

    def remove_instance(self, instance: ConditionInstance) -> None:
        """Elimina una instancia concreta (si sigue en la lista)."""
        for pos, current in enumerate(self.instances):
            if current is instance:
                del self.instances[pos]
                return

    def clear(self) -> None:
        self.instances.clear()


@dataclass
class ConditionEffect:
    """Efecto de una acción: deja una condición si el objetivo falla la
    salvación.

    ``save_ability=None`` significa que la condición se aplica
    automáticamente al impactar el ataque (sin salvación). Solo se permite
    si hay ``escape`` (una salida): si no, el estado sería permanente.
    """

    condition: Condition
    save_ability: str | None = None
    dc: int = 0
    duration_rounds: int | None = None
    repeat_save: bool = False
    on_success: str = "none"
    escape: EscapeCheck | None = None
    # Escalado al fallar la repetición (Sleep 2024): véase RepeatSave.
    escalate_to: Any = None
    escalate_rounds: int | None = None

    def __post_init__(self) -> None:
        if self.save_ability is None and self.escape is None:
            raise ValueError(
                f"La condición {self.condition.value!r} necesita una salvación o "
                f"una prueba de escape: si no, el estado no tendría salida."
            )


from ..core.log import log_line as _log_line


def _label(condition: Condition) -> str:
    return CONDITION_LABELS.get(condition, condition.value)


def _as_condition(condition: Any) -> Condition:
    """Normaliza a ``Condition``; lanza ValueError si no está en el Enum."""
    if isinstance(condition, Condition):
        return condition
    if isinstance(condition, str):
        try:
            return Condition(condition.strip().lower())
        except ValueError:
            pass
    raise ValueError(f"Condición desconocida: {condition!r}")


def apply_condition(target: Any, condition: Any, ctx: Any, *,
                    source: Any = None, duration_rounds: int | None = None,
                    repeat_save: RepeatSave | None = None,
                    escape: EscapeCheck | None = None,
                    break_on_attack: bool = True) -> ConditionInstance:
    """Aplica una condición a un objetivo y la registra en el log.

    Si el objetivo ya tiene esa condición, se añade otra instancia (cada
    fuente conserva su duración, su salvación de repetición, su escape y si
    termina al atacar).
    """
    condition = _as_condition(condition)
    tracker = getattr(target, "conditions", None)
    if tracker is None:
        raise ValueError(f"{getattr(target, 'name', target)} no tiene registro de condiciones.")

    instance = ConditionInstance(
        condition=condition,
        source=source,
        remaining_rounds=duration_rounds,
        repeat_save=repeat_save,
        escape=escape,
        break_on_attack=bool(break_on_attack),
    )
    tracker.add(instance)

    nombre = getattr(target, "name", target)
    if duration_rounds is None:
        duracion = ""
    elif duration_rounds == 1:
        duracion = " (1 ronda)"
    else:
        duracion = f" ({duration_rounds} rondas)"
    _log_line(ctx, f"{nombre} queda {_label(condition)}{duracion}")

    # Estadísticas: veces que se aplicó cada condición.
    conteo = getattr(ctx, "conditions_applied", None)
    if conteo is not None:
        try:
            conteo[condition.value] = conteo.get(condition.value, 0) + 1
        except Exception:
            pass
    return instance


def remove_condition(target: Any, condition: Any, ctx: Any = None) -> bool:
    """Elimina todas las instancias activas de una condición.

    Devuelve True si había alguna. Para la invisibilidad, que termina por
    un evento y no por el tiempo («until it attacks»), la rutina concreta es
    :func:`remove_invisibility_on_action`, que además distingue la que se
    rompe de la que no.
    """
    condition = _as_condition(condition)
    tracker = getattr(target, "conditions", None)
    if tracker is None:
        return False
    quitadas = False
    for instance in list(tracker.instances):
        if instance.condition is condition:
            tracker.remove_instance(instance)
            quitadas = True
    if quitadas:
        _log_line(ctx, f"{getattr(target, 'name', target)} deja de estar "
                       f"{_label(condition)}")
    return quitadas


def remove_invisibility_on_action(target: Any) -> bool:
    """Termina la invisibilidad **estándar** al atacar o al lanzar.

    Quita solo las instancias con ``break_on_attack=True``, que es la
    regla de la invisibilidad normal («[Invisibility] ends if the target
    attacks or casts a spell»). La Superior Invisibility de la pixie, que
    dura lo que su concentración, se aplica con ``False`` y por eso aquí no
    se toca.

    Devuelve True si se quitó alguna; no registra nada en el log: quien
    llama añade la línea con su motivo («(ataca)» en
    :func:`dnd_sim.engine.combat.attack_roll`, «(lanza un hechizo)» en
    ``_romper_invisibilidad_al_lanzar``), como ya hacía con
    :func:`remove_condition`.
    """
    tracker = getattr(target, "conditions", None)
    if tracker is None:
        return False
    quitadas = False
    for instance in list(tracker.instances):
        if instance.condition is Condition.INVISIBLE and instance.break_on_attack:
            tracker.remove_instance(instance)
            quitadas = True
    return quitadas


def _queda_accion(actor: Any, ctx: Any) -> bool:
    """¿Le queda acción al actor en este turno?"""
    resources = getattr(ctx, "resources", None)
    if resources is None:
        return False
    try:
        return bool(resources.can_use(ActionType.ACTION))
    except Exception:
        return False


def attempt_escapes(actor: Any, ctx: Any) -> None:
    """Intenta liberarse de los estados con prueba de escape.

    Se llama al INICIO del turno del afectado (no es una elección, es
    automático):

    1. Si el actor está incapacitado, no intenta nada (ni consume RNG): los
       estados que incapacitan se liberan con ``repeat_save`` o por
       duración.
    2. Recorre las instancias con ``escape`` en orden de aplicación. Si la
       prueba consume acción y el actor ya gastó su acción, se salta.
    3. Elige la característica (uniforme entre las posibles), tira la
       prueba y, si tiene éxito, elimina la instancia. Si la prueba
       consumía acción, la gasta acierte o falle.

    Orden del RNG: (característica elegida, si hay varias) y prueba, por
    instancia y en orden.
    """
    tracker = getattr(actor, "conditions", None)
    if tracker is None or not tracker.instances:
        return
    if not getattr(actor, "can_act", True):
        return  # incapacitado: no intenta escapar

    from .checks import ability_check
    from ..core.randomness import pick

    rng = getattr(ctx, "rng", None)
    nombre = getattr(actor, "name", actor)

    for instance in list(tracker.instances):
        escape = getattr(instance, "escape", None)
        if escape is None:
            continue
        if escape.consumes_action and not _queda_accion(actor, ctx):
            continue
        habilidades = list(escape.abilities) or ["str"]
        if len(habilidades) == 1:
            habilidad = habilidades[0]
        else:
            habilidad = pick(rng, habilidades)
        resultado = ability_check(actor, habilidad, escape.dc, rng)
        etiqueta = _label(instance.condition)
        # Estadísticas: intentos y éxitos por condición.
        _contar(ctx, "escape_attempts", instance.condition.value)
        if resultado.success:
            _contar(ctx, "escape_successes", instance.condition.value)
            tracker.remove_instance(instance)
            _log_line(ctx, f"{nombre} se libera de {etiqueta} "
                           f"(prueba {habilidad.upper()} {resultado.total} vs CD {escape.dc})")
        else:
            _log_line(ctx, f"{nombre} no logra liberarse de {etiqueta} "
                           f"(prueba {habilidad.upper()} {resultado.total} vs CD {escape.dc})")
        if escape.consumes_action:
            resources = getattr(ctx, "resources", None)
            if resources is not None:
                resources.use(ActionType.ACTION)


def _contar(ctx: Any, atributo: str, nombre: str) -> None:
    """Suma uno en el diccionario de estadísticas indicado del contexto."""
    conteo = getattr(ctx, atributo, None)
    if conteo is None:
        return
    try:
        conteo[nombre] = conteo.get(nombre, 0) + 1
    except Exception:
        pass


def end_turn(actor: Any, ctx: Any) -> None:
    """Final del turno de un combatiente vivo.

    Para cada instancia de sus condiciones, en el orden en que se añadieron:
    1. Si tiene salvación de repetición, se tira; si tiene éxito, la
       instancia se elimina.
    2. Si sigue y tiene duración finita, se reduce en 1; al llegar a 0 se
       elimina.

    Orden del RNG: las salvaciones de repetición se tiran en el orden de las
    instancias y solo si existen.
    """
    tracker = getattr(actor, "conditions", None)
    if tracker is None or not tracker.instances:
        return
    nombre = getattr(actor, "name", actor)

    for instance in list(tracker.instances):
        # 1. Salvación de repetición.
        if instance.repeat_save is not None:
            from .saves import registrar_resistencia, saving_throw
            sr = saving_throw(actor, instance.repeat_save.ability,
                              instance.repeat_save.dc, ctx.rng)
            sr = registrar_resistencia(ctx, actor, sr)
            habilidad = instance.repeat_save.ability.upper()
            if sr.success:
                tracker.remove_instance(instance)
                _log_line(ctx, f"{nombre} supera la salvación de {habilidad} "
                               f"({sr.total} vs CD {sr.dc}): termina {_label(instance.condition)}")
                continue
            _log_line(ctx, f"{nombre} falla la salvación de {habilidad} "
                           f"({sr.total} vs CD {sr.dc}): mantiene {_label(instance.condition)}")
            # Escalado (Sleep 2024): al fallar la repetición, la condición
            # pasa a ser otra más grave por el resto de la duración y sin
            # repetición adicional.
            escalada = getattr(instance.repeat_save, "escalate_to", None)
            if escalada is not None and instance.condition is not escalada:
                tracker.remove_instance(instance)
                tracker.add(ConditionInstance(
                    condition=escalada,
                    source=instance.source,
                    remaining_rounds=instance.repeat_save.escalate_rounds,
                    break_on_attack=instance.break_on_attack,
                ))
                _log_line(ctx, f"{nombre} queda {_label(escalada)} "
                               f"(falló la repetición de {_label(instance.condition)})")
                continue

        # 2. Duración.
        if instance.remaining_rounds is not None:
            instance.remaining_rounds -= 1
            if instance.remaining_rounds <= 0:
                tracker.remove_instance(instance)
                _log_line(ctx, f"{nombre}: termina {_label(instance.condition)}")


def _default_targeting():
    """Área por defecto (import perezoso para no crear ciclos)."""
    from .area import AreaTargeting
    return AreaTargeting()


@dataclass
class ConditionAction(CombatAction):
    """Acción con ``dc`` que deja una condición (sin daño).

    Elige objetivos hostiles vivos (uno al azar, o varios si la acción es de
    área) y cada objetivo tira su propia salvación: si falla, recibe la
    condición.
    """

    effect: Any = None
    targeting: Any = field(default_factory=_default_targeting)
    # Los hechizos de área (Sleep, Luz de hadas...) afectan a todos los
    # objetivos del área; sin este flag, AreaTargeting() con max=None
    # acabaría eligiendo un solo objetivo.
    es_area: bool = False
    usage: Any = None
    action_type: ActionType = ActionType.ACTION
    name: str = "Condición"

    def __post_init__(self) -> None:
        if not getattr(self, "name", ""):
            self.name = "Condición"

    def _seleccionar_objetivos(self, context) -> list:
        """Hostiles vivos: uno al azar, o todos si la acción es de área."""
        from .area import select_area_targets
        from ..core.randomness import pick

        actor = context.actor
        pool = list(valid_targets(actor, ctx=context))
        if not pool:
            return []
        if self.es_area:
            return select_area_targets(actor, context, self.targeting)
        minimo = int(getattr(self.targeting, "min_targets", 1) or 1)
        maximo = getattr(self.targeting, "max_targets", None)
        if maximo is None and minimo <= 1:
            # Objetivo único: uno al azar (sin tocar RNG si hay uno solo).
            return [pick(context.rng, pool)]
        return select_area_targets(actor, context, self.targeting)

    def execute(self, context) -> None:
        if not actor_is_alive(context):
            return  # el actor ya no está en pie: la habilidad no se lanza
        from .saves import registrar_resistencia, saving_throw

        effect = self.effect
        if effect is None:
            return
        actor = context.actor
        objetivos = self._seleccionar_objetivos(context)
        if not objetivos:
            return

        _log_line(context, f"{getattr(actor, 'name', actor)} usa {self.name} "
                           f"sobre {len(objetivos)} objetivo(s):")

        for objetivo in objetivos:
            if effect.save_ability is None:
                # Sin salvación: la condición se aplica directamente.
                repeat = None
                if effect.repeat_save:
                    repeat = RepeatSave(ability="dex", dc=effect.dc,
                                        escalate_to=getattr(effect, "escalate_to", None),
                                        escalate_rounds=getattr(effect, "escalate_rounds", None))
                apply_condition(
                    objetivo, effect.condition, context,
                    source=actor,
                    duration_rounds=effect.duration_rounds,
                    repeat_save=repeat,
                    escape=effect.escape,
                )
                continue
            sr = saving_throw(objetivo, effect.save_ability, effect.dc, context.rng)
            sr = registrar_resistencia(context, objetivo, sr)
            if sr.success:
                _log_line(context, f"  {getattr(objetivo, 'name', objetivo)}: "
                                   f"salvación {effect.save_ability.upper()} {sr.total} "
                                   f"vs CD {effect.dc}, éxito: sin efecto")
                continue
            repeat = None
            if effect.repeat_save:
                repeat = RepeatSave(ability=effect.save_ability, dc=effect.dc,
                                    escalate_to=getattr(effect, "escalate_to", None),
                                    escalate_rounds=getattr(effect, "escalate_rounds", None))
            apply_condition(
                objetivo, effect.condition, context,
                source=actor,
                duration_rounds=effect.duration_rounds,
                repeat_save=repeat,
                escape=effect.escape,
            )


__all__ = [
    "Condition", "EXCLUDED_CONDITIONS", "IMPLIED_CONDITIONS", "CONDITION_LABELS",
    "CONDITION_ATTACK_DAMAGE",
    "RepeatSave", "EscapeCheck", "ConditionInstance", "ConditionTracker",
    "ConditionEffect", "apply_condition", "attempt_escapes", "end_turn",
    "ConditionAction", "remove_condition", "remove_invisibility_on_action",
]

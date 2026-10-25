"""Base de los rasgos: la clase base y el despacho de hooks."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Trait:
    """Rasgo especial pasivo de una criatura (sin acciones propias)."""

    name: str = ""
    desc: str = ""

    # --- Tiradas -----------------------------------------------------------
    def modify_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                                rango: Any, ctx: Any = None,
                                rng: Any = None) -> None:
        """Hook: añade ventaja/desventaja a ``mods`` si el rasgo aplica.

        ``mods`` es un :class:`dnd_sim.rules.roll_modifiers.AttackModifiers` y
        ``rango`` el rango ya resuelto del ataque. ``ctx`` es el contexto
        del combate (con ``combatants``: la única información de posición
        que hay) y ``rng`` el generador, para los rasgos cuya condición no
        se puede comprobar (Pack Tactics). Si ``ctx`` o ``rng`` llegan
        vacíos el rasgo **no debe aplicarse** en lugar de inventar un
        resultado. Por defecto no hace nada.
        """
        return None

    # --- Daño recibido (fases de dnd_sim.rules.damage.inflict_damage) ------------
    def modify_incoming_damage(self, target: Any, amount: int,
                               damage_type: Any, source: Any,
                               ctx: Any = None) -> int | None:
        """Hook fase 1: ajusta el daño que ``target`` va a recibir.

        Recibe la cantidad en curso; devolver ``None`` deja el daño como
        está (devolver un entero lo sustituye; no puede ser negativo).
        """
        return None

    def after_damage_taken(self, target: Any, amount: int, damage_type: Any,
                           source: Any, ctx: Any = None) -> None:
        """Hook fase 2: efectos tras aplicar el daño.

        ``amount`` es el **daño original** que recibió ``target`` (ya
        descontado de sus PV en la fase 1).
        """
        return None

    # --- Al ser golpeado (hook de dnd_sim.engine.combat.attack_roll) ---------------
    def after_being_hit(self, target: Any, attacker: Any, rango: Any,
                        ctx: Any = None) -> None:
        """Hook: reacción cuando ``attacker`` **impacta** a ``target``.

        Se ejecuta tras el daño, en cada impacto (aunque el daño sea 0 por
        inmunidad), con ``rango`` el rango ya resuelto del ataque. Por
        defecto no hace nada.
        """
        return None

    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            crit: bool = False, ctx: Any = None,
                            rng: Any = None) -> int:
        """Hook: daño adicional que ``attacker`` suma a **este** ataque.

        Devuelve los PV extra (0 = nada). El motor los suma al daño bruto
        **antes** de la inmunidad/resistencia/vulnerabilidad del objetivo y
        con el tipo de daño del propio ataque; ``crit`` indica si el golpe
        es crítico para que los dados extra se dupliquen como el resto.
        Se dispara en :func:`dnd_sim.engine.combat.attack_roll`.
        """
        return 0

    # --- Salvaciones -------------------------------------------------------
    def modify_save_modifiers(self, mods: Any, target: Any,
                              ability: str, kind: str | None = None) -> None:
        """Hook: ventaja/desventaja en la salvación ``ability`` de ``target``.

        ``mods`` es un :class:`dnd_sim.rules.roll_modifiers.SaveModifiers` y
        ``ability`` la característica ya normalizada (``"str"``...).
        ``kind`` dice qué tipo de efecto provoca la salvación cuando quien
        la tira lo sabe: hoy solo ``"turn"`` (un efecto que convierte
        no-muertos, p. ej. Turn Undead) y todavía no lo pasa nadie
        (# TODO). Se ejecuta en :func:`dnd_sim.rules.roll_modifiers.save_modifiers`.
        Por defecto no hace nada.
        """
        return None

    # --- Pruebas de característica ----------------------------------------
    def modify_check_modifiers(self, mods: Any, target: Any, ability: str,
                               skill: str | None = None) -> None:
        """Hook: ventaja/desventaja en la prueba ``ability`` de ``target``.

        ``mods`` es un :class:`dnd_sim.rules.roll_modifiers.CheckModifiers`.
        ``skill`` es la habilidad asociada si la hubiera (``"perception"``);
        # TODO: las habilidades aún no se modelan, así que hoy siempre es
        ``None``: un rasgo limitado a una habilidad (Keen Senses) no puede
        distinguirla y debe esperar a ese modelo. Por defecto no hace nada.
        """
        return None

    # --- Inicio del turno --------------------------------------------------
    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        """Hook: efecto pasivo al inicio del turno propio de ``actor``.

        Se ejecuta en :func:`dnd_sim.rules.usage.begin_turn`, con los recursos ya
        cargados y **antes de comprobar si el actor está incapacitado**
        (es un efecto automático, no una acción). Por defecto no hace nada.
        """
        return None

    # --- Supervivencia a 0 PV ----------------------------------------------
    def survives_at_zero_hp(self, owner: Any) -> bool:
        """Hook: ¿sigue vivo ``owner`` aunque tenga 0 PV (o menos)?

        Lo consulta :attr:`dnd_sim.model.combatant.Combatant.alive` justo cuando
        los PV llegan a 0: un rasgo que responda ``True`` (Regeneration)
        mantiene a la criatura en pie hasta que **su propio** turno decida
        si se recupera o muere. Si nadie responde, 0 PV sigue significando
        muerte. Por defecto ``False``.
        """
        return False

    def on_reduced_to_zero_hp(self, owner: Any, amount: int,
                              damage_type: Any = None, source: Any = None,
                              crit: bool = False, ctx: Any = None,
                              rng: Any = None) -> int | None:
        """Hook: el daño acaba de dejar a ``owner`` a 0 PV; decide ya.

        A diferencia de ``survives_at_zero_hp``, que se consulta de forma
        **diferida** cuando se pregunta si sigue vivo (Regeneration decide
        en su propio turno), esta se resuelve **al instante**, al aplicar el
        daño (Undead Fortitude tira su salvación; Relentless mira su umbral
        de daño). Vive en :func:`dnd_sim.rules.damage.inflict_damage`, que solo
        la llama si el daño lo ha bajado desde PV positivos.

        ``amount`` es el daño que lo ha dejado a 0, ``crit`` si ese daño
        viene de un crítico y ``rng`` el generador con el que tirar (si no
        llega, el rasgo se abstiene en lugar de inventar un resultado).
        Devuelve los PV con los que sigue (1) o ``None`` si muere. Por
        defecto ``None``.
        """
        return None

    # --- Acciones que aporta el rasgo ----------------------------------------
    def extra_actions(self, owner: Any) -> list:
        """Hook: acciones que el rasgo añade al combatiente.

        Se ejecuta una sola vez, al construir el monstruo
        (:class:`dnd_sim.model.combatant.Monster`). Lo usa Superior Invisibility,
        que la ficha trae como acción de la criatura y no como rasgo
        pasivo: el rasgo sabe montarla y se la añade a ``owner.actions``.
        Devuelve la lista de acciones (vacía = ninguna). Por defecto
        ninguna.
        """
        return []

    # --- CA del defensor ----------------------------------------------------
    def defensive_ac_bonus(self, target: Any, attacker: Any, rango: Any,
                           total: int | None = None, ca: int | None = None,
                           ctx: Any = None, rng: Any = None) -> int:
        """Hook: CA extra que ``target`` suma contra **este** ataque.

        Solo se le pregunta cuando el ataque iba a impactar y no es
        crítico (un 20 natural da igual la CA). ``total`` es la tirada y
        ``ca`` la CA efectiva **sin** el bonificador, para que el rasgo
        decida si compensa: una reacción (Parry) solo se gasta si con el
        bonificador el golpe deja de entrar. Devuelve los puntos de CA
        (0 = nada). Se dispara en :func:`dnd_sim.engine.combat.attack_roll`.
        Por defecto no hace nada.
        """
        return 0

    # --- Reinicio de combate ------------------------------------------------
    def reset(self) -> None:
        """Hook: borra el estado propio del rasgo al empezar un combate.

        Se llama desde :meth:`dnd_sim.model.combatant.Combatant.reset` (los
        mismos objetos se reutilizan en ``simulate()``, así que el estado
        por combate se limpia aquí). Por defecto no hace nada.
        """
        return None


#: Nombres de los hooks que un rasgo puede sobrescribir (catálogo completo).
#: Es la fuente de verdad de :func:`hooks`: si añades un hook nuevo a
#: :class:`Trait`, regístralo aquí para que el despacho lo reconozca.
HOOK_NAMES: tuple[str, ...] = (
    "modify_attack_modifiers",
    "modify_save_modifiers",
    "modify_check_modifiers",
    "modify_incoming_damage",
    "after_damage_taken",
    "after_being_hit",
    "extra_attack_damage",
    "defensive_ac_bonus",
    "on_turn_start",
    "survives_at_zero_hp",
    "on_reduced_to_zero_hp",
    "extra_actions",
    "reset",
)


def hooks(traits: Any, nombre: str) -> list[Any]:
    """Rasgos de ``traits`` (lista o ``None``) que **sobrescriben** ``nombre``.

    Único punto de despacho de los hooks de los rasgos: los que no
    sobrescriben el hook (la base :class:`Trait` lo define como no-op) no se
    llaman. Todos los módulos que miran rasgos pasan por aquí para que el
    filtro sea idéntico en todos los puntos de enganche.

    Lanza ``ValueError`` si ``nombre`` no está en :data:`HOOK_NAMES` (typo
    detectado en cuanto se llama, no a mitad de un combate).
    """
    if nombre not in HOOK_NAMES:
        raise ValueError(f"Hook de rasgo desconocido: {nombre!r}")
    if not traits:
        return []
    base = getattr(Trait, nombre, None)
    activos: list[Any] = []
    for rasgo in traits:
        if not callable(getattr(rasgo, nombre, None)):
            continue
        # Sobrescribe si lo define la propia instancia o su clase no es la
        # implementación por defecto de Trait (no-op).
        si_propio = nombre in getattr(rasgo, "__dict__", {})
        if not si_propio:
            si_propio = getattr(type(rasgo), nombre, None) is not base
        if si_propio:
            activos.append(rasgo)
    return activos

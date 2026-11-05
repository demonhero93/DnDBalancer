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
                                rng: Any = None, atk: Any = None) -> None:
        """Hook: añade ventaja/desventaja a ``mods`` si el rasgo aplica.

        ``mods`` es un :class:`dnd_sim.rules.roll_modifiers.AttackModifiers` y
        ``rango`` el rango ya resuelto del ataque. ``ctx`` es el contexto
        del combate (con ``combatants``: la única información de posición
        que hay) y ``rng`` el generador, para los rasgos cuya condición no
        se puede comprobar (Pack Tactics). ``atk`` es el objeto ataque con
        que se tira (p. ej. para distinguir un ataque con FUE en Furia);
        ``None`` si el llamante no lo pasa. Si ``ctx`` o ``rng`` llegan
        vacíos el rasgo **no debe aplicarse** en lugar de inventar un
        resultado. Por defecto no hace nada.
        """
        return None

    # --- Ventaja/desventaja que este rasgo granta a los ataques de otros ------
    def grant_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                               rango: Any, ctx: Any = None,
                               rng: Any = None, atk: Any = None) -> None:
        """Hook: ventaja/desventaja que este rasgo **granta** al ataque de ``attacker``.

        Se ejecuta en :func:`dnd_sim.rules.roll_modifiers.attack_modifiers`
        consultando los rasgos del **resto** de combatientes del contexto
        (el atacante ya pasó por ``modify_attack_modifiers``): es la vía
        para que un rasgo influya en ataques de terceros (p. ej. Lobo/León
        del Corazón Salvaje). ``mods`` es el mismo
        :class:`dnd_sim.rules.roll_modifiers.AttackModifiers` y cada rasgo
        decide por sí mismo si aplica (bandos, cobertura...). Por defecto
        no hace nada.
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

    # --- Al golpear (otro hook de dnd_sim.engine.combat.attack_roll) ---------
    def after_dealing_hit(self, target: Any, attacker: Any, rango: Any,
                          ctx: Any = None, atk: Any = None,
                          damage: int | None = None) -> None:
        """Hook: efecto cuando ``attacker`` (dueño del rasgo) **impacta**.

        Espejo de :meth:`after_being_hit` por el lado del atacante: se
        ejecuta tras el daño, en cada impacto, con ``target`` la criatura
        golpeada (p. ej. Protectores Ancestrales: marcar a la primera
        criatura golpeada en el turno). ``atk`` es el objeto ataque y
        ``damage`` el daño principal final ya aplicado (p. ej. el Mordisco
        cura solo si ``damage > 0``); ``None`` si el llamante no los pasa.
        Por defecto no hace nada.
        """
        return None

    # --- Tras la tirada de ataque (hook de dnd_sim.engine.combat.attack_roll) -
    def after_attack_roll(self, attacker: Any, target: Any, atk: Any,
                          hit: bool, ctx: Any = None,
                          rng: Any = None) -> None:
        """Hook: efecto tras resolver una tirada de ataque, acierte o falle.

        Se dispara al final de :func:`dnd_sim.engine.combat.attack_roll`,
        con ``hit`` el resultado de la tirada. Lo usa el ataque extra de
        las Garras (Path of the Beast): se lanza aunque la tirada falle
        («when you attack with them»). Por defecto no hace nada.
        """
        return None

    # --- Furia del bárbaro (hooks de dnd_sim.rules.classes.barbarian) -------
    def on_rage_start(self, actor: Any, ctx: Any = None) -> None:
        """Hook: la Furia de ``actor`` acaba de empezar.

        Se dispara desde ``RageAction.execute`` tras activar la Furia (ya
        con ``rage_active`` verdadero). Lo usan las subclases para elegir
        su forma o sus aliados (Path of the Beast). Por defecto no hace
        nada.
        """
        return None

    def on_rage_end(self, actor: Any, ctx: Any = None) -> None:
        """Hook: la Furia de ``actor`` acaba de terminar por cualquier motivo.

        Se dispara desde ``BarbarianFeatures`` en cuanto pone
        ``rage_active`` a falso (incapacitado, expiración sin extensión...).
        Lo usan las subclases para retirar efectos ligados a la Furia.
        Por defecto no hace nada.
        """
        return None

    # --- Mitigar daño de otros (hook de dnd_sim.rules.damage) ----------------
    def reduce_damage_to_allies(self, target: Any, amount: int,
                                damage_type: Any = None,
                                source: Any = None,
                                ctx: Any = None) -> int | None:
        """Hook: reducir el daño que recibe **otro** combatiente.

        Se consulta a los rasgos del resto de combatientes (hace falta
        ``ctx`` con ``combatants``) justo antes de bajar los PV de
        ``target``; devuelve la cantidad nueva o ``None`` sin cambios.
        El nombre habla de aliados, pero el hook no comprueba bandos:
        quien lo implementa decide a quién protege (p. ej. Espíritu
        Guardián del Bárbaro, que no se protege a sí mismo).
        """
        return None

    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            crit: bool = False, ctx: Any = None,
                            rng: Any = None, atk: Any = None) -> int:
        """Hook: daño adicional que ``attacker`` suma a **este** ataque.

        Devuelve los PV extra (0 = nada). El motor los suma al daño bruto
        **antes** de la inmunidad/resistencia/vulnerabilidad del objetivo y
        con el tipo de daño del propio ataque; ``crit`` indica si el golpe
        es crítico para que los dados extra se dupliquen como el resto.
        ``atk`` es el objeto ataque (p. ej. para condicionarlo a una
        habilidad); ``None`` si el llamante no lo pasa.
        Se dispara en :func:`dnd_sim.engine.combat.attack_roll`.
        """
        return 0

    # --- Piso de los dados de daño (Great Weapon Fighting) --------------------
    def damage_dice_upgrades(self, attacker: Any, atk: Any,
                             rango: Any = None, ctx: Any = None,
                             rng: Any = None) -> int:
        """Hook: valor mínimo que pueden mostrar los dados de **este** golpe.

        Devuelve el piso (0 = sin piso); el motor lo pasa a
        :func:`dnd_sim.core.dice.roll_dice(floor=...)`, que cuenta los
        dados por debajo del piso como el propio piso (GWF: 1 o 2 → 3).
        No cambia el número de llamadas al RNG. Por defecto no hace nada.
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

    def grant_save_modifiers(self, mods: Any, target: Any, ability: str,
                             kind: str | None = None,
                             ctx: Any = None) -> None:
        """Hook: ventaja/desventaja que este rasgo **granta** a la salvación de ``target``.

        Se ejecuta en :func:`dnd_sim.rules.roll_modifiers.save_modifiers`
        consultando los rasgos del **resto** de combatientes del contexto
        (el propio objetivo ya pasó por ``modify_save_modifiers``): es la
        vía para que un rasgo influya en salvaciones de terceros (p. ej.
        Zealous Presence). ``mods`` es el mismo
        :class:`dnd_sim.rules.roll_modifiers.SaveModifiers` y cada rasgo
        decide por sí mismo si aplica (bandos, cobertura...). Por defecto
        no hace nada.
        """
        return None

    # --- Tras fallar una salvación -------------------------------------------
    def after_failed_save(self, target: Any, ability: str, result: Any,
                          ctx: Any = None) -> Any:
        """Hook: ``target`` acaba de FALLAR una salvación (o auto-falló).

        Se despacha desde :func:`dnd_sim.rules.registrar_resistencia`
        (el punto con contexto tras cada ``saving_throw``) solo si llega
        ``ctx`` y el resultado sigue fallando (la Resistencia legendaria
        ya se aplicó; un fallo convertido en éxito NO lo dispara).
        ``ability`` es la característica normalizada (``"con"``...) y
        ``result`` el :class:`SaveResult`. Devolver un ``SaveResult``
        nuevo **sustituye** al original (p. ej. la repetición de
        Fanatical Focus); devolver ``None`` lo deja igual. Lo usan
        Unstable Backlash (Path of Wild Magic) y Fanatical Focus (Path
        of the Zealot). Por defecto no hace nada.
        """
        return None

    # --- Pruebas de característica ----------------------------------------
    def modify_check_modifiers(self, mods: Any, target: Any, ability: str,
                               skill: str | None = None) -> None:
        """Hook: ventaja/desventaja en la prueba ``ability`` de ``target``.

        ``mods`` es un :class:`dnd_sim.rules.roll_modifiers.CheckModifiers`.
        ``skill`` es la habilidad asociada si la prueba es de habilidad
        (``"perception"``) o ``None`` en una prueba pura de característica:
        un rasgo limitado a una habilidad (Keen Senses) distingue entre
        ambas por ese argumento. Por defecto no hace nada.
        """
        return None

    # --- Condiciones --------------------------------------------------------
    def blocks_condition(self, condition: Any, ctx: Any = None) -> bool:
        """Hook: ¿impide ``condition`` aplicarse al dueño del rasgo?

        Se consulta en :func:`dnd_sim.rules.conditions.apply_condition`
        junto al campo estático ``Combatant.condition_immunities``: si el
        campo la lista o cualquier rasgo responde ``True``, no se crea la
        instancia y el log registra «X es inmune a …». ``ctx`` es el
        contexto del combate. Por defecto no bloquea nada.
        """
        return False

    # --- Inicio del turno --------------------------------------------------
    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        """Hook: efecto pasivo al inicio del turno propio de ``actor``.

        Se ejecuta en :func:`dnd_sim.rules.usage.begin_turn`, con los recursos ya
        cargados y **antes de comprobar si el actor está incapacitado**
        (es un efecto automático, no una acción). Por defecto no hace nada.
        """
        return None

    # --- Fin del turno -----------------------------------------------------
    def on_turn_end(self, actor: Any, ctx: Any = None) -> None:
        """Hook: efecto pasivo al fin del turno propio de ``actor``.

        Se ejecuta en :func:`dnd_sim.rules.conditions.end_turn` **antes**
        de mirar las condiciones (debe correr aunque no haya ninguna).
        Lo usa la Furia para evaluar su extensión/fin de ronda. Por defecto
        no hace nada.
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
    "grant_attack_modifiers",
    "modify_save_modifiers",
    "grant_save_modifiers",
    "after_failed_save",
    "modify_check_modifiers",
    "modify_incoming_damage",
    "after_damage_taken",
    "after_being_hit",
    "after_dealing_hit",
    "after_attack_roll",
    "reduce_damage_to_allies",
    "extra_attack_damage",
    "damage_dice_upgrades",
    "blocks_condition",
    "defensive_ac_bonus",
    "on_rage_start",
    "on_rage_end",
    "on_turn_start",
    "on_turn_end",
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

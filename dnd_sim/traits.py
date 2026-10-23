"""Rasgos especiales de monstruos (features de la ficha).

Todo lo que una criatura **genérica** puede tener ya vive en su sitio (CA,
PV, ataques, salvaciones, usos limitados, hechizos, legendario, estados y
condiciones). Aquí van los **rasgos con reglas propias** que no son acciones
ni estados: efectos pasivos que modifican cómo se resuelven las tiradas.

Formato real en la API (dnd5eapi.co, SRD 2014):

.. code-block:: json

    {"name": "Blood Frenzy",
     "desc": "The sahuagin has advantage on melee attack rolls against any
              creature that doesn't have all its hit points.",
     "damage": []}

Estructura:

- :class:`Trait`: el rasgo con su nombre y descripción más los **hooks** de
  reglas. Un hook que un rasgo no implementa no hace nada, así que cada rasgo
  solo influye en lo que sabe modelar.
- :data:`TRAIT_CLASSES`: registro ``nombre -> clase``; lo consume
  :func:`dnd_sim.data.trait_parser.parse_traits` para rellenar
  ``Combatant.traits`` al cargar un monstruo.

Rasgos implementados:

- **Blood Frenzy** (sahuagin): ventaja en los ataques **cuerpo a cuerpo**
  contra criaturas que no tienen todos sus PV. El hook se ejecuta en
  :func:`dnd_sim.roll_modifiers.attack_modifiers` (la única fuente del modo
  de tirada), así que convive correctamente con los indicadores estáticos y
  las condiciones: si hay ventaja y desventaja a la vez se anulan.
- **Damage Transfer** (cloaker): mientras esté enganchado, el daño que
  recibe se parte en dos: él baja la mitad (redondeada hacia abajo) y la
  criatura enganchada se lleva la otra mitad. Los hooks viven en
  :func:`dnd_sim.damage.inflict_damage` (fases 1 y 2); el enganche en sí lo
  modela :mod:`dnd_sim.attach`.
- **Heated Body** (azer): quien lo golpea cuerpo a cuerpo recibe 1d10 de
  daño de fuego. El trigger es el **impacto**, así que el hook vive en
  :func:`dnd_sim.combat.attack_roll` (``after_being_hit``) y se activa
  aunque el daño sea 0 por inmunidad.

Cómo añadir un rasgo nuevo (p. ej. Pack Tactics o Sunlight Sensitivity):

1. Crea la clase en este módulo con sus hooks (hoy:
   ``modify_attack_modifiers`` para tiradas; ``modify_incoming_damage`` /
   ``after_damage_taken`` para daño entrante; y ``after_being_hit`` para
   reacciones al ser golpeado; se añadirán ``modify_save_modifiers`` /
   ``modify_check_modifiers`` cuando un rasgo los necesite).
2. Regístrala en :data:`TRAIT_CLASSES` con su nombre en minúsculas.
3. Nada más: ``parse_traits()`` la detectará en ``special_abilities``.

# TODO: rasgos de la SRD que el motor aún no modela (no combativos o fuera
# de combate): Limited Amphibiousness, Shark Telepathy, Amphibious, Water
# Breathing... y los que dependen de un modelo que aún no existe:
# Light Sensitivity / Phantasms (necesitan luz e ilusiones).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:
    from .damage import inflict_damage
    from .dice import roll_dice
    from .roll_modifiers import AttackRange
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from damage import inflict_damage
        from dice import roll_dice
        from roll_modifiers import AttackRange
    except ImportError:
        from dnd_sim.damage import inflict_damage
        from dnd_sim.dice import roll_dice
        from dnd_sim.roll_modifiers import AttackRange


def _log_line(ctx: Any, line: str) -> None:
    log = getattr(ctx, "log", None)
    if log is None:
        return
    try:
        log.append(line)
    except Exception:
        pass


@dataclass
class Trait:
    """Rasgo especial pasivo de una criatura (sin acciones propias)."""

    name: str = ""
    desc: str = ""

    # --- Tiradas -----------------------------------------------------------
    def modify_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                                rango: Any) -> None:
        """Hook: añade ventaja/desventaja a ``mods`` si el rasgo aplica.

        ``mods`` es un :class:`dnd_sim.roll_modifiers.AttackModifiers` y
        ``rango`` el rango ya resuelto del ataque. Por defecto no hace nada.
        """
        return None

    # --- Daño recibido (fases de dnd_sim.damage.inflict_damage) ------------
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

    # --- Al ser golpeado (hook de dnd_sim.combat.attack_roll) ---------------
    def after_being_hit(self, target: Any, attacker: Any, rango: Any,
                        ctx: Any = None) -> None:
        """Hook: reacción cuando ``attacker`` **impacta** a ``target``.

        Se ejecuta tras el daño, en cada impacto (aunque el daño sea 0 por
        inmunidad), con ``rango`` el rango ya resuelto del ataque. Por
        defecto no hace nada.
        """
        return None


@dataclass
class BloodFrenzy(Trait):
    """Blood Frenzy (sahuagin): ventaja cuerpo a cuerpo contra un herido.

    «The sahuagin has advantage on melee attack rolls against any creature
    that doesn't have all its hit points.» (SRD 2014)
    """

    def modify_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                                rango: Any) -> None:
        if rango is not AttackRange.MELEE:
            return  # solo ataques cuerpo a cuerpo
        max_hp = int(getattr(target, "max_hp", 0) or 0)
        hp = int(getattr(target, "hp", max_hp) or 0)
        if 0 < max_hp and hp < max_hp:
            mods.advantage_sources.append(self.name or "Blood Frenzy")


@dataclass
class DamageTransfer(Trait):
    """Damage Transfer (cloaker): el daño que recibe se parte en dos.

    «While attached to a creature, the cloaker takes only half the damage
    dealt to it (rounded down), and that creature takes the other half.»
    (SRD 2014). Solo aplica mientras el portador esté enganchado: el
    enganche y su desenganche los modela :mod:`dnd_sim.attach`.
    """

    @staticmethod
    def _enganchado(target: Any) -> Any:
        """Criatura a la que ``target`` está enganchado (viva), o ``None``."""
        otro = getattr(getattr(target, "state", None), "attached_to", None)
        if otro is None or otro is target:
            return None
        if not getattr(target, "alive", True) or not getattr(otro, "alive", True):
            return None  # muerto de los dos lados: el reparto no aplica
        return otro

    def modify_incoming_damage(self, target: Any, amount: int,
                               damage_type: Any, source: Any,
                               ctx: Any = None) -> int | None:
        if self._enganchado(target) is None:
            return None
        return int(amount) // 2  # «only half ... (rounded down)»

    def after_damage_taken(self, target: Any, amount: int, damage_type: Any,
                           source: Any, ctx: Any = None) -> None:
        otro = self._enganchado(target)
        if otro is None:
            return
        otros = int(amount) - int(amount) // 2  # «and that creature takes the other half»
        if otros <= 0:
            return
        inflict_damage(otro, otros, damage_type, source=source, ctx=ctx)
        _log_line(
            ctx,
            f"{getattr(target, 'name', target)} reparte el daño: "
            f"{getattr(otro, 'name', otro)} recibe los otros {otros}",
        )


@dataclass
class HeatedBody(Trait):
    """Heated Body (azer): daño de fuego a quien lo golpea cuerpo a cuerpo.

    «A creature that touches the azer or hits it with a melee attack while
    within 5 ft. of it takes 5 (1d10) fire damage.» (SRD 2014). El trigger
    es el **impacto** (no el daño recibido), así que el hook vive en
    :func:`dnd_sim.combat.attack_roll` y se activa aunque el daño sea 0
    (p. ej. por inmunidad). El toque se modela como ataque cuerpo a cuerpo
    (el alcance del motor no distingue «toque» de «cuerpo a cuerpo»).
    """

    damage: str = "1d10"
    damage_type: str = "fire"

    def after_being_hit(self, target: Any, attacker: Any, rango: Any,
                        ctx: Any = None) -> None:
        if rango is not AttackRange.MELEE:
            return  # solo el contacto / ataque cuerpo a cuerpo
        if attacker is None or not getattr(attacker, "alive", True):
            return
        if int(getattr(attacker, "hp", 0) or 0) <= 0:
            return
        try:
            dados = str(self.damage or "1d10").strip() or "1d10"
        except Exception:
            dados = "1d10"
        rng = getattr(ctx, "rng", None)
        cantidad = roll_dice(dados, rng) if rng is not None else 1
        inflict_damage(attacker, cantidad, self.damage_type,
                       source=target, ctx=ctx)
        _log_line(
            ctx,
            f"{getattr(target, 'name', target)} quema a "
            f"{getattr(attacker, 'name', attacker)} (cuerpo ardiente): "
            f"{cantidad} daño de fuego",
        )


#: Registro de rasgos modelables: nombre en minúsculas -> clase.
TRAIT_CLASSES: dict[str, type[Trait]] = {
    "blood frenzy": BloodFrenzy,
    "damage transfer": DamageTransfer,
    "heated body": HeatedBody,
}


__all__ = ["Trait", "BloodFrenzy", "DamageTransfer", "HeatedBody",
           "TRAIT_CLASSES"]

"""Rasgos defensivos: reducen el daﾃｱo recibido o se oponen al ataque.

Damage Transfer, Heated Body (represalia al ser golpeado), Turn
Resistance y Parry (reacciﾃｳn que sube la CA).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .base import Trait
from ..conditions import Condition
from ..damage import (apply_damage_modifiers, inflict_damage,
                       parse_damage_type)
from ...core.dice import roll_dice
from ...core.log import log_line as _log_line
from ..roll_modifiers import AttackRange

@dataclass
class DamageTransfer(Trait):
    """Damage Transfer (cloaker): el daño que recibe se parte en dos.

    «While attached to a creature, the cloaker takes only half the damage
    dealt to it (rounded down), and that creature takes the other half.»
    (SRD 2014). Solo aplica mientras el portador esté enganchado: el
    enganche y su desenganche los modela :mod:`dnd_sim.rules.attach`. La otra
    mitad es daño normal para el receptor, así que su inmunidad,
    resistencia o vulnerabilidad también cuenta.
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
        mitad = int(amount) - int(amount) // 2  # «and that creature takes the other half»
        if mitad <= 0:
            return
        # La mitad transferida es daño como cualquier otro: el receptor
        # aplica su propia inmunidad/resistencia/vulnerabilidad (los tipos
        # que no se reconocen pasan sin modificar, como hace inflict_damage).
        try:
            dt = parse_damage_type(damage_type)
        except Exception:
            dt = None
        from ...engine.combat import _tag_modificadores as _tag
        final = mitad if dt is None else apply_damage_modifiers(mitad, dt, otro)
        tag = "" if dt is None else _tag(mitad, final, dt, otro)
        inflict_damage(otro, final, dt, source=source, ctx=ctx)
        _log_line(
            ctx,
            f"{getattr(target, 'name', target)} reparte el daño: "
            f"{getattr(otro, 'name', otro)} recibe los otros "
            f"{final}{tag}",
        )


@dataclass
class HeatedBody(Trait):
    """Heated Body (azer): daño de fuego a quien lo golpea cuerpo a cuerpo.

    «A creature that touches the azer or hits it with a melee attack while
    within 5 ft. of it takes 5 (1d10) fire damage.» (SRD 2014). El trigger
    es el **impacto** (no el daño recibido), así que el hook vive en
    :func:`dnd_sim.engine.combat.attack_roll` y se activa aunque el daño sea 0
    (p. ej. por inmunidad). El toque se modela como ataque cuerpo a cuerpo
    (el alcance del motor no distingue «toque» de «cuerpo a cuerpo»).

    Como todo daño, la represalia pasa por
    :func:`dnd_sim.rules.damage.apply_damage_modifiers`: a quien es **inmune** le
    llega 0 (se sigue registrando el impacto, como en el daño principal) y
    a quien resiste, la mitad.
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
        # Resistencias/inmunidades/vulnerabilidades del que golpea: la
        # llamada a inflict_damage se hace igualmente (con 0) para que el
        # impacto quede registrado como en el daño principal.
        cantidad = apply_damage_modifiers(cantidad, self.damage_type, attacker)
        sin_efecto = "" if cantidad > 0 else " (sin efecto: inmune o resistente)"
        inflict_damage(attacker, cantidad, self.damage_type,
                       source=target, ctx=ctx)
        _log_line(
            ctx,
            f"{getattr(target, 'name', target)} quema a "
            f"{getattr(attacker, 'name', attacker)} (cuerpo ardiente): "
            f"{cantidad} daño de fuego{sin_efecto}",
        )

@dataclass
class TurnResistance(Trait):
    """Turn Resistance (lich): ventaja en las salvaciones contra los
    efectos que convierten no-muertos.

    «The lich has advantage on saving throws against any effect that turns
    undead.» (API, SRD 2014). Solo se activa si la salvación llega marcada
    con ``kind="turn"``: hoy ningún efecto del motor convierte, así que el
    rasgo está cableado de punta a punta y probado, pero en reposo
    (# TODO: cuando exista Turn Undead deberá pasar ``kind="turn"``).
    """

    def modify_save_modifiers(self, mods: Any, target: Any, ability: str,
                              kind: str | None = None) -> None:
        if kind == "turn":
            mods.advantage_sources.append(self.name or "Turn Resistance")


def _ve_al_atacante(attacker: Any) -> bool:
    """¿Ve el defensor al atacante? (a un invisible no se le puede parar)."""
    try:
        return not attacker.conditions.has(Condition.INVISIBLE)
    except Exception:
        return True


def _empuna_arma_melee(defensor: Any) -> bool:
    """¿Empuña el defensor un arma cuerpo a cuerpo? («be wielding a melee
    weapon»). Sin ataques a distancia no hay con qué parar nada."""
    ataques = getattr(defensor, "attacks", None) or []
    return any(
        getattr(a, "range_type", AttackRange.MELEE) is not AttackRange.RANGED
        for a in ataques
    )


@dataclass
class Parry(Trait):
    """Parry (hobgoblin warlord, gladiador, caballero, noble...): +N de CA.

    «The hobgoblin adds 3 to its AC against one melee attack that would hit
    it. To do so, the hobgoblin must see the attacker and be wielding a
    melee weapon.» (SRD 2014). En la API lo traen seis monstruos, todos con
    la misma estructura y distinto número (2, 3, 4 o 5).

    Es una **reacción**: si el combatiente ya ha gastado la suya en este
    turno no puede parar (``state.reaction_used``, el mismo indicador que
    usan las reacciones del motor, y que se recarga en su propio turno).

    Y solo compensa si evita el golpe, así que el hook recibe la tirada y
    la CA y gasta la reacción **solo** si con el bonificador el ataque
    falla: nadie gasta su reacción en parar un golpe que igual entra.

    El número sale de la descripción («adds 3 to its AC»); sin número
    legible el rasgo no hace nada.
    """

    bonus: int = 0

    def __post_init__(self) -> None:
        match = re.search(r"adds (\d+) to its AC", self.desc or "")
        if match:
            self.bonus = int(match.group(1))

    def defensive_ac_bonus(self, target: Any, attacker: Any, rango: Any,
                           total: int | None = None, ca: int | None = None,
                           ctx: Any = None, rng: Any = None) -> int:
        if self.bonus <= 0:
            return 0  # descripción no interpretable: el rasgo no hace nada
        if rango is not AttackRange.MELEE:
            return 0  # «against one melee attack»
        if not _ve_al_atacante(attacker) or not _empuna_arma_melee(target):
            return 0  # «must see the attacker and be wielding a melee weapon»
        estado = getattr(target, "state", None)
        if estado is not None and getattr(estado, "reaction_used", False):
            return 0  # su reacción de este turno ya está gastada
        if total is not None and ca is not None and ca + self.bonus <= total:
            return 0  # no compensa: no se gasta la reacción en vano
        if estado is not None:
            estado.reaction_used = True
        _log_line(ctx, f"{getattr(target, 'name', target)} usa "
                       f"{self.name or 'Parry'}: +{self.bonus} CA "
                       f"(el ataque no llega)")
        return self.bonus

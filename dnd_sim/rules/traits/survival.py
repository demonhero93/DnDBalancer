"""Rasgos de supervivencia: quiﾃｩn aguanta a 0 PV y quiﾃｩn se recupera.

Regeneration (muere en su propio turno), Relentless y Undead Fortitude
(resuelven el daﾃｱo que los deja a 0 PV).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .base import Trait
from ..damage import DamageType, parse_damage_type
from ..usage import ActionUsage
from ...core.log import log_line as _log_line

@dataclass
class Regeneration(Trait):
    """Regeneration (troll): recupera PV al inicio de su turno.

    «The troll regains 10 hit points at the start of its turn. If the troll
    takes acid or fire damage, this trait doesn't function at the start of
    the troll's next turn. The troll dies only if it starts its turn with 0
    hit points and doesn't regenerate.» (API, SRD 2014)

    Cada frase es un hook:

    - ``after_damage_taken``: el ácido o el fuego bloquea **el próximo**
      inicio de turno (y solo ese).
    - ``on_turn_start``: cura ``amount`` PV; o bien muere si empieza el
      turno a 0 PV sin poder regenerarse.
    - ``survives_at_zero_hp``: hasta ese momento, a 0 PV sigue vivo (va a
      morir en su turno, no al recibir el golpe).
    - ``reset``: el estado es por combate y ``simulate()`` reutiliza los
      mismos objetos, así que se limpia con ``Combatant.reset()``.

    El ``amount`` sale de la descripción («regains 10 hit points»); si no
    se puede leer, el rasgo no hace nada y la criatura muere a 0 PV como
    cualquier otra.

    # TODO: la curación se calcula desde 0 PV porque el motor sí deja los
    # PV por debajo de 0 y la regla 5e no contempla PV negativos.
    """

    amount: int = 0
    blocked: bool = False   # ácido/fuego recibido desde su turno anterior
    dead: bool = False      # murió por no poder regenerarse a 0 PV

    def __post_init__(self) -> None:
        match = re.search(r"(\d+)\s+hit\s+points", self.desc or "")
        if match:
            self.amount = int(match.group(1))

    def after_damage_taken(self, target: Any, amount: int, damage_type: Any,
                           source: Any, ctx: Any = None) -> None:
        if int(amount or 0) <= 0:
            return
        try:
            dt = parse_damage_type(damage_type)
        except Exception:
            return  # sin tipo reconocible no hay con qué bloquearlo
        if dt in (DamageType.ACID, DamageType.FIRE):
            self.blocked = True

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        if self.amount <= 0 or self.dead:
            return  # sin cantidad legible, o ya muerto
        hp = int(getattr(actor, "hp", 0) or 0)
        max_hp = int(getattr(actor, "max_hp", hp) or hp)
        name = getattr(actor, "name", actor)
        if self.blocked:
            # El bloqueo dura exactamente un inicio de turno.
            self.blocked = False
            if hp <= 0:
                # «dies only if it starts its turn with 0 hit points and
                # doesn't regenerate».
                self.dead = True
                try:
                    ctx.skip_turn = True
                except Exception:
                    pass
                _log_line(ctx, f"{name} empieza su turno con 0 PV sin poder "
                               f"regenerarse: muere")
                return
            _log_line(ctx, f"{name} no regenera este turno (ácido o fuego)")
            return
        if hp <= 0:
            hp = 0  # la regla 5e no tiene PV negativos
        if hp >= max_hp:
            return  # nada que curar
        curado = min(self.amount, max_hp - hp)
        try:
            actor.hp = hp + curado
        except Exception:
            return
        _log_line(ctx, f"{name} regenera {curado} PV (Regeneration) "
                       f"(HP {max(actor.hp, 0)}/{max_hp})")

    def survives_at_zero_hp(self, owner: Any) -> bool:
        # Muere en el turno en que empieza a 0 PV sin regenerarse; hasta
        # entonces sigue en pie (y sigue siendo un objetivo más).
        return self.amount > 0 and not self.dead

    def reset(self) -> None:
        self.blocked = False
        self.dead = False

@dataclass
class Relentless(Trait):
    """Relentless (jabalí, jabalí gigante, hombre lobo): no cae con poco
    daño.

    «If the boar takes 7 damage or less that would reduce it to 0 hit
    points, it is reduced to 1 hit point instead.» (API, SRD 2014)

    El umbral sale de la descripción y cambia por ficha (7 el jabalí, 10 el
    gigante, 14 el hombre lobo). La ficha lo trae con ``usage`` de tipo
    «recharge after rest»: ``parse_traits`` se lo pasa ya convertido en
    :class:`dnd_sim.rules.usage.ActionUsage` y, como no se modelan descansos,
    equivale a un **uso por combate** (lo restaura ``reset()``, igual que
    los usos de las acciones).

    A diferencia de Regeneration no decide en su propio turno: el daño se
    resuelve al momento (hook ``on_reduced_to_zero_hp``).
    """

    threshold: int = 0
    usage: ActionUsage | None = None

    def __post_init__(self) -> None:
        match = re.search(r"takes (\d+) damage or less", self.desc or "")
        if match:
            self.threshold = int(match.group(1))

    def on_reduced_to_zero_hp(self, owner: Any, amount: int,
                              damage_type: Any = None, source: Any = None,
                              crit: bool = False, ctx: Any = None,
                              rng: Any = None) -> int | None:
        if self.threshold <= 0 or int(amount or 0) > self.threshold:
            return None  # no le llega, o la descripción no es interpretable
        if self.usage is not None:
            if not self.usage.available:
                return None  # ya gastó su único uso de este combate
            self.usage.spend()
        _log_line(ctx, f"{getattr(owner, 'name', owner)} se mantiene en pie "
                       f"({self.name or 'Relentless'}): {amount} PV -> 1 PV")
        return 1

    def reset(self) -> None:
        if self.usage is not None:
            self.usage.reset()


def _es_radiante(damage_type: Any) -> bool:
    """¿El daño es radiante? (los tipos no reconocidos no lo son)."""
    try:
        return parse_damage_type(damage_type) is DamageType.RADIANT
    except Exception:
        return False


def _guardar_salvacion(owner: Any, ability: str, dc: int, rng: Any):
    """Tira una salvación con import perezoso de :mod:`dnd_sim.rules.saves`.

    El import va dentro de la función (patrón del repo) para no abrir el
    ciclo ``saves`` -> ``traits``.
    """
    from ..saves import saving_throw
    return saving_throw(owner, ability, dc, rng)


@dataclass
class UndeadFortitude(Trait):
    """Undead Fortitude (zombi, zombi ogro): salvación para no caer.

    «If damage reduces the zombie to 0 hit points, it must make a
    Constitution saving throw with a DC of 5+the damage taken, unless the
    damage is radiant or from a critical hit. On a success, the zombie
    drops to 1 hit point instead.» (API, SRD 2014)

    Es la primera consumidora del hook ``on_reduced_to_zero_hp``: se
    resuelve **al aplicar el daño** (no en el turno) y pasa por
    :func:`dnd_sim.rules.saves.saving_throw` de siempre, así que las condiciones
    y las ventajas de rasgo también cuentan en la tirada.

    La DC base (5) sale de la descripción y se le suma el daño recibido.
    Un crítico o daño radiante no dan salvación.
    """

    dc_base: int = 0

    def __post_init__(self) -> None:
        match = re.search(r"DC of (\d+)", self.desc or "")
        if match:
            self.dc_base = int(match.group(1))

    def on_reduced_to_zero_hp(self, owner: Any, amount: int,
                              damage_type: Any = None, source: Any = None,
                              crit: bool = False, ctx: Any = None,
                              rng: Any = None) -> int | None:
        if self.dc_base <= 0:
            return None  # descripción no interpretable
        if crit:
            return None  # «unless ... from a critical hit»
        if _es_radiante(damage_type):
            return None  # «unless the damage is radiant»
        if rng is None:
            return None  # sin generador no se tira: no se inventa el resultado
        dc = self.dc_base + int(amount or 0)
        resultado = _guardar_salvacion(owner, "con", dc, rng)
        if not resultado.success:
            return None
        _log_line(ctx, f"{getattr(owner, 'name', owner)} supera "
                       f"{self.name or 'Undead Fortitude'} (DC {dc}): "
                       f"queda a 1 PV")
        return 1

"""Rasgos ofensivos: mejoran los ataques del portador.

Blood Frenzy, Pack Tactics y Martial Advantage comparten los helpers de
posiciﾃｳn (:func:`aliados_capaces`, :func:`_condicion_posicional`): sin
modelo de coordenadas, la condiciﾃｳn de ﾂｫaliado a 5 ft.ﾂｻ se sortea.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .base import Trait
from ...core.dice import roll_dice
from ...core.randomness import pick
from ..roll_modifiers import AttackRange

@dataclass
class BloodFrenzy(Trait):
    """Blood Frenzy (sahuagin): ventaja cuerpo a cuerpo contra un herido.

    «The sahuagin has advantage on melee attack rolls against any creature
    that doesn't have all its hit points.» (SRD 2014)
    """

    def modify_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                                rango: Any, ctx: Any = None,
                                rng: Any = None) -> None:
        if rango is not AttackRange.MELEE:
            return  # solo ataques cuerpo a cuerpo
        max_hp = int(getattr(target, "max_hp", 0) or 0)
        hp = int(getattr(target, "hp", max_hp) or 0)
        if 0 < max_hp and hp < max_hp:
            mods.advantage_sources.append(self.name or "Blood Frenzy")


def aliados_capaces(combatiente: Any, ctx: Any) -> list[Any]:
    """Aliados de ``combatiente`` en el combate que aún pueden participar.

    Es el «aliado que no está incapacitado» de las fichas (Pack Tactics,
    Martial Advantage): ``can_act`` ya cubre "vivo y no incapacitado" y
    ``is_hostile_to`` contempla el bando y el hechizado. Sin contexto (o
    sin ``combatants``) no hay aliados que contar.
    """
    resultado: list[Any] = []
    for otro in getattr(ctx, "combatants", None) or []:
        if otro is combatiente:
            continue
        if not getattr(otro, "can_act", True):
            continue
        try:
            if combatiente.is_hostile_to(otro):
                continue
        except Exception:
            continue
        resultado.append(otro)
    return resultado


def _condicion_posicional(combatiente: Any, ctx: Any, rng: Any) -> bool:
    """¿Se cumple una condición de posición que el motor no puede mirar?

    Las fichas la expresan como «un aliado no incapacitado está a menos de
    5 pies del objetivo»: aquí **no hay modelo de posición**, así que la
    decisión se toma al azar (50 %) **solo** si el combatiente tiene
    aliados capaces; sin aliados nunca se cumple. Consume RNG únicamente
    cuando hay algo que sortear, y devuelve ``False`` si no hay con qué
    decidir (sin ``ctx`` o sin ``rng`` no se inventa un resultado).
    """
    if ctx is None or rng is None:
        return False
    if not aliados_capaces(combatiente, ctx):
        return False
    return bool(pick(rng, [True, False]))

@dataclass
class PackTactics(Trait):
    """Pack Tactics (lobo): ventaja si un aliado está cerca del objetivo.

    «The wolf has advantage on an attack roll against a creature if at
    least one of the wolf's allies is within 5 ft. of the creature and the
    ally isn't incapacitated.» (API, SRD 2014). La posición no está
    modelada, así que la condición la resuelve
    :func:`_condicion_posicional`.
    """

    def modify_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                                rango: Any, ctx: Any = None,
                                rng: Any = None) -> None:
        if _condicion_posicional(attacker, ctx, rng):
            mods.advantage_sources.append(self.name or "Pack Tactics")


@dataclass
class MartialAdvantage(Trait):
    """Martial Advantage (hobgoblin): 2d6 extra si el objetivo está cerca
    de un aliado.

    «Once per turn, the hobgoblin can deal an extra 7 (2d6) damage to a
    creature it hits with a weapon attack if that creature is within 5 ft.
    of an ally of the hobgoblin that isn't incapacitated.» (API, SRD 2014).

    Los números no vienen en un campo aparte: se leen de la descripción
    («an extra 7 (2d6)») en ``__post_init__``. La posición se resuelve como
    en Pack Tactics y el daño entra por el hook ``extra_attack_damage``,
    antes de los modificadores del objetivo.

    # TODO: el «once per turn» hoy se cumple de serie porque el hobgoblin
    # solo ataca una vez por turno; convendría acotarlo si alguna ficha
    # llega a tener Multiattack o varios ataques por turno.
    """

    dice: str = ""      # dados del extra, p. ej. «2d6»
    bonus: int = 0      # media que imprime la ficha, p. ej. 7 (informativa)

    def __post_init__(self) -> None:
        match = re.search(r"an extra (\d+) \((\d+d\d+)\)", self.desc or "")
        if match:
            self.bonus = int(match.group(1))
            self.dice = match.group(2)

    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            crit: bool = False, ctx: Any = None,
                            rng: Any = None) -> int:
        if not self.dice:
            return 0  # descripción no interpretable: el rasgo no hace nada
        if not _condicion_posicional(attacker, ctx, rng):
            return 0
        return int(roll_dice(self.dice, rng, crit=crit))

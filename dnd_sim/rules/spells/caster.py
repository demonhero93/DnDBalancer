"""Lanzamiento de hechizo de un PJ: estadísticas, espacios y acción Magia.

El componente :class:`PCSpellcasting` guarda la característica, los
datos de lanzamiento (CD = 8 + PB + mod; ataque = PB + mod), los
trucos conocidos, los hechizos preparados y los :class:`SpellSlots`.
La acción :class:`PJSpellAction` es la que se mete en ``pj.actions``
con ``ActionType.ACTION`` (la acción Magia): al ejecutarse elige el
espacio con ``pick`` (sobrecarga uniforme, sin RNG con una sola
opción), lo gasta y construye la acción interna con
:func:`spell_action` pasando **el** ``Spellcasting`` del PJ, de modo que
CD y bonificador son los suyos sin tocar el camino de los monstruos.

Los monstruos con ``Spellcasting`` de ficha no pasan por aquí: sus
acciones siguen construyéndose en ``data/spell_parser.py`` con sus
datos fijos (suite idéntica).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ...core.randomness import pick
from ...core.spellcasting import SpellSlots
from ...model.actions import ActionType, CombatAction
from ..usage import ActionUsage
from .casting import Spell, Spellcasting, spell_action


@dataclass
class PCSpellcasting:
    """Componente de lanzamiento de un PJ (no es ``Trait``: sin hooks).

    - ``ability``: característica de lanzamiento (``"int"``...).
    - ``level``: nivel del personaje (escala los trucos al parsear la
      lista con este nivel).
    - ``sc``: :class:`Spellcasting` con la CD y el bonificador del PJ
      (lo que pasa a ``spell_action``).
    - ``slots``: espacios (el mismo objeto que ``Combatant.spell_slots``,
      que ``reset()`` restaura).
    - ``trucos`` / ``preparados``: listas fijas al crear el PJ.
    """

    ability: str
    level: int
    sc: Spellcasting
    slots: SpellSlots
    trucos: list[Spell] = field(default_factory=list)
    preparados: list[Spell] = field(default_factory=list)


def estadisticas_lanzador(pj: Any, caracteristica: str,
                          nivel: int) -> Spellcasting:
    """CD y bonificador del PJ: ``8 + PB + mod`` y ``PB + mod``.

    Usa la competencia y las características del propio personaje; los
    monstruos no pasan por aquí (siguen con los de su ficha).
    """
    mod = int(pj.abilities.mod(caracteristica))
    pb = int(getattr(pj, "proficiency", 0) or 0)
    return Spellcasting(
        ability=str(caracteristica),
        save_dc=8 + pb + mod,
        attack_bonus=pb + mod,
        level=int(nivel),
        ability_mod=mod,
    )


@dataclass
class PJSpellAction(CombatAction):
    """Acción Magia de un PJ (``ActionType.ACTION``).

    ``es_accion_magia`` la marca para que la Oleada de Acción no pueda
    elegirla en su acción extra (A7). Sin espacio disponible no es
    elegible (``can_use`` sin RNG) y al ejecutarse gasta el espacio que
    ``pick`` elija entre los de nivel >= que el del hechizo.
    """

    spell: Any = None
    caster: Any = None            # PCSpellcasting
    action_type: ActionType = ActionType.ACTION
    name: str = "Hechizo"
    usage: ActionUsage | None = None
    es_accion_magia: bool = True

    def __post_init__(self) -> None:
        if self.spell is not None:
            self.name = str(getattr(self.spell, "name", "") or self.name)

    def construir(self, slot_level: int | None = None) -> Any:
        """Acción interna con la CD/bonificador del PJ (sin RNG)."""
        return spell_action(self.spell, self.caster.sc,
                            slot_level=slot_level)

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        # Recursos de turno, combatiente vivo y uso (heredado).
        if not super().can_use(*args, **kwargs):
            return False
        if self.spell is None or self.caster is None:
            return False
        # Espacio >= que el del hechizo (truco: siempre; sin RNG).
        nivel = int(getattr(self.spell, "level", 0) or 0)
        if not self.caster.slots.can_cast(nivel):
            return False
        # Restricciones del efecto (aliado herido, objetivos...).
        interno = self.construir()
        return bool(interno is not None and interno.can_use(*args, **kwargs))

    def execute(self, context: Any) -> None:
        nivel = int(getattr(self.spell, "level", 0) or 0)
        slot: int | None = None
        if nivel >= 1:
            disponibles = self.caster.slots.niveles_disponibles(nivel)
            if not disponibles:
                return              # sin espacios: no gasta nada
            slot = pick(context.rng, disponibles)  # 1 opción = sin RNG
            self.caster.slots.spend(slot)
        interno = self.construir(slot)
        if interno is None:
            return
        interno.execute(context)


def construir_acciones(caster: PCSpellcasting) -> list[PJSpellAction]:
    """Una acción Magia por truco conocido y hechizo preparado."""
    return [PJSpellAction(spell=s, caster=caster)
            for s in [*caster.trucos, *caster.preparados]]


__all__ = ["PCSpellcasting", "PJSpellAction", "construir_acciones",
           "estadisticas_lanzador"]

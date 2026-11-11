"""Subclase Champion (Campeón, PHB 2024) del Guerrero.

Rasgos por nivel (Fighter 3 / 7 / 10 / 15 / 18):

- **Improved Critical** (3): las tiradas de ataque con arma pueden ser
  un Impacto Crítico con 19 o 20 en el d20. El umbral lo consulta el
  motor con ``ChampionFeatures.umbral_critico`` (helper
  ``evaluar_d20``/``umbral_critico`` de ``rules/roll_modifiers.py``;
  ver A3 en ``TODO.md``). Un 1 natural sigue fallando siempre y los
  ataques de hechizo no usan el umbral (campo ``spell_attack``).
- **Remarkable Athlete** (3): ventaja en iniciativa
  (``ventaja_iniciativa()``, duck-typing en ``roll_initiative``) y en
  pruebas de Atletismo (``modify_check_modifiers``, patrón Furia);
  ambas se anulan con desventaja por la regla estándar. No concede
  competencia en Atletismo. Moverse hasta la mitad de la velocidad
  tras un crítico es dato sin efecto (``# TODO``: sin movimiento).
- **Additional Fighting Style** (7): un segundo Estilo de Combate,
  elegido con ``pick`` o con el kwarg ``additional_fighting_style``
  validado (en A5, junto con la propiedad ``estilos``).
- **Heroic Warrior** (10): gana Inspiración Heroica al inicio de cada
  turno si no la tiene → dato sin efecto (el sim no modela la
  Inspiración Heroica); congelado con test freeze.
- **Superior Critical** (15): el umbral crítico baja a 18.
- **Survivor** (18): **Defy Death** (ventaja y 18-20 en salvaciones de
  muerte) → dato sin efecto (sin salvaciones de muerte: un PJ a 0 PG
  muere o queda fuera), congelado con test freeze. **Heroic Rally**
  (A6): al inicio de cada turno propio, si está Bloodied
  (``pg * 2 <= pg_max``) y con al menos 1 PG, recupera
  ``heroic_rally_amount(mod CON)`` PG sin pasar de los máximos.

Registro: clave ``"champion"`` en ``fighter/__init__.py``. Ver
``TODO.md`` (plan «Champion») y las entradas de
``PASOS-ANTERIORES.txt``.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from .....core.classes import (
    FIGHTER_STYLES,
    MAX_LEVEL,
    MIN_LEVEL,
)
from ....traits.base import Trait
from ..features import FighterFeatures

#: RNG con semilla fija para elegir el segundo Estilo de Combate cuando
#: el llamante no pasa ``rng``: crea el personaje siempre igual
#: (reproducible, patrón del resto de subclases).
_RNG_CREACION = random.Random(0)


def _de(actor: Any, clase: type) -> Any:
    """Primer trait de ``clase`` que lleve ``actor`` (o ``None``)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


@dataclass
class ChampionFeatures(Trait):
    """Rasgos de la subclase Champion y sus datos de ficha.

    Sin estado de combate propio hasta Heroic Rally (A6): el ciclo de
    vida ``reset``/``on_turn_start`` lo heredado del :class:`Trait`
    basta hasta entonces.
    """

    # Nivel del personaje (manda en las tablas de rasgos).
    level: int = MIN_LEVEL
    # Datos sin efecto congelados (decisión del maintainer): Heroic
    # Warrior (10, sin Inspiración Heroica en el modelo) y Defy Death
    # (18, sin salvaciones de muerte). El movimiento tras un crítico de
    # Remarkable Athlete también es dato sin efecto (sin movimiento).
    heroic_warrior: bool = True
    defy_death: bool = True
    # Dueño (guards de hooks y despacho de ``on_turn_start``).
    owner: Any = field(default=None, repr=False, compare=False)


def apply_champion(pj: Any, level: int | None = None,
                   rng: random.Random | None = None,
                   additional_fighting_style: str | None = None
                   ) -> ChampionFeatures:
    """Aplica la subclase Champion a un PJ Guerrero.

    Exige que ``pj`` ya tenga :class:`FighterFeatures`
    (:func:`apply_fighter`) y nivel >= 3. ``additional_fighting_style``
    (Additional Fighting Style) se VALIDA aquí: debe ser un Estilo de
    ``FIGHTER_STYLES`` y distinto del que ya tiene el PJ; su elección
    con ``pick``/aplicación de efectos llega en A5 (el kwarg todavía
    no se aplica). ``rng`` por defecto con semilla 0 (patrón del
    resto de subclases); hasta A5 no consume azar.
    """
    if _de(pj, FighterFeatures) is None:
        raise ValueError(
            "Primero aplica la clase guerrero con apply_fighter(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    if lvl < 3:
        raise ValueError(
            f"Champion requiere nivel >= 3: llegó {lvl}."
        )
    if additional_fighting_style is not None:
        if additional_fighting_style not in FIGHTER_STYLES:
            raise ValueError(
                f"{additional_fighting_style!r} no es un Estilo de "
                f"Combate de la clase Guerrero: opciones "
                f"{sorted(FIGHTER_STYLES)}."
            )
        primero = _de(pj, FighterFeatures).estilo
        if additional_fighting_style == primero:
            raise ValueError(
                "Additional Fighting Style repite el Estilo de Combate "
                f"que ya tiene el PJ ({primero!r}): una dote no se toma "
                "dos veces."
            )
    # Elección con pick y mutaciones del segundo estilo (Defense): A5.
    trait = ChampionFeatures(name="Champion", level=lvl)
    trait.owner = pj
    pj.traits.append(trait)
    return trait


__all__ = ["ChampionFeatures", "apply_champion"]

"""Subclase Eldritch Knight (Caballero Sobrenatural, PHB 2024).

Rasgos por nivel (Fighter 3 / 7 / 10 / 15 / 18):

- **Spellcasting** (3): característica INTELIGENCIA, lista de clase
  ``wizard``, progresión **tercio** con las tablas de
  ``core/classes.py`` (``eldritch_knight_prepared`` /
  ``eldritch_knight_cantrips``). **Sin restricción de escuelas**
  (decisión del maintainer): si se confirma evocación/abjuración,
  reactivar el parámetro ``escuelas`` de ``ELDRITCH_KNIGHT_SPELLS``
  aquí. Trucos y hechizos se eligen al crear el PJ con la mecánica
  común (``aplicar_lanzamiento`` → ``preparar_hechizos``), solo del
  pool soportado por el motor.
- **War Bond** (3): **dato sin efecto** (el sim no modela desarme ni
  invocación del arma vinculada; congelado con test).
- **War Magic** (7) — **versión PHB 2024 (decisión del maintainer)**:
  al tomar la acción Atacar, cada ataque puede sustituirse por el
  lanzamiento de un truco de tiempo de lanzamiento una acción (punto
  de consulta ``sustituir_ataque_por_hechizo``, ver A4); consume ese
  ataque y no gasta espacio. La acción sigue siendo una sola, así que
  no toca la restricción de Oleada.
- **Eldritch Strike** (10): +1 truco conocido (tabla de
  ``core/classes.py``) y marca de desventaja en la siguiente salvación
  del objetivo contra un hechizo del dueño (A6).
- **Arcane Charge** (15): **dato sin efecto** (sin movimiento; el
  teletransporte de Oleada no se modela; congelado con test).
- **Improved War Magic** (18) — **versión PHB 2024**: sustituir DOS
  ataques por un hechizo de nivel 1-2 (A5).

Registro: clave ``"eldritch_knight"`` en ``fighter/__init__.py``
(``SubclassDef`` con ``spellcasting=ELDRITCH_KNIGHT_SPELLS``). Ver
``TODO.md`` (plan «Eldritch Knight») y las entradas de
``PASOS-ANTERIORES.txt``.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .....core.classes import (
    MAX_LEVEL,
    MIN_LEVEL,
    eldritch_knight_cantrips,
    eldritch_knight_prepared,
)
from .....core.randomness import pick
from .....core.spellcasting import SpellcastingDef
from ....spells import aplicar_lanzamiento
from ....spells.caster import PJSpellAction
from ....traits.base import Trait
from ..features import FighterFeatures

#: Definición de lanzamiento del Eldritch Knight (PHB 2024): tercio,
#: INT, lista ``wizard``, nivel mínimo 3 y **sin restricción de
#: escuelas** (decisión del maintainer: aquí se reactivaría
#: ``escuelas=("evocation", "abjuration")`` si la regla se confirma).
#: Los conteos salen de las funciones de ``core/classes.py`` (una sola
#: fuente: si se corrige la tabla, se corrige allí).
ELDRITCH_KNIGHT_SPELLS = SpellcastingDef(
    progresion="third",
    caracteristica="int",
    lista_clase="wizard",
    trucos_conocidos={lvl: eldritch_knight_cantrips(lvl)
                     for lvl in range(MIN_LEVEL, MAX_LEVEL + 1)},
    preparados={lvl: eldritch_knight_prepared(lvl)
                for lvl in range(MIN_LEVEL, MAX_LEVEL + 1)},
    escuelas=None,
    min_level=3,
)


def _de(actor: Any, clase: type) -> Any:
    """Primer trait de ``clase`` que lleve ``actor`` (o ``None``)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


@dataclass
class EldritchKnightFeatures(Trait):
    """Rasgos de la subclase Eldritch Knight.

    ``strike_marks`` es la marca de Eldritch Strike por objetivo con
    caducidad (A6, patrón Vex). ``war_bond`` y ``arcane_charge`` son
    **datos sin efecto** congelados con test: el motor no modela
    desarme, invocación de armas ni movimiento/teletransporte.
    """

    level: int = MIN_LEVEL
    strike_marks: dict[str, int] = field(default_factory=dict)
    war_bond: bool = True
    arcane_charge: bool = True

    def sustituir_ataque_por_hechizo(self, restantes: int, ctx: Any) -> Any:
        """War Magic (7), PHB 2024: sustituir UN ataque por un truco.

        Un ``pick`` «no»/«sí» por ataque elegible y, si sí, ``pick``
        uniforme entre los trucos lanzables (1 opción = sin RNG).
        Devuelve ``(accion, coste)`` con coste 1 o ``None`` **sin RNG**
        cuando no es elegible (nivel < 7, sin trucos, fuera de la acción
        Atacar). El pool ``hechizo_soportado`` ya garantiza hechizos de
        tiempo de lanzamiento una acción: sin filtro extra de escuelas
        ni de tiempo aquí. La acción Atacar sigue siendo una sola, así
        que esto NO activa la restricción de Oleada; dentro de la pasada
        extra de la Oleada sí puede disparar (decisión documentada: la
        restricción solo excluye la acción Magia como acción extra).
        """
        if getattr(ctx, "is_reaction", False):
            return None  # solo la acción Atacar (patrón Rapid Strike)
        if not getattr(ctx, "in_attack_action", False):
            return None
        if self.level < 7:
            return None
        owner = self.owner
        if owner is None:
            return None
        acciones = getattr(owner, "actions", None) or []
        trucos = [a for a in acciones
                  if isinstance(a, PJSpellAction)
                  and int(getattr(a.spell, "level", 0) or 0) == 0
                  and a.can_use(ctx)]
        if not trucos:
            return None  # sin trucos elegibles: cero RNG
        eleccion = pick(ctx.rng, ["no", "truco"])
        if eleccion == "no":
            return None
        return pick(ctx.rng, trucos), 1


def apply_eldritch_knight(
    pj: Any,
    level: int | None = None,
    *,
    lista: Any = None,
    rng: Any = None,
    cantrips: Any = None,
    spells: Any = None,
) -> EldritchKnightFeatures:
    """Aplica la subclase Eldritch Knight a ``pj`` (guerrero, nivel >= 3).

    ``lista`` es la ``ClassSpellList`` que aporta el cargador de datos
    (``rules`` no importa ``data``); sin ella solo se crean los
    espacios (cero hechizos preparados). ``cantrips``/``spells`` son
    los kwargs explícitos de ``preparar_hechizos`` y se validan allí
    (``ValueError`` si repiten, exceden el conteo o no están en el pool
    legal). ``rng`` por defecto con semilla 0 (creación reproducible).
    """
    if _de(pj, FighterFeatures) is None:
        raise ValueError(
            "Primero aplica la clase guerrero con apply_fighter(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    if lvl < 3:
        raise ValueError(
            f"Eldritch Knight requiere nivel >= 3: llegó {lvl}."
        )
    aplicar_lanzamiento(
        pj, lvl, ELDRITCH_KNIGHT_SPELLS,
        [] if lista is None else lista,
        rng=rng, trucos=cantrips, hechizos=spells,
    )
    trait = EldritchKnightFeatures(name="Eldritch Knight", level=lvl)
    trait.owner = pj
    pj.traits.append(trait)
    return trait


__all__ = ["ELDRITCH_KNIGHT_SPELLS", "EldritchKnightFeatures",
           "apply_eldritch_knight"]

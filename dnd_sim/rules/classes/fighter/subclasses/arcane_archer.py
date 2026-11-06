"""Subclase Arcane Archer (Arquero Arcano, XGE) del Fighter.

Concentra en un único rasgo agregado (:class:`ArcaneArcherFeatures`)
las features de la subclase. :func:`apply_arcane_archer` monta el
personaje (exige que ``pj`` ya tenga :class:`FighterFeatures`).

Decisiones de simulación documentadas:

- **Arcane Archer Lore** (3): competencia en Arcanos o Naturaleza
  elegida con ``pick`` uniforme; el truco Prestidigitación/Druidismo se
  guarda como dato (sin utilidad en el sim).
- **Arcane Shot**: las opciones conocidas se eligen al crear el PJ con
  ``sample`` del pool :data:`ARCANE_SHOTS` (cuenta según el nivel);
  admite kwarg explícito ``arcane_shots`` validado (patrón
  ``fighting_style``). Piercing y Seeking quedan fuera del pool: sus
  ataques sin tirada reemplazarían el flujo de ataque del motor (ver
  TODO.md).
- **Ever-Ready Shot** (10): sin efecto (cada combate empieza con usos
  completos); dato de tabla.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from .....core.classes import MAX_LEVEL, MIN_LEVEL, arcane_shot_options_known
from .....core.randomness import pick, sample
from ....traits.base import Trait
from ..features import FighterFeatures

#: Pool de opciones de Arcane Shot implementadas (XGE). Piercing y
#: Seeking no están: reemplazan la tirada de ataque (ver TODO.md).
ARCANE_SHOTS: tuple[str, ...] = (
    "Banishing Arrow",
    "Beguiling Arrow",
    "Bursting Arrow",
    "Enfeebling Arrow",
    "Grasping Arrow",
    "Shadow Arrow",
)

#: Competencias que da Arcane Archer Lore (XGE: Arcanos o Naturaleza).
ARCANE_ARCHER_SKILLS: tuple[str, ...] = ("arcana", "nature")

#: Trucos de Arcane Archer Lore (dato sin efecto en el sim).
ARCANE_ARCHER_CANTRIPS: tuple[str, ...] = ("Prestidigitación", "Druidismo")

#: RNG con semilla fija para Lore y opciones cuando no pasa ``rng``:
#: crea el personaje siempre igual (reproducible).
_RNG_CREACION = random.Random(0)


def _de(actor: Any, clase: type) -> Any:
    """Primer rasgo de ``actor`` que sea instancia de ``clase`` (o None)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


@dataclass
class ArcaneArcherFeatures(Trait):
    """Features de la subclase y estado de Arcane Shot."""

    # Nivel del personaje (manda en las tablas de la subclase).
    level: int = MIN_LEVEL
    #: Competencia ganada con Lore ("arcana" o "nature").
    competencia: str = ""
    #: Truco aprendido con Lore (dato sin efecto).
    truco: str = ""
    #: Opciones de Arcane Shot conocidas (nombres de :data:`ARCANE_SHOTS`).
    opciones_conocidas: list[str] = field(
        default_factory=list, repr=False, compare=False)
    #: Dueño (para que ``reset`` pueda apagar los flags en el combatiente).
    owner: Any = field(default=None, repr=False, compare=False)


def apply_arcane_archer(pj: Any, level: int | None = None,
                        arcane_shots: tuple[str, ...] | None = None,
                        rng: Any = None) -> ArcaneArcherFeatures:
    """Aplica la subclase Arcane Archer a un PJ Guerrero.

    Exige que ``pj`` ya tenga :class:`FighterFeatures`
    (:func:`apply_fighter`). Añade el trait con Arcane Archer Lore
    (competencia y truco) y las opciones de Arcane Shot conocidas según
    el nivel (o las explícitas del kwarg ``arcane_shots``).
    """
    if _de(pj, FighterFeatures) is None:
        raise ValueError(
            "Primero aplica la clase guerrero con apply_fighter(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    generador = rng if rng is not None else _RNG_CREACION

    # Arcane Archer Lore (3): competencia y truco con pick uniforme.
    competencia = pick(generador, ARCANE_ARCHER_SKILLS)
    truco = pick(generador, ARCANE_ARCHER_CANTRIPS)
    pj.skill_proficiencies = set(pj.skill_proficiencies or set()) | {competencia}

    # Arcane Shot: N opciones conocidas (sample) o las explícitas.
    n = arcane_shot_options_known(lvl)
    if arcane_shots is None:
        opciones = list(sample(generador, ARCANE_SHOTS, n))
    else:
        opciones = list(arcane_shots)
        invalidas = [s for s in opciones if s not in ARCANE_SHOTS]
        if invalidas:
            raise ValueError(
                f"{invalidas!r} no es una opción de Arcane Shot: "
                f"opciones {sorted(ARCANE_SHOTS)}."
            )
        if len(opciones) != n:
            raise ValueError(
                f"se esperaban {n} opciones de Arcane Shot para el nivel "
                f"{lvl} y llegaron {len(opciones)}."
            )

    trait = ArcaneArcherFeatures(
        name="Arcane Archer",
        level=lvl,
        competencia=competencia,
        truco=truco,
        opciones_conocidas=opciones,
    )
    trait.owner = pj
    pj.traits.append(trait)
    return trait


__all__ = ["ARCANE_ARCHER_CANTRIPS", "ARCANE_ARCHER_SKILLS", "ARCANE_SHOTS",
           "ArcaneArcherFeatures", "apply_arcane_archer"]

"""Clase Fighter (Guerrero, PHB 2024), sin subclases.

Concentra en un único rasgo agregado (:class:`FighterFeatures`) todas
las features de clase que dependen de tiradas o decisiones, más las
acciones bonus de la clase. :func:`apply_fighter` monta el personaje
completo (salvaciones, habilidades, Extra Attack, estilo...) a partir de
su nivel.

Uso::

    from dnd_sim.rules.classes.fighter import apply_fighter
    apply_fighter(pj, skills=("athletics", "perception"), level=5)
    # o vía el registro genérico:
    from dnd_sim.rules.classes import apply_class
    apply_class(pj, "fighter", skills=("athletics",), level=5)

Decisiones de simulación documentadas:

- **Competencias** (armas sencillas y marciales, armaduras ligeras,
  medias y pesadas, escudos): el modelo de PJ no tiene campos de
  competencia de arma/armadura, así que no se registran (mismo criterio
  que el resto de clases).
- Las decisiones con azar (estilo de combate, Second Wind, Action
  Surge, Indomitable...) se toman con ``core.randomness.pick`` uniforme
  y no consumen RNG cuando solo hay una opción.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ....core.classes import FIGHTER_SKILLS, MAX_LEVEL, MIN_LEVEL
from ....core.skills import normalize_skill
from ...traits.base import Trait


@dataclass
class FighterFeatures(Trait):
    """Features de clase del Fighter/Guerrero y su estado.

    Un solo rasgo agregado reutiliza el despacho de hooks existente en
    vez de una clase por feature. El estado por combate se limpia en
    ``reset``.
    """

    # Nivel del personaje (manda en las tablas de features).
    level: int = MIN_LEVEL
    # Dueño (para que ``reset`` pueda apagar los flags en el combatiente).
    owner: Any = field(default=None, repr=False, compare=False)

    # --- Reinicio -----------------------------------------------------------
    def reset(self) -> None:
        """Sin estado persistente entre combates por ahora."""


# --- Aplicación de la clase a un PJ ------------------------------------------

def apply_fighter(pj: Any, skills: tuple[str, ...] = (),
                  level: int | None = None) -> FighterFeatures:
    """Aplica la clase Fighter (Guerrero) a ``pj`` según su nivel.

    - Salvaciones: FUE y CON.
    - ``skills``: validadas contra la lista de la clase (ValueError si no
      está; el recuento de elecciones lo decide quien llama).
    - Añade el rasgo :class:`FighterFeatures`; el resto de rasgos y
      acciones se añaden en los pasos siguientes de esta sesión.
    """
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))

    pj.save_proficiencies = set(pj.save_proficiencies or set()) | {"str", "con"}

    if skills:
        validas = set(FIGHTER_SKILLS)
        nuevas = set()
        for raw in skills:
            name = normalize_skill(raw)
            if name not in validas:
                raise ValueError(
                    f"{name!r} no es una habilidad de la clase Guerrero: "
                    f"opciones {sorted(validas)}."
                )
            nuevas.add(name)
        pj.skill_proficiencies = set(pj.skill_proficiencies or set()) | nuevas

    trait = FighterFeatures(name="Guerrero", level=lvl)
    trait.owner = pj
    pj.traits = list(getattr(pj, "traits", None) or []) + [trait]
    return trait


__all__ = ["FighterFeatures", "apply_fighter"]

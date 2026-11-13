"""Subclase Rune Knight (Caballero de las Runas, TCE) del Guerrero.

Rasgos por nivel (Fighter 3 / 7 / 10 / 15 / 18):

- **Bonus Proficiencies** (3): herramientas de herrero e idioma
  gigante → dato sin efecto (el modelo no lleva herramientas ni
  idiomas).
- **Rune Carver** (3): runas conocidas — ``sample`` del pool ``RUNES``
  (2/3/4/5 según nivel; tabla ``runes_known_count``), kwarg explícito
  ``runes`` validado (patrón maniobras de Battle Master) y ``rng`` por
  defecto con semilla 0. Cada runa se invoca **una vez por combate**
  (``rune_uses``: 1; 2 con Master of Runes, 15+). CD de runas y de
  Fire/Stone: 8 + PB + mod CON.
- **Giant's Might** (3): acción adicional; durante 1 minuto (= todo el
  combate) te vuelves Grande (patrón Giant Stature, ``size_base``),
  ventaja en pruebas y salvaciones de FUE (consulta de A3) y daño
  extra 1d6 (d8 desde 10, d10 desde 18; ``giants_might_die_sides``)
  una vez por turno. Usos = PB (``giants_might_uses``).
- **Runic Shield** (7): reacción que fuerza al atacante de un aliado
  impactado a repetir el d20. Usos = PB (``runic_shield_uses``).
- **Great Stature** (10): crecer 3d4 pulgadas → dato sin efecto; solo
  sube el dado de Giant's Might a d8.
- **Master of Runes** (15): dos invocaciones por runa.
- **Runic Juggernaut** (18): tamaño Enorme y alcance +5 ft (dato sin
  efecto), dado d10.

Runas con efecto (A7-A11): **frost** (+2 a pruebas/salvaciones de
FUE y CON), **hill** (resistencias temporales a F/P/C + resistencia
pasiva a veneno), **fire** (daño extra y Restringido), **stone**
(Hechizado al terminar su turno), **storm** (ventaja/desventaja) y
**cloud** (redirige el golpe). Los pasivos de las runas (salvo la
resistencia a veneno de Hill), Bonus Proficiencies, el crecimiento de
Great Stature, el alcance extra, la velocidad 0 de Stone y el
despertar de un tercero son datos sin efecto.

Registro: clave ``"rune_knight"`` en ``fighter/__init__.py``. Ver
``TODO.md`` (plan «Rune Knight») y las entradas de
``PASOS-ANTERIORES.txt``.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from .....core.classes import (
    MAX_LEVEL,
    MIN_LEVEL,
    RUNES,
    giants_might_uses,
    rune_uses,
    runes_known_count,
    runic_shield_uses,
)
from .....core.randomness import sample
from ....traits.base import Trait
from ..features import FighterFeatures

#: Creación reproducible (patrón de todas las subclases de Fighter).
_RNG_CREACION = random.Random(0)


def _de(actor: Any, clase: type) -> Any:
    """Primer trait de ``clase`` que lleve ``actor`` (o ``None``)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


@dataclass
class RuneKnightFeatures(Trait):
    """Rasgos, runas y estados de Rune Knight.

    Sin RNG en los guards: los ``pick`` de invocación de runas se
    deciden en sus puntos de consulta con el ``rng`` del combate.
    """

    # Nivel del personaje (manda en las tablas de rasgos).
    level: int = MIN_LEVEL
    # Runas conocidas (2/3/4/5 según nivel; pool ``RUNES``).
    runas: list[str] = field(default_factory=list, repr=False,
                             compare=False)
    # Usos restantes por runa (1; 2 con Master of Runes, 15+).
    usos_runa: dict = field(default_factory=dict, repr=False,
                            compare=False)
    # Giant's Might (3): usos por descanso largo + «una vez por turno»
    # del daño extra (flag se reinicia en ``on_turn_start``).
    giants_might_usos: int = 0
    giants_might_used_this_turn: bool = False
    # Runic Shield (7): usos por descanso largo; la reacción compartida
    # vive en ``state.reaction_used``.
    runic_shield_usos: int = 0
    # Estados activos de runas (duración = combate; los limpia
    # ``reset``). Fire/Stone marcan objetivos en ``CombatState`` (A8/A9).
    frost_activo: bool = False
    hill_activo: bool = False
    storm_activo: bool = False
    # Datos sin efecto congelados (decisión del maintainer): pasivos de
    # las runas (salvo la resistencia a veneno de Hill, A7) y Bonus
    # Proficiencies (herramientas de herrero e idioma gigante).
    pasivos_runas: bool = True
    bonus_proficiencies: bool = True
    # Dueño (guards de hooks y despacho de ``on_turn_start``).
    owner: Any = field(default=None, repr=False, compare=False)

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        # «Una vez por turno» de Giant's Might (A4): se reinicia al
        # empezar el turno.
        self.giants_might_used_this_turn = False

    def reset(self) -> None:
        """Un combate nuevo = un día descansado: usos restaurados."""
        self.usos_runa = {r: rune_uses(self.level) for r in self.runas}
        self.giants_might_usos = giants_might_uses(self.level)
        self.giants_might_used_this_turn = False
        self.runic_shield_usos = runic_shield_uses(self.level)
        self.frost_activo = False
        self.hill_activo = False
        self.storm_activo = False


def apply_rune_knight(pj: Any, level: int | None = None,
                      runes: tuple[str, ...] | None = None,
                      rng: random.Random | None = None
                      ) -> RuneKnightFeatures:
    """Aplica la subclase Rune Knight a un PJ Guerrero.

    Exige que ``pj`` ya tenga :class:`FighterFeatures`
    (:func:`apply_fighter`) y nivel >= 3. Elige las runas conocidas
    con ``sample`` del pool ``RUNES`` (o las explícitas del kwarg
    ``runes``, validadas por nombre y recuento). ``rng`` por defecto
    con semilla 0 (patrón de las demás subclases): la creación es
    reproducible.
    """
    if _de(pj, FighterFeatures) is None:
        raise ValueError(
            "Primero aplica la clase guerrero con apply_fighter(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    if lvl < 3:
        raise ValueError(
            f"Rune Knight requiere nivel >= 3: llegó {lvl}."
        )
    generador = rng if rng is not None else _RNG_CREACION

    # Runas conocidas: N del pool (sample) o las explícitas.
    n = runes_known_count(lvl)
    if runes is None:
        elegidas = list(sample(generador, RUNES, n))
    else:
        elegidas = list(runes)
        invalidas = [r for r in elegidas if r not in RUNES]
        if invalidas:
            raise ValueError(
                f"{invalidas!r} no es una runa de Rune Knight: "
                f"opciones {sorted(RUNES)}."
            )
        if len(elegidas) != n:
            raise ValueError(
                f"se esperaban {n} runas para el nivel {lvl} y "
                f"llegaron {len(elegidas)}."
            )

    trait = RuneKnightFeatures(
        name="Rune Knight",
        level=lvl,
        runas=elegidas,
        usos_runa={r: rune_uses(lvl) for r in elegidas},
        giants_might_usos=giants_might_uses(lvl),
        runic_shield_usos=runic_shield_uses(lvl),
    )
    trait.owner = pj
    pj.traits.append(trait)
    return trait


__all__ = ["RuneKnightFeatures", "apply_rune_knight"]

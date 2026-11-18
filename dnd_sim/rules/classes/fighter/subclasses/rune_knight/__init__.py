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

from ......core.classes import (
    MAX_LEVEL,
    MIN_LEVEL,
    RUNES,
    giants_might_uses,
    rune_uses,
    runes_known_count,
    runic_shield_uses,
)
from ......core.enums import DamageType
from ......core.randomness import sample
from ..._util import _de
from ...features import FighterFeatures
from .actions import GiantsMightAction, RuneInvokeAction
from .features import RuneKnightFeatures

#: Creación reproducible (patrón de todas las subclases de Fighter).
_RNG_CREACION = random.Random(0)

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

    # Pasivo de Hill: resistencia permanente a veneno (solo si se
    # conoce la runa; sin acumular si ya la tenía, patrón Guarded
    # Mind). La ventaja en salvaciones contra veneno NO se modela: el
    # motor no distingue «salvación contra veneno» (dato sin efecto).
    if "hill" in elegidas and DamageType.POISON not in pj.resistances:
        pj.resistances = set(pj.resistances) | {DamageType.POISON}

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
    # Acción adicional de Giant's Might (elegibilidad sin RNG).
    pj.actions.append(GiantsMightAction())
    # Invocaciones de runa (A7): una acción bonus por runa de efecto
    # continuo conocida (Fire/Stone/Cloud son reacciones, A8/A9/A11).
    for runa in ("frost", "hill", "storm"):
        if runa in elegidas:
            pj.actions.append(RuneInvokeAction(runa))
    return trait


__all__ = ["GiantsMightAction", "RuneInvokeAction", "RuneKnightFeatures",
           "apply_rune_knight"]

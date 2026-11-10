"""Subclase Cavalier (Caballero, XGE) del Guerrero.

Rasgos por nivel (Fighter 3 / 7 / 10 / 15 / 18):

- **Bonus Proficiency** (3): competencia en una habilidad de
  :data:`~dnd_sim.core.classes.CAVALIER_BONUS_SKILLS` que el PJ no
  tenga todavía (``pick`` uniforme; sin candidatas, sin cambio y sin
  RNG). El idioma alternativo del rasgo es dato sin efecto (el sim no
  modela idiomas).
- **Born to the Saddle** (3): ventaja en salvaciones para no caer de
  la montura, caída de pie y montar/desmontar barato → dato sin
  efecto (el sim no modela monturas ni caídas); congelado en tests.
- **Unwavering Mark** (3): marca tras impactar con arma cuerpo a
  cuerpo (``after_attack_roll``), desventaja en ``consumir_marcas``
  (campo propio ``marca_cavalier`` en ``CombatState``).

El resto de rasgos (ataque especial de la marca, Warding Maneuver,
Hold the Line, Ferocious Charger y Vigilant Defender) se implementa en
los pasos A4-A8 de la misma sesión; ver ``TODO.md`` (plan «Cavalier»)
y las entradas de ``PASOS-ANTERIORES.txt``.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from .....core.classes import (
    CAVALIER_BONUS_SKILLS,
    CHARGE_MOVE_PROBABILITY,
    MAX_LEVEL,
    MIN_LEVEL,
    cavalier_mark_uses,
    warding_maneuver_uses,
)
from .....core.enums import AttackRange
from .....core.randomness import pick
from ....traits.base import Trait
from ....usage import ActionUsage, UsageKind
from ..features import FighterFeatures

#: RNG con semilla fija para Bonus Proficiency cuando no pasa ``rng``:
#: crea el personaje siempre igual (reproducible), patrón Battle Master.
_RNG_CREACION = random.Random(0)


def _de(actor: Any, clase: type) -> Any:
    """Primer rasgo de ``clase`` del combatiente (``None`` si no hay)."""
    for rasgo in getattr(actor, "traits", None) or ():
        if isinstance(rasgo, clase):
            return rasgo
    return None


@dataclass
class CavalierFeatures(Trait):
    """Features de la subclase Cavalier y su estado."""

    #: Nivel del personaje (manda en las tablas de la subclase).
    level: int = MIN_LEVEL
    #: Usos de Unwavering Mark por descanso (se crean en ``apply_cavalier``).
    marca_usos: ActionUsage | None = field(
        default=None, repr=False, compare=False)
    #: Usos de Warding Maneuver (nivel 7+; ``None`` por debajo).
    warding_usos: ActionUsage | None = field(
        default=None, repr=False, compare=False)
    #: Habilidad ganada con Bonus Proficiency ("" sin candidatas).
    competencia: str = ""
    #: Born to the Saddle (3): dato sin efecto (sin monturas ni caídas).
    born_to_the_saddle: bool = True
    #: Probabilidad de la carga de Ferocious Charger (CLI ``--charge-p``).
    charge_probability: float = CHARGE_MOVE_PROBABILITY
    #: Contador de turnos propios (caducidad de marcas/flags, patrón
    #: ``FighterFeatures.turno_guerrero``).
    turno_cavalier: int = 0
    #: ¿Se evaluó ya la carga este turno? (Ferocious Charger; se
    #: limpia en ``on_turn_start``).
    carga_evaluada: bool = False
    #: Dueño (para que ``reset``/hooks encuentren al combatiente).
    owner: Any = field(default=None, repr=False, compare=False)

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        # Contador de turnos propios y flag «una vez por turno» de la
        # carga (Ferocious Charger).
        self.turno_cavalier += 1
        self.carga_evaluada = False

    def reset(self) -> None:
        self.turno_cavalier = 0
        self.carga_evaluada = False
        if self.marca_usos is not None:
            self.marca_usos.reset()
        if self.warding_usos is not None:
            self.warding_usos.reset()

    # --- Unwavering Mark (3): marca y desventaja --------------------------------
    def after_attack_roll(self, attacker: Any, target: Any, atk: Any,
                          hit: bool, ctx: Any = None,
                          rng: Any = None) -> None:
        """Marca al ``target`` tras impactarle con arma cuerpo a cuerpo.

        Marca hasta el final del siguiente turno del dueño (aproximación
        ``ronda + 2``, mismo criterio documentado que Goading). Gasta un
        uso de ``marca_usos``. Los guards van ANTES de todo RNG: sin
        acierto, sin arma cuerpo a cuerpo, incapacitado, sin usos o sin
        ``rng`` no hay ni pick. La desventaja la aplica
        ``rules.mastery.consumir_marcas`` (campo propio
        ``marca_cavalier``, separado de Goading).
        """
        if attacker is not self.owner or not hit:
            return None
        if getattr(atk, "range_type", None) is not AttackRange.MELEE:
            return None
        if not getattr(self.owner, "can_act", True) or rng is None:
            return None
        if self.marca_usos is None or not self.marca_usos.available:
            return None
        if not getattr(target, "alive", True) or not getattr(
                target, "name", None):
            return None
        estado = getattr(target, "state", None)
        ronda = getattr(ctx, "round", None)
        if estado is None or ronda is None:
            return None
        if pick(rng, ("no", "si")) == "no":
            return None
        self.marca_usos.spend()
        # Sustituye cualquier marca anterior (otro combatiente o la misma):
        # «la marca nueva sustituye a la anterior».
        estado.marca_cavalier.clear()
        # shortcut: caduca a las 2 rondas («hasta el final de tu
        # siguiente turno»), mismo criterio que Goading; la ref al
        # marcador permite anularla si muere o queda incapacitado.
        estado.marca_cavalier[self.owner.name] = (
            int(ronda) + 2, self.owner)
        return None


def apply_cavalier(pj: Any, level: int | None = None,
                   rng: Any = None) -> CavalierFeatures:
    """Aplica la subclase Cavalier a un PJ Guerrero.

    Exige que ``pj`` ya tenga :class:`FighterFeatures`
    (:func:`apply_fighter`) y nivel >= 3. Añade el trait con Bonus
    Proficiency (habilidad con ``pick``), los usos de Unwavering Mark
    (máx(1, mod FUE)) y, desde el nivel 7, los de Warding Maneuver
    (máx(1, mod CON)).
    """
    if _de(pj, FighterFeatures) is None:
        raise ValueError(
            "Primero aplica la clase guerrero con apply_fighter(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    if lvl < 3:
        raise ValueError(
            f"Cavalier requiere nivel >= 3: llegó {lvl}."
        )
    generador = rng if rng is not None else _RNG_CREACION

    # Bonus Proficiency (3): una habilidad del pool que el PJ no tenga.
    # Sin candidatas → sin cambio y sin RNG (mismo criterio que Student
    # of War en Battle Master).
    conocidas = set(pj.skill_proficiencies or set())
    candidatas = tuple(h for h in CAVALIER_BONUS_SKILLS if h not in conocidas)
    competencia = ""
    if candidatas:
        competencia = pick(generador, candidatas)
        pj.skill_proficiencies = conocidas | {competencia}

    trait = CavalierFeatures(
        name="Cavalier",
        level=lvl,
        competencia=competencia,
    )
    trait.owner = pj
    # Unwavering Mark: usos desde el nivel 3 (tabla de FUE del dueño).
    trait.marca_usos = ActionUsage(
        UsageKind.PER_DAY,
        uses_max=cavalier_mark_uses(int(pj.abilities.mod("str"))),
    )
    # Warding Maneuver: solo desde el nivel 7 (tabla de CON del dueño).
    if lvl >= 7:
        trait.warding_usos = ActionUsage(
            UsageKind.PER_DAY,
            uses_max=warding_maneuver_uses(int(pj.abilities.mod("con"))),
        )
    pj.traits.append(trait)
    return trait


__all__ = ["CavalierFeatures", "apply_cavalier"]

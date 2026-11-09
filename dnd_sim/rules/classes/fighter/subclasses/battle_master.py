"""Subclase Battle Master (Maestro de Batalla, PHB 2024) del Fighter.

Concentra en un único rasgo agregado (:class:`BattleMasterFeatures`)
las features de la subclase. :func:`apply_battle_master` monta el
personaje (exige que ``pj`` ya tenga :class:`FighterFeatures`).

Decisiones de simulación documentadas:

- **Combat Superiority** (3): dados de superioridad con la tabla
  ``core/classes.py`` (4/5/6 dados; d8/d10/d12 desde 10/18). En el sim
  un combate = un día descansado: ``reset`` los rellena y no se
  recuperan dentro del combate. Una maniobra como máximo por ataque.
- **Maniobras conocidas** (3): ``sample`` del pool
  :data:`~dnd_sim.core.classes.BATTLE_MASTER_MANEUVERS` (cuenta según
  el nivel) con kwarg explícito ``maneuvers`` validado (patrón
  ``fighting_style``).
- **Student of War** (3): competencia en una habilidad de
  ``FIGHTER_SKILLS`` que el PJ no tenga, elegida con ``pick`` uniforme
  (sin candidatas → sin cambio y sin RNG) y en un juego de herramientas
  de artesano (dato sin efecto: el modelo no guarda herramientas).
- **Know Your Enemy** (7): dato sin efecto (decisión de diseño: el sim
  no tiene IA que use inmunidades/resistencias/vulnerabilidades).
- **Relentless** (15): al ejecutar una maniobra, ``pick`` «no»/«sí»
  (sin RNG si nivel < 15 o ya usado este turno); si es «sí» se tira
  1d8 —siempre d8, aunque el dado del PJ sea mayor— y NO se gasta
  ningún dado. El flag se reinicia en ``on_turn_start``.
- Los efectos sin movimiento/posiciones/objetos (empuje, objeto
  soltado, alcance, movimiento del aliado) son dato sin efecto
  (``# TODO``): solo daño y salvación. Bait and Switch y Evasive
  Footwork quedan FUERA del pool (ver TODO.md).

La decisión por ataque vive en :meth:`BattleMasterFeatures.decidir_maniobra`
(punto único del motor tras conocer la tirada; ver el docstring) y la
ejecución en :meth:`BattleMasterFeatures.extra_attack_damage`.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from .....core.classes import (
    BATTLE_MASTER_MANEUVERS,
    FIGHTER_SKILLS,
    MAX_LEVEL,
    MIN_LEVEL,
    maneuvers_known_count,
    superiority_dice_count,
    superiority_die_sides,
)
from .....core.dice import roll_dice
from .....core.enums import AttackRange
from .....core.log import log_line as _log_line
from .....core.randomness import pick, sample
from .....core.targeting import valid_targets
from ....traits.base import Trait
from ..features import FighterFeatures

#: RNG con semilla fija para Student of War y maniobras cuando no pasa
#: ``rng``: crea el personaje siempre igual (reproducible).
_RNG_CREACION = random.Random(0)

#: Maniobras que se ejecutan al impactar (punto de decisión único).
#: Precision ataca el fallo (A6) y Feinting es acción bonus (A5).
MANEUVERS_ON_HIT: tuple[str, ...] = (
    "Disarming Attack",
    "Distracting Strike",
    "Goading Attack",
    "Lunging Attack",
    "Maneuvering Attack",
    "Menacing Attack",
    "Pushing Attack",
    "Sweeping Attack",
    "Trip Attack",
)

#: Maniobras solo para ataques cuerpo a cuerpo (el alcance extra de
#: Lunging y la geometría de Sweeping no están en el modelo).
MANEUVERS_MELEE_ONLY: frozenset[str] = frozenset(
    {"Lunging Attack", "Sweeping Attack"})


def _de(actor: Any, clase: type) -> Any:
    """Primer rasgo de ``actor`` que sea instancia de ``clase`` (o None)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


@dataclass
class BattleMasterFeatures(Trait):
    """Features de la subclase y estado de Combat Superiority."""

    # Nivel del personaje (manda en las tablas de la subclase).
    level: int = MIN_LEVEL
    # Dados de superioridad restantes (se rellenan en ``reset``).
    dados_restantes: int = 0
    # Caras del dado de superioridad del PJ (8/10/12 según nivel).
    dados_lados: int = 8
    #: Maniobras conocidas (nombres de :data:`BATTLE_MASTER_MANEUVERS`).
    maneuvers: list[str] = field(default_factory=list, repr=False,
                                 compare=False)
    #: ¿Ya se usó Relentless en el turno actual? (una vez por turno).
    relentless_used_this_turn: bool = False
    #: Know Your Enemy (7): dato sin efecto (sin IA que lo use).
    know_your_enemy: bool = False
    #: Competencia ganada con Student of War ("" si no había candidatas).
    competencia: str = ""
    #: Juego de herramientas de artesano (dato sin efecto).
    herramientas: str = "herramientas de artesano"
    #: Maniobra de impacto decidida y aún no ejecutada (se limpia en
    #: ``on_turn_start`` si el ataque no la resolvió).
    maniobra_pendiente: str | None = field(
        default=None, repr=False, compare=False)
    #: TOTAL de la tirada original, para que Sweeping compare su CA.
    maniobra_total: int = 0
    #: Feinting Attack (acción bonus): el siguiente ataque de este turno
    #: tiene ventaja y, si impacta, su dado se aplica (se limpia en
    #: ``on_turn_start``; el punto de decisión consume la ranura).
    feinting_pendiente: bool = False
    #: Dueño (para que ``reset`` pueda apagar los flags en el combatiente).
    owner: Any = field(default=None, repr=False, compare=False)

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        # «Una vez por turno» de Relentless: se reinicia al empezar el turno.
        self.relentless_used_this_turn = False
        # Feinting caduca al fin de su turno y una pendiente sin resolver
        # no viaja al turno siguiente.
        self.feinting_pendiente = False
        self.maniobra_pendiente = None

    def reset(self) -> None:
        """Un combate nuevo = un día descansado: dados de superioridad llenos."""
        self.dados_restantes = superiority_dice_count(self.level)
        self.relentless_used_this_turn = False
        self.feinting_pendiente = False
        self.maniobra_pendiente = None
        self.maniobra_total = 0

    # --- Punto de decisión único por ataque (3) --------------------------------
    def _elegibles(self, target: Any, rango: Any, ctx: Any) -> tuple[str, ...]:
        """Maniobras de impacto conocidas elegibles en este ataque.

        Filtros sin RNG: solo las de impacto conocidas; cuerpo a cuerpo
        para Lunging/Sweeping (sin geometría) y Sweeping exige OTRO
        enemigo vivo (sin elegibles, la maniobra sale del pool).
        """
        elegibles = []
        for m in self.maneuvers:
            if m not in MANEUVERS_ON_HIT:
                continue
            if m in MANEUVERS_MELEE_ONLY and rango is not AttackRange.MELEE:
                continue
            if m == "Sweeping Attack" and not self._otro_enemigo(ctx, target):
                continue
            elegibles.append(m)
        return tuple(elegibles)

    def _otro_enemigo(self, ctx: Any, target: Any) -> Any:
        """Primer enemigo vivo distinto de ``target`` (o None; sin RNG)."""
        for c in valid_targets(self.owner, ctx):
            if c is not target:
                return c
        return None

    def decidir_maniobra(self, attacker: Any, target: Any, atk: Any,
                         rango: Any, *, roll: int, total: int, ca: int,
                         hit: bool, ctx: Any = None, rng: Any = None,
                         log: Any = None) -> tuple[bool, int]:
        """Decisión ÚNICA de maniobra de este ataque (patrón Arcane Shot).

        Lo llama el motor en el paso 6b de ``attack_roll`` (duck-typing,
        ``_decidir_maniobra``). Guards primero (sin datos, pendiente sin
        resolver, Feinting encolado o sin rng → ``None`` SIN RNG; en
        fallo, de momento sin elegibles → SIN RNG: Precision entra en
        A6). Con elegibles: ``pick`` «no»/«sí» y ``pick`` uniforme entre
        las maniobras conocidas; la maniobra se guarda en
        ``maniobra_pendiente`` y su dado SOLO se gasta al ejecutarse
        (``extra_attack_damage``). Una maniobra como máximo por ataque.
        """
        if (attacker is not self.owner
                or target is None
                or rng is None
                or self.dados_restantes <= 0
                or self.maniobra_pendiente is not None
                or self.feinting_pendiente):
            return hit, total
        if not hit:
            return hit, total  # A6: Precision Attack (fallo → total)
        elegibles = self._elegibles(target, rango, ctx)
        if not elegibles:
            return hit, total  # sin elegibles: cero RNG
        if pick(rng, ("no", "si")) == "no":
            return hit, total
        self.maniobra_pendiente = pick(rng, elegibles)
        self.maniobra_total = total
        return hit, total

    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            *, crit: bool = False, ctx: Any = None,
                            rng: Any = None, atk: Any = None) -> int:
        """Ejecuta la maniobra pendiente al impactar: gasta el dado.

        La decisión ya se tomó en ``decidir_maniobra``; aquí se tira el
        dado de superioridad UNA vez (con la misma regla de críticos que
        los dados extra del motor: ``crit`` lo duplica), se gasta el
        dado —salvo Relentless, que tira 1d8 sin gastar— y se suma al
        daño. Las salvaciones/condiciones (A4), marcas (A5) y Sweeping
        (A6) se resuelven con la MISMA tirada. Sin pendiente, sin
        datos, sin rng o si el atacante no es el dueño → 0 SIN RNG.
        """
        if (attacker is not self.owner
                or target is None
                or self.maniobra_pendiente is None
                or self.dados_restantes <= 0
                or rng is None):
            return 0
        opcion = self.maniobra_pendiente
        self.maniobra_pendiente = None  # se ejecuta una sola vez
        # Relentless (15): 1d8 en lugar de gastar el dado; una vez por
        # turno y sin RNG por debajo del nivel 15 o si ya se usó.
        gastar = True
        if (self.level >= 15 and not self.relentless_used_this_turn
                and pick(rng, ("no", "si")) == "si"):
            valor = int(roll_dice("1d8", rng, crit=crit))
            self.relentless_used_this_turn = True
            gastar = False
        else:
            valor = int(roll_dice(f"1d{self.dados_lados}", rng, crit=crit))
        if gastar:
            self.dados_restantes -= 1
        # A4: salvaciones y condiciones con ``valor`` ya tirado.
        # A5: marcas Distracting/Goading.
        # A6: Sweeping reparte ``valor`` al segundo objetivo (0 propio).
        sufijo = "" if gastar else " (Relentless: sin gastar dado)"
        _log_line(ctx, f"Battle Master ({opcion}): +{valor} de daño{sufijo}")
        return valor


def apply_battle_master(pj: Any, level: int | None = None,
                        maneuvers: tuple[str, ...] | None = None,
                        rng: Any = None) -> BattleMasterFeatures:
    """Aplica la subclase Battle Master a un PJ Guerrero.

    Exige que ``pj`` ya tenga :class:`FighterFeatures`
    (:func:`apply_fighter`) y nivel >= 3. Añade el trait con Student of
    War (habilidad con ``pick``), las maniobras conocidas según el nivel
    (o las explícitas del kwarg ``maneuvers``), los dados de
    superioridad y Know Your Enemy (dato, nivel 7+).
    """
    if _de(pj, FighterFeatures) is None:
        raise ValueError(
            "Primero aplica la clase guerrero con apply_fighter(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    if lvl < 3:
        raise ValueError(
            f"Battle Master requiere nivel >= 3: llegó {lvl}."
        )
    generador = rng if rng is not None else _RNG_CREACION

    # Student of War (3): una habilidad de la clase que el PJ no tenga.
    # Sin candidatas → sin cambio y sin RNG (mismo criterio que Giant).
    conocidas = set(pj.skill_proficiencies or set())
    candidatas = tuple(h for h in FIGHTER_SKILLS if h not in conocidas)
    competencia = ""
    if candidatas:
        competencia = pick(generador, candidatas)
        pj.skill_proficiencies = conocidas | {competencia}

    # Maniobras conocidas: N del pool (sample) o las explícitas.
    n = maneuvers_known_count(lvl)
    if maneuvers is None:
        elegidas = list(sample(generador, BATTLE_MASTER_MANEUVERS, n))
    else:
        elegidas = list(maneuvers)
        invalidas = [m for m in elegidas if m not in BATTLE_MASTER_MANEUVERS]
        if invalidas:
            raise ValueError(
                f"{invalidas!r} no es una maniobra de Battle Master: "
                f"opciones {sorted(BATTLE_MASTER_MANEUVERS)}."
            )
        if len(elegidas) != n:
            raise ValueError(
                f"se esperaban {n} maniobras para el nivel {lvl} y "
                f"llegaron {len(elegidas)}."
            )

    trait = BattleMasterFeatures(
        name="Battle Master",
        level=lvl,
        dados_restantes=superiority_dice_count(lvl),
        dados_lados=superiority_die_sides(lvl),
        maneuvers=elegidas,
        know_your_enemy=lvl >= 7,
        competencia=competencia,
    )
    trait.owner = pj
    pj.traits.append(trait)
    return trait


__all__ = ["BattleMasterFeatures", "apply_battle_master"]

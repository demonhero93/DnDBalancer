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
- **Maniobras con salvación** (3): CD = 8 + PB + max(mod FUE, mod DES);
  Menacing (SAB) → Asustado 2 rondas; Trip (FUE, solo Grande o menor)
  → PRONE con el código de Topple; Goading (SAB) → marca en el estado
  del afectado; Disarming/Pushing (FUE) → solo log (objeto/empuje sin
  modelar); Distracting/Feinting son marcas (ver arriba) y
  Lunging/Maneuvering son solo daño.
- **Precision Attack** (3): solo con fallo (sin 1 natural) y si el
  dado máximo alcanza la CA; sube el TOTAL de la tirada —no el daño—
  y puede convertir el impacto. **Sweeping Attack** (3): solo cuerpo
  a cuerpo y con OTRO enemigo; el dado NO se suma al golpe propio: va
  al segundo objetivo si el TOTAL original cubre su CA efectiva.
- Los efectos sin movimiento/posiciones/objetos (empuje, objeto
  soltado, alcance, movimiento del aliado) son dato sin efecto
  (``# TODO``): solo daño y salvación. Bait and Switch y Evasive
  Footwork quedan FUERA del pool (ver TODO.md).
- **Commander's Strike** (4): el ataque del dueño se sustituye por el
  de un aliado con la reacción libre, usando un dado del dueño en
  ``ctx.dano_reaccion`` (patrón Riposte). La decisión es PREVIA a la
  tirada (paso 2b): no es equiprobable con las maniobras de impacto,
  que ven el resultado. El ataque aliado es de reacción: no activa
  maniobras de la sesión 1 ni reentra en Commander's Strike.
- **Rally** (acción bonus): un aliado vivo no hostil distinto del
  dueño recibe PV temporales = dado + mod CAR del dueño (mínimo 1; no
  se acumulan, se queda el mayor, patrón aura tundra). Exige la
  maniobra conocida; el dado se gasta en ``execute``.
- **Ambush** (3): ``bonus_iniciativa`` lo consulta
  ``roll_initiative`` (duck-typing, sin imports de rules en el
  motor): ``pick`` «no»/«sí» y un dado de superioridad sumado a la
  tirada. La parte de Sigilo es dato sin efecto (el motor no tira
  habilidades).

La decisión por ataque vive en :meth:`BattleMasterFeatures.decidir_maniobra`
(punto único del motor tras conocer la tirada; ver el docstring) y la
ejecución en :meth:`BattleMasterFeatures.extra_attack_damage`.
"""
from __future__ import annotations

import random

from ......core.classes import (
    BATTLE_MASTER_MANEUVERS,
    FIGHTER_SKILLS,
    MAX_LEVEL,
    MIN_LEVEL,
    superiority_dice_count,
    superiority_die_sides,
    maneuvers_known_count,
)
from ......core.randomness import pick, sample
from ..._util import _de
from ...features import FighterFeatures
from .actions import BattleMasterRallyAction, FeintingAttackAction
from .features import BattleMasterFeatures

#: RNG con semilla fija para Student of War y maniobras cuando no pasa
#: ``rng``: crea el personaje siempre igual (reproducible).
_RNG_CREACION = random.Random(0)

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
    # Feinting Attack (acción bonus): disponible desde el nivel 3.
    pj.actions.append(FeintingAttackAction())
    # Rally (acción bonus): disponible desde el nivel 3.
    pj.actions.append(BattleMasterRallyAction())
    return trait


__all__ = ["BattleMasterFeatures", "BattleMasterRallyAction",
           "FeintingAttackAction", "apply_battle_master"]

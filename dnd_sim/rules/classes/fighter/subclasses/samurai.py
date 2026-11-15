"""Subclase Samurai (Samurái, XGE) del Guerrero.

Rasgos por nivel (Fighter 3 / 7 / 10 / 15 / 18):

- **Bonus Proficiency** (3): competencia en Historia, Perspicacia,
  Interpretación o Persuasión, elegida con ``pick`` entre las que el PJ
  no tenga (:data:`~dnd_sim.core.classes.SAMURAI_BONUS_SKILLS`; las
  cuatro existen en la tabla del proyecto). Sin candidatas → sin cambio
  y sin RNG. El idioma alternativo es dato sin efecto (sin modelo).
- **Fighting Spirit** (3): acción adicional; hasta el final del turno,
  ventaja en TODAS las tiradas de ataque con arma y PV temporales
  5 (3-9) / 10 (10-14, con Tireless Spirit) / 15 (15+), sin acumulación
  con PV temporales existentes (se queda el mayor, patrón Vitality
  Surge). 3 usos por descanso largo (en el sim, por combate).
  **Orden de activación (decisión documentada):** el bucle del motor
  juega la ACTION antes que la BONUS y no existe un punto previo, así
  que la activación se decide en ``on_turn_start`` (con ``pick``
  «no»/«sí») marcando la acción adicional como gastada en
  ``ctx.resources``: así la ventaja se aplica a los ataques del MISMO
  turno sin tocar el orden de las pasadas (patrón documentado, ver
  PASOS). Elegibilidad sin RNG: nivel >= 3, quedan usos, acción
  adicional libre, no activo ya este turno y el dueño puede actuar.
- **Elegant Courtier** (7): competencia en salvaciones de SABIDURÍA; si
  el PJ ya la tuviera, elige INTELIGENCIA o CARISMA con ``pick`` (la
  que no tenga; sin candidatas, sin cambio). El bonificador igual al
  mod SAB (mín. +1) en Perspicacia/Persuasión es dato sin efecto (el
  sim no tira esas pruebas en combate; congelado con test).
- **Tireless Spirit** (10): recupera 1 uso de Fighting Spirit al tirar
  iniciativa si no le quedan → dato sin efecto por diseño (cada
  combate empieza con los usos completos; mismo criterio que
  Ever-Ready Shot, congelado con test).
- **Rapid Strike** (15): renunciar a la ventaja neta de una tirada de
  ataque con arma de la acción Atacar para hacer un ataque con arma
  adicional contra el mismo objetivo, una vez por turno. Decisión con
  ``pick`` ANTES del d20 en ``engine/combat/attack.py`` (consulta
  duck-typing ``renunciar_ventaja``; sin entrada en HOOK_NAMES; ver
  A4 del plan).
- **Strength Before Death** (18) — **versión DIFERIDA (decisión del
  maintainer)**: el daño que deja al Samurai a 0 PG sin matarlo de
  golpe puede gastar la reacción (1 uso por combate) para «quedarse en
  pie» (``en_pie_pendiente``) y jugar un turno extra **al terminar el
  turno del combatiente que lo dejó a 0**, antes del fin de combate y
  sin alterar la iniciativa. Cualquier daño adicional mientras está
  pendiente lo deja fuera de combate al momento (aproxima las tres
  salvaciones de muerte: el sim no las tiene) y cancela el turno
  extra; la curación por encima de 0 lo saca del estado pendiente. Al
  terminar el turno extra: con 0 PG queda fuera de combate, con PG > 0
  sigue normal. El predicado «en pie» es ``Combatant.alive``
  (``hp > 0`` o ``en_pie_pendiente``), así que objetivos, fin de
  combate y estadísticas lo tratan como en pie. Este turno extra no
  puede disparar otro. Sin salvaciones de muerte, sin interrupción
  inmediata (ver PASOS y ARCHITECTURE).

Registro: clave ``"samurai"`` en ``fighter/__init__.py``. Ver
``TODO.md`` (plan «Samurai») y las entradas de
``PASOS-ANTERIORES.txt``.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from .....core.classes import (
    MAX_LEVEL,
    MIN_LEVEL,
    SAMURAI_BONUS_SKILLS,
    fighting_spirit_uses,
)
from .....core.randomness import pick
from ....traits.base import Trait
from ....usage import ActionUsage, UsageKind
from ..features import FighterFeatures

#: RNG con semilla fija para las elecciones de creación (Bonus
#: Proficiency y salvación de Elegant Courtier) cuando el llamante no
#: pasa ``rng``: crea el personaje siempre igual (reproducible, patrón
#: del resto de subclases).
_RNG_CREACION = random.Random(0)


def _de(actor: Any, clase: type) -> Any:
    """Primer trait de ``clase`` que lleve ``actor`` (o ``None``)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


@dataclass
class SamuraiFeatures(Trait):
    """Rasgos de la subclase Samurai.

    Los flags ``spirit_activo`` y ``rapid_strike_used`` son por turno
    (se limpian en los ganchos de turno); ``spirit_uses`` (3) y
    ``sbd_uses`` (1) son por combate y los restaura ``reset()``.
    """

    competencia: str = ""          # Bonus Proficiency elegida ("" = sin cambio)
    courtier_save: str = ""        # Salvación concedida por Elegant Courtier
    level: int = MIN_LEVEL         # Nivel del personaje (manda en las tablas)
    spirit_uses: ActionUsage | None = None
    spirit_activo: bool = False    # ventaja de Fighting Spirit en este turno
    rapid_strike_used: bool = False  # ya ejerció Rapid Strike este turno
    sbd_uses: ActionUsage | None = None  # Strength Before Death (1 por combate)

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        """Limpia los flags por turno del dueño.

        La activación de Fighting Spirit (A3) se decide aquí, ANTES de
        las pasadas de acción, para que la ventaja cubra los ataques
        del mismo turno. El flag ``spirit_activo`` se limpia en
        ``on_any_turn_end`` (fin del turno del dueño), para que los
        ataques de oportunidad posteriores ya no cuenten.
        """
        if actor is not self.owner:
            return None
        self.rapid_strike_used = False
        return None

    def reset(self) -> None:
        """Un combate nuevo: usos completos y flags apagados."""
        if self.spirit_uses is not None:
            self.spirit_uses.reset()
        if self.sbd_uses is not None:
            self.sbd_uses.reset()
        self.spirit_activo = False
        self.rapid_strike_used = False
        return None


def apply_samurai(pj: Any, level: int | None = None,
                  rng: random.Random | None = None) -> SamuraiFeatures:
    """Aplica la subclase Samurai a ``pj`` (clase guerrero, nivel >= 3).

    Bonus Proficiency usa ``pick`` solo si hay candidatas; Elegant
    Courtier solo desde el nivel 7. ``rng`` por defecto: semilla fija 0
    (creación reproducible, patrón del resto de subclases).
    """
    if _de(pj, FighterFeatures) is None:
        raise ValueError(
            "Primero aplica la clase guerrero con apply_fighter(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    if lvl < 3:
        raise ValueError(
            f"Samurai requiere nivel >= 3: llegó {lvl}."
        )
    generador = rng if rng is not None else _RNG_CREACION

    # Bonus Proficiency (3): una habilidad del pool que el PJ no tenga.
    # Sin candidatas → sin cambio y sin RNG (patrón Cavalier).
    conocidas = set(pj.skill_proficiencies or set())
    candidatas = tuple(h for h in SAMURAI_BONUS_SKILLS if h not in conocidas)
    competencia = ""
    if candidatas:
        competencia = pick(generador, candidatas)
        pj.skill_proficiencies = conocidas | {competencia}

    # Elegant Courtier (7): salvación de SAB, o INT/CAR si ya la tiene.
    courtier = ""
    if lvl >= 7:
        saves = set(pj.save_proficiencies or set())
        if "wis" not in saves:
            saves = saves | {"wis"}
            courtier = "wis"
        else:
            alternativas = tuple(a for a in ("int", "cha") if a not in saves)
            if alternativas:
                courtier = pick(generador, alternativas)
                saves = saves | {courtier}
        pj.save_proficiencies = saves

    trait = SamuraiFeatures(
        name="Samurai",
        level=lvl,
        competencia=competencia,
        courtier_save=courtier,
    )
    trait.owner = pj
    trait.spirit_uses = ActionUsage(
        UsageKind.PER_DAY,
        uses_max=fighting_spirit_uses(lvl),
    )
    trait.sbd_uses = ActionUsage(UsageKind.PER_DAY, uses_max=1)
    pj.traits.append(trait)
    return trait


__all__ = ["SamuraiFeatures", "apply_samurai"]

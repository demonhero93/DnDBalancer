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
    fighting_spirit_temp_hp,
    fighting_spirit_uses,
)
from .....core.log import log_line as _log_line
from .....core.randomness import pick
from .....model.actions import ActionType
from ....conditions import Condition
from ....traits.base import Trait
from ....usage import ActionUsage, UsageKind
from .._util import _de
from ..features import FighterFeatures

#: RNG con semilla fija para las elecciones de creación (Bonus
#: Proficiency y salvación de Elegant Courtier) cuando el llamante no
#: pasa ``rng``: crea el personaje siempre igual (reproducible, patrón
#: del resto de subclases).
_RNG_CREACION = random.Random(0)


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
        """Limpia los flags por turno y decide Fighting Spirit (A3).

        La activación se decide AQUÍ, antes de las pasadas ACTION/BONUS
        (el motor no tiene punto previo: la ACTION va primero y no se
        toca el orden), con ``pick`` «no»/«sí» y solo si es elegible
        sin RNG. Al activarse gasta el uso, marca la acción adicional
        como gastada en ``ctx.resources`` (es su coste), otorga los PV
        temporales sin acumulación y enciende ``spirit_activo``: la
        ventaja la concede ``modify_attack_modifiers`` a los ataques
        del MISMO turno. El flag se apaga en ``on_any_turn_end``.

        ``rapid_strike_used`` se limpia aquí (una renuncia por turno).
        """
        if actor is not self.owner:
            return None
        self.rapid_strike_used = False
        # Elegibilidad sin RNG: usos, no activo ya este turno, acción
        # adicional libre y contexto con RNG. Sin candidato, sin pick.
        if self.spirit_activo:
            return None
        if self.spirit_uses is None or not self.spirit_uses.available:
            return None
        if ctx is None:
            return None
        recursos = getattr(ctx, "resources", None)
        if recursos is not None and getattr(
                recursos, "bonus_action_used", False):
            return None
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return None
        if pick(rng, ("no", "sí")) != "sí":
            return None
        self.spirit_uses.spend()
        cantidad = fighting_spirit_temp_hp(self.level)
        actual = int(getattr(actor, "temp_hp", 0) or 0)
        actor.temp_hp = max(actual, cantidad)  # sin acumulación
        self.spirit_activo = True
        if recursos is not None:
            recursos.use(ActionType.BONUS_ACTION)
        _log_line(
            ctx,
            f"{actor.name} invoca Fighting Spirit: ventaja en ataques "
            f"y {cantidad} PV temporales.",
        )
        return None

    def on_any_turn_end(self, actor: Any, ctx: Any = None) -> None:
        """Fin del turno del dueño: se apaga la ventaja de Fighting
        Spirit (hasta el final de ese turno; los ataques de
        oportunidad posteriores ya no cuentan)."""
        if actor is self.owner:
            self.spirit_activo = False
        return None

    def modify_attack_modifiers(self, mods: Any, attacker: Any,
                                target: Any, rango: Any, ctx: Any = None,
                                rng: Any = None, atk: Any = None) -> None:
        """Fighting Spirit: ventaja en ataques con arma del dueño.

        Solo con ``atk`` presente y no mágico (``spell_attack``); con
        desventaja se anula por la regla estándar (``AttackModifiers``).
        """
        if attacker is not self.owner or not self.spirit_activo:
            return None
        if atk is None or getattr(atk, "spell_attack", False):
            return None
        mods.advantage_sources.append("Fighting Spirit")
        return None

    def renunciar_ventaja(self, atk: Any, *, ctx: Any = None,
                          rng: Any = None) -> bool:
        """Rapid Strike (15): ¿renunciar a la ventaja de esta tirada?

        Elegibilidad SIN RNG: nivel >= 15, no ejercida aún este turno,
        ataque con arma (no hechizo), dentro de la acción Atacar
        (``ctx.in_attack_action``; no reacciones, ni bonus, ni
        ataques especiales de otra acción) y con ``rng`` disponible.
        Si es elegible, ``pick`` «no»/«sí» UNA vez por ataque; al
        decir que sí se gasta el flag por turno (limpiado en
        ``on_turn_start``): el ataque adicional no puede reactivarlo.
        """
        if self.level < 15 or self.rapid_strike_used:
            return False
        if atk is None or getattr(atk, "spell_attack", False):
            return False
        if ctx is None or rng is None:
            return False
        if getattr(ctx, "is_reaction", False):
            return False
        if not getattr(ctx, "in_attack_action", False):
            return False
        if pick(rng, ("no", "sí")) != "sí":
            return False
        self.rapid_strike_used = True
        return True

    def on_reduced_to_zero_hp(self, owner: Any, amount: Any,
                              damage_type: Any, source: Any, *,
                              crit: bool = False, ctx: Any = None,
                              rng: Any = None) -> None:
        """Strength Before Death (18): versión DIFERIDA del mantainer.

        Quien bajaría a 0 PV puede elegir (``pick`` «no»/«sí») seguir
        «en pie»: se pone ``en_pie_pendiente`` (lo consulta
        ``Combatant.alive``) y se apunta a la cola de turnos extra del
        propio ``state``. El turno extra se ejecuta AL FINAL de un
        turno de actor (procesado de cola en ``encounter``, decisión:
        de CADA turno para no bloquearse con reacciones o guarida) y
        tras él: con PV > 0 sigue, sin PV muere. No se encadena (1 uso
        por combate).

        Elegibilidad SIN RNG: nivel >= 18, uso disponible, sin flag
        previo, sin muerte ya marcada, reacción libre (el rasgo la
        gasta: es su coste), sin condición Incapacitado (NO ``can_act``:
        exige ``alive`` y los PV ya son 0) y contexto con RNG; con
        ``ctx``/``rng`` vacíos no se aplica (regla base). Devuelve
        ``None`` SIEMPRE (queda a 0 PV): si otro rasgo responde
        después con PV, la cola se resuelve sola al procesarse (cura =
        sin turno extra).
        """
        if owner is not self.owner or self.level < 18:
            return None
        if self.sbd_uses is None or not self.sbd_uses.available:
            return None
        if getattr(owner, "en_pie_pendiente", False):
            return None
        if getattr(owner, "dead", False):
            return None
        estado = getattr(owner, "state", None)
        if estado is None or getattr(estado, "reaction_used", True):
            return None
        if ctx is None or rng is None:
            return None
        # Incapacitado no puede usar su reacción. NO se mira ``can_act``:
        # en este punto los PV ya son 0 y ``can_act`` (que exige ``alive``)
        # daría False antes de poner el flag. La condición manda.
        try:
            if owner.conditions.has(Condition.INCAPACITATED):
                return None
        except Exception:
            pass
        if pick(rng, ("no", "sí")) != "sí":
            return None
        self.sbd_uses.spend()
        estado.reaction_used = True
        owner.en_pie_pendiente = True
        cola = getattr(estado, "turnos_extra_pendientes", None)
        if cola is not None and owner not in cola:
            cola.append(owner)
        _log_line(
            ctx,
            f"{owner.name} se resiste a caer (Strength Before Death): "
            "turno extra pendiente.",
        )
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

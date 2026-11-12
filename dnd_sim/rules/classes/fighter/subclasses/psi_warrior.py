"""Subclase Psi Warrior (Guerrero Psiónico, PHB 2024) del Guerrero.

Rasgos por nivel (Fighter 3 / 7 / 10 / 15 / 18):

- **Psionic Power** (3): dados de Energía Psiónica — reserva única
  compartida por todos los rasgos (2 × PB; d6/d8/d10/d12 según nivel,
  tablas ``psionic_dice_count``/``psionic_die_sides`` de ``core``).
  Un combate = un día descansado: ``reset`` los rellena todos (patrón
  dados de superioridad; sin recuperación por descanso corto dentro
  del combate). **Protective Field** (A5): reacción que reduce el
  daño de un aliado (o del dueño) con un dado. **Psionic Strike**
  (A3): daño de fuerza extra = dado + mod INT tras impactar y causar
  daño con un ataque con arma, una vez por turno. **Telekinetic
  Movement**: dato sin efecto (sin movimiento; sin dados ni RNG).
- **Telekinetic Adept** (7): **Psi-Powered Leap** → dato sin efecto
  (sin movimiento/vuelo; sin dados ni RNG). **Telekinetic Thrust**
  (A4): al aplicarse Psionic Strike, salvación de FUE — fallo ⇒
  PRONE (el empuje de 10 ft es dato sin efecto; decisión del
  maintainer: siempre PRONE).
- **Guarded Mind** (10): A6 — resistencia permanente al daño
  psíquico (sin acumular con otra fuente) y purga de Hechizado/
  Asustado al inicio del turno gastando un dado.
- **Bulwark of Force** (15): A7 — acción adicional que da media
  cobertura (+2 CA y +2 salvaciones de DES) a hasta ``max(1, mod
  INT)`` aliados vivos (incluido el dueño) por todo el combate;
  uso gratuito una vez o gasto de un dado.
- **Telekinetic Master** (18): A8 — activa (uso gratuito o dado) un
  efecto mientras el dueño no esté Incapacitado ni muerto (ver
  decisión sobre concentración en PASOS/TODO: versión simple, sin
  salvaciones de CON) y concede un ataque con arma como acción
  adicional en cada turno propio.

Característica de los poderes: INTELIGENCIA; CD = 8 + PB + mod INT.
La subclase no elige nada al crear el PJ (los ``pick`` de los rasgos
usan el ``rng`` del combate), así que el kwarg ``rng`` existe solo
por paridad con el resto de subclases.

Registro: clave ``"psi_warrior"`` en ``fighter/__init__.py``. Ver
``TODO.md`` (plan «Psi Warrior») y las entradas de
``PASOS-ANTERIORES.txt``.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from .....core.classes import (
    MAX_LEVEL,
    MIN_LEVEL,
    bulwark_targets,
    psionic_dice_count,
    psionic_die_sides,
)
from .....core.dice import roll_dice
from .....core.enums import DamageType
from .....core.log import log_line as _log_line
from .....core.randomness import pick
from .....model.actions import ActionType, CombatAction
from ....conditions import (Condition, EscapeCheck, apply_condition,
                            remove_condition)
from ....damage import apply_damage_modifiers, inflict_damage
from ....saves import registrar_resistencia, saving_throw
from ....traits.base import Trait
from ..features import FighterFeatures, _contexto, _es_aliado


def _de(actor: Any, clase: type) -> Any:
    """Primer trait de ``clase`` que lleve ``actor`` (o ``None``)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


@dataclass
class PsiWarriorFeatures(Trait):
    """Rasgos, reserva de dados y estado de Psi Warrior.

    Sin RNG en los guards: los ``pick`` de los rasgos (Psionic Strike,
    Protective Field, Guarded Mind, objetivos de Bulwark) se deciden
    en sus puntos de consulta con el ``rng`` del combate.
    """

    # Nivel del personaje (manda en las tablas de rasgos).
    level: int = MIN_LEVEL
    # Dados de Energía Psiónica: restantes y tamaño (se rellenan al
    # crear y en ``reset``; la tirada única al gastarse es A3+).
    dados_restantes: int = 0
    dados_lados: int = 6
    # Usos gratuitos (una vez por combate; se restauran en ``reset``).
    bulwark_uso_gratuito: bool = True
    telekinetic_master_uso_gratuito: bool = True
    # «Una vez por turno» de Psionic Strike (A3): se reinicia en
    # ``on_turn_start``.
    psionic_strike_used_this_turn: bool = False
    # Estado de Bulwark of Force (A7): activo por todo el combate +
    # referencias de los objetivos protegidos.
    bulwark_activo: bool = False
    bulwark_objetivos: list = field(
        default_factory=list, repr=False, compare=False)
    # Estado de Telekinetic Master (A8).
    telekinetic_master_activo: bool = False
    # Datos sin efecto congelados (decisión del maintainer): sin
    # movimiento ni vuelo en el modelo; no gastan dados ni RNG.
    telekinetic_movement: bool = True
    psi_powered_leap: bool = True
    # Dueño (guards de hooks y despacho de ``on_turn_start``).
    owner: Any = field(default=None, repr=False, compare=False)

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        # «Una vez por turno» de Psionic Strike (A3): se reinicia al
        # empezar el turno.
        self.psionic_strike_used_this_turn = False
        # Guarded Mind (A6): purga de Hechizado/Asustado con un dado.
        if self.level >= 10 and actor is self.owner:
            self._guarded_mind(ctx)

    def _guarded_mind(self, ctx: Any) -> None:
        """Guarded Mind (10): gasta un dado para terminar Hechizado/Asustado.

        Patrón Mindless Rage: si el dueño tiene alguna de las dos
        condiciones y hay dado, ``pick`` «no»/«sí»; al aceptar gasta el
        dado y retira TODAS las que tenga (los guards van antes del
        ``pick``: sin condición, sin ``rng`` o sin dados, ni consulta ni
        azar).
        """
        owner = self.owner
        tracker = getattr(owner, "conditions", None)
        if tracker is None:
            return
        afectadas = [cond for cond in (Condition.CHARMED,
                                       Condition.FRIGHTENED)
                     if tracker.has(cond)]
        if not afectadas:
            return  # sin condición: ni consulta ni RNG
        rng = getattr(ctx, "rng", None) if ctx is not None else None
        if rng is None or self.dados_restantes <= 0:
            return
        if pick(rng, ("no", "si")) == "no":
            return
        self.dados_restantes -= 1
        for cond in afectadas:
            remove_condition(owner, cond, ctx)
        nombres = ", ".join(c.value for c in afectadas)
        _log_line(ctx, f"{getattr(owner, 'name', owner)} usa Guarded Mind: "
                       f"termina {nombres}")

    def reset(self) -> None:
        """Un combate nuevo = un día descansado: dados psiónicos llenos."""
        self.dados_restantes = psionic_dice_count(self.level)
        self.psionic_strike_used_this_turn = False
        self.bulwark_uso_gratuito = True
        self.telekinetic_master_uso_gratuito = True
        self.bulwark_activo = False
        self.bulwark_objetivos = []
        self.telekinetic_master_activo = False

    def psionic_strike(self, target: Any, rango: Any, dmg: int, *,
                       atk: Any = None, crit: bool = False,
                       ctx: Any = None, rng: Any = None,
                       log: Any = None) -> None:
        """Psionic Strike (3): daño de fuerza extra (dado + mod INT).

        Lo llama el motor (walker ``_dano_extra_de_rasgo``) tras el
        daño principal de un impacto que causó daño, antes del daño
        adicional del arma. Guards primero (sin RNG): nivel, una vez
        por turno, reserva de dados, ``rng`` y ataque con arma (los
        hechizos quedan fuera). Decisión con ``pick`` «no»/«sí»; al
        gastarse, UNA tirada del dado que se reutiliza —sigue la regla
        de críticos del motor: ``crit`` viaja a ``roll_dice``—, se
        resta 1 a la reserva y se marca el turno. A4 (Telekinetic
        Thrust) se engancha tras aplicar el daño.
        """
        if (self.level < 3 or self.psionic_strike_used_this_turn
                or self.dados_restantes <= 0 or rng is None
                or dmg <= 0 or target is None):
            return
        if atk is not None and bool(getattr(atk, "spell_attack", False)):
            return  # solo ataques con arma
        if pick(rng, ("no", "si")) == "no":
            return
        self.dados_restantes -= 1
        self.psionic_strike_used_this_turn = True
        owner = self.owner
        mod_int = (int(owner.abilities.mod("int"))
                   if owner is not None else 0)
        crudo = int(roll_dice(f"1d{self.dados_lados}", rng, crit=crit))
        extra = apply_damage_modifiers(crudo + mod_int, DamageType.FORCE,
                                       target,
                                       magical=bool(getattr(atk, "magical",
                                                            False)))
        inflict_damage(target, extra, DamageType.FORCE, source=owner,
                       ctx=ctx, crit=crit, rng=rng,
                       magical=bool(getattr(atk, "magical", False)))
        _log_line(ctx, f"{getattr(owner, 'name', owner)} usa Psionic Strike: "
                       f"{crudo}+{mod_int} = {extra} de fuerza")
        if self.level >= 7:
            self._telekinetic_thrust(target, ctx, rng)

    def _telekinetic_thrust(self, target: Any, ctx: Any,
                            rng: Any) -> None:
        """Telekinetic Thrust (7): salvación FUE o cae PRONE (Topple).

        Se aplica SIEMPRE que Psionic Strike gasta el dado (sin pick
        propio): CD ``8 + competencia + mod INT``; fallo → PRONE con el
        mismo ``EscapeCheck`` de la Maestría Topple y con la Resistencia
        legendaria despachada como en el resto de salvaciones. Sin
        ``rng`` no hay salvación que tirar (defensivo: el walker ya lo
        garantiza).
        """
        if rng is None or target is None or self.owner is None:
            return
        owner = self.owner
        cd = (8 + int(getattr(owner, "proficiency", 0) or 0)
              + int(owner.abilities.mod("int")))
        sr = saving_throw(target, "str", cd, rng)
        sr = registrar_resistencia(ctx, target, sr)
        if sr.success:
            return
        apply_condition(target, Condition.PRONE, ctx, source=owner,
                        escape=EscapeCheck(abilities=("str", "dex"), dc=10,
                                           consumes_action=False))
        _log_line(ctx, f"{getattr(target, 'name', target)} cae derribado "
                       f"(Telekinetic Thrust de "
                       f"{getattr(owner, 'name', owner)})")

    def proteccion_psionica(self, objetivo: Any, cantidad: int,
                            tipo_dano: Any, fuente: Any, *,
                            ctx: Any = None, rng: Any = None) -> int | None:
        """Protective Field (6): reacción que reduce el daño con un dado.

        Lo llama el motor (walker ``_proteccion_psionica`` de
        ``rules/damage.py``) en la fase 1a para cualquier combatiente
        del contexto. Guards primero (sin RNG): nivel, cantidad,
        ``rng`` y reacción libre —compartida con Warding/Retaliation…:
        ``state.reaction_used``— más reserva de dados. Decisión con
        ``pick`` «no»/«sí»; al aceptar se gasta la reacción y un dado,
        la reducción es ``max(1, dado + mod INT)`` sin bajar de 0, y se
        registra en el log. Devuelve ``None`` = sin cambios.
        """
        if (self.level < 6 or cantidad <= 0 or rng is None
                or objetivo is None):
            return None
        estado = getattr(self.owner, "state", None)
        if (estado is None or estado.reaction_used
                or self.dados_restantes <= 0):
            return None
        if pick(rng, ("no", "si")) == "no":
            return None
        estado.reaction_used = True
        self.dados_restantes -= 1
        owner = self.owner
        mod_int = int(owner.abilities.mod("int"))
        crudo = int(roll_dice(f"1d{self.dados_lados}", rng))
        reduccion = max(1, crudo + mod_int)
        nuevo = max(0, int(cantidad) - reduccion)
        _log_line(ctx, f"{getattr(owner, 'name', owner)} usa Protective "
                       f"Field: -{min(reduccion, int(cantidad))} de daño "
                       f"(1d{self.dados_lados}={crudo}+{mod_int})")
        return nuevo


def _elegibles_bulwark(actor: Any, ctx: Any) -> list:
    """Aliados vivos de ``actor`` (incluido él) para Bulwark; sin RNG."""
    elegibles = [actor] if getattr(actor, "alive", True) else []
    for otro in getattr(ctx, "combatants", None) or []:
        if otro is actor:
            continue
        if _es_aliado(actor, otro):
            elegibles.append(otro)
    return elegibles


class PsiBulwarkAction(CombatAction):
    """Bulwark of Force (15, acción bonus): media cobertura a aliados.

    Elige con ``pick`` uniforme sin repetición hasta ``max(1, mod INT)``
    criaturas vivas del bando (incluido el dueño) y pone
    ``state.cobertura_bulwark`` en cada una: +2 a la CA y a las
    salvaciones de DES mientras el dueño siga vivo y sin estar
    Incapacitado (lectura dinámica en rules); dura todo el combate.
    Gasta primero el uso gratuito (sin RNG ni dado) y, si no queda, un
    dado de energía psiónica. La elegibilidad no consume RNG.
    """

    def __init__(self) -> None:
        self.name = "Bulwark of Force"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # el límite es el uso gratuito + la reserva

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None or not getattr(actor, "can_act", True):
            return False
        trait = _de(actor, PsiWarriorFeatures)
        if trait is None or trait.level < 15:
            return False
        if trait.bulwark_activo:
            return False  # una vez activo no se vuelve a activar
        if not trait.bulwark_uso_gratuito and trait.dados_restantes <= 0:
            return False
        return bool(_elegibles_bulwark(actor, ctx))

    def execute(self, context: Any) -> None:
        actor = getattr(context, "actor", None)
        rng = getattr(context, "rng", None)
        if actor is None or rng is None:
            return
        trait = _de(actor, PsiWarriorFeatures)
        if trait is None or trait.bulwark_activo:
            return
        if not trait.bulwark_uso_gratuito and trait.dados_restantes <= 0:
            return
        elegibles = _elegibles_bulwark(actor, context)
        if not elegibles:
            return
        # Gasto: primero el uso gratuito (sin dado), después un dado.
        if trait.bulwark_uso_gratuito:
            trait.bulwark_uso_gratuito = False
        else:
            trait.dados_restantes -= 1
        max_obj = bulwark_targets(int(actor.abilities.mod("int")))
        restantes = list(elegibles)
        objetivos = []
        while restantes and len(objetivos) < max_obj:
            idx = int(pick(rng, tuple(range(len(restantes)))))
            objetivos.append(restantes.pop(idx))
        for objetivo in objetivos:
            objetivo.state.cobertura_bulwark = actor
        trait.bulwark_activo = True
        trait.bulwark_objetivos = objetivos
        _log_line(context, f"{getattr(actor, 'name', actor)} usa Bulwark "
                           f"of Force: media cobertura a "
                           f"{len(objetivos)} criatura(s)")


def apply_psi_warrior(pj: Any, level: int | None = None,
                      rng: random.Random | None = None
                      ) -> PsiWarriorFeatures:
    """Aplica la subclase Psi Warrior a un PJ Guerrero.

    Exige que ``pj`` ya tenga :class:`FighterFeatures`
    (:func:`apply_fighter`) y nivel >= 3. Rellena la reserva de dados
    con las tablas de ``core``. ``rng`` por defecto con semilla 0
    (patrón del resto de subclases); la subclase no elige nada al
    crear el PJ, así que no consume azar aquí.
    """
    if _de(pj, FighterFeatures) is None:
        raise ValueError(
            "Primero aplica la clase guerrero con apply_fighter(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    if lvl < 3:
        raise ValueError(
            f"Psi Warrior requiere nivel >= 3: llegó {lvl}."
        )
    trait = PsiWarriorFeatures(
        name="Psi Warrior",
        level=lvl,
        dados_restantes=psionic_dice_count(lvl),
        dados_lados=psionic_die_sides(lvl),
    )
    trait.owner = pj
    # Guarded Mind (10): resistencia a daño psíquico permanente
    # (patrón Storm Soul: si ya la tenía, no se toca).
    if lvl >= 10 and DamageType.PSYCHIC not in pj.resistances:
        pj.resistances = set(pj.resistances) | {DamageType.PSYCHIC}
    pj.traits.append(trait)
    # Bulwark of Force (15): acción bonus, elegibilidad sin RNG (el
    # ``pick`` del encuentro decide entre las acciones candidatas).
    if lvl >= 15:
        pj.actions.append(PsiBulwarkAction())
    return trait


__all__ = ["PsiWarriorFeatures", "PsiBulwarkAction", "apply_psi_warrior"]

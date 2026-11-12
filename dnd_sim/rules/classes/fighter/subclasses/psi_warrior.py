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
    psionic_dice_count,
    psionic_die_sides,
)
from .....core.dice import roll_dice
from .....core.enums import DamageType
from .....core.log import log_line as _log_line
from .....core.randomness import pick
from ....damage import apply_damage_modifiers, inflict_damage
from ....traits.base import Trait
from ..features import FighterFeatures


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
        # empezar el turno. A6 añade aquí la purga de Guarded Mind.
        self.psionic_strike_used_this_turn = False

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
    pj.traits.append(trait)
    return trait


__all__ = ["PsiWarriorFeatures", "apply_psi_warrior"]

"""Subclase Path of the Berserker del bárbaro (PHB 2024).

Fuente: *Player's Handbook 2024* — Path of the Berserker (features en
niveles 3, 6, 10 y 14, mismos huecos que el resto de subclases). No
está ni en el SRD 2014 ni en la API, así que la tabla de features va
hardcodeada en :data:`BERSERKER_FEATURES`.

Decisiones de simulación documentadas:

- **Frenzy** (3): la primera acertada **que cualifica** de cada turno
  añade ``rage_damage(level)`` d6 al **mismo paquete de daño** del golpe
  (el crítico los duplica vía ``crit``). Cualifica: Furia activa,
  Ataque Temerario decidido a favor en el turno, turno propio y ataque
  de FUE; si el primer acertada no cualifica, el siguiente de ese
  turno sí puede pagar («on your first hit each turn»: solo se evalúa
  al pagar, nunca en reacciones). No causa agotamiento (PHB 2024).
  Sin ``rng`` el rasgo se abstiene: no hay bonus ni flag de pago.
- **Mindless Rage** (6): mientras dure la Furia, inmune a Hechizado y
  Aterrorizado (hook ``blocks_condition``); al entrar en Furia esas
  condiciones existentes **terminan** en el momento, todas las
  instancias de cualquier fuente (PHB 2024 «ends instead of
  postponing», hook ``on_rage_start``).
- **Retaliation** (10): reacción: ataque cuerpo a cuerpo contra quien
  te acierta en cuerpo a cuerpo (mismo patrón que la reacción de
  Beast): una por ronda (``state.reaction_used``), solo si sigues en
  pie y el atacante sigue vivo y no está a distancia. El arma se elige
  con ``pick`` entre ``attacks``/``weapons``/``dynamic_weapons``; sin
  arma melee a la mano se usa «Golpe sin armas» (1 + mod FUE
  contundente). Sin Frenzy ni ventaja de Temerario (la llamada va
  marcada ``is_reaction``).
  # TODO: el hook solo dispara con ``rango is MELEE``; el daño no
  melee que llegue por otras vías no está modelado.
- **Intimidating Presence** (14): acción bonus, salvación de SAB
  CD 8 + mod FUE + competencia de un número aleatorio de enemigos
  (convención de área); fallo → Aterrorizado 1 minuto (10 rondas) con
  repetición al fin de cada turno suyo. Un uso gratis por combate; la
  variante de Furia gasta un uso de Furia y **restaura** el uso gratis;
  si ambas están disponibles compiten con ``pick``. Funciona con o sin
  Furia activa. El estado diario vive en el trait (``Combatant.reset``
  lo recupera cada combate, igual que los usos de Furia).
  # TODO: emanación de 30 ft: sin posiciones reales se afecta a
  todos los enemigos vivos.
- Fuera de alcance: Weapon Mastery y Brutal Strike (no son features de
  subclase; # TODO en features de la clase), condiciones fuera del
  Enum Condition y efectos regionales.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any

from .....core.classes import MAX_LEVEL, MIN_LEVEL, rage_damage
from .....core.dice import roll_dice
from .....core.enums import AttackRange
from .....core.log import log_line as _log_line
from .....core.randomness import pick
from .....model.actions import ActionType, CombatAction
from .....model.attack import Attack
from ....area import AreaTargeting, select_area_targets
from ....conditions import (Condition, RepeatSave, apply_condition,
                            remove_condition)
from ....saves import registrar_resistencia, saving_throw
from ....traits.base import Trait
from ....usage import ActionUsage, UsageKind
from ..features import BarbarianFeatures, RageAction, _contexto

#: Features de subclase por nivel (PHB 2024; nombres en inglés como la API).
BERSERKER_FEATURES: dict[int, tuple[str, ...]] = {
    3: ("Frenzy",),
    6: ("Mindless Rage",),
    10: ("Retaliation",),
    14: ("Intimidating Presence",),
}


def _de(actor: Any, clase: type) -> Any:
    """Primer rasgo de ``actor`` que sea instancia de ``clase`` (o None)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


def _furia_de(actor: Any) -> RageAction | None:
    """La acción «Entrar en Furia» de ``actor`` (o None)."""
    for accion in getattr(actor, "actions", None) or []:
        if isinstance(accion, RageAction):
            return accion
    return None


def _armas_melee_de(criatura: Any) -> list:
    """Ataques cuerpo a cuerpo de ``criatura`` (mismo filtro que Beast).

    Incluye las armas dinámicas (``dynamic_weapons``, p. ej. el arma
    natural de la Beast mientras dura la Furia).
    """
    ataques = list(getattr(criatura, "attacks", None) or [])
    if not ataques:
        ataques = list(getattr(criatura, "weapons", None) or [])
    ataques += list(getattr(criatura, "dynamic_weapons", None) or [])
    return [
        a for a in ataques
        if getattr(a, "range_type", AttackRange.MELEE) is not AttackRange.RANGED
    ]


def _golpe_sin_armas() -> Attack:
    """Golpe sin armas (PHB): 1 + mod FUE, contundente."""
    return Attack("Golpe sin armas", "1", ability="str",
                  damage_type="bludgeoning")


@dataclass
class BerserkerFeatures(Trait):
    """Features de la subclase y estado de Frenzy/Presencia."""

    level: int = MIN_LEVEL
    #: ¿Ya se pagó Frenzy en este turno? (se evalúa en cada acertada
    #: hasta que una paga; el flag solo sube al pagar).
    frenzy_pagado: bool = field(default=False, repr=False, compare=False)
    #: Uso gratis diario de Presencia intimidante (1/día). El estado vive
    #: en el trait para que ``Combatant.reset`` lo recupere cada combate.
    presence_usage: ActionUsage = field(
        default_factory=lambda: ActionUsage(UsageKind.PER_DAY, 1),
        repr=False, compare=False,
    )
    owner: Any = field(default=None, repr=False, compare=False)

    @property
    def _furiosa(self) -> bool:
        barb = _de(self.owner, BarbarianFeatures)
        return bool(barb and barb.rage_active)

    # --- Frenzy (3) ----------------------------------------------------------
    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            crit: bool = False, ctx: Any = None,
                            rng: Any = None, atk: Any = None) -> int:
        """d6 extra de Frenzy en la primera acertada que cualifica del turno.

        Se evalúa en **cada** acertada hasta que una paga: si el primer
        golpe no cualifica (sin Furia, sin Temerario...), el siguiente de
        ese turno sí puede llevar Frenzy. Cualifica: turno propio (nunca
        reacciones ni turnos ajenos), Furia activa, Ataque Temerario
        decidido a favor y ataque de FUE (el ``atk`` ausente se asume
        cuerpo a cuerpo; un arma a distancia con mod de FUE se asume
        arrojadiza). Sin ``rng`` no paga ni se marca.
        """
        if self.level < 3 or self.owner is None or attacker is not self.owner:
            return 0
        if self.frenzy_pagado:
            return 0
        if getattr(ctx, "is_reaction", False):
            return 0  # la reacción no lleva Frenzy
        ctx_actor = getattr(ctx, "actor", None) if ctx is not None else None
        if ctx is not None and ctx_actor is not None and ctx_actor is not attacker:
            return 0  # fuera de su turno no paga
        barb = _de(self.owner, BarbarianFeatures)
        if barb is None or not barb.rage_active:
            return 0
        if not barb.reckless_active_this_turn:
            return 0
        if atk is not None and not BarbarianFeatures._es_fue(atk):
            return 0
        if rng is None:
            return 0  # sin RNG el rasgo se abstiene (no inventa dados)
        self.frenzy_pagado = True
        return int(roll_dice(f"{rage_damage(self.level)}d6", rng, crit=crit))

    # --- Mindless Rage (6) ---------------------------------------------------
    def blocks_condition(self, condition: Any, ctx: Any = None) -> bool:
        """Con Furia activa: inmune a Hechizado y Aterrorizado."""
        if self.level < 6:
            return False
        if condition not in (Condition.CHARMED, Condition.FRIGHTENED):
            return False
        return self._furiosa

    def on_rage_start(self, actor: Any, ctx: Any = None) -> None:
        """PHB 2024: entrar en Furia termina Hechizado/Aterrorizado."""
        if self.level < 6:
            return
        for cond in (Condition.CHARMED, Condition.FRIGHTENED):
            remove_condition(actor, cond, ctx)

    # --- Retaliation (10) ----------------------------------------------------
    def after_being_hit(self, target: Any, attacker: Any, rango: Any,
                        ctx: Any = None) -> None:
        """Reacción: ataque cuerpo a cuerpo contra quien te acierta melee."""
        if self.level < 10 or target is not self.owner or attacker is None:
            return
        if rango is not AttackRange.MELEE:
            return
        if not getattr(self.owner, "alive", True):
            return  # quién ha caído con el golpe no contraataca
        if not getattr(attacker, "alive", True):
            return
        if getattr(getattr(attacker, "state", None), "at_range", False):
            return  # el atacante está a distancia: no es un golpe melee
        if not getattr(self.owner, "can_act", True):
            return
        hostil = getattr(self.owner, "is_hostile_to", None)
        if hostil is not None and not hostil(attacker):
            return
        estado = getattr(self.owner, "state", None)
        if estado is not None and getattr(estado, "reaction_used", False):
            return
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return  # sin RNG el rasgo se abstiene (no tira ni gasta)
        pool = _armas_melee_de(self.owner)
        arma = pick(rng, pool) if pool else _golpe_sin_armas()
        if estado is not None:
            estado.reaction_used = True
        _log_line(ctx, f"{getattr(self.owner, 'name', self.owner)} usa su "
                       f"reacción para contraatacar (Retaliation)")
        # Import perezoso: rules no debe importar engine a nivel de módulo.
        from .....engine.combat import attack_roll
        # Copia superficial: marca la llamada como reacción (Ataque
        # Temerario no decide ni recibe ventaja fuera de su turno).
        r_ctx = copy.copy(ctx)
        r_ctx.is_reaction = True
        attack_roll(self.owner, attacker, arma, rng,
                    log=getattr(ctx, "log", None), ctx=r_ctx)

    # --- Ciclo de turno ------------------------------------------------------
    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        self.frenzy_pagado = False

    def reset(self) -> None:
        self.frenzy_pagado = False
        self.presence_usage.reset()


class IntimidatingPresenceAction(CombatAction):
    """Presencia intimidante: bonus action (nivel ≥ 14), pago o de Furia."""

    def __init__(self) -> None:
        self.name = "Presencia intimidante"
        self.action_type = ActionType.BONUS_ACTION
        # El límite diario vive en el trait: aquí no hay usage para que el
        # encuentro no gaste nada por su cuenta (el pago va en execute).
        self.usage = None

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        bers = _de(actor, BerserkerFeatures)
        if bers is None or bers.level < 14:
            return False
        if bers.presence_usage.available:
            return True
        # Uso adicional: exige un uso de Furia disponible.
        furia = _furia_de(actor)
        return bool(furia is not None and furia.usage is not None
                    and furia.usage.available)

    def execute(self, context: Any) -> None:
        actor = getattr(context, "actor", None)
        bers = _de(actor, BerserkerFeatures) if actor is not None else None
        if bers is None or bers.level < 14:
            return
        rng = getattr(context, "rng", None)
        if rng is None:
            return  # sin RNG no se tira nada (y no se paga el uso)
        # Objetivos por convención de área: número aleatorio de enemigos.
        objetivos = select_area_targets(actor, context, AreaTargeting())
        if not objetivos:
            return  # sin objetivos no se paga el uso
        # Pago: la variante gratis y la de Furia compiten con ``pick``
        # cuando ambas están disponibles; la de Furia gasta un uso de
        # Furia y restaura el uso gratis (PHB «additional uses requiring
        # an expenditure of your rage»).
        opciones = []
        if bers.presence_usage.available:
            opciones.append("gratis")
        furia = _furia_de(actor)
        if (furia is not None and furia.usage is not None
                and furia.usage.available):
            opciones.append("furia")
        if not opciones:
            return  # can_use ya lo impide: red de seguridad
        pago = pick(rng, opciones)
        if pago == "gratis":
            bers.presence_usage.spend()
        else:
            furia.usage.spend()
            bers.presence_usage.restore()
        dc = (8 + actor.abilities.mod("str")
              + int(getattr(actor, "proficiency", 0) or 0))
        _log_line(context, f"{actor.name} usa {self.name} sobre "
                           f"{len(objetivos)} objetivo(s):")
        for objetivo in objetivos:
            sr = saving_throw(objetivo, "wis", dc, rng, magical=False)
            registrar_resistencia(context, objetivo, sr)
            if not sr.success:
                # 1 minuto ≈ 10 rondas; la repetición al fin de cada
                # turno suyo es la cláusula estándar de Aterrorizado.
                apply_condition(
                    objetivo, Condition.FRIGHTENED, context, source=actor,
                    duration_rounds=10, repeat_save=RepeatSave("wis", dc),
                )


def apply_berserker(pj: Any, level: int | None = None) -> BerserkerFeatures:
    """Aplica la subclase Path of the Berserker a un PJ bárbaro.

    Exige que ``pj`` ya tenga :class:`BarbarianFeatures`
    (:func:`apply_barbarian`). Añade el trait de subclase y la acción
    bonus de Presencia intimidante.
    """
    if _de(pj, BarbarianFeatures) is None:
        raise ValueError(
            "Primero aplica la clase bárbaro con apply_barbarian(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    trait = BerserkerFeatures(name="Berserker", level=lvl)
    trait.owner = pj
    pj.traits.append(trait)
    pj.actions.append(IntimidatingPresenceAction())
    return trait


__all__ = ["BERSERKER_FEATURES", "BerserkerFeatures",
           "IntimidatingPresenceAction", "apply_berserker"]

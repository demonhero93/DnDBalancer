"""Clase Fighter (Guerrero, PHB 2024), sin subclases.

Concentra en un único rasgo agregado (:class:`FighterFeatures`) todas
las features de clase que dependen de tiradas o decisiones, más las
acciones bonus de la clase. :func:`apply_fighter` monta el personaje
completo (salvaciones, habilidades, Extra Attack, estilo...) a partir de
su nivel.

Uso::

    from dnd_sim.rules.classes.fighter import apply_fighter
    apply_fighter(pj, skills=("athletics", "perception"), level=5)
    # o vía el registro genérico:
    from dnd_sim.rules.classes import apply_class
    apply_class(pj, "fighter", skills=("athletics",), level=5)

Decisiones de simulación documentadas:

- **Competencias** (armas sencillas y marciales, armaduras ligeras,
  medias y pesadas, escudos): el modelo de PJ no tiene campos de
  competencia de arma/armadura, así que no se registran (mismo criterio
  que el resto de clases).
- **Tomar Aliento**: elegible SOLO si el PJ está herido (PV < PV
  máximos) y quedan usos; sin RNG en la elegibilidad. La curación es
  ``1d10 + nivel`` y nunca supera los PV máximos. Los usos no se
  recuperan en combate (escena única: el descanso se modela como
  ``Combatant.reset()``).
- **Oleada de Acción**: restaura el recurso de acción del turno
  (``TurnResources.action_used = False``) y el encuentro ejecuta una
  pasada de acción extra; máximo 1 uso por turno, solo si la acción ya
  se gastó (si no, se quedaría sin efecto) y nunca en la acción Magia
  (acción que el motor no tiene). Recarga por descanso = solo al
  empezar un combate nuevo (``reset``).
- Las decisiones con azar (estilo de combate, Second Wind, Action
  Surge, Indomitable...) se toman con ``core.randomness.pick`` uniforme
  y no consumen RNG cuando solo hay una opción.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ....core.classes import (
    FIGHTER_SKILLS,
    MAX_LEVEL,
    MIN_LEVEL,
    action_surge_uses,
    second_wind_uses,
)
from ....core.dice import roll_dice
from ....core.log import log_line as _log_line
from ....core.skills import normalize_skill
from ....model.actions import ActionType, CombatAction, TurnResources
from ...traits.base import Trait
from ...usage import ActionUsage, UsageKind


@dataclass
class FighterFeatures(Trait):
    """Features de clase del Fighter/Guerrero y su estado.

    Un solo rasgo agregado reutiliza el despacho de hooks existente en
    vez de una clase por feature. El estado por combate se limpia en
    ``reset``.
    """

    # Nivel del personaje (manda en las tablas de features).
    level: int = MIN_LEVEL
    # Usos de Tomar Aliento (se crea en ``apply_fighter`` con la tabla).
    second_wind_usage: ActionUsage | None = field(
        default=None, repr=False, compare=False)
    # Usos de Oleada de Acción (nivel 2+; None en nivel 1).
    action_surge_usage: ActionUsage | None = field(
        default=None, repr=False, compare=False)
    # ¿Ya se usó Oleada en el turno actual? (máximo 1 por turno).
    surge_used_this_turn: bool = False
    # Dueño (para que ``reset`` pueda apagar los flags en el combatiente).
    owner: Any = field(default=None, repr=False, compare=False)

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        # «Una vez por turno»: el límite se reinicia al empezar el turno.
        self.surge_used_this_turn = False

    # --- Reinicio -----------------------------------------------------------
    def reset(self) -> None:
        """Un combate nuevo = un día descansado: usos de Tomar Aliento llenos."""
        self.surge_used_this_turn = False
        if self.second_wind_usage is not None:
            self.second_wind_usage.reset()
        if self.action_surge_usage is not None:
            self.action_surge_usage.reset()


# --- Utilidades de acciones ---------------------------------------------------

def _contexto(args: tuple, kwargs: dict) -> Any:
    ctx = kwargs.get("context") or kwargs.get("ctx")
    if ctx is None:
        for a in args:
            if hasattr(a, "actor") and hasattr(a, "rng"):
                return a
    return ctx


def _rasgo(actor: Any) -> FighterFeatures | None:
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, FighterFeatures):
            return trait
    return None


class SecondWindAction(CombatAction):
    """Tomar Aliento (acción bonus): cura 1d10 + nivel gastando un uso.

    Solo es elegible si el combatiente está herido y quedan usos; la
    elegibilidad no consume RNG (el ``pick`` del encuentro decide entre
    las acciones candidatas de forma uniforme).
    """

    def __init__(self) -> None:
        self.name = "Tomar Aliento"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # los usos viven en el rasgo (comparten con Tactical Mind)

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        trait = _rasgo(actor)
        if trait is None or trait.second_wind_usage is None:
            return False
        if not trait.second_wind_usage.available:
            return False
        # Solo si está herido (a PG completos no se gasta el uso).
        try:
            return int(actor.hp) < int(actor.max_hp)
        except Exception:
            return False

    def execute(self, context: Any) -> None:
        actor = context.actor
        trait = _rasgo(actor)
        rng = getattr(context, "rng", None)
        if (trait is None or trait.second_wind_usage is None
                or not trait.second_wind_usage.available or rng is None):
            return  # sin usos o sin RNG el rasgo se abstiene
        curado = int(roll_dice("1d10", rng)) + trait.level
        antes = int(actor.hp)
        actor.hp = min(int(actor.max_hp), antes + curado)
        trait.second_wind_usage.spend()
        _log_line(
            context,
            f"{actor.name} usa Tomar Aliento: {actor.hp - antes} PV "
            f"({trait.second_wind_usage.uses_left} usos)",
        )


class ActionSurgeAction(CombatAction):
    """Oleada de Acción (acción bonus, nivel 2+): restaura la acción del turno.

    Solo es elegible si la acción ya se gastó este turno (así no se gasta
    un uso en vano) y no se ha usado Oleada antes en el mismo turno. Al
    ejecutarse pone ``resources.action_used = False``: el encuentro ve
    la acción libre y ejecuta UNA pasada de acción extra (ver
    ``engine/combat/encounter.py``). La acción Magia no existe en el
    motor, así que la prohibición de PHB no es aplicable aquí.
    """

    def __init__(self) -> None:
        self.name = "Oleada de Acción"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # los usos viven en el rasgo (se restablecen en reset)

    @staticmethod
    def _recursos(args: tuple, kwargs: dict, ctx: Any) -> Any:
        resources = kwargs.get("resources")
        if resources is None:
            for a in args:
                if isinstance(a, TurnResources):
                    resources = a
        if resources is None:
            resources = getattr(ctx, "resources", None)
        return resources

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        trait = _rasgo(actor)
        if (trait is None or trait.level < 2
                or trait.surge_used_this_turn
                or trait.action_surge_usage is None
                or not trait.action_surge_usage.available):
            return False
        resources = self._recursos(args, kwargs, ctx)
        if resources is None:
            return False
        # Solo si la acción de este turno ya se gastó (si no, no aporta).
        return bool(resources.action_used)

    def execute(self, context: Any) -> None:
        actor = context.actor
        trait = _rasgo(actor)
        resources = getattr(context, "resources", None)
        if (trait is None or trait.action_surge_usage is None
                or trait.surge_used_this_turn
                or not trait.action_surge_usage.available
                or resources is None or not resources.action_used):
            return
        trait.action_surge_usage.spend()
        trait.surge_used_this_turn = True
        resources.action_used = False  # el encuentro hará una pasada más
        _log_line(
            context,
            f"{actor.name} usa Oleada de Acción: acción restaurada "
            f"({trait.action_surge_usage.uses_left} usos)",
        )


# --- Aplicación de la clase a un PJ ------------------------------------------

def apply_fighter(pj: Any, skills: tuple[str, ...] = (),
                  level: int | None = None) -> FighterFeatures:
    """Aplica la clase Fighter (Guerrero) a ``pj`` según su nivel.

    - Salvaciones: FUE y CON.
    - ``skills``: validadas contra la lista de la clase (ValueError si no
      está; el recuento de elecciones lo decide quien llama).
    - Tomar Aliento (1): acción bonus con usos por nivel (2/3/4).
    - Oleada de Acción (2): acción bonus que restaura la acción del
      turno (usos 1/2 por nivel).
    - Añade el rasgo :class:`FighterFeatures` y las acciones de la clase.
    """
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))

    pj.save_proficiencies = set(pj.save_proficiencies or set()) | {"str", "con"}

    if skills:
        validas = set(FIGHTER_SKILLS)
        nuevas = set()
        for raw in skills:
            name = normalize_skill(raw)
            if name not in validas:
                raise ValueError(
                    f"{name!r} no es una habilidad de la clase Guerrero: "
                    f"opciones {sorted(validas)}."
                )
            nuevas.add(name)
        pj.skill_proficiencies = set(pj.skill_proficiencies or set()) | nuevas

    trait = FighterFeatures(name="Guerrero", level=lvl)
    trait.owner = pj
    trait.second_wind_usage = ActionUsage(
        UsageKind.PER_DAY, uses_max=second_wind_uses(lvl))
    acciones = [SecondWindAction()]
    if lvl >= 2:  # Oleada de Acción es del nivel 2.
        trait.action_surge_usage = ActionUsage(
            UsageKind.PER_DAY, uses_max=action_surge_uses(lvl))
        acciones.append(ActionSurgeAction())
    pj.traits = list(getattr(pj, "traits", None) or []) + [trait]
    pj.actions = list(pj.actions) + acciones
    return trait


__all__ = ["ActionSurgeAction", "FighterFeatures", "SecondWindAction",
           "apply_fighter"]

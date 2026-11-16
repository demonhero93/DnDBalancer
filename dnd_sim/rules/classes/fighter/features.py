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
- **Tactical Mind** (2): al fallar una prueba de característica con
  ``ctx``, decide con ``pick`` si gasta un uso de Tomar Aliento para
  sumar ``1d10``; el uso SOLO se gasta si la tirada final tiene éxito
  (hook ``after_failed_check``; sin usos o sin fallo, sin RNG).
- **Oleada de Acción**: restaura el recurso de acción del turno
  (``TurnResources.action_used = False``) y el encuentro ejecuta una
  pasada de acción extra; máximo 1 uso por turno, solo si la acción ya
  se gastó (si no, se quedaría sin efecto) y nunca en la acción Magia
  (acción que el motor no tiene). Recarga por descanso = solo al
  empezar un combate nuevo (``reset``).
- **Estilo de Combate** (1): elección con ``pick`` uniforme en
  ``apply_fighter`` (``fighting_style`` explícito o ``rng``; sin rng,
  semilla fija 0). Implementados: Archery (+2 a la tirada a distancia,
  ``AttackModifiers.bonus``), Defense (+1 CA, armadura dada por
  supuesta), Dueling (+2 daño cuerpo a cuerpo sin propiedad
  ``two-handed``, sin saber si hay otra arma en la mano), Great Weapon
  Fighting (dados de 1 o 2 cuentan como 3 en golpes cuerpo a cuerpo con
  arma ``two-handed``; ``versatile`` a dos manos no es modelable),
  Thrown Weapon Fighting (+2 si el arma tiene la propiedad ``thrown``),
  Protection (reacción: desventaja al atacante contra un aliado a 5
  pies; exige escudo, dato ``tiene_escudo``) e Interception (reacción:
  reduce el daño a un aliado a 5 pies con ``1d10 + PB``; requiere
  escudo o arma). Blind Fighting y Unarmed Fighting: dato sin efecto
  (sin sistema de visibilidad; el PJ elige armas). Two-Weapon Fighting:
  dato sin efecto hasta que exista el ataque adicional (TODO.md).
- **Ataques Estudiados** (13): un fallo marca al objetivo (clave por
  nombre) hasta el final de tu siguiente turno; el PRÓXIMO ataque
  contra él tiene ventaja y la consume, acierte o falle. La caducidad
  se mide en turnos propios (``on_turn_start``).
- Las decisiones con azar (estilo de combate, Second Wind, Action
  Surge, Indomitable...) se toman con ``core.randomness.pick`` uniforme
  y no consumen RNG cuando solo hay una opción.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from ....core.classes import (
    FIGHTER_SKILLS,
    FIGHTER_STYLES,
    MAX_LEVEL,
    MIN_LEVEL,
    action_surge_uses,
    fighter_extra_attacks_for,
    indomitable_uses,
    second_wind_uses,
    weapon_mastery_count,
)
from ....core.dice import roll_dice
from ....core.enums import AttackRange
from ....core.log import log_line as _log_line
from ....core.proficiency import proficiency_bonus
from ....core.randomness import pick, sample
from ....core.skills import normalize_skill
from ....model.actions import (
    ActionType,
    AttackEntry,
    CombatAction,
    MultiattackAction,
    TurnResources,
)
from ...checks import CheckResult
from ...mastery import maestria_de
from ...saves import SaveResult, saving_throw
from ...traits.base import Trait
from ...usage import ActionUsage, UsageKind

#: RNG con semilla fija para elegir el Estilo de Combate cuando el
#: llamante no pasa ``rng``: crea el personaje siempre igual (reproducible).
_RNG_CREACION = random.Random(0)

#: Cobertura abstracta de «a 5 pies» para Protection/Interception: el
#: modelo no guarda posiciones, así que se asume cobertura total
#: (patrón wild_heart con p=1.0: no consume RNG).
_COBERTURA_5_PIES = 1.0


def _en_5_pies(rng: Any) -> bool:
    """¿Está a 5 pies? (cobertura abstracta, sin posiciones)."""
    p = _COBERTURA_5_PIES
    if p <= 0.0:
        return False
    if p >= 1.0:
        return True
    if rng is None:
        return True  # sin RNG: cobertura completa (no inventa tiradas)
    return rng.random() < p


def _es_aliado(owner: Any, criatura: Any) -> bool:
    """¿``criatura`` es un aliado vivo de ``owner``? (sin cobertura)."""
    if criatura is None or criatura is owner:
        return False
    if not getattr(criatura, "alive", True):
        return False
    hostil = getattr(owner, "is_hostile_to", None)
    if hostil is not None and hostil(criatura):
        return False
    return True


@dataclass
class FighterFeatures(Trait):
    """Features de clase del Fighter/Guerrero y su estado.

    Un solo rasgo agregado reutiliza el despacho de hooks existente en
    vez de una clase por feature. El estado por combate se limpia en
    ``reset``.
    """

    # Nivel del personaje (manda en las tablas de features).
    level: int = MIN_LEVEL
    # Niveles de ASI (4/6/8/12/14/16): dato de tabla, sin efecto en el
    # modelo (el PJ se define en código con sus características finales).
    asi_levels: tuple[int, ...] = (4, 6, 8, 12, 14, 16)
    # Nivel del Don Épico (19): dato de tabla, sin efecto (igual que ASI).
    epic_boon_level: int = 19
    # Estilo de Combate elegido (1): clave en ``FIGHTER_STYLES``.
    estilo: str | None = None
    # Estilos adicionales (Additional Fighting Style, Champion 7):
    # vacío por defecto; los hooks consultan la propiedad ``estilos``.
    estilos_extra: list[str] = field(default_factory=list, repr=False,
                                     compare=False)
    # ¿Lleva escudo? (dato: el modelo no guarda equipo; quien construye
    # el PJ lo activa. Protection lo exige; Interception escudo o arma.)
    tiene_escudo: bool = False
    # Usos de Tomar Aliento (se crea en ``apply_fighter`` con la tabla).
    second_wind_usage: ActionUsage | None = field(
        default=None, repr=False, compare=False)
    # Usos de Oleada de Acción (nivel 2+; None en nivel 1).
    action_surge_usage: ActionUsage | None = field(
        default=None, repr=False, compare=False)
    # ¿Ya se usó Oleada en el turno actual? (máximo 1 por turno).
    surge_used_this_turn: bool = False
    # Usos de Indomitable (nivel 9+; None por debajo).
    indomitable_usage: ActionUsage | None = field(
        default=None, repr=False, compare=False)
    # Ataques Estudiados (13): nombre del objetivo → turno en que caduca.
    ataques_estudiados: dict[str, int] = field(
        default_factory=dict, repr=False, compare=False)
    # Contador de turnos propios (para la caducidad de la línea anterior).
    turno_guerrero: int = 0
    # Maestría con Armas (1): N armas elegidas (nombres); ``apply_fighter``
    # marca ``atk.mastery`` de cada ataque elegido con la propiedad de la
    # tabla. No es estado de combate: no se limpia en ``reset``.
    maestrias: list[str] = field(
        default_factory=list, repr=False, compare=False)
    # Dueño (para que ``reset`` pueda apagar los flags en el combatiente).
    owner: Any = field(default=None, repr=False, compare=False)

    @property
    def estilos(self) -> tuple[str, ...]:
        """Estilos de Combate activos: el principal y los adicionales.

        Los hooks de cada estilo comprueban pertenencia al conjunto, de
        modo que los dos estilos de Champion (7) funcionan a la vez.
        El atributo ``estilo`` (principal) sigue intacto para los tests
        y las mutaciones de ``apply_fighter`` (Defense: +1 CA una sola
        vez, al aplicar el estilo que corresponda).
        """
        return tuple(s for s in (self.estilo, *self.estilos_extra) if s)

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        # «Una vez por turno»: el límite se reinicia al empezar el turno.
        self.surge_used_this_turn = False
        # Ataques Estudiados: la marca vive hasta el fin del siguiente
        # turno propio (se marca en el turno N → caduca en N+2).
        self.turno_guerrero += 1
        for nombre in [n for n, caduca in self.ataques_estudiados.items()
                       if caduca <= self.turno_guerrero]:
            del self.ataques_estudiados[nombre]

    # --- Estilos de combate (1) ----------------------------------------------
    def damage_dice_upgrades(self, attacker: Any, atk: Any,
                             rango: Any = None, ctx: Any = None,
                             rng: Any = None) -> int:
        """Great Weapon Fighting: los dados de 1 o 2 del golpe cuentan como 3.

        Solo armas con la propiedad ``two-handed`` a cuerpo a cuerpo: el
        motor no guarda si una arma ``versatile`` se empuña a dos manos,
        así que ese caso queda sin modelar (decisión documentada).
        """
        if ("Great Weapon Fighting" not in self.estilos
                or attacker is not self.owner or atk is None
                or rango is not AttackRange.MELEE):
            return 0
        props = set(getattr(atk, "properties", None) or set())
        if "two-handed" not in props:
            return 0
        return 3

    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            *, crit: bool = False, ctx: Any = None,
                            rng: Any = None, atk: Any = None) -> int:
        """Dueling (+2 cuerpo a cuerpo a una mano) y Thrown (+2 arrojadizo)."""
        if attacker is not self.owner or atk is None:
            return 0
        props = set(getattr(atk, "properties", None) or set())
        if "Thrown Weapon Fighting" in self.estilos and "thrown" in props:
            return 2
        if ("Dueling" in self.estilos and rango is AttackRange.MELEE
                and "two-handed" not in props):
            return 2
        return 0

    def grant_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                               rango: Any, ctx: Any = None,
                               rng: Any = None, atk: Any = None) -> None:
        """Protection (reacción): desventaja al atacante contra un aliado.

        Requiere escudo (dato ``tiene_escudo``), aliado vivo del
        guardián a 5 pies (cobertura abstracta), atacante y objetivo
        distintos del guardián y su reacción libre. La decisión de usar
        la reacción es un ``pick`` uniforme; sin RNG el rasgo se
        abstiene sin consumir azar.
        """
        if "Protection" not in self.estilos or not self.tiene_escudo:
            return None
        owner = self.owner
        if owner is None or attacker is owner or target is owner:
            return None
        if not _es_aliado(owner, target):
            return None
        estado = getattr(owner, "state", None)
        if estado is not None and getattr(estado, "reaction_used", False):
            return None  # su reacción de este turno ya está gastada
        if rng is None:
            return None  # sin RNG el rasgo se abstiene
        if not _en_5_pies(rng):
            return None
        if pick(rng, ("no", "si")) == "no":
            return None  # decisión aleatoria de gastar la reacción
        if estado is not None:
            estado.reaction_used = True
        mods.disadvantage_sources.append("Protección")
        _log_line(ctx, f"{getattr(owner, 'name', owner)} usa Protección "
                       f"contra {getattr(attacker, 'name', attacker)}")
        return None

    def reduce_damage_to_allies(self, target: Any, amount: int,
                                damage_type: Any = None,
                                source: Any = None,
                                ctx: Any = None) -> int | None:
        """Interception (reacción): reduce el daño a un aliado con 1d10+PB.

        Requiere escudo o arma en mano (dato ``tiene_escudo`` o ataques
        del PJ), aliado vivo distinto del guardián a 5 pies (cobertura
        abstracta) y reacción libre. La decisión de usar la reacción es
        un ``pick`` uniforme; sin RNG el rasgo se abstiene. Devuelve el
        daño restante (mínimo 0), como Spirit Shield.
        """
        if "Interception" not in self.estilos:
            return None
        owner = self.owner
        if owner is None or target is None or target is owner:
            return None
        if not _es_aliado(owner, target):
            return None
        if not (self.tiene_escudo or getattr(owner, "attacks", None)
                or getattr(owner, "weapons", None)):
            return None  # sin escudo ni arma no hay con qué interceptar
        estado = getattr(owner, "state", None)
        if estado is not None and getattr(estado, "reaction_used", False):
            return None  # su reacción de este turno ya está gastada
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return None  # sin RNG el rasgo se abstiene
        if not _en_5_pies(rng):
            return None
        if pick(rng, ("no", "si")) == "no":
            return None  # decisión aleatoria de gastar la reacción
        reducido = min(int(amount),
                       int(roll_dice("1d10", rng)) + proficiency_bonus(self.level))
        if reducido <= 0:
            return None
        if estado is not None:
            estado.reaction_used = True
        _log_line(ctx, f"{getattr(owner, 'name', owner)} usa Intercepción: "
                       f"reduce {reducido} de daño a "
                       f"{getattr(target, 'name', target)}")
        return max(0, int(amount) - reducido)

    # --- Ataques Estudiados (13) ----------------------------------------------
    def after_attack_roll(self, attacker: Any, target: Any, atk: Any,
                          hit: bool, ctx: Any = None,
                          rng: Any = None) -> None:
        """Un fallo contra ``target`` da ventaja en el siguiente ataque."""
        if self.level < 13 or hit or attacker is not self.owner:
            return None
        nombre = getattr(target, "name", None)
        if not nombre:
            return None
        self.ataques_estudiados[nombre] = self.turno_guerrero + 2
        return None

    def modify_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                                rango: Any, ctx: Any = None,
                                rng: Any = None, atk: Any = None) -> None:
        """Archery: +2 a distancia. Ataques Estudiados: ventaja marcada."""
        if attacker is not self.owner:
            return None
        if "Archery" in self.estilos and rango is AttackRange.RANGED:
            mods.bonus += 2
        if self.level < 13:
            return None
        nombre = getattr(target, "name", None)
        if not nombre or nombre not in self.ataques_estudiados:
            return None
        if self.ataques_estudiados[nombre] <= self.turno_guerrero:
            del self.ataques_estudiados[nombre]  # caducada
            return None
        mods.advantage_sources.append("Ataques Estudiados")
        del self.ataques_estudiados[nombre]  # solo el siguiente ataque
        return None

    # --- Indomitable (9) -----------------------------------------------------
    def after_failed_save(self, target: Any, ability: str, result: Any,
                          ctx: Any = None) -> Any:
        """Repite la salvación fallida con bonificador = nivel (usos 1/2/3).

        La tirada nueva SUSTITUYE a la original (patrón Fanatical Focus):
        ``saving_throw`` anida sin re-despachar el hook, así que no hay
        recursión. Decisión aleatoria con ``pick``; sin usos o sin RNG el
        rasgo se abstiene sin consumir azar.
        """
        if self.level < 9 or target is not self.owner or result is None:
            return None
        if (self.indomitable_usage is None
                or not self.indomitable_usage.available):
            return None
        if getattr(result, "auto_fail", False):
            return None  # el fallo automático no se repite
        rng = getattr(ctx, "rng", None) if ctx is not None else None
        if rng is None:
            return None  # sin RNG el rasgo se abstiene
        if pick(rng, ("no", "si")) == "no":
            return None  # decisión aleatoria de repetirla
        self.indomitable_usage.spend()
        nuevo = saving_throw(target, result.ability, result.dc, rng)
        bonus = self.level
        total = int(nuevo.total) + bonus
        dc = int(result.dc)
        salida = SaveResult(
            ability=result.ability,
            dc=dc,
            rolls=list(nuevo.rolls),
            bonus=int(nuevo.bonus) + bonus,
            total=total,
            success=total >= dc,
            mode=nuevo.mode,
        )
        _log_line(ctx, f"{getattr(target, 'name', target)} repite la "
                       f"salvación {str(result.ability).upper()} con "
                       f"Indomitable ({total} vs CD {dc})")
        return salida

    # --- Tactical Mind (2) ---------------------------------------------------
    def after_failed_check(self, target: Any, ability: str, result: Any,
                           ctx: Any = None) -> Any:
        """Tactical Mind: gasta un uso de Tomar Aliento para sumar +1d10.

        Solo pruebas de característica falladas (el hook no se dispara en
        salvaciones ni ataques). Decisión aleatoria con ``pick``; sin usos
        de Tomar Aliento, con la prueba ya superada o sin ``ctx``/RNG el
        rasgo se abstiene sin consumir azar. El uso SOLO se gasta si la
        tirada final tiene éxito (si aun así falla, el uso queda).
        """
        if self.level < 2 or target is not self.owner or result is None:
            return None
        if getattr(result, "success", False):
            return None
        if (self.second_wind_usage is None
                or not self.second_wind_usage.available):
            return None
        rng = getattr(ctx, "rng", None) if ctx is not None else None
        if rng is None:
            return None  # sin RNG el rasgo se abstiene
        if pick(rng, ("no", "si")) == "no":
            return None  # decisión aleatoria de intentarlo
        d10 = int(roll_dice("1d10", rng))
        dc = int(result.dc)
        total = int(result.total) + d10
        salida = CheckResult(
            ability=result.ability,
            dc=dc,
            rolls=[*list(result.rolls), d10],
            bonus=int(result.bonus),
            total=total,
            success=total >= dc,
            mode=result.mode,
            skill=getattr(result, "skill", None),
        )
        nombre = getattr(target, "name", target)
        if salida.success:
            self.second_wind_usage.spend()
            _log_line(ctx, f"{nombre} usa Tactical Mind y gasta un uso de "
                           f"Tomar Aliento (+{d10} → {total} vs CD {dc})")
        else:
            _log_line(ctx, f"{nombre} usa Tactical Mind (+{d10} → {total} "
                           f"vs CD {dc}): el uso no se gasta")
        return salida

    # --- Tactical Master (9) -------------------------------------------------
    def sustituir_maestria(self, base: str, rng: Any = None) -> str:
        """Tactical Master: sustituye la maestría por Push, Sap o Slow.

        Consultado por :func:`dnd_sim.rules.mastery.resolver_maestria`
        en CADA ataque con maestría: decide con ``pick`` uniforme entre
        la propiedad original y ``push``/``sap``/``slow``. Bajo el nivel
        9 o sin ``rng`` devuelve la original sin consumir azar. La
        sustitución solo dura ese ataque (el campo ``Attack.mastery`` no
        cambia). Como Push y Slow no tienen efecto en el motor (sin
        movimiento ni posiciones), solo Sap y la original alteran el
        combate (decisión documentada en TODO.md).
        """
        if self.level < 9 or rng is None:
            return base
        return pick(rng, (base, "push", "sap", "slow"))

    # --- Reinicio -----------------------------------------------------------
    def reset(self) -> None:
        """Un combate nuevo = un día descansado: usos de Tomar Aliento llenos."""
        self.surge_used_this_turn = False
        self.ataques_estudiados.clear()
        self.turno_guerrero = 0
        if self.second_wind_usage is not None:
            self.second_wind_usage.reset()
        if self.action_surge_usage is not None:
            self.action_surge_usage.reset()
        if self.indomitable_usage is not None:
            self.indomitable_usage.reset()


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
    ``engine/combat/encounter.py``) que EXCLUYE las acciones de hechizo
    de PJ (``es_accion_magia``): la Oleada no puede lanzar conjuros
    (PHB).
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
                  level: int | None = None,
                  rng: random.Random | None = None,
                  fighting_style: str | None = None,
                  tiene_escudo: bool = False) -> FighterFeatures:
    """Aplica la clase Fighter (Guerrero) a ``pj`` según su nivel.

    - Salvaciones: FUE y CON.
    - ``skills``: validadas contra la lista de la clase (ValueError si no
      está; el recuento de elecciones lo decide quien llama).
    - Estilo de Combate (1): ``fighting_style`` explícito o ``pick``
      uniforme entre los implementados (con ``rng`` del llamante; sin él,
      semilla fija 0 para crear siempre el mismo personaje).
    - ``tiene_escudo``: dato que quien construye el PJ activa si lleva
      escudo (Protection lo exige; Interception escudo o arma).
    - Tomar Aliento (1): acción bonus con usos por nivel (2/3/4).
    - Oleada de Acción (2): acción bonus que restaura la acción del
      turno (usos 1/2 por nivel).
    - Extra Attack (5/11/20): 2/3/4 golpes con la acción Atacar.
    - Indomitable (9): hook ``after_failed_save`` que repite la
      salvación con bonificador = nivel (usos 1/2/3 por nivel).
    - Ataques Estudiados (13): ventaja en el siguiente ataque contra el
      objetivo de una tirada fallida, hasta el fin del siguiente turno.
    - Maestría con Armas (1): elige N armas (3/4/5/6 por nivel) y
      marca sus ataques con la propiedad de la tabla de
      ``rules/mastery.py`` (el motor ya la aplica); armas sin entrada
      en la tabla quedan sin maestría y sin error.
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

    # Estilo de Combate (1): validación antes de tocar al personaje.
    estilo = fighting_style
    if estilo is not None:
        if estilo not in FIGHTER_STYLES:
            raise ValueError(
                f"{estilo!r} no es un Estilo de Combate de la clase "
                f"Guerrero: opciones {sorted(FIGHTER_STYLES)}."
            )
    else:
        estilo = pick(rng if rng is not None else _RNG_CREACION,
                      FIGHTER_STYLES)

    # Extra Attack (5/11/20): 2/3/4 golpes con la acción Atacar
    # (mismo patrón que el bárbaro: atributo extra_attacks si el PJ
    # usa armas, si no un Multiattack con los golpes ciclados).
    golpes = fighter_extra_attacks_for(lvl)
    if golpes > 1:
        if getattr(pj, "weapons", None):
            pj.extra_attacks = max(int(pj.extra_attacks), golpes - 1)
        else:
            from ....model.actions import AttackAction
            ataques = [a for a in pj.attacks
                       if not getattr(a, "only_in_multiattack", False)] or list(pj.attacks)
            if ataques:
                entradas = [
                    AttackEntry(ataques[i % len(ataques)].name, count=1)
                    for i in range(golpes)
                ]
                multi = MultiattackAction([entradas])
                restantes = [a for a in pj.actions
                             if not isinstance(a, AttackAction)]
                restantes.append(multi)
                pj.actions = restantes

    trait = FighterFeatures(name="Guerrero", level=lvl, estilo=estilo,
                            tiene_escudo=tiene_escudo)
    trait.owner = pj
    # Maestría con Armas (1): selección de N armas y marca de SU clave
    # de la tabla en el objeto Attack (mutación in-place: las acciones
    # guardan el mismo objeto). Pool de ``weapons`` o, si el PJ no los
    # usa, de sus ataques; sin ninguno, lista vacía.
    pool = list(pj.weapons or []) or list(pj.attacks or [])
    trait.maestrias = [
        atk.name for atk in sample(
            rng if rng is not None else _RNG_CREACION,
            pool,
            weapon_mastery_count(lvl),
        )
    ]
    # Los ataques elegidos reciben su propiedad (Topple, Sap...). Los no
    # elegidos NO se tocan (un arma que ya traiga clave la conserva) y un
    # nombre fuera de la tabla queda sin maestría y sin error.
    elegidas = set(trait.maestrias)
    for lista in (pj.attacks, pj.weapons):
        for atk in lista or ():
            clave = maestria_de(atk.name)
            if clave and atk.name in elegidas:
                atk.mastery = clave
    if estilo == "Defense":
        # Defense (+1 CA): el modelo no guarda armadura equipada, se da
        # por supuesta (mismo criterio que Battlerager con su armadura).
        pj.ac += 1
    trait.second_wind_usage = ActionUsage(
        UsageKind.PER_DAY, uses_max=second_wind_uses(lvl))
    acciones = [SecondWindAction()]
    if lvl >= 2:  # Oleada de Acción es del nivel 2.
        trait.action_surge_usage = ActionUsage(
            UsageKind.PER_DAY, uses_max=action_surge_uses(lvl))
        acciones.append(ActionSurgeAction())
    if lvl >= 9:  # Indomitable es del nivel 9 (sin acción propia).
        trait.indomitable_usage = ActionUsage(
            UsageKind.PER_DAY, uses_max=indomitable_uses(lvl))
    pj.traits = list(getattr(pj, "traits", None) or []) + [trait]
    pj.actions = list(pj.actions) + acciones
    return trait


__all__ = ["ActionSurgeAction", "FighterFeatures", "SecondWindAction",
           "apply_fighter"]

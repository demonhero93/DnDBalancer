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
  (campo propio ``marca_cavalier`` en ``CombatState``). Si la criatura
  marcada daña a un tercero, ``inflict_damage`` llama a
  :meth:`CavalierFeatures.marcar_ataque_especial` y, en el SIGUIENTE
  turno del dueño, :class:`CavalierMarkAttackAction` (acción bonus)
  hace un ataque cuerpo a cuerpo con ventaja forzada y daño extra
  ``nivel // 2`` si impacta. Sin monturas ni movimiento: la velocidad 0
  de la marca es dato sin efecto.
- **Warding Maneuver** (7): ``defensa_ante_ataque`` (hook registrado en
  ``HOOK_NAMES``) devuelve 1d8 de CA —el motor recalcula el impacto— y
  resistencia si el golpe sigue entrando (concesión temporal al tipo
  durante ``apply_damage_modifiers``, sin acumularse). Reacción
  compartida; requiere escudo o arma cuerpo a cuerpo.
- **Hold the Line** (10): ``ataque_de_oportunidad`` (duck-typing, sin
  ``HOOK_NAMES``) —reinterpretación documentada: en lugar del ataque
  de oportunidad por movimiento (el sim no tiene movimiento), un
  ataque de reacción cuando un enemigo ataca con tirada a un aliado
  distinto del dueño; contraataque cuerpo a cuerpo con la reacción
  compartida. La velocidad 0 es dato sin efecto.
- **Vigilant Defender** (18): segunda reacción por ronda
  (``especial_usada_en_ronda`` comparada con ``ctx.round``)
  exclusiva de Hold the Line, consumida antes que la normal y solo
  fuera del turno propio; la restricción «mismo turno que otra
  reacción» es simplificación (sin identificador de turno ajeno).

- **Ferocious Charger** (15): ``_evaluar_carga`` en
  ``after_attack_roll`` —evaluación única por turno del primer
  impacto cuerpo a cuerpo con probabilidad fija ``charge_probability``
  (``--charge-p``, patrón Reckless; 0.0/1.0 sin RNG)— → ``pick`` y
  salvación de FUE CD 8 + PB + mod FUE; fallo → PRONE (EscapeCheck de
  Topple). El flag se limpia en ``on_turn_start``.

Ver ``TODO.md`` (plan «Cavalier», casillas B y Verificación) y las
entradas de ``PASOS-ANTERIORES.txt``.
"""
from __future__ import annotations

import copy
import random
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Any

from .....core.classes import (
    CAVALIER_BONUS_SKILLS,
    CHARGE_MOVE_PROBABILITY,
    MAX_LEVEL,
    MIN_LEVEL,
    cavalier_mark_extra_damage,
    cavalier_mark_uses,
    warding_maneuver_uses,
)
from .....core.dice import roll_dice
from .....core.enums import AttackRange
from .....core.log import log_line as _log_line
from .....core.randomness import pick
from .....model.actions import ActionType, CombatAction
from ....conditions import Condition, EscapeCheck, apply_condition
from ....saves import registrar_resistencia, saving_throw
from ....traits.base import Trait
from ....usage import ActionUsage, UsageKind
from .._util import _de
from ..features import FighterFeatures, _contexto, _es_aliado

#: RNG con semilla fija para Bonus Proficiency cuando no pasa ``rng``:
#: crea el personaje siempre igual (reproducible), patrón Battle Master.
_RNG_CREACION = random.Random(0)


def _armas_melee_de(criatura: Any) -> tuple:
    """Ataques cuerpo a cuerpo propios (sin RNG; vacío si no hay).

    Mismo criterio que ``battle_master._armas_melee_propias``:
    ``attacks`` si existe, si no ``weapons`` + ``dynamic_weapons``.
    """
    ataques = list(getattr(criatura, "attacks", None) or []) or (
        list(getattr(criatura, "weapons", None) or [])
        + list(getattr(criatura, "dynamic_weapons", None) or []))
    return tuple(a for a in ataques
                 if getattr(a, "range_type", None) is AttackRange.MELEE)


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
    #: Vigilant Defender (18): ronda en que se gastó la reacción
    #: especial (0 = nunca). Se compara con ``ctx.round``: así se
    #: «restablece» sola al empezar cada ronda, sin hook de ronda.
    especial_usada_en_ronda: int = 0
    #: Ataque especial de Unwavering Mark (A4): turno propio en el que
    #: vale el flag (``turno_cavalier + 1`` al armar; 0 = sin flag).
    ataque_marca_pendiente: int = 0
    #: Criatura marcada contra la que vale el ataque especial.
    ataque_marca_objetivo: Any = None
    #: Dueño (para que ``reset``/hooks encuentren al combatiente).
    owner: Any = field(default=None, repr=False, compare=False)

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        # Contador de turnos propios y flag «una vez por turno» de la
        # carga (Ferocious Charger). El flag del ataque especial NO se
        # toca aquí: debe sobrevivir hasta su turno válido.
        self.turno_cavalier += 1
        self.carga_evaluada = False

    def reset(self) -> None:
        self.turno_cavalier = 0
        self.carga_evaluada = False
        self.ataque_marca_pendiente = 0
        self.ataque_marca_objetivo = None
        self.especial_usada_en_ronda = 0
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
        # Ferocious Charger (15): evaluación de movimiento única por
        # turno sobre el PRIMER impacto cuerpo a cuerpo (patrón
        # RECKLESS/`--charge-p`). Vive antes del guard de melee para
        # poder descartar ataques a distancia sin marcar la bandera.
        self._evaluar_carga(target, atk, ctx=ctx, rng=rng)
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

    # --- Ferocious Charger (15): salvación de FUE al cargar -------------------
    def _evaluar_carga(self, target: Any, atk: Any, *, ctx: Any = None,
                       rng: Any = None) -> None:
        """Evalúa la carga una vez por turno sobre el primer impacto melee.

        Simplificación documentada: el movimiento por turno se simula con
        la probabilidad fija ``charge_probability`` (``--charge-p``,
        patrón ``RECKLESS_USE_PROBABILITY``): 0.0/1.0 no consumen RNG y
        con el resto UN ``rng.random()``. Guards SIN RNG ANTES de todo:
        nivel < 15, bandera ya puesta, ataque no cuerpo a cuerpo (la
        bandera NO se pega: un disparo no evalúa), incapacitado o sin
        rng (se abstiene y podrá decidir después, patrón Reckless).
        Si hay carga, ``pick`` «no»/«sí» («no» no fuerza nada); si
        «sí», salvación de FUE CD 8 + PB + mod FUE con el camino de
        ``saving_throw``/``registrar_resistencia``; fallo → PRONE con
        el ``EscapeCheck`` de Topple. Por debajo del nivel 15 no
        actúa; el flag se limpia en ``on_turn_start``.
        """
        if self.level < 15 or self.carga_evaluada:
            return None
        if target is None or getattr(atk, "range_type", None) is not AttackRange.MELEE:
            return None
        owner = self.owner
        if owner is None or not getattr(owner, "can_act", True):
            return None
        p = float(self.charge_probability)
        if 0.0 < p < 1.0 and rng is None:
            return None  # sin RNG el rasgo se abstiene (podrá decidir después)
        self.carga_evaluada = True
        if p <= 0.0:
            hay_carga = False
        elif p >= 1.0:
            hay_carga = True
        else:
            hay_carga = rng.random() < p
        if not hay_carga:
            return None
        if pick(rng, ("no", "si")) == "no":
            return None  # no fuerza la salvación
        cd = (8 + int(getattr(owner, "proficiency", 0) or 0)
              + int(owner.abilities.mod("str")))
        sr = saving_throw(target, "str", cd, rng)
        registrar_resistencia(ctx, target, sr)
        if sr.success:
            return None
        apply_condition(target, Condition.PRONE, ctx, source=owner,
                        escape=EscapeCheck(abilities=("str", "dex"), dc=10,
                                           consumes_action=False))
        _log_line(ctx, f"{getattr(owner, 'name', owner)} derriba con una "
                       f"carga a {getattr(target, 'name', target)} "
                       f"(salvación de FUE CD {cd})")
        return None

    # --- Unwavering Mark (3): ataque especial ----------------------------------
    def marcar_ataque_especial(self, marcado: Any,
                               ctx: Any = None) -> None:
        """Arma el ataque especial de la marca para el próximo turno propio.

        Lo llama ``inflict_damage`` (punto central con fuente) cuando
        ``marcado`` —una criatura marcada por este Cavalier— daña a un
        tercero. Sin RNG: solo guarda el flag con el patrón de turnos
        de Studied Attacks (``turno_cavalier + 1`` = siguiente turno
        propio; un disparo durante el propio turno vale ya para el
        siguiente). El último disparo gana si hay varias criaturas
        marcadas.
        """
        self.ataque_marca_pendiente = self.turno_cavalier + 1
        self.ataque_marca_objetivo = marcado
        return None

    # --- Warding Maneuver (7): defensa de reacción ----------------------------
    def defensa_ante_ataque(self, target: Any, attacker: Any, rango: Any,
                            total: int | None = None,
                            ca: int | None = None,
                            ctx: Any = None,
                            rng: Any = None) -> Any:
        """Warding Maneuver: 1d8 de CA y resistencia si el golpe sigue.

        Lo llama el motor (hook ``defensa_ante_ataque``, punto de
        consulta de CA ampliado a los aliados del objetivo) cuando el
        ataque iba a impactar o es crítico. Guards SIN RNG en orden:
        nivel < 7, sin owner/objetivo/atacante/rng, objetivo que no
        sea el dueño ni un aliado vivo, dueño muerto/incapacitado, sin
        escudo ni arma cuerpo a cuerpo (dato ``tiene_escudo`` del
        Guerrero), sin usos o reacción ya gastada. Decisión ``pick``
        «no»/«sí» («no» no gasta nada); el 1d8 se tira UNA vez y el
        resultado ``SimpleNamespace(ac_extra, resistencia)`` alimenta
        el recálculo de CA y, si el golpe sigue entrando, la resistencia
        temporal que aplica el motor (mitad, sin acumularse con la
        resistencia previa del tipo). Gasta reacción y un uso. Los 5
        pies del enunciado no se modelan: el sim no guarda posiciones,
        así que basta con que el objetivo sea el dueño o un aliado
        vivo (decisión documentada, con test freeze).
        """
        if self.level < 7:
            return None
        owner = self.owner
        if owner is None or target is None or attacker is None or rng is None:
            return None
        if target is not owner and not _es_aliado(owner, target):
            return None
        if not getattr(target, "alive", True):
            return None
        if not getattr(owner, "alive", True) or not getattr(
                owner, "can_act", True):
            return None
        fighter = _de(owner, FighterFeatures)
        escudo = bool(fighter is not None
                      and getattr(fighter, "tiene_escudo", False))
        if not escudo and not _armas_melee_de(owner):
            return None  # sin escudo ni arma cuerpo a cuerpo no hay con qué
        if self.warding_usos is None or not self.warding_usos.available:
            return None
        if owner.state.reaction_used:
            return None
        if pick(rng, ("no", "si")) == "no":
            return None
        owner.state.reaction_used = True
        self.warding_usos.spend()
        valor = int(roll_dice("1d8", rng))
        _log_line(ctx, f"{getattr(owner, 'name', owner)} usa Warding "
                       f"Maneuver: +{valor} de CA a "
                       f"{getattr(target, 'name', target)}")
        return SimpleNamespace(ac_extra=valor, resistencia=True)

    # --- Hold the Line (10): ataque de oportunidad abstracto -----------------
    def ataque_de_oportunidad(self, attacker: Any, target: Any, *,
                              ctx: Any = None, rng: Any = None,
                              log: Any = None) -> None:
        """Hold the Line: ataque de reacción contra el atacante de un aliado.

        Reinterpretación documentada: en las reglas la criatura
        provoca el ataque al moverse dentro del alcance; el sim no
        tiene movimiento, así que el «ataque de oportunidad abstracto»
        se dispara cuando un enemigo hace un ataque con tirada —impacte
        o falle— contra un aliado vivo distinto del dueño. Lo llama el
        motor (duck-typing ``_oportunidad_contra_bando``, sin entrada
        en ``HOOK_NAMES``) tras resolver la tirada; los hechizos de
        salvación y el área no lo disparan.

        Guards SIN RNG en orden: nivel < 10, sin ctx/rng/atacante u
        objetivo, reentrada (``ctx.is_reaction``: un ataque de
        reacción no dispara otro), dueño muerto/incapacitado, atacante
        muerto o no enemigo del dueño, objetivo que no sea un aliado
        vivo distinto del dueño, sin reacción disponible (Vigilant
        Defender: reacción especial por ronda consumida ANTES que la
        normal), sin ataque cuerpo a cuerpo propio. Decisión ``pick``
        «no»/«sí» («no» no gasta nada); arma con ``pick`` uniforme
        (sin RNG si solo hay una); gasta la reacción y contraataca
        con ``is_reaction`` en el ctx copiado. La velocidad 0 hasta el
        final del turno del atacante es dato sin efecto: el sim no
        modela velocidad.
        """
        if self.level < 10:
            return None
        if ctx is None or rng is None or attacker is None or target is None:
            return None
        if getattr(ctx, "is_reaction", False):
            return None  # reentrada: un ataque de reacción no dispara otro
        owner = self.owner
        if owner is None or not getattr(owner, "alive", True) or not getattr(
                owner, "can_act", True):
            return None
        if not getattr(attacker, "alive", True):
            return None
        hostil = getattr(owner, "is_hostile_to", None)
        if hostil is None or not hostil(attacker):
            return None  # solo contra enemigos del dueño
        if target is owner or not _es_aliado(owner, target):
            return None  # solo aliados vivos distintos del dueño
        # Vigilant Defender (18): reacción especial por ronda, EXCLUSIVA
        # de esta oportunidad, consumida antes que la normal y solo
        # fuera del turno propio. Simplificación documentada: la
        # restricción «no usarla en el mismo turno en que gastaste otra
        # reacción» no se aplica porque no hay identificador de turno
        # ajeno barato en ctx.
        estado = getattr(owner, "state", None)
        ronda = getattr(ctx, "round", None)
        especial = (self.level >= 18 and ronda is not None
                    and getattr(ctx, "actor", None) is not owner
                    and int(ronda) != self.especial_usada_en_ronda)
        if not especial and estado is not None and estado.reaction_used:
            return None  # sin especial ni reacción normal libre
        armas = _armas_melee_de(owner)
        if not armas:
            return None
        if pick(rng, ("no", "si")) == "no":
            return None
        arma = pick(rng, armas)  # sin RNG si solo hay una
        if especial:
            self.especial_usada_en_ronda = int(ronda)
        elif estado is not None:
            estado.reaction_used = True
        _log_line(ctx, f"{getattr(owner, 'name', owner)} usa Hold the Line "
                       f"contra {getattr(attacker, 'name', attacker)}")
        # TODO: velocidad 0 hasta el final del turno del atacante (dato
        # sin efecto: el sim no modela velocidad ni movimiento).
        r_ctx = copy.copy(ctx)
        r_ctx.is_reaction = True  # reentrada: el contraataque no dispara otro
        from .....engine.combat import attack_roll  # local: evita ciclo
        attack_roll(owner, attacker, arma, rng, log=log, ctx=r_ctx)
        return None


class CavalierMarkAttackAction(CombatAction):
    """Ataque especial de Unwavering Mark (acción bonus, A4).

    Solo es elegible si el flag vale en el turno actual (armado en el
    anterior), la criatura marcada sigue viva, la acción bonus está
    libre (``super().can_use``) y el dueño tiene un ataque cuerpo a
    cuerpo. Sin ``pick``: la elegibilidad no consume RNG (el ``pick``
    del encuentro decide entre las acciones candidatas de forma
    uniforme, patrón Tomar Aliento). Ejecuta un ataque cuerpo a cuerpo
    con ventaja forzada (``attacks_with_advantage``, se restaura al
    salir) y ``ctx.dano_reaccion`` = ``nivel // 2``, que solo suma si
    impacta. NO gasta un uso de marca (ya se gastó al marcar) ni la
    reacción (es acción bonus); sí marca ``is_reaction`` para que el
    ataque no reentre en maniobras. La velocidad 0 hasta el final del
    turno es dato sin efecto: el sim no modela velocidad ni movimiento.
    """

    def __init__(self) -> None:
        self.name = "Ataque de Marca"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # sin usos limitados: el límite es el bonus

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        trait = _de(actor, CavalierFeatures)
        if trait is None:
            return False
        if trait.ataque_marca_pendiente < trait.turno_cavalier:
            # Caducó (el turno propio ya pasó sin usarlo): se limpia.
            trait.ataque_marca_pendiente = 0
            trait.ataque_marca_objetivo = None
            return False
        if trait.ataque_marca_pendiente != trait.turno_cavalier:
            return False  # flag futuro: aún no es su turno válido
        marcado = trait.ataque_marca_objetivo
        if marcado is None or not getattr(marcado, "alive", True):
            return False
        if not _armas_melee_de(actor):
            return False
        return True

    def execute(self, context: Any) -> None:
        actor = context.actor
        trait = _de(actor, CavalierFeatures)
        rng = getattr(context, "rng", None)
        if trait is None or rng is None:
            return  # sin RNG el rasgo se abstiene
        marcado = trait.ataque_marca_objetivo
        if (trait.ataque_marca_pendiente != trait.turno_cavalier
                or marcado is None
                or not getattr(marcado, "alive", True)):
            return  # caducado o marcado muerto: sin RNG
        armas = _armas_melee_de(actor)
        if not armas:
            return
        arma = pick(rng, armas)  # sin RNG si solo hay una
        # Ataque único: el flag se consume aunque falle o falte el
        # objetivo tras la comprobación.
        trait.ataque_marca_pendiente = 0
        trait.ataque_marca_objetivo = None
        _log_line(context, f"{getattr(actor, 'name', actor)} realiza un "
                           f"Ataque de Marca contra "
                           f"{getattr(marcado, 'name', marcado)}")
        r_ctx = copy.copy(context)
        r_ctx.is_reaction = True  # reentrada: no activa maniobras
        # Daño extra nivel//2: daño_base_arma lo suma plano solo si
        # impacta (y lo pone a 0).
        r_ctx.dano_reaccion = cavalier_mark_extra_damage(trait.level)
        # Ventaja forzada: el indicador estático lo leen resolve_roll_mode
        # y attack_modifiers; se restaura para no colarla a otros ataques.
        antes = bool(getattr(actor, "attacks_with_advantage", False))
        actor.attacks_with_advantage = True
        try:
            from .....engine.combat import attack_roll  # local: evita ciclo
            attack_roll(actor, marcado, arma, rng,
                        log=getattr(context, "log", None), ctx=r_ctx)
        finally:
            actor.attacks_with_advantage = antes
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
    # Ataque especial de Unwavering Mark (acción bonus, elegibilidad
    # sin RNG: el pick del encuentro decide entre candidatas).
    pj.actions.append(CavalierMarkAttackAction())
    return trait


__all__ = ["CavalierFeatures", "CavalierMarkAttackAction", "apply_cavalier"]

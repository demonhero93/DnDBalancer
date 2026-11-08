"""Subclase Arcane Archer (Arquero Arcano, XGE) del Fighter.

Concentra en un único rasgo agregado (:class:`ArcaneArcherFeatures`)
las features de la subclase. :func:`apply_arcane_archer` monta el
personaje (exige que ``pj`` ya tenga :class:`FighterFeatures`).

Decisiones de simulación documentadas:

- **Arcane Archer Lore** (3): competencia en Arcanos o Naturaleza
  elegida con ``pick`` uniforme; el truco Prestidigitación/Druidismo se
  guarda como dato (sin utilidad en el sim).
- **Arcane Shot**: las opciones conocidas se eligen al crear el PJ con
  ``sample`` del pool :data:`ARCANE_SHOTS` (cuenta según el nivel);
  admite kwarg explícito ``arcane_shots`` validado (patrón
  ``fighting_style``). El pool tiene las 8 opciones: Piercing y Seeking
  entran (sus ataques sin tirada se resuelven en el punto de
  sustitución del motor, ver ``sustituir_ataque``).
- **Arcane Shot** (3): una vez por turno, la decisión es UN solo punto
  ANTES de la tirada de ataque: ``sustituir_ataque`` (paso 2b de
  ``attack_roll``) hace ``pick`` «no»/«sí» y después ``pick`` entre las
  opciones conocidas (sin usos, ya usado en el turno o ataque a cuerpo
  a cuerpo → cero RNG). Una opción de impacto (Banishing, Beguiling,
  Bursting, Enfeebling, Grasping, Shadow) se guarda en
  ``opcion_pendiente`` y se aplica SOLO si el ataque impacta (el uso se
  gasta al aplicar); Piercing y Seeking reemplazan la tirada: se
  ejecutan en la sustitución y el uso se gasta entonces. El daño extra
  de impacto se suma al del ataque (el motor no separa el tipo del
  bonus) y pasa de 2d6 a 4d6 desde el nivel 18. Decisiones de combate
  uniformes, sin IA.
- **Efectos de las opciones** (3): tras el daño, cada opción tira
  salvación con CD 8+PB+mod INT. Banishing (CAR) → Incapacitado 2
  rondas («hasta el final de tu siguiente turno» ≈ duración del
  afectado; la inatacabilidad no está modelada, TODO.md). Beguiling
  (aliado vivo con ``pick`` —sin posiciones: sin aliados solo daño y
  sin RNG—; SAB → Hechizado 2 rondas con fuente=aliado; el hechizo
  termina si el aliado ataca a la víctima, vía
  ``grant_attack_modifiers``). Enfeebling (CON) → marca en el estado
  del afectado que mitiga a la mitad el daño de sus ataques con arma
  (``CombatState.enfeeble_hasta_ronda``, consumida en ``attack.py``;
  los ataques mágicos quedan fuera). Shadow (SAB) → solo daño y
  salvación: la visión a 5 pies no depende de la distancia por ataque
  (TODO.md). Bursting (fuerza, sin salvación): el objetivo ya recibió
  el 2d6 base y todos los demás enemigos vivos del arquero —«a 10
  pies» abstracto, sin posiciones— reciben 2d6 de fuerza con una sola
  tirada compartida (patrón de área del sim: nunca aliados; sin RNG
  en la selección). Grasping sigue siendo solo daño
  (velocidad/moverse: sin sistema de movimiento).
- **Magic Arrow** (7): los arcos corto/largo del PJ (nombres EN/ES,
  normalización a minúsculas) se marcan ``magical=True`` in-place al
  crear el personaje (las acciones guardan el mismo objeto ``Attack``);
  solo desde el nivel 7.
- **Curving Shot** (7): al FALLAR un ataque a distancia con un arco
  mágico se guarda la marca (``curving_atk``/``curving_contra``); la
  acción bonus «Disparo Curvo» solo es elegible con bonus libre, marca
  presente y OTRO enemigo vivo («60 pies» abstracto: sin posiciones y
  sin RNG en la selección), con decisión ``pick`` «no»/«sí» (cero RNG
  si no es elegible); al ejecutar gasta la marca y vuelve a tirar con
  ``attack_roll`` contra el enemigo elegido.
- **Ever-Ready Shot** (10): sin efecto (cada combate empieza con usos
  completos); dato de tabla.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from .....core.classes import (
    MAX_LEVEL,
    MIN_LEVEL,
    arcane_shot_options_known,
    arcane_shot_uses,
)
from .....core.dice import roll_dice
from .....core.enums import AttackRange, parse_damage_type
from .....core.log import log_line as _log_line
from .....core.proficiency import proficiency_bonus
from .....core.randomness import pick, sample
from .....core.targeting import valid_targets
from .....model.actions import ActionType, CombatAction
from ....conditions import Condition, apply_condition
from ....damage import apply_damage_modifiers, inflict_damage
from ....saves import registrar_resistencia, saving_throw
from ....traits.base import AtaqueSustituido, Trait
from ....usage import ActionUsage, UsageKind
from ..features import FighterFeatures, _contexto

#: Pool de opciones de Arcane Shot implementadas (XGE): las 8. Piercing
#: y Seeking se ejecutan en el punto de sustitución (sin tirada).
ARCANE_SHOTS: tuple[str, ...] = (
    "Banishing Arrow",
    "Beguiling Arrow",
    "Bursting Arrow",
    "Enfeebling Arrow",
    "Grasping Arrow",
    "Shadow Arrow",
    "Piercing Arrow",
    "Seeking Arrow",
)

#: Opciones que REEMPLAZAN la tirada de ataque (sin d20): se ejecutan en
#: ``sustituir_ataque`` en lugar de guardarse como ``opcion_pendiente``.
ARCANE_SHOTS_SIN_TIRADA: tuple[str, ...] = (
    "Piercing Arrow",
    "Seeking Arrow",
)

#: Competencias que da Arcane Archer Lore (XGE: Arcanos o Naturaleza).
ARCANE_ARCHER_SKILLS: tuple[str, ...] = ("arcana", "nature")

#: Trucos de Arcane Archer Lore (dato sin efecto en el sim).
ARCANE_ARCHER_CANTRIPS: tuple[str, ...] = ("Prestidigitación", "Druidismo")

#: Nombres de arco que Magic Arrow vuelve mágicos (EN y ES, en
#: minúsculas; misma normalización que ``rules/mastery.py``).
_ARCOS: frozenset[str] = frozenset(
    {"arco corto", "arco largo", "shortbow", "longbow"})

#: RNG con semilla fija para Lore y opciones cuando no pasa ``rng``:
#: crea el personaje siempre igual (reproducible).
_RNG_CREACION = random.Random(0)


def _de(actor: Any, clase: type) -> Any:
    """Primer rasgo de ``actor`` que sea instancia de ``clase`` (o None)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


@dataclass
class ArcaneArcherFeatures(Trait):
    """Features de la subclase y estado de Arcane Shot."""

    # Nivel del personaje (manda en las tablas de la subclase).
    level: int = MIN_LEVEL
    #: Competencia ganada con Lore ("arcana" o "nature").
    competencia: str = ""
    #: Truco aprendido con Lore (dato sin efecto).
    truco: str = ""
    #: Opciones de Arcane Shot conocidas (nombres de :data:`ARCANE_SHOTS`).
    opciones_conocidas: list[str] = field(
        default_factory=list, repr=False, compare=False)
    #: Usos de Arcane Shot por descanso (patrón Second Wind).
    arcane_shot_usage: ActionUsage | None = None
    #: ¿Ya se aplicó Arcane Shot en el turno actual? (una vez por turno).
    shot_used_this_turn: bool = False
    #: Opción de impacto decidida ANTES de la tirada y aún no aplicada:
    #: solo se gasta el uso si el ataque llega a impactar. Se limpia al
    #: empezar el turno (decisión caducada).
    opcion_pendiente: str | None = field(
        default=None, repr=False, compare=False)
    #: Beguiling Arrow: nombre de la víctima → aliado hechizador. La
    #: borra el propio rasgo cuando el aliado ataca a la víctima.
    beguiling: dict[str, Any] = field(
        default_factory=dict, repr=False, compare=False)
    #: Curving Shot: ataque mágico fallado pendiente de re-tirar y
    #: nombre del objetivo que lo falló (para elegir a OTRO enemigo).
    curving_atk: Any = field(default=None, repr=False, compare=False)
    curving_contra: str | None = field(
        default=None, repr=False, compare=False)
    #: Dueño (para que ``reset`` pueda apagar los flags en el combatiente).
    owner: Any = field(default=None, repr=False, compare=False)

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        # «Una vez por turno»: el límite se reinicia al empezar el turno.
        self.shot_used_this_turn = False
        # Una pendiente sin impactar no viaja al turno siguiente.
        self.opcion_pendiente = None

    def reset(self) -> None:
        """Un combate nuevo = un día descansado: usos de Arcane Shot llenos."""
        self.shot_used_this_turn = False
        self.opcion_pendiente = None
        self.beguiling.clear()
        self.curving_atk = None
        self.curving_contra = None
        if self.arcane_shot_usage is not None:
            self.arcane_shot_usage.reset()

    # --- Arcane Shot (3) ------------------------------------------------------
    def sustituir_ataque(self, attacker: Any, target: Any, atk: Any,
                         rango: Any, *, ctx: Any = None,
                         rng: Any = None) -> Any:
        """Punto ÚNICO de decisión de Arcane Shot, antes de la tirada.

        Lo llama el motor en el paso 2b de ``attack_roll`` (duck-typing).
        Guards primero (sin usos, ya usado en el turno, pendiente sin
        resolver, sin rng o ataque a cuerpo a cuerpo → ``None`` SIN RNG).
        Con elegibles: ``pick`` «no»/«sí» y ``pick`` uniforme entre las
        opciones conocidas. Piercing/Seeking (solo con enemigos vivos en
        el pool) se ejecutan aquí y devuelven ``AtaqueSustituido``; las
        opciones de impacto se guardan en ``opcion_pendiente`` y el uso
        se gasta SOLO al impactar (``extra_attack_damage``).
        """
        if (attacker is not self.owner
                or target is None
                or rango is not AttackRange.RANGED
                or self.arcane_shot_usage is None
                or not self.arcane_shot_usage.available
                or self.shot_used_this_turn
                or self.opcion_pendiente is not None
                or rng is None):
            return None
        elegibles = valid_targets(self.owner, ctx)
        pool = tuple(
            o for o in self.opciones_conocidas
            if o not in ARCANE_SHOTS_SIN_TIRADA or elegibles
        )
        if not pool:
            return None  # sin elegibles: cero RNG
        if pick(rng, ("no", "si")) == "no":
            return None
        opcion = pick(rng, pool)
        if opcion in ARCANE_SHOTS_SIN_TIRADA:
            # Reemplaza la tirada: el uso se gasta AHORA (sin d20 ni
            # after_attack_roll). Daño y salvación: _ejecutar_* (A4/A5).
            self.arcane_shot_usage.spend()
            self.shot_used_this_turn = True
            return AtaqueSustituido(motivo=opcion)
        self.opcion_pendiente = opcion
        return None

    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            *, crit: bool = False, ctx: Any = None,
                            rng: Any = None,
                            atk: Any = None) -> int:
        """Aplica la opción de impacto pendiente al impactar a distancia.

        La decisión ya se tomó en ``sustituir_ataque``; aquí solo se
        aplica si hay pendiente. Sin pendiente, sin usos, ya usado en el
        turno, sin rng o ataque a cuerpo a cuerpo → 0 SIN RNG. El daño
        extra se suma al del ataque.
        """
        if (attacker is not self.owner
                or target is None
                or rango is not AttackRange.RANGED
                or self.opcion_pendiente is None
                or self.arcane_shot_usage is None
                or not self.arcane_shot_usage.available
                or self.shot_used_this_turn
                or rng is None):
            return 0
        opcion = self.opcion_pendiente
        self.opcion_pendiente = None
        self.arcane_shot_usage.spend()
        self.shot_used_this_turn = True
        dados = "4d6" if self.level >= 18 else "2d6"
        daño = int(roll_dice(dados, rng))
        _log_line(ctx, f"Arcane Shot ({opcion}): +{daño} de daño")
        self._efecto_de_opcion(opcion, target, ctx, rng)
        return daño

    def _cd(self) -> int:
        """CD de las salvaciones de Arcane Shot: 8 + PB + mod INT."""
        owner = self.owner
        mod_int = owner.abilities.mod("int") if owner is not None else 0
        return 8 + proficiency_bonus(self.level) + int(mod_int)

    def _aliado_para_beguiling(self, ctx: Any, rng: Any) -> Any:
        """Aliado vivo del dueño para Beguiling (o None, sin RNG).

        Sin posiciones: vale cualquier aliado vivo del contexto. Sin
        aliados no hay efecto posible y no se consume azar.
        """
        combatientes = getattr(ctx, "combatants", None) or []
        hostil = getattr(self.owner, "is_hostile_to", None)
        aliados = [
            c for c in combatientes
            if c is not self.owner
            and getattr(c, "alive", True)
            and (hostil is None or not hostil(c))
        ]
        if not aliados:
            return None
        return pick(rng, aliados)

    def _efecto_de_opcion(self, opcion: str, target: Any, ctx: Any,
                          rng: Any) -> None:
        """Salvación y condición de la opción elegida (tras el daño).

        Cada rama tira con la CD del rasgo; si la salvación se pasa no
        hay condición. Grasping es solo daño (velocidad y moverse: sin
        sistema de movimiento).
        """
        if opcion == "Banishing Arrow":
            sr = saving_throw(target, "cha", self._cd(), rng)
            registrar_resistencia(ctx, target, sr)
            if not sr.success:
                # «Hasta el final de tu siguiente turno» ≈ 2 rondas del
                # afectado (la duración tickea al fin de SU turno); la
                # inatacabilidad del objetivo no está modelada (TODO.md).
                apply_condition(target, Condition.INCAPACITATED, ctx,
                                source=self.owner, duration_rounds=2)
        elif opcion == "Beguiling Arrow":
            aliado = self._aliado_para_beguiling(ctx, rng)
            if aliado is None:
                return  # sin aliados: solo daño, sin RNG extra
            sr = saving_throw(target, "wis", self._cd(), rng)
            registrar_resistencia(ctx, target, sr)
            if not sr.success:
                instancia = apply_condition(
                    target, Condition.CHARMED, ctx, source=aliado,
                    duration_rounds=2)
                if instancia is not None:
                    self.beguiling[getattr(target, "name", "")] = aliado
        elif opcion == "Enfeebling Arrow":
            sr = saving_throw(target, "con", self._cd(), rng)
            registrar_resistencia(ctx, target, sr)
            ronda = getattr(ctx, "round", None)
            estado = getattr(target, "state", None)
            if not sr.success and ronda is not None and estado is not None:
                # Mitad del daño de SUS armas hasta el inicio del
                # siguiente turno del arquero ≈ ronda+1 (attack.py).
                estado.enfeeble_hasta_ronda[self.owner.name] = ronda + 1
        elif opcion == "Shadow Arrow":
            sr = saving_throw(target, "wis", self._cd(), rng)
            registrar_resistencia(ctx, target, sr)
            if not sr.success:
                # Solo daño + salvación: la visión a 5 pies no depende
                # de la distancia por ataque (TODO.md).
                _log_line(ctx, f"{getattr(target, 'name', target)} no ve "
                               f"a más de 5 pies (sin efecto de visión)")
        elif opcion == "Bursting Arrow":
            # «Cada criatura a 10 pies» sin posiciones: todos los
            # enemigos vivos del arquero salvo el objetivo (patrón de
            # área del sim: nunca aliados). Sin RNG en la selección y
            # una sola tirada de 2d6 compartida por los vecinos.
            vecinos = [c for c in valid_targets(self.owner, ctx)
                       if c is not target and getattr(c, "alive", True)]
            if not vecinos:
                return
            dado = int(roll_dice("2d6", rng))
            fuerza = parse_damage_type("force")
            for vecino in vecinos:
                dano = apply_damage_modifiers(dado, fuerza, vecino,
                                              magical=True)
                inflict_damage(vecino, dano, fuerza, source=self.owner,
                               ctx=ctx, rng=rng, magical=True)
            _log_line(ctx, f"Bursting Arrow: {len(vecinos)} criatura(s) "
                           f"a 10 pies reciben {dado} de daño de fuerza")
        # Grasping Arrow: solo daño (velocidad/moverse: sin movimiento).

    def grant_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                               rango: Any, ctx: Any = None,
                               rng: Any = None, atk: Any = None) -> None:
        """Beguiling: el hechizo termina si el aliado fuente ataca.

        El hook se despacha en cada tirada; sin marcas no hace nada
        (cero coste). También se borra la marca si la condición ya
        caducó por tiempo.
        """
        if not self.beguiling or target is None:
            return None
        nombre = getattr(target, "name", None)
        aliado = self.beguiling.get(nombre)
        if aliado is None or attacker is not aliado:
            return None
        tracker = getattr(target, "conditions", None)
        if tracker is not None:
            for instancia in list(tracker.instances):
                if (instancia.condition is Condition.CHARMED
                        and instancia.source is aliado):
                    tracker.remove_instance(instancia)
                    _log_line(
                        ctx,
                        f"El hechizo de {getattr(aliado, 'name', aliado)} "
                        f"sobre {nombre} termina (el aliado ataca)")
                    break
        self.beguiling.pop(nombre, None)
        return None

    # --- Curving Shot (7) -----------------------------------------------------
    def after_attack_roll(self, attacker: Any, target: Any, atk: Any,
                          hit: bool, ctx: Any = None,
                          rng: Any = None) -> None:
        """Marca el fallo con un arco mágico para poder re-tirar."""
        if self.level < 7 or hit or attacker is not self.owner:
            return None
        if getattr(atk, "range_type", None) is not AttackRange.RANGED:
            return None
        if not getattr(atk, "magical", False):
            return None  # solo con Magic Arrow (arcos marcados al crear)
        nombre = getattr(target, "name", None)
        if not nombre:
            return None
        self.curving_atk = atk
        self.curving_contra = nombre
        return None


def _otros_enemigos(actor: Any, ctx: Any, contra: str | None) -> list:
    """Enemigos vivos distintos de ``contra`` («60 pies» sin posiciones)."""
    return [c for c in valid_targets(actor, ctx)
            if getattr(c, "alive", True)
            and getattr(c, "name", None) != contra]


class CurvingShotAction(CombatAction):
    """Disparo Curvo (acción bonus, nivel 7+): re-tira tras un fallo.

    Solo es elegible con bonus libre, marca de fallo con arco mágico y
    OTRO enemigo vivo; la decisión de re-tirar es un ``pick`` «no»/«sí»
    (cero RNG si no es elegible). Al ejecutar gasta la marca y vuelve a
    tirar con ``attack_roll`` (el re-tiro es un ataque normal: puede
    aplicar Arcane Shot si aún no se usó en el turno).
    """

    def __init__(self) -> None:
        self.name = "Disparo Curvo"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None  # sin usos limitados: el límite es el bonus

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        trait = _de(actor, ArcaneArcherFeatures)
        if trait is None or trait.curving_atk is None:
            return False
        if not _otros_enemigos(actor, ctx, trait.curving_contra):
            return False  # sin otro objetivo: cero RNG
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return False  # sin RNG el rasgo se abstiene
        if pick(rng, ("no", "si")) == "no":
            return False  # decisión aleatoria de re-tirar
        return True

    def execute(self, context: Any) -> None:
        actor = context.actor
        trait = _de(actor, ArcaneArcherFeatures)
        rng = getattr(context, "rng", None)
        if trait is None or trait.curving_atk is None or rng is None:
            return
        otros = _otros_enemigos(actor, context, trait.curving_contra)
        if not otros:
            return
        atk = trait.curving_atk
        objetivo = pick(rng, otros)
        trait.curving_atk = None
        trait.curving_contra = None
        from .....engine.combat import attack_roll  # local: evita ciclo
        log = getattr(context, "log", None)
        attack_roll(actor, objetivo, atk, rng, log, ctx=context)


def apply_arcane_archer(pj: Any, level: int | None = None,
                        arcane_shots: tuple[str, ...] | None = None,
                        rng: Any = None) -> ArcaneArcherFeatures:
    """Aplica la subclase Arcane Archer a un PJ Guerrero.

    Exige que ``pj`` ya tenga :class:`FighterFeatures`
    (:func:`apply_fighter`). Añade el trait con Arcane Archer Lore
    (competencia y truco) y las opciones de Arcane Shot conocidas según
    el nivel (o las explícitas del kwarg ``arcane_shots``).
    """
    if _de(pj, FighterFeatures) is None:
        raise ValueError(
            "Primero aplica la clase guerrero con apply_fighter(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    generador = rng if rng is not None else _RNG_CREACION

    # Arcane Archer Lore (3): competencia y truco con pick uniforme.
    competencia = pick(generador, ARCANE_ARCHER_SKILLS)
    truco = pick(generador, ARCANE_ARCHER_CANTRIPS)
    pj.skill_proficiencies = set(pj.skill_proficiencies or set()) | {competencia}

    # Arcane Shot: N opciones conocidas (sample) o las explícitas.
    n = arcane_shot_options_known(lvl)
    if arcane_shots is None:
        opciones = list(sample(generador, ARCANE_SHOTS, n))
    else:
        opciones = list(arcane_shots)
        invalidas = [s for s in opciones if s not in ARCANE_SHOTS]
        if invalidas:
            raise ValueError(
                f"{invalidas!r} no es una opción de Arcane Shot: "
                f"opciones {sorted(ARCANE_SHOTS)}."
            )
        if len(opciones) != n:
            raise ValueError(
                f"se esperaban {n} opciones de Arcane Shot para el nivel "
                f"{lvl} y llegaron {len(opciones)}."
            )

    trait = ArcaneArcherFeatures(
        name="Arcane Archer",
        level=lvl,
        competencia=competencia,
        truco=truco,
        opciones_conocidas=opciones,
    )
    trait.owner = pj
    # Arcane Shot: usos por descanso (0 por debajo del nivel 3 → sin
    # gancho posible; patrón Second Wind).
    usos = arcane_shot_uses(lvl)
    trait.arcane_shot_usage = (
        ActionUsage(UsageKind.PER_DAY, uses_max=usos) if usos else None
    )
    pj.traits.append(trait)
    if lvl >= 7:
        # Magic Arrow (7): los arcos se vuelven mágicos. Mutación
        # in-place porque las acciones guardan el MISMO objeto Attack.
        for lista in (pj.attacks, pj.weapons):
            for atk in lista or []:
                if str(getattr(atk, "name", "")).strip().lower() in _ARCOS:
                    atk.magical = True
        # Curving Shot (7): acción bonus disponible desde el nivel 7.
        pj.actions.append(CurvingShotAction())
    return trait


__all__ = ["ARCANE_ARCHER_CANTRIPS", "ARCANE_ARCHER_SKILLS", "ARCANE_SHOTS",
           "ARCANE_SHOTS_SIN_TIRADA", "ArcaneArcherFeatures",
           "CurvingShotAction", "apply_arcane_archer"]

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
  ``fighting_style``). Piercing y Seeking quedan fuera del pool: sus
  ataques sin tirada reemplazarían el flujo de ataque del motor (ver
  TODO.md).
- **Arcane Shot** (3): una vez por turno, al impactar un ataque a
  distancia, ``pick`` «no»/«sí» y después ``pick`` entre las opciones
  conocidas; se gasta un uso solo al aplicar (sin usos, ya usado en el
  turno o ataque a cuerpo a cuerpo → cero RNG). El daño extra se suma
  al del ataque (el motor no separa el tipo del bonus) y pasa de 2d6 a
  4d6 desde el nivel 18. Decisiones de combate uniformes, sin IA.
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
from ....conditions import Condition, apply_condition
from ....damage import apply_damage_modifiers, inflict_damage
from ....saves import registrar_resistencia, saving_throw
from ....traits.base import Trait
from ....usage import ActionUsage, UsageKind
from ..features import FighterFeatures

#: Pool de opciones de Arcane Shot implementadas (XGE). Piercing y
#: Seeking no están: reemplazan la tirada de ataque (ver TODO.md).
ARCANE_SHOTS: tuple[str, ...] = (
    "Banishing Arrow",
    "Beguiling Arrow",
    "Bursting Arrow",
    "Enfeebling Arrow",
    "Grasping Arrow",
    "Shadow Arrow",
)

#: Competencias que da Arcane Archer Lore (XGE: Arcanos o Naturaleza).
ARCANE_ARCHER_SKILLS: tuple[str, ...] = ("arcana", "nature")

#: Trucos de Arcane Archer Lore (dato sin efecto en el sim).
ARCANE_ARCHER_CANTRIPS: tuple[str, ...] = ("Prestidigitación", "Druidismo")

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
    #: Beguiling Arrow: nombre de la víctima → aliado hechizador. La
    #: borra el propio rasgo cuando el aliado ataca a la víctima.
    beguiling: dict[str, Any] = field(
        default_factory=dict, repr=False, compare=False)
    #: Dueño (para que ``reset`` pueda apagar los flags en el combatiente).
    owner: Any = field(default=None, repr=False, compare=False)

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        # «Una vez por turno»: el límite se reinicia al empezar el turno.
        self.shot_used_this_turn = False

    def reset(self) -> None:
        """Un combate nuevo = un día descansado: usos de Arcane Shot llenos."""
        self.shot_used_this_turn = False
        self.beguiling.clear()
        if self.arcane_shot_usage is not None:
            self.arcane_shot_usage.reset()

    # --- Arcane Shot (3) ------------------------------------------------------
    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            *, crit: bool = False, ctx: Any = None,
                            rng: Any = None,
                            atk: Any = None) -> int:
        """Aplica una opción de Arcane Shot al impactar a distancia.

        Una vez por turno y con usos disponibles; sin usos, sin rng o
        con ataque a cuerpo a cuerpo → cero RNG y sin efecto. La
        decisión y la opción son ``pick`` uniforme; el daño extra se
        suma al del ataque.
        """
        if (attacker is not self.owner
                or target is None
                or rango is not AttackRange.RANGED
                or self.arcane_shot_usage is None
                or not self.arcane_shot_usage.available
                or self.shot_used_this_turn
                or rng is None):
            return 0
        if pick(rng, ("no", "si")) == "no":
            return 0
        opcion = pick(rng, tuple(self.opciones_conocidas))
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
    return trait


__all__ = ["ARCANE_ARCHER_CANTRIPS", "ARCANE_ARCHER_SKILLS", "ARCANE_SHOTS",
           "ArcaneArcherFeatures", "apply_arcane_archer"]

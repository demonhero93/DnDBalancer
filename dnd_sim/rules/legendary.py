"""Acciones legendarias y resistencia legendaria (D&D 5e).

Reglas implementadas:

- **Puntos legendarios**: cada monstruo legítimo tiene un número de puntos
  (3 por ronda en la SRD 2014, +1 en guarida). Se asume **siempre** la
  guarida del monstruo, así que el tope efectivo es 4 (MM 2024: 3, o 4 en
  guarida). Se rellenan al **inicio del turno de su dueño** hasta el
  máximo; los que no se usan se pierden (no se acumulan). Además, en una
  misma ronda no se pueden gastar más de ``points_max`` puntos.
- **Fase legendaria**: tras el turno de **cada** combatiente (también si el
  turno se perdió por incapacitación), todos los demás monstruos legítimos
  pueden usar **una** acción legendaria. Máximo una acción legendaria por
  dueño y por disparo.
- **Resistencia legendaria**: si el monstruo falla una salvación, puede
  convertir el fallo en éxito (3 usos por combate en la SRD 2014).
- **Fase de guarida**: en la iniciativa 20 (empates perdidos), cada dueño
  con ``data/lairs/<index>.json`` válido usa **una** acción de guarida por
  ronda sin repetir la de la ronda anterior. Sin fichero: ni fase, ni
  aviso, ni RNG.

Qué **no** se modela (fuera de alcance, con ``# TODO``):

- Efectos regionales (ignorados por diseño).
- Resistencia mágica (ventaja contra hechizos): solo "Legendary Resistance".
- Hechizos y conjuros, movimiento, detección, curación y utilidades.
- Puntos legendarios por ronda distintos de 3 (la API no los da); el CLI
  ``--legendary-points`` fija el valor final por encuentro.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..core.randomness import pick
from ..core.targeting import combat_finished, valid_targets

# Número de puntos legendarios por ronda (3 en la SRD 2014 / MM 2024).
# La API no da el número por monstruo (solo trae la lista de acciones),
# así que es lore estándar: excepciones conocidas se anotan en
# LEGENDARY_POINTS_OVERRIDES (valor base, sin el bonus de guarida) y el
# CLI --legendary-points fija el valor final por encuentro entero.
DEFAULT_LEGENDARY_POINTS = 3

#: Puntos legendarios extra por ronda. MM 2024: 3, o 4 en guarida;
#: asumimos siempre guarida, así que ``points_max = base +
#: LEGENDARY_LAIR_BONUS`` para todo monstruo legendario. El CLI
#: ``--legendary-points`` fija el valor final sin sumar este bonus.
LEGENDARY_LAIR_BONUS = 1

#: Excepciones por monstruo: índice del monstruo -> puntos por ronda.
#: La API no da el valor y hoy no se conoce ninguna ficha de la SRD que se
#: aparte de 3, así que la tabla está vacía. No contiene estadísticas de
#: monstruos: solo un entero de puntos por ronda (excepción permitida,
#: al estilo de spell_rules).
LEGENDARY_POINTS_OVERRIDES: dict[str, int] = {}


@dataclass
class LegendaryAction:
    """Una acción legendaria del monstruo.

    ``action`` es la acción real envuelta (se **reutiliza**, no se copia):
    un ``AttackAction``, un ``SaveAction``, un ``AreaSaveAction`` o un
    ``ConditionAction``.
    """

    name: str
    cost: int = 1
    action: Any = None


@dataclass
class LairAction:
    """Una acción de guarida del monstruo.

    Los datos viven en el repo (``data/lairs/<index>.json``; la API no
    trae guaridas) y los construye :mod:`dnd_sim.data.lair_loader` con
    los mismos constructores que el resto del motor. ``action`` es la
    acción real envuelta (un ``AttackAction``, un ``SaveAction``, un
    ``AreaSaveAction`` o un ``ConditionAction``).
    """

    name: str
    action: Any = None


@dataclass
class LegendaryState:
    """Estado legendario de un monstruo (puntos y resistencia legendaria)."""

    actions: list[LegendaryAction] = field(default_factory=list)
    points_max: int = DEFAULT_LEGENDARY_POINTS
    points_left: int = DEFAULT_LEGENDARY_POINTS
    # Contabilidad por ronda: los puntos legendarios son 3 **por ronda**.
    # ``round_id`` es la ronda de la última contabilidad y ``round_spent`` los
    # puntos ya gastados en ella.
    round_id: int = 0
    round_spent: int = 0
    resistance_max: int = 0
    resistance_left: int = 0
    # Probabilidad de usar una acción legendaria en cada disparo.
    use_probability: float = 1.0
    # Probabilidad de gastar la resistencia legendaria cuando toca.
    resistance_probability: float = 1.0
    # Acciones de guarida (vacío = el monstruo no tiene; la fase corre
    # siempre que haya fichero en data/lairs/). Las criaturas no legendarias
    # con guarida quedan sin modelar (# TODO).
    lair_actions: list[LairAction] = field(default_factory=list)
    # Nombre de la última acción de guarida usada y la ronda en la que se
    # usó: al empezar una ronda nueva se olvida, así una sola acción se usa
    # en rondas alternas y ninguna se repite en dos rondas consecutivas.
    last_lair_used: str | None = None
    lair_round: int | None = None

    def refill_points(self, round: int | None = None) -> None:
        """Rellena los puntos hasta el máximo (los no usados se pierden).

        ``round`` es la ronda en la que se rellenan (informativo): la
        contabilidad por ronda la lleva la fase legendaria. El tope
        ``points_max`` ya incluye ``LEGENDARY_LAIR_BONUS`` (siempre en
        guarida).
        """
        self.points_left = int(self.points_max)

    def spend_points(self, n: int) -> None:
        """Gasta ``n`` puntos (nunca por debajo de cero)."""
        self.points_left = max(0, int(self.points_left) - int(n))

    def reset(self) -> None:
        """Reinicia el estado (nuevo combate): puntos y resistencia."""
        self.points_left = int(self.points_max)
        self.round_id = 0
        self.round_spent = 0
        self.resistance_left = int(self.resistance_max)
        self.last_lair_used = None
        self.lair_round = None


# --- Fase legendaria -------------------------------------------------------- #


from ..core.log import log_line as _log_line


def _contexto_de(owner: Any, ctx: Any) -> Any:
    """Contexto de combate para el dueño de la acción legendaria.

    Se copia el contexto del combatiente que acaba su turno, pero **sin**
    recursos de turno (``resources=None``): la acción legendaria no gasta ni
    la acción, ni la acción adicional, ni la reacción del dueño.
    """
    from ..model.actions import CombatContext
    try:
        return CombatContext(
            rng=ctx.rng,
            actor=owner,
            combatants=list(getattr(ctx, "combatants", None) or []),
            round=int(getattr(ctx, "round", 0) or 0),
            log=getattr(ctx, "log", None),
            verbose=bool(getattr(ctx, "verbose", False)),
            resources=None,
            available_actions=[],
            action_uses=getattr(ctx, "action_uses", None),
            area_targets_hit=getattr(ctx, "area_targets_hit", None),
            conditions_applied=getattr(ctx, "conditions_applied", None),
            escape_attempts=getattr(ctx, "escape_attempts", None),
            escape_successes=getattr(ctx, "escape_successes", None),
            attacks_at_range=getattr(ctx, "attacks_at_range", None),
            legendary_stats=getattr(ctx, "legendary_stats", None),
            skip_turn=False,
        )
    except Exception:
        return ctx


def _accion_utilizable(accion: Any, owner: Any, ctx: Any) -> bool:
    """¿Se puede usar la acción legendaria ahora mismo?

    - La acción debe poder usarse (uso limitado disponible) **sin** que
      importen los recursos de turno del dueño.
    - Debe haber al menos un objetivo hostil vivo.
    """
    if accion is None:
        return False
    try:
        if not accion.can_use(ctx):
            return False
    except Exception:
        return False
    try:
        return bool(valid_targets(owner, ctx=ctx))
    except Exception:
        return False


def _presupuesto(legendary: LegendaryState) -> int:
    """Puntos que el dueño puede gastar ahora mismo (pool y tope por ronda)."""
    pool = int(getattr(legendary, "points_left", 0) or 0)
    maximo = int(getattr(legendary, "points_max", 0) or 0)
    gastados = int(getattr(legendary, "round_spent", 0) or 0)
    return max(0, min(pool, maximo - gastados))


def _acciones_asequibles(legendary: LegendaryState, owner: Any, ctx: Any,
                          presupuesto: int | None = None) -> list[LegendaryAction]:
    """Acciones legendarias que el dueño puede permitirse ahora mismo."""
    if presupuesto is None:
        presupuesto = _presupuesto(legendary)
    return [
        la for la in (getattr(legendary, "actions", None) or [])
        if int(getattr(la, "cost", 1) or 0) <= presupuesto
        and _accion_utilizable(getattr(la, "action", None), owner, ctx)
    ]


def legendary_phase(finished_actor: Any, ctx: Any) -> None:
    """Fase legendaria: se dispara tras el turno de ``finished_actor``.

    Para cada monstruo con estado legendario (en orden de iniciativa),
    distinto del combatiente que acaba su turno:

    1. Debe estar vivo y poder actuar (``can_act``).
    2. Se eligen las acciones **asequibles** (coste <= puntos restantes y con
       objetivos válidos). Si no hay ninguna, no se hace nada **y no se
       consume RNG**.
    3. Si ``use_probability < 1`` se tira una vez para decidir si actúa.
    4. Se elige una acción con ``pick`` (sin RNG si solo hay una).
    5. Se gastan los puntos y se resuelve la acción **sin** gastar los
       recursos de turno ni el uso limitado del dueño.

    Tras cada acción se comprueba si el combate ha terminado: si ha
    terminado, no se ejecutan más acciones ni más dueños.

    Orden del RNG: probabilidad (si ``p < 1``) -> elección de acción -> lo
    que consuma la acción.
    """
    rng = getattr(ctx, "rng", None)
    combatants = list(getattr(ctx, "combatants", None) or [])
    if rng is None or not combatants:
        return

    for owner in combatants:
        if owner is finished_actor:
            continue
        legendary = getattr(owner, "legendary", None)
        if legendary is None:
            continue
        if not getattr(owner, "alive", False):
            continue
        if not getattr(owner, "can_act", True):
            continue
        if combat_finished(combatants):
            return

        # El dueno tiene 3 acciones legendarias **por ronda**: aunque sus
        # puntos se rellenen al inicio de su propio turno, en una ronda no
        # puede gastar más de ``points_max``.
        ronda = int(getattr(ctx, "round", 0) or 0)
        if int(getattr(legendary, "round_id", 0) or 0) != ronda:
            legendary.round_id = ronda
            legendary.round_spent = 0
        presupuesto = _presupuesto(legendary)

        owner_ctx = _contexto_de(owner, ctx)
        affordable = _acciones_asequibles(legendary, owner, owner_ctx,
                                          presupuesto=presupuesto)
        if not affordable:
            continue

        # (3) Probabilidad de actuar (no consume RNG si es 1.0).
        probabilidad = float(getattr(legendary, "use_probability", 1.0) or 0.0)
        if probabilidad < 1.0 and rng.random() >= probabilidad:
            continue

        # (4) Elección de la acción (sin RNG si solo hay una).
        chosen = pick(rng, affordable)

        # (5) Gasto de puntos y resolución (sin recursos de turno ni uso).
        coste = int(getattr(chosen, "cost", 1) or 0)
        legendary.spend_points(coste)
        legendary.round_spent = int(getattr(legendary, "round_spent", 0) or 0) + coste
        _contar_puntos(ctx, coste)
        _log_line(
            ctx,
            f"[Legendaria] {getattr(owner, 'name', owner)} usa {chosen.name} "
            f"(coste {chosen.cost}, quedan {legendary.points_left}) "
            f"tras el turno de {getattr(finished_actor, 'name', finished_actor)}",
        )
        _contar_accion(ctx, chosen.name)
        accion = getattr(chosen, "action", None)
        if accion is not None:
            accion.execute(owner_ctx)

        if combat_finished(combatants):
            return


def lair_phase(ctx: Any) -> None:
    """Fase de guarida (siempre activa; la criatura asume su guarida).

    En la iniciativa 20 (con empates perdidos la sitúa el bucle de turnos),
    cada dueño de acciones de guarida vivo y capaz de actuar usa **una**
    acción por ronda:

    1. Se eligen las acciones que no se usaron en la ronda anterior. Si no
       queda ninguna, el dueño no actúa ese turno (una sola acción → se usa
       en rondas alternas). Si solo hay una opción no se consume RNG (misma
       regla que las legendarias).
    2. La acción se resuelve **sin** gastar recursos de turno, uso limitado
       ni puntos legendarios.
    3. Tras cada acción se comprueba el fin del combate: si ha terminado,
       no se ejecutan más acciones ni más dueños.

    Sin dueños con ``lair_actions`` (sin fichero en ``data/lairs/``) o sin
    combate vivo no se consume RNG.
    """
    rng = getattr(ctx, "rng", None)
    combatants = list(getattr(ctx, "combatants", None) or [])
    if rng is None or not combatants:
        return
    if combat_finished(combatants):
        return

    for owner in combatants:
        legendary = getattr(owner, "legendary", None)
        if legendary is None or not getattr(legendary, "lair_actions", None):
            continue
        if not getattr(owner, "alive", False):
            continue
        if not getattr(owner, "can_act", True):
            continue
        if combat_finished(combatants):
            return

        # Una por ronda y sin repetir la de la ronda anterior:
        # ``last_lair_used`` es lo que se usó la ronda pasada (None si
        # nada). Así una sola acción se usa en rondas alternas y, con
        # varias, ninguna se repite en dos rondas consecutivas.
        ronda = getattr(ctx, "round", 0)
        if legendary.lair_round == ronda:
            # La fase de este dueño ya corrió en esta ronda.
            continue
        legendary.lair_round = ronda

        opciones = list(legendary.lair_actions)
        elegibles = [
            a for a in opciones
            if a.name != getattr(legendary, "last_lair_used", None)
        ]
        if not elegibles:
            # Sin opciones (una sola acción ya usada en la ronda anterior):
            # este dueño no actúa, no se consume RNG y la ronda cuenta
            # como «sin uso».
            legendary.last_lair_used = None
            continue
        chosen = pick(rng, elegibles) if len(elegibles) > 1 else elegibles[0]
        legendary.last_lair_used = chosen.name
        _log_line(
            ctx,
            f"[Guarida] {getattr(owner, 'name', owner)} usa {chosen.name}",
        )
        accion = getattr(chosen, "action", None)
        if accion is not None:
            accion.execute(_contexto_de(owner, ctx))

        if combat_finished(combatants):
            return


def _contar_accion(ctx: Any, nombre: str) -> None:
    """Suma una acción legendaria a las estadísticas del combate."""
    stats = getattr(ctx, "legendary_stats", None)
    if not isinstance(stats, dict):
        return
    acciones = stats.setdefault("actions", {})
    acciones[nombre] = acciones.get(nombre, 0) + 1


def _contar_puntos(ctx: Any, puntos: int) -> None:
    """Suma los puntos legendarios gastados a las estadísticas del combate."""
    stats = getattr(ctx, "legendary_stats", None)
    if not isinstance(stats, dict):
        return
    stats["points"] = int(stats.get("points", 0) or 0) + int(puntos)


# --- Resistencia legendaria ------------------------------------------------ #


def _contar_resistencia(ctx: Any) -> None:
    """Suma una resistencia legendaria a las estadísticas del combate."""
    stats = getattr(ctx, "legendary_stats", None)
    if not isinstance(stats, dict):
        return
    stats["resistances"] = int(stats.get("resistances", 0) or 0) + 1


def legendary_resistance(target: Any, result: Any, rng: Any) -> Any:
    """Convierte un fallo de salvación en éxito con la Resistencia legendaria.

    Solo actúa si la salvación **ha fallado** (incluido el fallo automático
    por condición) y al monstruo le quedan usos de resistencia. Con
    ``resistance_probability < 1`` se tira una vez para decidir; con 1.0 no
    se consume RNG.

    Devuelve el mismo ``SaveResult`` (mutado) para poder encadenarlo.
    """
    legendary = getattr(target, "legendary", None)
    if legendary is None:
        return result
    if getattr(result, "success", False):
        return result
    if int(getattr(legendary, "resistance_left", 0) or 0) <= 0:
        return result

    probabilidad = float(getattr(legendary, "resistance_probability", 1.0) or 0.0)
    if probabilidad < 1.0:
        if rng is None or rng.random() >= probabilidad:
            return result

    legendary.resistance_left = int(legendary.resistance_left) - 1
    try:
        result.success = True
        result.legendary_resistance_used = True
    except Exception:
        pass
    return result


def registrar_resistencia_legendaria(ctx: Any, target: Any, result: Any) -> Any:
    """Log y estadísticas si la Resistencia legendaria se ha gastado.

    Se llama justo después de cada :func:`dnd_sim.rules.saves.saving_throw` (el
    único sitio donde hay contexto de combate).
    """
    if not getattr(result, "legendary_resistance_used", False):
        return result
    legendary = getattr(target, "legendary", None)
    if legendary is None:
        return result
    habilidad = str(getattr(result, "ability", "") or "").upper()
    _log_line(
        ctx,
        f"{getattr(target, 'name', target)} gasta Resistencia legendaria "
        f"(quedan {legendary.resistance_left}): salvación {habilidad} "
        f"falla -> superada",
    )
    _contar_resistencia(ctx)
    return result


__all__ = [
    "DEFAULT_LEGENDARY_POINTS",
    "LegendaryAction",
    "LairAction",
    "LegendaryState",
    "lair_phase",
    "legendary_phase",
    "legendary_resistance",
    "registrar_resistencia_legendaria",
]

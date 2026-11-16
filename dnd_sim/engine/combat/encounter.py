"""Bucle del combate: iniciativa, política de objetivo,
turno a turno y resultado del encuentro."""

from __future__ import annotations

import inspect
import random
from dataclasses import dataclass, field

from ...model.actions import ActionType, CombatContext
from ...model.combatant import Combatant, valid_targets
from ...core.targeting import combat_finished, living_teams
from ...rules.conditions import end_turn
from ...rules.damage import DamageRecorder
from ...core.dice import RollMode, d20, roll_d20
from ...rules.legendary import lair_phase, legendary_phase
from ...core.randomness import pick
from ..tactics import random_policy
from ...rules.usage import begin_turn
from ...rules.utility import (DodgeAction, debe_usar_utilitaria,
                              hay_utilitaria_accion)


@dataclass
class CombatResult:
    winner: str
    rounds: int
    survivors: dict[str, int]  # nombre -> hp restante
    log: list[str]
    # Estadísticas: usos por nombre de acción y objetivos afectados por área.
    action_uses: dict[str, int] = field(default_factory=dict)
    area_targets_hit: list[int] = field(default_factory=list)
    # Daño del combate por combatiente (nombre -> daño total).
    damage_dealt: dict[str, int] = field(default_factory=dict)
    damage_received: dict[str, int] = field(default_factory=dict)
    # Condiciones: veces aplicada cada una y turnos perdidos por incapacitación.
    conditions_applied: dict[str, int] = field(default_factory=dict)
    turns_lost_incapacitated: dict[str, int] = field(default_factory=dict)
    # Escapes: intentos y éxitos por condición; ataques contra objetivos a distancia.
    escape_attempts: dict[str, int] = field(default_factory=dict)
    escape_successes: dict[str, int] = field(default_factory=dict)
    attacks_vs_at_range: int = 0
    # Leyenda: acciones legendarias usadas (nombre -> veces), puntos gastados
    # y resistencias legendarias gastadas.
    legendary_actions_used: dict[str, int] = field(default_factory=dict)
    legendary_points_spent: int = 0
    legendary_resistances_used: int = 0
    # Espacios de conjuro gastados por combatiente (nombre -> max - actual);
    # solo aparece quien lleve ``spell_slots`` (PJ lanzador).
    spell_slots_spent: dict[str, int] = field(default_factory=dict)


def _summarize_damage(records) -> tuple[dict[str, int], dict[str, int]]:
    """Reparte el daño registrado por combatiente (infligido y recibido)."""
    dealt: dict[str, int] = {}
    received: dict[str, int] = {}
    for record in records or []:
        amount = int(record.get("amount") or 0)
        source = record.get("source")
        target = record.get("target")
        source_name = getattr(source, "name", None)
        target_name = getattr(target, "name", None)
        if source_name:
            dealt[source_name] = dealt.get(source_name, 0) + amount
        if target_name:
            received[target_name] = received.get(target_name, 0) + amount
    return dealt, received


def roll_initiative(combatants: list[Combatant], rng: random.Random) -> list[Combatant]:
    for c in combatants:
        # Fuentes de ventaja/desventaja de la iniciativa: el flag
        # ``initiative_with_advantage`` (Feral Instinct) y el
        # duck-typing ``ventaja_iniciativa()``/``desventaja_iniciativa()``
        # (Remarkable Athlete, Champion) —sin imports de rules, cada
        # rasgo aplica sus guards y no consume RNG solo—; si hay de
        # ambos lados se anulan y se tira normal (regla estándar).
        ventaja = bool(getattr(c, "initiative_with_advantage", False))
        desventaja = False
        for rasgo in getattr(c, "traits", None) or []:
            fn = getattr(rasgo, "ventaja_iniciativa", None)
            if callable(fn) and fn():
                ventaja = True
            fn = getattr(rasgo, "desventaja_iniciativa", None)
            if callable(fn) and fn():
                desventaja = True
        if ventaja and not desventaja:
            # Fuera de estas ramas el RNG sigue su curso normal, así
            # que el orden de tiradas de los demás no cambia respecto
            # a un combate sin la feature.
            roll = roll_d20(rng, RollMode.ADVANTAGE).value
        elif desventaja and not ventaja:
            roll = roll_d20(rng, RollMode.DISADVANTAGE).value
        else:
            roll = d20(rng)
        # Ambush (Battle Master): consulta duck-typing (sin imports de
        # rules); el rasgo aplica sus guards —sin RNG si no procede— y
        # suma un dado de superioridad a la tirada.
        for rasgo in getattr(c, "traits", None) or []:
            bonus = getattr(rasgo, "bonus_iniciativa", None)
            if callable(bonus):
                roll += int(bonus(rng=rng) or 0)
        c.initiative = roll + c.abilities.mod("dex")
    return sorted(combatants, key=lambda c: (c.initiative, c.abilities.dex), reverse=True)


def _invoke_policy(policy, ctx: CombatContext, candidates: list):
    ctx.available_actions = list(candidates)
    # Soporta policy(ctx) y policy(choices, rng) y variantes posicionales.
    try:
        sig = inspect.signature(policy)
        params = list(sig.parameters.values())
    except (TypeError, ValueError):
        params = []
    n_required = sum(1 for p in params if p.default is inspect.Parameter.empty and p.kind in (
        inspect.Parameter.POSITIONAL_ONLY,
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
    ))
    # Preferimos la convención más común del motor: policy(ctx).
    if len(params) <= 1:
        return policy(ctx)
    # Si espera 2+ posicionales, intentamos pasar (candidates, rng).
    try:
        return policy(candidates, ctx.rng)
    except TypeError:
        try:
            return policy(ctx, candidates)
        except TypeError:
            return policy(ctx)


def _avisar_ganchos_de_turno(order: list[Combatant], actor: Combatant,
                             ctx: CombatContext, *, inicio: bool) -> None:
    """Avisa ``on_any_turn_start``/``on_any_turn_end`` a todos los vivos.

    El argumento es el combatiente que actúa (``actor``); lo reciben los
    rasgos de todos los combatientes vivos de ``order``, no solo los suyos.
    Import local de ``hooks`` al estilo del resto del motor: sin rasgos
    que sobrescriban el gancho la lista sale vacía y no se consume RNG.
    """
    metodo = "on_any_turn_start" if inicio else "on_any_turn_end"
    for criatura in order:
        if not getattr(criatura, "alive", True):
            continue
        traits = getattr(criatura, "traits", None)
        if not traits:
            continue
        from ...rules.traits import hooks
        for rasgo in hooks(traits, metodo):
            getattr(rasgo, metodo)(actor, ctx)


def run_combat(combatants: list[Combatant], rng: random.Random,
               verbose: bool = False, max_rounds: int = 100,
               policy=None) -> CombatResult:
    """Ejecuta un combate y devuelve el resultado con sus estadísticas.

    El daño infligido se registra durante el combate (:class:`DamageRecorder`)
    para poder informar del daño medio de cada combatiente.

    Se asume siempre la guarida del monstruo legendario: la fase de guarida
    corre en la iniciativa 20 si el dueño tiene ``data/lairs/<index>.json``
    (sin fichero no hay fase, ni aviso, ni RNG).
    """
    with DamageRecorder() as recorder:
        result = _run_combat(combatants, rng, verbose=verbose, max_rounds=max_rounds,
                             policy=policy)
    dealt, received = _summarize_damage(recorder.records)
    result.damage_dealt = dealt
    result.damage_received = received
    return result


def _run_combat(combatants: list[Combatant], rng: random.Random,
                verbose: bool = False, max_rounds: int = 100,
                policy=None) -> CombatResult:
    if policy is None:
        policy = random_policy
    for c in combatants:
        c.reset()
    order = roll_initiative(combatants, rng)

    log: list[str] = []
    rnd = 0
    # Estadísticas del combate (compartidas por todos los turnos).
    action_uses: dict[str, int] = {}
    area_targets_hit: list[int] = []
    conditions_applied: dict[str, int] = {}
    turns_lost_incapacitated: dict[str, int] = {}
    escape_attempts: dict[str, int] = {}
    escape_successes: dict[str, int] = {}
    attacks_at_range: list[int] = []
    # Estadísticas legendarias (acciones usadas, puntos y resistencias).
    legendary_stats: dict = {"actions": {}, "points": 0, "resistances": 0}

    def _nuevo_ctx(actor: Combatant) -> CombatContext:
        """Contexto de un turno o de la fase de guarida (mismo round)."""
        return CombatContext(
            rng=rng, actor=actor, combatants=order, round=rnd,
            log=log if verbose else None, verbose=verbose, resources=None,
            action_uses=action_uses, area_targets_hit=area_targets_hit,
            conditions_applied=conditions_applied,
            escape_attempts=escape_attempts,
            escape_successes=escape_successes,
            attacks_at_range=attacks_at_range,
            legendary_stats=legendary_stats,
        )

    def _turno(actor: Combatant) -> bool:
        """Ejecuta el turno completo de ``actor``.

        Es el cuerpo de antes, extraído del bucle de rondas en A5 para
        reutilizarlo (turno extra de Strength Before Death) con CERO
        cambio de orden, llamadas o RNG: inicio de turno y recargas,
        ganchos «cualquier turno», pasadas ACTION/BONUS/Oleada, cierre
        (salvaciones de repetición) y fase legendaria.

        Devuelve ``True`` si el bucle puede seguir con el siguiente
        combatiente y ``False`` si debe cortarse (combate terminado o
        sin objetivos vivos).
        """
        if not actor.alive:
            return True
        enemies = valid_targets(actor, combatants=order)
        if not enemies:
            return False
        ctx = _nuevo_ctx(actor)
        # Inicio de turno: recursos nuevos y tiradas de recarga de las
        # acciones descargadas del actor. Si está incapacitado, pierde
        # el turno (sin política y sin consumir RNG).
        resources = begin_turn(actor, ctx)
        # El actor puede morir en su propio inicio de turno (p. ej.
        # Regeneration sin curación posible): si eso deja a un bando
        # sin nadie en pie, el combate termina aquí mismo.
        if combat_finished(order):
            return False
        # Ganchos «cualquier turno» (p. ej. runas de Rune Knight): a
        # los rasgos de TODOS los vivos, con el actor como argumento.
        # Si nadie los sobrescribe, `hooks` no devuelve nada y no se
        # consume RNG.
        _avisar_ganchos_de_turno(order, actor, ctx, inicio=True)
        if not ctx.skip_turn:
            accion_ejecutada = False

            def _pasada(action_type: ActionType, *,
                        permitir_magia: bool = True) -> bool:
                """Ejecuta como mucho una acción de ``action_type``.

                Devuelve ``False`` si el turno debe parar (combate
                terminado o actor caído) y ``True`` si puede seguir.
                Con ``permitir_magia=False`` (pasada extra de Oleada) se
                excluyen las acciones de hechizo de PJ
                (``es_accion_magia``): la Oleada no puede lanzar
                conjuros (PHB).
                """
                nonlocal accion_ejecutada
                # Fin ya decidido (último de un bando caído): no se
                # lanza ninguna habilidad más, ni siquiera la bonus.
                if combat_finished(order):
                    return False
                # Un actor que ha caído en mitad de su turno (p. ej.
                # represalias) no lanza nada más.
                if not actor.alive:
                    return False
                candidates = [
                    a for a in getattr(actor, "actions", [])
                    if getattr(a, "action_type", None) == action_type
                    and (permitir_magia
                         or not getattr(a, "es_accion_magia", False))
                    and a.can_use(resources, ctx)
                    and getattr(actor, "can_act", True)
                ]
                if not candidates:
                    return True
                chosen = None
                # Utilitaria: Esquivar sustituye la ACTION si toca.
                # Disponibilidad primero (hay acción, vivo, puede actuar
                # y no esquiva ya), probabilidad después.
                if (action_type is ActionType.ACTION
                        and hay_utilitaria_accion(actor)
                        and debe_usar_utilitaria(rng)):
                    chosen = DodgeAction()
                if chosen is None:
                    chosen = _invoke_policy(policy, ctx, candidates)
                    if chosen is None:
                        chosen = pick(rng, candidates)
                chosen.execute(ctx)
                accion_ejecutada = True
                resources.use(action_type)
                # El uso limitado se gasta aquí (una vez, aunque el área
                # afecte a pocos objetivos).
                usage = getattr(chosen, "usage", None)
                if usage is not None:
                    usage.spend()
                action_name = getattr(chosen, "name", "") or type(chosen).__name__
                action_uses[action_name] = action_uses.get(action_name, 0) + 1
                enemies = valid_targets(actor, combatants=order)
                # Con este golpe puede haber caído el último enemigo
                # (o el último aliado, vía represalias): fin del combate.
                if not enemies or combat_finished(order):
                    return False
                return True

            # Ejecuta como mucho una ACTION y una BONUS_ACTION por turno.
            if _pasada(ActionType.ACTION) and _pasada(ActionType.BONUS_ACTION):
                # Oleada de Acción: la acción bonus restauró el recurso
                # de acción, así que toca UNA pasada de acción extra.
                # Sin Oleada la acción queda gastada y no se entra aquí
                # (cero cambio de comportamiento ni de RNG).
                if accion_ejecutada and not resources.action_used:
                    # Pasada extra de Oleada: SIN hechizos de PJ (PHB).
                    _pasada(ActionType.ACTION, permitir_magia=False)
        else:
            # Turno perdido. Solo cuenta como incapacitación si la
            # criatura sigue viva: quien muere al empezar su turno
            # (Regeneration) no «pierde» el turno, ya no está.
            if actor.alive:
                turns_lost_incapacitated[actor.name] = (
                    turns_lost_incapacitated.get(actor.name, 0) + 1)
        # El combate terminado no cierra turnos ni dispara la fase
        # legendaria: el bucle se corta en el momento en que cae el
        # último de un bando.
        if combat_finished(order):
            return False
        # Final del turno: salvaciones de repetición y duración de las
        # condiciones del propio combatiente.
        end_turn(actor, ctx)
        # Ganchos «cualquier turno» de fin: solo si el actor sigue
        # vivo (un muerto no «termina» su turno; el combate ya se
        # corta más arriba si se decidió aquí).
        if actor.alive:
            _avisar_ganchos_de_turno(order, actor, ctx, inicio=False)
        # Strength Before Death (A6): aquí se resuelven los turnos
        # extra pendientes (al final de CADA turno, decisión
        # documentada) antes de la fase legendaria.
        _procesar_turnos_extra()
        # Fase legendaria: los demás monstruos legítimos pueden usar una
        # acción legendaria tras el turno de este combatiente.
        legendary_phase(actor, ctx)
        if combat_finished(order):
            return False
        return True

    def _procesar_turnos_extra() -> None:
        """Strength Before Death (A6): resuelve los turnos extra.

        Se llama AL FINAL de cada turno (tras los ganchos de fin y
        antes de la fase legendaria) y procesa TODAS las entradas
        pendientes: el «procesar todo en cada fin de turno» evita
        bloqueos con reacciones y fase de guarida (decisión del
        mantainer, documentada). Cada entrada, una sola vez (se saca
        de la cola ANTES de actuar):

        - ya curado (PV > 0) o muerto: sale sin turno extra;
        - sigue a 0 PV: turno extra completo con ``_turno`` y, tras
          él, PV > 0 → se suelta el flag, 0 PV → muere.
        """
        for combatiente in order:
            cola = getattr(getattr(combatiente, "state", None),
                           "turnos_extra_pendientes", None)
            if not cola:
                continue
            while cola:
                pendiente = cola.pop(0)
                if not getattr(pendiente, "en_pie_pendiente", False):
                    continue  # ya resuelto (curado o rematado)
                if getattr(pendiente, "dead", False):
                    pendiente.en_pie_pendiente = False
                    continue
                if int(getattr(pendiente, "hp", 0) or 0) > 0:
                    # Curado mientras esperaba: sale sin turno extra.
                    pendiente.en_pie_pendiente = False
                    continue
                _turno(pendiente)
                if combat_finished(order):
                    return
                if int(getattr(pendiente, "hp", 0) or 0) > 0:
                    pendiente.en_pie_pendiente = False
                elif not getattr(pendiente, "dead", False):
                    pendiente.en_pie_pendiente = False
                    marca = getattr(pendiente, "mark_dead", None)
                    if callable(marca):
                        marca()

    while rnd < max_rounds:
        rnd += 1
        if verbose:
            log.append(f"-- Ronda {rnd} --")
        # Fase de guarida: iniciativa 20 con empates perdidos (tras todos
        # los >= 20 y antes del primero con < 20; 0 = al inicio de la
        # ronda, len = al final). Siempre activa: sin fichero de guarida
        # la fase no hace nada ni consume RNG.
        lair_cut = next(
            (i for i, a in enumerate(order) if a.initiative < 20),
            len(order))
        for idx, actor in enumerate(order):
            if (idx == lair_cut and not combat_finished(order)):
                lair_phase(_nuevo_ctx(actor))
                if combat_finished(order):
                    break
            if not _turno(actor):
                break
        # Fase de guarida al final de la ronda: todos los combatientes
        # tenían iniciativa >= 20.
        if (lair_cut == len(order) and not combat_finished(order)):
            lair_phase(_nuevo_ctx(order[0]))
        if combat_finished(order):
            break

    equipos = living_teams(order)
    if "PJ" in equipos and "NPC" not in equipos:
        winner = "PJ"
    elif "NPC" in equipos and "PJ" not in equipos:
        winner = "NPC"
    else:
        winner = "Empate"
    espacios_gastados = {
        c.name: sum(c.spell_slots.maximos) - sum(c.spell_slots.actuales)
        for c in order if getattr(c, "spell_slots", None) is not None
    }
    return CombatResult(winner, rnd, {c.name: max(c.hp, 0) for c in order}, log,
                        action_uses=action_uses, area_targets_hit=area_targets_hit,
                        conditions_applied=conditions_applied,
                        turns_lost_incapacitated=turns_lost_incapacitated,
                        escape_attempts=escape_attempts,
                        escape_successes=escape_successes,
                        attacks_vs_at_range=len(attacks_at_range),
                        legendary_actions_used=legendary_stats["actions"],
                        legendary_points_spent=int(legendary_stats["points"]),
                        legendary_resistances_used=int(legendary_stats["resistances"]),
                        spell_slots_spent=espacios_gastados)

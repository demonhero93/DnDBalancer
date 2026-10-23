"""Motor de combate: ataques, iniciativa y bucle de rondas."""
import inspect
import random
from dataclasses import dataclass, field
from typing import Any

try:
    from .actions import (
        ActionType,
        AttackAction,
        CombatContext,
        MultiattackAction,
        TurnResources,
        WeaponAttackAction,
    )
    from .attack import Attack
    from .combatant import Combatant, CombatantType, valid_targets
    from .conditions import Condition, end_turn, remove_condition
    from .damage import DamageRecorder, apply_damage_modifiers, inflict_damage
    from .dice import RollMode, d20, roll_d20, roll_dice
    from .legendary import legendary_phase
    from .randomness import pick
    from .roll_modifiers import (
        AttackRange, RANGED_COVER_AC_BONUS, attack_modifiers, effective_ac,
        resolve_attack_range,
    )
    from .tactics import first_target_policy, random_policy
    from .usage import begin_turn
except ImportError:
    from actions import (
        ActionType,
        AttackAction,
        CombatContext,
        MultiattackAction,
        TurnResources,
        WeaponAttackAction,
    )
    from attack import Attack
    from combatant import Combatant, CombatantType, valid_targets
    from damage import DamageRecorder, apply_damage_modifiers, inflict_damage
    from dice import RollMode, d20, roll_d20, roll_dice
    from randomness import pick
    from tactics import first_target_policy, random_policy
    try:
        from conditions import Condition, end_turn, remove_condition
    except ImportError:
        from dnd_sim.conditions import Condition, end_turn, remove_condition
    try:
        from dnd_sim.legendary import legendary_phase
    except ImportError:
        from legendary import legendary_phase
    try:
        from roll_modifiers import (
            AttackRange, RANGED_COVER_AC_BONUS, attack_modifiers, effective_ac,
            resolve_attack_range,
        )
    except ImportError:
        from dnd_sim.roll_modifiers import (
            AttackRange, RANGED_COVER_AC_BONUS, attack_modifiers, effective_ac,
            resolve_attack_range,
        )
    try:
        from usage import begin_turn
    except ImportError:
        from dnd_sim.usage import begin_turn


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


def resolve_roll_mode(attacker: Combatant, target: Combatant,
                      attack: Any = None, rng: Any = None) -> RollMode:
    """Resuelve el modo de tirada por reglas (5e).

    Fuente única: :func:`dnd_sim.roll_modifiers.attack_modifiers` (indicadores
    estáticos + condiciones). Sin ``attack`` solo se aplican los indicadores
    estáticos (compatibilidad).
    """
    if attack is not None:
        return attack_modifiers(attacker, target, attack, rng).mode
    has_adv = bool(getattr(attacker, "attacks_with_advantage", False)) or bool(
        getattr(target, "grants_advantage_to_attackers", False)
    )
    has_dis = bool(getattr(attacker, "attacks_with_disadvantage", False)) or bool(
        getattr(target, "grants_disadvantage_to_attackers", False)
    )
    if has_adv and has_dis:
        return RollMode.NORMAL
    if has_adv:
        return RollMode.ADVANTAGE
    if has_dis:
        return RollMode.DISADVANTAGE
    return RollMode.NORMAL


def _mode_tag(mode: RollMode, result, reason: str = "") -> str:
    """ Sufijo de log con el modo de tirada y su motivo."""
    if mode == RollMode.ADVANTAGE:
        tag = f" (ventaja: {result.rolls[0]}, {result.rolls[1]} -> {result.value}"
        return f"{tag}; {reason})" if reason else f"{tag})"
    if mode == RollMode.DISADVANTAGE:
        tag = f" (desventaja: {result.rolls[0]}, {result.rolls[1]} -> {result.value}"
        return f"{tag}; {reason})" if reason else f"{tag})"
    if reason:
        return f" ({reason})"
    return ""


def _agrandado(combatant: Any) -> bool:
    """¿Tiene activa la condición ENLARGED (agrandado)?"""
    tracker = getattr(combatant, "conditions", None)
    if tracker is None:
        return False
    try:
        return tracker.has(Condition.ENLARGED)
    except Exception:
        return False


def _dados_de_ataque(attacker: Any, atk: Any) -> str:
    """Dados a tirar en ``attack_roll``.

    Si el atacante está agrandado y el ataque declara su variante
    agrandada (la ficha del duergar: «or 11 (2d8 + 2) ... while
    enlarged»), se usan esos dados; si no, los normales.
    """
    dados = str(getattr(atk, "damage", "") or "")
    variante = str(getattr(atk, "enlarged_damage", "") or "")
    if variante and _agrandado(attacker):
        return variante
    return dados


def _bonus_de_tamano(attacker: Any, atk: Any, rng: Any) -> int:
    """+1d4 de las armas agrandadas por el hechizo Enlarge/Reduce.

    El rasgo del duergar ya lleva sus dados duplicados en
    ``enlarged_damage`` (no se suma dos veces). Los ataques de hechizo
    usan la característica de lanzamiento, no Fuerza, así que no reciben
    este bonus («attacks with them [weapons] deal 1d4 extra damage»).
    """
    if not _agrandado(attacker):
        return 0
    if getattr(atk, "enlarged_damage", None):
        return 0
    if str(getattr(atk, "ability", "") or "").strip().lower() != "str":
        return 0
    if not str(getattr(atk, "damage", "") or "").strip():
        return 0
    return roll_dice("1d4", rng)


def attack_roll(attacker: Combatant, target: Combatant, atk: Attack,
                rng: random.Random, log: list[str] | None = None,
                verbose: bool = False, ctx: Any = None) -> None:
    """Resuelve un ataque.

    Secuencia (documentada):

    1. ``resolve_attack_range``: se decide el rango (un arma "cuerpo a
       cuerpo o a distancia" se decide con ``pick`` en **cada** ataque, lo
       que consume RNG).
    2. Se actualiza ``attacker.state.at_range`` (un ataque a distancia deja
       al atacante a distancia; uno cuerpo a cuerpo, cerca).
    3. ``attack_modifiers`` con el rango ya resuelto. Un atacante
       invisible ataca con ventaja; por eso su invisibilidad se quita
       justo **después** de calcular el modo («until it attacks»: este
       ataque ya se resuelve con ventaja).
    4. Tirada del d20 con el modo obtenido.
    5. Se compara contra la CA efectiva del objetivo (+2 si está a
       distancia).
    """
    if not attacker.is_hostile_to(target):
        raise ValueError(
            f"{attacker.name} no es hostil a {target.name}: no se permite fuego amigo."
        )
    # (1) Rango resuelto.
    rango = resolve_attack_range(atk, rng)
    # (2) Estado de distancia del atacante.
    _actualizar_distancia(attacker, rango, log)
    # (3) Modificadores (el rango ya está decidido). Un atacante invisible
    # ataca **con ventaja**, así que la invisibilidad se quita **después**
    # de calcular el modo: «until it attacks» significa que este ataque ya
    # se resuelve con ventaja y a partir de aquí deja de estar invisible
    # (# TODO: también al lanzar un hechizo o al usar Enlarge; hoy solo la
    # rompe un ataque).
    modifiers = attack_modifiers(attacker, target, atk, rango)
    mode = modifiers.mode
    if remove_condition(attacker, Condition.INVISIBLE, None) and log is not None:
        log.append(f"  {attacker.name} deja de estar invisible (ataca)")
    # (4) Tirada.
    result = roll_d20(rng, mode)
    roll = result.value
    bonus = attacker.to_hit(atk)
    total = roll + bonus
    crit = roll == 20
    # (5) CA efectiva (cobertura a distancia).
    ca_efectiva = effective_ac(target)
    # Estadística: ataques recibidos por objetivos a distancia.
    if getattr(getattr(target, "state", None), "at_range", False):
        recibidos = getattr(ctx, "attacks_at_range", None) if ctx is not None else None
        if recibidos is not None:
            try:
                recibidos.append(1)
            except Exception:
                pass
    hit = crit or (roll != 1 and total >= ca_efectiva)
    # Crítico automático (objetivo paralizado o inconsciente a cuerpo a cuerpo):
    # el impacto es crítico aunque el d20 no sea 20; un 1 natural sigue fallando.
    if hit and modifiers.auto_crit_on_hit:
        crit = True
    log_enabled = log is not None
    if hit:
        raw_dmg = 0
        if str(getattr(atk, "damage", "") or "").strip() not in ("", "0"):
            # Un ataque sin daño (p. ej. la Telaraña) no tira dados. Con la
            # condición ENLARGED se usan los dados agrandados de la ficha
            # (o se añade el +1d4 del hechizo Enlarge/Reduce).
            dados = _dados_de_ataque(attacker, atk)
            raw_dmg = max(0, roll_dice(dados, rng, crit=crit)
                          + attacker.dmg_bonus(atk))
            raw_dmg += _bonus_de_tamano(attacker, atk, rng)
        dt = atk.damage_type
        if dt in target.immunities:
            dmg = 0
            mod_tag = " (inmune)"
        elif dt in target.resistances and dt in target.vulnerabilities:
            after_resist = raw_dmg // 2
            dmg = after_resist * 2
            mod_tag = (f" (resistencia: {raw_dmg} -> {after_resist})"
                       f" (vulnerable: {after_resist} -> {dmg})")
        elif dt in target.resistances:
            dmg = raw_dmg // 2
            mod_tag = f" (resistencia: {raw_dmg} -> {dmg})"
        elif dt in target.vulnerabilities:
            dmg = raw_dmg * 2
            mod_tag = f" (vulnerable: {raw_dmg} -> {dmg})"
        else:
            dmg = raw_dmg
            mod_tag = ""
        dmg = apply_damage_modifiers(raw_dmg, dt, target)
        inflict_damage(target, dmg, dt, source=attacker, ctx=ctx)
        # Daño adicional del arma (p. ej. el 1d6 de fuego del Warhammer
        # del azer o el ácido del mordisco de un dragón). Cada entrada
        # tiene su propio tipo, así que resistencia/inmunidad/vulnerabilidad
        # se resuelven por separado y se suman al total. Los dados extra
        # también se duplican en crítico (como el daño principal).
        extra_total = 0
        extra_partes = []
        for _extra in getattr(atk, "extra_damage", None) or []:
            _raw_x = roll_dice(_extra.damage, rng, crit=crit)
            _dmg_x = apply_damage_modifiers(_raw_x, _extra.damage_type, target)
            if _dmg_x > 0:
                inflict_damage(target, _dmg_x, _extra.damage_type,
                               source=attacker, ctx=ctx)
            extra_total += _dmg_x
            extra_partes.append(f"{_dmg_x} {_extra.damage_type.value}")
        extra_tag = (" + " + " + ".join(extra_partes)) if extra_partes else ""
        _riders_to_run = list(getattr(atk, "save_riders", None) or [])
        _log_first = log_enabled
        if log_enabled:
            mode_tag = _mode_tag(mode, result, modifiers.reason())
            tag = " CRÍTICO" if crit else ""
            ca_tag = (f" (+{RANGED_COVER_AC_BONUS} cobertura a distancia)"
                      if getattr(getattr(target, "state", None), "at_range", False) else "")
            log.append(f"  {attacker.name} -> {target.name} con {atk.name}: "
                       f"{roll}{mode_tag}+{bonus}={total} vs CA {ca_efectiva}{ca_tag}{tag}, "
                       f"{dmg} daño{extra_tag} (HP {max(target.hp, 0)}/{target.max_hp}){mod_tag}")
        for _rider in _riders_to_run:
            try:
                from .saves import resolve_save_damage as _rsd
            except ImportError:
                try:
                    from saves import resolve_save_damage as _rsd
                except ImportError:
                    from dnd_sim.saves import resolve_save_damage as _rsd
            _rctx = type("RiderCtx", (), {})()
            _rctx.rng = rng
            _rctx.log = log if _log_first else None
            _rctx.verbose = _log_first
            _rsd(attacker, target, _rider, _rctx)
        # Riders de condición (tras el daño y los riders de daño).
        _apply_condition_riders(attacker, target, atk, rng, log if _log_first else None, ctx)
        # Reacción del objetivo golpeado (p. ej. Heated Body del azer): se
        # ejecuta en cada impacto, aunque el daño haya sido 0 por inmunidad.
        _trigger_after_being_hit(target, attacker, rango,
                                 log if _log_first else None, ctx, rng)
        # Efectos posteriores al impacto (p. ej. el enganche del cloaker):
        # reciben los modificadores para poder ver si el ataque iba con
        # ventaja (enganche a la cabeza).
        for _efecto in getattr(atk, "on_hit_effects", None) or []:
            _efecto.execute(attacker, target, ctx, modifiers)
        # Reacción del objetivo al recibir daño (p. ej. Hellish Rebuke).
        if dmg + extra_total > 0:
            _reaccion_si_procede(target, ctx)
    elif log_enabled:
        mode_tag = _mode_tag(mode, result, modifiers.reason())
        ca_tag = (f" (+{RANGED_COVER_AC_BONUS} cobertura a distancia)"
                  if getattr(getattr(target, "state", None), "at_range", False) else "")
        log.append(f"  {attacker.name} -> {target.name} con {atk.name}: "
                   f"{roll}{mode_tag}+{bonus}={total} vs CA {ca_efectiva}{ca_tag}, falla")


def _actualizar_distancia(attacker, rango, log) -> None:
    """El atacante queda a distancia tras un ataque a distancia (y al revés)."""
    state = getattr(attacker, "state", None)
    if state is None:
        return
    a_distancia = rango is AttackRange.RANGED
    if getattr(state, "at_range", False) == a_distancia:
        return
    state.at_range = a_distancia
    if log is not None:
        nombre = getattr(attacker, "name", attacker)
        log.append(f"  {nombre} {'pasa a distancia' if a_distancia else 'se acerca'}")


def _apply_condition_riders(attacker, target, atk, rng, log, ctx) -> None:
    """Aplica las condiciones del ataque (si el objetivo falla la salvación)."""
    riders = list(getattr(atk, "condition_riders", None) or [])
    if not riders:
        return
    try:
        from .conditions import RepeatSave, apply_condition
    except ImportError:
        try:
            from conditions import RepeatSave, apply_condition
        except ImportError:
            from dnd_sim.conditions import RepeatSave, apply_condition
    try:
        from .saves import registrar_resistencia, saving_throw
    except ImportError:
        try:
            from saves import registrar_resistencia, saving_throw
        except ImportError:
            from dnd_sim.saves import registrar_resistencia, saving_throw

    _ctx = ctx
    if _ctx is None:
        _ctx = type("RiderCtx", (), {})()
        _ctx.rng = rng
        _ctx.log = log
        _ctx.verbose = log is not None
        _ctx.conditions_applied = None

    for rider in riders:
        repeat = None
        if rider.repeat_save:
            repeat = RepeatSave(ability=rider.save_ability, dc=rider.dc)
        if rider.save_ability is None:
            # Sin salvación: la condición se aplica al impactar.
            apply_condition(
                target, rider.condition, _ctx,
                source=attacker,
                duration_rounds=rider.duration_rounds,
                repeat_save=repeat,
                escape=rider.escape,
            )
            continue
        sr = saving_throw(target, rider.save_ability, rider.dc, rng)
        sr = registrar_resistencia(_ctx, target, sr)
        if sr.success:
            continue
        apply_condition(
            target, rider.condition, _ctx,
            source=attacker,
            duration_rounds=rider.duration_rounds,
            repeat_save=repeat,
            escape=rider.escape,
        )


def _trigger_after_being_hit(target: Any, attacker: Any, rango: Any,
                             log: Any, ctx: Any, rng: Any = None) -> None:
    """Dispara los rasgos de ``target`` que reaccionan a ser golpeado.

    Hoy solo ``Heated Body`` (azer): daño de fuego a quien impacta cuerpo a
    cuerpo. El hook se ejecuta tras el daño, en **cada** impacto (aunque el
    daño haya sido 0 por inmunidad del objetivo), porque el trigger de la
    ficha es el impacto, no el daño recibido.
    """
    traits = list(getattr(target, "traits", None) or [])
    if not traits:
        return
    hookable = [t for t in traits if getattr(t, "after_being_hit", None)]
    if not hookable:
        return
    _ctx = ctx
    if _ctx is None:
        _ctx = type("HitCtx", (), {})()
        _ctx.rng = rng
        _ctx.log = log
        _ctx.verbose = log is not None
    elif getattr(_ctx, "rng", None) is None:
        _ctx.rng = rng
    for trait in hookable:
        try:
            trait.after_being_hit(target, attacker, rango, ctx=_ctx)
        except Exception:
            continue


def _reaccion_si_procede(target: Any, ctx: Any) -> None:
    """Dispara la reacción de ``target`` si acaba de recibir daño (5e).

    El import es perezoso para evitar ciclos (``spells`` importa ``combat``
    dentro de sus funciones).
    """
    if target is None or ctx is None:
        return
    try:
        from .spells import trigger_reaction
    except ImportError:  # pragma: no cover - ejecución como script suelto
        try:
            from spells import trigger_reaction
        except ImportError:
            from dnd_sim.spells import trigger_reaction
    try:
        trigger_reaction(target, ctx)
    except Exception:
        pass


def roll_initiative(combatants: list[Combatant], rng: random.Random) -> list[Combatant]:
    for c in combatants:
        c.initiative = d20(rng) + c.abilities.mod("dex")
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


def run_combat(combatants: list[Combatant], rng: random.Random,
               verbose: bool = False, max_rounds: int = 100,
               policy=None) -> CombatResult:
    """Ejecuta un combate y devuelve el resultado con sus estadísticas.

    El daño infligido se registra durante el combate (:class:`DamageRecorder`)
    para poder informar del daño medio de cada combatiente.
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
    while rnd < max_rounds:
        rnd += 1
        if verbose:
            log.append(f"-- Ronda {rnd} --")
        for actor in order:
            if not actor.alive:
                continue
            enemies = valid_targets(actor, combatants=order)
            if not enemies:
                break
            ctx = CombatContext(
                rng=rng, actor=actor, combatants=order, round=rnd,
                log=log if verbose else None, verbose=verbose, resources=None,
                action_uses=action_uses, area_targets_hit=area_targets_hit,
                conditions_applied=conditions_applied,
                escape_attempts=escape_attempts, escape_successes=escape_successes,
                attacks_at_range=attacks_at_range,
                legendary_stats=legendary_stats,
            )
            # Inicio de turno: recursos nuevos y tiradas de recarga de las
            # acciones descargadas del actor. Si está incapacitado, pierde
            # el turno (sin política y sin consumir RNG).
            resources = begin_turn(actor, ctx)
            if not ctx.skip_turn:
                # Ejecuta como mucho una ACTION y una BONUS_ACTION por turno.
                for action_type in (ActionType.ACTION, ActionType.BONUS_ACTION):
                    candidates = [
                        a for a in getattr(actor, "actions", [])
                        if getattr(a, "action_type", None) == action_type
                        and a.can_use(resources, ctx)
                        and getattr(actor, "can_act", True)
                    ]
                    if not candidates:
                        continue
                    chosen = _invoke_policy(policy, ctx, candidates)
                    if chosen is None:
                        chosen = pick(rng, candidates)
                    chosen.execute(ctx)
                    resources.use(action_type)
                    # El uso limitado se gasta aquí (una vez, aunque el área
                    # afecte a pocos objetivos).
                    usage = getattr(chosen, "usage", None)
                    if usage is not None:
                        usage.spend()
                    action_name = getattr(chosen, "name", "") or type(chosen).__name__
                    action_uses[action_name] = action_uses.get(action_name, 0) + 1
                    enemies = valid_targets(actor, combatants=order)
                    if not enemies:
                        break
            else:
                # Turno perdido por incapacitación.
                turns_lost_incapacitated[actor.name] = (
                    turns_lost_incapacitated.get(actor.name, 0) + 1)
            # Final del turno: salvaciones de repetición y duración de las
            # condiciones del propio combatiente.
            end_turn(actor, ctx)
            # Fase legendaria: los demás monstruos legítimos pueden usar una
            # acción legendaria tras el turno de este combatiente.
            legendary_phase(actor, ctx)
            players_alive = any(c.alive and c.combatant_type == CombatantType.PLAYER for c in order)
            npcs_alive = any(c.alive and c.combatant_type == CombatantType.NPC for c in order)
            if not players_alive or not npcs_alive:
                break
        players_alive = any(c.alive and c.combatant_type == CombatantType.PLAYER for c in order)
        npcs_alive = any(c.alive and c.combatant_type == CombatantType.NPC for c in order)
        if not players_alive or not npcs_alive:
            break

    players_alive = any(c.alive and c.combatant_type == CombatantType.PLAYER for c in order)
    npcs_alive = any(c.alive and c.combatant_type == CombatantType.NPC for c in order)
    if players_alive and not npcs_alive:
        winner = "PJ"
    elif npcs_alive and not players_alive:
        winner = "NPC"
    else:
        winner = "Empate"
    return CombatResult(winner, rnd, {c.name: max(c.hp, 0) for c in order}, log,
                        action_uses=action_uses, area_targets_hit=area_targets_hit,
                        conditions_applied=conditions_applied,
                        turns_lost_incapacitated=turns_lost_incapacitated,
                        escape_attempts=escape_attempts,
                        escape_successes=escape_successes,
                        attacks_vs_at_range=len(attacks_at_range),
                        legendary_actions_used=legendary_stats["actions"],
                        legendary_points_spent=int(legendary_stats["points"]),
                        legendary_resistances_used=int(legendary_stats["resistances"]))

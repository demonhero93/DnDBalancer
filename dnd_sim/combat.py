"""Motor de combate: ataques, iniciativa y bucle de rondas."""
import inspect
import random
from dataclasses import dataclass

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
    from .damage import apply_damage_modifiers, inflict_damage
    from .dice import RollMode, d20, roll_d20, roll_dice
    from .randomness import pick
    from .tactics import first_target_policy, random_policy
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
    from damage import apply_damage_modifiers, inflict_damage
    from dice import RollMode, d20, roll_d20, roll_dice
    from randomness import pick
    from tactics import first_target_policy, random_policy


@dataclass
class CombatResult:
    winner: str
    rounds: int
    survivors: dict[str, int]  # nombre -> hp restante
    log: list[str]


def resolve_roll_mode(attacker: Combatant, target: Combatant) -> RollMode:
    """Resuelve el modo de tirada por fuentes de ventaja/desventaja (regla 5e)."""
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


def attack_roll(attacker: Combatant, target: Combatant, atk: Attack,
                rng: random.Random, log: list[str] | None = None,
                verbose: bool = False) -> None:
    if not attacker.is_hostile_to(target):
        raise ValueError(
            f"{attacker.name} no es hostil a {target.name}: no se permite fuego amigo."
        )
    mode = resolve_roll_mode(attacker, target)
    result = roll_d20(rng, mode)
    roll = result.value
    bonus = attacker.to_hit(atk)
    total = roll + bonus
    crit = roll == 20
    hit = crit or (roll != 1 and total >= target.ac)
    log_enabled = log is not None
    if hit:
        raw_dmg = max(0, roll_dice(atk.damage, rng, crit=crit) + attacker.dmg_bonus(atk))
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
        inflict_damage(target, dmg, dt, source=attacker)
        _riders_to_run = list(getattr(atk, "save_riders", None) or [])
        _log_first = log_enabled
        if log_enabled:
            mode_tag = ""
            if mode == RollMode.ADVANTAGE:
                mode_tag = f" (ventaja: {result.rolls[0]}, {result.rolls[1]} -> {result.value})"
            elif mode == RollMode.DISADVANTAGE:
                mode_tag = f" (desventaja: {result.rolls[0]}, {result.rolls[1]} -> {result.value})"
            tag = " CRÍTICO" if crit else ""
            log.append(f"  {attacker.name} -> {target.name} con {atk.name}: "
                       f"{roll}{mode_tag}+{bonus}={total} vs CA {target.ac}{tag}, "
                       f"{dmg} daño (HP {max(target.hp, 0)}/{target.max_hp}){mod_tag}")
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
    elif log_enabled:
        mode_tag = ""
        if mode == RollMode.ADVANTAGE:
            mode_tag = f" (ventaja: {result.rolls[0]}, {result.rolls[1]} -> {result.value})"
        elif mode == RollMode.DISADVANTAGE:
            mode_tag = f" (desventaja: {result.rolls[0]}, {result.rolls[1]} -> {result.value})"
        log.append(f"  {attacker.name} -> {target.name} con {atk.name}: "
                   f"{roll}{mode_tag}+{bonus}={total} vs CA {target.ac}, falla")


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
    if policy is None:
        policy = random_policy
    for c in combatants:
        c.reset()
    order = roll_initiative(combatants, rng)

    log: list[str] = []
    rnd = 0
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
            resources = TurnResources()
            ctx = CombatContext(
                rng=rng, actor=actor, combatants=order, round=rnd,
                log=log if verbose else None, verbose=verbose, resources=resources,
            )
            # Ejecuta como mucho una ACTION y una BONUS_ACTION por turno.
            for action_type in (ActionType.ACTION, ActionType.BONUS_ACTION):
                candidates = [
                    a for a in getattr(actor, "actions", [])
                    if getattr(a, "action_type", None) == action_type
                    and a.can_use(resources, ctx)
                ]
                if not candidates:
                    continue
                chosen = _invoke_policy(policy, ctx, candidates)
                if chosen is None:
                    chosen = pick(rng, candidates)
                chosen.execute(ctx)
                resources.use(action_type)
                enemies = valid_targets(actor, combatants=order)
                if not enemies:
                    break
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
    return CombatResult(winner, rnd, {c.name: max(c.hp, 0) for c in order}, log)

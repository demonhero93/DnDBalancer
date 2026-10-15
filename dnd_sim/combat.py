"""Motor de combate: ataques, iniciativa y bucle de rondas."""
import random
from dataclasses import dataclass

try:
    from .attack import Attack
    from .combatant import Combatant
    from .damage import apply_damage_modifiers
    from .dice import d20, roll_dice
except ImportError:
    from attack import Attack
    from combatant import Combatant
    from damage import apply_damage_modifiers
    from dice import d20, roll_dice


@dataclass
class CombatResult:
    winner: str
    rounds: int
    survivors: dict[str, int]  # nombre -> hp restante
    log: list[str]


def attack_roll(attacker: Combatant, target: Combatant, atk: Attack,
                rng: random.Random, log: list[str] | None = None) -> None:
    roll = d20(rng)
    bonus = attacker.to_hit(atk)
    total = roll + bonus
    crit = roll == 20
    hit = crit or (roll != 1 and total >= target.ac)
    if hit:
        raw_dmg = max(0, roll_dice(atk.damage, rng, crit=crit) + attacker.dmg_bonus(atk))
        dt = atk.damage_type
        # Modificadores de daño del objetivo, en orden: inmunidad, resistencia, vulnerabilidad.
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
        # Fuente de verdad canónica.
        dmg = apply_damage_modifiers(raw_dmg, dt, target)
        target.hp -= dmg
        if log is not None:
            tag = " CRÍTICO" if crit else ""
            log.append(f"  {attacker.name} -> {target.name} con {atk.name}: "
                       f"{roll}+{bonus}={total} vs CA {target.ac}{tag}, "
                       f"{dmg} daño (HP {max(target.hp, 0)}/{target.max_hp}){mod_tag}")
    elif log is not None:
        log.append(f"  {attacker.name} -> {target.name} con {atk.name}: "
                   f"{roll}+{bonus}={total} vs CA {target.ac}, falla")


def roll_initiative(combatants: list[Combatant], rng: random.Random) -> list[Combatant]:
    for c in combatants:
        c.initiative = d20(rng) + c.abilities.mod("dex")
    return sorted(combatants, key=lambda c: (c.initiative, c.abilities.dex), reverse=True)


def run_combat(combatants: list[Combatant], rng: random.Random,
               verbose: bool = False, max_rounds: int = 100) -> CombatResult:
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
            enemies = [c for c in order if c.team != actor.team and c.alive]
            if not enemies:
                break
            if actor.attacks:  # sin IA: primer ataque, primer enemigo vivo
                attack_roll(actor, enemies[0], actor.attacks[0], rng, log if verbose else None)
        if len({c.team for c in order if c.alive}) <= 1:
            break

    teams_alive = {c.team for c in order if c.alive}
    winner = teams_alive.pop() if len(teams_alive) == 1 else "Empate"
    return CombatResult(winner, rnd, {c.name: max(c.hp, 0) for c in order}, log)

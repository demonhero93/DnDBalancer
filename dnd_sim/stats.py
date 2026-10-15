"""Simulaciones repetidas y estadísticas."""
import random
import statistics

try:
    from .combat import run_combat
    from .combatant import Combatant
except ImportError:
    from combat import run_combat
    from combatant import Combatant


def simulate(combatants: list[Combatant], n: int = 1000, seed: int | None = None) -> dict:
    rng = random.Random(seed)
    results = [run_combat(combatants, rng) for _ in range(n)]
    teams = {c.team for c in combatants}
    rounds = [r.rounds for r in results]
    return {
        "n": n,
        "win_rate": {t: sum(r.winner == t for r in results) / n for t in teams},
        "draw_rate": sum(r.winner == "Empate" for r in results) / n,
        "rounds_avg": statistics.mean(rounds),
        "rounds_median": statistics.median(rounds),
        "rounds_max": max(rounds),
        "hp_left_avg": {c.name: statistics.mean(r.survivors[c.name] for r in results)
                        for c in combatants},
    }


def print_report(stats: dict) -> None:
    print(f"\n=== {stats['n']} simulaciones ===")
    for team, rate in stats["win_rate"].items():
        print(f"Victorias {team}: {rate:.1%}")
    print(f"Empates: {stats['draw_rate']:.1%}")
    print(f"Rondas: media {stats['rounds_avg']:.1f} | mediana {stats['rounds_median']} "
          f"| máx {stats['rounds_max']}")
    for name, hp in stats["hp_left_avg"].items():
        print(f"HP medio restante de {name}: {hp:.1f}")

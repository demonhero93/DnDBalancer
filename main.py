"""Ejemplo de uso: python main.py"""
import random
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from dnd_sim import Abilities, Attack, Combatant, load_monster
    from dnd_sim.combat import run_combat
    from dnd_sim.stats import print_report, simulate
except ImportError:
    from abilities import Abilities
    from attack import Attack
    from combatant import Combatant
    from combat import run_combat
    from stats import print_report, simulate
    try:
        from dnd_sim import load_monster
    except ImportError:
        from loader import load_monster

guerrero = Combatant(
    name="Guerrero", team="PJ", max_hp=28, ac=18, proficiency=2,
    abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
    attacks=[Attack("Espada larga", "1d8", ability="str")],
)
ogro = load_monster("ogre")

if __name__ == "__main__":
    res = run_combat([guerrero, ogro], random.Random(42), verbose=True)
    print("\n".join(res.log))
    print(f"\nGanador: {res.winner} en {res.rounds} rondas")

    print_report(simulate([guerrero, ogro], n=100000, seed=1))
"""Ejemplo de uso: python main.py"""
import argparse
import random
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from dnd_sim import Abilities, Attack, PlayerCharacter, load_monster, run_combat
    from dnd_sim.stats import print_report, simulate
except ImportError:
    from abilities import Abilities
    from attack import Attack
    from combatant import PlayerCharacter
    from data.loader import load_monster
    from combat import run_combat
    from stats import print_report, simulate


def _parse_monster_token(token: str):
    """Devuelve (index, cantidad) aceptando 'index' o 'index:N'."""
    if ":" in token:
        index, count_text = token.rsplit(":", 1)
        count = int(count_text)
    else:
        index, count = token, 1
    if count < 1:
        raise argparse.ArgumentTypeError("La cantidad debe ser >= 1")
    return index, count


def _load_party(specs: list[str]) -> list:
    monsters: list[Combatant] = []
    for spec in specs:
        index, count = _parse_monster_token(spec)
        for i in range(1, count + 1):
            monster = load_monster(index)
            if count > 1:
                monster.name = f"{monster.name} {i}"
            monsters.append(monster)
    return monsters


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador de combate D&D 5e")
    parser.add_argument(
        "--monster", "-m", action="append", default=[],
        help="Monstruo a cargar desde la API (formato index o index:cantidad). "
             "Repetible. Ej: --monster owlbear --monster goblin:3",
    )
    parser.add_argument("-n", "--simulations", type=int, default=10000,
                        help="Número de simulaciones (default: 1000).")
    parser.add_argument("--seed", type=int, default=1, help="Semilla RNG.")
    parser.add_argument("--verbose", action="store_true", help="Muestra el primer combate.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    specs = args.monster if args.monster else ["giant-spider"]
    monsters = _load_party(specs)

    # El PJ sí se define aquí (personaje jugador).
    guerrero = PlayerCharacter(
        name="Guerrero", max_hp=28, ac=18, proficiency=2,
        abilities=Abilities(str=16, dex=12, con=14, int=10, wis=12, cha=8),
        attacks=[Attack("Espada larga", "1d8", ability="str")],
    )
    
    picaro = PlayerCharacter(
        name="Pícaro", max_hp=22, ac=15, proficiency=2,
        abilities=Abilities(str=10, dex=16, con=12, int=14, wis=10, cha=14),
        attacks=[Attack("Daga", "1d4", ability="dex")],
    )
    
    monje = PlayerCharacter(
        name="Monje", max_hp=24, ac=17, proficiency=2,
        abilities=Abilities(str=12, dex=16, con=14, int=10, wis=14, cha=8),
        attacks=[Attack("Puño", "1d6", ability="dex")],
    )
    

    combatants = [guerrero, picaro, monje] + monsters

    # Un combate de ejemplo con semilla fija para el log.
    res = run_combat(combatants, random.Random(args.seed), verbose=True)
    print("\n".join(res.log))
    print(f"\nGanador: {res.winner} en {res.rounds} rondas")

    report = simulate(combatants, n=args.simulations, seed=args.seed)
    print_report(report)


if __name__ == "__main__":
    main()

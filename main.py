"""Ejemplo de uso: python main.py"""
import argparse
import random
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from dnd_sim import (Abilities, Attack, AttackRange, PlayerCharacter,
                     load_monster, run_combat)
from dnd_sim.engine.stats import print_report, simulate


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


def _load_party(specs: list[str], legendary_p: float = 1.0,
                resistance_p: float = 1.0) -> list:
    monsters: list[Combatant] = []
    for spec in specs:
        index, count = _parse_monster_token(spec)
        for i in range(1, count + 1):
            monster = load_monster(index)
            if count > 1:
                monster.name = f"{monster.name} {i}"
            # Probabilidades de las acciones y la resistencia legendarias.
            legendary = getattr(monster, "legendary", None)
            if legendary is not None:
                legendary.use_probability = legendary_p
                legendary.resistance_probability = resistance_p
            monsters.append(monster)
    return monsters


# Plantillas de PJ (el grupo se elige con --party).
# Los ataques pueden ser ("nombre", "dados", "característica", rango) para
# marcar los que son a distancia (el arquero deja al atacante a distancia).
PARTY_TEMPLATES = [
    dict(name="Guerrero", max_hp=50, ac=18, proficiency=2,
         abilities=dict(str=16, dex=12, con=14, int=10, wis=12, cha=8),
         attacks=[("Espada larga", "1d8", "str", "melee"),
                  ("Arco corto", "1d6", "dex", "ranged")]),
    dict(name="Pícaro", max_hp=50, ac=15, proficiency=2,
         abilities=dict(str=10, dex=16, con=12, int=14, wis=10, cha=14),
         attacks=[("Daga", "1d4", "dex", "melee")]),
    dict(name="Monje", max_hp=50, ac=17, proficiency=2,
         abilities=dict(str=12, dex=16, con=14, int=10, wis=14, cha=8),
         attacks=[("Puño", "1d6", "dex", "melee")]),
    dict(name="Clérigo", max_hp=50, ac=16, proficiency=2,
         abilities=dict(str=14, dex=10, con=14, int=8, wis=16, cha=12),
         attacks=[("Maza", "1d6", "str", "melee")]),
]


def _build_party(size: int) -> list:
    """Construye el grupo de PJ a partir de las plantillas."""
    if size < 1 or size > len(PARTY_TEMPLATES):
        raise ValueError(
            f"El grupo debe tener entre 1 y {len(PARTY_TEMPLATES)} personajes."
        )
    party = []
    for template in PARTY_TEMPLATES[:size]:
        ataques = []
        for datos in template["attacks"]:
            nombre, dado, habilidad = datos[0], datos[1], datos[2]
            rango = datos[3] if len(datos) > 3 else "melee"
            ataques.append(
                Attack(nombre, dado, ability=habilidad,
                       range_type=AttackRange(rango))
            )
        party.append(
            PlayerCharacter(
                name=template["name"],
                max_hp=template["max_hp"],
                ac=template["ac"],
                proficiency=template["proficiency"],
                abilities=Abilities(**template["abilities"]),
                attacks=ataques,
            )
        )
    return party


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
    parser.add_argument(
        "--party", type=int, default=3,
        help="Número de personajes jugador del grupo (1-4). Default: 3.",
    )
    parser.add_argument(
        "--legendary-p", type=float, default=1.0,
        help="Probabilidad de que un monstruo legítimo use una acción "
             "legendaria en cada disparo (0.0-1.0). Default: 1.0.",
    )
    parser.add_argument(
        "--resistance-p", type=float, default=1.0,
        help="Probabilidad de que un monstruo Legendary Resistance convierta "
             "un fallo de salvación en éxito (0.0-1.0). Default: 1.0.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    specs = args.monster if args.monster else ["chimera"]
    monsters = _load_party(specs, legendary_p=args.legendary_p,
                           resistance_p=args.resistance_p)

    # Los PJ sí se definen aquí (personajes jugador).
    party = _build_party(args.party)

    combatants = party + monsters

    # Un combate de ejemplo con semilla fija para el log.
    res = run_combat(combatants, random.Random(args.seed), verbose=True)
    print("\n".join(res.log))
    print(f"\nGanador: {res.winner} en {res.rounds} rondas")

    report = simulate(combatants, n=args.simulations, seed=args.seed)
    print_report(report)


if __name__ == "__main__":
    main()

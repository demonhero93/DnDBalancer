"""Ejemplo de uso: python main.py"""
import argparse
import random
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from dnd_sim import (Abilities, Attack, AttackRange, PlayerCharacter,
                     apply_class, load_monster,
                     run_combat)
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
                resistance_p: float = 1.0,
                legendary_points: int | None = None) -> list:
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
                if legendary_points is not None:
                    legendary.points_max = legendary_points
                    legendary.points_left = legendary_points
            monsters.append(monster)
    return monsters


# Plantillas de PJ (el grupo se elige con --party).
# Los ataques pueden ser ("nombre", "dados", "característica", rango) para
# marcar los que son a distancia (el arquero deja al atacante a distancia).
PARTY_TEMPLATES = [
    dict(name="Eldrich_Knight", max_hp=50, ac=18, level=5,
        class_name="fighter",
        subclass_name="eldritch_knight",
        spell_list="wizard",
        save_proficiencies=("str", "con"),
        skill_proficiencies=("athletics", "intimidation", "perception",
                            "survival"),
        abilities=dict(str=16, dex=12, con=14, int=14, wis=10, cha=8),
        attacks=[("Espada larga", "1d8", "str", "melee")]),
    dict(name="Barbaro", max_hp=60, ac=12, level=5,
         class_name="barbarian",
         subclass_name="beast",
         save_proficiencies=("str", "con"),
         skill_proficiencies=("athletics", "intimidation", "perception",
                              "survival"),
        abilities=dict(str=18, dex=14, con=16, int=8, wis=10, cha=12),
        attacks=[("Hacha de batalla", "1d12", "str", "melee")])
    
]


def _build_party(size: int, reckless_p: float | None = None,
                 charge_p: float | None = None) -> list:
    """Construye el grupo de PJ a partir de las plantillas.

    ``reckless_p`` (opcional) fija la probabilidad de Ataque Temerario de
    todo bárbaro del grupo (``--reckless-p``). ``charge_p`` (opcional)
    fija la probabilidad de carga de Ferocious Charger de todo Cavalier
    (``--charge-p``).
    """
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
        pj = PlayerCharacter(
            name=template["name"],
            max_hp=template["max_hp"],
            ac=template["ac"],
            level=template["level"],
            save_proficiencies=set(template.get("save_proficiencies", ())),
            skill_proficiencies=set(template.get("skill_proficiencies", ())),
            skill_expertise=set(template.get("skill_expertise", ())),
            abilities=Abilities(**template["abilities"]),
            attacks=ataques,
        )
        if template.get("class_name"):
            # Salvaciones, habilidades, estilo y rasgos de clase + subclase:
            # todo desde el registro de clases. Las skills de la plantilla
            # deben estar en la lista de su clase.
            extra: dict = {}
            if template.get("spell_list"):
                # Carga perezosa: solo la plantilla que declara lista (EK).
                # Caché en disco primero; la red solo si no hay caché.
                from dnd_sim.data.class_spells import load_class_spell_list
                extra["lista"] = load_class_spell_list(
                    template["spell_list"],
                    nivel_lanzador=template["level"])
            apply_class(pj, template["class_name"],
                        template.get("subclass_name"),
                        skills=template.get("skill_proficiencies", ()),
                        level=template["level"], **extra)
        if reckless_p is not None:
            from dnd_sim.rules.classes.barbarian.features import (
                BarbarianFeatures,
            )
            for trait in getattr(pj, "traits", None) or []:
                if isinstance(trait, BarbarianFeatures):
                    trait.reckless_probability = float(reckless_p)
        if charge_p is not None:
            # Duck-typing: cualquier rasgo con el atributo (Cavalier)
            # acepta la probabilidad de carga.
            for trait in getattr(pj, "traits", None) or []:
                if hasattr(trait, "charge_probability"):
                    trait.charge_probability = float(charge_p)
        party.append(pj)
    return party


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador de combate D&D 5e")
    parser.add_argument(
        "--monster", "-m", action="append", default=[],
        help="Monstruo a cargar desde la API (formato index o index:cantidad). "
             "Repetible. Ej: --monster owlbear --monster goblin:3",
    )
    parser.add_argument("-n", "--simulations", type=int, default=1000,
                        help="Número de simulaciones (default: 1000).")
    parser.add_argument("--seed", type=int, default=1, help="Semilla RNG.")
    parser.add_argument("--verbose", action="store_true", help="Muestra el primer combate.")
    parser.add_argument(
        "--party", type=int, default=2,
        help="Número de personajes jugador del grupo (1-6). Default: 2.",
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
    parser.add_argument(
        "--legendary-points", type=int, default=None,
        help="Puntos legendarios finales por monstruo (fija el valor sin "
             "sumar el bonus de guarida). Default: base + 1.",
    )
    parser.add_argument(
        "--reckless-p", type=float, default=None,
        help="Probabilidad de que un bárbaro use Ataque Temerario en cada "
             "turno (0.0-1.0). Default: 0.5 (constante "
             "RECKLESS_USE_PROBABILITY).",
    )
    parser.add_argument(
        "--charge-p", type=float, default=None,
        help="Probabilidad de que un Cavalier simule un movimiento de "
             "carga en Ferocious Charger (0.0-1.0). Default: 0.5 "
             "(constante CHARGE_MOVE_PROBABILITY).",
    )
    parser.add_argument(
        "--utility-p", type=float, default=None,
        help="Probabilidad de usar una utilitaria (Esquivar/Agarrar/"
             "Empujar) en vez del ataque o acción previsto (0.0-1.0). "
             "Default: 0.05 (constante UTILITY_ACTION_PROBABILITY).",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.utility_p is not None:
        # Fija la probabilidad de utilitarias para todo el simulador.
        from dnd_sim.rules import utility
        utility.UTILITY_ACTION_PROBABILITY = float(args.utility_p)
    specs = args.monster if args.monster else ["troll:2"]
    monsters = _load_party(specs, legendary_p=args.legendary_p,
                           resistance_p=args.resistance_p,
                           legendary_points=args.legendary_points)

    # Los PJ sí se definen aquí (personajes jugador).
    party = _build_party(args.party, reckless_p=args.reckless_p,
                         charge_p=args.charge_p)

    combatants = party + monsters

    # Un combate de ejemplo con semilla fija para el log.
    res = run_combat(combatants, random.Random(args.seed), verbose=True)
    print("\n".join(res.log))
    print(f"\nGanador: {res.winner} en {res.rounds} rondas")

    report = simulate(combatants, n=args.simulations, seed=args.seed)
    print_report(report)


if __name__ == "__main__":
    main()

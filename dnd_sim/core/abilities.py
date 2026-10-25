"""Las 6 características de D&D.

Primitiva de la **capa core**: no depende de ningún otro módulo del
simulador, así que puede importarla cualquiera sin riesgo de ciclos (por
eso aquí vive también la normalización de nombres de característica, que
comparten ``saves``, ``combatant`` y los parsers de ``data``).
"""
from dataclasses import dataclass
from typing import Any

ABILITY_ALIASES: dict[str, str] = {
    "str": "str",
    "strength": "str",
    "s": "str",
    "dex": "dex",
    "dexterity": "dex",
    "d": "dex",
    "con": "con",
    "constitution": "con",
    "c": "con",
    "int": "int",
    "intelligence": "int",
    "i": "int",
    "wis": "wis",
    "wisdom": "wis",
    "w": "wis",
    "cha": "cha",
    "charisma": "cha",
    "h": "cha",
}


def ability_mod(score: int) -> int:
    return (score - 10) // 2


def normalize_ability(value: Any) -> str:
    """Normaliza 'DEX', 'Dexterity', 'dex', etc. a la abreviatura (str/dex/...)."""
    if value is None:
        raise ValueError("Característica inválida: None")
    text = str(value).strip().lower()
    text = text.replace(" ", "").replace("-", "").replace("_", "")
    if text in ABILITY_ALIASES:
        return ABILITY_ALIASES[text]
    # coincidencia por prefijo
    for abbr in ("str", "dex", "con", "int", "wis", "cha"):
        if text.startswith(abbr):
            return abbr
    for name, abbr in ABILITY_ALIASES.items():
        if (name.startswith(text) and len(text) >= 3) or (text.startswith(name) and len(name) >= 3):
            return abbr
    raise ValueError(f"Característica inválida: {value!r}")


@dataclass
class Abilities:
    str: int = 10
    dex: int = 10
    con: int = 10
    int: int = 10
    wis: int = 10
    cha: int = 10

    def mod(self, name: str) -> int:
        return ability_mod(getattr(self, name))

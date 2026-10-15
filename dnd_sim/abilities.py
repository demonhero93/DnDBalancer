"""Las 6 características de D&D."""
from dataclasses import dataclass


def ability_mod(score: int) -> int:
    return (score - 10) // 2


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

"""Personajes (PJ) y monstruos (NPC)."""
from dataclasses import dataclass, field

try:
    from .abilities import Abilities
    from .attack import Attack
    from .damage import DamageType, parse_damage_type
except ImportError:
    from abilities import Abilities
    from attack import Attack
    from damage import DamageType, parse_damage_type


@dataclass
class Combatant:
    name: str
    max_hp: int
    ac: int
    abilities: Abilities = field(default_factory=Abilities)
    attacks: list[Attack] = field(default_factory=list)
    proficiency: int = 2
    team: str = "PJ"
    resistances: set[DamageType] = field(default_factory=set)
    vulnerabilities: set[DamageType] = field(default_factory=set)
    immunities: set[DamageType] = field(default_factory=set)
    hp: int = field(init=False)
    initiative: int = field(init=False, default=0)

    def __post_init__(self):
        self.hp = self.max_hp
        self.resistances = {parse_damage_type(x) for x in (self.resistances or set())}
        self.vulnerabilities = {parse_damage_type(x) for x in (self.vulnerabilities or set())}
        self.immunities = {parse_damage_type(x) for x in (self.immunities or set())}

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def reset(self) -> None:
        self.hp = self.max_hp

    def to_hit(self, atk: Attack) -> int:
        if atk.attack_bonus is not None:
            return atk.attack_bonus
        return self.abilities.mod(atk.ability) + (self.proficiency if atk.proficient else 0)

    def dmg_bonus(self, atk: Attack) -> int:
        if atk.damage_bonus is not None:
            return atk.damage_bonus
        return self.abilities.mod(atk.ability)

"""Definición de un ataque."""
from dataclasses import dataclass, field
from typing import Any

from .damage import DamageType, parse_damage_type

try:
    from .usage import ActionUsage
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from usage import ActionUsage
    except ImportError:
        from dnd_sim.usage import ActionUsage

@dataclass
class Attack:
    name: str
    damage: str                      # "1d8", "2d6+2"...
    ability: str = "str"             # característica usada (str/dex...)
    proficient: bool = True          # suma bonificador de competencia
    attack_bonus: int | None = None  # fija el ataque (útil en fichas de monstruo)
    damage_bonus: int | None = None  # fija el bonus al daño; si None usa el mod
    damage_type: DamageType = DamageType.SLASHING
    only_in_multiattack: bool = False  # si True, no se ofrece como acción suelta
    save_riders: list = field(default_factory=list)
    # Uso limitado opcional del ataque (lo hereda el AttackAction).
    usage: Any = None  # daño con salvación adicional

    def __post_init__(self) -> None:
        # Permite construir Attack con un str como damage_type.
        self.damage_type = parse_damage_type(self.damage_type)
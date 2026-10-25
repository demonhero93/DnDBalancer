"""Definición de un ataque."""
from dataclasses import dataclass, field
from typing import Any

from ..core.enums import AttackRange, DamageType, parse_damage_type


@dataclass
class ExtraDamage:
    """Daño adicional de un arma en cada impacto (sin salvación).

    Ejemplos reales: el Warhammer del azer inflige 1d8+3 contundente
    **más** 1d6 de fuego (Heated Weapons), y el mordisco de un dragón
    añade daño de ácido/fuego sobre el perforante. Son entradas
    **adicionales** («plus ... damage»), no alternativas: se acumulan al
    daño principal.

    Cada entrada lleva su **propio** tipo de daño, de modo que la
    resistencia, vulnerabilidad o inmunidad del objetivo se resuelve por
    separado para cada una. No lleva bonificador de característica (los
    dados que declara la ficha ya son definitivos) ni salvación.
    """

    damage: str                                  # solo dados: "1d6", "2d6"...
    damage_type: DamageType = DamageType.FIRE

    def __post_init__(self) -> None:
        self.damage_type = parse_damage_type(self.damage_type)


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
    usage: Any = None
    # Tipo de alcance (melee / a distancia / ambos), por defecto cuerpo a cuerpo.
    range_type: AttackRange = AttackRange.MELEE
    # Condiciones que aplica si el ataque impacta (dnd_sim.rules.conditions).
    condition_riders: list = field(default_factory=list)  # daño con salvación adicional
    # Efectos que ocurren si el ataque impacta (p. ej. el enganche del
    # cloaker; véase dnd_sim.rules.attach). Los ejecuta ``attack_roll`` tras el
    # daño con la firma: execute(attacker, target, ctx, modifiers).
    on_hit_effects: list = field(default_factory=list)
    # Daño con los dados agrandados («doubles its damage dice», el Enlarge
    # del duergar: su ficha trae «or 11 (2d8 + 2) ... while enlarged»).
    # Si el atacante tiene la condición ENLARGED, ``attack_roll`` usa estos
    # dados en lugar de los normales.
    enlarged_damage: str | None = None
    # Daño adicional por impacto, cada entrada con su propio tipo (p. ej.
    # el 1d6 de fuego del Warhammer del azer o el ácido del mordisco de un
    # dragón). Se aplica tras el daño principal en ``attack_roll``.
    extra_damage: list = field(default_factory=list)  # list[ExtraDamage]

    def __post_init__(self) -> None:
        # Permite construir Attack con un str como damage_type.
        self.damage_type = parse_damage_type(self.damage_type)

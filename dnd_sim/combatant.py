"""Personajes (PJ) y monstruos (NPC)."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

try:
    from .abilities import Abilities
    from .attack import Attack
    from .damage import DamageType, parse_damage_type
except ImportError:
    try:
        from dnd_sim.abilities import Abilities
        from dnd_sim.attack import Attack
        from dnd_sim.damage import DamageType, parse_damage_type
    except ImportError:
        from abilities import Abilities
        from attack import Attack
        from damage import DamageType, parse_damage_type


try:
    from .saves import normalize_ability
except Exception:
    try:
        from dnd_sim.saves import normalize_ability
    except Exception:
        try:
            from saves import normalize_ability
        except Exception:
            def normalize_ability(value):
                return str(value).strip().lower()

class CombatantType(str, Enum):
    PLAYER = "PLAYER"
    NPC = "NPC"


def valid_targets(actor, ctx=None, combatants=None, enemies=None):
    if combatants is None:
        if enemies is not None:
            combatants = enemies
        elif ctx is not None:
            combatants = getattr(ctx, "combatants", None)
            if combatants is None:
                combatants = getattr(ctx, "enemies", None)
        else:
            combatants = None
    if combatants is None:
        return []
    result = []
    for c in combatants:
        if c is actor:
            continue
        if not getattr(c, "alive", True):
            continue
        try:
            if actor.is_hostile_to(c):
                result.append(c)
        except Exception:
            pass
    return result


@dataclass
class Combatant:
    name: str
    max_hp: int
    ac: int
    abilities: Abilities = field(default_factory=Abilities)
    attacks: list[Attack] = field(default_factory=list)
    proficiency: int = 2
    combatant_type: CombatantType = field(default=CombatantType.NPC)
    resistances: set[DamageType] = field(default_factory=set)
    vulnerabilities: set[DamageType] = field(default_factory=set)
    immunities: set[DamageType] = field(default_factory=set)
    # --- Salvaciones ---
    save_overrides: dict[str, int] = field(default_factory=dict)
    save_proficiencies: set[str] = field(default_factory=set)
    saves_with_advantage: set[str] = field(default_factory=set)
    saves_with_disadvantage: set[str] = field(default_factory=set)
    # --- Nuevos campos ---
    weapons: list[Attack] = field(default_factory=list)
    extra_attacks: int = 0
    attacks_with_advantage: bool = False
    attacks_with_disadvantage: bool = False
    grants_advantage_to_attackers: bool = False
    grants_disadvantage_to_attackers: bool = False
    # Multiataque opcional (sustituye a los ataques sueltos como ACTION).
    multiattack: Any = None
    # Acciones adicionales/construidas (WeaponAttackAction, AttackAction...).
    actions: list[Any] = field(default_factory=list)
    hp: int = field(init=False)
    initiative: int = field(init=False, default=0)

    def __post_init__(self):
        if isinstance(self.combatant_type, str):
            self.combatant_type = CombatantType(self.combatant_type)
        self.hp = self.max_hp
        self.resistances = {parse_damage_type(x) for x in (self.resistances or set())}
        self.vulnerabilities = {parse_damage_type(x) for x in (self.vulnerabilities or set())}
        self.immunities = {parse_damage_type(x) for x in (self.immunities or set())}

        # Normalización de campos de salvación.
        raw_overrides = dict(self.save_overrides or {})
        norm_overrides = {}
        for key, val in raw_overrides.items():
            try:
                norm_overrides[normalize_ability(key)] = int(val)
            except Exception:
                norm_overrides[str(key).strip().lower()] = val
        self.save_overrides = norm_overrides
        self.save_proficiencies = {
            normalize_ability(x) for x in (self.save_proficiencies or set())
        }
        self.saves_with_advantage = {
            normalize_ability(x) for x in (self.saves_with_advantage or set())
        }
        self.saves_with_disadvantage = {
            normalize_ability(x) for x in (self.saves_with_disadvantage or set())
        }

        # ---- Construcción automática de acciones (evita duplicados) ----
        try:
            from .actions import ActionType, AttackAction, WeaponAttackAction
        except ImportError:
            try:
                from dnd_sim.actions import ActionType, AttackAction, WeaponAttackAction
            except ImportError:
                from actions import ActionType, AttackAction, WeaponAttackAction

        built: list[Any] = []
        if self.multiattack is None:
            for atk in self.attacks or []:
                if getattr(atk, "only_in_multiattack", False):
                    continue
                built.append(AttackAction(atk, action_type=ActionType.ACTION))
        else:
            built.append(self.multiattack)

        if self.weapons:
            act = WeaponAttackAction("Atacar", ActionType.ACTION)
            built.append(act)

        for a in (self.actions or []):
            built.append(a)

        self.actions = built

        if self.multiattack is not None and hasattr(self.multiattack, "combatant"):
            try:
                self.multiattack.combatant = self
            except Exception:
                pass

    @property
    def team(self) -> str:
        return "PJ" if self.combatant_type == CombatantType.PLAYER else "NPC"

    @team.setter
    def team(self, value) -> None:
        raise AttributeError("El campo 'team' es de solo lectura; deriva del tipo de combatiente.")

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def reset(self) -> None:
        self.hp = self.max_hp
        # Los usos limitados (usos por día, recargas) viven en las acciones,
        # no en el combatiente: se reinician aquí.
        for action in getattr(self, "actions", []) or []:
            usage = getattr(action, "usage", None)
            if usage is not None:
                try:
                    usage.reset()
                except Exception:
                    pass

    def is_hostile_to(self, other) -> bool:
        if other is self:
            return False
        return getattr(other, "combatant_type", None) != self.combatant_type

    def is_ally_of(self, other) -> bool:
        # Mismo tipo y objeto distinto. (TODO: reacciones sobre aliados.)
        if other is self:
            return False
        return getattr(other, "combatant_type", None) == self.combatant_type

    def to_hit(self, atk: Attack) -> int:
        if atk.attack_bonus is not None:
            return atk.attack_bonus
        return self.abilities.mod(atk.ability) + (self.proficiency if atk.proficient else 0)

    def dmg_bonus(self, atk: Attack) -> int:
        if atk.damage_bonus is not None:
            return atk.damage_bonus
        return self.abilities.mod(atk.ability)

    def saving_throw_bonus(self, ability: str) -> int:
        ab = normalize_ability(ability)
        overrides = self.save_overrides or {}
        # busca tanto clave normalizada como original.
        for key, value in overrides.items():
            try:
                if normalize_ability(key) == ab:
                    return int(value)
            except Exception:
                if str(key).strip().lower() == ab:
                    return int(value)
        if ab in overrides:
            return int(overrides[ab])
        bonus = self.abilities.mod(ab)
        if ab in (self.save_proficiencies or set()):
            bonus += int(self.proficiency or 0)
        return int(bonus)


@dataclass
class PlayerCharacter(Combatant):
    def __post_init__(self):
        object.__setattr__(self, "combatant_type", CombatantType.PLAYER)
        # TODO: las competencias de salvación vendrán de la clase.
        super().__post_init__()


@dataclass
class Monster(Combatant):
    def __post_init__(self):
        object.__setattr__(self, "combatant_type", CombatantType.NPC)
        super().__post_init__()

"""Personajes (PJ) y monstruos (NPC)."""
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

from ..core.abilities import Abilities, normalize_ability
from .attack import Attack
from ..core.enums import DamageType, parse_damage_type
from ..core.targeting import valid_targets  # noqa: F401  (reexport)

from ..core.combat_state import CombatState
from ..rules.conditions import Condition, ConditionTracker

if TYPE_CHECKING:  # pragma: no cover - solo para tipado
    from ..rules.legendary import LegendaryState

# ``valid_targets`` se reexporta aquí (API pública histórica): la fuente
# única de verdad vive en :mod:`dnd_sim.core.targeting`.
__all__ = [
    "Combatant",
    "CombatantType",
    "Monster",
    "PlayerCharacter",
    "valid_targets",
]


class CombatantType(str, Enum):
    PLAYER = "PLAYER"
    NPC = "NPC"


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
    # Estado de condiciones (no forma parte del constructor público).
    conditions: ConditionTracker = field(init=False, default_factory=ConditionTracker)
    # Estado de combate (posición/cobertura; no forma parte del constructor).
    state: CombatState = field(init=False, default_factory=CombatState)
    # Ventaja/desventaja en pruebas de característica (por característica).
    checks_with_advantage: set[str] = field(default_factory=set)
    checks_with_disadvantage: set[str] = field(default_factory=set)
    # Estado legendario (acciones legendarias y resistencia legendaria).
    # Lo rellena ``load_monster`` desde la API.
    legendary: "LegendaryState | None" = None
    # Rasgos especiales pasivos de la ficha (p. ej. Blood Frenzy del
    # sahuagin). También los rellena ``load_monster`` (trait_parser).
    traits: list[Any] = field(default_factory=list)
    hp: int = field(init=False)
    initiative: int = field(init=False, default=0)
    # Estado de muerte explícito. Lo pone el motor (al recibir un daño igual
    # o mayor que los PV restantes, o al morir en su propio turno) y solo lo
    # limpia ``reset()``: así quien queda a 0 PV no «revive» a mitad de un
    # combate reutilizado y el combate se da por terminado al instante.
    dead: bool = field(init=False, default=False)

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
        from .actions import ActionType, AttackAction, WeaponAttackAction

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
        # El estado de muerte manda: quien queda marcado ya no vuelve.
        if self.dead:
            return False
        if self.hp > 0:
            return True
        # A 0 PV la criatura muere, salvo que un rasgo pueda salvarla hasta
        # su próximo turno de inicio (Regeneration): entonces sigue viva y
        # ese turno decide entre morir (a 0 PV no se regenera) o seguir.
        return self._sobrevive_a_cero()

    def mark_dead(self) -> None:
        """Marca el combatiente como muerto (estado definitivo).

        Lo llaman :func:`dnd_sim.rules.damage.inflict_damage` cuando el daño
        deja a 0 PV a quien no tiene rasgo que lo salve, y los rasgos que
        mueren en su propio turno (Regeneration). ``alive`` pasa a False al
        instante, así que el combate termina en el momento en que cae el
        último de un bando (PJ o NPC).
        """
        self.dead = True

    def _sobrevive_a_cero(self) -> bool:
        """¿Un rasgo mantiene a esta criatura viva con 0 PV?"""
        traits = getattr(self, "traits", None)
        if not traits:
            return False
        from ..rules.traits import hooks
        try:
            return any(r.survives_at_zero_hp(self)
                       for r in hooks(traits, "survives_at_zero_hp"))
        except Exception:
            return False

    def reset(self) -> None:
        self.hp = self.max_hp
        # Un combate nuevo revive a todos: el estado de muerte se limpia aquí.
        self.dead = False
        # Las condiciones duran hasta el fin del combate: se limpian aquí.
        try:
            self.conditions.clear()
        except Exception:
            pass
        # Todo el mundo empieza cuerpo a cuerpo, con la reacción cargada y
        # sin enganchar a nadie.
        try:
            self.state.at_range = False
            self.state.reaction_used = False
            self.state.attached_to = None
        except Exception:
            pass
        # Los usos limitados (usos por día, recargas) viven en las acciones,
        # no en el combatiente: se reinician aquí.
        for action in getattr(self, "actions", []) or []:
            usage = getattr(action, "usage", None)
            if usage is not None:
                try:
                    usage.reset()
                except Exception:
                    pass
        # El estado legendario también se reinicia (puntos y resistencia).
        legendary = getattr(self, "legendary", None)
        if legendary is not None:
            try:
                legendary.reset()
            except Exception:
                pass
        # Los rasgos con estado propio por combate (p. ej. Regeneration,
        # que guarda el bloqueo de ácido/fuego y su propia muerte) se
        # limpian aquí: ``simulate()`` reutiliza los mismos objetos.
        from ..rules.traits import hooks
        for rasgo in hooks(getattr(self, "traits", None), "reset"):
            try:
                rasgo.reset()
            except Exception:
                pass

    @property
    def can_act(self) -> bool:
        """¿Puede actuar? (incapacitado no puede usar acciones)"""
        if not self.alive:
            return False
        try:
            return not self.conditions.has(Condition.INCAPACITATED)
        except Exception:
            return True

    @property
    def can_react(self) -> bool:
        """¿Puede reaccionar? (incapacitado no puede usar reacciones)"""
        if not self.alive:
            return False
        try:
            return not self.conditions.has(Condition.INCAPACITATED)
        except Exception:
            return True

    def is_hostile_to(self, other) -> bool:
        if other is self:
            return False
        if self.is_charmed:
            # Hechizado: los objetivos se invierten (ataca a los de su propio
            # bando). El hechizador es su aliado.
            charmer = self.charmed_by
            if charmer is not None and other is charmer:
                return False
            return getattr(other, "combatant_type", None) == self.combatant_type
        return getattr(other, "combatant_type", None) != self.combatant_type

    @property
    def is_charmed(self) -> bool:
        """¿Está hechizado (sus objetivos están invertidos)?"""
        try:
            from ..rules.conditions import Condition
            return self.conditions.has(Condition.CHARMED)
        except Exception:
            return False

    @property
    def charmed_by(self):
        """Combatiente que lo hechizó (si lo hay)."""
        try:
            from ..rules.conditions import Condition
            for instance in list(self.conditions.instances):
                if instance.condition is Condition.CHARMED:
                    return instance.source
        except Exception:
            pass
        return None

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
        self._anadir_acciones_de_rasgos()

    def _anadir_acciones_de_rasgos(self) -> None:
        """Añade las acciones que aporten los rasgos (hook ``extra_actions``).

        Se ejecuta una vez, al construir el monstruo, y vale igual para una
        ficha cargada de la API que para un monstruo montado a mano en un
        test: Superior Invisibility no viene en el campo ``actions`` de la
        ficha sino que la aporta su propio rasgo.
        """
        traits = getattr(self, "traits", None)
        if not traits:
            return
        from ..rules.traits import hooks
        for rasgo in hooks(traits, "extra_actions"):
            extra = rasgo.extra_actions(self) or []
            if extra:
                self.actions.extend(extra)

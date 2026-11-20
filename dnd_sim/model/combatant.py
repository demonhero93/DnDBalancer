"""Personajes (PJ) y monstruos (NPC)."""
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

from ..core.abilities import Abilities, normalize_ability
from ..core.proficiency import proficiency_bonus
from ..core.backgrounds import Background, normalize_tool
from ..core.races import Race
from ..core.skills import normalize_skill, skill_ability
from .attack import Attack
from ..core.enums import DamageType, parse_damage_type
from ..core.targeting import valid_targets  # noqa: F401  (reexport)

from ..core.combat_state import CombatState
from ..core.spellcasting import SpellSlots
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
    # --- Daño mágico vs no mágico ---
    # Significado de la bandera ``magical`` de ``Attack``, ``SaveDamage`` y
    # ``ConditionEffect``: «el efecto ES mágico» (hechizos, armas mágicas,
    # armas naturales con Bestial Soul). Los dos conjuntos de abajo solo
    # aplican si el daño NO es mágico; la Furia del bárbaro y las
    # resistencias incondicionales de arriba no cambian con la bandera.
    #: Resistencias que solo cuentan contra daño NO mágico.
    nonmagical_resistances: set[DamageType] = field(default_factory=set)
    #: Inmunidades que solo cuentan contra daño NO mágico.
    nonmagical_immunities: set[DamageType] = field(default_factory=set)
    # --- Salvaciones ---
    save_overrides: dict[str, int] = field(default_factory=dict)
    save_proficiencies: set[str] = field(default_factory=set)
    saves_with_advantage: set[str] = field(default_factory=set)
    saves_with_disadvantage: set[str] = field(default_factory=set)
    # Rasgo «Magic Resistance» de la ficha: ventaja en salvaciones contra
    # hechizos y otros efectos mágicos. Lo consume save_modifiers cuando la
    # salvación llega con magical=True; el loader lo fija desde
    # special_abilities. No es Trait: estado puro sin lógica propia (como
    # saves_with_advantage).
    magic_resistance: bool = False
    # --- Inmunidades a condiciones ---
    # Condiciones que el combatiente nunca puede recibir (ficha de monstruo
    # o rasgo). Chequeadas en ``rules.conditions.apply_condition`` antes de
    # crear la instancia; vacío por defecto. No es Trait: estado puro, como
    # magic_resistance.
    condition_immunities: set[Condition] = field(default_factory=set)
    # --- Nuevos campos ---
    weapons: list[Attack] = field(default_factory=list)
    # Armas dinámicas (p. ej. el arma natural del Path of the Beast mientras
    # dura la Furia): WeaponAttackAction las ofrece **junto** a ``weapons``
    # sin mutar esta lista, que es la de la ficha. Las retira el rasgo que
    # las añadió (al terminar la Furia y en su ``reset``).
    dynamic_weapons: list[Attack] = field(default_factory=list)
    extra_attacks: int = 0
    attacks_with_advantage: bool = False
    attacks_with_disadvantage: bool = False
    grants_advantage_to_attackers: bool = False
    grants_disadvantage_to_attackers: bool = False
    # Feral Instinct (bárbaro nivel 7): la iniciativa se tira con ventaja.
    initiative_with_advantage: bool = False
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
    # Competencias en pruebas de característica (por característica).
    # En 5e solo un PJ puede tenerlas: salen de clase/antecedente/rasgos.
    check_proficiencies: set[str] = field(default_factory=set)
    # Habilidades competentes y expertise (doble competencia, p. ej. Pícaro).
    skill_proficiencies: set[str] = field(default_factory=set)
    skill_expertise: set[str] = field(default_factory=set)
    # Herramientas competentes (herramientas de ladrón, juegos...): las
    # aporta el transfondo.
    tool_proficiencies: set[str] = field(default_factory=set)
    # Totales de ficha de monstruo (igual que ``save_overrides``): mandan
    # sobre el cálculo de mod + competencia.
    skill_overrides: dict[str, int] = field(default_factory=dict)
    # Estado legendario (acciones legendarias y resistencia legendaria).
    # Lo rellena ``load_monster`` desde la API.
    legendary: "LegendaryState | None" = None
    # Rasgos especiales pasivos de la ficha (p. ej. Blood Frenzy del
    # sahuagin). También los rellena ``load_monster`` (trait_parser).
    traits: list[Any] = field(default_factory=list)
    hp: int = field(init=False)
    #: PV temporales (5e): absorben el daño antes que los PV normales.
    temp_hp: int = 0
    #: Tamaño (PHB): cadena de la ficha en minúsculas ("medium" por
    #: defecto). Lo rellena ``load_monster``; lo consume
    #: ``dnd_sim.rules.utility`` (Agarrar: un tamaño mayor como máximo).
    size: str = "medium"
    #: Tamaño original de la ficha: lo restaura ``reset()`` (y la Furia
    #: del Path of the Giant) tras un Giant Stature/Demiurgic Colossus.
    size_base: str = ""
    initiative: int = field(init=False, default=0)
    # Estado de muerte explícito. Lo pone el motor (al recibir un daño igual
    # o mayor que los PV restantes, o al morir en su propio turno) y solo lo
    # limpia ``reset()``: así quien queda a 0 PV no «revive» a mitad de un
    # combate reutilizado y el combate se da por terminado al instante.
    dead: bool = field(init=False, default=False)
    # Strength Before Death (Samurai, A6): quien esperando su turno extra
    # con 0 PV sigue «en pie» (``alive`` lo consulta antes de
    # ``_sobrevive_a_cero``). Lo pone el walker de daño al reducirlo a 0
    # con el rasgo, lo limpia el procesado de la cola al final de cada
    # turno (cura o muerte) y ``reset()``.
    en_pie_pendiente: bool = field(init=False, default=False)
    # PV mínimos alcanzados en el combate en curso (riesgo real de
    # ``engine.stats``): lo reinician ``__post_init__`` y ``reset()``,
    # y lo baja solo el daño en ``rules.damage.inflict_damage``.
    min_hp_reached: int = field(init=False, default=0)
    # Espacios de conjuro de un PJ lanzador (None = sin lanzamiento:
    # cero cambio para todo lo existente). Lo rellena
    # ``rules.spells.aplicar_lanzamiento``; ``reset()`` los restaura
    # (un combate = un día descansado, criterio ActionUsage).
    spell_slots: SpellSlots | None = None

    def __post_init__(self):
        if isinstance(self.combatant_type, str):
            self.combatant_type = CombatantType(self.combatant_type)
        self.hp = self.max_hp
        self.min_hp_reached = self.hp
        self.size = str(self.size or "medium").strip().lower() or "medium"
        self.size_base = (str(self.size_base or self.size).strip().lower()
                          or "medium")
        self.resistances = {parse_damage_type(x) for x in (self.resistances or set())}
        self.vulnerabilities = {parse_damage_type(x) for x in (self.vulnerabilities or set())}
        self.immunities = {parse_damage_type(x) for x in (self.immunities or set())}
        self.nonmagical_resistances = {
            parse_damage_type(x) for x in (self.nonmagical_resistances or set())}
        self.nonmagical_immunities = {
            parse_damage_type(x) for x in (self.nonmagical_immunities or set())}
        self.condition_immunities = {
            c if isinstance(c, Condition) else Condition(str(c).strip().lower())
            for c in (self.condition_immunities or set())}

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
        self.check_proficiencies = {
            normalize_ability(x) for x in (self.check_proficiencies or set())
        }

        # Normalización de campos de habilidades.
        raw_skills = dict(self.skill_overrides or {})
        norm_skills = {}
        for key, val in raw_skills.items():
            try:
                norm_skills[normalize_skill(key)] = int(val)
            except Exception:
                norm_skills[str(key).strip().lower()] = val
        self.skill_overrides = norm_skills
        self.skill_proficiencies = {
            normalize_skill(x) for x in (self.skill_proficiencies or set())
        }
        self.skill_expertise = {
            normalize_skill(x) for x in (self.skill_expertise or set())
        }
        self.tool_proficiencies = {
            normalize_tool(x) for x in (self.tool_proficiencies or set())
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
        # Strength Before Death (Samurai): pendiente de su turno extra
        # con 0 PV sigue en pie; sin flag, manda la salvación a cero.
        if self.en_pie_pendiente:
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
        # Concentración (5e): se pierde al morir (sin contexto no hay
        # log; la condición no sobrevive a un muerto de todas formas).
        for inst in list(getattr(self.conditions, "instances", []) or []):
            if inst.condition is Condition.CONCENTRATION:
                self.conditions.remove_instance(inst)

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
        self.min_hp_reached = self.hp
        # Un combate nuevo revive a todos: el estado de muerte se limpia aquí.
        self.dead = False
        # Strength Before Death: nadie empieza un combate pendiente.
        self.en_pie_pendiente = False
        # Los PV temporales tampoco sobreviven a un combate nuevo.
        self.temp_hp = 0
        # Espacios de conjuro: un combate = un día descansado.
        if self.spell_slots is not None:
            self.spell_slots.reset()
        # El tamaño vuelve al de la ficha (efectos como Giant Stature).
        self.size = self.size_base
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
            self.state.marked_by = None
            self.state.attacked_this_turn = False
            self.state.forced_save_this_turn = False
            self.state.dodging = False
            # Fire Rune (Rune Knight): sin marca al empezar un combate.
            self.state.fire_runa = None
            self.state.fire_runa_hasta = 0
            self.state.stone_de = None
            self.state.stone_pg = 0
            # Bulwark of Force (Psi Warrior): sin cobertura heredada al
            # empezar un combate nuevo.
            self.state.cobertura_bulwark = None
            # Marcas de maestría (Vex/Sap): un combate nuevo empieza sin ellas.
            self.state.maestria_ventaja.clear()
            self.state.maestria_desventaja.clear()
            # Marca de Enfeebling (Arcane Archer): un combate nuevo sin ella.
            self.state.enfeeble_hasta_ronda.clear()
            # Marca de Goading (Battle Master): un combate nuevo sin ella.
            self.state.goading.clear()
            # Marca de Unwavering Mark (Cavalier): sin ella en combate nuevo.
            self.state.marca_cavalier.clear()
            # Marca de Distracting (Battle Master): un combate nuevo sin ella.
            self.state.distracting.clear()
            # Turnos extra pendientes de Strength Before Death: la cola
            # vive en el SUJETO y un combate nuevo empieza vacía.
            self.state.turnos_extra_pendientes.clear()
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

    def check_bonus(self, ability: str) -> int:
        """Bono total de una prueba de característica.

        Suma el modificador de la característica y, si hay competencia
        declarada en ``check_proficiencies``, el bono de competencia.
        """
        ab = normalize_ability(ability)
        bonus = self.abilities.mod(ab)
        if ab in (self.check_proficiencies or set()):
            bonus += int(self.proficiency or 0)
        return int(bonus)

    def skill_bonus(self, skill: str, ability: str | None = None) -> int:
        """Bono total de una prueba de habilidad (Atletismo, Sigilo...).

        Un total de ficha en ``skill_overrides`` manda (monstruos); si no,
        modificador de la característica asociada + competencia, doble con
        expertise. ``ability`` permite tirar la habilidad con otra
        característica (Primal Knowledge: Sigilo como FUE con Furia).
        """
        name = normalize_skill(skill)
        overrides = self.skill_overrides or {}
        if name in overrides:
            return int(overrides[name])
        ab = normalize_ability(ability) if ability is not None else skill_ability(name)
        bonus = self.abilities.mod(ab)
        if name in (self.skill_expertise or set()):
            bonus += 2 * int(self.proficiency or 0)
        elif name in (self.skill_proficiencies or set()):
            bonus += int(self.proficiency or 0)
        return int(bonus)


@dataclass
class PlayerCharacter(Combatant):
    # Nivel total del PJ. Si se indica, manda sobre el campo ``proficiency``
    # (que se recalcula con la tabla PHB); los monstruos no lo usan.
    level: int | None = None
    # Transfondo elegido (si lo hay). Sus competencias se añaden con
    # ``apply_background``.
    background: Background | None = None
    # Raza elegida (si la hay). Sus competencias se añaden con
    # ``apply_race``; los hechizos que aporta quedan en ``race.spells``
    # (pendientes de conectar con el sistema de hechizos). Los bonos de
    # carácter de la raza se asumen ya aplicados.
    race: Race | None = None

    def __post_init__(self):
        object.__setattr__(self, "combatant_type", CombatantType.PLAYER)
        if self.level is not None:
            self.proficiency = proficiency_bonus(self.level)
        # TODO: las competencias de salvación vendrán de la clase.
        super().__post_init__()

    def apply_background(self, background: Background) -> None:
        """Añade al personaje las competencias de su transfondo.

        Skills y herramientas se fusionan con las que ya tenga (sin
        duplicar) y se guardan normalizados; el transfondo queda registrado
        en ``self.background``.
        """
        self.skill_proficiencies |= {
            normalize_skill(x) for x in background.skill_proficiencies
        }
        self.tool_proficiencies |= {
            normalize_tool(x) for x in background.tool_proficiencies
        }
        self.background = background

    def apply_race(self, race: Race, skill: str | None = None) -> None:
        """Añade al personaje las competencias de su raza.

        Fusiona las habilidades fijas con las que ya tenga. Si la raza da
        habilidades a elegir, se toma ``skill`` (validada contra la lista)
        o, si no se indica, la primera de la lista. Los hechizos quedan
        registrados en ``self.race.spells``; la raza no toca salvaciones
        ni características.
        """
        self.skill_proficiencies |= {
            normalize_skill(x) for x in race.skill_proficiencies
        }
        if skill is not None:
            choice = normalize_skill(skill)
            valid = {
                normalize_skill(x)
                for x in (*race.skill_proficiencies, *race.skill_choices)
            }
            if choice not in valid:
                raise ValueError(
                    f"{choice!r} no es una habilidad de {race.name!r}: "
                    f"opciones {sorted(valid)}."
                )
            self.skill_proficiencies.add(choice)
        elif race.skill_choices:
            self.skill_proficiencies.add(normalize_skill(race.skill_choices[0]))
        self.race = race


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

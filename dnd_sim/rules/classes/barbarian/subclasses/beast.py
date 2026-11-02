"""Path of the Beast (Tasha's Cauldron of Everything, 2014).

Subclase del bárbaro **no incluida en el PHB 2024**: el texto es el de
Tasha's, ejecutado sobre las reglas base 2024 del proyecto (Furia 2024,
Ataque Extra, Brutal Strike...). Los datos no vienen de la API (no está
en el SRD), igual que Battlerager y Ancestral Guardian: las reglas viven
aquí.

Decisiones de simulación:

- **Aleatoriedad, nada de estrategia**: al entrar en Furia la forma se
  elige con ``pick`` uniforme entre las 3 (``ExtendRageAction`` no vuelve
  a elegir); el efecto de la Fiereza infecciosa, con ``pick`` entre los
  disponibles; los aliados de Call the Hunt, con ``sample`` sin
  reemplazo. Los usos se gastan siempre que se puede. Orden de RNG:
  forma -> aliados de Call the Hunt -> lo demás.
- **Sin posiciones**: se asume que todos los aliados están a 9 m y que un
  atacante cuerpo a cuerpo está a menos de 3 m (la cola no reacciona ante
  ataques a distancia). # TODO: posición y distancia reales (nadar,
  trepar, saltar, alcance de la cola, mano libre de las garras).
- **Arma natural dinámica**: entra en ``Combatant.dynamic_weapons``
  mientras dura la Furia (sin mutar la lista ``weapons`` de la ficha) y
  la retira ``on_rage_end``/``reset``. Es arma simple cuerpo a cuerpo con
  competencia y mod de FUE, así que el daño de Furia, Brutal Strike y
  demases la reciben **por el mismo camino genérico** que cualquier arma.
- **Mordisco**: cura con el patrón de ``HealAction`` (sin pasar del
  máximo), solo con daño final > 0 y estrictamente por debajo de la
  mitad de los PG máximos, una vez por turno propio.
- **Garras**: el ataque extra se dispara en ``after_attack_roll`` solo
  cuando la acción es la de Atacar (``ctx.in_attack_action``), una vez
  por turno propio, con ``pick`` de objetivo y sin recursión (se marca
  antes de atacar). No cuenta contra el Ataque Extra.
- **Cola**: reutiliza la reacción defensiva de Parry
  (``defensive_ac_bonus``): tira 1d8 y gasta la reacción solo si con ese
  dado el ataque deja de entrar.
- **Fiereza infecciosa**: salvación de SAB por ``saving_throw`` (la
  Resistencia legendaria aplica); usa por impacto con arma natural en
  Furia, con o sin fallo. El daño psíquico pasa por
  ``apply_damage_modifiers`` e ``inflict_damage`` (sin duplicarse en
  crítico). La rama de contraataque usa el parámetro explícito
  ``allow_friendly`` de ``attack_roll`` **solo** para esa llamada.
- **Call the Hunt**: PV temporales con la regla de no apilar (si hay más
  ya, no se suman) que duran lo que la Furia; el +1d6 del aliado es un
  rasgo temporal (``CallTheHuntBonus``) que se añade sin apilarse y se
  retira en ``on_rage_end``/``reset`` sin iterar listas ajenas.
- **Alma bestial (6)**: las armas naturales (incluidas las dinámicas de
  la Furia, que son las mismas instancias) se construyen con
  ``Attack.magical=True`` desde el nivel 6, así superan las
  resistencias/inmunidades a daño no mágico. Nadar/trepar/saltar
  no se modelan (# TODO).
- **Weapon Mastery** no se aplica a las armas naturales (no tienen
  propiedad de maestría): # TODO.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .....core.classes import MAX_LEVEL, MIN_LEVEL, extra_attacks_for
from .....core.dice import roll_dice
from .....core.enums import AttackRange, parse_damage_type
from .....core.log import log_line as _log_line
from .....core.randomness import pick, sample
from .....core.targeting import valid_targets
from .....model.actions import AttackAction, MultiattackAction, WeaponAttackAction
from .....model.attack import Attack
from ....damage import apply_damage_modifiers, inflict_damage
from ....saves import saving_throw
from ....traits.base import Trait
from ....traits.defense import _ve_al_atacante
from ..features import BarbarianFeatures, _rasgo

#: Fracción de PG por debajo de la cual el Mordisco cura (estrictamente).
BITE_HEAL_BELOW_FRACTION = 0.5

#: PV temporales que aporta cada aliado elegido en Call the Hunt.
CALL_THE_HUNT_TEMP_HP = 5

#: Dados del daño psíquico de la Fiereza infecciosa.
INFECTIOUS_FURY_DICE = "2d12"


class FormOfTheBeast(Enum):
    """Las tres formas de la Forma de la Bestia (3)."""

    BITE = "bite"      # Mordisco
    CLAWS = "claws"    # Garras
    TAIL = "tail"      # Cola


@dataclass(frozen=True)
class NaturalWeapon:
    """Descripción de un arma natural (nombre, dados y tipo de daño)."""

    name: str
    damage: str
    damage_type: str = "piercing"
    ability: str = "str"

    def to_attack(self, magical: bool = False) -> Attack:
        """Construye la instancia de :class:`Attack` de esta arma.

        ``magical`` la marca como arma mágica (Alma bestial, nivel 6).
        """
        return Attack(self.name, self.damage, ability=self.ability,
                      damage_type=parse_damage_type(self.damage_type),
                      magical=magical)


#: Armas de cada forma (el trait crea instancias propias por personaje).
NATURAL_WEAPONS: dict[FormOfTheBeast, NaturalWeapon] = {
    FormOfTheBeast.BITE: NaturalWeapon("Mordisco", "1d8", "piercing"),
    FormOfTheBeast.CLAWS: NaturalWeapon("Garras", "1d6", "slashing"),
    FormOfTheBeast.TAIL: NaturalWeapon("Cola", "1d8", "piercing"),
}

#: Formas de la Bestia en el orden de elección (para el ``pick`` uniforme).
FORMS: tuple[FormOfTheBeast, ...] = tuple(FormOfTheBeast)


@dataclass
class BeastFeatures(Trait):
    """Rasgos del Camino de la Bestia (3/6/10/14) con su estado por combate."""

    level: int = MIN_LEVEL
    form: FormOfTheBeast | None = None
    # Instancias propias del arma natural de cada forma (identidad para
    # reconocer «es un arma natural» en los hooks).
    natural_attacks: dict = field(default_factory=dict)
    bite_heal_round: int = -1
    claws_extra_round: int = -1
    infectious_uses_max: int = 0
    infectious_uses: int = 0
    hunt_uses_max: int = 0
    hunt_uses: int = 0
    hunt_allies: list = field(default_factory=list)
    hunt_temp_granted: bool = False
    owner: Any = field(default=None, repr=False, compare=False)

    # --- Utilidades ---------------------------------------------------------
    def _barb(self) -> BarbarianFeatures | None:
        if self.owner is None:
            return None
        return _rasgo(self.owner)

    def _furiosa(self) -> bool:
        barb = self._barb()
        return bool(barb is not None and barb.rage_active)

    def _es_natural(self, atk: Any) -> bool:
        """¿``atk`` es una de **mis** instancias de arma natural?"""
        if atk is None:
            return False
        return any(atk is arma for arma in self.natural_attacks.values())

    @staticmethod
    def _round(ctx: Any) -> int:
        try:
            return int(getattr(ctx, "round", 0) or 0)
        except Exception:
            return 0

    @staticmethod
    def _aliados_de(ctx: Any, criatura: Any) -> list:
        """Vivos del mismo bando que ``criatura`` (sin ella misma)."""
        combatientes = getattr(ctx, "combatants", None) or []
        aliados = []
        for c in combatientes:
            if c is criatura or not getattr(c, "alive", False):
                continue
            try:
                if not criatura.is_hostile_to(c):
                    aliados.append(c)
            except Exception:
                continue
        return aliados

    # --- 3: Forma de la Bestia ---------------------------------------------
    def on_rage_start(self, actor: Any, ctx: Any = None) -> None:
        """Elige la forma (pick uniforme) y, en 14, los aliados de la caza.

        Orden de RNG documentado: forma -> aliados de Call the Hunt ->
        lo demás. Sin RNG (``ctx`` sin generador) no se elige nada.
        """
        if self.level < 3:
            return
        rng = getattr(ctx, "rng", None) if ctx is not None else None
        if rng is None:
            return
        forma = pick(rng, list(FORMS))
        self.form = forma
        arma = self.natural_attacks.get(forma)
        owner = self.owner or actor
        if arma is not None:
            # Sin mutar ``weapons``: el conjunto elegible pasa por
            # ``dynamic_weapons`` y lo retira ``on_rage_end``/``reset``.
            owner.dynamic_weapons = [arma]
            _log_line(ctx, f"{owner.name} adquiere la forma "
                           f"({forma.name.lower()}): {arma.name}")
        if self.level >= 14:
            self._elegir_aliados_de_caza(ctx, rng)

    def _elegir_aliados_de_caza(self, ctx: Any, rng: Any) -> None:
        """Call the Hunt (14): hasta mod CON (mínimo 1) aliados a 9 m."""
        if self.hunt_uses <= 0:
            return
        owner = self.owner
        if owner is None:
            return
        combatientes = getattr(ctx, "combatants", None) or []
        # Solo PJs vivos distintos del bárbaro y voluntarios (los PJs lo
        # son todos); a 9 m: sin posiciones se asume a todos a la vista.
        # TODO: distancia/visión reales.
        candidatos = [
            c for c in combatientes
            if c is not owner and getattr(c, "alive", False)
            and getattr(c, "combatant_type", None) == "PLAYER"
            and not owner.is_hostile_to(c)
        ]
        if not candidatos:
            return  # sin aliados NO se gasta el uso
        con = owner.abilities.mod("con")
        k = min(max(1, con), len(candidatos))
        if k <= 0:
            return
        elegidos = sample(rng, candidatos, k)
        self.hunt_uses -= 1
        self.hunt_allies = list(elegidos)
        # PV temporales con la regla de no apilar: si ya hay más, se
        # quedan los que había; en otro caso los nuevos sustituyen.
        owner.temp_hp = max(int(getattr(owner, "temp_hp", 0) or 0),
                            CALL_THE_HUNT_TEMP_HP * k)
        self.hunt_temp_granted = True
        for aliado in elegidos:
            self._poner_bonus_de_caza(aliado)
        _log_line(ctx, f"{owner.name} convoca a {k} aliado(s) "
                       f"(Call the Hunt): {CALL_THE_HUNT_TEMP_HP * k} PV temporales")

    def _poner_bonus_de_caza(self, aliado: Any) -> None:
        """Añade el rasgo temporal del +1d6 sin apilarse consigo mismo."""
        for trait in getattr(aliado, "traits", None) or []:
            if isinstance(trait, CallTheHuntBonus) and trait.beast is self:
                return  # ya lo tiene: no se apila
        bonus = CallTheHuntBonus(name="Call the Hunt", beast=self)
        aliado.traits = list(getattr(aliado, "traits", None) or []) + [bonus]

    def _quitar_bonus_de_caza(self) -> None:
        """Retira ``CallTheHuntBonus`` de los aliados (sin iterar mientras
        se despachan hooks: ``hooks()`` copia la lista en cada llamada y
        aquí solo tocamos la lista del aliado, nunca en medio de la suya)."""
        for aliado in self.hunt_allies:
            traits = list(getattr(aliado, "traits", None) or [])
            restantes = [t for t in traits
                         if not (isinstance(t, CallTheHuntBonus)
                                 and t.beast is self)]
            if len(restantes) != len(traits):
                aliado.traits = restantes
        self.hunt_allies = []

    # --- 6: Alma bestial ----------------------------------------------------
    # (ver docstring del módulo: armas naturales mágicas desde el nivel 6,
    # resueltas al construir ``natural_attacks`` en ``apply_beast``)

    # --- 10: Fiereza infecciosa + 3: Mordisco -------------------------------
    def after_dealing_hit(self, target: Any, attacker: Any, rango: Any,
                          ctx: Any = None, atk: Any = None,
                          damage: int | None = None) -> None:
        if self.level < 3 or not self._es_natural(atk):
            return
        owner = self.owner or attacker
        if attacker is not owner or not self._furiosa():
            return
        if ctx is None:
            return
        round_ = self._round(ctx)
        # Mordisco (3): una vez por turno, daño > 0 y PG estrictamente
        # por debajo de la mitad al impactar.
        if self.form is FormOfTheBeast.BITE and damage and damage > 0:
            if (int(owner.hp) * 2 < int(owner.max_hp)
                    and round_ != self.bite_heal_round):
                curar = int(getattr(owner, "proficiency", 0) or 0)
                if curar > 0:
                    self.bite_heal_round = round_
                    antes = int(owner.hp)
                    # Patrón de HealAction: nunca por encima del máximo.
                    owner.hp = min(int(owner.max_hp), antes + curar)
                    _log_line(ctx, f"{owner.name} recupera {owner.hp - antes} "
                                   f"PV (Mordisco)")
        # Fiereza infecciosa (10): impacto con arma natural en Furia.
        if self.level >= 10 and self.infectious_uses > 0:
            self._fiereza_infecciosa(target, owner, ctx)

    def _fiereza_infecciosa(self, target: Any, owner: Any, ctx: Any) -> None:
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return
        dc = 8 + owner.abilities.mod("con") + int(getattr(owner, "proficiency", 0) or 0)
        sr = saving_throw(target, "wis", dc, rng)
        # Un uso por impacto con arma natural, con o sin fallo.
        self.infectious_uses -= 1
        if sr.success:
            return
        efectos = ["dano"]
        if self._puede_contraatacar(target, ctx):
            efectos.append("reaccion")
        eleccion = pick(rng, efectos)
        if eleccion == "reaccion":
            self._contraataque_de_victima(target, ctx, rng)
            return
        # (a) 2d12 psíquicos por la vía estándar de daño (sin duplicarse
        # en crítico: la tirada no mira el golpe).
        cantidad = roll_dice(INFECTIOUS_FURY_DICE, rng)
        psiquico = parse_damage_type("psychic")
        aplicado = apply_damage_modifiers(cantidad, psiquico, target)
        inflict_damage(target, aplicado, psiquico, source=owner, ctx=ctx, rng=rng)
        _log_line(ctx, f"{getattr(target, 'name', target)} falla la salvación "
                       f"de SAB (CD {dc}) y recibe {aplicado} de daño psíquico "
                       f"(Fiereza infecciosa)")

    def _puede_contraatacar(self, target: Any, ctx: Any) -> bool:
        """¿Está la rama (b) disponible? (reacción + aliados + arma melee)"""
        if target is None or ctx is None:
            return False
        if not getattr(target, "can_act", True):
            return False
        estado = getattr(target, "state", None)
        if estado is not None and getattr(estado, "reaction_used", False):
            return False
        if not self._aliados_de(ctx, target):
            return False
        return bool(self._armas_melee_de(target))

    def _armas_melee_de(self, criatura: Any) -> list:
        ataques = list(getattr(criatura, "attacks", None) or [])
        if not ataques:
            ataques = list(getattr(criatura, "weapons", None) or [])
        return [
            a for a in ataques
            if getattr(a, "range_type", AttackRange.MELEE) is not AttackRange.RANGED
        ]

    def _contraataque_de_victima(self, target: Any, ctx: Any, rng: Any) -> None:
        """Rama (b): la víctima usa su reacción contra un aliado suyo.

        Reutiliza ``attack_roll`` con ``allow_friendly=True``, que salta la
        salvaguarda de fuego amigo **solo** en esta llamada.
        """
        aliados = self._aliados_de(ctx, target)
        armas = self._armas_melee_de(target)
        if not aliados or not armas:
            return
        elegido = pick(rng, aliados)
        arma = pick(rng, armas)
        estado = getattr(target, "state", None)
        if estado is not None:
            estado.reaction_used = True
        _log_line(ctx, f"{getattr(target, 'name', target)} usa su reacción "
                       f"para contraatacar (Fiereza infecciosa)")
        # Import perezoso: rules no debe importar engine a nivel de módulo.
        from .....engine.combat import attack_roll
        # Copia superficial: marca la llamada como reacción (Ataque
        # Temerario no decide ni recibe ventaja fuera de su turno).
        r_ctx = copy.copy(ctx)
        r_ctx.is_reaction = True
        attack_roll(target, elegido, arma, rng,
                    log=getattr(ctx, "log", None), ctx=r_ctx,
                    allow_friendly=True)

    # --- 3: Cola ------------------------------------------------------------
    def defensive_ac_bonus(self, target: Any, attacker: Any, rango: Any,
                           total: int | None = None, ca: int | None = None,
                           ctx: Any = None, rng: Any = None) -> int:
        """Cola (3): reacción estilo Parry, +1d8 de CA contra el golpe."""
        if self.level < 3 or self.form is not FormOfTheBeast.TAIL:
            return 0
        owner = self.owner or target
        if target is not owner:
            return 0  # el hook corre en los rasgos del defensor
        if not self._furiosa():
            return 0
        # Sin posiciones: un ataque cuerpo a cuerpo se asume a <3 m; la
        # cola no reacciona ante ataques a distancia. # TODO distancia.
        if rango is not AttackRange.MELEE:
            return 0
        if not _ve_al_atacante(attacker):
            return 0  # «a creature you can see»
        if not getattr(target, "can_act", True):
            return 0  # incapacitado no reacciona
        estado = getattr(target, "state", None)
        if estado is not None and getattr(estado, "reaction_used", False):
            return 0
        if rng is None or total is None or ca is None:
            return 0
        if ca + 8 <= total:
            return 0  # ni con el máximo del dado el golpe falla: en vano
        dado = roll_dice("1d8", rng)
        if ca + dado <= total:
            return 0  # no evita el golpe: la reacción no se gasta (estilo Parry)
        if estado is not None:
            estado.reaction_used = True
        _log_line(ctx, f"{getattr(target, 'name', target)} usa su cola: "
                       f"+{dado} CA (el ataque no llega)")
        return int(dado)

    # --- 3: Garras ----------------------------------------------------------
    def after_attack_roll(self, attacker: Any, target: Any, atk: Any,
                          hit: bool, ctx: Any = None,
                          rng: Any = None) -> None:
        """Garras (3): un ataque de garras extra dentro de la acción de Atacar.

        Se dispara acierte o falle la tirada («when you attack with them»),
        una vez por turno propio y solo si la acción es la de Atacar
        (``ctx.in_attack_action``). Se marca **antes** de atacar para que
        el ataque extra no dispare otro (sin recursión).
        """
        if self.level < 3 or self.form is not FormOfTheBeast.CLAWS:
            return
        owner = self.owner or attacker
        if attacker is not owner or not self._es_natural(atk):
            return
        if not self._furiosa() or ctx is None or rng is None:
            return
        if not getattr(ctx, "in_attack_action", False):
            return  # solo con la acción de Atacar (no bonus ni adicional)
        round_ = self._round(ctx)
        if round_ == self.claws_extra_round:
            return  # ya hubo un ataque de garras extra en este turno
        self.claws_extra_round = round_
        arma = self.natural_attacks.get(FormOfTheBeast.CLAWS) or atk
        equipos = {getattr(c, "team", None) for c in
                   (getattr(ctx, "combatants", None) or [])
                   if getattr(c, "alive", False)}
        if len(equipos) <= 1:
            return  # combate decidido
        enemigos = list(valid_targets(owner, ctx=ctx, atk=arma))
        if not enemigos:
            return
        objetivo = pick(rng, enemigos)
        # Import perezoso: rules no debe importar engine a nivel de módulo.
        from .....engine.combat import attack_roll
        attack_roll(owner, objetivo, arma, rng,
                    log=getattr(ctx, "log", None), ctx=ctx)

    # --- Fin de la Furia ----------------------------------------------------
    def on_rage_end(self, actor: Any, ctx: Any = None) -> None:
        """Retira la forma, el arma natural, los aliados y sus bonuses."""
        owner = self.owner or actor
        tenia_forma = self.form is not None
        self.form = None
        try:
            owner.dynamic_weapons = []
        except Exception:
            pass
        self._quitar_bonus_de_caza()
        if self.hunt_temp_granted:
            try:
                owner.temp_hp = 0  # los PV de Call the Hunt duran lo que la Furia
            except Exception:
                pass
            self.hunt_temp_granted = False
        if tenia_forma:
            _log_line(ctx, f"{getattr(owner, 'name', owner)}: "
                           f"la forma de la Bestia termina")

    # --- Reinicio -----------------------------------------------------------
    def reset(self) -> None:
        self.form = None
        self.bite_heal_round = -1
        self.claws_extra_round = -1
        self.infectious_uses = self.infectious_uses_max
        self.hunt_uses = self.hunt_uses_max
        self._quitar_bonus_de_caza()
        self.hunt_temp_granted = False
        owner = self.owner
        if owner is not None:
            try:
                owner.dynamic_weapons = []
            except Exception:
                pass


@dataclass
class CallTheHuntBonus(Trait):
    """+1d6 al daño del aliado mientras la Furia del bárbaro dura (14)."""

    beast: Any = None
    last_round: int = -1

    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            crit: bool = False, ctx: Any = None,
                            rng: Any = None, atk: Any = None) -> int:
        if self.beast is None or ctx is None or rng is None:
            return 0
        if not self.beast._furiosa():
            return 0  # la Furia terminó: el rasgo ya debió retirarse
        round_ = int(getattr(ctx, "round", 0) or 0)
        if round_ == self.last_round:
            return 0  # una vez por turno propio del aliado
        self.last_round = round_
        return int(roll_dice("1d6", rng, crit=crit))


def _habilitar_armas_naturales(pj: Any, lvl: int) -> None:
    """Convierte al PJ a la ruta de ``WeaponAttackAction`` si hacía falta.

    La Forma de la Bestia necesita que **cada** golpe elija arma al azar
    entre todas (ficha + natural). Un PJ sin ``weapons`` (Multiattack o
    ataques sueltos) pasa a tener ``weapons`` con sus propios ataques y la
    acción «Atacar»; la lista de ficha no se muta.
    """
    if getattr(pj, "weapons", None):
        return  # ya elige arma por golpe
    ataques = [a for a in (getattr(pj, "attacks", None) or [])
               if not getattr(a, "only_in_multiattack", False)] or list(
                   getattr(pj, "attacks", None) or [])
    if not ataques:
        return
    sustituye = any(isinstance(a, (AttackAction, MultiattackAction))
                    for a in (getattr(pj, "actions", None) or []))
    if not sustituye:
        return
    pj.weapons = list(ataques)
    pj.actions = [a for a in pj.actions
                  if not isinstance(a, (AttackAction, MultiattackAction))]
    if not any(isinstance(a, WeaponAttackAction) for a in pj.actions):
        pj.actions.append(WeaponAttackAction())
    golpes = extra_attacks_for(lvl)
    pj.extra_attacks = max(int(getattr(pj, "extra_attacks", 0) or 0),
                           golpes - 1)


def apply_beast(pj: Any, level: int | None = None) -> BeastFeatures:
    """Aplica el Camino de la Bestia a ``pj`` (bárbaro ya aplicado).

    - Exige :class:`BarbarianFeatures` (ValueError si no).
    - Crea las instancias de las 3 armas naturales y convierte la ruta de
      ataque si el PJ no tenía ``weapons``.
    - Usos por día de Fiereza infecciosa y Call the Hunt = bono de
      competencia; ``reset()`` los restaura.
    """
    if _rasgo(pj) is None:
        raise ValueError("Primero aplica la clase bárbaro con apply_barbarian(pj).")
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    try:
        pb = int(getattr(pj, "proficiency", 0) or 0)
    except Exception:
        pb = 0
    if pb <= 0:
        from .....core.proficiency import proficiency_bonus
        pb = proficiency_bonus(lvl)
    trait = BeastFeatures(
        name="Camino de la Bestia",
        level=lvl,
        natural_attacks={forma: arma.to_attack(magical=lvl >= 6)
                         for forma, arma in NATURAL_WEAPONS.items()},
        infectious_uses_max=pb, infectious_uses=pb,
        hunt_uses_max=pb, hunt_uses=pb,
    )
    trait.owner = pj
    _habilitar_armas_naturales(pj, lvl)
    pj.traits = list(getattr(pj, "traits", None) or []) + [trait]
    return trait


__all__ = ["BITE_HEAL_BELOW_FRACTION", "BeastFeatures", "CallTheHuntBonus",
           "FormOfTheBeast", "NATURAL_WEAPONS", "NaturalWeapon", "apply_beast"]

"""Subclase Path of the World Tree del bárbaro (PHB 2024).

Fuente: *Player's Handbook 2024* — Path of the World Tree (features en
niveles 3, 6, 10 y 14). No está ni en el SRD 2014 ni en la API, así que
la tabla va hardcodeada en :data:`WORLD_TREE_FEATURES`. Aplica sobre la
Furia del proyecto (reglas 2024). Una sola clave de registro:
``world_tree``.

Decisiones de simulación documentadas:

- **Vitality Surge** (3): al entrar en Furia el bárbaro gana PV
  temporales iguales a su nivel (``temp_hp = max(actual, nivel)``: no
  se acumulan). Automático, sin RNG. Los PV NO se revocan al terminar
  la Furia: la Furia base no los concede ni los retira (misma política
  que el aura de tundra del Storm Herald; Beast y Battlerager sí
  revocan los suyos porque su regla lo dice) (# TODO: [VERIFICAR]
  duración).
- **Life-Giving Force** (3): al inicio de cada turno propio con Furia
  activa, ``pick`` entre los aliados heridos vivos a 10 pies y la
  opción de no curar; cura ``rage_damage(level)`` d6 sin pasar del
  máximo (patrón ``HealAction``). Sin posiciones: cobertura con
  :data:`WORLD_TREE_COVERAGE_PROBABILITY` (mismo criterio que el aura
  del Storm Herald; helper copiado sin tocar ese módulo). Sin
  candidatos no hay ``pick`` ni RNG.
- **Branches of the Tree** (6): salvación de FUE, teleporte y
  congelar velocidad no modelados (sin posiciones ni movimiento): SOLO
  dato del rasgo, sin hook, sin gastar reacción y sin consumir RNG
  (# TODO).
- **Battering Roots** (10): alcance +10 pies con armas Pesadas o
  Versátiles no modelado (sin posiciones, # TODO). Al acertar en
  cuerpo a cuerpo en turno propio con un arma así, ``pick`` y
  salvación de CON (CD 8 + PB + mod de la característica del ataque);
  fallo = PRONE con el mismo ``EscapeCheck`` de Empujar. Push no tiene
  efecto sin posiciones: dato (# TODO). Si el arma ya tiene la maestría
  ``topple`` no se activa dos veces. NO exige Furia (regla de la
  sección 2; # TODO [VERIFICAR]).
- **Travel Along the Tree** (14): teleporte sin posiciones: dato, sin
  acción propia para no alterar el ``pick`` del encuentro (# TODO).
- ``extra_attack_damage`` solo lo invoca el motor en el golpe y
  ``on_turn_start`` solo en el turno propio; además se ignoran
  reacciones (``ctx.is_reaction``) y ``ctx.actor`` ajeno.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .....core.classes import MAX_LEVEL, MIN_LEVEL, rage_damage
from .....core.dice import roll_dice
from .....core.enums import AttackRange
from .....core.log import log_line as _log_line
from .....core.randomness import pick
from ....conditions import Condition, EscapeCheck, apply_condition
from ....saves import registrar_resistencia, saving_throw
from ....traits.base import Trait
from ..features import BarbarianFeatures

#: Features de subclase por nivel (PHB 2024; nombres en inglés).
WORLD_TREE_FEATURES: dict[int, tuple[str, ...]] = {
    3: ("Vitality of the Tree",),
    6: ("Branches of the Tree",),
    10: ("Battering Roots",),
    14: ("Travel Along the Tree",),
}

#: Probabilidad por criatura de estar «a 10 pies» (sin posiciones;
#: mismo criterio que STORM_AURA_COVERAGE_PROBABILITY). 1.0/0.0 no
#: consumen RNG; en medio, UNA tirada por criatura.
WORLD_TREE_COVERAGE_PROBABILITY: float = 1.0


def _de(actor: Any, clase: type) -> Any:
    """Primer rasgo de ``actor`` que sea instancia de ``clase`` (o None)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


def _en_10_pies(rng: Any) -> bool:
    """¿Está a 10 pies del bárbaro? (cobertura, sin posiciones)."""
    p = float(WORLD_TREE_COVERAGE_PROBABILITY)
    if p <= 0.0:
        return False
    if p >= 1.0:
        return True
    if rng is None:
        return True  # sin RNG: cobertura completa (no inventa tiradas)
    return rng.random() < p


def _aliados_heridos(actor: Any, ctx: Any) -> list:
    """Aliados vivos y heridos a 10 pies (sin incluir al propio actor)."""
    rng = getattr(ctx, "rng", None)
    pool: list = []
    for c in getattr(ctx, "combatants", None) or []:
        if c is actor:
            continue
        if not getattr(c, "alive", True):
            continue
        hostil = getattr(actor, "is_hostile_to", None)
        if hostil is not None and hostil(c):
            continue
        hp = int(getattr(c, "hp", 0) or 0)
        maximo = int(getattr(c, "max_hp", 0) or 0)
        if hp >= maximo:
            continue  # solo heridos
        if _en_10_pies(rng):
            pool.append(c)
    return pool


def _cd_ataque(actor: Any, atk: Any) -> int:
    """CD de Topple: 8 + competencia + mod de la característica del ataque."""
    ability = str(getattr(atk, "ability", "str") or "str")
    mod = 0
    try:
        mod = actor.abilities.mod(ability)
    except Exception:
        pass
    return 8 + int(getattr(actor, "proficiency", 0) or 0) + int(mod)


@dataclass
class WorldTreeFeatures(Trait):
    """Features de la subclase Path of the World Tree."""

    level: int = MIN_LEVEL
    owner: Any = field(default=None, repr=False, compare=False)

    @property
    def _furiosa(self) -> bool:
        barb = _de(self.owner, BarbarianFeatures)
        return bool(barb and barb.rage_active)

    # --- Vitality Surge (3): PV temporales al entrar en Furia ----------------
    def on_rage_start(self, actor: Any, ctx: Any = None) -> None:
        """Vitality Surge: PV temporales iguales al nivel (sin RNG)."""
        if self.level < 3:
            return
        actual = int(getattr(actor, "temp_hp", 0) or 0)
        actor.temp_hp = max(actual, int(self.level))  # no se acumula

    # --- Life-Giving Force (3): curación al inicio del turno -----------------
    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        """Cura ``rage_damage`` d6 a un aliado herido (decisión con pick)."""
        if self.level < 3 or actor is not self.owner or ctx is None:
            return
        if not self._furiosa:
            return
        if not getattr(actor, "alive", True):
            return
        if not getattr(actor, "can_act", True):
            return
        ctx_actor = getattr(ctx, "actor", None)
        if ctx_actor is not None and ctx_actor is not actor:
            return  # solo turno propio (defensivo: el motor ya lo garantiza)
        rng = getattr(ctx, "rng", None)
        if rng is None:
            return  # sin RNG el rasgo se abstiene
        candidatos = _aliados_heridos(actor, ctx)
        if not candidatos:
            return  # sin candidatos no hay pick ni RNG
        objetivo = pick(rng, [*candidatos, None])
        if objetivo is None:
            return  # decisión aleatoria de no curar
        dados = max(1, rage_damage(self.level))
        total = int(roll_dice(f"{dados}d6", rng))
        antes = int(getattr(objetivo, "hp", 0) or 0)
        maximo = int(getattr(objetivo, "max_hp", 0) or 0)
        objetivo.hp = min(maximo, antes + total)  # nunca por encima (HealAction)
        _log_line(
            ctx,
            f"{getattr(actor, 'name', actor)} cura a "
            f"{getattr(objetivo, 'name', objetivo)} con Fuerza "
            f"Vivificante ({total} PG)",
        )

    # --- Battering Roots (10): Topple al acertar -----------------------------
    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            crit: bool = False, ctx: Any = None,
                            rng: Any = None, atk: Any = None) -> int:
        """Topple con armas Pesadas/Versátiles (solo turno propio).

        Devuelve siempre 0 (no añade daño): el efecto es la condición.
        El motor solo invoca este hook en el golpe; sin ``rng`` el rasgo
        se abstiene.
        """
        if (self.level < 10 or attacker is not self.owner
                or target is None or atk is None
                or rango is not AttackRange.MELEE):
            return 0
        props = set(getattr(atk, "properties", None) or set())
        if not props & {"heavy", "versatile"}:
            return 0
        if str(getattr(atk, "mastery", "") or "").lower() == "topple":
            return 0  # el arma ya tiene Topple: no se activa dos veces
        if ctx is not None:
            if getattr(ctx, "is_reaction", False):
                return 0  # solo turno propio, no en reacciones
            ctx_actor = getattr(ctx, "actor", None)
            if ctx_actor is not None and ctx_actor is not attacker:
                return 0
        if rng is None:
            return 0  # sin RNG el rasgo se abstiene
        if pick(rng, ("no", "si")) == "no":
            return 0  # decisión aleatoria de usar la maestría
        sr = saving_throw(target, "con", _cd_ataque(attacker, atk), rng)
        registrar_resistencia(ctx, target, sr)
        if sr.success:
            return 0
        apply_condition(target, Condition.PRONE, ctx, source=attacker,
                        escape=EscapeCheck(abilities=("str", "dex"), dc=10,
                                           consumes_action=False))
        _log_line(ctx, f"{getattr(target, 'name', target)} cae derribado "
                       f"(Topple, Raíces Golpeadoras)")
        return 0


def apply_world_tree(pj: Any, level: int | None = None) -> WorldTreeFeatures:
    """Aplica la subclase Path of the World Tree a un PJ bárbaro.

    Exige que ``pj`` ya tenga :class:`BarbarianFeatures`
    (:func:`apply_barbarian`).
    """
    if _de(pj, BarbarianFeatures) is None:
        raise ValueError(
            "Primero aplica la clase bárbaro con apply_barbarian(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    trait = WorldTreeFeatures(name="World Tree", level=lvl)
    trait.owner = pj
    pj.traits.append(trait)
    return trait


__all__ = ["WORLD_TREE_COVERAGE_PROBABILITY", "WORLD_TREE_FEATURES",
           "WorldTreeFeatures", "apply_world_tree"]

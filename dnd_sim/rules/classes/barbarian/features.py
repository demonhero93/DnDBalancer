"""Clase bárbaro (PHB 2024), sin subclases.

Concentra en un único rasgo agregado (:class:`BarbarianFeatures`) todas
las features de clase que dependen de tiradas, más las dos acciones bonus
de Furia. :func:`apply_barbarian` monta el personaje completo (salvaciones,
Unarmored Defense, Extra Attack, iniciativa...) a partir de su nivel.

Decisiones de simulación documentadas:

- **Reckless Attack** es una decisión aleatoria por turno
  (``RECKLESS_USE_PROBABILITY``, por defecto 0.5): se decide en la
  primera tirada de ataque de FUE del turno propio, nunca en
  reacciones ni en turnos ajenos. **Brutal Strike** renuncia siempre a
  la ventaja que da.
- **Instinctive Pounce** (media velocidad), **Fast Movement**, **Weapon
  Mastery**, **Epic Boon** y los efectos de movimiento de Brutal Strike
  (push/slow) no están modelados: no hay sistema de distancia/velocidad.
- **Primal Champion** (nivel 20) no aplica +4 a PUE: los valores de
  carácter del PJ ya se dan por reflejados (mismo criterio que razas).
- **Unarmored Defense** se aplica como ``ac = max(ac, 10+DEX+CON)`` porque
  el modelo no distingue armaduras.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ....core.classes import (
    BARBARIAN_PRIMAL_SKILLS,
    BARBARIAN_SKILLS,
    MAX_LEVEL,
    MIN_LEVEL,
    extra_attacks_for,
    rage_damage,
    rage_uses,
)
from ....core.dice import roll_dice
from ....core.log import log_line as _log_line
from ....core.skills import normalize_skill
from ....model.actions import ActionType, AttackEntry, CombatAction, MultiattackAction
from ...saves import saving_throw
from ...traits.base import Trait, hooks
from ...usage import ActionUsage, UsageKind

#: Probabilidad por defecto de usar Ataque Temerario en un turno.
#: 0.5: ni siempre ni nunca, para que la simulación no asuma la política
#: óptima de la feature; configurable con ``--reckless-p`` en main.py.
RECKLESS_USE_PROBABILITY = 0.5


@dataclass
class BarbarianFeatures(Trait):
    """Features de clase del bárbaro y estado de Furia.

    Un solo rasgo agregado reutiliza el despacho de hooks existente en vez
    de una clase por feature. El estado por combate se limpia en ``reset``.
    """

    # Nivel del personaje (manda en las tablas de features).
    level: int = MIN_LEVEL
    # Furia activa y ronda (del combate) a cuyo FIN termina.
    rage_active: bool = False
    rage_expires_round: int = 0
    # Ataque temerario activo (hasta el inicio del siguiente turno).
    reckless_active: bool = False
    #: Probabilidad de decidir «sí» en el turno (CLI ``--reckless-p``).
    reckless_probability: float = RECKLESS_USE_PROBABILITY
    #: ¿Ya se decidió este turno? (una sola decisión por turno).
    reckless_decided: bool = False

    @property
    def reckless_active_this_turn(self) -> bool:
        """¿Usó Ataque Temerario en el turno actual? (alias claro para Frenzy)."""
        return self.reckless_active
    # Brutal Strike: pendiente de pagar en este golpe / ya usada este turno.
    brutal_pending: bool = False
    brutal_used_this_turn: bool = False
    # Usos de Furia Inaguantable (sube el CD +5 de cada uso siguiente).
    relentless_uses: int = 0
    # Dueño (para que ``reset`` pueda apagar los flags en el combatiente).
    owner: Any = field(default=None, repr=False, compare=False)

    # --- Utilidades --------------------------------------------------------
    @property
    def persistent_rage(self) -> bool:
        """¿Furia Persistente (nivel 15)? (10 min, sin decaer ronda a ronda)."""
        return self.level >= 15

    @staticmethod
    def _es_fue(atk: Any) -> bool:
        """¿El ataque tira con FUE? (``atk`` ausente → se asume cuerpo a cuerpo)."""
        if atk is None:
            return True
        from ....core.abilities import normalize_ability
        try:
            return normalize_ability(getattr(atk, "ability", "")) == "str"
        except Exception:
            return False

    @staticmethod
    def _condicion(actor: Any, cond: Any) -> bool:
        try:
            return bool(actor.conditions.has(cond))
        except Exception:
            return False

    def _incapacitado(self, actor: Any) -> bool:
        from ...conditions import Condition
        return self._condicion(actor, Condition.INCAPACITATED)

    def activate(self, round_: int) -> None:
        """Entra en Furia en la ronda ``round_`` (hasta el fin del siguiente)."""
        self.rage_active = True
        # Persistente (15): 10 minutos ≈ 600 rondas; el resto, hasta el
        # final de tu siguiente turno.
        self.rage_expires_round = round_ + (600 if self.persistent_rage else 1)

    # --- Ataque: Reckless Attack y Brutal Strike ---------------------------
    def _decidir_reckless(self, attacker: Any, ctx: Any, rng: Any) -> None:
        """Decisión aleatoria de Ataque Temerario (una por turno).

        0.0/1.0 no consumen RNG; con el resto, UN ``rng.random()``.
        """
        p = float(self.reckless_probability)
        nombre = getattr(attacker, "name", attacker)
        if 0.0 < p < 1.0:
            if rng is None:
                rng = getattr(ctx, "rng", None)
            if rng is None:
                return  # sin RNG el rasgo se abstiene (podrá decidir después)
        self.reckless_decided = True
        if p <= 0.0:
            self.reckless_active = False
        elif p >= 1.0:
            self.reckless_active = True
        else:
            self.reckless_active = rng.random() < p
        if self.reckless_active:
            _log_line(ctx, f"{nombre} ataca con temeridad")
        else:
            _log_line(ctx, f"{nombre} decide no atacar con temeridad")

    def modify_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                                rango: Any, ctx: Any = None,
                                rng: Any = None, atk: Any = None) -> None:
        # El pendiente de un golpe anterior (si falló) caduca aquí: cada
        # ataque evalúa lo suyo.
        self.brutal_pending = False
        if self.level < 2:  # Ataque Temerario es de nivel 2.
            return
        if not self._es_fue(atk):
            return
        if getattr(ctx, "is_reaction", False):
            # Reacciones (Retaliation, Fiereza infecciosa...): no deciden
            # ni reciben la ventaja, aunque el turno propio la tenga activa.
            return
        # Una sola decisión por turno, en la primera tirada de FUE del
        # turno propio (ctx sin actor = invocación directa de test).
        ctx_actor = getattr(ctx, "actor", None) if ctx is not None else None
        if (not self.reckless_decided
                and not (ctx is not None and ctx_actor is not None
                         and ctx_actor is not attacker)):
            self._decidir_reckless(attacker, ctx, rng)
        if not self.reckless_active:
            return
        fuente = "Ataque Temerario"
        mods.advantage_sources.append(fuente)
        try:
            attacker.grants_advantage_to_attackers = True
        except Exception:
            pass
        # Brutal Strike (9): una vez por turno, si la ventaja de este ataque
        # es SOLO la del Reckless, se renuncia a ella (sin desventaja) y el
        # golpe pasa a pagar 1d10 extra si impacta.
        if (self.level >= 9 and not self.brutal_used_this_turn
                and not mods.disadvantage_sources
                and len(mods.advantage_sources) == 1):
            mods.advantage_sources.remove(fuente)
            self.brutal_pending = True
            self.brutal_used_this_turn = True

    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            crit: bool = False, ctx: Any = None,
                            rng: Any = None, atk: Any = None) -> int:
        bonus = 0
        # Daño de Furia: ataques con FUE mientras dura (arma o cuerpo a
        # cuerpo; los ataques con bono fijo de hechizo no pasan por aquí con
        # otra característica).
        if self.rage_active and atk is not None and self._es_fue(atk):
            bonus += rage_damage(self.level)
        if self.brutal_pending:
            if rng is None:
                return bonus  # sin RNG el rasgo se abstiene (no inventa)
            dados = "2d10" if self.level >= 17 else "1d10"
            bonus += int(roll_dice(dados, rng, crit=crit))
            self.brutal_pending = False
        return bonus

    # --- Daño recibido: resistencia de Furia --------------------------------
    def modify_incoming_damage(self, target: Any, amount: int,
                               damage_type: Any, source: Any,
                               ctx: Any = None) -> int | None:
        if not self.rage_active:
            return None
        tipo = getattr(damage_type, "value", damage_type)
        if str(tipo).lower() not in {"bludgeoning", "piercing", "slashing"}:
            return None
        return max(0, int(amount) // 2)

    # --- Salvaciones: Furia (FUE), Sentido del Peligro, Indomitable Might ---
    def modify_save_modifiers(self, mods: Any, target: Any,
                              ability: str, kind: str | None = None) -> None:
        if self.rage_active and ability == "str":
            mods.advantage_sources.append("Furia")
        if (self.rage_active and ability == "dex" and self.level >= 2
                and not self._incapacitado(target)):
            mods.advantage_sources.append("Sentido del Peligro")
        if self.level >= 18 and ability == "str":
            score = int(getattr(getattr(target, "abilities", None), "str", 0) or 0)
            mods.minimum_total = score

    # --- Pruebas: Furia (FUE), Primal Knowledge, Indomitable Might ---------
    def modify_check_modifiers(self, mods: Any, target: Any, ability: str,
                               skill: str | None = None) -> None:
        eff = ability
        # Primal Knowledge (3): con Furia activa, estas habilidades se
        # tiran como FUE (y Furia da ventaja en tiradas de FUE).
        if (skill is not None and self.rage_active
                and skill in BARBARIAN_PRIMAL_SKILLS):
            mods.ability_override = "str"
            eff = "str"
        if self.rage_active and eff == "str":
            mods.advantage_sources.append("Furia")
        if self.level >= 18 and ability == "str":
            score = int(getattr(getattr(target, "abilities", None), "str", 0) or 0)
            mods.minimum_total = score

    # --- Ciclo de turno -----------------------------------------------------
    def _finalizar_furia(self, actor: Any, ctx: Any = None, *,
                         log: bool = False) -> None:
        """Termina la Furia y avisa a las subclases (hook ``on_rage_end``)."""
        self.rage_active = False
        if log:
            _log_line(ctx, f"{getattr(actor, 'name', actor)}: la Furia termina")
        # Despacho directo a los rasgos del dueño: los que no sobrescriben
        # el hook no se llaman (mismo filtro de ``hooks``).
        for rasgo in hooks(getattr(actor, "traits", None) or [], "on_rage_end"):
            rasgo.on_rage_end(actor, ctx)

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        # Reckless caduca al inicio de tu siguiente turno y con él la
        # ventaja que los demás tenían contra ti; la decisión del turno
        # anterior no vale para el nuevo.
        if self.reckless_active:
            self.reckless_active = False
            try:
                actor.grants_advantage_to_attackers = False
            except Exception:
                pass
        self.reckless_decided = False
        self.brutal_used_this_turn = False
        if not self.rage_active:
            return
        # La Furia termina antes con Incapacitado; Persistente (15) solo
        # con Unconscious (y también con armadura pesada: sin sistema).
        from ...conditions import Condition
        if self.persistent_rage:
            if self._condicion(actor, Condition.UNCONSCIOUS):
                self._finalizar_furia(actor, ctx)
        elif not actor.can_act:  # incapacitado
            self._finalizar_furia(actor, ctx)

    def on_turn_end(self, actor: Any, ctx: Any = None) -> None:
        """Fin de turno: evaluar el fin/extensión de la Furia."""
        if not self.rage_active or ctx is None:
            return
        if self.persistent_rage:
            return  # 10 minutos: no decae ronda a ronda
        round_ = int(getattr(ctx, "round", 0))
        if round_ < self.rage_expires_round:
            return  # aún no llega su fin
        state = getattr(actor, "state", None)
        extendio = bool(state is not None and (
            state.attacked_this_turn or state.forced_save_this_turn))
        if extendio:
            # Atacar u obligar a un enemigo a salvar extiende automáticamente
            # hasta el final del siguiente turno (sin gastar acción bonus).
            self.rage_expires_round = round_ + 1
        else:
            self._finalizar_furia(actor, ctx, log=True)

    # --- Supervivencia: Furia Inaguantable (11) -----------------------------
    def on_reduced_to_zero_hp(self, owner: Any, amount: int,
                              damage_type: Any = None, source: Any = None,
                              crit: bool = False, ctx: Any = None,
                              rng: Any = None) -> int | None:
        if not self.rage_active or self.level < 11:
            return None
        if rng is None:
            return None  # sin RNG, el rasgo se abstiene
        dc = 10 + 5 * self.relentless_uses
        sr = saving_throw(owner, "con", dc, rng)
        self.relentless_uses += 1
        if sr.success:
            hp = 2 * self.level
            _log_line(
                ctx,
                f"{getattr(owner, 'name', owner)} supera la salvación de FUE "
                f"(Furia Inaguantable) con CD {dc}: {hp} PV",
            )
            return hp
        _log_line(
            ctx,
            f"{getattr(owner, 'name', owner)} falla la salvación de CON "
            f"(Furia Inaguantable, CD {dc}): cae",
        )
        return None

    # --- Reinicio -----------------------------------------------------------
    def reset(self) -> None:
        self.rage_active = False
        self.rage_expires_round = 0
        self.reckless_active = False
        self.reckless_decided = False
        self.brutal_pending = False
        self.brutal_used_this_turn = False
        self.relentless_uses = 0
        owner = self.owner
        if owner is not None:
            try:
                owner.grants_advantage_to_attackers = False
            except Exception:
                pass


# --- Acciones bonus de Furia -------------------------------------------------

def _contexto(args: tuple, kwargs: dict) -> Any:
    ctx = kwargs.get("context") or kwargs.get("ctx")
    if ctx is None:
        for a in args:
            if hasattr(a, "actor") and hasattr(a, "rng"):
                return a
    return ctx


def _rasgo(actor: Any) -> BarbarianFeatures | None:
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, BarbarianFeatures):
            return trait
    return None


class RageAction(CombatAction):
    """Entrar en Furia (acción bonus, gasta un uso de la tabla por nivel)."""

    def __init__(self, uses: int = 0) -> None:
        self.name = "Entrar en Furia"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = ActionUsage(UsageKind.PER_DAY, uses_max=int(uses))

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        trait = _rasgo(actor)
        return trait is not None and not trait.rage_active

    def execute(self, context: Any) -> None:
        actor = context.actor
        trait = _rasgo(actor)
        if trait is None or trait.rage_active:
            return
        trait.activate(int(getattr(context, "round", 0)))
        _log_line(
            context,
            f"{actor.name} entra en Furia (hasta el final de su siguiente turno)",
        )
        # Las subclases se enteran de que la Furia empieza (p. ej. Path of
        # the Beast elige su forma). Los rasgos que no sobrescriben el hook
        # no se llaman, así que no hay RNG extra sin subclase.
        for rasgo in hooks(getattr(actor, "traits", None) or [], "on_rage_start"):
            rasgo.on_rage_start(actor, context)


class ExtendRageAction(CombatAction):
    """Extender la Furia con acción bonus (cuando no se atacó ni se forzó salvación).

    Si el bárbaro atacó o forzó una salvación en su turno, la Furia se
    extiende sola al fin del turno y esta acción no hace falta (ni se usa).
    """

    def __init__(self) -> None:
        self.name = "Mantener la Furia"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        trait = _rasgo(actor)
        if trait is None or not trait.rage_active or trait.persistent_rage:
            return False
        round_ = int(getattr(ctx, "round", 0))
        if round_ < trait.rage_expires_round:
            return False  # la Furia sigue vigente: aún no toca extender
        state = getattr(actor, "state", None)
        if state is not None and (state.attacked_this_turn
                                  or state.forced_save_this_turn):
            return False  # ya se extiende sola al fin del turno
        return True

    def execute(self, context: Any) -> None:
        actor = context.actor
        trait = _rasgo(actor)
        if trait is None:
            return
        round_ = int(getattr(context, "round", 0))
        trait.rage_expires_round = round_ + 1
        _log_line(
            context,
            f"{actor.name} mantiene la Furia con acción bonus "
            f"(hasta el final de la ronda {trait.rage_expires_round})",
        )


# --- Aplicación de la clase a un PJ ------------------------------------------

def apply_barbarian(pj: Any, skills: tuple[str, ...] = (),
                    level: int | None = None) -> BarbarianFeatures:
    """Aplica la clase bárbaro a ``pj`` según su nivel.

    - Salvaciones: FUE y CON.
    - ``skills``: validadas contra la lista de la clase (ValueError si no
      está; el recuento de elecciones lo decide quien llama).
    - Unarmored Defense: ``ac = max(ac, 10+DEX+CON)`` (sin sistema de
      armaduras, solo se sube la CA si sale mejor).
    - Nivel 5: la acción Atacar pasa a golpear 2 veces (Extra Attack).
    - Nivel 7: iniciativa con ventaja (Feral Instinct).
    - Añade el rasgo :class:`BarbarianFeatures` y las acciones de Furia.
    """
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))

    pj.save_proficiencies = set(pj.save_proficiencies or set()) | {"str", "con"}

    if skills:
        validas = set(BARBARIAN_SKILLS)
        nuevas = set()
        for raw in skills:
            name = normalize_skill(raw)
            if name not in validas:
                raise ValueError(
                    f"{name!r} no es una habilidad de la clase bárbaro: "
                    f"opciones {sorted(validas)}."
                )
            nuevas.add(name)
        pj.skill_proficiencies = set(pj.skill_proficiencies or set()) | nuevas

    # Unarmored Defense (1): sin armadura, CA = 10 + DEX + CON.
    try:
        pj.ac = max(int(pj.ac),
                    10 + pj.abilities.mod("dex") + pj.abilities.mod("con"))
    except Exception:
        pass

    # Extra Attack (5): dos golpes con la acción Atacar.
    golpes = extra_attacks_for(lvl)
    if golpes > 1:
        if getattr(pj, "weapons", None):
            pj.extra_attacks = max(int(pj.extra_attacks), golpes - 1)
        else:
            from ....model.actions import AttackAction
            ataques = [a for a in pj.attacks
                       if not getattr(a, "only_in_multiattack", False)] or list(pj.attacks)
            if ataques:
                entradas = [
                    AttackEntry(ataques[i % len(ataques)].name, count=1)
                    for i in range(golpes)
                ]
                multi = MultiattackAction([entradas])
                restantes = [a for a in pj.actions
                             if not isinstance(a, AttackAction)]
                restantes.append(multi)
                pj.actions = restantes

    # Feral Instinct (7): iniciativa con ventaja.
    if lvl >= 7:
        pj.initiative_with_advantage = True

    trait = BarbarianFeatures(name="Bárbaro", level=lvl)
    trait.owner = pj
    pj.traits = list(getattr(pj, "traits", None) or []) + [trait]
    pj.actions = list(pj.actions) + [
        RageAction(uses=rage_uses(lvl)),
        ExtendRageAction(),
    ]
    return trait


__all__ = ["BarbarianFeatures", "ExtendRageAction", "RageAction",
           "RECKLESS_USE_PROBABILITY", "apply_barbarian"]

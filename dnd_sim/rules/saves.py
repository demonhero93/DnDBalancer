"""Tiradas de salvación y daño con salvación (D&D 5e)."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Literal

from ..core.abilities import normalize_ability
from ..core.dice import RollMode, roll_d20, roll_dice
from .damage import apply_damage_modifiers, parse_damage_type

# ``normalize_ability`` vive en :mod:`dnd_sim.core.abilities` (capa core):
# la necesita ``combatant`` y este módulo ya no importa a ``combatant``, así
# que el ciclo saves <-> combatant no puede aparecer. Se reexporta aquí en
# ``__all__`` para no romper la API pública histórica.


# --- SaveResult / saving_throw -----------------------------------------------

@dataclass
class SaveResult:
    ability: str
    dc: int
    rolls: list[int]
    bonus: int
    total: int
    success: bool
    mode: RollMode
    # Fallo automático por condición (aturdido/paralizado/petrificado...):
    # no se tiran dados.
    auto_fail: bool = False
    # True si el fallo se convirtió en éxito con la Resistencia legendaria.
    legendary_resistance_used: bool = False


def _resolve_mode_str(value: Any) -> RollMode:
    if value is None:
        return RollMode.NORMAL
    if isinstance(value, RollMode):
        return value
    text = str(value).strip().lower()
    for mode in RollMode:
        if text == mode.value:
            return mode
    # alias
    if text in ("adv", "advantage"):
        return RollMode.ADVANTAGE
    if text in ("dis", "disadvantage"):
        return RollMode.DISADVANTAGE
    return RollMode.NORMAL


def saving_throw(target: Any, ability: str, dc: int, rng: random.Random,
                 mode: Any = None, *, kind: str | None = None) -> SaveResult:
    """Tira una salvación de D&D 5e.

    Un 20 natural NO es éxito automático y un 1 natural NO es fallo
    automático: éxito si total >= dc.

    Las condiciones pueden provocar un **fallo automático** (aturdido,
    paralizado, inconsciente o petrificado fallan siempre FUE y DES): en ese
    caso no se tiran dados y no se consume RNG.

    **Resistencia legendaria**: si la salvación falla (incluido el fallo
    automático) y el objetivo tiene usos de resistencia legendaria, se puede
    convertir el fallo en éxito (según ``resistance_probability``). El
    resultado se marca con ``legendary_resistance_used``.

    ``kind`` dice qué tipo de efecto provoca la salvación cuando quien lo
    conoce lo pasa (``"turn"`` = efecto que convierte no-muertos); lo
    reciben los hooks de rasgo vía
    :func:`dnd_sim.rules.roll_modifiers.save_modifiers`.

    # TODO: la Resistencia mágica (ventaja contra hechizos) no se modela.
    """
    ab = normalize_ability(ability)
    from .roll_modifiers import save_modifiers
    modifiers = save_modifiers(target, ab, kind)

    if modifiers.auto_fail:
        return _con_resistencia_legendaria(target, SaveResult(
            ability=ab,
            dc=int(dc),
            rolls=[],
            bonus=0,
            total=0,
            success=False,
            mode=RollMode.NORMAL,
            auto_fail=True,
        ), rng)

    if mode is None:
        mode = modifiers.mode
    else:
        mode = _resolve_mode_str(mode)
    bonus = 0
    try:
        bonus = target.saving_throw_bonus(ab)
    except Exception:
        pass
    result = roll_d20(rng, mode)
    total = result.value + int(bonus)
    success = total >= int(dc)
    return _con_resistencia_legendaria(target, SaveResult(
        ability=ab,
        dc=int(dc),
        rolls=list(result.rolls),
        bonus=int(bonus),
        total=int(total),
        success=bool(success),
        mode=mode,
    ), rng)


def _con_resistencia_legendaria(target: Any, result: SaveResult,
                                rng: random.Random) -> SaveResult:
    """Punto único donde se aplica la Resistencia legendaria.

    Import local (evita el ciclo ``saves`` -> ``legendary`` -> ``area`` ->
    ``saves``).
    """
    from .legendary import legendary_resistance
    try:
        return legendary_resistance(target, result, rng)
    except Exception:
        return result


def registrar_resistencia(ctx: Any, target: Any, result: SaveResult) -> SaveResult:
    """Log y estadísticas si la Resistencia legendaria se ha gastado.

    Se llama justo después de cada :func:`saving_throw` (el único sitio con
    contexto de combate).
    """
    from .legendary import registrar_resistencia_legendaria
    try:
        return registrar_resistencia_legendaria(ctx, target, result)
    except Exception:
        return result


# --- SaveDamage / resolve_save_damage ---------------------------------------

@dataclass
class SaveDamage:
    ability: Any
    dc: int
    damage: str
    damage_type: Any = "bludgeoning"
    on_success: Literal["none", "half"] = "none"

    def __post_init__(self) -> None:
        self.ability = normalize_ability(self.ability)
        try:
            self.damage_type = parse_damage_type(self.damage_type)
        except Exception:
            pass


def _as_combat_context(ctx: Any) -> Any:
    return ctx


from ..core.log import log_line as _log_line


def _inflict_for_save(target: Any, amount: int, damage_type: Any,
                      source: Any, ctx: Any = None) -> None:
    # Import local para evitar ciclos.
    from .damage import inflict_damage
    inflict_damage(target, amount, damage_type, source=source, ctx=ctx)


@dataclass
class SaveDamageOutcome:
    """Resultado de aplicar un daño con salvación a un objetivo."""

    save: SaveResult
    rolled_damage: int
    damage_after_save: int
    final_damage: int
    damage_type: Any = None


def _mode_tag(save: SaveResult) -> str:
    """ Sufijo de log con la tirada (ventaja/desventaja)."""
    if save.mode == RollMode.ADVANTAGE:
        return f" (ventaja: {save.rolls[0]}, {save.rolls[1]} -> {save.value - save.bonus})"
    if save.mode == RollMode.DISADVANTAGE:
        return f" (desventaja: {save.rolls[0]}, {save.rolls[1]} -> {save.value - save.bonus})"
    return ""


def _outcome_tag(save: SaveResult, on_success: str) -> str:
    """Etiqueta de log del resultado de la salvación."""
    if save.success and on_success == "half":
        return "mitad"
    if save.success and on_success == "none":
        return "ninguno"
    return "completo"


def apply_save_damage(source: Any, target: Any, effect: SaveDamage,
                       rolled_damage: int, ctx: Any, on_resolved=None) -> SaveDamageOutcome:
    """Núcleo del daño con salvación: el daño **ya está tirado**.

    Hace, en este orden: tirada de salvación propia del objetivo ->
    aplicación de ``on_success`` (mitad/nada/completo) -> resistencias,
    vulnerabilidades e inmunidades del objetivo -> ``inflict_damage``.

    ``on_resolved`` es un callback opcional que recibe el
    :class:`SaveDamageOutcome` justo antes de infligir el daño (permite
    loguear con el daño final ya calculado).

    No tira el daño: eso es responsabilidad de quien llama (así un área puede
    compartir la misma tirada base entre varios objetivos).
    """
    eff = effect
    if not isinstance(eff, SaveDamage):
        eff = SaveDamage(
            ability=getattr(effect, "ability", "dex"),
            dc=getattr(effect, "dc", 0),
            damage=getattr(effect, "damage", "0"),
            damage_type=getattr(effect, "damage_type", "bludgeoning"),
            on_success=getattr(effect, "on_success", "none"),
        )

    rng = getattr(ctx, "rng", None)
    if rng is None and hasattr(ctx, "randint"):
        rng = ctx

    raw_damage = int(rolled_damage)

    # 1. Tirar salvación (la del objetivo: ventaja/desventaja propias).
    sr = saving_throw(target, eff.ability, int(eff.dc), rng)
    sr = registrar_resistencia(ctx, target, sr)

    # 2. Aplicar el éxito de la salvación.
    if sr.success:
        if eff.on_success == "half":
            dmg_after_save = raw_damage // 2
        else:
            dmg_after_save = 0
    else:
        dmg_after_save = raw_damage

    # 3. Aplicar modificadores del objetivo.
    dt = eff.damage_type
    try:
        dt = parse_damage_type(dt)
    except Exception:
        pass
    final = apply_damage_modifiers(int(dmg_after_save), dt, target)

    outcome = SaveDamageOutcome(
        save=sr,
        rolled_damage=raw_damage,
        damage_after_save=int(dmg_after_save),
        final_damage=int(final),
        damage_type=dt,
    )

    # 4. Log (antes de infligir, como en el flujo original).
    if on_resolved is not None:
        try:
            on_resolved(outcome)
        except Exception:
            pass

    # 5. Infligir daño por la función única.
    _inflict_for_save(target, final, dt, source, ctx)

    return outcome


def resolve_save_damage(source: Any, target: Any, effect: SaveDamage,
                        ctx: Any) -> int:
    """Resuelve daño con salvación. Devuelve el daño final infligido.

    Orden del RNG: daño primero, luego salvación.
    """
    # Obtener rng.
    rng = getattr(ctx, "rng", None)
    if rng is None and hasattr(ctx, "randint"):
        rng = ctx

    eff = effect
    if not isinstance(eff, SaveDamage):
        # tolerante: construir desde dict-like
        eff = SaveDamage(
            ability=getattr(effect, "ability", "dex"),
            dc=getattr(effect, "dc", 0),
            damage=getattr(effect, "damage", "0"),
            damage_type=getattr(effect, "damage_type", "bludgeoning"),
            on_success=getattr(effect, "on_success", "none"),
        )

    verbose = bool(getattr(ctx, "verbose", False)) or (getattr(ctx, "log", None) is not None)

    # 1. Tirar daño completo UNA vez.
    raw_damage = roll_dice(str(eff.damage), rng)

    def _log_line_outcome(outcome: SaveDamageOutcome) -> None:
        if not verbose:
            return
        sr = outcome.save
        roll_value = sr.total - sr.bonus
        mode_tag = _mode_tag(sr)
        outcome_tag = _outcome_tag(sr, eff.on_success)
        _log_line(ctx, f"  {getattr(source, 'name', source)} -> {getattr(target, 'name', target)}: "
                 f"salvación {sr.ability.upper()} {roll_value}{mode_tag}+{sr.bonus}={sr.total} "
                 f"vs CD {sr.dc}, {'éxito' if sr.success else 'fallo'}, "
                 f"daño {outcome.rolled_damage} -> {outcome.damage_after_save} ({outcome_tag})")

    # 2. Núcleo: salvación, modificadores del objetivo e infligir daño.
    outcome = apply_save_damage(source, target, eff, raw_damage, ctx,
                                on_resolved=_log_line_outcome)

    # 3. Reacción del objetivo al recibir daño (p. ej. Hellish Rebuke).
    if int(outcome.final_damage) > 0:
        _reaccion_si_procede(target, ctx)

    return int(outcome.final_damage)


def _reaccion_si_procede(target: Any, ctx: Any) -> None:
    """Dispara la reacción de ``target`` si acaba de recibir daño (5e).

    Import perezoso de ``spells`` para evitar ciclos de importación.
    """
    if target is None or ctx is None:
        return
    from .spells import trigger_reaction
    try:
        trigger_reaction(target, ctx)
    except Exception:
        pass


# Exportar normalize para uso interno también.
__all__ = [
    "ABILITY_ALIASES",
    "normalize_ability",
    "SaveResult",
    "saving_throw",
    "registrar_resistencia",
    "SaveDamage",
    "SaveDamageOutcome",
    "apply_save_damage",
    "resolve_save_damage",
]

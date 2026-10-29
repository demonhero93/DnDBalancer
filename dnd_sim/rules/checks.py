"""Pruebas de característica de D&D 5e.

Regla 5e: en una prueba de característica el **20 natural NO es éxito
automático** y el **1 natural NO es fallo automático**: el éxito depende
solo de ``total >= cd``.

Estas pruebas permiten escapar de estados (por ejemplo, liberarse de la
telaraña de la araña gigante). Se tiran al **inicio del turno** del
afectado: no son una elección, son automáticas.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from ..core.dice import RollMode, roll_d20
from ..core.skills import normalize_skill, skill_ability
from .roll_modifiers import check_modifiers

from .saves import normalize_ability


@dataclass
class CheckResult:
    """Resultado de una prueba de característica."""

    ability: str
    dc: int
    rolls: list[int]
    bonus: int
    total: int
    success: bool
    mode: RollMode
    # Habilidad usada, si la prueba era de habilidad (``None`` en una
    # prueba de característica pura).
    skill: str | None = None


def ability_check_bonus(target: Any, ability: str) -> int:
    """Bono total de una prueba de característica.

    Delega en ``target.check_bonus`` (modificador + competencia si la
    hay). Objetivos sin ese método caen al modificador puro.
    """
    check_bonus = getattr(target, "check_bonus", None)
    if callable(check_bonus):
        try:
            return int(check_bonus(ability))
        except Exception:
            pass
    try:
        return int(target.abilities.mod(ability))
    except Exception:
        return 0


def skill_bonus(target: Any, skill: str, ability: str | None = None) -> int:
    """Bono total de una prueba de habilidad (modificador + competencia).

    Delega en ``target.skill_bonus``. Objetivos sin ese método caen al
    modificador de la característica asociada a la habilidad (o a
    ``ability``, si la prueba tira con otra característica).
    """
    bonus_of = getattr(target, "skill_bonus", None)
    if callable(bonus_of):
        try:
            return int(bonus_of(skill, ability=ability))
        except TypeError:
            # Objetivo duck-typed cuyo ``skill_bonus`` no acepta ``ability``.
            try:
                return int(bonus_of(skill))
            except Exception:
                pass
        except Exception:
            pass
    try:
        return int(target.abilities.mod(ability or skill_ability(skill)))
    except Exception:
        return 0


def _guia(target: Any, rng: Any) -> int:
    """Bonus de la guía (+1d4), si el objetivo está guiado.

    El hechizo de guía (PHB 2024) da +1d4 a **una** prueba de
    característica y **no se consume** al usarla: dura lo que el hechizo
    (hasta 1 minuto).
    """
    try:
        from .conditions import Condition
        tracker = getattr(target, "conditions", None)
        if tracker is None or not tracker.has(Condition.GUIDED):
            return 0
    except Exception:
        return 0
    if rng is None:
        return 0
    try:
        return int(rng.randint(1, 4))
    except Exception:
        return 0


def _resolve_mods(target: Any, ability: str,
                  skill: str | None, mode: Any) -> tuple[CheckModifiers, RollMode]:
    """Modificadores de la tirada y modo resuelto.

    Los modificadores se calculan siempre (suelo del total y
    ``ability_override`` viajan en ellos); el ``mode`` pedido, si lo hay,
    manda sobre el modo de los modificadores.
    """
    mods = check_modifiers(target, ability, skill=skill)
    if mode is None:
        return mods, mods.mode
    text = str(mode).strip().lower()
    resolved = RollMode(text) if text in {m.value for m in RollMode} else RollMode.NORMAL
    return mods, resolved


def _finish_check(ability: str, skill: str | None, dc: int, rng: Any,
                  mode: RollMode, bonus: int,
                  minimum_total: int | None = None) -> CheckResult:
    """Tira el d20 con ``bonus`` y arma el :class:`CheckResult`.

    ``minimum_total`` (Indomitable Might) sube el total si sale más bajo.
    """
    result = roll_d20(rng, mode)
    total = result.value + bonus
    if minimum_total is not None:
        total = max(int(total), int(minimum_total))
    return CheckResult(
        ability=ability,
        dc=int(dc),
        rolls=list(result.rolls),
        bonus=int(bonus),
        total=int(total),
        success=bool(total >= int(dc)),
        mode=mode,
        skill=skill,
    )


def ability_check(target: Any, ability: str, dc: int, rng: random.Random,
                  mode: Any = None) -> CheckResult:
    """Tira una prueba de característica.

    Usa ventaja/desventaja según :func:`check_modifiers` (y no el 20 natural
    como éxito automático).
    """
    ab = normalize_ability(ability)
    mods, resolved = _resolve_mods(target, ab, None, mode)
    bonus = ability_check_bonus(target, ab)
    # El hechizo de guía añade +1d4 a una prueba (y se consume).
    bonus += _guia(target, rng)
    return _finish_check(ab, None, dc, rng, resolved, bonus,
                         getattr(mods, "minimum_total", None))


def skill_check(target: Any, skill: str, dc: int, rng: random.Random,
                mode: Any = None) -> CheckResult:
    """Tira una prueba de habilidad (Atletismo, Sigilo, Arcana...).

    Usa la característica asociada a la habilidad y el bono completo
    (modificador + competencia/expertise vía :func:`skill_bonus`).
    """
    name = normalize_skill(skill)
    mods, resolved = _resolve_mods(target, skill_ability(name), name, mode)
    # Primal Knowledge: la habilidad puede tirarse con otra característica
    # (p. ej. Sigilo como FUE con Furia) y con esa se suma el bono.
    eff_ability = getattr(mods, "ability_override", None) or skill_ability(name)
    bonus = skill_bonus(target, name, ability=eff_ability)
    # El hechizo de guía añade +1d4 a una prueba (y se consume).
    bonus += _guia(target, rng)
    return _finish_check(eff_ability, name, dc, rng, resolved, bonus,
                         getattr(mods, "minimum_total", None))


__all__ = ["CheckResult", "ability_check", "ability_check_bonus",
           "skill_bonus", "skill_check"]

"""Áreas de efecto: acciones que afectan a varios objetivos hostiles.

Una acción de área elige al azar un número de objetivos válidos (hostiles
vivos: nunca aliados, ni el propio lanzador, ni muertos) y les aplica el
mismo daño base: la tirada de daño se hace **una sola vez** y cada objetivo
affected hace su propia tirada de salvación.

Orden del RNG (documentado y estable):

1. ``k`` (número de objetivos afectados),
2. muestreo de los objetivos,
3. tirada de daño (compartida),
4. salvación del objetivo 1, del objetivo 2, ... (en orden de selección).

# TODO: geometría real (alcance, cono, línea): aquí solo se sortea quién
cae dentro del área.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

try:
    from .actions import ActionType, CombatAction, CombatContext
    from .dice import roll_dice
    from .randomness import pick, sample
    from .saves import SaveDamage, _mode_tag, _outcome_tag, apply_save_damage
    from .targeting import valid_targets
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from actions import ActionType, CombatAction, CombatContext
        from dice import roll_dice
        from randomness import pick, sample
        from saves import SaveDamage, _mode_tag, _outcome_tag, apply_save_damage
        from targeting import valid_targets
    except ImportError:
        from dnd_sim.actions import ActionType, CombatAction, CombatContext
        from dnd_sim.dice import roll_dice
        from dnd_sim.randomness import pick, sample
        from dnd_sim.saves import SaveDamage, _mode_tag, _outcome_tag, apply_save_damage
        from dnd_sim.targeting import valid_targets


@dataclass
class AreaTargeting:
    """Cuántos objetivos puede afectar un área.

    ``min_targets`` y ``max_targets`` se recortan al número de objetivos
    disponibles; si ``max_targets`` es ``None`` el área puede alcanzar a
    todos los hostiles vivos.
    """

    min_targets: int = 1
    max_targets: int | None = None


def select_area_targets(actor, ctx, targeting: AreaTargeting) -> list:
    """Elige al azar los objetivos de un área.

    1. ``pool`` = hostiles vivos (nunca aliados, ni el lanzador, ni muertos).
    2. ``k`` uniforme en ``[lo, hi]`` (no consume RNG si solo hay un valor).
    3. Muestreo sin reemplazo de ``k`` objetivos.
    """
    pool = valid_targets(actor, ctx)
    if not pool:
        return []
    total = len(pool)
    lo = max(0, min(int(targeting.min_targets), total))
    hi = total if targeting.max_targets is None else min(int(targeting.max_targets), total)
    hi = max(hi, lo)
    k = lo if lo == hi else pick(ctx.rng, range(lo, hi + 1))
    return sample(ctx.rng, pool, k)


try:
    from .log import log_line as _log_line
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from log import log_line as _log_line
    except ImportError:
        from dnd_sim.log import log_line as _log_line


@dataclass
class AreaSaveAction(CombatAction):
    """Acción de área con daño y salvación (alientos, ácidos, conos...).

    ``effect`` es un :class:`~dnd_sim.saves.SaveDamage`; ``targeting`` dice
    cuántos objetivos puede alcanzar; ``usage`` es opcional (usos limitados).
    ``condition`` es opcional: un ``ConditionEffect`` que se aplica a cada
    objetivo que **falle** la misma salvación (p. ej. el derribo del ala del
    dragón: daño y condición comparten la tirada).
    """

    effect: Any = None
    targeting: AreaTargeting = field(default_factory=AreaTargeting)
    usage: Any = None
    action_type: ActionType = ActionType.ACTION
    name: str = "Área"
    # Condición opcional que se aplica si el objetivo falla la salvación.
    condition: Any = None

    def __post_init__(self) -> None:
        if not getattr(self, "name", ""):
            self.name = "Área"

    def _as_save_damage(self) -> SaveDamage | None:
        """Normaliza el efecto a ``SaveDamage`` (tolerante)."""
        effect = self.effect
        if isinstance(effect, SaveDamage):
            return effect
        try:
            return SaveDamage(
                ability=getattr(effect, "ability", "dex"),
                dc=getattr(effect, "dc", 0),
                damage=getattr(effect, "damage", "1d6"),
                damage_type=getattr(effect, "damage_type", "bludgeoning"),
                on_success=getattr(effect, "on_success", "none"),
            )
        except Exception:
            return None

    def execute(self, context: CombatContext) -> None:
        actor = context.actor
        effect = self._as_save_damage()
        if effect is None:
            return

        pool = valid_targets(actor, context)
        targets = select_area_targets(actor, context, self.targeting)

        # Registro de la acción de área (para estadísticas).
        hits = getattr(context, "area_targets_hit", None)
        if hits is not None:
            try:
                hits.append(len(targets))
            except Exception:
                pass

        _log_line(context, f"{getattr(actor, 'name', actor)} usa {self.name} "
                          f"sobre {len(targets)} de {len(pool)} objetivos:")

        if not targets:
            return

        # El daño se tira UNA sola vez y lo comparten todos los afectados.
        raw_damage = roll_dice(str(effect.damage), context.rng)

        for target in targets:
            def _log_target(outcome, _target=target) -> None:
                sr = outcome.save
                roll_value = sr.total - sr.bonus
                tag = _outcome_tag(sr, effect.on_success)
                _log_line(context,
                          f"  {getattr(_target, 'name', _target)}: "
                          f"salvación {sr.ability.upper()} {roll_value}{_mode_tag(sr)}"
                          f"+{sr.bonus}={sr.total} vs CD {sr.dc}, "
                          f"{'éxito' if sr.success else 'fallo'}, "
                          f"daño base {outcome.rolled_damage} -> "
                          f"{outcome.damage_after_save} ({tag}), "
                          f"daño final {outcome.final_damage}")

            outcome = apply_save_damage(actor, target, effect, raw_damage, context,
                                        on_resolved=_log_target)
            # Condición opcional: se aplica si el objetivo ha fallado la
            # misma salvación que el daño (p. ej. daño + derribo).
            if self.condition is not None and not outcome.save.success:
                self._aplicar_condicion(target, context, actor)

    def _aplicar_condicion(self, target, context, actor) -> None:
        """Aplica la condición opcional al objetivo que falló la salvación.

        La condición se modela con la misma mecánica que ``ConditionAction``:
        si el efecto tiene ``repeat_save``, se crea la salvación de repetición
        que el afectado podrá repetir al final de su turno.
        """
        efecto = self.condition
        try:
            from .conditions import RepeatSave, apply_condition
        except ImportError:  # pragma: no cover - ejecución como script suelto
            try:
                from conditions import RepeatSave, apply_condition
            except ImportError:
                from dnd_sim.conditions import RepeatSave, apply_condition
        repeat = None
        if getattr(efecto, "repeat_save", False):
            repeat = RepeatSave(ability=getattr(efecto, "save_ability", None) or "dex",
                                dc=int(getattr(efecto, "dc", 0) or 0))
        apply_condition(
            target, efecto.condition, context,
            source=actor,
            duration_rounds=getattr(efecto, "duration_rounds", None),
            repeat_save=repeat,
            escape=getattr(efecto, "escape", None),
        )


__all__ = ["AreaTargeting", "AreaSaveAction", "select_area_targets"]

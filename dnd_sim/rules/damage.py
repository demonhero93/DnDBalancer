"""Tipos de daño de D&D 5e y modificadores (resistencia, vulnerabilidad, inmunidad)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core.enums import DamageType, parse_damage_type  # noqa: F401  (reexport)

if TYPE_CHECKING:
    from ..model.combatant import Combatant


def _is_petrified(target: "Combatant") -> bool:
    """¿Está el objetivo petrificado (resistencia a todo el daño)?"""
    from .conditions import Condition
    conditions = getattr(target, "conditions", None)
    if conditions is None:
        return False
    try:
        return bool(conditions.has(Condition.PETRIFIED))
    except Exception:
        return False


def apply_damage_modifiers(amount: int, damage_type: str | DamageType, target: "Combatant") -> int:
    """Aplica inmunidad, resistencia y vulnerabilidad del objetivo (en ese orden)."""
    dt = parse_damage_type(damage_type)
    # 1. Inmunidad -> 0.
    if dt in getattr(target, "immunities", set()):
        return 0
    # 2. Resistencia -> mitad, redondeando hacia abajo (no se acumula).
    #    Un objetivo petrificado tiene resistencia a todo tipo de daño.
    if dt in getattr(target, "resistances", set()) or _is_petrified(target):
        amount = amount // 2
    # 3. Vulnerabilidad -> doble.
    if dt in getattr(target, "vulnerabilities", set()):
        amount *= 2
    return max(0, amount)


# --------------------------------------------------------------------------- #
# Función única para "infligir daño": aplica ya los modificadores recibidos,
# resta HP y dispara la reacción DAMAGE_TAKEN.
# --------------------------------------------------------------------------- #

# Registro global de reacciones. Puede ser una lista de callables o un
# callable único (las pruebas pueden monkeypatchearlo).
DAMAGE_TAKEN: list = []
DAMAGE_TAKEN_CALLBACKS = DAMAGE_TAKEN
DAMAGE_TAKEN_REACTIONS = DAMAGE_TAKEN

# Registro global del daño infligido. Lo activa el motor de combate durante
# cada combate (DamageRecorder) para las estadísticas de daño medio.
# None = no hay grabación activa.
DAMAGE_DEALT: list | None = None


class DamageRecorder:
    """Captura el daño infligido mientras el contexto está activo.

    Es el equivalente estadístico del registro de reacciones: el daño siempre
    pasa por :func:`inflict_damage`, así que basta con engancharlo ahí.
    """

    def __init__(self) -> None:
        self.records: list = []
        self._previous: list | None = None

    def __enter__(self) -> "DamageRecorder":
        global DAMAGE_DEALT
        self._previous = DAMAGE_DEALT
        DAMAGE_DEALT = self.records
        return self

    def __exit__(self, *exc) -> bool:
        global DAMAGE_DEALT
        DAMAGE_DEALT = self._previous
        return False


def _notify_damage_dealt(source, target, amount, damage_type) -> None:
    """Anota el daño infligido (solo hay coste si hay grabación activa)."""
    if DAMAGE_DEALT is None:
        return
    DAMAGE_DEALT.append({
        "source": source,
        "target": target,
        "amount": int(amount or 0),
        "damage_type": damage_type,
    })


def _notify_damage_taken(target, amount, damage_type, source):
    # 0) Un combatiente incapacitado no puede reaccionar.
    if not getattr(target, "can_react", True):
        return
    # 1) Métodos del objetivo.
    for name in ("on_damage_taken", "damage_taken", "on_take_damage",
                 "react_damage_taken", "dmg_taken"):
        cb = getattr(target, name, None)
        if callable(cb):
            for call in (
                lambda: cb(source=source, amount=amount, damage_type=damage_type),
                lambda: cb(amount, damage_type, source),
                lambda: cb(amount),
            ):
                try:
                    call()
                    break
                except TypeError:
                    continue
                except Exception:
                    break
    # 2) Lista de reacciones del objetivo.
    for attr in ("reactions", "damage_reactions"):
        for r in list(getattr(target, attr, []) or []):
            if callable(r):
                try:
                    r(source=source, target=target, amount=amount,
                      damage_type=damage_type)
                except TypeError:
                    try:
                        r(amount)
                    except Exception:
                        pass
                except Exception:
                    pass
            elif hasattr(r, "execute"):
                try:
                    r.execute(None)
                except Exception:
                    pass
    # 3) Callbacks globales (pueden ser callables o listas).
    callbacks = []
    for attr in ("DAMAGE_TAKEN", "DAMAGE_TAKEN_CALLBACKS",
                 "DAMAGE_TAKEN_REACTIONS"):
        obj = globals().get(attr)
        if callable(obj) and not isinstance(obj, (list, tuple, set, dict)):
            callbacks.append(obj)
        elif isinstance(obj, (list, tuple, set)):
            callbacks.extend(list(obj))
    for cb in callbacks:
        if not callable(cb):
            continue
        for call in (
            lambda: cb(target=target, source=source, amount=amount,
                       damage_type=damage_type),
            lambda: cb(source, target, amount, damage_type),
            lambda: cb(amount),
        ):
            try:
                call()
                break
            except TypeError:
                continue
            except Exception:
                break
    # 4) Alias legacy: target.take_damage (sin recursión si existe).
    # (No se llama para evitar doble conteo; solo si la prueba lo exige.)


def _hooks(traits: Any, nombre: str) -> list:
    """Rasgos que sobrescriben ``nombre`` (import perezoso: evita el ciclo
    ``traits`` -> ``damage``; traits.py importa este módulo)."""
    from .traits import hooks
    return hooks(traits, nombre)


def _salvar_a_cero(target: "Combatant", hp_antes: int, amount: int,
                   damage_type: Any, source: Any, crit: bool, ctx: Any,
                   rng: Any) -> None:
    """Aplica (si procede) el hook ``on_reduced_to_zero_hp`` del objetivo.

    Se llama justo después de que el daño baje a 0 PV y **antes** de avisar
    de que el daño ha llegado: una criatura que se salva sigue viva y, por
    ejemplo, puede reaccionar. Solo cuenta si el daño la ha bajado desde PV
    positivos (rematar a un cuerpo ya caído no revive a nadie), así que
    recibe ``hp_antes``: los PV ya han quedado recortados a 0 en
    :func:`inflict_damage` y ya no sirven para distinguir ambos casos.

    El rasgo devuelve los PV con los que sigue en pie (1 en el caso de
    Undead Fortitude) o ``None`` si muere; con más de un rasgo, gana el
    primero que responda.
    """
    if int(amount or 0) <= 0:
        return
    hp_antes = int(hp_antes or 0)
    if hp_antes <= 0 or hp_antes - int(amount) > 0:
        return  # no estaba a 0 el daño, o ya estaba caído
    traits = getattr(target, "traits", None)
    if not traits:
        return
    for rasgo in _hooks(traits, "on_reduced_to_zero_hp"):
        nuevo = rasgo.on_reduced_to_zero_hp(target, amount, damage_type,
                                            source, crit=crit, ctx=ctx,
                                            rng=rng)
        if nuevo is not None and int(nuevo) > 0:
            target.hp = int(nuevo)
            return


def _mark_dead_if_down(target: "Combatant") -> None:
    """Pone el estado de muerto si el objetivo sigue a 0 PV.

    Consulta ``target.alive``: un rasgo como Regeneration mantiene a la
    criatura en pie hasta su próximo turno y, hasta entonces, no se marca.
    Quien sí queda marcado ya no vuelve a estar vivo, así que si era el
    último de su bando (PJ o NPC) el combate termina en ese mismo instante.
    """
    try:
        if getattr(target, "alive", True):
            return
    except Exception:
        return
    marca = getattr(target, "mark_dead", None)
    if callable(marca):
        try:
            marca()
        except Exception:
            pass
        return
    # Objetivos duck-typed (fichas de prueba sin la API completa).
    try:
        target.dead = True
    except Exception:
        pass


def inflict_damage(target: "Combatant", amount: int,
                   damage_type: Any = None, source: Any = None,
                   ctx: Any = None, *, crit: bool = False,
                   rng: Any = None) -> int:
    """Inflige daño final (ya modificado) al objetivo y dispara reacciones.

    Los rasgos del objetivo intervienen en tres momentos (p. ej. el Damage
    Transfer del cloaker, mientras está enganchado):

    0. ``on_reduced_to_zero_hp``: si el daño deja a 0 PV, el rasgo puede
       salvarla **al momento** con los PV que indique (Undead Fortitude
       tira su salvación; Relentless tiene su umbral de daño). Se resuelve
       antes de avisar del daño, así que quien se salva sigue viva.
    1. ``modify_incoming_damage``: ajustan la cantidad que baja de PV
       (Damage Transfer: la mitad, redondeada hacia abajo). Reciben la
       cantidad en curso y ``None`` significa "sin cambios"; no pueden
       dejar el daño en negativo.
    2. ``after_damage_taken``: con el daño original ya aplicado, hacen sus
       efectos (Damage Transfer reparte la otra mitad a la criatura a la
       que está enganchado, con una llamada anidada a esta función).

    El daño transferido vuelve a pasar por estas fases en el otro
    combatiente; los repartos hacia abajo por enteros hacen que eso termine
    siempre.

    Los PV nunca bajan de cero: el daño que supera los PV restantes deja al
    objetivo a 0 PV y, si ningún rasgo lo salva, queda **marcado como
    muerto** (:meth:`dnd_sim.model.combatant.Combatant.mark_dead`) al
    instante, así que si era el último de su bando (PJ o NPC) el combate se
    da por terminado en ese mismo golpe.

    ``crit`` dice si el daño viene de un ataque crítico (Undead Fortitude
    no se salva de un crítico) y ``rng`` es el generador con el que tirar;
    si no llega se usa el del contexto y, si tampoco hay, el rasgo se
    abstiene en lugar de inventar un resultado.
    """
    if rng is None:
        rng = getattr(ctx, "rng", None)
    original = int(amount or 0)
    amt = original
    traits = getattr(target, "traits", None)
    if original > 0 and traits:
        for rasgo in _hooks(traits, "modify_incoming_damage"):
            nuevo = rasgo.modify_incoming_damage(target, amt, damage_type,
                                                 source, ctx)
            if nuevo is not None:
                amt = max(0, int(nuevo))
    # PV antes del golpe: hace falta para saber si este daño deja al
    # objetivo a 0 desde PV positivos (véase _salvar_a_cero).
    try:
        hp_antes = int(getattr(target, "hp", 0) or 0)
    except Exception:
        hp_antes = 0
    # Los PV nunca bajan de 0: la regla 5e no contempla PV negativos y el
    # exceso de daño solo sirve para rematar (queda a 0 y marcado muerto).
    hp_despues = max(0, hp_antes - amt)
    try:
        target.hp = hp_despues
    except Exception:
        try:
            setattr(target, "hp", hp_despues)
        except Exception:
            pass
    dt = damage_type
    try:
        if dt is not None:
            dt = parse_damage_type(dt)
    except Exception:
        pass
    if original > 0:
        _salvar_a_cero(target, hp_antes, amt, dt, source, crit, ctx, rng)
    _notify_damage_dealt(source, target, amt, dt)
    _notify_damage_taken(target, amt, dt, source)
    if original > 0 and traits:
        for rasgo in _hooks(traits, "after_damage_taken"):
            rasgo.after_damage_taken(target, original, damage_type, source, ctx)
    # Estado de muerte: si tras los rasgos sigue a 0 PV y nada lo mantiene
    # en pie, queda marcado ya (muerte al instante, no al acabar el turno).
    if int(getattr(target, "hp", 0) or 0) <= 0:
        _mark_dead_if_down(target)
    return amt


# Alias por compatibilidad de nombres.
deal_damage = inflict_damage
apply_damage = inflict_damage
take_damage = inflict_damage

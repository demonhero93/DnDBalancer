"""Motor de Maestría con Armas (PHB 2024) para los combatientes.

La clave de maestría viaja en ``Attack.mastery`` (``"topple"``, ``"vex"``...).
La tabla :data:`MAESTRIAS` traduce del nombre del arma a esa clave; el campo
``mastery`` es la FUENTE que consulta el motor (los monstruos que ya traen
``mastery`` relleno no cambian de comportamiento: la tabla solo se usa para
ASIGNAR claves en ``apply_fighter`` vía :func:`maestria_de`).

La llamada vive en :func:`dnd_sim.engine.combat.attack.attack_roll`, tras
resolver el daño y SOLO si ``atk.mastery`` no está vacío (sin clave no se
invoca nada: cero coste y cero RNG). :func:`resolver_maestria` resuelve la
propiedad final: la del arma, sustituida por Tactical Master (nivel 9, si el
rasgo del atacante lo pide).

Efectos implementados: Topple (salvación de CON → PRONE), Vex (ventaja en la
siguiente tirada contra el objetivo), Sap (desventaja del objetivo hasta tu
siguiente turno) y Graze (daño = modificador de característica al fallar).

Sin efecto (dato con ``# TODO``): Push y Slow (el sim no modela movimiento
ni posiciones). Pendientes en TODO.md: Cleave (segundo objetivo adyacente)
y Nick (ataque ligero extra).
"""
from __future__ import annotations

from typing import Any

from ..core.randomness import pick
from .conditions import Condition, EscapeCheck, apply_condition
from .damage import apply_damage_modifiers, inflict_damage
from .saves import registrar_resistencia, saving_throw

#: Propiedad de maestría de cada arma, por NOMBRE normalizado (minúsculas).
#: Claves EN del PHB + alias en español de los PJs del simulador.
MAESTRIAS: dict[str, str] = {
    # Simples cuerpo a cuerpo
    "club": "slow", "garrote": "slow",
    "dagger": "nick", "daga": "nick",
    "greatclub": "push", "porra": "push",
    "handaxe": "vex", "hacha de mano": "vex",
    "javelin": "slow", "jabalina": "slow",
    "light hammer": "nick", "martillo ligero": "nick",
    "mace": "sap", "maza": "sap",
    "quarterstaff": "topple", "bastón": "topple",
    "sickle": "nick", "hoz": "nick",
    "spear": "sap", "lanza": "sap",
    # Simples a distancia
    "dart": "vex", "dardo": "vex",
    "light crossbow": "slow", "ballesta ligera": "slow",
    "shortbow": "vex", "arco corto": "vex",
    "sling": "slow", "honda": "slow",
    # Marciales cuerpo a cuerpo
    "battleaxe": "topple", "hacha de batalla": "topple",
    "flail": "sap", "maza de guarnición": "sap",
    "glaive": "graze", "guadaña": "graze",
    "greataxe": "cleave", "hacha gigante": "cleave",
    "greatsword": "graze", "mandoble": "graze",
    "halberd": "cleave", "alabarda": "cleave",
    "lance": "topple", "lanza larga": "topple",
    "longsword": "sap", "espada larga": "sap",
    "maul": "topple", "martillo de guerra": "topple",
    "maza pesada": "topple",
    "morningstar": "sap", "estrella de alba": "sap",
    "pike": "push", "pica": "push",
    "rapier": "vex", "estoque": "vex",
    "scimitar": "nick", "sable": "nick", "guadaña corta": "nick",
    "shortsword": "vex", "espada corta": "vex",
    "trident": "topple", "tridente": "topple",
    "warhammer": "push",
    "war pick": "sap", "pico de guerra": "sap",
    "whip": "slow", "látigo": "slow",
    # Marciales a distancia
    "blowgun": "vex", "cerbatana": "vex",
    "hand crossbow": "vex", "ballesta de mano": "vex",
    "heavy crossbow": "push", "ballesta pesada": "push",
    "longbow": "slow", "arco largo": "slow",
    "musket": "slow", "mosquete": "slow",
    "pistol": "vex", "pistola": "vex",
}

#: Efectos registrados por clave (los que el modelo NO puede aplicar están
#: documentados aquí como sin efecto: ver docstring del módulo).
EFECTOS: tuple[str, ...] = ("topple", "vex", "sap", "graze")
#: Sin efecto en el sim (sin sistema de movimiento/posiciones).
# TODO: Push (empujar 10 ft) y Slow (-10 ft de velocidad) requieren
# movimiento y posiciones, que el sim no modela.
EFECTOS_SIN_EFECTO: tuple[str, ...] = ("push", "slow")


def maestria_de(nombre_arma: str) -> str:
    """Clave de maestría del arma llamada ``nombre_arma`` (``""`` si no hay)."""
    clave = str(nombre_arma or "").strip().lower()
    return MAESTRIAS.get(clave, "")


def resolver_maestria(attacker: Any, attack: Any, rng: Any = None) -> str:
    """Propiedad de maestría efectiva para este ataque.

    La base es SIEMPRE el campo ``attack.mastery`` (nunca la tabla: los
    monstruos no cambian y un arma sin clave sigue sin maestría). Si el
    atacante tiene un rasgo con ``sustituir_maestria`` (Tactical Master),
    este decide la sustitución. Sin clave base no se consulta nada (sin
    RNG).
    """
    base = str(getattr(attack, "mastery", "") or "").strip().lower()
    if not base:
        return ""
    for rasgo in getattr(attacker, "traits", None) or ():
        elegir = getattr(rasgo, "sustituir_maestria", None)
        if callable(elegir):
            base = str(elegir(base, rng) or base).strip().lower()
    return base


def _cd_topple(attacker: Any, attack: Any) -> int:
    """CD de Topple: 8 + competencia + mod de la característica del ataque."""
    ability = str(getattr(attack, "ability", "str") or "str")
    try:
        mod = attacker.abilities.mod(ability)
    except Exception:
        mod = 0
    return 8 + int(getattr(attacker, "proficiency", 0) or 0) + int(mod)


def _log(log: Any, line: str) -> None:
    if log is not None:
        log.append(line)


def _nombre(x: Any) -> str:
    return str(getattr(x, "name", x) or "")


def al_acertar(attacker: Any, target: Any, attack: Any, *,
               damage: int = 0, rango: Any = None, ctx: Any = None,
               rng: Any = None, log: Any = None) -> None:
    """Efectos de maestría al ACERTAR el ataque (Topple, Vex, Sap).

    Solo se invoca desde ``attack_roll`` si el ataque trae ``mastery``.
    Topple decide con ``pick`` (patrón Raíces Golpeadoras); Vex y Sap son
    automáticos (cero RNG) y solo necesitan ``ctx`` para la caducidad.
    """
    maestria = resolver_maestria(attacker, attack, rng)
    if not maestria:
        return
    if maestria == "topple":
        if rng is None or target is None:
            return
        if pick(rng, ("no", "si")) == "no":
            return  # decisión aleatoria de aplicar la maestría
        sr = saving_throw(target, "con", _cd_topple(attacker, attack), rng)
        registrar_resistencia(ctx, target, sr)
        if sr.success:
            return
        apply_condition(target, Condition.PRONE, ctx, source=attacker,
                        escape=EscapeCheck(abilities=("str", "dex"), dc=10,
                                           consumes_action=False))
        _log(log, f"  {_nombre(target)} cae derribado "
                  f"(Maestría Topple de {_nombre(attacker)})")
        return
    if ctx is None or target is None:
        return  # sin contexto no hay ronda ni nombres que marcar
    ronda = int(getattr(ctx, "round", 0) or 0)
    if maestria == "vex":
        # shortcut: caduca a los 2 rondas (cubre «tu siguiente turno»);
        # se consume en la primera tirada elegible.
        if int(damage) <= 0:
            return  # solo «al acertar y causar daño»
        estado = getattr(attacker, "state", None)
        nombre = _nombre(target)
        if estado is None or not nombre:
            return
        estado.maestria_ventaja[nombre] = ronda + 2
        _log(log, f"  {_nombre(attacker)} studia a {_nombre(target)} "
                  f"(Maestría Vex)")
    elif maestria == "sap":
        # shortcut: caduca en la ronda siguiente («hasta el inicio de tu
        # siguiente turno»); la desventaja vive en el SUJETO afectado.
        estado = getattr(target, "state", None)
        nombre = _nombre(attacker)
        if estado is None or not nombre:
            return
        estado.maestria_desventaja[nombre] = ronda + 1
        _log(log, f"  {_nombre(target)} queda observado por {_nombre(attacker)} "
                  f"(Maestría Sap)")


def al_fallar(attacker: Any, target: Any, attack: Any, *,
              rango: Any = None, ctx: Any = None, rng: Any = None,
              log: Any = None) -> None:
    """Efectos de maestría al FALLAR el ataque (Graze).

    Push/Slow no tienen efecto (sin movimiento) y Cleave/Nick no llegan
    aquí (ver docstring del módulo), así que una clave de ese grupo sale
    sin consumir nada.
    """
    maestria = resolver_maestria(attacker, attack, rng)
    if maestria != "graze" or target is None:
        return
    ability = str(getattr(attack, "ability", "str") or "str")
    try:
        bruto = int(attacker.abilities.mod(ability))
    except Exception:
        return
    bruto = max(0, bruto)  # «mínimo 0» (un modificador negativo no resta)
    if bruto <= 0:
        return  # sin modificador no hay daño que aplicar (y sin log)
    tipo = getattr(attack, "damage_type", None) or "bludgeoning"
    dmg = apply_damage_modifiers(bruto, tipo, target)
    if dmg <= 0:
        return  # inmunidad total: nada que aplicar
    inflict_damage(target, dmg, tipo, source=attacker, ctx=ctx,
                   crit=False, rng=rng)
    _log(log, f"  {_nombre(attacker)} roza a {_nombre(target)} con "
              f"{_nombre(attack)} (Maestría Graze: {dmg} "
              f"{getattr(tipo, 'value', tipo)})")


def consumir_marcas(mods: Any, attacker: Any, target: Any,
                    ctx: Any = None) -> None:
    """Consume las marcas pendientes en esta tirada.

    Se llama desde :func:`dnd_sim.rules.roll_modifiers.attack_modifiers`
    (bloque 5c): Vex da ventaja al ATACANTE contra ``target``; Sap da
    desventaja al atacante porque ``target`` lo marcó. Además las marcas
    de Battle Master: Distracting (en el OBJETIVO) da ventaja al primer
    atacante distinto del marcador y se consume; Goading (en el
    ATACANTE) da desventaja a quien está marcado al atacar a cualquiera
    que no sea su marcador y NO se consume. Cada marca caducada se borra
    y sin ``ctx`` o sin marcas no se hace nada (cero RNG).
    """
    if ctx is None or attacker is None or target is None:
        return
    ronda = int(getattr(ctx, "round", 0) or 0)
    estado = getattr(attacker, "state", None)
    nombre_obj = _nombre(target)
    marcas = getattr(estado, "maestria_ventaja", None)
    if marcas is not None and nombre_obj in marcas:
        if marcas[nombre_obj] > ronda:
            mods.advantage_sources.append("Maestría Vex")
        del marcas[nombre_obj]  # caducada o consumida
    estado_obj = getattr(target, "state", None)
    nombre_atk = _nombre(attacker)
    marcas_des = getattr(estado_obj, "maestria_desventaja", None)
    if marcas_des is not None and nombre_atk in marcas_des:
        if marcas_des[nombre_atk] > ronda:
            mods.disadvantage_sources.append("Maestría Sap")
        del marcas_des[nombre_atk]
    # Distracting Strike (Battle Master): ventaja al primer atacante
    # distinto del marcador; se consume al concederse y las caducadas se
    # borran. El propio marcador no gana ventaja ni consume la marca.
    marcas_dis = getattr(estado_obj, "distracting", None)
    if marcas_dis:
        for marcador, caduca in list(marcas_dis.items()):
            if caduca <= ronda:
                del marcas_dis[marcador]
            elif nombre_atk != marcador:
                mods.advantage_sources.append("Distracting Strike")
                del marcas_dis[marcador]
    # Goading Attack (Battle Master): desventaja al SUJETO marcado al
    # atacar a cualquiera que no sea su marcador; NO se consume (solo
    # caduca) y al atacar al propio marcador no hay desventaja.
    marcas_goad = getattr(estado, "goading", None)
    if marcas_goad:
        for marcador, caduca in list(marcas_goad.items()):
            if caduca <= ronda:
                del marcas_goad[marcador]
            elif nombre_obj != marcador:
                mods.disadvantage_sources.append("Goading Attack")


__all__ = ["EFECTOS", "EFECTOS_SIN_EFECTO", "MAESTRIAS", "al_acertar",
           "al_fallar", "consumir_marcas", "maestria_de", "resolver_maestria"]

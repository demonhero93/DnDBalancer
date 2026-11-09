"""Tirada de ataque completa: modificadores, ventajas,
críticos, daño, impactos reaccionarios y represalias."""

from __future__ import annotations

import random
from typing import Any

from ...model.attack import Attack
from ...model.combatant import Combatant
from ...core.enums import parse_damage_type
from ...rules.conditions import (CONDITION_ATTACK_DAMAGE, Condition,
                                 remove_invisibility_on_action)
from ...rules.damage import apply_damage_modifiers, inflict_damage
from ...core.dice import RollMode, roll_d20, roll_dice
from ...rules.roll_modifiers import (
    AttackRange, RANGED_COVER_AC_BONUS, attack_modifiers, effective_ac, resolve_attack_range
)


def resolve_roll_mode(attacker: Combatant, target: Combatant,
                      attack: Any = None, rng: Any = None) -> RollMode:
    """Resuelve el modo de tirada por reglas (5e).

    Fuente única: :func:`dnd_sim.rules.roll_modifiers.attack_modifiers` (indicadores
    estáticos + condiciones). Sin ``attack`` solo se aplican los indicadores
    estáticos (compatibilidad).
    """
    if attack is not None:
        return attack_modifiers(attacker, target, attack, rng).mode
    has_adv = bool(getattr(attacker, "attacks_with_advantage", False)) or bool(
        getattr(target, "grants_advantage_to_attackers", False)
    )
    has_dis = bool(getattr(attacker, "attacks_with_disadvantage", False)) or bool(
        getattr(target, "grants_disadvantage_to_attackers", False)
    )
    if has_adv and has_dis:
        return RollMode.NORMAL
    if has_adv:
        return RollMode.ADVANTAGE
    if has_dis:
        return RollMode.DISADVANTAGE
    return RollMode.NORMAL


def _mode_tag(mode: RollMode, result, reason: str = "") -> str:
    """ Sufijo de log con el modo de tirada y su motivo."""
    if mode == RollMode.ADVANTAGE:
        tag = f" (ventaja: {result.rolls[0]}, {result.rolls[1]} -> {result.value}"
        return f"{tag}; {reason})" if reason else f"{tag})"
    if mode == RollMode.DISADVANTAGE:
        tag = f" (desventaja: {result.rolls[0]}, {result.rolls[1]} -> {result.value}"
        return f"{tag}; {reason})" if reason else f"{tag})"
    if reason:
        return f" ({reason})"
    return ""


def _agrandado(combatant: Any) -> bool:
    """¿Tiene activa la condición ENLARGED (agrandado)?"""
    tracker = getattr(combatant, "conditions", None)
    if tracker is None:
        return False
    try:
        return tracker.has(Condition.ENLARGED)
    except Exception:
        return False


def _dados_de_ataque(attacker: Any, atk: Any) -> str:
    """Dados a tirar en ``attack_roll``.

    Si el atacante está agrandado y el ataque declara su variante
    agrandada (la ficha del duergar: «or 11 (2d8 + 2) ... while
    enlarged»), se usan esos dados; si no, los normales.
    """
    dados = str(getattr(atk, "damage", "") or "")
    variante = str(getattr(atk, "enlarged_damage", "") or "")
    if variante and _agrandado(attacker):
        return variante
    return dados


def _bonus_de_tamano(attacker: Any, atk: Any, rng: Any) -> int:
    """+1d4 de las armas agrandadas por el hechizo Enlarge/Reduce.

    El rasgo del duergar ya lleva sus dados duplicados en
    ``enlarged_damage`` (no se suma dos veces). Los ataques de hechizo
    usan la característica de lanzamiento, no Fuerza, así que no reciben
    este bonus («attacks with them [weapons] deal 1d4 extra damage»).
    """
    if not _agrandado(attacker):
        return 0
    if getattr(atk, "enlarged_damage", None):
        return 0
    if str(getattr(atk, "ability", "") or "").strip().lower() != "str":
        return 0
    if not str(getattr(atk, "damage", "") or "").strip():
        return 0
    return roll_dice("1d4", rng)


def _bonus_de_rasgos(attacker: Any, target: Any, rango: Any, crit: bool,
                     ctx: Any, rng: Any, log: Any, atk: Any = None) -> int:
    """Daño adicional que los rasgos del atacante suman a este golpe.

    Hoy solo Martial Advantage (hobgoblin): el hook decide si le aplica (su
    condición es de posición, resuelta al azar si el atacante tiene
    aliados) y tira sus dados. Devuelve la suma de todos los rasgos que
    aporten; el import de :mod:`dnd_sim.rules.traits` es perezoso y solo se hace
    si el atacante tiene rasgos.
    """
    traits = getattr(attacker, "traits", None)
    if not traits:
        return 0
    from ...rules.traits import hooks
    total = 0
    for rasgo in hooks(traits, "extra_attack_damage"):
        bonus = int(rasgo.extra_attack_damage(attacker, target, rango,
                                              crit=crit, ctx=ctx,
                                              rng=rng, atk=atk) or 0)
        if bonus <= 0:
            continue
        total += bonus
        if log is not None:
            log.append(f"  {getattr(attacker, 'name', attacker)} suma "
                       f"{bonus} de {getattr(rasgo, 'name', rasgo)} "
                       f"(daño extra)")
    return total


def _piso_dados_rasgos(attacker: Any, atk: Any, rango: Any, ctx: Any,
                       rng: Any) -> int:
    """Piso de los dados de daño que los rasgos del atacante imponen.

    Mismo patrón perezoso que :func:`_bonus_de_rasgos`; el máximo entre
    los rasgos gana (0 = sin piso, comportamiento idéntico al anterior).
    """
    traits = getattr(attacker, "traits", None)
    if not traits:
        return 0
    from ...rules.traits import hooks
    piso = 0
    for rasgo in hooks(traits, "damage_dice_upgrades"):
        piso = max(piso, int(rasgo.damage_dice_upgrades(attacker, atk,
                                                        rango=rango, ctx=ctx,
                                                        rng=rng) or 0))
    return piso


def _bonus_defensivo(target: Any, attacker: Any, rango: Any, total: int,
                     ca: int, ctx: Any, rng: Any) -> int:
    """CA extra que los rasgos del defensor suman a **este** ataque.

    Hoy solo Parry (hobgoblin warlord): el hook decide si le aplica (solo
    cuerpo a cuerpo, con arma a la mano y si ve al atacante) y, como recibe
    la tirada y la CA efectiva, gasta su reacción solo si con el bonificador
    el golpe deja de entrar. Devuelve la suma de todos los rasgos que
    aporten; el import de :mod:`dnd_sim.rules.traits` es perezoso y solo se hace
    si el defensor tiene rasgos (como en :func:`_bonus_de_rasgos`).
    """
    traits = getattr(target, "traits", None)
    if not traits:
        return 0
    from ...rules.traits import hooks
    total_bonus = 0
    for rasgo in hooks(traits, "defensive_ac_bonus"):
        bonus = int(rasgo.defensive_ac_bonus(target, attacker, rango,
                                              total=total, ca=ca, ctx=ctx,
                                              rng=rng) or 0)
        if bonus > 0:
            total_bonus += bonus
    return total_bonus


def daño_base_arma(attacker: Combatant, target: Combatant, atk: Attack,
                   rango: Any, *, crit: bool, ctx: Any, rng: Any,
                   log: list[str] | None = None) -> int:
    """Daño bruto del arma de un golpe, antes de resistencias.

    Extraído de :func:`attack_roll` sin cambiar el orden de las llamadas
    a ``roll_dice`` ni al RNG. Incluye los dados (con piso GWF si lo
    hay), el mod de característica, el bonus de tamaño, los bonus de
    rasgos (``extra_attack_damage``) y la mitigación de Enfeebling. Lo
    usan el camino normal del ataque y las opciones Piercing/Seeking
    («daño como si hubiera impactado»).
    """
    raw_dmg = 0
    if str(getattr(atk, "damage", "") or "").strip() not in ("", "0"):
        # Un ataque sin daño (p. ej. la Telaraña) no tira dados. Con la
        # condición ENLARGADA se usan los dados agrandados de la ficha
        # (o se añade el +1d4 del hechizo Enlarge/Reduce).
        dados = _dados_de_ataque(attacker, atk)
        piso = _piso_dados_rasgos(attacker, atk, rango, ctx, rng)
        # Sin piso se llama igual que siempre (compatibilidad con los
        # roll_dice parcheados en los tests y cero cambio de resultado).
        dados_dmg = (roll_dice(dados, rng, crit=crit, floor=piso)
                     if piso else roll_dice(dados, rng, crit=crit))
        raw_dmg = max(0, dados_dmg + attacker.dmg_bonus(atk))
        raw_dmg += _bonus_de_tamano(attacker, atk, rng)
        # Daño extra de los rasgos del atacante (p. ej. Martial
        # Advantage): entra en el bruto, así que la inmunidad y la
        # resistencia del objetivo también le afectan.
        raw_dmg += _bonus_de_rasgos(attacker, target, rango, crit,
                                    ctx, rng, log, atk=atk)
        # Enfeebling Arrow (Arcane Archer): mientras la marca siga
        # vigente, el daño de los ataques con arma del afectado va a
        # la mitad (los ataques mágicos —hechizos— quedan fuera).
        if (raw_dmg > 0 and not getattr(atk, "magical", False)
                and attacker.state.enfeeble_mitiga(
                    getattr(ctx, "round", None))):
            raw_dmg = raw_dmg // 2
    return raw_dmg


def _sustituir_ataque(attacker: Any, target: Any, atk: Any, rango: Any,
                      ctx: Any, rng: Any) -> Any:
    """Primer resultado no-None de ``sustituir_ataque`` de los rasgos.

    Duck-typing (patrón ``resolver_maestria``, sin hook HOOK_NAMES): cada
    rasgo del atacante puede definir
    ``sustituir_ataque(attacker, target, atk, rango, *, ctx, rng)`` y
    devolver un resultado (p. ej. ``AtaqueSustituido``) para que
    :func:`attack_roll` lo devuelva sin tirar d20. Si ningún rasgo lo
    define o todos devuelven ``None``, devuelve ``None`` **sin consumir
    RNG**: el flujo posterior es idéntico al de siempre.
    """
    for rasgo in (getattr(attacker, "traits", None) or []):
        metodo = getattr(rasgo, "sustituir_ataque", None)
        if metodo is None:
            continue
        resultado = metodo(attacker, target, atk, rango, ctx=ctx, rng=rng)
        if resultado is not None:
            return resultado
    return None


def _decidir_maniobra(attacker: Any, target: Any, atk: Any, rango: Any, *,
                      roll: int, total: int, ca: int, hit: bool,
                      ctx: Any, rng: Any, log: Any) -> tuple[bool, int]:
    """Punto ÚNICO de decisión de maniobras por ataque (Battle Master).

    Duck-typing (patrón ``_sustituir_ataque``, sin hook HOOK_NAMES): el
    primer rasgo que define
    ``decidir_maniobra(attacker, target, atk, rango, *, roll, total, ca,
    hit, ctx, rng, log)`` recibe la tirada ya conocida y devuelve
    ``(hit, total)`` posiblemente corregidos (Precision Attack puede
    subir el total y convertir un fallo en impacto). Se le llama justo
    DESPUÉS de conocer el resultado y ANTES de aplicar efectos; una
    maniobra como máximo por ataque. El bonificador defensivo del
    defensor (Parry) ya se resolvió antes: la conversión de Precision
    no lo vuelve a consultar (simplificación documentada). Sin rasgos
    que lo definan devuelve los valores recibidos **sin consumir RNG**.
    """
    for rasgo in (getattr(attacker, "traits", None) or []):
        metodo = getattr(rasgo, "decidir_maniobra", None)
        if metodo is None:
            continue
        hit, total = metodo(attacker, target, atk, rango, roll=roll,
                            total=total, ca=ca, hit=hit, ctx=ctx, rng=rng,
                            log=log)
        break
    return hit, total


def attack_roll(attacker: Combatant, target: Combatant, atk: Attack,
                rng: random.Random, log: list[str] | None = None,
                verbose: bool = False, ctx: Any = None,
                allow_friendly: bool = False) -> Any:
    """Resuelve un ataque.

    Secuencia (documentada):

    1. ``resolve_attack_range``: se decide el rango (un arma "cuerpo a
       cuerpo o a distancia" se decide con ``pick`` en **cada** ataque, lo
       que consume RNG).
    2. Se actualiza ``attacker.state.at_range`` (un ataque a distancia deja
       al atacante a distancia; uno cuerpo a cuerpo, cerca).
    3. ``attack_modifiers`` con el rango ya resuelto: un atacante invisible
       ataca con ventaja.
    4. Tirada del d20 con el modo obtenido.
    5. CA efectiva del objetivo (+2 si está a distancia) y comparación con
       la tirada.
    6. Si el ataque iba a entrar, los rasgos del defensor pueden subir su
       CA **contra ese ataque** (Parry), que es cuando se les consulta.
    7. La invisibilidad del atacante termina («until it attacks»): aquí, y
       no antes, porque mientras exista el ataque sale con ventaja y el
       defensor **no puede verlo** (Parry: «must see the attacker»).

    ``allow_friendly`` salta la salvaguarda de fuego amigo para un efecto
    que **fuerza** a un combatiente a atacar a su propio bando (p. ej. la
    rama de venganza de la Fiereza infecciosa); el valor por defecto
    ``False`` conserva el guard en todas las llamadas normales.

    Devuelve el resultado de un ``sustituir_ataque`` de los rasgos (si lo
    hay) en el paso 2b; en ese caso no tira d20 y devuelve ese objeto.
    """
    if not allow_friendly and not attacker.is_hostile_to(target):
        raise ValueError(
            f"{attacker.name} no es hostil a {target.name}: no se permite fuego amigo."
        )
    # Un ataque contra un enemigo extiende la Furia del bárbaro (aunque
    # la tirada falle: basta con haber atacado). Lo limpie ``begin_turn``.
    state = getattr(attacker, "state", None)
    if state is not None:
        try:
            state.attacked_this_turn = True
        except Exception:
            pass
    # (1) Rango resuelto.
    rango = resolve_attack_range(atk, rng)
    # (2) Estado de distancia del atacante.
    _actualizar_distancia(attacker, rango, log)
    # (2b) Sustitución del ataque por duck-typing: si un rasgo del
    # atacante decide reemplazar esta tirada (Piercing/Seeking Arrow),
    # devuelve su resultado aquí SIN d20, sin ``after_attack_roll`` ni
    # maestrías. Sin rasgos o ``None`` → flujo idéntico sin RNG.
    sustituido = _sustituir_ataque(attacker, target, atk, rango, ctx, rng)
    if sustituido is not None:
        return sustituido
    # (3) Modificadores (el rango ya está decidido). Un atacante invisible
    # ataca **con ventaja**; la invisibilidad se quita **después** de
    # resolver el golpe entero, no aquí: «until it attacks» significa que
    # este ataque ya se resuelve con ventaja y con el atacante delante
    # (Parry: «must see the attacker»), y a partir de aquí deja de estar
    # invisible (# TODO: también al lanzar un hechizo o al usar Enlarge;
    # hoy solo la rompe un ataque).
    modifiers = attack_modifiers(attacker, target, atk, rango, ctx=ctx,
                                 rng=rng)
    mode = modifiers.mode
    # (4) Tirada.
    result = roll_d20(rng, mode)
    roll = result.value
    bonus = attacker.to_hit(atk)
    total = roll + bonus + modifiers.bonus
    crit = roll == 20
    # (5) CA efectiva (cobertura a distancia).
    ca_efectiva = effective_ac(target)
    # Estadística: ataques recibidos por objetivos a distancia.
    if getattr(getattr(target, "state", None), "at_range", False):
        recibidos = getattr(ctx, "attacks_at_range", None) if ctx is not None else None
        if recibidos is not None:
            try:
                recibidos.append(1)
            except Exception:
                pass
    # (6) Bonificador de CA del defensor (Parry): solo se le pregunta si el
    # ataque iba a entrar y no es crítico (un 20 natural acierta siempre,
    # así que el rasgo no tendría nada que hacer). Como la tirada y la CA
    # se le pasan, el rasgo solo gasta su reacción si con eso el golpe
    # falla.
    if roll != 1 and not crit and total >= ca_efectiva:
        extra_ca = _bonus_defensivo(target, attacker, rango, total,
                                    ca_efectiva, ctx, rng)
        if extra_ca:
            ca_efectiva += extra_ca
    hit = crit or (roll != 1 and total >= ca_efectiva)
    # (6b) Punto ÚNICO de decisión de maniobras (Battle Master): tras
    # conocer la tirada y ANTES de aplicar efectos. Puede corregir el
    # total y el impacto (Precision); sin rasgo que lo defina el flujo
    # es idéntico y no consume RNG.
    hit, total = _decidir_maniobra(attacker, target, atk, rango,
                                   roll=roll, total=total, ca=ca_efectiva,
                                   hit=hit, ctx=ctx, rng=rng, log=log)
    # Crítico automático (objetivo paralizado o inconsciente a cuerpo a
    # cuerpo): el impacto es crítico aunque el d20 no sea 20; un 1 natural
    # sigue fallando.
    if hit and modifiers.auto_crit_on_hit:
        crit = True
    # (7) Termina la invisibilidad del atacante («until it attacks»), ya
    # resuelto el golpe: mientras existía no se le podía ver (Parry).
    if remove_invisibility_on_action(attacker) and log is not None:
        log.append(f"  {attacker.name} deja de estar invisible (ataca)")
    log_enabled = log is not None
    if hit:
        raw_dmg = daño_base_arma(attacker, target, atk, rango, crit=crit,
                                 ctx=ctx, rng=rng, log=log)
        dt = atk.damage_type
        # Única fuente de inmunidad/resistencia/vulnerabilidad (y de la
        # resistencia por estar petrificado): la regla se aplicaba **dos
        # veces** —una en este bloque y otra en apply_damage_modifiers— y el
        # valor de este bloque se descartaba justo después; solo sobrevivía
        # la etiqueta del log, que ahora se deriva del resultado real.
        dmg = apply_damage_modifiers(raw_dmg, dt, target,
                                     magical=bool(getattr(atk, "magical", False)))
        mod_tag = _tag_modificadores(raw_dmg, dmg, dt, target,
                                     magical=bool(getattr(atk, "magical", False)))
        # Resistencia por marca del defensor (p. ej. Protectores
        # Ancestrales): si el atacante está marcado y golpea a quien no
        # es su marcador, el daño principal queda a la mitad, igual que
        # una resistencia (sin apilarse con la del tipo: se calcula una
        # sola vez a partir del resultado ya modificado).
        _marcador = getattr(getattr(attacker, "state", None),
                            "marked_by", None)
        if dmg > 0 and _marcador is not None and target is not _marcador:
            dmg = max(0, dmg // 2)
        # ``crit`` y ``rng`` viajan con el daño: los rasgos que se salvan a
        # 0 PV (Undead Fortitude) necesitan saber si el golpe fue crítico y
        # con qué tirar.
        inflict_damage(target, dmg, dt, source=attacker, ctx=ctx,
                       crit=crit, rng=rng,
                       magical=bool(getattr(atk, "magical", False)))
        # Daño adicional del arma (p. ej. el 1d6 de fuego del Warhammer
        # del azer o el ácido del mordisco de un dragón). Cada entrada
        # tiene su propio tipo, así que resistencia/inmunidad/vulnerabilidad
        # se resuelven por separado y se suman al total. Los dados extra
        # también se duplican en crítico (como el daño principal).
        extra_total = 0
        extra_partes = []
        for _extra in getattr(atk, "extra_damage", None) or []:
            _raw_x = roll_dice(_extra.damage, rng, crit=crit)
            _dmg_x = apply_damage_modifiers(_raw_x, _extra.damage_type, target,
                                            magical=bool(getattr(atk, "magical", False)))
            # Como el daño principal, la llamada se hace **siempre** (aunque
            # quede en 0 por inmunidad): el registro de daño y las
            # reacciones ven el mismo flujo para los dos tipos.
            inflict_damage(target, _dmg_x, _extra.damage_type,
                           source=attacker, ctx=ctx, crit=crit, rng=rng,
                           magical=bool(getattr(atk, "magical", False)))
            extra_total += _dmg_x
            extra_partes.append(f"{_dmg_x} {_extra.damage_type.value}")
        # Daño extra por condiciones del **atacante** (Marca del cazador,
        # Favor divino): como el daño extra, con su propio tipo y sus
        # modificadores, y sus dados también se duplican en crítico.
        for _cond_extra, (_dados_c, _tipo_c) in CONDITION_ATTACK_DAMAGE.items():
            tracker_c = getattr(attacker, "conditions", None)
            if tracker_c is None or not tracker_c.has(_cond_extra):
                continue
            _tipo_dano = parse_damage_type(_tipo_c)
            _raw_c = roll_dice(_dados_c, rng, crit=crit)
            _dmg_c = apply_damage_modifiers(_raw_c, _tipo_dano, target)
            inflict_damage(target, _dmg_c, _tipo_dano, source=attacker,
                           ctx=ctx, crit=crit, rng=rng)
            extra_total += _dmg_c
            extra_partes.append(f"{_dmg_c} {_tipo_dano.value} "
                                f"({_cond_extra.value})")
        extra_tag = (" + " + " + ".join(extra_partes)) if extra_partes else ""
        _riders_to_run = list(getattr(atk, "save_riders", None) or [])
        if log_enabled:
            mode_tag = _mode_tag(mode, result, modifiers.reason())
            tag = " CRÍTICO" if crit else ""
            ca_tag = (f" (+{RANGED_COVER_AC_BONUS} cobertura a distancia)"
                      if getattr(getattr(target, "state", None), "at_range", False) else "")
            log.append(f"  {attacker.name} -> {target.name} con {atk.name}: "
                       f"{roll}{mode_tag}+{bonus}={total} vs CA {ca_efectiva}{ca_tag}{tag}, "
                       f"{dmg} daño{extra_tag} (HP {max(target.hp, 0)}/{target.max_hp}){mod_tag}")
        if _riders_to_run:
            # Import perezoso **una vez**, fuera del bucle: si no, se repite
            # por cada rider del ataque.
            from ...rules.saves import resolve_save_damage as _rsd
        for _rider in _riders_to_run:
            _rctx = type("RiderCtx", (), {})()
            _rctx.rng = rng
            _rctx.log = log
            _rctx.verbose = log_enabled
            # Los riders también ven a los demás combatientes, así que la
            # mitigación de terceros (Espíritu Guardián) les llega igual.
            _rctx.combatants = getattr(ctx, "combatants", None)
            _rsd(attacker, target, _rider, _rctx)
        # Riders de condición (tras el daño y los riders de daño).
        _apply_condition_riders(attacker, target, atk, rng, log, ctx)
        # Reacción del objetivo golpeado (p. ej. Heated Body del azer): se
        # ejecuta en cada impacto, aunque el daño haya sido 0 por inmunidad.
        _trigger_after_being_hit(target, attacker, rango,
                                 log, ctx, rng)
        # Efectos del propio atacante tras impactar (p. ej. Protectores
        # Ancestrales: marcar a la primera criatura golpeada en el turno).
        _trigger_after_dealing_hit(attacker, target, rango,
                                   log, ctx, rng, atk=atk, damage=dmg)
        # Efectos posteriores al impacto (p. ej. el enganche del cloaker):
        # reciben los modificadores para poder ver si el ataque iba con
        # ventaja (enganche a la cabeza).
        for _efecto in getattr(atk, "on_hit_effects", None) or []:
            _efecto.execute(attacker, target, ctx, modifiers)
        # Reacción del objetivo al recibir daño (p. ej. Hellish Rebuke).
        if dmg + extra_total > 0:
            _reaccion_si_procede(target, ctx)
    elif log_enabled:
        mode_tag = _mode_tag(mode, result, modifiers.reason())
        ca_tag = (f" (+{RANGED_COVER_AC_BONUS} cobertura a distancia)"
                  if getattr(getattr(target, "state", None), "at_range", False) else "")
        log.append(f"  {attacker.name} -> {target.name} con {atk.name}: "
                   f"{roll}{mode_tag}+{bonus}={total} vs CA {ca_efectiva}{ca_tag}, falla")
    # Tras resolver la tirada (acierte o falle): p. ej. el ataque extra de
    # las Garras del Path of the Beast, que se dispara «cuando atacas con
    # ellas», no solo cuando impactan.
    # Maestría con Armas: solo si el arma trae clave (los monstruos/PCs sin
    # ella no invocan nada → cero coste y cero RNG).
    if str(getattr(atk, "mastery", "") or "").strip():
        from ...rules.mastery import al_acertar, al_fallar
        if hit:
            al_acertar(attacker, target, atk, damage=dmg, rango=rango,
                       ctx=ctx, rng=rng, log=log)
        else:
            al_fallar(attacker, target, atk, rango=rango, ctx=ctx,
                      rng=rng, log=log)
    _trigger_after_attack_roll(attacker, target, atk, hit, log, ctx, rng)


def _tag_modificadores(raw: int, final: int, dt: Any, target: Any, *,
                       magical: bool = False) -> str:
    """Etiqueta del log con lo que han hecho inmunidad/resistencia/vulnerabilidad.

    Se deriva del resultado de :func:`dnd_sim.rules.damage.apply_damage_modifiers`
    (así el log también refleja la resistencia de estar petrificado, que la
    regla reimplementada en ``attack_roll`` no contemplaba). Sin daño que
    modificar no hay etiqueta.

    Si el daño NO es mágico y la regla que actúa es una ``nonmagical_*``
    del objetivo, la etiqueta lo indica («resistencia a daño no mágico:
    9 -> 4»).
    """
    if int(raw) <= 0 or int(final) == int(raw):
        return ""
    inmunidades = set(getattr(target, "immunities", set()) or set())
    resistencias = set(getattr(target, "resistances", set()) or set())
    sufijo = ""
    if not magical:
        inm_nm = set(getattr(target, "nonmagical_immunities", set()) or set())
        res_nm = set(getattr(target, "nonmagical_resistances", set()) or set())
        if (dt in inm_nm and dt not in inmunidades) or (
                dt in res_nm and dt not in resistencias):
            sufijo = " a daño no mágico"
        inmunidades |= inm_nm
        resistencias |= res_nm
    if dt in inmunidades:
        return f" (inmune{sufijo})"
    resiste = dt in resistencias
    vulnerable = dt in getattr(target, "vulnerabilities", set())
    if resiste and vulnerable:
        after_resist = int(raw) // 2
        return (f" (resistencia{sufijo}: {raw} -> {after_resist})"
                f" (vulnerable: {after_resist} -> {final})")
    if resiste:
        return f" (resistencia{sufijo}: {raw} -> {final})"
    if vulnerable:
        return f" (vulnerable: {raw} -> {final})"
    # Otra regla de apply_damage_modifiers (p. ej. petrificado: resiste todo).
    return f" (resistencia{sufijo}: {raw} -> {final})"


def _actualizar_distancia(attacker, rango, log) -> None:
    """El atacante queda a distancia tras un ataque a distancia (y al revés)."""
    state = getattr(attacker, "state", None)
    if state is None:
        return
    a_distancia = rango is AttackRange.RANGED
    if getattr(state, "at_range", False) == a_distancia:
        return
    state.at_range = a_distancia
    if log is not None:
        nombre = getattr(attacker, "name", attacker)
        log.append(f"  {nombre} {'pasa a distancia' if a_distancia else 'se acerca'}")


def _apply_condition_riders(attacker, target, atk, rng, log, ctx) -> None:
    """Aplica las condiciones del ataque (si el objetivo falla la salvación)."""
    riders = list(getattr(atk, "condition_riders", None) or [])
    if not riders:
        return
    from ...rules.conditions import RepeatSave, apply_condition
    from ...rules.saves import registrar_resistencia, saving_throw

    _ctx = ctx
    if _ctx is None:
        _ctx = type("RiderCtx", (), {})()
        _ctx.rng = rng
        _ctx.log = log
        _ctx.verbose = log is not None
        _ctx.conditions_applied = None

    for rider in riders:
        repeat = None
        if rider.repeat_save:
            repeat = RepeatSave(ability=rider.save_ability, dc=rider.dc)
        if rider.save_ability is None:
            # Sin salvación: la condición se aplica al impactar.
            apply_condition(
                target, rider.condition, _ctx,
                source=attacker,
                duration_rounds=rider.duration_rounds,
                repeat_save=repeat,
                escape=rider.escape,
                magical=bool(getattr(rider, "magical", False)),
            )
            continue
        sr = saving_throw(target, rider.save_ability, rider.dc, rng,
                          magical=bool(getattr(rider, "magical", False)),
                          ctx=_ctx)
        sr = registrar_resistencia(_ctx, target, sr)
        if sr.success:
            continue
        apply_condition(
            target, rider.condition, _ctx,
            source=attacker,
            duration_rounds=rider.duration_rounds,
            repeat_save=repeat,
            escape=rider.escape,
            magical=bool(getattr(rider, "magical", False)),
        )


def _trigger_after_being_hit(target: Any, attacker: Any, rango: Any,
                             log: Any, ctx: Any, rng: Any = None) -> None:
    """Dispara los rasgos de ``target`` que reaccionan a ser golpeado.

    Hoy solo ``Heated Body`` (azer): daño de fuego a quien impacta cuerpo a
    cuerpo. El hook se ejecuta tras el daño, en **cada** impacto (aunque el
    daño haya sido 0 por inmunidad del objetivo), porque el trigger de la
    ficha es el impacto, no el daño recibido. Solo se piden los rasgos que
    sobrescriben el hook (:func:`dnd_sim.rules.traits.hooks`).
    """
    traits = getattr(target, "traits", None)
    if not traits:
        return
    from ...rules.traits import hooks
    hookable = hooks(traits, "after_being_hit")
    if not hookable:
        return
    _ctx = ctx
    if _ctx is None:
        _ctx = type("HitCtx", (), {})()
        _ctx.rng = rng
        _ctx.log = log
        _ctx.verbose = log is not None
    elif getattr(_ctx, "rng", None) is None:
        _ctx.rng = rng
    for trait in hookable:
        trait.after_being_hit(target, attacker, rango, ctx=_ctx)


def _trigger_after_dealing_hit(attacker: Any, target: Any, rango: Any,
                               log: Any, ctx: Any, rng: Any = None,
                               atk: Any = None,
                               damage: int | None = None) -> None:
    """Dispara los rasgos de ``attacker`` que reaccionan a impactar.

    Espejo de :func:`_trigger_after_being_hit` por el lado del atacante
    (p. ej. Protectores Ancestrales: marcar a la primera criatura
    golpeada en el turno; el Mordisco de la Bestia: curar). Como allí, se
    ejecuta tras el daño y en cada impacto, y solo se piden los rasgos que
    sobrescriben el hook (:func:`dnd_sim.rules.traits.hooks`). ``atk`` es
    el objeto ataque y ``damage`` el daño principal final ya aplicado.
    """
    traits = getattr(attacker, "traits", None)
    if not traits:
        return
    from ...rules.traits import hooks
    hookable = hooks(traits, "after_dealing_hit")
    if not hookable:
        return
    _ctx = ctx
    if _ctx is None:
        _ctx = type("HitCtx", (), {})()
        _ctx.rng = rng
        _ctx.log = log
        _ctx.verbose = log is not None
    elif getattr(_ctx, "rng", None) is None:
        _ctx.rng = rng
    for trait in hookable:
        trait.after_dealing_hit(target, attacker, rango, ctx=_ctx, atk=atk,
                                damage=damage)


def _trigger_after_attack_roll(attacker: Any, target: Any, atk: Any,
                               hit: bool, log: Any, ctx: Any,
                               rng: Any = None) -> None:
    """Dispara los rasgos de ``attacker`` tras su tirada de ataque.

    Se llama al final de :func:`attack_roll`, tanto si impactó como si
    falló (p. ej. el ataque extra de las Garras). Solo se piden los rasgos
    que sobrescriben el hook (:func:`dnd_sim.rules.traits.hooks`).
    """
    traits = getattr(attacker, "traits", None)
    if not traits:
        return
    from ...rules.traits import hooks
    hookable = hooks(traits, "after_attack_roll")
    if not hookable:
        return
    _ctx = ctx
    if _ctx is None:
        _ctx = type("RollCtx", (), {})()
        _ctx.rng = rng
        _ctx.log = log
        _ctx.verbose = log is not None
    elif getattr(_ctx, "rng", None) is None:
        _ctx.rng = rng
    for trait in hookable:
        trait.after_attack_roll(attacker, target, atk, hit, ctx=_ctx, rng=rng)


def _reaccion_si_procede(target: Any, ctx: Any) -> None:
    """Dispara la reacción de ``target`` si acaba de recibir daño (5e).

    El import es perezoso para evitar ciclos (``spells`` importa ``combat``
    dentro de sus funciones).
    """
    if target is None or ctx is None:
        return
    from ...rules.spells import trigger_reaction
    try:
        trigger_reaction(target, ctx)
    except Exception:
        pass

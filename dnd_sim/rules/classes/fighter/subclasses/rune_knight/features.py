"""Rasgo Rune Knight: runas, Giant's Might y sus estados.

Módulo interno del paquete ``rune_knight``: la clase
:class:`RuneKnightFeatures` (hooks de runas Fire/Stone/Hill/Frost/Storm,
Runic Shield, Cloud). Las acciones bonus viven en :mod:`actions` y el
montaje del personaje en el ``__init__`` del paquete. El docstring de
decisiones está en el paquete.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ......core.classes import (
    MIN_LEVEL,
    giants_might_die_sides,
    giants_might_uses,
    rune_uses,
    runic_shield_uses,
)
from ......core.dice import RollMode, roll_d20, roll_dice
from ......core.enums import DamageType
from ......core.log import log_line as _log_line
from ......core.proficiency import proficiency_bonus
from ......core.randomness import pick
from .....conditions import Condition, apply_condition, remove_condition
from .....damage import inflict_damage
from .....roll_modifiers import evaluar_d20
from .....saves import saving_throw
from .....traits.base import Trait

#: Resistencias temporales de Hill (patrón Bear: lista de fuente propia,
#: solo se concede lo que falte y se revoca solo lo concedido).
_HILL_RESISTENCIAS: frozenset = frozenset({
    DamageType.BLUDGEONING,
    DamageType.PIERCING,
    DamageType.SLASHING,
})


@dataclass
class RuneKnightFeatures(Trait):
    """Rasgos, runas y estados de Rune Knight.

    Sin RNG en los guards: los ``pick`` de invocación de runas se
    deciden en sus puntos de consulta con el ``rng`` del combate.
    """

    # Nivel del personaje (manda en las tablas de rasgos).
    level: int = MIN_LEVEL
    # Runas conocidas (2/3/4/5 según nivel; pool ``RUNES``).
    runas: list[str] = field(default_factory=list, repr=False,
                             compare=False)
    # Usos restantes por runa (1; 2 con Master of Runes, 15+).
    usos_runa: dict = field(default_factory=dict, repr=False,
                            compare=False)
    # Giant's Might (3): usos por descanso largo + «una vez por turno»
    # del daño extra (flag se reinicia en ``on_turn_start``).
    giants_might_usos: int = 0
    giants_might_used_this_turn: bool = False
    # Giant's Might activo (dura todo el combate; lo pone la acción).
    giants_might_activo: bool = False
    # Runic Shield (7): usos por descanso largo; la reacción compartida
    # vive en ``state.reaction_used``.
    runic_shield_usos: int = 0
    # Estados activos de runas (duración = combate; los limpia
    # ``reset``). Fire/Stone marcan objetivos en ``CombatState`` (A8/A9).
    frost_activo: bool = False
    hill_activo: bool = False
    # Resistencias B/P/C que Hill concedió (para revocarlas en reset).
    hill_concedidas: list = field(default_factory=list, repr=False,
                                  compare=False)
    storm_activo: bool = False
    # Datos sin efecto congelados (decisión del maintainer): pasivos de
    # las runas (salvo la resistencia a veneno de Hill, A7) y Bonus
    # Proficiencies (herramientas de herrero e idioma gigante).
    pasivos_runas: bool = True
    bonus_proficiencies: bool = True
    # Dueño (guards de hooks y despacho de ``on_turn_start``).
    owner: Any = field(default=None, repr=False, compare=False)

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        # «Una vez por turno» de Giant's Might (A4): se reinicia al
        # empezar el turno.
        self.giants_might_used_this_turn = False

    def reset(self) -> None:
        """Un combate nuevo = un día descansado: usos restaurados."""
        self.usos_runa = {r: rune_uses(self.level) for r in self.runas}
        self.giants_might_usos = giants_might_uses(self.level)
        self.giants_might_used_this_turn = False
        self.giants_might_activo = False
        self.runic_shield_usos = runic_shield_uses(self.level)
        self.frost_activo = False
        self._revocar_hill()
        self.hill_activo = False
        self.storm_activo = False

    # --- Giant's Might (3) ---------------------------------------------------
    def _fue_giants_might(self, habilidad: Any, sujeto: Any) -> bool:
        """¿La consulta es una prueba/salvación de FUE del dueño activo?"""
        if not self.giants_might_activo or sujeto is not self.owner:
            return False
        return str(habilidad or "").strip().lower() in ("str", "strength")

    def _bonus_frost(self, habilidad: Any, sujeto: Any) -> int:
        """Frost: +2 a pruebas y salvaciones de FUE/CON del dueño."""
        if not self.frost_activo or sujeto is not self.owner:
            return 0
        if str(habilidad or "").strip().lower() in (
                "str", "strength", "con", "constitution"):
            return 2
        return 0

    def modificar_salvacion(self, habilidad: Any, sujeto: Any,
                            ctx: Any = None) -> tuple[bool, bool, int]:
        """Giant's Might (ventaja FUE) + Frost (+2 FUE/CON), consulta A3."""
        return (self._fue_giants_might(habilidad, sujeto), False,
                self._bonus_frost(habilidad, sujeto))

    def modificar_prueba(self, habilidad: Any, sujeto: Any,
                         ctx: Any = None) -> tuple[bool, bool, int]:
        """Giant's Might (ventaja FUE) + Frost (+2 FUE/CON), consulta A3."""
        return (self._fue_giants_might(habilidad, sujeto), False,
                self._bonus_frost(habilidad, sujeto))

    def repetir_d20(self, target: Any, attacker: Any, rango: Any, *,
                    bonus: int, ctx: Any = None, rng: Any = None,
                    atk: Any = None, log: Any = None) -> Any:
        """Runic Shield (7): fuerza al atacante a repetir el d20.

        Se decide tras acertar y antes del daño (mismo punto que
        Warding Maneuver). Solo contra OTRA criatura aliada viva del
        dueño (no el propio dueño ni un enemigo), con usos y reacción
        libre; sin RNG el rasgo se abstiene. La decisión es un
        ``pick`` «no»/«sí». La repetición es UN solo d20 en modo
        normal (sin conservar la ventaja original): el motor recibe
        ``(roll, total, crit, fallo_natural)`` y reevalúa el impacto
        con la CA; el crítico y el 1 natural salen del umbral del
        atacante (``evaluar_d20``, Champion). Guard de reentrada: el
        motor la consulta una sola vez por ataque.
        """
        owner = self.owner
        if (
            self.level < 7
            or owner is None
            or target is None
            or target is owner
            or int(self.runic_shield_usos) <= 0
            or not getattr(owner, "alive", True)
            or not getattr(owner, "can_react", True)
            or getattr(getattr(owner, "state", None), "reaction_used", True)
            or rng is None
        ):
            return None
        hostil = getattr(owner, "is_hostile_to", None)
        if hostil is not None and hostil(target):
            return None
        if pick(rng, ("no", "si")) == "no":
            return None
        self.runic_shield_usos -= 1
        owner.state.reaction_used = True
        nuevo = roll_d20(rng, RollMode.NORMAL)
        roll = int(nuevo.value)
        crit, fallo_natural = evaluar_d20(roll, attacker, atk)
        total = roll + int(bonus)
        if log is not None:
            log.append(
                f"  {owner.name} hace repetir el ataque a "
                f"{getattr(attacker, 'name', attacker)} (Runic Shield): "
                f"nuevo d20 {roll} -> {total}"
            )
        return roll, total, crit, fallo_natural

    def redirigir_ataque(self, target: Any, attacker: Any, rango: Any, *,
                         ctx: Any = None, rng: Any = None,
                         atk: Any = None, log: Any = None) -> Any:
        """Cloud Rune: redirige el golpe a otro enemigo del dueño (A11).

        Se decide tras impactar y antes del daño (mismo punto que
        Warding Maneuver, mismo walker que Runic Shield pero devolviendo
        el NUEVO objetivo: roll, total y crítico los conserva el motor).
        Candidatos: enemigos vivos del dueño distintos del atacante y
        del propio objetivo; sin candidatos el rasgo se abstiene SIN
        RNG. La decisión es un ``pick`` «no»/«sí» y el objetivo se
        elige con otro ``pick`` uniforme del pool. Gasta 1 uso de cloud
        y la reacción.
        """
        owner = self.owner
        if (
            "cloud" not in self.runas
            or owner is None
            or target is None
            or attacker is None
            or int(self.usos_runa.get("cloud", 0)) <= 0
            or not getattr(owner, "alive", True)
            or not getattr(owner, "can_react", True)
            or getattr(getattr(owner, "state", None), "reaction_used", True)
            or ctx is None
            or rng is None
        ):
            return None
        pool = []
        hostil = getattr(owner, "is_hostile_to", None)
        for otro in getattr(ctx, "combatants", None) or []:
            if otro is None or otro is attacker or otro is target:
                continue
            if not getattr(otro, "alive", True):
                continue
            if hostil is None or not hostil(otro):
                continue
            pool.append(otro)
        if not pool:
            return None  # sin elegibles: cero RNG
        if pick(rng, ("no", "si")) == "no":
            return None
        nuevo = pick(rng, tuple(pool))
        self.usos_runa["cloud"] = int(self.usos_runa["cloud"]) - 1
        owner.state.reaction_used = True
        if log is not None:
            log.append(
                f"  {owner.name} redirige el ataque de "
                f"{getattr(attacker, 'name', attacker)} a "
                f"{getattr(nuevo, 'name', nuevo)} (Cloud Rune)"
            )
        return nuevo

    def grant_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                               rango: Any, ctx: Any = None,
                               rng: Any = None, atk: Any = None) -> None:
        """Storm Rune (10, reacción): ventaja/desventaja por alianza.

        Mientras la runa esté invocada, el espíritu de la tormenta
        inclina el ataque según QUIÉN ataca: aliado del dueño (o el
        propio dueño) → ventaja; enemigo → desventaja
        (``is_hostile_to``, simétrico). Decidir gastar la reacción es
        un ``pick`` uniforme (patrón Protección) y al gastarse se marca
        ``reaction_used`` (una por ronda, como el resto de reacciones).
        Sin runa invocada, reacción ya usada, dueño muerto o
        Incapacitado (``can_react``: ahí la alianza queda sin efecto)
        o sin ``rng`` → el rasgo se abstiene sin consultar azar. Sin
        posiciones, la alianza no mira distancia (dato sin efecto).
        """
        owner = self.owner
        if ("storm" not in self.runas or not self.storm_activo
                or owner is None or attacker is None):
            return None
        estado = getattr(owner, "state", None)
        if estado is not None and getattr(estado, "reaction_used", False):
            return None
        if not getattr(owner, "can_react", True):
            return None
        if rng is None:
            return None
        if pick(rng, ("no", "si")) == "no":
            return None
        if estado is not None:
            estado.reaction_used = True
        nombre = getattr(attacker, "name", attacker)
        if owner.is_hostile_to(attacker):
            mods.disadvantage_sources.append("Storm Rune")
            _log_line(ctx, f"{owner.name} invoca Storm Rune: desventaja "
                           f"para {nombre}")
        else:
            mods.advantage_sources.append("Storm Rune")
            _log_line(ctx, f"{owner.name} invoca Storm Rune: ventaja "
                           f"para {nombre}")
        return None

    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            *, crit: bool = False, ctx: Any = None,
                            rng: Any = None, atk: Any = None) -> int:
        """Giant's Might + Fire Rune al impactar con un arma (A4/A8).

        Giant's Might: 1d6 (d8 con 10, d10 con 18) una vez por turno,
        del mismo tipo que el arma (el motor lo suma al bruto). Fire
        Rune: decide su ``pick`` y aplica sus efectos aparte (tipo
        fuego, salvación y marca), así que no aporta al bruto. Sin
        ``rng``, sin ``target`` o sin ataque no se consume nada (no hay
        dados que tirar).
        """
        if (attacker is not self.owner or target is None or atk is None
                or rng is None or getattr(atk, "spell_attack", False)):
            return 0
        bonus = 0
        if (self.giants_might_activo
                and not self.giants_might_used_this_turn):
            self.giants_might_used_this_turn = True
            lados = giants_might_die_sides(self.level)
            bonus = int(roll_dice(f"1d{lados}", rng, crit=crit))
        self._fire_rune(target, ctx, rng, crit=crit)
        return bonus

    # --- Runas Hill y Frost (A7) ----------------------------------------------
    def _otorgar_hill(self, actor: Any, ctx: Any) -> None:
        """Hill: resistencias temporales B/P/C (patrón Bear)."""
        previas = set(getattr(actor, "resistances", None) or set())
        nuevas = [t for t in sorted(_HILL_RESISTENCIAS, key=lambda t: t.value)
                  if t not in previas]
        if not nuevas:
            return
        actor.resistances = previas | set(nuevas)
        for tipo in nuevas:
            self.hill_concedidas.append((actor, tipo))
        _log_line(ctx, f"  {getattr(actor, 'name', actor)} gana "
                       f"resistencia a "
                       f"{', '.join(t.value for t in nuevas)} (Hill)")

    def _revocar_hill(self) -> None:
        """Retira SOLO las resistencias que Hill concedió."""
        for objeto, tipo in self.hill_concedidas:
            resis = getattr(objeto, "resistances", None)
            if resis is not None:
                resis.discard(tipo)
        self.hill_concedidas.clear()

    # --- Fire Rune (A8) --------------------------------------------------------
    def _cd_runa(self) -> int:
        """CD de las salvaciones de Fire y Stone: 8 + PB + mod CON."""
        owner = self.owner
        mod_con = owner.abilities.mod("con") if owner is not None else 0
        return 8 + proficiency_bonus(self.level) + int(mod_con)

    def _fire_rune(self, target: Any, ctx: Any, rng: Any, *,
                   crit: bool = False) -> None:
        """Fire Rune: 2d6 de fuego + salvación de FUE al impactar (A8).

        Guards sin RNG (runa desconocida, sin usos, dueño
        incapacitado o sin ``rng``); el ``pick`` solo se consulta al
        gastar. Si la salvación falla, el objetivo queda Restringido
        con marca en su ``CombatState`` hasta que supere la salvación
        de fin de turno. Sin ``escape`` en la condición: es efecto de
        la runa, no un agarre, así que ninguna prueba lo rompe.
        """
        owner = self.owner
        if ("fire" not in self.runas or target is None
                or int(self.usos_runa.get("fire", 0)) <= 0
                or not getattr(owner, "can_act", True) or rng is None):
            return  # sin elegibilidad: ni consulta ni RNG
        if pick(rng, ("no", "si")) == "no":
            return
        self.usos_runa["fire"] = int(self.usos_runa["fire"]) - 1
        extra = int(roll_dice("2d6", rng, crit=crit))
        inflict_damage(target, extra, DamageType.FIRE, source=owner,
                       ctx=ctx, rng=rng)
        _log_line(ctx, f"  {getattr(owner, 'name', owner)} invoca la "
                       f"Fire Rune: {extra} de daño de fuego")
        sr = saving_throw(target, "str", self._cd_runa(), rng, ctx=ctx)
        if sr.success:
            return  # la salvación de la invocación no restringe
        estado = getattr(target, "state", None)
        if estado is None:
            return
        ronda = int(getattr(ctx, "round", 1) or 1) if ctx is not None else 1
        # Una sola marca por objetivo: la caducidad se refresca pero la
        # condición solo se aplica la primera vez (sin apilar instancias).
        ya_marcado = getattr(estado, "fire_runa", None) is not None
        estado.fire_runa = owner
        estado.fire_runa_hasta = ronda + 100
        if not ya_marcado:
            apply_condition(target, Condition.RESTRAINED, ctx, source=owner)
        _log_line(ctx, f"  {getattr(target, 'name', target)} queda "
                       f"Restringido (Fire Rune)")

    def _limpiar_fire(self, target: Any) -> None:
        """Retira la marca de Fire y la condición del objetivo."""
        estado = getattr(target, "state", None)
        if estado is not None:
            estado.fire_runa = None
            estado.fire_runa_hasta = 0
        if (getattr(target, "conditions", None) is not None
                and target.conditions.has(Condition.RESTRAINED)):
            remove_condition(target, Condition.RESTRAINED, None)

    @staticmethod
    def _fire_vigente(target: Any, ctx: Any) -> Any:
        """Marca de Fire vigente sobre ``target`` (o ``None``)."""
        estado = getattr(target, "state", None)
        marca = getattr(estado, "fire_runa", None)
        if marca is None or estado is None:
            return None
        if ctx is not None:
            ronda = int(getattr(ctx, "round", 0) or 0)
            if ronda > int(getattr(estado, "fire_runa_hasta", 0) or 0):
                return None  # caducada (~1 minuto)
        return marca

    def on_any_turn_start(self, actor: Any, ctx: Any = None) -> None:
        """Dispatch A8/A9: marcas de Fire y Stone al inicio del turno.

        Los objetivos muertos no tienen turno propio, así que se barren
        en el turno del dueño de la runa (ambas marcas).
        """
        if actor is self.owner:
            for otro in getattr(ctx, "combatants", None) or []:
                estado = getattr(otro, "state", None)
                if (otro is actor or estado is None
                        or getattr(otro, "alive", True)):
                    continue
                if getattr(estado, "fire_runa", None) is self.owner:
                    self._limpiar_fire(otro)
                if getattr(estado, "stone_de", None) is self.owner:
                    self._limpiar_stone(otro)
        self._fire_al_inicio(actor, ctx)
        self._stone_al_inicio(actor, ctx)

    def on_any_turn_end(self, actor: Any, ctx: Any = None) -> None:
        """Dispatch A8/A9: Fire salva y Stone invoca al final del turno."""
        self._fire_al_fin(actor, ctx)
        self._stone_al_fin(actor, ctx)

    def _fire_al_inicio(self, actor: Any, ctx: Any = None) -> None:
        """Marca de Fire: limpieza y daño de 2d6 al inicio del turno (A8)."""
        estado = getattr(actor, "state", None)
        if (estado is None
                or getattr(estado, "fire_runa", None) is not self.owner):
            return
        if not getattr(actor, "alive", True) or (
                ctx is not None and self._fire_vigente(actor, ctx) is None):
            self._limpiar_fire(actor)
            return
        rng = getattr(ctx, "rng", None) if ctx is not None else None
        if rng is None:
            return  # sin RNG no hay dados
        extra = int(roll_dice("2d6", rng))
        inflict_damage(actor, extra, DamageType.FIRE, source=self.owner,
                       ctx=ctx, rng=rng)
        _log_line(ctx, f"  {getattr(actor, 'name', actor)} sufre "
                       f"{extra} de daño de fuego (Fire Rune)")

    def _fire_al_fin(self, actor: Any, ctx: Any = None) -> None:
        """Fire Rune: salvación de FUE al final del turno (A8)."""
        estado = getattr(actor, "state", None)
        if (estado is None
                or getattr(estado, "fire_runa", None) is not self.owner):
            return
        if not getattr(actor, "alive", True) or (
                ctx is not None and self._fire_vigente(actor, ctx) is None):
            self._limpiar_fire(actor)
            return
        rng = getattr(ctx, "rng", None) if ctx is not None else None
        if rng is None:
            return  # sin RNG no se tira: el efecto sigue vigente
        sr = saving_throw(actor, "str", self._cd_runa(), rng, ctx=ctx)
        if sr.success:
            self._limpiar_fire(actor)
            _log_line(ctx, f"  {getattr(actor, 'name', actor)} supera la "
                           f"Fire Rune")

    # --- Stone Rune (A9) ---------------------------------------------------

    def _limpiar_stone(self, target: Any) -> None:
        """Retira la marca de Stone y SUS condiciones (fuente = dueño).

        Filtra por ``source is self.owner``: no toca instancias de
        Hechizado/Incapacitado puestas por otra fuente.
        """
        tracker = getattr(target, "conditions", None)
        if tracker is not None:
            for instancia in list(tracker.instances):
                if (instancia.condition in (Condition.CHARMED,
                                            Condition.INCAPACITATED)
                        and instancia.source is self.owner):
                    tracker.remove_instance(instancia)
        estado = getattr(target, "state", None)
        if estado is not None:
            estado.stone_de = None
            estado.stone_pg = 0

    def _stone_al_fin(self, actor: Any, ctx: Any = None) -> None:
        """Stone Rune: invocación al acabar el turno de un enemigo (A9).

        Guards sin RNG (runa desconocida, propio turno, muerto, sin
        usos, dueño incapacitado, no hostil, ya Hechizado o sin
        ``rng``); el ``pick`` solo se consulta al gastar. La salvación
        de SAB con CD de runa; al fallar: Hechizado + Incapacitado con
        marca ``stone_de``/``stone_pg``. Sin distancia: el modelo no
        guarda posiciones (decisión documentada en PASOS).
        """
        owner = self.owner
        if ("stone" not in self.runas or actor is None or actor is owner
                or not getattr(actor, "alive", True)
                or int(self.usos_runa.get("stone", 0)) <= 0
                or not getattr(owner, "can_act", True)):
            return  # sin elegibilidad: ni consulta ni RNG
        hostil = getattr(owner, "is_hostile_to", None)
        if hostil is None or not hostil(actor):
            return  # solo enemigos del dueño
        tracker = getattr(actor, "conditions", None)
        if tracker is not None and tracker.has(Condition.CHARMED):
            return  # una sola vez: no repite mientras esté Hechizado
        rng = getattr(ctx, "rng", None) if ctx is not None else None
        if rng is None:
            return
        if pick(rng, ("no", "si")) == "no":
            return
        self.usos_runa["stone"] = int(self.usos_runa["stone"]) - 1
        sr = saving_throw(actor, "wis", self._cd_runa(), rng, ctx=ctx)
        if sr.success:
            return  # la salvación de la invocación no hechiza
        estado = getattr(actor, "state", None)
        if estado is None:
            return
        estado.stone_de = owner
        estado.stone_pg = int(getattr(actor, "hp", 0) or 0)
        apply_condition(actor, Condition.CHARMED, ctx, source=owner)
        apply_condition(actor, Condition.INCAPACITATED, ctx, source=owner)
        _log_line(ctx, f"  {getattr(actor, 'name', actor)} queda Hechizado "
                       f"e Incapacitado (Stone Rune)")

    def _stone_al_inicio(self, actor: Any, ctx: Any = None) -> None:
        """Stone: retirada por daño al empezar el turno del marcado (A9)."""
        estado = getattr(actor, "state", None)
        if (estado is None
                or getattr(estado, "stone_de", None) is not self.owner):
            return
        if not getattr(actor, "alive", True):
            self._limpiar_stone(actor)
            return
        if (int(getattr(actor, "hp", 0) or 0)
                < int(getattr(estado, "stone_pg", 0) or 0)):
            self._limpiar_stone(actor)
            _log_line(ctx, f"  {getattr(actor, 'name', actor)} recupera el "
                           f"control (Stone Rune: ha recibido daño)")


__all__ = ["RuneKnightFeatures"]

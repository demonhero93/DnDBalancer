"""Rasgo Battle Master: maniobras, dados de superioridad y decisiones.

Módulo interno del paquete ``battle_master``: la clase
:class:`BattleMasterFeatures` (punto de decisión único por ataque,
parry/riposte/commander, salvaciones de maniobras) y sus helpers.
Las acciones bonus viven en :mod:`actions` y el montaje del personaje
en el ``__init__`` del paquete. El docstring de decisiones de
simulación está en el paquete.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any

from ......core.classes import MIN_LEVEL, superiority_dice_count
from ......core.dice import roll_dice
from ......core.enums import AttackRange, parse_damage_type
from ......core.log import log_line as _log_line
from ......core.proficiency import proficiency_bonus
from ......core.randomness import pick
from ......core.targeting import valid_targets
from .....conditions import Condition, EscapeCheck, apply_condition
from .....damage import apply_damage_modifiers, inflict_damage
from .....roll_modifiers import effective_ac, evaluar_d20
from .....saves import registrar_resistencia, saving_throw
from .....traits.base import AtaqueSustituido, Trait
from ..._util import _TAMANOS, _orden_tamano
from ...features import _es_aliado

#: Maniobras que se ejecutan al impactar (punto de decisión único).
#: Feinting es acción bonus (A5) y no entra aquí.
MANEUVERS_ON_HIT: tuple[str, ...] = (
    "Disarming Attack",
    "Distracting Strike",
    "Goading Attack",
    "Lunging Attack",
    "Maneuvering Attack",
    "Menacing Attack",
    "Pushing Attack",
    "Sweeping Attack",
    "Trip Attack",
)

#: Maniobras solo para ataques cuerpo a cuerpo (el alcance extra de
#: Lunging y la geometría de Sweeping no están en el modelo).
MANEUVERS_MELEE_ONLY: frozenset[str] = frozenset(
    {"Lunging Attack", "Sweeping Attack"})

#: Maniobras que se ejecutan tras un FALLO (solo Precision hoy).
MANEUVERS_ON_MISS: tuple[str, ...] = ("Precision Attack",)


def _armas_propias(criatura: Any) -> tuple:
    """Armas propias: ``attacks``, o ``weapons`` + ``dynamic_weapons``."""
    ataques = list(getattr(criatura, "attacks", None) or []) or (
        list(getattr(criatura, "weapons", None) or [])
        + list(getattr(criatura, "dynamic_weapons", None) or []))
    return tuple(ataques)


def _armas_melee_propias(criatura: Any) -> tuple:
    """Armas cuerpo a cuerpo propias (patrón ``_armas_melee_de`` de Retaliation).

    Sin candidatas → pool vacío: la maniobra de reacción no es
    elegible (SIN RNG), a diferencia de Retaliation, que cae en golpe
    sin armas.
    """
    return tuple(a for a in _armas_propias(criatura)
                 if getattr(a, "range_type", AttackRange.MELEE)
                 is not AttackRange.RANGED)


def _aliados(owner: Any, ctx: Any) -> tuple:
    """Aliados vivos no hostiles distintos del dueño (sin RNG)."""
    return tuple(c for c in (getattr(ctx, "combatants", None) or ())
                 if _es_aliado(owner, c))


def _aliados_elegibles(owner: Any, ctx: Any) -> tuple:
    """Aliados que pueden recibir Commander's Strike (sin RNG).

    Filtros: vivo, no el dueño, no hostil (``_aliados``), con
    reacción disponible y con qué atacar (algún arma y algún enemigo
    objetivo).
    """
    aliados = []
    for c in _aliados(owner, ctx):
        if not getattr(c, "can_react", True):
            continue
        if getattr(getattr(c, "state", None), "reaction_used", False):
            continue
        if not _armas_propias(c):
            continue
        if not valid_targets(c, ctx):
            continue
        aliados.append(c)
    return tuple(aliados)


@dataclass
class BattleMasterFeatures(Trait):
    """Features de la subclase y estado de Combat Superiority."""

    # Nivel del personaje (manda en las tablas de la subclase).
    level: int = MIN_LEVEL
    # Dados de superioridad restantes (se rellenan en ``reset``).
    dados_restantes: int = 0
    # Caras del dado de superioridad del PJ (8/10/12 según nivel).
    dados_lados: int = 8
    #: Maniobras conocidas (nombres de :data:`BATTLE_MASTER_MANEUVERS`).
    maneuvers: list[str] = field(default_factory=list, repr=False,
                                 compare=False)
    #: ¿Ya se usó Relentless en el turno actual? (una vez por turno).
    relentless_used_this_turn: bool = False
    #: Know Your Enemy (7): dato sin efecto (sin IA que lo use).
    know_your_enemy: bool = False
    #: Competencia ganada con Student of War ("" si no había candidatas).
    competencia: str = ""
    #: Juego de herramientas de artesano (dato sin efecto).
    herramientas: str = "herramientas de artesano"
    #: Maniobra de impacto decidida y aún no ejecutada (se limpia en
    #: ``on_turn_start`` si el ataque no la resolvió).
    maniobra_pendiente: str | None = field(
        default=None, repr=False, compare=False)
    #: TOTAL de la tirada original, para que Sweeping compare su CA.
    maniobra_total: int = 0
    #: Feinting Attack (acción bonus): el siguiente ataque de este turno
    #: tiene ventaja y, si impacta, su dado se aplica (se limpia en
    #: ``on_turn_start``; el punto de decisión consume la ranura).
    feinting_pendiente: bool = False
    #: Dueño (para que ``reset`` pueda apagar los flags en el combatiente).
    owner: Any = field(default=None, repr=False, compare=False)

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        # «Una vez por turno» de Relentless: se reinicia al empezar el turno.
        self.relentless_used_this_turn = False
        # Feinting caduca al fin de su turno y una pendiente sin resolver
        # no viaja al turno siguiente.
        self.feinting_pendiente = False
        self.maniobra_pendiente = None

    def reset(self) -> None:
        """Un combate nuevo = un día descansado: dados de superioridad llenos."""
        self.dados_restantes = superiority_dice_count(self.level)
        self.relentless_used_this_turn = False
        self.feinting_pendiente = False
        self.maniobra_pendiente = None
        self.maniobra_total = 0

    # --- Punto de decisión único por ataque (3) --------------------------------
    def _elegibles(self, target: Any, rango: Any, ctx: Any) -> tuple[str, ...]:
        """Maniobras de impacto conocidas elegibles en este ataque.

        Filtros sin RNG: solo las de impacto conocidas; cuerpo a cuerpo
        para Lunging/Sweeping (sin geometría) y Sweeping exige OTRO
        enemigo vivo (sin elegibles, la maniobra sale del pool).
        """
        elegibles = []
        for m in self.maneuvers:
            if m not in MANEUVERS_ON_HIT:
                continue
            if m in MANEUVERS_MELEE_ONLY and rango is not AttackRange.MELEE:
                continue
            if m == "Sweeping Attack" and not self._otro_enemigo(ctx, target):
                continue
            elegibles.append(m)
        return tuple(elegibles)

    def _otro_enemigo(self, ctx: Any, target: Any) -> Any:
        """Primer enemigo vivo distinto de ``target`` (o None; sin RNG)."""
        for c in valid_targets(self.owner, ctx):
            if c is not target:
                return c
        return None

    def decidir_maniobra(self, attacker: Any, target: Any, atk: Any,
                         rango: Any, *, roll: int, total: int, ca: int,
                         hit: bool, ctx: Any = None, rng: Any = None,
                         log: Any = None) -> tuple[bool, int]:
        """Decisión ÚNICA de maniobra de este ataque (patrón Arcane Shot).

        Lo llama el motor en el paso 6b de ``attack_roll`` (duck-typing,
        ``_decidir_maniobra``). Guards primero (sin datos, pendiente sin
        resolver, Feinting encolado o sin rng → ``None`` SIN RNG; en
        fallo, de momento sin elegibles → SIN RNG: Precision entra en
        A6). Con elegibles: ``pick`` «no»/«sí» y ``pick`` uniforme entre
        las maniobras conocidas; la maniobra se guarda en
        ``maniobra_pendiente`` y su dado SOLO se gasta al ejecutarse
        (``extra_attack_damage``). Una maniobra como máximo por ataque.
        """
        if (attacker is not self.owner
                or target is None
                or rng is None
                or getattr(ctx, "is_reaction", False)):
            return hit, total
        if self.feinting_pendiente:
            # Este ataque es el de Feinting: consume la ranura (una
            # maniobra por ataque) y, si impacta, su dado se aplica en
            # ``extra_attack_damage``. Sin RNG en esta rama.
            self.feinting_pendiente = False
            if hit and self.maniobra_pendiente is None:
                self.maniobra_pendiente = "Feinting Attack"
                self.maniobra_total = total
            return hit, total
        if (self.dados_restantes <= 0
                or self.maniobra_pendiente is not None):
            return hit, total
        if not hit:
            # Precision Attack (fallo): suma el dado a la tirada y, si
            # ahora llega a la CA, el ataque impacta. Se ejecuta aquí
            # (una maniobra por ataque; el dado NO se suma al daño).
            if evaluar_d20(roll, attacker, atk)[1]:
                return hit, total  # 1 natural: nunca (sin RNG)
            elegibles = tuple(
                m for m in self.maneuvers
                if m in MANEUVERS_ON_MISS
                and total + self.dados_lados >= ca)
            if not elegibles or pick(rng, ("no", "si")) == "no":
                return hit, total  # sin elegibles: cero RNG
            opcion = pick(rng, elegibles)
            valor, gastar = self._tirar_dado(rng)
            total += valor
            hit = total >= ca  # roll != 1 ya comprobado
            sufijo = "" if gastar else " (Relentless: sin gastar dado)"
            _log_line(ctx, f"Battle Master ({opcion}): +{valor} a la "
                           f"tirada (total {total}){sufijo}")
            return hit, total
        elegibles = self._elegibles(target, rango, ctx)
        if not elegibles:
            return hit, total  # sin elegibles: cero RNG
        if pick(rng, ("no", "si")) == "no":
            return hit, total
        self.maniobra_pendiente = pick(rng, elegibles)
        self.maniobra_total = total
        return hit, total

    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            *, crit: bool = False, ctx: Any = None,
                            rng: Any = None, atk: Any = None) -> int:
        """Ejecuta la maniobra pendiente al impactar: gasta el dado.

        La decisión ya se tomó en ``decidir_maniobra``; aquí se tira el
        dado de superioridad UNA vez (con la misma regla de críticos que
        los dados extra del motor: ``crit`` lo duplica), se gasta el
        dado —salvo Relentless, que tira 1d8 sin gastar— y se suma al
        daño. Las salvaciones/condiciones (A4), marcas (A5) y Sweeping
        (A6) se resuelven con la MISMA tirada. Sin pendiente, sin
        datos, sin rng o si el atacante no es el dueño → 0 SIN RNG.
        """
        if (attacker is not self.owner
                or target is None
                or self.maniobra_pendiente is None
                or self.dados_restantes <= 0
                or rng is None):
            return 0
        opcion = self.maniobra_pendiente
        self.maniobra_pendiente = None  # se ejecuta una sola vez
        valor, gastar = self._tirar_dado(rng, crit=crit)
        if opcion == "Sweeping Attack":
            # Sweeping: el dado NO se suma al golpe propio; se reparte al
            # segundo objetivo si el TOTAL original cubre su CA.
            self._ejecutar_sweeping(target, valor, ctx, rng, atk)
            sufijo = "" if gastar else " (Relentless: sin gastar dado)"
            _log_line(ctx, f"Battle Master (Sweeping Attack): {valor} al "
                           f"segundo objetivo{sufijo}")
            return 0
        # A5: marcas Distracting/Goading (Goading se MARCA en su rama de
        # salvación; su consumo vive en consumir_marcas).
        sufijo = "" if gastar else " (Relentless: sin gastar dado)"
        _log_line(ctx, f"Battle Master ({opcion}): +{valor} de daño{sufijo}")
        self._efecto_de_maniobra(opcion, target, ctx, rng)
        return valor

    # --- Parry (reacción, sesión 2): reduce el daño recibido --------------------
    def reducir_dano_recibido(self, attacker: Any, rango: Any, dmg: int,
                              *, ctx: Any, rng: Any, log: Any) -> int:
        """Parry: gasta reacción y dado para reducir un golpe cuerpo a cuerpo.

        Lo llama el motor (duck-typing ``_reducir_dano_recibido``) justo
        ANTES de ``inflict_damage``, con el dueño como objetivo. Guards
        SIN RNG: sin daño, sin atacante, sin rng, rango no cuerpo a
        cuerpo, sin la maniobra conocida, sin dueño vivo o capaz de actuar,
        reacción ya usada o sin dados (y sin Relentless disponible).
        Decisión ``pick`` «no»/«sí» («no» no gasta nada); el dado se tira
        UNA vez y resta ``dado + max(mod FUE, mod DES)`` al daño ya
        modificado (mínimo 0). Gasta la reacción siempre que se usa;
        Relentless solo evita gastar el dado. Orden documentado: las
        resistencias/vulnerabilidades ya se aplicaron, Parry reduce el
        resultado final.
        """
        owner = self.owner
        if (dmg <= 0 or attacker is None or rng is None
                or rango is not AttackRange.MELEE
                or "Parry" not in self.maneuvers
                or owner is None or not owner.alive or not owner.can_act):
            return dmg
        if owner.state.reaction_used:
            return dmg
        if (self.dados_restantes <= 0
                and not (self.level >= 15
                         and not self.relentless_used_this_turn)):
            return dmg
        if pick(rng, ("no", "si")) == "no":
            return dmg
        owner.state.reaction_used = True
        valor, gastar = self._tirar_dado(rng)
        mod = max(int(owner.abilities.mod("str")),
                  int(owner.abilities.mod("dex")))
        reducido = max(0, dmg - (valor + mod))
        sufijo = "" if gastar else " (Relentless: sin gastar dado)"
        _log_line(ctx, f"Battle Master (Parry): {dmg} -> {reducido} de "
                       f"daño (-{valor + mod}){sufijo}")
        return reducido

    # --- Riposte (reacción, sesión 2): contraataque al fallo --------------------
    def reaccionar_al_fallo(self, attacker: Any, rango: Any, *,
                            ctx: Any, rng: Any, log: Any) -> None:
        """Riposte: ataque de reacción cuando el enemigo FALLA cuerpo a cuerpo.

        Lo llama el motor (duck-typing ``_reaccionar_al_fallo``) tras la
        rama de fallo de ``attack_roll``, con el dueño como objetivo.
        Guards SIN RNG: sin ctx/rng, rango no cuerpo a cuerpo, sin la
        maniobra, sin armas cuerpo a cuerpo propias (pool vacío: sin
        fallback a golpe sin armas), dueño muerto/no capaz de actuar,
        atacante muerto o a distancia, reacción ya usada o sin dados (y
        sin Relentless). Decisión ``pick`` «no»/«sí» («no» no gasta
        nada); arma con ``pick`` uniforme (sin RNG si solo hay una);
        gasta la reacción y tira el dado UNA vez: su valor viaja en
        ``ctx.dano_reaccion`` y ``daño_base_arma`` lo suma SOLO si el
        ataque de reacción impacta (plano: no se duplica en crítico).
        El contraataque marca ``is_reaction``: no activa maniobras de la
        sesión 1 (guard de reentrada en ``decidir_maniobra``).
        """
        owner = self.owner
        if (ctx is None or rng is None or rango is not AttackRange.MELEE
                or "Riposte" not in self.maneuvers
                or owner is None or attacker is None
                or not owner.alive or not owner.can_act
                or not attacker.alive
                or getattr(attacker.state, "at_range", False)):
            return
        estado = owner.state
        if estado.reaction_used:
            return
        if (self.dados_restantes <= 0
                and not (self.level >= 15
                         and not self.relentless_used_this_turn)):
            return
        armas = _armas_melee_propias(owner)
        if not armas:
            return  # sin cuerpo a cuerpo propio: sin RNG
        if pick(rng, ("no", "si")) == "no":
            return
        arma = armas[0] if len(armas) == 1 else pick(rng, armas)
        estado.reaction_used = True
        valor, gastar = self._tirar_dado(rng)
        sufijo = "" if gastar else " (Relentless: sin gastar dado)"
        _log_line(ctx, f"Battle Master (Riposte): ataque de reacción con "
                       f"{getattr(arma, 'name', arma)} (+{valor}){sufijo}")
        from ......engine.combat import attack_roll
        r_ctx = copy.copy(ctx)
        r_ctx.is_reaction = True
        r_ctx.dano_reaccion = valor
        attack_roll(owner, attacker, arma, rng,
                    log=getattr(ctx, "log", log), ctx=r_ctx)

    # --- Commander's Strike (4): el aliado ataca con tu dado -------------------
    def sustituir_ataque(self, attacker: Any, target: Any, atk: Any,
                         rango: Any, *, ctx: Any = None,
                         rng: Any = None) -> Any:
        """Commander's Strike: sustituye el ataque del dueño por el de un aliado.

        Lo llama el motor en el paso 2b de ``attack_roll`` (duck-typing),
        ANTES de la tirada. Guards SIN RNG: sin ctx/rng, el ataque es de
        reacción (en el sim, todo ataque del dueño fuera de su turno),
        maniobra no conocida, otra maniobra ya encolada (una por ataque),
        sin dados (y sin Relentless) o sin aliado elegible (vivo, no el
        dueño, no hostil, con reacción libre, con arma y con enemigo).

        Decisión ``pick`` «no»/«sí» («no» no gasta nada); luego ``pick``
        uniforme de aliado, de su objetivo y de su arma (sin RNG con una
        sola opción). Gasta un dado del DUEÑO (Relentless incluido) y la
        REACCIÓN del ALIADO; el valor viaja en ``ctx.dano_reaccion`` y
        ``daño_base_arma`` lo suma SOLO si el ataque aliado impacta.
        Devuelve ``AtaqueSustituido``: el ataque del dueño no se tira
        (sin d20, sin maestrías).

        Sesgo documentado: la decisión es PREVIA a la tirada (a diferencia
        de las maniobras de impacto, que ven el resultado), así que no es
        equiprobable respecto a ellas. El ataque aliado lleva
        ``is_reaction``: no activa maniobras de la sesión 1 ni cede
        reentrada a Commander's Strike (guard propio).
        """
        owner = self.owner
        if (owner is None or attacker is None or target is None
                or ctx is None or rng is None
                or attacker is not owner
                or getattr(ctx, "is_reaction", False)
                or "Commander's Strike" not in self.maneuvers
                or self.maniobra_pendiente is not None
                or self.feinting_pendiente
                or (self.dados_restantes <= 0
                    and not (self.level >= 15
                             and not self.relentless_used_this_turn))):
            return None
        aliados = _aliados_elegibles(owner, ctx)
        if not aliados:
            return None  # sin aliado elegible: cero RNG
        if pick(rng, ("no", "si")) == "no":
            return None
        aliado = aliados[0] if len(aliados) == 1 else pick(rng, aliados)
        objetivos = valid_targets(aliado, ctx)
        if not objetivos:
            return None  # no debería ocurrir (ya filtrado): sin RNG
        objetivo = objetivos[0] if len(objetivos) == 1 else pick(
            rng, objetivos)
        armas = _armas_propias(aliado)
        if not armas:
            return None  # no debería ocurrir (ya filtrado): sin RNG
        arma = armas[0] if len(armas) == 1 else pick(rng, armas)
        valor, gastar = self._tirar_dado(rng)
        aliado.state.reaction_used = True
        sufijo = "" if gastar else " (Relentless: sin gastar dado)"
        _log_line(ctx, f"Battle Master (Commander's Strike): "
                       f"{getattr(aliado, 'name', aliado)} ataca a "
                       f"{getattr(objetivo, 'name', objetivo)} (+{valor})"
                       f"{sufijo}")
        from ......engine.combat import attack_roll
        r_ctx = copy.copy(ctx)
        r_ctx.is_reaction = True
        r_ctx.dano_reaccion = valor
        attack_roll(aliado, objetivo, arma, rng,
                    log=getattr(ctx, "log", None), ctx=r_ctx)
        return AtaqueSustituido(motivo="Commander's Strike")

    # --- Ambush (3): dado de superioridad a la iniciativa --------------------
    def bonus_iniciativa(self, *, rng: Any = None) -> int:
        """Ambush: un dado de superioridad añadido a la tirada de iniciativa.

        Lo consulta ``roll_initiative`` (duck-typing, sin imports de
        rules en el motor). Guards SIN RNG: sin ``rng``, maniobra no
        conocida o sin dados (y sin Relentless). Después ``pick``
        «no»/«sí» («no» no gasta nada) y ``_tirar_dado``. La parte de
        Sigilo de la maniobra es dato sin efecto: el motor no tira
        habilidades. Sin log: la iniciativa corre sin ``ctx``.
        """
        if (rng is None or "Ambush" not in self.maneuvers
                or (self.dados_restantes <= 0
                    and not (self.level >= 15
                             and not self.relentless_used_this_turn))):
            return 0
        if pick(rng, ("no", "si")) == "no":
            return 0
        valor, _ = self._tirar_dado(rng)
        return valor

    def _tirar_dado(self, rng: Any, *, crit: bool = False) -> tuple[int, bool]:
        """Tira el dado de la maniobra y gasta el uso.

        Relentless (15): ``pick`` «no»/«sí» (sin RNG por debajo del
        nivel 15 o si ya se usó este turno); si es «sí» tira 1d8
        —siempre d8, aunque el dado del PJ sea mayor— y NO gasta nada.
        Devuelve ``(valor, gastado)``. El dado sigue la regla de
        críticos del motor (``crit`` lo duplica).
        """
        if (self.level >= 15 and not self.relentless_used_this_turn
                and pick(rng, ("no", "si")) == "si"):
            self.relentless_used_this_turn = True
            return int(roll_dice("1d8", rng, crit=crit)), False
        self.dados_restantes -= 1
        return int(roll_dice(f"1d{self.dados_lados}", rng, crit=crit)), True

    def _ejecutar_sweeping(self, target: Any, valor: int, ctx: Any,
                           rng: Any, atk: Any) -> None:
        """Sweeping: daño = dado al segundo enemigo si el TOTAL cubre su CA.

        Shortcut: si la tirada original no llega a la CA efectiva del
        segundo objetivo no hay daño (el dado ya se gastó al usar la
        maniobra). Sin segundo objetivo no hace nada.
        """
        segundo = self._otro_enemigo(ctx, target)
        if segundo is None:
            return  # sin elegibles no se decide (no debería llegar)
        if self.maniobra_total < effective_ac(segundo):
            _log_line(ctx, f"Sweeping Attack: la tirada no cubre la CA de "
                           f"{getattr(segundo, 'name', segundo)}")
            return
        tipo = parse_damage_type(getattr(atk, "damage_type", None) or "")
        magical = bool(getattr(atk, "magical", False))
        cantidad = apply_damage_modifiers(valor, tipo, segundo,
                                          magical=magical)
        inflict_damage(segundo, cantidad, tipo, source=self.owner, ctx=ctx,
                       rng=rng, magical=magical)
        _log_line(ctx, f"Sweeping Attack: {cantidad} de daño a "
                       f"{getattr(segundo, 'name', segundo)}")

    # --- Feinting Attack (5): ventaja en el siguiente ataque ------------------
    def modify_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                                rango: Any, ctx: Any = None,
                                rng: Any = None, atk: Any = None) -> None:
        """Feinting: ventaja mientras la marca siga encolada.

        El hook se despacha en cada tirada; la consume
        ``decidir_maniobra`` (una sola vez, justo después de la tirada),
        así que solo el SIGUIENTE ataque de este turno la recibe.
        """
        if attacker is not self.owner or not self.feinting_pendiente:
            return None
        mods.advantage_sources.append("Feinting Attack")
        return None

    # --- Salvaciones y condiciones de las maniobras (4) ------------------------
    def _cd(self) -> int:
        """CD de las maniobras: 8 + PB + max(mod FUE, mod DES)."""
        owner = self.owner
        if owner is None:
            return 8
        mod = max(int(owner.abilities.mod("str")),
                  int(owner.abilities.mod("dex")))
        return 8 + proficiency_bonus(self.level) + mod

    def _efecto_de_maniobra(self, opcion: str, target: Any, ctx: Any,
                            rng: Any) -> None:
        """Salvación y efecto de la maniobra ejecutada (tras el dado).

        Cada rama tira su propia salvación con la CD del rasgo; el dado
        de superioridad ya está tirado (``extra_attack_damage``) y no se
        vuelve a tirar. Efectos sin implementación (objeto soltado,
        empuje) son solo log + ``# TODO``: no alteran el combate.
        Lunging/Maneuvering son solo daño (sin alcance ni movimiento).
        """
        if opcion == "Disarming Attack":
            sr = saving_throw(target, "str", self._cd(), rng)
            registrar_resistencia(ctx, target, sr)
            if not sr.success:
                # TODO: el sim no modela objetos: solo la salvación.
                _log_line(ctx, f"{getattr(target, 'name', target)} suelta "
                               f"un objeto (dato sin efecto)")
        elif opcion == "Goading Attack":
            sr = saving_throw(target, "wis", self._cd(), rng)
            registrar_resistencia(ctx, target, sr)
            ronda = getattr(ctx, "round", None)
            estado = getattr(target, "state", None)
            if not sr.success and ronda is not None and estado is not None:
                # shortcut: caduca a las 2 rondas («hasta el final de tu
                # siguiente turno»); la desventaja vive en el SUJETO y se
                # consume en consumir_marcas (A5).
                estado.goading[self.owner.name] = ronda + 2
        elif opcion == "Menacing Attack":
            sr = saving_throw(target, "wis", self._cd(), rng)
            registrar_resistencia(ctx, target, sr)
            if not sr.success:
                # «Hasta el final de tu siguiente turno» ≈ 2 rondas del
                # afectado (mismo criterio que Banishing/Intimidating).
                apply_condition(target, Condition.FRIGHTENED, ctx,
                                source=self.owner, duration_rounds=2)
        elif opcion == "Pushing Attack":
            sr = saving_throw(target, "str", self._cd(), rng)
            registrar_resistencia(ctx, target, sr)
            if not sr.success:
                # TODO: el empuje de 15 ft no está modelado (sin movimiento).
                _log_line(ctx, f"{getattr(target, 'name', target)} es "
                               f"empujado 15 ft (dato sin efecto)")
        elif opcion == "Trip Attack":
            if _orden_tamano(target) <= _TAMANOS.index("large"):
                sr = saving_throw(target, "str", self._cd(), rng)
                registrar_resistencia(ctx, target, sr)
                if not sr.success:
                    apply_condition(
                        target, Condition.PRONE, ctx, source=self.owner,
                        escape=EscapeCheck(abilities=("str", "dex"), dc=10,
                                           consumes_action=False))
                # Enorme o mayor: sin salvación (solo daño).
        elif opcion == "Distracting Strike":
            ronda = getattr(ctx, "round", None)
            estado = getattr(target, "state", None)
            if ronda is not None and estado is not None:
                # shortcut: caduca en ronda+1 («antes del inicio de tu
                # siguiente turno»); la ventaja es para OTROS y la
                # consume consumir_marcas al primer atacante distinto.
                estado.distracting[self.owner.name] = ronda + 1
        # Feinting: la ventaja la concede modify_attack_modifiers y el
        # dato de la marca vive en el propio rasgo (feinting_pendiente).


__all__ = ["BattleMasterFeatures"]

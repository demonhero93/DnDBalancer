"""Subclase Path of the Zealot del bárbaro (PHB 2024).

Fuente: *Player's Handbook 2024* — Path of the Zealot (features en
niveles 3, 6, 10 y 14). No está ni en el SRD 2014 ni en la API, así que
la tabla va hardcodeada en :data:`ZEALOT_FEATURES`. Aplica sobre la
Furia del proyecto (reglas 2024). Una sola clave de registro:
``zealot``.

Decisiones de simulación documentadas:

- **Divine Fury** (3): mientras dure la Furia, en cada turno propio la
  PRIMERA criatura impactada recibe ``1d6 + level // 2`` de daño
  necrótico o radiante (elegido con ``pick`` en cada pago), cuerpo a
  cuerpo o a distancia, sin exigir Ataque Temerario. Se aplica como
  instancia de daño propia vía ``inflict_damage`` con
  ``magical=False`` [VERIFICAR: mágico o no]. Estado propio
  ``divine_pagado`` limpio en ``on_turn_start`` y ``reset`` (patrón
  Frenzy); no se paga en reacciones ni en turnos ajenos. Sin ``rng``
  el rasgo se abstiene (no paga ni se marca).
- **Warrior of the Gods** (3): reserva de d12 (4; 5 desde 6; 6 desde
  12; 7 desde 17 [VERIFICAR progresión]) repuesta en ``reset``. La
  bonus action :class:`WarriorHealAction` (usage=None; el límite vive
  en el trait) gasta ``pick(1..restantes)`` dados, tira ``Nd12`` y
  cura sin pasar del máximo; solo con el bárbaro herido, vivo y con
  dados. No exige Furia. Sin ``rng`` no se gasta nada.
- **Fanatical Focus** (6): una vez por Furia, tras FALLAR una
  salvación se repite con ``pick`` sí/no; la repetición tira de verdad
  (``saving_throw``) y suma ``rage_damage(level)`` al total, y el
  resultado nuevo SUSTITUYE al original (el hook ``after_failed_save``
  devuelve un ``SaveResult``; si lo salva, el bucle se corta). Los
  auto-fallos (aturdido...) NO se repiten [VERIFICAR]. Se repone en
  ``on_rage_start``/``reset``. Exige Furia activa.
- **Zealous Presence** (10): la bonus action
  :class:`ZealousPresenceAction` (patrón Intimidating Presence: uso
  gratis por combate o gasto de Furia con ``pick`` cuando compiten)
  activa ``presencia_activa`` hasta el inicio del siguiente turno del
  bárbaro (``on_turn_start``) o ``reset``: los aliados vivos no
  hostiles a 60 pies (cobertura
  :data:`ZEALOT_COVERAGE_PROBABILITY`, 1.0 → sin RNG) tienen ventaja
  en ATAQUES (hook ``grant_attack_modifiers``) y en SALVACIONES (hook
  nuevo ``grant_save_modifiers``). El propio bárbaro no se beneficia
  (en ataques el bucle salta al atacante; en salvaciones salta al
  propio objetivo). No exige Furia para activarlo.
- **Rage of the Gods** (14): al entrar en Furia, ``pick`` sí/no de
  asumir la forma divina; la forma es UNA vez por combate (si dice
  que no, se vuelve a ofrecer en la siguiente Furia) [VERIFICAR].
  En la forma: vuelo = velocidad (sin posiciones: dato, sin efecto);
  resistencias a necrótico/psíquico/radiante concedidas con lista
  propia (solo las que no tuviera ya) y revocadas en
  ``on_rage_end``/``reset``; Revivification: al caer a 0 PG
  (``on_reduced_to_zero_hp``, después de que Furia Inaguantable
  resuelva primero) gasta un uso de Furia y queda con PG = nivel, UNA
  vez por forma, de forma automática sin ``pick`` [VERIFICAR
  decisión]. La forma termina al terminar la Furia.
- **Sin posiciones**: Branches-like (vuelo) y el límite de «10
  criaturas» de la presencia no se modelan: se afecta a todos los
  aliados vivos en cobertura (# TODO).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .....core.classes import MAX_LEVEL, MIN_LEVEL, rage_damage
from .....core.dice import roll_dice
from .....core.enums import DamageType
from .....core.log import log_line as _log_line
from .....core.randomness import pick
from .....model.actions import ActionType, CombatAction
from ....damage import inflict_damage
from ....saves import SaveResult, saving_throw
from ....traits.base import Trait
from ....usage import ActionUsage, UsageKind
from .._util import _de, _furia_de
from ..features import BarbarianFeatures, _contexto

#: Features de subclase por nivel (PHB 2024; nombres en inglés).
ZEALOT_FEATURES: dict[int, tuple[str, ...]] = {
    3: ("Divine Fury", "Warrior of the Gods"),
    6: ("Fanatical Focus",),
    10: ("Zealous Presence",),
    14: ("Rage of the Gods",),
}

#: Probabilidad por criatura de estar «a 60 pies» (sin posiciones;
#: mismo criterio que las auras). 1.0/0.0 no consumen RNG.
ZEALOT_COVERAGE_PROBABILITY: float = 1.0

#: Tipos de Divine Fury: (clave de daño, nombre para el log).
_DIVINE_TIPOS: tuple[tuple[str, str], ...] = (
    ("necrotic", "necrótico"),
    ("radiante", "radiante"),
)


def _reserva_dados(level: int) -> int:
    """Dados de la reserva de Warrior of the Gods según el nivel."""
    n = 4
    if level >= 6:
        n += 1
    if level >= 12:
        n += 1
    if level >= 17:
        n += 1
    return n


def _en_60_pies(rng: Any) -> bool:
    """¿Está a 60 pies? (cobertura, sin posiciones)."""
    p = float(ZEALOT_COVERAGE_PROBABILITY)
    if p <= 0.0:
        return False
    if p >= 1.0:
        return True
    if rng is None:
        return True  # sin RNG: cobertura completa (no inventa tiradas)
    return rng.random() < p


def _es_aliado(owner: Any, criatura: Any, rng: Any) -> bool:
    """¿``criatura`` es un aliado vivo de ``owner`` en cobertura?"""
    if criatura is None or criatura is owner:
        return False
    if not getattr(criatura, "alive", True):
        return False
    hostil = getattr(owner, "is_hostile_to", None)
    if hostil is not None and hostil(criatura):
        return False
    return _en_60_pies(rng)


@dataclass
class ZealotFeatures(Trait):
    """Features de la subclase y estado de Furia divina/Presencia."""

    level: int = MIN_LEVEL
    #: ¿Ya se pagó Divine Fury en este turno? (limpio en on_turn_start).
    divine_pagado: bool = field(default=False, repr=False, compare=False)
    #: ¿Ya se usó Fanatical Focus en esta Furia? (limpio en on_rage_start).
    fanatical_usado: bool = field(default=False, repr=False, compare=False)
    #: Uso gratis diario de Zealous Presence (1/día). El estado vive en
    #: el trait para que ``Combatant.reset`` lo recupere cada combate.
    presence_usage: ActionUsage = field(
        default_factory=lambda: ActionUsage(UsageKind.PER_DAY, 1),
        repr=False, compare=False,
    )
    #: ¿Está la Presencia ferviente activa hasta el próximo turno?
    presencia_activa: bool = field(default=False, repr=False, compare=False)
    #: Dados restantes de la reserva de Warrior of the Gods.
    dados_restantes: int = 0
    #: Rage of the Gods: forma ofrecida/activa y usada (1 por combate).
    forma_usada: bool = field(default=False, repr=False, compare=False)
    forma_activa: bool = field(default=False, repr=False, compare=False)
    #: ¿Ya se pagó Revivification en esta forma?
    revivificada: bool = field(default=False, repr=False, compare=False)
    #: Resistencias concedidas por la forma (para revocar solo las nuestras).
    _forma_concedidas: list = field(default_factory=list, repr=False,
                                    compare=False)
    owner: Any = field(default=None, repr=False, compare=False)

    @property
    def _furiosa(self) -> bool:
        barb = _de(self.owner, BarbarianFeatures)
        return bool(barb and barb.rage_active)

    # --- Divine Fury (3) -----------------------------------------------------
    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            crit: bool = False, ctx: Any = None,
                            rng: Any = None, atk: Any = None) -> int:
        """1d6 + level//2 en la primera criatura impactada del turno.

        Cuerpo a cuerpo o a distancia, sin exigir Ataque Temerario. El
        daño va como instancia propia (necrótico/radiante elegido con
        ``pick`` cada vez) y NO se marca como mágico [VERIFICAR]. Turno
        propio (nunca reacciones ni turnos ajenos); sin ``rng`` no paga
        ni se marca.
        """
        if self.level < 3 or self.owner is None or attacker is not self.owner:
            return 0
        if self.divine_pagado or target is None:
            return 0
        if getattr(ctx, "is_reaction", False):
            return 0  # la reacción no lleva daño divino
        if ctx is not None:
            ctx_actor = getattr(ctx, "actor", None)
            if ctx_actor is not None and ctx_actor is not attacker:
                return 0  # fuera de su turno no paga
        if not self._furiosa:
            return 0
        if rng is None:
            return 0  # sin RNG el rasgo se abstiene (no inventa dados)
        self.divine_pagado = True
        tipo, txt = pick(rng, _DIVINE_TIPOS)
        total = int(roll_dice("1d6", rng)) + self.level // 2
        inflict_damage(target, total, tipo, source=self.owner, ctx=ctx,
                       magical=False)
        _log_line(ctx, f"{getattr(self.owner, 'name', self.owner)} inflige "
                       f"daño divino ({txt}) a "
                       f"{getattr(target, 'name', target)}")
        return 0

    # --- Warrior of the Gods (3) ---------------------------------------------
    # La curación vive en WarriorHealAction (abajo).

    # --- Fanatical Focus (6) --------------------------------------------------
    def after_failed_save(self, target: Any, ability: str, result: Any,
                          ctx: Any = None) -> Any:
        """Repite la salvación fallida con +rage_damage (una vez por Furia)."""
        if self.level < 6 or target is not self.owner or result is None:
            return None
        if self.fanatical_usado or not self._furiosa:
            return None
        if getattr(result, "auto_fail", False):
            return None  # el fallo automático no se repite [VERIFICAR]
        rng = getattr(ctx, "rng", None) if ctx is not None else None
        if rng is None:
            return None  # sin RNG el rasgo se abstiene
        if pick(rng, ("no", "si")) == "no":
            return None  # decisión aleatoria de repetirla
        self.fanatical_usado = True
        nuevo = saving_throw(target, result.ability, result.dc, rng)
        bonus = rage_damage(self.level)
        total = int(nuevo.total) + bonus
        dc = int(result.dc)
        salida = SaveResult(
            ability=result.ability,
            dc=dc,
            rolls=list(nuevo.rolls),
            bonus=int(nuevo.bonus) + bonus,
            total=total,
            success=total >= dc,
            mode=nuevo.mode,
        )
        _log_line(ctx, f"{getattr(target, 'name', target)} repite la "
                       f"salvación {str(result.ability).upper()} con "
                       f"Fanatical Focus ({total} vs CD {dc})")
        return salida

    # --- Zealous Presence (10) ------------------------------------------------
    def grant_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                               rango: Any, ctx: Any = None,
                               rng: Any = None, atk: Any = None) -> None:
        """Ventaja en los ATAQUES de los aliados mientras dure la Presencia."""
        if self.level < 10 or not self.presencia_activa or self.owner is None:
            return None
        if not _es_aliado(self.owner, attacker, rng):
            return None
        mods.advantage_sources.append("Presencia ferviente")
        return None

    def grant_save_modifiers(self, mods: Any, target: Any, ability: str,
                             kind: str | None = None,
                             ctx: Any = None) -> None:
        """Ventaja en las SALVACIONES de los aliados con la Presencia activa."""
        if self.level < 10 or not self.presencia_activa or self.owner is None:
            return None
        rng = getattr(ctx, "rng", None) if ctx is not None else None
        if not _es_aliado(self.owner, target, rng):
            return None
        mods.advantage_sources.append("Presencia ferviente")
        return None

    # --- Rage of the Gods (14) ------------------------------------------------
    def on_rage_start(self, actor: Any, ctx: Any = None) -> None:
        """Entrar en Furia repite Fanatical Focus y ofrece la forma divina."""
        if self.level >= 6:
            self.fanatical_usado = False
        if self.level < 14 or self.forma_usada or self.owner is None:
            return
        rng = getattr(ctx, "rng", None) if ctx is not None else None
        if rng is None:
            return  # sin RNG no se ofrece (no inventa la decisión)
        if pick(rng, ("no", "si")) == "no":
            return  # dijo no: se volverá a ofrecer en la próxima Furia
        self.forma_usada = True
        self.forma_activa = True
        self.revivificada = False
        concedidos = [t for t in (DamageType.NECROTIC, DamageType.PSYCHIC,
                                  DamageType.RADIANT)
                      if t not in actor.resistances]
        self._forma_concedidas = concedidos
        actor.resistances.update(concedidos)
        _log_line(ctx, f"{getattr(actor, 'name', actor)} asume la forma "
                       f"divina (Rage of the Gods)")

    def _revocar_forma(self) -> None:
        """Revoca solo las resistencias que concedió la forma."""
        owner = self.owner
        if owner is not None and self._forma_concedidas:
            try:
                owner.resistances.difference_update(self._forma_concedidas)
            except Exception:
                pass
        self._forma_concedidas = []
        self.forma_activa = False

    def on_reduced_to_zero_hp(self, owner: Any, amount: int,
                              damage_type: Any = None, source: Any = None,
                              crit: bool = False, ctx: Any = None,
                              rng: Any = None) -> int | None:
        """Revivification: gasta un uso de Furia y queda con PG = nivel.

        Corre DESPUÉS de Furia Inaguantable (el trait de la clase va
        primero en ``traits``): si esa ya lo salvó, este hook no se
        llama. Automático (sin ``pick``) y UNA vez por forma.
        """
        if (self.level < 14 or owner is not self.owner
                or not self.forma_activa or self.revivificada):
            return None
        furia = _furia_de(owner)
        if furia is None or furia.usage is None or not furia.usage.available:
            return None  # sin uso de Furia no se revive
        furia.usage.spend()
        self.revivificada = True
        _log_line(ctx, f"{getattr(owner, 'name', owner)} gasta un uso de "
                       f"Furia (Revivification) y queda con {self.level} PG")
        return int(self.level)

    # --- Ciclo de vida --------------------------------------------------------
    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        """Limpia el pago de Divine Fury y expira la Presencia."""
        self.divine_pagado = False
        self.presencia_activa = False

    def on_rage_end(self, actor: Any, ctx: Any = None) -> None:
        self._revocar_forma()

    def reset(self) -> None:
        self.divine_pagado = False
        self.fanatical_usado = False
        self.presencia_activa = False
        self.presence_usage.reset()
        self.dados_restantes = _reserva_dados(self.level)
        self.revivificada = False
        self.forma_usada = False
        self._revocar_forma()


class WarriorHealAction(CombatAction):
    """Curación de Warrior of the Gods: bonus action (nivel ≥ 3).

    Gasta ``pick(1..dados_restantes)`` dados de la reserva y cura el
    total sin pasar del máximo. El límite de la reserva vive en el
    trait (aquí ``usage`` es None para que el encuentro no gaste nada
    por su cuenta).
    """

    def __init__(self) -> None:
        self.name = "Guerrero de los Dioses"
        self.action_type = ActionType.BONUS_ACTION
        self.usage = None

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        zeal = _de(actor, ZealotFeatures)
        if zeal is None or zeal.level < 3:
            return False
        if not getattr(actor, "alive", True):
            return False
        if int(getattr(actor, "hp", 0) or 0) >= int(getattr(actor, "max_hp", 0) or 0):
            return False  # solo con el bárbaro herido
        return zeal.dados_restantes > 0

    def execute(self, context: Any) -> None:
        actor = getattr(context, "actor", None)
        zeal = _de(actor, ZealotFeatures) if actor is not None else None
        if zeal is None or zeal.level < 3:
            return
        rng = getattr(context, "rng", None)
        if rng is None:
            return  # sin RNG no se gasta nada
        if zeal.dados_restantes <= 0:
            return
        dados = pick(rng, range(1, zeal.dados_restantes + 1))
        total = int(roll_dice(f"{dados}d12", rng))
        max_hp = int(getattr(actor, "max_hp", 0) or 0)
        hp = int(getattr(actor, "hp", 0) or 0)
        actor.hp = min(max_hp, hp + total)  # nunca por encima del máximo
        zeal.dados_restantes -= int(dados)
        _log_line(context, f"{getattr(actor, 'name', actor)} se cura {total} "
                           f"PG con Guerrero de los Dioses")


class ZealousPresenceAction(CombatAction):
    """Presencia ferviente: bonus action (nivel ≥ 10), pago o de Furia.

    Mismo patrón que Intimidating Presence: uso gratis por combate; si
    no lo tiene, puede restaurarlo gastando un uso de Furia; si ambas
    están disponibles compiten con ``pick``.
    """

    def __init__(self) -> None:
        self.name = "Presencia ferviente"
        self.action_type = ActionType.BONUS_ACTION
        # El límite diario vive en el trait (el pago va en execute).
        self.usage = None

    def can_use(self, *args: Any, **kwargs: Any) -> bool:
        if not super().can_use(*args, **kwargs):
            return False
        ctx = _contexto(args, kwargs)
        actor = getattr(ctx, "actor", None)
        if actor is None:
            return False
        zeal = _de(actor, ZealotFeatures)
        if zeal is None or zeal.level < 10:
            return False
        if not getattr(actor, "alive", True):
            return False
        if not any(_es_aliado(actor, c, getattr(ctx, "rng", None))
                   for c in getattr(ctx, "combatants", None) or []):
            return False  # sin aliados no hay nada que grantar
        if zeal.presence_usage.available:
            return True
        furia = _furia_de(actor)
        return bool(furia is not None and furia.usage is not None
                    and furia.usage.available)

    def execute(self, context: Any) -> None:
        actor = getattr(context, "actor", None)
        zeal = _de(actor, ZealotFeatures) if actor is not None else None
        if zeal is None or zeal.level < 10:
            return
        rng = getattr(context, "rng", None)
        if rng is None:
            return  # sin RNG no se paga nada
        aliados = [c for c in getattr(context, "combatants", None) or []
                   if _es_aliado(actor, c, rng)]
        if not aliados:
            return  # sin aliados no se paga el uso
        # Pago: gratis y de Furia compiten con ``pick``; la de Furia
        # gasta un uso de Furia y restaura el uso gratis (mismo patrón
        # que Intimidating Presence).
        opciones = []
        if zeal.presence_usage.available:
            opciones.append("gratis")
        furia = _furia_de(actor)
        if (furia is not None and furia.usage is not None
                and furia.usage.available):
            opciones.append("furia")
        if not opciones:
            return  # can_use ya lo impide: red de seguridad
        pago = pick(rng, opciones)
        if pago == "gratis":
            zeal.presence_usage.spend()
        else:
            furia.usage.spend()
            zeal.presence_usage.restore()
        zeal.presencia_activa = True
        _log_line(context, f"{getattr(actor, 'name', actor)} usa "
                           f"Presencia ferviente sobre {len(aliados)} "
                           f"aliado(s)")


def apply_zealot(pj: Any, level: int | None = None) -> ZealotFeatures:
    """Aplica la subclase Path of the Zealot a un PJ bárbaro.

    Exige que ``pj`` ya tenga :class:`BarbarianFeatures`
    (:func:`apply_barbarian`). Añade el trait y las dos acciones bonus
    de la subclase.
    """
    if _de(pj, BarbarianFeatures) is None:
        raise ValueError(
            "Primero aplica la clase bárbaro con apply_barbarian(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    trait = ZealotFeatures(name="Zealot", level=lvl)
    trait.owner = pj
    trait.dados_restantes = _reserva_dados(lvl)
    pj.traits.append(trait)
    pj.actions.append(WarriorHealAction())
    pj.actions.append(ZealousPresenceAction())
    return trait


__all__ = ["ZEALOT_COVERAGE_PROBABILITY", "ZEALOT_FEATURES",
           "WarriorHealAction", "ZealotFeatures", "ZealousPresenceAction",
           "apply_zealot"]

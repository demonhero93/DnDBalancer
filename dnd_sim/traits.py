"""Rasgos especiales de monstruos (features de la ficha).

Todo lo que una criatura **genérica** puede tener ya vive en su sitio (CA,
PV, ataques, salvaciones, usos limitados, hechizos, legendario, estados y
condiciones). Aquí van los **rasgos con reglas propias** que no son acciones
ni estados: efectos pasivos que modifican cómo se resuelven las tiradas.

Formato real en la API (dnd5eapi.co, SRD 2014):

.. code-block:: json

    {"name": "Blood Frenzy",
     "desc": "The sahuagin has advantage on melee attack rolls against any
              creature that doesn't have all its hit points.",
     "damage": []}

Estructura:

- :class:`Trait`: el rasgo con su nombre y descripción más los **hooks** de
  reglas. Un hook que un rasgo no implementa no hace nada, así que cada rasgo
  solo influye en lo que sabe modelar.
- :data:`TRAIT_CLASSES`: registro ``nombre -> clase``; lo consume
  :func:`dnd_sim.data.trait_parser.parse_traits` para rellenar
  ``Combatant.traits`` al cargar un monstruo.

Rasgos implementados:

- **Blood Frenzy** (sahuagin): ventaja en los ataques **cuerpo a cuerpo**
  contra criaturas que no tienen todos sus PV. El hook se ejecuta en
  :func:`dnd_sim.roll_modifiers.attack_modifiers` (la única fuente del modo
  de tirada), así que convive correctamente con los indicadores estáticos y
  las condiciones: si hay ventaja y desventaja a la vez se anulan.
- **Pack Tactics** (lobo) y **Martial Advantage** (hobgoblin): la condición
  es de **posición** (un aliado no incapacitado cerca del objetivo), que el
  motor no modela, así que la decisión es **aleatoria**: si el atacante
  tiene aliados capaces se sortea (50 %) y si no tiene ninguno nunca aplica
  (véase :func:`_condicion_posicional`). El daño extra de Martial Advantage
  usa el hook ``extra_attack_damage`` y entra en el ataque **antes** de la
  inmunidad/resistencia del objetivo.
- **Damage Transfer** (cloaker): mientras esté enganchado, el daño que
  recibe se parte en dos: él baja la mitad (redondeada hacia abajo) y la
  criatura enganchada se lleva la otra mitad, que además pasa por sus
  **propios** modificadores (resistencia/inmunidad/vulnerabilidad). Los
  hooks viven en :func:`dnd_sim.damage.inflict_damage` (fases 1 y 2); el
  enganche en sí lo modela :mod:`dnd_sim.attach`.
- **Heated Body** (azer): quien lo golpea cuerpo a cuerpo recibe 1d10 de
  daño de fuego. El trigger es el **impacto**, así que el hook vive en
  :func:`dnd_sim.combat.attack_roll` (``after_being_hit``) y se activa
  aunque el daño sea 0 por inmunidad.
- **Regeneration** (troll): recupera 10 PV al inicio de su turno salvo que
  haya recibido daño de ácido o fuego desde su turno anterior, y a 0 PV no
  muere de inmediato sino **al empezar su turno** si no llega a
  regenerarse (hooks ``on_turn_start``, ``after_damage_taken``,
  ``survives_at_zero_hp`` y ``reset``).
- **Turn Resistance** (lich): ventaja en las salvaciones contra un efecto
  que convierte no-muertos. Esa ventaja solo llega si la salvación se pide
  con ``kind="turn"``; hoy ningún efecto del motor lo hace (# TODO: Turn
  Undead), así que el rasgo está cableado y probado pero sin consumidor.

Catálogo de hooks (un único punto de despacho: :func:`hooks`)

============================  ======================================================
Hook                          Dónde se dispara
============================  ======================================================
``modify_attack_modifiers``   :func:`dnd_sim.roll_modifiers.attack_modifiers`
``modify_save_modifiers``     :func:`dnd_sim.roll_modifiers.save_modifiers`
``modify_check_modifiers``    :func:`dnd_sim.roll_modifiers.check_modifiers`
``modify_incoming_damage``    :func:`dnd_sim.damage.inflict_damage` (fase 1)
``after_damage_taken``        :func:`dnd_sim.damage.inflict_damage` (fase 2)
``after_being_hit``           :func:`dnd_sim.combat.attack_roll`
``extra_attack_damage``       :func:`dnd_sim.combat.attack_roll`
``on_turn_start``             :func:`dnd_sim.usage.begin_turn`
``survives_at_zero_hp``       :attr:`dnd_sim.combatant.Combatant.alive`
``reset``                     :meth:`dnd_sim.combatant.Combatant.reset`
============================  ======================================================

Cómo añadir un rasgo nuevo (p. ej. Web Sense):

1. Crea la clase en este módulo sobrescribiendo **solo** los hooks que
   necesite; los que no sobrescriba no se llaman nunca (la base
   :class:`Trait` los define como no-op).
2. Regístrala en :data:`TRAIT_CLASSES` con su nombre en minúsculas.
3. Nada más: ``parse_traits()`` la detectará en ``special_abilities``.
4. Si el rasgo saca números de su descripción («regains 10 hit points»),
   que la propia clase los interprete en ``__post_init__`` a partir de
   ``self.desc``: ``parse_traits`` solo pasa nombre y descripción.
5. Si necesita un hook que aún no existe, añádelo a :class:`Trait` (con su
   implementación no-op) y a :data:`HOOK_NAMES`, y dispara desde el módulo
   correspondiente con **una sola** llamada a :func:`hooks` por punto de
   enganche (así todos los rasgos pasan por el mismo filtro).

# TODO: rasgos de la SRD que el motor aún no modela (no combativos o fuera
# de combate): Limited Amphibiousness, Shark Telepathy, Amphibious, Water
# Breathing... y los que dependen de un modelo que aún no existe:
#
# - **Keen Hearing and Smell** (lobo, búho) / **Sunlight Sensitivity** /
#   **Light Sensitivity** / **Illumination**: se ignoran por decisión (y
#   porque exigen habilidades y un modelo de luz). Sus hooks ya existen
#   (``modify_check_modifiers`` con ``skill`` y ``modify_attack_modifiers``),
#   falta el dato de entrada.
# - **Web Sense** / **Web Walker** / **Spider Climb**: movimiento y
#   telarañas, sin modelo.
# - **False Appearance**, **Rejuvenation**: fuera de combate.
# - **Turn Undead** (el consumidor de Turn Resistance): no existe aún.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

try:
    from .damage import (DamageType, apply_damage_modifiers, inflict_damage,
                         parse_damage_type)
    from .dice import roll_dice
    from .randomness import pick
    from .roll_modifiers import AttackRange
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from damage import (DamageType, apply_damage_modifiers,
                            inflict_damage, parse_damage_type)
        from dice import roll_dice
        from randomness import pick
        from roll_modifiers import AttackRange
    except ImportError:
        from dnd_sim.damage import (DamageType, apply_damage_modifiers,
                                    inflict_damage, parse_damage_type)
        from dnd_sim.dice import roll_dice
        from dnd_sim.randomness import pick
        from dnd_sim.roll_modifiers import AttackRange


try:
    from .log import log_line as _log_line
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from log import log_line as _log_line
    except ImportError:
        from dnd_sim.log import log_line as _log_line


@dataclass
class Trait:
    """Rasgo especial pasivo de una criatura (sin acciones propias)."""

    name: str = ""
    desc: str = ""

    # --- Tiradas -----------------------------------------------------------
    def modify_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                                rango: Any, ctx: Any = None,
                                rng: Any = None) -> None:
        """Hook: añade ventaja/desventaja a ``mods`` si el rasgo aplica.

        ``mods`` es un :class:`dnd_sim.roll_modifiers.AttackModifiers` y
        ``rango`` el rango ya resuelto del ataque. ``ctx`` es el contexto
        del combate (con ``combatants``: la única información de posición
        que hay) y ``rng`` el generador, para los rasgos cuya condición no
        se puede comprobar (Pack Tactics). Si ``ctx`` o ``rng`` llegan
        vacíos el rasgo **no debe aplicarse** en lugar de inventar un
        resultado. Por defecto no hace nada.
        """
        return None

    # --- Daño recibido (fases de dnd_sim.damage.inflict_damage) ------------
    def modify_incoming_damage(self, target: Any, amount: int,
                               damage_type: Any, source: Any,
                               ctx: Any = None) -> int | None:
        """Hook fase 1: ajusta el daño que ``target`` va a recibir.

        Recibe la cantidad en curso; devolver ``None`` deja el daño como
        está (devolver un entero lo sustituye; no puede ser negativo).
        """
        return None

    def after_damage_taken(self, target: Any, amount: int, damage_type: Any,
                           source: Any, ctx: Any = None) -> None:
        """Hook fase 2: efectos tras aplicar el daño.

        ``amount`` es el **daño original** que recibió ``target`` (ya
        descontado de sus PV en la fase 1).
        """
        return None

    # --- Al ser golpeado (hook de dnd_sim.combat.attack_roll) ---------------
    def after_being_hit(self, target: Any, attacker: Any, rango: Any,
                        ctx: Any = None) -> None:
        """Hook: reacción cuando ``attacker`` **impacta** a ``target``.

        Se ejecuta tras el daño, en cada impacto (aunque el daño sea 0 por
        inmunidad), con ``rango`` el rango ya resuelto del ataque. Por
        defecto no hace nada.
        """
        return None

    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            crit: bool = False, ctx: Any = None,
                            rng: Any = None) -> int:
        """Hook: daño adicional que ``attacker`` suma a **este** ataque.

        Devuelve los PV extra (0 = nada). El motor los suma al daño bruto
        **antes** de la inmunidad/resistencia/vulnerabilidad del objetivo y
        con el tipo de daño del propio ataque; ``crit`` indica si el golpe
        es crítico para que los dados extra se dupliquen como el resto.
        Se dispara en :func:`dnd_sim.combat.attack_roll`.
        """
        return 0

    # --- Salvaciones -------------------------------------------------------
    def modify_save_modifiers(self, mods: Any, target: Any,
                              ability: str, kind: str | None = None) -> None:
        """Hook: ventaja/desventaja en la salvación ``ability`` de ``target``.

        ``mods`` es un :class:`dnd_sim.roll_modifiers.SaveModifiers` y
        ``ability`` la característica ya normalizada (``"str"``...).
        ``kind`` dice qué tipo de efecto provoca la salvación cuando quien
        la tira lo sabe: hoy solo ``"turn"`` (un efecto que convierte
        no-muertos, p. ej. Turn Undead) y todavía no lo pasa nadie
        (# TODO). Se ejecuta en :func:`dnd_sim.roll_modifiers.save_modifiers`.
        Por defecto no hace nada.
        """
        return None

    # --- Pruebas de característica ----------------------------------------
    def modify_check_modifiers(self, mods: Any, target: Any, ability: str,
                               skill: str | None = None) -> None:
        """Hook: ventaja/desventaja en la prueba ``ability`` de ``target``.

        ``mods`` es un :class:`dnd_sim.roll_modifiers.CheckModifiers`.
        ``skill`` es la habilidad asociada si la hubiera (``"perception"``);
        # TODO: las habilidades aún no se modelan, así que hoy siempre es
        ``None``: un rasgo limitado a una habilidad (Keen Senses) no puede
        distinguirla y debe esperar a ese modelo. Por defecto no hace nada.
        """
        return None

    # --- Inicio del turno --------------------------------------------------
    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        """Hook: efecto pasivo al inicio del turno propio de ``actor``.

        Se ejecuta en :func:`dnd_sim.usage.begin_turn`, con los recursos ya
        cargados y **antes de comprobar si el actor está incapacitado**
        (es un efecto automático, no una acción). Por defecto no hace nada.
        """
        return None

    # --- Supervivencia a 0 PV ----------------------------------------------
    def survives_at_zero_hp(self, owner: Any) -> bool:
        """Hook: ¿sigue vivo ``owner`` aunque tenga 0 PV (o menos)?

        Lo consulta :attr:`dnd_sim.combatant.Combatant.alive` justo cuando
        los PV llegan a 0: un rasgo que responda ``True`` (Regeneration)
        mantiene a la criatura en pie hasta que **su propio** turno decida
        si se recupera o muere. Si nadie responde, 0 PV sigue significando
        muerte. Por defecto ``False``.
        """
        return False

    # --- Reinicio de combate ------------------------------------------------
    def reset(self) -> None:
        """Hook: borra el estado propio del rasgo al empezar un combate.

        Se llama desde :meth:`dnd_sim.combatant.Combatant.reset` (los
        mismos objetos se reutilizan en ``simulate()``, así que el estado
        por combate se limpia aquí). Por defecto no hace nada.
        """
        return None


#: Nombres de los hooks que un rasgo puede sobrescribir (catálogo completo).
#: Es la fuente de verdad de :func:`hooks`: si añades un hook nuevo a
#: :class:`Trait`, regístralo aquí para que el despacho lo reconozca.
HOOK_NAMES: tuple[str, ...] = (
    "modify_attack_modifiers",
    "modify_save_modifiers",
    "modify_check_modifiers",
    "modify_incoming_damage",
    "after_damage_taken",
    "after_being_hit",
    "extra_attack_damage",
    "on_turn_start",
    "survives_at_zero_hp",
    "reset",
)


def hooks(traits: Any, nombre: str) -> list[Any]:
    """Rasgos de ``traits`` (lista o ``None``) que **sobrescriben** ``nombre``.

    Único punto de despacho de los hooks de los rasgos: los que no
    sobrescriben el hook (la base :class:`Trait` lo define como no-op) no se
    llaman. Todos los módulos que miran rasgos pasan por aquí para que el
    filtro sea idéntico en todos los puntos de enganche.

    Lanza ``ValueError`` si ``nombre`` no está en :data:`HOOK_NAMES` (typo
    detectado en cuanto se llama, no a mitad de un combate).
    """
    if nombre not in HOOK_NAMES:
        raise ValueError(f"Hook de rasgo desconocido: {nombre!r}")
    if not traits:
        return []
    base = getattr(Trait, nombre, None)
    activos: list[Any] = []
    for rasgo in traits:
        if not callable(getattr(rasgo, nombre, None)):
            continue
        # Sobrescribe si lo define la propia instancia o su clase no es la
        # implementación por defecto de Trait (no-op).
        si_propio = nombre in getattr(rasgo, "__dict__", {})
        if not si_propio:
            si_propio = getattr(type(rasgo), nombre, None) is not base
        if si_propio:
            activos.append(rasgo)
    return activos


@dataclass
class BloodFrenzy(Trait):
    """Blood Frenzy (sahuagin): ventaja cuerpo a cuerpo contra un herido.

    «The sahuagin has advantage on melee attack rolls against any creature
    that doesn't have all its hit points.» (SRD 2014)
    """

    def modify_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                                rango: Any, ctx: Any = None,
                                rng: Any = None) -> None:
        if rango is not AttackRange.MELEE:
            return  # solo ataques cuerpo a cuerpo
        max_hp = int(getattr(target, "max_hp", 0) or 0)
        hp = int(getattr(target, "hp", max_hp) or 0)
        if 0 < max_hp and hp < max_hp:
            mods.advantage_sources.append(self.name or "Blood Frenzy")


def aliados_capaces(combatiente: Any, ctx: Any) -> list[Any]:
    """Aliados de ``combatiente`` en el combate que aún pueden participar.

    Es el «aliado que no está incapacitado» de las fichas (Pack Tactics,
    Martial Advantage): ``can_act`` ya cubre "vivo y no incapacitado" y
    ``is_hostile_to`` contempla el bando y el hechizado. Sin contexto (o
    sin ``combatants``) no hay aliados que contar.
    """
    resultado: list[Any] = []
    for otro in getattr(ctx, "combatants", None) or []:
        if otro is combatiente:
            continue
        if not getattr(otro, "can_act", True):
            continue
        try:
            if combatiente.is_hostile_to(otro):
                continue
        except Exception:
            continue
        resultado.append(otro)
    return resultado


def _condicion_posicional(combatiente: Any, ctx: Any, rng: Any) -> bool:
    """¿Se cumple una condición de posición que el motor no puede mirar?

    Las fichas la expresan como «un aliado no incapacitado está a menos de
    5 pies del objetivo»: aquí **no hay modelo de posición**, así que la
    decisión se toma al azar (50 %) **solo** si el combatiente tiene
    aliados capaces; sin aliados nunca se cumple. Consume RNG únicamente
    cuando hay algo que sortear, y devuelve ``False`` si no hay con qué
    decidir (sin ``ctx`` o sin ``rng`` no se inventa un resultado).
    """
    if ctx is None or rng is None:
        return False
    if not aliados_capaces(combatiente, ctx):
        return False
    return bool(pick(rng, [True, False]))


@dataclass
class DamageTransfer(Trait):
    """Damage Transfer (cloaker): el daño que recibe se parte en dos.

    «While attached to a creature, the cloaker takes only half the damage
    dealt to it (rounded down), and that creature takes the other half.»
    (SRD 2014). Solo aplica mientras el portador esté enganchado: el
    enganche y su desenganche los modela :mod:`dnd_sim.attach`. La otra
    mitad es daño normal para el receptor, así que su inmunidad,
    resistencia o vulnerabilidad también cuenta.
    """

    @staticmethod
    def _enganchado(target: Any) -> Any:
        """Criatura a la que ``target`` está enganchado (viva), o ``None``."""
        otro = getattr(getattr(target, "state", None), "attached_to", None)
        if otro is None or otro is target:
            return None
        if not getattr(target, "alive", True) or not getattr(otro, "alive", True):
            return None  # muerto de los dos lados: el reparto no aplica
        return otro

    def modify_incoming_damage(self, target: Any, amount: int,
                               damage_type: Any, source: Any,
                               ctx: Any = None) -> int | None:
        if self._enganchado(target) is None:
            return None
        return int(amount) // 2  # «only half ... (rounded down)»

    def after_damage_taken(self, target: Any, amount: int, damage_type: Any,
                           source: Any, ctx: Any = None) -> None:
        otro = self._enganchado(target)
        if otro is None:
            return
        mitad = int(amount) - int(amount) // 2  # «and that creature takes the other half»
        if mitad <= 0:
            return
        # La mitad transferida es daño como cualquier otro: el receptor
        # aplica su propia inmunidad/resistencia/vulnerabilidad (los tipos
        # que no se reconocen pasan sin modificar, como hace inflict_damage).
        try:
            dt = parse_damage_type(damage_type)
        except Exception:
            dt = None
        try:
            from .combat import _tag_modificadores as _tag
        except ImportError:  # pragma: no cover - ejecución como script suelto
            try:
                from combat import _tag_modificadores as _tag
            except ImportError:
                from dnd_sim.combat import _tag_modificadores as _tag
        final = mitad if dt is None else apply_damage_modifiers(mitad, dt, otro)
        tag = "" if dt is None else _tag(mitad, final, dt, otro)
        inflict_damage(otro, final, dt, source=source, ctx=ctx)
        _log_line(
            ctx,
            f"{getattr(target, 'name', target)} reparte el daño: "
            f"{getattr(otro, 'name', otro)} recibe los otros "
            f"{final}{tag}",
        )


@dataclass
class HeatedBody(Trait):
    """Heated Body (azer): daño de fuego a quien lo golpea cuerpo a cuerpo.

    «A creature that touches the azer or hits it with a melee attack while
    within 5 ft. of it takes 5 (1d10) fire damage.» (SRD 2014). El trigger
    es el **impacto** (no el daño recibido), así que el hook vive en
    :func:`dnd_sim.combat.attack_roll` y se activa aunque el daño sea 0
    (p. ej. por inmunidad). El toque se modela como ataque cuerpo a cuerpo
    (el alcance del motor no distingue «toque» de «cuerpo a cuerpo»).

    Como todo daño, la represalia pasa por
    :func:`dnd_sim.damage.apply_damage_modifiers`: a quien es **inmune** le
    llega 0 (se sigue registrando el impacto, como en el daño principal) y
    a quien resiste, la mitad.
    """

    damage: str = "1d10"
    damage_type: str = "fire"

    def after_being_hit(self, target: Any, attacker: Any, rango: Any,
                        ctx: Any = None) -> None:
        if rango is not AttackRange.MELEE:
            return  # solo el contacto / ataque cuerpo a cuerpo
        if attacker is None or not getattr(attacker, "alive", True):
            return
        if int(getattr(attacker, "hp", 0) or 0) <= 0:
            return
        try:
            dados = str(self.damage or "1d10").strip() or "1d10"
        except Exception:
            dados = "1d10"
        rng = getattr(ctx, "rng", None)
        cantidad = roll_dice(dados, rng) if rng is not None else 1
        # Resistencias/inmunidades/vulnerabilidades del que golpea: la
        # llamada a inflict_damage se hace igualmente (con 0) para que el
        # impacto quede registrado como en el daño principal.
        cantidad = apply_damage_modifiers(cantidad, self.damage_type, attacker)
        sin_efecto = "" if cantidad > 0 else " (sin efecto: inmune o resistente)"
        inflict_damage(attacker, cantidad, self.damage_type,
                       source=target, ctx=ctx)
        _log_line(
            ctx,
            f"{getattr(target, 'name', target)} quema a "
            f"{getattr(attacker, 'name', attacker)} (cuerpo ardiente): "
            f"{cantidad} daño de fuego{sin_efecto}",
        )


@dataclass
class PackTactics(Trait):
    """Pack Tactics (lobo): ventaja si un aliado está cerca del objetivo.

    «The wolf has advantage on an attack roll against a creature if at
    least one of the wolf's allies is within 5 ft. of the creature and the
    ally isn't incapacitated.» (API, SRD 2014). La posición no está
    modelada, así que la condición la resuelve
    :func:`_condicion_posicional`.
    """

    def modify_attack_modifiers(self, mods: Any, attacker: Any, target: Any,
                                rango: Any, ctx: Any = None,
                                rng: Any = None) -> None:
        if _condicion_posicional(attacker, ctx, rng):
            mods.advantage_sources.append(self.name or "Pack Tactics")


@dataclass
class MartialAdvantage(Trait):
    """Martial Advantage (hobgoblin): 2d6 extra si el objetivo está cerca
    de un aliado.

    «Once per turn, the hobgoblin can deal an extra 7 (2d6) damage to a
    creature it hits with a weapon attack if that creature is within 5 ft.
    of an ally of the hobgoblin that isn't incapacitated.» (API, SRD 2014).

    Los números no vienen en un campo aparte: se leen de la descripción
    («an extra 7 (2d6)») en ``__post_init__``. La posición se resuelve como
    en Pack Tactics y el daño entra por el hook ``extra_attack_damage``,
    antes de los modificadores del objetivo.

    # TODO: el «once per turn» hoy se cumple de serie porque el hobgoblin
    # solo ataca una vez por turno; convendría acotarlo si alguna ficha
    # llega a tener Multiattack o varios ataques por turno.
    """

    dice: str = ""      # dados del extra, p. ej. «2d6»
    bonus: int = 0      # media que imprime la ficha, p. ej. 7 (informativa)

    def __post_init__(self) -> None:
        match = re.search(r"an extra (\d+) \((\d+d\d+)\)", self.desc or "")
        if match:
            self.bonus = int(match.group(1))
            self.dice = match.group(2)

    def extra_attack_damage(self, attacker: Any, target: Any, rango: Any,
                            crit: bool = False, ctx: Any = None,
                            rng: Any = None) -> int:
        if not self.dice:
            return 0  # descripción no interpretable: el rasgo no hace nada
        if not _condicion_posicional(attacker, ctx, rng):
            return 0
        return int(roll_dice(self.dice, rng, crit=crit))


@dataclass
class Regeneration(Trait):
    """Regeneration (troll): recupera PV al inicio de su turno.

    «The troll regains 10 hit points at the start of its turn. If the troll
    takes acid or fire damage, this trait doesn't function at the start of
    the troll's next turn. The troll dies only if it starts its turn with 0
    hit points and doesn't regenerate.» (API, SRD 2014)

    Cada frase es un hook:

    - ``after_damage_taken``: el ácido o el fuego bloquea **el próximo**
      inicio de turno (y solo ese).
    - ``on_turn_start``: cura ``amount`` PV; o bien muere si empieza el
      turno a 0 PV sin poder regenerarse.
    - ``survives_at_zero_hp``: hasta ese momento, a 0 PV sigue vivo (va a
      morir en su turno, no al recibir el golpe).
    - ``reset``: el estado es por combate y ``simulate()`` reutiliza los
      mismos objetos, así que se limpia con ``Combatant.reset()``.

    El ``amount`` sale de la descripción («regains 10 hit points»); si no
    se puede leer, el rasgo no hace nada y la criatura muere a 0 PV como
    cualquier otra.

    # TODO: la curación se calcula desde 0 PV porque el motor sí deja los
    # PV por debajo de 0 y la regla 5e no contempla PV negativos.
    """

    amount: int = 0
    blocked: bool = False   # ácido/fuego recibido desde su turno anterior
    dead: bool = False      # murió por no poder regenerarse a 0 PV

    def __post_init__(self) -> None:
        match = re.search(r"(\d+)\s+hit\s+points", self.desc or "")
        if match:
            self.amount = int(match.group(1))

    def after_damage_taken(self, target: Any, amount: int, damage_type: Any,
                           source: Any, ctx: Any = None) -> None:
        if int(amount or 0) <= 0:
            return
        try:
            dt = parse_damage_type(damage_type)
        except Exception:
            return  # sin tipo reconocible no hay con qué bloquearlo
        if dt in (DamageType.ACID, DamageType.FIRE):
            self.blocked = True

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        if self.amount <= 0 or self.dead:
            return  # sin cantidad legible, o ya muerto
        hp = int(getattr(actor, "hp", 0) or 0)
        max_hp = int(getattr(actor, "max_hp", hp) or hp)
        name = getattr(actor, "name", actor)
        if self.blocked:
            # El bloqueo dura exactamente un inicio de turno.
            self.blocked = False
            if hp <= 0:
                # «dies only if it starts its turn with 0 hit points and
                # doesn't regenerate».
                self.dead = True
                try:
                    ctx.skip_turn = True
                except Exception:
                    pass
                _log_line(ctx, f"{name} empieza su turno con 0 PV sin poder "
                               f"regenerarse: muere")
                return
            _log_line(ctx, f"{name} no regenera este turno (ácido o fuego)")
            return
        if hp <= 0:
            hp = 0  # la regla 5e no tiene PV negativos
        if hp >= max_hp:
            return  # nada que curar
        curado = min(self.amount, max_hp - hp)
        try:
            actor.hp = hp + curado
        except Exception:
            return
        _log_line(ctx, f"{name} regenera {curado} PV (Regeneration) "
                       f"(HP {max(actor.hp, 0)}/{max_hp})")

    def survives_at_zero_hp(self, owner: Any) -> bool:
        # Muere en el turno en que empieza a 0 PV sin regenerarse; hasta
        # entonces sigue en pie (y sigue siendo un objetivo más).
        return self.amount > 0 and not self.dead

    def reset(self) -> None:
        self.blocked = False
        self.dead = False


@dataclass
class TurnResistance(Trait):
    """Turn Resistance (lich): ventaja en las salvaciones contra los
    efectos que convierten no-muertos.

    «The lich has advantage on saving throws against any effect that turns
    undead.» (API, SRD 2014). Solo se activa si la salvación llega marcada
    con ``kind="turn"``: hoy ningún efecto del motor convierte, así que el
    rasgo está cableado de punta a punta y probado, pero en reposo
    (# TODO: cuando exista Turn Undead deberá pasar ``kind="turn"``).
    """

    def modify_save_modifiers(self, mods: Any, target: Any, ability: str,
                              kind: str | None = None) -> None:
        if kind == "turn":
            mods.advantage_sources.append(self.name or "Turn Resistance")


#: Registro de rasgos modelables: nombre en minúsculas -> clase.
TRAIT_CLASSES: dict[str, type[Trait]] = {
    "blood frenzy": BloodFrenzy,
    "damage transfer": DamageTransfer,
    "heated body": HeatedBody,
    "martial advantage": MartialAdvantage,
    "pack tactics": PackTactics,
    "regeneration": Regeneration,
    "turn resistance": TurnResistance,
}


__all__ = ["Trait", "BloodFrenzy", "DamageTransfer", "HeatedBody",
           "MartialAdvantage", "PackTactics", "Regeneration",
           "TurnResistance", "TRAIT_CLASSES", "HOOK_NAMES", "hooks",
           "aliados_capaces"]

"""Definición del hechizo, datos del lanzador y
construcción de la acción a partir de la ficha."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ...model.actions import ActionType, CombatAction
from .actions import (HealAction, SpellAction, SpellAttackAction,
                      SpellFixedDamageAction, SpellStateAction)
from .effects import HealEffect


# Tabla de slots real de un **lanzador completo** (bardo, clérigo, druída,
# hechicero o mago: tabla PHB p. 113; el brujo de pacto tiene tabla propia).
# Índice = nivel de lanzador; valores = slots por nivel de hechizo 1..9.
FULL_CASTER_SLOTS: dict[int, tuple[int, ...]] = {
     1: (2, 0, 0, 0, 0, 0, 0, 0, 0),
     2: (3, 0, 0, 0, 0, 0, 0, 0, 0),
     3: (4, 2, 0, 0, 0, 0, 0, 0, 0),
     4: (4, 3, 0, 0, 0, 0, 0, 0, 0),
     5: (4, 3, 2, 0, 0, 0, 0, 0, 0),
     6: (4, 3, 3, 0, 0, 0, 0, 0, 0),
     7: (4, 3, 3, 1, 0, 0, 0, 0, 0),
     8: (4, 3, 3, 2, 0, 0, 0, 0, 0),
     9: (4, 3, 3, 3, 1, 0, 0, 0, 0),
    10: (4, 3, 3, 3, 2, 0, 0, 0, 0),
    11: (4, 3, 3, 3, 2, 1, 0, 0, 0),
    12: (4, 3, 3, 3, 2, 1, 0, 0, 0),
    13: (4, 3, 3, 3, 2, 1, 1, 0, 0),
    14: (4, 3, 3, 3, 2, 1, 1, 0, 0),
    15: (4, 3, 3, 3, 2, 1, 1, 1, 0),
    16: (4, 3, 3, 3, 2, 1, 1, 1, 0),
    17: (4, 3, 3, 3, 2, 1, 1, 1, 1),
    18: (4, 3, 3, 3, 3, 1, 1, 1, 1),
    19: (4, 3, 3, 3, 3, 2, 1, 1, 1),
    20: (4, 3, 3, 3, 3, 3, 2, 1, 1),
}


@dataclass
class Spellcasting:
    """Datos de lanzamiento de un lanzador de hechizos (de la API).

    ``ability_mod``: **modificador de característica** de lanzamiento (p. ej.
    +6 de INT). La API solo da ``modifier`` (bono de ataque = característica
    + competencia), así que ``parse_spellcasting`` lo deriva restando la
    competencia. Es el valor que usa el marcador ``MOD`` de la curación.
    """

    ability: str = "int"
    save_dc: int = 10
    attack_bonus: int = 0
    level: int = 5
    slots: dict = field(default_factory=dict)
    # Hechizos del lanzador: [{"name", "level", "url"}].
    spells: list = field(default_factory=list)
    # Modificador de característica (None = desconocido: se usa attack_bonus).
    ability_mod: int | None = None

    @property
    def heal_modifier(self) -> int:
        """MOD de la curación: modificador de característica si se conoce."""
        if self.ability_mod is not None:
            return int(self.ability_mod)
        return int(self.attack_bonus)

    def initialize_slots(self, caster_level: int = 1) -> None:
        """Rellena ``slots`` con la tabla real de un lanzador completo.

        - Nivel 0 (cantrips): None = usos infinitos.
        - Niveles 1..9: los slots de la tabla PHB para ``caster_level``
          (véase :data:`FULL_CASTER_SLOTS`). Un nivel de hechizo sin slots
          no se incluye (no se puede lanzar).
        """
        nivel = max(1, min(20, int(caster_level or 1)))
        tabla = FULL_CASTER_SLOTS[nivel]
        s = {0: None}  # cantrips infinitos
        for indice, cantidad in enumerate(tabla, start=1):
            if cantidad > 0:
                s[indice] = cantidad
        self.slots = s


@dataclass
class Spell:
    """Hechizo de la SRD 2014 con su efecto interpretado.

    ``kind`` dice qué efecto tiene:

    - ``"attack"``: ataque de hechizo (con ``elements`` elementos, cada uno
      contra un objetivo elegido al azar).
    - ``"save"``: daño con salvación (de objetivo único o de área).
    - ``"condition"``: deja una condición si el objetivo falla la salvación.
    - ``"heal"``: cura a un aliado herido.
    - ``""``: sin efecto modelable (utilidad, movimiento, etc.).
    """

    name: str
    index: str = ""
    level: int = 0
    school: str = ""
    casting_time: str = "1 action"
    range: str = ""
    duration: str = "Instantaneous"
    concentration: bool = False
    desc: list[str] = field(default_factory=list)
    # Tiempo de casteo -> tipo de acción (acción, acción bonus o reacción).
    action_type: ActionType = ActionType.ACTION
    # Nivel de slot por defecto con el que se lanza (0 = cantrip).
    slot_level: int = 0
    # --- Efecto ---
    kind: str = ""
    attack_type: str = ""        # "ranged" | "melee"
    damage: str = ""             # dados de daño (resueltos en slot_level)
    damage_type: str = "bludgeoning"
    elements: int = 1            # nº de elementos (rayos, dardos...)
    dc_ability: str = ""         # característica de la salvación
    dc_success: str = "none"     # "none" | "half"
    heal: str = ""               # dados de curación (resueltos en slot_level)
    condition: Any = None        # ConditionEffect
    state: Any = None            # StateEffect (hechizos de estado)
    state_target: str = ""       # "self" | "ally"
    damage_options: list = field(default_factory=list)  # opciones de daño
    area: bool = False
    ignored: str = ""            # motivo por el que no se modela
    # Tablas de escalado crudas de la API (para upcasting): nivel -> dados.
    # ``damage_table`` usa ``damage_at_character_level`` (cantrips) o
    # ``damage_at_slot_level`` (hechizos con slot); ``heal_table`` usa
    # ``heal_at_slot_level`` con el marcador ``MOD``.
    damage_table: dict = field(default_factory=dict)
    heal_table: dict = field(default_factory=dict)
    # Daño extra del ataque (True Strike 2024: +1d6/2d6/3d6 Radiante a
    # nivel 5/11/17), resuelto al parsear y copiado al ``Attack``.
    extra_damage: list = field(default_factory=list)
    # El ataque usa la característica del lanzador para el daño
    # (True Strike 2024: «uses your spellcasting ability for the attack
    # and damage rolls»).
    damage_bonus_from_ability: bool = False

    @property
    def is_cantrip(self) -> bool:
        """Los cantrips se lanzan cuantas veces se quiera."""
        return int(self.level) == 0


def dado_por_nivel(niveles: dict, nivel: int, modificador: int = 0) -> str:
    """Dados según el nivel del slot (o del lanzador en los cantrips).

    ``niveles`` es la tabla cruda de la API (``damage_at_slot_level``,
    ``damage_at_character_level`` o ``heal_at_slot_level``). Se elige la
    clave más alta <= ``nivel``; ``MOD`` se sustituye por ``modificador``.
    """
    if not isinstance(niveles, dict) or not niveles:
        return ""
    try:
        claves = sorted(int(k) for k in niveles)
    except (TypeError, ValueError):
        return ""
    elegido = None
    for k in claves:
        if k <= nivel:
            elegido = niveles[str(k)]
    if elegido is None:
        elegido = niveles[str(claves[0])]
    texto = str(elegido).replace("MOD", str(int(modificador)))
    return texto.replace(" ", "")


def duracion_en_rondas(duracion: str) -> int | None:
    """Duración de un hechizo en rondas (None = hasta el fin del combate)."""
    import re
    texto = str(duracion or "").lower()
    if "dispelled" in texto:
        return None
    if "round" in texto:
        return 1
    match = re.search(r"(\d+)\s*minute", texto)
    if match:
        return int(match.group(1)) * 10
    if "minute" in texto:
        return 10
    return None


def spell_action(spell: Spell, spellcasting: Spellcasting | None = None,
                 slot_level: int | None = None) -> CombatAction | None:
    """Construye la acción de combate de un hechizo.

    Reutiliza las acciones que ya existen: ``AttackAction`` (ataque de
    hechizo), ``SaveAction``/``AreaSaveAction`` (daño con salvación) y
    ``ConditionAction`` (condición con salvación).

    - El **tipo de acción** del hechizo (acción / acción bonus / reacción)
      se propaga al efecto interno, así que ambas capas coinciden y el
      hechizo se comprueba en su propia fase.
    - **No consume slots al construir**: el pool ``usage`` por nivel lo gasta
      el motor cuando el hechizo se lanza (``run_combat`` ->
      ``usage.spend()``).
    - ``slot_level`` prepara el **upcast**: se lanza en un slot de nivel >=
      que el del hechizo y el daño/la curación se reescalan con la tabla de
      la API. Por defecto se lanza en el nivel propio del hechizo.
    """
    if spell is None:
        return None
    from ...model.actions import AttackAction, SaveAction
    from ..area import AreaSaveAction, AreaTargeting
    from ...model.attack import Attack
    from ..conditions import ConditionAction
    from ..roll_modifiers import AttackRange
    from ..saves import SaveDamage

    sc = spellcasting or Spellcasting()
    nombre = spell.name
    # Nivel de slot usado: el propio del hechizo (o su slot por defecto) o
    # el del upcast pedido.
    nivel_propio = int(spell.slot_level or spell.level or 0)
    slot = nivel_propio
    if not spell.is_cantrip and slot_level is not None:
        slot = max(nivel_propio, int(slot_level))
    # Daño y curación del hechizo, reescalados al slot si hace upcast.
    dano = spell.damage
    cura = spell.heal
    if slot != nivel_propio:
        if spell.damage_table:
            dano = dado_por_nivel(spell.damage_table, slot) or dano
        if spell.heal_table:
            cura = (dado_por_nivel(spell.heal_table, slot, sc.heal_modifier)
                    or cura)
    # El efecto interno comparte el tipo de acción del hechizo.
    tipo = spell.action_type
    efecto = None

    if spell.kind == "attack":
        rango = AttackRange.RANGED if spell.attack_type == "ranged" else AttackRange.MELEE
        atk = Attack(
            name=nombre,
            damage=dano,
            ability=sc.ability,
            proficient=True,
            attack_bonus=int(sc.attack_bonus),
            # True Strike: el daño usa la característica del lanzador.
            damage_bonus=(int(sc.heal_modifier)
                          if spell.damage_bonus_from_ability else 0),
            damage_type=spell.damage_type,
            range_type=rango,
        )
        # Daño extra propio del hechizo (True Strike): sus dados también
        # se duplican en crítico (como cualquier daño extra del ataque).
        if spell.extra_damage:
            atk.extra_damage = list(spell.extra_damage)
        elementos = max(1, int(spell.elements or 1))
        if elementos == 1 and not spell.damage_options:
            efecto = AttackAction(atk, action_type=tipo, name=nombre)
        else:
            efecto = SpellAttackAction(
                spell=spell,
                attacks=[atk] * elementos,
                damage_options=list(spell.damage_options or []),
                action_type=tipo,
                name=nombre,
            )
    elif spell.kind == "save":
        eff = SaveDamage(
            ability=spell.dc_ability or "dex",
            dc=int(sc.save_dc),
            damage=dano,
            damage_type=spell.damage_type,
            on_success=spell.dc_success,
        )
        if spell.area:
            efecto = AreaSaveAction(
                name=nombre, effect=eff, targeting=AreaTargeting(),
                action_type=tipo,
            )
        else:
            efecto = SaveAction(
                name=nombre, effect=eff, action_type=tipo,
            )
    elif spell.kind == "condition":
        if spell.area:
            # De área (Sleep, Luz de hadas...): todos los objetivos.
            efecto = ConditionAction(
                name=nombre, effect=spell.condition,
                targeting=AreaTargeting(), es_area=True,
                action_type=tipo,
            )
        else:
            efecto = ConditionAction(
                name=nombre, effect=spell.condition,
                targeting=AreaTargeting(min_targets=1, max_targets=1),
                action_type=tipo,
            )
    elif spell.kind == "heal":
        efecto = HealAction(effect=HealEffect(cura), action_type=tipo,
                            name=nombre)
    elif spell.kind == "state":
        efecto = SpellStateAction(effect=spell.state, action_type=tipo,
                                  name=nombre)
    elif spell.kind == "fixed":
        efecto = SpellFixedDamageAction(
            damage=dano, damage_type=spell.damage_type,
            elements=max(1, int(spell.elements or 1)),
            action_type=tipo, name=nombre,
        )

    if efecto is None:
        return None

    return SpellAction(
        spell=spell,
        effect=efecto,
        concentration=bool(spell.concentration),
        duration_rounds=duracion_en_rondas(spell.duration),
        action_type=tipo,
        name=nombre,
    )

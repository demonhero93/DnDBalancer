"""Hechizos (D&D 5e): modelo, reglas y acciones de lanzamiento.

Estructura de los hechizos:

- :class:`Spell`: el hechizo con su efecto ya interpretado (datos de la API
  SRD 2014 + el efecto que el motor sabe aplicar).
- :class:`Spellcasting`: los datos del lanzador (característica, CD de
  salvación, bonificador y nivel), tal y como vienen en la API.
- :class:`SpellAction`: la acción de combate que lanza el hechizo: aplica la
  concentración (si el hechizo la requiere) y **delega** el efecto en las
  acciones que ya existen (``AttackAction``, ``SaveAction``,
  ``AreaSaveAction`` o ``ConditionAction``).
- :class:`HealAction`: la acción de curación.

Reglas implementadas:

- Los **cantrips** (nivel 0) se lanzan cuantas veces se quiera: no gastan
  slots ni usos por día y su daño escala con el **nivel del lanzador**.
- Los hechizos de nivel 1 o superior consumen un **slot** del nivel
  correspondiente **al lanzarse** (nunca al construir la acción): el pool de
  cada nivel se comparte entre los hechizos de ese nivel y lo gasta el motor
  de combate vía ``usage.spend()``. Se cargan hechizos de **todos los
  niveles** (0-9) que traiga la ficha.
- **Upcasting** (preparado): ``spell_action(spell, sc, slot_level=N)`` lanza
  el hechizo en un slot de nivel N (>= que el del hechizo); el daño y la
  curación se reescalan con la tabla del hechizo (``damage_at_slot_level`` /
  ``heal_at_slot_level``). Por defecto se lanza en su propio nivel.
- Se ignoran los hechizos con **tiempo de lanzamiento de 1 minuto o más**
  (no influyen en el combate).
- Se ignoran los hechizos que solo afectan al **movimiento** (propio o ajeno);
  si además hacen daño o dejan una condición, se conserva ese efecto y se
  ignora el movimiento (con aviso).
- Si el hechizo tiene **varias opciones o elementos**, se eligen al azar.
- Los hechizos de **curación** solo se lanzan contra un **aliado que ha
  perdido vida**, y su MOD usa el **modificador de característica** del
  lanzador (bono de ataque menos competencia), no el bono completo.
- El **tiempo de casteo** marca el tipo de acción: "1 action" -> acción,
  "1 bonus action" -> acción bonus, "1 reaction" -> reacción. El tipo de
  acción del hechizo se propaga al efecto interno, así que un hechizo de
  acción bonus o de reacción se comprueba (y se ejecuta) en su propia fase.
- Los **rituales** se ignoran (no se pueden usar en combate).
- Los hechizos que requieren **concentración** crean el estado
  ``CONCENTRATION`` en el lanzador (solo se mantiene una concentración a la
  vez).
- **Reacciones** (:func:`trigger_reaction`): cuando un combatiente recibe
  daño puede disparar una acción de reacción (p. ej. Hellish Rebuke). Como
  en las reglas, es **una reacción por turno propio**: se gasta al usarse y
  se recarga al inicio del turno (``begin_turn``).

# Reglas de slots (detalle):
# - El estado real de los slots vive en el pool ``ActionUsage`` por nivel que
#   construye ``build_spell_actions()`` (compartido por los hechizos de ese
#   nivel) y se gasta en ``run_combat`` con ``usage.spend()``.
# - ``Spellcasting.initialize_slots(nivel_de_lanzador)`` rellena
#   ``slots`` con la tabla real de un lanzador completo (útil para creadores
#   de monstruos/PJ sin datos de API); ``slots[0] = None`` = cantrips.
# - La recuperación de slots al descansar se modela con ``usage.reset()``,
#   que se llama en ``Combatant.reset()`` (un combate = un día descansado).
"""

from __future__ import annotations

from .effects import (HealEffect, StateEffect, apply_concentration,
                      chequeo_concentracion_al_danio)
from .reactions import trigger_reaction
from .actions import (HealAction, SpellAction, SpellAttackAction,
                      SpellFixedDamageAction, SpellStateAction)
from .casting import (ClassSpellList, FULL_CASTER_SLOTS, Spell,
                      Spellcasting, dado_por_nivel, duracion_en_rondas,
                      spell_action)
from .preparation import hechizo_soportado, preparar_hechizos
from .caster import (PCSpellcasting, PJSpellAction, aplicar_lanzamiento,
                     construir_acciones, estadisticas_lanzador)

__all__ = [
    "Spell",
    "Spellcasting",
    "ClassSpellList",
    "PCSpellcasting",
    "PJSpellAction",
    "aplicar_lanzamiento",
    "construir_acciones",
    "estadisticas_lanzador",
    "hechizo_soportado",
    "preparar_hechizos",
    "HealEffect",
    "StateEffect",
    "FULL_CASTER_SLOTS",
    "dado_por_nivel",
    "duracion_en_rondas",
    "spell_action",
    "SpellAction",
    "SpellAttackAction",
    "SpellFixedDamageAction",
    "SpellStateAction",
    "HealAction",
    "apply_concentration",
    "chequeo_concentracion_al_danio",
    "trigger_reaction",
]

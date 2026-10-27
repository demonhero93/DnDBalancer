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
  :func:`dnd_sim.rules.roll_modifiers.attack_modifiers` (la única fuente del modo
  de tirada), así que convive correctamente con los indicadores estáticos y
  las condiciones: si hay ventaja y desventaja a la vez se anulan.
- **Pack Tactics** (lobo) y **Martial Advantage** (hobgoblin): la condición
  es de **posición** (un aliado no incapacitado cerca del objetivo), que el
  motor no modela, así que la decisión es **aleatoria**: si el atacante
  tiene aliados capaces se sortea (50 %) y si no tiene ninguno nunca aplica
  (véase :func:`_condicion_posicional`). El daño extra de Martial Advantage
  usa el hook ``extra_attack_damage`` y entra en el ataque **antes** de la
  inmunidad/resistencia del objetivo.
- **Parry** (hobgoblin warlord, gladiador, caballero, noble, erinyes,
  marilith): +N de CA contra **un ataque cuerpo a cuerpo que iba a entrar**.
  El hook ``defensive_ac_bonus`` se le pregunta en
  :func:`dnd_sim.engine.combat.attack_roll` solo en ese caso, recibe la tirada y
  la CA para no gastar la reacción en un golpe que igual entra, y consume
  la reacción del combatiente (``state.reaction_used``), que se recarga en
  su propio turno.
- **Damage Transfer** (cloaker): mientras esté enganchado, el daño que
  recibe se parte en dos: él baja la mitad (redondeada hacia abajo) y la
  criatura enganchada se lleva la otra mitad, que además pasa por sus
  **propios** modificadores (resistencia/inmunidad/vulnerabilidad). Los
  hooks viven en :func:`dnd_sim.rules.damage.inflict_damage` (fases 1 y 2); el
  enganche en sí lo modela :mod:`dnd_sim.rules.attach`.
- **Heated Body** (azer): quien lo golpea cuerpo a cuerpo recibe 1d10 de
  daño de fuego. El trigger es el **impacto**, así que el hook vive en
  :func:`dnd_sim.engine.combat.attack_roll` (``after_being_hit``) y se activa
  aunque el daño sea 0 por inmunidad.
- **Regeneration** (troll): recupera 10 PV al inicio de su turno salvo que
  haya recibido daño de ácido o fuego desde su turno anterior. A 0 PV **no
  se regenera**: muere al empezar su turno (si no, el troll se salvaría
  siempre del golpe que lo deja a cero) (hooks ``on_turn_start``,
  ``after_damage_taken``, ``survives_at_zero_hp`` y ``reset``).
- **Relentless** (jabalí, jabalí gigante, hombre lobo): si el daño que lo
  dejaría a 0 no pasa de su umbral (7 el jabalí, 10 el gigante, 14 el
  hombre lobo) queda a 1 PV. Con uso limitado de la ficha («recharge after
  rest» = un uso por combate). Usa el hook ``on_reduced_to_zero_hp``, que
  se resuelve **al aplicar el daño**, no en el turno.
- **Superior Invisibility** (pixie): su acción de volverse invisible
  (hook ``extra_actions``), que deja la condición invisible **sin** que se
  pierda al atacar ni al lanzar un hechizo: la diferencia con el hechizo
  Invisibility está en ``ConditionInstance.break_on_attack``.
- **Turn Resistance** (lich): ventaja en las salvaciones contra un efecto
  que convierte no-muertos. Esa ventaja solo llega si la salvación se pide
  con ``kind="turn"``; hoy ningún efecto del motor lo hace (# TODO: Turn
  Undead), así que el rasgo está cableado y probado pero sin consumidor.
- **Undead Fortitude** (zombi, zombi ogro): salvación de CON al caer a 0
  PV (DC 5 + daño recibido, salvo que sea radiante o venga de un crítico)
  para quedar a 1 PV. Consumidora del mismo hook ``on_reduced_to_zero_hp``
  que Relentless, pero tirando con :func:`dnd_sim.rules.saves.saving_throw`.

Catálogo de hooks (un único punto de despacho: :func:`hooks`)

============================  ======================================================
Hook                          Dónde se dispara
============================  ======================================================
``modify_attack_modifiers``   :func:`dnd_sim.rules.roll_modifiers.attack_modifiers`
``modify_save_modifiers``     :func:`dnd_sim.rules.roll_modifiers.save_modifiers`
``modify_check_modifiers``    :func:`dnd_sim.rules.roll_modifiers.check_modifiers`
``modify_incoming_damage``    :func:`dnd_sim.rules.damage.inflict_damage` (fase 1)
``after_damage_taken``        :func:`dnd_sim.rules.damage.inflict_damage` (fase 2)
``after_being_hit``           :func:`dnd_sim.engine.combat.attack_roll`
``extra_attack_damage``       :func:`dnd_sim.engine.combat.attack_roll`
``defensive_ac_bonus``        :func:`dnd_sim.engine.combat.attack_roll` (si iba a entrar)
``on_turn_start``             :func:`dnd_sim.rules.usage.begin_turn`
``survives_at_zero_hp``       :attr:`dnd_sim.model.combatant.Combatant.alive`
``on_reduced_to_zero_hp``     :func:`dnd_sim.rules.damage.inflict_damage` (al bajar a 0)
``extra_actions``             :class:`dnd_sim.model.combatant.Monster` (al construirse)
``reset``                     :meth:`dnd_sim.model.combatant.Combatant.reset`
============================  ======================================================

Cómo añadir un rasgo nuevo (p. ej. Web Sense):

1. Crea la clase en este módulo sobrescribiendo **solo** los hooks que
   necesite; los que no sobrescriba no se llaman nunca (la base
   :class:`Trait` los define como no-op).
2. Regístrala en :data:`TRAIT_CLASSES` con su nombre en minúsculas.
3. Nada más: ``parse_traits()`` la detectará en ``special_abilities``.
4. Si el rasgo saca números de su descripción («regains 10 hit points»),
   que la propia clase los interprete en ``__post_init__`` a partir de
   ``self.desc``: ``parse_traits`` solo pasa nombre y descripción. Sí
   pasa además el campo ``usage`` de la ficha **si la clase lo declara**
   (es el caso de Relentless, que se gasta una vez por combate): el
   ``dict`` crudo de la API se convierte en ``ActionUsage`` en el parser.
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
#
# Pendientes de resolver más adelante, con su forma de implementarlos:
#
# - **Possession** (ghost, acción con recarga 6): «... must succeed on a DC
#   13 Charisma saving throw or be possessed by the ghost; the ghost then
#   disappears, and the target is incapacitated and loses control of its
#   body». Es el mayor de los cuatro porque **cambia el controlador** de un
#   combatiente. Sketch:
#     1. Estado nuevo en ``CombatState``: ``possessed_by`` (el fantasma) y
#        ``original_body``. El cuerpo poseído queda incapacitado (ya existe
#        ``Condition.INCAPACITATED``) y el fantasma deja de ser objetivo:
#        ``valid_targets`` hoy solo mira equipo y hostilidad, así que
#        habría que excluirlo ahí mientras dure.
#     2. ``_run_combat`` tendría que resolver el turno del cuerpo con las
#        acciones y la política del poseedor (hoy cada combatiente usa las
#        suyas) y no contar al fantasma como combatiente activo.
#     3. Fin de la posesión (0 PV del cuerpo, acción bonus del fantasma,
#        ser «turned», ``dispel evil and good``): el fantasma reaparece a
#        5 ft. y el cuerpo recupera el control; además, inmunidad de ese
#        cuerpo a esta posesión durante 24 h tras fallar o acabar (otro
#        estado con caducidad).
#     4. Falta posición para «within 5 ft.» (mismo bloqueo que Stench);
#        podría aproximarse por «a cuerpo a cuerpo» mientras no haya
#        coordenadas.
#
# - **Nimble Escape** (goblin): «The goblin can take the Disengage or Hide
#   action as a bonus action on each of its turns.» Sketch: dos acciones
#   nuevas con ``ActionType.BONUS_ACTION`` (el tipo ya existe y
#   ``_run_combat`` ya ejecuta una acción bonus por turno):
#     a) **Hide**: hoy no hay estado de «oculto». Lo más parecido es
#        INVISIBLE, pero eso da ventaja/desventaja de combate, no una
#        prueba de Sigilo: haría una tirada de ``ability_check(...,
#        skill="stealth")`` contra la percepción pasiva del enemigo, que
#        tampoco existe (``modify_check_modifiers`` ya recibe ``skill``,
#        pero nada tira Sigilo todavía). Mientras eso se decide, la salida
#        razonable es modelar «oculto» como una condición nueva con sus
#        efectos de tirada.
#     b) **Disengage**: sin desplazamiento no hay reacciones de
#        oportunidad que evitar (solo se modelan reacciones por daño con
#        ``trigger_reaction``), así que hoy sería un no-op. Con un modelo
#        de movimiento bastaría con marcar ``state.disengaged`` hasta el
#        final del turno y consultarlo ahí antes de disparar la reacción.
#
# - **Shadow Stealth** (shadow / shadow demon): «While in dim light or
#   darkness, the shadow can take the Hide action as a bonus action.»
#   Sketch: encadena lo anterior (necesita la acción Hide) **más** un
#   modelo de luz: hay que poder decir si la escena está en penumbra o a
#   oscuras, que es exactamente el bloqueo por el que se ignoran por
#   decisión Sunlight Sensitivity y Light Sensitivity (no hay campo de
#   entorno en el combate). Resuelto «Hide», el rasgo es barato: comprobar
#   el estado de luz y ofrecer la acción como bonus. La ficha del Shadow sí
#   está en ``cache/monsters/shadow.json`` (la del shadow demon no).
#
# - **Stench** (troglodyte): aura a 5 ft.: cada criatura que empieza su
#   turno ahí debe superar una salvación de CON o queda envenenada hasta
#   el final de su turno. Sketch:
#     1. Posición: el motor solo distingue «cuerpo a cuerpo / a distancia»
#        (``state.at_range``), que sería una aproximación muy burda para
#        «within 5 ft.»: sin coordenadas este es el bloqueo principal.
#     2. Con posición, sería un hook nuevo de aura, lo más natural en
#        ``usage.begin_turn`` (al empezar el turno propio, mirar a quién
#        hay en alcance) recorriendo ``ctx.combatants`` y pidiendo la
#        salvación con ``saving_throw(..., kind="stench")``.
#     3. El efecto ya existe: ``Condition.POISONED`` con duración de un
#        turno (el mismo mecanismo que usan los riders de condición), así
#        que lo que falta es el aura, no el resultado. La ficha no está ni
#        en la caché ni en la API.
"""

from __future__ import annotations

from .base import HOOK_NAMES, Trait, hooks
from .defense import (DamageTransfer, HeatedBody, Parry,
                      TurnResistance)
from .offense import (BloodFrenzy, MartialAdvantage, PackTactics,
                      aliados_capaces)
from .stealth import SuperiorInvisibility
from .survival import Regeneration, Relentless, UndeadFortitude


#: Registro de rasgos modelables: nombre en minúsculas -> clase.
TRAIT_CLASSES: dict[str, type[Trait]] = {
    "blood frenzy": BloodFrenzy,
    "damage transfer": DamageTransfer,
    "heated body": HeatedBody,
    "martial advantage": MartialAdvantage,
    "pack tactics": PackTactics,
    "parry": Parry,
    "regeneration": Regeneration,
    "relentless": Relentless,
    "superior invisibility": SuperiorInvisibility,
    "turn resistance": TurnResistance,
    "undead fortitude": UndeadFortitude,
}

__all__ = ["Trait", "BloodFrenzy", "DamageTransfer", "HeatedBody",
           "MartialAdvantage", "PackTactics", "Parry", "Regeneration",
           "Relentless", "SuperiorInvisibility", "TurnResistance",
           "UndeadFortitude", "TRAIT_CLASSES", "HOOK_NAMES", "hooks",
           "aliados_capaces"]

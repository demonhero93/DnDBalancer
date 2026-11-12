"""Subclase Champion (Campeón, PHB 2024) del Guerrero.

Rasgos por nivel (Fighter 3 / 7 / 10 / 15 / 18):

- **Improved Critical** (3): las tiradas de ataque con arma pueden ser
  un Impacto Crítico con 19 o 20 en el d20. El umbral lo consulta el
  motor con ``ChampionFeatures.umbral_critico`` (helper
  ``evaluar_d20``/``umbral_critico`` de ``rules/roll_modifiers.py``;
  ver A3 en ``TODO.md``). Un 1 natural sigue fallando siempre y los
  ataques de hechizo no usan el umbral (campo ``spell_attack``).
- **Remarkable Athlete** (3): ventaja en iniciativa
  (``ventaja_iniciativa()``, duck-typing en ``roll_initiative``) y en
  pruebas de Atletismo (``modify_check_modifiers``, patrón Furia);
  ambas se anulan con desventaja por la regla estándar. No concede
  competencia en Atletismo. Moverse hasta la mitad de la velocidad
  tras un crítico es dato sin efecto (``# TODO``: sin movimiento).
- **Additional Fighting Style** (7): un segundo Estilo de Combate,
  elegido con ``pick`` o con el kwarg ``additional_fighting_style``
  validado; entra en la propiedad ``estilos`` de ``FighterFeatures``
  (ambos estilos funcionan a la vez) y su mutación Defense (+1 CA)
  se aplica una sola vez al aplicarlo.
- **Heroic Warrior** (10): gana Inspiración Heroica al inicio de cada
  turno si no la tiene → dato sin efecto (el sim no modela la
  Inspiración Heroica); congelado con test freeze.
- **Superior Critical** (15): el umbral crítico baja a 18.
- **Survivor** (18): **Defy Death** (ventaja y 18-20 en salvaciones de
  muerte) → dato sin efecto (sin salvaciones de muerte: un PJ a 0 PG
  muere o queda fuera), congelado con test freeze. **Heroic Rally**
  (A6): al inicio de cada turno propio, si está Bloodied
  (``pg * 2 <= pg_max``) y con al menos 1 PG, recupera
  ``heroic_rally_amount(mod CON)`` PG sin pasar de los máximos.

Registro: clave ``"champion"`` en ``fighter/__init__.py``. Ver
``TODO.md`` (plan «Champion») y las entradas de
``PASOS-ANTERIORES.txt``.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from .....core.classes import (
    FIGHTER_STYLES,
    MAX_LEVEL,
    MIN_LEVEL,
    champion_crit_threshold,
    heroic_rally_amount,
)
from .....core.log import log_line as _log_line
from .....core.randomness import pick
from ....traits.base import Trait
from ..features import FighterFeatures

#: RNG con semilla fija para elegir el segundo Estilo de Combate cuando
#: el llamante no pasa ``rng``: crea el personaje siempre igual
#: (reproducible, patrón del resto de subclases).
_RNG_CREACION = random.Random(0)


def _de(actor: Any, clase: type) -> Any:
    """Primer trait de ``clase`` que lleve ``actor`` (o ``None``)."""
    for trait in getattr(actor, "traits", None) or []:
        if isinstance(trait, clase):
            return trait
    return None


@dataclass
class ChampionFeatures(Trait):
    """Rasgos de la subclase Champion y sus datos de ficha.

    Sin estado de combate propio hasta Heroic Rally (A6): el ciclo de
    vida ``reset``/``on_turn_start`` lo heredado del :class:`Trait`
    basta hasta entonces.
    """

    # Nivel del personaje (manda en las tablas de rasgos).
    level: int = MIN_LEVEL
    # Datos sin efecto congelados (decisión del maintainer): Heroic
    # Warrior (10, sin Inspiración Heroica en el modelo) y Defy Death
    # (18, sin salvaciones de muerte). El movimiento tras un crítico de
    # Remarkable Athlete también es dato sin efecto (sin movimiento).
    heroic_warrior: bool = True
    defy_death: bool = True
    # Dueño (guards de hooks y despacho de ``on_turn_start``).
    owner: Any = field(default=None, repr=False, compare=False)

    def umbral_critico(self, atk: Any = None) -> int:
        """Rango crítico del Champion (Improved/Superior Critical).

        Mínimo d20 que cuenta como Impacto Crítico en un ataque **con
        arma** de este combatiente: 19 desde el nivel 3 y 18 desde el
        15. Un ataque de hechizo (``atk.spell_attack``) no usa el
        umbral; un 1 natural sigue fallando siempre (lo decide
        ``evaluar_d20``). El helper solo consulta los rasgos del
        ATACANTE, así que un atacante ajeno (sin la subclase) ve 20.
        """
        if self.level < 3:
            return 20
        if atk is not None and bool(getattr(atk, "spell_attack", False)):
            return 20
        # TODO: al conseguir un crítico, moverte hasta la mitad de tu
        # velocidad sin provocar ataques de oportunidad (dato sin
        # efecto: el sim no modela velocidad ni movimiento).
        return champion_crit_threshold(self.level)

    def ventaja_iniciativa(self) -> bool:
        """Remarkable Athlete: ventaja en la tirada de iniciativa (3+).

        Lo consulta ``roll_initiative`` por duck-typing (sin RNG en sí:
        el motor decide el modo). Se anula con desventaja por la regla
        estándar; sin la subclase el motor ni lo consulta.
        """
        return self.level >= 3

    def modify_check_modifiers(self, mods: Any, target: Any, ability: str,
                               skill: str | None = None) -> None:
        """Remarkable Athlete: ventaja en pruebas de Atletismo (3+).

        Patrón Furia del bárbaro: solo el dueño y solo la habilidad
        ``athletics`` (no concede competencia). La ventaja se anula con
        desventaja en ``CheckModifiers.mode``; otras habilidades y
        pruebas puras de característica no reciben nada.
        """
        if self.level < 3 or target is not self.owner:
            return
        if skill == "athletics":
            mods.advantage_sources.append("Atleta notable")

    def on_turn_start(self, actor: Any, ctx: Any = None) -> None:
        """Heroic Rally (18): cura al inicio de cada turno propio.

        Sin RNG y sin decisión: si el dueño está vivo, tiene al menos
        1 PG y está Bloodied (``pg * 2 <= pg_max``), recupera
        ``heroic_rally_amount(mod CON)`` PG recortado a los PG
        máximos. Heroic Warrior (10) es dato sin efecto: el sim no
        modela la Inspiración Heroica.
        """
        if self.level < 18 or actor is not self.owner:
            return
        if not getattr(actor, "alive", True):
            return
        pg = int(getattr(actor, "hp", 0) or 0)
        pg_max = int(getattr(actor, "max_hp", 0) or 0)
        if pg < 1 or pg * 2 > pg_max:
            return  # no está Bloodied o ya no queda nada que curar
        con_mod = int(actor.abilities.mod("con"))
        cura = min(heroic_rally_amount(con_mod), pg_max - pg)
        if cura <= 0:
            return  # CON tan baja que la tabla da 0
        actor.hp = pg + cura  # nunca por encima de los PG máximos
        _log_line(ctx, f"{getattr(actor, 'name', actor)} recupera "
                       f"{cura} PG con Heroic Rally")


def apply_champion(pj: Any, level: int | None = None,
                   rng: random.Random | None = None,
                   additional_fighting_style: str | None = None
                   ) -> ChampionFeatures:
    """Aplica la subclase Champion a un PJ Guerrero.

    Exige que ``pj`` ya tenga :class:`FighterFeatures`
    (:func:`apply_fighter`) y nivel >= 3. ``additional_fighting_style``
    (Additional Fighting Style, nivel 7+) se VALIDA siempre: debe ser un
    Estilo de ``FIGHTER_STYLES`` y distinto del que ya tiene el PJ; sin
    kwarg, el segundo estilo se elige con ``pick`` uniforme entre el
    pool menos el primero. ``rng`` por defecto con semilla 0 (patrón
    del resto de subclases). Como ``apply_class`` no reenvía ``**kwargs``
    a la subclase, el kwarg se pasa llamando a ``apply_champion``
    directamente (mismo criterio que ``rng`` en Cavalier).
    """
    fighter = _de(pj, FighterFeatures)
    if fighter is None:
        raise ValueError(
            "Primero aplica la clase guerrero con apply_fighter(pj)."
        )
    lvl = level if level is not None else getattr(pj, "level", None)
    lvl = MIN_LEVEL if lvl is None else max(MIN_LEVEL, min(MAX_LEVEL, int(lvl)))
    if lvl < 3:
        raise ValueError(
            f"Champion requiere nivel >= 3: llegó {lvl}."
        )
    if additional_fighting_style is not None:
        if additional_fighting_style not in FIGHTER_STYLES:
            raise ValueError(
                f"{additional_fighting_style!r} no es un Estilo de "
                f"Combate de la clase Guerrero: opciones "
                f"{sorted(FIGHTER_STYLES)}."
            )
        if additional_fighting_style == fighter.estilo:
            raise ValueError(
                "Additional Fighting Style repite el Estilo de Combate "
                f"que ya tiene el PJ ({fighter.estilo!r}): una dote no se "
                "toma dos veces."
            )
    # Additional Fighting Style (7): el segundo estilo entra en la
    # propiedad ``estilos`` (los hooks la consultan) y su mutación
    # Defense (+1 CA) se aplica UNA vez aquí —el pool excluye el
    # primero—. Por debajo del nivel 7 no se concede nada (y el kwarg
    # validado arriba tampoco se aplica).
    if lvl >= 7:
        generador = rng if rng is not None else _RNG_CREACION
        pool = tuple(s for s in FIGHTER_STYLES if s != fighter.estilo)
        segundo = (additional_fighting_style
                   if additional_fighting_style is not None
                   else pick(generador, pool))
        fighter.estilos_extra.append(segundo)
        if segundo == "Defense":
            pj.ac += 1
    trait = ChampionFeatures(name="Champion", level=lvl)
    trait.owner = pj
    pj.traits.append(trait)
    return trait


__all__ = ["ChampionFeatures", "apply_champion"]

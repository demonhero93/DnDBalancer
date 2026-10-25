"""Interpreta el JSON de los hechizos de la API (dnd5eapi.co, SRD 2014).

Formato real (verificado sobre los hechizos de la SRD 2014):

.. code-block:: json

    {"name": "Ray of Frost", "index": "ray-of-frost", "level": 0,
     "casting_time": "1 action", "range": "60 feet",
     "components": ["V", "S"], "duration": "Instantaneous",
     "concentration": false, "ritual": false, "school": "evocation",
     "attack_type": "ranged",
     "damage": [{"damage_type": {"index": "cold"},
                 "damage_at_character_level": {"1": "1d8", "5": "2d8",
                                               "11": "3d8", "17": "4d8"}}],
     "desc": ["A frigid beam of blue-white light streaks toward a creature
               within range. Make a ranged spell attack against the target.
               On a hit, it takes 1d8 cold damage, and its speed is reduced
               by 10 feet until the start of your next turn."]}

Claves a tener en cuenta:

- El **daño** de un cantrip viene en ``damage_at_character_level`` (según el
  nivel del lanzador) y el de un hechizo con slot en ``damage_at_slot_level``.
- La **curación** viene en ``heal_at_slot_level``, con el marcador ``MOD``
  donde va el bonificador del lanzador.
- La **CD** de las salvaciones no está en el hechizo: la tiene el lanzador
  (``spellcasting.dc``). El hechizo solo dice la característica y si el
  éxito reduce el daño (``dc.dc_success``).
- El **número de elementos** (rayos, dardos...) solo aparece en el texto.

# TODO: los patrones de texto son frágiles (texto libre de la API).
"""
from __future__ import annotations

import re
import warnings
from typing import Any

from ..model.actions import ActionType
from ..rules.conditions import Condition, ConditionEffect, EXCLUDED_CONDITIONS
from ..rules.saves import normalize_ability
from ..rules.spells import (
    Spell, Spellcasting, StateEffect, dado_por_nivel, duracion_en_rondas
)
from .area_classifier import is_area_action
from .condition_parser import CONDITION_KEYWORDS, REPEAT_SAVE_RE
from .escape_parser import parse_escape

# Tiempo de lanzamiento: 1 minuto o más no influye en el combate.
LONG_CASTING_RE = re.compile(r"\b(\d+)\s*(minute|hour|day)s?\b", re.IGNORECASE)

# Tiempo de casteo -> tipo de acción (vocabulario cerrado).
CASTING_TIME_ACTIONS: dict[str, str] = {
    "1 action": "action",
    "1 bonus action": "bonus_action",
    "1 reaction": "reaction",
}

# Hechizos que crean objetos (si no hacen daño ni dejan estado: se omiten).
CREATE_MARKERS: tuple[str, ...] = (
    "you create", "you conjure", "appear in your hand", "appear in your hands",
)

# Escuela de las ilusiones (se omiten si no dejan estado en el rival).
ILLUSION_SCHOOL = "illusion"

# Dano directo a un objetivo (no un bonus a los ataques del lanzador):
# "A dart deals 1d4 + 1 force damage to its target".
DIRECT_DAMAGE_RE = re.compile(
    r"damage to (?:its|the) target|takes? [\w\d+ ]*damage", re.IGNORECASE)

# Efecto por puntos de vida ("Roll 5d8; the total is how many hit points of
# creatures this spell can affect"): no se modela.
HP_THRESHOLD_RE = re.compile(
    r"how many hit points of creatures", re.IGNORECASE)

# Palabras que delatan un efecto sobre el movimiento (se buscan como
# palabras completas: "firefly" no es "fly").
MOVEMENT_MARKERS: tuple[str, ...] = (
    "speed", "teleport", "dash", "levitate", "push", "pull", "shove",
    "knock", "swim", "jump", "walk", "fly", "flying", "movement", "descent",
)
MOVEMENT_RES = tuple(re.compile(rf"\b{re.escape(m)}\b", re.IGNORECASE)
                     for m in MOVEMENT_MARKERS)

# Elementos de un hechizo ("three rays of fire", "four beams at 17th level").
ELEMENT_BY_LEVEL_RE = re.compile(
    r"\b(two|three|four|five)\s+(?:beams|rays|darts|bolts)\s+at\s+(\d+)"
    r"(?:st|nd|rd|th)\s+level", re.IGNORECASE)
ELEMENT_RE = re.compile(
    r"\b(two|three|four|five|six)\s+(?:beams|rays|darts|bolts)\b", re.IGNORECASE)
# "Make a separate attack roll for each beam" / "attack for each ray".
SEPARATE_ELEMENTS_RE = re.compile(
    r"(?:attack roll for each|attack for each)", re.IGNORECASE)

# La API no siempre trae ``attack_type`` (p. ej. Scorching Ray): si el texto
# dice "ranged spell attack" / "melee spell attack" se trata como ataque.
SPELL_ATTACK_RE = re.compile(r"\b(ranged|melee)\s+spell attack\b", re.IGNORECASE)

# Hechizos que dejan un estado (vocabulario cerrado):
# nombre -> (condición, objetivo "self" | "ally" | "enemy", ¿salvación?).
SPELL_STATES: dict[str, tuple[str, str, bool]] = {
    "guidance": ("guided", "ally", False),
    "true strike": ("true_struck", "self", False),
    "charm person": ("charmed", "enemy", True),
    "faerie fire": ("marked", "enemy", True),
    # Enlarge/Reduce: se modela la variante Agrandar al propio lanzador
    # (auto-aplicada, sin salvación); la salvación CON contra un objetivo
    # no dispuesto no se modela. Comparte el estado ENLARGED con el rasgo
    # del duergar (dnd_sim.data.loader._STATE_BUFF_ACTIONS).
    "enlarge/reduce": ("enlarged", "self", False),
}

# Estado de "hechizado": "it is charmed by you until the spell ends".
CHARMED_RE = re.compile(r"\bis charmed by\b", re.IGNORECASE)
# Repeticion de la salvacion: "can make another wisdom saving throw".
SPELL_REPEAT_SAVE_RE = re.compile(
    r"(?:repeat|make another)\s+(?:\w+\s+)?saving throw", re.IGNORECASE)

NUMBER_WORDS: dict[str, int] = {
    "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
}


def _warn(monster_name: str, spell_name: str, motivo: str) -> None:
    """Avisa de que un hechizo se ignora (con su motivo)."""
    warnings.warn(
        f"Hechizo {spell_name!r} de {monster_name!r}: {motivo}. Se omite. "
        f"# TODO: modelar si procede.",
        stacklevel=3,
    )


# --- Datos del lanzador ---------------------------------------------------- #

def parse_spellcasting(monster_json: dict) -> Spellcasting | None:
    """Datos de lanzamiento del monstruo (``special_abilities``).

    El **modificador de característica** (``ability_mod``) se deriva del
    bono de ataque de la API restando la competencia (la API solo da el
    bono completo). Es el ``MOD`` de la curación: ``1d8 + MOD``.
    """
    for ability in monster_json.get("special_abilities") or []:
        if not isinstance(ability, dict):
            continue
        if str(ability.get("name") or "").strip().lower() != "spellcasting":
            continue
        data = ability.get("spellcasting") or {}
        ab = data.get("ability") or {}
        index = ab.get("index") if isinstance(ab, dict) else ab
        modifier = data.get("modifier")
        proficiency = monster_json.get("proficiency_bonus")
        ability_mod = None
        if modifier is not None and proficiency is not None:
            try:
                ability_mod = int(modifier) - int(proficiency)
            except (TypeError, ValueError):
                ability_mod = None
        return Spellcasting(
            ability=str(index or "int"),
            save_dc=int(data.get("dc") or 10),
            attack_bonus=int(modifier or 0),
            level=int(data.get("level") or 5),
            slots=dict(data.get("slots") or {}),
            spells=list(data.get("spells") or []),
            ability_mod=ability_mod,
        )
    return None


# --- Utilidades de datos --------------------------------------------------- #

# La resolución de dados por nivel vive en el módulo de reglas
# (``spells.dado_por_nivel``); aquí se conserva el alias interno.
_dado_por_nivel = dado_por_nivel


def _dados_de_dano(entries: list, nivel: int, slot: int = 0) -> str:
    """Dados de daño de la primera entrada con daño.

    El daño de un **cantrip** escala con el nivel del lanzador
    (``damage_at_character_level``) y el de un hechizo con slot con el nivel
    del **slot** usado (``damage_at_slot_level``).
    """
    for entry in entries or []:
        if not isinstance(entry, dict):
            continue
        if isinstance(entry.get("damage_at_character_level"), dict):
            dados = _dado_por_nivel(entry["damage_at_character_level"], nivel)
            if dados:
                return dados
        if isinstance(entry.get("damage_at_slot_level"), dict):
            dados = _dado_por_nivel(entry["damage_at_slot_level"], slot or 1)
            if dados:
                return dados
        for key in ("damage_dice", "damage", "dice"):
            if entry.get(key):
                return str(entry[key]).replace(" ", "")
    return ""


def _tabla_de_dano(entries: list) -> dict:
    """Tabla cruda de escalado del daño (guardada en ``Spell.damage_table``).

    Misma precedencia que :func:`_dados_de_dano`: primero
    ``damage_at_character_level`` (cantrips: escalan con el lanzador) y
    después ``damage_at_slot_level`` (hechizos con slot: escalan con el
    slot, incluido el upcast).
    """
    for entry in entries or []:
        if not isinstance(entry, dict):
            continue
        for key in ("damage_at_character_level", "damage_at_slot_level"):
            tabla = entry.get(key)
            if isinstance(tabla, dict) and tabla:
                return dict(tabla)
    return {}


def _opciones_de_dano(entries: list) -> list[str]:
    """Opciones de daño (formato ``{"choose": n, "from": {...}}``)."""
    opciones = []
    for entry in entries or []:
        if not isinstance(entry, dict):
            continue
        from_opts = entry.get("from")
        if isinstance(from_opts, dict):
            for opt in from_opts.get("options") or []:
                if not isinstance(opt, dict):
                    continue
                for key in ("damage_dice", "damage", "dice"):
                    if opt.get(key):
                        opciones.append(str(opt[key]).replace(" ", ""))
    return opciones


def _tipo_de_dano(entries: list) -> str:
    """Tipo de daño de la primera entrada con daño."""
    for entry in entries or []:
        if not isinstance(entry, dict):
            continue
        dt = entry.get("damage_type") or {}
        if isinstance(dt, dict):
            index = dt.get("index") or dt.get("name")
            if index:
                return str(index).lower()
        elif isinstance(dt, str) and dt:
            return dt.lower()
    return "bludgeoning"


def _dc_ability(dc_info: dict) -> str:
    """Característica de la salvación del hechizo."""
    tipo = dc_info.get("dc_type") or {}
    index = tipo.get("index") if isinstance(tipo, dict) else tipo
    try:
        return normalize_ability(index) if index else "dex"
    except Exception:
        return "dex"


def _numero_elementos(texto: str, nivel: int) -> int:
    """Nº de elementos de un hechizo (rayos, dardos,dardos...)."""
    if not SEPARATE_ELEMENTS_RE.search(texto):
        return 1
    mejor = None
    for match in ELEMENT_BY_LEVEL_RE.finditer(texto):
        lvl = int(match.group(2))
        if lvl <= nivel and (mejor is None or lvl >= mejor[0]):
            mejor = (lvl, NUMBER_WORDS.get(match.group(1).lower(), 1))
    if mejor is not None:
        return mejor[1]
    match = ELEMENT_RE.search(texto)
    if match is not None:
        return NUMBER_WORDS.get(match.group(1).lower(), 1)
    return 1


def _crea_objetos(texto: str) -> bool:
    """¿El hechizo crea objetos? (si no hacen daño ni efecto, se omiten)."""
    low = str(texto or "").lower()
    return any(marker in low for marker in CREATE_MARKERS)


def _es_ilusion(raw: dict) -> bool:
    """¿El hechizo pertenece a la escuela de la ilusión?"""
    school = raw.get("school") or ""
    index = school.get("index") if isinstance(school, dict) else str(school)
    return str(index or "").lower() == ILLUSION_SCHOOL


def _elementos_totales(texto: str) -> int:
    """Nº de elementos de un hechizo (dardos, dardos...) aunque no sean
    ataques independientes."""
    match = ELEMENT_RE.search(str(texto or ""))
    if match is not None:
        return NUMBER_WORDS.get(match.group(1).lower(), 1)
    return 1


def _afecta_movimiento(texto: str) -> bool:
    """¿El hechizo afecta al movimiento (propio o ajeno)?"""
    return any(p.search(str(texto or "")) for p in MOVEMENT_RES)


def _condicion_con_salvacion(texto: str, nombre: str, monster_name: str,
                              ability: str, dc: int,
                              duracion: int | None) -> ConditionEffect | None:
    """Condición que deja un hechizo con salvación (vocabulario cerrado).

    La duración es la del **hechizo** ("Until dispelled", "1 minute"...), no
    la del texto de la acción.
    """
    repeat = bool(REPEAT_SAVE_RE.search(texto) or SPELL_REPEAT_SAVE_RE.search(texto))
    escape = parse_escape(texto, monster_name, nombre)
    for clave, condicion in CONDITION_KEYWORDS.items():
        if clave in EXCLUDED_CONDITIONS:
            continue
        if clave == "charmed":
            # Solo el hechizo de hechizar (vocabulario cerrado) deja CHARMED.
            continue
        patron = (rf"saving throw[^.;]*?\b(?:be|become|fall)\s+"
                  rf"(?:knocked\s+)?{clave}\b")
        if re.search(patron, texto, re.IGNORECASE):
            return ConditionEffect(
                condition=condicion, save_ability=ability, dc=dc,
                duration_rounds=duracion, repeat_save=repeat, escape=escape,
            )
    return None


# --- Interpretación de un hechizo ------------------------------------------ #

def parse_spell(raw: dict, monster_name: str = "",
                spellcasting: Spellcasting | None = None) -> Spell | None:
    """Interpreta el JSON de un hechizo.

    Devuelve ``None`` si el hechizo no se puede modelar (con aviso).
    """
    nombre = str(raw.get("name") or "")
    desc = [str(d) for d in (raw.get("desc") or [])]
    texto = " ".join(desc)
    spell = Spell(
        name=nombre,
        index=str(raw.get("index") or ""),
        level=int(raw.get("level") or 0),
        school=str(raw.get("school") or ""),
        casting_time=str(raw.get("casting_time") or ""),
        range=str(raw.get("range") or ""),
        duration=str(raw.get("duration") or ""),
        concentration=bool(raw.get("concentration")),
        desc=desc,
    )

    # (1) Rituales: no se pueden usar en combate.
    if bool(raw.get("ritual")):
        _warn(monster_name, nombre, "ritual: no se usa en combate")
        return None

    # (2) Tiempo de lanzamiento de 1 minuto o más: no influye en el combate.
    if LONG_CASTING_RE.search(spell.casting_time):
        _warn(monster_name, nombre, "tiempo de lanzamiento de 1 minuto o más")
        return None

    # (3) Tiempo de casteo -> tipo de acción.
    tipo = CASTING_TIME_ACTIONS.get(spell.casting_time.strip().lower())
    if tipo is None:
        _warn(monster_name, nombre,
              f"tiempo de casteo no modelado ({spell.casting_time!r})")
        return None
    spell.action_type = ActionType(tipo)
    spell.slot_level = int(spell.level or 0)

    nivel = int(getattr(spellcasting, "level", 5) or 5)
    modificador = int(getattr(spellcasting, "attack_bonus", 0) or 0)
    # MOD de la curación: modificador de característica si se conoce
    # (la API solo da el bono de ataque completo).
    mod_curacion = int(getattr(spellcasting, "heal_modifier", modificador) or 0)
    # El slot usado: los hechizos con slot escalan con el slot, no con el
    # nivel del lanzador.
    slot = int(spell.level or 0)
    # Nivel de referencia para el nº de elementos: el del lanzador en los
    # cantrips y el del slot en los hechizos con slot.
    referencia = nivel if slot <= 0 else slot
    ataque = str(raw.get("attack_type") or "")
    if not ataque:
        # La API no trae attack_type en todos los hechizos (p. ej.
        # Scorching Ray): si el texto dice "ranged/melee spell attack"
        # se toma de ahí.
        coincidencia = SPELL_ATTACK_RE.search(texto)
        if coincidencia:
            ataque = coincidencia.group(1).lower()
    dc_info = raw.get("dc")
    damage = raw.get("damage") or []
    heal_levels = raw.get("heal_at_slot_level")
    # Tablas de escalado crudas: permiten reescalar daño/curación al hacer
    # upcast (``spell_action(..., slot_level=N)``) sin volver a la API.
    spell.damage_table = _tabla_de_dano(damage)
    if isinstance(heal_levels, dict):
        spell.heal_table = dict(heal_levels)

    # (4) Hechizos de estado (sin daño ni salvación): vocabulario cerrado.
    estado = SPELL_STATES.get(nombre.lower())
    if estado is not None:
        condicion, objetivo, necesita_salvacion = estado
        if not necesita_salvacion:
            spell.kind = "state"
            spell.state = StateEffect(
                condition=Condition(condicion),
                duration_rounds=duracion_en_rondas(spell.duration),
                target=objetivo,
            )
            spell.state_target = objetivo
            return spell

    # (5) Curación.
    if isinstance(heal_levels, dict) and heal_levels:
        if "temporary hit points" in texto.lower():
            # Puntos de vida temporales: el motor no los modela.
            _warn(monster_name, nombre, "puntos de vida temporales: no se modelan")
            return None
        spell.kind = "heal"
        spell.heal = _dado_por_nivel(heal_levels, slot, mod_curacion)
        if not spell.heal:
            _warn(monster_name, nombre, "curación sin dados reconocibles")
            return None
        return spell

    # (6) Ataque de hechizo.
    if ataque:
        dados = _dados_de_dano(damage, nivel, slot)
        if not dados:
            _warn(monster_name, nombre, "ataque sin daño modelable")
            return None
        spell.kind = "attack"
        spell.attack_type = ataque
        spell.damage = dados
        spell.damage_type = _tipo_de_dano(damage)
        spell.damage_options = _opciones_de_dano(damage)
        spell.elements = _numero_elementos(texto, referencia)
        if spell.elements > 1 and not SEPARATE_ELEMENTS_RE.search(texto):
            # El daño de la API es el total de todos los elementos.
            warnings.warn(
                f"Hechizo {nombre!r} de {monster_name!r}: el daño de la API es "
                f"el total de los {spell.elements} elementos; se aplica a un "
                f"solo objetivo. # TODO: repartir el daño entre los elementos.",
                stacklevel=3,
            )
            spell.elements = 1
        return spell

    # (7) Daño con salvación.
    if isinstance(dc_info, dict) and damage:
        dados = _dados_de_dano(damage, nivel, slot)
        if not dados:
            _warn(monster_name, nombre, "daño con salvación sin dados")
            return None
        spell.kind = "save"
        spell.damage = dados
        spell.damage_type = _tipo_de_dano(damage)
        spell.dc_ability = _dc_ability(dc_info)
        success = str(dc_info.get("dc_success") or "none").lower()
        spell.dc_success = "half" if success == "half" else "none"
        spell.area = is_area_action({"desc": texto})
        return spell

    # (8) Condición con salvación (o estado con salvación).
    if isinstance(dc_info, dict):
        dc = int(getattr(spellcasting, "save_dc", 10) or 10)
        if estado is not None:
            condicion, _objetivo, _ = estado
            efecto = ConditionEffect(
                condition=Condition(condicion),
                save_ability=_dc_ability(dc_info),
                dc=dc,
                duration_rounds=duracion_en_rondas(spell.duration),
                repeat_save=False,
                escape=None,
            )
        else:
            efecto = _condicion_con_salvacion(
                texto, nombre, monster_name, _dc_ability(dc_info), dc,
                duracion_en_rondas(spell.duration),
            )
        if efecto is None:
            if _afecta_movimiento(texto):
                _warn(monster_name, nombre, "solo afecta al movimiento")
            else:
                _warn(monster_name, nombre, "utilidad sin efecto en combate")
            return None
        spell.kind = "condition"
        spell.condition = efecto
        spell.dc_ability = _dc_ability(dc_info)
        spell.area = is_area_action({"desc": texto})
        return spell

    # (9) Daño automático (sin ataque ni salvación): p. ej. Proyectil Mágico.
    if damage and HP_THRESHOLD_RE.search(texto):
        _warn(monster_name, nombre, "efecto por puntos de vida: no se modela")
        return None
    if damage and DIRECT_DAMAGE_RE.search(texto):
        dados = _dados_de_dano(damage, nivel, slot)
        if dados:
            spell.kind = "fixed"
            spell.damage = dados
            spell.damage_type = _tipo_de_dano(damage)
            elementos = _elementos_totales(texto)
            if elementos > 1:
                warnings.warn(
                    f"Hechizo {nombre!r} de {monster_name!r}: el daño de la API es "
                    f"el total de los {elementos} elementos; se aplica a un solo "
                    f"objetivo. # TODO: repartir el daño entre los elementos.",
                    stacklevel=3,
                )
            spell.elements = 1
            return spell

    # (10) Sin efecto modelable.
    if HP_THRESHOLD_RE.search(texto):
        _warn(monster_name, nombre,
              "efecto por puntos de vida: no se modela")
        return None
    if _es_ilusion(raw):
        _warn(monster_name, nombre, "ilusión sin estado en el rival")
        return None
    if _crea_objetos(texto):
        _warn(monster_name, nombre, "crea objetos sin daño ni efecto")
        return None
    if _afecta_movimiento(texto):
        _warn(monster_name, nombre, "solo afecta al movimiento")
    else:
        _warn(monster_name, nombre, "utilidad sin efecto en combate")
    return None


def build_spell_actions(monster_json: dict, monster_name: str = "",
                        get_spell=None,
                        max_spell_level: int | None = None) -> list:
    """Acciones de hechizo del monstruo: **todos sus hechizos** (0-9).

    - Los **cantrips** (nivel 0) se lanzan cuantas veces se quiera: no
      gastan slots ni usos por día (``usage = None``).
    - Los hechizos de nivel 1 o superior comparten un **pool de slots por
      nivel** (``ActionUsage`` compartido entre los hechizos de ese nivel);
      el motor lo gasta al lanzar (``usage.spend()``) y ``Combatant.reset()``
      lo restaura al empezar el combate.
    - ``max_spell_level`` permite limitar el nivel cargado (None = todos,
      la ficha manda). Útil para comparar balance con/sin hechizos altos.

    ``get_spell`` es la función que descarga el JSON del hechizo (por
    defecto :func:`dnd_sim.data.api_client.get_spell`).
    """
    from ..rules.spells import spell_action

    from ..rules.usage import ActionUsage, UsageKind

    if get_spell is None:
        from .api_client import get_spell as _get
        get_spell = _get

    spellcasting = parse_spellcasting(monster_json)
    if spellcasting is None:
        return []

    # Un pool de slots por nivel (compartido por los hechizos de ese nivel).
    # Los cantrips (nivel 0) no entran: son ilimitados.
    slots: dict[int, Any] = {}
    for nivel, usos in (spellcasting.slots or {}).items():
        try:
            cantidad = int(usos)
            nivel_int = int(nivel)
        except (TypeError, ValueError):
            continue
        if cantidad > 0 and nivel_int > 0:
            slots[nivel_int] = ActionUsage(kind=UsageKind.PER_DAY,
                                            uses_max=cantidad,
                                            uses_left=cantidad)

    acciones = []
    for entrada in spellcasting.spells:
        if not isinstance(entrada, dict):
            continue
        nivel = int(entrada.get("level") or 0)
        if max_spell_level is not None and nivel > max_spell_level:
            continue
        url = str(entrada.get("url") or "")
        indice = url.rsplit("/", 1)[-1] if url else str(entrada.get("name") or "")
        if not indice:
            continue
        try:
            raw = get_spell(indice)
        except Exception:
            warnings.warn(
                f"Hechizo {entrada.get('name')!r} de {monster_name!r}: no se ha "
                f"podido cargar. # TODO: revisar la conexión con la API.",
                stacklevel=3,
            )
            continue
        spell = parse_spell(raw, monster_name, spellcasting)
        if spell is None:
            continue
        accion = spell_action(spell, spellcasting)
        if accion is not None:
            # Un hechizo con slot usa el pool de su nivel (compartido).
            # (El slot se gasta al lanzar, no aquí.)
            accion.usage = slots.get(nivel)
            acciones.append(accion)
    return acciones


__all__ = [
    "parse_spell",
    "parse_spellcasting",
    "build_spell_actions",
    "SPELL_STATES",
    "LONG_CASTING_RE",
    "ELEMENT_RE",
]

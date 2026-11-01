"""Interpreta el JSON de los hechizos de la API (dnd5eapi.co, PHB 2024).

Formato real (verificado sobre los hechizos del PHB 2024):

.. code-block:: json

    {"name": "Ray of Frost", "index": "ray-of-frost", "level": 0,
     "casting_time": "Action", "range": "60 feet",
     "components": ["V", "S"], "duration": "Instantaneous",
     "concentration": false, "ritual": false,
     "school": {"index": "evocation", "name": "Evocation", "url": "..."},
     "damage": {"damage_type": {"index": "cold", "url": "..."},
                "damage_at_slot_level": {"0": "1d8"}},
     "description": "A frigid beam ... Make a ranged spell attack ...",
     "higher_level": null}

Diferencias con la SRD 2014 que condicionan el parser:

- ``description``/``higher_level`` son **cadenas** (no listas), ``school`` es
  un objeto y ``damage`` es **un objeto** (no una lista) con solo
  ``damage_at_slot_level`` (los cantrips usan la clave ``"0"``).
- **No** hay campos ``dc``, ``attack_type`` ni ``heal_at_slot_level``: la
  característica de la salvación («Dexterity saving throw»), el medio daño
  («half as much damage»), el daño fijo («base damage is 12d6»), la
  curación («regains ... Hit Points equal to 2d8») y las condiciones
  («have the Blinded condition») salen del **texto**.
- El escalado (upcast) también vive en el texto: «increases by 1d6 for
  each spell slot level above 1» (daño o curación) y en los cantrips
  «levels 5 (2d6), 11 (3d6), and 17 (4d6)».
- El lanzador va en ``actions`` (bloque «Spellcasting») con ``dc`` y
  ``spells[].usage`` («at will» / «per day N»): sin ``modifier``, ``level``
  ni ``slots``; el bono de ataque se deriva de la CD (CD − 8) y el nivel de
  lanzador se estima como 2 × nivel de hechizo máx − 1.

# TODO: el parser es frágil por naturaleza (texto libre): si un hechizo
se clasifica mal, hay que ajustar el regex correspondiente aquí.
"""
from __future__ import annotations

import re
import warnings
from typing import Any

from ..model.actions import ActionType
from ..model.attack import ExtraDamage
from ..rules.conditions import Condition, ConditionEffect
from ..rules.damage import DamageType, parse_damage_type
from ..rules.saves import normalize_ability
from ..rules.spells import (Spell, Spellcasting, StateEffect, dado_por_nivel,
                            duracion_en_rondas, spell_action)
from ..rules.usage import ActionUsage, UsageKind
from .area_classifier import is_area_action
from .condition_parser import CONDITION_KEYWORDS
from .escape_parser import parse_escape


# ---------------------------------------------------------------------------
# Vocabulario del PHB 2024 (expresiones literales de los textos de la API)
# ---------------------------------------------------------------------------

# «1 minute», «1 hour», «1 day» en el tiempo de lanzamiento: no se modela.
LONG_CASTING_RE = re.compile(r"\b(\d+)\s*(minute|hour|day)s?\b", re.IGNORECASE)
# «Action», «Bonus Action», «Reaction, which you take...».
CASTING_TIME_RE = re.compile(
    r"^\s*(?:\d+\s*)?(bonus action|reaction|action)\b", re.IGNORECASE)
_ACTION_TYPES = {"bonus action": ActionType.BONUS_ACTION,
                 "reaction": ActionType.REACTION,
                 "action": ActionType.ACTION}
# «Make a ranged spell attack» / «Make a melee spell attack».
SPELL_ATTACK_RE = re.compile(r"\b(ranged|melee)\s+spell attack\b",
                             re.IGNORECASE)
# «a Constitution saving throw» (primera mención del texto).
SAVE_RE = re.compile(
    r"\b(Strength|Dexterity|Constitution|Intelligence|Wisdom|Charisma)"
    r"\s+saving throw", re.IGNORECASE)
# «half as much damage» / «takes half as much damage only».
HALF_RE = re.compile(r"half as much damage", re.IGNORECASE)
# «The damage increases by 1d6 for each spell slot level above 1.»
UPCAST_DAMAGE_RE = re.compile(
    r"damage increases by (\d+d\d+) for each spell slot level above (\d+)",
    re.IGNORECASE)
# «The healing increases by 2d8 for each spell slot level above 1.»
UPCAST_HEAL_RE = re.compile(
    r"healing increases by (\d+d\d+) for each spell slot level above (\d+)",
    re.IGNORECASE)
# Cantrips: «levels 5 (2d6), 11 (3d6), and 17 (4d6)».
CANTRIP_UPGRADE_RE = re.compile(
    r"levels 5 \((\w+)\), 11 \((\w+)\), and 17 \((\w+)\)", re.IGNORECASE)
# «You create three glowing darts» / «You hurl three fiery rays».
ELEMENT_RE = re.compile(
    r"\b(two|three|four|five|six)\s+(?:\w+\s+)?(?:beams|rays|darts|bolts)\b",
    re.IGNORECASE)
# «The spell creates two beams at level 5, three beams at level 11, ...»
ELEMENT_BY_LEVEL_RE = re.compile(
    r"\b(two|three|four|five)\s+(?:\w+\s+)?(?:beams|rays|darts|bolts)"
    r"\s+at level (\d+)", re.IGNORECASE)
# «Make a separate attack roll for each beam» / «attack for each ray».
SEPARATE_ELEMENTS_RE = re.compile(
    r"separate attack roll for each|attack for each|"
    r"roll (?:a|an|the) .{0,40} for each", re.IGNORECASE)
# «have the Charmed condition» / «has the Prone and Incapacitated
# conditions» / «or fall Prone» / «be knocked prone».
CONDITION_2024_RE = re.compile(
    r"\b(?:have|has)\s+(?:the\s+)?([a-z]+(?:\s+and\s+[a-z]+)*)\s+conditions?\b"
    r"|\bor fall\s+(\w+)\b"
    r"|\bbe knocked\s+(\w+)\b", re.IGNORECASE)
# Frase con salvación: «saving throw», «On a failed save», «repeats the
# save», «fails the second save»...
_SALVACION_EN_FRASE_RE = re.compile(
    r"saving throw|failed save|fails?\b[^.]{0,40}\bsave\b|"
    r"repeats? the save|that save", re.IGNORECASE)
# «the target repeats the save» / «it makes another Wisdom saving throw».
REPEAT_SAVE_RE = re.compile(
    r"(?:repeat(?:s)?|makes? another)\s+(?:\w+\s+)?(?:saving throw|save)",
    re.IGNORECASE)
# «If the target fails the second save, the target has the Unconscious
# condition for the duration» (Sleep 2024): escalado de la repetición.
ESCALATE_RE = re.compile(
    r"fails the (?:second|repeat)[^.]*?has the (\w+) condition",
    re.IGNORECASE)
# «... until the end of your next turn»: la condición dura 1 ronda.
UNTIL_NEXT_TURN_RE = re.compile(
    r"until the end of (?:your|its|his|her|their) next turn", re.IGNORECASE)
# «regains a number of Hit Points equal to 2d8 plus your spellcasting
# ability modifier».
HEAL_RE = re.compile(
    r"regains (?:a number of )?Hit Points equal to (\d+d\d+)"
    r"(\s*plus your spellcasting ability modifier)?", re.IGNORECASE)
# «The spell's base damage is 12d6» (Delayed Blast Fireball).
BASE_DAMAGE_RE = re.compile(r"base damage is (\d+d\d+)", re.IGNORECASE)
# «A creature takes Fire damage equal to the total accumulated damage»:
# tipo de daño del hechizo sin campo estructurado (Delayed Blast Fireball).
DAMAGE_TYPE_TEXT_RE = re.compile(r"takes (\w+) damage", re.IGNORECASE)
# «taking 7d8 + 30 Necrotic damage on a failed save» (Finger of Death):
# daño con salvación sin campo estructurado en la API.
SAVE_DAMAGE_TEXT_RE = re.compile(
    r"taking (\d+d\d+)(?:\s*\+\s*(\d+))?\s+(\w+) damage", re.IGNORECASE)
# «A dart deals 1d4 + 1 Force damage to its target» (Magic Missile).
PER_ELEMENT_DAMAGE_RE = re.compile(
    r"(\d+)d(\d+)\s*\+\s*(\d+)\s+(\w+)\s+damage", re.IGNORECASE)
# «The spell creates one more dart for each spell slot level above 1.»
ONE_MORE_ELEMENT_RE = re.compile(
    r"creates one more \w+ for each spell slot level above (\d+)",
    re.IGNORECASE)
# «damage to its target» / «takes 2d8 Fire damage».
DIRECT_DAMAGE_RE = re.compile(r"damage to (?:its|the) target|"
                              r"takes? [\w\d+ ]*damage", re.IGNORECASE)
# «You gain 2d4 + 4 Temporary Hit Points»: no se modelan.
TEMP_HP_RE = re.compile(r"temporary hit points", re.IGNORECASE)

# Expresiones de dados «NdX», «NdX+3» o «NdX+MOD» (para sumar upcast).
_DADOS_RE = re.compile(r"^(\d+)d(\d+)(?:([+-])(\d+|MOD))?$", re.IGNORECASE)

_NUMEROS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}

# Hechizos de estado del SRD (vocabulario cerrado):
# nombre -> (condición, destino, necesita salvación).
# - Guidance: +1d4 a una prueba durante 1 minuto (PHB 2024: no se consume
#   al usarla).
# - Divine Favor / Hunter's Mark: el **portador** inflige daño extra con
#   sus ataques (véase CONDITION_ATTACK_DAMAGE en rules.conditions).
# - Charm Person / Faerie Fire necesitan salvación, que sale del texto.
SPELL_STATES: dict[str, tuple[str, str, bool]] = {
    "guidance": ("guided", "ally", False),
    "charm person": ("charmed", "enemy", True),
    "faerie fire": ("marked", "enemy", True),
    "enlarge/reduce": ("enlarged", "self", False),
    "divine favor": ("divine_favor", "self", False),
    "hunter's mark": ("hunters_mark", "self", False),
}

# Marcas de texto para lo que NO se modela (sin daño ni condición).
CREATE_MARKERS = ("you create", "you conjure", "appear in your hand",
                  "appear in your hands")
MOVEMENT_MARKERS = ("speed", "teleport", "dash", "levitate", "push", "pull",
                    "shove", "knock", "swim", "jump", "walk", "fly",
                    "flying", "movement", "descent")

# Gravedad de las condiciones 2024: cuando el texto enumera varias («the
# Prone and Incapacitated conditions»), se aplica la más grave.
GRAVEDAD: tuple[str, ...] = (
    "stunned", "paralyzed", "unconscious", "petrified", "incapacitated",
    "restrained", "blinded", "prone", "poisoned", "frightened", "charmed")


def _avisar(monster_name: str, nombre: str, motivo: str) -> None:
    warnings.warn(f"[hechizo] {nombre} ({monster_name or 'SRD'}): {motivo}",
                  stacklevel=2)


# ---------------------------------------------------------------------------
# Auxiliares de texto
# ---------------------------------------------------------------------------

def _frases(texto: str) -> list[str]:
    """Divide el texto en frases (exige misma frase para salvación+condición)."""
    return [f.strip() for f in re.split(r"(?<=[.!?])\s+|\n+", texto) if f.strip()]


def _condiciones_de_frase(frase: str) -> list[str]:
    """Condiciones del vocabulario 2024 presentes en la frase."""
    match = CONDITION_2024_RE.search(frase)
    if not match:
        return []
    bruto = match.group(1) or match.group(2) or match.group(3) or ""
    candidatos = [p.strip().lower()
                  for p in re.split(r"\s+and\s+", bruto) if p.strip()]
    return [c for c in candidatos if c in CONDITION_KEYWORDS]


def _condicion_con_salvacion(texto: str) -> Condition | None:
    """Condición ligada textualmente a una salvación (PHB 2024).

    Vocabulario: «or have the Charmed condition», «has the Prone and
    Incapacitated conditions» (se elige la más grave) u «or fall Prone».
    La frase debe contener también palabras de salvación para no confundir
    efectos secundarios de otras frases.
    """
    for frase in _frases(texto):
        if not _SALVACION_EN_FRASE_RE.search(frase):
            continue
        candidatos = _condiciones_de_frase(frase)
        if not candidatos:
            continue
        candidatos.sort(key=lambda c: (GRAVEDAD.index(c) if c in GRAVEDAD
                                       else len(GRAVEDAD)))
        return Condition(CONDITION_KEYWORDS[candidatos[0]])
    return None


def _slot_table(entry: dict) -> dict[str, str]:
    """Tabla {nivel: dados} del objeto ``damage`` (2024: solo slots)."""
    tabla = (entry.get("damage_at_slot_level")
             or entry.get("damage_at_character_level") or {})
    if not isinstance(tabla, dict):
        return {}
    out: dict[str, str] = {}
    for clave, valor in tabla.items():
        try:
            out[str(int(clave))] = str(valor)
        except (TypeError, ValueError):
            continue
    return out


def _tipo_de_dano(entries: list) -> str:
    for entry in entries:
        tipo = entry.get("damage_type") or {}
        if isinstance(tipo, dict):
            return str(tipo.get("index") or "")
        return str(tipo or "")
    return ""


def _tabla_cantrip(base: str, texto: str,
                   con_base: bool = True) -> dict[str, str]:
    """Tabla de escalado de cantrip por **nivel de personaje**."""
    tabla = {"1": base} if con_base else {}
    match = CANTRIP_UPGRADE_RE.search(texto)
    if match:
        tabla["5"] = str(match.group(1))
        tabla["11"] = str(match.group(2))
        tabla["17"] = str(match.group(3))
    return tabla


def _dados_hasta(tabla: dict[str, str], nivel: int) -> str:
    """Dados de la clave más alta <= nivel ('' si no hay ninguna)."""
    try:
        claves = sorted(int(k) for k in tabla)
    except (TypeError, ValueError):
        return ""
    elegido = None
    for clave in claves:
        if clave <= nivel:
            elegido = clave
    return str(tabla[str(elegido)]) if elegido is not None else ""


def _sumar_dados(base: str, incremento: str) -> str | None:
    """Suma dos expresiones de dados de igual cara (upcast).

    Devuelve None si no se puede (cara distinta o formato raro): quien
    llama no extiende la tabla y avisa.
    """
    m1 = _DADOS_RE.match(str(base).strip())
    m2 = _DADOS_RE.match(str(incremento).strip())
    if not m1 or not m2:
        return None
    n1, c1, s1, f1 = m1.groups()
    n2, c2, s2, f2 = m2.groups()
    if c1 != c2:
        return None
    if f1 is None and f2 is None:
        flat = ""
    elif f1 is None:
        flat = f"{s2}{f2}"
    elif f2 is None:
        flat = f"{s1}{f1}"
    elif s1 == s2 and f1 == f2:
        flat = f"{s1}{f1}"  # MOD+MOD (o el mismo plano)
    elif f1.isdigit() and f2.isdigit():
        total = int(f1) + (int(f2) if s2 == "+" else -int(f2))
        flat = f"{s1}{total}" if total else ""
    else:
        return None
    return f"{int(n1) + int(n2)}d{c1}{flat}"


def _extender_tabla(tabla: dict[str, str], incremento: str, desde: int,
                    monster_name: str, nombre: str) -> dict[str, str]:
    """Extiende la tabla de daño/curación con el upcast del texto."""
    out = {str(k): str(v) for k, v in tabla.items()}
    if str(desde) not in out:
        return out
    for nivel in range(desde + 1, 10):
        previo = out.get(str(nivel - 1))
        if previo is None:
            break
        nuevo = _sumar_dados(previo, incremento)
        if nuevo is None:
            _avisar(monster_name, nombre,
                    f"upcast con dados distintos ({previo} + {incremento}): "
                    "tabla sin extender")
            break
        out[str(nivel)] = nuevo
    return out


def _elementos_totales(texto: str) -> int:
    match = ELEMENT_RE.search(texto)
    if not match:
        return 1
    return _NUMEROS.get(match.group(1).lower(), 1)


def _elementos_por_nivel(texto: str, nivel: int) -> int:
    """Elementos por nivel de lanzador («two beams at level 5, ...»)."""
    tabla: dict[int, int] = {}
    for match in ELEMENT_BY_LEVEL_RE.finditer(texto):
        tabla[int(match.group(2))] = _NUMEROS.get(match.group(1).lower(), 1)
    if not tabla:
        return _elementos_totales(texto)
    elegido = 1
    for clave in sorted(tabla):
        if clave <= nivel:
            elegido = tabla[clave]
    return elegido


# ---------------------------------------------------------------------------
# Parser de un hechizo
# ---------------------------------------------------------------------------

def parse_spell(raw: dict, monster_name: str = "",
                spellcasting: Spellcasting | None = None) -> Spell | None:
    """Interpreta la ficha de un hechizo del PHB 2024.

    Devuelve un :class:`Spell` con el efecto ya interpretado, o ``None`` si
    no se modela (ritual, 1 minuto de casteo, utilidad...). En ese caso se
    emite un aviso con el motivo.
    """
    nombre = str(raw.get("name") or "")
    desc_str = str(raw.get("description") or "")
    higher = str(raw.get("higher_level") or "")
    texto = desc_str
    texto_completo = (desc_str + " " + higher).strip()
    desc = [p.strip() for p in desc_str.split("\n") if p.strip()]
    school = raw.get("school") or ""
    if isinstance(school, dict):
        school = str(school.get("index") or "")
    nivel = int(raw.get("level") or 0)
    spell = Spell(
        name=nombre,
        index=str(raw.get("index") or ""),
        level=nivel,
        school=str(school),
        casting_time=str(raw.get("casting_time") or ""),
        range=str(raw.get("range") or ""),
        duration=str(raw.get("duration") or ""),
        concentration=bool(raw.get("concentration")),
        desc=desc,
        slot_level=nivel,
    )
    sc = spellcasting
    nivel_lanzador = int(getattr(sc, "level", 0) or 0) or max(1, nivel)

    # (1) Ritual: no se modela el componente ni el tiempo.
    if raw.get("ritual"):
        spell.ignored = "ritual"
        _avisar(monster_name, nombre, spell.ignored)
        return None
    # (2) Tiempo de lanzamiento largo («1 minute» o más).
    if LONG_CASTING_RE.search(spell.casting_time):
        spell.ignored = "1 minuto"
        _avisar(monster_name, nombre, spell.ignored)
        return None
    # (3) Tiempo de lanzamiento -> tipo de acción («Action», «Bonus
    #     Action», «Reaction, which you take...»).
    match = CASTING_TIME_RE.match(spell.casting_time)
    if match:
        spell.action_type = _ACTION_TYPES[match.group(1).lower()]

    # (4) Hechizos de estado sin salvación (vocabulario cerrado).
    estado = SPELL_STATES.get(nombre.lower())
    if estado is not None and not estado[2]:
        spell.kind = "state"
        spell.state_target = estado[1]
        spell.state = StateEffect(
            condition=Condition(estado[0]),
            duration_rounds=duracion_en_rondas(spell.duration),
            target=estado[1],
        )
        return spell

    # (5) True Strike: ataque real con el arma del lanzador (genérica 1d8
    #     Radiante) + daño extra Radiante según el nivel del lanzador.
    if nombre.lower() == "true strike":
        spell.kind = "attack"
        spell.attack_type = "melee"
        spell.damage = "1d8"
        spell.damage_type = "radiant"
        spell.damage_bonus_from_ability = True
        extra = _dados_hasta(
            _tabla_cantrip("1d6", texto_completo, con_base=False),
            nivel_lanzador)
        if extra:
            spell.extra_damage = [ExtraDamage(extra, DamageType.RADIANT)]
        return spell

    # (6) Puntos de vida temporales: no se modelan.
    if TEMP_HP_RE.search(texto_completo):
        spell.ignored = "puntos de vida temporales: no se modelan."
        _avisar(monster_name, nombre, spell.ignored)
        return None

    # --- Daño estructurado (objeto `damage` con damage_at_slot_level) ---
    damage = raw.get("damage")
    entries = [damage] if isinstance(damage, dict) else list(damage or [])
    entries = [e for e in entries if isinstance(e, dict)]
    if entries:
        tipo = _tipo_de_dano(entries)
        if tipo:
            spell.damage_type = parse_damage_type(tipo).value
        tabla_slots = _slot_table(entries[0])
        if nivel == 0:
            # Cantrip: base en la clave «0» + escalado del texto
            # (levels 5 (2d8), 11 (3d8), 17 (4d8)) con el nivel del
            # lanzador.
            base = tabla_slots.get("0") or tabla_slots.get("1") or ""
            if base:
                spell.damage_table = _tabla_cantrip(base, texto_completo)
                spell.damage = dado_por_nivel(spell.damage_table,
                                              nivel_lanzador)
        else:
            spell.damage_table = dict(tabla_slots)
            match = UPCAST_DAMAGE_RE.search(texto_completo)
            if match:
                spell.damage_table = _extender_tabla(
                    spell.damage_table, match.group(1), int(match.group(2)),
                    monster_name, nombre)
            spell.damage = dado_por_nivel(spell.damage_table, spell.slot_level)
    else:
        # Sin campo estructurado: daño por texto (Delayed Blast Fireball:
        # «The spell's base damage is 12d6»).
        match = BASE_DAMAGE_RE.search(texto_completo)
        if match:
            spell.damage_table = {str(spell.slot_level): match.group(1)}
            match_tipo = DAMAGE_TYPE_TEXT_RE.search(texto_completo)
            if match_tipo:
                spell.damage_type = parse_damage_type(
                    match_tipo.group(1)).value
            match2 = UPCAST_DAMAGE_RE.search(texto_completo)
            if match2:
                spell.damage_table = _extender_tabla(
                    spell.damage_table, match2.group(1), int(match2.group(2)),
                    monster_name, nombre)
            spell.damage = dado_por_nivel(spell.damage_table, spell.slot_level)

    # --- Salvación («a Constitution saving throw») y medio daño ---
    match = SAVE_RE.search(texto_completo)
    save_ability = normalize_ability(match.group(1)) if match else ""
    half = bool(HALF_RE.search(texto_completo))

    # (7) Curación por texto («regains ... Hit Points equal to 2d8 plus
    #     your spellcasting ability modifier»). No hay salvación ni ataque.
    match = HEAL_RE.search(texto_completo)
    if match and not save_ability and not SPELL_ATTACK_RE.search(texto_completo):
        dados = match.group(1)
        base = f"{dados}+MOD" if match.group(2) else dados
        spell.kind = "heal"
        spell.heal_table = {str(spell.slot_level): base}
        match2 = UPCAST_HEAL_RE.search(texto_completo)
        if match2:
            spell.heal_table = _extender_tabla(
                spell.heal_table, match2.group(1), int(match2.group(2)),
                monster_name, nombre)
        spell.heal = dado_por_nivel(spell.heal_table, spell.slot_level,
                                    int(getattr(sc, "heal_modifier", 0) or 0))
        return spell

    # (8) Ataque de hechizo («Make a ranged spell attack»).
    match = SPELL_ATTACK_RE.search(texto_completo)
    if match:
        spell.kind = "attack"
        spell.attack_type = match.group(1).lower()
        if SEPARATE_ELEMENTS_RE.search(texto_completo):
            if ELEMENT_BY_LEVEL_RE.search(texto_completo):
                spell.elements = _elementos_por_nivel(texto_completo,
                                                      nivel_lanzador)
            else:
                spell.elements = _elementos_totales(texto_completo)
        return spell

    # (9) Daño con salvación («must succeed on a Dexterity saving throw...
    #     taking 3d6 Fire damage» / «base damage is 12d6»). Si la API no
    #     trae el campo, el daño sale del texto (Finger of Death).
    if save_ability and not spell.damage:
        match = SAVE_DAMAGE_TEXT_RE.search(texto_completo)
        if match:
            base = (f"{match.group(1)}+{match.group(2)}" if match.group(2)
                    else match.group(1))
            spell.damage_table = {str(spell.slot_level): base}
            match2 = UPCAST_DAMAGE_RE.search(texto_completo)
            if match2:
                spell.damage_table = _extender_tabla(
                    spell.damage_table, match2.group(1), int(match2.group(2)),
                    monster_name, nombre)
            spell.damage = dado_por_nivel(spell.damage_table, spell.slot_level)
            spell.damage_type = parse_damage_type(match.group(3)).value
    if save_ability and spell.damage:
        spell.kind = "save"
        spell.dc_ability = save_ability
        spell.dc_success = "half" if half else "none"
        spell.area = is_area_action({"desc": texto_completo})
        return spell

    # (10) Condición con salvación («or have the Blinded condition»).
    if save_ability:
        condicion = None
        if estado is not None:
            # Hechizo de estado con salvación (Charm Person, Luz de hadas).
            condicion = Condition(estado[0])
        if condicion is None:
            condicion = _condicion_con_salvacion(texto_completo)
        if condicion is not None:
            duracion = (1 if UNTIL_NEXT_TURN_RE.search(texto_completo)
                        else duracion_en_rondas(spell.duration))
            repite = bool(REPEAT_SAVE_RE.search(texto_completo))
            escala_a = None
            escala_rondas = None
            match = ESCALATE_RE.search(texto_completo)
            if match:
                try:
                    escala_a = Condition(match.group(1).lower())
                    escala_rondas = duracion_en_rondas(spell.duration)
                except ValueError:
                    escala_a = None
            spell.kind = "condition"
            spell.dc_success = "none"
            spell.area = is_area_action({"desc": texto_completo})
            spell.condition = ConditionEffect(
                condition=condicion,
                save_ability=save_ability,
                dc=int(getattr(sc, "save_dc", 10) or 10),
                duration_rounds=duracion,
                repeat_save=repite,
                escape=parse_escape(texto_completo),
                escalate_to=escala_a,
                escalate_rounds=escala_rondas,
                magical=True,
            )
            return spell

    # (11) Daño fijo sin salvación (Magic Missile): se modela como el
    #      **total** de los dardos (p. ej. 3d4+3, 5d4+5 en slot 3).
    match = PER_ELEMENT_DAMAGE_RE.search(texto_completo)
    match2 = ONE_MORE_ELEMENT_RE.search(texto_completo)
    if (not spell.kind and not save_ability and match and match2
            and DIRECT_DAMAGE_RE.search(texto_completo)):
        caras = int(match.group(2))
        plano = int(match.group(3))
        base = _elementos_totales(texto_completo)
        desde = int(match2.group(1))
        tabla: dict[str, str] = {}
        for slot in range(1, 10):
            dardos = base + max(0, slot - desde)
            tabla[str(slot)] = f"{dardos}d{caras}+{dardos * plano}"
        spell.kind = "fixed"
        spell.damage_type = parse_damage_type(match.group(4)).value
        spell.damage_table = tabla
        spell.damage = dado_por_nivel(tabla, spell.slot_level)
        spell.area = False
        _avisar(monster_name, nombre,
                "daño fijo modelado como el total de los elementos "
                "(se aplica a un solo objetivo)")
        return spell

    # (12) Ignorado: el motivo más específico que coincida.
    texto_bajo = texto_completo.lower()
    if "illusion" in spell.school.lower():
        motivo = "ilusión sin estado en el rival"
    elif any(m in texto_bajo for m in CREATE_MARKERS):
        motivo = "crea objetos sin daño ni efecto"
    elif any(m in texto_bajo for m in MOVEMENT_MARKERS):
        motivo = "solo afecta al movimiento"
    else:
        motivo = "utilidad sin efecto en combate"
    spell.ignored = motivo
    _avisar(monster_name, nombre, motivo)
    return None


# ---------------------------------------------------------------------------
# Lanzador y carga de acciones
# ---------------------------------------------------------------------------

def parse_spellcasting(monster_json: dict) -> Spellcasting | None:
    """Datos del lanzador del monstruo (bloque «Spellcasting» del PHB 2024).

    El bloque va en ``actions`` (no en ``special_abilities``) y trae
    ``ability``, ``dc`` y ``spells`` (cada entrada con ``level`` y
    ``usage``). No hay ``modifier``, ``level`` ni ``slots``:

    - bono de ataque = CD − 8 (en 5e el bono de ataque de un hechizo es 8
      menos su CD);
    - MOD de característica = bono de ataque − competencia (si la ficha la
      trae);
    - nivel de lanzador estimado = 2 × nivel de hechizo máx − 1 (clamp
      1..20), para escalar los cantrips.
    """
    if not isinstance(monster_json, dict):
        return None
    for ability in monster_json.get("actions") or []:
        if not isinstance(ability, dict):
            continue
        if str(ability.get("name") or "").strip().lower() != "spellcasting":
            continue
        data = ability.get("spellcasting") or {}
        abilidad = data.get("ability") or {}
        if isinstance(abilidad, dict):
            index = abilidad.get("index")
        else:
            index = abilidad
        dc = int(data.get("dc") or 10)
        attack_bonus = dc - 8
        ability_mod = None
        proficiency = monster_json.get("proficiency_bonus")
        if proficiency is not None:
            try:
                ability_mod = attack_bonus - int(proficiency)
            except (TypeError, ValueError):
                ability_mod = None
        spells = [s for s in (data.get("spells") or []) if isinstance(s, dict)]
        max_level = max((int(s.get("level") or 0) for s in spells), default=0)
        level = max(1, min(20, 2 * max_level - 1)) if max_level > 0 else 1
        return Spellcasting(
            ability=str(index or "int"),
            save_dc=dc,
            attack_bonus=attack_bonus,
            level=level,
            slots={},
            spells=spells,
            ability_mod=ability_mod,
        )
    return None


def _uso_de_entrada(entrada: dict, monster_name: str,
                    spell: Spell) -> ActionUsage | None:
    """Uso por hechizo del PHB 2024 (sin pools compartidos por nivel).

    - Cantrips (nivel 0): ``None`` = usos infinitos.
    - «at will»: uso ilimitado (siempre disponible).
    - «per day N»: N usos **propios** de ese hechizo.
    """
    if spell.is_cantrip:
        return None
    uso = entrada.get("usage") or {}
    tipo = str(uso.get("type") or "").strip().lower()
    if tipo == "at will":
        return ActionUsage(UsageKind.AT_WILL)
    if tipo == "per day":
        try:
            veces = int(uso.get("times") or 0)
        except (TypeError, ValueError):
            veces = 0
        if veces > 0:
            return ActionUsage(UsageKind.PER_DAY, veces)
        _avisar(monster_name, spell.name,
                "uso «per day» sin veces: se ignora")
    return None


def build_spell_actions(monster_json: dict, monster_name: str = "",
                        get_spell: Any = None,
                        max_spell_level: int | None = None) -> list:
    """Carga los hechizos del bloque «Spellcasting» del PHB 2024.

    Cada entrada de ``spells`` trae su ``level`` (el **slot** con el que la
    lanza el monstruo, p. ej. Fireball a nivel 5) y su ``usage`` («at
    will» = ilimitado; «per day N» = N usos propios del hechizo).
    ``max_spell_level`` filtra por el nivel de la entrada (los cantrips
    siempre pasan).
    """
    if not isinstance(monster_json, dict):
        return []
    spellcasting = parse_spellcasting(monster_json)
    if spellcasting is None:
        return []
    if get_spell is None:
        from .api_client import get_spell as _get
        get_spell = _get
    acciones: list = []
    for entrada in spellcasting.spells:
        nivel = int(entrada.get("level") or 0)
        if max_spell_level is not None and nivel > max_spell_level:
            continue
        url = str(entrada.get("url") or "")
        indice = (url.rstrip("/").split("/")[-1] if url
                  else str(entrada.get("name") or "").lower().replace(" ", "-"))
        try:
            raw = get_spell(indice)
            spell = parse_spell(raw, monster_name, spellcasting)
        except Exception as exc:  # red, 404, JSON raro...
            _avisar(monster_name, str(entrada.get("name") or indice),
                    f"no se ha podido cargar ({exc})")
            continue
        if spell is None:
            continue
        # El slot de la entrada es el nivel con el que el monstruo lanza
        # el hechizo (upcast): Fireball a nivel 5 tira sus dados de 5.
        accion = spell_action(spell, spellcasting, slot_level=nivel or None)
        if accion is None:
            continue
        accion.usage = _uso_de_entrada(entrada, monster_name, spell)
        acciones.append(accion)
    return acciones


__all__ = [
    "parse_spell", "parse_spellcasting", "build_spell_actions",
    "SPELL_STATES", "LONG_CASTING_RE", "ELEMENT_RE",
]

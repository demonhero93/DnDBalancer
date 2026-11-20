"""Parsea las condiciones de la API de dnd5eapi.co (vocabulario cerrado).

Los datos reales de la SRD 2014 (verificado sobre los 334 monstruos):

- La **condición** y la **CD** de un efecto de área aparecen en el texto de
  la acción, no en el campo ``dc``::

    "If the target is a creature, it must succeed on a DC 11 Strength saving
     throw or be knocked prone."                       (wolf)

    "it must succeed on a DC 10 Constitution saving throw or be paralyzed for
     1 minute. The target can repeat the saving throw at the end of each of
     its turns, ending the effect on itself on a success."   (ghoul)

- Las **acciones con campo ``dc``** (aliento de dragón, "Frightful Presence",
  "Stunning Screech" del vrock...) sí traen la CD estructurada, y la condición
  en el texto.

Duraciones reales encontradas: "for 1 minute" (51), "for 1 hour" (8),
"for 10 minute(s)", "until the end of <algo>'s next turn" y "knocked prone".

# TODO: el parser es frágil por naturaleza (texto libre). Si algún monstruo
se clasifica mal, hay que añadir una excepción aquí.
"""
from __future__ import annotations

import re
import warnings

from ..rules.conditions import Condition, ConditionEffect, EXCLUDED_CONDITIONS
from ..rules.roll_modifiers import AttackRange
from ..rules.saves import normalize_ability
from .escape_parser import parse_escape


# Condiciones del Enum y la palabra que las delata en el texto.
CONDITION_KEYWORDS: dict[str, Condition] = {
    "blinded": Condition.BLINDED,
    "charmed": Condition.CHARMED,
    "frightened": Condition.FRIGHTENED,
    "incapacitated": Condition.INCAPACITATED,
    "paralyzed": Condition.PARALYZED,
    "petrified": Condition.PETRIFIED,
    "poisoned": Condition.POISONED,
    "prone": Condition.PRONE,
    "grappled": Condition.GRAPPLED,
    "restrained": Condition.RESTRAINED,
    "stunned": Condition.STUNNED,
    "unconscious": Condition.UNCONSCIOUS,
}

# "saving throw or be <cond>" / "saving throw or become <cond>".
SAVE_OR_CONDITION_RE = re.compile(
    r"saving throw or (?:be|become)\s+((?:knocked\s+)?[a-z]+)(?P<rest>[^.;]*)",
    re.IGNORECASE,
)
# Patrones extra (opcionales, solo para las acciones legendarias):
# - "saving throw against this magic or become frightened" (lich).
SAVE_AGAINST_OR_CONDITION_RE = re.compile(
    r"saving throw against [^.;]*?\bor (?:be|become)\s+((?:knocked\s+)?[a-z]+)(?P<rest>[^.;]*)",
    re.IGNORECASE,
)
# - "saving throw or take 15 (2d6 + 8) bludgeoning damage and be knocked prone"
#   (ala del dragón): la condición va **después** del daño.
SAVE_OR_DAMAGE_AND_CONDITION_RE = re.compile(
    r"saving throw or [^.;]*?\band (?:be|become)\s+((?:knocked\s+)?[a-z]+)(?P<rest>[^.;]*)",
    re.IGNORECASE,
)
# "DC 11 Strength saving throw".
DC_SAVE_RE = re.compile(r"DC\s*(\d+)\s+(\w+)\s+saving throw", re.IGNORECASE)
# "Strength Saving Throw: DC 11" (orden 2024: habilidad primero).
DC_SAVE_2024_RE = re.compile(r"(\w+) Saving Throw: DC (\d+)", re.IGNORECASE)
# "Failure: The target has the Paralyzed condition until the end of its
# next turn." (2024: la condición va tras «Failure:», no tras «or be»).
FAILURE_CONDITION_RE = re.compile(
    r"Failure:[^.]*?has the ([a-z]+) condition(?P<rest>[^.]*)",
    re.IGNORECASE,
)
# "it has the Prone condition" (2024: se aplica al impactar, sin salvación).
AUTO_CONDITION_RE = re.compile(r"\bit has the ([a-z]+) condition\b", re.IGNORECASE)
# "until the end of the vrock's next turn".
DURATION_NEXT_TURN_RE = re.compile(r"until the end of[^.;]*?next turn", re.IGNORECASE)
# "for 1 minute" / "for 10 minutes".
DURATION_MINUTES_RE = re.compile(r"for\s+(\d+)\s+minutes?\b", re.IGNORECASE)
# "for 1 hour" / "for 24 hours".
DURATION_HOURS_RE = re.compile(r"for\s+(\d+)\s+hours?\b", re.IGNORECASE)
# "until the web is destroyed" (giant-spider 2024).
# shortcut: el motor no modela HP de objetos destruibles, así que la
# condición dura hasta el fin del combate; upgrade con objetos destruibles.
DURATION_UNTIL_DESTROYED_RE = re.compile(r"until [^.;]*?is destroyed", re.IGNORECASE)
# Repetición de la salvación ("can repeat the saving throw ...").
REPEAT_SAVE_RE = re.compile(r"repeat the saving throw", re.IGNORECASE)
# Escape con prueba de característica ("can make a DC 12 Strength check").
CHARACTERISTIC_CHECK_RE = re.compile(r"DC\s*\d+\s+\w+\s+check\b", re.IGNORECASE)
# Tipos de ataque.
MELEE_RE = re.compile(r"\bmelee\b", re.IGNORECASE)
RANGED_RE = re.compile(r"\branged\b", re.IGNORECASE)

# "knocked prone": el creature se levanta en su siguiente turno.
KNOCKED_PRONE_ROUNDS = 1


def _condition_from_phrase(phrase: str) -> Condition | None:
    """Condición a partir de la frase tras la salvación ("knocked prone")."""
    words = phrase.lower().split()
    if not words:
        return None
    if words[0] == "knocked":
        words = words[1:]
    if not words:
        return None
    return CONDITION_KEYWORDS.get(words[-1])


def _duration_rounds(text: str) -> tuple[int | None, bool]:
    """Duración en rondas. Devuelve (rondas, reconocida).

    ``rondas`` None significa "hasta el fin del combate" (duración reconocida
    pero no acotada). El segundo valor dice si la duración se entendió.
    """
    if not text:
        return None, False
    if DURATION_NEXT_TURN_RE.search(text):
        return 1, True
    if DURATION_HOURS_RE.search(text):
        # Una hora o más: hasta el fin del combate.
        # TODO: modelar el paso del tiempo real.
        return None, True
    if DURATION_UNTIL_DESTROYED_RE.search(text):
        # Fin del combate (ver shortcut en la definición del patrón).
        return None, True
    match = DURATION_MINUTES_RE.search(text)
    if match:
        return int(match.group(1)) * 10, True
    return None, False


def _sentence_with(desc: str, position: int) -> str:
    """Frase (separada por '.') que contiene la posición indicada."""
    inicio = desc.rfind(".", 0, position) + 1
    fin = desc.find(".", position)
    if fin == -1:
        fin = len(desc)
    return desc[inicio:fin]


def _dc_ability(dc_info: dict | None, frase: str) -> tuple[int, str] | None:
    """(CD, característica): del campo `dc` si existe, si no de la frase.

    Acepta el orden 2014 («DC 11 Strength saving throw») y el 2024
    («Strength Saving Throw: DC 11»). Devuelve None si no hay CD.
    """
    if isinstance(dc_info, dict) and dc_info:
        dc = int(dc_info.get("dc_value", 0) or 0)
        tipo = dc_info.get("dc_type") or {}
        index = tipo.get("index") if isinstance(tipo, dict) else tipo
        return dc, str(index) if index else "dex"
    match = DC_SAVE_RE.search(frase)
    if match:
        return int(match.group(1)), match.group(2)
    match = DC_SAVE_2024_RE.search(frase)
    if match:
        return int(match.group(2)), match.group(1)
    return None


def parse_range_type(desc: str, monster_name: str = "", action_name: str = "") -> AttackRange:
    """Tipo de alcance de un ataque, deducido del texto de la acción.

    "Melee Weapon Attack" -> MELEE; "Ranged Weapon Attack" -> RANGED;
    "Melee or Ranged Weapon Attack" -> MELEE_OR_RANGED.
    """
    text = str(desc or "")
    if not text:
        return AttackRange.MELEE
    melee = bool(MELEE_RE.search(text))
    ranged = bool(RANGED_RE.search(text))
    if melee and ranged:
        return AttackRange.MELEE_OR_RANGED
    if ranged:
        return AttackRange.RANGED
    if melee:
        return AttackRange.MELEE
    warnings.warn(
        f"Tipo de ataque no reconocido en la acción {action_name!r} de "
        f"{monster_name!r}: se asume cuerpo a cuerpo. "
        f"# TODO: ampliar el vocabulario.",
        stacklevel=2,
    )
    return AttackRange.MELEE


def parse_condition_effects(action: dict, monster_name: str = "",
                            dc_info: dict | None = None,
                            allow_extra_patterns: bool = False) -> list[ConditionEffect]:
    """Efectos de condición de una acción de la API.

    Dos casos:

    a) La condición depende de un fallo de salvación ("saving throw or be
       <cond>"): el objetivo tira la salvación y, si falla, recibe la
       condición. La variante 2024 (a2) la describe tras «Failure: The
       target has the <cond> condition» con la CD en «Word Saving Throw:
       DC N».
    b) La condición se aplica directamente (sin salvación) pero la acción
       ofrece una prueba de escape ("DC 12 Strength check", "escape DC 16"):
       el estado se puede liberar con esa prueba. La variante 2024 (b2)
       aplica la condición al impactar sin escapatoria ("it has the Prone
       condition"), con la misma duración que «knocked prone».

    Las condiciones excluidas avisan y no se aplican. Las condiciones sin
    salida (ni salvación ni escape) también avisan y no se aplican.

    ``allow_extra_patterns`` habilita dos patrones extra ("saving throw
    against this magic or become X" y "saving throw or take ... damage and
    be X"), que solo usan las acciones legendarias: con el valor por
    defecto el comportamiento del loader normal no cambia.
    """
    desc = str(action.get("desc") or "")
    nombre = str(action.get("name") or "")
    if not desc:
        return []
    low = desc.lower()

    # 1. Condiciones excluidas: aviso y no se aplican.
    for clave, motivo in EXCLUDED_CONDITIONS.items():
        if re.search(rf"\b{re.escape(clave)}\b", low):
            warnings.warn(
                f"La acción {nombre!r} de {monster_name!r} menciona la condición "
                f"excluida {clave!r} ({motivo}); no se aplica. "
                f"# TODO: modelar si procede.",
                stacklevel=2,
            )

    escape = parse_escape(desc, monster_name, nombre)
    efectos: list[ConditionEffect] = []
    aplicadas: set[Condition] = set()

    # (a) Condiciones ligadas a un fallo de salvación.
    patrones = [SAVE_OR_CONDITION_RE]
    if allow_extra_patterns:
        patrones.append(SAVE_AGAINST_OR_CONDITION_RE)
        patrones.append(SAVE_OR_DAMAGE_AND_CONDITION_RE)
    for patron in patrones:
        for match in patron.finditer(desc):
            condicion = _condition_from_phrase(match.group(1))
            if condicion is None:
                continue
            frase = _sentence_with(desc, match.start())

            # La CD y la característica: del campo `dc` si existe, si no del texto.
            dc_ability = _dc_ability(dc_info, frase)
            if dc_ability is None:
                continue
            dc, ability = dc_ability
            try:
                ability = normalize_ability(ability)
            except Exception:
                ability = "dex"

            # Duración.
            resto = match.group("rest") or ""
            if "knocked" in match.group(1).lower():
                rondas, reconocida = KNOCKED_PRONE_ROUNDS, True
            else:
                rondas, reconocida = _duration_rounds(resto)
            if not reconocida:
                warnings.warn(
                    f"Duración no reconocida en la condición {condicion.value!r} de la "
                    f"acción {nombre!r} de {monster_name!r}: no se aplica. "
                    f"# TODO: no adivinar la duración.",
                    stacklevel=2,
                )
                continue

            repeat = bool(REPEAT_SAVE_RE.search(desc))
            efectos.append(ConditionEffect(
                condition=condicion,
                save_ability=ability,
                dc=dc,
                duration_rounds=rondas,
                repeat_save=repeat,
                escape=escape,
            ))
            aplicadas.add(condicion)

    # (a2) Texto 2024: «Constitution Saving Throw: DC 10. Failure: The
    # target has the Paralyzed condition ...» (ghoul Claw, giant-spider
    # Web). La CD sale del campo `dc` o de la frase; la condición, de la
    # cláusula «Failure:».
    for match in FAILURE_CONDITION_RE.finditer(desc):
        keyword = match.group(1).lower()
        condicion = CONDITION_KEYWORDS.get(keyword)
        if condicion is None or condicion in aplicadas:
            continue
        if keyword in EXCLUDED_CONDITIONS:
            continue  # ya avisado en el paso 1
        dc_ability = _dc_ability(dc_info, desc)
        if dc_ability is None:
            continue
        dc, ability = dc_ability
        try:
            ability = normalize_ability(ability)
        except Exception:
            ability = "dex"
        rondas, reconocida = _duration_rounds(match.group("rest") or "")
        if not reconocida:
            warnings.warn(
                f"Duración no reconocida en la condición {condicion.value!r} de la "
                f"acción {nombre!r} de {monster_name!r}: no se aplica. "
                f"# TODO: no adivinar la duración.",
                stacklevel=2,
            )
            continue
        efectos.append(ConditionEffect(
            condition=condicion,
            save_ability=ability,
            dc=dc,
            duration_rounds=rondas,
            repeat_save=bool(REPEAT_SAVE_RE.search(desc)),
            escape=escape,
        ))
        aplicadas.add(condicion)

    # (b) Condiciones sin salvación pero con prueba de escape.
    if escape is not None:
        for clave, condicion in CONDITION_KEYWORDS.items():
            if condicion in aplicadas:
                continue
            if not re.search(rf"\b{re.escape(clave)}\b", low):
                continue
            if clave in EXCLUDED_CONDITIONS:
                continue  # ya avisado antes
            # Duración: si el texto no la da, el estado dura hasta que se
            # libere (o hasta el fin del combate).
            rondas, _ = _duration_rounds(desc)
            efectos.append(ConditionEffect(
                condition=condicion,
                save_ability=None,
                dc=0,
                duration_rounds=rondas,
                repeat_save=False,
                escape=escape,
            ))
            aplicadas.add(condicion)

    # (b2) Texto 2024: «it has the Prone condition» sin salvación (wolf
    # Bite, chimera Ram): el golpe la aplica y dura lo mismo que «knocked
    # prone» — la criatura se levanta en su siguiente turno.
    for match in AUTO_CONDITION_RE.finditer(desc):
        keyword = match.group(1).lower()
        condicion = CONDITION_KEYWORDS.get(keyword)
        if condicion is None or condicion in aplicadas:
            continue
        if keyword in EXCLUDED_CONDITIONS:
            continue  # ya avisado en el paso 1
        efectos.append(ConditionEffect(
            condition=condicion,
            save_ability=None,
            dc=0,
            duration_rounds=KNOCKED_PRONE_ROUNDS,
            repeat_save=False,
            escape=escape,
        ))
        aplicadas.add(condicion)

    # (c) Condiciones mencionadas sin salida posible: aviso y no se aplican.
    for clave, condicion in CONDITION_KEYWORDS.items():
        if condicion in aplicadas:
            continue
        if not re.search(rf"\b{re.escape(clave)}\b", low):
            continue
        if clave in EXCLUDED_CONDITIONS:
            continue  # ya avisado antes
        warnings.warn(
            f"La condición {condicion.value!r} de la acción {nombre!r} de "
            f"{monster_name!r} no depende de una salvación reconocible ni de una "
            f"prueba de escape: no se aplica. # TODO: modelar efectos condicionales.",
            stacklevel=2,
        )
    return efectos


def has_condition_text(action: dict) -> bool:
    """¿El texto de la acción menciona alguna condición del Enum?"""
    low = str(action.get("desc") or "").lower()
    return any(re.search(rf"\b{re.escape(clave)}\b", low)
               for clave in CONDITION_KEYWORDS)


__all__ = [
    "CONDITION_KEYWORDS", "parse_condition_effects", "parse_range_type",
    "has_condition_text",
]

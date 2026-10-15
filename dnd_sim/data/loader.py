"""Carga de monstruos de la API como Combatant."""
from __future__ import annotations

import warnings

# TODO: Multiataque es una acción de texto libre que aún no se parsea.

try:
    from ..abilities import Abilities
    from ..attack import Attack
    from ..combatant import Combatant
    from ..damage import DamageType
    from .api_client import get_monster
except ImportError:  # ejecución como script suelto (cwd en dnd_sim o data)
    try:
        from abilities import Abilities
        from attack import Attack
        from combatant import Combatant
        from damage import DamageType
        from api_client import get_monster
    except ImportError:
        from dnd_sim.abilities import Abilities
        from dnd_sim.attack import Attack
        from dnd_sim.combatant import Combatant
        from dnd_sim.damage import DamageType
        from dnd_sim.data.api_client import get_monster


def _armor_class_value(raw) -> int:
    """Soporta ac como número o como lista de objetos con 'value'."""
    if isinstance(raw, bool):
        return int(raw)
    if isinstance(raw, (int, float)):
        return int(raw)
    if isinstance(raw, dict):
        if "value" in raw:
            return int(raw["value"])
        # Algunas variantes devuelven el valor bajo otra clave.
        for v in raw.values():
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                return int(v)
        return 0
    if isinstance(raw, (list, tuple)):
        if not raw:
            return 0
        first = raw[0]
        if isinstance(first, dict):
            return int(first.get("value", 0))
        if isinstance(first, (int, float, bool)):
            return int(first)
        return _armor_class_value(first)
    return int(raw)


def _damage_type(entry: dict) -> str:
    dt = entry.get("damage_type") or {}
    if isinstance(dt, dict):
        return str(dt.get("index") or dt.get("name") or "bludgeoning").lower()
    if isinstance(dt, str):
        return dt.lower()
    return "bludgeoning"


def _simple_damage_modifiers(values) -> set:
    """Convierte una lista de la API en set de DamageType.

    Los tipos simples ('fire', 'poison', ...) se añaden. Los textos complejos
    ('bludgeoning, piercing, and slashing from nonmagical weapons', etc.)
    no se parsean todavía: se emite un warnings.warn y se omiten.
    TODO: requiere un campo `magical: bool` en Attack para distinguir daño
    mágico/no mágico y resolver esos modificadores compuestos.
    """
    result = set()
    for raw in values or []:
        text = str(raw).strip()
        if not text:
            continue
        simple = text.lower().replace(" ", "")
        try:
            result.add(DamageType(simple))
            continue
        except ValueError:
            pass
        warnings.warn(
            f"Modificador de daño complejo ignorado (no soportado aún): {text!r}",
            stacklevel=2,
        )
    return result


def load_monster(index: str, team: str = "NPC") -> Combatant:
    """Convierte un monstruo de la API en un Combatant listo para simular."""
    data = get_monster(index)

    abilities = Abilities(
        str=int(data.get("strength", 10)),
        dex=int(data.get("dexterity", 10)),
        con=int(data.get("constitution", 10)),
        int=int(data.get("intelligence", 10)),
        wis=int(data.get("wisdom", 10)),
        cha=int(data.get("charisma", 10)),
    )

    attacks = []
    for action in data.get("actions") or []:
        # TODO: Multiataque (acción de texto libre) y otras acciones sin tirada
        # de ataque se ignoran por ahora.
        attack_bonus = action.get("attack_bonus")
        damage_list = action.get("damage") or []
        if attack_bonus is None or not damage_list:
            # Salvaciones, aliento, multiataque, etc.
            continue

        # Si hay varios tipos de daño, usamos el primero como principal.
        # TODO: se ignoran los tipos de daño adicionales.
        first_damage = damage_list[0]

        damage_dice = (
            first_damage.get("damage_dice")
            or first_damage.get("damage")
            or first_damage.get("dice")
        )
        if not damage_dice:
            continue

        attacks.append(
            Attack(
                name=action.get("name", "Ataque"),
                damage=str(damage_dice),
                ability="str",
                proficient=True,
                attack_bonus=int(attack_bonus),
                # El daño de la API ya incluye el bonus ("2d8+4");
                # evitamos doble conteo fijando el bonus a 0.
                damage_bonus=0,
                damage_type=_damage_type(first_damage),
            )
        )

    if not attacks:
        raise ValueError(
            f"El monstruo {data.get('name', index)!r} no tiene ataques válidos."
        )

    return Combatant(
        name=data.get("name", index),
        team=team,
        max_hp=int(data.get("hit_points", data.get("hit_points", 1))),
        ac=_armor_class_value(data.get("armor_class", 10)),
        abilities=abilities,
        attacks=attacks,
        proficiency=int(data.get("proficiency_bonus", 2)),
        resistances=_simple_damage_modifiers(data.get("damage_resistances")),
        vulnerabilities=_simple_damage_modifiers(data.get("damage_vulnerabilities")),
        immunities=_simple_damage_modifiers(data.get("damage_immunities")),
    )

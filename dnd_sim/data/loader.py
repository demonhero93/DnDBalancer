"""Carga de monstruos de la API como Combatant."""
from __future__ import annotations

import re
import warnings

# TODO: Multiataque es una acción de texto libre que aún no se parsea.

try:
    from ..abilities import Abilities
    from ..actions import ActionType, AttackEntry, MultiattackAction, SaveAction
    from ..attack import Attack
    from ..combatant import CombatantType, Monster
    from ..damage import DamageType
    from ..saves import SaveDamage, normalize_ability
    from .api_client import get_monster
    from .multiattack_parser import extract_multiattack_alternatives, resolve_multiattack
    from .save_builder import (build_save_action, build_save_effect,
                               damage_dice_of, damage_type_of)
    from .usage_parser import UnknownUsageError, parse_usage
except ImportError:  # ejecución como script suelto (cwd en dnd_sim o data)
    try:
        from abilities import Abilities
        from actions import ActionType, AttackEntry, MultiattackAction, SaveAction
        from attack import Attack
        from combatant import CombatantType, Monster
        from damage import DamageType
        from saves import SaveDamage, normalize_ability
        from api_client import get_monster
        from multiattack_parser import extract_multiattack_alternatives, resolve_multiattack
        from save_builder import (build_save_action, build_save_effect,
                                  damage_dice_of, damage_type_of)
        from usage_parser import UnknownUsageError, parse_usage
    except ImportError:
        from dnd_sim.abilities import Abilities
        from dnd_sim.actions import ActionType, AttackEntry, MultiattackAction, SaveAction
        from dnd_sim.attack import Attack
        from dnd_sim.combatant import CombatantType, Monster
        from dnd_sim.damage import DamageType
        from dnd_sim.saves import SaveDamage, normalize_ability
        from dnd_sim.data.api_client import get_monster
        from dnd_sim.data.multiattack_parser import (extract_multiattack_alternatives,
                                                      resolve_multiattack)
        from dnd_sim.data.save_builder import (build_save_action, build_save_effect,
                                               damage_dice_of, damage_type_of)
        from dnd_sim.data.usage_parser import UnknownUsageError, parse_usage


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
    """Alias del helper compartido (compatibilidad interna)."""
    return damage_type_of(entry)


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


def _norm_name(value: str) -> str:
    return "".join(str(value).lower().split())


def _extract_multiattack_alternatives(raw_action: dict) -> list[list[dict]]:
    """Alternativas del multiataque (delegado al parser de la API)."""
    return extract_multiattack_alternatives(raw_action)


def load_monster(index: str, team: str = "NPC", combatant_type=None) -> Monster:
    """Convierte un monstruo de la API en un Combatant listo para simular."""
    data = get_monster(index)
    monster_name = data.get("name", index)

    abilities = Abilities(
        str=int(data.get("strength", 10)),
        dex=int(data.get("dexterity", 10)),
        con=int(data.get("constitution", 10)),
        int=int(data.get("intelligence", 10)),
        wis=int(data.get("wisdom", 10)),
        cha=int(data.get("charisma", 10)),
    )

    # Salvaciones del monstruo (totales de la ficha).
    save_overrides = {}
    for prof in data.get("proficiencies") or []:
        if not isinstance(prof, dict):
            continue
        prof_obj = prof.get("proficiency") if isinstance(prof.get("proficiency"), dict) else None
        idx = prof.get("index")
        if idx is None and isinstance(prof_obj, dict):
            idx = prof_obj.get("index")
        if not isinstance(idx, str) or not idx.startswith("saving-throw-"):
            continue
        abbr = idx[len("saving-throw-"):]
        try:
            abbr = normalize_ability(abbr)
        except Exception:
            pass
        value = prof.get("value")
        if value is None and isinstance(prof_obj, dict):
            value = prof_obj.get("value")
        if value is None:
            continue
        save_overrides[abbr] = int(value)

    # Primera pasada: ataques sueltos válidos.
    attacks = []
    save_actions: list = []
    for action in data.get("actions") or []:
        name = str(action.get("name") or "")
        desc = str(action.get("desc") or "")
        # El Multiataque no es un ataque suelto utilizable directamente.
        if "multiattack" in name.lower() or "multiattack" in desc.lower():
            continue
        attack_bonus = action.get("attack_bonus")
        damage_list = action.get("damage") or []
        dc_info = action.get("dc")

        # Acciones de salvación propias (con dc + daño), con uso limitado
        # opcional ("recharge on roll", "per day"...).
        if attack_bonus is None and isinstance(dc_info, dict) and damage_list:
            try:
                usage = parse_usage(action.get("usage"), monster_name, name)
            except UnknownUsageError:
                # Tipo de uso desconocido: se omite la acción (ya avisado).
                continue
            # TODO: con varias entradas de damage en un área se usa la primera.
            eff = build_save_effect(dc_info, damage_list[0])
            if eff is None:
                continue
            # De área (según el clasificador) o de objetivo único.
            save_actions.append(build_save_action(action, eff, usage))
            continue

        # Acciones con dc sin daño (condiciones) -> se ignoran con TODO.
        if attack_bonus is None and isinstance(dc_info, dict) and not damage_list:
            # TODO: condiciones (aturdido, paralizado...), Áreas de efecto.
            continue

        if attack_bonus is None or not damage_list:
            # Salvaciones, aliento, etc.
            continue

        # Separar entradas de daño con dc (riders) de las demás.
        rider_entries = [d for d in damage_list if isinstance(d, dict) and "dc" in d]
        main_candidates = [d for d in damage_list if not (isinstance(d, dict) and "dc" in d)]

        # Si no hay candidato principal, usamos el primero disponible.
        if not main_candidates:
            main_candidates = [damage_list[0]]

        first_damage = main_candidates[0]

        damage_dice = damage_dice_of(first_damage)
        if not damage_dice:
            continue

        # Construir riders estructurados.
        riders = []
        for entry in rider_entries:
            dc_i = entry.get("dc") if isinstance(entry.get("dc"), dict) else None
            if not dc_i:
                continue
            dc_type = dc_i.get("dc_type") or {}
            dc_abbr = dc_type.get("index") if isinstance(dc_type, dict) else dc_type
            ability = normalize_ability(dc_abbr) if dc_abbr else "dex"
            success_type = str(dc_i.get("success_type") or "none").lower()
            on_success = "half" if success_type == "half" else "none"
            dice_i = damage_dice_of(entry)
            if not dice_i:
                continue
            riders.append(
                SaveDamage(
                    ability=ability,
                    dc=int(dc_i.get("dc_value", 0)),
                    damage=str(dice_i),
                    damage_type=_damage_type(entry),
                    on_success=on_success,
                )
            )

        # Rider desde texto (fallback para casos reales como giant-spider).
        if not riders and isinstance(dc_info, dict) is False:
            # buscar patrón DC en la descripción
            m = re.search(r"DC\s*(\d+)\s+(\w+)\s+saving throw", desc, re.I)
            if m:
                dmg_m = re.search(r"taking\s+(?:\d+\s*\()?\s*(\d+d\d+(?:\s*[+-]\s*\d+)?)\s*\)?\s+(\w+)\s+damage", desc, re.I)
                if dmg_m:
                    dc_val = int(m.group(1))
                    ability_word = m.group(2)
                    try:
                        ability_fb = normalize_ability(ability_word)
                    except Exception:
                        ability_fb = "con"
                    dice_fb = dmg_m.group(1).replace(" ", "")
                    type_fb = dmg_m.group(2).lower()
                    on_success_fb = "half" if "half as much" in desc.lower() else "none"
                    try:
                        riders.append(
                            SaveDamage(
                                ability=ability_fb,
                                dc=dc_val,
                                damage=dice_fb,
                                damage_type=type_fb,
                                on_success=on_success_fb,
                            )
                        )
                    except Exception:
                        pass

        # TODO: tipos de daño adicionales ignorados.
        # Uso limitado opcional del ataque (p. ej. "recharge on roll").
        try:
            usage = parse_usage(action.get("usage"), monster_name, name)
        except UnknownUsageError:
            # Tipo de uso desconocido: se omite la acción (ya avisado).
            continue
        atk = Attack(
            name=action.get("name", "Ataque"),
            damage=str(damage_dice),
            ability="str",
            proficient=True,
            attack_bonus=int(attack_bonus),
            damage_bonus=0,
            damage_type=_damage_type(first_damage),
            save_riders=riders,
            usage=usage,
        )
        attacks.append(atk)

    if not attacks:
        raise ValueError(
            f"El monstruo {monster_name!r} no tiene ataques válidos."
        )

    # Segunda pasada: Multiataque estructurado.
    multiattack = None
    for action in data.get("actions") or []:
        action_name = str(action.get("name") or "")
        desc = str(action.get("desc") or "")
        is_multi = "multiattack" in action_name.lower() or "multiattack" in desc.lower()
        if not is_multi:
            continue

        alternatives_raw = _extract_multiattack_alternatives(action)
        if not alternatives_raw:
            # Solo texto libre: no parseamos con regex frágiles.
            warnings.warn(
                f"Multiattack en texto libre no parseado para {monster_name!r}: "
                f"{desc!r}. Se usan ataques sueltos. "
                f"# TODO: parsear si la API aporta datos estructurados.",
                stacklevel=2,
            )
            continue

        # Resolver action_name contra los ataques extraídos (tolerante a
        # mayúsculas/espacios). Error explícito si no coincide.
        # Resolver las entradas contra los ataques y acciones del monstruo.
        try:
            alternatives = resolve_multiattack(alternatives_raw, attacks,
                                               save_actions, monster_name)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"El Multiataque de {monster_name!r} es inválido: {exc}. "
                f"Texto: {desc!r}"
            ) from exc

        # Convención: los ataques referenciados dejan de competir como acciones
        # sueltas; solo viven dentro del Multiataque. Lo mismo con las
        # acciones (p. ej. el Aliento de la quimera, que sustituye a un
        # ataque dentro del multiataque).
        referenced = {e.attack_name for alt in alternatives for e in alt
                      if not getattr(e, "is_action", False)}
        for atk in attacks:
            if atk.name in referenced:
                atk.only_in_multiattack = True

        referenced_actions = {e.attack_name for alt in alternatives for e in alt
                              if getattr(e, "is_action", False)}
        action_entries = {}
        if referenced_actions:
            action_entries = {getattr(a, "name", ""): a for a in save_actions
                              if getattr(a, "name", "") in referenced_actions}
            # No se ofrece como acción suelta (solo dentro del multiataque).
            save_actions = [a for a in save_actions
                            if getattr(a, "name", "") not in referenced_actions]

        multiattack = MultiattackAction(options=alternatives,
                                        action_entries=action_entries)
        break

    if combatant_type is None:
        combatant_type = CombatantType.PLAYER if team == "PJ" else CombatantType.NPC
    if isinstance(combatant_type, str):
        combatant_type = CombatantType(combatant_type)

    # Acciones de salvación y riders se conservan.
    # save_actions ya construidas pasan al Monster como actions adicionales.
    extra_actions = list(save_actions)

    return Monster(
        name=monster_name,
        combatant_type=combatant_type,
        max_hp=int(data.get("hit_points", data.get("hit_points", 1))),
        ac=_armor_class_value(data.get("armor_class", 10)),
        abilities=abilities,
        attacks=attacks,
        proficiency=int(data.get("proficiency_bonus", 2)),
        resistances=_simple_damage_modifiers(data.get("damage_resistances")),
        vulnerabilities=_simple_damage_modifiers(data.get("damage_vulnerabilities")),
        immunities=_simple_damage_modifiers(data.get("damage_immunities")),
        multiattack=multiattack,
        save_overrides=save_overrides,
        actions=extra_actions,
    )

"""Interpreta ``special_abilities`` y devuelve los rasgos modelables.

La ficha trae rasgos de todo tipo: de combate (Blood Frenzy), de
exploración (Limited Amphibiousness), de flavor (Shark Telepathy) o que ya
gestiona otro módulo (Spellcasting, Legendary Resistance). Solo se devuelven
los registrados en :data:`dnd_sim.traits.TRAIT_CLASSES`; el resto se
**ignoran sin aviso**: no cambian un combate y avisar de ellos solo añade
ruido (los que sí cambian uno ya tienen su aviso en su propio módulo).
"""
from __future__ import annotations

try:
    from ..traits import TRAIT_CLASSES, Trait
except ImportError:  # pragma: no cover - ejecución como script suelto
    try:
        from traits import TRAIT_CLASSES, Trait
    except ImportError:
        from dnd_sim.traits import TRAIT_CLASSES, Trait


def parse_traits(monster_json: dict) -> list[Trait]:
    """Rasgos modelables del monstruo (``special_abilities``).

    Cada entrada reconocida se construye con su nombre tal cual viene en la
    API y su descripción (de referencia). Las entradas desconocidas o
    malformadas se omiten.
    """
    traits: list[Trait] = []
    for ability in monster_json.get("special_abilities") or []:
        if not isinstance(ability, dict):
            continue
        nombre = str(ability.get("name") or "").strip()
        clase = TRAIT_CLASSES.get(nombre.lower())
        if clase is None:
            continue  # no combativo, de flavor o gestionado por otro parser
        traits.append(clase(name=nombre, desc=str(ability.get("desc") or "")))
    return traits


__all__ = ["parse_traits"]

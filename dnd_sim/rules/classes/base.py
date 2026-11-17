"""Registro genérico de clases y subclases jugables.

El registro es el dict :data:`CLASSES`, con una entrada por clase
(:class:`ClassDef`) y, dentro, sus subclases (:class:`SubclassDef`).
Solo está implementada la clase bárbaro; el mecanismo es genérico y
cualquier clase futura se da de alta con :func:`register_class`.

Convención de los ``apply``:

* de clase: ``apply(pj, **kwargs)`` (p. ej. ``skills``/``level``);
* de subclase: ``apply(pj, level=None)`` (recibe siempre ``level``,
  aunque sea ``None``: la subclase lo resuelve con ``pj.level``).

Los nombres se normalizan a minúsculas con ``_`` (espacios y guiones
también son ``_``): ``"Ancestral Guardian"`` → ``"ancestral_guardian"``.
El registro se completa al importar el paquete de la clase (vía
``dnd_sim.rules.classes``), que es quien declara sus subclases.
"""
from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable

from ...core.classes import MIN_LEVEL
from ...core.spellcasting import SpellcastingDef


@dataclass
class SubclassDef:
    """Definición de una subclase: nombre, clase, nivel mínimo y apply."""

    name: str
    class_name: str
    min_level: int
    apply: Callable[..., Any]
    #: Lanzamiento de conjuros de la subclase (Eldritch Knight...);
    #: ``None`` = sin lanzamiento (cambio cero para las existentes).
    spellcasting: SpellcastingDef | None = None


@dataclass
class ClassDef:
    """Definición de una clase: nombre, apply y sus subclases por clave."""

    name: str
    apply: Callable[..., Any]
    subclasses: dict[str, SubclassDef] = field(default_factory=dict)
    #: Lanzamiento de conjuros de la clase; ``None`` = sin él.
    spellcasting: SpellcastingDef | None = None


#: Registro global de clases (clave normalizada → ClassDef).
CLASSES: dict[str, ClassDef] = {}


def normalize_class_name(name: Any) -> str:
    """Normaliza un nombre de clase o subclase (minúsculas, ``_``)."""
    return str(name).strip().lower().replace(" ", "_").replace("-", "_")


def register_class(class_def: ClassDef) -> ClassDef:
    """Registra ``class_def`` (normalizando su nombre y el de sus subclases)."""
    key = normalize_class_name(class_def.name)
    class_def.name = key
    class_def.subclasses = {
        normalize_class_name(k): v for k, v in class_def.subclasses.items()
    }
    CLASSES[key] = class_def
    return class_def


def _params_de(func: Any) -> set[str]:
    """Nombres de parámetros que declara ``func`` (vacío si no se puede)."""
    try:
        return set(inspect.signature(func).parameters)
    except (TypeError, ValueError):
        return set()


def apply_class(pj: Any, class_name: str, subclass_name: str | None = None,
                **kwargs: Any) -> Any:
    """Aplica la clase ``class_name`` a ``pj`` y, si se indica, su subclase.

    Valida **antes** de tocar al personaje: que la clase exista, que la
    subclase pertenezca a esa clase y que el nivel del PJ alcance
    ``min_level`` de la subclase (ValueError con las opciones válidas).
    Después aplica la clase con ``**kwargs`` y la subclase con
    ``level=kwargs.get("level")`` más, como **reenvío perezoso**, los
    kwargs que SOLO declare el apply de la subclase (p. ej. ``lista``/
    ``cantrips``/``spells`` de Eldritch Knight: no van a la clase para
    no reventar su firma) y los compartidos (p. ej. ``rng``) en ambas
    llamadas. Los calls existentes solo pasan ``level`` a la subclase →
    llamada idéntica. Devuelve lo que devuelva el apply de la clase.
    """
    key = normalize_class_name(class_name)
    clase = CLASSES.get(key)
    if clase is None:
        raise ValueError(
            f"Clase desconocida {class_name!r}: válidas {sorted(CLASSES)}."
        )
    sub: SubclassDef | None = None
    if subclass_name is not None:
        skey = normalize_class_name(subclass_name)
        sub = clase.subclasses.get(skey)
        if sub is None:
            raise ValueError(
                f"{subclass_name!r} no es una subclase de {key!r}: "
                f"válidas {sorted(clase.subclasses)}."
            )
        lvl = kwargs.get("level")
        if lvl is None:
            lvl = getattr(pj, "level", None)
        lvl = MIN_LEVEL if lvl is None else int(lvl)
        if lvl < sub.min_level:
            raise ValueError(
                f"{sub.name} requiere nivel >= {sub.min_level}: "
                f"{getattr(pj, 'name', pj)} tiene nivel {lvl}."
            )
    p_clase = _params_de(clase.apply)
    p_sub = _params_de(sub.apply) if sub is not None else set()
    # Claves que solo la subclase declara: fuera del apply de la clase
    # (si no, TypeError por parámetro desconocido en la firma de clase).
    solo_sub = {k for k in kwargs
                if k in p_sub and k not in p_clase and k not in ("pj", "level")}
    kwargs_clase = {k: v for k, v in kwargs.items() if k not in solo_sub}
    trait = clase.apply(pj, **kwargs_clase)
    if sub is not None:
        extra = {k: v for k, v in kwargs.items()
                 if k in p_sub and k not in ("pj", "level")}
        sub.apply(pj, level=kwargs.get("level"), **extra)
    return trait


__all__ = ["CLASSES", "ClassDef", "SubclassDef", "apply_class",
           "normalize_class_name", "register_class"]

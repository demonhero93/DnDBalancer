"""Pool de hechizos soportado para un PJ lanzador.

Un hechizo solo entra en el pool si el motor sabe ejecutarlo con las
acciones de hechizo ya existentes (ataque, salvación con daño, área,
condición, curación, estado o daño fijo) y si su tiempo de lanzamiento
es la acción Magia. El resto (ritual, utilidad, buffs sin efecto
modelable, reacciones de hechizo como Shield o Absorb Elements,
hechizos de acción bonus) queda FUERA: ver «Hechizos de PJ: pendientes
reales» en ``TODO.md``.
"""
from __future__ import annotations

import random
from typing import Any

from ...core.randomness import sample
from ...model.actions import ActionType
from .casting import Spell


def hechizo_soportado(spell: Any) -> bool:
    """¿Puede el motor lanzar ``spell`` como acción de un PJ?

    ``False`` si es ``None``, si el parser lo marcó ``ignored`` (ritual,
    utilidad, 1 minuto...), si no tiene ``kind`` (sin efecto modelable)
    o si no se lanza con la acción Magia (acción bonus o reacción: la
    acción bonus bloquearía el resto del turno y la reacción no es una
    decisión de turno; ambas aplazadas en TODO.md).
    """
    if spell is None:
        return False
    if str(getattr(spell, "ignored", "") or ""):
        return False
    if not str(getattr(spell, "kind", "") or ""):
        return False
    tipo = getattr(spell, "action_type", ActionType.ACTION)
    return tipo is ActionType.ACTION


def preparar_hechizos(
    lista_clase: Any,
    nivel: int,
    def_: Any,
    *,
    trucos: Any = None,
    hechizos: Any = None,
    rng: random.Random | None = None,
) -> tuple[list[Spell], list[Spell]]:
    """Prepara los hechizos de un PJ al crearlo (lista fija).

    Devuelve ``(trucos_conocidos, hechizos_preparados)``.

    - El pool legal es la ``lista_clase`` filtrada por
      :func:`hechizo_soportado`, por las escuelas de ``def_`` si las
      restringe, y (para hechizos de nivel >= 1) por el mayor nivel de
      espacio disponible en ``nivel`` de PJ: un hechizo de nivel N solo
      entra si queda un espacio >= N. Los trucos (nivel 0) siempre son
      legales si están en el pool.
    - Sin kwargs: se toma un ``sample`` uniforme de cada pool hasta los
      conteos de la tabla (``def_.trucos_conocidos`` /
      ``def_.preparados``), con ``min(conteo, len(pool))`` elementos.
      ``rng`` por defecto con semilla 0: personaje reproducible.
    - Con kwargs explícitos: se validan (``ValueError`` si repiten, si
      exceden el conteo, o si no están en el pool legal — mensaje
      concreto para «truco como preparado» y «nivel inalcanzable») y se
      usan tal cual, sin RNG. El kwarg no dado se muestrea igual que
      arriba.
    """
    escuelas = getattr(def_, "escuelas", None)
    escuelas_norm = ({str(e).strip().lower() for e in escuelas}
                     if escuelas else None)

    def _legal(spell: Any) -> bool:
        if not hechizo_soportado(spell):
            return False
        if escuelas_norm is not None:
            escuela = str(getattr(spell, "school", "") or "").strip().lower()
            if escuela not in escuelas_norm:
                return False
        return True

    pool = [s for s in (lista_clase or []) if _legal(s)]
    espacios = def_.espacios(nivel)
    max_slot = max((i for i, n in enumerate(espacios, 1) if n > 0),
                   default=0)
    pool_trucos = [s for s in pool
                   if int(getattr(s, "level", 0) or 0) == 0]
    pool_preparables = [s for s in pool
                        if 1 <= int(getattr(s, "level", 0) or 0) <= max_slot]
    cuenta_trucos = max(0, int(def_.trucos_conocidos.get(nivel, 0) or 0))
    cuenta_preparados = max(0, int(def_.preparados.get(nivel, 0) or 0))

    def _validar(sel: list[Spell], pool_ok: list[Spell], cuenta: int,
                 categoria: str) -> list[Spell]:
        if len(sel) > cuenta:
            raise ValueError(
                f"{categoria}: {len(sel)} hechizos, el conteo de la tabla "
                f"para nivel {nivel} es {cuenta}.")
        vistos: set[Any] = set()
        for s in sel:
            clave = getattr(s, "index", None) or id(s)
            if clave in vistos:
                raise ValueError(f"{categoria}: hechizo repetido "
                                 f"{getattr(s, 'name', s)!r}.")
            vistos.add(clave)
            if s in pool_ok:
                continue
            niv_s = int(getattr(s, "level", 0) or 0)
            if categoria == "hechizos preparados" and niv_s == 0:
                raise ValueError(f"{categoria}: {getattr(s, 'name', s)!r} "
                                 f"es un truco; no puede prepararse.")
            if niv_s > max_slot:
                raise ValueError(
                    f"{categoria}: {getattr(s, 'name', s)!r} tiene nivel "
                    f"{niv_s} inalcanzable (mayor espacio disponible: "
                    f"{max_slot}).")
            raise ValueError(
                f"{categoria}: {getattr(s, 'name', s)!r} no está en el "
                f"pool legal (lista, soporte o escuela).")
        return list(sel)

    def _muestrear(pool_ok: list[Spell], cuenta: int) -> list[Spell]:
        k = min(cuenta, len(pool_ok))
        if k <= 0:
            return []
        if rng is None:
            return sample(random.Random(0), pool_ok, k)
        return sample(rng, pool_ok, k)

    if trucos is None:
        sel_trucos = _muestrear(pool_trucos, cuenta_trucos)
    else:
        sel_trucos = _validar(list(trucos), pool_trucos, cuenta_trucos,
                              "trucos conocidos")
    if hechizos is None:
        sel_hechizos = _muestrear(pool_preparables, cuenta_preparados)
    else:
        sel_hechizos = _validar(list(hechizos), pool_preparables,
                                cuenta_preparados, "hechizos preparados")
    return sel_trucos, sel_hechizos


__all__ = ["hechizo_soportado", "preparar_hechizos"]

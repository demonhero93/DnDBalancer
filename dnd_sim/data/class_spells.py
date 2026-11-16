"""Listas de hechizos de clase jugable desde la API (con caché en disco).

Carga ``GET /api/classes/<index>/spells`` (SRD 2024) con la misma
mecánica que el resto del cliente: caché en ``cache/classes/<index>.json``
primero, red después. Cada entrada de la lista se resuelve con el
cargador de hechizos existente (:func:`parse_spell`), de modo que el
resultado es una :class:`~dnd_sim.rules.spells.ClassSpellList` (lista de
``Spell`` ya interpretados) que la capa ``rules`` recibe como argumento:
``rules`` no importa de ``data``.

Los hechizos que no existen o que el parser no modela (ritual,
utilidad...) se omiten de la lista: no son candidatos a pool de PJ.

Los tests nunca acceden a la red: usan fixtures JSON y un ``get_spell``
sustituto.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

from ..rules.spells import ClassSpellList, Spellcasting
from .api_client import (API_BASE_URL, DEFAULT_TIMEOUT,
                         MonsterNotFoundError, NetworkError)
from .spell_parser import parse_spell

#: Caché de las listas de hechizos de clase (relativa al cwd).
CLASS_SPELL_CACHE_DIR = Path("cache") / "classes"


def _fetch_class_spells(index: str, *, cache_dir: Path | str | None = None,
                        force_refresh: bool = False,
                        timeout: int = DEFAULT_TIMEOUT) -> dict:
    """JSON de la lista de hechizos de una clase (caché en disco o red)."""
    base = Path(cache_dir) if cache_dir is not None else CLASS_SPELL_CACHE_DIR
    path = base / f"{index}.json"
    if not force_refresh and path.exists():
        try:
            with path.open("r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            pass  # caché corrupta: reintentar descarga

    url = f"{API_BASE_URL}/classes/{index}/spells"
    hint = (f"Puedes descargarlo manualmente con: curl -sS {url} "
            f"-o cache/classes/{index}.json")
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise MonsterNotFoundError(
                f"La clase {index!r} no existe en la API ({url})."
            ) from exc
        raise NetworkError(
            f"Error HTTP {exc.code} al pedir {url}: {exc.reason}. {hint}"
        ) from exc
    except urllib.error.URLError as exc:
        raise NetworkError(
            f"Sin red o error de conexión al pedir {url}: {exc.reason}. {hint}"
        ) from exc
    except TimeoutError as exc:
        raise NetworkError(f"Timeout al pedir {url}: {exc.reason}. {hint}") from exc

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
    except OSError:
        pass  # sin caché escribible no falla la carga
    return data


def load_class_spell_list(
    index: str,
    *,
    nivel_lanzador: int = 1,
    spellcasting: Spellcasting | None = None,
    get_spell: Callable[[str], dict] | None = None,
    cache_dir: Path | str | None = None,
    force_refresh: bool = False,
) -> ClassSpellList:
    """Lista de hechizos de la clase ``index``, ya parseados.

    - ``nivel_lanzador``: nivel del PJ que lanza; si no se pasa
      ``spellcasting``, se usa uno con ese nivel (escala los trucos con
      ``damage_at_character_level``).
    - ``spellcasting``: datos del lanzador para el parser (CD, MOD de
      curación, nivel); por defecto ninguno.
    - ``get_spell``: cargador de cada hechizo (por defecto el de la API
      con caché); los tests lo sustituyen por uno de fixtures.
    - ``cache_dir`` / ``force_refresh``: igual que en el resto del
      cliente (``cache/classes`` por defecto).

    Un hechizo inexistente o no modelado por el parser se omite.
    """
    raw_list = _fetch_class_spells(index, cache_dir=cache_dir,
                                   force_refresh=force_refresh)
    if get_spell is None:
        from .api_client import get_spell as _get
        get_spell = _get
    sc = spellcasting
    if sc is None:
        sc = Spellcasting(level=max(1, int(nivel_lanzador or 1)))
    lista: ClassSpellList = []
    for entrada in raw_list.get("results") or []:
        if not isinstance(entrada, dict):
            continue
        indice = str(entrada.get("index") or "").strip()
        if not indice:
            url = str(entrada.get("url") or "")
            indice = url.rstrip("/").split("/")[-1]
        if not indice:
            continue
        try:
            raw = get_spell(indice)
        except Exception:      # 404, red, JSON raro: se omite el hechizo
            continue
        spell = parse_spell(raw, "", sc)
        if spell is None:      # ritual, utilidad...: fuera del pool
            continue
        # El nivel de la lista de clase es el de la ficha (la API lo
        # trae en cada entrada); si viene, manda sobre el del JSON.
        nivel_entrada = entrada.get("level")
        if nivel_entrada is not None:
            try:
                spell.level = int(nivel_entrada)
                spell.slot_level = spell.level
            except (TypeError, ValueError):
                pass
        lista.append(spell)
    return lista


__all__ = ["CLASS_SPELL_CACHE_DIR", "load_class_spell_list"]

"""Cliente HTTP para la API de dnd5eapi.co con caché en disco."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

# Versión de reglas fijada por recurso: la migración a 2024 es **por partes**
# (decisión: solo hechizos ahora). Los hechizos ya salen del PHB 2024; los
# monstruos siguen en la SRD 2014 hasta su tarea de migración (su vocabulario
# de condiciones, salvaciones en texto y legendarias cambiaron en 2024).
SPELL_API_VERSION = "2024"
MONSTER_API_VERSION = "2014"
# Compatibilidad: la versión "por defecto" es la de los hechizos (2024).
API_VERSION = SPELL_API_VERSION
API_BASE_URL = f"https://www.dnd5eapi.co/api/{API_VERSION}"
MONSTER_API_BASE_URL = f"https://www.dnd5eapi.co/api/{MONSTER_API_VERSION}"
SPELL_API_BASE_URL = f"https://www.dnd5eapi.co/api/{SPELL_API_VERSION}"

# Directorio de caché (relativo al directorio de trabajo).
CACHE_DIR = Path("cache") / "monsters"
# Caché de los hechizos (PHB 2024).
SPELL_CACHE_DIR = Path("cache") / "spells"

DEFAULT_TIMEOUT = 15


class MonsterNotFoundError(ValueError):
    """El monstruo pedido no existe en la API."""


class NetworkError(RuntimeError):
    """No se pudo contactar con la API (sin red, DNS, timeout, ...)."""


def _cache_path(index: str, cache_dir: Path | None = None) -> Path:
    base = Path(cache_dir) if cache_dir is not None else CACHE_DIR
    return base / f"{index}.json"


def get_monster(
    index: str,
    force_refresh: bool = False,
    refresh: bool | None = None,
    force: bool | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    cache_dir: Path | str | None = None,
) -> dict:
    """Descarga (o lee de caché) el JSON de un monstruo por su índice.

    Parámetros
    ----------
    index:
        Índice del monstruo en la API (ej. ``"ogre"``).
    force_refresh / refresh / force:
        Si es verdadero, ignora la caché y vuelve a pedir a la red.
    timeout:
        Timeout HTTP en segundos.
    cache_dir:
        Directorio de caché alternativo (útil en tests).
    """
    # Alias del parámetro de refresco.
    if refresh is not None:
        force_refresh = bool(refresh)
    if force is not None:
        force_refresh = bool(force)

    path = _cache_path(index, cache_dir)

    # 1) Caché en disco: si existe y no se fuerza refresco, leer de disco.
    if not force_refresh and path.exists():
        try:
            with path.open("r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            # Caché corrupta: reintentar descarga.
            pass

    url = f"{MONSTER_API_BASE_URL}/monsters/{index}"

    # 2) Petición de red.
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise MonsterNotFoundError(
                f"El monstruo {index!r} no existe en la API ({url})."
            ) from exc
        hint = f"Puedes descargarlo manualmente con: curl -sS {url} -o cache/monsters/{index}.json"
        raise NetworkError(
            f"Error HTTP {exc.code} al pedir {url}: {exc.reason}. {hint}"
        ) from exc
    except urllib.error.URLError as exc:
        hint = f"Puedes descargarlo manualmente con: curl -sS {url} -o cache/monsters/{index}.json"
        raise NetworkError(
            f"Sin red o error de conexión al pedir {url}: {exc.reason}. {hint}"
        ) from exc
    except TimeoutError as exc:
        hint = f"Puedes descargarlo manualmente con: curl -sS {url} -o cache/monsters/{index}.json"
        raise NetworkError(f"Timeout al pedir {url}. {hint}") from exc

    # 3) Guardar en caché para futuras ejecuciones.
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
    except OSError:
        # Si no se puede escribir la caché, no fallar la función.
        pass

    return data


def get_spell(
    index: str,
    force_refresh: bool = False,
    refresh: bool | None = None,
    force: bool | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    cache_dir: Path | str | None = None,
) -> dict:
    """Descarga (o lee de caché) el JSON de un hechizo por su índice.

    Igual que :func:`get_monster`, pero en la caché de hechizos
    (``cache/spells``).
    """
    if refresh is not None:
        force_refresh = bool(refresh)
    if force is not None:
        force_refresh = bool(force)

    base = Path(cache_dir) if cache_dir is not None else SPELL_CACHE_DIR
    path = base / f"{index}.json"

    if not force_refresh and path.exists():
        try:
            with path.open("r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            pass

    url = f"{SPELL_API_BASE_URL}/spells/{index}"

    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise MonsterNotFoundError(
                f"El hechizo {index!r} no existe en la API ({url})."
            ) from exc
        hint = f"Puedes descargarlo manualmente con: curl -sS {url} -o cache/spells/{index}.json"
        raise NetworkError(
            f"Error HTTP {exc.code} al pedir {url}: {exc.reason}. {hint}"
        ) from exc
    except urllib.error.URLError as exc:
        hint = f"Puedes descargarlo manualmente con: curl -sS {url} -o cache/spells/{index}.json"
        raise NetworkError(
            f"Sin red o error de conexión al pedir {url}: {exc.reason}. {hint}"
        ) from exc
    except TimeoutError as exc:
        hint = f"Puedes descargarlo manualmente con: curl -sS {url} -o cache/spells/{index}.json"
        raise NetworkError(f"Timeout al pedir {url}. {hint}") from exc

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
    except OSError:
        pass

    return data
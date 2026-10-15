"""Cliente HTTP para la API de dnd5eapi.co con caché en disco."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

# Versión de reglas fijada para que los resultados sean consistentes.
API_VERSION = "2014"
API_BASE_URL = f"https://www.dnd5eapi.co/api/{API_VERSION}"

# Directorio de caché (relativo al directorio de trabajo).
CACHE_DIR = Path("cache") / "monsters"

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

    url = f"{API_BASE_URL}/monsters/{index}"

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
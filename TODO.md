# TODO — DnDBalancer / dnd_sim

Revisar al principio de cada sesión. Última revisión: 2026-10-30.
Contexto detallado: PASOS-ANTERIORES.txt (sección 7) y ARCHITECTURE.md.

## Bloque 2026-10-30 (commiteado)

- `ff30aac` feat(classes): registro de clases + Path of the Beast (20 ficheros).
- `667bc0a` docs: reglas, log de sesión y este TODO.
- `37b2806` chore(graph): grafo regenerado.
- Pendiente de push si hay remoto.

## TODOs en código (marcados `# TODO`)

- Bestial Soul: necesita flag `magical` en `Attack` (beast.py).
- Cola de la Bestia: no reacciona a ataques a distancia; movimiento y
  posiciones sin modelar (beast.py).
- Weapon Mastery y propiedades Light/Nick en armas naturales (beast.py).
- Resistencia legendaria y otros efectos pendientes en saves.py.

## Grafo y verificación

- `.graphify_labels.pending.json` tiene etiquetas sin confirmar.
- Mantener `graphify update .` y GRAPH_REPORT.md al día tras cambios.
- Verificación obligatoria tras cada cambio (regla 7):
  `pytest tests/test_arquitectura.py`, `pytest`,
  `python tools/capas.py` (con `PYTHONIOENCODING=utf-8` en Windows),
  `graphify update .`.

## Rutina sugerida al abrir sesión

1. Leer este archivo.
2. `git status` → ¿trabajo sin commitear?
3. `pytest -q` → ¿suite en verde? (sin red; usa `cache/monsters/`)
4. Empezar tarea nueva.

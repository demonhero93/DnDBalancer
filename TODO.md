# TODO — DnDBalancer / dnd_sim

Revisar al principio de cada sesión. Última revisión: 2026-10-30.
Contexto detallado: PASOS-ANTERIORES.txt (sección 7) y ARCHITECTURE.md.

## Sin commitear (bloque 2026-10-30, prioridad alta)

Todo el registro de clases y Path of the Beast está sin commitear.
Antes de empezar trabajo nuevo: `git status` y decidir si se commitea.

- Movidos (borrados en la raíz): `dnd_sim/rules/classes/{barbarian,ancestral_guardian,battlerager}.py`
  → paquete `dnd_sim/rules/classes/barbarian/`.
- Nuevos: `dnd_sim/rules/classes/base.py`, paquete `barbarian/` completo,
  `tests/test_clases.py`, `tests/test_beast.py`.
- Modificados: fachada `dnd_sim/__init__.py`, `engine/combat/attack.py`,
  `model/actions.py`, `model/combatant.py`, `rules/traits/base.py`,
  `main.py`, `ARCHITECTURE.md`, tests de bárbaro/ancestral/battlerager,
  `graphify-out/`.
- Sugerencia de commits (una idea por commit, regla 10.1):
  1. registro de clases (base + paquete barbarian + fachada);
  2. hooks de traits + dynamic_weapons + allow_friendly;
  3. subclase beast + sus tests;
  4. ARCHITECTURE.md + grafo.

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

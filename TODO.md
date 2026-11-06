# TODO — DnDBalancer / dnd_sim

Revisar al principio de cada sesión. Última revisión: 2026-11-06.
Solo tareas SIN implementar. Lo ya hecho: PASOS-ANTERIORES.txt
(bloque 15 «Clase Fighter», bloque «CIERRE DE PENDIENTES DEL FIGHTER»)
y ARCHITECTURE.md.

## Pendientes generales

- Push a `origin`: hay commits locales sin push (ver
  `git log origin/main..HEAD`).

## TODOs en código (marcados `# TODO`)

- Path of the Giant (`rules/classes/barbarian/subclasses/giant.py`):
  - Mighty Impel: alcance 9 m y «o criatura voluntaria» no modelados;
    solo se usa contra un enemigo con GRAPPLED (simplificación del
    enunciado). La decisión de usarlo o no la hace el `pick` del
    encuentro entre acciones candidatas (patrón Intimidating
    Presence).
- Path of Wild Magic (`rules/classes/barbarian/subclasses/wild_magic.py`):
  - La tabla Wild Surge de 8 efectos va de memoria [VERIFICAR]: si el
    usuario aporta el texto oficial, ese manda. La entrada 8 ocupa la
    ranura con «Pendiente» (sin efecto mecánico).
  - Bolstering Magic (6): acción adicional que da 1d3 a ataques y
    pruebas o recupera un espacio de conjuro [VERIFICAR texto]: sin
    bono plano a la tirada ni espacios de conjuro en el motor, sin
    efecto — solo dato (no se creó un hook solo por esto).
- Path of the World Tree (`rules/classes/barbarian/subclasses/world_tree.py`):
  - `Attack.properties`/`Attack.mastery` son campos nuevos con defaults
    vacíos: el loader NO los rellena, así que Battering Roots solo se
    activa en armas construidas en código con esas propiedades.

## Fighter: pendientes reales

- **Cleave** (maestría de hacha gigante/mandoble/alabarda): necesita el
  segundo golpe contra un objetivo adicional (sin motor de objetivos
  múltiples para maestrías).
- **Nick** (maestría de arma ligera): permite el ataque extra con
  acción de ataque; depende de que exista el ataque bonus/off-hand.
- **Two-Weapon Fighting**: sin efecto hasta que exista el ataque
  adicional (depende de Nick; el motor no tiene ataques bonus).
- **Push/Slow** (efecto de maestría): sin posiciones ni movimiento que
  desplazar (`# TODO` en `rules/mastery.py`).
- **Subclases Fighter**: receta en «Fighter: cómo añadir una subclase»;
  candidatas Champion, Battle Master, Eldritch Knight, Psi Warrior.

## Fighter: cómo añadir una subclase

Receta (patrón bárbaro, ver `barbarian/subclasses/`):

1. Crear `rules/classes/fighter/subclasses/<clave>.py` con un
   `SubclassDef(name="<clave>", class_name="fighter", min_level=3,
   apply=...)` y su rasgo (`Trait`) con los hooks necesarios.
2. Registrar en `rules/classes/fighter/__init__.py`: importar la
   `SubclassDef` y añadirla al dict `subclasses` del `FIGHTER_CLASS`.
3. Reexportar la API en la fachada `dnd_sim/__init__.py` (import +
   `__all__`) si expone símbolos nuevos.
4. Tests: `tests/test_<clave>.py` en español (registro, apply por
   `apply_class("fighter", subclass_name="<clave>", level=3)`, rasgos).
5. Actualizar `ARCHITECTURE.md` (tabla de paquetes con fachada) y el
   bloque Guerrero de `PASOS-ANTERIORES.txt`.

Pendientes (candidatas PHB 2024): Champion, Battle Master, Eldritch
Knight, Psi Warrior. Ninguna implementada; `CLASSES["fighter"].subclasses`
está vacío (test congelado en `tests/test_fighter.py`).

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

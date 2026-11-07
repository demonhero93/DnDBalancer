# TODO — DnDBalancer / dnd_sim

Revisar al principio de cada sesión. Última revisión: 2026-11-07.
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

- **Subclases Fighter**: candidatas Champion, Battle Master, Eldritch
  Knight, Psi Warrior (Arcane Archer implementado, ver plan abajo).
- **Arcane Archer — Piercing/Seeking**: fuera del pool (`ARCANE_SHOTS`
  = 6 opciones). Ambas reemplazan la tirada de ataque («instead of
  making an attack roll») y el motor no tiene ningún gancho previo a
  `attack_roll` (el primer gancho del flujo es `extra_attack_damage`,
  que exige impactar); además su geometría (línea 1 ft × 30 ft / punto
  visto) no existe sin posiciones. Implementarlas exige un gancho nuevo
  antes de la tirada + área con posición → más allá del «gancho
  mínimo». Si se retoman: hook previo a la tirada, `pick` entre
  conocidas y salvación DES.
- **Arcane Archer — Ever-Ready Shot (10)**: sin efecto, dato de tabla
  documentado en el docstring de `arcane_archer.py` (cada combate
  empieza con los usos de Arcane Shot completos).

## Arcane Archer: plan de sesión

Cada casilla = un commit. Registro tras cada paso en
PASOS-ANTERIORES.txt. NO tocar la API (reglas en el prompt de la tarea).

- [x] 1. Estructura y datos: tablas `arcane_shot_options_known` /
  `arcane_shot_uses` en `core/classes.py`; `subclasses/arcane_archer.py`
  con `ArcaneArcherFeatures` + `apply_arcane_archer` (valida clase
  fighter y nivel ≥3; Arcane Archer Lore: competencia Arcanos/Naturaleza
  con `pick` + truco dato; pool de opciones con kwarg explícito
  validado); registro `"arcane_archer"` en `fighter/__init__.py`;
  reexports (subclasses/__init__, fachada `dnd_sim/__init__.py`);
  `tests/test_arquitectura.py` si procede; tests registro/equivalencia/
  errores/tablas/Lore/pool. **Test existente que cambia (explicado)**:
  `tests/test_fighter.py` que congela tabla vacía → exige
  `{"arcane_archer"}` (el de `"champion"` sigue válido).
- [x] 2. Arcane Shot base: usos 2/3 (`arcane_shot_uses`), flag «una vez
  por turno» con reinicio en `on_turn_start` (patrón Oleada de Acción),
  decisión `pick` «no/sí» solo al impactar a distancia (cero RNG si no
  corresponde), `pick` entre opciones conocidas, gasto de uso, CD =
  8+PB+INT; primera opción: Grasping Arrow (daño 2d6 veneno puro,
  4d6 desde nivel 18).
- [x] 3. Opciones con salvación: Banishing (CAR → incapacitado con
  duración, sin inatacabilidad), Beguiling (SAB → Hechizado por aliado
  `pick`, termina si el aliado le ataca), Enfeebling (CON → marca que
  mitiga el daño de sus ataques, patrón `maestria_desventaja`), Shadow
  (SAB → solo daño + salvación, visión sin efecto `# TODO`).
- [x] 4. Bursting Arrow: 2d6 fuerza al objetivo y vecinos a 10 ft sin
  salvación, con `select_area_targets`/`AreaTargeting` (patrón
  Intimidating Presence).
- [x] 5. Magic Arrow (≥7: marca `magical` in-place en arco corto/largo
  EN/ES) + Curving Shot (bonus action re-tira contra otro enemigo
  `pick`, patrón Unstable Backlash; sin bonus libre u otro objetivo →
  sin RNG).
- [x] 6. Piercing/Seeking: implementar solo si cabe con gancho mínimo;
  si no, a «pendientes reales» con el motivo exacto y fuera del pool.
  Ever-Ready Shot: dato de tabla documentado (sin efecto en el sim).
- [x] 7. Tests de integración: `run_combat` con semilla fija, cero RNG
  sin la subclase; suite completa.
- [x] 8. Docs: `TODO.md` (candidata marcada + pendientes reales con
  motivos), `PASOS-ANTERIORES.txt` (bloque ARCANE ARCHER en ESTADO
  ACTUAL), `ARCHITECTURE.md` (fila + grafo + recuentos).
- [ ] 9. Verificación final: arquitectura, suite, `capas.py`,
  `graphify update .`; commit final del grafo.


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
Knight, Psi Warrior. Arcane Archer YA está implementado
(`CLASSES["fighter"].subclasses` = `{"arcane_archer"}`).

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

# TODO — DnDBalancer / dnd_sim

Revisar al principio de cada sesión. Última revisión: 2026-11-05.
Contexto detallado: PASOS-ANTERIORES.txt (secciones 9-13) y ARCHITECTURE.md.

## Bloque 2026-10-30 (commiteado)

- `ff30aac` feat(classes): registro de clases + Path of the Beast (20 ficheros).
- `667bc0a` docs: reglas, log de sesión y este TODO.
- `37b2806` chore(graph): grafo regenerado.
- Pendiente de push si hay remoto.

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

## Fighter: plan de sesión

Clase base Fighter (Guerrero, PHB 2024), niveles 1-20, sin subclases
(dejar estructura lista). Cada casilla = un commit (una idea).

- [x] 1. Estructura y registro: `rules/classes/fighter/` (init + features
      con salvaciones FUE+CON y skills + subclasses/ vacío),
      `FIGHTER_SKILLS` en core, fachada `dnd_sim/__init__.py`,
      test_arquitectura, test de registro y `apply_class("fighter")`.
      → tests/test_fighter.py: 7 tests; registro `fighter` con tabla de
      subclases vacía. (Pendiente log en PASOS.)
- [x] 2. Datos de nivel: `FIGHTER_FEATURES` + `fighter_extra_attacks_for`
      en `core/classes.py` (tabla 1-20 y golpes 1/2/3/4). → 2 tests.
- [x] 3. Second Wind: acción de bonus, usos 2/3/4 por nivel, cura 1d10+nivel.
      → 5 tests (curación, tope de PV, usos 2/3/4, no elegible a PG
      completos, no elegible sin usos).
- [x] 4. Action Surge: acción que restaura recurso de acción + 3ª pasada
      en `engine/combat/encounter.py` (guard: solo si se restauró).
      → 8 tests (usos 1/2, nivel 1, restaura+gasta, 1/turno, 3
      elegibilidades, integración run_combat).
- [x] 5. Extra Attack 2/3/4 (20): `pj.extra_attacks` o MultiattackAction.
      → 4 tests (multiataque 2/3/4, sin ataques, con armas, <5).
      (Commit 27d8bb2.)
- [x] 6. Indomitable: hook `after_failed_save` (patrón Fanatical Focus),
      bonificador = nivel, usos 1/2/3.
      → 7 tests (usos, ausencia <9, bono=nivel, nueva tirada manda,
      sin usos sin RNG, nivel<9 sin pick, reset). Suite 1043 passed.
      Commit 81fa1e3.
- [x] 7. Studied Attacks (13): `after_attack_roll` marca, ventaja por
      objetivo en `modify_attack_modifiers`, caduca en 2 turnos.
      → 7 tests. Suite 1050 passed. Commit 02448f9.
- [x] 8. Estilos de Combate: pick + kwarg (3d97afc infra/Defense/
      Dueling/Thrown, 3a7bf6b Archery con AttackModifiers.bonus,
      2d3746c GWF con hook damage_dice_upgrades + roll_dice floor).
      → 14 tests (fichero total 54). Suite 1064 passed.
      Protection/Interception/Blind/Unarmed/TWF = dato sin efecto
      (casilla 9).
- [x] 9. Datos sin efecto + Weapon Mastery: Tactical Mind (sin gancho
      `ability_check`: checks.py no recibe ctx → sin hook), Tactical
      Shift (sin movimiento), Tactical Master (sin infra Push/Sap/Slow),
      Weapon Mastery pick de N armas como dato (`weapon_mastery_count`
      + `trait.maestrias`), ASI/Don Épico sin efecto.
      → 5 tests. (Detalle: «Fighter: datos sin efecto» más abajo.)
- [x] 10. Plantilla "Guerrero" en `main.py`: la existente gana
      `class_name="fighter"` (commit 8605d28, 1 test → total 60).
- [x] 11. `tests/test_fighter.py` completo (+ fixture JSON de niveles).
- [x] 12. Docs: receta "cómo añadir una subclase" en este archivo,
       bloque Guerrero en PASOS-ANTERIORES.txt, ARCHITECTURE.md.
- [x] 13. Verificación final: arquitectura, suite, capas, grafo + commits.

Decisiones tomadas (detalle en PASOS-ANTERIORES.txt):
- Sin alias "guerrero": `test_clases.py` usa esa clave como clase
  desconocida (bárbaro tampoco tiene alias en español).
- Two-Weapon Fighting: dato sin efecto — el motor no tiene ataques
  bonus/off-hand que mejorar.

## Fighter: datos sin efecto

Rasgos del PHB 2024 que el simulador NO modela. Documentados aquí; si
algún día se necesitan, el punto de entrada está indicado.

- **Tactical Mind (2)**: al fallar una prueba de característica gastar 1
  uso de Tomar Aliento para sumar 1d10. Sin efecto: `checks.py`
  (`ability_check`/`skill_check`) no recibe `ctx`, no hay gancho
  `after_failed_check` y no se creó uno solo por esto. Para
  implementarlo: añadir gancho mínimo en `rules/checks.py` + entrada en
  `HOOK_NAMES` (patrón `after_failed_save`).
- **Tactical Shift (5)**: moverse al activar Tomar Aliento. Sin efecto:
  el simulador no tiene sistema de movimiento/posiciones.
- **Tactical Master (9)**: sustituir la maestría por Push/Sap/Slow.
  Sin efecto: el motor no aplica propiedades de maestría a los PJs (la
  infra `Attack.mastery` solo la usa world_tree en monstruos cargados
  con esas claves).
- **Weapon Mastery (1)**: implementado solo como DATO —
  `weapon_mastery_count` (3/4/5/6 en 1/4/10/16) + `sample` de armas del
  PJ en `trait.maestrias` (pool `weapons` o, si no, `attacks`). Efectos
  de maestría: pendientes hasta que haya motor de maestría para PJs.
- **ASI (4/6/8/12/14/16) y Don Épico (19)**: sin efecto — el modelo de
  PJ no aplica mejoras de atributo ni dones épicos.
- **Estilos sin efecto**: Protection, Interception, Blind Fighting,
  Unarmed Fighting (sin infra de reacciones/visión/sin arma) y
  Two-Weapon Fighting (ver decisión arriba).

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

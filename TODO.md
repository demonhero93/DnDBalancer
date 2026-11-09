# TODO — DnDBalancer / dnd_sim

Revisar al principio de cada sesión. Última revisión: 2026-11-09.
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

- **Subclases Fighter**: candidatas Champion, Eldritch Knight, Psi
  Warrior (Arcane Archer y Battle Master implementados, ver planes
  abajo).
- **Arcane Archer**: Piercing/Seeking implementados (2026-11-08, ver
  plan abajo y PASOS). Efectos parciales restantes (motivo en el
  docstring de `arcane_archer.py`):
  - Grasping Arrow: velocidad -10 y 2d6 al moverse → sin sistema de
    movimiento; hoy solo daño.
  - Shadow Arrow: «no ve a más de 5 pies» → sin modelo de visión;
    hoy solo daño + salvación DES.
  - Banishing Arrow: la inatacabilidad del destino no está modelada;
    hoy incapacitado 2 rondas.
  - Seeking Arrow: «aprendes la ubicación» y «sin camino → la flecha
    desaparece» → sin posiciones; daño + salvación completos.
  - Enfeebling Arrow (aproximación documentada): mitad solo de ataques
    con arma no mágicos y hasta la ronda+1 («hasta el inicio de tu
    siguiente turno»).
  - Ever-Ready Shot (10): decisión de diseño (NO deuda), congelada en
    `test_ever_ready_shot_no_cambia_los_usos_al_empezar_un_combate`:
    cada combate empieza con los usos completos. Reabrir solo si el
    sim modela más de un combate por descanso.


## Arcane Archer: Piercing y Seeking

Plan de sesión (una casilla = un commit):

- [x] A1 — Helper `daño_base_arma` en `engine/combat/attack.py`
  (extraer el cálculo del daño bruto; refactor sin cambio de
  resultados, suite verde antes de seguir).
- [x] A2 — Punto de sustitución del ataque: `sustituir_ataque` por
  duck-typing en `attack_roll` (patrón `resolver_maestria`, sin hook
  nuevo en HOOK_NAMES; tipo de retorno mínimo `AtaqueSustituido`).
- [x] A3 — Decisión única de Arcane Shot ANTES de la tirada (un solo
  `pick` «no/sí» + `pick` entre conocidas) y `ARCANE_SHOTS` con las 8
  opciones (Piercing/Seeking entran al pool; RNG de AA cambia → tests
  de `test_arcane_archer.py` explicados en PASOS antes de tocarlos).
- [x] A4 — Piercing Arrow: k con `pick` 1-3 limitado, daño del arma
  una sola vez, salvación DES por objetivo (mitad si supera).
- [x] A5 — Seeking Arrow: enemigo vivo con `pick`, daño + salvación
  DES; ubicación/alcance = dato sin efecto (`# TODO`).
- [x] B — Ever-Ready Shot como decisión de diseño (test que lo
  congela) y TODO.md solo con pendientes reales de Arcane Archer.
- [x] Docs — ARCHITECTURE.md (punto de sustitución, helper, recuentos,
  Ever-Ready) + PASOS-ANTERIORES.txt (bloque y ESTADO ACTUAL).
- [x] Verificación + grafo (`pytest` arquitectura, suite, `capas.py`,
  `graphify update .`, commit final).

## Battle Master: plan de sesión 1

- [x] A1. Tablas `superiority_dice_count` / `superiority_die_sides` /
  `maneuvers_known_count` y pool `BATTLE_MASTER_MANEUVERS` en `core/classes.py`
  + tests por nivel.
- [x] A2. Esqueleto `battle_master.py`, registro `"battle_master"` y reexportes;
  Student of War (habilidad con `pick`) y Know Your Enemy (dato); tests.
- [x] A3. Punto de decisión único por ataque (duck-typing desde `attack.py`),
  gasto de dado al ejecutar, una maniobra por ataque, Relentless; tests.
- [x] A4. Maniobras de impacto con daño y salvación (Disarming, Goading,
  Lunging, Maneuvering, Menacing, Pushing, Trip); tests.
- [x] A5. Marcas Distracting / Goading / Feinting en `CombatState`; tests.
- [x] A6. Precision Attack y Sweeping Attack; tests.
- [x] A7. Cierre de pool: Relentless, Know Your Enemy dato, Bait and Switch
  fuera si no hay CA temporal; tests.
- [x] B. Decisiones de diseño y cambio de test existente explicado (subclases
  registradas pasa a `{"arcane_archer", "battle_master"}`).
- [x] Docs. `ARCHITECTURE.md`, `PASOS-ANTERIORES.txt`, `TODO.md` (sesión 2).
- [x] Verificación. `pytest tests/test_arquitectura.py`, `pytest`,
  `python tools/capas.py`, `graphify update .` y commit final del grafo.

## Battle Master: plan de sesión 2

(una casilla = un commit; entrada en PASOS tras cada paso)

- [x] A1 — Pool y tablas: `parry`, `riposte` y `commanders_strike`
  en `BATTLE_MASTER_MANEUVERS` (11→14) + tests (pool, `sample`,
  kwarg) + reseed de los tests afectados por el cambio de `sample`
  (cada test tocado, explicado en PASOS ANTES de tocarlo).
- [x] A2 — Parry: consulta duck-typing
  `reducir_dano_recibido(target, attacker, rango, *, dmg, ctx, rng,
  log)` desde `attack.py` antes de `inflict_damage`; reduce
  `dado + max(mod FUE, mod DES)` con mínimo 0; guards (cuerpo a
  cuerpo, daño > 0, reacción libre, dado/Relentless, maniobra
  conocida); tests.
- [ ] A3 — Riposte: consulta duck-typing `reaccionar_al_fallo(...)`
  en la rama de fallo de `attack_roll`; ataque de reacción patrón
  Retaliation (`r_ctx.is_reaction`); el dado viaja en
  `ctx.dano_reaccion` y lo suma `daño_base_arma` (plano); guard de
  reentrada `is_reaction` en `decidir_maniobra`; tests.
- [ ] A4 — Commander's Strike: `sustituir_ataque` propio (guard
  `is_reaction`); pick previo «no/sí» + pick de aliado elegible y de
  su objetivo; el aliado gasta SU reacción y el dado del dueño va en
  `ctx.dano_reaccion`; sesgo documentado (docstring + ARCHITECTURE +
  TODO); tests.
- [ ] B1 — Rally: `BattleMasterRallyAction` (bonus, `usage=None`,
  elegibilidad sin RNG) y `rally` al pool (14→15, reseed explicado);
  PV temporales `dado + mod CAR` (mínimo 1) sin acumular; tests.
- [ ] B2 — Bait and Switch: re-inspección de CA temporal con
  caducidad (Defense, Shielding Storm, Protection); si no existe →
  FUERA del pool con motivo en PASOS (+ test si cambia el pool).
- [ ] Docs — `ARCHITECTURE.md` (reacciones nuevas en el motor,
  Commander's Strike y su sesgo, recuentos), `PASOS-ANTERIORES.txt`
  (bloque «BATTLE MASTER (SESIÓN 2)» + ESTADO ACTUAL), `TODO.md`
  (sesión cerrada y pendientes reales).
- [ ] Verificación — `pytest tests/test_arquitectura.py`, `pytest`,
  `python tools/capas.py`, `graphify update .` y commit final.

Fuera de esta sesión (siguen pendientes): Ambush y Commanding
Presence no tienen casilla en los bloques A/B de la tarea.

## Fighter: cómo añadir una subclase

Receta (patrón bárbaro, ver `barbarian/subclasses/`; ejemplos de
fighter: `arcane_archer.py` y `battle_master.py`):

1. Crear `rules/classes/fighter/subclasses/<clave>.py` con un
   `SubclassDef(name="<nombre visible>", class_name="fighter",
   min_level=3, apply=...)` y su rasgo (`Trait`) con los hooks
   necesarios. Si supera ~700 líneas, paquete `battle_master/` con
   reexport y ajustar `tests/test_arquitectura.py`.
2. Registrar en `rules/classes/fighter/__init__.py`: importar la
   `SubclassDef` y añadirla al dict `subclasses` del `FIGHTER_CLASS`.
3. Reexportar la API en `rules/classes/__init__.py` y en la fachada
   `dnd_sim/__init__.py` (import + `__all__`) si expone símbolos
   nuevos.
4. Tests: `tests/test_<clave>.py` en español (registro, apply por
   `apply_class("fighter", subclass_name="<clave>", level=3)`, rasgos).
   Si un test existente congela el registro de subclases del fighter,
   explicarlo ANTES de tocarlo.
5. Actualizar `ARCHITECTURE.md` (tabla de paquetes con fachada) y el
   bloque Guerrero de `PASOS-ANTERIORES.txt`.

Pendientes (candidatas PHB 2024): Champion, Eldritch Knight, Psi
Warrior. Arcane Archer y Battle Master YA están implementados
(`CLASSES["fighter"].subclasses` = `{"arcane_archer", "battle_master"}`).

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

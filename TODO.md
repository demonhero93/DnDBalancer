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

- **Subclases Fighter**: candidata Eldritch Knight (Arcane Archer,
  Battle Master, Cavalier, Champion, Psi Warrior y Rune Knight
  implementados, ver planes abajo).
- **Rune Knight**: hecho (plan abajo). Límites congelados como dato
  sin efecto en `tests/test_rune_knight.py` (velocidad, alcance,
  distancias, runas despertadas, pruebas características de Storm,
  ventaja de Hill en salvaciones de veneno): sin posiciones ni
  movimiento, ningún efecto mide distancia. Reabrir solo si existe
  sistema de movimiento/posiciones o salvaciones tipadas.
- **Psi Warrior**: hecho (plan abajo). Protective Field usa el punto
  central de `inflict_damage` (fase 1a), así que no aplica el
  «solo daño de ataques». Concentración de Telekinetic Master =
  versión simple (ver A8). Recuperación de dados por descanso corto:
  cuando existan descansos.
- **Champion**: hecho (plan abajo). Heroic Warrior y Defy Death son
  dato sin efecto: reabrir SOLO si el sim modela Inspiración Heroica
  o salvaciones de muerte, respectivamente.
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

Fuera de esta sesión (siguen pendientes): el paquete
`battle_master/` del recetario de abajo queda pendiente porque 17
tests parchean `bm_mod.pick`/`roll_dice` en el módulo único
(`battle_master.py`, 845 líneas).

## Champion: plan de sesión

(una casilla = un commit; entrada en PASOS tras cada paso)

- [x] A1 — Tablas en `core/classes.py` (`champion_crit_threshold`,
  `heroic_rally_amount`) + tests de tablas por nivel.
  **Hecho**: ambas con `_clamp`/`max(0, ...)`; 2 tests, fichero
  `tests/test_champion.py`.
- [x] A2 — Esqueleto `fighter/subclasses/champion.py`
  (`ChampionFeatures`, `apply_champion` con kwarg
  `additional_fighting_style` validado; la aplicación del estilo se
  completa en A5) + registro `"champion"` y reexportes + tests
  (registro/equivalencia, error clase/nivel, Heroic Warrior y Defy
  Death dato sin efecto, cero RNG sin subclase). Cambio esperado en
  los 4 tests que congelan/usaban el registro (explicado en PASOS
  ANTES de tocarlos).
  **Hecho**: 4 tests de registro con freeze/ejemplo tocados
  (`test_fighter` ×2, `test_arcane_archer`, `test_battle_master` —
  explicados en PASOS (2)); 7 tests nuevos, suite 1396 passed.
- [x] A3 — Rango crítico ampliado: refactor previo (helper
  `evaluar_d20`/`umbral_critico` en `rules/roll_modifiers.py`, suite
  idéntica ANTES de seguir) + umbral por atacante duck-typing
  (`ChampionFeatures.umbral_critico`, campo `spell_attack` para no
  afectar a hechizos) + verificación de consumidores (Precision,
  Warding, Sweeping, Studied, reacciones) + tests.
  **Hecho**: refactor verde 1396 antes del umbral; campo nuevo
  `spell_attack` en `model/attack.py` + `casting.py`; 9 tests,
  suite 1405 passed.
- [x] A4 — Remarkable Athlete: ventaja en iniciativa
  (`ventaja_iniciativa()` duck-typing en `roll_initiative`, solo
  Champion consume RNG nuevo) + ventaja en Atletismo
  (`modify_check_modifiers`, patrón Furia) + movimiento tras crítico
  `# TODO` dato sin efecto + tests.
  **Hecho**: recuento de fuentes con `desventaja_iniciativa()`
  (anulación estándar); `# TODO` en `umbral_critico`; 10 tests,
  suite 1415 passed.
- [x] A5 — Additional Fighting Style: generalizar `FighterFeatures` a
  propiedad `estilos` (sin romper `estilo` ni `fighting_style`),
  refactor con suite verde, `apply_champion` elige con `pick`/kwarg y
  aplica mutaciones (Defense) + tests.
  **Hecho**: refactor 1415 idéntico; `estilos_extra` + `estilos`;
  6 hooks por membresía; gate nivel ≥7; 9 tests, suite 1424 passed.
- [x] A6 — Heroic Rally: `on_turn_start` (patrón Life-Giving Force),
  Bloodied `pg * 2 <= pg_max`, `heroic_rally_amount` recortado a los
  PG máximos, sin RNG + tests.
  **Hecho**: guards nivel ≥18/dueño/vivo/≥1 PG/Bloodied; cura
  `min(amount, pg_max - pg)` con `log_line`; 8 tests,
  suite 1432 passed.
- [x] B — Decisiones de diseño: 3 tests de freeze de registro
  explicados ANTES; límites con test freeze (Heroic Warrior, Defy
  Death, movimiento tras crítico); `TODO.md` con Champion hecha y
  pendientes reales (Eldritch Knight, Psi Warrior, condiciones de
  reabrir Heroic Warrior/Defy Death).
  **Hecho**: freeze ya en A2/A4; `TODO.md` candidatas y condiciones
  de reabrir actualizados. Commit de B.
- [x] Docs — `ARCHITECTURE.md` (fila `rules/classes/`, helper de
  crítico por umbral, soporte de ventaja en iniciativa/pruebas,
  recuentos), `PASOS-ANTERIORES.txt` (bloque CHAMPION + ESTADO
  ACTUAL), `TODO.md` (receta y pendientes).
  **Hecho**: tabla remediada (85/20584, tests 55/22585/1432), sección
  `## Champion (PHB 2024)`, nota iniciativa en Ambush, ESTADO ACTUAL
  + bullet Champion, candidatas actualizadas. Commit de Docs.
- [x] Verificación — `pytest tests/test_arquitectura.py`, `pytest`,
  `python tools/capas.py`, `graphify update .` + commit final con el
  grafo.
  **Hecho**: 3 + 1432 passed; capas total 1 (excepción conocida);
  grafo 4087/14882/123. FIN sesión Champion.

## Psi Warrior: plan de sesión

(una casilla = un commit; entrada en PASOS tras cada paso)

- [x] A1 — Tablas en `core/classes.py` (`psionic_dice_count`,
  `psionic_die_sides`, `bulwark_targets`) + tests de tablas por nivel.
  **Hecho**: PB local `2 + (lvl - 1) // 4` en core; 3 tests, fichero
  `tests/test_psi_warrior.py`.
- [x] A2 — Esqueleto `fighter/subclasses/psi_warrior.py`
  (`PsiWarriorFeatures` con dados, usos gratuitos, flags por turno y
  estado de Bulwark/Telekinetic Master; `apply_psi_warrior`) +
  registro `"psi_warrior"` y reexportes + tests (registro/
  equivalencia, error clase/nivel, dados por nivel, Telekinetic
  Movement y Psi-Powered Leap dato sin efecto, cero RNG sin
  subclase). Cambio esperado en los 4 tests de freeze de registro
  (explicado en PASOS ANTES de tocarlos).
  **Hecho**: `psi_warrior.py` con `reset`/`on_turn_start`; sin
  `_RNG_CREACION` (no hay elección al crear; documentado en PASOS
  (2)); 8 tests + 3 A1, suite 1443 passed.
- [x] A3 — Psionic Strike: opción de impacto tras acertar y causar
  daño (duck-typing desde `attack.py`, patrón Arcane Shot/maniobras),
  `pick` «no»/«sí», dado tirado una vez, daño de fuerza = dado + mod
  INT con `apply_damage_modifiers`, flag por turno + tests.
  **Hecho**: walker `_dano_extra_de_rasgo` tras el daño principal;
  9 tests, suite 1452 passed.
- [x] A4 — Telekinetic Thrust: salvación FUE CD `8+PB+mod INT` al
  aplicarse Psionic Strike con nivel >= 7, fallo → PRONE con
  EscapeCheck de Topple + tests.
  **Hecho**: `_telekinetic_thrust` tras gastar el dado; 4 tests,
  suite 1456 passed.
- [x] A5 — Protective Field (paso delicado, aislado): punto central
  de daño o punto Parry/Warding, guards de la sección 1, reducción
  `max(1, dado + mod INT)`, reacción compartida + tests. Suite
  completa en verde ANTES de seguir (Parry/Warding/Interception/
  Protection sin cambios).
  **Hecho**: walker `_proteccion_psionica` en fase 1a de
  `inflict_damage` (todos los combatientes incluido el target); 8
  tests, suite 1464 passed.
- [x] A6 — Guarded Mind: resistencia psíquica permanente (patrón
  Storm Soul) + purga Hechizado/Asustado en `on_turn_start` (patrón
  Mindless Rage) con `pick` + tests.
  **Hecho**: resistencia en `apply_psi_warrior` + `_guarded_mind`
  (nivel 10, corregido en fix A6); 8 tests, suite 1472 passed.
- [x] A7 — Bulwark of Force: `PsiBulwarkAction` (acción adicional,
  `usage=None`), cobertura reutilizada o bonificador temporal
  documentado, uso gratuito primero y luego dado, validez dinámica
  + tests.
  **Hecho**: campo `cobertura_bulwark` + `cobertura_bulwark_activa` +
  rama en `effective_ac`/`saving_throw` (DES); 10 tests, suite 1482
  passed.
- [x] A8 — Telekinetic Master: `TelekineticMasterAction` +
  `TelekineticMasterAttackAction` (helper de ataque adicional
  existente), concentración reutilizada o simple + tests con
  integración `run_combat` semilla fija.
  **Hecho**: versión simple de concentración (flag mientras el dueño
  no esté Incapacitado ni muerto, SIN salvaciones de CON: sin
  mecánica de ruptura reutilizable — «concentración parcial» queda
  como pendiente real en B); 11 tests, suite 1493 passed.
- [x] B — Decisiones: 4 tests de freeze de registro explicados
  ANTES; límites con test freeze (movimiento, empuje, 30 ft,
  Telekinesis); `TODO.md` con Psi Warrior hecha y pendientes
  reales (Eldritch Knight, concentración parcial, descansos).
  **Hecho**: corrección Protective Field (gate nivel 3 + guard de
  aliado; 5 tests reescritos + 3 de deuda), 3 tests de límites,
  candidatas y pendientes actualizados; suite 1499 passed.
- [x] Docs — `ARCHITECTURE.md` (fila `rules/classes/`, grafo acíclico
  `fighter.features ← fighter.subclasses`, puntos de consulta del
  motor, recuentos), `PASOS-ANTERIORES.txt` (bloque PSI WARRIOR +
  ESTADO ACTUAL), `TODO.md` (receta y pendientes).
  **Hecho**: sección `## Psi Warrior (PHB 2024)`, recuentos
  86/21276 + 56/23617/1499, ESTADO ACTUAL y receta; grafo ya
  documentado. Commit de Docs.
- [x] Verificación — `pytest tests/test_arquitectura.py`, `pytest`,
  `python tools/capas.py`, `graphify update .` + commit final con el
  grafo.
  **Hecho**: 3 passed, 1499 passed, capas total 1 (excepción
  conocida), grafo 4262/15557/136. Commit final con el grafo.

## Rune Knight: plan de sesión

Pasos (una casilla = un commit; tras cada uno, entrada en
`PASOS-ANTERIORES.txt` y suite completa):

- [x] A1 — Tablas en `core/classes.py`: `runes_known_count`,
  `giants_might_die_sides`, `rune_uses`, `runic_shield_uses`,
  `giants_might_uses`, pool `RUNES` + tests por nivel.
  **Hecho**: 6 funciones + `RUNES` en `__all__`; 6 tests, suite
  1505 passed.
- [x] A2 — Esqueleto `rune_knight.py` + registro `rune_knight` en los
  4 puntos + tests (registro, apply, kwargs, pasivos sin efecto).
  **Hecho**: esqueleto y registro: `rune_knight.py`
  (`RuneKnightFeatures` + `apply_rune_knight`, kwarg `runes`
  validado) y clave `"rune_knight"` en los 4 puntos de registro.
  **Hecho**: 3 freeze tests de registro ampliados (explicados en
  PASOS); 8 tests, suite 1513 passed.
- [x] A3 — Consulta perezosa `modificar_salvacion`/`modificar_prueba`
  (duck-typing, sin HOOK_NAMES) + tests de RNG idéntico.
  **Hecho**: en `roll_modifiers` con `fusionar_modo`; complementa (no
  sustituye) los hooks existentes (decisión en PASOS); `skill_check`
  pasa la característica efectiva; 9 tests, suite 1522 passed.
- [x] A4 — `GiantsMightAction` (acción adicional, tamaño, ventaja
  FUE, daño extra 1d6/d8/d10) + tests.
  **Hecho**: campo `giants_might_activo` + acción + consulta A3 +
  `extra_attack_damage`; 9 tests, suite 1531 passed.
- [x] A5 — Runic Shield (reacción en el punto de Warding, re-tirada
  de UN d20) + tests.
  **Hecho**: walker `_repetir_d20_del_bando` + método `repetir_d20`;
  10 tests, suite 1541 passed.
- [x] A6 — Ganchos `on_any_turn_start`/`on_any_turn_end` en Trait +
  encounter + test_traits + cuenta de hooks + tests.
  **Hecho**: 28 hooks en `HOOK_NAMES`, helper en `encounter.py`,
  4 tests, suite 1545 passed.
- [x] A7 — Runas Hill y Frost (`RuneInvokeAction`) + tests.
  **Hecho**: acción por runa (solo frost/hill en apply), Frost +2
  FUE/CON vía consulta A3, Hill B/P/C con lista de fuente propia +
  pasiva de veneno; ventaja de Hill en salvaciones de veneno = dato
  sin efecto (el motor no distingue salvación contra veneno; ver
  pendientes reales). 7 tests, suite 1552 passed.
- [x] A8 — Fire Rune (marca en CombatState, Restringido, 2d6) + tests.
  **Hecho**: en `extra_attack_damage` (daño `2d6` fuego aparte +
  salvación FUE 8+PB+CON); `fire_runa`/`fire_runa_hasta` en
  `CombatState`, RESTRAINED sin escape, ganchos de turno; 10 tests,
  suite 1562 passed.
- [x] A9 — Stone Rune (`on_any_turn_end`, Hechizado+Incapacitado) +
  tests.
  **Hecho**: dispatchers fire/stone + `_cd_runa`; 10 tests, suite
  1572 passed.
- [x] A10 — Storm Rune (acción + reacción ventaja/desventaja por
  alianza) + tests.
  **Hecho**: `RuneInvokeAction` ampliada a storm + hook
  `grant_attack_modifiers` (dirección por `is_hostile_to`, pick de
  reacción patrón Protección); 9 tests, suite 1581 passed.
- [x] A11 — Cloud Rune (redirección en el punto de Warding) + tests.
  **Hecho**: walker `_redirigir_del_bando` + `redirigir_ataque` (CA
  recalculada contra el nuevo objetivo); 9 tests, suite 1590 passed.
- [x] A12 — Master of Runes (2 usos) + tests de cierre.
  **Hecho**: efectos ya en tablas A1 (`rune_uses` 2 en 15+,
  `runes_known_count` 5 en 15+); 4 tests de cierre (frontera 14/15,
  3 invocaciones, Stone doble uso, integración `run_combat` semilla
  fija), suite 1594 passed.
- [x] B — Decisiones: test de registro explicado ANTES; límites con
  test freeze; TODO con Rune Knight hecha y pendientes reales.
  **Hecho**: registro ya explicado en PASOS (2) antes de tocarlo
  (A2); 5 tests freeze de límites (velocidad/alcance, distancias,
  pruebas Storm, runas despertadas, ventaja Hill en salvaciones de
  veneno); pendientes reales abajo. Suite 1599 passed.
- [ ] Docs — `ARCHITECTURE.md` (fila, hooks N, consulta, recuentos),
  PASOS (bloque RUNE KNIGHT + ESTADO ACTUAL), TODO (receta).
- [ ] Verificación — arquitectura + suite + capas + graphify +
  commit final con grafo.

## Fighter: cómo añadir una subclase

Receta (patrón bárbaro, ver `barbarian/subclasses/`; ejemplos de
fighter: `arcane_archer.py`, `battle_master.py`, `cavalier.py`,
`champion.py` y `psi_warrior.py`):

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

Pendientes (candidata PHB 2024): Eldritch Knight.
Arcane Archer, Battle Master, Cavalier, Champion, Psi Warrior y
Rune Knight YA están implementados (`CLASSES["fighter"].subclasses`
tiene sus 6 claves).

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

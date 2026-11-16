# TODO — DnDBalancer / dnd_sim

Revisar al principio de cada sesión. Última revisión: 2026-11-14.
Solo tareas SIN implementar. Lo ya hecho: PASOS-ANTERIORES.txt
(bloque 15 «Clase Fighter», bloque «CIERRE DE PENDIENTES DEL FIGHTER»)
y ARCHITECTURE.md.

## Samurai: plan de sesión

Una casilla = un commit. Registro en `PASOS-ANTERIORES.txt` tras cada
casilla. Enunciado completo en el mensaje de tarea de la sesión.

- [x] A1 — Tablas en `core/classes.py`: `fighting_spirit_uses`,
  `fighting_spirit_temp_hp`, `SAMURAI_BONUS_SKILLS` + tests por nivel.
  **Hecho**: 3 tests, suite 1602 passed.
- [x] A2 — Esqueleto `samurai.py` (`SamuraiFeatures` + `apply_samurai`),
  registro `"samurai"` en `fighter/__init__.py` + reexports + fachada;
  cambio explicado del test freeze de subclases de `test_fighter.py`.
  **Hecho**: 11 tests; en realidad el registro lo congelan 3 tests
  (`test_fighter`, `test_arcane_archer`, `test_battle_master`), los
  tres tocados con el patrón «Cambio esperado». Suite: 1613 passed.
- [ ] A3 — Fighting Spirit: activación previa en `on_turn_start`
  (decisión con `pick`; el motor no tiene punto previo a la acción),
  gasto de la acción adicional en `ctx.resources`, PV temporales sin
  acumulación y ventaja en `modify_attack_modifiers` solo con arma.
  **Hecho**: 10 tests, suite 1623 passed.
- [ ] A4 — Rapid Strike: consulta duck-typing `renunciar_ventaja` en
  `engine/combat/attack.py` tras el modo de ventaja y antes del d20;
  ataque adicional al final de `attack_roll`.
  **Hecho**: 6 tests, suite 1629 passed.
- [x] A5 — Función de turno reutilizable en `encounter.py` (extraída
  del bucle de rondas; cero cambio de RNG; suite idéntica).
  **Hecho**: `_turno(actor) -> bool`; snapshot de equivalencia semilla
  42 en `tests/test_samurai.py`. Suite: 1630 passed.
- [x] A6 — Strength Before Death: campos `en_pie_pendiente` y cola de
  turnos extra, predicado «en pie» (`alive`), dispara en `inflict_damage`
  y cola procesada al final de cada turno con la función de A5.
  **Hecho**: 6 tests; `_procesar_turnos_extra` al final de `_turno`
  antes de guarida. Suite: 1636 passed.
- [x] B — Decisiones: freeze de datos sin efecto (idioma, bonificador
  social, Tireless Spirit, salvaciones de muerte), reinterpretación del
  turno extra diferido en docstrings, lista de candidatas en TODO.
  **Hecho**: 2 tests nuevos (idioma, salvaciones de muerte) + 2
  existentes; docstring SBD diferido en A6; TODO 7/8 + bloque de
  congelación. Suite: 1638 passed.
- [x] Docs — `ARCHITECTURE.md` (fila `rules/classes/`, función de turno,
  estado en pie pendiente, recuentos), bloque SAMURAI en
  `PASOS-ANTERIORES.txt`, receta y pendientes de `TODO.md`.
  **Hecho**: sección Samurai (XGE) + recuentos 88/22924 y 1638 tests;
  entradas (A1)-(B) y (Docs) en PASOS. Suite: 1638 passed.
- [x] Verificación final — `pytest tests/test_arquitectura.py` +
  `pytest` + `python tools/capas.py` + `graphify update .` + commit
  con el grafo.
  **Hecho**: 3 + 1638 passed; capas solo la excepción única; grafo
  4639 nodos / 16949 aristas / 175 comunidades.

## Hechizos de PJ: plan de sesión 1

Una casilla = un commit. Registro en `PASOS-ANTERIORES.txt` tras cada
casilla. Enunciado completo en el mensaje de tarea de la sesión. NO se
añade ninguna clase lanzadora real (el Eldritch Knight va en la sesión
siguiente); la clase de tests es falsa.

- [x] A1 — Tablas de espacios (full/half/third 2024),
  `spell_slots_for(progresion, nivel)` y `SpellcastingDef` en módulo
  nuevo `core/spellcasting.py` + tests por nivel y límites.
  **Hecho**: 7 tests, suite 1645 passed.
- [x] A2 — `SpellSlots` (dataclass core: max/actuales, `can_cast`,
  `niveles_disponibles`, `spend`, `reset`) + campo opcional en
  `Combatant` (None por defecto) restaurado en `reset` + tests.
  **Hecho**: 6 tests, suite 1651 passed.
- [ ] A3 — Cargador de listas de clase en `data/` (`/classes/<index>/spells`
  con caché en disco y fixture JSON) devolviendo `ClassSpellList`
  (tipo definido en `rules/spells`, recibido como argumento) + tests
  sin red.
- [ ] A4 — `rules/spells`: `hechizo_soportado`, `PCSpellcasting`
  (CD/bonificador = PB + mod) y acción de hechizo de PJ con gasto de
  espacio y `pick` de sobrecarga; suite completa idéntica antes de
  seguir (monstruos intactos).
- [ ] A5 — `preparar_hechizos(...)` con `sample` uniforme del pool
  soportado y legal, kwargs explícitos validados (`ValueError`), rng
  semilla 0 por defecto + tests.
- [ ] A6 — `ClassDef`/`SubclassDef` con `spellcasting: SpellcastingDef |
  None`, helper `aplicar_lanzamiento`, clase falsa SOLO de test (no
  registrada en producción) e integración en `run_combat`.
- [ ] A7 — La acción extra de Oleada de Acción no puede lanzar hechizo
  (marca `es_accion_magia`; mínima cambio en la tercera pasada) +
  anular la nota «la acción Magia no existe».
- [ ] A8 — Estadísticas: hechizos de PJ en `action_uses` sin cambiar
  formato; «espacios gastados» si es barato, si no a pendientes.
- [ ] B — Límites del modelo documentados (rituales, utilidad, buffs,
  reacciones de hechizo, Pact Magic, componentes, distancias...) en
  `ARCHITECTURE.md` + «Hechizos de PJ: pendientes reales» y receta
  «Cómo añadir una clase lanzadora» en `TODO.md`.
- [ ] Docs — `ARCHITECTURE.md` (módulos nuevos, borde
  `rules/classes → rules/spells`, recuentos), bloque
  «HECHIZOS DE PJ (sesión 1)» en `PASOS-ANTERIORES.txt`.
- [ ] Verificación final — `pytest tests/test_arquitectura.py` +
  `pytest` + `python tools/capas.py` + `graphify update .` + commit
  con el grafo.

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

- **Subclase pendiente**: Eldritch Knight (candidata PHB 2024). Las
  otras 7 YA están implementadas: Arcane Archer, Battle Master,
  Cavalier, Champion, Psi Warrior, Rune Knight y Samurai
  (`CLASSES["fighter"].subclasses` tiene sus 7 claves).
- **Samurai — datos sin efecto congelados** (reabrir SOLO si el sim
  modela la mecánica; tests en `tests/test_samurai.py`):
  - Bonus Proficiency: el idioma alternativo (sin modelo de idiomas).
  - Elegant Courtier: bonificador igual al mod SAB en
    Perspicacia/Persuasión (sin pruebas sociales en combate).
  - Tireless Spirit: recuperar 1 uso de Fighting Spirit al tirar
    iniciativa (cada combate empieza con usos completos, criterio
    Ever-Ready Shot).
  - Strength Before Death: salvaciones de muerte (SBD difiere el
    turno extra; reabrir SOLO si existan salvaciones de muerte).
- **Paquete `battle_master/`**: `battle_master.py` tiene 845 líneas
  (la receta pide paquete por encima de ~700); pospuesto porque 17
  tests parchean `bm_mod.pick`/`roll_dice` apuntando al módulo único.
- **Maestrías sin efecto** (`rules/mastery.py`): Cleave (segundo
  objetivo adyacente) y Nick (ataque ligero extra) pendientes; Push y
  Slow son `EFECTOS_SIN_EFECTO` con `# TODO` (sin sistema de
  movimiento).
- **Two-Weapon Fighting**: dato sin efecto hasta que exista el ataque
  adicional (docstring de `fighter/features.py`).
- **Arcane Archer — efectos parciales** (motivo en el docstring de
  `arcane_archer.py`):
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
- **Psi Warrior**: Protective Field usa el punto central de
  `inflict_damage` (fase 1a), así que no aplica el «solo daño de
  ataques». Concentración de Telekinetic Master = versión simple (sin
  salvaciones de CON, ver PASOS casilla A8). Recuperación de dados por
  descanso corto: cuando existan descansos.
- **Champion**: Heroic Warrior y Defy Death son dato sin efecto:
  reabrir SOLO si el sim modela Inspiración Heroica o salvaciones de
  muerte, respectivamente.
- **Rune Knight**: límites congelados como dato sin efecto en
  `tests/test_rune_knight.py` (velocidad, alcance, distancias, runas
  despertadas, pruebas características de Storm, ventaja de Hill en
  salvaciones de veneno): sin posiciones ni movimiento, ningún efecto
  mide distancia. Reabrir solo si existe sistema de movimiento/
  posiciones o salvaciones tipadas.

## Fighter: cómo añadir una subclase

Receta (patrón bárbaro, ver `barbarian/subclasses/`; ejemplos de
fighter: `arcane_archer.py`, `battle_master.py`, `cavalier.py`,
`champion.py`, `psi_warrior.py`, `rune_knight.py` y `samurai.py`):

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

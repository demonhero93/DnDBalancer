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
- [ ] A5 — Función de turno reutilizable en `encounter.py` (extraída
  del bucle de rondas; cero cambio de RNG; suite idéntica).
- [ ] A6 — Strength Before Death: campos `en_pie_pendiente` y cola de
  turnos extra, predicado «en pie» (`alive`), dispara en `inflict_damage`
  y cola procesada al final de cada turno con la función de A5.
- [ ] B — Decisiones: freeze de datos sin efecto (idioma, bonificador
  social, Tireless Spirit, salvaciones de muerte), reinterpretación del
  turno extra diferido en docstrings, lista de candidatas en TODO.
- [ ] Docs — `ARCHITECTURE.md` (fila `rules/classes/`, función de turno,
  estado en pie pendiente, recuentos), bloque SAMURAI en
  `PASOS-ANTERIORES.txt`, receta y pendientes de `TODO.md`.
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
  otras 6 YA están implementadas: Arcane Archer, Battle Master,
  Cavalier, Champion, Psi Warrior y Rune Knight
  (`CLASSES["fighter"].subclasses` tiene sus 6 claves).
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
`champion.py`, `psi_warrior.py` y `rune_knight.py`):

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

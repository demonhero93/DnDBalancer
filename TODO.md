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
- [x] A3 — Cargador de listas de clase en `data/` (`/classes/<index>/spells`
  con caché en disco y fixture JSON) devolviendo `ClassSpellList`
  (tipo definido en `rules/spells`, recibido como argumento) + tests
  sin red.
  **Hecho**: 3 tests, suite 1654 passed.
- [x] A4 — `rules/spells`: `hechizo_soportado`, `PCSpellcasting`
  (CD/bonificador = PB + mod) y acción de hechizo de PJ con gasto de
  espacio y `pick` de sobrecarga; suite completa idéntica antes de
  seguir (monstruos intactos).
  **Hecho**: `preparation.py` + `caster.py`, concentración completada
  (no existía: salvación de CON al daño, Incapacitado, muerte), 12
  tests, suite 1666 passed.
- [x] A5 — `preparar_hechizos(...)` con `sample` uniforme del pool
  soportado y legal, kwargs explícitos validados (`ValueError`), rng
  semilla 0 por defecto + tests.
  **Hecho**: 11 tests, suite 1677 passed.
- [x] A6 — `ClassDef`/`SubclassDef` con `spellcasting: SpellcastingDef |
  None`, helper `aplicar_lanzamiento`, clase falsa SOLO de test (no
  registrada en producción) e integración en `run_combat`.
  **Hecho**: 3 tests, suite 1680 passed.
- [x] A7 — La acción extra de Oleada de Acción no puede lanzar hechizo
  (marca `es_accion_magia`; mínima cambio en la tercera pasada) +
  anular la nota «la acción Magia no existe».
  **Hecho**: filtro `permitir_magia=False` en la pasada extra, nota
  revocada, 2 tests, suite 1682 passed.
- [x] A8 — Estadísticas: hechizos de PJ en `action_uses` sin cambiar
  formato; «espacios gastados» si es barato, si no a pendientes.
  **Hecho**: solo test para `action_uses` (ya funcionaba); campo
  `spell_slots_spent` en `CombatResult`, suite 1683 passed.
- [x] B — Límites del modelo documentados (rituales, utilidad, buffs,
  reacciones de hechizo, Pact Magic, componentes, distancias...) en
  `ARCHITECTURE.md` + «Hechizos de PJ: pendientes reales» y receta
  «Cómo añadir una clase lanzadora» en `TODO.md`.
  **Hecho**: sección «Hechizos de PJ (PHB 2024)» en ARCHITECTURE
  (módulos, borde, límites) + los dos bloques en TODO.md.
- [x] Docs — `ARCHITECTURE.md` (módulos nuevos, borde
  `rules/classes → rules/spells`, recuentos), bloque
  «HECHIZOS DE PJ (sesión 1)» en `PASOS-ANTERIORES.txt`.
  **Hecho**: sección nueva + tabla de recuentos actualizada (92
  módulos / 23683 líneas / 1683 tests); el bloque de PASOS se fue
  escribiendo paso a paso (A1-A8) y ESTADO ACTUAL queda actualizado.
- [x] Verificación final — `pytest tests/test_arquitectura.py` +
  `pytest` + `python tools/capas.py` + `graphify update .` + commit
  con el grafo.
  **Hecho**: 3 + 1683 en verde, capas total 1 (solo la excepción
  conocida), grafo regenerado (4782 nodos / 17478 aristas).

## Eldritch Knight: plan de sesión

Añadir SOLO la subclase Eldritch Knight (Caballero Sobrenatural, PHB
2024) al Guerrero sobre la mecánica común de hechizos ya existente.
Una casilla = un commit. Rasgos: 3 Spellcasting (INT, lista wizard,
tercio) + War Bond (dato sin efecto); 7 War Magic (sustituir UN ataque
de la acción Atacar por un truco); 10 Eldritch Strike (+1 truco,
marca de desventaja en salvación del siguiente hechizo); 15 Arcane
Charge (dato sin efecto); 18 Improved War Magic (sustituir DOS
ataques por un hechizo nivel 1-2).

- [x] A1 — Tablas en `core/classes.py`: `eldritch_knight_prepared(level)`
  (0 en <3; 3:3 4:4 5:4 6:4 7:5 8:6 9:6 10:7 11:8 12:8 13:9 14:10
  15:10 16:11 17:11 18:11 19:12 20:13) y `eldritch_knight_cantrips(level)`
  (0 / 2 / 3 en <3 / 3-9 / 10+) + tests por nivel y límites.
  **Hecho**: 3 tests, suite 1686 passed.
- [ ] A2 — Esqueleto y registro: `fighter/subclasses/eldritch_knight.py`
  (`EldritchKnightFeatures`, `apply_eldritch_knight` valida fighter y
  nivel >= 3, kwargs `cantrips`/`spells` validados, rng semilla 0,
  recibe `ClassSpellList` y llama `aplicar_lanzamiento`), `SpellcastingDef`
  (tercio, INT, wizard, tablas A1, escuelas None, min 3), clave
  `"eldritch_knight"` en `fighter/__init__.py` + reexports (subclasses,
  rules/classes, fachada) + `test_arquitectura` si congela. Registro,
  equivalencia `apply_class`, errores (clase distinta, nivel <3),
  espacios/conteos (3: 2 espacios/3 preparados; 7: 4+2; 19: 4/3/3/1),
  kwargs inválidos → ValueError, War Bond y Arcane Charge congelados
  como dato sin efecto, cero RNG sin la subclase.
- [ ] A3 — Lanzamiento extremo a extremo: EK nivel 3 y 10 con
  `run_combat` + fixtures (truco de ataque, truco de salvación, hechizo
  nivel 1 con `damage_at_slot_level`, hechizo de concentración);
  sobrecarga, concentración, CD/ataque INT; Oleada NO lanza hechizos
  con un EK real.
- [ ] A4 — War Magic (PASO DELICADO): inspeccionar cadena de ataques
  (extra_attacks/MultiattackAction), punto de consulta perezoso
  duck-typing p. ej. `sustituir_ataque_por_hechizo(restantes, ctx)`
  antes de cada ataque de la acción Atacar (sin entrada en HOOK_NAMES),
  distinguido de reacciones/adicionales con `ctx.in_attack_action` /
  `ctx.is_reaction` (patrón Rapid Strike); `pick` no/sí solo si
  elegible (nivel >=7, trucos soportados, en acción Atacar); si sí,
  `pick` uniforme entre trucos y lanza en vez de ese ataque (consume
  ese ataque, sin RNG con una sola opción). Suite completa idéntica
  ANTES de seguir. Tests: sustituye y no hace el ataque con arma, sin
  trucos → sin RNG (rng que revienta), nivel 6 no actúa, no en
  reacciones ni adicionales, consume un solo ataque, truco usa CD y
  escalado del PJ, sin subclase cero RNG.
- [ ] A5 — Improved War Magic: opción «hechizo nivel 1-2 por DOS
  ataques» en el mismo punto de consulta; decisión conjunta con War
  Magic en un solo `pick` sobre las opciones elegibles (no / truco por
  un ataque / hechizo por dos) para equiprobabilidad; espacio con
  sobrecarga común. Tests: elegible con >=2 ataques restantes, consume
  dos, nivel 3+ no se ofrece, pick único espía cuando coexisten, sin
  espacios no elegible, nivel 17 no actúa.
- [ ] A6 — Eldritch Strike: marca por objetivo con caducidad (patrón
  Vex, `after_attack_roll`) solo con ataque con arma (no fallo, no
  ataque de hechizo), desventaja en la siguiente salvación del marcado
  contra hechizo del dueño vía `modificar_salvacion` (Rune Knight,
  sin duplicar mecanismo), se consume al concederla, caduca al final
  del siguiente turno del dueño, por objetivo, nivel 9 no actúa, truco
  de ataque de hechizo no la consume, sin subclase cero RNG.
- [ ] A7 — Plantilla/CLI «Caballero Sobrenatural» en `main.py` si es
  barato (class_name="fighter", subclass="eldritch_knight", cargador
  con caché); si exige red → TODO.
- [ ] B — Tests de registro congelado (`test_fighter.py`,
  `test_arcane_archer.py`, `test_battle_master.py`, patrón «Cambio
  esperado»): añadir `"eldritch_knight"` — EXPLICAR ANTES de tocar.
  Ningún otro test existente cambia. Límites: War Bond, Arcane Charge,
  distancias, reacciones de hechizo, rituales/utilidad. Decisiones del
  maintainer a anotar: tabla de preparados, ausencia de restricción de
  escuelas (dónde reactivar evocación/abjuración), versión 2024 de
  War Magic. TODO.md: marcar EK como hecha en la lista de candidatas.
- [ ] Docs — `ARCHITECTURE.md` (fila `rules/classes/`, punto de
  consulta de sustitución, recuentos), bloque «ELDRITCH KNIGHT» en
  `PASOS-ANTERIORES.txt`, receta y pendientes en `TODO.md`.
- [ ] Verificación final — `pytest tests/test_arquitectura.py` +
  `pytest` + `python tools/capas.py` (solo excepción conocida) +
  `graphify update .` + commit final con el grafo.

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

## Hechizos de PJ: pendientes reales

Límites del modelo actual (NO son deuda: cada uno se cierra aquí con
motivo y dependencia):

- **Rituales** (`ritual: true`): el parser los marca `ignored` (10 min
  de canalización no modelados). Dependencia: decidir si un ritual
  cuenta como acción o como tiempo fuera de combate.
- **Utilidad sin efecto de combate** (Jump, Mage Hand, Detect Magic...):
  `ignored` porque no alteran PV/CA/condiciones. Dependencia: modelo
  de objetos y movimiento (fuera de alcance de la sesión).
- **Buffs sin efecto modelable** (Invisibility: «ilusión sin estado en
  el rival»): ídem, mismo motivo y dependencia.
- **Reacciones de hechizo** (Shield, Absorb Elements, Counterspell):
  `action_type != ACTION` → fuera del pool. Dependencia: decidir cómo
  encaja una reacción de PJ en el helper de reacción del encuentro
  (hoy pensado para monstruos) y el gasto de espacio en turno ajeno.
- **Acción bonus** (Healing Word, Misty Step): antes de admitirlas hay
  que modelar la regla PHB «tras una acción bonus no queda otra
  acción de nivel ≥ 1 en el turno» (apuntada en el plan; si no es
  barato, se queda aquí).
- **Pact Magic (Brujo)**: progresión propia de espacios distinta de
  las tres tablas; `spell_slots_for` lanza `ValueError` a propósito.
  Dependencia: tabla + tests del brujo (sesión aparte).
- **Preparar/cambiar hechizos entre combates**: `preparar_hechizos`
  fija las listas al crear el PJ (diseño: «un combate = un día»).
  Cambiarlas entre combates requiere decisión de API.
- **Componentes y materiales**: sin coste de componentes ni foco.
- **Recuperación de espacios en medio de la jornada**: `reset()` solo
  restaura al empezar el combate; descansos cortos/largos entre
  combates no existen aún.
- **Distancias/rango**: sin posición ni distancia (fuera de alcance):
  los hechizos se resuelven sin comprobar rango.
- **`stats.py`**: `spell_slots_spent` (de `CombatResult`) no se agrega
  todavía en `run_many`; si hace falta, es el mismo patrón de
  `action_uses` (~4 líneas).

## Hechizos de PJ: cómo añadir una clase lanzadora

Receta (patrón del mago de test de `tests/test_hechizos_pj.py`):

1. Declarar la `SpellcastingDef` en `core/spellcasting.py`:
   progresión (full/half/third), característica, `trucos_conocidos` y
   `preparados` por nivel, `min_level`, `escuelas` si la clase las
   restringe.
2. Poner `spellcasting=` en el `ClassDef` de la clase (o en la
   `SubclassDef`, p. ej. Eldritch Knight): el campo ya existe con
   default `None`.
3. En el `apply` correspondiente, llamar
   `aplicar_lanzamiento(pj, nivel, def, lista_clase, *, rng, trucos,
   hechizos)` (`rules/spells/caster.py`): crea `PCSpellcasting`
   (CD/ataque del propio PJ), pone `pj.spell_slots` (lo restaura
   `reset()`), prepara con `preparar_hechizos` (o kwargs explícitos
   validados) y añade una `PJSpellAction` por hechizo a `pj.actions`.
4. Cargar la lista desde la capa `data` (la llama quien compone el
   PJ, nunca `rules`):
   `load_class_spell_list("<index>", ..., spellcasting=estadisticas_lanzador(pj,
   def.caracteristica, nivel))` — los trucos escalan al parsear según
   el nivel del PJ.
5. Tests: `apply` crea espacios y acciones; `run_combat` con semilla
   gasta sin exceder; pool (`hechizo_soportado`) deja fuera lo no
   modelado. La prohibición de la Oleada la cubre ya A7 por código, no
   hace falta repetirla por clase.

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

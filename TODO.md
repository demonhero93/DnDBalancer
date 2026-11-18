# TODO — DnDBalancer / dnd_sim

Revisar al principio de cada sesión. Última revisión: 2026-11-17.
Solo tareas SIN implementar. Lo ya hecho: PASOS-ANTERIORES.txt
(bloques de cada sesión) y ARCHITECTURE.md.

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

- **Subclase pendiente**: Ninguna — las 8/8 registradas en
  `CLASSES["fighter"].subclasses`: Arcane Archer, Battle Master,
  Cavalier, Champion, Eldritch Knight (añadida 2026-11-16, commits
  A1-A7), Psi Warrior, Rune Knight y Samurai.
- **EK — verificación final sin marcar**: la casilla del plan quedó
  abierta (el grafo sí se regeneró, commit 1102662); falta constancia
  de pytest + capas en PASOS. Marcarla o anotar el motivo.
- **EK — pendientes reales** (reabrir SOLO con regla nueva del sim):
  distancia/movimiento (War Magic y hechizos sin alcance modelado),
  reacciones de hechizo, rituales/utilidad del pool, restricción PHB
  de escuelas (evocación/abjuración) si la confirma el maintainer,
  «contra hechizo del dueño» exacto (marker en
  `PJSpellAction.execute` en vez del shortcut `ctx.actor is owner`);
  War Bond y Arcane Charge = datos sin efecto.
- **Samurai — datos sin efecto congelados** (reabrir SOLO si el sim
  modela la mecánica; tests en `tests/clases/fighter/test_samurai.py`):
  - Bonus Proficiency: el idioma alternativo (sin modelo de idiomas).
  - Elegant Courtier: bonificador igual al mod SAB en
    Perspicacia/Persuasión (sin pruebas sociales en combate).
  - Tireless Spirit: recuperar 1 uso de Fighting Spirit al tirar
    iniciativa (cada combate empieza con usos completos, criterio
    Ever-Ready Shot).
  - Strength Before Death: salvaciones de muerte (SBD difiere el
    turno extra; reabrir SOLO si existan salvaciones de muerte).
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
  `tests/clases/fighter/test_rune_knight.py` (velocidad, alcance, distancias, runas
  despertadas, pruebas características de Storm, ventaja de Hill en
  salvaciones de veneno): sin posiciones ni movimiento, ningún efecto
  mide distancia. Reabrir solo si existe sistema de movimiento/
  posiciones o salvaciones tipadas.

## Fighter: cómo añadir una subclase

Receta (patrón bárbaro, ver `barbarian/subclasses/`; ejemplos de
fighter: `arcane_archer.py`, `cavalier.py`, `champion.py`,
`psi_warrior.py`, `samurai.py` y `eldritch_knight.py`; en paquete
`battle_master/` y `rune_knight/`):

1. Crear `rules/classes/fighter/subclasses/<clave>.py` con un
   `SubclassDef(name="<nombre visible>", class_name="fighter",
   min_level=3, apply=...)` y su rasgo (`Trait`) con los hooks
   necesarios. Si supera ~700 líneas, paquete con `__init__.py`
   (docstring de decisiones + `apply_*` + `_RNG_CREACION` + reexport),
   `features.py` (rasgo) y `actions.py` (acciones bonus); reapuntar los
   `monkeypatch` de `bm_mod`/`rk_mod` al submódulo donde vive el nombre
   parcheado (ver `battle_master/`, `rune_knight/`).
2. Registrar en `rules/classes/fighter/__init__.py`: importar la
   `SubclassDef` y añadirla al dict `subclasses` del `FIGHTER_CLASS`.
3. Reexportar la API en `rules/classes/__init__.py` y en la fachada
   `dnd_sim/__init__.py` (import + `__all__`) si expone símbolos
   nuevos.
4. Tests: `tests/clases/<clase>/test_<clave>.py` en español (registro, apply por
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

Receta (patrón del mago de test de `tests/reglas/spells/test_hechizos_pj.py`):

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
  `pytest tests/arquitectura/test_arquitectura.py`, `pytest`,
  `python tools/capas.py` (con `PYTHONIOENCODING=utf-8` en Windows),
  `graphify update .`.

## Rutina sugerida al abrir sesión

1. Leer este archivo.
2. `git status` → ¿trabajo sin commitear?
3. `pytest -q` → ¿suite en verde? (sin red; usa `cache/monsters/`)
4. Empezar tarea nueva.

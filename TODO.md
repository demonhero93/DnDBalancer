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

- **Subclases Fighter**: candidatas Eldritch Knight, Psi Warrior
  (Arcane Archer, Battle Master, Cavalier y Champion implementados,
  ver planes abajo).
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
- [ ] Docs — `ARCHITECTURE.md` (fila `rules/classes/`, helper de
  crítico por umbral, soporte de ventaja en iniciativa/pruebas,
  recuentos), `PASOS-ANTERIORES.txt` (bloque CHAMPION + ESTADO
  ACTUAL), `TODO.md` (receta y pendientes).
- [ ] Verificación — `pytest tests/test_arquitectura.py`, `pytest`,
  `python tools/capas.py`, `graphify update .` + commit final con el
  grafo.

## Fighter: cómo añadir una subclase

Receta (patrón bárbaro, ver `barbarian/subclasses/`; ejemplos de
fighter: `arcane_archer.py`, `battle_master.py` y `cavalier.py`):

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

Pendientes (candidatas PHB 2024): Eldritch Knight, Psi Warrior.
Arcane Archer, Battle Master, Cavalier y Champion YA están
implementados (`CLASSES["fighter"].subclasses` tiene sus 4 claves).

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

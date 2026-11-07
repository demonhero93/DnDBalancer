# Arquitectura de `dnd_sim`

Documento para humanos **y** para IA: qué carpetas hay, qué reglas de
importación siguen y cómo comprobar que siguen cumpliéndose.

```
core  <  model  <  rules  <  engine / data  <  fachada (dnd_sim)
```

Una capa solo importa de la suya o de una inferior. De abajo arriba:
primitivas puras (`core`), el dominio (`model`), las reglas del 5e
(`rules`), la orquestación (`engine` y `data`, hermanas: ninguna depende
de la otra) y, al final, la fachada pública `dnd_sim/__init__.py`.

## Carpetas

| Carpeta | Mód. | Líneas | Contenido |
|---|---:|---:|---|
| `dnd_sim/core/` | 13 | 943 | Dados, habilidades, enums, estado de combate, log, aleatoriedad, apuntado. **Cero imports internos.** |
| `dnd_sim/model/` | 4 | 1040 | Dataclasses del dominio: `Combatant`, `Monster`, `PlayerCharacter`, ataques y acciones. |
| `dnd_sim/rules/` | 31 | 9247 | Reglas 5e: condiciones, daño, salvaciones, pruebas, modificadores, legendario, uso, enganche, área, clases, maestrías. |
| `dnd_sim/rules/traits/` | 6 | 1268 | Los rasgos de monstruo (paquete, ver abajo). |
| `dnd_sim/rules/spells/` | 5 | 915 | Hechizos (paquete). |
| `dnd_sim/engine/` | 3 | 224 | Tácticas (políticas de objetivo) e informes (`stats`). |
| `dnd_sim/engine/combat/` | 3 | 926 | El motor: tirada de ataque y bucle de rondas (paquete). |
| `dnd_sim/data/` | 16 | 3394 | Carga de fichas de la API: parsers por tipo de dato. |
| `dnd_sim/__init__.py` | 1 | 184 | Fachada: reexporta la API pública ordenada por capa. |
| **Total** | **82** | **18141** | + `tests/` con 51 ficheros y 18589 líneas (1168 tests). |

## Reglas de dependencia

1. **`core` no importa nada de dentro de `dnd_sim`.** Es la base: si algo de
   `core` necesita `rules`, el sitio de ese algo no es `core`.
2. **`model` solo puede ver `core`.** Un combatiente no debe conocer las
   reglas; quien aplica reglas es `rules`/`engine`.
3. **`rules` puede ver `core` y `model`, y a sí mismo.** Las reglas se
   aplican *sobre* el dominio.
4. **`engine` y `data` pueden ver las tres capas de abajo.** `engine`
   orquesta la simulación; `data` construye combatientes desde JSON.
5. **La fachada lo reexporta todo y nadie la importa por dentro.** Dentro
   del paquete jamás se hace `from dnd_sim import X`; se importa el módulo
   concreto (`from ..core.dice import roll_d20`).

### Excepción única admitida

`model/combatant.py` → `rules.conditions` (capa 1 mirando a la 2). Es la
única violación consciente del paquete: `Combatant` necesita crear sus
condiciones y `conditions` necesita el tipo de combatiente. Prefiere
`Combatant` importar `rules.conditions` a esconderlo en un import diferido.

Está **congelada** en `tests/test_arquitectura.py`, que falla si aparece
una segunda violación o si esta desaparece (lista muerta).

## Paquetes con fachada

Tres ficheros gigantes se partieron en paquetes cuyo `__init__` reexporta
la misma API, así que **las importaciones de fuera no cambiaron**:

| Paquete | Módulos | Contenido |
|---|---|---|
| `rules/traits/` | `base` · `offense` · `defense` · `survival` · `stealth` | `Trait`, `HOOK_NAMES` (25 hooks, incl. `after_failed_check`), `hooks` y `TRAIT_CLASSES` en el `__init__`; los 12 rasgos agrupados por intención. |
| `rules/spells/` | `effects` · `reactions` · `actions` · `casting` | Efectos y concentración, represalias al recibir daño, las 5 acciones de hechizo y `Spell`/`Spellcasting`/`spell_action`. |
| `rules/classes/` | `base` · `barbarian/features` · `barbarian/subclasses/{ancestral_guardian,battlerager,beast,berserker,giant,storm_herald,wild_heart,wild_magic,world_tree,zealot}` · `fighter/features` · `fighter/subclasses/{arcane_archer}` | Registro genérico de clases y subclases (`CLASSES`, `apply_class`) y las clases bárbaro y guerrero con sus subclases (Path of the… y Arcane Archer). |
| `engine/combat/` | `attack` · `encounter` | Tirada de ataque completa (modificadores, ventajas, críticos, daño, represalias) e iniciativa, política de objetivo, bucle de rondas y `CombatResult`. |

Dentro de cada paquete el grafo es acíclico:

* `traits`: `base` ← {`offense`, `defense`, `survival`, `stealth`}
* `spells`: `effects` ← `actions` ← `casting`, `reactions` ← `actions`
* `combat`: `attack` y `encounter` sin dependencias internas
* `classes`: `base` ← `barbarian.features` ← `barbarian.subclasses` y
  `base` ← `fighter.features` ← `fighter.subclasses`;
  el `__init__` de cada clase reexporta `features` y declara la clase
  en el registro.

El personaje se define en código con sus características finales: ASI
(4/6/8/12/14/16) y Don Épico (19) del Guerrero solo son datos de tabla
en `FighterFeatures` (`asi_levels`, `epic_boon_level`), sin efecto
mecánico.

Los tests que parchean un símbolo apuntan al módulo que lo **define**
(`import dnd_sim.engine.combat.attack as combat_mod`), porque el
`monkeypatch` sustituye un nombre del espacio de nombres de ese módulo.

## Guaridas: política fija

Se asume **siempre** que la criatura legendaria está en su guarida; no
hay interruptor de encuentro.

- **Puntos legendarios**: `points_max = base + LEGENDARY_LAIR_BONUS`
  (MM 2024: 3, o 4 en guarida → siempre 4) para todo monstruo legendario.
  `DEFAULT_LEGENDARY_POINTS` es la base; `LEGENDARY_POINTS_OVERRIDES`
  guarda excepciones de base por índice; el CLI `--legendary-points N`
  fija el valor final sin sumar el bonus.
- **Fase de guarida** (`rules/legendary.py: lair_phase`): corre en la
  iniciativa 20 (empates perdidos) en cada ronda, cortado en
  `engine/combat/encounter.py`. Una acción por dueño y ronda, sin repetir
  la de la ronda anterior, `pick` entre elegibles (sin RNG con una sola
  opción), sin gastar recursos de turno ni puntos legendarios.
- **Sin fichero** `data/lairs/<index>.json` no hay fase, ni aviso, ni RNG.
  Los datos reales los aporta el maintainer; `data/lairs/` está vacío.
- **Efectos regionales**: ignorados por diseño.

## Imports diferidos

Los imports dentro de una función o de `if TYPE_CHECKING` no son
dependencias: existen para cortar ciclos de importación que ninguna capa
puede romper por sí sola. Por eso sí pueden apuntar hacia arriba
(`rules.traits.defense` importa `engine.combat` dentro de una función).

`python tools/capas.py` imprime las dos listas por separado y las
violaciones de capa. El criterio (solo nivel de módulo) está congelado en
`tests/test_arquitectura.py`.

## Cómo comprobar que todo sigue en orden

```bash
pytest tests/test_arquitectura.py   # reglas de capa + fachadas de paquete
pytest                              # 1168 tests
python tools/capas.py               # mapa de dependencias y violaciones
graphify update .                   # grafo y comunidades en graphify-out/
```

Al añadir un módulo nuevo basta con meterlo en su carpeta: si intenta
importar de una capa superior, `test_las_capas_no_se_miran_hacia_arriba`
lo dice con el par exacto `origen -> destino`.

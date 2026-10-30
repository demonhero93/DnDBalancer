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
| `dnd_sim/core/` | 13 | 758 | Dados, habilidades, enums, estado de combate, log, aleatoriedad, apuntado. **Cero imports internos.** |
| `dnd_sim/model/` | 4 | 932 | Dataclasses del dominio: `Combatant`, `Monster`, `PlayerCharacter`, ataques y acciones. |
| `dnd_sim/rules/` | 17 | 3872 | Reglas 5e: condiciones, daño, salvaciones, pruebas, modificadores, legendario, uso, enganche, área, clases. |
| `dnd_sim/rules/traits/` | 6 | 1129 | Los rasgos de monstruo (paquete, ver abajo). |
| `dnd_sim/rules/spells/` | 5 | 909 | Hechizos (paquete). |
| `dnd_sim/engine/` | 3 | 224 | Tácticas (políticas de objetivo) e informes (`stats`). |
| `dnd_sim/engine/combat/` | 3 | 765 | El motor: tirada de ataque y bucle de rondas (paquete). |
| `dnd_sim/data/` | 15 | 3110 | Carga de fichas de la API: parsers por tipo de dato. |
| `dnd_sim/__init__.py` | 1 | 132 | Fachada: reexporta la API pública ordenada por capa. |
| **Total** | **68** | **12546** | + `tests/` con 35 ficheros y 10826 líneas (671 tests). |

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
| `rules/traits/` | `base` · `offense` · `defense` · `survival` · `stealth` | `Trait`, `HOOK_NAMES`, `hooks` y `TRAIT_CLASSES` en el `__init__`; los 12 rasgos agrupados por intención. |
| `rules/spells/` | `effects` · `reactions` · `actions` · `casting` | Efectos y concentración, represalias al recibir daño, las 5 acciones de hechizo y `Spell`/`Spellcasting`/`spell_action`. |
| `rules/classes/` | `base` · `barbarian/features` · `barbarian/subclasses/{base,ancestral_guardian,battlerager,beast}` | Registro genérico de clases y subclases (`CLASSES`, `apply_class`) y la clase bárbaro con las suyas. |
| `engine/combat/` | `attack` · `encounter` | Tirada de ataque completa (modificadores, ventajas, críticos, daño, represalias) e iniciativa, política de objetivo, bucle de rondas y `CombatResult`. |

Dentro de cada paquete el grafo es acíclico:

* `traits`: `base` ← {`offense`, `defense`, `survival`, `stealth`}
* `spells`: `effects` ← `actions` ← `casting`, `reactions` ← `actions`
* `combat`: `attack` y `encounter` sin dependencias internas
* `classes`: `base` ← `barbarian.features` ← `barbarian.subclasses`;
  el `__init__` de `barbarian` reexporta `features` y declara la clase
  en el registro.

Los tests que parchean un símbolo apuntan al módulo que lo **define**
(`import dnd_sim.engine.combat.attack as combat_mod`), porque el
`monkeypatch` sustituye un nombre del espacio de nombres de ese módulo.

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
pytest                              # 671 tests
python tools/capas.py               # mapa de dependencias y violaciones
graphify update .                   # grafo y comunidades en graphify-out/
```

Al añadir un módulo nuevo basta con meterlo en su carpeta: si intenta
importar de una capa superior, `test_las_capas_no_se_miran_hacia_arriba`
lo dice con el par exacto `origen -> destino`.

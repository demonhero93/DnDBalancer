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
| `dnd_sim/core/` | 13 | 1090 | Dados, habilidades, enums, estado de combate, log, aleatoriedad, apuntado. **Cero imports internos.** |
| `dnd_sim/model/` | 4 | 1050 | Dataclasses del dominio: `Combatant`, `Monster`, `PlayerCharacter`, ataques y acciones. |
| `dnd_sim/rules/` | 34 | 11212 | Reglas 5e: condiciones, daño, salvaciones, pruebas, modificadores, legendario, uso, enganche, área, clases, maestrías, umbral crítico. |
| `dnd_sim/rules/traits/` | 6 | 1299 | Los rasgos de monstruo (paquete, ver abajo). |
| `dnd_sim/rules/spells/` | 5 | 917 | Hechizos (paquete). |
| `dnd_sim/engine/` | 3 | 224 | Tácticas (políticas de objetivo) e informes (`stats`). |
| `dnd_sim/engine/combat/` | 3 | 1206 | El motor: tirada de ataque y bucle de rondas (paquete). |
| `dnd_sim/data/` | 16 | 3394 | Carga de fichas de la API: parsers por tipo de dato. |
| `dnd_sim/__init__.py` | 1 | 192 | Fachada: reexporta la API pública ordenada por capa. |
| **Total** | **86** | **21276** | + `tests/` con 56 ficheros y 23617 líneas (1499 tests). |

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
| `rules/traits/` | `base` · `offense` · `defense` · `survival` · `stealth` | `Trait`, `HOOK_NAMES` (28 hooks, incl. `on_any_turn_start`, `on_any_turn_end`, `after_failed_check` y `defensa_ante_ataque`), `hooks` y `TRAIT_CLASSES` en el `__init__`; los 12 rasgos agrupados por intención. |
| `rules/spells/` | `effects` · `reactions` · `actions` · `casting` | Efectos y concentración, represalias al recibir daño, las 5 acciones de hechizo y `Spell`/`Spellcasting`/`spell_action`. |
| `rules/classes/` | `base` · `barbarian/features` · `barbarian/subclasses/{ancestral_guardian,battlerager,beast,berserker,giant,storm_herald,wild_heart,wild_magic,world_tree,zealot}` · `fighter/features` · `fighter/subclasses/{arcane_archer,battle_master,cavalier,champion,psi_warrior}` | Registro genérico de clases y subclases (`CLASSES`, `apply_class`) y las clases bárbaro y guerrero con sus subclases (Path of the…, Arcane Archer, Battle Master, Cavalier, Champion y Psi Warrior). |
| `engine/combat/` | `attack` · `encounter` | Tirada de ataque completa (modificadores, ventajas, críticos por umbral `evaluar_d20`, daño, represalias): helper `daño_base_arma` (daño bruto reutilizable) y punto de sustitución `sustituir_ataque` (duck-typing, sin hook en HOOK_NAMES) en el paso 2b, antes del d20. Más iniciativa, política de objetivo, bucle de rondas y `CombatResult`. |

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

## Arcane Archer (XGE)

- **Punto de sustitución del ataque**: `sustituir_ataque` en el paso 2b
  de `attack_roll` (patrón `resolver_maestria`, duck-typing, NO hook en
  `HOOK_NAMES`). Sin rasgos o con `None` → flujo idéntico sin RNG; con
  resultado (`rules.traits.base.AtaqueSustituido`) → se devuelve sin
  d20, sin `after_attack_roll` ni maestrías. Lo usan Piercing/Seeking.
- **Helper de daño**: `daño_base_arma` en `engine/combat/attack.py`
  extrae el daño bruto del arma (misma función para un impacto normal
  y para «daño como si hubiera impactado»), sin cambiar el orden de
  `roll_dice`/RNG.
- **Ever-Ready Shot (10) es una decisión de diseño, NO deuda**: cada
  combate empieza con los usos de Arcane Shot completos, así que su
  ventaja es inalcanzable por diseño. Congelada en
  `test_ever_ready_shot_no_cambia_los_usos_al_empezar_un_combate`;
  reabrir solo si el sim modela más de un combate por descanso.

## Battle Master (PHB 2024)

- **Reacciones (sesión 2)**: Parry (`reducir_dano_recibido`, sobre el
  atacado, antes de `inflict_damage`), Riposte (`reaccionar_al_fallo`,
  tras un fallo cuerpo a cuerpo) y Commander's Strike
  (`sustituir_ataque`, paso 2b). Las tres son duck-typing sobre el
  dueño del rasgo, sin entrada en `HOOK_NAMES`; guards SIN RNG y
  decisión `pick` «no»/«sí». El dado sale de `_tirar_dado`
  (Relentless incluido) y, en los ataques de reacción, viaja en
  `ctx.dano_reaccion` (plano: `daño_base_arma` lo suma sin duplicarlo
  en crítico).
- **Commander's Strike — sesgo documentado, NO deuda**: el aliado se
  elige ANTES de la tirada (paso 2b), mientras que las maniobras de
  impacto se deciden después de conocer el resultado; la decisión no
  es equiprobable con ellas. El dueño gasta el dado, el aliado gasta
  SU reacción. El ataque aliado lleva `r_ctx.is_reaction=True`: no
  reentra en Commander's Strike ni activa maniobras de la sesión 1.
  Congelado en `test_commanders_strike_*` de
  `tests/test_battle_master.py`.
- **Rally (B1, acción bonus)**: `BattleMasterRallyAction` con
  `usage=None` y patrón Feinting (guards sin RNG + pick «no»/«sí»).
  Exige la maniobra conocida; PV temporales = max(1, dado + mod CAR
  del dueño) con política `max(actual, cantidad)` (no se acumulan,
  patrón aura tundra). No consume la reacción de nadie.
- **Ambush (B3, iniciativa)**: `bonus_iniciativa` lo consulta
  `roll_initiative` con duck-typing puro (el motor no importa
  rules): guards sin RNG + pick «no»/«sí» + un dado de superioridad
  sumado antes del mod DES. La parte de Sigilo es dato sin efecto
  (el motor no tira habilidades en combate). El mismo bucle consulta
  `ventaja_iniciativa()`/`desventaja_iniciativa()` (Champion,
  Remarkable Athlete) y combina las fuentes con la regla estándar:
  solo Champion consume RNG nuevo aquí.

## Cavalier (XGE)

- **Warding Maneuver (7)**: hook nuevo `defensa_ante_ataque` en
  `HOOK_NAMES`; el motor lo consulta en el paso 6 de `attack_roll`
  con `_defensa_del_bando` (enumera el bando del OBJETIVO con
  `_bando_del`, la misma enumeración que `reduce_damage_to_allies`)
  cuando el golpe iba a entrar o es crítico. Devuelve
  `SimpleNamespace(ac_extra, resistencia)`: la CA extra recalcula el
  impacto (el 20 natural siempre impacta) y la resistencia es una
  concesión temporal del tipo SOLO durante `apply_damage_modifiers`
  (no se acumula con la resistencia previa del tipo). Reacción
  compartida con Parry/Riposte/Hold the Line.
- **Unwavering Mark (3)**: marca tras impactar (`after_attack_roll`),
  desventaja en `consumir_marcas` (campo propio `marca_cavalier`),
  ataque especial `CavalierMarkAttackAction` armado desde
  `inflict_damage` (punto central con fuente: cubre salvaciones y
  área).
- **Hold the Line (10)**: `_oportunidad_contra_bando` al FINAL de
  `attack_roll` (duck-typing, NO en `HOOK_NAMES`, guard
  `ctx.is_reaction`) llama al `ataque_de_oportunidad` del bando del
  atacado. Reinterpretación documentada: sin movimiento en el sim, el
  ataque de oportunidad abstracto se dispara cuando un enemigo ataca
  con tirada a un aliado distinto del dueño (los hechizos de
  salvación no pasan por `attack_roll`).
- **Vigilant Defender (18)**: segunda reacción por ronda
  (`especial_usada_en_ronda` comparada con `ctx.round`) exclusiva de
  Hold the Line, consumida antes que la normal y solo fuera del turno
  propio; simplificación: sin identificador de turno ajeno en `ctx`
  no se aplica la restricción «mismo turno que otra reacción».
- **Ferocious Charger (15)**: `_evaluar_carga` desde
  `after_attack_roll` — UNA evaluación por turno en el primer
  impacto cuerpo a cuerpo, patrón Reckless: constante
  `CHARGE_MOVE_PROBABILITY` = 0.5 en `core/classes.py` y CLI
  `--charge-p` en `main.py` (0.0/1.0 sin RNG); si hay carga, `pick`
  «no»/«sí» y salvación de FUE CD 8 + PB + mod FUE → `PRONE` con el
  `EscapeCheck` de Topple.
- **Datos sin efecto (freeze en `tests/test_cavalier.py`)**: Born to
  the Saddle (monturas), velocidad 0 de la marca (modelo sin campo
  de velocidad) y los 5 ft de Warding (el sim no guarda posiciones).

## Champion (PHB 2024)

- **Rango crítico ampliado (3/15)**: helpers nuevos
  `umbral_critico(attacker, atk)` y `evaluar_d20(roll, attacker, atk)`
  en `rules/roll_modifiers.py`; el motor los usa en `attack_roll`
  (decisión de crítico/impacto automático y de 1 natural, sustituyendo
  el `roll == 20` literal). `umbral_critico` recorre los traits del
  ATACANTE por duck-typing (`fn(atk)`, sin entrada en `HOOK_NAMES`) y
  devuelve el mínimo con 20; sin rasgo → 20 sin RNG.
  `ChampionFeatures.umbral_critico` devuelve
  `champion_crit_threshold(nivel)` de `core/classes.py` (20 / 19
  desde el 3 / 18 desde el 15) y 20 para ataques de hechizo gracias
  al campo nuevo `spell_attack` (default `False` en `model/attack.py`;
  `spells/casting.py` lo pone a `True` — `magical` no sirve: también
  lo llevan armas mágicas y naturales). Un crítico por rango ampliado
  cuenta como crítico en todos los consumidores (dados doblados,
  Warding Maneuver, Sweeping, Studied Attacks, reacciones,
  Precision).
- **Remarkable Athlete (3)**: `ventaja_iniciativa()` en
  `ChampionFeatures` lo consulta `roll_initiative` (recuento de
  fuentes: flag `initiative_with_advantage` o trait, contra
  `desventaja_iniciativa()`; solo ventaja/desventaja tira dos d20 con
  `roll_d20`, ambas o ninguna → `d20` normal, RNG del resto exacto).
  `modify_check_modifiers` añade ventaja en Atletismo (patrón Furia;
  se anula con desventaja en `CheckModifiers.mode`; sin competencia
  añadida). Moverse tras un crítico: `# TODO` dato sin efecto.
- **Additional Fighting Style (7)**: `FighterFeatures.estilos_extra`
  + propiedad `estilos` (principal + adicionales); los 6 hooks de
  estilos comprueban pertenencia al conjunto (el atributo `estilo` y
  la mutación Defense de `apply_fighter` quedan intactos).
  `apply_champion` valida siempre el kwarg `additional_fighting_style`
  (en el pool y ≠ primero) y, solo con nivel ≥ 7, elige con `pick`
  entre `FIGHTER_STYLES` menos el primero (semilla 0 vía
  `_RNG_CREACION`) y aplica `+1 CA` si el segundo es Defense —una
  sola vez, el pool excluye el primero—. `apply_class` no reenvía
  `**kwargs`: el kwarg se pasa llamando a `apply_champion` directo.
- **Heroic Rally (18)**: `on_turn_start` con guards (nivel ≥ 18,
  dueño, vivo, ≥ 1 PG, Bloodied `pg * 2 <= pg_max`); cura
  `min(heroic_rally_amount(mod CON), pg_max - pg)` vía `log_line`,
  sin RNG.
- **Datos sin efecto (freeze en `tests/test_champion.py`)**: Heroic
  Warrior (sin Inspiración Heroica) y Defy Death (sin salvaciones de
  muerte); reabrir solo si el sim los modela (condiciones en
  `TODO.md`).

## Psi Warrior (PHB 2024)

- **Psionic Power (3)**: tablas nuevas `psionic_dice_count` /
  `psionic_die_sides` / `bulwark_targets` en `core/classes.py`;
  reserva única de dados (2 × PB) compartida por todos los rasgos;
  un combate = un día descansado (`reset` los rellena).
- **Protective Field (3)**: walker NUEVO `_proteccion_psionica` en la
  fase 1a de `rules/damage.py` (entre `reduce_damage_to_allies` y los
  PV temporales), que recorre TODOS los combatientes incluido el
  target; duck-typing por `getattr`, sin entrada en `HOOK_NAMES`.
  Guards sin RNG (nivel ≥ 3, daño > 0, objetivo = dueño o aliado
  vivo — nunca enemigos —, reacción libre compartida, dados) y
  `pick` «no»/«sí»; reduce `max(1, dado + mod INT)` sin bajar de 0.
- **Psionic Strike (3)**: walker NUEVO `_dano_extra_de_rasgo` en
  `engine/combat/attack.py`, tras el `inflict_damage` principal y
  antes del bucle `extra_damage` (duck-typing, sin `HOOK_NAMES`);
  daño de fuerza `dado + mod INT` una vez por turno (flag; solo
  armas — `spell_attack` queda excluido —, los naturales cuentan).
- **Telekinetic Thrust (7)**: al gastarse el dado, salvación de FUE
  CD 8 + PB + mod INT → `PRONE` con `EscapeCheck`; el empuje de 10 ft
  es dato sin efecto.
- **Guarded Mind (10)**: resistencia permanente a psíquico (patrón
  Storm Soul, sin acumular) + purga de Hechizado/Asustado en
  `on_turn_start` con `pick` y `remove_condition`.
- **Bulwark of Force (15)**: `PsiBulwarkAction` (acción bonus,
  `usage=None`); campo nuevo `cobertura_bulwark` (ref al dueño) en
  `CombatState` + `effective_ac` +2 (máx. con `at_range`, sin sumar)
  y salvaciones de DES +2 mientras el dueño siga vivo y sin estar
  Incapacitado (`can_act`); uso gratuito primero y luego un dado.
- **Telekinetic Master (18)**: `TelekineticMasterAction` +
  `TelekineticMasterAttackAction` (helper `attack_roll` +
  `copy.copy(context)`, patrón Unwavering Mark); concentración
  SIMPLE: flag mientras el dueño no esté Incapacitado ni muerto, SIN
  salvaciones de CON («concentración parcial» en `TODO.md`).
- **Datos sin efecto (freeze en `tests/test_psi_warrior.py`)**:
  Telekinetic Movement y Psi-Powered Leap (sin movimiento), empuje
  de 10 ft de Thrust, distancias de 30 ft y el efecto de Telekinesis
  (solo concede el ataque adicional).

## Cómo comprobar que todo sigue en orden

```bash
pytest tests/test_arquitectura.py   # reglas de capa + fachadas de paquete
pytest                              # 1499 tests
python tools/capas.py               # mapa de dependencias y violaciones
graphify update .                   # grafo y comunidades en graphify-out/
```

Al añadir un módulo nuevo basta con meterlo en su carpeta: si intenta
importar de una capa superior, `test_las_capas_no_se_miran_hacia_arriba`
lo dice con el par exacto `origen -> destino`.

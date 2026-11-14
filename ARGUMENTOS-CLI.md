# CLI del simulador: `build_parser()`

Documento de referencia de los argumentos de línea de comandos.
Función fuente: `build_parser()` en `main.py:141-183`.
Punto de entrada: `main()` en `main.py:186-208`, que llama
`args = build_parser().parse_args()`.

`build_parser()` crea un `argparse.ArgumentParser` con descripción
"Simulador de combate D&D 5e" y devuelve el parser. No valida nada por sí
solo: la validación real ocurre en `main()` y en los helpers que consumen
los valores.

## Resumen de flags

| Flag | Alias | Tipo | Default | Efecto |
|------|-------|------|---------|--------|
| `--monster` | `-m` | `str`, `action="append"` | `[]` | Carga monstruos desde la API. Repetible. |
| `--simulations` | `-n` | `int` | `1000` | Número de simulaciones del reporte. |
| `--seed` | — | `int` | `1` | Semilla RNG (combate de ejemplo + simulación). |
| `--verbose` | — | `store_true` | `False` | Definido pero no consumido en `main()`. Ver "Observaciones". |
| `--party` | — | `int` | `5` | Tamaño del grupo de PJ (1-5). |
| `--legendary-p` | — | `float` | `1.0` | Prob. de acción legendaria por disparo (0.0-1.0). |
| `--resistance-p` | — | `float` | `1.0` | Prob. de que Legendary Resistance convierta fallo en éxito (0.0-1.0). |
| `--legendary-points` | — | `int` | `None` | Fija puntos legendarios por monstruo sin bonus de guarida. |
| `--reckless-p` | — | `float` | `None` | Prob. de Ataque Temerario por turno (0.0-1.0). |
| `--utility-p` | — | `float` | `None` | Prob. de acción utilitaria (0.0-1.0). |

## Detalle por flag

### `--monster` / `-m`

- `action="append"`: cada aparición añade un token a la lista
  `args.monster`. Ej: `--monster owlbear --monster goblin:3`.
- Formato del token: `index` o `index:cantidad`. Lo parsea
  `_parse_monster_token()` (`main.py:15-24`):
  - `index` es el nombre del monstruo en la API (case-insensitive vía
    `index()` de `api.py`).
  - `cantidad` se separa con `rsplit(":", 1)`; ausente = 1.
  - `cantidad < 1` lanza `argparse.ArgumentTypeError`.
- Consumo en `main()` (`main.py:192-195`): si la lista queda vacía, se usa
  el default `["skeleton:25"]`. Luego `_load_party()` (`main.py:27-46`)
  instancia cada monstruo con `load_monster(index)` y, si `cantidad > 1`,
  renombra como `"Nombre i"`.
- Errores de índice inexistente los produce `load_monster`, no argparse.

### `--simulations` / `-n`

Entero. Pasa como `n` a `simulate(combatants, n=args.simulations,
seed=args.seed)` (`main.py:207`). Default 1000.

### `--seed`

Entero. Se usa dos veces con el mismo valor:
1. `run_combat(..., random.Random(args.seed), verbose=True)` para el combate
   de ejemplo (`main.py:203`).
2. `simulate(..., seed=args.seed)` para el reporte (`main.py:207`).

Mismo seed ⇒ mismos resultados en ambas fases.

### `--verbose`

Flag booleano. Ayuda: "Muestra el primer combate."
**No se lee en `main()`**: el combate de ejemplo se ejecuta siempre con
`verbose=True` (`main.py:203`). Ver "Observaciones".

### `--party`

Entero, default 5. Indica cuántas plantillas de `PARTY_TEMPLATES`
(`main.py:52-88`) se usan, en orden: Guerrero, Pícaro, Monje, Clérigo,
Barbaro.

Validación en `_build_party()` (`main.py:97-100`): lanza `ValueError` si
`size < 1` o `size > len(PARTY_TEMPLATES)` (5). La validación no está en
argparse: el error aparece en tiempo de ejecución de `main()`, no al
parsear.

### `--legendary-p`

Float, default 1.0. Probabilidad de que un monstruo use una acción
legendaria en cada disparo.

Consumo en `_load_party()` (`main.py:38-41`): solo aplica a monstruos con
atributo `legendary` distinto de `None`. Se asigna a
`legendary.use_probability`.

### `--resistance-p`

Float, default 1.0. Probabilidad de que Legendary Resistance convierta un
fallo de salvación en éxito.

Mismo consumo que `--legendary-p`: `legendary.resistance_probability`
(`main.py:41`), solo si el monstruo tiene `legendary`.

### `--legendary-points`

Entero, default `None`.

- `None`: cada monstruo mantiene su valor base + bonus de guarida (cálculo
  interno de la carga del monstruo).
- Con valor: `_load_party()` fija `legendary.points_max` y
  `legendary.points_left` a ese número, sin sumar bonus (`main.py:42-44`).
  Solo aplica si el monstruo tiene `legendary`.

### `--reckless-p`

Float, default `None`. Probabilidad de que un bárbaro use Ataque Temerario
en cada turno (0.0-1.0).

- `None`: no se toca nada. Rige la constante
  `RECKLESS_USE_PROBABILITY = 0.5` en
  `dnd_sim/rules/classes/barbarian/features.py:56`.
- Con valor: `_build_party()` recorre los traits de cada PJ y, si es
  `BarbarianFeatures`, fija `trait.reckless_probability`
  (`main.py:130-136`).

**Invariante del proyecto**: Ataque Temerario es siempre una decisión
aleatoria por turno (`RECKLESS_USE_PROBABILITY`, por defecto 0.5), nunca
una estrategia fija. El flag cambia la probabilidad, no convierte la
acción en fija.

### `--utility-p`

Float, default `None`. Probabilidad de usar una utilitaria
(Esquivar/Agarrar/Empujar) en vez del ataque o acción previsto (0.0-1.0).

- `None`: no se toma ninguna acción. Rige
  `UTILITY_ACTION_PROBABILITY = 0.05` en `dnd_sim/rules/utility.py:30`.
- Con valor: `main()` reasigna el global del módulo antes de simular:
  `utility.UTILITY_ACTION_PROBABILITY = float(args.utility_p)`
  (`main.py:188-191`). Efecto en todo el proceso.

## Flujo de `main()`

1. `build_parser().parse_args()`.
2. Si `--utility-p` llegó, reasigna `UTILITY_ACTION_PROBABILITY`.
3. Carga monstruos: `args.monster` o `["skeleton:25"]` → `_load_party()`.
4. Carga PJ: `_build_party(args.party, reckless_p=args.reckless_p)`.
5. Combate de ejemplo con `seed`, imprime log y ganador.
6. `simulate(..., n=args.simulations, seed=args.seed)` + `print_report()`.

## Ejemplos

```bash
# Default: 25 esqueletos vs 5 PJ, 1000 simulaciones
python main.py

# Owlbear solo vs 3 PJ
python main.py -m owlbear --party 3

# Horda: 1 owlbear + 3 goblins, semilla fija, 5000 simulaciones
python main.py -m owlbear -m goblin:3 -n 5000 --seed 42

# Tuning legendario y de utilidad
python main.py -m "young red dragon" --legendary-p 0.8 --resistance-p 0.5 \
  --legendary-points 4 --reckless-p 0.7 --utility-p 0.1
```

## Observaciones (para humanos y IA)

1. `--verbose` está declarado pero nunca se lee en `main()`. El combate de
   ejemplo se imprime siempre. Para apagarlo habría que leer `args.verbose`
   en `main.py:203`.
2. `--party` no se valida en argparse: un valor fuera de 1-5 muere con
   `ValueError` después del parseo.
3. `--legendary-p`, `--resistance-p` y `--legendary-points` no hacen nada
   con monstruos sin atributo `legendary` (silencioso, sin aviso).
4. `--reckless-p` y `--utility-p` con `None` significan "no tocar el
   default global"; el default real vive en las constantes citadas, no en
   argparse.
5. El texto de ayuda de `--legendary-p` dice "monstruo legítimo"; es typo
   por "legendario".

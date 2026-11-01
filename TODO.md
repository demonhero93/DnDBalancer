# TODO — DnDBalancer / dnd_sim

Revisar al principio de cada sesión. Última revisión: 2026-10-30.
Contexto detallado: PASOS-ANTERIORES.txt (sección 7) y ARCHITECTURE.md.

## Bloque 2026-10-30 (commiteado)

- `ff30aac` feat(classes): registro de clases + Path of the Beast (20 ficheros).
- `667bc0a` docs: reglas, log de sesión y este TODO.
- `37b2806` chore(graph): grafo regenerado.
- Pendiente de push si hay remoto.

## TODOs en código (marcados `# TODO`)

- Grapple y Shove: opciones del Golpe sin armas que sustituyen UN ataque de
  la acción de Atacar (2024). Dodge: una Acción completa. Si algún rasgo
  concede la versión como acción adicional, entra con la misma política.
- Política de "a veces": probabilidad baja y configurable por turno
  (constante `UTILITY_ACTION_PROBABILITY`, valor por defecto a decidir y
  parámetro opcional en `main.py`). Solo se consulta el RNG si hay alguna
  utilitaria disponible: sin ellas, ni una tirada extra. Si sale, se
  elige entre las utilitarias disponibles con `pick`. Debe poder
  desactivarse a 0 para recuperar las referencias A/B exactas.
- Grapple: salvación del objetivo de FUE o DES (a elegir por `pick`, o la
  mejor según la regla que se verifique) contra CD = 8 + mod FUE +
  competencia. Si falla, queda agarrado. Escape: reutilizar `EscapeCheck`
  y `attempt_escapes` (prueba de FUE o DES contra esa CD). Límite de
  tamaño (un tamaño mayor como máximo): usar el `size` de la API si el
  modelo lo guarda; si no, `# TODO`.
- Shove: misma salvación; si falla, derribado (PRONE, que ya existe) o
  empujado (el empuje se ignora sin movimiento: solo se usa la opción
  derribar).
- Dodge: hasta el inicio de su siguiente turno, los ataques contra él
  tienen desventaja (si ve al atacante) y tiene ventaja en salvaciones de
  DES; se pierde si queda incapacitado. Integrar en `roll_modifiers.py` con
  una fuente legible `"Esquivar"`.
- Restricciones: no agarrar si ya agarra o el objetivo ya está agarrado por
  él; no empujar a alguien ya derribado; Dodge no si ya está esquivando.
  Nunca contra aliados (`valid_targets`).
- Condición GRAPPLED: hoy está en `EXCLUDED_CONDITIONS` por "no dar ventaja
  ni desventaja", pero en 2024 impone desventaja a los ataques contra
  cualquier objetivo que no sea el agarrador. Revisar y, si procede,
  moverla al Enum `Condition` actualizando el test guardián y la
  documentación.
- Tests: frecuencia de uso acorde a la probabilidad configurada; ningún
  consumo de RNG sin utilitarias disponibles; A/B exactas con p = 0;
  efecto de cada acción en una simulación; reproducibilidad.
- Una decisión por turno propio, justo antes de la primera tirada de ataque
  de FUE del turno (regla 2024: solo puede decidirse en esa tirada).
  Reacciones y ataques fuera de su turno (Retaliation, Spiked Retribution,
  cola de la Beast) NO lo deciden ni lo reciben.
- La decisión NO depende de la Furia: se tira esté o no activa. Furia
  activa solo es requisito de Frenzy, no de Ataque Temerario.
- Constante `RECKLESS_USE_PROBABILITY = 0.5` (valor por defecto, comentada
  con el motivo de diseño) y opción `--reckless-p` en `main.py`, igual que
  `--legendary-p`. Con `0.0` no se usa nunca y con `1.0` siempre, y en esos
  dos valores NO se consume RNG; con cualquier otro valor se consume
  exactamente UNA tirada por turno, solo cuando hay una primera tirada de
  ataque de FUE que decidir. No inventes un `pick` con pesos: usa el mismo
  patrón de probabilidad que `use_probability` de las legendarias.
- Antes del nivel 2 (o sin ataques de FUE ese turno), no hay decisión ni
  RNG.
- Efecto si se usa: ventaja en sus tiradas de ataque de FUE durante ese
  turno; los ataques contra él tienen ventaja hasta el inicio de su
  siguiente turno. Pasa por `roll_modifiers.py` con fuentes legibles
  (`"Ataque Temerario"`); NO cambies las reglas de cancelación de ventaja y
  desventaja.
- Estado por turno: `reckless_active_this_turn` (la propiedad que Frenzy
  consulta) y el estado de "ataques contra él con ventaja" se reinician en
  `on_turn_start` y en `reset()`.
- Log: `Guerrero ataca con temeridad` / `Guerrero decide no atacar con
  temeridad`.

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

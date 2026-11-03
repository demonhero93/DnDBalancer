# TODO — DnDBalancer / dnd_sim

Revisar al principio de cada sesión. Última revisión: 2026-11-03.
Contexto detallado: PASOS-ANTERIORES.txt (secciones 9-10) y ARCHITECTURE.md.

## Bloque 2026-10-30 (commiteado)

- `ff30aac` feat(classes): registro de clases + Path of the Beast (20 ficheros).
- `667bc0a` docs: reglas, log de sesión y este TODO.
- `37b2806` chore(graph): grafo regenerado.
- Pendiente de push si hay remoto.

## TODOs en código (marcados `# TODO`)

- Path of the Giant (`rules/classes/barbarian/subclasses/giant.py`):
  - Giant's Power: el truco Druidcraft/Thaumaturgy es dato
    informativo, sin efecto mecánico (trucos fuera de combate no
    modelados).
  - Alcance +5 ft (Giant Stature) y +10 ft (Demiurgic Colossus) no
    modelados: no hay sistema de movimiento/posiciones.
  - Elemental Cleaver: cambiar el tipo elegido al impactar o como
    acción adicional NO implementado (a petición); recoger el arma
    lanzada no se modela (se recobra sola).
  - Mighty Impel: alcance 9 m y «o criatura voluntaria» no modelados;
    solo se usa contra un enemigo con GRAPPLED (simplificación del
    enunciado). La decisión de usarlo o no la hace el `pick` del
    encuentro entre acciones candidatas (patrón Intimidating
    Presence).

- Path of the Storm Herald
  (`rules/classes/barbarian/subclasses/storm_herald.py`):
  - La «acción adicional» de Storm Aura se modela como bonus action:
    el motor solo ejecuta una ACTION y una BONUS_ACTION por turno;
    la decisión de activarla la hace el `pick` del encuentro entre
    candidatas (patrón Intimidating Presence / Mighty Impel).
  - Aura sin posiciones: `STORM_AURA_COVERAGE_PROBABILITY = 1.0`
    (convención de `rules/area.py`: todo el mundo cuenta a 10 ft);
    1.0/0.0 no consumen RNG y en medio hay UNA tirada por criatura.
    Cambiar la constante si algún día hay geometría real.
  - «Que vea» (Sea) y «aliados elegidos» (Shielding Storm / tundra):
    sin sistema de visión/elección se usa el pool completo (todos los
    enemigos / todos los aliados del aura).
  - Storm Soul: solo la resistencia; los efectos de exploración
    (respirar bajo el agua, nadar, congelar agua, calor extremo) no
    tienen efecto en combate sin movimiento: no se modelan.
  - Raging Storm tundra: la velocidad 0 se guarda como dato
    (`velocidad_cero`) hasta el próximo turno del bárbaro; sin
    sistema de movimiento no tiene efecto mecánico.
  - Raging Storm tundra no tiene reacción (solo actúa al activarse),
    igual que el enunciado.

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

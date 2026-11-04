# TODO — DnDBalancer / dnd_sim

Revisar al principio de cada sesión. Última revisión: 2026-11-04.
Contexto detallado: PASOS-ANTERIORES.txt (secciones 9-13) y ARCHITECTURE.md.

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

- Path of the Wild Heart (`rules/classes/barbarian/subclasses/wild_heart.py`):
  - Animal Speaker (3), Nature Speaker (10) y Aspect of the Wilds (6:
    Owl/Panther/Salmon, parámetro fijo `aspecto`, no aleatorio): rituales
    y exploración sin efecto en combate — solo dato del rasgo.
  - Eagle (3): Disengage/Dash como acción adicional; sin posiciones no
    tienen efecto mecánico (1/3 de las activaciones no aporta nada: es
    el comportamiento esperado del pick).
  - Falcon (14) queda FUERA del pick de Power of the Wilds por no tener
    efecto (velocidad de vuelo sin posiciones); añadirla si algún día
    hay modelo de movimiento.
  - Bear: los B/P/S no se añaden al set de resistencias: ya los
    recorta la Furia base (`modify_incoming_damage`) durante la MISMA
    ventana y duplicarlos recortaría el daño a un cuarto (mismo efecto
    efectivo). El resto de tipos se concede con lista de fuente propia.
  - Wolf/Lion sin posiciones: «a 5 pies» usa
    `WILD_HEART_COVERAGE_PROBABILITY = 1.0` (mismo criterio que el
    aura del Storm Herald); 1.0/0.0 no consumen RNG y en medio hay UNA
    tirada por criatura.
  - Lion: «otro personaje con este mismo beneficio» interpretado como
    un Wild Heart en Furia con opción León (lectura literal del
    enunciado; cambiar si el usuario quiere otra cosa).
  - Ram: alcance y «voluntaria» no modelados; PRONE con el mismo
    escape de Empujar (FUE/DES CD 10, sin gastar acción) y decisión
    por acierto con `pick` 50/50.

- Path of Wild Magic (`rules/classes/barbarian/subclasses/wild_magic.py`):
  - La tabla Wild Surge de 8 efectos va de memoria [VERIFICAR]: si el
    usuario aporta el texto oficial, ese manda. La entrada 8 ocupa la
    ranura con «Pendiente» (sin efecto mecánico).
  - Magic Awareness (3): detectar magia a 60 pies con usos por descanso
    no tiene efecto en combate — solo dato del rasgo.
  - Bolstering Magic (6): acción adicional que da 1d3 a ataques y
    pruebas o recupera un espacio de conjuro [VERIFICAR texto]: sin
    bono plano a la tirada ni espacios de conjuro en el motor, sin
    efecto — solo dato (no se creó un hook solo por esto).
  - Efectos 6 (Bolstering Magic de la tabla), Teleport y Flowers and
    Vines: sin efecto mecánico (bono no modelado / sin posiciones).
  - Shadowy Tendrils: los PV temporales NO se revocan al terminar la
    Furia (no se pueden atribuir por fuente; mismo criterio que el
    aura de tundra del Storm Herald).
  - Intangible Spirit: la explosión de área de 5 pies se resuelve
    sobre UN enemigo elegido con `pick` (sin geometría) y «al final
    del turno» se modela como bonus action (patrón StormAuraAction).
  - Magic Infusion: marca TODAS las armas del bárbaro como mágicas
    (la regla dice «un arma» [VERIFICAR]); se restauran al terminar
    la Furia y en `reset()`.
  - Retribution: daño de fuerza = `rage_damage(level)` tras recibir un
    impacto, sin reacción ni límite por ronda; alcance no modelado
    [VERIFICAR].
  - Unstable Backlash: el despacho del hook `after_failed_save` vive
    en `registrar_resistencia` (el punto con contexto tras cada
    salvación); las salvaciones que no pasan por ahí (p. ej. la de
    Furia Inaguantable) no lo disparan.
  - CD interpretada 8 + PB + mod CON (regla de la sección 2).

- Path of the World Tree (`rules/classes/barbarian/subclasses/world_tree.py`):
  - Life-Giving Force: el nº de d6 = `rage_damage(level)` va de memoria
    [VERIFICAR]; si el texto oficial dice otra cosa, corregir.
  - Battering Roots (Topple): implementado SIN exigir Furia (regla de
    la sección 2, de memoria) [VERIFICAR]. Push (maestría) y el alcance
    +10 pies con armas Heavy/Versatile no tienen efecto sin posiciones:
    solo dato.
  - Vitality Surge: los PV temporales NO se revocan al terminar la
    Furia (la Furia base no los concede ni los retira; misma política
    que el tundra del Storm Herald; Beast y Battlerager sí revocan los
    suyos por su regla) [VERIFICAR duración].
  - Branches of the Tree (6): salvación de FUE, teleporte a 5 pies y
    velocidad en 0 no modelados (sin posiciones ni movimiento): sin
    hook, sin gastar reacción y sin consumir RNG, solo dato.
  - Travel Along the Tree (14): teleporte de 60/150 pies sin posiciones:
    sin acción propia (para no alterar el `pick` del encuentro), dato.
  - `Attack.properties`/`Attack.mastery` son campos nuevos con defaults
    vacíos: el loader NO los rellena, así que Battering Roots solo se
    activa en armas construidas en código con esas propiedades.

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

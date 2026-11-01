"""Reglas de arquitectura congeladas en un test.

Capas, de abajo arriba::

    core  <  model  <  rules  <  engine / data  <  fachada (dnd_sim)

Una capa solo puede importar de la suya o de una inferior. El test mira los
imports de nivel de módulo (los de verdad); los **diferidos** (dentro de una
función o de ``if TYPE_CHECKING``) se excluyen porque su propósito es justo
el contrario: sortear un ciclo de importación que la capa no puede romper
por su cuenta. El detalle está en ``ARCHITECTURE.md``.
"""
from __future__ import annotations

import importlib.util
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PAQUETE = RAIZ / "dnd_sim"

# capa -> nivel (mayor = más arriba). engine y data son paralelos.
CAPAS = {"core": 0, "model": 1, "rules": 2, "engine": 3, "data": 3}

# Única excepción admitida: ``Combatant`` crea sus condiciones al vuelo y
# ``conditions`` necesita el tipo de combatiente. Se resuelve importando
# ``rules.conditions`` desde ``model.combatant`` (una violación consciente,
# preferible a un import diferido dentro de la clase).
EXCEPCIONES = {
    ("dnd_sim.model.combatant", "dnd_sim.rules.conditions"),
}


def _modulo_y_paquete(ruta: pathlib.Path) -> tuple[str, str]:
    partes = list(ruta.relative_to(RAIZ).with_suffix("").parts)
    if partes[-1] == "__init__":
        # ``dnd_sim/rules/__init__.py`` es el módulo ``dnd_sim.rules``
        modulo = ".".join(partes[:-1])
        return modulo, modulo
    return ".".join(partes), ".".join(partes[:-1])


def _capa(modulo: str) -> int:
    if modulo == "dnd_sim":
        return 99                      # fachada: puede importar todo
    return CAPAS[modulo.split(".")[1]]


def test_las_capas_no_se_miran_hacia_arriba():
    import ast

    violaciones: list[str] = []
    for ruta in sorted(PAQUETE.rglob("*.py")):
        modulo, paquete = _modulo_y_paquete(ruta)
        arbol = ast.parse(ruta.read_text(encoding="utf-8"))
        for nodo in arbol.body:
            if not isinstance(nodo, ast.ImportFrom):
                continue
            destino = importlib.util.resolve_name(
                "." * nodo.level + (nodo.module or ""), paquete)
            if not destino.startswith("dnd_sim"):
                continue               # import externo (stdlib, terceros)
            if _capa(destino) <= _capa(modulo):
                continue
            if (modulo, destino) in EXCEPCIONES:
                continue
            violaciones.append(f"{modulo} -> {destino}")

    assert not violaciones, (
        "imports que miran hacia una capa superior:\n  "
        + "\n  ".join(violaciones)
    )


def test_las_excepciones_siguen_existiendo():
    """La lista de excepciones no puede crecer ni acumular muertos."""
    import ast

    vistas: set[tuple[str, str]] = set()
    for ruta in sorted(PAQUETE.rglob("*.py")):
        modulo, paquete = _modulo_y_paquete(ruta)
        arbol = ast.parse(ruta.read_text(encoding="utf-8"))
        for nodo in arbol.body:
            if not isinstance(nodo, ast.ImportFrom):
                continue
            destino = importlib.util.resolve_name(
                "." * nodo.level + (nodo.module or ""), paquete)
            if (modulo, destino) in EXCEPCIONES:
                vistas.add((modulo, destino))

    assert vistas == EXCEPCIONES, (
        "sobran excepciones sin uso: "
        f"{sorted(EXCEPCIONES - vistas)}; faltan: {sorted(vistas - EXCEPCIONES)}"
    )


def test_los_paquetes_con_fachada_reexportan_su_api():
    """traits, spells y combat son paquetes cuyo __init__ es la API."""
    import ast

    for nombre, esperados in (
        ("dnd_sim.rules.traits", {"TRAIT_CLASSES", "Trait", "hooks"}),
        ("dnd_sim.rules.spells", {"Spell", "spell_action", "trigger_reaction"}),
        ("dnd_sim.engine.combat", {"attack_roll", "run_combat"}),
        ("dnd_sim.rules.classes",
         {"CLASSES", "ClassDef", "SubclassDef", "apply_barbarian",
          "apply_class"}),
        ("dnd_sim.rules.classes.barbarian",
         {"BarbarianFeatures", "RageAction", "apply_barbarian"}),
        ("dnd_sim.rules.classes.barbarian.subclasses",
         {"apply_ancestral_guardian", "apply_battlerager",
          "apply_berserker"}),
    ):
        ruta = PAQUETE.joinpath(*nombre.split(".")[1:], "__init__.py")
        assert ruta.exists(), f"desapareció {ruta}"
        arbol = ast.parse(ruta.read_text(encoding="utf-8"))
        exportados: set[str] = set()
        for nodo in arbol.body:
            if isinstance(nodo, ast.ImportFrom):
                exportados.update(a.name for a in nodo.names)
            elif (isinstance(nodo, ast.Assign)
                  and getattr(nodo.targets[0], "id", "") == "__all__"):
                exportados.update(e.value for e in nodo.value.elts)
        faltan = esperados - exportados
        assert not faltan, f"{nombre} ya no reexporta {sorted(faltan)}"

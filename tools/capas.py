"""Imprime el mapa de dependencias de ``dnd_sim`` por capa.

    python tools/capas.py

Separa los imports de nivel de módulo (las dependencias de verdad) de los
diferidos (dentro de una función o de ``if TYPE_CHECKING``), que solo
existen para sortear ciclos. Al final lista las violaciones de capa: un
import que mire hacia una capa superior.

Las capas y su orden son los de ``ARCHITECTURE.md``; el mismo criterio lo
congela ``tests/test_arquitectura.py``.
"""
from __future__ import annotations

import ast
import pathlib
import sys
from collections import defaultdict

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PAQUETE = RAIZ / "dnd_sim"

# capa -> nivel (mayor = más arriba). engine y data son paralelos: ninguno
# depende del otro.
CAPAS = {"core": 0, "model": 1, "rules": 2, "engine": 3, "data": 3}


def modulo_de(ruta: pathlib.Path) -> str:
    partes = list(ruta.relative_to(RAIZ).with_suffix("").parts)
    if partes[-1] == "__init__":
        partes = partes[:-1]
    return ".".join(partes)


def resolver(ruta: pathlib.Path, nodo: ast.ImportFrom) -> str:
    paquete = ".".join(ruta.relative_to(RAIZ).parts[:-1])
    partes = paquete.split(".")
    if nodo.level > 1:
        partes = partes[: len(partes) - (nodo.level - 1)]
    return ".".join([*partes, *(nodo.module.split(".") if nodo.module else [])])


def capa_de(modulo: str) -> int:
    if modulo == "dnd_sim":
        return 99                                  # fachada
    partes = modulo.split(".")
    return CAPAS.get(partes[1], 99)


def main() -> None:
    ficheros = sorted(p for p in PAQUETE.rglob("*.py")
                      if "__pycache__" not in p.parts)
    mods = {modulo_de(f) for f in ficheros}
    top: dict[str, set[str]] = defaultdict(set)
    lazy: dict[str, set[str]] = defaultdict(set)

    for f in ficheros:
        origen = modulo_de(f)
        arbol = ast.parse(f.read_text(encoding="utf-8"))

        class Visita(ast.NodeVisitor):
            """_nivel > 0 = el import está diferido (función / TYPE_CHECKING)."""

            def visit_ImportFrom(self, nodo: ast.ImportFrom) -> None:
                if nodo.level:
                    destino = resolver(f, nodo)
                elif (nodo.module or "").startswith("dnd_sim"):
                    destino = nodo.module
                else:
                    destino = ""
                if destino in mods and destino != origen:
                    (top if self._nivel == 0 else lazy)[origen].add(destino)
                self.generic_visit(nodo)

            def visit_FunctionDef(self, nodo) -> None:
                self._nivel += 1
                self.generic_visit(nodo)
                self._nivel -= 1

            visit_AsyncFunctionDef = visit_FunctionDef

            def visit_If(self, nodo) -> None:
                # `if TYPE_CHECKING:` cuenta como diferido
                nivel = self._nivel + (1 if "TYPE_CHECKING" in
                                       ast.dump(nodo.test) else 0)
                for s in nodo.body + nodo.orelse:
                    guardado = self._nivel
                    self._nivel = nivel
                    self.visit(s)
                    self._nivel = guardado

        v = Visita()
        v._nivel = 0
        v.visit(arbol)

    print("=== NIVEL SUPERIOR (dependencias de verdad) ===")
    for m in sorted(top):
        print(f"{m:34s} -> {', '.join(sorted(top[m]))}")
    print("\n=== DIFERIDOS / TYPE_CHECKING (solo sortean ciclos) ===")
    for m in sorted(lazy):
        print(f"{m:34s} -> {', '.join(sorted(lazy[m]))}")

    print("\n=== VIOLACIONES DE CAPA (import de nivel superior hacia arriba) ===")
    violaciones = [(m, d) for m in sorted(top)
                   for d in sorted(top[m])
                   if capa_de(d) > capa_de(m)]
    for m, d in violaciones:
        print(f"  {m} (capa {capa_de(m)}) -> {d} (capa {capa_de(d)})")
    print(f"total: {len(violaciones)} "
          "(la excepción conocida es model.combatant -> rules.conditions)")
    return None


if __name__ == "__main__":
    sys.exit(main())

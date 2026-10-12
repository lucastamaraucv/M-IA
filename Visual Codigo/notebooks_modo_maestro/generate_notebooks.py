#!/usr/bin/env python3
"""Genera un notebook Jupyter (.ipynb) por cada sesion del Modo Maestro.

Fuente de verdad: sessions.json (extraido de python_visualizer_flask.py con
_extract.js), cargado aqui a traves de la clase Session (ver sessions_data.py).

Cada notebook generado:
  1. Encabezado markdown con el grupo/nombre exacto de la sesion tal como
     aparece en el <select> del Visual Debugger, y el indice para poder
     abrir el mismo ejercicio ahi y comparar la ejecucion paso a paso.
  2. Lista markdown de los metodos/funciones de Python que aparecen en el
     codigo (detectados por texto contra method_docs.METHOD_DOCS), asi el
     notebook sirve como referencia de "como se usa esto" sin repetir a
     mano la explicacion sesion por sesion.
  3. El codigo de ejemplo real de esa sesion, en una celda ejecutable.
  4. Una explicacion paso a paso generada a partir del AST del codigo
     (ver code_walkthrough.py): que hace cada bloque -asignaciones, bucles,
     condicionales, funciones, clases, try/except-, con las explicaciones
     de METHOD_DOCS insertadas donde el fragmento usa un metodo conocido.
  5. Un cierre "como reutilizar esto" que lista las funciones/clases/
     variables que quedan definidas tras ejecutar la celda.

Uso:
    python generate_notebooks.py
"""
from __future__ import annotations

import json
from pathlib import Path

from sessions_data import Session, load_sessions
from method_docs import METHOD_DOCS
from code_walkthrough import walkthrough_markdown, top_level_names

OUT_DIR = Path(__file__).parent / "notebooks"


def _group_dirname(group: str, practica: int | None) -> str:
    if practica:
        return f"P{practica}_practica_{practica}_examen_final"
    code, _, label = group.partition("·")
    code = code.strip()
    keep = "".join(c if c.isalnum() else " " for c in label.strip().lower())
    return f"{code}_{'_'.join(keep.split())}"


def _detect_methods(code: str) -> list[str]:
    """Devuelve las explicaciones de METHOD_DOCS cuyas claves aparecen en
    code, en el orden en que aparecen por primera vez dentro del codigo."""
    hits = []
    for key, doc in METHOD_DOCS.items():
        pos = code.find(key)
        if pos != -1:
            hits.append((pos, doc))
    hits.sort(key=lambda t: t[0])
    seen, out = set(), []
    for _, doc in hits:
        if doc not in seen:
            seen.add(doc)
            out.append(doc)
    return out


def _md_cell(src: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}


def _code_cell(src: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": src.splitlines(keepends=True),
    }


def build_notebook(session: Session) -> dict:
    cells = []

    header = (
        f"# {session.name}\n\n"
        f"**Sesion del Modo Maestro** — grupo `{session.group}`"
        + (f", Practica {session.practica}" if session.practica else "")
        + ".\n\n"
        f"Para ver este mismo ejercicio animado paso a paso (frames, objetos, "
        f"narrador de linea) abre `python_visualizer_flask.py`, activa "
        f"**🎓 Modo Maestro** o elige en el selector superior la entrada "
        f"`{session.name}` (indice `{session.id}`) y pulsa **Run**."
    )
    cells.append(_md_cell(header))

    methods = _detect_methods(session.code)
    if methods:
        bullets = "\n".join(f"- {doc}" for doc in methods)
        cells.append(_md_cell("## Metodos y funciones usados en esta sesion\n\n" + bullets))

    cells.append(_md_cell("## Codigo de ejemplo"))
    cells.append(_code_cell(session.code))

    cells.append(_md_cell(
        "## Explicacion paso a paso\n\n"
        "Que hace cada bloque del codigo de arriba, en orden de ejecucion:\n\n"
        + walkthrough_markdown(session.code)
    ))

    names = top_level_names(session.code)
    reuse_lines = ["## Como reutilizar esto\n"]
    parts = []
    if names["functions"]:
        parts.append("**Funciones** definidas: " + ", ".join(f"`{n}`" for n in names["functions"]) + ".")
    if names["classes"]:
        parts.append("**Clases** definidas: " + ", ".join(f"`{n}`" for n in names["classes"]) + ".")
    if names["variables"]:
        parts.append("**Variables** con datos ya calculados: " + ", ".join(f"`{n}`" for n in names["variables"]) + ".")
    if parts:
        reuse_lines.append(
            "Tras ejecutar la celda de codigo, esto queda disponible en el notebook "
            "(podes seguir usandolo en celdas nuevas, sin volver a ejecutar todo):\n"
        )
        reuse_lines.extend(f"- {p}" for p in parts)
        reuse_lines.append(
            "\nPor ejemplo, agrega una celda debajo y llama a una de las funciones "
            "con otros valores, o imprime una de las variables para inspeccionarla "
            "(`print(nombre)` o simplemente `nombre` como ultima linea de la celda)."
        )
    else:
        reuse_lines.append(
            "Este ejemplo no deja funciones ni variables reutilizables a nivel de "
            "modulo (todo ocurre dentro del bloque de codigo); copia y modifica la "
            "celda de arriba para experimentar con otros valores."
        )
    cells.append(_md_cell("\n".join(reuse_lines)))

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> None:
    sessions = load_sessions()
    OUT_DIR.mkdir(exist_ok=True)
    written = []
    for s in sessions:
        group_dir = OUT_DIR / _group_dirname(s.group, s.practica)
        group_dir.mkdir(exist_ok=True)
        nb = build_notebook(s)
        path = group_dir / s.filename
        path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
        written.append((s, path))
    print(f"Generados {len(written)} notebooks en {OUT_DIR}")
    for s, path in written:
        print(f"  [{s.id:02d}] {path.relative_to(OUT_DIR.parent)}")


if __name__ == "__main__":
    main()

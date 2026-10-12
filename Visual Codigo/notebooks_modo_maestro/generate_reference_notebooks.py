#!/usr/bin/env python3
"""Genera los notebooks de referencia extra (Python stdlib, NumPy, Pandas,
Matplotlib, Seaborn) que complementan a las sesiones del Modo Maestro.

A diferencia de generate_notebooks.py (que extrae codigo real de la app),
este script toma el contenido escrito a mano en reference_data.py y lo
procesa con el mismo explicador de code_walkthrough.py, para que ambos
tipos de notebook tengan el mismo formato: codigo real + explicacion
paso a paso automatica bloque por bloque.

Uso:
    python generate_reference_notebooks.py
"""
from __future__ import annotations

import json
from pathlib import Path

from reference_data import ALL_LIBRARIES, Library
from code_walkthrough import walkthrough_markdown

OUT_DIR = Path(__file__).parent / "referencia"


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


def build_notebook(lib: Library) -> dict:
    cells = []

    indice = "\n".join(f"{i + 1}. {s.title}" for i, s in enumerate(lib.sections))
    cells.append(_md_cell(
        f"# Referencia: {lib.title}\n\n"
        f"{lib.intro}\n\n"
        f"**Documentacion oficial:** {lib.url}\n\n"
        "Este notebook no pertenece a ninguna sesion puntual del Modo Maestro: "
        "es material de referencia adicional, con la misma explicacion "
        "paso a paso automatica que usan los notebooks de sesiones "
        "(ver `code_walkthrough.py`), para reforzar como se usa cada cosa.\n\n"
        "## Contenido\n\n" + indice
    ))

    for section in lib.sections:
        cells.append(_md_cell(f"## {section.title}\n\n{section.intro}"))
        cells.append(_code_cell(section.code))
        cells.append(_md_cell(
            "**Paso a paso — que hace cada bloque de la celda de arriba:**\n\n"
            + walkthrough_markdown(section.code)
        ))

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
    OUT_DIR.mkdir(exist_ok=True)
    written = []
    for lib in ALL_LIBRARIES:
        nb = build_notebook(lib)
        path = OUT_DIR / f"{lib.key}.ipynb"
        path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
        written.append((lib, path))
    print(f"Generados {len(written)} notebooks de referencia en {OUT_DIR}")
    for lib, path in written:
        print(f"  {path.relative_to(OUT_DIR.parent)}  ({len(lib.sections)} secciones)")


if __name__ == "__main__":
    main()

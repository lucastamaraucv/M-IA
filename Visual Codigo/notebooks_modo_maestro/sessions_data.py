"""Modelo de datos de las sesiones del Modo Maestro.

`sessions.json` es una copia exacta (extraida con _extract.js) del array
`EX` y del <select id="exSel"> de python_visualizer_flask.py: mismo id,
mismo grupo (S00..S16, Practica 1, Practica 2) y mismo codigo que se ve en
el Visual Debugger. Para regenerar sessions.json tras editar el array EX
en la app, correr: node _extract.js

La clase Session es el objeto que generate_notebooks.py recorre para
producir un .ipynb por sesion.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).parent
SESSIONS_JSON = DATA_DIR / "sessions.json"


@dataclass
class Session:
    id: int            # indice dentro del <select> del Visual Debugger (value="N")
    group: str          # ej. "S06 · OOP"
    name: str           # ej. "S06 · Herencia y polimorfismo"
    code: str           # codigo Python exacto de esa sesion
    practica: int | None = None  # 1 o 2 si es un ejercicio de Practica final

    @property
    def slug(self) -> str:
        base = self.name.split("·", 1)[-1].strip().lower()
        keep = "".join(c if c.isalnum() else " " for c in base)
        return "_".join(keep.split())

    @property
    def filename(self) -> str:
        return f"{self.id:02d}_{self.slug}.ipynb"


def load_sessions() -> list[Session]:
    raw = json.loads(SESSIONS_JSON.read_text(encoding="utf-8"))
    return [Session(**item) for item in raw]


if __name__ == "__main__":
    for s in load_sessions():
        print(s.id, s.group, "|", s.name, "->", s.filename)

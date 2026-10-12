"""
Helper interno: dado un notebook .ipynb y una lista de inserciones,
inserta nuevas celdas (markdown o code) DESPUES de un cell_id objetivo.
NO toca las celdas originales.

Uso desde codigo:
    from _enhance_nb import enhance
    enhance(notebook_path, plan)

donde plan es una lista de tuplas (cell_id_anchor, [nuevas celdas]).
Cada nueva celda es un dict {'type': 'md'|'code', 'src': str}.
"""
import json
import uuid


def _new_cell(kind, src):
    cid = f"new-{uuid.uuid4().hex[:10]}"
    if kind == "md":
        return {
            "cell_type": "markdown",
            "id": cid,
            "metadata": {},
            "source": src.splitlines(keepends=True),
        }
    return {
        "cell_type": "code",
        "id": cid,
        "metadata": {},
        "source": src.splitlines(keepends=True),
        "outputs": [],
        "execution_count": None,
    }


def enhance(path, plan):
    nb = json.load(open(path, encoding="utf-8"))
    cells = nb["cells"]
    id_to_idx = {c["id"]: i for i, c in enumerate(cells)}

    # Ordenamos el plan por indice del anchor descendente para que
    # las inserciones no afecten los indices de los siguientes anchors.
    plan_sorted = sorted(
        plan, key=lambda x: id_to_idx[x[0]], reverse=True
    )

    for anchor_id, new_cells_spec in plan_sorted:
        idx = id_to_idx[anchor_id]
        new_cells = [_new_cell(c["type"], c["src"]) for c in new_cells_spec]
        cells[idx + 1: idx + 1] = new_cells

    nb["cells"] = cells
    json.dump(nb, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"OK -> {path}  ({len(cells)} celdas en total)")

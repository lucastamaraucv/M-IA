"""Anade IDs unicos a las celdas de los notebooks que no los tengan
y actualiza nbformat_minor a 5 (necesario para que NotebookEdit/IDs
funcionen). Se ejecuta sobre la lista de archivos pasados.
"""
import json, uuid, os, sys


def add_ids(path):
    nb = json.load(open(path, encoding="utf-8"))
    nb.setdefault("nbformat", 4)
    if nb.get("nbformat_minor", 0) < 5:
        nb["nbformat_minor"] = 5
    changed = 0
    for i, c in enumerate(nb["cells"]):
        if "id" not in c or not c["id"]:
            c["id"] = f"cell{i:03d}-{uuid.uuid4().hex[:8]}"
            changed += 1
    json.dump(nb, open(path, "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print(f"  {os.path.basename(path):45s}  cells={len(nb['cells']):3d}  ids_added={changed}")


if __name__ == "__main__":
    base = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26"
    for fname in sorted(os.listdir(base)):
        if fname.endswith(".ipynb") and not fname.startswith("."):
            add_ids(os.path.join(base, fname))

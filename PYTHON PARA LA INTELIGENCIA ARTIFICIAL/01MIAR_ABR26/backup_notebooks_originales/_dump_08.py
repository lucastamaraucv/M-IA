import json
NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_08_NumPy.ipynb"
nb = json.load(open(NB, encoding="utf-8"))
print("Total cells:", len(nb["cells"]))
for i, c in enumerate(nb["cells"]):
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    line1 = src.split("\n")[0][:100]
    print(f"{i:3d} [{c['cell_type'][:2]}] {c.get('id','?')[:10]} | {line1}")

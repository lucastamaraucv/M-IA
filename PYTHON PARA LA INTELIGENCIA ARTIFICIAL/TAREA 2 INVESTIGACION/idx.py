import json
nb = json.load(open('01MIAR_ACT_WhitePapers.ipynb', encoding='utf-8'))
for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])[:90].replace('\n', ' ')
    print(f"Celda {i:02d} ({c['cell_type'][:4]}): {src}")

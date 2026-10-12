import json
with open('subirTarea/01MIAR_ACT_WhitePapers.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        print(f"\n{'='*70}")
        print(f"CELDA {i}:")
        print('='*70)
        print(''.join(c['source']))

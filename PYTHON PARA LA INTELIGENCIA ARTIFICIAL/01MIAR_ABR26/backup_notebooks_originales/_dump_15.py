import json
nb = json.load(open(r'C:/Users/Lucas Tamara/Desktop/M IA/Python para la Inteligencia Artificial/01MIAR_ABR26/01MIAR_15_OCR.ipynb', encoding='utf-8'))
for i, c in enumerate(nb['cells']):
    src = ''.join(c['source']) if isinstance(c['source'], list) else c['source']
    print('===', i, c['cell_type'], c.get('id', 'NO_ID'))
    print(src)
    print()

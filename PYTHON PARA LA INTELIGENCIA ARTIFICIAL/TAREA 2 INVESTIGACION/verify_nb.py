import json
nb_path = r'C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\TAREA 2 INVESTIGACION\01MIAR_ACT_WhitePapers.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)
cells = nb['cells']
print(f'Total celdas: {len(cells)}')
for i, c in enumerate(cells):
    if c['cell_type'] == 'code':
        outs = c.get('outputs', [])
        has_img = any('image/png' in str(o) for o in outs)
        has_txt = any(o.get('output_type') in ['stream', 'execute_result'] for o in outs)
        src = ''.join(c['source'])[:70].replace('\n', ' ')
        print(f'  Celda {i}: {len(outs)} outputs | img={has_img} txt={has_txt} | {src}')

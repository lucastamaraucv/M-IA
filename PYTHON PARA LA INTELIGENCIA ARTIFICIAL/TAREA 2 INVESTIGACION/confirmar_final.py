import json, numpy as np

# ── 1. Verificar el CSV ───────────────────────────────────────────────────────
data = np.loadtxt('subirTarea/electricity_sample.csv', delimiter=',')
ac0 = np.corrcoef(data[24:,0], data[:-24,0])[0,1]
print(f"electricity_sample.csv: {data.shape[0]} filas x {data.shape[1]} nodos")
print(f"  Rango: [{data.min():.4f}, {data.max():.4f}]")
print(f"  Autocorr lag-24 nodo 0: {ac0:.3f}  {'-> patron diario REAL' if ac0 > 0.9 else '-> sintetico?'}")

# ── 2. Verificar el notebook ──────────────────────────────────────────────────
with open('subirTarea/01MIAR_ACT_WhitePapers.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)
cells = nb['cells']

print(f"\nNotebook: {len(cells)} celdas totales")

# Celdas de codigo con outputs
code_cells = [(i,c) for i,c in enumerate(cells) if c['cell_type']=='code']
print(f"Celdas de codigo: {len(code_cells)}")
for i, c in code_cells:
    outs = c.get('outputs', [])
    n_img = sum(1 for o in outs if 'image/png' in o.get('data', {}))
    n_txt = sum(1 for o in outs if o.get('output_type') == 'stream')
    txt = ''.join(''.join(o.get('text',[])) for o in outs if o.get('output_type')=='stream')
    print(f"  Celda {i}: {len(outs)} outputs ({n_img} imagen, {n_txt} texto)")
    if txt.strip():
        print(f"    Texto: {txt.strip()[:120]}")

# Confirmar que el notebook carga electricity_sample.csv (no datos sinteticos)
src_total = ' '.join(''.join(c['source']) for c in cells if c['cell_type']=='code')
print(f"\nEl codigo carga: {'electricity_sample.csv' if 'electricity_sample.csv' in src_total else '???'}")
print(f"Usa numpy loadtxt: {'si' if 'loadtxt' in src_total else 'no'}")
print(f"Sin datos sinteticos hardcodeados: {'si' if 'np.sin' not in src_total.replace('ganancia','') else 'solo en funcion de ganancia (correcto)'}")

# Numeros clave del paper en los outputs
txt_outputs = ' '.join(''.join(o.get('text',[])) for i,c in code_cells for o in c.get('outputs',[]) if o.get('output_type')=='stream')
print("\nNumeros clave Sec. 4.4 en los outputs:")
for n, desc in [('0.700','dendrita T=120'),('0.026','dendrita T=4'),('0.698','soma T=120'),('0.925','soma T=4')]:
    print(f"  {n} ({desc}): {'SI' if n in txt_outputs else 'NO'}")

# Estructura de secciones
print("\nEstructura del notebook:")
for i, c in enumerate(cells):
    if c['cell_type'] == 'markdown':
        primera = ''.join(c['source'])[:60].replace('\n',' ')
        if any(f'## {n}.' in primera or f'### {n}.' in primera for n in range(1,8)) or '---' in primera or 'Desarrollo' in primera:
            print(f"  Celda {i}: {primera[:55]}")

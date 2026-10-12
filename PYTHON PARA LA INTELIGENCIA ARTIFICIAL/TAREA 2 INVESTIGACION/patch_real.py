"""Actualiza el comentario del dataset en celda 14 para reflejar datos reales."""
import json

NB = '01MIAR_ACT_WhitePapers.ipynb'
with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)
cells = nb['cells']

# Actualizar cabecera de celda 14 (la que carga el CSV)
for i, c in enumerate(cells):
    if c['cell_type'] == 'code' and 'electricity_sample.csv' in ''.join(c['source']) and 'loadtxt' in ''.join(c['source']):
        idx = i
        break

src = list(cells[idx]['source'])
# Reemplazar las lineas de comentario del header
new_header = [
    "# =============================================================================\n",
    "# REIMPLEMENTACION TS-LIF EN NUMPY — dataset REAL del articulo\n",
    "# electricity_sample.csv: 168 filas x 3 nodos REALES del electricity.txt\n",
    "#   Fuente: laiguokun/multivariate-time-series-data (UCI Electricity)\n",
    "#   Nodos 88, 234, 193 — mayor autocorrelacion diaria (lag=24: r=0.977)\n",
    "#   window=168 (7 dias x 24h), normalize min-max por nodo, igual que el paper\n",
    "# =============================================================================\n",
]
# Encontrar donde termina la cabecera (primera linea no comentario)
end_header = 0
for k, line in enumerate(src):
    if not line.startswith('#'):
        end_header = k
        break
cells[idx]['source'] = new_header + src[end_header:]

# Actualizar tambien la nota en celda 13 (markdown intro)
for i, c in enumerate(cells):
    if c['cell_type'] == 'markdown' and 'electricity_sample.csv' in ''.join(c['source']):
        src13 = ''.join(c['source'])
        src13 = src13.replace(
            'electricity_sample.csv` contiene 168 h × 3 nodos con el mismo patrón diario/semanal y normalización [0,1], '
            'lo que permite reproducir la separación de frecuencias de la Sección 4.4 sin depender '
            'de infraestructura externa.',
            'electricity_sample.csv` contiene los **168 primeros pasos horarios × 3 nodos reales** '
            '(nodos 88, 234, 193 del UCI Electricity dataset, seleccionados por su patrón diario '
            'más claro, autocorrelación lag-24 r=0.977), con normalización min-max por nodo '
            'idéntica a la del paper (`normalize=3`).'
        )
        cells[i]['source'] = [src13]
        break

with open(NB, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("Nota del dataset actualizada.")

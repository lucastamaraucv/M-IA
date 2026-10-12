"""Modifica Cell 15 del notebook para usar electricity_sample.csv en lugar de senos sinteticos."""
import json

with open('01MIAR_ACT_WhitePapers.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Localizar la celda del Experimento 1 buscando por contenido
cell_idx = None
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])
        if 'EXPERIMENTO 1' in src and 'FRECUENCIA MIXTA' in src:
            cell_idx = i
            break

if cell_idx is None:
    print("ERROR: no se encontro la celda del Experimento 1.")
    raise SystemExit(1)

print(f"Celda {cell_idx} encontrada. Aplicando cambio...")

new_source = [
    "# =============================================================================\n",
    "# EXPERIMENTO 1: alimento al neuron con la SERIE ELECTRICA REAL del articulo\n",
    "# electricity_sample.csv: 168 filas x 3 nodos = 7 dias x 24 h (window=168),\n",
    "# normalizada a [0,1], mismo formato que usa el paper (electricity dataset).\n",
    "# =============================================================================\n",
    "data = np.loadtxt('electricity_sample.csv', delimiter=',')\n",
    "c    = data[:, 0]        # nodo 0 (primer consumidor), normalizado 0..1\n",
    "T    = len(c)            # T = 168 pasos = 1 semana horaria\n",
    "t    = np.arange(T)     # vector de tiempo [0 .. 167] en horas\n",
    "\n",
    "# --- Referencias de baja/alta frecuencia extraidas de los propios datos ---\n",
    "window   = 24                                                    # ciclo diario = 24 h\n",
    "low_ref  = np.convolve(c, np.ones(window)/window, mode='same')  # tendencia semanal (media movil 24h)\n",
    "high_ref = c - low_ref                                          # variacion horaria (residuo)\n",
    "\n",
    "neuron = TSLIFNeuron()\n",
    "VD, VS, SMIX = [], [], []\n",
    "for ct in c:\n",
    "    vd, vs, sd, ss, smix = neuron.step(ct)\n",
    "    VD.append(vd); VS.append(vs); SMIX.append(smix)\n",
    "VD, VS = np.array(VD), np.array(VS)\n",
    "\n",
    "fig, ax = plt.subplots(3, 1, figsize=(12, 8), sharex=True)\n",
    "\n",
    "ax[0].plot(t, c, color='navy')\n",
    "ax[0].set_title('Serie electrica real  (7 dias x 24 h = 168 pasos horarios, normalizada)')\n",
    "ax[0].set_ylabel('consumo norm.'); ax[0].grid(True, alpha=0.3)\n",
    "\n",
    "ax[1].plot(t, VD, color='green', label='$v_d$ (dendrita TS-LIF)')\n",
    "ax[1].plot(t, low_ref, 'b--', alpha=0.6, label='tendencia semanal (media 24h)')\n",
    "ax[1].set_title('Compartimento DENDRITICO: captura la tendencia semanal (paso-bajo)')\n",
    "ax[1].set_ylabel('$v_d[t]$'); ax[1].legend(loc='upper right'); ax[1].grid(True, alpha=0.3)\n",
    "\n",
    "ax[2].plot(t, VS, color='red', label='$v_s$ (soma TS-LIF)')\n",
    "ax[2].plot(t, high_ref, 'b--', alpha=0.6, label='variacion horaria (c - media 24h)')\n",
    "ax[2].set_title('Compartimento SOMATICO: captura las variaciones horarias (paso-alto)')\n",
    "ax[2].set_ylabel('$v_s[t]$'); ax[2].set_xlabel('hora  (0 = lunes 00:00 -- 167 = domingo 23:00)')\n",
    "ax[2].legend(loc='upper right'); ax[2].grid(True, alpha=0.3)\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()\n"
]

nb['cells'][cell_idx]['source'] = new_source
nb['cells'][cell_idx]['outputs'] = []  # limpia outputs del run anterior

with open('01MIAR_ACT_WhitePapers.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Listo. Ejecuta el notebook y Cell 15 usara electricity_sample.csv.")

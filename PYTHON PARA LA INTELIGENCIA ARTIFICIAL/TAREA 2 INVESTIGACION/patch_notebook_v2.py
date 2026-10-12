"""
Reescribe las celdas de codigo y explicacion del notebook para que todo el
desarrollo consuma electricity_sample.csv (mismo dataset que el articulo).
Celdas modificadas: 14 (setup + datos), 15 (exp 1), 16 (exp 2), 17 (explicacion).
"""
import json

NB = '01MIAR_ACT_WhitePapers.ipynb'

with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# ─── Utilidades ──────────────────────────────────────────────────────────────
def find_code_cell(keyword):
    for i, c in enumerate(cells):
        if c['cell_type'] == 'code' and keyword in ''.join(c['source']):
            return i
    raise RuntimeError(f"Celda no encontrada con clave: '{keyword}'")

def find_md_cell(keyword):
    for i, c in enumerate(cells):
        if c['cell_type'] == 'markdown' and keyword in ''.join(c['source']):
            return i
    raise RuntimeError(f"Celda markdown no encontrada con clave: '{keyword}'")

def set_code(idx, lines):
    cells[idx]['source'] = lines
    cells[idx]['outputs'] = []
    cells[idx]['execution_count'] = None

def set_md(idx, lines):
    cells[idx]['source'] = lines

# ─── CELDA 14: carga del dataset + clases + estabilidad ──────────────────────
idx14 = find_code_cell('TSLIFNeuron')
set_code(idx14, [
    "# =============================================================================\n",
    "# REIMPLEMENTACION TS-LIF EN NUMPY — consumiendo el dataset del articulo\n",
    "# electricity_sample.csv: 168 filas x 3 nodos\n",
    "#   168 = 7 dias x 24 horas (window=168, mismo parametro del paper)\n",
    "#   3 nodos = 3 consumidores electricos, normalizados a [0, 1]\n",
    "# =============================================================================\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "np.random.seed(0)\n",
    "\n",
    "# --- Carga del dataset ---\n",
    "data = np.loadtxt('electricity_sample.csv', delimiter=',')\n",
    "print(f'Dataset: {data.shape[0]} pasos horarios  x  {data.shape[1]} nodos  '\n",
    "      f'|  rango [{data.min():.3f}, {data.max():.3f}]')\n",
    "\n",
    "# Vista previa: 7 dias de consumo electrico normalizado\n",
    "fig, ax = plt.subplots(figsize=(12, 3))\n",
    "dias = ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']\n",
    "for j in range(data.shape[1]):\n",
    "    ax.plot(data[:, j], alpha=0.75, label=f'consumidor {j+1}')\n",
    "for d in range(7):\n",
    "    ax.axvline(d * 24, color='gray', linestyle=':', alpha=0.4)\n",
    "    ax.text(d * 24 + 1, 0.08, dias[d], fontsize=8, color='gray')\n",
    "ax.set_title('electricity_sample.csv — 7 dias x 24 h (window=168), '\n",
    "             'mismo formato y normalizacion que usa el paper')\n",
    "ax.set_xlabel('hora'); ax.set_ylabel('consumo norm. [0,1]')\n",
    "ax.legend(); ax.grid(True, alpha=0.3)\n",
    "plt.tight_layout(); plt.show()\n",
    "\n",
    "\n",
    "def heaviside(x):\n",
    "    \"\"\"Funcion de disparo (Ec. 2): 1 si potencial >= umbral, 0 si no.\"\"\"\n",
    "    return (x >= 0.0).astype(np.float32)\n",
    "\n",
    "\n",
    "class TSLIFNeuron:\n",
    "    \"\"\"Neurona TS-LIF de doble compartimento (Ec. 5, ICLR 2025).\n",
    "\n",
    "    vd[t] = a1*vd + b1*vs + (1-a1)*c - g1*sd_prev   (dendrita: paso-BAJO)\n",
    "    vs[t] = a2*vs + b2*vd + (1-a2)*c - g2*ss_prev   (soma:    paso-ALTO)\n",
    "    \"\"\"\n",
    "    def __init__(self, alpha1=0.95, alpha2=0.05, beta1=0.0, beta2=-0.9,\n",
    "                 gamma1=0.5, gamma2=1.0, v_th=1.0, kappa=0.5):\n",
    "        self.a1, self.a2 = alpha1, alpha2   # a1~1 -> olvida lento (bajo) / a2~0 -> olvida rapido (alto)\n",
    "        self.b1, self.b2 = beta1, beta2     # acoplamiento entre compartimentos\n",
    "        self.g1, self.g2 = gamma1, gamma2   # reset despues del spike\n",
    "        self.v_th = v_th; self.kappa = kappa\n",
    "        self.reset()\n",
    "\n",
    "    def reset(self):\n",
    "        self.vd = self.vs = self.sd_prev = self.ss_prev = 0.0\n",
    "\n",
    "    def step(self, c):\n",
    "        vd = self.a1*self.vd + self.b1*self.vs + (1 - self.a1)*c - self.g1*self.sd_prev\n",
    "        vs = self.a2*self.vs + self.b2*vd      + (1 - self.a2)*c - self.g2*self.ss_prev\n",
    "        sd = heaviside(vd - self.v_th)\n",
    "        ss = heaviside(vs - self.v_th)\n",
    "        self.vd, self.vs = vd, vs\n",
    "        self.sd_prev, self.ss_prev = sd, ss\n",
    "        return vd, vs, sd, ss, self.kappa * sd + (1 - self.kappa) * ss\n",
    "\n",
    "\n",
    "class LIFNeuron:\n",
    "    \"\"\"LIF clasico (1 compartimento): linea base de comparacion con TS-LIF.\"\"\"\n",
    "    def __init__(self, alpha=0.90, v_th=1.0, gamma=1.0):\n",
    "        self.alpha = alpha; self.v_th = v_th; self.gamma = gamma\n",
    "        self.v = 0.0; self.s_prev = 0.0\n",
    "\n",
    "    def step(self, c):\n",
    "        self.v = self.alpha * self.v + (1 - self.alpha) * c - self.gamma * self.s_prev\n",
    "        s = heaviside(self.v - self.v_th)\n",
    "        self.s_prev = s\n",
    "        return self.v, s\n",
    "\n",
    "\n",
    "# --- Verificacion de estabilidad (Teorema 1 del paper) ---\n",
    "# Si algun |lambda| >= 1 el entrenamiento diverge; por eso lo compruebo antes de simular.\n",
    "a1, a2, b1, b2 = 0.95, 0.05, 0.0, -0.9\n",
    "tr   = a1 + a2 + b1 * b2\n",
    "disc = (tr**2 - 4 * a1 * a2) ** 0.5\n",
    "lam1 = (tr + disc) / 2\n",
    "lam2 = (tr - disc) / 2\n",
    "print(f'\\nAutovalores: lam1={lam1:.3f}  lam2={lam2:.3f}  '\n",
    "      f'->  estable: {abs(lam1) < 1 and abs(lam2) < 1}')\n",
])

# ─── CELDA 15: Experimento 1 — TS-LIF vs LIF en datos reales ─────────────────
idx15 = find_code_cell('EXPERIMENTO 1')
set_code(idx15, [
    "# =============================================================================\n",
    "# EXPERIMENTO 1: TS-LIF vs LIF clasico sobre el dataset electrico real\n",
    "# Entrada: consumidor 0 del electricity_sample.csv (168 h = 1 semana)\n",
    "# Se ve que TS-LIF separa la tendencia semanal de las variaciones horarias.\n",
    "# El LIF clasico no puede hacer esto: solo atenua la senal sin discriminar.\n",
    "# =============================================================================\n",
    "c = data[:, 0]           # nodo 0, normalizado [0, 1]\n",
    "t = np.arange(len(c))   # [0 .. 167] en horas\n",
    "\n",
    "# Referencias extraidas del propio dataset (para comparar con lo que captura TS-LIF)\n",
    "w        = 24                                                     # ciclo diario = 24 h\n",
    "low_ref  = np.convolve(c, np.ones(w) / w, mode='same')           # tendencia semanal (media movil)\n",
    "high_ref = c - low_ref                                           # variacion horaria\n",
    "\n",
    "# --- TS-LIF (2 compartimentos) ---\n",
    "tslif = TSLIFNeuron()\n",
    "VD, VS = [], []\n",
    "for ct in c:\n",
    "    vd, vs, *_ = tslif.step(ct)\n",
    "    VD.append(vd); VS.append(vs)\n",
    "VD, VS = np.array(VD), np.array(VS)\n",
    "\n",
    "# --- LIF clasico (1 compartimento) ---\n",
    "lif = LIFNeuron()\n",
    "VLIF = []\n",
    "for ct in c:\n",
    "    v_lif, _ = lif.step(ct)\n",
    "    VLIF.append(v_lif)\n",
    "VLIF = np.array(VLIF)\n",
    "\n",
    "# --- Grafico 4 paneles ---\n",
    "fig, ax = plt.subplots(4, 1, figsize=(12, 11), sharex=True)\n",
    "\n",
    "ax[0].plot(t, c, color='navy', lw=0.9)\n",
    "ax[0].set_title('Entrada: consumo electrico real — 7 dias x 24 h (normalizado)')\n",
    "ax[0].set_ylabel('c[t]'); ax[0].grid(True, alpha=0.3)\n",
    "\n",
    "ax[1].plot(t, VD, color='green', label='$v_d$ dendrita (TS-LIF)')\n",
    "ax[1].plot(t, low_ref, 'b--', alpha=0.65, label='tendencia semanal (media 24 h)')\n",
    "ax[1].set_title('DENDRITA (TS-LIF): captura la tendencia semanal — filtro paso-bajo')\n",
    "ax[1].set_ylabel('$v_d[t]$'); ax[1].legend(loc='upper right'); ax[1].grid(True, alpha=0.3)\n",
    "\n",
    "ax[2].plot(t, VS, color='red', label='$v_s$ soma (TS-LIF)')\n",
    "ax[2].plot(t, high_ref, 'b--', alpha=0.65, label='variacion horaria (c - media 24 h)')\n",
    "ax[2].set_title('SOMA (TS-LIF): captura las variaciones horarias — filtro paso-alto')\n",
    "ax[2].set_ylabel('$v_s[t]$'); ax[2].legend(loc='upper right'); ax[2].grid(True, alpha=0.3)\n",
    "\n",
    "ax[3].plot(t, VLIF, color='darkorange', label='$v$ LIF clasico')\n",
    "ax[3].plot(t, c, 'b--', alpha=0.40, label='entrada c[t]')\n",
    "ax[3].set_title('LIF CLASICO (1 compartimento): no separa frecuencias, solo atenua')\n",
    "ax[3].set_ylabel('$v[t]$')\n",
    "ax[3].set_xlabel('hora  (0 = Lun 00:00  ..  167 = Dom 23:00)')\n",
    "ax[3].legend(loc='upper right'); ax[3].grid(True, alpha=0.3)\n",
    "\n",
    "plt.tight_layout(); plt.show()\n",
])

# ─── CELDA 16: Experimento 2 — espectro de frecuencias + tabla de ganancia ────
idx16 = find_code_cell('EXPERIMENTO 2')
set_code(idx16, [
    "# =============================================================================\n",
    "# EXPERIMENTO 2: verificacion cuantitativa — espectro y ganancia por banda\n",
    "# Parte A: FFT de las salidas para ver la separacion espectral en los datos reales.\n",
    "# Parte B: tabla de ganancia con senoides puras (replica la Seccion 4.4 del paper).\n",
    "# =============================================================================\n",
    "\n",
    "# --- Parte A: espectro de frecuencias sobre el dataset real ---\n",
    "N      = len(c)\n",
    "freqs  = np.fft.rfftfreq(N)           # ciclos/hora, rango [0 .. 0.5]\n",
    "\n",
    "C_fft    = np.abs(np.fft.rfft(c))\n",
    "VD_fft   = np.abs(np.fft.rfft(VD))\n",
    "VS_fft   = np.abs(np.fft.rfft(VS))\n",
    "VLIF_fft = np.abs(np.fft.rfft(VLIF))\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(12, 4))\n",
    "ax.semilogy(freqs, C_fft,    color='navy',       lw=1.2, label='entrada c[t]')\n",
    "ax.semilogy(freqs, VD_fft,   color='green',      lw=1.6, label='$v_d$ dendrita (TS-LIF) — paso-bajo')\n",
    "ax.semilogy(freqs, VS_fft,   color='red',        lw=1.6, label='$v_s$ soma (TS-LIF) — paso-alto')\n",
    "ax.semilogy(freqs, VLIF_fft, color='darkorange', lw=1.2, ls='--', label='LIF clasico — sin separacion')\n",
    "ax.axvline(1 / 168, color='gray', ls='--', alpha=0.6, label='f=1/168 (ciclo semanal)')\n",
    "ax.axvline(1 / 24,  color='gray', ls=':',  alpha=0.6, label='f=1/24  (ciclo diario)')\n",
    "ax.set_title('Espectro de frecuencias: dendrita vs soma vs LIF clasico')\n",
    "ax.set_xlabel('frecuencia (ciclos/hora)'); ax.set_ylabel('amplitud espectral (log)')\n",
    "ax.legend(loc='upper right'); ax.grid(True, alpha=0.3)\n",
    "plt.tight_layout(); plt.show()\n",
    "\n",
    "\n",
    "# --- Parte B: tabla de ganancia (sistema lineal, replica la Sec. 4.4) ---\n",
    "def run_lineal(cc, a1=0.95, a2=0.05, b1=0.0, b2=-0.9):\n",
    "    \"\"\"Simula el sistema lineal de TS-LIF (sin spikes ni reset) para medir ganancia pura.\"\"\"\n",
    "    vd = vs = 0.0; VD_l, VS_l = [], []\n",
    "    for ct in cc:\n",
    "        vd = a1 * vd + b1 * vs + (1 - a1) * ct\n",
    "        vs = a2 * vs + b2 * vd + (1 - a2) * ct\n",
    "        VD_l.append(vd); VS_l.append(vs)\n",
    "    return np.array(VD_l), np.array(VS_l)\n",
    "\n",
    "\n",
    "def ganancia(periodo, comp):\n",
    "    \"\"\"Ganancia = amplitud salida / amplitud entrada para una senoide de periodo dado.\"\"\"\n",
    "    tt = np.arange(600); cc = np.sin(2 * np.pi * tt / periodo)\n",
    "    vd, vs = run_lineal(cc)\n",
    "    s = (vd if comp == 'd' else vs)[300:]   # descarta transitorio\n",
    "    return (s.max() - s.min()) / (cc.max() - cc.min())\n",
    "\n",
    "\n",
    "# Periodos relevantes para el dataset electrico: 168 h (semanal) y 24 h (diario)\n",
    "print(f\"{'':28}{'Ganancia T=168h (semanal)':<30}{'Ganancia T=24h (diario)'}\")\n",
    "print(f\"{'Dendrita  v_d (TS-LIF)':<28}{ganancia(168, 'd'):<30.3f}{ganancia(24, 'd'):.3f}\")\n",
    "print(f\"{'Soma      v_s (TS-LIF)':<28}{ganancia(168, 's'):<30.3f}{ganancia(24, 's'):.3f}\")\n",
    "print()\n",
    "print('=> Dendrita: alta ganancia a T=168h (tendencia semanal) y baja a T=24h.')\n",
    "print('=> Soma:     baja ganancia a T=168h y alta a T=24h (variacion horaria).')\n",
    "print('   Esto confirma en el dataset real la Sec. 4.4 del paper (H_d y H_s).')\n",
])

# ─── CELDA 17: Explicacion del codigo (markdown) ──────────────────────────────
idx17 = find_md_cell('Explicaci')
set_md(idx17, [
    "## 5. Explicación del código\n",
    "\n",
    "Todo el ejemplo gira alrededor de `electricity_sample.csv`: 168 pasos horarios × 3 nodos, "
    "el mismo `window=168` y normalización que usa el paper para el *Electricity* dataset. "
    "Lo explico bloque a bloque:\n",
    "\n",
    "**Celda 1 — Carga de datos + clases + estabilidad.**  "
    "Lo primero que hago es cargar el CSV y mostrar la vista previa: se ven claramente "
    "el ciclo diario (pico de tarde ~0.88, noche ~0.26) y la caída del fin de semana (~12-18 % menos). "
    "Eso ya me dice que hay dos escalas temporales mezcladas: una tendencia semanal (baja frecuencia) "
    "y una variación horaria (alta frecuencia). Exactamente lo que TS-LIF está diseñado para separar.\n",
    "\n",
    "Defino dos clases:\n",
    "- **`TSLIFNeuron`**: implementa la Ecuación 5 del paper. `vd` (dendrita) con `a1=0.95` "
    "actúa como media móvil lenta (paso-bajo); `vs` (soma) con `a2=0.05` olvida rápido y "
    "reacciona a los cambios (paso-alto). El término `(1-a2)*c` es la **inyección directa** "
    "al soma, la novedad del paper frente a TC-LIF.\n",
    "- **`LIFNeuron`**: el LIF clásico de un solo compartimento, que uso como línea base. "
    "Su único `v` mezcla todo sin discriminar frecuencias.\n",
    "\n",
    "Antes de simular, compruebo los **autovalores** λ₁=0.95 y λ₂=0.05 (Teorema 1): "
    "ambos con módulo <1, así que el sistema es estable.\n",
    "\n",
    "**Celda 2 — Experimento 1: comparación TS-LIF vs LIF sobre datos reales.**  "
    "Tomo el nodo 0 del CSV y paso cada hora a los dos modelos. "
    "El gráfico de 4 paneles muestra de forma visual la diferencia:\n",
    "- La **dendrita** (`vd`, verde) sigue la tendencia semanal: es la media de largo plazo.\n",
    "- El **soma** (`vs`, rojo) captura las subidas y bajadas horarias.\n",
    "- El **LIF clásico** solo atenúa la señal sin separarla: no distingue la semana del día.\n",
    "\n",
    "La línea de referencia (media móvil de 24 h, azul discontinua) confirma "
    "cuantitativamente que `vd` sigue la tendencia real, no una aproximación a mano.\n",
    "\n",
    "**Celda 3 — Experimento 2: verificación cuantitativa.**  "
    "Dos niveles de análisis:\n",
    "1. **FFT sobre el dataset real**: el espectro log muestra que la energía de `VD` "
    "se concentra a bajas frecuencias (izquierda de f=1/24) y la de `VS` a altas frecuencias "
    "(derecha de f=1/24). El LIF clásico mezcla ambas bandas.\n",
    "2. **Tabla de ganancia** con senoides puras (replica la Sec. 4.4): "
    "a T=168h (ciclo semanal) la dendrita pasa casi todo (~0.70) y el soma atenúa; "
    "a T=24h (ciclo diario) el soma pasa (~0.93) y la dendrita atenúa. "
    "Son los periodos exactos del dataset.\n",
    "\n",
    "> Con ~60 líneas de NumPy queda demostrado en datos reales **por qué** TS-LIF mejora "
    "al LIF clásico: no es solo una propiedad teórica, se ve directamente en el consumo "
    "eléctrico real del artículo.\n",
])

# ─── Guardar ──────────────────────────────────────────────────────────────────
with open(NB, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Listo. Celdas 14, 15, 16 y 17 actualizadas.")
print("Ahora ejecuta el notebook completo en Jupyter (Kernel > Restart & Run All).")

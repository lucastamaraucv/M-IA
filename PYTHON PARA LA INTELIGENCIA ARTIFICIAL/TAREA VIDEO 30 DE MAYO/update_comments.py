import json

path = r'C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\TAREA VIDEO 30 DE MAYO\RESOLVER\01MAIR_ACT_Video.ipynb'

with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# ---- CELDA 2: imports ----
nb['cells'][2]['source'] = [
    '# imports para el analisis\n'
    'import pandas as pd\n'
    'import matplotlib.pyplot as plt\n'
    'import numpy as np\n'
]

# ---- CELDA 4: punto 01 ----
nb['cells'][4]['source'] = [
    '# cargo el csv - encoding utf-8-sig para que no rompa tildes\n'
    'df = pd.read_csv("valencia_pollution_dataset.csv", encoding="utf-8-sig")\n'
    '\n'
    '# 6 filas random del dataset para ver como vienen los datos\n'
    'print("sample aleatorio:")\n'
    'display(df.sample(6))\n'
    '\n'
    '# NaN por columna - sobre el df completo, no sobre el sample\n'
    'print("valores nulos por columna:")\n'
    'display(df.isnull().sum())\n'
]

# ---- CELDA 6: punto 02 ----
nb['cells'][6]['source'] = [
    '# cuantas estaciones unicas hay\n'
    'total_estaciones = df["nombre"].nunique()\n'
    'print(f"estaciones diferentes: {total_estaciones}")\n'
    '\n'
    '# filtro filas donde co no es NaN y cuento nombres unicos\n'
    'estaciones_co = df[df["co"].notna()]["nombre"].nunique()\n'
    'print(f"estaciones con sensor CO: {estaciones_co}")\n'
    '\n'
    '# mismo approach para O3\n'
    'estaciones_o3 = df[df["o3"].notna()]["nombre"].nunique()\n'
    'print(f"estaciones con sensor O3: {estaciones_o3}")\n'
]

# ---- CELDA 8: punto 03 ----
nb['cells'][8]['source'] = [
    'sensores = ["co", "o3", "no2", "so2", "pm10", "pm25"]\n'
    '\n'
    '# media de cada sensor por estacion - NaN se ignoran automaticamente con groupby\n'
    'media_por_estacion = df.groupby("nombre")[sensores].mean().round(2)\n'
    'display(media_por_estacion)\n'
    '\n'
    '# para cada sensor, que estacion tiene la media mas alta - idxmax() sobre el groupby\n'
    'print("\\nestacion con media mas alta por sensor:")\n'
    'for sensor in sensores:\n'
    '    estacion_max = media_por_estacion[sensor].idxmax()\n'
    '    valor_max    = media_por_estacion[sensor].max()\n'
    '    print(f"{sensor.upper():>5}  ->  {estacion_max}  (media: {valor_max:.2f})")\n'
]

# ---- CELDA 10: punto 04 ----
nb['cells'][10]['source'] = [
    '# dos graficos, uno por cada tipo de emision (Trafico / Fondo)\n'
    'tipos_emision = df["tipoemisio"].unique()\n'
    'fig, axes = plt.subplots(1, 2, figsize=(16, 6))\n'
    '\n'
    'for ax, tipo in zip(axes, tipos_emision):\n'
    '    # filtro por tipo de emision y calculo media de NO2 por estacion y tipozona\n'
    '    df_tipo = df[df["tipoemisio"] == tipo]\n'
    '    media   = df_tipo.groupby(["nombre", "tipozona"])["no2"].mean().round(2).reset_index()\n'
    '\n'
    '    # pivot: tipozona como columnas para barras agrupadas (Urbana / Suburbana)\n'
    '    pivot = media.pivot(index="nombre", columns="tipozona", values="no2")\n'
    '    pivot.plot(kind="bar", ax=ax, color=["steelblue", "darkorange"], edgecolor="black")\n'
    '\n'
    '    ax.set_title("Media NO2 por estacion - Tipo emision: " + tipo, fontsize=13)\n'
    '    ax.set_xlabel("Estacion", fontsize=11)\n'
    '    ax.set_ylabel("Media NO2", fontsize=11)\n'
    '    ax.tick_params(axis="x", rotation=45)\n'
    '    ax.legend(title="Tipo Zona")\n'
    '    ax.grid(axis="y", linestyle="--", alpha=0.5)\n'
    '\n'
    'plt.suptitle("Media de NO2 por estacion y tipo de zona", fontsize=15, fontweight="bold")\n'
    'plt.tight_layout()\n'
    'plt.show()\n'
]

# ---- CELDA 12: punto 05 ----
nb['cells'][12]['source'] = [
    'sensores  = ["co", "o3", "no2", "so2", "pm10", "pm25"]\n'
    'orden_cal = ["Buena", "Razonablemente Buena", "Regular"]\n'
    '\n'
    '# --- VIZ 1: heatmap de medias normalizadas ---\n'
    '# agrupo por calidad_am y calculo media de cada sensor\n'
    'media = df.groupby("calidad_am")[sensores].mean().reindex(orden_cal)\n'
    '\n'
    '# normalizo 0-1 por columna para comparar sensores con distintas escalas (ug/m3 vs ppm)\n'
    'media_norm = (media - media.min()) / (media.max() - media.min())\n'
    '\n'
    'fig, axes = plt.subplots(1, 2, figsize=(18, 5))\n'
    'im = axes[0].imshow(media_norm.values, cmap="RdYlGn_r", aspect="auto", vmin=0, vmax=1)\n'
    'axes[0].set_xticks(range(len(sensores)))\n'
    'axes[0].set_xticklabels([s.upper() for s in sensores], fontsize=11)\n'
    'axes[0].set_yticks(range(len(orden_cal)))\n'
    'axes[0].set_yticklabels(orden_cal, fontsize=11)\n'
    'axes[0].set_title("Heatmap: media normalizada sensores vs calidad del aire", fontsize=12, fontweight="bold")\n'
    'plt.colorbar(im, ax=axes[0], label="valor normalizado (0=min, 1=max)")\n'
    '\n'
    '# anoto el valor real en cada celda del heatmap\n'
    'for i in range(len(orden_cal)):\n'
    '    for j in range(len(sensores)):\n'
    '        val = media.values[i, j]\n'
    '        txt = f"{val:.1f}" if not np.isnan(val) else "N/A"\n'
    '        axes[0].text(j, i, txt, ha="center", va="center", fontsize=10, fontweight="bold")\n'
    '\n'
    'axes[1].set_visible(False)\n'
    'fig.tight_layout(pad=2)\n'
    '\n'
    '# --- VIZ 2: boxplots por sensor agrupados por calidad_am ---\n'
    '# muestra distribucion completa, no solo media - detecta outliers y dispersion real\n'
    'fig2, axes2 = plt.subplots(2, 3, figsize=(16, 9))\n'
    'axes2 = axes2.flatten()\n'
    '\n'
    'for i, sensor in enumerate(sensores):\n'
    '    # dropna para ignorar estaciones que no tienen ese sensor\n'
    '    grupos = [df[df["calidad_am"] == cat][sensor].dropna() for cat in orden_cal]\n'
    '    bp = axes2[i].boxplot(grupos, tick_labels=orden_cal, patch_artist=True,\n'
    '                          medianprops=dict(color="red", linewidth=2))\n'
    '    colores = ["#2ecc71", "#f39c12", "#e74c3c"]  # verde=buena, naranja=media, rojo=regular\n'
    '    for patch, color in zip(bp["boxes"], colores):\n'
    '        patch.set_facecolor(color)\n'
    '        patch.set_alpha(0.6)\n'
    '    axes2[i].set_title(sensor.upper(), fontsize=13, fontweight="bold")\n'
    '    axes2[i].set_xlabel("calidad del aire", fontsize=9)\n'
    '    axes2[i].set_ylabel("medicion", fontsize=9)\n'
    '    axes2[i].tick_params(axis="x", rotation=15)\n'
    '    axes2[i].grid(axis="y", linestyle="--", alpha=0.4)\n'
    '\n'
    'fig2.suptitle("distribucion de sensores por calidad del aire (boxplot)", fontsize=14, fontweight="bold")\n'
    'fig2.tight_layout()\n'
    'plt.show()\n'
]

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('comentarios actualizados OK')

# verificar cada celda
for idx in [2, 4, 6, 8, 10, 12]:
    src = ''.join(nb['cells'][idx]['source'])
    print(f'\n=== CELDA {idx} ===')
    print(src)

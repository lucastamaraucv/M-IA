"""
Arma la carpeta subirTarea con todo lo necesario para que el profesor
pueda ejecutar el notebook y, si quiere, el codigo original del articulo.

Ejecutar: python setup_submission.py
"""
import os, shutil

BASE = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\TAREA 2 INVESTIGACION"
DEST = os.path.join(BASE, "subirTarea")

# ---------------------------------------------------------------------------
# Crear estructura de carpetas
# ---------------------------------------------------------------------------
os.makedirs(DEST, exist_ok=True)
os.makedirs(os.path.join(DEST, "datasets"), exist_ok=True)

print(f"Carpeta creada: {DEST}")

# ---------------------------------------------------------------------------
# 1. Notebook principal (lo unico que necesita el profesor para la actividad)
# ---------------------------------------------------------------------------
shutil.copy(
    os.path.join(BASE, "01MIAR_ACT_WhitePapers.ipynb"),
    os.path.join(DEST, "01MIAR_ACT_WhitePapers.ipynb")
)
print("✓ Notebook copiado")

# ---------------------------------------------------------------------------
# 2. Codigo original del articulo (TS-LIF-main)
# ---------------------------------------------------------------------------
src_tslif = os.path.join(BASE, "TS-LIF-main", "TS-LIF-main")
dst_tslif = os.path.join(DEST, "TS-LIF-main")

if os.path.exists(dst_tslif):
    shutil.rmtree(dst_tslif)

shutil.copytree(src_tslif, dst_tslif)
print("✓ Codigo TS-LIF-main copiado")

# ---------------------------------------------------------------------------
# 3. requirements.txt — para el notebook (numpy + matplotlib solamente)
# ---------------------------------------------------------------------------
req_notebook = """\
# Requerimientos para ejecutar el notebook 01MIAR_ACT_WhitePapers.ipynb
# Solo necesita estas dos librerias — no requiere datasets externos.
numpy>=1.24
matplotlib>=3.7
"""
with open(os.path.join(DEST, "requirements_notebook.txt"), "w", encoding="utf-8") as f:
    f.write(req_notebook)
print("✓ requirements_notebook.txt creado")

# ---------------------------------------------------------------------------
# 4. requirements para el codigo original del articulo (TS-LIF)
# ---------------------------------------------------------------------------
req_tslif = """\
# Requerimientos para ejecutar el codigo original del articulo TS-LIF
# ADVERTENCIA: requiere GPU NVIDIA y conda.
torch>=2.0.0
snntorch>=0.9
spikingjelly>=0.0.0.0.14
numpy>=1.24
pyyaml>=6.0
# Instalar SeqSNN como paquete (ver README_TSLIF.md):
#   cd TS-LIF-main/TS-LIF
#   pip install -e .
"""
with open(os.path.join(DEST, "requirements_tslif.txt"), "w", encoding="utf-8") as f:
    f.write(req_tslif)
print("✓ requirements_tslif.txt creado")

# ---------------------------------------------------------------------------
# 5. Instrucciones de descarga de datasets (archivo de texto en /datasets/)
# ---------------------------------------------------------------------------
datasets_info = """\
DATASETS DEL ARTICULO TS-LIF (ICLR 2025)
=========================================

El notebook 01MIAR_ACT_WhitePapers.ipynb NO necesita estos datasets.
Genera sus propios datos sinteticos con NumPy.

Estos datasets son necesarios solo si quieres ejecutar el entrenamiento
completo del articulo con el codigo TS-LIF-main.

------------------------------------------------------------
1. METR-LA y PEMS-BAY (datos de trafico de Los Angeles / Bay Area)
------------------------------------------------------------
Formato: .h5
Fuente:  Google Drive (link oficial del repositorio del articulo)
URL:     https://drive.google.com/drive/folders/10FOTa6HXPqX8Pf5WRoRwcFnW9BrNZEIX

Descarga los archivos:
  - metr-la.h5
  - pems-bay.h5

Guarda ambos en esta carpeta: datasets/

------------------------------------------------------------
2. SOLAR (energia solar en Alabama)
------------------------------------------------------------
Formato: .txt
Fuente:  GitHub - laiguokun/multivariate-time-series-data
URL:     https://github.com/laiguokun/multivariate-time-series-data

Descarga: solar_AL.txt
Guarda en: datasets/

------------------------------------------------------------
3. ELECTRICITY (consumo electrico)
------------------------------------------------------------
Formato: .txt
Fuente:  GitHub - laiguokun/multivariate-time-series-data
URL:     https://github.com/laiguokun/multivariate-time-series-data

Descarga: electricity.txt
Guarda en: datasets/

------------------------------------------------------------
CONFIGURACION despues de descargar
------------------------------------------------------------
Edita los archivos .yml en TS-LIF-main/TS-LIF/exp/forecast/dataset/
y cambia la linea "file: /home/feng/..." por la ruta local, por ejemplo:

  metr-la.yml:
    file: ../../../datasets/metr-la.h5    <- cambiar esto

  solar.yml:
    file: ../../../datasets/solar_AL.txt  <- cambiar esto

  electricity.yml:
    file: ../../../datasets/electricity.txt <- cambiar esto

  pems-bay.yml:
    file: ../../../datasets/pems-bay.h5   <- cambiar esto
"""
with open(os.path.join(DEST, "datasets", "DESCARGAR_DATASETS.txt"), "w", encoding="utf-8") as f:
    f.write(datasets_info)
print("✓ Instrucciones de descarga de datasets creadas")

# ---------------------------------------------------------------------------
# 6. README principal
# ---------------------------------------------------------------------------
readme = """\
# TAREA 2 — Actividad WhitePapers
## Python para la Inteligencia Artificial (01MIAR)
**Alumno:** Lucas Támara | lucastamaraucv@gmail.com
**Artículo:** TS-LIF: A Temporal Segment Spiking Neuron Network for Time Series Forecasting (ICLR 2025)

---

## Estructura de esta carpeta

```
subirTarea/
├── 01MIAR_ACT_WhitePapers.ipynb    <- ENTREGA PRINCIPAL (ejecutar esto)
├── requirements_notebook.txt        <- dependencias del notebook
├── requirements_tslif.txt           <- dependencias del codigo original
├── TS-LIF-main/                     <- codigo original del articulo (referencia)
│   └── TS-LIF/
│       ├── SeqSNN/                  <- paquete principal del modelo
│       └── exp/forecast/            <- configuraciones de experimentos
└── datasets/
    └── DESCARGAR_DATASETS.txt       <- instrucciones para descargar los datos
```

---

## Opcion 1: Ejecutar el NOTEBOOK (recomendado, sin GPU)

El notebook es completamente autonomo. Genera sus propios datos sinteticos
con NumPy y no requiere descargar ningun dataset externo.

**Pasos:**

```bash
# 1. Instalar dependencias
pip install -r requirements_notebook.txt

# 2. Abrir el notebook
jupyter notebook 01MIAR_ACT_WhitePapers.ipynb

# 3. Ejecutar todas las celdas (Cell > Run All)
```

**Requiere:** Python 3.8+, numpy, matplotlib. Nada mas.

---

## Opcion 2: Ejecutar el codigo original del articulo (requiere GPU)

> ADVERTENCIA: este codigo requiere GPU NVIDIA y puede tardar horas en entrenar.

```bash
# 1. Crear entorno conda
conda create -n SeqSNN python=3.9
conda activate SeqSNN

# 2. Instalar el paquete SeqSNN
cd TS-LIF-main/TS-LIF
pip install -e .

# 3. Instalar dependencias adicionales
pip install -r ../../requirements_tslif.txt

# 4. Descargar datasets (ver datasets/DESCARGAR_DATASETS.txt)
#    y actualizar las rutas en exp/forecast/dataset/*.yml

# 5. Ejecutar un experimento (ejemplo con TS-GRU en Solar)
python -m SeqSNN.entry.tsforecast exp/forecast/spikegru/spikegru_solar.yml
```

---

## Referencia del articulo

Feng, S., Feng, W., Gao, X., Zhao, P., y Shen, Z. (2025).
TS-LIF: A Temporal Segment Spiking Neuron Network for Time Series Forecasting.
ICLR 2025. https://arxiv.org/abs/2503.05108

Repositorio oficial: https://github.com/kkking-kk/TS-LIF
"""
with open(os.path.join(DEST, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme)
print("✓ README.md creado")

# ---------------------------------------------------------------------------
# Resumen final
# ---------------------------------------------------------------------------
print("\n" + "="*60)
print("LISTO. Estructura de subirTarea:")
for root, dirs, files in os.walk(DEST):
    level = root.replace(DEST, "").count(os.sep)
    indent = "  " * level
    folder = os.path.basename(root)
    print(f"{indent}{folder}/")
    subindent = "  " * (level + 1)
    for f in files:
        fpath = os.path.join(root, f)
        size_kb = os.path.getsize(fpath) / 1024
        print(f"{subindent}{f}  ({size_kb:.1f} KB)")
print("="*60)
print("\nPara comprimir: clic derecho en subirTarea -> Enviar a -> Carpeta comprimida")

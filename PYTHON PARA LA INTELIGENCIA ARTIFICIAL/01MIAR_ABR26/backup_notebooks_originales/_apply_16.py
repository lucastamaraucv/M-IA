"""Aplica mejoras al notebook 16 Image Analysis con teoria detallada y bloques de colores."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, dato, aviso
import json

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_16_Image_Analysis.ipynb"

nb = json.load(open(NB, encoding="utf-8"))


def find_id(fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if fragment in src:
            return c["id"]
    return None


ID_TITULO    = nb["cells"][0]["id"]
ID_OPENCV    = find_id("## OpenCV")
ID_CARGAR    = find_id("## Cargar / Mostrar")
ID_DESCOMP   = find_id("Descomponer imagen")
ID_SUMAR     = find_id("Sumar dos im")
ID_BLENDING  = find_id("## Blending")
ID_BORDES    = None
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if src.startswith("## Detecci") and "borde" in src.lower():
        ID_BORDES = c["id"]
        break
ID_CARAS     = None
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if src.startswith("## Detecci") and "cara" in src.lower():
        ID_CARAS = c["id"]
        break


plan = []

# ===== INTRO =====
plan.append((ID_TITULO, [
    {"type": "md", "src": teoria(
        "Como leer este notebook (mejorado)",
        """Este notebook fue **enriquecido** con bloques de colores:

- <span style="color:#1864ab"><b>AZUL = TEORIA</b></span>
- <span style="color:#a05a00"><b>AMARILLO = TU TURNO</b></span>
- <span style="color:#1b5e20"><b>VERDE = SOLUCION</b></span>
- <span style="color:#7d1818"><b>ROJO = CUIDADO</b></span>

**Que vas a aprender aqui?** A cargar imagenes, manipular sus pixeles, aplicar filtros, detectar bordes y detectar caras con redes neuronales (DNN). Todo con OpenCV.

#### Que es una imagen para el ordenador?

Una imagen es un **array de NumPy** con forma `(alto, ancho, canales)`:

| Tipo | Shape | Ejemplo |
|---|---|---|
| Escala de grises | `(H, W)` | un valor 0-255 por pixel |
| Color RGB | `(H, W, 3)` | tres valores: rojo, verde, azul |
| Color con alpha | `(H, W, 4)` | RGBA (alpha = transparencia) |

> **Trampa de OpenCV:** OpenCV usa **BGR** (Blue-Green-Red), NO RGB. Si mezclas codigo de matplotlib (RGB) con OpenCV (BGR), los colores salen invertidos."""
    )},
]))

# ===== OPENCV intro =====
plan.append((ID_OPENCV, [
    {"type": "md", "src": teoria(
        "Que es OpenCV?",
        """**OpenCV** (Open Source Computer Vision) es la libreria mas usada del mundo para **vision por computador**. Esta escrita en C++ con bindings de Python.

#### Que puedes hacer con OpenCV?

| Tarea | Funcion |
|---|---|
| Leer / escribir imagenes | `cv2.imread`, `cv2.imwrite` |
| Mostrar | `cv2.imshow` (en Jupyter mejor `plt.imshow`) |
| Cambiar color (BGR <-> gris, RGB, HSV) | `cv2.cvtColor` |
| Redimensionar / rotar / voltear | `cv2.resize`, `cv2.warpAffine`, `cv2.flip` |
| Filtros (suavizado, bordes) | `cv2.GaussianBlur`, `cv2.Sobel`, `cv2.Canny` |
| Operaciones | `cv2.add`, `cv2.subtract`, `cv2.addWeighted` |
| Detectar caras / objetos | `cv2.CascadeClassifier`, `cv2.dnn.readNet` |
| Tracking de video | `cv2.VideoCapture`, trackers |

#### Instalacion

```
pip install opencv-python              # version basica
pip install opencv-contrib-python      # con modulos extra
```

#### Convencion en Jupyter

`cv2.imshow` abre una ventana del SO que no funciona bien en notebooks. **En Jupyter usa matplotlib**:

```python
import cv2, matplotlib.pyplot as plt
img_bgr = cv2.imread('foto.jpg')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb); plt.axis('off'); plt.show()
```"""
    )},
]))

# ===== CARGAR / MOSTRAR =====
plan.append((ID_CARGAR, [
    {"type": "md", "src": teoria(
        "Cargar y mostrar imagenes",
        """#### Cargar

```python
img = cv2.imread('ruta/foto.jpg')          # carga en BGR
img = cv2.imread('ruta/foto.jpg', cv2.IMREAD_GRAYSCALE)   # en gris
img = cv2.imread('ruta/foto.jpg', cv2.IMREAD_UNCHANGED)   # con canal alpha si lo tiene

print(img.shape)     # (alto, ancho, 3) si es color, (alto, ancho) si es gris
print(img.dtype)     # uint8 -> valores 0..255
```

> **CUIDADO:** si la ruta esta mal, `imread` NO da error: devuelve `None`. Comprueba siempre `if img is None: ...`.

#### Acceder a un pixel

```python
img[100, 50]            # pixel fila 100, columna 50 -> [B, G, R]
img[100, 50, 0]         # canal Blue del pixel
img[100, 50] = [0, 0, 255]   # poner el pixel rojo
```

#### Mostrar en Jupyter (recomendado)

```python
import matplotlib.pyplot as plt
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
```"""
    )},
    {"type": "md", "src": tu_turno(1,
        """1. Carga una imagen del directorio `res/` (por ejemplo `cv2.imread('res/people.jpg')`).
2. Imprime su `shape` y `dtype`.
3. Imprime los valores B, G, R del pixel central.
4. Mostrarla con matplotlib (recordando convertir BGR -> RGB)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import cv2, matplotlib.pyplot as plt\n# img = cv2.imread('res/people.jpg')\n# if img is None:\n#     print('No se pudo cargar. Comprueba la ruta.')\n# else:\n#     print('Shape:', img.shape, 'Dtype:', img.dtype)\n#     h, w = img.shape[:2]\n#     b, g, r = img[h//2, w//2]\n#     print(f'Pixel central: B={b} G={g} R={r}')\n#     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)); plt.axis('off'); plt.show()\n"},
]))

# ===== DESCOMPONER =====
if ID_DESCOMP:
    plan.append((ID_DESCOMP, [
        {"type": "md", "src": teoria(
            "Descomponer y recomponer canales",
            """Una imagen color es una **pila de tres matrices 2D** (B, G, R en OpenCV).

```python
b, g, r = cv2.split(img)      # tres arrays 2D
img2 = cv2.merge([b, g, r])   # vuelve a ser una imagen 3D
```

#### Espacios de color

OpenCV soporta muchos. Los mas usados:

| Espacio | Cuando usarlo |
|---|---|
| **BGR** | el de OpenCV por defecto |
| **RGB** | el de matplotlib |
| **GRAY** | para procesar mas rapido (1 canal vs 3) |
| **HSV** | Hue/Saturation/Value -> mejor para filtrar por color |
| **LAB** | perceptualmente uniforme |

#### Conversiones

```python
gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
rgb  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
```

> Si trabajas con vision por color (segmentar objetos rojos, verdes...), **pasa siempre a HSV**: el canal H representa el color independientemente de la iluminacion."""
        )},
        {"type": "md", "src": tu_turno(2,
            """1. Carga una imagen color.
2. Conviertela a **escala de grises** y muestra ambas (la original y la gris) con matplotlib en una grilla 1x2.
3. Bonus: separa los 3 canales (B, G, R) y muestralos por separado en una grilla 1x3."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import cv2, matplotlib.pyplot as plt\n# img = cv2.imread('res/people.jpg')\n# gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\n#\n# fig, axs = plt.subplots(1, 2, figsize=(10,4))\n# axs[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)); axs[0].set_title('Original')\n# axs[1].imshow(gris, cmap='gray'); axs[1].set_title('Gris')\n# for ax in axs: ax.axis('off')\n# plt.show()\n#\n# b, g, r = cv2.split(img)\n# fig, axs = plt.subplots(1, 3, figsize=(15,4))\n# for ax, canal, nombre in zip(axs, [b, g, r], ['Blue', 'Green', 'Red']):\n#     ax.imshow(canal, cmap='gray'); ax.set_title(nombre); ax.axis('off')\n# plt.show()\n"},
    ]))

# ===== SUMAR =====
if ID_SUMAR:
    plan.append((ID_SUMAR, [
        {"type": "md", "src": teoria(
            "Operaciones aritmeticas: suma, resta, blending",
            """Las imagenes son arrays NumPy: las puedes sumar, restar, multiplicar... pero hay sutilezas.

#### Suma con NumPy vs OpenCV

```python
# NumPy: hace modulo 256 (los valores se reinician)
255 + 5  =  4   (overflow uint8)

# OpenCV: hace saturacion (lo manda al maximo)
cv2.add(255, 5)  = 255   (clamp)
```

> **Regla:** para imagenes usa `cv2.add` y `cv2.subtract` para no perder informacion por overflow.

#### Blending: mezclar dos imagenes

`cv2.addWeighted(img1, alpha, img2, beta, gamma)` calcula:
```
salida = img1 * alpha + img2 * beta + gamma
```

| Parametro | Significado |
|---|---|
| alpha | peso de la primera imagen (0..1) |
| beta | peso de la segunda imagen (0..1) |
| gamma | brillo extra (suma constante, normalmente 0) |

> Las dos imagenes deben tener **el mismo shape**. Si no, hay que redimensionar antes."""
        )},
        {"type": "md", "src": tu_turno(3,
            """Carga una imagen y crea otra blanca del mismo tamano (`np.full_like(img, 255)`). Hazlas blending al **50% cada una** con `cv2.addWeighted`. Mostrar el resultado (deberias ver la imagen difuminada hacia el blanco)."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import cv2, numpy as np, matplotlib.pyplot as plt\n# img = cv2.imread('res/people.jpg')\n# blanco = np.full_like(img, 255)\n# mezcla = cv2.addWeighted(img, 0.5, blanco, 0.5, 0)\n# plt.imshow(cv2.cvtColor(mezcla, cv2.COLOR_BGR2RGB)); plt.axis('off'); plt.show()\n"},
    ]))

# ===== BLENDING =====
if ID_BLENDING:
    plan.append((ID_BLENDING, [
        {"type": "md", "src": teoria(
            "Blending en la practica",
            """Casos reales donde se usa blending:

- **Watermarks**: poner un logo semitransparente sobre una foto.
- **Crossfade en video**: transicion suave entre dos clips.
- **Comparacion antes/despues**: deslizar entre dos versiones de la misma imagen.
- **Overlay**: dibujar texto/iconos translucidos.

```python
out = cv2.addWeighted(foto, 0.7, logo, 0.3, 0)
```

#### Mascaras (alpha) en lugar de blending uniforme

Si solo quieres mezclar una **region** de una imagen con otra (no toda), necesitas una **mascara** (array del mismo tamano con valores 0..255 o 0..1):

```python
img_final = (img_a * (mask/255.0) + img_b * (1 - mask/255.0)).astype('uint8')
```

Esto se usa muchisimo en **segmentacion** (cuando quieres aislar un objeto del fondo)."""
        )},
    ]))

# ===== DETECCION DE BORDES =====
if ID_BORDES:
    plan.append((ID_BORDES, [
        {"type": "md", "src": teoria(
            "Deteccion de bordes: Sobel, Laplacian, Canny",
            """Un **borde** es una zona donde el brillo cambia bruscamente. Detectarlos es fundamental para:

- Segmentar objetos.
- Reconocimiento de formas.
- Pre-procesado para OCR.
- Compresion (los bordes contienen la informacion clave de la imagen).

#### Idea matematica: el gradiente

Un borde es una **derivada alta** del brillo. NumPy/OpenCV calculan el gradiente con filtros (kernels):

| Filtro | Que detecta |
|---|---|
| **Sobel X** | bordes verticales (cambios horizontales) |
| **Sobel Y** | bordes horizontales (cambios verticales) |
| **Laplacian** | bordes en cualquier direccion (segunda derivada) |
| **Canny** | algoritmo completo (suaviza + sobel + thinning + thresholding) |

#### Codigo tipico

```python
import cv2

img_gris = cv2.imread('foto.jpg', cv2.IMREAD_GRAYSCALE)

sobel_x   = cv2.Sobel(img_gris, cv2.CV_64F, 1, 0, ksize=5)
sobel_y   = cv2.Sobel(img_gris, cv2.CV_64F, 0, 1, ksize=5)
laplacian = cv2.Laplacian(img_gris, cv2.CV_64F)
canny     = cv2.Canny(img_gris, threshold1=100, threshold2=200)
```

> **Tip:** si tus bordes salen muy ruidosos, suaviza primero con `cv2.GaussianBlur(img, (5,5), 0)`.

#### Por que CV_64F y luego conversion?

Las derivadas pueden ser negativas. Si las guardas en `uint8` (0..255), las negativas se truncan a 0 y pierdes informacion. Por eso usas `CV_64F` (float64) y luego conviertes con `np.absolute(...).astype('uint8')`."""
        )},
        {"type": "md", "src": tu_turno(4,
            """1. Carga una imagen en escala de grises.
2. Aplicale los 4 detectores de bordes: Sobel X, Sobel Y, Laplacian y Canny.
3. Muestra los 4 resultados en una grilla 2x2 con matplotlib.

> Pista: para Canny prueba con `threshold1=50, threshold2=150`. Para Sobel y Laplacian, recuerda convertir a `uint8` con `np.absolute(...).astype(np.uint8)`."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import cv2, numpy as np, matplotlib.pyplot as plt\n# img = cv2.imread('res/people.jpg', cv2.IMREAD_GRAYSCALE)\n#\n# sx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)\n# sy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)\n# lap = cv2.Laplacian(img, cv2.CV_64F)\n# canny = cv2.Canny(img, 50, 150)\n#\n# fig, axs = plt.subplots(2, 2, figsize=(10, 10))\n# axs[0,0].imshow(np.absolute(sx).astype(np.uint8), cmap='gray');  axs[0,0].set_title('Sobel X')\n# axs[0,1].imshow(np.absolute(sy).astype(np.uint8), cmap='gray');  axs[0,1].set_title('Sobel Y')\n# axs[1,0].imshow(np.absolute(lap).astype(np.uint8), cmap='gray'); axs[1,0].set_title('Laplacian')\n# axs[1,1].imshow(canny, cmap='gray');                              axs[1,1].set_title('Canny')\n# for ax in axs.flat: ax.axis('off')\n# plt.tight_layout(); plt.show()\n"},
    ]))

# ===== DETECCION DE CARAS =====
if ID_CARAS:
    plan.append((ID_CARAS, [
        {"type": "md", "src": teoria(
            "Deteccion de caras con DNN",
            """OpenCV trae un **modelo pre-entrenado** (Caffe / TensorFlow) para detectar caras. Es mucho mas robusto que los Haar Cascades clasicos.

#### Pipeline tipico

```python
import cv2, numpy as np

# 1. Cargar el modelo (necesitas dos archivos: .prototxt y .caffemodel)
net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'res10_300x300_ssd_iter_140000.caffemodel')

# 2. Preparar la imagen como 'blob' (formato que la red espera)
img = cv2.imread('foto.jpg')
h, w = img.shape[:2]
blob = cv2.dnn.blobFromImage(
    cv2.resize(img, (300, 300)),    # la red espera 300x300
    scalefactor=1.0,
    size=(300, 300),
    mean=(104.0, 177.0, 123.0)      # restar la media (preprocesado del modelo)
)

# 3. Pasar por la red
net.setInput(blob)
detecciones = net.forward()

# 4. Recorrer detecciones y dibujar rectangulos
for i in range(detecciones.shape[2]):
    confianza = detecciones[0, 0, i, 2]
    if confianza < 0.5:
        continue
    box = detecciones[0, 0, i, 3:7] * np.array([w, h, w, h])
    x1, y1, x2, y2 = box.astype(int)
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
```

#### Conceptos clave

| Concepto | Que es |
|---|---|
| **Blob** | tensor preprocesado (4D: batch x canales x alto x ancho) que la red consume |
| **scalefactor** | normaliza pixeles (ej. dividir entre 255 para llevar a [0,1]) |
| **mean** | la media RGB con la que se entreno la red, hay que restarla |
| **confidence_threshold** | umbral minimo para considerar una deteccion valida |

> Estos modelos se llaman **SSD** (Single Shot Detector) y son la base de muchos sistemas de deteccion en tiempo real."""
        )},
        {"type": "md", "src": tu_turno(5,
            """Si tienes el modelo cargado en `net` (como en el ejemplo del notebook):

1. Pasa una imagen y obten las detecciones.
2. Filtra las que tengan confianza > 0.7.
3. Para cada deteccion valida, dibuja un rectangulo verde y escribe la confianza encima con `cv2.putText`.
4. Muestra la imagen final con matplotlib (acuerdate de BGR -> RGB)."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import cv2, numpy as np, matplotlib.pyplot as plt\n# # asume que 'net' y 'img' ya existen\n# h, w = img.shape[:2]\n# blob = cv2.dnn.blobFromImage(cv2.resize(img, (300,300)), 1.0, (300,300), (104.0,177.0,123.0))\n# net.setInput(blob)\n# det = net.forward()\n# img_out = img.copy()\n# for i in range(det.shape[2]):\n#     conf = det[0, 0, i, 2]\n#     if conf < 0.7:\n#         continue\n#     box = det[0, 0, i, 3:7] * np.array([w, h, w, h])\n#     x1, y1, x2, y2 = box.astype(int)\n#     cv2.rectangle(img_out, (x1,y1), (x2,y2), (0,255,0), 2)\n#     cv2.putText(img_out, f'{conf:.2f}', (x1, y1-10),\n#                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)\n# plt.imshow(cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)); plt.axis('off'); plt.show()\n"},
    ]))


enhance(NB, plan)
print("Done.")

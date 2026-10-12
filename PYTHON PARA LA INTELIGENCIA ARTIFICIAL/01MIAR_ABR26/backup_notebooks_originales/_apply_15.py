"""Aplica mejoras al notebook 15_OCR con bloques de colores y teoria detallada.

El notebook original trata el reconocimiento de digitos escritos a mano con
scikit-learn (un caso clasico y didactico de OCR). Aprovechamos este contexto
para introducir tambien la teoria general de OCR y la herramienta estandar de
la industria: Tesseract (con su binding Python pytesseract).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, solucion_md, dato, aviso

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_15_OCR.ipynb"

import json
nb = json.load(open(NB, encoding="utf-8"))


def find_id(text_fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if text_fragment in src:
            return c["id"]
    return None


# IDs reales del notebook 15 (16 celdas)
ID_TITULO       = nb["cells"][0]["id"]                                 # 0  intro
ID_DATASET_MD   = find_id("Dataset de D")                              # 1  intro dataset
ID_LOAD         = find_id("datasets.load_digits")                      # 2  load_digits
ID_MATRIZ       = find_id("Imagenes como matriz")                      # 3  matriz
ID_IMSHOW       = find_id("Visualizar un digito")                      # 4  plt.imshow
ID_DESCR        = find_id("Descripcion del dataset")                   # 5  DESCR
ID_TARGETS      = find_id("Valores numericos, targets")                # 6  targets
ID_APREND_MD    = find_id("## Aprendiendo")                            # 7  Aprendiendo
ID_SVM          = find_id("Support Vector Machine")                    # 8  svm
ID_FLATTEN      = find_id("Aplanar imagenes a 1D")                     # 9  reshape
ID_SPLIT        = find_id("Dividir dataset en entrenamiento")          # 10 train_test_split
ID_FIT          = find_id("Entremaniento")                             # 11 fit
ID_PRED_MD      = find_id("## Predicci")                               # 12 Prediccion
ID_PREDICT      = find_id("predicted = svc.predict")                   # 13 predict
ID_VISPRED      = find_id("Visualizar predicciones")                   # 14 visualizar predicciones
ID_REPORT       = find_id("Informe del resultado")                     # 15 classification_report


plan = []

# -------- INTRO al notebook --------
plan.append((ID_TITULO, [
    {"type": "md", "src": teoria(
        "Como leer este notebook (version mejorada)",
        """Este notebook fue **enriquecido** para ayudarte a aprender escribiendo codigo. Encontraras tres tipos de bloques de colores:

<div style="background-color:#e7f5ff;border-left:6px solid #1c7ed6;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AZUL = TEORIA</b></div> -> explicacion en palabras simples antes de cada concepto.

<div style="background-color:#fff9db;border-left:6px solid #f59f00;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AMARILLO = TU TURNO</b></div> -> el ejercicio que TU debes resolver. Hay una celda vacia debajo donde escribes el codigo.

<div style="background-color:#ebfbee;border-left:6px solid #2f9e44;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>VERDE = SOLUCION</b></div> -> codigo de referencia comentado por si te trabas. Destapa solo despues de intentar.

> **Promesa importante**: el codigo y la teoria del profesor original no se han tocado. Solo se han ANIADIDO bloques. Asi puedes seguir comparando con la version original cuando quieras."""
    )},
    {"type": "md", "src": teoria(
        "Que es OCR (Optical Character Recognition)?",
        """**OCR** son las siglas de *Optical Character Recognition*, en castellano **Reconocimiento Optico de Caracteres**. Es la tecnologia que **convierte una imagen con texto en texto digital editable**.

#### Ejemplos de uso cotidiano

- Escanear el DNI con el movil y autocompletar formularios.
- Pasar una factura en papel a una hoja de calculo.
- Buscar palabras dentro de un PDF que es una foto escaneada.
- Leer matriculas de coches en un parking.
- Reconocer texto en fotos para traducirlo (Google Lens).

#### Tipos de OCR

| Tipo | Descripcion | Ejemplo |
|---|---|---|
| **OCR clasico** | Reglas + plantillas, requiere texto limpio e impreso | Lectura de cheques bancarios |
| **OCR estadistico/ML** | Modelos entrenados (SVM, kNN) con pixeles como features | Este notebook con `digits` |
| **OCR neuronal moderno** | Redes profundas (LSTM, Transformers) | Tesseract 4/5, EasyOCR, PaddleOCR |
| **HCR/HTR** | *Handwritten* OCR, texto manuscrito | Lectura de manuscritos historicos |

#### Que vamos a hacer en este notebook?

Vamos a entrenar un clasificador (un **SVM**) sobre el dataset `digits` de scikit-learn (digitos manuscritos en imagenes 8x8). Este es un **caso didactico de OCR**: el modelo aprende a mapear pixeles -> caracter.

Para texto real (parrafos, paginas, facturas) **NO** se reentrena un SVM desde cero: se usan motores ya hechos como **Tesseract** (lo veremos a continuacion)."""
    )},
    {"type": "md", "src": teoria(
        "Tesseract y pytesseract: el OCR estandar de la industria",
        """**Tesseract** es el motor OCR libre mas usado del mundo. Lo desarrollo HP en los 80 y desde 2006 lo mantiene Google. **pytesseract** es el binding de Python: una capa fina que llama al ejecutable de Tesseract.

#### Como funciona Tesseract a alto nivel

1. **Preprocesado interno**: limpia y umbraliza la imagen.
2. **Deteccion de lineas y palabras**: encuentra rectangulos de texto.
3. **Segmentacion de caracteres**: divide cada palabra en glifos.
4. **Reconocimiento**: a partir de la version 4, usa una **red neuronal LSTM** entrenada con muchisimo texto. La version 3 usaba clasificadores clasicos.
5. **Postproceso**: corrige usando un diccionario del idioma seleccionado.

#### Instalacion en Windows (importante!)

`pip install pytesseract` **NO** instala el motor, solo el wrapper de Python. Hay dos pasos:

```text
1) Instalar el motor:
   - Descarga desde https://github.com/UB-Mannheim/tesseract/wiki
   - Instalador .exe -> instala normalmente (por defecto en
     C:\\Program Files\\Tesseract-OCR\\tesseract.exe)
   - Marca los idiomas que quieras (Spanish, English, ...)

2) Instalar el wrapper de Python:
   pip install pytesseract pillow
```

#### Codigo minimo en Python

```python
import pytesseract
from PIL import Image

# En Windows hay que decirle donde esta el .exe
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = Image.open('res/factura.png')
texto = pytesseract.image_to_string(img, lang='spa')   # 'spa' = espaniol
print(texto)
```

#### Funciones principales de pytesseract

| Funcion | Que devuelve |
|---|---|
| `image_to_string(img, lang='spa')` | El texto plano detectado |
| `image_to_data(img, output_type=...)` | Cada palabra con su caja, confianza, linea |
| `image_to_boxes(img)` | Caja de cada caracter individual |
| `image_to_osd(img)` | Orientacion y script (latin, arabe...) detectados |
| `get_languages()` | Idiomas instalados |"""
    )},
]))

# -------- DATASET digits --------
plan.append((ID_DATASET_MD, [
    {"type": "md", "src": teoria(
        "El dataset 'digits' de scikit-learn",
        """Antes de aplicar Tesseract a texto real, es muy didactico **construir un OCR pequeno desde cero**. Para eso scikit-learn trae el dataset `digits`:

| Caracteristica | Valor |
|---|---|
| Imagenes | 1797 |
| Tamanio de cada imagen | 8 x 8 = 64 pixeles |
| Color | Escala de grises, 16 niveles (0=blanco, 16=negro) |
| Clases | 10 (digitos del 0 al 9) |
| Origen | Subconjunto del clasico **MNIST/UCI Optical Digits** |

#### Estructura del objeto `digits`

```python
digits = datasets.load_digits()

digits.images   # array (1797, 8, 8) -> matriz 8x8 por imagen
digits.data     # array (1797, 64)   -> imagen aplanada a vector
digits.target   # array (1797,)      -> etiqueta (0..9) de cada imagen
digits.DESCR    # texto con la descripcion del dataset
```

> El dataset es **muy pequenio** (8x8 pixeles!) por eso un SVM ya da > 95% de acierto. Para imagenes reales necesitarias resolucion mayor y modelos mas potentes."""
    )},
]))

plan.append((ID_TARGETS, [
    {"type": "md", "src": tu_turno(1,
        """Explora el dataset `digits` por tu cuenta. Imprime:

1. La **forma** (`shape`) de `digits.images` y `digits.data`.
2. Cuantas imagenes hay de cada digito (pista: `numpy.unique(..., return_counts=True)`).
3. El **valor minimo y maximo** de los pixeles (para entender el rango)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport numpy as np\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n#\n# # 1) shape\n# print('images shape:', digits.images.shape)   # (1797, 8, 8)\n# print('data shape:  ', digits.data.shape)     # (1797, 64)\n#\n# # 2) cuantas imagenes hay por clase\n# valores, conteos = np.unique(digits.target, return_counts=True)\n# for v, c in zip(valores, conteos):\n#     print(f'Digito {v}: {c} imagenes')\n#\n# # 3) rango de los pixeles\n# print('Pixel min:', digits.images.min())   # 0\n# print('Pixel max:', digits.images.max())   # 16\n"},
]))

# -------- PREPROCESADO (antes de aprender) --------
plan.append((ID_APREND_MD, [
    {"type": "md", "src": teoria(
        "Preprocesado de imagen: el paso CLAVE en OCR",
        """Tanto si entrenas tu propio modelo como si usas Tesseract, **la calidad del preprocesado decide el resultado**. Tesseract puede pasar del 70% al 99% de acierto con un buen preprocesado.

#### Pasos tipicos (en este orden)

| Paso | Para que sirve | Codigo OpenCV |
|---|---|---|
| **1. Escala de grises** | Quita color, reduce a 1 canal | `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` |
| **2. Reescalado (DPI)** | Tesseract pide ~300 DPI | `cv2.resize(img, None, fx=2, fy=2)` |
| **3. Eliminacion de ruido** | Quita motas y granulado | `cv2.medianBlur(img, 3)` o `GaussianBlur` |
| **4. Binarizacion** | Solo blanco y negro: texto vs fondo | `cv2.threshold` u **Otsu** o **adaptativo** |
| **5. Deskew** | Endereza el texto inclinado | rotar segun angulo detectado |
| **6. Erosion/Dilatacion** | Engrosar o adelgazar trazos | `cv2.erode`, `cv2.dilate` |

#### Binarizacion: lo mas importante

Convierte la imagen en pixeles **0 o 255** (negro o blanco). Tres metodos:

1. **Umbral fijo**: `cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)`. Solo si la iluminacion es uniforme.
2. **Otsu**: `cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)`. Calcula el umbral automaticamente. Recomendado.
3. **Adaptativo**: `cv2.adaptiveThreshold(...)`. Para imagenes con sombras o iluminacion irregular (foto de movil).

#### Idiomas en Tesseract

Tesseract necesita **datos de entrenamiento por idioma** (archivos `.traineddata`). Los pasas con el parametro `lang`:

```python
pytesseract.image_to_string(img, lang='spa')         # espaniol
pytesseract.image_to_string(img, lang='eng')         # ingles
pytesseract.image_to_string(img, lang='spa+eng')    # combinado
```

Si pides un idioma no instalado, da error. `pytesseract.get_languages()` te lista los disponibles.

#### Configuracion adicional (PSM y OEM)

```python
config = r'--oem 3 --psm 6'
pytesseract.image_to_string(img, config=config)
```

- **OEM (Engine Mode)**: 3 = por defecto, 1 = solo LSTM (red neuronal).
- **PSM (Page Segmentation Mode)**: como interpretar el layout. Los mas usados:
  - `6` = un bloque uniforme de texto
  - `7` = una sola linea
  - `8` = una sola palabra
  - `10` = un solo caracter
  - `11` = texto disperso (carteles)"""
    )},
    {"type": "md", "src": aviso(
        """**Errores tipicos al usar Tesseract en Windows:**

1. `TesseractNotFoundError` -> no instalaste el motor o no esta en el PATH. Define `pytesseract.pytesseract.tesseract_cmd` con la ruta al `.exe`.
2. `Failed loading language 'spa'` -> el idioma espaniol no esta instalado. Vuelve a ejecutar el instalador y marca *Spanish*, o copia `spa.traineddata` a la carpeta `tessdata`.
3. **Resultado vacio o basura** -> casi siempre es **falta de preprocesado**. Convierte a gris, binariza con Otsu y reescala a 300 DPI.
4. **Acentos rotos** (la `n` con tilde sale como `?`) -> codifica a UTF-8 al imprimir o guardar el resultado: `print(texto.encode('utf-8', errors='replace').decode('utf-8'))`."""
    )},
    {"type": "md", "src": tu_turno(2,
        """**Ejercicio de preprocesado con OpenCV** (asume que tienes una imagen en `res/images/` o usa `res/meerkat.jpg` para practicar el flujo).

Escribe codigo que:

1. Cargue una imagen con `cv2.imread('res/meerkat.jpg')`.
2. La convierta a **escala de grises**.
3. Aplique **desenfoque mediano** (kernel 3) para quitar ruido.
4. Aplique **binarizacion de Otsu**.
5. Muestre las cuatro versiones (original, gris, desenfocada, binarizada) en una rejilla 2x2 con `matplotlib`.

> Si no tienes OpenCV instalado: `pip install opencv-python`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n# import cv2\n# import matplotlib.pyplot as plt\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import cv2\n# import matplotlib.pyplot as plt\n#\n# # 1) Cargar imagen (BGR por defecto)\n# img = cv2.imread('res/meerkat.jpg')\n#\n# # 2) Convertir a escala de grises\n# gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\n#\n# # 3) Reduccion de ruido con desenfoque mediano\n# desenfocada = cv2.medianBlur(gris, 3)\n#\n# # 4) Binarizacion automatica con Otsu\n# umbral, binaria = cv2.threshold(\n#     desenfocada, 0, 255,\n#     cv2.THRESH_BINARY + cv2.THRESH_OTSU\n# )\n# print('Umbral elegido por Otsu:', umbral)\n#\n# # 5) Mostrar las 4 versiones en una rejilla 2x2\n# fig, axes = plt.subplots(2, 2, figsize=(10, 8))\n# # Convertimos BGR -> RGB para matplotlib (que espera RGB)\n# axes[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))\n# axes[0, 0].set_title('Original')\n# axes[0, 1].imshow(gris, cmap='gray')\n# axes[0, 1].set_title('Escala de grises')\n# axes[1, 0].imshow(desenfocada, cmap='gray')\n# axes[1, 0].set_title('Desenfoque mediano')\n# axes[1, 1].imshow(binaria, cmap='gray')\n# axes[1, 1].set_title('Binarizada (Otsu)')\n# for ax in axes.flat:\n#     ax.axis('off')\n# plt.tight_layout()\n# plt.show()\n"},
]))

# -------- SVM --------
plan.append((ID_SVM, [
    {"type": "md", "src": teoria(
        "Por que un SVM para clasificar digitos?",
        """**SVM** (*Support Vector Machine*) es un clasificador clasico que busca la **frontera (hiperplano) que mejor separe** las clases en el espacio de features. Para imagenes pequenias (8x8) funciona muy bien y entrena en segundos.

#### Parametros que veras

```python
svc = svm.SVC(gamma=0.001, C=100.)
```

| Parametro | Significado | Efecto |
|---|---|---|
| `C` | Penalizacion por errores | C alto -> menos errores en train, mas riesgo de overfit |
| `gamma` | Cuanto influye un punto en su vecindad (kernel RBF) | gamma alto -> fronteras complejas |
| `kernel` | Forma de medir similitud | `'rbf'` (defecto), `'linear'`, `'poly'` |

#### Por que NO usariamos SVM para texto real

- Las imagenes reales son grandes (300x100 o mas), no 8x8.
- El texto tiene fuentes, tamanios y posiciones variables.
- Necesitarias **segmentar** caracter por caracter antes (es lo dificil).
- Para eso ya existen sistemas listos como **Tesseract** o redes profundas (CRNN)."""
    )},
]))

plan.append((ID_FLATTEN, [
    {"type": "md", "src": teoria(
        "Por que aplanamos las imagenes a un vector 1D?",
        """`scikit-learn` espera que cada muestra sea un **vector de features** (1D). Pero una imagen es 2D (alto x ancho). La solucion: **aplanarla**.

```python
n_samples = len(digits.images)             # 1797
data = digits.images.reshape((n_samples, -1))   # (1797, 64)
```

El `-1` significa "calcula tu mismo esa dimension para que cuadre". Como 8*8=64, queda `(1797, 64)`.

#### Lo que se pierde al aplanar

Cuando aplanas pierdes la **estructura espacial**: para el SVM el pixel (0,1) y el pixel (1,0) son simplemente las features 1 y 8, sin relacion espacial. Por eso para imagenes grandes se usan **CNNs** (redes convolucionales), que mantienen la estructura 2D."""
    )},
    {"type": "md", "src": tu_turno(3,
        """Visualiza **9 digitos del dataset** en una rejilla 3x3 con matplotlib, mostrando como titulo de cada uno la etiqueta correcta (`digits.target[i]`).

Pista: usa `plt.subplots(3, 3, figsize=(6, 6))` y un bucle con `enumerate(axes.flat)`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport matplotlib.pyplot as plt\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import matplotlib.pyplot as plt\n#\n# # Creamos la rejilla 3x3 (9 subplots)\n# fig, axes = plt.subplots(3, 3, figsize=(6, 6))\n#\n# # Iteramos sobre los 9 ejes y los 9 primeros digitos\n# for i, ax in enumerate(axes.flat):\n#     # imshow con escala de grises invertida (gray_r)\n#     ax.imshow(digits.images[i], cmap='gray_r')\n#     # El titulo es la etiqueta verdadera\n#     ax.set_title(f'Etiqueta: {digits.target[i]}')\n#     ax.axis('off')\n#\n# plt.tight_layout()\n# plt.show()\n"},
]))

# -------- TRAIN/TEST SPLIT --------
plan.append((ID_SPLIT, [
    {"type": "md", "src": teoria(
        "Por que dividir en train/test?",
        """Si entrenamos y evaluamos con los **mismos datos**, el modelo puede memorizar (overfit) y dar 100% sin haber aprendido nada generalizable. Por eso reservamos una **porcion para test** que el modelo nunca ve durante el entrenamiento.

```python
X_train, X_test, y_train, y_test = train_test_split(
    data, digits.target,
    test_size=0.05,    # 5% para test
    shuffle=False      # NO mezcla -> coge los ultimos 5%
)
```

| Parametro | Detalle |
|---|---|
| `test_size=0.05` | Fraccion (5%) o numero absoluto (`90`) para test |
| `shuffle=False` | Mantiene el orden original. Util para reproducibilidad pero peligroso si hay orden por clase |
| `random_state=42` | Semilla para que la division sea reproducible |
| `stratify=y` | Mantiene la proporcion de clases en train y test |

> En este notebook usan `shuffle=False`. Es una eleccion didactica para que veas las predicciones y los digitos en orden, **pero en produccion casi siempre quieres `shuffle=True` con `stratify=y`**."""
    )},
    {"type": "md", "src": tu_turno(4,
        """Repite la division pero con una **separacion mas habitual**:

- 80% train / 20% test
- `shuffle=True`
- `random_state=42`
- `stratify=digits.target`

Despues, comprueba que las clases estan **balanceadas** en train y test imprimiendo el conteo de cada digito en `y_train` y en `y_test`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport numpy as np\nfrom sklearn.model_selection import train_test_split\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# from sklearn.model_selection import train_test_split\n#\n# # Division 80/20 con barajado y estratificacion por clase\n# X_tr, X_te, y_tr, y_te = train_test_split(\n#     data, digits.target,\n#     test_size=0.20,\n#     shuffle=True,\n#     random_state=42,\n#     stratify=digits.target\n# )\n#\n# # Tamanios resultantes\n# print('Train:', X_tr.shape, ' Test:', X_te.shape)\n#\n# # Conteo por clase en train\n# vals_tr, cnts_tr = np.unique(y_tr, return_counts=True)\n# print('Distribucion train:', dict(zip(vals_tr, cnts_tr)))\n#\n# # Conteo por clase en test\n# vals_te, cnts_te = np.unique(y_te, return_counts=True)\n# print('Distribucion test :', dict(zip(vals_te, cnts_te)))\n"},
]))

# -------- PREDICCION --------
plan.append((ID_PRED_MD, [
    {"type": "md", "src": teoria(
        "Prediccion: usar el modelo entrenado",
        """Una vez `svc.fit(...)` ha terminado, el modelo ha aprendido los pesos. Ahora podemos pedirle que clasifique imagenes que **nunca vio**:

```python
predicted = svc.predict(X_test)   # vector con la prediccion para cada imagen
```

`predicted` tiene la misma longitud que `X_test`: para cada fila de pixeles, un digito (0..9).

#### Como interpretar los aciertos

```python
aciertos = (predicted == y_test).sum()
total    = len(y_test)
print(f'Acierto: {aciertos}/{total} = {aciertos/total:.2%}')
```

#### Probabilidades, no solo la clase

Si construyes el SVC con `probability=True`, puedes pedir tambien la **confianza** del modelo:

```python
svc = svm.SVC(gamma=0.001, C=100., probability=True)
svc.fit(X_train, y_train)
probs = svc.predict_proba(X_test)   # (n_test, 10)
```"""
    )},
]))

plan.append((ID_VISPRED, [
    {"type": "md", "src": tu_turno(5,
        """Encuentra todos los **errores** del modelo en el conjunto de test (casos donde `predicted[i] != y_test[i]`) y **muestralos** con matplotlib en una sola figura, anotando como titulo: `Real: X | Pred: Y`.

Si no hay errores (puede pasar con `test_size=0.05`), usa `test_size=0.2` con `shuffle=True` y vuelve a entrenar para encontrar alguno."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport numpy as np\nimport matplotlib.pyplot as plt\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# import matplotlib.pyplot as plt\n#\n# # 1) Indices donde la prediccion no coincide con la realidad\n# errores_idx = np.where(predicted != y_test)[0]\n# print(f'Numero de errores: {len(errores_idx)}')\n#\n# if len(errores_idx) == 0:\n#     print('Sin errores con esta division. Prueba test_size=0.2 con shuffle=True')\n# else:\n#     # 2) Mostramos hasta 6 errores en una fila\n#     n_mostrar = min(6, len(errores_idx))\n#     fig, axes = plt.subplots(1, n_mostrar, figsize=(2 * n_mostrar, 3))\n#     # Si solo hay 1 axes, lo metemos en lista para iterar igual\n#     if n_mostrar == 1:\n#         axes = [axes]\n#     for ax, idx in zip(axes, errores_idx[:n_mostrar]):\n#         # Reconstruimos la imagen 8x8 desde el vector de 64\n#         img = X_test[idx].reshape(8, 8)\n#         ax.imshow(img, cmap='gray_r')\n#         ax.set_title(f'Real: {y_test[idx]} | Pred: {predicted[idx]}')\n#         ax.axis('off')\n#     plt.tight_layout()\n#     plt.show()\n"},
]))

# -------- METRICS / FINAL --------
plan.append((ID_REPORT, [
    {"type": "md", "src": teoria(
        "Como leer el classification_report",
        """`classification_report` te da las **metricas por clase** mas usadas:

| Metrica | Que mide | Formula |
|---|---|---|
| **precision** | De los que predije como X, cuantos eran X | TP / (TP + FP) |
| **recall** | De los que eran X, cuantos detecte | TP / (TP + FN) |
| **f1-score** | Equilibrio precision/recall | 2 * (P * R) / (P + R) |
| **support** | Cuantos casos hay de esa clase en test |  |

Tres filas de resumen al final:

- **accuracy**: % global de aciertos.
- **macro avg**: media simple por clase (cada clase pesa igual).
- **weighted avg**: media ponderada por `support` (clases grandes pesan mas).

#### Otras herramientas utiles

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

cm = confusion_matrix(y_test, predicted)
ConfusionMatrixDisplay(cm).plot()
plt.show()
```

La **matriz de confusion** te dice no solo cuantos errores hay, sino **con que clase los confunde**. Para digitos suele confundir 1 con 7, 4 con 9, etc."""
    )},
    {"type": "md", "src": dato(
        """**Recapitulacion: del SVM al OCR real**

Lo que aprendiste aqui (SVM sobre digitos 8x8) es el **principio basico** de un OCR. Para texto real necesitas:

1. **Detectar regiones de texto** en la imagen (no es trivial: parrafos, lineas, columnas).
2. **Segmentar palabras y caracteres**.
3. **Reconocer cada caracter** (eso es lo que hace el SVM aqui, pero a otra escala).
4. **Postproceso linguistico** (diccionario, modelos de lenguaje).

**Tesseract** ya hace los 4 pasos por ti, con LSTM y diccionarios por idioma. Para casos especiales (manuscrito, idiomas raros, layouts complejos) hay alternativas: **EasyOCR**, **PaddleOCR**, **TrOCR** (Microsoft, basado en Transformers)."""
    )},
    {"type": "md", "src": tu_turno(6,
        """**Ejercicio final: matriz de confusion + tu primer OCR con Tesseract**

Parte A (con scikit-learn):
1. Calcula e imprime la **matriz de confusion** del modelo.
2. Visualizala con `ConfusionMatrixDisplay`.
3. Identifica que **par de digitos** se confunde mas.

Parte B (con Tesseract, opcional - solo si lo tienes instalado):
1. Coloca una imagen con texto en `res/` (por ejemplo `res/texto.png`).
2. Configura `pytesseract.pytesseract.tesseract_cmd` con la ruta a `tesseract.exe`.
3. Carga la imagen con OpenCV, conviertela a gris, binariza con Otsu.
4. Llama a `pytesseract.image_to_string(img, lang='spa')` y muestra el texto.
5. Compara el resultado **con** y **sin** preprocesado: veras la diferencia."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo (Parte A):\nimport matplotlib.pyplot as plt\nfrom sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay\n\n"},
    {"type": "code", "src": "# === Solucion Parte A ===\n# import matplotlib.pyplot as plt\n# from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay\n#\n# # 1) Matriz de confusion (filas: real, columnas: prediccion)\n# cm = confusion_matrix(y_test, predicted)\n# print('Matriz de confusion:')\n# print(cm)\n#\n# # 2) Visualizacion\n# disp = ConfusionMatrixDisplay(confusion_matrix=cm,\n#                               display_labels=range(10))\n# disp.plot(cmap='Blues')\n# plt.title('Matriz de confusion - Digitos')\n# plt.show()\n#\n# # 3) Par de clases con mas confusion (fuera de la diagonal)\n# import numpy as np\n# cm_sin_diag = cm.copy()\n# np.fill_diagonal(cm_sin_diag, 0)         # ignoramos aciertos\n# i, j = np.unravel_index(cm_sin_diag.argmax(), cm_sin_diag.shape)\n# print(f'Mayor confusion: real={i} predicho como={j} ({cm[i, j]} casos)')\n"},
    {"type": "code", "src": "# Escribe aqui tu codigo (Parte B - Tesseract):\n# import cv2\n# import pytesseract\n\n"},
    {"type": "code", "src": "# === Solucion Parte B ===\n# import cv2\n# import pytesseract\n#\n# # 1) Indicar a pytesseract donde esta el motor en Windows\n# pytesseract.pytesseract.tesseract_cmd = (\n#     r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'\n# )\n#\n# # 2) Comprobar idiomas instalados (debe aparecer 'spa')\n# print('Idiomas disponibles:', pytesseract.get_languages())\n#\n# # 3) Cargar imagen con texto desde res/\n# img = cv2.imread('res/texto.png')\n#\n# # --- 3a) OCR sin preprocesar (resultado base) ---\n# texto_crudo = pytesseract.image_to_string(img, lang='spa')\n# print('--- SIN preprocesado ---')\n# print(texto_crudo)\n#\n# # --- 3b) OCR con preprocesado: gris + Otsu ---\n# gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\n# # Otsu calcula el umbral optimo automaticamente\n# _, binaria = cv2.threshold(\n#     gris, 0, 255,\n#     cv2.THRESH_BINARY + cv2.THRESH_OTSU\n# )\n# # PSM 6 = bloque uniforme de texto\n# config = r'--oem 3 --psm 6'\n# texto_limpio = pytesseract.image_to_string(\n#     binaria, lang='spa', config=config\n# )\n# print('--- CON preprocesado ---')\n# print(texto_limpio)\n#\n# # 4) Cajas de cada palabra (bounding boxes y confianza)\n# datos = pytesseract.image_to_data(\n#     binaria, lang='spa', output_type=pytesseract.Output.DICT\n# )\n# for i, palabra in enumerate(datos['text']):\n#     conf = datos['conf'][i]\n#     # Solo palabras con confianza > 60 y no vacias\n#     if palabra.strip() and float(conf) > 60:\n#         x, y, w, h = (datos['left'][i], datos['top'][i],\n#                       datos['width'][i], datos['height'][i])\n#         print(f'{palabra!r}  conf={conf}  box=({x},{y},{w},{h})')\n"},
]))


enhance(NB, plan)
print("Done.")

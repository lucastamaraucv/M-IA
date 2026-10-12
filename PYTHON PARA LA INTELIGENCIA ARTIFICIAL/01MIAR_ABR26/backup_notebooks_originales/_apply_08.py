"""Aplica mejoras al notebook 08 NumPy con teoria detallada y bloques de colores."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, dato, aviso
import json

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_08_NumPy.ipynb"

nb = json.load(open(NB, encoding="utf-8"))


def find_id(fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if fragment in src:
            return c["id"]
    return None


ID_TITULO       = nb["cells"][0]["id"]
ID_NDARRAY      = find_id("# NumPy ndarray")
ID_PERF         = find_id("Performance Sample")
ID_CREATE       = find_id("Formas de crear ndarrays")
ID_INFO         = find_id("Obtener informaci")
ID_RESHAPE      = find_id("Redimensionar los datos")
ID_MANIP        = find_id("Manipulaci")
ID_INDEX        = find_id("# Índices y slicing")
ID_BROADCAST    = find_id("## Broadcasting")
ID_MATH         = find_id("Funciones matem")
ID_STATS        = find_id("Estadística descriptiva")
ID_LINALG       = find_id("Álgebra lineal")
ID_FILTER       = find_id("Filtrado de datos")
ID_RANDOM       = find_id("# Números aleatorios")
ID_SEED         = find_id("Random seed")
ID_NPY          = find_id("Escritura y lectura")


plan = []

# ===== INTRO al notebook =====
plan.append((ID_TITULO, [
    {"type": "md", "src": teoria(
        "Como leer este notebook (mejorado)",
        """Este notebook fue **enriquecido** con bloques de colores. Cada vez que veas:

- <span style="color:#1864ab"><b>AZUL = TEORIA</b></span> -> explicacion en palabras simples del concepto.
- <span style="color:#a05a00"><b>AMARILLO = TU TURNO</b></span> -> ejercicio que TU resuelves en la celda vacia siguiente.
- <span style="color:#1b5e20"><b>VERDE = SOLUCION</b></span> -> codigo de referencia comentado.
- <span style="color:#4c2d9e"><b>VIOLETA = PARA RECORDAR</b></span> -> apunte clave.
- <span style="color:#7d1818"><b>ROJO = CUIDADO</b></span> -> trampas frecuentes.

**NumPy es la libreria mas importante de toda la stack de IA en Python.** Pandas, scikit-learn, TensorFlow, PyTorch -> todos usan arrays NumPy por debajo. Si dominas NumPy, dominas el resto."""
    )},
]))

# ===== NDARRAY =====
plan.append((ID_NDARRAY, [
    {"type": "md", "src": teoria(
        "Que es un ndarray?",
        """`ndarray` significa **N-dimensional array**: una caja que guarda numeros (o booleanos) en una **tabla de N dimensiones**.

#### Comparacion mental rapida

| Dimensiones | Como lo llamamos | Ejemplo |
|---|---|---|
| 0-D | escalar | `np.array(5)` |
| 1-D | vector | `np.array([1, 2, 3])` |
| 2-D | matriz | `np.array([[1,2],[3,4]])` |
| 3-D | tensor | imagen RGB: alto x ancho x 3 canales |
| N-D | tensor general | un batch de imagenes: 32 x 224 x 224 x 3 |

#### Por que NO usar listas Python?

| Aspecto | `list` | `ndarray` |
|---|---|---|
| **Tipo** | Heterogenea (mezcla cualquier cosa) | Homogenea (UN solo dtype) |
| **Memoria** | Cada elemento es un objeto Python (~28 B) | Numeros raw uno detras de otro |
| **Velocidad** | Bucles en Python | Bucles internos en C |
| **Operaciones** | `[x*2 for x in lista]` | `arr * 2` (vectorizado) |
| **Multidimensional** | Listas de listas (lento) | Nativo |

> **Regla de oro:** si vas a hacer matematicas con muchos datos, usa NumPy. Para todo lo demas, usa list/dict.

#### Atributos clave de un ndarray

```python
import numpy as np
a = np.array([[1, 2, 3], [4, 5, 6]])

a.ndim       # 2          (numero de dimensiones)
a.shape      # (2, 3)     (filas, columnas)
a.size       # 6          (total de elementos)
a.dtype      # dtype('int64')   (tipo de dato)
a.itemsize   # 8          (bytes por elemento)
a.nbytes     # 48         (memoria total)
```"""
    )},
]))

# ===== PERFORMANCE =====
plan.append((ID_PERF, [
    {"type": "md", "src": teoria(
        "Por que NumPy es brutalmente mas rapido?",
        """Tres razones tecnicas:

1. **Memoria contigua**: los numeros estan uno al lado del otro en RAM. La CPU los puede leer en bloque (cache friendly).
2. **Sin overhead de objetos Python**: cada `int` en una lista lleva una cabecera de ~28 bytes. En NumPy son 8 bytes raw.
3. **Vectorizacion en C/SIMD**: los bucles internos estan compilados y usan instrucciones de hardware paralelas.

En IA, esta diferencia significa que un entrenamiento que con bucles puros tardaria semanas, en NumPy tarda horas. **Vectorizar = nunca escribir bucles `for` con datos numericos**."""
    )},
    {"type": "md", "src": tu_turno(1,
        """Crea dos secuencias de UN MILLON de numeros, una como lista Python y otra como `np.arange(1_000_000)`. Suma 100 a cada elemento de las dos formas. Mide el tiempo con `%time` (en Jupyter) o con `time.perf_counter()`. Imprime ambos tiempos y calcula cuantas veces mas rapido fue NumPy."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np, time\n# arr = np.arange(1_000_000)\n# lst = list(range(1_000_000))\n#\n# t0 = time.perf_counter()\n# arr2 = arr + 100\n# t_np = time.perf_counter() - t0\n#\n# t0 = time.perf_counter()\n# lst2 = [x + 100 for x in lst]\n# t_py = time.perf_counter() - t0\n#\n# print(f'NumPy: {t_np:.4f}s | Python: {t_py:.4f}s | NumPy fue {t_py/t_np:.1f}x mas rapido')\n"},
]))

# ===== CREAR ARRAYS =====
plan.append((ID_CREATE, [
    {"type": "md", "src": teoria(
        "Las 10 formas mas usadas de crear un array",
        """| Funcion | Que hace | Ejemplo |
|---|---|---|
| `np.array(...)` | desde lista/tupla | `np.array([1,2,3])` |
| `np.zeros(shape)` | array de ceros | `np.zeros((3,4))` -> matriz 3x4 de 0.0 |
| `np.ones(shape)` | array de unos | `np.ones((2,2))` |
| `np.full(shape, x)` | array de un valor | `np.full((3,3), 7)` |
| `np.empty(shape)` | sin inicializar (rapido pero basura) | `np.empty((1000,))` |
| `np.arange(start, stop, step)` | rango (como `range`) | `np.arange(0, 10, 2)` -> [0,2,4,6,8] |
| `np.linspace(start, stop, n)` | n puntos equiespaciados | `np.linspace(0, 1, 5)` -> [0, .25, .5, .75, 1] |
| `np.eye(n)` | matriz identidad NxN | `np.eye(3)` |
| `np.random.rand(shape)` | aleatorios uniformes [0,1) | `np.random.rand(3,3)` |
| `np.random.randn(shape)` | aleatorios normales (mu=0, sigma=1) | `np.random.randn(100)` |

#### Especificar dtype

```python
np.zeros(10, dtype=np.int32)
np.ones((3,3), dtype=np.float32)
np.array([1, 2, 3], dtype=bool)   # [True, True, True]
```

> **Importante en IA:** `float32` ocupa la mitad que `float64`. Si tu modelo no necesita precision extra, usa `float32` (es lo que esperan las GPUs)."""
    )},
    {"type": "md", "src": tu_turno(2,
        """Crea las siguientes estructuras:

1. Vector de 10 ceros (`v0`).
2. Matriz 4x4 de unos (`m1`).
3. Matriz identidad 5x5 (`ident`).
4. Vector con los numeros del 0 al 50 con paso 5 (`pasos`).
5. Vector de 11 puntos equiespaciados entre -1 y 1 (`equi`).

Imprime cada uno y su `shape`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# v0    = np.zeros(10)\n# m1    = np.ones((4, 4))\n# ident = np.eye(5)\n# pasos = np.arange(0, 51, 5)\n# equi  = np.linspace(-1, 1, 11)\n#\n# for nombre, arr in [('v0',v0), ('m1',m1), ('ident',ident), ('pasos',pasos), ('equi',equi)]:\n#     print(nombre, arr.shape)\n#     print(arr)\n#     print('---')\n"},
]))

# ===== INFO =====
plan.append((ID_INFO, [
    {"type": "md", "src": teoria(
        "Atributos vs metodos: que es shape, ndim, size, dtype",
        """Un ndarray tiene varios **atributos** (no llevan parentesis) que te dicen su forma:

| Atributo | Devuelve | Ejemplo (`a` es 3x4) |
|---|---|---|
| `a.ndim` | dimensiones | `2` |
| `a.shape` | tupla de tamanos por dimension | `(3, 4)` |
| `a.size` | total de elementos | `12` |
| `a.dtype` | tipo de cada elemento | `dtype('float64')` |
| `a.itemsize` | bytes por elemento | `8` |
| `a.nbytes` | bytes totales | `96` |
| `a.T` | la traspuesta (no copia) | array 4x3 |

Confusion frecuente: `a.shape` NO es lo mismo que `len(a)`. `len(a)` te da SOLO la primera dimension. Usa `a.shape` para todo."""
    )},
    {"type": "md", "src": tu_turno(3,
        """Crea un array bidimensional `m` con `np.arange(24).reshape(4, 6)`. Imprime: `ndim`, `shape`, `size`, `dtype`, `itemsize`, `nbytes`. Luego imprime tambien `len(m)` y compara con `m.shape[0]`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# m = np.arange(24).reshape(4, 6)\n# print('ndim:    ', m.ndim)\n# print('shape:   ', m.shape)\n# print('size:    ', m.size)\n# print('dtype:   ', m.dtype)\n# print('itemsize:', m.itemsize)\n# print('nbytes:  ', m.nbytes)\n# print('len:     ', len(m))      # 4 (primera dim)\n# print('shape[0]:', m.shape[0])  # 4 (idem)\n"},
]))

# ===== RESHAPE =====
plan.append((ID_RESHAPE, [
    {"type": "md", "src": teoria(
        "Redimensionar: reshape, ravel, flatten",
        """`reshape` cambia la forma del array **sin cambiar los datos**. Solo necesita que el numero total de elementos cuadre.

```python
a = np.arange(12)        # shape (12,)
a.reshape(3, 4)          # shape (3, 4)
a.reshape(2, 2, 3)       # shape (2, 2, 3)
a.reshape(-1, 4)         # -1 = "calcula tu", aqui sale (3, 4)
a.reshape(4, -1)         # (4, 3)
```

| Metodo | Que hace |
|---|---|
| `a.reshape(...)` | Devuelve una **vista** (sin copiar memoria) si es posible. |
| `a.ravel()` | Devuelve una vista 1D. |
| `a.flatten()` | Devuelve una **copia** 1D. |
| `a.T` | Traspuesta. |

#### Vista vs copia

Una **vista** es un array que comparte la memoria con el original: si modificas la vista, **modificas el original**.

```python
a = np.arange(12)
b = a.reshape(3, 4)   # vista
b[0, 0] = 99
print(a)              # tambien cambio: a[0] = 99

c = a.flatten()       # copia
c[0] = -1
print(a)              # NO cambio
```"""
    )},
    {"type": "md", "src": tu_turno(4,
        """Crea `arr = np.arange(20)`. Reshape-ea a una matriz de 4 filas (deja a NumPy calcular las columnas con `-1`). Llamala `M`. Imprime `M`, su `shape` y `M.T` (traspuesta)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# arr = np.arange(20)\n# M = arr.reshape(4, -1)\n# print('shape:', M.shape)\n# print(M)\n# print('Traspuesta:')\n# print(M.T)\n"},
]))

# ===== INDEX y SLICING =====
plan.append((ID_INDEX, [
    {"type": "md", "src": teoria(
        "Indexacion y slicing: la sintaxis mas potente de NumPy",
        """NumPy soporta **mucho** mas que las listas Python. Aprenderlo bien te evita escribir bucles.

#### 1. Acceso por indice (clasico)

```python
a = np.array([10, 20, 30, 40])
a[0]      # 10
a[-1]     # 40

m = np.array([[1,2,3], [4,5,6]])
m[1, 2]   # 6     (fila 1, columna 2)  -- NO uses m[1][2], es mas lento
```

#### 2. Slicing (rebanadas)

```python
a[1:3]            # [20, 30]
a[::-1]           # invertir
m[0]              # primera fila completa: [1,2,3]
m[:, 0]           # primera columna entera: [1, 4]
m[0:2, 1:3]       # submatriz
```

#### 3. Fancy indexing (con array de indices)

```python
a = np.array([10, 20, 30, 40, 50])
a[[0, 2, 4]]      # [10, 30, 50]   -- saca posiciones especificas
```

#### 4. Boolean indexing (con mascara)

```python
a = np.array([1, 5, 10, 15, 20])
a > 10            # array([False, False, False, True, True])
a[a > 10]         # array([15, 20])

# Combinaciones (fijate: usar & y |, NO and/or!)
a[(a > 5) & (a < 20)]
```

> **CUIDADO:** los `slices` son **vistas** (modificarlos modifica el original). Los `fancy` y `boolean` siempre devuelven **copias**.

#### Diferencia con listas Python

```python
# Listas:
[1,2,3,4][1:3]    # [2, 3] (copia)

# NumPy slice:
arr = np.array([1,2,3,4])
sub = arr[1:3]    # vista
sub[0] = 99       # arr tambien cambia!
```"""
    )},
    {"type": "md", "src": tu_turno(5,
        """Crea la matriz `M = np.arange(1, 26).reshape(5, 5)`. Es decir:
```
[[ 1,  2,  3,  4,  5],
 [ 6,  7,  8,  9, 10],
 [11, 12, 13, 14, 15],
 [16, 17, 18, 19, 20],
 [21, 22, 23, 24, 25]]
```

Extrae con slicing:

1. La **tercera fila** completa.
2. La **ultima columna** completa.
3. La **submatriz central 3x3** (filas 1-3, columnas 1-3).
4. Solo los elementos **mayores que 15** (boolean indexing).
5. Los elementos en posiciones `(0,0)`, `(2,2)`, `(4,4)` (la diagonal). Pista: usa fancy con dos arrays."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# M = np.arange(1, 26).reshape(5, 5)\n# print('Tercera fila:', M[2])\n# print('Ultima columna:', M[:, -1])\n# print('Submatriz central:')\n# print(M[1:4, 1:4])\n# print('Mayores que 15:', M[M > 15])\n# print('Diagonal:', M[[0,1,2,3,4], [0,1,2,3,4]])\n# # Tambien: print(np.diag(M))\n"},
]))

# ===== BROADCASTING =====
plan.append((ID_BROADCAST, [
    {"type": "md", "src": teoria(
        "Broadcasting: la magia que hace que NumPy sea facil",
        """**Broadcasting** es la regla que permite operar arrays de tamanos distintos sin tener que repetir manualmente.

#### Caso simple: array + escalar

```python
a = np.array([1, 2, 3])
a + 10     # [11, 12, 13]   <- el 10 se "expande" a cada elemento
```

#### Caso medio: matriz + vector

```python
m = np.array([[1, 2, 3], [4, 5, 6]])      # shape (2, 3)
v = np.array([10, 20, 30])                 # shape (3,)
m + v      # cada fila se suma con v
# [[11, 22, 33],
#  [14, 25, 36]]
```

#### La REGLA de broadcasting

NumPy alinea los shapes **por la derecha** y mira dimension a dimension. Una dimension es **compatible** si:
- Es **igual** a la otra, o
- Es **1**, o
- **No existe** (se considera 1).

Si TODAS las dimensiones son compatibles, broadcasting funciona.

| Shape A | Shape B | Resultado |
|---|---|---|
| `(3, 4)` | `(4,)` | `(3, 4)` -> OK |
| `(3, 4)` | `(3, 1)` | `(3, 4)` -> OK |
| `(3, 4)` | `(3,)` | ERROR (4 vs 3 no compatibles) |
| `(2, 3, 4)` | `(4,)` | `(2, 3, 4)` -> OK |
| `(2, 3, 4)` | `(3, 4)` | `(2, 3, 4)` -> OK |
| `(2, 3, 4)` | `(2, 1, 4)` | `(2, 3, 4)` -> OK |

#### Caso practico tipico: normalizar columnas

```python
X = np.random.rand(100, 5)        # 100 filas, 5 columnas
medias = X.mean(axis=0)           # shape (5,)
desv  = X.std(axis=0)             # shape (5,)
X_norm = (X - medias) / desv      # broadcasting: cada columna se normaliza
```

> **En IA esto es CRITICO**: normalizar features, restar medias, escalar imagenes, anadir bias en redes neuronales -> todo es broadcasting."""
    )},
    {"type": "md", "src": tu_turno(6,
        """Tienes una matriz `X` de 4 filas y 3 columnas con `np.arange(12).reshape(4, 3)`. Calcula:

1. La **media de cada columna** (con `axis=0`). Pista: el resultado tiene shape `(3,)`.
2. **Resta** esa media a `X` (broadcasting). Llama al resultado `X_centrado`.
3. Verifica que la media de `X_centrado` por columna ahora es practicamente 0."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# X = np.arange(12).reshape(4, 3).astype(float)\n# print('X:'); print(X)\n# medias = X.mean(axis=0)\n# print('Medias por columna:', medias)\n# X_centrado = X - medias\n# print('X_centrado:'); print(X_centrado)\n# print('Media de X_centrado:', X_centrado.mean(axis=0))   # ~0\n"},
]))

# ===== ESTADISTICA =====
plan.append((ID_STATS, [
    {"type": "md", "src": teoria(
        "Estadistica descriptiva en una linea",
        """NumPy trae todas las estadisticas basicas. La clave es el parametro **`axis`**.

| Funcion | Que calcula |
|---|---|
| `np.mean(a)` / `a.mean()` | media |
| `np.median(a)` | mediana |
| `np.std(a)` / `a.std()` | desviacion estandar |
| `np.var(a)` / `a.var()` | varianza |
| `np.min(a)` / `a.min()` | minimo |
| `np.max(a)` / `a.max()` | maximo |
| `np.sum(a)` / `a.sum()` | suma |
| `np.prod(a)` | producto |
| `np.argmin(a)` | indice del minimo |
| `np.argmax(a)` | indice del maximo |
| `np.percentile(a, 50)` | percentil (50 = mediana) |
| `np.unique(a)` | valores unicos |

#### El parametro <code>axis</code>

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])

m.sum()           # 21       (sum de todo)
m.sum(axis=0)     # [5, 7, 9]    (sum por columna -- una suma por columna)
m.sum(axis=1)     # [6, 15]      (sum por fila)
```

> **Truco mnemotecnico:** `axis=0` colapsa filas (se mueve a lo largo del eje 0 = filas), `axis=1` colapsa columnas. **El eje que pasas es el que DESAPARECE.**"""
    )},
    {"type": "md", "src": tu_turno(7,
        """Crea una matriz de notas `notas = np.array([[7, 8, 9, 6], [5, 7, 8, 4], [9, 9, 10, 8]])`. Cada fila es un alumno, cada columna una asignatura. Calcula:

1. Media de cada **alumno** (axis=1).
2. Media de cada **asignatura** (axis=0).
3. Asignatura con mayor media (con `argmax`).
4. Indice del alumno con mejor media."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# notas = np.array([[7, 8, 9, 6], [5, 7, 8, 4], [9, 9, 10, 8]])\n#\n# media_alumno    = notas.mean(axis=1)\n# media_asig      = notas.mean(axis=0)\n# print('Media por alumno:    ', media_alumno)\n# print('Media por asignatura:', media_asig)\n# print('Asignatura top idx:  ', np.argmax(media_asig))\n# print('Alumno top idx:      ', np.argmax(media_alumno))\n"},
]))

# ===== ALGEBRA LINEAL =====
plan.append((ID_LINALG, [
    {"type": "md", "src": teoria(
        "Algebra lineal: el corazon del Machine Learning",
        """**`np.linalg`** es el submodulo de algebra lineal. En IA literalmente todo se reduce a productos de matrices.

#### Producto de matrices

| Operador | Que hace | Equivalente |
|---|---|---|
| `A @ B` | producto matricial (Python 3.5+) | `np.matmul(A, B)` |
| `np.dot(A, B)` | producto matricial / interno | igual que `@` para 2D |
| `A * B` | producto **elemento a elemento** (broadcasting) | NO matricial |

```python
A = np.array([[1, 2], [3, 4]])     # 2x2
B = np.array([[5, 6], [7, 8]])     # 2x2

A @ B          # producto matricial
A * B          # elemento a elemento
```

#### Funciones utiles de `np.linalg`

```python
np.linalg.inv(A)          # inversa
np.linalg.det(A)          # determinante
np.linalg.eig(A)          # autovalores y autovectores
np.linalg.solve(A, b)     # resuelve Ax = b
np.linalg.norm(v)         # norma euclidea (longitud de un vector)
np.linalg.matrix_rank(A)  # rango
np.trace(A)               # traza (suma de la diagonal)
```

#### Ejemplo: regresion lineal manual

```python
# Resolver y = X*w por minimos cuadrados:
# w = (X^T X)^(-1) X^T y
w = np.linalg.inv(X.T @ X) @ X.T @ y
```

Esto es lo que scikit-learn hace por dentro en `LinearRegression`."""
    )},
    {"type": "md", "src": tu_turno(8,
        """Crea dos matrices aleatorias de 3x3 (`A` y `B`) usando `np.random.rand(3, 3)`. Calcula:

1. `A @ B` (producto matricial).
2. `A * B` (elemento a elemento) -- comprueba que es DIFERENTE del anterior.
3. La inversa de A (`np.linalg.inv(A)`).
4. Verifica que `A @ inv(A)` te da la **identidad** (con `np.allclose` para comparar floats)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# np.random.seed(42)\n# A = np.random.rand(3, 3)\n# B = np.random.rand(3, 3)\n#\n# print('A @ B:'); print(A @ B)\n# print('A * B (elem-wise):'); print(A * B)\n#\n# A_inv = np.linalg.inv(A)\n# print('A @ A_inv =~ identidad:', np.allclose(A @ A_inv, np.eye(3)))\n"},
]))

# ===== FILTRADO =====
plan.append((ID_FILTER, [
    {"type": "md", "src": teoria(
        "Filtrado de datos con mascaras booleanas",
        """**Idea central:** una **mascara** es un array booleano del mismo tamano que tus datos. Donde la mascara es `True`, el dato pasa; donde es `False`, se filtra.

```python
edades = np.array([15, 22, 47, 19, 30, 8])

mayores = edades >= 18         # array de bool
print(mayores)                 # [False, True, True, True, True, False]
edades[mayores]                # [22, 47, 19, 30]
```

#### Combinar mascaras

Usa `&` (and), `|` (or), `~` (not). **NUNCA** `and`/`or`/`not` (esos son para booleanos sueltos, no para arrays).

```python
adultos_jovenes = edades[(edades >= 18) & (edades < 30)]
no_menores      = edades[~(edades < 18)]
```

> Pon **siempre** parentesis alrededor de cada condicion: `(a > x) & (b < y)`. La precedencia de `&` es muy alta y rompe expresiones sin parentesis.

#### Funciones relacionadas

| Funcion | Que hace |
|---|---|
| `np.where(cond, A, B)` | devuelve `A` donde `cond` es True, `B` donde es False |
| `np.where(cond)` | devuelve los **indices** donde `cond` es True |
| `np.nonzero(a)` | indices de elementos no cero |
| `np.any(a)` | True si hay al menos uno True |
| `np.all(a)` | True solo si TODOS son True |"""
    )},
    {"type": "md", "src": tu_turno(9,
        """Tienes datos de temperatura: `temps = np.array([12, 18, 25, 30, 8, 22, 35, 5, 16, 28])`. Resuelve:

1. Cuenta cuantos dias tuvieron temperatura `>= 20` (usa `.sum()` sobre la mascara).
2. Extrae las temperaturas entre 15 y 25 (incluidos).
3. Crea un array `etiquetas` que ponga `'caliente'` si `>= 25`, `'frio'` si `<= 10`, y `'templado'` en cualquier otro caso. Usa `np.where` anidados o `np.select`.

> Pista: para 3, busca `np.select(condlist, choicelist, default)`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# temps = np.array([12, 18, 25, 30, 8, 22, 35, 5, 16, 28])\n#\n# print('Dias >=20:', (temps >= 20).sum())\n# print('Entre 15 y 25:', temps[(temps >= 15) & (temps <= 25)])\n#\n# etiquetas = np.select(\n#     [temps >= 25, temps <= 10],\n#     ['caliente', 'frio'],\n#     default='templado'\n# )\n# print(etiquetas)\n"},
]))

# ===== RANDOM =====
plan.append((ID_RANDOM, [
    {"type": "md", "src": teoria(
        "Numeros aleatorios: <code>np.random</code>",
        """En IA necesitamos **muchos** numeros aleatorios: inicializacion de pesos, particionar train/test, data augmentation, dropout, etc.

#### Generadores mas usados

| Funcion | Genera |
|---|---|
| `np.random.rand(*shape)` | uniformes en [0, 1) |
| `np.random.randn(*shape)` | normales N(0, 1) |
| `np.random.randint(low, high, size)` | enteros en [low, high) |
| `np.random.uniform(low, high, size)` | uniformes en [low, high) |
| `np.random.normal(mu, sigma, size)` | normales con media mu y std sigma |
| `np.random.choice(arr, size, replace, p)` | elementos de un array |
| `np.random.shuffle(arr)` | mezcla in-place |
| `np.random.permutation(arr)` | devuelve copia mezclada |

#### API moderna (NumPy >= 1.17, recomendada)

```python
rng = np.random.default_rng(seed=42)
rng.random((3, 3))
rng.normal(0, 1, 100)
rng.integers(0, 10, size=20)
```

Es mas robusta y reproducible que `np.random.*` directamente."""
    )},
]))

# ===== SEED =====
plan.append((ID_SEED, [
    {"type": "md", "src": teoria(
        "Random seed: la base de la reproducibilidad",
        """Sin seed, cada vez que corras el codigo obtienes numeros distintos. Para que tus experimentos sean **reproducibles** (paper, comparativa, debugging), fija una semilla:

```python
np.random.seed(42)
np.random.rand(5)   # mismos numeros cada vez

# o con la API moderna:
rng = np.random.default_rng(42)
rng.random(5)       # mismos numeros cada vez
```

> **En IA:** fija la seed al principio del notebook. Si comparas dos modelos y no fijas seed, **no sabes si la diferencia es real o azar**.

> **CUIDADO:** la seed de NumPy NO afecta a la seed de Python (`random.seed`), ni a la de TensorFlow, PyTorch o sklearn. Si quieres reproducibilidad TOTAL fija las cuatro."""
    )},
    {"type": "md", "src": tu_turno(10,
        """1. Sin fijar seed, genera 5 numeros aleatorios con `np.random.rand(5)`. Hazlo dos veces. Ves que cambian.
2. Ahora fija seed con `np.random.seed(123)` ANTES de cada llamada y repite. Comprueba que ahora los numeros son **identicos**.
3. Bonus: usa la API moderna `rng = np.random.default_rng(123)` y haz lo mismo."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n#\n# # Sin seed\n# print('Sin seed 1:', np.random.rand(5))\n# print('Sin seed 2:', np.random.rand(5))   # diferente\n#\n# # Con seed\n# np.random.seed(123); print('Con seed 1:', np.random.rand(5))\n# np.random.seed(123); print('Con seed 2:', np.random.rand(5))   # igual\n#\n# # API moderna\n# rng = np.random.default_rng(123)\n# print('rng 1:', rng.random(5))\n"},
]))

# ===== NPY save/load =====
plan.append((ID_NPY, [
    {"type": "md", "src": teoria(
        "Guardar y cargar arrays: <code>.npy</code> y <code>.npz</code>",
        """Cuando trabajas con datasets grandes, guardarlos como CSV es **muy lento**. NumPy tiene su propio formato binario.

| Funcion | Para que |
|---|---|
| `np.save('archivo.npy', arr)` | guarda UN array (formato binario) |
| `np.load('archivo.npy')` | carga UN array |
| `np.savez('archivo.npz', a=arr1, b=arr2)` | varios arrays comprimidos |
| `np.savez_compressed(...)` | igual, con mejor compresion |
| `np.savetxt('a.csv', arr, delimiter=',')` | exporta a CSV (lento, solo si lo necesitas) |
| `np.loadtxt('a.csv', delimiter=',')` | lee CSV |

#### Por que .npy y no CSV?

- **Velocidad**: .npy es ~100x mas rapido que CSV con NumPy.
- **Tamano**: ocupa menos (binario vs texto).
- **Conserva el dtype**: el CSV convierte todo a texto y luego tienes que parsear.
- **Multidimensional**: CSV solo soporta 2D, .npy guarda cualquier shape (3D, 4D, ...).

#### Limitaciones

- Solo NumPy puede leerlo facilmente. Para compartir con otros sistemas, usa CSV o HDF5.
- No es portable entre versiones muy distantes de NumPy."""
    )},
    {"type": "md", "src": tu_turno(11,
        """1. Crea una matriz `M = np.random.rand(1000, 1000)`.
2. Guardala en `'mi_matriz.npy'` con `np.save`.
3. Cargala de vuelta en una variable `M2`.
4. Verifica con `np.array_equal(M, M2)` que es identica.
5. Bonus: borra el archivo con `os.remove('mi_matriz.npy')` para limpiar."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np, os\n# M = np.random.rand(1000, 1000)\n# np.save('mi_matriz.npy', M)\n# M2 = np.load('mi_matriz.npy')\n# print('Iguales:', np.array_equal(M, M2))\n# print('Tamano del archivo:', os.path.getsize('mi_matriz.npy'), 'bytes')\n# os.remove('mi_matriz.npy')\n"},
]))


enhance(NB, plan)
print("Done.")

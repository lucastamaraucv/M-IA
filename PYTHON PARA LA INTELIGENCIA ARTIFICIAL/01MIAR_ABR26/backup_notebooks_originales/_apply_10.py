"""Aplica mejoras al notebook 10 (+Pandas) con bloques de colores y teoria detallada."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, solucion_md, dato, aviso
import json

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_10_+Pandas.ipynb"

nb = json.load(open(NB, encoding="utf-8"))


def find_id(text_fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if text_fragment in src:
            return c["id"]
    return None


# IDs ancla
ID_TITULO        = nb["cells"][0]["id"]
ID_OPER_PANDAS   = find_id("# Operaciones en pandas")
ID_BUSQUEDA      = find_id("Busqueda") or find_id("squeda")
ID_ORDENACION    = find_id("Ordenaci")
ID_RANKING       = find_id("Ranking")
ID_OPERACIONES   = find_id("# Operaciones")
ID_OPS_SERIES    = find_id("Operaciones entre Series")
ID_APPLY         = find_id("apply")
ID_ESTAD         = find_id("# Estad")
ID_AGREGACIONES  = find_id("## Agregaciones")
ID_CORRELACIONES = find_id("## Correlaciones")
ID_CORR_TODOS    = find_id("Correlaciones entre todos")
ID_EJERCICIOS    = find_id("## Ejercicios")


plan = []

# -------- INTRO al notebook --------
plan.append((ID_TITULO, [
    {"type": "md", "src": teoria(
        "Como leer este notebook (version mejorada)",
        """Este notebook fue **enriquecido** para ayudarte a aprender escribiendo codigo. Vas a encontrar tres tipos de bloques de colores:

<div style="background-color:#e7f5ff;border-left:6px solid #1c7ed6;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AZUL = TEORIA</b></div> -> explicacion en palabras simples antes de cada concepto.

<div style="background-color:#fff9db;border-left:6px solid #f59f00;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AMARILLO = TU TURNO</b></div> -> el ejercicio que TU debes resolver. Hay una celda vacia debajo donde escribes el codigo.

<div style="background-color:#ebfbee;border-left:6px solid #2f9e44;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>VERDE = SOLUCION</b></div> -> codigo de referencia comentado por si te trabas. Destapa solo despues de intentar.

> **Promesa**: las celdas y la teoria del profesor original NO se han tocado. Solo se han ANADIDO bloques. Asi puedes seguir la version original cuando quieras.

#### De que trata este notebook 10
Este es el segundo notebook de Pandas y se centra en **lo que hace a Pandas tan potente para analisis de datos**:

| Bloque | Idea clave |
|---|---|
| Operaciones | Aritmetica entre DataFrames y Series, alineacion automatica por etiquetas. |
| `apply` | Aplicar una funcion a cada fila o columna. |
| Estadistica descriptiva | `describe`, `mean`, `std`, `idxmax`... la chuleta del analista. |
| **Agregaciones (`groupby`)** | El concepto **mas importante** de Pandas: dividir, calcular y combinar. |
| Correlaciones | Relacion lineal entre variables numericas, base del feature engineering. |"""
    )},
]))

# ============ OPERACIONES EN PANDAS ============
plan.append((ID_OPER_PANDAS, [
    {"type": "md", "src": teoria(
        "Operaciones en Pandas: idea general",
        """Pandas combina dos cosas:

1. La **velocidad de NumPy** (operaciones vectorizadas en C, sin bucles Python).
2. Las **etiquetas** (nombres de filas y columnas) que te permiten trabajar de forma legible.

#### Operaciones vectorizadas
En Pandas, cuando haces `df + 1`, **se suma 1 a cada celda** sin que tu escribas un bucle. Esto es:

- **Mas rapido** que un `for` en Python (cientos a miles de veces).
- **Mas legible**: una linea expresa la intencion.
- **Mas seguro**: NumPy/Pandas se encargan de dimensiones, NaN, dtypes.

```python
df['precio'] * 1.21         # IVA aplicado a toda la columna
df['edad'] + df['hijos']    # suma columna a columna
df > 0                      # mascara booleana del mismo tamano
```

#### Alineacion por etiquetas
Cuando operas dos DataFrames, Pandas **alinea por nombre de fila/columna**, no por posicion. Si una etiqueta no existe en uno de los dos, el resultado es `NaN` (a menos que uses `fill_value`).

```python
A + B   # alinea por indice y columna; donde no coincide -> NaN
A.add(B, fill_value=0)   # rellena con 0 lo que falte en uno de los dos
```

> Esta es la diferencia clave con NumPy: NumPy se basa en posiciones, Pandas en etiquetas."""
    )},
]))

# ============ BUSQUEDA ============
if ID_BUSQUEDA:
    plan.append((ID_BUSQUEDA, [
        {"type": "md", "src": teoria(
            "Busqueda en DataFrames: in, isin, mascaras booleanas",
            """Tres formas tipicas de **buscar** en un DataFrame:

| Forma | Para que sirve | Ejemplo |
|---|---|---|
| `'colname' in df` | Ver si existe una **columna**. | `'edad' in df` |
| `df.isin([v1, v2])` | Mascara booleana: True donde el valor **esta en la lista**. | `df.isin([2, 3, 4])` |
| `df['col'] == valor` | Mascara booleana sobre **una columna**. | `df['edad'] > 30` |
| `df.query("...")` | Filtro por expresion tipo SQL. | `df.query("edad > 30")` |

#### Mascaras booleanas: el patron rey de Pandas
Una **mascara** es un DataFrame (o Serie) del mismo tamano lleno de `True`/`False`. La usas para:

```python
# 1. Filtrar filas
df[df['edad'] > 30]

# 2. Contar cuantos True hay (True == 1)
(df['edad'] > 30).sum()

# 3. Reemplazar valores que cumplan una condicion
df.loc[df['edad'] < 18, 'categoria'] = 'menor'

# 4. Combinar mascaras con &, |, ~  (NO uses and/or/not con Pandas)
df[(df['edad'] > 30) & (df['ciudad'] == 'Madrid')]
```

> **Cuidado:** con Pandas se usa `&`, `|`, `~` y los **parentesis son obligatorios** en cada condicion. `and`/`or` lanzan error porque trabajan con un solo bool, no con un Series."""
        )},
        {"type": "md", "src": tu_turno(1,
            """Crea un DataFrame de 5 filas y 4 columnas (`A, B, C, D`) con enteros aleatorios entre 0 y 9.

1. Comprueba si la columna `B` existe.
2. Genera una mascara booleana de los valores **mayores que 5**.
3. Cuenta cuantos valores cumplen la condicion **por columna** (suma sobre `axis=0`).
4. Filtra las **filas** donde la columna `A` sea mayor que 5."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\nimport numpy as np\n\nnp.random.seed(0)\ndf = pd.DataFrame(np.random.randint(0, 10, size=(5, 4)), columns=list('ABCD'))\ndisplay(df)\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n# import numpy as np\n#\n# np.random.seed(0)\n# df = pd.DataFrame(np.random.randint(0, 10, size=(5, 4)), columns=list('ABCD'))\n# display(df)\n#\n# # 1) existencia de columna\n# print('B' in df)\n#\n# # 2) mascara booleana\n# mask = df > 5\n# display(mask)\n#\n# # 3) contar True por columna (axis=0 es el eje de filas, suma a lo largo de filas)\n# print(mask.sum(axis=0))\n#\n# # 4) filtrar filas con A > 5\n# display(df[df['A'] > 5])\n"},
    ]))

# ============ ORDENACION ============
if ID_ORDENACION:
    plan.append((ID_ORDENACION, [
        {"type": "md", "src": teoria(
            "Ordenacion: sort_index vs sort_values",
            """Pandas separa dos cosas que en Excel solemos confundir:

| Metodo | Que ordena | Ejemplo |
|---|---|---|
| `sort_index()` | Ordena por el **indice** (etiquetas de fila o columna). | `df.sort_index()` |
| `sort_values()` | Ordena por **el contenido** de una columna o fila. | `df.sort_values(by='edad')` |

#### Argumentos clave (ambos los aceptan)

| Argumento | Que hace | Valores tipicos |
|---|---|---|
| `axis` | 0 = filas (defecto), 1 = columnas. | `axis=0` o `axis=1` |
| `ascending` | Sentido. | `True` (defecto) o `False` |
| `inplace` | Modifica el DataFrame original o devuelve copia. | `True` o `False` (defecto) |
| `kind` | Algoritmo (`quicksort`, `mergesort`, `stable`). | normalmente lo dejas. |
| `na_position` | Donde poner los NaN. | `'last'` (defecto) o `'first'` |

#### Ejemplos pragmaticos
```python
# Top 5 productos por precio
df.sort_values('precio', ascending=False).head(5)

# Ordenar por dos criterios (primero por ciudad, luego por edad)
df.sort_values(['ciudad', 'edad'])

# Ordenar columnas alfabeticamente
df.sort_index(axis=1)
```

> **Truco:** `sort_values(by=['a','b'], ascending=[True, False])` permite criterios mixtos."""
        )},
        {"type": "md", "src": tu_turno(2,
            """Tienes este DataFrame:

```python
df = pd.DataFrame({
    'producto': ['pan', 'leche', 'queso', 'huevos', 'agua'],
    'precio':   [1.20,   0.95,    4.30,    2.50,     0.50],
    'stock':    [50,     30,      10,      40,       100]
})
```

1. Ordena las filas por **precio descendente**.
2. Ordena por **stock ascendente** y, si empatan, por **precio ascendente**.
3. Ordena las **columnas** alfabeticamente."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\n\ndf = pd.DataFrame({\n    'producto': ['pan', 'leche', 'queso', 'huevos', 'agua'],\n    'precio':   [1.20,   0.95,    4.30,    2.50,     0.50],\n    'stock':    [50,     30,      10,      40,       100]\n})\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n#\n# df = pd.DataFrame({\n#     'producto': ['pan', 'leche', 'queso', 'huevos', 'agua'],\n#     'precio':   [1.20,   0.95,    4.30,    2.50,     0.50],\n#     'stock':    [50,     30,      10,      40,       100]\n# })\n#\n# # 1) precio descendente\n# display(df.sort_values('precio', ascending=False))\n#\n# # 2) stock asc, en empates precio asc\n# display(df.sort_values(['stock', 'precio'], ascending=[True, True]))\n#\n# # 3) columnas alfabeticas\n# display(df.sort_index(axis=1))\n"},
    ]))

# ============ RANKING ============
if ID_RANKING:
    plan.append((ID_RANKING, [
        {"type": "md", "src": teoria(
            "Ranking: rank() y sus metodos de empate",
            """`rank()` te da la **posicion (1, 2, 3...)** de cada valor dentro de una columna o fila. Util para podios, percentiles y normalizacion.

#### Como trata los empates? (parametro `method`)

| `method` | Que hace en empate | Ejemplo: valores `[10, 20, 20, 30]` -> ranks |
|---|---|---|
| `'average'` (defecto) | Promedio de las posiciones | `1, 2.5, 2.5, 4` |
| `'min'` | Posicion mas pequena | `1, 2, 2, 4` |
| `'max'` | Posicion mas grande | `1, 3, 3, 4` |
| `'first'` | Por orden de aparicion | `1, 2, 3, 4` |
| `'dense'` | Como `min`, pero sin huecos | `1, 2, 2, 3` |

#### Otros parametros
- `ascending=True/False`: 1 al menor o al mayor.
- `axis=0/1`: ranquear por columna (defecto) o por fila.
- `pct=True`: devuelve **percentil** en lugar de posicion absoluta.

```python
df['posicion'] = df['puntos'].rank(method='dense', ascending=False)  # podio
df['percentil'] = df['nota'].rank(pct=True)                          # 0..1
```"""
        )},
        {"type": "md", "src": tu_turno(3,
            """Construye un ranking de **alumnos por nota descendente** sobre este DataFrame:

```python
notas = pd.DataFrame({
    'alumno': ['Ana', 'Bea', 'Carlos', 'David', 'Eva'],
    'nota':   [8.5,    9.0,   7.0,      9.0,    8.5]
})
```

1. Anade una columna `posicion` que de la posicion del alumno usando `method='dense'` (sin huecos en empates).
2. Anade otra columna `percentil` con `pct=True`.
3. Ordena el resultado por `posicion` ascendente."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\n\nnotas = pd.DataFrame({\n    'alumno': ['Ana', 'Bea', 'Carlos', 'David', 'Eva'],\n    'nota':   [8.5,    9.0,   7.0,      9.0,    8.5]\n})\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n#\n# notas = pd.DataFrame({\n#     'alumno': ['Ana', 'Bea', 'Carlos', 'David', 'Eva'],\n#     'nota':   [8.5,    9.0,   7.0,      9.0,    8.5]\n# })\n#\n# # rank descendente: el de mas nota recibe posicion 1\n# notas['posicion']  = notas['nota'].rank(method='dense', ascending=False)\n# notas['percentil'] = notas['nota'].rank(pct=True)\n#\n# display(notas.sort_values('posicion'))\n"},
    ]))

# ============ OPERACIONES ENTRE FRAMES ============
if ID_OPERACIONES:
    plan.append((ID_OPERACIONES, [
        {"type": "md", "src": teoria(
            "Operaciones entre DataFrames: alineacion y fill_value",
            """Cuando haces `frameA + frameB`, Pandas:

1. **Alinea** filas y columnas por sus etiquetas (no por posicion).
2. Donde la etiqueta existe en los dos -> calcula.
3. Donde NO coincide -> resultado `NaN`.

```python
A = pd.DataFrame({'x':[1,2], 'y':[3,4]})
B = pd.DataFrame({'x':[10,20], 'z':[100,200]})
A + B
#       x      y      z
# 0    11    NaN    NaN
# 1    22    NaN    NaN
```

#### Metodos en lugar de operadores: la ventaja del `fill_value`

| Operador | Metodo equivalente | Ventaja del metodo |
|---|---|---|
| `+` | `.add(other, fill_value=...)` | Rellenar huecos |
| `-` | `.sub(other, fill_value=...)` | idem |
| `*` | `.mul(other, fill_value=...)` | idem |
| `/` | `.div(other, fill_value=...)` | idem |
| `**` | `.pow(other, fill_value=...)` | idem |

```python
A.add(B, fill_value=0)   # cuando falta una etiqueta en uno de los dos, usa 0
```

> **Por que es util?** Imagina dos meses de ventas en DataFrames con productos distintos. Si haces `enero + febrero`, los productos que solo aparecen en uno daran NaN. Con `fill_value=0` cuentan como cero ventas el otro mes."""
        )},
    ]))

# ============ OPERACIONES SERIES VS DATAFRAMES ============
if ID_OPS_SERIES:
    plan.append((ID_OPS_SERIES, [
        {"type": "md", "src": teoria(
            "Broadcasting: operaciones entre Series y DataFrames",
            """Cuando haces `df - serie`, Pandas hace **broadcasting**: aplica la operacion **fila a fila** o **columna a columna** segun como alineen las etiquetas.

#### Regla general
- Si la Serie tiene los **mismos nombres que las COLUMNAS** del DataFrame -> se aplica **fila a fila** (defecto).
- Si la Serie tiene los **mismos nombres que las FILAS** del DataFrame -> usa el argumento `axis=0`.

```python
df = pd.DataFrame({'A':[1,2,3], 'B':[10,20,30]})

# Serie cuyo indice coincide con las COLUMNAS de df:
s_col = pd.Series({'A':1, 'B':10})
df - s_col           # se resta a CADA fila
#    A   B
# 0  0   0
# 1  1  10
# 2  2  20

# Serie cuyo indice coincide con las FILAS de df:
s_fila = pd.Series([100, 200, 300])
df.sub(s_fila, axis=0)   # se resta a CADA columna
```

#### Caso muy comun: centrar (restar la media)
```python
df_centrado = df - df.mean()         # df.mean() es Serie con index = columnas
```

#### Caso muy comun: normalizar
```python
df_norm = (df - df.mean()) / df.std()  # z-score
```

> Sin esta alineacion automatica, tendrias que hacer un bucle por columna. Con Pandas es una linea."""
        )},
        {"type": "md", "src": tu_turno(4,
            """Tienes un DataFrame de notas:

```python
df = pd.DataFrame({
    'mate':   [7, 8, 9, 6],
    'lengua': [9, 7, 5, 8],
    'arte':   [10, 9, 7, 6]
}, index=['Ana', 'Bea', 'Carlos', 'David'])
```

1. Calcula la **media** de cada asignatura (Serie con `df.mean()`).
2. Resta la media a cada nota para obtener un DataFrame **centrado** (cada celda dice cuanto se aleja de la media de su asignatura).
3. Calcula tambien las notas **normalizadas (z-score)**: `(df - df.mean()) / df.std()`."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\n\ndf = pd.DataFrame({\n    'mate':   [7, 8, 9, 6],\n    'lengua': [9, 7, 5, 8],\n    'arte':   [10, 9, 7, 6]\n}, index=['Ana', 'Bea', 'Carlos', 'David'])\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n#\n# df = pd.DataFrame({\n#     'mate':   [7, 8, 9, 6],\n#     'lengua': [9, 7, 5, 8],\n#     'arte':   [10, 9, 7, 6]\n# }, index=['Ana', 'Bea', 'Carlos', 'David'])\n#\n# # 1) media por columna\n# medias = df.mean()\n# print(medias)\n#\n# # 2) centrado: la media de cada columna a cero\n# df_centrado = df - medias\n# display(df_centrado)\n#\n# # 3) z-score: media 0, std 1\n# df_z = (df - df.mean()) / df.std()\n# display(df_z)\n"},
    ]))

# ============ APPLY ============
if ID_APPLY:
    plan.append((ID_APPLY, [
        {"type": "md", "src": teoria(
            "apply: aplicar una funcion a cada fila o columna",
            """`apply` es la **navaja suiza** de Pandas: ejecuta una funcion sobre **cada columna** (o cada fila) del DataFrame y junta los resultados.

```python
df.apply(funcion)            # axis=0 (defecto): la funcion recibe cada COLUMNA
df.apply(funcion, axis=1)    # la funcion recibe cada FILA
```

#### Tres patrones tipicos

**1. Estadistica por columna** (cuando un metodo nativo no existe):
```python
df.apply(lambda col: col.max() - col.min())   # rango de cada columna
```

**2. Estadistica por fila**:
```python
df.apply(lambda fila: fila.sum(), axis=1)    # suma de cada fila
```

**3. Crear una columna nueva combinando varias**:
```python
df['IMC'] = df.apply(lambda fila: fila['peso'] / fila['altura']**2, axis=1)
```

#### apply vs map vs applymap (cuando usar cada uno)

| Quien lo tiene | Funcion | Sirve para |
|---|---|---|
| Serie | `s.map(f)` | Aplicar `f` a **cada elemento** de la Serie. |
| DataFrame | `df.apply(f)` | Aplicar `f` a **cada fila o columna** (recibe Serie). |
| DataFrame | `df.applymap(f)` (o `.map` en pandas 2.1+) | Aplicar `f` a **cada celda** individual. |

> **Rendimiento:** apply es flexible pero NO es el codigo mas rapido. Si puedes resolver tu problema con operaciones vectorizadas (`df['a'] + df['b']`), siempre seran mas rapidas que `apply`. Usa `apply` cuando NO existe la version vectorizada."""
        )},
        {"type": "md", "src": tu_turno(5,
            """Tienes este DataFrame de personas con peso (kg) y altura (m):

```python
personas = pd.DataFrame({
    'nombre':  ['Ana', 'Bea', 'Carlos', 'David'],
    'peso':    [60, 75, 85, 70],
    'altura':  [1.65, 1.80, 1.75, 1.70]
})
```

1. Usando `apply` con `axis=1`, crea una columna `IMC` = `peso / altura**2`.
2. Usando `apply` (sin axis) sobre las columnas numericas (`peso`, `altura`), calcula el **rango** (`max - min`) de cada una.
3. Crea otra columna `categoria` con `apply(axis=1)`: `'bajo'` si IMC<18.5, `'normal'` si IMC<25, `'alto'` en otro caso."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\n\npersonas = pd.DataFrame({\n    'nombre':  ['Ana', 'Bea', 'Carlos', 'David'],\n    'peso':    [60, 75, 85, 70],\n    'altura':  [1.65, 1.80, 1.75, 1.70]\n})\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n#\n# personas = pd.DataFrame({\n#     'nombre':  ['Ana', 'Bea', 'Carlos', 'David'],\n#     'peso':    [60, 75, 85, 70],\n#     'altura':  [1.65, 1.80, 1.75, 1.70]\n# })\n#\n# # 1) IMC por fila\n# personas['IMC'] = personas.apply(lambda r: r['peso'] / r['altura']**2, axis=1)\n#\n# # 2) rango por columna numerica\n# rangos = personas[['peso', 'altura']].apply(lambda c: c.max() - c.min())\n# print(rangos)\n#\n# # 3) categoria por fila\n# def categoria(r):\n#     if r['IMC'] < 18.5:\n#         return 'bajo'\n#     elif r['IMC'] < 25:\n#         return 'normal'\n#     else:\n#         return 'alto'\n#\n# personas['categoria'] = personas.apply(categoria, axis=1)\n# display(personas)\n"},
    ]))

# ============ ESTADISTICA DESCRIPTIVA ============
if ID_ESTAD:
    plan.append((ID_ESTAD, [
        {"type": "md", "src": teoria(
            "Estadistica descriptiva: la chuleta del analista",
            """Antes de modelar nada, **mira tus datos**. Pandas tiene metodos vectorizados para todos los estadisticos basicos.

#### Metodos generales sobre DataFrame / Serie

| Metodo | Devuelve |
|---|---|
| `count()` | Numero de **valores no nulos** por columna. |
| `sum()` | Suma. |
| `mean()` | Media aritmetica. |
| `median()` | Mediana (valor central). |
| `std()` | Desviacion tipica (n-1). |
| `var()` | Varianza. |
| `min()`, `max()` | Min y max. |
| `idxmin()`, `idxmax()` | **Indice** (etiqueta) del min/max, no el valor. |
| `quantile(0.25)` | Cuantiles. |
| `cumsum()`, `cummax()`, `cumprod()` | Acumulados. |
| `describe()` | Resumen completo: count, mean, std, min, 25%, 50%, 75%, max. |
| `value_counts()` | Frecuencia de cada valor (en Series). |
| `nunique()` | Cuantos valores **distintos** hay. |
| `corr()` | Matriz de correlaciones. |
| `cov()` | Matriz de covarianzas. |

#### Argumentos utiles
- `axis=0` (defecto, columnas) o `axis=1` (filas).
- `numeric_only=True`: ignora columnas no numericas en lugar de fallar.
- `skipna=True` (defecto): ignora NaN. Cambialo a `False` si quieres que un solo NaN haga el resultado NaN.

#### `describe()` segun el tipo
```python
df.describe()                   # solo numericas (defecto)
df.describe(include='all')      # tambien object/categorical (count, unique, top, freq)
df.describe(include='object')   # solo categoricas
```

#### Truco: encadenar para top-N
```python
df['ciudad'].value_counts().head(5)   # las 5 ciudades mas frecuentes
```"""
        )},
        {"type": "md", "src": tu_turno(6,
            """Tienes el DataFrame del notebook:

```python
diccionario = {
    'nombre': ['Marisa', 'Laura', 'Manuel', 'Carlos'],
    'edad':   [34, 34, 11, 30],
    'puntos': [95, 80, 50, 50]
}
frame = pd.DataFrame(diccionario)
```

Calcula:
1. La **media** y la **mediana** de la columna `puntos`.
2. La **edad maxima** y el **nombre** de la persona con esa edad (pista: `idxmax`).
3. El **percentil 25** (cuartil inferior) de `puntos`.
4. Un **resumen completo** con `describe(include='all')`."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\n\ndiccionario = {\n    'nombre': ['Marisa', 'Laura', 'Manuel', 'Carlos'],\n    'edad':   [34, 34, 11, 30],\n    'puntos': [95, 80, 50, 50]\n}\nframe = pd.DataFrame(diccionario)\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n#\n# diccionario = {\n#     'nombre': ['Marisa', 'Laura', 'Manuel', 'Carlos'],\n#     'edad':   [34, 34, 11, 30],\n#     'puntos': [95, 80, 50, 50]\n# }\n# frame = pd.DataFrame(diccionario)\n#\n# # 1) media y mediana de puntos\n# print('Media puntos:  ', frame['puntos'].mean())\n# print('Mediana puntos:', frame['puntos'].median())\n#\n# # 2) edad maxima y persona\n# idx = frame['edad'].idxmax()           # idx es el indice de la fila\n# print('Edad max: ', frame['edad'].max())\n# print('Quien:    ', frame.loc[idx, 'nombre'])\n#\n# # 3) percentil 25\n# print('Q1 puntos:', frame['puntos'].quantile(0.25))\n#\n# # 4) describe completo (incluye nombre)\n# display(frame.describe(include='all'))\n"},
    ]))

# ============ AGREGACIONES (LA SECCION CLAVE) ============
if ID_AGREGACIONES:
    plan.append((ID_AGREGACIONES, [
        {"type": "md", "src": teoria(
            "groupby: el corazon de Pandas (split-apply-combine)",
            """Si solo te llevas UNA cosa de este notebook, que sea `groupby`. Es el equivalente Pandas de `GROUP BY` en SQL y de las **tablas dinamicas** de Excel.

#### El patron split-apply-combine

`groupby` aplica un patron de tres pasos:

```
   datos
     |
     | SPLIT  -> partir en grupos segun una columna categorica
     v
   [grupo A] [grupo B] [grupo C]
     |        |        |
     | APPLY -> calcular algo en cada grupo (mean, sum, count, custom...)
     v        v        v
    valA     valB     valC
     \\       |       /
      \\______|______/
             |
             | COMBINE -> juntar los resultados en un nuevo DataFrame/Serie
             v
           resultado
```

#### Ejemplo guiado

Imagina ventas:

| producto | tienda | unidades |
|---|---|---|
| pan      | A | 10 |
| pan      | B | 15 |
| leche    | A | 8  |
| leche    | B | 12 |
| pan      | A | 5  |

```python
ventas.groupby('producto')['unidades'].sum()
# producto
# leche    20
# pan      30
```

Que paso por dentro:
1. **Split**: separa filas con `producto='pan'` de las de `producto='leche'`.
2. **Apply**: en cada grupo, suma la columna `unidades`.
3. **Combine**: arma una Serie indexada por producto.

#### Sintaxis general

```python
df.groupby('columna')                       # devuelve un GroupBy object (perezoso)
df.groupby('columna')['col_num'].mean()      # media de una columna por grupo
df.groupby(['col1', 'col2']).sum()           # group por VARIAS columnas (multinivel)
df.groupby('col').agg(['mean', 'std', 'count'])   # varios estadisticos a la vez
df.groupby('col').agg({'A': 'mean', 'B': 'sum'})  # estadisticos distintos por columna
```

#### Funciones de agregacion comunes

| Funcion | Que hace |
|---|---|
| `count()` | Numero de elementos no nulos. |
| `size()` | Numero de elementos (incluyendo NaN). |
| `sum()`, `mean()`, `median()`, `min()`, `max()`, `std()`, `var()` | Las habituales. |
| `first()`, `last()`, `nth(n)` | Primer / ultimo / n-esimo elemento del grupo. |
| `nunique()` | Cuantos distintos hay por grupo. |
| `agg(...)` | Aplicar una o varias funciones a la vez. |

#### transform vs apply vs filter (en groupby)

| Metodo | Devuelve | Para que |
|---|---|---|
| `agg` / metodos | Una fila por grupo. | Resumir. |
| `transform` | Mismo tamano que el original. | Anadir una columna calculada por grupo (ej. media del grupo en cada fila). |
| `filter` | Mismo formato, menos filas. | Quedarte solo con los grupos que cumplen una condicion. |
| `apply` | Lo que tu quieras. | Mas flexible, mas lento. |

```python
# transform: anadir la media del grupo a cada fila original
df['media_tienda'] = df.groupby('tienda')['unidades'].transform('mean')

# filter: quedarte con grupos que tengan al menos 100 unidades en total
df.groupby('tienda').filter(lambda g: g['unidades'].sum() > 100)
```

> **Excel mental model:** `groupby` + `agg` es practicamente una **tabla dinamica**: filas = grupos, columnas = estadisticos."""
        )},
        {"type": "md", "src": dato(
            """**Notacion mental que ayuda mucho:**

```python
df.groupby('X')['Y'].FUNCION()
#       ^         ^         ^
#       |         |         |
#       columna   columna   que calcular en cada grupo
#       que crea  que mide  (mean, sum, count...)
#       grupos
```

Lee como: *"Para cada valor de X, calcula FUNCION sobre Y"*."""
        )},
        {"type": "md", "src": tu_turno(7,
            """Tienes ventas por tienda y producto:

```python
ventas = pd.DataFrame({
    'tienda':   ['A', 'A', 'B', 'B', 'A', 'B', 'A', 'B'],
    'producto': ['pan', 'leche', 'pan', 'queso', 'queso', 'leche', 'pan', 'queso'],
    'unidades': [10, 5, 7, 3, 6, 4, 2, 8],
    'precio':   [1.2, 0.95, 1.2, 4.3, 4.3, 0.95, 1.2, 4.3]
})
```

Calcula:

1. **Total de unidades vendidas por tienda**.
2. **Media de unidades por producto**.
3. **Total de unidades** y **media de precio** por (`tienda`, `producto`) usando un solo `agg(...)`.
4. Anade una columna `pct_tienda` con el **porcentaje** que cada fila representa sobre el total de su tienda (pista: `transform('sum')`).
5. Quedate solo con las tiendas cuya **suma total** de unidades sea **mayor de 20** (pista: `filter`)."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\n\nventas = pd.DataFrame({\n    'tienda':   ['A', 'A', 'B', 'B', 'A', 'B', 'A', 'B'],\n    'producto': ['pan', 'leche', 'pan', 'queso', 'queso', 'leche', 'pan', 'queso'],\n    'unidades': [10, 5, 7, 3, 6, 4, 2, 8],\n    'precio':   [1.2, 0.95, 1.2, 4.3, 4.3, 0.95, 1.2, 4.3]\n})\ndisplay(ventas)\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n#\n# ventas = pd.DataFrame({\n#     'tienda':   ['A', 'A', 'B', 'B', 'A', 'B', 'A', 'B'],\n#     'producto': ['pan', 'leche', 'pan', 'queso', 'queso', 'leche', 'pan', 'queso'],\n#     'unidades': [10, 5, 7, 3, 6, 4, 2, 8],\n#     'precio':   [1.2, 0.95, 1.2, 4.3, 4.3, 0.95, 1.2, 4.3]\n# })\n#\n# # 1) total de unidades por tienda\n# print(ventas.groupby('tienda')['unidades'].sum())\n#\n# # 2) media de unidades por producto\n# print(ventas.groupby('producto')['unidades'].mean())\n#\n# # 3) varias agregaciones a la vez por (tienda, producto)\n# resumen = ventas.groupby(['tienda', 'producto']).agg(\n#     unidades_tot=('unidades', 'sum'),\n#     precio_medio=('precio', 'mean')\n# )\n# display(resumen)\n#\n# # 4) porcentaje sobre el total de la tienda usando transform\n# total_tienda = ventas.groupby('tienda')['unidades'].transform('sum')\n# ventas['pct_tienda'] = ventas['unidades'] / total_tienda * 100\n# display(ventas)\n#\n# # 5) filter: solo tiendas con suma de unidades > 20\n# resultado = ventas.groupby('tienda').filter(lambda g: g['unidades'].sum() > 20)\n# display(resultado)\n"},
    ]))

# ============ INTRO MERGE / CONCAT / PIVOT (concepto extra que el nb original no cubre, pero es esencial) ============
# Lo enganchamos al final de la seccion de agregaciones para que lo encuentren
if ID_AGREGACIONES:
    # Lo anadimos en la celda final de la seccion (justo antes de Correlaciones)
    # En lugar de eso, anadimos despues de la celda groupby final
    pass

# ============ CORRELACIONES ============
if ID_CORRELACIONES:
    plan.append((ID_CORRELACIONES, [
        {"type": "md", "src": teoria(
            "Correlaciones: medir la relacion entre dos variables",
            """La **correlacion** mide si dos variables numericas se mueven juntas. La mas usada es la **correlacion de Pearson**, que da un numero entre **-1 y 1**:

| Valor | Significado |
|---|---|
| `+1` | Relacion lineal **perfecta y directa** (sube una, sube la otra). |
| `0`  | No hay relacion lineal. |
| `-1` | Relacion lineal **perfecta e inversa** (sube una, baja la otra). |

Y los valores intermedios:

| Rango | Interpretacion (orientativa) |
|---|---|
| 0.0 - 0.3 | Debil |
| 0.3 - 0.7 | Moderada |
| 0.7 - 1.0 | Fuerte |

> **Cuidado:** correlacion **NO implica causalidad**. Que dos cosas suban juntas no significa que una cause la otra (puede haber una tercera variable detras).

#### En Pandas

```python
df['x'].corr(df['y'])         # correlacion entre dos columnas (Pearson)
df.corr(numeric_only=True)    # matriz de correlacion entre TODAS las numericas
df.corr(method='spearman')    # rangos -> mide relacion monotona, no solo lineal
df.corr(method='kendall')     # otra alternativa robusta
```

#### Diferencia entre Pearson y Spearman
- **Pearson**: mide relacion **lineal**.
- **Spearman**: convierte cada valor a su **ranking** y mide relacion. Robusto a outliers y captura relaciones monotonas no lineales (ej. exponencial creciente).

#### Por que importa para Machine Learning
- **Feature selection**: si dos features tienen correlacion 0.99, son practicamente la misma informacion -> eliminar una.
- **Multicolinealidad**: en regresion lineal, features muy correlacionadas hacen los coeficientes inestables.
- **Visualizacion**: heatmaps de correlaciones son lo primero que mira un data scientist."""
        )},
    ]))

if ID_CORR_TODOS:
    plan.append((ID_CORR_TODOS, [
        {"type": "md", "src": tu_turno(8,
            """Carga el dataset `mpg_data` que ya ha cargado el notebook (consumo de coches).

1. Calcula la matriz de correlacion entre todas las columnas numericas (`mpg_data.corr(numeric_only=True)`).
2. Encuentra el **par de columnas con correlacion mas negativa** (excluyendo la diagonal).
3. Encuentra el **par con correlacion mas positiva** (excluyendo la diagonal).
4. Para la columna `mpg`, ordena las demas columnas por **correlacion absoluta descendente** (las que mas la explican, en cualquier sentido)."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\n# nota: requiere que el notebook ya haya cargado mpg_data en celdas anteriores\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# # 1) matriz de correlacion\n# import numpy as np\n# corr = mpg_data.corr(numeric_only=True)\n# display(corr)\n#\n# # 2) y 3): excluir la diagonal poniendola a NaN para que min/max no la consideren\n# corr_off = corr.where(~np.eye(len(corr), dtype=bool))\n#\n# # par mas negativo:\n# # idxmin sobre cada columna devuelve la fila con min, despues coger el min global\n# valor_min = corr_off.min().min()\n# # buscar (fila, col) con ese valor\n# pos = corr_off.stack().idxmin()       # tupla (fila, col)\n# print('Mas negativo:', pos, '->', valor_min)\n#\n# # par mas positivo:\n# pos_pos = corr_off.stack().idxmax()\n# print('Mas positivo:', pos_pos, '->', corr_off.stack().max())\n#\n# # 4) lo que mas explica mpg, en valor absoluto\n# corr_mpg = corr['mpg'].drop('mpg')\n# print(corr_mpg.abs().sort_values(ascending=False))\n"},
    ]))

# ============ EJERCICIO FINAL DEL BLOQUE ============
if ID_EJERCICIOS:
    plan.append((ID_EJERCICIOS, [
        {"type": "md", "src": teoria(
            "Recapitulacion del notebook 10",
            """Has visto los pilares de Pandas para analisis de datos:

1. **Operaciones vectorizadas** entre DataFrames y Series (con alineacion por etiquetas).
2. **`apply`** para funciones personalizadas por fila o columna.
3. **Estadistica descriptiva** (`describe`, `mean`, `std`, `quantile`, `idxmax`).
4. **`groupby`**: split-apply-combine para resumir por categorias.
5. **Correlaciones**: medir relaciones lineales entre variables numericas.

#### Que falta (y veras en proximos materiales)
- **`merge` / `join` / `concat`**: combinar varios DataFrames (equivalente a SQL JOIN).
- **`pivot` / `melt`**: cambiar el formato entre **ancho** (columnas por categoria) y **largo** (una fila por observacion).

#### Una vista rapida de merge / pivot / melt (adelanto)

**merge** combina dos DataFrames por una columna comun:
```python
clientes.merge(pedidos, on='id_cliente', how='inner')
# how='inner' (defecto), 'left', 'right', 'outer'
```

| `how`     | Filas resultantes |
|---|---|
| `'inner'` | Solo las claves que estan en LOS DOS. |
| `'left'`  | Todas las del izquierdo, NaN cuando no hay derecho. |
| `'right'` | Todas las del derecho. |
| `'outer'` | Todas las de los dos lados, NaN donde falte. |

**pivot** convierte filas en columnas (formato ancho):
```python
ventas.pivot(index='fecha', columns='producto', values='unidades')
```

**melt** hace lo contrario (formato largo):
```python
df.melt(id_vars=['fecha'], var_name='producto', value_name='unidades')
```

| Excel | Pandas |
|---|---|
| Tabla dinamica | `groupby` + `agg`, o `pivot_table` |
| BUSCARV / VLOOKUP | `merge` |
| Apilar columnas | `melt` |
| Cruzar tabla | `pivot` |"""
        )},
        {"type": "md", "src": tu_turno(9,
            """**Ejercicio final integrador.** Tienes dos DataFrames:

```python
clientes = pd.DataFrame({
    'id_cliente': [1, 2, 3, 4],
    'nombre':     ['Ana', 'Bea', 'Carlos', 'David'],
    'ciudad':     ['Madrid', 'Madrid', 'Bilbao', 'Sevilla']
})

pedidos = pd.DataFrame({
    'id_pedido':  [101, 102, 103, 104, 105, 106],
    'id_cliente': [1, 2, 1, 3, 1, 2],
    'producto':   ['libro', 'taza', 'libro', 'lampara', 'taza', 'libro'],
    'importe':    [15.0, 8.0, 22.0, 35.0, 9.0, 12.0]
})
```

1. Haz un **`merge`** de `pedidos` con `clientes` (`how='left'` sobre `id_cliente`).
2. Sobre el resultado, agrupa por `ciudad` y calcula la **suma del importe** y el **numero de pedidos**.
3. Ordena el resultado por la suma del importe descendente.
4. **Bonus**: usando `pivot_table`, crea una tabla con filas = `ciudad`, columnas = `producto`, valores = suma del importe (rellena los huecos con 0)."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\n\nclientes = pd.DataFrame({\n    'id_cliente': [1, 2, 3, 4],\n    'nombre':     ['Ana', 'Bea', 'Carlos', 'David'],\n    'ciudad':     ['Madrid', 'Madrid', 'Bilbao', 'Sevilla']\n})\n\npedidos = pd.DataFrame({\n    'id_pedido':  [101, 102, 103, 104, 105, 106],\n    'id_cliente': [1, 2, 1, 3, 1, 2],\n    'producto':   ['libro', 'taza', 'libro', 'lampara', 'taza', 'libro'],\n    'importe':    [15.0, 8.0, 22.0, 35.0, 9.0, 12.0]\n})\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n#\n# clientes = pd.DataFrame({\n#     'id_cliente': [1, 2, 3, 4],\n#     'nombre':     ['Ana', 'Bea', 'Carlos', 'David'],\n#     'ciudad':     ['Madrid', 'Madrid', 'Bilbao', 'Sevilla']\n# })\n#\n# pedidos = pd.DataFrame({\n#     'id_pedido':  [101, 102, 103, 104, 105, 106],\n#     'id_cliente': [1, 2, 1, 3, 1, 2],\n#     'producto':   ['libro', 'taza', 'libro', 'lampara', 'taza', 'libro'],\n#     'importe':    [15.0, 8.0, 22.0, 35.0, 9.0, 12.0]\n# })\n#\n# # 1) merge: cada pedido se completa con la info del cliente\n# combinado = pedidos.merge(clientes, on='id_cliente', how='left')\n# display(combinado)\n#\n# # 2) agregacion por ciudad\n# resumen = combinado.groupby('ciudad').agg(\n#     importe_total=('importe', 'sum'),\n#     pedidos=('id_pedido', 'count')\n# )\n#\n# # 3) ordenar por importe descendente\n# resumen = resumen.sort_values('importe_total', ascending=False)\n# display(resumen)\n#\n# # 4) tabla pivote: ciudad x producto, valores = suma de importe\n# tabla = combinado.pivot_table(\n#     index='ciudad',\n#     columns='producto',\n#     values='importe',\n#     aggfunc='sum',\n#     fill_value=0\n# )\n# display(tabla)\n"},
    ]))


enhance(NB, plan)
print("Done.")

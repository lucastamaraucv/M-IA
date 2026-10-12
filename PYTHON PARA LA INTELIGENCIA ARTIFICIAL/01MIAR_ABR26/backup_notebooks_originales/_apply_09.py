"""Aplica mejoras al notebook 09_Pandas con bloques de colores y teoria detallada."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, solucion_md, dato, aviso
import json

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_09_Pandas.ipynb"

nb = json.load(open(NB, encoding="utf-8"))
def find_id(fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if fragment in src:
            return c["id"]
    return None

def find_id_starts(prefix):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if src.lstrip().startswith(prefix):
            return c["id"]
    return None

# Anchors
ID_TITULO       = nb["cells"][0]["id"]
ID_INTRO_PANDAS = find_id_starts("# Pandas")
ID_VERSION      = find_id("pd.__version__")
ID_SERIES       = find_id_starts("# Series")
ID_SERIE_INDEX  = find_id("# especificando el")
ID_SLICING_S    = find_id("# slicing\nprint(football_cities['a':'c'])")
ID_MASKS        = find_id("# uso de masks para seleccionar")
ID_ITER_S       = find_id_starts("### Iteraci")
ID_SERIES_DICT  = find_id_starts("## Series como diccionarios")
ID_OPS_SERIES   = find_id_starts("## Operaciones entre series")
ID_NAN_SERIE    = find_id("isnull() para cambiar los NaN")
ID_DIFF_DICT    = find_id_starts("###  Diferencias entre Pandas Series")
ID_DATAFRAME    = find_id_starts("# DataFrame")
ID_DF_CREAR     = find_id("# crear un DataFrame a partir de un diccionario")
ID_DF_COLACC    = find_id("# acceso a columnas devuelve una serie")
ID_FORMAS_DF    = find_id_starts("### Formas de crear un DataFrame")
ID_MOD_DF       = find_id_starts("## Modificar DataFrames")
ID_ADD_COL      = find_id("# a")  # generic, will be overridden
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if "frame['Direccion'] = 'Desconocida'" in src:
        ID_ADD_COL = c["id"]
        break
ID_DROP_AXIS    = find_id('frame.drop("Nacionalidad", axis=1')
ID_ITER_DF      = find_id_starts("## Iteraci") if False else None
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if src.lstrip().startswith("## Iteraci") and "DataFrame" not in src:
        # second occurrence (DF iteration)
        pass
# search the second "## Iteraci" - the DF one
iter_count = 0
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if src.lstrip().startswith("## Iteraci"):
        iter_count += 1
        if iter_count == 1:
            ID_ITER_DF = c["id"]
            break

ID_INDEX_SLICING = find_id_starts("## Indexaci")
ID_ACC_COL      = find_id_starts(" * Acceder a columnas")
ID_ACC_ILOC     = find_id("Acceder a filas por")  # "iloc"
# Need both anchors - find them
ID_ILOC_ANCHOR = None
ID_LOC_ANCHOR = None
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if "`iloc`" in src and "posicion" in src.lower():
        ID_ILOC_ANCHOR = c["id"]
    if "`loc`" in src and "ntico" in src:  # "semantico"
        ID_LOC_ANCHOR = c["id"]

ID_AMBIG        = find_id("por defecto, pandas interpreta")
ID_AXIS         = find_id_starts(" * Axis para definir")
ID_SLICE_POS    = find_id_starts(" * Slicing con")
ID_WARNING_SLI  = find_id_starts("## Warning para slices")
ID_INDEX_OBJ    = find_id_starts("## Objeto Index")
ID_MASCARAS     = find_id_starts("## Mascaras")
ID_FILTRO_FILAS = find_id("filtrar filas y columnas")
ID_CARGAR       = find_id_starts("# Cargar y guardar datos")
ID_GUARDAR_CSV  = find_id("# Guardar a csv")
ID_OTROS_ARGS   = find_id_starts("#### otros argumentos to_csv")
ID_OTROS_FORM   = find_id("Pandas tambi")
ID_EJ_PRACTICO  = find_id_starts("# Ejemplo pr")
ID_DTYPES       = find_id("# tipos de datos sobre las columnas")
ID_DESCRIBE     = find_id("# informaci")  # describe
ID_INFO         = find_id("users_dataset.info()")
ID_FILTER_F     = find_id("# cu")  # cuantos usuarios son mujeres
ID_GROUPBY      = find_id("# Agrupar datos por atributos")
ID_EJERCICIOS   = find_id_starts("# Ejercicios")

# ---------------------------------------------------------------------
plan = []

# -------- INTRO al notebook --------
plan.append((ID_TITULO, [
    {"type": "md", "src": teoria(
        "Como leer este notebook (version mejorada)",
        """Este notebook fue **enriquecido** para ayudarte a aprender Pandas escribiendo codigo. Vas a encontrar tres tipos de bloques de colores:

<div style="background-color:#e7f5ff;border-left:6px solid #1c7ed6;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AZUL = TEORIA</b></div> -> explicacion en palabras simples antes de cada concepto.

<div style="background-color:#fff9db;border-left:6px solid #f59f00;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AMARILLO = TU TURNO</b></div> -> el ejercicio que TU debes resolver. Hay una celda vacia debajo donde escribes el codigo.

<div style="background-color:#ebfbee;border-left:6px solid #2f9e44;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>VERDE = SOLUCION</b></div> -> codigo de referencia comentado por si te trabas. Destapa solo despues de intentar.

<div style="background-color:#fff0f0;border-left:6px solid #e03131;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>ROJO = CUIDADO</b></div> -> trampas comunes (en pandas hay muchas, especialmente con `.loc` vs `.iloc`).

> **Promesa importante**: el codigo y la teoria del profesor original no se han tocado. Solo se han ANADIDO bloques. Asi puedes seguir comparando con la version original cuando quieras."""
    )},
]))

# -------- INTRO PANDAS --------
plan.append((ID_INTRO_PANDAS, [
    {"type": "md", "src": teoria(
        "Que es Pandas y por que es la herramienta #1 de datos en Python",
        """**Pandas** es la libreria de facto para trabajar con **datos tabulares** (filas y columnas, como una hoja de Excel o una tabla SQL). Construida sobre **NumPy**, anade dos estructuras clave:

| Estructura | Que es | Analogia |
|---|---|---|
| `Series` | Vector unidimensional con indice | Una columna de Excel |
| `DataFrame` | Tabla 2D con indices y columnas | Una hoja de Excel completa, una tabla SQL |

#### Por que Pandas y no listas/dicts puros?

| Tarea | Python puro | Pandas |
|---|---|---|
| Leer un CSV de 1M filas | parseando manualmente | `pd.read_csv(...)` en una linea |
| Filtrar filas por condicion | bucle `for` + `if` | `df[df['edad'] > 18]` |
| Agrupar y calcular medias | bucles complejos | `df.groupby('ciudad').mean()` |
| Manejar valores faltantes | comprobar `None` cada vez | `df.dropna()`, `df.fillna(...)` |
| Estadisticas resumen | calcular a mano | `df.describe()` |

#### Convencion universal

```python
import pandas as pd       # alias 'pd' es ESTANDAR
from pandas import Series, DataFrame
```

A partir de aqui veras `pd.algo(...)` constantemente. **No cambies el alias**: toda la documentacion, Stack Overflow y tutoriales usan `pd`.

#### Que aprenderemos en este notebook

1. **Series**: el ladrillo basico (1D).
2. **DataFrame**: la tabla 2D y sus operaciones esenciales.
3. **Indexacion** y la diferencia critica entre `.loc` y `.iloc`.
4. **Filtrado booleano** (mascaras).
5. **NaN**: como detectarlos y tratarlos.
6. **Lectura/escritura** de CSV, Excel, JSON.
7. **Caso real** con MovieLens."""
    )},
]))

# -------- VERSION --------
plan.append((ID_VERSION, [
    {"type": "md", "src": dato(
        """Comprobar la version de pandas es importante: la API ha cambiado de forma significativa entre versiones (por ejemplo, el metodo `.append()` en DataFrames se ELIMINO en pandas 2.0). Para este curso te servira cualquier version 1.x o 2.x.

Si necesitas instalarlo: `pip install pandas` (o `conda install pandas`)."""
    )},
]))

# -------- SERIES --------
plan.append((ID_SERIES, [
    {"type": "md", "src": teoria(
        "Series: el bloque fundamental de Pandas",
        """Una **Series** es como un array de NumPy con **etiquetas (indices)** asociadas a cada valor:

```
indice    valor
   0   ->  'Spain'
   1   ->  'Andorra'
   2   ->  'Gibraltar'
```

#### Anatomia de una Serie

```python
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'], name='puntos')
```

| Componente | Que es | Como acceder |
|---|---|---|
| `values` | El array de datos (NumPy) | `s.values` |
| `index` | Las etiquetas | `s.index` |
| `name` | Nombre de la Serie | `s.name` |
| `dtype` | Tipo de los valores | `s.dtype` |

#### Diferencias clave con una lista de Python

| Operacion | Lista | Series |
|---|---|---|
| Crear | `[1,2,3]` | `pd.Series([1,2,3])` |
| Indices | solo numericos 0..n | numericos O **personalizados** (str, fecha, etc.) |
| Operaciones vectoriales | bucles | `s * 2`, `s + s2` automatico |
| Acceso | `l[0]` | `s[0]`, `s['etiqueta']`, `s.iloc[0]`, `s.loc['etiqueta']` |
| NaN | tienes que manejarlos a mano | soporte nativo `isna()`, `fillna()` |

#### Formas de crear una Series

```python
pd.Series([1, 2, 3])                          # desde lista, indice 0..n
pd.Series([1, 2, 3], index=['a', 'b', 'c'])   # con indices propios
pd.Series({'a': 1, 'b': 2})                   # desde dict (claves -> indices)
pd.Series(5, index=range(4))                  # mismo valor para todos
```"""
    )},
]))

plan.append((ID_SERIE_INDEX, [
    {"type": "md", "src": tu_turno(1,
        """Crea una `pd.Series` con las temperaturas medias mensuales (en grados): `[10, 11, 13, 16, 19, 24, 27, 27, 23, 18, 13, 11]`. Usa como indices los nombres de los meses: `['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']` y ponle `name='Temperaturas Madrid'`.

Despues:
1. Imprime la temperatura de `'jul'`.
2. Imprime las temperaturas de `'jun'`, `'jul'`, `'ago'` (varios indices a la vez).
3. Calcula la **media** con `.mean()` y el **maximo** con `.max()`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n# meses = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']\n# temps = [10, 11, 13, 16, 19, 24, 27, 27, 23, 18, 13, 11]\n# s = pd.Series(temps, index=meses, name='Temperaturas Madrid')\n# print(s['jul'])\n# print(s[['jun','jul','ago']])\n# print('Media:', s.mean())\n# print('Maximo:', s.max())\n"},
]))

# -------- SLICING SERIES --------
plan.append((ID_SLICING_S, [
    {"type": "md", "src": aviso(
        """**Trampa importante con el slicing en Series:**

| Tipo de indice | `s[0:3]` | `s['a':'c']` |
|---|---|---|
| Posicional (entero) | excluye el final (3 NO se incluye) | - |
| Etiqueta (string) | - | **incluye AMBOS extremos** |

Es decir, con etiquetas Pandas se comporta **al reves que Python**: el final SI se incluye. Es facil equivocarse aqui."""
    )},
]))

# -------- MASKS --------
plan.append((ID_MASKS, [
    {"type": "md", "src": teoria(
        "Mascaras booleanas: el filtrado mas usado en Pandas",
        """Una **mascara booleana** es una Series de `True`/`False` del mismo tamano que tu Series/DataFrame. Pandas usa esa mascara para **quedarse solo con las filas True**.

#### Como se crea una mascara

```python
s = pd.Series([0, 1, 1, 2, 3, 5, 8, 13, 21])

mask = s > 4         # crea Series de bool: [False, False, ..., True, True, True]
print(s[mask])       # devuelve solo los que cumplen la condicion
# 5, 8, 13, 21
```

Tambien puedes hacerlo en una sola linea:

```python
s[s > 4]
```

#### Combinar varias condiciones

| Operador Python | En Pandas | Razon |
|---|---|---|
| `and` | `&` | `and` no funciona con Series |
| `or` | `\\|` | igual |
| `not` | `~` | igual |

**Y los parentesis son OBLIGATORIOS** alrededor de cada condicion porque `&` tiene mayor precedencia que `>`:

```python
s[(s > 2) & (s < 10)]      # entre 2 y 10
s[(s == 0) \\| (s > 20)]    # cero o muy grande
s[~(s == 0)]                # distintos de cero
```

> Si pones `s[s > 2 & s < 10]` te dara error de truthiness o resultados extranos. Acostumbrate a los parentesis."""
    )},
]))

# -------- ITERACION SERIES --------
plan.append((ID_ITER_S, [
    {"type": "md", "src": teoria(
        "Iterar Series y DataFrames: que opciones hay",
        """Aunque Pandas funciona mejor con **operaciones vectoriales** (sin bucles), a veces necesitas iterar.

#### Series

| Sintaxis | Que devuelve |
|---|---|
| `for v in s:` | solo VALORES |
| `for i in s.index:` | solo INDICES |
| `for i, v in s.items():` | INDICE + valor (recomendada) |

#### DataFrames

| Sintaxis | Que devuelve |
|---|---|
| `for col in df:` | nombres de COLUMNAS (raro de necesitar) |
| `for idx, row in df.iterrows():` | (indice, fila como Series) |
| `for row in df.itertuples():` | namedtuple por fila (mas rapido) |

> **Buena practica:** intenta SIEMPRE primero una solucion vectorial. Iterar es lento en Pandas. Si tu codigo tiene un `for df.iterrows()`, casi siempre se puede reescribir con una operacion de columna o un `apply()`."""
    )},
]))

# -------- SERIES DICT --------
plan.append((ID_SERIES_DICT, [
    {"type": "md", "src": teoria(
        "Series como diccionarios: similitudes y diferencias",
        """Las Series se parecen mucho a los diccionarios: ambos asocian **clave -> valor**. Pero hay diferencias:

| Caracteristica | dict | Series |
|---|---|---|
| Acceso por clave | `d['a']` | `s['a']` |
| Acceso por posicion | NO | `s.iloc[0]` |
| Operaciones vectoriales | NO | SI (`s * 2`, `s + s2`) |
| Orden de claves | depende de la version | mantenido siempre |
| Tipos heterogeneos en valores | SI libre | SI pero comparten dtype |
| NaN | a mano con `None` | nativo `np.nan` |
| Operaciones estadisticas | a mano | nativas (`mean`, `std`, `max`...) |

Conversion entre ambos:
```python
s = pd.Series({'a': 1, 'b': 2})    # dict -> Series
d = s.to_dict()                     # Series -> dict
```"""
    )},
]))

# -------- OPERACIONES ENTRE SERIES --------
plan.append((ID_OPS_SERIES, [
    {"type": "md", "src": teoria(
        "Alineacion automatica por indice (la magia de Pandas)",
        """Cuando sumas, restas o haces cualquier operacion entre dos Series, **Pandas alinea por INDICE**, no por posicion. Esto es muy distinto a NumPy.

```python
s1 = pd.Series([10, 20, 30, 40], index=['a','b','c','d'])
s2 = pd.Series([1, 2, 3],          index=['b','c','e'])

s1 + s2
#  a     NaN     <- 'a' solo en s1
#  b    21.0    <- 20 + 1
#  c    32.0    <- 30 + 2
#  d     NaN    <- 'd' solo en s1
#  e     NaN    <- 'e' solo en s2
```

#### Reglas

1. Si un indice esta en **ambas**, se opera normalmente.
2. Si un indice esta en **solo una**, el resultado es `NaN`.
3. Para evitar NaN, usa el metodo equivalente con `fill_value`:

```python
s1.add(s2, fill_value=0)   # trata los faltantes como 0
s1.sub(s2, fill_value=0)
s1.mul(s2, fill_value=1)
```

Esta alineacion automatica te ahorra muchos bucles, pero tambien es **fuente de bugs** si no eres consciente."""
    )},
    {"type": "md", "src": tu_turno(2,
        """Tienes las ventas de dos meses en dos Series:

```python
ene = pd.Series([100, 200, 150], index=['libros','musica','peliculas'])
feb = pd.Series([120, 180, 200, 50], index=['libros','peliculas','juegos','musica'])
```

1. Calcula el total de ventas combinado por categoria (`ene + feb`). Que pasa con `juegos`?
2. Repite el calculo, pero usando `.add(... , fill_value=0)` para que las categorias presentes en una sola Serie cuenten como 0.
3. Filtra solo las categorias que vendieron mas de 200 en el total."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\nene = pd.Series([100, 200, 150], index=['libros','musica','peliculas'])\nfeb = pd.Series([120, 180, 200, 50], index=['libros','peliculas','juegos','musica'])\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n# ene = pd.Series([100, 200, 150], index=['libros','musica','peliculas'])\n# feb = pd.Series([120, 180, 200, 50], index=['libros','peliculas','juegos','musica'])\n#\n# total = ene + feb\n# print(total)            # 'juegos' sale NaN porque no esta en 'ene'\n#\n# total_seguro = ene.add(feb, fill_value=0)\n# print(total_seguro)\n#\n# print(total_seguro[total_seguro > 200])\n"},
]))

# -------- NaN SERIE --------
plan.append((ID_NAN_SERIE, [
    {"type": "md", "src": teoria(
        "NaN: el valor faltante en Pandas",
        """`NaN` (Not a Number) representa un valor **faltante o desconocido**. Pandas lo trata como un ciudadano de primera clase.

#### Como crearlo

```python
import numpy as np
import pandas as pd

s = pd.Series([1, 2, np.nan, 4])
```

#### Detectarlos

| Funcion | Que hace |
|---|---|
| `s.isna()` (o `isnull()`) | Series de bool: True donde hay NaN |
| `s.notna()` | el opuesto |
| `s.isna().sum()` | cuantos NaN hay |
| `s.isna().any()` | hay AL MENOS uno? |
| `s.isna().all()` | son TODOS NaN? |

#### Tratarlos

| Metodo | Que hace |
|---|---|
| `s.dropna()` | Devuelve la Serie SIN los NaN |
| `s.fillna(0)` | Reemplaza los NaN con 0 |
| `s.fillna(s.mean())` | con la media |
| `s.fillna(method='ffill')` | propaga hacia adelante (deprecated en 2.x: usar `s.ffill()`) |
| `s.fillna(method='bfill')` | propaga hacia atras (usar `s.bfill()`) |

#### Trampa frecuente

```python
s == np.nan      # NUNCA funciona! Siempre da False
s.isna()         # ESTA es la forma correcta
```

Esto pasa porque `NaN` esta definido (segun el estandar IEEE) como **distinto de todo, incluido el mismo**. Por eso necesitas la funcion especial `isna()`."""
    )},
]))

# -------- DataFrame --------
plan.append((ID_DATAFRAME, [
    {"type": "md", "src": teoria(
        "DataFrame: la tabla 2D, el caballo de batalla de Pandas",
        """Un **DataFrame** es una **tabla 2D** con filas y columnas etiquetadas. Cada **columna** es una `Series`. Comparten el mismo `index` (las filas).

```
            Nombre   Edad   Ciudad
   0       Marisa     25   Madrid
   1       Carlos     30   Sevilla
   2       Ana        22   Valencia
   ^         ^         ^      ^
 index   columna  columna  columna
```

#### Anatomia de un DataFrame

| Componente | Acceso |
|---|---|
| Indices de filas | `df.index` |
| Nombres de columnas | `df.columns` |
| Valores (numpy 2D) | `df.values` |
| Tamano (filas, cols) | `df.shape` |
| Tipos por columna | `df.dtypes` |
| Vista rapida superior | `df.head(n)` |
| Vista rapida inferior | `df.tail(n)` |
| Resumen estadistico | `df.describe()` |
| Info de memoria + tipos | `df.info()` |

#### Comparado con otras herramientas

| Herramienta | Equivalente |
|---|---|
| Excel | hoja de calculo completa |
| SQL | tabla |
| R | data.frame |
| NumPy | matriz 2D, pero CON etiquetas en filas y columnas |"""
    )},
]))

# -------- DF crear --------
plan.append((ID_DF_CREAR, [
    {"type": "md", "src": teoria(
        "Cinco formas de crear un DataFrame",
        """No hay UNA forma de crear un DataFrame. Conocer las mas comunes te ahorrara tiempo.

#### 1. Diccionario de listas (la mas comun)

```python
df = pd.DataFrame({
    'nombre': ['Ana', 'Pedro', 'Lucia'],
    'edad':   [30, 25, 35]
})
```

#### 2. Lista de diccionarios (cada dict es una fila)

```python
df = pd.DataFrame([
    {'nombre': 'Ana',   'edad': 30},
    {'nombre': 'Pedro', 'edad': 25},
    {'nombre': 'Lucia', 'edad': 35},
])
```

> **Util:** si las claves no coinciden entre filas, los faltantes se llenan con `NaN`.

#### 3. Diccionario de Series

```python
nombres = pd.Series(['Ana', 'Pedro'])
edades  = pd.Series([30, 25])
df = pd.DataFrame({'nombre': nombres, 'edad': edades})
```

#### 4. Array NumPy 2D + columnas

```python
import numpy as np
df = pd.DataFrame(np.array([[1,2],[3,4]]), columns=['a','b'])
```

#### 5. Desde archivo (la mas usada en el dia a dia)

```python
df = pd.read_csv('datos.csv')
df = pd.read_excel('datos.xlsx')
df = pd.read_json('datos.json')
df = pd.read_sql(query, conn)
```"""
    )},
]))

# -------- DF acceso a columnas --------
plan.append((ID_DF_COLACC, [
    {"type": "md", "src": teoria(
        "Acceso a columnas: dos sintaxis (corchetes vs punto)",
        """Existen **dos formas** de acceder a una columna de un DataFrame:

| Sintaxis | Cuando usar |
|---|---|
| `df['Nombre']` | **Siempre funciona** (recomendada) |
| `df.Nombre` | Solo si el nombre es un identificador valido (sin espacios, sin empezar por numero) y NO choca con un atributo de pandas |

```python
df['Nombre']        # Siempre OK
df.Nombre           # OK aqui
df['Mes nacimiento']  # Solo asi (tiene espacio)
df.shape            # Esto NO es columna, es atributo del DF
df['shape']         # Si tu columna se llama 'shape', usa corchetes
```

#### Que devuelve?

`df['Nombre']` -> una **Series** (la columna entera).

#### Multiples columnas

Para varias columnas usa **doble corchete** (lista dentro de corchetes):

```python
df[['Nombre', 'Edad']]    # devuelve un DataFrame nuevo con esas 2 columnas
df['Nombre', 'Edad']     # ERROR
```

> **Regla nemotecnica:** corchete simple = una columna (Series). Corchete doble = varias columnas (DataFrame)."""
    )},
    {"type": "md", "src": tu_turno(3,
        """Crea un DataFrame con datos de 4 personas:

```python
data = {
    'Nombre':  ['Ana', 'Bea', 'Carlos', 'David'],
    'Edad':    [25, 32, 41, 19],
    'Ciudad':  ['Madrid', 'Sevilla', 'Valencia', 'Bilbao'],
    'Salario': [30000, 45000, 60000, 22000]
}
```

Despues:
1. Crea el DataFrame.
2. Imprime SOLO la columna `'Nombre'` y muestra su tipo (`type(...)`).
3. Imprime las columnas `'Nombre'` y `'Salario'` juntas (DataFrame de 2 cols).
4. Muestra `df.shape`, `df.dtypes` y `df.describe()`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n# data = {\n#     'Nombre':  ['Ana','Bea','Carlos','David'],\n#     'Edad':    [25, 32, 41, 19],\n#     'Ciudad':  ['Madrid','Sevilla','Valencia','Bilbao'],\n#     'Salario': [30000, 45000, 60000, 22000]\n# }\n# df = pd.DataFrame(data)\n#\n# print(df['Nombre'])\n# print(type(df['Nombre']))     # Series\n# print(df[['Nombre','Salario']])\n# print(df.shape)               # (4, 4)\n# print(df.dtypes)\n# print(df.describe())\n"},
]))

# -------- INDEXACION --------
if ID_INDEX_SLICING:
    plan.append((ID_INDEX_SLICING, [
        {"type": "md", "src": teoria(
            "Indexacion en DataFrames: las 4 formas que debes dominar",
            """Acceder a datos de un DataFrame admite varias sintaxis. Esto es **donde mas se confunden** los principiantes. Vamos por partes.

| Que quiero | Sintaxis | Notas |
|---|---|---|
| Una columna | `df['col']` | Devuelve Series |
| Varias columnas | `df[['col1','col2']]` | Devuelve DataFrame |
| Una fila por **POSICION** | `df.iloc[2]` | Por entero, 0-indexed |
| Una fila por **ETIQUETA** | `df.loc['a']` | Por nombre del indice |
| Celda por posicion | `df.iloc[2, 3]` | fila 2, columna 3 |
| Celda por etiqueta | `df.loc['a', 'col']` | fila 'a', columna 'col' |
| Filas + columnas | `df.loc['a':'c', ['col1','col2']]` | mezcla |
| Filtrado booleano | `df[df['col'] > 5]` | mascara sobre todas las filas |

#### Las 4 formas mas frecuentes

```python
df['col']             # 1) columna
df.iloc[i]            # 2) fila por posicion (entero)
df.loc[etiq]          # 3) fila por etiqueta del indice
df[df['col'] > 5]     # 4) filtrado booleano
```

Te las vas a saber de memoria al final del notebook."""
        )},
    ]))

# -------- iloc explanation --------
if ID_ILOC_ANCHOR:
    plan.append((ID_ILOC_ANCHOR, [
        {"type": "md", "src": teoria(
            ".iloc vs .loc: la trampa #1 de Pandas",
            """**Esta es probablemente la diferencia que mas confusion causa en Pandas.** Lee esto despacio.

| | `.iloc` | `.loc` |
|---|---|---|
| **Que busca** | POSICION numerica (0, 1, 2, ...) | ETIQUETA del indice ('a', 'fila_3', 2024-01-15...) |
| **Si tu indice es 0,1,2,...** | iloc[2] = fila #3 | loc[2] = fila con etiqueta 2 (mismo!) |
| **Si tu indice es 'a','b','c'** | iloc[0] = primera fila | loc['a'] = primera fila |
| **Si tu indice es 100,200,300** | iloc[0] = fila #1 | loc[100] = fila con etiqueta 100 |
| **Slicing** | excluye el final (Python) | INCLUYE el final |
| **Si la etiqueta no existe** | IndexError | KeyError |

#### Ejemplo que aclara TODO

```python
df = pd.DataFrame({'val': [10, 20, 30]}, index=[100, 200, 300])

df.iloc[0]    # 10  (POSICION 0 = primera fila)
df.loc[100]   # 10  (ETIQUETA 100 = misma fila)

df.iloc[2]    # 30  (POSICION 2 = tercera fila)
df.loc[2]     # KeyError! No hay etiqueta 2 (las etiquetas son 100,200,300)

df.iloc[0:2]  # filas con posicion 0 y 1   (excluye 2, como Python)
df.loc[100:200]  # filas con etiqueta 100 Y 200  (INCLUYE el final!)
```

#### Regla de oro

> **Si lo piensas en numero de fila -> `.iloc`. Si lo piensas en nombre/etiqueta -> `.loc`.**

#### Sin .loc/.iloc (estilo antiguo): NO LO USES

`df[2]` con un indice numerico es ambiguo: pandas no sabe si quieres la posicion o la etiqueta. **Siempre** usa `.iloc[]` o `.loc[]` para evitar errores. Las versiones nuevas de Pandas incluso te dan warnings si lo haces sin `.loc`/`.iloc`."""
        )},
        {"type": "md", "src": tu_turno(4,
            """Crea este DataFrame:

```python
df = pd.DataFrame({
    'producto': ['pan', 'leche', 'huevos', 'queso'],
    'precio':   [1.20, 0.95, 2.50, 4.30],
    'stock':    [50, 30, 100, 20]
}, index=['p1', 'p2', 'p3', 'p4'])
```

Realiza:
1. Accede a la **primera fila** usando `.iloc`.
2. Accede a la fila con etiqueta `'p3'` usando `.loc`.
3. Accede al **precio** del producto `'p2'` (celda concreta) con `.loc[fila, columna]`.
4. Saca las **2 primeras filas** y solo las columnas `'producto'` y `'precio'`.
5. Saca las filas desde `'p2'` hasta `'p4'` (incluido) con `.loc`.
6. Saca las mismas filas con `.iloc` (recuerda que excluye el final)."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n# df = pd.DataFrame({\n#     'producto': ['pan','leche','huevos','queso'],\n#     'precio':   [1.20, 0.95, 2.50, 4.30],\n#     'stock':    [50, 30, 100, 20]\n# }, index=['p1','p2','p3','p4'])\n#\n# # 1) Primera fila por POSICION\n# print(df.iloc[0])\n#\n# # 2) Fila con ETIQUETA 'p3'\n# print(df.loc['p3'])\n#\n# # 3) Celda concreta: fila 'p2', columna 'precio'\n# print(df.loc['p2', 'precio'])\n#\n# # 4) 2 primeras filas, solo 2 columnas\n# print(df.iloc[:2][['producto','precio']])\n# # o:\n# print(df.loc[['p1','p2'], ['producto','precio']])\n#\n# # 5) Slicing con .loc INCLUYE el final\n# print(df.loc['p2':'p4'])     # 3 filas (p2, p3, p4)\n#\n# # 6) Slicing con .iloc EXCLUYE el final\n# print(df.iloc[1:4])          # 3 filas (indices 1,2,3 -> p2, p3, p4)\n# print(df.iloc[1:3])          # 2 filas (p2, p3) -- el 4 no entra!\n"},
    ]))

# -------- AMBIGUEDAD --------
if ID_AMBIG:
    plan.append((ID_AMBIG, [
        {"type": "md", "src": aviso(
            """**Resumen de la trampa que el codigo de arriba ilustra:**

Cuando creas `pd.DataFrame(..., index=[1,2,3])` y haces `frame[2]`, **pandas NO sabe** si quieres la fila con etiqueta 2 o la fila en posicion 2 (porque el indice y la posicion son ambos enteros).

**La regla salvavidas:**

> Cuando tu indice esta hecho de enteros (no de strings), **NUNCA uses `df[N]`**. Usa siempre `df.loc[N]` (etiqueta) o `df.iloc[N]` (posicion). Asi no te equivocas y el codigo es legible."""
        )},
    ]))

# -------- WARNING SLICES --------
if ID_WARNING_SLI:
    plan.append((ID_WARNING_SLI, [
        {"type": "md", "src": aviso(
            """**SettingWithCopyWarning: el warning mas famoso de Pandas.**

Cuando haces algo como `df[df['edad']>18]['edad'] = 0`, pandas no sabe si estas modificando el DataFrame original o una copia temporal. Te lanza el warning porque podria no funcionar.

**Forma INCORRECTA (chained indexing):**
```python
df[df['edad'] > 18]['edad'] = 99   # warning, y posiblemente NO modifica df
```

**Forma CORRECTA con .loc:**
```python
df.loc[df['edad'] > 18, 'edad'] = 99   # correcto, asignacion atomica
```

La regla: **si vas a ASIGNAR, usa siempre `.loc[fila, columna] = valor` en una sola operacion.**"""
        )},
    ]))

# -------- INDEX OBJ --------
if ID_INDEX_OBJ:
    plan.append((ID_INDEX_OBJ, [
        {"type": "md", "src": teoria(
            "El objeto Index: las 'etiquetas' son objetos especiales",
            """El `index` de una Series o DataFrame **NO es una lista**, es un objeto especial llamado `pd.Index`. Tiene tres caracteristicas que conviene recordar:

1. **Es inmutable**: no puedes hacer `df.index[0] = 99`. Para cambiar el indice, lo reemplazas entero (`df.index = nueva_lista` o `df.set_index('col')`).
2. **Soporta operaciones de set**: union, interseccion, diferencia entre indices.
3. **Permite duplicados** (aunque normalmente no quieras).

#### Operaciones tipicas con Index

```python
df.set_index('col_id')      # convierte una columna en indice
df.reset_index()            # devuelve el indice a 0..n y mueve el actual a columna
df.reset_index(drop=True)   # tira el indice viejo
df.sort_index()              # ordena por indice
df.sort_values('col')        # ordena por valores de una columna
df.index.name = 'mi_id'     # nombre del indice
```"""
        )},
    ]))

# -------- MASCARAS --------
if ID_MASCARAS:
    plan.append((ID_MASCARAS, [
        {"type": "md", "src": teoria(
            "Filtrado booleano en DataFrames: la herramienta del 90% del tiempo",
            """Filtrar filas que cumplen una condicion es probablemente lo que **mas vas a hacer en pandas**.

#### Patron basico

```python
# 1) Construyes una mascara booleana sobre alguna columna
mask = df['edad'] > 18

# 2) La aplicas al DataFrame entero -> obtienes solo las filas True
df[mask]

# Misma cosa en una linea:
df[df['edad'] > 18]
```

#### Operadores de comparacion

| Operador | Significado |
|---|---|
| `==`, `!=` | igual / distinto |
| `<`, `>`, `<=`, `>=` | comparaciones |
| `.isin([a,b,c])` | esta en la lista |
| `.between(a, b)` | entre dos valores (incluidos) |
| `.str.contains('texto')` | strings que contienen un texto |
| `.str.startswith('a')` | strings que empiezan por 'a' |
| `.isna()`, `.notna()` | NaN o no NaN |

#### Combinar condiciones (RECUERDA: con `&` `|` `~` y parentesis)

```python
df[(df['edad'] > 18) & (df['ciudad'] == 'Madrid')]
df[(df['salario'] < 20000) \\| (df['salario'] > 80000)]
df[~df['activo']]                 # negacion
df[df['ciudad'].isin(['Madrid','Valencia'])]
df[df['edad'].between(18, 65)]
```

#### Filtrado + seleccion de columnas

```python
df.loc[df['edad'] > 18, ['nombre', 'edad']]
```

Esta es la forma **canonica**: filtrar filas por condicion Y elegir columnas en una sola operacion."""
        )},
    ]))

# -------- FILTRO FILAS --------
if ID_FILTRO_FILAS:
    plan.append((ID_FILTRO_FILAS, [
        {"type": "md", "src": tu_turno(5,
            """Construye este DataFrame:

```python
df = pd.DataFrame({
    'nombre':  ['Ana','Bea','Carlos','David','Elena','Fernando'],
    'edad':    [25, 17, 41, 19, 35, 16],
    'ciudad':  ['Madrid','Sevilla','Valencia','Bilbao','Madrid','Sevilla'],
    'salario': [30000, 0, 60000, 22000, 50000, 0]
})
```

Resuelve usando filtrado booleano:

1. Personas **mayores de edad** (>= 18).
2. Personas que viven en **Madrid o Valencia** (usa `.isin`).
3. Personas con salario **entre 20000 y 50000** (usa `.between`).
4. Personas mayores de edad **Y** que viven en `'Madrid'` (combinacion con `&`).
5. Solo el `'nombre'` y `'salario'` de los de Madrid (filtrado + seleccion de columnas con `.loc`).

> Recuerda los parentesis al combinar condiciones."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n# df = pd.DataFrame({\n#     'nombre':  ['Ana','Bea','Carlos','David','Elena','Fernando'],\n#     'edad':    [25, 17, 41, 19, 35, 16],\n#     'ciudad':  ['Madrid','Sevilla','Valencia','Bilbao','Madrid','Sevilla'],\n#     'salario': [30000, 0, 60000, 22000, 50000, 0]\n# })\n#\n# # 1) Mayores de edad\n# print(df[df['edad'] >= 18])\n#\n# # 2) Madrid o Valencia\n# print(df[df['ciudad'].isin(['Madrid','Valencia'])])\n#\n# # 3) Salario entre 20000 y 50000\n# print(df[df['salario'].between(20000, 50000)])\n#\n# # 4) Mayores de edad Y de Madrid\n# print(df[(df['edad'] >= 18) & (df['ciudad'] == 'Madrid')])\n#\n# # 5) Nombre y salario de los de Madrid\n# print(df.loc[df['ciudad'] == 'Madrid', ['nombre','salario']])\n"},
    ]))

# -------- CARGAR --------
if ID_CARGAR:
    plan.append((ID_CARGAR, [
        {"type": "md", "src": teoria(
            "Cargar y guardar datos: CSV, Excel, JSON",
            """Pandas tiene **una familia entera** de funciones `read_*` y metodos `to_*`. La idea es la misma para todos los formatos.

| Formato | Leer | Escribir |
|---|---|---|
| CSV | `pd.read_csv('f.csv')` | `df.to_csv('f.csv', index=False)` |
| Excel | `pd.read_excel('f.xlsx')` | `df.to_excel('f.xlsx', index=False)` |
| JSON | `pd.read_json('f.json')` | `df.to_json('f.json')` |
| Parquet | `pd.read_parquet('f.parquet')` | `df.to_parquet('f.parquet')` |
| SQL | `pd.read_sql(query, conn)` | `df.to_sql('tabla', conn)` |
| HDF5 | `pd.read_hdf('f.h5')` | `df.to_hdf('f.h5', key='df')` |

#### Argumentos clave de `read_csv` (los que mas vas a usar)

| Argumento | Que hace |
|---|---|
| `sep=','` | Separador (a veces es `';'` o `'\\t'`) |
| `header=0` | Que fila usar como cabecera. `None` si no hay cabecera. |
| `names=[...]` | Nombres de columnas (cuando no hay cabecera) |
| `index_col=0` | Que columna usar como indice |
| `na_values=['?', '-']` | Que strings tratar como NaN |
| `encoding='latin-1'` | Para archivos no UTF-8 |
| `nrows=1000` | Leer solo las N primeras filas (util para inspeccionar grandes) |
| `skiprows=N` | Saltar N filas iniciales |
| `dtype={...}` | Forzar tipos por columna |
| `parse_dates=['fecha']` | Parsear columnas como fechas |

#### Cuidado con el separador

```python
# Si abres un CSV en Excel ESPANOL, el separador es ';' y los decimales con ','
pd.read_csv('datos_excel_es.csv', sep=';', decimal=',')
```

#### Inspeccionar antes de cargar todo

Cuando trabajes con archivos grandes, lee solo unas filas primero:

```python
df_muestra = pd.read_csv('grande.csv', nrows=10)
print(df_muestra.dtypes)
```"""
        )},
    ]))

# -------- DTYPES --------
if ID_DTYPES:
    plan.append((ID_DTYPES, [
        {"type": "md", "src": teoria(
            "Tipos de datos en Pandas: dtypes",
            """Cada **columna** de un DataFrame tiene un tipo (dtype). Conocerlos te evita bugs sutiles.

| dtype | Que es | Ejemplo |
|---|---|---|
| `int64` | enteros | 1, 2, 3 |
| `float64` | decimales (incluido NaN) | 1.5, NaN |
| `bool` | booleanos | True, False |
| `object` | strings o tipos mezclados | 'hola', None |
| `datetime64[ns]` | fechas | 2024-01-15 |
| `category` | categorica (eficiente) | 'M'/'F' |

#### Por que importa el dtype?

- **`object` con strings es lento**. Para columnas con valores repetitivos (genero, ciudad, categoria) considera `df['col'] = df['col'].astype('category')`.
- **Si una columna numerica sale como `object`**, casi siempre hay strings inesperados o un decimal mal escrito.
- **Operaciones aritmeticas** solo funcionan sobre tipos numericos.

#### Cambiar el dtype

```python
df['edad'] = df['edad'].astype(int)
df['fecha'] = pd.to_datetime(df['fecha'])
df['categoria'] = df['categoria'].astype('category')
```

#### Inspeccion rapida

```python
df.dtypes        # tipos por columna
df.info()        # tipos + memoria + NaN por columna
df.describe()    # estadisticas (solo numericas por defecto)
df.describe(include='all')   # incluyendo objetos
```"""
        )},
    ]))

# -------- DESCRIBE/INFO --------
if ID_INFO:
    plan.append((ID_INFO, [
        {"type": "md", "src": dato(
            """Tres metodos imprescindibles para **inspeccionar un DataFrame que acabas de cargar**:

| Metodo | Cuando usar |
|---|---|
| `df.head(n)` | Primer vistazo a los datos (5 filas por defecto) |
| `df.tail(n)` | Ultimas N filas (util para detectar filas raras al final) |
| `df.sample(n)` | N filas aleatorias (mas representativo que head para datos ordenados) |
| `df.info()` | tipos, no nulos, memoria |
| `df.describe()` | stats: count, mean, std, min, 25%, 50%, 75%, max |
| `df.dtypes` | solo los tipos |
| `df.shape` | (filas, columnas) |
| `df.columns` | nombres de columnas |
| `df.isna().sum()` | cuantos NaN por columna |

**Rutina recomendada nada mas cargar un dataset:**

```python
df = pd.read_csv('mi_archivo.csv')
print(df.shape)
print(df.dtypes)
print(df.head())
print(df.isna().sum())
print(df.describe())
```"""
        )},
    ]))

# -------- GROUPBY --------
if ID_GROUPBY:
    plan.append((ID_GROUPBY, [
        {"type": "md", "src": teoria(
            "groupby: agrupar y agregar",
            """`groupby` es el equivalente al `GROUP BY` de SQL. **Agrupa filas que comparten un valor** y luego aplica una operacion (suma, media, conteo) a cada grupo.

#### Patron split-apply-combine

```python
df.groupby('ciudad')['salario'].mean()
#         |          |         |
#       (split)  (columna)  (apply: aggregator)
```

1. **Split**: pandas separa el DF en grupos segun los valores de `'ciudad'`.
2. **Apply**: aplica `mean()` a la columna `'salario'` de cada grupo.
3. **Combine**: junta los resultados en una nueva Series/DataFrame.

#### Ejemplos

```python
# Salario medio por ciudad
df.groupby('ciudad')['salario'].mean()

# Multiples agregaciones de varias columnas
df.groupby('ciudad').agg({
    'salario': ['mean', 'max'],
    'edad':    'mean'
})

# Cuantas filas por grupo
df.groupby('ciudad').size()

# Agrupar por dos columnas
df.groupby(['ciudad', 'genero'])['salario'].mean()

# Aplicar una funcion personalizada
df.groupby('ciudad')['salario'].apply(lambda x: x.max() - x.min())
```

#### Sort de los resultados

```python
df.groupby('ciudad')['salario'].mean().sort_values(ascending=False)
```"""
        )},
        {"type": "md", "src": tu_turno(6,
            """Tienes este DataFrame de empleados:

```python
df = pd.DataFrame({
    'empleado':  ['Ana','Bea','Carlos','David','Elena','Fernando','Gabriel','Hugo'],
    'ciudad':    ['Madrid','Madrid','Sevilla','Sevilla','Valencia','Valencia','Madrid','Sevilla'],
    'departamento': ['IT','RRHH','IT','Ventas','IT','RRHH','Ventas','IT'],
    'salario':   [30000, 28000, 45000, 33000, 50000, 25000, 32000, 42000]
})
```

Resuelve:

1. **Salario medio por ciudad**.
2. **Salario MAXIMO por departamento**.
3. **Numero de empleados** en cada ciudad (usa `.size()`).
4. Salario medio por **ciudad y departamento** a la vez (groupby con dos columnas).
5. **Ordena** la tabla del paso 1 de mayor a menor salario."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n# df = pd.DataFrame({\n#     'empleado':  ['Ana','Bea','Carlos','David','Elena','Fernando','Gabriel','Hugo'],\n#     'ciudad':    ['Madrid','Madrid','Sevilla','Sevilla','Valencia','Valencia','Madrid','Sevilla'],\n#     'departamento': ['IT','RRHH','IT','Ventas','IT','RRHH','Ventas','IT'],\n#     'salario':   [30000, 28000, 45000, 33000, 50000, 25000, 32000, 42000]\n# })\n#\n# # 1) Salario medio por ciudad\n# print(df.groupby('ciudad')['salario'].mean())\n#\n# # 2) Salario maximo por departamento\n# print(df.groupby('departamento')['salario'].max())\n#\n# # 3) Numero de empleados por ciudad\n# print(df.groupby('ciudad').size())\n#\n# # 4) Salario medio por ciudad y departamento\n# print(df.groupby(['ciudad','departamento'])['salario'].mean())\n#\n# # 5) Ordenado de mayor a menor\n# print(df.groupby('ciudad')['salario'].mean().sort_values(ascending=False))\n"},
    ]))

# -------- EJERCICIOS final --------
if ID_EJERCICIOS:
    plan.append((ID_EJERCICIOS, [
        {"type": "md", "src": teoria(
            "Resumen final: la chuleta que vas a querer guardar",
            """Has cubierto los fundamentos de Pandas. Aqui tienes la **chuleta condensada** para volver cuando lo necesites.

#### Crear / cargar
```python
pd.Series([...])
pd.DataFrame({...})
pd.read_csv(path, sep=',', index_col=0, na_values=['?'], encoding='utf-8')
pd.read_excel(path, sheet_name=0)
pd.read_json(path)
df.to_csv(path, index=False)
```

#### Inspeccion
```python
df.shape; df.dtypes; df.columns; df.index
df.head(); df.tail(); df.sample(5)
df.info(); df.describe()
df.isna().sum()
```

#### Indexacion (CRITICO)
```python
df['col']                         # columna -> Series
df[['col1','col2']]               # varias columnas -> DataFrame
df.loc[fila_etiq]                 # fila por etiqueta
df.loc[fila_etiq, 'col']          # celda por etiqueta
df.iloc[i]                        # fila por posicion
df.iloc[i, j]                     # celda por posicion
df.loc[df['edad']>18, ['nom']]    # filtro + seleccion (canonica)
```

#### Filtrado booleano
```python
df[df['col'] > x]
df[df['col'].isin([a, b])]
df[df['col'].between(a, b)]
df[df['col'].str.contains('foo')]
df[(df['a'] > 1) & (df['b'] < 5)]      # & | ~ con parentesis
```

#### NaN
```python
df.isna(); df.notna()
df.dropna(); df.dropna(subset=['col'])
df.fillna(0); df['c'].fillna(df['c'].mean())
```

#### Ordenar
```python
df.sort_values('col')
df.sort_values(['c1','c2'], ascending=[True, False])
df.sort_index()
```

#### Agrupar
```python
df.groupby('col').mean()
df.groupby('col').agg({'x': 'mean', 'y': 'sum'})
df.groupby(['c1','c2']).size()
```

#### Modificar
```python
df['nueva'] = df['a'] + df['b']
df.loc[df['edad']>18, 'adulto'] = True
df.drop('col', axis=1, inplace=True)
df.drop(index_etiq, axis=0)
df.rename(columns={'old':'new'})
```

#### Apply / map
```python
df['col'].apply(lambda x: x*2)
df['col'].map({'F':'Mujer','M':'Hombre'})
df.apply(lambda row: row['a']+row['b'], axis=1)
```"""
        )},
        {"type": "md", "src": tu_turno(7,
            """**Reto integrador**: con el dataset de usuarios de MovieLens (`users_dataset`) que ya cargaste arriba, responde:

1. Cuantos hombres (`Gender == 'M'`) y cuantas mujeres (`Gender == 'F'`) hay en total? (Pista: `value_counts()`)
2. Cual es la **edad media** por genero?
3. Cuantos NaN hay en cada columna?
4. Crea una nueva columna `'Mayor_25'` que sea True/False segun la edad sea > 25.
5. Los **5 codigos postales** mas frecuentes (`value_counts().head(5)`).
6. Guarda el DataFrame resultante a un nuevo CSV `users_modificado.csv` (sin indice)."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# # 1) Conteo por genero\n# print(users_dataset['Gender'].value_counts())\n#\n# # 2) Edad media por genero\n# print(users_dataset.groupby('Gender')['Age'].mean())\n#\n# # 3) NaN por columna\n# print(users_dataset.isna().sum())\n#\n# # 4) Nueva columna booleana\n# users_dataset['Mayor_25'] = users_dataset['Age'] > 25\n# print(users_dataset.head())\n#\n# # 5) Top 5 codigos postales\n# print(users_dataset['Zip-code'].value_counts().head(5))\n#\n# # 6) Guardar a CSV\n# import os\n# users_dataset.to_csv(os.path.join('res', 'users_modificado.csv'), index=False)\n# print('Guardado.')\n"},
    ]))

enhance(NB, plan)
print("Done.")

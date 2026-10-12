"""Aplica mejoras al notebook 12_Data_Processing con bloques de colores y teoria detallada."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, solucion_md, dato, aviso

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_12_Data_Processing.ipynb"

import json
nb = json.load(open(NB, encoding="utf-8"))

def find_id(text_fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if text_fragment in src:
            return c["id"]
    return None

# IDs clave del notebook 12
ID_TITULO         = nb["cells"][0]["id"]                                 # cell 0 (intro)
ID_JOIN_MERGE     = find_id("Uniendo datasets con 'join' y 'merge'")     # cell 2
ID_COMBINAR       = find_id("Combinar varios datasets")                  # cell 3
ID_PIVOT          = find_id("## Pivot")                                  # cell 12
ID_AGRUPACIONES   = find_id("## Agrupaciones")                           # cell 15
ID_STRINGS_MAN    = find_id("## Manipulaci")                             # cell 18 (Manipulacion de strings)
ID_REGEX          = find_id("Ejemplo con Regular Expressions")           # cell 31
ID_EJ_COLECC      = find_id("Ejercicio de operaciones con colecciones")  # cell 39
ID_REDUCE         = find_id("#### Reduce")                               # cell 40
ID_MAP            = find_id("#### Map")                                  # cell 46
ID_FILTER         = find_id("#### Filter")                               # cell 49
ID_TIPO_DATOS     = find_id("## Cambiar tipo de datos")                  # cell 52
ID_TRANSFORM      = find_id("Transformaci")                              # cell 54 (Transformacion de variables - calidad de datos)
ID_TRATAMIENTO    = find_id("## Tratamiento de valores nulos")           # cell 62 (codigo)
# El subtitulo "Tratamiento de valores nulos" aparece como comentario; mejor anclar al cell 61 (display matrix)
# Buscamos el que tiene "## Tratamiento" en markdown:
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if c.get("cell_type") == "code" and "Tratamiento de valores nulos" in src:
        ID_TRATAMIENTO = c["id"]
        break
ID_DUPLICADOS     = find_id("Tratar valores duplicados")                 # cell 67
ID_CATEGORICOS    = find_id("## Valores categ")                          # cell 70
ID_DISCRETIZAR    = find_id("Discretizaci")                              # cell 74

plan = []

# -------- INTRO al notebook --------
plan.append((ID_TITULO, [
    {"type": "md", "src": teoria(
        "Como leer este notebook (version mejorada)",
        """Este notebook fue **enriquecido** para ayudarte a aprender escribiendo codigo. Vas a encontrar tres tipos de bloques de colores:

<div style="background-color:#e7f5ff;border-left:6px solid #1c7ed6;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AZUL = TEORIA</b></div> -> explicacion en palabras simples antes de cada concepto.

<div style="background-color:#fff9db;border-left:6px solid #f59f00;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AMARILLO = TU TURNO</b></div> -> el ejercicio que TU debes resolver. Hay una celda vacia debajo donde escribes el codigo.

<div style="background-color:#ebfbee;border-left:6px solid #2f9e44;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>VERDE = SOLUCION</b></div> -> codigo de referencia comentado por si te trabas. Destapa solo despues de intentar.

> **Promesa importante**: el codigo y la teoria del profesor original no se han tocado. Solo se han ANADIDO bloques. Asi puedes seguir comparando con la version original cuando quieras."""
    )},
    {"type": "md", "src": teoria(
        "Procesamiento de datos: el 80% del trabajo real",
        """En proyectos de Machine Learning e Inteligencia Artificial, **el 70-80% del tiempo se dedica a preparar los datos**, no a entrenar modelos. La calidad del modelo nunca puede superar la calidad de los datos: *garbage in, garbage out*.

#### Que problemas tipicos aparecen en los datos crudos?

| Problema | Que significa | Tipico en |
|---|---|---|
| **Valores faltantes (NaN)** | Celdas vacias o nulas | Encuestas, sensores, bases con campos opcionales |
| **Duplicados** | Filas repetidas | Combinacion de fuentes, errores de captura |
| **Outliers** | Valores extremos atipicos | Errores de medicion, casos raros, fraudes |
| **Formatos inconsistentes** | "Madrid" vs "madrid" vs "MADRID" | Datos cargados manualmente |
| **Tipos incorrectos** | Numeros guardados como string | CSV mal parseado |
| **Variables categoricas en texto** | Modelo necesita numeros | Genero, pais, nivel educativo |
| **Escalas distintas** | Una columna [0,1], otra [0,1_000_000] | Algoritmos de distancia (KNN, K-means, redes) |

#### Las cuatro etapas tipicas de un pipeline de procesamiento

1. **Limpieza** -> quitar/imputar NaN, eliminar duplicados, detectar outliers, corregir formatos.
2. **Transformacion** -> derivar nuevas columnas, separar/concatenar campos, parsear strings.
3. **Encoding** -> convertir variables categoricas a numericas (one-hot, label, ordinal).
4. **Normalizacion / Escalado** -> poner todas las columnas numericas en escalas comparables (min-max, z-score).

Este notebook te lleva por las herramientas de pandas para resolver cada una. Los **TU TURNO** te haran practicar sobre datasets reales."""
    )},
]))

# ============ JOIN/MERGE ============
plan.append((ID_JOIN_MERGE, [
    {"type": "md", "src": teoria(
        "merge / join: combinar datasets relacionados",
        """Cuando trabajas con datos del mundo real, casi nunca tienes UN unico dataset gigante: tienes **varios datasets relacionados** por una clave en comun (ej: `UserID`, `MovieID`, `ProductCode`).

`pd.merge()` (y `DataFrame.join()`) replican el `JOIN` de SQL.

#### Tipos de union (parametro `how`)

| `how` | Resultado | Equivalente SQL |
|---|---|---|
| `'inner'` | Solo filas con clave en **ambos** | `INNER JOIN` |
| `'left'` | Todas las del izquierdo + las que matchen del derecho | `LEFT JOIN` |
| `'right'` | Todas las del derecho + las que matchen del izquierdo | `RIGHT JOIN` |
| `'outer'` | **Todas** las filas de los dos (rellena NaN donde no haya match) | `FULL OUTER JOIN` |

#### Parametros importantes

```python
pd.merge(df_left, df_right,
         on='UserID',         # columna comun (debe llamarse igual)
         left_on='id_user',   # si tienen distinto nombre
         right_on='user_id',
         how='inner')         # tipo de union
```

> **Cuidado:** si la clave no es unica en alguno de los dos lados, el numero de filas resultante puede **multiplicarse** (es la causa numero uno de bugs en pipelines de datos)."""
    )},
]))

plan.append((ID_COMBINAR, [
    {"type": "md", "src": tu_turno(1,
        """Crea dos DataFrames manuales (puedes hacerlos pequenos):

```python
clientes = pd.DataFrame({
    'cliente_id': [1, 2, 3, 4],
    'nombre':     ['Ana', 'Pedro', 'Lucia', 'Mario']
})
pedidos = pd.DataFrame({
    'cliente_id': [1, 1, 2, 5],
    'producto':   ['libro', 'taza', 'mochila', 'reloj'],
    'precio':     [12.5, 8.0, 30.0, 45.0]
})
```

1. Haz un `merge` **inner** entre los dos.
2. Haz un `merge` **left** (que pasa con Lucia y Mario que no tienen pedidos?).
3. Haz un `merge` **outer** (que pasa con el cliente_id 5 que no esta en clientes?).
4. Cuenta cuantas filas tiene cada resultado y explica por que."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\n\nclientes = pd.DataFrame({\n    'cliente_id': [1, 2, 3, 4],\n    'nombre':     ['Ana', 'Pedro', 'Lucia', 'Mario']\n})\npedidos = pd.DataFrame({\n    'cliente_id': [1, 1, 2, 5],\n    'producto':   ['libro', 'taza', 'mochila', 'reloj'],\n    'precio':     [12.5, 8.0, 30.0, 45.0]\n})\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n#\n# # 1) inner: solo coincidencias en AMBOS lados (cliente_id 1 y 2)\n# inner = pd.merge(clientes, pedidos, on='cliente_id', how='inner')\n# print('INNER:', len(inner), 'filas')\n# print(inner)\n#\n# # 2) left: todos los clientes; Lucia y Mario aparecen con NaN en pedidos\n# left = pd.merge(clientes, pedidos, on='cliente_id', how='left')\n# print('LEFT:', len(left), 'filas')\n# print(left)\n#\n# # 3) outer: incluye cliente 5 (no esta en clientes) -> nombre NaN\n# outer = pd.merge(clientes, pedidos, on='cliente_id', how='outer')\n# print('OUTER:', len(outer), 'filas')\n# print(outer)\n#\n# # Conclusion:\n# # - inner descarta filas sin match (ojo si tu pipeline depende de ello)\n# # - left/right preserva el lado elegido y rellena con NaN\n# # - outer es el union total y suele introducir mas NaN\n"},
]))

# ============ PIVOT ============
plan.append((ID_PIVOT, [
    {"type": "md", "src": teoria(
        "pivot_table: resumir datos en una tabla cruzada",
        """Una **tabla pivote** te permite ver un valor numerico **agregado** por dos dimensiones a la vez (filas y columnas), como una tabla dinamica de Excel.

```python
df.pivot_table(values='Rating',     # columna que se agrega
               index='Gender',       # filas
               columns='Age',        # columnas
               aggfunc='mean')       # como agregar (default: mean)
```

#### Funciones de agregacion comunes (`aggfunc`)

| `aggfunc` | Que calcula |
|---|---|
| `'mean'` | Media (por defecto) |
| `'sum'` | Suma |
| `'count'` | Cuantas observaciones |
| `'min'` / `'max'` | Minimo / maximo |
| `'std'` / `'var'` | Desviacion estandar / varianza |
| `'median'` | Mediana |
| Lista: `['mean', 'count']` | Varias a la vez |
| Funcion lambda | Personalizada |

#### Ejemplo: ratings medios por genero y edad

Te ayuda a responder preguntas como: *los hombres jovenes valoran las peliculas mas alto que las mujeres mayores?*. Es la base del **analisis exploratorio (EDA)** y muchas veces detecta sesgos en los datos antes de modelar."""
    )},
    {"type": "md", "src": tu_turno(2,
        """Sobre el dataset `all_dataset` que ya construyeron arriba (con users + ratings + movies):

1. Calcula la **media de Rating** por `Occupation` (filas) y `Gender` (columnas) usando `pivot_table`.
2. Calcula el **conteo de ratings** por `Occupation` y `Gender` (cambia `aggfunc='count'`).
3. Identifica que combinacion de `Occupation` x `Gender` ha dado el rating medio mas alto (puedes usar `.stack().idxmax()`)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo (reusa all_dataset definido arriba):\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# # 1) Rating medio por Occupation x Gender\n# tabla_media = all_dataset.pivot_table('Rating',\n#                                       index='Occupation',\n#                                       columns='Gender',\n#                                       aggfunc='mean')\n# display(tabla_media)\n#\n# # 2) Conteo de ratings\n# tabla_conteo = all_dataset.pivot_table('Rating',\n#                                       index='Occupation',\n#                                       columns='Gender',\n#                                       aggfunc='count')\n# display(tabla_conteo)\n#\n# # 3) Combinacion con la media mas alta\n# # stack convierte la tabla en serie; idxmax devuelve la (Occupation, Gender)\n# combinacion_top = tabla_media.stack().idxmax()\n# print('Combinacion con rating medio mas alto:', combinacion_top)\n# print('Valor:', tabla_media.stack().max())\n"},
]))

# ============ AGRUPACIONES ============
plan.append((ID_AGRUPACIONES, [
    {"type": "md", "src": teoria(
        "Agrupaciones y conteos: explorar la composicion de los datos",
        """Antes de cualquier transformacion, conviene **conocer** los datos. Estas son las herramientas basicas:

| Metodo | Para que sirve |
|---|---|
| `Series.unique()` | Lista de **valores distintos** que aparecen |
| `Series.nunique()` | **Cuantos** valores distintos hay |
| `Series.value_counts()` | Frecuencia de cada valor (ordenado desc) |
| `Series.value_counts(normalize=True)` | Frecuencia **relativa** (porcentaje) |
| `df.groupby(col).agg(...)` | Agrupa por una columna y aplica funciones |
| `df.describe()` | Estadisticos basicos (count, mean, std, min, max, cuartiles) |
| `df.info()` | Tipos de datos y memoria |

#### Patron clasico: groupby + agg

```python
df.groupby('Gender').agg({
    'Rating': ['mean', 'count', 'std'],
    'Age':    'mean'
})
```

Esto te da, **por cada genero**, varias estadisticas a la vez.

#### Detectar problemas con value_counts

```python
df['Pais'].value_counts()
# Espana    1200
# espana       8     <- error de capitalizacion!
# ESPANA       3
# Spain        5     <- idioma diferente
```

Solo con `value_counts` ya detectaste 4 problemas que un `==` ingenuo no ve."""
    )},
]))

# ============ MANIPULACION DE STRINGS ============
plan.append((ID_STRINGS_MAN, [
    {"type": "md", "src": teoria(
        "Manipulacion de strings en pandas: el accesor <code>.str</code>",
        """En pandas, los metodos de string se aplican a **una columna entera** (Series) usando el accesor `.str`. Asi evitas escribir bucles.

```python
df['nombre'].str.upper()           # todo en mayusculas
df['nombre'].str.lower()           # todo en minusculas
df['nombre'].str.strip()           # quita espacios en bordes
df['nombre'].str.replace('a','@')  # reemplaza
df['nombre'].str.contains('Ana')   # bool: contiene?
df['nombre'].str.startswith('A')   # bool: empieza con?
df['nombre'].str.split('|')        # lista de partes
df['nombre'].str.len()             # longitud
df['nombre'].str[0]                # primer caracter de cada fila
df['nombre'].str[:3]               # tres primeros
```

#### Limpieza tipica de strings

| Problema | Solucion |
|---|---|
| Espacios extra: `'  Madrid '` | `.str.strip()` |
| Mayusculas mezcladas | `.str.lower()` o `.str.title()` |
| Tildes / caracteres raros | `.str.normalize('NFKD')` + filtrado |
| Separadores varios `'a;b,c'` | `.str.replace(';',',').str.split(',')` |
| Necesitas extraer un patron | `.str.extract(r'(...)')` con regex |

> **Buena practica:** crea una funcion `limpiar_texto(s)` que aplique strip + lower + replace de tildes, y aplicala con `.apply` a todas las columnas de texto al cargar el CSV. Te ahorra horas de bugs."""
    )},
    {"type": "md", "src": tu_turno(3,
        """Tienes esta serie con nombres de ciudades cargada de forma sucia:

```python
ciudades = pd.Series(['  Madrid', 'madrid ', 'MADRID', 'BARCELONA', 'Barcelona  ', 'valencia', 'Valencia'])
```

Aplicale las transformaciones necesarias para que **todas las versiones de Madrid** queden iguales (lo mismo con las otras). Despues, usa `value_counts` para ver el conteo final.

> Pista: necesitas combinar `.str.strip()` y `.str.lower()` (o `.str.title()`)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\nciudades = pd.Series(['  Madrid', 'madrid ', 'MADRID', 'BARCELONA', 'Barcelona  ', 'valencia', 'Valencia'])\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n# ciudades = pd.Series(['  Madrid', 'madrid ', 'MADRID', 'BARCELONA', 'Barcelona  ', 'valencia', 'Valencia'])\n#\n# # 1) Quitar espacios en los bordes\n# # 2) Pasar todo al mismo case (title -> 'Madrid', 'Barcelona', ...)\n# ciudades_limpias = ciudades.str.strip().str.lower().str.title()\n# print(ciudades_limpias)\n# print()\n# print(ciudades_limpias.value_counts())\n# # Resultado: Madrid 3, Barcelona 2, Valencia 2\n"},
]))

# ============ REGEX ============
plan.append((ID_REGEX, [
    {"type": "md", "src": teoria(
        "Expresiones regulares (regex): patrones para texto",
        """Las **regex** son pequenos lenguajes para describir patrones en texto. En pandas se usan con `.str.match`, `.str.contains`, `.str.extract` y `.str.replace`.

#### Atomos basicos

| Patron | Significa |
|---|---|
| `.` | Cualquier caracter (excepto salto de linea) |
| `\\d` | Un digito (0-9) |
| `\\w` | Letra, digito o `_` |
| `\\s` | Espacio en blanco |
| `[abc]` | a, b o c |
| `[^abc]` | Cualquier caracter EXCEPTO a, b, c |
| `[a-z]` | Cualquier minuscula |

#### Cuantificadores

| Patron | Significa |
|---|---|
| `*` | 0 o mas veces |
| `+` | 1 o mas veces |
| `?` | 0 o 1 vez (opcional) |
| `{5}` | exactamente 5 |
| `{3,7}` | entre 3 y 7 |

#### Anclas

| Patron | Significa |
|---|---|
| `^` | Inicio de string |
| `$` | Final de string |

#### Grupos

| Patron | Significa |
|---|---|
| `(...)` | Grupo de captura (lo que extraes) |
| `(?:...)` | Grupo SIN captura |

#### Ejemplos tipicos

```python
'^\\d{5}$'          # exactamente 5 digitos -> codigos postales espanoles
'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'   # email
'\\b\\d{4}\\b'       # un numero de 4 digitos (anio) entre limites de palabra
'(\\d{2})/(\\d{2})/(\\d{4})'   # fecha dd/mm/yyyy con tres grupos
```

> **Tip:** [regex101.com](https://regex101.com/) te muestra que matchea cada parte de tu regex en tiempo real. Imprescindible al aprender."""
    )},
]))

# ============ EJERCICIO COLECCIONES (ANTES DE REDUCE/MAP/FILTER) ============
plan.append((ID_EJ_COLECC, [
    {"type": "md", "src": teoria(
        "reduce, map y filter: programacion funcional aplicada a datos",
        """Estas tres funciones vienen de la **programacion funcional**. Aunque pandas tiene equivalentes mas idiomaticos, conocerlas te ayuda a leer codigo de otros y a entender mejor `apply`.

| Funcion | Entrada | Salida | Para que |
|---|---|---|---|
| `reduce(f, iter)` | iterable | **un valor** | Acumular (suma, producto, max...) |
| `map(f, iter)` | iterable | iterable | Transformar cada elemento |
| `filter(f, iter)` | iterable + condicion | iterable | Quedarte con los que cumplen |

| Funcional | Pandas equivalente |
|---|---|
| `reduce(lambda x,y: x+y, lista)` | `Series.sum()`, `.any()`, `.all()` |
| `map(lambda x: x*2, lista)` | `Series.apply(lambda x: x*2)` |
| `filter(lambda x: x>0, lista)` | `Series[Series > 0]` |

> En 99% de los casos en pandas, **prefiere las soluciones nativas** (`apply`, mascaras booleanas, agregaciones). Son mas rapidas y mas legibles. `reduce/map/filter` son utiles en Python puro."""
    )},
]))

# ============ TIPO DE DATOS ============
plan.append((ID_TIPO_DATOS, [
    {"type": "md", "src": teoria(
        "Tipos de datos en pandas: por que importan",
        """Cada columna (`Series`) tiene un **dtype** que determina:

- **Que operaciones puedes hacer** (no puedes sumar strings).
- **Cuanta memoria ocupa** (`int8` ocupa 8x menos que `int64`).
- **Velocidad** (operaciones vectorizadas en `int` son rapidisimas).

#### Tipos comunes

| dtype pandas | Tipo Python | Ejemplo |
|---|---|---|
| `int64` / `int32` / `int8` | int | Edades, contadores |
| `float64` / `float32` | float | Precios, scores, NaN |
| `bool` | bool | Mascaras, flags |
| `object` | str / mixto | Texto generico (lento) |
| `string` (nuevo) | str | Texto explicito (mejor) |
| `category` | categorias | Genero, pais (con pocos valores distintos) |
| `datetime64[ns]` | datetime | Fechas, timestamps |
| `timedelta64[ns]` | timedelta | Duraciones |

#### Convertir tipos

```python
df['edad'] = df['edad'].astype(int)
df['precio'] = df['precio'].astype('float32')
df['fecha'] = pd.to_datetime(df['fecha'])
df['categoria'] = df['categoria'].astype('category')
```

#### Cuando usar `category`?

Cuando una columna tiene **pocos valores distintos repetidos muchas veces** (ej: genero con 'M'/'F'/'Otro' en un millon de filas). Pandas guarda los valores una sola vez y referencia con un entero. **Ahorra muchisima memoria**."""
    )},
]))

# ============ TRANSFORMACION DE VARIABLES (NULL/DUPLICATES) ============
plan.append((ID_TRANSFORM, [
    {"type": "md", "src": teoria(
        "Limpieza de datos: el corazon del preprocesado",
        """Antes de entrenar cualquier modelo necesitas detectar y resolver:

#### 1. Valores faltantes (NaN, None, NaT)

**Como detectarlos:**
```python
df.isnull().sum()              # cuantos NaN por columna
df.isnull().sum().sum()        # total de NaN en el DataFrame
df.isnull().mean() * 100       # % de NaN por columna
df[df['col'].isnull()]         # filas con NaN en 'col'
```

**Como tratarlos:** ver el bloque siguiente sobre **imputacion**.

#### 2. Duplicados

```python
df.duplicated()                # bool por fila
df.duplicated().sum()          # cuantos
df.drop_duplicates()           # quitar duplicados completos
df.drop_duplicates(subset=['email'])   # duplicados solo en 'email'
df.drop_duplicates(keep='first' | 'last' | False)
```

#### 3. Outliers (valores extremos)

**Detectar (regla del rango intercuartil, IQR):**
```python
Q1 = df['col'].quantile(0.25)
Q3 = df['col'].quantile(0.75)
IQR = Q3 - Q1
lim_inf = Q1 - 1.5 * IQR
lim_sup = Q3 + 1.5 * IQR
outliers = df[(df['col'] < lim_inf) | (df['col'] > lim_sup)]
```

**Tratar:** eliminar, capar (clip), o transformar (log).

#### 4. Formatos inconsistentes

`.str.strip().str.lower()`, regex con `.str.replace(r'\\s+', ' ', regex=True)`, parseo de fechas con `pd.to_datetime`."""
    )},
    {"type": "md", "src": teoria(
        "Imputacion: rellenar valores faltantes",
        """**Imputar** = sustituir un NaN por un valor razonable. La estrategia depende del tipo de variable y del contexto.

| Estrategia | Cuando usar | Codigo pandas |
|---|---|---|
| **Eliminar fila** | Pocos NaN, datos suficientes | `df.dropna()` |
| **Eliminar columna** | Columna con > 50% NaN | `df.dropna(axis=1)` |
| **Media** (mean) | Numerica simetrica, sin outliers | `df['col'].fillna(df['col'].mean())` |
| **Mediana** (median) | Numerica con outliers o sesgada | `df['col'].fillna(df['col'].median())` |
| **Moda** (mode) | Categorica o discreta | `df['col'].fillna(df['col'].mode()[0])` |
| **Valor fijo** | Sabes el valor 'por defecto' | `df['col'].fillna(0)` o `'desconocido'` |
| **Forward fill** (ffill) | Series temporales | `df['col'].ffill()` |
| **Backward fill** (bfill) | Series temporales | `df['col'].bfill()` |
| **Interpolacion** | Series numericas continuas | `df['col'].interpolate()` |
| **Imputacion por grupo** | NaN distintos por categoria | `df.groupby('cat')['col'].transform(lambda x: x.fillna(x.median()))` |
| **Modelo (KNN, MICE)** | Datasets pequenos / criticos | `sklearn.impute.KNNImputer` |

#### Tabla de decision rapida

| Tu variable es... | Empieza por |
|---|---|
| Numerica simetrica | **Media** |
| Numerica sesgada o con outliers | **Mediana** |
| Categorica | **Moda** o `'desconocido'` |
| Serie temporal | **ffill / bfill / interpolate** |
| > 40% de NaN | Considera **eliminar la columna** |

> **Atencion:** la imputacion **se calcula sobre el train**, no sobre todo el dataset (si no, cometes *data leakage*). En sklearn usa `SimpleImputer` dentro de un `Pipeline`."""
    )},
]))

plan.append((ID_TRATAMIENTO, [
    {"type": "md", "src": tu_turno(4,
        """Crea este DataFrame con valores faltantes y trabajalo:

```python
import numpy as np
import pandas as pd
df = pd.DataFrame({
    'edad':    [25, np.nan, 30, 22, np.nan, 41, 28, np.nan, 35, 50],
    'salario': [30000, 45000, np.nan, 28000, 50000, np.nan, 33000, 42000, np.nan, 80000],
    'ciudad':  ['Madrid', 'Barcelona', np.nan, 'Madrid', 'Valencia', 'Madrid', np.nan, 'Barcelona', 'Sevilla', 'Madrid']
})
```

1. Cuantos NaN tiene cada columna? (usa `isnull().sum()`).
2. Imputa `edad` con la **mediana** (es numerica con un valor extremo, 50).
3. Imputa `salario` con la **media**.
4. Imputa `ciudad` con la **moda** (la mas frecuente).
5. Comprueba que ya no hay NaN."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport numpy as np\nimport pandas as pd\ndf = pd.DataFrame({\n    'edad':    [25, np.nan, 30, 22, np.nan, 41, 28, np.nan, 35, 50],\n    'salario': [30000, 45000, np.nan, 28000, 50000, np.nan, 33000, 42000, np.nan, 80000],\n    'ciudad':  ['Madrid', 'Barcelona', np.nan, 'Madrid', 'Valencia', 'Madrid', np.nan, 'Barcelona', 'Sevilla', 'Madrid']\n})\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# import pandas as pd\n# df = pd.DataFrame({\n#     'edad':    [25, np.nan, 30, 22, np.nan, 41, 28, np.nan, 35, 50],\n#     'salario': [30000, 45000, np.nan, 28000, 50000, np.nan, 33000, 42000, np.nan, 80000],\n#     'ciudad':  ['Madrid', 'Barcelona', np.nan, 'Madrid', 'Valencia', 'Madrid', np.nan, 'Barcelona', 'Sevilla', 'Madrid']\n# })\n#\n# # 1) Inspeccion inicial\n# print('NaN por columna antes:')\n# print(df.isnull().sum())\n#\n# # 2) Edad con mediana (robusta a outliers)\n# mediana_edad = df['edad'].median()\n# df['edad'] = df['edad'].fillna(mediana_edad)\n#\n# # 3) Salario con media (asumimos que esta bien)\n# media_salario = df['salario'].mean()\n# df['salario'] = df['salario'].fillna(media_salario)\n#\n# # 4) Ciudad con la moda (categorica)\n# moda_ciudad = df['ciudad'].mode()[0]   # mode() devuelve una Series\n# df['ciudad'] = df['ciudad'].fillna(moda_ciudad)\n#\n# # 5) Verificacion\n# print('NaN por columna despues:')\n# print(df.isnull().sum())\n# print()\n# print(df)\n"},
]))

# ============ DUPLICADOS ============
plan.append((ID_DUPLICADOS, [
    {"type": "md", "src": teoria(
        "Duplicados: detectar y eliminar filas repetidas",
        """Las filas duplicadas son frecuentes cuando combinas datasets, exportas/importas varias veces o hay errores de captura. Pueden **inflar artificialmente** las metricas y confundir al modelo.

| Metodo | Que hace |
|---|---|
| `df.duplicated()` | Devuelve un bool por fila (True = es duplicado) |
| `df.duplicated().sum()` | Cuantos duplicados hay en total |
| `df.duplicated(subset=['col1','col2'])` | Considera duplicado solo si se repiten esas columnas |
| `df.drop_duplicates()` | Elimina duplicados (se queda con la primera por defecto) |
| `df.drop_duplicates(keep='last')` | Se queda con la ultima |
| `df.drop_duplicates(keep=False)` | Elimina **todas** las apariciones de los duplicados |
| `df.drop_duplicates(subset=['email'])` | Quita filas con el mismo email aunque otras columnas difieran |

#### Casos tipicos

```python
# Caso 1: filas idensticamente identicas
df = df.drop_duplicates()

# Caso 2: misma persona registrada varias veces (mismo email pero distinto timestamp)
df_unicos = df.sort_values('timestamp').drop_duplicates(subset=['email'], keep='last')

# Caso 3: detectar duplicados antes de decidir
print(df[df.duplicated(subset=['email'], keep=False)].sort_values('email'))
```"""
    )},
    {"type": "md", "src": tu_turno(5,
        """Crea este DataFrame con duplicados sutiles:

```python
df = pd.DataFrame({
    'email':    ['ana@x.com', 'pedro@x.com', 'ana@x.com', 'lucia@x.com', 'pedro@x.com', 'mario@x.com'],
    'compras':  [3, 5, 7, 2, 5, 1],
    'fecha':    ['2024-01-01','2024-01-02','2024-03-15','2024-02-10','2024-01-02','2024-04-01']
})
```

1. Cuantas filas son duplicadas exactas? (todas las columnas iguales).
2. Cuantos clientes UNICOS hay (por email)?
3. Quedate con la fila **mas reciente** de cada email (pista: ordena por `fecha` y usa `drop_duplicates(subset=['email'], keep='last')`)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\ndf = pd.DataFrame({\n    'email':    ['ana@x.com', 'pedro@x.com', 'ana@x.com', 'lucia@x.com', 'pedro@x.com', 'mario@x.com'],\n    'compras':  [3, 5, 7, 2, 5, 1],\n    'fecha':    ['2024-01-01','2024-01-02','2024-03-15','2024-02-10','2024-01-02','2024-04-01']\n})\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n# df = pd.DataFrame({\n#     'email':    ['ana@x.com', 'pedro@x.com', 'ana@x.com', 'lucia@x.com', 'pedro@x.com', 'mario@x.com'],\n#     'compras':  [3, 5, 7, 2, 5, 1],\n#     'fecha':    ['2024-01-01','2024-01-02','2024-03-15','2024-02-10','2024-01-02','2024-04-01']\n# })\n#\n# # 1) Duplicados exactos: misma fila completa\n# # ('pedro@x.com', 5, '2024-01-02') aparece dos veces -> 1 duplicado\n# print('Duplicados exactos:', df.duplicated().sum())\n#\n# # 2) Clientes unicos por email\n# print('Clientes unicos:', df['email'].nunique())\n#\n# # 3) Fila mas reciente por email\n# df['fecha'] = pd.to_datetime(df['fecha'])\n# df_unicos = (df.sort_values('fecha')\n#                .drop_duplicates(subset=['email'], keep='last'))\n# print(df_unicos)\n"},
]))

# ============ VALORES CATEGORICOS ============
plan.append((ID_CATEGORICOS, [
    {"type": "md", "src": teoria(
        "Variables categoricas y encoding: pasar texto a numero",
        """Los modelos de Machine Learning trabajan con **numeros**, no con texto. Si tienes columnas como `genero`, `pais`, `nivel_educativo`, necesitas **codificarlas (encoding)**.

#### Tres familias de encoding

##### 1. Label Encoding (etiqueta numerica)

Asigna un numero a cada categoria.

```python
# pandas con .astype('category').cat.codes
df['genero_lab'] = df['genero'].astype('category').cat.codes
# 'F' -> 0, 'M' -> 1, 'Otro' -> 2

# sklearn
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['genero_lab'] = le.fit_transform(df['genero'])
```

**Cuando usarlo:** SOLO si los valores tienen un **orden natural** (XS < S < M < L < XL). Si no lo tienen y los pasas a un modelo lineal, este interpretara que `2 > 1 > 0` y te hara conclusiones falsas.

##### 2. One-Hot Encoding (binarizar)

Crea una columna nueva por cada categoria, con 0/1.

```python
# pandas
df_oh = pd.get_dummies(df, columns=['pais'])
# crea columnas: pais_Espana, pais_Francia, pais_Italia ...

# sklearn
from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder(sparse_output=False)
ohe.fit_transform(df[['pais']])
```

**Cuando usarlo:** **CASI SIEMPRE** para variables categoricas sin orden natural. Es la opcion por defecto.

> Cuidado con la **explosion dimensional**: si tu columna tiene 1000 valores distintos, generaras 1000 columnas. Soluciones: agrupar categorias raras en `'Otros'`, o usar embeddings.

##### 3. Ordinal Encoding (orden conocido)

Asignas numeros respetando un **orden definido por ti**.

```python
from sklearn.preprocessing import OrdinalEncoder
oe = OrdinalEncoder(categories=[['XS','S','M','L','XL']])
df['talla_ord'] = oe.fit_transform(df[['talla']])
# XS->0, S->1, M->2, L->3, XL->4
```

**Cuando usarlo:** cuando hay un **orden semantico real** que el modelo deberia aprovechar.

#### Tabla resumen: que encoding usar?

| Tipo de variable | Encoding recomendado |
|---|---|
| Sin orden, pocas categorias (<10) | **One-Hot** |
| Sin orden, muchas categorias | One-Hot + agrupar raras / Target encoding |
| Con orden natural | **Ordinal** (con categorias explicitas) |
| Binaria (`Si`/`No`) | Label (mapeada a 0/1) |
| Para arboles (Random Forest, XGBoost) | Label suele bastar (los arboles no asumen orden) |
| Para modelos lineales y redes | One-Hot u Ordinal segun corresponda |"""
    )},
    {"type": "md", "src": teoria(
        "Normalizacion y escalado: poner las columnas en la misma escala",
        """Cuando tus columnas numericas tienen escalas muy distintas (edad [0,100] vs salario [0,200_000]), los algoritmos basados en **distancias** (KNN, K-Means, SVM, redes neuronales) **se desequilibran**: el salario domina por completo y la edad pasa a ser irrelevante.

#### Dos tecnicas principales

##### Min-Max Scaling (normalizacion al [0, 1])

Formula: `x_new = (x - min) / (max - min)`

```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df_norm = scaler.fit_transform(df[['edad','salario']])

# Equivalente con pandas:
df['edad_norm'] = (df['edad'] - df['edad'].min()) / (df['edad'].max() - df['edad'].min())
```

**Pros:** todo en [0,1], facil de interpretar.
**Contras:** muy sensible a outliers (un valor extremo aplasta los demas).

##### Z-score / Standard Scaling (estandarizacion)

Formula: `x_new = (x - mean) / std`

Resultado: media 0, desviacion 1. Permite valores fuera de [0,1].

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df_std = scaler.fit_transform(df[['edad','salario']])

# Equivalente con pandas:
df['edad_z'] = (df['edad'] - df['edad'].mean()) / df['edad'].std()
```

**Pros:** menos sensible a outliers, asume distribucion aproximadamente normal.
**Contras:** los valores no estan acotados.

##### Robust Scaling (alternativa a outliers)

Usa **mediana e IQR** en vez de media y std. Util cuando hay muchos outliers.

```python
from sklearn.preprocessing import RobustScaler
```

#### Tabla de decision: que escalado usar?

| Situacion | Escalado |
|---|---|
| Variables sin outliers, distribucion aproximadamente normal | **StandardScaler** (z-score) |
| Variables acotadas conocidas, redes neuronales (entradas en [0,1]) | **MinMaxScaler** |
| Muchos outliers | **RobustScaler** |
| Solo arboles (Random Forest, XGBoost) | **Ningun escalado** -> los arboles son invariantes a escala |
| Imagenes (pixeles 0-255) | Dividir entre 255 -> [0,1] |

#### Atencion: train vs test

```python
# CORRECTO
scaler.fit(X_train)               # SOLO se ajusta con train
X_train_s = scaler.transform(X_train)
X_test_s  = scaler.transform(X_test)   # con los parametros de TRAIN

# INCORRECTO (data leakage)
scaler.fit(X_total)               # NUNCA mires el test al ajustar
```"""
    )},
    {"type": "md", "src": tu_turno(6,
        """Trabaja sobre este DataFrame mixto que combina los problemas de encoding y escalado:

```python
import pandas as pd
df = pd.DataFrame({
    'edad':    [25, 32, 45, 22, 60, 35, 28],
    'salario': [30000, 45000, 80000, 25000, 120000, 55000, 32000],
    'pais':    ['Espana', 'Francia', 'Espana', 'Italia', 'Francia', 'Espana', 'Italia'],
    'talla':   ['M', 'L', 'XL', 'S', 'XL', 'M', 'L']
})
```

1. Aplica **One-Hot Encoding** a `pais` con `pd.get_dummies`. Cuantas columnas nuevas aparecen?
2. Aplica **Ordinal Encoding** a `talla` con el orden `['S','M','L','XL']`. Pista: usa un dict y `.map(...)`.
3. Aplica **Min-Max scaling manual** a `edad` para que quede en `[0, 1]`.
4. Aplica **Z-score manual** a `salario`.
5. Muestra el DataFrame final."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport pandas as pd\ndf = pd.DataFrame({\n    'edad':    [25, 32, 45, 22, 60, 35, 28],\n    'salario': [30000, 45000, 80000, 25000, 120000, 55000, 32000],\n    'pais':    ['Espana', 'Francia', 'Espana', 'Italia', 'Francia', 'Espana', 'Italia'],\n    'talla':   ['M', 'L', 'XL', 'S', 'XL', 'M', 'L']\n})\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n# df = pd.DataFrame({\n#     'edad':    [25, 32, 45, 22, 60, 35, 28],\n#     'salario': [30000, 45000, 80000, 25000, 120000, 55000, 32000],\n#     'pais':    ['Espana', 'Francia', 'Espana', 'Italia', 'Francia', 'Espana', 'Italia'],\n#     'talla':   ['M', 'L', 'XL', 'S', 'XL', 'M', 'L']\n# })\n#\n# # 1) One-Hot Encoding sobre 'pais'\n# # get_dummies crea una columna binaria por cada valor distinto\n# df = pd.get_dummies(df, columns=['pais'])\n# # Aparecen 3 columnas: pais_Espana, pais_Francia, pais_Italia\n#\n# # 2) Ordinal Encoding sobre 'talla' con un orden semantico\n# orden_talla = {'S': 0, 'M': 1, 'L': 2, 'XL': 3}\n# df['talla_ord'] = df['talla'].map(orden_talla)\n#\n# # 3) Min-Max scaling manual de 'edad' -> rango [0, 1]\n# df['edad_minmax'] = (df['edad'] - df['edad'].min()) / (df['edad'].max() - df['edad'].min())\n#\n# # 4) Z-score / Standard scaling manual de 'salario'\n# df['salario_z'] = (df['salario'] - df['salario'].mean()) / df['salario'].std()\n#\n# # 5) Resultado final\n# print(df)\n"},
]))

# ============ DISCRETIZACION ============
plan.append((ID_DISCRETIZAR, [
    {"type": "md", "src": teoria(
        "Discretizacion: convertir numerico en categorico (binning)",
        """A veces te interesa **agrupar** valores numericos en bandas (bins) y tratarlos como categorias. Es lo que hace el `pd.cut` que ves abajo.

#### Por que discretizar?

- **Modelos mas robustos**: a veces, en vez de la edad exacta, lo que importa es 'menor', 'joven', 'adulto', 'mayor'.
- **Visualizacion**: histogramas, agrupaciones por rango.
- **Reglas de negocio**: tarifas por rango de ingresos, descuentos por edad.
- **Tratar outliers** sin perderlos.

#### Dos funciones clave

| Funcion | Como divide |
|---|---|
| `pd.cut(x, bins=...)` | Por **rangos de igual ancho** (define los limites) |
| `pd.qcut(x, q=...)` | Por **cuantiles** (cada bin tiene aprox el mismo numero de observaciones) |

#### Ejemplo

```python
edades = [16, 25, 18, 71, 44, 100, 12]

# cut: limites explicitos
bins = [0, 18, 35, 65, 99, np.inf]
etiquetas = ['Menor', 'Joven', 'Adulto', 'Mayor', 'Anciano']
pd.cut(edades, bins, labels=etiquetas)

# qcut: 3 grupos del mismo tamano (terciles)
pd.qcut(edades, q=3, labels=['bajo','medio','alto'])
```

#### Cuando usar cada uno?

| Necesitas... | Usa |
|---|---|
| Limites con sentido de negocio (ej: edad legal, percentiles educativos) | **`cut`** con bins definidos |
| Bins equiprobables (mismo numero de observaciones por bin) | **`qcut`** |
| Distribucion uniforme entre min y max | **`cut`** con `bins=N` (entero) |"""
    )},
    {"type": "md", "src": tu_turno(7,
        """Tienes esta serie de salarios:

```python
import pandas as pd
salarios = pd.Series([18000, 22000, 25000, 28000, 32000, 38000, 45000, 55000, 70000, 95000, 150000])
```

1. Usa `pd.cut` con bins explicitos `[0, 25000, 40000, 70000, np.inf]` y etiquetas `['Bajo','Medio','Alto','Muy alto']`. Imprime cuantos hay en cada categoria con `value_counts`.
2. Usa `pd.qcut` con `q=4` y etiquetas `['Q1','Q2','Q3','Q4']` (cuartiles). Comprueba que en cada cuartil hay aprox el mismo numero de personas.
3. Que diferencia ves entre los dos enfoques?"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport numpy as np\nimport pandas as pd\nsalarios = pd.Series([18000, 22000, 25000, 28000, 32000, 38000, 45000, 55000, 70000, 95000, 150000])\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# import pandas as pd\n# salarios = pd.Series([18000, 22000, 25000, 28000, 32000, 38000, 45000, 55000, 70000, 95000, 150000])\n#\n# # 1) cut: rangos definidos por nosotros (igual ancho del bin)\n# bins = [0, 25000, 40000, 70000, np.inf]\n# etiquetas = ['Bajo', 'Medio', 'Alto', 'Muy alto']\n# cat_cut = pd.cut(salarios, bins=bins, labels=etiquetas)\n# print('cut (rangos por valor):')\n# print(cat_cut.value_counts())\n# # Resultado: bins desiguales en numero de observaciones\n#\n# # 2) qcut: por cuantiles (mismo numero por bin, distinto rango)\n# cat_qcut = pd.qcut(salarios, q=4, labels=['Q1','Q2','Q3','Q4'])\n# print('qcut (cuartiles):')\n# print(cat_qcut.value_counts())\n# # Resultado: aprox el mismo numero por bin (3, 3, 3, 2 con 11 datos)\n#\n# # 3) Diferencia:\n# # - cut respeta los limites de negocio pero algunos bins pueden quedar vacios\n# #   o muy poblados.\n# # - qcut equilibra el numero de observaciones, util para crear\n# #   variables categoricas con poder predictivo equilibrado.\n"},
]))


enhance(NB, plan)
print("Done.")

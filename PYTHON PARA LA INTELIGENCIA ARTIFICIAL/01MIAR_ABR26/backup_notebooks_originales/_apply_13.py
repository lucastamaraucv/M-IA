"""Aplica mejoras al notebook 13_Generators con bloques de colores y teoria detallada."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, solucion_md, dato, aviso

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_13_Generators.ipynb"

import json
nb = json.load(open(NB, encoding="utf-8"))

def find_id(text_fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if text_fragment in src:
            return c["id"]
    return None

# IDs reales del notebook 13
ID_TITULO         = nb["cells"][0]["id"]                       # img viu_logo
ID_GEN_INTRO      = find_id("## Generadores en Python")         # cell 1
ID_LISTA_FUN      = find_id("# Devuelve lista")                 # cell 2 (squares_fun lista)
ID_GEN_YIELD      = find_id("# Usar generador")                 # cell 4 (yield) primera ocurrencia
ID_NEXT           = find_id("- Next (envia None")               # cell 6
ID_SEND           = find_id("- Send (se pueden enviar")          # cell 10
ID_GEXPR          = find_id("## Expresiones Generadoras")        # cell 15
ID_GEXPR_PAREN    = find_id("- Generator Expressions")           # cell 17
ID_PIPELINES      = find_id("## Pipelines de Datos con Generadores")   # cell 20
ID_TRAIN_GEN      = find_id("## Generadores para entrenar modelos")     # cell 32
ID_KERAS_IMG      = find_id("## Generadores de datos de im")            # cell 43
ID_AUGMENT        = find_id("### Augmentations")                # cell 62
ID_CUSTOM         = find_id("## Generadores de datos custom con Keras")  # cell 70

plan = []

# ======== INTRO al notebook ========
plan.append((ID_TITULO, [
    {"type": "md", "src": teoria(
        "Como leer este notebook (version mejorada)",
        """Este notebook fue **enriquecido** con celdas adicionales de teoria y ejercicios. Vas a encontrar tres tipos de bloques de colores:

<div style="background-color:#e7f5ff;border-left:6px solid #1c7ed6;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AZUL = TEORIA</b></div> -> explicacion en palabras simples antes de cada concepto.

<div style="background-color:#fff9db;border-left:6px solid #f59f00;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AMARILLO = TU TURNO</b></div> -> el ejercicio que TU debes resolver. Hay una celda vacia debajo donde escribes el codigo.

<div style="background-color:#ebfbee;border-left:6px solid #2f9e44;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>VERDE = SOLUCION</b></div> -> codigo de referencia comentado por si te trabas.

> **Promesa importante**: el codigo y la teoria del profesor original no se han tocado. Solo se han ANADIDO bloques."""
    )},
]))

# ======== INTRO GENERADORES ========
plan.append((ID_GEN_INTRO, [
    {"type": "md", "src": teoria(
        "Iterables, iteradores y generadores: la jerarquia",
        """Antes de entender un **generador** hay que dominar tres conceptos que se confunden mucho.

#### 1. Iterable

Un objeto **iterable** es **algo por lo que se puede iterar** (recorrer con `for`). Implementa el metodo magico `__iter__()` que devuelve un iterador.

Ejemplos: `list`, `tuple`, `str`, `dict`, `set`, `range`, los ficheros abiertos, los generadores.

```python
mi_lista = [1, 2, 3]
for x in mi_lista:    # funciona porque la lista es iterable
    print(x)
```

#### 2. Iterador (iterator)

Un **iterador** es el objeto que produce los valores **uno a uno** cuando le llamas `next(...)`. Implementa DOS metodos magicos:

- `__iter__()` -> se devuelve a si mismo.
- `__next__()` -> devuelve el siguiente valor o lanza `StopIteration`.

```python
mi_lista = [10, 20, 30]
it = iter(mi_lista)        # iter() llama a __iter__() y crea el iterador
print(next(it))             # 10
print(next(it))             # 20
print(next(it))             # 30
print(next(it))             # StopIteration -> error
```

| Concepto | Que es | Que metodos tiene |
|---|---|---|
| **Iterable** | algo recorrible | `__iter__` |
| **Iterator** | algo que da valores uno a uno | `__iter__` y `__next__` |

> Una lista es iterable PERO NO es iterador: necesitas pasarle por `iter(...)` primero. En cambio, un generador es **las dos cosas a la vez**.

#### 3. Generador (generator)

Un **generador** es una **forma facil de crear un iterador** sin tener que escribir clases con `__iter__` y `__next__` a mano.

Hay dos formas de crearlo:

- **Funcion generadora**: una funcion que usa `yield` en lugar de `return`.
- **Generator expression**: como una list comprehension pero con `( )` en lugar de `[ ]`.

#### Por que son utiles los generadores en IA?

| Problema | Solucion con generador |
|---|---|
| Un dataset no cabe en RAM (millones de imagenes, GB de texto) | Lees por **lotes** sin cargar todo |
| Procesar un fichero gigante linea a linea | Generator pipeline (lo veras abajo) |
| Data augmentation aleatoria | El generador produce variaciones infinitas |
| Streaming de datos en tiempo real | El generador NUNCA termina |

Keras y PyTorch dependen MUCHO de generadores para alimentar redes neuronales con datos que no caben en memoria."""
    )},
    {"type": "md", "src": dato(
        """**Evaluacion perezosa (lazy evaluation)**: el principio que hace especiales a los generadores.

Una lista calcula **TODOS** los valores y los guarda en memoria al instante.
Un generador NO calcula nada hasta que le pides el siguiente valor con `next(...)` o lo recorres con `for`.

```python
# 'Comprehension' INMEDIATA: ocupa RAM ahora mismo
cuadrados = [x**2 for x in range(1_000_000_000)]   # CRASH (8 GB)

# Generador PEREZOSO: solo calcula bajo demanda
cuadrados = (x**2 for x in range(1_000_000_000))   # OK, casi 0 bytes
```

El generador solo recuerda **donde se quedo**. Es como un libro con un marcapaginas: no lees las paginas hasta que las pides."""
    )},
]))

# ======== LISTA TRADICIONAL VS GENERADOR ========
plan.append((ID_LISTA_FUN, [
    {"type": "md", "src": teoria(
        "Lista vs generador: comparativa real",
        """Aqui ves la **forma clasica** (devolver una lista). Compara despues con el generador (siguiente celda).

| Aspecto | `squares_fun(50000)` (lista) | `squares(50000)` (generador) |
|---|---|---|
| Memoria al crearlo | reserva 50000 enteros | reserva casi nada |
| Tiempo de creacion | calcula los 50000 | instantaneo |
| Reutilizable? | si, recorrible varias veces | **NO**, una sola pasada |
| Acceso por indice | si: `lista[100]` | NO: `gen[100]` -> error |
| len() | si | NO |
| Util para datos grandes | NO | SI |

#### Cuando usar uno u otro?

- **Lista**: si vas a recorrer los datos varias veces, si necesitas indexacion, si caben en RAM y son rapidos de calcular.
- **Generador**: si los datos son enormes, si solo los recorres una vez, si quieres componer un pipeline, si los produces de forma incremental (sensores, web scraping, etc.)."""
    )},
]))

# ======== GENERADOR CON YIELD ========
plan.append((ID_GEN_YIELD, [
    {"type": "md", "src": teoria(
        "<code>yield</code>: la palabra magica que crea un generador",
        """Cualquier funcion que contenga `yield` (en cualquier parte del cuerpo) **deja de ser una funcion normal** y pasa a ser una **funcion generadora**.

```python
def squares(n):
    for i in range(n):
        yield i ** 2     # <- yield, no return
```

#### Que pasa cuando llamas a `squares(5)`?

**NO ejecuta el cuerpo**. Solo devuelve un objeto **generator**:

```python
gen = squares(5)
print(gen)               # <generator object squares at 0x...>
print(type(gen))         # <class 'generator'>
```

#### Cuando se ejecuta el cuerpo?

Solo cuando llamas a `next(gen)` (o iteras con `for`):

1. Primer `next(gen)`: ejecuta hasta el primer `yield`, devuelve el valor y **PAUSA** la funcion exactamente ahi.
2. Segundo `next(gen)`: **REANUDA** desde el `yield` anterior y vuelve a parar en el siguiente.
3. Cuando la funcion termina (sin mas `yield`): lanza `StopIteration`.

```
[next] -> ejecuta -> yield 0  (PAUSA)
[next] -> reanuda -> yield 1  (PAUSA)
[next] -> reanuda -> yield 4  (PAUSA)
...
[next] -> reanuda -> fin        -> StopIteration
```

> **Lo magico**: el generador **conserva su estado** (variables locales, posicion del bucle) entre llamadas. Es como si la funcion durmiera entre yields y se despertara con cada `next()`.

#### Diferencias con `return`

| `return` | `yield` |
|---|---|
| Termina la funcion | **Pausa** la funcion |
| Devuelve UN valor y se acabo | Puede devolver muchos, uno por llamada |
| El estado local se pierde | El estado local se preserva |"""
    )},
    {"type": "md", "src": tu_turno(1,
        """Define una **funcion generadora** llamada `pares_hasta(n)` que produzca todos los **numeros pares desde 0 hasta n** (incluido si es par).

Despues:
1. Crea el generador `g = pares_hasta(10)`.
2. Comprueba su tipo con `type(g)`.
3. Recorrelo con un `for` e imprime cada valor.

> Resultado esperado: 0, 2, 4, 6, 8, 10."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def pares_hasta(n):\n#     # bucle desde 0 hasta n incluido\n#     for i in range(n + 1):\n#         # solo emite los que son pares\n#         if i % 2 == 0:\n#             yield i   # cada yield pausa la funcion\n#\n# # Llamar a la funcion crea el generador, NO ejecuta el cuerpo\n# g = pares_hasta(10)\n# print(type(g))   # <class 'generator'>\n#\n# # Iterar consume los valores uno a uno\n# for x in g:\n#     print(x)\n"},
]))

# ======== NEXT ========
plan.append((ID_NEXT, [
    {"type": "md", "src": teoria(
        "<code>next()</code>: avanzar un paso en el generador",
        """`next(gen)` le dice al generador: **dame el siguiente valor**.

```python
def basico():
    print('A')
    yield 1
    print('B')
    yield 2
    print('C')
    yield 3

g = basico()         # NO imprime nada todavia (no se ha ejecutado el cuerpo)
print(next(g))       # imprime 'A' y luego 1
print(next(g))       # imprime 'B' y luego 2
print(next(g))       # imprime 'C' y luego 3
print(next(g))       # StopIteration -> excepcion
```

#### Patron tipico: `next()` con valor por defecto

Para evitar la excepcion `StopIteration` cuando se acaba el generador:

```python
valor = next(gen, None)        # devuelve None en lugar de fallar
valor = next(gen, 'sin datos')   # mensaje por defecto
```

#### Cuando usar `next()` directamente?

- Para **inspeccionar el primer elemento** sin recorrerlo todo.
- Para **avanzar manualmente** el generador (saltar la cabecera de un CSV, por ejemplo).
- En tests para verificar la salida del generador paso a paso.

En el codigo de arriba veras que cada `next(gen)` ejecuta el codigo hasta el siguiente `yield` y se queda esperando."""
    )},
    {"type": "md", "src": tu_turno(2,
        """Define un generador `cuenta_atras(n)` que emita los numeros de `n` hasta `0` (incluidos).

Despues:
1. Crea `g = cuenta_atras(3)`.
2. Llama a `next(g)` cuatro veces e imprime cada resultado. La cuarta llamada deberia funcionar todavia (devuelve 0).
3. Llama una **quinta** vez con valor por defecto: `next(g, 'fin')`. Imprimelo."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def cuenta_atras(n):\n#     # bucle de n hasta 0, decrementando 1\n#     while n >= 0:\n#         yield n          # entrega n y pausa\n#         n -= 1           # al reanudar, decrementa\n#\n# g = cuenta_atras(3)        # crea el generador (no ejecuta nada todavia)\n# print(next(g))             # 3\n# print(next(g))             # 2\n# print(next(g))             # 1\n# print(next(g))             # 0\n# print(next(g, 'fin'))      # 'fin' (con default evita StopIteration)\n"},
]))

# ======== SEND ========
plan.append((ID_SEND, [
    {"type": "md", "src": teoria(
        "<code>.send(valor)</code>: enviar datos AL generador",
        """`yield` no solo **devuelve** un valor, tambien puede **recibir** un valor del exterior.

```python
def gen():
    x = 0
    for i in range(10):
        x = yield i * x          # yield emite i*x Y recibe el valor que llegue por .send()
        print(f'recibi {x}')
```

#### Como funciona

1. La primera vez tienes que hacer `next(g)` (no `send`) para **arrancar** el generador.
2. Despues, `g.send(valor)` se comporta como `next()` PERO ademas: dentro del generador, la **expresion `yield`** se evalua al `valor` enviado.

```python
g = gen()
next(g)         # 0   (arranca, x todavia es 0, i=0, emite i*x = 0)
g.send(2)       # ahora yield = 2 -> x = 2; siguiente iteracion: i=1, emite 1*2 = 2
g.send(10)      # yield = 10 -> x = 10; i=2, emite 2*10 = 20
```

#### Para que sirve esto?

- **Corutinas** (programacion concurrente cooperativa).
- **Maquinas de estados** que reciben eventos.
- En `asyncio` y librerias asincronas, `send` es la base.

> Es un tema avanzado. En el dia a dia de IA usaras `yield` simple muchisimo mas que `.send()`."""
    )},
]))

# ======== GENERATOR EXPRESSIONS ========
plan.append((ID_GEXPR, [
    {"type": "md", "src": teoria(
        "List comprehension vs Generator expression",
        """La sintaxis es **casi identica**. La unica diferencia visible son los **parentesis**:

```python
[ x**2 for x in range(5) ]    # LIST comprehension  -> crea una lista [0,1,4,9,16]
( x**2 for x in range(5) )    # GENERATOR expression -> crea un generador perezoso
```

#### Comparativa

| Aspecto | `[x for x in ...]` lista | `(x for x in ...)` generador |
|---|---|---|
| Sintaxis | corchetes `[ ]` | parentesis `( )` |
| Resultado | `list` | `generator` |
| Memoria | toda en RAM al crear | casi 0 bytes |
| Velocidad de creacion | calcula todo ya | instantanea |
| Reutilizable | si | NO, un solo uso |
| Indexable | si: `lista[5]` | no |
| Tiene `len()` | si | no |
| `print()` muestra | los elementos | `<generator object ...>` |

#### Truco: parentesis se pueden omitir como argumento

Cuando el generator expression es el **unico argumento** a una funcion, no hace falta escribir los parentesis dobles:

```python
sum(x**2 for x in range(100))     # bonito
sum((x**2 for x in range(100)))  # tambien valido pero sobra un par
```

#### Casos perfectos para generator expression

```python
# Sumar valores que no caben en lista
total = sum(linea.count(',') for linea in open('huge.csv'))

# Encontrar primero que cumple condicion
primer_par = next(x for x in numeros if x % 2 == 0)

# Pipeline encadenado (lo veras abajo en el ejemplo del Titanic)
limpios   = (linea.strip() for linea in fichero)
campos    = (linea.split(',') for linea in limpios)
filtrados = (c for c in campos if c[0] == 'OK')
```"""
    )},
]))

plan.append((ID_GEXPR_PAREN, [
    {"type": "md", "src": tu_turno(3,
        """Tienes esta lista:

```python
numeros = list(range(1, 11))   # [1, 2, ..., 10]
```

1. Crea una **list comprehension** `cuad_lista` con los cuadrados de cada numero. Imprime su tipo y la lista entera.
2. Crea una **generator expression** `cuad_gen` con los cuadrados. Imprime su tipo y el resultado de `print(cuad_gen)` (vas a ver `<generator object ...>`).
3. Usa `sum(...)` con un generator expression directamente para calcular la **suma de los cuadrados** de los numeros pares de la lista. (Ojo, los pares: 2, 4, 6, 8, 10).

> Resultado esperado: 4 + 16 + 36 + 64 + 100 = 220."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nnumeros = list(range(1, 11))\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# numeros = list(range(1, 11))\n#\n# # 1) List comprehension: crea TODA la lista en memoria\n# cuad_lista = [x**2 for x in numeros]\n# print(type(cuad_lista))   # <class 'list'>\n# print(cuad_lista)         # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]\n#\n# # 2) Generator expression: solo describe COMO calcular, no calcula\n# cuad_gen = (x**2 for x in numeros)\n# print(type(cuad_gen))     # <class 'generator'>\n# print(cuad_gen)           # <generator object ...>\n#\n# # 3) Suma de cuadrados de pares con generator expression\n# # No hace falta corchetes adentro: sum() acepta el generator directo\n# total = sum(x**2 for x in numeros if x % 2 == 0)\n# print(total)              # 220\n"},
]))

# ======== PIPELINES ========
plan.append((ID_PIPELINES, [
    {"type": "md", "src": teoria(
        "Pipeline de generadores: encadenar transformaciones",
        """Un **pipeline** es una serie de generadores donde **cada uno consume** los valores que produce el anterior. Ningun valor se almacena entero: fluye **paso a paso** por la cadena.

```
fichero -> generador1 (leer linea) -> generador2 (split) -> generador3 (filtrar) -> sum()
```

#### Por que esto es genial

| Ventaja | Detalle |
|---|---|
| **Memoria casi nula** | Solo una linea viva a la vez, da igual si el fichero tiene 100 GB. |
| **Composable** | Cada paso es una linea independiente, facil de leer y testear. |
| **Lazy** | Si solo te interesan las primeras 10 filas, el pipeline solo procesa esas. |
| **Reutilizable** | Cambiar un paso no afecta a los otros. |

#### Patron general

```python
# Paso 1: producir lineas crudas
lineas = (l for l in open('fichero.csv'))

# Paso 2: limpiar y dividir por columnas
campos = (l.rstrip().split(',') for l in lineas)

# Paso 3: tirar la cabecera
cabecera = next(campos)

# Paso 4: pasar a diccionarios
filas = (dict(zip(cabecera, c)) for c in campos)

# Paso 5: filtrar
adultos = (f for f in filas if int(f['edad']) >= 18)

# Paso 6: consumir
total = sum(1 for _ in adultos)
print(total)
```

> **No olvides cerrar el fichero** despues. Mejor todavia: usa `with open(...) as f:` y haz el pipeline dentro del bloque.

#### En IA esto es CRUCIAL

Los datasets de produccion **no caben en RAM**. Los generadores de Keras (`flow_from_directory`, `Sequence`) son exactamente este patron: producen lotes (`batches`) sin cargar nunca todo en memoria."""
    )},
    {"type": "md", "src": dato(
        """**El pipeline del Titanic que vas a ver:**

1. `lines = (line for line in file_handler)` -> producir lineas.
2. `list_line = (s.rstrip().split(',') for s in lines)` -> limpiar y dividir.
3. `cols = next(list_line)` -> extraer la cabecera (consume una fila).
4. `passengers = (dict(zip(cols, data)) for data in list_line)` -> pasar a dicts.
5. `passenger_in_class3_survived = (int(p['Survived']) for p in passengers if p['Pclass']=='3')` -> filtrar y proyectar.
6. `sum(passenger_in_class3_survived)` -> contar supervivientes.

Solo en el paso 6 se ejecuta TODO el pipeline, una linea a la vez. Lee el codigo con esta vision."""
    )},
    {"type": "md", "src": tu_turno(4,
        """Sin abrir ningun fichero, vamos a probar un mini pipeline en memoria con esta lista de strings:

```python
datos = [
    'manzana,5',
    'pera,3',
    'uva,12',
    'kiwi,7',
    'mango,2'
]
```

Construye un pipeline de generadores que:

1. `divididos`: por cada linea, devuelva una lista `[fruta, cantidad_str]` (usa `split(',')`).
2. `parseados`: por cada elemento divido, devuelva una **tupla** `(fruta, int(cantidad))`.
3. `mayores`: filtre solo las frutas con cantidad **mayor o igual a 5**.
4. Imprime el **total de frutas** sumando con `sum(...)` sobre el generador `mayores` proyectado a la cantidad.

> Resultado esperado: 5 + 12 + 7 = 24."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\ndatos = [\n    'manzana,5',\n    'pera,3',\n    'uva,12',\n    'kiwi,7',\n    'mango,2'\n]\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# datos = ['manzana,5', 'pera,3', 'uva,12', 'kiwi,7', 'mango,2']\n#\n# # Paso 1: dividir cada string por la coma -> ['manzana', '5'], ...\n# divididos = (linea.split(',') for linea in datos)\n#\n# # Paso 2: convertir cantidad a int -> ('manzana', 5), ...\n# parseados = ((fruta, int(cantidad)) for fruta, cantidad in divididos)\n#\n# # Paso 3: filtrar solo las que tienen cantidad >= 5\n# mayores = ((fruta, cantidad) for fruta, cantidad in parseados if cantidad >= 5)\n#\n# # Paso 4: sumar las cantidades de las que pasan el filtro\n# # NOTA: la suma se calcula recorriendo todo el pipeline UNA vez\n# total = sum(cantidad for _, cantidad in mayores)\n# print(total)   # 24\n"},
]))

# ======== TRAIN MODEL ========
plan.append((ID_TRAIN_GEN, [
    {"type": "md", "src": teoria(
        "Generadores para entrenar modelos: por que importan",
        """Cuando trabajas con datasets reales (millones de filas, GB o TB de imagenes) **no puedes cargar todo en RAM**. Esta es la situacion mas frecuente en proyectos de IA serios.

#### El truco: cargar por LOTES (batches)

Un **batch** es un subconjunto pequeno de datos (16, 32, 64 ejemplos). El modelo:

1. Lee un batch del disco.
2. Calcula la perdida.
3. Actualiza pesos.
4. Olvida ese batch y carga el siguiente.

Asi en cualquier instante solo hay 1 batch en memoria, no el dataset entero.

#### Quien suministra los batches?

Un **generador**. Por eso Keras acepta directamente un generador en `model.fit(generator, ...)` en lugar de un array NumPy.

```python
def generate_arrays_from_file(path, batchsize):
    while True:                          # bucle infinito (Keras lo controla)
        with open(path) as f:
            inputs, targets = [], []
            for linea in f:
                x, y = linea.strip().split(',')
                inputs.append([float(x)])
                targets.append([float(y)])
                if len(inputs) == batchsize:
                    yield np.array(inputs), np.array(targets)   # entrega un batch
                    inputs, targets = [], []                     # reinicia
```

#### Parametros importantes en `model.fit(...)`

| Parametro | Que es |
|---|---|
| `steps_per_epoch` | cuantos batches forman una epoca (= total / batch_size) |
| `epochs` | cuantas pasadas completas al dataset |
| `batch_size` | cuantos ejemplos por batch (lo controla el generador) |

#### Ojo: el generador debe ser INFINITO

A diferencia de los pipelines de antes, este generador NO termina (`while True`). Keras se encarga de pararlo despues de `steps_per_epoch * epochs` batches."""
    )},
]))

# ======== KERAS IMG ========
plan.append((ID_KERAS_IMG, [
    {"type": "md", "src": teoria(
        "ImageDataGenerator: generadores de imagenes en Keras",
        """Para datasets de **imagenes** Keras incluye `ImageDataGenerator`, una clase que automaticamente:

1. Lee imagenes desde disco.
2. Las redimensiona.
3. Las normaliza (divide por 255 para llevar a [0, 1]).
4. Aplica **augmentations** (rotaciones, flips, zooms aleatorios).
5. Las entrega en batches al modelo.

#### Tres formas principales de alimentarlo

| Metodo | De donde lee | Cuando usar |
|---|---|---|
| `.flow_from_directory(carpeta)` | Carpeta organizada por clases (un subdir por clase) | Lo mas comun para clasificacion de imagenes |
| `.flow(x, y)` | Arrays NumPy en memoria | Datasets pequenos como MNIST |
| `.flow_from_dataframe(df, ...)` | DataFrame con paths y labels | Cuando tienes un CSV con metadatos |

#### Estructura tipica de carpeta para `flow_from_directory`

```
res/images/
    perro/
        foto1.jpg
        foto2.jpg
    gato/
        foto3.jpg
        foto4.jpg
```

`generator.class_indices` te devuelve `{'gato': 0, 'perro': 1}` (orden alfabetico).

#### Diferencia clave con un generador 'a mano'

`ImageDataGenerator` ya implementa `__iter__` y `__next__`, asi que se comporta como cualquier iterador Python. **Pero tambien es infinito**, justo como necesita Keras."""
    )},
]))

# ======== AUGMENTATIONS ========
plan.append((ID_AUGMENT, [
    {"type": "md", "src": teoria(
        "Data Augmentation: por que es decisivo en vision",
        """**Augmentation** = generar **variaciones aleatorias** de cada imagen sobre la marcha.

#### El problema

Si tu dataset tiene 1000 fotos de gatos, el modelo puede memorizarlas. Pero si **cada epoca** ve esas mismas 1000 fotos un poco rotadas, recortadas o invertidas... aprende a reconocer **gatos** en general, no esas 1000 fotos en particular.

| Sin augmentation | Con augmentation |
|---|---|
| Modelo ve 1000 fotos | Modelo ve 1000 fotos x 50 epocas = 50000 variaciones distintas |
| Tiende a sobreajustar (overfitting) | Generaliza mejor a fotos nuevas |
| Necesitas mas datos reales | Aprovechas mas los pocos que tienes |

#### Transformaciones tipicas

| Parametro | Que hace |
|---|---|
| `rotation_range=45` | rota +/- 45 grados |
| `width_shift_range=0.2` | desplaza horizontal hasta 20% |
| `height_shift_range=0.2` | desplaza vertical |
| `zoom_range=0.3` | zoom in/out |
| `horizontal_flip=True` | espeja izq-dcha |
| `vertical_flip=True` | espeja arriba-abajo |
| `brightness_range=(0.5, 1.5)` | varia brillo |
| `shear_range=0.2` | deformacion en angulo |
| `rescale=1./255` | normaliza a [0, 1] |

#### Cuidado: no toda transformacion es valida

- **`vertical_flip=True` en perros / gatos**: los animales no se ven volteados al reves en la realidad. Puede confundir al modelo.
- **`vertical_flip=True` en imagenes de satelite**: si funciona, no hay un 'arriba' fijo.
- **Rotacion grande en digitos MNIST**: un 6 rotado 180 grados parece un 9. Cuidado con cambiar la clase real."""
    )},
    {"type": "md", "src": tu_turno(5,
        """**Reflexion (sin codigo).** Imagina que entrenas un clasificador de **placas de matricula**. Para cada uno de estos augmentations decide si SI o NO los aplicarias y por que:

1. `horizontal_flip=True`
2. `rotation_range=10`
3. `rotation_range=180`
4. `brightness_range=(0.5, 1.5)`
5. `vertical_flip=True`
6. `zoom_range=0.1`

Escribe la respuesta como comentarios en la celda."""
    )},
    {"type": "code", "src": "# Escribe aqui tu razonamiento como comentarios:\n\n# 1) horizontal_flip=True ->\n# 2) rotation_range=10 ->\n# 3) rotation_range=180 ->\n# 4) brightness_range=(0.5, 1.5) ->\n# 5) vertical_flip=True ->\n# 6) zoom_range=0.1 ->\n"},
    {"type": "code", "src": "# === Solucion sugerida (criterio razonado) ===\n#\n# 1) horizontal_flip=True -> NO. Una matricula espejada cambia las letras\n#    (B se convierte en algo distinto). El modelo aprenderia patrones falsos.\n#\n# 2) rotation_range=10 -> SI. En la realidad las fotos pueden estar un\n#    poco torcidas (camara mal alineada, coche en pendiente). +/- 10 grados\n#    es razonable y la matricula sigue legible.\n#\n# 3) rotation_range=180 -> NO. Una matricula del reves no existe en la realidad\n#    y el modelo veria datos imposibles. Solo confunde.\n#\n# 4) brightness_range=(0.5, 1.5) -> SI. Es excelente: simula condiciones\n#    de luz reales (dia nublado, sombra, sol directo).\n#\n# 5) vertical_flip=True -> NO. Lo mismo que la rotacion 180. Una matricula\n#    boca abajo no es algo realista.\n#\n# 6) zoom_range=0.1 -> SI. Las matriculas se ven a distintas distancias en\n#    fotos reales. Un zoom moderado ayuda a generalizar.\n#\n# REGLA GENERAL: solo aplica augmentations que generen imagenes que\n# realmente podrian aparecer en produccion.\n"},
]))

# ======== CUSTOM ========
plan.append((ID_CUSTOM, [
    {"type": "md", "src": teoria(
        "Generador custom: heredar de <code>tf.keras.utils.Sequence</code>",
        """Cuando los `ImageDataGenerator` no son suficientes (datos no son imagenes, formato raro, augmentations especiales) puedes crear tu **propio generador** heredando de `Sequence`.

#### Por que Sequence y no un generador normal con yield?

| Ventaja de `Sequence` | Detalle |
|---|---|
| **Multiprocessing seguro** | Keras puede paralelizar varios workers leyendo datos. |
| **Conoce su tamano** | Implementas `__len__()` y Keras sabe cuantos batches hay. |
| **Indexable** | `gen[i]` te da el batch i, en cualquier orden. |
| **Hook de fin de epoca** | Sobrescribes `on_epoch_end()` para barajar, recargar, etc. |

#### Metodos que DEBES implementar

```python
import tensorflow as tf
import numpy as np

class MiGen(tf.keras.utils.Sequence):

    def __init__(self, data, batch_size):
        self.data = data
        self.batch_size = batch_size

    def __len__(self):
        # Cuantos batches caben en una epoca
        return len(self.data) // self.batch_size

    def __getitem__(self, idx):
        # Devuelve el batch numero idx como (X, y)
        inicio = idx * self.batch_size
        fin    = inicio + self.batch_size
        batch  = self.data[inicio:fin]
        X = np.array([item['x'] for item in batch])
        y = np.array([item['y'] for item in batch])
        return X, y

    def on_epoch_end(self):
        # Se llama al acabar cada epoca: util para barajar
        np.random.shuffle(self.data)
```

#### Cuando usar Sequence vs ImageDataGenerator?

- `ImageDataGenerator`: solo imagenes en formato estandar. **Lo mas usado**.
- `Sequence`: cualquier otra cosa. Audio, texto, series temporales, datos tabulares enormes, formatos propietarios."""
    )},
    {"type": "md", "src": dato(
        """**Resumen del notebook 13: cuando uso cada cosa?**

| Caso | Herramienta |
|---|---|
| Calcular cuadrados al vuelo, pocos | `[x**2 for x in ...]` (lista) |
| Calcular cuadrados al vuelo, muchos | `(x**2 for x in ...)` (generator expr) |
| Funcion que produce valores con logica | `def f(): yield ...` (generator function) |
| Pipeline de transformaciones lazy | encadenar generator expressions |
| Datos que no caben en RAM | generador con `yield` (ej. lectura de fichero) |
| Imagenes para CNN | `ImageDataGenerator` + `flow_from_directory` |
| Pequeno dataset en memoria + augment | `ImageDataGenerator` + `.flow(x, y)` |
| Formato custom (audio, tabular pesado) | `class MiGen(tf.keras.utils.Sequence)` |"""
    )},
    {"type": "md", "src": tu_turno(6,
        """**Ejercicio final integrador.** Vamos a recrear, en miniatura, lo que hace `Sequence` pero con un **generador con yield** simple.

Tienes:

```python
import numpy as np
np.random.seed(0)
X = np.arange(20).reshape(20, 1)        # 20 ejemplos de entrada
y = (X.flatten() * 2 + 3)                # y = 2*x + 3
batch_size = 4
```

1. Define una **funcion generadora infinita** `batch_gen(X, y, batch_size)` que:
   - Recorra los datos en orden.
   - Cuando se acabe un epoch, **vuelva a empezar** desde el principio (`while True`).
   - En cada llamada haga `yield` de una tupla `(X_batch, y_batch)` con tamano `batch_size`.

2. Crea el generador.
3. Llama a `next(...)` 6 veces (recuerda: hay 5 batches en una epoca, asi que la 6 ya esta en la segunda epoca) e imprime el `X_batch` de cada uno.

> Tip: usa un indice `i` que empiece en 0 y se incremente en `batch_size`, reseteandose cuando supere `len(X)`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport numpy as np\nnp.random.seed(0)\nX = np.arange(20).reshape(20, 1)\ny = (X.flatten() * 2 + 3)\nbatch_size = 4\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# np.random.seed(0)\n# X = np.arange(20).reshape(20, 1)   # forma (20, 1)\n# y = (X.flatten() * 2 + 3)            # y = 2x + 3, shape (20,)\n# batch_size = 4\n#\n# def batch_gen(X, y, batch_size):\n#     # Generador INFINITO: imprescindible para usarlo en model.fit con steps_per_epoch\n#     i = 0\n#     while True:\n#         # si nos pasamos del final, reiniciamos al principio (nuevo epoch)\n#         if i + batch_size > len(X):\n#             i = 0\n#         # extraemos un batch\n#         X_batch = X[i:i + batch_size]\n#         y_batch = y[i:i + batch_size]\n#         # avanzamos el indice para la siguiente llamada\n#         i += batch_size\n#         # entregamos el batch y pausamos hasta el proximo next()\n#         yield X_batch, y_batch\n#\n# # Crear el generador\n# gen = batch_gen(X, y, batch_size)\n#\n# # Pedir 6 batches: vemos el wrap-around al volver al principio\n# for paso in range(6):\n#     Xb, yb = next(gen)\n#     print(f'paso {paso} -> X_batch.flatten() = {Xb.flatten()}')\n"},
]))


enhance(NB, plan)
print("Done.")

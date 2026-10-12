"""Aplica mejoras pedagogicas al notebook 00_Intro.ipynb.
Inserta celdas de explicacion simple y ejercicios 'TU TURNO'
alrededor de cada ejemplo de codigo, sin tocar el original.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_00_Intro.ipynb"

# ----------------------------------------------------------
# Cell IDs (de 01MIAR_00_Intro.ipynb tras anadirles ID)
# ----------------------------------------------------------
ID_CONTENIDOS    = "cell12-ef2547a6"   # # Contenidos
ID_PYTHON_VER    = "cell13-afdf4b23"   # python_version()
ID_HELLO_VAR     = "cell14-e41119b0"   # a = 15
ID_FSTRING       = "cell15-e1cc8fa1"   # print(f"el valor {a}...")
ID_DEF_MULT      = "cell16-27baff75"   # def mult(a,b): ...
ID_FOR_ENUM      = "cell17-960a401b"   # for i,value in enumerate(...)
ID_NUMPY         = "cell19-47bf48a8"   # numpy random
ID_PANDAS        = "cell21-ebc932a8"   # pandas DataFrame
ID_MATPLOTLIB    = "cell23-0de2e775"   # frame.plot()


plan = []

# -------- Despues de Contenidos: como usar este notebook --------
plan.append((ID_CONTENIDOS, [
    {"type": "md", "src": """### Como usar este notebook (version mejorada)

Este notebook fue **enriquecido** con:

- Explicaciones en **palabras sencillas** antes de cada ejemplo.
- Ejercicios **`TU TURNO`** con celdas vacias para que TU escribas el codigo.
- Cada ejercicio incluye al final una **solucion sugerida** en una celda comentada que puedes destapar si te trabas.

**Como avanzar:**
1. Lee la celda de teoria.
2. Ejecuta la celda de ejemplo (Shift + Enter).
3. Cuando veas un bloque `TU TURNO`, escribe el codigo en la celda vacia que sigue y ejecutala.
4. Si te trabas, destapa la solucion sugerida.

> No saltes los ejercicios. La unica forma de aprender Python es **escribiendo Python**.
"""},
]))

# -------- Despues de python_version() --------
plan.append((ID_PYTHON_VER, [
    {"type": "md", "src": """#### Que acaba de pasar?

- `from platform import python_version` -> trajimos UNA funcion del modulo `platform`. Es como pedir prestado UN libro de una biblioteca, no toda la biblioteca.
- `python_version()` -> esa funcion nos devuelve un texto con la version (ej. `'3.12.1'`).
- `print(...)` -> muestra el texto por pantalla.

**Por que importa la version?** Algunas funciones modernas (como los `f-strings` que veras enseguida) solo existen desde Python 3.6. Si tu version es 2.x o muy antigua, mucho del codigo del curso fallaria.
"""},
    {"type": "md", "src": """##### TU TURNO 1
Importa `system` desde el mismo modulo `platform` y muestra en pantalla en que sistema operativo estas (Windows, Linux, Darwin para macOS).

> Pista: la funcion se llama `system()` y devuelve un texto.
"""},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida (descomenta para ver) ===\n# from platform import system\n# print(system())\n"},
]))

# -------- Despues de a = 15 --------
plan.append((ID_HELLO_VAR, [
    {"type": "md", "src": """#### Que es una variable?

Una **variable** es un nombre que apunta a un valor. Piensa en ella como una **etiqueta pegada a una caja** que contiene algo.

```
a = 15        # Pegamos la etiqueta 'a' a la caja con el numero 15
```

En Python:

- **NO** declaramos el tipo: solo asignamos. Python deduce que `15` es un entero.
- El simbolo `=` significa **asignar**, no "es igual a" (eso es `==`).
- Los nombres de variables deben empezar por letra o `_`, no llevar espacios y no usar palabras reservadas (como `for`, `if`).

Si miras la celda anterior, **no veras nada en pantalla** porque solo asignamos. Para ver el valor tenemos que pedir que se muestre (lo veremos enseguida).
"""},
    {"type": "md", "src": """##### TU TURNO 2
Crea tres variables:
- `nombre` con tu nombre (texto, entre comillas).
- `edad` con tu edad (numero).
- `altura` con tu altura en metros (decimal, ej. `1.75`).

Despues, en la siguiente celda, intenta imprimir las tres usando `print(...)`.
"""},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# nombre = 'Lucas'\n# edad = 30\n# altura = 1.75\n# print(nombre)\n# print(edad)\n# print(altura)\n"},
]))

# -------- Despues de print(f"el valor {a}...") --------
plan.append((ID_FSTRING, [
    {"type": "md", "src": """#### Las f-strings (texto con variables dentro)

Una **f-string** es un texto que **inserta el valor de una variable** sin tener que concatenar con `+`. Se reconoce por la `f` antes de las comillas.

```
nombre = 'Lucas'
print(f'Hola {nombre}')   # -> Hola Lucas
```

Las llaves `{ }` actuan como **huecos** que Python rellena con la variable que pongas dentro.

Por que se usa tanto?
- Es **mas corta** que `'Hola ' + nombre`.
- Es **mas legible**: ves el texto final tal y como va a quedar.
- Soporta calculos: `f'El doble es {n * 2}'`.
"""},
    {"type": "md", "src": """##### TU TURNO 3
Usando las variables `nombre`, `edad` y `altura` de antes, imprime UNA sola linea con la siguiente forma:

```
Me llamo Lucas, tengo 30 anios y mido 1.75 metros.
```

Cambialo con TUS datos. Usa **una sola** f-string.
"""},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# print(f'Me llamo {nombre}, tengo {edad} anios y mido {altura} metros.')\n"},
]))

# -------- Despues de def mult --------
plan.append((ID_DEF_MULT, [
    {"type": "md", "src": """#### Que es una funcion?

Una **funcion** es una **receta de cocina**: la escribes una vez con los pasos, y la usas todas las veces que quieras.

```
def mult(a, b):       # nombre y parametros (los ingredientes)
    return a * b      # lo que devuelve la receta (el plato)
```

Partes:
- `def` -> palabra clave para "definir una funcion".
- `mult` -> el nombre que le pones (eliges tu).
- `(a, b)` -> los parametros, los datos que necesita la funcion para trabajar.
- `return` -> que valor te devuelve. Si no pones return, devuelve `None` (nada).

**Importante:** definir la funcion no la ejecuta. Para usarla la **llamas**:

```
mult(3, 4)   # -> 12
```

La indentacion (los 4 espacios) le dice a Python que esa linea **pertenece** a la funcion.
"""},
    {"type": "md", "src": """##### TU TURNO 4
Define una funcion llamada `saludar` que reciba un parametro `nombre` y devuelva el texto `Hola, NOMBRE!`.

Despues, llama a la funcion con tu nombre y muestrala con `print(...)`.
"""},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def saludar(nombre):\n#     return f'Hola, {nombre}!'\n#\n# mensaje = saludar('Lucas')\n# print(mensaje)\n"},
]))

# -------- Despues de lista + for + enumerate --------
plan.append((ID_FOR_ENUM, [
    {"type": "md", "src": """#### Listas y bucles `for` (paso a paso)

**Lista:** una caja con varios valores **ordenados**, separados por comas, dentro de corchetes.

```
lista = [1, 2, 3]
```

**Bucle for:** repite un bloque de codigo **una vez por cada elemento** de la lista.

```
for value in lista:
    print(value)
```

Si necesitas tambien la **posicion** (0, 1, 2, ...), usa `enumerate`:

```
for i, value in enumerate(lista):
    # i = 0, value = 1   (primera vuelta)
    # i = 1, value = 2   (segunda vuelta)
    # i = 2, value = 3   (tercera vuelta)
    ...
```

En el ejemplo de arriba, dentro del bucle hicimos `lista[i] = mult(value, 10)`. Eso significa: **modifica la lista en la posicion i, poniendo value * 10**.
Por eso al final la lista quedo `[10, 20, 30]`.
"""},
    {"type": "md", "src": """##### TU TURNO 5
Tienes la lista `precios = [100, 200, 300]`. Aplicale un descuento del 10% a cada precio (es decir, multiplica cada elemento por `0.9`) y muestra la lista resultante.

> Resultado esperado: `[90.0, 180.0, 270.0]`
"""},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nprecios = [100, 200, 300]\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# precios = [100, 200, 300]\n# for i, p in enumerate(precios):\n#     precios[i] = p * 0.9\n# print(precios)\n"},
]))

# -------- Despues de NumPy --------
plan.append((ID_NUMPY, [
    {"type": "md", "src": """#### Que es NumPy?

`numpy` es la libreria de **calculo numerico** de Python. Por debajo esta escrita en C, asi que es **muy** rapida.

```
import numpy as np                     # convencion: alias 'np'
np.random.randint(200, size=(10, 2))   # matriz 10x2 de enteros 0..199
```

Que hicimos arriba?
- `np.random.randint(200, ...)` -> genera enteros aleatorios entre 0 y 199.
- `size=(10, 2)` -> queremos una matriz de **10 filas y 2 columnas**.
- El resultado se llama **array** (es como una lista pero mucho mas potente).

Los arrays soportan **operaciones vectorizadas**: puedes multiplicar todo el array por 2 con `arr * 2`, sin necesidad de bucles. En IA esto es lo que hace que entrenar modelos sea viable.
"""},
    {"type": "md", "src": """##### TU TURNO 6
Genera una matriz aleatoria de **5 filas y 3 columnas** con enteros entre 0 y 99 y guardala en una variable llamada `matriz`. Luego mostrala.
"""},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# matriz = np.random.randint(100, size=(5, 3))\n# print(matriz)\n"},
]))

# -------- Despues de pandas --------
plan.append((ID_PANDAS, [
    {"type": "md", "src": """#### Que es pandas?

`pandas` convierte arrays/datos en **tablas** llamadas `DataFrame`. Es como tener Excel dentro de Python, pero mas potente.

```
import pandas as pd
frame = pd.DataFrame(random_list)
```

Lo que recibes:
- Una **tabla** con filas y columnas.
- Con **indice** automatico (0, 1, 2, ...) si no le das uno tu.
- Puedes filtrar, agrupar, ordenar... todo lo que harias en SQL/Excel.

En la celda de arriba creamos un DataFrame a partir de la matriz aleatoria que NumPy nos dio.
"""},
    {"type": "md", "src": """##### TU TURNO 7
Convierte tu `matriz` del ejercicio anterior en un DataFrame de pandas y guardalo en `df`. Pero esta vez asignale **nombres a las columnas**: `'A'`, `'B'`, `'C'`.

> Pista: `pd.DataFrame(datos, columns=['A','B','C'])`
"""},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import pandas as pd\n# df = pd.DataFrame(matriz, columns=['A', 'B', 'C'])\n# df\n"},
]))

# -------- Despues de matplotlib --------
plan.append((ID_MATPLOTLIB, [
    {"type": "md", "src": """#### Que es matplotlib?

`matplotlib` es la libreria estandar para **dibujar graficas** en Python.

```
import matplotlib.pyplot as plt
frame.plot()    # llama internamente a matplotlib y dibuja la tabla
plt.show()      # muestra la grafica en pantalla
```

Que paso?
- `frame.plot()` toma cada columna del DataFrame y la pinta como una linea.
- `plt.show()` abre la ventana con el grafico (en Jupyter no hace falta si tienes `%matplotlib inline`).

En la clase 11 (Visualizacion) veras como personalizarlo: cambiar colores, anadir titulo, ejes, leyendas, etc.
"""},
    {"type": "md", "src": """##### TU TURNO 8
Dibuja un grafico de tu DataFrame `df` (el del ejercicio 7). Solo necesitas **una linea**.
"""},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# df.plot()\n"},
]))


enhance(NB, plan)
print("Done.")

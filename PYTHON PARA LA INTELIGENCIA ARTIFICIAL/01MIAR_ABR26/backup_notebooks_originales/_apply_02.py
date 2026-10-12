"""Aplica mejoras al notebook 02_DataTypes con bloques de colores y teoria detallada."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, solucion_md, dato, aviso

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_02_Python101_DataTypes.ipynb"

# IDs clave del notebook 02
ID_TITULO         = "c64a58eb-2c64-4c5b-9a81-..." # NO USAR - cambia
# Vamos a usar los anchors reales mapeados:
ID_TIPOS_COMMENT  = "b8a9458d-8e9a-4b03-a7fa-..." # "Tipos de comentarios" - cambia tambien
# Mejor extraer los IDs reales con script

import json
nb = json.load(open(NB, encoding="utf-8"))
def find_id(text_fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if text_fragment in src:
            return c["id"]
    return None

ID_TITULO         = nb["cells"][0]["id"]                                # img viu_logo
ID_TIPOS_COMMENT  = find_id("Tipos de comentarios")                     # cell 4
ID_DOCSTRING      = find_id("def producto(x, y):")                      # cell 7
ID_LITERALES      = find_id("## Literales")                             # cell 11
ID_LIT_COMP       = find_id("Literales compuestos")                    # cell 14
ID_VARS           = find_id("## Variables")                             # cell 16
ID_VAR_ASIG       = find_id("Sentencia de asignaci")                    # cell 18
ID_VAR_NOTYPE     = find_id("Las variables no tienen tipo")            # cell 21
ID_REF_COMPART    = find_id("Referencias compartidas")                 # cell 26
ID_INT_GRAND      = find_id("Ojo con los enteros")                     # cell 29
ID_NOMBRES        = find_id("Respecto a los nombres de las variables") # cell 32
ID_ASIG_MULT      = find_id("Asignaci")                                 # primera ocurrencia
ID_ASIG_MULT2     = find_id("Asignaci")
# para evitar la primera, busca multiple
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if "m" in c["id"] and "Asignaci" in src and "ltiple" in src:
        ID_ASIG_MULT2 = c["id"]
        break
ID_OTROS_TIPOS    = find_id("Otros tipos de datos")                    # cell 41
ID_BOOL           = find_id("#### Bool")                                # cell 42
ID_INT_BASES      = find_id("Enteros en otras bases")                  # cell 45
ID_STRINGS        = find_id("#### Strings")                            # cell 48
ID_STR_INMU       = find_id("# Es inmutable")                           # cell 51
ID_CONV           = find_id("Conversi")                                # primera, "Conversion entre tipos"
# busqueda mas precisa
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if src.strip().startswith("## Conversi"):
        ID_CONV = c["id"]
        break
ID_OPERS          = find_id("## Operadores")                           # cell 55
ID_OP_ARIT        = find_id("Operatores aritm")                        # cell 56
ID_OP_COMP        = find_id("Operadores de comparaci")                 # cell 58
ID_OP_LOG         = find_id("Operadores L")                            # cell 60
ID_OP_BIT         = find_id("Bitwise")                                 # cell 63
ID_OP_ASIG        = find_id("Operadores de Asignaci")                  # cell 65
ID_OP_IDENT       = find_id("Operadores de Identidad")                 # cell 67
ID_OP_PERTEN      = find_id("Operadores de Pertenencia")               # cell 69
ID_INPUT          = find_id("## Entrada de valores")                   # cell 71
ID_COL_HEADER     = find_id("# Tipos de datos compuestos")             # cell 74
ID_LISTAS         = find_id("## Listas")                               # cell 75
ID_LIST_CREA      = find_id("Creaci")  # primera, "Creacion de listas"
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if src.strip().startswith("#### Creaci") and "listas" in src:
        ID_LIST_CREA = c["id"]
        break
ID_LIST_OPS       = find_id("Operaciones b")                           # cell 79
ID_LIST_SLICE     = find_id("**Slicing**")                              # cell 86
ID_LIST_ALIAS     = find_id("Alias/Referencias")                       # cell 91
ID_LIST_ANIDA     = find_id("Anidamiento.")  # primera
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if src.strip().startswith("#### Anidamiento"):
        ID_LIST_ANIDA = c["id"]
        break
ID_TUPLAS         = find_id("## Tuplas")                               # cell 128
ID_TUP_INMU       = find_id("Asignación a tuplas falla")           # cell 139
ID_TUP_UNPACK     = find_id("Desempaquetar una tupla")                 # cell 148
ID_SETS           = find_id("## Sets")                                  # cell 152
ID_SET_OPS        = find_id("Uni")                                      # primera, "Union, interseccion"
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if src.strip().startswith("* Uni"):
        ID_SET_OPS = c["id"]
        break
ID_SECUENCIAS     = find_id("## Secuencias")                           # cell 175
ID_DICTS          = find_id("## Diccionarios")                         # cell 180
ID_DICT_GET       = find_id("Buscar de forma segura")                  # cell 191
ID_FINAL_MAT      = find_id("matiz importante")                        # cell 205


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
]))

# ============ COMENTARIOS ============
plan.append((ID_TIPOS_COMMENT, [
    {"type": "md", "src": teoria(
        "Comentarios: tipos y cuando usar cada uno",
        """Un **comentario** es texto que Python **ignora al ejecutar**. Existe solo para humanos.

#### 1. Comentario de UNA linea: `#`
```python
# Esto es un comentario completo
x = 5  # Tambien puede ir al final de la linea
```

#### 2. Comentario de VARIAS lineas (truco): triple comilla
```python
'''
Este texto ocupa
varias lineas y Python lo ignora porque
no se asigna a nada.
'''
```
Tecnicamente es un *string* sin asignar, no un comentario real, pero funciona.

#### 3. Docstring: documentar funciones, clases, modulos
```python
def producto(x, y):
    '''Calcula el producto de dos numeros.'''   # docstring
    return x * y

help(producto)   # imprime el docstring
producto.__doc__ # accede al docstring
```

| Cuando usar | Que tipo |
|---|---|
| Explicar el **POR QUE** de una linea | `#` al final |
| Documentar una funcion / clase / modulo | docstring `'''...'''` justo debajo |
| Anular codigo temporalmente para depurar | `#` |

**Buena practica (PEP 257):** todas tus funciones publicas deberian tener un docstring corto que diga **que hacen**, no **como lo hacen**."""
    )},
]))

plan.append((ID_DOCSTRING, [
    {"type": "md", "src": tu_turno(1,
        """Define una funcion `area_rectangulo(base, altura)` que devuelva `base * altura`. Anadele un **docstring** de UNA linea explicando que hace. Despues, llama a `help(area_rectangulo)` para ver tu docstring."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def area_rectangulo(base, altura):\n#     '''Devuelve el area de un rectangulo: base * altura.'''\n#     return base * altura\n#\n# help(area_rectangulo)\n"},
]))

# ============ LITERALES ============
plan.append((ID_LITERALES, [
    {"type": "md", "src": teoria(
        "Que es un literal?",
        """Un **literal** es un valor que escribes directamente en el codigo, **sin ponerle un nombre**. Python sabe que tipo de dato es solo de mirarlo.

```python
4           # literal entero (int)
3.14        # literal decimal (float)
"Hola"      # literal cadena (str)
True        # literal booleano (bool)
None        # literal especial: ausencia de valor
[1, 2, 3]   # literal lista
(1, 2, 3)   # literal tupla
{1, 2, 3}   # literal conjunto (set)
{'a': 1}    # literal diccionario
```

**Tipos primitivos basicos** (los que veras enseguida):

| Literal | Tipo Python | Ejemplo |
|---|---|---|
| Entero | `int` | `42`, `-7`, `1_000_000` |
| Decimal | `float` | `3.14`, `2.0`, `1e3` |
| Cadena | `str` | `'hola'`, `"mundo"`, `'''multi linea'''` |
| Booleano | `bool` | `True`, `False` |
| Vacio | `NoneType` | `None` |
| Complejo | `complex` | `2+3j` |

**Truco util:** los enteros aceptan guiones bajos para que sean legibles: `1_000_000` es lo mismo que `1000000`."""
    )},
]))

plan.append((ID_LIT_COMP, [
    {"type": "md", "src": teoria(
        "Literales compuestos: una vista rapida",
        """Los **literales compuestos** son colecciones que agrupan varios valores. Veras cada uno en detalle mas adelante, pero conviene saber distinguirlos:

| Sintaxis | Tipo | Mutable? | Ordenado? | Permite duplicados? |
|---|---|---|---|---|
| `[1, 2, 3]` | `list` | Si | Si | Si |
| `(1, 2, 3)` | `tuple` | **No** | Si | Si |
| `{1, 2, 3}` | `set` | Si | No | **No** |
| `{'a': 1, 'b': 2}` | `dict` | Si | Si (3.7+) | claves no |

**Mutable** = puedes cambiar su contenido despues de crearlo.
**Ordenado** = los elementos mantienen el orden en que los pones.
**Permite duplicados** = `[1, 1, 2]` es valido, pero un set lo reduce a `{1, 2}`."""
    )},
    {"type": "md", "src": tu_turno(2,
        """Crea un literal de cada uno de los 4 tipos compuestos: una `lista`, una `tupla`, un `set` y un `dict`. Luego usa `type(...)` con cada uno y muestra el resultado con `print(...)`.

> Pista: `print(type(mi_lista))` deberia mostrar `<class 'list'>`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# mi_lista  = [1, 2, 3]\n# mi_tupla  = (1, 2, 3)\n# mi_set    = {1, 2, 3}\n# mi_dict   = {'a': 1, 'b': 2}\n# print(type(mi_lista))\n# print(type(mi_tupla))\n# print(type(mi_set))\n# print(type(mi_dict))\n"},
]))

# ============ VARIABLES ============
plan.append((ID_VARS, [
    {"type": "md", "src": teoria(
        "Variables: la idea de la 'etiqueta'",
        """Una **variable** en Python es un **nombre que apunta a un objeto**. NO es una caja que contiene el valor, es una **etiqueta pegada** a un objeto que vive en memoria.

```python
a = 5
```

Lo que pasa por dentro:

1. Python crea el objeto `5` en algun lugar de la memoria.
2. Python pega la etiqueta `a` a ese objeto.

Si haces `b = a`, **NO copias el valor**: pegas otra etiqueta al mismo objeto.

```
   memoria
   --------
   [obj 5]  <- a
            <- b   (apunta al mismo objeto)
```

**Consecuencia:** entender esto te ahorra un mundo de bugs cuando trabajes con listas, diccionarios u objetos."""
    )},
]))

plan.append((ID_VAR_NOTYPE, [
    {"type": "md", "src": teoria(
        "Las variables no tienen tipo, los OBJETOS si",
        """Una variable en Python **no tiene tipo**: es solo un nombre. **El tipo lo tiene el OBJETO al que apunta**.

```python
a = 1        # 'a' apunta a un objeto int
a = 'hola'   # ahora 'a' apunta a un objeto str
a = [1, 2]   # ahora 'a' apunta a una lista
```

En cada linea, el objeto al que apuntaba `a` antes queda **huerfano**. Si ningun otro nombre lo usa, Python lo elimina de la memoria automaticamente (*garbage collection*).

**Otros lenguajes (Java, C#)** te obligan a declarar el tipo: `int a = 5;`. Python no.

**Para saber el tipo en cualquier momento:**
```python
type(a)         # <class 'list'>
isinstance(a, list)  # True
```"""
    )},
    {"type": "md", "src": tu_turno(3,
        """Crea una variable `x` y asignale **secuencialmente** estos cuatro valores, imprimiendo `type(x)` despues de cada asignacion: `42`, `3.14`, `"texto"`, `[1, 2, 3]`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# x = 42\n# print(type(x))\n# x = 3.14\n# print(type(x))\n# x = 'texto'\n# print(type(x))\n# x = [1, 2, 3]\n# print(type(x))\n"},
]))

plan.append((ID_REF_COMPART, [
    {"type": "md", "src": teoria(
        "Referencias compartidas y la funcion <code>id()</code>",
        """Cada objeto en memoria tiene un **identificador unico** (su direccion). La funcion `id(objeto)` te lo devuelve.

```python
a = 100
b = a       # b apunta al mismo objeto que a
print(id(a) == id(b))   # True

a is b      # True   <- 'is' compara IDENTIDAD (mismo objeto)
a == b      # True   <- '==' compara VALOR
```

**Diferencia clave:**
- `==` -> *son iguales en valor?*
- `is` -> *son el MISMO objeto en memoria?*

```python
x = [1, 2, 3]
y = [1, 2, 3]    # otra lista, mismo contenido
x == y           # True  (mismo valor)
x is y           # False (objetos distintos)
```

**Optimizacion curiosa:** Python guarda los enteros pequenos (-5 a 256) y los strings cortos en cache. Por eso a veces `is` te puede sorprender con numeros pequenos."""
    )},
]))

plan.append((ID_INT_GRAND, [
    {"type": "md", "src": tu_turno(4,
        """Crea dos variables `a = 256` y `b = 256`. Comprueba si `a is b`. Despues, repite el experimento con `a = 1000` y `b = 1000`. Que observas?

> Lo que veras explica el comentario del codigo de arriba sobre el rango `[-5, 256]`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# a = 256\n# b = 256\n# print(a is b)   # True (Python cachea enteros pequenos)\n# a = 1000\n# b = 1000\n# print(a is b)   # Puede dar False (depende del cache)\n# # MORALEJA: usa '==' para comparar valores, NO 'is'\n"},
]))

# ============ STRINGS ============
plan.append((ID_STRINGS, [
    {"type": "md", "src": teoria(
        "Strings (cadenas de texto): teoria completa",
        """Un **string** es una **secuencia inmutable de caracteres**. En Python no hay un tipo aparte para 'caracter': un caracter es simplemente un string de longitud 1.

#### Crear un string

```python
s1 = 'hola'           # comillas simples
s2 = "mundo"          # comillas dobles (equivalentes)
s3 = '''varias        # triple comilla -> permite saltos de linea
lineas'''
s4 = "Ella dijo: 'hola'"   # mezcla para evitar escapar
s5 = 'Ella dijo: "hola"'
```

#### Caracteristicas clave

| Propiedad | Detalle |
|---|---|
| **Inmutable** | NO puedes modificar un caracter individual: `s[0] = 'H'` -> error. |
| **Indexable** | `s[0]` primer caracter, `s[-1]` ultimo. |
| **Soporta slicing** | `s[1:4]`, `s[::-1]` (invertir). |
| **Iterable** | `for c in s:` recorre cada caracter. |
| **Soporta `len`** | `len('hola')` -> 4. |
| **Soporta `in`** | `'la' in 'hola'` -> True. |

#### Caracteres especiales

```python
'\\n'    # salto de linea
'\\t'    # tabulacion
'\\\\'   # barra inversa literal
'\\''    # comilla simple dentro de comilla simple
'\\"'    # comilla doble dentro de comilla doble
```

#### Operaciones tipicas

```python
'hola' + ' ' + 'mundo'     # 'hola mundo'  (concatenacion)
'ja' * 3                   # 'jajaja'       (repeticion)
'hola'.upper()             # 'HOLA'
'HOLA'.lower()             # 'hola'
'  hola  '.strip()         # 'hola'         (quita espacios en bordes)
'hola mundo'.split()       # ['hola', 'mundo']
'-'.join(['a', 'b', 'c'])  # 'a-b-c'
'hola'.replace('o', '0')   # 'h0la'
'hola'.startswith('h')     # True
'hola mundo'.find('mu')    # 5  (posicion, o -1 si no esta)
```

#### f-strings (formato moderno, Python 3.6+)

```python
nombre = 'Lucas'
edad = 30
print(f'Hola {nombre}, tienes {edad} anios')
print(f'El doble es {edad * 2}')   # acepta expresiones
print(f'{3.14159:.2f}')            # formato: 3.14
```"""
    )},
]))

plan.append((ID_STR_INMU, [
    {"type": "md", "src": aviso(
        """Acabas de ver que `s[2] = 't'` da error. Eso confirma que **los strings son inmutables**.

Si necesitas 'modificar' un string, en realidad creas uno nuevo:
```python
s = 'hola'
s = s[:2] + 't' + s[3:]   # 'hota'  (nuevo string, no modifica el viejo)
```

Esto es **importante para el rendimiento**: concatenar miles de strings con `+` en un bucle es lento (crea muchos objetos temporales). Para eso usa `''.join(lista_de_strings)`."""
    )},
    {"type": "md", "src": tu_turno(5,
        """Tienes el string `frase = 'python es genial'`. Sin tocar la variable original (recuerda: inmutable), genera un NUEVO string llamado `resultado` que sea la frase **en mayusculas y con la palabra 'genial' reemplazada por 'fantastico'**. Imprimelo.

> Resultado esperado: `PYTHON ES FANTASTICO`"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nfrase = 'python es genial'\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# frase = 'python es genial'\n# resultado = frase.replace('genial', 'fantastico').upper()\n# print(resultado)\n"},
]))

# ============ CONVERSION ============
plan.append((ID_CONV, [
    {"type": "md", "src": teoria(
        "Conversion entre tipos (casting)",
        """A veces tienes un valor en un tipo pero lo necesitas en otro. Python tiene **funciones de conversion** con el nombre del tipo:

| Funcion | De que -> a que | Ejemplo |
|---|---|---|
| `int(x)` | float/str -> int | `int(2.8)` -> `2` (trunca) |
| `float(x)` | int/str -> float | `float('3.14')` -> `3.14` |
| `str(x)` | cualquier -> str | `str(42)` -> `'42'` |
| `bool(x)` | cualquier -> bool | `bool(0)` -> `False` |
| `list(x)` | iterable -> list | `list('abc')` -> `['a','b','c']` |
| `tuple(x)` | iterable -> tuple | `tuple([1,2])` -> `(1,2)` |
| `set(x)` | iterable -> set | `set([1,1,2])` -> `{1,2}` |

#### Cuidado con la conversion a bool

Estos valores se consideran **`False`**:
- `0`, `0.0`, `0j` (cero numerico)
- `''`, `[]`, `()`, `{}`, `set()` (colecciones vacias)
- `None`
- `False`

**Todo lo demas es `True`**, incluido `'False'` (un string no vacio!) y `[0]` (una lista no vacia).

#### Cuando falla la conversion

```python
int('hola')       # ValueError: no se puede convertir
float('3,14')     # ValueError: usa punto, no coma
int('3.14')       # ValueError: int() no acepta decimales en string
int(float('3.14')) # 3  -> truco: a float primero, luego a int
```"""
    )},
    {"type": "md", "src": tu_turno(6,
        """Tienes la variable `texto = '42'`. Conviertela a entero, multiplicalo por 2 y vuelve a convertirlo a string. Imprime el resultado y su tipo.

> Resultado esperado: `'84'` con `type` `<class 'str'>`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\ntexto = '42'\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# texto = '42'\n# numero = int(texto)\n# doble = numero * 2\n# resultado = str(doble)\n# print(resultado)\n# print(type(resultado))\n"},
]))

# ============ OPERADORES ============
plan.append((ID_OPERS, [
    {"type": "md", "src": teoria(
        "Operadores: panorama general",
        """Los **operadores** son simbolos que combinan valores para producir nuevos valores. Python los agrupa en familias:

| Familia | Que hacen | Ejemplos |
|---|---|---|
| **Aritmeticos** | calcular | `+`, `-`, `*`, `/`, `//`, `%`, `**` |
| **Comparacion** | preguntar si | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| **Logicos** | combinar booleanos | `and`, `or`, `not` |
| **Asignacion** | asignar y operar | `=`, `+=`, `-=`, `*=`, etc. |
| **Identidad** | mismo objeto? | `is`, `is not` |
| **Pertenencia** | esta dentro? | `in`, `not in` |
| **Bitwise** | bit a bit | `&`, `|`, `^`, `~`, `<<`, `>>` |

**Distinciones que confunden mucho a los principiantes:**

- `=` asigna. `==` compara. **NO son lo mismo**.
- `/` da decimal: `7 / 2 = 3.5`. `//` da entero (division entera): `7 // 2 = 3`.
- `%` es el **resto** (modulo): `7 % 2 = 1`.
- `**` es potencia: `2 ** 10 = 1024`.
- `is` compara identidad. `==` compara valor.
- `and`/`or` son **cortocircuito**: `False and X` no llega a evaluar `X`."""
    )},
]))

plan.append((ID_OP_ARIT, [
    {"type": "md", "src": teoria(
        "Operadores aritmeticos: tabla de bolsillo",
        """| Operador | Nombre | Ejemplo | Resultado |
|---|---|---|---|
| `+` | suma | `3 + 4` | `7` |
| `-` | resta | `10 - 3` | `7` |
| `*` | multiplicacion | `3 * 4` | `12` |
| `/` | division (siempre float) | `7 / 2` | `3.5` |
| `//` | division entera | `7 // 2` | `3` |
| `%` | modulo (resto) | `7 % 2` | `1` |
| `**` | potencia | `2 ** 10` | `1024` |

**Precedencia (de mayor a menor):** `**`, luego `*` `/` `//` `%`, luego `+` `-`. Usa parentesis cuando dudes.

**Casos curiosos:**
```python
3 + 4 * 2     # 11    (no 14: el * va antes que el +)
(3 + 4) * 2   # 14
2 ** 0.5      # 1.41... raiz cuadrada
-7 // 2       # -4    (redondea hacia abajo, no hacia cero!)
0 / 1         # 0.0
1 / 0         # ZeroDivisionError
```"""
    )},
    {"type": "md", "src": tu_turno(7,
        """Pide al usuario su edad con `input(...)` (sale como str, recuerda convertir). Luego imprime:
- Su edad **en meses** (edad * 12).
- Su edad **en dias** (aproximada: edad * 365).
- Si su edad es par o impar (usa `%` con 2)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# edad = int(input('Tu edad: '))\n# print('Meses:', edad * 12)\n# print('Dias aprox:', edad * 365)\n# resto = edad % 2\n# if resto == 0:\n#     print('Es par')\n# else:\n#     print('Es impar')\n"},
]))

plan.append((ID_OP_LOG, [
    {"type": "md", "src": teoria(
        "Operadores logicos: <code>and</code>, <code>or</code>, <code>not</code>",
        """Combinan valores **booleanos** (`True`/`False`).

| Operador | Significado | Tabla rapida |
|---|---|---|
| `and` | Y (los dos True) | `True and True` -> `True`. Cualquier `False` -> `False`. |
| `or` | O (al menos uno True) | `False or False` -> `False`. Cualquier `True` -> `True`. |
| `not` | Negacion | `not True` -> `False`, `not False` -> `True`. |

#### Cortocircuito (importante!)

Python **no evalua lo que no necesita**:
```python
False and funcion_costosa()   # NO llama a la funcion (ya sabe que es False)
True  or  funcion_costosa()   # NO llama a la funcion (ya sabe que es True)
```

Esto se aprovecha para evitar errores:
```python
x = None
if x is not None and x > 0:   # si x es None, NO evalua x > 0 (no falla)
    ...
```

#### Truco: <code>and</code>/<code>or</code> no devuelven booleanos

Devuelven el **valor que decidio** el resultado. Es raro pero importante:
```python
0 or 'hola'    # 'hola'   (0 es falsy, pasa al siguiente)
5 or 'hola'    # 5        (5 es truthy, no necesita mirar el siguiente)
5 and 'hola'   # 'hola'   (los dos truthy, devuelve el ultimo)
0 and 'hola'   # 0        (0 es falsy, corta)
```"""
    )},
]))

plan.append((ID_OP_IDENT, [
    {"type": "md", "src": teoria(
        "Identidad (<code>is</code>) vs Igualdad (<code>==</code>)",
        """Esta es una de las trampas mas frecuentes en Python:

```python
==   # iguales en VALOR
is   # iguales en IDENTIDAD (mismo objeto en memoria)
```

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b    # True   (contenido igual)
a is b    # False  (son dos listas distintas)

c = a
a is c    # True   (c apunta al mismo objeto que a)
```

**Cuando usar `is`?** Solo para comparar con singletons especiales:
```python
x is None
x is True
x is False
```

Para todo lo demas, **usa `==`**. Si usas `is` con strings o numeros, a veces funciona por casualidad (cache de Python) y a veces no. Es una bomba de relojeria."""
    )},
    {"type": "md", "src": tu_turno(8,
        """Crea dos listas distintas con el mismo contenido: `lista1 = [1, 2, 3]`, `lista2 = [1, 2, 3]`. Despues haz `lista3 = lista1`. Compara las tres con `==` y con `is` y muestra los resultados con un texto explicativo."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# lista1 = [1, 2, 3]\n# lista2 = [1, 2, 3]\n# lista3 = lista1\n#\n# print('lista1 == lista2:', lista1 == lista2)   # True\n# print('lista1 is lista2:', lista1 is lista2)   # False\n# print('lista1 == lista3:', lista1 == lista3)   # True\n# print('lista1 is lista3:', lista1 is lista3)   # True (mismo objeto)\n"},
]))

# ============ INPUT ============
plan.append((ID_INPUT, [
    {"type": "md", "src": teoria(
        "<code>input()</code>: pedir datos al usuario",
        """`input()` es la funcion incorporada para **leer una linea de texto** que el usuario teclee.

```python
nombre = input('Como te llamas? ')
print('Hola', nombre)
```

#### CLAVE: input() SIEMPRE devuelve un string

Aunque el usuario escriba `42`, lo que recibes es `'42'` (texto). Si quieres un numero, **convierte**:

```python
edad = input('Tu edad: ')         # '30' (string!)
edad = int(input('Tu edad: '))    # 30 (int)
peso = float(input('Tu peso: ')) # 75.5 (float)
```

#### Patrones comunes

```python
# Pedir un numero con valor por defecto si esta vacio
texto = input('Edad (vacio = 18): ')
edad = int(texto) if texto else 18

# Pedir varios valores en una linea
a, b = input('Dos numeros separados por espacio: ').split()
a, b = int(a), int(b)

# Validar
while True:
    edad = input('Edad: ')
    if edad.isdigit():
        edad = int(edad)
        break
    print('Por favor, escribe un numero')
```"""
    )},
    {"type": "md", "src": tu_turno(9,
        """Pide al usuario dos numeros (uno por linea) usando `input()`. Convierte ambos a `float`. Imprime su **suma**, **resta**, **producto** y **division**, cada uno en una linea con un texto descriptivo (usa f-strings)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# a = float(input('Primer numero: '))\n# b = float(input('Segundo numero: '))\n# print(f'Suma:    {a + b}')\n# print(f'Resta:   {a - b}')\n# print(f'Producto:{a * b}')\n# print(f'Division:{a / b}')\n"},
]))

# ============ LISTAS (la teoria mas grande) ============
plan.append((ID_LISTAS, [
    {"type": "md", "src": teoria(
        "Listas: la coleccion mas usada de Python",
        """Una **lista** es una **coleccion ordenada y mutable** de elementos. Es probablemente el tipo de dato que mas vas a usar en Python.

#### Que tipos de datos puede contener una lista?

**CUALQUIERA. Y MEZCLADOS.** Las listas Python son **heterogeneas**:

```python
mezcla = [1, 'hola', 3.14, True, None, [10, 20], {'a': 1}]
#         int  str   float bool None  lista       dict
```

Esto las diferencia de los arrays de C, Java o NumPy, que solo aceptan UN tipo. En Python no hay esa restriccion.

#### Caracteristicas clave

| Propiedad | Significado |
|---|---|
| **Ordenada** | Mantiene el orden en que pones los elementos. |
| **Indexable** | `lista[0]`, `lista[-1]` (ultimo). |
| **Mutable** | Puedes anadir, modificar y quitar elementos. |
| **Heterogenea** | Mezcla cualquier tipo de dato. |
| **Tamano dinamico** | No fijas tamano al crearla. |
| **Iterable** | `for x in lista:` recorre todos los elementos. |
| **Soporta duplicados** | `[1, 1, 2]` esta permitido. |

#### Cinco formas de crearla

```python
l1 = []                       # vacia
l2 = list()                   # vacia (forma alternativa)
l3 = [1, 2, 3]                # con valores
l4 = list('abc')              # ['a', 'b', 'c']  desde un iterable
l5 = [x * 2 for x in range(5)]  # [0,2,4,6,8] - list comprehension
```

> En el codigo de abajo veras estas formas. La **list comprehension** la veras a fondo en la clase 03 y 04, pero adelantamos: es una forma compacta de crear listas con un bucle interno."""
    )},
]))

plan.append((ID_LIST_OPS, [
    {"type": "md", "src": teoria(
        "Operaciones basicas con listas: la chuleta",
        """Aqui esta el **80% de lo que vas a hacer** con listas. Memoriza esta tabla.

| Operacion | Codigo | Que hace |
|---|---|---|
| Tamano | `len(l)` | Cuantos elementos |
| Acceso | `l[i]` | Elemento en posicion i (0-indexed) |
| Acceso final | `l[-1]` | Ultimo elemento |
| Modificar | `l[i] = x` | Cambia el elemento i |
| Slicing | `l[a:b]` | Sublista de a (incluido) a b (excluido) |
| Slicing paso | `l[a:b:p]` | Sublista con paso p |
| Invertir | `l[::-1]` | Lista invertida (copia) |
| Anadir final | `l.append(x)` | Anade x al final |
| Anadir varios | `l.extend([x,y])` | Concatena varios al final |
| Insertar | `l.insert(i, x)` | Inserta x en posicion i |
| Quitar valor | `l.remove(x)` | Quita la PRIMERA aparicion de x |
| Quitar pos | `l.pop(i)` | Quita y devuelve el de la posicion i (defecto: ultimo) |
| Buscar pos | `l.index(x)` | Posicion de la primera aparicion |
| Contar | `l.count(x)` | Cuantas veces aparece |
| Ordenar | `l.sort()` | Ordena en sitio |
| Ordenar copia | `sorted(l)` | Devuelve copia ordenada |
| Invertir | `l.reverse()` | Invierte en sitio |
| Concatenar | `l1 + l2` | Nueva lista |
| Repetir | `l * 3` | Nueva lista repetida |
| Pertenencia | `x in l` | True/False |
| Recorrer | `for x in l:` | Iterar |
| Vaciar | `l.clear()` | Quita todo |
| Copiar | `l.copy()` o `l[:]` | Copia superficial |

#### Slicing con detalle

```python
letras = ['a', 'b', 'c', 'd', 'e']
#         0    1    2    3    4
#        -5   -4   -3   -2   -1

letras[1:3]    # ['b', 'c']     (incluye 1, excluye 3)
letras[:3]     # ['a', 'b', 'c'] (desde el inicio)
letras[2:]     # ['c', 'd', 'e'] (hasta el final)
letras[:]      # ['a','b','c','d','e']  (copia completa!)
letras[::2]    # ['a', 'c', 'e']   (paso 2)
letras[::-1]   # ['e','d','c','b','a'] (invertido)
```"""
    )},
]))

plan.append((ID_LIST_SLICE, [
    {"type": "md", "src": tu_turno(10,
        """Tienes `numeros = list(range(10))`. Eso es `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`. Usando **solo slicing**:

1. Extrae los **primeros 3** elementos.
2. Extrae los **ultimos 3** elementos.
3. Extrae los **pares** (paso de 2).
4. Crea la lista **invertida**.
5. Extrae los elementos del **medio** (sin el primero ni el ultimo).

Imprime cada resultado."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nnumeros = list(range(10))\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# numeros = list(range(10))\n# print(numeros[:3])      # [0, 1, 2]\n# print(numeros[-3:])     # [7, 8, 9]\n# print(numeros[::2])     # [0, 2, 4, 6, 8]\n# print(numeros[::-1])    # [9, 8, 7, ..., 0]\n# print(numeros[1:-1])    # [1, 2, 3, 4, 5, 6, 7, 8]\n"},
]))

plan.append((ID_LIST_ALIAS, [
    {"type": "md", "src": teoria(
        "Alias y referencias: cuidado con copiar listas",
        """Esto es **el bug numero 1** que les pasa a los principiantes en Python.

```python
a = [1, 2, 3]
b = a           # b NO es una copia, es OTRO NOMBRE para la misma lista
b.append(4)
print(a)        # [1, 2, 3, 4]   <- a tambien cambio!
```

Por que? Porque `=` solo **pega otra etiqueta** al mismo objeto. **No copia el contenido**.

#### Como hacer una copia REAL?

```python
b = a.copy()       # copia superficial (recomendada)
b = a[:]           # copia superficial (forma vieja)
b = list(a)        # copia superficial
import copy
b = copy.deepcopy(a)   # copia PROFUNDA (recursiva)
```

#### Diferencia entre superficial y profunda

```python
a = [[1, 2], [3, 4]]
b = a.copy()        # b es una NUEVA lista, pero sus elementos siguen apuntando a las MISMAS sublistas
b[0].append(99)
print(a)            # [[1, 2, 99], [3, 4]]   <- a tambien cambio en la sublista!

import copy
c = copy.deepcopy(a)   # c y todas sus sublistas son nuevas
c[0].append(100)
print(a)               # SIN tocar
```

| Que copio | Necesito |
|---|---|
| Lista de tipos simples (int, str, float) | `.copy()` o `[:]` basta |
| Lista de listas / dicts / objetos | `copy.deepcopy(...)` |"""
    )},
    {"type": "md", "src": tu_turno(11,
        """Crea una lista `original = [10, 20, 30]`. Haz tres 'copias' distintas:

1. `mala_copia = original` (no es copia, es un alias).
2. `buena_copia_1 = original.copy()`.
3. `buena_copia_2 = original[:]`.

Despues, anade `99` a `original` y muestra las tres listas. Vas a ver que solo `mala_copia` se contagio del cambio."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# original = [10, 20, 30]\n# mala_copia = original\n# buena_copia_1 = original.copy()\n# buena_copia_2 = original[:]\n#\n# original.append(99)\n#\n# print('original:      ', original)       # [10, 20, 30, 99]\n# print('mala_copia:    ', mala_copia)     # [10, 20, 30, 99]  <- alias!\n# print('buena_copia_1: ', buena_copia_1)  # [10, 20, 30]\n# print('buena_copia_2: ', buena_copia_2)  # [10, 20, 30]\n"},
]))

# ============ TUPLAS ============
plan.append((ID_TUPLAS, [
    {"type": "md", "src": teoria(
        "Tuplas: como listas, pero <b>inmutables</b>",
        """Una **tupla** es como una lista, pero **no se puede modificar** despues de crearla. Se escribe con parentesis (o sin nada):

```python
t1 = (1, 2, 3)         # tupla con parentesis
t2 = 1, 2, 3           # tambien es tupla! (los parentesis son opcionales)
t3 = (1,)              # tupla de UN elemento. La coma es OBLIGATORIA
t4 = ()                # tupla vacia
t5 = tuple([1, 2, 3])  # desde una lista
```

> **Trampa:** `(1)` NO es tupla, es solo el numero 1 con parentesis. Necesitas la coma: `(1,)`.

#### Por que existen las tuplas si ya hay listas?

| Ventaja | Detalle |
|---|---|
| **Inmutables** | Garantia de que nadie las modifica. Mas seguras como claves de un dict, parametros de funcion, constantes. |
| **Mas rapidas** | Menos memoria y mas rapidas de crear que las listas (Python sabe que no cambiaran). |
| **Hashables** | Puedes usarlas como claves en dicts o elementos en sets (las listas no, porque son mutables). |
| **Desempaquetado** | `a, b = (1, 2)` lo permite, y se usa muchisimo. |

#### Operaciones que SI funcionan en tuplas

Practicamente todas las de **lectura**:
```python
t = (10, 20, 30, 20)
len(t)        # 4
t[0]          # 10
t[-1]         # 30
t[1:3]        # (20, 30)
t.count(20)   # 2
t.index(30)   # 2
20 in t       # True
for x in t: print(x)
```

#### Lo que NO funciona

```python
t[0] = 99        # ERROR: 'tuple' object does not support item assignment
t.append(40)    # ERROR: las tuplas no tienen append
```

#### Que hago si necesito 'modificar' una tupla?

Conviertela a lista, modificala, y vuelvela a tupla:
```python
t = (1, 2, 3)
l = list(t)
l[0] = 99
t = tuple(l)
```"""
    )},
]))

plan.append((ID_TUP_UNPACK, [
    {"type": "md", "src": teoria(
        "Desempaquetado de tuplas (unpacking): el truco que usaras a diario",
        """**Desempaquetar** una tupla significa **asignar cada elemento a una variable** en una sola linea:

```python
punto = (3, 5)
x, y = punto         # x = 3, y = 5

persona = ('Lucas', 30, 'Madrid')
nombre, edad, ciudad = persona
```

#### Intercambiar variables (sin variable temporal)

```python
a, b = 1, 2
a, b = b, a       # ahora a=2, b=1   (sin necesidad de temp!)
```

#### Desempaquetado con <code>*</code>: el resto

Si tienes una tupla con muchos elementos pero solo te interesan algunos:

```python
t = (1, 2, 3, 4, 5)

primero, *resto = t          # primero=1, resto=[2, 3, 4, 5]
*todos_menos_ultimo, ultimo = t   # [1,2,3,4], 5
primero, *medio, ultimo = t  # 1, [2,3,4], 5
```

Nota: el `*resto` siempre captura una **lista**, no una tupla.

#### En funciones (lo veras en clase 04)

Las funciones que devuelven varios valores en realidad devuelven una tupla:
```python
def min_max(lista):
    return min(lista), max(lista)   # devuelve una tupla

a, b = min_max([3, 1, 4, 1, 5])     # desempaqueta directamente
```"""
    )},
    {"type": "md", "src": tu_turno(12,
        """Tienes la tupla `datos = ('Ada', 'Lovelace', 1815, 'matematicas')`. Desempaquetala en cuatro variables: `nombre`, `apellido`, `anio`, `area`. Luego imprime: `Ada Lovelace nacio en 1815 y trabajo en matematicas`.

**Bonus:** ahora con `numeros = (10, 20, 30, 40, 50)`, usa `*` para guardar el primero en `primero`, el ultimo en `ultimo` y el resto en `medio` (que sera una lista de tres elementos)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\ndatos = ('Ada', 'Lovelace', 1815, 'matematicas')\nnumeros = (10, 20, 30, 40, 50)\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# datos = ('Ada', 'Lovelace', 1815, 'matematicas')\n# nombre, apellido, anio, area = datos\n# print(f'{nombre} {apellido} nacio en {anio} y trabajo en {area}')\n#\n# numeros = (10, 20, 30, 40, 50)\n# primero, *medio, ultimo = numeros\n# print(primero, medio, ultimo)\n"},
]))

# ============ SETS ============
plan.append((ID_SETS, [
    {"type": "md", "src": teoria(
        "Sets (conjuntos): coleccion sin duplicados ni orden",
        """Un **set** es una coleccion de elementos **unicos** y **sin orden**. Se inspira en los conjuntos matematicos.

```python
s1 = set()              # set vacio
s2 = {1, 2, 3}          # set con valores
s3 = set([1, 1, 2, 3])  # {1, 2, 3}  -- los duplicados se eliminan
```

> **Cuidado:** `{}` es un **dict vacio**, no un set vacio. Para un set vacio usa `set()`.

#### Caracteristicas

| Propiedad | Detalle |
|---|---|
| **Sin duplicados** | Si anades el mismo valor, no se duplica. |
| **Sin orden** | NO puedes acceder por indice: `s[0]` da error. |
| **Mutable** | Puedes anadir y quitar. |
| **Elementos hashables** | Solo acepta tipos inmutables (int, str, tuple). NO listas. |
| **Muy rapido para `in`** | `x in set` es O(1), `x in lista` es O(n). |

#### Operaciones de conjuntos (notacion matematica)

```python
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

A | B    # {1,2,3,4,5,6}    union
A & B    # {3, 4}           interseccion
A - B    # {1, 2}           diferencia
A ^ B    # {1,2,5,6}        diferencia simetrica (ni en uno ni en otro)
```

Tambien tienes los metodos: `A.union(B)`, `A.intersection(B)`, `A.difference(B)`, `A.symmetric_difference(B)`.

#### Modificacion

```python
s = {1, 2, 3}
s.add(4)         # {1, 2, 3, 4}
s.remove(2)      # {1, 3, 4}      ERROR si 2 no esta
s.discard(99)   # NO da error si no esta
s.update({5,6})  # {1,3,4,5,6}
s.clear()        # set()
```

#### Cuando usar set?

- **Eliminar duplicados** de una lista: `list(set(mi_lista))`.
- **Comprobar pertenencia** a alta velocidad.
- **Operaciones de conjuntos**: clientes que compraron A pero no B, palabras unicas en un texto, etc."""
    )},
    {"type": "md", "src": tu_turno(13,
        """Tienes dos listas con los lenguajes que conoce cada amigo:

```python
ana   = ['python', 'java', 'c++', 'sql', 'python']
pedro = ['python', 'go', 'rust', 'sql']
```

Usando **sets**, calcula:

1. Los lenguajes que conocen **los dos** (interseccion).
2. Los lenguajes que conoce Ana **pero no** Pedro (diferencia).
3. **Todos** los lenguajes distintos entre los dos (union).
4. Los lenguajes **unicos** que sabe Ana (sin duplicados)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nana   = ['python', 'java', 'c++', 'sql', 'python']\npedro = ['python', 'go', 'rust', 'sql']\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# ana   = ['python', 'java', 'c++', 'sql', 'python']\n# pedro = ['python', 'go', 'rust', 'sql']\n#\n# set_ana = set(ana)\n# set_pedro = set(pedro)\n#\n# print('Ambos:           ', set_ana & set_pedro)\n# print('Solo Ana:        ', set_ana - set_pedro)\n# print('Todos:           ', set_ana | set_pedro)\n# print('Unicos de Ana:   ', set_ana)\n"},
]))

# ============ SECUENCIAS ============
plan.append((ID_SECUENCIAS, [
    {"type": "md", "src": teoria(
        "Secuencias utiles: <code>range</code>, <code>enumerate</code>, <code>zip</code>",
        """Estas tres funciones devuelven **iteradores** (objetos por los que se puede recorrer una vez). Las usaras con `for` constantemente.

#### <code>range(start, stop, step)</code>: numeros en sucesion

```python
range(5)            # 0, 1, 2, 3, 4
range(2, 7)         # 2, 3, 4, 5, 6
range(0, 10, 2)     # 0, 2, 4, 6, 8
range(10, 0, -1)    # 10, 9, 8, ..., 1
```

> `range` NO genera la lista entera, genera los numeros uno a uno. Por eso `range(1_000_000_000)` no rompe tu RAM. Si necesitas la lista, hazle `list(range(...))`.

#### <code>enumerate(iterable)</code>: indice + valor

```python
fruits = ['manzana', 'pera', 'uva']
for i, fruta in enumerate(fruits):
    print(i, fruta)
# 0 manzana
# 1 pera
# 2 uva
```

Mucho mas elegante que:
```python
for i in range(len(fruits)):     # ANTI-PATTERN en Python
    print(i, fruits[i])
```

#### <code>zip(a, b, c, ...)</code>: emparejar varias listas

```python
nombres = ['Ana', 'Pedro', 'Lucia']
edades  = [30, 25, 35]

for nombre, edad in zip(nombres, edades):
    print(f'{nombre} tiene {edad}')
```

`zip` corta cuando se acaba el iterable mas corto.

#### Truco: 'desempaquetar' con <code>*</code> (unzip)

```python
parejas = [('Ana', 30), ('Pedro', 25), ('Lucia', 35)]
nombres, edades = zip(*parejas)
# nombres = ('Ana', 'Pedro', 'Lucia')
# edades  = (30, 25, 35)
```"""
    )},
    {"type": "md", "src": tu_turno(14,
        """Tienes dos listas paralelas con productos y sus precios:

```python
productos = ['pan', 'leche', 'huevos', 'queso']
precios   = [1.20, 0.95, 2.50, 4.30]
```

Usando `zip`, imprime cada producto junto a su precio en una linea con f-string como:

```
pan: 1.20 EUR
leche: 0.95 EUR
...
```

**Bonus:** usa tambien `enumerate` para anadir un numero de linea: `1) pan: 1.20 EUR`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nproductos = ['pan', 'leche', 'huevos', 'queso']\nprecios   = [1.20, 0.95, 2.50, 4.30]\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# productos = ['pan', 'leche', 'huevos', 'queso']\n# precios   = [1.20, 0.95, 2.50, 4.30]\n#\n# for prod, prec in zip(productos, precios):\n#     print(f'{prod}: {prec:.2f} EUR')\n#\n# # Bonus con enumerate:\n# for i, (prod, prec) in enumerate(zip(productos, precios), start=1):\n#     print(f'{i}) {prod}: {prec:.2f} EUR')\n"},
]))

# ============ DICCIONARIOS ============
plan.append((ID_DICTS, [
    {"type": "md", "src": teoria(
        "Diccionarios: la estructura mas potente de Python",
        """Un **diccionario** es una coleccion de **pares clave-valor**. Es como una agenda telefonica: das una clave (nombre) y obtienes el valor (telefono).

```python
persona = {
    'nombre': 'Lucas',
    'edad': 30,
    'ciudad': 'Madrid'
}

persona['nombre']    # 'Lucas'
```

#### Caracteristicas

| Propiedad | Detalle |
|---|---|
| **Acceso por clave** | No por indice. `d['nombre']`, no `d[0]`. |
| **Mutable** | Puedes anadir, modificar y quitar. |
| **Claves unicas** | Si pones dos veces la misma clave, solo queda la ultima. |
| **Claves hashables** | str, int, float, tuple... NO listas ni dicts. |
| **Ordenado (3.7+)** | Mantiene el orden de insercion. |
| **Acceso O(1)** | Buscar una clave es practicamente instantaneo. |

#### Cinco formas de crearlo

```python
d1 = {}                              # vacio
d2 = dict()                          # vacio
d3 = {'a': 1, 'b': 2}                # literal
d4 = dict(a=1, b=2)                  # con argumentos nombrados
d5 = dict([('a', 1), ('b', 2)])       # desde lista de tuplas
d6 = dict(zip(['a','b'], [1, 2]))      # uniendo dos listas
```

#### Operaciones esenciales

```python
d = {'a': 1, 'b': 2}

d['a']                # 1                    leer
d['c'] = 3            # anadir / modificar
del d['b']            # eliminar clave
'a' in d              # True                 existe?
len(d)                # 2

d.keys()              # dict_keys(['a', 'c'])
d.values()            # dict_values([1, 3])
d.items()             # dict_items([('a',1),('c',3)])

# Iterar
for k, v in d.items():
    print(k, v)

# Acceso seguro (NO da error si la clave no existe)
d.get('z')            # None
d.get('z', 0)         # 0   (valor por defecto)

# Anadir solo si no existe
d.setdefault('a', 99)  # 1   (ya existe, no la cambia)
d.setdefault('z', 99)  # 99  (la crea)
```

#### Cuando usar dict?

- **Mapear** una cosa a otra: id -> nombre, palabra -> traduccion, codigo -> precio.
- **Contar** ocurrencias (con `collections.Counter`).
- **Configuracion** flexible (en lugar de muchas variables).
- **JSON**: los JSON se cargan directamente como dicts en Python."""
    )},
]))

plan.append((ID_DICT_GET, [
    {"type": "md", "src": tu_turno(15,
        """Tienes este diccionario con las capitales:

```python
capitales = {
    'Espana': 'Madrid',
    'Francia': 'Paris',
    'Italia': 'Roma',
    'Alemania': 'Berlin'
}
```

Resuelve:

1. Imprime la capital de Italia.
2. Anade `'Portugal': 'Lisboa'` al diccionario.
3. Cambia la capital de Espana a `'Madrid (capital)'`.
4. Comprueba si `'Suecia'` esta en el dict (con `in`).
5. Recorre el dict e imprime cada par como: `Espana -> Madrid`.
6. Usa `.get(...)` para pedir la capital de Suecia con valor por defecto `'desconocida'`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\ncapitales = {\n    'Espana': 'Madrid',\n    'Francia': 'Paris',\n    'Italia': 'Roma',\n    'Alemania': 'Berlin'\n}\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# capitales = {'Espana':'Madrid','Francia':'Paris','Italia':'Roma','Alemania':'Berlin'}\n#\n# print(capitales['Italia'])\n# capitales['Portugal'] = 'Lisboa'\n# capitales['Espana'] = 'Madrid (capital)'\n# print('Suecia' in capitales)\n# for pais, cap in capitales.items():\n#     print(f'{pais} -> {cap}')\n# print(capitales.get('Suecia', 'desconocida'))\n"},
]))


enhance(NB, plan)
print("Done.")

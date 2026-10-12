"""Aplica mejoras al notebook 03_Control con bloques de colores y teoria detallada."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, solucion_md, dato, aviso
import json

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_03_Python101_Control.ipynb"

nb = json.load(open(NB, encoding="utf-8"))


def find_id(fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if fragment in src:
            return c["id"]
    return None


def find_id_startswith(prefix):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if src.lstrip().startswith(prefix):
            return c["id"]
    return None


# --- IDs clave ---
ID_TITULO          = nb["cells"][0]["id"]                                          # cell 0  imagen + titulo
ID_SELECCION       = find_id("Selecci")                                             # cell 2  intro a if
ID_IF_PRIMER       = find_id("Valor positivo")                                      # cell 3  primer ejemplo if/else
ID_ELIF_INTRO      = find_id("ramas' en sentencias condicionales")                  # cell 6  introducir elif
ID_ELIF_EJ         = find_id("Valor nulo")                                          # cell 7  ejemplo if/elif/else
ID_ANIDAMIENTO     = find_id("Anidamiento.")                                        # cell 8
ID_TERNARIO_INTRO  = find_id("Expresi") and find_id("ternaria")                     # cell 10
ID_TERNARIO_EJ     = find_id("c�lculo del valor absoluto")                          # cell 11 (puede no encontrarse por encoding)
if ID_TERNARIO_EJ is None:
    ID_TERNARIO_EJ = find_id("resultado = x if x >= 0 else -x")
ID_CONCAT_COMP     = find_id("Concatenaci") and find_id("comparaciones")            # cell 13
ID_BOOL_VAL        = find_id("Valor booleano")                                      # cell 18
ID_LISTA_VACIA     = find_id('Lista no vac')                                        # cell 20
ID_MATCH           = find_id("## Match")                                            # cell 21
ID_MATCH_GUARD     = find_id('"*guard*"')                                           # cell 27
ID_ITER_HEADER     = find_id("Iteraci") and find_id("(bucles)")                     # cell 30
ID_WHILE_INTRO     = find_id("Bucle 'while'")                                       # cell 31
ID_WHILE_EJ1       = find_id("Mostrar los primeros 3 objetos")                      # cell 32
ID_WHILE_INFINITE  = find_id("Bucle infinito")                                      # cell 35
ID_FOR_INTRO       = find_id("Bucle 'for'")                                         # cell 36
ID_FOR_PELIS       = find_id("peliculas = ['Matrix'")                               # cell 37
ID_FOR_RANGE_INTRO = find_id("counted loops")                                       # cell 38
ID_FOR_RANGE_EJ    = find_id("for i in range(10):\n    print(i)")                   # cell 39
ID_FOR_LEN         = find_id("range")
# Buscamos especificamente la celda con el ejemplo for letra in nombre
ID_FOR_LETRAS      = find_id("for letra in nombre")                                 # cell 42
ID_FOR_TUPLAS      = find_id("Iteraci") and find_id("tuplas")                       # cell 43
ID_FOR_DICT        = find_id("for key in diccionario.keys()")                       # cell 46
ID_FOR_DICT_VAL    = find_id("for value in diccionario.values()")                   # cell 49
ID_FOR_DESEMP      = find_id("for a, b, c in")                                      # cell 51
ID_BCE_HEADER      = find_id("sentencias break, continue y else")                   # cell 52
ID_BREAK_INTRO     = find_id("#### Break")                                          # cell 53
ID_BREAK_EJ        = find_id("rating_to_find")                                      # cell 54
ID_ELSE_INTRO      = find_id("#### Else")                                           # cell 55
ID_ELSE_EJ_FLAG    = find_id("Same, but with flag")                                 # cell 57
ID_CONTINUE_INTRO  = find_id("#### Continue")                                       # cell 58
ID_CONTINUE_EJ     = find_id("Si el n")                                             # cell 59 (numero es par)
ID_BREAK_NESTED    = find_id("for i in range(5):\n    for a in range(3):")          # cell 63
ID_LC_HEADER       = find_id("# List Comprehensions")                               # cell 64
ID_LC_INTRO        = find_id("Permiten construir listas")                           # cell 65
ID_LC_SINTAXIS     = find_id("[<expression> for <item>")                            # cell 66
ID_LC_EJ_BASIC     = find_id("char * 2 for char in")                                # cell 68
ID_LC_NO_USA_ITEM  = find_id("Com")
# busqueda mas precisa: celda que dice "Comunmente, el item de la sentencia"
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if "Com" in src and "el item de la sentencia" in src:
        ID_LC_NO_USA_ITEM = c["id"]
        break
ID_LC_FILTRO       = find_id("se puede especificar un filtro")
# Mejor: buscar celda que diga "obtener n�meros pares:"
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if src.strip().startswith("Ejemplo: obtener n"):
        ID_LC_FILTRO = c["id"]
        break
ID_LC_PARES        = find_id("[x for x in range(9) if x % 2 == 0]")                 # cell 75
ID_LC_COMPLETA     = find_id("### Versi") and find_id("completa")                   # cell 78
ID_LC_TERNARIA     = find_id("[0 if x % 2 == 0 else x for x in range(9)]")          # cell 80
ID_LC_ANIDAMIENTO  = find_id("### Anidamiento")                                     # cell 85
ID_LC_NESTED_EJ    = find_id("[(x, y) for x in lista_1 for y in lista_2]")          # cell 87
ID_LC_PROS         = find_id("Pros y contras")                                      # cell 88
ID_LC_OTROS        = find_id("Otros tipos de comprehensions")                       # cell 90
ID_DICT_COMP       = find_id("Dictionary comprehensions")                           # cell 91
ID_DICT_COMP_EJ    = find_id("d = {x: x*x")                                         # cell 92
ID_SET_COMP        = find_id("Set comprehensions")                                  # cell 95
ID_TUPLE_COMP      = find_id("Tuple comprehensions")                                # cell 97
ID_EXC_HEADER      = find_id("# Excepciones")                                       # cell 99
ID_EXC_INTRO       = find_id("Las excepciones son eventos")                         # cell 100
ID_TRY_INTRO       = find_id("#### Try/except")                                     # cell 101
ID_TRY_EJ_BASE     = find_id("lista[4]")                                            # cell 102
ID_TRY_EJ_INDEX    = find_id("IndexError")
# busca primera celda con "except IndexError"
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if "except IndexError" in src and "He capturado" in src:
        ID_TRY_EJ_INDEX = c["id"]
        break
ID_TRY_GENERIC     = find_id("4/0")
# celda con "except:" pelado
for c in nb["cells"]:
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if "4/0" in src and "except:" in src:
        ID_TRY_GENERIC = c["id"]
        break
ID_EXC_AS_E        = find_id("except Exception as e")                               # cell 107
ID_FINALLY_INTRO   = find_id("Try/finally")                                          # cell 108
ID_FINALLY_EJ      = find_id("Exception IndexError Captured")                       # cell 109
ID_RAISE_INTRO     = find_id("#### raise")                                          # cell 111
ID_RAISE_EJ        = find_id("indice >= len(lista)")                                # cell 112
ID_EJERCICIOS      = find_id("# Ejercicios")                                        # cell 113


# Sanity print
critical = {
    "TITULO": ID_TITULO, "SELECCION": ID_SELECCION, "IF_PRIMER": ID_IF_PRIMER,
    "ELIF_EJ": ID_ELIF_EJ, "TERNARIO_EJ": ID_TERNARIO_EJ, "BOOL_VAL": ID_BOOL_VAL,
    "MATCH": ID_MATCH, "WHILE_INTRO": ID_WHILE_INTRO, "WHILE_EJ1": ID_WHILE_EJ1,
    "FOR_INTRO": ID_FOR_INTRO, "FOR_PELIS": ID_FOR_PELIS, "FOR_DICT": ID_FOR_DICT,
    "BREAK_INTRO": ID_BREAK_INTRO, "ELSE_INTRO": ID_ELSE_INTRO,
    "CONTINUE_INTRO": ID_CONTINUE_INTRO, "BREAK_NESTED": ID_BREAK_NESTED,
    "LC_HEADER": ID_LC_HEADER, "LC_EJ_BASIC": ID_LC_EJ_BASIC,
    "LC_PARES": ID_LC_PARES, "LC_TERNARIA": ID_LC_TERNARIA,
    "LC_NESTED_EJ": ID_LC_NESTED_EJ, "DICT_COMP_EJ": ID_DICT_COMP_EJ,
    "EXC_HEADER": ID_EXC_HEADER, "TRY_EJ_INDEX": ID_TRY_EJ_INDEX,
    "EXC_AS_E": ID_EXC_AS_E, "FINALLY_INTRO": ID_FINALLY_INTRO,
    "RAISE_INTRO": ID_RAISE_INTRO, "EJERCICIOS": ID_EJERCICIOS,
}
for k, v in critical.items():
    if v is None:
        print(f"WARNING: ID {k} no encontrado!")


plan = []

# ============ INTRO al notebook ============
plan.append((ID_TITULO, [
    {"type": "md", "src": teoria(
        "Como leer este notebook (version mejorada)",
        """Este notebook fue **enriquecido** para ayudarte a aprender escribiendo codigo. Vas a encontrar tres tipos de bloques de colores:

<div style="background-color:#e7f5ff;border-left:6px solid #1c7ed6;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AZUL = TEORIA</b></div> -> explicacion en palabras simples antes de cada concepto.

<div style="background-color:#fff9db;border-left:6px solid #f59f00;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AMARILLO = TU TURNO</b></div> -> el ejercicio que TU debes resolver. Hay una celda vacia debajo donde escribes el codigo.

<div style="background-color:#ebfbee;border-left:6px solid #2f9e44;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>VERDE = SOLUCION</b></div> -> codigo de referencia comentado por si te trabas. Destapa solo despues de intentar.

> **Promesa importante**: el codigo y la teoria del profesor original no se han tocado. Solo se han ANADIDO bloques. Asi puedes seguir comparando con la version original cuando quieras.

#### Que veras en esta clase

Las **estructuras de control** son las que dictan **el flujo** de tu programa: cuando algo se ejecuta, cuando se repite y cuando se interrumpe. Sin ellas tu codigo seria una lista lineal de instrucciones rigida.

| Bloque | Para que sirve |
|---|---|
| `if / elif / else` | Tomar decisiones segun condiciones. |
| `match / case` | Comparar un valor contra muchos casos posibles. |
| `while` | Repetir mientras una condicion sea verdadera. |
| `for` | Recorrer todos los elementos de una secuencia. |
| `break / continue / else` | Modificar el flujo dentro de bucles. |
| List/Dict/Set comprehensions | Crear colecciones con un bucle compacto. |
| `try / except / finally / raise` | Capturar y lanzar errores sin que el programa muera. |"""
    )},
]))


# ============ SELECCION (if/elif/else) ============
plan.append((ID_SELECCION, [
    {"type": "md", "src": teoria(
        "if / elif / else: tomar decisiones",
        """La sentencia `if` ejecuta un bloque de codigo **solo cuando una condicion se cumple**. Es la herramienta de toma de decisiones mas basica.

#### Sintaxis general

```python
if condicion_1:
    # codigo si condicion_1 es True
elif condicion_2:
    # codigo si condicion_1 es False y condicion_2 es True
elif condicion_3:
    # codigo si las anteriores son False y condicion_3 es True
else:
    # codigo si NINGUNA de las condiciones anteriores se cumple
```

#### Reglas clave

| Regla | Detalle |
|---|---|
| Indentacion | El bloque dentro del `if` se delimita por **sangria** (4 espacios). Sin sangria, no es parte del `if`. |
| Dos puntos | Cada cabecera (`if`, `elif`, `else`) termina en `:`. |
| `elif` opcional | Puedes tener 0, 1, 2 o N `elif`. |
| `else` opcional | Como mucho UN `else`, al final. |
| Solo se ejecuta UNA rama | En cuanto una condicion da True, las demas se ignoran. |

#### Que tipos de datos acepta una condicion?

**Cualquier expresion** que pueda evaluarse a `True` o `False`. Esto incluye:

- Comparaciones: `x > 5`, `nombre == 'Lucas'`, `dato is None`.
- Booleanos: `True`, `False`, `flag`, `not flag`.
- Operadores logicos: `a > 0 and b > 0`, `x == 1 or x == 2`.
- Pertenencia: `letra in 'aeiou'`, `5 in lista`.
- **Cualquier objeto** (Python lo convierte a bool): un numero (0 = False, distinto de 0 = True), una cadena (vacia = False, no vacia = True), una lista (vacia = False, no vacia = True), `None` = False.

#### Trampas comunes

```python
if x = 5:           # ERROR: '=' es asignacion. Usa '==' para comparar
if (x > 0):         # funciona, pero los parentesis NO son necesarios
if x > 0 :          # funciona, espacio antes de ':' permitido pero feo
```"""
    )},
]))

plan.append((ID_IF_PRIMER, [
    {"type": "md", "src": tu_turno(1,
        """Pide un numero al usuario con `input(...)` (recuerda convertirlo a `int`). Despues:

- Si es **mayor que 0**, imprime `Es positivo`.
- Si es **menor que 0**, imprime `Es negativo`.
- Si es **exactamente 0**, imprime `Es cero`.

Usa `if`, `elif` y `else`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# n = int(input('Dame un numero: '))\n# if n > 0:\n#     print('Es positivo')\n# elif n < 0:\n#     print('Es negativo')\n# else:\n#     print('Es cero')\n"},
]))

plan.append((ID_ELIF_EJ, [
    {"type": "md", "src": tu_turno(2,
        """Crea una variable `nota = 7.5` y construye un programa que imprima la calificacion textual segun el rango:

| Nota | Texto |
|---|---|
| `< 5` | `Suspenso` |
| `>= 5 y < 7` | `Aprobado` |
| `>= 7 y < 9` | `Notable` |
| `>= 9 y <= 10` | `Sobresaliente` |
| Otro caso | `Nota invalida` |

Usa `if / elif / else`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nnota = 7.5\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# nota = 7.5\n# if nota < 0 or nota > 10:\n#     print('Nota invalida')\n# elif nota < 5:\n#     print('Suspenso')\n# elif nota < 7:\n#     print('Aprobado')\n# elif nota < 9:\n#     print('Notable')\n# else:\n#     print('Sobresaliente')\n"},
]))

plan.append((ID_ANIDAMIENTO, [
    {"type": "md", "src": dato(
        """**Anidar `if` dentro de `if`** es valido pero suele empeorar la legibilidad. Si te encuentras con 3 o mas niveles de anidamiento, considera:

1. Usar **operadores logicos** (`and`, `or`) para combinar condiciones en una sola.
2. Usar **early return** dentro de funciones (terminar pronto los casos faltantes).
3. Usar `continue` para casos negativos en bucles.

Ejemplo: este codigo anidado...
```python
if val > 0:
    if val < 100:
        print('positivo')
    else:
        print('muy positivo')
```
...es equivalente a esto, mas plano:
```python
if 0 < val < 100:
    print('positivo')
elif val >= 100:
    print('muy positivo')
```"""
    )},
]))


# ============ TERNARIO ============
if ID_TERNARIO_EJ:
    plan.append((ID_TERNARIO_EJ, [
        {"type": "md", "src": teoria(
            "Expresion ternaria (if-else en una linea)",
            """La sintaxis ternaria de Python condensa un `if/else` en **una sola linea** y devuelve un valor:

```python
valor = expr_si_True if condicion else expr_si_False
```

Compara:
```python
# Forma larga
if x >= 0:
    abs_x = x
else:
    abs_x = -x

# Forma ternaria
abs_x = x if x >= 0 else -x
```

#### Cuando usarla

- Para **asignar un valor** simple basado en una condicion.
- Cuando el codigo ocupa una sola linea y es legible.

#### Cuando NO usarla

- Si tienes mas de un `else if` (concatenar ternarios se lee fatal).
- Si las expresiones son largas o tienen efectos secundarios.

#### Trampa habitual

El orden es **valor_si_True PRIMERO**, luego `if`, luego `else`. NO es como en C/Java:
```python
# Python
y = 1 if x > 0 else -1

# C / Java (NO es Python)
y = (x > 0) ? 1 : -1
```"""
        )},
        {"type": "md", "src": tu_turno(3,
            """Tienes una variable `temperatura = 22`. Usando una **expresion ternaria** en UNA sola linea, asigna a `mensaje` el texto:
- `'Calor'` si la temperatura es **mayor o igual que 25**.
- `'Templado'` en cualquier otro caso.

Imprime el resultado.

**Bonus:** repite el ejercicio anidando dos ternarias para tres rangos: `'Frio'` (< 15), `'Templado'` (entre 15 y 24) y `'Calor'` (>= 25)."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\ntemperatura = 22\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# temperatura = 22\n# mensaje = 'Calor' if temperatura >= 25 else 'Templado'\n# print(mensaje)\n#\n# # Bonus con dos ternarias anidadas:\n# mensaje = 'Frio' if temperatura < 15 else ('Templado' if temperatura < 25 else 'Calor')\n# print(mensaje)\n"},
    ]))


# ============ Concatenacion de comparaciones ============
if ID_CONCAT_COMP:
    plan.append((ID_CONCAT_COMP, [
        {"type": "md", "src": teoria(
            "Combinar comparaciones con and / or / not",
            """Para escribir una condicion compuesta, conectas comparaciones con **operadores logicos**:

| Operador | Significado | Resultado True cuando... |
|---|---|---|
| `and` | y | LAS DOS comparaciones son True |
| `or` | o | AL MENOS UNA comparacion es True |
| `not` | no | la comparacion es False |

```python
edad = 25
es_mayor = edad >= 18 and edad < 65        # True
es_extremo = edad < 18 or edad >= 65        # False
no_adulto = not (edad >= 18)                # False
```

#### Atajo: comparaciones encadenadas

Python permite escribir intervalos de forma **matematica natural**:
```python
if 0 < x < 100:        # equivale a:  0 < x and x < 100
    ...

if 'a' <= letra <= 'z':
    ...
```

#### Cortocircuito (importante)

Python NO evalua lo que ya no necesita:
```python
if x is not None and x > 0:    # si x es None, la 2a parte NO se evalua
    ...
```
Esto te permite poner una **comprobacion de seguridad primero** sin que la segunda comparacion explote."""
        )},
        {"type": "md", "src": tu_turno(4,
            """Tienes tres variables: `genero = 'Comedia'`, `anio = 2005`, `duracion = 95` (minutos). Imprime `'Te puede gustar'` si **TODAS** estas condiciones se cumplen:

1. El genero es `'Comedia'` o `'Accion'`.
2. El anio es **mayor o igual a 2000**.
3. La duracion es **menor o igual a 120**.

Si falla alguna condicion, imprime `'No es para ti'`. Usa una sola sentencia `if / else` con `and` y `or`."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\ngenero = 'Comedia'\nanio = 2005\nduracion = 95\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# genero = 'Comedia'\n# anio = 2005\n# duracion = 95\n#\n# if (genero == 'Comedia' or genero == 'Accion') and anio >= 2000 and duracion <= 120:\n#     print('Te puede gustar')\n# else:\n#     print('No es para ti')\n"},
    ]))


# ============ Valor booleano ============
plan.append((ID_BOOL_VAL, [
    {"type": "md", "src": teoria(
        "Truthiness: cualquier objeto se puede usar como condicion",
        """En Python NO necesitas comparar contra `True` o `False` cuando el propio objeto ya tiene un valor de verdad implicito. Esto se llama **truthiness**.

#### Valores que se consideran <b>False</b> (falsy)

- `False`, `None`
- `0`, `0.0`, `0j` (cero numerico de cualquier tipo)
- `''`, `""` (string vacio)
- `[]`, `()`, `{}`, `set()` (cualquier coleccion vacia)
- Objetos que definen `__bool__` para devolver False

#### Todo lo demas es <b>True</b> (truthy)

Un string con un solo espacio (`' '`) es True. La cadena `'False'` (texto, no booleano) es True. La lista `[0]` es True (no esta vacia, aunque su unico elemento sea 0).

#### Idioma pythonico

```python
# Verboso (anti-pattern)
if len(lista) > 0:
    ...
if mi_string != '':
    ...
if x is not None and x != 0:
    ...

# Pythonico
if lista:
    ...
if mi_string:
    ...
if x:
    ...
```

#### Cuidado: NO siempre quieres truthiness

Si te importa **distinguir entre `0` y `None`**, NO uses `if x:` (los dos son falsy). Usa `if x is None:` o `if x is not None:`. Ejemplo: una funcion que recibe un descuento opcional, donde `0` significa 'sin descuento' y `None` significa 'no se especifico'."""
    )},
]))

plan.append((ID_LISTA_VACIA, [
    {"type": "md", "src": tu_turno(5,
        """Crea una funcion `describe(valor)` que reciba cualquier objeto e imprima:

- `'Vacio o falso'` si el valor es **falsy**.
- `'Tiene contenido'` en cualquier otro caso.

Pruebala con: `0`, `None`, `''`, `[]`, `'hola'`, `[0]`, `{'a': 1}`, `False`, `True`, `' '` (espacio).

Veras que `[0]` y `' '` cuentan como **truthy** (no son colecciones vacias).
"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def describe(valor):\n#     if valor:\n#         print('Tiene contenido ->', repr(valor))\n#     else:\n#         print('Vacio o falso  ->', repr(valor))\n#\n# for v in [0, None, '', [], 'hola', [0], {'a': 1}, False, True, ' ']:\n#     describe(v)\n"},
]))


# ============ MATCH ============
plan.append((ID_MATCH, [
    {"type": "md", "src": teoria(
        "match/case: comparar un valor contra muchos casos",
        """El `match` (Python 3.10+) es una estructura de control que **compara una variable contra varios patrones** y ejecuta el bloque del primero que coincida.

#### Sintaxis basica

```python
match valor:
    case patron_1:
        # codigo si valor coincide con patron_1
    case patron_2:
        # codigo si valor coincide con patron_2
    case _:
        # codigo si NADA coincide (caso por defecto, opcional)
```

El guion bajo `_` es el **comodin**: coincide con cualquier cosa.

#### Por que existe?

Con muchos `if/elif/elif/...` el codigo se hace pesado y repetitivo. `match` es:
- Mas legible para muchas alternativas.
- Mas potente porque permite **patrones estructurales** (tuplas, dicts, clases).

#### Capacidades extra

```python
case 'A' | 'B' | 'C':       # un patron multiple (OR)
case (0, 0):                  # patron de tupla literal
case (x, 0):                  # tupla con primera variable libre
case {'nombre': n}:           # dict con clave 'nombre' (n captura el valor)
case [primero, *resto]:       # lista no vacia
case val if val > 0:          # patron con guard
```

#### Avisos importantes

- Solo Python 3.10+. Versiones viejas dan SyntaxError.
- NO sustituye totalmente al `if/elif`: para condiciones complejas (multiples variables, rangos numericos, etc.) sigue siendo mas claro `if/elif`."""
    )},
]))

if ID_MATCH_GUARD:
    plan.append((ID_MATCH_GUARD, [
        {"type": "md", "src": tu_turno(6,
            """Escribe una funcion `dia_tipo(d)` que reciba un string corto representando el dia (`'L'`, `'M'`, `'X'`, `'J'`, `'V'`, `'S'`, `'D'`) y use **`match/case`** para devolver:

- `'Laborable'` si es L, M, X, J o V.
- `'Fin de semana'` si es S o D.
- `'Desconocido'` en cualquier otro caso.

Pista: usa el patron multiple `case 'L' | 'M' | 'X' | 'J' | 'V':`.

Pruebala con: `'L'`, `'D'`, `'Z'`."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# def dia_tipo(d):\n#     match d:\n#         case 'L' | 'M' | 'X' | 'J' | 'V':\n#             return 'Laborable'\n#         case 'S' | 'D':\n#             return 'Fin de semana'\n#         case _:\n#             return 'Desconocido'\n#\n# print(dia_tipo('L'))\n# print(dia_tipo('D'))\n# print(dia_tipo('Z'))\n"},
    ]))


# ============ ITERACION (intro) ============
if ID_ITER_HEADER:
    plan.append((ID_ITER_HEADER, [
        {"type": "md", "src": teoria(
            "Bucles: repetir un bloque de codigo",
            """Un **bucle** ejecuta un mismo bloque de codigo varias veces. Python tiene dos tipos de bucle:

| Bucle | Cuando lo usas |
|---|---|
| `while` | Cuando NO sabes cuantas veces vas a iterar. La iteracion termina cuando una condicion deja de ser True. |
| `for` | Cuando vas a recorrer una secuencia (lista, string, range, dict, etc.). |

#### Anatomia general

```python
while condicion:
    # cuerpo (se repite mientras condicion sea True)

for elemento in iterable:
    # cuerpo (se ejecuta una vez por cada elemento)
```

#### Tres palabras clave que modifican el flujo

- `break` -> sale del bucle inmediatamente.
- `continue` -> salta a la siguiente iteracion (ignora el resto del cuerpo).
- `else` -> bloque que se ejecuta solo si el bucle termina **sin break**. Es raro pero util.

Veras los tres con detalle mas abajo."""
        )},
    ]))


# ============ WHILE ============
plan.append((ID_WHILE_INTRO, [
    {"type": "md", "src": teoria(
        "while: repetir mientras una condicion sea verdadera",
        """`while` es el bucle **condicional**. Repite el cuerpo **mientras** la condicion siga siendo True.

```python
while condicion:
    # cuerpo del bucle
```

#### Anatomia tipica

Casi todo `while` sigue este patron:

1. **Inicializar** una variable de control antes del bucle.
2. **Comprobar** la condicion en la cabecera.
3. **Modificar** la variable dentro del cuerpo (para que en algun momento la condicion sea False).

```python
i = 0                    # 1) inicializar
while i < 5:             # 2) comprobar
    print(i)
    i += 1               # 3) modificar -> sin esto, bucle infinito!
```

#### Cuando elegir while en lugar de for

- Cuando el numero de iteraciones **depende de una condicion** (no de una secuencia).
- Cuando la condicion incluye **input del usuario** (esperar a que escriba algo correcto).
- Cuando **lees un archivo o stream** hasta que se acaba.

#### Trampa #1: bucle infinito

Si **olvidas modificar la variable** que controla la condicion, el bucle nunca termina:
```python
i = 0
while i < 5:
    print(i)         # i NUNCA cambia -> bucle infinito
```
**Como salir de un bucle infinito en Jupyter:** menu Kernel -> Interrupt o el cuadrado negro de la barra.

#### Trampa #2: off-by-one

```python
i = 1
while i <= 10:   # imprime 1..10
    print(i)
    i += 1

i = 1
while i < 10:    # imprime 1..9 (un numero menos!)
    print(i)
    i += 1
```"""
    )},
]))

plan.append((ID_WHILE_EJ1, [
    {"type": "md", "src": tu_turno(7,
        """Pide al usuario un numero positivo con `input(...)` y, usando un **`while`**, valida que efectivamente sea positivo. Si introduce un numero <= 0, vuelve a pedirlo. Cuando reciba un numero positivo, imprime `Gracias, recibido X`.

> Pista: usa una variable `n` y un `while n <= 0:` con `int(input(...))` dentro."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# n = int(input('Numero positivo: '))\n# while n <= 0:\n#     print('No es positivo, prueba otra vez.')\n#     n = int(input('Numero positivo: '))\n# print(f'Gracias, recibido {n}')\n"},
]))

plan.append((ID_WHILE_INFINITE, [
    {"type": "md", "src": aviso(
        """Esta celda contiene un bucle **potencialmente infinito**. Si la ejecutas tal cual, descomentando la linea sin la solucion, **tu kernel se quedara colgado**.

Para detenerlo:
- En Jupyter Lab/Notebook: menu **Kernel -> Interrupt** o boton del cuadrado negro.
- En linea de comandos: **Ctrl+C**.

Para evitar bucles infinitos:
1. Asegurate SIEMPRE de modificar la variable de control dentro del cuerpo.
2. Anade una condicion de salida con `break` (por ejemplo, un contador maximo)."""
    )},
    {"type": "md", "src": tu_turno(8,
        """Escribe un bucle `while True:` que pida al usuario un numero. **Termina** el bucle cuando el usuario escriba `'salir'`. En cualquier otro caso, imprime el doble del numero introducido.

> Pista: usa `break` para salir cuando entrada == 'salir'. Convierte a int **solo si** no es 'salir'."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# while True:\n#     entrada = input('Numero (o salir): ')\n#     if entrada == 'salir':\n#         break\n#     try:\n#         n = int(entrada)\n#         print('Doble:', n * 2)\n#     except ValueError:\n#         print('No es un numero, intenta de nuevo.')\n"},
]))


# ============ FOR ============
plan.append((ID_FOR_INTRO, [
    {"type": "md", "src": teoria(
        "for: recorrer cualquier iterable",
        """`for` es el bucle **mas pythonico** para recorrer una coleccion. La sintaxis es:

```python
for variable in iterable:
    # cuerpo (se ejecuta una vez por cada elemento)
```

En cada vuelta, `variable` toma el siguiente elemento del iterable.

#### Que es 'iterable'?

Un **iterable** es cualquier objeto que se pueda recorrer. Incluye:

| Iterable | Ejemplo |
|---|---|
| Lista | `[1, 2, 3]` |
| Tupla | `(1, 2, 3)` |
| String | `'abc'` (recorre caracter a caracter) |
| Set | `{1, 2, 3}` |
| Dict | `{'a': 1}` (recorre las CLAVES por defecto) |
| `range(...)` | `range(10)` |
| Archivos | `open('f.txt')` (recorre lineas) |
| Generadores | cualquier funcion con `yield` |

#### Comparacion rapida con while

```python
# Recorrer una lista con while (verboso, anti-pattern)
i = 0
while i < len(lista):
    print(lista[i])
    i += 1

# Recorrer una lista con for (pythonico)
for elemento in lista:
    print(elemento)
```

#### Convencion para variables 'usar y tirar'

Si NO necesitas el valor en cada iteracion, usa **`_`** como nombre:
```python
for _ in range(5):       # 'no me importa el valor, solo iterar 5 veces'
    print('hola')
```"""
    )},
]))

plan.append((ID_FOR_PELIS, [
    {"type": "md", "src": tu_turno(9,
        """Tienes la lista:
```python
peliculas = ['Matrix', 'The Purge', 'Avatar', 'Star Wars']
```

Usando un `for`, imprime cada pelicula con su numero de orden, asi:
```
1. Matrix
2. The Purge
3. Avatar
4. Star Wars
```

> Pista: necesitas una variable contador o usa `enumerate(peliculas, start=1)` (mas pythonico)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\npeliculas = ['Matrix', 'The Purge', 'Avatar', 'Star Wars']\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# peliculas = ['Matrix', 'The Purge', 'Avatar', 'Star Wars']\n#\n# # Opcion 1 (manual):\n# i = 1\n# for p in peliculas:\n#     print(f'{i}. {p}')\n#     i += 1\n#\n# # Opcion 2 (pythonica con enumerate):\n# for i, p in enumerate(peliculas, start=1):\n#     print(f'{i}. {p}')\n"},
]))


# ============ FOR + RANGE ============
plan.append((ID_FOR_RANGE_INTRO, [
    {"type": "md", "src": teoria(
        "range: numeros en sucesion para los for 'contados'",
        """`range(...)` produce una **secuencia de enteros** sin generarlos todos en memoria. Es la herramienta ideal para hacer un bucle un **numero exacto** de veces.

#### Tres firmas

```python
range(stop)                # 0, 1, 2, ..., stop-1
range(start, stop)         # start, start+1, ..., stop-1
range(start, stop, step)   # start, start+step, ..., < stop
```

> El **stop NUNCA se incluye**. Es el limite SUPERIOR exclusivo.

#### Ejemplos

```python
list(range(5))             # [0, 1, 2, 3, 4]
list(range(2, 7))          # [2, 3, 4, 5, 6]
list(range(0, 10, 2))      # [0, 2, 4, 6, 8]      pares menores que 10
list(range(10, 0, -1))     # [10, 9, 8, ..., 1]   cuenta atras
list(range(0, 10, 3))      # [0, 3, 6, 9]
```

#### Por que NO es una lista

`range(...)` NO devuelve una lista, devuelve un **objeto perezoso** que va generando los numeros uno a uno cuando los pides. Eso significa que `range(1_000_000_000)` ocupa unos pocos bytes en memoria, mientras que `list(range(1_000_000_000))` te llenaria la RAM.

Cuando necesitas la lista de verdad, usa `list(range(...))`.

#### Anti-pattern: for i in range(len(...))

```python
# Anti-pattern: solo necesitas el indice si vas a hacer cosas raras
for i in range(len(lista)):
    print(lista[i])

# Pythonico cuando solo te interesa el valor
for elemento in lista:
    print(elemento)

# Pythonico cuando necesitas indice + valor
for i, elemento in enumerate(lista):
    print(i, elemento)
```"""
    )},
]))

plan.append((ID_FOR_RANGE_EJ, [
    {"type": "md", "src": tu_turno(10,
        """Resuelve los tres apartados con `for` + `range`:

1. Imprime los numeros del **1 al 10** (incluido el 10).
2. Imprime los **multiplos de 5** entre 0 y 50, incluido el 50.
3. Imprime una **cuenta atras** del 10 al 1 (en orden descendente).

Cada apartado en celda visible separada con un titulo `print('--- 1 ---')`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# print('--- 1 ---')\n# for i in range(1, 11):\n#     print(i)\n#\n# print('--- 2 ---')\n# for i in range(0, 51, 5):\n#     print(i)\n#\n# print('--- 3 ---')\n# for i in range(10, 0, -1):\n#     print(i)\n"},
]))


# ============ FOR sobre dict ============
plan.append((ID_FOR_DICT, [
    {"type": "md", "src": teoria(
        "Recorrer un diccionario con for",
        """Un diccionario es iterable, pero por defecto **te da las CLAVES**, no los pares completos. Hay tres formas:

| Codigo | Que recorres |
|---|---|
| `for k in d:` | Solo las claves (igual que `d.keys()`). |
| `for v in d.values():` | Solo los valores. |
| `for k, v in d.items():` | Pares clave-valor (lo mas usado). |

#### Ejemplo

```python
precios = {'pan': 1.2, 'leche': 0.95, 'queso': 4.3}

for producto in precios:
    print(producto)
# pan
# leche
# queso

for precio in precios.values():
    print(precio)
# 1.2
# 0.95
# 4.3

for producto, precio in precios.items():
    print(f'{producto}: {precio} EUR')
# pan: 1.2 EUR
# leche: 0.95 EUR
# queso: 4.3 EUR
```

#### Modificar el dict mientras se itera: NO

```python
for k in d:
    if d[k] == 0:
        del d[k]    # RuntimeError: dictionary changed size during iteration
```
La solucion: itera sobre una **copia** de las claves: `for k in list(d.keys())`."""
    )},
]))

if ID_FOR_DICT_VAL:
    plan.append((ID_FOR_DICT_VAL, [
        {"type": "md", "src": tu_turno(11,
            """Tienes este dict de calificaciones:
```python
notas = {'Maria': 7.5, 'Pedro': 4.8, 'Lucia': 9.1, 'Juan': 5.0}
```

Usando un solo bucle `for ... in notas.items():`, imprime una linea por persona como:
```
Maria saco 7.5  -> Aprobado
Pedro saco 4.8  -> Suspenso
...
```
La regla es: si la nota es **>= 5** -> `Aprobado`, en otro caso -> `Suspenso`.

**Bonus:** despues del bucle, imprime la nota MEDIA. Pista: `sum(notas.values()) / len(notas)`."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\nnotas = {'Maria': 7.5, 'Pedro': 4.8, 'Lucia': 9.1, 'Juan': 5.0}\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# notas = {'Maria': 7.5, 'Pedro': 4.8, 'Lucia': 9.1, 'Juan': 5.0}\n#\n# for nombre, nota in notas.items():\n#     estado = 'Aprobado' if nota >= 5 else 'Suspenso'\n#     print(f'{nombre} saco {nota}  -> {estado}')\n#\n# media = sum(notas.values()) / len(notas)\n# print(f'Media: {media:.2f}')\n"},
    ]))


# ============ DESEMPAQUETADO en for ============
if ID_FOR_DESEMP:
    plan.append((ID_FOR_DESEMP, [
        {"type": "md", "src": dato(
            """**Desempaquetado en la cabecera del `for`**

Cuando el iterable contiene tuplas (o listas) de tamano fijo, puedes desempaquetar **en la propia cabecera**:

```python
# En lugar de esto:
for tupla in [(1, 2, 3), (4, 5, 6)]:
    a = tupla[0]
    b = tupla[1]
    c = tupla[2]
    print(a, b, c)

# Hazlo asi:
for a, b, c in [(1, 2, 3), (4, 5, 6)]:
    print(a, b, c)
```

Esto se usa muchisimo con:
- `enumerate(...)` -> `for i, valor in enumerate(lista):`
- `dict.items()` -> `for k, v in d.items():`
- `zip(...)` -> `for a, b in zip(lista1, lista2):`"""
        )},
    ]))


# ============ BREAK ============
plan.append((ID_BREAK_INTRO, [
    {"type": "md", "src": teoria(
        "break: salir de un bucle de inmediato",
        """`break` interrumpe el bucle **inmediatamente**, sin importar cuantas iteraciones queden. El programa continua con la primera linea **despues del bucle**.

```python
for x in lista:
    if x == objetivo:
        print('encontrado!')
        break          # sale del for
print('siguiente codigo despues del bucle')
```

#### Casos tipicos de uso

1. **Buscar** un elemento y parar al encontrarlo (no malgastar iteraciones).
2. Salir de un `while True:` cuando se cumple una condicion.
3. Detener un proceso cuando se acaba el tiempo o se encuentra un error.

#### Trampa: solo afecta al bucle MAS INTERNO

Si tienes bucles anidados, `break` solo sale del bucle en el que esta:

```python
for i in range(3):
    for j in range(3):
        if j == 1:
            break       # sale del 'for j', NO del 'for i'
    # aqui llegan las siguientes iteraciones de i
```

Para salir de varios bucles a la vez, lo mas limpio es **mover el codigo a una funcion** y usar `return`:

```python
def buscar(matriz, objetivo):
    for fila in matriz:
        for v in fila:
            if v == objetivo:
                return True   # sale de las DOS por completo
    return False
```"""
    )},
]))

plan.append((ID_BREAK_EJ, [
    {"type": "md", "src": tu_turno(12,
        """Tienes una lista de numeros:
```python
numeros = [3, 7, 1, 8, 5, 12, 6, 2]
```

Usando `for` + `break`, encuentra **el primer numero mayor o igual a 10** y guardalo en una variable `encontrado`. Imprime el resultado. Si no hubiera ninguno, imprime `'no hay'`.

> Pista: inicializa `encontrado = None` antes del for. Asigna y rompe en cuanto lo halles. Despues del bucle, comprueba si sigue siendo None."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nnumeros = [3, 7, 1, 8, 5, 12, 6, 2]\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# numeros = [3, 7, 1, 8, 5, 12, 6, 2]\n# encontrado = None\n# for n in numeros:\n#     if n >= 10:\n#         encontrado = n\n#         break\n#\n# if encontrado is None:\n#     print('no hay')\n# else:\n#     print('Primer numero >= 10:', encontrado)\n"},
]))


# ============ ELSE en bucles ============
plan.append((ID_ELSE_INTRO, [
    {"type": "md", "src": teoria(
        "for/while con else: el truco poco conocido",
        """Los bucles en Python admiten una clausula `else` opcional. **Pero NO funciona como crees**:

> El bloque `else` se ejecuta SOLO si el bucle termina **sin haber encontrado un `break`**.

```python
for x in iterable:
    if condicion:
        break
else:
    # se ejecuta si SE TERMINO el iterable SIN break
    ...
```

Es decir: el `else` significa **'no encontre lo que buscaba'**. Por eso muchos programadores lo encuentran confuso (mejor nombre seria `nobreak`).

#### Caso de uso clasico: busqueda con confirmacion

```python
for elemento in lista:
    if elemento == buscado:
        print('Lo encontre!')
        break
else:
    print('No esta en la lista.')
```

Sin `else`, tendrias que usar una **bandera (flag)**:
```python
encontrado = False
for elemento in lista:
    if elemento == buscado:
        encontrado = True
        break
if not encontrado:
    print('No esta en la lista.')
```

Las dos versiones funcionan, la primera es mas compacta. Usala cuando la veas, pero **deja un comentario** que explique que hace, porque mucha gente la lee mal."""
    )},
]))

plan.append((ID_ELSE_EJ_FLAG, [
    {"type": "md", "src": tu_turno(13,
        """Reescribe el ejercicio anterior usando `for ... else` (sin variable bandera):

Dada `lista = [10, 20, 30, 40]` y `buscado = 25`, escribe un `for` que recorra la lista y use `break` cuando encuentre el valor. En el `else` del for, imprime `'No encontrado'`. Si lo encuentra, imprime `'Encontrado!'` antes del break.

Pruebalo cambiando `buscado` a `30` para ver el caso del Encontrado."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nlista = [10, 20, 30, 40]\nbuscado = 25\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# lista = [10, 20, 30, 40]\n# buscado = 25\n#\n# for elemento in lista:\n#     if elemento == buscado:\n#         print('Encontrado!')\n#         break\n# else:\n#     print('No encontrado')\n"},
]))


# ============ CONTINUE ============
plan.append((ID_CONTINUE_INTRO, [
    {"type": "md", "src": teoria(
        "continue: saltar a la siguiente iteracion",
        """`continue` **descarta el resto del cuerpo** del bucle en la iteracion actual y salta directamente a la siguiente.

```python
for x in iterable:
    if no_me_interesa(x):
        continue           # salta al siguiente x
    procesar(x)
```

#### Cuando es util

- **Filtrar** elementos sin aumentar la profundidad de anidamiento.
- Poner las **comprobaciones de exclusion** al principio del bucle (estilo 'guard clause').

#### Comparacion: con vs sin continue

```python
# Sin continue (con if anidado)
for n in numeros:
    if n > 0:
        if n % 2 == 0:
            print(n)

# Con continue (mas plano y legible)
for n in numeros:
    if n <= 0:
        continue
    if n % 2 != 0:
        continue
    print(n)
```

#### Trampa: no olvidarte de avanzar dentro de un while

En `for`, `continue` simplemente avanza el iterable. **Pero en `while`, si tu variable de control se modifica DESPUES del filtrado, `continue` puede crear un bucle infinito:**

```python
i = 0
while i < 10:
    if i == 5:
        continue       # i SIGUE siendo 5, no avanza -> BUCLE INFINITO
    print(i)
    i += 1
```
Solucion: incrementa `i` ANTES del `continue` o usa `for`."""
    )},
]))

plan.append((ID_CONTINUE_EJ, [
    {"type": "md", "src": tu_turno(14,
        """Recorre los numeros del 1 al 30 con `for ... in range(1, 31)`. Usando `continue`, salta:

- Los **multiplos de 3** (`n % 3 == 0`).
- Los numeros mayores que 20.

Imprime los numeros que **sobreviven** a los filtros y, al final, imprime cuantos quedaron (con un contador)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# contador = 0\n# for n in range(1, 31):\n#     if n % 3 == 0:\n#         continue\n#     if n > 20:\n#         continue\n#     print(n)\n#     contador += 1\n# print('Total:', contador)\n"},
]))


# ============ BUCLES ANIDADOS ============
plan.append((ID_BREAK_NESTED, [
    {"type": "md", "src": dato(
        """**Bucles anidados y break**

Recordatorio importante: `break` solo sale del bucle **mas cercano** que lo contiene. Si necesitas salir de varios bucles a la vez, las opciones son:

1. **Encapsular en una funcion** y usar `return`:
   ```python
   def buscar(matriz, x):
       for fila in matriz:
           for v in fila:
               if v == x:
                   return True
       return False
   ```

2. **Usar una bandera**:
   ```python
   salir = False
   for i in range(N):
       for j in range(M):
           if condicion:
               salir = True
               break
       if salir:
           break
   ```

3. **Aplanar los bucles** con `itertools.product`:
   ```python
   from itertools import product
   for i, j in product(range(N), range(M)):
       if condicion:
           break        # un solo bucle, un solo break
   ```"""
    )},
]))


# ============ LIST COMPREHENSIONS ============
plan.append((ID_LC_HEADER, [
    {"type": "md", "src": teoria(
        "List comprehensions: el atajo mas pythonico",
        """Una **list comprehension** es una forma compacta de **construir una lista** aplicando una expresion a cada elemento de un iterable. Es el equivalente a un `for + append`, pero en una linea.

#### Las tres formas

```python
# 1) Basica:        [expr  for item in iterable]
[x * 2 for x in range(5)]
# -> [0, 2, 4, 6, 8]

# 2) Con filtro:    [expr  for item in iterable  if condicion]
[x for x in range(20) if x % 2 == 0]
# -> [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# 3) Con ternaria:  [expr_T if cond else expr_F  for item in iterable]
[x if x > 0 else 0 for x in [-2, -1, 0, 1, 2]]
# -> [0, 0, 0, 1, 2]
```

#### Comparacion

```python
# Bucle clasico
cuadrados = []
for x in range(10):
    cuadrados.append(x ** 2)

# List comprehension
cuadrados = [x ** 2 for x in range(10)]
```

#### Cuando NO usarlas

| Situacion | Mejor opcion |
|---|---|
| El cuerpo del bucle es muy largo o tiene varias instrucciones | `for` clasico |
| Hay 3 o mas `for` anidados | `for` clasico (la legibilidad cae en picado) |
| Necesitas efectos secundarios (`print`, `append` a otra lista) | `for` clasico |
| Solo quieres iterar por algo (no construir una lista) | `for` clasico |

#### Truco: NO solo listas

La misma sintaxis con distintos delimitadores te da **set comprehensions**, **dict comprehensions** y **generadores**:

```python
[x*2 for x in range(5)]      # list:  [0, 2, 4, 6, 8]
{x*2 for x in range(5)}      # set:   {0, 2, 4, 6, 8}
{x: x*2 for x in range(5)}   # dict:  {0:0, 1:2, 2:4, 3:6, 4:8}
(x*2 for x in range(5))      # generator: objeto perezoso
```"""
    )},
]))

plan.append((ID_LC_EJ_BASIC, [
    {"type": "md", "src": tu_turno(15,
        """Resuelve los tres apartados usando **list comprehensions** en una sola linea cada uno:

1. Crea una lista con los **cuadrados** de los numeros del 1 al 10.
2. Dado el string `s = 'Programar'`, crea una lista con cada caracter en **minuscula**.
3. Crea una lista con todos los numeros del 1 al 100 que sean **multiplos de 7**.

Imprime cada resultado."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\ns = 'Programar'\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# # 1)\n# print([n ** 2 for n in range(1, 11)])\n#\n# # 2)\n# s = 'Programar'\n# print([c.lower() for c in s])\n#\n# # 3)\n# print([n for n in range(1, 101) if n % 7 == 0])\n"},
]))


# ============ LC con filtro ============
plan.append((ID_LC_PARES, [
    {"type": "md", "src": tu_turno(16,
        """Tienes esta lista mixta de strings:
```python
palabras = ['Sol', 'mar', 'Cielo', 'aire', 'Tierra', 'Agua']
```

Usando una **sola list comprehension con filtro**, crea una lista con las palabras que **empiezan en mayuscula** (usa `palabra[0].isupper()` o `palabra.istitle()`). Imprime el resultado.

Resultado esperado: `['Sol', 'Cielo', 'Tierra', 'Agua']`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\npalabras = ['Sol', 'mar', 'Cielo', 'aire', 'Tierra', 'Agua']\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# palabras = ['Sol', 'mar', 'Cielo', 'aire', 'Tierra', 'Agua']\n# resultado = [p for p in palabras if p[0].isupper()]\n# print(resultado)\n"},
]))


# ============ LC con ternaria ============
plan.append((ID_LC_TERNARIA, [
    {"type": "md", "src": teoria(
        "Donde va el if: filtro vs ternaria",
        """Las dos formas son distintas y se confunden mucho. La **posicion del `if`** determina su rol:

| Posicion | Rol | Sintaxis |
|---|---|---|
| **Despues** del `for` | **Filtro**: descarta elementos que no cumplen | `[x for x in it if cond]` |
| **Antes** del `for` | **Ternaria**: transforma cada elemento | `[a if cond else b for x in it]` |

#### Ejemplos contrastados

```python
# FILTRO: salen solo los pares (los impares no aparecen)
[x for x in range(10) if x % 2 == 0]
# -> [0, 2, 4, 6, 8]

# TERNARIA: TODOS aparecen, pero los pares se transforman a 0
[0 if x % 2 == 0 else x for x in range(10)]
# -> [0, 1, 0, 3, 0, 5, 0, 7, 0, 9]
```

#### Combinarlos

Puedes tener **ternaria + filtro** a la vez:
```python
[x*2 if x > 0 else 0 for x in [-2, -1, 0, 1, 2] if x != 0]
# -> [0, 2, 4]      (excluye el 0, transforma negativos a 0, dobla positivos)
```"""
    )},
    {"type": "md", "src": tu_turno(17,
        """Tienes la lista:
```python
numeros = [-3, -1, 0, 2, 5, -7, 8]
```

Usando una **sola list comprehension con ternaria**, crea una lista nueva donde:
- Los numeros **negativos** se conviertan a `0`.
- Los demas se queden iguales.

Resultado esperado: `[0, 0, 0, 2, 5, 0, 8]`.

**Bonus:** ahora con filtro y ternaria juntos: misma transformacion pero **excluyendo** el 0 del resultado final. Resultado esperado: `[0, 0, 2, 5, 0, 8]`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nnumeros = [-3, -1, 0, 2, 5, -7, 8]\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# numeros = [-3, -1, 0, 2, 5, -7, 8]\n#\n# # Solo ternaria:\n# r1 = [n if n >= 0 else 0 for n in numeros]\n# print(r1)\n#\n# # Bonus: ternaria + filtro\n# r2 = [n if n >= 0 else 0 for n in numeros if n != 0]\n# print(r2)\n"},
]))


# ============ LC anidamiento ============
plan.append((ID_LC_NESTED_EJ, [
    {"type": "md", "src": teoria(
        "Comprehensions con varios for (anidamiento)",
        """Puedes tener **dos o mas `for`** dentro de la misma comprehension. Se leen **de izquierda a derecha**, igual que escribirias los bucles anidados:

```python
# List comp con dos for
[(x, y) for x in [1, 2, 3] for y in [4, 5]]

# Equivale a:
resultado = []
for x in [1, 2, 3]:
    for y in [4, 5]:
        resultado.append((x, y))

# -> [(1,4), (1,5), (2,4), (2,5), (3,4), (3,5)]
```

#### Aplanar una lista de listas (flatten)

```python
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
plana = [n for fila in matriz for n in fila]
# -> [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

#### Con filtro adicional

```python
parejas = [(x, y) for x in range(4) for y in range(4) if x != y]
# todas las parejas (x, y) con x distinto de y
```"""
    )},
    {"type": "md", "src": tu_turno(18,
        """Tienes esta matriz (lista de listas):
```python
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

1. Usa una list comprehension con **dos `for`** para **aplanarla** y obtener `[1, 2, 3, 4, 5, 6, 7, 8, 9]`.
2. Usa otra list comprehension para obtener una lista solo con los **numeros pares** de la matriz: `[2, 4, 6, 8]`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nmatriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\n#\n# plana = [n for fila in matriz for n in fila]\n# print(plana)\n#\n# pares = [n for fila in matriz for n in fila if n % 2 == 0]\n# print(pares)\n"},
]))


# ============ DICT COMPREHENSION ============
plan.append((ID_DICT_COMP_EJ, [
    {"type": "md", "src": teoria(
        "Dict comprehensions: construir diccionarios sobre la marcha",
        """Igual que las list comprehensions, pero usan llaves `{}` y dos expresiones separadas por `:` (clave : valor):

```python
{clave_expr: valor_expr  for item in iterable}
{clave_expr: valor_expr  for item in iterable  if cond}
```

#### Casos clasicos

```python
# Mapear numero -> cuadrado
{n: n*n for n in range(5)}
# -> {0:0, 1:1, 2:4, 3:9, 4:16}

# Combinar dos listas en dict (con zip)
items = ['Banana', 'Pera', 'Olivas']
precio = [1.1, 1.4, 2.4]
shopping = {k: v for k, v in zip(items, precio)}
# -> {'Banana': 1.1, 'Pera': 1.4, 'Olivas': 2.4}

# Invertir un dict (intercambiar clave y valor)
original = {'a': 1, 'b': 2, 'c': 3}
invertido = {v: k for k, v in original.items()}
# -> {1: 'a', 2: 'b', 3: 'c'}

# Filtrar un dict
notas = {'Maria': 7, 'Pedro': 3, 'Lucia': 9}
aprobados = {k: v for k, v in notas.items() if v >= 5}
# -> {'Maria': 7, 'Lucia': 9}
```

#### Cuidado: claves duplicadas

Si la misma clave aparece dos veces, **gana la ultima**:
```python
{c: i for i, c in enumerate('abcabc')}
# -> {'a': 3, 'b': 4, 'c': 5}    (no {a:0, b:1, c:2})
```"""
    )},
    {"type": "md", "src": tu_turno(19,
        """Tienes:
```python
nombres = ['Ana', 'Pedro', 'Lucia', 'Juan']
```

Usando una **dict comprehension**, crea un diccionario donde la clave sea cada nombre y el valor sea su **longitud**. Resultado esperado:
```python
{'Ana': 3, 'Pedro': 5, 'Lucia': 5, 'Juan': 4}
```

**Bonus:** crea otro diccionario con solo los nombres cuya longitud sea **mayor que 3**."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nnombres = ['Ana', 'Pedro', 'Lucia', 'Juan']\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# nombres = ['Ana', 'Pedro', 'Lucia', 'Juan']\n#\n# d = {n: len(n) for n in nombres}\n# print(d)\n#\n# # Bonus con filtro\n# d2 = {n: len(n) for n in nombres if len(n) > 3}\n# print(d2)\n"},
]))


# ============ EXCEPCIONES ============
plan.append((ID_EXC_HEADER, [
    {"type": "md", "src": teoria(
        "Excepciones: cuando algo sale mal",
        """Una **excepcion** es un evento que **interrumpe el flujo normal** del programa porque ha ocurrido algo inesperado. En Python TODO error en tiempo de ejecucion es una excepcion.

#### Excepciones que veras a menudo

| Tipo | Cuando ocurre |
|---|---|
| `ValueError` | Conversion fallida, ej. `int('hola')`. |
| `TypeError` | Tipo equivocado, ej. `'a' + 1`. |
| `IndexError` | Indice de lista fuera de rango. |
| `KeyError` | Clave que no existe en un dict. |
| `ZeroDivisionError` | Division entre 0. |
| `FileNotFoundError` | Archivo que no existe al abrirlo. |
| `AttributeError` | Acceder a un atributo que no existe en el objeto. |
| `NameError` | Variable usada antes de declararla. |
| `KeyboardInterrupt` | El usuario pulso Ctrl+C. |

#### Que pasa si NO la capturas?

El programa **se detiene** y Python imprime el llamado **traceback**: el mensaje de error con la cadena de llamadas. Despues de eso, ninguna instruccion se ejecuta.

#### Idea clave

Hay dos filosofias para manejar 'cosas que pueden ir mal':

- **LBYL** (Look Before You Leap): comprueba antes con un `if`.
- **EAFP** (Easier to Ask Forgiveness than Permission): intenta y captura. **Es la filosofia oficial de Python.**

```python
# LBYL
if 'clave' in d:
    valor = d['clave']
else:
    valor = 0

# EAFP (mas pythonico)
try:
    valor = d['clave']
except KeyError:
    valor = 0
```"""
    )},
]))

plan.append((ID_TRY_INTRO, [
    {"type": "md", "src": teoria(
        "try / except: capturar y manejar excepciones",
        """La sintaxis para capturar excepciones es:

```python
try:
    # codigo que puede fallar
except TipoDeError:
    # que hago si ocurre TipoDeError
except (OtroTipo, OtroMas):
    # un except puede capturar varios tipos
except Exception as e:
    # 'e' contiene el objeto excepcion -> str(e) da el mensaje
else:
    # se ejecuta SOLO si NO hubo excepcion (opcional)
finally:
    # se ejecuta SIEMPRE, haya o no excepcion (opcional)
```

#### Reglas y orden

1. Primero el `try` (obligatorio).
2. Despues uno o varios `except` (al menos uno, salvo si solo usas `finally`).
3. `else` opcional: codigo que solo corre si el `try` salio limpio.
4. `finally` opcional: limpieza que SIEMPRE se ejecuta.

#### Buenas practicas

- **Captura tipos especificos.** Evita el `except:` pelado, porque atrapa **todo**, incluso `KeyboardInterrupt` (Ctrl+C) y bugs reales.
- **Captura solo lo que sabes manejar.** Si no sabes que hacer con un error, dejalo subir.
- **No silencies errores.** Como minimo, registra el error con `print` o `logging`.

#### Acceder al mensaje del error

```python
try:
    1 / 0
except ZeroDivisionError as e:
    print('Error:', e)        # 'Error: division by zero'
    print(type(e).__name__)   # 'ZeroDivisionError'
```"""
    )},
]))

if ID_TRY_EJ_INDEX:
    plan.append((ID_TRY_EJ_INDEX, [
        {"type": "md", "src": tu_turno(20,
            """Pide un numero al usuario con `input(...)`. Conviertelo a entero. Si el usuario escribe algo que **no es un numero**, captura el `ValueError` y muestra `'Introduce un numero valido'`. Si lo introduce bien, imprime su doble.

> Pista: la conversion `int(input(...))` es lo que puede lanzar `ValueError`."""
        )},
        {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
        {"type": "code", "src": "# === Solucion sugerida ===\n# try:\n#     n = int(input('Numero: '))\n#     print('Doble:', n * 2)\n# except ValueError:\n#     print('Introduce un numero valido')\n"},
    ]))


# ============ except generico - aviso ============
if ID_TRY_GENERIC:
    plan.append((ID_TRY_GENERIC, [
        {"type": "md", "src": aviso(
            """**No uses `except:` pelado** en codigo serio. Captura **todas** las excepciones, incluyendo cosas como `KeyboardInterrupt` (Ctrl+C) o `SystemExit`. Eso significa que tu usuario no puede ni interrumpir el programa, y los bugs quedan ocultos.

| En lugar de | Usa |
|---|---|
| `except:` | `except Exception:` (igual de generico, pero respeta Ctrl+C) |
| `except Exception as e: print(e)` solo en pruebas | Loggea el error y/o re-lanzalo despues |

Si DE VERDAD necesitas capturar todo (bucles externos, daemons), captura `BaseException` con cuidado y vuelve a lanzar despues de loggear."""
        )},
    ]))


# ============ except as e ============
plan.append((ID_EXC_AS_E, [
    {"type": "md", "src": tu_turno(21,
        """Escribe una funcion `dividir(a, b)` que devuelva `a / b`. Llamala dentro de un `try / except` que capture **dos** excepciones distintas:

- `ZeroDivisionError` -> imprime `'No se puede dividir entre cero'`.
- `TypeError` -> imprime `'Los argumentos deben ser numericos: <mensaje>'` mostrando el mensaje real con `as e`.

Llama a la funcion 3 veces para probar:
1. `dividir(10, 2)` -> 5.0
2. `dividir(10, 0)` -> mensaje 1
3. `dividir(10, 'a')` -> mensaje 2"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def dividir(a, b):\n#     return a / b\n#\n# for caso in [(10, 2), (10, 0), (10, 'a')]:\n#     try:\n#         print(dividir(*caso))\n#     except ZeroDivisionError:\n#         print('No se puede dividir entre cero')\n#     except TypeError as e:\n#         print(f'Los argumentos deben ser numericos: {e}')\n"},
]))


# ============ FINALLY ============
plan.append((ID_FINALLY_INTRO, [
    {"type": "md", "src": teoria(
        "finally: codigo que SIEMPRE se ejecuta",
        """El bloque `finally` se ejecuta **siempre**, hubiera o no hubiera excepcion. Tambien se ejecuta aunque hagas `return` dentro del try.

```python
try:
    archivo = open('datos.txt')
    datos = archivo.read()
except FileNotFoundError:
    print('No existe el archivo')
finally:
    archivo.close()    # <- esto SIEMPRE intenta cerrar el archivo
```

#### Para que se usa?

- **Liberar recursos**: cerrar archivos, cerrar conexiones a bases de datos, liberar locks.
- **Limpiar estado**: poner una variable global a su valor original, vaciar buffers.
- **Garantizar que algo siempre pase**, sin importar el resultado.

#### Mas pythonico: el contexto `with`

Para cerrar archivos, usar `with` es mas limpio que `try/finally`:

```python
# Forma vieja
try:
    archivo = open('datos.txt')
    datos = archivo.read()
finally:
    archivo.close()

# Forma moderna (with se encarga de cerrar)
with open('datos.txt') as archivo:
    datos = archivo.read()
```

`finally` sigue siendo util para **otros recursos** o cuando no hay un `with` apropiado."""
    )},
]))


# ============ RAISE ============
plan.append((ID_RAISE_INTRO, [
    {"type": "md", "src": teoria(
        "raise: lanzar tus propias excepciones",
        """Hasta ahora hemos **capturado** excepciones. Tambien puedes **lanzarlas tu mismo** con `raise`.

```python
raise TipoDeError('mensaje opcional')
```

#### Por que querrias lanzar una excepcion?

1. **Validar argumentos**: en una funcion publica, si te llegan datos invalidos, lanza un error claro en lugar de seguir y romper en otro sitio.
2. **Logica de negocio**: 'no hay saldo suficiente', 'el usuario ya existe', etc.
3. **Re-lanzar despues de loggear**: capturar para registrar y volver a lanzar para que la siguiente capa lo gestione.

#### Ejemplos

```python
def raiz_cuadrada(x):
    if x < 0:
        raise ValueError(f'No se puede sacar raiz de un negativo: {x}')
    return x ** 0.5
```

#### Excepciones personalizadas

Cuando los tipos estandar no encajan, defines tu propio tipo heredando de `Exception`:

```python
class SaldoInsuficiente(Exception):
    pass

def retirar(cuenta, cantidad):
    if cantidad > cuenta.saldo:
        raise SaldoInsuficiente(f'Pediste {cantidad}, tienes {cuenta.saldo}')
```

#### Re-lanzar manteniendo el traceback

Dentro de un `except`, simplemente `raise` (sin argumentos) re-lanza la excepcion actual conservando toda la informacion:

```python
try:
    operacion()
except Exception as e:
    log.error(e)
    raise           # vuelve a lanzar para que la capa superior la vea
```"""
    )},
]))

plan.append((ID_RAISE_EJ, [
    {"type": "md", "src": tu_turno(22,
        """Escribe una funcion `edad_valida(edad)` que:

1. Lance un `TypeError` con un mensaje descriptivo si `edad` no es `int`. Pista: usa `isinstance(edad, int)`.
2. Lance un `ValueError` si `edad` es **negativa** o **mayor que 130**.
3. En caso contrario, devuelva `True`.

Pruebala envuelta en un `try / except` con tres llamadas:
- `edad_valida(30)`
- `edad_valida(-5)`
- `edad_valida('treinta')`

Captura cada excepcion e imprime el tipo y el mensaje."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def edad_valida(edad):\n#     if not isinstance(edad, int):\n#         raise TypeError(f'Edad debe ser int, no {type(edad).__name__}')\n#     if edad < 0 or edad > 130:\n#         raise ValueError(f'Edad fuera de rango: {edad}')\n#     return True\n#\n# for caso in [30, -5, 'treinta']:\n#     try:\n#         edad_valida(caso)\n#         print(f'{caso} OK')\n#     except (TypeError, ValueError) as e:\n#         print(f'{type(e).__name__}: {e}')\n"},
]))


# ============ Cierre antes de los Ejercicios ============
if ID_EJERCICIOS:
    plan.append((ID_EJERCICIOS, [
        {"type": "md", "src": teoria(
            "Resumen rapido antes de los ejercicios oficiales",
            """Ya tienes en la mano todas las herramientas de control de flujo de Python. Usa esta tabla como **chuleta** para los ejercicios:

| Quiero... | Usa |
|---|---|
| Tomar una decision | `if / elif / else` |
| Asignar un valor segun condicion | ternaria `a if cond else b` |
| Comparar contra muchos casos | `match / case` |
| Repetir un numero conocido de veces | `for ... in range(...)` |
| Recorrer una coleccion | `for ... in coleccion` |
| Recorrer indice + valor | `for i, v in enumerate(...)` |
| Recorrer dos colecciones a la vez | `for a, b in zip(...)` |
| Recorrer dict (clave + valor) | `for k, v in d.items()` |
| Repetir mientras una condicion | `while condicion:` |
| Salir de un bucle al instante | `break` |
| Saltar a la siguiente iteracion | `continue` |
| Codigo si el bucle no se rompio | `for...else` / `while...else` |
| Construir lista filtrada/transformada | list comprehension |
| Construir dict / set | dict / set comprehension |
| Capturar errores | `try / except / [else] / [finally]` |
| Lanzar errores | `raise TipoError('mensaje')` |

Animo con los ejercicios! Si te trabas, **vuelve a la teoria** del bloque correspondiente y **piensa primero en pseudo-codigo** antes de teclear."""
        )},
    ]))


# ============ aplicar ============
enhance(NB, plan)
print("Done.")

"""Aplica mejoras al notebook 04_Functions con bloques de colores y teoria detallada."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, solucion_md, dato, aviso
import json

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_04_Python101_Functions.ipynb"

nb = json.load(open(NB, encoding="utf-8"))


def find_id(fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if fragment in src:
            return c["id"]
    return None


# IDs reales del notebook 04
ID_TITULO          = nb["cells"][0]["id"]                     # 0
ID_QUE_SON         = find_id("Son un mecanismo que te ofrece") # 2
ID_EJEMPLO_HEAD    = find_id("## Ejemplo")                     # 3
ID_DEF_SUMAR       = find_id("def sumar(x, y):")              # 4
ID_FAHRENHEIT      = find_id("convert_celsius_to_fahrenheit(degrees)") # 7
ID_VENTAJAS        = find_id("Eliminaci")                      # 8 (Eliminacion duplicacion codigo)
ID_PROG_FUNC       = find_id("## Programaci")                  # 9
ID_FORMATO_GENERAL = find_id("Formato general")                # 10
ID_INSTR_CONV      = find_id("instrucciones convencionales")   # 11
ID_FUNC_ANIDADAS   = find_id("anidadas en sentencias")         # 14
ID_ARGS_OPCIONALES = find_id("Argumentos y return son opcionales") # 16
ID_RETURN_NONE     = find_id("no tiene sentencia *return*")    # 18
ID_RETURN_LOC      = find_id("puede aparecer en cualquier")    # 20
ID_RETURN_MULTI    = find_id("Puede haber m")                  # 22 - "mas de un valor de retorno"
ID_TYPE_HINTS      = find_id("son simples hints")              # 25
ID_DEFAULT_ARGS    = find_id("valores por defecto")            # 28
ID_KEYWORD_ARGS    = find_id("orden se puede alterar")         # 30
ID_FUNC_OBJETO     = find_id("Al ejecutarse una sentencia *def*") # 32
ID_FUNC_REFERENCIA = find_id("Variables pueden referenciar")   # 34
ID_PASS            = find_id("placeholders")                    # 36
ID_PASO_PARAM      = find_id("## Paso de par")                  # 38
ID_PASO_VALOR      = find_id("Tipos simples (inmutables)")     # 39
ID_PASO_REF_REAL   = find_id("se pas") and find_id("por referencia")  # 41
ID_PASO_MUTABLES   = find_id("Tipos complejos (mutables)")     # 43
ID_MOD_BASICO      = find_id("modificar un objeto que es de un tipo b") # 45
ID_NO_MOD_COPIA    = find_id("no se modifique un objeto de un tipo complejo") # 47
ID_ARGS_ARBITRARIOS = find_id("## Argumentos arbitrarios")     # 49
ID_ARGS_TUPLA      = find_id("se reciben como una tupla")      # 50
ID_KWARGS          = find_id("doble asterisco")                # 52
ID_DESEMPAQUETADO  = find_id("### Desempaquetado en funciones") # 54
ID_LAMBDA_HEAD     = find_id("## Funciones Lambda")            # 57
ID_LAMBDA_DEF      = find_id("definir funciones an")           # 58
ID_LAMBDA_FORMATO  = find_id("Formato general:") and find_id("lambda <lista de argumentos>") # 59
ID_LAMBDA_REF      = find_id("guardar una referencia")         # 62
ID_LAMBDA_LISTA    = find_id("formar parte de una lista")      # 64
ID_DICT_SWITCH     = find_id("Diccionarios se pueden utilizar como 'switch'") # 66
ID_RECURSION_HEAD  = find_id("## Recursividad")                # 68
ID_RECURSION_DEF   = find_id("se llaman a s")                  # 69
ID_FACTORIAL       = find_id("def factorial(n):")              # 70
ID_SCOPES_HEAD     = find_id("## Scopes")                      # 72
ID_SCOPES_DEF      = find_id("localizaci")                     # 73
ID_LEGB            = find_id("Regla LEGB")                     # 75
ID_GLOBAL          = find_id("La sentencia *global*")          # 78
ID_NO_GLOBAL_LECTURA = find_id("No hay necesidad de usar *global*") # 80
ID_CLOSURES        = find_id("#### Closures")                  # 83
ID_NONLOCAL        = find_id("Sentencia *nonlocal*")           # 85
ID_EJERCICIOS      = find_id("## Ejercicios")                  # 87


plan = []

# -------- INTRO al notebook --------
plan.append((ID_TITULO, [
    {"type": "md", "src": teoria(
        "Como leer este notebook (version mejorada)",
        """Este notebook fue **enriquecido** para que aprendas escribiendo codigo. Vas a encontrar varios tipos de bloques de colores:

<div style="background-color:#e7f5ff;border-left:6px solid #1c7ed6;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AZUL = TEORIA</b></div> -> explicacion en palabras simples antes de cada concepto.

<div style="background-color:#fff9db;border-left:6px solid #f59f00;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AMARILLO = TU TURNO</b></div> -> el ejercicio que TU debes resolver. Hay una celda vacia debajo donde escribes el codigo.

<div style="background-color:#ebfbee;border-left:6px solid #2f9e44;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>VERDE = SOLUCION</b></div> -> codigo de referencia comentado por si te trabas. Mira solo despues de intentar.

<div style="background-color:#f3f0ff;border-left:6px solid #7048e8;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>VIOLETA = PARA RECORDAR</b></div> -> dato puntual que conviene fijar.

<div style="background-color:#fff0f0;border-left:6px solid #e03131;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>ROJO = CUIDADO</b></div> -> trampas tipicas que conviene evitar.

> **Promesa importante**: el codigo y la teoria del profesor original no se han tocado. Solo se han ANADIDO bloques. Asi puedes seguir comparando con la version original cuando quieras.

#### Tema de hoy: FUNCIONES

Vas a aprender:
- Que es una funcion y por que existen.
- Como definirlas con `def`, parametros, valores por defecto y `return`.
- Argumentos posicionales, keyword, `*args` y `**kwargs`.
- Funciones `lambda` (anonimas).
- Recursividad.
- Scope de variables (LEGB), `global` y `nonlocal`.
- Funciones como objetos de primera clase y closures."""
    )},
]))

# ============ QUE ES UNA FUNCION ============
plan.append((ID_QUE_SON, [
    {"type": "md", "src": teoria(
        "Que es una funcion?",
        """Una **funcion** es un bloque de codigo con **nombre** que hace **una tarea concreta**. La defines una vez y la usas muchas.

#### Por que existen?

Sin funciones, escribirias el mismo codigo una y otra vez. Con funciones:

| Beneficio | Por que importa |
|---|---|
| **Reutilizacion** | Escribes una vez, llamas N veces. |
| **Legibilidad** | `calcular_iva(precio)` cuenta una historia mejor que 5 lineas de calculos. |
| **Mantenimiento** | Si cambias la formula, la cambias en UN sitio. |
| **Abstraccion** | Esconden detalles complejos detras de un nombre simple. |
| **Pruebas** | Pueden probarse aisladas (unit testing). |

#### Anatomia de una funcion en Python

```python
def saludar(nombre):              # 'def' + nombre + parametros + ':'
    '''Imprime un saludo.'''       # docstring (opcional pero recomendado)
    mensaje = f'Hola {nombre}'    # cuerpo (indentado)
    print(mensaje)
    return mensaje                # valor que devuelve (opcional)
```

| Parte | Significado |
|---|---|
| `def` | Palabra clave para definir |
| `saludar` | Nombre de la funcion (snake_case en Python) |
| `(nombre)` | Lista de parametros |
| `:` | Inicia el bloque |
| docstring | Documentacion (la lee `help(funcion)`) |
| cuerpo | Lineas indentadas que ejecuta |
| `return` | Devuelve un valor al que llamo (opcional) |

#### Que pasa cuando llamas a una funcion?

```python
saludar('Lucas')   # llamada (invocacion)
```

Python:
1. Busca el objeto `saludar`.
2. Crea un **scope local** nuevo.
3. Asigna `nombre = 'Lucas'` dentro de ese scope.
4. Ejecuta el cuerpo.
5. Devuelve lo que diga `return` (o `None` si no hay return).
6. Borra el scope local."""
    )},
]))

plan.append((ID_DEF_SUMAR, [
    {"type": "md", "src": tu_turno(1,
        """Define una funcion `saludar(nombre)` que **devuelva** (con `return`) la cadena `Hola, <nombre>!`. Llamala con tu nombre y guarda el resultado en una variable `mensaje`. Imprime `mensaje`.

> Resultado esperado si pasas `'Lucas'`: `Hola, Lucas!`"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def saludar(nombre):\n#     '''Devuelve un saludo personalizado.'''\n#     return f'Hola, {nombre}!'\n#\n# mensaje = saludar('Lucas')\n# print(mensaje)\n"},
]))

# ============ VENTAJAS / FORMATO GENERAL ============
plan.append((ID_FORMATO_GENERAL, [
    {"type": "md", "src": teoria(
        "Formato general y reglas de nombres",
        """```python
def nombre_funcion(param1, param2, ...):
    cuerpo
    return valor    # opcional
```

#### Reglas de nombres (PEP 8)

- Usa **snake_case**: `calcular_iva`, no `calcularIVA` ni `CalcularIVA`.
- Sin espacios. Sin tildes ni caracteres raros.
- Empieza por letra o `_`. Nunca por numero.
- No uses palabras reservadas (`def`, `if`, `class`, `return`, etc.).
- Que el nombre **diga que hace** la funcion: verbos como `obtener_`, `calcular_`, `es_`, `tiene_`.

#### Que tipos de datos puede recibir y devolver?

**Cualquier cosa**: int, float, str, list, dict, otra funcion, None, objetos personalizados... Python no obliga a declarar tipos. Pero PUEDES (mas adelante veras los **type hints**).

| Que parametros puedo poner? | Ejemplo |
|---|---|
| Sin parametros | `def saludar():` |
| Uno o varios posicionales | `def sumar(a, b):` |
| Con valor por defecto | `def saludar(nombre='Mundo'):` |
| Numero variable | `def total(*nums):` |
| Variable con clave=valor | `def config(**opciones):` |
| Type hints (informativos) | `def sumar(a: int, b: int) -> int:` |"""
    )},
]))

plan.append((ID_FUNC_ANIDADAS, [
    {"type": "md", "src": dato(
        """Las funciones se pueden definir **dentro de otras funciones** o **dentro de bloques `if`/`for`**. La definicion solo se ejecuta cuando Python pasa por esa linea, asi que la **funcion no existe** hasta entonces. Si llamas a una funcion antes de definirla, obtendras `NameError`."""
    )},
    {"type": "md", "src": tu_turno(2,
        """Crea una variable `modo = 'estricto'`. Luego define **DENTRO de un `if`** una funcion `verificar(x)` que:

- Si `modo == 'estricto'`, devuelva `True` solo si `x > 100`.
- Si no (`else`), devuelva `True` si `x > 0`.

Llama `verificar(50)` y muestralo. Cambia `modo` a `'flexible'` (vuelve a ejecutar la celda) y observa la diferencia."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# modo = 'estricto'\n# if modo == 'estricto':\n#     def verificar(x):\n#         return x > 100\n# else:\n#     def verificar(x):\n#         return x > 0\n#\n# print(verificar(50))   # False con 'estricto', True con 'flexible'\n"},
]))

# ============ ARGUMENTOS Y RETURN OPCIONALES ============
plan.append((ID_ARGS_OPCIONALES, [
    {"type": "md", "src": teoria(
        "<code>return</code>: como sale informacion de la funcion",
        """`return` es la sentencia que **termina** la funcion y **devuelve un valor** a quien la llamo.

#### Cosas que conviene saber

| Caso | Que pasa |
|---|---|
| Funcion sin `return` | Devuelve `None` automaticamente. |
| `return` sin valor | Devuelve `None` y termina la funcion. |
| `return X` | Devuelve `X` y **detiene** la funcion. |
| Varios `return` en distintas ramas | Solo se ejecuta el primero alcanzado. |
| `return a, b, c` | Devuelve **una tupla** `(a, b, c)`. |

```python
def es_par(n):
    if n % 2 == 0:
        return True       # sale aqui si es par
    return False          # sale aqui si no
```

> Tip: cualquier codigo despues de un `return` que se ejecute es **codigo muerto** (nunca corre). Algunos editores te lo avisan."""
    )},
]))

plan.append((ID_RETURN_NONE, [
    {"type": "md", "src": aviso(
        """Si una funcion **no tiene `return`** (o tiene `return` sin valor), devuelve **`None`**. Esto es la causa de muchos bugs:

```python
def imprimir_doble(x):
    print(x * 2)        # imprime, pero NO devuelve

resultado = imprimir_doble(5)
print(resultado)         # None  <- sorpresa!
print(resultado + 1)     # ERROR: unsupported operand type(s)
```

**Regla:** si quieres usar el resultado, devuelvelo con `return`. Si solo quieres mostrarlo, usa `print` (pero no esperes recibir nada)."""
    )},
]))

plan.append((ID_RETURN_LOC, [
    {"type": "md", "src": tu_turno(3,
        """Define una funcion `division_segura(a, b)` que:

- Si `b == 0`, devuelva el string `'No se puede dividir por cero'`.
- Si no, devuelva `a / b`.

Probada con `division_segura(10, 2)` -> `5.0` y `division_segura(10, 0)` -> mensaje."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def division_segura(a, b):\n#     if b == 0:\n#         return 'No se puede dividir por cero'\n#     return a / b\n#\n# print(division_segura(10, 2))   # 5.0\n# print(division_segura(10, 0))   # mensaje\n"},
]))

# ============ RETURN MULTIPLE ============
plan.append((ID_RETURN_MULTI, [
    {"type": "md", "src": teoria(
        "Devolver varios valores: en realidad, una tupla",
        """En Python una funcion solo puede devolver **un objeto**. Pero puede devolver una **tupla** con varios valores, y la sintaxis es tan limpia que parece magia.

```python
def min_max(lista):
    return min(lista), max(lista)    # devuelve UNA tupla (min, max)

resultado = min_max([3, 1, 4, 1, 5])   # resultado es una tupla
print(resultado)                        # (1, 5)
print(type(resultado))                  # <class 'tuple'>
```

#### Desempaquetado: lo elegante

Si en la llamada pones tantas variables como elementos devuelve, Python las **desempaqueta** automaticamente:

```python
minimo, maximo = min_max([3, 1, 4, 1, 5])
print(minimo, maximo)    # 1 5
```

Hasta puedes ignorar valores con `_`:

```python
def coordenadas():
    return 10, 20, 30    # tupla (x, y, z)

x, _, z = coordenadas()  # ignora la y
```

#### Devolver una tupla NOMBRADA (mas adelante)

Cuando devuelves muchos valores, conviene usar `collections.namedtuple` o `dataclasses` para que tengan nombre. Pero eso lo veras en clases avanzadas."""
    )},
    {"type": "md", "src": tu_turno(4,
        """Define una funcion `estadisticas(numeros)` que reciba una lista de numeros y devuelva tres valores: la **suma**, el **minimo** y el **maximo**. Despues llamala con `[3, 7, 2, 9, 5]` y desempaqueta el resultado en tres variables. Imprime cada una con un texto descriptivo.

> Resultado esperado: suma=26, minimo=2, maximo=9."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def estadisticas(numeros):\n#     return sum(numeros), min(numeros), max(numeros)\n#\n# total, minimo, maximo = estadisticas([3, 7, 2, 9, 5])\n# print(f'Suma:    {total}')\n# print(f'Minimo:  {minimo}')\n# print(f'Maximo:  {maximo}')\n"},
]))

# ============ TYPE HINTS ============
plan.append((ID_TYPE_HINTS, [
    {"type": "md", "src": teoria(
        "Type hints: anotaciones de tipo (informativas)",
        """Los **type hints** son una forma de **documentar** que tipos esperas y que tipo devuelves. Python **NO los comprueba** en tiempo de ejecucion: son ayudas para humanos y herramientas (como `mypy`, IDE, autocompletado).

```python
def sumar(a: int, b: int) -> int:
    return a + b

sumar(1, 2)        # 3
sumar('hi', 'ho')  # 'hiho'  <- Python NO lanza error
```

| Sintaxis | Significado |
|---|---|
| `param: int` | el parametro deberia ser `int` |
| `param: str = 'x'` | str con valor por defecto `'x'` |
| `param: list[int]` | lista de enteros (Python 3.9+) |
| `-> bool` | devuelve `bool` |
| `-> None` | no devuelve nada (sirve para funciones con efecto solo) |
| `Optional[int]` | int o None (importar de `typing`) |

#### Por que usarlos?

| Pro | Detalle |
|---|---|
| Autocompletado mejor | el IDE sabe que `lista` tiene `.append`, `.sort`... |
| Documentacion | leer `def f(x: int) -> bool:` te dice todo |
| Deteccion de bugs | herramientas como `mypy` te avisan ANTES de ejecutar |

> **No los comprueba Python**: si pasas un float a un parametro `int`, no falla. Solo es una guia."""
    )},
    {"type": "md", "src": tu_turno(5,
        """Reescribe esta funcion anadiendo type hints adecuados:

```python
def precio_con_iva(precio, iva=0.21):
    return precio * (1 + iva)
```

Pista: `precio` es un `float`, `iva` es un `float`, devuelve un `float`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def precio_con_iva(precio: float, iva: float = 0.21) -> float:\n#     '''Devuelve el precio con IVA aplicado.'''\n#     return precio * (1 + iva)\n#\n# print(precio_con_iva(100))         # 121.0\n# print(precio_con_iva(50, 0.10))    # 55.0\n"},
]))

# ============ DEFAULT ARGS ============
plan.append((ID_DEFAULT_ARGS, [
    {"type": "md", "src": teoria(
        "Argumentos con valor por defecto",
        """Puedes dar a un parametro un **valor por defecto**. Si no lo pasas al llamar, se usa ese valor.

```python
def saludar(nombre, mensaje='Hola'):
    print(f'{mensaje}, {nombre}')

saludar('Lucas')                      # 'Hola, Lucas'
saludar('Lucas', 'Buenos dias')       # 'Buenos dias, Lucas'
saludar('Lucas', mensaje='Adios')     # 'Adios, Lucas'
```

#### Reglas

| Regla | Por que |
|---|---|
| Los parametros con default van **al final** | Si no, Python no sabria a quien asignar los posicionales. |
| Sintaxis: `nombre = valor` (sin espacios) | Convencion PEP 8 dentro de la firma. |
| El default se evalua **una vez**, al definir | Aqui hay una trampa importante (ver abajo). |"""
    )},
    {"type": "md", "src": aviso(
        """**Trampa clasica**: nunca uses una **lista, dict o set** como valor por defecto. Se crea **una sola vez** y se comparte entre llamadas.

```python
def anadir(elem, lista=[]):     # NO HACER
    lista.append(elem)
    return lista

print(anadir(1))   # [1]
print(anadir(2))   # [1, 2]   <- la misma lista de antes!
print(anadir(3))   # [1, 2, 3]
```

**Solucion correcta:** usa `None` como sentinela y crea la lista dentro:

```python
def anadir(elem, lista=None):
    if lista is None:
        lista = []
    lista.append(elem)
    return lista
```

Esto vale tambien para `dict`, `set` y cualquier objeto mutable."""
    )},
    {"type": "md", "src": tu_turno(6,
        """Define una funcion `crear_usuario(nombre, edad=18, activo=True)`. Llamala de TRES formas distintas:

1. Solo con el nombre.
2. Con nombre y edad.
3. Con nombre y `activo=False` (saltandote `edad`, usa el nombre del parametro).

En cada llamada, devuelve un dict con los tres valores e imprimelo."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def crear_usuario(nombre, edad=18, activo=True):\n#     return {'nombre': nombre, 'edad': edad, 'activo': activo}\n#\n# print(crear_usuario('Ana'))\n# print(crear_usuario('Pedro', 25))\n# print(crear_usuario('Lucia', activo=False))\n"},
]))

# ============ KEYWORD ARGS ============
plan.append((ID_KEYWORD_ARGS, [
    {"type": "md", "src": teoria(
        "Argumentos posicionales vs keyword (por nombre)",
        """En Python puedes pasar argumentos de **dos maneras**:

#### 1. Posicional: por orden

```python
def f(a, b, c):
    print(a, b, c)

f(1, 2, 3)    # a=1, b=2, c=3
```

#### 2. Keyword (por nombre): por etiqueta

```python
f(a=1, b=2, c=3)
f(c=3, a=1, b=2)    # el orden no importa cuando das nombres
```

#### Mezcla: posicional primero, keyword despues

```python
f(1, c=3, b=2)      # a=1 posicional; b y c por nombre
```

**Regla de oro:** los keyword arguments **siempre van despues** de los posicionales.

```python
f(a=1, 2, 3)        # ERROR: positional argument follows keyword argument
```

#### Por que usar keyword args?

| Razon | Ejemplo |
|---|---|
| **Legibilidad** | `crear_usuario('Ana', activo=False)` se lee mejor que `crear_usuario('Ana', 18, False)`. |
| **Saltarte parametros** opcionales | Cuando hay muchos defaults y solo quieres cambiar uno. |
| **Evitar bugs por orden** | Si la funcion tiene 5 parametros, el orden es facil de equivocar. |"""
    )},
    {"type": "md", "src": dato(
        """Existen las **funciones keyword-only**: parametros que SOLO se pueden pasar por nombre. Se separan con `*`:

```python
def conectar(host, puerto, *, usuario, password):
    ...

conectar('a', 80, usuario='u', password='p')   # OK
conectar('a', 80, 'u', 'p')                     # ERROR
```

Y al reves, los **positional-only** con `/` (Python 3.8+):

```python
def f(a, b, /, c, d):
    ...
# a y b solo posicionales; c y d posicionales o keyword
```"""
    )},
    {"type": "md", "src": tu_turno(7,
        """Define una funcion `enviar_email(destinatario, asunto, cuerpo, copia=None, prioridad='normal')`. Llamala usando **keyword arguments** para enviar un email a `'jefe@empresa.com'` con asunto `'Reporte'` y prioridad `'alta'`, omitiendo `cuerpo` (deberas pasarlo como string vacio porque no tiene default) y `copia`.

Imprime los argumentos recibidos."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def enviar_email(destinatario, asunto, cuerpo, copia=None, prioridad='normal'):\n#     print(f'Para: {destinatario}')\n#     print(f'Asunto: {asunto}')\n#     print(f'Cuerpo: {cuerpo}')\n#     print(f'Copia: {copia}')\n#     print(f'Prioridad: {prioridad}')\n#\n# enviar_email(destinatario='jefe@empresa.com',\n#              asunto='Reporte',\n#              cuerpo='',\n#              prioridad='alta')\n"},
]))

# ============ FUNCIONES COMO OBJETOS ============
plan.append((ID_FUNC_OBJETO, [
    {"type": "md", "src": teoria(
        "Las funciones SON objetos de primera clase",
        """En Python, **una funcion es un objeto**, igual que un numero o una lista. Eso significa que puedes:

1. **Asignarla a una variable**.
2. **Pasarla como argumento** a otra funcion.
3. **Devolverla** desde otra funcion.
4. **Guardarla** en una lista, set, dict, etc.
5. **Definirla dentro** de otra funcion.

```python
def cuadrado(x):
    return x ** 2

f = cuadrado          # f apunta al MISMO objeto funcion
print(f(5))           # 25
print(cuadrado(5))    # 25
print(f is cuadrado)  # True
```

#### Eso es lo que permite cosas como:

```python
# Pasar una funcion como argumento
sorted([1, -3, 2], key=abs)        # ordena por valor absoluto
list(map(cuadrado, [1, 2, 3]))     # aplica cuadrado a cada elemento
list(filter(lambda x: x > 0, [1,-2,3]))  # filtra positivos

# Lista de funciones
operaciones = [cuadrado, abs, len]
```

| Concepto | Ejemplo |
|---|---|
| **Funcion como argumento** | `map`, `filter`, `sorted(key=...)` |
| **Funcion como retorno** | Decoradores, factories, closures |
| **Funcion en una coleccion** | dict de operaciones (switch en otros lenguajes) |"""
    )},
]))

plan.append((ID_FUNC_REFERENCIA, [
    {"type": "md", "src": tu_turno(8,
        """1. Define dos funciones cortas: `doblar(x)` que devuelva `x * 2` y `cuadrar(x)` que devuelva `x ** 2`.
2. Crea una **lista** que contenga las dos funciones (como objetos): `operaciones = [doblar, cuadrar]`.
3. Recorre esa lista con un `for` y llama a cada funcion pasandole `5`. Imprime el nombre y el resultado: `doblar(5) = 10`.

> Pista: para imprimir el nombre de una funcion usa `f.__name__`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def doblar(x):\n#     return x * 2\n#\n# def cuadrar(x):\n#     return x ** 2\n#\n# operaciones = [doblar, cuadrar]\n# for f in operaciones:\n#     print(f'{f.__name__}(5) = {f(5)}')\n"},
]))

# ============ PASS ============
plan.append((ID_PASS, [
    {"type": "md", "src": dato(
        """`pass` es una sentencia que **no hace nada**. Sirve para reservar sitio donde Python **necesita** un cuerpo pero todavia no tienes nada que poner: funciones, clases, condicionales, bucles. Sin `pass`, el bloque vacio da `IndentationError`.

```python
def todavia_no_implementada():
    pass     # placeholder, lo rellenare luego

if condicion:
    pass     # ya implementare la rama
```

Tambien existen alternativas como `raise NotImplementedError` (mejor cuando quieres que **falle visiblemente** si alguien la usa antes de tiempo) o `...` (Ellipsis), que algunos usan como placeholder en stubs de tipos."""
    )},
]))

# ============ PASO DE PARAMETROS ============
plan.append((ID_PASO_PARAM, [
    {"type": "md", "src": teoria(
        "Como pasa Python los parametros? (la pregunta del millon)",
        """En Python, los parametros se pasan **por referencia de objeto** (en ingles: *pass-by-object-reference* o *call-by-sharing*). No es ni "por valor" ni "por referencia" puros: es un punto medio que confunde si vienes de C o Java.

#### La idea en una frase

> La funcion **recibe la misma etiqueta** que tienes fuera. Apunta al MISMO objeto.

#### Pero entonces...

| Si dentro de la funcion haces... | Que pasa fuera |
|---|---|
| `x = 10` (REASIGNAS) | Fuera **NO cambia**. La etiqueta local se mueve a otro objeto. |
| `x.append(99)` (MUTAS el objeto) | Fuera **SI cambia**, porque es el mismo objeto. |

Por eso parece que con tipos **inmutables** (int, float, str, tuple) funciona "por valor", y con tipos **mutables** (list, dict, set) funciona "por referencia". En realidad Python siempre hace lo mismo, lo que cambia es si el objeto es mutable o no.

```python
def cambiar_inmutable(x):
    x = x + 1     # reasignacion: x apunta a otro int
    return x

a = 5
cambiar_inmutable(a)
print(a)         # 5 (sin cambios)

def mutar_lista(l):
    l.append(99)  # mutacion: cambia el objeto

lista = [1, 2, 3]
mutar_lista(lista)
print(lista)     # [1, 2, 3, 99]  <- cambio!
```

#### Resumen visual

```
Antes:   a -> [obj 5]
Llamas:  cambiar(a)  ->  x -> [obj 5]   (a y x apuntan al mismo)
Dentro:  x = x+1     ->  x -> [obj 6]   (x se mueve)
                         a -> [obj 5]   (a sigue donde estaba)
```"""
    )},
]))

plan.append((ID_PASO_MUTABLES, [
    {"type": "md", "src": aviso(
        """Cuando una funcion recibe una **lista, dict o set**, puede **mutarlo** y los cambios se ven fuera. A veces eso es lo que quieres; otras veces es un bug grave.

```python
def borrar_negativos(numeros):
    for n in numeros[:]:           # iterar copia para evitar saltar
        if n < 0:
            numeros.remove(n)      # MUTA la lista original

datos = [1, -2, 3, -4]
borrar_negativos(datos)
print(datos)        # [1, 3]   <- cambio el original
```

**Si quieres preservar el original:** copia dentro de la funcion (o fuera antes de llamarla):

```python
def sin_negativos(numeros):
    return [n for n in numeros if n >= 0]   # devuelve LISTA NUEVA
```

> **Buena practica:** si tu funcion modifica al receptor, deja claro en el nombre o docstring que tiene "efectos secundarios"."""
    )},
    {"type": "md", "src": tu_turno(9,
        """Escribe **dos versiones** de una funcion que duplique cada elemento de una lista:

1. `doblar_inplace(lista)`: **muta** la lista original (no devuelve nada).
2. `doblar_copia(lista)`: NO toca la original, devuelve una **nueva lista** con los valores doblados.

Pruebalas con `[1, 2, 3]` y comprueba el efecto sobre la original en cada caso."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def doblar_inplace(lista):\n#     for i in range(len(lista)):\n#         lista[i] *= 2\n#\n# def doblar_copia(lista):\n#     return [x * 2 for x in lista]\n#\n# original = [1, 2, 3]\n# doblar_inplace(original)\n# print(original)              # [2, 4, 6]\n#\n# original2 = [1, 2, 3]\n# nueva = doblar_copia(original2)\n# print(original2)             # [1, 2, 3]\n# print(nueva)                 # [2, 4, 6]\n"},
]))

# ============ ARGS ARBITRARIOS ============
plan.append((ID_ARGS_ARBITRARIOS, [
    {"type": "md", "src": teoria(
        "<code>*args</code>: numero variable de argumentos",
        """A veces no sabes **cuantos argumentos** vas a recibir. Para eso usas `*args` (el nombre `args` es solo convencion, podrias llamarlo `*numeros`).

```python
def total(*args):
    print(type(args))   # <class 'tuple'>
    return sum(args)

total()                # 0
total(1)               # 1
total(1, 2, 3, 4, 5)   # 15
```

| Detalle | Explicacion |
|---|---|
| `*args` recoge **los posicionales sobrantes** | Lo que no encaje en parametros normales. |
| Llega como **tupla** | Aunque sea un solo valor o vacio. |
| El `*` es lo importante, `args` es solo el nombre | Puedes usar `*numeros`, `*nombres`, etc. |

#### Combinarlo con parametros normales

```python
def saludar(saludo, *nombres):
    for n in nombres:
        print(f'{saludo}, {n}')

saludar('Hola', 'Ana', 'Pedro', 'Lucia')
# Hola, Ana
# Hola, Pedro
# Hola, Lucia
```

#### Desempaquetar con `*` al llamar

El asterisco tambien funciona **en la llamada** para "explotar" una lista o tupla en argumentos posicionales:

```python
def sumar(a, b, c):
    return a + b + c

valores = [1, 2, 3]
sumar(*valores)        # equivale a sumar(1, 2, 3)
```"""
    )},
    {"type": "md", "src": tu_turno(10,
        """Define una funcion `mayor_de(*numeros)` que reciba un numero variable de argumentos y devuelva el **mayor** de todos. Si no le pasas nada, devuelve `None`.

Pruebala con: `mayor_de(3, 7, 1)`, `mayor_de(10)`, `mayor_de()`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def mayor_de(*numeros):\n#     if len(numeros) == 0:\n#         return None\n#     return max(numeros)\n#\n# print(mayor_de(3, 7, 1))   # 7\n# print(mayor_de(10))         # 10\n# print(mayor_de())           # None\n"},
]))

# ============ KWARGS ============
plan.append((ID_KWARGS, [
    {"type": "md", "src": teoria(
        "<code>**kwargs</code>: argumentos clave-valor variables",
        """`**kwargs` recoge un numero variable de argumentos **por nombre** (clave=valor). Llega como un **diccionario**.

```python
def configurar(**kwargs):
    print(type(kwargs))   # <class 'dict'>
    for k, v in kwargs.items():
        print(f'{k} = {v}')

configurar(host='localhost', puerto=8080, debug=True)
# host = localhost
# puerto = 8080
# debug = True
```

#### Combinacion completa: todo a la vez

```python
def todo(a, b=10, *args, **kwargs):
    print('a:', a)
    print('b:', b)
    print('args:', args)
    print('kwargs:', kwargs)

todo(1, 2, 3, 4, x=5, y=6)
# a: 1
# b: 2
# args: (3, 4)
# kwargs: {'x': 5, 'y': 6}
```

| Orden obligatorio en la firma |
|---|
| 1. Posicionales normales |
| 2. Con default |
| 3. `*args` |
| 4. Keyword-only |
| 5. `**kwargs` |

#### Desempaquetar con `**` al llamar

Igual que `*` desempaqueta listas, `**` desempaqueta dicts en la llamada:

```python
def saludar(nombre, edad):
    print(f'{nombre}, {edad} anios')

datos = {'nombre': 'Ana', 'edad': 30}
saludar(**datos)        # equivale a saludar(nombre='Ana', edad=30)
```"""
    )},
    {"type": "md", "src": tu_turno(11,
        """Define una funcion `crear_perfil(**kwargs)` que reciba cualquier numero de campos por nombre. La funcion debe:

1. Imprimir el numero de campos recibidos.
2. Comprobar si tiene la clave `'email'`. Si no, anadirla con valor `'no especificado'`.
3. Devolver el dict resultante.

Pruebala con: `crear_perfil(nombre='Ana', edad=30, ciudad='Madrid')`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def crear_perfil(**kwargs):\n#     print(f'Campos recibidos: {len(kwargs)}')\n#     if 'email' not in kwargs:\n#         kwargs['email'] = 'no especificado'\n#     return kwargs\n#\n# perfil = crear_perfil(nombre='Ana', edad=30, ciudad='Madrid')\n# print(perfil)\n"},
]))

# ============ DESEMPAQUETADO ============
plan.append((ID_DESEMPAQUETADO, [
    {"type": "md", "src": teoria(
        "Desempaquetado al LLAMAR: <code>*</code> y <code>**</code> en la invocacion",
        """Hasta ahora has visto `*` y `**` en la **firma** (la definicion). Tambien funcionan **en la llamada**, pero al reves: para "explotar" colecciones en argumentos.

| En definicion | En llamada |
|---|---|
| `def f(*args):` -> recoge en tupla | `f(*lista)` -> explota la lista |
| `def f(**kwargs):` -> recoge en dict | `f(**dict)` -> explota el dict |

#### `*` para listas/tuplas en la llamada

```python
def punto(x, y, z):
    print(x, y, z)

coords = [1, 2, 3]
punto(*coords)           # equivale a punto(1, 2, 3)
```

Si la lista no tiene la longitud correcta, da error.

#### `**` para dicts en la llamada

```python
def configurar(host, puerto):
    print(host, puerto)

cfg = {'host': 'localhost', 'puerto': 8080}
configurar(**cfg)        # equivale a configurar(host='localhost', puerto=8080)
```

Las claves del dict tienen que **coincidir con los nombres** de los parametros.

#### Caso clasico: pasar argumentos de una funcion a otra

```python
def wrapper(*args, **kwargs):
    print('Llamando a la funcion real con', args, kwargs)
    return funcion_real(*args, **kwargs)
```

Esto es la base de los **decoradores**, que ahora veras."""
    )},
    {"type": "md", "src": tu_turno(12,
        """Tienes esta funcion ya definida:

```python
def saludar(nombre, edad, ciudad):
    return f'{nombre}, {edad} anios, {ciudad}'
```

Tambien tienes una **lista** `datos_lista = ['Ana', 30, 'Madrid']` y un **dict** `datos_dict = {'nombre': 'Pedro', 'edad': 25, 'ciudad': 'Lugo'}`. Llama a `saludar` UNA vez usando `*` y otra usando `**`. Imprime ambos resultados."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\ndef saludar(nombre, edad, ciudad):\n    return f'{nombre}, {edad} anios, {ciudad}'\n\ndatos_lista = ['Ana', 30, 'Madrid']\ndatos_dict  = {'nombre': 'Pedro', 'edad': 25, 'ciudad': 'Lugo'}\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def saludar(nombre, edad, ciudad):\n#     return f'{nombre}, {edad} anios, {ciudad}'\n#\n# datos_lista = ['Ana', 30, 'Madrid']\n# datos_dict  = {'nombre': 'Pedro', 'edad': 25, 'ciudad': 'Lugo'}\n#\n# print(saludar(*datos_lista))    # explota la lista en posicionales\n# print(saludar(**datos_dict))    # explota el dict en keyword args\n"},
]))

# ============ LAMBDA ============
plan.append((ID_LAMBDA_HEAD, [
    {"type": "md", "src": teoria(
        "Funciones lambda: funciones anonimas en una linea",
        """Una **lambda** es una funcion **anonima** (sin nombre), normalmente corta, escrita en una sola linea.

```python
# Sintaxis:
lambda parametros: expresion

# Ejemplo:
doblar = lambda x: x * 2
doblar(5)      # 10
```

#### Como se compara con `def`?

```python
# Equivalente con def:
def doblar(x):
    return x * 2
```

La unica diferencia tecnica relevante: una lambda **es una expresion**, asi que puedes ponerla en sitios donde una `def` no cabe (dentro de un argumento, en una lista, etc.).

| Aspecto | `def` | `lambda` |
|---|---|---|
| Tiene nombre | Si | No (a menos que la asignes) |
| Cuerpo | Multilinea | Solo UNA expresion |
| `return` | Necesario | Implicito (devuelve la expresion) |
| Uso tipico | logica reutilizable | argumento corto en `map`, `filter`, `sorted`, `key=...` |
| Acepta `*args`, `**kwargs`, defaults | Si | Si |

#### Cuando usar lambda?

Para funciones **muy cortas y de un solo uso**, sobre todo como argumento:

```python
sorted([(3, 'c'), (1, 'a'), (2, 'b')], key=lambda t: t[1])  # ordena por la letra
list(map(lambda x: x ** 2, [1, 2, 3]))                       # [1, 4, 9]
list(filter(lambda x: x > 0, [-1, 2, -3, 4]))                # [2, 4]
```

#### Cuando NO usar lambda?

- Si la logica es larga o tiene varias lineas: usa `def`.
- Si necesitas docstring: usa `def`.
- Si la vas a reutilizar mucho: dale un nombre real con `def`."""
    )},
]))

plan.append((ID_LAMBDA_FORMATO, [
    {"type": "md", "src": tu_turno(13,
        """Convierte estas funciones `def` en lambdas y guardalas en variables:

1. Una funcion que dado un numero diga si es **par** (devuelve `True`/`False`).
2. Una funcion que reciba un string y devuelva su **longitud**.
3. Una funcion que reciba dos numeros y devuelva su **producto**.

Despues, ejecuta cada una con un valor de prueba e imprime el resultado."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# es_par     = lambda n: n % 2 == 0\n# longitud   = lambda s: len(s)\n# producto   = lambda a, b: a * b\n#\n# print(es_par(4))            # True\n# print(longitud('python'))   # 6\n# print(producto(3, 7))       # 21\n"},
]))

plan.append((ID_LAMBDA_LISTA, [
    {"type": "md", "src": tu_turno(14,
        """Tienes una lista de tuplas `personas = [('Ana', 30), ('Pedro', 22), ('Lucia', 45)]`. Usa `sorted` con una **lambda** como `key` para ordenar la lista por **edad** (segundo elemento de cada tupla).

> Resultado esperado: `[('Pedro', 22), ('Ana', 30), ('Lucia', 45)]`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\npersonas = [('Ana', 30), ('Pedro', 22), ('Lucia', 45)]\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# personas = [('Ana', 30), ('Pedro', 22), ('Lucia', 45)]\n# ordenadas = sorted(personas, key=lambda p: p[1])\n# print(ordenadas)\n"},
]))

plan.append((ID_DICT_SWITCH, [
    {"type": "md", "src": tu_turno(15,
        """Crea un diccionario llamado `operaciones` que mapee strings a funciones lambda:

- `'sumar'` -> lambda que suma dos numeros.
- `'restar'` -> lambda que resta.
- `'multiplicar'` -> lambda que multiplica.
- `'dividir'` -> lambda que divide.

Despues, escribe una funcion `calcular(op, a, b)` que use el dict para escoger la operacion y la aplique. Pruebala con `calcular('sumar', 3, 4)` y `calcular('dividir', 10, 2)`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# operaciones = {\n#     'sumar':       lambda a, b: a + b,\n#     'restar':      lambda a, b: a - b,\n#     'multiplicar': lambda a, b: a * b,\n#     'dividir':     lambda a, b: a / b,\n# }\n#\n# def calcular(op, a, b):\n#     funcion = operaciones.get(op)\n#     if funcion is None:\n#         return 'Operacion no valida'\n#     return funcion(a, b)\n#\n# print(calcular('sumar', 3, 4))     # 7\n# print(calcular('dividir', 10, 2))  # 5.0\n"},
]))

# ============ RECURSION ============
plan.append((ID_RECURSION_HEAD, [
    {"type": "md", "src": teoria(
        "Recursividad: funciones que se llaman a si mismas",
        """Una funcion **recursiva** es una funcion que **se llama a si misma** durante su ejecucion. Es una tecnica para resolver problemas que se pueden descomponer en versiones mas pequenas del mismo problema.

#### Las dos partes obligatorias

| Parte | Que hace | Si falta... |
|---|---|---|
| **Caso base** | Detiene la recursion | bucle infinito -> `RecursionError` |
| **Caso recursivo** | Llama a la funcion con un problema mas pequeno | nunca progresa hacia el caso base |

#### El ejemplo clasico: factorial

`n!` se define como:
- `0! = 1`         (caso base)
- `n! = n * (n-1)!` (caso recursivo)

```python
def factorial(n):
    if n == 0:        # caso base
        return 1
    return n * factorial(n - 1)   # caso recursivo

factorial(5)    # 120
```

Como se ejecuta `factorial(3)`?

```
factorial(3) = 3 * factorial(2)
             = 3 * (2 * factorial(1))
             = 3 * (2 * (1 * factorial(0)))
             = 3 * (2 * (1 * 1))
             = 6
```

#### Cuando usar recursion?

- **Problemas con estructura recursiva natural**: arboles, grafos, fractales, divide y venceras (ej. quicksort, busqueda binaria).
- **Algoritmos elegantes**: a veces la version recursiva es 5 lineas y la iterativa 30.

#### Cuando NO usar recursion?

- **Bucles simples**: un `for` es mas rapido y no consume pila.
- **Mucha profundidad**: Python tiene un limite (`sys.setrecursionlimit`, ~1000 por defecto).
- **Sin caso base claro**: te metes en `RecursionError`."""
    )},
    {"type": "md", "src": aviso(
        """**Errores tipicos en recursion:**

1. **Olvidar el caso base** -> `RecursionError: maximum recursion depth exceeded`.
2. **Caso base inalcanzable**: el problema no se reduce. Ej: `f(n)` llama a `f(n)` o `f(n+1)`.
3. **Mucha profundidad**: para listas grandes, prefiere bucles.
4. **Repetir calculos**: `fibonacci(n)` recursivo recalcula los mismos valores miles de veces. Solucion: memoizacion (`functools.lru_cache`)."""
    )},
    {"type": "md", "src": tu_turno(16,
        """Escribe una funcion **recursiva** `suma_hasta(n)` que devuelva la suma de los enteros de 1 a `n`. Es decir, `suma_hasta(4) = 1+2+3+4 = 10`.

- Caso base: `suma_hasta(0) = 0`.
- Caso recursivo: `suma_hasta(n) = n + suma_hasta(n-1)`.

Pruebala con `suma_hasta(5)` (debe dar 15) y `suma_hasta(10)` (debe dar 55)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def suma_hasta(n):\n#     if n == 0:               # caso base\n#         return 0\n#     return n + suma_hasta(n - 1)   # caso recursivo\n#\n# print(suma_hasta(5))    # 15\n# print(suma_hasta(10))   # 55\n"},
]))

plan.append((ID_FACTORIAL, [
    {"type": "md", "src": tu_turno(17,
        """Escribe una funcion recursiva `cuenta_atras(n)` que imprima los numeros de `n` a 1 y al final imprima `'Despegue!'`. Si `n <= 0`, no debe hacer nada.

Pruebala con `cuenta_atras(5)`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def cuenta_atras(n):\n#     if n <= 0:\n#         print('Despegue!')\n#         return\n#     print(n)\n#     cuenta_atras(n - 1)\n#\n# cuenta_atras(5)\n# # 5\n# # 4\n# # 3\n# # 2\n# # 1\n# # Despegue!\n"},
]))

# ============ SCOPES ============
plan.append((ID_SCOPES_HEAD, [
    {"type": "md", "src": teoria(
        "Scope (alcance): donde puedes ver una variable",
        """El **scope** de una variable es la zona del codigo desde donde puedes acceder a ella. En Python NO se decide por las llaves (no hay), se decide por la **funcion donde la asignes** y por una regla llamada **LEGB**.

#### Por que importa?

```python
def f():
    x = 10        # x vive solo dentro de f
    print(x)

f()
print(x)          # NameError: name 'x' is not defined
```

La variable `x` esta en el scope **local** de `f`. Fuera de `f`, no existe.

#### Cuatro scopes: L-E-G-B

| Letra | Scope | Donde |
|---|---|---|
| **L** | Local | Dentro de la funcion actual. |
| **E** | Enclosing | En funciones que envuelven a la actual (anidadas). |
| **G** | Global | A nivel de modulo (archivo `.py`). |
| **B** | Built-in | Lo que viene de serie con Python (`len`, `print`, `range`...). |

Cuando escribes `x` en una funcion, Python busca en este orden: **L -> E -> G -> B**. Si no la encuentra, `NameError`.

```python
x = 'global'                    # G

def fuera():
    x = 'enclosing'             # E (relativo a 'dentro')
    def dentro():
        x = 'local'             # L
        print(x)                # 'local'
    dentro()

fuera()
print(x)                        # 'global'
```"""
    )},
]))

plan.append((ID_LEGB, [
    {"type": "md", "src": tu_turno(18,
        """Escribe el siguiente codigo y predice ANTES de ejecutarlo que va a imprimir cada `print`:

```python
x = 'GLOBAL'

def exterior():
    x = 'EXTERIOR'
    def interior():
        x = 'INTERIOR'
        print('1.', x)
    interior()
    print('2.', x)

exterior()
print('3.', x)
```

> Resultado esperado: `INTERIOR`, `EXTERIOR`, `GLOBAL`. Si comentas la asignacion en `interior`, observa como cambia el `1.`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# x = 'GLOBAL'\n#\n# def exterior():\n#     x = 'EXTERIOR'\n#     def interior():\n#         x = 'INTERIOR'\n#         print('1.', x)\n#     interior()\n#     print('2.', x)\n#\n# exterior()\n# print('3.', x)\n# # 1. INTERIOR\n# # 2. EXTERIOR\n# # 3. GLOBAL\n"},
]))

plan.append((ID_GLOBAL, [
    {"type": "md", "src": teoria(
        "<code>global</code>: modificar variables globales desde una funcion",
        """Por defecto, si **asignas** a una variable dentro de una funcion, Python la considera **local** (aunque exista una global con el mismo nombre).

```python
contador = 0

def incrementar():
    contador = contador + 1     # ERROR! UnboundLocalError
```

Por que falla? Python ve la asignacion `contador = ...` y marca `contador` como local. Cuando intenta evaluar la parte derecha, todavia no tiene valor local, asi que falla.

#### Solucion: declarar `global`

```python
contador = 0

def incrementar():
    global contador             # AVISA: voy a usar la variable global
    contador = contador + 1

incrementar()
incrementar()
print(contador)                  # 2
```

#### Cuando usar `global`?

**Casi nunca.** Es una mala practica en codigo grande porque:

- Hace dificil seguir de donde vienen los cambios.
- Crea acoplamiento entre funciones.
- Complica las pruebas unitarias.

**Mejor alternativa:** devolver el nuevo valor:

```python
def incrementar(c):
    return c + 1

contador = 0
contador = incrementar(contador)
```

#### Detalle importante

Para **leer** una variable global, NO necesitas `global`:

```python
nombre_app = 'MiApp'

def saludar():
    print(nombre_app)        # OK, solo lee. Lo encuentra en G.
```

Solo necesitas `global` cuando vas a **modificar / asignar**."""
    )},
    {"type": "md", "src": tu_turno(19,
        """Define una variable global `clicks = 0`. Despues, escribe una funcion `click()` que **incremente** `clicks` en 1 cada vez que se llama. Llamala 5 veces e imprime el resultado final.

> Resultado esperado: `clicks = 5`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# clicks = 0\n#\n# def click():\n#     global clicks\n#     clicks += 1\n#\n# for _ in range(5):\n#     click()\n#\n# print(f'clicks = {clicks}')   # 5\n"},
]))

# ============ CLOSURES ============
plan.append((ID_CLOSURES, [
    {"type": "md", "src": teoria(
        "Closures: funciones que recuerdan su contexto",
        """Una **closure** es una funcion **definida dentro de otra** que **recuerda las variables** del scope donde nacio, **incluso despues de que ese scope haya terminado**.

```python
def hacer_multiplicador(n):
    def multiplicar(x):
        return x * n           # 'n' viene del enclosing scope
    return multiplicar

doblar = hacer_multiplicador(2)
triplicar = hacer_multiplicador(3)

print(doblar(5))      # 10
print(triplicar(5))   # 15
```

`doblar` y `triplicar` son la misma funcion `multiplicar`, pero **cada una recuerda su propio `n`**. Eso es una closure.

#### Para que sirve?

| Uso | Ejemplo |
|---|---|
| **Function factories** | crear funciones especializadas (como arriba). |
| **Configuracion** | `crear_logger(nivel='DEBUG')` devuelve un logger con ese nivel preconfigurado. |
| **Decoradores** | son closures que envuelven otras funciones. |
| **Mantener estado privado** | un contador que solo la funcion devuelta puede tocar. |

#### Closure vs clase

Las closures son una alternativa **ligera** a tener una clase con un solo metodo. Si necesitas mas estado o mas metodos, usa una clase. Para casos simples, una closure es mas concisa."""
    )},
    {"type": "md", "src": tu_turno(20,
        """Crea una funcion `crear_contador()` que devuelva una funcion **interna** sin parametros. Cada vez que llames a la funcion interna, debe **devolver el siguiente numero** empezando por 1.

Pista: usa `nonlocal` (lo veras en la siguiente seccion) o ponlo en una lista (truco viejo: `[0]` y muta el indice 0).

> Comportamiento:
> ```
> contador = crear_contador()
> contador()  # 1
> contador()  # 2
> contador()  # 3
> ```"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def crear_contador():\n#     n = 0\n#     def siguiente():\n#         nonlocal n\n#         n += 1\n#         return n\n#     return siguiente\n#\n# contador = crear_contador()\n# print(contador())   # 1\n# print(contador())   # 2\n# print(contador())   # 3\n#\n# # Cada contador es independiente:\n# otro = crear_contador()\n# print(otro())       # 1 (empieza en 1 porque es otra closure)\n"},
]))

# ============ NONLOCAL ============
plan.append((ID_NONLOCAL, [
    {"type": "md", "src": teoria(
        "<code>nonlocal</code>: modificar variables del enclosing",
        """Hermana pequena de `global`. Sirve para **modificar** una variable del scope **enclosing** (no global) desde una funcion anidada.

```python
def fuera():
    x = 10
    def dentro():
        nonlocal x        # quiero modificar la x del enclosing, no crear una local
        x += 1
    dentro()
    print(x)              # 11

fuera()
```

#### Comparacion con global

| Sentencia | Que hace |
|---|---|
| `global x` | "use la x del scope GLOBAL". |
| `nonlocal x` | "use la x del scope **inmediatamente exterior** (que NO sea global)". |

#### Sin nonlocal vs con nonlocal

```python
def fuera():
    x = 10
    def dentro():
        x = 99            # crea una x LOCAL (la del enclosing no se toca)
    dentro()
    print(x)              # 10
```

```python
def fuera():
    x = 10
    def dentro():
        nonlocal x
        x = 99            # MODIFICA la x del enclosing
    dentro()
    print(x)              # 99
```

#### Para que se usa en la practica?

Casi siempre con **closures que mantienen estado**: contadores, acumuladores, caches manuales..."""
    )},
    {"type": "md", "src": tu_turno(21,
        """Crea una funcion `crear_acumulador(inicio=0)` que devuelva otra funcion `add(n)`. Cada vez que llames a `add(n)`, debe **sumar `n`** al acumulador interno y devolver el total acumulado.

> Comportamiento:
> ```
> acc = crear_acumulador(10)
> acc(5)    # 15
> acc(3)    # 18
> acc(2)    # 20
> ```"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def crear_acumulador(inicio=0):\n#     total = inicio\n#     def add(n):\n#         nonlocal total\n#         total += n\n#         return total\n#     return add\n#\n# acc = crear_acumulador(10)\n# print(acc(5))   # 15\n# print(acc(3))   # 18\n# print(acc(2))   # 20\n"},
]))

# ============ DECORADORES (BONUS) ============
plan.append((ID_EJERCICIOS, [
    {"type": "md", "src": teoria(
        "Decoradores: funciones que envuelven otras funciones",
        """Un **decorador** es una funcion que **recibe otra funcion** y **devuelve una version modificada** de ella. Sirve para anadir comportamiento (logging, control de tiempo, autenticacion, cache...) **sin tocar la funcion original**.

#### Idea basica

```python
def mi_decorador(funcion):
    def envoltorio(*args, **kwargs):
        print('Antes de llamar')
        resultado = funcion(*args, **kwargs)
        print('Despues de llamar')
        return resultado
    return envoltorio

def saludar(nombre):
    print(f'Hola {nombre}')

# Aplicar el decorador manualmente:
saludar = mi_decorador(saludar)

saludar('Lucas')
# Antes de llamar
# Hola Lucas
# Despues de llamar
```

#### Sintaxis con `@`: azucar de Python

```python
@mi_decorador
def saludar(nombre):
    print(f'Hola {nombre}')

# Equivale exactamente a:
# saludar = mi_decorador(saludar)
```

#### Ejemplo util: cronometrar funciones

```python
import time

def cronometro(funcion):
    def envoltorio(*args, **kwargs):
        inicio = time.time()
        resultado = funcion(*args, **kwargs)
        fin = time.time()
        print(f'{funcion.__name__} tardo {fin - inicio:.4f} s')
        return resultado
    return envoltorio

@cronometro
def trabajar():
    suma = 0
    for i in range(10_000_000):
        suma += i
    return suma

trabajar()
# trabajar tardo 0.4523 s
```

#### Decoradores famosos en la libreria estandar

| Decorador | Que hace |
|---|---|
| `@property` | convierte un metodo en un atributo de solo lectura. |
| `@staticmethod` | declara un metodo estatico de clase. |
| `@classmethod` | declara un metodo de clase. |
| `@functools.lru_cache` | cachea resultados por argumentos (memoizacion). |
| `@dataclass` | autogenera `__init__`, `__repr__`, etc. |

> Los decoradores usan TODO lo que has aprendido: funciones como objetos, closures, `*args`/`**kwargs`. Ahora que dominas eso, los decoradores son solo una sintaxis comoda."""
    )},
    {"type": "md", "src": tu_turno(22,
        """Crea un decorador `con_log` que, cada vez que se llame a la funcion decorada, imprima:

1. Antes: `'Llamando a <nombre_funcion>'` (usa `funcion.__name__`).
2. Despues: `'Termino <nombre_funcion>'`.
3. Devuelva el resultado original sin modificarlo.

Despues, decora una funcion `sumar(a, b)` con `@con_log` y llamala con `sumar(3, 4)`. Imprime el resultado.

> Salida esperada:
> ```
> Llamando a sumar
> Termino sumar
> 7
> ```"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def con_log(funcion):\n#     def envoltorio(*args, **kwargs):\n#         print(f'Llamando a {funcion.__name__}')\n#         resultado = funcion(*args, **kwargs)\n#         print(f'Termino {funcion.__name__}')\n#         return resultado\n#     return envoltorio\n#\n# @con_log\n# def sumar(a, b):\n#     return a + b\n#\n# print(sumar(3, 4))\n"},
    {"type": "md", "src": dato(
        """**Has llegado al final del notebook de funciones!**

Resumen de lo que dominas ahora:

| Concepto | Para que sirve |
|---|---|
| `def` y `return` | Definir y devolver. |
| Parametros (posicional, default, keyword) | Distintas formas de llamar. |
| `*args`, `**kwargs` | Numero variable de argumentos. |
| Type hints | Documentar tipos. |
| `lambda` | Funciones cortas en una linea. |
| Recursividad | Resolver problemas que se repiten en escala menor. |
| LEGB y `global` / `nonlocal` | Saber donde vive cada variable. |
| Closures y decoradores | Funciones que recuerdan o envuelven otras. |

Sigue practicando con los ejercicios del profesor que vienen abajo. Ahi estan los **9 ejercicios oficiales** con sus soluciones."""
    )},
]))


enhance(NB, plan)
print("Done.")

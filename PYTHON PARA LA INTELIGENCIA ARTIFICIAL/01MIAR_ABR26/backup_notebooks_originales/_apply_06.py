"""Aplica mejoras al notebook 06_OOP con bloques de colores y teoria detallada."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, solucion_md, dato, aviso
import json

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_06_Python101_OOP.ipynb"

nb = json.load(open(NB, encoding="utf-8"))


def find_id(fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if fragment in src:
            return c["id"]
    return None


# ---- Mapeo de IDs (usa fragmentos UNICOS de cada celda) ----
ID_TITULO            = nb["cells"][0]["id"]                                # img viu_logo
ID_QUE_CLASES        = find_id("Qu") and find_id("son las clases")         # 3
ID_IMG_EMPLEADO      = find_id("class_employee.png")                       # 5
ID_LENG_DIN          = find_id("Lenguajes est")                            # 6
ID_FIRST_CODE        = find_id("Definici")                                  # 8 (primer codigo Empleado)
ID_INIT_BASIC        = find_id("nombre_empleado")                          # 9 - codigo init
ID_DEF_COMPORT       = find_id("c") and find_id("mo puedo definir comport") # 10
ID_SELF              = find_id("### Self")                                 # 13
ID_CONSTR            = find_id("### Constructor")                          # 14
ID_INIT_DESC         = find_id("se invoca al crear instancias de la clase") # 15
ID_PERSONA_CODE      = find_id("class Persona():")                         # 16
ID_DOT_NOTATION      = find_id("notaci") and find_id("'.'")                # 17
ID_DATOS_INST_CLS    = find_id("Datos y comportamiento de instancia y de clase") # 19
ID_EMP_GOOGLE        = find_id('empresa = "Google"')                       # 21
ID_HERENCIA          = find_id("## Herencia")                              # 22
ID_HERENCIA_CODE     = find_id("class Persona:") and find_id("def presentar(self):") # 25
ID_SINTAXIS_GEN      = find_id("Sintaxis general de la sentencia")         # 26
ID_VISIBILIDAD       = find_id("## Visibilidad")                           # 28
ID_PUBLICO           = find_id("### P") and find_id("blico")               # 30
ID_PUB_CODE          = find_id("schoolName = 'XYZ School'")                # 31
ID_PROTEGIDO         = find_id("### Protegido")                            # 33
ID_PRIV              = find_id("### Privado")                              # 36
ID_PRIV_CODE         = find_id("__schoolName")                             # 37
ID_EXT_VS_REPL       = find_id("Extensi") and find_id("reemplazo")         # 39
ID_DELEGACION        = find_id("Delegaci") and find_id("clases abstractas") # 45
ID_PYTHON3X          = find_id("#### En Python 3.X")                       # 50
ID_ABC_CODE          = find_id("from abc import ABC")                      # 52
ID_DECORADORES       = find_id("#### Decoradores")                         # 53
ID_STATIC_CODE       = find_id("@staticmethod")                            # 54 (Calculator)
ID_CLASSMETHOD_CODE  = find_id("@classmethod")                             # 55
ID_PROPERTY_GETTER   = find_id("Property, se usa como getter")             # 56
ID_PROPERTY_SETTER   = find_id("Property setter")                          # 59
ID_PROPERTY_DEL      = find_id("Property deleter")                         # 62
ID_OP_OVERLOAD       = find_id("Sobreescritura de operadores")             # 65
ID_OP_DEFAULT        = find_id("no hay comportamiento por defecto")        # 68
ID_STR_EXAMPLE       = find_id("utilizado, por ejemplo, por *print*")      # 70
ID_OP_OTHERS         = find_id("Otros ejemplos de operadores")             # 74
ID_OP_OTHERS_CODE    = find_id("def __sub__")                              # 75
ID_VENTAJAS          = find_id("Ventajas de la Programaci")                # 77
ID_REUTIL            = find_id("#### Reutilizaci")                         # 78
ID_POLIMORFISMO      = find_id("#### Polimorfismo")                        # 79
ID_POLI_CODE         = find_id("emitir_sonidos")                           # 80
ID_BUSQUEDA          = find_id("squeda de atributos")                      # 81
ID_EJERCICIOS        = find_id("## Ejercicios")                            # 93


plan = []

# ============================ INTRO ============================
plan.append((ID_TITULO, [
    {"type": "md", "src": teoria(
        "Como leer este notebook (version mejorada)",
        """Este notebook fue **enriquecido** para ayudarte a aprender escribiendo codigo. Encontraras tres tipos de bloques de colores:

<div style="background-color:#e7f5ff;border-left:6px solid #1c7ed6;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AZUL = TEORIA</b></div> -> explicacion en palabras simples antes de cada concepto.

<div style="background-color:#fff9db;border-left:6px solid #f59f00;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AMARILLO = TU TURNO</b></div> -> el ejercicio que TU debes resolver. Hay una celda vacia debajo donde escribes el codigo.

<div style="background-color:#ebfbee;border-left:6px solid #2f9e44;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>VERDE = SOLUCION</b></div> -> codigo de referencia comentado por si te trabas. Destapa solo despues de intentar.

> **Promesa importante**: el codigo y la teoria del profesor original no se han tocado. Solo se han ANADIDO bloques. Asi puedes seguir comparando con la version original cuando quieras.

#### Mapa mental del notebook

1. **Que son las clases y los objetos** (la idea fundamental).
2. **Como definirlas**: `class`, `__init__`, `self`.
3. **Atributos**: de instancia vs de clase.
4. **Metodos** y la notacion `objeto.metodo()`.
5. **Herencia** y `super()`.
6. **Visibilidad**: publico, protegido (`_`), privado (`__`).
7. **Clases abstractas** y delegacion.
8. **Decoradores** OOP: `@staticmethod`, `@classmethod`, `@property`.
9. **Metodos especiales** (`__init__`, `__str__`, `__add__`, ...).
10. **Polimorfismo** y busqueda de atributos."""
    )},
]))

# ============================ QUE ES UNA CLASE ============================
plan.append((ID_QUE_CLASES, [
    {"type": "md", "src": teoria(
        "Que es una clase, una instancia y un objeto?",
        """La **Programacion Orientada a Objetos (OOP)** es una forma de organizar el codigo agrupando **datos** (atributos) y **comportamiento** (metodos) en una unidad llamada **objeto**.

#### Analogia: el plano y la casa

Piensalo asi:

- Una **clase** es como un **plano de arquitecto** para construir una casa. Define que tendra (puertas, ventanas, habitaciones) y que se podra hacer en ella (abrir puertas, encender luces). El plano no es la casa.
- Una **instancia** (u objeto) es la **casa construida** a partir del plano. Cada casa puede tener distintos colores, propietarios o muebles, pero comparte la misma estructura.

```
Clase   : Coche             (el plano)
Objetos : mi_coche, tu_coche (las instancias creadas con ese plano)
```

#### En Python TODO es un objeto

Hasta los numeros y los strings:

```python
type(3)        # <class 'int'>
type("hola")   # <class 'str'>
type([1, 2])   # <class 'list'>
```

Cada tipo de dato es una **clase**, y cada valor concreto es una **instancia** de esa clase.

#### Que ganamos al hacer nuestras propias clases?

| Ventaja | Detalle |
|---|---|
| **Encapsulacion** | Datos y comportamiento juntos en un solo lugar. |
| **Reutilizacion** | Crear muchos objetos del mismo tipo sin repetir codigo. |
| **Herencia** | Construir una clase a partir de otra ya existente. |
| **Polimorfismo** | Distintos objetos pueden responder a los mismos mensajes. |
| **Abstraccion** | Esconder detalles internos y exponer solo lo necesario. |

#### Tabla comparativa: clase vs instancia

| Aspecto | Clase | Instancia |
|---|---|---|
| Que es | El plano / molde | El objeto concreto creado |
| Cuantas | Una por tipo | Muchas (`mi_coche`, `tu_coche`, ...) |
| Sintaxis | `class Coche:` | `mi_coche = Coche()` |
| Datos | Compartidos por todas | Propios de cada objeto |
| Ejemplo real | El concepto 'Persona' | Tu, yo, tu vecino |"""
    )},
]))

# ============================ DEFINICION class ============================
plan.append((ID_FIRST_CODE, [
    {"type": "md", "src": teoria(
        "La sentencia <code>class</code>: anatomia minima",
        """La forma mas basica de declarar una clase en Python es:

```python
class NombreClase:
    pass
```

`pass` es un marcador de posicion: 'aqui no hay nada todavia, pero la clase es valida'.

#### Convenciones de nombres (PEP 8)

| Cosa | Estilo | Ejemplo |
|---|---|---|
| Clase | `CamelCase` | `Empleado`, `MiClaseGenial` |
| Funcion / metodo | `snake_case` | `calcular_total`, `presentar()` |
| Constante | `MAYUSCULAS` | `PI = 3.14` |
| Atributo privado | `_` o `__` al inicio | `_saldo`, `__id` |

#### Crear una instancia (instanciacion)

```python
mi_obj = NombreClase()   # los parentesis llaman al 'constructor'
```

Aqui pasan **dos cosas a la vez**:

1. Python crea un objeto vacio en memoria.
2. Llama al metodo `__init__` (si existe) para inicializarlo.

#### Diferencia: definicion vs instanciacion

| Definicion | Instanciacion |
|---|---|
| Escribir el plano (`class`) | Construir una casa con ese plano |
| Se hace UNA vez | Se hace tantas veces como objetos quieras |
| `class Empleado:` | `e1 = Empleado()` |"""
    )},
]))

# ============================ __init__ y self ============================
plan.append((ID_SELF, [
    {"type": "md", "src": teoria(
        "<code>self</code>: el yo del objeto",
        """`self` es la palabra magica de OOP en Python. Aunque no es palabra reservada, **por convencion** todos los metodos de instancia reciben como **primer parametro** una referencia al objeto sobre el que fueron llamados, y la llamamos `self`.

#### Que es exactamente?

Cuando haces:

```python
mi_emp.presentar()
```

Python lo traduce internamente a:

```python
Empleado.presentar(mi_emp)   # mi_emp se pasa como self
```

Es decir, `self` es el **objeto actual**, el que esta a la izquierda del punto.

#### Por que se llama 'self'?

Solo es una **convencion**. Podrias llamarlo `yo`, `this` o `pepito`, pero **NUNCA** lo hagas: cualquier programador Python espera ver `self`.

#### Para que sirve self dentro de los metodos?

| Uso | Codigo |
|---|---|
| Leer un atributo del objeto | `self.nombre` |
| Modificar un atributo | `self.nombre = 'Ana'` |
| Crear un atributo nuevo | `self.edad = 30` (basta con asignar) |
| Llamar a otro metodo del mismo objeto | `self.presentar()` |

#### Ejemplo paso a paso

```python
class Empleado:
    def __init__(self, nombre):    # self <- empleado nuevo
        self.nombre = nombre        # asigna atributo al objeto

    def saludar(self):              # self <- empleado actual
        print(f'Hola, soy {self.nombre}')

e1 = Empleado('Ana')   # __init__ se llama con self=e1
e2 = Empleado('Pepe')  # __init__ se llama con self=e2

e1.saludar()           # equivale a Empleado.saludar(e1) -> 'Hola, soy Ana'
e2.saludar()           # equivale a Empleado.saludar(e2) -> 'Hola, soy Pepe'
```

Las dos instancias comparten el **codigo** del metodo, pero `self` es distinto en cada llamada."""
    )},
]))

plan.append((ID_INIT_DESC, [
    {"type": "md", "src": teoria(
        "<code>__init__</code>: el constructor",
        """`__init__` es un **metodo especial** (los que tienen doble guion bajo a cada lado se llaman *dunder*, de *double underscore*). Python lo invoca **automaticamente** justo despues de crear una instancia.

#### Funciones tipicas del __init__

1. **Recibir** los datos iniciales que el objeto necesita.
2. **Guardarlos** como atributos en `self`.
3. (Opcional) **Validar** que los datos son correctos.
4. (Opcional) **Llamar** al `__init__` de la clase padre con `super().__init__(...)`.

```python
class Persona:
    def __init__(self, nombre, edad):
        if edad < 0:
            raise ValueError('La edad no puede ser negativa')
        self.nombre = nombre
        self.edad = edad
```

#### Cuidado con los argumentos por defecto MUTABLES

Esta es una de las **trampas mas famosas de Python**:

```python
class MalEjemplo:
    def __init__(self, items=[]):     # MAL: la lista se crea UNA sola vez
        self.items = items
        self.items.append('x')

a = MalEjemplo()
b = MalEjemplo()
print(a.items)   # ['x', 'x']  <- compartido entre a y b!
print(b.items)   # ['x', 'x']
```

Lo correcto es usar `None` como sentinel:

```python
class BienEjemplo:
    def __init__(self, items=None):
        self.items = items if items is not None else []
        self.items.append('x')
```

| Argumento por defecto | Seguro? |
|---|---|
| `int`, `float`, `str`, `tuple`, `None` (inmutables) | Si |
| `list`, `dict`, `set` (mutables) | NO -> usa `None` |"""
    )},
    {"type": "md", "src": tu_turno(1,
        """Define una clase `Libro` con un constructor `__init__` que reciba `titulo`, `autor` y `paginas`. Guarda los tres como atributos. Despues:

1. Crea dos instancias distintas: `libro1 = Libro('Cien anios de soledad', 'Garcia Marquez', 471)` y `libro2 = Libro('1984', 'Orwell', 326)`.
2. Imprime `titulo` y `paginas` de cada uno.

> Resultado esperado:
>
> ```
> Cien anios de soledad - 471 paginas
> 1984 - 326 paginas
> ```"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# class Libro:\n#     def __init__(self, titulo, autor, paginas):\n#         # self apunta a la instancia recien creada\n#         self.titulo = titulo\n#         self.autor = autor\n#         self.paginas = paginas\n#\n# libro1 = Libro('Cien anios de soledad', 'Garcia Marquez', 471)\n# libro2 = Libro('1984', 'Orwell', 326)\n#\n# # Accedemos a los atributos con notacion punto:\n# print(f'{libro1.titulo} - {libro1.paginas} paginas')\n# print(f'{libro2.titulo} - {libro2.paginas} paginas')\n"},
]))

# ============================ NOTACION PUNTO ============================
plan.append((ID_DOT_NOTATION, [
    {"type": "md", "src": teoria(
        "La notacion punto: <code>objeto.atributo</code>",
        """La **notacion punto** es la forma en que accedes a TODO lo que esta dentro de un objeto: tanto sus datos (atributos) como sus comportamientos (metodos).

```python
mi_obj.atributo            # leer un dato
mi_obj.atributo = 5        # modificar un dato
mi_obj.metodo()            # llamar a un metodo (los parentesis lo invocan)
mi_obj.metodo              # NO llama, solo obtiene la referencia al metodo
```

#### Patrones comunes

```python
persona = Persona('Ana', 30)

# Leer
print(persona.nombre)         # Ana

# Modificar
persona.edad = 31

# Anadir un atributo NUEVO (Python te deja!)
persona.profesion = 'Ingeniera'

# Borrar un atributo
del persona.profesion

# Comprobar si existe
hasattr(persona, 'nombre')    # True
getattr(persona, 'nombre')    # 'Ana'
getattr(persona, 'altura', 0) # 0  (valor por defecto si no existe)
setattr(persona, 'altura', 170)
```

> **Curiosidad**: Python permite **anadir atributos en caliente** despues de crear el objeto. Esto es muy flexible pero peligroso. Lo veras de nuevo cuando estudiemos `__slots__` (mas adelante)."""
    )},
]))

# ============================ ATRIBUTOS DE CLASE VS INSTANCIA ============================
plan.append((ID_DATOS_INST_CLS, [
    {"type": "md", "src": teoria(
        "Atributos de instancia vs atributos de clase",
        """Esta es una de las confusiones mas comunes. Lee con calma.

#### Atributo de instancia

Es **propio de cada objeto**. Se define con `self.xxx = ...` (normalmente dentro de `__init__`).

```python
class Persona:
    def __init__(self, nombre):
        self.nombre = nombre   # ATRIBUTO DE INSTANCIA: cada persona tiene el suyo
```

#### Atributo de clase

Es **compartido por TODAS las instancias**. Se define **directamente dentro de la clase**, fuera de cualquier metodo, sin `self`.

```python
class Persona:
    especie = 'Homo sapiens'    # ATRIBUTO DE CLASE: compartido por todos

    def __init__(self, nombre):
        self.nombre = nombre
```

#### Como acceder a cada uno?

```python
p = Persona('Ana')

p.nombre           # 'Ana'              -> atributo de instancia
p.especie          # 'Homo sapiens'     -> Python busca en la clase
Persona.especie    # 'Homo sapiens'     -> tambien funciona desde la clase
```

#### Tabla comparativa

| Atributo de instancia | Atributo de clase |
|---|---|
| `self.x = ...` (en `__init__` o metodos) | `x = ...` (directamente en `class`) |
| Una copia por objeto | Una sola copia compartida |
| Cambia en uno NO afecta al resto | Cambiarlo via `Clase.x = ...` afecta a TODOS |
| Sirve para: datos personales (nombre, edad) | Sirve para: constantes, contadores globales |
| Acceso: `obj.x` | Acceso: `obj.x` o `Clase.x` |

#### TRAMPA: el "shadowing"

Si haces `obj.especie = 'X'` (asignacion sobre la instancia), **NO modificas el atributo de clase**. Creas uno **nuevo** de instancia que la **oculta**:

```python
p1 = Persona('Ana')
p2 = Persona('Pepe')

Persona.especie = 'Mutante'   # CAMBIA para todos
print(p1.especie)             # 'Mutante'
print(p2.especie)             # 'Mutante'

p1.especie = 'Particular'     # SOLO p1 tiene su atributo de instancia
print(p1.especie)             # 'Particular' (instancia)
print(p2.especie)             # 'Mutante'    (sigue siendo el de clase)
```

#### TRAMPA: atributos de clase MUTABLES

Si el atributo de clase es una lista o diccionario, ten cuidado:

```python
class Equipo:
    miembros = []                      # MAL: compartido!
    def agregar(self, nombre):
        self.miembros.append(nombre)   # modifica la lista de la CLASE

a = Equipo()
b = Equipo()
a.agregar('Ana')
print(b.miembros)   # ['Ana']  <- b tambien lo ve!
```

Lo correcto es inicializar la lista en `__init__`:

```python
class Equipo:
    def __init__(self):
        self.miembros = []   # cada instancia su propia lista
```"""
    )},
    {"type": "md", "src": tu_turno(2,
        """Crea una clase `CuentaBancaria` con:

- Atributo de **clase**: `banco = 'BancoVIU'` (igual para todas las cuentas).
- En el `__init__`: recibe `titular` y `saldo_inicial`, los guarda como atributos de **instancia**.
- Metodo `mostrar()`: imprime `'<titular> - banco: <banco>, saldo: <saldo>'`.

Crea dos cuentas distintas y llama a `mostrar()` en cada una. Luego cambia `CuentaBancaria.banco` a `'NuevoBanco'` y vuelve a imprimir: ambas cuentas deben mostrar el nuevo banco."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# class CuentaBancaria:\n#     banco = 'BancoVIU'   # ATRIBUTO DE CLASE: compartido\n#\n#     def __init__(self, titular, saldo_inicial):\n#         # ATRIBUTOS DE INSTANCIA: propios de cada cuenta\n#         self.titular = titular\n#         self.saldo = saldo_inicial\n#\n#     def mostrar(self):\n#         # self.banco busca primero en la instancia, luego en la clase\n#         print(f'{self.titular} - banco: {self.banco}, saldo: {self.saldo}')\n#\n# c1 = CuentaBancaria('Ana', 1000)\n# c2 = CuentaBancaria('Pepe', 2500)\n# c1.mostrar()\n# c2.mostrar()\n#\n# # Cambiar el atributo de clase afecta a TODAS las instancias:\n# CuentaBancaria.banco = 'NuevoBanco'\n# c1.mostrar()\n# c2.mostrar()\n"},
]))

# ============================ HERENCIA ============================
plan.append((ID_HERENCIA, [
    {"type": "md", "src": teoria(
        "Herencia: heredar el plano para extenderlo",
        """La **herencia** permite crear una clase nueva (clase **hija** o subclase) que **reutiliza** lo que ya tiene otra clase (clase **padre** o superclase) y le **anade** cosas o le **modifica** algunas.

#### Analogia

- La clase `Vehiculo` tiene atributos comunes (`marca`, `velocidad`) y metodos basicos (`acelerar`, `frenar`).
- La clase `Coche(Vehiculo)` **hereda** todo eso, y **anade** lo suyo (`numero_puertas`, `abrir_maletero`).
- La clase `Moto(Vehiculo)` **hereda** lo mismo, y anade otra cosa (`hacer_caballito`).

```
            Vehiculo
           /    |    \\
       Coche  Moto  Camion
```

Todo lo que vale para `Vehiculo` vale para `Coche`, `Moto` y `Camion`. Pero al reves no.

#### Sintaxis

```python
class Padre:
    def __init__(self, x):
        self.x = x
    def saludar(self):
        print('Hola desde Padre')

class Hija(Padre):                 # entre parentesis: la(s) clase(s) padre
    def __init__(self, x, y):
        super().__init__(x)         # llama al __init__ del padre
        self.y = y                  # ademas, atributo propio
    def saludar(self):              # SOBREESCRIBIMOS el metodo
        super().saludar()           # primero llamamos al del padre
        print('Y tambien desde Hija')
```

#### Que es <code>super()</code>?

`super()` es una **referencia a la clase padre** desde dentro de la clase hija. Sirve para:

1. **Llamar al `__init__` del padre** sin tener que repetir `self.x = x`.
2. **Extender** un metodo (hacer lo mismo que el padre Y algo mas).

```python
class Hija(Padre):
    def __init__(self, x, y):
        super().__init__(x)   # <-- equivale a: Padre.__init__(self, x)
        self.y = y
```

#### Reemplazar vs extender

| Que hago en la subclase | Resultado |
|---|---|
| Defino un metodo con el MISMO nombre que el padre | **Reemplazo** total |
| Lo defino y dentro llamo a `super().metodo()` | **Extiendo** (anado al original) |
| No lo redefino | **Hereda** tal cual |

#### Trampa con MRO (Method Resolution Order)

Cuando hay **herencia multiple** (una clase hereda de varias), `super()` sigue un orden llamado **MRO**. Lo puedes ver con `Clase.__mro__` o `Clase.mro()`:

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
print(D.__mro__)
# (D, B, C, A, object)
```

Para casos simples (una sola clase padre), no te preocupes. Para casos complejos, **cada clase debe llamar a `super().__init__()`** para que la cadena funcione."""
    )},
]))

plan.append((ID_HERENCIA_CODE, [
    {"type": "md", "src": tu_turno(3,
        """Crea una jerarquia de clases:

1. Clase `Animal` con `__init__(self, nombre)` que guarda `self.nombre`. Metodo `presentar()` que imprime `'Soy <nombre> y soy un animal'`.
2. Clase `Perro(Animal)` que **extiende** `presentar()`: primero llama al de `Animal` con `super()`, y despues imprime `'Y ladro: guau guau'`.
3. Clase `Gato(Animal)` que **reemplaza** `presentar()`: solo imprime `'Soy <nombre> y maullo: miau'`.

Crea un `perro = Perro('Rex')` y un `gato = Gato('Mish')`. Llama a `presentar()` en ambos.

> Resultado esperado:
>
> ```
> Soy Rex y soy un animal
> Y ladro: guau guau
> Soy Mish y maullo: miau
> ```"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# class Animal:\n#     def __init__(self, nombre):\n#         self.nombre = nombre\n#\n#     def presentar(self):\n#         print(f'Soy {self.nombre} y soy un animal')\n#\n# class Perro(Animal):\n#     # No redefinimos __init__: hereda el del padre\n#     def presentar(self):\n#         super().presentar()                # extension: llamamos al original\n#         print('Y ladro: guau guau')        # y anadimos lo nuestro\n#\n# class Gato(Animal):\n#     def presentar(self):\n#         # reemplazo total: NO llamamos a super().presentar()\n#         print(f'Soy {self.nombre} y maullo: miau')\n#\n# perro = Perro('Rex')\n# gato  = Gato('Mish')\n# perro.presentar()\n# gato.presentar()\n"},
]))

# ============================ VISIBILIDAD / ENCAPSULACION ============================
plan.append((ID_VISIBILIDAD, [
    {"type": "md", "src": teoria(
        "Encapsulacion: publico, protegido y privado",
        """**Encapsular** significa **esconder** los detalles internos de una clase para que el usuario solo interactue con lo que tu has decidido exponer. Es uno de los pilares de OOP.

#### Como lo hace Python?

Python **no tiene** `public`, `protected` ni `private` como palabras reservadas (a diferencia de Java o C++). En su lugar, usa **convenciones de nombre**:

| Prefijo | Visibilidad | Significado |
|---|---|---|
| ninguno | **publico** | Cualquiera lo puede usar. Forma parte del 'contrato' de la clase. |
| `_` (un guion bajo) | **protegido** | "Uso interno". No es obligatorio respetarlo, pero es de mala educacion tocarlo desde fuera. |
| `__` (dos guiones bajos al inicio, sin guiones al final) | **privado** | Python le aplica *name mangling* (lo renombra a `_NombreClase__atributo`). Realmente NO es privado, pero es mas dificil de tocar accidentalmente. |
| `__xxx__` (dunder) | **especial** | Reservado para Python (`__init__`, `__str__`, ...). NO inventes los tuyos. |

#### Ejemplo

```python
class CuentaBancaria:
    def __init__(self, saldo):
        self.titular = 'Ana'        # publico
        self._tipo = 'corriente'     # protegido (uso interno)
        self.__saldo = saldo         # privado (no toques desde fuera)

c = CuentaBancaria(1000)
print(c.titular)        # 'Ana'        OK
print(c._tipo)          # 'corriente'  funciona, pero NO deberias
print(c.__saldo)        # AttributeError!
print(c._CuentaBancaria__saldo)   # 1000 (name mangling)
```

#### "We are all consenting adults"

Es la **filosofia oficial de Python**: confiamos en que el programador es responsable. No bloqueamos el acceso, solo lo marcamos. Si alguien decide tocar `_tipo` o `__saldo`, tendra sus motivos (pruebas, debugging) y asumira las consecuencias.

#### Cuando usar cada uno?

| Caso | Que prefijo |
|---|---|
| Nombre de la persona, edad, color, todo lo que el usuario debe ver y poder cambiar | nada (publico) |
| Variable que usas dentro de la clase para calcular algo, no es parte del API | `_` |
| Variable que NO quieres que se sobreescriba accidentalmente al heredar | `__` |
| Metodo de Python (operadores especiales) | `__xxx__` |"""
    )},
]))

# ============================ STATIC y CLASS METHODS ============================
plan.append((ID_DECORADORES, [
    {"type": "md", "src": teoria(
        "<code>@staticmethod</code> vs <code>@classmethod</code> vs metodo de instancia",
        """En una clase puedes definir **tres tipos** de funciones segun el primer parametro que reciben:

| Tipo | Decorador | Primer parametro | Para que sirve |
|---|---|---|---|
| Metodo de instancia | (ninguno) | `self` (la instancia) | Operar sobre los datos de UN objeto |
| Metodo de clase | `@classmethod` | `cls` (la clase) | Operar sobre la clase, contar instancias, factories |
| Metodo estatico | `@staticmethod` | (ninguno) | Funcion auxiliar que solo agrupamos en la clase por organizacion |

#### Ejemplo de los tres

```python
class Pizza:
    contador = 0     # atributo de clase

    def __init__(self, ingredientes):
        self.ingredientes = ingredientes
        Pizza.contador += 1

    # METODO DE INSTANCIA: usa self
    def describir(self):
        return f'Pizza con: {", ".join(self.ingredientes)}'

    # METODO DE CLASE: recibe cls. Util para FACTORY METHODS
    @classmethod
    def margarita(cls):
        return cls(['mozzarella', 'tomate', 'albahaca'])
        # equivale a Pizza(['mozzarella', 'tomate', 'albahaca'])

    @classmethod
    def total_pizzas(cls):
        return cls.contador

    # METODO ESTATICO: ni self ni cls. Funcion 'normal' agrupada
    @staticmethod
    def es_ingrediente_valido(ing):
        return isinstance(ing, str) and len(ing) > 0
```

Uso:

```python
p = Pizza.margarita()                   # llamada de classmethod desde la clase
print(p.describir())                    # metodo de instancia
print(Pizza.total_pizzas())             # 1
print(Pizza.es_ingrediente_valido('queso'))  # True (no necesita instancia)
```

#### <code>@classmethod</code> como FACTORY (patron muy comun)

Imagina que un objeto se puede crear de varias formas. En vez de tener un `__init__` con muchos `if`, ofreces varios constructores alternativos:

```python
class Fecha:
    def __init__(self, dia, mes, anio):
        self.dia, self.mes, self.anio = dia, mes, anio

    @classmethod
    def desde_string(cls, s):           # 'dd-mm-aaaa'
        d, m, a = s.split('-')
        return cls(int(d), int(m), int(a))

    @classmethod
    def hoy(cls):
        from datetime import date
        h = date.today()
        return cls(h.day, h.month, h.year)

f1 = Fecha(1, 1, 2024)
f2 = Fecha.desde_string('15-08-2024')
f3 = Fecha.hoy()
```

#### Resumen visual

```
metodo(self, ...)     -> necesita una INSTANCIA
@classmethod cls,...  -> trabaja con la CLASE
@staticmethod         -> no necesita ni una ni otra
```"""
    )},
    {"type": "md", "src": tu_turno(4,
        """Crea una clase `Temperatura` con:

- `__init__(self, celsius)`: guarda `self.celsius`.
- Metodo de instancia `a_fahrenheit(self)`: devuelve `self.celsius * 9/5 + 32`.
- Metodo de clase `desde_fahrenheit(cls, f)`: crea una `Temperatura` a partir de grados Fahrenheit (formula inversa: `(f - 32) * 5/9`).
- Metodo estatico `es_temperatura_humana(c)`: devuelve `True` si `c` esta entre `-50` y `60`, `False` si no.

Pruebalo:

```python
t1 = Temperatura(25)
print(t1.a_fahrenheit())              # 77.0
t2 = Temperatura.desde_fahrenheit(100)
print(t2.celsius)                      # 37.77...
print(Temperatura.es_temperatura_humana(150))   # False
```"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# class Temperatura:\n#     def __init__(self, celsius):\n#         self.celsius = celsius\n#\n#     # Metodo de instancia: usa self.celsius\n#     def a_fahrenheit(self):\n#         return self.celsius * 9 / 5 + 32\n#\n#     # Factory method: crea una instancia desde Fahrenheit\n#     @classmethod\n#     def desde_fahrenheit(cls, f):\n#         celsius = (f - 32) * 5 / 9\n#         return cls(celsius)   # equivale a Temperatura(celsius)\n#\n#     # Funcion auxiliar agrupada en la clase, no necesita ni self ni cls\n#     @staticmethod\n#     def es_temperatura_humana(c):\n#         return -50 <= c <= 60\n#\n# t1 = Temperatura(25)\n# print(t1.a_fahrenheit())\n# t2 = Temperatura.desde_fahrenheit(100)\n# print(t2.celsius)\n# print(Temperatura.es_temperatura_humana(150))\n# print(Temperatura.es_temperatura_humana(20))\n"},
]))

# ============================ @property ============================
plan.append((ID_PROPERTY_GETTER, [
    {"type": "md", "src": teoria(
        "<code>@property</code>: atributos calculados / con validacion",
        """`@property` permite que un **metodo** se vea **como un atributo**. Es decir, se accede sin parentesis. Es la forma 'pythonica' de implementar **getters y setters**.

#### Por que existe?

En lenguajes como Java es comun escribir:

```java
empleado.getNombre();
empleado.setNombre("Ana");
```

En Python esto se considera feo. La filosofia es: **empieza con atributos publicos**, y solo si necesitas validar o calcular algo, **conviertelos en `@property` mas tarde** sin romper a nadie.

#### Ejemplo: atributo calculado

```python
class Circulo:
    def __init__(self, radio):
        self.radio = radio

    @property
    def area(self):
        return 3.14159 * self.radio ** 2

c = Circulo(10)
print(c.area)     # 314.159   <- sin parentesis, parece un atributo
```

#### Ejemplo: validacion con setter

```python
class Persona:
    def __init__(self, edad):
        self.edad = edad     # internamente llama al setter

    @property
    def edad(self):           # GETTER
        return self._edad

    @edad.setter
    def edad(self, valor):    # SETTER (mismo nombre del property)
        if valor < 0:
            raise ValueError('La edad no puede ser negativa')
        self._edad = valor

p = Persona(30)
print(p.edad)     # 30
p.edad = 31       # OK
p.edad = -5       # ValueError!
```

#### Trampa: dentro del setter NO uses `self.edad = valor` directamente

Eso provocaria una **recursion infinita** (el setter se llama a si mismo). Por eso usamos un nombre interno como `self._edad`.

#### Resumen

| Quiero... | Uso... |
|---|---|
| Atributo calculado a partir de otros | `@property` |
| Atributo con validacion al asignar | `@property` + `@xxx.setter` |
| Atributo de solo lectura | solo `@property` (sin setter) |
| Borrar el atributo con `del` | `@xxx.deleter` |"""
    )},
]))

plan.append((ID_PROPERTY_DEL, [
    {"type": "md", "src": tu_turno(5,
        """Crea una clase `Cuadrado` con:

- `__init__(self, lado)`: guarda `self._lado` (con guion bajo, como atributo 'protegido').
- Una `@property` llamada `lado` que devuelva `self._lado`.
- Un `@lado.setter` que **valide** que el lado es positivo. Si no, lanza `ValueError('El lado debe ser positivo')`.
- Una `@property` llamada `area` que devuelva `self._lado ** 2` (de SOLO LECTURA, sin setter).

Pruebalo:

```python
c = Cuadrado(5)
print(c.lado, c.area)    # 5 25
c.lado = 10
print(c.lado, c.area)    # 10 100
c.lado = -3              # debe lanzar ValueError
```"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# class Cuadrado:\n#     def __init__(self, lado):\n#         # asignamos via la property para activar la validacion\n#         self.lado = lado\n#\n#     @property\n#     def lado(self):\n#         return self._lado\n#\n#     @lado.setter\n#     def lado(self, valor):\n#         if valor <= 0:\n#             raise ValueError('El lado debe ser positivo')\n#         self._lado = valor   # OJO: usar _lado, NO self.lado (recursion!)\n#\n#     @property\n#     def area(self):\n#         # area solo se calcula al leerla, siempre coherente con _lado\n#         return self._lado ** 2\n#\n# c = Cuadrado(5)\n# print(c.lado, c.area)   # 5 25\n# c.lado = 10\n# print(c.lado, c.area)   # 10 100\n# # c.lado = -3           # descomenta y veras el ValueError\n"},
]))

# ============================ OPERADORES (METODOS ESPECIALES) ============================
plan.append((ID_OP_OVERLOAD, [
    {"type": "md", "src": teoria(
        "Metodos especiales (dunder methods)",
        """Los **metodos especiales** o *dunder methods* (porque tienen **d**ouble **under**score: `__xxx__`) permiten que tus objetos se comporten como los tipos nativos de Python: que se sumen, se comparen, se conviertan a string, se midan con `len()`, se iteren, etc.

#### Tabla de los mas usados

| Operador / funcion | Metodo dunder | Que hace |
|---|---|---|
| `print(obj)`, `str(obj)` | `__str__` | Representacion 'amigable' para humanos |
| `repr(obj)`, eco en consola | `__repr__` | Representacion 'tecnica' para depurar |
| `obj1 == obj2` | `__eq__` | Igualdad |
| `obj1 != obj2` | `__ne__` | Desigualdad (defecto: lo contrario de `__eq__`) |
| `obj1 < obj2` | `__lt__` | Menor que |
| `obj1 + obj2` | `__add__` | Suma |
| `obj1 - obj2` | `__sub__` | Resta |
| `obj1 * obj2` | `__mul__` | Multiplicacion |
| `len(obj)` | `__len__` | Longitud |
| `obj[i]` | `__getitem__` | Indexacion |
| `obj[i] = x` | `__setitem__` | Asignacion por indice |
| `x in obj` | `__contains__` | Pertenencia |
| `for x in obj:` | `__iter__` | Iteracion |
| `bool(obj)`, `if obj:` | `__bool__` | Veracidad |
| `hash(obj)` | `__hash__` | Para usar como clave de dict / elemento de set |
| `obj()` | `__call__` | Hace al objeto invocable como una funcion |

#### Ejemplo completo

```python
class Vector2D:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f'Vector2D({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, otro):
        return self.x == otro.x and self.y == otro.y

    def __add__(self, otro):
        return Vector2D(self.x + otro.x, self.y + otro.y)

    def __len__(self):
        # truncamos a entero porque __len__ DEBE devolver int
        return int((self.x ** 2 + self.y ** 2) ** 0.5)

v1 = Vector2D(3, 4)
v2 = Vector2D(1, 2)

print(v1)           # (3, 4)        <- usa __str__
print(repr(v1))     # Vector2D(3, 4)<- usa __repr__
print(v1 + v2)      # (4, 6)        <- usa __add__
print(v1 == Vector2D(3, 4))   # True
print(len(v1))      # 5             <- usa __len__
```

#### Diferencia entre <code>__str__</code> y <code>__repr__</code>

| `__str__` | `__repr__` |
|---|---|
| Para humanos finales | Para programadores / debugging |
| `print(obj)`, `str(obj)` | `repr(obj)`, mostrar en REPL, `repr` en logs |
| Bonito, legible | Idealmente, codigo Python valido que recrearia el objeto |

Si solo defines uno, **define `__repr__`**: Python usara `__repr__` como fallback de `__str__`."""
    )},
]))

plan.append((ID_OP_OTHERS_CODE, [
    {"type": "md", "src": tu_turno(6,
        """Crea una clase `Fraccion` que represente una fraccion `a/b`. Implementa:

- `__init__(self, num, den)`: guarda `num` y `den`.
- `__str__(self)`: devuelve `'<num>/<den>'`.
- `__repr__(self)`: devuelve `'Fraccion(<num>, <den>)'`.
- `__add__(self, otro)`: suma dos fracciones. Recuerda: `a/b + c/d = (a*d + c*b) / (b*d)`.
- `__eq__(self, otro)`: dos fracciones son iguales si `a/b == c/d`, es decir si `a*d == c*b`.

Pruebalo:

```python
f1 = Fraccion(1, 2)
f2 = Fraccion(1, 3)
print(f1)             # 1/2
print(repr(f1))       # Fraccion(1, 2)
print(f1 + f2)        # 5/6
print(Fraccion(2, 4) == Fraccion(1, 2))   # True
```"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# class Fraccion:\n#     def __init__(self, num, den):\n#         if den == 0:\n#             raise ValueError('El denominador no puede ser cero')\n#         self.num = num\n#         self.den = den\n#\n#     def __str__(self):\n#         # representacion amigable, la que ve el usuario final\n#         return f'{self.num}/{self.den}'\n#\n#     def __repr__(self):\n#         # representacion tecnica: idealmente codigo Python valido\n#         return f'Fraccion({self.num}, {self.den})'\n#\n#     def __add__(self, otro):\n#         # a/b + c/d = (a*d + c*b) / (b*d)\n#         nuevo_num = self.num * otro.den + otro.num * self.den\n#         nuevo_den = self.den * otro.den\n#         return Fraccion(nuevo_num, nuevo_den)\n#\n#     def __eq__(self, otro):\n#         # a/b == c/d  <=>  a*d == c*b\n#         return self.num * otro.den == otro.num * self.den\n#\n# f1 = Fraccion(1, 2)\n# f2 = Fraccion(1, 3)\n# print(f1)\n# print(repr(f1))\n# print(f1 + f2)\n# print(Fraccion(2, 4) == Fraccion(1, 2))\n"},
]))

# ============================ POLIMORFISMO ============================
plan.append((ID_POLIMORFISMO, [
    {"type": "md", "src": teoria(
        "Polimorfismo: muchas formas, una sola interfaz",
        """**Polimorfismo** significa literalmente 'muchas formas'. En OOP, es la capacidad de **tratar objetos de clases distintas como si fueran del mismo tipo**, siempre que respondan a los mismos mensajes (metodos).

#### Analogia

Imagina un mando a distancia con un boton 'play'. Lo apuntas a:

- Una TV: empieza la pelicula.
- Un equipo de musica: empieza la cancion.
- Un libro electronico: lee en voz alta.

Cada aparato hace algo distinto, pero **todos entienden el mismo mensaje** (`play`). Tu, como usuario del mando, no necesitas saber que aparato hay del otro lado. **Eso es polimorfismo.**

#### En Python: 'duck typing'

> "Si camina como un pato y suena como un pato, es un pato."

Python no comprueba el tipo de un objeto antes de llamar a un metodo. Solo intenta llamarlo. Si funciona, bien. Si no, error.

```python
class Perro:
    def hablar(self):
        return 'Guau'

class Gato:
    def hablar(self):
        return 'Miau'

class Vaca:
    def hablar(self):
        return 'Muu'

def coro(animales):
    # No necesito saber si son perros, gatos o vacas.
    # Solo necesito que sepan hablar().
    for a in animales:
        print(a.hablar())

coro([Perro(), Gato(), Vaca()])   # Guau, Miau, Muu
```

#### Polimorfismo via herencia

Es la forma 'clasica'. Una clase abstracta define la interfaz, y las hijas la implementan:

```python
from abc import ABC, abstractmethod

class Figura(ABC):
    @abstractmethod
    def area(self):
        ...

class Cuadrado(Figura):
    def __init__(self, lado): self.lado = lado
    def area(self): return self.lado ** 2

class Circulo(Figura):
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r ** 2

for f in [Cuadrado(5), Circulo(3)]:
    print(f.area())   # cada una calcula a su manera
```

#### Tabla: tipos de polimorfismo en Python

| Tipo | Como se logra | Ejemplo |
|---|---|---|
| **De subtipo** | Herencia + sobrescritura de metodos | `Cuadrado` y `Circulo` ambos con `area()` |
| **Duck typing** | Misma interfaz, sin necesidad de heredar | Cualquier objeto con `.read()` puede usarse como un fichero |
| **Sobrecarga de operadores** | `__add__`, `__lt__`, etc. | `Fraccion(1,2) + Fraccion(1,3)` |"""
    )},
    {"type": "md", "src": tu_turno(7,
        """Crea tres clases que representen formas de pago: `Tarjeta`, `Efectivo`, `Bizum`. Cada una debe tener un metodo `pagar(self, cantidad)` que devuelva un string distinto:

- `Tarjeta`: `'Pagados <cantidad> EUR con tarjeta. Comision 1%.'`
- `Efectivo`: `'Pagados <cantidad> EUR en efectivo. Sin comision.'`
- `Bizum`: `'Pagados <cantidad> EUR con Bizum. Pago instantaneo.'`

Crea una funcion `procesar_pagos(metodos, cantidad)` que reciba una lista de objetos de pago y la cantidad, y para cada uno llame a `pagar(cantidad)` e imprima el resultado.

> Eso es polimorfismo: la funcion no sabe ni le importa que tipo es cada uno; solo sabe que todos tienen `.pagar(...)`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# class Tarjeta:\n#     def pagar(self, cantidad):\n#         return f'Pagados {cantidad} EUR con tarjeta. Comision 1%.'\n#\n# class Efectivo:\n#     def pagar(self, cantidad):\n#         return f'Pagados {cantidad} EUR en efectivo. Sin comision.'\n#\n# class Bizum:\n#     def pagar(self, cantidad):\n#         return f'Pagados {cantidad} EUR con Bizum. Pago instantaneo.'\n#\n# def procesar_pagos(metodos, cantidad):\n#     # Polimorfismo via duck typing: solo necesito que tengan .pagar(...)\n#     for m in metodos:\n#         print(m.pagar(cantidad))\n#\n# procesar_pagos([Tarjeta(), Efectivo(), Bizum()], 50)\n"},
]))

# ============================ FINAL: RESUMEN ============================
plan.append((ID_EJERCICIOS, [
    {"type": "md", "src": teoria(
        "Resumen y chuleta de OOP",
        """Antes de los ejercicios finales, una chuleta para recordarlo todo:

#### Anatomia de una clase 'completa'

```python
class MiClase(ClasePadre):
    # Atributo de clase (compartido)
    contador = 0

    # Constructor
    def __init__(self, x, y):
        super().__init__()      # opcional, llama al padre
        self.x = x               # atributo de instancia publico
        self._y = y              # atributo 'protegido' por convencion
        self.__id = id(self)     # privado (name mangling)
        MiClase.contador += 1

    # Metodo de instancia
    def metodo(self):
        return self.x + self._y

    # Metodo de clase (factory, contador, etc.)
    @classmethod
    def crear_cero(cls):
        return cls(0, 0)

    # Metodo estatico (utilidad)
    @staticmethod
    def es_par(n):
        return n % 2 == 0

    # Property (getter)
    @property
    def doble_x(self):
        return self.x * 2

    # Dunder methods
    def __str__(self):
        return f'MiClase({self.x}, {self._y})'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, otro):
        return self.x == otro.x and self._y == otro._y

    def __add__(self, otro):
        return MiClase(self.x + otro.x, self._y + otro._y)

    def __len__(self):
        return abs(self.x) + abs(self._y)
```

#### Los 4 pilares de OOP

| Pilar | En una frase | En Python |
|---|---|---|
| **Encapsulacion** | Esconder los detalles internos | `_xxx`, `__xxx`, `@property` |
| **Herencia** | Reusar lo que ya existe | `class Hija(Padre):` + `super()` |
| **Polimorfismo** | Misma interfaz, distinta implementacion | duck typing + sobreescritura |
| **Abstraccion** | Definir QUE se hace, no COMO | clases abstractas (`abc.ABC`, `@abstractmethod`) |

#### Cuando NO usar OOP

- Para scripts cortos (un sumador rapido, un pequeno calculo).
- Cuando una funcion suelta basta.
- Cuando solo necesitas agrupar datos: usa `dataclass` o `namedtuple`.
- Cuando creas clases que solo tienen un metodo: probablemente quieres una funcion.

> **Idea final**: OOP es una herramienta, no una religion. En Python, la simplicidad gana. Empieza con funciones; pasa a clases solo cuando los datos y el comportamiento empiezan a ir juntos."""
    )},
]))


enhance(NB, plan)
print("Done.")

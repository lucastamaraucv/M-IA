"""Aplica mejoras al notebook 07_Advanced con bloques de colores y teoria detallada."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, dato, aviso
import json

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_07_Python101_Advanced.ipynb"

nb = json.load(open(NB, encoding="utf-8"))

def find_id(fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if fragment in src:
            return c["id"]
    return None

# --- Anchors elegidos (9) ---
ID_TITULO   = nb["cells"][0]["id"]                              # portada
ID_ARRAY    = find_id("## Array")                                # Array
ID_LINKED   = find_id("## Lista enlazada")                       # Linked list
ID_STACK    = find_id("## Pila (Stack)")                         # Stack
ID_QUEUE    = find_id("## Cola (Queue)")                         # Queue
ID_HEAP     = find_id("## Cola de prioridad")                    # Heap
ID_HASH     = find_id("## Tabla Hash")                           # Hash
ID_GRAPH    = find_id("## Grafo")                                # Graph
ID_CRAFT    = find_id("# Software Craftsmanship")                # Clean code
ID_TESTING  = find_id("# Software Testing")                      # Testing


plan = []

# ============ INTRO ============
plan.append((ID_TITULO, [
    {"type": "md", "src": teoria(
        "Como leer este notebook (version mejorada)",
        """Este notebook fue **enriquecido** con bloques de teoria detallada y ejercicios para que practiques **estructuras de datos avanzadas, buenas practicas y testing**.

<div style="background-color:#e7f5ff;border-left:6px solid #1c7ed6;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AZUL = TEORIA</b></div> -> explicacion en palabras simples antes de cada concepto.

<div style="background-color:#fff9db;border-left:6px solid #f59f00;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AMARILLO = TU TURNO</b></div> -> ejercicio para resolver. Tienes una celda vacia donde escribir tu codigo.

<div style="background-color:#ebfbee;border-left:6px solid #2f9e44;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>VERDE = SOLUCION</b></div> -> codigo de referencia comentado. Destapalo SOLO despues de intentar.

> **Promesa:** el codigo y la teoria del profesor original NO se han tocado. Solo se han ANADIDO bloques nuevos."""
    )},
    {"type": "md", "src": dato(
        """**Temas principales de esta clase:**

- **Estructuras de datos avanzadas**: arrays, listas enlazadas, pilas, colas, colas de prioridad, tablas hash y grafos.
- **Software Craftsmanship**: como escribir codigo limpio, legible y mantenible (nombres, funciones, comentarios, etc.).
- **Software Testing**: pruebas automaticas con `pytest`, TDD y pirámide de tests.

**Por que importan las estructuras de datos?** Cada estructura tiene un **coste** distinto para insertar, buscar o eliminar elementos. Elegir bien acelera tu programa de segundos a milisegundos.

**Por que importa el codigo limpio?** Pasamos mucho mas tiempo **leyendo** codigo que escribiendolo. Codigo limpio = menos bugs y mantenimiento mas barato.

**Por que importan los tests?** Te dan confianza para refactorizar y detectar regresiones. En cualquier proyecto serio son tan importantes como el codigo de produccion."""
    )},
]))

# ============ ARRAY ============
plan.append((ID_ARRAY, [
    {"type": "md", "src": teoria(
        "Array: la estructura de datos mas basica",
        """Un **array** es una **secuencia de elementos del mismo tipo guardados en memoria contigua**. Es la estructura mas eficiente para acceso por indice.

#### Caracteristicas

| Operacion | Coste | Por que |
|---|---|---|
| Acceso por indice `a[i]` | **O(1)** | Calcula la direccion: `base + i * tam` |
| Buscar valor | O(n) | Hay que recorrer |
| Insertar al final | O(1) amortizado (en `list`) | Si hay capacidad |
| Insertar en medio | O(n) | Hay que desplazar elementos |
| Borrar | O(n) | Igual: desplazamiento |

#### En Python

Python NO tiene arrays clasicos por defecto: tiene **`list`**, que es un array dinamico (se redimensiona solo). Para arrays homogeneos eficientes existe el modulo `array` o, mejor, **`numpy.ndarray`**.

```python
# list (dinamica, tipos mixtos)
nums = [1, 2, 3]
nums.append(4)        # O(1) amortizado
nums[0]               # O(1) acceso

# array (homogeneo, mas compacto)
import array
a = array.array('i', [1, 2, 3])   # 'i' = int de 4 bytes

# numpy (la herramienta de IA)
import numpy as np
v = np.array([1, 2, 3])
```

#### Cuando usarlo?

- Cuando necesitas acceso aleatorio rapido por indice.
- Cuando el tamano es relativamente estable o crece al final.
- **NO** cuando insertas/borras mucho en el medio (mejor lista enlazada o deque)."""
    )},
    {"type": "md", "src": tu_turno(1,
        """Crea una lista de 10 numeros del 1 al 10. Calcula:

1. El **acceso por indice** del elemento en la posicion 5.
2. La **suma** de todos los elementos usando `sum()`.
3. El **maximo** y el **minimo**.
4. Una nueva lista con cada elemento **al cuadrado** (usa list comprehension).
5. Inserta el numero `99` en la posicion 0 con `.insert(0, 99)` y observa que ahora el resto se desplaza."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# nums = list(range(1, 11))\n# print('Lista:', nums)\n#\n# # 1) Acceso por indice O(1)\n# print('Elemento en pos 5:', nums[5])\n#\n# # 2) Suma\n# print('Suma:', sum(nums))\n#\n# # 3) Max y min\n# print('Max:', max(nums), 'Min:', min(nums))\n#\n# # 4) Cuadrados con list comprehension\n# cuadrados = [n ** 2 for n in nums]\n# print('Cuadrados:', cuadrados)\n#\n# # 5) Insercion en posicion 0 (operacion O(n) porque desplaza)\n# nums.insert(0, 99)\n# print('Tras insertar 99 en pos 0:', nums)\n"},
]))

# ============ LISTA ENLAZADA ============
plan.append((ID_LINKED, [
    {"type": "md", "src": teoria(
        "Lista enlazada: nodos conectados por punteros",
        """Una **lista enlazada** es una secuencia de **nodos** donde cada nodo guarda:

- Un **valor**.
- Una **referencia** (puntero) al siguiente nodo.

```
[1|*]-->[2|*]-->[3|*]-->[4|None]
```

#### Comparacion con array

| Operacion | Array | Lista enlazada |
|---|---|---|
| Acceso por indice | **O(1)** | O(n) (hay que recorrer) |
| Insertar al inicio | O(n) | **O(1)** |
| Insertar al final | O(1) amortizado | O(n) (o O(1) si tienes puntero al final) |
| Insertar en medio (con referencia al nodo) | O(n) | **O(1)** |
| Memoria | Compacta | Dispersa (mas overhead por puntero) |
| Cache CPU | Buen aprovechamiento | Malo (saltos en memoria) |

#### Variantes

- **Simple**: cada nodo apunta solo al siguiente.
- **Doble**: cada nodo apunta al siguiente Y al anterior. Permite recorrer en ambas direcciones.
- **Circular**: el ultimo nodo apunta al primero.

#### En Python

Python NO tiene lista enlazada en la libreria estandar (la `list` es array dinamico). Si necesitas comportamiento similar, usa **`collections.deque`** que esta implementada como lista doblemente enlazada y ofrece `append`, `appendleft`, `pop`, `popleft` en O(1)."""
    )},
    {"type": "md", "src": tu_turno(2,
        """Implementa una **lista enlazada simple** muy basica con dos clases:

1. Clase `Nodo` con atributos `valor` y `siguiente` (inicialmente `None`).
2. Clase `ListaEnlazada` con un atributo `cabeza` (inicialmente `None`) y un metodo `agregar_inicio(valor)` que crea un nuevo nodo apuntando a la cabeza actual y lo convierte en la nueva cabeza.

Despues:
- Crea una lista enlazada vacia.
- Agrega los valores 1, 2, 3 al inicio (terminaras con la cabeza apuntando a 3).
- Recorre la lista imprimiendo cada valor."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# class Nodo:\n#     def __init__(self, valor):\n#         self.valor = valor\n#         self.siguiente = None\n#\n# class ListaEnlazada:\n#     def __init__(self):\n#         self.cabeza = None\n#\n#     def agregar_inicio(self, valor):\n#         # Crear nodo nuevo apuntando a la cabeza actual\n#         nuevo = Nodo(valor)\n#         nuevo.siguiente = self.cabeza\n#         # El nuevo pasa a ser la cabeza\n#         self.cabeza = nuevo\n#\n# lista = ListaEnlazada()\n# lista.agregar_inicio(1)\n# lista.agregar_inicio(2)\n# lista.agregar_inicio(3)   # cabeza -> 3 -> 2 -> 1 -> None\n#\n# # Recorrido\n# actual = lista.cabeza\n# while actual is not None:\n#     print(actual.valor)\n#     actual = actual.siguiente\n"},
]))

# ============ STACK ============
plan.append((ID_STACK, [
    {"type": "md", "src": teoria(
        "Pila (Stack): el ultimo en entrar es el primero en salir (LIFO)",
        """Una **pila** sigue el principio **LIFO** (*Last In, First Out*): el ultimo elemento agregado es el primero en salir. Como una pila de platos: solo puedes coger el de arriba.

#### Operaciones

| Operacion | Que hace | Coste |
|---|---|---|
| `push(x)` | Apila `x` arriba | O(1) |
| `pop()` | Quita y devuelve el de arriba | O(1) |
| `peek()` / `top()` | Mira el de arriba sin quitarlo | O(1) |
| `is_empty()` | True si esta vacia | O(1) |

#### En Python

Tres opciones:

```python
# 1. list (la mas comun, simple)
pila = []
pila.append(1)        # push
pila.append(2)
x = pila.pop()        # pop -> 2
arriba = pila[-1]     # peek -> 1

# 2. collections.deque (mejor si haces muchos pop/push)
from collections import deque
pila = deque()
pila.append(1)
pila.pop()

# 3. queue.LifoQueue (thread-safe, util en concurrencia)
from queue import LifoQueue
```

#### Casos de uso reales

- **Funciones**: la pila de llamadas (call stack) que ves en los tracebacks.
- **Deshacer/Rehacer** en editores (undo/redo).
- **Validar parentesis balanceados**: `({[]})` -> apila al abrir, desapila al cerrar.
- **DFS** (busqueda en profundidad) en grafos.
- **Evaluar expresiones** con notacion polaca inversa."""
    )},
    {"type": "md", "src": tu_turno(3,
        """Escribe una funcion `parentesis_balanceados(texto)` que reciba un string con caracteres `()`, `[]`, `{}` y devuelva `True` si todos los parentesis estan **correctamente balanceados** y `False` si no.

**Idea:** usa una pila. Por cada caracter:
- Si es de apertura (`(`, `[`, `{`), lo apilas.
- Si es de cierre, sacas el de arriba y compruebas que es el de apertura correspondiente.
- Al final la pila debe estar vacia.

Pruebalo con:
- `'({[]})'` -> True
- `'(]'`     -> False
- `'((()))'` -> True
- `'(('`     -> False"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def parentesis_balanceados(texto):\n#     pila = []\n#     pares = {')': '(', ']': '[', '}': '{'}\n#     aperturas = set('([{')\n#     for c in texto:\n#         if c in aperturas:\n#             pila.append(c)        # apilamos apertura\n#         elif c in pares:\n#             # cierre: comprobar que la apertura coincide\n#             if not pila or pila.pop() != pares[c]:\n#                 return False\n#     # Si quedaron aperturas sin cerrar, mal\n#     return len(pila) == 0\n#\n# print(parentesis_balanceados('({[]})'))   # True\n# print(parentesis_balanceados('(]'))       # False\n# print(parentesis_balanceados('((()))'))   # True\n# print(parentesis_balanceados('(('))       # False\n"},
]))

# ============ QUEUE ============
plan.append((ID_QUEUE, [
    {"type": "md", "src": teoria(
        "Cola (Queue): el primero en entrar es el primero en salir (FIFO)",
        """Una **cola** sigue el principio **FIFO** (*First In, First Out*): el primer elemento agregado es el primero en salir. Como la cola del supermercado.

#### Operaciones

| Operacion | Que hace | Coste |
|---|---|---|
| `enqueue(x)` | Agrega al final | O(1) |
| `dequeue()` | Saca y devuelve el primero | O(1) |
| `peek()` | Mira el primero sin sacarlo | O(1) |
| `is_empty()` | True si esta vacia | O(1) |

#### En Python: NO uses `list` para colas

```python
# MAL: muy lento porque pop(0) es O(n)
cola = []
cola.append(1)
cola.pop(0)        # O(n) -> desplaza todos los elementos!

# BIEN: deque tiene popleft en O(1)
from collections import deque
cola = deque()
cola.append(1)        # enqueue
cola.append(2)
x = cola.popleft()    # dequeue -> 1
```

#### Casos de uso reales

- **Colas de tareas / mensajes**: procesar trabajos en orden de llegada.
- **BFS** (busqueda en anchura) en grafos.
- **Buffer de eventos**: teclas presionadas, paquetes de red.
- **Colas de impresion**.
- **Productores-consumidores** en concurrencia (`queue.Queue` es thread-safe).

#### Variantes

- **Cola doble (deque)**: permite agregar y sacar por ambos extremos. `collections.deque`.
- **Cola circular**: tamano fijo; al llenarse, se sobrescribe la cabeza.
- **Cola de prioridad**: el orden NO es por llegada sino por una prioridad. Lo veras en la siguiente seccion."""
    )},
    {"type": "md", "src": tu_turno(4,
        """Simula un **sistema de turnos** de una panaderia. Crea una `deque` vacia y:

1. Agrega 5 clientes con nombres `'C1'`, `'C2'`, `'C3'`, `'C4'`, `'C5'` (con `append`).
2. Atiende a los 3 primeros usando `popleft()` e imprime quien se atendio.
3. Llega un cliente VIP `'VIP1'` que pasa al inicio: usa `appendleft('VIP1')`.
4. Atiende al siguiente y verifica que es el VIP.
5. Imprime los clientes que quedan en cola."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# from collections import deque\n#\n# cola = deque()\n#\n# # 1) Agregamos 5 clientes\n# for nombre in ['C1', 'C2', 'C3', 'C4', 'C5']:\n#     cola.append(nombre)\n# print('Cola inicial:', list(cola))\n#\n# # 2) Atendemos a los 3 primeros\n# for _ in range(3):\n#     atendido = cola.popleft()\n#     print('Atendido:', atendido)\n#\n# # 3) Llega un VIP que pasa al inicio\n# cola.appendleft('VIP1')\n# print('Cola tras VIP:', list(cola))\n#\n# # 4) Atendemos al siguiente\n# print('Atendido:', cola.popleft())   # VIP1\n#\n# # 5) Resto\n# print('Quedan:', list(cola))\n"},
]))

# ============ HEAP / PRIORITY QUEUE ============
plan.append((ID_HEAP, [
    {"type": "md", "src": teoria(
        "Cola de prioridad (Heap): el mas urgente primero",
        """Una **cola de prioridad** devuelve los elementos en orden de **prioridad**, no en orden de llegada. Internamente se implementa con un **heap** (monticulo): un arbol binario donde cada padre es menor (min-heap) o mayor (max-heap) que sus hijos.

#### Operaciones

| Operacion | Que hace | Coste |
|---|---|---|
| `push(x)` | Inserta `x` | O(log n) |
| `pop()` | Saca el de mayor (o menor) prioridad | O(log n) |
| `peek()` | Mira el primero sin sacarlo | O(1) |

#### En Python: modulo `heapq`

`heapq` implementa un **min-heap** sobre una lista:

```python
import heapq

heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)

print(heapq.heappop(heap))   # 1 (el menor)
print(heapq.heappop(heap))   # 2
print(heapq.heappop(heap))   # 3
```

#### Como hacer un MAX-heap?

`heapq` solo es min-heap. Truco: **negar** los valores.

```python
heapq.heappush(heap, -valor)
mayor = -heapq.heappop(heap)
```

#### Heap con elementos complejos (prioridad + dato)

Apila **tuplas** `(prioridad, dato)`. Python compara por el primer elemento.

```python
tareas = []
heapq.heappush(tareas, (2, 'limpiar'))
heapq.heappush(tareas, (1, 'urgente: bug'))
heapq.heappush(tareas, (3, 'reunion'))

while tareas:
    prio, t = heapq.heappop(tareas)
    print(prio, t)
# 1 urgente: bug
# 2 limpiar
# 3 reunion
```

#### Casos de uso reales

- **Algoritmo de Dijkstra** (caminos mas cortos).
- **Algoritmo A*** (busqueda informada).
- **Schedulers**: ejecutar tareas por prioridad.
- **Top-K**: encontrar los `k` mayores/menores en un stream."""
    )},
    {"type": "md", "src": tu_turno(5,
        """Simula un **triage de hospital**. Define una lista de pacientes como tuplas `(gravedad, nombre)` donde **menor numero = mas grave** (gravedad 1 es la maxima):

```python
pacientes = [
    (3, 'Ana'),
    (1, 'Pedro'),
    (5, 'Lucia'),
    (2, 'Carmen'),
    (4, 'Juan'),
]
```

1. Crea un heap vacio.
2. Inserta cada paciente con `heapq.heappush`.
3. Atiendelos en orden de gravedad usando `heapq.heappop` hasta vaciar el heap. Imprime el orden.

> Verifica que se atiende a Pedro primero (gravedad 1) y a Lucia al final (gravedad 5)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import heapq\n#\n# pacientes = [\n#     (3, 'Ana'),\n#     (1, 'Pedro'),\n#     (5, 'Lucia'),\n#     (2, 'Carmen'),\n#     (4, 'Juan'),\n# ]\n#\n# heap = []\n# for p in pacientes:\n#     heapq.heappush(heap, p)\n#\n# print('Orden de atencion:')\n# while heap:\n#     gravedad, nombre = heapq.heappop(heap)\n#     print(f'  Gravedad {gravedad}: {nombre}')\n"},
]))

# ============ HASH TABLE ============
plan.append((ID_HASH, [
    {"type": "md", "src": teoria(
        "Tabla hash: busqueda en tiempo casi constante",
        """Una **tabla hash** asocia **claves** con **valores** y permite consultar el valor de una clave en **O(1) promedio**. En Python es el `dict`.

#### Como funciona por dentro?

1. Se calcula `hash(clave)`: una funcion que convierte la clave en un entero.
2. Se reduce ese entero al rango de un array interno: `indice = hash % tamano`.
3. Se guarda el par `(clave, valor)` en ese indice.

```
hash('Ana') = 9028273...
9028273 % 8 = 5
-> array[5] = ('Ana', 30)
```

#### Colisiones

Dos claves distintas pueden caer en el mismo indice. Las dos estrategias clasicas:

- **Encadenamiento (chaining)**: cada celda guarda una lista de pares.
- **Direccionamiento abierto**: si la celda esta ocupada, prueba la siguiente.

Python usa una variante de direccionamiento abierto.

#### Costes

| Operacion | Promedio | Peor caso |
|---|---|---|
| Insertar | **O(1)** | O(n) (muchas colisiones) |
| Buscar | **O(1)** | O(n) |
| Borrar | **O(1)** | O(n) |

#### Que tipos pueden ser claves?

Solo objetos **hashables** (inmutables): `int`, `float`, `str`, `tuple` (de hashables), `frozenset`, etc.

**NO** se pueden usar como clave: `list`, `dict`, `set` (mutables).

```python
d = {}
d[(1, 2)] = 'ok'      # tupla -> ok
# d[[1, 2]] = 'no'    # TypeError: unhashable
```

#### Operaciones tipicas en `dict`

```python
d = {'a': 1, 'b': 2}
d['c'] = 3            # insertar/actualizar
d.get('x', 0)         # default si no existe
'a' in d              # True (busqueda O(1))
del d['a']            # borrar
for k, v in d.items():
    print(k, v)
```

#### Set: la primita del dict

`set` es una tabla hash sin valores (solo claves). Util para:
- Quitar duplicados: `set([1, 2, 2, 3]) -> {1, 2, 3}`.
- Test de pertenencia rapido: `x in mi_set` es O(1)."""
    )},
    {"type": "md", "src": tu_turno(6,
        """**Contador de palabras.** Dado el texto:

```python
texto = "el gato come el pescado y el pato come pan"
```

Cuenta cuantas veces aparece cada palabra y ordena el resultado de mas frecuente a menos frecuente.

**Pasos sugeridos:**

1. Divide en palabras con `texto.split()`.
2. Usa un `dict` (o `collections.Counter`) para contar.
3. Ordena con `sorted(d.items(), key=lambda x: x[1], reverse=True)`.

> Bonus: hazlo tambien usando `collections.Counter(palabras).most_common()`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# texto = 'el gato come el pescado y el pato come pan'\n# palabras = texto.split()\n#\n# # Version 1: dict manual con .get\n# conteo = {}\n# for p in palabras:\n#     conteo[p] = conteo.get(p, 0) + 1\n# print('Conteo:', conteo)\n#\n# # Ordenado por frecuencia descendente\n# orden = sorted(conteo.items(), key=lambda x: x[1], reverse=True)\n# print('Ordenado:', orden)\n#\n# # Version 2: Counter (idiomatico)\n# from collections import Counter\n# c = Counter(palabras)\n# print('Most common:', c.most_common())\n"},
]))

# ============ GRAFO ============
plan.append((ID_GRAPH, [
    {"type": "md", "src": teoria(
        "Grafo: nodos conectados por aristas",
        """Un **grafo** es un conjunto de **nodos (vertices)** conectados por **aristas (edges)**. Modelan relaciones: redes sociales, mapas de carreteras, dependencias entre tareas, etc.

#### Tipos

| Tipo | Caracteristicas | Ejemplo |
|---|---|---|
| **No dirigido** | Aristas sin direccion | Amistades en Facebook |
| **Dirigido** (digrafo) | Aristas con direccion | Seguidores en Twitter, web links |
| **Ponderado** | Las aristas tienen peso | Distancia entre ciudades |
| **Ciclico / Aciclico** | Tiene ciclos o no (DAG) | DAG: dependencias de tareas |

#### Representaciones tipicas

**1. Lista de adyacencia** (la mas comun, eficiente en memoria):

```python
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A'],
    'D': ['B'],
}
```

**2. Matriz de adyacencia** (`n x n`):

```
    A  B  C  D
A [ 0  1  1  0 ]
B [ 1  0  0  1 ]
C [ 1  0  0  0 ]
D [ 0  1  0  0 ]
```

| | Lista de adyacencia | Matriz de adyacencia |
|---|---|---|
| Memoria | O(V + E) | O(V^2) |
| Saber si A conecta con B | O(grado(A)) | **O(1)** |
| Iterar vecinos | **Eficiente** | O(V) |

#### Algoritmos clasicos

- **BFS** (busqueda en anchura): usa **cola**. Encuentra el camino mas corto en aristas.
- **DFS** (busqueda en profundidad): usa **pila** o recursion. Util para detectar ciclos.
- **Dijkstra**: caminos mas cortos en grafos ponderados (heap).
- **Topological sort**: ordenar tareas con dependencias (DAG).

#### En Python real

Para algo serio, usa la libreria **`networkx`**:

```python
import networkx as nx
G = nx.Graph()
G.add_edge('A', 'B')
G.add_edge('A', 'C')
nx.shortest_path(G, 'B', 'C')   # ['B', 'A', 'C']
```"""
    )},
    {"type": "md", "src": tu_turno(7,
        """**Implementa BFS** (busqueda en anchura) sobre una lista de adyacencia.

Dado el grafo:

```python
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E'],
}
```

Escribe `bfs(grafo, inicio)` que devuelva la lista de nodos visitados en orden de descubrimiento, partiendo del nodo `inicio`.

**Pista:**
- Usa una **cola** (`collections.deque`).
- Mantén un `set` de visitados para no repetir.
- Empieza encolando el nodo inicial. Mientras la cola no este vacia, sacas un nodo, lo marcas, anades sus vecinos no visitados.

Pruebalo con `bfs(grafo, 'A')`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# from collections import deque\n#\n# def bfs(grafo, inicio):\n#     visitados = set()\n#     orden = []\n#     cola = deque([inicio])\n#     visitados.add(inicio)\n#     while cola:\n#         nodo = cola.popleft()\n#         orden.append(nodo)\n#         for vecino in grafo[nodo]:\n#             if vecino not in visitados:\n#                 visitados.add(vecino)\n#                 cola.append(vecino)\n#     return orden\n#\n# grafo = {\n#     'A': ['B', 'C'],\n#     'B': ['A', 'D', 'E'],\n#     'C': ['A', 'F'],\n#     'D': ['B'],\n#     'E': ['B', 'F'],\n#     'F': ['C', 'E'],\n# }\n#\n# print(bfs(grafo, 'A'))\n# # Posible salida: ['A', 'B', 'C', 'D', 'E', 'F']\n"},
]))

# ============ SOFTWARE CRAFTSMANSHIP ============
plan.append((ID_CRAFT, [
    {"type": "md", "src": teoria(
        "Software Craftsmanship: por que importa el codigo limpio",
        """**Software Craftsmanship** es la idea de tratar el desarrollo como un **oficio**: con orgullo, calidad y mejora continua. El movimiento se popularizo con libros como *Clean Code* (Robert C. Martin) y *The Pragmatic Programmer*.

#### Por que importa?

- **Pasamos mas tiempo leyendo codigo que escribiendolo** (proporcion 10:1 segun Uncle Bob). Codigo legible = mas productividad.
- **Los bugs viven en el codigo confuso.** Codigo claro = menos errores.
- **El equipo cambia.** Tu codigo debe ser mantenible por alguien que llega manana.
- **Refactorizar codigo malo es caro.** El "deuda tecnica" se paga con intereses.

#### Reglas basicas (resumen del libro Clean Code)

1. **Nombres significativos**: `n` -> `numero_alumnos`. Variable, funcion y clase deben decir QUE son.
2. **Funciones cortas**: idealmente menos de 20 lineas. Una sola responsabilidad.
3. **Argumentos pocos**: 0-2 ideales, 3 ya es mucho. Mas de 3 -> agrupa en objeto.
4. **Sin duplicacion (DRY)**: *Don't Repeat Yourself*. Cada conocimiento, una sola vez.
5. **Comentarios solo para el porque**: el codigo dice QUE hace. El comentario dice POR QUE.
6. **Manejo de errores explicito**: no silencies excepciones, no ignores codigos de error.
7. **Tests**: codigo sin tests es legacy desde el dia 1.

#### Principios SOLID (orientacion a objetos)

| Letra | Principio | Idea |
|---|---|---|
| **S** | Single Responsibility | Una clase, una razon para cambiar |
| **O** | Open/Closed | Abierto a extension, cerrado a modificacion |
| **L** | Liskov Substitution | Subclases deben ser intercambiables con su padre |
| **I** | Interface Segregation | Interfaces pequenas, especificas |
| **D** | Dependency Inversion | Depende de abstracciones, no de implementaciones |

#### El boy scout rule

> "Deja el codigo mas limpio de como lo encontraste."

Cada vez que tocas un fichero, mejoralo un poco: renombra una variable, extrae una funcion, anade un test."""
    )},
    {"type": "md", "src": aviso(
        """**Senales de alarma (code smells)** que debes detectar y refactorizar:

- Funcion con mas de 50 lineas. Probablemente hace varias cosas.
- Clase con mas de 500 lineas. Probablemente viola SRP.
- Funcion con mas de 4 argumentos. Difícil de usar y probar.
- Variables `temp`, `data`, `aux`, `x1`, `x2`. Renombra.
- `if/elif/else` larguisimo. Usa polimorfismo o un dict de funciones.
- Comentarios que explican un trozo confuso. Renombra y extrae funciones en su lugar.
- Codigo duplicado en varios sitios. Extrae a una funcion.
- "Numeros magicos" sin nombre. Crea constantes: `MAX_ALUMNOS = 30`."""
    )},
    {"type": "md", "src": tu_turno(8,
        """**Refactoriza** este codigo aplicando los principios de codigo limpio:

```python
def f(l):
    s = 0
    for i in range(len(l)):
        if l[i] > 0:
            s += l[i]
    return s
```

Mejoras a aplicar:

1. Renombra `f`, `l`, `s`, `i` con nombres significativos.
2. Anade un docstring explicando que hace.
3. Anade type hints: `(numeros: list[int]) -> int`.
4. Reescribe el bucle de forma mas idiomatica (sin `range(len(...))`).
5. Bonus: usa `sum()` con generator expression para hacerlo en una linea."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def suma_positivos(numeros: list[int]) -> int:\n#     '''Devuelve la suma de los numeros positivos de la lista.'''\n#     total = 0\n#     for numero in numeros:\n#         if numero > 0:\n#             total += numero\n#     return total\n#\n# # Version aun mas idiomatica (one-liner pythonico)\n# def suma_positivos_v2(numeros: list[int]) -> int:\n#     '''Devuelve la suma de los numeros positivos de la lista.'''\n#     return sum(n for n in numeros if n > 0)\n#\n# print(suma_positivos([1, -2, 3, -4, 5]))     # 9\n# print(suma_positivos_v2([1, -2, 3, -4, 5]))  # 9\n"},
]))

# ============ TESTING ============
plan.append((ID_TESTING, [
    {"type": "md", "src": teoria(
        "Software Testing: por que probar tu codigo automaticamente",
        """Un **test automatizado** es codigo que **prueba otro codigo**. Tipicamente:

1. Crea un escenario de partida (*setup*).
2. Ejecuta la accion bajo prueba.
3. Verifica que el resultado coincide con lo esperado (*assert*).
4. Limpia (*teardown*).

#### Por que automatizar?

| Sin tests | Con tests |
|---|---|
| Probar a mano cada cambio | Ejecutas `pytest` y todo se valida |
| Miedo a refactorizar | Refactorizas con red de seguridad |
| Bugs en produccion | Bugs detectados antes de mergear |
| Documentacion desactualizada | Tests = documentacion ejecutable |

#### La piramide de testing

```
            /\\
           /  \\   E2E (pocos, lentos, frágiles)
          /----\\
         /      \\  Integracion
        /--------\\
       /          \\ Unitarios (muchos, rapidos)
      /____________\\
```

- **Unitarios**: prueban una funcion / clase aislada. Rapidos (ms). Muchos.
- **Integracion**: prueban como interactuan varios componentes (DB, API).
- **End-to-end (E2E)**: prueban el sistema completo desde la UI o la API publica. Lentos.

**Regla del 70/20/10**: 70% unitarios, 20% integracion, 10% E2E.

#### TDD: Test-Driven Development

Ciclo **rojo-verde-refactor**:

1. **Rojo**: escribe un test que falla.
2. **Verde**: escribe el codigo MINIMO para que pase.
3. **Refactor**: limpia sin romper los tests.

Beneficios: te obliga a pensar la API antes de implementar, te da cobertura desde el inicio, te lleva a un diseno mas modular.

#### PyTest: el framework estandar de Python

```python
# fichero: test_calculadora.py

def suma(a, b):
    return a + b

def test_suma_positivos():
    assert suma(2, 3) == 5

def test_suma_negativos():
    assert suma(-1, -1) == -2

def test_suma_cero():
    assert suma(0, 0) == 0
```

Para ejecutar: `pytest` (descubre automaticamente los `test_*.py`).

#### Convenciones de PyTest

- Ficheros: `test_*.py` o `*_test.py`.
- Funciones: `test_*`.
- Clases: `Test*`.
- Aserciones: simplemente `assert` (no necesitas `assertEqual`).

#### Fixtures (preparar el entorno)

```python
import pytest

@pytest.fixture
def lista_vacia():
    return []

def test_append(lista_vacia):
    lista_vacia.append(1)
    assert lista_vacia == [1]
```

#### Parametrizar tests (varios casos en un solo test)

```python
@pytest.mark.parametrize('a,b,esperado', [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_suma(a, b, esperado):
    assert suma(a, b) == esperado
```"""
    )},
    {"type": "md", "src": dato(
        """**Cobertura (coverage)**: porcentaje de lineas de codigo cubiertas por tests. Se mide con `pytest --cov`.

- 100% cobertura NO garantiza que no haya bugs (puedes cubrir lineas sin verificar bien).
- Pero <50% suele indicar zonas frias donde los bugs prosperan.
- Un objetivo razonable en producion: 70-90% en logica de negocio."""
    )},
    {"type": "md", "src": tu_turno(9,
        """Vas a practicar **TDD** con una funcion sencilla.

**Paso 1: tests primero (rojo).** Escribe los siguientes tests **antes** de implementar la funcion `es_palindromo(texto)`. Un palindromo es una palabra que se lee igual al derecho y al reves (ignora mayusculas).

```python
def test_palindromo_simple():
    assert es_palindromo('oso') == True

def test_no_palindromo():
    assert es_palindromo('python') == False

def test_palindromo_vacio():
    assert es_palindromo('') == True

def test_ignora_mayusculas():
    assert es_palindromo('AnA') == True
```

**Paso 2: implementacion (verde).** Implementa `es_palindromo(texto)` para que TODOS los tests pasen.

**Paso 3:** ejecuta los tests llamandolos a mano (sin pytest) y verifica que ninguno levanta `AssertionError`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# def es_palindromo(texto: str) -> bool:\n#     '''Devuelve True si el texto se lee igual al derecho y al reves.\n#     No distingue mayusculas/minusculas.'''\n#     limpio = texto.lower()\n#     return limpio == limpio[::-1]\n#\n# # Tests (los escribirias en TDD ANTES de la implementacion)\n# def test_palindromo_simple():\n#     assert es_palindromo('oso') == True\n#\n# def test_no_palindromo():\n#     assert es_palindromo('python') == False\n#\n# def test_palindromo_vacio():\n#     assert es_palindromo('') == True\n#\n# def test_ignora_mayusculas():\n#     assert es_palindromo('AnA') == True\n#\n# # Ejecucion manual\n# for nombre, t in list(globals().items()):\n#     if nombre.startswith('test_'):\n#         try:\n#             t()\n#             print(f'OK   - {nombre}')\n#         except AssertionError:\n#             print(f'FAIL - {nombre}')\n"},
]))


enhance(NB, plan)
print("Done.")

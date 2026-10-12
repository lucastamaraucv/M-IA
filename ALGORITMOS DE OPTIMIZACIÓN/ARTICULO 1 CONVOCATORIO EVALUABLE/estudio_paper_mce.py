"""
GUIA DE ESTUDIO: Parallelizing Maximal Clique Enumeration on GPUs
Paper: Almasri et al., PACT 2023 — arXiv:2212.01473v3

Ejecuta este archivo completo o seccion por seccion.
Cada bloque tiene teoria + codigo + salida explicada.
"""

import time
import random
from collections import defaultdict, deque

SEPARADOR = "=" * 70
SUBSEP    = "-" * 50


# =============================================================================
# UTILIDAD: imprimir secciones con formato
# =============================================================================

def titulo(texto):
    print(f"\n{SEPARADOR}")
    print(f"  {texto}")
    print(SEPARADOR)

def subtitulo(texto):
    print(f"\n{SUBSEP}")
    print(f"  {texto}")
    print(SUBSEP)

def pausa():
    input("\n  [ENTER para continuar...]\n")


# =============================================================================
# MODULO 1: FUNDAMENTOS DE TEORIA DE GRAFOS
# =============================================================================

titulo("MODULO 1 — TEORIA DE GRAFOS: CONCEPTOS BASICOS")

print("""
Un GRAFO G = (V, E) tiene:
  V = conjunto de vertices (nodos)
  E = conjunto de aristas (conexiones entre nodos)

Analogia: una red social
  Personas  → vertices
  Amistades → aristas
""")

# ---- Representacion de un grafo ----
subtitulo("1.1 Representacion de un grafo como lista de adyacencia")

def crear_grafo(aristas):
    """
    Recibe lista de pares (u, v) y devuelve diccionario de adyacencia.
    El grafo es no dirigido: si existe (u,v) tambien existe (v,u).
    """
    grafo = defaultdict(set)
    for u, v in aristas:
        grafo[u].add(v)
        grafo[v].add(u)
    return grafo

# Grafo de ejemplo: 6 nodos, varios cliques
aristas_ejemplo = [
    (0, 1), (0, 2), (1, 2),   # triangulo {0,1,2}
    (1, 3), (2, 3), (3, 4),   # {1,2,3} otro triangulo, 3-4
    (4, 5), (3, 5),            # {3,4,5}
]

G = crear_grafo(aristas_ejemplo)

print("Grafo de ejemplo (lista de adyacencia):")
for nodo in sorted(G):
    vecinos = sorted(G[nodo])
    print(f"  Nodo {nodo} → vecinos: {vecinos}")

print("""
Visualizacion:
  0 - 1 - 3 - 5
  |\ |   |\ /
  | \|   | 4
  2--+   |/
     \---3

  Cliques visibles a simple vista:
    {0,1,2} → todos conectados entre si
    {1,2,3} → todos conectados entre si
    {3,4,5} → todos conectados entre si
""")

pausa()


# ---- Definicion de clique y verificacion ----
subtitulo("1.2 ¿Que es un Clique? Definicion y verificacion")

print("""
Un CLIQUE es un subconjunto S de vertices donde
TODOS los pares de vertices en S estan conectados.

Formalmente: para todo u,v en S → (u,v) en E
""")

def es_clique(grafo, subconjunto):
    """
    Verifica si un subconjunto de vertices forma un clique.
    Revisa que cada par de vertices este conectado.
    """
    vertices = list(subconjunto)
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            u, v = vertices[i], vertices[j]
            if v not in grafo[u]:
                return False
    return True

# Probamos distintos subconjuntos
candidatos = [
    {0, 1, 2},    # triangulo completo
    {0, 1, 3},    # 0 y 3 no estan conectados
    {1, 2, 3},    # triangulo completo
    {3, 4, 5},    # triangulo completo
    {0, 1, 2, 3}, # demasiado grande
]

print("Verificando si cada conjunto es un clique:\n")
for c in candidatos:
    resultado = es_clique(G, c)
    simbolo = "✓ CLIQUE    " if resultado else "✗ NO clique "
    print(f"  {simbolo} {sorted(c)}")

pausa()


# ---- Clique Maximal vs Maximo ----
subtitulo("1.3 Diferencia crucial: Clique MAXIMAL vs Clique MAXIMO")

print("""
┌─────────────────────────────────────────────────────────┐
│  CLIQUE MAXIMAL:                                        │
│    No se puede agregar ningun vertice mas.              │
│    Puede haber MUCHOS en un grafo.                      │
│                                                         │
│  CLIQUE MAXIMO (maximum):                              │
│    El de mayor tamaño en TODO el grafo.                 │
│    Puede ser unico o haber varios del mismo tamaño.     │
│                                                         │
│  REGLA: Todo maximo es maximal.                         │
│          NO todo maximal es maximo.                     │
└─────────────────────────────────────────────────────────┘
""")

def es_clique_maximal(grafo, subconjunto):
    """
    Un clique es maximal si:
    1. Es un clique.
    2. No se puede agregar ningun vertice exterior.
    """
    if not es_clique(grafo, subconjunto):
        return False
    todos_los_nodos = set(grafo.keys())
    nodos_fuera = todos_los_nodos - subconjunto
    for v in nodos_fuera:
        # ¿puedo agregar v? solo si v es vecino de TODOS en el subconjunto
        if all(v in grafo[u] for u in subconjunto):
            return False  # se puede extender → no es maximal
    return True

print("Verificando maximalidad:\n")
for c in candidatos:
    es_c   = es_clique(G, c)
    es_max = es_clique_maximal(G, c) if es_c else False
    print(f"  {sorted(c)}")
    print(f"    ¿Es clique?          {'Si' if es_c else 'No'}")
    print(f"    ¿Es clique maximal?  {'Si' if es_max else 'No'}")

pausa()


# =============================================================================
# MODULO 2: EL PROBLEMA MCE
# =============================================================================

titulo("MODULO 2 — MCE: MAXIMAL CLIQUE ENUMERATION")

print("""
MCE = Encontrar TODOS los cliques maximales de un grafo.
      No uno. No el mas grande. TODOS.

¿Por que es dificil?
  - Puede haber hasta 3^(n/3) cliques maximales (exponencial).
  - Para n=30 nodos → hasta ~2 millones de cliques posibles.
  - Es un problema NP-Hard.

Aplicaciones reales:
  → Redes sociales: detectar comunidades
  → Bioinformatica: proteinas que interactuan
  → Deteccion de fraude: grupos de cuentas sospechosas
  → Analisis de codigo: modulos fuertemente acoplados
""")

def contar_cliques_maximales(grafo):
    """Cuenta cuantos cliques maximales tiene el grafo (fuerza bruta)."""
    nodos = list(grafo.keys())
    n = len(nodos)
    count = 0
    for tam in range(1, n + 1):
        from itertools import combinations
        for combo in combinations(nodos, tam):
            s = set(combo)
            if es_clique_maximal(grafo, s):
                count += 1
    return count

from itertools import combinations

def listar_cliques_maximales_fuerza_bruta(grafo):
    """Fuerza bruta O(2^n): lista todos los cliques maximales."""
    nodos = list(grafo.keys())
    n = len(nodos)
    resultado = []
    for tam in range(1, n + 1):
        for combo in combinations(nodos, tam):
            s = frozenset(combo)
            if es_clique_maximal(grafo, s):
                resultado.append(s)
    return resultado

subtitulo("2.1 Encontrando todos los cliques maximales (fuerza bruta)")

cliques_fb = listar_cliques_maximales_fuerza_bruta(G)
print(f"Grafo de {len(G)} nodos → {len(cliques_fb)} cliques maximales:\n")
for i, c in enumerate(sorted(cliques_fb, key=lambda x: sorted(x))):
    print(f"  CM{i+1}: {sorted(c)}")

print("""
¿Por que la fuerza bruta es impractica?
  n=10  → 1024 subconjuntos a verificar
  n=30  → 1,073,741,824 subconjuntos
  n=60  → 1.15 × 10^18 subconjuntos  (imposible)
""")

pausa()


# =============================================================================
# MODULO 3: ALGORITMO BRON-KERBOSCH
# =============================================================================

titulo("MODULO 3 — ALGORITMO BRON-KERBOSCH")

subtitulo("3.1 Los tres conjuntos R, P, X")

print("""
El algoritmo mantiene 3 conjuntos en cada llamada recursiva:

  R (Result)   → vertices del clique que estoy construyendo AHORA
  P (Possible) → vertices que PUEDO agregar a R (son vecinos de todos en R)
  X (Excluded) → vertices que ya PROCESE en otra rama anterior

CONDICION DE EXITO: si P = ∅ y X = ∅ → R es un clique maximal

CONDICION DE PODA:  si P = ∅ pero X ≠ ∅ → algun vertice en X ya extiende R
                    entonces R no es maximal (no lo reportamos)

INICIO: R = {}, P = todos los vertices, X = {}
""")

pausa()

subtitulo("3.2 Bron-Kerbosch version basica (sin pivote) — con traza")

cliques_encontrados = []

def bron_kerbosch_basico(grafo, R, P, X, profundidad=0, traza=True):
    """
    Version basica del algoritmo Bron-Kerbosch sin optimizacion de pivote.

    Parametros:
        grafo : diccionario de adyacencia
        R     : clique actual (frozenset)
        P     : candidatos a agregar (set)
        X     : excluidos (set)
        profundidad : nivel del arbol de busqueda (para visualizacion)
    """
    indent = "  " * profundidad

    if traza:
        print(f"{indent}BK(R={sorted(R)}, P={sorted(P)}, X={sorted(X)})")

    # Condicion de parada: encontramos un clique maximal
    if not P and not X:
        cliques_encontrados.append(frozenset(R))
        if traza:
            print(f"{indent}  *** CLIQUE MAXIMAL ENCONTRADO: {sorted(R)} ***")
        return

    for v in list(P):
        vecinos_v = grafo[v]
        # Agregar v al clique actual
        nueva_R = R | {v}
        nueva_P = P & vecinos_v   # solo candidatos que tambien son vecinos de v
        nueva_X = X & vecinos_v   # solo excluidos que tambien son vecinos de v

        bron_kerbosch_basico(grafo, nueva_R, nueva_P, nueva_X,
                             profundidad + 1, traza)

        # Mover v de P a X (ya fue procesado en esta rama)
        P = P - {v}
        X = X | {v}

# Grafo pequeño para ver la traza completa
aristas_pequeno = [(0,1), (0,2), (1,2), (1,3), (2,3)]
G_pequeno = crear_grafo(aristas_pequeno)

print("Grafo pequeño: aristas =", aristas_pequeno)
print("\nArbol de busqueda Bron-Kerbosch (traza completa):\n")

cliques_encontrados = []
nodos = set(G_pequeno.keys())
bron_kerbosch_basico(G_pequeno, frozenset(), nodos.copy(), set(), traza=True)

print(f"\nCliques maximales encontrados: {len(cliques_encontrados)}")
for c in cliques_encontrados:
    print(f"  {sorted(c)}")

pausa()


subtitulo("3.3 Bron-Kerbosch CON PIVOTE — optimizacion clave")

print("""
PROBLEMA de la version basica:
  Itera sobre TODOS los vertices de P en cada nivel.
  Genera ramas redundantes.

SOLUCION — Seleccion de pivote:
  1. Elegir un pivote u ∈ P ∪ X con el MAXIMO numero de vecinos en P.
  2. Solo iterar sobre vertices de P que NO son vecinos del pivote.

¿POR QUE FUNCIONA?
  Todo clique maximal debe contener al menos un vertice
  que NO sea vecino del pivote.
  (Si todos los vertices del clique fueran vecinos del pivote,
   podriamos agregar el pivote → contradice maximalidad)
""")

def seleccionar_pivote(grafo, P, X):
    """
    Selecciona el pivote u ∈ P ∪ X con mas vecinos en P.
    Minimiza el numero de iteraciones en el bucle principal.
    """
    mejor_pivote = None
    max_vecinos_en_P = -1
    for u in P | X:
        vecinos_en_P = len(grafo[u] & P)
        if vecinos_en_P > max_vecinos_en_P:
            max_vecinos_en_P = vecinos_en_P
            mejor_pivote = u
    return mejor_pivote

cliques_con_pivote = []

def bron_kerbosch_pivote(grafo, R, P, X, profundidad=0, traza=True):
    """
    Bron-Kerbosch con seleccion de pivote.
    Mucho mas eficiente que la version basica.
    """
    indent = "  " * profundidad

    if not P and not X:
        cliques_con_pivote.append(frozenset(R))
        if traza:
            print(f"{indent}*** CLIQUE: {sorted(R)} ***")
        return

    # Seleccionar pivote
    pivote = seleccionar_pivote(grafo, P, X)

    if traza and (P or X):
        print(f"{indent}R={sorted(R)} | Pivote elegido: {pivote} | Candidatos: {sorted(P - grafo[pivote])}")

    # Iterar solo sobre P \ N(pivote)
    for v in list(P - grafo[pivote]):
        vecinos_v = grafo[v]
        bron_kerbosch_pivote(
            grafo,
            R | {v},
            P & vecinos_v,
            X & vecinos_v,
            profundidad + 1,
            traza
        )
        P = P - {v}
        X = X | {v}

print("Misma ejecucion pero CON pivote (menos ramas):\n")
cliques_con_pivote = []
nodos_p = set(G_pequeno.keys())
bron_kerbosch_pivote(G_pequeno, frozenset(), nodos_p.copy(), set(), traza=True)

print(f"\nResultado identico: {len(cliques_con_pivote)} cliques maximales")
for c in cliques_con_pivote:
    print(f"  {sorted(c)}")

pausa()


# =============================================================================
# MODULO 4: EL ARBOL DE BUSQUEDA — BFS vs DFS
# =============================================================================

titulo("MODULO 4 — EL ARBOL DE BUSQUEDA: BFS vs DFS")

print("""
La recursion de Bron-Kerbosch genera un ARBOL DE BUSQUEDA.

  Cada NODO del arbol = un estado (R, P, X)
  Las HOJAS = cliques maximales (cuando P=∅ y X=∅)
  Las RAMAS = las decisiones de agregar un vertice v

Hay dos estrategias para recorrer este arbol:
""")

subtitulo("4.1 DFS — Depth-First Search (Lo que usa el paper)")

print("""
DFS = ir hasta el fondo de una rama antes de explorar la siguiente.

Visualizacion con nuestro grafo pequeno:

  Estado raiz: R={}, P={0,1,2,3}
  │
  ├─ agrego v=0 → R={0}, P={1,2}
  │   ├─ agrego v=1 → R={0,1}, P={2}
  │   │   └─ agrego v=2 → R={0,1,2}, P={} X={} → *** CLIQUE {0,1,2} ***
  │   └─ agrego v=2 → R={0,2}, P={} X={1}  → (no reportar, X≠∅)
  │
  ├─ agrego v=1 → R={1}, P={2,3}
  │   ├─ agrego v=2 → R={1,2}, P={3}
  │   │   └─ agrego v=3 → R={1,2,3}, P={} X={} → *** CLIQUE {1,2,3} ***
  │   └─ agrego v=3 → R={1,3}, P={} X={2}  → (no reportar)
  │
  └─ agrego v=2 → ...

DFS: cada rama se explora COMPLETAMENTE antes de pasar a la siguiente.
     → Uso de memoria acotado (proporcional a la profundidad del arbol)
""")

subtitulo("4.2 BFS — Breadth-First Search (Lo que hacian trabajos previos)")

print("""
BFS = explorar todos los nodos del nivel 1, luego todos del nivel 2, etc.

Nivel 0: [{}, P=todos]
Nivel 1: [{0}, P={1,2}]   [{1}, P={2,3}]   [{2}, P={3}]   [{3}, P={}]
Nivel 2: [{0,1},P={2}]  [{0,2},P={}}]  [{1,2},P={3}] [{1,3},P={}] ...
...

PROBLEMA del BFS en grafos grandes:
  En niveles profundos puede haber MILLONES de nodos activos simultaneamente.
  Cada nodo necesita almacenar su estado (R, P, X).
  → Explosion de memoria → la GPU se queda sin memoria.

VENTAJA del DFS (propuesta del paper):
  Solo se mantiene UN camino activo a la vez.
  Memoria proporcional a la profundidad, no al ancho del arbol.
""")

# Demostracion: contar nodos por nivel en BFS vs DFS
def contar_nodos_bfs_por_nivel(grafo):
    """Simula el BFS y cuenta cuantos nodos habria en cada nivel."""
    nodos_iniciales = set(grafo.keys())
    # Nivel 0: estado inicial
    cola = [(frozenset(), nodos_iniciales.copy(), set())]
    niveles = []

    for nivel in range(5):
        if not cola:
            break
        niveles.append(len(cola))
        siguiente_cola = []
        for R, P, X in cola:
            pivote = seleccionar_pivote(grafo, P, X) if P or X else None
            candidatos = P - grafo[pivote] if pivote is not None else P
            for v in candidatos:
                vecinos_v = grafo[v]
                nueva_R = R | {v}
                nueva_P = P & vecinos_v
                nueva_X = X & vecinos_v
                if nueva_P or nueva_X or True:
                    siguiente_cola.append((nueva_R, nueva_P, nueva_X))
            P_nuevo = P.copy()
            X_nuevo = X.copy()
        cola = siguiente_cola

    return niveles

print("\nSimulacion: cuantos nodos activos hay en cada nivel (BFS):")
niveles = contar_nodos_bfs_por_nivel(G)
for i, count in enumerate(niveles):
    barra = "█" * count
    print(f"  Nivel {i}: {count:4d} nodos  {barra}")

print("""
  En grafos reales con miles de nodos, el nivel 3-4 puede tener
  MILLONES de nodos simultaneos → inviable con BFS en GPU.
""")

pausa()


# =============================================================================
# MODULO 5: PARALELISMO Y GPU (conceptual en Python)
# =============================================================================

titulo("MODULO 5 — PARALELISMO: CONCEPTOS GPU")

print("""
Las GPUs tienen miles de nucleos que pueden ejecutar codigo en PARALELO.

Jerarquia de una GPU NVIDIA (CUDA):

  GPU
  └── Streaming Multiprocessors (SMs)
       └── Warps (grupos de 32 hilos)
            └── Threads (hilos individuales)

Modelo SIMT: Single Instruction, Multiple Threads
  → 32 hilos de un warp ejecutan LA MISMA instruccion
  → pero cada uno con DIFERENTES datos

Memoria:
  Global Memory   : grande, lenta, accesible por todos
  Shared Memory   : pequeña, rapida, compartida por un bloque
  Register Memory : muy rapida, privada de cada hilo
""")

subtitulo("5.1 Warp Divergence — el enemigo del paralelismo GPU")

print("""
PROBLEMA: si dentro de un warp los hilos toman ramas distintas (if/else),
          los hilos que no cumplen la condicion ESPERAN.

  Hilo  0: if (v in P):  → SI  ← ejecuta
  Hilo  1: if (v in P):  → NO  ← espera
  Hilo  2: if (v in P):  → SI  ← ejecuta
  ...

  El warp SERIALIZA: primero ejecuta los SI, luego los NO.
  Perdida de rendimiento proporcional al nivel de divergencia.

En MCE esto es critico porque cada vertice tiene distinto numero de vecinos
→ distintos tamaños de P → distintas profundidades del arbol → DIVERGENCIA.

La solucion del paper (Worker List) ayuda a reducir este desbalance.
""")

subtitulo("5.2 Simulacion de paralelismo con threads Python")

import threading

def explorar_subconjunto(grafo, R_inicial, P_inicial, X_inicial, resultados, lock):
    """
    Simula un 'hilo GPU' que explora independientemente un subárbol.
    En Python usamos threading para ilustrar la idea.
    """
    cliques_locales = []

    def bk(R, P, X):
        if not P and not X:
            cliques_locales.append(frozenset(R))
            return
        pivote = seleccionar_pivote(grafo, P, X)
        for v in list(P - grafo[pivote]):
            vecinos_v = grafo[v]
            bk(R | {v}, P & vecinos_v, X & vecinos_v)
            P = P - {v}; X = X | {v}

    bk(R_inicial, P_inicial, X_inicial)

    with lock:
        resultados.extend(cliques_locales)

# Dividimos el trabajo inicial entre 'hilos' (como haria la GPU)
print("Simulando paralelismo: dividiendo el trabajo entre hilos...\n")

nodos_grafo = set(G.keys())
# El hilo 0 del GPU empieza con v=0, el hilo 1 con v=1, etc.
resultados_paralelos = []
hilos = []
lock = threading.Lock()

P_global = nodos_grafo.copy()
X_global = set()

for v in sorted(nodos_grafo):
    vecinos_v = G[v]
    R_hilo = frozenset({v})
    P_hilo = P_global & vecinos_v
    X_hilo = X_global & vecinos_v

    t = threading.Thread(
        target=explorar_subconjunto,
        args=(G, R_hilo, P_hilo, X_hilo, resultados_paralelos, lock)
    )
    hilos.append((v, t))
    P_global = P_global - {v}
    X_global = X_global | {v}

print(f"  Lanzando {len(hilos)} hilos (uno por vertice inicial)...\n")

inicio = time.time()
for v, t in hilos:
    t.start()
    print(f"  Hilo {v}: explorando subárbol con raiz v={v}")
for v, t in hilos:
    t.join()
fin = time.time()

# Eliminar duplicados
resultados_unicos = list(set(resultados_paralelos))
print(f"\n  Hilos finalizados en {(fin-inicio)*1000:.2f} ms")
print(f"  Cliques encontrados en paralelo: {len(resultados_unicos)}")
for c in sorted(resultados_unicos, key=lambda x: sorted(x)):
    print(f"    {sorted(c)}")

pausa()


# =============================================================================
# MODULO 6: CONTRIBUCIONES DEL PAPER
# =============================================================================

titulo("MODULO 6 — CONTRIBUCIONES DEL PAPER: LAS 3 IDEAS CLAVE")

subtitulo("6.1 Worker List — Balanceo Dinamico de Carga")

print("""
PROBLEMA: Desbalance de carga (Load Imbalance)

  Algunos subarboles tienen MILES de cliques (trabajo pesado).
  Otros tienen 0 cliques (trabajo trivial).

  Si el hilo GPU-0 toma un subárbol pesado y GPU-1 toma uno trivial:
    GPU-0: trabajando 10 minutos
    GPU-1: termino en 1 segundo y esta INACTIVO
    → Desperdicio del 90% del hardware

SOLUCION: Worker List (Lista de trabajadores)

  Una cola compartida de subárboles pendientes.

  Cuando un hilo termina su trabajo actual:
    → Toma el siguiente subárbol disponible de la lista.

  Cuando un hilo tiene un subárbol muy grande:
    → Puede dividirlo y poner subproblemas en la lista
      para que otros hilos los tomen.

  Resultado: todos los hilos trabajan constantemente.
""")

class WorkerList:
    """
    Simulacion de la Worker List del paper.
    Cola thread-safe de subproblemas pendientes.
    """
    def __init__(self):
        self._cola = deque()
        self._lock = threading.Lock()
        self._completados = 0

    def agregar(self, tarea):
        with self._lock:
            self._cola.append(tarea)

    def tomar(self):
        with self._lock:
            if self._cola:
                return self._cola.popleft()
            return None

    def marcar_completado(self):
        with self._lock:
            self._completados += 1

    def tamaño(self):
        with self._lock:
            return len(self._cola)

def demostrar_worker_list(grafo):
    """Demuestra como la Worker List distribuye el trabajo."""
    lista = WorkerList()
    resultados = []
    lock_resultados = threading.Lock()

    # Inicializar la lista con los subproblemas raiz
    nodos = set(grafo.keys())
    P = nodos.copy()
    X = set()
    for v in sorted(nodos):
        vecinos_v = grafo[v]
        lista.agregar((frozenset({v}), P & vecinos_v, X & vecinos_v))
        P = P - {v}
        X = X | {v}

    print(f"  Worker List inicializada con {lista.tamaño()} tareas\n")

    trabajos_por_hilo = defaultdict(int)

    def worker(id_hilo):
        while True:
            tarea = lista.tomar()
            if tarea is None:
                break
            R, P_t, X_t = tarea
            trabajos_por_hilo[id_hilo] += 1

            # Resolver el subproblema localmente
            def bk_local(R, P, X):
                if not P and not X:
                    with lock_resultados:
                        resultados.append(frozenset(R))
                    return
                pivote = seleccionar_pivote(grafo, P, X)
                for v in list(P - grafo[pivote]):
                    vecinos_v = grafo[v]
                    bk_local(R | {v}, P & vecinos_v, X & vecinos_v)
                    P = P - {v}; X = X | {v}

            bk_local(R, P_t, X_t)
            lista.marcar_completado()

    NUM_HILOS = 3
    hilos = [threading.Thread(target=worker, args=(i,)) for i in range(NUM_HILOS)]
    for h in hilos: h.start()
    for h in hilos: h.join()

    print(f"  Trabajo distribuido entre {NUM_HILOS} hilos:")
    for hilo_id, trabajos in sorted(trabajos_por_hilo.items()):
        barra = "█" * trabajos
        print(f"    Hilo {hilo_id}: {trabajos} tareas  {barra}")

    print(f"\n  Total cliques encontrados: {len(set(resultados))}")

demostrar_worker_list(G)

pausa()


subtitulo("6.2 Partial Induced Subgraphs — Reducir Memoria")

print("""
PROBLEMA: Uso de memoria

  Cada nodo del arbol de busqueda necesita almacenar (R, P, X).
  En grafos reales con 100,000 nodos y millones de aristas:
    → Almacenar P completo en cada nivel = GIGABYTES de memoria
    → La GPU tipica tiene 16-80 GB de memoria global
    → Se agota rapidamente con BFS

SOLUCION: Partial Induced Subgraph

  En vez de almacenar P como lista de todos los vertices candidatos,
  almacenamos solo el SUBGRAFO INDUCIDO por P.

  ¿Qué es un subgrafo inducido?
    El subgrafo G[P] = solo los vertices de P y las aristas ENTRE ellos.

  ¿Por que usa menos memoria?
    En niveles profundos del arbol, P se vuelve muy pequeño.
    El subgrafo inducido refleja directamente esta reduccion.
    No necesitamos hacer intersecciones con el grafo original completo.
""")

def subgrafo_inducido(grafo_original, vertices):
    """
    Construye el subgrafo inducido por el conjunto de vertices.
    Solo incluye aristas entre vertices del conjunto.
    """
    sub = defaultdict(set)
    for v in vertices:
        for u in grafo_original[v]:
            if u in vertices:
                sub[v].add(u)
    return sub

# Demostracion
P_ejemplo = {1, 2, 3}
sub = subgrafo_inducido(G, P_ejemplo)

print(f"\n  Grafo original: {sum(len(v) for v in G.values())//2} aristas totales")
print(f"  Subgrafo inducido por P={sorted(P_ejemplo)}:")
for nodo in sorted(sub):
    print(f"    Nodo {nodo} → vecinos en P: {sorted(sub[nodo])}")
aristas_sub = sum(len(v) for v in sub.values()) // 2
print(f"  Aristas en el subgrafo: {aristas_sub} (vs {sum(len(v) for v in G.values())//2} originales)")
print("""
  Ahorro de memoria proporcional a la reduccion de P.
  En niveles profundos el ahorro puede ser del 99%.
""")

pausa()


subtitulo("6.3 Compressed Vertex Sets — Representacion Compacta de X")

print("""
PROBLEMA con X (conjunto de vertices excluidos):
  X puede crecer mucho a medida que avanzamos en el arbol.
  Almacenarlo como lista de enteros ocupa mucho espacio.

SOLUCION: Representacion con BITSET (conjunto de bits)

  Idea: usar un entero de N bits donde el bit i = 1 si el vertice i esta en X.

  Ejemplo con N=8 vertices:
    X = {1, 3, 5}
    Representacion: 00101010  (bit 1, 3, 5 activos)
    En un entero Python: 0b00101010 = 42

  Operaciones con bitsets son MUY rapidas en GPU:
    Union:        X1 | X2   (OR bit a bit)
    Interseccion: X1 & X2   (AND bit a bit)
    Pertenencia:  X & (1<<v) != 0
""")

def vertices_a_bitset(vertices, n_total):
    """Convierte un conjunto de vertices a representacion bitset."""
    bits = 0
    for v in vertices:
        bits |= (1 << v)
    return bits

def bitset_a_vertices(bits):
    """Convierte un bitset a conjunto de vertices."""
    vertices = set()
    i = 0
    while bits:
        if bits & 1:
            vertices.add(i)
        bits >>= 1
        i += 1
    return vertices

def interseccion_bitset(b1, b2):
    return b1 & b2

def union_bitset(b1, b2):
    return b1 | b2

# Demostracion
N = len(G)
X1 = {1, 3, 5}
X2 = {3, 5, 7} if 7 in G else {3, 5}

b1 = vertices_a_bitset(X1, N)
b2 = vertices_a_bitset(X2, N)

print(f"\n  X1 = {sorted(X1)}  →  bitset: {bin(b1)}")
print(f"  X2 = {sorted(X2)}  →  bitset: {bin(b2)}")
print(f"  X1 ∩ X2 = {sorted(bitset_a_vertices(interseccion_bitset(b1, b2)))}  →  bitset: {bin(interseccion_bitset(b1, b2))}")
print(f"  X1 ∪ X2 = {sorted(bitset_a_vertices(union_bitset(b1, b2)))}   →  bitset: {bin(union_bitset(b1, b2))}")

print(f"""
  Comparacion de espacio:
    Lista de enteros: {N} vertices × 4 bytes = {N*4} bytes por conjunto
    Bitset:           {N} bits = {N//8} bytes  (ahorro de {(1 - (N//8)/(N*4))*100:.0f}%)

  Con grafos de 100,000 vertices:
    Lista: 400,000 bytes por conjunto
    Bitset:  12,500 bytes por conjunto  (32x mas compacto)
""")

pausa()


# =============================================================================
# MODULO 7: IMPLEMENTACION COMPLETA Y BENCHMARK
# =============================================================================

titulo("MODULO 7 — IMPLEMENTACION COMPLETA Y COMPARACION")

subtitulo("7.1 Version final optimizada de Bron-Kerbosch")

def bron_kerbosch_completo(grafo, R=None, P=None, X=None):
    """
    Implementacion completa de Bron-Kerbosch con pivote.
    Retorna lista de todos los cliques maximales.
    """
    if R is None: R = frozenset()
    if P is None: P = set(grafo.keys())
    if X is None: X = set()

    if not P and not X:
        return [frozenset(R)]

    resultado = []
    pivote = seleccionar_pivote(grafo, P, X)
    for v in list(P - grafo[pivote]):
        vecinos_v = grafo[v]
        resultado += bron_kerbosch_completo(
            grafo, R | {v}, P & vecinos_v, X & vecinos_v
        )
        P = P - {v}
        X = X | {v}
    return resultado

subtitulo("7.2 Benchmark: basico vs con pivote en grafos aleatorios")

def grafo_aleatorio(n, densidad=0.4, semilla=42):
    """Genera un grafo aleatorio con n vertices y densidad dada."""
    random.seed(semilla)
    aristas = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < densidad:
                aristas.append((i, j))
    return crear_grafo(aristas)

def bron_kerbosch_sin_pivote(grafo, R=None, P=None, X=None):
    """Version sin pivote (mas lenta)."""
    if R is None: R = frozenset()
    if P is None: P = set(grafo.keys())
    if X is None: X = set()

    if not P and not X:
        return [frozenset(R)]

    resultado = []
    for v in list(P):
        vecinos_v = grafo[v]
        resultado += bron_kerbosch_sin_pivote(
            grafo, R | {v}, P & vecinos_v, X & vecinos_v
        )
        P = P - {v}
        X = X | {v}
    return resultado

print("Comparando rendimiento en grafos de distinto tamaño:\n")
print(f"  {'N nodos':>8}  {'Sin pivote':>12}  {'Con pivote':>12}  {'Speedup':>8}")
print(f"  {'-'*8}  {'-'*12}  {'-'*12}  {'-'*8}")

for n in [8, 10, 12, 15]:
    G_rand = grafo_aleatorio(n)

    t0 = time.perf_counter()
    r1 = bron_kerbosch_sin_pivote(G_rand)
    t1 = time.perf_counter()
    tiempo_sin = (t1 - t0) * 1000

    t0 = time.perf_counter()
    r2 = bron_kerbosch_completo(G_rand)
    t1 = time.perf_counter()
    tiempo_con = (t1 - t0) * 1000

    speedup = tiempo_sin / tiempo_con if tiempo_con > 0 else float('inf')
    cliques = len(r1)

    print(f"  {n:>8}  {tiempo_sin:>10.2f}ms  {tiempo_con:>10.2f}ms  {speedup:>6.1f}x  ({cliques} cliques)")

pausa()


# =============================================================================
# MODULO 8: RESULTADOS DEL PAPER Y CONTEXTO
# =============================================================================

titulo("MODULO 8 — RESULTADOS Y EVALUACION DEL PAPER")

print("""
El paper reporta los siguientes resultados experimentales:

┌─────────────────────────────────────────────────────────────┐
│  RESULTADO PRINCIPAL:                                       │
│                                                             │
│  GPU unica  vs  CPU paralela (estado del arte):            │
│    Speedup promedio (media geometrica): 4.9x               │
│    Speedup maximo:                     16.7x               │
│                                                             │
│  Escalabilidad multi-GPU: lineal (casi perfecta)           │
└─────────────────────────────────────────────────────────────┘

¿Que es la media geometrica y por que usarla?
  La media geometrica es mejor que la media aritmetica
  para comparar ratios (speedups) porque no se distorsiona
  con valores extremos.

  Media geometrica de [2, 4, 8, 16] = (2 × 4 × 8 × 16)^(1/4)
                                     = 1024^0.25 ≈ 5.66

  Media aritmetica  de [2, 4, 8, 16] = (2+4+8+16)/4 = 7.5
  (sobreestima el rendimiento tipico)
""")

import math

speedups_ejemplo = [2.1, 3.4, 4.9, 6.2, 8.8, 16.7, 1.8, 4.1]

media_geo = math.exp(sum(math.log(s) for s in speedups_ejemplo) / len(speedups_ejemplo))
media_ari = sum(speedups_ejemplo) / len(speedups_ejemplo)

print(f"  Speedups de ejemplo: {speedups_ejemplo}")
print(f"  Media aritmetica:  {media_ari:.2f}x  ← sobreestima casos tipicos")
print(f"  Media geometrica:  {media_geo:.2f}x  ← mejor representa el comportamiento promedio")

print("""

Baseline del paper:
  Comparado contra: mejor implementacion CPU paralela conocida (MCE-BF/MCE-Pivoting)
  Hardware CPU: servidor multi-nucleo de ultima generacion
  Hardware GPU: NVIDIA GPU de gama alta

Grafos evaluados:
  Grafos reales de distinto dominio:
    - Redes sociales (Facebook, Twitter subgrafos)
    - Grafos de colaboracion cientifica
    - Redes de proteinas
    - Grafos de carretera/transporte
""")

pausa()


# =============================================================================
# MODULO 9: PREGUNTAS DE PRACTICA — EXAMEN
# =============================================================================

titulo("MODULO 9 — PREGUNTAS DE PRACTICA TIPO EXAMEN")

print("""
A continuacion se presentan 15 preguntas del estilo del examen.
Intenta responderlas antes de ver la respuesta.
""")

PREGUNTAS = [
    {
        "nivel": "BASICO",
        "pregunta": "¿Cuál es la diferencia entre un clique MÁXIMO y un clique MAXIMAL?",
        "respuesta": """
  Clique MAXIMAL: un clique al que NO se puede agregar ningún vértice más
                  (está 'atrapado', no hay vecino común externo).
  Clique MÁXIMO:  el clique de mayor tamaño en TODO el grafo.

  Relación: Todo clique máximo ES maximal, pero NO todo maximal es máximo.

  Ejemplo: Grafo con {A-B, B-C, A-C, C-D}
    {A,B,C} es MAXIMAL y MÁXIMO (tamaño 3)
    {C,D}   es MAXIMAL pero NO MÁXIMO (tamaño 2)
"""
    },
    {
        "nivel": "BASICO",
        "pregunta": "¿Qué significa MCE y cuál es su objetivo?",
        "respuesta": """
  MCE = Maximal Clique Enumeration (Enumeración de Cliques Maximales).
  Objetivo: encontrar TODOS los cliques maximales de un grafo.
  No uno, no el más grande: TODOS sin excepción.
  Es un problema NP-Hard porque el número de cliques puede ser exponencial.
"""
    },
    {
        "nivel": "BASICO",
        "pregunta": "Define los tres conjuntos R, P, X del algoritmo Bron-Kerbosch.",
        "respuesta": """
  R (Result/Resultado): vértices que ya están en el clique actual.
  P (Possible/Posibles): vértices que PUEDO agregar a R
                         (son vecinos de todos los vértices en R).
  X (Excluded/Excluidos): vértices ya procesados en ramas anteriores.

  Condición de éxito: P = ∅ y X = ∅ → R es un clique maximal (reportarlo).
  Condición de poda:  P = ∅ pero X ≠ ∅ → R no es maximal (ignorarlo).
"""
    },
    {
        "nivel": "INTERMEDIO",
        "pregunta": "¿Qué es el PIVOTE en Bron-Kerbosch y por qué reduce el trabajo?",
        "respuesta": """
  El pivote u es un vértice elegido de P ∪ X con el MÁXIMO número
  de vecinos en P. En vez de iterar sobre todos los vértices de P,
  solo iteramos sobre P \\ N(u)  (los que NO son vecinos del pivote).

  ¿Por qué funciona?
  Todo clique maximal debe contener al menos un vértice que NO sea
  vecino del pivote. Si todos fueran vecinos del pivote, podríamos
  agregar el pivote → contradicción con maximalidad.

  Efecto: reduce drásticamente el número de ramas recursivas.
"""
    },
    {
        "nivel": "INTERMEDIO",
        "pregunta": "¿Por qué el enfoque BFS en GPU tiene problemas de escalabilidad para MCE?",
        "respuesta": """
  En BFS, todos los nodos de un nivel del árbol de búsqueda se procesan
  SIMULTÁNEAMENTE. En niveles profundos, el árbol 'explota': puede haber
  millones de nodos activos al mismo tiempo. Cada nodo necesita almacenar
  su estado (R, P, X) en memoria GPU. Esto agota rápidamente la memoria
  de la GPU (típicamente 16-80 GB). A mayor densidad del grafo, peor.
"""
    },
    {
        "nivel": "INTERMEDIO",
        "pregunta": "¿Cómo resuelve el paper el problema de memoria que tiene el BFS?",
        "respuesta": """
  El paper propone usar DFS (Depth-First Search) en lugar de BFS.
  Con DFS, cada hilo GPU explora UN subárbol completo de forma independiente.
  Solo se mantiene activo UN camino del árbol a la vez por hilo.
  El uso de memoria es proporcional a la PROFUNDIDAD del árbol (no al ancho).
  Adicionalmente, usan partial induced subgraphs y compressed vertex sets
  para reducir aún más la memoria por nodo.
"""
    },
    {
        "nivel": "INTERMEDIO",
        "pregunta": "¿Qué es load imbalance en el contexto de MCE en GPU?",
        "respuesta": """
  Load imbalance = desbalance de carga entre los hilos GPU.

  Causa: distintos subárboles tienen tamaños muy diferentes.
  Algunos subárboles contienen miles de cliques (carga pesada).
  Otros contienen 0 cliques (carga trivial).

  Si GPU-hilo-0 toma el subárbol pesado (tarda 10 minutos)
  y GPU-hilo-1 toma el trivial (termina en 1 segundo),
  el hilo-1 queda inactivo mientras el hilo-0 trabaja.
  → Desperdicio masivo de recursos de la GPU.
"""
    },
    {
        "nivel": "AVANZADO",
        "pregunta": "Explica la Worker List propuesta en el paper. ¿Qué problema resuelve y cómo?",
        "respuesta": """
  La Worker List es una cola compartida de subproblemas pendientes.

  Problema que resuelve: load imbalance (desbalance de carga).

  Funcionamiento:
    1. Inicialmente se llena con los subproblemas raíz del árbol.
    2. Cada hilo GPU toma un subproblema de la lista y lo resuelve.
    3. Cuando un hilo TERMINA su tarea, toma otra de la lista.
    4. Si un subproblema es muy grande, el hilo puede dividirlo
       y poner los subproblemas menores en la lista.

  Resultado: todos los hilos permanecen activos → mejor utilización de GPU.
  Esto es un tipo de 'work stealing' dinámico.
"""
    },
    {
        "nivel": "AVANZADO",
        "pregunta": "¿Qué son los Partial Induced Subgraphs y por qué reducen el consumo de memoria?",
        "respuesta": """
  En vez de almacenar P como lista completa de vértices candidatos,
  se almacena el SUBGRAFO INDUCIDO por P: G[P].

  G[P] = solo los vértices de P y las aristas ENTRE vértices de P.

  Beneficio de memoria:
    En niveles profundos del árbol, P se vuelve muy pequeño
    (ya que P ⊆ N(v1) ∩ N(v2) ∩ ... para los vértices ya en R).
    El subgrafo inducido tiene pocas aristas → mucho menos espacio.
    No necesitamos guardar referencias al grafo original completo.

  La reducción de memoria puede ser del 90-99% en niveles profundos.
"""
    },
    {
        "nivel": "AVANZADO",
        "pregunta": "¿Qué es la representación comprimida del conjunto X y cuál es su ventaja?",
        "respuesta": """
  El conjunto X se representa como un BITSET (mapa de bits).

  Para un grafo de N vértices, se usa un entero de N bits donde
  el bit i = 1 si el vértice i ∈ X.

  Ventajas:
    1. Espacio: N bits en vez de N×4 bytes → 32x más compacto.
    2. Velocidad: las operaciones de conjunto (intersección, unión)
       se convierten en operaciones a nivel de bits (AND, OR)
       que la GPU ejecuta en UN solo ciclo de reloj.

  Con 1000 vértices:
    Lista de enteros: 4,000 bytes por conjunto X
    Bitset:             125 bytes por conjunto X (32x reducción)
"""
    },
    {
        "nivel": "AVANZADO",
        "pregunta": "¿Cuáles son las dos métricas de rendimiento reportadas en el paper y qué significan?",
        "respuesta": """
  1. Speedup de media geométrica: 4.9x
     La GPU es en PROMEDIO 4.9 veces más rápida que la mejor CPU paralela.
     Se usa media geométrica (no aritmética) porque es más adecuada
     para comparar ratios y no se distorsiona por valores extremos.

  2. Speedup máximo: 16.7x
     En el mejor caso (grafo con características favorables para GPU),
     la GPU es hasta 16.7 veces más rápida.

  Baseline de comparación: la mejor implementación CPU paralela conocida
  (estado del arte) ejecutando en un servidor multi-núcleo de alto rendimiento.
"""
    },
    {
        "nivel": "RAZONAMIENTO",
        "pregunta": "En el grafo {A-B, B-C, A-C, C-D}, lista TODOS los cliques maximales.",
        "respuesta": """
  Vértices: A, B, C, D
  Aristas: A-B, B-C, A-C, C-D

  Paso 1 — identificar todos los cliques:
    {A,B,C}: A-B ✓, A-C ✓, B-C ✓ → ES clique
    {C,D}:   C-D ✓             → ES clique
    {A,B}:   A-B ✓             → ES clique, ¿pero es maximal?

  Paso 2 — verificar maximalidad:
    {A,B,C}: ¿puedo agregar D? D necesita estar conectado a A,B,C.
              D-A NO existe → NO se puede agregar D. ✓ MAXIMAL
    {C,D}:   ¿puedo agregar A? A-D NO existe → NO. ✓ MAXIMAL
              ¿puedo agregar B? B-D NO existe → NO. ✓ MAXIMAL
    {A,B}:   ¿puedo agregar C? C-A ✓ y C-B ✓ → SÍ se puede → NO maximal

  RESPUESTA: Los cliques maximales son {A,B,C} y {C,D}.
"""
    },
    {
        "nivel": "RAZONAMIENTO",
        "pregunta": "¿Por qué si P=∅ pero X≠∅, el conjunto R NO es un clique maximal?",
        "respuesta": """
  Si X ≠ ∅, existe al menos un vértice u ∈ X tal que u es vecino
  de TODOS los vértices en R (de lo contrario, u no estaría en X).

  Esto significa que u PODRÍA ser agregado a R para formar un clique
  mayor. Pero entonces R sería un subconjunto de un clique más grande,
  que ya fue explorado en una rama anterior del árbol.

  Por tanto, R no es maximal: existe un clique que lo contiene.

  (El invariante del algoritmo garantiza que si u ∈ X, entonces
  el clique R ∪ {u} ya fue reportado como subclique de otro clique
  maximal en una rama anterior.)
"""
    },
    {
        "nivel": "RAZONAMIENTO",
        "pregunta": "¿Por qué el paper elige DFS en lugar de BFS para paralelizar en GPU?",
        "respuesta": """
  Razón 1 — MEMORIA:
    BFS requiere mantener TODOS los nodos de un nivel en memoria simultáneamente.
    En grafos densos, esto crece exponencialmente y agota la memoria GPU.
    DFS solo mantiene un camino activo por hilo → memoria controlada.

  Razón 2 — INDEPENDENCIA:
    Con DFS, los subárboles son COMPLETAMENTE INDEPENDIENTES entre sí.
    Un hilo puede explorar su subárbol sin comunicarse con otros hilos.
    Esto es ideal para GPU donde la comunicación entre hilos es costosa.

  Razón 3 — TRABAJO DINÁMICO:
    DFS permite dividir el árbol en subproblemas independientes
    que pueden redistribuirse dinámicamente (Worker List).
    Con BFS, todos los nodos del nivel N dependen del nivel N-1.
"""
    },
    {
        "nivel": "RAZONAMIENTO",
        "pregunta": "¿Qué es warp divergence y cómo podría afectar la implementación GPU de Bron-Kerbosch?",
        "respuesta": """
  Warp divergence: cuando hilos del mismo warp (grupo de 32) toman
  ramas diferentes en un if/else. Los que no cumplen la condición
  quedan INACTIVOS hasta que los otros terminen → ejecución serializada.

  En Bron-Kerbosch, cada vértice tiene diferente número de vecinos,
  por lo que P tiene diferente tamaño en cada hilo. Esto puede causar:
    - Hilos con P vacío (terminan pronto) esperan a hilos con P grande.
    - Condicionales distintos según si el vértice está en P o no.

  El paper mitiga esto con la Worker List que redistribuye el trabajo,
  reduciendo la divergencia al mantener cargas más homogéneas por warp.
"""
    },
]

for i, q in enumerate(PREGUNTAS, 1):
    print(f"\n{'='*60}")
    print(f"  PREGUNTA {i:02d} [{q['nivel']}]")
    print(f"{'='*60}")
    print(f"\n  {q['pregunta']}\n")
    input("  [ENTER para ver la respuesta]\n")
    print("  RESPUESTA:")
    print(q['respuesta'])


# =============================================================================
# MODULO 10: RESUMEN EJECUTIVO
# =============================================================================

titulo("MODULO 10 — RESUMEN EJECUTIVO (repasa esto antes del examen)")

print("""
┌─────────────────────────────────────────────────────────────────┐
│                    7 PUNTOS CLAVE DEL PAPER                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CLIQUE vs MAXIMAL vs MÁXIMO                                 │
│     Clique = todos conectados. Maximal = no extensible.         │
│     Máximo = el más grande. MCE = encontrar TODOS los maximales.│
│                                                                 │
│  2. BRON-KERBOSCH: R, P, X                                      │
│     R = actual. P = candidatos. X = excluidos.                  │
│     Parar cuando P=∅ y X=∅ → reportar R.                        │
│                                                                 │
│  3. PIVOTE                                                      │
│     u ∈ P∪X con más vecinos en P.                               │
│     Iterar solo sobre P \ N(u). Reduce ramas innecesarias.      │
│                                                                 │
│  4. DFS > BFS en GPU                                            │
│     BFS explota en memoria en niveles profundos.                │
│     DFS: memoria controlada, subárboles independientes.         │
│                                                                 │
│  5. WORKER LIST                                                 │
│     Cola de subproblemas compartida.                            │
│     Resuelve load imbalance: hilos toman trabajo dinámicamente. │
│                                                                 │
│  6. OPTIMIZACIONES DE MEMORIA                                   │
│     Partial induced subgraphs: P como subgrafo, no lista.       │
│     Compressed X: bitset en vez de lista de enteros.            │
│                                                                 │
│  7. RESULTADOS                                                  │
│     4.9x speedup promedio (media geométrica) vs CPU paralela.   │
│     Hasta 16.7x en el mejor caso. Escalable a multi-GPU.        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Paper: Almasri et al., "Parallelizing Maximal Clique Enumeration on GPUs"
       PACT 2023 (págs. 162-175) — arXiv:2212.01473v3

¡Mucho éxito en el examen!
""")

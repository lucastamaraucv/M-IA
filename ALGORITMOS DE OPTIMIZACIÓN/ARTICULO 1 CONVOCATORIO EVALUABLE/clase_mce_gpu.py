# -*- coding: utf-8 -*-
r"""
================================================================================
 CLASE INTERACTIVA: "Parallelizing Maximal Clique Enumeration on GPUs"
 (Almasri, Hajj, Nagi, Xiong, Hwu — 2022, arXiv:2212.01473)
================================================================================

Este archivo es una "clase en código": cada sección implementa, con fines
PURAMENTE DIDÁCTICOS (no productivos), uno de los conceptos centrales del
paper. Se ejecuta con Python estándar, sin GPU ni dependencias externas:

    python clase_mce_gpu.py

Secciones (en el mismo orden del paper):

  1. Bron-Kerbosch básico            -> el árbol de búsqueda R/P/X
  2. Bron-Kerbosch con pivoteo       -> poda de ramas redundantes
  3. Ordenamiento por degeneración   -> acotar el tamaño de P
  4. Subárboles independientes       -> paralelismo de 1er y 2do nivel
                                        (Algoritmos 3 y 4 del paper)
  5. Worker list                     -> balanceo de carga dinámico
  6. X compacto (XP + XX)            -> comprimir memoria explotando
                                        propiedades monótonas (Fig. 2)
  7. Conclusiones en código          -> qué principio enseña cada sección

GRAFO DE EJEMPLO (el mismo espíritu del ejemplo del paper):

        E ---- F
         \    /
          \  /
           A
          /|\
         / | \
        B--+--D          Cliques maximales:
         \ | /              {A, B, C, D}   (un K4: todos conectados entre sí)
          \|/               {A, E, F}      (un triángulo)
           C

IMPORTANTE: todo el "paralelismo" de este archivo usa hilos de Python como
ANALOGÍA CONCEPTUAL de los bloques de hilos (thread blocks) de una GPU.
No es CUDA real: en CPython el GIL impide paralelismo real de CPU, pero la
ESTRUCTURA del reparto de trabajo es la misma idea que en la GPU, que es lo
que queremos entender.
================================================================================
"""

import sys
import threading
import time
from collections import deque

# La consola de Windows a veces usa la codificación cp1252, que no conoce
# símbolos como '∩'. Forzamos UTF-8 para que los prints no revienten.
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ==============================================================================
# EL GRAFO DE EJEMPLO
# ==============================================================================
# Lo representamos como un diccionario: vértice -> conjunto de vecinos.
# Es la "lista de adyacencia" clásica. En la GPU real el paper usa formato
# CSR (Compressed Sparse Row), que es la misma idea pero en arreglos planos
# para que los hilos accedan a memoria de forma contigua (coalesced).

GRAFO = {
    'A': {'B', 'C', 'D', 'E', 'F'},
    'B': {'A', 'C', 'D'},
    'C': {'A', 'B', 'D'},
    'D': {'A', 'B', 'C'},
    'E': {'A', 'F'},
    'F': {'A', 'E'},
}


def fmt(conjunto):
    """Formatea un conjunto de vértices de forma ordenada y legible: {A, B, C}"""
    return '{' + ', '.join(sorted(conjunto)) + '}'


def titulo(texto):
    """Imprime un separador de sección grande, para leer la salida como clase."""
    print()
    print('=' * 78)
    print(texto)
    print('=' * 78)


# ==============================================================================
# SECCIÓN 1: BRON-KERBOSCH BÁSICO
# ==============================================================================
# ¿POR QUÉ existe este algoritmo?
#
# Enumerar cliques maximales por fuerza bruta (probar todos los subconjuntos
# de vértices) costaría 2^n. Bron-Kerbosch organiza la búsqueda como un ÁRBOL
# donde cada nodo mantiene TRES conjuntos:
#
#   R (Result)   : el clique parcial que estamos construyendo. Todos los
#                  vértices de R son vecinos entre sí (invariante clave).
#   P (Possible) : vértices que son vecinos de TODOS los de R, y que por lo
#                  tanto PUEDEN extender el clique. Son el "futuro".
#   X (eXcluded) : vértices que también son vecinos de todos los de R, pero
#                  que YA fueron explorados en otra rama. Son el "pasado".
#
# ¿POR QUÉ necesitamos X? Sin X reportaríamos cliques NO maximales o
# duplicados: si P está vacío pero X no, significa que R se puede extender
# con algún vértice de X (o sea, R no es maximal) y además ese clique más
# grande ya se encontró (o se encontrará) por otra rama. X es el mecanismo
# que garantiza "cada clique maximal se reporta EXACTAMENTE una vez".
#
# Regla de reporte:  R es clique maximal  <=>  P == vacío  Y  X == vacío.
#
# Regla de expansión: para cada v en P:
#     - bajamos con R' = R ∪ {v},  P' = P ∩ N(v),  X' = X ∩ N(v)
#       (intersectar con N(v) mantiene el invariante "vecinos de todo R")
#     - al volver, movemos v de P a X: "v ya fue explorado, si aparece en
#       otra rama es porque esa rama repetiría trabajo".
# ==============================================================================

def bron_kerbosch_basico(grafo, R, P, X, nivel=0, stats=None, verbose=True):
    """
    Versión original (sin pivote) que imprime el árbol de búsqueda completo.

    Cada llamada recursiva es un NODO del árbol de búsqueda. El paper
    paraleliza precisamente este árbol: distintas ramas son independientes
    entre sí, así que pueden ir a distintos bloques de la GPU.
    """
    if stats is not None:
        stats['nodos'] += 1  # contamos nodos del árbol para comparar después

    sangria = '    ' * nivel  # indentación proporcional al nivel de recursión
    if verbose:
        print(f"{sangria}[nivel {nivel}] R={fmt(R)}  P={fmt(P)}  X={fmt(X)}")

    # Caso base: no hay futuro (P vacío). Si tampoco hay pasado (X vacío),
    # R es maximal. Si X NO está vacío, R está contenido en un clique mayor
    # ya explorado -> esta rama muere sin reportar (poda por corrección).
    if not P and not X:
        if verbose:
            print(f"{sangria}    >>> CLIQUE MAXIMAL ENCONTRADO: {fmt(R)} <<<")
        if stats is not None:
            stats['cliques'].append(set(R))
        return

    if not P and verbose:
        print(f"{sangria}    (rama muerta: P vacío pero X={fmt(X)} no vacío "
              f"=> R no es maximal)")

    # Expansión: probamos CADA vértice de P como siguiente miembro del clique.
    # Iteramos sobre una copia porque modificamos P dentro del bucle.
    for v in sorted(P):          # sorted() solo para salida reproducible
        if v not in P:           # v pudo haber sido movido a X en una vuelta previa
            continue
        vecinos_v = grafo[v]
        bron_kerbosch_basico(
            grafo,
            R | {v},             # R' : agregamos v al clique parcial
            P & vecinos_v,       # P' : solo sobreviven los vecinos de v
            X & vecinos_v,       # X' : idem para los excluidos
            nivel + 1, stats, verbose,
        )
        # Al volver de explorar v: v pasa del "futuro" al "pasado".
        # ESTE movimiento es el que evita duplicados entre ramas hermanas.
        P = P - {v}
        X = X | {v}


def seccion_1():
    titulo("SECCIÓN 1: Bron-Kerbosch básico — el árbol de búsqueda R/P/X")
    print("""
Leyenda del árbol:
  - Cada línea es una llamada recursiva (un nodo del árbol de búsqueda).
  - R = clique parcial, P = candidatos posibles, X = ya explorados.
  - Un clique se reporta SOLO cuando P y X quedan vacíos a la vez.
Observa cómo el árbol repite trabajo: varias ramas terminan muriendo en
"P vacío pero X no vacío". Eso es lo que el pivoteo (Sección 2) va a podar.
""")
    stats = {'nodos': 0, 'cliques': []}
    bron_kerbosch_basico(GRAFO, set(), set(GRAFO), set(), stats=stats)
    print(f"\nRESUMEN: {stats['nodos']} nodos de árbol explorados, "
          f"{len(stats['cliques'])} cliques maximales: "
          f"{[fmt(c) for c in stats['cliques']]}")
    return stats['nodos']


# ==============================================================================
# SECCIÓN 2: BRON-KERBOSCH CON PIVOTEO
# ==============================================================================
# ¿POR QUÉ pivotear?
#
# Observación clave (Tomita et al.): si u es un vértice de P ∪ X, entonces
# TODO clique maximal debe contener a u O a algún NO-vecino de u.
# (Si un clique contuviera solo vecinos de u y no a u, podríamos añadir u
#  y no sería maximal.)
#
# Consecuencia: en cada nodo del árbol NO hace falta ramificar por todos los
# v de P; basta ramificar por  P \ N(u)  (los no-vecinos de u, más u mismo
# si está en P). Las ramas por vecinos de u son REDUNDANTES: cualquier
# clique que encontrarían se encuentra también pasando por u.
#
# ¿Qué pivote elegir? El que tenga MÁS vecinos dentro de P, porque así
# P \ N(u) queda lo más pequeño posible => máxima poda. Esta es la heurística
# del paper (y la clásica de Tomita). En la GPU, calcular |P ∩ N(u)| para
# todos los candidatos u es un trabajo perfectamente paralelo: cada hilo del
# bloque cuenta intersecciones de una parte -> por eso el pivoteo "cabe" bien
# en el modelo GPU aunque parezca un paso secuencial.
# ==============================================================================

def bron_kerbosch_pivote(grafo, R, P, X, nivel=0, stats=None, verbose=True):
    """Variante con pivote. Imprime qué ramas se EXPLORAN y cuáles se PODAN."""
    if stats is not None:
        stats['nodos'] += 1

    sangria = '    ' * nivel
    if verbose:
        print(f"{sangria}[nivel {nivel}] R={fmt(R)}  P={fmt(P)}  X={fmt(X)}")

    if not P and not X:
        if verbose:
            print(f"{sangria}    >>> CLIQUE MAXIMAL: {fmt(R)} <<<")
        if stats is not None:
            stats['cliques'].append(set(R))
        return
    if not P:
        return

    # --- Selección de pivote -------------------------------------------------
    # Candidatos: P ∪ X. Elegimos el u que maximiza |P ∩ N(u)|.
    # ¿Por qué también mirar en X? Porque un vértice ya excluido puede seguir
    # siendo el que más candidatos "cubre", y cubrir candidatos = podar ramas.
    pivote = max(sorted(P | X), key=lambda u: len(P & grafo[u]))
    ramas = P - grafo[pivote]        # SOLO ramificamos por los no-vecinos del pivote
    podadas = P & grafo[pivote]      # estas ramas se AHORRAN por completo

    if stats is not None:
        stats['podadas'] += len(podadas)
    if verbose:
        print(f"{sangria}    pivote u = {pivote}  "
              f"(cubre {len(podadas)} candidatos de P)")
        print(f"{sangria}    ramas a explorar: {fmt(ramas)}   "
              f"ramas PODADAS: {fmt(podadas)}")

    for v in sorted(ramas):
        if v not in P:
            continue
        vecinos_v = grafo[v]
        bron_kerbosch_pivote(grafo, R | {v}, P & vecinos_v, X & vecinos_v,
                             nivel + 1, stats, verbose)
        P = P - {v}
        X = X | {v}


def seccion_2(nodos_sin_pivote):
    titulo("SECCIÓN 2: Bron-Kerbosch con pivoteo — podar ramas redundantes")
    print("""
Regla del pivote: todo clique maximal contiene al pivote u O a un no-vecino
de u. Por lo tanto solo ramificamos por P \\ N(u); las ramas por vecinos de u
son redundantes y se podan enteras (con TODO su subárbol).
""")
    stats = {'nodos': 0, 'cliques': [], 'podadas': 0}
    bron_kerbosch_pivote(GRAFO, set(), set(GRAFO), set(), stats=stats)
    print(f"""
COMPARACIÓN (mismo grafo, mismos cliques encontrados):
  Sin pivote : {nodos_sin_pivote} nodos de árbol explorados
  Con pivote : {stats['nodos']} nodos de árbol explorados
  Ramas podadas directamente en los nodos: {stats['podadas']}
  (cada rama podada se lleva consigo TODO su subárbol; en grafos reales
   la diferencia es de órdenes de magnitud, no de unos pocos nodos)
""")
    return stats['nodos']


# ==============================================================================
# SECCIÓN 3: ORDENAMIENTO POR DEGENERACIÓN (degeneracy ordering)
# ==============================================================================
# ¿QUÉ es la degeneración d de un grafo?
#
# Es el menor número d tal que TODO subgrafo tiene algún vértice con grado
# <= d. Intuición: mide qué tan "denso en el peor rincón" es el grafo. Las
# redes reales (sociales, web) tienen degeneración pequeña aunque tengan
# millones de aristas.
#
# ¿CÓMO se calcula? Con "peeling" (pelado): repetidamente quitar el vértice
# de grado mínimo. El orden en que se quitan es el DEGENERACY ORDERING, y la
# degeneración es el mayor grado observado en el momento de quitar.
#
# ¿POR QUÉ le sirve a Bron-Kerbosch (Eppstein et al.)?
#
# En el primer nivel, en vez de un P gigante con todos los vértices,
# procesamos los vértices EN ese orden v1, v2, ..., vn y para cada vi:
#     P = vecinos de vi POSTERIORES en el orden   (futuro)
#     X = vecinos de vi ANTERIORES en el orden    (pasado)
# Por definición del pelado, ¡los vecinos posteriores son a lo más d!
# => TODO subárbol de primer nivel arranca con |P| <= d.
#
# Esto es ORO para la GPU por dos razones del paper:
#   1) Tiempo: acota la profundidad/anchura de cada subárbol (menos trabajo
#      y subárboles más parecidos entre sí => menos desbalance).
#   2) MEMORIA: cada bloque debe reservar memoria para sus conjuntos POR
#      NIVEL antes de lanzar el kernel; con |P| <= d esa reserva pasa de
#      O(n por nivel) a O(d por nivel). Sin esta cota, grafos grandes ni
#      siquiera cabrían en la memoria de la GPU.
# ==============================================================================

def orden_degeneracion(grafo, verbose=True):
    """
    Calcula el degeneracy ordering por "peeling": quitar siempre el vértice
    de grado mínimo del grafo restante. Devuelve (orden, degeneración).
    """
    grados = {v: len(vecinos) for v, vecinos in grafo.items()}
    restantes = set(grafo)
    orden = []
    degeneracion = 0

    while restantes:
        # vértice de grado mínimo entre los que quedan
        v = min(sorted(restantes), key=lambda u: grados[u])
        degeneracion = max(degeneracion, grados[v])
        if verbose:
            print(f"  pelamos {v} (grado actual {grados[v]}); "
                  f"quedan {fmt(restantes - {v})}")
        orden.append(v)
        restantes.remove(v)
        for w in grafo[v]:
            if w in restantes:
                grados[w] -= 1  # al quitar v, sus vecinos pierden un grado
    return orden, degeneracion


def seccion_3():
    titulo("SECCIÓN 3: Ordenamiento por degeneración — acotar el tamaño de P")
    print("Cálculo por 'peeling' (quitar siempre el vértice de grado mínimo):\n")
    orden, d = orden_degeneracion(GRAFO)
    posicion = {v: i for i, v in enumerate(orden)}
    print(f"\n  Orden de degeneración : {' -> '.join(orden)}")
    print(f"  Degeneración d = {d}  (máximo grado visto al momento de pelar)")

    print(f"""
Ahora corremos el PRIMER NIVEL siguiendo ese orden. Para cada vértice v:
  P = vecinos POSTERIORES a v en el orden (aún no procesados)
  X = vecinos ANTERIORES  a v en el orden (ya procesados por su propia rama)
La garantía: |P| <= d = {d} en TODOS los subárboles de primer nivel.
Compara con la versión ingenua, cuyo P inicial tiene |P| = {len(GRAFO)}.
""")
    max_P = 0
    for v in orden:
        P = {w for w in GRAFO[v] if posicion[w] > posicion[v]}
        X = {w for w in GRAFO[v] if posicion[w] < posicion[v]}
        max_P = max(max_P, len(P))
        print(f"  subárbol de {v}:  P={fmt(P)} (|P|={len(P)})  X={fmt(X)}")
        # Dentro de cada subárbol seguimos usando pivoteo (silencioso aquí;
        # la Sección 4 los ejecuta en "paralelo" y muestra sus cliques).
        stats = {'nodos': 0, 'cliques': [], 'podadas': 0}
        bron_kerbosch_pivote(GRAFO, {v}, P, X, stats=stats, verbose=False)
        for c in stats['cliques']:
            print(f"      -> clique maximal encontrado en este subárbol: {fmt(c)}")

    print(f"""
RESULTADO: el mayor P de primer nivel midió {max_P} <= d = {d}.
Memoria por nivel: pasa de O(n) = O({len(GRAFO)}) a O(d) = O({d}).
En un grafo real con n = 10^6 y d = 100, esa diferencia decide si el
problema CABE o NO CABE en la memoria de la GPU.
""")
    return orden, posicion, d


# ==============================================================================
# SECCIÓN 4: SUBÁRBOLES INDEPENDIENTES DE 1er Y 2do NIVEL
#            (Algoritmos 3 y 4 del paper)
# ==============================================================================
# La observación que habilita TODO el paper: una vez fijados (R, P, X), el
# subárbol que cuelga de ese nodo NO necesita comunicarse con ningún otro
# subárbol. Son tareas independientes => reparto natural entre bloques GPU.
#
# ALGORITMO 3 (primer nivel): un "bloque" por cada vértice v del orden de
#   degeneración. El bloque recibe (R={v}, P=vecinos posteriores,
#   X=vecinos anteriores) y explora SU subárbol completo, en serie dentro
#   del bloque pero en paralelo con los demás bloques.
#     + Ventaja : poca memoria (un contexto R/P/X por bloque).
#     - Problema: solo hay n subárboles y sus tamaños son MUY dispares
#                 (el subárbol de un hub es enorme, el de una hoja trivial).
#
# ALGORITMO 4 (segundo nivel): expandimos UN nivel más ANTES de repartir:
#   las tareas son pares (v, w) con w ∈ P(v). Muchas más tareas y más
#   pequeñas => mejor ocupación de la GPU y menos desbalance...
#     - a cambio de más memoria total (un contexto por cada par) y de
#       trabajo redundante al expandir ese nivel extra.
#
# Es el clásico trade-off granularidad fina (balance) vs gruesa (overhead).
#
# *** SIMULACIÓN CONCEPTUAL ***: usamos threading.Thread como analogía de un
# "thread block" de CUDA. En CPython el GIL serializa la ejecución, así que
# NO hay speedup real; lo que modelamos fielmente es el REPARTO del trabajo,
# que es el aporte del paper. Dentro de un bloque GPU real, además, los ~
# cientos de hilos del bloque cooperan para hacer las intersecciones
# P ∩ N(v) en paralelo (paralelismo de grano fino que aquí omitimos).
# ==============================================================================

def _expandir_segundo_nivel(grafo, v, P, X):
    """
    Genera las tareas de SEGUNDO nivel del subárbol de v: pares (v, w).

    Detalle sutil anti-duplicados: al expandir w1, w2, ... ∈ P(v) en orden,
    cada par hereda en X a los w anteriores (igual que hace el bucle interno
    de Bron-Kerbosch al mover v de P a X). Sin esto, dos tareas distintas
    reportarían el mismo clique. (El paper además pivotea en este nivel;
    aquí lo simplificamos para que se vea la estructura.)
    """
    tareas = []
    P_local, X_local = set(P), set(X)
    for w in sorted(P):
        vecinos_w = grafo[w]
        tareas.append({
            'R': {v, w},
            'P': P_local & vecinos_w,
            'X': X_local & vecinos_w,
        })
        P_local -= {w}
        X_local |= {w}
    return tareas


def _bloque_gpu(nombre, grafo, tarea, resultados, lock, contar_nodos=None):
    """
    Simula UN bloque de la GPU: recibe su contexto (R, P, X) y explora el
    subárbol completo con Bron-Kerbosch pivotado, sin hablar con nadie más.
    """
    stats = {'nodos': 0, 'cliques': [], 'podadas': 0}
    bron_kerbosch_pivote(grafo, tarea['R'], tarea['P'], tarea['X'],
                         stats=stats, verbose=False)
    with lock:  # el lock es solo para no entremezclar los prints
        print(f"  [{nombre}] recibió R={fmt(tarea['R'])} "
              f"P={fmt(tarea['P'])} X={fmt(tarea['X'])} "
              f"-> exploró {stats['nodos']} nodos, "
              f"cliques: {[fmt(c) for c in stats['cliques']] or 'ninguno'}")
        resultados.extend(stats['cliques'])
        if contar_nodos is not None:
            contar_nodos[nombre] = stats['nodos']


def seccion_4(orden, posicion):
    titulo("SECCIÓN 4: Subárboles independientes de 1er y 2do nivel "
           "(Algoritmos 3 y 4)")

    lock = threading.Lock()

    # ---------- ALGORITMO 3: un bloque por vértice (primer nivel) ----------
    print("\n--- Algoritmo 3: paralelismo de PRIMER nivel (1 bloque = 1 vértice) ---")
    print("Cada 'bloque' (hilo Python) explora el subárbol de su vértice:\n")
    tareas_n1 = []
    for v in orden:
        P = {w for w in GRAFO[v] if posicion[w] > posicion[v]}
        X = {w for w in GRAFO[v] if posicion[w] < posicion[v]}
        tareas_n1.append((v, {'R': {v}, 'P': P, 'X': X}))

    resultados, nodos_por_bloque = [], {}
    hilos = [threading.Thread(target=_bloque_gpu,
                              args=(f"bloque-{v}", GRAFO, t, resultados, lock,
                                    nodos_por_bloque))
             for v, t in tareas_n1]
    for h in hilos: h.start()
    for h in hilos: h.join()
    print(f"\n  Cliques totales (sin duplicados por construcción): "
          f"{[fmt(c) for c in resultados]}")
    print(f"  Nodos por bloque: { {k: v for k, v in sorted(nodos_por_bloque.items())} }")
    print("  ^ Fíjate en el DESBALANCE: unos bloques trabajan mucho más que "
          "otros.\n    Ese es el problema que motiva las Secciones 4b y 5.")

    # ---------- ALGORITMO 4: un bloque por par (segundo nivel) ----------
    print("\n--- Algoritmo 4: paralelismo de SEGUNDO nivel (1 bloque = 1 par v,w) ---")
    print("Expandimos un nivel más ANTES de repartir: tareas más chicas y "
          "numerosas.\n")
    tareas_n2 = []
    for v, t in tareas_n1:
        if not t['P'] and not t['X']:
            # caso borde: {v} ya es maximal por sí solo; sin este chequeo,
            # la descomposición por pares se lo saltaría.
            tareas_n2.append((f"{v}(solo)", {'R': {v}, 'P': set(), 'X': set()}))
            continue
        for tarea in _expandir_segundo_nivel(GRAFO, v, t['P'], t['X']):
            par = ''.join(sorted(tarea['R']))
            tareas_n2.append((par, tarea))

    resultados2, nodos_por_bloque2 = [], {}
    hilos = [threading.Thread(target=_bloque_gpu,
                              args=(f"bloque-{nombre}", GRAFO, t, resultados2,
                                    lock, nodos_por_bloque2))
             for nombre, t in tareas_n2]
    for h in hilos: h.start()
    for h in hilos: h.join()
    print(f"\n  Cliques totales: {[fmt(c) for c in resultados2]}")
    print(f"""
COMPARACIÓN de granularidad:
  1er nivel: {len(tareas_n1)} tareas, tamaños {sorted(nodos_por_bloque.values(), reverse=True)}
  2do nivel: {len(tareas_n2)} tareas, tamaños {sorted(nodos_por_bloque2.values(), reverse=True)}
Más tareas y más pequeñas => la GPU llena mejor sus SMs y el bloque más
cargado espera menos... a cambio de más memoria (un contexto por tarea).
El paper elige el nivel según memoria disponible; y para el desbalance que
QUEDA, usa el worker list de la Sección 5.
""")


# ==============================================================================
# SECCIÓN 5: BALANCEO DE CARGA CON "WORKER LIST"
# ==============================================================================
# Problema: aunque partamos en segundo nivel, los subárboles siguen teniendo
# tamaños imposibles de predecir (dependen de la estructura del grafo). Con
# asignación ESTÁTICA, un bloque desafortunado se queda trabajando solo
# mientras los demás están ociosos: el tiempo total = el bloque más lento.
#
# Solución del paper (dinámica): un WORKER LIST global en memoria de la GPU.
#   - Cuando un bloque termina y no hay más tareas, se declara "hambriento".
#   - Un bloque con MUCHO trabajo pendiente DONA parte de su subárbol
#     (empuja al worker list los sub-subárboles que aún no exploró, con su
#     contexto R/P/X completo) en vez de recorrerlo él solo.
#   - Los bloques hambrientos toman esas donaciones de la cola compartida.
#
# Es "work stealing/donating" clásico, adaptado a GPU: la cola vive en
# memoria global y se accede con operaciones atómicas.
#
# Nuestra simulación: hilos Python + collections.deque como cola compartida.
# Para que el desbalance se VEA en un grafo tan chico, cada nodo de árbol
# "cuesta" un pequeño sleep (simula el trabajo de las intersecciones).
# ==============================================================================

COSTO_POR_NODO = 0.01  # segundos de "trabajo" simulado por nodo de árbol

# NOTA: en esta sección usamos la versión SIN pivote dentro de los bloques,
# a propósito: genera subárboles más grandes y desiguales, que es justo el
# fenómeno de desbalance que queremos visualizar en un grafo tan pequeño.


def _explorar_contando(grafo, R, P, X, contador):
    """BK (sin pivote) que solo cuenta nodos y simula costo (sin prints)."""
    contador['nodos'] += 1
    time.sleep(COSTO_POR_NODO)
    if not P and not X:
        contador['cliques'].append(set(R))
        return
    for v in sorted(P):
        if v not in P:
            continue
        _explorar_contando(grafo, R | {v}, P & grafo[v], X & grafo[v], contador)
        P = P - {v}
        X = X | {v}


def _explorar_con_donacion(grafo, R, P, X, contador, worker_list, lock,
                           estado):
    """
    Igual que arriba, PERO: antes de explorar cada hijo, si hay bloques
    hambrientos, el bloque DONA ese hijo (su contexto R/P/X) a la cola
    compartida en vez de explorarlo él mismo. Así el subárbol grande se
    reparte sobre la marcha, exactamente la idea del worker list del paper.
    """
    contador['nodos'] += 1
    time.sleep(COSTO_POR_NODO)
    if not P and not X:
        contador['cliques'].append(set(R))
        return
    for v in sorted(P):
        if v not in P:
            continue
        hijo = (R | {v}, P & grafo[v], X & grafo[v])
        dono = False
        with lock:
            if estado['hambrientos'] > 0 and len(hijo[1]) > 0:
                # hay alguien ocioso y el hijo tiene subárbol no trivial:
                # lo donamos en lugar de bajar nosotros.
                worker_list.append(hijo)
                estado['pendientes'] += 1   # una tarea más en circulación
                contador['donados'] += 1
                dono = True
        if not dono:
            _explorar_con_donacion(grafo, *hijo, contador, worker_list, lock,
                                   estado)
        P = P - {v}
        X = X | {v}


def _bloque_estatico(nombre, tareas, reporte, lock):
    """Bloque con asignación estática: procesa SU lista y nada más."""
    contador = {'nodos': 0, 'cliques': []}
    t0 = time.perf_counter()
    for (R, P, X) in tareas:
        _explorar_contando(GRAFO, R, P, X, contador)
    with lock:
        reporte[nombre] = {'nodos': contador['nodos'],
                           'tiempo': time.perf_counter() - t0,
                           'cliques': contador['cliques']}


def _bloque_dinamico(nombre, worker_list, reporte, lock, estado):
    """
    Bloque con worker list: toma tareas de la cola compartida; si la cola
    está vacía pero AÚN quedan tareas en circulación ('pendientes' > 0), se
    declara hambriento y espera una donación. Termina cuando pendientes == 0
    (terminación global correcta: nadie trabaja y nada queda por hacer).
    """
    contador = {'nodos': 0, 'cliques': [], 'donados': 0}
    t0 = time.perf_counter()
    while True:
        tarea = None
        with lock:
            if worker_list:
                tarea = worker_list.popleft()
            elif estado['pendientes'] == 0:
                break                       # fin global: no queda trabajo
            else:
                estado['hambrientos'] += 1  # anuncio: "estoy ocioso, dónenme"
        if tarea is None:
            time.sleep(COSTO_POR_NODO / 5)  # espera breve por una donación
            with lock:
                estado['hambrientos'] -= 1
            continue
        _explorar_con_donacion(GRAFO, *tarea, contador, worker_list, lock,
                               estado)
        with lock:
            estado['pendientes'] -= 1       # esta tarea quedó 100% explorada
    tiempo = time.perf_counter() - t0
    with lock:
        reporte[nombre] = {'nodos': contador['nodos'], 'tiempo': tiempo,
                           'cliques': contador['cliques'],
                           'donados': contador['donados']}


def seccion_5(orden, posicion):
    titulo("SECCIÓN 5: Balanceo de carga con worker list (donación de trabajo)")
    print(f"""
Simulación: 2 'bloques' procesan los {len(orden)} subárboles de primer nivel.
Cada nodo de árbol cuesta {COSTO_POR_NODO}s simulados (el sleep representa el
trabajo de las intersecciones). El subárbol de 'A' (el hub del K4) es mucho
más grande que el resto: veremos cómo la asignación ESTÁTICA deja a un bloque
ocioso mientras el otro pelea solo con el subárbol grande, y cómo la DINÁMICA
reparte ese subárbol al vuelo mediante donaciones.
""")
    # Las tareas: subárboles de primer nivel (contextos R/P/X) según el
    # orden de degeneración.
    tareas = []
    for v in orden:
        P = {w for w in GRAFO[v] if posicion[w] > posicion[v]}
        X = {w for w in GRAFO[v] if posicion[w] < posicion[v]}
        tareas.append(({v}, P, X))

    lock = threading.Lock()

    # ---------- SIN worker list: reparto estático por mitades ----------
    # (bloque-0 se lleva la primera mitad del orden, bloque-1 la segunda;
    #  en la GPU esto equivale a asignar subárboles por índice, sin robo)
    mitad = len(tareas) // 2
    asignacion = {'bloque-0': tareas[:mitad], 'bloque-1': tareas[mitad:]}
    reporte_est = {}
    hilos = [threading.Thread(target=_bloque_estatico,
                              args=(n, ts, reporte_est, lock))
             for n, ts in asignacion.items()]
    t0 = time.perf_counter()
    for h in hilos: h.start()
    for h in hilos: h.join()
    total_est = time.perf_counter() - t0

    print("SIN worker list (asignación estática):")
    for n in sorted(reporte_est):
        r = reporte_est[n]
        print(f"  {n}: {r['nodos']:3d} nodos procesados en {r['tiempo']:.3f}s  "
              f"cliques: {[fmt(c) for c in r['cliques']] or '-'}")
    peor = max(r['tiempo'] for r in reporte_est.values())
    mejor = min(r['tiempo'] for r in reporte_est.values())
    print(f"  Tiempo total (lo marca el bloque MÁS LENTO): {total_est:.3f}s")
    print(f"  Desbalance: el bloque rápido estuvo ocioso "
          f"{(1 - mejor / peor) * 100:.0f}% del tiempo del lento.\n")

    # ---------- CON worker list: cola compartida + donación ----------
    # Encolamos las tareas de MENOR a MAYOR (por |P|): así el subárbol
    # grande queda para el final, un bloque se queda a solas con él, el otro
    # se declara hambriento... y la donación entra en acción. (En la GPU no
    # se conoce el tamaño real por adelantado; esto solo hace la demo
    # reproducible.)
    tareas_ordenadas = sorted(tareas, key=lambda t: len(t[1]))
    worker_list = deque(tareas_ordenadas)
    estado = {'pendientes': len(tareas_ordenadas), 'hambrientos': 0}
    reporte_din = {}
    hilos = [threading.Thread(target=_bloque_dinamico,
                              args=(f"bloque-{i}", worker_list, reporte_din,
                                    lock, estado))
             for i in range(2)]
    t0 = time.perf_counter()
    for h in hilos: h.start()
    for h in hilos: h.join()
    total_din = time.perf_counter() - t0

    print("CON worker list (cola compartida + donación de subárboles):")
    for n in sorted(reporte_din):
        r = reporte_din[n]
        print(f"  {n}: {r['nodos']:3d} nodos procesados en {r['tiempo']:.3f}s, "
              f"donó {r['donados']} subárboles  "
              f"cliques: {[fmt(c) for c in r['cliques']] or '-'}")
    print(f"  Tiempo total: {total_din:.3f}s  "
          f"(vs {total_est:.3f}s estático => "
          f"{(1 - total_din / total_est) * 100:.0f}% menos)")
    print("""
LECTURA: con la cola compartida, un bloque que agota su trabajo recibe
subárboles DONADOS por el bloque cargado (que en vez de bajar él mismo por
cada hijo, empuja el contexto R/P/X del hijo a la cola). El trabajo total
(nodos) es el mismo; lo que cambia es QUIÉN lo hace y, por tanto, el
tiempo del bloque más lento. En la GPU real esto se implementa con una cola
en memoria global manipulada con operaciones atómicas. (Ojo: al usar hilos
reales, los tiempos y el número de donaciones pueden variar un poco entre
ejecuciones; el fenómeno cualitativo es siempre el mismo.)""")


# ==============================================================================
# SECCIÓN 6: REPRESENTACIÓN COMPACTA DE X  (XP + XX, Fig. 2 del paper)
# ==============================================================================
# El problema de memoria: la recursión de Bron-Kerbosch necesita RESTAURAR
# P y X al volver de cada hijo. La solución ingenua guarda UNA COPIA COMPLETA
# de X por cada nivel de recursión => memoria O(profundidad × |X|), y en
# grafos reales X puede tener MILES de vértices (todos los vecinos
# anteriores en el orden de degeneración). En la GPU, donde cada bloque
# tiene su propio arsenal de memoria preasignado, esto es prohibitivo.
#
# La observación del paper (Fig. 2): X tiene DOS poblaciones muy distintas.
#
#   XP: vértices que llegaron a X desde P (fueron candidatos, se exploraron
#       y se movieron al "pasado"). Como P está acotado por la degeneración
#       (Sección 3), XP es PEQUEÑO => nos podemos permitir una copia por
#       nivel, igual que con P.
#
#   XX: vértices que ya estaban excluidos desde el primer nivel (los vecinos
#       ANTERIORES en el orden de degeneración). Puede ser ENORME. Pero tiene
#       una propiedad MONÓTONA: dentro del subárbol, un vértice de XX jamás
#       regresa a P (nunca vuelve a ser candidato). Su único cambio posible
#       es "dejar de estar" al intersectar con N(v)... y "reaparecer" al
#       backtrackear. O sea: a lo largo de UNA rama, XX solo se ENCOGE al
#       bajar y se restaura EXACTO al subir.
#
# Con esa monotonía no hace falta copiar XX por nivel: basta UNA sola copia
# compartida donde cada vértice anota EN QUÉ NIVEL fue removido:
#   - bajar al nivel l con vértice v: los x ∈ XX activos que NO son vecinos
#     de v se marcan "removido_en = l" (siguen ahí, solo marcados);
#   - pertenencia en el nivel l: x está en XX si removido_en > l (o nunca);
#   - backtrack del nivel l: desmarcar los que tienen removido_en == l.
# Costo: UN entero por vértice EN TOTAL, en vez de una copia por nivel.
# (El paper lo implementa con punteros/particiones por nivel dentro de un
#  mismo arreglo; nuestro dict 'removido_en' es la versión didáctica.)
# ==============================================================================

class XCompacto:
    """
    Estructura didáctica que imita la Fig. 2 del paper.

    - self.xp_por_nivel : lista de copias de XP, una por nivel (XP es chico:
      está acotado por la degeneración, igual que P).
    - self.xx           : UNA SOLA tabla compartida vértice -> nivel en el
      que fue removido (INFINITO = sigue activo). Nunca se copia.

    También lleva contadores de memoria "teórica" (en unidades de enteros
    almacenados) para comparar contra la representación ingenua.
    """
    INF = float('inf')

    def __init__(self, xx_inicial):
        self.xp_por_nivel = [set()]           # nivel 0 arranca con XP vacío
        self.xx = {v: self.INF for v in xx_inicial}
        # --- contadores de memoria (peak = máximo simultáneo) ---
        self.mem_compacta_peak = 0
        self.mem_ingenua_peak = 0
        self._x_ingenuo_por_nivel = [len(xx_inicial)]  # |X| completo por nivel

    # ---------- operaciones que usa la recursión ----------
    def bajar_nivel(self, v, grafo, nuevo_xp):
        """Entrar a un nivel más profundo eligiendo el candidato v."""
        nivel = len(self.xp_por_nivel)          # el nivel al que ENTRAMOS
        # XX: solo MARCAMOS (no copiamos) los que no sobreviven a N(v)
        for x, removido_en in self.xx.items():
            if removido_en > nivel - 1 and x not in grafo[v]:
                self.xx[x] = nivel
        # XP: copia nueva por nivel (es chico, nos lo permitimos)
        self.xp_por_nivel.append(set(nuevo_xp))
        # contabilidad ingenua: habría copiado TODO X (XP + XX activos)
        activos_xx = sum(1 for r in self.xx.values() if r > nivel)
        self._x_ingenuo_por_nivel.append(len(nuevo_xp) + activos_xx)
        self._medir()

    def subir_nivel(self):
        """Backtrack: restaurar el estado del nivel anterior."""
        nivel = len(self.xp_por_nivel) - 1
        # XX: desmarcar lo removido EXACTAMENTE en este nivel (restauración
        # perfecta gracias a la monotonía; ¡sin haber copiado nada!)
        for x, removido_en in self.xx.items():
            if removido_en == nivel:
                self.xx[x] = self.INF
        self.xp_por_nivel.pop()
        self._x_ingenuo_por_nivel.pop()

    def xx_activos(self):
        nivel = len(self.xp_por_nivel) - 1
        return {x for x, r in self.xx.items() if r > nivel}

    def x_completo(self):
        """El X 'lógico' del nivel actual = XP del nivel ∪ XX activos."""
        return self.xp_por_nivel[-1] | self.xx_activos()

    # ---------- contabilidad de memoria ----------
    def _medir(self):
        # compacta: todas las copias de XP + la tabla XX compartida (en el
        # paper XX es UN arreglo: el vértice es el índice y solo se guarda
        # su marca de nivel => 1 entero por vértice, UNA sola vez) + 1
        # puntero de nivel por nivel de recursión activo.
        niveles = len(self.xp_por_nivel)
        compacta = (sum(len(s) for s in self.xp_por_nivel)
                    + len(self.xx) + niveles)
        # ingenua: una copia COMPLETA de X (XP + XX activos) por nivel activo
        ingenua = sum(self._x_ingenuo_por_nivel)
        self.mem_compacta_peak = max(self.mem_compacta_peak, compacta)
        self.mem_ingenua_peak = max(self.mem_ingenua_peak, ingenua)


def seccion_6(orden, posicion):
    titulo("SECCIÓN 6: X compacto — XP (copia por nivel) + XX (copia única "
           "compartida)")
    # En el grafo de juguete el X de primer nivel es diminuto y el ahorro no
    # se aprecia. Para la demo EXTENDEMOS el grafo: imaginamos que antes de
    # 'A' ya se procesaron 8 vértices más (G..N), todos vecinos de A, B y C.
    # Son exactamente el tipo de vértices que pueblan XX en un grafo real:
    # anteriores en el orden de degeneración => JAMÁS regresan a P dentro
    # del subárbol de A. (Nota: como son vecinos de A,B,C pero NO de D,
    # {A,B,C,D} sigue siendo maximal; el ejemplo sigue siendo consistente.)
    extra = ['G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
    grafo_ext = {v: set(vec) for v, vec in GRAFO.items()}
    for u in extra:
        grafo_ext[u] = {'A', 'B', 'C'}
        for w in ('A', 'B', 'C'):
            grafo_ext[w].add(u)

    v_raiz = 'A'
    P0 = {w for w in GRAFO[v_raiz] if posicion[w] > posicion[v_raiz]}
    XX0 = {w for w in GRAFO[v_raiz]
           if posicion[w] < posicion[v_raiz]} | set(extra)

    print(f"""
Demostración sobre el subárbol de primer nivel de '{v_raiz}' en el grafo
extendido (8 vértices 'anteriores' extra G..N, vecinos de A, B y C):
  R = {{{v_raiz}}}   P inicial = {fmt(P0)}
  XX inicial (vecinos ANTERIORES en el orden) = {fmt(XX0)}

Simulamos la rama en la que la sub-rama de B ya fue explorada (B pasó de P
a X: entra en XP) y ahora bajamos por C y luego por D. En cada nivel
mostramos el X "lógico" y cómo lo almacena cada representación. La clave:
XX NUNCA se copia; cada vértice solo se MARCA con el nivel en que dejó de
ser válido, y el backtrack lo restaura borrando la marca.
""")
    xc = XCompacto(XX0)
    R = {v_raiz}
    nivel = 0
    print(f"  nivel {nivel}: R={fmt(R)}  XP={fmt(xc.xp_por_nivel[-1])}  "
          f"XX activos={fmt(xc.xx_activos())}")

    # Pasos de la rama simulada: (vértice con el que bajamos, XP heredado).
    # Al bajar con C, el hermano ya explorado B ∈ N(C) viaja en XP.
    pasos = [('C', {'B'}), ('D', {'B'})]
    for v, xp_heredado in pasos:
        xc.bajar_nivel(v, grafo_ext, xp_heredado & grafo_ext[v])
        R = R | {v}
        nivel += 1
        marcados = {x for x, r in xc.xx.items() if r == nivel}
        print(f"  nivel {nivel}: bajamos con '{v}' -> R={fmt(R)}")
        print(f"           XP (copia nueva de este nivel) = "
              f"{fmt(xc.xp_por_nivel[-1])}")
        print(f"           XX: marcados 'removido en nivel {nivel}': "
              f"{fmt(marcados)}   XX aún activos: {fmt(xc.xx_activos())}")

    print(f"""
  En la hoja: X lógico = {fmt(xc.x_completo())} != vacío, o sea que esta
  rama muere sin reportar ({fmt(R)} se puede extender con B: correcto,
  porque {{A, B, C, D}} ya se reporta por la rama que pasa por B).
""")
    print("  ... y ahora el BACKTRACK restaura XX solo borrando marcas:")
    while nivel > 0:
        xc.subir_nivel()
        nivel -= 1
        print(f"  nivel {nivel}: XX activos de nuevo = {fmt(xc.xx_activos())} "
              f"(restaurado sin haber copiado nada)")

    print(f"""
CONSUMO DE MEMORIA (pico simultáneo, en 'enteros almacenados'):
  Ingenua  (una copia completa de X por nivel)          : {xc.mem_ingenua_peak}
  Compacta (XP por nivel + XX única + puntero por nivel): {xc.mem_compacta_peak}

Y la cuenta asintótica, que es la que importa: con degeneración d
(profundidad y |XP| son O(d)) y m vértices en XX (en un hub, m ~ n):
  ingenua  : O(d * (d + m))   <- re-copia XX en cada nivel  :(
  compacta : O(d*d  +  m)     <- XX se guarda UNA sola vez  :)
Con n = 10^6 y d = 100: ingenua ~ 10^8 enteros por bloque (no cabe),
compacta ~ 10^6 (cabe). ESTA es la diferencia que hace entrar el
algoritmo en la memoria de una GPU.""")


# ==============================================================================
# SECCIÓN 7: CONCLUSIONES EN CÓDIGO
# ==============================================================================

CONCLUSIONES = """
================================================================================
CONCLUSIONES — qué principio de diseño enseña cada sección
================================================================================

1. BRON-KERBOSCH BÁSICO
   Principio: convertir una búsqueda exponencial en un ÁRBOL con estado
   explícito (R, P, X). El conjunto X no es decoración: es el mecanismo de
   CORRECCIÓN que garantiza reportar cada clique maximal exactamente una vez.
   Todo lo demás del paper son optimizaciones SOBRE este árbol.

2. PIVOTEO
   Principio: PODA POR DOMINANCIA. Si toda solución pasa por el pivote u o
   por un no-vecino de u, ramificar por los vecinos de u es trabajo
   redundante. Elegir el pivote que maximiza |P ∩ N(u)| maximiza la poda.
   Lección general: antes de paralelizar, reduce el trabajo total; ningún
   hardware compensa un algoritmo derrochador.

3. ORDENAMIENTO POR DEGENERACIÓN
   Principio: usar propiedades ESTRUCTURALES del grafo para acotar recursos.
   Procesar los vértices en orden de pelado garantiza |P| <= d en todos los
   subárboles de primer nivel. En GPU esto no es solo velocidad: es lo que
   permite PREASIGNAR memoria por bloque y que el problema quepa.

4. SUBÁRBOLES INDEPENDIENTES (Algoritmos 3 y 4)
   Principio: GRANULARIDAD del paralelismo. Los subárboles de BK no
   comparten estado => son tareas perfectas para bloques GPU. Primer nivel:
   pocas tareas grandes (poca memoria, mucho desbalance). Segundo nivel:
   muchas tareas chicas (mejor balance y ocupación, más memoria y trabajo
   redundante). No hay granularidad "correcta" universal: es un trade-off.

5. WORKER LIST
   Principio: BALANCEO DINÁMICO vs ESTÁTICO. Cuando el tamaño de las tareas
   es impredecible (y en árboles de búsqueda lo es SIEMPRE), ninguna
   partición estática funciona: el makespan lo dicta el bloque más lento.
   La donación de subárboles a una cola compartida iguala la carga AL VUELO,
   pagando solo el costo de encolar contextos (R, P, X) pequeños.

6. X COMPACTO (XP + XX)
   Principio: EXPLOTAR MONOTONÍA PARA COMPRIMIR ESTADO. Los vértices de XX
   nunca regresan a P dentro del subárbol; su membresía solo se encoge al
   bajar y se restaura al subir. Entonces basta UNA copia compartida con
   marcas de nivel, en vez de una copia por nivel. Lección general: si una
   estructura cambia de forma monótona a lo largo de la recursión, no la
   copies: versiona sus fronteras (punteros/niveles).

MORALEJA FINAL DEL PAPER
   GPU + búsqueda recursiva irregular NO se llevan bien de forma natural
   (recursión profunda, memoria dinámica, desbalance). El paper muestra la
   receta para domarla: (a) podar primero (pivote), (b) acotar con
   estructura (degeneración), (c) partir en tareas independientes con la
   granularidad adecuada, (d) rebalancear dinámicamente, y (e) comprimir el
   estado explotando invariantes. Cada técnica ataca UNA de las fricciones
   entre el algoritmo y el hardware.

--------------------------------------------------------------------------------
PREGUNTAS TIPO EXAMEN (para autoevaluarte):
  Q1. ¿Por qué Bron-Kerbosch necesita el conjunto X si con R y P ya puede
      construir cliques? ¿Qué se rompería sin él?
  Q2. Demuestra la regla del pivote: ¿por qué todo clique maximal contiene
      al pivote u o a un no-vecino de u?
  Q3. ¿Por qué el orden de degeneración garantiza |P| <= d SOLO en el primer
      nivel, y por qué eso basta para acotar la memoria de todo el subárbol?
  Q4. Da un caso donde convenga paralelismo de segundo nivel sobre el de
      primer nivel, y el costo que se paga a cambio.
  Q5. ¿Qué propiedad de XX hace válida la representación con una sola copia,
      y por qué XP NO tiene esa propiedad?
================================================================================
"""


# ==============================================================================
# PROGRAMA PRINCIPAL: la clase completa, en orden
# ==============================================================================

def main():
    print(__doc__)
    nodos_basico = seccion_1()
    seccion_2(nodos_basico)
    orden, posicion, d = seccion_3()
    seccion_4(orden, posicion)
    seccion_5(orden, posicion)
    seccion_6(orden, posicion)
    titulo("SECCIÓN 7: Conclusiones")
    print(CONCLUSIONES)


if __name__ == '__main__':
    main()

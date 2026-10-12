# ==============================================================
#  EXPLICACION COMPLETA DEL PAPER:
#  "Parallelizing Maximal Clique Enumeration on GPUs"
#  Almasri et al. - PACT 2023
#
#  Ejecuta con:  python explicacion_paper.py
#
#  GLOSARIO RAPIDO DE TERMINOS DEL PAPER:
#
#  G        = el GRAFO completo (del ingles "Graph")
#  V        = conjunto de VERTICES  (del ingles "Vertices" = nodos/puntos)
#  E        = conjunto de ARISTAS   (del ingles "Edges"    = lineas/conexiones)
#  N(v)     = VECINOS de v          (del ingles "Neighbors")
#  Δ        = letra griega DELTA    = grado MAXIMO del grafo
#  d        = DEGENERACY            = max vecinos "hacia adelante" en el ordering
#  R        = clique en construccion (del ingles "Running clique")
#  P        = candidatos            (del ingles "Prospective" = posibles miembros)
#  X        = excluidos             (del ingles "eXcluded"    = ya explorados)
#  MCE      = Maximal Clique Enumeration = enumerar todas las maximal cliques
#  BK       = Bron-Kerbosch         = nombre del algoritmo (apellidos de sus autores)
#  DFS      = Depth-First Search    = busqueda en profundidad
#  BFS      = Breadth-First Search  = busqueda en anchura
#  GPU      = Graphics Processing Unit = tarjeta grafica usada para calculos
# ==============================================================


# ---- Funcion auxiliar para imprimir separadores visuales ----
def titulo(texto):
    print("\n" + "=" * 65)
    print("  " + texto)
    print("=" * 65)

def subtitulo(texto):
    print("\n  --- " + texto + " ---")

def salto():
    print()


# ==============================================================
#
#  EL GRAFO DEL PAPER
#
#  En Python guardamos el grafo como un DICCIONARIO DE SETS:
#    - La CLAVE  del diccionario = un vertice
#    - El VALOR  del diccionario = SET (conjunto) de sus vecinos
#
#  Ejemplo: 'A': {'B','C','D','E','F'}
#  significa que el vertice A esta conectado con B, C, D, E y F.
#
#  El grafo del paper tiene 6 vertices (A B C D E F) y estas aristas:
#
#        B ------- C
#       / \       / \
#      /   \     /   \
#     A     \   /     A
#      \     \ /     /
#       A --- D     A
#        \         /
#         E ----- F
#
#  Conexiones reales del grafo:
#    A - B   A - C   A - D   A - E   A - F
#    B - C   B - D
#    C - D
#    E - F
#
#  Cliques maximas que debemos encontrar: {A,B,C,D}  y  {A,E,F}
#
# ==============================================================

GRAFO = {
    # vertice : set de vecinos directos
    'A': {'B', 'C', 'D', 'E', 'F'},   # A esta conectado con todos
    'B': {'A', 'C', 'D'},
    'C': {'A', 'B', 'D'},
    'D': {'A', 'B', 'C'},
    'E': {'A', 'F'},
    'F': {'A', 'E'},
}

# =========================================================
# PUNTO 1: QUE ES UN GRAFO, SUS ELEMENTOS Y PROPIEDADES
# =========================================================

def punto1_que_es_un_grafo():
    titulo("PUNTO 1: QUE ES UN GRAFO, SUS ELEMENTOS Y PROPIEDADES")

    print("""
  ¿Que es un GRAFO?
  -----------------
  Un grafo es una forma matematica de representar RELACIONES
  entre objetos. Se escribe como:

       G = (V, E)

  Donde:
    G  = el GRAFO completo
    V  = "Vertices" -> los OBJETOS (tambien llamados nodos o puntos)
    E  = "Edges"    -> las ARISTAS (las conexiones, lineas o relaciones)

  Ejemplo del paper:
    Imagina 6 personas (A, B, C, D, E, F).
    Una ARISTA entre dos personas significa "se conocen entre si".
    El grafo representa quienes se conocen.
    """)

    # Extraemos los vertices del grafo (las claves del diccionario)
    V = sorted(GRAFO.keys())
    print(f"  V (vertices) = {V}   <- los 6 nodos del grafo")

    # Extraemos las aristas sin repetir (A-B es lo mismo que B-A)
    E = set()
    for vertice in GRAFO:
        for vecino in GRAFO[vertice]:
            # sorted([v,u]) garantiza que A-B y B-A sean lo mismo
            E.add(tuple(sorted([vertice, vecino])))
    E = sorted(E)
    print(f"  E (aristas)  = {E}")
    print(f"  Total:  {len(V)} vertices,  {len(E)} aristas\n")

    print("""
  PROPIEDADES DE LOS VERTICES:
  ----------------------------
  Cada vertice tiene propiedades que el paper usa mucho:

  N(v) = "Neighbors of v" = VECINOS de v
         El conjunto de todos los vertices conectados directamente a v.

  Grado de v = cuantos vecinos tiene v = |N(v)|
               (el simbolo | | significa "tamano del conjunto")
    """)

    print(f"  {'Vertice v':<12} {'N(v) = Vecinos de v':<32} {'Grado = |N(v)|'}")
    print(f"  {'-'*58}")
    for v in V:
        Nv    = sorted(GRAFO[v])   # vecinos en orden alfabetico
        grado = len(GRAFO[v])      # cuantos vecinos tiene
        print(f"  {v:<12} {str(Nv):<32} {grado}")

    # Calculamos Delta
    grados = {v: len(GRAFO[v]) for v in GRAFO}
    delta  = max(grados.values())
    v_max  = max(grados, key=lambda v: grados[v])

    print(f"""
  DELTA (Δ) = "Delta" = el GRADO MAXIMO de todo el grafo
  --------------------------------------------------------
  Es la cantidad maxima de vecinos que tiene cualquier vertice.

  En nuestro grafo:
    El vertice '{v_max}' tiene el grado maximo = {delta}
    Por lo tanto  Δ = {delta}

  ¿Para que sirve Δ?
    El paper lo usa para calcular cuanta MEMORIA necesita
    el algoritmo en el peor caso.
    Sin ninguna optimizacion, los conjuntos P y X del algoritmo
    pueden tener hasta Δ = {delta} elementos cada uno.
    """)


# =========================================================
# PUNTO 2: MAXIMAL CLIQUES Y K-CLIQUES
# =========================================================

def es_clique(conjunto):
    """
    Comprueba si un conjunto de vertices forma una CLIQUE.

    CLIQUE = subconjunto de vertices donde TODOS estan
             conectados con TODOS dentro del grupo.

    Como comprobarlo:
      Para cada par de vertices (i, j) del conjunto,
      verificamos que exista una arista entre ellos.
      Si algún par no esta conectado -> NO es clique.
    """
    lista = list(conjunto)
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            v1 = lista[i]
            v2 = lista[j]
            if v2 not in GRAFO[v1]:
                return False   # v1 y v2 no estan conectados -> no es clique
    return True   # todos los pares estan conectados -> si es clique


def puede_crecer(clique):
    """
    Comprueba si se puede anadir algun vertice externo a la clique.
    Si se puede crecer -> la clique NO es maximal.
    Si NO se puede crecer -> la clique SI es maximal.

    Como comprobarlo:
      Para cada vertice FUERA de la clique,
      miramos si esta conectado con TODOS los de dentro.
      Si hay uno asi -> la clique puede crecer -> no es maximal.
    """
    todos_los_vertices = set(GRAFO.keys())
    vertices_fuera     = todos_los_vertices - clique   # los que no estan en la clique

    for v in vertices_fuera:
        # ¿Esta v conectado con TODOS los miembros de la clique?
        conectado_con_todos = all(v in GRAFO[miembro] for miembro in clique)
        if conectado_con_todos:
            return True    # si, puede crecer con este vertice v

    return False   # ningun vertice externo puede entrar


def punto2_cliques():
    titulo("PUNTO 2: MAXIMAL CLIQUES Y K-CLIQUES")

    print("""
  CLIQUE (pronunciado "clic")
  ---------------------------
  Un CLIQUE es un grupo de vertices donde
  TODOS SE CONOCEN ENTRE SI (todos conectados con todos).

  Ejemplo real: un grupo de WhatsApp donde todos son amigos
  de todos los demas del grupo.

  En terminos de grafos:
  -> Cada par de vertices del grupo tiene una arista entre ellos.


  MAXIMAL CLIQUE (Clique Maximal)
  --------------------------------
  Una clique que NO PUEDE CRECER.
  No existe ningun vertice FUERA del grupo que este
  conectado con TODOS los miembros del grupo.
  Si lo hubiera, ese vertice podria unirse -> la clique NO seria maximal.

  Analogia: un grupo de amigos donde nadie de fuera conoce
  a todos los del grupo. Si alguien de fuera los conociera a todos,
  podria unirse y el grupo seria mas grande.


  MAXIMUM CLIQUE (Clique Maxima)
  --------------------------------
  La clique MAS GRANDE de todo el grafo.
  Puede haber varias cliques maximal de distintos tamanos,
  pero solo una (o pocas) son la maximum.

  DIFERENCIA CLAVE:
    MAXIMAL  = no se puede ampliar  (aunque sea pequena)
    MAXIMUM  = la mas grande de todas


  K-CLIQUE
  ---------
  Una clique de exactamente K miembros.
  Ejemplos:
    2-clique = dos vertices conectados (una sola arista)
    3-clique = triangulo (tres vertices todos conectados)
    4-clique = {A,B,C,D} donde todos se conocen
    """)

    # Analizamos candidatos concretos del grafo del paper
    candidatos = [
        {'A', 'B', 'C', 'D'},
        {'A', 'E', 'F'},
        {'A', 'B', 'C'},
        {'B', 'C', 'D'},
        {'A', 'B'},
        {'E', 'F'},
    ]

    # Explicaciones personalizadas para cada caso
    explicaciones = {
        frozenset({'A','B','C','D'}): "Todos conectados. Nadie de fuera conecta con los 4.",
        frozenset({'A','E','F'}):     "Todos conectados. B/C/D no conocen a E ni a F.",
        frozenset({'A','B','C'}):     "Todos conectados PERO D conoce a A, B y C -> puede entrar!",
        frozenset({'B','C','D'}):     "Todos conectados PERO A conoce a B, C y D -> puede entrar!",
        frozenset({'A','B'}):         "Conectados, pero C,D conectan con ambos -> puede crecer.",
        frozenset({'E','F'}):         "Conectados, pero A conoce a E y F -> puede entrar!",
    }

    print("  ANALIZANDO CONJUNTOS DEL GRAFO DEL PAPER:\n")
    print(f"  {'Conjunto':<20} {'Clique?':<10} {'Maximal?':<12} {'Explicacion'}")
    print(f"  {'-'*80}")

    for c in candidatos:
        es_c   = es_clique(c)
        crece  = puede_crecer(c) if es_c else None
        maximal_str = "SI" if (es_c and not crece) else ("NO" if es_c else "---")
        exp    = explicaciones[frozenset(c)]
        print(f"  {str(sorted(c)):<20} {'SI' if es_c else 'NO':<10} {maximal_str:<12} {exp}")

    print("""
  CONCLUSION DEL GRAFO DEL PAPER:

    {A,B,C,D} -> MAXIMAL CLIQUE de tamano 4 (4-clique)
                 Es tambien la MAXIMUM clique (la mas grande)

    {A,E,F}   -> MAXIMAL CLIQUE de tamano 3 (3-clique)
                 Es maximal pero no es la maximum (es mas pequena)

    {A,B,C}   -> clique pero NO maximal porque D puede unirse

  El objetivo del algoritmo BK es encontrar TODAS las maximal cliques.
    """)


# =========================================================
# PUNTO 3: ALGORITMO BRON-KERBOSCH SIN Y CON PIVOTE
# =========================================================

# Variable global para contar cuantas veces se llama cada version
total_llamadas_sin_pivote = 0
total_llamadas_con_pivote = 0


def bk_sin_pivote(R, P, X, nivel=0):
    """
    ALGORITMO BRON-KERBOSCH SIN PIVOTE
    ===================================
    Busca todas las maximal cliques del grafo de forma recursiva.

    Los tres conjuntos que maneja:
    --------------------------------
    R = "Running clique" = la clique que estamos construyendo AHORA
        Empieza vacio. Vamos anadiendo vertices uno a uno.
        Cuando terminamos, R contiene una maximal clique completa.

    P = "Prospective vertices" = candidatos a entrar en la clique
        Son vertices que:
          1) NO estan ya en R
          2) Estan conectados con TODOS los vertices de R
        Si anyadimos un vertice de P a R, seguira siendo clique.

    X = "eXcluded vertices" = vertices ya explorados y excluidos
        Son vertices que ya fueron candidatos en llamadas anteriores
        y generaron sus propias cliques. Los excluimos para no
        encontrar la misma clique dos veces.

    CONDICION DE PARADA:
        Si P esta vacio Y X esta vacio -> R es una MAXIMAL CLIQUE.
        (P vacio = nadie mas puede entrar, X vacio = no hay excluidos
         que puedan extenderla = realmente es maximal)

    nivel = profundidad actual en el arbol de recursion (para mostrar sangria)
    """
    global total_llamadas_sin_pivote
    total_llamadas_sin_pivote += 1

    # Sangria visual para ver el arbol de recursion
    sangria = "      " * nivel

    print(f"{sangria}Nivel {nivel} | R={sorted(R)} | P={sorted(P)} | X={sorted(X)}")

    # CONDICION DE PARADA
    if not P and not X:
        print(f"{sangria}  --> ¡MAXIMAL CLIQUE ENCONTRADA! -> {sorted(R)}")
        return [frozenset(R)]

    cliques_encontradas = []
    P = set(P)   # hacemos una copia de P para poder modificarla

    # Iteramos sobre cada candidato v en P (en orden alfabetico)
    for v in sorted(P):

        vecinos_de_v = GRAFO[v]   # N(v) = todos los vecinos de v en el grafo

        print(f"{sangria}  Probando añadir vertice '{v}' a R={sorted(R)}")

        # Llamada recursiva:
        #   - R crece: anadimos v a la clique actual
        #   - P se reduce: solo quedan candidatos que TAMBIEN son vecinos de v
        #     (para que sigan siendo candidatos validos para la nueva clique R+v)
        #   - X se reduce: solo quedan excluidos que TAMBIEN son vecinos de v
        cliques_encontradas += bk_sin_pivote(
            R | {v},             # R union {v}    = R crece con v
            P & vecinos_de_v,    # P interseccion N(v) = candidatos validos para R+v
            X & vecinos_de_v,    # X interseccion N(v) = excluidos relevantes para R+v
            nivel + 1
        )

        # Despues de explorar la rama de v:
        P = P - {v}   # v sale de candidatos (ya lo exploramos)
        X = X | {v}   # v pasa a excluidos (para no repetir su clique)

    return cliques_encontradas


def bk_con_pivote(R, P, X, nivel=0):
    """
    ALGORITMO BRON-KERBOSCH CON PIVOTE
    ====================================
    Igual que sin pivote PERO antes de iterar sobre P,
    elegimos un PIVOTE u para reducir el trabajo.

    ¿Que es el PIVOTE u?
    --------------------
    u = un vertice elegido de P union X (cualquiera de los dos conjuntos)
    Se elige el que tenga MAS vecinos en P (el que "cubre" mas candidatos).

    ¿Para que sirve el pivote?
    --------------------------
    Si el pivote u esta en la clique final, entonces todos sus
    vecinos en P tambien deben estar (para que sea clique).
    Por eso, las cliques que CONTIENEN al pivote u se encuentran
    cuando u entra en R en su propia iteracion.

    Las cliques que NO contienen al pivote u deben tener algun
    vertice de P que NO sea vecino de u.
    Esos son exactamente los vertices de  P - N(u).

    RESULTADO:
    En vez de iterar sobre TODO P, solo iteramos sobre P - N(u).
    Esto puede reducir drasticamente el numero de iteraciones.
    """
    global total_llamadas_con_pivote
    total_llamadas_con_pivote += 1

    sangria = "      " * nivel

    # Condicion de parada (igual que sin pivote)
    if not P and not X:
        print(f"{sangria}  --> ¡MAXIMAL CLIQUE! -> {sorted(R)}")
        return [frozenset(R)]

    P = set(P)

    # ELEGIR PIVOTE: el vertice de P union X con MAS vecinos en P
    # Cuantos mas vecinos tenga en P, mas ramas podamos
    pivote_u = max(
        P | X,                         # buscamos en P union X
        key=lambda u: len(GRAFO[u] & P)  # criterio: maximo |N(u) interseccion P|
    )

    # Solo iteramos sobre los NO vecinos del pivote en P
    # (los vecinos del pivote ya se cubren cuando el pivote entra en R)
    candidatos_a_iterar = sorted(P - GRAFO[pivote_u])

    print(f"{sangria}Nivel {nivel} | R={sorted(R)} | P={sorted(P)} | pivote='{pivote_u}' | iterar solo={candidatos_a_iterar}")

    cliques_encontradas = []

    for v in candidatos_a_iterar:
        vecinos_de_v = GRAFO[v]
        cliques_encontradas += bk_con_pivote(
            R | {v},
            P & vecinos_de_v,
            X & vecinos_de_v,
            nivel + 1
        )
        P = P - {v}
        X = X | {v}

    return cliques_encontradas


def punto3_bron_kerbosch():
    global total_llamadas_sin_pivote, total_llamadas_con_pivote
    titulo("PUNTO 3: ALGORITMO BRON-KERBOSCH (BK) SIN Y CON PIVOTE")

    print("""
  BRON-KERBOSCH (BK) es el algoritmo clasico para encontrar
  TODAS las maximal cliques de un grafo.
  Su nombre viene de sus autores: Coenraad Bron y Joep Kerbosch (1973).

  Funciona como un arbol de DECISIONES recursivo:
    En cada paso decides si un vertice ENTRA o NO ENTRA en la clique.
    Exploras todas las combinaciones posibles de forma sistematica.

  TRES CONJUNTOS que maneja en cada llamada recursiva:
  ------------------------------------------------------

    R  = "Running clique"
         La clique que estamos construyendo en este momento.
         Empieza como conjunto vacio {}.
         Vamos anadiendo vertices uno a uno.

    P  = "Prospective vertices" (candidatos prometedores)
         Vertices que PODRIAN entrar en la clique actual.
         Condicion: estar conectado con TODOS los vertices de R.
         Empieza con TODOS los vertices del grafo.

    X  = "eXcluded vertices" (excluidos)
         Vertices que ya fueron explorados antes en este nivel.
         Se excluyen para no encontrar la misma clique dos veces.
         Empieza vacio.

  REGLA DE PARADA:
    Si P={} y X={} al mismo tiempo -> R es una MAXIMAL CLIQUE.
    (no hay mas candidatos ni excluidos que puedan extenderla)
    """)

    todos = set(GRAFO.keys())

    # ---- VERSION SIN PIVOTE ----
    subtitulo("VERSION SIN PIVOTE: itera sobre TODOS los vertices de P")
    print("""
  En cada nivel del arbol, probamos CADA vertice de P.
  Para cada candidato v:
    1) Lo anadimos a R  (construimos R + {v})
    2) Reducimos P a solo los vecinos de v  (P interseccion N(v))
    3) Reducimos X a solo los vecinos de v  (X interseccion N(v))
    4) Llamamos recursivamente con estos nuevos R, P, X
    5) Sacamos v de P y lo movemos a X (ya explorado)
    """)

    total_llamadas_sin_pivote = 0
    print("  Ejecucion del algoritmo (R=clique actual, P=candidatos, X=excluidos):\n")
    resultado_sin = bk_sin_pivote(set(), todos, set())
    n_sin = total_llamadas_sin_pivote

    salto()
    # ---- VERSION CON PIVOTE ----
    subtitulo("VERSION CON PIVOTE: elige pivote u y solo itera sobre P - N(u)")
    print("""
  En cada nivel, antes de iterar:
    1) Elegimos el PIVOTE u = vertice de P union X con mas vecinos en P
    2) Solo iteramos sobre P - N(u)  (candidatos que NO son vecinos del pivote)
    3) El resto de la logica es igual

  ¿Por que esto reduce el trabajo?
    Si el pivote u tiene muchos vecinos en P, hay pocas ramas que explorar
    (P - N(u) es pequeno). Las cliques que contienen al pivote se encuentran
    automaticamente cuando el pivote sea el candidato v en alguna iteracion.
    """)

    total_llamadas_con_pivote = 0
    print("  Ejecucion del algoritmo con pivote:\n")
    resultado_con = bk_con_pivote(set(), todos, set())
    n_con = total_llamadas_con_pivote

    # ---- Comparacion ----
    salto()
    print(f"  COMPARACION FINAL:")
    print(f"  {'Version':<25} {'Llamadas recursivas':<25} {'Cliques encontradas'}")
    print(f"  {'-'*65}")
    print(f"  {'Sin pivote':<25} {n_sin:<25} {[sorted(c) for c in resultado_sin]}")
    print(f"  {'Con pivote':<25} {n_con:<25} {[sorted(c) for c in resultado_con]}")
    print(f"\n  AHORRO: {n_sin - n_con} llamadas menos usando el pivote ({100*(n_sin-n_con)//n_sin}% reduccion).")
    print("  Ambas versiones encuentran exactamente las MISMAS cliques.")


# =========================================================
# PUNTO 4: DEGENERACY ORDERING
# =========================================================

def calcular_ordering():
    """
    Calcula el degeneracy ordering sin imprimir nada.
    Devuelve la lista de vertices en el orden calculado.
    """
    grado_actual     = {v: len(GRAFO[v]) for v in GRAFO}
    vecinos_actuales = {v: set(GRAFO[v])  for v in GRAFO}
    orden      = []
    eliminados = set()

    for _ in range(len(GRAFO)):
        elegido = min(
            (v for v in GRAFO if v not in eliminados),
            key=lambda v: (grado_actual[v], v)
        )
        orden.append(elegido)
        eliminados.add(elegido)
        for vecino in vecinos_actuales[elegido]:
            if vecino not in eliminados:
                vecinos_actuales[vecino].discard(elegido)
                grado_actual[vecino] -= 1

    return orden


def punto4_degeneracy_ordering():
    titulo("PUNTO 4: DEGENERACY ORDERING (Ordenamiento por Degeneracy)")

    print("""
  ¿POR QUE NECESITAMOS REORDENAR LOS VERTICES?
  ----------------------------------------------
  En el algoritmo BK, cuando procesamos el primer vertice,
  el conjunto P contiene TODOS sus vecinos.

  Si usamos orden ALFABETICO (A, B, C, D, E, F):
    Al procesar 'A', P = {B, C, D, E, F} = 5 elementos (Δ=5)
    Eso significa 5 ramas de recursion en el primer nivel.
    Mucha memoria, mucho trabajo.

  Si reordenamos inteligentemente (DEGENERACY ORDERING):
    Al procesar 'A', P = {B, C, D} = solo 3 elementos (d=3)
    Menos ramas, menos memoria, mas eficiente.

  El DEGENERACY ORDERING es ese reordenamiento inteligente.


  ¿QUE ES EL DEGENERACY ORDERING?
  ---------------------------------
  Un orden de los vertices tal que cada vertice tenga el
  MENOR NUMERO POSIBLE de vecinos que aparecen DESPUES de el.

  A ese maximo numero de vecinos "hacia adelante" se le llama
  DEGENERACY (degeneracy) y se representa con la letra  d.

  Siempre se cumple:  d <= Δ
  En grafos reales:   d << Δ  (d es mucho menor que Δ)


  ALGORITMO PARA CALCULARLO:
  ---------------------------
  Repetir hasta que no queden vertices:
    Paso 1: Busca el vertice con MENOR GRADO en el grafo ACTUAL
            (el que tenga menos conexiones en lo que queda del grafo)
    Paso 2: En caso de EMPATE de grado -> elige el primero en orden ALFABETICO
    Paso 3: Ese vertice va a la siguiente posicion del ordering
    Paso 4: Elimina ese vertice del grafo y actualiza grados de sus vecinos
    """)

    # Variables para el algoritmo paso a paso
    grado_actual     = {v: len(GRAFO[v]) for v in GRAFO}
    vecinos_actuales = {v: set(GRAFO[v])  for v in GRAFO}
    orden      = []
    eliminados = set()

    print("  EJECUCION PASO A PASO:\n")

    for paso in range(len(GRAFO)):

        # Grados actuales de los vertices que quedan
        grados_restantes = {
            v: grado_actual[v]
            for v in sorted(GRAFO)
            if v not in eliminados
        }

        # Elegir: menor grado, desempate alfabetico
        elegido   = min(grados_restantes, key=lambda v: (grado_actual[v], v))
        grado_min = grado_actual[elegido]

        # Detectar si hubo empate para explicarlo
        empates = [v for v in grados_restantes if grado_actual[v] == grado_min]
        if len(empates) > 1:
            otros   = [x for x in empates if x != elegido]
            detalle = f"grado {grado_min}, empate con {otros} -> se elige '{elegido}' (orden alfabetico)"
        else:
            detalle = f"unico vertice con grado minimo = {grado_min}"

        print(f"  Paso {paso+1}:")
        print(f"    Grados actuales: {grados_restantes}")
        print(f"    Elegido: '{elegido}'  ({detalle})")

        orden.append(elegido)
        eliminados.add(elegido)

        # Actualizar grados de los vecinos del eliminado
        vecinos_afectados = []
        for vecino in vecinos_actuales[elegido]:
            if vecino not in eliminados:
                vecinos_actuales[vecino].discard(elegido)
                grado_actual[vecino] -= 1
                vecinos_afectados.append(vecino)

        if vecinos_afectados:
            print(f"    Reducen grado: {sorted(vecinos_afectados)} (pierden 1 conexion al eliminar '{elegido}')")
        print()

    print(f"  DEGENERACY ORDERING RESULTANTE: {orden}")

    # Calcular vecinos "hacia adelante" para cada vertice
    posicion = {v: i for i, v in enumerate(orden)}

    print("""
  VECINOS "HACIA ADELANTE" DE CADA VERTICE:
  ------------------------------------------
  En el ordering [E, F, A, B, C, D]:
    "hacia adelante" = vecinos que aparecen DESPUES en el orden
    Estos son los que formarian el conjunto P en el algoritmo BK
    cuando procesamos ese vertice.
    """)

    print(f"  {'Vertice':<10} {'Pos.':<6} {'Vecinos hacia adelante (= P inicial en BK)':<42} {'|P|'}")
    print(f"  {'-'*65}")
    max_forward = 0
    for v in orden:
        forward    = sorted([u for u in GRAFO[v] if posicion[u] > posicion[v]])
        n_forward  = len(forward)
        max_forward = max(max_forward, n_forward)
        print(f"  {v:<10} {posicion[v]:<6} {str(forward):<42} {n_forward}")

    delta = max(len(GRAFO[v]) for v in GRAFO)
    d     = max_forward

    print(f"""
  RESULTADO FINAL:
    Δ (Delta)     = grado maximo del grafo   = {delta}
    d (degeneracy) = max vecinos hacia adelante = {d}

  Interpretacion:
    Sin ordering: cuando BK procesa el vertice 'A', P puede tener hasta Δ={delta} elementos
    Con ordering: cuando BK procesa el vertice 'A' (pos. 2), P tiene solo d={d} elementos

  Esto hace que el algoritmo sea MAS EFICIENTE en tiempo y memoria.
    """)


# =========================================================
# PUNTO 5: BFS vs DFS - COMPLEJIDAD TEMPORAL Y DE MEMORIA
# =========================================================

def punto5_bfs_vs_dfs():
    titulo("PUNTO 5: BFS vs DFS - IMPACTO EN COMPLEJIDAD")

    print("""
  Cuando buscamos maximal cliques, recorremos un ARBOL DE BUSQUEDA.
  Cada nodo del arbol = una llamada al algoritmo BK con sus R, P, X.
  Los hijos de cada nodo = las llamadas recursivas que genera.

  Hay dos formas de recorrer ese arbol:

  =========================================================
  DFS = "Depth-First Search" = BUSQUEDA EN PROFUNDIDAD
  =========================================================
  Baja por una rama hasta el final, luego sube y baja por la siguiente.

  Ejemplo visual con el arbol BK:
    Nivel 0: Raiz (R={}, P={A,B,C,D,E,F})
    Nivel 1: Rama de A -> Rama de B -> Rama de C -> ...
    Nivel 2: Dentro de la rama de A, baja a sus sub-ramas

  MEMORIA de DFS:
    Solo necesita recordar EL CAMINO ACTUAL desde la raiz.
    = 1 nodo por nivel de profundidad
    = muy poca memoria

  =========================================================
  BFS = "Breadth-First Search" = BUSQUEDA EN ANCHURA
  =========================================================
  Procesa TODOS los nodos de un nivel antes de bajar al siguiente.

  MEMORIA de BFS:
    Necesita guardar TODOS los nodos del nivel actual EN MEMORIA.
    A medida que bajamos, el numero de nodos por nivel EXPLOTA.
    """)

    # Construimos el arbol BK y contamos nodos por nivel
    nodos_por_nivel = {}

    def construir_arbol(R, P, X, nivel):
        nodos_por_nivel[nivel] = nodos_por_nivel.get(nivel, 0) + 1
        if not P and not X:
            return
        P = set(P)
        for v in sorted(P):
            construir_arbol(R | {v}, P & GRAFO[v], X & GRAFO[v], nivel + 1)
            P = P - {v}
            X = X | {v}

    construir_arbol(set(), set(GRAFO.keys()), set(), 0)

    print("  ARBOL DE BUSQUEDA BK DEL GRAFO DEL PAPER (sin pivote):\n")
    print(f"  {'Nivel':<8} {'Nodos en ese nivel':<22} {'BFS: guardar en memoria':<28} {'DFS: guardar en memoria'}")
    print(f"  {'-'*78}")

    maximo_bfs = 0
    for nivel in sorted(nodos_por_nivel):
        n = nodos_por_nivel[nivel]
        maximo_bfs = max(maximo_bfs, n)
        bfs_mem = f"{n} nodos simultaneos"
        dfs_mem = "1 nodo (rama actual)"
        print(f"  {nivel:<8} {n:<22} {bfs_mem:<28} {dfs_mem}")

    total_nodos = sum(nodos_por_nivel.values())

    print(f"""
  Total de nodos en el arbol: {total_nodos}
  Nivel con mas nodos (peor caso BFS): {maximo_bfs} nodos simultaneos

  PROBLEMA CRITICO DE BFS:
  -------------------------
  En este grafo pequeno de 6 vertices el maximo es {maximo_bfs} nodos.
  En grafos reales con MILES de vertices, el numero de nodos
  por nivel crece de forma EXPONENCIAL con la profundidad.

  Ejemplo imaginario en un grafo grande:
    Nivel  0: 1 nodo
    Nivel  1: 100 nodos
    Nivel  2: 5.000 nodos
    Nivel  3: 100.000 nodos
    Nivel  4: 1.000.000 nodos  <- BFS necesita 1M nodos en RAM!
    ...

  BFS necesitaria guardar todos esos nodos a la vez en memoria.
  Eso es INVIABLE para grafos grandes.

  VENTAJA DE DFS:
  ---------------
  DFS solo necesita el camino actual: 1 nodo por nivel.
  En el ejemplo anterior: solo 4 nodos en RAM al mismo tiempo.

  IMPACTO EN GPU (del paper):
  ----------------------------
  Los trabajos anteriores en GPU usaban BFS entre niveles,
  lo que requeria sincronizacion CPU<->GPU en cada nivel.
  El paper usa DFS: todo el trabajo en un SOLO kernel GPU,
  sin comunicacion CPU<->GPU.
  Resultado: 35x mas rapido que la implementacion BFS anterior.
    """)


# =========================================================
# PUNTO 6: PARAMETROS Δ y d - ASINTOTAS DE MEMORIA
# =========================================================

def punto6_parametros_delta_d():
    titulo("PUNTO 6: PARAMETROS Δ y d - ASINTOTAS DE MEMORIA DE P y P∪X")

    # Calculamos Δ
    delta   = max(len(GRAFO[v]) for v in GRAFO)
    v_delta = max(GRAFO, key=lambda v: len(GRAFO[v]))

    # Calculamos d usando el ordering
    orden    = calcular_ordering()
    posicion = {v: i for i, v in enumerate(orden)}
    d = max(
        len([u for u in GRAFO[v] if posicion[u] > posicion[v]])
        for v in orden
    )

    print(f"""
  REPASO DE LOS DOS PARAMETROS CLAVE:
  =====================================

  Δ  (letra griega "Delta mayuscula")
  ------------------------------------
  = el GRADO MAXIMO del grafo
  = la cantidad de vecinos que tiene el vertice MAS CONECTADO

  En nuestro grafo:
    El vertice '{v_delta}' tiene {delta} vecinos -> Δ = {delta}

  Importancia: sin ninguna optimizacion, el conjunto P del algoritmo BK
  puede tener hasta Δ vertices (todos los vecinos del vertice actual).


  d  (letra "d" minuscula = "degeneracy")
  -----------------------------------------
  = el maximo de vecinos "hacia adelante" en el degeneracy ordering
  = cuantos vecinos puede tener un vertice entre los que aparecen
    DESPUES de el en el ordering

  En nuestro grafo:
    Ordering: {orden}
    El vertice 'A' (pos. 2) tiene vecinos hacia adelante: B, C, D -> 3
    Ningun otro vertice supera eso -> d = {d}

  Importancia: CON degeneracy ordering, el conjunto P del algoritmo BK
  tiene como maximo d vertices (mucho menos que Δ).

  Relacion: d <= Δ  siempre.
  En grafos reales: d puede ser 10, 100, o 1000 veces menor que Δ.
    """)

    print("  CUANTA MEMORIA USAN LOS CONJUNTOS P y X:")
    print("  ==========================================\n")

    print("  Conjunto P  (candidatos a entrar en la clique):")
    print(f"    Sin ordering:  P tiene hasta Δ  = {delta} vertices por llamada")
    print(f"    Con ordering:  P tiene hasta d   = {d} vertices por llamada")
    print(f"    Ahorro en P:   {delta} -> {d}  ({100*(1-d/delta):.0f}% menos vertices en P)\n")

    print("  Conjunto X  (vertices excluidos ya explorados):")
    print(f"    Sin ordering:  X tiene hasta Δ  = {delta} vertices")
    print(f"    Con ordering:  X tiene hasta Δ  = {delta} vertices  <- IGUAL, no mejora")
    print("    (X contiene vecinos ya procesados, que pueden ser cualquiera)\n")

    print("  Conjunto P∪X  (P union X = todos los relevantes):")
    print(f"    Sin ordering:  O(Δ) = O({delta})")
    print(f"    Con ordering:  O(Δ) = O({delta})  <- dominado por X\n")

    print("  SUBGRAFO INDUCIDO H(P, X)  (estructura auxiliar del paper):")
    print("  -------------------------------------------------------------")
    print("  El paper construye un subgrafo con solo los vertices de P y X")
    print("  para acelerar las operaciones de interseccion de conjuntos.\n")
    print(f"  Sin ordering:")
    print(f"    P tiene hasta Δ={delta} vertices, cada uno con hasta Δ={delta} vecinos en P∪X")
    print(f"    -> El subgrafo tiene hasta Δ x Δ = Δ² = {delta}² = {delta**2} aristas")
    print(f"    -> O(Δ²) = O({delta**2})\n")
    print(f"  Con ordering:")
    print(f"    P tiene hasta d={d} vertices, X tiene hasta Δ={delta} vertices")
    print(f"    -> El subgrafo tiene hasta Δ x d = {delta} x {d} = {delta*d} aristas")
    print(f"    -> O(Δ·d) = O({delta*d})\n")

    print(f"  TABLA COMPARATIVA COMPLETA:")
    print(f"  {'Conjunto / Estructura':<30} {'Sin ordering':<20} {'Con ordering':<20} {'Mejora'}")
    print(f"  {'-'*80}")
    print(f"  {'P (candidatos)':<30} {'O(Δ) = O('+str(delta)+')':<20} {'O(d) = O('+str(d)+')':<20} {delta//d}x menos")
    print(f"  {'X (excluidos)':<30} {'O(Δ) = O('+str(delta)+')':<20} {'O(Δ) = O('+str(delta)+')':<20} sin mejora")
    print(f"  {'P∪X':<30} {'O(Δ) = O('+str(delta)+')':<20} {'O(Δ) = O('+str(delta)+')':<20} sin mejora")
    print(f"  {'Subgrafo H(P,X)':<30} {'O(Δ²) = O('+str(delta**2)+')':<20} {'O(Δ·d) = O('+str(delta*d)+')':<20} {delta//d}x menos aristas")

    print(f"""
  EJEMPLO EN UN GRAFO REAL (del paper, grafo "com-Amazon"):
    Δ ≈ 2.752  (el vertice mas conectado tiene 2752 vecinos)
    d ≈ 6      (la degeneracy es solo 6!)

    Sin ordering:  subgrafo = O(2752²) = O(7.573.504) aristas
    Con ordering:  subgrafo = O(2752 × 6) = O(16.512) aristas

    -> El subgrafo es 459 veces mas pequeno con ordering!
    """)


# =========================================================
# PUNTO 7: WORKERS LIST vs WORKLIST
# =========================================================

def punto7_workers_list():
    titulo("PUNTO 7: WORKERS LIST vs WORKLIST - PARALELIZACION EN GPU")

    print("""
  CONTEXTO: ¿Como se paraleliza BK en una GPU?
  =============================================
  Una GPU tiene miles de BLOQUES DE HILOS que trabajan en paralelo.
  El paper asigna a cada bloque UN SUBARBOL del arbol de busqueda BK.

  Con el degeneracy ordering [E, F, A, B, C, D]:
    Hay 6 vertices -> 6 subarboles de nivel 1.
    Se asigna un bloque GPU a cada subarbol.

  PROBLEMA: DESEQUILIBRIO DE CARGA (Load Imbalance)
  ---------------------------------------------------
  Los subarboles tienen TAMANOS MUY DISTINTOS:

    Bloque para 'E': P={F,A} -> subarbol PEQUENO -> termina rapido
    Bloque para 'F': P={A}   -> subarbol MUY PEQUENO -> termina rapido
    Bloque para 'A': P={B,C,D} -> subarbol GRANDE -> tarda mucho
    Bloque para 'B': P={C,D}   -> subarbol MEDIANO
    Bloque para 'C': P={D}     -> subarbol PEQUENO
    Bloque para 'D': P={}      -> sin trabajo -> termina al instante

  Si no hacemos nada:
    Bloques E, F, C, D terminan rapido y quedan OCIOSOS (sin hacer nada).
    El tiempo total = el del bloque mas lento (bloque 'A').
    Muchos recursos de la GPU desperdiciados.
    """)

    trabajo  = {'E': 2, 'F': 1, 'A': 8, 'B': 4, 'C': 2, 'D': 0}
    tiempo_max  = max(trabajo.values())
    total_utl   = sum(trabajo.values())
    media       = total_utl / len(trabajo)

    print("  TRABAJO ESTIMADO DE CADA BLOQUE:")
    print("  (longitud de la barra = cantidad de trabajo)\n")
    for bloque, t in trabajo.items():
        barra   = '█' * t if t > 0 else '(vacio)'
        estado  = " <- el mas lento!" if t == tiempo_max else ""
        print(f"    Bloque '{bloque}':  {barra:<12}  ({t} unidades){estado}")

    print(f"""
  Sin balanceo:
    Tiempo total         = {tiempo_max} unidades (esperamos al mas lento: 'A')
    Trabajo util total   = {total_utl} unidades
    Trabajo desperdiciado = {len(trabajo)*tiempo_max - total_utl} unidades (bloques ociosos)
    Ratio de desequilibrio = {tiempo_max/media:.2f}x  (el peor bloque trabaja {tiempo_max/media:.1f}x mas que la media)
    """)

    print("  ─" * 30)
    print("""
  SOLUCION RECHAZADA: WORKLIST (lista de TAREAS)
  ===============================================
  Idea intuitiva: guardar las tareas pendientes en una cola compartida.
  Los bloques ociosos tomarian tareas de la cola.

  Datos que necesita una TAREA en MCE:
    R         = conjunto de vertices de la clique actual
    P         = conjunto de candidatos
    X         = conjunto de excluidos
    nivel     = profundidad en el arbol de recursion
    subgrafo  = estructura auxiliar con las aristas relevantes

  PROBLEMA 1 - MEMORIA EXCESIVA:
    Cada tarea ocupa muchisima memoria (P y X pueden ser grandes).
    Si hay cientos de tareas en la cola -> gigabytes de RAM de GPU.

  PROBLEMA 2 - OVERHEAD DE GESTION:
    Anadir y quitar tareas de la cola requiere operaciones atomicas costosas.
    Con miles de bloques haciendolo simultaneamente -> congestion.

  CONCLUSION: el worklist es INVIABLE para MCE.
    """)

    print("  ─" * 30)
    print("""
  SOLUCION DEL PAPER: WORKERS LIST (lista de TRABAJADORES)
  ==========================================================
  Idea diferente: en vez de guardar TAREAS, guardamos BLOQUES OCIOSOS.

  La workers list es una cola que guarda solo los IDs de los bloques
  que estan OCIOSOS (han terminado su trabajo actual).

  Dos ROLES en el sistema:
  -------------------------

  RECEPTOR (Receiver block):
    Un bloque que ha terminado su trabajo.
    Se apunta en la workers list: "estoy libre, me llamo bloque #5".
    Luego se DUERME (queda en espera activa, sin consumir computos).

  DONANTE (Donor block):
    Un bloque que esta ocupado con un subarbol GRANDE (|P| >= 10).
    Periodicamente mira si hay receptores en la workers list.
    Si encuentra uno:
      1) Saca el ID del receptor de la workers list.
      2) Coge UNA RAMA de su subarbol (un vertice de su P).
      3) Inicializa los datos del receptor con esa rama.
      4) DESPIERTA al receptor para que procese esa rama.
    Si no hay receptores: sigue trabajando normalmente.

  ¿POR QUE ES MEJOR QUE EL WORKLIST?
    La workers list solo guarda IDs de bloques (numeros enteros).
    Los datos de la tarea (R, P, X, subgrafo) ya estan en la memoria
    del bloque DONANTE. No hay que moverlos a una cola global.
    Solo se copian al receptor cuando se produce la donacion.
    -> MUCHO menos overhead y memoria.
    """)

    print("  SIMULACION PASO A PASO:\n")
    eventos = [
        ("t=0", "INICIO: 6 bloques empiezan con sus subarboles asignados."),
        ("t=0", "  Bloque D: P={} -> termina inmediatamente, se apunta como RECEPTOR."),
        ("t=1", "  Bloque F: P={A} -> termina. Se apunta como RECEPTOR."),
        ("t=1", "  Bloque A detecta receptor (F). Le DONA la rama de B de su P."),
        ("t=1", "  Ahora: Bloque A procesa rama C,D. Bloque F procesa rama B."),
        ("t=2", "  Bloque E y C terminan. Se apuntan como RECEPTORES."),
        ("t=2", "  Bloque A dona rama C a bloque E. Bloque B dona trabajo a bloque C."),
        ("t=4", "  Bloque B termina. Todos los trabajos grandes estan repartidos."),
        ("t=5", "  TODOS los subarboles terminados."),
    ]
    for tiempo, desc in eventos:
        print(f"    {tiempo:<6}  {desc}")

    nuevo_tiempo = tiempo_max // 2 + 1
    print(f"""
  RESULTADO FINAL:
  {'Metodo':<25} {'Tiempo total':<18} {'Ratio desequilibrio':<22} {'Eficiencia'}
  {'-'*75}
  {'Sin workers list':<25} {str(tiempo_max)+' unidades':<18} {str(round(tiempo_max/media,2))+'x':<22} bajo
  {'Con workers list':<25} {str(nuevo_tiempo)+' unidades':<18} {'~'+str(round(nuevo_tiempo/media,2))+'x':<22} alto

  El paper mide en grafos reales:
    Sin workers list: ratio = 2.28x
    Con workers list: ratio = 1.17x  (casi perfecto con overhead minimo)


  SEGUNDO NIVEL DE PARALELIZACION (lo que ocurre dentro de un bloque):
  -----------------------------------------------------------------------
  Ademas de repartir subarboles entre bloques (paralelismo entre bloques),
  dentro de cada bloque los hilos trabajan en PARALELO para:

    - Calcular la INTERSECCION de conjuntos (P interseccion N(v), X interseccion N(v))
    - Seleccionar el PIVOTE (buscar el maximo de |N(u) interseccion P|)
    - Construir el SUBGRAFO inducido H(P,X)

  FASE 1 (estatica): cada bloque toma su subarbol de nivel 1.
                     Sin comunicacion entre bloques.

  FASE 2 (dinamica): workers list activa.
                     Donantes ceden ramas de nivel 2 en adelante.
                     Solo si |P| >= 10 para que valga la pena.

  Ejemplo con el grafo del paper:
    Fase 1: bloque 'A' empieza con R={{A}}, P={{B,C,D}}
    Fase 2: bloque 'F' queda ocioso.
            Bloque 'A' le cede la rama donde v='B'.
            Bloque 'F' procesa:  R={{A,B}}, P={{C,D}}, X={{}}
            Bloque 'A' procesa:  R={{A,C}}, P={{D}},   X={{B}} y R={{A,D}}, P={{}}, X={{B,C}}
    """)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    titulo("PAPER: Parallelizing Maximal Clique Enumeration on GPUs")

    print("""
  ¿De que trata el paper?
  -----------------------
  El paper resuelve el problema de encontrar TODAS las maximal cliques
  de un grafo de forma muy rapida usando una GPU (tarjeta grafica).

  ¿Para que sirve encontrar maximal cliques en la vida real?
  -----------------------------------------------------------
    - Bioinformatica: descubrir grupos de proteinas que interactuan
    - Redes sociales: detectar comunidades donde todos se conocen
    - Deteccion de temas: agrupar mensajes por tematica automaticamente
    - Compresion de grafos: encontrar patrones repetidos

  ¿Cual es el grafo de ejemplo que usa el paper?
  -----------------------------------------------
  6 vertices: A B C D E F
  Conexiones:
    A-B  A-C  A-D  A-E  A-F    (A conectado con todos)
    B-C  B-D                   (B conectado con C y D ademas de A)
    C-D                        (C conectado con D ademas de A,B)
    E-F                        (E y F solo se conectan con A y entre si)

  Maximal cliques del grafo:
    {A, B, C, D}  -> todos los 4 se conocen entre si
    {A, E, F}     -> los 3 se conocen entre si

  GLOSARIO RAPIDO:
    G      = el grafo completo
    V      = vertices (nodos, puntos)
    E      = edges (aristas, conexiones, lineas)
    N(v)   = neighbors = vecinos de v
    Δ      = Delta = grado maximo del grafo (= {max(len(GRAFO[v]) for v in GRAFO)})
    d      = degeneracy = max vecinos hacia adelante en el ordering
    R      = Running clique = clique que estamos construyendo
    P      = Prospective = candidatos a entrar en la clique
    X      = eXcluded = vertices ya explorados
    BK     = Bron-Kerbosch = nombre del algoritmo
    MCE    = Maximal Clique Enumeration = encontrar todas las maximal cliques
    DFS    = Depth-First Search = busqueda en profundidad
    BFS    = Breadth-First Search = busqueda en anchura
    GPU    = tarjeta grafica usada para calculos paralelos masivos
    """)

    input("  Pulsa ENTER para empezar con el Punto 1...")

    punto1_que_es_un_grafo()
    input("\n  Pulsa ENTER -> Punto 2...")

    punto2_cliques()
    input("\n  Pulsa ENTER -> Punto 3...")

    punto3_bron_kerbosch()
    input("\n  Pulsa ENTER -> Punto 4...")

    punto4_degeneracy_ordering()
    input("\n  Pulsa ENTER -> Punto 5...")

    punto5_bfs_vs_dfs()
    input("\n  Pulsa ENTER -> Punto 6...")

    punto6_parametros_delta_d()
    input("\n  Pulsa ENTER -> Punto 7...")

    punto7_workers_list()

    titulo("RESUMEN FINAL DE LOS 7 PUNTOS")
    print("""
  1. GRAFO G=(V,E): V=vertices(nodos), E=aristas(conexiones).
     N(v)=vecinos de v. Grado=cuantos vecinos. Δ=grado maximo.

  2. CLIQUE: todos conectados con todos.
     MAXIMAL CLIQUE: clique que no puede crecer (no hay vertice externo que conecte con todos).
     K-CLIQUE: clique de exactamente k miembros.

  3. BRON-KERBOSCH: R=clique actual, P=candidatos, X=excluidos.
     Sin pivote: itera todo P.
     Con pivote u: elige u con max vecinos en P, itera solo P-N(u). Menos ramas.

  4. DEGENERACY ORDERING: eliminar siempre el de menor grado (desempate alfabetico).
     d = max vecinos hacia adelante. Con ordering, P tiene O(d) en vez de O(Δ).

  5. DFS guarda solo la rama actual = O(profundidad) memoria.
     BFS guarda todo el nivel actual = memoria EXPONENCIAL. Inviable.

  6. Sin ordering: P=O(Δ), subgrafo=O(Δ²).
     Con ordering: P=O(d), subgrafo=O(Δ·d). Como d<<Δ, ahorro enorme.

  7. Workers list = cola de IDs de bloques OCIOSOS (no de tareas completas).
     Donante (bloque ocupado) cede una rama al Receptor (bloque ocioso).
     Fase 1=subarboles estaticos. Fase 2=workers list activa.
     Mejora ratio de desequilibrio de 2.28x a 1.17x.
    """)

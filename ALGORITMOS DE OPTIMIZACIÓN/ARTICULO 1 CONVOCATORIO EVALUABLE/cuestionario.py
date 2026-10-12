# ==============================================================
#  CUESTIONARIO DE EVALUACION
#  "Parallelizing Maximal Clique Enumeration on GPUs"
#  Almasri et al. - PACT 2023
#
#  Ordenado de MAS BASICO a MAS AVANZADO.
#  Cada pregunta construye sobre la anterior.
#  Ejecuta con:  python cuestionario.py
# ==============================================================

VERDE    = "\033[92m"
ROJO     = "\033[91m"
AMARILLO = "\033[93m"
AZUL     = "\033[94m"
CIAN     = "\033[96m"
NEGRITA  = "\033[1m"
RESET    = "\033[0m"

NIVELES_COLOR = {"Basico": VERDE, "Medio": AMARILLO, "Avanzado": ROJO}

PREGUNTAS = [

    # ╔══════════════════════════════╗
    # ║  PUNTO 1 — El grafo         ║
    # ╚══════════════════════════════╝

    {
        "punto": 1, "nivel": "Basico",
        "tema" : "P1.1 — Que es un grafo G=(V,E)",
        "teoria": """\
  ¿QUE ES UN GRAFO?
  ──────────────────
  Un GRAFO es una estructura matematica para representar relaciones.
  Se usa en redes sociales, proteinas, mapas, textos, etc.

  Se escribe:  G = (V, E)

    G  ->  "Graph"    = el grafo completo
    V  ->  "Vertices" = los OBJETOS (nodos / puntos)
    E  ->  "Edges"    = las CONEXIONES entre objetos (aristas / lineas)

  Grafo del paper: 6 personas A-F.
    V = {A, B, C, D, E, F}
    E = {A-B, A-C, A-D, A-E, A-F, B-C, B-D, C-D, E-F}   (9 aristas)\
""",
        "pregunta": "¿Que representa cada letra en G = (V, E)?",
        "opciones": [
            "G = grafo completo,  V = velocidad,  E = eficiencia",
            "G = grafo completo,  V = Vertices (nodos),  E = Edges (aristas/conexiones)",
            "G = generador,  V = vector de datos,  E = espacio de busqueda",
            "G = grado maximo,  V = valores,  E = etiquetas",
        ],
        "correcta": 1,
        "explicacion": """\
  G = (V, E):
    V = "Vertices" = los nodos/objetos del grafo.
    E = "Edges"    = las aristas/conexiones entre ellos.
  En el paper: V tiene 6 vertices y E tiene 9 aristas.\
""",
    },

    {
        "punto": 1, "nivel": "Basico",
        "tema" : "P1.2 — Vecinos N(v) y grado de un vertice",
        "teoria": """\
  CONTINUANDO: ahora que sabes que G=(V,E), veamos las propiedades
  de cada vertice individual.

  N(v) = "Neighbors of v" = VECINOS de v
         Todos los vertices conectados DIRECTAMENTE con v.
         v NO se incluye a si mismo.

  GRADO de v = cuantos vecinos tiene = |N(v)|
               (| | = "numero de elementos del conjunto")

  En el grafo del paper:
    N(A) = {B,C,D,E,F}  ->  grado(A) = 5
    N(E) = {A,F}         ->  grado(E) = 2
    N(D) = {A,B,C}       ->  grado(D) = 3\
""",
        "pregunta": "¿Cuanto vale N(E) y el grado de E en el grafo del paper?",
        "opciones": [
            "N(E) = {A,E,F}  y  grado(E) = 3  (contando al propio E)",
            "N(E) = {A,F}    y  grado(E) = 2",
            "N(E) = {A}      y  grado(E) = 1",
            "N(E) = {A,B,F}  y  grado(E) = 3",
        ],
        "correcta": 1,
        "explicacion": """\
  E esta conectado directamente con A y con F.
  N(E) = {A, F}  ->  grado(E) = 2.
  Un vertice NO se cuenta a si mismo entre sus vecinos.\
""",
    },

    {
        "punto": 1, "nivel": "Basico",
        "tema" : "P1.3 — Contar aristas totales del grafo",
        "teoria": """\
  CONTINUANDO: ya sabes calcular N(v) y el grado.
  Ahora usaremos los grados para contar el TOTAL de aristas del grafo.

  TRUCO: la suma de todos los grados = 2 x numero de aristas.
  ¿Por que? Porque cada arista A-B suma 1 al grado de A Y 1 al grado de B.
  Es decir, cada arista se cuenta DOS veces en la suma de grados.

  Grados del grafo del paper:
    grado(A)=5, grado(B)=3, grado(C)=3,
    grado(D)=3, grado(E)=2, grado(F)=2
    Suma = 5+3+3+3+2+2 = 18

  Total de aristas = 18 / 2 = 9

  Verificacion: las 9 aristas son
    A-B, A-C, A-D, A-E, A-F, B-C, B-D, C-D, E-F   ✓\
""",
        "pregunta": "¿Cuantas aristas tiene en total el grafo del paper y como se calcula ese numero?",
        "opciones": [
            "6 aristas, porque hay 6 vertices y cada uno tiene una arista principal",
            "12 aristas, porque se cuentan A-B y B-A por separado",
            "9 aristas, calculadas como (suma de grados) / 2 = 18/2 = 9",
            "15 aristas, porque con 6 vertices el maximo posible es 6x5/2 = 15",
        ],
        "correcta": 2,
        "explicacion": """\
  Suma de grados = 5+3+3+3+2+2 = 18.
  Total aristas  = 18 / 2 = 9.
  (cada arista aporta 1 al grado de cada extremo, por eso se divide entre 2)

  Las 9 aristas: A-B, A-C, A-D, A-E, A-F, B-C, B-D, C-D, E-F.\
""",
    },

    {
        "punto": 1, "nivel": "Medio",
        "tema" : "P1.4 — Grafo NO dirigido y Delta (Δ)",
        "teoria": """\
  CONTINUANDO: conoces los vertices, aristas y grados.
  Dos propiedades mas que usa el paper:

  GRAFO NO DIRIGIDO:
    Las aristas NO tienen direccion. Si A-B existe, entonces B-A tambien.
    El paper trabaja con grafos NO dirigidos.
    (Comparacion: en Twitter te puedo seguir sin que tu me sigas = DIRIGIDO.
                  En Facebook si somos amigos, los dos nos seguimos = NO DIRIGIDO)

  Δ (DELTA MAYUSCULA) = el GRADO MAXIMO del grafo:
    Δ = el numero de vecinos del vertice MAS conectado.
    Para calcularlo: miras todos los grados y coges el mayor.

    Grados del paper: A=5, B=3, C=3, D=3, E=2, F=2.
    El mayor es 5 (vertice A)  ->  Δ = 5.

  ¿Para que sirve Δ?
    Marca el PEOR CASO de memoria del algoritmo BK sin optimizar.
    El conjunto P de candidatos puede tener hasta Δ elementos.\
""",
        "pregunta": "¿Cuanto vale Δ en el grafo del paper y que implica para la memoria del algoritmo?",
        "opciones": [
            "Δ = 9, el numero total de aristas del grafo",
            "Δ = 3, el grado mas frecuente entre los vertices",
            "Δ = 5, el grado maximo. Sin optimizacion, P puede tener hasta 5 candidatos",
            "Δ = 6, el numero total de vertices del grafo",
        ],
        "correcta": 2,
        "explicacion": """\
  Δ = grado maximo = grado(A) = 5.
  Sin degeneracy ordering, el conjunto P puede tener hasta Δ=5 elementos.
  Cuanto mayor es Δ, mas memoria y tiempo necesita el algoritmo.
  Reducir el tamano efectivo de P es uno de los objetivos del paper.\
""",
    },

    {
        "punto": 1, "nivel": "Medio",
        "tema" : "P1.5 — Leer el grafo: verificar una arista concreta",
        "teoria": """\
  CONTINUANDO: ya dominas la estructura del grafo.
  Ultimo detalle importante: saber LEER el grafo del paper.

  El grafo del paper tiene estas aristas (conexiones):
    A conecta con: B, C, D, E, F   (A es el vertice central)
    B conecta con: A, C, D
    C conecta con: A, B, D
    D conecta con: A, B, C
    E conecta con: A, F
    F conecta con: A, E

  Preguntas que puedes hacerte:
    "¿Existe la arista B-E?"  ->  B no esta en N(E) ni E en N(B)  -> NO existe.
    "¿Existe la arista C-D?"  ->  D esta en N(C) y C en N(D)      -> SI existe.
    "¿Existe la arista E-C?"  ->  C no esta en N(E)               -> NO existe.

  Saber esto de memoria es fundamental para seguir los algoritmos.\
""",
        "pregunta": "¿Cuales de estas aristas EXISTEN en el grafo del paper?",
        "opciones": [
            "B-E existe  y  E-C existe",
            "B-D existe  y  E-F existe",
            "B-F existe  y  C-E existe",
            "D-F existe  y  B-E existe",
        ],
        "correcta": 1,
        "explicacion": """\
  B-D: D esta en N(B) = {A,C,D} ✓  ->  B-D SI existe.
  E-F: F esta en N(E) = {A,F}   ✓  ->  E-F SI existe.

  B-E: E no esta en N(B) ✗  ->  NO existe.
  E-C: C no esta en N(E) ✗  ->  NO existe.
  D-F: F no esta en N(D) ✗  ->  NO existe.\
""",
    },

    # ╔══════════════════════════════╗
    # ║  PUNTO 2 — Cliques          ║
    # ╚══════════════════════════════╝

    {
        "punto": 2, "nivel": "Basico",
        "tema" : "P2.1 — Que es una clique",
        "teoria": """\
  AHORA QUE SABES LEER EL GRAFO, vamos a buscar CLIQUES en el.

  CLIQUE = grupo de vertices donde TODOS se conectan con TODOS.
  Condicion exacta: para CADA PAR (u,v) del grupo, la arista u-v existe.

  Analogia: grupo de WhatsApp donde cada persona es amiga de TODAS las demas.

  Para verificar si {A,B,C} es clique, compruebas los pares:
    A-B ✓  A-C ✓  B-C ✓    -> los 3 pares existen -> SI es clique.

  Para verificar si {A,B,E} es clique:
    A-B ✓  A-E ✓  B-E ✗    -> B-E no existe -> NO es clique.\
""",
        "pregunta": "¿Cual de estos conjuntos forma una CLIQUE en el grafo del paper?",
        "opciones": [
            "{A, B, E}   porque A conecta con B y con E",
            "{B, C, D}   porque B-C existe, B-D existe y C-D existe",
            "{D, E, F}   porque son los vertices de menor grado",
            "{A, C, F}   porque A conecta con C y con F",
        ],
        "correcta": 1,
        "explicacion": """\
  {B,C,D}: B-C ✓, B-D ✓, C-D ✓ -> todos los pares conectados -> SÍ es clique.
  {A,B,E}: B-E no existe -> NO es clique.
  {D,E,F}: D-E no existe -> NO es clique.
  {A,C,F}: C-F no existe -> NO es clique.\
""",
    },

    {
        "punto": 2, "nivel": "Basico",
        "tema" : "P2.2 — Maximal vs maximum clique",
        "teoria": """\
  CONTINUANDO: ya sabes identificar cliques.
  Ahora el concepto mas importante del paper: MAXIMAL CLIQUE.

  MAXIMAL CLIQUE = clique que NO PUEDE CRECER.
    No hay ningun vertice FUERA del grupo conectado con TODOS los de dentro.

  MAXIMUM CLIQUE = la clique MAS GRANDE del grafo.

  Como comprobar si una clique es maximal:
    Para cada vertice v FUERA del grupo:
      ¿Conecta v con TODOS los miembros? -> SI -> NO es maximal.
      ¿No conecta con alguno?            -> NO -> seguir comprobando.
    Si ningun externo conecta con todos -> SI es maximal.

  En el paper:
    {A,B,C,D}: externos son E y F.
      E-B no existe ✗ -> E no puede entrar.
      F-B no existe ✗ -> F no puede entrar.
      -> SÍ es maximal.

    {A,B,C}: externos son D, E, F.
      D-A ✓  D-B ✓  D-C ✓ -> D PUEDE entrar -> NO es maximal.\
""",
        "pregunta": "¿Cuál es la diferencia entre una clique MAXIMAL y una clique MAXIMUM?",
        "opciones": [
            "Son sinonimos: ambas son la clique mas grande del grafo",
            "Maximal = no puede crecer (ningún externo conecta con todos). Maximum = la mas grande del grafo",
            "Maximal = tiene tamano par. Maximum = tiene tamano impar",
            "Maximal = contiene al vertice A. Maximum = no contiene al vertice A",
        ],
        "correcta": 1,
        "explicacion": """\
  MAXIMAL = no se puede ampliar.
  MAXIMUM = la mas grande de todo el grafo.

  Toda maximum ES maximal. Pero una maximal puede ser pequena.
  Ejemplo: {A,E,F} es maximal (no puede crecer) pero NO es maximum (solo 3 miembros).\
""",
    },

    {
        "punto": 2, "nivel": "Basico",
        "tema" : "P2.3 — Cuantas maximal cliques tiene el grafo del paper",
        "teoria": """\
  CONTINUANDO: sabes que es una maximal clique y como verificarla.
  Ahora la pregunta natural es: ¿cuantas hay en el grafo del paper?

  Para encontrarlas TODAS, hay que comprobar todos los posibles grupos.
  El algoritmo Bron-Kerbosch (que estudiaremos en el Punto 3) lo hace
  de forma sistematica. Pero para el grafo pequeno del paper podemos
  buscarlas manualmente.

  Candidatas a maximal clique (cliques que no pueden crecer):
    {A,B,C,D}: externos E y F no pueden entrar (B-E y B-F no existen) -> MAXIMAL ✓
    {A,E,F}:   externos B,C,D no pueden entrar (B-E, C-E, D-E no existen) -> MAXIMAL ✓
    {A,B,C}:   D puede entrar (D-A ✓, D-B ✓, D-C ✓) -> NO maximal.
    {B,C,D}:   A puede entrar (A-B ✓, A-C ✓, A-D ✓) -> NO maximal.
    {A,B}:     C puede entrar -> NO maximal.

  Resultado: hay EXACTAMENTE 2 maximal cliques en el grafo del paper.
  El objetivo del paper (MCE) es encontrar esas 2 de forma eficiente.\
""",
        "pregunta": "¿Cuantas maximal cliques tiene el grafo del paper y cuales son?",
        "opciones": [
            "4 maximal cliques: {A,B,C,D}, {A,E,F}, {B,C,D} y {A,B,C}",
            "1 maximal clique: {A,B,C,D} porque es la mas grande",
            "2 maximal cliques: {A,B,C,D} y {A,E,F}",
            "3 maximal cliques: {A,B,C,D}, {A,E,F} y {A,B,C}",
        ],
        "correcta": 2,
        "explicacion": """\
  Hay exactamente 2 maximal cliques:
    {A,B,C,D}: no puede crecer (E y F no conectan con todos).
    {A,E,F}:   no puede crecer (B, C, D no conectan con E ni F).

  {B,C,D} no es maximal (A puede entrar).
  {A,B,C} no es maximal (D puede entrar).
  MCE = encontrar estas 2 de forma automatica y eficiente.\
""",
    },

    {
        "punto": 2, "nivel": "Medio",
        "tema" : "P2.4 — Verificar paso a paso que {A,E,F} es maximal",
        "teoria": """\
  CONTINUANDO: ya sabes que {A,E,F} es una de las 2 maximal cliques.
  Ahora vamos a VERIFICARLO paso a paso para fijar el metodo.

  Paso 1: ¿Es clique?
    A-E existe ✓   A-F existe ✓   E-F existe ✓
    -> SÍ es clique.

  Paso 2: ¿Puede crecer? (vertices fuera: B, C, D)
    ¿B conecta con TODOS {A,E,F}?
      B-A ✓   B-E ✗ (no existe)  -> B NO puede entrar.
    ¿C conecta con TODOS {A,E,F}?
      C-A ✓   C-E ✗ (no existe)  -> C NO puede entrar.
    ¿D conecta con TODOS {A,E,F}?
      D-A ✓   D-E ✗ (no existe)  -> D NO puede entrar.

  Nadie puede entrar -> {A,E,F} SI es maximal clique.

  Clave: E y F actuan como "barrera" que impide que B, C y D entren,
  porque B, C y D no conocen a E ni a F.\
""",
        "pregunta": "¿Por que {A, E, F} SI es una maximal clique en el grafo del paper?",
        "opciones": [
            "Porque {A,E,F} tiene 3 miembros y todas las cliques de 3 son maximal",
            "Porque es una clique (A-E, A-F y E-F existen) y ninguno de los vertices externos B, C, D conecta con E ni con F",
            "Porque A es el vertice central y cualquier clique que contenga a A es maximal",
            "Porque {A,E,F} es la segunda clique mas grande y eso la hace maximal",
        ],
        "correcta": 1,
        "explicacion": """\
  {A,E,F} es clique: A-E ✓, A-F ✓, E-F ✓.
  Es maximal porque B, C y D no pueden entrar:
    B-E no existe, C-E no existe, D-E no existe.
  Ningún externo conecta con TODOS los miembros -> no puede crecer -> maximal.\
""",
    },

    {
        "punto": 2, "nivel": "Medio",
        "tema" : "P2.5 — Por que {B,C,D} no es maximal y k-cliques",
        "teoria": """\
  CONTINUANDO: ya verificaste maximal cliques concretas.
  Ahora combinamos con el concepto de K-CLIQUE.

  K-CLIQUE = clique de EXACTAMENTE k vertices.
    3-clique = {A,E,F}   (k=3, triangulo)
    4-clique = {A,B,C,D} (k=4)
    2-clique = {A,B}     (k=2, una sola arista)

  Clique maximal vs k-clique: son conceptos ortogonales.
    Una 4-clique puede ser maximal o no.
    Una 3-clique puede ser maximal o no.

  Ejemplo de 3-clique NO maximal en el paper:
    {B,C,D} es una 3-clique (k=3): B-C ✓, B-D ✓, C-D ✓.
    Pero A puede unirse: A-B ✓, A-C ✓, A-D ✓.
    -> {B,C,D} es una 3-clique pero NO es maximal.
    -> Si le anades A, se convierte en la 4-clique maximal {A,B,C,D}.\
""",
        "pregunta": "¿Por que {B,C,D} es una 3-clique pero NO es una maximal clique?",
        "opciones": [
            "Porque una clique de 3 vertices nunca puede ser maximal en ningun grafo",
            "Porque {B,C,D} no cumple la condicion de clique: la arista C-D no existe",
            "Porque A esta conectado con B, C y D, por lo que A puede unirse -> la clique puede crecer",
            "Porque E esta conectado con A y eso impide que {B,C,D} sea maximal",
        ],
        "correcta": 2,
        "explicacion": """\
  {B,C,D} SÍ es una 3-clique: B-C ✓, B-D ✓, C-D ✓.
  Pero NO es maximal porque A puede unirse:
    A-B ✓   A-C ✓   A-D ✓  ->  A conecta con todos -> puede entrar.
  La clique crece a {A,B,C,D} que SI es maximal.\
""",
    },

    {
        "punto": 2, "nivel": "Medio",
        "tema" : "P2.6 — Por que A aparece en todas las maximal cliques",
        "teoria": """\
  CONTINUANDO: ahora que conoces las 2 maximal cliques {A,B,C,D} y {A,E,F},
  observa algo curioso: el vertice A aparece EN AMBAS.

  ¿Por que ocurre esto?

  A tiene grado Δ=5 (conecta con TODOS los demas vertices).
  Cualquier subconjunto de vertices SIN A puede ser ampliado
  con A porque A conecta con todos.
  Por tanto, ningun subconjunto que no incluya a A puede ser
  maximal, porque A siempre podria unirse.

  Excepcion: si el subconjunto incluye a algun vertice que no
  conecta con A... pero en este grafo A conecta con todos.

  Conclusion:
    En este grafo, TODA maximal clique debe contener a A.
    A es el "nexo" que conecta los dos grupos {B,C,D} y {E,F}.

  Aplicacion real: en redes de proteinas, un vertice como A
  representa una proteina "hub" que interactua con muchas otras.\
""",
        "pregunta": "¿Por que el vertice A aparece en TODAS las maximal cliques del grafo del paper?",
        "opciones": [
            "Porque A tiene el grado maximo y los vertices con mas grado siempre aparecen en todas las cliques",
            "Porque A conecta con TODOS los demas vertices (grado=5=Δ), por lo que cualquier grupo sin A podria siempre ampliarse anadiendo A",
            "Porque el algoritmo BK siempre empieza por el vertice A al ser el primero del alfabeto",
            "Porque A fue el primer vertice anadido al grafo y por tanto forma parte de todas las estructuras",
        ],
        "correcta": 1,
        "explicacion": """\
  A tiene grado 5 = Δ, conecta con todos los demas vertices.
  Si tienes cualquier clique sin A:
    A-B ✓, A-C ✓, A-D ✓, A-E ✓, A-F ✓ -> A siempre puede unirse.
  Por tanto ningun grupo sin A puede ser maximal en este grafo.
  A es el "hub" (vertice central) que aparece en todas las maximal cliques.\
""",
    },

    # ╔══════════════════════════════╗
    # ║  PUNTO 3 — Bron-Kerbosch    ║
    # ╚══════════════════════════════╝

    {
        "punto": 3, "nivel": "Basico",
        "tema" : "P3.1 — Los tres conjuntos R, P y X del algoritmo BK",
        "teoria": """\
  AHORA QUE SABES QUE SON LAS MAXIMAL CLIQUES, el algoritmo BK
  es el metodo sistematico para encontrarlas TODAS.

  BK = Bron-Kerbosch (apellidos de sus autores, 1973).
  RECURSIVO = la funcion se llama a si misma con datos mas pequenos.

  En cada llamada recursiva, BK mantiene TRES conjuntos:

  R = "Running clique" = la clique que construimos AHORA.
      Empieza vacio {}. Crece cuando anadimos un vertice.

  P = "Prospective" = CANDIDATOS que podrian entrar en la clique.
      Condicion: deben conectar con TODOS los de R.
      Empieza con TODOS los vertices del grafo.

  X = "eXcluded" = ya explorados. No se repiten para no
      encontrar la misma clique dos veces. Empieza vacio {}.

  PARADA: P={} y X={} al mismo tiempo -> R es MAXIMAL CLIQUE.\
""",
        "pregunta": "En el algoritmo BK, ¿que representa cada conjunto y como empieza cada uno?",
        "opciones": [
            "R = resultado,     P = parametros,  X = extras.      Todos empiezan llenos.",
            "R = clique actual, P = candidatos,  X = excluidos.   R={}, P=todos, X={}.",
            "R = raiz,          P = profundidad, X = extremos.    R=todos, P={}, X={}.",
            "R = rechazados,    P = pivote,      X = extras.      Todos empiezan vacios.",
        ],
        "correcta": 1,
        "explicacion": """\
  R = "Running clique"  -> empieza vacio {}, se va llenando.
  P = "Prospective"     -> empieza con TODOS los vertices.
  X = "eXcluded"        -> empieza vacio {}.
  Parada: P={} y X={} -> R es maximal clique.\
""",
    },

    {
        "punto": 3, "nivel": "Basico",
        "tema" : "P3.2 — Condicion de parada: P vacio pero X no vacio",
        "teoria": """\
  CONTINUANDO: la condicion de parada es P={} y X={} SIMULTANEAMENTE.
  ¿Que pasa si P={} pero X≠{}? Esto es un caso diferente y muy importante.

  Si P={} pero X≠{}: R NO se reporta como maximal clique.
  ¿Por que? Porque algun vertice de X (que ya fue explorado antes)
  podria estar conectado con todos los de R.
  Eso significaria que R ya fue encontrado como SUBCONJUNTO de una
  clique mas grande en una iteracion anterior.
  -> R no es maximal (ya fue "superado").

  Resumen de los tres casos posibles al final de una llamada BK:
  ┌─────────────┬─────────────┬─────────────────────────────────────────┐
  │      P      │      X      │  Que ocurre                             │
  ├─────────────┼─────────────┼─────────────────────────────────────────┤
  │    vacio    │    vacio    │  R es MAXIMAL CLIQUE -> REPORTAR         │
  │    vacio    │  no vacio   │  R no es maximal -> NO reportar          │
  │  no vacio   │  cualquiera │  Seguir explorando (recursion normal)   │
  └─────────────┴─────────────┴─────────────────────────────────────────┘\
""",
        "pregunta": "En BK, si P={} pero X={A,B} (no vacio), ¿que significa y que hace el algoritmo?",
        "opciones": [
            "R es una maximal clique y se reporta. X indica que ya fue verificada.",
            "El algoritmo ha terminado y reporta R como resultado final.",
            "R NO es maximal: algun vertice de X podria extenderla (ya fue superada antes). No se reporta.",
            "El algoritmo reinicia desde el principio con un nuevo conjunto P.",
        ],
        "correcta": 2,
        "explicacion": """\
  P={} pero X≠{}: R NO es maximal clique y no se reporta.
  Razon: los vertices de X ya fueron explorados ANTES en este nivel.
  Si algun vertice de X conecta con todos los de R, entonces R
  fue encontrado como subconjunto de una clique mayor en una rama anterior.
  Solo se reporta cuando P={} Y X={} al mismo tiempo.\
""",
    },

    {
        "punto": 3, "nivel": "Medio",
        "tema" : "P3.3 — Recursion de BK sin pivote: nuevos P y X",
        "teoria": """\
  CONTINUANDO: sabes cuando parar. Ahora veamos como AVANZAR.

  En cada llamada, tomamos un vertice v de P y llamamos recursivamente.
  Los nuevos conjuntos para esa llamada son:

    Nuevo R = R  union  {v}              <- v entra en la clique
    Nuevo P = P  interseccion  N(v)      <- solo candidatos vecinos de v
    Nuevo X = X  interseccion  N(v)      <- solo excluidos vecinos de v

  union        = A union B        = todo lo que esta en A o en B.
  interseccion = A interseccion B = solo lo que esta en AMBOS.
  N(v)         = vecinos de v en el grafo original.

  ¿Por que P interseccion N(v)?
    Si v entra en la clique (R), los futuros miembros deben conectar con v.
    Solo los vecinos de v siguen siendo candidatos validos.

  Despues de explorar la rama de v:
    P = P - {v}   (v ya fue explorado, sale de candidatos)
    X = X union {v}   (v pasa a excluidos)\
""",
        "pregunta": "Al explorar v=B con R={A}, P={B,C,D}, X={E,F}, ¿cuales son los nuevos R, P, X?",
        "opciones": [
            "Nuevo R={A,B},  Nuevo P={C,D} interseccion N(B)={A,C,D} = {C,D},  Nuevo X={E,F} interseccion N(B) = {}",
            "Nuevo R={A,B},  Nuevo P={C,D},  Nuevo X={E,F,B}",
            "Nuevo R={B},    Nuevo P={A,C,D} - {B} = {A,C,D},  Nuevo X={}",
            "Nuevo R={A,B},  Nuevo P={A,B,C,D} interseccion N(B),  Nuevo X={}",
        ],
        "correcta": 0,
        "explicacion": """\
  v=B, N(B) = {A,C,D}.
  Nuevo R = {A} union {B} = {A,B}.
  Nuevo P = {B,C,D} interseccion {A,C,D} = {C,D}.
  Nuevo X = {E,F} interseccion {A,C,D} = {} (ni E ni F estan en N(B)).

  Siguiente paso: BK({A,B}, {C,D}, {}).
  Desde ahi se encontrara la clique {A,B,C,D}.\
""",
    },

    {
        "punto": 3, "nivel": "Medio",
        "tema" : "P3.4 — BK con pivote: como se elige el pivote",
        "teoria": """\
  CONTINUANDO: ya sabes la recursion basica.
  Ahora la MEJORA del pivote que reduce el numero de ramas.

  Sin pivote: en cada nivel se itera sobre TODOS los vertices de P.
  Con pivote: elegimos un vertice especial u (el PIVOTE) y solo
              iteramos sobre P - N(u) (los NO vecinos del pivote).

  ELECCION DEL PIVOTE u:
    u se toma de P union X (puede ser de cualquiera de los dos).
    Criterio: el que tenga MAS vecinos dentro de P.
    Esto maximiza la poda (menos vertices a iterar).

  RAZON POR LA QUE FUNCIONA:
    Cualquier maximal clique que CONTENGA a u se encontrara
    cuando u sea el candidato v en su propia iteracion.
    Las cliques SIN u deben tener algun no-vecino de u.
    Esos no-vecinos son exactamente P - N(u).
    -> Solo hay que iterar sobre P - N(u).\
""",
        "pregunta": "Con R={}, P={A,B,C,D,E,F}, X={}, ¿cual es el pivote correcto y sobre que vertices se itera?",
        "opciones": [
            "Pivote=E (2 vecinos en P). Iterar sobre P-N(E)={B,C,D,F} = 4 vertices.",
            "Pivote=A (5 vecinos en P, el maximo). Iterar sobre P-N(A)={A} = 1 vertice.",
            "Pivote=B (3 vecinos en P). Iterar sobre P-N(B)={A,E,F} = 3 vertices.",
            "Pivote=F (2 vecinos en P). Iterar sobre P-N(F)={B,C,D,A} = 4 vertices.",
        ],
        "correcta": 1,
        "explicacion": """\
  Calculamos |N(v) interseccion P| para cada v:
    A:5, B:3, C:3, D:3, E:2, F:2  ->  maximo es A con 5.
  Pivote = A.
  P - N(A) = {A,B,C,D,E,F} - {B,C,D,E,F} = {A}.
  Solo 1 iteracion en vez de 6. Poda maxima en este nivel.\
""",
    },

    {
        "punto": 3, "nivel": "Medio",
        "tema" : "P3.5 — BK con degeneracy ordering: inicializacion",
        "teoria": """\
  CONTINUANDO: ya dominas BK con y sin pivote para el grafo completo.
  Ahora combinamos con el degeneracy ordering (que veremos en detalle en P4).

  BK CON DEGENERACY ORDERING:
  En vez de una llamada con P=todos los vertices, se hacen N llamadas,
  una por cada vertice v del ordering.
  Para cada vertice v en el ordering (posicion i):

    R = {v}                              (v ya esta en la clique)
    P = N(v) interseccion {vertices tras v en el ordering}
        = vecinos de v que van DESPUES en el orden
    X = N(v) interseccion {vertices antes de v en el ordering}
        = vecinos de v que van ANTES en el orden

  Con ordering [E, F, A, B, C, D]:
  Llamada para v=A (posicion 2):
    R = {A}
    P = N(A) interseccion {B,C,D} = {B,C,D}    (los que van tras A)
    X = N(A) interseccion {E,F}   = {E,F}       (los que van antes de A)\
""",
        "pregunta": "Con ordering [E,F,A,B,C,D], ¿como se inicializa la llamada BK para el vertice B (posicion 3)?",
        "opciones": [
            "R={B},  P=N(B)={A,C,D},  X={}",
            "R={B},  P=N(B) interseccion {C,D} = {C,D},  X=N(B) interseccion {E,F,A} = {A}",
            "R={},   P={C,D},          X={A,E,F}",
            "R={B},  P={A,C,D},        X={A,E,F}",
        ],
        "correcta": 1,
        "explicacion": """\
  B esta en posicion 3 en el ordering [E,F,A,B,C,D].
    Vertices ANTES de B (pos 0,1,2) = {E, F, A}
    Vertices DESPUES de B (pos 4,5) = {C, D}

  R = {B}.
  P = N(B) interseccion {C,D} = {A,C,D} interseccion {C,D} = {C,D}.
  X = N(B) interseccion {E,F,A} = {A,C,D} interseccion {E,F,A} = {A}.\
""",
    },

    {
        "punto": 3, "nivel": "Avanzado",
        "tema" : "P3.6 — Trazar BK completo desde R={A}, P={B,C,D}, X={E,F}",
        "teoria": """\
  CONTINUANDO: sabes la inicializacion para cada vertice.
  Ahora trazamos la llamada de A HASTA ENCONTRAR la clique {A,B,C,D}.

  Llamada inicial para A: BK({A}, {B,C,D}, {E,F})
    Pivote: u de {B,C,D} union {E,F} con max vecinos en P={B,C,D}.
      N(B) inter P = {C,D} -> 2.  N(C) inter P = {B,D} -> 2.
      N(D) inter P = {B,C} -> 2.  N(E) inter P = {} -> 0.
      Empate en 2, desempate alfabetico -> u=B.
    Iterar sobre P - N(B) = {B,C,D} - {A,C,D} = {B}.
    Solo v=B.

  BK({A,B}, P interseccion N(B), X interseccion N(B))
    = BK({A,B}, {B,C,D} inter {A,C,D}, {E,F} inter {A,C,D})
    = BK({A,B}, {C,D}, {})
    ... (en esta llamada se encontrara {A,B,C,D})

  La clique {A,B,C,D} se encuentra cuando desde BK({A,B},{C,D},{})
  se anade C y luego D: BK({A,B,C,D},{},{}) -> MAXIMAL!\
""",
        "pregunta": "Siguiendo la traza de BK con pivote para la llamada BK({A},{B,C,D},{E,F}), ¿cual es el primer vertice que se anade a R tras A, y por que?",
        "opciones": [
            "Se anade E, porque E esta en X y tiene prioridad.",
            "Se anade B, porque el pivote u=B tiene los mas vecinos en P (2) con desempate alfabetico, y P-N(B)={B}.",
            "Se anade C, porque C es el primer vertice de P en orden alfabetico y no hay pivote.",
            "Se anade D, porque D tiene el menor grado en el subgrafo inducido.",
        ],
        "correcta": 1,
        "explicacion": """\
  Con pivote: u = B (max vecinos en P, desempate alfabetico).
  Iterar sobre P - N(B) = {B,C,D} - {A,C,D} = {B}.
  Solo hay que probar v=B -> Nuevo R = {A,B}.
  Desde BK({A,B},{C,D},{}) se llegara a la clique {A,B,C,D}.\
""",
    },

    {
        "punto": 3, "nivel": "Avanzado",
        "tema" : "P3.7 — Comparar llamadas recursivas con y sin pivote",
        "teoria": """\
  CONTINUANDO: has trazado la ejecucion con pivote.
  Ahora cuantificamos la diferencia.

  SIN pivote — llamada BK({}, {A,B,C,D,E,F}, {}):
    Itera sobre los 6 vertices de P.
    Genera 6 ramas en el nivel 0.
    En niveles inferiores, cada rama genera mas sub-ramas.
    Total de llamadas recursivas: mayor.

  CON pivote — misma llamada inicial:
    Pivote = A (5 vecinos en P).
    Itera sobre P - N(A) = {A} -> solo 1 rama en nivel 0.
    Total de llamadas recursivas: mucho menor.

  En el grafo del paper:
    Sin pivote: ~30+ llamadas recursivas.
    Con pivote: ~15 llamadas recursivas.
    Ahorro aproximado: 50%.

  En grafos GRANDES (miles de vertices):
    El ahorro puede ser de 90-99% de las llamadas.
    El pivote es ESENCIAL para que el algoritmo sea practico.\
""",
        "pregunta": "¿Por que el pivote es ESENCIAL (no solo util) en grafos grandes?",
        "opciones": [
            "Porque sin pivote el algoritmo no encuentra todas las cliques, solo algunas.",
            "Porque en grafos grandes el numero de ramas sin pivote crece exponencialmente, haciendo el calculo imposible en tiempo razonable.",
            "Porque el pivote reduce el uso de memoria de R, que en grafos grandes ocuparia demasiado espacio.",
            "Porque sin pivote el algoritmo BK no termina nunca (entra en bucle infinito).",
        ],
        "correcta": 1,
        "explicacion": """\
  Sin pivote, el numero de ramas crece EXPONENCIALMENTE con el tamano del grafo.
  En grafos con miles de vertices, explorar todas las ramas sin poda es imposible
  en cualquier tiempo razonable (dias, años, siglos).

  Con pivote, se podan la mayoria de las ramas manteniendo el mismo resultado.
  El pivote NO cambia las cliques encontradas, solo reduce el trabajo.\
""",
    },

    # ╔══════════════════════════════════╗
    # ║  PUNTO 4 — Degeneracy ordering  ║
    # ╚══════════════════════════════════╝

    {
        "punto": 4, "nivel": "Basico",
        "tema" : "P4.1 — Para que sirve el degeneracy ordering",
        "teoria": """\
  AHORA QUE DOMINAS BK, veamos como mejorarlo con el ordering.

  SIN ordering (orden alfabetico A,B,C,D,E,F):
    Al procesar A, P = N(A) = {B,C,D,E,F} = 5 elementos.
    El algoritmo tiene 5 ramas desde el inicio.

  CON degeneracy ordering:
    Se reordenan los vertices para que cada uno tenga el MENOR
    numero posible de vecinos "hacia adelante" en el orden.
    "Hacia adelante" = los que aparecen DESPUES en el ordering.
    Esos vecinos forman el conjunto P cuando se procesa ese vertice.

  d = DEGENERACY = el maximo de vecinos hacia adelante de cualquier vertice.
  Con ordering: P <= d para todos los vertices.
  Sin ordering: P <= Δ para todos los vertices.

  Como d <= Δ siempre (y normalmente d << Δ):
    Con ordering, P es mas pequeno -> menos trabajo -> mas rapido.\
""",
        "pregunta": "¿Cual es el beneficio principal del degeneracy ordering en el algoritmo BK?",
        "opciones": [
            "Encuentra mas maximal cliques que sin ordering.",
            "Reduce el tamano del conjunto P: con ordering P <= d en vez de P <= Δ.",
            "Elimina los vertices del grafo que no pertenecen a ninguna clique.",
            "Hace que el algoritmo BK no necesite el conjunto X.",
        ],
        "correcta": 1,
        "explicacion": """\
  El ordering reduce P de O(Δ) a O(d).
  Sin ordering: P de A = {B,C,D,E,F} = 5 elementos.
  Con ordering [E,F,A,B,C,D]: P de A = {B,C,D} = 3 elementos.
  Mismas cliques encontradas, menos trabajo.\
""",
    },

    {
        "punto": 4, "nivel": "Medio",
        "tema" : "P4.2 — Paso 1 del ordering: eliminar E y actualizar grados",
        "teoria": """\
  CONTINUANDO: vamos a ejecutar el algoritmo paso a paso.
  Te ayudo con el primer paso para que practiques el segundo.

  Grados INICIALES del grafo del paper:
    A=5,  B=3,  C=3,  D=3,  E=2,  F=2

  Algoritmo: eliminar el vertice de MENOR grado actual.
  Empate -> orden ALFABETICO.

  PASO 1:
    Minimo grado = 2.  Tienen grado 2: E y F.  Empate -> E (alfabetico).
    Elegido: E.  Ordering hasta ahora: [E]

    Actualizar grados: los vecinos de E pierden 1.
    N(E) = {A, F}
      A: 5 - 1 = 4
      F: 2 - 1 = 1

  Grados DESPUES del paso 1 (E ya no existe):
    A=4,  B=3,  C=3,  D=3,  F=1\
""",
        "pregunta": "Despues de eliminar E en el paso 1, ¿cuales son los grados actualizados y quien se elige en el paso 2?",
        "opciones": [
            "Grados: A=5,B=3,C=3,D=3,F=2. Se elige F (grado min=2).",
            "Grados: A=4,B=3,C=3,D=3,F=1. Se elige F (unico con grado min=1).",
            "Grados: A=4,B=2,C=2,D=2,F=1. Se elige F (grado min=1).",
            "Grados: A=4,B=3,C=3,D=3,F=2. Se elige B (grado min=3, alfabetico).",
        ],
        "correcta": 1,
        "explicacion": """\
  N(E) = {A, F}. Al eliminar E:
    A pierde 1 vecino: 5-1=4.
    F pierde 1 vecino: 2-1=1.
    B, C, D no cambian (no eran vecinos de E).

  Grados tras paso 1: A=4, B=3, C=3, D=3, F=1.
  Paso 2: minimo grado=1, solo F -> se elige F.
  Ordering: [E, F].\
""",
    },

    {
        "punto": 4, "nivel": "Medio",
        "tema" : "P4.3 — Ordering completo y desempate alfabetico",
        "teoria": """\
  CONTINUANDO: ya calculaste los pasos 1 y 2 ([E, F]).
  Sigamos con los pasos 3-6.

  Tras eliminar E y F, el grafo restante tiene {A,B,C,D} con:
    Aristas: A-B, A-C, A-D, B-C, B-D, C-D
    Grados:  A=3, B=3, C=3, D=3

  PASO 3: minimo grado=3, empate entre A,B,C,D -> alfabetico -> A.
    Ordering: [E, F, A]
    N(A) en {B,C,D} = {B,C,D}. Al eliminar A: B=2, C=2, D=2.

  PASO 4: minimo grado=2, empate B,C,D -> B.
    Ordering: [E, F, A, B]
    N(B) en {C,D} = {C,D}. Al eliminar B: C=1, D=1.

  PASO 5: minimo grado=1, empate C,D -> C.
    Ordering: [E, F, A, B, C]

  PASO 6: solo queda D.
    Ordering: [E, F, A, B, C, D]  <- RESULTADO FINAL\
""",
        "pregunta": "¿Cual es el degeneracy ordering completo del grafo del paper con desempate alfabetico?",
        "opciones": [
            "[ A, B, C, D, E, F ]   orden alfabetico directo",
            "[ F, E, D, C, B, A ]   orden alfabetico inverso",
            "[ E, F, A, B, C, D ]   minimo grado iterativo con desempate alfabetico",
            "[ D, C, B, A, F, E ]   maximo grado iterativo con desempate alfabetico",
        ],
        "correcta": 2,
        "explicacion": """\
  Paso 1: E (grado 2, empate con F, E<F alfabetico).
  Paso 2: F (grado 1 tras perder a E).
  Paso 3: A (grado 3, empate con B,C,D, A es el primero).
  Paso 4: B (grado 2, empate con C,D).
  Paso 5: C (grado 1, empate con D).
  Paso 6: D.
  Ordering: [E, F, A, B, C, D].\
""",
    },

    {
        "punto": 4, "nivel": "Avanzado",
        "tema" : "P4.4 — Calcular d: vecinos hacia adelante de cada vertice",
        "teoria": """\
  CONTINUANDO: tienes el ordering [E,F,A,B,C,D].
  Ahora calcula d (degeneracy) contando vecinos hacia adelante.

  VECINOS HACIA ADELANTE de v = vecinos de v que aparecen en
  posiciones POSTERIORES a v en el ordering.

  Posiciones: E=0, F=1, A=2, B=3, C=4, D=5.

  Para cada vertice:
    E(pos 0): N(E)={A,F}. Estan tras E: F(1)✓, A(2)✓. -> 2 vecinos adelante.
    F(pos 1): N(F)={A,E}. Estan tras F: A(2)✓, E(0)✗. -> 1 vecino adelante.
    A(pos 2): N(A)={B,C,D,E,F}. Tras A: B(3)✓,C(4)✓,D(5)✓,E(0)✗,F(1)✗. -> 3.
    B(pos 3): N(B)={A,C,D}. Tras B: C(4)✓,D(5)✓,A(2)✗. -> 2 vecinos adelante.
    C(pos 4): N(C)={A,B,D}. Tras C: D(5)✓,A(2)✗,B(3)✗. -> 1 vecino adelante.
    D(pos 5): N(D)={A,B,C}. Tras D: ninguno (es el ultimo). -> 0.

  d = maximo = max(2,1,3,2,1,0) = 3. Lo alcanza A (vecinos adelante: B,C,D).\
""",
        "pregunta": "¿Cuanto vale d (degeneracy) para el grafo del paper y que vertice lo determina?",
        "opciones": [
            "d=5, lo alcanza E porque tiene el mayor numero de vecinos en total",
            "d=2, lo alcanza E con vecinos hacia adelante {F,A}",
            "d=3, lo alcanza A (posicion 2) con vecinos hacia adelante {B,C,D}",
            "d=4, lo alcanza A porque tiene 4 vecinos que van antes de el en el ordering",
        ],
        "correcta": 2,
        "explicacion": """\
  Vecinos hacia adelante: E->2, F->1, A->3, B->2, C->1, D->0.
  d = max = 3.  Lo alcanza A con vecinos hacia adelante {B,C,D}.

  Con ordering: P tiene como maximo d=3 elementos (en vez de Δ=5 sin ordering).
  Δ=5, d=3 -> mejora del 40% en el tamano de P.\
""",
    },

    {
        "punto": 4, "nivel": "Avanzado",
        "tema" : "P4.5 — Vecinos hacia atras (X inicial) de cada vertice",
        "teoria": """\
  CONTINUANDO: ya calculaste los vecinos hacia adelante (forman P).
  Los VECINOS HACIA ATRAS forman X en la llamada inicial de BK.

  VECINOS HACIA ATRAS de v = vecinos de v que aparecen en
  posiciones ANTERIORES a v en el ordering.

  Con ordering [E(0),F(1),A(2),B(3),C(4),D(5)]:
    E(pos 0): ningun vecino anterior (es el primero). X={}.
    F(pos 1): N(F)={A,E}. Anteriores: E(0)✓. -> X={E}.
    A(pos 2): N(A)={B,C,D,E,F}. Anteriores: E(0)✓,F(1)✓. -> X={E,F}.
    B(pos 3): N(B)={A,C,D}. Anteriores: A(2)✓. -> X={A}.
    C(pos 4): N(C)={A,B,D}. Anteriores: A(2)✓,B(3)✓. -> X={A,B}.
    D(pos 5): N(D)={A,B,C}. Anteriores: A(2)✓,B(3)✓,C(4)✓. -> X={A,B,C}.

  Observacion:
    P (vecinos adelante): va de 2,1,3,2,1,0 -> acotado por d=3.
    X (vecinos atras):    va de 0,1,2,1,2,3 -> puede llegar hasta Δ=5
    -> X NO mejora con el ordering (sigue siendo O(Δ) en el peor caso).\
""",
        "pregunta": "¿Cuales son los vecinos hacia atras (X inicial) de C (posicion 4) en el ordering [E,F,A,B,C,D]?",
        "opciones": [
            "X={D}  porque D es el unico vertice que va despues de C",
            "X={A,B,C}  incluyendo al propio C",
            "X={A,B}  porque A(pos 2) y B(pos 3) son vecinos de C y van antes que C",
            "X={}  porque C no tiene vecinos anteriores en el ordering",
        ],
        "correcta": 2,
        "explicacion": """\
  C esta en posicion 4. Sus vecinos son N(C) = {A,B,D}.
  Vertices que van ANTES de C en el ordering (posiciones 0,1,2,3) = {E,F,A,B}.
  N(C) interseccion {E,F,A,B} = {A,B}.
  -> X inicial de C = {A,B}.

  D va DESPUES (posicion 5), por eso D forma parte de P, no de X.\
""",
    },

    {
        "punto": 4, "nivel": "Avanzado",
        "tema" : "P4.6 — Por que P mejora con ordering pero X no mejora",
        "teoria": """\
  CONTINUANDO: ahora entiendes P y X para cada vertice.
  Esta pregunta es la MAS IMPORTANTE del punto 4.

  RESUMEN de P y X con ordering [E,F,A,B,C,D]:
  ┌─────────┬──────┬─────────────────────┬───┬───────────────────────┬───┐
  │ Vertice │ Pos. │ P (vecinos adelante) │|P|│ X (vecinos atras)     │|X|│
  ├─────────┼──────┼─────────────────────┼───┼───────────────────────┼───┤
  │ E       │  0   │ {F,A}               │ 2 │ {}                    │ 0 │
  │ F       │  1   │ {A}                 │ 1 │ {E}                   │ 1 │
  │ A       │  2   │ {B,C,D}             │ 3 │ {E,F}                 │ 2 │
  │ B       │  3   │ {C,D}               │ 2 │ {A}                   │ 1 │
  │ C       │  4   │ {D}                 │ 1 │ {A,B}                 │ 2 │
  │ D       │  5   │ {}                  │ 0 │ {A,B,C}               │ 3 │
  └─────────┴──────┴─────────────────────┴───┴───────────────────────┴───┘

  P maximo = 3 (acotado por d=3) -> O(d)   <- MEJORA con ordering.
  X maximo = 3 (puede llegar a Δ=5 en grafos mas grandes) -> O(Δ) <- NO mejora.

  Por que X no mejora:
    X = vecinos hacia ATRAS. Cuanto mas tarde aparece un vertice
    en el ordering, mas vecinos ya procesados tiene -> X crece.
    No hay garantia de que X sea pequeno.\\
""",
        "pregunta": "¿Por que con degeneracy ordering P mejora a O(d) pero X sigue siendo O(Δ)?",
        "opciones": [
            "Porque el algoritmo solo aplica el ordering a P, no a X.",
            "Porque P contiene vecinos hacia adelante (acotados por d por definicion de degeneracy), mientras X contiene vecinos hacia atras que pueden ser hasta Δ.",
            "Porque X siempre empieza vacio y nunca supera el tamano de P.",
            "Porque d y Δ son iguales para X, asi que no hay diferencia.",
        ],
        "correcta": 1,
        "explicacion": """\
  P = vecinos hacia ADELANTE: por definicion de degeneracy, son como maximo d. -> O(d).
  X = vecinos hacia ATRAS: un vertice puede tener hasta Δ vecinos anteriores. -> O(Δ).

  El ordering GARANTIZA que P <= d. No garantiza nada sobre X.
  Este es el motivo por el que el paper propone una representacion
  especial para X (dividiendolo en X_P y X_X).\
""",
    },

    # ╔══════════════════════════════╗
    # ║  PUNTO 5 — BFS vs DFS       ║
    # ╚══════════════════════════════╝

    {
        "punto": 5, "nivel": "Basico",
        "tema" : "P5.1 — Que son DFS y BFS",
        "teoria": """\
  EL ARBOL DE BUSQUEDA Y COMO RECORRERLO
  ────────────────────────────────────────
  El algoritmo BK genera un ARBOL DE BUSQUEDA.
  Cada NODO del arbol = una llamada al algoritmo con R,P,X.
  Las HOJAS = nodos donde P=X={} (maximal cliques encontradas).

  Dos formas de recorrer ese arbol:

  DFS = "Depth-First Search" = BUSQUEDA EN PROFUNDIDAD
    Baja por una rama COMPLETA hasta la hoja, luego vuelve
    y baja por la siguiente.
    Analogia: leer un libro capitulo a capitulo (completo cada uno).
    MEMORIA: solo guarda el CAMINO ACTUAL = O(profundidad).

  BFS = "Breadth-First Search" = BUSQUEDA EN ANCHURA
    Procesa TODOS los nodos de un nivel antes de bajar al siguiente.
    Analogia: limpiar el suelo fila por fila.
    MEMORIA: guarda TODOS los nodos del nivel actual = puede explotar.\
""",
        "pregunta": "¿Como recorre el arbol DFS y como lo recorre BFS?",
        "opciones": [
            "DFS procesa nivel por nivel. BFS baja por ramas completas.",
            "DFS baja por ramas completas hasta las hojas. BFS procesa todos los nodos de un nivel antes de bajar.",
            "DFS y BFS son identicos pero DFS empieza por la izquierda y BFS por la derecha.",
            "DFS va de hojas a raiz. BFS va de raiz a hojas de forma aleatoria.",
        ],
        "correcta": 1,
        "explicacion": """\
  DFS (profundidad): rama completa hasta hoja, luego siguiente rama.
  Memoria = O(profundidad).

  BFS (anchura): todo el nivel antes de bajar.
  Memoria = O(nodos en el nivel mas ancho) = puede ser exponencial.\
""",
    },

    {
        "punto": 5, "nivel": "Medio",
        "tema" : "P5.2 — Comparar memoria de DFS vs BFS con numeros",
        "teoria": """\
  CONTINUANDO: sabes la diferencia conceptual.
  Ahora cuantificamos con el grafo del paper.

  Para el arbol BK del grafo del paper (sin pivote):
    Nivel 0: 1 nodo (la raiz con P={A,B,C,D,E,F})
    Nivel 1: 6 nodos (uno por cada vertice del nivel 0)
    Nivel 2: varios nodos (llamadas recursivas del nivel 1)
    ...y asi hasta las hojas.

  MEMORIA de DFS en cualquier momento:
    Solo el camino actual = UN NODO POR NIVEL.
    Si el arbol tiene profundidad 6 -> DFS necesita 6 nodos en RAM.

  MEMORIA de BFS en el nivel mas ancho:
    Todos los nodos de ese nivel a la vez.
    Si hay 20 nodos en ese nivel -> BFS necesita 20 nodos en RAM.

  En grafos REALES con miles de vertices:
    DFS: decenas de nodos en RAM.
    BFS: MILLONES o MILES DE MILLONES de nodos en RAM -> IMPOSIBLE.

  Esta diferencia es la razon por la que el paper usa DFS.\
""",
        "pregunta": "Si el arbol BK de un grafo real tiene profundidad 15 y el nivel mas ancho tiene 500.000 nodos, ¿cuanta memoria necesita cada estrategia?",
        "opciones": [
            "DFS: 500.000 nodos en RAM.  BFS: 15 nodos en RAM.",
            "DFS: 15 nodos en RAM.  BFS: 500.000 nodos en RAM.",
            "DFS y BFS necesitan la misma memoria porque recorren el mismo arbol.",
            "DFS: 15 x 500.000 = 7.5M nodos.  BFS: 500.000 nodos en RAM.",
        ],
        "correcta": 1,
        "explicacion": """\
  DFS solo guarda el CAMINO ACTUAL: 1 nodo por nivel = 15 nodos en RAM.
  BFS debe guardar TODOS los nodos del nivel actual = 500.000 nodos en RAM.

  En grafos reales, el nivel mas ancho puede tener millones de nodos.
  BFS se vuelve completamente inviable.
  DFS mantiene el uso de memoria completamente controlado.\
""",
    },

    {
        "punto": 5, "nivel": "Medio",
        "tema" : "P5.3 — Por que BFS falla en GPU: sincronizacion entre niveles",
        "teoria": """\
  CONTINUANDO: ya entiendes el problema de memoria de BFS.
  Hay un segundo problema de BFS especifico para la GPU.

  GPU = tarjeta grafica. Ejecuta KERNELS (programas paralelos).
  KERNEL = codigo que corre en la GPU con miles de hilos en paralelo.
  OVERHEAD = tiempo extra perdido en tareas administrativas (no trabajo util).

  IMPLEMENTACION BFS EN GPU (trabajos anteriores al paper):
    La CPU divide el trabajo del nivel 0 y lo envia a la GPU -> KERNEL 1.
    GPU procesa nivel 0, genera nodos del nivel 1, los devuelve a la CPU.
    CPU recibe nivel 1, lo reorganiza y lo envia a la GPU -> KERNEL 2.
    GPU procesa nivel 1, genera nivel 2... y asi nivel por nivel.
    -> Muchos KERNELS, mucha comunicacion CPU<->GPU.
    -> Cada transferencia de datos tiene overhead alto.

  IMPLEMENTACION DFS EN GPU (el paper):
    La CPU envia el trabajo inicial a la GPU UNA SOLA VEZ.
    La GPU ejecuta TODO el algoritmo BK en un UNICO KERNEL.
    No hay comunicacion CPU<->GPU durante la busqueda.
    Al terminar, devuelve las cliques encontradas.
    -> 1 kernel, sin overhead de sincronizacion.\\
""",
        "pregunta": "¿Por que la implementacion BFS en GPU tiene mas overhead que la implementacion DFS del paper?",
        "opciones": [
            "Porque BFS usa mas nucleos de la GPU que DFS, generando conflictos de acceso a memoria.",
            "Porque BFS necesita un kernel de GPU por cada nivel del arbol, con transferencias CPU-GPU entre cada nivel. DFS usa un unico kernel sin transferencias intermedias.",
            "Porque BFS no puede ejecutarse en GPU, solo en CPU.",
            "Porque BFS necesita construir el subgrafo inducido H(P,X) mas veces que DFS.",
        ],
        "correcta": 1,
        "explicacion": """\
  BFS en GPU: un kernel por nivel + transferencia CPU<->GPU entre cada nivel.
  Muchas transferencias = mucho overhead.

  DFS en GPU: un unico kernel que ejecuta todo el BK internamente.
  Sin transferencias intermedias = overhead minimo.

  Resultado: el paper es 35x mas rapido que la implementacion BFS anterior.\
""",
    },

    {
        "punto": 5, "nivel": "Avanzado",
        "tema" : "P5.4 — El speedup de 35x y sus factores",
        "teoria": """\
  CONTINUANDO: el paper afirma una mejora de 35x frente a la GPU anterior.
  SPEEDUP = cuantas veces mas rapido es el nuevo metodo.
  35x speedup = el paper hace en 1 minuto lo que el anterior hacia en 35 minutos.

  ¿De donde viene ese 35x? Son VARIOS factores combinados:

  FACTOR 1: DFS en vez de BFS -> elimina overhead de sincronizacion CPU-GPU.
  FACTOR 2: Un solo kernel -> no hay transferencias intermedias de datos.
  FACTOR 3: Degeneracy ordering -> P mas pequeno -> menos trabajo por llamada.
  FACTOR 4: Subgrafo inducido H(P,X) -> operaciones de interseccion mas rapidas.
  FACTOR 5: Workers list -> carga balanceada entre bloques GPU.
  FACTOR 6: Representacion binaria -> operaciones de bits muy rapidas en GPU.

  Ningun factor solo da 35x. La combinacion de todos ellos produce ese resultado.

  Comparacion del paper con CPU:
    Una sola GPU A100 = 4.9x mas rapido que 96 hilos de CPU.
    Hasta 16.7x en algunos grafos especificos.\
""",
        "pregunta": "El speedup de 35x del paper sobre implementaciones anteriores de GPU se debe a:",
        "opciones": [
            "Unicamente al uso de DFS en vez de BFS.",
            "Unicamente a la GPU A100 que es mas potente que las GPUs anteriores.",
            "A la combinacion de DFS, degeneracy ordering, subgrafo inducido, workers list y representacion binaria.",
            "Al uso de BFS mejorado con pivote y representacion binaria.",
        ],
        "correcta": 2,
        "explicacion": """\
  El 35x viene de la COMBINACION de mejoras:
  DFS (elimina sincronizacion) + degeneracy ordering (P mas pequeno)
  + subgrafo inducido H(P,X) (intersecciones mas rapidas)
  + workers list (carga balanceada)
  + representacion binaria (operaciones de bits rapidas).

  Cada mejora individual contribuye, pero juntas producen el 35x total.\
""",
    },

    # ╔════════════════════════════════════╗
    # ║  PUNTO 6 — Parametros Δ y d       ║
    # ╚════════════════════════════════════╝

    {
        "punto": 6, "nivel": "Medio",
        "tema" : "P6.1 — Asintotas de P, X y P union X sin ordering",
        "teoria": """\
  NOTACION O() = "ORDER OF" = como crece la memoria con el tamano del grafo.
    O(Δ)   = crece proporcional a Δ.
    O(Δ²)  = crece proporcional a Δ al cuadrado.
    O(Δ·d) = crece proporcional a Δ multiplicado por d.

  SIN degeneracy ordering:
    Al procesar el vertice v en el nivel superior de BK:
      P = N(v) = todos los vecinos de v.
      En el peor caso (vertice con grado Δ): |P| = Δ.
      -> P = O(Δ).

      X puede crecer hasta todos los vertices ya explorados.
      En el peor caso: |X| = Δ.
      -> X = O(Δ).

      P∪X = P union X. Domina el mayor: O(Δ).
      -> P∪X = O(Δ).

  En el grafo del paper: Δ=5.
  Sin ordering: P <= 5, X <= 5, P∪X <= 5.\
""",
        "pregunta": "En BK SIN degeneracy ordering, ¿cuales son las asintotas de P, X y P union X?",
        "opciones": [
            "P=O(d), X=O(Δ), P∪X=O(Δ)",
            "P=O(Δ), X=O(Δ), P∪X=O(Δ)",
            "P=O(Δ²), X=O(Δ²), P∪X=O(Δ²)",
            "P=O(Δ), X=O(d), P∪X=O(Δ)",
        ],
        "correcta": 1,
        "explicacion": """\
  Sin ordering:
    P = N(v) -> hasta Δ elementos -> O(Δ).
    X = vertices explorados -> hasta Δ -> O(Δ).
    P∪X = dominado por el mayor -> O(Δ).
  En el paper: Δ=5 -> P,X,P∪X <= 5 sin ordering.\
""",
    },

    {
        "punto": 6, "nivel": "Medio",
        "tema" : "P6.2 — Asintotas de P, X y P union X con ordering",
        "teoria": """\
  CONTINUANDO: ya sabes las asintotas sin ordering.
  Ahora veamos como cambian CON degeneracy ordering.

  CON ordering [E,F,A,B,C,D]:
    Al procesar el vertice v en posicion i:
      P = vecinos de v en posiciones > i (hacia adelante).
        Por definicion de degeneracy: |P| <= d.
        -> P = O(d).   MEJORA de O(Δ) a O(d).

      X = vecinos de v en posiciones < i (hacia atras).
        Puede llegar a Δ en el peor caso.
        -> X = O(Δ).   NO MEJORA.

      P∪X: P<=d, X<=Δ. El maximo es Δ.
        -> P∪X = O(Δ).   NO MEJORA (dominado por X).

  En el grafo del paper: Δ=5, d=3.
  Con ordering: P<=3, X<=5, P∪X<=5.
  Mejora solo en P: de O(5) a O(3).\
""",
        "pregunta": "En BK CON degeneracy ordering, ¿cuales son las asintotas de P, X y P union X?",
        "opciones": [
            "P=O(d), X=O(d), P∪X=O(d)",
            "P=O(Δ), X=O(Δ), P∪X=O(Δ)",
            "P=O(d), X=O(Δ), P∪X=O(Δ)",
            "P=O(d), X=O(Δ), P∪X=O(d+Δ)=O(Δ)",
        ],
        "correcta": 2,
        "explicacion": """\
  Con ordering:
    P = vecinos adelante -> acotado por d -> O(d).   MEJORA.
    X = vecinos atras    -> puede ser Δ  -> O(Δ).   No mejora.
    P∪X = dominado por X -> O(Δ).

  La clave: solo P mejora. X sigue siendo O(Δ).\
""",
    },

    {
        "punto": 6, "nivel": "Avanzado",
        "tema" : "P6.3 — Asintota del subgrafo H(P,X): con y sin ordering",
        "teoria": """\
  CONTINUANDO: ya sabes las asintotas de P, X y P∪X.
  Ahora la mas importante para el paper: el SUBGRAFO INDUCIDO H(P,X).

  SUBGRAFO INDUCIDO H(P,X):
    El paper construye un subgrafo auxiliar con los vertices de P∪X
    y las aristas entre ellos. Sirve para acelerar las intersecciones.

  CUANTAS ARISTAS tiene H(P,X)?
  En el peor caso: cada vertice de P∪X puede conectar con todos los demas.

  SIN ordering:
    |P∪X| hasta Δ vertices, cada uno con hasta Δ vecinos en P∪X.
    -> Hasta Δ x Δ = Δ² aristas.
    -> H(P,X) = O(Δ²).
    Con Δ=5: hasta 25 aristas.

  CON ordering:
    |P∪X| sigue hasta Δ, pero P tiene solo d vertices.
    Las aristas estan entre P-P, P-X y X-X.
    El termino dominante es Δ x d (vertices totales x vertices en P).
    -> H(P,X) = O(Δ·d).
    Con Δ=5, d=3: hasta 15 aristas.

  Ejemplo real del paper (grafo "com-Amazon"):
    Δ≈2752, d≈6.
    Sin: O(2752²)=O(7.573.504). Con: O(2752x6)=O(16.512). -> 459x menos!\
""",
        "pregunta": "¿Cuales son las asintotas del subgrafo H(P,X) con y sin ordering?",
        "opciones": [
            "Sin ordering: O(Δ+d).  Con ordering: O(Δ·d)",
            "Sin ordering: O(Δ²).   Con ordering: O(Δ·d)",
            "Sin ordering: O(Δ·d).  Con ordering: O(d²)",
            "Sin ordering: O(Δ²).   Con ordering: O(d²)",
        ],
        "correcta": 1,
        "explicacion": """\
  SIN ordering: |P∪X|<=Δ, cada uno con <=Δ vecinos -> O(Δ²).
  CON ordering: |P∪X|<=Δ, pero P solo tiene d vertices -> O(Δ·d).

  Ejemplo real: Δ=2752, d=6.
    Sin: 7.573.504 aristas. Con: 16.512 aristas. Ahorro del 99.8%!\
""",
    },

    {
        "punto": 6, "nivel": "Avanzado",
        "tema" : "P6.4 — Calcular P union X exacto para vertice A con ordering",
        "teoria": """\
  CONTINUANDO: sabes las asintotas. Ahora calculamos con numeros exactos.

  Para el vertice A (posicion 2 en [E,F,A,B,C,D]):

  SIN degeneracy ordering (orden alfabetico A,B,C,D,E,F):
    P = N(A) = {B,C,D,E,F}  ->  |P| = 5.
    X = {} (al inicio)      ->  |X| = 0.
    P∪X = {B,C,D,E,F}       -> |P∪X| = 5.
    H(P,X): hasta 5 vertices x 5 vecinos = O(25) aristas.

  CON degeneracy ordering [E,F,A,B,C,D]:
    P = {B,C,D}  (vecinos de A hacia adelante)  ->  |P| = 3.
    X = {E,F}    (vecinos de A hacia atras)      ->  |X| = 2.
    P∪X = {B,C,D,E,F}                           -> |P∪X| = 5.
    H(P,X): aristas entre {B,C,D,E,F}.
      Las conexiones relevantes: B-C✓,B-D✓,C-D✓,E-F✓ = 4 aristas.
      (ni E ni F conectan con B, C o D en el grafo del paper)

  Mejora en H(P,X): de O(25) a solo 4 aristas reales.\
""",
        "pregunta": "Para el vertice A con ordering, ¿cuanto valen |P|, |X| y |P∪X| exactamente?",
        "opciones": [
            "|P|=5, |X|=0, |P∪X|=5  (igual que sin ordering)",
            "|P|=3, |X|=2, |P∪X|=5  (P={B,C,D}, X={E,F})",
            "|P|=2, |X|=3, |P∪X|=5  (P={E,F}, X={B,C,D})",
            "|P|=3, |X|=0, |P∪X|=3  (X empieza siempre vacio)",
        ],
        "correcta": 1,
        "explicacion": """\
  A esta en posicion 2 en [E,F,A,B,C,D].
  P = vecinos de A con posicion > 2 = {B(3),C(4),D(5)} -> |P|=3.
  X = vecinos de A con posicion < 2 = {E(0),F(1)}      -> |X|=2.
  P∪X = {B,C,D,E,F}                                    -> |P∪X|=5.

  P mejora (5->3) pero P∪X no mejora (sigue siendo 5).\
""",
    },

    {
        "punto": 6, "nivel": "Avanzado",
        "tema" : "P6.5 — La representacion compacta de X: X_P y X_X",
        "teoria": """\
  CONTINUANDO: X sigue siendo O(Δ) con ordering.
  El paper propone una representacion especial para manejar X mejor.

  X SE DIVIDE EN DOS PARTES:
    X_P = vertices que originalmente estaban en P y pasaron a X.
          Estos vertices CRECEN Y DECRECEN con la profundidad de la recursion.
          Se representan con CODIFICACION BINARIA (un bit por vertice de P).
          Se guarda UNA COPIA POR NIVEL de recursion.

    X_X = vertices que ya estaban en X desde el inicio de esta llamada.
          Estos vertices solo DECRECEN (algunos se eliminan pero nunca se añaden).
          Se guarda como un ARRAY con punteros a nivel.

  ¿Por que esta division?
    X_P y X_X tienen comportamientos diferentes:
      X_P puede crecer y decrecer -> necesita copia por nivel.
      X_X solo decrece -> basta con punteros al array compartido.
    Esto reduce la memoria total de X de O(Δ·d) a O(Δ + d²).

  Sin esta optimizacion: X ocupa O(Δ·d) por nivel de recursion.
  Con ella: O(Δ) para X_X + O(d²) para X_P = O(Δ + d²).\
""",
        "pregunta": "¿Por que el paper divide X en dos partes X_P y X_X?",
        "opciones": [
            "Para poder paralelizar el procesamiento de X entre dos bloques GPU.",
            "Porque X_P y X_X tienen comportamientos distintos: X_P crece y decrece (necesita copia por nivel), X_X solo decrece (basta con punteros). Reduce memoria de O(Δ·d) a O(Δ+d²).",
            "Para poder aplicar el pivote sobre X_P y el degeneracy ordering sobre X_X.",
            "Porque X_P contiene los vertices del grafo y X_X contiene las aristas del grafo.",
        ],
        "correcta": 1,
        "explicacion": """\
  X_P = vertices que pasaron de P a X durante la recursion.
        Comportamiento: crece y decrece -> copia por nivel -> O(d) por nivel.
  X_X = vertices que empezaron en X.
        Comportamiento: solo decrece -> punteros -> O(Δ) compartido.

  Sin division: O(Δ·d) por nivel.
  Con division: O(Δ) + O(d²) = O(Δ+d²). Ahorro significativo.\
""",
    },

    # ╔══════════════════════════════════╗
    # ║  PUNTO 7 — Workers list         ║
    # ╚══════════════════════════════════╝

    {
        "punto": 7, "nivel": "Basico",
        "tema" : "P7.1 — El desequilibrio de carga en la GPU",
        "teoria": """\
  PARALELIZACION: BLOQUES Y DESEQUILIBRIO
  ─────────────────────────────────────────
  GPU = tarjeta grafica con miles de BLOQUES DE HILOS en paralelo.
  El paper asigna un SUBARBOL de BK a cada bloque.
  Con ordering [E,F,A,B,C,D] hay 6 subarboles de nivel 1 -> 6 bloques.

  DESEQUILIBRIO DE CARGA (Load Imbalance):
  Problema: los subarboles tienen TAMANOS MUY DISTINTOS.

    Bloque D: P={}, R={D} -> 0 trabajo -> termina AL INSTANTE.
    Bloque F: P={A}       -> muy poco trabajo -> termina RAPIDO.
    Bloque E: P={F,A}     -> algo de trabajo.
    Bloque C: P={D}       -> poco trabajo.
    Bloque B: P={C,D}     -> trabajo moderado.
    Bloque A: P={B,C,D}   -> MAS TRABAJO -> tarda mas.

  Sin balanceo:
    Bloques D,F terminan rapido y quedan OCIOSOS (desperdicio).
    El tiempo total = el del bloque MAS LENTO (A).
    RATIO = tiempo peor bloque / tiempo medio = 2.28x en grafos reales.\
""",
        "pregunta": "¿Que es el desequilibrio de carga (load imbalance) en la GPU del paper?",
        "opciones": [
            "Que la GPU consume mas electricidad que la CPU al ejecutar el algoritmo.",
            "Que algunos bloques GPU tienen subarboles grandes (mucho trabajo) mientras otros tienen subarboles pequenos y quedan ociosos, desperdiciando recursos.",
            "Que el algoritmo BK no distribuye igualmente los vertices del grafo entre los bloques.",
            "Que la memoria de la GPU se llena antes de terminar el calculo.",
        ],
        "correcta": 1,
        "explicacion": """\
  El desequilibrio de carga = algunos bloques tienen MUCHO trabajo y otros POCO.
  Los que terminan pronto quedan ociosos mientras los lentos siguen.
  El tiempo total lo marca el bloque mas lento.
  En grafos reales: ratio = 2.28x (el peor trabaja 2.28 veces mas que la media).\
""",
    },

    {
        "punto": 7, "nivel": "Medio",
        "tema" : "P7.2 — Por que el worklist es inviable y la workers list es viable",
        "teoria": """\
  CONTINUANDO: el desequilibrio es el problema. Hay dos soluciones posibles.

  SOLUCION 1 — WORKLIST (lista de TAREAS) — RECHAZADA:
    Cola compartida con tareas pendientes.
    Los bloques ociosos toman tareas.
    Una TAREA en MCE = {R, P, X, nivel, subgrafo H(P,X)}.
    Problema: una sola tarea puede ocupar megabytes.
      P tiene hasta d vertices (hasta cientos).
      X tiene hasta Δ vertices (hasta miles).
      H(P,X) tiene hasta Δ·d aristas (hasta miles de miles).
    Con cien tareas -> gigabytes -> INVIABLE.
    Ademas: anadir/quitar tareas tiene OVERHEAD alto (operaciones atomicas).

  SOLUCION 2 — WORKERS LIST (lista de TRABAJADORES) — USADA:
    Cola con IDs de bloques ociosos (solo numeros enteros pequenos).
    Los datos de la tarea quedan en el bloque DONANTE.
    Solo se copian los datos iniciales al receptor cuando se dona.
    -> Memoria minima en la cola.
    -> Overhead minimo.\
""",
        "pregunta": "¿Cuál es la diferencia fundamental entre WORKLIST y WORKERS LIST?",
        "opciones": [
            "Worklist es para CPU y workers list es para GPU. Ambas guardan lo mismo.",
            "Worklist guarda tareas completas (R,P,X,subgrafo) = mucha memoria. Workers list guarda solo IDs de bloques ociosos = memoria minima.",
            "Worklist usa memoria estatica y workers list usa memoria dinamica.",
            "Worklist guarda IDs de bloques y workers list guarda las tareas completas.",
        ],
        "correcta": 1,
        "explicacion": """\
  WORKLIST: guarda TAREAS COMPLETAS (R,P,X,nivel,subgrafo).
  Una tarea = megabytes. Muchas tareas = gigabytes -> INVIABLE.

  WORKERS LIST: guarda solo IDs de bloques OCIOSOS (numeros enteros).
  Los datos quedan en el donante. Solo se copian al donar.
  Memoria y overhead minimos -> VIABLE.\
""",
    },

    {
        "punto": 7, "nivel": "Medio",
        "tema" : "P7.3 — Roles de RECEPTOR y DONANTE",
        "teoria": """\
  CONTINUANDO: ya sabes que la workers list guarda IDs de bloques ociosos.
  Ahora veamos los dos roles en detalle.

  RECEPTOR (Receiver block) = bloque que QUIERE trabajo:
    1. El bloque termino su subarbol. Esta ocioso.
    2. Escribe su ID en la workers list: "bloque #5 disponible".
    3. Se DUERME (espera activa, consume muy pocos recursos).
    4. Espera a ser despertado por un donante.

  DONANTE (Donor block) = bloque con MUCHO trabajo:
    1. Esta procesando un subarbol con |P| >= 10.
       (|P|>=10 porque si P es muy pequeno, preparar la donacion
        cuesta mas que el trabajo que se dona.)
    2. PERIODICAMENTE revisa la workers list.
    3. Si hay un receptor libre:
       a. Extrae el ID del receptor de la workers list.
       b. Elige un vertice v de su P actual.
       c. Inicializa los datos de la rama de v en la memoria del receptor.
       d. DESPIERTA al receptor: ahora el receptor procesa la rama de v.
    4. El donante sigue con el resto de su P original.\
""",
        "pregunta": "Un bloque GPU ha terminado su subarbol. ¿Que hace segun el sistema de workers list?",
        "opciones": [
            "Se detiene y espera a que terminen todos los demas bloques.",
            "Empieza a procesar el subarbol del siguiente vertice en el ordering.",
            "Escribe su ID en la workers list como RECEPTOR y se duerme, esperando que un donante le asigne trabajo.",
            "Notifica a la CPU que ha terminado y espera nuevas instrucciones.",
        ],
        "correcta": 2,
        "explicacion": """\
  Un bloque que termina su subarbol se convierte en RECEPTOR:
  1. Escribe su ID en la workers list ("estoy disponible").
  2. Se duerme (espera activa sin consumir recursos de calculo).
  3. Espera a que un DONANTE lo despierte con trabajo nuevo.

  Esto evita que el bloque quede completamente ocioso.\
""",
    },

    {
        "punto": 7, "nivel": "Medio",
        "tema" : "P7.4 — Por que la condicion |P|>=10 antes de donar",
        "teoria": """\
  CONTINUANDO: el donante solo dona si |P| >= 10.
  ¿Por que este umbral concreto?

  Cuando un donante prepara una donacion:
    1. Debe comprobar si hay receptores en la workers list.
    2. Debe copiar los datos iniciales al receptor.
    3. Debe despertar al receptor.
  Estas operaciones tienen un COSTE (overhead).

  Si el subarbol a donar tiene |P| = 2 (muy pequeno):
    El trabajo que se dona es MUY POCO.
    El overhead de preparar la donacion puede ser MAYOR que el trabajo donado.
    -> No compensa donar.

  Si el subarbol a donar tiene |P| = 50 (grande):
    El trabajo donado es MUCHO.
    El overhead de la donacion es una fraccion pequena del total.
    -> Compensa claramente donar.

  El umbral |P| >= 10 es el punto de equilibrio encontrado
  empiricamente por los autores del paper.
  Por debajo de 10: el overhead no compensa.
  Por encima de 10: la donacion mejora el rendimiento.\
""",
        "pregunta": "¿Por que el donante solo cede trabajo cuando |P| >= 10?",
        "opciones": [
            "Porque la GPU solo puede procesar subarboles de tamano mayor a 10.",
            "Porque con |P| < 10 no se puede aplicar el algoritmo BK con pivote.",
            "Porque con |P| < 10, el overhead de preparar la donacion (copiar datos, despertar receptor) es mayor que el trabajo que se dona. No compensa.",
            "Porque 10 es el numero maximo de receptores que puede tener la workers list simultaneamente.",
        ],
        "correcta": 2,
        "explicacion": """\
  La donacion tiene un COSTE (overhead): copiar datos, operaciones atomicas, despertar receptor.
  Si |P| < 10, el trabajo donado es tan pequeno que el overhead lo supera.
  Si |P| >= 10, el trabajo donado supera el overhead con creces.
  El umbral 10 es el valor empirico encontrado por los autores.\
""",
    },

    {
        "punto": 7, "nivel": "Avanzado",
        "tema" : "P7.5 — Las dos fases de paralelizacion",
        "teoria": """\
  CONTINUANDO: ya entiendes receptor, donante y la condicion de donacion.
  Ahora el esquema completo de 2 fases.

  FASE 1 — ESTATICA (trabajo fijo, sin comunicacion):
    Se asigna UN subarbol de nivel 1 a cada bloque GPU.
    Un subarbol de nivel 1 = el subarbol que tiene como raiz
    un vertice del degeneracy ordering.
    Con [E,F,A,B,C,D]: 6 subarboles -> 6 bloques, asignacion fija.
    Los bloques trabajan COMPLETAMENTE INDEPENDIENTES.
    No hay comunicacion entre bloques.

  FASE 2 — DINAMICA (workers list activa):
    Cuando un bloque termina en la Fase 1 -> se convierte en RECEPTOR.
    Bloques con |P|>=10 -> comprueban si hay receptores -> DONANTES.
    Las donaciones son de ramas de NIVEL 2 y superiores
    (ramas internas al subarbol del donante).
    Sin sincronizacion global (no paran todos los bloques a la vez).

  EFECTO MEDIDO:
    Sin workers list: ratio desequilibrio = 2.28x.
    Con workers list: ratio desequilibrio = 1.17x.
    Casi equilibrio perfecto (1.0x = todos trabajan lo mismo).\
""",
        "pregunta": "¿En que consisten la Fase 1 y la Fase 2 del esquema de paralelizacion del paper?",
        "opciones": [
            "Fase 1=BFS hasta nivel 2. Fase 2=DFS desde nivel 2. Workers list activa en ambas fases.",
            "Fase 1=cada bloque toma un subarbol de nivel 1, trabajo estatico sin comunicacion. Fase 2=workers list activa, bloques ociosos reciben ramas de nivel 2+ de bloques ocupados.",
            "Fase 1=construccion del subgrafo H(P,X). Fase 2=aplicacion de BK con pivote.",
            "Fase 1=paralelismo de hilos dentro de un bloque. Fase 2=paralelismo entre bloques con worklist.",
        ],
        "correcta": 1,
        "explicacion": """\
  FASE 1 (estatica): un bloque = un subarbol de nivel 1. Sin comunicacion.
  FASE 2 (dinamica): workers list activa.
    Bloques ociosos (receptores) reciben ramas de nivel 2+
    de bloques ocupados (donantes, |P|>=10).

  Mejora: ratio de 2.28x a 1.17x.\
""",
    },

    {
        "punto": 7, "nivel": "Avanzado",
        "tema" : "P7.6 — Que datos copia el donante al receptor",
        "teoria": """\
  CONTINUANDO: cuando un donante cede una rama al receptor,
  ¿que datos exactamente tiene que copiar?

  Para que el receptor pueda empezar a procesar la rama de v,
  necesita saber cual es su estado inicial:

  DATOS QUE COPIA EL DONANTE AL RECEPTOR:
    1. R_nuevo = R_donante union {v}
       (la clique del donante mas el vertice v cedido)

    2. P_nuevo = P_donante interseccion N(v)
       (candidatos de la rama de v)

    3. X_nuevo = X_donante interseccion N(v)
       (excluidos relevantes para la rama de v)

    4. Referencia al SUBGRAFO INDUCIDO H(P_donante, X_donante)
       (el receptor puede reutilizarlo para calcular sus intersecciones)

  El donante NO copia su P completo, solo el necesario para la rama de v.
  Esto minimiza la cantidad de datos transferidos.

  Despues de la donacion:
    El DONANTE elimina v de su P y sigue con el resto de su P.
    El RECEPTOR procesa la rama de v de forma independiente.\
""",
        "pregunta": "Cuando el donante cede la rama del vertice v al receptor, ¿que datos debe inicializar en la memoria del receptor?",
        "opciones": [
            "Solo el ID del vertice v. El receptor puede deducir el resto del grafo original.",
            "El R, P y X COMPLETOS del donante. El receptor trabaja con exactamente los mismos datos.",
            "R_nuevo=R_donante∪{v}, P_nuevo=P_donante∩N(v), X_nuevo=X_donante∩N(v), y referencia al subgrafo H.",
            "Solo el conjunto P del donante interseccionado con N(v). R y X no son necesarios.",
        ],
        "correcta": 2,
        "explicacion": """\
  El receptor necesita exactamente el estado inicial de la rama de v:
    R_nuevo = R_donante ∪ {v}          (v entra en la clique).
    P_nuevo = P_donante ∩ N(v)         (candidatos para esa rama).
    X_nuevo = X_donante ∩ N(v)         (excluidos para esa rama).
    Subgrafo H: referencia compartida para las operaciones.

  Esto es exactamente lo que calcularia el donante al explorar v
  en la siguiente iteracion sin la workers list.\
""",
    },

    {
        "punto": 7, "nivel": "Avanzado",
        "tema" : "P7.7 — Interpretar el ratio de desequilibrio: 2.28x -> 1.17x",
        "teoria": """\
  CONTINUANDO: el paper mide la mejora del balanceo con el RATIO DE DESEQUILIBRIO.

  RATIO DE DESEQUILIBRIO = tiempo_del_bloque_mas_lento / tiempo_medio_de_todos.

    Ratio = 1.0x = equilibrio PERFECTO. Todos trabajan exactamente lo mismo.
    Ratio = 2.0x = el peor bloque trabaja el DOBLE que la media.
    Ratio = 2.28x = el peor bloque trabaja 2.28 veces mas que la media.

  Si hay 6 bloques y el tiempo total de trabajo es 120 unidades:
    Tiempo medio = 120/6 = 20 unidades.

  SIN workers list (ratio=2.28x):
    El peor bloque trabaja 2.28 x 20 = 45.6 unidades.
    El tiempo total del calculo = 45.6 (esperamos al mas lento).
    Tiempo desperdiciado en bloques ociosos = 45.6x6 - 120 = 153.6 unidades.

  CON workers list (ratio=1.17x):
    El peor bloque trabaja 1.17 x 20 = 23.4 unidades.
    El tiempo total del calculo = 23.4.
    AHORRO = 45.6 - 23.4 = 22.2 unidades = ~49% mas rapido.

  En grafos reales con tiempos de horas, este ahorro es enorme.\
""",
        "pregunta": "¿Que significa exactamente que el ratio de desequilibrio mejore de 2.28x a 1.17x?",
        "opciones": [
            "Que el algoritmo es 2.28/1.17 = 1.95 veces mas preciso al encontrar cliques.",
            "Que el bloque mas lento pasaba de trabajar 2.28x la media a trabajar 1.17x la media, reduciendo el tiempo total de espera en casi la mitad.",
            "Que el numero de bloques activos aumento de 1.17 a 2.28 veces el numero inicial.",
            "Que la GPU usa el 2.28% de su capacidad sin workers list y el 1.17% con ella.",
        ],
        "correcta": 1,
        "explicacion": """\
  Ratio = tiempo_peor_bloque / tiempo_medio.
    Sin workers list: peor bloque trabaja 2.28x la media. Tiempo total = 2.28x media.
    Con workers list: peor bloque trabaja 1.17x la media. Tiempo total = 1.17x media.

  Mejora en tiempo total: 2.28/1.17 ≈ 1.95x -> casi el doble de rapido.
  El balance casi perfecto (1.17 vs ideal 1.0) se consigue con overhead minimo.\
""",
    },

]   # fin PREGUNTAS


# ═══════════════════════════════════════════════════
#  MOTOR DEL CUESTIONARIO
# ═══════════════════════════════════════════════════

def mostrar_cabecera(num, total, preg):
    col = NIVELES_COLOR.get(preg["nivel"], RESET)
    print("\n\n")
    print(f"{AZUL}{NEGRITA}{'─'*65}{RESET}")
    print(f"{AZUL}{NEGRITA}  Pregunta {num}/{total}   Punto {preg['punto']}: {preg['tema']}{RESET}")
    print(f"  Dificultad: {col}{NEGRITA}{preg['nivel']}{RESET}")
    print(f"{AZUL}{NEGRITA}{'─'*65}{RESET}")

def mostrar_teoria(preg):
    print(f"\n  {CIAN}{NEGRITA}LEE ESTO ANTES DE RESPONDER:{RESET}\n")
    for linea in preg["teoria"].split("\n"):
        print(f"  {CIAN}{linea}{RESET}")

def mostrar_opciones(preg):
    letras = ['a','b','c','d']
    print(f"\n  {AMARILLO}{NEGRITA}{'─'*55}{RESET}")
    print(f"  {AMARILLO}{NEGRITA}PREGUNTA:{RESET}\n")
    for linea in preg["pregunta"].split("\n"):
        print(f"  {NEGRITA}{linea}{RESET}")
    print()
    for i, op in enumerate(preg["opciones"]):
        print(f"  {NEGRITA}{letras[i]}){RESET}  {op}")
    print()
    while True:
        r = input("  Tu respuesta (a/b/c/d): ").strip().lower()
        if r in letras:
            return letras.index(r)
        print(f"  {AMARILLO}  Solo a, b, c o d.{RESET}")

def mostrar_feedback(correcta, elegida, preg):
    letras  = ['a','b','c','d']
    acierto = (elegida == correcta)
    print()
    if acierto:
        print(f"  {VERDE}{NEGRITA}  ✓  CORRECTO!{RESET}")
    else:
        print(f"  {ROJO}{NEGRITA}  ✗  INCORRECTO.{RESET}")
        print(f"  {ROJO}  Tu respuesta:       {letras[elegida]}) {preg['opciones'][elegida]}{RESET}")
        print(f"  {VERDE}  Respuesta correcta: {letras[correcta]}) {preg['opciones'][correcta]}{RESET}")
    print(f"\n  {AMARILLO}{NEGRITA}  ¿POR QUE ES CORRECTA?{RESET}")
    for linea in preg["explicacion"].split("\n"):
        print(f"  {linea}")
    print()
    input("  Pulsa ENTER para continuar...")
    return acierto

def mostrar_resumen(resultados):
    print("\n\n")
    print(f"{AZUL}{NEGRITA}{'═'*65}{RESET}")
    print(f"{AZUL}{NEGRITA}  RESULTADO FINAL{RESET}")
    print(f"{AZUL}{NEGRITA}{'═'*65}{RESET}\n")
    total = len(resultados)
    ok    = sum(1 for r in resultados if r["correcto"])
    pct   = (ok/total)*100
    col   = VERDE if pct>=70 else (AMARILLO if pct>=50 else ROJO)
    print(f"  {col}{NEGRITA}  {ok} de {total} correctas  ({pct:.0f}%){RESET}")
    llenas = int(pct/5)
    print(f"\n  [{col}{'█'*llenas}{RESET}{'░'*(20-llenas)}]  {pct:.0f}%\n")
    if   pct>=90: print(f"  {VERDE}{NEGRITA}  Excelente! Estas listo para el examen del 14 de junio.{RESET}")
    elif pct>=70: print(f"  {VERDE}  Bien! Repasa los temas marcados en rojo.{RESET}")
    elif pct>=50: print(f"  {AMARILLO}  Regular. Vuelve a leer los puntos con mas fallos.{RESET}")
    else:         print(f"  {ROJO}  Necesitas mas repaso. Ejecuta explicacion_paper.py primero.{RESET}")

    nombres = {
        1:"Grafo",2:"Cliques",3:"Bron-Kerbosch",
        4:"Degeneracy ordering",5:"BFS vs DFS",
        6:"Parametros Δ y d",7:"Workers list",
    }
    print(f"\n  {'─'*60}")
    print(f"  DESGLOSE POR PUNTO:")
    print(f"  {'─'*60}")
    for p in range(1,8):
        rp  = [r for r in resultados if r["punto"]==p]
        if not rp: continue
        nok = sum(1 for r in rp if r["correcto"])
        nt  = len(rp)
        pc  = (nok/nt)*100
        c   = VERDE if pc>=70 else (AMARILLO if pc>=50 else ROJO)
        bar = ('█'*nok)+('░'*(nt-nok))
        print(f"  Punto {p}: {nombres[p]:<22} {c}{bar}  {nok}/{nt}  ({pc:.0f}%){RESET}")

    fallados = [r for r in resultados if not r["correcto"]]
    if fallados:
        print(f"\n  {ROJO}  TEMAS A REPASAR:{RESET}")
        for r in fallados:
            cn = NIVELES_COLOR.get(r["nivel"], RESET)
            print(f"  {ROJO}    [{cn}{r['nivel']}{ROJO}] {r['tema']}{RESET}")
    print(f"\n  {'═'*65}\n")


# ═══════════════════════════════════════════════════
#  MENU
# ═══════════════════════════════════════════════════

def menu():
    print("\n\n")
    print(f"{AZUL}{NEGRITA}{'═'*65}{RESET}")
    print(f"{AZUL}{NEGRITA}  CUESTIONARIO — Maximal Clique Enumeration on GPUs{RESET}")
    print(f"{AZUL}{NEGRITA}{'═'*65}{RESET}\n")

    total  = len(PREGUNTAS)
    nb     = sum(1 for p in PREGUNTAS if p["nivel"]=="Basico")
    nm     = sum(1 for p in PREGUNTAS if p["nivel"]=="Medio")
    na     = sum(1 for p in PREGUNTAS if p["nivel"]=="Avanzado")
    print(f"  Total: {total} preguntas  ({VERDE}{NEGRITA}{nb} Basicas{RESET} / "
          f"{AMARILLO}{NEGRITA}{nm} Medias{RESET} / {ROJO}{NEGRITA}{na} Avanzadas{RESET})\n")

    print(f"  Modos:\n")
    print("  1)  Completo en orden basico -> avanzado")
    print("  2)  Solo Basicas  (fundamentos)")
    print("  3)  Solo Medias   (comprension)")
    print("  4)  Solo Avanzadas (dominio total)")
    print("  5)  Un Punto concreto (1-7)")
    print("  6)  Salir\n")
    while True:
        op = input("  Tu eleccion (1-6): ").strip()
        if op in ["1","2","3","4","5","6"]: return op
        print(f"  {AMARILLO}  Escribe 1-6.{RESET}")

def elegir_punto():
    nombres = {
        "1":"Grafo: elementos y propiedades",
        "2":"Maximal cliques y k-cliques",
        "3":"Algoritmo Bron-Kerbosch",
        "4":"Degeneracy ordering",
        "5":"BFS vs DFS",
        "6":"Parametros Δ y d",
        "7":"Workers list vs Worklist",
    }
    print("\n  ¿Que punto quieres practicar?\n")
    for k,v in nombres.items():
        rp = [p for p in PREGUNTAS if p["punto"]==int(k)]
        print(f"  {k})  Punto {k}: {v}  ({len(rp)} preguntas)")
    print()
    while True:
        op = input("  Tu eleccion (1-7): ").strip()
        if op in nombres: return int(op)
        print(f"  {AMARILLO}  Escribe 1-7.{RESET}")


# ═══════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    while True:
        op = menu()
        if op == "6":
            print(f"\n  {VERDE}  Hasta luego!{RESET}\n")
            break

        if   op == "1": sel = list(PREGUNTAS)
        elif op == "2": sel = [p for p in PREGUNTAS if p["nivel"]=="Basico"]
        elif op == "3": sel = [p for p in PREGUNTAS if p["nivel"]=="Medio"]
        elif op == "4": sel = [p for p in PREGUNTAS if p["nivel"]=="Avanzado"]
        elif op == "5":
            pt  = elegir_punto()
            sel = [p for p in PREGUNTAS if p["punto"]==pt]

        if not sel:
            print(f"  {AMARILLO}  No hay preguntas para esa seleccion.{RESET}")
            continue

        resultados = []
        for i, preg in enumerate(sel, 1):
            mostrar_cabecera(i, len(sel), preg)
            mostrar_teoria(preg)
            elegida  = mostrar_opciones(preg)
            correcto = mostrar_feedback(preg["correcta"], elegida, preg)
            resultados.append({
                "punto"  : preg["punto"],
                "nivel"  : preg["nivel"],
                "tema"   : preg["tema"],
                "correcto": correcto,
            })

        mostrar_resumen(resultados)
        rep = input("  ¿Otro cuestionario? (s/n): ").strip().lower()
        if rep != "s":
            print(f"\n  {VERDE}  Hasta luego!{RESET}\n")
            break

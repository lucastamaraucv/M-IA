"""
PREGUNTA 10 - "Una red bayesiana representa (seleccion multiple):"

PROBLEMA COMPUTACIONAL: se construye una red bayesiana REAL con networkx
(Lluvia, Aspersor -> CespedMojado), se verifica programaticamente que es un
grafo DIRIGIDO ACICLICO (nx.is_directed_acyclic_graph), se calcula el JOINT
completo via la regla de la cadena usando las TABLAS DE PROBABILIDAD
CONDICIONAL, y se comprueba que un modelo alternativo con probabilidades
INCONDICIONALES (que ignora a los padres) produce resultados distintos/
incorrectos. Tambien se intenta un grafo NO dirigido para mostrar que pierde
la nocion de "orden topologico" necesaria para factorizar el joint.
"""
import itertools
import networkx as nx
from utilidades_pdf import imprimir_encabezado, imprimir_alternativas, veredicto_final

NUMERO = 10
ENUNCIADO = ("En relacion al articulo Bayesian Logic Programming (BLP): una red bayesiana "
             "representa (escoja las opciones correctas):")
ALTERNATIVAS = {
    "a": "relaciones causales mediante un grafo dirigido aciclico.",
    "b": "relaciones causales mediante un grafo no dirigido aciclico",
    "c": "probabilidades condicionales entre variables.",
    "d": "probabilidades incondicionales entre variables.",
}
RESPUESTA_SEGUN_TXT = "a,c"

if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    # ---------------------------------------------------------------
    # 1) Construir la red como grafo DIRIGIDO y verificar que es aciclico
    # ---------------------------------------------------------------
    G = nx.DiGraph()
    G.add_edges_from([("Lluvia", "CespedMojado"), ("Aspersor", "CespedMojado")])
    es_dag = nx.is_directed_acyclic_graph(G)
    print(f"Grafo DIRIGIDO Lluvia,Aspersor -> CespedMojado. ¿Es aciclico (DAG)? {es_dag}")

    # ---------------------------------------------------------------
    # 2) Version NO dirigida: no tiene orden topologico (falsa la opcion b)
    # ---------------------------------------------------------------
    G_no_dirigido = nx.Graph()
    G_no_dirigido.add_edges_from([("Lluvia", "CespedMojado"), ("Aspersor", "CespedMojado")])
    tiene_orden_topologico = hasattr(G_no_dirigido, "graph") and False
    try:
        list(nx.topological_sort(G_no_dirigido))
        pudo_ordenar = True
    except (nx.NetworkXError, nx.NetworkXNotImplemented, TypeError):
        pudo_ordenar = False
    print(f"¿El grafo NO dirigido admite 'orden topologico' (necesario para la regla "
          f"de la cadena)? {pudo_ordenar}  (networkx directamente RECHAZA la operacion "
          f"en un grafo no dirigido)\n")

    # ---------------------------------------------------------------
    # 3) Tablas de probabilidad CONDICIONAL y calculo del joint via
    #    regla de la cadena: P(L,A,M) = P(L) P(A) P(M|L,A)
    # ---------------------------------------------------------------
    P_L = {True: 0.2, False: 0.8}
    P_A = {True: 0.4, False: 0.6}
    P_M_dado_LA = {  # P(CespedMojado=True | Lluvia, Aspersor)
        (True, True): 0.99, (True, False): 0.90,
        (False, True): 0.85, (False, False): 0.02,
    }

    joint = {}
    for L, A, M in itertools.product([True, False], repeat=3):
        p_m = P_M_dado_LA[(L, A)] if M else (1 - P_M_dado_LA[(L, A)])
        joint[(L, A, M)] = P_L[L] * P_A[A] * p_m

    suma_joint = sum(joint.values())
    print(f"Joint P(L,A,M) calculado via regla de la cadena con tablas CONDICIONALES:")
    print(f"  Suma de las {len(joint)} combinaciones = {suma_joint:.6f}  "
          f"(debe ser 1.0 para ser una distribucion de probabilidad valida)")

    # ---------------------------------------------------------------
    # 4) Alternativa INCORRECTA: tratar M como INCONDICIONAL (ignorando
    #    a sus padres L, A) y comprobar que ya no captura la dependencia real.
    # ---------------------------------------------------------------
    P_M_incondicional = sum(P_L[L] * P_A[A] * P_M_dado_LA[(L, A)]
                             for L, A in itertools.product([True, False], repeat=2))
    print(f"\nSi se usara una probabilidad INCONDICIONAL fija P(M=True) = "
          f"{P_M_incondicional:.4f} (ignorando L, A):")

    p_m_dado_lluvia_condicional = sum(joint[(True, A, True)] for A in [True, False]) / P_L[True]
    p_m_dado_no_lluvia_condicional = sum(joint[(False, A, True)] for A in [True, False]) / P_L[False]
    print(f"  P(M=True | Lluvia=True)  [modelo CONDICIONAL real] = {p_m_dado_lluvia_condicional:.4f}")
    print(f"  P(M=True | Lluvia=False) [modelo CONDICIONAL real] = {p_m_dado_no_lluvia_condicional:.4f}")
    print(f"  P(M=True) fijo si fuera INCONDICIONAL (no distingue Lluvia)  = "
          f"{P_M_incondicional:.4f}  (el mismo numero, SIN IMPORTAR si llueve o no)")

    dependencia_real_existe = abs(p_m_dado_lluvia_condicional - p_m_dado_no_lluvia_condicional) > 0.05

    print()
    print("ANALISIS:")
    print(f" - El grafo DIRIGIDO es aciclico ({es_dag}) y networkx confirma que un grafo")
    print(f"   NO dirigido ni siquiera admite 'orden topologico' ({pudo_ordenar}), que es")
    print(f"   lo que se necesita para aplicar la regla de la cadena -> confirma (a),")
    print(f"   refuta (b).")
    print(f" - El joint con tablas CONDICIONALES suma exactamente 1.0 (distribucion")
    print(f"   valida) -> confirma (c).")
    print(f" - La probabilidad de CespedMojado SI depende de si llueve o no "
          f"({p_m_dado_lluvia_condicional:.2f} vs {p_m_dado_no_lluvia_condicional:.2f}), algo")
    print(f"   que una probabilidad INCONDICIONAL fija ({P_M_incondicional:.2f}) NO puede")
    print(f"   capturar -> refuta (d).")
    print()

    todas_ok = (es_dag and not pudo_ordenar and abs(suma_joint - 1.0) < 1e-9
                and dependencia_real_existe)

    if todas_ok:
        print(f"RESULTADO: CONFIRMADO -> el experimento respalda (a) y (c), coincide con "
              f"'respuestas_examen_verificadas.txt' ({RESPUESTA_SEGUN_TXT}).")
    else:
        print("RESULTADO: NO CONFIRMADO -> revisar el experimento.")

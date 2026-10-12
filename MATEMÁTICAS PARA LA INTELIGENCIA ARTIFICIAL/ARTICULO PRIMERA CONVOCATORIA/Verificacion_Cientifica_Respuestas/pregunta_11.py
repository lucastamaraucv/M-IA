"""
PREGUNTA 11 - "El concepto de support network hace referencia a:"

PROBLEMA COMPUTACIONAL: se construye una red bayesiana de 5 variables con DOS
ramas: una relevante para la consulta (A, B -> C) y otra INDEPENDIENTE y
totalmente ajena (D -> E). Se calcula P(C=True | A=True) -una consulta
CONCRETA- de DOS formas: (1) por enumeracion exacta sobre las 5 variables
(la "red completa"), y (2) usando SOLO el support network de la consulta
{A,B,C} (Definicion 1.8), ignorando D y E por completo. Si ambos resultados
coinciden exactamente, se verifica computacionalmente el Teorema 1.9 del
articulo: el calculo NO depende de nodos fuera del support network.
"""
import itertools
from utilidades_pdf import imprimir_encabezado, imprimir_alternativas, veredicto_final

NUMERO = 11
ENUNCIADO = "El concepto de support network hace referencia a:"
ALTERNATIVAS = {
    "a": "responder consultas probabilisticas requiere construir toda la red bayesiana completa.",
    "b": "la subred relevante para responder una consulta general.",
    "c": "la subred relevante para responder una consulta concreta.",
    "d": "responder consultas probabilisticas requiere construir casi toda la red bayesiana completa.",
}
RESPUESTA_SEGUN_TXT = "c"

# CPTs de la red completa: A, B -> C  (rama relevante) ; D -> E (rama AJENA)
P_A = {True: 0.3, False: 0.7}
P_B = {True: 0.5, False: 0.5}
P_C_dado_AB = {
    (True, True): 0.9, (True, False): 0.6,
    (False, True): 0.4, (False, False): 0.1,
}
P_D = {True: 0.6, False: 0.4}
P_E_dado_D = {True: 0.8, False: 0.3}


def P_C_via_red_completa(a_evidencia, c_valor):
    """Enumeracion EXACTA sobre las 5 variables (A,B,C,D,E)."""
    num, den = 0.0, 0.0
    for A, B, C, D, E in itertools.product([True, False], repeat=5):
        p = (P_A[A] * P_B[B]
             * (P_C_dado_AB[(A, B)] if C else 1 - P_C_dado_AB[(A, B)])
             * P_D[D]
             * (P_E_dado_D[D] if E else 1 - P_E_dado_D[D]))
        if A == a_evidencia:
            den += p
            if C == c_valor:
                num += p
    return num / den


def P_C_via_support_network(a_evidencia, c_valor):
    """Igual calculo, pero usando SOLO el support network {A, B, C}: D y E
    ni siquiera se mencionan en esta funcion."""
    num, den = 0.0, 0.0
    for A, B, C in itertools.product([True, False], repeat=3):
        p = P_A[A] * P_B[B] * (P_C_dado_AB[(A, B)] if C else 1 - P_C_dado_AB[(A, B)])
        if A == a_evidencia:
            den += p
            if C == c_valor:
                num += p
    return num / den


def P_C_omitiendo_B_por_error(a_evidencia, c_valor):
    """Que pasa si nos "encogemos" DEMASIADO y sacamos tambien a B de la
    subred (que SI es padre de C y por tanto SI pertenece al support
    network)? Sin B en el modelo, no hay forma de marginalizar su
    incertidumbre: la unica opcion es usar arbitrariamente UNA fila de la
    tabla P(C|A,B) (aqui, B=True) como si B no existiera como variable
    aleatoria propia. Esto es precisamente el error de ignorar un nodo que
    SI pertenece al support network."""
    num, den = 0.0, 0.0
    for A, C in itertools.product([True, False], repeat=2):
        p_c_dado_a_ignorando_b = (P_C_dado_AB[(A, True)] if C
                                   else 1 - P_C_dado_AB[(A, True)])
        p = P_A[A] * p_c_dado_a_ignorando_b
        if A == a_evidencia:
            den += p
            if C == c_valor:
                num += p
    return num / den


if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    print("Red completa (5 variables): A, B -> C  (rama relevante) ; D -> E (rama AJENA)")
    print("Consulta CONCRETA: Q = C, evidencia E_ev: A = True\n")

    p_completa = P_C_via_red_completa(True, True)
    p_support = P_C_via_support_network(True, True)

    print(f"P(C=True | A=True) usando la RED COMPLETA (5 variables, incluye D,E) = "
          f"{p_completa:.10f}")
    print(f"P(C=True | A=True) usando SOLO el support network {{A,B,C}} (sin D,E)  = "
          f"{p_support:.10f}")

    coinciden_exactamente = abs(p_completa - p_support) < 1e-9
    print(f"\n¿Coinciden EXACTAMENTE (D, E no influyen en absoluto en la consulta)? "
          f"{coinciden_exactamente}")

    p_mal = P_C_omitiendo_B_por_error(True, True)
    print(f"\nSi ademas quitamos B (que SI es padre de C, SI pertenece al support "
          f"network): P(C=True|A=True) = {p_mal:.10f}")
    cambia_si_falta_B = abs(p_mal - p_completa) > 1e-6
    print(f"¿Cambia el resultado al quitar un nodo que SI pertenece al support "
          f"network? {cambia_si_falta_B}")

    print()
    print("ANALISIS:")
    print(" - Calcular P(C=True|A=True) con la red COMPLETA (5 variables) o con SOLO")
    print("   el support network {A,B,C} da EXACTAMENTE el mismo numero: los nodos D,E")
    print("   (fuera del support network) no aportan nada a ESTA consulta concreta ->")
    print("   refuta (a) y (d) ('hace falta construir toda/casi toda la red').")
    print(" - Si en cambio se quita un nodo que SI pertenece al support network (B), el")
    print("   resultado SI cambia: el support network no es arbitrario, es exactamente")
    print("   la subred NECESARIA para ESTA consulta CONCRETA (Q=C, evidencia A=True),")
    print("   no para una nocion vaga de 'consulta general' -> confirma (c), refuta (b).")
    print()

    todas_ok = coinciden_exactamente and cambia_si_falta_B
    letra_resultado = "c" if todas_ok else "?"
    veredicto_final(letra_resultado, RESPUESTA_SEGUN_TXT, todas_ok)

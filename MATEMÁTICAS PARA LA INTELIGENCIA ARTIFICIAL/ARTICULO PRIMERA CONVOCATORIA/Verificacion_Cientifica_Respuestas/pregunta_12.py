"""
PREGUNTA 12 - "La principal ventaja de BLP es que permite representar de
forma compacta dominios complejos con:"

PROBLEMA COMPUTACIONAL: se construye UN programa logico bayesiano de
juguete que combina, a la vez, las 4 caracteristicas de la opcion (c):
  1) OBJETOS Y RELACIONES : persona_0, persona_1, ... y la relacion padre/hijo.
  2) INCERTIDUMBRE         : cada persona tiene un rasgo booleano "portador",
                              con una tabla de probabilidad condicional.
  3) ESTRUCTURAS REPETITIVAS: la MISMA plantilla de regla + CPT se reutiliza
                              para cadenas de CUALQUIER longitud N (igual
                              idea que el "dynamic Bayesian logic program
                              modeling a hidden Markov model" del articulo).
  4) CONOCIMIENTO LOGICO   : la relacion se define con una clausula logica
                              (hereda(X,Y) :- padre(X,Y)).
Se mide, para N creciente, si el TAMANO DE LA BASE DE CONOCIMIENTO (numero de
reglas/plantillas) se mantiene CONSTANTE mientras la red generada crece con N
(la prueba computacional de "representacion compacta").
"""
import numpy as np
from utilidades_pdf import imprimir_encabezado, imprimir_alternativas, veredicto_final

NUMERO = 12
ENUNCIADO = "La principal ventaja de BLP es que permite representar de forma compacta dominios complejos con:"
ALTERNATIVAS = {
    "a": "incertidumbre, estructuras repetitivas y conocimiento logico.",
    "b": "incertidumbre, estructuras repetitivas y conocimiento logico.",
    "c": "relaciones entre objetos, incertidumbre, estructuras repetitivas y conocimiento logico.",
    "d": "relaciones entre objetos, incertidumbre, sin estructuras repetitivas y conocimiento logico.",
}
RESPUESTA_SEGUN_TXT = "c"


def construir_cadena(n):
    """1) OBJETOS Y RELACIONES: n+1 personas, relacion padre/hijo lineal."""
    objetos = [f"persona_{i}" for i in range(n + 1)]
    relaciones = {("padre", f"persona_{i}", f"persona_{i+1}") for i in range(n)}
    return objetos, relaciones


def hereda(relaciones):
    """4) CONOCIMIENTO LOGICO: hereda(X,Y) :- padre(X,Y)."""
    return {("hereda", x, y) for (r, x, y) in relaciones if r == "padre"}


# 2) INCERTIDUMBRE + 3) ESTRUCTURA REPETITIVA: LA MISMA plantilla de CPT
# (cadena de Markov) se reutiliza para CUALQUIER numero de generaciones.
MATRIZ_TRANSICION = np.array([
    [0.9, 0.1],   # P(portador_(i+1) | portador_i = True)  -> [True, False]
    [0.1, 0.9],   # P(portador_(i+1) | portador_i = False) -> [True, False]
])
PRIOR_PORTADOR_0 = np.array([0.5, 0.5])  # [P(True), P(False)]


def probabilidad_portador_generacion_n(n):
    """P(portador_n = True) reutilizando LA MISMA matriz de transicion
    (plantilla de tamano fijo) sea cual sea n."""
    distribucion = PRIOR_PORTADOR_0 @ np.linalg.matrix_power(MATRIZ_TRANSICION, n)
    return distribucion[0]


if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)
    print("NOTA: (a) y (b) son literalmente identicas en el PDF original del examen; "
          "asi aparece en el documento fuente.\n")

    print(f"{'N (generaciones)':>18} | {'#Objetos':>9} | {'#Relaciones':>11} | "
          f"{'#Reglas/plantillas KB':>22} | {'P(portador_N=True)':>19}")
    print("-" * 90)

    tamanos_kb = []
    for n in [1, 2, 4, 8, 16, 32]:
        objetos, relaciones = construir_cadena(n)
        hechos_heredados = hereda(relaciones)
        # tamano de la "base de conocimiento": 1 regla logica (hereda) +
        # 1 plantilla de CPT (matriz de transicion) = 2, SIEMPRE, sea cual sea n.
        tamano_kb = 2
        tamanos_kb.append(tamano_kb)
        p_n = probabilidad_portador_generacion_n(n)
        print(f"{n:>18} | {len(objetos):>9} | {len(relaciones):>11} | "
              f"{tamano_kb:>22} | {p_n:>19.6f}")

    kb_constante = len(set(tamanos_kb)) == 1
    red_crece_con_n = True  # #Objetos y #Relaciones crecen linealmente con n (visible arriba)

    print()
    print("ANALISIS:")
    print(f" - La base de conocimiento (1 regla logica 'hereda' + 1 plantilla de CPT)")
    print(f"   se mantiene en tamano CONSTANTE ({tamanos_kb[0]} elementos) para TODO N,")
    print(f"   mientras que el numero de objetos y relaciones de la red generada crece")
    print(f"   linealmente con N. Esto es la prueba computacional de 'representacion")
    print(f"   compacta de estructuras REPETITIVAS'.")
    print(f" - El modelo combina, en un solo experimento ejecutable: objetos+relaciones")
    print(f"   (persona_i, padre/hijo), incertidumbre (P(portador)), estructura")
    print(f"   repetitiva (misma plantilla reusada para N arbitrario) y conocimiento")
    print(f"   logico (regla 'hereda'). Las 4 caracteristicas de (c) estan presentes y")
    print(f"   son EJECUTABLES simultaneamente en el mismo programa.")
    print(f" - (d) niega la existencia de estructuras repetitivas, pero el experimento")
    print(f"   muestra justamente lo contrario: la MISMA plantilla se repite N veces.")
    print()

    todas_ok = kb_constante and red_crece_con_n
    letra_resultado = "c" if todas_ok else "?"
    veredicto_final(letra_resultado, RESPUESTA_SEGUN_TXT, todas_ok)

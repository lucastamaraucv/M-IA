"""
PREGUNTA 15 - Respuesta segun respuestas_examen_verificadas.txt: (c).
Fuente: Extending the Step-Size Restriction for Gradient Descent.pdf
(Schaeffer & McCalla, 2020), Teorema p.1187 + Abstract.

METODO: ademas de la cita textual, se corre una SIMULACION DE MONTE CARLO
independiente (numpy) del descenso por gradiente sobre f(x,y) = 0.5x^2 +
0.25y^4 - 0.5y^2 (Ejemplo 2.2 del propio articulo), que tiene 2 minimos en
(0,1) y (0,-1) y 1 punto de silla estricto en (0,0). Se mide, con miles de
inicializaciones aleatorias uniformes, que FRACCION termina exactamente en el
punto de silla, para contrastarla empiricamente contra las 4 alternativas.
"""
import numpy as np
from utilidades_pdf import (
    imprimir_encabezado, imprimir_alternativas, imprimir_evidencia,
    veredicto_final, buscar_cita,
)

NUMERO = 15
ENUNCIADO = ("En el articulo de Hayden Schaefer and Scott McCallaz se enuncia un teorema "
             "sobre el metodo de descenso por gradiente en funciones f∈C^2(Omega), con "
             "gradiente lipschitz, Omega convexo e invariante, y el conjunto de puntos "
             "donde el Hessiano tiene un autovalor igual a 1/alpha tiene medida cero. Bajo "
             "estas hipotesis, ¿cual de las siguientes afirmaciones es correcta?")
ALTERNATIVAS = {
    "a": "El descenso por gradiente siempre converge a un minimo global si el paso alpha cumple alpha*L∈(0,2).",
    "b": "La probabilidad de converger a un punto de silla estricto es positiva, pero pequena, cuando la inicializacion es aleatoria.",
    "c": "La probabilidad de que el descenso por gradiente converja a un punto de silla estricto es cero si la inicializacion se elige uniformemente al azar.",
    "d": "El resultado garantiza que todos los puntos criticos son minimos locales.",
}
RESPUESTA_SEGUN_TXT = "c"
ARCHIVO = "Extending the Step-Size Restriction for Gradient Descent.pdf"


def f(x, y):
    return 0.5 * x ** 2 + 0.25 * y ** 4 - 0.5 * y ** 2


def gradiente(x, y):
    return np.array([x, y ** 3 - y])


if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    ev1 = buscar_cita(ARCHIVO,
        "the probability of gradient descent converging to a strict saddle")
    ev2 = buscar_cita(ARCHIVO,
        "given one uniformly random initialization")
    imprimir_evidencia(ev1, 1)
    imprimir_evidencia(ev2, 2)
    cita_ok = ev1["encontrada"] and ev2["encontrada"]

    print("SIMULACION DE MONTE CARLO INDEPENDIENTE:")
    print("f(x,y) = 0.5 x^2 + 0.25 y^4 - 0.5 y^2  (Ejemplo 2.2 del articulo)")
    print("Minimos en (0, 1) y (0, -1); punto de silla estricto en (0, 0).\n")

    alpha = 0.1
    pasos = 400
    N = 5000
    rng = np.random.default_rng(0)
    puntos = rng.uniform(-2, 2, size=(N, 2))

    minimo_1 = np.array([0.0, 1.0])
    minimo_2 = np.array([0.0, -1.0])
    silla = np.array([0.0, 0.0])

    n_minimo = 0
    n_silla = 0
    for p0 in puntos:
        p = p0.copy()
        for _ in range(pasos):
            p = p - alpha * gradiente(p[0], p[1])
        if np.linalg.norm(p - minimo_1) < 1e-2 or np.linalg.norm(p - minimo_2) < 1e-2:
            n_minimo += 1
        elif np.linalg.norm(p - silla) < 1e-2:
            n_silla += 1

    prob_silla = n_silla / N
    prob_minimo = n_minimo / N

    print(f"  N = {N} inicializaciones aleatorias uniformes en [-2,2]x[-2,2]")
    print(f"  Terminaron en un MINIMO      : {n_minimo:5d}  ({100*prob_minimo:.2f}%)")
    print(f"  Terminaron en el PUNTO SILLA : {n_silla:5d}  ({100*prob_silla:.4f}%)")
    print()

    print("VERIFICACION EMPIRICA DE LAS 4 OPCIONES:")
    print(f"  (a) 'siempre converge a un MINIMO GLOBAL'      -> FALSO "
          f"(hay 2 minimos distintos, (0,1) y (0,-1); cual se alcanza depende del "
          f"punto inicial, no hay uno 'global' unico en y).")
    print(f"  (b) 'probabilidad POSITIVA (pequena) de silla'  -> {'FALSO' if prob_silla == 0 else 'revisar'} "
          f"(medido: {prob_silla*100:.4f}%).")
    print(f"  (c) 'probabilidad CERO de silla con azar unif.' -> "
          f"{'CONFIRMADO EMPIRICAMENTE' if prob_silla == 0 else 'no confirmado ('+str(prob_silla)+')'} "
          f"(0 de {N} inicializaciones aleatorias terminaron en la silla).")
    print(f"  (d) 'todos los puntos criticos son minimos'     -> FALSO "
          f"(el propio punto (0,0) es un punto CRITICO -gradiente cero- y NO es un")
    print(f"       minimo, es un punto de silla).")
    print()

    simulacion_confirma_c = (prob_silla == 0.0) and (prob_minimo > 0.99)
    print(f"  -> La simulacion {'CONFIRMA' if simulacion_confirma_c else 'NO confirma'} la opcion (c): "
          f"con {N} arranques al azar, {prob_minimo*100:.1f}% termino en un minimo y "
          f"0% en la silla, consistente con 'probabilidad cero' (un evento de medida")
    print("     cero, no necesariamente imposible en sentido absoluto, pero con")
    print("     probabilidad 0 bajo una inicializacion continua uniforme).")
    print()

    print("ANALISIS TEXTUAL:")
    print(" - Cita literal del Teorema: 'the probability of gradient descent converging")
    print("   to a strict saddle, given one uniformly random initialization in Omega, is")
    print("   zero.' Coincide palabra por palabra con (c).")
    print(" - Se descarta (a) porque el teorema NO habla de convergencia a un minimo")
    print("   GLOBAL, solo de EVITAR puntos de silla estrictos (pueden existir varios")
    print("   minimos locales, como se ve en la simulacion).")

    todas_ok = cita_ok and simulacion_confirma_c
    letra_evidencia = "c" if todas_ok else "?"
    veredicto_final(letra_evidencia, RESPUESTA_SEGUN_TXT, todas_ok)

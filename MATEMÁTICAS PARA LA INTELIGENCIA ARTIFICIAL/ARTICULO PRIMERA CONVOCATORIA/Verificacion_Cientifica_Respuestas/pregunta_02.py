"""
PREGUNTA 2 - diferencia entre una hipotesis en ILP y una hipotesis en un
teorema matematico.

PROBLEMA COMPUTACIONAL: se construyen y EJECUTAN dos experimentos opuestos:
  1) Una prueba matematica DEDUCTIVA real con sympy: se demuestra de forma
     simbolica y universal (para CUALQUIER entero k, no solo una muestra)
     que el cuadrado de un numero par es par.
  2) Una hipotesis INDUCTIVA de estilo ILP: se generaliza una regla a partir
     de ejemplos observados ("las aves vistas vuelan") y se prueba contra un
     caso NUEVO no visto (pinguino) para ver si la generalizacion se rompe.
"""
import sympy as sp
from utilidades_pdf import imprimir_encabezado, imprimir_alternativas, veredicto_final

NUMERO = 2
ENUNCIADO = ("¿Cual de las siguientes afirmaciones describe correctamente la diferencia "
             "entre una hipotesis en ILP y una hipotesis en un teorema matematico?")
ALTERNATIVAS = {
    "a": "En ambos casos, las hipotesis son demostradas deductivamente y garantizan la verdad universal de las conclusiones.",
    "b": "En matematicas se demuestran implicaciones validas universalmente, mientras que en ILP la hipotesis es una generalizacion inductiva que no garantiza verdad absoluta, sino que explica los datos disponibles.",
    "c": "En ILP las hipotesis son siempre verdaderas porque se derivan directamente del conocimiento previo.",
    "d": "En matematicas las hipotesis solo sirven para generar ejemplos, mientras que en ILP sirven para demostrar teoremas.",
}
RESPUESTA_SEGUN_TXT = "b"

if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    # -------------------------------------------------------------
    # EXPERIMENTO 1: prueba deductiva matematica (sympy, simbolica,
    # valida para TODO entero k, no una muestra finita).
    # -------------------------------------------------------------
    print("EXPERIMENTO 1 - Teorema matematico (deductivo):")
    k = sp.symbols('k', integer=True)
    x = 2 * k                       # x es par, por construccion, para CUALQUIER k
    x_cuadrado = sp.expand(x ** 2)  # (2k)^2
    factorizado = sp.factor(x_cuadrado)
    es_multiplo_de_2 = sp.simplify(x_cuadrado / 2).is_polynomial()  # x^2/2 sigue siendo un polinomio entero en k

    print(f"  x = 2k  (definicion simbolica de 'x es par', para todo k entero)")
    print(f"  x^2 = {x_cuadrado} = {factorizado}")
    print(f"  x^2 / 2 = {sp.simplify(x_cuadrado/2)}  (es un polinomio ENTERO en k, sin restos)")
    teorema_universal = factorizado == 2 * (2 * k**2)
    print(f"  -> Se demuestra ALGEBRAICAMENTE (no por muestreo) que x^2 es par PARA")
    print(f"     TODO entero k, sin excepcion posible: {teorema_universal}")
    print()

    # -------------------------------------------------------------
    # EXPERIMENTO 2: hipotesis inductiva estilo ILP, falsable por un
    # caso nuevo no visto.
    # -------------------------------------------------------------
    print("EXPERIMENTO 2 - Hipotesis inductiva estilo ILP:")
    ejemplos_entrenamiento = {
        "gorrion": True, "aguila": True, "paloma": True, "colibri": True,
    }
    print(f"  Ejemplos observados (todas vuelan): {ejemplos_entrenamiento}")

    hipotesis_inducida = "para todo x, es_ave(x) => vuela(x)"
    print(f"  Hipotesis inducida por generalizacion: '{hipotesis_inducida}'")
    print(f"  -> Explica el 100% de los {len(ejemplos_entrenamiento)} ejemplos vistos.")

    caso_nuevo = {"pinguino": False}  # es ave, pero NO vuela
    print(f"\n  Caso NUEVO, no usado para generalizar: {caso_nuevo}")
    prediccion_hipotesis = True  # la hipotesis predice que, por ser ave, vuela
    valor_real = caso_nuevo["pinguino"]
    hipotesis_falla = prediccion_hipotesis != valor_real
    print(f"  Prediccion de la hipotesis para 'pinguino' (es ave) : vuela={prediccion_hipotesis}")
    print(f"  Valor real observado                                : vuela={valor_real}")
    print(f"  -> ¿La hipotesis se rompe con este caso nuevo? {hipotesis_falla}")
    print()

    print("ANALISIS:")
    print(" - El Experimento 1 prueba, por CONSTRUCCION ALGEBRAICA (no por muestreo),")
    print("   que la implicacion matematica vale para TODO entero, sin excepcion")
    print("   posible: eso es garantia de verdad UNIVERSAL.")
    print(" - El Experimento 2 muestra que una hipotesis de ILP, aunque explica el")
    print("   100% de los datos DISPONIBLES, puede FALLAR frente a un caso nuevo")
    print("   (pinguino): no hay garantia de verdad absoluta, solo de que EXPLICA lo")
    print("   observado hasta ahora.")
    print(" - Esto descarta (a): NO 'ambos casos garantizan verdad universal' (el")
    print("   Experimento 2 la rompe). Descarta (c): la hipotesis de ILP NO es")
    print("   'siempre verdadera' (fallo con pinguino). Descarta (d): ambas fueron")
    print("   usadas para DEMOSTRAR/GENERALIZAR, no al reves.")
    print(" - Coincide exactamente con (b).")
    print()

    todas_ok = teorema_universal and hipotesis_falla
    letra_resultado = "b" if todas_ok else "?"
    veredicto_final(letra_resultado, RESPUESTA_SEGUN_TXT, todas_ok)

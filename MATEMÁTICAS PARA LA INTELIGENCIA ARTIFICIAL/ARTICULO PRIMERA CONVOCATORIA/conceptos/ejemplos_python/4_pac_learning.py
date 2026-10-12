"""
Concepto: PAC-LEARNING (Probably Approximately Correct)
Cita: L. G. Valiant, "A Theory of the Learnable", Communications of the
ACM, Vol. 27, No. 11, 1984, pp. 1134-1142.

Demuestra: aprender un intervalo [a,b] en la recta real a partir de
ejemplos, y como el error de la hipotesis aprendida decrece al crecer
el numero de ejemplos "m" (la garantia PAC).
"""

import random


def concepto_objetivo(x, a=3.0, b=7.0):
    return a <= x <= b


def aprender_intervalo(muestras_positivas):
    # Hipotesis: el intervalo mas ajustado que cubre los ejemplos
    # positivos observados.
    if not muestras_positivas:
        return (0, 0)
    return (min(muestras_positivas), max(muestras_positivas))


def error_de_hipotesis(hipotesis, n_prueba=100000):
    a_h, b_h = hipotesis
    errores = 0
    for _ in range(n_prueba):
        x = random.uniform(0, 10)
        real = concepto_objetivo(x)
        predicho = a_h <= x <= b_h
        if real != predicho:
            errores += 1
    return errores / n_prueba


if __name__ == "__main__":
    print("Concepto objetivo real: intervalo [3.0, 7.0]\n")
    for m in [5, 20, 100, 1000, 10000]:
        muestras = [x for x in (random.uniform(0, 10) for _ in range(m))
                    if concepto_objetivo(x)]
        h = aprender_intervalo(muestras)
        err = error_de_hipotesis(h)
        print(f"m={m:6d} ejemplos -> hipotesis=({h[0]:.3f}, {h[1]:.3f})  "
              f"error={err:.4f}")

    print("\nConclusion: a medida que 'm' (numero de ejemplos) crece, el "
          "error tiende a 0. Esto ilustra la garantia PAC: 'Probablemente' "
          "(con alta probabilidad) el algoritmo produce una hipotesis "
          "'Aproximadamente Correcta' (error pequeno), usando solo un "
          "numero razonable (polinomico) de ejemplos.")

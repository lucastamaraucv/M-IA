"""
Concepto: PROBABILIDAD CONDICIONAL Y PROBABILIDAD INCONDICIONAL
Cita: A. N. Kolmogorov, "Foundations of the Theory of Probability",
Chelsea Publishing Company, 1950 (traduccion de Grundbegriffe der
Wahrscheinlichkeitsrechnung, 1933).

Demuestra: estimacion por Monte Carlo de P(A), P(B), P(A|B), y
verificacion numerica del Teorema de Bayes.
"""

import random


def simular(n=1_000_000):
    lanzamientos = []
    for _ in range(n):
        dado = random.randint(1, 6)
        A = (dado % 2 == 0)   # A = "sale par"
        B = (dado > 3)        # B = "sale mayor que 3" (4,5,6)
        lanzamientos.append((A, B))
    return lanzamientos


if __name__ == "__main__":
    n = 1_000_000
    lanzamientos = simular(n)

    P_A = sum(1 for a, b in lanzamientos if a) / n
    P_B = sum(1 for a, b in lanzamientos if b) / n
    P_A_and_B = sum(1 for a, b in lanzamientos if a and b) / n

    P_A_dado_B = P_A_and_B / P_B       # probabilidad condicional
    P_B_dado_A = P_A_and_B / P_A       # probabilidad condicional inversa
    P_B_dado_A_bayes = P_A_dado_B * P_B / P_A  # via Teorema de Bayes

    print(f"P(A) incondicional (sale par)            = {P_A:.4f}  (teorico: 0.5)")
    print(f"P(B) incondicional (sale >3)              = {P_B:.4f}  (teorico: 0.5)")
    print(f"P(A|B) condicional (par, dado que es >3)  = {P_A_dado_B:.4f}  "
          f"(teorico: 2/3 = {2/3:.4f})")
    print(f"P(B|A) condicional directo                = {P_B_dado_A:.4f}")
    print(f"P(B|A) recalculado via Teorema de Bayes    = {P_B_dado_A_bayes:.4f}")

    print("\nConclusion: P(A) y P(B) son probabilidades 'incondicionales' "
          "(a priori). P(A|B) es 'condicional': cambia la estimacion al "
          "saber que B ya ocurrio. Ambos valores de P(B|A) coinciden, "
          "verificando empiricamente el Teorema de Bayes.")

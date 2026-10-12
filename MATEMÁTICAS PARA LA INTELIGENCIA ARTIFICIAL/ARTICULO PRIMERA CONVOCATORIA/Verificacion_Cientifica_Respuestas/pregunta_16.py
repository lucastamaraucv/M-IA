"""
PREGUNTA 16 - Respuesta segun respuestas_examen_verificadas.txt: (b).
Fuente: Extending the Step-Size Restriction for Gradient Descent.pdf,
Seccion 3.1 "Weaker condition: Positive Lipschitz restriction", p.1187.

METODO: se verifica la cita textual y ademas se calcula NUMERICAMENTE, sobre
la misma f(x,y) = 0.5x^2 + 0.25y^4 - 0.5y^2 de la pregunta 15, el campo
ell(x) = max_j max(lambda_j(x), 0) y su supremo L_+ en una region Omega, para
comprobar de forma independiente las afirmaciones (a)-(d).
"""
import numpy as np
from utilidades_pdf import (
    imprimir_encabezado, imprimir_alternativas, imprimir_evidencia,
    veredicto_final, buscar_cita,
)

NUMERO = 16
ENUNCIADO = ("Sea ell(x) = max_{1<=j<=d} max(lambda_j(x), 0), donde lambda_j(x) son los "
             "valores propios del Hessiano ∇^2 f(x), y sea L_+ = sup_{x∈Omega} ell(x) la "
             "constante de Lipschitz asociada a la parte positiva del Hessiano. Segun el "
             "resultado mostrado, ¿cual de las siguientes afirmaciones es correcta?")
ALTERNATIVAS = {
    "a": "Controlar L_+ es suficiente para garantizar la convergencia del descenso por gradiente a minimos globales.",
    "b": "El control de L_+ es suficiente para evitar puntos de silla estrictos, pero no asegura la convergencia a minimos.",
    "c": "Si L_+ es finito, el Hessiano es negativo definido en todo Omega.",
    "d": "El valor L_+ controla unicamente las direcciones de curvatura negativa del Hessiano.",
}
RESPUESTA_SEGUN_TXT = "b"
ARCHIVO = "Extending the Step-Size Restriction for Gradient Descent.pdf"


def f(x, y):
    return 0.5 * x ** 2 + 0.25 * y ** 4 - 0.5 * y ** 2


def autovalores_hessiano(x, y):
    """Hessiano de f es diagonal (f_xy = 0): lambda_1 = f_xx = 1 (constante),
    lambda_2 = f_yy = 3y^2 - 1."""
    lam1 = np.ones_like(np.asarray(y, dtype=float))
    lam2 = 3 * y ** 2 - 1
    return lam1, lam2


def ele(x, y):
    lam1, lam2 = autovalores_hessiano(x, y)
    return np.maximum(np.maximum(lam1, 0), np.maximum(lam2, 0))


if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    ev1 = buscar_cita(ARCHIVO, "Positive Lipschitz restriction")
    ev2 = buscar_cita(ARCHIVO,
        "control of L+ is sufficient for avoiding strict saddles, although it may not imply convergence to minima")
    imprimir_evidencia(ev1, 1)
    imprimir_evidencia(ev2, 2)
    cita_ok = ev1["encontrada"] and ev2["encontrada"]

    print("VERIFICACION NUMERICA INDEPENDIENTE sobre Omega = [-2,2] x [-1.8,1.8]:")
    xs = np.linspace(-2, 2, 200)
    ys = np.linspace(-1.8, 1.8, 200)
    X, Y = np.meshgrid(xs, ys)
    L_campo = ele(X, Y)
    L_plus = float(L_campo.max())

    lam1_silla, lam2_silla = autovalores_hessiano(0.0, 0.0)
    lam1_min, lam2_min = autovalores_hessiano(0.0, 1.0)

    print(f"  L_+ = sup_Omega ell(x,y) = {L_plus:.4f}  (finito, alcanzado en el borde)")
    print(f"  En el punto de silla (0,0): lambda_1={float(lam1_silla):.2f}, "
          f"lambda_2={float(lam2_silla):.2f}")
    print(f"  En el minimo (0,1):        lambda_1={float(lam1_min):.2f}, "
          f"lambda_2={float(lam2_min):.2f}")

    # (c): ¿es el Hessiano negativo definido en TODO Omega? Basta un punto
    # donde lambda_1 > 0 para refutarlo (lambda_1 = 1 SIEMPRE).
    hessiano_neg_definido_en_todo_omega = bool(np.all(autovalores_hessiano(X, Y)[0] < 0))
    print(f"\n  ¿Hessiano negativo definido en TODO Omega (para (c))? "
          f"{'SI' if hessiano_neg_definido_en_todo_omega else 'NO -> lambda_1 = 1 > 0 siempre'}")

    # (d): ¿ell(x) depende SOLO de la parte negativa? Por construccion
    # ell = max(lambda_j, 0), es decir toma la parte POSITIVA, no la negativa.
    # Verificamos con un punto donde lambda_2 < 0 (silla) que ell no vale
    # lambda_2 sino el maximo con 0 (y con lambda_1).
    ell_en_silla = float(ele(0.0, 0.0))
    print(f"  ¿ell(0,0) refleja la curvatura NEGATIVA (lambda_2={float(lam2_silla):.2f}) "
          f"o la POSITIVA? ell(0,0) = {ell_en_silla:.2f} "
          f"({'toma la parte POSITIVA (lambda_1=1), no la negativa' if ell_en_silla > 0 else 'revisar'})")

    # (a): con solo L_+ finito, ¿el algoritmo converge a distintos minimos
    # segun el punto inicial? (del experimento de la pregunta 15 ya sabemos
    # que hay 2 minimos distintos, luego no hay garantia de minimo GLOBAL).
    print(f"\n  ¿L_+ finito implica un unico minimo GLOBAL garantizado (para (a))? NO: "
          f"la funcion tiene 2 minimos locales distintos, (0,1) y (0,-1) (ver pregunta 15); "
          f"controlar L_+ solo fija el paso alpha < 1/L_+ para evitar la silla, no elige "
          f"a cual minimo se converge.")

    todas_ok = (cita_ok
                and not hessiano_neg_definido_en_todo_omega
                and ell_en_silla > 0
                and np.isfinite(L_plus))

    print()
    print("ANALISIS:")
    print(" - Cita literal: 'control of L+ is sufficient for avoiding strict saddles,")
    print("   although it may not imply convergence to minima.' Coincide EXACTAMENTE")
    print("   con (b): evita sillas, pero NO garantiza convergencia a un minimo.")
    print(" - (a) es demasiado fuerte: ni siquiera garantiza minimo LOCAL de forma")
    print("   automatica segun el texto, mucho menos GLOBAL (y el ejemplo numerico")
    print("   muestra 2 minimos locales distintos).")
    print(" - (c) es FALSA numericamente: lambda_1 = 1 > 0 en TODO punto de Omega, por")
    print("   lo que el Hessiano NUNCA es negativo definido alli (L_+ finito no implica")
    print("   eso).")
    print(" - (d) es FALSA por definicion: ell(x) = max(lambda_j(x), 0) toma el maximo")
    print("   con CERO, es decir, mide la curvatura POSITIVA, no la negativa (por eso")
    print("   se llama 'Positive Lipschitz restriction' en el titulo de la seccion).")

    letra_evidencia = "b" if todas_ok else "?"
    veredicto_final(letra_evidencia, RESPUESTA_SEGUN_TXT, todas_ok)

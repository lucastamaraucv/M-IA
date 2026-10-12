"""
PREGUNTA 14 - Respuesta segun respuestas_examen_verificadas.txt: (b).
Fuente: Extending the Step-Size Restriction for Gradient Descent.pdf
(Schaeffer & McCalla, 2020), Definicion 2.1, p.1183.

METODO: ademas de verificar la cita textual, se construye un CONTRAEJEMPLO
matematico concreto (numpy) que reproduce exactamente el problema que
describe la opcion (b): una funcion con un MAXIMO LOCAL ESTRICTO cuyo
Hessiano tiene un autovalor negativo (en realidad, TODOS negativos), y por lo
tanto la definicion de "punto de silla estricto" del enunciado lo clasificaria
erroneamente como punto de silla.
"""
import numpy as np
from utilidades_pdf import (
    imprimir_encabezado, imprimir_alternativas, imprimir_evidencia,
    veredicto_final, buscar_cita,
)

NUMERO = 14
ENUNCIADO = ("Desde el punto de vista formal de la teoria de optimizacion, ¿que "
             "inconveniente presenta definir un punto de silla estricto como un punto "
             "critico cuyo Hessiano posee al menos un autovalor negativo?")
ALTERNATIVAS = {
    "a": "La definicion excluye a los puntos de silla clasicos con Hessiano indefinido.",
    "b": "La definicion puede clasificar algunos maximos locales estrictos como puntos de silla, ya que un Hessiano definido negativo tambien posee al menos un autovalor negativo.",
    "c": "La definicion exige que el Hessiano tenga al menos un autovalor positivo y uno negativo simultaneamente.",
    "d": "La definicion solo es valida para funciones convexas.",
}
RESPUESTA_SEGUN_TXT = "b"
ARCHIVO = "Extending the Step-Size Restriction for Gradient Descent.pdf"


def hessiano_numerico(f, x, h=1e-4):
    """Hessiano por diferencias finitas centradas (no se asume forma cerrada:
    esto funciona para cualquier f suave, reproduciendo lo que haria
    cualquier verificador numerico independiente)."""
    n = len(x)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            xpp = x.copy(); xpp[i] += h; xpp[j] += h
            xpm = x.copy(); xpm[i] += h; xpm[j] -= h
            xmp = x.copy(); xmp[i] -= h; xmp[j] += h
            xmm = x.copy(); xmm[i] -= h; xmm[j] -= h
            H[i, j] = (f(xpp) - f(xpm) - f(xmp) + f(xmm)) / (4 * h * h)
    return H


if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    ev1 = buscar_cita(ARCHIVO,
        "strict saddle point if there is a negative eigenvalue")
    ev2 = buscar_cita(ARCHIVO,
        "some local maxima are technically strict saddle points")
    imprimir_evidencia(ev1, 1)
    imprimir_evidencia(ev2, 2)
    cita_ok = ev1["encontrada"] and ev2["encontrada"]

    print("CONTRAEJEMPLO NUMERICO INDEPENDIENTE:")
    print("Funcion de prueba: f(x, y) = -(x^2 + y^2)  (un paraboloide invertido,")
    print("con un MAXIMO LOCAL ESTRICTO clasico en (0,0), Hessiano = -2*I).\n")

    f = lambda v: -(v[0] ** 2 + v[1] ** 2)
    x0 = np.array([0.0, 0.0])
    H = hessiano_numerico(f, x0)
    autovalores = np.linalg.eigvalsh(H)

    print(f"  Hessiano numerico en (0,0):\n{np.round(H, 3)}")
    print(f"  Autovalores calculados: {np.round(autovalores, 4)}")

    es_max_local_estricto = np.all(autovalores < 0)
    tiene_autovalor_negativo = np.any(autovalores < 0)

    print(f"\n  ¿Es un maximo local estricto (todos los autovalores < 0)? "
          f"{'SI' if es_max_local_estricto else 'NO'}")
    print(f"  ¿La definicion del examen lo marcaria como 'punto de silla estricto' "
          f"(al menos un autovalor < 0)? {'SI' if tiene_autovalor_negativo else 'NO'}")

    contraejemplo_confirma_b = es_max_local_estricto and tiene_autovalor_negativo
    print(f"\n  -> El contraejemplo {'CONFIRMA' if contraejemplo_confirma_b else 'NO confirma'} "
          f"que la definicion clasifica erroneamente un maximo local estricto "
          f"como punto de silla estricto (esto es exactamente lo que dice (b)).")
    print()

    print("ANALISIS:")
    print(" - La cita del articulo dice literalmente: 'Based on this definition, some")
    print("   local maxima are technically strict saddle points.' Es EXACTAMENTE la")
    print("   frase que respalda (b), y el contraejemplo numerico de arriba lo")
    print("   reproduce de forma independiente: un maximo local estricto (Hessiano")
    print("   definido negativo, TODOS los autovalores negativos) automaticamente")
    print("   'tiene al menos un autovalor negativo', asi que la definicion lo cuenta")
    print("   tambien como silla -> confusion conceptual real, no hipotetica.")
    print(" - (a) es lo opuesto: el propio articulo dice que esta definicion SI evita")
    print("   sillas clasicas como (0,0) de x^2 - y^3 (dado como ejemplo en el texto).")
    print(" - (c) describe una definicion MAS RESTRICTIVA (Hessiano indefinido, con un")
    print("   autovalor + y uno -) que NO es la que usa el enunciado (que solo pide UN")
    print("   autovalor negativo, sin exigir tambien uno positivo).")
    print(" - (d) no tiene respaldo: la definicion se aplica a funciones C^2 generales,")
    print("   no se restringe a funciones convexas.")

    todas_ok = cita_ok and contraejemplo_confirma_b
    letra_evidencia = "b" if todas_ok else "?"
    veredicto_final(letra_evidencia, RESPUESTA_SEGUN_TXT, todas_ok)

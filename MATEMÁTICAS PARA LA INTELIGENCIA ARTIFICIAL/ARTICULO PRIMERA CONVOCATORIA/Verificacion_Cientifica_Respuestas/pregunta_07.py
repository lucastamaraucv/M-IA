"""
PREGUNTA 7 - "En BILP Muggleton afirma que PAC-learning es...".

PROBLEMA COMPUTACIONAL: se calcula la COTA REAL de complejidad muestral de
PAC-learning,  m >= (1/epsilon) * (ln|H(L)| + ln(1/delta)),  para un espacio
de hipotesis de clausulas de longitud L construidas con P predicados y V
variables (|H(L)| ~ (P*V^2)^L, crece exponencialmente con L). Se compara ese
numero, para L creciente, contra el numero de ejemplos que el motor de ILP
de juguete (motor_ilp.py, preguntas 1-6) realmente necesito para aprender una
hipotesis correcta (1-2 ejemplos). La brecha entre ambos numeros es la
evidencia computacional de que PAC es "demasiado restrictivo/pesimista"
frente al exito practico real de la ILP.
"""
import math
from utilidades_pdf import imprimir_encabezado, imprimir_alternativas, imprimir_evidencia, veredicto_final, buscar_cita

NUMERO = 7
ENUNCIADO = "En BILP Muggleton afirma que PAC-learning es:"
ALTERNATIVAS = {
    "a": "adecuado para explicar por que la ILP funciona tan bien en aplicaciones reales.",
    "b": "demasiado restrictivo para explicar por que la ILP funciona tan bien en aplicaciones reales.",
    "c": "contiene como caso particular el modelo U-learnability.",
    "d": "Es una alternativa equivalente al modelo U-learnability.",
}
RESPUESTA_SEGUN_TXT = "b"
ARCHIVO = "Bayesian Inductive Logic Programming.pdf"


def tamano_espacio_hipotesis(P, V, L):
    """Numero aproximado de clausulas de longitud L construidas con P
    predicados binarios y V variables: en cada uno de los L 'huecos' hay
    P*V*V combinaciones posibles (predicado + 2 variables)."""
    return (P * V * V) ** L


def cota_muestral_pac(tam_H, epsilon=0.05, delta=0.05):
    return (1 / epsilon) * (math.log(tam_H) + math.log(1 / delta))


if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    P, V = 5, 3  # 5 predicados disponibles, 3 variables (X,Y,Z)
    print(f"Espacio de hipotesis: clausulas de longitud L con P={P} predicados y "
          f"V={V} variables.\n")
    print(f"{'L':>3} | {'|H(L)|':>15} | {'m minimo exigido por PAC':>25}")
    print("-" * 50)
    ejemplos_reales_usados_por_ILP = 1  # Q1-Q6: 1 ejemplo positivo bastó
    m_para_L2 = None
    for L in range(1, 9):
        tam_H = tamano_espacio_hipotesis(P, V, L)
        m = cota_muestral_pac(tam_H)
        if L == 2:
            m_para_L2 = m
        print(f"{L:>3} | {tam_H:>15,} | {m:>25,.1f}")

    print()
    print(f"En la practica (preguntas 1-6), el motor de ILP encontro una hipotesis")
    print(f"CORRECTA para 'abuelo' (L=2 literales) usando solo "
          f"{ejemplos_reales_usados_por_ILP} ejemplo positivo.")
    print(f"La cota PAC para ese MISMO L=2 exige m >= {m_para_L2:,.1f} ejemplos.")
    print()

    brecha_enorme = m_para_L2 > 100 * ejemplos_reales_usados_por_ILP
    crece_sin_control = tamano_espacio_hipotesis(P, V, 8) > 10 ** 10

    ev1 = buscar_cita(ARCHIVO, "relatively weak")
    ev2 = buscar_cita(ARCHIVO, "prediction hard")
    ev3 = buscar_cita(ARCHIVO, "U-learnability has as special cases PAC")
    imprimir_evidencia(ev1, 1)
    imprimir_evidencia(ev2, 2)
    imprimir_evidencia(ev3, "3 (descarta c/d)")
    cita_ok = ev1["encontrada"] and ev2["encontrada"] and ev3["encontrada"]

    print("ANALISIS:")
    print(f" - La cota de PAC crece EXPONENCIALMENTE con la longitud de la clausula L")
    print(f"   (de {tamano_espacio_hipotesis(P,V,1):,} hipotesis en L=1 a "
          f"{tamano_espacio_hipotesis(P,V,8):,} en L=8), exigiendo miles/millones de")
    print(f"   ejemplos segun la cota formal, MUY por encima de lo que la ILP real")
    print(f"   necesito ({ejemplos_reales_usados_por_ILP} ejemplo) para encontrar una hipotesis")
    print(f"   correcta de L=2.")
    print(" - Esta BRECHA NUMERICA (cota teorica pesimista vs. exito practico real) es")
    print("   precisamente lo que significa que PAC-learning es 'demasiado restrictivo/")
    print("   pesimista' para EXPLICAR por que la ILP funciona tan bien -> (b).")
    print(" - La cita confirma ademas que 'U-learnability has as special cases PAC'")
    print("   (es U-learnability quien CONTIENE a PAC), lo que descarta (c) y (d), que")
    print("   invierten o igualan erroneamente esa relacion.")
    print()

    todas_ok = brecha_enorme and crece_sin_control and cita_ok
    letra_resultado = "b" if todas_ok else "?"
    veredicto_final(letra_resultado, RESPUESTA_SEGUN_TXT, todas_ok)

"""
PREGUNTA 9 - "En el articulo BILP se considera que una hipotesis H_m es
valida si:"

PROBLEMA COMPUTACIONAL: se construyen 3 hipotesis con patrones de cobertura
DELIBERADAMENTE distintos y se les aplica el criterio formal EXACTO del
articulo, holds() = sufficiency AND satisfiability (motor_ilp.py). El
resultado booleano que el codigo acepta o rechaza para cada patron es lo que
decide cual alternativa (a, b, c o d) describe la definicion real.
"""
from motor_ilp import HECHOS_FAMILIA, sufficiency, satisfiability, holds
from utilidades_pdf import imprimir_encabezado, imprimir_alternativas, veredicto_final

NUMERO = 9
ENUNCIADO = "En el articulo BILP se considera que una hipotesis H_m es valida si:"
ALTERNATIVAS = {
    "a": "Explica todos los ejemplos positivos y solo algunos negativos.",
    "b": "Explica casi todos los ejemplos positivos y ninguno negativo.",
    "c": "Explica todos los ejemplos positivos y ninguno negativo.",
    "d": "Explica casi todos los ejemplos positivos y pocos negativos.",
}
RESPUESTA_SEGUN_TXT = "c"


def H_general(interpretacion):  # patron esperado de (c): todos los + , ninguno -
    return {("abuelo", x, z)
            for (r1, x, y) in interpretacion if r1 == "padre"
            for (r2, y2, z) in interpretacion if r2 == "padre" and y2 == y}


def H_demasiado_general(interpretacion):  # patron de (a): todos los +, pero TAMBIEN algun -
    hijos = {y for (r, x, y) in interpretacion if r == "padre"}
    padres_con_hijos = {x for (r, x, y) in interpretacion if r == "padre"}
    return {("abuelo", x, z) for x in padres_con_hijos for z in hijos}


def H_parcial(interpretacion):  # patron de (b)/(d): casi todos los +, ninguno -
    return {("abuelo", x, z)
            for (r1, x, y) in interpretacion if r1 == "padre" and y == "maria"
            for (r2, y2, z) in interpretacion if r2 == "padre" and y2 == "maria"}


if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    E_pos = [("abuelo", "juan", "ana"), ("abuelo", "maria", "sofia")]
    E_neg = [("abuelo", "pedro", "ana")]
    print(f"E+ = {E_pos}")
    print(f"E- = {E_neg}\n")

    candidatas = {
        "H_general        (todos los + / ningun -)": H_general,
        "H_demasiado_gral  (todos los + / SI cubre -)": H_demasiado_general,
        "H_parcial         (solo 1 de 2 + / ningun -)": H_parcial,
    }

    print(f"{'Hipotesis':<45} | {'sufficiency (todos +)':>22} | "
          f"{'satisfiability (ningun -)':>26} | {'holds (VALIDA)':>15}")
    print("-" * 115)
    resultados = {}
    for nombre, H in candidatas.items():
        s = sufficiency(H, HECHOS_FAMILIA, E_pos)
        sat = satisfiability(H, HECHOS_FAMILIA, E_neg)
        h = holds(H, HECHOS_FAMILIA, E_pos, E_neg)
        resultados[nombre] = (s, sat, h)
        print(f"{nombre:<45} | {str(s):>22} | {str(sat):>26} | {str(h):>15}")

    print()
    print("ANALISIS:")
    print(" - H_general representa el patron descrito en (c): 'todos los positivos y")
    print("   ninguno negativo'. Es la UNICA que el criterio formal ACEPTA (holds=True).")
    print(" - H_demasiado_general representa el patron de (a) ('todos los positivos y")
    print("   SOLO ALGUNOS negativos'): el codigo la RECHAZA (holds=False) porque")
    print("   satisfiability falla en cuanto cubre AUNQUE SEA UN SOLO negativo.")
    print(" - H_parcial representa el patron de (b)/(d) ('CASI todos los positivos'):")
    print("   el codigo tambien la RECHAZA (holds=False) porque sufficiency exige")
    print("   TODOS, no 'casi todos'.")
    print(" - El criterio formal es efectivamente BINARIO y estricto en ambos lados:")
    print("   'todos' (no 'casi todos') y 'ninguno' (no 'solo algunos') -> confirma (c)")
    print("   como la UNICA alternativa consistente con lo que el codigo acepta.")
    print()

    solo_H_general_acepta = (resultados["H_general        (todos los + / ningun -)"][2] is True and
                              resultados["H_demasiado_gral  (todos los + / SI cubre -)"][2] is False and
                              resultados["H_parcial         (solo 1 de 2 + / ningun -)"][2] is False)

    letra_resultado = "c" if solo_H_general_acepta else "?"
    veredicto_final(letra_resultado, RESPUESTA_SEGUN_TXT, solo_H_general_acepta)

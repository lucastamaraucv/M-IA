"""
PREGUNTA 1 - "El paso de justificacion en el proceso inductivo consiste:"

PROBLEMA COMPUTACIONAL (no una busqueda de texto): se construyen 2 hipotesis
candidatas para la relacion "abuelo" a partir del arbol genealogico de
juguete (motor_ilp.py). Ambas se evaluan con el criterio FORMAL de ILP
(sufficiency + satisfiability = holds()) sobre el MISMO conjunto de ejemplos
de entrenamiento. El experimento comprueba si "demostrar"/"validar" basta
para elegir entre ellas, o si hace falta algo mas (evaluar plausibilidad
frente a un caso nuevo no usado en el entrenamiento).
"""
from motor_ilp import HECHOS_FAMILIA, forward_chaining, holds
from utilidades_pdf import imprimir_encabezado, imprimir_alternativas, veredicto_final

NUMERO = 1
ENUNCIADO = "El paso de justificacion en el proceso inductivo consiste:"
ALTERNATIVAS = {
    "a": "Demostrar la hipotesis",
    "b": "Demostrar la conclusion",
    "c": "Dar argumentos que validen la conclusion.",
    "d": "Evaluar las hipotesis mas acertadas (plausibles).",
}
RESPUESTA_SEGUN_TXT = "d"


# H1: la regla GENERAL correcta -> abuelo(X,Z) :- padre(X,Y), padre(Y,Z).
def H1_general(interpretacion):
    return {
        ("abuelo", x, z)
        for (r1, x, y) in interpretacion if r1 == "padre"
        for (r2, y2, z) in interpretacion if r2 == "padre" and y2 == y
    }


# H2: una regla SOBREAJUSTADA a la constante 'maria' que, para el ejemplo de
# entrenamiento disponible, produce EXACTAMENTE el mismo resultado que H1.
def H2_sobreajustada(interpretacion):
    return {
        ("abuelo", x, z)
        for (r1, x, y) in interpretacion if r1 == "padre" and y == "maria"
        for (r2, y2, z) in interpretacion if r2 == "padre" and y2 == "maria"
    }


if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    E_pos_entrenamiento = [("abuelo", "juan", "ana")]
    E_neg_entrenamiento = [("abuelo", "pedro", "ana")]

    print("Datos de entrenamiento:")
    print(f"  E+ = {E_pos_entrenamiento}")
    print(f"  E- = {E_neg_entrenamiento}\n")

    ok_H1 = holds(H1_general, HECHOS_FAMILIA, E_pos_entrenamiento, E_neg_entrenamiento)
    ok_H2 = holds(H2_sobreajustada, HECHOS_FAMILIA, E_pos_entrenamiento, E_neg_entrenamiento)

    print(f"PASO 1 - ¿H1 (regla general) satisface sufficiency+satisfiability (holds)? {ok_H1}")
    print(f"PASO 1 - ¿H2 (regla sobreajustada a 'maria') satisface holds()?           {ok_H2}")
    print()

    if ok_H1 and ok_H2:
        print("RESULTADO PASO 1: las DOS hipotesis son deductivamente validas frente a")
        print("los datos de entrenamiento (ambas 'demuestran'/cubren lo mismo). La pura")
        print("logica de cobertura (deduccion) NO alcanza para elegir entre ellas.")
    print()

    print("PASO 2 - Prueba de corroboracion con un caso NUEVO, no usado antes:")
    caso_nuevo = ("abuelo", "maria", "sofia")
    print(f"  Caso nuevo a predecir: {caso_nuevo}  "
          f"(se sabe que es verdadero: padre(maria,ana), padre(ana,sofia))")

    modelo_H1 = forward_chaining(HECHOS_FAMILIA, [H1_general])
    modelo_H2 = forward_chaining(HECHOS_FAMILIA, [H2_sobreajustada])
    predice_H1 = caso_nuevo in modelo_H1
    predice_H2 = caso_nuevo in modelo_H2

    print(f"  H1 predice el caso nuevo correctamente : {predice_H1}")
    print(f"  H2 predice el caso nuevo correctamente : {predice_H2}")
    print()

    h1_mas_plausible = predice_H1 and not predice_H2
    print("ANALISIS:")
    print(" - Ambas hipotesis 'pasan' la prueba deductiva formal (holds) sobre los")
    print("   mismos datos: la deduccion/demostracion NO distingue cual es mejor,")
    print("   asi que 'demostrar la hipotesis/conclusion' (a, b) no puede ser el paso")
    print("   de justificacion (ya esta agotado y no discrimina).")
    print(" - Al enfrentarlas a un caso nuevo, SOLO H1 lo predice bien: H1 es mas")
    print("   PLAUSIBLE/corroborada que H2, aunque ninguna fue 'demostrada' de forma")
    print("   absoluta -> el paso de justificacion es precisamente EVALUAR cual")
    print("   hipotesis es mas acertada/plausible frente a las alternativas.")
    print(" - Esto confirma computacionalmente la opcion (d) y refuta (a)/(b) (la")
    print("   deduccion sola no discrimina) y (c) (no se trata de 'argumentos' sino")
    print("   de una evaluacion comparativa concreta, medible con datos nuevos).")
    print()

    todas_ok = ok_H1 and ok_H2 and h1_mas_plausible
    letra_resultado = "d" if todas_ok else "?"
    veredicto_final(letra_resultado, RESPUESTA_SEGUN_TXT, todas_ok)

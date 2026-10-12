"""
Concepto: MODELO MINIMO DE HERBRAND
Cita: M. H. van Emden, R. A. Kowalski, "The Semantics of Predicate
Logic as a Programming Language", Journal of the ACM, Vol. 23, No. 4,
1976, pp. 733-742.

Demuestra: el calculo del punto fijo del operador de consecuencia
inmediata T_P, que produce el modelo minimo de Herbrand del programa
logico "abuelo".
"""

hechos = {("padre", "juan", "maria"), ("padre", "maria", "ana")}


def regla_abuelo(interpretacion):
    # abuelo(X,Z) :- padre(X,Y), padre(Y,Z).
    return {
        ("abuelo", x, z)
        for (r1, x, y) in interpretacion if r1 == "padre"
        for (r2, y2, z) in interpretacion if r2 == "padre" and y2 == y
    }


def operador_Tp(interpretacion, hechos):
    return set(interpretacion) | set(hechos) | regla_abuelo(interpretacion)


def modelo_minimo_herbrand(hechos):
    interpretacion = set()
    iteracion = 0
    while True:
        iteracion += 1
        siguiente = operador_Tp(interpretacion, hechos)
        print(f"Iteracion {iteracion}: {sorted(siguiente)}")
        if siguiente == interpretacion:  # punto fijo alcanzado
            return interpretacion
        interpretacion = siguiente


if __name__ == "__main__":
    modelo = modelo_minimo_herbrand(hechos)
    print("\nModelo minimo de Herbrand final:")
    for atomo in sorted(modelo):
        print(" ", atomo)

    print("\nConclusion: el conjunto obtenido es el minimo punto fijo de "
          "T_P (lfp(T_P)) y, segun van Emden y Kowalski (1976), coincide "
          "exactamente con el modelo minimo de Herbrand del programa: "
          "contiene solo los atomos ground estrictamente deducibles.")

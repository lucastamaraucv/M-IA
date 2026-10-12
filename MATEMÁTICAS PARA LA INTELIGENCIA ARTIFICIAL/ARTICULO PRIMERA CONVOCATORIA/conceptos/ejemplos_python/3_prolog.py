"""
Concepto: PROLOG (programacion logica)
Cita: A. Colmerauer, P. Roussel, "The Birth of Prolog", HOPL-II, ACM,
1993, pp. 37-52 (manuscrito original: 19 de noviembre de 1992).
Complementar con: R. Kowalski, "Predicate Logic as Programming
Language", IFIP Congress, 1974, pp. 569-574.

Demuestra: el estilo declarativo de PROLOG (hechos + reglas + consulta
por unificacion), replicando el ejemplo clasico "abuelo(X,Z)".
"""

hechos = {
    ("padre", "juan", "maria"),
    ("padre", "maria", "ana"),
    ("padre", "pedro", "luis"),
}


def regla_abuelo(x, z, hechos):
    # Equivalente a la clausula PROLOG:
    #   abuelo(X,Z) :- padre(X,Y), padre(Y,Z).
    for (rel, a, b) in hechos:
        if rel == "padre" and a == x:
            y = b
            if ("padre", y, z) in hechos:
                return True, y  # y = el "eslabon" intermedio encontrado
    return False, None


def consulta_abuelo(x, z):
    return regla_abuelo(x, z, hechos)


if __name__ == "__main__":
    consultas = [("juan", "ana"), ("pedro", "ana"), ("maria", "ana")]

    for x, z in consultas:
        es_verdad, intermedio = consulta_abuelo(x, z)
        if es_verdad:
            print(f"?- abuelo({x}, {z}).  ->  true "
                  f"(via padre({x},{intermedio}), padre({intermedio},{z}))")
        else:
            print(f"?- abuelo({x}, {z}).  ->  false")

    print("\nConclusion: nunca se declaro 'abuelo(juan,ana)' como hecho; "
          "se DEDUJO automaticamente a partir de la regla y los hechos, "
          "igual que hace el motor de resolucion SLD de PROLOG.")

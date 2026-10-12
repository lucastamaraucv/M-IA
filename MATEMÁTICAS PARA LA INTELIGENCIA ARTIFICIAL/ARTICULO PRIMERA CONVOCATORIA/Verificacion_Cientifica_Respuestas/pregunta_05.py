"""
PREGUNTA 5 - diferencia entre "Explicar" y "Justificar" una hipotesis en ILP.

PROBLEMA COMPUTACIONAL: se implementan DOS FUNCIONES DISTINTAS sobre la
MISMA hipotesis H1 y se observa que tipo de resultado produce cada una:
  - explica(H, B, E+)   -> booleano (True/False), solo necesita H, B y los
                            ejemplos positivos (relacion de cobertura logica,
                            B ∧ H ⊨ E+).
  - justifica(H, ...)   -> un NUMERO entre 0 y 1 (probabilidad posterior de
                            Bayes) que ademas depende de que OTRAS hipotesis
                            compiten con H.
Si ambas dieran siempre lo mismo (fueran "equivalentes", opcion b), el
resultado de justifica no deberia depender de nada mas que de H; el
experimento comprueba si eso es cierto o no.
"""
from motor_ilp import HECHOS_FAMILIA, sufficiency, bayes_posterior
from utilidades_pdf import imprimir_encabezado, imprimir_alternativas, veredicto_final

NUMERO = 5
ENUNCIADO = ('Dada una hipotesis en ILP, ¿que alternativa describe la diferencia entre '
             'los terminos "Explicar" y "Justificar"?')
ALTERNATIVAS = {
    "a": "Explicar una hipotesis significa demostrarla deductivamente, mientras que justificarla consiste en invalidarla si contradice los datos.",
    "b": "Explicar y justificar una hipotesis son procesos equivalentes que consisten en comprobar su validez logica absoluta.",
    "c": "Explicar una hipotesis implica usar probabilidades, mientras que justificarla consiste en derivar ejemplos negativos.",
    "d": "Una hipotesis junto con el conocimiento previo, permite explicar (cubrir) los ejemplos observados. Justificar una hipotesis consiste en evaluar su plausibilidad frente a otras hipotesis posibles.",
}
RESPUESTA_SEGUN_TXT = "d"


def H1_general(interpretacion):
    return {("abuelo", x, z)
            for (r1, x, y) in interpretacion if r1 == "padre"
            for (r2, y2, z) in interpretacion if r2 == "padre" and y2 == y}


def H2_sobreajustada(interpretacion):
    return {("abuelo", x, z)
            for (r1, x, y) in interpretacion if r1 == "padre" and y == "maria"
            for (r2, y2, z) in interpretacion if r2 == "padre" and y2 == "maria"}


def explica(H, B, E_pos):
    """B ∧ H ⊨ E+ (posterior sufficiency): booleano puro."""
    return sufficiency(H, B, E_pos)


def justifica(H_nombre, likelihoods, priors):
    """Requiere comparar H contra sus COMPETIDORAS via Bayes: el resultado
    es un numero que cambia si cambia el conjunto de hipotesis rivales."""
    posterior = bayes_posterior(priors, likelihoods)
    return posterior[H_nombre]


if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    E_pos = [("abuelo", "juan", "ana")]

    explica_H1 = explica(H1_general, HECHOS_FAMILIA, E_pos)
    print(f"explica(H1, B, E+) = {explica_H1}   (tipo: {type(explica_H1).__name__}; "
          f"solo depende de H1, B y E+)")

    likelihoods = {"H1": 1.0, "H2": 1.0}
    prior_A = {"H1": 0.5, "H2": 0.5}          # escenario A: sin preferencia
    prior_B = {"H1": 0.9, "H2": 0.1}          # escenario B: se prefiere H1 (mas general)

    justifica_H1_escenario_A = justifica("H1", likelihoods, prior_A)
    justifica_H1_escenario_B = justifica("H1", likelihoods, prior_B)

    print(f"justifica(H1) con prior A (sin preferencia)   = {justifica_H1_escenario_A:.4f}")
    print(f"justifica(H1) con prior B (se prefiere H1)    = {justifica_H1_escenario_B:.4f}")
    print()

    cambia_con_competidoras = justifica_H1_escenario_A != justifica_H1_escenario_B

    print("ANALISIS:")
    print(" - 'explica(H1,...)' es un booleano fijo: no cambia aunque agreguemos o")
    print("   quitemos hipotesis rivales -> es una relacion de COBERTURA LOGICA")
    print("   (B ∧ H ⊨ E+), coincide con la primera mitad de (d).")
    print(" - 'justifica(H1,...)' SI cambia (de "
          f"{justifica_H1_escenario_A:.2f} a {justifica_H1_escenario_B:.2f}) segun que")
    print("   otras hipotesis compitan y con que probabilidad previa: es una")
    print("   evaluacion RELATIVA/comparativa de plausibilidad, no un booleano fijo.")
    print(" - Si (b) fuera cierto ('procesos equivalentes'), justifica() deberia ser")
    print("   tambien un booleano fijo independiente de las competidoras -> el")
    print("   experimento lo refuta directamente.")
    print(" - (a) y (c) invierten los roles (asignan la parte probabilistica a")
    print("   'explicar' en vez de a 'justificar', o inventan 'derivar ejemplos")
    print("   negativos' como definicion de justificar, algo que el experimento no")
    print("   respalda en ningun momento.")
    print(" - Confirma computacionalmente la opcion (d).")
    print()

    todas_ok = (explica_H1 is True) and cambia_con_competidoras
    letra_resultado = "d" if todas_ok else "?"
    veredicto_final(letra_resultado, RESPUESTA_SEGUN_TXT, todas_ok)

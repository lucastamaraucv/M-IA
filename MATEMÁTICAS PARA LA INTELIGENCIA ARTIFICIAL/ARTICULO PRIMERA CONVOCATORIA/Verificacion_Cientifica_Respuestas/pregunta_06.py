"""
PREGUNTA 6 - "El articulo (BILP) redefine la ILP usando:"

PROBLEMA COMPUTACIONAL: se implementa LITERALMENTE la formula que el
articulo de Muggleton (BILP, COLT'94, Seccion 2) da para el posterior:
    p(Hn|E) = p(E|Hn)*p(Hn) / p(E),   con p(E|Hn) = 1 si holds(Hn,E), 0 si no.
Se muestra que, ante EVIDENCIA NUEVA, la probabilidad PREVIA (prior) sola NO
basta para decidir cual hipotesis es mejor: hace falta el TEOREMA DE BAYES
para actualizarla con la evidencia y obtener el POSTERIOR, que es lo que de
verdad cambia el ranking de hipotesis.
"""
from motor_ilp import bayes_posterior
from utilidades_pdf import imprimir_encabezado, imprimir_alternativas, veredicto_final

NUMERO = 6
ENUNCIADO = "En relacion al articulo Bayesian Logic Programming (BILP): el articulo redefine la ILP usando:"
ALTERNATIVAS = {
    "a": "probabilidades incondicionales.",
    "b": "el teorema de Bayes, que permite calcular la probabilidad posterior de una hipotesis.",
    "c": "como punto de partida, ejemplos positivos y negativos.",
    "d": "Una probabilidad previa a cada hipotesis.",
}
RESPUESTA_SEGUN_TXT = "b"

if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    prior = {"H_A": 0.3, "H_B": 0.7}
    print(f"Probabilidad PREVIA (prior), antes de ver evidencia: {prior}")
    ganadora_solo_prior = max(prior, key=prior.get)
    print(f"  -> Si solo mirasemos el prior (incondicional, opciones a/d), "
          f"ganaria: {ganadora_solo_prior}\n")

    print("Llega evidencia NUEVA E: solo H_A la explica (holds(H_A,E)=True,")
    print("holds(H_B,E)=False).")
    likelihood = {"H_A": 1.0, "H_B": 0.0}
    print(f"  p(E|H) = {likelihood}\n")

    posterior = bayes_posterior(prior, likelihood)
    print(f"POSTERIOR via TEOREMA DE BAYES  p(H|E) = p(E|H)*p(H) / p(E): {posterior}")
    ganadora_posterior = max(posterior, key=posterior.get)
    print(f"  -> Considerando la evidencia (Bayes), ahora gana: {ganadora_posterior}\n")

    el_ranking_cambio = ganadora_solo_prior != ganadora_posterior

    print("ANALISIS:")
    print(" - Con SOLO el prior (probabilidad incondicional, sin condicionar a la")
    print("   evidencia), la hipotesis preferida seria H_B (prior mas alto) -> esto es")
    print("   lo que dirian (a) y (d) si bastaran por si solos.")
    print(" - Al llegar evidencia que SOLO H_A explica, el TEOREMA DE BAYES actualiza")
    print("   las probabilidades y CAMBIA el ganador a H_A. El mecanismo que produce")
    print("   este cambio -condicionar el prior con la evidencia- es exactamente el")
    print("   teorema de Bayes para calcular la probabilidad POSTERIOR.")
    print(" - (c) describe el punto de partida de la ILP CLASICA (ejemplos +/-), no lo")
    print("   que este articulo AGREGA (el calculo Bayesiano del posterior).")
    print(" - El experimento demuestra que ni el prior solo (a, d) ni los ejemplos")
    print("   solos (c) bastan para explicar el cambio observado: hace falta el")
    print("   teorema de Bayes -> confirma (b).")
    print()

    todas_ok = el_ranking_cambio and ganadora_posterior == "H_A"
    letra_resultado = "b" if todas_ok else "?"
    veredicto_final(letra_resultado, RESPUESTA_SEGUN_TXT, todas_ok)

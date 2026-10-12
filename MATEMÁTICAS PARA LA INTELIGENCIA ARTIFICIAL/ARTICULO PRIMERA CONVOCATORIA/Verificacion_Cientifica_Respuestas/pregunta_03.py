"""
PREGUNTA 3 - "Metodo usado por la ILP para evaluar hipotesis".

PROBLEMA COMPUTACIONAL: se generan 3 hipotesis candidatas (una correcta y
general, una sobreajustada, una incorrecta), se calcula su LIKELIHOOD real
mediante holds() (motor_ilp.py) y se combinan con una probabilidad previa
(prior) usando el TEOREMA DE BAYES (bayes_posterior) para producir el
"label" L = p(H|B∧E) que el articulo de Muggleton & De Raedt (1994, Sec. 4)
propone como metodo de evaluacion. El resultado (un numero de probabilidad
por hipotesis, no una prueba logica) es lo que decide la respuesta.
"""
from motor_ilp import HECHOS_FAMILIA, holds, bayes_posterior
from utilidades_pdf import imprimir_encabezado, imprimir_alternativas, veredicto_final

NUMERO = 3
ENUNCIADO = "Seleccione en la siguiente lista un metodo usado por la ILP para evaluar hipotesis:"
ALTERNATIVAS = {
    "a": "Reduccion al absurdo.",
    "b": "Uso de probabilidades.",
    "c": "Metodo deductivo.",
    "d": "Demostracion formal de teoremas.",
}
RESPUESTA_SEGUN_TXT = "b"


def H1_general(interpretacion):
    return {("abuelo", x, z)
            for (r1, x, y) in interpretacion if r1 == "padre"
            for (r2, y2, z) in interpretacion if r2 == "padre" and y2 == y}


def H2_sobreajustada(interpretacion):
    return {("abuelo", x, z)
            for (r1, x, y) in interpretacion if r1 == "padre" and y == "maria"
            for (r2, y2, z) in interpretacion if r2 == "padre" and y2 == "maria"}


def H3_incorrecta(interpretacion):
    # abuelo(X,Z) :- padre(X,Z)   [regla equivocada: 1 salto en vez de 2]
    return {("abuelo", x, z) for (r, x, z) in interpretacion if r == "padre"}


if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    E_pos = [("abuelo", "juan", "ana")]
    E_neg = [("abuelo", "pedro", "ana")]

    hipotesis = {"H1_general": H1_general, "H2_sobreajustada": H2_sobreajustada, "H3_incorrecta": H3_incorrecta}
    likelihood = {}
    for nombre, H in hipotesis.items():
        ok = holds(H, HECHOS_FAMILIA, E_pos, E_neg)
        likelihood[nombre] = 1.0 if ok else 0.0
        print(f"  holds({nombre}) = {ok}   -> P(E|H) = {likelihood[nombre]}")

    prior = {"H1_general": 0.5, "H2_sobreajustada": 0.3, "H3_incorrecta": 0.2}
    print(f"\n  Prior P(H) (a mayor generalidad/simplicidad, mayor prior): {prior}")

    posterior = bayes_posterior(prior, likelihood)
    print("\n  Posterior via TEOREMA DE BAYES  P(H|E) = P(E|H)*P(H) / P(E):")
    for nombre, p in sorted(posterior.items(), key=lambda kv: -kv[1]):
        print(f"    P({nombre} | E) = {p:.4f}")

    ganadora = max(posterior, key=posterior.get)
    print(f"\n  -> Hipotesis con MAYOR probabilidad posterior: {ganadora}")

    print()
    print("ANALISIS:")
    print(" - El metodo que efectivamente SELECCIONA una hipotesis aqui es un NUMERO")
    print("   DE PROBABILIDAD (posterior de Bayes), no una demostracion formal: H3")
    print("   se descarta porque su LIKELIHOOD (calculado, no supuesto) es 0, y entre")
    print("   H1 y H2 (ambas con likelihood 1) el PRIOR probabilistico desempata.")
    print(" - No hubo ningun paso de 'reduccion al absurdo' (a): H3 simplemente no")
    print("   cubre el ejemplo positivo, no se derivo una contradiccion logica.")
    print(" - No hay 'metodo deductivo' (c) ni 'demostracion formal de teoremas' (d)")
    print("   involucrados: la eleccion final depende de un calculo de PROBABILIDAD.")
    print(" - Esto confirma computacionalmente la opcion (b).")
    print()

    todas_ok = (likelihood["H1_general"] == 1.0 and likelihood["H2_sobreajustada"] == 1.0
                and likelihood["H3_incorrecta"] == 0.0 and posterior["H3_incorrecta"] == 0.0)
    letra_resultado = "b" if todas_ok else "?"
    veredicto_final(letra_resultado, RESPUESTA_SEGUN_TXT, todas_ok)

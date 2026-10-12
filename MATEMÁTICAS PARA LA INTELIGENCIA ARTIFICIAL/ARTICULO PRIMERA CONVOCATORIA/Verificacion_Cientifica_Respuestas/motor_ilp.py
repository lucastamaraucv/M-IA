"""
Motor de juguete compartido por las preguntas 1-9 (ILP y BILP).

No es una cita ni un resumen: es un MOTOR LOGICO EJECUTABLE (estilo Datalog/
Prolog, igual que conceptos/ejemplos_python/3_prolog.py y 5_herbrand.py) que
implementa de verdad las definiciones formales del articulo "Inductive Logic
Programming: Theory and Methods" (Muggleton & De Raedt, 1994) y de "Bayesian
Inductive Logic Programming" (Muggleton, 1994):

  - forward_chaining(B, regla):  calcula el punto fijo de T_P (igual que
    5_herbrand.py), es decir, TODO lo que B + una regla candidata implican.
  - cubre(regla, B, atomo):      ¿el atomo se deriva de B+regla? (relacion de
    consecuencia logica |=, calculada de verdad, no simulada).
  - sufficiency / satisfiability / holds: exactamente las 2 condiciones
    formales citadas en BILP (p.634-635 y Seccion 2).
  - bayes_posterior:             P(H|E) = P(E|H)*P(H) / P(E), con
    P(E|H) = 1 si holds(H,E), 0 en otro caso (formula literal del articulo
    BILP).

Cada pregunta_XX.py importa estas piezas y las usa para construir un
ESCENARIO CONCRETO (hechos, ejemplos, hipotesis candidatas) y deja que el
computo -no una opinion- decida cual alternativa del examen es consistente
con lo que el codigo observa al ejecutarse.
"""

# ---------------------------------------------------------------------
# Conocimiento previo (background knowledge B): arbol genealogico de juguete
# ---------------------------------------------------------------------
HECHOS_FAMILIA = {
    ("padre", "juan", "maria"),
    ("padre", "maria", "ana"),
    ("padre", "ana", "sofia"),
    ("padre", "pedro", "luis"),
    ("padre", "luis", "carla"),
}


def forward_chaining(hechos_base, reglas, max_iter=50):
    """Punto fijo del operador de consecuencia inmediata T_P (igual idea que
    5_herbrand.py), pero generalizado a una LISTA de reglas (funciones que
    reciben la interpretacion actual y devuelven nuevos atomos derivables)."""
    interpretacion = set(hechos_base)
    for _ in range(max_iter):
        nuevos = set(interpretacion)
        for regla in reglas:
            nuevos |= regla(interpretacion)
        if nuevos == interpretacion:
            return interpretacion
        interpretacion = nuevos
    raise RuntimeError("No convergio (revisar reglas: ¿hay recursion infinita?)")


def regla_abuelo(interpretacion):
    return {
        ("abuelo", x, z)
        for (r1, x, y) in interpretacion if r1 == "padre"
        for (r2, y2, z) in interpretacion if r2 == "padre" and y2 == y
    }


def regla_antepasado(interpretacion):
    """antepasado(X,Z) :- padre(X,Z).  antepasado(X,Z) :- padre(X,Y), antepasado(Y,Z).
    A diferencia de 'abuelo' (2 niveles fijos), esta regla es RECURSIVA: se
    aplica sobre su propio resultado, por lo que puede alcanzar cualquier
    profundidad (necesita un numero de iteraciones no acotado de antemano),
    igual que una funcion recursiva general en una maquina de Turing."""
    directos = {("antepasado", x, y) for (r, x, y) in interpretacion if r == "padre"}
    transitivos = {
        ("antepasado", x, z)
        for (r1, x, y) in interpretacion if r1 == "padre"
        for (r2, y2, z) in interpretacion if r2 == "antepasado" and y2 == y
    }
    return directos | transitivos


def cubre(regla, hechos_base, atomo):
    """¿'atomo' se deriva logicamente de hechos_base + regla? (|= real)."""
    modelo = forward_chaining(hechos_base, [regla])
    return atomo in modelo


def sufficiency(regla, hechos_base, ejemplos_positivos):
    """H ⊨ E+ : la hipotesis (+ background) debe derivar TODOS los positivos."""
    modelo = forward_chaining(hechos_base, [regla])
    return all(e in modelo for e in ejemplos_positivos)


def satisfiability(regla, hechos_base, ejemplos_negativos):
    """H ∧ E- ⊭ ⊥ : la hipotesis NO debe derivar NINGUN ejemplo negativo."""
    modelo = forward_chaining(hechos_base, [regla])
    return not any(e in modelo for e in ejemplos_negativos)


def holds(regla, hechos_base, ejemplos_positivos, ejemplos_negativos):
    return sufficiency(regla, hechos_base, ejemplos_positivos) and \
           satisfiability(regla, hechos_base, ejemplos_negativos)


def bayes_posterior(prior, likelihood_por_hipotesis):
    """P(H|E) = P(E|H) P(H) / sum_H' P(E|H') P(H')  (Bayes, formula literal
    citada en Bayesian Inductive Logic Programming, Seccion 2)."""
    evidencia = sum(likelihood_por_hipotesis[h] * prior[h] for h in prior)
    if evidencia == 0:
        return {h: 0.0 for h in prior}
    return {h: (likelihood_por_hipotesis[h] * prior[h]) / evidencia for h in prior}

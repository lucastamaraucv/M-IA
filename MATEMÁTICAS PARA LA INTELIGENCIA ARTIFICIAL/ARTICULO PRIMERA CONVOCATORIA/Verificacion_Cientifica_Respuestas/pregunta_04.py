"""
PREGUNTA 4 - papel del conocimiento previo (background knowledge) en ILP.

PROBLEMA COMPUTACIONAL: se implementa un pequeno buscador de hipotesis
"bottom-up" (al estilo DUCE/CIGOL citado en el articulo) que GENERA reglas
candidatas usando los PREDICADOS DISPONIBLES en el background knowledge B.
Se corre un experimento de ABLACION: la misma busqueda, una vez CON B
(los hechos de la familia) y una vez SIN B (B vacio), para observar
directamente si el conocimiento previo solo "valida al final" o si de verdad
GUIA/CONSTRUYE la hipotesis durante la busqueda.
"""
from motor_ilp import holds
from utilidades_pdf import imprimir_encabezado, imprimir_alternativas, veredicto_final

NUMERO = 4
ENUNCIADO = "¿Cual es el papel del conocimiento previo (background knowledge) en ILP?"
ALTERNATIVAS = {
    "a": "No interviene en el aprendizaje, ya que la ILP solo utiliza ejemplos.",
    "b": "Sirve unicamente para validar la hipotesis final mediante demostraciones deductivas.",
    "c": "Permite construir y guiar la generacion de hipotesis, facilitando la explicacion de los ejemplos.",
    "d": "Se utiliza unicamente para generar ejemplos negativos.",
}
RESPUESTA_SEGUN_TXT = "c"

HECHOS_FAMILIA = {
    ("padre", "juan", "maria"), ("padre", "maria", "ana"),
    ("padre", "ana", "sofia"), ("padre", "pedro", "luis"),
}


def predicados_disponibles(background):
    """Lo que el generador de hipotesis PUEDE usar depende directamente de
    que predicados existan en B. Sin B, esta lista queda vacia."""
    return sorted({r for (r, *_ ) in background})


def generar_candidatas(background):
    """Generador bottom-up MUY simplificado: por cada predicado binario
    presente en B, propone la regla de composicion de 2 saltos
    'objetivo(X,Z) :- pred(X,Y), pred(Y,Z)'. Si B no tiene predicados,
    no hay NADA que proponer (lista vacia)."""
    candidatas = []
    for pred in predicados_disponibles(background):
        def hacer_regla(pred=pred):
            def regla(interpretacion):
                return {("abuelo", x, z)
                        for (r1, x, y) in interpretacion if r1 == pred
                        for (r2, y2, z) in interpretacion if r2 == pred and y2 == y}
            return regla
        candidatas.append((f"abuelo(X,Z) :- {pred}(X,Y), {pred}(Y,Z)", hacer_regla()))
    return candidatas


def buscar_hipotesis(background, E_pos, E_neg):
    for descripcion, regla in generar_candidatas(background):
        if holds(regla, background, E_pos, E_neg):
            return descripcion
    return None


if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    E_pos = [("abuelo", "juan", "ana")]
    E_neg = [("abuelo", "pedro", "ana")]

    print("EXPERIMENTO DE ABLACION: misma busqueda de hipotesis, con y sin B.\n")

    print("CASO A - CON background knowledge B (hechos de la familia):")
    print(f"  Predicados disponibles en B: {predicados_disponibles(HECHOS_FAMILIA)}")
    candidatas_con_B = generar_candidatas(HECHOS_FAMILIA)
    print(f"  Candidatas generadas a partir de B: {[c[0] for c in candidatas_con_B]}")
    hipotesis_con_B = buscar_hipotesis(HECHOS_FAMILIA, E_pos, E_neg)
    print(f"  -> Hipotesis encontrada que explica E+/E-: {hipotesis_con_B}\n")

    print("CASO B - SIN background knowledge (B = conjunto vacio):")
    B_vacio = set()
    print(f"  Predicados disponibles en B: {predicados_disponibles(B_vacio)}")
    candidatas_sin_B = generar_candidatas(B_vacio)
    print(f"  Candidatas generadas a partir de B: {[c[0] for c in candidatas_sin_B]}")
    hipotesis_sin_B = buscar_hipotesis(B_vacio, E_pos, E_neg)
    print(f"  -> Hipotesis encontrada que explica E+/E-: {hipotesis_sin_B}\n")

    print("ANALISIS:")
    print(" - CON B: el generador usa los predicados de B ('padre') para PROPONER")
    print("   candidatas, y encuentra una hipotesis que explica los ejemplos.")
    print(" - SIN B: el generador no tiene ningun predicado del que partir -> NO PUEDE")
    print("   ni siquiera PROPONER una hipotesis candidata (lista vacia), sin importar")
    print("   cuantos ejemplos E+/E- se le den. El fallo ocurre en la GENERACION, no")
    print("   en una validacion final.")
    print(" - Esto refuta (a) ('no interviene'): sin B la busqueda colapsa por completo.")
    print(" - Refuta (b) ('solo valida al final'): aqui B interviene ANTES, generando")
    print("   las candidatas mismas, no solo comprobandolas al final.")
    print(" - Refuta (d): B se uso para generar la HIPOTESIS, no ejemplos negativos.")
    print(" - Confirma (c): B permite CONSTRUIR y GUIAR la generacion de hipotesis.")
    print()

    todas_ok = (hipotesis_con_B is not None) and (hipotesis_sin_B is None) and \
               (len(candidatas_sin_B) == 0) and (len(candidatas_con_B) > 0)
    letra_resultado = "c" if todas_ok else "?"
    veredicto_final(letra_resultado, RESPUESTA_SEGUN_TXT, todas_ok)

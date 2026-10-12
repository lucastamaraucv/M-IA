"""
PREGUNTA 8 - "U-learnability fue disenado para poder tratar representaciones:"

PROBLEMA COMPUTACIONAL: se compara una regla de longitud FIJA (acotada, tipo
PAC: "abuelo" solo alcanza 2 generaciones) contra una regla RECURSIVA
("antepasado", motor_ilp.regla_antepasado) que se auto-aplica hasta alcanzar
un punto fijo, sin limite de profundidad prefijado -exactamente como una
funcion recursiva general/Turing-computable-. Se genera una cadena
familiar cada vez mas larga y se mide en que generacion cada representacion
deja de funcionar.
"""
from motor_ilp import forward_chaining, regla_antepasado
from utilidades_pdf import imprimir_encabezado, imprimir_alternativas, imprimir_evidencia, veredicto_final, buscar_cita

NUMERO = 8
ENUNCIADO = "Segun el articulo BILP, U-learnability fue disenado para poder tratar representaciones:"
ALTERNATIVAS = {
    "a": "Turing-computables.",
    "b": "Turing-completas.",
    "c": "Turing-computables y Turing-completas.",
    "d": "Simplificadas de PAC-learning.",
}
RESPUESTA_SEGUN_TXT = "a"
ARCHIVO = "Bayesian Inductive Logic Programming.pdf"


def regla_de_longitud_fija(interpretacion):
    """Version ACOTADA (estilo PAC: longitud de clausula L=2 fija):
    solo alcanza 2 generaciones, sin importar cuan larga sea la cadena."""
    return {("antepasado_L2", x, z)
            for (r1, x, y) in interpretacion if r1 == "padre"
            for (r2, y2, z) in interpretacion if r2 == "padre" and y2 == y}


def generar_cadena(n_generaciones):
    return {("padre", f"persona_{i}", f"persona_{i+1}") for i in range(n_generaciones)}


if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    ev = buscar_cita(ARCHIVO, "It is argued that U-learnability is more appropriate than PAC for Universal")
    imprimir_evidencia(ev, 1)

    print(f"{'Generaciones':>13} | {'Fija(L=2) alcanza el mas antiguo?':>35} | "
          f"{'Recursiva alcanza el mas antiguo?':>35}")
    print("-" * 90)

    resultados = []
    for n in [2, 4, 8, 16, 32]:
        cadena = generar_cadena(n)
        objetivo = ("persona_0", f"persona_{n}")

        modelo_fija = forward_chaining(cadena, [regla_de_longitud_fija])
        alcanza_fija = ("antepasado_L2",) + objetivo in modelo_fija

        modelo_recursiva = forward_chaining(cadena, [regla_antepasado])
        alcanza_recursiva = ("antepasado",) + objetivo in modelo_recursiva

        resultados.append((n, alcanza_fija, alcanza_recursiva))
        print(f"{n:>13} | {str(alcanza_fija):>35} | {str(alcanza_recursiva):>35}")

    print()
    fija_falla_en_algun_punto = any(not fija for (n, fija, rec) in resultados if n > 2)
    recursiva_siempre_funciona = all(rec for _, _, rec in resultados)

    print("ANALISIS:")
    print(" - La regla de longitud FIJA (L=2, estilo hipotesis PAC de tamano acotado)")
    print("   SOLO funciona para exactamente 2 generaciones; para cadenas mas largas")
    print("   (4, 8, 16, 32 generaciones) deja de alcanzar al ancestro mas antiguo, sin")
    print("   importar cuantos ejemplos se le den: su REPRESENTACION esta limitada de")
    print("   antemano.")
    print(" - La regla RECURSIVA ('antepasado', que se auto-aplica hasta el punto fijo)")
    print("   alcanza al ancestro mas antiguo en TODOS los casos, sin limite de")
    print("   profundidad prefijado -exactamente el tipo de computo NO acotado que")
    print("   puede realizar una maquina de Turing (recursion general)-.")
    print(" - Esto ilustra por que U-learnability se disena para representaciones")
    print("   TURING-COMPUTABLES (que permiten esta clase de recursion no acotada),")
    print("   mientras que representaciones de longitud fija (como asume PAC) quedan")
    print("   limitadas por construccion -> confirma (a), refuta (b)/(c) (Turing-")
    print("   completo es una propiedad de LENGUAJES/maquinas, no de la clase de")
    print("   representacion que aqui se aprende) y (d).")
    print()

    todas_ok = ev["encontrada"] and fija_falla_en_algun_punto and recursiva_siempre_funciona
    letra_resultado = "a" if todas_ok else "?"
    veredicto_final(letra_resultado, RESPUESTA_SEGUN_TXT, todas_ok)

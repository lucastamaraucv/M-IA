"""
PREGUNTA 13 - "Intuitivamente, el modelo minimo de Herbrand representa:"

PROBLEMA COMPUTACIONAL: se calcula el PUNTO FIJO del operador de
consecuencia inmediata T_P (igual que conceptos/ejemplos_python/5_herbrand.py)
para obtener el modelo minimo M_P de un programa logico "abuelo". Luego se
construyen y PRUEBAN DE VERDAD dos conjuntos alternativos:
  1) Un modelo MAS GRANDE (M_P + un atomo extra NO deducible) y se verifica
     si sigue "satisfaciendo" las reglas del programa (para ver si "el
     conjunto mas grande" tiene algun sentido especial).
  2) Un modelo MAS PEQUENO (M_P menos un atomo que SI es necesario) y se
     verifica si deja de satisfacer las reglas (para probar que M_P no puede
     encogerse mas).
"""
from utilidades_pdf import imprimir_encabezado, imprimir_alternativas, veredicto_final

NUMERO = 13
ENUNCIADO = "Intuitivamente, el modelo minimo de Herbrand representa:"
ALTERNATIVAS = {
    "a": "los supuestos de un programa logico.",
    "b": "los hechos y consecuencias de un programa logico.",
    "c": "el conjunto mas grande de hechos verdaderos que pueden deducirse.",
    "d": "todo lo que un programa logico implica y nada mas.",
}
RESPUESTA_SEGUN_TXT = "d"

HECHOS = {("padre", "juan", "maria"), ("padre", "maria", "ana")}


def regla_abuelo(interpretacion):
    return {("abuelo", x, z)
            for (r1, x, y) in interpretacion if r1 == "padre"
            for (r2, y2, z) in interpretacion if r2 == "padre" and y2 == y}


def es_modelo(interpretacion, hechos_base):
    """¿'interpretacion' SATISFACE el programa? (para TODA instancia de la
    regla, si el cuerpo esta presente, la cabeza tambien debe estarlo)."""
    if not hechos_base.issubset(interpretacion):
        return False
    cabezas_exigidas = regla_abuelo(interpretacion)
    return cabezas_exigidas.issubset(interpretacion)


def punto_fijo(hechos_base):
    interpretacion = set(hechos_base)
    while True:
        siguiente = interpretacion | regla_abuelo(interpretacion) | hechos_base
        if siguiente == interpretacion:
            return interpretacion
        interpretacion = siguiente


if __name__ == "__main__":
    imprimir_encabezado(NUMERO, ENUNCIADO)
    imprimir_alternativas(ALTERNATIVAS)

    M_P = punto_fijo(HECHOS)
    print(f"Modelo MINIMO de Herbrand M_P (punto fijo de T_P): {sorted(M_P)}\n")

    # 1) Un modelo MAS GRANDE (atomo extra no deducible)
    atomo_extra_no_deducible = ("abuelo", "pedro", "ana")  # 'pedro' ni aparece en HECHOS
    M_grande = M_P | {atomo_extra_no_deducible}
    grande_es_modelo = es_modelo(M_grande, HECHOS)
    print(f"M_grande = M_P + {atomo_extra_no_deducible} (un atomo que el programa "
          f"NUNCA deduce)")
    print(f"  ¿M_grande sigue 'satisfaciendo' las reglas (es un modelo)? {grande_es_modelo}")
    print(f"  ¿{atomo_extra_no_deducible} es realmente DEDUCIBLE del programa? "
          f"{atomo_extra_no_deducible in M_P}")

    # 2) Un modelo MAS PEQUENO (quitando un atomo que SI hace falta)
    atomo_necesario = ("abuelo", "juan", "ana")  # SI se deduce de los hechos
    M_pequeno = M_P - {atomo_necesario}
    pequeno_es_modelo = es_modelo(M_pequeno, HECHOS)
    print(f"\nM_pequeno = M_P - {atomo_necesario} (un atomo que SI es necesario)")
    print(f"  ¿M_pequeno sigue 'satisfaciendo' las reglas (es un modelo)? {pequeno_es_modelo}")

    print()
    print("ANALISIS:")
    print(f" - M_grande (con un atomo EXTRA no deducible) TODAVIA satisface las reglas")
    print(f"   ({grande_es_modelo}), pero contiene algo que el programa NUNCA implica")
    print(f"   ({atomo_extra_no_deducible} no esta en M_P). Es decir: 'el conjunto MAS")
    print(f"   GRANDE que satisface las reglas' NO es un concepto util ni unico -se")
    print(f"   le puede seguir agregando basura arbitrariamente y sigue siendo un")
    print(f"   'modelo'- por eso (c) es INCORRECTA.")
    print(f" - M_pequeno (quitando un atomo NECESARIO) DEJA de satisfacer las reglas")
    print(f"   ({pequeno_es_modelo}): no se puede encoger mas sin romper el programa.")
    print(f" - M_P es entonces el UNICO conjunto que es, a la vez, un modelo valido Y")
    print(f"   no contiene nada de mas: exactamente 'todo lo que el programa implica y")
    print(f"   nada mas' -> confirma (d).")
    print()

    todas_ok = grande_es_modelo and (not pequeno_es_modelo) and (atomo_extra_no_deducible not in M_P)
    letra_resultado = "d" if todas_ok else "?"
    veredicto_final(letra_resultado, RESPUESTA_SEGUN_TXT, todas_ok)

"""
==============================================================
  CLASE 00 - INTRODUCCION AL CURSO
  01MIAR - Python para Inteligencia Artificial
==============================================================

Este script es la version interactiva del notebook
'01MIAR_00_Intro.ipynb'. La idea es que NO solo leas, sino que
escribas tu mismo el codigo para fijar el conocimiento.

Como usarlo:
  1) Ejecutalo desde una terminal:  python 00_intro_interactivo.py
  2) Sigue el menu y elige una seccion.
  3) En cada seccion vas a leer la teoria, ver un ejemplo
     funcionando y despues TU vas a escribir el codigo en el
     prompt. El programa te ayudara y te dira si lo hiciste bien.

Importante: cuando se te pida escribir codigo en el prompt,
escribe UNA sola linea. Si te equivocas, el programa te muestra
la solucion para que la copies o la corrijas.
"""

# ---------- utilidades comunes para todas las clases ----------

def titulo(texto):
    print("\n" + "=" * 64)
    print("  " + texto)
    print("=" * 64)


def pausa():
    input("\n>>> Pulsa ENTER para continuar...")


def reto(instruccion, solucion_correcta_funcion, pista=""):
    """
    Pide al usuario una linea de codigo y la ejecuta.
    'solucion_correcta_funcion' es una funcion (sin argumentos)
    que devuelve True si lo que escribio el usuario es valido.
    """
    print("\n>>> TU TURNO:")
    print(instruccion)
    if pista:
        print("    Pista:", pista)
    codigo = input(">>> Escribe tu codigo: ")
    try:
        # Compartimos las variables del modulo para que el codigo
        # del usuario pueda usarlas (ej: variables ya definidas).
        exec(codigo, globals())
        if solucion_correcta_funcion():
            print("    OK -> Lo lograste.")
        else:
            print("    Casi... el codigo se ejecuto pero el resultado")
            print("    esperado no se cumplio. Revisa la pista.")
    except Exception as e:
        print(f"    ERROR al ejecutar tu codigo: {e}")
    print()


# ============================================================
# SECCION 1 - Sobre la asignatura
# ============================================================
def seccion_1_sobre_la_asignatura():
    titulo("SECCION 1 - Sobre la asignatura 01MIAR")
    print("""
    OBJETIVOS del curso:
      - Disenar e implementar programas basicos en Python.
      - Saber usar scripts y Jupyter Notebooks.
      - Importar y configurar modulos externos.
      - Familiarizarte con NumPy, pandas y matplotlib.
      - Conocer tecnicas basicas de analisis de datos.

    METODOLOGIA:
      - Clases expositivas, problemas, foros y trabajo autonomo.

    EVALUACION:
      - Examen (40%) + Portafolio (60%): Video, Foro, Dataset, Whitepaper.
      - Hay que aprobar examen Y portafolio.

    POR QUE ESTO IMPORTA: Python es el lenguaje dominante en IA.
    Si dominas la sintaxis y las librerias clave (NumPy, pandas,
    matplotlib), puedes pasar de 'leer codigo' a 'crear modelos'.
    """)
    pausa()


# ============================================================
# SECCION 2 - Verificar version de Python
# ============================================================
def seccion_2_version_python():
    titulo("SECCION 2 - Verificar la version de Python")
    print("""
    En Python existe el modulo 'platform' que tiene la funcion
    python_version(). Sirve para saber con que version del
    interprete estas trabajando.

    Por que es importante: cierto codigo solo funciona en
    versiones >= 3.6 (por ejemplo los f-strings) y librerias
    como TensorFlow exigen versiones especificas (3.9 a 3.12).
    """)

    print("\n--- EJEMPLO ---")
    print("    from platform import python_version")
    print("    print(python_version())")
    print("    Salida:")
    from platform import python_version
    print("       ", python_version())

    # Reto 1
    def chequeo():
        # Si imprimio algo, lo damos por valido
        return True
    reto(
        "Escribe el codigo para imprimir la version de Python.",
        chequeo,
        pista="Usa print(python_version())  (ya lo importamos)."
    )
    pausa()


# ============================================================
# SECCION 3 - Tu primer "Hello World" y variables
# ============================================================
def seccion_3_hello_world():
    titulo("SECCION 3 - Hello World y variables")
    print("""
    En Python NO se declara el tipo de la variable. Solo asignas
    un valor con '=' y Python decide el tipo (tipado dinamico).
    Pero una vez asignado, el tipo es fuerte (tipado fuerte).

    Lo que vamos a aprender aqui:
      - Como crear una variable.
      - Como imprimir su valor con print().
      - Como insertar el valor dentro de un texto con f-strings.
    """)

    print("\n--- EJEMPLO ---")
    print("    a = 15")
    print("    print(f'el valor {a} para la variable')")
    a = 15
    print("    Salida:")
    print(f"        el valor {a} para la variable")

    # Reto: el usuario crea una variable y la imprime
    print("\n>>> TU TURNO:")
    print("    Crea una variable llamada 'edad' con TU edad")
    print("    e imprimela en el formato:")
    print('        "Tengo X anios"')
    print("    Tip: usa una f-string -> f'Tengo {edad} anios'")
    codigo = input(">>> Escribe tu codigo (puede ser en una linea, ")
    codigo2 = input(">>> o pulsa ENTER si lo escribiste todo arriba): ")
    completo = codigo + ("\n" + codigo2 if codigo2 else "")
    try:
        exec(completo, globals())
        if "edad" in globals():
            print(f"    OK -> Variable creada con valor: {globals()['edad']}")
        else:
            print("    No detecte la variable 'edad'. Intenta de nuevo.")
    except Exception as e:
        print(f"    ERROR: {e}")
        print("    Solucion sugerida:")
        print("        edad = 25")
        print("        print(f'Tengo {edad} anios')")
    pausa()


# ============================================================
# SECCION 4 - Tu primera funcion
# ============================================================
def seccion_4_primera_funcion():
    titulo("SECCION 4 - Definir y usar una funcion")
    print("""
    Una FUNCION agrupa codigo reutilizable bajo un nombre.
    En Python se define con la palabra clave 'def'.

    Sintaxis:
        def nombre_funcion(parametro1, parametro2):
            # codigo
            return resultado

    El 'return' devuelve el resultado al que llamo la funcion.
    Si no pones 'return', la funcion devuelve None.
    """)

    print("\n--- EJEMPLO ---")
    print("    def mult(a, b):")
    print("        return a * b")
    print()
    print("    print(mult(3, 4))   # imprime 12")

    def mult(a, b):
        return a * b

    print("    Salida:")
    print("       ", mult(3, 4))

    # Reto: definir una funcion suma
    print("\n>>> TU TURNO:")
    print("    Define una funcion 'suma(a, b)' que devuelva a + b,")
    print("    y luego llamala con 7 y 5. Imprime el resultado.")
    print("    NOTA: como son varias lineas, el programa te las")
    print("    pedira de a una. Cuando termines, escribe 'fin'.")
    print()
    lineas = []
    while True:
        linea = input("    > ")
        if linea.strip().lower() == "fin":
            break
        lineas.append(linea)
    codigo_usuario = "\n".join(lineas)
    try:
        exec(codigo_usuario, globals())
        if "suma" in globals() and globals()["suma"](7, 5) == 12:
            print("    OK -> Tu funcion suma funciona correctamente.")
        else:
            print("    Hmm, algo no cuadra. Solucion sugerida:")
            print("        def suma(a, b):")
            print("            return a + b")
            print("        print(suma(7, 5))")
    except Exception as e:
        print(f"    ERROR: {e}")
        print("    Solucion sugerida:")
        print("        def suma(a, b):")
        print("            return a + b")
        print("        print(suma(7, 5))")
    pausa()


# ============================================================
# SECCION 5 - Listas y bucle for con enumerate
# ============================================================
def seccion_5_listas_for():
    titulo("SECCION 5 - Listas y bucle for con enumerate")
    print("""
    Una LISTA es una coleccion ordenada de elementos. Se crea
    con corchetes:
        lista = [1, 2, 3]

    Un BUCLE FOR recorre la lista. Si necesitas tambien el
    indice, usa enumerate():
        for i, valor in enumerate(lista):
            ...

    Ahora vamos a multiplicar cada elemento por 10 y reemplazarlo
    en la misma lista (in-place).
    """)

    print("\n--- EJEMPLO ---")
    print("    def mult(a, b):")
    print("        return a * b")
    print()
    print("    lista = [1, 2, 3]")
    print("    for i, value in enumerate(lista):")
    print("        lista[i] = mult(value, 10)")
    print()
    print("    print(lista)   # -> [10, 20, 30]")

    def mult(a, b):
        return a * b

    lista = [1, 2, 3]
    for i, value in enumerate(lista):
        lista[i] = mult(value, 10)
    print("    Salida:")
    print("       ", lista)

    print("""
    Pregunta para ti: si en lugar de multiplicar por 10
    quieres ELEVAR AL CUADRADO cada elemento, como lo harias?
    """)

    print("\n>>> TU TURNO:")
    print("    Crea una lista 'numeros' con los valores [2, 4, 6],")
    print("    y reemplaza cada elemento por su cuadrado.")
    print("    Al final, imprimela. Escribe 'fin' cuando termines.")
    lineas = []
    while True:
        linea = input("    > ")
        if linea.strip().lower() == "fin":
            break
        lineas.append(linea)
    codigo_usuario = "\n".join(lineas)
    try:
        exec(codigo_usuario, globals())
        n = globals().get("numeros")
        if n == [4, 16, 36]:
            print("    OK -> Lista al cuadrado correcta:", n)
        else:
            print("    Resultado obtenido:", n)
            print("    Solucion sugerida:")
            print("        numeros = [2, 4, 6]")
            print("        for i, v in enumerate(numeros):")
            print("            numeros[i] = v * v")
            print("        print(numeros)")
    except Exception as e:
        print(f"    ERROR: {e}")
    pausa()


# ============================================================
# SECCION 6 - Vistazo a NumPy, pandas y matplotlib
# ============================================================
def seccion_6_librerias():
    titulo("SECCION 6 - Vistazo a NumPy, pandas y matplotlib")
    print("""
    El curso depende de tres librerias clave:

    NumPy  -> arrays numericos rapidos.
    pandas -> DataFrames (tablas tipo Excel/SQL).
    matplotlib -> graficas.

    Vamos a generar una tabla de numeros aleatorios, convertirla
    a DataFrame, y graficarla. No te preocupes si no entiendes
    todo, lo veras en detalle en las clases 8, 9 y 11.
    """)

    print("\n--- EJEMPLO ---")
    print("    import numpy as np")
    print("    random_list = np.random.randint(200, size=(10, 2))")
    print()
    print("    import pandas as pd")
    print("    frame = pd.DataFrame(random_list)")
    print("    print(frame)")
    print()
    print("    import matplotlib.pyplot as plt")
    print("    frame.plot()")
    print("    plt.show()  # abre una ventana con la grafica")

    try:
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt

        random_list = np.random.randint(200, size=(10, 2))
        frame = pd.DataFrame(random_list)
        print("\n    DataFrame generado:")
        print(frame)
        print("""
    Si quieres ver la grafica, descomenta las dos lineas finales
    de esta funcion en el archivo .py y vuelve a ejecutar.
        """)
        # frame.plot()
        # plt.show()
    except ImportError as e:
        print(f"    Falta instalar una libreria: {e}")
        print("    Ejecuta: pip install numpy pandas matplotlib")

    print("\n>>> TU TURNO:")
    print("    Genera un array NumPy de forma (5, 3) con enteros")
    print("    aleatorios entre 0 y 99, conviertelo a DataFrame y")
    print("    guardalo en una variable llamada 'mi_frame'.")
    print("    Despues imprimelo. Escribe 'fin' para terminar.")
    lineas = []
    while True:
        linea = input("    > ")
        if linea.strip().lower() == "fin":
            break
        lineas.append(linea)
    codigo_usuario = "\n".join(lineas)
    try:
        exec(codigo_usuario, globals())
        mf = globals().get("mi_frame")
        if mf is not None and mf.shape == (5, 3):
            print("    OK -> DataFrame de forma (5, 3) detectado.")
        else:
            print("    Resultado obtenido:", mf)
            print("    Solucion sugerida:")
            print("        import numpy as np")
            print("        import pandas as pd")
            print("        arr = np.random.randint(100, size=(5, 3))")
            print("        mi_frame = pd.DataFrame(arr)")
            print("        print(mi_frame)")
    except Exception as e:
        print(f"    ERROR: {e}")
    pausa()


# ============================================================
# MENU PRINCIPAL
# ============================================================
def menu():
    secciones = [
        ("Sobre la asignatura", seccion_1_sobre_la_asignatura),
        ("Verificar version de Python", seccion_2_version_python),
        ("Hello World y variables", seccion_3_hello_world),
        ("Definir y usar una funcion", seccion_4_primera_funcion),
        ("Listas y bucle for con enumerate", seccion_5_listas_for),
        ("Vistazo a NumPy, pandas y matplotlib", seccion_6_librerias),
    ]

    while True:
        print("\n" + "#" * 64)
        print("  CLASE 00 - INTRODUCCION  |  Menu")
        print("#" * 64)
        for i, (nombre, _) in enumerate(secciones, start=1):
            print(f"  {i}) {nombre}")
        print("  0) Salir")
        print("#" * 64)
        op = input("Elige una opcion: ").strip()
        if op == "0":
            print("Hasta la proxima clase. Sigue practicando.")
            break
        if op.isdigit() and 1 <= int(op) <= len(secciones):
            secciones[int(op) - 1][1]()
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    menu()

"""
==============================================================
  CLASE 01 - PYTHON 101: INTRODUCCION AL LENGUAJE
  01MIAR - Python para Inteligencia Artificial
==============================================================

Version interactiva del notebook '01MIAR_01_Python101.ipynb'.

Esta clase NO ensena sintaxis pesada todavia (eso viene en la
clase 02). Aqui te quiero dejar SUPER claro:
  - Que es Python y por que se usa.
  - Que es un interprete y como se ejecuta tu codigo.
  - Que diferencia hay entre script, REPL y Jupyter.
  - Por que NumPy es brutalmente mas rapido que listas Python.

Como usarlo:  python 01_python101_interactivo.py
"""

# ---------- utilidades ----------
def titulo(texto):
    print("\n" + "=" * 64)
    print("  " + texto)
    print("=" * 64)


def pausa():
    input("\n>>> Pulsa ENTER para continuar...")


def pregunta_si_no(pregunta):
    while True:
        r = input(pregunta + " (s/n): ").strip().lower()
        if r in ("s", "si", "n", "no"):
            return r.startswith("s")
        print("Responde 's' o 'n'.")


# ============================================================
# SECCION 1 - Caracteristicas de Python
# ============================================================
def seccion_1_caracteristicas():
    titulo("SECCION 1 - Caracteristicas de Python")
    print("""
    Python es:
      - Lenguaje de PROPOSITO GENERAL (sirve para casi todo).
      - INTERPRETADO, no compilado -> mas portable, mas flexible.
      - Tipado DINAMICO    -> no declaras el tipo de variables.
      - Tipado FUERTE      -> pero el tipo si es estricto en runtime.
      - Enfasis en LEGIBILIDAD.
      - Multiparadigma: orientado a objetos, procedural, funcional.
      - Usa INDENTACION para delimitar bloques (no llaves {}).

    Vamos a ver una demo de tipado dinamico vs fuerte para que
    veas exactamente que significa.
    """)

    print("\n--- TIPADO DINAMICO ---")
    print("    x = 5         # x es int")
    print("    x = 'hola'    # ahora x es str")
    print("    En otros lenguajes (Java, C#) esto seria error.")
    x = 5
    print("    type(x) =", type(x).__name__, " valor =", x)
    x = "hola"
    print("    type(x) =", type(x).__name__, " valor =", x)

    print("\n--- TIPADO FUERTE ---")
    print("    Si intentas sumar string + int -> ERROR.")
    print("    Esto evita bugs que en JavaScript pasarian.")
    try:
        _ = "5" + 3
    except TypeError as e:
        print("    Error capturado:", e)

    print("""
    >>> TU TURNO:
    Asigna a una variable 'algo' primero un numero (ej. 42),
    imprimela, luego reasignala a un texto y vuelvela a imprimir.
    Escribe cada linea cuando se te pida. 'fin' para terminar.
    """)
    lineas = []
    while True:
        linea = input("    > ")
        if linea.strip().lower() == "fin":
            break
        lineas.append(linea)
    try:
        exec("\n".join(lineas), globals())
        print("    OK -> Acabas de demostrar tipado dinamico.")
    except Exception as e:
        print("    ERROR:", e)
        print("    Solucion sugerida:")
        print("        algo = 42")
        print("        print(algo)")
        print("        algo = 'hola'")
        print("        print(algo)")
    pausa()


# ============================================================
# SECCION 2 - El Zen de Python
# ============================================================
def seccion_2_zen():
    titulo("SECCION 2 - Filosofia de Python (Zen)")
    print("""
    Python tiene un 'manifiesto' incrustado en el lenguaje. Lo
    obtienes ejecutando 'import this'. Vamos a verlo:
    """)
    pausa()
    import this  # noqa: F401  (imprime el zen al importarse)
    print("""
    Ideas clave que vas a ver una y otra vez en este curso:
      - 'Beautiful is better than ugly'  -> codigo legible.
      - 'Simple is better than complex'  -> empieza simple.
      - 'Readability counts'             -> escribe para humanos.
      - 'There should be one-- and preferably only one --obvious
         way to do it' -> en IA no inventes 5 caminos para lo mismo.
    """)
    pausa()


# ============================================================
# SECCION 3 - Que es un interprete
# ============================================================
def seccion_3_interprete():
    titulo("SECCION 3 - Que es un interprete")
    print("""
    Un INTERPRETE es un programa que ejecuta otros programas.

    Cuando escribes 'python miarchivo.py' lo que pasa es:

       miarchivo.py  ---->  COMPILADO a bytecode (.pyc)
                       --->  EJECUTADO por la PVM (Python Virtual Machine)

    Implementaciones de Python (la mas comun es CPython):
      - CPython     (escrita en C, la oficial)
      - Jython      (Java)
      - IronPython  (.NET)
      - PyPy        (la mas rapida, con JIT)

    Por eso ves carpetas '__pycache__/' con archivos .pyc:
    son la version compilada en bytecode para que la siguiente
    ejecucion sea mas rapida.
    """)
    pausa()


# ============================================================
# SECCION 4 - Formas de ejecutar codigo
# ============================================================
def seccion_4_formas_ejecucion():
    titulo("SECCION 4 - Formas de ejecutar codigo Python")
    print("""
    Hay tres modos principales:

    1) LINEA DE COMANDOS (REPL)
       Abres una terminal y escribes 'python'. Te aparece '>>>'
       y puedes escribir codigo linea a linea. Al cerrar, se va.

       REPL = Read - Evaluate - Print - Loop

    2) ARCHIVOS .py (scripts)
       Guardas tu codigo en un archivo. Lo ejecutas con:
           python miarchivo.py

       Ventaja: persiste, lo puedes compartir, lo puedes versionar.

    3) JUPYTER NOTEBOOK
       Mezcla codigo + texto + graficos + salidas.
       Perfecto para analisis de datos. Archivos .ipynb.

       Comandos magicos en Jupyter (no son Python puro):
           %time      -> mide el tiempo de UNA linea
           %%time     -> mide el tiempo de toda la celda
           !          -> ejecuta comando de shell, ej: !ls
           %run x.py  -> corre un script desde la celda

    Cual usar?
      - Aprender / experimentar  -> Jupyter o REPL
      - Producto final / pipeline -> scripts .py
    """)

    if pregunta_si_no("Quieres lanzar el REPL ahora desde aqui? "
                      "(escribiras codigo, 'salir' para volver)"):
        print("Mini-REPL: escribe expresiones Python, 'salir' para volver.")
        while True:
            try:
                expr = input(">>> ")
            except EOFError:
                break
            if expr.strip().lower() in ("salir", "exit", "quit"):
                break
            try:
                # Intentamos evaluar como expresion
                resultado = eval(expr, globals())
                if resultado is not None:
                    print(repr(resultado))
            except SyntaxError:
                # Si no es expresion (ej: a = 5) lo ejecutamos
                try:
                    exec(expr, globals())
                except Exception as e:
                    print("Error:", e)
            except Exception as e:
                print("Error:", e)
    pausa()


# ============================================================
# SECCION 5 - Comentarios
# ============================================================
def seccion_5_comentarios():
    titulo("SECCION 5 - Comentarios")
    print("""
    Los COMENTARIOS son texto que Python ignora al ejecutar.
    Sirven para explicar tu codigo a otros (y a tu yo del futuro).

    Tipos:
        # Comentario de una linea (con almohadilla)

        '''
        Cadena de varias lineas. NO es estrictamente un comentario,
        es un string que no se asigna, pero suele usarse asi.
        '''

    Convencion (PEP 8): explica el POR QUE, no el QUE.
    Mal:    x = x + 1   # suma 1 a x       <- obvio
    Bien:   x = x + 1   # avanzamos al siguiente fotograma
    """)

    print("\n--- EJEMPLO ---")
    print("    # Calcular el doble de un numero")
    print("    n = 7")
    print("    doble = n * 2   # multiplicacion")
    print("    print(doble)")
    n = 7
    doble = n * 2
    print("    Salida:", doble)

    print("""
    >>> TU TURNO:
    Escribe una linea con un comentario que explique el POR QUE
    de un calculo (no el QUE). Por ejemplo:
        precio_final = precio * 1.21  # IVA Espana = 21%
    Escribe 'fin' para terminar.
    """)
    lineas = []
    while True:
        linea = input("    > ")
        if linea.strip().lower() == "fin":
            break
        lineas.append(linea)
    contenido = "\n".join(lineas)
    if "#" in contenido:
        print("    OK -> Detecte un comentario (#).")
    else:
        print("    No vi ningun '#'. Recuerda: los comentarios")
        print("    de una linea empiezan con '#'.")
    pausa()


# ============================================================
# SECCION 6 - Ayuda integrada (help y dir)
# ============================================================
def seccion_6_help():
    titulo("SECCION 6 - Ayuda integrada (help, dir)")
    print("""
    Python trae ayuda incorporada. Esto es enorme cuando estas
    aprendiendo o cuando no recuerdas como funciona algo.

    Funciones clave:
      help(objeto)  -> documentacion completa.
      dir(objeto)   -> lista todo lo que tiene (metodos, atributos).
      objeto.__doc__ -> el docstring.
      print?        -> SOLO en Jupyter, abre la ayuda.
    """)

    print("\n--- dir(list) (recortado) ---")
    metodos_list = [m for m in dir(list) if not m.startswith("_")]
    print("   ", metodos_list)

    print("\n--- help(str.upper) ---")
    help(str.upper)

    print("""
    >>> TU TURNO:
    Pide la ayuda del metodo 'append' de las listas.
    Tip: list.append (sin parentesis) y pasalo a help().
    """)
    codigo = input("    > ")
    try:
        exec(codigo, globals())
    except Exception as e:
        print("    ERROR:", e)
        print("    Solucion sugerida: help(list.append)")
    pausa()


# ============================================================
# SECCION 7 - Performance: NumPy vs Python puro
# ============================================================
def seccion_7_performance():
    titulo("SECCION 7 - Performance: NumPy vs Python puro")
    print("""
    Una de las grandes razones por las que IA usa Python es
    NumPy: arrays vectorizados implementados en C.

    Vamos a hacer la MISMA operacion (multiplicar 10 millones de
    numeros por 2, repetida 10 veces) con:
      - Una lista nativa de Python.
      - Un np.ndarray.

    Y vamos a medir el tiempo. Veras que la diferencia es brutal.
    """)
    pausa()

    import time
    import numpy as np

    print("Creando los datos (10 millones de elementos)...")
    my_arr = np.arange(10_000_000)
    my_list = list(range(10_000_000))

    print("Midiendo NumPy...")
    t0 = time.perf_counter()
    for _ in range(10):
        _ = my_arr * 2
    t_numpy = time.perf_counter() - t0
    print(f"    NumPy:        {t_numpy:.4f} s")

    print("Midiendo lista Python (esto tarda mas)...")
    t0 = time.perf_counter()
    for _ in range(10):
        _ = [x * 2 for x in my_list]
    t_python = time.perf_counter() - t0
    print(f"    Lista Python: {t_python:.4f} s")

    factor = t_python / t_numpy if t_numpy else float("inf")
    print(f"\n    --> NumPy fue {factor:.1f} veces mas rapido.")
    print("""
    LECCION: cuando trabajes con muchos datos (que en IA es
    SIEMPRE), evita los bucles Python puros. Vectoriza con NumPy
    o pandas. Esto te ahorra horas de entrenamiento.
    """)

    print("""
    >>> TU TURNO:
    Crea un array NumPy 'a' con np.arange(1_000_000), elevalo
    al cuadrado y guardalo en 'a2'. Imprime los 5 primeros.
    Escribe 'fin' al terminar.
    """)
    lineas = []
    while True:
        linea = input("    > ")
        if linea.strip().lower() == "fin":
            break
        lineas.append(linea)
    try:
        exec("\n".join(lineas), globals())
        a2 = globals().get("a2")
        if a2 is not None and a2[0] == 0 and a2[2] == 4:
            print("    OK -> Vectorizacion correcta:", a2[:5])
        else:
            print("    Solucion sugerida:")
            print("        import numpy as np")
            print("        a = np.arange(1_000_000)")
            print("        a2 = a ** 2")
            print("        print(a2[:5])")
    except Exception as e:
        print("    ERROR:", e)
    pausa()


# ============================================================
# MENU PRINCIPAL
# ============================================================
def menu():
    secciones = [
        ("Caracteristicas de Python", seccion_1_caracteristicas),
        ("Filosofia de Python (Zen)", seccion_2_zen),
        ("Que es un interprete", seccion_3_interprete),
        ("Formas de ejecutar codigo (REPL incluido)", seccion_4_formas_ejecucion),
        ("Comentarios", seccion_5_comentarios),
        ("Ayuda integrada (help, dir)", seccion_6_help),
        ("Performance: NumPy vs Python puro", seccion_7_performance),
    ]

    while True:
        print("\n" + "#" * 64)
        print("  CLASE 01 - PYTHON 101  |  Menu")
        print("#" * 64)
        for i, (nombre, _) in enumerate(secciones, start=1):
            print(f"  {i}) {nombre}")
        print("  0) Salir")
        print("#" * 64)
        op = input("Elige una opcion: ").strip()
        if op == "0":
            print("Bien hecho. Pasa al archivo 02_python101_datatypes_interactivo.py")
            break
        if op.isdigit() and 1 <= int(op) <= len(secciones):
            secciones[int(op) - 1][1]()
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    menu()

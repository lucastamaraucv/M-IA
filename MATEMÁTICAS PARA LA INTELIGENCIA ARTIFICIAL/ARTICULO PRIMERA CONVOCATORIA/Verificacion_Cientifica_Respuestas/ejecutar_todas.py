"""
Corre las 16 verificaciones (pregunta_01.py ... pregunta_16.py) una por una,
en procesos separados, captura su salida completa y genera:

  1. informe_resultados.txt  -> salida integra de las 16 verificaciones
                                  + tabla resumen final.
  2. Un resumen por consola con el veredicto de cada pregunta.

No inventa nada: cada script hace su propia busqueda real en los PDF y/o su
propio calculo numerico; este archivo solo orquesta la ejecucion de los 16 y
agrega los resultados.

Ejecutar:
    python ejecutar_todas.py
"""
import subprocess
import sys
import os
import re

CARPETA = os.path.dirname(os.path.abspath(__file__))
NUM_PREGUNTAS = 16


def main():
    resumen = []
    bloques = []

    for i in range(1, NUM_PREGUNTAS + 1):
        nombre = f"pregunta_{i:02d}.py"
        ruta = os.path.join(CARPETA, nombre)
        print(f"Ejecutando {nombre} ...")
        proceso = subprocess.run(
            [sys.executable, ruta],
            cwd=CARPETA,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        salida = proceso.stdout
        if proceso.returncode != 0:
            salida += "\n\n*** ERROR AL EJECUTAR EL SCRIPT ***\n" + proceso.stderr

        bloques.append(salida)

        m = re.search(r"RESULTADO:\s*(CONFIRMADO|NO CONFIRMADO|DISCREPANCIA)", salida)
        veredicto = m.group(1) if m else "SIN RESULTADO (ver error)"
        resumen.append((i, veredicto))

    # ---------------------------------------------------------------
    # Informe completo
    # ---------------------------------------------------------------
    ruta_informe = os.path.join(CARPETA, "informe_resultados.txt")
    with open(ruta_informe, "w", encoding="utf-8") as f:
        f.write("INFORME DE VERIFICACION CIENTIFICA - 16 PREGUNTAS\n")
        f.write("Generado ejecutando pregunta_01.py .. pregunta_16.py con Python.\n")
        f.write("Cada verificacion abre los PDF originales con PyMuPDF y busca las\n")
        f.write("citas reales que respaldan la respuesta marcada en\n")
        f.write("respuestas_examen_verificadas.txt; las preguntas 14-16 ademas corren\n")
        f.write("calculos numericos independientes (autovalores del Hessiano,\n")
        f.write("simulacion de Monte Carlo del descenso por gradiente).\n")
        f.write("=" * 78 + "\n\n")
        for i, bloque in enumerate(bloques, start=1):
            f.write(bloque)
            f.write("\n\n")

        f.write("=" * 78 + "\n")
        f.write("TABLA RESUMEN FINAL\n")
        f.write("=" * 78 + "\n")
        for i, veredicto in resumen:
            f.write(f"  Pregunta {i:>2}: {veredicto}\n")

        n_confirmadas = sum(1 for _, v in resumen if v == "CONFIRMADO")
        f.write(f"\nTotal CONFIRMADAS: {n_confirmadas} / {NUM_PREGUNTAS}\n")

    # ---------------------------------------------------------------
    # Resumen por consola
    # ---------------------------------------------------------------
    print("\n" + "=" * 78)
    print("TABLA RESUMEN FINAL")
    print("=" * 78)
    for i, veredicto in resumen:
        print(f"  Pregunta {i:>2}: {veredicto}")
    n_confirmadas = sum(1 for _, v in resumen if v == "CONFIRMADO")
    print(f"\nTotal CONFIRMADAS: {n_confirmadas} / {NUM_PREGUNTAS}")
    print(f"\nInforme completo guardado en: {ruta_informe}")


if __name__ == "__main__":
    main()

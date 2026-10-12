"""
Proyección de la NOTA FINAL de Razonamiento Aproximado (04MIAR, VIU).

Basado en la guía de la asignatura (sección 5):
  - Prueba final ........................ 40 % a 60 %
  - Actividades de evaluación continua ... 5 % a 10 %   (aquí: Test sobre Video)
  - Grupos de debate .................... 10 %          (aquí: Foro de debate)
  - Portafolio / informe / laboratorio .. 10 % a 30 %   (aquí: Actividad 1 = el resto hasta 100 %)
  - Requisito: aprobar con >= 5 el portafolio y la prueba final.

Como la guía solo da RANGOS, el script prueba todas las combinaciones de pesos que
suman 100 % y te da el rango completo, la mediana y qué nota mínima necesitas.

Uso:
    python nota_final.py                      # usa MIS_NOTAS (editables abajo)
    python nota_final.py --act1 9 --foro 8    # simula otras notas pendientes
"""
import argparse

# ---- TUS NOTAS (sobre 10). Edita las pendientes cuando las publiquen ----
MIS_NOTAS = {
    "test": 10.0,    # Test sobre Video (calificado)
    "examen": 6.4,   # Examen 1ª convocatoria (calificado)
    "act1": 10.0,    # Actividad 1: sistema borroso (PENDIENTE: hipótesis)
    "foro": 10.0,    # Foro de debate (PENDIENTE: hipótesis)
}
# Rangos de la guía (en %). Actividad 1 = portafolio/laboratorio: 10 a 30 %.
RANGO_EXAMEN = (40, 60)
RANGO_TEST = (5, 10)
PESO_FORO = 10
RANGO_ACT1 = (10, 30)
# ------------------------------------------------------------------------


def clasificar(nota):
    if nota < 5:
        return "Suspenso"
    if nota < 7:
        return "Aprobado"
    if nota < 9:
        return "Notable"
    return "Sobresaliente (Matrícula de Honor si >= 9,5)"


def combinaciones_de_pesos():
    """Todas las combinaciones de pesos (paso 1 %) que cumplen la guía y suman 100 %."""
    for w_ex in range(RANGO_EXAMEN[0], RANGO_EXAMEN[1] + 1):
        for w_test in range(RANGO_TEST[0], RANGO_TEST[1] + 1):
            w_act1 = 100 - w_ex - w_test - PESO_FORO
            if RANGO_ACT1[0] <= w_act1 <= RANGO_ACT1[1]:
                yield {"examen": w_ex, "test": w_test, "foro": PESO_FORO, "act1": w_act1}


def nota_final(notas, pesos):
    return sum(notas[k] * pesos[k] for k in notas) / 100


def cuantil(ordenados, q):
    return ordenados[int(round(q * (len(ordenados) - 1)))]


def resumen(notas):
    finales = sorted(nota_final(notas, p) for p in combinaciones_de_pesos())
    return finales


def main():
    ap = argparse.ArgumentParser(description="Proyección de la nota final")
    for k in MIS_NOTAS:
        ap.add_argument(f"--{k}", type=float, help=f"nota de {k} sobre 10")
    args = ap.parse_args()
    notas = dict(MIS_NOTAS)
    for k in notas:
        valor = getattr(args, k)
        if valor is not None:
            if not 0 <= valor <= 10:
                raise SystemExit(f"ERROR: la nota de {k} debe estar entre 0 y 10.")
            notas[k] = valor

    pesos_validos = list(combinaciones_de_pesos())
    finales = resumen(notas)
    mediana = cuantil(finales, 0.5)

    print("=== Proyección de la nota final: Razonamiento Aproximado ===\n")
    print("Notas usadas: " + ", ".join(f"{k}={v:g}" for k, v in notas.items()))
    print(f"Combinaciones de pesos válidas según la guía: {len(pesos_validos)}\n")

    print("NOTA FINAL PROYECTADA (sobre 10)")
    print(f"  Mínima : {finales[0]:.2f}")
    print(f"  Mediana: {mediana:.2f}   <- valor central más representativo")
    print(f"  Máxima : {finales[-1]:.2f}")
    print(f"  Calificación (mediana): {clasificar(mediana)}\n")

    print("REQUISITOS DE LA GUÍA (cada apartado >= 5)")
    print(f"  Prueba final ({notas['examen']:g}) : {'OK' if notas['examen'] >= 5 else 'NO CUMPLE'}")
    print(f"  Actividad 1  ({notas['act1']:g}) : {'OK' if notas['act1'] >= 5 else 'NO CUMPLE'}")
    aprobado = finales[0] >= 5 and notas["examen"] >= 5 and notas["act1"] >= 5
    print(f"  ¿Aprobado en TODOS los escenarios?: {'SÍ' if aprobado else 'NO (depende de los pesos)'}\n")

    print("SI LA ACTIVIDAD 1 Y EL FORO SALEN IGUAL (otros escenarios)")
    print(f"  {'Nota Act.1 y Foro':>18} {'Mínima':>8} {'Mediana':>8} {'Máxima':>8}  Calificación (mediana)")
    for g in (10, 9, 8, 7, 6, 5, 4):
        f = resumen({**notas, "act1": g, "foro": g})
        med = cuantil(f, 0.5)
        print(f"  {g:>18} {f[0]:>8.2f} {med:>8.2f} {f[-1]:>8.2f}  {clasificar(med)}")

    # Nota mínima común para asegurar >= 5 en el peor reparto de pesos
    minimo = next((g / 10 for g in range(0, 101)
                   if min(resumen({**notas, "act1": g / 10, "foro": g / 10})) >= 5), None)
    if minimo is not None:
        print(f"\nCon tu examen ({notas['examen']:g}) y test ({notas['test']:g}), necesitas al menos "
              f"{max(minimo, 5):.1f} en Actividad 1 (y Foro) para asegurar >= 5 de nota final "
              f"y cumplir el mínimo del apartado.")

    print("\nNota: es una proyección. La nota oficial la publica el profesor/universidad.")


if __name__ == "__main__":
    main()
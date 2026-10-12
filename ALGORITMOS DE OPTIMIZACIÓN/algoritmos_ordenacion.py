"""
Algoritmos de ordenación — VC2 (03MIAR Algoritmos de Optimización)

Aclaración importante (pregunta trampa típica de examen):
Quick Sort y Merge Sort son Divide y Vencerás, NO Programación Dinámica.

- Divide y Vencerás: los sub-problemas son DISJUNTOS (no se solapan).
  Quick Sort separa la lista en "menores que el pivote" / "mayores que el
  pivote" y esos dos grupos nunca se vuelven a mezclar ni a recalcular.
- Programación Dinámica: los sub-problemas se REPITEN en distintas ramas,
  por eso hace falta memoizar (ver el ejemplo del "viaje por el río").

Ordenar una lista nunca repite sub-problemas, así que Programación
Dinámica no aplica a ningún algoritmo de ordenación de esta sesión.

Complejidades según el material del curso:
  Inserción: O(n) mejor caso, O(n^2) peor caso.
  Burbuja:   sin valor Big-O dado en las diapositivas.
  Selección: O(n^2) siempre, independientemente de la disposición inicial.
  Mezcla (Merge Sort): O(n log n) siempre, en todos los casos.
  Quick Sort: O(n^2) peor caso, O(n log n) mejor caso / promedio.
"""

import random
import sys
import time


def insercion_sort(lista):
    for i in range(1, len(lista)):
        valor = lista[i]
        j = i - 1
        while j >= 0 and lista[j] > valor:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = valor
    return lista


def burbuja_sort(lista):
    n = len(lista)
    for i in range(n - 1):
        hubo_intercambio = False
        for j in range(n - 1 - i):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                hubo_intercambio = True
        if not hubo_intercambio:
            break
    return lista


def seleccion_sort(lista):
    n = len(lista)
    for i in range(n - 1):
        indice_minimo = i
        for j in range(i + 1, n):
            if lista[j] < lista[indice_minimo]:
                indice_minimo = j
        lista[i], lista[indice_minimo] = lista[indice_minimo], lista[i]
    return lista


def merge_sort(lista):
    if len(lista) <= 1:
        return lista

    mitad = len(lista) // 2
    izquierda = merge_sort(lista[:mitad])
    derecha = merge_sort(lista[mitad:])

    return _combinar(izquierda, derecha)


def _combinar(izquierda, derecha):
    resultado = []
    i = j = 0
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado


def particionar(lista, inicio, fin):
    pivote = lista[fin]           # elegimos el último elemento como pivote
    i = inicio - 1                # marca el límite de "menores que el pivote"

    for j in range(inicio, fin):
        if lista[j] <= pivote:
            i += 1
            lista[i], lista[j] = lista[j], lista[i]   # intercambio

    lista[i + 1], lista[fin] = lista[fin], lista[i + 1]  # coloca el pivote en su sitio
    return i + 1


def particionar_aleatorio(lista, inicio, fin):
    pivote_random = random.randint(inicio, fin)
    lista[pivote_random], lista[fin] = lista[fin], lista[pivote_random]
    return particionar(lista, inicio, fin)


def quick_sort(lista, inicio=0, fin=None, aleatorio=True):
    if fin is None:
        fin = len(lista) - 1

    if inicio < fin:
        # 1. Particionar: coloca el pivote en su posición final correcta
        if aleatorio:
            posicion_pivote = particionar_aleatorio(lista, inicio, fin)
        else:
            posicion_pivote = particionar(lista, inicio, fin)

        # 2. Dividir: ordena recursivamente cada mitad (sub-problemas DISJUNTOS)
        quick_sort(lista, inicio, posicion_pivote - 1, aleatorio)   # parte izquierda (menores)
        quick_sort(lista, posicion_pivote + 1, fin, aleatorio)      # parte derecha (mayores)
        # 3. Combinar: no hace falta combinar nada extra,
        #    la lista ya queda ordenada en el mismo espacio (in-place)

    return lista


if __name__ == "__main__":
    ejemplo = [54, 26, 93, 17, 77, 31, 44, 55, 20]

    print("Lista original: ", ejemplo)
    print("Inserción:      ", insercion_sort(ejemplo.copy()))
    print("Burbuja:        ", burbuja_sort(ejemplo.copy()))
    print("Selección:      ", seleccion_sort(ejemplo.copy()))
    print("Mezcla:         ", merge_sort(ejemplo.copy()))
    print("Quick Sort:     ", quick_sort(ejemplo.copy()))

    # --- Comportamiento con 1 millón de elementos desordenados ---
    sys.setrecursionlimit(2_000_000)  # Python limita la recursión por defecto

    datos = [random.randint(1, 1_000_000) for _ in range(1_000_000)]

    inicio_tiempo = time.time()
    quick_sort(datos.copy(), aleatorio=False)  # pivote = último elemento
    print(f"\nQuick Sort (pivote fijo, datos al azar):    {time.time()-inicio_tiempo:.2f}s")

    inicio_tiempo = time.time()
    quick_sort(datos.copy(), aleatorio=True)  # pivote aleatorio
    print(f"Quick Sort (pivote aleatorio, datos al azar): {time.time()-inicio_tiempo:.2f}s")

    # Con datos ya ordenados, el pivote fijo (último elemento) degenera a O(n^2):
    # cada partición solo separa 1 elemento del resto, en vez de dividir por la mitad.
    # El pivote aleatorio evita ese peor caso independientemente del orden de entrada.

# Quick Sort explicado paso a paso, ordenando solo 3 números.
#
# Idea sencilla: tomamos el ÚLTIMO número como "pivote". Recorremos el
# resto de la lista comparando cada número con el pivote:
#   - si es MENOR o igual, lo movemos junto a los demás menores (izquierda)
#   - si es MAYOR, se queda donde está (a la derecha)
# Al final, el pivote se coloca justo en el punto donde separan los
# menores de los mayores — esa es su posición DEFINITIVA, ya no se mueve más.
# Luego repetimos exactamente lo mismo, por separado, con la parte de los
# menores y con la parte de los mayores (eso es la recursión).
#
# Es "Divide y Vencerás" (no Programación Dinámica) porque los menores y
# los mayores son dos grupos que ya nunca se vuelven a mezclar ni a
# recalcular entre sí.


def particionar(lista, inicio, fin):
    pivote = lista[fin]
    print(f"  Pivote elegido (último número del tramo): {pivote}")
    i = inicio - 1  # todavía no hemos encontrado ningún menor que el pivote

    for j in range(inicio, fin):
        print(f"    ¿{lista[j]} es menor o igual que {pivote}?", end=" ")
        if lista[j] <= pivote:
            i += 1
            print("Sí -> lo paso al grupo de los menores")
            lista[i], lista[j] = lista[j], lista[i]
        else:
            print("No -> se queda en el grupo de los mayores")

    lista[i + 1], lista[fin] = lista[fin], lista[i + 1]
    print(f"  Pivote {pivote} colocado en su posición definitiva -> {lista}\n")
    return i + 1


def quick_sort(lista, inicio=0, fin=None):
    if fin is None:
        fin = len(lista) - 1

    if inicio < fin:
        print(f"Tramo a ordenar: {lista[inicio:fin + 1]}")
        pos_pivote = particionar(lista, inicio, fin)

        quick_sort(lista, inicio, pos_pivote - 1)   # ahora, lo mismo con los menores
        quick_sort(lista, pos_pivote + 1, fin)      # ahora, lo mismo con los mayores
    elif inicio == fin:
        print(f"El número {lista[inicio]} está solo -> ya está en su sitio\n")

    return lista


numeros = [82, 15, 4]

print("Lista original:", numeros, "\n")
quick_sort(numeros)
print("Lista ordenada:", numeros)

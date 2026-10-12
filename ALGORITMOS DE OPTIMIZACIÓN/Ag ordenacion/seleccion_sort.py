def seleccion_sort(lista):
    n = len(lista)
    for i in range(n - 1):
        indice_minimo = i
        for j in range(i + 1, n):
            if lista[j] < lista[indice_minimo]:
                indice_minimo = j
        lista[i], lista[indice_minimo] = lista[indice_minimo], lista[i]
    return lista


ejemplo = [26, 54, 93, 17, 77, 31, 44, 55, 20]
print(seleccion_sort(ejemplo))

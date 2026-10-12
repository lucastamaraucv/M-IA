def insercion_sort(lista):
    for i in range(1, len(lista)):
        valor = lista[i]
        j = i - 1
        while j >= 0 and lista[j] > valor:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = valor
    return lista


ejemplo = [8, 7, 5, 9, 1, 6, 2, 4, 3]
print(insercion_sort(ejemplo))

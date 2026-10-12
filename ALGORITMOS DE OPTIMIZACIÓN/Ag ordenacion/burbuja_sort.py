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


ejemplo = [54, 26, 93, 17, 77, 31, 44, 55, 20]
print(burbuja_sort(ejemplo))

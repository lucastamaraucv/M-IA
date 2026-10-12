def Torres_Hanoi_iterativa(N, desde, hasta):
    pila = [('resolver', N, desde, hasta)]

    while pila:
        tarea = pila.pop()

        if tarea[0] == 'mover':
            _, d, h = tarea
            print("Lleva la ficha ", d, " hasta ", h)
        else:
            _, n, d, h = tarea
            if n == 1:
                print("Lleva la ficha ", d, " hasta ", h)
            else:
                aux = 6 - d - h
                pila.append(('resolver', n-1, aux, h))
                pila.append(('mover', d, h))
                pila.append(('resolver', n-1, d, aux))

Torres_Hanoi_iterativa(3, 1, 3)
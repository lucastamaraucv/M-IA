def separador(loriginal):
    # Creamos dos copias independientes
    listaint = loriginal.copy()
    listastr = loriginal.copy()

    for i in range(len(loriginal)):
        # Convertimos cada elemento al tipo que corresponde en cada lista
        listaint[i] = int(loriginal[i])
        listastr[i] = str(loriginal[i])

    return listaint, listastr

loriginal=["1",2,"3",4,"5"]
listaint,listastr= separador(loriginal)

print(listaint,listastr)

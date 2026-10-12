datos=("1",2,"3",4,"5",6)
def organizador(datos):
    listaEntero=[]
    ListaStr=[]
    print("datos en rango",range(len(datos)))
    for i in range(len(datos)):
        listaEntero.append(int(datos[i]))
        ListaStr.append(str(datos[i]))

    return listaEntero,ListaStr

ListaDatosEntero,ListaCadena=organizador(datos)


print("lista de entero",ListaDatosEntero)
print("lista de string",ListaCadena)
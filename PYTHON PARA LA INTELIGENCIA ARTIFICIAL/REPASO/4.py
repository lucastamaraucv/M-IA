#[print(x)for x in range(1,11)]

#[print(x**2)for x in range(1,6)]

#[print(x)for x in range(1,11) if x%2==0]

#palabras = ["sol", "computadora", "casa", "python", "IA", "universidad"]

#[print(palabra," -->",len(palabra)," -->","si entra" if len(palabra)>=11 else "no entra") for palabra in palabras ]


#nombres = ["ana", "pedro", "lucas", "maria"]
#[print(nombre.upper()) for nombre in nombres]

#numeros = [1, 2, 3, 4, 5, 6]
#[print(x,"-> par ->",x, "² =",x**2) if x%2==0 else print(x,"-> impar -> se descarta") for x in numeros]


#numeros = [-5, 3, -2, 8, -1, 10, 0]
#print([(x) for x in numeros if x>0])


#palabras = ["Python", "IA", "Algoritmo", "Lista"]

#print([len(x) for x in palabras ])



#numeros = [1, 2, 3, 4, 5, 6]

#print(["par"if x%2==0  else"impar" for x in numeros ])

#numeros = [2, 5, 8, 11, 14, 17, 20]
#[print(x,"par y mayor que 5 -->",x**2) if x%2==0 and x>5 else  print(x,",par pero no es mayor que 5 --->")   if x%2==0 else print(x,"es impar")  for x in numeros  ]
#
#
#numeros = [2, 5, 8, 11, 14, 17, 20]
#
#for x in numeros:
#    if x%2==0 and x>5:
#        print(x,"es par y mayor que 5")
#    elif x%2==0 :
#        print(x,"es par pero no es mayor 5 ")
#    elif x%2!=0:
#        print(x,"es impar")
#    else:
#        print("ninguna de las anteriores")    
#


#cuadradado = [x**2 for in range(1,21) if x % 2 !=0]
#print(cuadradado)
#
#nombres ={"ana", "bob","Carlos"}
#
#longitudes ={n: len(n) for n in nombres}
#print(longitudes)
#
#pares = {x:x**2 for x in range(1,8) if x %2==0}
#print(pares)
#


#def estadisticas(numeros: list) -> dict:
#    # TODO: escribe tu código aquí
#    if all(isinstance(x, (int)) for x in numeros):
#       return{
#        "min":min(numeros),
#        "max": max(numeros),
#        "media": sum(numeros)/len(numeros),
#        "n": len(numeros)}
#        
#    else:
#        print("no es numero")
#
#        
#
#resultado = estadisticas([3, 1, 4, 1, 5, 9, 2, 6])
#
#for clave, valor in resultado.items():
#    print(clave, ":", valor)




import random

def crear_individuo(n_genes):
    return [random.randint(0, 1) for _ in range(n_genes)]

def crear_poblacion(tam_poblacion, n_genes):
    return [crear_individuo(n_genes) for _ in range(tam_poblacion)]

poblacion = crear_poblacion(6, 8)


#print(" la poblacion es ",poblacion)
for i,individuo in enumerate(poblacion):
    print ("posicion  es ", i, "individuo",individuo)

# el curso insiste en que la poblacion inicial sea VARIADA: que aparezcan
# ambos alelos (0 y 1) en cada posicion, no una poblacion casi identica
for gen in range(8):
    alelos = set(individuo[gen] for individuo in poblacion)
    print(f"gen {gen}: alelos presentes = {alelos}")

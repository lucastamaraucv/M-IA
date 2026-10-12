/* ──────────── Examples ──────────── */
const EX = [
/* S00 */
{name:'S00 · Variables y tipos', code:
`nombre = "Ana"
edad   = 25
altura = 1.65
activo = True

print(nombre, edad, altura, activo)
print(type(nombre), type(edad), type(altura), type(activo))

x, y, z = 10, 20, 30
print("Suma:", x + y + z)
print("id de edad:", id(edad))`},

{name:'S00 · Strings y slicing', code:
`s = "Python para IA"
print(s[0])
print(s[-2:])
print(s[7:12])
print(s[::-1])
print(s.upper())
print(s.split(" "))
print(s.replace("Python", "Aprender"))
print(len(s))`},

{name:'S00 · Operadores', code:
`print(7 // 2)
print(7 % 2)
print(2 ** 10)

print(5 > 3 and 2 < 4)
print(not False)

frutas = ["manzana", "pera", "naranja"]
print("pera" in frutas)
print("uva" not in frutas)`},

/* S01 */
{name:'S01 · Lista, Tupla, Set, Dict', code:
`nums = [3, 1, 4, 1, 5, 9]
nums.append(2)
nums.sort()
print("Lista:", nums)

coordenada = (40.41, -3.70)
print("Tupla:", coordenada)

colores = {"rojo", "azul", "rojo", "verde"}
print("Set:", colores)

persona = {"nombre": "Ana", "edad": 30}
persona["ciudad"] = "Madrid"
print("Dict:", persona)
print("Keys:", list(persona.keys()))`},

/* S02 */
{name:'S02 · if / elif / else', code:
`nota = 7.5

if nota >= 9:
    cal = "Sobresaliente"
elif nota >= 7:
    cal = "Notable"
elif nota >= 5:
    cal = "Aprobado"
else:
    cal = "Suspenso"

print(f"Nota {nota}: {cal}")

edad = 20
status = "mayor" if edad >= 18 else "menor"
print(f"Con {edad} anos eres {status} de edad")`},

{name:'S02 · while, for, enumerate', code:
`i = 0
while True:
    if i >= 5:
        break
    print(i, end=" ")
    i += 1
print()

for n in range(10):
    if n % 2 == 0:
        continue
    print(n, end=" ")
print()

frutas = ["manzana", "pera", "naranja"]
for i, f in enumerate(frutas):
    print(f"  [{i}] {f}")`},

{name:'S02 · for: listas, strings y range', code:
`numeros = [10, 20, 30]

# for x in lista: recorre los VALORES directamente, uno por uno
for x in numeros:
    print(x)

# for x in "texto": un string tambien se puede recorrer, caracter por caracter
for letra in "hola":
    print(letra, end="-")
print()

# range(inicio, fin, paso): el paso puede ser negativo para ir hacia atras
for i in range(10, 0, -2):
    print(i, end=" ")
print()

# reversed() y sorted() devuelven un iterable NUEVO: no modifican la lista original
for x in reversed(numeros):
    print(x, end=" ")
print()

desordenada = [5, 1, 4, 2]
for x in sorted(desordenada):
    print(x, end=" ")
print()
print("la lista original sigue igual:", desordenada)`},

{name:'S02 · for: diccionarios, zip y desempaquetado', code:
`persona = {"nombre": "Ana", "edad": 30, "ciudad": "Lima"}

# for clave in dict: por defecto un diccionario recorre solo sus CLAVES
for clave in persona:
    print(clave)

# .values(): recorre solo los VALORES
for valor in persona.values():
    print(valor)

# .items(): recorre pares (clave, valor) a la vez — por eso se "desempaquetan"
# en dos variables, k y v, igual que hiciste vos mas arriba
for k, v in persona.items():
    print(f"{k} -> {v}")

# zip(lista1, lista2): recorre DOS listas en paralelo, posicion a posicion
nombres = ["Ana", "Bob", "Carlos"]
edades = [30, 25, 40]
for nombre, edad in zip(nombres, edades):
    print(f"{nombre} tiene {edad} años")

# una lista de tuplas se desempaqueta exactamente igual que .items()
pares = [(1, "uno"), (2, "dos"), (3, "tres")]
for numero, palabra in pares:
    print(numero, palabra)

# for anidado: por cada fila de la matriz, otro for recorre sus columnas
matriz = [[1, 2], [3, 4]]
for fila in matriz:
    for celda in fila:
        print(celda, end=" ")
print()`},

/* S03 */
{name:'S03 · List y Dict comprehension', code:
`cuadrados = [x**2 for x in range(1, 21) if x % 2 != 0]
print(cuadrados)

nombres = ["Ana", "Bob", "Carlos"]
longitudes = {n: len(n) for n in nombres}
print(longitudes)

pares = {x: x**2 for x in range(1, 8) if x % 2 == 0}
print(pares)`},

{name:'S03 · Comprehension: filtrar vs transformar', code:
`numeros = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6]

# 1) La comprehension SIEMPRE construye una lista con lo que pongas antes del "for".
# Si pones print(x) ahi, la lista queda llena de None (lo que retorna print).
etiquetas = ["par" if x % 2 == 0 else "impar" for x in numeros]
print(etiquetas)

ruido = [print(x) for x in numeros[:3]]
print("ruido contiene:", ruido)

# 2) if SOLO como filtro: no hay "else" porque el que no cumple simplemente no entra
positivos = [x for x in numeros if x > 0]
print(positivos)

# 3) if/else para ELEGIR un valor: el resultado va ANTES del for porque es una expresion, no un filtro
signo = ["cero" if x == 0 else ("positivo" if x > 0 else "negativo") for x in numeros]
print(signo)

# 4) filtrar (if al final) + transformar (expresion al inicio) al mismo tiempo
cuadrados_pares = [x**2 for x in numeros if x % 2 == 0]
print(cuadrados_pares)

# 5) varias condiciones: "and" exige las dos, "or" exige al menos una
pares_grandes = [x**2 for x in numeros if x % 2 == 0 and x > 3]
print(pares_grandes)
impares_o_negativos = [x for x in numeros if x % 2 != 0 or x < 0]
print(impares_o_negativos)`},

{name:'S03 · Comprehension: if/elif/else como expresion', code:
`numeros = [-4, 0, 3, 8, 15]

# 6) Forma tradicional: un valor distinto por rama
def clasificar_tradicional(x):
    if x < 0:
        resultado = "negativo"
    elif x == 0:
        resultado = "cero"
    else:
        resultado = "positivo"
    return resultado

clasico = [clasificar_tradicional(x) for x in numeros]
print(clasico)

# Misma logica como expresion encadenada: cada "elif" se vuelve otro "else ... if ..."
expresion = ["negativo" if x < 0 else "cero" if x == 0 else "positivo" for x in numeros]
print(expresion)

# 7) Esto NO existe en Python, no se puede escribir "elif" dentro de una expresion:
#   "negativo" if x < 0 elif x == 0 "cero" else "positivo"   -> SyntaxError
# La forma correcta encadena "else <valor> if <condicion> else <valor>"

# 8) no repitas la condicion: si ya comprobaste x % 2 == 0, el else YA es el caso impar
par_o_impar = ["par" if x % 2 == 0 else "impar" for x in numeros]
print(par_o_impar)

# 9) orden de evaluacion: para cada x primero se revisa el "if" del final (el filtro);
# solo si pasa, se calcula la expresion de la izquierda
grandes_pares = [x**2 for x in numeros if x % 2 == 0 and x > 5]
print(grandes_pares)`},

/* S04 */
{name:'S04 · try / except / else / finally', code:
`def dividir(a, b):
    try:
        resultado = a / b
    except ZeroDivisionError:
        print("Error: division por cero")
        return None
    else:
        print(f"{a} / {b} = {resultado}")
        return resultado
    finally:
        print("--- fin operacion ---")

dividir(10, 2)
dividir(5, 0)`},

/* S05 */
{name:'S05 · Funciones con anotaciones', code:
`def estadisticas(numeros: list) -> dict:
    if not numeros:
        return {}
    return {
        "min": min(numeros),
        "max": max(numeros),
        "media": sum(numeros) / len(numeros),
        "n": len(numeros)
    }

resultado = estadisticas([3, 1, 4, 1, 5, 9, 2, 6])
for k, v in resultado.items():
    print(f"  {k}: {v}")`},

{name:'S05 · *args y **kwargs', code:
`def mostrar(*args, **kwargs):
    print("Posicionales:", args)
    print("Nombrados:", kwargs)

mostrar(1, 2, 3, nombre="Ana", edad=25)

numeros = [10, 20, 30]
print(max(*numeros))

config = {"sep": " | ", "end": "\\n"}
print("a", "b", "c", **config)`},

{name:'S05 · Lambda, recursion, closure', code:
`personas = [("Ana", 30), ("Bob", 25), ("Clara", 35)]
orden_edad = sorted(personas, key=lambda p: p[1])
print(orden_edad)

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(6))

def make_contador(inicio=0):
    cuenta = [inicio]
    def incrementar():
        cuenta[0] += 1
        return cuenta[0]
    return incrementar

c = make_contador()
print(c(), c(), c())`},

/* S06 */
{name:'S06 · Clases y objetos', code:
`class Rectangulo:
    def __init__(self, ancho: float, alto: float):
        self.ancho = ancho
        self.alto = alto

    def area(self) -> float:
        return self.ancho * self.alto

    def perimetro(self) -> float:
        return 2 * (self.ancho + self.alto)

    def __str__(self) -> str:
        return f"Rectangulo({self.ancho}x{self.alto})"

r = Rectangulo(5, 3)
print(r)
print(f"Area: {r.area()}")
print(f"Perimetro: {r.perimetro()}")`},

{name:'S06 · Herencia y polimorfismo', code:
`class Animal:
    def __init__(self, nombre: str, sonido: str):
        self.nombre = nombre
        self._sonido = sonido

    def hablar(self) -> str:
        return f"{self.nombre} dice: {self._sonido}"

class Perro(Animal):
    def __init__(self, nombre: str, raza: str):
        super().__init__(nombre, "Guau")
        self.raza = raza

    def hablar(self) -> str:
        return f"{self.nombre} ({self.raza}) dice: {self._sonido}!"

    def buscar(self) -> str:
        return f"{self.nombre} esta buscando..."

perro = Perro("Rex", "Pastor Aleman")
print(perro.hablar())
print(perro.buscar())
print(isinstance(perro, Animal))`},

{name:'S06 · @property y @staticmethod', code:
`class Temperatura:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, valor: float):
        if valor < -273.15:
            raise ValueError("Bajo cero absoluto")
        self._celsius = valor

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9/5 + 32

    @staticmethod
    def punto_ebullicion() -> float:
        return 100.0

t = Temperatura(25)
print(f"{t.celsius}C = {t.fahrenheit}F")
t.celsius = 100
print(f"{t.celsius}C = {t.fahrenheit}F")
print("Ebullicion:", Temperatura.punto_ebullicion())`},

{name:'S06 · Clases abstractas (ABC)', code:
`from abc import ABC, abstractmethod

class Figura(ABC):
    @abstractmethod
    def area(self) -> float: pass

    @abstractmethod
    def perimetro(self) -> float: pass

    def descripcion(self):
        return f"{type(self).__name__}: area={self.area():.2f}, per={self.perimetro():.2f}"

class Circulo(Figura):
    def __init__(self, radio: float):
        self.radio = radio
    def area(self): return 3.14159 * self.radio ** 2
    def perimetro(self): return 2 * 3.14159 * self.radio

class Cuadrado(Figura):
    def __init__(self, lado: float):
        self.lado = lado
    def area(self): return self.lado ** 2
    def perimetro(self): return 4 * self.lado

figuras = [Circulo(5), Cuadrado(4), Circulo(3)]
for f in figuras:
    print(f.descripcion())`},

/* S07 */
{name:'S07 · Stack, Queue, Heap', code:
`from collections import deque
import heapq

pila = deque()
pila.append("a")
pila.append("b")
pila.append("c")
print("Stack:", list(pila))
print("Pop:", pila.pop())

cola = deque()
cola.append("primero")
cola.append("segundo")
cola.append("tercero")
print("Queue:", list(cola))
print("Dequeue:", cola.popleft())

tareas = []
heapq.heappush(tareas, (3, "Tarea C"))
heapq.heappush(tareas, (1, "Tarea A"))
heapq.heappush(tareas, (2, "Tarea B"))
print("Siguiente:", heapq.heappop(tareas))`},

{name:'S07 · Grafos y BFS', code:
`from collections import deque

grafo = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C"]
}

def bfs(grafo, inicio):
    visitados = []
    cola = deque([inicio])
    visto = {inicio}
    while cola:
        nodo = cola.popleft()
        visitados.append(nodo)
        for vecino in grafo[nodo]:
            if vecino not in visto:
                visto.add(vecino)
                cola.append(vecino)
    return visitados

print("BFS desde A:", bfs(grafo, "A"))
print("BFS desde C:", bfs(grafo, "C"))`},

/* S08 */
{name:'S08 · map / filter / reduce', code:
`from functools import reduce

numeros = [1, 2, 3, 4, 5]
dobles = list(map(lambda x: x*2, numeros))
print("map dobles:", dobles)

pares = list(filter(lambda x: x % 2 == 0, range(1, 11)))
print("filter pares:", pares)

total = reduce(lambda x, y: x + y, numeros)
print("reduce suma:", total)

palabras = ["hola", "mundo", "python"]
mayus = list(map(str.upper, palabras))
print("map upper:", mayus)`},

/* S09 */
{name:'S09 · yield y next (generadores)', code:
`def cuadrados_lista(n):
    return [i**2 for i in range(n)]

def cuadrados_gen(n):
    for i in range(n):
        yield i**2

lst = cuadrados_lista(5)
print("Lista:", lst)

gen = cuadrados_gen(5)
print("Primero:", next(gen))
print("Segundo:", next(gen))
print("Resto:", list(gen))

def contador(inicio, fin):
    while inicio <= fin:
        yield inicio
        inicio += 1

for n in contador(1, 5):
    print(n, end=" ")
print()`},

/* S10 NumPy */
{name:'S10 · NumPy Arrays basicos', code:
`import numpy as np

a1 = np.array([1, 2, 3, 4, 5])
a2 = np.array([[1, 2, 3], [4, 5, 6]])
a3 = np.zeros((3, 4))
a4 = np.arange(0, 20, 2)
a5 = np.linspace(0, 1, 5)
a6 = np.eye(3)

print("1D:", a1)
print("2D shape:", a2.shape, "ndim:", a2.ndim)
print("zeros 3x4 shape:", a3.shape)
print("arange:", a4)
print("linspace:", a5)`},

{name:'S10 · NumPy Indexado y slicing', code:
`import numpy as np

arr = np.array([[10, 20, 30],
                [40, 50, 60],
                [70, 80, 90]])

print("Elemento [1,2]:", arr[1, 2])
print("Fila 0:", arr[0])
print("Columna 1:", arr[:, 1])
print("Submatriz:", arr[:2, 1:])
print("Mayores de 50:", arr[arr > 50])

sub = arr[0:2, 0:2].copy()
sub[0, 0] = 999
print("Original arr[0,0]:", arr[0, 0])`},

{name:'S10 · NumPy Broadcasting y stats', code:
`import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])
v = np.array([10, 20, 30])
print("Broadcasting a+v:", a + v)
print("a * 2:", a * 2)

data = np.array([[4, 2, 7, 1],
                 [3, 8, 5, 9],
                 [6, 0, 4, 2]])
print("Media total:", data.mean())
print("Media columnas:", data.mean(axis=0))
print("Media filas:", data.mean(axis=1))
print("Std:", data.std().round(2))`},

{name:'S10 · NumPy Algebra lineal', code:
`import numpy as np

A = np.array([[2, 1], [1, 3]])
b = np.array([5, 10])

x = np.linalg.solve(A, b)
print("Solucion x:", x)
print("Verificacion A@x:", A @ x)

arr = np.array([-3, -1, 0, 2, 4, -5, 7])
sin_neg = np.where(arr >= 0, arr, 0)
print("Sin negativos:", sin_neg)

np.random.seed(42)
m = np.random.randint(1, 101, (3, 3))
print("Matriz aleatoria:", m)
print("Media por fila:", m.mean(axis=1).round(2))`},

/* S11 Pandas */
{name:'S11 · Pandas Series', code:
`import pandas as pd

s = pd.Series([10, 20, 30, 40, 50], index=["a", "b", "c", "d", "e"])
print("Serie:", s.to_dict())
print("Elemento c:", s["c"])
print("Slicing a:c:", s["a":"c"].to_dict())
print("Mayores 25:", s[s > 25].to_dict())
print("Media:", s.mean(), "Suma:", s.sum())`},

{name:'S11 · Pandas DataFrame', code:
`import pandas as pd

df = pd.DataFrame({
    "Nombre": ["Ana", "Luis", "Maria", "Carlos"],
    "Edad": [30, 25, 35, 28],
    "Ciudad": ["Madrid", "Barcelona", "Sevilla", "Valencia"]
})

print("Shape:", df.shape)
print("Nombres:", df["Nombre"].tolist())
print("Edades:", df["Edad"].tolist())
print("Mayor de 27:", df[df["Edad"] > 27]["Nombre"].tolist())
print("Iloc[0]:", df.iloc[0].to_dict())`},

{name:'S11 · Pandas groupby y apply', code:
`import pandas as pd

df = pd.DataFrame({
    "genero": ["F", "M", "F", "M", "F"],
    "edad":   [30, 25, 35, 28, 22],
    "puntos": [90, 75, 85, 92, 88]
})

rango = df[["edad", "puntos"]].apply(lambda c: c.max() - c.min())
print("Rango por columna:", rango.to_dict())

por_genero = df.groupby("genero")[["edad","puntos"]].mean()
print("Media F:", por_genero.loc["F"].to_dict())
print("Media M:", por_genero.loc["M"].to_dict())`},

{name:'S11 · Pandas merge', code:
`import pandas as pd

clientes = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "nombre": ["Ana", "Luis", "Maria", "Carlos"]
})

pedidos = pd.DataFrame({
    "cliente_id": [1, 1, 2, 3],
    "producto": ["Laptop", "Raton", "Monitor", "Teclado"],
    "precio": [1200, 25, 300, 80]
})

resultado = clientes.merge(pedidos, left_on="id", right_on="cliente_id", how="left")
print("Pedidos:", resultado[["nombre","producto","precio"]].to_dict("records"))

total = resultado.groupby("nombre")["precio"].sum()
print("Total por cliente:", total.to_dict())`},

/* Additional sessions S05/S07/S10-S16 */
{name:'S05 · Archivos con io.StringIO', code:
`import io

buf = io.StringIO()
buf.write("Primera linea\\n")
buf.write("Segunda linea\\n")
buf.write("Tercera linea\\n")
contenido = buf.getvalue()
print("Escrito:", repr(contenido))

lector = io.StringIO(contenido)
for i, linea in enumerate(lector, 1):
    print(f"  Linea {i}: {linea.strip()}")`},

{name:'S05 · CSV en memoria', code:
`import io, csv

registros = [
    ["nombre", "edad", "ciudad"],
    ["Ana",    30,     "Madrid"],
    ["Luis",   25,     "Barcelona"],
    ["Maria",  35,     "Sevilla"]
]

buf = io.StringIO()
csv.writer(buf).writerows(registros)
csv_texto = buf.getvalue()
print("CSV generado:")
print(csv_texto)

lector = csv.DictReader(io.StringIO(csv_texto))
for fila in lector:
    print(f"  {fila['nombre']} ({fila['edad']}) - {fila['ciudad']}")`},

{name:'S07 · Tests con assert', code:
`def es_palindromo(texto):
    limpio = texto.lower().replace(" ", "")
    return limpio == limpio[::-1]

def suma_lista(nums):
    return sum(nums)

def maximo(lista):
    if not lista:
        raise ValueError("Lista vacia")
    return max(lista)

assert es_palindromo("Ana") == True
assert es_palindromo("oso") == True
assert es_palindromo("Python") == False
assert es_palindromo("Anita lava la tina") == True

assert suma_lista([1, 2, 3]) == 6
assert suma_lista([]) == 0
assert suma_lista([-1, 1]) == 0

assert maximo([3, 1, 4, 1, 5]) == 5

print("Todos los tests pasaron!")
print(f"palindromo 'Ana': {es_palindromo('Ana')}")
print(f"suma [1..5]: {suma_lista([1,2,3,4,5])}")`},

{name:'S10 · Correlaciones', code:
`import pandas as pd
import numpy as np

np.random.seed(42)
n = 50
df = pd.DataFrame({
    "altura": np.random.normal(170, 10, n),
    "edad":   np.random.randint(18, 60, n).astype(float),
    "puntos": np.random.normal(75, 15, n)
})
df["peso"] = df["altura"] * 0.4 + np.random.normal(0, 5, n)

print("Correlacion altura-peso:", round(df["altura"].corr(df["peso"]), 3))
print("Correlacion altura-edad:", round(df["altura"].corr(df["edad"]), 3))
print("Correlacion edad-puntos:", round(df["edad"].corr(df["puntos"]), 3))

corr = df.corr(numeric_only=True).round(3)
print("\\nMatriz de correlacion:")
print(corr)`},

{name:'S10 · Nulos y limpieza', code:
`import pandas as pd
import numpy as np

df = pd.DataFrame({
    "nombre": ["Ana", "Luis", None, "Carlos"],
    "edad":   [30, None, 35, 28],
    "puntos": [90.0, 75.0, np.nan, 92.0]
})

print("Nulos por columna:", df.isnull().sum().to_dict())
print("Total nulos:", df.isnull().sum().sum())

media_edad = df["edad"].mean()
df_limpio = df.fillna({
    "nombre": "Desconocido",
    "edad": round(media_edad, 1),
    "puntos": df["puntos"].median()
})
print("\\nDespues fillna:")
print(df_limpio.to_dict("records"))
print("Filas sin nulos:", len(df.dropna()), "de", len(df))`},

{name:'S10 · Pivot table', code:
`import pandas as pd

df = pd.DataFrame({
    "producto": ["A","B","A","B","A","B","A","B"],
    "region":   ["Norte","Norte","Sur","Sur","Este","Este","Norte","Sur"],
    "ventas":   [100, 200, 150, 80, 120, 300, 90, 110],
    "cantidad": [5, 8, 6, 3, 4, 12, 3, 5]
})

pivot = df.pivot_table(
    values="ventas",
    index="region",
    columns="producto",
    aggfunc="sum",
    fill_value=0
)
print("Pivot ventas (region x producto):")
print(pivot)
print("\\nTotal por region:", pivot.sum(axis=1).to_dict())
print("Total por producto:", pivot.sum(axis=0).to_dict())`},

{name:'S10 · Strings en Pandas', code:
`import pandas as pd

df = pd.DataFrame({
    "nombre":  ["  Ana Garcia  ", "LUIS RODRIGUEZ", "maria lopez", "Carlos M."],
    "email":   ["ana@gmail.com", "luis@hotmail.com", "maria@yahoo.es", "carlos@empresa.org"],
    "version": ["Python 3.10", "NumPy 1.24", "Pandas 2.0", "Flask 3.1"]
})

df["nombre_limpio"] = df["nombre"].str.strip().str.title()
df["dominio"] = df["email"].str.split("@").str[1]
df["es_gmail"] = df["email"].str.contains("gmail")
df["libreria"] = df["version"].str.extract(r"([A-Za-z]+)")
df["version_num"] = df["version"].str.extract(r"(\\d+\\.\\d+)")

print("Nombres limpios:", df["nombre_limpio"].tolist())
print("Dominios:", df["dominio"].tolist())
print("Es gmail:", df["es_gmail"].tolist())
print("Librerias:", df[["libreria","version_num"]].to_dict("records"))`},

{name:'S11 · Datos para graficos (NumPy)', code:
`import numpy as np

x = np.linspace(0, 2 * np.pi, 10)
y_sin = np.sin(x).round(3)
y_cos = np.cos(x).round(3)

print("x (10 puntos 0..2*pi):", x.round(2))
print("sin(x):", y_sin)
print("cos(x):", y_cos)

print(f"\\nsin(0)={np.sin(0):.1f}  sin(pi/2)={np.sin(np.pi/2):.1f}  sin(pi)={np.sin(np.pi):.4f}")

np.random.seed(42)
alturas = np.random.normal(170, 10, 100)
hist, edges = np.histogram(alturas, bins=5)
print("\\nHistograma alturas:")
for i, cnt in enumerate(hist):
    print(f"  {edges[i]:.0f}-{edges[i+1]:.0f}: {cnt} personas")`},

{name:'S13 · Generator expressions', code:
`import sys

# Mismos datos, diferente estructura en memoria
lista  = [x**2 for x in range(8)]
genexp = (x**2 for x in range(8))

print("Lista    :", lista)
print("Genexp tipo:", type(genexp).__name__)
print("Bytes lista:", sys.getsizeof(lista))
print("Bytes genexp:", sys.getsizeof(genexp))

# Encadenar genexps (evaluacion perezosa)
pares   = (x for x in range(20) if x % 2 == 0)
mayores = (x for x in pares if x > 10)
print("Pares > 10:", list(mayores))

suma = sum(x**2 for x in range(10))
print("Suma cuadrados 0-9:", suma)`},

{name:'S13 · Pipeline de generadores', code:
`def leer(datos):
    for item in datos:
        yield item

def filtrar(stream, umbral):
    for item in stream:
        if item > umbral:
            yield item

def transformar(stream, factor):
    for item in stream:
        yield item * factor

def acumular(stream):
    total = 0
    for item in stream:
        total += item
        yield total

datos = [1, 5, 3, 8, 2, 9, 4, 7, 6]
pipeline = list(acumular(transformar(filtrar(leer(datos), 4), 2)))
print("Datos:", datos)
print("Filtrar >4, x2, acumular:", pipeline)

total_pipeline = sum(transformar(filtrar(leer(datos), 4), 2))
print("Suma total del pipeline:", total_pipeline)`},

{name:'S14 · NLP sin NLTK', code:
`import string
from collections import Counter

texto = (
    "Python es un lenguaje de programacion versatil y potente. "
    "Python se usa en inteligencia artificial y ciencia de datos. "
    "El aprendizaje de Python abre muchas puertas en tecnologia moderna."
)

palabras = texto.lower().split()
palabras_limpias = [w.strip(string.punctuation) for w in palabras if w.strip(string.punctuation)]
print("Total palabras:", len(palabras_limpias))

stopwords = {"el", "la", "de", "en", "y", "se", "un", "es", "a", "que"}
utiles = [w for w in palabras_limpias if w not in stopwords]

frecuencia = Counter(utiles)
print("\\nMas frecuentes:")
for palabra, cnt in frecuencia.most_common(5):
    print(f"  '{palabra}': {cnt}")

bigramas = [(palabras_limpias[i], palabras_limpias[i+1])
            for i in range(len(palabras_limpias)-1)]
print("\\nBigramas mas comunes:")
for bg, cnt in Counter(bigramas).most_common(3):
    print(f"  '{bg[0]} {bg[1]}': {cnt}")`},

{name:'S15 · KNN desde cero (ML)', code:
`import math
from collections import Counter

def distancia(p1, p2):
    return math.sqrt(sum((a-b)**2 for a,b in zip(p1,p2)))

def knn_predecir(X_train, y_train, punto, k=3):
    dists = [(distancia(punto, x), y) for x, y in zip(X_train, y_train)]
    dists.sort(key=lambda t: t[0])
    k_vecinos = [y for _, y in dists[:k]]
    return Counter(k_vecinos).most_common(1)[0][0]

# 2 clases: grupo A (cerca de [1,1]) y B (cerca de [7,7])
X_train = [[1,1],[1.5,2],[2,1.5],[2.5,2],
           [7,7],[7.5,8],[8,7.5],[8.5,8]]
y_train = [  0,    0,     0,      0,
             1,    1,     1,      1]

X_test  = [[1.8, 1.9], [7.8, 7.5], [2.1, 2.2], [6.9, 7.1]]
y_real  = [0, 1, 0, 1]

print("Predicciones KNN (k=3):")
correctas = 0
for punto, real in zip(X_test, y_real):
    pred = knn_predecir(X_train, y_train, punto)
    ok = pred == real
    if ok: correctas += 1
    print(f"  {punto} -> pred={pred} real={real} {'OK' if ok else 'X'}")

print(f"Precision: {correctas}/{len(y_real)} = {correctas/len(X_test):.1%}")
print("(sklearn hace esto con: KNeighborsClassifier(n_neighbors=3).fit(X, y))")`},

{name:'S16 · Imagenes con NumPy', code:
`import numpy as np

img = np.zeros((10, 10), dtype=np.uint8)
img[2:8, 2:8] = 150
img[4:6, 4:6] = 255

print("Imagen (escala de grises 0-255):")
print(img)
print("Shape:", img.shape, "| Min:", img.min(), "Max:", img.max())
print("Media:", img.mean().round(2))

binaria = (img > 100).astype(np.uint8) * 255
print("\\nBinarizada (>100) fila 5:", binaria[5])

invertida = 255 - img
print("Invertida centro:", invertida[4:6, 4:6].tolist())

def blur3x3(imagen):
    r = np.zeros_like(imagen, dtype=float)
    for i in range(1, imagen.shape[0]-1):
        for j in range(1, imagen.shape[1]-1):
            r[i,j] = imagen[i-1:i+2, j-1:j+2].mean()
    return r.astype(np.uint8)

suave = blur3x3(img)
print("\\nBlur 3x3 fila 5:", suave[5])`},

/* ──── Práctica 1 (examen final) ──── */
{practica:1, name:'P1 · 01 FRange (iterativo)', code:
`# Practica 1 - Ejercicio 1: FRange
# Crear una lista de numeros desde 'init' hasta 'finish' con paso 'step', sin usar NumPy.
import math

def frange(init, finish, step):
    numeros = []
    while init <= finish or math.isclose(init, finish):
        numeros.append(round(init, 2))
        init += step
    return numeros

# Test Use Case
expected_output = [30, 30.4, 30.8, 31.2, 31.6, 32.0, 32.4, 32.8, 33.2, 33.6, 34.0, 34.4, 34.8, 35.2, 35.6, 36.0]
output = frange(30, 36, 0.4)

print("Esperado:", expected_output)
print("Obtenido:", output)
assert expected_output == output
print("OK: frange funciona correctamente")`},

{practica:1, name:'P1 · 01 FRange (con range)', code:
`# Practica 1 - Ejercicio 1 (variante): FRange calculando primero el numero de pasos
def frange(start, end, step):
    numero_de_pasos = int((end - start) / step) + 1
    salida = []
    for i in range(numero_de_pasos):
        salida.append(round(start + float(i) * step, 2))
    return salida

output = frange(30, 36, 0.4)
print("Obtenido:", output)
print("Cantidad de elementos:", len(output))`},

{practica:1, name:'P1 · 02 Ciudades en Florida', code:
`# Practica 1 - Ejercicio 2: contar ciudades distintas de Florida
# Version offline (dataset embebido) en vez de descargar el CSV real,
# para poder animar el algoritmo paso a paso sin depender de internet.
# Formato original: City|State short|State full|County|City alias
datos_csv = """Miami|FL|Florida|Miami-Dade|
Orlando|FL|Florida|Orange|
Tampa|FL|Florida|Hillsborough|
Miami|FL|Florida|Miami-Dade|Miami Beach
Jacksonville|FL|Florida|Duval|
Atlanta|GA|Georgia|Fulton|
Savannah|GA|Georgia|Chatham|
Naples|FL|Florida|Collier|
Sarasota|FL|Florida|Sarasota|
Houston|TX|Texas|Harris|"""

def cities_in_florida(data):
    ciudades = set()
    for linea in data.strip().splitlines():
        columnas = linea.split("|")
        if columnas[1] == "FL":
            ciudades.add(columnas[0])
    return len(ciudades)

total = cities_in_florida(datos_csv)
print("Ciudades distintas en Florida:", total)`},

{practica:1, name:'P1 · 03 RLE (iterativo)', code:
`# Practica 1 - Ejercicio 3: RLE (Run Length Encoding) iterativo
# 'dddddwwoooodddaaa' -> 'd5w2o4d3a3'
def rle(string):
    salida = string[0]
    resto = string[1:]
    contador = 1

    while resto:
        caracter = resto[0]
        if caracter == salida[-1]:
            contador += 1
        else:
            salida = salida + str(contador) + caracter
            contador = 1
        resto = resto[1:]

    salida += str(contador)
    return salida

# Test Use Case
cadena = 'dddddwwoooodddaaa'
esperado = 'd5w2o4d3a3'
resultado = rle(cadena)

print("Esperado:", esperado)
print("Obtenido:", resultado)
assert esperado == resultado
print("OK: rle funciona correctamente")`},

{practica:1, name:'P1 · 03 RLE (recursivo)', code:
`# Practica 1 - Ejercicio 3 (variante recursiva de RLE)
# Observa en Frames como se apila cada llamada recursiva
def rle(s):
    if not s:
        return ''
    contador = 1
    while contador < len(s) and s[contador] == s[0]:
        contador += 1
    comprimido = s[0] + str(contador)
    return comprimido + rle(s[contador:])

cadena = 'dddddwwoooodddaaa'
resultado = rle(cadena)
print("Obtenido:", resultado)
assert resultado == 'd5w2o4d3a3'
print("OK: version recursiva tambien funciona")`},

/* ──── Práctica 2 (examen final) ──── */
{practica:2, name:'P2 · 01 sort_by (generador)', code:
`import pandas as pd

# Practica 2 - Ejercicio 1: generador que devuelve las filas de un DataFrame
# ordenadas de mayor a menor segun 'column'
def sort_by(df, column):
    for _, fila in df.sort_values(by=column, ascending=False).iterrows():
        yield fila                          # yield = lo entrega fila a fila

# Dataset reducido (version corta de la practica real) para poder seguir la animacion
players = pd.DataFrame({
    "Name":   ["LeBron James", "Anthony Davis", "D'Angelo Russell", "Austin Reaves", "Jarred Vanderbilt", "Jaxson Hayes"],
    "Height": [2.06, 2.08, 1.93, 1.96, 2.03, 2.11],
    "Weight": [224, 198, 203, 235, 160, 212],
    "Points": [25, 48, 12, 29, 23, 51],
})

generador = sort_by(players, "Points")
orden_pesos = [int(fila["Weight"]) for fila in generador]

print("Points original:", list(players["Points"]))
print("Weights ordenados por Points (desc):", orden_pesos)`},

{practica:2, name:'P2 · 02 categorizar (np.where)', code:
`import pandas as pd
import numpy as np

# Practica 2 - Ejercicio 2: convertir columnas numericas en categorias
def categorizar(df):
    df = df.copy()                          # copia para no tocar el original
    df["Height"] = np.where(df["Height"] >= df["Height"].median(), "alto", "bajo")
    df["Weight"] = np.where(df["Weight"] >= 200, "pesado", "liviano")
    return df

players = pd.DataFrame({
    "Name":   ["LeBron James", "Anthony Davis", "D'Angelo Russell", "Austin Reaves", "Jarred Vanderbilt", "Jaxson Hayes"],
    "Height": [2.06, 2.08, 1.93, 1.96, 2.03, 2.11],
    "Weight": [224, 198, 203, 235, 160, 212],
    "Points": [25, 48, 12, 29, 23, 51],
})

categorizado = categorizar(players)
print(categorizado)`},

{practica:2, name:'P2 · 03 pivot_table', code:
`import pandas as pd

# Practica 2 - Ejercicio 3: tabla pivote con suma y media de Points
# segun cada combinacion de las categorias Height x Weight
def pivotar(df):
    return df.pivot_table(values="Points", index="Height", columns="Weight", aggfunc=["sum", "mean"])

players = pd.DataFrame({
    "Name":   ["LeBron James", "Anthony Davis", "D'Angelo Russell", "Austin Reaves", "Jarred Vanderbilt", "Jaxson Hayes"],
    "Height": ["alto", "alto", "bajo", "bajo", "alto", "alto"],
    "Weight": ["pesado", "liviano", "pesado", "pesado", "liviano", "pesado"],
    "Points": [25, 48, 12, 29, 23, 51],
})

tabla = pivotar(players)
print(tabla)`},

/* ──── Práctica 3 (examen final) ──── */
{practica:3, name:'P3 · 01 Pinguinos - Exploracion', code:
`import pandas as pd

# Practica 3 - Ejercicio 1: exploracion del dataset 'penguins' de seaborn
# Version offline: mini-muestra embebida (en vez de sns.load_dataset('penguins'),
# que descarga un CSV de internet) para poder trazar el analisis paso a paso
# sin depender de la red. Conserva nulos "tipicos" del dataset real: una fila
# totalmente vacia y algun sexo sin registrar.
df = pd.DataFrame({
    "species": ["Adelie","Adelie","Adelie","Adelie","Adelie","Adelie",
                "Chinstrap","Chinstrap","Chinstrap",
                "Gentoo","Gentoo","Gentoo","Gentoo","Gentoo","Gentoo"],
    "island": ["Torgersen","Torgersen","Biscoe","Biscoe","Dream","Dream",
               "Dream","Dream","Dream",
               "Biscoe","Biscoe","Biscoe","Biscoe","Biscoe","Biscoe"],
    "bill_length_mm": [39.1,39.5,37.8,40.6,39.5,None,46.5,50.0,51.3,46.1,50.0,48.7,50.0,45.2,47.3],
    "bill_depth_mm":  [18.7,17.4,18.3,18.6,16.7,None,17.9,19.5,19.2,13.2,16.3,14.1,15.2,None,13.8],
    "flipper_length_mm": [181,186,174,183,178,None,192,196,193,211,230,210,218,212,216],
    "body_mass_g": [3750,3800,3400,3550,3250,None,3500,3900,3650,4500,5700,4450,5700,5200,4725],
    "sex": ["Male","Female","Female","Male","Female",None,"Female","Male","Male","Female","Male","Female","Male","Female",None],
})
print(df.head())

# 1.2 Forma, tipos y resumen estadistico
print(df.shape)
print(df.dtypes)
print(df.describe())

# 1.3 Nulos por columna, de mayor a menor
nulos_por_columna = df.isnull().sum().sort_values(ascending=False)
print(nulos_por_columna)

# 1.4 Pinguinos por especie y por isla
print(df['species'].value_counts())
print(df['island'].value_counts())

# 1.5 pd.crosstab: combinaciones especie/isla
tabla_especie_isla = pd.crosstab(df['species'], df['island'])
print(tabla_especie_isla)
# No todas las especies aparecen en todas las islas: Adelie esta en las tres,
# Chinstrap solo en Dream y Gentoo solo en Biscoe -> la isla predice bastante
# bien la especie.`},

{practica:3, name:'P3 · 02 Pinguinos - NumPy', code:
`import pandas as pd
import numpy as np

# Practica 3 - Ejercicio 2: estadisticos con NumPy sobre el dataset de pinguinos
# (mismo mini-dataset embebido que en el ejercicio de exploracion)
df = pd.DataFrame({
    "species": ["Adelie","Adelie","Adelie","Adelie","Adelie","Adelie",
                "Chinstrap","Chinstrap","Chinstrap",
                "Gentoo","Gentoo","Gentoo","Gentoo","Gentoo","Gentoo"],
    "island": ["Torgersen","Torgersen","Biscoe","Biscoe","Dream","Dream",
               "Dream","Dream","Dream",
               "Biscoe","Biscoe","Biscoe","Biscoe","Biscoe","Biscoe"],
    "bill_length_mm": [39.1,39.5,37.8,40.6,39.5,None,46.5,50.0,51.3,46.1,50.0,48.7,50.0,45.2,47.3],
    "bill_depth_mm":  [18.7,17.4,18.3,18.6,16.7,None,17.9,19.5,19.2,13.2,16.3,14.1,15.2,None,13.8],
    "flipper_length_mm": [181,186,174,183,178,None,192,196,193,211,230,210,218,212,216],
    "body_mass_g": [3750,3800,3400,3550,3250,None,3500,3900,3650,4500,5700,4450,5700,5200,4725],
    "sex": ["Male","Female","Female","Male","Female",None,"Female","Male","Male","Female","Male","Female","Male","Female",None],
})

# 2.1 media, mediana, desviacion standard y rango de body_mass_g (sin nulos)
body_mass = df['body_mass_g'].dropna()
media = np.mean(body_mass)
mediana = np.median(body_mass)
desviacion_std = np.std(body_mass)
rango = np.max(body_mass) - np.min(body_mass)
print("media:", round(media, 2), "mediana:", mediana, "std:", round(desviacion_std, 2), "rango:", rango)

# 2.2 z-score de bill_length_mm (sin nulos), primeros 5 valores
bill_length = df['bill_length_mm'].dropna()
z_score = (bill_length - np.mean(bill_length)) / np.std(bill_length)
print("z-score bill_length (5 primeros):", z_score.round(3).tolist()[:5])

# 2.3 np.where: clasificar por encima/debajo de la media global
media_global = np.mean(body_mass)
clasificacion = np.where(body_mass > media_global, 'pesado', 'ligero')
valores, conteos = np.unique(clasificacion, return_counts=True)
print(dict(zip(valores, conteos)))`},

{practica:3, name:'P3 · 03 Pinguinos - Limpieza y nueva columna', code:
`import pandas as pd

# Practica 3 - Ejercicio 3: limpieza y nueva columna sobre el dataset de pinguinos
df = pd.DataFrame({
    "species": ["Adelie","Adelie","Adelie","Adelie","Adelie","Adelie",
                "Chinstrap","Chinstrap","Chinstrap",
                "Gentoo","Gentoo","Gentoo","Gentoo","Gentoo","Gentoo"],
    "island": ["Torgersen","Torgersen","Biscoe","Biscoe","Dream","Dream",
               "Dream","Dream","Dream",
               "Biscoe","Biscoe","Biscoe","Biscoe","Biscoe","Biscoe"],
    "bill_length_mm": [39.1,39.5,37.8,40.6,39.5,None,46.5,50.0,51.3,46.1,50.0,48.7,50.0,45.2,47.3],
    "bill_depth_mm":  [18.7,17.4,18.3,18.6,16.7,None,17.9,19.5,19.2,13.2,16.3,14.1,15.2,None,13.8],
    "flipper_length_mm": [181,186,174,183,178,None,192,196,193,211,230,210,218,212,216],
    "body_mass_g": [3750,3800,3400,3550,3250,None,3500,3900,3650,4500,5700,4450,5700,5200,4725],
    "sex": ["Male","Female","Female","Male","Female",None,"Female","Male","Male","Female","Male","Female","Male","Female",None],
})

# 3.1 copia df_clean sin filas con sexo nulo
df_clean = df.copy()
df_clean = df_clean.dropna(subset=['sex'])
print("Filas tras quitar sex nulo:", df_clean.shape)

# 3.2 rellenar nulos numericos con la mediana de cada especie (no la mediana global)
columnas_numericas = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
for columna in columnas_numericas:
    df_clean[columna] = df_clean[columna].fillna(df_clean.groupby('species')[columna].transform('median'))
print("Nulos restantes:", df_clean[columnas_numericas].isnull().sum().to_dict())

# 3.3 nueva columna bill_ratio = bill_length_mm / bill_depth_mm
df_clean['bill_ratio'] = df_clean['bill_length_mm'] / df_clean['bill_depth_mm']
print(df_clean[['bill_length_mm', 'bill_depth_mm', 'bill_ratio']].head().to_dict('records'))

# 3.4 Gentoo con body_mass_g > 5000g: cuantos y de que islas
gentoo_pesados = df_clean[(df_clean['species'] == 'Gentoo') & (df_clean['body_mass_g'] > 5000)]
print("Gentoo >5000g:", len(gentoo_pesados), "islas:", gentoo_pesados['island'].unique().tolist())`},

{practica:3, name:'P3 · 04 Titanic - Exploracion', code:
`import pandas as pd

# Practica 3 - Ejercicio 4: exploracion del dataset 'titanic' de seaborn
# Version offline: mini-muestra embebida (en vez de sns.load_dataset('titanic'),
# que descarga un CSV de internet) para poder trazar el analisis paso a paso
# sin depender de la red.
df = pd.DataFrame({
    "pclass":   [1,1,1,1, 2,2,2,2, 3,3,3,3,3,3,3],
    "sex":      ["female","male","female","male",
                 "female","male","female","male",
                 "female","male","female","male","female","male","female"],
    "age":      [38,54,40,None, 14,34,28,None, 4,22,27,2,None,32,19],
    "sibsp":    [1,0,0,0, 1,0,0,0, 1,0,0,3,0,0,0],
    "parch":    [0,0,0,0, 0,0,0,0, 1,0,2,1,0,0,0],
    "fare":     [133.65,51.86,27.72,26.55, 30.07,13.00,13.00,10.50, 16.70,7.25,11.13,21.08,7.75,8.05,7.88],
    "embarked": ["C","S","C","S", "C","S","S","S", "S","S","S","S","Q",None,"S"],
    "survived": [1,0,1,0, 1,0,1,0, 1,0,1,0,1,0,1],
})
df["class"] = df["pclass"].map({1: "First", 2: "Second", 3: "Third"})
df["embark_town"] = df["embarked"].map({"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"})
print(df.head())

# 1.2 Forma, tipos y resumen estadistico
print(df.shape)
print(df.dtypes)
print(df.describe())

# 1.3 Nulos por columna, de mayor a menor
nulos_por_columna = df.isnull().sum().sort_values(ascending=False)
print(nulos_por_columna)

# 1.4 Pasajeros por clase y por puerto de embarque
print(df['pclass'].value_counts())
print(df['embarked'].value_counts())

# 1.5 pd.crosstab: combinaciones clase/puerto
tabla_clase_puerto = pd.crosstab(df['class'], df['embark_town'])
print(tabla_clase_puerto)
# No todas las clases se reparten igual entre puertos: Southampton concentra
# la mayoria de la tercera clase, mientras que Cherbourg tiene mas peso
# relativo en primera clase -> el puerto de embarque tambien esta asociado
# a la clase del pasajero.`},

{practica:3, name:'P3 · 05 Titanic - NumPy', code:
`import pandas as pd
import numpy as np

# Practica 3 - Ejercicio 5: estadisticos con NumPy sobre el dataset de titanic
# (mismo mini-dataset embebido que en el ejercicio de exploracion)
df = pd.DataFrame({
    "pclass":   [1,1,1,1, 2,2,2,2, 3,3,3,3,3,3,3],
    "sex":      ["female","male","female","male",
                 "female","male","female","male",
                 "female","male","female","male","female","male","female"],
    "age":      [38,54,40,None, 14,34,28,None, 4,22,27,2,None,32,19],
    "sibsp":    [1,0,0,0, 1,0,0,0, 1,0,0,3,0,0,0],
    "parch":    [0,0,0,0, 0,0,0,0, 1,0,2,1,0,0,0],
    "fare":     [133.65,51.86,27.72,26.55, 30.07,13.00,13.00,10.50, 16.70,7.25,11.13,21.08,7.75,8.05,7.88],
    "embarked": ["C","S","C","S", "C","S","S","S", "S","S","S","S","Q",None,"S"],
    "survived": [1,0,1,0, 1,0,1,0, 1,0,1,0,1,0,1],
})

# 2.1 media, mediana, desviacion standard y rango de fare (sin nulos)
fare = df['fare'].dropna()
media = np.mean(fare)
mediana = np.median(fare)
desviacion_std = np.std(fare)
rango = np.max(fare) - np.min(fare)
print("media:", round(media, 2), "mediana:", mediana, "std:", round(desviacion_std, 2), "rango:", rango)

# 2.2 z-score de age (sin nulos), primeros 5 valores
age = df['age'].dropna()
z_score = (age - np.mean(age)) / np.std(age)
print("z-score age (5 primeros):", z_score.round(3).tolist()[:5])

# 2.3 np.where: clasificar por encima/debajo de la media global de fare
media_global = np.mean(fare)
clasificacion = np.where(fare > media_global, 'caro', 'economico')
valores, conteos = np.unique(clasificacion, return_counts=True)
print(dict(zip(valores, conteos)))`},

{practica:3, name:'P3 · 06 Titanic - Limpieza y nueva columna', code:
`import pandas as pd

# Practica 3 - Ejercicio 6: limpieza y nueva columna sobre el dataset de titanic
df = pd.DataFrame({
    "pclass":   [1,1,1,1, 2,2,2,2, 3,3,3,3,3,3,3],
    "sex":      ["female","male","female","male",
                 "female","male","female","male",
                 "female","male","female","male","female","male","female"],
    "age":      [38,54,40,None, 14,34,28,None, 4,22,27,2,None,32,19],
    "sibsp":    [1,0,0,0, 1,0,0,0, 1,0,0,3,0,0,0],
    "parch":    [0,0,0,0, 0,0,0,0, 1,0,2,1,0,0,0],
    "fare":     [133.65,51.86,27.72,26.55, 30.07,13.00,13.00,10.50, 16.70,7.25,11.13,21.08,7.75,8.05,7.88],
    "embarked": ["C","S","C","S", "C","S","S","S", "S","S","S","S","Q",None,"S"],
    "survived": [1,0,1,0, 1,0,1,0, 1,0,1,0,1,0,1],
})
df["class"] = df["pclass"].map({1: "First", 2: "Second", 3: "Third"})
df["embark_town"] = df["embarked"].map({"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"})

# 3.1 copia df_clean sin filas con puerto de embarque nulo
df_clean = df.copy()
df_clean = df_clean.dropna(subset=['embarked'])
print("Filas tras quitar embarked nulo:", df_clean.shape)

# 3.2 rellenar age con la mediana de cada clase (pclass), no la mediana global
df_clean['age'] = df_clean['age'].fillna(df_clean.groupby('pclass')['age'].transform('median'))
print("Nulos en age:", df_clean['age'].isnull().sum())

# 3.3 nueva columna family_size = sibsp + parch + 1
df_clean['family_size'] = df_clean['sibsp'] + df_clean['parch'] + 1
print(df_clean[['sibsp', 'parch', 'family_size']].head().to_dict('records'))

# 3.4 primera clase con fare > 100: cuantos y de que puerto
primera_caros = df_clean[(df_clean['pclass'] == 1) & (df_clean['fare'] > 100)]
print("Primera clase fare>100:", len(primera_caros), "puertos:", primera_caros['embark_town'].unique().tolist())`},
];


/* ──────────── Modo Maestro: temario guiado S00→S16→Práctica 1→Práctica 2→Práctica 3 ────────────
   A diferencia de un autoplay ciego, el ritmo lo marca el alumno: navega el ejemplo
   actual con los controles normales (Forward/Back/Loop) y solo avanza de tema cuando
   pulsa "Entendido, siguiente". El progreso se guarda en localStorage para retomar
   el repaso otro día justo donde se quedó. */
const MASTER_KEY='pyvizMasterProgress';
let _masterOn=false, _masterPos=0, _masterDone=new Set();
// Reto de código: caché por índice de tema — stub/prompt del backend,
// borrador del alumno, pistas.
let _masterChallenge={}, _masterDrafts={}, _masterHints={};
// Cuántas pistas de _masterHints[idx] ya se le mostraron al alumno para ese
// tema — permite revelarlas de a una (ver pistaReto()) sin perder el
// progreso si cierra y reabre el modal antes de aprobar el Reto.
let _masterHintsRevealed={};
let _cmEditor=null;
// Explicación con Claude Code (bajo demanda, ver explicarConClaude()): último
// error/línea que probarReto() detectó, línea resaltada en el editor, y un
// cache en memoria por (tema+línea+error+código) para no volver a llamar a
// Claude si el alumno pulsa el botón varias veces sin cambiar nada — eso es
// lo que ahorra tokens en los reintentos repetidos.
let _lastChallengeError=null, _lastChallengeErrorLine=null, _cmErrorLine=null;
const _aiExplainCache=new Map();

function _loadMasterProgress(){
  try{
    const raw=localStorage.getItem(MASTER_KEY);
    if(raw){ const d=JSON.parse(raw); _masterDone=new Set(d.done||[]); }
  }catch(e){ _masterDone=new Set(); }
}
function _saveMasterProgress(){
  try{ localStorage.setItem(MASTER_KEY, JSON.stringify({done:[..._masterDone]})); }catch(e){}
}
function _masterFirstPending(){
  for(let i=0;i<EX.length;i++) if(!_masterDone.has(i)) return i;
  return EX.length-1; // todo completado: se queda en el último tema
}
function toggleMasterMode(){
  if(_masterOn){ exitMasterMode(); return; }
  if(_aoOn) exitMasterAo(); // un solo temario guiado activo a la vez
  if(_mathOn) exitMasterMath();
  if(_raOn) exitMasterRa();
  if(_asOn) exitMasterAs();
  if(typeof _nsOn!=='undefined' && _nsOn) exitMasterNs();
  if(typeof _rnOn!=='undefined' && _rnOn) exitMasterRn();
  if(typeof _rfOn!=='undefined' && _rfOn) exitMasterRf();
  if(_reviewOn) exitReviewMode();
  if(typeof _calOn!=='undefined' && _calOn) _calClose();
  if(typeof _reportOn!=='undefined' && _reportOn) _reportClose();
  _masterOn=true;
  _loadMasterProgress();
  document.getElementById('masterBar').style.display='flex';
  const b=document.getElementById('bMaster');
  if(b){ b.textContent='🎓 Modo Maestro Py (activo)'; b.classList.add('btn-looping'); }
  autoLayout();
  _masterGoTo(_masterFirstPending());
}
function exitMasterMode(){
  _masterOn=false;
  document.getElementById('masterBar').style.display='none';
  document.getElementById('masterChecklist').style.display='none';
  const b=document.getElementById('bMaster');
  if(b){ b.textContent='🎓 Modo Maestro Py'; b.classList.remove('btn-looping'); }
  autoLayout();
}
function _masterGoTo(idx){
  _masterPos=Math.max(0, Math.min(EX.length-1, idx));
  document.getElementById('exSel').value=_masterPos;
  document.getElementById('codeInput').value=EX[_masterPos].code;
  renderLineNums();
  document.getElementById('frBody').innerHTML='<div class="ob-ph">No variables yet</div>';
  document.getElementById('obBody').innerHTML='<div class="ob-ph">Click [→] to inspect</div>';
  document.getElementById('outBody').innerHTML='<span class="out-empty">No output yet</span>';
  runCode();
  _masterRenderBar();
  _masterFetchChallenge(_masterPos);
  _masterCaptureAfterRun(_masterPos);
  _resetSelfExplain('py');
}
/* Colapsa y vacía el bloque de autoexplicación al cambiar de tema — igual que
   hace _mathGoTo(): la respuesta de un tema no debe arrastrarse al siguiente. */
function _resetSelfExplain(mode){
  const ids={py:['selfExplainPy','selfExplainTextPy'],
    ao:['selfExplainAo','selfExplainTextAo','selfExplainSavedAo'],
    ra:['selfExplainRa','selfExplainTextRa','selfExplainSavedRa'],
    as:['selfExplainAs','selfExplainTextAs','selfExplainSavedAs'],
    ns:['selfExplainNs','selfExplainTextNs','selfExplainSavedNs'],
    rn:['selfExplainRn','selfExplainTextRn','selfExplainSavedRn'],
    rf:['selfExplainRf','selfExplainTextRf','selfExplainSavedRf']};
  const tuple=ids[mode];
  if(!tuple) return;
  const el=document.getElementById(tuple[0]);
  const ta=document.getElementById(tuple[1]);
  if(el) el.style.display='none';
  if(ta) ta.value='';
  if(tuple[2]){
    const saved=document.getElementById(tuple[2]);
    if(saved){ saved.style.display='none'; saved.textContent=''; }
  }
  // Peldaño Transferencia (solo ao/ra/as, ver _transferSaveQuestion en
  // master-math.js): mismo criterio que el textarea de autoexplicación,
  // no debe arrastrar el problema inventado del tema anterior.
  const transferIds={ao:['transferTextAo','transferSavedAo'], ra:['transferTextRa','transferSavedRa'], as:['transferTextAs','transferSavedAs']}[mode];
  if(transferIds){
    const tTa=document.getElementById(transferIds[0]);
    const tSaved=document.getElementById(transferIds[1]);
    if(tTa) tTa.value='';
    if(tSaved){ tSaved.style.display='none'; tSaved.textContent=''; }
  }
}
/* Pide al backend el stub/prompt del Reto para este tema (análisis AST puro,
   no ejecuta nada) — se cachea por índice y solo repinta la barra si seguimos
   en ese mismo tema cuando responde. */
function _masterFetchChallenge(idx){
  fetch('/challenge',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({code:EX[idx].code})})
    .then(r=>r.json()).then(d=>{
      _masterChallenge[idx]=d;
      if(_masterPos===idx) _masterRenderBar();
    }).catch(()=>{ _masterChallenge[idx]={challengeable:false}; if(_masterPos===idx) _masterRenderBar(); });
}
/* Tras runCode(), espera a que lleguen los steps de ESTE tema para derivar
   una pista estructural del narrador. Se aborta si el alumno ya navegó a
   otro tema mientras tanto. */
function _masterCaptureAfterRun(idx){
  const check=()=>{
    if(_masterPos!==idx) return;
    if(steps && steps.length>1){
      _masterHints[idx]=_masterDeriveHint();
    } else {
      setTimeout(check,150);
    }
  };
  setTimeout(check,150);
}
/* Devuelve [{line, text}, ...] en orden de aparición en el código — una
   entrada por cada línea con análisis estructural del narrador (sin
   duplicar texto repetido). pistaReto() las revela de a una, ancladas a su
   línea de origen, en vez de mostrar todo el análisis de golpe. */
function _masterDeriveHint(){
  const skip=new Set(['print','import']);
  const seen=new Set(), items=[];
  Object.keys(explains).map(Number).sort((a,b)=>a-b).forEach(ln=>{
    const e=explains[ln];
    if(!e || skip.has(e.kind) || seen.has(e.text)) return;
    seen.add(e.text);
    items.push({line:ln, text:e.text});
  });
  return items;
}
/* Pinta el bloque #challengeHint y el botón #cBtnPista según cuántas pistas
   ya se revelaron para este tema (_masterHintsRevealed[idx]) — reusado por
   pistaReto() (al revelar una más) y por openChallenge() (al reabrir el
   modal, para no perder el progreso ya hecho). */
function _masterRenderHintBox(idx){
  const hints=_masterHints[idx];
  const shown=_masterHintsRevealed[idx]||0;
  const el=document.getElementById('challengeHint');
  const btn=document.getElementById('cBtnPista');
  if(!hints){
    el.style.display='none';
    btn.textContent='💡 Pista';
    btn.disabled=false;
    return;
  }
  if(shown>0){
    el.textContent=hints.slice(0,shown).map(h=>`Línea ${h.line}: ${h.text}`).join('\n');
    el.style.display='block';
  } else {
    el.style.display='none';
  }
  if(!hints.length){
    btn.textContent='💡 Sin pistas estructurales para este tema';
    btn.disabled=true;
  } else if(shown>=hints.length){
    btn.textContent=`💡 Ya viste todas las pistas (${hints.length}/${hints.length})`;
    btn.disabled=true;
  } else if(shown>0){
    btn.textContent=`💡 Otra pista (${shown}/${hints.length})`;
    btn.disabled=false;
  } else {
    btn.textContent='💡 Pista';
    btn.disabled=false;
  }
}
function _masterRenderBar(){
  const ex=EX[_masterPos];
  const pct=Math.round((_masterDone.size/EX.length)*100);
  document.getElementById('masterTitle').textContent=
    `🎓 Py · Tema ${_masterPos+1}/${EX.length} · ${ex.name}`;
  document.getElementById('masterFill').style.width=pct+'%';
  document.getElementById('masterPct').textContent=pct+'% del temario dominado';
  document.getElementById('mPrev').disabled=(_masterPos<=0);
  const ch=_masterChallenge[_masterPos];
  const nextBtn=document.getElementById('mNext');
  const atEnd=_masterPos>=EX.length-1;
  if(!ch){
    nextBtn.disabled=true;
    nextBtn.textContent='⏳ Preparando reto…';
  } else if(ch.challengeable){
    nextBtn.disabled=false;
    nextBtn.textContent=atEnd ? '✍️ Ponme a prueba (último tema)' : '✍️ Ponme a prueba';
  } else {
    nextBtn.disabled=false;
    nextBtn.textContent=atEnd ? '✅ Entendido, terminar' : '✅ Entendido, siguiente ▶';
  }
  if(document.getElementById('masterChecklist').style.display!=='none') _masterRenderChecklist();
}
function masterPrev(){ if(_masterPos>0) _masterGoTo(_masterPos-1); }
function masterRepeat(){ _masterGoTo(_masterPos); }
function _masterRestart(){ _masterGoTo(0); }
/* Botón "mNext": si el tema tiene Reto, lo abre en vez de avanzar directo — el
   avance real (marcar hecho + progresar) queda en _masterAdvance(), que solo
   se llama tras aprobar el Reto (o "Saltar", o si no hay Reto para este tema). */
function masterNext(){
  const ch=_masterChallenge[_masterPos];
  if(ch && ch.challengeable){ openChallenge(); }
  else { _masterAdvance(); }
}
function _masterAdvance(){
  _masterDone.add(_masterPos);
  _saveMasterProgress();
  closeChallenge();
  if(_masterPos>=EX.length-1){
    _masterRenderBar();
    setSt('🎉 ¡Completaste todo el temario S00–S16 + Práctica 1, 2 y 3! Estás listo para el parcial.');
    return;
  }
  _masterGoTo(_masterPos+1);
}
function _masterToggleChecklist(){
  const cl=document.getElementById('masterChecklist');
  const show=cl.style.display==='none';
  cl.style.display=show?'block':'none';
  if(show) _masterRenderChecklist();
}
function _masterRenderChecklist(){
  const cl=document.getElementById('masterChecklist');
  cl.innerHTML=EX.map((ex,i)=>{
    const done=_masterDone.has(i);
    const cur=i===_masterPos;
    return `<div class="master-item${done?' master-item-done':''}${cur?' master-item-current':''}" onclick="_masterGoTo(${i})">`+
      `<span class="master-item-chk">${done?'✓':(i+1)}</span><span class="master-item-name">${esc(ex.name)}</span>${_failsBadge('py',i)}</div>`;
  }).join('');
}
/* Si el usuario cambia el ejemplo a mano por el desplegable estando en Modo Maestro,
   mantener el panel sincronizado con esa posición en vez de desincronizarse. */
function _masterSyncFromDropdown(idx){
  if(!_masterOn) return;
  _masterPos=idx;
  _masterRenderBar();
  _masterFetchChallenge(idx);
  _masterCaptureAfterRun(idx);
}


/* ──────────── Reto de código: editor CodeMirror + evaluación ──────────── */
function _cmEnsure(){
  if(_cmEditor) return _cmEditor;
  _cmEditor=CodeMirror.fromTextArea(document.getElementById('challengeTextarea'), {
    mode:'python', theme:'material-darker', lineNumbers:true, indentUnit:4, tabSize:4,
    extraKeys:{
      'Ctrl-Space':'autocomplete',
      Tab:function(cm){
        if(cm.somethingSelected()) cm.indentSelection('add');
        else cm.replaceSelection('    ','end');
      }
    }
  });
  const PY_KEYWORDS=['False','None','True','and','as','assert','async','await','break','class',
    'continue','def','del','elif','else','except','finally','for','from','global','if','import',
    'in','is','lambda','nonlocal','not','or','pass','raise','return','try','while','with','yield',
    'print','len','range','str','int','float','list','dict','set','tuple','enumerate','zip','map',
    'filter','sorted','sum','min','max','abs','round','isinstance','super','self'];
  CodeMirror.registerHelper('hint','pyHint', function(cm){
    const anyword=CodeMirror.hint.anyword(cm, {word:/[\w]+/});
    const cur=cm.getCursor(), tok=cm.getTokenAt(cur);
    const start=/^\w+$/.test(tok.string) ? tok.start : cur.ch;
    const prefix=cm.getRange({line:cur.line,ch:start},cur).toLowerCase();
    const kw=prefix.length>0 ? PY_KEYWORDS.filter(k=>k.toLowerCase().startsWith(prefix)) : [];
    const seen=new Set(kw);
    const merged=kw.concat(((anyword&&anyword.list)||[]).filter(w=>!seen.has(w)));
    return {list:merged, from:CodeMirror.Pos(cur.line,start), to:cur};
  });
  // Autocompletado SOLO bajo demanda (Ctrl-Space), nunca automático en cada
  // tecla: show-hint.js vincula Enter/Tab a "aceptar sugerencia" mientras el
  // popup está abierto, así que auto-disparar el popup en cada letra hacía
  // que escribir código normal (Enter al final de cada línea, Tab para
  // indentar) reemplazara silenciosamente el texto por una sugerencia —
  // el código "se veía" igual al del ejemplo pero en realidad quedaba
  // corrompido, y el Reto lo rechazaba aunque pareciera idéntico.
  _cmEditor.setOption('hintOptions', {hint:CodeMirror.hint.pyHint, completeSingle:false});
  return _cmEditor;
}
function openChallenge(){
  const idx=_masterPos, ch=_masterChallenge[idx];
  if(!ch || !ch.challengeable){ _masterAdvance(); return; }
  document.getElementById('challengeTopic').textContent=EX[idx].name;
  document.getElementById('challengePrompt').textContent=ch.prompt;
  const st=document.getElementById('challengeStatus');
  st.className='challenge-status'; st.textContent='';
  document.getElementById('challengeDiff').style.display='none';
  _masterRenderHintBox(idx); // conserva las pistas ya reveladas de intentos anteriores
  document.getElementById('challengeSolution').style.display='none';
  document.getElementById('challengeActions').style.display='flex';
  document.getElementById('challengePassActions').style.display='none';
  document.getElementById('challengeModal').style.display='flex';
  const cm=_cmEnsure();
  cm.setValue(_masterDrafts[idx]!=null ? _masterDrafts[idx] : (ch.stub||''));
  setTimeout(()=>cm.refresh(),0); // CodeMirror mide mal si se inicializa oculto
  _resetAiExplain();
}
function closeChallenge(){
  if(_cmEditor) _masterDrafts[_masterPos]=_cmEditor.getValue();
  document.getElementById('challengeModal').style.display='none';
  _clearErrorLine();
}
/* Limpia el resaltado de la línea con error y esconde/deshabilita el bloque
   y botón de "Explícamelo con Claude" — se llama al abrir el Reto y cada vez
   que se vuelve a pulsar "Probar mi código" (el error anterior ya no aplica). */
function _resetAiExplain(){
  _lastChallengeError=null; _lastChallengeErrorLine=null;
  _clearErrorLine();
  const box=document.getElementById('challengeAI');
  if(box){ box.style.display='none'; box.textContent=''; }
  const btn=document.getElementById('cBtnExplain');
  if(btn){ btn.disabled=true; btn.textContent='🤖 Explícamelo'; }
}
function _clearErrorLine(){
  if(_cmErrorLine!=null && _cmEditor) _cmEditor.removeLineClass(_cmErrorLine-1,'background','cm-error-line');
  _cmErrorLine=null;
}
function _markErrorLine(line){
  _clearErrorLine();
  if(!line || !_cmEditor) return;
  _cmEditor.addLineClass(line-1,'background','cm-error-line');
  _cmEditor.scrollIntoView({line:Math.max(0,line-1),ch:0}, 80);
  _cmErrorLine=line;
}
/* Traduce el mensaje crudo de una excepción real de Python a una frase
   accionable en español, extrayendo el dato concreto que el propio mensaje
   ya trae (nombre de variable, clave, tipos...) — sin IA ni red: son reglas
   fijas por tipo de excepción, así que solo cubre los errores más comunes
   de un alumno. Si el tipo no está contemplado devuelve '' (no se muestra
   nada extra, se sigue viendo el mensaje crudo como antes). */
function _errorHint(errorText){
  const m = /^(\w+):\s*(.*)$/s.exec(errorText||'');
  if(!m) return '';
  const kind=m[1], msg=m[2];
  let mm;
  switch(kind){
    case 'NameError':
      mm=/name '(\w+)' is not defined/.exec(msg);
      return mm ? `Estás usando \`${mm[1]}\` pero no está definido antes de esta línea — ¿un typo, o te olvidaste de definirlo?` : '';
    case 'IndexError':
      mm=/(list|string|tuple) index out of range/.exec(msg);
      return mm ? `Estás accediendo a una posición de ${mm[1]==='list'?'una lista':mm[1]==='string'?'un texto':'una tupla'} que no existe — revisá los límites de tu bucle o el índice que usás.` : '';
    case 'KeyError':
      return `Estás buscando la clave ${msg} en un diccionario que no la tiene — revisá que esté bien escrita o que la hayas agregado antes.`;
    case 'ZeroDivisionError':
      return 'Estás dividiendo entre cero en algún punto — revisá el valor del divisor antes de esa operación.';
    case 'TypeError':
      if((mm=/unsupported operand type\(s\) for \S+: '(\w+)' and '(\w+)'/.exec(msg)))
        return `Estás combinando \`${mm[1]}\` y \`${mm[2]}\` en una operación que no lo permite — probablemente falta convertir uno de los dos con \`int(...)\`/\`str(...)\`.`;
      if((mm=/can only concatenate str \(not "(\w+)"\) to str/.exec(msg)))
        return `Estás uniendo un texto con algo de tipo \`${mm[1]}\` usando \`+\` — con \`+\` no se puede mezclar texto y números directamente, hace falta convertir ese valor con \`str(...)\`.`;
      if((mm=/'(\w+)' object is not subscriptable/.exec(msg)))
        return `Estás usando \`[...]\` sobre algo de tipo \`${mm[1]}\`, que no admite indexarse así.`;
      if((mm=/'(\w+)' object is not callable/.exec(msg)))
        return `Estás usando \`(...)\` sobre algo de tipo \`${mm[1]}\` como si fuera una función, pero no lo es — ¿le pusiste el mismo nombre a una variable y a una función?`;
      if((mm=/takes (\d+) positional argument.*but (\d+).*given/.exec(msg)))
        return `Estás llamando a una función con ${mm[2]} argumento(s), pero espera ${mm[1]} — revisá cuántos parámetros pide su definición.`;
      return '';
    case 'AttributeError':
      mm=/'(\w+)' object has no attribute '(\w+)'/.exec(msg);
      return mm ? `Estás usando \`.${mm[2]}\` sobre algo de tipo \`${mm[1]}\`, que no tiene ese método o atributo — revisá el tipo de dato o si escribiste bien el nombre.` : '';
    case 'ValueError':
      mm=/invalid literal for int\(\) with base 10: '([^']*)'/.exec(msg);
      return mm ? `Estás convirtiendo \`'${mm[1]}'\` a número con \`int(...)\`, pero no es un valor numérico válido.` : '';
    case 'AssertionError':
      return msg.trim() ? `El assert falló: ${msg.trim()}` : '';
    default:
      return '';
  }
}
function probarReto(){
  const idx=_masterPos;
  const code=_cmEnsure().getValue();
  _masterDrafts[idx]=code;
  const st=document.getElementById('challengeStatus');
  const diffBox=document.getElementById('challengeDiff');
  st.className='challenge-status'; st.textContent='⏳ Probando tu código…';
  diffBox.style.display='none';
  _resetAiExplain(); // el error del intento anterior (si había) ya no aplica
  fetch('/prepare',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({code})})
    .then(r=>r.json()).then(d=>{
      // Criterio del Reto: que el código corra sin errores (no se exige que
      // la salida coincida palabra por palabra con la referencia) — si
      // funciona, se pasa al siguiente tema.
      let pass=false, detail='', diff='';
      if(!d.steps || d.steps.length<=1){
        detail=d.error||'El código no produjo ningún paso ejecutable.';
      } else if(d.error){
        detail=d.error;
        diff=_errorHint(d.error);
      } else {
        pass=true;
      }
      _recordAttempt('py', idx, pass);
      if(pass){
        st.className='challenge-status ok';
        st.textContent='✅ ¡Correcto! Tu código funciona sin errores.';
        document.getElementById('challengeActions').style.display='none';
        document.getElementById('challengePassActions').style.display='flex';
      } else {
        st.className='challenge-status fail';
        st.textContent='❌ Aún no.'+(detail?(' '+detail):'');
        if(diff){ diffBox.textContent=diff; diffBox.style.display='block'; }
        // Guarda el error/línea para el botón "Explícamelo" (bajo demanda —
        // no se llama a Claude automáticamente, solo si el alumno lo pide).
        if(d.error){
          _lastChallengeError=d.error;
          _lastChallengeErrorLine=d.error_line||null;
          _markErrorLine(_lastChallengeErrorLine);
          const btn=document.getElementById('cBtnExplain');
          if(btn) btn.disabled=false;
        }
      }
    }).catch(e=>{ st.className='challenge-status fail'; st.textContent='❌ Error al probar: '+e.message; });
}
/* Bajo demanda (botón "🤖 Explícamelo"): le pide a Claude Code (headless,
   con la suscripción de la CLI — no una API key por token) que explique el
   último error de este intento. Cachea por (tema+línea+error+código) para
   no volver a llamar a Claude si el alumno pulsa varias veces sin cambiar
   nada — junto con el recorte a pocas líneas que hace el backend
   (ver _error_window en Python), es lo que mantiene el consumo bajo. */
function explicarConClaude(){
  if(!_lastChallengeError) return;
  const idx=_masterPos;
  const code=_cmEnsure().getValue();
  const key=idx+'|'+_lastChallengeErrorLine+'|'+_lastChallengeError+'|'+code;
  const box=document.getElementById('challengeAI');
  const btn=document.getElementById('cBtnExplain');
  box.style.display='block';
  if(_aiExplainCache.has(key)){
    box.textContent=_aiExplainCache.get(key)+'\n(respuesta en caché — mismo error, no se volvió a llamar a Claude)';
    return;
  }
  btn.disabled=true; btn.textContent='🤖 Preguntando a Claude…';
  box.textContent='⏳ Esperando la respuesta de Claude…';
  fetch('/explain_error',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({code, error:_lastChallengeError, error_line:_lastChallengeErrorLine})})
    .then(r=>r.json()).then(d=>{
      const text=(d && d.explanation) ? d.explanation : 'No se pudo obtener una explicación.';
      _aiExplainCache.set(key, text);
      box.textContent=text;
      btn.disabled=false; btn.textContent='🤖 Explícamelo';
    }).catch(e=>{
      box.textContent='❌ No se pudo conectar con Claude: '+e.message;
      btn.disabled=false; btn.textContent='🤖 Explícamelo';
    });
}
function pistaReto(){
  const idx=_masterPos;
  const hints=_masterHints[idx];
  if(!hints){
    const el=document.getElementById('challengeHint');
    el.textContent='Todavía no hay pistas listas — esperá un segundo e intentá de nuevo.';
    el.style.display='block';
    return;
  }
  const shown=_masterHintsRevealed[idx]||0;
  if(shown<hints.length) _masterHintsRevealed[idx]=shown+1;
  _masterRenderHintBox(idx);
}
function depurarIntento(){
  const idx=_masterPos;
  _masterDrafts[idx]=_cmEnsure().getValue();
  closeChallenge();
  document.getElementById('codeInput').value=_masterDrafts[idx];
  renderLineNums();
  document.getElementById('frBody').innerHTML='<div class="ob-ph">No variables yet</div>';
  document.getElementById('obBody').innerHTML='<div class="ob-ph">Click [→] to inspect</div>';
  document.getElementById('outBody').innerHTML='<span class="out-empty">No output yet</span>';
  runCode();
  setSt('🔍 Depurando tu intento del Reto — pulsa "✍️ Ponme a prueba" en la barra para volver.');
}
function saltarReto(){
  _recordAttempt('py', _masterPos, false);
  document.getElementById('challengeSolution').textContent=EX[_masterPos].code;
  document.getElementById('challengeSolution').style.display='block';
  document.getElementById('challengeActions').style.display='none';
  document.getElementById('challengePassActions').style.display='flex';
}

function isComplex(v){
  if(!v || typeof v!=='object') return false;
  return Array.isArray(v) || v.__set__ || v.__obj__ || v.__matrix__ || v.__series__ || v.__df__ ||
         Object.keys(v).length > 0;
}

/* How "worth watching" a variable is, for auto-picking the Objects panel's
   default — a static dict (e.g. read-only input data like `bitmasks`) is
   far less useful to land on by default than the list/partition an
   algorithm is actually mutating, even if the dict appears earlier in the
   source. Higher score wins; on a tie the LAST-seen wins (see the >= in
   autoPickObj), which in practice means the innermost frame, since
   step.frames goes outermost-first. */
function _animInterest(v){
  if(Array.isArray(v)){
    if(v.length===0) return 0;
    if(v.every(x=>Array.isArray(x))) return 5;                    // groups/bins — most specific
    if(v.every(x=>typeof x==='number'&&isFinite(x))) return 4;    // sortable bars
    const shape=_listShape(v);
    if(shape && shape.length>=2) return 3;                        // regular N-dim grid
    return 2;                                                     // plain list
  }
  if(v && typeof v==='object'){
    if(v.__matrix__) return 3;
    return 1;                                                     // dict/set/obj/series/df
  }
  return 0;
}

let _lastObjName=null;
// Whether the current selVar was chosen by autoPickObj's own heuristic
// (re-evaluated every step, so a more interesting variable created later
// — e.g. a partition an algorithm starts mutating — can take over from a
// static one picked earlier, like a read-only input dict) vs a deliberate
// click on "🔍 ver" (which always sticks, see pickObj).
let _autoSelected=false;

function autoPickObj(step){
  // A variable the user explicitly picked always keeps showing.
  if(selVar && !_autoSelected){
    for(const fr of step.frames){
      if(selVar in fr.variables){
        renderObjects(selVar, fr.variables[selVar]);
        _flashObjPanel(selVar);
        return;
      }
    }
    selVar=null;
  }
  // Otherwise re-evaluate every step: pick the most "animation-worthy"
  // complex variable currently in scope. Re-scoring each time (instead of
  // locking onto whatever was auto-picked first) is what lets e.g. a
  // partition/list an algorithm starts building later in the run take
  // over from a static input variable defined earlier in the source.
  // step.frames goes OUTERMOST-first (sandbox.py's stack() inserts each
  // caller at the front as it walks f_back), so on a tied score ">=" (not
  // ">") is what lets a function-local list win over an outer one with the
  // same score — e.g. insercion_sort's local `lista` (the one actually
  // being sorted) over the untouched top-level `ejemplo` it was copied
  // from, which otherwise "wins" the tie just by being seen first and the
  // panel looks frozen/unsorted for the whole call even though the real
  // sorting is happening one frame in.
  let best=null, bestScore=-1;
  for(const fr of step.frames){
    for(const [k,v] of Object.entries(fr.variables)){
      if(!isComplex(v)) continue;
      const sc=_animInterest(v);
      if(sc>=bestScore){ bestScore=sc; best=[k,v]; }
    }
  }
  if(best){
    const [k,v]=best;
    const isNew = k !== _lastObjName;
    selVar=k; _lastObjName=k; _autoSelected=true;
    renderObjects(k,v);
    _flashObjPanel(k, isNew);
    return;
  }
  // No complex variable — show iteration state if simple vars present
  selVar=null; _autoSelected=false; _lastObjName=null;
  const pt=document.querySelector('.ptitle-ob');
  if(pt){ pt.textContent='Objects'; pt.style.color=''; }
  _showIterState(step);
}

function _showIterState(step){
  const el=document.getElementById('obBody');
  // Collect all simple vars across frames
  const simpleVars=[];
  for(const fr of step.frames)
    for(const [k,v] of Object.entries(fr.variables))
      if(!isComplex(v) && v!==null) simpleVars.push([k,v]);

  if(!simpleVars.length){
    el.innerHTML='<div class="ob-ph" style="color:#333;text-align:center;padding-top:20px">— sin variables —</div>';
    return;
  }
  // Detect iteration: if there are simple vars, show them as "active values"
  const line=step.line;
  let h=`<div class="ob-hdr"><span class="ob-hdr-type" style="background:#1a2a1a;color:#6a9;font-size:10px">iter</span>
    <span class="ob-hdr-name" style="color:#888;font-size:11px">Línea ${line} — variables simples</span></div>`;
  h+=`<div style="padding:6px 8px">`;
  simpleVars.forEach(([k,v],i)=>{
    const {t,cls,d}=obTypeInfo(v);
    const bar = (typeof v==='number'&&v>=0&&v<=200) ?
      `<div class="nbar" style="margin:2px 0 4px"><div class="nbar-f" style="width:${Math.min(v,100)}%;opacity:.6"></div></div>` : '';
    h+=`<div style="display:flex;align-items:center;gap:6px;padding:3px 0;border-bottom:1px solid #1a1a2a;animation:ob-pop .18s ease-out both;animation-delay:${i*35}ms">
      <span style="color:#555;font-family:monospace;font-size:10px;min-width:16px">${i}</span>
      <span style="font-family:monospace;font-size:12px;color:#999;min-width:60px">${esc(k)}</span>
      <span class="ob-td-val ${cls}" style="font-family:monospace;font-size:13px;font-weight:700">${d}</span>
      <span style="font-size:9px;color:#444;margin-left:auto">${t}</span>
    </div>${bar}`;
  });
  h+=`</div>`;
  el.innerHTML=h;
  autoLayout();
}


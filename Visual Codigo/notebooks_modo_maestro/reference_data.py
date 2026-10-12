"""Contenido de los notebooks de referencia extra (Python stdlib, NumPy,
Pandas, Matplotlib, Seaborn) que complementan a las sesiones del Modo
Maestro. A diferencia de sessions.json, este contenido no se extrae de
python_visualizer_flask.py: esta escrito a mano aqui, organizado por
libreria y por seccion, y generate_reference_notebooks.py lo procesa con
el mismo explicador de code_walkthrough.py que usan las sesiones, para que
ambos tipos de notebook se lean igual.

Cada Library tiene una URL a la documentacion oficial correspondiente:
  - Python stdlib -> https://docs.python.org/3/
  - NumPy         -> https://numpy.org/
  - Pandas        -> https://pandas.pydata.org/
  - Matplotlib    -> https://matplotlib.org/
  - Seaborn       -> https://seaborn.pydata.org/
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Section:
    title: str
    intro: str
    code: str


@dataclass
class Library:
    key: str
    title: str
    url: str
    intro: str
    sections: list[Section]


PYTHON_STDLIB = Library(
    key="python_stdlib",
    title="Python — biblioteca estandar",
    url="https://docs.python.org/3/",
    intro=(
        "Complementa las sesiones S00-S09 del Modo Maestro con partes de la "
        "biblioteca estandar de Python que no salen ahi: mas metodos de "
        "listas/tuplas/dicts, y modulos de uso diario como `itertools`, "
        "`functools`, `re`, `datetime`, `pathlib`, `json`, `dataclasses`, "
        "`contextlib` y `typing`."
    ),
    sections=[
        Section(
            "Strings avanzado",
            "Metodos de formateo y limpieza de texto que no aparecen en S00.",
            'texto = "  Python es Genial  "\n'
            "print(texto.strip())\n"
            'print(texto.strip().ljust(20, "."))\n'
            'print(texto.strip().rjust(20, "."))\n'
            'print("7".zfill(3))\n'
            'print("a,b,,c".split(","))\n'
            'print("clave=valor".partition("="))\n'
            'nombre, edad = "Ana", 30\n'
            'print(f"{nombre} tiene {edad} anios, o sea {edad * 12} meses")\n'
            'print("{} tiene {} anios".format(nombre, edad))\n'
            'print("Texto\\ncon\\nvarias\\nlineas".splitlines())',
        ),
        Section(
            "Listas y tuplas: metodos completos",
            "insert/remove/count/index/sort(key=)/reverse y unpacking extendido con *.",
            "numeros = [5, 3, 8, 1, 9, 3]\n"
            "numeros.insert(0, 100)\n"
            "print(numeros)\n"
            "numeros.remove(3)\n"
            "print(numeros)\n"
            "print(numeros.count(3))\n"
            "print(numeros.index(8))\n"
            "numeros.sort(key=lambda x: -x)\n"
            "print(numeros)\n"
            "numeros.reverse()\n"
            "print(numeros)\n\n"
            "primero, *resto, ultimo = [1, 2, 3, 4, 5]\n"
            "print(primero, resto, ultimo)\n\n"
            "punto = (3, 4)\n"
            "x, y = punto\n"
            'print(f"x={x} y={y}")',
        ),
        Section(
            "Diccionarios avanzados",
            "Union de diccionarios con `|`, comprehensions y `defaultdict`.",
            'base = {"a": 1, "b": 2}\n'
            'extra = {"b": 20, "c": 3}\n'
            "combinado = base | extra\n"
            "print(combinado)\n\n"
            "cuadrados = {n: n**2 for n in range(6) if n % 2 == 0}\n"
            "print(cuadrados)\n\n"
            "from collections import defaultdict\n"
            "conteo = defaultdict(int)\n"
            'for letra in "abracadabra":\n'
            "    conteo[letra] += 1\n"
            "print(dict(conteo))",
        ),
        Section(
            "itertools: combinar iterables",
            "chain, product, permutations, combinations y cycle+islice.",
            "import itertools\n\n"
            "print(list(itertools.chain([1, 2], [3, 4], [5])))\n"
            'print(list(itertools.product([1, 2], ["a", "b"])))\n'
            "print(list(itertools.permutations([1, 2, 3], 2)))\n"
            "print(list(itertools.combinations([1, 2, 3], 2)))\n\n"
            "repetido = itertools.islice(itertools.cycle([1, 2, 3]), 7)\n"
            "print(list(repetido))",
        ),
        Section(
            "functools: reduce, partial, lru_cache",
            "Programacion funcional y memoizacion sin escribir cache a mano.",
            "from functools import reduce, partial, lru_cache\n\n"
            "producto = reduce(lambda a, b: a * b, [1, 2, 3, 4])\n"
            'print("Producto:", producto)\n\n'
            "def potencia(base, exponente):\n"
            "    return base ** exponente\n\n"
            "cuadrado = partial(potencia, exponente=2)\n"
            'print("Cuadrado de 9:", cuadrado(9))\n\n'
            "@lru_cache(maxsize=None)\n"
            "def fib(n):\n"
            "    if n < 2:\n"
            "        return n\n"
            "    return fib(n - 1) + fib(n - 2)\n\n"
            'print("Fibonacci(20):", fib(20))',
        ),
        Section(
            "re: expresiones regulares basicas",
            "Buscar patrones, capturar grupos y reemplazar texto.",
            "import re\n\n"
            'texto = "Contacto: ana@mail.com, tel 555-1234, luis@empresa.org"\n\n'
            'emails = re.findall(r"[\\w.]+@[\\w.]+", texto)\n'
            'print("Emails:", emails)\n\n'
            'm = re.search(r"tel (\\d{3}-\\d{4})", texto)\n'
            'print("Telefono:", m.group(1) if m else None)\n\n'
            'limpio = re.sub(r"\\d", "#", texto)\n'
            'print("Numeros ocultos:", limpio)',
        ),
        Section(
            "datetime: fechas y duraciones",
            "Crear, formatear y restar fechas con `strftime`/`strptime`/`timedelta`.",
            "from datetime import datetime, timedelta\n\n"
            "ahora = datetime(2026, 7, 30, 14, 30)\n"
            'print(ahora.strftime("%d/%m/%Y %H:%M"))\n\n'
            "en_una_semana = ahora + timedelta(days=7)\n"
            'print(en_una_semana.strftime("%d/%m/%Y"))\n\n'
            'texto_fecha = "2026-12-25"\n'
            'navidad = datetime.strptime(texto_fecha, "%Y-%m-%d")\n'
            "dias_restantes = (navidad - ahora).days\n"
            'print(f"Faltan {dias_restantes} dias para Navidad")',
        ),
        Section(
            "pathlib: rutas de archivos",
            "Construir y descomponer rutas sin concatenar strings a mano.",
            "from pathlib import Path\n\n"
            'carpeta = Path("proyecto") / "datos" / "entrada.csv"\n'
            "print(carpeta)\n"
            'print("Nombre:", carpeta.name)\n'
            'print("Extension:", carpeta.suffix)\n'
            'print("Carpeta padre:", carpeta.parent)\n'
            'print("Sin extension:", carpeta.stem)',
        ),
        Section(
            "json: serializar y leer datos",
            "Convertir estructuras de Python a texto JSON y de vuelta.",
            "import json\n\n"
            'persona = {"nombre": "Ana", "edad": 30, "activo": True, "notas": [8.5, 9, 7.5]}\n'
            "texto_json = json.dumps(persona, indent=2, ensure_ascii=False)\n"
            "print(texto_json)\n\n"
            "de_vuelta = json.loads(texto_json)\n"
            'print(de_vuelta["notas"])',
        ),
        Section(
            "dataclasses: clases de datos sin boilerplate",
            "`@dataclass` genera `__init__`, `__repr__` y `__eq__` automaticamente.",
            "from dataclasses import dataclass\n\n"
            "@dataclass\n"
            "class Punto:\n"
            "    x: float\n"
            "    y: float\n"
            '    etiqueta: str = "sin nombre"\n\n'
            "    def distancia_origen(self) -> float:\n"
            "        return (self.x ** 2 + self.y ** 2) ** 0.5\n\n"
            "p = Punto(3, 4)\n"
            "print(p)\n"
            "print(p.distancia_origen())\n"
            "print(p == Punto(3, 4))",
        ),
        Section(
            "context managers: with y contextlib",
            "Como funciona `with` por dentro, usando `@contextmanager`.",
            "from contextlib import contextmanager\n"
            "import time\n\n"
            "@contextmanager\n"
            "def cronometro(nombre):\n"
            "    inicio = time.perf_counter()\n"
            '    print(f"Iniciando {nombre}...")\n'
            "    yield\n"
            "    duracion = time.perf_counter() - inicio\n"
            '    print(f"{nombre} tomo {duracion:.4f}s")\n\n'
            'with cronometro("suma"):\n'
            "    total = sum(range(1_000_000))\n\n"
            'print("Total:", total)',
        ),
        Section(
            "typing: anotaciones de tipos",
            "Documentar (y dejar que herramientas como mypy verifiquen) los tipos esperados.",
            "from typing import Optional, Union\n\n"
            "def buscar_usuario(id_usuario: int, base: dict[int, str]) -> Optional[str]:\n"
            "    return base.get(id_usuario)\n\n"
            "def normalizar(valor: Union[int, float, str]) -> float:\n"
            "    return float(valor)\n\n"
            'usuarios = {1: "Ana", 2: "Luis"}\n'
            "print(buscar_usuario(1, usuarios))\n"
            "print(buscar_usuario(99, usuarios))\n"
            'print(normalizar("3.5"), normalizar(10))',
        ),
    ],
)


NUMPY = Library(
    key="numpy",
    title="NumPy",
    url="https://numpy.org/",
    intro=(
        "Complementa la sesion S10 del Modo Maestro con mas operaciones de "
        "arrays: creacion, dtypes, indexado avanzado, reshape, broadcasting, "
        "rendimiento vectorizado, agregaciones por eje, algebra lineal, "
        "ordenar/buscar y numeros aleatorios reproducibles."
    ),
    sections=[
        Section(
            "Creacion de arrays",
            "Las formas mas comunes de construir un ndarray desde cero.",
            "import numpy as np\n\n"
            "a = np.array([1, 2, 3, 4, 5])\n"
            "b = np.zeros((2, 3))\n"
            "c = np.ones((3,))\n"
            "d = np.full((2, 2), 7)\n"
            "e = np.arange(0, 10, 2)\n"
            "f = np.linspace(0, 1, 5)\n"
            "g = np.eye(3)\n\n"
            'print("array:", a)\n'
            'print("zeros:\\n", b)\n'
            'print("full:\\n", d)\n'
            'print("arange:", e)\n'
            'print("linspace:", f)',
        ),
        Section(
            "dtype y casting",
            "Todo ndarray tiene un tipo de dato unico; convertirlo cambia memoria y precision.",
            "import numpy as np\n\n"
            "enteros = np.array([1, 2, 3])\n"
            "print(enteros.dtype)\n\n"
            "flotantes = enteros.astype(np.float64)\n"
            "print(flotantes.dtype, flotantes)\n\n"
            "mixto = np.array([1, 2.5, 3])\n"
            "print(mixto.dtype)\n\n"
            "booleanos = np.array([0, 1, 2, 0]).astype(bool)\n"
            "print(booleanos)",
        ),
        Section(
            "Indexado, slicing y mascaras booleanas",
            "Acceder a sub-arrays y filtrar por condicion sin bucles.",
            "import numpy as np\n\n"
            "m = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])\n"
            "print(m[1, 2])\n"
            "print(m[:, 0])\n"
            "print(m[0:2, 1:])\n\n"
            "mascara = m > 40\n"
            "print(mascara)\n"
            "print(m[mascara])\n\n"
            "indices = [0, 2]\n"
            "print(m[indices])",
        ),
        Section(
            "Reshape y combinar arrays",
            "Cambiar la forma de un array y apilar varios en uno solo.",
            "import numpy as np\n\n"
            "a = np.arange(12)\n"
            "matriz = a.reshape(3, 4)\n"
            "print(matriz)\n"
            "print(matriz.ravel())\n\n"
            "x = np.array([1, 2, 3])\n"
            "y = np.array([4, 5, 6])\n"
            "print(np.vstack([x, y]))\n"
            "print(np.hstack([x, y]))\n"
            "print(np.concatenate([x, y]))",
        ),
        Section(
            "Broadcasting",
            "NumPy expande automaticamente arrays de forma compatible para operar sin bucles.",
            "import numpy as np\n\n"
            "matriz = np.array([[1, 2, 3], [4, 5, 6]])\n"
            "vector = np.array([10, 20, 30])\n"
            "print(matriz + vector)\n\n"
            "columna = np.array([[1], [2]])\n"
            "print(matriz + columna)\n\n"
            "print(matriz * 2)",
        ),
        Section(
            "Operaciones vectorizadas vs bucles Python",
            "Por que se prefiere `array * 2` a un `for` — mismo resultado, mucho mas rapido.",
            "import numpy as np\n"
            "import time\n\n"
            "n = 200_000\n"
            "datos = np.arange(n)\n\n"
            "inicio = time.perf_counter()\n"
            "resultado_vectorizado = datos * 2 + 1\n"
            "tiempo_vector = time.perf_counter() - inicio\n\n"
            "inicio = time.perf_counter()\n"
            "resultado_bucle = [x * 2 + 1 for x in range(n)]\n"
            "tiempo_bucle = time.perf_counter() - inicio\n\n"
            'print(f"Vectorizado: {tiempo_vector:.5f}s")\n'
            'print(f"Bucle Python: {tiempo_bucle:.5f}s")\n'
            'print("Mismo resultado:", list(resultado_vectorizado[:5]) == resultado_bucle[:5])',
        ),
        Section(
            "Agregaciones y ejes",
            "sum/mean/max con `axis=0` (por columna) o `axis=1` (por fila).",
            "import numpy as np\n\n"
            "datos = np.array([[4, 2, 7], [1, 8, 3], [6, 5, 0]])\n"
            'print("Suma total:", datos.sum())\n'
            'print("Suma por columna (axis=0):", datos.sum(axis=0))\n'
            'print("Suma por fila (axis=1):", datos.sum(axis=1))\n'
            'print("Media:", datos.mean())\n'
            'print("Maximo:", datos.max(), "en la posicion", datos.argmax())',
        ),
        Section(
            "Algebra lineal",
            "Resolver sistemas de ecuaciones y operar con matrices.",
            "import numpy as np\n\n"
            "A = np.array([[2, 1], [1, 3]])\n"
            "b = np.array([5, 10])\n\n"
            "x = np.linalg.solve(A, b)\n"
            'print("Solucion:", x)\n'
            'print("Verificacion A@x:", A @ x)\n'
            'print("Transpuesta:\\n", A.T)\n'
            'print("Inversa:\\n", np.linalg.inv(A))\n'
            'print("Determinante:", np.linalg.det(A))',
        ),
        Section(
            "Ordenar y buscar",
            "sort, argsort, unique y where — sin escribir el algoritmo a mano.",
            "import numpy as np\n\n"
            "datos = np.array([5, 2, 9, 1, 5, 6])\n"
            'print("Ordenado:", np.sort(datos))\n'
            'print("Indices que ordenan:", np.argsort(datos))\n'
            'print("Unicos:", np.unique(datos))\n'
            'print("Donde es > 4:", np.where(datos > 4))\n'
            'print("Reemplazo condicional:", np.where(datos > 4, datos, 0))',
        ),
        Section(
            "Numeros aleatorios reproducibles",
            "`default_rng(seed)` — la forma moderna de generar aleatoriedad reproducible.",
            "import numpy as np\n\n"
            "rng = np.random.default_rng(seed=42)\n"
            'print("Enteros:", rng.integers(1, 100, size=5))\n'
            'print("Normal:", rng.normal(loc=0, scale=1, size=5).round(3))\n'
            'print("Eleccion:", rng.choice(["a", "b", "c", "d"], size=3))',
        ),
    ],
)


PANDAS = Library(
    key="pandas",
    title="Pandas",
    url="https://pandas.pydata.org/",
    intro=(
        "Complementa la sesion S11 del Modo Maestro: seleccion con loc/iloc, "
        "ordenar y rankear, groupby con multiples agregaciones, merge/concat, "
        "pivot_table/crosstab, datos faltantes, apply/map/.str, fechas, "
        "CSV en memoria y estadisticas descriptivas."
    ),
    sections=[
        Section(
            "Series y DataFrame: creacion",
            "Las dos estructuras base de Pandas: columna (Series) y tabla (DataFrame).",
            "import pandas as pd\n\n"
            'serie = pd.Series([10, 20, 30], index=["a", "b", "c"], name="valores")\n'
            "print(serie)\n\n"
            "df = pd.DataFrame({\n"
            '    "producto": ["Laptop", "Mouse", "Teclado", "Monitor"],\n'
            '    "precio": [1200, 25, 80, 300],\n'
            '    "stock": [5, 50, 30, 12],\n'
            "})\n"
            "print(df)\n"
            "print(df.dtypes)",
        ),
        Section(
            "Seleccion: loc, iloc y filtrado booleano",
            "loc selecciona por etiqueta, iloc por posicion; los boolean masks filtran filas.",
            "import pandas as pd\n\n"
            "df = pd.DataFrame({\n"
            '    "producto": ["Laptop", "Mouse", "Teclado", "Monitor"],\n'
            '    "precio": [1200, 25, 80, 300],\n'
            '    "stock": [5, 50, 30, 12],\n'
            "})\n\n"
            'print(df.loc[0, "producto"])\n'
            "print(df.iloc[1:3])\n"
            'print(df[df["precio"] > 100])\n'
            'print(df.loc[df["stock"] < 20, ["producto", "stock"]])',
        ),
        Section(
            "Ordenar y rankear",
            "sort_values ordena filas; rank asigna una posicion relativa a cada valor.",
            "import pandas as pd\n\n"
            "df = pd.DataFrame({\n"
            '    "producto": ["Laptop", "Mouse", "Teclado", "Monitor"],\n'
            '    "precio": [1200, 25, 80, 300],\n'
            "})\n\n"
            'print(df.sort_values("precio", ascending=False))\n'
            'print(df.sort_values("precio").reset_index(drop=True))\n'
            'df["ranking"] = df["precio"].rank(ascending=False).astype(int)\n'
            "print(df)",
        ),
        Section(
            "groupby y agregaciones multiples",
            "Agrupar filas por una o varias columnas y resumirlas con `.agg([...])`.",
            "import pandas as pd\n\n"
            "ventas = pd.DataFrame({\n"
            '    "region": ["Norte", "Sur", "Norte", "Sur", "Norte"],\n'
            '    "producto": ["A", "A", "B", "B", "A"],\n'
            '    "monto": [100, 150, 200, 90, 120],\n'
            "})\n\n"
            'por_region = ventas.groupby("region")["monto"].agg(["sum", "mean", "count"])\n'
            "print(por_region)\n\n"
            'por_ambos = ventas.groupby(["region", "producto"])["monto"].sum()\n'
            "print(por_ambos)",
        ),
        Section(
            "merge, join y concat",
            "Combinar tablas: merge cruza por clave (como un JOIN de SQL), concat apila filas.",
            "import pandas as pd\n\n"
            'clientes = pd.DataFrame({"id": [1, 2, 3], "nombre": ["Ana", "Luis", "Eva"]})\n'
            'pedidos = pd.DataFrame({"cliente_id": [1, 1, 2], "monto": [100, 50, 200]})\n\n'
            'combinado = clientes.merge(pedidos, left_on="id", right_on="cliente_id", how="left")\n'
            "print(combinado)\n\n"
            'extra = pd.DataFrame({"id": [4], "nombre": ["Marcos"]})\n'
            "todos = pd.concat([clientes, extra], ignore_index=True)\n"
            "print(todos)",
        ),
        Section(
            "pivot_table y crosstab",
            "Tablas resumen cruzando dos categorias, con una funcion de agregacion.",
            "import pandas as pd\n\n"
            "ventas = pd.DataFrame({\n"
            '    "region": ["Norte", "Sur", "Norte", "Sur"],\n'
            '    "producto": ["A", "A", "B", "B"],\n'
            '    "monto": [100, 150, 200, 90],\n'
            "})\n\n"
            'pivote = ventas.pivot_table(values="monto", index="region", columns="producto", aggfunc="sum", fill_value=0)\n'
            "print(pivote)\n\n"
            'tabla_cruzada = pd.crosstab(ventas["region"], ventas["producto"])\n'
            "print(tabla_cruzada)",
        ),
        Section(
            "Datos faltantes",
            "isna/fillna/dropna — detectar, rellenar o eliminar valores nulos (NaN).",
            "import pandas as pd\n"
            "import numpy as np\n\n"
            "df = pd.DataFrame({\n"
            '    "nombre": ["Ana", "Luis", None, "Eva"],\n'
            '    "edad": [30, np.nan, 25, 40],\n'
            "})\n\n"
            "print(df.isna().sum())\n"
            'print(df.fillna({"nombre": "Desconocido", "edad": df["edad"].mean()}))\n'
            "print(df.dropna())",
        ),
        Section(
            "apply, map y metodos de texto vectorizados",
            "Transformar columnas con una funcion propia, o con el accessor `.str`.",
            "import pandas as pd\n\n"
            "df = pd.DataFrame({\n"
            '    "nombre": [" ana garcia ", "LUIS PEREZ", "eva  torres"],\n'
            '    "puntos": [10, 25, 18],\n'
            "})\n\n"
            'df["nombre_limpio"] = df["nombre"].str.strip().str.title()\n'
            'df["categoria"] = df["puntos"].map(lambda p: "alto" if p >= 20 else "bajo")\n'
            'df["doble_puntos"] = df["puntos"].apply(lambda p: p * 2)\n'
            "print(df)",
        ),
        Section(
            "Fechas con to_datetime",
            "Convertir texto a fechas reales y extraer componentes (mes, dia de la semana...).",
            "import pandas as pd\n\n"
            'fechas = pd.to_datetime(["2026-01-15", "2026-03-02", "2026-07-30"])\n'
            'df = pd.DataFrame({"fecha": fechas, "ventas": [100, 150, 200]})\n'
            'df["mes"] = df["fecha"].dt.month\n'
            'df["dia_semana"] = df["fecha"].dt.day_name()\n'
            "print(df)",
        ),
        Section(
            "Leer y escribir CSV en memoria",
            "to_csv/read_csv funcionan igual con un archivo real o con io.StringIO.",
            "import pandas as pd\n"
            "import io\n\n"
            'df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})\n'
            "buffer = io.StringIO()\n"
            "df.to_csv(buffer, index=False)\n"
            "print(buffer.getvalue())\n\n"
            "buffer.seek(0)\n"
            "leido = pd.read_csv(buffer)\n"
            "print(leido)",
        ),
        Section(
            "Estadisticas descriptivas",
            "describe(), corr() y value_counts() para un primer vistazo a los datos.",
            "import pandas as pd\n\n"
            "df = pd.DataFrame({\n"
            '    "edad": [25, 30, 35, 40, 45],\n'
            '    "salario": [30000, 45000, 50000, 62000, 58000],\n'
            "})\n\n"
            "print(df.describe())\n"
            "print(df.corr())\n"
            'print(df["edad"].value_counts(bins=2))',
        ),
    ],
)


MATPLOTLIB = Library(
    key="matplotlib",
    title="Matplotlib",
    url="https://matplotlib.org/",
    intro=(
        "Complementa la sesion S11 (Visualizacion) del Modo Maestro: como armar "
        "graficos de linea, barras, dispersion e histogramas, usar subplots, "
        "personalizar estilos/leyendas y trabajar con la interfaz orientada a "
        "objetos (`fig, ax`) en vez de la interfaz de estado (`plt.algo()`)."
    ),
    sections=[
        Section(
            "Grafico de linea basico",
            "plt.plot dibuja una serie de puntos (x, y) conectados por una linea.",
            "import matplotlib.pyplot as plt\n"
            "import numpy as np\n\n"
            "x = np.linspace(0, 10, 100)\n"
            "y = np.sin(x)\n\n"
            "plt.plot(x, y)\n"
            'plt.title("Funcion seno")\n'
            'plt.xlabel("x")\n'
            'plt.ylabel("sin(x)")\n'
            "plt.show()",
        ),
        Section(
            "Subplots: varias graficas en una figura",
            "plt.subplots(filas, columnas) devuelve una figura y un array de ejes.",
            "import matplotlib.pyplot as plt\n"
            "import numpy as np\n\n"
            "x = np.linspace(0, 10, 100)\n"
            "fig, ejes = plt.subplots(1, 2, figsize=(10, 4))\n\n"
            'ejes[0].plot(x, np.sin(x), color="tab:blue")\n'
            'ejes[0].set_title("Seno")\n\n'
            'ejes[1].plot(x, np.cos(x), color="tab:orange")\n'
            'ejes[1].set_title("Coseno")\n\n'
            "plt.tight_layout()\n"
            "plt.show()",
        ),
        Section(
            "Grafico de barras",
            "plt.bar compara valores entre categorias.",
            "import matplotlib.pyplot as plt\n\n"
            'productos = ["A", "B", "C", "D"]\n'
            "ventas = [120, 85, 200, 60]\n\n"
            'plt.bar(productos, ventas, color="tab:green")\n'
            'plt.title("Ventas por producto")\n'
            'plt.ylabel("Unidades vendidas")\n'
            "plt.show()",
        ),
        Section(
            "Scatter (dispersion)",
            "plt.scatter muestra cada punto por separado — ideal para ver correlacion entre dos variables.",
            "import matplotlib.pyplot as plt\n"
            "import numpy as np\n\n"
            "rng = np.random.default_rng(0)\n"
            "x = rng.normal(0, 1, 100)\n"
            "y = x * 2 + rng.normal(0, 1, 100)\n\n"
            'plt.scatter(x, y, alpha=0.6, c=y, cmap="viridis")\n'
            'plt.title("Dispersion x vs y")\n'
            'plt.colorbar(label="valor de y")\n'
            "plt.show()",
        ),
        Section(
            "Histograma",
            "plt.hist agrupa valores en bins para mostrar como se distribuyen.",
            "import matplotlib.pyplot as plt\n"
            "import numpy as np\n\n"
            "rng = np.random.default_rng(0)\n"
            "datos = rng.normal(170, 10, 500)\n\n"
            'plt.hist(datos, bins=20, color="tab:purple", edgecolor="white")\n'
            'plt.title("Distribucion de alturas")\n'
            'plt.xlabel("cm")\n'
            'plt.ylabel("frecuencia")\n'
            "plt.show()",
        ),
        Section(
            "Personalizacion: colores, estilos y leyenda",
            "Lineas punteadas, colores por nombre, `label=` + `plt.legend()`.",
            "import matplotlib.pyplot as plt\n"
            "import numpy as np\n\n"
            "x = np.linspace(0, 10, 50)\n\n"
            'plt.plot(x, np.sin(x), "--", color="crimson", label="seno")\n'
            'plt.plot(x, np.cos(x), ":", color="navy", label="coseno")\n'
            "plt.legend()\n"
            "plt.grid(True, alpha=0.3)\n"
            'plt.title("Seno y coseno")\n'
            "plt.show()",
        ),
        Section(
            "Estilo orientado a objetos (fig, ax)",
            "La forma recomendada para graficos complejos: controlar la figura y los ejes directamente.",
            "import matplotlib.pyplot as plt\n"
            "import numpy as np\n"
            "import io\n\n"
            "fig, ax = plt.subplots(figsize=(6, 4))\n"
            "x = np.linspace(-5, 5, 100)\n"
            "ax.plot(x, x**2)\n"
            'ax.set_title("Parabola")\n'
            'ax.set_xlabel("x")\n'
            'ax.set_ylabel("x^2")\n'
            'ax.axhline(0, color="gray", linewidth=0.5)\n'
            'ax.axvline(0, color="gray", linewidth=0.5)\n\n'
            "buffer = io.BytesIO()\n"
            'fig.savefig(buffer, format="png", dpi=100)\n'
            'print("Figura serializada en memoria:", len(buffer.getvalue()), "bytes")',
        ),
        Section(
            "Anotaciones y texto en el grafico",
            "plt.annotate senala un punto con texto y una flecha.",
            "import matplotlib.pyplot as plt\n"
            "import numpy as np\n\n"
            "x = np.linspace(0, 10, 100)\n"
            "y = np.sin(x)\n"
            "maximo_idx = np.argmax(y)\n\n"
            "plt.plot(x, y)\n"
            'plt.annotate("maximo", xy=(x[maximo_idx], y[maximo_idx]),\n'
            "             xytext=(x[maximo_idx] + 1, y[maximo_idx] - 0.3),\n"
            '             arrowprops=dict(arrowstyle="->"))\n'
            'plt.title("Seno con anotacion")\n'
            "plt.show()",
        ),
    ],
)


SEABORN = Library(
    key="seaborn",
    title="Seaborn",
    url="https://seaborn.pydata.org/",
    intro=(
        "Seaborn se construye sobre Matplotlib y trabaja directamente con "
        "DataFrames de Pandas: menos codigo para graficos estadisticos "
        "(distribuciones, comparaciones entre grupos, correlaciones). Los "
        "datos de estos ejemplos se generan con NumPy en vez de descargarlos "
        "con `sns.load_dataset`, para que corran sin conexion a internet."
    ),
    sections=[
        Section(
            "Preparar datos y tema (sns.set_theme)",
            "sns.set_theme() cambia el aspecto de TODOS los graficos siguientes, sean de seaborn o matplotlib.",
            "import seaborn as sns\n"
            "import pandas as pd\n"
            "import numpy as np\n\n"
            'sns.set_theme(style="whitegrid")\n\n'
            "rng = np.random.default_rng(7)\n"
            "df = pd.DataFrame({\n"
            '    "horas_estudio": rng.uniform(0, 10, 80),\n'
            '    "grupo": rng.choice(["A", "B"], 80),\n'
            "})\n"
            'df["nota"] = 4 + df["horas_estudio"] * 0.6 + rng.normal(0, 1, 80)\n'
            "print(df.head())",
        ),
        Section(
            "scatterplot con hue",
            "`hue=` colorea los puntos segun una columna categorica, para comparar grupos en el mismo grafico.",
            "import seaborn as sns\n"
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n"
            "import numpy as np\n\n"
            "rng = np.random.default_rng(7)\n"
            "df = pd.DataFrame({\n"
            '    "horas_estudio": rng.uniform(0, 10, 80),\n'
            '    "grupo": rng.choice(["A", "B"], 80),\n'
            "})\n"
            'df["nota"] = 4 + df["horas_estudio"] * 0.6 + rng.normal(0, 1, 80)\n\n'
            'sns.scatterplot(data=df, x="horas_estudio", y="nota", hue="grupo")\n'
            'plt.title("Nota segun horas de estudio")\n'
            "plt.show()",
        ),
        Section(
            "histplot: distribucion de una variable",
            "Histograma + estimador de densidad (`kde=True`) en una sola llamada.",
            "import seaborn as sns\n"
            "import matplotlib.pyplot as plt\n"
            "import numpy as np\n\n"
            "rng = np.random.default_rng(1)\n"
            "alturas = rng.normal(170, 8, 300)\n\n"
            'sns.histplot(alturas, bins=25, kde=True, color="teal")\n'
            'plt.title("Distribucion de alturas (con estimador de densidad)")\n'
            "plt.show()",
        ),
        Section(
            "boxplot y violinplot: comparar grupos",
            "Ambos resumen la distribucion por categoria; el violin ademas muestra la forma completa.",
            "import seaborn as sns\n"
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n"
            "import numpy as np\n\n"
            "rng = np.random.default_rng(3)\n"
            "df = pd.DataFrame({\n"
            '    "region": rng.choice(["Norte", "Sur", "Este"], 150),\n'
            '    "ventas": rng.normal(100, 20, 150),\n'
            "})\n\n"
            "fig, ejes = plt.subplots(1, 2, figsize=(10, 4))\n"
            'sns.boxplot(data=df, x="region", y="ventas", ax=ejes[0])\n'
            'sns.violinplot(data=df, x="region", y="ventas", ax=ejes[1])\n'
            "plt.tight_layout()\n"
            "plt.show()",
        ),
        Section(
            "heatmap: matriz de correlacion",
            "Combina `df.corr()` de Pandas con `sns.heatmap` para ver relaciones entre variables de un vistazo.",
            "import seaborn as sns\n"
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n"
            "import numpy as np\n\n"
            "rng = np.random.default_rng(5)\n"
            "df = pd.DataFrame({\n"
            '    "altura": rng.normal(170, 10, 100),\n'
            '    "peso": rng.normal(70, 12, 100),\n'
            '    "edad": rng.integers(18, 60, 100),\n'
            "})\n"
            'df["peso"] = df["peso"] + df["altura"] * 0.3\n\n'
            'sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")\n'
            'plt.title("Correlacion entre variables")\n'
            "plt.show()",
        ),
        Section(
            "barplot con intervalo de confianza",
            "Cada barra muestra el promedio; la lineita vertical es la variabilidad (`errorbar=`).",
            "import seaborn as sns\n"
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n"
            "import numpy as np\n\n"
            "rng = np.random.default_rng(9)\n"
            "df = pd.DataFrame({\n"
            '    "producto": rng.choice(["A", "B", "C"], 120),\n'
            '    "satisfaccion": rng.uniform(1, 5, 120),\n'
            "})\n\n"
            'sns.barplot(data=df, x="producto", y="satisfaccion", errorbar="sd")\n'
            'plt.title("Satisfaccion promedio por producto (barra = desvio estandar)")\n'
            "plt.show()",
        ),
        Section(
            "pairplot: relaciones entre varias variables",
            "Una grilla con cada variable numerica cruzada contra las demas — un scatter matrix automatico.",
            "import seaborn as sns\n"
            "import pandas as pd\n"
            "import numpy as np\n\n"
            "rng = np.random.default_rng(11)\n"
            "df = pd.DataFrame({\n"
            '    "altura": rng.normal(170, 10, 60),\n'
            '    "peso": rng.normal(70, 12, 60),\n'
            '    "grupo": rng.choice(["X", "Y"], 60),\n'
            "})\n"
            'df["peso"] = df["peso"] + df["altura"] * 0.2\n\n'
            'sns.pairplot(df, hue="grupo")',
        ),
        Section(
            "lineplot con intervalo de confianza (series temporales)",
            "Con datos repetidos por `x`, seaborn dibuja el promedio y una banda de variabilidad automaticamente.",
            "import seaborn as sns\n"
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n"
            "import numpy as np\n\n"
            "rng = np.random.default_rng(13)\n"
            "dias = list(range(30)) * 3\n"
            "valores = []\n"
            "for repeticion in range(3):\n"
            "    valores += list(20 + np.cumsum(rng.normal(0, 1, 30)))\n\n"
            'df = pd.DataFrame({"dia": dias, "valor": valores})\n\n'
            'sns.lineplot(data=df, x="dia", y="valor", errorbar="sd")\n'
            'plt.title("Evolucion diaria (con banda de variabilidad)")\n'
            "plt.show()",
        ),
    ],
)

ALL_LIBRARIES: list[Library] = [PYTHON_STDLIB, NUMPY, PANDAS, MATPLOTLIB, SEABORN]

"""Diccionario de metodos y funciones de Python -> explicacion corta en espanol.

generate_notebooks.py escanea el codigo de cada sesion del Modo Maestro en
busca de estas claves (por texto literal, ej. ".append(" o "sorted(") y arma
automaticamente la seccion "Metodos y funciones usados aqui" de cada
notebook. Mantener esto en un solo diccionario evita repetir la misma
explicacion 48 veces a mano y facilita agregar nuevas sesiones despues.

El orden de los items no importa: generate_notebooks.py los presenta en el
orden en que aparecen dentro del codigo de cada sesion.
"""

METHOD_DOCS = {
    # ── listas ──
    ".append(": "list.append(x) — agrega x al final de la lista, en el sitio (no devuelve nada).",
    ".extend(": "list.extend(it) — agrega todos los elementos del iterable it al final.",
    ".insert(": "list.insert(i, x) — inserta x en la posicion i, desplazando el resto.",
    ".pop(": "list.pop(i=-1) — elimina y devuelve el elemento en la posicion i (por defecto, el ultimo).",
    ".remove(": "list.remove(x) — elimina la primera aparicion del valor x (error si no existe).",
    ".index(": "seq.index(x) — devuelve la posicion de la primera aparicion de x.",
    ".count(": "seq.count(x) — cuenta cuantas veces aparece x.",
    ".sort(": "list.sort(key=None, reverse=False) — ordena la lista en el sitio.",
    ".reverse(": "list.reverse() — invierte el orden de la lista en el sitio.",
    ".copy(": "obj.copy() — copia superficial (shallow copy) de la lista/dict.",
    # ── tuplas / desempaquetado ──
    "= (": "tupla — coleccion inmutable y ordenada; se crea con parentesis y comas.",
    ", = ": "desempaquetado (unpacking) — asigna varios nombres a la vez desde una secuencia.",
    # ── dicts ──
    ".keys(": "dict.keys() — vista con todas las claves del diccionario.",
    ".values(": "dict.values() — vista con todos los valores del diccionario.",
    ".items(": "dict.items() — vista de pares (clave, valor), ideal para iterar con for k, v in d.items().",
    ".get(": "dict.get(clave, default) — busca la clave sin lanzar KeyError si no existe.",
    ".update(": "dict.update(otro) — mezcla otro diccionario/iterable de pares dentro del actual.",
    ".setdefault(": "dict.setdefault(clave, default) — devuelve el valor si existe; si no, lo crea con default.",
    # ── sets ──
    ".add(": "set.add(x) — agrega x al conjunto (no hace nada si ya estaba).",
    ".discard(": "set.discard(x) — elimina x del conjunto si esta presente, sin lanzar error si no.",
    ".union(": "set.union(otro) — nuevo conjunto con todos los elementos de ambos.",
    ".intersection(": "set.intersection(otro) — nuevo conjunto solo con los elementos comunes.",
    # ── strings ──
    ".split(": "str.split(sep) — parte el string en una lista de trozos segun el separador.",
    ".join(": "sep.join(iterable) — une los elementos del iterable en un solo string, separados por sep.",
    ".strip(": "str.strip(chars=None) — quita espacios (o los caracteres indicados) al inicio y al final.",
    ".replace(": "str.replace(viejo, nuevo) — devuelve un string nuevo con las coincidencias reemplazadas.",
    ".upper(": "str.upper() — devuelve el string en mayusculas.",
    ".lower(": "str.lower() — devuelve el string en minusculas.",
    ".title(": "str.title() — pone en mayuscula la primera letra de cada palabra.",
    ".format(": "str.format(...) — sustituye placeholders {} por valores.",
    ".startswith(": "str.startswith(prefijo) — True si el string empieza con ese prefijo.",
    ".endswith(": "str.endswith(sufijo) — True si el string termina con ese sufijo.",
    ".find(": "str.find(sub) — indice de la primera aparicion de sub, o -1 si no esta.",
    "[::-1]": "slicing [::-1] — invierte una secuencia (string, lista, tupla) creando una copia.",
    "f\"": "f-string — interpolacion de expresiones dentro de un string con f\"...{expr}...\".",
    "f'": "f-string — interpolacion de expresiones dentro de un string con f'...{expr}...'.",
    # ── control de flujo / funcional ──
    "enumerate(": "enumerate(it) — recorre un iterable devolviendo pares (indice, valor).",
    "zip(": "zip(a, b) — combina dos (o mas) iterables en pares/tuplas, elemento a elemento.",
    "map(": "map(fn, it) — aplica fn a cada elemento de it (evaluacion perezosa).",
    "filter(": "filter(fn, it) — conserva solo los elementos de it para los que fn(elem) es True.",
    "reduce(": "functools.reduce(fn, it) — acumula it aplicando fn de a pares hasta un solo resultado.",
    "sorted(": "sorted(it, key=None, reverse=False) — devuelve una NUEVA lista ordenada (no modifica it).",
    "lambda": "lambda args: expr — funcion anonima de una sola expresion, comun como key= en sorted/map/filter.",
    "yield": "yield — pausa la funcion y la convierte en generador; produce un valor cada vez que se le pide con next().",
    "next(": "next(gen) — pide el siguiente valor de un generador/iterador.",
    "range(": "range(a, b, paso) — secuencia perezosa de enteros, muy usada en bucles for.",
    "*args": "`*args` — junta los argumentos posicionales extra de una funcion en una tupla.",
    "**kwargs": "`**kwargs` — junta los argumentos nombrados extra de una funcion en un diccionario.",
    "super(": "super() — llama a la implementacion de la clase padre (usado en herencia).",
    "@property": "@property — convierte un metodo en un atributo de solo lectura (se accede sin parentesis).",
    "@staticmethod": "@staticmethod — metodo que no recibe self, vive en la clase solo por organizacion.",
    "@abstractmethod": "@abstractmethod — obliga a las subclases de una ABC a implementar ese metodo.",
    "isinstance(": "isinstance(obj, Clase) — comprueba el tipo (o herencia) de un objeto.",
    "try:": "try/except/else/finally — captura errores en tiempo de ejecucion sin romper el programa.",
    "assert ": "assert condicion — lanza AssertionError si la condicion es falsa; usado para tests rapidos.",
    "raise ": "raise Excepcion(...) — lanza una excepcion manualmente.",
    "[x for x in": "list comprehension — [expr for x in it if cond] crea una lista en una sola linea.",
    "for x in range": "generator expression — (expr for x in it) es como una list comprehension pero perezosa.",
    # ── estructuras de datos (collections/heapq) ──
    "deque(": "collections.deque — lista doblemente enlazada; append/appendleft y pop/popleft son O(1).",
    ".popleft(": "deque.popleft() — saca y devuelve el elemento del extremo izquierdo (para colas FIFO).",
    ".appendleft(": "deque.appendleft(x) — agrega x al extremo izquierdo.",
    "heapq.heappush(": "heapq.heappush(heap, x) — inserta x manteniendo la propiedad de min-heap.",
    "heapq.heappop(": "heapq.heappop(heap) — extrae y devuelve el elemento mas pequeno del heap.",
    "Counter(": "collections.Counter — diccionario especializado para contar apariciones de elementos.",
    ".most_common(": "Counter.most_common(n) — los n elementos mas frecuentes, de mayor a menor.",
    # ── numpy ──
    "np.array(": "np.array(lista) — crea un ndarray de NumPy a partir de una lista (o lista de listas).",
    "np.zeros(": "np.zeros(shape) — crea un array lleno de ceros con la forma indicada.",
    "np.arange(": "np.arange(a, b, paso) — como range() pero devuelve un ndarray.",
    "np.linspace(": "np.linspace(a, b, n) — n puntos equiespaciados entre a y b (incluye ambos extremos).",
    "np.eye(": "np.eye(n) — matriz identidad de n x n.",
    "np.where(": "np.where(cond, si, no) — array condicional elemento a elemento (vectorizado).",
    "np.linalg.solve(": "np.linalg.solve(A, b) — resuelve el sistema lineal A @ x = b.",
    "np.random.seed(": "np.random.seed(n) — fija la semilla aleatoria para resultados reproducibles.",
    "np.random.randint(": "np.random.randint(a, b, shape) — enteros aleatorios en [a, b) con la forma dada.",
    "np.random.normal(": "np.random.normal(media, std, n) — n muestras de una distribucion normal.",
    "np.histogram(": "np.histogram(datos, bins) — cuenta cuantos valores caen en cada intervalo (bin).",
    ".mean(": "ndarray/Series.mean(axis=None) — promedio; con axis=0/1 promedia por columnas/filas.",
    ".std(": "ndarray/Series.std() — desviacion estandar.",
    ".astype(": "ndarray.astype(tipo) — convierte el array a otro dtype (ej. np.uint8).",
    "@ ": "@ — operador de multiplicacion de matrices (equivalente a np.matmul).",
    # ── pandas ──
    "pd.Series(": "pd.Series(datos, index=...) — columna etiquetada de una dimension.",
    "pd.DataFrame(": "pd.DataFrame(dict) — tabla 2D; cada clave del dict se vuelve una columna.",
    ".groupby(": "df.groupby(col) — agrupa filas por el valor de una columna para agregarlas despues.",
    ".apply(": "Series/DataFrame.apply(fn) — aplica una funcion a cada elemento, fila o columna.",
    ".merge(": "df.merge(otro, on=...) — combina dos DataFrames como un JOIN de SQL.",
    ".pivot_table(": "df.pivot_table(values, index, columns, aggfunc) — tabla resumen cruzando categorias.",
    ".fillna(": "df.fillna(valor) — rellena los valores nulos (NaN) con el valor/estrategia indicada.",
    ".dropna(": "df.dropna() — elimina las filas (o columnas) que contienen algun nulo.",
    ".isnull(": "df.isnull() — mascara booleana de que celdas son nulas (NaN).",
    ".corr(": "df.corr() — matriz de correlacion entre columnas numericas.",
    ".iterrows(": "df.iterrows() — recorre el DataFrame fila por fila como pares (indice, Series).",
    ".sort_values(": "df.sort_values(by=col) — ordena las filas segun los valores de una columna.",
    ".to_dict(": "df/Series.to_dict() — convierte a diccionario (o lista de dicts) de Python puro.",
    ".loc[": "df.loc[etiqueta] — selecciona filas/columnas por etiqueta (nombre de indice).",
    ".iloc[": "df.iloc[pos] — selecciona filas/columnas por posicion numerica.",
    ".str.": "accessor .str — aplica metodos de string (split, strip, contains...) a toda una columna a la vez.",
    # ── archivos / io ──
    "io.StringIO(": "io.StringIO() — un archivo de texto que vive en memoria, sin tocar el disco.",
    "csv.writer(": "csv.writer(archivo) — escribe filas como texto CSV.",
    "csv.DictReader(": "csv.DictReader(archivo) — lee CSV y entrega cada fila como diccionario {columna: valor}.",
}

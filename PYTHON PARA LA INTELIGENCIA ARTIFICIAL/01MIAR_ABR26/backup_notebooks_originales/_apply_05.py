"""Aplica mejoras al notebook 05_Files con bloques de colores y teoria detallada."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, solucion_md, dato, aviso
import json

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_05_Python101_Files.ipynb"

nb = json.load(open(NB, encoding="utf-8"))

def find_id(fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if fragment in src:
            return c["id"]
    return None

# IDs de anchors clave del notebook 05
ID_TITULO       = nb["cells"][0]["id"]                            # cell 0  - portada
ID_ACCESO       = find_id("# Acceso a ficheros")                  # cell 1
ID_FICHEROS     = find_id("## Ficheros")                          # cell 2
ID_FORMATO      = find_id("Formato general para abrir un fichero")# cell 4
ID_LEC_READ     = find_id("Lectura desde fichero usando")         # cell 5  (codigo)
ID_LEC_FOR      = find_id("Lectura linea a linea")                # cell 6  (codigo)
ID_LEC_LIST     = find_id("leer de un archivo a una lista")       # cell 7  (codigo)
ID_PATHS        = find_id("Resoluci")                              # cell 8  - paths plataforma
ID_PATHS_CODE   = find_id("dataset_file_path = ")                  # cell 9  (codigo)
ID_WITH         = find_id("close")                                  # cell 10 - with
ID_WITH_CODE    = find_id("with open(ruta) as mi_fichero")         # cell 11 (codigo)
ID_VARIOS       = find_id("Se puede abrir varios ficheros")        # cell 12
ID_VARIOS_CODE  = find_id("abrir varios ficheros en el mismo with")# cell 13
ID_MODOS        = find_id("## Modos de acceso")                    # cell 14
ID_TABLA_MODOS  = find_id("Al crear un objeto de tipo")            # cell 15
ID_ESCRITURA    = find_id("## Acceso para escritura")              # cell 16
ID_ESCR_FUNC    = find_id("def crear_lista")                       # cell 17 (codigo)
ID_ESCR_USO     = find_id("o_dummy.txt")                           # cell 18 (codigo)
ID_BUFFERING    = find_id("#### Buffering")                        # cell 19
ID_BUFF_TEXTO   = find_id("Por defecto, el texto que transfieres") # cell 20
ID_BUFF_CODE3   = find_id("fichero_write.flush()")                 # cell 23
ID_CSV          = find_id("## Archivos CSV")                       # cell 24
ID_CSV_TEXTO    = find_id("Python permite leer datos de ficheros CSV") # cell 25
ID_CSV_LEER     = find_id("tabla_operaciones.csv contiene valores") # cell 26 (codigo)
ID_CSV_ESC      = find_id("o_tabla_operaciones.csv")               # cell 27 (codigo)
ID_DOCSTRINGS   = find_id("# Docstrings")                          # cell 28
ID_EJERCICIOS   = find_id("## Ejercicios")                         # cell 49
ID_EJ3          = find_id("anyadir_palabra")                       # cell 53 (final)


plan = []

# ============ INTRO ============
plan.append((ID_TITULO, [
    {"type": "md", "src": teoria(
        "Como leer este notebook (version mejorada)",
        """Este notebook fue **enriquecido** con bloques de teoria detallada y ejercicios para que practiques **leyendo y escribiendo ficheros** desde Python.

<div style="background-color:#e7f5ff;border-left:6px solid #1c7ed6;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AZUL = TEORIA</b></div> -> explicacion en palabras simples antes de cada concepto.

<div style="background-color:#fff9db;border-left:6px solid #f59f00;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AMARILLO = TU TURNO</b></div> -> ejercicio para resolver. Tienes una celda vacia donde escribir tu codigo.

<div style="background-color:#ebfbee;border-left:6px solid #2f9e44;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>VERDE = SOLUCION</b></div> -> codigo de referencia comentado. Destapalo SOLO despues de intentar.

> **Promesa:** el codigo y la teoria del profesor original NO se han tocado. Solo se han ANADIDO bloques nuevos."""
    )},
    {"type": "md", "src": dato(
        """En esta clase aprenderas a **interactuar con ficheros del disco**. Es uno de los temas mas practicos: casi cualquier programa real necesita leer datos de entrada (CSVs, JSONs, logs) y guardar resultados.

**Temas que cubriremos:**
- `open(...)`, modos de apertura (`r`, `w`, `a`, `b`, `+`, `t`).
- `with` (context manager) y por que es la forma correcta.
- `read`, `readline`, `readlines`, iteracion linea a linea.
- `write`, `writelines`, `flush`.
- Codificacion: `encoding='utf-8'` y por que importa.
- Modulo `csv` (`reader`, `writer`, `DictReader`, `DictWriter`).
- Modulo `json` (`load`, `dump`, `loads`, `dumps`).
- Modulo `pickle` (serializar objetos Python).
- `pathlib` y `os.path` para rutas portables.

**Importante:** todos los ejercicios usaran la carpeta `res/` que ya existe en el proyecto, o crearan archivos temporales que luego eliminaremos."""
    )},
]))

# ============ ACCESO A FICHEROS - panorama ============
plan.append((ID_ACCESO, [
    {"type": "md", "src": teoria(
        "Que es leer y escribir un fichero?",
        """Un **fichero** (o archivo) es una **secuencia de bytes** guardada en el disco con un nombre. Puede ser:

- **Texto** (`.txt`, `.csv`, `.json`, `.py`, `.md`...): bytes que representan caracteres legibles.
- **Binario** (`.png`, `.jpg`, `.zip`, `.pkl`, `.exe`...): bytes que NO representan texto.

#### El ciclo basico de trabajo con un fichero

```
1. ABRIR    -> open(ruta, modo)         devuelve un objeto file
2. LEER o ESCRIBIR -> .read(), .write()  hacer trabajo
3. CERRAR   -> .close()                 liberar el recurso
```

**Por que cerrar es importante?**
- Si no cierras, los datos pueden quedar **en buffer** sin escribir realmente.
- Otros programas pueden no poder abrir el fichero (queda bloqueado).
- Consumes un *file descriptor* del sistema operativo.

**La buena noticia:** el bloque `with` (que veras en seguida) cierra el fichero **automaticamente** por ti, incluso si hay errores. Es la forma recomendada en Python."""
    )},
]))

# ============ FORMATO GENERAL DE OPEN ============
plan.append((ID_FORMATO, [
    {"type": "md", "src": teoria(
        "<code>open()</code>: la firma completa",
        """La funcion incorporada `open()` tiene mas argumentos de los que parecen. Aqui los importantes:

```python
open(file, mode='r', encoding=None, newline=None, buffering=-1)
```

| Parametro | Para que sirve |
|---|---|
| `file` | Ruta al fichero (string o `pathlib.Path`). |
| `mode` | Modo de apertura: `'r'`, `'w'`, `'a'`, con `'b'` o `'t'` y `'+'`. |
| `encoding` | Codificacion de texto. **Recomendado: `'utf-8'`** (ver abajo). |
| `newline` | Como se manejan los saltos de linea. Importante en CSV. |
| `buffering` | Tamano del buffer en bytes. Por defecto, automatico. |

#### Que devuelve `open()`?

Un **objeto fichero** (`io.TextIOWrapper` para texto, `io.BufferedReader` para binario). Sobre ese objeto llamas a metodos como `.read()`, `.readline()`, `.write()`, `.close()`.

#### Por que casi siempre poner `encoding='utf-8'`?

Si no lo pones, Python usa la codificacion **por defecto del sistema**, que en **Windows suele ser `cp1252`** y en Linux/Mac `utf-8`. Esto causa errores raros con tildes, emojis o cualquier caracter no ingles.

```python
# MAL (puede fallar en Windows con tildes):
open('archivo.txt')

# BIEN (portable):
open('archivo.txt', encoding='utf-8')
```

**Regla:** SIEMPRE especifica `encoding='utf-8'` salvo que sepas que el fichero usa otra codificacion."""
    )},
    {"type": "md", "src": tu_turno(1,
        """Abre el fichero `res/one_line.txt` con `open()`, lee TODO su contenido con `.read()` y muestralo. Recuerda **cerrar** el fichero con `.close()` al final.

> Debe imprimir la unica linea que contiene ese fichero."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# # Abrimos el fichero en modo lectura (por defecto 'r')\n# fichero = open('res/one_line.txt', encoding='utf-8')\n# # Leemos todo el contenido como un solo string\n# contenido = fichero.read()\n# print(contenido)\n# # IMPORTANTE: cerrar para liberar el recurso\n# fichero.close()\n"},
]))

# ============ METODOS DE LECTURA ============
plan.append((ID_LEC_READ, [
    {"type": "md", "src": teoria(
        "Tres formas de leer un fichero",
        """Una vez abierto un fichero en modo texto, tienes **tres metodos** para leerlo:

| Metodo | Que devuelve | Cuando usarlo |
|---|---|---|
| `.read()` | TODO el contenido como un solo string | Ficheros pequenos. **Cuidado con ficheros grandes**: carga todo en RAM. |
| `.read(n)` | Los proximos `n` caracteres | Leer en trozos (chunks). |
| `.readline()` | UNA linea (con su `\\n` final) | Procesar linea a linea controlando el flujo. |
| `.readlines()` | Lista de TODAS las lineas | Necesitas todas las lineas en memoria. |
| `for linea in f:` | Itera linea a linea, eficiente | **La forma recomendada** para ficheros de cualquier tamano. |

#### Por que iterar con `for` es lo mejor?

Porque Python lee **una linea a la vez**, sin cargar el fichero entero en RAM. Funciona igual con un fichero de 10 KB que con uno de 10 GB.

```python
with open('grande.txt', encoding='utf-8') as f:
    for linea in f:
        # procesar linea (incluye el '\\n' al final)
        ...
```

#### El `\\n` de mas

`.readline()` y la iteracion con `for` devuelven cada linea **con el salto de linea final**. Si haces `print(linea)`, veras una linea en blanco extra (porque `print` ya anade su propio `\\n`).

**Soluciones:**
- `print(linea, end='')` -> no anadir el `\\n` extra de print.
- `linea.rstrip()` o `linea.rstrip('\\n')` -> quitar el `\\n` de la linea."""
    )},
]))

plan.append((ID_LEC_LIST, [
    {"type": "md", "src": tu_turno(2,
        """Tienes el fichero `res/multiple_lines.txt`. Abre con `open(...)` (modo `r`, encoding utf-8) y resuelve **TRES tareas**:

1. Cuenta **cuantas lineas** tiene el fichero (usa `.readlines()` y `len(...)`).
2. Imprime **solo la primera linea** del fichero (usa `.readline()` despues de reabrir).
3. Imprime cada linea **sin la doble linea en blanco** (usa el truco `end=''` o `rstrip()`).

Acuerdate de cerrar (o usa `with` si ya lo conoces)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# # 1) Contar lineas con readlines\n# f = open('res/multiple_lines.txt', encoding='utf-8')\n# lineas = f.readlines()       # lista de strings (cada uno termina en \\n)\n# print('Numero de lineas:', len(lineas))\n# f.close()\n#\n# # 2) Solo la primera linea con readline\n# f = open('res/multiple_lines.txt', encoding='utf-8')\n# primera = f.readline()        # devuelve UNA linea con su \\n final\n# print('Primera linea:', primera, end='')\n# f.close()\n#\n# # 3) Iterar sin doble salto de linea\n# f = open('res/multiple_lines.txt', encoding='utf-8')\n# for linea in f:\n#     print(linea, end='')      # no anadimos otro \\n\n# f.close()\n"},
]))

# ============ PATHS ============
plan.append((ID_PATHS, [
    {"type": "md", "src": teoria(
        "Rutas portables: <code>os.path.join</code> y <code>pathlib</code>",
        """Cada sistema operativo separa las carpetas de forma distinta:

- **Windows:** `res\\datos\\fichero.txt` (barra invertida `\\`).
- **Linux / Mac:** `res/datos/fichero.txt` (barra normal `/`).

Si escribes la ruta a mano con barras, tu codigo **no sera portable**. Python te ofrece dos formas correctas:

#### 1. La forma clasica: <code>os.path</code>

```python
import os

ruta = os.path.join('res', 'datos', 'fichero.txt')
# Windows: 'res\\\\datos\\\\fichero.txt'
# Linux:   'res/datos/fichero.txt'

os.path.exists(ruta)       # True/False
os.path.isfile(ruta)       # True si existe y es fichero
os.path.isdir(ruta)        # True si es carpeta
os.path.basename(ruta)     # 'fichero.txt'
os.path.dirname(ruta)      # 'res/datos'
os.path.splitext(ruta)     # ('res/datos/fichero', '.txt')
```

#### 2. La forma moderna: <code>pathlib</code> (Python 3.4+)

`pathlib` te da un objeto **`Path`** orientado a objetos, mucho mas comodo:

```python
from pathlib import Path

ruta = Path('res') / 'datos' / 'fichero.txt'   # uses '/' como operador!

ruta.exists()        # True/False
ruta.is_file()       # True/False
ruta.is_dir()        # True/False
ruta.name            # 'fichero.txt'
ruta.stem            # 'fichero'
ruta.suffix          # '.txt'
ruta.parent          # Path('res/datos')

# Leer / escribir directamente desde el Path:
texto = ruta.read_text(encoding='utf-8')
ruta.write_text('hola', encoding='utf-8')

# Listar contenido de una carpeta:
for f in Path('res').iterdir():
    print(f)

# Buscar con patrones:
for csv in Path('res').glob('*.csv'):
    print(csv)
```

**Recomendacion:** usa `pathlib` en codigo nuevo. Es mas legible y potente."""
    )},
    {"type": "md", "src": tu_turno(3,
        """Usando **`pathlib`**:

1. Crea un `Path` que apunte a `res/multiple_lines.txt`.
2. Comprueba que existe con `.exists()`.
3. Imprime su `.name`, `.stem` y `.suffix`.
4. Lee su contenido completo con `.read_text(encoding='utf-8')` y muestra los primeros 50 caracteres."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# from pathlib import Path\n#\n# # 1) Construimos el path con el operador /\n# ruta = Path('res') / 'multiple_lines.txt'\n#\n# # 2) Comprobamos existencia\n# print('Existe:', ruta.exists())\n#\n# # 3) Partes del path\n# print('Name  :', ruta.name)     # multiple_lines.txt\n# print('Stem  :', ruta.stem)     # multiple_lines\n# print('Suffix:', ruta.suffix)   # .txt\n#\n# # 4) Leemos el contenido directamente\n# texto = ruta.read_text(encoding='utf-8')\n# print('Primeros 50 chars:', repr(texto[:50]))\n"},
]))

# ============ WITH ============
plan.append((ID_WITH, [
    {"type": "md", "src": teoria(
        "<code>with</code>: el bloque que cierra el fichero por ti",
        """El **context manager** `with` es la **forma correcta y recomendada** de trabajar con ficheros en Python.

#### Comparacion lado a lado

```python
# FORMA ANTIGUA (no recomendada)
f = open('archivo.txt', encoding='utf-8')
contenido = f.read()
f.close()                # facil de olvidar
                         # Y SI HAY UNA EXCEPCION ENTRE OPEN Y CLOSE?
                         # El fichero queda abierto.

# FORMA RECOMENDADA
with open('archivo.txt', encoding='utf-8') as f:
    contenido = f.read()
# AL SALIR DEL with (incluso si hay error), Python cierra f automaticamente.
```

#### Que es exactamente un context manager?

Un objeto que sabe **`__enter__`** (al entrar al `with`) y **`__exit__`** (al salir, incluso por excepcion). Para ficheros, `__exit__` llama a `.close()`. Tu te despreocupas.

#### Multiples ficheros en el mismo `with`

Hay **dos formas**:

```python
# Forma 1: comas
with open('a.txt') as fa, open('b.txt') as fb:
    ...

# Forma 2 (Python 3.10+): parentesis
with (
    open('a.txt') as fa,
    open('b.txt') as fb,
):
    ...
```

#### Buenas practicas

- SIEMPRE usa `with` salvo que tengas una razon muy concreta para no usarlo.
- Mantenlo lo mas corto posible: abre, lee/escribe lo que necesites, sal del bloque.
- Si necesitas el contenido fuera del `with`, leelo dentro y guarda el resultado:
  ```python
  with open('a.txt', encoding='utf-8') as f:
      datos = f.read()
  # aqui ya no necesitas f, pero datos sigue disponible
  ```"""
    )},
]))

plan.append((ID_VARIOS_CODE, [
    {"type": "md", "src": tu_turno(4,
        """Crea un fichero **temporal** llamado `res/o_saludo.txt` y dentro escribe la frase `Hola mundo desde Python`. Usa `with open(...)` con modo `'w'` y `encoding='utf-8'`.

Despues, en otro `with`, **lee** el fichero y muestra su contenido.

Por ultimo, eliminalo con `os.remove(ruta)` o `Path(ruta).unlink()` (lo que prefieras) para no dejar basura."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import os\n# ruta = os.path.join('res', 'o_saludo.txt')\n#\n# # Escritura: 'w' crea o sobrescribe\n# with open(ruta, 'w', encoding='utf-8') as f:\n#     f.write('Hola mundo desde Python')\n#\n# # Lectura\n# with open(ruta, 'r', encoding='utf-8') as f:\n#     contenido = f.read()\n# print(contenido)\n#\n# # Limpieza: borramos el fichero\n# os.remove(ruta)\n# print('Fichero eliminado.')\n"},
]))

# ============ MODOS ============
plan.append((ID_MODOS, [
    {"type": "md", "src": teoria(
        "Modos de apertura: la tabla maestra",
        """Los **modos** de `open()` son letras que combinas para indicar QUE quieres hacer y COMO.

#### Letra principal (que vas a hacer)

| Modo | Significado | Si NO existe el fichero | Si SI existe |
|---|---|---|---|
| `'r'` | Leer (read) | Error `FileNotFoundError` | Lee desde el principio |
| `'w'` | Escribir (write) | Lo crea | **Lo VACIA** (cuidado!) |
| `'a'` | Anadir (append) | Lo crea | Anade al final, sin tocar el contenido previo |
| `'x'` | Crear exclusivo | Lo crea | Error `FileExistsError` (no sobrescribe) |

#### Letra secundaria (formato del contenido)

| Modo | Significado |
|---|---|
| `'t'` | Texto (DEFECTO). Lee/escribe `str` y maneja `\\n`. |
| `'b'` | Binario. Lee/escribe `bytes`. Usar para imagenes, audio, pickle... |

#### El extra: <code>+</code> (lectura **Y** escritura)

| Modo | Que permite |
|---|---|
| `'r+'` | Lee y escribe. NO trunca. Falla si no existe. |
| `'w+'` | Lee y escribe. **TRUNCA** al abrir. |
| `'a+'` | Lee y anade. Crea si no existe. La escritura siempre va al final. |

#### Combinaciones tipicas

| Quiero... | Modo |
|---|---|
| Leer un .txt | `'r'` (o `'rt'`) |
| Leer una imagen | `'rb'` |
| Crear un .txt nuevo | `'w'` |
| Anadir lineas a un log | `'a'` |
| Escribir bytes (pickle) | `'wb'` |
| Leer bytes (pickle) | `'rb'` |

> **Cuidado mortal:** `'w'` **borra todo** el contenido previo del fichero al abrirlo. Si el fichero contenia datos importantes, se perdieron. Si no estas seguro, usa `'a'` o `'x'`."""
    )},
    {"type": "md", "src": aviso(
        """**Resumen visual de los peligros:**

- Abrir con `'w'` **siempre** vacia el fichero. No hay confirmacion.
- Abrir con `'r'` un fichero que no existe lanza `FileNotFoundError`.
- Abrir con `'x'` un fichero que YA existe lanza `FileExistsError`. Esto es bueno: te protege de sobrescribir.
- Si no especificas `encoding`, en Windows leeras tildes mal. SIEMPRE pon `encoding='utf-8'`.
- En modo binario (`'b'`) NO se puede usar `encoding`: trabajas con bytes."""
    )},
]))

plan.append((ID_TABLA_MODOS, [
    {"type": "md", "src": tu_turno(5,
        """Practica los modos. Crea (en orden):

1. Un fichero `res/o_log.txt` con modo `'w'` que contenga `linea inicial\\n`.
2. Abre el MISMO fichero con modo `'a'` (append) y escribe `linea anadida 1\\n` y luego `linea anadida 2\\n`.
3. Abre el fichero con modo `'r'` y muestra todo su contenido.
4. Intenta abrir con modo `'x'`: deberia fallar con `FileExistsError` (capturalo con `try/except` y muestra `'Ya existe'`).
5. Borra el fichero al final."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import os\n# ruta = os.path.join('res', 'o_log.txt')\n#\n# # 1) Crear con 'w' (sobrescribe si existe)\n# with open(ruta, 'w', encoding='utf-8') as f:\n#     f.write('linea inicial\\n')\n#\n# # 2) Anadir con 'a' (NO toca lo previo)\n# with open(ruta, 'a', encoding='utf-8') as f:\n#     f.write('linea anadida 1\\n')\n#     f.write('linea anadida 2\\n')\n#\n# # 3) Leer con 'r'\n# with open(ruta, 'r', encoding='utf-8') as f:\n#     print(f.read())\n#\n# # 4) Intentar 'x' sobre fichero existente\n# try:\n#     with open(ruta, 'x', encoding='utf-8') as f:\n#         f.write('no llegara')\n# except FileExistsError:\n#     print('Ya existe')\n#\n# # 5) Limpieza\n# os.remove(ruta)\n"},
]))

# ============ ESCRITURA ============
plan.append((ID_ESCRITURA, [
    {"type": "md", "src": teoria(
        "Escribir en ficheros: <code>write</code> y <code>writelines</code>",
        """Para escribir en un fichero abierto en modo `'w'`, `'a'` o `'x'`:

#### `.write(string)`

Escribe **un solo string**. Devuelve el numero de caracteres escritos.

```python
with open('out.txt', 'w', encoding='utf-8') as f:
    f.write('Hola\\n')
    f.write('Mundo\\n')
```

> `.write()` **NO anade** salto de linea automatico. Si quieres una linea por escritura, debes incluir tu `\\n`.

#### `.writelines(iterable_de_strings)`

Escribe **una secuencia de strings** uno detras de otro. **TAMPOCO anade `\\n`** entre ellos: tu debes ponerlos.

```python
lineas = ['uno\\n', 'dos\\n', 'tres\\n']
with open('out.txt', 'w', encoding='utf-8') as f:
    f.writelines(lineas)
```

> Pese a su nombre, `writelines` no anade saltos. Si tus strings no terminan en `\\n`, todo se escribe pegado en una sola linea gigante.

#### Truco util: usar `print` con un fichero

`print` tiene un argumento `file` que redirige la salida a un fichero (anadiendo el salto de linea por ti):

```python
with open('out.txt', 'w', encoding='utf-8') as f:
    print('Hola', file=f)
    print('Mundo', file=f)
    print('A=', 5, 'B=', 10, file=f)   # 'A= 5 B= 10'
```

#### Que pasa si escribes en `'r'`?

Error: `io.UnsupportedOperation: not writable`. El fichero esta abierto solo para leer.

#### Anadir vs sobrescribir

| Quiero... | Modo |
|---|---|
| Empezar con un fichero vacio (borrar lo viejo) | `'w'` |
| Conservar lo viejo y anadir al final | `'a'` |
| Que falle si el fichero ya existe | `'x'` |"""
    )},
]))

plan.append((ID_ESCR_USO, [
    {"type": "md", "src": tu_turno(6,
        """Crea un fichero `res/o_tabla.txt` con la **tabla de multiplicar del 7** (del 7x1 al 7x10), una linea por cada producto, con este formato:

```
7 x 1 = 7
7 x 2 = 14
...
7 x 10 = 70
```

Despues lee el fichero y muestralo. Borra el fichero al final.

> Pista: usa un bucle `for i in range(1, 11):` y un f-string."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import os\n# ruta = os.path.join('res', 'o_tabla.txt')\n#\n# # Escritura\n# with open(ruta, 'w', encoding='utf-8') as f:\n#     for i in range(1, 11):\n#         # f-string con el resultado y un salto de linea\n#         f.write(f'7 x {i} = {7 * i}\\n')\n#\n# # Lectura\n# with open(ruta, 'r', encoding='utf-8') as f:\n#     print(f.read())\n#\n# # Limpieza\n# os.remove(ruta)\n"},
]))

# ============ BUFFERING ============
plan.append((ID_BUFFERING, [
    {"type": "md", "src": teoria(
        "Buffering: por que tus datos a veces no aparecen",
        """Cuando llamas a `f.write('hola')`, **Python NO escribe inmediatamente en el disco**. Guarda los datos en un **buffer** (una zona de memoria) y los escribe cuando:

1. El buffer se llena (por defecto, unos KB).
2. Tu llamas a `f.flush()` (forzar escritura).
3. Tu cierras el fichero con `f.close()` o sales del `with`.

#### Por que existe el buffer?

Porque escribir en disco es **mucho mas lento** que escribir en memoria. Si cada `write()` golpeara el disco, el rendimiento seria pesimo. El buffer agrupa varias escrituras y las hace todas de golpe.

#### Cuando me afecta?

```python
f = open('out.txt', 'w', encoding='utf-8')
f.write('hola')
# AQUI: si abres out.txt desde otro programa, esta VACIO.
# Los datos siguen en el buffer.
f.close()
# AHORA: ya esta en disco.
```

#### Como forzar la escritura?

```python
f.flush()       # vacia el buffer al disco SIN cerrar el fichero
f.close()       # vacia el buffer y cierra
```

Si usas `with`, `flush` ocurre automaticamente al salir del bloque.

#### Casos en los que importa

- **Logs en tiempo real:** quieres ver las lineas en cuanto se escriben. Usa `flush=True` en `print()`:
  ```python
  print('avance...', file=f, flush=True)
  ```
- **Procesos largos:** si tu programa se cuelga sin cerrar el fichero, perderas los datos del buffer.
- **Otro programa lee el fichero mientras tu escribes:** usa `flush()` para que vea los cambios."""
    )},
]))

plan.append((ID_BUFF_CODE3, [
    {"type": "md", "src": tu_turno(7,
        """Reproduce el efecto del buffer **a mano**:

1. Abre `res/o_buffer.txt` con `'w'`, escribe `'pendiente'` y NO cierres aun.
2. Abre el mismo fichero con `'r'` y muestra su contenido (lo veras vacio o sin la palabra).
3. Llama a `flush()` sobre el fichero de escritura.
4. Vuelve a leer y muestra el contenido (ahora SI veras `'pendiente'`).
5. Cierra ambos ficheros y borra el archivo."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import os\n# ruta = os.path.join('res', 'o_buffer.txt')\n#\n# # 1) Abrimos para escribir y escribimos sin cerrar\n# fw = open(ruta, 'w', encoding='utf-8')\n# fw.write('pendiente')\n#\n# # 2) Abrimos otro handle para leer (los datos siguen en buffer)\n# fr = open(ruta, 'r', encoding='utf-8')\n# print('Antes de flush:', repr(fr.read()))   # vacio\n#\n# # 3) Forzamos la escritura al disco\n# fw.flush()\n#\n# # 4) Releemos (necesitamos volver al inicio con seek o reabrir)\n# fr.seek(0)\n# print('Despues de flush:', repr(fr.read()))  # 'pendiente'\n#\n# # 5) Cerrar y limpiar\n# fw.close()\n# fr.close()\n# os.remove(ruta)\n"},
]))

# ============ CSV ============
plan.append((ID_CSV, [
    {"type": "md", "src": teoria(
        "CSV: un formato simple para datos tabulares",
        """**CSV** = *Comma-Separated Values*. Es **texto plano** donde cada linea es una fila y los campos van separados por comas (o por `;`, tabuladores...).

#### Ejemplo

```
nombre,edad,ciudad
Ana,30,Madrid
Pedro,25,Barcelona
Lucia,35,Valencia
```

#### Por que NO leer un CSV con `read()` y `split(',')`?

Porque parece simple pero tiene casos peligrosos:
- Un campo puede llevar comas dentro: `"apellido, nombre"` (entre comillas).
- Un campo puede llevar saltos de linea.
- Algunos CSVs usan `;` o `\\t` como separador.
- Los strings se pueden escapar con `""`.

**El modulo `csv` de la libreria estandar** maneja todo eso por ti.

#### Las cuatro herramientas del modulo

| Clase | Para que |
|---|---|
| `csv.reader(f)` | Lee filas como **listas** `['Ana', '30', 'Madrid']` |
| `csv.writer(f)` | Escribe filas pasandole listas |
| `csv.DictReader(f)` | Lee filas como **diccionarios** `{'nombre':'Ana', 'edad':'30', ...}` |
| `csv.DictWriter(f, fieldnames=...)` | Escribe filas pasandole diccionarios |

#### Patron tipico de lectura

```python
import csv

with open('datos.csv', 'r', encoding='utf-8', newline='') as f:
    lector = csv.reader(f)
    cabecera = next(lector)        # primera fila = nombres de columna
    for fila in lector:
        print(fila)                # ['Ana', '30', 'Madrid']
```

#### Patron tipico con DictReader

```python
import csv

with open('datos.csv', 'r', encoding='utf-8', newline='') as f:
    lector = csv.DictReader(f)
    for fila in lector:
        # fila ya es un dict con las claves de la cabecera
        print(fila['nombre'], fila['edad'])
```

#### Patron tipico de escritura

```python
import csv

filas = [
    ['Ana', 30, 'Madrid'],
    ['Pedro', 25, 'Barcelona'],
]

with open('out.csv', 'w', encoding='utf-8', newline='') as f:
    escritor = csv.writer(f)
    escritor.writerow(['nombre', 'edad', 'ciudad'])  # cabecera
    escritor.writerows(filas)                         # todas las filas
```

#### Por que <code>newline=''</code>?

Si NO lo pones, en Windows aparecen **lineas en blanco extra** entre filas. El modulo `csv` ya gestiona los saltos de linea, asi que le decimos a `open` que no transforme nada.

> **Regla de oro:** abre ficheros CSV SIEMPRE con `newline=''` y `encoding='utf-8'`."""
    )},
]))

plan.append((ID_CSV_ESC, [
    {"type": "md", "src": tu_turno(8,
        """Tienes datos de productos. Realiza lo siguiente:

1. Crea una **lista de diccionarios** con 3 productos: cada dict tiene `id`, `nombre`, `precio`.
2. Escribelos en `res/o_productos.csv` usando **`csv.DictWriter`**. Recuerda escribir la cabecera con `.writeheader()`.
3. Vuelve a abrirlo con **`csv.DictReader`** y muestra cada producto en una linea como `{nombre} -> {precio} EUR`.
4. Borra el fichero al final."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import csv, os\n# ruta = os.path.join('res', 'o_productos.csv')\n#\n# productos = [\n#     {'id': 1, 'nombre': 'pan',    'precio': 1.20},\n#     {'id': 2, 'nombre': 'leche',  'precio': 0.95},\n#     {'id': 3, 'nombre': 'huevos', 'precio': 2.50},\n# ]\n#\n# # 1+2) Escritura con DictWriter\n# with open(ruta, 'w', encoding='utf-8', newline='') as f:\n#     campos = ['id', 'nombre', 'precio']\n#     escritor = csv.DictWriter(f, fieldnames=campos)\n#     escritor.writeheader()\n#     escritor.writerows(productos)\n#\n# # 3) Lectura con DictReader\n# with open(ruta, 'r', encoding='utf-8', newline='') as f:\n#     lector = csv.DictReader(f)\n#     for fila in lector:\n#         # ojo: los valores leidos son strings\n#         print(f\"{fila['nombre']} -> {fila['precio']} EUR\")\n#\n# # 4) Limpieza\n# os.remove(ruta)\n"},
]))

# ============ JSON (no esta en el original, lo inyectamos despues de CSV) ============
plan.append((ID_CSV_ESC, [
    {"type": "md", "src": teoria(
        "JSON: el formato estrella para datos estructurados",
        """**JSON** = *JavaScript Object Notation*. Es un formato de texto que se ha convertido en el estandar para intercambiar datos entre sistemas (APIs web, configuracion, almacenamiento ligero).

#### Por que es popular?

- Es **legible por humanos**.
- Mapea **directamente** a tipos basicos de Python (dict, list, str, int, float, bool, None).
- Lo entienden practicamente todos los lenguajes de programacion.

#### Equivalencias JSON <-> Python

| JSON | Python |
|---|---|
| `{"a": 1}` | `dict` |
| `[1, 2, 3]` | `list` |
| `"hola"` | `str` |
| `42` / `3.14` | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

> **Cuidado:** JSON usa `true`/`false`/`null` en minuscula. Python usa `True`/`False`/`None`. El modulo `json` traduce por ti.

#### Las cuatro funciones del modulo `json`

| Funcion | Que hace | Trabaja con |
|---|---|---|
| `json.dumps(obj)` | Convierte un objeto Python a string JSON | string |
| `json.loads(string)` | Convierte un string JSON a objeto Python | string |
| `json.dump(obj, f)` | Convierte y **escribe** en un fichero abierto | fichero |
| `json.load(f)` | **Lee** un fichero y convierte a objeto Python | fichero |

> Nemotecnia: las que terminan en `s` trabajan con **s**trings. Las otras con ficheros.

#### Ejemplos

```python
import json

datos = {
    'nombre': 'Ana',
    'edad': 30,
    'aficiones': ['leer', 'correr'],
    'casado': False,
    'hijos': None,
}

# 1) A string
texto = json.dumps(datos, ensure_ascii=False, indent=2)
print(texto)

# 2) De string a objeto
obj = json.loads('{"a": 1, "b": [10, 20]}')
print(obj['b'][1])   # 20

# 3) Escribir a fichero
with open('datos.json', 'w', encoding='utf-8') as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)

# 4) Leer desde fichero
with open('datos.json', 'r', encoding='utf-8') as f:
    leido = json.load(f)
print(leido['nombre'])
```

#### Argumentos utiles

| Argumento | Para que |
|---|---|
| `indent=2` | Formatea el JSON con sangrias bonitas (legible). Sin esto, todo en una linea. |
| `ensure_ascii=False` | Permite caracteres no ASCII (utiles para utf-8). Por defecto, escapa todo a `\\u00...`. |
| `sort_keys=True` | Ordena las claves alfabeticamente. |
| `default=str` | Convierte tipos no serializables (ej: `datetime`) llamando a `str(obj)`. |

#### Limitaciones de JSON

JSON **NO sabe** serializar:
- Tuplas (las convierte a listas).
- Sets, datetime, objetos personalizados.
- Funciones, clases.

Para esas cosas necesitas `pickle` o convertir manualmente."""
    )},
    {"type": "md", "src": tu_turno(9,
        """Crea un diccionario `usuario` con estas claves: `nombre`, `edad`, `intereses` (lista de strings), `activo` (bool), `apellido_segundo` (None).

1. Escribelo a `res/o_usuario.json` con **`json.dump`**, `indent=2` y `ensure_ascii=False`.
2. Vuelve a leerlo con **`json.load`** y comprueba que `type(leido)` es `dict`.
3. Imprime el JSON resultante usando **`json.dumps(leido, indent=2)`** para ver el formato bonito.
4. Borra el fichero."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import json, os\n# ruta = os.path.join('res', 'o_usuario.json')\n#\n# usuario = {\n#     'nombre': 'Ana',\n#     'edad': 30,\n#     'intereses': ['leer', 'correr', 'python'],\n#     'activo': True,\n#     'apellido_segundo': None,\n# }\n#\n# # 1) Escribir a fichero\n# with open(ruta, 'w', encoding='utf-8') as f:\n#     json.dump(usuario, f, indent=2, ensure_ascii=False)\n#\n# # 2) Leer de fichero\n# with open(ruta, 'r', encoding='utf-8') as f:\n#     leido = json.load(f)\n# print('Tipo leido:', type(leido))     # <class 'dict'>\n#\n# # 3) Bonito\n# print(json.dumps(leido, indent=2, ensure_ascii=False))\n#\n# # 4) Limpieza\n# os.remove(ruta)\n"},
    {"type": "md", "src": teoria(
        "Pickle: serializar CUALQUIER objeto Python",
        """**Pickle** es la solucion de Python para guardar y cargar **objetos arbitrarios** (incluyendo cosas que JSON no puede manejar como tuplas, sets, objetos de clases personalizadas, modelos de machine learning entrenados, etc.).

#### JSON vs Pickle

| Aspecto | JSON | Pickle |
|---|---|---|
| Formato | Texto legible | Binario (no humano) |
| Portable a otros lenguajes | Si | **NO** (solo Python) |
| Tipos soportados | Basicos | **Casi todo** |
| Seguridad | Seguro | **PELIGROSO** (codigo arbitrario) |
| Velocidad | Mas lento | Rapido |
| Uso tipico | APIs, config | Cache, modelos ML |

#### CUIDADO con la seguridad

**NUNCA cargues un fichero pickle de origen desconocido.** Pickle puede ejecutar codigo Python arbitrario al deserializar. Si alguien malicioso te pasa un .pkl, puede tomar control de tu maquina.

#### Las cuatro funciones del modulo `pickle`

| Funcion | Que hace |
|---|---|
| `pickle.dumps(obj)` | Serializa a bytes (no a string) |
| `pickle.loads(b)` | Deserializa de bytes |
| `pickle.dump(obj, f)` | Serializa y escribe a fichero (modo `'wb'`) |
| `pickle.load(f)` | Lee y deserializa de fichero (modo `'rb'`) |

> Pickle trabaja con **BYTES**, no con texto. Por eso los modos son `'wb'` y `'rb'`. NO uses `encoding`.

#### Ejemplos

```python
import pickle

datos = {
    'tupla': (1, 2, 3),       # JSON la convertiria en lista
    'set': {10, 20, 30},      # JSON no puede manejar sets
    'lista_anidada': [[1, 2], [3, 4]],
}

# 1) Escribir a fichero (modo binario!)
with open('datos.pkl', 'wb') as f:
    pickle.dump(datos, f)

# 2) Leer de fichero
with open('datos.pkl', 'rb') as f:
    leido = pickle.load(f)

print(type(leido['tupla']))   # <class 'tuple'>  (mantiene el tipo)
print(type(leido['set']))     # <class 'set'>
```

#### Cuando usar pickle?

- **Cache de calculos largos:** computar algo lento una vez, guardarlo, recuperarlo en proximas ejecuciones.
- **Modelos de Machine Learning:** despues de entrenar `model.fit(...)`, guardar con `pickle.dump(model, f)` y cargarlo en produccion.
- **Estado intermedio de un programa.**

#### Cuando NO usar pickle?

- Para compartir datos con otros lenguajes (usa JSON o CSV).
- Para configuracion editable a mano (usa JSON o YAML).
- Para datos de fuente no confiable (peligro de codigo malicioso)."""
    )},
    {"type": "md", "src": tu_turno(10,
        """Crea un objeto Python con tipos que JSON NO sabria manejar:

```python
mi_objeto = {
    'tupla': (1, 2, 3),
    'conjunto': {10, 20, 30},
    'matriz': [[1, 2], [3, 4]],
}
```

1. Guardalo en `res/o_objeto.pkl` usando **`pickle.dump`** (modo `'wb'`).
2. Vuelve a cargarlo con **`pickle.load`** (modo `'rb'`).
3. Comprueba que `type(leido['tupla']) is tuple` y `type(leido['conjunto']) is set` (los tipos se mantienen, a diferencia de JSON).
4. Borra el fichero al final."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import pickle, os\n# ruta = os.path.join('res', 'o_objeto.pkl')\n#\n# mi_objeto = {\n#     'tupla': (1, 2, 3),\n#     'conjunto': {10, 20, 30},\n#     'matriz': [[1, 2], [3, 4]],\n# }\n#\n# # 1) Escribimos a fichero EN MODO BINARIO ('wb')\n# with open(ruta, 'wb') as f:\n#     pickle.dump(mi_objeto, f)\n#\n# # 2) Leemos de fichero EN MODO BINARIO ('rb')\n# with open(ruta, 'rb') as f:\n#     leido = pickle.load(f)\n#\n# # 3) Comprobamos que los tipos se han conservado\n# print(type(leido['tupla']) is tuple)       # True\n# print(type(leido['conjunto']) is set)      # True\n# print(leido)\n#\n# # 4) Limpieza\n# os.remove(ruta)\n"},
    {"type": "md", "src": dato(
        """**Resumen visual: que formato elegir?**

| Tienes... | Quieres... | Usa |
|---|---|---|
| Datos tabulares (filas y columnas) | Compartir con Excel / R / otros | **CSV** |
| Diccionario / lista de tipos basicos | API web / configuracion legible | **JSON** |
| Objeto Python complejo (tuplas, sets, modelos ML, clases) | Solo Python -> Python | **Pickle** |
| Texto libre (logs, notas) | Lectura humana | **TXT** plano |
| Imagen / audio / pdf | Almacenar tal cual | **modo binario `'rb'`/`'wb'`** |"""
    )},
]))

# ============ EJERCICIOS FINAL ============
plan.append((ID_EJ3, [
    {"type": "md", "src": teoria(
        "Resumen final y patron canonico",
        """Si te quedas con UNA sola idea de esta clase, que sea esta:

```python
from pathlib import Path
import json   # o csv, o pickle, segun el caso

ruta = Path('res') / 'datos.json'

# LECTURA
with open(ruta, 'r', encoding='utf-8') as f:
    datos = json.load(f)

# ... trabajar con datos ...

# ESCRITURA
ruta_salida = Path('res') / 'salida.json'
with open(ruta_salida, 'w', encoding='utf-8') as f:
    json.dump(datos, f, indent=2, ensure_ascii=False)
```

**Checklist al manipular ficheros:**

- [ ] Uso `with` (cierra automaticamente).
- [ ] Especifico `encoding='utf-8'` para texto.
- [ ] Para CSV anado `newline=''`.
- [ ] Para binarios uso `'rb'` / `'wb'` (sin encoding).
- [ ] No uso `'w'` accidentalmente cuando queria `'a'` (sobrescribir vs anadir).
- [ ] Manejo errores comunes con `try/except`: `FileNotFoundError`, `PermissionError`, `IsADirectoryError`.
- [ ] Para datos tabulares uso `csv`. Para datos estructurados, `json`. Para objetos Python, `pickle`."""
    )},
    {"type": "md", "src": tu_turno(11,
        """**Ejercicio integrador.** Tienes que construir una mini-pipeline:

1. Define una **lista de diccionarios** con 3 alumnos: cada uno con `id`, `nombre`, `notas` (lista de 3 enteros).
2. Calcula la nota **media** de cada alumno y anadela a su dict como clave `media`.
3. Guarda la lista resultante en `res/o_alumnos.json` (con `indent=2`).
4. Tambien escribe una version CSV en `res/o_alumnos.csv` con columnas `id,nombre,media` (sin la lista `notas`). Usa `csv.DictWriter`.
5. Vuelve a leer el JSON y muestra los alumnos cuya media sea **>= 7**.
6. Borra los dos ficheros."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import json, csv, os\n#\n# # 1) Datos de partida\n# alumnos = [\n#     {'id': 1, 'nombre': 'Ana',   'notas': [8, 9, 7]},\n#     {'id': 2, 'nombre': 'Pedro', 'notas': [5, 6, 4]},\n#     {'id': 3, 'nombre': 'Lucia', 'notas': [9, 9, 10]},\n# ]\n#\n# # 2) Calculamos la media\n# for a in alumnos:\n#     a['media'] = sum(a['notas']) / len(a['notas'])\n#\n# # 3) Guardar a JSON\n# ruta_json = os.path.join('res', 'o_alumnos.json')\n# with open(ruta_json, 'w', encoding='utf-8') as f:\n#     json.dump(alumnos, f, indent=2, ensure_ascii=False)\n#\n# # 4) Guardar a CSV (sin la lista 'notas')\n# ruta_csv = os.path.join('res', 'o_alumnos.csv')\n# with open(ruta_csv, 'w', encoding='utf-8', newline='') as f:\n#     escritor = csv.DictWriter(f, fieldnames=['id', 'nombre', 'media'])\n#     escritor.writeheader()\n#     for a in alumnos:\n#         # Solo las columnas que queremos\n#         escritor.writerow({'id': a['id'], 'nombre': a['nombre'], 'media': a['media']})\n#\n# # 5) Releemos JSON y filtramos\n# with open(ruta_json, 'r', encoding='utf-8') as f:\n#     leido = json.load(f)\n# aprobados = [a for a in leido if a['media'] >= 7]\n# print('Alumnos con media >= 7:')\n# for a in aprobados:\n#     print(f\"  {a['nombre']}: {a['media']:.2f}\")\n#\n# # 6) Limpieza\n# os.remove(ruta_json)\n# os.remove(ruta_csv)\n"},
]))


enhance(NB, plan)
print("Done.")

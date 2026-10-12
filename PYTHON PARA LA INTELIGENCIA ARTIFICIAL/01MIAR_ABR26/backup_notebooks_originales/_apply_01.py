"""Aplica mejoras al notebook 01_Python101 con bloques de colores."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, solucion_md

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_01_Python101.ipynb"

# IDs originales (UUIDs largos del notebook 01)
ID_IMPORT_THIS    = "57222417-fed9-4ceb-a527-0bced0977a17"
ID_HELLO_WORLD    = "fc73d7ed-ede9-4fb4-91f2-4cc43f9b02a0"
ID_COMENTARIOS    = "dd43110c-e253-40af-9c94-20e05318bb39"
ID_NUMPY_DATA     = "ffa0b467-500f-423f-a4ad-9bdf224e5f4e"
ID_TIME_PERF      = "878fedc5-c064-4bb4-9e8d-649f72d6f3a5"
ID_PRINCIPALES    = "3fbe0887-17fd-4050-86c8-4620ade0d3f6"  # caracteristicas


plan = []

# -------- Despues del titulo "Principales caracteristicas" --------
plan.append((ID_PRINCIPALES, [
    {"type": "md", "src": teoria(
        "Que significa cada caracteristica en la practica?",
        """La lista que ves arriba es densa. Vamos a desempacarla con palabras simples:

- **Lenguaje de proposito general**: sirve para web, ciencia de datos, automatizacion, IA, scripts, etc. No esta atado a un solo dominio.

- **Interpretado, no compilado**: tu codigo se traduce y ejecuta linea a linea. **Ventaja:** lo cambias y vuelves a correr al instante. **Desventaja:** mas lento que C/C++ en bucles puros (por eso usaremos NumPy luego).

- **Tipado dinamico**: NO declaras el tipo de las variables. `x = 5` y luego `x = "hola"` esta permitido.

- **Tipado fuerte**: PERO Python no convierte tipos por ti. `"5" + 3` lanza error (en JavaScript daria `"53"`). Esto evita bugs raros.

- **Enfasis en la legibilidad**: la indentacion es obligatoria, no opcional. El codigo Python tiende a leerse casi como ingles.

- **Multiparadigma**: puedes escribir codigo procedural (paso a paso), orientado a objetos (clases) o funcional (funciones puras). Lo veras en las clases 06 y 07.

- **Indentacion para delimitar bloques**: en Java/C usan llaves `{ }`, en Python usan los **espacios** (4 por convencion). No es un capricho: te obliga a escribir codigo limpio.

- **Gestion automatica de memoria**: tu no haces `malloc`/`free` ni te preocupas por la RAM. Python tiene un *garbage collector* que limpia lo que ya no usas.

- **Multiplataforma**: el mismo `.py` corre en Windows, macOS y Linux sin cambios.
"""
    )},
]))

# -------- Despues de import this --------
plan.append((ID_IMPORT_THIS, [
    {"type": "md", "src": teoria(
        "Que es 'import this'?",
        """`import this` es una **broma seria**: al ejecutarlo Python imprime el **Zen de Python**, una lista de 19 reglas no oficiales que guian el estilo del lenguaje.

Las reglas mas utiles para ti hoy:

- **Beautiful is better than ugly** -> codigo bonito > codigo feo.
- **Explicit is better than implicit** -> mejor decir las cosas de forma clara que magia escondida.
- **Simple is better than complex** -> empieza simple, complica solo si hace falta.
- **Readability counts** -> escribes codigo para HUMANOS (incluido tu yo del futuro), no solo para la maquina.
- **There should be one obvious way to do it** -> en Python suele haber una unica forma idiomatica de hacer algo.

Estas reglas NO son sintaxis ni rules de compilacion. Son una **filosofia** que te ayudara a escribir codigo que otros (y tu) puedan leer."""
    )},
    {"type": "md", "src": tu_turno(1,
        """Ejecuta `import this` en la celda anterior si aun no lo has hecho. Despues, en la siguiente celda, **escribe un comentario** (linea con `#`) explicando con tus palabras cual de las reglas del Zen te parece mas util y por que."""
    )},
    {"type": "code", "src": "# Escribe aqui tu reflexion (con #):\n\n"},
    {"type": "code", "src": "# === Solucion sugerida (un ejemplo posible) ===\n# # 'Readability counts' es la mas util porque me obliga\n# # a pensar en la persona que leera el codigo despues, no solo\n# # en hacer que funcione hoy.\n"},
]))

# -------- Despues de print('Hello World') --------
plan.append((ID_HELLO_WORLD, [
    {"type": "md", "src": teoria(
        "Que hizo <code>print(...)</code> realmente?",
        """`print()` es una **funcion incorporada** (built-in) de Python que **escribe en la salida estandar** (lo que ves en la consola o debajo de la celda).

Cosas que vale la pena saber:

```python
print('Hola')                  # texto literal
print('Hola', 'mundo')         # varios valores separados por coma
print('a', 'b', sep='-')       # personalizar separador -> a-b
print('Linea 1', end=' ')      # NO saltar de linea al final
print('Linea 2')               # -> Linea 1 Linea 2

print(1 + 2)                   # tambien imprime el resultado de calculos
print(type(42))                # imprime <class 'int'>
```

**Por que es la primera funcion que aprendes?** Porque hasta que no aprendes a *ver* lo que tu codigo esta haciendo, no puedes depurarlo. `print` es tu microscopio."""
    )},
    {"type": "md", "src": tu_turno(2,
        """Crea dos variables: `nombre` (con tu nombre) y `lenguaje` (con `'Python'`). Despues, con UNA sola llamada a `print(...)`, muestra el texto:

```
NOMBRE esta aprendiendo Python
```

Pista: pasa varios argumentos a `print` separados por coma, o usa una **f-string**."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# nombre = 'Lucas'\n# lenguaje = 'Python'\n# print(nombre, 'esta aprendiendo', lenguaje)\n# # o:\n# print(f'{nombre} esta aprendiendo {lenguaje}')\n"},
]))

# -------- Despues de comentarios --------
plan.append((ID_COMENTARIOS, [
    {"type": "md", "src": teoria(
        "Comentarios en Python",
        """Los **comentarios** son texto que Python **ignora al ejecutar**. Sirven solo para los humanos que leen el codigo.

```python
# Esto es un comentario de UNA linea (con almohadilla)

x = 5  # tambien puede ir al final de una linea

'''
Esto es una cadena de TRES comillas. Tecnicamente NO es un
comentario (es un string), pero Python no la asigna a nada
asi que actua como uno. Se usa mucho para documentacion.
'''
```

**Buena practica (PEP 8):**
- Explica el **POR QUE**, no el **QUE**. El codigo ya dice que hace.
- Manten los comentarios actualizados. Un comentario obsoleto miente.
- Codigo claro > muchos comentarios. Si necesitas explicar mucho, quiza el codigo necesita refactor.

```python
# MAL:
x = x + 1  # suma 1 a x         <- obvio, no aporta nada

# BIEN:
x = x + 1  # avanzamos al siguiente fotograma del video
```"""
    )},
    {"type": "md", "src": tu_turno(3,
        """En la siguiente celda escribe:
1. Una variable `precio = 100`.
2. Una variable `precio_con_iva = precio * 1.21`.
3. Un comentario al lado de la segunda linea explicando POR QUE multiplicas por 1.21.
4. Un `print(precio_con_iva)`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# precio = 100\n# precio_con_iva = precio * 1.21  # IVA Espana = 21%\n# print(precio_con_iva)\n"},
]))

# -------- Despues del bloque NumPy data --------
plan.append((ID_NUMPY_DATA, [
    {"type": "md", "src": teoria(
        "Por que comparar NumPy con listas Python?",
        """Estas dos lineas crean **lo mismo conceptualmente**: una secuencia de 10 millones de numeros del 0 al 9999999.

Pero por dentro son **muy distintas**:

| Aspecto | `list(range(...))` | `np.arange(...)` |
|---|---|---|
| Tipo de dato | Lista heterogenea | Array homogeneo (int64 fijo) |
| Memoria | Cada elemento es un objeto Python (~28 bytes) | Numeros raw uno detras de otro |
| Operaciones | Bucles Python (lentos) | Operaciones vectorizadas en C (rapidas) |

En la siguiente celda mediremos los tiempos de la **misma** operacion (`* 2` repetida 10 veces) sobre cada uno. Veras que NumPy es **decenas de veces** mas rapido. En IA, donde manejamos millones de datos, esa diferencia es lo que hace que entrenar un modelo dure 1 hora en vez de 10 dias."""
    )},
]))

# -------- Despues del benchmark de tiempo --------
plan.append((ID_TIME_PERF, [
    {"type": "md", "src": teoria(
        "Que es <code>%time</code>?",
        """`%time` es un **comando magico** de Jupyter (no es Python puro). Mide cuanto tarda en ejecutarse la siguiente linea.

```python
%time tu_codigo()         # mide UNA linea
%%time                    # mide la celda entera (va al inicio de la celda)
```

En el ejemplo de arriba veras dos numeros importantes:

- **CPU times**: tiempo que el procesador estuvo ocupado.
- **Wall time**: tiempo de reloj (lo que tardo en la realidad).

Normalmente miraras el **Wall time** porque es el que sientes."""
    )},
    {"type": "md", "src": tu_turno(4,
        """En la siguiente celda:
1. Crea un array NumPy llamado `nums` con `np.arange(1_000_000)`.
2. Usa `%time` para medir cuanto tarda en calcular `nums ** 2` (eleva al cuadrado todos los numeros)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# nums = np.arange(1_000_000)\n# %time _ = nums ** 2\n"},
]))


enhance(NB, plan)
print("Done.")

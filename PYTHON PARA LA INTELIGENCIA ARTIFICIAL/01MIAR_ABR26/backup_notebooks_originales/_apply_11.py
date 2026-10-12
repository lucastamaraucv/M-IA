"""Aplica mejoras al notebook 11_Visualization con bloques de colores y teoria detallada."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, solucion_md, dato, aviso

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_11_Visualization.ipynb"

import json
nb = json.load(open(NB, encoding="utf-8"))

def find_id(text_fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if text_fragment in src:
            return c["id"]
    return None

# Anchors estables (IDs reales del notebook)
ID_TITULO       = "cell000-b87092bf"   # portada
ID_ELEMENTOS    = "cell004-366f5627"   # Elementos de visualizacion
ID_PRIMERPLOT   = "cell007-53223f04"   # plot(data) y show()
ID_FIGAXES      = "cell013-d728f8a0"   # figure, axes (anatomia)
ID_PLOT_PARAMS  = "cell020-0074352c"   # .plot() multiples parametros
ID_DECORADORES  = "cell025-605c2982"   # Decoradores
ID_ANOTACIONES  = "cell026-8b5ad193"   # Anotaciones
ID_TIPOS_GRAF   = "cell029-b7fc451d"   # Tipos de graficos
ID_GRABAR       = "cell034-661f2216"   # Grabar a archivo
ID_PANDAS_PLOT  = "cell036-d594d581"   # Representacion en pandas
ID_FRAMEPLOT    = "cell038-a5ee6ae2"   # frame.plot() parametros
ID_SEABORN      = "cell045-5e006f82"   # Seaborn
ID_RELACIONES   = "cell053-74657b33"   # Relaciones entre variables
ID_DISTRIB      = "cell058-1b749623"   # Distribucion
ID_CORREL       = "cell066-a99e047a"   # Visualizacion de correlaciones
ID_EJERCICIOS   = "cell071-37dc1532"   # Ejercicios

plan = []

# -------- INTRO al notebook --------
plan.append((ID_TITULO, [
    {"type": "md", "src": teoria(
        "Como leer este notebook (version mejorada)",
        """Este notebook fue **enriquecido** con bloques de colores para que aprendas haciendo:

<div style="background-color:#e7f5ff;border-left:6px solid #1c7ed6;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AZUL = TEORIA</b></div> -> explicacion antes de cada concepto.

<div style="background-color:#fff9db;border-left:6px solid #f59f00;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AMARILLO = TU TURNO</b></div> -> ejercicio que TU resuelves en la celda vacia.

<div style="background-color:#ebfbee;border-left:6px solid #2f9e44;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>VERDE = SOLUCION</b></div> -> codigo de referencia comentado por si te trabas.

<div style="background-color:#fff0f0;border-left:6px solid #e03131;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>ROJO = CUIDADO</b></div> -> trampas y errores frecuentes.

<div style="background-color:#f3f0ff;border-left:6px solid #7048e8;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>VIOLETA = PARA RECORDAR</b></div> -> resumen para llevar.

> **El codigo y la teoria del profesor original NO se han tocado**. Solo se han ANADIDO bloques nuevos. Puedes seguir comparando con la version original en `backup_notebooks_originales/`."""
    )},
    {"type": "md", "src": teoria(
        "Por que invertimos tiempo en visualizar?",
        """Una imagen comunica patrones que una tabla esconde. Antes de modelar **cualquier** problema de IA, conviene **MIRAR** los datos.

#### Anscombe's Quartet (la ilustracion clasica)
Cuatro datasets distintos pueden tener **la misma media, varianza, correlacion y recta de regresion**, pero al graficarlos descubres que uno es lineal, otro curvo, otro tiene un outlier brutal y otro es vertical. **Solo verlos lo revela**.

#### Para que sirve la visualizacion en este curso

| Fase del proyecto | Que graficas | Para que |
|---|---|---|
| EDA (analisis exploratorio) | histogramas, boxplots, scatter | Detectar outliers, distribuciones, relaciones |
| Modelado | curvas de aprendizaje, residuos | Ver si el modelo aprende y donde falla |
| Comunicacion | barras, lineas, mapas | Contar la historia a un humano no tecnico |

#### El stack que veras en este notebook

| Libreria | Nivel | Para que |
|---|---|---|
| **matplotlib** | Bajo | Control total. La base de todo. |
| **pandas.plot** | Medio | Atajo cuando ya tienes un DataFrame. |
| **seaborn** | Alto | Graficos estadisticos bonitos en una linea. |

Las tres se llevan bien y se mezclan: seaborn produce objetos matplotlib, asi que puedes seguir customizando con `plt.title(...)` despues de un `sns.something(...)`."""
    )},
]))

# ============ ELEMENTOS DE VISUALIZACION ============
plan.append((ID_ELEMENTOS, [
    {"type": "md", "src": teoria(
        "Anatomia de un grafico matplotlib (Figure, Axes, Axis)",
        """Esta es la jerarquia que **DEBES** memorizar. Te ahorrara horas de confusion.

```
+------------------------------------------------+
|  Figure  (el lienzo entero, lo que se exporta) |
|  +------------------+  +------------------+    |
|  |  Axes (subplot)  |  |  Axes (subplot)  |    |
|  |  - Axis x        |  |  - Axis x        |    |
|  |  - Axis y        |  |  - Axis y        |    |
|  |  - title, lines  |  |  - title, lines  |    |
|  +------------------+  +------------------+    |
+------------------------------------------------+
```

| Concepto | Que es | Lo creas con |
|---|---|---|
| **Figure** | El lienzo completo (la "ventana"). | `plt.figure()` o `plt.subplots(...)` |
| **Axes** | UN grafico (un panel con sus ejes). NO confundir con plural de Axis. | `fig.add_subplot()` o `plt.subplots(...)` |
| **Axis** | UN eje individual (X o Y). | `ax.xaxis`, `ax.yaxis` |
| **Artist** | Cualquier cosa dibujable (linea, texto, leyenda). | `ax.plot(...)`, `ax.text(...)` |

#### Una figura puede tener N Axes (subplots)

```python
fig, ax = plt.subplots()             # 1 figura, 1 axes
fig, axes = plt.subplots(2, 3)       # 1 figura, 2x3 = 6 axes (un ndarray)
fig, (ax1, ax2) = plt.subplots(1, 2) # desempaquetando
```

> Truco mental: **Figure es el folio. Axes son cada uno de los recuadros que pintas en el folio.**"""
    )},
    {"type": "md", "src": teoria(
        "Dos estilos: <code>plt.</code> (estado) vs orientado a objetos (OO)",
        """Existen **dos formas equivalentes** de usar matplotlib. Verlas claras te evitara una vida de copia-pega.

#### Estilo 1: <code>pyplot</code> (estilo MATLAB, basado en estado)

```python
plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])
plt.title('Titulo')
plt.xlabel('x')
plt.show()
```

`plt` mantiene una **figura activa** por debajo. Comodo para scripts cortos en Jupyter.

#### Estilo 2: orientado a objetos (RECOMENDADO)

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_title('Titulo')
ax.set_xlabel('x')
plt.show()
```

Trabajas con los objetos `fig` y `ax` directamente. **Imprescindible** cuando hay varios subplots.

| Estilo | Cuando usarlo |
|---|---|
| `plt.algo(...)` | Graficos de una sola panel, scripts rapidos |
| `ax.set_algo(...)` | Subplots multiples, codigo reutilizable, librerias |

| pyplot (estado) | OO (objetos) |
|---|---|
| `plt.title('x')` | `ax.set_title('x')` |
| `plt.xlabel('x')` | `ax.set_xlabel('x')` |
| `plt.ylabel('y')` | `ax.set_ylabel('y')` |
| `plt.xlim(0, 10)` | `ax.set_xlim(0, 10)` |
| `plt.xticks([...])` | `ax.set_xticks([...])` |
| `plt.legend()` | `ax.legend()` |

> Regla: **mientras puedas, usa el estilo OO**. Es mas explicito y crece bien."""
    )},
]))

plan.append((ID_PRIMERPLOT, [
    {"type": "md", "src": dato(
        """**`plt.show()` muestra TODO lo que hay pendiente** en la figura activa y la cierra. En notebooks Jupyter con `%matplotlib inline` funciona automaticamente al final de la celda, pero es buena practica llamarlo explicitamente.

Si te aparece `<Figure size ...>` repetido en la salida, es que se imprime el `repr` del objeto. Llama a `plt.show()` o asigna a `_` para silenciarlo."""
    )},
    {"type": "md", "src": tu_turno(1,
        """Crea un array `x = np.arange(0, 20)` y otro `y = x ** 2`. Dibuja la curva con `plt.plot(x, y)` y muestra el grafico. Anade un titulo `'Mi primer grafico'` con `plt.title(...)`.

Este es el "Hola Mundo" de matplotlib."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# import matplotlib.pyplot as plt\n#\n# # 1) preparamos datos\n# x = np.arange(0, 20)        # [0, 1, ..., 19]\n# y = x ** 2                  # parabola\n#\n# # 2) graficamos\n# plt.plot(x, y)\n# plt.title('Mi primer grafico')\n# plt.xlabel('x')\n# plt.ylabel('x al cuadrado')\n# plt.show()\n"},
]))

# ============ FIGURE / AXES ============
plan.append((ID_FIGAXES, [
    {"type": "md", "src": teoria(
        "<code>plt.subplots()</code>: la funcion que mas vas a usar",
        """`plt.subplots(filas, columnas)` crea una **Figure** y un **array de Axes** de una sola vez. Es la forma idiomatica.

```python
fig, ax = plt.subplots()                # 1 axes
fig, axes = plt.subplots(2, 3)          # 6 axes en grid 2x3
fig, axes = plt.subplots(1, 2,
                         figsize=(10,4),# tamano en pulgadas
                         sharey=True)   # comparte eje Y
```

#### Acceso a los axes

| Caso | Como acceder |
|---|---|
| 1x1 | `ax` (es un objeto unico) |
| 1xN o Nx1 | `axes[i]` (es un array 1D) |
| MxN | `axes[i, j]` (es un array 2D) |

```python
fig, axes = plt.subplots(2, 3)
axes[0, 0].plot(...)   # esquina superior izq
axes[1, 2].bar(...)    # esquina inferior dcha
```

#### Layouts comunes que vas a necesitar

```python
# Mismos limites de Y para comparar
fig, axes = plt.subplots(1, 3, sharey=True)

# Solo eje X comun (sirve para series de tiempo apiladas)
fig, axes = plt.subplots(3, 1, sharex=True)

# Ratios distintos entre subplots (uno mas grande)
fig, axes = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})
```

#### `fig.tight_layout()` y `figsize`

- `figsize=(ancho, alto)` en pulgadas (a 100 dpi -> pixeles).
- `fig.tight_layout()` elimina solapamientos entre titulos y etiquetas. Llamalo **al final**, antes de `plt.show()`."""
    )},
    {"type": "md", "src": tu_turno(2,
        """Crea una figura `2x2` con `plt.subplots(2, 2, figsize=(10, 8))`. En cada subplot pinta una funcion distinta usando `x = np.linspace(0, 10, 100)`:

| Posicion | Funcion |
|---|---|
| `[0,0]` | `np.sin(x)` |
| `[0,1]` | `np.cos(x)` |
| `[1,0]` | `x ** 2` |
| `[1,1]` | `np.exp(x / 5)` |

Anade a cada uno un titulo y llama a `fig.tight_layout()` antes de `plt.show()`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# import matplotlib.pyplot as plt\n#\n# # 1) datos en eje X\n# x = np.linspace(0, 10, 100)\n#\n# # 2) figura 2x2\n# fig, axes = plt.subplots(2, 2, figsize=(10, 8))\n#\n# # 3) cada subplot con su funcion y titulo\n# axes[0, 0].plot(x, np.sin(x))\n# axes[0, 0].set_title('seno')\n#\n# axes[0, 1].plot(x, np.cos(x))\n# axes[0, 1].set_title('coseno')\n#\n# axes[1, 0].plot(x, x ** 2)\n# axes[1, 0].set_title('x al cuadrado')\n#\n# axes[1, 1].plot(x, np.exp(x / 5))\n# axes[1, 1].set_title('exponencial')\n#\n# # 4) evita solapamientos y muestra\n# fig.tight_layout()\n# plt.show()\n"},
]))

# ============ PLOT PARAMS ============
plan.append((ID_PLOT_PARAMS, [
    {"type": "md", "src": teoria(
        "Customizacion: color, marker, linestyle, label, alpha",
        """Cualquier llamada a `plot(...)` acepta multiples parametros que controlan la apariencia. Memoriza los siete que mas vas a usar.

| Parametro | Que controla | Ejemplos |
|---|---|---|
| `color` o `c` | Color de la linea | `'red'`, `'#1f77b4'`, `(0.2, 0.4, 0.6)` |
| `linestyle` o `ls` | Tipo de linea | `'-'`, `'--'`, `'-.'`, `':'` |
| `linewidth` o `lw` | Grosor | `1`, `2.5` |
| `marker` | Forma de los puntos | `'o'`, `'s'`, `'^'`, `'x'` |
| `markersize` o `ms` | Tamano del marker | `4`, `10` |
| `label` | Texto en la leyenda | `'ventas 2024'` |
| `alpha` | Transparencia | `0.0` a `1.0` |

#### El atajo de tres caracteres: `'rs--'`

Tres simbolos juntos = `[color][marker][line]`:

```python
ax.plot(x, y, 'rs--')   # red squares con linea discontinua
ax.plot(x, y, 'go-')    # green circles con linea solida
ax.plot(x, y, 'b^:')    # blue triangles con linea de puntos
```

Equivalente a:
```python
ax.plot(x, y, color='red', marker='s', linestyle='--')
```

> Es comodo pero se lee peor. Para codigo serio prefiere los nombres completos.

#### Leyenda: para que sirva, todo `plot` debe tener `label=...`

```python
ax.plot(x, y1, label='ventas 2023')
ax.plot(x, y2, label='ventas 2024')
ax.legend(loc='best')   # 'best', 'upper right', 'lower left', etc.
```

Si no pones `label`, la curva no aparecera en la leyenda."""
    )},
]))

# ============ DECORADORES (titles, ticks, lim) ============
plan.append((ID_DECORADORES, [
    {"type": "md", "src": teoria(
        "Customizacion estructural: title, labels, xlim/ylim, xticks",
        """Los **decoradores** del Axes controlan el contexto del grafico. Son los metodos `set_*` mas usados.

#### Tabla de bolsillo (estilo OO)

| Que quiero | Metodo | Ejemplo |
|---|---|---|
| Titulo del grafico | `ax.set_title(...)` | `ax.set_title('Ventas 2024')` |
| Etiqueta eje X | `ax.set_xlabel(...)` | `ax.set_xlabel('Mes')` |
| Etiqueta eje Y | `ax.set_ylabel(...)` | `ax.set_ylabel('EUR')` |
| Limites eje X | `ax.set_xlim(...)` | `ax.set_xlim(0, 12)` |
| Limites eje Y | `ax.set_ylim(...)` | `ax.set_ylim(-1, 1)` |
| Ticks eje X | `ax.set_xticks(...)` | `ax.set_xticks([0, 3, 6, 9, 12])` |
| Etiquetas de ticks | `ax.set_xticks(pos, labels=...)` | `ax.set_xticks([0,1], labels=['A','B'])` |
| Rejilla | `ax.grid(...)` | `ax.grid(True, alpha=0.3)` |
| Aspecto cuadrado | `ax.set_aspect('equal')` | util para scatter de coordenadas |
| Quitar marco | `ax.set_frame_on(False)` | look minimalista |
| Leyenda | `ax.legend(...)` | `ax.legend(loc='upper left')` |
| Atajo todo en uno | `ax.set(...)` | `ax.set(xlabel='x', ylabel='y', title='t')` |

#### El truco `ax.set(...)`

Para no escribir 5 lineas, agrupa varios `set_*` en uno:
```python
ax.set(title='Ventas',
       xlabel='Mes',
       ylabel='EUR',
       xlim=(0, 12),
       ylim=(0, 5000))
```

#### Rotar etiquetas largas (muy comun con fechas)

```python
ax.tick_params(axis='x', rotation=45)
# o tambien
plt.xticks(rotation=45)
```"""
    )},
    {"type": "md", "src": tu_turno(3,
        """Tienes los datos `meses = ['Ene','Feb','Mar','Abr','May','Jun']` y `ventas = [120, 135, 150, 145, 170, 180]`.

Pinta una linea con marker circular azul y customizala asi:
- Titulo: `'Ventas primer semestre'`
- Etiqueta X: `'Mes'`, etiqueta Y: `'Miles de EUR'`
- `set_ylim(100, 200)`
- Rejilla activada con `alpha=0.3`
- Leyenda con etiqueta `'2024'`"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nmeses = ['Ene','Feb','Mar','Abr','May','Jun']\nventas = [120, 135, 150, 145, 170, 180]\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import matplotlib.pyplot as plt\n#\n# meses = ['Ene','Feb','Mar','Abr','May','Jun']\n# ventas = [120, 135, 150, 145, 170, 180]\n#\n# # 1) crear figura y axes\n# fig, ax = plt.subplots(figsize=(8, 4))\n#\n# # 2) pintar linea: color azul, marker circulo, linea solida\n# ax.plot(meses, ventas,\n#         color='blue', marker='o', linestyle='-',\n#         linewidth=2, label='2024')\n#\n# # 3) decoradores en bloque\n# ax.set(title='Ventas primer semestre',\n#        xlabel='Mes',\n#        ylabel='Miles de EUR',\n#        ylim=(100, 200))\n#\n# # 4) rejilla y leyenda\n# ax.grid(True, alpha=0.3)\n# ax.legend(loc='best')\n#\n# plt.show()\n"},
]))

# ============ ANOTACIONES ============
plan.append((ID_ANOTACIONES, [
    {"type": "md", "src": teoria(
        "Anotaciones: <code>ax.text</code> vs <code>ax.annotate</code>",
        """Cuando un punto es importante, **escribelo en el grafico** en lugar de obligar al lector a buscarlo.

#### `ax.text(x, y, 'texto')` - simple

Pone un texto en las coordenadas (x, y) **del dataset**.
```python
ax.text(2024, 180, 'pico historico')
```

#### `ax.annotate(...)` - con flecha

Apunta a un punto desde un texto separado.
```python
ax.annotate('Outlier!',
            xy=(5, 90),                 # punto al que apunta la flecha
            xytext=(7, 60),             # posicion del texto
            arrowprops=dict(facecolor='red', shrink=0.05))
```

| Parametro | Significado |
|---|---|
| `xy` | Coordenadas del **punto** apuntado |
| `xytext` | Coordenadas donde va el **texto** |
| `arrowprops` | Diccionario con estilo de la flecha |
| `xycoords` | Sistema de coordenadas (`'data'`, `'axes fraction'`) |

#### Cuando usar cada uno?

| Caso | Que usar |
|---|---|
| Etiquetar un punto sin flecha | `ax.text` |
| Senalar con flecha | `ax.annotate` |
| Watermark / sello | `ax.text` con `transform=ax.transAxes` |"""
    )},
]))

# ============ TIPOS DE GRAFICOS ============
plan.append((ID_TIPOS_GRAF, [
    {"type": "md", "src": teoria(
        "Que tipo de grafico usar? La pregunta clave",
        """Elegir mal el grafico te hace contar mal la historia. Esta tabla resume **cuando usar cada uno**.

| Grafico | Cuando | Cuando NO |
|---|---|---|
| **Linea** (`plot`) | Variable continua a lo largo del tiempo / X ordenado | Categorias sin orden natural |
| **Barras** (`bar`, `barh`) | Comparar **categorias** discretas | Series temporales largas |
| **Scatter** (`scatter`) | Relacion entre 2 variables continuas | Cuando una de las dos es categorica |
| **Histograma** (`hist`) | Distribucion de UNA variable numerica | Comparar grupos pequenos |
| **Boxplot** (`boxplot`) | Distribucion + outliers, comparar grupos | Cuando hay pocos puntos (<10) |
| **Heatmap** (`imshow`, `sns.heatmap`) | Matrices, correlaciones, intensidades 2D | Datos 1D |
| **Pie** (`pie`) | Composicion de un total cuando hay <=5 categorias | >5 categorias o si te importa comparar tamanos parecidos |
| **Stack plot** (`stackplot`) | Composicion que cambia con el tiempo | Series sin parte-todo |

#### Linea vs Barra vs Scatter (la decision tipica)

| Pregunta que respondes | Grafico ideal |
|---|---|
| "Como evoluciono X en el tiempo?" | **Linea** |
| "Quien tiene mas X?" | **Barra** |
| "X y Y estan relacionadas?" | **Scatter** |
| "Que distribucion tiene X?" | **Histograma o Boxplot** |

#### Reglas que se rompen y duelen

- **Pie chart con 12 categorias**: ilegible. Usa una barra horizontal ordenada.
- **Linea para categorias** (ej: paises): el orden de la linea no significa nada -> enganoso.
- **Eje Y que no empieza en 0** en barras: exagera diferencias falsas. Las lineas si lo permiten.
- **3D innecesario**: los graficos 3D son casi siempre menos legibles que los 2D."""
    )},
    {"type": "md", "src": teoria(
        "Histograma y boxplot: imprescindibles en EDA",
        """En cualquier proyecto de Machine Learning, lo primero que haras con una variable numerica son **estos dos**.

#### Histograma: <code>plt.hist</code>

Cuenta cuantos valores caen en cada rango (bin). Sirve para ver **forma de la distribucion**: simetrica, sesgada, multimodal.

```python
plt.hist(datos, bins=20, color='steelblue', edgecolor='black')
plt.xlabel('valor')
plt.ylabel('frecuencia')
```

| Parametro | Detalle |
|---|---|
| `bins` | Numero de contenedores (15-30 suele estar bien) |
| `density` | Si True, normaliza a area=1 (probabilidad) |
| `cumulative` | Si True, acumula |
| `alpha` | Transparencia para superponer histogramas |

#### Boxplot (diagrama de caja)

Resume una distribucion en cinco numeros: minimo, Q1, mediana, Q3, maximo, mas outliers.

```
       outliers
            |
   |-------|     |-------|
   |       |  +  |       |     o   o
   |-------|     |-------|
       |
   bigote   caja con mediana   bigote
```

| Elemento | Que es |
|---|---|
| Linea central de la caja | **Mediana** (Q2) |
| Borde inferior | Q1 (percentil 25) |
| Borde superior | Q3 (percentil 75) |
| Bigotes | Hasta 1.5*IQR del Q1/Q3 |
| Puntos sueltos | **Outliers** |

```python
plt.boxplot([grupo_a, grupo_b, grupo_c],
            labels=['A', 'B', 'C'])
```

> El boxplot es **el detector de outliers** que vas a usar en TODO proyecto de ML."""
    )},
    {"type": "md", "src": tu_turno(4,
        """Genera datos sinteticos con `np.random.seed(0)` y luego:

```python
normal = np.random.normal(loc=50, scale=10, size=500)
sesgada = np.random.exponential(scale=10, size=500)
```

Crea una figura con 2 subplots en una fila (`figsize=(12, 4)`):

1. En el primero, dibuja un **histograma** de `normal` con `bins=30`, color azul, titulo `'Distribucion normal'`.
2. En el segundo, dibuja un **histograma** de `sesgada` con `bins=30`, color naranja, titulo `'Distribucion sesgada'`.

Bonus: anade `fig.tight_layout()` antes de `plt.show()`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# import matplotlib.pyplot as plt\n#\n# # 1) reproducibilidad\n# np.random.seed(0)\n# normal  = np.random.normal(loc=50, scale=10, size=500)\n# sesgada = np.random.exponential(scale=10, size=500)\n#\n# # 2) figura con 2 subplots\n# fig, axes = plt.subplots(1, 2, figsize=(12, 4))\n#\n# # 3) primer subplot: distribucion normal\n# axes[0].hist(normal, bins=30, color='steelblue', edgecolor='black')\n# axes[0].set_title('Distribucion normal')\n# axes[0].set_xlabel('valor')\n# axes[0].set_ylabel('frecuencia')\n#\n# # 4) segundo subplot: distribucion sesgada\n# axes[1].hist(sesgada, bins=30, color='orange', edgecolor='black')\n# axes[1].set_title('Distribucion sesgada')\n# axes[1].set_xlabel('valor')\n# axes[1].set_ylabel('frecuencia')\n#\n# fig.tight_layout()\n# plt.show()\n"},
]))

# ============ GRABAR ============
plan.append((ID_GRABAR, [
    {"type": "md", "src": teoria(
        "Exportar el grafico a archivo: <code>fig.savefig</code>",
        """Para informes y memorias necesitas el grafico en disco. La funcion clave es `fig.savefig(...)`.

```python
fig.savefig('grafico.png',
            dpi=150,                # resolucion (150-300 para impresion)
            bbox_inches='tight',    # recorta margenes blancos
            facecolor='white')       # fondo (no transparente)
```

| Parametro | Para que |
|---|---|
| `dpi` | Calidad. 100 web, 150 pantalla, 300 imprenta |
| `bbox_inches='tight'` | Quita el espacio en blanco innecesario |
| `format` | Lo deduce de la extension. Soporta png, pdf, svg, eps, jpg |
| `transparent=True` | Fondo transparente (util para web) |

#### Recomendacion segun el destino

| Destino | Formato | Por que |
|---|---|---|
| Web / Slack | `.png` | Universal, fondo blanco |
| Documento Word/Google Docs | `.png` a 200 dpi | Calidad correcta |
| LaTeX / publicacion academica | `.pdf` o `.svg` | **Vectorial**: no se pixela al hacer zoom |
| Iconos / web responsive | `.svg` | Vectorial pequeno |

> **NUNCA hagas screenshot del notebook**. Usa `savefig`. Es mas nitido y reproducible."""
    )},
]))

# ============ PANDAS PLOT ============
plan.append((ID_PANDAS_PLOT, [
    {"type": "md", "src": teoria(
        "<code>DataFrame.plot</code>: matplotlib en una linea",
        """Pandas envuelve matplotlib y te da una API mas corta cuando ya tienes un DataFrame.

```python
df.plot()                           # todas las columnas como lineas
df.plot(x='fecha', y='ventas')      # eligiendo columnas
df['col'].plot(kind='hist')          # de una columna sola
```

#### Equivalencias rapidas

| matplotlib puro | pandas |
|---|---|
| `plt.plot(df['x'], df['y'])` | `df.plot(x='x', y='y')` |
| 5 lineas para 5 columnas | `df.plot()` (una sola) |
| `plt.bar(df['x'], df['y'])` | `df.plot(kind='bar', x='x', y='y')` |

#### Ventaja: usa los nombres de columna automaticamente

Las leyendas y los ejes salen ya con los nombres de las columnas. Te ahorra muchos `set_xlabel`."""
    )},
]))

plan.append((ID_FRAMEPLOT, [
    {"type": "md", "src": teoria(
        "Tipos de <code>kind=</code> en pandas",
        """| `kind=` | Equivalente matplotlib | Cuando usar |
|---|---|---|
| `'line'` (default) | `plot` | Series temporales |
| `'bar'` | `bar` | Comparar categorias (vertical) |
| `'barh'` | `barh` | Comparar categorias (horizontal). Mejor si nombres largos. |
| `'hist'` | `hist` | Distribucion de una columna |
| `'box'` | `boxplot` | Distribucion comparada de varias columnas |
| `'kde'` o `'density'` | density | Histograma suavizado |
| `'area'` | `stackplot` | Composicion acumulada |
| `'pie'` | `pie` | Composicion (pocas categorias) |
| `'scatter'` | `scatter` | Necesita `x` e `y` |
| `'hexbin'` | `hexbin` | Scatter con muchos puntos solapados |

#### `subplots=True` para series independientes

```python
df.plot(subplots=True, figsize=(8, 6), sharex=True)
```
Crea un subplot por cada columna automaticamente. Es perfecto cuando las columnas tienen escalas distintas."""
    )},
    {"type": "md", "src": tu_turno(5,
        """Crea este DataFrame:

```python
df = pd.DataFrame({
    'norte': np.random.randint(50, 200, 12),
    'sur':   np.random.randint(50, 200, 12),
    'este':  np.random.randint(50, 200, 12),
}, index=['Ene','Feb','Mar','Abr','May','Jun',
          'Jul','Ago','Sep','Oct','Nov','Dic'])
```

Genera 3 graficos distintos del mismo DataFrame:
1. Lineas en una sola figura.
2. Barras agrupadas (`kind='bar'`).
3. Boxplot por region (`kind='box'`).

Cada uno con un titulo descriptivo."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import numpy as np\n# import pandas as pd\n# import matplotlib.pyplot as plt\n#\n# np.random.seed(42)\n#\n# # 1) construimos el DataFrame\n# df = pd.DataFrame({\n#     'norte': np.random.randint(50, 200, 12),\n#     'sur':   np.random.randint(50, 200, 12),\n#     'este':  np.random.randint(50, 200, 12),\n# }, index=['Ene','Feb','Mar','Abr','May','Jun',\n#           'Jul','Ago','Sep','Oct','Nov','Dic'])\n#\n# # 2) lineas (default kind='line')\n# df.plot(title='Ventas mensuales por region (lineas)')\n# plt.show()\n#\n# # 3) barras agrupadas\n# df.plot(kind='bar', title='Ventas mensuales por region (barras)')\n# plt.show()\n#\n# # 4) boxplot por region\n# df.plot(kind='box', title='Distribucion de ventas por region')\n# plt.show()\n"},
]))

# ============ SEABORN ============
plan.append((ID_SEABORN, [
    {"type": "md", "src": teoria(
        "Seaborn: matplotlib estadistico de alto nivel",
        """**seaborn** envuelve matplotlib y se especializa en **graficos estadisticos**. Su filosofia: una linea de codigo, mucha informacion.

#### Por que seaborn brilla

| Ventaja | Detalle |
|---|---|
| **Trabaja con DataFrames** | Pasa nombres de columnas como strings: `x='col_x'`, `y='col_y'`, `data=df` |
| **Estetica por defecto** | Colores y estilo agradables sin tunear nada |
| **Estadistica integrada** | Anade automaticamente intervalos de confianza, regresion, KDE... |
| **Facetas automaticas** | `col=`, `row=`, `hue=` dividen el grafico por categoria |
| **Compatible con matplotlib** | Devuelve objetos matplotlib que puedes seguir customizando |

#### Conceptos clave: <code>hue</code>, <code>col</code>, <code>row</code>

Estos tres parametros te ahorran horas:

| Parametro | Que hace |
|---|---|
| `hue='cat'` | Pinta cada categoria en un **color** distinto |
| `col='cat'` | Crea una **columna de subplots** por categoria |
| `row='cat'` | Crea una **fila de subplots** por categoria |
| `size='num'` | Tamano de los puntos por una variable numerica |
| `style='cat'` | Cambia marker o linestyle por categoria |

#### Familias de funciones (las mas usadas)

| Familia | Funciones tipicas | Para que |
|---|---|---|
| **Relacionales** | `relplot`, `scatterplot`, `lineplot` | Relacion entre 2 numericas |
| **Categoricas** | `barplot`, `boxplot`, `swarmplot`, `violinplot`, `countplot` | Numerica vs categorica |
| **Distribucion** | `displot`, `histplot`, `kdeplot`, `jointplot` | Forma de una variable |
| **Regresion** | `regplot`, `lmplot` | Tendencia lineal o polinomica |
| **Matrices** | `heatmap`, `clustermap` | Matrices 2D, correlaciones |
| **Multivariable** | `pairplot` | Todos contra todos |

#### Estilo

```python
sns.set_theme(style='whitegrid')  # 'darkgrid','white','ticks'
sns.set_context('notebook')        # 'paper','notebook','talk','poster'
```"""
    )},
    {"type": "md", "src": dato(
        """**Cuando usar matplotlib y cuando seaborn?**

| Necesito | Usa |
|---|---|
| Control total, codigo de produccion | matplotlib |
| Explorar relaciones rapidamente | seaborn |
| Customizacion fina sobre algo seaborn | seaborn + matplotlib (combinado) |

Recuerda: **los objetos que devuelve seaborn son matplotlib por dentro**. Puedes hacer:
```python
ax = sns.boxplot(...)
ax.set_title('Mi titulo')
ax.set_ylim(0, 100)
```"""
    )},
]))

# ============ RELACIONES ============
plan.append((ID_RELACIONES, [
    {"type": "md", "src": teoria(
        "<code>relplot</code>: relaciones entre dos variables",
        """`sns.relplot(x, y, data, kind, hue, col, row, ...)` es un **wrapper de alto nivel** sobre `scatterplot` y `lineplot`.

```python
sns.relplot(x='total_bill', y='tip',
            data=tips,
            hue='time',         # color por categoria
            col='sex',          # un subplot por sexo
            kind='scatter')     # 'scatter' o 'line'
```

#### Diferencia entre `relplot` y `scatterplot`

| Funcion | Devuelve | Permite facetas |
|---|---|---|
| `sns.scatterplot(...)` | un Axes (un grafico) | NO |
| `sns.relplot(...)` | una FacetGrid (figura entera) | SI (`col=`, `row=`) |

Misma logica para `lineplot` vs `relplot(kind='line')`.

#### Pinta media + intervalo de confianza

Si pasas datos repetidos en X, `lineplot` calcula la media y dibuja un sombreado con el intervalo de confianza. Sin escribir matematicas:

```python
sns.lineplot(x='year', y='passengers', data=flights)
```

Es por esto que es tan querido en analisis de series temporales con replicaciones."""
    )},
]))

# ============ DISTRIBUCION ============
plan.append((ID_DISTRIB, [
    {"type": "md", "src": teoria(
        "<code>displot</code>, <code>histplot</code>, <code>kdeplot</code>, <code>jointplot</code>",
        """Cuando exploras una variable, esta es la familia de seaborn que mas usaras.

| Funcion | Que dibuja | Cuando |
|---|---|---|
| `histplot` | Histograma | 1 variable, conteo en bins |
| `kdeplot` | Curva de densidad | 1 variable suavizada |
| `displot` | Wrapper que decide segun `kind` | `kind='hist'`, `'kde'`, `'ecdf'` |
| `jointplot` | 2 variables: scatter + hist en margenes | Distribucion conjunta |
| `rugplot` | Tickitos en el eje | Marcar cada observacion |
| `pairplot` | Todas las variables 2 a 2 | EDA general |

#### Trucos

```python
# Comparar dos grupos en el mismo histograma
sns.histplot(data=tips, x='tip', hue='sex', kde=True)

# Density 2D (mapa de calor de probabilidad)
sns.jointplot(data=iris, x='petal_length', y='petal_width', kind='kde')

# Pairplot con color por clase (clasico)
sns.pairplot(iris, hue='species')
```

#### `kde=True` en histogramas

Anade la curva de densidad encima. Util para comparar la forma con una normal teorica."""
    )},
]))

# ============ CORRELACIONES ============
plan.append((ID_CORREL, [
    {"type": "md", "src": teoria(
        "Regresion y correlacion: <code>regplot</code>, <code>lmplot</code>, <code>heatmap</code>",
        """Para mostrar la **tendencia** entre dos variables seaborn ofrece dos funciones casi gemelas.

| Funcion | Para que | Permite facetas |
|---|---|---|
| `sns.regplot(x, y, data, order=1)` | Scatter + recta de regresion + IC | NO |
| `sns.lmplot(x, y, data, hue, col, row, order=1)` | Como regplot pero con facetas | SI |

```python
sns.regplot(x='total_bill', y='tip', data=tips)            # recta lineal
sns.regplot(x='total_bill', y='tip', data=tips, order=2)   # parabola
sns.lmplot(x='total_bill', y='tip', data=tips,
           hue='smoker', col='time', order=2)
```

#### `order=` controla el grado del polinomio

- `order=1` -> recta lineal (default).
- `order=2` -> parabola.
- `order=3+` -> mas flexibilidad, mas riesgo de overfitting.

#### Heatmap de correlaciones (te lo van a pedir mucho)

```python
import seaborn as sns
sns.heatmap(df.corr(numeric_only=True),
            annot=True,         # escribe el valor en cada celda
            fmt='.2f',          # 2 decimales
            cmap='coolwarm',    # paleta divergente para [-1, 1]
            center=0)           # 0 en blanco
```

| Parametro | Detalle |
|---|---|
| `annot=True` | Anade los valores numericos |
| `cmap` | `'coolwarm'` (divergente), `'viridis'` (secuencial), `'YlOrRd'` |
| `center=0` | Solo si paleta divergente y rango incluye negativos |
| `vmin`/`vmax` | Forzar limites de la escala |"""
    )},
    {"type": "md", "src": tu_turno(6,
        """Carga el dataset `iris` con `sns.load_dataset('iris')` y haz tres graficos:

1. Un **scatter con regresion** entre `petal_length` (x) y `petal_width` (y), de orden 1.
2. El mismo scatter pero **separado por especie** (con `lmplot` y `hue='species'`).
3. Un **heatmap** de correlaciones de las columnas numericas (`iris.corr(numeric_only=True)`) con `annot=True`, `cmap='coolwarm'` y `center=0`.

Cada uno en su propia celda."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import seaborn as sns\n# import matplotlib.pyplot as plt\n#\n# # 1) cargar dataset\n# iris = sns.load_dataset('iris')\n#\n# # 2) regresion simple\n# sns.regplot(x='petal_length', y='petal_width', data=iris)\n# plt.title('Regresion lineal: petal_length vs petal_width')\n# plt.show()\n#\n# # 3) regresion separada por especie con lmplot (que SI permite hue)\n# sns.lmplot(x='petal_length', y='petal_width',\n#            data=iris, hue='species', height=4, aspect=1.4)\n# plt.show()\n#\n# # 4) heatmap de correlaciones\n# corr = iris.corr(numeric_only=True)\n# sns.heatmap(corr, annot=True, fmt='.2f',\n#             cmap='coolwarm', center=0)\n# plt.title('Matriz de correlacion - iris')\n# plt.show()\n"},
]))

# ============ EJERCICIOS FINALES ============
plan.append((ID_EJERCICIOS, [
    {"type": "md", "src": dato(
        """**Resumen rapido para la parte de ejercicios:**

#### Para los ejercicios de matplotlib

```python
years = list(range(2000, 2021))            # eje x: 21 anios
y0 = np.random.randint(0, 100, len(years)) # eje y aleatorio
# ... y1, y2, y3 igual
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(years, y0, label='Hawaii')
ax.plot(years, y1, label='San Marino')
# ...
ax.legend()
ax.set(title='Datos aleatorios', xlabel='Anio', ylabel='GDP')
ax.annotate('Pico', xy=(2010, 90), xytext=(2012, 70),
            arrowprops=dict(facecolor='black', shrink=0.05))
plt.show()
```

#### Para los ejercicios de seaborn

Sugerencias de datasets que NO son tips, iris ni flights:

| Dataset | `sns.load_dataset(...)` | Variables interesantes |
|---|---|---|
| `penguins` | pinguinos | `bill_length_mm`, `flipper_length_mm`, `species` |
| `diamonds` | diamantes | `carat`, `price`, `cut` |
| `mpg` | coches | `horsepower`, `mpg`, `origin` |
| `titanic` | titanic | `age`, `fare`, `class` |
| `planets` | exoplanetas | `mass`, `distance`, `method` |

Estructura recomendada:
```python
df = sns.load_dataset('penguins').dropna()
sns.pairplot(df, hue='species')           # parejas
sns.regplot(x='bill_length_mm', y='flipper_length_mm', data=df)  # correlacion
sns.relplot(x='bill_length_mm', y='body_mass_g',
            hue='species', data=df)       # 2 numericas + 1 categorica
sns.boxplot(x='species', y='body_mass_g', data=df)  # distribucion
```"""
    )},
    {"type": "md", "src": aviso(
        """**Errores frecuentes en los ejercicios finales (revisa antes de entregar):**

1. **Olvidar `plt.show()`** al final de cada celda -> aparece basura en consola.
2. **Mezclar `plt.title` con OO**: si usas `fig, ax = plt.subplots()`, llama a `ax.set_title(...)`, no a `plt.title(...)`. Aunque a veces funciona, te va a dar dolores de cabeza.
3. **No fijar `np.random.seed(...)`** -> tus graficos cambian cada vez que corres la celda. Para entregas, fijalo.
4. **Pie chart con muchas categorias** -> ilegible. Usa `barh` ordenado por valor.
5. **Histograma con `bins=10` por defecto cuando tienes muchos datos** -> queda grueso. Sube a 30-50.
6. **`sns.regplot` con `hue`** -> no lo soporta. Usa `sns.lmplot` para separar por categoria."""
    )},
]))


enhance(NB, plan)
print("Done.")

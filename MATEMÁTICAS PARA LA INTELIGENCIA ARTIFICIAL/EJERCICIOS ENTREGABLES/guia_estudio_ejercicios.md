# Guía de Estudio — Ejercicios Entregables
> Lee esto antes de revisar el código. Cada concepto explicado desde cero.

---

# EJERCICIO 1: DETERMINANTE

## Qué es el determinante — antes de calcular nada

El determinante es un número que le corresponde a cada matriz cuadrada.
Tiene varios significados dependiendo del contexto:

**Significado geométrico (el más útil para entenderlo):**

En 2D: si tienes una matriz 2×2, el determinante es el **área** del paralelogramo
que forman las dos filas como vectores.

```
A = | 2  0 |
    | 0  3 |

Las filas son los vectores (2,0) y (0,3).
El paralelogramo es un rectángulo de 2×3 = 6.
det(A) = 6 ✓
```

En 3D: el determinante es el **volumen** del paralelepípedo.

**En ML:** si det(A) = 0, la matriz no es invertible → el sistema Ax=b puede no tener solución. Determinar si una transformación lineal es invertible es crucial en PCA, regresión lineal, etc.

---

## 1a) Cómo funciona la expansión de Laplace

La idea: para calcular det de una matriz n×n, la descomponemos en n determinantes de matrices (n-1)×(n-1). Y así recursivamente hasta llegar a 2×2 (que sabemos calcular directo).

**det de 2×2 (caso base):**
```
| a  b |
| c  d |  = a·d - b·c
```
Simplemente: diagonal principal menos diagonal secundaria.

**det de 3×3 (primer nivel recursivo):**

Expando por la primera fila: tomo cada elemento de la fila, lo multiplico por det de la submatriz que queda al tapar su fila y columna, y alterno signos (+, -, +).

```
A = | 1  2  3 |
    | 4  5  6 |
    | 7  8  9 |

Elemento a_01 = 1, signo = +, tapo fila 0 y col 0:
    submatriz = | 5  6 |    det = 5·9 - 6·8 = 45-48 = -3
                | 8  9 |

Elemento a_02 = 2, signo = -, tapo fila 0 y col 1:
    submatriz = | 4  6 |    det = 4·9 - 6·7 = 36-42 = -6
                | 7  9 |

Elemento a_03 = 3, signo = +, tapo fila 0 y col 2:
    submatriz = | 4  5 |    det = 4·8 - 5·7 = 32-35 = -3
                | 7  8 |

det(A) = 1·(-3) - 2·(-6) + 3·(-3) = -3 + 12 - 9 = 0
```

**El patrón de signos siempre es: +, -, +, -, +, ...**

Esto viene de (-1)^(fila+columna): en fila 0, columna 0 → (-1)^0 = +1, columna 1 → (-1)^1 = -1, etc.

**Por qué es O(n!) — visualizando el árbol de recursión:**

```
det(4×4) llama a:
├── det(3×3) que llama a:
│   ├── det(2×2)
│   ├── det(2×2)
│   └── det(2×2)
├── det(3×3) que llama a:
│   ├── det(2×2)
│   ├── det(2×2)
│   └── det(2×2)
├── det(3×3) ... (igual)
└── det(3×3) ... (igual)

n=4:  4 × 3 × 2 × 1 = 24 operaciones = 4!
n=10: 10! = 3,628,800
n=20: 20! ≈ 2,400,000,000,000,000,000  → imposible
```

---

## 1b) Determinante de matriz triangular — el truco de la diagonal

**Qué es triangular superior:** todos los ceros están DEBAJO de la diagonal.
```
| 2  5  1 |
| 0  3  7 |     ← ceros abajo de la diagonal
| 0  0  4 |
```

**Qué es triangular inferior:** todos los ceros están ARRIBA de la diagonal.
```
| 2  0  0 |
| 5  3  0 |     ← ceros arriba de la diagonal
| 1  7  4 |
```

**El resultado:** en ambos casos, det = producto de la diagonal.
```
det = 2 × 3 × 4 = 24
```

**Por qué funciona (para triangular superior):**

Expando por la primera columna. En triangular superior, la primera columna tiene:
- a_00 = 2 (el pivote)
- a_10 = 0
- a_20 = 0

Los ceros no contribuyen. Solo queda:
```
det = a_00 × det(submatriz sin fila0 y col0)
    = 2 × det| 3  7 |
             | 0  4 |
    = 2 × (3×4 - 7×0)
    = 2 × 12
    = 24 ✓
```

El mismo argumento aplica recursivamente. Para triangular inferior, expandís por la primera fila en vez de la primera columna — mismo resultado.

**Por qué esto importa:** Gauss convierte A en triangular → det = solo multiplicar la diagonal = O(n).

---

## 1c) Operaciones elementales — qué le pasan al determinante

**Operación 1 — intercambiar dos filas:**
```
Antes:  det = X
Después: det = -X   (cambia el signo)
```

**Por qué:** el determinante mide el volumen del paralelepípedo formado por las filas. Si intercambias dos filas, "giras" el paralelepípedo → el volumen tiene el mismo valor pero la orientación cambia (de derecha a zurda o viceversa), lo que en matemáticas se representa con el signo negativo.

**Operación 2 — sumar α veces una fila a otra:**
```
fila_i ← fila_i + α·fila_k
Resultado: det no cambia
```

**Por qué:** imagina que separas la fila modificada en dos partes:
- Parte 1: la fila original fila_i → contribuye det(A) (sin cambio)
- Parte 2: α·fila_k → crea una matriz con fila_k repetida → det = 0

Resultado total: det(A) + 0 = det(A). El det no cambia.

**El resumen que necesitas para Gauss:**
```
Swap de filas      → det cambia de signo (hay que registrar cuántos swaps)
Eliminación (op 2) → det no cambia (puedes ignorarlos)
```

---

## 1d) Eliminación de Gauss — el algoritmo completo, paso a paso

**Objetivo:** convertir A en triangular superior U, registrando cuántos swaps hiciste.

**Ejemplo con números concretos:**

```
A = | 2   1  -1 |
    |-3  -1   2 |
    |-2   1   2 |
```

**Columna 0 — hacer ceros en posición (1,0) y (2,0):**

Paso 1 — Pivoteo parcial (elegir la fila con el mayor valor absoluto en col 0):
```
|a_00| = |2| = 2
|a_10| = |-3| = 3  ← este es mayor
|a_20| = |-2| = 2

Swap fila 0 ↔ fila 1 → num_swaps = 1

A = |-3  -1   2 |   ← fila con mayor pivote queda arriba
    | 2   1  -1 |
    |-2   1   2 |
```

Paso 2 — Eliminación (crear ceros debajo del pivote -3):

Para fila 1:
```
multiplicador m = a_10/a_00 = 2/(-3) = -0.6667
fila_1 ← fila_1 - m·fila_0
fila_1[0] = 2 - (-0.6667)·(-3) = 2 - 2 = 0  ✓
fila_1[1] = 1 - (-0.6667)·(-1) = 1 - 0.667 = 0.333
fila_1[2] = -1- (-0.6667)·(2) = -1 + 1.333 = 0.333
```

Para fila 2:
```
m = (-2)/(-3) = 0.6667
fila_2 ← fila_2 - m·fila_0
fila_2[0] = -2 - 0.6667·(-3) = -2 + 2 = 0  ✓
fila_2[1] = 1 - 0.6667·(-1) = 1 + 0.667 = 1.667
fila_2[2] = 2 - 0.6667·(2) = 2 - 1.333 = 0.667
```

Resultado después de columna 0:
```
|-3    -1     2   |
| 0     0.333 0.333|
| 0     1.667 0.667|
```

**Columna 1 — hacer cero en posición (2,1):**

Pivoteo: |a_11|=0.333, |a_21|=1.667 → swap fila 1 ↔ fila 2 → num_swaps = 2
```
|-3    -1     2   |
| 0     1.667 0.667|
| 0     0.333 0.333|
```

Eliminación:
```
m = 0.333/1.667 = 0.2
fila_2 ← fila_2 - 0.2·fila_1
fila_2[1] = 0.333 - 0.2·1.667 = 0.333 - 0.333 = 0  ✓
fila_2[2] = 0.333 - 0.2·0.667 = 0.333 - 0.133 = 0.2
```

**Resultado final — U triangular superior:**
```
U = |-3    -1     2   |
    | 0     1.667 0.667|
    | 0     0     0.2  |
```

**Por qué pivoteo parcial:** si el pivote fuera 0 (o muy pequeño), no puedes dividir.
Elegir el pivote más grande en módulo evita este problema y da más estabilidad numérica.

---

## 1e) Calcular det(A) con el resultado de Gauss

Ya tenemos U y sabemos que num_swaps = 2. Aplicamos la fórmula:

```
det(A) = (-1)^num_swaps × det(U)
       = (-1)^2 × (producto de la diagonal de U)
       = (+1) × ((-3) × 1.667 × 0.2)
       = (+1) × (-1.0)
       = -1.0
```

**Verificación con numpy:** np.linalg.det(A) = -1.0 ✓

**La fórmula conecta todo:**
- El det de U es fácil (triangular → producto diagonal) → gracias al apartado b
- Los swaps aportan el signo → gracias al apartado c
- Gauss no cambia el det con las eliminaciones → gracias al apartado c

---

## 1f) Complejidad — por qué importa tanto la diferencia

| n | Laplace (n!) | Gauss (n³/3) | Factor de diferencia |
|---|-------------|-------------|---------------------|
| 5 | 120 ops | 42 ops | 3× |
| 10 | 3,628,800 ops | 333 ops | **10,000×** |
| 15 | 1.3×10¹² ops | 1,125 ops | **1,000,000,000×** |
| 20 | 2.4×10¹⁸ ops | 2,667 ops | impensable |

Con una CPU de 10⁹ operaciones/segundo:
- Gauss con n=20 → termina en 0.000003 segundos
- Laplace con n=20 → tardaría **77 años**

---

---

# EJERCICIO 2: DESCENSO DE GRADIENTE

## La idea central — bajar una colina

Imagina que estás en una colina con los ojos vendados y quieres llegar al punto más bajo.
¿Qué haces? Tocas el suelo alrededor de tus pies y caminas en la dirección donde el suelo baja más.

Eso es exactamente el descenso de gradiente:
- La colina = la función f(x) que queremos minimizar
- Tu posición = el valor actual de x
- La dirección de mayor bajada = **-∇f(x)** (gradiente negativo)

**La regla de actualización:**
```
x_nuevo = x_actual - γ × gradiente_en_x_actual
```

donde γ (gamma) es el "tamaño de paso" — cuánto te mueves en cada iteración.

**Cuándo paras:**
- Cuando el gradiente es casi 0 (estás cerca de un mínimo, máximo, o punto de silla)
- O cuando llegas al máximo de iteraciones (por si diverge y nunca llega)

---

## Qué es el gradiente

**En 1D:** el gradiente es simplemente la derivada f'(x).
- f'(x) > 0 → la función sube a la derecha
- f'(x) < 0 → la función baja a la derecha
- f'(x) = 0 → punto crítico (mínimo, máximo, o silla)

Entonces x_nuevo = x - γ·f'(x):
- Si f'(x)>0 (función subiendo) → x_nuevo < x (nos movemos a la izquierda, bajando)
- Si f'(x)<0 (función bajando) → x_nuevo > x (nos movemos a la derecha, bajando)

**En 2D (o más):** el gradiente es un vector de derivadas parciales:
```
∇f(x,y) = (∂f/∂x, ∂f/∂y)
```
Apunta en la dirección de mayor crecimiento. Nos movemos en la dirección opuesta.

---

## Análisis de f(x) = 3x⁴ + 4x³ − 12x² + 7

**Paso 1: derivada para encontrar puntos críticos**

```
f'(x) = 12x³ + 12x² - 24x
      = 12x(x² + x - 2)      ← saco factor común 12x
      = 12x(x + 2)(x - 1)    ← factorizo la cuadrática
```

Para factorizar x² + x - 2: busco dos números que multiplicados den -2 y sumados den +1. Son +2 y -1. Entonces (x+2)(x-1).

f'(x) = 0 cuando x=0, x=-2, o x=1.

**Paso 2: derivada segunda para clasificar**

```
f''(x) = 36x² + 24x - 24

f''(-2) = 36·4 + 24·(-2) - 24 = 144 - 48 - 24 = 72 > 0  → MÍNIMO
f''(0)  = 0 + 0 - 24 = -24 < 0                            → MÁXIMO
f''(1)  = 36 + 24 - 24 = 36 > 0                           → MÍNIMO
```

**Por qué f'' clasifica el punto:**
- f'' > 0 → la función es convexa en ese punto (como ∪) → mínimo
- f'' < 0 → la función es cóncava en ese punto (como ∩) → máximo

**Visualización de la función (texto):**

```
f(x)
 7 |    *                          ← máximo en x=0, f=7
   |   / \
   |  /   \
 2 |              *               ← mínimo local en x=1, f=2
   |               \
   |                \
-25|  *              \            ← mínimo global en x=-2, f=-25
   |
   +--+--+--+--+--+--+--→  x
     -3 -2 -1  0  1  2  3
```

**Las cuencas de atracción:**
```
← todo lo de aquí converge a x=-2 | todo lo de aquí converge a x=1 →
                                  0
                             (la frontera)
```

Si empiezas con x<0, llegas al mínimo global. Si empiezas con x>0, llegas al mínimo local.
El punto x=0 es la frontera entre cuencas.

---

## Los 4 experimentos — por qué cada uno da un resultado distinto

**Experimento 2b-i: x₀=3, γ=0.001 → llega a x=1 (mínimo LOCAL)**

```
Paso 1: f'(3) = 12·27 + 12·9 - 24·3 = 324 + 108 - 72 = 360
        x₁ = 3 - 0.001 × 360 = 3 - 0.36 = 2.64
```

Con paso tan pequeño (0.001), x se mueve poco cada vez. Nunca cruza x=0. Se queda en la zona x>0 y converge al mínimo local x=1. Tarda 831 iteraciones.

**Experimento 2b-ii: x₀=3, γ=0.01 → llega a x=-2 (mínimo GLOBAL)**

```
Paso 1: x₁ = 3 - 0.01 × 360 = 3 - 3.6 = -0.6
```

Con un paso 10× más grande, en la primera iteración x salta al lado negativo.
Ahora x < 0 → está en la cuenca del mínimo global → converge a x=-2. Solo tarda 31 iteraciones.

**¿Cuál es mejor?** No hay respuesta universal. γ=0.001 encontró el local, γ=0.01 encontró el global — pero γ=0.01 también podría haber divergido si la función fuera diferente.

**Experimento 2b-iv: x₀=3, γ=0.1 → DIVERGE**

```
Paso 1: x₁ = 3 - 0.1 × 360 = -33
Paso 2: f'(-33) es enormemente negativo
        x₂ = -33 - 0.1 × (algo enorme negativo) = +41705
Paso 3: f'(41705) → overflow del computador
```

El sistema oscila entre valores cada vez más grandes → **explota**. En deep learning esto se llama "gradient explosion" y es un problema real en el entrenamiento de redes recurrentes.

Solución en la práctica: **gradient clipping** (si el gradiente es mayor que un umbral, lo recortas).

**Experimento 2b-v: x₀=0, γ=0.001 → ATRAPADO EN EL MÁXIMO**

```
f'(0) = 12·0·(0+2)·(0-1) = 0
||gradiente|| = 0 < tolerancia → el algoritmo para en 0 iteraciones
```

El gradiente en x=0 es exactamente 0. El algoritmo interpreta eso como "ya llegué" y se detiene. Pero x=0 es un MÁXIMO local, no un mínimo.

**¿Es un resultado deseable? NO.**

El gradiente cero es condición necesaria para ser mínimo, pero no suficiente. También se cumple en máximos y puntos de silla. El algoritmo no puede distinguir entre ellos.

---

## Análisis de g(x,y) = x² + y³ + 3xy + 1

**Paso 1: gradiente de g**

```
∂g/∂x = 2x + 3y
∂g/∂y = 3y² + 3x
```

**Paso 2: igualar a cero para encontrar puntos críticos**

```
2x + 3y = 0    →    y = -2x/3       (despejo y de la primera)
3y² + 3x = 0   →    x = -y²         (despejo x de la segunda)
```

Sustituyo y = -2x/3 en x = -y²:
```
x = -(-2x/3)² = -(4x²/9)
9x = -4x²
4x² + 9x = 0
x(4x + 9) = 0
```

Soluciones: x=0 → y=0 → P₁=(0,0) y x=-9/4 → y=3/2 → P₂=(-2.25, 1.5)

**Paso 3: Hessiana para clasificar**

La Hessiana es la matriz de derivadas segundas (como la "f''" pero en 2D):

```
H = | ∂²g/∂x²    ∂²g/∂x∂y |   =   | 2     3  |
    | ∂²g/∂y∂x   ∂²g/∂y²  |       | 3    6y  |
```

Para clasificar el punto crítico usamos det(H) y el signo de H₀₀:

```
si det(H) > 0 y H₀₀ > 0  →  mínimo local
si det(H) > 0 y H₀₀ < 0  →  máximo local
si det(H) < 0             →  punto de silla
```

**En P₁=(0,0):**
```
H = | 2  3 |
    | 3  0 |

det(H) = 2·0 - 3·3 = -9 < 0  →  PUNTO DE SILLA
```

**En P₂=(-9/4, 3/2):**
```
H = | 2  3 |
    | 3  9 |     (porque 6·(3/2) = 9)

det(H) = 2·9 - 3·3 = 18 - 9 = 9 > 0
H₀₀ = 2 > 0                       →  MÍNIMO LOCAL
```

---

## Qué es un punto de silla — explicado simple

Un punto de silla es un punto donde el gradiente es cero, pero NO es ni mínimo ni máximo.

**La analogía:** imagina la silla de montar de un caballo.
- Si te paras en el centro y miras hacia adelante/atrás → estás en un MÍNIMO (la silla está más alta al frente y atrás)
- Si te paras en el centro y miras hacia los lados → estás en un MÁXIMO (la silla cae hacia los lados)

Desde el centro exacto, el gradiente es 0. Pero la función sube en una dirección y baja en otra.

```
Vista lateral (dirección donde baja):
         \     /
          \   /
           \_/   ← parece un mínimo en esta vista

Vista frontal (dirección donde sube):
           /\
          /  \
         /    \
        /______\  ← parece un máximo en esta vista
```

**Por qué GD queda atrapado:** al llegar al punto (0,0), el gradiente es exactamente [0,0]. El algoritmo ve norma=0 < tolerancia y para. No puede ver que en realidad tiene que escapar en alguna dirección.

**Por qué esto importa en deep learning:**
En redes neuronales con millones de parámetros, los puntos de silla son extremadamente comunes. Los verdaderos mínimos locales malos casi no existen — lo que hay son puntos de silla en todas partes. Por eso se usan:
- **Momentum:** como si la bola de la colina tuviera inercia — puede cruzar zonas de gradiente bajo
- **Adam:** ajusta el learning rate por parámetro — si un parámetro tiene gradientes pequeños le da pasos más grandes

---

## Resumen visual — los 5 conceptos clave

```
LANDSCAPE DE UNA FUNCIÓN 1D:

   f(x)
     |
  7  |    MÁXIMO (GD queda atrapado si empieza aquí)
     |   ╱ ╲
     |  ╱   ╲
  2  |         ╲ MÍNIMO LOCAL
     |          ╲
-25  |   MÍNIMO GLOBAL
     |
     +----------→ x
        |
    FRONTERA entre cuencas de atracción
    (cruzarla con γ grande puede darte el mínimo global)
```

| Situación | Resultado | Por qué |
|-----------|-----------|---------|
| x₀>0, γ pequeño | Mínimo local | No cruza la frontera |
| x₀>0, γ mediano | Mínimo global | Cruza la frontera en el primer paso |
| x₀>0, γ grande | Diverge | El paso es tan grande que explota |
| x₀ en punto crítico | Se queda ahí | Gradiente=0, el algoritmo no se mueve |

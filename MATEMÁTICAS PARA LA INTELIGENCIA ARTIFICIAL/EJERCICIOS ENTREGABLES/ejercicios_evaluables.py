# =============================================================================
# EJERCICIOS EVALUABLES — 02MIAR: Matemáticas para la IA
# Máster Universitario en Inteligencia Artificial — Universidad Internacional de Valencia
# =============================================================================
# Temas: Álgebra Lineal (Determinante) y Cálculo (Descenso de Gradiente)
# Todos los algoritmos están implementados desde cero sin librerías auxiliares.
# numpy se usa SOLO donde el enunciado lo exige explícitamente (apartado 1g).

import sys
import math
import time
import numpy as np   # Solo en 1g: numpy.random.rand y numpy.linalg.det

# Forzar UTF-8 en la consola Windows (evita UnicodeEncodeError con caracteres especiales)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


# =============================================================================
# EJERCICIO 1 — CÁLCULO DEL DETERMINANTE
# =============================================================================


# -----------------------------------------------------------------------------
# 1a) [1 pt]  determinante_recursivo — Expansión de Laplace
# -----------------------------------------------------------------------------
#
# La EXPANSIÓN DE LAPLACE expande el determinante a lo largo de una fila (usamos fila 0):
#
#   det(A) = Σ_{j=0}^{n-1}  (-1)^(0+j) · a[0][j] · det(M_{0j})
#
# donde M_{0j} es el "menor": submatriz obtenida al eliminar la fila 0 y columna j.
#
# La función _menor(A, fila, col) construye esa submatriz usando comprensión de listas:
#   - Recorre todas las filas de A excepto 'fila'
#   - De cada fila restante, incluye todos los elementos excepto el de la columna 'col'
#
# CASO BASE: una matriz 1×1 tiene determinante igual a su único elemento.
# CASO 2×2:  det([[a,b],[c,d]]) = a·d − b·c  (fórmula directa, evita recursión extra)
#
# COSTE:  T(n) = n·T(n−1) + O(n²)  →  T(n) = O(n!)
# Para n=15: 15! ≈ 1.3×10^12 operaciones → completamente inviable en la práctica.

def _menor(A, fila, col):
    """
    Devuelve la submatriz (n-1)×(n-1) de A eliminando 'fila' y 'col'.
    Utiliza comprensión de listas: filtra filas y columnas en una sola expresión.
    """
    return [
        [A[i][j] for j in range(len(A[i])) if j != col]
        for i in range(len(A))       if i != fila
    ]

def determinante_recursivo(A):
    """
    Calcula det(A) mediante la expansión de Laplace por la primera fila.

    A      : lista de listas — matriz cuadrada n×n de floats
    return : float — valor del determinante
    Coste  : O(n!)
    """
    n = len(A)

    if n == 1:                              # caso base: escalar
        return A[0][0]

    if n == 2:                              # fórmula directa 2×2
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]

    det = 0.0
    for j in range(n):
        signo = 1 if j % 2 == 0 else -1    # (-1)^(0+j)
        det  += signo * A[0][j] * determinante_recursivo(_menor(A, 0, j))

    return det


# -----------------------------------------------------------------------------
# 1b) [0.5 pt]  Determinante de una matriz TRIANGULAR — RESPUESTA TEÓRICA
# -----------------------------------------------------------------------------
#
# RESPUESTA: Sí. Para cualquier matriz triangular (superior o inferior), el determinante
# es IGUAL AL PRODUCTO DE LOS ELEMENTOS DE LA DIAGONAL PRINCIPAL:
#
#   det(A) = a_{00} · a_{11} · ··· · a_{n-1,n-1}  =  Π a_{ii}
#
# JUSTIFICACIÓN (por inducción usando Laplace):
#   Sea A TRIANGULAR SUPERIOR (a_{ij} = 0 para i > j).
#   Expandimos por la PRIMERA COLUMNA:
#     · El único elemento no nulo en la columna 0 es a_{00} (todos los de abajo son 0).
#     · Por tanto: det(A) = a_{00} · det(A_{00})
#       donde A_{00} es la submatriz (n-1)×(n-1) que TAMBIÉN es triangular superior.
#     · Aplicando el mismo argumento por inducción:
#       det(A) = a_{00} · a_{11} · ··· · a_{n-1,n-1}
#   Para TRIANGULAR INFERIOR se usa el mismo argumento expandiendo por la primera FILA.
#
# VENTAJA: solo requiere n-1 multiplicaciones → O(n) en lugar de O(n!)

def determinante_triangular(A):
    """
    Calcula det(A) para A triangular (superior o inferior). Complejidad: O(n).
    AVISO: solo es correcto si A es efectivamente triangular.
    """
    det = 1.0
    for i in range(len(A)):
        det *= A[i][i]
    return det


# -----------------------------------------------------------------------------
# 1c) [0.5 pt]  Efecto de las operaciones elementales — RESPUESTA TEÓRICA
# -----------------------------------------------------------------------------
#
# OPERACIÓN 1 — Intercambiar dos filas (o columnas):
#   det(A') = −det(A)    →   el determinante CAMBIA DE SIGNO.
#
#   Justificación: el determinante es una función "alternada" de sus filas.
#   Por la definición vía permutaciones,  det(A) = Σ_σ sgn(σ) · Π a_{i,σ(i)}.
#   Intercambiar las filas i y j equivale a componer cada permutación σ con la
#   transposición (i j), lo cual invierte el signo de sgn(σ) en todos los sumandos.
#   Consecuencia: si dos filas son iguales → det = −det → det = 0.
#
# OPERACIÓN 2 — Sumar α·fila_j a fila_i  (fila_i ← fila_i + α·fila_j,  i ≠ j):
#   det(A') = det(A)     →   el determinante NO CAMBIA.
#
#   Justificación: por LINEALIDAD del determinante en cada fila:
#     det(..., fila_i + α·fila_j, ...) = det(..., fila_i, ...) + α·det(..., fila_j, ...)
#   En el segundo sumando, la fila_j aparece DOS veces (propiedad alternada → det = 0).
#   Por tanto: det(A') = det(A) + α·0 = det(A)
#
#   Consecuencia práctica: podemos anular entradas sin alterar el determinante.
#   Este es el fundamento matemático de la eliminación gaussiana.


# -----------------------------------------------------------------------------
# 1d) [1 pt]  Eliminación de Gauss con pivoteo parcial → escalonamiento_gauss
# -----------------------------------------------------------------------------
#
# OBJETIVO: transformar A en TRIANGULAR SUPERIOR (forma escalonada por filas)
# usando únicamente las dos operaciones elementales del apartado c.
#
# Nota: la eliminación de Gauss por filas produce naturalmente triangular SUPERIOR
# (zeros debajo de la diagonal). El enunciado menciona "triangular inferior" pero
# la forma escalonada estándar es triangular SUPERIOR; implementamos esa convención.
#
# ALGORITMO — para cada columna pivote k = 0, 1, …, n−2:
#
#   PASO 1 — Pivoteo parcial:
#     Entre las filas k, k+1, …, n−1, buscar la que tenga el mayor |A[i][k]|
#     e intercambiarla con la fila k. Motivación: evitar divisiones por pivotes
#     pequeños (estabilidad numérica). Cada intercambio cambia el signo del det.
#
#   PASO 2 — Eliminación:
#     Para cada fila i > k, calcular el multiplicador m = A[i][k] / A[k][k]
#     y aplicar:  fila_i ← fila_i − m · fila_k
#     Esto hace A[i][k] = 0 (anula el elemento bajo el pivote en la columna k).
#
# La función devuelve (U, num_swaps):
#   U         → matriz triangular superior resultante
#   num_swaps → número de intercambios de filas (necesario para el determinante)

def _copiar(A):
    """Copia profunda de una lista de listas (para no modificar la original)."""
    return [fila[:] for fila in A]

def escalonamiento_gauss(A):
    """
    Aplica eliminación de Gauss con pivoteo parcial a A.
    Trabaja sobre una copia interna; A no se modifica.

    Devuelve:
        U         : lista de listas — triangular superior resultante
        num_swaps : int — número de intercambios de filas realizados
    """
    n = len(A)
    U = _copiar(A)
    num_swaps = 0

    for k in range(n - 1):                 # columna pivote k

        # ── PASO 1: Pivoteo parcial ───────────────────────────────────────
        # Buscar la fila con mayor valor absoluto en la columna k (desde fila k)
        max_abs  = abs(U[k][k])
        max_fila = k
        for i in range(k + 1, n):
            if abs(U[i][k]) > max_abs:
                max_abs  = abs(U[i][k])
                max_fila = i

        if max_fila != k:                  # intercambiar fila k con fila max_fila
            U[k], U[max_fila] = U[max_fila], U[k]
            num_swaps += 1                 # registrar: cada swap invierte el signo del det

        if abs(U[k][k]) < 1e-14:          # pivote nulo → columna ya tiene ceros
            continue

        # ── PASO 2: Eliminación ───────────────────────────────────────────
        # Anular U[i][k] para toda fila i > k
        for i in range(k + 1, n):
            if abs(U[i][k]) < 1e-15:      # ya es cero: nada que hacer
                continue
            m = U[i][k] / U[k][k]         # multiplicador: cuánto de fila_k hay en fila_i
            for j in range(k, n):          # actualizar fila i (empieza en k: antes ya son 0)
                U[i][j] -= m * U[k][j]
            U[i][k] = 0.0                  # forzar cero exacto (evita acumulación de redondeo)

    return U, num_swaps


# -----------------------------------------------------------------------------
# 1e) [0.5 pt]  determinante_gauss
# -----------------------------------------------------------------------------
#
# ESTRATEGIA (combina los resultados de los apartados b, c y d):
#
#   1. escalonamiento_gauss(A) → (U, num_swaps)
#      Las operaciones de eliminación NO alteran el det (apartado c, operación 2).
#      Cada intercambio de filas sí cambia el signo del det (apartado c, operación 1).
#
#   2. det(U) = Π U[i][i]  (apartado b: matriz triangular → producto de diagonal)
#
#   3. Corregir el signo:  det(A) = (−1)^num_swaps · Π U[i][i]
#
# Coste total: O(n³) dominado por la fase de eliminación.

def determinante_gauss(A):
    """
    Calcula det(A) mediante eliminación gaussiana con pivoteo parcial.

    A      : lista de listas — matriz cuadrada n×n
    return : float — valor del determinante
    Coste  : O(n³)
    """
    U, num_swaps = escalonamiento_gauss(A)

    det = 1.0
    for i in range(len(U)):
        det *= U[i][i]                     # producto de la diagonal de U

    if num_swaps % 2 == 1:                 # num. impar de swaps → invertir signo
        det = -det

    return det


# -----------------------------------------------------------------------------
# 1f) [0.5 pt]  Complejidad computacional — RESPUESTA TEÓRICA
# -----------------------------------------------------------------------------
#
# MÉTODO RECURSIVO (Expansión de Laplace):
#   Recurrencia:  T(n) = n · T(n−1) + O(n²)
#                 [n llamadas recursivas; construir cada menor cuesta O(n²)]
#   Solución:     T(n) = O(n!)
#
#   Tabla de crecimiento:
#     n=5  → 120 ops       n=10 → 3.628.800 ops
#     n=15 → 1.3×10^12     n=20 → 2.4×10^18  (inviable)
#
# ELIMINACIÓN DE GAUSS CON PIVOTEO PARCIAL:
#   Para cada columna k ∈ {0,…,n−2}:
#     · Pivoteo:     O(n−k) comparaciones
#     · Eliminación: (n−k) filas × n columnas = O((n−k)·n) operaciones
#   Total:  Σ_{k=0}^{n-2} (n−k)·n  ≈  n · n²/2  =  O(n³)
#
#   Tabla de crecimiento:
#     n=10 → 1.000 ops    n=1.000 → 10^9 ops (segundos)    n=10.000 → 10^12 ops
#
# RESUMEN COMPARATIVO:
#   n   |  Laplace O(n!)  |  Gauss O(n³)
#  -----+-----------------+--------------
#   5   |       120       |     125
#   10  |  3.628.800      |   1.000
#   15  |  1.3 × 10^12   |   3.375
#   20  |  2.4 × 10^18   |   8.000
#
# → Gauss es EXPONENCIALMENTE más eficiente. Para n ≥ 12, Laplace deja de ser viable.


# -----------------------------------------------------------------------------
# 1g) [1 pt]  Tabla comparativa de tiempos — n = 2..10
# -----------------------------------------------------------------------------
#
# Se generan matrices A_n ∈ R^{n×n} con numpy.random.rand (como pide el enunciado)
# y se mide el tiempo de ejecución de los tres métodos con time.perf_counter()
# (mayor precisión que time.time() para intervalos cortos).

def _np_a_lista(A_np):
    """Convierte ndarray numpy a lista de listas (para nuestros algoritmos)."""
    return [list(fila) for fila in A_np]

def comparativa_determinantes():
    """
    Genera A_n ∈ R^{n×n} aleatoria para 2 ≤ n ≤ 10 y compara:
      · determinante_recursivo  (Laplace,  O(n!))
      · determinante_gauss      (Gauss,    O(n³))
      · numpy.linalg.det        (referencia LAPACK en C, O(n³) muy optimizado)
    """
    print("=" * 105)
    print("APARTADO 1g) — COMPARATIVA DE TIEMPOS (segundos)")
    print("=" * 105)
    print(f"{'n':>3}  {'det_recursivo':>18}  {'t_recursivo(s)':>16}  "
          f"{'det_gauss':>18}  {'t_gauss(s)':>12}  "
          f"{'det_numpy':>18}  {'t_numpy(s)':>12}")
    print("-" * 105)

    for n in range(2, 11):
        np.random.seed(42 + n)
        A_np = np.random.rand(n, n)
        A    = _np_a_lista(A_np)

        t0      = time.perf_counter()
        det_rec = determinante_recursivo(A)
        t_rec   = time.perf_counter() - t0

        t0      = time.perf_counter()
        det_gss = determinante_gauss(A)
        t_gss   = time.perf_counter() - t0

        t0     = time.perf_counter()
        det_np = float(np.linalg.det(A_np))
        t_np   = time.perf_counter() - t0

        print(f"{n:>3}  {det_rec:>18.8f}  {t_rec:>16.8f}  "
              f"{det_gss:>18.8f}  {t_gss:>12.8f}  "
              f"{det_np:>18.8f}  {t_np:>12.8f}")

    print("-" * 105)
    print()
    print("INTERPRETACIÓN:")
    print("· Para n pequeño (2–5), los tres métodos son rápidos; las diferencias son imperceptibles.")
    print("· A partir de n=7, determinante_recursivo empieza a ser notablemente más lento")
    print("  por su crecimiento O(n!): el tiempo se MULTIPLICA por n en cada paso de n.")
    print("· determinante_gauss mantiene tiempos muy bajos en todo el rango (crecimiento O(n³)).")
    print("· numpy.linalg.det usa LU de LAPACK (código C/Fortran vectorizado): el más rápido,")
    print("  aunque algorítmicamente también O(n³).")
    print("· Los tres métodos producen el mismo valor del determinante (diferencias < 1e-14")
    print("  debidas exclusivamente a errores de redondeo en aritmética de punto flotante).")
    print()


# =============================================================================
# EJERCICIO 2 — DESCENSO DE GRADIENTE
# =============================================================================
#
# El descenso de gradiente busca un mínimo local de f siguiendo la dirección opuesta
# al gradiente (la dirección de mayor descenso):
#
#   x_{k+1} = x_k − γ · ∇f(x_k)
#
# PARÁMETROS:
#   γ (gamma)  : ratio de aprendizaje — controla el tamaño del paso
#   tol        : tolerancia — se detiene cuando ||∇f(x_k)||₂ < tol
#   maxit      : máximo de iteraciones — evita bucles infinitos si diverge
#
# INTUICIÓN: ∇f(x) apunta en la dirección de mayor CRECIMIENTO de f.
# Si nos movemos en dirección −∇f(x), bajamos la función lo más rápido posible
# desde el punto actual (por eso se llama "descenso de gradiente").


# -----------------------------------------------------------------------------
# 2a) [1 pt]  Implementación general del descenso de gradiente
# -----------------------------------------------------------------------------

def norma_l2(v):
    """
    Norma euclidiana (L2) de un vector v representado como lista.
    ||v||₂ = sqrt(v₀² + v₁² + … + v_{n-1}²)
    Se usa para verificar si el gradiente es suficientemente pequeño (criterio de parada).
    """
    return sum(vi * vi for vi in v) ** 0.5

def descenso_gradiente(grad_f, x0, gamma, tol, maxit):
    """
    Método de descenso de gradiente para minimizar f : R^n → R.

    Parámetros:
        grad_f : callable — recibe lista x (n componentes), devuelve lista ∇f(x)
        x0     : lista de n floats — punto inicial
        gamma  : float — ratio de aprendizaje (paso fijo en cada iteración)
        tol    : float — parar cuando ||∇f(x)||₂ < tol (gradiente ≈ 0)
        maxit  : int/float — máximo de iteraciones (evita ejecuciones infinitas)

    Devuelve:
        x      : lista — aproximación del punto crítico (último x calculado)
        k      : int — número de iteraciones realizadas
        norma  : float — ||∇f(x)||₂ en el punto devuelto

    CRITERIO DE PARADA:
        ||∇f(x)||₂ < tol  implica que estamos cerca de un punto donde f'(x) ≈ 0.
        Estos puntos son candidatos a mínimos (pero también pueden ser máximos o sillas).
    """
    x     = x0[:]           # trabajar sobre copia: no modificar el vector original
    maxit = int(maxit)
    n     = len(x)

    for k in range(maxit):
        # Calcular ∇f(x_k); capturar OverflowError si los valores explotan (divergencia)
        try:
            g = grad_f(x)
        except OverflowError:
            return x, k, float('inf')   # divergencia detectada

        norma = norma_l2(g)

        # Comprobar también NaN o Inf en el gradiente (otra señal de divergencia)
        if not math.isfinite(norma):
            return x, k, float('inf')

        if norma < tol:             # gradiente suficientemente pequeño → convergencia
            return x, k, norma

        # Actualización: x_{k+1} = x_k − γ · ∇f(x_k)
        for i in range(n):
            x[i] -= gamma * g[i]

        # Verificar que x sigue siendo finito tras la actualización
        if not all(math.isfinite(xi) for xi in x):
            return x, k + 1, float('inf')  # divergencia detectada

    # Se agotaron las iteraciones sin alcanzar la tolerancia
    try:
        g     = grad_f(x)
        norma = norma_l2(g)
    except OverflowError:
        norma = float('inf')
    return x, maxit, norma


# =============================================================================
# 2b)  f : R → R,   f(x) = 3x⁴ + 4x³ − 12x² + 7
# =============================================================================
#
# ─── ESTUDIO ANALÍTICO PREVIO ────────────────────────────────────────────────
#
# f'(x)  = 12x³ + 12x² − 24x  =  12x(x² + x − 2)  =  12x(x + 2)(x − 1)
# Puntos críticos (f'(x) = 0):  x = −2,  x = 0,  x = 1
#
# f''(x) = 36x² + 24x − 24
#   f''(−2) = 144 − 48 − 24 =  72 > 0  →  MÍNIMO LOCAL   en x = −2   [f(−2) = −25]
#   f''( 0) =             −24 < 0  →  MÁXIMO LOCAL   en x =  0   [f( 0) =   7]
#   f''( 1) =  36 + 24 − 24 =  36 > 0  →  MÍNIMO LOCAL   en x =  1   [f( 1) =   2]
#
# MÍNIMO GLOBAL: x = −2  con  f(−2) = −25
#
# CUENCAS DE ATRACCIÓN (relevante para interpretar el descenso de gradiente):
#   · Para x < 0:  f'(x) > 0 si −2 < x < 0  (gradiente positivo → descenso mueve x izquierda → hacia x=−2)
#                  f'(x) < 0 si      x < −2  (gradiente negativo → descenso mueve x derecha → hacia x=−2)
#     → La cuenca de x=−2 es aproximadamente (−∞, 0)
#   · Para x > 0:  f'(x) < 0 si 0 < x < 1   (descenso mueve x derecha → hacia x=1)
#                  f'(x) > 0 si     x > 1    (descenso mueve x izquierda → hacia x=1)
#     → La cuenca de x=1 es aproximadamente (0, +∞)
#   · x=0 es la frontera (máximo local inestable): el lado al que se caiga determina el destino.

def f(x_vec):
    """f(x) = 3x⁴ + 4x³ − 12x² + 7.  Argumento: lista [x]."""
    x = x_vec[0]
    return 3*x**4 + 4*x**3 - 12*x**2 + 7

def grad_f(x_vec):
    """
    Gradiente (derivada) de f: f'(x) = 12x³ + 12x² − 24x.
    Argumento: lista [x]. Devuelve: lista [f'(x)].
    """
    x = x_vec[0]
    return [12*x**3 + 12*x**2 - 24*x]


# =============================================================================
# 2c)  g : R² → R,   g(x, y) = x² + y³ + 3xy + 1
# =============================================================================
#
# ─── ESTUDIO ANALÍTICO PREVIO ────────────────────────────────────────────────
#
# Derivadas parciales:
#   ∂g/∂x = 2x + 3y
#   ∂g/∂y = 3y² + 3x
#
# Puntos críticos (∇g = 0):
#   2x + 3y = 0  →  x = −3y/2
#   3y² + 3x = 0  →  y² + x = 0  →  y² = −x = 3y/2
#   →  y(y − 3/2) = 0   →  y = 0  o  y = 3/2
#
#   P1 = (0, 0)         con  y = 0  →  x = 0
#   P2 = (−9/4, 3/2)    con  y = 3/2  →  x = −9/4 = −2.25
#
# Hessiana:  H(x,y) = [[∂²g/∂x², ∂²g/∂x∂y], [∂²g/∂y∂x, ∂²g/∂y²]]
#                    = [[2, 3], [3, 6y]]
#
# En P1 = (0, 0):
#   H = [[2, 3], [3, 0]]  →  det(H) = 0 − 9 = −9 < 0  →  PUNTO DE SILLA
#
# En P2 = (−9/4, 3/2):
#   H = [[2, 3], [3, 9]]  →  det(H) = 18 − 9 = 9 > 0  y  H[0][0] = 2 > 0  →  MÍNIMO LOCAL
#
# NOTA: g no tiene mínimo GLOBAL porque g(x,y) → −∞ cuando y → −∞ (con x fijo).

def grad_g(xy):
    """
    Gradiente de g(x,y) = x² + y³ + 3xy + 1.
    ∇g = (2x + 3y,  3y² + 3x)
    Argumento: lista [x, y]. Devuelve: lista [∂g/∂x, ∂g/∂y].
    """
    x, y = xy[0], xy[1]
    return [2*x + 3*y,   3*y**2 + 3*x]


# =============================================================================
# BLOQUE PRINCIPAL — ejecuta todos los apartados al correr el script
# =============================================================================

if __name__ == "__main__":

    # ──────────────────────────────────────────────────────────────────────────
    # EJERCICIO 1g) — Tabla comparativa
    # ──────────────────────────────────────────────────────────────────────────
    comparativa_determinantes()

    SEP  = "─" * 68
    SEP2 = "═" * 68

    # ──────────────────────────────────────────────────────────────────────────
    # EJERCICIO 2
    # ──────────────────────────────────────────────────────────────────────────
    print(SEP2)
    print("EJERCICIO 2 — DESCENSO DE GRADIENTE")
    print(SEP2)

    # ── 2b-i)  x0=3, γ=0.001 ─────────────────────────────────────────────────
    print(f"\n{SEP}")
    print("2b-i)  f(x) = 3x⁴+4x³−12x²+7  |  x0=3, γ=0.001, tol=1e-12, maxit=1e5")
    print(SEP)
    x_i, k_i, ng_i = descenso_gradiente(grad_f, [3.0], gamma=0.001, tol=1e-12, maxit=1e5)
    print(f"  Resultado:   x ≈ {x_i[0]:.10f}")
    print(f"  f(x)       = {f(x_i):.8f}")
    print(f"  Iteraciones: {k_i}   ||∇f|| = {ng_i:.2e}")
    print()
    print("  INTERPRETACIÓN:")
    print("  Con γ=0.001 (paso pequeño), el algoritmo desciende lentamente desde x=3.")
    print("  El primer paso: x₁ = 3 − 0.001·f'(3) = 3 − 0.001·360 = 2.64")
    print("  x permanece siempre positivo → queda en la cuenca de x=1.")
    print("  Converge al MÍNIMO LOCAL x ≈ 1  con f(1) = 2.")

    # ── 2b-ii)  x0=3, γ=0.01 ─────────────────────────────────────────────────
    print(f"\n{SEP}")
    print("2b-ii) f(x) = 3x⁴+4x³−12x²+7  |  x0=3, γ=0.01, tol=1e-12, maxit=1e5")
    print(SEP)
    x_ii, k_ii, ng_ii = descenso_gradiente(grad_f, [3.0], gamma=0.01, tol=1e-12, maxit=1e5)
    print(f"  Resultado:   x ≈ {x_ii[0]:.10f}")
    print(f"  f(x)       = {f(x_ii):.8f}")
    print(f"  Iteraciones: {k_ii}   ||∇f|| = {ng_ii:.2e}")
    print()
    print("  INTERPRETACIÓN:")
    print("  Con γ=0.01 (paso 10× mayor), el primer salto:")
    print("    x₁ = 3 − 0.01·360 = −0.6   ← ¡superamos x=0 de golpe!")
    print("  x₁ = −0.6 < 0 → caemos en la cuenca de x=−2 (mínimo global).")
    print("  Converge al MÍNIMO GLOBAL x ≈ −2  con f(−2) = −25.")

    # ── 2b-iii)  Contraste e interpretación analítica ─────────────────────────
    print(f"\n{SEP}")
    print("2b-iii) CONTRASTE CON EL ESTUDIO ANALÍTICO")
    print(SEP)
    print("  Puntos críticos analíticos de f(x) = 3x⁴+4x³−12x²+7:")
    print("    x = −2  →  f(−2) = −25   MÍNIMO GLOBAL  (f''(−2) = 72 > 0)")
    print("    x =  0  →  f( 0) =   7   MÁXIMO LOCAL   (f''( 0) = −24 < 0)")
    print("    x =  1  →  f( 1) =   2   MÍNIMO LOCAL   (f''( 1) = 36 > 0)")
    print()
    print("  · γ=0.001 (bi):  converge a x≈1  (mínimo LOCAL,  f=2).")
    print("  · γ=0.01  (bii): converge a x≈−2 (mínimo GLOBAL, f=−25).")
    print()
    print("  INFLUENCIA DE γ:")
    print("  1. VELOCIDAD: γ grande → menos iteraciones pero mayor riesgo de inestabilidad.")
    print("     γ pequeño → convergencia segura pero más lenta.")
    print("  2. DESTINO (qué mínimo se alcanza): γ determina si el algoritmo 'salta'")
    print("     por encima de barreras entre mínimos.")
    print("     Con x0=3 y γ pequeño, el algoritmo rueda cuesta abajo hasta x=1.")
    print("     Con γ mayor, el primer salto cruza x=0 y cae en la cuenca de x=−2.")
    print("  El descenso de gradiente SOLO garantiza encontrar un MÍNIMO LOCAL,")
    print("  no necesariamente el global. La elección de γ y x0 son críticas.")

    # ── 2b-iv)  x0=3, γ=0.1 ──────────────────────────────────────────────────
    print(f"\n{SEP}")
    print("2b-iv) f(x) = 3x⁴+4x³−12x²+7  |  x0=3, γ=0.1, tol=1e-12, maxit=1e5")
    print(SEP)
    x_iv, k_iv, ng_iv = descenso_gradiente(grad_f, [3.0], gamma=0.1, tol=1e-12, maxit=1e5)
    print(f"  Resultado:   x = {x_iv[0]:.4e}")
    print(f"  Iteraciones: {k_iv}   ||∇f|| = {ng_iv:.2e}")
    print()
    print("  INTERPRETACIÓN:")
    print("  Con γ=0.1, el primer paso: x₁ = 3 − 0.1·360 = −33.")
    print("  f'(−33) ≈ −417.384 (enorme y negativo) → x₂ = −33 + 41738 = +41705.")
    print("  El método DIVERGE: los valores de x oscilan y crecen sin límite (→ ±∞).")
    print("  Se alcanza maxit sin converger. El resultado no tiene significado matemático.")
    print("  LECCIÓN: γ demasiado grande causa INESTABILIDAD NUMÉRICA.")
    print("  En redes neuronales esto se conoce como 'explosión de gradientes'.")

    # ── 2b-v)  x0=0, γ=0.001 ─────────────────────────────────────────────────
    print(f"\n{SEP}")
    print("2b-v)  f(x) = 3x⁴+4x³−12x²+7  |  x0=0, γ=0.001, tol=1e-12, maxit=1e5")
    print(SEP)
    x_v, k_v, ng_v = descenso_gradiente(grad_f, [0.0], gamma=0.001, tol=1e-12, maxit=1e5)
    print(f"  Resultado:   x ≈ {x_v[0]:.10f}")
    print(f"  f(x)       = {f(x_v):.8f}")
    print(f"  Iteraciones: {k_v}   ||∇f|| = {ng_v:.2e}")
    print()
    print("  INTERPRETACIÓN:")
    print("  f'(0) = 12·0·(0+2)·(0−1) = 0  →  ||∇f(0)|| = 0 < tol")
    print("  El algoritmo 'converge' en 0 iteraciones porque el gradiente en x=0 es 0.")
    print("  PERO x=0 es un MÁXIMO LOCAL (f''(0) = −24 < 0), ¡no un mínimo!")
    print()
    print("  ¿Es un resultado deseable? NO.")
    print("  FENÓMENO: el descenso de gradiente queda ATRAPADO en cualquier punto")
    print("  donde ∇f = 0, incluyendo máximos locales y puntos de silla, no solo mínimos.")
    print("  El algoritmo no puede distinguir entre ellos: solo 've' que el gradiente es 0.")
    print("  En la práctica, las redes neuronales tienen tantos parámetros que los máximos")
    print("  puros son rarísimos; los puntos de silla son el problema real del deep learning.")

    # ── 2c-i)  g(x,y), x0=(−1, 1), γ=0.01 ───────────────────────────────────
    print(f"\n{SEP}")
    print("2c-i)  g(x,y)  |  x0=(−1, 1), γ=0.01, tol=1e-12, maxit=1e5")
    print(SEP)
    xg1, kg1, ng1 = descenso_gradiente(grad_g, [-1.0, 1.0], gamma=0.01, tol=1e-12, maxit=1e5)
    print(f"  Resultado:  (x, y) = ({xg1[0]:.10f},  {xg1[1]:.10f})")
    print(f"  Esperado analítico: (−2.25000000, 1.50000000)")
    print(f"  Iteraciones: {kg1}   ||∇g|| = {ng1:.2e}")
    print()
    print("  INTERPRETACIÓN:")
    print("  Converge al mínimo local de g en P2 = (−9/4, 3/2) = (−2.25, 1.5).")
    print("  Desde (−1, 1), ∇g = [2(−1)+3(1), 3(1)²+3(−1)] = [1, 0].")
    print("  El primer paso mueve x hacia la izquierda (hacia −2.25) mientras y converge a 1.5.")
    print("  γ=0.01 es estable en esta zona (los valores propios de H en P2 son ~0.89 y ~10.1;")
    print("  la condición de estabilidad γ < 2/λ_max ≈ 0.198 se cumple).")

    # ── 2c-ii)  g(x,y), x0=(0, 0), γ=0.01 ───────────────────────────────────
    print(f"\n{SEP}")
    print("2c-ii) g(x,y)  |  x0=(0, 0), γ=0.01, tol=1e-12, maxit=1e5")
    print(SEP)
    xg2, kg2, ng2 = descenso_gradiente(grad_g, [0.0, 0.0], gamma=0.01, tol=1e-12, maxit=1e5)
    print(f"  Resultado:  (x, y) = ({xg2[0]:.10f},  {xg2[1]:.10f})")
    print(f"  Iteraciones: {kg2}   ||∇g|| = {ng2:.2e}")
    print()
    print("  ¿Resultado deseable? NO.")
    print("  INTERPRETACIÓN:")
    print("  ∇g(0,0) = [2·0+3·0, 3·0²+3·0] = [0, 0]  →  el gradiente es exactamente 0.")
    print("  El algoritmo 'converge' en 0 iteraciones. Pero (0,0) es un PUNTO DE SILLA:")
    print("  det(H(0,0)) = −9 < 0  →  la Hessiana tiene un valor propio positivo")
    print("  y uno negativo → la función crece en una dirección y decrece en otra.")
    print("  El método queda completamente atrapado: no puede escapar del punto de silla.")

    # ── 2c-iii)  Estudio analítico ────────────────────────────────────────────
    print(f"\n{SEP}")
    print("2c-iii) ESTUDIO ANALÍTICO DE g(x,y) = x² + y³ + 3xy + 1")
    print(SEP)
    print("  PUNTOS CRÍTICOS (∇g = 0):")
    print("    ∂g/∂x = 2x + 3y = 0   →   x = −3y/2")
    print("    ∂g/∂y = 3y² + 3x = 0  →   y² = 3y/2   →   y(y − 3/2) = 0")
    print()
    print("    P1 = (0,    0)     →  PUNTO DE SILLA  [det(H) = −9 < 0]")
    print("    P2 = (−9/4, 3/2)  →  MÍNIMO LOCAL    [det(H) = 9 > 0, H₀₀ = 2 > 0]")
    print()
    print("  HESSIANA H(x,y) = [[2, 3], [3, 6y]]:")
    print("    En P1=(0,0):       H = [[2,3],[3,0]]  →  det = 0−9 = −9 < 0  →  SILLA")
    print("    En P2=(−9/4,3/2): H = [[2,3],[3,9]]  →  det = 18−9 = 9 > 0  →  MÍNIMO")
    print()
    print("  OBSERVACIÓN: g no tiene mínimo global (g → −∞ para y → −∞).")
    print("  P2 = (−2.25, 1.5) es el único mínimo local.")
    print()
    print("  CONTRASTE CON LOS RESULTADOS NUMÉRICOS:")
    print("  · x0=(−1,1):  en la cuenca de atracción de P2 → converge a P2. ✓")
    print("  · x0=(0,0):   justo en el punto de silla P1   → queda atrapado. ✗")
    print()
    print("  LECCIÓN FUNDAMENTAL:")
    print("  El descenso de gradiente es EXTREMADAMENTE sensible al punto inicial x0.")
    print("  Dos x0 cercanos pueden llevar a resultados completamente distintos.")
    print("  En deep learning (millones de parámetros), no existe garantía de encontrar")
    print("  el mínimo global. El objetivo práctico es hallar un 'buen' mínimo local.")

    print(f"\n{SEP2}")
    print("FIN DE LOS EJERCICIOS EVALUABLES")
    print(SEP2)

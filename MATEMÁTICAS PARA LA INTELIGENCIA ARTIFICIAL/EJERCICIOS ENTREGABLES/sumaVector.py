"""
====================================================================
EXPLICACION PASO A PASO: Como encontrar minimos y maximos
====================================================================
Funcion de ejemplo:  f(x) = 3x^4 + 4x^3 - 12x^2 + 7

Este script hace EXACTAMENTE lo mismo que el notebook original,
pero con comentarios y mensajes que explican cada paso, para que
puedas seguirlo mientras estudias derivadas en tu curso.

Al final se genera tambien una GRAFICA (matplotlib) que muestra:
  - la curva completa de f(x)
  - el minimo global (verde)
  - el maximo local (rojo)
  - el minimo local (azul)
  - flechas indicando si la curva sube o baja en cada tramo
====================================================================
"""

import matplotlib.pyplot as plt
import numpy as np

print("=" * 70)
print("PASO 0: La funcion con la que vamos a trabajar")
print("=" * 70)
print("""
f(x) = 3x^4 + 4x^3 - 12x^2 + 7

Piensa en f(x) como la ALTURA de una montaña en la posicion x.
Vamos a caminar sobre esa montaña con las derivadas.
""")


def f(x):
    """La funcion original: nos da la ALTURA en el punto x."""
    return 3 * x**4 + 4 * x**3 - 12 * x**2 + 7


# --------------------------------------------------------------
# PASO 1: PRIMERA DERIVADA -> nos dice la PENDIENTE (inclinacion)
# --------------------------------------------------------------
print("=" * 70)
print("PASO 1: Primera derivada f'(x) -- la PENDIENTE del terreno")
print("=" * 70)
print("""
La derivada de una funcion te dice que tan inclinado esta el
terreno en cada punto x. Es como preguntar:

    "Si estoy parado en x, hacia donde apunta la pendiente?
     hacia arriba (subiendo)? hacia abajo (bajando)? o esta
     completamente plano (ni sube ni baja)?"

Para derivar 3x^4 + 4x^3 - 12x^2 + 7, se usa una regla simple:
para cada termino a*x^n, la derivada es (a*n)*x^(n-1).

    3x^4   -> 3*4 * x^3        = 12x^3
    4x^3   -> 4*3 * x^2        = 12x^2
   -12x^2  -> -12*2 * x^1      = -24x
    +7     -> (constante, no aporta pendiente) = 0

Sumando todo:

    f'(x) = 12x^3 + 12x^2 - 24x
""")


def f_prima(x):
    """Primera derivada: nos da la PENDIENTE en el punto x."""
    return 12 * x**3 + 12 * x**2 - 24 * x


print(">>> Verificacion: evaluamos f'(x) en varios puntos <<<\n")
for x_prueba in [-3, -2, -1, 0, 0.5, 1, 2]:
    pendiente = f_prima(x_prueba)
    if pendiente > 0:
        estado = "subiendo"
    elif pendiente < 0:
        estado = "bajando"
    else:
        estado = "PLANO (punto especial)"
    print(f"  En x = {x_prueba:>5}:  f'(x) = {pendiente:>8.2f}   -> {estado}")

print("""
Fijate que en x = -2, x = 0 y x = 1 la pendiente da CERO.
Esos son los "puntos especiales": ahi la curva deja de subir
o bajar por un instante. Vamos a encontrarlos formalmente.
""")


# --------------------------------------------------------------
# PASO 2: IGUALAR LA DERIVADA A CERO -> encontrar puntos criticos
# --------------------------------------------------------------
print("=" * 70)
print("PASO 2: Igualar f'(x) = 0 -- encontrar los puntos planos")
print("=" * 70)
print("""
Para encontrar EXACTAMENTE donde la pendiente es cero, resolvemos
la ecuacion:

    12x^3 + 12x^2 - 24x = 0

Primero sacamos 12x en factor comun:

    12x * (x^2 + x - 2) = 0

Luego factorizamos x^2 + x - 2 en dos parentesis:

    12x * (x + 2) * (x - 1) = 0

Un producto es cero cuando AL MENOS UNO de sus factores es cero:

    x = 0        (del primer factor)
    x + 2 = 0  -> x = -2
    x - 1 = 0  -> x = 1

Resultado: los puntos criticos son x = -2, x = 0, x = 1
""")

puntos_criticos = [-2, 0, 1]

print(">>> Verificacion numerica: f'(x) debe dar 0 en estos puntos <<<\n")
for x in puntos_criticos:
    print(f"  f'({x}) = {f_prima(x):.6f}   (debe ser 0)")


# --------------------------------------------------------------
# PASO 3: SEGUNDA DERIVADA -> nos dice la CURVATURA (pico o valle)
# --------------------------------------------------------------
print("\n" + "=" * 70)
print("PASO 3: Segunda derivada f''(x) -- la CURVATURA del terreno")
print("=" * 70)
print("""
Ya sabemos DONDE esta plano el terreno (x = -2, 0, 1).
Pero necesitamos saber QUE TIPO de punto plano es cada uno:

    - Si el terreno esta curvado como un CUENCO (forma de U),
      ese punto plano es el FONDO de un valle -> MINIMO.

    - Si el terreno esta curvado como una COLINA (forma de U
      invertida, forma de "n"), ese punto plano es la CIMA
      de un pico -> MAXIMO.

Para saber la curvatura, derivamos OTRA VEZ (derivamos la
derivada). Eso se llama "segunda derivada".

Derivamos f'(x) = 12x^3 + 12x^2 - 24x, termino por termino:

    12x^3  ->  12*3 * x^2   = 36x^2
    12x^2  ->  12*2 * x^1   = 24x
   -24x    ->  -24 (constante)

Sumando todo:

    f''(x) = 36x^2 + 24x - 24
""")


def f_segunda(x):
    """Segunda derivada: nos dice si el punto es un valle o un pico."""
    return 36 * x**2 + 24 * x - 24


# --------------------------------------------------------------
# PASO 4: CLASIFICAR CADA PUNTO (evaluando la segunda derivada)
# --------------------------------------------------------------
print("=" * 70)
print("PASO 4: Evaluar f''(x) en cada punto critico para clasificar")
print("=" * 70)
print("""
Regla simple:

    f''(x) > 0   ->   curvatura hacia ARRIBA (cuenco)  -> MINIMO
    f''(x) < 0   ->   curvatura hacia ABAJO (colina)    -> MAXIMO
""")

resultados = []
for x in puntos_criticos:
    altura = f(x)
    segunda = f_segunda(x)
    if segunda > 0:
        tipo = "MINIMO (valle)"
    elif segunda < 0:
        tipo = "MAXIMO (pico)"
    else:
        tipo = "indeterminado, hace falta otro analisis"

    resultados.append((x, altura, segunda, tipo))

    print(f"  x = {x}")
    print(f"    altura de la montaña aqui:  f({x})  = {altura:.2f}")
    print(f"    curvatura aqui:             f''({x}) = {segunda:.2f}")
    print(f"    conclusion:                 {tipo}")
    print()


# --------------------------------------------------------------
# PASO 5: COMPARAR VALORES -> decidir GLOBAL vs LOCAL
# --------------------------------------------------------------
print("=" * 70)
print("PASO 5: Comparar alturas -- decidir si es GLOBAL o solo LOCAL")
print("=" * 70)
print("""
Ya sabemos cuales son valles y cuales son picos. Pero falta un
paso: un valle puede ser "el mas profundo de TODA la montaña"
(eso se llama GLOBAL) o puede ser solo "el mas profundo de ESA
ZONA nada mas" (eso se llama LOCAL).

Para decidirlo, comparamos las ALTURAS reales de los valles
entre si (y lo mismo se haria con los picos si hubiera mas de
uno).
""")

minimos = [(x, alt) for (x, alt, _, tipo) in resultados if "MINIMO" in tipo]
maximos = [(x, alt) for (x, alt, _, tipo) in resultados if "MAXIMO" in tipo]

print("  Valles encontrados (candidatos a minimo):")
for x, alt in minimos:
    print(f"    x = {x:>3}   altura = {alt:>8.2f}")

if minimos:
    x_global, alt_global = min(minimos, key=lambda t: t[1])
    print(f"\n  El valle mas profundo es x = {x_global} con altura {alt_global:.2f}")
    print(f"  -> ese es el MINIMO GLOBAL.")
    for x, alt in minimos:
        if x != x_global:
            print(f"  -> x = {x} (altura {alt:.2f}) es MINIMO LOCAL, "
                  f"porque {alt:.2f} > {alt_global:.2f} (no es el mas bajo de todos).")

print("\n  Picos encontrados (candidatos a maximo):")
for x, alt in maximos:
    print(f"    x = {x:>3}   altura = {alt:>8.2f}")

print("""
  Nota importante: como f(x) tiene grado 4 con coeficiente
  positivo (el 3 de 3x^4), la montaña SUBE SIN LIMITE hacia
  ambos lados (hacia x muy negativo y hacia x muy positivo).
  Por eso NINGUN pico puede ser "el mas alto de toda la
  montaña": siempre hay algo mas alto mas lejos.
  Entonces todos los picos que encontremos seran MAXIMOS LOCALES,
  nunca maximo global.
""")


# --------------------------------------------------------------
# RESUMEN FINAL
# --------------------------------------------------------------
print("=" * 70)
print("RESUMEN FINAL")
print("=" * 70)
encabezado_segunda_deriv = "f''(x)"
print(f"{'x':>6}  {'f(x)':>8}  {encabezado_segunda_deriv:>8}   Clasificacion")
print("-" * 55)
for x, alt, segunda, tipo in resultados:
    if x == x_global:
        etiqueta = "MINIMO GLOBAL"
    elif "MINIMO" in tipo:
        etiqueta = "minimo local"
    else:
        etiqueta = "maximo local"
    print(f"{x:>6}  {alt:>8.2f}  {segunda:>8.2f}   {etiqueta}")

print("""
En tres pasos:
  1) f'(x) = 0        -> encuentra los puntos "planos"
  2) f''(x) evaluado  -> clasifica cada punto: valle o pico
  3) comparar alturas -> decide si es el extremo de TODA la
                          grafica (global) o solo de su zona (local)
""")


# ====================================================================
# PASO 6: GRAFICA -- ver todo esto de forma visual
# ====================================================================
print("=" * 70)
print("PASO 6: Generando la grafica...")
print("=" * 70)
print("""
Ahora vamos a DIBUJAR la funcion f(x) para ver con los ojos todo lo
que acabamos de calcular con numeros:

  - La linea gris es la curva completa de f(x).
  - El punto VERDE es el minimo global (el valle mas profundo).
  - El punto ROJO es el maximo local (la cima).
  - El punto AZUL es el minimo local (el otro valle, menos profundo).
  - Las flechas muestran hacia donde "camina" la curva en cada tramo:
    subiendo o bajando.
""")

# Generamos muchos puntos de x para dibujar una curva suave
x_vals = np.linspace(-4, 3, 600)
y_vals = f(x_vals)

fig, ax = plt.subplots(figsize=(10, 7))

# 1) La curva completa
ax.plot(x_vals, y_vals, color="#555555", linewidth=2, label="f(x) = 3x^4 + 4x^3 - 12x^2 + 7")

# 2) Los tres puntos especiales, coloreados segun su clasificacion
colores = {"MINIMO GLOBAL": "green", "minimo local": "blue", "maximo local": "red"}
marcadores = {"MINIMO GLOBAL": "o", "minimo local": "^", "maximo local": "s"}

for x, alt, segunda, tipo in resultados:
    etiqueta = "MINIMO GLOBAL" if x == x_global else ("minimo local" if "MINIMO" in tipo else "maximo local")
    ax.scatter(
        x, alt,
        color=colores[etiqueta],
        marker=marcadores[etiqueta],
        s=180,
        zorder=5,
        edgecolor="black",
        label=f"{etiqueta}  (x={x}, f(x)={alt:.0f})"
    )
    # Texto al lado de cada punto
    ax.annotate(
        f"{etiqueta}\n({x}, {alt:.0f})",
        xy=(x, alt),
        xytext=(x + 0.3, alt + (10 if alt < 0 else 6)),
        fontsize=9,
        fontweight="bold",
        color=colores[etiqueta],
    )

# 3) Flechas mostrando "subiendo" / "bajando" en cada tramo, usando
#    el signo de la primera derivada (igual que en el Paso 1)
tramos_muestra = [-3.3, -1, 0.5, 2.3]
for xt in tramos_muestra:
    pendiente = f_prima(xt)
    direccion = 1 if pendiente > 0 else -1
    ax.annotate(
        "",
        xy=(xt + 0.35 * direccion, f(xt + 0.35 * direccion)),
        xytext=(xt, f(xt)),
        arrowprops=dict(arrowstyle="->", color="gray", lw=1.5),
    )

# 4) Detalles esteticos
ax.axhline(0, color="lightgray", linewidth=0.8, zorder=0)
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_title("f(x) = 3x^4 + 4x^3 - 12x^2 + 7\ny sus puntos criticos (minimo global, maximo local, minimo local)")
ax.legend(loc="upper center", fontsize=8)
ax.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig("grafica_puntos_criticos.png", dpi=150)
print("Grafica guardada como: grafica_puntos_criticos.png")
plt.show()
"""
Práctica 28-05-2026 — Matemáticas para la Inteligencia Artificial
Máster Universitario en Inteligencia Artificial
Profesora: Zoraida Sivoli Barrios

Programa de práctica interactivo en consola.
Cada ejercicio explica la teoría, la fórmula y la solución paso a paso.
"""

import math
import random
from collections import Counter


# ─────────────────────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────────────────────

def sep(c="=", n=68): print(c * n)
def linea():          sep("-")

def titulo(texto):
    sep()
    print(f"  {texto}")
    sep()

def subtitulo(texto):
    print()
    linea()
    print(f"  {texto}")
    linea()

def pausa(msg="  [Enter para continuar...] "):
    input(f"\n{msg}")

def pedir(msg="  Tu respuesta: "):
    raw = input(f"\n{msg}").strip()
    # Limpiar prefijos comunes que el usuario puede copiar del contexto:
    # "=288", "= 288", "288 ordenaciones", etc.
    raw = raw.lstrip("=: ").split()[0] if raw.lstrip("=: ") else raw
    return raw

def verificar(resp, correcto):
    try:
        if int(resp) == int(correcto):
            print(f"\n  CORRECTO! La respuesta es {correcto}.")
            return True
    except (ValueError, TypeError):
        pass
    print(f"\n  Incorrecto. Escribiste: '{resp}' | Respuesta correcta: {correcto}")
    print(f"  (Escribe solo el numero, sin signos como = o espacios extra)")
    return False

def bloque(titulo_bloque, texto):
    """Muestra un bloque enmarcado de teoría."""
    print()
    print(f"  {'─'*60}")
    print(f"  | {titulo_bloque}")
    print(f"  {'─'*60}")
    for linea_txt in texto.strip().split("\n"):
        print(f"  {linea_txt}")
    print(f"  {'─'*60}")


# ─────────────────────────────────────────────────────────────
# CONECTORES LÓGICOS
# ─────────────────────────────────────────────────────────────

def impl(p, q):  return 0 if (p == 1 and q == 0) else 1
def bicond(p, q): return 1 if p == q else 0
def conj(p, q):  return p & q
def disy(p, q):  return p | q
def neg(p):      return 1 - p

FILAS_2 = [(1, 1), (1, 0), (0, 1), (0, 0)]


# ═══════════════════════════════════════════════════════════════
#   BLOQUE 1 — COMBINATORIA  (Ejercicios 1-7)
# ═══════════════════════════════════════════════════════════════

def teoria_combinatoria():
    titulo("TEORÍA COMPLETA — COMBINATORIA")
    print("""
  La combinatoria cuenta de cuántas formas se pueden elegir o
  arreglar elementos. Antes de aplicar una fórmula, hazte
  SIEMPRE estas dos preguntas:

  ╔══════════════════════════════════════════════════════════╗
  ║  PREGUNTA 1: ¿El ORDEN importa?                         ║
  ║  PREGUNTA 2: ¿Se pueden REPETIR los elementos?          ║
  ╚══════════════════════════════════════════════════════════╝

  Dependiendo de las respuestas, usas una fórmula distinta:

  ┌────────────────────────┬──────────┬────────────┬─────────────────────────┐
  │ Tipo                   │ ¿Orden?  │ ¿Repet.?   │ Fórmula                 │
  ├────────────────────────┼──────────┼────────────┼─────────────────────────┤
  │ Permutación total      │   SÍ     │   NO       │ n!                      │
  │ Variación sin rep.     │   SÍ     │   NO       │ n! / (n-r)!             │
  │ Variación con rep.     │   SÍ     │   SÍ       │ n^r                     │
  │ Combinación sin rep.   │   NO     │   NO       │ n! / (r! · (n-r)!)      │
  │ Combinación con rep.   │   NO     │   SÍ       │ (n+r-1)! / (r! · (n-1)!)│
  │ Perm. con repetición   │   SÍ     │   (letras) │ n! / (n1! · n2! · …)   │
  └────────────────────────┴──────────┴────────────┴─────────────────────────┘

  QUÉ SIGNIFICA n! (factorial):
    n! = n × (n-1) × (n-2) × … × 2 × 1
    Ejemplo: 4! = 4 × 3 × 2 × 1 = 24
    Representa el total de formas de ordenar n objetos distintos.

  TRUCO para identificar el tipo:
    • Medallas, puestos, rankings   → orden SÍ importa
    • Comités, equipos, conjuntos   → orden NO importa
    • Contraseñas, códigos PIN      → repetición permitida
    • Letras de una misma palabra   → permutación con repetición
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej1_libros_orden_fijo():
    titulo("EJERCICIO 1 — Libros con grupos en ORDEN FIJO")

    print("""
  ENUNCIADO:
  La Sra. Torres tiene 10 libros: 4 de matemáticas, 3 de química,
  2 de historia y 1 de idiomas.
  Quiere que los grupos vayan en ese orden exacto:
    1º Matemáticas → 2º Química → 3º Historia → 4º Idiomas
  ¿Cuántas ordenaciones distintas son posibles?
""")

    subtitulo("PASO 1 — Entender qué está FIJO y qué es LIBRE")
    print("""
  Lo que está FIJO:
    El ORDEN de los grupos no cambia. Matemáticas va primero,
    química segundo, etc. No hay elección en eso.

  Lo que es LIBRE:
    Dentro de cada grupo, los libros del mismo tema se pueden
    ordenar entre sí de cualquier manera.
    Ejemplo: los 4 libros de matemáticas pueden ir en 4! órdenes distintos.
""")

    subtitulo("PASO 2 — La fórmula que se aplica: Permutación")
    print("""
  Una PERMUTACIÓN es el total de formas de ordenar n objetos distintos.

    Fórmula:  n! = n × (n-1) × (n-2) × … × 1

  ¿Por qué n!?
    Imagina que tienes n sillas en fila y n personas.
    Para la primera silla tienes n opciones.
    Para la segunda silla tienes (n-1) opciones (una persona ya está sentada).
    Para la tercera silla tienes (n-2) opciones.
    ... y así hasta que solo queda 1 opción para la última silla.
    Total: n × (n-1) × … × 1 = n!
""")

    subtitulo("PASO 3 — Aplicar al problema")
    f4 = math.factorial(4)
    f3 = math.factorial(3)
    f2 = math.factorial(2)
    f1 = math.factorial(1)
    print(f"""
  Grupo de Matemáticas (4 libros) → 4! = {f4} ordenaciones internas
  Grupo de Química     (3 libros) → 3! = {f3} ordenaciones internas
  Grupo de Historia    (2 libros) → 2! = {f2} ordenaciones internas
  Grupo de Idiomas     (1 libro)  → 1! = {f1} ordenación interna

  Regla del producto:
    Si el evento A ocurre de 'a' formas Y el evento B ocurre de 'b' formas,
    juntos ocurren de a × b formas.
    (Cada ordenación interna de un grupo es independiente de la otra.)

  Total = 4! × 3! × 2! × 1!
        = {f4} × {f3} × {f2} × {f1}
""")

    resultado = f4 * f3 * f2 * f1
    resp = pedir("Escribe el resultado (solo el numero): ")
    verificar(resp, resultado)
    print(f"\n  Solucion: {f4} x {f3} x {f2} x {f1} = {resultado}")

    subtitulo("CONCLUSIÓN")
    print(f"""
  Hay {resultado} formas distintas de ordenar los libros.
  No multiplicamos los grupos entre sí porque su POSICIÓN ya está fija.
  Solo contamos los órdenes posibles DENTRO de cada grupo.
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej2_libros_orden_libre():
    titulo("EJERCICIO 2 — Libros con grupos en ORDEN LIBRE")

    print("""
  ENUNCIADO:
  Los mismos 10 libros: 4 matemáticas, 3 química, 2 historia, 1 idiomas.
  Condición: todos los libros del mismo tema deben ir JUNTOS.
  Pero ahora los grupos pueden ir en CUALQUIER orden.
  ¿Cuántas ordenaciones distintas son posibles?
""")

    subtitulo("PASO 1 — Comparar con el Ejercicio 1")
    print("""
  En el Ej.1 el orden de grupos era fijo: mat → quím → hist → id.
  Aquí el orden de los grupos TAMBIÉN puede cambiar.

  Podría ser:
    Química → Matemáticas → Idiomas → Historia
    Historia → Química → Matemáticas → Idiomas
    … cualquier orden de los 4 grupos.
""")

    subtitulo("PASO 2 — Contar de cuántas formas se pueden ordenar los grupos")
    print("""
  Tenemos 4 grupos distintos. ¿De cuántas formas se pueden ordenar 4 grupos?

  Aplicamos la fórmula de permutación: n! con n = 4 grupos.

  Imagina que los 4 grupos son 4 "cajas":
    [ MAT ] [ QUÍM ] [ HIST ] [ IDIOM ]

  Para la posición 1: cualquiera de 4 cajas → 4 opciones
  Para la posición 2: quedan 3 cajas        → 3 opciones
  Para la posición 3: quedan 2 cajas        → 2 opciones
  Para la posición 4: queda 1 caja          → 1 opción

  Total de órdenes de grupos = 4! = 4 × 3 × 2 × 1 = 24
""")

    subtitulo("PASO 3 — Ordenaciones internas de cada grupo (igual que Ej.1)")
    f4, f3, f2, f1 = math.factorial(4), math.factorial(3), math.factorial(2), 1
    print(f"""
  Dentro de cada grupo, los libros también se pueden permutar:
    Matemáticas: 4! = {f4}
    Química:     3! = {f3}
    Historia:    2! = {f2}
    Idiomas:     1! = {f1}

  Permutaciones internas = 4! × 3! × 2! × 1! = {f4 * f3 * f2 * f1}
""")

    subtitulo("PASO 4 — Aplicar la Regla del Producto")
    perm_grupos  = math.factorial(4)
    perm_int     = f4 * f3 * f2 * f1
    resultado    = perm_grupos * perm_int
    print(f"""
  Cada orden de grupos se combina con cada orden interno.
  Todos son independientes entre sí → multiplicamos.

  Total = (órdenes de grupos) × (permutaciones internas)
        = 4!  ×  (4! × 3! × 2! × 1!)
        = {perm_grupos}  ×  {perm_int}
""")

    resp = pedir(f"Escribe el resultado de {perm_grupos} x {perm_int} (solo el numero): ")
    verificar(resp, resultado)
    print(f"\n  Solucion: {perm_grupos} x {perm_int} = {resultado}")

    subtitulo("CONCLUSIÓN — Diferencia clave con Ej.1")
    print(f"""
  Ej.1 (orden fijo):   {f4 * f3 * f2 * f1}  ordenaciones
  Ej.2 (orden libre):  {resultado}  ordenaciones

  La diferencia es exactamente el factor 4! = 24 (los órdenes de grupos).
  Siempre que los grupos son intercambiables, hay que multiplicar por k!
  donde k es el número de grupos.
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej3_medallas():
    titulo("EJERCICIO 3 — Variación sin repetición (medallas)")

    print("""
  ENUNCIADO:
  En una carrera participan 10 atletas.
  ¿De cuántas formas distintas se pueden otorgar las medallas
  de oro, plata y bronce?
""")

    subtitulo("PASO 1 — Las dos preguntas clave")
    print("""
  ¿El orden importa?
    SÍ. Oro ≠ Plata ≠ Bronce.
    Si Ana gana oro y Bob gana plata → es distinto a que Bob gane oro y Ana plata.

  ¿Se puede repetir?
    NO. El mismo atleta no puede ganar dos medallas.

  Conclusión: usamos VARIACIÓN SIN REPETICIÓN.
""")

    subtitulo("PASO 2 — Por qué la fórmula es n! / (n-r)!")
    print("""
  Queremos elegir r=3 atletas de n=10, en un ORDEN específico.

  Piénsalo posición por posición:
    Oro   → cualquiera de los 10 atletas → 10 opciones
    Plata → cualquiera de los 9 restantes →  9 opciones
    Bronce→ cualquiera de los 8 restantes →  8 opciones

  Total = 10 × 9 × 8

  ¿Por qué esto es n!/(n-r)!?
    10! = 10 × 9 × 8 × 7 × 6 × 5 × 4 × 3 × 2 × 1
    7!  =              7 × 6 × 5 × 4 × 3 × 2 × 1

    10! / 7! = (10 × 9 × 8 × 7!) / 7! = 10 × 9 × 8

    Es decir: 10! / (10-3)! = 10! / 7! = 10 × 9 × 8
    Los factores que "se cancelan" son los atletas que no compiten.

  Fórmula general: V(n,r) = n! / (n-r)! = n × (n-1) × … × (n-r+1)
""")

    subtitulo("PASO 3 — Calcular")
    print("""
  V(10, 3) = 10 × 9 × 8 = ?
""")
    resultado = math.perm(10, 3)
    resp = pedir("Escribe el resultado de 10 x 9 x 8 (solo el numero): ")
    verificar(resp, resultado)
    print(f"\n  Solucion: 10 x 9 x 8 = {resultado}")

    subtitulo("CONCLUSIÓN")
    print(f"""
  Hay {resultado} formas distintas de otorgar las tres medallas.
  La clave fue: orden importa + sin repetición → V(n,r) = n!/(n-r)!
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej4_codigos():
    titulo("EJERCICIO 4 — Variación CON repetición (códigos)")

    print("""
  ENUNCIADO:
  Una empresa fabrica códigos de 4 dígitos usando los números del 0 al 9.
  Los dígitos PUEDEN repetirse (p.ej. "1122" es válido).
  ¿Cuántos códigos distintos se pueden formar?
""")

    subtitulo("PASO 1 — Las dos preguntas clave")
    print("""
  ¿El orden importa?
    SÍ. El código "1234" es distinto a "4321".

  ¿Se puede repetir?
    SÍ. El enunciado lo dice explícitamente.

  Conclusión: usamos VARIACIÓN CON REPETICIÓN.
""")

    subtitulo("PASO 2 — Por qué la fórmula es n^r")
    print("""
  Tenemos 4 posiciones (r=4) y en cada posición podemos poner
  cualquiera de los 10 dígitos (n=10), independientemente de
  qué pusimos en las otras posiciones.

  Posición 1: 10 opciones (0,1,2,...,9)
  Posición 2: 10 opciones (puede repetirse el de la pos.1)
  Posición 3: 10 opciones
  Posición 4: 10 opciones

  Regla del producto → 10 × 10 × 10 × 10 = 10⁴

  La fórmula n^r dice: n opciones elegidas r veces de forma independiente.
  Cada posición es un evento independiente con n resultados posibles.
""")

    subtitulo("PASO 3 — Calcular")
    print("""
  10⁴ = 10 × 10 × 10 × 10 = ?
""")
    resultado = 10 ** 4
    resp = pedir("Escribe el resultado de 10 elevado a la 4 (solo el numero): ")
    verificar(resp, resultado)
    print(f"\n  Solucion: 10^4 = {resultado}")

    subtitulo("CONCLUSIÓN")
    print(f"""
  Hay {resultado} códigos distintos posibles.

  Nota comparativa:
    Sin repetición habría sido V(10,4) = 10×9×8×7 = {math.perm(10,4)} códigos.
    Con repetición hay {resultado}. La repetición AUMENTA las posibilidades.
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej5_comite():
    titulo("EJERCICIO 5 — Combinación sin repetición (comité)")

    print("""
  ENUNCIADO:
  En un grupo de 12 estudiantes se quiere formar un comité de 3 personas.
  ¿De cuántas maneras distintas se puede formar el comité?
""")

    subtitulo("PASO 1 — Las dos preguntas clave")
    print("""
  ¿El orden importa?
    NO. El comité {Ana, Bob, Carlos} es el mismo sin importar
    en qué orden los nombremos: {Carlos, Ana, Bob} = mismo comité.

  ¿Se puede repetir?
    NO. Una persona no puede estar dos veces en el mismo comité.

  Conclusión: usamos COMBINACIÓN SIN REPETICIÓN.
""")

    subtitulo("PASO 2 — Por qué la fórmula es C(n,r) = n! / (r! · (n-r)!)")
    print("""
  Primero contamos COMO SI el orden importara → usaríamos V(12,3):
    12 × 11 × 10 = 1320 (variaciones)

  Pero en un comité, {Ana,Bob,Carlos} y {Bob,Ana,Carlos} son lo mismo.
  ¿Cuántas veces estamos contando cada grupo de 3 personas?
    Las mismas 3 personas se pueden ordenar de 3! = 6 formas distintas.
    (ABC, ACB, BAC, BCA, CAB, CBA → 6 órdenes, 1 solo comité)

  Para no contar repetidos, dividimos entre r!:
    C(12,3) = V(12,3) / 3! = 1320 / 6

  Fórmula general:
    C(n,r) = n! / (r! · (n-r)!)

  ¿Cómo leerla?
    n!     → ordena todos los n elementos
    (n-r)! → cancela los elementos que NO elegimos
    r!     → elimina las repeticiones por orden dentro del grupo elegido
""")

    subtitulo("PASO 3 — Calcular")
    num = 12 * 11 * 10
    den = math.factorial(3)
    resultado = math.comb(12, 3)
    print(f"""
  C(12, 3) = (12 × 11 × 10) / (3 × 2 × 1)
           = {num} / {den}
           = ?
""")
    resp = pedir(f"Escribe el resultado de {num} / {den} (solo el numero): ")
    verificar(resp, resultado)
    print(f"\n  Solucion: {num} / {den} = {resultado}")

    subtitulo("CONCLUSIÓN")
    print(f"""
  Hay {resultado} comités distintos posibles.
  La clave fue: orden NO importa + sin repetición → C(n,r) = n!/(r!·(n-r)!)
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej6_helado():
    titulo("EJERCICIO 6 — Combinación CON repetición (heladería)")

    print("""
  ENUNCIADO:
  En una heladería hay 5 sabores distintos.
  ¿De cuántas maneras se pueden elegir 3 bolas de helado
  si se PUEDEN repetir sabores y el ORDEN NO importa?
""")

    subtitulo("PASO 1 — Las dos preguntas clave")
    print("""
  ¿El orden importa?
    NO. Un cucurucho con {Vainilla, Chocolate, Fresa} es el mismo
    sin importar en qué posición va cada bola.

  ¿Se puede repetir?
    SÍ. Puedo pedir 3 bolas de chocolate.

  Conclusión: usamos COMBINACIÓN CON REPETICIÓN.
""")

    subtitulo("PASO 2 — Por qué la fórmula es C(n+r-1, r)")
    print("""
  Esta fórmula es menos intuitiva. Se deriva de un truco
  llamado "estrellas y barras" (stars and bars).

  IDEA:
    Tenemos 5 sabores (n=5) y queremos elegir 3 bolas (r=3).
    Representamos la elección con 3 estrellas (★) y 4 barras (|)
    que separan los 5 sabores.

    Ejemplo con sabores: [Choc | Fresa | Lim | Vai | Caramelo]

    ★ ★ | | ★ | |    → 2 Choc, 0 Fresa, 1 Limón, 0 Vainilla, 0 Caramelo
    | ★ | ★ | ★ | |  → 0 Choc, 1 Fresa, 1 Limón, 1 Vainilla, 0 Caramelo

    Total de símbolos = r estrellas + (n-1) barras = 3 + 4 = 7

    Elegir la posición de las 3 estrellas entre 7 posiciones:
    C(7, 3) = C(n+r-1, r)

  Fórmula: CR(n, r) = C(n+r-1, r) = (n+r-1)! / (r! · (n-1)!)
""")

    subtitulo("PASO 3 — Calcular")
    n, r = 5, 3
    nuevo_n = n + r - 1
    resultado = math.comb(nuevo_n, r)
    num = nuevo_n * (nuevo_n-1) * (nuevo_n-2)
    den = math.factorial(r)
    print(f"""
  CR(5, 3) = C(5+3-1, 3) = C({nuevo_n}, {r})

  C({nuevo_n}, {r}) = ({nuevo_n} × {nuevo_n-1} × {nuevo_n-2}) / (3 × 2 × 1)
         = {num} / {den}
         = ?
""")
    resp = pedir(f"Escribe el resultado de {num} / {den} (solo el numero): ")
    verificar(resp, resultado)
    print(f"\n  Solucion: {num} / {den} = {resultado}")

    subtitulo("CONCLUSIÓN")
    print(f"""
  Hay {resultado} formas distintas de elegir las 3 bolas.

  Nota: si el orden importara (un cucurucho con capas definidas),
  serían variaciones con repetición: 5³ = {5**3} formas.
  Como el orden no importa → C(7,3) = {resultado}.
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej7_anagramas():
    titulo("EJERCICIO 7 — Anagramas (permutación con letras repetidas)")
    palabra = "probabilidad"

    print(f"""
  ENUNCIADO:
  ¿Cuántos anagramas (reordenaciones de letras) se pueden formar
  con la palabra '{palabra.upper()}'?
""")

    subtitulo("PASO 1 — ¿Por qué no es simplemente n!?")
    n = len(palabra)
    print(f"""
  Si todas las letras fueran distintas, habría {n}! = {math.factorial(n):,} anagramas.

  Pero hay letras REPETIDAS. Cuando una letra se repite, muchas
  reordenaciones producen la misma palabra visible.

  Ejemplo simple con "ANA" (3 letras, A se repite 2 veces):
    Si llamamos a las dos A's como A1 y A2:
    A1-N-A2  y  A2-N-A1  → ambas se ven como "ANA" (indistinguibles)

    Sin distinción habría 3! = 6, pero como la A se repite 2 veces,
    dividimos entre 2! para no contar duplicados: 6/2 = 3 anagramas reales.

  REGLA GENERAL:
    Si en n letras la letra₁ se repite n₁ veces, la letra₂ se repite n₂ veces…
                                                                            n!
    Número de anagramas =  ─────────────────────────────────
                           n₁! × n₂! × n₃! × … × nₖ!

  Dividir entre nᵢ! elimina las reordenaciones internas de las letras
  repetidas que producen palabras visualmente idénticas.
""")

    subtitulo("PASO 2 — Contar las letras de 'PROBABILIDAD'")
    conteo = Counter(palabra)
    denominador = 1
    print(f"  Palabra: '{palabra.upper()}'  →  {n} letras en total\n")
    print(f"  {'Letra':<8} {'Apariciones':<15} {'Factorial'}")
    print(f"  {'─'*35}")
    for letra, freq in sorted(conteo.items()):
        print(f"  '{letra.upper()}'      {freq:<15} {freq}! = {math.factorial(freq)}")
        denominador *= math.factorial(freq)
    print(f"\n  Denominador = producto de todos los factoriales = {denominador:,}")

    subtitulo("PASO 3 — Aplicar la fórmula")
    numerador = math.factorial(n)
    resultado = numerador // denominador
    print(f"""
  Anagramas = {n}! / {denominador:,}
            = {numerador:,} / {denominador:,}
            = ?
""")
    resp = pedir("Escribe el resultado (puede ser numero grande): ")
    verificar(resp, resultado)
    print(f"\n  Solucion: {numerador:,} / {denominador:,} = {resultado:,}")

    subtitulo("CONCLUSIÓN")
    print(f"""
  Hay {resultado:,} anagramas distintos de '{palabra.upper()}'.
  La clave: dividimos n! entre los factoriales de cada letra repetida
  para no contar como distintas las reordenaciones de letras iguales.
""")
    pausa()


# ═══════════════════════════════════════════════════════════════
#   BLOQUE 2 — LÓGICA  (Ejercicios 8, 9, 13, 14)
# ═══════════════════════════════════════════════════════════════

def teoria_logica():
    titulo("TEORÍA COMPLETA — LÓGICA PROPOSICIONAL Y PREDICADOS")
    print("""
  ┌─────────────────────────────────────────────────────────┐
  │  CONECTORES LÓGICOS Y SUS TABLAS DE VERDAD             │
  └─────────────────────────────────────────────────────────┘

  p  q │ ¬p │ p∧q │ p∨q │ p→q │ p↔q
  ─────┼────┼─────┼─────┼─────┼─────
  1  1 │  0 │  1  │  1  │  1  │  1
  1  0 │  0 │  0  │  1  │  0  │  0
  0  1 │  1 │  0  │  1  │  1  │  0
  0  0 │  1 │  0  │  0  │  1  │  1

  CÓMO LEER CADA CONECTOR:
    ¬p   (negación)     → invierte el valor de p
    p∧q  (conjunción)   → verdadero SOLO SI los dos son verdaderos
    p∨q  (disyunción)   → verdadero si AL MENOS UNO es verdadero
    p→q  (condicional)  → falso SOLO SI p=1 y q=0
                          (promesa rota solo cuando se da la condición pero no la consecuencia)
    p↔q  (bicondicional)→ verdadero cuando p y q tienen el MISMO valor

  EQUIVALENCIAS IMPORTANTES:
    p → q    ≡   ¬p ∨ q            (reescribir condicional como disyunción)
    ¬(p → q) ≡   p ∧ ¬q            (negar un condicional)
    p ↔ q    ≡   (p→q) ∧ (q→p)
    p ↔ q    ≡   (p∧q) ∨ (¬p∧¬q)

  ┌─────────────────────────────────────────────────────────┐
  │  CUANTIFICADORES                                        │
  └─────────────────────────────────────────────────────────┘

  ∀x P(x)  →  "Para TODO x, P(x) es verdadero"
  ∃x P(x)  →  "EXISTE al menos un x tal que P(x) es verdadero"

  CÓMO NEGAR CUANTIFICADORES:
    ¬(∀x P(x))  ≡  ∃x ¬P(x)    (si no es verdad para todos → hay uno que falla)
    ¬(∃x P(x))  ≡  ∀x ¬P(x)    (si no existe ninguno → todos fallan)

  NEGAR UN CONDICIONAL con cuantificadores:
    ¬(∀x: p(x) → q(x))  ≡  ∃x: p(x) ∧ ¬q(x)
    Paso 1: ¬∀  →  ∃
    Paso 2: ¬(p→q)  →  p ∧ ¬q

  CUANTIFICADORES ANIDADOS — negar de afuera hacia adentro:
    ¬[(∀x)(∃y) P(x,y)]  ≡  (∃x)(∀y) ¬P(x,y)
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej8_equivalencias():
    titulo("EJERCICIO 8 — Demostración de equivalencias lógicas")

    print("""
  ESTRATEGIA: tabla de verdad completa
  Si dos fórmulas tienen la misma columna de valores para TODAS
  las combinaciones posibles de p, q, r → son equivalentes.
""")

    subtitulo("EQUIVALENCIA 1:  (p→q) ∧ (p→r)  ≡  p→(q∧r)")

    print("""
  INTERPRETACIÓN con lenguaje natural:
    Izquierda: "Si p entonces q, Y además si p entonces r"
    Derecha:   "Si p entonces (q y r al mismo tiempo)"

  Intuitivamente deberían ser lo mismo: si p implica tanto q como r por
  separado, entonces p implica que ambos se dan juntos.
  La tabla de verdad lo confirma:
""")
    print("  p  q  r │ p→q │ p→r │ (p→q)∧(p→r) │ q∧r │ p→(q∧r) │ ¿Igual?")
    sep("-")
    todas = True
    for p in [1, 0]:
        for q in [1, 0]:
            for r in [1, 0]:
                pq  = impl(p, q)
                pr  = impl(p, r)
                lhs = conj(pq, pr)
                qr  = conj(q, r)
                rhs = impl(p, qr)
                ok  = "  SI" if lhs == rhs else "  NO ←"
                if lhs != rhs: todas = False
                print(f"  {p}  {q}  {r} │  {pq}  │  {pr}  │      {lhs}      │  {qr}  │    {rhs}     │{ok}")
    print()
    print("  Resultado:", "Columnas IGUALES → SON EQUIVALENTES ✓" if todas else "DISTINTAS → NO equivalentes")

    pausa()

    subtitulo("EQUIVALENCIA 2:  (p↔q)  ≡  (p∧q) ∨ (¬p∧¬q)")
    print("""
  INTERPRETACIÓN:
    El bicondicional p↔q es verdadero cuando p y q tienen el MISMO valor.
    ¿Cuándo tienen el mismo valor?
      • Cuando los DOS son verdaderos: (p∧q)
      • Cuando los DOS son falsos:     (¬p∧¬q)
    La unión de estos dos casos es: (p∧q) ∨ (¬p∧¬q)

  Es exactamente lo que la tabla confirma:
""")
    print("  p  q │ p↔q │ p∧q │ ¬p │ ¬q │ ¬p∧¬q │ (p∧q)∨(¬p∧¬q) │ ¿Igual?")
    sep("-")
    todas = True
    for p, q in FILAS_2:
        bc   = bicond(p, q)
        pq   = conj(p, q)
        np_  = neg(p)
        nq   = neg(q)
        npnq = conj(np_, nq)
        rhs  = disy(pq, npnq)
        ok   = "  SI" if bc == rhs else "  NO ←"
        if bc != rhs: todas = False
        print(f"  {p}  {q} │  {bc}  │  {pq}  │  {np_} │  {nq} │   {npnq}    │       {rhs}       │{ok}")
    print()
    print("  Resultado:", "Columnas IGUALES → SON EQUIVALENTES ✓" if todas else "DISTINTAS → NO equivalentes")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej9_cuantificadores():
    titulo("EJERCICIO 9 — Predicados equivalentes con cuantificadores")

    print("""
  IDEA CENTRAL:
  Los cuantificadores ∀ (para todo) y ∃ (existe) son "duales":
  negar uno produce el otro, con la proposición interna negada.

  ¿Por qué?
    Si digo "TODOS los estudiantes aprueban" y esto es FALSO,
    entonces existe AL MENOS UNO que no aprueba.
    ¬(∀x P(x))  ≡  ∃x ¬P(x)

    Si digo "EXISTE un número negativo positivo" y esto es FALSO,
    entonces TODOS los números negativos no son positivos.
    ¬(∃x P(x))  ≡  ∀x ¬P(x)
""")

    casos = [
        (
            "∃x ¬p(x)",
            "¬(∀x p(x))",
            """  Lectura: "Existe algún x para el que p(x) es FALSO"
  Es lo mismo que: "No es cierto que p(x) sea verdad PARA TODOS"
  Aplicamos: ∃x ¬p(x) ≡ ¬(∀x p(x))  [leemos al revés la regla]""",
            "Negar ∀ produce ∃ con negación. Aquí lo usamos al revés."
        ),
        (
            "¬(∃x p(x))",
            "∀x ¬p(x)",
            """  Lectura: "No existe NINGÚN x tal que p(x) sea verdadero"
  Es lo mismo que: "Para TODO x, p(x) es falso"
  Aplicamos directamente: ¬(∃x P(x)) ≡ ∀x ¬P(x)""",
            "Negar ∃ produce ∀ con negación → regla directa."
        ),
        (
            "∀x (p(x) ∧ q(x))",
            "∀x p(x)  ∧  ∀x q(x)",
            """  Lectura: "Para todo x, se cumplen p(x) Y q(x) simultáneamente"
  Se puede separar: "p vale para todo x, Y q vale para todo x"
  ∀x(p∧q) ≡ ∀x p ∧ ∀x q  [distributividad del ∀ sobre ∧]""",
            "El ∀ distribuye sobre ∧ (pero NO sobre ∨)."
        ),
        (
            "∃x (p(x) ∨ q(x))",
            "∃x p(x)  ∨  ∃x q(x)",
            """  Lectura: "Existe algún x donde se cumple p(x) O q(x)"
  Se puede separar: "(existe x con p) O (existe x con q)"
  ∃x(p∨q) ≡ ∃x p ∨ ∃x q  [distributividad del ∃ sobre ∨]""",
            "El ∃ distribuye sobre ∨ (pero NO sobre ∧)."
        ),
    ]

    for i, (pred, equiv, explicacion, regla) in enumerate(casos, 1):
        subtitulo(f"Caso {i}: Encontrar equivalente a  {pred}")
        print(explicacion)
        print(f"\n  Regla usada: {regla}")
        pedir("  Escribe el equivalente (Enter para ver): ")
        print(f"\n  Equivalente: {equiv}")
        print()
    pausa()


# ──────────────────────────────────────────────────────────────
def ej13_negaciones():
    titulo("EJERCICIO 13 — Negaciones de proposiciones con cuantificadores")

    print("""
  ENUNCIADO:
  Dadas las proposiciones:
    a.  ∃n ∈ N : n² = n
    b.  ∀x ∈ ℝ : x > 2  →  x² > 3

  Encontrar la negación de cada una.

  RECUERDA:
    ¬(∀x P(x)) = ∃x ¬P(x)        negar ∀  →  ∃ con negación
    ¬(∃x P(x)) = ∀x ¬P(x)        negar ∃  →  ∀ con negación
    ¬(p → q)   = p ∧ ¬q           negar →   saca la hipótesis y niega la tesis
""")

    subtitulo("PROPOSICIÓN a:  ∃n ∈ N : n² = n")
    print("""
  ANÁLISIS DE LA PROPOSICIÓN ORIGINAL:
    Cuantificador: ∃ (existe)
    Proposición interna: n² = n

  ¿Es verdadera la proposición original?
    Sí: n=0 → 0²=0 ✓  y  n=1 → 1²=1 ✓
    (Así que la original es verdadera, y su negación será falsa.)

  CÓMO NEGAR:
    Paso 1: negar ∃  →  cambiar a ∀
    Paso 2: negar la proposición interna: n² = n  →  n² ≠ n
""")
    pedir("  Escribe la negación (Enter para ver): ")
    print("""
  NEGACIÓN:  ∀n ∈ N : n² ≠ n
  Lectura: "Para TODO natural n, n² es DISTINTO de n"
  (Esta negación es FALSA, porque n=0 y n=1 la contradicen.)
""")

    subtitulo("PROPOSICIÓN b:  ∀x ∈ ℝ : x > 2  →  x² > 3")
    print("""
  ANÁLISIS:
    Cuantificador: ∀ (para todo)
    Proposición interna: (x > 2) → (x² > 3)
    La proposición interna es un CONDICIONAL.

  CÓMO NEGAR — dos pasos:
    Paso 1: negar ∀  →  ∃, la proposición interna queda negada:
            ∃x ∈ ℝ : ¬(x > 2 → x² > 3)

    Paso 2: negar el condicional usando  ¬(p→q) = p ∧ ¬q:
            ¬(x > 2 → x² > 3)  =  (x > 2) ∧ ¬(x² > 3)
                                =  (x > 2) ∧ (x² ≤ 3)
""")
    pedir("  Escribe la negación completa (Enter para ver): ")
    print("""
  NEGACIÓN:  ∃x ∈ ℝ : x > 2  ∧  x² ≤ 3
  Lectura: "Existe algún real x mayor que 2 cuyo cuadrado es ≤ 3"

  ¿Es verdadera esta negación?
    Necesitaríamos x > 2 y x² ≤ 3, es decir 2 < x ≤ √3 ≈ 1.73.
    Pero √3 < 2, así que no existe tal x. La negación es FALSA.
    → La proposición original es VERDADERA. ✓
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej14_cuantificadores_anidados():
    titulo("EJERCICIO 14 — Negación de cuantificadores anidados")

    print("""
  ENUNCIADO:
  Encontrar una proposición equivalente a la negación de:
    (∃x ∈ ℝ)(∀y ∈ ℝ) : x + y ≠ 0
""")

    subtitulo("PASO 1 — Entender la proposición original")
    print("""
  Lectura:
    "Existe algún número real x tal que, para CUALQUIER número
     real y, la suma x + y nunca es cero."

  ¿Es verdadera?
    Si x fuera fijo, siempre podría tomar y = -x → x + y = 0.
    Por tanto NO existe ningún x que funcione para TODOS los y.
    La proposición original es FALSA.
    → Su negación será VERDADERA.
""")

    subtitulo("PASO 2 — Negar de AFUERA hacia ADENTRO")
    print("""
  La regla para cuantificadores anidados:
    Entrar de afuera hacia adentro, negando cada cuantificador,
    hasta llegar a la proposición atómica y negarla también.

  Original:
    (∃x)(∀y) :  x + y ≠ 0

  ┌─────────────────────────────────────────────────────┐
  │ Paso 1: Ponemos ¬ adelante y negamos ∃x → ∀x       │
  │   ¬[(∃x)(∀y): x+y≠0]  =  (∀x) ¬[(∀y): x+y≠0]     │
  ├─────────────────────────────────────────────────────┤
  │ Paso 2: Continuamos hacia adentro, negamos ∀y → ∃y  │
  │   (∀x) ¬[(∀y): x+y≠0]  =  (∀x)(∃y) ¬[x+y≠0]      │
  ├─────────────────────────────────────────────────────┤
  │ Paso 3: Negamos la proposición interna              │
  │   ¬(x + y ≠ 0)  =  (x + y = 0)                    │
  └─────────────────────────────────────────────────────┘
""")

    subtitulo("PASO 3 — Resultado final")
    pedir("  Escribe la negación completa (Enter para ver): ")
    print("""
  NEGACIÓN EQUIVALENTE:
    (∀x ∈ ℝ)(∃y ∈ ℝ) : x + y = 0

  Lectura:
    "Para todo número real x, EXISTE algún número real y tal que x + y = 0"

  ¿Es verdadera esta negación?
    SÍ. Dado cualquier x, basta tomar y = -x → x + (-x) = 0. ✓
    La negación es verdadera, confirmando que la original era falsa.
""")
    pausa()


# ═══════════════════════════════════════════════════════════════
#   BLOQUE 3 — ÁLGEBRA DE BOOLE  (Ejercicios 10-12)
# ═══════════════════════════════════════════════════════════════

def teoria_boole():
    titulo("TEORÍA COMPLETA — ÁLGEBRA DE BOOLE")
    print("""
  DEFINICIÓN:
  Un Álgebra de Boole es una estructura (B, +, ·, ', 0, 1) donde:
    • B es un conjunto con al menos dos elementos
    • + (suma/unión) y · (producto/intersección) son operaciones binarias
    • ' (complemento) es una operación unaria
    • 0 y 1 son elementos distinguidos (neutros)

  CINCO AXIOMAS FUNDAMENTALES:
    B1. Conmutatividad:    a + b = b + a           a · b = b · a
    B2. Asociatividad:     a + (b+c) = (a+b) + c   a · (b·c) = (a·b) · c
    B3. Distributividad:   a · (b+c) = a·b + a·c   a + (b·c) = (a+b) · (a+c)
    B4. Neutros:           a + 0 = a               a · 1 = a
    B5. Complementos:      a + a' = 1              a · a' = 0

  PROPIEDADES DERIVADAS (se prueban usando los axiomas):
    • Idempotencia:    a + a = a       a · a = a
    • Absorción:       a + 1 = 1       a · 0 = 0
    • Doble neg.:      (a')' = a
    • De Morgan:       (a+b)' = a'·b'   (a·b)' = a'+b'

  EJEMPLO PRINCIPAL — Álgebra de Boole en ℘(A):
    B  = ℘(A) = conjunto de todos los subconjuntos de A
    +  = ∪  (unión)          →  neutro = ∅  (porque X∪∅ = X)
    ·  = ∩  (intersección)   →  neutro = A  (porque X∩A = X)
    a' = A − a               (complemento relativo a A)
    0  = ∅                   (elemento mínimo)
    1  = A                   (elemento máximo)

  CÓMO VERIFICAR EL NEUTRO:
    El neutro para ∪ es el e tal que:  X ∪ e = X  para todo X → e = ∅
    El neutro para ∩ es el e tal que:  X ∩ e = X  para todo X → e = A (total)

  CÓMO VERIFICAR EL COMPLEMENTO de X:
    X' debe satisfacer simultáneamente:
      X ∪ X' = 1 (el total)    → X ∪ X' = A
      X ∩ X' = 0 (el vacío)    → X ∩ X' = ∅
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej10_boole_partes():
    titulo("EJERCICIO 10 — Álgebra de Boole en P(A)")

    A = {4, 5, 6}
    print(f"""
  ENUNCIADO:
  Sea A = {{4, 5, 6}}  y  B = ℘(A) (conjunto de todas las partes de A).
  Consideramos el Álgebra de Boole  (B, ∪, ∩, complemento).

  Calcular:
    a. El neutro para ∪
    b. El neutro para ∩
    c. El complemento de {{5, 6}}
""")

    subtitulo("CONTEXTO — ¿Qué elementos tiene ℘(A)?")
    PA = [set(), {4}, {5}, {6}, {4,5}, {4,6}, {5,6}, {4,5,6}]
    print(f"  A = {A}  →  |A| = 3  →  |℘(A)| = 2³ = 8 elementos\n")
    print("  ℘(A) = {")
    for elem in PA:
        print(f"           {elem if elem else 'conjunto vacío (∅)'},")
    print("         }")

    subtitulo("a) NEUTRO PARA ∪")
    print("""
  Pregunta: ¿cuál es el elemento e tal que  X ∪ e = X  para todo X ∈ ℘(A)?

  Prueba:  {4,5} ∪ e = {4,5}  →  e no puede añadir elementos nuevos  →  e = ∅
           {4,6} ∪ e = {4,6}  →  e = ∅  ✓
           {}    ∪ e = {}     →  e = ∅  ✓

  Regla general:  X ∪ ∅ = X  para CUALQUIER conjunto X.
                  ∅ es el NEUTRO para ∪.
""")
    pedir("  ¿Cuál es el neutro para ∪? (Enter para ver): ")
    print("  Neutro para ∪ = ∅  (conjunto vacío)")

    subtitulo("b) NEUTRO PARA ∩")
    print(f"""
  Pregunta: ¿cuál es el elemento e tal que  X ∩ e = X  para todo X ∈ ℘(A)?

  Prueba:  {{4,5}} ∩ e = {{4,5}}  →  e debe CONTENER a {{4,5}}
           {{4,6}} ∩ e = {{4,6}}  →  e debe CONTENER a {{4,6}}
           {{5,6}} ∩ e = {{5,6}}  →  e debe CONTENER a {{5,6}}
           El único conjunto de ℘(A) que contiene a todos es A = {A}

  Regla general:  X ∩ A = X  para cualquier X ⊆ A.
                  A (el conjunto total) es el NEUTRO para ∩.
""")
    pedir("  ¿Cuál es el neutro para ∩? (Enter para ver): ")
    print(f"  Neutro para ∩ = {A}  (el conjunto A completo)")

    subtitulo("c) COMPLEMENTO DE {5, 6}")
    subconj = {5, 6}
    compl   = A - subconj
    print(f"""
  El complemento de X es el conjunto X' que satisface:
    X ∪ X' = A   (juntos cubren todo)
    X ∩ X' = ∅   (no comparten elementos)

  Para X = {subconj}:
    X' = A − X = {A} − {subconj} = {compl}

  Verificación:
    {subconj} ∪ {compl} = {subconj | compl}  = A = {A}  ✓
    {subconj} ∩ {compl} = {subconj & compl}  = ∅         ✓
""")
    pedir("  ¿Cuál es el complemento de {5,6}? (Enter para ver): ")
    print(f"  Complemento de {subconj} = {compl}")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej11_idempotencia():
    titulo("EJERCICIO 11 — Demostración de idempotencia en el Álgebra de Boole")

    print("""
  ENUNCIADO:
  Probar que en CUALQUIER álgebra de Boole se satisface:
    a.  a + a = a      (idempotencia de +)
    b.  a · a = a      (idempotencia de ·)

  IMPORTANTE: Solo podemos usar los 5 axiomas (B1-B5).
  No podemos "dar por obvio" el resultado.
""")

    subtitulo("a) DEMOSTRACIÓN de  a + a = a")
    print("""
  El truco es introducir el 1 (usando B5: a + a' = 1) y luego
  usar distributividad (B3) para simplificar.

  Paso 1:  a + a  =  (a + a) · 1
           Justificación: B4 dice a·1 = a, aplicamos a (a+a): (a+a)·1 = a+a ✓
           Pero lo escribimos al revés para poder manipularlo.

  Paso 2:  (a + a) · 1  =  (a + a) · (a + a')
           Justificación: B5 dice a + a' = 1, sustituimos 1 por (a + a').

  Paso 3:  (a + a) · (a + a')  =  a + (a · a')
           Justificación: B3 (distributividad): X·(Y+Z) = X·Y + X·Z
           aquí al revés: (X+Y)·(X+Z) = X + (Y·Z)  [otra forma de B3]
           Con X=a, Y=a, Z=a': (a+a)·(a+a') = a + (a·a')

  Paso 4:  a + (a · a')  =  a + 0
           Justificación: B5 dice a · a' = 0, sustituimos.

  Paso 5:  a + 0  =  a
           Justificación: B4 dice a + 0 = a.

  ∴  a + a = a  ✓
""")

    subtitulo("b) DEMOSTRACIÓN de  a · a = a")
    print("""
  Estrategia dual (intercambiamos + ↔ · y 0 ↔ 1):

  Paso 1:  a · a  =  (a · a) + 0
           Justificación: B4 dice a + 0 = a, aplicamos a (a·a): (a·a)+0 = a·a

  Paso 2:  (a · a) + 0  =  (a · a) + (a · a')
           Justificación: B5 dice a · a' = 0, sustituimos.

  Paso 3:  (a · a) + (a · a')  =  a · (a + a')
           Justificación: B3 distributividad: X·Y + X·Z = X·(Y+Z)
           Con X=a, Y=a, Z=a': a·a + a·a' = a·(a+a')

  Paso 4:  a · (a + a')  =  a · 1
           Justificación: B5 dice a + a' = 1, sustituimos.

  Paso 5:  a · 1  =  a
           Justificación: B4 dice a · 1 = a.

  ∴  a · a = a  ✓
""")
    print("  OBSERVACIÓN: ambas pruebas son DUALES entre sí.")
    print("  Intercambiar + ↔ · y 0 ↔ 1 convierte una en la otra.")
    print("  Esto es el Principio de Dualidad del Álgebra de Boole.")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej12_boole_producto():
    titulo("EJERCICIO 12 — Álgebra de Boole producto cartesiano ℘(A) × ℘(B)")

    A = {1, 2, 3}
    B = {4, 5, 6}
    print(f"""
  ENUNCIADO:
  Sean A = {A},  B = {B}
  𝔸 = ℘(A),  𝔹 = ℘(B)
  C = 𝔸 × 𝔹  (pares (x, y) donde x ∈ ℘(A) e y ∈ ℘(B))

  Operaciones definidas componente a componente:
    (x₁, y₁) ∪ (x₂, y₂)  =  (x₁∪x₂ , y₁∪y₂)
    (x₁, y₁) ∩ (x₂, y₂)  =  (x₁∩x₂ , y₁∩y₂)

  Calcular:
    a. El neutro para ∪ en C
    b. El neutro para ∩ en C
    c. El complemento de  ({{1,3}}, {{5}})
""")

    subtitulo("PASO PREVIO — Entender el producto cartesiano de álgebras")
    print(f"""
  Un elemento de C es un par ordenado, por ejemplo:
    ({{1,2}}, {{5,6}})  es un elemento de C = ℘(A) × ℘(B)

  La operación se hace posición a posición:
    ({{1,2}}, {{5,6}}) ∪ ({{2,3}}, {{4}})
    = ({{1,2}}∪{{2,3}} , {{5,6}}∪{{4}})
    = ({{1,2,3}} , {{4,5,6}})

  Sabemos de la teoría que:
    • En ℘(A): neutro ∪ = ∅,   neutro ∩ = A = {A}
    • En ℘(B): neutro ∪ = ∅,   neutro ∩ = B = {B}
""")

    subtitulo("a) NEUTRO PARA ∪ en C")
    print(f"""
  Buscamos (e₁, e₂) tal que (x,y) ∪ (e₁,e₂) = (x,y) para todo (x,y) ∈ C.

  Componente 1:  x ∪ e₁ = x  →  e₁ = ∅  (neutro de ∪ en ℘(A))
  Componente 2:  y ∪ e₂ = y  →  e₂ = ∅  (neutro de ∪ en ℘(B))

  Neutro para ∪ en C = (∅, ∅)

  Verificación: ({{1,3}}, {{5}}) ∪ (∅, ∅) = ({{1,3}}∪∅ , {{5}}∪∅) = ({{1,3}}, {{5}}) ✓
""")

    subtitulo("b) NEUTRO PARA ∩ en C")
    print(f"""
  Buscamos (e₁, e₂) tal que (x,y) ∩ (e₁,e₂) = (x,y) para todo (x,y) ∈ C.

  Componente 1:  x ∩ e₁ = x  →  e₁ = {A}  (neutro de ∩ en ℘(A))
  Componente 2:  y ∩ e₂ = y  →  e₂ = {B}  (neutro de ∩ en ℘(B))

  Neutro para ∩ en C = ({A}, {B})
""")

    subtitulo("c) COMPLEMENTO DE ({1,3}, {5})")
    x = {1, 3};  y = {5}
    cx = A - x;  cy = B - y
    print(f"""
  El complemento (x,y)' debe satisfacer:
    (x,y) ∪ (x,y)' = ({A}, {B})   [el neutro de ∩, que es el "1" del álgebra]
    (x,y) ∩ (x,y)' = (∅, ∅)       [el neutro de ∪, que es el "0" del álgebra]

  Se calcula componente a componente:
    Complemento de x = {x} en ℘(A):  A − x = {A} − {x} = {cx}
    Complemento de y = {y} en ℘(B):  B − y = {B} − {y} = {cy}

  Complemento de ({x}, {y}) = ({cx}, {cy})

  Verificación:
    ({x},{y}) ∪ ({cx},{cy}) = ({x|cx},{y|cy}) = ({A},{B}) ✓  (el total)
    ({x},{y}) ∩ ({cx},{cy}) = ({x&cx},{y&cy}) = (∅,∅)    ✓  (el vacío)
""")
    pausa()


# ═══════════════════════════════════════════════════════════════
#   BLOQUE 4 — FUNCIONES  (Ejercicios 15-20)
# ═══════════════════════════════════════════════════════════════

def teoria_funciones():
    titulo("TEORÍA COMPLETA — FUNCIONES")
    print("""
  Una función f: A → B asigna a cada elemento de A exactamente
  un elemento de B. A se llama dominio, B codominio.

  ┌───────────────────────────────────────────────────────────┐
  │ INYECTIVA (uno a uno / "injective"):                      │
  │   Definición: f(a₁) = f(a₂)  ⟹  a₁ = a₂               │
  │   Significado: elementos distintos tienen imágenes dists. │
  │   Imagen mental: cada flecha llega a un destino distinto  │
  │   Cond. necesaria (finitos): |A| ≤ |B|                   │
  │   Cómo probar: suponer f(a₁)=f(a₂) y deducir a₁=a₂     │
  └───────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────┐
  │ SOBREYECTIVA (sobre / "surjective"):                      │
  │   Definición: ∀b ∈ B, ∃a ∈ A : f(a) = b                │
  │   Significado: todo elemento de B tiene preimagen en A    │
  │   Imagen mental: ningún destino queda "sin visitar"       │
  │   Cond. necesaria (finitos): |A| ≥ |B|                   │
  │   Cómo probar: dado b arbitrario, encontrar a tal que f(a)=b │
  └───────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────┐
  │ BIYECTIVA (invertible / "bijective"):                     │
  │   Definición: inyectiva + sobreyectiva                    │
  │   Significado: correspondencia perfecta uno a uno         │
  │   Consecuencia: existe f⁻¹: B → A                       │
  │   Cond. necesaria (finitos): |A| = |B|                   │
  └───────────────────────────────────────────────────────────┘

  COMPOSICIÓN  h ∘ s:
    (h ∘ s)(x) = h(s(x))
    Se lee: "primero aplica s, luego aplica h al resultado"
    Dominio de h∘s = { x ∈ Dom(s)  tal que  s(x) ∈ Dom(h) }

  CARDINALIDAD Y TIPO DE FUNCIÓN f: A → B:
    |A| < |B|  →  NUNCA sobreyectiva,  PUEDE ser inyectiva
    |A| > |B|  →  NUNCA inyectiva (principio palomar), PUEDE ser sobreyectiva
    |A| = |B|  →  puede ser biyectiva

  PRINCIPIO DEL PALOMAR (pigeonhole):
    Si hay más palomas que casillas, al menos dos palomas comparten casilla.
    → Si |A| > |B|, dos elementos de A DEBEN ir al mismo b ∈ B.
    → Por tanto f NO puede ser inyectiva cuando |A| > |B|.
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej15_funcion_x2():
    titulo("EJERCICIO 15 — f(x) = x²: dominio y codominio por tipo")

    print("""
  ENUNCIADO:
  Sea f(x) = x².  Encontrar dominio A y codominio B tal que
  f: A → B sea:
    a) Inyectiva
    b) Sobreyectiva
    c) Invertible (biyectiva). Encontrar la inversa.
""")

    subtitulo("ANÁLISIS PREVIO — ¿Qué hace f(x) = x²?")
    print("""
  • f(-3) = 9  y  f(3) = 9   → dos entradas distintas, misma salida
    → NO inyectiva en ℝ (por las raíces positiva y negativa)

  • El recorrido de x² para x ∈ ℝ es [0, +∞)
    → Si B = ℝ, los negativos no tienen preimagen → NO sobreyectiva

  El dominio y codominio que elijamos determinan qué tipo es.
""")

    subtitulo("a) INYECTIVA")
    print("""
  Problema: f(-3) = f(3) = 9  →  dos x distintos con la misma imagen.

  Solución: eliminar la parte negativa del dominio.
    Si A = [0, +∞):
      Para x₁, x₂ ≥ 0: si x₁² = x₂² → x₁ = x₂  (ambos no negativos)
      → f es inyectiva en [0, +∞).

  A = [0, +∞),  B = ℝ   →   f: [0,+∞) → ℝ  es INYECTIVA

  (No es sobreyectiva porque los negativos de ℝ no tienen preimagen.)
""")

    subtitulo("b) SOBREYECTIVA")
    print("""
  Problema: x² nunca produce valores negativos.

  Solución: restringir el codominio al recorrido real de f.
    El recorrido de x² para x ∈ ℝ es [0, +∞).
    Si B = [0, +∞):
      Para cualquier b ≥ 0, tomamos a = √b ∈ ℝ → f(a) = (√b)² = b ✓

  A = ℝ,  B = [0,+∞)   →   f: ℝ → [0,+∞)  es SOBREYECTIVA

  (No es inyectiva porque f(-√b) = f(√b) = b para b > 0.)
""")

    subtitulo("c) INVERTIBLE (biyectiva) y su inversa")
    print("""
  Necesitamos inyectividad + sobreyectividad a la vez.
  Combinamos las restricciones de a) y b):

  A = [0, +∞),  B = [0, +∞)
  f: [0,+∞) → [0,+∞),  f(x) = x²

  • Inyectiva: x₁, x₂ ≥ 0 y x₁² = x₂² → x₁ = x₂  ✓
  • Sobreyectiva: dado b ≥ 0, tomamos a = √b ≥ 0 → f(a) = b  ✓

  INVERSA:
    f(x) = x²  →  f⁻¹(y) = √y  (raíz cuadrada positiva)

    Verificación:
    f(f⁻¹(y)) = f(√y) = (√y)² = y  ✓
    f⁻¹(f(x)) = f⁻¹(x²) = √(x²) = x  (para x ≥ 0)  ✓
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej16_composicion_sqrt_cubo():
    titulo("EJERCICIO 16 — Composición: h(x)=√x , s(x)=x³")

    print("""
  ENUNCIADO:
  h(x) = √x   (raíz cuadrada)
  s(x) = x³   (cubo)
  Definidas en sus dominios más amplios.
  ¿Es posible encontrar  a) h∘s   b) s∘h ?
  c) Encuentre los dominios adecuados.
""")

    subtitulo("PASO PREVIO — Dominios naturales")
    print("""
  h(x) = √x:
    Necesitamos x ≥ 0 para que la raíz sea real.
    Dom(h) = [0, +∞)

  s(x) = x³:
    El cubo está definido para cualquier real.
    Dom(s) = ℝ = (-∞, +∞)
""")

    subtitulo("a) h ∘ s  (primero s, luego h)")
    print("""
  (h∘s)(x) = h(s(x)) = h(x³) = √(x³)

  ¿Cuándo está definido?
    √(x³) requiere x³ ≥ 0
    x³ ≥ 0  ↔  x ≥ 0   (el cubo preserva el signo)

  Dom(h∘s) = [0, +∞)
  Fórmula:   (h∘s)(x) = √(x³) = x^(3/2)
""")

    subtitulo("b) s ∘ h  (primero h, luego s)")
    print("""
  (s∘h)(x) = s(h(x)) = s(√x) = (√x)³ = x^(3/2)

  ¿Cuándo está definido?
    Primero necesitamos que h(x) = √x esté definida: x ≥ 0
    Luego s puede aplicarse a cualquier valor real → no añade restricción.

  Dom(s∘h) = [0, +∞)
  Fórmula:   (s∘h)(x) = (√x)³ = x^(3/2)
""")

    subtitulo("c) Conclusión y observación importante")
    print("""
  Dom(h∘s) = [0,+∞)   (h∘s)(x) = x^(3/2)
  Dom(s∘h) = [0,+∞)   (s∘h)(x) = x^(3/2)

  En este caso h∘s = s∘h (misma fórmula y mismo dominio).
  Esto es una EXCEPCIÓN. En general, la composición NO es conmutativa.
  El siguiente ejercicio muestra el caso más habitual donde h∘s ≠ s∘h.
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej17_composicion_sqrt_lineal():
    titulo("EJERCICIO 17 — Composición: h(x)=√(x−1) , s(x)=−x+2")

    print("""
  ENUNCIADO:
  h(x) = √(x−1)
  s(x) = −x + 2
  Definidas en sus dominios más amplios.
  ¿Es posible encontrar  d) h∘s   e) s∘h ?
  f) Encuentre los dominios adecuados.
""")

    subtitulo("PASO PREVIO — Dominios naturales")
    print("""
  h(x) = √(x−1):
    Necesitamos x − 1 ≥ 0  →  x ≥ 1
    Dom(h) = [1, +∞)

  s(x) = −x + 2:
    Polinomio de grado 1 → definido para todo x.
    Dom(s) = ℝ
""")

    subtitulo("d) h ∘ s  (primero s, luego h)")
    print("""
  (h∘s)(x) = h(s(x)) = h(−x+2) = √((−x+2)−1) = √(1−x)

  ¿Cuándo está definido?
    Necesitamos que la entrada de h esté en Dom(h) = [1,+∞).
    s(x) = −x+2 debe ser ≥ 1:
      −x + 2 ≥ 1  →  −x ≥ −1  →  x ≤ 1

  Dom(h∘s) = (−∞, 1]
  Fórmula:   (h∘s)(x) = √(1−x)
""")

    subtitulo("e) s ∘ h  (primero h, luego s)")
    print("""
  (s∘h)(x) = s(h(x)) = s(√(x−1)) = −(√(x−1)) + 2 = 2 − √(x−1)

  ¿Cuándo está definido?
    Primero necesitamos x ∈ Dom(h) = [1,+∞): x ≥ 1.
    Luego s está definida para todo real → no añade restricción.

  Dom(s∘h) = [1, +∞)
  Fórmula:   (s∘h)(x) = 2 − √(x−1)
""")

    subtitulo("f) Conclusión — Aquí h∘s ≠ s∘h")
    print("""
  h∘s:  fórmula = √(1−x),     dominio = (−∞, 1]
  s∘h:  fórmula = 2−√(x−1),  dominio = [1, +∞)

  Tienen distinta fórmula y distinto dominio → h∘s ≠ s∘h.
  La composición de funciones en general NO es conmutativa.
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej18_19_cardinalidad():
    titulo("EJERCICIOS 18 y 19 — Cardinalidad y tipo de función")

    subtitulo("EJERCICIO 18:  Si |A| < |B|,  f: A → B")
    print("""
  Contexto: hay MENOS elementos en A que en B.
  Imagina A tiene 3 elementos y B tiene 5.

  Análisis de cada opción:

  a) "f ES sobreyectiva"
     FALSO. Para que f sea sobreyectiva, TODOS los b ∈ B deben tener
     preimagen. Pero con solo 3 elementos en A, como mucho podemos cubrir
     3 de los 5 elementos de B. Imposible cubrir los 5. → NUNCA sobreyectiva.

  b) "f NO PUEDE SER sobreyectiva"  ← VERDADERA ✓
     Confirmado por el argumento anterior.

  c) "f ES inyectiva"
     FALSO. Puede ser inyectiva, pero no necesariamente.
     (Podría haber dos elementos de A que apunten al mismo b ∈ B.)

  d) "f PUEDE SER inyectiva"  ← VERDADERA ✓
     Sí puede. Con |A| < |B| hay "espacio" en B para asignar
     imágenes distintas a cada elemento de A.

     Ejemplo: A={1,2,3}, B={a,b,c,d,e}
     f(1)=a, f(2)=b, f(3)=c → inyectiva (d y e no tienen preimagen).

  RESPUESTAS VERDADERAS: b) y d)
""")

    pausa()

    subtitulo("EJERCICIO 19:  Si |A| > |B|,  f: A → B")
    print("""
  Contexto: hay MÁS elementos en A que en B.
  Imagina A tiene 5 elementos y B tiene 3.

  a) "f es sobreyectiva"
     No necesariamente. PUEDE serlo, pero no DEBE serlo.

  b) "f no puede ser sobreyectiva"
     FALSO. Puede perfectamente ser sobreyectiva.
     Ejemplo: A={1,2,3,4,5}, B={a,b,c}
     f(1)=a, f(2)=a, f(3)=b, f(4)=b, f(5)=c → sobreyectiva.

  c) "f es inyectiva"
     FALSO. No puede serlo (ver opción e).

  d) "f puede ser inyectiva"
     FALSO. No puede serlo por el principio del palomar.

  e) "f NO PUEDE SER inyectiva"  ← VERDADERA ✓
     PRINCIPIO DEL PALOMAR (pigeonhole):
       Si hay más palomas (elementos de A) que casillas (elementos de B),
       al menos dos palomas deben compartir casilla.
       Con |A|=5 y |B|=3: no puedo asignar imágenes distintas a 5 elementos
       si solo tengo 3 imágenes posibles. Al menos dos coinciden.
       → f NO puede ser inyectiva cuando |A| > |B|.

  RESPUESTA VERDADERA: e)
""")
    pausa()


# ──────────────────────────────────────────────────────────────
def ej20_cantor():
    titulo("EJERCICIO 20 — Teorema de Cantor: φ: A → ℘(A)")

    print("""
  ENUNCIADO:
  Sea A un conjunto arbitrario y ℘(A) las partes de A.
  ¿Es posible definir una función sobreyectiva  φ: A → ℘(A)?
""")

    subtitulo("INTUICIÓN ANTES DE LA DEMOSTRACIÓN")
    print("""
  Para conjuntos finitos es fácil verlo:
    Si A = {1,2} → ℘(A) = {∅, {1}, {2}, {1,2}}  →  |A|=2 < |℘(A)|=4
    Por el Ej.19: |A| < |℘(A)| → φ NO puede ser sobreyectiva.

  Para conjuntos finitos: |℘(A)| = 2^|A| > |A| siempre.
  Para conjuntos infinitos... el argumento es más sutil y elegante.
""")

    subtitulo("DEMOSTRACIÓN FORMAL — Argumento diagonal de Cantor")
    print("""
  MÉTODO: contradicción (reductio ad absurdum).

  1. SUPONEMOS que φ: A → ℘(A) ES sobreyectiva.
     (Queremos llegar a una contradicción para refutar esta suposición.)

  2. Definimos el "conjunto diagonal":
       D = { x ∈ A  :  x ∉ φ(x) }
     Lectura: D contiene todos los elementos de A que NO pertenecen
     a su propia imagen por φ.

  3. D ⊆ A, por tanto D ∈ ℘(A).

  4. Como asumimos que φ es sobreyectiva, D debe tener preimagen:
     ∃ d ∈ A  tal que  φ(d) = D.

  5. Preguntamos: ¿d ∈ D?

     ┌─────────────────────────────────────────────────────────┐
     │ CASO 1: Supongamos  d ∈ D                               │
     │   Por definición de D: d ∈ D  ⟺  d ∉ φ(d)            │
     │   Pero φ(d) = D, así que: d ∉ D   ← CONTRADICCIÓN     │
     ├─────────────────────────────────────────────────────────┤
     │ CASO 2: Supongamos  d ∉ D                               │
     │   Por definición de D: d ∉ D  ⟺  d ∈ φ(d)            │
     │   Pero φ(d) = D, así que: d ∈ D   ← CONTRADICCIÓN     │
     └─────────────────────────────────────────────────────────┘

  6. En AMBOS casos llegamos a contradicción.
     → La suposición inicial era FALSA.
     → NO existe φ: A → ℘(A) sobreyectiva.

  CONSECUENCIA (Teorema de Cantor):
    |A| < |℘(A)|  para cualquier conjunto A.
    Hay infinitos de distintos "tamaños":
      ℵ₀  <  2^ℵ₀  <  2^(2^ℵ₀)  <  ...
    (ℵ₀ es el infinito de los naturales; 2^ℵ₀ el de los reales.)
""")
    pausa()


# ═══════════════════════════════════════════════════════════════
#   TEST RÁPIDO
# ═══════════════════════════════════════════════════════════════

PREGUNTAS_TEST = [
    (
        "C(8,3) = ?",
        ["24", "56", "336", "40320"],
        "56",
        "C(8,3) = 8!/(3!·5!) = (8×7×6)/(6) = 56. Orden NO importa, sin repetición."
    ),
    (
        "V(6,2) [Variación sin repetición] = ?",
        ["12", "15", "30", "720"],
        "30",
        "V(6,2) = 6×5 = 30. Orden SÍ importa, sin repetición."
    ),
    (
        "Anagramas de 'ANA' = ?",
        ["6", "3", "2", "4"],
        "3",
        "3! / 2! = 6/2 = 3. La A se repite 2 veces → dividimos entre 2!"
    ),
    (
        "Códigos de 3 dígitos (0-9) CON repetición = ?",
        ["720", "504", "1000", "100"],
        "1000",
        "10³ = 1000. Variación con repetición: n^r con n=10, r=3."
    ),
    (
        "Helados: 4 sabores, elegir 2 con repetición sin orden = ?",
        ["6", "10", "12", "16"],
        "10",
        "CR(4,2) = C(4+2-1,2) = C(5,2) = 10. Comb. con repetición."
    ),
    (
        "Si p=0 y q=1, ¿cuánto vale p→q?",
        ["0", "1"],
        "1",
        "p→q es FALSO solo cuando p=1 y q=0. Aquí p=0 → verdadero."
    ),
    (
        "Si p=1 y q=0, ¿cuánto vale p↔q?",
        ["0", "1"],
        "0",
        "p↔q es verdadero solo cuando p y q tienen el MISMO valor. Aquí no."
    ),
    (
        "¬(∃x P(x)) equivale a:",
        ["∃x ¬P(x)", "∀x ¬P(x)", "∀x P(x)", "¬∀x P(x)"],
        "∀x ¬P(x)",
        "Negar ∃ produce ∀ con la proposición negada."
    ),
    (
        "En P(A) con A={1,2,3}, el neutro para ∩ es:",
        ["vacío", "{1,2,3}", "{1}", "{2,3}"],
        "{1,2,3}",
        "X ∩ A = X para todo X ⊆ A → el neutro de ∩ es el conjunto total A."
    ),
    (
        "Si |A|=4 y |B|=7, f: A→B ¿puede ser inyectiva?",
        ["Si, porque |A| < |B|", "No, porque |A| < |B|"],
        "Si, porque |A| < |B|",
        "|A| < |B| → hay espacio en B para asignar imágenes distintas."
    ),
    (
        "Si |A|=7 y |B|=4, f: A→B ¿puede ser inyectiva?",
        ["Si", "No, por el principio del palomar"],
        "No, por el principio del palomar",
        "|A| > |B| → por palomar, dos elementos de A comparten imagen."
    ),
    (
        "¿Para qué sirve dividir entre r! en C(n,r)?",
        ["Para quitar los repetidos por orden",
         "Para incluir las repeticiones",
         "Para contar el orden interno",
         "Para añadir el grupo neutro"],
        "Para quitar los repetidos por orden",
        "Sin /r! contamos {A,B,C} y {B,A,C} como distintos. Dividir elimina esos duplicados."
    ),
]


def test_rapido():
    titulo("TEST RÁPIDO DE REPASO — 12 preguntas aleatorias")
    preguntas = list(PREGUNTAS_TEST)
    random.shuffle(preguntas)
    aciertos = 0

    for i, (pregunta, opciones, correcta, explicacion) in enumerate(preguntas, 1):
        print(f"\n  Pregunta {i}/{len(preguntas)}:")
        print(f"  {pregunta}")
        ops = opciones[:]
        random.shuffle(ops)
        for j, op in enumerate(ops, 1):
            print(f"    {j}) {op}")

        resp = pedir("Tu respuesta (número): ")
        try:
            elegida = ops[int(resp) - 1]
        except (ValueError, IndexError):
            elegida = ""

        if elegida == correcta:
            print("  CORRECTO!")
            aciertos += 1
        else:
            print(f"  Incorrecto. Respuesta: {correcta}")
        print(f"  Por que: {explicacion}")

    pct = aciertos * 100 // len(preguntas)
    print()
    sep()
    print(f"  RESULTADO: {aciertos}/{len(preguntas)}  ({pct}%)")
    if pct == 100:   print("  Dominas todos los conceptos. Listo para el examen.")
    elif pct >= 70:  print("  Bien! Repasa los que fallaste con los ejercicios del menu.")
    else:            print("  Revisa la teoria de cada bloque antes de intentarlo de nuevo.")
    sep()
    pausa()


# ═══════════════════════════════════════════════════════════════
#   MENÚS
# ═══════════════════════════════════════════════════════════════

def menu_combinatoria():
    while True:
        titulo("COMBINATORIA — Ejercicios 1 a 7")
        print("  T. Teoria completa de combinatoria")
        print("  1. Ej.1  — Libros con grupos en ORDEN FIJO")
        print("  2. Ej.2  — Libros con grupos en ORDEN LIBRE")
        print("  3. Ej.3  — Medallas (variacion sin repeticion)")
        print("  4. Ej.4  — Codigos  (variacion con repeticion)")
        print("  5. Ej.5  — Comite   (combinacion sin repeticion)")
        print("  6. Ej.6  — Heladeria (combinacion con repeticion)")
        print("  7. Ej.7  — Anagramas (permutacion con letras repetidas)")
        print("  0. Volver")
        op = input("\n  Elige: ").strip().upper()
        if op == "T":   teoria_combinatoria()
        elif op == "1": ej1_libros_orden_fijo()
        elif op == "2": ej2_libros_orden_libre()
        elif op == "3": ej3_medallas()
        elif op == "4": ej4_codigos()
        elif op == "5": ej5_comite()
        elif op == "6": ej6_helado()
        elif op == "7": ej7_anagramas()
        elif op == "0": break


def menu_logica():
    while True:
        titulo("LOGICA Y PREDICADOS — Ejercicios 8, 9, 13, 14")
        print("  T. Teoria completa de logica")
        print("  1. Ej.8  — Equivalencias logicas (tablas de verdad)")
        print("  2. Ej.9  — Predicados equivalentes con cuantificadores")
        print("  3. Ej.13 — Negaciones de proposiciones cuantificadas")
        print("  4. Ej.14 — Negacion con cuantificadores anidados")
        print("  0. Volver")
        op = input("\n  Elige: ").strip().upper()
        if op == "T":   teoria_logica()
        elif op == "1": ej8_equivalencias()
        elif op == "2": ej9_cuantificadores()
        elif op == "3": ej13_negaciones()
        elif op == "4": ej14_cuantificadores_anidados()
        elif op == "0": break


def menu_boole():
    while True:
        titulo("ALGEBRA DE BOOLE — Ejercicios 10, 11, 12")
        print("  T. Teoria completa del Algebra de Boole")
        print("  1. Ej.10 — Neutros y complemento en P(A)")
        print("  2. Ej.11 — Probar idempotencia (a+a=a, a.a=a)")
        print("  3. Ej.12 — Algebra de Boole producto cartesiano")
        print("  0. Volver")
        op = input("\n  Elige: ").strip().upper()
        if op == "T":   teoria_boole()
        elif op == "1": ej10_boole_partes()
        elif op == "2": ej11_idempotencia()
        elif op == "3": ej12_boole_producto()
        elif op == "0": break


def menu_funciones():
    while True:
        titulo("FUNCIONES — Ejercicios 15 a 20")
        print("  T. Teoria completa de funciones")
        print("  1. Ej.15 — f(x)=x2: inyectiva / sobreyectiva / invertible")
        print("  2. Ej.16 — Composicion: h(x)=raiz(x),  s(x)=x^3")
        print("  3. Ej.17 — Composicion: h(x)=raiz(x-1), s(x)=-x+2")
        print("  4. Ej.18 — Cardinalidad |A|<|B|")
        print("  5. Ej.19 — Cardinalidad |A|>|B|")
        print("  6. Ej.20 — Teorema de Cantor (phi: A -> P(A) sobreyectiva?)")
        print("  0. Volver")
        op = input("\n  Elige: ").strip().upper()
        if op == "T":          teoria_funciones()
        elif op == "1":        ej15_funcion_x2()
        elif op == "2":        ej16_composicion_sqrt_cubo()
        elif op == "3":        ej17_composicion_sqrt_lineal()
        elif op in ("4","5"):  ej18_19_cardinalidad()
        elif op == "6":        ej20_cantor()
        elif op == "0":        break


def main():
    while True:
        titulo("MATEMATICAS PARA IA — Practica 28-05-2026")
        print("  Master Universitario en Inteligencia Artificial")
        print("  Profesora: Zoraida Sivoli Barrios")
        print()
        print("  CONSEJO: Empieza por la letra T (teoria) de cada bloque.")
        print("  Luego haz los ejercicios en orden, uno por uno.")
        print()
        print("  1.  COMBINATORIA          (Ejercicios 1-7)")
        print("  2.  LOGICA Y PREDICADOS   (Ejercicios 8, 9, 13, 14)")
        print("  3.  ALGEBRA DE BOOLE      (Ejercicios 10-12)")
        print("  4.  FUNCIONES             (Ejercicios 15-20)")
        print("  5.  TEST RAPIDO DE REPASO (12 preguntas aleatorias)")
        print()
        print("  0.  Salir")
        print()

        op = input("  Elige un bloque: ").strip()
        if op == "1":   menu_combinatoria()
        elif op == "2": menu_logica()
        elif op == "3": menu_boole()
        elif op == "4": menu_funciones()
        elif op == "5": test_rapido()
        elif op == "0":
            print("\n  Mucho exito en tu practica.")
            break
        else:
            print("  Opcion no valida.")


if __name__ == "__main__":
    main()

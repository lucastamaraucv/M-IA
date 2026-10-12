"""
APRENDER LÓGICA — GUI Interactiva
Capítulo 1 del Manual (secciones 1.1 a 1.5)
Máster Universitario en Inteligencia Artificial — VIU

Ejecuta:   python aprender_logica.py

Diseñado para alguien que arranca DESDE CERO: cada lección muestra
TEORÍA + EJEMPLO al lado de la PREGUNTA, con feedback inmediato.
"""

import sys
import os
import re
import math
import time
import random
import sqlite3
import tkinter as tk
from tkinter import ttk, font as tkfont
from itertools import product

# Matplotlib (opcional) para vistas 3D rotables embebidas. Si no está
# instalado, la app sigue funcionando: solo se ocultan los botones 3D.
try:
    import numpy as _np
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registra '3d')
    _HAS_MPL = True
except Exception:
    _HAS_MPL = False

# Banco externo de ejemplos progresivos (básico → intermedio → experto).
# Generado a partir del Manual VIU; indexado por (sección, título_lección).
try:
    from extra_ejemplos import EXTRA_EJEMPLOS
except ImportError:
    EXTRA_EJEMPLOS = {}

# UTF-8 en consola Windows (cp1252 rompe con ∧ ∨ ¬ ∀ ∃)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# =====================================================================
#  CONTENIDO DIDÁCTICO — cada lección es un dict con teoría + pregunta
# =====================================================================
#
# Estructura de una lección:
#   title       : nombre corto que sale como cabecera
#   theory      : explicación PASO A PASO (lado izquierdo)
#   example     : ejemplo asociado a la teoría (se anexa abajo de teoría)
#   q_type      : "mc"  (radio, una respuesta correcta)
#                 "tf"  (Verdadero/Falso)
#                 "tt"  (tabla de verdad: el usuario rellena 4 celdas 0/1)
#                 "info"(solo teoría + botón Siguiente)
#   question    : enunciado de la pregunta
#   options     : lista de opciones (solo para "mc")
#   correct     : índice correcto (mc/tf) o lista [v00,v01,v10,v11] (tt)
#   explanation : texto que aparece al responder, ATADO a la teoría
# =====================================================================

LECCIONES = {

    # =================================================================
    "1.1  Lógica proposicional": [

        {
            "title": "¿Qué es una proposición lógica?",
            "theory":
                "Una PROPOSICIÓN LÓGICA es una frase a la que puedes "
                "decir, sin discusión: 'esto es VERDADERO (V)' o 'esto "
                "es FALSO (F)'.\n\n"
                "Sí son proposiciones:\n"
                "   • '5 es mayor que 3'   →  V\n"
                "   • '7 es un número par' →  F\n"
                "   • 'Madrid está en España' → V\n\n"
                "NO son proposiciones:\n"
                "   • '¡Hola!'             (saludo, no afirma nada)\n"
                "   • '¿Qué hora es?'      (pregunta)\n"
                "   • 'Hace buen tiempo'   (opinión, depende)\n\n"
                "💡 REGLA: si no puedes decir V/F sin dudar, NO es "
                "proposición lógica.",
            "example":
                "Asociamos V = 1   y   F = 0.\n"
                "Así podremos trabajar las proposiciones como "
                "números binarios.",
            "q_type": "mc",
            "question": "¿Cuál de estas frases es una proposición lógica?",
            "options": [
                "¡Buenos días a todos!",
                "10 es divisible por 2",
                "¿Vienes mañana al cine?",
                "Qué bonito amanecer",
            ],
            "correct": 1,
            "explanation":
                "Solo '10 es divisible por 2' es proposición: es V (10/2=5).\n"
                "Las otras son saludo, pregunta y opinión: no se les puede "
                "asignar V/F sin ambigüedad.",
        },

        {
            "title": "Tautología, contradicción y contingencia",
            "theory":
                "Una proposición se clasifica según si su valor "
                "de verdad CAMBIA o no:\n\n"
                "• TAUTOLOGÍA: SIEMPRE es Verdadera, pase lo que pase.\n"
                "      Ej.: 'todo múltiplo de 6 es múltiplo de 3'\n"
                "      Ej.: 'mañana lloverá o no lloverá'\n\n"
                "• CONTRADICCIÓN: SIEMPRE es Falsa.\n"
                "      Ej.: '10 es un número primo'\n"
                "      Ej.: 'existe un número par que no es divisible por 2'\n\n"
                "• CONTINGENCIA: a veces V y a veces F, depende del caso.\n"
                "      Ej.: 'mañana lloverá'\n"
                "      Ej.: 'hoy es martes'",
            "example":
                "Truco de memoria:\n"
                "   tautología   = TODO verdadero  (TAU = TODO)\n"
                "   contradicción= TODO falso\n"
                "   contingencia = DEPENDE",
            "q_type": "mc",
            "question": "¿Qué es 'mañana saldrá el sol o no saldrá'?",
            "options": [
                "Contradicción",
                "Contingencia",
                "Tautología",
                "No es proposición",
            ],
            "correct": 2,
            "explanation":
                "Es TAUTOLOGÍA. Diga lo que diga la realidad, una de las "
                "dos opciones ocurre: sale o no sale. Siempre V.",
        },

        {
            "title": "Conector Y (∧, AND, conjunción)",
            "theory":
                "El conector Y (símbolo ∧, o AND en inglés) une dos "
                "proposiciones.\n\n"
                "REGLA:  p ∧ q  es VERDADERO solo si AMBOS son V.\n"
                "Si UNO solo falla, todo el resultado es F.\n\n"
                "Tabla de verdad:\n"
                "      p   q   |  p ∧ q\n"
                "      F   F   |   F\n"
                "      F   V   |   F\n"
                "      V   F   |   F\n"
                "      V   V   |   V\n\n"
                "💡 Analogía: 'necesito pan Y leche'. Si me falta "
                "uno solo, NO completé el encargo.",
            "example":
                "Sea p='4 es par' (V) y q='4 es múltiplo de 3' (F).\n"
                "Entonces p ∧ q = '4 es par Y múltiplo de 3' = F.",
            "q_type": "tt",
            "question":
                "Rellena la tabla de verdad de p ∧ q.\n"
                "(Escribe 0=F o 1=V en cada celda)",
            # orden: (F,F), (F,V), (V,F), (V,V)
            "correct": [0, 0, 0, 1],
            "explanation":
                "Recuerda: ∧ solo da 1 cuando AMBOS son 1. En los otros "
                "tres casos siempre da 0.",
            "visual": {
                "tipo": "tabla",
                "headers": ["p", "q", "p ∧ q"],
                "rows": [["0", "0", "0"],
                          ["0", "1", "0"],
                          ["1", "0", "0"],
                          ["1", "1", "1"]],
                "highlight_rows": [3],
                "title": "Tabla de verdad de AND",
            },
        },

        {
            "title": "Conector O (∨, OR, disyunción)",
            "theory":
                "El conector O (símbolo ∨, o OR en inglés) también "
                "une dos proposiciones.\n\n"
                "REGLA:  p ∨ q  es FALSO solo si AMBOS son F.\n"
                "Basta con que UNO sea V para que todo sea V.\n\n"
                "Tabla de verdad:\n"
                "      p   q   |  p ∨ q\n"
                "      F   F   |   F\n"
                "      F   V   |   V\n"
                "      V   F   |   V\n"
                "      V   V   |   V\n\n"
                "💡 Analogía: 'puedes pagar con tarjeta O efectivo'. "
                "Solo te quedas sin opciones si NINGUNO funciona.\n\n"
                "OJO: en lógica, 'o' es INCLUSIVO (también incluye "
                "el caso 'los dos').",
            "example":
                "Sea p='5 es par' (F) y q='5 es múltiplo de 3' (F).\n"
                "Entonces p ∨ q = F (ninguno se cumple).\n\n"
                "Sea p='4 es par' (V) y q='4 es múltiplo de 3' (F).\n"
                "Entonces p ∨ q = V (basta con p).",
            "q_type": "tt",
            "question": "Rellena la tabla de verdad de p ∨ q.",
            "correct": [0, 1, 1, 1],
            "explanation":
                "∨ solo da 0 cuando AMBOS son 0. En el resto siempre 1.",
            "visual": {
                "tipo": "tabla",
                "headers": ["p", "q", "p ∨ q"],
                "rows": [["0", "0", "0"],
                          ["0", "1", "1"],
                          ["1", "0", "1"],
                          ["1", "1", "1"]],
                "highlight_rows": [0],
                "title": "Tabla de verdad de OR",
            },
        },

        {
            "title": "Conector NO (¬, NOT, negación)",
            "theory":
                "El NO (símbolo ¬, o NOT) actúa sobre UNA sola "
                "proposición y la INVIERTE.\n\n"
                "REGLA:\n"
                "      p   |  ¬p\n"
                "      F   |   V\n"
                "      V   |   F\n\n"
                "💡 Si p='los burros vuelan' (F), entonces\n"
                "    ¬p='los burros NO vuelan' (V).\n\n"
                "PROPIEDAD: doble negación.   ¬(¬p) = p.\n"
                "Negar dos veces te devuelve a lo original.",
            "example":
                "p = '8 es par'         (V)\n"
                "¬p = '8 NO es par'      (F)\n"
                "¬(¬p) = '8 es par'      (V)  ← volvemos a empezar.",
            "q_type": "tf",
            "question": "Si p='París está en Francia' es V, ¿cuál es ¬p?",
            "options": ["Verdadero", "Falso"],
            "correct": 1,
            "explanation":
                "¬p = 'París NO está en Francia'. Eso es FALSO.\n"
                "La negación invierte el valor de verdad.",
        },

        {
            "title": "Implicación (→, 'si... entonces')",
            "theory":
                "p → q  se lee 'si p entonces q'.\n"
                "Es el conector más DIFÍCIL de entender al principio.\n\n"
                "REGLA:  p → q es FALSO SOLO cuando p=V y q=F.\n"
                "En cualquier otro caso es V.\n\n"
                "      p   q   |  p → q\n"
                "      F   F   |   V\n"
                "      F   V   |   V\n"
                "      V   F   |   F   ← único caso falso\n"
                "      V   V   |   V\n\n"
                "💡 Analogía 'promesa':\n"
                "  p = 'apruebas el examen'\n"
                "  q = 'te regalo un coche'\n"
                "  p→q = 'si apruebas, te regalo un coche'\n"
                "Solo HE MENTIDO si apruebas (V) y NO te lo doy (F).\n"
                "Si no apruebas, te lo dé o no, no incumplí la promesa.",
            "example":
                "TEOREMA muy útil:   p → q   ≡   ¬p ∨ q\n"
                "Cualquier implicación se puede reescribir como\n"
                "'NO p, O q'. Te servirá para simplificar.",
            "q_type": "mc",
            "question":
                "¿En qué caso p → q es FALSO?",
            "options": [
                "Cuando p=F y q=F",
                "Cuando p=F y q=V",
                "Cuando p=V y q=F",
                "Cuando p=V y q=V",
            ],
            "correct": 2,
            "explanation":
                "p → q solo es F si tienes la causa (p=V) pero NO la "
                "consecuencia (q=F). Eso rompe la promesa.",
            "simple_explanation":
                "Piensa en la implicación como una PROMESA del tipo:\n"
                "  «Si llueve (p), llevo paraguas (q)».\n\n"
                "¿Cuándo te puedo llamar MENTIROSO?\n"
                "  • Llovió Y NO llevé paraguas  →  ¡MENTIRA! (V→F)\n"
                "  • Llovió Y llevé paraguas      →  cumplí (V→V)\n"
                "  • NO llovió Y llevé paraguas   →  no prometí nada\n"
                "                                   sobre eso (F→V)\n"
                "  • NO llovió Y NO llevé          →  no prometí nada\n"
                "                                   sobre eso (F→F)\n\n"
                "La ÚNICA forma de romper la promesa es:\n"
                "    pasó lo de la izquierda PERO falló lo de la derecha.",
            "similar_examples": [
                "Promesa: 'Si apruebas (p), te invito a cenar (q)'.\n"
                "  Apruebas y NO te invito → MENTIRA  (V→F)\n"
                "  Apruebas y te invito    → OK       (V→V)\n"
                "  No apruebas, te invito  → OK (regalo extra)  (F→V)\n"
                "  No apruebas, no invito  → OK (no incumplí)   (F→F)\n"
                "Solo el primer caso me hace mentir.",

                "Versión matemática:\n"
                "  p='n es múltiplo de 4',  q='n es par'.\n"
                "  Si n=8: p=V, q=V → V (no contradice nada)\n"
                "  Si n=6: p=F, q=V → V (no se prometió nada para n no múltiplo de 4)\n"
                "  Si n=3: p=F, q=F → V (lo mismo)\n"
                "  ¿n con p=V y q=F? ¡IMPOSIBLE! No existe múltiplo de 4 impar.\n"
                "Por eso 'múltiplo de 4 → par' es un teorema CIERTO.",

                "Truco de la equivalencia:\n"
                "  p → q  es lógicamente lo mismo que  ¬p ∨ q.\n"
                "Es decir: 'NO ocurre p, O bien ocurre q'.\n"
                "  Si p es falso → ¬p=V → todo es V (no importa q).\n"
                "  Si p es verdadero → necesito q=V para que sea V.\n"
                "Lo que rompe la implicación es: p=V y q=F simultáneamente.",
            ],
        },

        {
            "title": "Bicondicional (↔, 'si y solo si')",
            "theory":
                "p ↔ q se lee 'p si y solo si q', o 'p y q son "
                "equivalentes'.\n\n"
                "REGLA: p ↔ q es V cuando AMBOS tienen el MISMO valor.\n"
                "(los dos V, o los dos F).\n\n"
                "      p   q   |  p ↔ q\n"
                "      F   F   |   V\n"
                "      F   V   |   F\n"
                "      V   F   |   F\n"
                "      V   V   |   V\n\n"
                "💡 Analogía: dos interruptores 'gemelos': el "
                "bicondicional dice 'ambos están igual'.",
            "example":
                "p='ser múltiplo de 2 y de 3'\n"
                "q='ser múltiplo de 6'\n"
                "Estas dos cosas son EXACTAMENTE lo mismo,\n"
                "entonces p ↔ q es siempre V (es una tautología).",
            "q_type": "tt",
            "question": "Rellena la tabla de verdad de p ↔ q.",
            "correct": [1, 0, 0, 1],
            "explanation":
                "↔ vale 1 cuando p y q son IGUALES (ambos 0 o ambos 1) "
                "y 0 cuando son distintos.",
        },

        {
            "title": "Leyes de Morgan",
            "theory":
                "Las LEYES DE MORGAN dicen cómo se 'mete' una negación\n"
                "dentro de un paréntesis con ∧ u ∨:\n\n"
                "  ¬(p ∧ q)  ≡  ¬p ∨ ¬q       (la AND se vuelve OR)\n"
                "  ¬(p ∨ q)  ≡  ¬p ∧ ¬q       (la OR se vuelve AND)\n\n"
                "REGLA RÁPIDA: al negar el grupo, el conector\n"
                "CAMBIA (∧↔∨) y cada parte se niega.\n\n"
                "💡 ejemplo de la vida real:\n"
                "  'NO es cierto que llueva Y haga frío'\n"
                "        es lo mismo que\n"
                "  'NO llueve, O NO hace frío'",
            "example":
                "Comprobación con números:\n"
                "  p='ser par', q='ser múltiplo de 3', x=4\n"
                "  ¬(p ∧ q):  4 no es múltiplo de 6  →  V\n"
                "  ¬p ∨ ¬q:   4 no es par (F)  o  no múltiplo de 3 (V) → V\n"
                "  ¡Ambas dan lo mismo!",
            "q_type": "mc",
            "question": "¿A qué es equivalente  ¬(p ∨ q) ?",
            "options": [
                "¬p ∨ ¬q",
                "¬p ∧ ¬q",
                "p ∧ q",
                "p ∨ q",
            ],
            "correct": 1,
            "explanation":
                "Por Morgan: al negar el grupo, el ∨ se convierte en ∧ "
                "y cada parte se niega.  ¬(p ∨ q) = ¬p ∧ ¬q.",
        },
        {
            "title": "🎬 Disyunción EXCLUSIVA (⊻, XOR) (Sesión 1)",
            "nivel": "intermedio",
            "theory":
                "La disyunción EXCLUSIVA (símbolo ⊻, o XOR) es una 'o' "
                "más estricta que la ∨ que ya conoces.\n\n"
                "REGLA:  p ⊻ q  vale 1 solo si EXACTAMENTE uno de los dos "
                "es 1. Si ambos coinciden (los dos 0 o los dos 1), da 0.\n\n"
                "Diferencia con la ∨ INCLUSIVA:\n"
                "  ∨ (inclusiva): basta con que UNO sea 1, e incluso "
                "admite el caso 'los dos a la vez' (1∨1 = 1).\n"
                "  ⊻ (exclusiva): el caso 'los dos a la vez' se DESCARTA "
                "(1⊻1 = 0). Es el clásico 'o lo uno o lo otro, pero no "
                "ambos'.\n\n"
                "Tabla de verdad (orden de la GUI):\n"
                "      p   q   |  p ⊻ q\n"
                "      0   0   |   0\n"
                "      0   1   |   1\n"
                "      1   0   |   1\n"
                "      1   1   |   0\n\n"
                "💡 Analogía: el menú del día ofrece 'sopa O ensalada'. "
                "Eliges una, no las dos. Eso es un ⊻.",
            "example":
                "Sea p='Valencia pertenece a la C.Valenciana' (V) y "
                "q='Alicante pertenece a la C.Valenciana' (V).\n"
                "Como AMBAS son verdaderas, p ⊻ q = 0.\n\n"
                "Con la ∨ inclusiva habríamos obtenido 1; pero la ⊻ "
                "exige que solo una sea verdadera, y aquí lo son las dos.",
            "q_type": "tt",
            "question":
                "Rellena la tabla de verdad de p ⊻ q.\n"
                "(Escribe 0 o 1 en cada celda)",
            "options": [],
            "correct": [0, 1, 1, 0],
            "explanation":
                "⊻ da 1 solo cuando las entradas son DISTINTAS: (0,1) y "
                "(1,0). Cuando coinciden, (0,0) y (1,1), da 0. Por eso se "
                "llama 'detector de diferencia'.",
            "visual": {
                "tipo": "tabla",
                "headers": ["p", "q", "p ⊻ q"],
                "rows": [["0", "0", "0"],
                          ["0", "1", "1"],
                          ["1", "0", "1"],
                          ["1", "1", "0"]],
                "highlight_rows": [1, 2],
                "title": "Tabla de la disyunción exclusiva (XOR)",
            },
        },
        {
            "title": "🎬 Equivalencia p→q ≡ ¬p ∨ q (Sesión 2)",
            "nivel": "intermedio",
            "theory":
                "Una de las equivalencias más útiles de la lógica dice "
                "que la implicación se puede reescribir SIN la flecha:\n\n"
                "      p → q   ≡   ¬p ∨ q\n\n"
                "La forma de demostrarlo es construir la tabla de verdad "
                "de ambas expresiones y comprobar que su columna de "
                "resultados es IDÉNTICA fila a fila.\n\n"
                "Recuerda dos cosas al rellenar:\n"
                "  ¬0 = 1  y  ¬1 = 0  (la negación invierte).\n"
                "  p → q solo es 0 en el caso (1,0): premisa verdadera y "
                "conclusion falsa.\n\n"
                "Tabla completa (orden de la GUI):\n"
                "   p  q | p→q | ¬p∨q\n"
                "   0  0 |  1  |  1∨0 = 1\n"
                "   0  1 |  1  |  1∨1 = 1\n"
                "   1  0 |  0  |  0∨0 = 0\n"
                "   1  1 |  1  |  0∨1 = 1\n\n"
                "💡 Las dos últimas columnas coinciden: 1,1,0,1. Eso "
                "PRUEBA la equivalencia.",
            "example":
                "Sea p='llueve' y q='cojo el paraguas'.\n"
                "  p → q = 'si llueve, entonces cojo el paraguas'.\n"
                "  ¬p ∨ q = 'o no llueve, o cojo el paraguas'.\n"
                "Ambas frases prometen lo mismo: la única forma de "
                "romper la promesa es que llueva (p=1) y NO coja el "
                "paraguas (q=0), justo la fila (1,0) donde ambas dan 0.",
            "q_type": "mc",
            "question":
                "En la tabla, ¿qué columna coincide exactamente con la "
                "de p → q, demostrando la equivalencia?",
            "options": ["p ∧ q", "¬p ∨ q", "p ∨ q", "¬p ∧ q"],
            "correct": 1,
            "explanation":
                "p→q da la secuencia 1,1,0,1. La columna ¬p∨q da "
                "1∨0=1, 1∨1=1, 0∨0=0, 0∨1=1, es decir 1,1,0,1: idéntica. "
                "Por tanto p→q ≡ ¬p∨q queda demostrada.",
            "visual": {
                "tipo": "tabla",
                "headers": ["p", "q", "p→q", "¬p∨q"],
                "rows": [["0", "0", "1", "1"],
                          ["0", "1", "1", "1"],
                          ["1", "0", "0", "0"],
                          ["1", "1", "1", "1"]],
                "highlight_rows": [2],
                "title": "Demostración de p→q ≡ ¬p∨q",
            },
        },
    ],

    # =================================================================
    "1.2  Álgebra de Boole": [

        {
            "title": "¿Qué es un álgebra de Boole?",
            "theory":
                "Un ÁLGEBRA DE BOOLE es una 'caja matemática' con:\n"
                "  • Un conjunto de elementos (por ejemplo {0,1}).\n"
                "  • Dos operaciones: una llamada SUMA (+) y otra\n"
                "    PRODUCTO (·).\n"
                "  • Reglas que estas operaciones DEBEN cumplir.\n\n"
                "El ejemplo más simple es B = {0, 1} donde:\n"
                "       +   se comporta como OR\n"
                "       ·   se comporta como AND\n\n"
                "Lo inventó George Boole en 1847 para 'algebraicizar'\n"
                "la lógica. Hoy es la base del diseño de circuitos\n"
                "y procesadores.",
            "example":
                "Tablas:\n"
                "      +  0  1            ·  0  1\n"
                "      0  0  1            0  0  0\n"
                "      1  1  1            1  0  1\n\n"
                "Verás que + = OR  y  · = AND.",
            "q_type": "info",
            "question": "",
            "options": [],
            "correct": None,
            "explanation": "",
        },

        {
            "title": "Propiedades — Idempotencia y Absorción",
            "theory":
                "El álgebra de Boole tiene reglas curiosas que NO se\n"
                "cumplen en los números normales:\n\n"
                "• IDEMPOTENCIA:\n"
                "      x + x  = x\n"
                "      x · x  = x\n"
                "  ('hacer dos veces lo mismo no aporta nada nuevo')\n\n"
                "• ABSORCIÓN:\n"
                "      x + (x · y)  = x\n"
                "      x · (x + y)  = x\n"
                "  ('si ya tienes x, el resto sobra')\n\n"
                "• DOMINACIÓN:\n"
                "      x + 1 = 1     (el 1 domina al sumar)\n"
                "      x · 0 = 0     (el 0 domina al multiplicar)",
            "example":
                "Verifica con x=1, y=0:\n"
                "  x + x  = 1+1 = 1 = x   ✓\n"
                "  x · x  = 1·1 = 1 = x   ✓\n"
                "  x + (x·y) = 1 + 0 = 1 = x  ✓",
            "q_type": "mc",
            "question": "¿Cuánto vale  x + 1  en un álgebra de Boole?",
            "options": ["x", "1", "0", "x · 1"],
            "correct": 1,
            "explanation":
                "Propiedad de DOMINACIÓN: el 1 al sumar siempre 'gana'.\n"
                "Da igual lo que valga x.",
        },

        {
            "title": "Elemento complementario",
            "theory":
                "Cada elemento x tiene un COMPLEMENTARIO, escrito x' o x̄,\n"
                "que cumple:\n"
                "      x + x' = 1     (juntos cubren todo)\n"
                "      x · x' = 0     (no comparten nada)\n\n"
                "En B = {0,1}:\n"
                "      0' = 1\n"
                "      1' = 0\n\n"
                "💡 El complementario en lógica es la NEGACIÓN.",
            "example":
                "Idea visual: piensa en encendido (1) y apagado (0).\n"
                "Su complementario es el estado contrario.",
            "q_type": "tf",
            "question": "¿Es cierto que  1 · 1' = 0  ?",
            "options": ["Verdadero", "Falso"],
            "correct": 0,
            "explanation":
                "1' = 0, entonces 1 · 0 = 0.  ✓\n"
                "Esto refleja la regla x · x' = 0.",
        },
    ],

    # =================================================================
    "1.3  Funciones booleanas y puertas": [

        # ============== BÁSICO ============================================

        {
            "title": "¿Qué es una función booleana?",
            "nivel": "básico",
            "theory":
                "Una FUNCIÓN BOOLEANA es una 'máquina' que recibe ceros\n"
                "y unos como entrada y devuelve un cero o un uno.\n\n"
                "Formalmente:   f : {0,1}^n  →  {0,1}\n\n"
                "Cada PUERTA LÓGICA es una función booleana concreta:\n"
                "AND, OR, NOT, XOR, NAND, NOR, XNOR.",
            "example":
                "En electrónica, 1 = pasa corriente, 0 = no pasa.\n"
                "Las puertas combinan corrientes para hacer cálculos.\n"
                "Abajo verás cómo se REPRESENTAN gráficamente.",
            "diagram": {
                "vars": ["x", "y"],
                "gates": [
                    {"id": "A", "type": "AND",  "pos": (110, 20),
                     "inputs": ["x", "y"], "etiqueta": "AND"},
                    {"id": "B", "type": "OR",   "pos": (110, 80),
                     "inputs": ["x", "y"], "etiqueta": "OR"},
                    {"id": "C", "type": "XOR",  "pos": (260, 50),
                     "inputs": ["A", "B"], "etiqueta": "XOR"},
                ],
                "outputs": [{"from": "C", "label": "f"}],
            },
            "q_type": "info",
            "question": "",
            "options": [], "correct": None, "explanation": "",
        },

        {
            "title": "Puerta AND  —  símbolo y comportamiento",
            "nivel": "básico",
            "theory":
                "La puerta AND da 1 SOLO si AMBAS entradas son 1.\n\n"
                "      x   y   | AND\n"
                "      0   0   |  0\n"
                "      0   1   |  0\n"
                "      1   0   |  0\n"
                "      1   1   |  1\n\n"
                "💡 Equivale al conector lógico ∧ (Y).\n"
                "💡 Circuito: dos interruptores en SERIE.\n"
                "💡 Símbolo IEEE: cuerpo en forma de 'D'.",
            "example":
                "En Python:  AND = lambda x, y: x & y\n"
                "  AND(1,1) = 1    AND(1,0) = 0\n\n"
                "Abajo ves su forma gráfica estándar:",
            "diagram": {
                "vars": ["x", "y"],
                "gates": [{"id": "G", "type": "AND", "pos": (170, 50),
                           "inputs": ["x", "y"]}],
                "outputs": [{"from": "G", "label": "x·y"}],
            },
            "q_type": "tt",
            "question": "Rellena la tabla de verdad de AND.",
            "correct": [0, 0, 0, 1],
            "explanation":
                "AND solo da 1 cuando AMBOS son 1. Es el más 'exigente'.",
        },

        {
            "title": "Puerta OR  —  símbolo y comportamiento",
            "nivel": "básico",
            "theory":
                "La puerta OR da 1 si AL MENOS UNA entrada es 1.\n\n"
                "      x   y   | OR\n"
                "      0   0   |  0\n"
                "      0   1   |  1\n"
                "      1   0   |  1\n"
                "      1   1   |  1\n\n"
                "💡 Equivale al conector lógico ∨ (O).\n"
                "💡 Circuito: dos interruptores en PARALELO.\n"
                "💡 Símbolo IEEE: forma de escudo con tip pointed.",
            "example":
                "En Python:  OR = lambda x, y: x | y\n"
                "  OR(0,0) = 0    OR(1,0) = 1\n\n"
                "Su símbolo gráfico:",
            "diagram": {
                "vars": ["x", "y"],
                "gates": [{"id": "G", "type": "OR", "pos": (170, 50),
                           "inputs": ["x", "y"]}],
                "outputs": [{"from": "G", "label": "x+y"}],
            },
            "q_type": "tt",
            "question": "Rellena la tabla de verdad de OR.",
            "correct": [0, 1, 1, 1],
            "explanation": "OR solo da 0 cuando AMBOS son 0.",
        },

        {
            "title": "Puerta NOT  —  símbolo y comportamiento",
            "nivel": "básico",
            "theory":
                "La puerta NOT invierte la entrada. Solo tiene 1 entrada.\n\n"
                "      x   | NOT\n"
                "      0   |  1\n"
                "      1   |  0\n\n"
                "💡 Equivale a la NEGACIÓN ¬.\n"
                "💡 Símbolo IEEE: triángulo + círculo pequeño (bubble).\n"
                "Ese círculo de la salida significa 'INVERTIR'.",
            "example":
                "En Python:  NOT = lambda x: 1 - x\n"
                "  NOT(0) = 1     NOT(1) = 0\n"
                "  NOT(NOT(1)) = 1\n\n"
                "Su símbolo gráfico:",
            "diagram": {
                "vars": ["x"],
                "gates": [{"id": "G", "type": "NOT", "pos": (180, 50),
                           "inputs": ["x"]}],
                "outputs": [{"from": "G", "label": "x'"}],
            },
            "q_type": "mc",
            "question": "¿Cuánto vale NOT(NOT(0)) ?",
            "options": ["0", "1", "Depende", "Indefinido"],
            "correct": 0,
            "explanation":
                "NOT(0) = 1.  Luego NOT(1) = 0. Volvemos al original.\n"
                "Esta es la propiedad de DOBLE NEGACIÓN.",
        },

        {
            "title": "Puerta XOR  —  O exclusivo",
            "nivel": "básico",
            "theory":
                "XOR ('exclusive OR') da 1 cuando las entradas son\n"
                "DIFERENTES, y 0 cuando son iguales.\n\n"
                "      x   y   | XOR\n"
                "      0   0   |  0\n"
                "      0   1   |  1\n"
                "      1   0   |  1\n"
                "      1   1   |  0\n\n"
                "💡 'Una cosa O la otra, pero NO ambas'.\n"
                "💡 Muy usada en criptografía y suma binaria.\n"
                "💡 Símbolo: igual que OR pero con un ARCO extra detrás.",
            "example":
                "Truco: XOR(x,y) = 1  ⇔  x ≠ y\n"
                "Sirve para detectar diferencias entre dos bits.",
            "diagram": {
                "vars": ["x", "y"],
                "gates": [{"id": "G", "type": "XOR", "pos": (170, 50),
                           "inputs": ["x", "y"]}],
                "outputs": [{"from": "G", "label": "x⊕y"}],
            },
            "q_type": "tt",
            "question": "Rellena la tabla de verdad de XOR.",
            "correct": [0, 1, 1, 0],
            "explanation":
                "XOR = 1 solo cuando los bits son DISTINTOS (0,1) o (1,0).",
            "visual": {
                "tipo": "tabla",
                "headers": ["x", "y", "x ⊕ y"],
                "rows": [["0", "0", "0"],
                          ["0", "1", "1"],
                          ["1", "0", "1"],
                          ["1", "1", "0"]],
                "highlight_rows": [1, 2],
                "title": "Tabla XOR (1 cuando entradas distintas)",
            },
        },

        {
            "title": "Puertas NAND y NOR  —  las 'invertidas'",
            "nivel": "básico",
            "theory":
                "NAND = NOT(AND).  NOR = NOT(OR).\n\n"
                "Símbolo: el de AND/OR + un círculo pequeño (bubble)\n"
                "en la salida. Ese círculo significa 'invertir'.\n\n"
                "NAND:                        NOR:\n"
                "  x y | NAND                  x y | NOR\n"
                "  0 0 |  1                    0 0 |  1\n"
                "  0 1 |  1                    0 1 |  0\n"
                "  1 0 |  1                    1 0 |  0\n"
                "  1 1 |  0                    1 1 |  0\n\n"
                "💡 NAND y NOR son 'universales': con SOLO NAND (o\n"
                "solo NOR) puedes construir TODAS las demás puertas.\n"
                "Por eso los chips reales se hacen mayormente con NAND.",
            "example":
                "Construir NOT usando solo NAND:\n"
                "      NOT(x) = NAND(x, x)\n\n"
                "Mira los dos símbolos abajo: fíjate en la BUBBLE\n"
                "(círculo blanco) que sale de cada uno.",
            "diagram": {
                "vars": ["x", "y"],
                "gates": [
                    {"id": "G1", "type": "NAND", "pos": (110, 20),
                     "inputs": ["x", "y"]},
                    {"id": "G2", "type": "NOR",  "pos": (110, 100),
                     "inputs": ["x", "y"]},
                ],
                "outputs": [
                    {"from": "G1", "label": "NAND"},
                    {"from": "G2", "label": "NOR"},
                ],
            },
            "q_type": "tt",
            "question": "Rellena la tabla de verdad de NAND.",
            "correct": [1, 1, 1, 0],
            "explanation":
                "NAND es 'casi todo 1', solo da 0 cuando AMBOS son 1.\n"
                "Es exactamente lo contrario de AND.",
        },

        # ============== INTERMEDIO ========================================
        # Bloque ampliado siguiendo el Capítulo 1, §1.3.3 del Manual VIU.
        # Cada lección de nivel intermedio incluye:
        #   • theory: derivación paso a paso (Ejemplos 1, 2 y 3 del manual)
        #   • example: cálculo concreto y observación didáctica
        #   • diagram + trace_values: el circuito puede ANIMARSE
        #     (botón «▶ Animar» en la GUI) propagando 0/1 visualmente.

        {
            "title": "Trazar un circuito paso a paso (Ejemplo 1 del manual)",
            "nivel": "intermedio",
            "theory":
                "El manual (§1.3.3, Ejemplo 1) recomienda una RECETA en 4 pasos\n"
                "para obtener la función booleana asociada a un circuito:\n\n"
                "  1) ETIQUETA cada puerta con una letra (A, B, C, …).\n"
                "  2) Escribe la SALIDA de cada puerta en función de sus\n"
                "     entradas, usando '+' para OR, '·' para AND y la barra\n"
                "     para NOT (z̄ = NOT(z)).\n"
                "  3) Sustituye las letras intermedias hasta dejar la\n"
                "     SALIDA FINAL en términos solo de las variables\n"
                "     originales (x, y, z, …).\n"
                "  4) Para EVALUAR en un caso concreto, propaga las señales\n"
                "     de IZQUIERDA a DERECHA respetando dependencias.\n\n"
                "💡 Truco: una buena heurística es marcar con color las\n"
                "     señales 1 (verde) y 0 (rojo). Lo verás con el botón\n"
                "     «▶ Animar» bajo el ejemplo.",
            "example":
                "CIRCUITO (Figura 11 del manual)\n"
                "─────────────────────────────────\n"
                "  Entradas: x, y, z\n"
                "  A = x · y          (puerta AND)\n"
                "  B = z̄             (puerta NOT)\n"
                "  C = A + B          (puerta OR)  ← salida\n\n"
                "DERIVACIÓN ALGEBRAICA\n"
                "  C = A + B\n"
                "    = (x · y) + z̄\n"
                "  →  f(x, y, z) = x · y + z̄     (función del manual)\n\n"
                "EVALUACIÓN para (x, y, z) = (1, 1, 0)\n"
                "  A = 1 · 1 = 1\n"
                "  B = NOT(0) = 1\n"
                "  C = 1 + 1 = 1     ⇒  f(1, 1, 0) = 1\n\n"
                "Pulsa «▶ Animar» para ver la señal verde recorriendo\n"
                "el circuito en este mismo orden.",
            "diagram": {
                "vars": ["x", "y", "z"],
                "gates": [
                    {"id": "A", "type": "AND", "pos": (140, 18),
                     "inputs": ["x", "y"]},
                    {"id": "B", "type": "NOT", "pos": (140, 118),
                     "inputs": ["z"]},
                    {"id": "C", "type": "OR",  "pos": (310, 60),
                     "inputs": ["A", "B"]},
                ],
                "outputs": [{"from": "C", "label": "f = x·y + z̄"}],
                "trace_values": {"x": 1, "y": 1, "z": 0},
            },
            "q_type": "mc",
            "question":
                "Con el mismo circuito  f(x,y,z) = x·y + z̄, ¿cuánto vale\n"
                "f(0, 1, 1)?",
            "options": ["0", "1", "Indefinido", "Depende"],
            "correct": 0,
            "explanation":
                "Paso a paso, propagando las señales:\n"
                "  A = 0 · 1 = 0\n"
                "  B = NOT(1) = 0\n"
                "  C = A + B = 0 + 0 = 0   ⇒  f = 0\n\n"
                "Lectura algebraica: f = 0·1 + 1̄ = 0 + 0 = 0.",
        },

        {
            "title": "Circuito con NOR + NOT + XOR (Ejemplo 2 del manual)",
            "nivel": "intermedio",
            "theory":
                "Este es el segundo ejemplo resuelto del manual (Figura 12).\n"
                "Mezcla TRES tipos de puerta y nos obliga a usar las LEYES\n"
                "DE MORGAN durante la simplificación:\n\n"
                "  • A = NOR(x, y) = x + y  =  x̄ · ȳ     ← Morgan\n"
                "  • B = NOT(z)    = z̄\n"
                "  • C = XOR(A, B)\n\n"
                "Recuerda la definición algebraica de XOR del manual:\n"
                "      XOR(A, B)  =  A · B̄  +  Ā · B\n\n"
                "Sustituyendo A y B, y usando que B̄ = z, queda\n"
                "una expresión cerrada en (x, y, z):\n\n"
                "      f(x, y, z) = x̄·ȳ·z  +  (x + y)·z̄\n\n"
                "💡 Observa cómo cada NOR / NOT 'aplasta' la salida\n"
                "    a 0 cuando alguna entrada está activa. El XOR\n"
                "    final actúa como un detector de DIFERENCIAS\n"
                "    entre A y B.",
            "example":
                "EVALUACIÓN para (x, y, z) = (1, 0, 0)\n"
                "─────────────────────────────────────\n"
                "  A = NOR(1, 0) = 0     (basta un 1 para que NOR=0)\n"
                "  B = NOT(0)    = 1\n"
                "  C = XOR(0, 1) = 1     (entradas distintas → 1)\n"
                "  f(1, 0, 0) = 1\n\n"
                "  Comprobación por la fórmula:\n"
                "     f = x̄·ȳ·z + (x+y)·z̄\n"
                "       = 0·1·0  + (1+0)·1\n"
                "       = 0 + 1 = 1   ✓ coincide\n\n"
                "EVALUACIÓN para (x, y, z) = (0, 0, 1)\n"
                "  A = NOR(0, 0) = 1\n"
                "  B = NOT(1)    = 0\n"
                "  C = XOR(1, 0) = 1     ⇒  f(0, 0, 1) = 1\n\n"
                "💡 Cuando dudes entre propagación y fórmula, propaga\n"
                "    en la FIGURA paso a paso: te ahorra errores algebraicos.",
            "diagram": {
                "vars": ["x", "y", "z"],
                "gates": [
                    {"id": "A", "type": "NOR", "pos": (140, 18),
                     "inputs": ["x", "y"]},
                    {"id": "B", "type": "NOT", "pos": (140, 118),
                     "inputs": ["z"]},
                    {"id": "C", "type": "XOR", "pos": (310, 60),
                     "inputs": ["A", "B"]},
                ],
                "outputs": [{"from": "C", "label": "f"}],
                "trace_values": {"x": 1, "y": 0, "z": 0},
            },
            "q_type": "mc",
            "question":
                "Mismo circuito (NOR-NOT-XOR). ¿Cuánto vale f(0, 0, 0)?",
            "options": ["0", "1", "No se puede saber", "Depende"],
            "correct": 0,
            "explanation":
                "Propagación paso a paso para (0, 0, 0):\n"
                "  A = NOR(0, 0) = 1    (única manera de que NOR=1)\n"
                "  B = NOT(0)    = 1\n"
                "  C = XOR(1, 1) = 0    (entradas iguales → 0)\n"
                "  ⇒  f(0, 0, 0) = 0\n\n"
                "El XOR final es el que 'apaga' la salida: A y B\n"
                "llegan ambos a 1 y XOR(1,1)=0.",
        },

        {
            "title": "Identificar una puerta por su tabla",
            "nivel": "intermedio",
            "theory":
                "Una habilidad clave: ver una tabla de verdad y\n"
                "RECONOCER en menos de 2 segundos qué puerta es.\n"
                "Usa esta tabla mental (orden 00 → 01 → 10 → 11):\n\n"
                "  ┌──────┬───────────────┬──────────────────────────┐\n"
                "  │PATRÓN│ PUERTA        │ LECTURA RÁPIDA           │\n"
                "  ├──────┼───────────────┼──────────────────────────┤\n"
                "  │0001  │ AND  (·)      │ 1 SOLO al final          │\n"
                "  │0111  │ OR   (+)      │ 0 SOLO al inicio         │\n"
                "  │0110  │ XOR  (⊕)      │ simétrico, '0' en bordes │\n"
                "  │1110  │ NAND          │ 0 SOLO al final          │\n"
                "  │1000  │ NOR           │ 1 SOLO al inicio         │\n"
                "  │1001  │ XNOR  (⊙)     │ espejo de XOR            │\n"
                "  └──────┴───────────────┴──────────────────────────┘\n\n"
                "💡 Truco: cuenta los UNOS. Si hay 1 solo → AND/NOR;\n"
                "    si hay 3 → OR/NAND; si hay 2 simétricos → XOR/XNOR.\n"
                "    El que la fila (0,0) sea 0 o 1 distingue OR de NOR,\n"
                "    AND de NAND, etc.",
            "example":
                "Tabla recibida:  [1, 0, 0, 1]   (orden 00, 01, 10, 11)\n"
                "  • 2 unos, en posiciones SIMÉTRICAS (00 y 11)\n"
                "  • Da 1 cuando ambas entradas son IGUALES\n"
                "  →  XNOR ✓  (también llamada 'equivalencia bit a bit')\n\n"
                "Aplicación real: el XNOR es el operador 'son iguales'\n"
                "que usan los comparadores hardware bit a bit.",
            "q_type": "mc",
            "question":
                "Una puerta produce esta tabla:\n"
                "  (0,0)→1, (0,1)→0, (1,0)→0, (1,1)→0\n"
                "¿Qué puerta es?",
            "options": ["AND", "NAND", "NOR", "XOR"],
            "correct": 2,
            "explanation":
                "Patrón [1, 0, 0, 0]: 1 SOLO cuando ambas entradas son 0.\n"
                "Es NOR = NOT(OR). Es la única que requiere AUSENCIA\n"
                "total de señal para activarse.",
            "simple_explanation":
                "TRUCO MNEMOTÉCNICO en 2 pasos:\n\n"
                "  PASO 1 — Cuenta los UNOS en la columna de salida:\n"
                "    1 uno  → AND o NOR\n"
                "    2 unos → XOR o XNOR (simétricos)\n"
                "    3 unos → OR o NAND\n\n"
                "  PASO 2 — Mira dónde está el uno SOLITARIO:\n"
                "    AND: el uno está en la FILA 11 (ambos 1).\n"
                "    NOR: el uno está en la FILA 00 (ambos 0).\n"
                "    OR:  el cero está en la FILA 00.\n"
                "    NAND: el cero está en la FILA 11.\n"
                "    XOR:  unos en 01 y 10 (entradas distintas).\n"
                "    XNOR: unos en 00 y 11 (entradas iguales).",
            "similar_examples": [
                "Tabla [0, 0, 0, 1]:\n"
                "  Un solo 1, en posición 11. → AND.\n"
                "  Da 1 solo cuando ambas son 1 (estricto).",

                "Tabla [1, 0, 0, 1]:\n"
                "  Dos unos, en posiciones SIMÉTRICAS (00 y 11). → XNOR.\n"
                "  Da 1 cuando las entradas SON IGUALES.",

                "Tabla [1, 1, 1, 0]:\n"
                "  Tres unos. El cero está en posición 11. → NAND.\n"
                "  Es el NEGATIVO de AND: 'no ambos son 1'.",

                "Tabla [0, 1, 1, 0]:\n"
                "  Dos unos, en posiciones DIFERENTES (01 y 10). → XOR.\n"
                "  Da 1 cuando las entradas SON DISTINTAS.",
            ],
        },

        {
            "title": "NAND universal · construir NOT, AND y OR con NAND",
            "nivel": "intermedio",
            "theory":
                "NAND es UNIVERSAL: con solo puertas NAND puedes construir\n"
                "TODAS las demás. Esto es lo que hace que la mayor parte\n"
                "del silicio en un procesador esté hecho con NAND.\n\n"
                "Las tres construcciones básicas (memorízalas):\n\n"
                "  ① NOT(x)    = NAND(x, x)\n"
                "       (idempotencia: x · x = x, luego NAND = NOT(x))\n\n"
                "  ② AND(x, y) = NAND( NAND(x, y), NAND(x, y) )\n"
                "       (aplicas NAND y luego inviertes con NOT-vía-NAND)\n\n"
                "  ③ OR(x, y)  = NAND( NAND(x, x), NAND(y, y) )\n"
                "       (niegas cada entrada y aplicas NAND;\n"
                "       por Morgan:  x̄ · ȳ  → invertido → x + y)\n\n"
                "💡 NOR también es universal (con construcciones duales).",
            "example":
                "DEMOSTRACIÓN de ②, paso a paso para (x, y) = (1, 1):\n"
                "  T = NAND(1, 1) = 0    (negación de AND)\n"
                "  AND(1, 1) = NAND(T, T) = NAND(0, 0) = 1   ✓\n\n"
                "DEMOSTRACIÓN de ③ para (x, y) = (0, 1):\n"
                "  U = NAND(0, 0) = 1\n"
                "  V = NAND(1, 1) = 0\n"
                "  OR(0, 1) = NAND(U, V) = NAND(1, 0) = 1     ✓\n\n"
                "El diagrama de abajo ilustra ② (AND con 2 NANDs).",
            "diagram": {
                "vars": ["x", "y"],
                "gates": [
                    {"id": "T", "type": "NAND", "pos": (140, 60),
                     "inputs": ["x", "y"]},
                    {"id": "U", "type": "NAND", "pos": (310, 60),
                     "inputs": ["T", "T"]},
                ],
                "outputs": [{"from": "U", "label": "AND(x, y)"}],
                "trace_values": {"x": 1, "y": 1},
            },
            "q_type": "mc",
            "question":
                "¿Cuántas puertas NAND como mínimo necesitas para\n"
                "construir un OR con solo NAND?",
            "options": ["1", "2", "3", "4"],
            "correct": 2,
            "explanation":
                "Tres NANDs:\n"
                "  · NAND(x, x)   = x̄\n"
                "  · NAND(y, y)   = ȳ\n"
                "  · NAND(x̄, ȳ) = ¬(x̄ · ȳ) = x + y   (Morgan)\n"
                "Total: 3 puertas NAND.",
        },

        {
            "title": "Aplicar Morgan en circuitos · ahorrar puertas",
            "nivel": "intermedio",
            "theory":
                "Las LEYES DE MORGAN trasladadas a circuitos:\n\n"
                "  NOT(A · B)  =  NOT(A) + NOT(B)        [NAND → OR de\n"
                "                                          negaciones]\n"
                "  NOT(A + B)  =  NOT(A) · NOT(B)        [NOR  → AND de\n"
                "                                          negaciones]\n\n"
                "Usos prácticos en hardware:\n"
                "  • REDUCIR el número de puertas → menos silicio,\n"
                "    menos retardo, menos consumo.\n"
                "  • CONVERTIR un diseño 'AND + NOT' al lenguaje\n"
                "    NAND-only que prefieren las fábricas.\n"
                "  • SIMPLIFICAR fórmulas booleanas que luego\n"
                "    sintetizamos en una sola puerta.\n\n"
                "💡 Regla de oro: cuando veas dos NOTs delante de un\n"
                "    AND/OR, dales la vuelta. Sale gratis."
                ,
            "example":
                "TRANSFORMACIÓN clásica:\n"
                "  Inicial:   f = x̄ · ȳ           (NOT + NOT + AND)  3 puertas\n"
                "  Morgan:    f = NOT(x + y)       (NOR)              1 puerta\n"
                "  Ahorro:    2 puertas (≈ 60-70 % menos transistores)\n\n"
                "Verifiquemos con (x, y) = (1, 0):\n"
                "  Inicial:   1̄ · 0̄ = 0 · 1 = 0\n"
                "  Morgan:    NOT(1 + 0) = NOT(1) = 0    ✓ idéntico\n\n"
                "Mira el diagrama abajo: el circuito ya está SIMPLIFICADO\n"
                "a una sola puerta NOR.",
            "diagram": {
                "vars": ["x", "y"],
                "gates": [{"id": "G", "type": "NOR", "pos": (180, 50),
                           "inputs": ["x", "y"]}],
                "outputs": [{"from": "G", "label": "≡ x̄ · ȳ"}],
                "trace_values": {"x": 1, "y": 0},
            },
            "q_type": "mc",
            "question":
                "¿A qué circuito equivale  x̄ + ȳ  (NOT-NOT-OR)?",
            "options": [
                "AND(x, y)",
                "OR(x, y)",
                "NAND(x, y)",
                "NOR(x, y)",
            ],
            "correct": 2,
            "explanation":
                "Por Morgan:  x̄ + ȳ  =  NOT(x · y)  =  NAND(x, y).\n"
                "Truco mnemónico: al meter el NOT por fuera, ∧ ↔ ∨ y\n"
                "se invierten las entradas. Aquí ahorramos 2 NOT.",
        },

        {
            "title": "Suma y producto de funciones booleanas",
            "nivel": "intermedio",
            "theory":
                "El manual (§1.3.1, Teorema) muestra que el conjunto Fₙ\n"
                "de funciones booleanas con n variables forma a su vez\n"
                "un ÁLGEBRA DE BOOLE con las operaciones puntuales:\n\n"
                "  (f + g)(x₁, …, xₙ) = f(x₁, …, xₙ) + g(x₁, …, xₙ)\n"
                "  (f · g)(x₁, …, xₙ) = f(x₁, …, xₙ) · g(x₁, …, xₙ)\n"
                "  f̄  (x₁, …, xₙ) = NOT( f(x₁, …, xₙ) )\n\n"
                "Es decir: sumar dos circuitos punto a punto es OR; \n"
                "multiplicar es AND; complementar es invertir cada\n"
                "valor. Esto justifica formalmente que podamos\n"
                "manipular CIRCUITOS con álgebra (Morgan, distributiva,\n"
                "absorción, idempotencia…).\n\n"
                "💡 Es el mismo paso conceptual que se da en cálculo\n"
                "    cuando se define (f + g)(x) = f(x) + g(x): permite\n"
                "    tratar funciones como si fueran números.",
            "example":
                "Sean  f(x, y) = x · y     y    g(x, y) = x + y.\n"
                "Calculamos (f + g) y (f · g) puntualmente:\n\n"
                "  (x, y)  f  g | f+g   f·g\n"
                "   0 0    0  0 |  0     0\n"
                "   0 1    0  1 |  1     0\n"
                "   1 0    0  1 |  1     0\n"
                "   1 1    1  1 |  1     1\n\n"
                "Observa:\n"
                "  • f + g = g    (porque f está 'dentro' de g — absorción)\n"
                "  • f · g = f    (lo mismo, simétrico)\n"
                "Es exactamente la LEY DE ABSORCIÓN del álgebra de Boole.",
            "q_type": "mc",
            "question":
                "Sean f(x, y) = x  y  g(x, y) = ȳ.  ¿Qué función es f · g?",
            "options": [
                "x · ȳ",
                "x + ȳ",
                "x̄ · y",
                "x ⊕ y",
            ],
            "correct": 0,
            "explanation":
                "Por la definición puntual:\n"
                "  (f · g)(x, y) = f(x, y) · g(x, y) = x · ȳ.\n\n"
                "Tabla rápida (00,01,10,11):  0, 0, 1, 0.\n"
                "Es 1 SOLO cuando x=1 y y=0 (inhibición de y sobre x).",
        },

        {
            "title": "Equivalencia de circuitos · 4 puertas → 1",
            "nivel": "intermedio",
            "theory":
                "Dos circuitos son EQUIVALENTES si dan la misma salida\n"
                "para cada combinación de entradas. Comprobarlo:\n\n"
                "  1) Escribe la fórmula booleana de cada circuito.\n"
                "  2) Aplica leyes del álgebra (Morgan, absorción,\n"
                "     idempotencia, distributiva) hasta llegar a la\n"
                "     misma expresión, o bien…\n"
                "  3) Construye AMBAS tablas de verdad y compáralas.\n\n"
                "Si en 2ⁿ filas todas las salidas coinciden, los dos\n"
                "circuitos son intercambiables (¡aunque uno tenga 4\n"
                "puertas y el otro solo 1!).\n\n"
                "💡 Esto es lo que hace un sintetizador lógico: lee tu\n"
                "    descripción 'humana' del circuito y busca una\n"
                "    expresión MÍNIMA que dé la misma tabla.",
            "example":
                "Compara estos dos circuitos:\n\n"
                "  CIRCUITO A:   f₁ = NOT(x · y) · NOT(x + y)\n"
                "                (4 puertas: AND, OR, 2×NOT, AND final)\n\n"
                "  CIRCUITO B:   f₂ = NOR(x, y)\n"
                "                (1 puerta)\n\n"
                "Vemos su tabla:\n"
                "  (x, y)  x·y  x+y  NOT(x·y)  NOT(x+y)  f₁    f₂\n"
                "   0 0    0    0     1         1         1     1\n"
                "   0 1    0    1     1         0         0     0\n"
                "   1 0    0    1     1         0         0     0\n"
                "   1 1    1    1     0         0         0     0\n\n"
                "f₁ = f₂ en las 4 filas ⇒ EQUIVALENTES. Reemplazamos\n"
                "el circuito de 4 puertas por una sola NOR.",
            "diagram": {
                "vars": ["x", "y"],
                "gates": [
                    {"id": "G", "type": "NOR", "pos": (180, 50),
                     "inputs": ["x", "y"]},
                ],
                "outputs": [{"from": "G", "label": "f = NOR(x, y)"}],
                "trace_values": {"x": 0, "y": 0},
            },
            "q_type": "mc",
            "question":
                "Otro circuito da la tabla  [0, 1, 1, 0] (para 00,01,10,11).\n"
                "¿Cuál de los siguientes es equivalente?",
            "options": [
                "AND(x, y)",
                "OR(x, y)",
                "XOR(x, y)",
                "XNOR(x, y)",
            ],
            "correct": 2,
            "explanation":
                "El patrón [0, 1, 1, 0] es la firma de XOR: produce 1\n"
                "exactamente cuando las entradas son DIFERENTES.",
        },

        # ============== EXPERTO ===========================================

        {
            "title": "Circuito de 4 puertas con entrada negada",
            "nivel": "experto",
            "theory":
                "Los circuitos reales pueden tener varios niveles.\n"
                "Para evaluarlos, traza la señal de IZQUIERDA a DERECHA.\n\n"
                "Truco: si te lías, RENOMBRA cada salida intermedia\n"
                "(A, B, C…) y reduce el problema a aritmética binaria.",
            "example":
                "El circuito de abajo tiene 4 puertas:\n"
                "  A = NAND(x, y)\n"
                "  B = NOT(z)\n"
                "  C = AND(A, B)\n"
                "  salida = XOR(C, x)\n\n"
                "Para x=1, y=1, z=0:\n"
                "  A = NAND(1,1) = 0\n"
                "  B = NOT(0)    = 1\n"
                "  C = AND(0,1)  = 0\n"
                "  salida = XOR(0,1) = 1",
            "diagram": {
                "vars": ["x", "y", "z"],
                "gates": [
                    {"id": "A", "type": "NAND", "pos": (110, 10),
                     "inputs": ["x", "y"]},
                    {"id": "B", "type": "NOT",  "pos": (110, 110),
                     "inputs": ["z"]},
                    {"id": "C", "type": "AND",  "pos": (260, 60),
                     "inputs": ["A", "B"]},
                    {"id": "D", "type": "XOR",  "pos": (400, 35),
                     "inputs": ["C", "x"]},
                ],
                "outputs": [{"from": "D", "label": "f"}],
            },
            "q_type": "mc",
            "question":
                "Con el circuito de la figura, ¿cuánto vale  f(1, 0, 1)?",
            "options": ["0", "1", "Indefinido", "Depende"],
            "correct": 1,
            "explanation":
                "Paso a paso (x=1, y=0, z=1):\n"
                "  A = NAND(1,0) = 1\n"
                "  B = NOT(1)    = 0\n"
                "  C = AND(1,0)  = 0\n"
                "  f = XOR(0,1)  = 1",
        },

        {
            "title": "Construir XOR usando solo NAND (4 puertas)",
            "nivel": "experto",
            "theory":
                "Construcción clásica de XOR con SOLO 4 puertas NAND.\n"
                "Es un ejercicio típico en electrónica digital.\n\n"
                "Sean A = NAND(x, y) y entonces:\n"
                "  P = NAND(x, A)\n"
                "  Q = NAND(y, A)\n"
                "  XOR(x,y) = NAND(P, Q)\n\n"
                "Verifica que produce 1 SOLO cuando x ≠ y.",
            "example":
                "Trazado para x=1, y=0:\n"
                "  A = NAND(1, 0) = 1\n"
                "  P = NAND(1, 1) = 0\n"
                "  Q = NAND(0, 1) = 1\n"
                "  XOR = NAND(0, 1) = 1  ✓  (x≠y → 1)\n\n"
                "Verifica también x=1, y=1 (debe dar 0):\n"
                "  A = NAND(1,1) = 0\n"
                "  P = NAND(1,0) = 1\n"
                "  Q = NAND(1,0) = 1\n"
                "  XOR = NAND(1,1) = 0  ✓",
            "diagram": {
                "vars": ["x", "y"],
                "gates": [
                    {"id": "A", "type": "NAND", "pos": (110, 65),
                     "inputs": ["x", "y"]},
                    {"id": "P", "type": "NAND", "pos": (260, 15),
                     "inputs": ["x", "A"]},
                    {"id": "Q", "type": "NAND", "pos": (260, 110),
                     "inputs": ["y", "A"]},
                    {"id": "R", "type": "NAND", "pos": (410, 60),
                     "inputs": ["P", "Q"]},
                ],
                "outputs": [{"from": "R", "label": "x⊕y"}],
            },
            "q_type": "mc",
            "question":
                "Para x=0, y=1, ¿cuál es la salida del XOR construido?",
            "options": ["0", "1", "Depende", "Indefinido"],
            "correct": 1,
            "explanation":
                "Pasos (x=0, y=1):\n"
                "  A = NAND(0,1) = 1\n"
                "  P = NAND(0,1) = 1\n"
                "  Q = NAND(1,1) = 0\n"
                "  XOR = NAND(1,0) = 1   ✓  (x≠y → 1)",
        },

        {
            "title": "Multiplexor 2:1 (MUX) con puertas básicas",
            "nivel": "experto",
            "theory":
                "Un MUX 2:1 selecciona entre dos entradas (x0, x1)\n"
                "usando una señal de selección s:\n\n"
                "    f = x0  si  s=0\n"
                "    f = x1  si  s=1\n\n"
                "Implementación con AND/OR/NOT:\n"
                "    f = (NOT(s) AND x0)  OR  (s AND x1)\n\n"
                "Si s=0, la rama de x1 se anula y f = x0.\n"
                "Si s=1, la rama de x0 se anula y f = x1.",
            "example":
                "Para s=1, x0=0, x1=1:\n"
                "  NOT(s) = 0,  NOT(s) AND x0 = 0\n"
                "  s AND x1 = 1\n"
                "  f = 0 OR 1 = 1  ←  igual a x1, ¡correcto!\n\n"
                "El MUX es la pieza FUNDAMENTAL de las decisiones\n"
                "en un procesador (if/else en hardware).",
            "diagram": {
                "vars": ["x0", "x1", "s"],
                "gates": [
                    {"id": "N", "type": "NOT", "pos": (130, 110),
                     "inputs": ["s"]},
                    {"id": "A", "type": "AND", "pos": (260, 20),
                     "inputs": ["N", "x0"]},
                    {"id": "B", "type": "AND", "pos": (260, 100),
                     "inputs": ["s", "x1"]},
                    {"id": "C", "type": "OR",  "pos": (410, 60),
                     "inputs": ["A", "B"]},
                ],
                "outputs": [{"from": "C", "label": "f"}],
            },
            "q_type": "mc",
            "question":
                "MUX 2:1 con s=0, x0=1, x1=0. ¿Cuánto vale f?",
            "options": ["0", "1", "Depende", "Indefinido"],
            "correct": 1,
            "explanation":
                "Cuando s=0, el MUX selecciona x0. Como x0=1, f=1.\n"
                "Cálculo:  NOT(0)=1; 1·1=1; 0·0=0; 1+0 = 1.",
        },
        {
            "title": "🎬 Circuito interactivo f(x,y,z) = (x+y)·z (Sesión 2)",
            "nivel": "intermedio",
            "theory":
                "Este es el circuito estrella de la sesión. La función "
                "f(x,y,z) = (x+y)·z combina DOS puertas en cascada:\n\n"
                "  1) Primero una puerta OR suma x e y:  A = x + y.\n"
                "  2) Luego una puerta AND multiplica ese resultado por "
                "z:  f = A · z.\n\n"
                "TRAZADO de la señal (de izquierda a derecha):\n"
                "  La entrada A de la AND es lo que sale de la OR.\n"
                "  La segunda entrada de la AND es z directamente.\n\n"
                "Observacion clave: como la salida pasa por una AND con "
                "z, si z = 0 la AND se ANULA y f = 0 siempre, da igual "
                "cuanto valgan x e y. z actua como un 'interruptor "
                "maestro'.\n\n"
                "💡 Pulsa ▶ Animar y prueba otras entradas: veras como "
                "la señal se propaga puerta a puerta hasta la salida f.",
            "example":
                "Con x=1, y=0, z=1:\n"
                "  A = x + y = 1 + 0 = 1  (la OR pasa a 1).\n"
                "  f = A · z = 1 · 1 = 1  (la AND deja pasar).\n"
                "Resultado: f = 1.\n\n"
                "Si ahora bajamos z a 0 manteniendo x=1, y=0:\n"
                "  f = 1 · 0 = 0. La AND queda anulada por z.",
            "diagram": {
                "vars": ["x", "y", "z"],
                "gates": [
                    {"id": "A", "type": "OR",  "pos": (110, 30),
                     "inputs": ["x", "y"], "etiqueta": "OR"},
                    {"id": "G", "type": "AND", "pos": (260, 55),
                     "inputs": ["A", "z"], "etiqueta": "AND"},
                ],
                "outputs": [{"from": "G", "label": "f"}],
                "trace_values": {"x": 1, "y": 0, "z": 1},
            },
            "q_type": "mc",
            "question": "¿Cuánto vale f(x,y,z) = (x+y)·z con x=1, y=0, z=0?",
            "options": ["0", "1"],
            "correct": 0,
            "explanation":
                "x+y = 1+0 = 1, pero la AND multiplica por z=0: f = 1·0 "
                "= 0. Siempre que z=0 la AND se anula y f vale 0.",
        },
        {
            "title": "🎬 Circuito XNOR (NXOR) detector de igualdad (Sesión 2)",
            "nivel": "experto",
            "theory":
                "La función XNOR (o NXOR) detecta cuando dos bits "
                "COINCIDEN. Su expresion algebraica es:\n\n"
                "      f = x·y + x̄·ȳ\n\n"
                "Se lee: 'ambos a 1' (x·y) O BIEN 'ambos a 0' (x̄·ȳ). "
                "x̄ significa NOT x.\n\n"
                "Construccion con puertas basicas:\n"
                "  NOT(x) -> x̄     NOT(y) -> ȳ\n"
                "  AND(x, y)   -> A1  (1 cuando ambos valen 1)\n"
                "  AND(x̄, ȳ) -> A2  (1 cuando ambos valen 0)\n"
                "  OR(A1, A2)  -> f   (1 si se cumple cualquiera de los "
                "dos casos)\n\n"
                "XNOR es el bicondicional bit a bit (x ↔ y): vale 1 "
                "cuando las entradas son IGUALES y 0 cuando difieren. Es "
                "justo el opuesto del XOR.\n\n"
                "💡 Pulsa ▶ Animar y prueba (0,0), (1,1), (0,1): observa "
                "que solo se enciende f cuando las entradas coinciden.",
            "example":
                "Con x=1, y=1:\n"
                "  A1 = x·y = 1·1 = 1.\n"
                "  A2 = x̄·ȳ = 0·0 = 0.\n"
                "  f = A1 + A2 = 1 + 0 = 1  (coinciden, se enciende).\n\n"
                "Con x=0, y=1:\n"
                "  A1 = 0·1 = 0,  A2 = 1·0 = 0.\n"
                "  f = 0 + 0 = 0  (son distintos, se apaga).",
            "diagram": {
                "vars": ["x", "y"],
                "gates": [
                    {"id": "NX", "type": "NOT", "pos": (90, 95),
                     "inputs": ["x"], "etiqueta": "NOT"},
                    {"id": "NY", "type": "NOT", "pos": (90, 125),
                     "inputs": ["y"], "etiqueta": "NOT"},
                    {"id": "A1", "type": "AND", "pos": (200, 30),
                     "inputs": ["x", "y"], "etiqueta": "AND"},
                    {"id": "A2", "type": "AND", "pos": (200, 105),
                     "inputs": ["NX", "NY"], "etiqueta": "AND"},
                    {"id": "G",  "type": "OR",  "pos": (310, 65),
                     "inputs": ["A1", "A2"], "etiqueta": "OR"},
                ],
                "outputs": [{"from": "G", "label": "f"}],
                "trace_values": {"x": 1, "y": 1},
            },
            "q_type": "tt",
            "question":
                "Rellena la tabla de verdad de la XNOR f = x·y + x̄·ȳ.\n"
                "(Escribe 0 o 1 en cada celda)",
            "options": [],
            "correct": [1, 0, 0, 1],
            "explanation":
                "XNOR da 1 cuando las entradas COINCIDEN: (0,0) -> "
                "0+1·1=1 y (1,1) -> 1·1+0=1. Cuando difieren, (0,1) y "
                "(1,0), ambos productos dan 0 y f=0. Es el detector de "
                "igualdad, opuesto del XOR.",
        },
        {
            "title": "🎬 Una sola puerta: AND con sus casillas (Sesión 2)",
            "nivel": "básico",
            "theory":
                "Antes de encadenar puertas conviene dominar UNA sola. "
                "La puerta AND realiza el producto booleano:\n\n"
                "      f = x · y\n\n"
                "Solo se enciende (f=1) cuando AMBAS entradas valen 1. "
                "En cualquier otro caso da 0. Por eso se dice que es la "
                "puerta mas 'exigente'.\n\n"
                "  x   y  |  x·y\n"
                "  0   0  |   0\n"
                "  0   1  |   0\n"
                "  1   0  |   0\n"
                "  1   1  |   1\n\n"
                "💡 Pulsa ▶ Animar y cambia las casillas x e y: la "
                "salida solo se ilumina cuando pones las dos a 1.",
            "example":
                "Con x=1, y=1:  f = 1·1 = 1 (la unica combinacion que "
                "enciende la salida).\n"
                "Con x=1, y=0:  f = 1·0 = 0 (basta un 0 para apagarla).",
            "diagram": {
                "vars": ["x", "y"],
                "gates": [
                    {"id": "G", "type": "AND", "pos": (180, 50),
                     "inputs": ["x", "y"], "etiqueta": "AND"},
                ],
                "outputs": [{"from": "G", "label": "f"}],
                "trace_values": {"x": 1, "y": 1},
            },
            "q_type": "tt",
            "question": "Rellena la tabla de verdad de la puerta AND (f = x·y).",
            "options": [],
            "correct": [0, 0, 0, 1],
            "explanation":
                "La AND solo da 1 en la fila (1,1). En las otras tres "
                "combinaciones siempre hay al menos un 0, asi que f=0.",
        },
    ],

    # =================================================================
    "1.4  Lógica de predicados": [

        {
            "title": "¿Qué es un predicado?",
            "theory":
                "Un PREDICADO es una proposición CON UN HUECO (variable).\n"
                "El hueco se rellena con un valor concreto, y entonces\n"
                "el predicado se vuelve V o F.\n\n"
                "Notación:   p(x):  'x es par'\n"
                "  p(2) = V     (2 es par)\n"
                "  p(3) = F     (3 no es par)\n"
                "  p(8) = V\n\n"
                "Pueden tener varios huecos:\n"
                "   p(x, y): 'x es mayor que y'\n"
                "  p(5, 3) = V\n"
                "  p(1, 2) = F",
            "example":
                "Cualquier 'if' de un programa esconde un predicado:\n"
                "    if x > 0:           ← predicado p(x): 'x > 0'\n"
                "        y = 1\n"
                "    else:\n"
                "        y = 0",
            "q_type": "mc",
            "question":
                "Sea p(x): 'x es un número primo'. ¿Cuál es V?",
            "options": [
                "p(4)",
                "p(6)",
                "p(7)",
                "p(9)",
            ],
            "correct": 2,
            "explanation":
                "Los primos hasta 10: 2, 3, 5, 7.\n"
                "  p(4)=F (4=2·2)   p(6)=F (6=2·3)\n"
                "  p(7)=V           p(9)=F (9=3·3)",
        },

        {
            "title": "Universo de discurso (U)",
            "theory":
                "El UNIVERSO U es el conjunto de valores que puede\n"
                "tomar la variable de un predicado. Hay que fijarlo\n"
                "ANTES de evaluar.\n\n"
                "Ejemplos:\n"
                "  p(x): 'x es estudiante'   →  U = personas\n"
                "  p(x): 'x es par'          →  U = números enteros\n"
                "  p(x): 'x es capital'      →  U = ciudades\n\n"
                "Si el universo no tiene sentido, la pregunta no tiene\n"
                "sentido. ('¿es par el color azul?' no tiene sentido).",
            "example":
                "Mismo predicado, distinto universo, distinta respuesta:\n"
                "  p(x): 'x < 5'   con U = {1,2,3,4}   → todos cumplen\n"
                "  p(x): 'x < 5'   con U = {1,2,...,10} → no todos cumplen",
            "q_type": "info",
            "question": "",
            "options": [],
            "correct": None,
            "explanation": "",
        },

        {
            "title": "Cuantificador ∀ (para todo)",
            "theory":
                "El símbolo ∀ se lee 'para todo'.\n"
                "      ∀x, p(x)   significa\n"
                "      'para CADA x del universo, p(x) es V'.\n\n"
                "Es V solo si TODOS los elementos cumplen p.\n"
                "Basta UN solo caso F (contraejemplo) para que sea F.\n\n"
                "💡 En Python:  ∀x, p(x)  ↔   all(p(x) for x in U)",
            "example":
                "U = {2, 4, 6, 8} ;  p(x): 'x es par'\n"
                "  ∀x ∈ U, p(x)  →  V (todos son pares)\n\n"
                "U = {2, 3, 4} ;  p(x): 'x es par'\n"
                "  ∀x ∈ U, p(x)  →  F  (3 NO es par, contraejemplo)",
            "q_type": "tf",
            "question":
                "U = {1, 2, 3, 4, 5}. ¿Es V que  ∀x ∈ U,  x < 10  ?",
            "options": ["Verdadero", "Falso"],
            "correct": 0,
            "explanation":
                "Sí. Cada elemento de U (1,2,3,4,5) cumple 'x < 10'.\n"
                "No hay contraejemplo, así que ∀ es V.",
        },

        {
            "title": "Cuantificador ∃ (existe)",
            "theory":
                "El símbolo ∃ se lee 'existe (al menos uno)'.\n"
                "      ∃x : p(x)   significa\n"
                "      'hay al menos un x del universo con p(x) = V'.\n\n"
                "Es V si encuentras UNO solo que cumpla. Es F solo si\n"
                "NINGUNO cumple.\n\n"
                "💡 En Python:  ∃x, p(x)  ↔   any(p(x) for x in U)",
            "example":
                "U = {1, 2, 3} ;  p(x): 'x es par'\n"
                "  ∃x ∈ U : p(x)  →  V (el 2 cumple, ¡basta uno!)\n\n"
                "U = {1, 3, 5} ;  p(x): 'x es par'\n"
                "  ∃x ∈ U : p(x)  →  F (ninguno cumple)",
            "q_type": "tf",
            "question":
                "U = {2, 4, 6, 8}. ¿Es V que  ∃x ∈ U,  x es impar?",
            "options": ["Verdadero", "Falso"],
            "correct": 1,
            "explanation":
                "No. Todos son pares. Ninguno cumple 'ser impar'.\n"
                "Por tanto ∃ es F.",
        },

        {
            "title": "Negación de cuantificadores (Morgan generalizado)",
            "theory":
                "Las leyes de Morgan se extienden a cuantificadores:\n\n"
                "  ¬(∀x, p(x))   ≡   ∃x, ¬p(x)\n"
                "  ¬(∃x : p(x))  ≡   ∀x, ¬p(x)\n\n"
                "💡 Truco mnemotécnico: al meter la ¬,\n"
                "el cuantificador se INVIERTE (∀ ↔ ∃)\n"
                "y la negación pasa al predicado.\n\n"
                "Lectura natural:\n"
                "  'no todos son pares'  =  'existe alguno que no es par'\n"
                "  'no existe ninguno par' = 'todos son no pares'",
            "example":
                "U = {1,2,3,4}\n"
                "  ¬(∀x, x es par) = V  ('no todos son pares')\n"
                "  ∃x, ¬(x es par) = V  ('existe uno impar': el 1)\n"
                "Ambos dan V. ✓",
            "q_type": "mc",
            "question":
                "¿A qué equivale  ¬(∃x : p(x)) ?",
            "options": [
                "∃x : ¬p(x)",
                "∀x, p(x)",
                "∀x, ¬p(x)",
                "¬p(x)",
            ],
            "correct": 2,
            "explanation":
                "El ∃ se convierte en ∀ y la negación pasa dentro:\n"
                "  ¬(∃x : p(x)) = ∀x, ¬p(x)",
            "simple_explanation":
                "REGLA INTUITIVA (la lectura en castellano coincide):\n\n"
                "  ¬(∃x: p) = «NO existe ningún x con p»\n"
                "         = «TODO x cumple ¬p»  →  ∀x, ¬p(x)\n\n"
                "  ¬(∀x, p) = «NO todos cumplen p»\n"
                "         = «existe ALGUNO que no cumple p»\n"
                "                                  →  ∃x, ¬p(x)\n\n"
                "Memoriza esto:\n"
                "  AL METER LA NEGACIÓN DENTRO,\n"
                "  el cuantificador SE DA LA VUELTA (∀↔∃)\n"
                "  y la negación pasa al predicado.",
            "similar_examples": [
                "Ejemplo cotidiano:\n"
                "  «Todos los cisnes son blancos» → ∀x: blanco(x)\n"
                "  Negar: «Existe un cisne NO blanco» → ∃x: ¬blanco(x).\n"
                "  Basta UN cisne negro para tumbar el ∀.",

                "Otro:\n"
                "  «Existe un alumno que aprueba» → ∃x: aprueba(x).\n"
                "  Negar: «NINGÚN alumno aprueba» = «∀x: NO aprueba(x)».\n"
                "  El ∃ se vuelve ∀ y aprueba se vuelve ¬aprueba.",

                "Combinado con ∧:\n"
                "  ¬(∀x, p(x) ∧ q(x))\n"
                "    = ∃x, ¬(p(x) ∧ q(x))\n"
                "    = ∃x, ¬p(x) ∨ ¬q(x)       (Morgan)\n"
                "Leer: 'existe un x donde falla p o falla q'.",
            ],
        },

        {
            "title": "¡El ORDEN de los cuantificadores importa!",
            "theory":
                "Cambiar el orden de ∀ y ∃ cambia el significado por\n"
                "completo. Compara:\n\n"
                "  (1)   ∀x ∈ ℕ,  ∃y ∈ ℕ :  y > x\n"
                "        'para cada x, existe ALGÚN y mayor'\n"
                "        → V (siempre podemos tomar y = x+1)\n\n"
                "  (2)   ∃y ∈ ℕ :  ∀x ∈ ℕ,  y > x\n"
                "        'existe UN y que es mayor que TODO x'\n"
                "        → F (no hay un natural mayor que todos)\n\n"
                "💡 Regla: en (1), el y puede DEPENDER de x.\n"
                "En (2), el y debe servir para TODOS los x a la vez.",
            "example":
                "Frase de la vida real:\n"
                "  'Para toda cerradura existe una llave'  → V (probable)\n"
                "  'Existe una llave para toda cerradura'  → F (no hay llave universal)",
            "q_type": "tf",
            "question":
                "¿Tiene siempre el mismo significado  ∀x ∃y P(x,y)\n"
                "que  ∃y ∀x P(x,y)?",
            "options": ["Verdadero", "Falso"],
            "correct": 1,
            "explanation":
                "FALSO. El orden importa. En la primera, el y puede\n"
                "depender del x. En la segunda, el y es ÚNICO y vale\n"
                "para todos los x.",
            "simple_explanation":
                "TRUCO MENTAL: el ORDEN de los cuantificadores cambia\n"
                "QUIÉN ELIGE PRIMERO.\n\n"
                "  ∀x ∃y :   Primero te dan UN x; tú eliges DESPUÉS un y.\n"
                "             El y PUEDE DEPENDER del x.\n\n"
                "  ∃y ∀x :   PRIMERO eliges UN y; ese y debe servir\n"
                "             PARA TODOS los x que vengan después.\n"
                "             El y es ÚNICO para todos.\n\n"
                "El segundo es más fuerte: es como decir 'tengo una\n"
                "llave maestra' frente a 'para cada puerta tengo SU llave'.",
            "similar_examples": [
                "Llaves y cerraduras:\n"
                "  ∀ cerradura, ∃ llave que la abre. → V (cada una tiene la suya)\n"
                "  ∃ llave, ∀ cerradura: la llave abre TODAS. → F (no hay maestra)\n"
                "El mismo enunciado verbal, distinto orden, distinto valor.",

                "Números reales:\n"
                "  ∀x ∈ ℝ, ∃y ∈ ℝ: y > x. → V (siempre y = x+1).\n"
                "  ∃y ∈ ℝ, ∀x ∈ ℝ: y > x. → F (no hay máximo en ℝ).\n"
                "El primer y depende de x; el segundo debe ser único.",

                "ε-δ en cálculo (clave en límites):\n"
                "  ∀ε > 0, ∃δ > 0 : si |x-c| < δ ⇒ |f(x)-L| < ε.\n"
                "  → δ DEPENDE de ε. Para cada precisión ε tú eliges δ.\n"
                "Si fuera al revés (∃δ ∀ε...) los límites no existirían.",
            ],
        },
    ],

    # =================================================================
    "1.5  Lógica inductiva": [

        {
            "title": "¿Qué es la lógica INDUCTIVA?",
            "theory":
                "La lógica INDUCTIVA va de lo PARTICULAR a lo GENERAL.\n"
                "Observas varios casos y construyes una regla general.\n\n"
                "Ejemplo cotidiano:\n"
                "  • Vi 100 cisnes y los 100 eran blancos.\n"
                "  • Conclusión inductiva: 'todos los cisnes son blancos'.\n"
                "  • Pero existe el cisne negro... no tiene GARANTÍA.\n\n"
                "Contraste con la lógica DEDUCTIVA (la que vimos antes):\n"
                "  • Deducción: regla → caso (GARANTIZA la conclusión).\n"
                "  • Inducción: casos → regla (es solo HIPÓTESIS).",
            "example":
                "Inducción típica de IA:\n"
                "  Datos: 10.000 fotos etiquetadas 'gato' / 'no gato'.\n"
                "  Resultado: un modelo que adivina si nuevas fotos\n"
                "  son gatos. Es una HIPÓTESIS, puede fallar.",
            "q_type": "mc",
            "question":
                "Cuál es un razonamiento INDUCTIVO:",
            "options": [
                "Todos los humanos son mortales; Sócrates es humano; "
                "luego Sócrates es mortal.",
                "He visto 50 manzanas rojas, luego todas las manzanas son rojas.",
                "Si llueve, el suelo se moja. Llueve. Luego se moja.",
                "2+2=4 porque está demostrado en matemáticas.",
            ],
            "correct": 1,
            "explanation":
                "La 2ª es inducción: SALTA de muchos casos particulares\n"
                "(50 manzanas) a una regla general. No está garantizado.\n"
                "Las otras tres son DEDUCCIÓN (la conclusión está\n"
                "asegurada por las premisas).",
        },

        {
            "title": "Programación Lógica Inductiva (ILP)",
            "theory":
                "ILP = Inductive Logic Programming.\n"
                "Es la intersección entre:\n"
                "  • aprendizaje INDUCTIVO (sacar reglas de ejemplos), y\n"
                "  • programación LÓGICA (representación formal de datos).\n\n"
                "Esquema típico:\n"
                "  1. Tienes ejemplos POSITIVOS (lo que sí se cumple).\n"
                "  2. Tienes ejemplos NEGATIVOS (lo que no se cumple).\n"
                "  3. Tienes conocimiento de BASE.\n"
                "  4. El sistema busca una REGLA (hipótesis) que cubra\n"
                "     los positivos y excluya los negativos.",
            "example":
                "Datos:\n"
                "  Diabético(Ana),  HijoDe(Ana, José),  PredisposGen(José)\n"
                "  Diabético(Tomás),HijoDe(Tomás, Álvaro),PredisposGen(Álvaro)\n\n"
                "Hipótesis inducida:\n"
                "  Diabético(X)  ←  HijoDe(X,Y) ∧ PredisposGen(Y)\n\n"
                "Significa: 'si tu padre tiene predisposición genética,\n"
                "entonces tú eres diabético'.",
            "q_type": "info",
            "question": "",
            "options": [],
            "correct": None,
            "explanation": "",
        },

        {
            "title": "Árbol de decisión (ejemplo del examen)",
            "theory":
                "Un ÁRBOL DE DECISIÓN es una forma muy gráfica de\n"
                "representar reglas inducidas.\n\n"
                "Reglas del manual:\n"
                "  Si dedicación = ALTA   → APRUEBA\n"
                "  Si dedicación = BAJA   → SUSPENDE\n"
                "  Si dedicación = MEDIA  → depende:\n"
                "         dificultad BAJA → APRUEBA\n"
                "         dificultad MEDIA + tipo TEST → APRUEBA\n"
                "         resto → SUSPENDE\n\n"
                "Árbol:\n"
                "                   Dedicación\n"
                "             /        |          \\\n"
                "          alta     media         baja\n"
                "           ↓         ↓            ↓\n"
                "         APRUEBA  Dificultad   SUSPENDE\n"
                "                  /    |    \\\n"
                "                baja  media  alta\n"
                "                 ↓     ↓      ↓\n"
                "             APRUEBA  Tipo  SUSPENDE\n"
                "                     /    \\\n"
                "                  test   otro\n"
                "                   ↓       ↓\n"
                "               APRUEBA  SUSPENDE",
            "example":
                "Estudiante con dedicación=ALTA, dificultad=ALTA → APRUEBA.\n"
                "Estudiante con dedicación=MEDIA, dificultad=ALTA → SUSPENDE.",
            "q_type": "mc",
            "question":
                "Un estudiante: dedicación=MEDIA, dificultad=MEDIA, tipo=TEST.\n"
                "Según el árbol, ¿cuál es la predicción?",
            "options": ["APRUEBA", "SUSPENDE", "Depende", "No se puede saber"],
            "correct": 0,
            "explanation":
                "Recorrido por el árbol:\n"
                "  dedicación=MEDIA → vamos al subárbol\n"
                "  dificultad=MEDIA → bajamos a Tipo\n"
                "  tipo=TEST → APRUEBA  ✓",
        },

        {
            "title": "Generalización: rlgg",
            "theory":
                "rlgg = 'Relative Least General Generalization'\n"
                "(generalización relativa menos general).\n\n"
                "IDEA: dados dos casos, busca la regla MÍNIMA que los\n"
                "abarca a ambos sustituyendo las constantes por\n"
                "VARIABLES comunes.\n\n"
                "Ejemplo paso a paso:\n"
                "  C1: Diabético(Ana)   ∧ HijoDe(Ana, José)\n"
                "  C2: Diabético(Tomás) ∧ HijoDe(Tomás, Álvaro)\n\n"
                "Comparamos:\n"
                "  Diabético(Ana) y Diabético(Tomás) → Diabético(X)\n"
                "  HijoDe(Ana,José) y HijoDe(Tomás,Álvaro) → HijoDe(X,Y)\n\n"
                "Generalización:  Diabético(X) ∧ HijoDe(X, Y)",
            "example":
                "Patrón parecido a 'unificación' en Prolog.\n"
                "Cuanto MÁS común sea el patrón, MÁS general es la regla.",
            "q_type": "mc",
            "question":
                "¿Cuál es la generalización rlgg de:\n"
                "  C1: Padre(Juan, Pedro)\n"
                "  C2: Padre(Luis, María) ?",
            "options": [
                "Padre(X, X)",
                "Padre(X, Y)",
                "Padre(Juan, Y)",
                "Padre(X, Pedro)",
            ],
            "correct": 1,
            "explanation":
                "Cada posición tiene constantes distintas (Juan/Luis y\n"
                "Pedro/María), por lo que ambas se sustituyen por\n"
                "variables: X e Y.  →  Padre(X, Y).",
        },

        {
            "title": "Inducción predictiva vs descriptiva",
            "theory":
                "Dos sabores de inducción:\n\n"
                "• PREDICTIVA (supervisada):\n"
                "  - Tienes datos ETIQUETADOS (cada caso tiene 'respuesta').\n"
                "  - Aprendes una regla que PREDICE la etiqueta.\n"
                "  - Ej.: árboles de decisión, clasificación.\n\n"
                "• DESCRIPTIVA (no supervisada):\n"
                "  - NO tienes etiquetas, solo datos.\n"
                "  - Buscas PATRONES interesantes que los describan.\n"
                "  - Ej.: reglas de asociación, subgrupos.\n\n"
                "💡 Predictiva = 'aprende a contestar'.\n"
                "💡 Descriptiva = 'aprende a observar'.",
            "example":
                "Predictiva:\n"
                "  'Si edad>60 y colesterol alto → riesgo cardíaco'\n"
                "Descriptiva:\n"
                "  'Quienes compran pan suelen comprar mantequilla'\n"
                "  (regla de asociación clásica de supermercado)",
            "q_type": "mc",
            "question":
                "Identifica el tipo de tarea:\n"
                "'Encontrar qué productos se compran juntos en una tienda,\n"
                "sin saber a priori cuáles relacionar.'",
            "options": [
                "Inducción predictiva",
                "Inducción descriptiva",
                "Deducción",
                "Tautología",
            ],
            "correct": 1,
            "explanation":
                "Es DESCRIPTIVA: no hay etiqueta a predecir, buscamos\n"
                "patrones (qué productos coocurren).\n"
                "Es el clásico problema de 'cesta de la compra'.",
        },
        {
            "title": "🎬 Arbol de decision: aprobar el examen (Sesión 3)",
            "nivel": "intermedio",
            "theory":
                "Un ARBOL DE DECISION encadena preguntas para llegar a una "
                "conclusion. Se lee desde la raiz, eligiendo la rama segun "
                "el valor de cada atributo.\n\n"
                "Reglas para predecir si se aprueba:\n"
                "• Dedicacion = Alta  →  Aprobado.\n"
                "• Dedicacion = Media y Dificultad = Baja  →  Aprobado.\n"
                "• Dedicacion = Media y Dificultad = Alta  →  Suspenso.\n"
                "• Dedicacion = Media y Dificultad = Media:\n"
                "      Tipo = Test   →  Aprobado.\n"
                "      Tipo distinto de Test  →  Suspenso.\n\n"
                "Primero se mira la DEDICACION; si es Media se mira la "
                "DIFICULTAD; y si esta es Media se mira el TIPO de examen.\n\n"
                "💡 Cada hoja (verde = Aprobado, rojo = Suspenso) es la "
                "decision final de ese camino.",
            "example":
                "Caso: Dedicacion = Media, Dificultad = Media, Tipo = Test.\n"
                "Recorrido:  Dedicacion --Media--> Dificultad --Media--> "
                "Tipo --Test--> Aprobado.",
            "q_type": "mc",
            "question":
                "Un alumno con Dedicacion = Media, Dificultad = Media y "
                "Tipo = Test, ¿que resultado obtiene?",
            "options": [
                "Aprobado",
                "Suspenso",
                "Depende, el arbol no decide",
                "Faltan datos para decidir",
            ],
            "correct": 0,
            "explanation":
                "Bajamos por Dedicacion=Media hasta Dificultad, luego por "
                "Dificultad=Media hasta Tipo, y por Tipo=Test llegamos a la "
                "hoja Aprobado. Resultado: APROBADO.",
            "visual": {
                "tipo": "arbol",
                "title": "Aprobar el examen",
                "root": {
                    "label": "Dedicacion",
                    "children": [
                        {"label": "Aprobado", "edge_label": "Alta", "color": "#16361f"},
                        {"label": "Dificultad", "edge_label": "Media", "children": [
                            {"label": "Aprobado", "edge_label": "Baja", "color": "#16361f"},
                            {"label": "Suspenso", "edge_label": "Alta", "color": "#3a1d1d"},
                            {"label": "Tipo", "edge_label": "Media", "children": [
                                {"label": "Aprobado", "edge_label": "Test", "color": "#16361f"},
                                {"label": "Suspenso", "edge_label": "otro", "color": "#3a1d1d"},
                            ]},
                        ]},
                    ],
                },
            },
        },
    ],

    # =================================================================
    "1.6  Complejidad computacional": [
        {
            "title": "Introducción a la complejidad",
            "nivel": "básico",
            "q_type": "info",
            "question": "",
            "options": [],
            "correct": None,
            "explanation": "",
            "theory":
                "La complejidad computacional es la magnitud de la\n"
                "complejidad de un algoritmo que da solución a un\n"
                "problema decidible o computable (manual 1.6).\n\n"
                "Un problema es decidible si sus respuestas posibles\n"
                "son sólo SÍ o NO (1/0, V/F).\n\n"
                "Para resolverlo necesitamos dos recursos:\n"
                "  • Tiempo: número de pasos T(n) que ejecuta el\n"
                "    algoritmo en función del tamaño de entrada n.\n"
                "  • Espacio: cantidad de memoria S(n) requerida.\n\n"
                "El tiempo se considera el recurso crítico, ya que\n"
                "el espacio es reutilizable y, hoy en día, abundante;\n"
                "el tiempo, en cambio, no se recupera.\n\n"
                "Hablamos de problemas tratables (resolubles de forma\n"
                "razonable, como búsqueda y ordenación) e intratables\n"
                "(como las torres de Hanoi o el problema del viajero).",
            "example":
                "Problema del viajero con N=10 ciudades:\n"
                "  combinaciones a explorar = N! = 10! = 3 628 800.\n"
                "Con N=12 sube a 479 001 600. El crecimiento es\n"
                "factorial, no polinómico → problema intratable.",
        },
        {
            "title": "Notación O grande (cota asintótica)",
            "nivel": "básico",
            "theory":
                "Para comparar algoritmos usamos la notación O(f(n)),\n"
                "que describe cómo crece T(n) cuando n → ∞.\n\n"
                "Decimos que T(n) ∈ O(f(n)) si existen constantes\n"
                "c > 0 y n₀ tales que T(n) ≤ c·f(n) para todo n ≥ n₀.\n\n"
                "Jerarquía habitual de menor a mayor coste:\n"
                "  O(1) ≤ O(log n) ≤ O(n) ≤ O(n log n)\n"
                "  ≤ O(n²) ≤ O(n³) ≤ O(2ⁿ) ≤ O(n!)\n\n"
                "Las funciones polinómicas (nᵏ) se consideran\n"
                "tratables; las exponenciales y factoriales, no.",
            "example":
                "Buscar un valor en una lista NO ordenada de n=1000\n"
                "elementos:\n"
                "  • Búsqueda lineal:    T(n)=n     → 1000 pasos.\n"
                "  • Búsqueda binaria*:  T(n)=log₂n → ≈ 10 pasos.\n"
                "(*requiere lista ordenada).\n\n"
                "Tabla comparativa con n=10⁶:\n"
                "  O(log n) ≈ 20\n"
                "  O(n)     ≈ 10⁶   (≈ 1 segundo)\n"
                "  O(n²)    ≈ 10¹²  (≈ 11 días)\n"
                "  O(2ⁿ)    ≈ 10³⁰¹⁰³⁰ (más que átomos del universo)\n\n"
                "Otro ejemplo: ordenar n elementos.\n"
                "  Bubble sort:  O(n²)\n"
                "  Merge sort:   O(n log n)\n"
                "Para n=10⁶: bubble ≈ 10¹², merge ≈ 2·10⁷.\n"
                "Merge gana por un factor de 50 000.",
            "q_type": "mc",
            "question":
                "Para n=1 000 000, ¿qué algoritmo es MÁS eficiente\n"
                "según su complejidad temporal?",
            "options": [
                "Uno con T(n) = n²",
                "Uno con T(n) = n·log₂ n",
                "Uno con T(n) = 2ⁿ",
                "Uno con T(n) = n!",
            ],
            "correct": 1,
            "explanation":
                "n·log₂n ≈ 2·10⁷ operaciones; n² = 10¹² (un millón\n"
                "de veces peor); 2ⁿ y n! son astronómicamente mayores.",
        },
        {
            "title": "Modelos de computación: Turing y RAM",
            "nivel": "intermedio",
            "theory":
                "Para razonar formalmente sobre algoritmos usamos\n"
                "modelos de cómputo. El más clásico es la Máquina\n"
                "de Turing (MT), definida por Alan Turing.\n\n"
                "Según el manual 1.6.2, la MT 'modeliza la idea de\n"
                "una persona haciendo cálculos provista de lápiz y\n"
                "un borrador'. Cada MT resuelve un problema y\n"
                "representa un algoritmo.\n\n"
                "Distinguimos dos variantes:\n"
                "  • MT determinista (MTD): de un estado existe\n"
                "    UNA sola transición posible.\n"
                "  • MT no determinista (MTND): de un estado puede\n"
                "    haber VARIAS transiciones posibles.\n\n"
                "El modelo RAM (Random Access Machine) es una\n"
                "alternativa más cercana al ordenador real. Para\n"
                "clasificar complejidad, MT y RAM son equivalentes\n"
                "salvo factores polinómicos.",
            "example":
                "Detección del valor 7 en la lista [3, 5, 7, 9]:\n"
                "una MTD recorre celda a celda y se detiene al\n"
                "encontrarlo. Una MTND podría 'adivinar' la posición\n"
                "y verificarla en un único paso.",
            "q_type": "tf",
            "question":
                "Según el manual, una MT determinista admite, desde\n"
                "un mismo estado, varias transiciones distintas.",
            "options": ["Verdadero", "Falso"],
            "correct": 1,
            "explanation":
                "Falso. En la MT determinista existe UNA única\n"
                "transición posible de un estado a otro.",
        },
        {
            "title": "Clases P, NP y NP-Completo",
            "nivel": "experto",
            "theory":
                "Llamamos tiempo polinómico al tiempo de ejecución\n"
                "que se considera asumible (manual 1.6.3).\n\n"
                "  • Clase P: problemas resolubles por una MT\n"
                "    DETERMINISTA en tiempo polinómico. Son los\n"
                "    'tratables' (ordenación, búsqueda, etc.).\n\n"
                "  • Clase NP: problemas resolubles por una MT NO\n"
                "    determinista en tiempo polinómico.\n"
                "    Como toda MTD es un caso particular de MTND,\n"
                "    se cumple P ⊆ NP.\n\n"
                "  • Clase NP-Completo: un problema X es NP-Completo\n"
                "    si está en NP y, además, todo problema de NP\n"
                "    se puede reducir a X.\n\n"
                "La pregunta abierta más célebre: ¿P = NP?",
            "example":
                "Ejemplos por clase:\n"
                "  • P:           ordenar n números (n log n).\n"
                "  • NP:          SAT (satisfacibilidad booleana).\n"
                "  • NP-Completo: SAT, viajante (TSP decisión),\n"
                "                 mochila, coloreo de grafos.",
            "q_type": "mc",
            "question":
                "¿Cuál de las siguientes afirmaciones es correcta\n"
                "según las definiciones del manual?",
            "options": [
                "P y NP son conjuntos disjuntos.",
                "P ⊆ NP, porque toda MTD es un caso particular de MTND.",
                "Todo problema NP es automáticamente NP-Completo.",
                "Los problemas de ordenación pertenecen a NP-Completo.",
            ],
            "correct": 1,
            "explanation":
                "El manual indica que los MTD son un caso particular\n"
                "de MTND, luego P ⊆ NP.",
        },
    ],

    # =================================================================
    "1.7  Teoría de grafos": [
        {
            "title": "¿Qué es un grafo? (V, E, ψ)",
            "nivel": "básico",
            "q_type": "info",
            "question": "",
            "options": [],
            "correct": None,
            "explanation": "",
            "theory":
                "La teoría de grafos fue diseñada por Leonhard Euler\n"
                "(s. XVIII) para resolver problemas de conectividad.\n\n"
                "Un grafo es una terna G = (V, E, ψ), donde:\n"
                "  • V = conjunto de vértices (nodos).\n"
                "  • E = conjunto de aristas (lados).\n"
                "  • ψ: E → Ω es la aplicación de incidencia, que\n"
                "    asigna a cada arista el par {v, v'} de los dos\n"
                "    vértices que conecta.\n\n"
                "Para simplificar, suele identificarse cada arista\n"
                "directamente con su par de vértices, e = {v, v'}.\n\n"
                "Un grafo simple no contiene aristas múltiples ni\n"
                "bucles (aristas que unen un vértice consigo mismo).",
            "example":
                "Sea V = {v1, v2, v3, v4} y\n"
                "E = {e1, e2, e3, e4} con\n"
                "  ψ(e1) = {v1, v2}\n"
                "  ψ(e2) = {v1, v3}\n"
                "  ψ(e3) = {v2, v3}\n"
                "  ψ(e4) = {v3, v4}\n"
                "Este grafo es simple: ninguna arista se repite y\n"
                "ningún vértice se une a sí mismo.",
        },
        {
            "title": "Grafo dirigido vs no dirigido",
            "nivel": "básico",
            "theory":
                "En un grafo NO DIRIGIDO la incidencia es un conjunto\n"
                "{v, v'}: la arista se recorre en ambos sentidos.\n\n"
                "En un grafo DIRIGIDO, ψ: E → V × V devuelve un par\n"
                "ORDENADO (v, v'). Se dibujan con flechas.\n\n"
                "Matriz de adyacencia A (n×n):\n"
                "  A(i,j) = 1 si vi → vj hay arista, 0 si no.\n"
                "  • No dirigido → A es SIMÉTRICA.\n"
                "  • Dirigido    → A puede NO ser simétrica.",
            "example":
                "Grafo dirigido con V={v1,v2,v3,v4} y aristas\n"
                "(1,2), (1,3), (2,1), (2,4), (3,4).\n\n"
                "Matriz de adyacencia (filas = origen):\n"
                "        v1 v2 v3 v4\n"
                "   v1 [  0  1  1  0 ]\n"
                "   v2 [  1  0  0  1 ]\n"
                "   v3 [  0  0  0  1 ]\n"
                "   v4 [  0  0  0  0 ]\n"
                "No es simétrica: hay flecha v1→v3 pero no v3→v1.",
            "q_type": "tf",
            "question":
                "En un grafo no dirigido la matriz de adyacencia es\n"
                "siempre simétrica.",
            "options": ["Verdadero", "Falso"],
            "correct": 0,
            "explanation":
                "Verdadero. Como las aristas son conjuntos {v, v'}\n"
                "sin orden, A(i,j) = A(j,i) para todo i, j.",
        },
        {
            "title": "Grado de un vértice y Euler",
            "nivel": "intermedio",
            "theory":
                "Sea G un grafo y v ∈ V. El GRADO de v, g(v),\n"
                "es el número de aristas incidentes a v.\n\n"
                "Propiedades útiles:\n"
                "  • Lema del apretón de manos:\n"
                "       Σ g(v) = 2·|E|\n"
                "    Suma de grados = doble del nº de aristas.\n"
                "  • El número de vértices de grado IMPAR es par.\n\n"
                "Teorema (caminos/ciclos eulerianos):\n"
                "  • G tiene un CAMINO euleriano ⇔ tiene exactamente\n"
                "    2 vértices de grado impar.\n"
                "  • G tiene un CICLO euleriano  ⇔ todos los\n"
                "    vértices tienen grado par.",
            "example":
                "Grafo con V={1,2,3,4,5} y aristas\n"
                "{1,2},{1,3},{2,3},{3,4},{3,5}.\n"
                "Grados:\n"
                "  g(1)=2,  g(2)=2,  g(3)=4,  g(4)=1,  g(5)=1.\n"
                "Suma = 10 = 2·5 = 2·|E|.  ✓\n"
                "Hay 2 vértices de grado impar (4 y 5),\n"
                "por tanto existe un camino euleriano (resaltado abajo).",
            "visual": {
                "tipo": "grafo",
                "nodes": [
                    {"id": "1", "pos": (80, 50),  "label": "1"},
                    {"id": "2", "pos": (220, 50), "label": "2"},
                    {"id": "3", "pos": (150, 130), "label": "3"},
                    {"id": "4", "pos": (60, 200),  "label": "4"},
                    {"id": "5", "pos": (240, 200), "label": "5"},
                ],
                "edges": [
                    {"from": "1", "to": "2"},
                    {"from": "1", "to": "3"},
                    {"from": "2", "to": "3"},
                    {"from": "3", "to": "4"},
                    {"from": "3", "to": "5"},
                ],
                "highlight_path": ["4", "3", "2", "1", "3", "5"],
            },
            "q_type": "mc",
            "question":
                "En un grafo con grados g(1)=3, g(2)=3, g(3)=4,\n"
                "g(4)=3, g(5)=3, ¿qué se puede afirmar?",
            "options": [
                "Tiene un ciclo euleriano.",
                "Tiene un camino euleriano pero no un ciclo.",
                "No tiene ni camino ni ciclo euleriano.",
                "Tiene exactamente 2 aristas.",
            ],
            "correct": 2,
            "explanation":
                "Hay 4 vértices de grado impar, no 0 ni 2, así que\n"
                "no se cumple ninguna de las dos condiciones.",
        },
        {
            "title": "Caminos y conexión",
            "nivel": "intermedio",
            "theory":
                "Un CAMINO C entre v1 y vn en un grafo G es una\n"
                "sucesión de aristas {v1,v2}, {v2,v3}, …, {vn-1,vn}\n"
                "que conecta v1 con vn.\n\n"
                "Clasificación de caminos:\n"
                "  • Longitud = número de aristas recorridas.\n"
                "  • Cerrado: v1 = vn. Abierto: en otro caso.\n"
                "  • Simple: no repite vértices.\n"
                "  • Ciclo: simple y cerrado.\n\n"
                "CONEXIÓN: G es CONEXO si para cada par de vértices\n"
                "existe algún camino que los une.\n\n"
                "Un ÁRBOL es un grafo conexo y SIN ciclos.",
            "example":
                "Grafo G con aristas {1,2},{1,3},{1,4},{2,4},{3,4}:\n"
                "  • {2,4},{4,3}            longitud 2, abierto.\n"
                "  • {1,2},{2,4},{4,1}      longitud 3, ciclo.\n"
                "  • {2,4},{4,1},{4,3},{3,4},{4,2}\n"
                "                            longitud 5, no simple.",
            "q_type": "mc",
            "question":
                "Dado el grafo con V={1,2,3,4,5} y aristas\n"
                "{1,2},{1,3},{2,3},{4,5}, ¿es conexo?",
            "options": [
                "Sí, porque tiene 5 vértices.",
                "Sí, porque {2,3} y {4,5} comparten vértices.",
                "No, porque no hay camino de 3 a 4.",
                "Sí, porque tiene un ciclo {1,2,3}.",
            ],
            "correct": 2,
            "explanation":
                "El grafo se descompone en dos componentes: {1,2,3}\n"
                "y {4,5}. No existe camino entre 3 y 4.",
        },
        {
            "title": "Grafos y redes neuronales",
            "nivel": "experto",
            "theory":
                "Una red neuronal artificial se modela como un\n"
                "grafo DIRIGIDO y PONDERADO G = (V, E, ψ, p):\n"
                "  • V = neuronas (entrada, ocultas, salida).\n"
                "  • E = conexiones sinápticas (dirigidas).\n"
                "  • p: E → ℝ asigna a cada arista un peso wij.\n\n"
                "En una red feed-forward el grafo es ACÍCLICO\n"
                "(DAG): la información fluye sin ciclos.\n\n"
                "La matriz de adyacencia ponderada COINCIDE con la\n"
                "matriz de pesos W de la capa. Por eso el cálculo\n"
                "de una capa es a = σ(W·x + b).\n\n"
                "Una RNN introduce ciclos: el grafo deja de ser DAG.",
            "example":
                "Red 2-3-1 (2 entradas, 3 ocultas, 1 salida):\n"
                "  V = {x1, x2, h1, h2, h3, y},  |V| = 6.\n"
                "  E = 2·3 + 3·1 = 9 aristas dirigidas.\n"
                "Matriz de pesos W¹ (3×2) entre entrada y oculta;\n"
                "W² (1×3) entre oculta y salida.\n"
                "Grado de h1 = fan-in(2) + fan-out(1) = 3.",
            "q_type": "mc",
            "question":
                "¿Qué tipo de grafo modeliza mejor una red neuronal\n"
                "feed-forward clásica (MLP)?",
            "options": [
                "Grafo no dirigido con ciclos.",
                "Grafo dirigido acíclico (DAG) y ponderado.",
                "Árbol no dirigido.",
                "Grafo dirigido fuertemente conexo.",
            ],
            "correct": 1,
            "explanation":
                "Un MLP es dirigido, acíclico y ponderado. Por\n"
                "tanto, es un DAG ponderado.",
        },
        {
            "title": "🎬 Grafo conexo (Sesión 4)",
            "nivel": "básico",
            "theory":
                "Un GRAFO es un conjunto de VÉRTICES (puntos) unidos por "
                "ARISTAS (líneas).\n\n"
                "Un grafo es CONEXO si, partiendo de cualquier vértice, "
                "puedes llegar a cualquier otro siguiendo aristas.\n\n"
                "Tomemos G con vértices 1,2,3,4,5 y aristas:\n"
                "   {1,2}, {1,3}, {2,3}, {3,4}, {3,5}, {4,5}\n\n"
                "Desde el vértice 1 alcanzo 2 y 3; desde 3 alcanzo 4 y 5. "
                "Luego desde CUALQUIER vértice llego a todos los demás.\n\n"
                "💡 Si existe un camino entre cada par de vértices, el grafo "
                "es conexo (una sola pieza).",
            "example":
                "Camino de 1 a 5:  1 — 3 — 5.  Tambien 1 — 3 — 4 — 5.\n"
                "Hay mas de un camino: senal clara de que esta todo conectado.\n\n"
                "▶ Pulsa «Animar»: un recorrido 1→2→3→4→5 visita TODOS los\n"
                "vertices siguiendo aristas reales. Si el recorrido alcanza\n"
                "a todos, el grafo es conexo (una sola pieza).",
            "q_type": "mc",
            "question": "¿Es G conexo?",
            "options": [
                "Si: desde cualquier vertice se llega a todos los demas",
                "No: el vertice 5 queda aislado",
                "No: forma dos piezas separadas",
                "No se puede saber sin la matriz",
            ],
            "correct": 0,
            "explanation":
                "Es conexo. El vertice 3 actua de puente: conecta el grupo "
                "1-2-3 con 4 y 5. Existe un camino entre todo par de "
                "vertices, por ejemplo 1-3-5, asi que G es una sola pieza.",
            "visual": {
                "tipo": "grafo",
                "title": "G conexo (5 vertices)",
                "nodes": [
                    {"id": "1", "pos": (110, 40),  "label": "1"},
                    {"id": "2", "pos": (40, 130),  "label": "2"},
                    {"id": "3", "pos": (220, 110), "label": "3"},
                    {"id": "4", "pos": (330, 50),  "label": "4"},
                    {"id": "5", "pos": (360, 160), "label": "5"},
                ],
                "edges": [
                    {"from": "1", "to": "2", "dir": False},
                    {"from": "1", "to": "3", "dir": False},
                    {"from": "2", "to": "3", "dir": False},
                    {"from": "3", "to": "4", "dir": False},
                    {"from": "3", "to": "5", "dir": False},
                    {"from": "4", "to": "5", "dir": False},
                ],
                "highlight_path": ["1", "3", "5"],
                "animate": {"tipo": "recorrido",
                            "secuencia": ["1", "2", "3", "4", "5"]},
            },
        },
        {
            "title": "🎬 Grafo no conexo (Sesión 4)",
            "nivel": "básico",
            "theory":
                "Un grafo NO es conexo cuando se parte en varios trozos "
                "separados. Cada trozo se llama COMPONENTE CONEXA.\n\n"
                "Tomemos H con vertices 1,2,3,4,5 y aristas:\n"
                "   {1,2}, {1,3}, {2,3}, {4,5}\n\n"
                "Los vertices 1, 2 y 3 estan unidos entre si: forman una "
                "componente. Los vertices 4 y 5 estan unidos solo entre "
                "ellos: forman OTRA componente.\n\n"
                "No hay ninguna arista que cruce de un grupo al otro, asi "
                "que desde 1 NUNCA llegas a 5.\n\n"
                "💡 Numero de componentes = numero de piezas separadas.",
            "example":
                "Componente A:  {1, 2, 3}  (triangulo).\n"
                "Componente B:  {4, 5}  (una sola arista).\n"
                "Como hay 2 piezas sin conexion, H NO es conexo.",
            "q_type": "mc",
            "question": "¿Cuantas componentes conexas tiene H?",
            "options": [
                "1",
                "2",
                "3",
                "5",
            ],
            "correct": 1,
            "explanation":
                "Tiene 2 componentes: {1,2,3} y {4,5}. Ninguna arista las "
                "une, por eso el grafo esta partido en dos trozos y no es "
                "conexo.",
            "visual": {
                "tipo": "grafo",
                "title": "H con 2 componentes",
                "nodes": [
                    {"id": "1", "pos": (90, 40),   "label": "1"},
                    {"id": "2", "pos": (40, 150),  "label": "2"},
                    {"id": "3", "pos": (160, 150), "label": "3"},
                    {"id": "4", "pos": (320, 60),  "label": "4"},
                    {"id": "5", "pos": (370, 160), "label": "5"},
                ],
                "edges": [
                    {"from": "1", "to": "2", "dir": False},
                    {"from": "1", "to": "3", "dir": False},
                    {"from": "2", "to": "3", "dir": False},
                    {"from": "4", "to": "5", "dir": False},
                ],
            },
        },
        {
            "title": "🎬 Grafo dirigido (Sesión 4)",
            "nivel": "intermedio",
            "theory":
                "En un GRAFO DIRIGIDO cada arista tiene un SENTIDO: va de "
                "un vertice ORIGEN a un vertice DESTINO, como una calle de "
                "sentido unico.\n\n"
                "La funcion gamma asigna a cada arista un PAR ORDENADO "
                "(origen, destino):\n"
                "   gamma(e1) = (v1, v2)\n"
                "   gamma(e2) = (v1, v3)\n"
                "   gamma(e3) = (v2, v3)\n"
                "   gamma(e4) = (v3, v4)\n\n"
                "Que sea ORDENADO importa: (v1, v2) significa de v1 hacia "
                "v2, y NO de v2 hacia v1.\n\n"
                "💡 La flecha apunta siempre al destino.",
            "example":
                "La arista e3 = (v2, v3) se dibuja como flecha v2 → v3.\n"
                "Puedo ir de v2 a v3, pero no de v3 a v2 por esa arista.\n\n"
                "▶ Pulsa «Animar»: el recorrido v1→v2→v3→v4 sigue las\n"
                "flechas en su sentido valido, paso a paso.",
            "q_type": "mc",
            "question": "Segun gamma(e3) = (v2, v3), ¿que afirmacion es correcta?",
            "options": [
                "La arista va de v2 a v3 (origen v2, destino v3)",
                "La arista va de v3 a v2",
                "La arista une v2 y v3 sin sentido definido",
                "v2 y v3 no estan conectados",
            ],
            "correct": 0,
            "explanation":
                "Como es un par ORDENADO (v2, v3), el origen es v2 y el "
                "destino es v3: la flecha apunta v2 → v3. El orden del par "
                "fija el sentido de la arista.",
            "visual": {
                "tipo": "grafo",
                "title": "Grafo dirigido (4 vertices)",
                "nodes": [
                    {"id": "v1", "pos": (70, 40),   "label": "v1"},
                    {"id": "v2", "pos": (70, 170),  "label": "v2"},
                    {"id": "v3", "pos": (250, 110), "label": "v3"},
                    {"id": "v4", "pos": (400, 110), "label": "v4"},
                ],
                "edges": [
                    {"from": "v1", "to": "v2", "dir": True, "label": "e1"},
                    {"from": "v1", "to": "v3", "dir": True, "label": "e2"},
                    {"from": "v2", "to": "v3", "dir": True, "label": "e3"},
                    {"from": "v3", "to": "v4", "dir": True, "label": "e4"},
                ],
                "animate": {"tipo": "recorrido",
                            "secuencia": ["v1", "v2", "v3", "v4"]},
            },
        },
        {
            "title": "🎬 Matriz de adyacencia de un grafo (Sesión 5)",
            "nivel": "intermedio",
            "theory":
                "La MATRIZ DE ADYACENCIA A traduce un grafo a numeros. "
                "Para un grafo de n vertices es n x n:\n"
                "   A[i][j] = 1  si hay arista entre i y j\n"
                "   A[i][j] = 0  si no la hay\n\n"
                "Grafo G (no dirigido) con vertices 1,2,3,4 y aristas:\n"
                "   {1,2}, {1,3}, {2,3}, {3,4}\n\n"
                "Construimos A leyendo fila por fila:\n"
                "   fila 1:  0 1 1 0   (1 toca a 2 y 3)\n"
                "   fila 2:  1 0 1 0   (2 toca a 1 y 3)\n"
                "   fila 3:  1 1 0 1   (3 toca a 1, 2 y 4)\n"
                "   fila 4:  0 0 1 0   (4 toca a 3)\n\n"
                "💡 En un grafo no dirigido, si i toca a j entonces j toca "
                "a i: por eso A es SIMETRICA (A[i][j] = A[j][i]).",
            "example":
                "Mira la celda (1,2)=1 y la celda (2,1)=1: son iguales.\n"
                "El reflejo respecto a la diagonal es identico, porque la "
                "arista {1,2} no tiene sentido: une 1 con 2 en ambos lados.",
            "q_type": "mc",
            "question": "A es simetrica porque el grafo es...",
            "options": [
                "no dirigido",
                "dirigido",
                "conexo",
                "completo",
            ],
            "correct": 0,
            "explanation":
                "Como G es NO DIRIGIDO, cada arista {i,j} cuenta en los dos "
                "sentidos, asi que A[i][j] = A[j][i] y la matriz queda "
                "simetrica respecto a la diagonal principal.",
            "visual": {
                "tipo": "matriz",
                "label": "A",
                "title": "A 4x4 (adyacencia de G)",
                "matrix": [[0, 1, 1, 0],
                           [1, 0, 1, 0],
                           [1, 1, 0, 1],
                           [0, 0, 1, 0]],
                "highlight_cells": [(0, 1), (1, 0)],
                "highlight_rows": [],
                "highlight_cols": [],
            },
        },
    ],

    # =================================================================
    "2.1  Teoría de conjuntos": [
        {
            "title": "Conjuntos: definición y pertenencia",
            "nivel": "básico",
            "theory":
                "Un conjunto es una colección de objetos llamados\n"
                "elementos. Se escribe entre llaves separando los\n"
                "elementos por comas, p. ej. A = {1, 2, 3}.\n"
                "Si x está en A escribimos x ∈ A; si no, x ∉ A.\n"
                "Reglas básicas:\n"
                "  • Los elementos no se repiten.\n"
                "  • El orden no importa.\n"
                "  • El conjunto sin elementos es el vacío ∅.\n"
                "El cardinal |A| es el número de elementos de A.",
            "example":
                "Sea A = {2, 3, 5, 7, 11} (primos menores que 12).\n"
                "Entonces:\n"
                "  • 3 ∈ A  (3 está en A).\n"
                "  • 4 ∉ A  (4 no está en A).\n"
                "  • |A| = 5.",
            "q_type": "mc",
            "question": "Sea B = {a, b, c, d}. ¿Cuál afirmación es correcta?",
            "options": [
                "b ∉ B y |B| = 4",
                "b ∈ B y |B| = 4",
                "b ∈ B y |B| = 3",
                "{a, b} ∈ B y |B| = 2",
            ],
            "correct": 1,
            "explanation":
                "b está listado en B, luego b ∈ B. El conjunto tiene\n"
                "4 elementos distintos.",
        },
        {
            "title": "Inclusión y subconjuntos (⊆, ⊊)",
            "nivel": "básico",
            "theory":
                "A es subconjunto de B, A ⊆ B, si todo elemento de\n"
                "A pertenece a B:  ∀x (x ∈ A → x ∈ B).\n"
                "Si A ⊆ B y A ≠ B: subconjunto propio, A ⊊ B.\n"
                "Casos especiales:\n"
                "  • ∅ ⊆ A para todo A.\n"
                "  • A ⊆ A.\n"
                "No confundir ∈ con ⊆: ∈ relaciona elemento-conjunto,\n"
                "⊆ relaciona conjunto-conjunto.",
            "example":
                "Sea A = {1, 2} y B = {1, 2, 3, 4}.\n"
                "  • A ⊆ B porque 1 ∈ B y 2 ∈ B.\n"
                "  • A ⊊ B (es propio, porque 3 ∈ B pero 3 ∉ A).\n"
                "  • {1} ⊆ A, pero 1 ∈ A (no 1 ⊆ A).",
            "q_type": "tf",
            "question": "¿Es cierto que ∅ ⊆ {7, 8, 9}?",
            "options": ["Verdadero", "Falso"],
            "correct": 0,
            "explanation":
                "El conjunto vacío es subconjunto de cualquier conjunto.",
        },
        {
            "title": "Unión, intersección y diferencia",
            "nivel": "intermedio",
            "theory":
                "Sean A, B conjuntos:\n"
                "  • Unión:        A ∪ B = {x / x ∈ A ∨ x ∈ B}.\n"
                "  • Intersección: A ∩ B = {x / x ∈ A ∧ x ∈ B}.\n"
                "  • Diferencia:   B \\ A = {x / x ∈ B ∧ x ∉ A}.\n"
                "  • Complemento:  Aᶜ = X \\ A, con X el total.\n"
                "Si A ∩ B = ∅: disjuntos.\n"
                "Propiedades: conmutativa, asociativa, distributiva.",
            "example":
                "Sean A = {1, 2, 3, 4} y B = {3, 4, 5, 6}.\n"
                "  • A ∪ B = {1, 2, 3, 4, 5, 6}.\n"
                "  • A ∩ B = {3, 4}.\n"
                "  • A \\ B = {1, 2}.\n"
                "El diagrama de Venn de abajo lo ilustra: en el centro\n"
                "(intersección) están 3 y 4; a la izquierda 1, 2 (solo A);\n"
                "a la derecha 5, 6 (solo B).",
            "visual": {
                "tipo": "venn",
                "sets": [
                    {"label": "A", "pos": (130, 130), "r": 70,
                     "color": "#f85149"},
                    {"label": "B", "pos": (240, 130), "r": 70,
                     "color": "#39c5cf"},
                ],
                "elements": [
                    {"label": "1", "pos": (95, 110)},
                    {"label": "2", "pos": (95, 150)},
                    {"label": "3", "pos": (185, 110)},
                    {"label": "4", "pos": (185, 150)},
                    {"label": "5", "pos": (270, 110)},
                    {"label": "6", "pos": (270, 150)},
                ],
            },
            "q_type": "mc",
            "question":
                "Si A = {2, 4, 6, 8} y B = {1, 2, 3, 4}, ¿cuál es A ∩ B?",
            "options": [
                "{1, 2, 3, 4, 6, 8}",
                "{2, 4}",
                "{6, 8}",
                "∅",
            ],
            "correct": 1,
            "explanation":
                "Los elementos comunes a A y B son 2 y 4.",
        },
        {
            "title": "Leyes de De Morgan en conjuntos",
            "nivel": "experto",
            "theory":
                "Sea X total y A, B ⊆ X. Las leyes de De Morgan:\n"
                "  (1) (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ.\n"
                "  (2) (A ∩ B)ᶜ = Aᶜ ∪ Bᶜ.\n"
                "Intuición: negar 'en A o en B' equivale a 'no en A\n"
                "y no en B'. Generalización a familias finitas.",
            "example":
                "Sea X = {1..8}, A = {1, 2, 3, 4}, B = {3, 4, 5, 6}.\n"
                "  • A ∪ B = {1..6};  (A∪B)ᶜ = {7, 8}.\n"
                "  • Aᶜ = {5,6,7,8};  Bᶜ = {1,2,7,8}.\n"
                "  • Aᶜ ∩ Bᶜ = {7, 8}.  Coincide con (A∪B)ᶜ. ✓",
            "q_type": "mc",
            "question":
                "Según De Morgan, (A ∩ B)ᶜ es igual a:",
            "options": [
                "Aᶜ ∩ Bᶜ",
                "A ∪ B",
                "Aᶜ ∪ Bᶜ",
                "(A ∪ B)ᶜ",
            ],
            "correct": 2,
            "explanation":
                "La segunda ley dice (A ∩ B)ᶜ = Aᶜ ∪ Bᶜ.",
        },
        {
            "title": "Partes P(A) y cardinalidad 2ⁿ",
            "nivel": "intermedio",
            "theory":
                "El conjunto de las partes de A es:\n"
                "    P(A) = {B / B ⊆ A}.\n"
                "Siempre ∅ ∈ P(A) y A ∈ P(A).\n"
                "Teorema: si |A| = n, entonces |P(A)| = 2ⁿ.\n"
                "Razón: cada elemento puede 'entrar' o 'no entrar'\n"
                "(2 opciones), así 2ⁿ posibilidades.",
            "example":
                "Sea A = {1, 2, 3}. Subconjuntos:\n"
                "  • Cardinal 0: ∅.\n"
                "  • Cardinal 1: {1}, {2}, {3}.\n"
                "  • Cardinal 2: {1,2}, {1,3}, {2,3}.\n"
                "  • Cardinal 3: {1, 2, 3}.\n"
                "Total: 8 = 2³. ✓\n\n"
                "Caso 2: A = {a, b, c, d} (4 elementos):\n"
                "  |P(A)| = 2⁴ = 16 subconjuntos.\n"
                "Lo verifica el binomio:\n"
                "  C(4,0)+C(4,1)+C(4,2)+C(4,3)+C(4,4)\n"
                "  = 1 + 4 + 6 + 4 + 1 = 16.\n\n"
                "Caso 3: ¿Por qué 2ⁿ? Cada elemento puede ENTRAR (1) o\n"
                "NO ENTRAR (0) en el subconjunto. Son n bits independientes\n"
                "→ 2ⁿ combinaciones posibles (idea de la lógica binaria).",
            "q_type": "mc",
            "question":
                "Si |A| = 5, ¿cuántos elementos tiene P(A)?",
            "options": ["10", "25", "32", "120"],
            "correct": 2,
            "explanation":
                "|P(A)| = 2ⁿ con n=5 → 2⁵ = 32 subconjuntos.\n"
                "Las otras opciones corresponden a confusiones comunes:\n"
                "  10 = 2·5 (suma vs potencia),\n"
                "  25 = 5² (orden equivocado: nⁿ⁻¹ es trampa),\n"
                "  120 = 5! (factorial es para permutaciones).",
        },
        {
            "title": "🎬 Union, interseccion y diferencia con Venn (Sesión 3)",
            "nivel": "básico",
            "theory":
                "Un CONJUNTO es una coleccion de elementos. Con dos "
                "conjuntos A y B definimos:\n\n"
                "• UNION  A union B: todo lo que esta en A o en B.\n"
                "• INTERSECCION  A inter B: lo que esta en A Y a la vez en B.\n"
                "• DIFERENCIA  A menos B: lo que esta en A pero NO en B.\n\n"
                "Tomemos:\n"
                "   A = {-1, 3, 5, 2, 6, 9}\n"
                "   B = {-1, 0, 4, 3, 7, 9, 10}\n\n"
                "Los elementos COMUNES (estan en ambos) son -1, 3 y 9: esa "
                "es la interseccion, la zona donde los dos circulos se "
                "solapan.\n\n"
                "💡 La interseccion vive siempre en el solapamiento central "
                "del diagrama de Venn.",
            "example":
                "Solo en A (izquierda):  5, 2, 6\n"
                "Solo en B (derecha):    0, 4, 7, 10\n"
                "En el centro (A y B):   -1, 3, 9",
            "q_type": "mc",
            "question": "¿Cual es A interseccion B?",
            "options": [
                "{-1, 3, 9}",
                "{5, 2, 6}",
                "{0, 4, 7, 10}",
                "{-1, 0, 2, 3, 4, 5, 6, 7, 9, 10}",
            ],
            "correct": 0,
            "explanation":
                "A inter B = {-1, 3, 9}: son los unicos elementos que "
                "aparecen en los dos conjuntos a la vez.\n"
                "Ademas:\n"
                "   A union B = {-1, 0, 2, 3, 4, 5, 6, 7, 9, 10}\n"
                "   A menos B = {5, 2, 6}  (lo de A que no esta en B)",
            "visual": {
                "tipo": "venn",
                "sets": [
                    {"label": "A", "pos": (170, 110), "r": 95, "color": "#ff7b72"},
                    {"label": "B", "pos": (290, 110), "r": 95, "color": "#79c0ff"},
                ],
                "elements": [
                    {"label": "5",  "pos": (110, 80),  "in": ["A"]},
                    {"label": "2",  "pos": (95, 130),  "in": ["A"]},
                    {"label": "6",  "pos": (130, 160), "in": ["A"]},
                    {"label": "-1", "pos": (230, 75),  "in": ["A", "B"]},
                    {"label": "3",  "pos": (230, 115), "in": ["A", "B"]},
                    {"label": "9",  "pos": (230, 155), "in": ["A", "B"]},
                    {"label": "0",  "pos": (345, 80),  "in": ["B"]},
                    {"label": "4",  "pos": (360, 120), "in": ["B"]},
                    {"label": "7",  "pos": (335, 155), "in": ["B"]},
                    {"label": "10", "pos": (375, 95),  "in": ["B"]},
                ],
            },
        },
    ],

    # =================================================================
    "2.2  Relaciones y aplicaciones": [
        {
            "title": "Producto cartesiano A × B",
            "nivel": "básico",
            "theory":
                "Un par ordenado (a, b) une dos elementos en orden:\n"
                "(a, b) ≠ (b, a) en general.\n"
                "    A × B = {(a, b) / a ∈ A ∧ b ∈ B}.\n"
                "Cardinalidad: |A × B| = |A| · |B|.\n"
                "Ej. canónico: ℝ × ℝ = ℝ² (plano real).",
            "example":
                "A = {1, 2, 3}, B = {c, d}:\n"
                "  A × B = {(1,c),(1,d),(2,c),(2,d),(3,c),(3,d)}.\n"
                "6 pares = 3·2.",
            "q_type": "mc",
            "question":
                "Si |A| = 4 y |B| = 7, ¿cuánto vale |A × B|?",
            "options": ["11", "14", "28", "47"],
            "correct": 2,
            "explanation":
                "|A × B| = |A| · |B| = 4 · 7 = 28.",
        },
        {
            "title": "Relación binaria entre conjuntos",
            "nivel": "básico",
            "theory":
                "Una relación R de A en B es cualquier subconjunto\n"
                "de A × B:\n"
                "    R ⊆ A × B,  (a, b) ∈ R ↔ aRb.\n"
                "Queda determinada por el subconjunto de pares.",
            "example":
                "A = {1..5}, B = {-2, 0, 1, -3}.\n"
                "aRb si a es par Y b es negativo.\n"
                "  R = {(2,-2),(2,-3),(4,-2),(4,-3)}.",
            "q_type": "tf",
            "question":
                "Toda relación de A en B es un subconjunto de A × B.",
            "options": ["Verdadero", "Falso"],
            "correct": 0,
            "explanation":
                "Por definición, una relación es subconjunto de A × B.",
        },
        {
            "title": "Relaciones de equivalencia",
            "nivel": "intermedio",
            "theory":
                "R en A es de equivalencia si:\n"
                "  1. Reflexiva:  ∀a ∈ A,  aRa.\n"
                "  2. Simétrica:  aRb → bRa.\n"
                "  3. Transitiva: aRb ∧ bRc → aRc.\n"
                "Particiona A en clases [a] = {b / aRb} disjuntas.",
            "example":
                "En ℤ: aRb si b - a es múltiplo de 3.\n"
                "Cumple las 3 propiedades. Hay 3 clases por restos:\n"
                "  [0] = {..., -3, 0, 3, 6, ...},\n"
                "  [1] = {..., -2, 1, 4, ...},\n"
                "  [2] = {..., -1, 2, 5, ...}.",
            "q_type": "mc",
            "question":
                "¿Cuál NO es propiedad de una relación de equivalencia?",
            "options": [
                "Reflexiva",
                "Simétrica",
                "Antisimétrica",
                "Transitiva",
            ],
            "correct": 2,
            "explanation":
                "Antisimétrica es propia de las relaciones de orden.",
        },
        {
            "title": "Aplicaciones (funciones) entre conjuntos",
            "nivel": "intermedio",
            "theory":
                "f: A → B es aplicación si a cada a ∈ A le corresponde\n"
                "UN ÚNICO b ∈ B: ∀a ∈ A, ∃! b ∈ B : f(a) = b.\n"
                "  • Dominio: Dom(f) = A.\n"
                "  • Imagen:  Im(f) = {f(a) / a ∈ A} ⊆ B.\n"
                "No es función si algún a no tiene imagen o tiene dos.",
            "example":
                "A = {1,2,3}, B = {1,3,5,8}.\n"
                "  • f(1)=3, f(2)=5, f(3)=3 → SÍ es aplicación.\n"
                "    Im(f) = {3, 5} ⊊ B.\n"
                "  • g(1)=1 y g(1)=3 → NO (1 tiene dos imágenes).",
            "q_type": "mc",
            "question":
                "Para que f: A → B sea aplicación, cada elemento de A debe…",
            "options": [
                "tener al menos un valor en B.",
                "tener exactamente un valor en B.",
                "tener valores distintos en B.",
                "estar relacionado con todo B.",
            ],
            "correct": 1,
            "explanation":
                "Exactamente una imagen (existencia y unicidad).",
        },
        {
            "title": "Inyectiva, suprayectiva y biyectiva",
            "nivel": "experto",
            "theory":
                "Sea f: A → B.\n"
                "  • Inyectiva: f(a) = f(b) → a = b.\n"
                "  • Suprayectiva: f(A) = B (∀b ∈ B, ∃a con f(a)=b).\n"
                "  • Biyectiva: inyectiva Y suprayectiva.\n"
                "Para finitos:\n"
                "  • Inyectiva ⇒ |A| ≤ |B|.\n"
                "  • Sobre     ⇒ |A| ≥ |B|.\n"
                "  • Biyectiva ⇒ |A| = |B|.\n"
                "Toda biyección tiene inversa f⁻¹: B → A.",
            "example":
                "A = {x,y,z}, B = {-1,0,1}, f(x)=0, f(y)=-1, f(z)=1.\n"
                "Inyectiva ✓ y sobre ✓ → biyectiva.\n"
                "Inversa: f⁻¹(0)=x, f⁻¹(-1)=y, f⁻¹(1)=z.",
            "q_type": "mc",
            "question":
                "Si f: A → B es biyectiva y A, B son finitos:",
            "options": [
                "|A| < |B|",
                "|A| > |B|",
                "|A| = |B|",
                "|A| y |B| no se relacionan",
            ],
            "correct": 2,
            "explanation":
                "Biyectiva obliga a |A| ≤ |B| y |A| ≥ |B|, luego son iguales.",
        },
    ],

    # =================================================================
    "2.3  Combinatoria": [
        {
            "title": "Principio de adición",
            "nivel": "básico",
            "theory":
                "Si A y B son finitos y disjuntos (A ∩ B = ∅):\n"
                "    |A ∪ B| = |A| + |B|.\n"
                "Para n conjuntos disjuntos: se suman todos.\n"
                "Si NO son disjuntos: |A∪B| = |A|+|B|-|A∩B|.",
            "example":
                "34 aprobados + 15 suspensos = 49 alumnos.",
            "q_type": "mc",
            "question":
                "En una urna hay 12 bolas rojas y 8 azules. ¿Cuántas hay?",
            "options": ["4", "20", "96", "Depende"],
            "correct": 1,
            "explanation":
                "Conjuntos disjuntos: 12 + 8 = 20.",
        },
        {
            "title": "Principio de multiplicación",
            "nivel": "básico",
            "theory":
                "Si una elección se hace en pasos independientes,\n"
                "el total es el PRODUCTO de las opciones:\n"
                "    |A₁ × A₂ × … × Aₙ| = |A₁|·|A₂|·…·|Aₙ|.",
            "example":
                "Disco: {HDD, SSD}, S.O.: {Ubuntu, Debian, Fedora}.\n"
                "Configuraciones = 2 · 3 = 6.",
            "q_type": "mc",
            "question":
                "Un menú: 4 entrantes, 5 principales, 3 postres. "
                "¿Menús distintos?",
            "options": ["12", "20", "60", "120"],
            "correct": 2,
            "explanation":
                "Cada elección es INDEPENDIENTE (entrante × principal × postre),\n"
                "luego por el principio de multiplicación:\n"
                "  4 · 5 · 3 = 60 menús distintos.\n"
                "Errores típicos:\n"
                "  12 = 4+5+3 (SUMA, sería válido si fueran 'o' en vez de 'y'),\n"
                "  120 = 5! (factorial, no aplica aquí).",
        },
        {
            "title": "Permutaciones Pₙ = n!",
            "nivel": "intermedio",
            "theory":
                "Permutación de n elementos = ordenación de todos.\n"
                "    Pₙ = n! = n·(n-1)·…·2·1.\n"
                "Convenio: 0! = 1.\n"
                "Crecimiento muy rápido: 5! = 120, 10! ≈ 3.6 millones.",
            "example":
                "Ordenar {a,b,c,d}: 4! = 24 ordenaciones.\n"
                "Posición 1: 4 opciones; 2: 3; 3: 2; 4: 1.",
            "q_type": "mc",
            "question":
                "6 personas, 6 sillas en fila. ¿Formas?",
            "options": ["36", "120", "720", "46 656"],
            "correct": 2,
            "explanation":
                "Es una permutación de 6 elementos distintos:\n"
                "  P₆ = 6! = 6·5·4·3·2·1 = 720.\n"
                "Errores comunes:\n"
                "  36 = 6² (variaciones de 2 con repetición, no aplica),\n"
                "  120 = 5! (1 elemento de menos),\n"
                "  46 656 = 6⁶ (con repetición, pero las personas son únicas).",
        },
        {
            "title": "Variaciones V(n,k)",
            "nivel": "intermedio",
            "theory":
                "Elegir k entre n con orden, sin repetir:\n"
                "    V(n, k) = n!/(n-k)! = n·(n-1)·…·(n-k+1).\n"
                "Con repetición:  VR(n, k) = nᵏ.\n"
                "Variación: el orden SÍ importa.",
            "example":
                "Números 2 cifras distintas con {1,2,3,4}:\n"
                "  V(4,2) = 4!/2! = 12.\n"
                "  12,13,14,21,23,24,31,32,34,41,42,43.",
            "q_type": "mc",
            "question":
                "8 corredores, podio (oro/plata/bronce). ¿Formas?",
            "options": ["24", "56", "336", "512"],
            "correct": 2,
            "explanation":
                "V(8,3) = 8·7·6 = 336.",
        },
        {
            "title": "Combinaciones C(n,k) y póker",
            "nivel": "experto",
            "theory":
                "Elegir k entre n SIN orden:\n"
                "    C(n, k) = n! / [k!·(n-k)!]\n"
                "Propiedades: C(n,0)=C(n,n)=1; C(n,k)=C(n,n-k).\n"
                "Relación: V(n,k) = C(n,k)·k!",
            "example":
                "Manos de póker (5 cartas de 52):\n"
                "  C(52,5) = 2 598 960 manos.\n"
                "Lotería 6/49:  C(49,6) = 13 983 816.",
            "q_type": "mc",
            "question":
                "Comités de 3 personas de un grupo de 10:",
            "options": ["30", "120", "720", "1000"],
            "correct": 1,
            "explanation":
                "C(10,3) = 10·9·8 / (3·2·1) = 120.",
        },
        {
            "title": "🎬 Variaciones: con y sin repetición (Sesión 4)",
            "nivel": "intermedio",
            "theory":
                "Una VARIACION cuenta de cuantas formas podemos ordenar "
                "elementos cuando el ORDEN importa (12 es distinto de 21).\n\n"
                "SIN repeticion (no se repiten elementos):\n"
                "   V(n,k) = n! / (n-k)!\n\n"
                "CON repeticion (se pueden repetir):\n"
                "   VR(n,k) = n^k\n\n"
                "Ejemplo de la sesion: numeros de 2 cifras usando los "
                "digitos {1,2,3,4}.",
            "example":
                "SIN repeticion, V(4,2) = 4! / 2! = 24 / 2 = 12:\n"
                "   12 13 14 21 23 24 31 32 34 41 42 43\n"
                "   (se descartan 11, 22, 33, 44)\n\n"
                "CON repeticion, VR(4,2) = 4^2 = 16:\n"
                "   se añaden 11, 22, 33, 44 a los 12 anteriores.",
            "q_type": "mc",
            "question": "¿Cuántos números de 2 cifras se forman con {1,2,3,4} si NO se repiten cifras?",
            "options": [
                "12",
                "16",
                "8",
                "24",
            ],
            "correct": 0,
            "explanation":
                "Sin repeticion: V(4,2) = 4!/2! = 24/2 = 12.\n"
                "Si SI se permitiera repetir, serian VR(4,2) = 4^2 = 16 "
                "(los 12 anteriores mas 11, 22, 33, 44). El orden importa, "
                "por eso son variaciones y no combinaciones.",
            "visual": {
                "tipo": "matriz",
                "label": "V",
                "title": "Variaciones sin repeticion V(4,2)=12",
                "matrix": [[12, 13, 14], [21, 23, 24], [31, 32, 34]],
                "highlight_cells": [(0, 0)],
                "highlight_rows": [],
                "highlight_cols": [],
            },
        },
    ],

    # =================================================================
    "2.4  Espacios vectoriales": [
        {
            "title": "Definición y axiomas",
            "nivel": "básico",
            "theory":
                "Un espacio vectorial V sobre un cuerpo K (típicamente\n"
                "K = ℝ) es un conjunto con dos operaciones:\n"
                " • Suma:  + : V × V → V\n"
                " • Producto externo: · : K × V → V\n\n"
                "8 axiomas (∀u,v,w ∈ V; a,b ∈ K):\n"
                " 1) asociativa suma     2) conmutativa suma\n"
                " 3) neutro 0            4) opuesto -u\n"
                " 5) asociativa producto 6) neutro 1·u=u\n"
                " 7) distributiva a·(u+v) 8) distributiva (a+b)·u\n\n"
                "Ejemplo canónico: ℝⁿ con suma componente a componente.",
            "example":
                "V = ℝ², u = (2,-1), v = (3,4), a = 5.\n"
                "  u + v = (5, 3)\n"
                "  -u = (-2, 1)\n"
                "  a·u = (10, -5)\n"
                "  a·(u+v) = (25, 15) = a·u + a·v  ✓\n"
                "El diagrama muestra u, v y u+v en el plano.",
            "visual": {
                "tipo": "vectores2d",
                "xrange": (-3, 6),
                "yrange": (-3, 5),
                "vectores": [
                    {"v": (2, -1), "label": "u",   "color": "#39c5cf"},
                    {"v": (3,  4), "label": "v",   "color": "#3fb950"},
                    {"v": (5,  3), "label": "u+v", "color": "#f85149"},
                ],
                "animate": {"tipo": "vectores"},
            },
            "q_type": "mc",
            "question":
                "¿Cuál NO es axioma de espacio vectorial?",
            "options": [
                "Conmutatividad de la suma de vectores",
                "Existencia de elemento neutro para la suma",
                "Conmutatividad del producto de dos vectores",
                "Distributividad del producto respecto a la suma",
            ],
            "correct": 2,
            "explanation":
                "El producto entre dos vectores NO está definido como\n"
                "operación interna. Solo el producto escalar · : K × V → V.",
        },
        {
            "title": "Combinación lineal",
            "nivel": "básico",
            "theory":
                "Dados v₁,…,vₖ ∈ V y escalares a₁,…,aₖ ∈ K:\n"
                "    w = a₁·v₁ + … + aₖ·vₖ\n"
                "El conjunto de TODAS las combinaciones lineales es\n"
                "el subespacio generado ⟨v₁,…,vₖ⟩, siempre subespacio\n"
                "de V.\n\n"
                "En ℝ³: 1 vector → recta; 2 vectores no colineales →\n"
                "plano; 3 independientes → todo ℝ³.",
            "example":
                "v₁ = (1,2,0), v₂ = (0,1,-1).\n"
                "Combinación con a₁=3, a₂=-2:\n"
                "  w = 3·(1,2,0) + (-2)·(0,1,-1)\n"
                "    = (3,6,0) + (0,-2,2) = (3, 4, 2).",
            "q_type": "mc",
            "question":
                "Dados v₁=(1,0), v₂=(0,1), ¿qué combinación da (4,-3)?",
            "options": [
                "4·v₁ + 3·v₂",
                "4·v₁ - 3·v₂",
                "-4·v₁ + 3·v₂",
                "3·v₁ - 4·v₂",
            ],
            "correct": 1,
            "explanation":
                "4·(1,0) + (-3)·(0,1) = (4,-3). ✓",
        },
        {
            "title": "Dependencia e independencia lineal",
            "nivel": "intermedio",
            "theory":
                "v₁,…,vₖ son linealmente INDEPENDIENTES si:\n"
                "    a₁·v₁ + … + aₖ·vₖ = 0  ⇒  todos aᵢ = 0.\n"
                "En caso contrario son DEPENDIENTES (algún vᵢ es\n"
                "combinación del resto).\n\n"
                "Criterio práctico: matriz A con los vᵢ como columnas.\n"
                "  rank(A) = k → independientes.\n"
                "  rank(A) < k → dependientes.\n"
                "Para k vectores en ℝᵏ: det(A) ≠ 0.",
            "example":
                "v₁=(1,-1,2), v₂=(0,1,1):\n"
                "  a₁(1,-1,2) + a₂(0,1,1) = 0\n"
                "  ⇒ a₁=0, a₂=0  → independientes.\n\n"
                "v₁=(1,0,2), v₂=(-2,0,-4):  v₂ = -2·v₁ → dependientes.",
            "q_type": "tf",
            "question":
                "Tres vectores de ℝ² siempre son linealmente dependientes.",
            "options": ["Verdadero", "Falso"],
            "correct": 0,
            "explanation":
                "En un espacio de dim n, más de n vectores son siempre\n"
                "dependientes. Aquí n=2.",
            "simple_explanation":
                "IDEA SENCILLA:\n"
                "  Dependientes = uno SOBRA (se puede escribir con los otros).\n"
                "  Independientes = ninguno sobra.\n\n"
                "Test rápido en ℝ²:\n"
                "  • 1 vector solo (no nulo): siempre indep.\n"
                "  • 2 vectores: indep ↔ NO son uno múltiplo del otro\n"
                "    (no son paralelos).\n"
                "  • 3 o más en ℝ²: SIEMPRE dependientes (sobra al menos uno).\n\n"
                "Test rápido en ℝ³:\n"
                "  • 3 vectores: indep ↔ det de su matriz ≠ 0.\n"
                "  • 4 o más en ℝ³: SIEMPRE dependientes.\n\n"
                "Regla general:  k vectores en ℝⁿ son DEPENDIENTES si k > n.",
            "similar_examples": [
                "ℝ²:  v₁=(1,0), v₂=(2,0).\n"
                "  v₂ = 2·v₁ → dependientes.\n"
                "  Geometría: son COLINEALES (misma dirección).",

                "ℝ²:  v₁=(1,0), v₂=(0,1).\n"
                "  No hay escalar α con v₂=α·v₁ → independientes.\n"
                "  Geometría: ejes X e Y, NO paralelos.",

                "ℝ³:  v₁=(1,1,0), v₂=(0,1,1), v₃=(1,2,1).\n"
                "  Observa: v₃ = v₁ + v₂.\n"
                "  → dependientes (v₃ se 'fabrica' con los otros).",

                "ℝ²:  v₁=(1,0), v₂=(0,1), v₃=(2,3).\n"
                "  v₃ = 2·v₁ + 3·v₂ → dependientes (3 vec en ℝ²).\n"
                "  Cualquier 3er vector en ℝ² es comb. lineal de los dos primeros.",
            ],
        },
        {
            "title": "Sistemas generadores y bases",
            "nivel": "intermedio",
            "theory":
                "Sea V un espacio vectorial y S ⊆ V:\n"
                " • S es LIBRE si todos sus vectores son independientes.\n"
                " • S es GENERADOR si ⟨S⟩ = V.\n"
                " • S es BASE si es libre Y generador.\n\n"
                "Toda base de V (finito) tiene el mismo cardinal n.\n"
                "Base canónica de ℝⁿ: {e₁,…,eₙ} con eᵢ = (0,…,1,…,0).\n"
                "Coordenadas de v en base B: únicos αᵢ con v = Σαᵢ·bᵢ.",
            "example":
                "En ℝ², S = {(1,0), (0,1), (1,1)}:\n"
                "  Generador ✓ pero NO libre (1,1) = (1,0)+(0,1).\n"
                "  No es base.\n\n"
                "B = {(1,0), (0,1)}: libre y generador → base canónica.",
            "q_type": "mc",
            "question":
                "¿Cuál de estos conjuntos es base de ℝ³?",
            "options": [
                "{(1,0,0), (0,1,0)}",
                "{(1,1,0), (2,2,0), (0,0,1)}",
                "{(1,0,0), (0,1,0), (0,0,1), (1,1,1)}",
                "{(1,0,0), (1,1,0), (1,1,1)}",
            ],
            "correct": 3,
            "explanation":
                "La opción 1 (pocos) y 3 (demasiados) no son base.\n"
                "La 2: (2,2,0) = 2·(1,1,0), dependiente.\n"
                "La 4: tres vectores independientes en ℝ³ → base.",
        },
        {
            "title": "Dimensión y rango",
            "nivel": "intermedio",
            "theory":
                "Si V admite base finita B con |B| = n, dim(V) = n.\n"
                " • dim(ℝⁿ) = n.\n"
                " • Subespacio W ⊆ V: dim(W) ≤ dim(V).\n"
                " • W ⊆ V con dim(W) = dim(V) ⇒ W = V.\n\n"
                "Grassmann: dim(W₁+W₂) = dim(W₁)+dim(W₂)-dim(W₁∩W₂).\n"
                "Para A ∈ ℝᵐˣⁿ: dim(⟨col(A)⟩) = rank(A).",
            "example":
                "W = ⟨v₁,v₂,v₃⟩ con\n"
                "  v₁=(1,0,-1), v₂=(-1,-2,0), v₃=(1,4,-3).\n"
                "Matriz A por filas: det(A)=0 → rank<3.\n"
                "Menor 2x2: det([[1,0],[-1,-2]])=-2≠0 → rank=2.\n"
                "Por tanto dim(W) = 2 (un plano en ℝ³).",
            "q_type": "mc",
            "question":
                "A ∈ ℝ⁴ˣ⁵, rank(A)=3. ¿Dim del subespacio columna?",
            "options": ["2", "3", "4", "5"],
            "correct": 1,
            "explanation":
                "dim(⟨col(A)⟩) = rank(A) = 3.",
        },
        {
            "title": "Aplicaciones lineales y matriz asociada",
            "nivel": "experto",
            "theory":
                "f : U → V es LINEAL si:\n"
                "    f(a·u₁ + b·u₂) = a·f(u₁) + b·f(u₂).\n\n"
                "Teorema: toda f : ℝⁿ → ℝᵐ lineal tiene una matriz\n"
                "única A ∈ ℝᵐˣⁿ con f(v) = A·v. Las columnas de A\n"
                "son las imágenes de la base canónica:\n"
                "    columna i de A = f(eᵢ).\n\n"
                "ker(f) = {v / f(v)=0} (núcleo).\n"
                "im(f)  = imagen.\n"
                "Teorema rango–nulidad: dim(ker) + dim(im) = n.",
            "example":
                "f(x,y) = (3x-y, x+2y).\n"
                "  f(1,0) = (3, 1) → columna 1\n"
                "  f(0,1) = (-1, 2) → columna 2\n"
                "  A = [[3, -1],\n"
                "       [1,  2]]\n"
                "Verifica: A·(x,y)ᵀ = (3x-y, x+2y) = f(x,y). ✓",
            "q_type": "mc",
            "question":
                "f(x,y) = (3x-y, x+2y). ¿Matriz asociada en base canónica?",
            "options": [
                "[[3, 1], [-1, 2]]",
                "[[3, -1], [1, 2]]",
                "[[3, 1], [1, 2]]",
                "[[1, 3], [-1, 2]]",
            ],
            "correct": 1,
            "explanation":
                "Columnas = f(eᵢ): (3,1) y (-1,2).",
        },
        {
            "title": "🎬 Combinación lineal (animada) (Sesión 5)",
            "nivel": "básico",
            "theory":
                "Una COMBINACION LINEAL de los vectores v1 y v2 es "
                "a1·v1 + a2·v2, donde a1 y a2 son escalares (numeros).\n\n"
                "En clase el ejemplo era 3D con U=(1,3,-2) y V=(5,1,0), "
                "pero aqui lo ilustramos con un caso 2D equivalente para "
                "poder DIBUJARLO en el plano.\n\n"
                "Tomamos u=(2,1), v=(-1,2) y los escalares a=2, b=1.\n"
                "El resultado 2u+v es una combinacion lineal de u y v.\n\n"
                "💡 El conjunto de TODAS las combinaciones lineales de unos "
                "vectores se llama SPAN (lo que generan).",
            "example":
                "2u + v con u=(2,1), v=(-1,2):\n"
                "   primera componente: 2·2 + (-1) = 4 - 1 = 3\n"
                "   segunda componente: 2·1 + 2     = 2 + 2 = 4\n"
                "   2u + v = (3,4)\n\n"
                "Mira la animacion: primero u, luego v, y por ultimo el "
                "resultado 2u+v.",
            "q_type": "mc",
            "question": "¿Cuánto vale 2u+v con u=(2,1), v=(-1,2)?",
            "options": [
                "(3,4)",
                "(1,3)",
                "(4,3)",
                "(3,3)",
            ],
            "correct": 0,
            "explanation":
                "2u+v = (2·2+(-1), 2·1+2) = (3,4).\n"
                "En IA, una capa lineal calcula Wx: cada salida es una "
                "combinacion lineal de las entradas. Todo lo que una capa "
                "lineal puede producir vive dentro del span de las filas de W.",
            "visual": {
                "tipo": "vectores2d",
                "xrange": (-3, 6),
                "yrange": (-3, 5),
                "vectores": [
                    {"v": (2, 1), "label": "u", "color": "#39c5cf"},
                    {"v": (-1, 2), "label": "v", "color": "#3fb950"},
                    {"v": (3, 4), "label": "2u+v", "color": "#f85149"},
                ],
                "animate": {"tipo": "vectores"},
            },
            "visual3d": {
                "tipo": "vectores3d",
                "title": "Combinación lineal U + V en ℝ³ (vectores de clase)",
                "vectores": [
                    {"v": (1, 3, -2), "label": "U", "color": "#39c5cf"},
                    {"v": (5, 1, 0),  "label": "V", "color": "#3fb950"},
                ],
                "combinacion": {"v": (6, 4, -2), "label": "U+V",
                                "color": "#f85149"},
            },
        },
        {
            "title": "🎬 Producto escalar y ortogonalidad (Sesión 4)",
            "nivel": "básico",
            "theory":
                "El PRODUCTO ESCALAR de dos vectores es la suma de sus "
                "componentes multiplicadas una a una:\n"
                "   u·v = u1·v1 + u2·v2 + ...\n\n"
                "Propiedad clave: dos vectores son ORTOGONALES "
                "(perpendiculares) exactamente cuando su producto escalar "
                "vale 0:\n"
                "   u ⊥ v   ⟺   u·v = 0\n\n"
                "Esto sale de la formula u·v = ‖u‖·‖v‖·cos θ: si el angulo "
                "es de 90 grados, cos(90) = 0, asi que el producto escalar "
                "se anula.",
            "example":
                "Con u=(2,1) y v=(-1,2):\n"
                "   u·v = 2·(-1) + 1·2 = -2 + 2 = 0\n"
                "Como u·v = 0, los vectores son ortogonales: forman un "
                "angulo de 90 grados. Compruebalo en el dibujo.",
            "q_type": "mc",
            "question": "¿Cuánto vale u·v con u=(2,1), v=(-1,2), y qué significa?",
            "options": [
                "0; son ortogonales",
                "0; son paralelos",
                "5; son ortogonales",
                "-4; no significa nada",
            ],
            "correct": 0,
            "explanation":
                "u·v = 2·(-1) + 1·2 = 0, asi que u y v son ortogonales.\n"
                "Como u·v = ‖u‖·‖v‖·cos θ y cos(90)=0, el producto escalar 0 "
                "indica angulo recto. En IA el producto escalar mide la "
                "similitud (coseno) entre embeddings: 0 significa que no se "
                "parecen en absoluto.",
            "visual": {
                "tipo": "vectores2d",
                "xrange": (-3, 5),
                "yrange": (-3, 4),
                "vectores": [
                    {"v": (2, 1), "label": "u", "color": "#39c5cf"},
                    {"v": (-1, 2), "label": "v", "color": "#3fb950"},
                ],
                "animate": {"tipo": "vectores"},
            },
        },
        {
            "title": "🎬 Norma euclídea de un vector (Sesión 4)",
            "nivel": "básico",
            "theory":
                "La NORMA EUCLIDEA (o norma 2) de un vector mide su "
                "longitud. Se calcula con el teorema de Pitagoras:\n"
                "   ‖v‖2 = raiz( v1^2 + v2^2 + ... )\n\n"
                "Es la distancia desde el origen hasta la punta del vector.",
            "example":
                "Con v=(3,4):\n"
                "   ‖v‖ = raiz(3^2 + 4^2) = raiz(9 + 16) = raiz(25) = 5\n"
                "Es el clasico triangulo 3-4-5. El vector (3,4) mide 5 "
                "unidades de largo.",
            "q_type": "mc",
            "question": "¿Cuánto vale la norma euclídea de v=(3,4)?",
            "options": [
                "5",
                "7",
                "25",
                "12",
            ],
            "correct": 0,
            "explanation":
                "‖v‖ = raiz(3^2 + 4^2) = raiz(25) = 5.\n"
                "En IA las normas se usan para medir el tamaño de los pesos "
                "(regularizacion) y para normalizar embeddings antes de "
                "compararlos.",
            "visual": {
                "tipo": "vectores2d",
                "xrange": (-1, 5),
                "yrange": (-1, 5),
                "vectores": [
                    {"v": (3, 4), "label": "v", "color": "#f85149"},
                ],
            },
        },
    ],

    # =================================================================
    "2.5  Factorización de matrices": [
        {
            "title": "Valores y vectores propios",
            "nivel": "básico",
            "theory":
                "A ∈ ℝⁿˣⁿ. λ es VALOR PROPIO si ∃ v ≠ 0 con:\n"
                "    A·v = λ·v\n"
                "v es el VECTOR PROPIO asociado.\n\n"
                "Para hallarlos: det(A - λI) = 0 (polinomio característico).\n"
                "Sus raíces son los valores propios. Por cada λ, los\n"
                "vectores propios forman Vλ = ker(A - λI).",
            "example":
                "A = [[5,-3],[6,-4]].\n"
                "  det(A-λI) = (5-λ)(-4-λ)+18 = λ²-λ-2 = 0\n"
                "  λ₁=-1,  λ₂=2.\n"
                "Para λ₁=-1: (A+I)v=0 → 2x-y=0 → v₁=(1, 2).\n"
                "Para λ₂=2:  (A-2I)v=0 → x=y → v₂=(1, 1).\n"
                "Verifica: A·(1,2)=(-1,-2)=-1·(1,2). ✓",
            "visual": {
                "tipo": "matriz",
                "matrix": [[5, -3], [6, -4]],
                "label": "A",
                "title": "A 2×2 (autovalores λ=-1 y λ=2)",
            },
            "q_type": "mc",
            "question":
                "Si A es diagonal con entradas d₁,…,dₙ, sus valores propios son:",
            "options": [
                "Siempre 0 y 1",
                "Las raíces de un polinomio de grado 2",
                "Las propias entradas d₁,…,dₙ",
                "La suma y producto de la diagonal",
            ],
            "correct": 2,
            "explanation":
                "det(A-λI) = (d₁-λ)…(dₙ-λ) = 0 cuando λ = dᵢ.",
        },
        {
            "title": "Diagonalización",
            "nivel": "intermedio",
            "theory":
                "A es DIAGONALIZABLE si existe P invertible con:\n"
                "    P⁻¹·A·P = D   (D diagonal)\n"
                "Construcción: D contiene los λᵢ; P tiene los vectores\n"
                "propios como columnas.\n\n"
                "Criterio: multiplicidad algebraica = geométrica para\n"
                "cada λ. Si todos los λᵢ son distintos, es diagonalizable.\n\n"
                "Uso: Aᵏ = P·Dᵏ·P⁻¹ (potencia trivial en diagonal).",
            "example":
                "Continuando: A = [[5,-3],[6,-4]].\n"
                "  D = [[-1, 0],[0, 2]]\n"
                "  P = [[1, 1],[2, 1]],  P⁻¹ = [[-1, 1],[2, -1]]\n"
                "Comprobación: P⁻¹·A·P = D. ✓",
            "q_type": "tf",
            "question":
                "Si A ∈ ℝⁿˣⁿ tiene n valores propios distintos, A es diagonalizable.",
            "options": ["Verdadero", "Falso"],
            "correct": 0,
            "explanation":
                "Valores propios distintos ⇒ n vectores propios independientes\n"
                "⇒ P invertible ⇒ diagonalizable.",
        },
        {
            "title": "Factorización LU",
            "nivel": "intermedio",
            "theory":
                "A = L·U con:\n"
                " • L triangular inferior, diagonal = 1.\n"
                " • U triangular superior.\n\n"
                "Se obtiene por eliminación gaussiana SIN pivotaje.\n"
                "Uso clave: resolver A·x = b con dos sustituciones:\n"
                "  L·y = b (adelante), U·x = y (atrás). Cada una O(n²).\n"
                "Eficiente cuando se resuelve para muchos b distintos.",
            "example":
                "A = [[4,3],[6,3]].\n"
                "  m = 6/4 = 1.5; F2 ← F2 - 1.5·F1\n"
                "  nueva F2 = (0, -1.5)\n"
                "  U = [[4, 3],[0,-1.5]]\n"
                "  L = [[1, 0],[1.5, 1]]\n"
                "L·U = A ✓. det(A) = 4·(-1.5) = -6.",
            "q_type": "mc",
            "question":
                "¿Por qué es eficiente LU para resolver A·x = b?",
            "options": [
                "Convierte A en diagonal",
                "Resuelve con dos sustituciones triangulares O(n²)",
                "Da siempre una matriz ortogonal",
                "Calcula la inversa de A directamente",
            ],
            "correct": 1,
            "explanation":
                "Factorizar es O(n³) UNA vez; cada b nuevo se resuelve\n"
                "en O(n²) con sustitución triangular.",
        },
        {
            "title": "Factorización de Cholesky",
            "nivel": "intermedio",
            "theory":
                "Para S simétrica Y definida positiva (xᵀSx > 0):\n"
                "    S = L·Lᵀ\n"
                "L triangular inferior con diagonal positiva, única.\n\n"
                "Ventajas vs LU: la mitad de operaciones (~n³/3),\n"
                "estable sin pivotaje.\n\n"
                "En IA: mínimos cuadrados (AᵀA), procesos gaussianos,\n"
                "muestreo de normales multivariadas.",
            "example":
                "S = [[4, 2],[2, 5]] (simétrica, det>0).\n"
                "Buscamos L con L·Lᵀ = S:\n"
                "  l₁₁² = 4 → l₁₁ = 2\n"
                "  l₂₁·l₁₁ = 2 → l₂₁ = 1\n"
                "  l₂₁²+l₂₂² = 5 → l₂₂ = 2\n"
                "  L = [[2,0],[1,2]],  L·Lᵀ = S ✓",
            "q_type": "tf",
            "question":
                "Cholesky se aplica a cualquier matriz cuadrada invertible.",
            "options": ["Verdadero", "Falso"],
            "correct": 1,
            "explanation":
                "Exige simétrica Y definida positiva, no basta con invertible.",
        },
        {
            "title": "Factorización QR",
            "nivel": "experto",
            "theory":
                "A ∈ ℝᵐˣⁿ (m≥n, columnas independientes):\n"
                "    A = Q·R\n"
                " • Q ortogonal (QᵀQ = Iₙ), columnas ortonormales.\n"
                " • R triangular superior.\n\n"
                "Gram–Schmidt: ortogonalizar columnas paso a paso:\n"
                "  u₁ = a₁;  q₁ = u₁/‖u₁‖\n"
                "  uₖ = aₖ - Σⱼ<ₖ ⟨aₖ,qⱼ⟩·qⱼ;  qₖ = uₖ/‖uₖ‖\n\n"
                "Uso: mínimos cuadrados estables, algoritmo QR para autovalores.",
            "example":
                "A = [[1,1],[1,0],[0,1]] (columnas a₁=(1,1,0), a₂=(1,0,1)).\n"
                "  q₁ = (1/√2)(1,1,0)\n"
                "  ⟨a₂,q₁⟩ = 1/√2\n"
                "  u₂ = (1/2, -1/2, 1); ‖u₂‖ = √(3/2)\n"
                "  q₂ = (1/√6, -1/√6, 2/√6)\n"
                "Q tiene q₁, q₂ por columnas; R triangular superior 2×2.",
            "q_type": "mc",
            "question":
                "En A = Q·R, ¿qué propiedad cumple Q?",
            "options": [
                "Es triangular superior",
                "Es simétrica definida positiva",
                "Es ortogonal: QᵀQ = I",
                "Es la inversa de R",
            ],
            "correct": 2,
            "explanation":
                "Q tiene columnas ortonormales por Gram–Schmidt.",
        },
        {
            "title": "SVD y su uso en IA",
            "nivel": "experto",
            "theory":
                "Para CUALQUIER A ∈ ℝᵐˣⁿ:\n"
                "    A = U·Σ·Vᵀ\n"
                " • U, V ortogonales.\n"
                " • Σ diagonal con valores singulares σ₁≥σ₂≥…≥0.\n\n"
                "σᵢ = √(λᵢ de AᵀA).\n\n"
                "USOS CLAVE en IA:\n"
                " • PCA: columnas de V = componentes principales,\n"
                "   σᵢ² = varianza capturada.\n"
                " • Compresión: aproximar A con k mayores σᵢ.\n"
                " • Pseudoinversa A⁺ = V·Σ⁺·Uᵀ (mínimos cuadrados).\n"
                " • Sistemas recomendadores (factores latentes).\n"
                " • Reducción de ruido en embeddings.",
            "example":
                "A = [[3,0],[4,5]].\n"
                "  AᵀA = [[25,20],[20,25]]\n"
                "  det(AᵀA-λI) = (25-λ)²-400 = 0  → λ=45, 5.\n"
                "  σ₁ = √45 ≈ 6.708,  σ₂ = √5 ≈ 2.236.\n"
                "Aproximación rango 1 retiene 45/50 = 90% de la información.",
            "q_type": "mc",
            "question":
                "¿Por qué es clave la SVD en PCA?",
            "options": [
                "Invierte matrices no cuadradas sin error",
                "Los valores singulares cuantifican varianza en cada dirección",
                "Σ es siempre la identidad",
                "Convierte cualquier matriz en simétrica",
            ],
            "correct": 1,
            "explanation":
                "σᵢ² (escalado) = varianza de la i-ésima componente principal.",
        },
        {
            "title": "🎬 El producto de matrices NO conmuta (Sesión 5)",
            "nivel": "intermedio",
            "theory":
                "Con los numeros normales da igual el orden: 3·5 = 5·3. "
                "Con las MATRICES esto NO ocurre: en general A·B no es "
                "igual a B·A. Decimos que el producto de matrices no es "
                "conmutativo.\n\n"
                "Usamos las matrices de la sesion:\n"
                "   A = [[1,0],[-1,2]]\n"
                "   B = [[0,1],[-3,4]]\n\n"
                "Cada celda del producto se obtiene multiplicando una fila "
                "de la primera matriz por una columna de la segunda y "
                "sumando.",
            "example":
                "A·B (fila por columna):\n"
                "   (0,0): 1·0 + 0·(-3) = 0\n"
                "   (0,1): 1·1 + 0·4    = 1\n"
                "   (1,0): -1·0 + 2·(-3)= -6\n"
                "   (1,1): -1·1 + 2·4   = 7\n"
                "   A·B = [[0,1],[-6,7]]\n\n"
                "B·A:\n"
                "   B·A = [[-1,2],[-7,8]]\n\n"
                "Como [[0,1],[-6,7]] no es [[-1,2],[-7,8]], queda claro que "
                "A·B ≠ B·A.",
            "q_type": "mc",
            "question": "¿Es A·B = B·A en general para matrices?",
            "options": [
                "No; el producto de matrices no es conmutativo",
                "Sí; siempre da lo mismo",
                "Sí, pero solo si son cuadradas",
                "No se puede multiplicar matrices",
            ],
            "correct": 0,
            "explanation":
                "Con A=[[1,0],[-1,2]] y B=[[0,1],[-3,4]]:\n"
                "   A·B = [[0,1],[-6,7]]\n"
                "   B·A = [[-1,2],[-7,8]]\n"
                "Son distintas, asi que A·B ≠ B·A. Por eso en redes "
                "neuronales el ORDEN de las multiplicaciones de matrices "
                "(de las capas) importa y no se puede cambiar.",
            "visual": {
                "tipo": "matriz",
                "label": "A·B",
                "title": "Producto A·B = [[0,1],[-6,7]]",
                "matrix": [[0, 1], [-6, 7]],
                "highlight_cells": [(1, 0)],
                "highlight_rows": [],
                "highlight_cols": [],
            },
        },
        {
            "title": "🎬 Determinante 2x2 y regularidad (Sesión 5)",
            "nivel": "intermedio",
            "theory":
                "El DETERMINANTE de una matriz 2x2 se calcula asi:\n"
                "   det([[a,b],[c,d]]) = a·d - b·c\n\n"
                "Sirve para saber si una matriz es REGULAR (invertible):\n"
                "   A es regular  ⟺  det(A) ≠ 0  ⟺  rank(A) = n\n\n"
                "Si el determinante es 0, la matriz es singular: no tiene "
                "inversa y sus filas son linealmente dependientes.",
            "example":
                "Con A = [[1,2],[3,4]]:\n"
                "   det(A) = 1·4 - 2·3 = 4 - 6 = -2\n"
                "Como det(A) = -2 ≠ 0, la matriz A es regular: tiene "
                "inversa y su rango es 2.",
            "q_type": "mc",
            "question": "¿Cuánto vale det(A) con A=[[1,2],[3,4]] y es A invertible?",
            "options": [
                "-2; sí, es invertible",
                "0; no es invertible",
                "2; sí, es invertible",
                "-2; no es invertible",
            ],
            "correct": 0,
            "explanation":
                "det(A) = 1·4 - 2·3 = -2. Como es distinto de 0, A es "
                "regular y por tanto invertible (rank=2).\n"
                "En IA el determinante avisa si una transformacion lineal "
                "es reversible o si aplasta el espacio (det=0) perdiendo "
                "informacion.",
            "visual": {
                "tipo": "matriz",
                "label": "A",
                "title": "A = [[1,2],[3,4]], det = -2",
                "matrix": [[1, 2], [3, 4]],
                "highlight_cells": [(0, 0), (1, 1)],
                "highlight_rows": [],
                "highlight_cols": [],
            },
        },
    ],

    # =================================================================
    "2.6  Cálculo tensorial + TensorFlow": [
        {
            "title": "Concepto de tensor: rango y dimensión",
            "nivel": "básico",
            "theory":
                "Un TENSOR es generalización de vector/matriz.\n"
                "Caracterizado por:\n"
                " • RANGO r: nº de índices (grados de libertad).\n"
                " • DIMENSIÓN N: tamaño del espacio de cada índice.\n\n"
                "Clasificación:\n"
                " • Rango 0 → ESCALAR.\n"
                " • Rango 1 → VECTOR.\n"
                " • Rango 2 → MATRIZ.\n"
                " • Rango ≥ 3 → tensor general (p.ej. imagen RGB).\n\n"
                "Nº componentes total = Nᵣ.\n"
                "Convenio Einstein: índices repetidos suman.",
            "example":
                " • s = 7.3  → rango 0, 1 componente.\n"
                " • v = (2,-1,4) → rango 1, dim 3.\n"
                " • M = [[1,2,3],[4,5,6]] → rango 2, shape (2,3).\n"
                " • Imagen RGB 64×64 → rango 3, shape (64,64,3).",
            "q_type": "mc",
            "question":
                "Una imagen color de 28×28 píxeles con 3 canales (RGB) es tensor de:",
            "options": [
                "Rango 1 con 2352 componentes",
                "Rango 2 con shape (28, 28)",
                "Rango 3 con shape (28, 28, 3)",
                "Rango 4 con shape (1, 28, 28, 3)",
            ],
            "correct": 2,
            "explanation":
                "Tres índices: fila, columna y canal.",
        },
        {
            "title": "Tensores covariantes y contravariantes",
            "nivel": "experto",
            "theory":
                "Un tensor formal: aplicación multilineal\n"
                "T : V₁ × … × Vₙ → ℝ.\n\n"
                " • COVARIANTES: índices ABAJO (aᵢ). Transforman IGUAL\n"
                "   que la base. Ejemplo: gradiente.\n"
                " • CONTRAVARIANTES: índices ARRIBA (bʲ). Transforman\n"
                "   INVERSAMENTE a la base. Ejemplo: vector velocidad.\n\n"
                "Tensor tipo (r, s): r contravariantes + s covariantes.\n"
                "Combinación aᵢbⁱ con índice mudo es invariante (escalar).",
            "example":
                "Tensor mixto Tⱼⁱ = aᵢ·bʲ en ℝ²:\n"
                "  T₁¹ = a₁·b¹, T₂¹ = a₂·b¹,\n"
                "  T₁² = a₁·b², T₂² = a₂·b².\n"
                "Bajo cambio de base P:\n"
                "  contravariante → con P⁻¹\n"
                "  covariante → con Pᵀ",
            "q_type": "mc",
            "question":
                "¿Qué representa un superíndice frente a un subíndice?",
            "options": [
                "Potencia vs derivada",
                "Componente contravariante vs covariante",
                "Solo cambia la posición visual",
                "Fila vs columna",
            ],
            "correct": 1,
            "explanation":
                "Convención clásica: superíndices contravariantes,\n"
                "subíndices covariantes.",
        },
        {
            "title": "Introducción a TensorFlow",
            "nivel": "básico",
            "theory":
                "TensorFlow: plataforma open source para ML de Google.\n"
                "Estructura básica: tensores n-dimensionales.\n\n"
                "Primitivas:\n"
                " • tf.constant(valor, dtype): tensor INMUTABLE.\n"
                " • tf.Variable(valor, dtype): tensor MUTABLE con estado.\n"
                "   Soporta .assign() — base de los pesos entrenables.\n\n"
                "Atributos: shape, dtype, rank.",
            "example":
                "f(x) = 2x + 1, datos:\n"
                "  x = tf.constant([0,1,2,3,4], shape=(5,1), tf.float32)\n"
                "  y = tf.constant([1,3,5,7,9], shape=(5,1), tf.float32)\n\n"
                "Pesos entrenables:\n"
                "  w = tf.Variable(0.0)\n"
                "  b = tf.Variable(0.0)\n"
                "  w.assign(w - lr*grad_w)",
            "q_type": "mc",
            "question":
                "Diferencia clave entre tf.constant y tf.Variable:",
            "options": [
                "tf.constant es int, tf.Variable es float",
                "tf.constant es inmutable; tf.Variable es mutable y entrenable",
                "tf.Variable es más rápida pero sin GPU",
                "Son alias el uno del otro",
            ],
            "correct": 1,
            "explanation":
                "tf.Variable mantiene estado mutable para entrenamiento.",
        },
        {
            "title": "Operaciones tensoriales y broadcasting",
            "nivel": "intermedio",
            "theory":
                "Operaciones elementales:\n"
                " • Suma: A + B (elemento a elemento).\n"
                " • Producto Hadamard: A * B.\n"
                " • Producto matricial: A @ B (tf.matmul).\n"
                " • Reducciones: tf.reduce_sum, tf.reduce_mean (axis).\n\n"
                "BROADCASTING: operar shapes distintas. Reglas:\n"
                " 1) Shapes se alinean por la DERECHA.\n"
                " 2) Cada dim igual O alguna vale 1 (se replica).\n"
                " 3) Si shape más corta: se rellena con 1s a la izquierda.",
            "example":
                "A shape (2,3), v shape (3,):\n"
                "  A = [[1,2,3],[4,5,6]],  v = [10,20,30].\n"
                "  A + v = [[11,22,33],[14,25,36]].  (v se replica)\n"
                "  A * v = [[10,40,90],[40,100,180]].\n\n"
                "A @ B con B (3,2) = [[1,0],[0,1],[1,1]]:\n"
                "  A @ B = [[4, 5],[10, 11]]  (2×2).\n"
                "tf.reduce_sum(A, axis=0) = [5, 7, 9].",
            "q_type": "tf",
            "question":
                "A shape (3,4) y v shape (4,): A + v es válido por broadcasting.",
            "options": ["Verdadero", "Falso"],
            "correct": 0,
            "explanation":
                "Alineadas por derecha: (3,4) y (_,4). Dim 4 coincide,\n"
                "v se replica en las 3 filas.",
        },
    ],

    # =================================================================
    "3.1  Cálculo infinitesimal": [
        {
            "title": "Límite y continuidad",
            "nivel": "básico",
            "theory":
                "El límite describe a qué valor se acerca f(x)\n"
                "cuando x se acerca a un punto c:\n"
                "    lim f(x) = L  (x → c)\n"
                "Definición ε-δ: ∀ε>0 ∃δ>0 tal que\n"
                "    |x-c|<δ ⇒ |f(x)-L|<ε.\n\n"
                "f es CONTINUA en p si:\n"
                "  1) f(p) existe\n"
                "  2) lim f(x) (x→p) existe\n"
                "  3) lim f(x) = f(p)\n\n"
                "Derivable ⇒ continua (no al revés).",
            "example":
                "f(x)=x², continua: lim f(x) cuando x→3 es f(3)=9.\n"
                "f(x)=|x|: continua en 0, pero NO derivable\n"
                "(pendientes -1 y +1 no coinciden).",
            "q_type": "mc",
            "question":
                "¿Cuál es lim (x²-4)/(x-2) cuando x→2?",
            "options": ["0", "2", "4", "No existe"],
            "correct": 2,
            "explanation":
                "(x²-4)/(x-2) = (x+2)(x-2)/(x-2) = x+2.\n"
                "Tomando x→2: 2+2 = 4.",
        },
        {
            "title": "Derivada: definición",
            "nivel": "básico",
            "theory":
                "Derivada = pendiente de la tangente en (x, f(x)).\n"
                "    f'(x) = lim [f(x+h) - f(x)] / h  (h → 0)\n"
                "Notación: df/dx, f'(x).\n\n"
                "Casos básicos:\n"
                "  • Recta f(x)=ax+b → f'(x) = a.\n"
                "  • Constante → derivada 0.\n"
                "  • Polinomio xⁿ → derivada n·xⁿ⁻¹.",
            "example":
                "f(x)=x², por definición:\n"
                "  [(x+h)²-x²]/h = [2xh+h²]/h = 2x+h → 2x\n"
                "→ f'(x) = 2x. En x=3 la pendiente es 6.",
            "q_type": "mc",
            "question":
                "¿Cuál es la derivada de f(x) = 5x + 7?",
            "options": ["5", "7", "5x", "12"],
            "correct": 0,
            "explanation":
                "Derivada de ax+b es a. Aquí a=5.",
        },
        {
            "title": "Reglas: suma, producto, cadena",
            "nivel": "intermedio",
            "theory":
                "Reglas fundamentales:\n"
                "  Suma:    (f+g)' = f' + g'\n"
                "  Escalar: (a·f)' = a·f'\n"
                "  Producto:(f·g)' = f'·g + f·g'\n"
                "  Cociente:(f/g)' = (f'g - fg')/g²\n"
                "  Cadena:  (f(g(x)))' = f'(g(x))·g'(x)\n\n"
                "Derivadas básicas:\n"
                "  (xⁿ)' = n·xⁿ⁻¹\n"
                "  (eˣ)' = eˣ\n"
                "  (ln x)' = 1/x (x>0)\n"
                "  (sin x)' = cos x,  (cos x)' = -sin x",
            "example":
                "f(x) = exp(5x³+x²-1).\n"
                "  Sea h(x) = 5x³+x²-1, h'(x) = 15x²+2x.\n"
                "  f'(x) = exp(5x³+x²-1)·(15x²+2x).\n\n"
                "g(x) = 2x⁴ + sin(3x):\n"
                "  g'(x) = 8x³ + 3·cos(3x).",
            "q_type": "mc",
            "question":
                "¿Derivada de f(x) = x²·ln(x)?",
            "options": [
                "2x · ln(x)",
                "2x · ln(x) + x",
                "2x + 1/x",
                "x · ln(x) + x²",
            ],
            "correct": 1,
            "explanation":
                "Producto: u=x², v=ln(x), u'=2x, v'=1/x.\n"
                "f' = 2x·ln(x) + x²·(1/x) = 2x·ln(x) + x.",
            "simple_explanation":
                "REGLA DEL PRODUCTO (en 1 línea):\n"
                "  Si f(x) = u(x)·v(x), entonces\n"
                "       f'(x) = u'·v + u·v'\n\n"
                "Lectura: «la derivada del primero por el segundo SIN derivar\n"
                "+ el primero SIN derivar por la derivada del segundo».\n\n"
                "REGLA DE LA CADENA (composición):\n"
                "  Si f(x) = g(h(x)), entonces\n"
                "       f'(x) = g'(h(x)) · h'(x)\n"
                "Lectura: 'derivada de fuera (evaluada en lo de dentro)\n"
                "POR la derivada de lo de dentro'.",
            "similar_examples": [
                "Producto con potencia:  f(x) = x³ · eˣ.\n"
                "  u=x³, v=eˣ, u'=3x², v'=eˣ.\n"
                "  f'(x) = 3x²·eˣ + x³·eˣ = x²·eˣ·(3 + x).",

                "Cadena con exponencial:  f(x) = e^(x²).\n"
                "  Fuera: g(t)=eᵗ, dentro: h(x)=x².\n"
                "  g'(t) = eᵗ,  h'(x) = 2x.\n"
                "  f'(x) = e^(x²) · 2x.",

                "Cadena con logaritmo:  f(x) = ln(3x+1).\n"
                "  Fuera: g(t)=ln(t), dentro: h(x)=3x+1.\n"
                "  g'(t)=1/t, h'(x)=3.\n"
                "  f'(x) = (1/(3x+1)) · 3 = 3/(3x+1).",

                "Producto Y cadena combinados:  f(x) = x · sin(x²).\n"
                "  Producto: u=x, v=sin(x²).\n"
                "  v' por cadena: cos(x²)·2x.\n"
                "  f'(x) = 1·sin(x²) + x·cos(x²)·2x\n"
                "        = sin(x²) + 2x²·cos(x²).",
            ],
        },
        {
            "title": "Crecimiento y monotonía",
            "nivel": "intermedio",
            "theory":
                "Signo de f' indica monotonía:\n"
                "  f'(x) > 0 → f creciente alrededor de x\n"
                "  f'(x) < 0 → f decreciente\n"
                "  f'(x) = 0 → posible punto crítico",
            "example":
                "h(x) = 4x - x².\n"
                "  h'(x) = 4 - 2x.\n"
                "  h' > 0 ↔ x < 2 (creciente)\n"
                "  h' < 0 ↔ x > 2 (decreciente)\n"
                "  h'(2)=0 (máximo). Mira la gráfica abajo.",
            "visual": {
                "tipo": "funcion",
                "expr": lambda x: 4 * x - x * x,
                "xrange": (-1, 5),
                "yrange": (-2, 5),
                "marks": [(2, 4, "max (2,4)")],
                "title": "h(x) = 4x - x²",
            },
            "q_type": "mc",
            "question":
                "f(x) = x³ - 3x. ¿En qué intervalo decrece?",
            "options": [
                "(-∞, -1)",
                "(-1, 1)",
                "(1, ∞)",
                "Nunca decrece",
            ],
            "correct": 1,
            "explanation":
                "f' = 3(x-1)(x+1) < 0 ⇔ -1 < x < 1.",
        },
        {
            "title": "Extremos relativos",
            "nivel": "intermedio",
            "theory":
                "Punto crítico: f'(x₀) = 0 (o no existe).\n"
                "Teorema de Fermat: extremo local ⇒ f' = 0.\n\n"
                "Criterio segunda derivada en x₀ crítico:\n"
                "  f''(x₀) > 0 ⇒ mínimo local\n"
                "  f''(x₀) < 0 ⇒ máximo local\n"
                "  f''(x₀) = 0 ⇒ inconcluyente.",
            "example":
                "g(x) = x³ - 6x² + 1.\n"
                "  g' = 3x² - 12x = 3x(x-4). Críticos: x=0, x=4.\n"
                "  g'' = 6x - 12.\n"
                "  g''(0) = -12 < 0 → máximo local en x=0.\n"
                "  g''(4) = +12 > 0 → mínimo local en x=4.\n"
                "Mira la recta numérica con la clasificación.",
            "visual": {
                "tipo": "recta_numerica",
                "xrange": (-2, 7),
                "intervals": [
                    {"a": -2, "b": 0, "label": "creciente",
                     "color": "#3fb950", "above": True},
                    {"a": 0, "b": 4, "label": "decreciente",
                     "color": "#f85149", "above": True},
                    {"a": 4, "b": 7, "label": "creciente",
                     "color": "#3fb950", "above": True},
                ],
                "marks": [
                    {"x": 0, "label": "máx local", "color": "#f85149"},
                    {"x": 4, "label": "mín local", "color": "#3fb950"},
                ],
                "title": "g(x) = x³ - 6x² + 1: monotonía y extremos",
            },
            "q_type": "mc",
            "question":
                "f(x) = x² - 4x + 7. ¿Qué tipo de extremo tiene en x=2?",
            "options": [
                "Máximo local",
                "Mínimo local",
                "Punto de inflexión",
                "No es punto crítico",
            ],
            "correct": 1,
            "explanation":
                "f'(2) = 0, f'' = 2 > 0 → mínimo local.",
        },
        {
            "title": "Optimización: extremos absolutos",
            "nivel": "experto",
            "theory":
                "Teorema de Weierstrass: toda f continua en [a,b]\n"
                "alcanza máximo y mínimo absolutos.\n\n"
                "Receta para optimizar en [a,b]:\n"
                "  1) Hallar puntos críticos en (a,b)\n"
                "  2) Evaluar f en críticos\n"
                "  3) Evaluar f(a) y f(b)\n"
                "  4) Comparar: mayor = máximo, menor = mínimo.",
            "example":
                "f(x) = x³ - 3x en [-2, 2].\n"
                "  f' = 0 ⇒ x = ±1.\n"
                "  f(-2)=-2, f(-1)=2, f(1)=-2, f(2)=2.\n"
                "Máximo absoluto = 2; mínimo absoluto = -2.",
            "q_type": "mc",
            "question":
                "f(x)=x²-4x+1 en [0,3]. ¿Mínimo absoluto?",
            "options": ["-3", "1", "-2", "0"],
            "correct": 0,
            "explanation":
                "f'(x)=2x-4=0 ⇒ x=2. f(0)=1, f(2)=-3, f(3)=-2.\n"
                "Mínimo: -3 en x=2.",
        },
        {
            "title": "Integral definida y Barrow",
            "nivel": "experto",
            "theory":
                "∫ₐᵇ f(x) dx interpreta el ÁREA bajo f en [a,b].\n"
                "Se define como límite de sumas de Riemann.\n\n"
                "Primitiva F: F'=f. Teorema fundamental (Barrow):\n"
                "    ∫ₐᵇ f(x) dx = F(b) - F(a)\n\n"
                "Primitivas básicas:\n"
                "  ∫ xᵏ dx = xᵏ⁺¹/(k+1)   (k≠-1)\n"
                "  ∫ eˣ dx = eˣ\n"
                "  ∫ (1/x) dx = ln|x|",
            "example":
                "∫₀² x² dx = [x³/3]₀² = 8/3.\n"
                "∫₁ᵉ (1/x) dx = ln(e) - ln(1) = 1.",
            "q_type": "mc",
            "question":
                "¿Cuál es ∫₀¹ (2x + 1) dx?",
            "options": ["1", "2", "3", "1/2"],
            "correct": 1,
            "explanation":
                "F(x) = x² + x. F(1) - F(0) = 2.",
        },
    ],

    # =================================================================
    "3.2  Cálculo multivariable": [
        {
            "title": "Derivadas parciales",
            "nivel": "básico",
            "theory":
                "Para f(x₁,…,xₙ), la derivada parcial respecto a xᵢ:\n"
                "  ∂f/∂xᵢ = lim [f(…,xᵢ+h,…) - f(…,xᵢ,…)]/h\n"
                "Idea práctica: derivar respecto a xᵢ tratando el\n"
                "resto como CONSTANTES.",
            "example":
                "f(x,y) = x²·y + 3y.\n"
                "  ∂f/∂x = 2xy (y constante)\n"
                "  ∂f/∂y = x² + 3 (x constante)\n\n"
                "g(x,y) = sin(xy):\n"
                "  ∂g/∂x = y·cos(xy)\n"
                "  ∂g/∂y = x·cos(xy)",
            "q_type": "mc",
            "question":
                "f(x,y) = x³ + 2xy² + y. ¿∂f/∂x en (1, 2)?",
            "options": ["3", "11", "8", "5"],
            "correct": 1,
            "explanation":
                "∂f/∂x = 3x² + 2y². En (1,2): 3 + 8 = 11.",
        },
        {
            "title": "Gradiente y derivada direccional",
            "nivel": "intermedio",
            "theory":
                "GRADIENTE: vector con todas las parciales:\n"
                "    ∇f(x) = (∂f/∂x₁, …, ∂f/∂xₙ)\n\n"
                "Derivada DIRECCIONAL en dirección v:\n"
                "    ∂f/∂v = ∇f · v (producto escalar)\n\n"
                "PROPIEDAD CLAVE: ∇f apunta a la dirección de\n"
                "MÁXIMO CRECIMIENTO. -∇f es la dirección de\n"
                "máximo decrecimiento (base del gradient descent).",
            "example":
                "g(x,y) = 2xy + y².\n"
                "  ∇g = (2y, 2x+2y).\n"
                "Derivada en dirección v=(1,2):\n"
                "  ∇g·v = 2y + 2·(2x+2y) = 4x + 6y.\n"
                "En (1,1): 10.",
            "q_type": "mc",
            "question":
                "f(x,y) = x² + y². ¿∇f en (1, 2)?",
            "options": [
                "(1, 2)",
                "(2, 4)",
                "(2x, 2y)",
                "(0, 0)",
            ],
            "correct": 1,
            "explanation":
                "∇f = (2x, 2y). En (1,2): (2, 4).",
        },
        {
            "title": "Matriz hessiana",
            "nivel": "intermedio",
            "theory":
                "HESSIANA H(f): matriz n×n de segundas parciales:\n"
                "    H(f)ᵢⱼ = ∂²f/(∂xᵢ∂xⱼ)\n\n"
                "Schwarz: si continuas, ∂²f/∂xᵢ∂xⱼ = ∂²f/∂xⱼ∂xᵢ\n"
                "→ H es SIMÉTRICA.\n\n"
                "Para n=2:\n"
                "  H = [[fₓₓ, fₓᵧ],\n"
                "       [fᵧₓ, fᵧᵧ]]",
            "example":
                "f(x,y) = x² + 3xy + y³.\n"
                "  fₓ = 2x+3y, fᵧ = 3x+3y²\n"
                "  fₓₓ = 2, fᵧᵧ = 6y, fₓᵧ = fᵧₓ = 3 (Schwarz ✓)\n"
                "  H = [[2, 3],[3, 6y]]\n"
                "En (1,1): H = [[2,3],[3,6]].",
            "q_type": "mc",
            "question":
                "Para f(x,y) = x²y, ¿hessiana?",
            "options": [
                "[[2y, 2x],[2x, 0]]",
                "[[2x, 2y],[2y, 0]]",
                "[[0, 2x],[2x, 0]]",
                "[[2y, x],[x, 0]]",
            ],
            "correct": 0,
            "explanation":
                "fₓ=2xy, fᵧ=x². fₓₓ=2y, fᵧᵧ=0, fₓᵧ=2x.",
        },
        {
            "title": "Puntos críticos y hessiana",
            "nivel": "experto",
            "theory":
                "Punto crítico: ∇f(x*) = 0.\n\n"
                "Para n=2, A=fₓₓ, B=fᵧᵧ, C=fₓᵧ:\n"
                "  det(H) = A·B - C²\n"
                "  det>0 y A>0 ⇒ mínimo local\n"
                "  det>0 y A<0 ⇒ máximo local\n"
                "  det<0       ⇒ punto SILLA\n"
                "  det=0       ⇒ no concluyente.",
            "example":
                "f(x,y) = x² + y² - 4x - 6y + 13.\n"
                "  ∇f = (2x-4, 2y-6) = 0 ⇒ (2, 3).\n"
                "  H = [[2,0],[0,2]], det = 4>0, A=2>0 ⇒ mínimo.\n"
                "f(2,3) = 0.",
            "q_type": "mc",
            "question":
                "f(x,y) = x² - y². ¿Qué es (0, 0)?",
            "options": [
                "Mínimo local",
                "Máximo local",
                "Punto silla",
                "No es crítico",
            ],
            "correct": 2,
            "explanation":
                "H = [[2,0],[0,-2]], det = -4 < 0 → silla.",
        },
        {
            "title": "Lagrange: optimización con restricciones",
            "nivel": "experto",
            "theory":
                "Para optimizar f(x,y) bajo g(x,y) = 0:\n"
                "    ∇f = λ·∇g\n"
                "Sistema:\n"
                "  ∂f/∂x = λ·∂g/∂x\n"
                "  ∂f/∂y = λ·∂g/∂y\n"
                "  g(x, y) = 0\n\n"
                "Aplicación ML: regularización, SVM, restricciones físicas.",
            "example":
                "Maximizar f(x,y) = xy bajo x + y = 10.\n"
                "  ∇f = (y, x), ∇g = (1, 1).\n"
                "  y = λ, x = λ ⇒ x = y. Con x+y=10: x=y=5.\n"
                "Máximo: f(5,5) = 25.",
            "q_type": "mc",
            "question":
                "Minimizar f(x,y)=x²+y² sujeto a x+y=2. ¿Punto óptimo?",
            "options": [
                "(2, 0)",
                "(0, 2)",
                "(1, 1)",
                "(-1, 3)",
            ],
            "correct": 2,
            "explanation":
                "2x=λ, 2y=λ ⇒ x=y. Con x+y=2: x=y=1.",
        },
    ],

    # =================================================================
    "3.3  Gradient descent + Backprop": [
        {
            "title": "Idea geométrica del GD",
            "nivel": "básico",
            "theory":
                "Gradient Descent: método iterativo para MINIMIZAR\n"
                "una función de coste E(w).\n\n"
                "Intuición: bajar una colina. ∇E apunta hacia ARRIBA,\n"
                "-∇E apunta hacia ABAJO. Movemos pequeños pasos en\n"
                "dirección -∇E hasta llegar a un mínimo.",
            "example":
                "E(w) = (w-3)², mínimo en w=3.\n"
                "  ∇E(w) = 2(w-3).\n"
                "Si w=5: ∇E = +4 (sube derecha) → ir IZQUIERDA.",
            "q_type": "tf",
            "question":
                "En GD nos movemos en dirección OPUESTA al gradiente\n"
                "para minimizar.",
            "options": ["Verdadero", "Falso"],
            "correct": 0,
            "explanation":
                "El gradiente apunta a máximo crecimiento; -∇ baja.",
        },
        {
            "title": "Algoritmo GD con learning rate",
            "nivel": "básico",
            "theory":
                "Regla:\n"
                "    w_{t+1} = w_t - η·∇E(w_t)\n\n"
                "η (eta) > 0 = tasa de aprendizaje.\n"
                "  η muy pequeño → converge lentísimo.\n"
                "  η muy grande  → DIVERGE / oscila.",
            "example":
                "E(w)=(w-1)², η=0.5, w₀=3.\n"
                "  ∇E = 2(3-1) = 4\n"
                "  w₁ = 3 - 0.5·4 = 1  (¡llega!)\n\n"
                "Si η = 1.1: w₁ = -1.4, se aleja → DIVERGE.",
            "q_type": "mc",
            "question":
                "¿Qué problema causa una η demasiado grande?",
            "options": [
                "Converge muy lento",
                "Puede divergir o saltar el mínimo",
                "Aumenta el coste de memoria",
                "Hace que el gradiente sea cero",
            ],
            "correct": 1,
            "explanation":
                "Pasos demasiado grandes saltan sobre el mínimo.",
        },
        {
            "title": "Ejemplo numérico: minimizar x²",
            "nivel": "intermedio",
            "theory":
                "f(x) = x², mínimo en x=0. f'(x) = 2x.\n"
                "Regla: x_{t+1} = x_t - η·2x_t = x_t·(1-2η).\n"
                "Con η=0.1: factor = 0.8. x converge a 0 geométricamente.",
            "example":
                "x₀ = 2, η = 0.1.\n"
                "  t=1: x = 2 - 0.1·4 = 1.6\n"
                "  t=2: x = 1.6 - 0.1·3.2 = 1.28\n"
                "  t=3: x = 1.28 - 0.256 = 1.024\n"
                "Valores f: 4 → 2.56 → 1.64 → 1.05 ...\n"
                "Pulsa «▶ Animar» para ver la bolita bajar por f(x)=x².\n"
                "🧊 «Ver en 3D»: el mismo descenso sobre el cuenco\n"
                "z = x² + y² (la versión real con 2 variables).",
            "visual": {
                "tipo": "funcion",
                "expr": lambda x: x * x,
                "xrange": (-2.5, 2.5),
                "yrange": (-0.5, 5),
                "title": "Descenso de gradiente sobre f(x) = x²",
                "animate": {
                    "tipo": "descenso",
                    "x0": 2.0, "lr": 0.1, "steps": 10,
                    "grad": lambda x: 2 * x,
                },
            },
            "visual3d": {
                "tipo": "superficie",
                "title": "Descenso de gradiente sobre z = x² + y²",
                "f": lambda x, y: x * x + y * y,
                "xrange": (-2.5, 2.5),
                "yrange": (-2.5, 2.5),
                "x0": 2.2, "y0": 1.8, "lr": 0.12, "steps": 14,
                "grad": lambda x, y: (2 * x, 2 * y),
            },
            "q_type": "mc",
            "question":
                "f(x)=x², η=0.1, x₀=2. ¿x tras 2 iteraciones?",
            "options": ["1.6", "1.28", "1.024", "0.8"],
            "correct": 1,
            "explanation":
                "Aplicando GD x_{t+1} = x_t - η·2x_t = x_t·(1-2η):\n"
                "  Con η=0.1:  factor = 1 - 0.2 = 0.8.\n"
                "  Iteración 1: x₁ = 2·0.8 = 1.6.\n"
                "  Iteración 2: x₂ = 1.6·0.8 = 1.28.   ✓\n"
                "Tras 3 iter sería 1.024 (otra opción que confundir).",
        },
        {
            "title": "Forward pass en red simple",
            "nivel": "intermedio",
            "theory":
                "Forward pass: calcular ŷ dado x, capa por capa.\n"
                "Para una neurona:\n"
                "  z = w·x + b\n"
                "  a = σ(z)\n"
                "Sigmoide: σ(z) = 1/(1+e⁻ᶻ).\n"
                "Su derivada: σ'(z) = σ(z)·(1-σ(z)).",
            "example":
                "Red 1→1→1: w₁=2, b₁=-1, w₂=1, b₂=0, σ=sigmoid.\n"
                "x=1:\n"
                "  z₁ = 2·1 - 1 = 1\n"
                "  a₁ = σ(1) ≈ 0.7311\n"
                "  ŷ = 1·0.7311 + 0 = 0.7311",
            "q_type": "mc",
            "question":
                "¿Cuál NO forma parte del forward pass?",
            "options": [
                "Calcular z = w·x + b",
                "Aplicar la activación σ(z)",
                "Propagar errores hacia capas anteriores",
                "Encadenar capa por capa hasta la salida",
            ],
            "correct": 2,
            "explanation":
                "Propagar errores hacia atrás es backprop, no forward.",
        },
        {
            "title": "Backpropagation: regla de la cadena",
            "nivel": "experto",
            "theory":
                "Backprop = regla de la cadena propagada hacia ATRÁS.\n\n"
                "Red simple: z=wx+b, a=σ(z), ŷ=a, E coste.\n"
                "  ∂E/∂w = (∂E/∂a)·(∂a/∂z)·(∂z/∂w)\n\n"
                "Con sigmoide: ∂a/∂z = a(1-a). ∂z/∂w = x.\n"
                "Luego: w ← w - η·∂E/∂w.",
            "example":
                "ŷ = σ(w·x + b), E = (ŷ-y)².\n"
                "  ∂E/∂w = 2(ŷ-y)·ŷ(1-ŷ)·x\n\n"
                "Con x=1, y=0, ŷ=0.7311:\n"
                "  ∂E/∂w = 2·0.7311·0.7311·0.2689·1 ≈ 0.287.\n"
                "Δw = -0.1·0.287 ≈ -0.029.",
            "q_type": "mc",
            "question":
                "¿Qué regla del cálculo permite obtener ∂E/∂w en capas profundas?",
            "options": [
                "Regla del producto",
                "Regla de la cadena",
                "Teorema de Weierstrass",
                "Teorema de Fermat",
            ],
            "correct": 1,
            "explanation":
                "Backprop = regla de la cadena en cada capa.",
            "simple_explanation":
                "Imagina backprop como un PEAJE INVERSO:\n\n"
                "  Forward (ida):  x → · → + → σ → ŷ → L\n"
                "  Backward (vuelta): L ← · ← + ← σ ← ŷ ← L\n\n"
                "En cada nodo guardas la DERIVADA LOCAL.\n"
                "Al hacer el viaje de vuelta, MULTIPLICAS todas las\n"
                "derivadas locales del camino. Eso es la REGLA DE LA\n"
                "CADENA aplicada a un grafo.\n\n"
                "Ejemplo mental: si en cada peaje pagas '×0.5', y hay 4\n"
                "peajes en serie, al llegar al final pagaste 0.5⁴ = 0.0625.\n"
                "Por eso los gradientes se DESVANECEN en redes profundas\n"
                "(vanishing gradient): muchas derivadas <1 multiplicadas.",
            "similar_examples": [
                "Red de 1 capa, x→z=w·x+b → ŷ = σ(z) → L = (ŷ-y)².\n"
                "  ∂L/∂ŷ = 2(ŷ-y)\n"
                "  ∂ŷ/∂z = σ'(z) = ŷ(1-ŷ)\n"
                "  ∂z/∂w = x\n"
                "  ∂L/∂w = 2(ŷ-y)·ŷ(1-ŷ)·x\n"
                "Solo 3 factores. En redes profundas son más.",

                "Red de 2 capas (h y ŷ):\n"
                "  z₁ = W₁x+b₁,  h = σ(z₁),  z₂ = W₂h+b₂,  ŷ = z₂\n"
                "  Buscamos ∂L/∂W₁.\n"
                "  Por la cadena:\n"
                "    ∂L/∂W₁ = ∂L/∂ŷ · ∂ŷ/∂z₂ · ∂z₂/∂h · ∂h/∂z₁ · ∂z₁/∂W₁\n"
                "         = (ŷ-y)·1·W₂·σ'(z₁)·x\n"
                "Cada flecha del grafo aporta UN factor en el producto.",

                "Por qué se llama 'propagación HACIA ATRÁS':\n"
                "Calculas primero las derivadas en la SALIDA, luego las\n"
                "vas pasando hacia los pesos cercanos a la ENTRADA,\n"
                "multiplicando capa por capa. La complejidad es O(|E|)\n"
                "donde |E| son las aristas del grafo de cómputo.",
            ],
        },
        {
            "title": "GD en TensorFlow (conceptual)",
            "nivel": "experto",
            "theory":
                "TensorFlow automatiza gradientes con tf.GradientTape:\n"
                "  1) Dentro del tape, ejecuta forward + cost.\n"
                "  2) tape.gradient(loss, vars) hace backprop.\n"
                "  3) optimizer.apply_gradients() actualiza con GD.",
            "example":
                "Pseudocódigo:\n"
                "  with tf.GradientTape() as tape:\n"
                "      y_pred = model(x)\n"
                "      loss = mse(y, y_pred)\n"
                "  grads = tape.gradient(loss, model.trainable_variables)\n"
                "  optimizer.apply_gradients(\n"
                "      zip(grads, model.trainable_variables))",
            "q_type": "mc",
            "question":
                "¿Qué hace tape.gradient(loss, vars) en TensorFlow?",
            "options": [
                "Ejecuta el forward pass",
                "Calcula ∂loss/∂vars vía backpropagation",
                "Actualiza los pesos del modelo",
                "Define la arquitectura",
            ],
            "correct": 1,
            "explanation":
                "tape.gradient aplica regla de la cadena sobre las\n"
                "operaciones grabadas en el tape.",
        },
    ],

    # =================================================================
    "4.1  Probabilidad": [
        {
            "title": "Experimento, espacio muestral, sucesos",
            "nivel": "básico",
            "theory":
                "EXPERIMENTO aleatorio: acción cuyo resultado no se\n"
                "predice con certeza.\n"
                "ESPACIO MUESTRAL Ω: conjunto de todos los resultados.\n"
                "SUCESO E: subconjunto de Ω.\n\n"
                "Operaciones: E∪F, E∩F, Eᶜ.\n"
                "Probabilidad P: P(Ω)=1, 0≤P(E)≤1,\n"
                "  P(E∪F) = P(E)+P(F) si E∩F=∅.",
            "example":
                "Dado de 6: Ω = {1,2,3,4,5,6}.\n"
                "E = 'sale par' = {2,4,6}. P(E) = 3/6 = 0.5.",
            "q_type": "mc",
            "question":
                "Lanzamos dos dados. ¿Espacio muestral?",
            "options": [
                "Los 12 valores del 1 al 12",
                "Los 36 pares ordenados (i,j) con 1≤i,j≤6",
                "Los 21 pares no ordenados",
                "Las sumas {2,…,12}",
            ],
            "correct": 1,
            "explanation":
                "|Ω| = 6 × 6 = 36 pares ordenados.",
        },
        {
            "title": "Regla de Laplace",
            "nivel": "básico",
            "theory":
                "Si Ω finito y resultados equiprobables:\n"
                "    P(E) = |E| / |Ω|  (favorables/posibles).\n"
                "Requiere simetría (dado equilibrado, baraja barajada).",
            "example":
                "Urna 30 blancas + 70 negras:\n"
                "  P(blanca) = 30/100 = 0.30.\n"
                "Dado: P(múltiplo de 3) = 2/6 = 1/3.",
            "q_type": "mc",
            "question":
                "Baraja española 40 cartas. ¿Probabilidad de espada (10)?",
            "options": ["0.10", "0.25", "0.40", "0.50"],
            "correct": 1,
            "explanation":
                "Por Laplace: P(E) = |E| / |Ω| = 10 / 40 = 0.25 (25 %).\n"
                "Errores típicos:\n"
                "  0.10 = 10/100 (confundir total),\n"
                "  0.40 = 10/25 (denominador erróneo),\n"
                "  0.50 = la mitad — un sesgo común sin contar.",
        },
        {
            "title": "Independencia de sucesos",
            "nivel": "intermedio",
            "theory":
                "A y B son INDEPENDIENTES si:\n"
                "    P(A ∩ B) = P(A)·P(B)\n"
                "Consecuencia: P(A|B) = P(A) cuando indep.\n\n"
                "NO confundir con incompatibles (A∩B = ∅).\n"
                "Independencia ≠ disjuntos.",
            "example":
                "Dos monedas equilibradas: A='cara en 1ª',\n"
                "B='cara en 2ª'. P(A)=P(B)=0.5.\n"
                "P(A∩B) = 1/4 = 0.5·0.5 → independientes.",
            "q_type": "mc",
            "question":
                "P(A)=0.4, P(B)=0.5, independientes. ¿P(A∩B)?",
            "options": ["0.10", "0.20", "0.45", "0.90"],
            "correct": 1,
            "explanation":
                "Independencia ⇒ P(A∩B) = P(A)·P(B) = 0.4·0.5 = 0.20.\n"
                "Distractores:\n"
                "  0.90 = P(A)+P(B) (suma, sería para A∪B sin intersección),\n"
                "  0.45 = (P(A)+P(B))/2 (media, no significa nada aquí),\n"
                "  0.10 = |P(A)-P(B)| (diferencia, tampoco aplica).",
        },
        {
            "title": "Probabilidad condicionada",
            "nivel": "intermedio",
            "theory":
                "    P(A|B) = P(A∩B) / P(B)   (P(B)>0)\n"
                "Regla del producto:\n"
                "    P(A∩B) = P(A|B)·P(B)\n\n"
                "Si A,B indep: P(A|B) = P(A).\n"
                "En general P(A|B) ≠ P(B|A).",
            "example":
                "Dos dados, F='ambos pares', E='valores iguales'.\n"
                "|F| = 9, |E∩F| = 3 (pares iguales pares).\n"
                "P(E|F) = 3/9 = 1/3.",
            "q_type": "tf",
            "question":
                "Si A y B son independientes, P(A|B) = P(A).",
            "options": ["Verdadero", "Falso"],
            "correct": 0,
            "explanation":
                "P(A|B) = P(A)P(B)/P(B) = P(A) cuando indep.",
            "simple_explanation":
                "P(A|B) responde: «si SÉ que ocurrió B, ¿cuál es la\n"
                "probabilidad de A?»\n\n"
                "Receta concreta:\n"
                "  1) Imagina los 'casos posibles' que cumplen B.\n"
                "  2) De ellos, cuenta los que también cumplen A.\n"
                "  3) Dividir:  casos A∩B / casos B.\n\n"
                "Importante: P(A|B) NO es lo mismo que P(B|A).\n"
                "Si el grupo B es pequeño y A∩B grande, P(A|B) sube;\n"
                "si B es enorme, P(A|B) baja aunque P(A∩B) sea el mismo.",
            "similar_examples": [
                "Dos dados, F='ambos pares' (9 pares posibles),\n"
                "                E='ambos iguales' (3 pares dentro de F):\n"
                "  P(E|F) = 3/9 = 1/3.\n"
                "Si solo conoces F (pares), restringes tu universo a 9\n"
                "casos y dentro buscas E.",

                "Cartas: A='es rey', B='es figura' (J,Q,K).\n"
                "  Hay 12 figuras en la baraja (4 J, 4 Q, 4 K).\n"
                "  Reyes que son figuras: 4.\n"
                "  P(A|B) = 4/12 = 1/3.\n"
                "Sabiendo que es figura, 1 de cada 3 es rey.",

                "Comparación P(A|B) vs P(B|A):\n"
                "  En el caso de cartas, P(B|A) (figura SABIENDO que es rey):\n"
                "    todos los reyes son figuras → P(B|A) = 1.\n"
                "  ¡Distinto de P(A|B) = 1/3!\n"
                "Por eso decir 'casi todos los X son Y' NO implica\n"
                "'casi todos los Y son X'.",
            ],
        },
        {
            "title": "Teorema de Bayes (test diagnóstico)",
            "nivel": "experto",
            "theory":
                "    P(A|B) = P(B|A)·P(A) / P(B)\n\n"
                "P(B) por probabilidad total:\n"
                "    P(B) = P(B|A)·P(A) + P(B|Aᶜ)·P(Aᶜ)\n\n"
                "Términos:\n"
                "  P(A): a PRIORI    P(B|A): VEROSIMILITUD\n"
                "  P(A|B): POSTERIORI\n"
                "  P(B): evidencia (normalizador).",
            "example":
                "Enfermedad rara: P(E)=0.01, P(+|E)=0.99, P(+|Eᶜ)=0.05.\n"
                "P(+) = 0.99·0.01 + 0.05·0.99 = 0.0594.\n"
                "P(E|+) = 0.0099/0.0594 ≈ 0.167 (¡solo 16.7%!).",
            "q_type": "mc",
            "question":
                "Si P(E) sube a 0.10 manteniendo test, P(E|+) será:",
            "options": [
                "Aproximadamente igual (≈0.17)",
                "Considerablemente mayor",
                "Considerablemente menor",
                "Igual a la sensibilidad (0.99)",
            ],
            "correct": 1,
            "explanation":
                "Con P(E)=0.10: P(+)=0.144; P(E|+)≈0.688.",
            "visual": {
                "tipo": "arbol",
                "title": "Árbol de Bayes — test diagnóstico",
                "root": {
                    "label": "1000 personas",
                    "color": "#102530",
                    "children": [
                        {"label": "Enfermos (10)",
                         "edge_label": "P(E)=0.01",
                         "color": "#3a1d1d", "outline": "#f85149",
                         "children": [
                             {"label": "+  (≈10)",
                              "edge_label": "0.99",
                              "color": "#16361f",
                              "outline": "#3fb950"},
                             {"label": "-  (≈0)",
                              "edge_label": "0.01"},
                         ]},
                        {"label": "Sanos (990)",
                         "edge_label": "P(¬E)=0.99",
                         "color": "#102530", "outline": "#39c5cf",
                         "children": [
                             {"label": "+  (≈50)",
                              "edge_label": "0.05",
                              "color": "#3a1d1d",
                              "outline": "#f85149"},
                             {"label": "-  (≈940)",
                              "edge_label": "0.95"},
                         ]},
                    ],
                },
            },
            "simple_explanation":
                "BAYES con NÚMEROS CONCRETOS (imagina 1000 personas):\n\n"
                "Caso del ejemplo (P(E)=0.01, sensibilidad 99%, FP 5%):\n"
                "  • Enfermos        : 10 personas\n"
                "       de ellos, 99% positivos → 9.9 ≈ 10 positivos\n"
                "  • Sanos          : 990 personas\n"
                "       de ellos, 5% falsos positivos → 49.5 ≈ 50 +\n"
                "  • Total positivos = 10 + 50 = 60\n"
                "  • ¿De esos 60 positivos, cuántos son enfermos?\n"
                "       10 / 60 ≈ 16.7%\n\n"
                "Por eso un test que parece muy bueno (99% sensibilidad)\n"
                "da casi un 84% de FALSOS POSITIVOS cuando la enfermedad\n"
                "es rara. La probabilidad PREVIA (prevalencia) IMPORTA.",
            "similar_examples": [
                "Caso prevalencia ALTA (P(E) = 0.50):\n"
                "  De 1000: 500 enfermos, 500 sanos.\n"
                "  Positivos enfermos: 500·0.99 = 495\n"
                "  Falsos positivos:   500·0.05 = 25\n"
                "  Total positivos: 520\n"
                "  P(E|+) = 495/520 ≈ 95.2%. (¡Ahora SÍ es alto!)",

                "Caso prevalencia BAJÍSIMA (P(E)=0.001):\n"
                "  De 100 000: 100 enfermos, 99 900 sanos.\n"
                "  Positivos enfermos: 99\n"
                "  Falsos positivos: 99 900·0.05 = 4995\n"
                "  P(E|+) = 99/5094 ≈ 1.9%.\n"
                "  ¡Hasta un test muy bueno es casi inútil aquí!",

                "Por qué la prevalencia manda:\n"
                "  Bayes  ∝  verosimilitud · PRIOR\n"
                "  Si el prior es minúsculo, ni una verosimilitud\n"
                "  enorme puede salvar el posterior.\n"
                "  Solución práctica: hacer DOS tests independientes\n"
                "  para multiplicar la evidencia.",
            ],
        },
        {
            "title": "Variables aleatorias: discretas y continuas",
            "nivel": "intermedio",
            "theory":
                "Variable aleatoria X: Ω → ℝ.\n\n"
                "DISCRETA: valores numerables.\n"
                "  f(x) = P(X=x), ∑f(x) = 1.\n\n"
                "CONTINUA: densidad f(x) ≥ 0 con ∫f=1 y\n"
                "  P(X∈[a,b]) = ∫ₐᵇ f(x) dx.\n"
                "P(X=x) = 0 en continuas.",
            "example":
                "Bernoulli(p=0.3): P(X=1)=0.3, P(X=0)=0.7.\n\n"
                "Uniforme [0,2]: f(x)=1/2 en [0,2].\n"
                "P(0.5≤X≤1.5) = 0.5.\n"
                "P(X=1) = 0 (continua).",
            "q_type": "mc",
            "question":
                "Para X continua con densidad f, ¿P(X=1.7)?",
            "options": ["1.7", "f(1.7)", "0", "Depende de f"],
            "correct": 2,
            "explanation":
                "En continuas, P de punto concreto = 0.",
        },
        {
            "title": "Esperanza y varianza (dado)",
            "nivel": "experto",
            "theory":
                "ESPERANZA:\n"
                "  Discreta: E[X] = ∑ x·P(X=x)\n"
                "  Continua: E[X] = ∫ x·f(x) dx\n"
                "Linealidad: E[aX+bY] = aE[X]+bE[Y].\n\n"
                "VARIANZA: Var(X) = E[X²] - E[X]².\n"
                "  Var(aX+b) = a²Var(X).\n"
                "  σ = √Var.",
            "example":
                "Dado: X ∈ {1..6}, P=1/6 c.u.\n"
                "  E[X] = 21/6 = 3.5\n"
                "  E[X²] = 91/6 ≈ 15.17\n"
                "  Var(X) = 15.17 - 12.25 ≈ 2.92\n"
                "  σ ≈ 1.708.\n"
                "La gráfica de barras muestra la distribución uniforme.",
            "visual": {
                "tipo": "distribucion",
                "data": [(1, 1/6), (2, 1/6), (3, 1/6),
                          (4, 1/6), (5, 1/6), (6, 1/6)],
                "title": "Distribución dado equilibrado",
            },
            "q_type": "mc",
            "question":
                "Si Var(X)=4, ¿Var(3X+5)?",
            "options": ["12", "36", "37", "9"],
            "correct": 1,
            "explanation":
                "Var(aX+b) = a²·Var(X) = 9·4 = 36.",
        },
    ],

    # =================================================================
    "4.2  Estimación de parámetros": [
        {
            "title": "Muestras i.i.d. y estimadores",
            "nivel": "básico",
            "theory":
                "Muestra i.i.d.: X₁,…,Xₙ independientes y misma\n"
                "distribución que la población.\n\n"
                "Estimadores muestrales:\n"
                "  media:    x̄ = (1/n)∑xᵢ\n"
                "  varianza: s² = (1/(n-1))∑(xᵢ-x̄)²\n"
                "El divisor n-1 hace que s² sea INSESGADO de σ².",
            "example":
                "Muestra: 4, 8, 6, 10, 2 (n=5).\n"
                "  x̄ = 30/5 = 6.\n"
                "  Desviaciones²: 4, 4, 0, 16, 16 → suma 40.\n"
                "  s² = 40/4 = 10, s ≈ 3.16.",
            "q_type": "mc",
            "question":
                "¿Por qué se divide entre n-1 en la varianza muestral?",
            "options": [
                "Por convención sin justificar",
                "Para que sea insesgado de σ²",
                "Porque siempre da menor",
                "Porque n no es entero",
            ],
            "correct": 1,
            "explanation":
                "n-1 compensa el sesgo introducido al usar x̄ en vez de μ.",
        },
        {
            "title": "Ley de grandes números y TCL",
            "nivel": "intermedio",
            "theory":
                "X₁, X₂, … i.i.d. con media μ y varianza σ².\n\n"
                "LGN: x̄ₙ → μ cuando n → ∞.\n\n"
                "TCL: para n grande,\n"
                "    x̄ₙ ≈ N(μ, σ²/n).\n"
                "Justifica el uso de la normal en estadística.",
            "example":
                "Dado: μ=3.5, σ² ≈ 2.92.\n"
                "Para n=100: x̄ ≈ N(3.5, 0.0292), σ̄ ≈ 0.17.\n"
                "P(3.3 ≤ x̄ ≤ 3.7) ≈ 0.76.",
            "q_type": "mc",
            "question":
                "Por TCL, distribución de x̄ₙ con n grande:",
            "options": [
                "N(0, 1)",
                "N(μ, σ²)",
                "N(μ, σ²/n)",
                "N(nμ, nσ²)",
            ],
            "correct": 2,
            "explanation":
                "Media μ y varianza σ²/n, normal para n grande.",
        },
        {
            "title": "Método de los momentos",
            "nivel": "intermedio",
            "theory":
                "Igualar momentos teóricos y muestrales:\n"
                "  E[X] = (1/n)∑xᵢ\n"
                "  E[X²] = (1/n)∑xᵢ²\n"
                "  ...\n"
                "Resolver el sistema para los parámetros.\n"
                "Ventaja: sencillo. Inconveniente: menos eficiente que MLE.",
            "example":
                "X ~ Unif([0, θ]), muestra de 10 valores con x̄=3.3.\n"
                "E[X] = θ/2. Ecuación: θ/2 = 3.3 → θ̂ = 6.6.",
            "q_type": "tf",
            "question":
                "El método de los momentos es siempre el más eficiente.",
            "options": ["Verdadero", "Falso"],
            "correct": 1,
            "explanation":
                "MLE suele tener mejores propiedades estadísticas.",
        },
        {
            "title": "Máxima verosimilitud (MLE)",
            "nivel": "experto",
            "theory":
                "Verosimilitud: L(θ|x) = ∏ f(xᵢ|θ).\n"
                "Log-verosimilitud: ℓ(θ) = ∑ log f(xᵢ|θ).\n"
                "MLE: θ̂ = argmax ℓ(θ). Derivar, igualar a 0.\n\n"
                "Bernoulli(p): ℓ(p) = n₁·log p + n₀·log(1-p).\n"
                "dℓ/dp = 0 ⇒ p̂ = n₁/n (proporción muestral).",
            "example":
                "Moneda lanzada 20 veces, 12 caras.\n"
                "  p̂_MLE = 12/20 = 0.60.",
            "q_type": "mc",
            "question":
                "50 emails, 8 spam. MLE de p = P(spam):",
            "options": ["0.08", "0.16", "0.42", "0.50"],
            "correct": 1,
            "explanation":
                "Para Bernoulli, p̂_MLE = n_éxitos / n = 8/50 = 0.16.\n"
                "Confusiones típicas:\n"
                "  0.08 = 8/100 (denominador erróneo),\n"
                "  0.42 = 1 - 0.58 (confundir con P(no-spam) mal contado),\n"
                "  0.50 = punto medio (suposición uniforme sin datos).",
            "simple_explanation":
                "IDEA INTUITIVA de MLE: «¿qué valor del parámetro\n"
                "hace MÁS PROBABLE haber observado mis datos?».\n\n"
                "Receta en 3 pasos:\n"
                "  1) Escribir L(θ) = producto de probabilidades de\n"
                "     cada observación bajo el modelo.\n"
                "  2) Tomar log para convertir productos en sumas\n"
                "     (más fácil de derivar).\n"
                "  3) Derivar respecto a θ, igualar a cero, resolver.\n\n"
                "Para Bernoulli (éxito/fallo):\n"
                "  p̂_MLE = nº de éxitos / nº de ensayos.\n"
                "Es la PROPORCIÓN MUESTRAL, lo más natural del mundo.",
            "similar_examples": [
                "Caso lanzamientos de moneda:\n"
                "  100 tiradas, 67 caras → p̂ = 67/100 = 0.67.\n"
                "Hipótesis: la moneda no parece justa.",

                "Caso eventos raros (Poisson):\n"
                "  Cuentas llegadas por hora durante 5 horas:\n"
                "  [3, 2, 4, 3, 3]. Total = 15.\n"
                "  λ̂_MLE = 15/5 = 3 llegadas/hora.\n"
                "Para Poisson, λ̂ = media muestral.",

                "Caso normal N(μ, σ²):\n"
                "  Muestra: 4, 8, 6, 10, 2.\n"
                "  μ̂_MLE = (4+8+6+10+2)/5 = 6.\n"
                "  σ̂²_MLE = (1/n)·∑(xᵢ-μ̂)² = 40/5 = 8.\n"
                "(MLE usa n; el insesgado usa n-1).",

                "Por qué se llama 'verosimilitud':\n"
                "  Probabilidad VE-RO-SIMIL = parece verdad.\n"
                "Buscamos el θ que hace los datos OBSERVADOS\n"
                "más probables (no más raros).",
            ],
        },
    ],

    # =================================================================
    "4.3  Procesos estocásticos": [
        {
            "title": "Matrices estocásticas",
            "nivel": "básico",
            "theory":
                "Matriz M ∈ ℝⁿˣⁿ es ESTOCÁSTICA (por filas) si:\n"
                "  1) aᵢⱼ ≥ 0 ∀i,j.\n"
                "  2) ∑ⱼ aᵢⱼ = 1 para cada fila i.\n\n"
                "Cada fila = distribución de transiciones desde el\n"
                "estado i a los demás.",
            "example":
                "P = [[0.7, 0.3],[0.4, 0.6]].\n"
                "  Fila 1: 0.7+0.3 = 1 ✓\n"
                "  Fila 2: 0.4+0.6 = 1 ✓\n"
                "Es estocástica.",
            "q_type": "mc",
            "question":
                "¿Cuál NO es estocástica (por filas)?",
            "options": [
                "[[1, 0], [0, 1]]",
                "[[0.5, 0.5], [0.2, 0.8]]",
                "[[0.6, 0.5], [0.3, 0.7]]",
                "[[0, 1], [1, 0]]",
            ],
            "correct": 2,
            "explanation":
                "Opción C: fila 1 suma 1.1 (viola condición).",
        },
        {
            "title": "Cadena de Markov: lluvia y sol",
            "nivel": "intermedio",
            "theory":
                "Propiedad de Markov: el futuro depende solo del presente.\n"
                "  P(Xₙ₊₁=j | Xₙ=i, …, X₀) = P(Xₙ₊₁=j | Xₙ=i) = Pᵢⱼ.\n\n"
                "P matriz de transición (estocástica).\n"
                "Distribución tras n pasos: πₙ = π₀·Pⁿ.",
            "example":
                "Estados: 0=sol, 1=lluvia.\n"
                "P = [[0.8, 0.2],[0.5, 0.5]].\n"
                "Hoy sol: π₀ = (1, 0).\n"
                "Mañana: π₁ = (0.8, 0.2).\n"
                "P² = [[0.74, 0.26],[0.65, 0.35]].\n"
                "Pasado mañana: 26% lluvia.\n"
                "Pulsa «▶ Animar» para ver una trayectoria de estados.",
            "visual": {
                "tipo": "grafo",
                "title": "Cadena de Markov: sol ⇄ lluvia",
                "nodes": [
                    {"id": "S", "pos": (110, 120), "label": "☀ Sol"},
                    {"id": "L", "pos": (310, 120), "label": "☂ Lluvia"},
                ],
                "edges": [
                    {"from": "S", "to": "L", "dir": True, "label": "0.2"},
                    {"from": "L", "to": "S", "dir": True, "label": "0.5"},
                ],
                "animate": {
                    "tipo": "markov",
                    "secuencia": ["S", "S", "S", "L", "S", "L", "L", "S"],
                },
            },
            "q_type": "mc",
            "question":
                "¿Qué info necesita una cadena de Markov para el sig. estado?",
            "options": [
                "Toda la historia desde X₀",
                "Solo el estado actual",
                "Los dos últimos",
                "Inicial y actual",
            ],
            "correct": 1,
            "explanation":
                "Definición misma de propiedad de Markov.",
        },
        {
            "title": "Distribución estacionaria",
            "nivel": "experto",
            "theory":
                "π estacionaria si π·P = π y ∑πᵢ=1, πᵢ≥0.\n"
                "Si la cadena es irreducible y aperiódica:\n"
                "  π es única.\n"
                "  πᵢ ≈ fracción de tiempo a largo plazo en estado i.",
            "example":
                "Sol/lluvia, P = [[0.8,0.2],[0.5,0.5]].\n"
                "Sistema π·P = π:\n"
                "  π₀ = 0.8π₀ + 0.5π₁ ⇒ 0.2π₀ = 0.5π₁ ⇒ π₁ = 0.4π₀\n"
                "  π₀ + π₁ = 1 ⇒ π₀ ≈ 0.714, π₁ ≈ 0.286.\n"
                "Largo plazo: ≈71% sol, 29% lluvia.",
            "q_type": "tf",
            "question":
                "Si π·P = π, entonces π·Pⁿ = π para todo n.",
            "options": ["Verdadero", "Falso"],
            "correct": 0,
            "explanation":
                "Aplicando P n veces siempre se obtiene π.",
        },
        {
            "title": "Procesos gaussianos",
            "nivel": "intermedio",
            "theory":
                "Proceso gaussiano (GP): {Xₜ} tal que cualquier vector\n"
                "(Xₜ₁,…,Xₜₖ) sigue normal multivariante.\n\n"
                "Caracterizado por:\n"
                "  • m(t) = E[Xₜ] (media)\n"
                "  • k(s,t) = Cov(Xₛ, Xₜ) (kernel)\n\n"
                "Usos en IA: regresión bayesiana, optimización\n"
                "bayesiana de hiperparámetros, series temporales suaves.\n\n"
                "Kernel típico (RBF): k(s,t) = exp(-(s-t)²/(2ℓ²)).",
            "example":
                "GP con m=0 y kernel RBF (ℓ=1).\n"
                "Para t = (-1, 0, 1):\n"
                "  K = [[1.000, 0.607, 0.135],\n"
                "       [0.607, 1.000, 0.607],\n"
                "       [0.135, 0.607, 1.000]]\n"
                "Puntos cercanos tienen alta covarianza → función suave.",
            "q_type": "mc",
            "question":
                "Un proceso gaussiano queda caracterizado por:",
            "options": [
                "Solo la media m(t)",
                "Solo el kernel k(s,t)",
                "La media m(t) y el kernel k(s,t)",
                "El número de puntos muestreados",
            ],
            "correct": 2,
            "explanation":
                "Ambos: m y k determinan todo el GP.",
        },
    ],

    # =================================================================
    "4.4  TensorFlow Probability": [
        {
            "title": "Introducción a TensorFlow Probability",
            "nivel": "básico",
            "theory":
                "TFP: librería sobre TensorFlow para modelos\n"
                "probabilísticos. Componentes:\n"
                "  • tfp.distributions: distribuciones\n"
                "  • bijectores (cambios de variable)\n"
                "  • tfp.mcmc: muestreo MCMC\n"
                "  • tfp.vi: inferencia variacional\n"
                "  • capas bayesianas\n\n"
                "Soporta autograd (gradientes automáticos) → MLE, MAP, VI.",
            "example":
                "  import tensorflow_probability as tfp\n"
                "  tfd = tfp.distributions\n"
                "  d = tfd.Normal(loc=0., scale=1.)\n"
                "  d.prob(0.0)      # ≈ 0.3989\n"
                "  d.cdf(1.96)      # ≈ 0.975\n"
                "  d.sample(5)      # 5 muestras N(0,1)",
            "q_type": "tf",
            "question":
                "TFP se usa para modelos probabilísticos sobre TensorFlow.",
            "options": ["Verdadero", "Falso"],
            "correct": 0,
            "explanation":
                "Esa es la razón de existir de tfp.",
        },
        {
            "title": "Distribuciones: tfp.distributions.Normal",
            "nivel": "básico",
            "theory":
                "  d = tfd.Normal(loc=μ, scale=σ)\n"
                "  scale es σ (NO σ²).\n\n"
                "Métodos:\n"
                "  d.sample(n), d.prob(x), d.log_prob(x),\n"
                "  d.cdf(x), d.mean(), d.stddev().\n\n"
                "Soporta batches (loc/scale como tensores).\n"
                "Otras: Bernoulli, Categorical, Beta, Gamma, MVNormal.",
            "example":
                "  d = tfd.Normal(loc=2.0, scale=0.5)\n"
                "  d.mean()       # 2.0\n"
                "  d.stddev()     # 0.5\n"
                "  d.cdf(2.0)     # 0.5\n"
                "  d2 = tfd.Normal([0., 5.], [1., 2.])  # batch de 2\n"
                "Gráfica abajo: densidad de N(2.0, 0.5).",
            "visual": {
                "tipo": "distribucion",
                "tipo_distrib": "curva",
                "expr": lambda x: math.exp(-((x - 2.0) ** 2) / (2 * 0.25)) / (0.5 * math.sqrt(2 * math.pi)),
                "xrange": (0, 4),
                "ymax": 0.9,
                "title": "Densidad N(μ=2, σ=0.5)",
            },
            "q_type": "mc",
            "question":
                "En tfd.Normal(loc=3., scale=2.), ¿qué es scale?",
            "options": [
                "La varianza σ²",
                "La desviación estándar σ",
                "La media μ",
                "Un factor arbitrario",
            ],
            "correct": 1,
            "explanation":
                "scale es σ; la varianza sería σ² = scale².",
        },
        {
            "title": "Muestreo de Monte Carlo",
            "nivel": "intermedio",
            "theory":
                "Aproximar esperanzas con muestras:\n"
                "  E[g(X)] ≈ (1/N) ∑ g(xᵢ)\n"
                "Convergencia por LGN. Error decrece como 1/√N\n"
                "(independiente de la dimensión).",
            "example":
                "Estimar P(Z>1.96) con Z ~ N(0,1) (real ≈ 0.025):\n"
                "  d = tfd.Normal(0., 1.)\n"
                "  x = d.sample(100_000)\n"
                "  p̂ = tf.reduce_mean(tf.cast(x > 1.96, tf.float32))\n"
                "  # p̂ ≈ 0.0248",
            "q_type": "mc",
            "question":
                "Si Monte Carlo usa N muestras, ¿cómo decrece el error?",
            "options": [
                "Como 1/N",
                "Como 1/√N",
                "Como 1/N²",
                "No depende de N",
            ],
            "correct": 1,
            "explanation":
                "Error estándar = σ/√N por TCL.",
        },
        {
            "title": "Inferencia variacional",
            "nivel": "experto",
            "theory":
                "VI: aproximar posterior intratable p(θ|x) por una\n"
                "distribución sencilla q_φ(θ).\n\n"
                "Minimizar KL(q ‖ p), equivalente a maximizar ELBO:\n"
                "  ELBO(φ) = E_q[log p(x,θ) - log q_φ(θ)] ≤ log p(x).\n\n"
                "Convierte la inferencia en OPTIMIZACIÓN (gradient).\n"
                "Escala bien a datos grandes. Implementado en tfp.vi.",
            "example":
                "Pseudocódigo:\n"
                "  q = tfd.Normal(loc=tf.Variable(0.),\n"
                "                 scale=tfp.util.TransformedVariable(\n"
                "                       1., tfb.Softplus()))\n"
                "  def neg_elbo():\n"
                "      θ = q.sample(64)\n"
                "      return -tf.reduce_mean(log_joint(θ,data)\n"
                "                              - q.log_prob(θ))\n"
                "  opt = tf.optimizers.Adam(0.05)\n"
                "  for _ in range(1000):\n"
                "      opt.minimize(neg_elbo, q.trainable_variables)",
            "q_type": "mc",
            "question":
                "En VI, ¿qué cantidad se maximiza?",
            "options": [
                "La divergencia KL exacta",
                "La verosimilitud p(x|θ)",
                "El ELBO (Evidence Lower Bound)",
                "El error cuadrático",
            ],
            "correct": 2,
            "explanation":
                "Maximizar ELBO equivale a minimizar KL(q‖p).",
        },
    ],

    # =================================================================
    "🤖  Aplicaciones a IA (extensión)": [
        {
            "title": "Regresión lineal y MSE",
            "nivel": "intermedio",
            "theory":
                "Regresión lineal: y = w·x + b.\n"
                "Error Cuadrático Medio (MSE):\n"
                "  MSE(w,b) = (1/n)∑(yᵢ - (w·xᵢ+b))²\n\n"
                "MSE es PARÁBOLA en w y b → mínimo único.\n"
                "Derivamos:\n"
                "  ∂MSE/∂w = -(2/n)∑ xᵢ(yᵢ-(wxᵢ+b))\n"
                "  ∂MSE/∂b = -(2/n)∑(yᵢ-(wxᵢ+b))\n\n"
                "Si los puntos están alineados → MSE = 0.",
            "example":
                "Datos: (1,2), (2,4), (3,6). Recta y=2x:\n"
                "  Errores: 0, 0, 0. MSE = 0.\n\n"
                "Recta y=x:\n"
                "  Errores: 1, 2, 3. MSE = (1+4+9)/3 ≈ 4.67.",
            "q_type": "mc",
            "question":
                "Si los puntos no están alineados, ¿qué pasa con el MSE mínimo?",
            "options": [
                "Siempre exactamente 0",
                "Estrictamente positivo (mide el error residual)",
                "Negativo porque hay errores",
                "No existe",
            ],
            "correct": 1,
            "explanation":
                "Cada término (yᵢ-ŷᵢ)² ≥ 0, MSE ≥ 0.\n"
                "Solo vale 0 si todos los puntos están en la recta.",
        },
        {
            "title": "Naive Bayes: filtro de spam",
            "nivel": "intermedio",
            "theory":
                "Naive Bayes aplica Bayes para clasificar texto:\n"
                "  P(spam|palabra) = P(palabra|spam)·P(spam) / P(palabra)\n\n"
                "P(palabra) por prob. total:\n"
                "  P(palabra) = P(palabra|spam)·P(spam) +\n"
                "               P(palabra|normal)·P(normal)\n\n"
                "'Naive' = asume independencia entre palabras dada la clase.\n"
                "En la práctica: log-verosimilitudes para evitar productos pequeños.",
            "example":
                "P(spam)=0.40, P(normal)=0.60.\n"
                "P('ofertas'|spam)=0.30, P('ofertas'|normal)=0.05.\n\n"
                "Numerador: 0.30·0.40 = 0.12\n"
                "Denominador: 0.12 + 0.05·0.60 = 0.15\n"
                "P(spam|'ofertas') = 0.12/0.15 = 0.80.",
            "q_type": "mc",
            "question":
                "En el ejemplo, ¿P(spam | 'ofertas')?",
            "options": ["0.30", "0.40", "0.60", "0.80"],
            "correct": 3,
            "explanation":
                "Bayes: (0.30·0.40)/(0.15) = 0.80.",
        },
        {
            "title": "PCA vía SVD",
            "nivel": "experto",
            "theory":
                "PCA busca direcciones de máxima varianza para reducir\n"
                "dimensionalidad.\n\n"
                "X centrada (n×d): X = U·Σ·Vᵀ (SVD).\n"
                "Columnas de V = direcciones principales.\n"
                "var_i = σᵢ²/(n-1) = varianza por componente.\n\n"
                "Reducir a k dims: X_red = X·V[:, :k].\n"
                "Fracción de varianza retenida = (σ₁²+…+σₖ²)/(σ₁²+…+σd²).",
            "example":
                "X = [[3,0,0],[0,2,0]] (2 muestras, 3 features).\n"
                "  σ₁=3, σ₂=2 (la 3ª columna no aporta).\n"
                "  Varianza total ∝ 9+4 = 13.\n"
                "  Con 1 componente: 9/13 ≈ 69%.\n"
                "  Con 2: 13/13 = 100%.",
            "q_type": "mc",
            "question":
                "En SVD aplicado a PCA, los σᵢ representan:",
            "options": [
                "Medias de cada variable",
                "Correlaciones entre features",
                "Magnitud de varianza en cada dirección principal",
                "Número de muestras por clase",
            ],
            "correct": 2,
            "explanation":
                "σᵢ²/(n-1) = varianza capturada por la i-ésima componente.",
        },
        {
            "title": "Softmax + entropía cruzada",
            "nivel": "intermedio",
            "theory":
                "Clasificación multiclase. Logits z = (z₁,…,zK).\n"
                "  softmax(z)ᵢ = exp(zᵢ) / ∑ⱼ exp(zⱼ)\n"
                "Convierte logits en probabilidades (suman 1).\n\n"
                "Entropía cruzada:\n"
                "  H(y, p) = -∑ yᵢ·log(pᵢ)\n"
                "Para y one-hot con clase c: H = -log(p_c).\n"
                "p_c → 1: H → 0. p_c → 0: H → ∞.\n\n"
                "El gradiente softmax+CE se simplifica a (p - y).",
            "example":
                "z = [2, 1, 0.1].\n"
                "  exp = [7.389, 2.718, 1.105], suma = 11.212.\n"
                "  softmax ≈ [0.659, 0.242, 0.099].\n\n"
                "Si y = [1, 0, 0]:\n"
                "  CE = -log(0.659) ≈ 0.417.",
            "q_type": "mc",
            "question":
                "Softmax da 0.66 para la clase correcta. ¿CE aprox?",
            "options": ["0.00", "0.42", "1.00", "2.30"],
            "correct": 1,
            "explanation":
                "CE = -log(0.66) ≈ 0.42.",
            "simple_explanation":
                "SOFTMAX en 3 pasos:\n"
                "  1) Exponencial de cada logit:  eᶻⁱ  (siempre > 0).\n"
                "  2) Suma de los exponenciales: S = Σ eᶻⁱ.\n"
                "  3) Divide cada uno por S: pᵢ = eᶻⁱ / S.\n"
                "  → Vector de probabilidades que SUMAN 1.\n\n"
                "ENTROPÍA CRUZADA (caso simple, etiqueta one-hot):\n"
                "  Si la clase correcta es c y la prob predicha es pc:\n"
                "       CE = -log(pc).\n"
                "  pc cerca de 1 → CE ≈ 0  (predicción perfecta).\n"
                "  pc cerca de 0 → CE muy grande  (predicción mala).\n\n"
                "REGLA RÁPIDA del log:\n"
                "  -log(0.99) ≈ 0.01  (casi sin pérdida)\n"
                "  -log(0.50) ≈ 0.69\n"
                "  -log(0.10) ≈ 2.30  (mucha pérdida)\n"
                "  -log(0.01) ≈ 4.60  (catastrófica)",
            "similar_examples": [
                "Logits z = [1, 1, 1] (todos iguales):\n"
                "  exp = [2.72, 2.72, 2.72], S = 8.15.\n"
                "  softmax = [0.33, 0.33, 0.33] (uniforme, no sabe nada).\n"
                "  Si la verdadera es la 1ª: CE = -log(0.33) ≈ 1.10.",

                "Logits z = [5, 0, 0]:\n"
                "  exp ≈ [148.4, 1, 1], S ≈ 150.4.\n"
                "  softmax ≈ [0.987, 0.007, 0.007] (muy seguro de la 1ª).\n"
                "  Si la verdadera es la 1ª: CE = -log(0.987) ≈ 0.013.\n"
                "  Si la verdadera es la 2ª: CE = -log(0.007) ≈ 4.96.\n"
                "Estar 'muy seguro y equivocarse' duele MUCHO.",

                "¿Por qué exp() en softmax?\n"
                "  Porque convierte CUALQUIER número real en uno POSITIVO,\n"
                "  y amplifica las diferencias. z=[2,1] da ≈[0.73, 0.27],\n"
                "  no [2/3, 1/3].\n"
                "  La 'temperatura' T en softmax(z/T) controla qué tan\n"
                "  'segura' es la distribución (T pequeña → más extremo).",

                "Conexión con MLE:\n"
                "  Minimizar CE de la clase correcta es EQUIVALENTE\n"
                "  a maximizar log p(y|x) (verosimilitud). Por eso es\n"
                "  el coste estándar de clasificación.",
            ],
        },
        {
            "title": "Markov para generación de texto",
            "nivel": "intermedio",
            "theory":
                "Cadena de Markov modela secuencias:\n"
                "  P(w_{t+1} | w_t, w_{t-1}, …) = P(w_{t+1} | w_t).\n\n"
                "Matriz de transición P (filas suman 1).\n"
                "Generar texto: muestrear según fila actual.\n\n"
                "P(frase w1→w2→w3) = P(w1)·P(w2|w1)·P(w3|w2).\n"
                "LLMs son extensiones (condicionan en TODO el contexto).",
            "example":
                "Vocabulario: {gato, come, pescado}.\n"
                "P[gato] = [0.0, 0.9, 0.1]\n"
                "P[come] = [0.1, 0.0, 0.9]\n"
                "P[pescado] = [0.5, 0.4, 0.1]\n\n"
                "P('gato come pescado'|start='gato') = 0.9·0.9 = 0.81.\n"
                "P('gato pescado come') = 0.1·0.4 = 0.04.",
            "q_type": "mc",
            "question":
                "¿Cuál frase es más probable empezando en 'gato'?",
            "options": [
                "gato gato come",
                "gato come pescado",
                "gato pescado come",
                "gato pescado pescado",
            ],
            "correct": 1,
            "explanation":
                "0.9·0.9 = 0.81, mucho mayor que las otras.",
        },
        {
            "title": "Red neuronal: composición y cadena",
            "nivel": "experto",
            "theory":
                "Red de 2 capas es composición de funciones:\n"
                "  h = σ(W₁·x + b₁)\n"
                "  ŷ = W₂·h + b₂\n\n"
                "Para entrenar: ∂L/∂W₁ por regla de la cadena:\n"
                "  ∂L/∂W₁ = ∂L/∂ŷ · ∂ŷ/∂h · ∂h/∂z₁ · ∂z₁/∂W₁\n\n"
                "Backpropagation = recorrer el GRAFO de cómputo hacia\n"
                "atrás multiplicando derivadas locales.",
            "example":
                "Red 1D: z₁=w₁·x+b₁, h=σ(z₁), ŷ=w₂·h+b₂, L=(ŷ-y)².\n"
                "Con x=1, w₁=2, b₁=0, w₂=3, b₂=0, σ=id, y=10:\n"
                "  z₁=2, h=2, ŷ=6, L=16.\n"
                "  ∂L/∂ŷ = -8, ∂ŷ/∂h = 3, ∂h/∂z₁ = 1, ∂z₁/∂w₁ = 1.\n"
                "  ∂L/∂w₁ = -8·3·1·1 = -24.",
            "q_type": "mc",
            "question":
                "Para ∂L/∂W₁ en red de 2 capas, ¿qué herramienta es esencial?",
            "options": [
                "Teorema de Bayes",
                "Regla de la cadena del cálculo",
                "Descomposición SVD",
                "Teorema central del límite",
            ],
            "correct": 1,
            "explanation":
                "Backprop = regla de la cadena sobre el grafo.",
        },
        {
            "title": "Descenso de gradiente: el learning rate",
            "nivel": "experto",
            "theory":
                "w_{t+1} = w_t - η·∇L(w_t)\n\n"
                "η es el LEARNING RATE:\n"
                "  • muy pequeño → converge lentísimo.\n"
                "  • adecuado    → converge al mínimo.\n"
                "  • muy grande  → oscila o DIVERGE.\n\n"
                "Para L(w) = w²:\n"
                "  w_{t+1} = w_t·(1-2η).\n"
                "Converge si |1-2η| < 1 ⇔ 0 < η < 1.",
            "example":
                "L(w)=w², ∇L=2w. w₀=4.\n\n"
                "η=0.5: w₁ = 4 - 0.5·8 = 0 (¡un paso!).\n\n"
                "η=0.25: w₁=2, w₂=1, w₃=0.5 (converge).\n\n"
                "η=2.0:  w₁=-12, w₂=36, w₃=-108 (DIVERGE).",
            "q_type": "mc",
            "question":
                "Si η es demasiado grande, ¿qué le pasa al GD?",
            "options": [
                "Converge más rápido al mínimo",
                "Se queda estancado en el punto inicial",
                "Oscila o diverge alejándose del mínimo",
                "Encuentra el mínimo exacto",
            ],
            "correct": 2,
            "explanation":
                "Pasos demasiado grandes sobrepasan el mínimo;\n"
                "en el peor caso los valores explotan.",
        },
    ],

    # =================================================================
    "📚  Metodología": [

        {
            "title": "Cómo usar este curso (resumen)",
            "theory":
                "Basado en 4 artículos científicos (ver\n"
                "metodologia_estudio.md en la misma carpeta) hay 6\n"
                "prácticas con evidencia robusta para aprender\n"
                "matemática avanzada como la de este máster.\n\n"
                "Cada lección de esta sección te explica UNA práctica\n"
                "y te pregunta cómo aplicarla en tu rutina.\n\n"
                "FUENTES:\n"
                "  • Brunmair & Richter (2019) — interleaving\n"
                "  • Sweller, van Merriënboer & Paas (2019) — CLT\n"
                "  • Hodds, Alcock & Inglis (2014) — self-explanation\n"
                "  • Freeman et al. (2014) — active learning",
            "example":
                "💡 Regla de oro:\n"
                "   Si no puedes EJECUTARLO en Python,\n"
                "   no lo entendiste.\n"
                "   Si no puedes EXPLICÁRSELO a alguien,\n"
                "   tampoco.",
            "q_type": "info",
            "question": "",
            "options": [],
            "correct": None,
            "explanation": "",
        },

        {
            "title": "Práctica #1 — Worked examples PRIMERO",
            "theory":
                "Sweller et al. (2019) — Worked Example Effect.\n\n"
                "Para un PRINCIPIANTE en un tema, estudiar 2-3 ejemplos\n"
                "completamente RESUELTOS enseña MÁS que intentar\n"
                "resolver problemas tú solo desde cero.\n\n"
                "Por qué: cuando intentas resolver sin saber, tu memoria\n"
                "de trabajo se gasta 'buscando' en vez de aprender el\n"
                "patrón de solución.\n\n"
                "REGLA: para cada concepto NUEVO del manual:\n"
                "  1) Lee 2-3 ejemplos resueltos COMPLETOS.\n"
                "  2) Reprodúcelos en papel o Python SIN copiar.\n"
                "  3) SOLO ENTONCES haz ejercicios propios.\n\n"
                "OJO (expertise reversal): cuando ya dominas el tema,\n"
                "los worked examples DEJAN de servir. Pasa a ejercicios.",
            "example":
                "Aplicado al manual VIU:\n"
                "Antes de hacer ejercicios de las leyes de Morgan,\n"
                "estudia los 5 ejemplos de simplificación que el\n"
                "manual da en la pág. 17. Solo después intenta los\n"
                "tuyos.",
            "q_type": "mc",
            "question":
                "Estás empezando un tema nuevo (ej. factorización SVD).\n"
                "¿Qué deberías hacer PRIMERO?",
            "options": [
                "Resolver 10 ejercicios para practicar mucho.",
                "Estudiar 2-3 ejemplos completamente resueltos.",
                "Memorizar la fórmula y aplicarla.",
                "Ver un video de YouTube sin pausar.",
            ],
            "correct": 1,
            "explanation":
                "Para un tema NUEVO, los worked examples son lo más\n"
                "eficaz (Sweller 2019). Resolver sin entender el patrón\n"
                "satura la memoria de trabajo y aprendes menos.",
        },

        {
            "title": "Práctica #2 — Self-explanation (las 4 preguntas)",
            "theory":
                "Hodds, Alcock & Inglis (2014) — JRME.\n\n"
                "Tamaño del efecto: d = 0.95 (ENORME) sobre comprensión\n"
                "de demostraciones matemáticas.\n\n"
                "Después de cada LÍNEA densa (teorema, definición o\n"
                "paso de un proof), hazte estas 4 preguntas en voz\n"
                "alta o por escrito:\n\n"
                "  1) ¿Entiendo las IDEAS usadas en esta línea?\n"
                "  2) ¿Por qué se usa esta idea AQUÍ y no otra?\n"
                "  3) ¿Cómo se ENLAZA con definiciones o teoremas\n"
                "     que ya conozco?\n"
                "  4) ¿Mi explicación RESPONDE a las preguntas\n"
                "     que me estaba haciendo?\n\n"
                "Una intervención de SOLO 15 MIN tiene efecto duradero.",
            "example":
                "Lo que NO sirve:\n"
                "  ✗ Parafrasear: 'p y q tienen que ser enteros'\n"
                "  ✗ Monitorear : 'OK, esto lo entiendo'\n\n"
                "Lo que SÍ sirve:\n"
                "  ✓ 'p=314 y q=100 porque son enteros y p/q=3.14.\n"
                "    Esto CUMPLE la DEFINICIÓN de número racional,\n"
                "    por eso completa la prueba.'",
            "q_type": "mc",
            "question":
                "¿Cuál es una self-explanation VÁLIDA tras leer\n"
                "'¬(p ∧ q) ≡ ¬p ∨ ¬q'?",
            "options": [
                "'Vale, la entiendo.'",
                "'Es lo mismo que decir: no es cierto que p y q.'",
                "'Por Morgan, al negar el AND se vuelve OR y cada parte\n"
                "se niega — es coherente con que negar 'y' debería dar\n"
                "'al menos uno no'.'",
                "'Hay que memorizarla así tal cual.'",
            ],
            "correct": 2,
            "explanation":
                "Solo la tercera CONECTA con el porqué y otras ideas\n"
                "previas (Morgan, semántica de AND/OR). Las otras son\n"
                "monitoreo, paráfrasis o memorización.",
        },

        {
            "title": "Práctica #3 — Active learning (producir, no consumir)",
            "theory":
                "Freeman et al. (2014) — PNAS, meta-análisis de 225\n"
                "estudios en STEM universitario.\n\n"
                "Resultados:\n"
                "  • Clase magistral pasiva: 33.8 % suspende\n"
                "  • Aprendizaje activo    : 21.8 % suspende\n"
                "  • Probabilidad de suspender: 1.5× MÁS en pasivo\n\n"
                "REGLA: en cada sesión de estudio DEBES PRODUCIR algo.\n"
                "Producir = resolver, escribir, codificar, explicar.\n"
                "NO cuenta: solo leer, solo ver video, solo subrayar.\n\n"
                "Para tu caso: usa este script. Cada lección que ves\n"
                "te obliga a contestar. Eso ya es active learning.",
            "example":
                "Sustituye:\n"
                "  'Ver video' → 'Ver, pausar cada 2 min, resumir'\n"
                "  'Leer manual' → 'Leer + reproducir el ejemplo en .py'\n"
                "  'Subrayar' → 'Reescribir con tus palabras'",
            "q_type": "tf",
            "question":
                "Es más eficaz LEER el manual 3 veces que LEERLO 1 vez\n"
                "y luego resolver 5 ejercicios.",
            "options": ["Verdadero", "Falso"],
            "correct": 1,
            "explanation":
                "FALSO. Releer es pasivo. Resolver es activo y reduce\n"
                "la probabilidad de suspender significativamente\n"
                "(Freeman 2014).",
        },

        {
            "title": "Práctica #4 — Interleaving (mezclar temas similares)",
            "theory":
                "Brunmair & Richter (2019) — Psychological Bulletin.\n\n"
                "Meta-análisis de 59 estudios: mezclar ejemplos de\n"
                "varios temas en una misma sesión funciona mejor que\n"
                "estudiarlos en bloques separados.\n\n"
                "Para matemática: efecto g = 0.34 (pequeño pero +).\n"
                "El efecto AUMENTA cuando:\n"
                "  • Los temas son PARECIDOS entre sí (se confunden).\n"
                "  • El material es COMPLEJO.\n\n"
                "¡OJO! Para VOCABULARIO (definiciones, símbolos\n"
                "nuevos) el bloqueo es MEJOR (g = -0.39). No mezcles\n"
                "al memorizar notación nueva.",
            "example":
                "Aplicado al manual VIU:\n"
                "  ✗ MALO  : 20 ejercicios seguidos de 1.1 (AND/OR/NOT)\n"
                "  ✓ BUENO : 5 ejercicios mezclando AND/OR/NOT + Morgan\n"
                "             + tabla de verdad de implicación + Boole\n\n"
                "Cuando llegues a 2.5 (factorizaciones): mezcla LU +\n"
                "Cholesky + QR. Te obliga a IDENTIFICAR cuál aplicar.",
            "q_type": "mc",
            "question":
                "Estás preparando 30 ejercicios para esta semana. Tres\n"
                "temas: conjunción, disyunción, implicación.\n"
                "¿Qué orden es MEJOR?",
            "options": [
                "10 de conjunción, 10 de disyunción, 10 de implicación\n"
                "  (en bloques).",
                "Aleatorizar los 30 mezclando los tres tipos\n"
                "  (interleaving).",
                "Solo los 10 más difíciles para optimizar el tiempo.",
                "Releer la teoría 30 veces sin hacer ejercicios.",
            ],
            "correct": 1,
            "explanation":
                "Los tres son conectores SIMILARES y se confunden.\n"
                "Mezclarlos te obliga a IDENTIFICAR cuál aplicar,\n"
                "que es la habilidad real que te van a evaluar.",
        },

        {
            "title": "Práctica #5 — Aislar antes de integrar",
            "theory":
                "Sweller et al. (2019) — Isolated Elements Effect.\n\n"
                "Cuando un tema tiene MUCHOS elementos que interactúan\n"
                "(backpropagation, SVD, redes neuronales completas),\n"
                "presentarlos TODOS A LA VEZ satura la memoria de\n"
                "trabajo.\n\n"
                "SOLUCIÓN: estudia cada elemento POR SEPARADO primero,\n"
                "luego intégralos.",
            "example":
                "Para BACKPROPAGATION (Cap. 3):\n"
                "  Día 1: derivada parcial (sola)\n"
                "  Día 2: regla de la cadena (sola)\n"
                "  Día 3: gradiente (solo)\n"
                "  Día 4: combinarlos en backprop completo\n\n"
                "No intentes entender backprop el Día 1. Saturarás\n"
                "la memoria de trabajo y NO aprenderás nada.",
            "q_type": "tf",
            "question":
                "Para un tema complejo (ej. SVD), conviene estudiar\n"
                "todos los componentes JUNTOS desde el principio.",
            "options": ["Verdadero", "Falso"],
            "correct": 1,
            "explanation":
                "FALSO. Hay que AISLAR cada elemento primero (valores\n"
                "propios, ortogonalidad, descomposición) y luego\n"
                "integrar. El cerebro no procesa muchos elementos\n"
                "interactuando a la vez.",
        },

        {
            "title": "Práctica #6 — Fading del andamiaje",
            "theory":
                "Sweller et al. (2019) — Guidance-Fading Effect +\n"
                "Expertise Reversal Effect.\n\n"
                "Lo que te ayuda CUANDO EMPIEZAS un tema (worked\n"
                "examples, instrucciones detalladas, andamiaje fuerte)\n"
                "EMPIEZA A FRENARTE cuando ya dominas el tema.\n\n"
                "Solución: PROGRESIÓN en 3 etapas para cada nuevo\n"
                "método:\n"
                "  1) Ejemplo COMPLETAMENTE resuelto.\n"
                "  2) Ejemplo con HUECOS (rellenas tú la mitad).\n"
                "  3) Problema desde CERO (sin ayuda).\n\n"
                "REGLA: si un método dejó de costarte, SÚBETE LA\n"
                "DIFICULTAD. Si te sigue costando, vuelve un paso.",
            "example":
                "Aplicado a límites (Cap. 3):\n"
                "  Semana 1: 5 worked examples completos.\n"
                "  Semana 2: 5 ejercicios con la mitad resuelta.\n"
                "  Semana 3: 5 ejercicios sin pista.\n"
                "  Semana 4: ejercicios mezclados (interleaving) con\n"
                "             continuidad y derivadas.",
            "q_type": "mc",
            "question":
                "Llevas 3 semanas con derivadas y los ejercicios ya te\n"
                "salen 'demasiado fáciles'. ¿Qué haces?",
            "options": [
                "Sigue con los mismos para asegurarte.",
                "Pasa a ejercicios con menos andamiaje o más difíciles.",
                "Empieza un tema completamente nuevo y olvida derivadas.",
                "Vuelve a leer la teoría desde cero.",
            ],
            "correct": 1,
            "explanation":
                "Expertise reversal: lo que te ayudaba al principio\n"
                "(repetición, andamiaje) ahora te frena. Súbete el\n"
                "nivel — interleaving con otros temas o problemas\n"
                "más complejos.",
        },

        {
            "title": "Tu plan semanal (resumen ejecutable)",
            "theory":
                "Para ~10-12 h/semana en esta asignatura, divide en\n"
                "5 sesiones de ~2 h. Cada sesión tiene esta estructura\n"
                "basada en TODAS las prácticas anteriores:\n\n"
                "  Bloque A (20 min) — INPUT GUIADO\n"
                "       Lee con self-explanation (4 preguntas).\n\n"
                "  Bloque B (30 min) — WORKED EXAMPLES\n"
                "       Estudia y reproduce 2-3 ejemplos resueltos.\n\n"
                "  Bloque C (40 min) — INTERLEAVING ACTIVO\n"
                "       4-6 ejercicios MEZCLADOS, no en bloques.\n\n"
                "  Bloque D (20 min) — CODIFICAR\n"
                "       Implementa el concepto en Python.\n\n"
                "  Bloque E (10 min) — RETRIEVAL\n"
                "       Cierra todo. Recuerda lo aprendido por escrito.",
            "example":
                "EJEMPLO real para la próxima sesión (Cap. 1.1-1.2):\n\n"
                "  A: lee 1.1 con las 4 preguntas.\n"
                "  B: estudia los 5 ejemplos de simplificación.\n"
                "  C: 5 ejercicios mezclando ∧, ∨, →, Morgan.\n"
                "  D: ejecuta este script (sección 1.1) y modifica\n"
                "      una pregunta para añadir otra tuya.\n"
                "  E: cierra el portátil y escribe en una hoja qué\n"
                "      es Morgan generalizado y cuándo se aplica.",
            "q_type": "info",
            "question": "",
            "options": [],
            "correct": None,
            "explanation": "",
        },
    ],
}


# =====================================================================
#  INTERFAZ GRÁFICA (Tkinter)
# =====================================================================

COLOR_BG       = "#0f1419"
COLOR_PANEL    = "#1a212b"
COLOR_ACCENT   = "#39c5cf"
COLOR_ACCENT2  = "#a371f7"   # color para el modo mezclado
COLOR_OK       = "#3fb950"
COLOR_BAD      = "#f85149"
COLOR_THEORY   = "#15202b"
COLOR_EXAMPLE  = "#102530"   # fondo del ejemplo resuelto
COLOR_BTNINAC  = "#2a3441"
COLOR_TEXT     = "#f0f6fc"
COLOR_TEXT2    = "#8b98a5"   # texto secundario


# --- Las 4 preguntas de SELF-EXPLANATION (Hodds, Alcock & Inglis 2014) -----
# Tamaño de efecto reportado: d = 0.95 sobre comprensión de demostraciones
AUTOEXPLICACION_4Q = [
    "1. ¿Entiendo las IDEAS usadas en esta lección?",
    "2. ¿Por qué se usa esta idea AQUÍ y no otra?",
    "3. ¿Cómo se ENLAZA con definiciones o teoremas que ya conozco?",
    "4. ¿Mi explicación RESPONDE a las preguntas que me estaba haciendo?",
]
AUTOEXPLICACION_INFO = (
    "💡 Pasa por estas 4 preguntas DESPUÉS de leer la teoría.\n"
    "    Solo el monitoreo ('OK, lo entiendo') o el parafraseo no sirven —\n"
    "    necesitas conectar con DEFINICIONES o ideas previas.\n\n"
    "Fuente: Hodds, Alcock & Inglis (2014).\n"
    "Comprobado en 3 experimentos (d = 0.95 sobre comprensión de proofs)."
)


# =====================================================================
#  DIBUJO DE PUERTAS LÓGICAS (Canvas, formas IEEE estándar)
# =====================================================================
#
# Cada función dibuja UNA puerta en la posición (x, y), donde (x, y)
# es la esquina superior izquierda del CUERPO de la puerta. Las líneas
# de entrada/salida se extienden fuera de ese rectángulo.
#
# Retornan un dict con:
#   "inputs"   : lista de coords (x, y) de las entradas externas
#   "output"   : coord (x, y) de la salida externa
#   "body_id"  : ID del polígono principal en el canvas (para recolor)
#   "wire_ids" : lista de IDs de los segmentos internos (entradas+salida)
#                que conviene recolorear cuando llega una señal.
#
# Esto permite que el motor de animación, definido más abajo, recoloree
# los tramos con verde (=1) o rojo (=0) sin tener que volver a dibujar.

GATE_W = 70      # ancho del cuerpo de la puerta (más grande)
GATE_H = 54      # alto del cuerpo
GATE_PAD = 22    # longitud de la línea entrada/salida que sobresale
BUBBLE_R = 6     # radio del círculo de negación

# Paleta para la animación de señales (active learning visual).
COLOR_SIGNAL_HI   = "#3fb950"   # verde — señal 1
COLOR_SIGNAL_LO   = "#f85149"   # rojo  — señal 0
COLOR_SIGNAL_IDLE = "#f0f6fc"   # gris-negro — aún sin propagar
GATE_FILL_IDLE    = {
    "AND":  "#15202b", "NAND": "#15202b",
    "OR":   "#1f2a36", "NOR":  "#1f2a36",
    "XOR":  "#1f2a36", "XNOR": "#1f2a36",
    "NOT":  "#241a26",
}

# Colores por NET (cada cable se pinta según su origen, para distinguir
# claramente las conexiones). Se evitan verde/rojo, reservados para la
# animación de señales (1/0). Se reciclan si hay muchas redes.
NET_COLORS = ["#39c5cf", "#d29922", "#a371f7", "#f778ba",
              "#79c0ff", "#56d4c4", "#ff9e64", "#c9d1d9"]
COLOR_WIRE_DIM = "#39424f"   # cable atenuado al resaltar otra conexión


def _add_bubble(canvas, cx, cy, color="#c9d1d9"):
    """Dibuja el círculo de negación (bubble) en (cx, cy)."""
    return canvas.create_oval(cx - BUBBLE_R, cy - BUBBLE_R,
                              cx + BUBBLE_R, cy + BUBBLE_R,
                              fill="white", outline=color, width=2)


def _conectar_in_out(canvas, gx, gy, w, h, has_in2=True,
                     color=COLOR_SIGNAL_IDLE):
    """Dibuja las líneas estándar de entrada y devuelve
    (in1, in2, out, [line_in1_id, line_in2_id])."""
    in1 = (gx - GATE_PAD, gy + h * 0.30)
    in2 = (gx - GATE_PAD, gy + h * 0.70)
    out = (gx + w + GATE_PAD, gy + h / 2)
    ids = []
    ids.append(canvas.create_line(in1[0], in1[1], gx, in1[1],
                                  fill=color, width=2))
    if has_in2:
        ids.append(canvas.create_line(in2[0], in2[1], gx, in2[1],
                                      fill=color, width=2))
    return in1, in2, out, ids


def dibujar_AND(canvas, x, y, w=GATE_W, h=GATE_H, neg=False, etiqueta=None):
    """Puerta AND (forma D). neg=True la convierte en NAND."""
    pts = [x, y, x + w * 0.5, y]
    for i in range(0, 19):
        a = math.radians(-90 + i * 10)
        pts.extend([x + w * 0.5 + (w * 0.5) * math.cos(a),
                    y + h / 2 + (h / 2) * math.sin(a)])
    pts.extend([x + w * 0.5, y + h, x, y + h])
    body = canvas.create_polygon(
        *pts, fill=GATE_FILL_IDLE["AND"],
        outline="#c9d1d9", width=2)
    in1, in2, out, in_ids = _conectar_in_out(canvas, x, y, w, h)
    out_line_ids = []
    if neg:
        _add_bubble(canvas, x + w + BUBBLE_R, y + h / 2)
        new_out = (x + w + 2 * BUBBLE_R + GATE_PAD, y + h / 2)
        out_line_ids.append(canvas.create_line(
            x + w + 2 * BUBBLE_R, y + h / 2, new_out[0], y + h / 2,
            fill=COLOR_SIGNAL_IDLE, width=2))
        out = new_out
    canvas.create_text(x + w * 0.40, y + h / 2,
                       text="NAND" if neg else "AND",
                       font=("Consolas", 9, "bold"))
    if etiqueta:
        canvas.create_text(x + w / 2, y - 9, text=etiqueta,
                           font=("Consolas", 10, "bold"),
                           fill="#39c5cf")
    return {"inputs": [in1, in2], "output": out,
            "body_id": body, "wire_ids": in_ids + out_line_ids}


def dibujar_OR(canvas, x, y, w=GATE_W, h=GATE_H,
               neg=False, exor=False, etiqueta=None):
    """Puerta OR (forma escudo). neg→NOR. exor→XOR (añade arco)."""
    pts = [x, y]
    for t in [i / 20 for i in range(0, 21)]:
        # parte superior: curva desde (x, y) hasta (x+w, y+h/2)
        px = x + w * t
        py = y + (h / 2) * (t ** 1.8)
        pts.extend([px, py])
    pts.extend([x + w, y + h / 2])
    for t in [i / 20 for i in range(20, -1, -1)]:
        px = x + w * t
        py = y + h - (h / 2) * (t ** 1.8)
        pts.extend([px, py])
    # parte de atrás (cóncava)
    for t in [i / 8 for i in range(8, -1, -1)]:
        px = x + w * 0.10 * (1 - 4 * (t - 0.5) ** 2)
        py = y + h * t
        pts.extend([px, py])
    body = canvas.create_polygon(
        *pts, fill=GATE_FILL_IDLE["OR"],
        outline="#c9d1d9", width=2, smooth=True)
    in1, in2, out, in_ids = _conectar_in_out(canvas, x, y, w, h)
    out_line_ids = []
    if exor:
        # arco extra en la parte de atrás (XOR)
        arc_pts = []
        for t in [i / 12 for i in range(0, 13)]:
            ax = x - 5 + 9 * (1 - 4 * (t - 0.5) ** 2)
            ay = y + h * t
            arc_pts.extend([ax, ay])
        canvas.create_line(*arc_pts, fill="#c9d1d9", width=2, smooth=True)
    if neg:
        _add_bubble(canvas, x + w + BUBBLE_R, y + h / 2)
        new_out = (x + w + 2 * BUBBLE_R + GATE_PAD, y + h / 2)
        out_line_ids.append(canvas.create_line(
            x + w + 2 * BUBBLE_R, y + h / 2, new_out[0], y + h / 2,
            fill=COLOR_SIGNAL_IDLE, width=2))
        out = new_out
    label = "OR"
    if exor and neg:  label = "XNOR"
    elif exor:        label = "XOR"
    elif neg:         label = "NOR"
    canvas.create_text(x + w * 0.50, y + h / 2,
                       text=label, font=("Consolas", 9, "bold"))
    if etiqueta:
        canvas.create_text(x + w / 2, y - 9, text=etiqueta,
                           font=("Consolas", 10, "bold"),
                           fill="#39c5cf")
    return {"inputs": [in1, in2], "output": out,
            "body_id": body, "wire_ids": in_ids + out_line_ids}


def dibujar_NOT(canvas, x, y, w=GATE_W, h=GATE_H, etiqueta=None):
    """Puerta NOT (triángulo + bubble)."""
    body = canvas.create_polygon(
        x, y, x + w * 0.85, y + h / 2, x, y + h,
        fill=GATE_FILL_IDLE["NOT"], outline="#c9d1d9", width=2)
    _add_bubble(canvas, x + w * 0.85 + BUBBLE_R, y + h / 2)
    in1 = (x - GATE_PAD, y + h / 2)
    out = (x + w * 0.85 + 2 * BUBBLE_R + GATE_PAD, y + h / 2)
    in_id = canvas.create_line(in1[0], in1[1], x, in1[1],
                               fill=COLOR_SIGNAL_IDLE, width=2)
    out_id = canvas.create_line(x + w * 0.85 + 2 * BUBBLE_R, y + h / 2,
                                out[0], y + h / 2,
                                fill=COLOR_SIGNAL_IDLE, width=2)
    canvas.create_text(x + w * 0.30, y + h / 2, text="NOT",
                       font=("Consolas", 9, "bold"))
    if etiqueta:
        canvas.create_text(x + w / 2, y - 9, text=etiqueta,
                           font=("Consolas", 10, "bold"),
                           fill="#39c5cf")
    return {"inputs": [in1], "output": out,
            "body_id": body, "wire_ids": [in_id, out_id]}


# Despachador genérico
_DISPATCH_PUERTA = {
    "AND":  lambda c, x, y, et=None: dibujar_AND(c, x, y, neg=False, etiqueta=et),
    "OR":   lambda c, x, y, et=None: dibujar_OR (c, x, y, neg=False, exor=False, etiqueta=et),
    "NOT":  lambda c, x, y, et=None: dibujar_NOT(c, x, y, etiqueta=et),
    "NAND": lambda c, x, y, et=None: dibujar_AND(c, x, y, neg=True, etiqueta=et),
    "NOR":  lambda c, x, y, et=None: dibujar_OR (c, x, y, neg=True, exor=False, etiqueta=et),
    "XOR":  lambda c, x, y, et=None: dibujar_OR (c, x, y, neg=False, exor=True, etiqueta=et),
    "XNOR": lambda c, x, y, et=None: dibujar_OR (c, x, y, neg=True, exor=True, etiqueta=et),
}


# Funciones lógicas (para el motor de simulación / animación)
_EVAL_PUERTA = {
    "AND":  lambda v: v[0] & v[1],
    "OR":   lambda v: v[0] | v[1],
    "NOT":  lambda v: 1 - v[0],
    "NAND": lambda v: 1 - (v[0] & v[1]),
    "NOR":  lambda v: 1 - (v[0] | v[1]),
    "XOR":  lambda v: v[0] ^ v[1],
    "XNOR": lambda v: 1 - (v[0] ^ v[1]),
}


def _color_para(valor):
    """Verde si la señal es 1, rojo si es 0."""
    return COLOR_SIGNAL_HI if valor == 1 else COLOR_SIGNAL_LO


def _fill_gate_para(valor, tipo):
    """Color de relleno suave para el cuerpo de la puerta según señal."""
    if valor is None:
        return GATE_FILL_IDLE.get(tipo, "#1a212b")
    return "#16361f" if valor == 1 else "#3a1d1d"


def dibujar_circuito(canvas, descripcion):
    """Dibuja un circuito completo y devuelve un MODELO usable por el
    animador. La forma del modelo es:

        {
          "canvas":   <ref al canvas>,
          "vars":     {nombre: {"coord": (x,y), "label_id": int,
                                "wire_ids": [...]}},
          "gates":    {id_puerta: {"type": str, "inputs": [str,...],
                                   "geom": {body_id, wire_ids,
                                            inputs, output},
                                   "wire_in_ids": [int,...],
                                   "wire_out_ids": [int,...]}},
          "eval_order": [ids en orden topológico],
          "output":   {"from": gate_id, "label_id": int,
                       "wire_ids": [...]},
          "trace_values": dict opcional con valores precargados.
        }

    Los `wire_ids` son los IDs de los segmentos del canvas que el
    animador recolorea durante la propagación de señales.
    """
    canvas.delete("all")
    gates_geom = {}     # id → geom dict
    var_outputs = {}    # nombre var → coord

    # Color por NET: cada variable y cada salida de puerta tiene su color,
    # para que las conexiones se distingan a simple vista.
    _nets = list(descripcion.get("vars", [])) + \
        [g["id"] for g in descripcion["gates"]]
    net_color = {n: NET_COLORS[i % len(NET_COLORS)]
                 for i, n in enumerate(_nets)}
    idle_color = {}     # wire_id → color en reposo (su color de net)
    net_wires = {}      # net → [wire_ids] (para resaltar al pulsar)

    # 1) Dibujar las puertas
    for g in descripcion["gates"]:
        x, y = g["pos"]
        et = g.get("etiqueta")
        geom = _DISPATCH_PUERTA[g["type"]](canvas, x, y, et)
        gates_geom[g["id"]] = geom

    # 2) Colocar variables de entrada (texto + punto de origen)
    vars_list = descripcion.get("vars", [])
    var_info = {}
    for i, var in enumerate(vars_list):
        vy = 36 + i * 38
        col = net_color.get(var, "#a371f7")
        label_id = canvas.create_text(
            18, vy, text=var, font=("Consolas", 12, "bold"),
            fill=col)
        var_outputs[var] = (32, vy)
        var_info[var] = {"coord": (32, vy), "label_id": label_id,
                          "wire_ids": [], "color": col}

    # 3) Cablear inputs → puertas con CANALES verticales distintos.
    #    Cada conexión gira en su propia columna (no se solapan los
    #    cables). Se agrupan por la x de destino y se reparten los canales
    #    en el hueco que hay justo antes de las puertas.
    gate_wire_in = {gid: [] for gid in gates_geom}

    conexiones = []   # (gid, input_name, (sx, sy), (dx, dy))
    for g in descripcion["gates"]:
        ins = gates_geom[g["id"]]["inputs"]
        for input_name, in_coord in zip(g["inputs"], ins):
            if input_name in gates_geom:
                src_out = gates_geom[input_name]["output"]
            elif input_name in var_outputs:
                src_out = var_outputs[input_name]
            else:
                continue
            conexiones.append((g["id"], input_name, src_out, in_coord))

    # Agrupar por x de destino y asignar un canal por conexión.
    grupos = {}
    for c in conexiones:
        grupos.setdefault(round(c[3][0]), []).append(c)

    canal = {}   # id(conexión) → x del canal vertical
    for dx_key, grupo in grupos.items():
        # ordenar por y de origen → abanico ordenado, menos cruces
        orden = sorted(range(len(grupo)), key=lambda k: grupo[k][2][1])
        left = max(c[2][0] for c in grupo) + 12
        right = dx_key - 10
        if right - left < 6 * len(grupo):     # hueco estrecho → ensanchar
            left = min(c[2][0] for c in grupo) + 14
        n = len(grupo)
        for rank, k in enumerate(orden):
            if right > left:
                canal[id(grupo[k])] = left + (rank + 1) * (right - left) / (n + 1)
            else:
                canal[id(grupo[k])] = grupo[k][3][0] - 12

    # fan-out: cuántas entradas alimenta cada origen (para los nodos)
    from_count = {}
    for c in conexiones:
        from_count[c[1]] = from_count.get(c[1], 0) + 1
    drawn_junction = set()

    for c in conexiones:
        gid, input_name, (sx, sy), (dx, dy) = c
        col = net_color.get(input_name, COLOR_SIGNAL_IDLE)
        cx = canal.get(id(c), (sx + dx) / 2)
        wid = canvas.create_line(sx, sy, cx, sy, cx, dy, dx, dy,
                                 fill=col, width=2)
        idle_color[wid] = col
        net_wires.setdefault(input_name, []).append(wid)
        gate_wire_in[gid].append({"src": input_name, "id": wid})
        if input_name in var_info:
            var_info[input_name]["wire_ids"].append(wid)
        # punto en el pin de entrada (muestra el color de quien lo alimenta)
        canvas.create_oval(dx - 3, dy - 3, dx + 3, dy + 3,
                           fill=col, outline=col)
        # nodo de bifurcación en el origen si esa red se reparte (≥2 destinos)
        if from_count.get(input_name, 0) >= 2 and input_name not in drawn_junction:
            canvas.create_oval(sx - 4, sy - 4, sx + 4, sy + 4,
                               fill=col, outline=col)
            drawn_junction.add(input_name)

    # 4) Línea final hacia la etiqueta de salida
    output_info = {}
    for o in descripcion.get("outputs", []):
        if o["from"] not in gates_geom:
            continue
        out_coord = gates_geom[o["from"]]["output"]
        col = net_color.get(o["from"], "#3fb950")
        wid = canvas.create_line(out_coord[0], out_coord[1],
                                 out_coord[0] + 22, out_coord[1],
                                 fill=col, width=2)
        idle_color[wid] = col
        net_wires.setdefault(o["from"], []).append(wid)
        label_id = canvas.create_text(
            out_coord[0] + 36, out_coord[1],
            text=o.get("label", "f"), anchor="w",
            font=("Consolas", 11, "bold"), fill="#3fb950")
        output_info = {"from": o["from"], "label_id": label_id,
                        "wire_ids": [wid]}

    # 5) Orden topológico de evaluación
    eval_order = _orden_topologico([(g["id"], g["inputs"])
                                    for g in descripcion["gates"]])

    # 6) Estructurar modelo final
    modelo = {
        "canvas": canvas,
        "vars": var_info,
        "gates": {},
        "eval_order": eval_order,
        "output": output_info,
        "trace_values": descripcion.get("trace_values"),
        "net_color": net_color,
        "idle_color": idle_color,
        "net_wires": net_wires,
    }
    for g in descripcion["gates"]:
        modelo["gates"][g["id"]] = {
            "type": g["type"],
            "inputs": g["inputs"],
            "geom": gates_geom[g["id"]],
            "wire_in_ids": gate_wire_in[g["id"]],
        }

    # 7) Interacción: pulsar una variable o una puerta ENCIENDE su
    #    conexión (la engrosa en su color) y atenúa el resto, para ver
    #    con total claridad por dónde va esa red.
    def _restaurar(_e=None):
        for wid, col in idle_color.items():
            canvas.itemconfig(wid, fill=col, width=2)

    def _resaltar(net):
        for wid, col in idle_color.items():
            canvas.itemconfig(wid, fill=COLOR_WIRE_DIM, width=2)
        cl = net_color.get(net, "#ffffff")
        for wid in net_wires.get(net, []):
            canvas.itemconfig(wid, fill=cl, width=5)
        canvas.after(2200, _restaurar)

    for _vname, _vinfo in var_info.items():
        canvas.tag_bind(_vinfo["label_id"], "<Button-1>",
                        lambda e, n=_vname: _resaltar(n))
    for g in descripcion["gates"]:
        canvas.tag_bind(gates_geom[g["id"]]["body_id"], "<Button-1>",
                        lambda e, n=g["id"]: _resaltar(n))

    _cw, _ch = _canvas_size(canvas)
    canvas.create_text(
        _cw / 2, _ch - 7, anchor="s",
        text="🖱  Pulsa una variable o una puerta para encender su conexión",
        font=("Consolas", 8), fill=COLOR_TEXT2)
    return modelo


def _orden_topologico(adj):
    """Devuelve los IDs de puerta en orden tal que cada puerta aparece
    DESPUÉS de aquellas cuyas salidas necesita.
    `adj` es una lista de tuplas (id, [inputs]).  Los inputs que no son
    IDs de puerta (variables) se ignoran."""
    ids = [gid for gid, _ in adj]
    deps = {gid: [i for i in ins if i in ids] for gid, ins in adj}
    orden = []
    visit = set()

    def dfs(n):
        if n in visit:
            return
        visit.add(n)
        for d in deps.get(n, []):
            dfs(d)
        orden.append(n)

    for gid in ids:
        dfs(gid)
    return orden


# =====================================================================
#  MOTOR DE ANIMACIÓN — propagación de señales 0/1 por el circuito
# =====================================================================
#
# Una "simulación" arranca con un dict {var: 0|1} y va calculando
# las salidas de cada puerta en orden topológico, mientras recolorea
# los segmentos correspondientes para que el usuario VEA cómo viaja
# la señal por el circuito (verde = 1, rojo = 0). Apoya el "active
# visual learning" sugerido por Freeman et al. (2014).

ANIM_DELAY_MS = 650   # tiempo entre pasos de la animación


def simular_circuito_paso(modelo, valores, paso=0,
                          on_step=None, on_done=None):
    """Anima la propagación de señales paso a paso.

    `modelo`  : dict devuelto por `dibujar_circuito`.
    `valores` : dict {nombre_var: 0|1} con las entradas.
    `paso`    : índice interno (no tocar al llamar desde fuera).
    `on_step` : callback opcional (gate_id_o_var, valor) tras cada paso.
    `on_done` : callback opcional (resultados_dict) al terminar.

    Retorna inmediatamente; usa `canvas.after` para el siguiente paso.
    """
    canvas = modelo["canvas"]
    pasos = ["_vars"] + list(modelo["eval_order"])
    resultados = getattr(simular_circuito_paso, "_buf",
                         {}) if paso > 0 else {}
    if paso == 0:
        resultados = {}
    simular_circuito_paso._buf = resultados

    # Cuando ya recorrimos todos los pasos: pintar la salida final
    if paso >= len(pasos):
        out = modelo.get("output") or {}
        if out and out.get("from") in resultados:
            v = resultados[out["from"]]
            color = _color_para(v)
            for wid in out["wire_ids"]:
                canvas.itemconfig(wid, fill=color, width=3)
            canvas.itemconfig(out["label_id"],
                              text=canvas.itemcget(out["label_id"], "text")
                                   + f"  = {v}",
                              fill=color)
        if on_done:
            on_done(resultados)
        return

    actual = pasos[paso]

    if actual == "_vars":
        # Pinta cada variable y SUS cables salientes con el color de su valor
        for var, info in modelo["vars"].items():
            if var not in valores:
                continue
            v = valores[var]
            color = _color_para(v)
            canvas.itemconfig(info["label_id"],
                              text=f"{var}={v}", fill=color)
            for wid in info["wire_ids"]:
                canvas.itemconfig(wid, fill=color, width=3)
        if on_step:
            on_step("_vars", valores)
    else:
        gid = actual
        gate = modelo["gates"][gid]
        # Obtenemos los valores de las entradas
        in_vals = []
        for in_name in gate["inputs"]:
            if in_name in resultados:
                in_vals.append(resultados[in_name])
            else:
                in_vals.append(valores.get(in_name, 0))
        # Evaluamos la puerta
        v = _EVAL_PUERTA[gate["type"]](in_vals)
        resultados[gid] = v
        color = _color_para(v)
        # Recoloreamos: cuerpo + cables de salida (= wire_ids del geom
        # excepto los de entrada, que ya estaban pintados al propagar
        # la señal de la puerta anterior)
        canvas.itemconfig(gate["geom"]["body_id"],
                          fill=_fill_gate_para(v, gate["type"]))
        # Cables internos de salida (los que dibujamos AL CONSTRUIR la
        # puerta, normalmente la línea que sale de la bubble en NAND/NOR/NOT)
        for wid in gate["geom"]["wire_ids"]:
            # Si era una entrada de la puerta, mejor lo dejamos:
            # solo pintamos los wires con coord. x > centro
            canvas.itemconfig(wid, fill=color, width=3)
        # Cables hacia las puertas siguientes que consumen esta salida:
        # los recolorea automáticamente el siguiente paso (cuando esa
        # puerta esté siendo evaluada). PERO también podemos pintar
        # ahora los cables que entran a otras puertas y proceden de gid.
        for otro_id, otro in modelo["gates"].items():
            for w in otro["wire_in_ids"]:
                if w["src"] == gid:
                    canvas.itemconfig(w["id"], fill=color, width=3)
        if on_step:
            on_step(gid, v)

    canvas.after(ANIM_DELAY_MS,
                 lambda: simular_circuito_paso(modelo, valores, paso + 1,
                                               on_step, on_done))


def resetear_colores(modelo):
    """Devuelve todos los cables/cuerpos a su color 'idle'."""
    if not modelo:
        return
    c = modelo["canvas"]
    idle = modelo.get("idle_color", {})

    def _idle(wid):
        return idle.get(wid, COLOR_SIGNAL_IDLE)

    for info in modelo["vars"].values():
        # restaurar el texto original (sin =0/=1) y su color de net
        txt = c.itemcget(info["label_id"], "text")
        if "=" in txt:
            txt = txt.split("=")[0]
        c.itemconfig(info["label_id"], text=txt,
                     fill=info.get("color", "#a371f7"))
        for wid in info["wire_ids"]:
            c.itemconfig(wid, fill=_idle(wid), width=2)
    for g in modelo["gates"].values():
        c.itemconfig(g["geom"]["body_id"],
                     fill=_fill_gate_para(None, g["type"]))
        for wid in g["geom"]["wire_ids"]:
            c.itemconfig(wid, fill=_idle(wid), width=2)
        for w in g["wire_in_ids"]:
            c.itemconfig(w["id"], fill=_idle(w["id"]), width=2)
    out = modelo.get("output") or {}
    if out:
        for wid in out["wire_ids"]:
            c.itemconfig(wid, fill=_idle(wid), width=2)
        # restaura la etiqueta sin "= valor"
        txt = c.itemcget(out["label_id"], "text")
        if "=" in txt:
            txt = txt.split("=")[0].rstrip()
        c.itemconfig(out["label_id"], text=txt, fill="#3fb950")


# =====================================================================
#  VISUALIZACIONES GENERALES — para secciones distintas de lógica:
#  grafos (1.7), diagramas de Venn (2.1), funciones (3.1, 3.3),
#  distribuciones (4.1), vectores 2D (2.4). Cada función limpia el
#  canvas y dibuja la figura.
# =====================================================================

def dibujar_grafo(canvas, datos):
    """Dibuja un grafo a partir de:
        {"nodes": [{"id":"A","pos":(x,y),"label":"v1"}, ...],
         "edges": [{"from":"A","to":"B","dir":True/False,"label":"3"}],
         "highlight_path": ["A","B","C"]  # opcional}
    Las coordenadas se CENTRAN automáticamente en el canvas real.
    """
    canvas.delete("all")
    cw, ch = _canvas_size(canvas)

    # Bounding box de las posiciones declaradas en los datos
    xs = [n["pos"][0] for n in datos["nodes"]]
    ys = [n["pos"][1] for n in datos["nodes"]]
    if xs and ys:
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        # Margen para que los nodos no se peguen al borde
        pad = 30
        data_w = max(1, x_max - x_min + 2 * pad)
        data_h = max(1, y_max - y_min + 2 * pad)
        scale = min((cw) / data_w, (ch) / data_h, 1.6)
        # Offset para centrar
        cx_data = (x_min + x_max) / 2
        cy_data = (y_min + y_max) / 2
        ox = cw / 2 - cx_data * scale
        oy = ch / 2 - cy_data * scale
    else:
        scale, ox, oy = 1.0, 0, 0

    def _T(p):
        return (p[0] * scale + ox, p[1] * scale + oy)

    pos = {n["id"]: _T(n["pos"]) for n in datos["nodes"]}

    # Aristas primero (para que queden detrás de los nodos)
    highlight = set()
    path = datos.get("highlight_path") or []
    for i in range(len(path) - 1):
        highlight.add(frozenset([path[i], path[i + 1]]))
        highlight.add((path[i], path[i + 1]))

    for e in datos["edges"]:
        sx, sy = pos[e["from"]]
        ex, ey = pos[e["to"]]
        is_hl = (
            frozenset([e["from"], e["to"]]) in highlight or
            (e["from"], e["to"]) in highlight
        )
        col = "#3fb950" if is_hl else "#8b98a5"
        w = 3 if is_hl else 2
        if e.get("dir"):
            canvas.create_line(sx, sy, ex, ey, fill=col, width=w,
                                arrow="last", arrowshape=(12, 14, 5))
        else:
            canvas.create_line(sx, sy, ex, ey, fill=col, width=w)
        if e.get("label"):
            canvas.create_text((sx + ex) / 2, (sy + ey) / 2 - 8,
                                text=str(e["label"]),
                                font=("Consolas", 9, "bold"),
                                fill="#39c5cf")

    # Nodos
    r = 18
    for n in datos["nodes"]:
        x, y = n["pos"]
        is_hl = n["id"] in path
        fill = "#16361f" if is_hl else "#1f2a36"
        outline = "#3fb950" if is_hl else "#39c5cf"
        canvas.create_oval(x - r, y - r, x + r, y + r,
                            fill=fill, outline=outline, width=2)
        label = n.get("label", n["id"])
        canvas.create_text(x, y, text=label,
                            font=("Consolas", 10, "bold"),
                            fill="#f0f6fc")


def dibujar_venn(canvas, datos):
    """Dibuja un diagrama de Venn de 2 o 3 conjuntos.
        {"sets": [{"label":"A","pos":(x,y),"r":60,"color":"#..."}],
         "elements": [{"label":"3","pos":(x,y),"in":["A","B"]}]  # opc}
    Centrado automáticamente al canvas real.
    """
    canvas.delete("all")
    cw, ch = _canvas_size(canvas)
    colores_def = ["#ff7b72", "#79c0ff", "#d2a8ff"]

    # Bounding box de las posiciones de los conjuntos
    xs = [s["pos"][0] for s in datos["sets"]]
    ys = [s["pos"][1] for s in datos["sets"]]
    rs = [s.get("r", 70) for s in datos["sets"]]
    if xs and ys:
        x_min = min(xs) - max(rs)
        x_max = max(xs) + max(rs)
        y_min = min(ys) - max(rs)
        y_max = max(ys) + max(rs)
        cx_data = (x_min + x_max) / 2
        cy_data = (y_min + y_max) / 2
        ox = cw / 2 - cx_data
        oy = ch / 2 - cy_data
    else:
        ox = oy = 0

    for i, s in enumerate(datos["sets"]):
        x, y = s["pos"][0] + ox, s["pos"][1] + oy
        r = s.get("r", 70)
        col = s.get("color", colores_def[i % 3])
        canvas.create_oval(x - r, y - r, x + r, y + r,
                            outline=col, width=3, fill="",
                            stipple="gray25")
        canvas.create_text(x - r * 0.7, y - r * 0.9,
                            text=s["label"], anchor="w",
                            font=("Consolas", 14, "bold"),
                            fill=col)
    for e in datos.get("elements", []):
        x, y = e["pos"][0] + ox, e["pos"][1] + oy
        canvas.create_text(x, y, text=str(e["label"]),
                            font=("Consolas", 11, "bold"),
                            fill="#f0f6fc")


def _canvas_size(canvas, default_w=440, default_h=220):
    """Devuelve (w, h) del canvas usando el tamaño real si está disponible;
    si no, el reqwidth/reqheight; si no, los defaults pasados."""
    canvas.update_idletasks()
    w = canvas.winfo_width()
    if w <= 1:
        w = canvas.winfo_reqwidth()
    if w <= 1:
        w = default_w
    h = canvas.winfo_height()
    if h <= 1:
        h = canvas.winfo_reqheight()
    if h <= 1:
        h = default_h
    return w, h


def dibujar_funcion(canvas, datos):
    """Dibuja la gráfica de una función dada como lista de valores
    o como una función Python. Acepta:
        {"expr": callable o list of (x,y),
         "xrange": (xmin, xmax),
         "yrange": (ymin, ymax),
         "marks": [(x, y, "etiqueta")],   # puntos destacados
         "title": "f(x) = x²"}
    """
    canvas.delete("all")
    w, h = _canvas_size(canvas)
    margin = 34
    xmin, xmax = datos.get("xrange", (-5, 5))
    ymin, ymax = datos.get("yrange", (-5, 5))

    def sx(x): return margin + (x - xmin) / (xmax - xmin) * (w - 2 * margin)
    def sy(y): return h - margin - (y - ymin) / (ymax - ymin) * (h - 2 * margin)

    # Rejilla suave (líneas en cada entero)
    for gx in range(int(math.ceil(xmin)), int(math.floor(xmax)) + 1):
        canvas.create_line(sx(gx), margin, sx(gx), h - margin,
                            fill="#22303d", width=1)
    for gy in range(int(math.ceil(ymin)), int(math.floor(ymax)) + 1):
        canvas.create_line(margin, sy(gy), w - margin, sy(gy),
                            fill="#22303d", width=1)

    # Ejes principales (más oscuros) + etiquetas en los extremos
    if ymin <= 0 <= ymax:
        canvas.create_line(margin, sy(0), w - margin, sy(0),
                            fill="#5a6b7a", width=1)
        canvas.create_text(w - margin + 6, sy(0), text="x", anchor="w",
                            font=("Consolas", 9, "italic"), fill="#5a6b7a")
    if xmin <= 0 <= xmax:
        canvas.create_line(sx(0), margin, sx(0), h - margin,
                            fill="#5a6b7a", width=1)
        canvas.create_text(sx(0) + 6, margin - 2, text="y", anchor="w",
                            font=("Consolas", 9, "italic"), fill="#5a6b7a")

    expr = datos.get("expr")
    if callable(expr):
        # Trazamos en segmentos para no unir saltos (asíntotas)
        N = 240
        pts = []
        for i in range(N + 1):
            x = xmin + (xmax - xmin) * i / N
            try:
                y = expr(x)
                if ymin <= y <= ymax:
                    pts.extend([sx(x), sy(y)])
                else:
                    if len(pts) >= 4:
                        canvas.create_line(*pts, fill="#39c5cf",
                                           width=3, smooth=True)
                    pts = []
            except Exception:
                if len(pts) >= 4:
                    canvas.create_line(*pts, fill="#39c5cf",
                                       width=3, smooth=True)
                pts = []
        if len(pts) >= 4:
            canvas.create_line(*pts, fill="#39c5cf", width=3, smooth=True)
    elif isinstance(expr, list):
        pts = []
        for (x, y) in expr:
            pts.extend([sx(x), sy(y)])
        if len(pts) >= 4:
            canvas.create_line(*pts, fill="#39c5cf", width=3, smooth=True)

    # Marcas/puntos destacados
    for m in datos.get("marks", []):
        if len(m) >= 2:
            mx, my = m[0], m[1]
            lab = m[2] if len(m) > 2 else f"({mx}, {my})"
            r = 5
            canvas.create_oval(sx(mx) - r, sy(my) - r,
                                sx(mx) + r, sy(my) + r,
                                fill="#f85149", outline="#f85149")
            canvas.create_text(sx(mx) + 8, sy(my) - 10,
                                text=lab, anchor="w",
                                font=("Consolas", 9, "bold"),
                                fill="#f85149")

    titulo = datos.get("title")
    if titulo:
        canvas.create_text(w / 2, 14, text=titulo, anchor="center",
                            font=("Consolas", 11, "bold"),
                            fill="#39c5cf")


def dibujar_distribucion(canvas, datos):
    """Dibuja barras (discreta) o curva (continua).
    Decide por el contenido:
      • Si hay "data" → barras (lista de (x, p)).
      • Si hay "expr" → curva continua sobre xrange.
    """
    canvas.delete("all")
    w, h = _canvas_size(canvas)
    margin = 30
    # "tipo" estaría sobrescrito por el despachador; usamos el contenido.
    if "data" in datos:
        modo = "barras"
    elif "expr" in datos:
        modo = "curva"
    else:
        modo = datos.get("tipo_distrib", "barras")

    if modo == "barras":
        bars = datos["data"]
        if not bars:
            return
        pmax = max(p for _, p in bars)
        bar_w = (w - 2 * margin) / len(bars) * 0.75
        for i, (xv, p) in enumerate(bars):
            bx = margin + (i + 0.5) * (w - 2 * margin) / len(bars)
            bh = (p / pmax) * (h - 2 * margin)
            canvas.create_rectangle(bx - bar_w/2, h - margin - bh,
                                     bx + bar_w/2, h - margin,
                                     fill="#a371f7", outline="")
            canvas.create_text(bx, h - margin + 12, text=str(xv),
                                font=("Consolas", 9, "bold"),
                                fill="#f0f6fc")
            canvas.create_text(bx, h - margin - bh - 8,
                                text=f"{p:.2f}",
                                font=("Consolas", 8),
                                fill="#8b98a5")
    elif modo == "curva":
        xmin, xmax = datos.get("xrange", (-3, 3))
        ymax = datos.get("ymax", 0.5)
        expr = datos["expr"]
        N = 150
        pts = []
        for i in range(N + 1):
            x = xmin + (xmax - xmin) * i / N
            try:
                y = expr(x)
                px = margin + (x - xmin) / (xmax - xmin) * (w - 2 * margin)
                py = h - margin - (y / ymax) * (h - 2 * margin)
                pts.extend([px, py])
            except Exception:
                pass
        if len(pts) >= 4:
            # área bajo la curva
            poly = list(pts)
            poly.extend([w - margin, h - margin, margin, h - margin])
            canvas.create_polygon(*poly, fill="#241a40", outline="")
            canvas.create_line(*pts, fill="#a371f7", width=2, smooth=True)

    # Eje X
    canvas.create_line(margin, h - margin, w - margin, h - margin,
                        fill="#8b98a5", width=1)
    titulo = datos.get("title")
    if titulo:
        canvas.create_text(w / 2, 14, text=titulo, anchor="center",
                            font=("Consolas", 11, "bold"),
                            fill="#a371f7")


def dibujar_vectores2d(canvas, datos):
    """Vectores en el plano:
        {"vectores": [{"v":(x,y),"color":"#..","label":"u"}],
         "xrange": (-3,3), "yrange": (-3,3)}
    """
    canvas.delete("all")
    w, h = _canvas_size(canvas)
    margin = 24
    xmin, xmax = datos.get("xrange", (-5, 5))
    ymin, ymax = datos.get("yrange", (-5, 5))

    def sx(x): return margin + (x - xmin) / (xmax - xmin) * (w - 2 * margin)
    def sy(y): return h - margin - (y - ymin) / (ymax - ymin) * (h - 2 * margin)

    # Grid + ejes
    for gx in range(int(xmin), int(xmax) + 1):
        canvas.create_line(sx(gx), margin, sx(gx), h - margin,
                            fill="#22303d", width=1)
    for gy in range(int(ymin), int(ymax) + 1):
        canvas.create_line(margin, sy(gy), w - margin, sy(gy),
                            fill="#22303d", width=1)
    canvas.create_line(margin, sy(0), w - margin, sy(0),
                        fill="#5a6b7a", width=1)
    canvas.create_line(sx(0), margin, sx(0), h - margin,
                        fill="#5a6b7a", width=1)

    colores = ["#39c5cf", "#3fb950", "#f85149", "#d29922", "#a371f7"]
    for i, vec in enumerate(datos["vectores"]):
        x, y = vec["v"]
        col = vec.get("color", colores[i % len(colores)])
        lab = vec.get("label", f"v{i+1}")
        x0, y0 = vec.get("origen", (0, 0))
        canvas.create_line(sx(x0), sy(y0), sx(x), sy(y),
                            fill=col, width=3,
                            arrow="last", arrowshape=(14, 16, 6))
        # etiqueta cerca de la punta
        canvas.create_text(sx(x) + 8, sy(y) - 8, text=lab,
                            anchor="w",
                            font=("Consolas", 10, "bold"), fill=col)


def dibujar_tabla(canvas, datos):
    """Dibuja una tabla con cabecera y filas:
        {"headers": ["A", "B", "f"],
         "rows": [["0","0","1"], ...],
         "highlight_rows": [0],
         "title": "Tabla de verdad"}
    """
    canvas.delete("all")
    cw, ch = _canvas_size(canvas)
    headers = datos.get("headers", [])
    rows = datos.get("rows", [])
    hl = set(datos.get("highlight_rows", []))
    if not headers or not rows:
        return

    ncols = len(headers)
    nrows = len(rows) + 1
    cell_w = min(80, (cw - 40) // ncols)
    cell_h = min(28, (ch - 30) // nrows)
    total_w = cell_w * ncols
    total_h = cell_h * nrows
    ox = (cw - total_w) // 2
    oy = (ch - total_h) // 2 + 8

    for j, hdr in enumerate(headers):
        x0 = ox + j * cell_w
        canvas.create_rectangle(x0, oy, x0 + cell_w, oy + cell_h,
                                 fill="#39c5cf", outline="white", width=1)
        canvas.create_text(x0 + cell_w / 2, oy + cell_h / 2,
                            text=str(hdr), fill="white",
                            font=("Consolas", 10, "bold"))

    for i, row in enumerate(rows):
        y0 = oy + (i + 1) * cell_h
        bg = ("#33301a" if i in hl
              else "#1f2a36" if i % 2 == 0 else "#1a212b")
        for j, cell in enumerate(row):
            x0 = ox + j * cell_w
            canvas.create_rectangle(x0, y0, x0 + cell_w, y0 + cell_h,
                                     fill=bg, outline="#2f3b48", width=1)
            txt = str(cell).strip()
            col = (COLOR_SIGNAL_HI if txt == "1"
                   else COLOR_SIGNAL_LO if txt == "0"
                   else "#f0f6fc")
            canvas.create_text(x0 + cell_w / 2, y0 + cell_h / 2,
                                text=txt, fill=col,
                                font=("Consolas", 11, "bold"))

    titulo = datos.get("title")
    if titulo:
        canvas.create_text(cw / 2, 12, text=titulo, anchor="center",
                            font=("Consolas", 11, "bold"),
                            fill="#39c5cf")


def dibujar_recta_numerica(canvas, datos):
    """Recta numérica con intervalos, puntos y etiquetas:
        {"xrange": (-3, 5),
         "marks": [{"x": 2, "label": "máx", "color": "#3fb950"}],
         "intervals": [{"a": 0, "b": 2, "label": "creciente",
                        "color": "#3fb950", "above": True}],
         "title": "..."}
    """
    canvas.delete("all")
    cw, ch = _canvas_size(canvas)
    xmin, xmax = datos.get("xrange", (-5, 5))
    margin = 40
    y0 = ch * 0.6

    def sx(x):
        return margin + (x - xmin) / (xmax - xmin) * (cw - 2 * margin)

    canvas.create_line(margin, y0, cw - margin, y0,
                        fill="#f0f6fc", width=2,
                        arrow="both", arrowshape=(10, 12, 4))

    for k in range(int(xmin), int(xmax) + 1):
        x = sx(k)
        canvas.create_line(x, y0 - 5, x, y0 + 5, fill="#8b98a5", width=1)
        canvas.create_text(x, y0 + 18, text=str(k), anchor="center",
                            font=("Consolas", 9), fill="#8b98a5")

    for iv in datos.get("intervals", []):
        a, b = iv["a"], iv["b"]
        col = iv.get("color", "#39c5cf")
        lbl = iv.get("label", "")
        above = iv.get("above", True)
        ay = y0 - 22 if above else y0 + 22
        canvas.create_line(sx(a), ay, sx(b), ay,
                            fill=col, width=6, capstyle="round")
        canvas.create_text((sx(a) + sx(b)) / 2,
                            ay + (-12 if above else 14),
                            text=lbl, fill=col,
                            font=("Consolas", 10, "bold"))

    for m in datos.get("marks", []):
        col = m.get("color", "#f85149")
        r = 6
        x = sx(m["x"])
        canvas.create_oval(x - r, y0 - r, x + r, y0 + r,
                            fill=col, outline=col)
        if m.get("label"):
            canvas.create_text(x, y0 - 18, text=m["label"], anchor="s",
                                fill=col,
                                font=("Consolas", 10, "bold"))

    titulo = datos.get("title")
    if titulo:
        canvas.create_text(cw / 2, 14, text=titulo, anchor="center",
                            font=("Consolas", 11, "bold"),
                            fill="#39c5cf")


def dibujar_arbol(canvas, datos):
    """Árbol jerárquico (Bayes, decisión…):
        {"root": {"label": "raíz",
                  "children": [
                      {"label": "izq", "edge_label": "p=0.3"},
                      {"label": "der", "edge_label": "p=0.7"},
                  ]},
         "title": "..."}
    """
    canvas.delete("all")
    cw, ch = _canvas_size(canvas)

    def colocar(node, x, y, dx, level=0):
        node["_x"] = x
        node["_y"] = y
        node["_level"] = level
        ch_list = node.get("children", []) or []
        n = len(ch_list)
        if n == 0:
            return
        for i, c in enumerate(ch_list):
            if n == 1:
                cx = x
            else:
                cx = x - dx + i * (2 * dx / (n - 1))
            colocar(c, cx, y + 60, dx / max(n, 1) * 0.95, level + 1)

    root = datos.get("root")
    if not root:
        return
    colocar(root, cw / 2, 40, cw / 4)

    def dibujar_aristas(node):
        for c in node.get("children", []) or []:
            canvas.create_line(node["_x"], node["_y"] + 10,
                                c["_x"], c["_y"] - 10,
                                fill="#8b98a5", width=2)
            elbl = c.get("edge_label", "")
            if elbl:
                mx = (node["_x"] + c["_x"]) / 2
                my = (node["_y"] + c["_y"]) / 2
                canvas.create_text(mx + 8, my, anchor="w", text=elbl,
                                    font=("Consolas", 9, "bold"),
                                    fill="#39c5cf")
            dibujar_aristas(c)
    dibujar_aristas(root)

    def dibujar_nodos(node):
        col = node.get("color", "#1f2a36")
        outline = node.get("outline", "#39c5cf")
        x, y = node["_x"], node["_y"]
        w = max(60, 8 * len(str(node["label"])))
        canvas.create_rectangle(x - w / 2, y - 14, x + w / 2, y + 14,
                                 fill=col, outline=outline, width=2)
        canvas.create_text(x, y, text=str(node["label"]),
                            font=("Consolas", 10, "bold"),
                            fill="#f0f6fc")
        for c in node.get("children", []) or []:
            dibujar_nodos(c)
    dibujar_nodos(root)

    titulo = datos.get("title")
    if titulo:
        canvas.create_text(cw / 2, 12, text=titulo, anchor="center",
                            font=("Consolas", 11, "bold"),
                            fill="#39c5cf")


def dibujar_matriz(canvas, datos):
    """Matriz con celdas / filas / columnas resaltadas:
        {"matrix": [[1,2,3],[4,5,6]],
         "highlight_cells": [(0,0)], "highlight_rows": [1],
         "highlight_cols": [2], "label": "A",
         "title": "A 2×3"}
    """
    canvas.delete("all")
    cw, ch = _canvas_size(canvas)
    M = datos.get("matrix", [])
    if not M:
        return
    nr = len(M)
    nc = max(len(row) for row in M)
    cell = min(60, (cw - 80) // max(nc, 1), (ch - 60) // max(nr, 1))
    total_w = cell * nc
    total_h = cell * nr
    ox = (cw - total_w) // 2 + 30
    oy = (ch - total_h) // 2 + 8

    hl_cells = set(tuple(c) for c in datos.get("highlight_cells", []))
    hl_rows = set(datos.get("highlight_rows", []))
    hl_cols = set(datos.get("highlight_cols", []))

    # Corchetes [   ]
    canvas.create_line(ox - 8, oy - 4, ox - 14, oy - 4,
                        ox - 14, oy + total_h + 4, ox - 8, oy + total_h + 4,
                        fill="#f0f6fc", width=2)
    canvas.create_line(ox + total_w + 8, oy - 4, ox + total_w + 14, oy - 4,
                        ox + total_w + 14, oy + total_h + 4,
                        ox + total_w + 8, oy + total_h + 4,
                        fill="#f0f6fc", width=2)

    label = datos.get("label", "")
    if label:
        canvas.create_text(ox - 26, oy + total_h / 2, text=label,
                            font=("Consolas", 13, "bold italic"),
                            fill="#39c5cf", anchor="e")

    for i, row in enumerate(M):
        for j, val in enumerate(row):
            x0 = ox + j * cell
            y0 = oy + i * cell
            if (i, j) in hl_cells:
                bg = "#33301a"
            elif i in hl_rows or j in hl_cols:
                bg = "#1d2e1a"
            else:
                bg = "#1a212b"
            canvas.create_rectangle(x0, y0, x0 + cell, y0 + cell,
                                     fill=bg, outline="#2f3b48", width=1)
            canvas.create_text(x0 + cell / 2, y0 + cell / 2,
                                text=str(val),
                                font=("Consolas", 11, "bold"),
                                fill="#f0f6fc")

    titulo = datos.get("title")
    if titulo:
        canvas.create_text(cw / 2, 12, text=titulo, anchor="center",
                            font=("Consolas", 11, "bold"),
                            fill="#39c5cf")


# Despachador: tipo de "visual" → función de dibujo.
_DISPATCH_VISUAL = {
    "grafo":           dibujar_grafo,
    "venn":            dibujar_venn,
    "funcion":         dibujar_funcion,
    "distribucion":    dibujar_distribucion,
    "vectores2d":      dibujar_vectores2d,
    "tabla":           dibujar_tabla,
    "recta_numerica":  dibujar_recta_numerica,
    "arbol":           dibujar_arbol,
    "matriz":          dibujar_matriz,
}


# =====================================================================
#  ANIMACIONES SOBRE VISUALIZACIONES (no circuitos)
#  · descenso de gradiente: bolita que rueda por la curva
#  · vectores: se dibujan secuencialmente (u, luego v, luego u+v)
#  · markov: el estado activo "salta" según la matriz de transición
# =====================================================================

ANIM_VIS_DELAY = 700   # ms entre pasos de animación de visuales


def animar_descenso(canvas, visual, on_done=None):
    """Anima el descenso de gradiente sobre una función.
    El visual debe ser de tipo 'funcion' con sub-dict 'animate':
        "animate": {"tipo": "descenso", "x0": 2.5, "lr": 0.15,
                     "steps": 8, "grad": callable}
    Dibuja la curva y mueve una bolita roja paso a paso por la
    trayectoria w_{t+1} = w_t - lr·grad(w_t), dejando rastro.
    """
    anim = visual.get("animate", {})
    expr = visual.get("expr")
    grad = anim.get("grad")
    if not callable(expr) or not callable(grad):
        if on_done:
            on_done()
        return

    # Redibujar la curva base (limpia el rastro previo)
    dibujar_funcion(canvas, visual)

    w, h = _canvas_size(canvas)
    margin = 34
    xmin, xmax = visual.get("xrange", (-5, 5))
    ymin, ymax = visual.get("yrange", (-5, 5))

    def sx(x): return margin + (x - xmin) / (xmax - xmin) * (w - 2 * margin)
    def sy(y): return h - margin - (y - ymin) / (ymax - ymin) * (h - 2 * margin)

    # Precalcular la trayectoria
    x = anim.get("x0", 2.0)
    lr = anim.get("lr", 0.1)
    steps = anim.get("steps", 8)
    traj = [x]
    for _ in range(steps):
        x = x - lr * grad(x)
        traj.append(x)

    estado = {"i": 0, "prev": None}

    def paso():
        i = estado["i"]
        if i >= len(traj):
            # Marcar el punto final
            xf = traj[-1]
            try:
                yf = expr(xf)
                canvas.create_text(sx(xf), sy(yf) - 22,
                                   text=f"≈ mínimo (x={xf:.2f})",
                                   fill="#3fb950", anchor="s",
                                   font=("Consolas", 9, "bold"))
            except Exception:
                pass
            if on_done:
                on_done()
            return
        xi = traj[i]
        try:
            yi = expr(xi)
        except Exception:
            yi = ymin
        px, py = sx(xi), sy(yi)
        # Rastro desde el punto anterior
        if estado["prev"] is not None:
            ppx, ppy = estado["prev"]
            canvas.create_line(ppx, ppy, px, py,
                               fill="#d29922", width=2, dash=(3, 2))
        # Bolita
        r = 7
        canvas.create_oval(px - r, py - r, px + r, py + r,
                           fill="#f85149", outline="#7a1f1a", width=2)
        canvas.create_text(px, py - 14, text=str(i),
                           fill="#7a1f1a", anchor="s",
                           font=("Consolas", 8, "bold"))
        estado["prev"] = (px, py)
        estado["i"] += 1
        canvas.after(ANIM_VIS_DELAY, paso)

    paso()


def animar_vectores(canvas, visual, on_done=None):
    """Dibuja los vectores 2D uno a uno (secuencial)."""
    vecs = visual.get("vectores", [])
    estado = {"i": 0}

    def paso():
        i = estado["i"]
        if i > len(vecs):
            if on_done:
                on_done()
            return
        parcial = dict(visual)
        parcial["vectores"] = vecs[:i]
        dibujar_vectores2d(canvas, parcial)
        estado["i"] += 1
        if i <= len(vecs):
            canvas.after(ANIM_VIS_DELAY, paso)
        elif on_done:
            on_done()

    paso()


def animar_markov(canvas, visual, on_done=None):
    """Resalta el estado activo de una cadena de Markov saltando
    entre nodos de un grafo según una secuencia precalculada.
    El visual es de tipo 'grafo' con 'animate':
        "animate": {"tipo": "markov", "secuencia": ["S","S","L","S"]}
    """
    anim = visual.get("animate", {})
    secuencia = anim.get("secuencia", [])
    estado = {"i": 0}

    def paso():
        i = estado["i"]
        if i >= len(secuencia):
            if on_done:
                on_done()
            return
        parcial = dict(visual)
        parcial["highlight_path"] = secuencia[:i + 1]
        dibujar_grafo(canvas, parcial)
        w, _h = _canvas_size(canvas)
        canvas.create_text(w / 2, 14,
                           text=f"Paso {i}: estado = {secuencia[i]}",
                           fill="#a371f7", anchor="center",
                           font=("Consolas", 11, "bold"))
        estado["i"] += 1
        canvas.after(ANIM_VIS_DELAY, paso)

    paso()


def animar_recorrido(canvas, visual, on_done=None):
    """Anima el RECORRIDO de un camino sobre un grafo: ilumina los
    vértices y las aristas uno a uno, dejando el rastro del camino.
    Hace TANGIBLE un concepto abstracto (camino, alcanzabilidad, conexión).
    El visual es de tipo 'grafo' con 'animate':
        "animate": {"tipo": "recorrido", "secuencia": ["1","3","5"]}
    """
    anim = visual.get("animate", {})
    secuencia = anim.get("secuencia", [])
    estado = {"i": 0}

    def paso():
        i = estado["i"]
        w, _h = _canvas_size(canvas)
        if i >= len(secuencia):
            recorrido = " → ".join(str(s) for s in secuencia)
            canvas.create_text(w / 2, 14,
                               text=f"✓ recorrido: {recorrido}",
                               fill=COLOR_OK, anchor="center",
                               font=("Consolas", 11, "bold"))
            if on_done:
                on_done()
            return
        parcial = dict(visual)
        parcial["highlight_path"] = secuencia[:i + 1]
        dibujar_grafo(canvas, parcial)
        recorrido = " → ".join(str(s) for s in secuencia[:i + 1])
        canvas.create_text(w / 2, 14,
                           text=f"Paso {i + 1}/{len(secuencia)}:  {recorrido}",
                           fill=COLOR_ACCENT, anchor="center",
                           font=("Consolas", 11, "bold"))
        estado["i"] += 1
        canvas.after(ANIM_VIS_DELAY, paso)

    paso()


_DISPATCH_ANIM_VISUAL = {
    "descenso":  animar_descenso,
    "vectores":  animar_vectores,
    "markov":    animar_markov,
    "recorrido": animar_recorrido,
}


# =====================================================================
#  VISTA 3D (Matplotlib embebido) — rotable con el ratón + animación.
#  Para conceptos que SON 3D de verdad: vectores en ℝ³ y superficies
#  de descenso de gradiente. El lienzo Tkinter es 2D; esto abre una
#  ventana aparte sin tocar el resto de la interfaz.
# =====================================================================

def _estilo_ax3d(ax, titulo=""):
    """Aplica el tema oscuro 'Consola IA' a unos ejes 3D de Matplotlib."""
    ax.set_facecolor(COLOR_PANEL)
    pane = (0.06, 0.08, 0.10, 1.0)
    edge = (0.25, 0.30, 0.36, 1.0)
    for eje in (ax.xaxis, ax.yaxis, ax.zaxis):
        try:
            eje.set_pane_color(pane)
            eje.pane.set_edgecolor(edge)
        except Exception:
            pass
    ax.tick_params(colors="#8b98a5")
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    for lbl in (ax.xaxis.label, ax.yaxis.label, ax.zaxis.label):
        lbl.set_color("#f0f6fc")
    if titulo:
        ax.set_title(titulo, color="#39c5cf", fontsize=11, pad=10)


def _traj_gd(grad, x0, y0, lr, steps):
    """Trayectoria de descenso de gradiente (x_{t+1}=x_t-lr·∇f)."""
    xs, ys = [x0], [y0]
    x, y = x0, y0
    for _ in range(steps):
        gx, gy = grad(x, y)
        x, y = x - lr * gx, y - lr * gy
        xs.append(x); ys.append(y)
    return xs, ys


def abrir_visor_3d(parent, spec):
    """Abre una ventana 3D (Matplotlib embebido), rotable con el ratón y
    con botón de animación. spec['tipo'] ∈ {'vectores3d', 'superficie'}."""
    if not _HAS_MPL or not spec:
        return
    tipo = spec.get("tipo")
    win = tk.Toplevel(parent)
    win.title("🧊  Vista 3D — " + spec.get("title", ""))
    win.configure(bg=COLOR_BG)
    win.geometry("780x720")

    fig = Figure(figsize=(7.4, 6.2), dpi=100, facecolor=COLOR_PANEL)
    ax = fig.add_subplot(111, projection="3d")
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True,
                                padx=8, pady=8)
    estado = {"rot_job": None, "anim_job": None}
    COLS = ["#39c5cf", "#3fb950", "#f85149", "#d29922", "#a371f7"]

    # ---------- VECTORES 3D ----------
    def _base_vectores(n_vis=None):
        ax.clear()
        _estilo_ax3d(ax, spec.get("title", "Vectores en ℝ³"))
        vecs = spec.get("vectores", [])
        comb = spec.get("combinacion")
        todos = [v["v"] for v in vecs] + ([comb["v"]] if comb else [])
        m = max([abs(c) for v in todos for c in v] + [1])
        lim = spec.get("lim", m * 1.1)
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
        # ejes por el origen
        ax.plot([-lim, lim], [0, 0], [0, 0], color="#5a6b7a", lw=0.8)
        ax.plot([0, 0], [-lim, lim], [0, 0], color="#5a6b7a", lw=0.8)
        ax.plot([0, 0], [0, 0], [-lim, lim], color="#5a6b7a", lw=0.8)
        cuantos = len(vecs) if n_vis is None else n_vis
        for i, v in enumerate(vecs[:cuantos]):
            x, y, z = v["v"]
            col = v.get("color", COLS[i % len(COLS)])
            ax.quiver(0, 0, 0, x, y, z, color=col, lw=2.5,
                      arrow_length_ratio=0.12)
            ax.text(x, y, z, "  " + v.get("label", ""), color=col,
                    fontsize=11, fontweight="bold")
        if comb and (n_vis is None or n_vis >= len(vecs)):
            x, y, z = comb["v"]
            col = comb.get("color", "#f85149")
            ax.quiver(0, 0, 0, x, y, z, color=col, lw=3,
                      arrow_length_ratio=0.12)
            ax.text(x, y, z, "  " + comb.get("label", ""), color=col,
                    fontsize=11, fontweight="bold")

    # ---------- SUPERFICIE z=f(x,y) ----------
    def _base_superficie(n_vis=None):
        ax.clear()
        _estilo_ax3d(ax, spec.get("title", "z = f(x, y)"))
        f = spec.get("f", lambda x, y: x * x + y * y)
        xa, xb = spec.get("xrange", (-3, 3))
        ya, yb = spec.get("yrange", (-3, 3))
        X = _np.linspace(xa, xb, 40)
        Y = _np.linspace(ya, yb, 40)
        X, Y = _np.meshgrid(X, Y)
        Z = f(X, Y)
        ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.55,
                        linewidth=0, antialiased=True)
        # trayectoria de descenso
        tx = spec.get("trayectoria")
        if tx is None and spec.get("grad"):
            xs, ys = _traj_gd(spec["grad"], spec.get("x0", 2.0),
                              spec.get("y0", 2.0), spec.get("lr", 0.1),
                              spec.get("steps", 12))
        elif tx is not None:
            xs = [p[0] for p in tx]; ys = [p[1] for p in tx]
        else:
            xs = ys = None
        if xs:
            zs = [float(f(_np.array(x), _np.array(y)))
                  for x, y in zip(xs, ys)]
            k = len(xs) if n_vis is None else max(1, n_vis)
            ax.plot(xs[:k], ys[:k], zs[:k], color="#f85149", lw=2.2,
                    marker="o", markersize=3)
            # bolita en la posición actual
            j = min(k, len(xs)) - 1
            ax.scatter([xs[j]], [ys[j]], [zs[j]], color="#f85149", s=60)
        return spec.get("grad") is not None or spec.get("trayectoria")

    def _render(n_vis=None):
        if tipo == "vectores3d":
            _base_vectores(n_vis)
        else:
            _base_superficie(n_vis)
        canvas.draw_idle()

    # ---------- animación (dibujo progresivo) ----------
    def _animar():
        if estado["anim_job"]:
            return
        if tipo == "vectores3d":
            total = len(spec.get("vectores", [])) + \
                    (1 if spec.get("combinacion") else 0)
        else:
            tx = spec.get("trayectoria")
            total = (len(tx) if tx else spec.get("steps", 12) + 1)

        def paso(i=1):
            _render(i)
            if i >= total:
                estado["anim_job"] = None
                return
            estado["anim_job"] = win.after(600, lambda: paso(i + 1))
        paso(1)

    # ---------- rotación automática ----------
    def _toggle_rot():
        if estado["rot_job"]:
            win.after_cancel(estado["rot_job"]); estado["rot_job"] = None
            btn_rot.config(text="⟳  Rotar")
            return
        btn_rot.config(text="⏸  Parar")

        def girar():
            ax.view_init(elev=ax.elev, azim=(ax.azim + 2) % 360)
            canvas.draw_idle()
            estado["rot_job"] = win.after(60, girar)
        girar()

    # ---------- barra inferior ----------
    barra = tk.Frame(win, bg=COLOR_PANEL)
    barra.pack(side="bottom", fill="x")
    tk.Label(barra, text="🖱 Arrastra con el ratón para rotar la vista",
             bg=COLOR_PANEL, fg=COLOR_TEXT2,
             font=("Consolas", 9)).pack(side="left", padx=10, pady=6)
    btn_anim = tk.Button(barra, text="▶  Animar", font=("Consolas", 10, "bold"),
                         bg=COLOR_OK, fg="white", relief="flat",
                         padx=12, pady=4, cursor="hand2", command=_animar)
    btn_anim.pack(side="left", padx=4, pady=6)
    btn_rot = tk.Button(barra, text="⟳  Rotar", font=("Consolas", 10, "bold"),
                        bg=COLOR_ACCENT, fg="#0f1419", relief="flat",
                        padx=12, pady=4, cursor="hand2", command=_toggle_rot)
    btn_rot.pack(side="left", padx=4, pady=6)

    def _cerrar():
        for j in ("rot_job", "anim_job"):
            if estado[j]:
                try:
                    win.after_cancel(estado[j])
                except Exception:
                    pass
        win.destroy()
    tk.Button(barra, text="Cerrar", font=("Consolas", 10, "bold"),
              bg=COLOR_BTNINAC, fg=COLOR_TEXT, relief="flat",
              padx=12, pady=4, cursor="hand2", command=_cerrar).pack(
        side="right", padx=10, pady=6)
    win.protocol("WM_DELETE_WINDOW", _cerrar)

    _render()


# =====================================================================
#  PERSISTENCIA SQLite — almacena cada respuesta y calcula dominio
#  por lección con un EMA (exponential moving average) que da más
#  peso a los errores recientes. La cola adaptativa muestrea las
#  lecciones más débiles.
# =====================================================================

try:
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _BASE_DIR = os.getcwd()
DB_PATH = os.path.join(_BASE_DIR, "progreso.db")

# Parámetro del EMA: α=0.3 → cada nueva respuesta cuenta 30 %.
# Mayor α = más reactivo a los últimos intentos; menor = más estable.
EMA_ALPHA = 0.3


def db_conectar():
    """Abre la conexión y crea las tablas si no existen."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS respuestas (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            seccion       TEXT    NOT NULL,
            leccion_idx   INTEGER NOT NULL,
            leccion_title TEXT,
            es_variante   INTEGER DEFAULT 0,
            correcta      INTEGER NOT NULL,  -- 0 o 1
            timestamp     TEXT    NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dominio (
            seccion       TEXT,
            leccion_idx   INTEGER,
            n_intentos    INTEGER DEFAULT 0,
            n_correctas   INTEGER DEFAULT 0,
            ema_acierto   REAL    DEFAULT 0.5,
            ultimo_visto  TEXT,
            PRIMARY KEY (seccion, leccion_idx)
        )
    """)
    conn.commit()
    return conn


def db_registrar(seccion, idx, titulo, correcta, es_variante=False):
    """Registra una respuesta y actualiza el EMA de dominio."""
    conn = db_conectar()
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
        INSERT INTO respuestas
            (seccion, leccion_idx, leccion_title, es_variante,
             correcta, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (seccion, idx, titulo, int(es_variante), int(correcta), ts))

    row = conn.execute("""
        SELECT n_intentos, n_correctas, ema_acierto
        FROM dominio WHERE seccion=? AND leccion_idx=?
    """, (seccion, idx)).fetchone()

    c_int = int(correcta)
    if row is None:
        n_int, n_cor = 1, c_int
        ema = (1 - EMA_ALPHA) * 0.5 + EMA_ALPHA * c_int
    else:
        n_int = row[0] + 1
        n_cor = row[1] + c_int
        ema = (1 - EMA_ALPHA) * row[2] + EMA_ALPHA * c_int

    conn.execute("""
        INSERT OR REPLACE INTO dominio
            (seccion, leccion_idx, n_intentos, n_correctas,
             ema_acierto, ultimo_visto)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (seccion, idx, n_int, n_cor, ema, ts))

    conn.commit()
    conn.close()


def db_cargar_dominio():
    """Devuelve {(seccion, idx): {intentos, correctas, ema, ultimo}}."""
    conn = db_conectar()
    rows = conn.execute("""
        SELECT seccion, leccion_idx, n_intentos, n_correctas,
               ema_acierto, ultimo_visto FROM dominio
    """).fetchall()
    conn.close()
    return {(r[0], r[1]): {"intentos": r[2], "correctas": r[3],
                            "ema": r[4], "ultimo": r[5]}
            for r in rows}


def db_estadisticas():
    """Devuelve resumen global y por sección."""
    conn = db_conectar()
    total = conn.execute(
        "SELECT COUNT(*) FROM respuestas").fetchone()[0]
    correctas = conn.execute(
        "SELECT COUNT(*) FROM respuestas WHERE correcta=1").fetchone()[0]
    por_seccion = conn.execute("""
        SELECT seccion, COUNT(*), SUM(correcta)
        FROM respuestas GROUP BY seccion ORDER BY seccion
    """).fetchall()
    conn.close()
    return total, correctas, por_seccion


def db_fallos_de_leccion(seccion, idx):
    """Cuenta cuántas veces se ha FALLADO una lección concreta."""
    conn = db_conectar()
    n = conn.execute("""
        SELECT COUNT(*) FROM respuestas
        WHERE seccion=? AND leccion_idx=? AND correcta=0
    """, (seccion, idx)).fetchone()[0]
    conn.close()
    return n


def db_lecciones_falladas(min_fallos=1):
    """Devuelve lecciones donde el usuario ha FALLADO al menos `min_fallos`
    veces. Ordenadas por una puntuación que premia:
      • más fallos absolutos (n_fallos)
      • mayor proporción fallos/intentos
      • fallos más RECIENTES (timestamp del último fallo)

    Retorna lista de tuplas: (seccion, leccion_idx, n_fallos, n_intentos,
                              ultimo_fallo_ts, puntuacion).
    La puntuación se usa luego en muestreo ponderado.
    """
    conn = db_conectar()
    rows = conn.execute("""
        SELECT
            seccion,
            leccion_idx,
            SUM(CASE WHEN correcta=0 THEN 1 ELSE 0 END)   AS fallos,
            COUNT(*)                                       AS intentos,
            MAX(CASE WHEN correcta=0 THEN timestamp END)   AS ultimo_fallo
        FROM respuestas
        GROUP BY seccion, leccion_idx
        HAVING fallos >= ?
    """, (min_fallos,)).fetchall()
    conn.close()

    if not rows:
        return []

    # Calculamos puntuación: fallos/intentos (0..1) +  bonus por recencia.
    # Cuanto más reciente el último fallo, MÁS peso (spaced retrieval).
    ahora = time.time()
    resultado = []
    for sec, idx, fallos, intentos, ultimo in rows:
        ratio = fallos / max(intentos, 1)
        recencia = 0.5
        if ultimo:
            try:
                ts = time.mktime(time.strptime(ultimo, "%Y-%m-%d %H:%M:%S"))
                dias = (ahora - ts) / 86400.0
                # decae con vida media de ~5 días
                recencia = 2 ** (-dias / 5.0)
            except Exception:
                pass
        puntuacion = ratio * 0.6 + recencia * 0.3 + min(fallos / 5.0, 0.1)
        resultado.append((sec, idx, fallos, intentos, ultimo, puntuacion))

    # Ordenamos por puntuación descendente
    resultado.sort(key=lambda r: r[5], reverse=True)
    return resultado


# =====================================================================
#  GENERADOR DE VARIANTES NUEVAS PARA MODO "🎯 REFORZAR"
# =====================================================================
#
# Cuando una lección sale como DÉBIL en estadísticas, queremos no solo
# repetirla sino ENRIQUECERLA con ejemplos extra que apliquen el mismo
# concepto a valores distintos. Para circuitos esto es fácil: tomamos
# el diagrama, lo evaluamos con valores aleatorios de entrada, y
# pedimos al usuario que prediga la salida.
#
# Para lecciones puramente conceptuales (info, tf, mc sin diagrama)
# devolvemos la lección original con opciones barajadas — es lo mejor
# que podemos hacer sin acceder al texto.

def _eval_circuito(diagrama, valores):
    """Evalúa un diagrama con un dict {var:0|1} y devuelve {gate_id: 0|1}."""
    gates = {g["id"]: g for g in diagrama["gates"]}
    ids = list(gates.keys())
    # Orden topológico simple (igual que en _orden_topologico)
    orden, visit = [], set()
    def dfs(n):
        if n in visit:
            return
        visit.add(n)
        for d in gates[n]["inputs"]:
            if d in gates:
                dfs(d)
        orden.append(n)
    for gid in ids:
        dfs(gid)
    res = dict(valores)
    for gid in orden:
        g = gates[gid]
        in_vals = [res[n] for n in g["inputs"]]
        res[gid] = _EVAL_PUERTA[g["type"]](in_vals)
    return res


def generar_variantes_leccion(leccion, n, semilla):
    """Devuelve una lista de hasta `n` variantes de la lección.

    Estrategia:
      • Si la lección tiene `diagram`: genera preguntas mc preguntando
        el valor de salida del circuito para combinaciones distintas
        de las entradas. La respuesta correcta se calcula por simulación.
      • En otro caso, devuelve la lección original con opciones
        barajadas (efecto variabilidad — Sweller 2019).
    Cada variante reutiliza el MISMO diagrama, así el usuario puede
    pulsar «▶ Animar» y ver cómo cambia la salida con cada combinación.
    """
    rnd = random.Random(semilla)
    diagrama = leccion.get("diagram")
    if not diagrama or not diagrama.get("vars"):
        # Sin circuito → variante por barajado (lo único que podemos)
        return [aplicar_variante(leccion, semilla + i) for i in range(n)]

    vars_list = diagrama["vars"]
    # Todas las combinaciones posibles de entradas (2^len)
    combos = list(product([0, 1], repeat=len(vars_list)))
    rnd.shuffle(combos)
    variantes = []
    salida_id = diagrama["outputs"][0]["from"] if diagrama.get("outputs") else None

    gate_types = {g["id"]: g["type"] for g in diagrama["gates"]}
    gate_order = [g["id"] for g in diagrama["gates"]]

    for combo in combos[:n]:
        valores = dict(zip(vars_list, combo))
        resultado = _eval_circuito(diagrama, valores)
        salida = resultado[salida_id] if salida_id else 0

        nuevo_diag = dict(diagrama)
        nuevo_diag["trace_values"] = valores

        args = ", ".join(f"{v}={valores[v]}" for v in vars_list)
        pasos = "\n".join(
            f"  {gid} ({gate_types[gid]}) → {resultado[gid]}"
            for gid in gate_order
        )

        variante = {
            "title": leccion["title"] + "  · refuerzo",
            "nivel": leccion.get("nivel", ""),
            "theory":
                "REFUERZO: vuelve a aplicar la receta paso a paso\n"
                "sobre el mismo circuito con valores nuevos.\n\n"
                "  1) Identifica cada puerta del diagrama.\n"
                "  2) Empieza por las puertas cuyas entradas son\n"
                "     variables (a la izquierda).\n"
                "  3) Propaga sus salidas a las puertas siguientes.\n"
                "  4) Llega a la salida final f.\n\n"
                "💡 Antes de pulsar 'Comprobar', usa «▶ Animar» con\n"
                "    los valores ya cargados para VERIFICAR tu cálculo.",
            "example":
                f"Vamos a evaluar el circuito con  {args}.\n"
                "Haz tú primero la cuenta a mano, y solo después\n"
                "pulsa «▶ Animar» para comprobar el resultado.\n\n"
                "Recuerda los patrones rápidos:\n"
                "  AND → 1 SOLO si ambas son 1\n"
                "  OR  → 0 SOLO si ambas son 0\n"
                "  XOR → 1 cuando son DISTINTAS\n"
                "  NOT → invierte\n"
                "  NAND/NOR/XNOR → invierten las anteriores",
            "diagram": nuevo_diag,
            "q_type": "mc",
            "question": f"Para el circuito con  {args}, ¿cuánto vale f?",
            "options": ["0", "1", "No se puede saber", "Depende"],
            "correct": int(salida),
            "explanation":
                f"Propagación con {args}:\n{pasos}\n"
                f"  ⇒  f = {salida}",
        }
        variantes.append(variante)
    return variantes


# =====================================================================
#  GENERADOR METODOLÓGICO — variantes con worked-example + self-explain
# =====================================================================
#
# Versión enriquecida del generador. Para una lección FALLADA construye
# una secuencia de "cards" que aplica las 4 prácticas con más evidencia
# en aprendizaje matemático:
#
#   ① Worked example primero (Sweller 2019, d ≈ 0.6 en novatos)
#        → Se inyecta una card "info" que muestra la teoría y un caso
#          resuelto antes de cualquier pregunta.
#
#   ② Self-explanation (Hodds, Alcock, Inglis 2014, d = 0.95)
#        → Se invita a aplicar las 4 preguntas en la primera card.
#
#   ③ Retrieval practice activa (Freeman 2014, OR = 1.5)
#        → Las siguientes cards SON preguntas: el usuario PRODUCE.
#
#   ④ Interleaving (Brunmair & Richter 2019, g = 0.34 en mates)
#        → El llamador mezcla variantes de distintas lecciones falladas
#          (anti-clustering, ya implementado).
#
# Esta función NO mezcla — solo expande UNA lección a N cards. El
# llamador se encarga del interleaving.

def generar_banco_metodologico(leccion, n_variantes, semilla):
    """Devuelve una lista de cards para una sola lección.
    Estructura: 1 card "info" (worked example) + N preguntas variantes.

    Si la lección tiene `diagram` (circuito): genera hasta `n_variantes`
    preguntas mc evaluando el circuito con combinaciones distintas de
    entradas. Si no, genera `n_variantes` barajados de la mc original.
    """
    cards = []

    # ─── Card 1: WORKED EXAMPLE + invitación a self-explanation ──────
    worked = {
        "title": leccion["title"] + "  · estudio guiado",
        "nivel": leccion.get("nivel", ""),
        "theory":
            "🧠  MOMENTO DE ESTUDIO (worked-example mode)\n"
            "════════════════════════════════════════════\n\n"
            "Esta lección la has FALLADO antes. Antes de las\n"
            "preguntas, vamos a re-estudiarla aplicando 2\n"
            "técnicas con evidencia muy fuerte:\n\n"
            "  ① WORKED EXAMPLE (Sweller 2019)\n"
            "     Lee el ejemplo de abajo SIN saltarte pasos.\n"
            "     Cubre la solución con la mano y trata de\n"
            "     anticipar cada línea antes de descubrirla.\n\n"
            "  ② SELF-EXPLANATION (Hodds, Alcock, Inglis 2014)\n"
            "     Tras leer, formúlate las 4 preguntas:\n"
            "       1. ¿Entiendo las ideas usadas?\n"
            "       2. ¿Por qué se usa ESTA idea aquí?\n"
            "       3. ¿Cómo se enlaza con lo que ya sé?\n"
            "       4. ¿Mi explicación responde a mis dudas?\n\n"
            "Cuando estés listo, pulsa Siguiente para empezar\n"
            "con las preguntas de refuerzo.\n\n"
            "─── TEORÍA ORIGINAL ───────────────────────────\n\n"
            + leccion["theory"],
        "example":
            leccion.get("example", "") + "\n\n"
            "💡 Antes de responder las próximas preguntas,\n"
            "   reproduce este ejemplo con números distintos\n"
            "   en una hoja de papel. Producir activa es lo\n"
            "   que graba el patrón en memoria a largo plazo.",
        "diagram": leccion.get("diagram"),
        "q_type": "info",
        "question": "",
        "options": [],
        "correct": None,
        "explanation": "",
    }
    cards.append(worked)

    # ─── Cards 2..N: variantes con preguntas (retrieval activo) ──────
    variantes = generar_variantes_leccion(leccion, n_variantes, semilla)
    cards.extend(variantes)

    return cards


# =====================================================================
#  Variabilidad (Sweller — variability effect)
#  Barajamos el orden de las opciones de las MC para que el usuario no
#  memorice "era la B"; le obliga a re-leer y razonar.
# =====================================================================

def aplicar_variante(leccion, semilla):
    """Devuelve una versión de la lección con opciones barajadas.
    Solo afecta a preguntas tipo 'mc'. Las 'tt' y 'tf' se devuelven
    sin cambios para no romper la semántica."""
    if leccion["q_type"] != "mc":
        return leccion
    rnd = random.Random(semilla)
    orden = list(range(len(leccion["options"])))
    rnd.shuffle(orden)
    nueva = dict(leccion)
    nueva["options"] = [leccion["options"][i] for i in orden]
    nueva["correct"] = orden.index(leccion["correct"])
    return nueva


def _aclarar_hex(hex_color, factor=1.15):
    """Devuelve un hex ligeramente más claro (factor>1) o más oscuro."""
    try:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


def _bind_hover(btn, color_base, color_hover=None):
    """Asocia eventos Enter/Leave al botón para resaltar al pasar."""
    if color_hover is None:
        color_hover = _aclarar_hex(color_base, 1.18)
    btn.bind("<Enter>", lambda e, b=btn, c=color_hover: b.config(bg=c))
    btn.bind("<Leave>", lambda e, b=btn, c=color_base: b.config(bg=c))


# =====================================================================
#  GLOSARIO automático — explica la jerga EN LENGUAJE LLANO, en línea.
#  La GUI inserta la aclaración entre paréntesis la PRIMERA vez que un
#  término aparece en la pregunta / opciones / explicación de cada
#  lección. Mantiene el término técnico (sirve para el examen) y añade
#  su significado sencillo al lado. Términos multi-palabra van PRIMERO
#  para que ganen sobre los de una sola palabra.
# =====================================================================
GLOSARIO = {
    # --- álgebra lineal (multi-palabra primero) ---
    "producto escalar": "multiplicar componente a componente y sumar; mide cuánto se parecen",
    "combinación lineal": "sumar vectores multiplicados por números",
    "linealmente independientes": "ninguno se obtiene de los demás",
    "linealmente independiente": "ninguno se obtiene de los demás",
    "linealmente dependientes": "alguno se obtiene de los demás",
    "producto cartesiano": "todos los pares posibles (a, b)",
    "valor propio": "factor por el que la matriz estira una dirección",
    "vector propio": "dirección que la matriz solo estira, sin girar",
    "derivada parcial": "derivar respecto a una variable dejando fijas las demás",
    "espacio muestral": "todos los resultados posibles",
    "máxima verosimilitud": "elegir el modelo que hace MÁS probables los datos vistos",
    "ángulo recto": "de 90°, en forma de L",
    # --- lógica ---
    "proposición": "frase que es verdadera o falsa, sin discusión",
    "tautología": "frase que SIEMPRE es verdadera",
    "contradicción": "frase que SIEMPRE es falsa",
    "contingencia": "a veces verdadera, a veces falsa",
    "contingente": "a veces verdadera, a veces falsa",
    "conjunción": "el 'Y' lógico",
    "disyunción": "el 'O' lógico",
    "negación": "el 'NO' lógico, invierte el valor",
    "implicación": "el 'si... entonces'",
    "bicondicional": "'si y solo si', se cumple en los dos sentidos",
    "antecedente": "la parte del 'si' (la condición)",
    "consecuente": "la parte del 'entonces' (la consecuencia)",
    "equivalentes": "que valen lo mismo en todos los casos",
    "equivalencia": "que valen lo mismo en todos los casos",
    "predicado": "afirmación con variables, p. ej. 'x es par'",
    "cuantificador": "palabra de cantidad: 'para todo' o 'existe'",
    "universal": "'para todo' (∀)",
    "existencial": "'existe al menos uno' (∃)",
    "inductiva": "ir de casos concretos a una regla general",
    "inducción": "ir de casos concretos a una regla general",
    "asintótica": "cómo crece cuando el tamaño se hace muy grande",
    "asintótico": "cómo crece cuando el tamaño se hace muy grande",
    "conmutativo": "el orden no cambia el resultado",
    "conmuta": "el orden no cambia el resultado",
    "asociativa": "da igual cómo agrupes los términos",
    "distributiva": "repartir una operación sobre otra",
    "idempotencia": "repetir algo no cambia el resultado",
    # --- funciones booleanas / circuitos ---
    "booleana": "que solo vale 0 o 1",
    # --- grafos ---
    "vértice": "punto del grafo",
    "vértices": "puntos del grafo",
    "arista": "línea que une dos puntos",
    "aristas": "líneas que unen puntos",
    "conexo": "de una sola pieza: se llega de cualquier punto a cualquier otro",
    "componentes": "los trozos separados de un grafo",
    "dirigido": "con flechas; cada línea tiene un sentido",
    "adyacencia": "qué punto está unido con cuál",
    "grado": "número de líneas que tocan un vértice",
    # --- conjuntos ---
    "subconjunto": "conjunto contenido dentro de otro",
    "intersección": "lo que está en AMBOS conjuntos a la vez",
    "cardinal": "número de elementos",
    # --- aplicaciones / funciones ---
    "inyectiva": "entradas distintas dan salidas distintas",
    "sobreyectiva": "alcanza todas las salidas posibles",
    "suprayectiva": "alcanza todas las salidas posibles",
    "biyectiva": "uno a uno y además alcanza todas las salidas",
    "dominio": "el conjunto de entradas",
    "aplicación": "función: regla que asigna a cada entrada una única salida",
    "aplicaciones": "funciones: reglas que asignan a cada entrada una única salida",
    "composición": "encadenar dos funciones, una tras otra",
    # --- combinatoria ---
    "permutación": "ordenar TODOS los elementos (importa el orden)",
    "permutaciones": "ordenar TODOS los elementos (importa el orden)",
    "variación": "elegir unos cuantos Y ordenarlos (importa el orden)",
    "variaciones": "elegir unos cuantos Y ordenarlos (importa el orden)",
    "combinaciones": "elegir sin que importe el orden",
    # --- álgebra lineal (una palabra) ---
    "ortogonales": "perpendiculares, en ángulo recto de 90°",
    "ortogonal": "perpendicular, en ángulo recto de 90°",
    "escalar": "un número suelto que multiplica",
    "vectores": "listas ordenadas de números (como flechas)",
    "vector": "lista ordenada de números (como una flecha)",
    "matrices": "tablas de números en filas y columnas",
    "matriz": "tabla de números en filas y columnas",
    "determinante": "número que dice si la matriz se puede invertir",
    "invertible": "que se puede 'deshacer' (tiene inversa)",
    "regular": "que tiene inversa (se puede deshacer)",
    "rango": "número de filas/columnas realmente independientes",
    "traspuesta": "la matriz con filas y columnas intercambiadas",
    "diagonalizar": "reescribir la matriz en su forma más simple",
    "factorización": "descomponer en producto de matrices más simples",
    "base": "conjunto mínimo de vectores que genera todo el espacio",
    "dimensión": "número de vectores de una base",
    "tensor": "vector/matriz generalizado a más dimensiones",
    "norma": "longitud (tamaño) de un vector",
    # --- cálculo ---
    "derivada": "ritmo de cambio; la pendiente de la curva",
    "pendiente": "lo inclinada que está la recta",
    "gradiente": "la derivada con varias variables; apunta a la subida más rápida",
    "hessiana": "tabla de segundas derivadas (mide la curvatura)",
    "monotonía": "si la función crece o decrece",
    "integral": "el área bajo la curva",
    "multivariable": "con varias variables a la vez",
    "direccional": "el ritmo de cambio en una dirección concreta",
    "continuidad": "sin saltos: se dibuja sin levantar el lápiz",
    "continua": "sin saltos: se dibuja sin levantar el lápiz",
    # --- probabilidad / estadística ---
    "equiprobables": "todos con la misma probabilidad",
    "condicionada": "probabilidad sabiendo que ya ocurrió otra cosa",
    "independientes": "que no se influyen entre sí",
    "independencia": "que no se influyen entre sí",
    "esperanza": "el valor medio que se espera",
    "varianza": "cuánto se dispersan los valores respecto a la media",
    "estimador": "fórmula para aproximar un valor desconocido a partir de datos",
    "verosimilitud": "qué tan probables son los datos según el modelo",
    "estocástico": "que evoluciona con azar",
    "estocástica": "que evoluciona con azar",
    "estacionaria": "que ya no cambia con el tiempo",
    "distribución": "cómo se reparten las probabilidades entre los resultados",
    "aleatoria": "que depende del azar",
    "aleatorio": "que depende del azar",
    "suceso": "un resultado o grupo de resultados posibles",
}


def _sin_tildes(s):
    """Quita tildes (á→a…) conservando la ñ. Mapea 1 char→1 char, así que
    las posiciones del texto NO cambian: sirve para casar con/sin acentos."""
    tabla = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU")
    return s.translate(tabla)


def _aplicar_glosario(texto, usados):
    """Inserta entre paréntesis el significado llano de los términos del
    GLOSARIO que aparezcan en `texto`, solo la primera vez (controlado por
    el conjunto `usados`, compartido en toda la lección). No solapa términos.
    Insensible a tildes. No modifica los datos: opera sobre el texto mostrado."""
    if not texto:
        return texto
    plano = _sin_tildes(texto)        # mismas posiciones que `texto`
    inserciones = []                  # (posición_fin, texto_a_insertar)
    ocupado = []                      # rangos ya cubiertos, para no solapar
    for term, expl in GLOSARIO.items():
        if term in usados:
            continue
        patron = r'(?<!\w)' + re.escape(_sin_tildes(term)) + r'\w*(?!\w)'
        m = re.search(patron, plano, re.IGNORECASE)
        if not m:
            continue
        s, e = m.start(), m.end()
        if any(s < oe and e > os for os, oe in ocupado):
            continue
        inserciones.append((e, " (" + expl + ")"))
        ocupado.append((s, e))
        usados.add(term)
    for pos, ins in sorted(inserciones, key=lambda t: t[0], reverse=True):
        texto = texto[:pos] + ins + texto[pos:]
    return texto


class AppLogica(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Aprender Lógica — Matemáticas para IA (VIU)")
        self.geometry("1180x760")
        self.minsize(1000, 680)
        self.configure(bg=COLOR_BG)

        # Estado
        self.seccion_actual = list(LECCIONES.keys())[0]
        self.idx_leccion = 0
        self.respuesta_dada = False

        # --- Tracking de progreso (active learning / Freeman 2014) -------
        # Estado por lección: None=no hecha, "ok"=correcta, "fail"=incorrecta
        self.progreso = {sec: [None] * len(lecs)
                         for sec, lecs in LECCIONES.items()}

        # --- Modo MEZCLADO / interleaving (Brunmair & Richter 2019) ------
        # Cuando está activo, las preguntas se sacan en orden aleatorio
        # de las secciones 1.1 a 1.5 (no de Metodología).
        self.modo_mezclado = False
        self.cola_mezclada = []   # lista de tuplas (seccion, idx)
        self.pos_mezclada = 0

        # --- Modo ADAPTATIVO (retrieval + variabilidad + interleaving) ---
        # Selecciona preguntas con muestreo ponderado por debilidad,
        # leyendo la BD SQLite de respuestas previas.
        self.modo_adaptativo = False
        self.cola_adaptativa = []
        self.pos_adaptativa = 0
        self.variante_semilla = 0  # se renueva al cargar la lección

        # --- Modo PROGRESIVO (orden por dificultad: básico→intermedio→experto)
        self.modo_progresivo = False
        self.cola_progresiva = []
        self.pos_progresiva = 0

        # --- Modo REFUERZO (lección débil + N variantes nuevas) ----------
        # Se activa desde la ventana de Estadísticas con un botón
        # "🎯 Reforzar" junto a cada lección débil. Genera variantes
        # con valores nuevos del circuito y las muestra encadenadas
        # para subir el dominio de ese concepto concreto.
        self.modo_refuerzo = False
        self.cola_refuerzo = []           # lista de (sec, idx, leccion_var)
        self.pos_refuerzo = 0
        self.refuerzo_titulo = ""         # nombre del foco (p.ej. lección X)

        # --- Modo POR NIVEL (preguntas de un nivel en orden ALEATORIO) ---
        # El usuario elige básico/intermedio/experto y recibe preguntas
        # SOLO de ese nivel, mezcladas entre todas las secciones
        # (interleaving — Brunmair 2019). Distinto de Progresiva, que
        # va en orden básico→intermedio→experto.
        self.modo_nivel = False
        self.cola_nivel = []
        self.pos_nivel = 0
        self.nivel_filtro = ""            # "básico" / "intermedio" / "experto"

        # Inicializar BD y cargar dominio
        self.dominio = db_cargar_dominio()
        # Sincronizar self.progreso con el dominio persistido
        for (sec, i), datos in self.dominio.items():
            if sec in self.progreso and i < len(self.progreso[sec]):
                # Marca como 'ok' si EMA ≥ 0.7, si no 'fail'
                self.progreso[sec][i] = "ok" if datos["ema"] >= 0.7 else "fail"

        # Fuentes (tema "Consola IA": monoespaciada protagonista, con
        # selección robusta de la mejor familia disponible en el sistema)
        _fams = set(tkfont.families(self))
        def _pick(prefs):
            for f in prefs:
                if f in _fams:
                    return f
            return "Consolas"
        _disp = _pick(["Cascadia Code", "JetBrains Mono", "Consolas"])
        _mono = _pick(["Cascadia Mono", "Consolas"])
        self.font_titulo = tkfont.Font(family=_disp, size=17, weight="bold")
        self.font_subt   = tkfont.Font(family=_disp, size=12, weight="bold")
        self.font_normal = tkfont.Font(family=_mono, size=11)
        self.font_mono   = tkfont.Font(family=_mono, size=11)
        self.font_btn    = tkfont.Font(family=_disp, size=10, weight="bold")

        self._build_ui()
        self._cargar_leccion()

    # -----------------------------------------------------------------
    def _build_ui(self):
        # --- Estilo oscuro para widgets ttk (scrollbars) ----------------
        _st = ttk.Style(self)
        try:
            _st.theme_use("clam")
        except Exception:
            pass
        for _orient in ("Vertical.TScrollbar", "Horizontal.TScrollbar"):
            _st.configure(_orient, troughcolor=COLOR_BG,
                          background=COLOR_BTNINAC, bordercolor=COLOR_BG,
                          arrowcolor=COLOR_TEXT2, relief="flat")
            _st.map(_orient, background=[("active", COLOR_ACCENT)])

        # --- Cabecera (consola: fondo oscuro + prompt neón) -------------
        cab = tk.Frame(self, bg=COLOR_PANEL, height=58)
        cab.pack(side="top", fill="x")
        tk.Label(cab,
                 text="▮ APRENDER LÓGICA · Matemáticas para IA (VIU)",
                 fg=COLOR_ACCENT, bg=COLOR_PANEL,
                 font=self.font_titulo).pack(side="left", padx=20, pady=10)
        # filo de acento neón bajo la cabecera
        tk.Frame(self, bg=COLOR_OK, height=2).pack(side="top", fill="x")

        # --- Barra de CAPÍTULOS (nivel 1) + sub-secciones (nivel 2) -----
        # Con 22+ secciones la barra de 1 sola fila desborda. Agrupamos
        # por prefijo de capítulo y mostramos las sub-secciones del
        # capítulo activo.
        self.capitulos = self._agrupar_por_capitulo()
        self.capitulo_actual = next(iter(self.capitulos.keys()))

        barra_cap = tk.Frame(self, bg=COLOR_BG)
        barra_cap.pack(side="top", fill="x", padx=10, pady=(8, 2))
        self.btns_capitulo = {}
        for codigo, info in self.capitulos.items():
            b = tk.Button(barra_cap, text=info["label"],
                          font=self.font_btn,
                          bg=COLOR_BTNINAC, fg=COLOR_TEXT,
                          activebackground=COLOR_ACCENT,
                          relief="flat", padx=14, pady=8,
                          cursor="hand2",
                          command=lambda c=codigo: self._cambiar_capitulo(c))
            b.pack(side="left", padx=4)
            self.btns_capitulo[codigo] = b

        # Barra de sub-secciones del capítulo activo
        barra = tk.Frame(self, bg=COLOR_BG)
        barra.pack(side="top", fill="x", padx=10, pady=(0, 8))
        self.barra_subsecciones = barra
        self.btns_seccion = {}

        # --- Botones de práctica avanzada (en la barra de capítulos) ---
        # 📊 Estadísticas (lee la BD)
        tk.Button(barra_cap, text="📊  Estadísticas",
                  font=self.font_btn,
                  bg=COLOR_BTNINAC, fg=COLOR_TEXT,
                  relief="flat", padx=10, pady=8, cursor="hand2",
                  command=self._mostrar_estadisticas).pack(side="right",
                                                            padx=4)

        # 🎲 Mezclado (interleaving — orden aleatorio)
        self.btn_mezclado = tk.Button(
            barra_cap, text="🎲  Mezclada",
            font=self.font_btn,
            bg=COLOR_ACCENT2, fg="white",
            activebackground=COLOR_ACCENT2,
            relief="flat", padx=12, pady=8, cursor="hand2",
            command=self._toggle_mezclado)
        self.btn_mezclado.pack(side="right", padx=4)

        # 🧠 Adaptativa (ponderada por debilidad + variantes)
        self.btn_adaptativa = tk.Button(
            barra_cap, text="🧠  Adaptativa",
            font=self.font_btn,
            bg="#d29922", fg="white",
            activebackground="#d29922",
            relief="flat", padx=12, pady=8, cursor="hand2",
            command=self._toggle_adaptativa)
        self.btn_adaptativa.pack(side="right", padx=4)

        # 🎯 Progresiva (orden por dificultad: básico → intermedio → experto)
        self.btn_progresiva = tk.Button(
            barra_cap, text="🎯  Progresiva",
            font=self.font_btn,
            bg="#3fb950", fg="white",
            activebackground="#3fb950",
            relief="flat", padx=12, pady=8, cursor="hand2",
            command=self._toggle_progresiva)
        self.btn_progresiva.pack(side="right", padx=4)

        # 🎯 Refuerzo (solo se enciende desde 📊 Estadísticas; aquí
        #    el botón sirve para SALIR del modo si está activo)
        self.btn_refuerzo = tk.Button(
            barra_cap, text="🎯  Refuerzo",
            font=self.font_btn,
            bg="#da3633", fg="white",
            activebackground="#da3633",
            relief="flat", padx=12, pady=8, cursor="hand2",
            command=self._toggle_refuerzo)
        self.btn_refuerzo.pack(side="right", padx=4)

        # 🎰 Por nivel (elige básico/intermedio/experto → aleatorio)
        self.btn_nivel = tk.Button(
            barra_cap, text="🎰  Por nivel",
            font=self.font_btn,
            bg="#8957e5", fg="white",
            activebackground="#8957e5",
            relief="flat", padx=12, pady=8, cursor="hand2",
            command=self._toggle_nivel)
        self.btn_nivel.pack(side="right", padx=4)

        # Aplicar hover a los botones de modos (efecto táctil)
        _bind_hover(self.btn_mezclado,   COLOR_ACCENT2)
        _bind_hover(self.btn_adaptativa, "#d29922")
        _bind_hover(self.btn_progresiva, "#3fb950")
        _bind_hover(self.btn_refuerzo,   "#da3633")
        _bind_hover(self.btn_nivel,      "#8957e5")

        # Render inicial de las sub-secciones (capítulo activo)
        self._render_subsecciones()

        # --- Cabecera de lección + barra de progreso por sección --------
        cabeza = tk.Frame(self, bg=COLOR_BG)
        cabeza.pack(side="top", fill="x", padx=14, pady=(8, 4))

        self.lbl_titulo = tk.Label(cabeza, text="",
                                   font=self.font_subt,
                                   bg=COLOR_BG, fg=COLOR_TEXT,
                                   anchor="w")
        self.lbl_titulo.pack(side="left", anchor="w")

        # Strip de puntitos de progreso (⬤ ⬤ ⬤ ○ ✗ ○ ...)
        self.lbl_dots = tk.Label(cabeza, text="",
                                 font=self.font_normal,
                                 bg=COLOR_BG, fg=COLOR_TEXT2)
        self.lbl_dots.pack(side="right")

        # --- Cuerpo: teoría+ejemplo (izq) + pregunta (der) --------------
        # Va dentro de un Canvas con SCROLL vertical para que el pie de
        # página (botón «Siguiente») quede SIEMPRE visible, aunque la
        # lección sea larga (p. ej. tablas de verdad con diagrama).
        _wrap = tk.Frame(self, bg=COLOR_BG)
        _wrap.pack(side="top", fill="both", expand=True)
        self._vcanvas = tk.Canvas(_wrap, bg=COLOR_BG, highlightthickness=0,
                                  bd=0, height=420)
        _vsb = ttk.Scrollbar(_wrap, orient="vertical",
                             command=self._vcanvas.yview)
        self._vcanvas.configure(yscrollcommand=_vsb.set)
        _vsb.pack(side="right", fill="y")
        self._vcanvas.pack(side="left", fill="both", expand=True)

        cuerpo = tk.Frame(self._vcanvas, bg=COLOR_BG)
        self._cuerpo_win = self._vcanvas.create_window(
            (10, 4), window=cuerpo, anchor="nw")

        def _ajustar_scroll(_e=None):
            self._vcanvas.configure(scrollregion=self._vcanvas.bbox("all"))
        cuerpo.bind("<Configure>", _ajustar_scroll)

        def _ajustar_ancho(e):
            self._vcanvas.itemconfigure(self._cuerpo_win,
                                        width=max(1, e.width - 20))
        self._vcanvas.bind("<Configure>", _ajustar_ancho)

        def _rueda(e):
            self._vcanvas.yview_scroll(int(-e.delta / 120), "units")
        self._vcanvas.bind_all("<MouseWheel>", _rueda)

        # Panel izquierdo dividido en TEORÍA (arriba) + EJEMPLO RESUELTO
        # (abajo). Aplicar Sweller (worked-example effect): el ejemplo
        # resuelto se estudia ANTES de intentar la pregunta.
        izq = tk.Frame(cuerpo, bg=COLOR_BG)
        izq.pack(side="left", fill="both", expand=True, padx=(0, 6))

        # -- Sub-panel 1: TEORÍA --
        teoria_panel = tk.LabelFrame(
            izq, text="  📖  TEORÍA  ",
            bg=COLOR_THEORY, font=self.font_subt, fg=COLOR_TEXT,
            labelanchor="nw", bd=1, relief="solid")
        teoria_panel.pack(side="top", fill="both", expand=True, pady=(0, 4))

        self.txt_teoria = tk.Text(teoria_panel, wrap="word",
                                  bg=COLOR_THEORY, fg=COLOR_TEXT,
                                  font=self.font_mono,
                                  bd=0, padx=14, pady=12,
                                  state="disabled")
        self.txt_teoria.pack(side="left", fill="both", expand=True)
        sb1 = ttk.Scrollbar(teoria_panel, command=self.txt_teoria.yview)
        sb1.pack(side="right", fill="y")
        self.txt_teoria.configure(yscrollcommand=sb1.set)

        # -- Sub-panel 2: EJEMPLO RESUELTO --
        ej_panel = tk.LabelFrame(
            izq, text="  📚  EJEMPLO RESUELTO  (estúdialo PRIMERO) ",
            bg=COLOR_EXAMPLE, font=self.font_subt, fg=COLOR_ACCENT,
            labelanchor="nw", bd=1, relief="solid")
        ej_panel.pack(side="top", fill="both", expand=True, pady=(4, 0))

        # Sub-sub-panel del ejemplo: texto + (opcional) canvas con diagrama
        ej_interior = tk.Frame(ej_panel, bg=COLOR_EXAMPLE)
        ej_interior.pack(side="left", fill="both", expand=True)

        self.txt_ejemplo = tk.Text(ej_interior, wrap="word",
                                   bg=COLOR_EXAMPLE, fg=COLOR_TEXT,
                                   font=self.font_mono, height=6,
                                   bd=0, padx=14, pady=10,
                                   state="disabled")
        self.txt_ejemplo.pack(side="top", fill="x")

        # Canvas para diagramas de puertas / circuitos (oculto si no aplica)
        self.canvas_diagrama = tk.Canvas(
            ej_interior, bg="#0d1117",
            height=220, bd=0, highlightthickness=1,
            highlightbackground="#2f3b48")
        # Lo packeamos solo cuando hay diagrama (gestionado en _cargar_leccion)

        # Estado del animador
        self._diagrama_modelo = None
        self._anim_running = False
        self._anim_inputs = {}   # entradas elegidas por el usuario para animar

        # Barra de controles de animación + leyenda. Aparece bajo el canvas
        # cuando la lección tiene diagrama. Apoya el "active visual learning"
        # (Freeman 2014) y permite ver la propagación señal a señal.
        self.frame_anim = tk.Frame(ej_interior, bg=COLOR_EXAMPLE)

        # Botones de control (▶ Animar / ⏮ Reset)
        self.btn_animar = tk.Button(
            self.frame_anim, text="▶  Animar señales",
            font=self.font_btn,
            bg=COLOR_OK, fg="white", relief="flat",
            padx=12, pady=4, cursor="hand2",
            command=self._animar_circuito)
        self.btn_animar.pack(side="left", padx=(6, 4), pady=4)

        self.btn_reset_anim = tk.Button(
            self.frame_anim, text="⏮  Reiniciar",
            font=self.font_btn,
            bg=COLOR_BTNINAC, fg=COLOR_TEXT, relief="flat",
            padx=10, pady=4, cursor="hand2",
            command=self._reset_animacion)
        self.btn_reset_anim.pack(side="left", padx=4, pady=4)

        # Sub-zona donde aparecerán Entry para que el usuario cambie
        # las entradas (x, y, z, …) antes de animar.
        self.zona_inputs_anim = tk.Frame(self.frame_anim, bg=COLOR_EXAMPLE)
        self.zona_inputs_anim.pack(side="left", padx=(8, 6))

        # Leyenda de colores
        self.lbl_leyenda = tk.Label(
            self.frame_anim,
            text="●  1  (verde)     ●  0  (rojo)     ●  sin propagar",
            bg=COLOR_EXAMPLE, fg=COLOR_TEXT2,
            font=("Consolas", 9))
        self.lbl_leyenda.pack(side="right", padx=6)

        # Barra de animación para VISUALES (descenso, vectores, markov).
        # Se empaqueta solo cuando la lección trae visual con "animate".
        self.frame_anim_vis = tk.Frame(ej_interior, bg=COLOR_EXAMPLE)
        self._visual_actual = None        # visual con animación pendiente
        self._anim_vis_running = False
        self.btn_animar_vis = tk.Button(
            self.frame_anim_vis, text="▶  Animar",
            font=self.font_btn, bg=COLOR_OK, fg="white",
            relief="flat", padx=12, pady=4, cursor="hand2",
            command=self._animar_visual)
        self.btn_animar_vis.pack(side="left", padx=(6, 4), pady=4)
        self.lbl_anim_vis = tk.Label(
            self.frame_anim_vis, text="",
            bg=COLOR_EXAMPLE, fg=COLOR_TEXT2, font=("Consolas", 9))
        self.lbl_anim_vis.pack(side="left", padx=8)
        # Botón de vista 3D (Matplotlib); oculto salvo lecciones con visual3d
        self._visual3d_actual = None
        self.btn_3d = tk.Button(
            self.frame_anim_vis, text="🧊  Ver en 3D",
            font=self.font_btn, bg=COLOR_ACCENT2, fg="white",
            relief="flat", padx=12, pady=4, cursor="hand2",
            command=self._abrir_3d)
        _bind_hover(self.btn_3d, COLOR_ACCENT2)

        sb2 = ttk.Scrollbar(ej_panel, command=self.txt_ejemplo.yview)
        sb2.pack(side="right", fill="y")
        self.txt_ejemplo.configure(yscrollcommand=sb2.set)

        # Pregunta (derecha)
        preg_panel = tk.LabelFrame(cuerpo, text="  ✏  PREGUNTA  ",
                                   bg=COLOR_PANEL,
                                   font=self.font_subt, fg=COLOR_TEXT,
                                   labelanchor="nw", bd=1, relief="solid")
        preg_panel.pack(side="left", fill="both", expand=True, padx=(6, 0))

        self.lbl_pregunta = tk.Label(preg_panel, text="",
                                     bg=COLOR_PANEL, fg=COLOR_TEXT,
                                     font=self.font_normal,
                                     wraplength=480, justify="left",
                                     anchor="nw")
        self.lbl_pregunta.pack(side="top", anchor="w", padx=14, pady=(14, 10))

        # Área dinámica donde aparecen los botones/inputs según q_type
        self.area_respuesta = tk.Frame(preg_panel, bg=COLOR_PANEL)
        self.area_respuesta.pack(side="top", fill="x", padx=14)

        # Feedback en un Text scrollable: tolera explicaciones LARGAS
        # (la simple_explanation y la concatenación de explicaciones puede
        # superar los 1500 chars). Altura fija; el contenido se scrollea.
        feedback_wrap = tk.Frame(preg_panel, bg=COLOR_PANEL)
        feedback_wrap.pack(side="top", fill="both", expand=False,
                            padx=14, pady=(8, 6))
        self.txt_feedback = tk.Text(
            feedback_wrap, height=10, wrap="word",
            bg=COLOR_PANEL, fg=COLOR_TEXT, font=self.font_normal,
            bd=0, padx=2, pady=4, state="disabled",
            relief="flat")
        self.txt_feedback.pack(side="left", fill="both", expand=True)
        fbsb = ttk.Scrollbar(feedback_wrap, command=self.txt_feedback.yview)
        fbsb.pack(side="right", fill="y")
        self.txt_feedback.configure(yscrollcommand=fbsb.set)

        # Configuramos tags para colorear (ok/bad/normal)
        self.txt_feedback.tag_configure("ok",  foreground=COLOR_OK,
                                         font=self.font_normal)
        self.txt_feedback.tag_configure("bad", foreground=COLOR_BAD,
                                         font=self.font_normal)
        self.txt_feedback.tag_configure("warn",
                                         foreground="#d29922",
                                         font=self.font_normal)

        # Para compatibilidad con el código existente exponemos un
        # shim "lbl_feedback" con .config(text=..., fg=...)
        class _FeedbackShim:
            def __init__(self, txt):  self._t = txt
            def config(self, text="", fg=None):
                self._t.config(state="normal")
                self._t.delete("1.0", "end")
                if text:
                    tag = ("ok" if fg == COLOR_OK
                           else "bad" if fg == COLOR_BAD
                           else "warn" if fg == "#d29922"
                           else None)
                    if tag:
                        self._t.insert("1.0", text, tag)
                    else:
                        self._t.insert("1.0", text)
                self._t.config(state="disabled")
            def cget(self, key):
                if key == "text":
                    return self._t.get("1.0", "end-1c")
                return ""
        self.lbl_feedback = _FeedbackShim(self.txt_feedback)

        # Botones de apoyo pedagógico (self-explanation + ejemplos parecidos)
        botonera_aux = tk.Frame(preg_panel, bg=COLOR_PANEL)
        botonera_aux.pack(anchor="w", padx=14, pady=(4, 10))

        tk.Button(botonera_aux, text="💭  Auto-explícate (4 preguntas)",
                  font=self.font_btn,
                  bg=COLOR_THEORY, fg=COLOR_TEXT,
                  relief="flat", padx=14, pady=6, cursor="hand2",
                  command=self._mostrar_autoexplicacion).pack(
            side="left", padx=(0, 6))

        self.btn_similares = tk.Button(
            botonera_aux, text="📚  Ejemplos parecidos",
            font=self.font_btn,
            bg="#15202b", fg=COLOR_TEXT,
            relief="flat", padx=14, pady=6, cursor="hand2",
            command=self._mostrar_ejemplos_parecidos)
        self.btn_similares.pack(side="left", padx=(0, 6))

        # 💼 Ejemplos progresivos: 3 ejemplos básico → intermedio → experto
        # tomados del banco externo extra_ejemplos.py. Si la lección no
        # tiene entradas en ese banco, el botón aparece deshabilitado.
        self.btn_progresivos = tk.Button(
            botonera_aux, text="💼  Ejemplos progresivos",
            font=self.font_btn,
            bg="#102530", fg=COLOR_TEXT,
            relief="flat", padx=14, pady=6, cursor="hand2",
            command=self._mostrar_ejemplos_progresivos)
        self.btn_progresivos.pack(side="left")

        # --- Pie: navegación --------------------------------------------
        pie = tk.Frame(self, bg=COLOR_BG)
        pie.pack(side="bottom", fill="x", padx=14, pady=12)

        self.btn_prev = tk.Button(pie, text="←  Anterior",
                                  font=self.font_btn,
                                  bg=COLOR_BTNINAC, fg=COLOR_TEXT,
                                  relief="flat", padx=14, pady=6,
                                  cursor="hand2",
                                  command=self._leccion_anterior)
        self.btn_prev.pack(side="left")

        self.btn_next = tk.Button(pie, text="Siguiente  →",
                                  font=self.font_btn,
                                  bg=COLOR_ACCENT, fg="white",
                                  relief="flat", padx=14, pady=6,
                                  cursor="hand2",
                                  command=self._leccion_siguiente)
        self.btn_next.pack(side="right")

        self.lbl_progreso = tk.Label(pie, text="",
                                     font=self.font_normal,
                                     bg=COLOR_BG, fg=COLOR_TEXT)
        self.lbl_progreso.pack(side="left", expand=True)

        tk.Button(pie, text="↺  Reiniciar progreso",
                  font=self.font_btn,
                  bg=COLOR_BTNINAC, fg=COLOR_TEXT,
                  relief="flat", padx=10, pady=4, cursor="hand2",
                  command=self._reiniciar_progreso).pack(side="right",
                                                         padx=(0, 8))

    # -----------------------------------------------------------------
    def _cambiar_seccion(self, nombre):
        # Al cambiar de sección, salimos de los modos especiales
        self.modo_mezclado = False
        self.modo_adaptativo = False
        self.modo_progresivo = False
        self.modo_refuerzo = False
        self.modo_nivel = False
        self.seccion_actual = nombre
        self.idx_leccion = 0
        # Sincronizar el capítulo activo con la sección seleccionada
        nuevo_cap = self._capitulo_de_seccion(nombre)
        if nuevo_cap and nuevo_cap != self.capitulo_actual:
            self.capitulo_actual = nuevo_cap
            self._render_subsecciones()
        self._cargar_leccion()

    # ---------- Helpers de navegación por capítulos -----------------
    @staticmethod
    def _agrupar_por_capitulo():
        """Agrupa las claves de LECCIONES por prefijo:
            1.x → Capítulo 1   ·   2.x → Capítulo 2   etc.
            🤖   → Aplicaciones IA
            📚   → Metodología
        Devuelve un dict ordenado:
            {codigo: {"label": str, "secciones": [nombres,…]}}
        """
        grupos = {}
        for nombre in LECCIONES.keys():
            n = nombre.strip()
            if n.startswith("1."):  cod, lab = "1", "📗  Cap. 1 · Lógica"
            elif n.startswith("2."): cod, lab = "2", "📘  Cap. 2 · Álgebra"
            elif n.startswith("3."): cod, lab = "3", "📙  Cap. 3 · Análisis"
            elif n.startswith("4."): cod, lab = "4", "📕  Cap. 4 · Probabilidad"
            elif n.startswith("🤖"): cod, lab = "ia", "🤖  Aplicaciones a IA"
            elif n.startswith("📚"): cod, lab = "met", "📚  Metodología"
            else:                    cod, lab = "otros", "Otros"
            grupos.setdefault(cod, {"label": lab, "secciones": []})
            grupos[cod]["secciones"].append(nombre)
        return grupos

    def _capitulo_de_seccion(self, nombre):
        """Devuelve el código de capítulo al que pertenece la sección."""
        for cod, info in self.capitulos.items():
            if nombre in info["secciones"]:
                return cod
        return None

    def _render_subsecciones(self):
        """Repinta la barra de sub-secciones del capítulo activo y
        resalta los botones de capítulo. Si las sub-secciones no caben
        en la ventana, ofrecemos scroll horizontal con la rueda."""
        # Resaltar capítulos
        for cod, b in self.btns_capitulo.items():
            if cod == self.capitulo_actual:
                b.config(bg=COLOR_ACCENT, fg="white")
            else:
                b.config(bg=COLOR_BTNINAC, fg=COLOR_TEXT)

        # Limpiar y volver a dibujar los botones de sub-sección dentro
        # de un Canvas con scroll horizontal (para Cap. con muchas subs).
        for w in self.barra_subsecciones.winfo_children():
            w.destroy()
        self.btns_seccion = {}

        canvas_sub = tk.Canvas(self.barra_subsecciones, bg=COLOR_BG,
                                highlightthickness=0, height=42)
        canvas_sub.pack(side="left", fill="x", expand=True)
        interior = tk.Frame(canvas_sub, bg=COLOR_BG)
        ventana = canvas_sub.create_window(0, 0, anchor="nw",
                                            window=interior)

        for nombre in self.capitulos[self.capitulo_actual]["secciones"]:
            etiqueta = nombre.strip()
            if len(etiqueta) > 36:
                etiqueta = etiqueta[:34] + "…"
            b = tk.Button(interior, text=etiqueta,
                          font=self.font_btn,
                          bg=COLOR_BTNINAC, fg=COLOR_TEXT,
                          activebackground=COLOR_ACCENT,
                          relief="flat", padx=10, pady=6,
                          cursor="hand2",
                          command=lambda n=nombre: self._cambiar_seccion(n))
            b.pack(side="left", padx=3)
            self.btns_seccion[nombre] = b

        # Recalcular scrollregion tras dibujar
        def _update_scroll(_evt=None):
            canvas_sub.update_idletasks()
            canvas_sub.configure(scrollregion=canvas_sub.bbox("all"))
        interior.bind("<Configure>", _update_scroll)

        # Scroll horizontal con la rueda del ratón (Windows: <MouseWheel>)
        def _on_wheel(evt):
            canvas_sub.xview_scroll(-1 * int(evt.delta / 60), "units")
        canvas_sub.bind("<MouseWheel>", _on_wheel)
        interior.bind("<MouseWheel>", _on_wheel)

    def _cambiar_capitulo(self, codigo):
        """Cambia el capítulo activo. Salta a la 1ª sección del capítulo."""
        self.capitulo_actual = codigo
        self._render_subsecciones()
        primera = self.capitulos[codigo]["secciones"][0]
        self._cambiar_seccion(primera)

    def _leccion_anterior(self):
        if self.modo_nivel:
            if self.pos_nivel > 0:
                self.pos_nivel -= 1
                self.seccion_actual, self.idx_leccion = \
                    self.cola_nivel[self.pos_nivel]
                self._cargar_leccion()
            return
        if self.modo_refuerzo:
            if self.pos_refuerzo > 0:
                self.pos_refuerzo -= 1
                self.seccion_actual, self.idx_leccion, _ = \
                    self.cola_refuerzo[self.pos_refuerzo]
                self._cargar_leccion()
            return
        if self.modo_progresivo:
            if self.pos_progresiva > 0:
                self.pos_progresiva -= 1
                self.seccion_actual, self.idx_leccion = \
                    self.cola_progresiva[self.pos_progresiva]
                self._cargar_leccion()
            return
        if self.modo_adaptativo:
            if self.pos_adaptativa > 0:
                self.pos_adaptativa -= 1
                self.seccion_actual, self.idx_leccion = \
                    self.cola_adaptativa[self.pos_adaptativa]
                self.variante_semilla = int(time.time())
                self._cargar_leccion()
            return
        if self.modo_mezclado:
            if self.pos_mezclada > 0:
                self.pos_mezclada -= 1
                self.seccion_actual, self.idx_leccion = \
                    self.cola_mezclada[self.pos_mezclada]
                self._cargar_leccion()
            return
        if self.idx_leccion > 0:
            self.idx_leccion -= 1
            self._cargar_leccion()

    def _leccion_siguiente(self):
        if self.modo_nivel:
            self.pos_nivel += 1
            if self.pos_nivel >= len(self.cola_nivel):
                self.lbl_feedback.config(
                    text=f"🎰  Nivel «{self.nivel_filtro}» completado "
                         f"({len(self.cola_nivel)} preguntas).\n"
                         f"   Vuelve a pulsar 🎰 Por nivel para otra ronda.",
                    fg=COLOR_OK)
                self.modo_nivel = False
                self.btn_nivel.config(text="🎰  Por nivel")
                return
            self.seccion_actual, self.idx_leccion = \
                self.cola_nivel[self.pos_nivel]
            self._cargar_leccion()
            return

        if self.modo_refuerzo:
            self.pos_refuerzo += 1
            if self.pos_refuerzo >= len(self.cola_refuerzo):
                self.lbl_feedback.config(
                    text=f"🎯  Refuerzo completado — {self.refuerzo_titulo}.\n"
                         f"   Vuelve a Estadísticas para ver cómo subió\n"
                         f"   tu dominio EMA en esta lección.",
                    fg=COLOR_OK)
                self.modo_refuerzo = False
                self.btn_refuerzo.config(text="🎯  Refuerzo")
                return
            self.seccion_actual, self.idx_leccion, _ = \
                self.cola_refuerzo[self.pos_refuerzo]
            self._cargar_leccion()
            return

        if self.modo_progresivo:
            self.pos_progresiva += 1
            if self.pos_progresiva >= len(self.cola_progresiva):
                self.lbl_feedback.config(
                    text="🎉  Progresiva completada — has pasado de\n"
                         "    básico → intermedio → experto.",
                    fg=COLOR_OK)
                self.modo_progresivo = False
                return
            self.seccion_actual, self.idx_leccion = \
                self.cola_progresiva[self.pos_progresiva]
            self._cargar_leccion()
            return

        if self.modo_adaptativo:
            self.pos_adaptativa += 1
            if self.pos_adaptativa >= len(self.cola_adaptativa):
                ok = sum(1 for s, i in self.cola_adaptativa
                         if self.progreso.get(s, [])[i] == "ok"
                         if i < len(self.progreso.get(s, [])))
                self.lbl_feedback.config(
                    text=f"🎉  Adaptativa completada.\n"
                         f"   La BD se ha actualizado: vuelve a pulsar\n"
                         f"   '🧠 Adaptativa' para una nueva ronda\n"
                         f"   centrada en tus debilidades actuales.",
                    fg=COLOR_OK)
                self.modo_adaptativo = False
                self.btn_adaptativa.config(text="🧠  Adaptativa")
                return
            self.seccion_actual, self.idx_leccion = \
                self.cola_adaptativa[self.pos_adaptativa]
            self.variante_semilla = int(time.time() * 1000) + self.pos_adaptativa
            self._cargar_leccion()
            return

        if self.modo_mezclado:
            self.pos_mezclada += 1
            if self.pos_mezclada >= len(self.cola_mezclada):
                # Fin de la práctica mezclada
                ok = sum(1 for s, i in self.cola_mezclada
                         if self.progreso[s][i] == "ok")
                self.lbl_feedback.config(
                    text=f"🎉  Práctica mezclada completada.\n"
                         f"   Aciertos: {ok} / {len(self.cola_mezclada)}",
                    fg=COLOR_OK)
                self.modo_mezclado = False
                return
            self.seccion_actual, self.idx_leccion = \
                self.cola_mezclada[self.pos_mezclada]
            self._cargar_leccion()
            return

        lecciones = LECCIONES[self.seccion_actual]
        if self.idx_leccion < len(lecciones) - 1:
            self.idx_leccion += 1
            self._cargar_leccion()
        else:
            # Saltar a la siguiente sección
            secciones = list(LECCIONES.keys())
            i = secciones.index(self.seccion_actual)
            if i < len(secciones) - 1:
                self.seccion_actual = secciones[i + 1]
                self.idx_leccion = 0
                self._cargar_leccion()
            else:
                self.lbl_feedback.config(
                    text="🎉  ¡Has terminado todas las secciones!",
                    fg=COLOR_OK)

    # -----------------------------------------------------------------
    def _typewriter_titulo(self, texto):
        """Revela el título con efecto máquina de escribir (estética consola).
        Protegido por token para que cambios rápidos de lección no se mezclen."""
        self._tw_token = getattr(self, "_tw_token", 0) + 1
        tok = self._tw_token
        n = len(texto)
        paso = max(6, min(20, int(420 / max(1, n))))   # total ≈ 0.4 s

        def escribir(i=0):
            if tok != getattr(self, "_tw_token", 0):
                return
            if i >= n:
                self.lbl_titulo.config(text=texto)
                return
            self.lbl_titulo.config(text=texto[:i + 1] + "▋")
            self.after(paso, lambda: escribir(i + 1))

        escribir()

    def _cargar_leccion(self):
        # Sincronizar capítulo activo con la sección actual (los modos
        # especiales pueden saltar a una sección de otro capítulo).
        nuevo_cap = self._capitulo_de_seccion(self.seccion_actual)
        if nuevo_cap and nuevo_cap != self.capitulo_actual:
            self.capitulo_actual = nuevo_cap
            self._render_subsecciones()

        # Resaltar botón de sección activa
        for nombre, b in self.btns_seccion.items():
            if nombre == self.seccion_actual and not self.modo_mezclado:
                b.config(bg=COLOR_ACCENT, fg="white")
            else:
                b.config(bg=COLOR_BTNINAC, fg=COLOR_TEXT)

        # Botones de modos especiales destacados según activos
        self.btn_mezclado.config(
            text="🎲  Mezclada ACTIVA — salir" if self.modo_mezclado
            else "🎲  Mezclada")
        self.btn_adaptativa.config(
            text="🧠  Adaptativa ACTIVA — salir" if self.modo_adaptativo
            else "🧠  Adaptativa")
        self.btn_progresiva.config(
            text="🎯  Progresiva ACTIVA — salir" if self.modo_progresivo
            else "🎯  Progresiva")
        self.btn_refuerzo.config(
            text="🎯  Refuerzo ACTIVO — salir" if self.modo_refuerzo
            else "🎯  Refuerzo")
        self.btn_nivel.config(
            text="🎰  Nivel ACTIVO — salir" if self.modo_nivel
            else "🎰  Por nivel")

        lecciones = LECCIONES[self.seccion_actual]
        leccion = lecciones[self.idx_leccion]

        # --- En modo REFUERZO usamos la VARIANTE pregenerada con valores
        # distintos del circuito (no la lección original). -----------------
        if self.modo_refuerzo and self.pos_refuerzo < len(self.cola_refuerzo):
            _, _, leccion_var = self.cola_refuerzo[self.pos_refuerzo]
            leccion = leccion_var
        # --- En modo adaptativo aplicamos VARIANTE (Sweller variability) -
        elif self.modo_adaptativo:
            leccion = aplicar_variante(leccion, self.variante_semilla)
        else:
            # Barajado GLOBAL de opciones para todas las preguntas mc.
            # Evita que el usuario memorice "siempre la opción B" cuando
            # los autores tendieron a poner la respuesta en una posición
            # concreta (efecto variabilidad — Sweller 2019).
            # Usamos una semilla determinista por (sección, idx) para que
            # la misma pregunta se vea siempre igual EN LA MISMA SESIÓN.
            semilla = hash((self.seccion_actual, self.idx_leccion)) & 0xFFFFFF
            leccion = aplicar_variante(leccion, semilla)
        self._leccion_actual_render = leccion

        # --- Cabecera con título + indicador de nivel ★ ---
        nivel = leccion.get("nivel", "")
        estrellas = {"básico": "★",
                     "intermedio": "★★",
                     "experto": "★★★"}.get(nivel, "")
        nivel_tag = f"  [{estrellas} {nivel}]" if estrellas else ""

        if self.modo_nivel:
            estrellas = {"básico": "★", "intermedio": "★★",
                         "experto": "★★★"}.get(self.nivel_filtro, "")
            prefix = (f"🎰 Nivel {estrellas} {self.nivel_filtro} "
                      f"{self.pos_nivel + 1}/{len(self.cola_nivel)} "
                      f"({self.seccion_actual.split()[0]}) — ")
        elif self.modo_refuerzo:
            prefix = (f"🎯 Refuerzo {self.pos_refuerzo + 1}/"
                      f"{len(self.cola_refuerzo)} · "
                      f"{self.refuerzo_titulo} — ")
        elif self.modo_progresivo:
            prefix = (f"🎯 Progresiva {self.pos_progresiva + 1}/"
                      f"{len(self.cola_progresiva)} "
                      f"({self.seccion_actual.split()[0]}) — ")
        elif self.modo_adaptativo:
            datos = self.dominio.get((self.seccion_actual, self.idx_leccion),
                                     {"ema": 0.5, "intentos": 0})
            prefix = (f"🧠 Adaptativa {self.pos_adaptativa + 1}/"
                      f"{len(self.cola_adaptativa)} "
                      f"({self.seccion_actual.split()[0]} · "
                      f"dominio={datos['ema']:.0%}) — ")
        elif self.modo_mezclado:
            prefix = (f"🎲 Mezclada {self.pos_mezclada + 1}/"
                      f"{len(self.cola_mezclada)} "
                      f"({self.seccion_actual.split()[0]}) — ")
        else:
            prefix = (f"Lección {self.idx_leccion + 1} de "
                      f"{len(lecciones)} — ")
        self._typewriter_titulo(prefix + leccion['title'] + nivel_tag)

        # --- Strip de dots de progreso de la sección actual ---
        self.lbl_dots.config(text=self._calcular_dots(self.seccion_actual))

        # --- Panel TEORÍA ---
        self.txt_teoria.config(state="normal")
        self.txt_teoria.delete("1.0", "end")
        self.txt_teoria.insert("1.0", leccion["theory"])
        self.txt_teoria.config(state="disabled")

        # --- Panel EJEMPLO RESUELTO (worked example, Sweller 2019) ---
        self.txt_ejemplo.config(state="normal")
        self.txt_ejemplo.delete("1.0", "end")
        ejemplo = leccion.get("example") or "(Esta lección no tiene ejemplo aparte.)"
        self.txt_ejemplo.insert("1.0", ejemplo)
        self.txt_ejemplo.config(state="disabled")

        # --- Diagrama de circuito (si la lección lo trae) ---
        diagrama = leccion.get("diagram")
        # Limpiamos los Entry de animación previos (cambiamos de circuito)
        for w in self.zona_inputs_anim.winfo_children():
            w.destroy()
        self._anim_inputs = {}
        self._diagrama_modelo = None
        self._anim_running = False

        # Visualización GENERAL (grafo/Venn/función/distribución/vectores).
        # Es un campo alternativo a "diagram". Se procesa si está presente.
        visual = leccion.get("visual")

        if diagrama:
            self.canvas_diagrama.pack(side="top", fill="both",
                                       expand=True, pady=(4, 4),
                                       padx=4)
            try:
                self._diagrama_modelo = dibujar_circuito(
                    self.canvas_diagrama, diagrama)
            except Exception as e:
                self.canvas_diagrama.delete("all")
                self.canvas_diagrama.create_text(
                    200, 90, text=f"(no se pudo dibujar: {e})",
                    fill="red")
                self._diagrama_modelo = None

            # Mostrar barra de animación + Entry para cada variable
            self.frame_anim.pack(side="top", fill="x", pady=(2, 4))
            trace = diagrama.get("trace_values", {}) or {}
            for var in diagrama.get("vars", []):
                tk.Label(self.zona_inputs_anim, text=f"{var}=",
                         bg=COLOR_EXAMPLE, fg=COLOR_TEXT,
                         font=("Consolas", 10, "bold")).pack(
                    side="left", padx=(4, 1))
                e = tk.Entry(self.zona_inputs_anim, width=2,
                             font=("Consolas", 11), justify="center",
                             bg="#0d1117", fg=COLOR_TEXT,
                             insertbackground=COLOR_TEXT, relief="flat",
                             highlightthickness=1,
                             highlightbackground=COLOR_ACCENT)
                e.insert(0, str(trace.get(var, 0)))
                e.pack(side="left", padx=(0, 6))
                self._anim_inputs[var] = e
        elif visual:
            # Visualización general (no circuito → sin animación de señales)
            self.canvas_diagrama.pack(side="top", fill="both",
                                       expand=True, pady=(4, 4),
                                       padx=4)
            self.frame_anim.pack_forget()
            tipo = visual.get("tipo")
            fn = _DISPATCH_VISUAL.get(tipo)
            if fn is None:
                self.canvas_diagrama.delete("all")
                self.canvas_diagrama.create_text(
                    200, 90, text=f"(tipo desconocido: {tipo})", fill="red")
            else:
                self.canvas_diagrama.update_idletasks()
                try:
                    fn(self.canvas_diagrama, visual)
                except Exception as e:
                    self.canvas_diagrama.delete("all")
                    self.canvas_diagrama.create_text(
                        200, 90, text=f"(no se pudo dibujar: {e})",
                        fill="red")

            # ¿Tiene animación? Mostramos la barra con ▶ Animar
            self._anim_vis_running = False
            anim = visual.get("animate")
            if anim and anim.get("tipo") in _DISPATCH_ANIM_VISUAL:
                self._visual_actual = visual
                etiquetas = {"descenso": "Verás la bolita bajar por la curva",
                             "vectores": "Verás los vectores dibujarse uno a uno",
                             "markov": "Verás el estado saltar paso a paso",
                             "recorrido": "Verás recorrer el camino vértice a vértice"}
                self.lbl_anim_vis.config(
                    text=etiquetas.get(anim["tipo"], ""))
                self.btn_animar_vis.config(state="normal", text="▶  Animar")
                self.frame_anim_vis.pack(side="top", fill="x", pady=(2, 4))
            else:
                self._visual_actual = None
                self.frame_anim_vis.pack_forget()
        else:
            self.canvas_diagrama.pack_forget()
            self.frame_anim.pack_forget()
            self.frame_anim_vis.pack_forget()
            self._visual_actual = None

        # --- Botón "Ver en 3D" si la lección trae datos 3D (visual3d) ---
        self._visual3d_actual = leccion.get("visual3d")
        if self._visual3d_actual and _HAS_MPL and visual:
            if not self.frame_anim_vis.winfo_ismapped():
                self.frame_anim_vis.pack(side="top", fill="x", pady=(2, 4))
            self.btn_3d.config(state="normal")
            self.btn_3d.pack(side="right", padx=(4, 10), pady=4)
        else:
            self.btn_3d.pack_forget()

        # --- Pregunta (con glosario llano de la jerga) ---
        self._glosados = set()
        self.lbl_pregunta.config(text=self._glosar(leccion["question"]))

        # Limpiar área de respuesta y feedback
        for w in self.area_respuesta.winfo_children():
            w.destroy()
        self.lbl_feedback.config(text="")
        self.respuesta_dada = False

        # Renderizar widget según tipo
        qt = leccion["q_type"]
        if qt == "mc":
            self._render_mc(leccion)
        elif qt == "tf":
            self._render_tf(leccion)
        elif qt == "tt":
            self._render_tt(leccion)
        elif qt == "info":
            self._render_info(leccion)

        # --- Progreso global ---
        total_global = sum(len(v) for v in LECCIONES.values())
        hechas_global = sum(
            1 for sec, lst in self.progreso.items() for v in lst if v is not None
        )
        aciertos_global = sum(
            1 for sec, lst in self.progreso.items() for v in lst if v == "ok"
        )
        self.lbl_progreso.config(
            text=f"Progreso global: {hechas_global}/{total_global} hechas  "
                 f"|  Aciertos: {aciertos_global}")

        # Recolocar el scroll arriba y recalcular el área desplazable
        # (la lección nueva puede ser más alta o más baja que la anterior).
        if hasattr(self, "_vcanvas"):
            self._vcanvas.update_idletasks()
            self._vcanvas.configure(scrollregion=self._vcanvas.bbox("all"))
            self._vcanvas.yview_moveto(0)

    # ---------- Renderizadores por tipo de pregunta ------------------
    def _render_mc(self, leccion):
        self.var_mc = tk.IntVar(value=-1)
        for i, op in enumerate(leccion["options"]):
            rb = tk.Radiobutton(self.area_respuesta,
                                text=f"  {chr(65 + i)})  {self._glosar(op)}",
                                variable=self.var_mc, value=i,
                                bg=COLOR_PANEL, fg=COLOR_TEXT,
                                font=self.font_normal,
                                anchor="w", wraplength=460,
                                justify="left",
                                activebackground=COLOR_PANEL,
                                selectcolor=COLOR_THEORY,
                                cursor="hand2")
            rb.pack(fill="x", anchor="w", pady=3)
        tk.Button(self.area_respuesta, text="Comprobar",
                  font=self.font_btn,
                  bg=COLOR_ACCENT, fg="white",
                  relief="flat", padx=18, pady=6, cursor="hand2",
                  command=lambda: self._comprobar_mc(leccion)).pack(
            anchor="w", pady=10)

    def _render_tf(self, leccion):
        self.var_mc = tk.IntVar(value=-1)
        for i, op in enumerate(leccion["options"]):
            rb = tk.Radiobutton(self.area_respuesta,
                                text=f"  {self._glosar(op)}",
                                variable=self.var_mc, value=i,
                                bg=COLOR_PANEL, fg=COLOR_TEXT,
                                font=self.font_normal,
                                anchor="w",
                                activebackground=COLOR_PANEL,
                                selectcolor=COLOR_THEORY,
                                cursor="hand2")
            rb.pack(fill="x", anchor="w", pady=3)
        tk.Button(self.area_respuesta, text="Comprobar",
                  font=self.font_btn,
                  bg=COLOR_ACCENT, fg="white",
                  relief="flat", padx=18, pady=6, cursor="hand2",
                  command=lambda: self._comprobar_mc(leccion)).pack(
            anchor="w", pady=10)

    def _render_tt(self, leccion):
        # Tabla de verdad: 4 entries
        tk.Label(self.area_respuesta,
                 text="Recuerda: escribe 0 (Falso) o 1 (Verdadero)",
                 bg=COLOR_PANEL, fg=COLOR_TEXT,
                 font=self.font_normal).pack(anchor="w", pady=(0, 6))

        tabla = tk.Frame(self.area_respuesta, bg=COLOR_PANEL)
        tabla.pack(anchor="w", pady=6)

        # Cabecera
        for j, txt in enumerate(["p", "q", "resultado"]):
            tk.Label(tabla, text=txt, font=self.font_subt,
                     bg=COLOR_PANEL, fg=COLOR_TEXT, width=10,
                     borderwidth=1, relief="solid").grid(row=0, column=j,
                                                         padx=1, pady=1)

        # Filas: (0,0), (0,1), (1,0), (1,1)
        self.entries_tt = []
        filas = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for i, (p, q) in enumerate(filas, start=1):
            tk.Label(tabla, text=str(p), font=self.font_mono,
                     bg=COLOR_PANEL, fg=COLOR_TEXT, width=10,
                     borderwidth=1, relief="solid").grid(row=i, column=0,
                                                         padx=1, pady=1)
            tk.Label(tabla, text=str(q), font=self.font_mono,
                     bg=COLOR_PANEL, fg=COLOR_TEXT, width=10,
                     borderwidth=1, relief="solid").grid(row=i, column=1,
                                                         padx=1, pady=1)
            e = tk.Entry(tabla, font=self.font_mono,
                         width=8, justify="center",
                         bg="#0d1117", fg=COLOR_TEXT,
                         insertbackground=COLOR_TEXT, relief="flat",
                         highlightthickness=1,
                         highlightbackground=COLOR_ACCENT)
            e.grid(row=i, column=2, padx=1, pady=1)
            self.entries_tt.append(e)

        tk.Button(self.area_respuesta, text="Comprobar",
                  font=self.font_btn,
                  bg=COLOR_ACCENT, fg="white",
                  relief="flat", padx=18, pady=6, cursor="hand2",
                  command=lambda: self._comprobar_tt(leccion)).pack(
            anchor="w", pady=10)

    def _render_info(self, leccion):
        tk.Label(self.area_respuesta,
                 text="(Esta lección es solo informativa.\n"
                      "Lee la teoría y pulsa 'Siguiente →' cuando estés listo.)",
                 bg=COLOR_PANEL, fg=COLOR_TEXT,
                 font=self.font_normal, justify="left").pack(anchor="w",
                                                              pady=8)

    # ---------- Verificación de respuesta (con persistencia SQL) -----
    def _comprobar_mc(self, leccion):
        elegido = self.var_mc.get()
        if elegido == -1:
            self.lbl_feedback.config(
                text="⚠  Selecciona una opción primero.", fg=COLOR_BAD)
            return
        acierta = (elegido == leccion["correct"])
        if acierta:
            self._marcar_progreso("ok")
            self.lbl_feedback.config(
                text="✓  ¡CORRECTO!\n\n" + self._glosar(leccion["explanation"]),
                fg=COLOR_OK)
        else:
            self._marcar_progreso("fail")
            correcta = self._glosar(leccion["options"][leccion["correct"]])
            self.lbl_feedback.config(
                text=f"✗  Incorrecto. La respuesta correcta era:\n"
                     f"   → {correcta}\n\n{self._glosar(leccion['explanation'])}"
                     + self._extra_pedagogico(leccion),
                fg=COLOR_BAD)
        self._guardar_db_y_refrescar(leccion, acierta)

    def _comprobar_tt(self, leccion):
        try:
            valores = [int(e.get().strip()) for e in self.entries_tt]
        except ValueError:
            self.lbl_feedback.config(
                text="⚠  Rellena las 4 celdas con 0 o 1.", fg=COLOR_BAD)
            return
        if any(v not in (0, 1) for v in valores):
            self.lbl_feedback.config(
                text="⚠  Solo se admiten 0 o 1.", fg=COLOR_BAD)
            return
        acierta = (valores == leccion["correct"])
        if acierta:
            self._marcar_progreso("ok")
            self.lbl_feedback.config(
                text="✓  ¡CORRECTO!\n\n" + self._glosar(leccion["explanation"]),
                fg=COLOR_OK)
        else:
            self._marcar_progreso("fail")
            esp = leccion["correct"]
            self.lbl_feedback.config(
                text=f"✗  No coincide.\n"
                     f"   Tu respuesta : {valores}\n"
                     f"   Correcta     : {esp}\n\n{self._glosar(leccion['explanation'])}"
                     + self._extra_pedagogico(leccion),
                fg=COLOR_BAD)
        self._guardar_db_y_refrescar(leccion, acierta)

    def _extra_pedagogico(self, leccion):
        """Devuelve texto extra (explicación SENCILLA) si esta lección ya
        había sido fallada antes. Aplica retrieval-spaced + worked examples
        cuando el patrón de error se REPITE."""
        # Si la lección no es la original (modo refuerzo/adaptativa pueden
        # mostrar una variante), buscamos en la lección base por idx.
        try:
            base = LECCIONES[self.seccion_actual][self.idx_leccion]
        except (KeyError, IndexError):
            base = leccion
        simple = base.get("simple_explanation")
        if not simple:
            return ""
        # Contar fallos PREVIOS (antes del actual que acabamos de añadir).
        try:
            n = db_fallos_de_leccion(self.seccion_actual, self.idx_leccion)
        except Exception:
            n = 0
        if n < 1:
            return ""
        return ("\n\n" + "─" * 50
                + f"\n💡  EXPLICACIÓN MÁS SENCILLA "
                + f"(esta lección la has fallado {n+1} veces)\n"
                + "─" * 50
                + "\n" + simple)

    def _guardar_db_y_refrescar(self, leccion, acierta):
        """Persiste la respuesta en SQLite y refresca el dominio en memoria."""
        # Usamos siempre la (seccion, idx) original — no la variante —
        # para que el dominio acumule sobre la lección conceptual.
        # El título guardado es el de la lección original.
        original = LECCIONES[self.seccion_actual][self.idx_leccion]
        try:
            db_registrar(self.seccion_actual, self.idx_leccion,
                         original["title"], acierta,
                         es_variante=self.modo_adaptativo)
            self.dominio = db_cargar_dominio()
        except Exception as e:
            print(f"[Aviso] no se pudo guardar en BD: {e}")
        self.lbl_dots.config(text=self._calcular_dots(self.seccion_actual))

    # ---------- Helpers nuevos (metodología aplicada) ----------------
    def _marcar_progreso(self, estado):
        """Registra el resultado (ok/fail) de la lección actual."""
        # Solo subimos a 'ok' si no estaba ya en 'ok'. Si falla, marcamos fail.
        prev = self.progreso[self.seccion_actual][self.idx_leccion]
        if estado == "ok" and prev == "fail":
            # Si ya había fallado, lo dejamos como ok pero menos brillante
            self.progreso[self.seccion_actual][self.idx_leccion] = "ok"
        else:
            self.progreso[self.seccion_actual][self.idx_leccion] = estado

    def _calcular_dots(self, seccion):
        """Genera la cadena visual de progreso para una sección."""
        simbolos = {None: "○", "ok": "●", "fail": "✗"}
        estado = self.progreso.get(seccion, [])
        # Marcamos la actual con un cursor
        out = []
        for i, e in enumerate(estado):
            ch = simbolos[e]
            if i == self.idx_leccion and not self.modo_mezclado:
                out.append(f"[{ch}]")
            else:
                out.append(f" {ch} ")
        return "".join(out)

    def _reiniciar_progreso(self):
        """Borra todo el progreso registrado."""
        self.progreso = {sec: [None] * len(lecs)
                         for sec, lecs in LECCIONES.items()}
        self.lbl_feedback.config(text="↺  Progreso reiniciado.",
                                 fg=COLOR_TEXT2)
        self.lbl_dots.config(text=self._calcular_dots(self.seccion_actual))
        self._cargar_leccion()

    # ---------- Animación del circuito (propagación de señales) -------
    def _leer_inputs_anim(self):
        """Lee los Entry y devuelve {var: 0|1}, o None si hay error."""
        valores = {}
        for var, entry in self._anim_inputs.items():
            txt = entry.get().strip()
            if txt not in ("0", "1"):
                return None
            valores[var] = int(txt)
        return valores

    def _animar_circuito(self):
        """Arranca la animación paso a paso del circuito actual."""
        if self._anim_running or self._diagrama_modelo is None:
            return
        valores = self._leer_inputs_anim()
        if valores is None:
            self.btn_animar.config(text="⚠ usa solo 0 ó 1")
            self.after(1500, lambda: self.btn_animar.config(
                text="▶  Animar señales"))
            return
        # Resetear colores antes de empezar
        resetear_colores(self._diagrama_modelo)
        self._anim_running = True
        self.btn_animar.config(state="disabled", text="⏵ animando…")

        def on_done(resultados):
            self._anim_running = False
            self.btn_animar.config(state="normal",
                                   text="▶  Animar señales")

        simular_circuito_paso(
            self._diagrama_modelo, valores,
            paso=0, on_done=on_done)

    def _reset_animacion(self):
        """Vuelve a colores iniciales (no afecta a la pregunta)."""
        if self._diagrama_modelo is not None:
            resetear_colores(self._diagrama_modelo)

    # ---------- Animación de VISUALES (descenso, vectores, markov) ----
    def _glosar(self, texto):
        """Añade aclaraciones llanas a la jerga (ver GLOSARIO). Usa el
        conjunto self._glosados para no repetir un término en la misma lección."""
        if not hasattr(self, "_glosados"):
            self._glosados = set()
        return _aplicar_glosario(texto, self._glosados)

    def _abrir_3d(self):
        """Abre la ventana de vista 3D (Matplotlib) para la lección actual."""
        if getattr(self, "_visual3d_actual", None):
            abrir_visor_3d(self, self._visual3d_actual)

    def _animar_visual(self):
        """Lanza la animación del visual actual (si la soporta)."""
        if self._anim_vis_running or self._visual_actual is None:
            return
        anim = self._visual_actual.get("animate", {})
        fn = _DISPATCH_ANIM_VISUAL.get(anim.get("tipo"))
        if fn is None:
            return
        self._anim_vis_running = True
        self.btn_animar_vis.config(state="disabled", text="⏵ animando…")

        def on_done():
            self._anim_vis_running = False
            self.btn_animar_vis.config(state="normal", text="▶  Animar")

        try:
            fn(self.canvas_diagrama, self._visual_actual, on_done=on_done)
        except Exception:
            on_done()

    # ---------- Práctica mezclada (interleaving — Brunmair 2019) ------
    def _toggle_mezclado(self):
        if self.modo_mezclado:
            # Salir del modo mezclado
            self.modo_mezclado = False
            self._cargar_leccion()
            return
        # Salir de adaptativa si estaba activa
        self.modo_adaptativo = False
        # Construir cola con TODAS las lecciones de 1.1 a 1.5 que tienen
        # pregunta (excluimos 'info' y excluimos Metodología).
        cola = []
        for sec, lecs in LECCIONES.items():
            if "Metodología" in sec:
                continue
            for i, lec in enumerate(lecs):
                if lec["q_type"] != "info":
                    cola.append((sec, i))
        if not cola:
            return
        random.shuffle(cola)
        self.cola_mezclada = cola
        self.pos_mezclada = 0
        self.modo_mezclado = True
        self.seccion_actual, self.idx_leccion = cola[0]
        self._cargar_leccion()

    # ---------- Práctica ADAPTATIVA (retrieval + ponderación) ---------
    # Combina:
    #  · Retrieval practice (Freeman): re-presentación con producción
    #  · Variabilidad     (Sweller) : barajado de opciones
    #  · Interleaving     (Brunmair): no permitir 2 seguidas de misma sección
    #  · Spaced retrieval           : prioriza lecciones débiles
    def _toggle_adaptativa(self, n_preguntas=10):
        if self.modo_adaptativo:
            self.modo_adaptativo = False
            self._cargar_leccion()
            return
        self.modo_mezclado = False

        # 1) Construir lista de candidatos con peso por debilidad
        candidatos, pesos = [], []
        for sec, lecs in LECCIONES.items():
            if "Metodología" in sec:
                continue
            for i, lec in enumerate(lecs):
                if lec["q_type"] == "info":
                    continue
                datos = self.dominio.get((sec, i))
                if datos is None or datos["intentos"] == 0:
                    # Lección nueva (no intentada) → peso intermedio
                    peso = 0.5
                else:
                    # ema 1.0 (perfecta) → peso 0.1
                    # ema 0.0 (siempre falla) → peso 1.1
                    peso = (1.0 - datos["ema"]) + 0.1
                candidatos.append((sec, i))
                pesos.append(peso)

        if not candidatos:
            return

        # 2) Muestreo ponderado SIN reemplazo
        n = min(n_preguntas, len(candidatos))
        cola = self._muestreo_ponderado(candidatos, pesos, n)

        # 3) Anti-clustering: evitar 2 consecutivas de misma sección
        cola = self._anti_cluster(cola)

        self.cola_adaptativa = cola
        self.pos_adaptativa = 0
        self.modo_adaptativo = True
        self.variante_semilla = int(time.time() * 1000)
        self.seccion_actual, self.idx_leccion = cola[0]
        self._cargar_leccion()

    # ---------- Práctica PROGRESIVA (orden por nivel de dificultad) ---
    # Saca preguntas SOLO con pregunta (no info) ordenadas por nivel:
    # básico → intermedio → experto, mezclando secciones dentro de cada nivel
    # para que también haya algo de interleaving.
    def _toggle_progresiva(self):
        if self.modo_progresivo:
            self.modo_progresivo = False
            self._cargar_leccion()
            return
        # Apagar otros modos
        self.modo_mezclado = False
        self.modo_adaptativo = False

        orden = {"básico": 0, "intermedio": 1, "experto": 2}
        cola = []
        for sec, lecs in LECCIONES.items():
            if "Metodología" in sec:
                continue
            for i, lec in enumerate(lecs):
                if lec["q_type"] == "info":
                    continue
                nivel = lec.get("nivel", "básico")
                cola.append((orden.get(nivel, 0), sec, i))

        if not cola:
            return

        # Ordenar por nivel ascendente. Dentro de cada nivel, baraja
        # (interleaving — Brunmair) para que no salgan todas las de
        # 1.1 seguidas y luego todas las de 1.2.
        por_nivel = {}
        for n, sec, i in cola:
            por_nivel.setdefault(n, []).append((sec, i))
        cola_final = []
        for n in sorted(por_nivel.keys()):
            sublista = por_nivel[n]
            random.shuffle(sublista)
            cola_final.extend(sublista)

        self.cola_progresiva = cola_final
        self.pos_progresiva = 0
        self.modo_progresivo = True
        self.seccion_actual, self.idx_leccion = cola_final[0]
        self._cargar_leccion()

    # ---------- Práctica REFUERZO (lección débil + N variantes) -------
    # Se lanza desde la ventana de Estadísticas. Construye una cola
    # con N variantes generadas evaluando el circuito con valores
    # nuevos de las entradas (o barajando las opciones si la lección
    # no tiene diagrama).
    def _toggle_refuerzo(self):
        if self.modo_refuerzo:
            self.modo_refuerzo = False
            self._cargar_leccion()

    def _iniciar_refuerzo_leccion(self, seccion, idx, n_variantes=6):
        """Lanza una sesión de refuerzo enfocada en UNA lección."""
        try:
            base = LECCIONES[seccion][idx]
        except (KeyError, IndexError):
            return
        # Cerramos otros modos
        self.modo_mezclado = False
        self.modo_adaptativo = False
        self.modo_progresivo = False

        semilla = int(time.time() * 1000)
        variantes = generar_variantes_leccion(base, n_variantes, semilla)
        if not variantes:
            self.lbl_feedback.config(
                text="(No se pudieron generar variantes para esta lección.)",
                fg=COLOR_BAD)
            return

        self.cola_refuerzo = [(seccion, idx, v) for v in variantes]
        self.pos_refuerzo = 0
        self.modo_refuerzo = True
        self.refuerzo_titulo = base["title"]
        self.seccion_actual, self.idx_leccion, _ = self.cola_refuerzo[0]
        self._cargar_leccion()

    # ---------- Práctica POR NIVEL (aleatoria, filtrada por dificultad)
    def _toggle_nivel(self):
        if self.modo_nivel:
            self.modo_nivel = False
            self._cargar_leccion()
            return
        # Diálogo para elegir el nivel
        self._dialogo_elegir_nivel()

    def _dialogo_elegir_nivel(self):
        """Pequeña ventana modal para elegir el nivel a practicar."""
        win = tk.Toplevel(self)
        win.title("🎰  Practicar por nivel")
        win.geometry("420x340")
        win.configure(bg=COLOR_BG)
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="🎰  ELIGE TU NIVEL",
                 font=self.font_titulo,
                 bg=COLOR_BG, fg="#8957e5").pack(pady=(16, 4))
        tk.Label(win,
                 text="Recibirás preguntas SOLO de ese nivel,\n"
                      "mezcladas al azar entre todas las secciones\n"
                      "(interleaving — Brunmair & Richter 2019).",
                 font=self.font_normal,
                 bg=COLOR_BG, fg=COLOR_TEXT2,
                 justify="center").pack(pady=(0, 12))

        opciones = [
            ("★      BÁSICO",      "básico",     "#3fb950"),
            ("★★    INTERMEDIO",   "intermedio", "#d29922"),
            ("★★★  EXPERTO",       "experto",    "#da3633"),
            ("🎲    TODOS (mezcla)", "todos",     "#8957e5"),
        ]
        for etiqueta, nivel, color in opciones:
            # Conteo de preguntas disponibles de ese nivel
            n = self._contar_preguntas_nivel(nivel)
            b = tk.Button(
                win, text=f"{etiqueta}    ({n} preguntas)",
                font=self.font_btn, bg=color, fg="white",
                relief="flat", padx=18, pady=10, cursor="hand2",
                anchor="w",
                command=lambda nv=nivel, w=win: (
                    w.destroy(), self._iniciar_modo_nivel(nv)))
            b.pack(fill="x", padx=30, pady=4)
            _bind_hover(b, color)

    @staticmethod
    def _contar_preguntas_nivel(nivel):
        """Cuenta preguntas (no info) del nivel dado en todo el curso."""
        n = 0
        for sec, lecs in LECCIONES.items():
            if "Metodología" in sec:
                continue
            for lec in lecs:
                if lec["q_type"] == "info":
                    continue
                lvl = lec.get("nivel", "básico")
                if nivel == "todos" or lvl == nivel:
                    n += 1
        return n

    def _iniciar_modo_nivel(self, nivel):
        """Construye una cola ALEATORIA de preguntas del nivel dado."""
        self.modo_mezclado = False
        self.modo_adaptativo = False
        self.modo_progresivo = False
        self.modo_refuerzo = False

        cola = []
        for sec, lecs in LECCIONES.items():
            if "Metodología" in sec:
                continue
            for i, lec in enumerate(lecs):
                if lec["q_type"] == "info":
                    continue
                lvl = lec.get("nivel", "básico")
                if nivel == "todos" or lvl == nivel:
                    cola.append((sec, i))
        if not cola:
            self.lbl_feedback.config(
                text=f"(No hay preguntas de nivel «{nivel}».)",
                fg=COLOR_BAD)
            return

        random.shuffle(cola)
        self.cola_nivel = cola
        self.pos_nivel = 0
        self.nivel_filtro = nivel
        self.modo_nivel = True
        self.seccion_actual, self.idx_leccion = cola[0]
        self._cargar_leccion()

    def _iniciar_refuerzo_solo_fallos(self, n_lecciones=8,
                                       n_por_leccion=4,
                                       min_fallos=1):
        """Lanza una sesión enfocada SOLO en lecciones que has FALLADO
        (al menos `min_fallos` veces). Aplica las 4 metodologías:

          • Worked-example primero  (Sweller 2019)
          • Self-explanation        (Hodds 2014)
          • Active retrieval        (Freeman 2014)
          • Interleaving            (Brunmair & Richter 2019)

        Cada lección fallada aporta 1 card de estudio guiado +
        `n_por_leccion` variantes nuevas, todo mezclado anti-cluster.
        """
        falladas = db_lecciones_falladas(min_fallos=min_fallos)
        if not falladas:
            self.lbl_feedback.config(
                text="✓  Aún no tienes fallos registrados.\n"
                     "    Cuando falles alguna pregunta podrás\n"
                     "    practicarla aquí con metodología avanzada.",
                fg=COLOR_OK)
            return

        # Limitamos a las TOP n_lecciones por puntuación
        falladas = falladas[:n_lecciones]

        # Cerramos otros modos
        self.modo_mezclado = False
        self.modo_adaptativo = False
        self.modo_progresivo = False

        # Construimos la cola: por cada lección fallada, generamos cards
        # con metodología (1 worked-example + N preguntas variantes).
        cola = []
        semilla_base = int(time.time() * 1000)
        for j, fila in enumerate(falladas):
            sec, idx, n_fal, n_int, ult, _ = fila
            try:
                base = LECCIONES[sec][idx]
            except (KeyError, IndexError):
                continue
            cards = generar_banco_metodologico(
                base, n_por_leccion, semilla_base + j)
            for c in cards:
                cola.append((sec, idx, c))

        if not cola:
            return

        # Interleaving: que no salgan dos seguidas del mismo concepto.
        # (El worked-example queda al principio de su bloque pero,
        # tras anti_cluster, los grupos pueden re-ordenarse — sigue
        # siendo válido didácticamente.)
        cola = self._anti_cluster_3(cola)

        self.cola_refuerzo = cola
        self.pos_refuerzo = 0
        self.modo_refuerzo = True
        self.refuerzo_titulo = (
            f"📛 SOLO fallos · {len(falladas)} lecciones · "
            f"{len(cola)} cards"
        )
        self.seccion_actual, self.idx_leccion, _ = cola[0]
        self._cargar_leccion()

    def _iniciar_refuerzo_global(self, n_lecciones=5, n_por_leccion=2):
        """Lanza un refuerzo combinado sobre las TOP-N lecciones más débiles
        (basado en EMA en la base de datos)."""
        # 1) Construir lista de débiles desde el dominio cargado
        debiles = sorted(
            [(sec, i, d) for (sec, i), d in self.dominio.items()
             if d["intentos"] > 0 and d["ema"] < 0.8],
            key=lambda x: x[2]["ema"])[:n_lecciones]
        if not debiles:
            self.lbl_feedback.config(
                text="✓ Aún no tienes lecciones débiles registradas. "
                     "Haz algunas preguntas primero.",
                fg=COLOR_OK)
            return

        self.modo_mezclado = False
        self.modo_adaptativo = False
        self.modo_progresivo = False

        cola = []
        for sec, i, _ in debiles:
            base = LECCIONES.get(sec, [None] * (i + 1))[i] \
                   if i < len(LECCIONES.get(sec, [])) else None
            if base is None:
                continue
            semilla = int(time.time() * 1000) + i
            variantes = generar_variantes_leccion(base, n_por_leccion, semilla)
            for v in variantes:
                cola.append((sec, i, v))
        if not cola:
            return

        # Anti-clustering: que no salgan dos seguidas del mismo concepto
        # (igual idea que en modo adaptativa)
        cola = self._anti_cluster_3(cola)

        self.cola_refuerzo = cola
        self.pos_refuerzo = 0
        self.modo_refuerzo = True
        self.refuerzo_titulo = f"top-{len(debiles)} débiles"
        self.seccion_actual, self.idx_leccion, _ = cola[0]
        self._cargar_leccion()

    @staticmethod
    def _anti_cluster_3(cola):
        """Versión de anti-cluster para tuplas (sec, idx, variante).
        Evita 2 seguidas de la misma (sec, idx)."""
        if len(cola) <= 2:
            return cola
        cola = list(cola)
        for _ in range(10):
            cambios = 0
            for i in range(len(cola) - 1):
                if (cola[i][0], cola[i][1]) == (cola[i + 1][0], cola[i + 1][1]):
                    for j in range(i + 2, len(cola)):
                        if ((cola[j][0], cola[j][1]) !=
                                (cola[i][0], cola[i][1])):
                            cola[i + 1], cola[j] = cola[j], cola[i + 1]
                            cambios += 1
                            break
            if cambios == 0:
                break
        return cola

    @staticmethod
    def _muestreo_ponderado(items, pesos, n):
        """Muestreo aleatorio sin reemplazo, sesgado por 'pesos'."""
        items = list(items)
        pesos = list(pesos)
        seleccion = []
        for _ in range(n):
            if not items:
                break
            total = sum(pesos)
            r = random.uniform(0, total)
            acc = 0
            for j, w in enumerate(pesos):
                acc += w
                if acc >= r:
                    seleccion.append(items[j])
                    items.pop(j)
                    pesos.pop(j)
                    break
        return seleccion

    @staticmethod
    def _anti_cluster(cola):
        """Reordena para minimizar (sec, idx) consecutivas de misma sección."""
        if len(cola) <= 2:
            return cola
        cola = list(cola)
        for _ in range(10):  # algunas pasadas suelen bastar
            cambios = 0
            for i in range(len(cola) - 1):
                if cola[i][0] == cola[i + 1][0]:
                    # intentar swap con un vecino más adelante
                    for j in range(i + 2, len(cola)):
                        if (cola[j][0] != cola[i][0] and
                                (j == len(cola) - 1 or
                                 cola[j + 1][0] != cola[i][0])):
                            cola[i + 1], cola[j] = cola[j], cola[i + 1]
                            cambios += 1
                            break
            if cambios == 0:
                break
        return cola

    # ---------- Ventana de estadísticas (lee SQLite) ------------------
    def _mostrar_estadisticas(self):
        total, correctas, por_seccion = db_estadisticas()
        dominio = db_cargar_dominio()

        # Ranking de las 10 lecciones MÁS DÉBILES (ema más bajo) con
        # al menos 1 intento
        debiles = sorted(
            [(sec, i, d) for (sec, i), d in dominio.items()
             if d["intentos"] > 0],
            key=lambda x: x[2]["ema"])[:10]

        win = tk.Toplevel(self)
        win.title("📊  Mis estadísticas — Aprender Lógica")
        win.geometry("780x620")
        win.configure(bg=COLOR_BG)

        tk.Label(win, text="📊  MIS ESTADÍSTICAS",
                 font=self.font_titulo,
                 bg=COLOR_BG, fg=COLOR_ACCENT).pack(pady=(14, 4))

        if total == 0:
            tk.Label(win, text="Aún no has respondido ninguna pregunta.\n"
                              "Cuando lo hagas, aquí verás tus estadísticas.",
                     font=self.font_normal, bg=COLOR_BG, fg=COLOR_TEXT,
                     justify="center").pack(pady=20)
            tk.Button(win, text="Cerrar", font=self.font_btn,
                      bg=COLOR_ACCENT, fg="white", relief="flat",
                      padx=18, pady=6, command=win.destroy).pack(pady=14)
            return

        pct = 100 * correctas / max(total, 1)
        resumen = (f"Total de respuestas registradas: {total}\n"
                   f"Aciertos: {correctas}   ({pct:.1f} %)\n"
                   f"BD almacenada en: {DB_PATH}")
        tk.Label(win, text=resumen, font=self.font_normal,
                 bg=COLOR_BG, fg=COLOR_TEXT, justify="left").pack(
            padx=14, pady=(0, 10))

        # --- Por sección: barras horizontales (ACIERTOS %) -------------
        tk.Label(win, text="ACIERTOS POR SECCIÓN", font=self.font_subt,
                 bg=COLOR_BG, fg=COLOR_ACCENT).pack(anchor="w", padx=14)
        tk.Label(win,
                 text="Verde ≥ 70 %   ·   ámbar 50–70 %   ·   rojo < 50 %",
                 font=self.font_normal,
                 bg=COLOR_BG, fg=COLOR_TEXT2).pack(anchor="w", padx=14)

        contb = tk.Frame(win, bg=COLOR_BG)
        contb.pack(fill="x", padx=14, pady=(4, 8))

        for sec, n, ok in por_seccion:
            ok = ok or 0
            p = 100 * ok / max(n, 1)
            color = (COLOR_OK if p >= 70
                     else "#d29922" if p >= 50 else COLOR_BAD)

            fila = tk.Frame(contb, bg=COLOR_BG)
            fila.pack(fill="x", pady=1)

            # Etiqueta de la sección (alineada a la izquierda)
            tk.Label(fila, text=sec.strip(),
                     bg=COLOR_BG, fg=COLOR_TEXT,
                     font=self.font_normal, width=32,
                     anchor="w").pack(side="left")

            # Barra horizontal usando un canvas
            cw, ch = 260, 14
            c = tk.Canvas(fila, width=cw, height=ch, bg=COLOR_BG,
                          highlightthickness=0)
            c.pack(side="left", padx=6)
            c.create_rectangle(0, 0, cw, ch,
                                fill="#2a3441", outline="")
            ancho = max(1, int(cw * p / 100))
            c.create_rectangle(0, 0, ancho, ch,
                                fill=color, outline="")
            # Marca del 70 % (umbral de dominio)
            x70 = int(cw * 0.7)
            c.create_line(x70, 0, x70, ch, fill="#3fb950",
                          dash=(2, 2))

            # Texto numérico (%) + intentos
            tk.Label(fila,
                     text=f"{p:.0f}%   ({ok}/{n})",
                     bg=COLOR_BG, fg=color,
                     font=self.font_normal,
                     width=14, anchor="w").pack(side="left")

        # --- Top 10 débiles + botones de refuerzo individuales ---
        tk.Label(win, text="\nTUS 10 LECCIONES MÁS DÉBILES (dominio EMA)",
                 font=self.font_subt,
                 bg=COLOR_BG, fg=COLOR_BAD).pack(anchor="w", padx=14)
        tk.Label(win,
                 text="Pulsa  🎯 Reforzar  junto a una lección para generar\n"
                      "variantes nuevas (mismo circuito, valores distintos)\n"
                      "y subir su dominio.",
                 font=self.font_normal,
                 bg=COLOR_BG, fg=COLOR_TEXT2,
                 justify="left").pack(anchor="w", padx=14)

        cont_deb = tk.Frame(win, bg=COLOR_BG)
        cont_deb.pack(fill="x", padx=18, pady=(4, 4))

        for sec, i, d in debiles:
            try:
                title = LECCIONES[sec][i]["title"]
            except Exception:
                title = "?"
            fila = tk.Frame(cont_deb, bg=COLOR_BG)
            fila.pack(fill="x", anchor="w", pady=1)

            txt = (f"  · {sec.split()[0]} L{i + 1}: {title}    "
                   f"EMA={d['ema']:.0%}  ·  {d['correctas']}/{d['intentos']}")
            color = (COLOR_BAD if d["ema"] < 0.5
                     else "#d29922" if d["ema"] < 0.7 else COLOR_TEXT)
            tk.Label(fila, text=txt, font=self.font_normal,
                     bg=COLOR_BG, fg=color, anchor="w").pack(
                side="left", fill="x", expand=True)

            # Botón "🎯 Reforzar" para la lección concreta
            tk.Button(
                fila, text="🎯  Reforzar",
                font=self.font_btn,
                bg="#da3633", fg="white", relief="flat",
                padx=8, pady=2, cursor="hand2",
                command=lambda s=sec, ii=i: (
                    win.destroy(),
                    self._iniciar_refuerzo_leccion(s, ii, n_variantes=6))
            ).pack(side="right", padx=4)

        # --- Bloque destacado: PRACTICAR SOLO FALLOS con metodología ----
        # Lee la BD y muestra cuántas preguntas se han fallado para que
        # el usuario decida si quiere lanzar la práctica metodológica.
        falladas = db_lecciones_falladas(min_fallos=1)
        if falladas:
            top_n = min(8, len(falladas))
            n_fallos_tot = sum(f[2] for f in falladas)
            mef = tk.Frame(win, bg="#3a1d1d", bd=1, relief="solid")
            mef.pack(fill="x", padx=14, pady=(10, 4))
            tk.Label(
                mef,
                text=f"📛  TIENES {n_fallos_tot} FALLO(S) EN "
                     f"{len(falladas)} LECCIÓN(ES)",
                font=self.font_subt,
                bg="#3a1d1d", fg="white").pack(anchor="w",
                                                padx=10, pady=(6, 2))
            tk.Label(
                mef,
                text=(
                    "El siguiente modo aplica las 4 metodologías con\n"
                    "mayor evidencia en aprendizaje matemático:\n"
                    "  ① Worked-example primero (Sweller 2019)\n"
                    "  ② Self-explanation, 4 preguntas (Hodds 2014)\n"
                    "  ③ Retrieval activa con variantes (Freeman 2014)\n"
                    "  ④ Interleaving anti-clúster (Brunmair 2019)"
                ),
                font=self.font_normal,
                bg="#3a1d1d", fg="#f4d6d6",
                justify="left").pack(anchor="w", padx=10, pady=(0, 4))

            tk.Button(
                mef,
                text=(f"📛  Practicar SOLO fallos  ·  "
                      f"top {top_n} × 4 variantes c/u"),
                font=self.font_btn,
                bg="#da3633", fg="white", relief="flat",
                padx=16, pady=6, cursor="hand2",
                command=lambda: (
                    win.destroy(),
                    self._iniciar_refuerzo_solo_fallos(
                        n_lecciones=top_n, n_por_leccion=4))
            ).pack(anchor="w", padx=10, pady=(2, 8))

        # --- Botonera inferior: refuerzo global + cerrar ---
        botonera = tk.Frame(win, bg=COLOR_BG)
        botonera.pack(pady=14)

        tk.Button(
            botonera, text="🚀  Reforzar TODAS las débiles",
            font=self.font_btn,
            bg=COLOR_OK, fg="white", relief="flat",
            padx=18, pady=6, cursor="hand2",
            command=lambda: (win.destroy(),
                             self._iniciar_refuerzo_global(
                                 n_lecciones=5, n_por_leccion=2))
        ).pack(side="left", padx=4)

        tk.Button(botonera, text="Cerrar", font=self.font_btn,
                  bg=COLOR_ACCENT, fg="white", relief="flat",
                  padx=18, pady=6, cursor="hand2",
                  command=win.destroy).pack(side="left", padx=4)

    # ---------- Ejemplos PARECIDOS (no idénticos) — refuerzo cognitivo
    def _mostrar_ejemplos_parecidos(self):
        """Abre un popup con ejemplos análogos al de la lección actual.

        Si la lección tiene `similar_examples` (lista de strings), los
        muestra. Si no, intenta autogenerar variantes para circuitos.
        Si tampoco hay diagrama, ofrece links a 3 lecciones cercanas
        de la misma sección como práctica relacionada.
        """
        try:
            base = LECCIONES[self.seccion_actual][self.idx_leccion]
        except (KeyError, IndexError):
            return

        win = tk.Toplevel(self)
        win.title("📚  Ejemplos parecidos — " + base["title"])
        win.geometry("760x640")
        win.configure(bg=COLOR_BG)

        tk.Label(win, text=f"📚  Ejemplos parecidos · {base['title']}",
                 font=self.font_titulo,
                 bg=COLOR_BG, fg=COLOR_ACCENT,
                 wraplength=720,
                 justify="center").pack(pady=(14, 4))
        tk.Label(win,
                 text="Casos análogos al concepto de esta lección. \n"
                      "No son la MISMA pregunta — son variaciones que activan\n"
                      "el patrón de razonamiento desde un ángulo distinto.\n"
                      "Esto mejora la TRANSFERENCIA del concepto (Sweller, 2019).",
                 font=self.font_normal,
                 bg=COLOR_BG, fg=COLOR_TEXT2,
                 justify="left").pack(padx=18, pady=(0, 8))

        contenedor = tk.Frame(win, bg=COLOR_BG)
        contenedor.pack(fill="both", expand=True, padx=18, pady=4)

        # Fuente 1: campo similar_examples (manual, lecciones clave)
        similares = base.get("similar_examples") or []

        # Fuente 2: si hay diagrama, autogeneramos 3 variantes
        if not similares and base.get("diagram"):
            try:
                vs = generar_variantes_leccion(base, 3, int(time.time()))
                for v in vs:
                    tv = v["diagram"].get("trace_values", {})
                    args = ", ".join(f"{k}={tv[k]}" for k in tv)
                    similares.append(
                        f"Para el mismo circuito con {args}:\n"
                        f"  {v['explanation']}"
                    )
            except Exception:
                pass

        # Render
        if similares:
            for i, ej in enumerate(similares, start=1):
                bloque = tk.LabelFrame(
                    contenedor, text=f"  Caso parecido {i}  ",
                    bg=COLOR_EXAMPLE, fg=COLOR_ACCENT,
                    font=self.font_subt, bd=1, relief="solid",
                    labelanchor="nw")
                bloque.pack(fill="x", pady=6)
                tk.Label(bloque, text=ej,
                         bg=COLOR_EXAMPLE, fg=COLOR_TEXT,
                         font=self.font_mono,
                         justify="left", anchor="w",
                         wraplength=700).pack(padx=12, pady=10, anchor="w")
        else:
            tk.Label(contenedor,
                     text=(
                       "No hay ejemplos análogos diseñados para esta\n"
                       "lección concreta. Como alternativa, prueba:\n"
                       "  •  🎯  Reforzar esta lección\n"
                       "  •  🎲  Mezclada (interleaving — Brunmair 2019)\n"
                       "  •  Las siguientes lecciones de la misma sección.\n"
                     ),
                     bg=COLOR_BG, fg=COLOR_TEXT2,
                     font=self.font_normal,
                     justify="left").pack(padx=10, pady=20, anchor="w")

        tk.Button(win, text="Cerrar", font=self.font_btn,
                  bg=COLOR_ACCENT, fg="white",
                  relief="flat", padx=18, pady=6, cursor="hand2",
                  command=win.destroy).pack(pady=14)

    # ---------- Ejemplos PROGRESIVOS (básico → intermedio → experto) --
    def _mostrar_ejemplos_progresivos(self):
        """Abre un popup con 3 ejemplos del banco EXTRA_EJEMPLOS,
        cada uno en una pestaña/card con su nivel:
              [BÁSICO]  →  [INTERMEDIO]  →  [EXPERTO]
        Aplica el Guidance-Fading Effect (Sweller 2019):
        empezar guiado → ir soltando andamiaje.
        """
        try:
            base = LECCIONES[self.seccion_actual][self.idx_leccion]
        except (KeyError, IndexError):
            return
        titulo_base = base["title"]

        # Buscar en el banco
        ejemplos = EXTRA_EJEMPLOS.get((self.seccion_actual, titulo_base))
        if not ejemplos:
            # Tolerar coincidencias parciales si el título incluye sufijos
            for (sec, tit), val in EXTRA_EJEMPLOS.items():
                if sec == self.seccion_actual and (
                    tit.startswith(titulo_base[:25]) or
                    titulo_base.startswith(tit[:25])
                ):
                    ejemplos = val
                    break

        win = tk.Toplevel(self)
        win.title("💼  Ejemplos progresivos — " + titulo_base)
        win.geometry("820x680")
        win.configure(bg=COLOR_BG)

        tk.Label(win, text="💼  EJEMPLOS PROGRESIVOS",
                 font=self.font_titulo,
                 bg=COLOR_BG, fg=COLOR_ACCENT).pack(pady=(14, 4))
        tk.Label(win, text=titulo_base, font=self.font_subt,
                 bg=COLOR_BG, fg=COLOR_TEXT2,
                 wraplength=760, justify="center").pack(pady=(0, 4))
        tk.Label(
            win,
            text=(
                "3 ejemplos crecientes en dificultad. Estudia el primero\n"
                "como WORKED EXAMPLE (cobre la solución, anticipa cada paso).\n"
                "Luego el intermedio con menos andamiaje. Finalmente el experto\n"
                "te conecta con casos reales de IA."
            ),
            font=self.font_normal,
            bg=COLOR_BG, fg=COLOR_TEXT2,
            justify="left").pack(padx=20, pady=(0, 10))

        if not ejemplos:
            tk.Label(
                win,
                text="(Aún no hay ejemplos progresivos diseñados para esta\n"
                     "lección concreta. Usa el botón 📚 Ejemplos parecidos\n"
                     "o el modo 🎯 Refuerzo para más práctica.)",
                font=self.font_normal,
                bg=COLOR_BG, fg=COLOR_TEXT,
                justify="center").pack(pady=30)
        else:
            # Cada ejemplo en su propia card de color
            colores_card = ["#102530", "#15202b", "#241a26"]
            etiquetas = ["★  BÁSICO", "★★  INTERMEDIO", "★★★  EXPERTO"]
            color_etq = [COLOR_OK, "#d29922", COLOR_BAD]

            cont = tk.Frame(win, bg=COLOR_BG)
            cont.pack(fill="both", expand=True, padx=20, pady=4)

            for i, ej in enumerate(ejemplos[:3]):
                card = tk.LabelFrame(
                    cont, text="  " + etiquetas[i] + "  ",
                    bg=colores_card[i], fg=color_etq[i],
                    font=self.font_subt, bd=1, relief="solid",
                    labelanchor="nw")
                card.pack(fill="x", pady=6)
                # Quitar la etiqueta "[BÁSICO]" inicial si la trae el string
                texto = ej
                for tag in ("[BÁSICO]", "[INTERMEDIO]", "[EXPERTO]"):
                    if texto.startswith(tag):
                        texto = texto[len(tag):].strip()
                tk.Label(card, text=texto,
                         bg=colores_card[i], fg=COLOR_TEXT,
                         font=self.font_mono,
                         justify="left", anchor="w",
                         wraplength=760).pack(padx=12, pady=10, anchor="w")

        tk.Button(win, text="Cerrar", font=self.font_btn,
                  bg=COLOR_ACCENT, fg="white",
                  relief="flat", padx=18, pady=6, cursor="hand2",
                  command=win.destroy).pack(pady=14)

    # ---------- Auto-explicación (las 4 preguntas de Hodds 2014) ------
    def _mostrar_autoexplicacion(self):
        """Abre un popup con las 4 preguntas de self-explanation y un
        cuadro de texto para que el usuario escriba sus respuestas.
        Apoya la práctica #2 (Hodds, Alcock & Inglis 2014, d=0.95)."""
        win = tk.Toplevel(self)
        win.title("💭  Auto-explícate — Las 4 preguntas de Hodds (2014)")
        win.geometry("720x600")
        win.configure(bg=COLOR_BG)

        tk.Label(win,
                 text="💭  AUTO-EXPLICACIÓN",
                 font=self.font_titulo,
                 bg=COLOR_BG, fg=COLOR_ACCENT).pack(pady=(14, 4))

        tk.Label(win, text=AUTOEXPLICACION_INFO,
                 font=self.font_normal,
                 bg=COLOR_BG, fg=COLOR_TEXT,
                 justify="left",
                 wraplength=680).pack(padx=14, pady=(0, 10))

        for pregunta in AUTOEXPLICACION_4Q:
            frame = tk.LabelFrame(win, text=pregunta,
                                  font=self.font_subt,
                                  bg=COLOR_THEORY, fg=COLOR_TEXT,
                                  labelanchor="nw", bd=1, relief="solid")
            frame.pack(fill="x", padx=14, pady=4)
            tk.Text(frame, height=2, wrap="word",
                    bg=COLOR_PANEL, fg=COLOR_TEXT,
                    font=self.font_normal, bd=0,
                    padx=8, pady=6).pack(fill="x", padx=2, pady=2)

        tk.Button(win, text="Cerrar",
                  font=self.font_btn,
                  bg=COLOR_ACCENT, fg="white",
                  relief="flat", padx=18, pady=6,
                  cursor="hand2",
                  command=win.destroy).pack(pady=14)


# =====================================================================
def main():
    try:
        app = AppLogica()
        app.mainloop()
    except tk.TclError as e:
        print("No se pudo iniciar la GUI:", e)
        print("Comprueba que tu sistema tenga soporte gráfico para Tkinter.")


if __name__ == "__main__":
    main()


/* ──────────── Modo Maestro RF (Aprendizaje por Refuerzo) ──────────────
   Octavo temario guiado, independiente del resto. Piloto de 3 conceptos (12 preguntas aplanadas) construido leyendo Kelleher, The Science of Deep Learning, Cap.11 (Reinforcement Learning: bandido multi-brazo, procesos de Markov, función de valor) -- código 100% numpy, sin librerías de RL especializadas.
   Fuente: ver comentario de cada tema (cita de página real). Verificado
   ejecutando de verdad el código con el intérprete Python del sistema antes
   de fijar cualquier número en la teoría o en las preguntas. */
const EX_RF = [
 {
  "name": "Refuerzo · Bandido multi-brazo y ε-greedy",
  "theory": "Imaginate 3 máquinas tragamonedas distintas, cada una con una probabilidad de pago distinta que NO conocés de antemano — tenés que ir probando para descubrir cuál conviene. Si actuás <b>greedy</b> (\"codicioso\": siempre elegís la máquina que hasta ahora te dio mejor resultado), corrés un riesgo real: si por pura mala suerte la MEJOR máquina te dio un resultado malo en tu primer intento, la vas a descartar y nunca más la vas a volver a probar — quedás \"pegado\" explotando una máquina mediocre para siempre.<br><br>En el código, esto pasa literalmente: la estrategia greedy (ε=0) elige el brazo 2 (el mejor en realidad) exactamente 0 de 80 veces, terminando con una recompensa total de solo ≈85,0. La estrategia <b>ε-greedy</b> (con ε=0,1: el 10% de las veces elegís un brazo al azar en vez del \"mejor conocido\") sí termina descubriendo que el brazo 2 es el mejor, eligiéndolo 69 de 80 veces, y consigue casi el DOBLE de recompensa total: ≈169,2. Ese 10% de \"probar algo distinto\" es lo que evita quedarse pegado en una mala decisión temprana.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.11.2, Algoritmo 11.1): el valor estimado de una acción se actualiza como $Q(a) \\leftarrow Q(a) + \\frac{r(a) - Q(a)}{N(a)}$, y la política ε-greedy elige $\\arg\\max_a Q(a)$ con probabilidad $1-\\varepsilon$, o una acción al azar con probabilidad $\\varepsilon$.",
  "code": "# Bandido multi-brazo y el dilema exploracion vs explotacion (Kelleher,\n# Sec 11.2, Algoritmo 11.1: e-greedy). Formula EXACTA del libro para\n# actualizar el valor estimado: Q(a) = Q(a) + (r(a) - Q(a)) / N(a)\n# (n_pasos=80: mantiene la traza del depurador dentro del limite de pasos\n# de esta app, sin cambiar el algoritmo del libro).\nimport numpy as np\n\nverdaderas_medias = [1.0, 1.5, 2.0]  # el brazo 2 es el MEJOR en realidad\nn_pasos = 80\n\ndef simular(epsilon, seed):\n    rng = np.random.default_rng(seed)\n    Q = [0.0, 0.0, 0.0]; N = [0, 0, 0]\n    recompensa_total = 0.0; elegido_optimo = 0\n    for t in range(n_pasos):\n        if rng.random() < epsilon:\n            a = rng.integers(0, 3)          # explorar: brazo al azar\n        else:\n            a = int(np.argmax(Q))            # explotar: el mejor conocido\n        r = rng.normal(verdaderas_medias[a], 1.0)\n        N[a] += 1\n        Q[a] = Q[a] + (r - Q[a]) / N[a]      # formula del Algoritmo 11.1\n        recompensa_total += r\n        if a == 2: elegido_optimo += 1\n    return Q, N, recompensa_total, elegido_optimo\n\nQg, Ng, Rg, Og = simular(epsilon=0.0, seed=15)   # GREEDY puro\nQe, Ne, Re, Oe = simular(epsilon=0.1, seed=15)   # EPSILON-GREEDY\n\nprint(\"GREEDY (epsilon=0):     Q estimado=\", [round(v,2) for v in Qg])\nprint(\"  veces elegido cada brazo:\", Ng, \" recompensa total:\", round(Rg,1))\nprint(\"  veces que eligio el brazo OPTIMO (2):\", Og, \"/\", n_pasos)\nprint(\"\\nEPSILON-GREEDY (e=0.1): Q estimado=\", [round(v,2) for v in Qe])\nprint(\"  veces elegido cada brazo:\", Ne, \" recompensa total:\", round(Re,1))\nprint(\"  veces que eligio el brazo OPTIMO (2):\", Oe, \"/\", n_pasos)",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Greedy · recompensa total",
     "ε-greedy · recompensa total"
    ],
    "values": [
     85.0,
     169.2
    ],
    "unit": "",
    "aria": "La estrategia greedy termina con recompensa total 85.0 (nunca descubre el mejor brazo); epsilon-greedy termina con 169.2, casi el doble (lo descubre explorando)"
   }
  },
  "application": "El dilema exploración-explotación no es exclusivo de máquinas tragamonedas: es el mismo problema de fondo que enfrenta Netflix decidiendo si recomendarte tu género favorito de siempre (explotar lo que sabe que te gusta) o algo nuevo que podría gustarte aún más (explorar); o un ensayo clínico decidiendo si seguir dando el tratamiento que mejor resultado dio hasta ahora, o probar uno experimental que podría ser mejor todavía. Cualquier sistema que aprende actuando — no solo observando — tarde o temprano se topa con esta misma tensión, y ε-greedy es la solución más simple que existe para resolverla (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.2).",
  "codeAnatomy": {
   "title": "ε-greedy: explorar o explotar",
   "caption": "Decisión + actualización del bandido multi-brazo (Kelleher, Alg. 11.1)",
   "lines": [
    "if rng.random() < epsilon:",
    "    a = rng.integers(0, 3)",
    "else:",
    "    a = int(np.argmax(Q))",
    "r = rng.normal(verdaderas_medias[a], 1.0)",
    "N[a] += 1",
    "Q[a] = Q[a] + (r - Q[a]) / N[a]"
   ],
   "annotations": [
    {
     "line": 0,
     "text": "rng.random() < epsilon",
     "label": "¿Explorar?",
     "desc": "(al azar, con prob. epsilon)",
     "side": "top"
    },
    {
     "line": 1,
     "text": "rng.integers(0, 3)",
     "label": "Brazo al azar",
     "desc": "(explorar)",
     "side": "top"
    },
    {
     "line": 3,
     "text": "np.argmax(Q)",
     "label": "Mejor conocido",
     "desc": "(explotar)",
     "side": "top"
    },
    {
     "line": 4,
     "text": "rng.normal(verdaderas_medias[a], 1.0)",
     "label": "Recompensa recibida",
     "desc": "(al azar, centrada en la media real)",
     "side": "bottom"
    },
    {
     "line": 5,
     "text": "N[a] += 1",
     "label": "Contador",
     "desc": "(veces que se probó ese brazo)",
     "side": "bottom"
    },
    {
     "line": 6,
     "text": "(r - Q[a]) / N[a]",
     "label": "Ajuste incremental",
     "desc": "(fórmula del libro, Alg. 11.1)",
     "side": "bottom"
    }
   ]
  }
 },
 {
  "name": "Refuerzo · Bandido multi-brazo y ε-greedy — pregunta 2",
  "theory": "Imaginate 3 máquinas tragamonedas distintas, cada una con una probabilidad de pago distinta que NO conocés de antemano — tenés que ir probando para descubrir cuál conviene. Si actuás <b>greedy</b> (\"codicioso\": siempre elegís la máquina que hasta ahora te dio mejor resultado), corrés un riesgo real: si por pura mala suerte la MEJOR máquina te dio un resultado malo en tu primer intento, la vas a descartar y nunca más la vas a volver a probar — quedás \"pegado\" explotando una máquina mediocre para siempre.<br><br>En el código, esto pasa literalmente: la estrategia greedy (ε=0) elige el brazo 2 (el mejor en realidad) exactamente 0 de 80 veces, terminando con una recompensa total de solo ≈85,0. La estrategia <b>ε-greedy</b> (con ε=0,1: el 10% de las veces elegís un brazo al azar en vez del \"mejor conocido\") sí termina descubriendo que el brazo 2 es el mejor, eligiéndolo 69 de 80 veces, y consigue casi el DOBLE de recompensa total: ≈169,2. Ese 10% de \"probar algo distinto\" es lo que evita quedarse pegado en una mala decisión temprana.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.11.2, Algoritmo 11.1): el valor estimado de una acción se actualiza como $Q(a) \\leftarrow Q(a) + \\frac{r(a) - Q(a)}{N(a)}$, y la política ε-greedy elige $\\arg\\max_a Q(a)$ con probabilidad $1-\\varepsilon$, o una acción al azar con probabilidad $\\varepsilon$.",
  "code": "# Bandido multi-brazo y el dilema exploracion vs explotacion (Kelleher,\n# Sec 11.2, Algoritmo 11.1: e-greedy). Formula EXACTA del libro para\n# actualizar el valor estimado: Q(a) = Q(a) + (r(a) - Q(a)) / N(a)\n# (n_pasos=80: mantiene la traza del depurador dentro del limite de pasos\n# de esta app, sin cambiar el algoritmo del libro).\nimport numpy as np\n\nverdaderas_medias = [1.0, 1.5, 2.0]  # el brazo 2 es el MEJOR en realidad\nn_pasos = 80\n\ndef simular(epsilon, seed):\n    rng = np.random.default_rng(seed)\n    Q = [0.0, 0.0, 0.0]; N = [0, 0, 0]\n    recompensa_total = 0.0; elegido_optimo = 0\n    for t in range(n_pasos):\n        if rng.random() < epsilon:\n            a = rng.integers(0, 3)          # explorar: brazo al azar\n        else:\n            a = int(np.argmax(Q))            # explotar: el mejor conocido\n        r = rng.normal(verdaderas_medias[a], 1.0)\n        N[a] += 1\n        Q[a] = Q[a] + (r - Q[a]) / N[a]      # formula del Algoritmo 11.1\n        recompensa_total += r\n        if a == 2: elegido_optimo += 1\n    return Q, N, recompensa_total, elegido_optimo\n\nQg, Ng, Rg, Og = simular(epsilon=0.0, seed=15)   # GREEDY puro\nQe, Ne, Re, Oe = simular(epsilon=0.1, seed=15)   # EPSILON-GREEDY\n\nprint(\"GREEDY (epsilon=0):     Q estimado=\", [round(v,2) for v in Qg])\nprint(\"  veces elegido cada brazo:\", Ng, \" recompensa total:\", round(Rg,1))\nprint(\"  veces que eligio el brazo OPTIMO (2):\", Og, \"/\", n_pasos)\nprint(\"\\nEPSILON-GREEDY (e=0.1): Q estimado=\", [round(v,2) for v in Qe])\nprint(\"  veces elegido cada brazo:\", Ne, \" recompensa total:\", round(Re,1))\nprint(\"  veces que eligio el brazo OPTIMO (2):\", Oe, \"/\", n_pasos)",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Greedy · recompensa total",
     "ε-greedy · recompensa total"
    ],
    "values": [
     85.0,
     169.2
    ],
    "unit": "",
    "aria": "La estrategia greedy termina con recompensa total 85.0 (nunca descubre el mejor brazo); epsilon-greedy termina con 169.2, casi el doble (lo descubre explorando)"
   }
  },
  "application": "El dilema exploración-explotación no es exclusivo de máquinas tragamonedas: es el mismo problema de fondo que enfrenta Netflix decidiendo si recomendarte tu género favorito de siempre (explotar lo que sabe que te gusta) o algo nuevo que podría gustarte aún más (explorar); o un ensayo clínico decidiendo si seguir dando el tratamiento que mejor resultado dio hasta ahora, o probar uno experimental que podría ser mejor todavía. Cualquier sistema que aprende actuando — no solo observando — tarde o temprano se topa con esta misma tensión, y ε-greedy es la solución más simple que existe para resolverla (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.2)."
 },
 {
  "name": "Refuerzo · Bandido multi-brazo y ε-greedy — pregunta 3",
  "theory": "Imaginate 3 máquinas tragamonedas distintas, cada una con una probabilidad de pago distinta que NO conocés de antemano — tenés que ir probando para descubrir cuál conviene. Si actuás <b>greedy</b> (\"codicioso\": siempre elegís la máquina que hasta ahora te dio mejor resultado), corrés un riesgo real: si por pura mala suerte la MEJOR máquina te dio un resultado malo en tu primer intento, la vas a descartar y nunca más la vas a volver a probar — quedás \"pegado\" explotando una máquina mediocre para siempre.<br><br>En el código, esto pasa literalmente: la estrategia greedy (ε=0) elige el brazo 2 (el mejor en realidad) exactamente 0 de 80 veces, terminando con una recompensa total de solo ≈85,0. La estrategia <b>ε-greedy</b> (con ε=0,1: el 10% de las veces elegís un brazo al azar en vez del \"mejor conocido\") sí termina descubriendo que el brazo 2 es el mejor, eligiéndolo 69 de 80 veces, y consigue casi el DOBLE de recompensa total: ≈169,2. Ese 10% de \"probar algo distinto\" es lo que evita quedarse pegado en una mala decisión temprana.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.11.2, Algoritmo 11.1): el valor estimado de una acción se actualiza como $Q(a) \\leftarrow Q(a) + \\frac{r(a) - Q(a)}{N(a)}$, y la política ε-greedy elige $\\arg\\max_a Q(a)$ con probabilidad $1-\\varepsilon$, o una acción al azar con probabilidad $\\varepsilon$.",
  "code": "# Bandido multi-brazo y el dilema exploracion vs explotacion (Kelleher,\n# Sec 11.2, Algoritmo 11.1: e-greedy). Formula EXACTA del libro para\n# actualizar el valor estimado: Q(a) = Q(a) + (r(a) - Q(a)) / N(a)\n# (n_pasos=80: mantiene la traza del depurador dentro del limite de pasos\n# de esta app, sin cambiar el algoritmo del libro).\nimport numpy as np\n\nverdaderas_medias = [1.0, 1.5, 2.0]  # el brazo 2 es el MEJOR en realidad\nn_pasos = 80\n\ndef simular(epsilon, seed):\n    rng = np.random.default_rng(seed)\n    Q = [0.0, 0.0, 0.0]; N = [0, 0, 0]\n    recompensa_total = 0.0; elegido_optimo = 0\n    for t in range(n_pasos):\n        if rng.random() < epsilon:\n            a = rng.integers(0, 3)          # explorar: brazo al azar\n        else:\n            a = int(np.argmax(Q))            # explotar: el mejor conocido\n        r = rng.normal(verdaderas_medias[a], 1.0)\n        N[a] += 1\n        Q[a] = Q[a] + (r - Q[a]) / N[a]      # formula del Algoritmo 11.1\n        recompensa_total += r\n        if a == 2: elegido_optimo += 1\n    return Q, N, recompensa_total, elegido_optimo\n\nQg, Ng, Rg, Og = simular(epsilon=0.0, seed=15)   # GREEDY puro\nQe, Ne, Re, Oe = simular(epsilon=0.1, seed=15)   # EPSILON-GREEDY\n\nprint(\"GREEDY (epsilon=0):     Q estimado=\", [round(v,2) for v in Qg])\nprint(\"  veces elegido cada brazo:\", Ng, \" recompensa total:\", round(Rg,1))\nprint(\"  veces que eligio el brazo OPTIMO (2):\", Og, \"/\", n_pasos)\nprint(\"\\nEPSILON-GREEDY (e=0.1): Q estimado=\", [round(v,2) for v in Qe])\nprint(\"  veces elegido cada brazo:\", Ne, \" recompensa total:\", round(Re,1))\nprint(\"  veces que eligio el brazo OPTIMO (2):\", Oe, \"/\", n_pasos)",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Greedy · recompensa total",
     "ε-greedy · recompensa total"
    ],
    "values": [
     85.0,
     169.2
    ],
    "unit": "",
    "aria": "La estrategia greedy termina con recompensa total 85.0 (nunca descubre el mejor brazo); epsilon-greedy termina con 169.2, casi el doble (lo descubre explorando)"
   }
  },
  "application": "El dilema exploración-explotación no es exclusivo de máquinas tragamonedas: es el mismo problema de fondo que enfrenta Netflix decidiendo si recomendarte tu género favorito de siempre (explotar lo que sabe que te gusta) o algo nuevo que podría gustarte aún más (explorar); o un ensayo clínico decidiendo si seguir dando el tratamiento que mejor resultado dio hasta ahora, o probar uno experimental que podría ser mejor todavía. Cualquier sistema que aprende actuando — no solo observando — tarde o temprano se topa con esta misma tensión, y ε-greedy es la solución más simple que existe para resolverla (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.2)."
 },
 {
  "name": "Refuerzo · Bandido multi-brazo y ε-greedy — pregunta 4",
  "theory": "Imaginate 3 máquinas tragamonedas distintas, cada una con una probabilidad de pago distinta que NO conocés de antemano — tenés que ir probando para descubrir cuál conviene. Si actuás <b>greedy</b> (\"codicioso\": siempre elegís la máquina que hasta ahora te dio mejor resultado), corrés un riesgo real: si por pura mala suerte la MEJOR máquina te dio un resultado malo en tu primer intento, la vas a descartar y nunca más la vas a volver a probar — quedás \"pegado\" explotando una máquina mediocre para siempre.<br><br>En el código, esto pasa literalmente: la estrategia greedy (ε=0) elige el brazo 2 (el mejor en realidad) exactamente 0 de 80 veces, terminando con una recompensa total de solo ≈85,0. La estrategia <b>ε-greedy</b> (con ε=0,1: el 10% de las veces elegís un brazo al azar en vez del \"mejor conocido\") sí termina descubriendo que el brazo 2 es el mejor, eligiéndolo 69 de 80 veces, y consigue casi el DOBLE de recompensa total: ≈169,2. Ese 10% de \"probar algo distinto\" es lo que evita quedarse pegado en una mala decisión temprana.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.11.2, Algoritmo 11.1): el valor estimado de una acción se actualiza como $Q(a) \\leftarrow Q(a) + \\frac{r(a) - Q(a)}{N(a)}$, y la política ε-greedy elige $\\arg\\max_a Q(a)$ con probabilidad $1-\\varepsilon$, o una acción al azar con probabilidad $\\varepsilon$.",
  "code": "# Bandido multi-brazo y el dilema exploracion vs explotacion (Kelleher,\n# Sec 11.2, Algoritmo 11.1: e-greedy). Formula EXACTA del libro para\n# actualizar el valor estimado: Q(a) = Q(a) + (r(a) - Q(a)) / N(a)\n# (n_pasos=80: mantiene la traza del depurador dentro del limite de pasos\n# de esta app, sin cambiar el algoritmo del libro).\nimport numpy as np\n\nverdaderas_medias = [1.0, 1.5, 2.0]  # el brazo 2 es el MEJOR en realidad\nn_pasos = 80\n\ndef simular(epsilon, seed):\n    rng = np.random.default_rng(seed)\n    Q = [0.0, 0.0, 0.0]; N = [0, 0, 0]\n    recompensa_total = 0.0; elegido_optimo = 0\n    for t in range(n_pasos):\n        if rng.random() < epsilon:\n            a = rng.integers(0, 3)          # explorar: brazo al azar\n        else:\n            a = int(np.argmax(Q))            # explotar: el mejor conocido\n        r = rng.normal(verdaderas_medias[a], 1.0)\n        N[a] += 1\n        Q[a] = Q[a] + (r - Q[a]) / N[a]      # formula del Algoritmo 11.1\n        recompensa_total += r\n        if a == 2: elegido_optimo += 1\n    return Q, N, recompensa_total, elegido_optimo\n\nQg, Ng, Rg, Og = simular(epsilon=0.0, seed=15)   # GREEDY puro\nQe, Ne, Re, Oe = simular(epsilon=0.1, seed=15)   # EPSILON-GREEDY\n\nprint(\"GREEDY (epsilon=0):     Q estimado=\", [round(v,2) for v in Qg])\nprint(\"  veces elegido cada brazo:\", Ng, \" recompensa total:\", round(Rg,1))\nprint(\"  veces que eligio el brazo OPTIMO (2):\", Og, \"/\", n_pasos)\nprint(\"\\nEPSILON-GREEDY (e=0.1): Q estimado=\", [round(v,2) for v in Qe])\nprint(\"  veces elegido cada brazo:\", Ne, \" recompensa total:\", round(Re,1))\nprint(\"  veces que eligio el brazo OPTIMO (2):\", Oe, \"/\", n_pasos)",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Greedy · recompensa total",
     "ε-greedy · recompensa total"
    ],
    "values": [
     85.0,
     169.2
    ],
    "unit": "",
    "aria": "La estrategia greedy termina con recompensa total 85.0 (nunca descubre el mejor brazo); epsilon-greedy termina con 169.2, casi el doble (lo descubre explorando)"
   }
  },
  "application": "El dilema exploración-explotación no es exclusivo de máquinas tragamonedas: es el mismo problema de fondo que enfrenta Netflix decidiendo si recomendarte tu género favorito de siempre (explotar lo que sabe que te gusta) o algo nuevo que podría gustarte aún más (explorar); o un ensayo clínico decidiendo si seguir dando el tratamiento que mejor resultado dio hasta ahora, o probar uno experimental que podría ser mejor todavía. Cualquier sistema que aprende actuando — no solo observando — tarde o temprano se topa con esta misma tensión, y ε-greedy es la solución más simple que existe para resolverla (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.2)."
 },
 {
  "name": "Refuerzo · Proceso de Markov: estados y transiciones",
  "theory": "Un Proceso de Markov describe un mundo con memoria muy corta: lo único que importa para saber qué pasa DESPUÉS es dónde estás AHORA y qué acción tomás — no importa cómo llegaste ahí. Es como un juego de la oca: tu próxima casilla depende solo de en qué casilla estás parado y qué tirás en el dado, nunca de qué camino recorriste antes para llegar ahí.<br><br>En el código, un robot tiene 3 estados posibles (caído, de pie, moviéndose) y 2 acciones (ir lento o rápido). Las probabilidades de transición son datos conocidos y fijos: si está caído y va lento, tiene 3/5 de probabilidad de seguir caído y 2/5 de pararse — es la ÚNICA forma de levantarse (si va rápido estando caído, se queda caído siempre). Si está de pie y va rápido, tiene 3/5 de empezar a moverse pero 2/5 de caerse. Con una política fija (ir lento solo cuando está caído, rápido el resto del tiempo), se puede simular una trayectoria completa paso a paso, siguiendo exactamente esas probabilidades.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.11.4): un proceso de Markov se define por un conjunto de estados $S$, un conjunto de acciones $A$, y un modelo de transición $T: S \\times A \\times S \\rightarrow \\mathbb{R}$, donde $P(s_{t+1}|s_t, a_t)$ depende ÚNICAMENTE del estado y la acción actuales — nunca de la historia completa anterior (la \"propiedad de Markov\").",
  "code": "# Proceso de Markov (Kelleher, Sec 11.3-11.4): el ejemplo del robot del\n# libro. Estados={caido, de_pie, moviendose}, acciones={lento, rapido},\n# con matrices de transicion de probabilidad REALES del texto.\nimport numpy as np\n\nestados = ['caido', 'de_pie', 'moviendose']\n\n# P(s' | s, accion=lento) -- filas = estado actual, columnas = estado siguiente\nP_lento = np.array([\n    [3/5, 2/5, 0],   # caido + lento -> 3/5 sigue caido, 2/5 se para\n    [0,   0,   1],   # de_pie + lento -> siempre empieza a moverse\n    [0,   0,   1],   # moviendose + lento -> sigue moviendose\n])\n# P(s' | s, accion=rapido)\nP_rapido = np.array([\n    [1,   0,   0],   # caido + rapido -> se queda caido (no puede pararse rapido)\n    [0,   2/5, 3/5], # de_pie + rapido -> 3/5 se mueve, 2/5 sigue de pie\n    [0,   1/5, 4/5], # moviendose + rapido -> 4/5 sigue, 1/5 se cae\n])\n\nprint(\"cada fila de P_lento suma 1?\", np.allclose(P_lento.sum(axis=1), 1))\nprint(\"cada fila de P_rapido suma 1?\", np.allclose(P_rapido.sum(axis=1), 1))\n\nrng = np.random.default_rng(7)\ndef politica_optima(s):\n    return 'lento' if s == 0 else 'rapido'   # unica forma de levantarse: ir lento\n\ns = 0  # empieza 'caido'\ntrayectoria = [estados[s]]\nfor _ in range(10):\n    a = politica_optima(s)\n    P = P_lento if a == 'lento' else P_rapido\n    s = rng.choice(3, p=P[s])\n    trayectoria.append(estados[s])\n\nprint(\"\\ntrayectoria de 10 pasos siguiendo la politica (lento si caido, rapido si no):\")\nprint(' -> '.join(trayectoria))",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 3,
    "cols": 3,
    "barMode": false,
    "rowLabels": [
     "caído",
     "de_pie",
     "moviendose"
    ],
    "values": [
     [
      0.6,
      0.4,
      0
     ],
     [
      0,
      0,
      1
     ],
     [
      0,
      0,
      1
     ]
    ],
    "cellText": [
     [
      "3/5",
      "2/5",
      "0"
     ],
     [
      "0",
      "0",
      "1"
     ],
     [
      "0",
      "0",
      "1"
     ]
    ],
    "min": 0,
    "max": 1,
    "aria": "Matriz de transicion P(s'|s, accion=lento): cada fila suma 1 (probabilidad total)"
   }
  },
  "application": "La formalización de Procesos de Markov (y su extensión, los Procesos de Decisión de Markov o MDP) es el lenguaje matemático estándar detrás de prácticamente todo el aprendizaje por refuerzo moderno: desde robots que aprenden a caminar, hasta AlphaGo jugando Go, hasta sistemas de recomendación que deciden qué mostrarte a continuación. Cualquier problema donde un agente toma decisiones secuenciales en un entorno con incertidumbre — y donde el futuro depende del estado actual, no de todo el historial — se puede modelar como un proceso de Markov (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.3-11.4).",
  "codeAnatomy": {
   "title": "Simulando una trayectoria bajo la política",
   "caption": "En cada paso, la acción elegida decide qué matriz de transición se usa",
   "lines": [
    "a = politica_optima(s)",
    "P = P_lento if a == 'lento' else P_rapido",
    "s = rng.choice(3, p=P[s])"
   ],
   "annotations": [
    {
     "line": 0,
     "text": "politica_optima(s)",
     "label": "Política fija",
     "desc": "(lento si caído, rápido si no)",
     "side": "top"
    },
    {
     "line": 1,
     "text": "P_lento if a == 'lento' else P_rapido",
     "label": "Elige la matriz",
     "desc": "(según la acción tomada)",
     "side": "top"
    },
    {
     "line": 2,
     "text": "P[s]",
     "label": "Fila actual",
     "desc": "(probabilidades desde el estado en el que está)",
     "side": "bottom"
    },
    {
     "line": 2,
     "text": "rng.choice(3, p=P[s])",
     "label": "Sortea el siguiente estado",
     "desc": "(según esas probabilidades, no siempre el mismo resultado)",
     "side": "bottom"
    }
   ]
  }
 },
 {
  "name": "Refuerzo · Proceso de Markov: estados y transiciones — pregunta 2",
  "theory": "Un Proceso de Markov describe un mundo con memoria muy corta: lo único que importa para saber qué pasa DESPUÉS es dónde estás AHORA y qué acción tomás — no importa cómo llegaste ahí. Es como un juego de la oca: tu próxima casilla depende solo de en qué casilla estás parado y qué tirás en el dado, nunca de qué camino recorriste antes para llegar ahí.<br><br>En el código, un robot tiene 3 estados posibles (caído, de pie, moviéndose) y 2 acciones (ir lento o rápido). Las probabilidades de transición son datos conocidos y fijos: si está caído y va lento, tiene 3/5 de probabilidad de seguir caído y 2/5 de pararse — es la ÚNICA forma de levantarse (si va rápido estando caído, se queda caído siempre). Si está de pie y va rápido, tiene 3/5 de empezar a moverse pero 2/5 de caerse. Con una política fija (ir lento solo cuando está caído, rápido el resto del tiempo), se puede simular una trayectoria completa paso a paso, siguiendo exactamente esas probabilidades.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.11.4): un proceso de Markov se define por un conjunto de estados $S$, un conjunto de acciones $A$, y un modelo de transición $T: S \\times A \\times S \\rightarrow \\mathbb{R}$, donde $P(s_{t+1}|s_t, a_t)$ depende ÚNICAMENTE del estado y la acción actuales — nunca de la historia completa anterior (la \"propiedad de Markov\").",
  "code": "# Proceso de Markov (Kelleher, Sec 11.3-11.4): el ejemplo del robot del\n# libro. Estados={caido, de_pie, moviendose}, acciones={lento, rapido},\n# con matrices de transicion de probabilidad REALES del texto.\nimport numpy as np\n\nestados = ['caido', 'de_pie', 'moviendose']\n\n# P(s' | s, accion=lento) -- filas = estado actual, columnas = estado siguiente\nP_lento = np.array([\n    [3/5, 2/5, 0],   # caido + lento -> 3/5 sigue caido, 2/5 se para\n    [0,   0,   1],   # de_pie + lento -> siempre empieza a moverse\n    [0,   0,   1],   # moviendose + lento -> sigue moviendose\n])\n# P(s' | s, accion=rapido)\nP_rapido = np.array([\n    [1,   0,   0],   # caido + rapido -> se queda caido (no puede pararse rapido)\n    [0,   2/5, 3/5], # de_pie + rapido -> 3/5 se mueve, 2/5 sigue de pie\n    [0,   1/5, 4/5], # moviendose + rapido -> 4/5 sigue, 1/5 se cae\n])\n\nprint(\"cada fila de P_lento suma 1?\", np.allclose(P_lento.sum(axis=1), 1))\nprint(\"cada fila de P_rapido suma 1?\", np.allclose(P_rapido.sum(axis=1), 1))\n\nrng = np.random.default_rng(7)\ndef politica_optima(s):\n    return 'lento' if s == 0 else 'rapido'   # unica forma de levantarse: ir lento\n\ns = 0  # empieza 'caido'\ntrayectoria = [estados[s]]\nfor _ in range(10):\n    a = politica_optima(s)\n    P = P_lento if a == 'lento' else P_rapido\n    s = rng.choice(3, p=P[s])\n    trayectoria.append(estados[s])\n\nprint(\"\\ntrayectoria de 10 pasos siguiendo la politica (lento si caido, rapido si no):\")\nprint(' -> '.join(trayectoria))",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 3,
    "cols": 3,
    "barMode": false,
    "rowLabels": [
     "caído",
     "de_pie",
     "moviendose"
    ],
    "values": [
     [
      0.6,
      0.4,
      0
     ],
     [
      0,
      0,
      1
     ],
     [
      0,
      0,
      1
     ]
    ],
    "cellText": [
     [
      "3/5",
      "2/5",
      "0"
     ],
     [
      "0",
      "0",
      "1"
     ],
     [
      "0",
      "0",
      "1"
     ]
    ],
    "min": 0,
    "max": 1,
    "aria": "Matriz de transicion P(s'|s, accion=lento): cada fila suma 1 (probabilidad total)"
   }
  },
  "application": "La formalización de Procesos de Markov (y su extensión, los Procesos de Decisión de Markov o MDP) es el lenguaje matemático estándar detrás de prácticamente todo el aprendizaje por refuerzo moderno: desde robots que aprenden a caminar, hasta AlphaGo jugando Go, hasta sistemas de recomendación que deciden qué mostrarte a continuación. Cualquier problema donde un agente toma decisiones secuenciales en un entorno con incertidumbre — y donde el futuro depende del estado actual, no de todo el historial — se puede modelar como un proceso de Markov (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.3-11.4)."
 },
 {
  "name": "Refuerzo · Proceso de Markov: estados y transiciones — pregunta 3",
  "theory": "Un Proceso de Markov describe un mundo con memoria muy corta: lo único que importa para saber qué pasa DESPUÉS es dónde estás AHORA y qué acción tomás — no importa cómo llegaste ahí. Es como un juego de la oca: tu próxima casilla depende solo de en qué casilla estás parado y qué tirás en el dado, nunca de qué camino recorriste antes para llegar ahí.<br><br>En el código, un robot tiene 3 estados posibles (caído, de pie, moviéndose) y 2 acciones (ir lento o rápido). Las probabilidades de transición son datos conocidos y fijos: si está caído y va lento, tiene 3/5 de probabilidad de seguir caído y 2/5 de pararse — es la ÚNICA forma de levantarse (si va rápido estando caído, se queda caído siempre). Si está de pie y va rápido, tiene 3/5 de empezar a moverse pero 2/5 de caerse. Con una política fija (ir lento solo cuando está caído, rápido el resto del tiempo), se puede simular una trayectoria completa paso a paso, siguiendo exactamente esas probabilidades.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.11.4): un proceso de Markov se define por un conjunto de estados $S$, un conjunto de acciones $A$, y un modelo de transición $T: S \\times A \\times S \\rightarrow \\mathbb{R}$, donde $P(s_{t+1}|s_t, a_t)$ depende ÚNICAMENTE del estado y la acción actuales — nunca de la historia completa anterior (la \"propiedad de Markov\").",
  "code": "# Proceso de Markov (Kelleher, Sec 11.3-11.4): el ejemplo del robot del\n# libro. Estados={caido, de_pie, moviendose}, acciones={lento, rapido},\n# con matrices de transicion de probabilidad REALES del texto.\nimport numpy as np\n\nestados = ['caido', 'de_pie', 'moviendose']\n\n# P(s' | s, accion=lento) -- filas = estado actual, columnas = estado siguiente\nP_lento = np.array([\n    [3/5, 2/5, 0],   # caido + lento -> 3/5 sigue caido, 2/5 se para\n    [0,   0,   1],   # de_pie + lento -> siempre empieza a moverse\n    [0,   0,   1],   # moviendose + lento -> sigue moviendose\n])\n# P(s' | s, accion=rapido)\nP_rapido = np.array([\n    [1,   0,   0],   # caido + rapido -> se queda caido (no puede pararse rapido)\n    [0,   2/5, 3/5], # de_pie + rapido -> 3/5 se mueve, 2/5 sigue de pie\n    [0,   1/5, 4/5], # moviendose + rapido -> 4/5 sigue, 1/5 se cae\n])\n\nprint(\"cada fila de P_lento suma 1?\", np.allclose(P_lento.sum(axis=1), 1))\nprint(\"cada fila de P_rapido suma 1?\", np.allclose(P_rapido.sum(axis=1), 1))\n\nrng = np.random.default_rng(7)\ndef politica_optima(s):\n    return 'lento' if s == 0 else 'rapido'   # unica forma de levantarse: ir lento\n\ns = 0  # empieza 'caido'\ntrayectoria = [estados[s]]\nfor _ in range(10):\n    a = politica_optima(s)\n    P = P_lento if a == 'lento' else P_rapido\n    s = rng.choice(3, p=P[s])\n    trayectoria.append(estados[s])\n\nprint(\"\\ntrayectoria de 10 pasos siguiendo la politica (lento si caido, rapido si no):\")\nprint(' -> '.join(trayectoria))",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 3,
    "cols": 3,
    "barMode": false,
    "rowLabels": [
     "caído",
     "de_pie",
     "moviendose"
    ],
    "values": [
     [
      0.6,
      0.4,
      0
     ],
     [
      0,
      0,
      1
     ],
     [
      0,
      0,
      1
     ]
    ],
    "cellText": [
     [
      "3/5",
      "2/5",
      "0"
     ],
     [
      "0",
      "0",
      "1"
     ],
     [
      "0",
      "0",
      "1"
     ]
    ],
    "min": 0,
    "max": 1,
    "aria": "Matriz de transicion P(s'|s, accion=lento): cada fila suma 1 (probabilidad total)"
   }
  },
  "application": "La formalización de Procesos de Markov (y su extensión, los Procesos de Decisión de Markov o MDP) es el lenguaje matemático estándar detrás de prácticamente todo el aprendizaje por refuerzo moderno: desde robots que aprenden a caminar, hasta AlphaGo jugando Go, hasta sistemas de recomendación que deciden qué mostrarte a continuación. Cualquier problema donde un agente toma decisiones secuenciales en un entorno con incertidumbre — y donde el futuro depende del estado actual, no de todo el historial — se puede modelar como un proceso de Markov (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.3-11.4)."
 },
 {
  "name": "Refuerzo · Proceso de Markov: estados y transiciones — pregunta 4",
  "theory": "Un Proceso de Markov describe un mundo con memoria muy corta: lo único que importa para saber qué pasa DESPUÉS es dónde estás AHORA y qué acción tomás — no importa cómo llegaste ahí. Es como un juego de la oca: tu próxima casilla depende solo de en qué casilla estás parado y qué tirás en el dado, nunca de qué camino recorriste antes para llegar ahí.<br><br>En el código, un robot tiene 3 estados posibles (caído, de pie, moviéndose) y 2 acciones (ir lento o rápido). Las probabilidades de transición son datos conocidos y fijos: si está caído y va lento, tiene 3/5 de probabilidad de seguir caído y 2/5 de pararse — es la ÚNICA forma de levantarse (si va rápido estando caído, se queda caído siempre). Si está de pie y va rápido, tiene 3/5 de empezar a moverse pero 2/5 de caerse. Con una política fija (ir lento solo cuando está caído, rápido el resto del tiempo), se puede simular una trayectoria completa paso a paso, siguiendo exactamente esas probabilidades.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.11.4): un proceso de Markov se define por un conjunto de estados $S$, un conjunto de acciones $A$, y un modelo de transición $T: S \\times A \\times S \\rightarrow \\mathbb{R}$, donde $P(s_{t+1}|s_t, a_t)$ depende ÚNICAMENTE del estado y la acción actuales — nunca de la historia completa anterior (la \"propiedad de Markov\").",
  "code": "# Proceso de Markov (Kelleher, Sec 11.3-11.4): el ejemplo del robot del\n# libro. Estados={caido, de_pie, moviendose}, acciones={lento, rapido},\n# con matrices de transicion de probabilidad REALES del texto.\nimport numpy as np\n\nestados = ['caido', 'de_pie', 'moviendose']\n\n# P(s' | s, accion=lento) -- filas = estado actual, columnas = estado siguiente\nP_lento = np.array([\n    [3/5, 2/5, 0],   # caido + lento -> 3/5 sigue caido, 2/5 se para\n    [0,   0,   1],   # de_pie + lento -> siempre empieza a moverse\n    [0,   0,   1],   # moviendose + lento -> sigue moviendose\n])\n# P(s' | s, accion=rapido)\nP_rapido = np.array([\n    [1,   0,   0],   # caido + rapido -> se queda caido (no puede pararse rapido)\n    [0,   2/5, 3/5], # de_pie + rapido -> 3/5 se mueve, 2/5 sigue de pie\n    [0,   1/5, 4/5], # moviendose + rapido -> 4/5 sigue, 1/5 se cae\n])\n\nprint(\"cada fila de P_lento suma 1?\", np.allclose(P_lento.sum(axis=1), 1))\nprint(\"cada fila de P_rapido suma 1?\", np.allclose(P_rapido.sum(axis=1), 1))\n\nrng = np.random.default_rng(7)\ndef politica_optima(s):\n    return 'lento' if s == 0 else 'rapido'   # unica forma de levantarse: ir lento\n\ns = 0  # empieza 'caido'\ntrayectoria = [estados[s]]\nfor _ in range(10):\n    a = politica_optima(s)\n    P = P_lento if a == 'lento' else P_rapido\n    s = rng.choice(3, p=P[s])\n    trayectoria.append(estados[s])\n\nprint(\"\\ntrayectoria de 10 pasos siguiendo la politica (lento si caido, rapido si no):\")\nprint(' -> '.join(trayectoria))",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 3,
    "cols": 3,
    "barMode": false,
    "rowLabels": [
     "caído",
     "de_pie",
     "moviendose"
    ],
    "values": [
     [
      0.6,
      0.4,
      0
     ],
     [
      0,
      0,
      1
     ],
     [
      0,
      0,
      1
     ]
    ],
    "cellText": [
     [
      "3/5",
      "2/5",
      "0"
     ],
     [
      "0",
      "0",
      "1"
     ],
     [
      "0",
      "0",
      "1"
     ]
    ],
    "min": 0,
    "max": 1,
    "aria": "Matriz de transicion P(s'|s, accion=lento): cada fila suma 1 (probabilidad total)"
   }
  },
  "application": "La formalización de Procesos de Markov (y su extensión, los Procesos de Decisión de Markov o MDP) es el lenguaje matemático estándar detrás de prácticamente todo el aprendizaje por refuerzo moderno: desde robots que aprenden a caminar, hasta AlphaGo jugando Go, hasta sistemas de recomendación que deciden qué mostrarte a continuación. Cualquier problema donde un agente toma decisiones secuenciales en un entorno con incertidumbre — y donde el futuro depende del estado actual, no de todo el historial — se puede modelar como un proceso de Markov (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.3-11.4)."
 },
 {
  "name": "Refuerzo · Función de valor V(s) y el factor de descuento γ",
  "theory": "La función de valor V(s) responde una pregunta muy concreta: \"¿qué tan buena es esta posición, si sigo mi estrategia desde acá hasta el final?\". No es el premio de ESTE paso, es la suma de TODOS los premios futuros que vas a ir juntando desde ahí. El factor de descuento γ (gamma) decide cuánto te importa el futuro lejano: con γ=0 sos completamente miope, solo te importa el premio inmediato del próximo paso; con γ=1 sos completamente \"de largo plazo\", cada paso futuro pesa exactamente igual que el de ahora, por lejano que esté.<br><br>En el código, un corredor de 4 casillas (0→1→2→3=meta) da -1 de recompensa en cada paso hasta llegar. Con γ=0, V(estado 0) da exactamente -1 (solo mira el paso inmediato). Con γ=1, da exactamente -3 (la suma sin descontar de los 3 pasos reales que faltan hasta la meta). Con γ=0,9 (un punto intermedio realista) da -2,71 — ni tan ciego al futuro como γ=0, ni tan \"literal\" como γ=1. Y mirando cada estado por separado con γ=0,9: el valor va SUBIENDO (mejorando, acercándose a 0) a medida que el estado está más cerca de la meta — V(0)=-2,71, V(1)=-1,9, V(2)=-1,0, V(3)=0 — exactamente lo que uno esperaría de una buena función de valor.<br><br>📐 <b>Referencia formal</b> (Kelleher, Ec.11.12-11.13): $V^h_\\pi(s) = R(s,\\pi(s)) + \\gamma \\sum_{s'} T(s,\\pi(s),s') V^{h-1}_\\pi(s')$, y para horizonte infinito, $V_\\pi(s) = \\mathbb{E}_\\pi[R_0 + \\gamma R_1 + \\gamma^2 R_2 + \\cdots \\mid s_0=s]$.",
  "code": "# Funcion de valor V(s) y el factor de descuento gamma (Kelleher, Sec 11.6.3).\n# Corredor de 4 estados: 0,1,2 son intermedios, 3 es la meta. Recompensa\n# -1 en cada paso hasta llegar (igual que el laberinto del libro: 'we lose\n# a point' en cada paso). Formula recursiva EXACTA del libro (Ec. 11.12).\nsiguiente = {0: 1, 1: 2, 2: 3, 3: 3}\nrecompensa = {0: -1, 1: -1, 2: -1, 3: 0}\n\ndef V_horizonte(s, h, gamma):\n    if h == 0:\n        return 0.0\n    return recompensa[s] + gamma * V_horizonte(siguiente[s], h - 1, gamma)\n\nprint(\"Vision miope (gamma=0) vs vision de largo plazo (gamma cercano a 1):\")\nfor gamma in [0.0, 0.5, 0.9, 1.0]:\n    v0 = V_horizonte(0, 10, gamma)\n    print(f\"  gamma={gamma}: V(estado 0) con horizonte 10 pasos = {round(v0, 3)}\")\n\nprint(\"\\nvalor de CADA estado del corredor con gamma=0.9 (horizonte largo=20):\")\nfor s in range(4):\n    print(f\"  V(estado {s}) = {round(V_horizonte(s, 20, 0.9), 3)}\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "V(estado 0)",
     "V(estado 1)",
     "V(estado 2)",
     "V(estado 3, meta)"
    ],
    "values": [
     -2.71,
     -1.9,
     -1.0,
     0.0
    ],
    "unit": "",
    "aria": "El valor de cada estado sube (se acerca a 0) a medida que el estado esta mas cerca de la meta, con gamma=0.9"
   }
  },
  "application": "El factor de descuento γ no es un detalle técnico menor: en la práctica, es literalmente la decisión de cuánto le importa a un agente el futuro. Un robot de reparto con γ bajo optimizaría solo la entrega inmediata sin importarle quedar mal posicionado para la siguiente; un sistema de trading con γ cercano a 1 sacrifica ganancias inmediatas si eso mejora la posición a largo plazo. La misma matemática de V(s) con descuento es la base de casi todos los algoritmos modernos de aprendizaje por refuerzo (Q-learning, Deep Q-Networks, y los agentes que juegan Atari o Go que vas a ver en el Cap.12 del libro), que en el fondo intentan estimar esta función de valor sin conocer de antemano las probabilidades de transición reales del entorno (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.6).",
  "codeAnatomy": {
   "title": "def V_horizonte(s, h, gamma):",
   "caption": "La función de valor recursiva — recompensa inmediata + el resto del futuro, descontado",
   "lines": [
    "def V_horizonte(s, h, gamma):",
    "    if h == 0:",
    "        return 0.0",
    "    return recompensa[s] + gamma * V_horizonte(siguiente[s], h - 1, gamma)"
   ],
   "annotations": [
    {
     "line": 0,
     "text": "def V_horizonte(s, h, gamma)",
     "label": "Función recursiva",
     "desc": "(estado, pasos que quedan, factor de descuento)",
     "side": "top"
    },
    {
     "line": 1,
     "text": "h == 0",
     "label": "Caso base",
     "desc": "(sin pasos restantes, no queda nada más que sumar)",
     "side": "top"
    },
    {
     "line": 3,
     "text": "recompensa[s]",
     "label": "Premio inmediato",
     "desc": "(de este paso, sin descuento)",
     "side": "bottom"
    },
    {
     "line": 3,
     "text": "gamma * V_horizonte(siguiente[s], h - 1, gamma)",
     "label": "Resto del futuro, descontado",
     "desc": "(un paso menos, multiplicado por gamma)",
     "side": "bottom"
    }
   ]
  }
 },
 {
  "name": "Refuerzo · Función de valor V(s) y el factor de descuento γ — pregunta 2",
  "theory": "La función de valor V(s) responde una pregunta muy concreta: \"¿qué tan buena es esta posición, si sigo mi estrategia desde acá hasta el final?\". No es el premio de ESTE paso, es la suma de TODOS los premios futuros que vas a ir juntando desde ahí. El factor de descuento γ (gamma) decide cuánto te importa el futuro lejano: con γ=0 sos completamente miope, solo te importa el premio inmediato del próximo paso; con γ=1 sos completamente \"de largo plazo\", cada paso futuro pesa exactamente igual que el de ahora, por lejano que esté.<br><br>En el código, un corredor de 4 casillas (0→1→2→3=meta) da -1 de recompensa en cada paso hasta llegar. Con γ=0, V(estado 0) da exactamente -1 (solo mira el paso inmediato). Con γ=1, da exactamente -3 (la suma sin descontar de los 3 pasos reales que faltan hasta la meta). Con γ=0,9 (un punto intermedio realista) da -2,71 — ni tan ciego al futuro como γ=0, ni tan \"literal\" como γ=1. Y mirando cada estado por separado con γ=0,9: el valor va SUBIENDO (mejorando, acercándose a 0) a medida que el estado está más cerca de la meta — V(0)=-2,71, V(1)=-1,9, V(2)=-1,0, V(3)=0 — exactamente lo que uno esperaría de una buena función de valor.<br><br>📐 <b>Referencia formal</b> (Kelleher, Ec.11.12-11.13): $V^h_\\pi(s) = R(s,\\pi(s)) + \\gamma \\sum_{s'} T(s,\\pi(s),s') V^{h-1}_\\pi(s')$, y para horizonte infinito, $V_\\pi(s) = \\mathbb{E}_\\pi[R_0 + \\gamma R_1 + \\gamma^2 R_2 + \\cdots \\mid s_0=s]$.",
  "code": "# Funcion de valor V(s) y el factor de descuento gamma (Kelleher, Sec 11.6.3).\n# Corredor de 4 estados: 0,1,2 son intermedios, 3 es la meta. Recompensa\n# -1 en cada paso hasta llegar (igual que el laberinto del libro: 'we lose\n# a point' en cada paso). Formula recursiva EXACTA del libro (Ec. 11.12).\nsiguiente = {0: 1, 1: 2, 2: 3, 3: 3}\nrecompensa = {0: -1, 1: -1, 2: -1, 3: 0}\n\ndef V_horizonte(s, h, gamma):\n    if h == 0:\n        return 0.0\n    return recompensa[s] + gamma * V_horizonte(siguiente[s], h - 1, gamma)\n\nprint(\"Vision miope (gamma=0) vs vision de largo plazo (gamma cercano a 1):\")\nfor gamma in [0.0, 0.5, 0.9, 1.0]:\n    v0 = V_horizonte(0, 10, gamma)\n    print(f\"  gamma={gamma}: V(estado 0) con horizonte 10 pasos = {round(v0, 3)}\")\n\nprint(\"\\nvalor de CADA estado del corredor con gamma=0.9 (horizonte largo=20):\")\nfor s in range(4):\n    print(f\"  V(estado {s}) = {round(V_horizonte(s, 20, 0.9), 3)}\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "V(estado 0)",
     "V(estado 1)",
     "V(estado 2)",
     "V(estado 3, meta)"
    ],
    "values": [
     -2.71,
     -1.9,
     -1.0,
     0.0
    ],
    "unit": "",
    "aria": "El valor de cada estado sube (se acerca a 0) a medida que el estado esta mas cerca de la meta, con gamma=0.9"
   }
  },
  "application": "El factor de descuento γ no es un detalle técnico menor: en la práctica, es literalmente la decisión de cuánto le importa a un agente el futuro. Un robot de reparto con γ bajo optimizaría solo la entrega inmediata sin importarle quedar mal posicionado para la siguiente; un sistema de trading con γ cercano a 1 sacrifica ganancias inmediatas si eso mejora la posición a largo plazo. La misma matemática de V(s) con descuento es la base de casi todos los algoritmos modernos de aprendizaje por refuerzo (Q-learning, Deep Q-Networks, y los agentes que juegan Atari o Go que vas a ver en el Cap.12 del libro), que en el fondo intentan estimar esta función de valor sin conocer de antemano las probabilidades de transición reales del entorno (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.6)."
 },
 {
  "name": "Refuerzo · Función de valor V(s) y el factor de descuento γ — pregunta 3",
  "theory": "La función de valor V(s) responde una pregunta muy concreta: \"¿qué tan buena es esta posición, si sigo mi estrategia desde acá hasta el final?\". No es el premio de ESTE paso, es la suma de TODOS los premios futuros que vas a ir juntando desde ahí. El factor de descuento γ (gamma) decide cuánto te importa el futuro lejano: con γ=0 sos completamente miope, solo te importa el premio inmediato del próximo paso; con γ=1 sos completamente \"de largo plazo\", cada paso futuro pesa exactamente igual que el de ahora, por lejano que esté.<br><br>En el código, un corredor de 4 casillas (0→1→2→3=meta) da -1 de recompensa en cada paso hasta llegar. Con γ=0, V(estado 0) da exactamente -1 (solo mira el paso inmediato). Con γ=1, da exactamente -3 (la suma sin descontar de los 3 pasos reales que faltan hasta la meta). Con γ=0,9 (un punto intermedio realista) da -2,71 — ni tan ciego al futuro como γ=0, ni tan \"literal\" como γ=1. Y mirando cada estado por separado con γ=0,9: el valor va SUBIENDO (mejorando, acercándose a 0) a medida que el estado está más cerca de la meta — V(0)=-2,71, V(1)=-1,9, V(2)=-1,0, V(3)=0 — exactamente lo que uno esperaría de una buena función de valor.<br><br>📐 <b>Referencia formal</b> (Kelleher, Ec.11.12-11.13): $V^h_\\pi(s) = R(s,\\pi(s)) + \\gamma \\sum_{s'} T(s,\\pi(s),s') V^{h-1}_\\pi(s')$, y para horizonte infinito, $V_\\pi(s) = \\mathbb{E}_\\pi[R_0 + \\gamma R_1 + \\gamma^2 R_2 + \\cdots \\mid s_0=s]$.",
  "code": "# Funcion de valor V(s) y el factor de descuento gamma (Kelleher, Sec 11.6.3).\n# Corredor de 4 estados: 0,1,2 son intermedios, 3 es la meta. Recompensa\n# -1 en cada paso hasta llegar (igual que el laberinto del libro: 'we lose\n# a point' en cada paso). Formula recursiva EXACTA del libro (Ec. 11.12).\nsiguiente = {0: 1, 1: 2, 2: 3, 3: 3}\nrecompensa = {0: -1, 1: -1, 2: -1, 3: 0}\n\ndef V_horizonte(s, h, gamma):\n    if h == 0:\n        return 0.0\n    return recompensa[s] + gamma * V_horizonte(siguiente[s], h - 1, gamma)\n\nprint(\"Vision miope (gamma=0) vs vision de largo plazo (gamma cercano a 1):\")\nfor gamma in [0.0, 0.5, 0.9, 1.0]:\n    v0 = V_horizonte(0, 10, gamma)\n    print(f\"  gamma={gamma}: V(estado 0) con horizonte 10 pasos = {round(v0, 3)}\")\n\nprint(\"\\nvalor de CADA estado del corredor con gamma=0.9 (horizonte largo=20):\")\nfor s in range(4):\n    print(f\"  V(estado {s}) = {round(V_horizonte(s, 20, 0.9), 3)}\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "V(estado 0)",
     "V(estado 1)",
     "V(estado 2)",
     "V(estado 3, meta)"
    ],
    "values": [
     -2.71,
     -1.9,
     -1.0,
     0.0
    ],
    "unit": "",
    "aria": "El valor de cada estado sube (se acerca a 0) a medida que el estado esta mas cerca de la meta, con gamma=0.9"
   }
  },
  "application": "El factor de descuento γ no es un detalle técnico menor: en la práctica, es literalmente la decisión de cuánto le importa a un agente el futuro. Un robot de reparto con γ bajo optimizaría solo la entrega inmediata sin importarle quedar mal posicionado para la siguiente; un sistema de trading con γ cercano a 1 sacrifica ganancias inmediatas si eso mejora la posición a largo plazo. La misma matemática de V(s) con descuento es la base de casi todos los algoritmos modernos de aprendizaje por refuerzo (Q-learning, Deep Q-Networks, y los agentes que juegan Atari o Go que vas a ver en el Cap.12 del libro), que en el fondo intentan estimar esta función de valor sin conocer de antemano las probabilidades de transición reales del entorno (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.6)."
 },
 {
  "name": "Refuerzo · Función de valor V(s) y el factor de descuento γ — pregunta 4",
  "theory": "La función de valor V(s) responde una pregunta muy concreta: \"¿qué tan buena es esta posición, si sigo mi estrategia desde acá hasta el final?\". No es el premio de ESTE paso, es la suma de TODOS los premios futuros que vas a ir juntando desde ahí. El factor de descuento γ (gamma) decide cuánto te importa el futuro lejano: con γ=0 sos completamente miope, solo te importa el premio inmediato del próximo paso; con γ=1 sos completamente \"de largo plazo\", cada paso futuro pesa exactamente igual que el de ahora, por lejano que esté.<br><br>En el código, un corredor de 4 casillas (0→1→2→3=meta) da -1 de recompensa en cada paso hasta llegar. Con γ=0, V(estado 0) da exactamente -1 (solo mira el paso inmediato). Con γ=1, da exactamente -3 (la suma sin descontar de los 3 pasos reales que faltan hasta la meta). Con γ=0,9 (un punto intermedio realista) da -2,71 — ni tan ciego al futuro como γ=0, ni tan \"literal\" como γ=1. Y mirando cada estado por separado con γ=0,9: el valor va SUBIENDO (mejorando, acercándose a 0) a medida que el estado está más cerca de la meta — V(0)=-2,71, V(1)=-1,9, V(2)=-1,0, V(3)=0 — exactamente lo que uno esperaría de una buena función de valor.<br><br>📐 <b>Referencia formal</b> (Kelleher, Ec.11.12-11.13): $V^h_\\pi(s) = R(s,\\pi(s)) + \\gamma \\sum_{s'} T(s,\\pi(s),s') V^{h-1}_\\pi(s')$, y para horizonte infinito, $V_\\pi(s) = \\mathbb{E}_\\pi[R_0 + \\gamma R_1 + \\gamma^2 R_2 + \\cdots \\mid s_0=s]$.",
  "code": "# Funcion de valor V(s) y el factor de descuento gamma (Kelleher, Sec 11.6.3).\n# Corredor de 4 estados: 0,1,2 son intermedios, 3 es la meta. Recompensa\n# -1 en cada paso hasta llegar (igual que el laberinto del libro: 'we lose\n# a point' en cada paso). Formula recursiva EXACTA del libro (Ec. 11.12).\nsiguiente = {0: 1, 1: 2, 2: 3, 3: 3}\nrecompensa = {0: -1, 1: -1, 2: -1, 3: 0}\n\ndef V_horizonte(s, h, gamma):\n    if h == 0:\n        return 0.0\n    return recompensa[s] + gamma * V_horizonte(siguiente[s], h - 1, gamma)\n\nprint(\"Vision miope (gamma=0) vs vision de largo plazo (gamma cercano a 1):\")\nfor gamma in [0.0, 0.5, 0.9, 1.0]:\n    v0 = V_horizonte(0, 10, gamma)\n    print(f\"  gamma={gamma}: V(estado 0) con horizonte 10 pasos = {round(v0, 3)}\")\n\nprint(\"\\nvalor de CADA estado del corredor con gamma=0.9 (horizonte largo=20):\")\nfor s in range(4):\n    print(f\"  V(estado {s}) = {round(V_horizonte(s, 20, 0.9), 3)}\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "V(estado 0)",
     "V(estado 1)",
     "V(estado 2)",
     "V(estado 3, meta)"
    ],
    "values": [
     -2.71,
     -1.9,
     -1.0,
     0.0
    ],
    "unit": "",
    "aria": "El valor de cada estado sube (se acerca a 0) a medida que el estado esta mas cerca de la meta, con gamma=0.9"
   }
  },
  "application": "El factor de descuento γ no es un detalle técnico menor: en la práctica, es literalmente la decisión de cuánto le importa a un agente el futuro. Un robot de reparto con γ bajo optimizaría solo la entrega inmediata sin importarle quedar mal posicionado para la siguiente; un sistema de trading con γ cercano a 1 sacrifica ganancias inmediatas si eso mejora la posición a largo plazo. La misma matemática de V(s) con descuento es la base de casi todos los algoritmos modernos de aprendizaje por refuerzo (Q-learning, Deep Q-Networks, y los agentes que juegan Atari o Go que vas a ver en el Cap.12 del libro), que en el fondo intentan estimar esta función de valor sin conocer de antemano las probabilidades de transición reales del entorno (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.6)."
 },
 {
  "name": "Refuerzo · Q-learning real (aprender sin conocer el entorno)",
  "theory": "En el tema anterior calculaste V(s) con una <b>fórmula</b> que YA conocía exactamente cómo se movía el agente y qué premio recibía en cada paso — eso se llama <i>planning</i> (planificar con el mapa completo en la mano). El <b>Q-learning</b> real es otra cosa: el agente NO conoce el mapa. No sabe de antemano a dónde lo va a llevar cada acción ni qué premio va a recibir — tiene que ir <b>probando</b> (muestreando el entorno) y aprender de a poco, con cada experiencia real que vive.<br><br>La fórmula de actualización es la clave: cada vez que el agente prueba una acción y observa lo que pasó de verdad (recompensa <code>r</code> y nuevo estado <code>s'</code>), corrige su estimación <code>Q(s,a)</code> un poquito hacia lo que acaba de aprender — ni de golpe (eso sería inestable), ni ignorando la experiencia nueva. En el código, después de solo 60 intentos de recorrer el corredor <b>sin que nadie le haya dado nunca las fórmulas de \"siguiente\" ni \"recompensa\"</b>, el agente aprende exactamente los mismos valores que la fórmula cerrada del tema anterior: -2,71, -1,9 y -1,0. Aprendió solo, por experiencia, lo mismo que antes calculaste con la fórmula completa del mapa.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.11.9): la actualización de Q-learning es $Q(s,a) \\leftarrow Q(s,a) + \\alpha\\big(r + \\gamma \\max_{a'} Q(s',a') - Q(s,a)\\big)$ — el término entre paréntesis se llama <i>error TD</i> (diferencia temporal): la diferencia entre lo que el agente CREÍA que valía esa acción y lo que acaba de observar que realmente vale.",
  "code": "# Q-learning real (Kelleher, Sec.11.9): a diferencia del tema de la\n# funcion de valor V(s) (que usaba una FORMULA conocida de antemano),\n# aca el agente NO conoce 'siguiente'/'recompensa' -- los descubre\n# MUESTREANDO el entorno, y aprende Q(s,a) con la actualizacion TD real:\n# Q(s,a) <- Q(s,a) + alpha*(r + gamma*max_a' Q(s',a') - Q(s,a))\nimport numpy as np\n\n# mismo corredor de 4 estados del tema anterior: 0,1,2 intermedios, 3=meta\nsiguiente = {0: 1, 1: 2, 2: 3, 3: 3}\nrecompensa = {0: -1, 1: -1, 2: -1, 3: 0}\nacciones = ['avanzar']\n\nQ = {s: {a: 0.0 for a in acciones} for s in range(4)}\nalpha = 0.5   # tasa de aprendizaje\ngamma = 0.9   # mismo descuento del tema anterior\n\nhistorial_Q0 = []\nfor episodio in range(60):\n    s = 0\n    while s != 3:\n        a = 'avanzar'\n        r = recompensa[s]\n        s2 = siguiente[s]              # el agente MUESTREA esto, no lo sabia antes\n        mejor_siguiente = max(Q[s2].values())\n        Q[s][a] = Q[s][a] + alpha * (r + gamma * mejor_siguiente - Q[s][a])\n        s = s2\n    historial_Q0.append(round(Q[0]['avanzar'], 3))\n\nprint(\"Q(0,avanzar) cada 10 episodios:\", historial_Q0[::10])\nprint(\"Q(0,avanzar) final tras 60 episodios:\", round(Q[0]['avanzar'], 3))\nprint(\"Q(1,avanzar) final:\", round(Q[1]['avanzar'], 3))\nprint(\"Q(2,avanzar) final:\", round(Q[2]['avanzar'], 3))\nprint(\"\\ncomparacion con el V(s) EXACTO del tema anterior (formula cerrada):\")\nprint(\"  V(0)=-2.71  V(1)=-1.9  V(2)=-1.0\")\nprint(\"Q-learning aprendio ESTOS MISMOS valores solo muestreando el entorno,\")\nprint(\"sin que nunca se le dieran las formulas de siguiente/recompensa.\")",
  "viz": {
   "type": "curve",
   "data": {
    "points": [
     -0.5,
     -2.678,
     -2.71,
     -2.71,
     -2.71,
     -2.71
    ],
    "xLabel": "episodio (x10)",
    "yLabel": "Q(0, avanzar)",
    "aria": "Q(0,avanzar) converge desde -0.5 hasta -2.71 en pocos episodios, el mismo valor que la formula cerrada de V(0) del tema anterior"
   }
  },
  "application": "Q-learning (Watkins, 1989) es probablemente el algoritmo más influyente de todo el aprendizaje por refuerzo clásico — es la base conceptual detrás de DQN (Deep Q-Network), el sistema que en 2015 aprendió a jugar decenas de juegos de Atari al nivel humano usando solo los píxeles de la pantalla como entrada, sin que nadie le programara las reglas del juego. La idea central es siempre la misma que en este ejemplo minúsculo: un agente que no conoce las reglas del mundo puede aun así aprender a comportarse bien, con tal de poder probar, observar el resultado, y corregir su estimación — desde un termostato que aprende tus preferencias de temperatura hasta un robot que aprende a caminar por ensayo y error (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.9).",
  "codeAnatomy": {
   "title": "Actualización de Q(s,a) por experiencia real",
   "caption": "El agente muestrea el entorno paso a paso — no conoce las fórmulas de antemano",
   "lines": [
    "s2 = siguiente[s]              # el agente MUESTREA esto, no lo sabia antes",
    "mejor_siguiente = max(Q[s2].values())",
    "Q[s][a] = Q[s][a] + alpha * (r + gamma * mejor_siguiente - Q[s][a])"
   ],
   "annotations": [
    {
     "line": 0,
     "text": "siguiente[s]",
     "label": "Muestrea el entorno",
     "desc": "(no lo conocía de antemano, lo descubre en este paso)",
     "side": "top"
    },
    {
     "line": 1,
     "text": "max(Q[s2].values())",
     "label": "Mejor valor futuro conocido",
     "desc": "(hasta ahora, según lo aprendido)",
     "side": "top"
    },
    {
     "line": 2,
     "text": "r + gamma * mejor_siguiente - Q[s][a]",
     "label": "Error TD",
     "desc": "(diferencia entre lo observado y lo que creía)",
     "side": "bottom"
    },
    {
     "line": 2,
     "text": "Q[s][a] = Q[s][a] + alpha * (r + gamma * mejor_siguiente - Q[s][a])",
     "label": "Actualización incremental",
     "desc": "(corrige un poquito, no de golpe)",
     "side": "bottom"
    }
   ]
  }
 },
 {
  "name": "Refuerzo · Q-learning real (aprender sin conocer el entorno) — pregunta 2",
  "theory": "En el tema anterior calculaste V(s) con una <b>fórmula</b> que YA conocía exactamente cómo se movía el agente y qué premio recibía en cada paso — eso se llama <i>planning</i> (planificar con el mapa completo en la mano). El <b>Q-learning</b> real es otra cosa: el agente NO conoce el mapa. No sabe de antemano a dónde lo va a llevar cada acción ni qué premio va a recibir — tiene que ir <b>probando</b> (muestreando el entorno) y aprender de a poco, con cada experiencia real que vive.<br><br>La fórmula de actualización es la clave: cada vez que el agente prueba una acción y observa lo que pasó de verdad (recompensa <code>r</code> y nuevo estado <code>s'</code>), corrige su estimación <code>Q(s,a)</code> un poquito hacia lo que acaba de aprender — ni de golpe (eso sería inestable), ni ignorando la experiencia nueva. En el código, después de solo 60 intentos de recorrer el corredor <b>sin que nadie le haya dado nunca las fórmulas de \"siguiente\" ni \"recompensa\"</b>, el agente aprende exactamente los mismos valores que la fórmula cerrada del tema anterior: -2,71, -1,9 y -1,0. Aprendió solo, por experiencia, lo mismo que antes calculaste con la fórmula completa del mapa.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.11.9): la actualización de Q-learning es $Q(s,a) \\leftarrow Q(s,a) + \\alpha\\big(r + \\gamma \\max_{a'} Q(s',a') - Q(s,a)\\big)$ — el término entre paréntesis se llama <i>error TD</i> (diferencia temporal): la diferencia entre lo que el agente CREÍA que valía esa acción y lo que acaba de observar que realmente vale.",
  "code": "# Q-learning real (Kelleher, Sec.11.9): a diferencia del tema de la\n# funcion de valor V(s) (que usaba una FORMULA conocida de antemano),\n# aca el agente NO conoce 'siguiente'/'recompensa' -- los descubre\n# MUESTREANDO el entorno, y aprende Q(s,a) con la actualizacion TD real:\n# Q(s,a) <- Q(s,a) + alpha*(r + gamma*max_a' Q(s',a') - Q(s,a))\nimport numpy as np\n\n# mismo corredor de 4 estados del tema anterior: 0,1,2 intermedios, 3=meta\nsiguiente = {0: 1, 1: 2, 2: 3, 3: 3}\nrecompensa = {0: -1, 1: -1, 2: -1, 3: 0}\nacciones = ['avanzar']\n\nQ = {s: {a: 0.0 for a in acciones} for s in range(4)}\nalpha = 0.5   # tasa de aprendizaje\ngamma = 0.9   # mismo descuento del tema anterior\n\nhistorial_Q0 = []\nfor episodio in range(60):\n    s = 0\n    while s != 3:\n        a = 'avanzar'\n        r = recompensa[s]\n        s2 = siguiente[s]              # el agente MUESTREA esto, no lo sabia antes\n        mejor_siguiente = max(Q[s2].values())\n        Q[s][a] = Q[s][a] + alpha * (r + gamma * mejor_siguiente - Q[s][a])\n        s = s2\n    historial_Q0.append(round(Q[0]['avanzar'], 3))\n\nprint(\"Q(0,avanzar) cada 10 episodios:\", historial_Q0[::10])\nprint(\"Q(0,avanzar) final tras 60 episodios:\", round(Q[0]['avanzar'], 3))\nprint(\"Q(1,avanzar) final:\", round(Q[1]['avanzar'], 3))\nprint(\"Q(2,avanzar) final:\", round(Q[2]['avanzar'], 3))\nprint(\"\\ncomparacion con el V(s) EXACTO del tema anterior (formula cerrada):\")\nprint(\"  V(0)=-2.71  V(1)=-1.9  V(2)=-1.0\")\nprint(\"Q-learning aprendio ESTOS MISMOS valores solo muestreando el entorno,\")\nprint(\"sin que nunca se le dieran las formulas de siguiente/recompensa.\")",
  "viz": {
   "type": "curve",
   "data": {
    "points": [
     -0.5,
     -2.678,
     -2.71,
     -2.71,
     -2.71,
     -2.71
    ],
    "xLabel": "episodio (x10)",
    "yLabel": "Q(0, avanzar)",
    "aria": "Q(0,avanzar) converge desde -0.5 hasta -2.71 en pocos episodios, el mismo valor que la formula cerrada de V(0) del tema anterior"
   }
  },
  "application": "Q-learning (Watkins, 1989) es probablemente el algoritmo más influyente de todo el aprendizaje por refuerzo clásico — es la base conceptual detrás de DQN (Deep Q-Network), el sistema que en 2015 aprendió a jugar decenas de juegos de Atari al nivel humano usando solo los píxeles de la pantalla como entrada, sin que nadie le programara las reglas del juego. La idea central es siempre la misma que en este ejemplo minúsculo: un agente que no conoce las reglas del mundo puede aun así aprender a comportarse bien, con tal de poder probar, observar el resultado, y corregir su estimación — desde un termostato que aprende tus preferencias de temperatura hasta un robot que aprende a caminar por ensayo y error (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.9)."
 },
 {
  "name": "Refuerzo · Q-learning real (aprender sin conocer el entorno) — pregunta 3",
  "theory": "En el tema anterior calculaste V(s) con una <b>fórmula</b> que YA conocía exactamente cómo se movía el agente y qué premio recibía en cada paso — eso se llama <i>planning</i> (planificar con el mapa completo en la mano). El <b>Q-learning</b> real es otra cosa: el agente NO conoce el mapa. No sabe de antemano a dónde lo va a llevar cada acción ni qué premio va a recibir — tiene que ir <b>probando</b> (muestreando el entorno) y aprender de a poco, con cada experiencia real que vive.<br><br>La fórmula de actualización es la clave: cada vez que el agente prueba una acción y observa lo que pasó de verdad (recompensa <code>r</code> y nuevo estado <code>s'</code>), corrige su estimación <code>Q(s,a)</code> un poquito hacia lo que acaba de aprender — ni de golpe (eso sería inestable), ni ignorando la experiencia nueva. En el código, después de solo 60 intentos de recorrer el corredor <b>sin que nadie le haya dado nunca las fórmulas de \"siguiente\" ni \"recompensa\"</b>, el agente aprende exactamente los mismos valores que la fórmula cerrada del tema anterior: -2,71, -1,9 y -1,0. Aprendió solo, por experiencia, lo mismo que antes calculaste con la fórmula completa del mapa.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.11.9): la actualización de Q-learning es $Q(s,a) \\leftarrow Q(s,a) + \\alpha\\big(r + \\gamma \\max_{a'} Q(s',a') - Q(s,a)\\big)$ — el término entre paréntesis se llama <i>error TD</i> (diferencia temporal): la diferencia entre lo que el agente CREÍA que valía esa acción y lo que acaba de observar que realmente vale.",
  "code": "# Q-learning real (Kelleher, Sec.11.9): a diferencia del tema de la\n# funcion de valor V(s) (que usaba una FORMULA conocida de antemano),\n# aca el agente NO conoce 'siguiente'/'recompensa' -- los descubre\n# MUESTREANDO el entorno, y aprende Q(s,a) con la actualizacion TD real:\n# Q(s,a) <- Q(s,a) + alpha*(r + gamma*max_a' Q(s',a') - Q(s,a))\nimport numpy as np\n\n# mismo corredor de 4 estados del tema anterior: 0,1,2 intermedios, 3=meta\nsiguiente = {0: 1, 1: 2, 2: 3, 3: 3}\nrecompensa = {0: -1, 1: -1, 2: -1, 3: 0}\nacciones = ['avanzar']\n\nQ = {s: {a: 0.0 for a in acciones} for s in range(4)}\nalpha = 0.5   # tasa de aprendizaje\ngamma = 0.9   # mismo descuento del tema anterior\n\nhistorial_Q0 = []\nfor episodio in range(60):\n    s = 0\n    while s != 3:\n        a = 'avanzar'\n        r = recompensa[s]\n        s2 = siguiente[s]              # el agente MUESTREA esto, no lo sabia antes\n        mejor_siguiente = max(Q[s2].values())\n        Q[s][a] = Q[s][a] + alpha * (r + gamma * mejor_siguiente - Q[s][a])\n        s = s2\n    historial_Q0.append(round(Q[0]['avanzar'], 3))\n\nprint(\"Q(0,avanzar) cada 10 episodios:\", historial_Q0[::10])\nprint(\"Q(0,avanzar) final tras 60 episodios:\", round(Q[0]['avanzar'], 3))\nprint(\"Q(1,avanzar) final:\", round(Q[1]['avanzar'], 3))\nprint(\"Q(2,avanzar) final:\", round(Q[2]['avanzar'], 3))\nprint(\"\\ncomparacion con el V(s) EXACTO del tema anterior (formula cerrada):\")\nprint(\"  V(0)=-2.71  V(1)=-1.9  V(2)=-1.0\")\nprint(\"Q-learning aprendio ESTOS MISMOS valores solo muestreando el entorno,\")\nprint(\"sin que nunca se le dieran las formulas de siguiente/recompensa.\")",
  "viz": {
   "type": "curve",
   "data": {
    "points": [
     -0.5,
     -2.678,
     -2.71,
     -2.71,
     -2.71,
     -2.71
    ],
    "xLabel": "episodio (x10)",
    "yLabel": "Q(0, avanzar)",
    "aria": "Q(0,avanzar) converge desde -0.5 hasta -2.71 en pocos episodios, el mismo valor que la formula cerrada de V(0) del tema anterior"
   }
  },
  "application": "Q-learning (Watkins, 1989) es probablemente el algoritmo más influyente de todo el aprendizaje por refuerzo clásico — es la base conceptual detrás de DQN (Deep Q-Network), el sistema que en 2015 aprendió a jugar decenas de juegos de Atari al nivel humano usando solo los píxeles de la pantalla como entrada, sin que nadie le programara las reglas del juego. La idea central es siempre la misma que en este ejemplo minúsculo: un agente que no conoce las reglas del mundo puede aun así aprender a comportarse bien, con tal de poder probar, observar el resultado, y corregir su estimación — desde un termostato que aprende tus preferencias de temperatura hasta un robot que aprende a caminar por ensayo y error (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.9)."
 },
 {
  "name": "Refuerzo · Q-learning real (aprender sin conocer el entorno) — pregunta 4",
  "theory": "En el tema anterior calculaste V(s) con una <b>fórmula</b> que YA conocía exactamente cómo se movía el agente y qué premio recibía en cada paso — eso se llama <i>planning</i> (planificar con el mapa completo en la mano). El <b>Q-learning</b> real es otra cosa: el agente NO conoce el mapa. No sabe de antemano a dónde lo va a llevar cada acción ni qué premio va a recibir — tiene que ir <b>probando</b> (muestreando el entorno) y aprender de a poco, con cada experiencia real que vive.<br><br>La fórmula de actualización es la clave: cada vez que el agente prueba una acción y observa lo que pasó de verdad (recompensa <code>r</code> y nuevo estado <code>s'</code>), corrige su estimación <code>Q(s,a)</code> un poquito hacia lo que acaba de aprender — ni de golpe (eso sería inestable), ni ignorando la experiencia nueva. En el código, después de solo 60 intentos de recorrer el corredor <b>sin que nadie le haya dado nunca las fórmulas de \"siguiente\" ni \"recompensa\"</b>, el agente aprende exactamente los mismos valores que la fórmula cerrada del tema anterior: -2,71, -1,9 y -1,0. Aprendió solo, por experiencia, lo mismo que antes calculaste con la fórmula completa del mapa.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.11.9): la actualización de Q-learning es $Q(s,a) \\leftarrow Q(s,a) + \\alpha\\big(r + \\gamma \\max_{a'} Q(s',a') - Q(s,a)\\big)$ — el término entre paréntesis se llama <i>error TD</i> (diferencia temporal): la diferencia entre lo que el agente CREÍA que valía esa acción y lo que acaba de observar que realmente vale.",
  "code": "# Q-learning real (Kelleher, Sec.11.9): a diferencia del tema de la\n# funcion de valor V(s) (que usaba una FORMULA conocida de antemano),\n# aca el agente NO conoce 'siguiente'/'recompensa' -- los descubre\n# MUESTREANDO el entorno, y aprende Q(s,a) con la actualizacion TD real:\n# Q(s,a) <- Q(s,a) + alpha*(r + gamma*max_a' Q(s',a') - Q(s,a))\nimport numpy as np\n\n# mismo corredor de 4 estados del tema anterior: 0,1,2 intermedios, 3=meta\nsiguiente = {0: 1, 1: 2, 2: 3, 3: 3}\nrecompensa = {0: -1, 1: -1, 2: -1, 3: 0}\nacciones = ['avanzar']\n\nQ = {s: {a: 0.0 for a in acciones} for s in range(4)}\nalpha = 0.5   # tasa de aprendizaje\ngamma = 0.9   # mismo descuento del tema anterior\n\nhistorial_Q0 = []\nfor episodio in range(60):\n    s = 0\n    while s != 3:\n        a = 'avanzar'\n        r = recompensa[s]\n        s2 = siguiente[s]              # el agente MUESTREA esto, no lo sabia antes\n        mejor_siguiente = max(Q[s2].values())\n        Q[s][a] = Q[s][a] + alpha * (r + gamma * mejor_siguiente - Q[s][a])\n        s = s2\n    historial_Q0.append(round(Q[0]['avanzar'], 3))\n\nprint(\"Q(0,avanzar) cada 10 episodios:\", historial_Q0[::10])\nprint(\"Q(0,avanzar) final tras 60 episodios:\", round(Q[0]['avanzar'], 3))\nprint(\"Q(1,avanzar) final:\", round(Q[1]['avanzar'], 3))\nprint(\"Q(2,avanzar) final:\", round(Q[2]['avanzar'], 3))\nprint(\"\\ncomparacion con el V(s) EXACTO del tema anterior (formula cerrada):\")\nprint(\"  V(0)=-2.71  V(1)=-1.9  V(2)=-1.0\")\nprint(\"Q-learning aprendio ESTOS MISMOS valores solo muestreando el entorno,\")\nprint(\"sin que nunca se le dieran las formulas de siguiente/recompensa.\")",
  "viz": {
   "type": "curve",
   "data": {
    "points": [
     -0.5,
     -2.678,
     -2.71,
     -2.71,
     -2.71,
     -2.71
    ],
    "xLabel": "episodio (x10)",
    "yLabel": "Q(0, avanzar)",
    "aria": "Q(0,avanzar) converge desde -0.5 hasta -2.71 en pocos episodios, el mismo valor que la formula cerrada de V(0) del tema anterior"
   }
  },
  "application": "Q-learning (Watkins, 1989) es probablemente el algoritmo más influyente de todo el aprendizaje por refuerzo clásico — es la base conceptual detrás de DQN (Deep Q-Network), el sistema que en 2015 aprendió a jugar decenas de juegos de Atari al nivel humano usando solo los píxeles de la pantalla como entrada, sin que nadie le programara las reglas del juego. La idea central es siempre la misma que en este ejemplo minúsculo: un agente que no conoce las reglas del mundo puede aun así aprender a comportarse bien, con tal de poder probar, observar el resultado, y corregir su estimación — desde un termostato que aprende tus preferencias de temperatura hasta un robot que aprende a caminar por ensayo y error (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.11.9)."
 },
 {
  "name": "Refuerzo · Tabla vs. función: por qué Q-learning necesita aproximar Q(s,a)",
  "theory": "Imaginate que en vez de aprenderte la <b>tabla de multiplicar</b> de memoria (2×1=2, 2×2=4, 2×3=6... una casilla por cada combinación posible), aprendés la <b>regla</b> \"multiplicar es sumar el primer número tantas veces como diga el segundo\". Con la tabla, si te preguntan 2×1000 y nunca memorizaste esa fila, estás perdido. Con la regla, te sirve para CUALQUIER número, incluso uno que nunca viste. Eso es exactamente lo que le pasa a Q-learning cuando el número de estados posibles crece: una tabla Q(s,a) con una casilla POR CADA estado se vuelve gigante o directamente imposible de guardar (el propio libro da un ejemplo extremo: el juego de Go tiene 10¹⁷⁰ estados posibles — muchísimos más que átomos hay en el universo observable). La solución no es agrandar la tabla, es REEMPLAZARLA por una función con unos pocos parámetros ajustables, que generaliza incluso a estados que nunca visitó.<br><br>En el código: <code>Q_tabla</code> (lo que aprendió Q-learning en el tema anterior) tiene 4 entradas EXACTAS, una por estado: -2,71, -1,9, -1,0 y 0,0 — funciona porque solo hay 4 estados. Pero si el corredor tuviera 1000 posiciones posibles en vez de 4, la tabla necesitaría 1000 números guardados. En cambio, aproximando Q(s) con la función lineal más simple que existe, <code>Q_aprox(s) = w·s + b</code>, solo hacen falta 2 números (w y b) — sin importar si el estado tiene 4, 1000 o infinitos valores posibles. Ajustando w y b con el MISMO tipo de corrección por diferencia temporal que usó Q-learning (pero corrigiendo los PARÁMETROS de la función en vez de una casilla de tabla), después de solo 40 episodios la función aprende Q_aprox(0)=-2,677, Q_aprox(1)=-1,838, Q_aprox(2)=-1,0 — muy cerca de los valores EXACTOS de la tabla (-2,71, -1,9, -1,0), con un error cuadrático medio de apenas 0,0016, usando 500 veces MENOS parámetros que una tabla de 1000 estados.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.12.1-12.2, pág.229-230): «storing the Q values in a table may be infeasible when the state or action spaces are very large or when they are continuous… the game of Go consists of 10¹⁷⁰ states». La solución es aproximar $Q_\\theta(s,a) \\approx Q_\\pi(s,a)$ con una función de parámetros $\\theta$, ajustados por descenso del gradiente: $\\Delta\\theta = \\alpha\\big(r + \\gamma\\max_{a'}Q_\\theta(s',a') - Q_\\theta(s,a)\\big)\\nabla_\\theta Q_\\theta(s,a)$ (Ec.12.14).",
  "code": "# Cuando la tabla Q ya no alcanza: aproximar Q(s) con una funcion en vez\n# de guardarla EXACTA (Kelleher, Sec 12.1 Introduction, pag.229): \"storing\n# the Q values in a table may be infeasible when the state or action\n# spaces are very large or when they are continuous. For example, the\n# game of Go consists of 10^170 states.\" La solucion (Sec 12.2, pag.230):\n# aproximar Q(s,a) con una funcion de PARAMETROS (una red neuronal en\n# DQN; aca, la mas simple posible: una recta) en vez de una tabla.\nimport numpy as np\n\n# Q_tabla: lo que aprendio Q-learning en el tema anterior, GUARDADO\n# exacto, una entrada por estado -- funciona porque solo hay 4 estados.\nQ_tabla = {0: -2.71, 1: -1.9, 2: -1.0, 3: 0.0}\n\n# si el estado no fueran 4 casillas sino, por ejemplo, 1000 posiciones\n# distintas (o un numero CONTINUO, como en Go: 10^170), una tabla\n# necesitaria 1 entrada POR CADA estado posible:\nn_estados_grande = 1000\nparametros_tabla = n_estados_grande\nparametros_funcion = 2   # w y b -- NO CAMBIA sin importar cuantos estados haya\n\n# mismo corredor de siempre: 0,1,2 intermedios, 3=meta (terminal)\nsiguiente = {0: 1, 1: 2, 2: 3}\nrecompensa = {0: -1, 1: -1, 2: -1}\ngamma = 0.9\nalpha = 0.2\n\n# en vez de una tabla, aproximamos Q(s) = w*s + b (una funcion LINEAL,\n# la mas simple que existe). Actualizacion identica a la Ec.12.14 del\n# libro (semi-gradiente TD): Delta_theta = alpha*(r + gamma*max Q_theta(s')\n# - Q_theta(s)) * grad_theta Q_theta(s); para Q(s)=w*s+b: grad_w=s, grad_b=1\nw, b = 0.0, 0.0\nhistorial_b = []\nfor episodio in range(40):\n    s = 0\n    while s != 3:\n        s2 = siguiente[s]\n        objetivo = recompensa[s] if s2 == 3 else recompensa[s] + gamma * (w * s2 + b)\n        error_td = objetivo - (w * s + b)\n        w, b = w + alpha * error_td * s, b + alpha * error_td\n        s = s2\n    if episodio % 5 == 0:\n        historial_b.append(round(float(b), 3))\nhistorial_b.append(round(float(b), 3))\n\nQ_aprox = {s: round(float(w * s + b), 3) for s in range(4)}\nerror = np.array([Q_tabla[s] - Q_aprox[s] for s in range(3)])\n\nprint(\"Q_tabla (guardada exacta, tema anterior):\", Q_tabla)\nprint(\"Q_aprox (aprendida con SOLO 2 parametros w,b):\", Q_aprox)\nprint(\"w final:\", round(w, 4), \" b final:\", round(b, 4))\nprint(\"Q(0) durante el entrenamiento (cada 5 episodios):\", historial_b)\nprint(\"\\nerror por estado (tabla - funcion), estados 0,1,2:\", [round(float(e), 3) for e in error])\nprint(\"error cuadratico medio:\", round(float(np.mean(error ** 2)), 4))\nprint(\"\\nparametros necesarios con TABLA (1000 estados posibles):\", parametros_tabla)\nprint(\"parametros necesarios con FUNCION (w,b), sin importar cuantos estados haya:\", parametros_funcion)\nprint(\"la funcion usa\", round(parametros_tabla / parametros_funcion), \"veces MENOS parametros\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Tabla · 1000 estados posibles",
     "Función Q(s)=w·s+b"
    ],
    "values": [
     1000,
     2
    ],
    "unit": " parámetros",
    "aria": "Una tabla con 1000 estados posibles necesita 1000 parametros guardados (uno por estado); la funcion lineal Q(s)=w*s+b necesita solo 2 parametros (w y b), sin importar cuantos estados haya"
   }
  },
  "application": "La idea de aproximar Q(s,a) con una función en vez de guardarla en una tabla es exactamente lo que hace posible el Aprendizaje por Refuerzo Profundo (Deep RL): reemplazar la función lineal w·s+b de este ejemplo por una red neuronal profunda (por ejemplo, una CNN) que recibe el estado — los píxeles de una pantalla, la posición de un robot, el tablero de Go — y aproxima Q(s,a) o la política π(a|s) sin necesitar una tabla imposible de guardar. Así funciona DQN (Deep Q-Network, Mnih et al., 2015), que aprendió a jugar decenas de juegos de Atari al nivel humano usando solo los píxeles como entrada; y así funcionan sistemas que, según el propio libro, dominan el ajedrez, Shogi y Go (Silver et al., 2018), alcanzan nivel Gran Maestro en StarCraft II, o controlan un robot cuadrúpedo caminando sobre terreno difícil — en todos los casos, el espacio de estados es demasiado grande para una tabla, y una red neuronal aproxima el valor de cada estado entrenándose por descenso del gradiente (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.12.1, pág.229).",
  "codeAnatomy": {
   "title": "Tabla vs. función: cuántos parámetros hacen falta",
   "caption": "Una tabla necesita 1 entrada por estado; una función lineal siempre necesita 2",
   "lines": [
    "parametros_tabla = n_estados_grande",
    "parametros_funcion = 2   # w y b -- NO CAMBIA sin importar cuantos estados haya",
    "Q_aprox = {s: round(float(w * s + b), 3) for s in range(4)}"
   ],
   "annotations": [
    {
     "line": 0,
     "text": "n_estados_grande",
     "label": "Un parámetro por estado",
     "desc": "(1000 si hubiera 1000 estados posibles)",
     "side": "top"
    },
    {
     "line": 1,
     "text": "2",
     "label": "Siempre 2",
     "desc": "(w y b, sin importar cuántos estados haya)",
     "side": "top"
    },
    {
     "line": 2,
     "text": "w * s + b",
     "label": "Una recta",
     "desc": "(la función más simple posible)",
     "side": "bottom"
    },
    {
     "line": 2,
     "text": "for s in range(4)",
     "label": "Evaluable en cualquier estado",
     "desc": "(incluso uno nunca visitado)",
     "side": "bottom"
    }
   ]
  }
 },
 {
  "name": "Refuerzo · Tabla vs. función: por qué Q-learning necesita aproximar Q(s,a) — pregunta 2",
  "theory": "Imaginate que en vez de aprenderte la <b>tabla de multiplicar</b> de memoria (2×1=2, 2×2=4, 2×3=6... una casilla por cada combinación posible), aprendés la <b>regla</b> \"multiplicar es sumar el primer número tantas veces como diga el segundo\". Con la tabla, si te preguntan 2×1000 y nunca memorizaste esa fila, estás perdido. Con la regla, te sirve para CUALQUIER número, incluso uno que nunca viste. Eso es exactamente lo que le pasa a Q-learning cuando el número de estados posibles crece: una tabla Q(s,a) con una casilla POR CADA estado se vuelve gigante o directamente imposible de guardar (el propio libro da un ejemplo extremo: el juego de Go tiene 10¹⁷⁰ estados posibles — muchísimos más que átomos hay en el universo observable). La solución no es agrandar la tabla, es REEMPLAZARLA por una función con unos pocos parámetros ajustables, que generaliza incluso a estados que nunca visitó.<br><br>En el código: <code>Q_tabla</code> (lo que aprendió Q-learning en el tema anterior) tiene 4 entradas EXACTAS, una por estado: -2,71, -1,9, -1,0 y 0,0 — funciona porque solo hay 4 estados. Pero si el corredor tuviera 1000 posiciones posibles en vez de 4, la tabla necesitaría 1000 números guardados. En cambio, aproximando Q(s) con la función lineal más simple que existe, <code>Q_aprox(s) = w·s + b</code>, solo hacen falta 2 números (w y b) — sin importar si el estado tiene 4, 1000 o infinitos valores posibles. Ajustando w y b con el MISMO tipo de corrección por diferencia temporal que usó Q-learning (pero corrigiendo los PARÁMETROS de la función en vez de una casilla de tabla), después de solo 40 episodios la función aprende Q_aprox(0)=-2,677, Q_aprox(1)=-1,838, Q_aprox(2)=-1,0 — muy cerca de los valores EXACTOS de la tabla (-2,71, -1,9, -1,0), con un error cuadrático medio de apenas 0,0016, usando 500 veces MENOS parámetros que una tabla de 1000 estados.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.12.1-12.2, pág.229-230): «storing the Q values in a table may be infeasible when the state or action spaces are very large or when they are continuous… the game of Go consists of 10¹⁷⁰ states». La solución es aproximar $Q_\\theta(s,a) \\approx Q_\\pi(s,a)$ con una función de parámetros $\\theta$, ajustados por descenso del gradiente: $\\Delta\\theta = \\alpha\\big(r + \\gamma\\max_{a'}Q_\\theta(s',a') - Q_\\theta(s,a)\\big)\\nabla_\\theta Q_\\theta(s,a)$ (Ec.12.14).",
  "code": "# Cuando la tabla Q ya no alcanza: aproximar Q(s) con una funcion en vez\n# de guardarla EXACTA (Kelleher, Sec 12.1 Introduction, pag.229): \"storing\n# the Q values in a table may be infeasible when the state or action\n# spaces are very large or when they are continuous. For example, the\n# game of Go consists of 10^170 states.\" La solucion (Sec 12.2, pag.230):\n# aproximar Q(s,a) con una funcion de PARAMETROS (una red neuronal en\n# DQN; aca, la mas simple posible: una recta) en vez de una tabla.\nimport numpy as np\n\n# Q_tabla: lo que aprendio Q-learning en el tema anterior, GUARDADO\n# exacto, una entrada por estado -- funciona porque solo hay 4 estados.\nQ_tabla = {0: -2.71, 1: -1.9, 2: -1.0, 3: 0.0}\n\n# si el estado no fueran 4 casillas sino, por ejemplo, 1000 posiciones\n# distintas (o un numero CONTINUO, como en Go: 10^170), una tabla\n# necesitaria 1 entrada POR CADA estado posible:\nn_estados_grande = 1000\nparametros_tabla = n_estados_grande\nparametros_funcion = 2   # w y b -- NO CAMBIA sin importar cuantos estados haya\n\n# mismo corredor de siempre: 0,1,2 intermedios, 3=meta (terminal)\nsiguiente = {0: 1, 1: 2, 2: 3}\nrecompensa = {0: -1, 1: -1, 2: -1}\ngamma = 0.9\nalpha = 0.2\n\n# en vez de una tabla, aproximamos Q(s) = w*s + b (una funcion LINEAL,\n# la mas simple que existe). Actualizacion identica a la Ec.12.14 del\n# libro (semi-gradiente TD): Delta_theta = alpha*(r + gamma*max Q_theta(s')\n# - Q_theta(s)) * grad_theta Q_theta(s); para Q(s)=w*s+b: grad_w=s, grad_b=1\nw, b = 0.0, 0.0\nhistorial_b = []\nfor episodio in range(40):\n    s = 0\n    while s != 3:\n        s2 = siguiente[s]\n        objetivo = recompensa[s] if s2 == 3 else recompensa[s] + gamma * (w * s2 + b)\n        error_td = objetivo - (w * s + b)\n        w, b = w + alpha * error_td * s, b + alpha * error_td\n        s = s2\n    if episodio % 5 == 0:\n        historial_b.append(round(float(b), 3))\nhistorial_b.append(round(float(b), 3))\n\nQ_aprox = {s: round(float(w * s + b), 3) for s in range(4)}\nerror = np.array([Q_tabla[s] - Q_aprox[s] for s in range(3)])\n\nprint(\"Q_tabla (guardada exacta, tema anterior):\", Q_tabla)\nprint(\"Q_aprox (aprendida con SOLO 2 parametros w,b):\", Q_aprox)\nprint(\"w final:\", round(w, 4), \" b final:\", round(b, 4))\nprint(\"Q(0) durante el entrenamiento (cada 5 episodios):\", historial_b)\nprint(\"\\nerror por estado (tabla - funcion), estados 0,1,2:\", [round(float(e), 3) for e in error])\nprint(\"error cuadratico medio:\", round(float(np.mean(error ** 2)), 4))\nprint(\"\\nparametros necesarios con TABLA (1000 estados posibles):\", parametros_tabla)\nprint(\"parametros necesarios con FUNCION (w,b), sin importar cuantos estados haya:\", parametros_funcion)\nprint(\"la funcion usa\", round(parametros_tabla / parametros_funcion), \"veces MENOS parametros\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Tabla · 1000 estados posibles",
     "Función Q(s)=w·s+b"
    ],
    "values": [
     1000,
     2
    ],
    "unit": " parámetros",
    "aria": "Una tabla con 1000 estados posibles necesita 1000 parametros guardados (uno por estado); la funcion lineal Q(s)=w*s+b necesita solo 2 parametros (w y b), sin importar cuantos estados haya"
   }
  },
  "application": "La idea de aproximar Q(s,a) con una función en vez de guardarla en una tabla es exactamente lo que hace posible el Aprendizaje por Refuerzo Profundo (Deep RL): reemplazar la función lineal w·s+b de este ejemplo por una red neuronal profunda (por ejemplo, una CNN) que recibe el estado — los píxeles de una pantalla, la posición de un robot, el tablero de Go — y aproxima Q(s,a) o la política π(a|s) sin necesitar una tabla imposible de guardar. Así funciona DQN (Deep Q-Network, Mnih et al., 2015), que aprendió a jugar decenas de juegos de Atari al nivel humano usando solo los píxeles como entrada; y así funcionan sistemas que, según el propio libro, dominan el ajedrez, Shogi y Go (Silver et al., 2018), alcanzan nivel Gran Maestro en StarCraft II, o controlan un robot cuadrúpedo caminando sobre terreno difícil — en todos los casos, el espacio de estados es demasiado grande para una tabla, y una red neuronal aproxima el valor de cada estado entrenándose por descenso del gradiente (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.12.1, pág.229)."
 },
 {
  "name": "Refuerzo · Tabla vs. función: por qué Q-learning necesita aproximar Q(s,a) — pregunta 3",
  "theory": "Imaginate que en vez de aprenderte la <b>tabla de multiplicar</b> de memoria (2×1=2, 2×2=4, 2×3=6... una casilla por cada combinación posible), aprendés la <b>regla</b> \"multiplicar es sumar el primer número tantas veces como diga el segundo\". Con la tabla, si te preguntan 2×1000 y nunca memorizaste esa fila, estás perdido. Con la regla, te sirve para CUALQUIER número, incluso uno que nunca viste. Eso es exactamente lo que le pasa a Q-learning cuando el número de estados posibles crece: una tabla Q(s,a) con una casilla POR CADA estado se vuelve gigante o directamente imposible de guardar (el propio libro da un ejemplo extremo: el juego de Go tiene 10¹⁷⁰ estados posibles — muchísimos más que átomos hay en el universo observable). La solución no es agrandar la tabla, es REEMPLAZARLA por una función con unos pocos parámetros ajustables, que generaliza incluso a estados que nunca visitó.<br><br>En el código: <code>Q_tabla</code> (lo que aprendió Q-learning en el tema anterior) tiene 4 entradas EXACTAS, una por estado: -2,71, -1,9, -1,0 y 0,0 — funciona porque solo hay 4 estados. Pero si el corredor tuviera 1000 posiciones posibles en vez de 4, la tabla necesitaría 1000 números guardados. En cambio, aproximando Q(s) con la función lineal más simple que existe, <code>Q_aprox(s) = w·s + b</code>, solo hacen falta 2 números (w y b) — sin importar si el estado tiene 4, 1000 o infinitos valores posibles. Ajustando w y b con el MISMO tipo de corrección por diferencia temporal que usó Q-learning (pero corrigiendo los PARÁMETROS de la función en vez de una casilla de tabla), después de solo 40 episodios la función aprende Q_aprox(0)=-2,677, Q_aprox(1)=-1,838, Q_aprox(2)=-1,0 — muy cerca de los valores EXACTOS de la tabla (-2,71, -1,9, -1,0), con un error cuadrático medio de apenas 0,0016, usando 500 veces MENOS parámetros que una tabla de 1000 estados.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.12.1-12.2, pág.229-230): «storing the Q values in a table may be infeasible when the state or action spaces are very large or when they are continuous… the game of Go consists of 10¹⁷⁰ states». La solución es aproximar $Q_\\theta(s,a) \\approx Q_\\pi(s,a)$ con una función de parámetros $\\theta$, ajustados por descenso del gradiente: $\\Delta\\theta = \\alpha\\big(r + \\gamma\\max_{a'}Q_\\theta(s',a') - Q_\\theta(s,a)\\big)\\nabla_\\theta Q_\\theta(s,a)$ (Ec.12.14).",
  "code": "# Cuando la tabla Q ya no alcanza: aproximar Q(s) con una funcion en vez\n# de guardarla EXACTA (Kelleher, Sec 12.1 Introduction, pag.229): \"storing\n# the Q values in a table may be infeasible when the state or action\n# spaces are very large or when they are continuous. For example, the\n# game of Go consists of 10^170 states.\" La solucion (Sec 12.2, pag.230):\n# aproximar Q(s,a) con una funcion de PARAMETROS (una red neuronal en\n# DQN; aca, la mas simple posible: una recta) en vez de una tabla.\nimport numpy as np\n\n# Q_tabla: lo que aprendio Q-learning en el tema anterior, GUARDADO\n# exacto, una entrada por estado -- funciona porque solo hay 4 estados.\nQ_tabla = {0: -2.71, 1: -1.9, 2: -1.0, 3: 0.0}\n\n# si el estado no fueran 4 casillas sino, por ejemplo, 1000 posiciones\n# distintas (o un numero CONTINUO, como en Go: 10^170), una tabla\n# necesitaria 1 entrada POR CADA estado posible:\nn_estados_grande = 1000\nparametros_tabla = n_estados_grande\nparametros_funcion = 2   # w y b -- NO CAMBIA sin importar cuantos estados haya\n\n# mismo corredor de siempre: 0,1,2 intermedios, 3=meta (terminal)\nsiguiente = {0: 1, 1: 2, 2: 3}\nrecompensa = {0: -1, 1: -1, 2: -1}\ngamma = 0.9\nalpha = 0.2\n\n# en vez de una tabla, aproximamos Q(s) = w*s + b (una funcion LINEAL,\n# la mas simple que existe). Actualizacion identica a la Ec.12.14 del\n# libro (semi-gradiente TD): Delta_theta = alpha*(r + gamma*max Q_theta(s')\n# - Q_theta(s)) * grad_theta Q_theta(s); para Q(s)=w*s+b: grad_w=s, grad_b=1\nw, b = 0.0, 0.0\nhistorial_b = []\nfor episodio in range(40):\n    s = 0\n    while s != 3:\n        s2 = siguiente[s]\n        objetivo = recompensa[s] if s2 == 3 else recompensa[s] + gamma * (w * s2 + b)\n        error_td = objetivo - (w * s + b)\n        w, b = w + alpha * error_td * s, b + alpha * error_td\n        s = s2\n    if episodio % 5 == 0:\n        historial_b.append(round(float(b), 3))\nhistorial_b.append(round(float(b), 3))\n\nQ_aprox = {s: round(float(w * s + b), 3) for s in range(4)}\nerror = np.array([Q_tabla[s] - Q_aprox[s] for s in range(3)])\n\nprint(\"Q_tabla (guardada exacta, tema anterior):\", Q_tabla)\nprint(\"Q_aprox (aprendida con SOLO 2 parametros w,b):\", Q_aprox)\nprint(\"w final:\", round(w, 4), \" b final:\", round(b, 4))\nprint(\"Q(0) durante el entrenamiento (cada 5 episodios):\", historial_b)\nprint(\"\\nerror por estado (tabla - funcion), estados 0,1,2:\", [round(float(e), 3) for e in error])\nprint(\"error cuadratico medio:\", round(float(np.mean(error ** 2)), 4))\nprint(\"\\nparametros necesarios con TABLA (1000 estados posibles):\", parametros_tabla)\nprint(\"parametros necesarios con FUNCION (w,b), sin importar cuantos estados haya:\", parametros_funcion)\nprint(\"la funcion usa\", round(parametros_tabla / parametros_funcion), \"veces MENOS parametros\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Tabla · 1000 estados posibles",
     "Función Q(s)=w·s+b"
    ],
    "values": [
     1000,
     2
    ],
    "unit": " parámetros",
    "aria": "Una tabla con 1000 estados posibles necesita 1000 parametros guardados (uno por estado); la funcion lineal Q(s)=w*s+b necesita solo 2 parametros (w y b), sin importar cuantos estados haya"
   }
  },
  "application": "La idea de aproximar Q(s,a) con una función en vez de guardarla en una tabla es exactamente lo que hace posible el Aprendizaje por Refuerzo Profundo (Deep RL): reemplazar la función lineal w·s+b de este ejemplo por una red neuronal profunda (por ejemplo, una CNN) que recibe el estado — los píxeles de una pantalla, la posición de un robot, el tablero de Go — y aproxima Q(s,a) o la política π(a|s) sin necesitar una tabla imposible de guardar. Así funciona DQN (Deep Q-Network, Mnih et al., 2015), que aprendió a jugar decenas de juegos de Atari al nivel humano usando solo los píxeles como entrada; y así funcionan sistemas que, según el propio libro, dominan el ajedrez, Shogi y Go (Silver et al., 2018), alcanzan nivel Gran Maestro en StarCraft II, o controlan un robot cuadrúpedo caminando sobre terreno difícil — en todos los casos, el espacio de estados es demasiado grande para una tabla, y una red neuronal aproxima el valor de cada estado entrenándose por descenso del gradiente (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.12.1, pág.229)."
 },
 {
  "name": "Refuerzo · Tabla vs. función: por qué Q-learning necesita aproximar Q(s,a) — pregunta 4",
  "theory": "Imaginate que en vez de aprenderte la <b>tabla de multiplicar</b> de memoria (2×1=2, 2×2=4, 2×3=6... una casilla por cada combinación posible), aprendés la <b>regla</b> \"multiplicar es sumar el primer número tantas veces como diga el segundo\". Con la tabla, si te preguntan 2×1000 y nunca memorizaste esa fila, estás perdido. Con la regla, te sirve para CUALQUIER número, incluso uno que nunca viste. Eso es exactamente lo que le pasa a Q-learning cuando el número de estados posibles crece: una tabla Q(s,a) con una casilla POR CADA estado se vuelve gigante o directamente imposible de guardar (el propio libro da un ejemplo extremo: el juego de Go tiene 10¹⁷⁰ estados posibles — muchísimos más que átomos hay en el universo observable). La solución no es agrandar la tabla, es REEMPLAZARLA por una función con unos pocos parámetros ajustables, que generaliza incluso a estados que nunca visitó.<br><br>En el código: <code>Q_tabla</code> (lo que aprendió Q-learning en el tema anterior) tiene 4 entradas EXACTAS, una por estado: -2,71, -1,9, -1,0 y 0,0 — funciona porque solo hay 4 estados. Pero si el corredor tuviera 1000 posiciones posibles en vez de 4, la tabla necesitaría 1000 números guardados. En cambio, aproximando Q(s) con la función lineal más simple que existe, <code>Q_aprox(s) = w·s + b</code>, solo hacen falta 2 números (w y b) — sin importar si el estado tiene 4, 1000 o infinitos valores posibles. Ajustando w y b con el MISMO tipo de corrección por diferencia temporal que usó Q-learning (pero corrigiendo los PARÁMETROS de la función en vez de una casilla de tabla), después de solo 40 episodios la función aprende Q_aprox(0)=-2,677, Q_aprox(1)=-1,838, Q_aprox(2)=-1,0 — muy cerca de los valores EXACTOS de la tabla (-2,71, -1,9, -1,0), con un error cuadrático medio de apenas 0,0016, usando 500 veces MENOS parámetros que una tabla de 1000 estados.<br><br>📐 <b>Referencia formal</b> (Kelleher, Sec.12.1-12.2, pág.229-230): «storing the Q values in a table may be infeasible when the state or action spaces are very large or when they are continuous… the game of Go consists of 10¹⁷⁰ states». La solución es aproximar $Q_\\theta(s,a) \\approx Q_\\pi(s,a)$ con una función de parámetros $\\theta$, ajustados por descenso del gradiente: $\\Delta\\theta = \\alpha\\big(r + \\gamma\\max_{a'}Q_\\theta(s',a') - Q_\\theta(s,a)\\big)\\nabla_\\theta Q_\\theta(s,a)$ (Ec.12.14).",
  "code": "# Cuando la tabla Q ya no alcanza: aproximar Q(s) con una funcion en vez\n# de guardarla EXACTA (Kelleher, Sec 12.1 Introduction, pag.229): \"storing\n# the Q values in a table may be infeasible when the state or action\n# spaces are very large or when they are continuous. For example, the\n# game of Go consists of 10^170 states.\" La solucion (Sec 12.2, pag.230):\n# aproximar Q(s,a) con una funcion de PARAMETROS (una red neuronal en\n# DQN; aca, la mas simple posible: una recta) en vez de una tabla.\nimport numpy as np\n\n# Q_tabla: lo que aprendio Q-learning en el tema anterior, GUARDADO\n# exacto, una entrada por estado -- funciona porque solo hay 4 estados.\nQ_tabla = {0: -2.71, 1: -1.9, 2: -1.0, 3: 0.0}\n\n# si el estado no fueran 4 casillas sino, por ejemplo, 1000 posiciones\n# distintas (o un numero CONTINUO, como en Go: 10^170), una tabla\n# necesitaria 1 entrada POR CADA estado posible:\nn_estados_grande = 1000\nparametros_tabla = n_estados_grande\nparametros_funcion = 2   # w y b -- NO CAMBIA sin importar cuantos estados haya\n\n# mismo corredor de siempre: 0,1,2 intermedios, 3=meta (terminal)\nsiguiente = {0: 1, 1: 2, 2: 3}\nrecompensa = {0: -1, 1: -1, 2: -1}\ngamma = 0.9\nalpha = 0.2\n\n# en vez de una tabla, aproximamos Q(s) = w*s + b (una funcion LINEAL,\n# la mas simple que existe). Actualizacion identica a la Ec.12.14 del\n# libro (semi-gradiente TD): Delta_theta = alpha*(r + gamma*max Q_theta(s')\n# - Q_theta(s)) * grad_theta Q_theta(s); para Q(s)=w*s+b: grad_w=s, grad_b=1\nw, b = 0.0, 0.0\nhistorial_b = []\nfor episodio in range(40):\n    s = 0\n    while s != 3:\n        s2 = siguiente[s]\n        objetivo = recompensa[s] if s2 == 3 else recompensa[s] + gamma * (w * s2 + b)\n        error_td = objetivo - (w * s + b)\n        w, b = w + alpha * error_td * s, b + alpha * error_td\n        s = s2\n    if episodio % 5 == 0:\n        historial_b.append(round(float(b), 3))\nhistorial_b.append(round(float(b), 3))\n\nQ_aprox = {s: round(float(w * s + b), 3) for s in range(4)}\nerror = np.array([Q_tabla[s] - Q_aprox[s] for s in range(3)])\n\nprint(\"Q_tabla (guardada exacta, tema anterior):\", Q_tabla)\nprint(\"Q_aprox (aprendida con SOLO 2 parametros w,b):\", Q_aprox)\nprint(\"w final:\", round(w, 4), \" b final:\", round(b, 4))\nprint(\"Q(0) durante el entrenamiento (cada 5 episodios):\", historial_b)\nprint(\"\\nerror por estado (tabla - funcion), estados 0,1,2:\", [round(float(e), 3) for e in error])\nprint(\"error cuadratico medio:\", round(float(np.mean(error ** 2)), 4))\nprint(\"\\nparametros necesarios con TABLA (1000 estados posibles):\", parametros_tabla)\nprint(\"parametros necesarios con FUNCION (w,b), sin importar cuantos estados haya:\", parametros_funcion)\nprint(\"la funcion usa\", round(parametros_tabla / parametros_funcion), \"veces MENOS parametros\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Tabla · 1000 estados posibles",
     "Función Q(s)=w·s+b"
    ],
    "values": [
     1000,
     2
    ],
    "unit": " parámetros",
    "aria": "Una tabla con 1000 estados posibles necesita 1000 parametros guardados (uno por estado); la funcion lineal Q(s)=w*s+b necesita solo 2 parametros (w y b), sin importar cuantos estados haya"
   }
  },
  "application": "La idea de aproximar Q(s,a) con una función en vez de guardarla en una tabla es exactamente lo que hace posible el Aprendizaje por Refuerzo Profundo (Deep RL): reemplazar la función lineal w·s+b de este ejemplo por una red neuronal profunda (por ejemplo, una CNN) que recibe el estado — los píxeles de una pantalla, la posición de un robot, el tablero de Go — y aproxima Q(s,a) o la política π(a|s) sin necesitar una tabla imposible de guardar. Así funciona DQN (Deep Q-Network, Mnih et al., 2015), que aprendió a jugar decenas de juegos de Atari al nivel humano usando solo los píxeles como entrada; y así funcionan sistemas que, según el propio libro, dominan el ajedrez, Shogi y Go (Silver et al., 2018), alcanzan nivel Gran Maestro en StarCraft II, o controlan un robot cuadrúpedo caminando sobre terreno difícil — en todos los casos, el espacio de estados es demasiado grande para una tabla, y una red neuronal aproxima el valor de cada estado entrenándose por descenso del gradiente (Kelleher, <i>The Science of Deep Learning</i> (Cambridge University Press, 2024), Sec.12.1, pág.229)."
 }
];

/* ──────────── Preguntas de práctica del Modo Maestro RF (superaprendizaje) ────
   Array PARALELO a EX_RF por índice, mismo mecanismo de practice-testing +
   feedback inmediato que AO/Matemáticas/RA/AS -- cada pregunta se fundamenta
   en el propio código/fórmula de ESE tema, verificado ejecutando realmente
   el código antes de fijar la respuesta correcta. */
const RF_QUIZ = [
 [
  {
   "question": "La estrategia GREEDY nunca descubre que el brazo 2 es el mejor (0/80 veces elegido), mientras que ε-greedy sí lo descubre (69/80). ¿Por qué le pasa esto a greedy?",
   "type": "mc",
   "options": [
    "Porque greedy siempre elige el brazo con mejor valor estimado HASTA AHORA, y si ese estimado inicial es engañoso (mala suerte en los primeros intentos), nunca vuelve a probar los otros brazos",
    "Porque greedy tiene un error de programación que lo hace elegir siempre el mismo brazo al azar",
    "Porque el brazo 2 en realidad no es el mejor, y greedy lo detecta correctamente",
    "Porque greedy usa una fórmula distinta para calcular Q(a) que epsilon-greedy"
   ],
   "correct": 0,
   "solution": "Greedy toma siempre argmax Q(a) — el mejor SEGÚN LA EVIDENCIA QUE YA TIENE. Si por mala suerte los primeros intentos con el brazo 2 dieron resultados mediocres, greedy lo descarta y nunca vuelve a probarlo, aunque en realidad (verdaderas_medias=[1.0,1.5,2.0]) sea el mejor de los tres.",
   "whyNot": [
    null,
    "El código de simular() es idéntico para ambas estrategias salvo el parámetro epsilon — no hay ningún error de programación, es el comportamiento matemático esperado de una política puramente greedy.",
    "El código define explícitamente verdaderas_medias=[1.0,1.5,2.0] — el brazo 2 (media 2.0) SÍ es el mejor en realidad; que greedy nunca lo elija es justamente el problema que se está ilustrando, no una detección correcta.",
    "Ambas estrategias usan EXACTAMENTE la misma fórmula de actualización, Q(a) = Q(a) + (r(a)-Q(a))/N(a) — la única diferencia entre greedy y epsilon-greedy es CÓMO ELIGEN la acción (siempre la mejor conocida, vs. 90%/10%), no cómo actualizan el valor."
   ],
   "steps": [
    "Buscá qué hace greedy en cada paso: siempre elige argmax Q(a) — el brazo con mejor valor estimado HASTA AHORA.",
    "Si los primeros intentos con el brazo 2 dieron mala suerte, su Q(2) queda bajo y greedy nunca vuelve a probarlo — no hay ningún mecanismo que lo obligue a reconsiderar.",
    "Los datos verdaderos (verdaderas_medias=[1.0,1.5,2.0]) muestran que el brazo 2 SÍ es el mejor — solo que greedy nunca lo descubre por quedarse pegado a su primera mala impresión.",
    "Por eso 0/80: sin exploración, no hay forma de corregir una mala estimación inicial."
   ],
   "stakes": "Un sistema real de recomendaciones (qué anuncio mostrar, qué producto sugerir) que use una estrategia puramente greedy puede quedarse años mostrando la opción equivocada solo porque tuvo mala suerte los primeros días."
  },
  {
   "question": "Ambas simulaciones (greedy y epsilon-greedy) llaman a simular(epsilon=..., seed=15) usando el MISMO seed=15. ¿Por qué es importante que compartan el mismo seed en esta comparación?",
   "type": "mc",
   "options": [
    "Porque usar el mismo seed hace que ambas simulaciones partan de la misma secuencia de números 'aleatorios', así la diferencia en los resultados (recompensa 85,0 vs 169,2) se debe a la estrategia (epsilon), no a la suerte del azar",
    "Porque sin el mismo seed, el código no podría ejecutarse y arrojaría un error",
    "Porque el mismo seed garantiza que ambas estrategias elijan siempre el mismo brazo en cada paso",
    "Porque el seed determina cuántas veces se puede llamar a la función simular()"
   ],
   "correct": 0,
   "solution": "Usar el mismo seed para ambas llamadas fija la misma secuencia de números pseudoaleatorios subyacente en np.random.default_rng(seed) — así, la única diferencia real entre ambas corridas es el valor de epsilon, no una racha de suerte distinta. Es la forma de aislar la variable que se quiere comparar.",
   "whyNot": [
    null,
    "El código funcionaría perfectamente bien con seeds distintos para cada llamada (por ejemplo, seed=15 y seed=99) — no hay ninguna restricción técnica que exija el mismo seed, es una decisión de diseño para una comparación justa.",
    "Los resultados mismos lo desmienten: aunque comparten seed, Og=0/80 (greedy) y Oe=69/80 (epsilon-greedy) son completamente distintos — el seed fija la secuencia de números aleatorios de fondo, pero epsilon sigue cambiando QUÉ acción se elige en cada paso.",
    "El seed no tiene ninguna relación con cuántas veces se invoca la función — simular() se llama exactamente 2 veces en el código, una por cada estrategia, sin importar qué seed se use."
   ],
   "steps": [
    "Fijate que ambas llamadas a simular() reciben exactamente el mismo argumento seed=15.",
    "Eso significa que rng.random(), rng.integers() y rng.normal() producen, en igualdad de condiciones, la misma secuencia de números 'al azar' en ambas corridas.",
    "Como la única diferencia entre las dos llamadas es el valor de epsilon, cualquier diferencia en el resultado final se puede atribuir con confianza a la estrategia, no al azar."
   ],
   "stakes": "Fijar el mismo seed al comparar dos algoritmos es una práctica estándar en experimentos reales de machine learning — sin ese control, no se puede saber si una diferencia de resultados se debe al algoritmo o simplemente a que le tocó mejor suerte en esa corrida particular."
  }
 ],
 [
  {
   "question": "ε-greedy con ε=0,1 elige una acción al azar el 10% de las veces. ¿Qué función cumple exactamente ese 10% de exploración?",
   "type": "mc",
   "options": [
    "Da la oportunidad de descubrir que un brazo descartado por mala suerte inicial en realidad es mejor de lo que parecía",
    "Reduce a la mitad el tiempo total que tarda en correr la simulación",
    "Garantiza que los 3 brazos se elijan exactamente la misma cantidad de veces",
    "Evita que el código tenga que calcular Q(a) para cada brazo"
   ],
   "correct": 0,
   "solution": "Ese 10% aleatorio es precisamente lo que evita quedarse 'pegado' en una mala decisión temprana: aunque el valor estimado de un brazo sea bajo, sigue teniendo una probabilidad de ser probado de nuevo, dando la chance de corregir una estimación inicial engañosa.",
   "whyNot": [
    null,
    "El código corre exactamente n_pasos=80 iteraciones en ambos casos (greedy y epsilon-greedy) — la exploración no cambia la duración de la simulación, solo QUÉ acción se elige en cada paso.",
    "Los resultados mismos lo desmienten: Ne=[9, 2, 69] muestra un reparto MUY desigual entre los 3 brazos, no una distribución uniforme — ε-greedy sigue explotando el brazo que cree mejor la mayor parte del tiempo.",
    "Q(a) se sigue actualizando para CUALQUIER brazo elegido, sea por exploración o explotación — la fórmula de actualización (Q(a) = Q(a) + (r(a)-Q(a))/N(a)) se aplica siempre después de elegir una acción, cualquiera sea el motivo de la elección."
   ],
   "steps": [
    "Fijate qué hace el código el 10% de las veces: elige una acción AL AZAR, sin importar cuál tenga mejor Q(a) estimado.",
    "Eso significa que incluso un brazo con Q(a) bajo (por mala suerte inicial) sigue teniendo una chance de ser probado de nuevo.",
    "Esa probabilidad constante de volver a probar es justo lo que le falta a greedy — y es lo que le permite a ε-greedy corregir una estimación inicial engañosa."
   ],
   "stakes": "Este es el motivo por el que los sistemas de A/B testing y recomendación reales casi nunca muestran SOLO la opción que 'parece mejor' — sin algo de exploración constante, nunca detectan cuando una opción descartada en realidad era mejor."
  },
  {
   "question": "El array Ne=[9, 2, 69] (mencionado en este mismo tema) muestra cuántas veces epsilon-greedy eligió cada uno de los 3 brazos en 80 pasos. ¿Qué te dice esa distribución sobre el comportamiento real de la política ε-greedy?",
   "type": "mc",
   "options": [
    "Que dedica la mayoría de sus elecciones a explotar el brazo que cree mejor (69 de 80 veces el brazo 2), pero igual reparte una porción menor entre los otros dos (9 y 2 veces) — combina explotación dominante con algo de exploración",
    "Que epsilon-greedy elige los 3 brazos con exactamente la misma frecuencia, en partes iguales",
    "Que epsilon-greedy nunca elige el brazo 0 ni el brazo 1 en ningún paso",
    "Que la distribución prueba que hay un error, porque debería haber elegido cada brazo exactamente 8 veces (10% de 80)"
   ],
   "correct": 0,
   "solution": "9+2+69=80: la mayor parte de las elecciones (69) van al brazo que la política identificó como mejor, mientras que una porción menor (9 y 2) corresponde a la exploración ocasional de los otros dos brazos. Es exactamente la combinación esperada: explotar la mayoría del tiempo, explorar solo una fracción.",
   "whyNot": [
    null,
    "Los números (9, 2, 69) son claramente muy distintos entre sí — no hay ningún reparto equitativo entre los 3 brazos, el brazo 2 concentra la enorme mayoría de las elecciones.",
    "El brazo 0 fue elegido 9 veces y el brazo 1 fue elegido 2 veces — ambos números son mayores a cero, así que sí fueron elegidos, solo que con mucha menos frecuencia que el brazo 2.",
    "El 10% de epsilon es la PROBABILIDAD de explorar en cada paso individual, no una garantía de que cada brazo reciba exactamente 8 exploraciones — una vez que el agente identifica que el brazo 2 es bueno, sigue explotándolo la mayoría del tiempo, y la exploración restante se reparte de forma desigual entre los otros dos por puro azar."
   ],
   "steps": [
    "Sumá los 3 números: 9+2+69=80, coincide con el total de pasos (n_pasos=80).",
    "El brazo 2 (69 veces) concentra la abrumadora mayoría — es el brazo que la política identificó como mejor y explota casi siempre.",
    "Los brazos 0 y 1 (9 y 2 veces) reciben una porción mucho menor, correspondiente a la exploración aleatoria ocasional del 10% de las veces."
   ],
   "stakes": "Este patrón — explotar fuertemente la mejor opción conocida, pero seguir dedicando una fracción chica a explorar — es exactamente el comportamiento que se busca en un sistema real de recomendación: aprovechar lo que funciona sin dejar de revisar ocasionalmente si hay algo mejor."
  }
 ],
 [
  {
   "question": "La fórmula del libro es Q(a) ← Q(a) + (r(a) − Q(a))/N(a). ¿Qué logra dividir por N(a) (el número de veces que se eligió esa acción)?",
   "type": "mc",
   "options": [
    "Que Q(a) termine siendo el PROMEDIO de todas las recompensas recibidas al elegir esa acción, no solo la última recompensa",
    "Que Q(a) se resetee a cero cada N(a) pasos",
    "Que solo se pueda elegir cada acción un máximo de N(a) veces",
    "Que el valor de epsilon disminuya proporcionalmente a N(a)"
   ],
   "correct": 0,
   "solution": "Esta es la fórmula incremental clásica para calcular un promedio: dividir la diferencia (r(a)-Q(a)) por N(a) hace que, con el tiempo, Q(a) converja exactamente al promedio de TODAS las recompensas obtenidas al elegir esa acción — sin necesidad de guardar el historial completo de recompensas.",
   "whyNot": [
    null,
    "Q(a) nunca se resetea en el código — se actualiza incrementalmente en cada paso, acumulando información de todas las veces que se eligió esa acción desde el principio de la simulación.",
    "N(a) es simplemente un contador que crece con cada elección de esa acción — no impone ningún límite máximo de cuántas veces se puede elegir un brazo.",
    "epsilon es un parámetro fijo (0.0 o 0.1 en los dos experimentos) que no cambia durante la simulación — no tiene ninguna relación con N(a), que es un contador independiente por cada brazo."
   ],
   "steps": [
    "Mirá la fórmula: Q(a) ← Q(a) + (r(a) − Q(a))/N(a) — es la forma incremental clásica de calcular un promedio.",
    "Cada vez que se elige la acción, N(a) crece, y el ajuste (r(a)-Q(a))/N(a) se hace cada vez más chico — como agregar un dato más a un promedio ya establecido.",
    "Con el tiempo, ese proceso hace que Q(a) converja al promedio de TODAS las recompensas recibidas, sin necesitar guardar el historial completo."
   ],
   "stakes": "Esta misma fórmula incremental se usa en sistemas reales que necesitan actualizar un promedio sobre millones de eventos sin guardar el historial completo — por ejemplo, el 'rating promedio' de un producto que se actualiza con cada nueva reseña."
  },
  {
   "question": "El código imprime tanto Q estimado (el valor promedio aprendido para cada brazo) como N (cuántas veces se eligió cada brazo). ¿Por qué es importante mostrar también N, y no solo mirar los valores de Q?",
   "type": "mc",
   "options": [
    "Porque N indica cuánta evidencia respalda cada estimación de Q — un Q(a) calculado con N(a) chico se basa en pocas muestras y es menos confiable que uno calculado con N(a) grande, aunque el número final se vea igual de 'seguro'",
    "Porque N determina directamente el valor de epsilon usado en cada simulación",
    "Porque sin N no se podría calcular la recompensa total acumulada",
    "Porque Q y N son en realidad el mismo número, solo que impreso de dos formas distintas"
   ],
   "correct": 0,
   "solution": "La fórmula de actualización divide por N(a): Q(a) = Q(a) + (r(a)-Q(a))/N(a). Eso significa que Q(a) es un promedio de N(a) observaciones — con pocas observaciones (N(a) chico), ese promedio puede ser ruidoso o poco representativo, aunque el número impreso se vea tan 'definitivo' como uno calculado con muchas observaciones.",
   "whyNot": [
    null,
    "epsilon es un parámetro fijo que se pasa directamente a la función simular() (epsilon=0.0 o epsilon=0.1) — no depende de N ni se calcula a partir de los conteos de elección de cada brazo.",
    "recompensa_total se acumula directamente en el bucle con 'recompensa_total += r' en cada paso — no necesita consultar N(a) para nada, se suma independientemente de cuántas veces se haya elegido cada brazo.",
    "Q(a) es el valor promedio ESTIMADO de una acción, mientras que N(a) es un CONTADOR de cuántas veces se eligió — son dos cantidades con significados distintos, por eso el código las imprime por separado."
   ],
   "steps": [
    "Mirá la fórmula de actualización: Q(a) = Q(a) + (r(a)-Q(a))/N(a) — divide por N(a), la cantidad de veces que se eligió esa acción.",
    "Eso hace que Q(a) sea, en el fondo, un promedio de N(a) observaciones.",
    "Un promedio de pocas observaciones (N(a) chico) puede estar lejos del valor real solo por casualidad, mientras que uno de muchas observaciones (N(a) grande) es más confiable — el número de Q solo no distingue entre esos dos casos, pero N sí."
   ],
   "stakes": "Un promedio calculado con pocas muestras (como la calificación de un producto basada en apenas 2 reseñas) puede ser muy engañoso — cualquier sistema real que decide en base a promedios necesita saber también cuántos datos respaldan cada uno."
  }
 ],
 [
  {
   "question": "Si corrieras la simulación con ε=1.0 (siempre elegir al azar, nunca explotar), ¿qué esperarías que pasara con la recompensa total, comparado con ε=0,1?",
   "type": "mc",
   "options": [
    "Sería probablemente menor, porque nunca aprovecharía lo que ya descubrió sobre cuál brazo es mejor, ni siquiera después de encontrarlo",
    "Sería exactamente igual, porque epsilon no afecta el resultado final",
    "Sería mayor, porque explorar siempre garantiza encontrar el mejor brazo más rápido",
    "El código no podría ejecutarse con ε=1.0"
   ],
   "correct": 0,
   "solution": "Con ε=1.0 la elección de acción sería SIEMPRE al azar (rng.random() < 1.0 es siempre verdadero) — el agente nunca 'explotaría' el conocimiento que va acumulando en Q(a), eligiendo brazos subóptimos con la misma frecuencia que el óptimo, incluso después de tener evidencia clara de cuál es mejor.",
   "whyNot": [
    null,
    "Los propios resultados del código YA muestran que epsilon afecta fuertemente el resultado (85,0 vs 169,2 de recompensa total entre ε=0 y ε=0,1, casi el doble) — epsilon determina el balance exploración/explotación, que impacta directamente cuánta recompensa se acumula.",
    "Explorar siempre ayuda a DESCUBRIR cuál es el mejor brazo, pero no ayuda a APROVECHARLO una vez descubierto — con ε=1.0 seguirías eligiendo brazos malos al azar la mayor parte del tiempo, incluso sabiendo cuál es el mejor.",
    "El código funcionaría sin problemas con epsilon=1.0 (rng.random() < 1.0 es una comparación válida) — no hay ninguna restricción técnica que impida usar ese valor."
   ],
   "steps": [
    "Con ε=1.0, la condición rng.random() < 1.0 es siempre verdadera — el agente elige al azar en TODOS los pasos, nunca usa Q(a).",
    "Eso significa que, aunque el agente vaya acumulando evidencia de cuál brazo es mejor, nunca la aprovecha para decidir.",
    "Sigue eligiendo brazos subóptimos con la misma frecuencia que el óptimo, incluso después de tener pruebas claras — por eso la recompensa total esperada sería menor que con ε=0,1."
   ],
   "stakes": "Un sistema real con demasiada exploración (por ejemplo, un A/B test que sigue mostrando variantes perdedoras el 100% del tiempo) desperdicia oportunidades reales de negocio — hay que balancear explorar con aprovechar lo ya aprendido."
  },
  {
   "question": "El código lleva dos métricas separadas por experimento: 'elegido_optimo' (se incrementa solo cuando a==2) y 'recompensa_total' (suma r en cada paso, cualquiera sea el brazo elegido). ¿Qué distingue exactamente a estas dos medidas de desempeño?",
   "type": "mc",
   "options": [
    "'elegido_optimo' cuenta cuántas veces se HIZO la elección objetivamente correcta (el brazo 2, el mejor real), mientras que 'recompensa_total' suma el resultado numérico obtenido en cada paso, sin importar qué brazo se haya elegido — son dos formas distintas de medir el desempeño",
    "Son exactamente la misma medida, solo que expresada con una escala numérica distinta",
    "'elegido_optimo' cuenta cuánto dinero se ganó, y 'recompensa_total' cuenta cuántos brazos hay en total",
    "'recompensa_total' solo se calcula para la estrategia greedy, nunca para epsilon-greedy"
   ],
   "correct": 0,
   "solution": "'elegido_optimo' es un contador de ACIERTOS EN LA DECISIÓN (elegir el brazo 2, que es objetivamente el mejor según verdaderas_medias). 'recompensa_total' es la suma de los valores numéricos r efectivamente recibidos, que dependen tanto del brazo elegido como del resultado aleatorio de cada tirada. Son métricas relacionadas pero no idénticas: se puede elegir bien la mayoría de las veces y aun así tener una racha de mala suerte en los números concretos recibidos, o viceversa.",
   "whyNot": [
    null,
    "elegido_optimo termina en, por ejemplo, 0 o 69 (sobre 80 pasos posibles) mientras que recompensa_total termina en valores como 85,0 o 169,2 — son escalas y significados completamente distintos, no la misma cantidad reexpresada.",
    "elegido_optimo no mide dinero, mide cuántas veces se eligió específicamente el brazo 2 (el mejor conocido según verdaderas_medias); y recompensa_total no cuenta brazos — hay exactamente 3 brazos fijos en todo el experimento (verdaderas_medias tiene 3 elementos), ese número nunca cambia durante la simulación.",
    "El código calcula recompensa_total dentro de la misma función simular(), que se ejecuta una vez para epsilon=0.0 (dando Rg) y otra vez para epsilon=0.1 (dando Re) — ambas estrategias tienen su propia recompensa_total impresa."
   ],
   "steps": [
    "'elegido_optimo' solo se incrementa 'if a==2' — cuenta ACIERTOS en la elección, sin importar qué recompensa numérica se haya recibido ese paso.",
    "'recompensa_total' suma 'r' (la recompensa numérica real) en CADA paso, sin importar si el brazo elegido era el óptimo o no.",
    "Por eso son dos formas distintas de medir desempeño: una mide qué tan seguido se decidió bien, la otra mide cuánto se ganó en números concretos."
   ],
   "stakes": "En sistemas reales de recomendación o publicidad, distinguir 'cuántas veces elegimos la opción objetivamente mejor' de 'cuánto ingreso generamos en total' ayuda a diagnosticar si un mal resultado se debe a decisiones equivocadas o simplemente a mala suerte puntual."
  }
 ],
 [
  {
   "question": "La 'propiedad de Markov' dice que P(s_{t+1}|s_t, a_t) depende SOLO del estado y acción actuales. ¿Qué NO se necesita saber para predecir el siguiente estado del robot?",
   "type": "mc",
   "options": [
    "El camino completo de estados anteriores que el robot recorrió para llegar a su estado actual",
    "El estado actual del robot (caído, de pie o moviéndose)",
    "La acción que el robot decide tomar ahora (lento o rápido)",
    "Las probabilidades de transición definidas en P_lento y P_rapido"
   ],
   "correct": 0,
   "solution": "La propiedad de Markov es exactamente esa: el futuro depende solo del PRESENTE (estado actual + acción elegida), no de la historia completa. Por eso el código solo necesita 's' (el estado actual) y 'a' (la acción) para elegir la fila correcta de la matriz de transición — nunca consulta 'trayectoria' para decidir el siguiente paso.",
   "whyNot": [
    null,
    "El estado actual es EXACTAMENTE lo que sí hace falta — es uno de los dos únicos ingredientes (junto con la acción) que determinan la probabilidad del siguiente estado, según la propia definición de la propiedad de Markov.",
    "La acción elegida también es imprescindible — el código usa P_lento o P_rapido según cuál acción se tomó; sin saber la acción no se podría elegir la matriz de transición correcta.",
    "Las probabilidades de transición (P_lento, P_rapido) son precisamente los datos que definen el proceso de Markov — sin ellas no habría ningún modelo con el cual calcular el siguiente estado."
   ],
   "steps": [
    "La fórmula dice P(s_{t+1}|s_t, a_t) — fijate qué variables aparecen ahí: solo el estado actual y la acción actual.",
    "El 'camino recorrido antes' no aparece en ningún lado de esa fórmula ni en el código (que solo usa 's' y 'a' para elegir la fila de la matriz).",
    "Por eso lo que NO hace falta saber es la trayectoria completa — con el estado y la acción actuales alcanza para predecir el siguiente estado."
   ],
   "stakes": "Esta suposición (que el futuro depende solo del presente, no de toda la historia) es lo que hace viable modelar sistemas reales complejos, como el tráfico o el estado de una máquina, sin necesitar guardar un historial infinito."
  },
  {
   "question": "El comentario en politica_optima dice 'unica forma de levantarse: ir lento'. Según la fila 'caido' de P_rapido ([1, 0, 0]), ¿por qué ir rápido nunca sirve para levantarse estando caído?",
   "type": "mc",
   "options": [
    "Porque la fila 'caido' de P_rapido es [1, 0, 0]: probabilidad 1 de seguir caído y 0 de pasar a cualquier otro estado — ir rápido estando caído no ofrece ninguna posibilidad real de levantarse",
    "Porque yendo rápido, el robot pasa automáticamente a 'moviendose' sin pasar nunca por 'de_pie'",
    "Porque P_rapido no tiene ninguna fila definida para el estado 'caido'",
    "Porque el código tiene un 'if' explícito que prohíbe usar la acción 'rapido' cuando el robot está caído"
   ],
   "correct": 0,
   "solution": "La primera fila de P_rapido (correspondiente a 'caido') es [1, 0, 0]: 100% de probabilidad de seguir caído, 0% de pasar a 'de_pie' o a 'moviendose'. El comentario del código lo confirma: 'caido + rapido -> se queda caido (no puede pararse rapido)'. Por eso la única fila con alguna probabilidad de pasar a 'de_pie' desde 'caido' es la de P_lento.",
   "whyNot": [
    null,
    "Es justo lo contrario: la fila 'caido' de P_rapido es [1, 0, 0] — la probabilidad de pasar a 'moviendose' (o a cualquier otro estado) es exactamente 0, el robot se queda caído con certeza.",
    "P_rapido SÍ tiene una fila definida para 'caido' — es la primera fila de la matriz, [1, 0, 0], la misma que se usa para responder esta pregunta.",
    "No hay ningún 'if' en el código que prohíba explícitamente usar 'rapido' estando caído — politica_optima(s) simplemente elige 'lento' cuando s==0 por diseño de la política, pero nada en las matrices de transición impide técnicamente intentar 'rapido' desde ese estado, solo que sería inútil porque la probabilidad de seguir caído es 1."
   ],
   "steps": [
    "Mirá la primera fila de P_rapido, correspondiente a 'caido': [1, 0, 0].",
    "Esa fila dice: 100% de probabilidad de seguir 'caido', 0% de pasar a cualquier otro estado.",
    "Por eso, sin importar cuántas veces se intente, ir rápido estando caído nunca saca al robot de ese estado — la única fila con alguna probabilidad real de pasar a 'de_pie' es la de P_lento."
   ],
   "stakes": "Diseñar bien la política de un robot real requiere identificar qué acciones son matemáticamente inútiles en cada estado — usar la acción equivocada podría dejarlo atascado indefinidamente en una situación de la que nunca puede salir."
  }
 ],
 [
  {
   "question": "El código verifica que cada fila de P_lento y P_rapido suma exactamente 1 (np.allclose(...sum(axis=1), 1)). ¿Por qué esto es un requisito matemático, no un detalle opcional?",
   "type": "mc",
   "options": [
    "Porque cada fila representa TODAS las probabilidades posibles de a dónde puede ir el robot desde ese estado — y una distribución de probabilidad completa siempre debe sumar 1",
    "Porque los números de la matriz siempre tienen que ser fracciones simples como 3/5 o 2/5",
    "Porque el robot solo puede visitar 3 estados en total durante toda la simulación",
    "Porque np.allclose exige que los valores sean todos positivos"
   ],
   "correct": 0,
   "solution": "Cada fila de la matriz de transición lista la probabilidad de terminar en CADA posible estado siguiente, dado el estado y la acción actuales — como el robot necesariamente termina en ALGÚN estado, esas probabilidades (mutuamente excluyentes y exhaustivas) deben sumar exactamente 1, es una propiedad matemática básica de cualquier distribución de probabilidad.",
   "whyNot": [
    null,
    "No hay ningún requisito de que las probabilidades sean fracciones 'simples' — podrían ser decimales como 0.6 o 0.4173 sin cambiar el requisito matemático de que la fila sume 1; 3/5 y 2/5 son solo los valores concretos de ESTE ejemplo del libro.",
    "Los 3 estados (caído/de_pie/moviendose) son los que aparecen en ESTE ejemplo particular, pero el requisito de que las filas sumen 1 aplicaría igual con cualquier cantidad de estados posibles.",
    "np.allclose solo compara si dos valores son numéricamente iguales (con cierta tolerancia) — no impone ninguna restricción de signo; la verificación aquí es específicamente que la suma dé 1, no que los valores sean positivos."
   ],
   "steps": [
    "Cada fila de P_lento/P_rapido lista la probabilidad de terminar en CADA uno de los estados posibles, dado el estado y la acción actuales.",
    "El robot necesariamente termina en ALGÚN estado — no puede desaparecer ni quedar en dos estados a la vez.",
    "Como esas probabilidades cubren TODOS los resultados posibles y no se solapan, tienen que sumar exactamente 1 — es una propiedad básica de cualquier distribución de probabilidad, no un detalle de implementación."
   ],
   "stakes": "Verificar que las probabilidades de un modelo real sumen exactamente 1 es una comprobación básica de sanidad antes de confiar en cualquier sistema de decisión automatizado basado en probabilidades."
  },
  {
   "question": "Comparando la fila 'moviendose' de P_lento ([0, 0, 1], sigue moviendose con certeza) contra la fila 'moviendose' de P_rapido ([0, 1/5, 4/5], con 1/5 de probabilidad real de caerse), ¿qué trade-off ilustra esta diferencia?",
   "type": "mc",
   "options": [
    "Ir rápido mientras se mueve es más arriesgado (1/5 de probabilidad real de caerse) que ir lento (que garantiza seguir moviéndose sin ningún riesgo de caída) — más velocidad, más riesgo",
    "Son exactamente equivalentes: ambas acciones garantizan seguir moviéndose con certeza total",
    "Ir rápido mientras se mueve es en realidad más seguro que ir lento, porque tiene mayor probabilidad total",
    "La fila de P_rapido para 'moviendose' no suma 1, lo que indica un error en el modelo"
   ],
   "correct": 0,
   "solution": "P_lento en 'moviendose' es [0,0,1]: certeza absoluta de seguir moviéndose, sin ningún riesgo. P_rapido en 'moviendose' es [0,1/5,4/5]: reparte esa probabilidad, dejando un 1/5 real de caerse a cambio de mayor velocidad. Es el trade-off clásico entre ir más rápido y asumir más riesgo.",
   "whyNot": [
    null,
    "No son equivalentes: P_lento da certeza total (probabilidad 1) de seguir moviéndose sin riesgo, mientras que P_rapido introduce un riesgo real y distinto de cero (1/5) de caerse que P_lento no tiene.",
    "'Mayor probabilidad total' no tiene sentido como comparación: ambas filas suman exactamente 1 por ser distribuciones de probabilidad válidas — lo que cambia es CÓMO se reparte esa probabilidad, y P_rapido reparte una parte de ella hacia el riesgo de caída, algo que P_lento no hace.",
    "0 + 1/5 + 4/5 = 1 — la fila suma exactamente 1, no hay ningún error en el modelo."
   ],
   "steps": [
    "Mirá las dos filas 'moviendose': P_lento=[0,0,1], P_rapido=[0,1/5,4/5].",
    "P_lento no tiene ningún riesgo: 100% de probabilidad de seguir moviéndose.",
    "P_rapido en cambio reparte esa probabilidad: 4/5 de seguir moviéndose, pero 1/5 real de caerse — un riesgo que P_lento no tiene.",
    "Esa diferencia ilustra el trade-off clásico entre velocidad y seguridad: ir más rápido acelera el avance pero introduce un riesgo que no existía yendo lento."
   ],
   "stakes": "Este mismo trade-off (velocidad vs. riesgo de caída o falla) aparece en el diseño real de robots móviles y vehículos autónomos, donde aumentar la velocidad casi siempre incrementa la probabilidad de un evento no deseado."
  }
 ],
 [
  {
   "question": "Según las matrices del libro, si el robot está 'de_pie' y elige la acción 'lento', ¿qué pasa con certeza (probabilidad 1)?",
   "type": "mc",
   "options": [
    "Pasa a estar 'moviendose' — es la única transición posible desde ese estado con esa acción",
    "Se cae con toda seguridad",
    "Se queda 'de_pie' para siempre",
    "El resultado es completamente impredecible, sin ninguna probabilidad definida"
   ],
   "correct": 0,
   "solution": "La fila correspondiente a 'de_pie' en P_lento es [0, 0, 1] — probabilidad 0 de seguir de_pie, 0 de caerse, y 1 (certeza total) de pasar a moviendose. El comentario del propio código lo aclara: 'de_pie + lento -> siempre empieza a moverse'.",
   "whyNot": [
    null,
    "La fila de P_lento para 'de_pie' es [0,0,1] — la probabilidad de caerse en esa fila es exactamente 0, no hay ningún riesgo de caída al ir lento estando de pie.",
    "La probabilidad de quedarse de_pie en esa fila también es 0 — yendo lento, el robot SIEMPRE pasa a moviendose, nunca se queda parado.",
    "El resultado es completamente predecible en este caso particular: la fila [0,0,1] asigna probabilidad 1 (certeza) a un único resultado — no hay incertidumbre en esta transición específica, aunque otras transiciones del modelo sí sean probabilísticas."
   ],
   "steps": [
    "Buscá la fila 'de_pie' dentro de la matriz P_lento: [0, 0, 1].",
    "Esos 3 números son las probabilidades de terminar en cada uno de los 3 estados posibles — acá, 0 de seguir de_pie, 0 de caerse, 1 de pasar a moviendose.",
    "Una probabilidad de 1 significa certeza total: con esa acción, desde ese estado, SIEMPRE pasa lo mismo."
   ],
   "stakes": "Modelar correctamente qué transiciones son CIERTAS (probabilidad 1) frente a las inciertas es clave en sistemas reales de control — como saber que cierta acción de un robot SIEMPRE lleva a un estado, sin dejarlo al azar innecesariamente."
  },
  {
   "question": "Fijate en la fila 'de_pie' de P_rapido: [0, 2/5, 3/5] (en el orden de columnas caido, de_pie, moviendose). ¿Qué NO puede pasarle al robot si está 'de_pie' y elige 'rapido', según esta fila?",
   "type": "mc",
   "options": [
    "No puede caerse directamente (la probabilidad de pasar a 'caido' es 0) — desde 'de_pie' yendo rápido, solo puede quedarse de pie (2/5) o empezar a moverse (3/5)",
    "No puede empezar a moverse: solo puede quedarse de pie o caerse",
    "No puede quedarse de pie: tiene que elegir entre caerse o moverse",
    "No puede hacer nada: la fila no define ninguna transición válida"
   ],
   "correct": 0,
   "solution": "La fila 'de_pie' de P_rapido es [0, 2/5, 3/5]: la primera posición (probabilidad de pasar a 'caido') es exactamente 0. Desde 'de_pie' yendo rápido, el robot solo puede terminar 'de_pie' (2/5) o 'moviendose' (3/5) — nunca directamente en 'caido'. El riesgo de caída aparece en otra fila (moviendose+rapido), no en esta.",
   "whyNot": [
    null,
    "La probabilidad de pasar a 'moviendose' es 3/5, un valor claramente distinto de cero — el robot SÍ puede empezar a moverse desde 'de_pie' yendo rápido, de hecho es el resultado más probable.",
    "La probabilidad de quedarse 'de_pie' es 2/5, también distinta de cero — el robot puede perfectamente seguir de pie, no está forzado a elegir entre caerse o moverse.",
    "La fila define una distribución de probabilidad perfectamente válida: 0 + 2/5 + 3/5 = 1, cubre los 3 resultados posibles con sus probabilidades correspondientes."
   ],
   "steps": [
    "La fila 'de_pie' de P_rapido es [0, 2/5, 3/5], en el orden de estados [caido, de_pie, moviendose].",
    "El primer número (probabilidad de pasar a 'caido') es 0 — no hay forma de caerse directamente desde 'de_pie' yendo rápido.",
    "Solo puede pasar a 'de_pie' (quedarse, 2/5) o a 'moviendose' (3/5) — nunca directamente a 'caido' desde ese estado y esa acción."
   ],
   "stakes": "Identificar exactamente desde qué estados existe un riesgo real de caída (y desde cuáles no) es información crítica para diseñar el comportamiento seguro de un robot real."
  }
 ],
 [
  {
   "question": "¿Por qué el modelo del libro define matrices de transición SEPARADAS para la acción 'lento' y para la acción 'rápido'?",
   "type": "mc",
   "options": [
    "Porque la probabilidad de pasar de un estado a otro depende de QUÉ ACCIÓN se elige, no solo del estado actual — cada acción tiene sus propias consecuencias probables",
    "Porque el robot solo puede usar la matriz 'lento' durante la primera mitad de la simulación",
    "Porque las dos matrices en realidad contienen exactamente los mismos números",
    "Porque 'lento' y 'rápido' son simplemente dos nombres distintos para la misma transición"
   ],
   "correct": 0,
   "solution": "La definición formal de un proceso de Markov es T: S × A × S → ℝ — la transición depende tanto del estado COMO de la acción. Por eso el código necesita dos matrices distintas: la probabilidad de caerse yendo rápido (2/5 desde 'de_pie') es distinta de la probabilidad de caerse yendo lento (0, siempre pasa a moviendose) — la acción elegida cambia genuinamente el resultado probable.",
   "whyNot": [
    null,
    "No hay ninguna restricción de 'primera mitad de la simulación' en el código — la política politica_optima(s) puede elegir 'lento' o 'rápido' en cualquier paso, según el estado actual, no según en qué momento de la simulación se está.",
    "Las matrices son claramente distintas: por ejemplo, la fila 'caído' en P_lento es [3/5, 2/5, 0] mientras que en P_rapido es [1, 0, 0] — resultados de probabilidad completamente diferentes según la acción.",
    "Son dos acciones con consecuencias probabilísticas genuinamente distintas (por ejemplo, solo yendo lento el robot puede levantarse estando caído) — no son sinónimos ni producen las mismas transiciones."
   ],
   "steps": [
    "La definición formal de Markov es T: S × A × S → ℝ — la transición depende del estado Y de la acción, no solo del estado.",
    "Compará las dos matrices: la probabilidad de caerse yendo rápido es distinta (2/5) de la probabilidad de caerse yendo lento (0) desde el mismo estado.",
    "Si la acción elegida cambia genuinamente qué tan probable es cada resultado, hace falta una matriz separada por cada acción posible."
   ],
   "stakes": "Ignorar que la acción elegida cambia las probabilidades reales (por ejemplo, en un robot o un vehículo autónomo) llevaría a un modelo que subestima el riesgo de ciertas decisiones — una limitación peligrosa en un sistema de control real."
  },
  {
   "question": "Si el proceso NO tuviera acciones que elegir (fuera un simple proceso de Markov, sin decisiones), ¿cuántas matrices de transición harían falta en vez de las 2 que usa el código (P_lento, P_rapido)?",
   "type": "mc",
   "options": [
    "Solo 1 — sin acciones que elegir, habría una única probabilidad fija de pasar de cada estado a cada otro, sin depender de ninguna decisión",
    "3, una por cada uno de los 3 estados",
    "0, un proceso de Markov sin acciones no necesita ninguna matriz de transición",
    "Seguirían haciendo falta 2, el número de acciones no tiene relación con el número de matrices"
   ],
   "correct": 0,
   "solution": "El código usa 2 matrices exactamente porque hay 2 acciones posibles (lento, rapido) y la transición depende de cuál se elige. Sin ninguna acción que decidir, la probabilidad de pasar de un estado a otro sería fija — solo haría falta 1 matriz P(s'|s), como en una cadena de Markov simple, sin el componente de decisión de un MDP.",
   "whyNot": [
    null,
    "El número de matrices necesarias no está atado al número de estados, sino al número de acciones — una cadena de Markov simple (sin acciones) necesita exactamente 1 matriz de transición, sin importar si tiene 3, 10 o 100 estados.",
    "Un proceso de Markov, con o sin acciones, sigue necesitando modelar transiciones entre estados — 'sin acciones' no significa 'sin transiciones', solo significa que esas transiciones colapsan a una única probabilidad fija por estado en vez de depender de una decisión.",
    "Es exactamente lo opuesto al patrón del código: precisamente PORQUE hay 2 acciones (lento, rapido) hacen falta 2 matrices — el número de matrices escala directamente con el número de acciones disponibles."
   ],
   "steps": [
    "El código usa 2 matrices (P_lento, P_rapido) porque hay 2 acciones posibles a elegir en cada estado.",
    "Sin ninguna acción que decidir, la transición dependería solo del estado actual — habría una única probabilidad fija de pasar de un estado a otro.",
    "Por eso, en un proceso de Markov simple (sin decisiones, sin MDP), solo haría falta 1 matriz de transición, no 2."
   ],
   "stakes": "Esta distinción entre proceso de Markov 'simple' y Proceso de Decisión de Markov (MDP, con acciones) es la que separa un modelo puramente descriptivo (que solo observa) de uno que sirve para tomar decisiones activamente, como el robot de este ejemplo."
  }
 ],
 [
  {
   "question": "Con γ=0, V(estado 0) da exactamente -1. Con γ=1, da exactamente -3. ¿Qué explica esta diferencia tan marcada?",
   "type": "mc",
   "options": [
    "Con γ=0 el agente es completamente miope (solo le importa el premio del próximo paso); con γ=1 suma sin descuento TODOS los pasos futuros hasta la meta (3 pasos, 3 puntos de recompensa)",
    "Es un error de cálculo: ambos deberían dar el mismo resultado, sin importar gamma",
    "γ=1 hace que la función V_horizonte entre en un bucle infinito",
    "γ=0 significa que el agente nunca llega a la meta"
   ],
   "correct": 0,
   "solution": "La propia fórmula lo explica: V^h(s) = R(s,π(s)) + γ·V^{h-1}(s'). Con γ=0, el segundo término se anula completamente — solo queda el reward inmediato (-1). Con γ=1, cada paso futuro se suma SIN descontar, así que los 3 pasos reales que separan al estado 0 de la meta se suman completos: -1-1-1=-3.",
   "whyNot": [
    null,
    "No es un error: γ es precisamente el parámetro que controla cuánto pesa el futuro en el cálculo — es matemáticamente correcto (y esperado) que V(s) cambie según qué tan 'miope' o 'farsighted' sea el agente.",
    "El código usa horizonte h=10 (un número finito de pasos), y la recursión V_horizonte(s,h,gamma) se detiene exactamente cuando h llega a 0 — no hay ningún bucle infinito, sin importar el valor de gamma.",
    "El estado 0 SÍ llega a la meta (a través de 1→2→3, como define el diccionario 'siguiente') — γ no afecta la DINÁMICA del entorno (a dónde se mueve el agente), solo cómo se PESAN los rewards futuros al calcular V(s)."
   ],
   "steps": [
    "Mirá la fórmula: V^h(s) = R(s,π(s)) + γ·V^{h-1}(s') — γ multiplica al valor de los pasos FUTUROS.",
    "Con γ=0, ese segundo término se anula por completo (cualquier cosa por 0 es 0) — solo queda el reward inmediato, -1.",
    "Con γ=1, cada paso futuro se suma SIN descuento — los 3 pasos reales hasta la meta se suman completos: -1-1-1=-3.",
    "La diferencia entre -1 y -3 es exactamente el efecto de 'contar' o no los pasos futuros."
   ],
   "stakes": "Elegir mal gamma en un sistema real (por ejemplo, un algoritmo de trading o de gestión de inventario) determina si el sistema prioriza ganancias inmediatas a costa del largo plazo, o planifica con visión de futuro."
  },
  {
   "question": "El diccionario 'siguiente' define siguiente[3]=3 (el estado meta se apunta a sí mismo) y recompensa[3]=0. Usando horizonte h=10 en vez de los 3 pasos reales que separan al estado 0 de la meta, ¿por qué el resultado de V(0) no se ve afectado por ese horizonte más largo de lo necesario?",
   "type": "mc",
   "options": [
    "Porque al llegar al estado 3 (la meta), el agente se queda ahí para siempre (siguiente[3]=3) recibiendo recompensa 0 en cada paso extra — esos pasos adicionales no suman nada al valor total, así que un horizonte más largo que el necesario no cambia el resultado",
    "Porque V_horizonte() ignora automáticamente cualquier horizonte mayor a 3, sin importar qué número se le pase",
    "Porque gamma multiplicado muchas veces siempre da como resultado exactamente 0, sin importar su valor",
    "Porque el código en realidad usa h=3 en ambos bucles, no h=10 ni h=20"
   ],
   "correct": 0,
   "solution": "Una vez que el estado llega a 3, 'siguiente[3]=3' hace que se quede ahí indefinidamente, y 'recompensa[3]=0' hace que cada paso adicional en ese estado sume exactamente cero al valor acumulado. Por eso, sin importar si el horizonte es 10, 20 o cualquier número mayor a los 3 pasos reales necesarios, los pasos 'extra' después de llegar a la meta no cambian el resultado — solo suman ceros.",
   "whyNot": [
    null,
    "V_horizonte() no ignora nada especial: la función recursiona exactamente 'h' veces, sea cual sea su valor — lo que ocurre es que, una vez en el estado 3, cada recursión adicional suma 0 (la recompensa de ese estado), no que la función 'corte' el horizonte por sí sola.",
    "gamma elevado a una potencia alta tiende a 0 solo si gamma<1, pero eso no es lo que explica este resultado — el motivo real es que la recompensa en el estado meta es directamente 0, así que da igual cuánto se multiplique por gamma: 0 por cualquier número sigue siendo 0.",
    "El código usa claramente h=10 en el primer bucle ('V_horizonte(0, 10, gamma)') y h=20 en el segundo ('V_horizonte(s, 20, 0.9)') — ningún bucle usa h=3."
   ],
   "steps": [
    "Mirá el diccionario 'siguiente': siguiente[3]=3 — al llegar a la meta, el estado se queda apuntando a sí mismo para siempre.",
    "Y 'recompensa[3]=0' — cada paso adicional en la meta suma exactamente 0 al valor acumulado.",
    "Por eso, aunque el horizonte sea 10, 20, o cualquier número mayor a los 3 pasos reales necesarios, los pasos 'extra' después de llegar a la meta no cambian el resultado — solo suman ceros."
   ],
   "stakes": "Diseñar bien el estado terminal (con recompensa 0 y auto-transición) es una práctica estándar en RL real para poder usar un horizonte fijo suficientemente largo sin preocuparse por 'pasarse' de la meta."
  }
 ],
 [
  {
   "question": "Con γ=0,9, los valores por estado son V(0)=-2,71, V(1)=-1,9, V(2)=-1,0, V(3)=0. ¿Qué patrón muestra esta secuencia?",
   "type": "mc",
   "options": [
    "El valor mejora (se acerca a 0) a medida que el estado está más cerca de la meta — tiene sentido, porque hacen falta menos pasos con recompensa -1 para llegar",
    "El valor empeora a medida que el estado está más cerca de la meta",
    "Todos los estados tienen exactamente el mismo valor, sin importar la distancia a la meta",
    "El valor de los estados no tiene ninguna relación con la distancia a la meta"
   ],
   "correct": 0,
   "solution": "Cuantos menos pasos con recompensa -1 falten para llegar a la meta (recompensa 0), menos negativo es el valor acumulado esperado — por eso V(2) (a un solo paso de la meta) es mucho mejor que V(0) (a tres pasos): la función de valor refleja exactamente 'qué tan cerca estás de terminar bien'.",
   "whyNot": [
    null,
    "Es justo lo contrario de lo observado: los números van SUBIENDO (de -2,71 a -1,9 a -1,0 a 0), es decir, MEJORANDO, a medida que el estado se acerca a la meta — no empeorando.",
    "Los 4 valores son claramente distintos entre sí (-2,71, -1,9, -1,0, 0) — no hay ninguna igualdad entre ellos, cada estado tiene un valor propio según su distancia a la meta.",
    "La relación es directa y calculable: cada estado adicional de distancia a la meta agrega aproximadamente un paso más de recompensa -1 (descontada por gamma) al valor total — la distancia SÍ determina el valor."
   ],
   "steps": [
    "Fijate en los 4 valores en orden: V(0)=-2,71, V(1)=-1,9, V(2)=-1,0, V(3)=0 — van subiendo (acercándose a 0) a medida que el estado se acerca a la meta.",
    "Cada paso hasta la meta suma una recompensa de -1 — cuantos menos pasos falten, menos negativos se acumulan.",
    "Por eso el estado más cercano a la meta (2) tiene mejor valor que el más lejano (0): el valor refleja qué tan cerca está de terminar bien."
   ],
   "stakes": "Este patrón (mejor valor cuanto más cerca de la meta) es lo que le permite a un sistema real de navegación o logística decidir qué ruta tomar, incluso sin haber calculado el camino completo de antemano."
  },
  {
   "question": "El código calcula V(estado 0) dos veces con gamma=0,9: una con horizonte 10 (dentro del primer bucle) y otra con horizonte 20 (dentro del segundo bucle, junto a los demás estados). Ambas dan -2,71. ¿Qué te dice esta coincidencia?",
   "type": "mc",
   "options": [
    "Que aumentar el horizonte más allá de cierto punto ya no cambia el resultado — la serie de recompensas descontadas ya convergió, así que agregar más pasos futuros (de 10 a 20) no aporta un valor adicional significativo",
    "Que hay un error en el código, porque horizontes distintos deberían dar siempre resultados distintos",
    "Que gamma=0,9 hace que el horizonte no tenga ningún efecto en absoluto sobre V(s)",
    "Que el estado 0 y el estado 3 (la meta) tienen exactamente el mismo valor"
   ],
   "correct": 0,
   "solution": "Con gamma=0,9 (menor a 1), cada paso adicional de horizonte se multiplica por una potencia cada vez más chica de 0,9 — su aporte al valor total se hace casi nulo. Por eso, una vez que el horizonte es 'suficientemente largo' (acá, 10 ya alcanza), agregar más pasos (hasta 20) no cambia el resultado redondeado: la suma ya convergió.",
   "whyNot": [
    null,
    "No es un error: con gamma<1 la serie de recompensas descontadas converge matemáticamente, así que es esperable (no un bug) que horizontes suficientemente largos den el mismo resultado redondeado — de hecho, esa coincidencia es justamente la evidencia de que la convergencia ya ocurrió.",
    "gamma sí afecta fuertemente a V(s) — comparando con gamma=0 (da -1) y gamma=1 (da -3) del mismo tema, el valor de gamma cambia muchísimo el resultado. Lo que deja de tener efecto, una vez que es suficientemente largo, es el HORIZONTE, no gamma.",
    "El estado 3 (meta) tiene V=0 según el propio listado por estado, un valor claramente distinto de V(0)=-2,71 — no son iguales en absoluto."
   ],
   "steps": [
    "Compará: V(0) con horizonte 10 y gamma=0,9 da -2,71; V(0) con horizonte 20 y el mismo gamma también da -2,71.",
    "Con gamma=0,9 (menor a 1), cada paso adicional se multiplica por una potencia cada vez más chica de 0,9 — su aporte al valor total se vuelve casi nulo.",
    "Por eso, una vez que el horizonte es 'suficientemente largo' (acá, 10 ya alcanza), agregar más pasos (hasta 20) no cambia el resultado redondeado — la suma ya convergió."
   ],
   "stakes": "Saber cuándo un horizonte es 'suficientemente largo' para que el cálculo converja es clave en sistemas reales de planificación — usar un horizonte innecesariamente largo desperdicia cómputo sin mejorar la precisión."
  }
 ],
 [
  {
   "question": "¿Qué representa exactamente 'siguiente' y 'recompensa' en el código, en términos de la teoría de Procesos de Decisión de Markov?",
   "type": "mc",
   "options": [
    "'siguiente' es el modelo de transición (a qué estado se pasa), y 'recompensa' es la función de recompensa R(s,a) para cada estado — juntos definen el entorno del problema",
    "Ambos son simplemente nombres de variables sin ningún significado matemático especial",
    "'siguiente' es la función de valor V(s), y 'recompensa' es la política π",
    "Son dos formas distintas de calcular exactamente lo mismo"
   ],
   "correct": 0,
   "solution": "En el vocabulario formal del capítulo, 'siguiente' codifica el modelo de transición T(s,a,s') (aquí determinístico, un único estado siguiente por cada estado) y 'recompensa' codifica R(s,a) — la recompensa inmediata de estar en ese estado. La función V_horizonte() combina ambos, junto con gamma, siguiendo exactamente la Ecuación 11.12 del libro.",
   "whyNot": [
    null,
    "Sí tienen un significado matemático preciso: son las piezas mínimas necesarias (transición + recompensa) para poder calcular la función de valor V(s) con la fórmula recursiva del libro — no son solo nombres arbitrarios.",
    "La función de valor V(s) es justamente lo que V_horizonte() CALCULA usando 'siguiente' y 'recompensa' como ingredientes — no son la política π, que sería una regla de qué acción tomar en cada estado (aquí la política está implícita: siempre avanzar).",
    "'siguiente' (a dónde se va) y 'recompensa' (qué premio se recibe) son conceptualmente distintos y cumplen roles diferentes en la fórmula V^h(s) = R(s,π(s)) + γ·V^{h-1}(s') — no calculan lo mismo."
   ],
   "steps": [
    "Pensá qué necesita saber cualquier MDP para funcionar: a qué estado se pasa (transición) y qué recompensa se recibe (recompensa) en cada estado.",
    "'siguiente' en el código cumple exactamente el primer rol: da el estado al que se pasa desde cada estado.",
    "'recompensa' cumple el segundo: da el valor inmediato de estar en cada estado.",
    "Juntos, esos dos elementos son lo que V_horizonte() combina, siguiendo la Ecuación 11.12 del libro."
   ],
   "stakes": "Distinguir claramente el modelo de transición de la función de recompensa es esencial al diseñar cualquier sistema real de RL — confundirlos es una fuente común de bugs al programar un nuevo entorno de simulación."
  },
  {
   "question": "En la función V_horizonte(s, h, gamma), el caso base es 'if h == 0: return 0.0'. ¿Qué representa exactamente este caso base en términos del problema?",
   "type": "mc",
   "options": [
    "Que, si no queda ningún paso más de horizonte por considerar, el valor adicional que se puede sumar es cero — es el punto donde la recursión se detiene y deja de sumar recompensas futuras",
    "Que el estado 0 (el primer estado del corredor) siempre tiene valor 0",
    "Que gamma siempre vale 0 en la primera llamada a la función",
    "Que la recompensa recibida en el primer paso del corredor siempre es 0"
   ],
   "correct": 0,
   "solution": "El caso base se activa cuando el parámetro 'h' (horizonte restante, no el estado) llega a 0 — en ese punto la función deja de sumar más términos y devuelve 0, indicando que ya no hay más valor 'adicional' que agregar más allá del horizonte considerado. Es el punto de corte que detiene la recursión.",
   "whyNot": [
    null,
    "'h' es el parámetro de horizonte (pasos restantes), completamente distinto del parámetro 's' (el estado) — el estado 0 en realidad tiene un valor de -2,71 con gamma=0,9, no 0.",
    "gamma no se pone en 0 en ningún momento del caso base — gamma mantiene el valor que se le pasó a toda la llamada (por ejemplo, 0,9); lo que llega a 0 es el contador de horizonte 'h', un parámetro distinto.",
    "recompensa[0] es -1, no 0, según el diccionario 'recompensa' — el valor de retorno 0.0 del caso base pertenece al corte de la recursión, no a la recompensa de ningún estado en particular."
   ],
   "steps": [
    "El caso base 'if h == 0: return 0.0' se dispara cuando ya no queda ningún paso de horizonte por mirar hacia el futuro.",
    "En ese punto, la función deja de sumar más términos: retorna 0, indicando que no hay más valor 'adicional' que agregar más allá del horizonte considerado.",
    "Es el punto de corte de la recursión — sin él, V_horizonte() llamaría a sí misma indefinidamente."
   ],
   "stakes": "Definir correctamente el caso base de una recursión (cuándo parar y qué devolver) es una de las decisiones más importantes al implementar cualquier algoritmo recursivo real, incluidos los de planificación en aprendizaje por refuerzo."
  }
 ],
 [
  {
   "question": "Si un agente real (por ejemplo, un robot de reparto) tuviera γ muy cercano a 0, ¿qué tipo de decisiones tendería a tomar?",
   "type": "mc",
   "options": [
    "Decisiones que maximizan el beneficio INMEDIATO, sin importarle mucho si eso lo deja en mala posición para el futuro cercano",
    "Decisiones perfectamente equilibradas entre el corto y el largo plazo",
    "El agente directamente no podría tomar ninguna decisión con γ cercano a 0",
    "Decisiones que solo dependen del último estado visitado antes del actual"
   ],
   "correct": 0,
   "solution": "Un γ cercano a 0 hace que los términos futuros del cálculo de V(s) casi desaparezcan (se multiplican por un número casi nulo) — el agente queda efectivamente 'miope', optimizando casi exclusivamente la recompensa del paso inmediato, sin pesar mucho las consecuencias futuras de esa elección.",
   "whyNot": [
    null,
    "Es exactamente lo opuesto a un equilibrio: γ cercano a 0 sesga fuertemente la decisión hacia el corto plazo, casi ignorando el largo plazo — un verdadero equilibrio necesitaría un γ intermedio, no cercano a los extremos.",
    "El agente sigue pudiendo calcular V(s) y tomar decisiones con cualquier valor de gamma entre 0 y 1 — γ cambia QUÉ decisiones resultan óptimas, no si es posible calcular algo en absoluto.",
    "Eso describiría una violación de la propiedad de Markov (depender de estados PASADOS) — gamma no tiene ninguna relación con cuántos estados anteriores se consideran, solo con cuánto pesan los REWARDS FUTUROS en el cálculo de valor."
   ],
   "steps": [
    "Con γ cercano a 0, cualquier término futuro del cálculo de V(s) se multiplica por un número casi nulo — casi desaparece.",
    "Eso significa que, al decidir, el agente prácticamente solo pesa la recompensa del PRÓXIMO paso, no lo que viene después.",
    "Un agente así optimiza el beneficio inmediato sin importarle mucho las consecuencias futuras de esa elección — por eso se dice que es 'miope'."
   ],
   "stakes": "Un agente real con gamma muy bajo (por ejemplo, un bot de trading de alta frecuencia mal configurado) puede tomar decisiones rentables a corto plazo pero desastrosas a mediano plazo, por ignorar sistemáticamente las consecuencias futuras."
  },
  {
   "question": "El código separa el análisis en dos bucles: primero varía gamma (manteniendo el estado fijo en 0, horizonte 10), y después varía el estado (manteniendo gamma fijo en 0,9, horizonte 20). ¿Qué compara exactamente cada una de esas dos partes?",
   "type": "mc",
   "options": [
    "La primera parte aísla el efecto de gamma sobre V(0) (probando distintos gamma con el mismo estado); la segunda aísla el efecto de la posición en el corredor sobre V(s) (probando distintos estados con el mismo gamma) — cada bucle cambia una sola variable a la vez",
    "Ambas partes miden exactamente lo mismo, solo que en distinto orden de ejecución",
    "La primera parte mide el efecto del estado, y la segunda mide el efecto de gamma — al revés de lo que realmente hace el código",
    "La segunda parte recalcula V(0) con un gamma distinto en cada iteración, igual que la primera"
   ],
   "correct": 0,
   "solution": "El primer bucle ('for gamma in [0.0,0.5,0.9,1.0]: V_horizonte(0,10,gamma)') fija el estado en 0 y varía gamma. El segundo ('for s in range(4): V_horizonte(s,20,0.9)') fija gamma en 0,9 y varía el estado. Cada bucle cambia una sola variable, lo que permite atribuir con claridad el efecto observado a esa variable en particular.",
   "whyNot": [
    null,
    "No miden lo mismo: uno cambia gamma con estado fijo, el otro cambia el estado con gamma fijo — son dos comparaciones distintas sobre variables distintas, no la misma repetida.",
    "Es exactamente al revés de lo que hace el código: el primer bucle fija el estado en 0 y varía gamma; el segundo fija gamma en 0,9 y varía el estado 's'.",
    "El segundo bucle usa siempre el mismo gamma=0,9 (un valor fijo, hardcodeado) en cada una de sus 4 iteraciones — solo cambia 's', nunca recalcula con un gamma distinto."
   ],
   "steps": [
    "Mirá el primer bucle: 'for gamma in [0.0,0.5,0.9,1.0]: v0 = V_horizonte(0,10,gamma)' — el estado está fijo en 0, solo gamma cambia.",
    "Mirá el segundo: 'for s in range(4): V_horizonte(s,20,0.9)' — gamma está fijo en 0,9, solo el estado cambia.",
    "Cada bucle aísla una sola variable para poder atribuirle claramente el efecto observado — cambiar solo una cosa a la vez es la forma correcta de comparar."
   ],
   "stakes": "Esta técnica de 'cambiar una sola variable por vez' es el fundamento de cualquier experimento controlado real, sea en ciencia de datos, en un ensayo clínico, o en el ajuste de parámetros de un sistema de aprendizaje por refuerzo."
  }
 ],
 [
  {
   "question": "Q(0,'avanzar') converge a -2,71 tras 60 episodios — exactamente el mismo valor que V(0) del tema anterior, calculado con una fórmula cerrada que SÍ conocía el mapa completo. ¿Qué demuestra esta coincidencia?",
   "type": "mc",
   "options": [
    "Que Q-learning puede aprender el valor correcto de las acciones SOLO por experiencia, sin que nadie le dé de antemano las reglas del entorno (transición y recompensa)",
    "Que Q-learning y la fórmula V(s) del tema anterior son literalmente el mismo código copiado",
    "Que la coincidencia es pura casualidad, sin ninguna relación matemática",
    "Que el corredor de este tema tiene una recompensa distinta al del tema anterior"
   ],
   "correct": 0,
   "solution": "Es el punto central del tema: el agente de Q-learning nunca recibió las fórmulas 'siguiente'/'recompensa' como una fórmula cerrada para calcular directamente — las descubrió muestreando (viviendo el episodio paso a paso) y actualizando Q con la regla TD. Que converja al mismo valor que la solución exacta prueba que el aprendizaje por experiencia funciona.",
   "whyNot": [
    null,
    "El código de Q-learning (bucle while con muestreo y actualización TD) es estructuralmente distinto al de V_horizonte() del tema anterior (una función recursiva con la fórmula cerrada) — no son el mismo código, aunque usen el mismo corredor de ejemplo.",
    "La coincidencia no es azar: es la consecuencia matemática esperada de que la actualización TD, aplicada muchas veces, converge exactamente al valor real bajo la política dada — es un resultado teórico garantizado, no una suerte del ejemplo.",
    "El corredor usa exactamente los mismos diccionarios 'siguiente' y 'recompensa' que el tema anterior (mismos valores: -1 por paso, 0 en la meta) — es intencional, para poder comparar ambos métodos sobre el mismo problema."
   ],
   "steps": [
    "Recordá cómo se calculó V(0) en el tema anterior: con una fórmula cerrada que YA conocía 'siguiente' y 'recompensa' de antemano.",
    "Acá, en cambio, el agente de Q-learning nunca recibió esas fórmulas — solo vivió episodios paso a paso y fue actualizando Q con la regla TD, por experiencia.",
    "Que ambos caminos (fórmula exacta vs. prueba y error) lleguen al MISMO número (-2,71) demuestra que aprender por experiencia realmente puede encontrar el valor correcto, sin que nadie le dé las reglas del entorno."
   ],
   "stakes": "Esta validación (aprender por experiencia da el mismo resultado que la solución exacta) es la que da confianza para usar RL en sistemas reales donde el modelo del entorno NO se conoce de antemano, como un robot en un entorno nuevo."
  },
  {
   "question": "El código define acciones=['avanzar'] — solo hay UNA acción posible en cada estado. Aun así, la actualización usa mejor_siguiente = max(Q[s2].values()). ¿Por qué usar max() si de todos modos solo hay un valor en Q[s2]?",
   "type": "mc",
   "options": [
    "Porque la fórmula general de Q-learning siempre toma el MEJOR valor entre todas las acciones posibles del siguiente estado — con una sola acción disponible, max() simplemente devuelve ese único valor, pero el código sigue la fórmula general tal cual está definida para cualquier cantidad de acciones",
    "Porque max() en este caso siempre devuelve 0, sin importar los valores de Q",
    "Porque sin max(), el código no podría ejecutarse por un error de sintaxis",
    "Porque max() elige aleatoriamente entre las acciones disponibles en cada paso"
   ],
   "correct": 0,
   "solution": "La fórmula general de Q-learning es Q(s,a) <- Q(s,a) + alpha*(r + gamma*max_a' Q(s',a') - Q(s,a)) — siempre toma el máximo sobre todas las acciones posibles del estado siguiente. Con acciones=['avanzar'] hay una sola acción disponible, así que max() sobre un diccionario de un solo valor simplemente devuelve ese valor — el código no necesita un caso especial, la fórmula general ya lo cubre naturalmente.",
   "whyNot": [
    null,
    "max() devuelve el valor real almacenado en Q[s2]['avanzar'], que va cambiando a lo largo del entrenamiento (empieza en 0.0 y se va ajustando episodio a episodio hasta converger) — no es siempre 0.",
    "max() sobre un diccionario con una sola clave ('avanzar') es una operación perfectamente válida en Python, no genera ningún error de sintaxis ni de ejecución.",
    "max() es una función determinística que siempre elige el valor más grande entre los disponibles — no involucra ninguna aleatoriedad; con una sola acción, simplemente devuelve el único valor que hay."
   ],
   "steps": [
    "Mirá acciones=['avanzar'] — hay una sola acción posible en todo el problema.",
    "La fórmula general de Q-learning, Q(s,a) <- ... + gamma*max_a' Q(s',a'), siempre toma el máximo sobre TODAS las acciones del siguiente estado, sea cuantas sean.",
    "Con una sola acción disponible, max() sobre un solo valor simplemente devuelve ese valor — el código no necesita un caso especial, la fórmula general ya lo cubre naturalmente."
   ],
   "stakes": "Escribir el código siguiendo la fórmula general (en vez de simplificarla a mano para este caso particular de una sola acción) hace que sea trivial extenderlo después a un problema con múltiples acciones reales, sin tener que reescribir la lógica central."
  }
 ],
 [
  {
   "question": "La fórmula de actualización es Q(s,a) ← Q(s,a) + α(r + γ·max Q(s',a') − Q(s,a)). ¿Qué representa el término entre paréntesis (r + γ·max Q(s',a') − Q(s,a))?",
   "type": "mc",
   "options": [
    "El 'error TD': la diferencia entre lo que el agente creía que valía esa acción y lo que acaba de observar que realmente vale",
    "El número total de episodios que se van a entrenar",
    "La probabilidad de que la acción elegida sea la correcta",
    "El tiempo en segundos que tarda en ejecutarse cada episodio"
   ],
   "correct": 0,
   "solution": "r + γ·max Q(s',a') es la nueva estimación 'observada' (recompensa real más el valor descontado del mejor siguiente estado); restarle Q(s,a) (la estimación VIEJA) da exactamente cuánto se equivocaba la estimación anterior — ese es el error de diferencia temporal (TD), la señal de aprendizaje.",
   "whyNot": [
    null,
    "El número de episodios es el parámetro 'range(60)' del bucle externo, algo completamente distinto y fijado de antemano — no tiene relación con el cálculo del error TD dentro de cada paso.",
    "Q-learning en este ejemplo tiene una sola acción posible ('avanzar'), así que no hay ninguna noción de 'probabilidad de acierto' en juego — el error TD mide una diferencia de VALOR estimado, no una probabilidad.",
    "El tiempo de ejecución es una propiedad del hardware y del intérprete, no un valor que aparezca en la fórmula matemática de Q-learning — la fórmula solo involucra recompensas y valores Q, no tiempos de cómputo."
   ],
   "steps": [
    "Separá la fórmula en dos partes: r + γ·max Q(s',a') es lo que el agente ACABA de observar que vale esa acción.",
    "Q(s,a) (lo que se resta) es lo que el agente CREÍA que valía, antes de esta observación.",
    "La diferencia entre 'lo que acabo de ver' y 'lo que creía' es exactamente el error de estimación — el error TD, la señal que usa para corregirse."
   ],
   "stakes": "El error TD es literalmente la señal de entrenamiento que usan sistemas reales como los que juegan videojuegos o controlan robots — sin ese cálculo de 'cuánto me equivoqué', no hay forma de que el agente mejore con la experiencia."
  },
  {
   "question": "El código usa alpha=0.5 (la 'tasa de aprendizaje') en la fórmula Q(s,a) <- Q(s,a) + alpha*(r + gamma*max Q(s',a') - Q(s,a)). ¿Qué controla exactamente el valor de alpha en esa actualización?",
   "type": "mc",
   "options": [
    "Qué tan grande es el 'salto' que da Q(s,a) hacia la nueva estimación en cada actualización — un alpha más alto corrige más agresivamente en cada paso, uno más bajo corrige más gradualmente",
    "Cuántos episodios en total se van a entrenar",
    "El factor de descuento aplicado a las recompensas futuras",
    "La probabilidad de explorar una acción distinta a 'avanzar' en vez de explotar la conocida"
   ],
   "correct": 0,
   "solution": "El término entre paréntesis (r + gamma*max Q(s',a') - Q(s,a)) es el error TD. alpha multiplica ese error antes de sumarlo a Q(s,a) — un alpha=0,5 aplica la mitad de la corrección completa en cada actualización, ni ignora el error (alpha=0) ni lo aplica entero de una sola vez (alpha=1).",
   "whyNot": [
    null,
    "El número de episodios está controlado por 'range(60)' en el bucle externo de entrenamiento — es un parámetro completamente distinto de alpha, sin relación entre ambos.",
    "El factor de descuento es gamma (=0.9 en este código), una variable separada de alpha que aparece en un lugar distinto de la fórmula (multiplicando a max Q(s',a'), no al error completo).",
    "En este código no hay ningún mecanismo de exploración: acciones=['avanzar'] significa que hay una sola acción posible en cada paso, así que no existe elección entre 'explotar' o 'explorar' — alpha no tiene ninguna relación con eso."
   ],
   "steps": [
    "Mirá la fórmula: Q(s,a) <- Q(s,a) + alpha*(r + gamma*max Q(s',a') - Q(s,a)).",
    "El término entre paréntesis es el error TD — cuánto se equivocaba la estimación anterior.",
    "alpha multiplica ese error antes de sumarlo — un alpha=0,5 aplica la mitad de la corrección completa en cada paso, ni ignora el error (alpha=0) ni lo aplica entero de una vez (alpha=1)."
   ],
   "stakes": "Elegir mal la tasa de aprendizaje en un sistema real de machine learning (muy alta: inestable y oscila; muy baja: aprende demasiado lento) es uno de los errores de configuración más comunes al entrenar cualquier modelo, no solo en aprendizaje por refuerzo."
  }
 ],
 [
  {
   "question": "¿Cuál es la diferencia clave entre 'planning' (el tema anterior, V(s) con fórmula cerrada) y 'reinforcement learning' real (este tema, Q-learning)?",
   "type": "mc",
   "options": [
    "En planning el agente CONOCE de antemano la función de transición y recompensa del entorno; en RL real el agente NO las conoce y tiene que descubrirlas muestreando",
    "Planning usa Python y RL real usa otro lenguaje de programación",
    "Planning solo funciona con 1 estado; RL real funciona con cualquier cantidad",
    "No hay ninguna diferencia real entre ambos, son dos nombres para lo mismo"
   ],
   "correct": 0,
   "solution": "Es exactamente la distinción que hace el propio capítulo del libro: planning asume un MDP conocido (transición y recompensa dadas, como en V_horizonte() del tema anterior); reinforcement learning asume que esas funciones son DESCONOCIDAS, y el agente debe aprenderlas interactuando con el entorno — como hace Q-learning en este código.",
   "whyNot": [
    null,
    "Ambos temas están escritos en Python, ejecutados por el mismo intérprete de esta app — el lenguaje de programación no tiene ninguna relación con la distinción conceptual entre planning y RL.",
    "El corredor de este ejemplo tiene 4 estados en ambos temas (planning y Q-learning) — la cantidad de estados no es lo que distingue a uno del otro, ambos podrían aplicarse a problemas de cualquier tamaño.",
    "Sí hay una diferencia real y central, es el tema completo de esta comparación: si el agente conoce o no de antemano cómo funciona el entorno determina si el problema es de planning o de aprendizaje por refuerzo genuino."
   ],
   "steps": [
    "En el tema anterior (V_horizonte), el código YA tenía 'siguiente' y 'recompensa' como datos conocidos de entrada — el entorno estaba dado.",
    "Acá, Q-learning nunca recibe esas funciones directamente — el agente tiene que descubrir cómo se comporta el entorno viviendo episodios.",
    "Esa es la distinción central: planning asume un modelo del entorno conocido; RL real asume que hay que aprenderlo interactuando."
   ],
   "stakes": "Esta distinción determina qué algoritmo usar en un proyecto real: si se conocen las reglas del entorno (como en un juego de mesa), planning alcanza; si no se conocen (como el comportamiento real de usuarios), hace falta RL genuino."
  },
  {
   "question": "El código sigue usando los diccionarios 'siguiente' y 'recompensa' directamente (s2 = siguiente[s], r = recompensa[s]), igual que en el tema de la función de valor V(s). Si la idea central de Q-learning es que el agente 'no conoce' el entorno de antemano, ¿cómo se explica que el código los use así?",
   "type": "mc",
   "options": [
    "'siguiente' y 'recompensa' aquí representan el ENTORNO REAL (lo que efectivamente pasa cuando se actúa) — el propio comentario del código aclara que el agente 'MUESTREA esto, no lo sabia antes': lo descubre paso a paso viviendo episodios, nunca los consulta como fórmula para planear de antemano, a diferencia de V_horizonte() del tema anterior",
    "Es una contradicción real: el código tiene un error, no debería usar esos diccionarios en absoluto",
    "'siguiente' y 'recompensa' aquí tienen valores completamente distintos a los del tema de la función de valor V(s)",
    "El agente sí conoce por completo el entorno en este tema, exactamente igual que en el tema anterior — no hay ninguna diferencia real entre ambos"
   ],
   "correct": 0,
   "solution": "El comentario del propio código lo aclara: 's2 = siguiente[s] # el agente MUESTREA esto, no lo sabia antes'. Esos diccionarios representan lo que realmente ocurre en el entorno cuando se actúa, pero el agente de Q-learning solo accede a ese resultado paso a paso (viviendo el episodio), nunca los usa como fórmula cerrada para planificar sin haber actuado — que es justo lo que sí hacía V_horizonte() en el tema anterior.",
   "whyNot": [
    null,
    "No es un error: toda simulación necesita código que determine 'qué pasa realmente' cuando el agente actúa (el entorno real) — eso es distinto de que el AGENTE tenga acceso a esa función para planificar de antemano, que es lo que sí ocurría en V_horizonte().",
    "El código usa exactamente los mismos valores que el tema anterior (siguiente={0:1,1:2,2:3,3:3}, recompensa={0:-1,1:-1,2:-1,3:0}) — mismo corredor, mismos números, de forma intencional para poder comparar ambos métodos.",
    "El comentario del propio código lo desmiente: 'el agente MUESTREA esto, no lo sabia antes' — el agente descubre el resultado paso a paso viviendo episodios, nunca usa esos diccionarios como fórmula cerrada para planificar de antemano, como sí hacía V_horizonte()."
   ],
   "steps": [
    "En V_horizonte() (tema anterior), la función que calcula V accedía directamente a 'siguiente' y 'recompensa' como fórmulas conocidas para planificar sin haber actuado nunca.",
    "Acá, esos mismos diccionarios representan la 'verdad' del entorno — lo que efectivamente pasa — pero el agente de Q-learning solo los toca indirectamente, viviendo un paso a la vez y observando (r, s2) como resultado de haber actuado.",
    "El código necesita simular el entorno real de alguna forma (por eso usa los diccionarios), pero el AGENTE nunca los consulta como fórmula cerrada para planear — solo reacciona a lo que observa paso a paso."
   ],
   "stakes": "Esta distinción entre simular el entorno real y dar al agente acceso directo a sus reglas es exactamente la misma que separa un simulador de entrenamiento (que sí conoce las reglas del mundo, para poder simularlo) del agente que se entrena en él sin tener acceso a esas reglas — como pasa en la práctica con simuladores de robots o videojuegos usados para entrenar RL."
  }
 ],
 [
  {
   "question": "Si el corredor tuviera 10 estados en vez de 4 (mismo patrón, más pasos hasta la meta), ¿qué esperarías que le pasara a Q-learning para converger al valor correcto?",
   "type": "mc",
   "options": [
    "Necesitaría más episodios de experiencia para que la información de la recompensa final se propague, paso a paso, hacia atrás hasta los estados más lejanos",
    "Convergería instantáneamente en 1 solo episodio, sin importar la distancia a la meta",
    "Dejaría de funcionar por completo con más de 4 estados",
    "El valor de alpha tendría que volverse negativo para que funcione"
   ],
   "correct": 0,
   "solution": "La actualización TD propaga información de a un paso por episodio: recién cuando el agente llega a la meta (o cerca de ella) esa señal 'viaja hacia atrás' a los estados anteriores en episodios sucesivos. Con más estados entre el inicio y la meta, hacen falta más episodios para que la señal recorra todo el camino y los valores Q converjan a lo largo de todo el corredor.",
   "whyNot": [
    null,
    "La convergencia de Q-learning es progresiva, no instantánea — el propio código muestra a Q(0,'avanzar') tardando varios episodios en estabilizarse (de -0,5 en el episodio 10 a -2,71 recién más adelante), y esa demora crecería con más estados, no desaparecería.",
    "Q-learning es un algoritmo general que funciona con cualquier cantidad de estados (de hecho se usa en problemas con miles o millones de estados, como en juegos de Atari) — no hay ningún límite de 4 estados en la definición del algoritmo.",
    "alpha (la tasa de aprendizaje) siempre es un valor positivo entre 0 y 1 por definición — un alpha negativo invertiría la dirección de la corrección y rompería la convergencia, no es lo que se necesitaría para más estados."
   ],
   "steps": [
    "La actualización TD solo mueve la información un paso hacia atrás por episodio — recién cuando el agente llega cerca de la meta esa señal empieza a viajar hacia atrás.",
    "Con 4 estados, esa señal tarda pocos episodios en llegar hasta el estado inicial.",
    "Con 10 estados, el camino hasta la meta es más largo — la misma señal necesita más episodios sucesivos para propagarse paso a paso hasta los estados más lejanos."
   ],
   "stakes": "Subestimar cuántos episodios hacen falta para un entorno real más grande es un error común de planificación de proyecto — un sistema de RL que funcionó bien en una simulación chica puede necesitar mucho más entrenamiento en el entorno real."
  },
  {
   "question": "El bucle interno del entrenamiento usa 'while s != 3', y cada episodio arranca siempre en 's = 0'. ¿Qué garantiza exactamente esta condición en cada uno de los 60 episodios?",
   "type": "mc",
   "options": [
    "Que el episodio recorre el corredor completo, paso a paso, actualizando Q en cada estado (0, 1, 2) hasta llegar exactamente al estado meta (3), donde el bucle se detiene",
    "Que el episodio se repite exactamente 60 veces dentro de un mismo 'while'",
    "Que la variable 's' nunca puede tomar el valor 0 durante el entrenamiento",
    "Que el agente puede terminar el episodio en cualquier estado, no necesariamente en la meta"
   ],
   "correct": 0,
   "solution": "'s = 0' arranca cada episodio en el estado inicial, y 'while s != 3' sigue ejecutando pasos mientras el estado no sea la meta, deteniéndose solo cuando s llega exactamente a 3. Eso garantiza que cada episodio completo recorre el corredor entero, actualizando Q en cada paso intermedio, hasta llegar a la meta.",
   "whyNot": [
    null,
    "60 es el número de repeticiones del bucle EXTERNO ('for episodio in range(60)'), algo distinto del bucle 'while' interno, que se ejecuta una vez por cada PASO dentro de un mismo episodio hasta llegar a la meta.",
    "'s' arranca EXACTAMENTE en 0 al inicio de cada episodio ('s = 0' justo después de 'for episodio in range(60):') — 0 es precisamente el valor inicial de cada episodio, no un valor excluido.",
    "'while s != 3' significa que el bucle sigue ejecutándose MIENTRAS s no sea la meta — solo puede salir del bucle cuando s se vuelve exactamente 3, así que cada episodio necesariamente termina en el estado meta, nunca en otro."
   ],
   "steps": [
    "Mirá el código: 's = 0' arranca cada episodio en el estado inicial.",
    "'while s != 3' sigue ejecutando pasos MIENTRAS el estado no sea la meta — solo se detiene cuando s llega a 3.",
    "Eso garantiza que cada episodio completo recorre el corredor entero, actualizando Q en cada paso intermedio, hasta llegar exactamente a la meta."
   ],
   "stakes": "Definir bien la condición de fin de episodio (llegar a un estado terminal) es fundamental en cualquier sistema real de aprendizaje por refuerzo episódico — un simulador de entrenamiento mal definido podría dejar episodios corriendo indefinidamente o terminarlos antes de tiempo."
  }
 ],
 [
  {
   "question": "El libro dice que guardar Q(s,a) en una tabla \"puede ser inviable cuando el espacio de estados o acciones es muy grande o continuo\", y da el ejemplo de Go (10¹⁷⁰ estados). ¿Por qué es exactamente ese el problema?",
   "type": "mc",
   "options": [
    "Porque una tabla necesita UNA casilla guardada por cada estado (o par estado-acción) posible, y si hay millones o 10¹⁷⁰ estados posibles, no existe memoria física suficiente para guardarlos todos",
    "Porque la fórmula de Q-learning (Q(s,a) ← Q(s,a) + α(r + γ·max Q(s',a') − Q(s,a))) deja de ser matemáticamente válida cuando hay muchos estados",
    "Porque con muchos estados el agente tarda más en jugar cada partida, no porque haya un problema de memoria",
    "Porque el juego de Go en realidad no se puede resolver con aprendizaje por refuerzo, tabla o función"
   ],
   "correct": 0,
   "solution": "El problema es puramente de ALMACENAMIENTO: una tabla Q(s,a) reserva una casilla distinta por cada combinación posible de estado y acción. Con 10¹⁷⁰ estados (más que átomos en el universo observable) esa tabla nunca podría existir físicamente, sin importar cuánta memoria se tenga. La fórmula de Q-learning en sí sigue siendo válida — lo que deja de ser viable es GUARDARLA en una tabla exacta.",
   "whyNot": [
    null,
    "La fórmula de actualización de Q-learning (Q(s,a) ← Q(s,a) + α(r + γ·max Q(s',a') − Q(s,a))) sigue siendo matemáticamente correcta sin importar cuántos estados haya — el problema no es la fórmula, es DÓNDE guardar los valores que esa fórmula calcula.",
    "El código de este tema no mide tiempo de ejecución en absoluto — el problema que ilustra es que 1000 (o 10¹⁷⁰) números NO ENTRAN en una tabla, no que tardar más en calcularlos.",
    "El propio libro describe sistemas reales que SÍ resuelven Go con aprendizaje por refuerzo (AlphaGo, Silver et al., 2018) — la solución no es abandonar el problema, es aproximar Q(s,a) con una función en vez de una tabla."
   ],
   "steps": [
    "Una tabla Q(s,a) necesita reservar una casilla de memoria distinta por cada combinación posible de estado y acción.",
    "Con 10¹⁷⁰ estados posibles (como en Go), esa cantidad de casillas supera ampliamente cualquier memoria física disponible, sin importar qué tan grande sea.",
    "El problema no es que la fórmula de Q-learning deje de funcionar — es puramente que no hay dónde guardar una tabla de ese tamaño."
   ],
   "stakes": "Esta limitación de memoria es exactamente por qué ningún sistema real de RL a gran escala (un auto autónomo, un agente que juega Go o Atari) usa una tabla Q — es la razón práctica detrás de toda la aproximación de funciones moderna."
  },
  {
   "question": "El código imprime 'la funcion usa 500 veces MENOS parametros' (parametros_tabla=1000 dividido parametros_funcion=2). Si en vez de 1000 estados el problema tuviera 10.000, sabiendo que parametros_funcion sigue siendo 2, ¿qué pasaría con esa razón?",
   "type": "mc",
   "options": [
    "La razón crecería a 5000 veces menos — parametros_funcion se queda fijo en 2 sin importar cuántos estados haya, mientras que parametros_tabla crece proporcionalmente al número de estados",
    "La razón se mantendría exactamente en 500, sin cambiar",
    "La razón bajaría, porque más estados significa que la función también necesitaría más parámetros",
    "parametros_funcion tendría que aumentar a 20 para poder representar 10 veces más estados"
   ],
   "correct": 0,
   "solution": "parametros_tabla = n_estados_grande, así que crece exactamente igual que la cantidad de estados. parametros_funcion=2 es un número fijo en el código, marcado explícitamente como que 'NO CAMBIA sin importar cuantos estados haya'. Con 10.000 estados, parametros_tabla pasaría a 10.000, mientras parametros_funcion seguiría en 2 — la razón pasaría de 500 a 5000.",
   "whyNot": [
    null,
    "La razón no es un número fijo — depende de parametros_tabla, que en este código es igual a n_estados_grande y por lo tanto crece linealmente con la cantidad de estados; con más estados, la razón también crece.",
    "La ventaja central de aproximar con una función lineal es justamente que parametros_funcion=2 no cambia sin importar cuántos estados haya, como dice el propio comentario del código — más estados no implica más parámetros para la función.",
    "Exactamente lo contrario: la esencia de aproximar con una función lineal es que 2 parámetros (w,b) alcanzan sin importar si hay 1000, 10.000 o cualquier otra cantidad de estados — no hace falta escalar parametros_funcion con el tamaño del problema."
   ],
   "steps": [
    "parametros_tabla = n_estados_grande — crece exactamente igual que la cantidad de estados (con 1000 estados, 1000 parámetros).",
    "parametros_funcion = 2 — es un número fijo en el código, no depende de n_estados_grande.",
    "Si n_estados_grande pasara de 1000 a 10.000, parametros_tabla pasaría a 10.000 pero parametros_funcion seguiría en 2 — la razón (parametros_tabla/parametros_funcion) pasaría de 500 a 5000."
   ],
   "stakes": "Esta brecha que se agranda cuanto más grande es el problema real es exactamente por qué la aproximación de funciones se vuelve indispensable (no solo conveniente) a medida que el espacio de estados crece, como en Go o en los píxeles de un videojuego."
  }
 ],
 [
  {
   "question": "En el código, guardar Q con una tabla de 1000 estados necesitaría 1000 parámetros, pero la función Q_aprox(s)=w·s+b solo necesita 2 (w y b). ¿Por qué la función se arregla con tan pocos números sin importar cuántos estados haya?",
   "type": "mc",
   "options": [
    "Porque w y b son 2 números fijos que definen la recta COMPLETA; una vez ajustados, Q_aprox(s) puede calcularse para CUALQUIER valor de s (incluso uno nunca visitado), sin necesitar una entrada separada guardada por estado",
    "Porque el código solo probó 4 estados reales (el corredor), y para 1000 estados de verdad también haría falta una entrada por estado",
    "Porque w y b se recalculan y se guardan por separado para cada uno de los 1000 estados posibles",
    "Porque en realidad la tabla Q_tabla también usa solo 2 parámetros, igual que la función"
   ],
   "correct": 0,
   "solution": "Una recta queda completamente determinada por su pendiente (w) y su ordenada al origen (b) — con esos 2 números fijos, evaluar Q_aprox(s)=w·s+b para s=0, s=500 o s=999 es la MISMA cuenta, sin guardar nada adicional por estado. Por eso parametros_funcion=2 no depende de n_estados_grande=1000: la función GENERALIZA, la tabla MEMORIZA.",
   "whyNot": [
    null,
    "Todo lo contrario: la ventaja central de aproximar con una función es que generaliza a estados NUNCA vistos — el código usa el corredor de 4 estados para entrenar w y b, pero esos mismos 2 números servirían igual de bien para evaluar Q_aprox en un estado 1000 que nunca se muestreó.",
    "w y b son UN SOLO PAR de números compartidos por TODOS los estados — el código los actualiza una vez por paso de entrenamiento (w, b = w + alpha*error_td*s, b + alpha*error_td), no hay una copia separada de w,b por cada estado posible.",
    "Q_tabla en el código es un diccionario con 4 entradas explícitas (una por cada uno de los 4 estados), cada una guardada por separado — es exactamente el patrón que NO escala: parametros_tabla=n_estados_grande crece con el número de estados, parametros_funcion=2 no."
   ],
   "steps": [
    "Una recta queda completamente definida por 2 números: su pendiente (w) y su ordenada al origen (b).",
    "Con esos 2 números fijos, Q_aprox(s)=w·s+b puede evaluarse para CUALQUIER valor de s — incluso uno nunca visto — sin guardar nada adicional.",
    "Por eso parametros_funcion=2 no depende de cuántos estados haya (n_estados_grande=1000): la función generaliza con una regla fija, la tabla necesitaría memorizar cada caso por separado."
   ],
   "stakes": "Esta capacidad de generalizar a estados nunca vistos es lo que hace útil un modelo real: un sistema de RL entrenado con una tabla no podría actuar frente a una situación nueva, mientras que uno con una función aproximada sí puede estimar algo razonable."
  },
  {
   "question": "El código imprime 'historial_b' bajo la etiqueta 'Q(0) durante el entrenamiento'. ¿Por qué el valor de 'b' por sí solo, sin necesitar 'w', ya representa exactamente Q_aprox(0)?",
   "type": "mc",
   "options": [
    "Porque Q_aprox(s) = w*s + b, y al evaluar en s=0 el término w*s se anula (w*0=0) — quedando Q_aprox(0) = b exactamente, sin importar cuál sea el valor de w",
    "Porque w siempre vale 0 durante todo el entrenamiento",
    "Porque b y w son en realidad el mismo número, calculado dos veces",
    "Porque el estado 0 no forma parte del corredor, así que Q_aprox(0) no tiene sentido calcularlo"
   ],
   "correct": 0,
   "solution": "Q_aprox(s) = w*s + b. Al evaluar en s=0: w*0 + b = 0 + b = b — el término con w desaparece por completo. Por eso seguir el valor de b a lo largo del entrenamiento es exactamente lo mismo que seguir cómo evoluciona Q_aprox(0), sin necesitar ningún cálculo extra.",
   "whyNot": [
    null,
    "w cambia a lo largo del entrenamiento (se actualiza en 'w, b = w + alpha*error_td*s, ...') y termina en un valor final distinto de 0, impreso como 'w final' — no se mantiene constante en 0.",
    "w y b son dos parámetros distintos, actualizados con reglas distintas (w se corrige multiplicando por 's', b se corrige directamente por el error) — no son el mismo número.",
    "El estado 0 sí es parte del corredor: es el estado inicial de cada episodio ('s = 0' al comienzo del bucle 'for episodio'), y Q_aprox(0) aparece explícitamente en el diccionario final Q_aprox que se imprime."
   ],
   "steps": [
    "Mirá la fórmula: Q_aprox(s) = w*s + b.",
    "Si evaluás en s=0: w*0 + b = 0 + b = b — el término con 'w' desaparece completamente.",
    "Por eso, seguir el valor de 'b' a lo largo del entrenamiento es exactamente lo mismo que seguir cómo evoluciona Q_aprox(0) — no hace falta ningún cálculo extra."
   ],
   "stakes": "Entender qué representa cada parámetro de un modelo simple (como que 'b' es literalmente el valor en s=0) ayuda a interpretar modelos más complejos — en una red neuronal real, entender qué mide cada parte del modelo es clave para depurarlo."
  }
 ],
 [
  {
   "question": "Q_aprox no da exactamente igual que Q_tabla: por ejemplo Q_aprox(0)=-2,677 contra el valor exacto de la tabla, -2,71 (error cuadrático medio de 0,0016 en total). ¿Qué significa esa diferencia?",
   "type": "mc",
   "options": [
    "Que una función lineal (una recta) es una APROXIMACIÓN simple, no memoriza los valores exactos como la tabla — el error es chico, y a cambio se gana la capacidad de generalizar a estados nunca vistos, algo que la tabla no puede hacer",
    "Que hay un error de programación en el código: si estuviera bien escrito, Q_aprox debería dar EXACTAMENTE igual que Q_tabla",
    "Que Q-learning y la aproximación de funciones son dos algoritmos completamente distintos, sin ninguna relación entre sí",
    "Que usar menos episodios (40 en vez de los 60 del tema anterior) es la única causa del error, y con 60 episodios el error desaparecería por completo"
   ],
   "correct": 0,
   "solution": "Aproximar con una función siempre implica ceder algo de precisión: una recta no puede pasar EXACTAMENTE por los 3 valores -2,71/-1,9/-1,0 salvo que esos 3 puntos ya estuvieran perfectamente alineados (no lo están del todo). Ese pequeño costo (MSE=0,0016) es el precio de ganar una representación con 500 veces menos parámetros que generaliza a estados que la tabla nunca podría cubrir.",
   "whyNot": [
    null,
    "El código no tiene ningún error: la actualización semi-gradiente (w, b = w + alpha*error_td*s, b + alpha*error_td) es exactamente la Ec.12.14 del libro. Que una función lineal no reproduzca los 3 valores con precisión perfecta es esperable — una recta tiene solo 2 grados de libertad para ajustar 3 puntos.",
    "Q-learning y la aproximación por función usan la MISMA idea de fondo (corregir con el error de diferencia temporal r + γ·max Q(s',a') − Q(s,a)); la diferencia es que uno corrige una casilla de tabla y el otro corrige los parámetros w,b de una función — no son algoritmos sin relación.",
    "Aumentar los episodios reduce el error de CONVERGENCIA (que la función se acerque a lo mejor que una recta puede ajustar), pero no lo hace desaparecer del todo: una recta simplemente no puede representar una curva no perfectamente lineal con error cero, sin importar cuántos episodios se entrenen."
   ],
   "steps": [
    "Comparalos: Q_aprox(0)=-2,677 vs. el valor exacto de la tabla, -2,71 — hay una pequeña diferencia, no son idénticos.",
    "Una recta no puede pasar EXACTAMENTE por 3 puntos salvo que esos 3 puntos ya estuvieran perfectamente alineados — y no lo están del todo acá.",
    "Ese error chico (MSE=0,0016) es el costo de usar una representación con muchísimos menos parámetros, que además puede generalizar a estados que la tabla nunca podría cubrir."
   ],
   "stakes": "Aceptar un pequeño error a cambio de generalización es una decisión de diseño constante en sistemas reales de machine learning — el objetivo casi nunca es memorizar perfectamente los datos de entrenamiento, sino funcionar bien con datos nuevos."
  },
  {
   "question": "Comparando los 3 valores aproximados con los exactos: Q_aprox(0)=-2,677 vs Q_tabla(0)=-2,71 (diferencia notable), pero Q_aprox(2)=-1,0 vs Q_tabla(2)=-1,0 (coinciden exactamente). ¿Qué explica que el ajuste sea mucho mejor en el estado 2 que en el estado 0?",
   "type": "mc",
   "options": [
    "Una recta (w*s+b) es una aproximación GLOBAL: ajusta lo mejor posible en promedio a los 3 puntos, pero no necesariamente igual de bien en cada uno — en este caso particular, terminó ajustando casi perfecto en un extremo (estado 2) mientras deja más error en el otro (estado 0)",
    "Es imposible que eso pase: los 3 estados siempre tienen exactamente el mismo error de aproximación",
    "Ocurre porque el estado 2 usa una fórmula de actualización distinta a la del estado 0",
    "El estado 2 se entrenó con más episodios que el estado 0 dentro del mismo entrenamiento"
   ],
   "correct": 0,
   "solution": "Una recta es una única línea que debe pasar cerca de los 3 puntos (-2,71 en s=0, -1,9 en s=1, -1,0 en s=2) a la vez — no puede ajustarse perfectamente a los 3 salvo que ya estuvieran alineados. El ajuste, guiado por el error TD, reparte el error entre los 3 puntos según minimiza el error total, no necesariamente por igual en cada uno; acá terminó ajustando casi perfecto en el estado 2 y dejando más margen de error en el estado 0.",
   "whyNot": [
    null,
    "Los datos mismos lo contradicen: el error es distinto para cada estado (notable en el estado 0, prácticamente nulo en el estado 2) — no son iguales entre sí.",
    "Los 3 estados usan exactamente la misma fórmula de actualización ('w, b = w + alpha*error_td*s, b + alpha*error_td') dentro del mismo bucle de entrenamiento — no hay una fórmula distinta según el estado.",
    "Los 3 estados se visitan dentro del mismo episodio, recorriendo el corredor completo (0→1→2→3), con el mismo número total de episodios (40) para todos — no hay un entrenamiento diferenciado por estado."
   ],
   "steps": [
    "Una recta es una única línea que tiene que pasar cerca de los 3 puntos (-2,71 en s=0, -1,9 en s=1, -1,0 en s=2) a la vez — no puede ajustarse perfectamente a los 3 salvo que ya estén alineados.",
    "El ajuste, guiado por el error TD, reparte el error entre los 3 puntos según cómo minimiza el error total, no necesariamente por igual en cada uno.",
    "En este caso particular, terminó ajustando casi perfecto en el estado 2 y dejando más margen de error en el estado 0 — es un resultado del ajuste global, no un tratamiento especial a ningún estado."
   ],
   "stakes": "Que un modelo aproximado ajuste mejor en algunas partes del espacio de estados que en otras es un fenómeno real y esperado en machine learning — evaluar solo el error promedio no basta, a veces hace falta revisar específicamente dónde el modelo se equivoca más."
  }
 ],
 [
  {
   "question": "En este tema se aproxima Q(s) con la función más simple posible: una recta, Q_aprox(s)=w·s+b, con solo 2 parámetros. ¿Qué reemplaza a esa recta en un sistema real como DQN (Deep Q-Network)?",
   "type": "mc",
   "options": [
    "Una red neuronal profunda (por ejemplo, una CNN) con muchos más parámetros ajustables, entrenada con la MISMA idea de este tema: corregir los parámetros por descenso del gradiente en vez de llenar casillas de tabla",
    "Una tabla todavía más grande, con una fila guardada por cada píxel posible de la pantalla del juego",
    "Un algoritmo completamente distinto, sin relación con Q-learning ni con el descenso del gradiente",
    "En realidad DQN sigue usando una tabla Q(s,a) tradicional, solo que optimizada para ser más rápida"
   ],
   "correct": 0,
   "solution": "El propio capítulo lo dice explícito: una red neuronal profunda es 'una aproximación de función rápida' (fast function approximation) que reemplaza a la tabla — el mismo principio de este tema (ajustar parámetros con descenso del gradiente sobre el error de diferencia temporal), solo que con una red mucho más flexible que una recta en vez de solo w y b.",
   "whyNot": [
    null,
    "Justamente lo contrario: la razón de usar una red neuronal en DQN es EVITAR una tabla — el libro explica que guardar Q en tabla es inviable con espacios de estados grandes o continuos, como los píxeles de una pantalla de Atari (miles de valores posibles por píxel, en miles de píxeles).",
    "DQN (Mnih et al., 2015) es explícitamente descrito en el libro como un método de Q-learning que usa aproximación de función — la actualización de sus parámetros usa la misma Ec.12.14 (el error de diferencia temporal r + γ·max Qθ(s',a') − Qθ(s,a)) que se usó para ajustar w,b en este tema.",
    "Es exactamente al revés: DQN existe PORQUE una tabla Q(s,a) tradicional se vuelve inviable con estados de alta dimensión (como imágenes) — la red neuronal reemplaza la tabla, no la hace más rápida mientras la sigue usando."
   ],
   "steps": [
    "En este tema, la aproximación más simple posible de Q(s) es una recta: solo 2 parámetros (w y b).",
    "El mismo PRINCIPIO — ajustar parámetros con descenso del gradiente en vez de llenar casillas de tabla — se puede aplicar con un modelo mucho más flexible.",
    "Una red neuronal profunda tiene muchísimos más parámetros ajustables que una recta, así que puede aproximar funciones mucho más complejas que Q_aprox(s)=w·s+b.",
    "Por eso DQN reemplaza la recta simple por una red neuronal profunda, manteniendo la misma idea de fondo de este tema."
   ],
   "stakes": "Este es el puente directo hacia sistemas reales que juegan Atari o Go a nivel sobrehumano (DQN, AlphaGo): la misma idea de este tema, escalada con una red neuronal en vez de una recta."
  },
  {
   "question": "La actualización del código es: w = w + alpha*error_td*s, pero b = b + alpha*error_td (sin multiplicar por 's'). ¿Por qué la corrección de 'w' sí se multiplica por 's' y la de 'b' no?",
   "type": "mc",
   "options": [
    "Porque el gradiente de Q(s)=w*s+b respecto a w es 's' (grad_w=s), mientras que el gradiente respecto a b es 1 (grad_b=1) — la regla de descenso del gradiente multiplica el error por el gradiente de CADA parámetro, y son distintos para w y para b",
    "Es un error del código: ambas actualizaciones deberían multiplicarse por 's'",
    "Porque 'b' nunca cambia durante el entrenamiento, así que no necesita ningún factor multiplicando",
    "Porque 's' representa el número de episodios de entrenamiento, no el estado"
   ],
   "correct": 0,
   "solution": "El propio comentario del código lo indica: 'para Q(s)=w*s+b: grad_w=s, grad_b=1'. La regla de descenso del gradiente corrige cada parámetro multiplicando el error por su propio gradiente — como el gradiente de w es 's' y el de b es 1, la actualización de w se multiplica por 's' y la de b efectivamente no lleva ningún factor extra (multiplicar por 1 no cambia nada).",
   "whyNot": [
    null,
    "El propio comentario del código lo aclara explícitamente: 'para Q(s)=w*s+b: grad_w=s, grad_b=1' — son gradientes distintos por diseño matemático, no un error de programación.",
    "'b' sí cambia en cada actualización ('b = b + alpha*error_td') — de hecho, el 'historial_b' impreso muestra esos cambios a lo largo de las 40 iteraciones de entrenamiento.",
    "'s' es el estado actual dentro del bucle interno (viene de 's = 0' al inicio de cada episodio, y de 'siguiente[s]' en cada paso) — no tiene relación con el contador de episodios ('episodio' es una variable completamente distinta del bucle externo 'for episodio in range(40)')."
   ],
   "steps": [
    "El comentario del código dice: 'para Q(s)=w*s+b: grad_w=s, grad_b=1'.",
    "La regla de descenso del gradiente corrige cada parámetro multiplicando el error por SU PROPIO gradiente.",
    "Como el gradiente de w es 's' y el de b es 1, la actualización de w se multiplica por 's' y la de b se multiplica por 1 (o sea, no lleva ningún factor extra) — son fórmulas distintas porque los gradientes son distintos."
   ],
   "stakes": "Esta misma regla — multiplicar el error por el gradiente específico de cada parámetro — es exactamente lo que hace el backpropagation en una red neuronal real, solo que con muchísimos más parámetros y gradientes más complejos de calcular."
  }
 ]
];

/* ──────────── Modo Maestro RF (Aprendizaje por Refuerzo) ────────────
   Mismo patrón exacto que master-as.js (ver ese archivo para el diseño
   original): progreso propio en localStorage, reutiliza runCode()/panel de
   pasos (el código sigue siendo Python), teoría + Visualízalo + Aplicación
   real + quiz con whyNot completo + confianza + razonamiento + Leitner. */
const MASTER_RF_KEY='pyvizMasterRfProgressV1';
let _rfOn=false, _rfPos=0, _rfDone=new Set(), _rfQuizAnswered=false, _rfQuizShuffledCorrect=null, _rfCurrentQuiz=null, _rfQuizSubPos=0, _rfQuizOrder=null;

function _loadRfProgress(){
  try{
    const raw=localStorage.getItem(MASTER_RF_KEY);
    if(raw){ const d=JSON.parse(raw); _rfDone=new Set(d.done||[]); }
  }catch(e){ _rfDone=new Set(); }
}
function _saveRfProgress(){
  try{ localStorage.setItem(MASTER_RF_KEY, JSON.stringify({done:[..._rfDone]})); }catch(e){}
}
function _rfFirstPending(){
  for(let i=0;i<EX_RF.length;i++) if(!_rfDone.has(i)) return i;
  return EX_RF.length-1;
}
function toggleMasterRf(){
  if(_rfOn){ exitMasterRf(); return; }
  if(_masterOn) exitMasterMode();
  if(_aoOn) exitMasterAo();
  if(_mathOn) exitMasterMath();
  if(_raOn) exitMasterRa();
  if(typeof _asOn!=='undefined' && _asOn) exitMasterAs();
  if(typeof _nsOn!=='undefined' && _nsOn && 'rf'!=='ns') exitMasterNs();
  if(typeof _rnOn!=='undefined' && _rnOn && 'rf'!=='rn') exitMasterRn();
  if(typeof _rfOn!=='undefined' && _rfOn && 'rf'!=='rf') exitMasterRf();
  if(_reviewOn) exitReviewMode();
  if(typeof _calOn!=='undefined' && _calOn) _calClose();
  if(typeof _reportOn!=='undefined' && _reportOn) _reportClose();
  if(typeof _sessionOn!=='undefined' && _sessionOn) _sessionClosePanel();
  if(typeof _errorsOn!=='undefined' && _errorsOn) _errorsClose();
  if(typeof _examOn!=='undefined' && _examOn) _examClose();
  _rfOn=true;
  _loadRfProgress();
  document.getElementById('masterRfBar').style.display='flex';
  const b=document.getElementById('bMasterRf');
  if(b){ b.textContent='🕹️ Modo Maestro RF (activo)'; b.classList.add('btn-looping'); }
  autoLayout();
  _rfGoTo(_rfFirstPending());
}
function exitMasterRf(){
  _rfOn=false;
  document.getElementById('masterRfBar').style.display='none';
  document.getElementById('masterRfChecklist').style.display='none';
  const b=document.getElementById('bMasterRf');
  if(b){ b.textContent='🕹️ Modo Maestro RF'; b.classList.remove('btn-looping'); }
  autoLayout();
}
function _rfGoTo(idx){
  _rfPos=Math.max(0, Math.min(EX_RF.length-1, idx));
  _rfQuizSubPos=0;
  document.getElementById('codeInput').value=EX_RF[_rfPos].code;
  renderLineNums();
  document.getElementById('frBody').innerHTML='<div class="ob-ph">No variables yet</div>';
  document.getElementById('obBody').innerHTML='<div class="ob-ph">Click [→] to inspect</div>';
  document.getElementById('outBody').innerHTML='<span class="out-empty">No output yet</span>';
  runCode();
  _rfRenderBar();
  _resetSelfExplain('rf');
  _rfRenderTheory();
  _rfRenderConceptViz();
  _rfRenderApplication();
  _rfRenderCodeAnatomy();
  _rfRenderQuiz();
}
function _rfRenderTheory(){
  const t=EX_RF[_rfPos].theory;
  const block=document.getElementById('rfTheoryBlock');
  if(!t){ block.style.display='none'; return; }
  if(_theoryIsLocked('rf', 'rf', _rfPos)){
    document.getElementById('rfTheoryBody').innerHTML=_theoryGateHtml('rf', _rfPos, '_rfRenderTheory');
    block.style.display='block';
    return;
  }
  document.getElementById('rfTheoryBody').innerHTML=t;
  block.style.display='block';
}
function _rfRenderConceptViz(){
  const viz=EX_RF[_rfPos].viz;
  const block=document.getElementById('rfConceptVizBlock');
  if(!viz){ block.style.display='none'; return; }
  const svg=renderConceptViz(viz);
  if(!svg){ block.style.display='none'; return; }
  document.getElementById('rfConceptVizBody').innerHTML=svg;
  block.style.display='block';
}
function _rfRenderApplication(){
  const a=EX_RF[_rfPos].application;
  const block=document.getElementById('rfApplicationBlock');
  if(!a){ block.style.display='none'; return; }
  document.getElementById('rfApplicationBody').innerHTML=a;
  block.style.display='block';
}
/* Panel "🔬 Anatomía del código" -- ver la cabecera igual en master-ra.js
   para el porqué. Piloto hecho a mano, un tema por modo. */
function _rfRenderCodeAnatomy(){
  const spec=EX_RF[_rfPos].codeAnatomy;
  const block=document.getElementById('rfCodeAnatomyBlock');
  if(!spec){ block.style.display='none'; return; }
  const svg=renderCodeAnatomy(spec);
  if(!svg){ block.style.display='none'; return; }
  document.getElementById('rfCodeAnatomyBody').innerHTML=svg;
  block.style.display='block';
}
function _rfRenderQuiz(){
  const bank=RF_QUIZ[_rfPos];
  const q=bank[_rfQuizSubPos];
  _rfCurrentQuiz=q;
  _rfQuizAnswered=false;
  document.getElementById('rfQuizProgress').textContent=
    bank.length>1 ? `(pregunta ${_rfQuizSubPos+1}/${bank.length} de este tema)` : '';
  document.getElementById('rfQuizNextBtn').style.display='none';
  document.getElementById('rfQuizQuestion').innerHTML=q.question;
  const optWrap=document.getElementById('rfQuizOptions');
  const numWrap=document.getElementById('rfQuizNumericWrap');
  if(q.type==='mc'){
    numWrap.style.display='none';
    const res=_quizRenderAnswerArea('rf', 'rf', _rfPos, q);
    _rfQuizShuffledCorrect=res.shuffled?res.shuffled.correct:null;
    _rfQuizOrder=res.shuffled?res.shuffled.order:null;
  } else {
    optWrap.style.display='none';
    numWrap.style.display='flex';
    const inp=document.getElementById('rfQuizNumericInput');
    inp.value=''; inp.disabled=false;
    _rfQuizShuffledCorrect=null;
    _rfQuizOrder=null;
  }
  document.getElementById('rfQuizFeedback').style.display='none';
  document.getElementById('rfQuizSolutionBtn').style.display='none';
  const solBody=document.getElementById('rfQuizSolutionBody');
  solBody.style.display='none'; solBody.innerHTML='';
  _quizResetExtras('rf');
}
function _rfCheckQuizAnswer(selectedIdx){
  if(_rfQuizAnswered) return;
  const q=_rfCurrentQuiz;
  let ok=false;
  if(q.type==='mc'){
    ok = selectedIdx===_rfQuizShuffledCorrect;
    document.querySelectorAll('#rfQuizOptions .math-option').forEach((btn,i)=>{
      btn.classList.remove('math-option-correct','math-option-wrong');
      if(ok){
        btn.disabled=true;
        if(i===_rfQuizShuffledCorrect) btn.classList.add('math-option-correct');
      } else if(i===selectedIdx){
        btn.classList.add('math-option-wrong');
      }
    });
  } else {
    const inp=document.getElementById('rfQuizNumericInput');
    const val=parseFloat(inp.value.trim().replace(',','.'));
    const dec=q.decimals||0;
    const pw=Math.pow(10,dec);
    ok = !isNaN(val) && Math.round(val*pw)===Math.round(q.correct*pw);
    inp.disabled=ok;
  }
  if(ok) _rfQuizAnswered=true;
  _recordAttempt('rf', _rfPos, ok);
  _rfRenderTheory();
  const fb=document.getElementById('rfQuizFeedback');
  fb.style.display='block';
  fb.className='math-feedback '+(ok?'math-feedback-ok':'math-feedback-bad');
  const whyNot = (!ok && q.type==='mc' && q.whyNot && _rfQuizOrder) ? q.whyNot[_rfQuizOrder[selectedIdx]] : null;
  if(whyNot) _logErrorJournal('rf', _rfPos, EX_RF[_rfPos].name, q.question, q.options[_rfQuizOrder[selectedIdx]], q.options[q.correct], whyNot);
  fb.textContent = ok ? '✅ Correcto.' :
    (whyNot ? '❌ '+whyNot+' Puedes intentarlo de nuevo, o revisar la solución.'
            : '❌ Incorrecto — puedes intentarlo de nuevo, o revisar la solución.');
  document.getElementById('rfQuizSolutionBtn').style.display='inline-block';
  if(ok) _quizRenderConfidencePrompt('rf');
  if(q.type==='mc' && _rfQuizOrder){
    const otherOptionTexts=q.options.filter((_,i)=>i!==_rfQuizOrder[selectedIdx]);
    _quizRenderReasonPrompt('rf', otherOptionTexts);
  }
  if(ok && _rfQuizSubPos<RF_QUIZ[_rfPos].length-1)
    document.getElementById('rfQuizNextBtn').style.display='inline-block';
}
function _rfNextQuizQuestion(){
  if(_rfQuizSubPos<RF_QUIZ[_rfPos].length-1){ _rfQuizSubPos++; _rfRenderQuiz(); }
}
function _rfShowQuizSolution(){
  const q=_rfCurrentQuiz;
  const el=document.getElementById('rfQuizSolutionBody');
  el.innerHTML=q.solution+_quizStepsHtml(q)+_quizWhyNotHtml(q, _rfQuizOrder)+_quizStakesHtml(q);
  el.style.display='block';
}
function _rfRenderBar(){
  const ex=EX_RF[_rfPos];
  const pct=Math.round((_rfDone.size/EX_RF.length)*100);
  document.getElementById('masterRfTitle').textContent=
    `🕹️ Tema ${_rfPos+1}/${EX_RF.length} · ${ex.name}`;
  document.getElementById('masterRfFill').style.width=pct+'%';
  document.getElementById('masterRfPct').textContent=pct+'% del temario RF dominado';
  document.getElementById('mPrevRf').disabled=(_rfPos<=0);
  const atEnd=_rfPos>=EX_RF.length-1;
  document.getElementById('mNextRf').textContent=atEnd ? '✅ Entendido, terminar' : '✅ Entendido, siguiente ▶';
  if(document.getElementById('masterRfChecklist').style.display!=='none') _rfRenderChecklist();
}
function rfPrev(){ if(_rfPos>0) _rfGoTo(_rfPos-1); }
function rfRepeat(){ _rfGoTo(_rfPos); }
function _rfRestart(){ _rfGoTo(0); }
function rfNext(){
  _rfDone.add(_rfPos);
  _saveRfProgress();
  if(_rfPos>=EX_RF.length-1){
    _rfRenderBar();
    setSt('🎉 ¡Completaste el piloto del Modo Maestro de Aprendizaje por Refuerzo!');
    return;
  }
  _rfGoTo(_rfPos+1);
}
function _rfToggleChecklist(){
  const cl=document.getElementById('masterRfChecklist');
  const show=cl.style.display==='none';
  cl.style.display=show?'block':'none';
  if(show) _rfRenderChecklist();
}
function _rfRenderChecklist(){
  const cl=document.getElementById('masterRfChecklist');
  cl.innerHTML=EX_RF.map((ex,i)=>{
    const done=_rfDone.has(i);
    const cur=i===_rfPos;
    return `<div class="master-item${done?' master-item-done':''}${cur?' master-item-current':''}" onclick="_rfGoTo(${i})">`+
      `<span class="master-item-chk">${done?'✓':(i+1)}</span><span class="master-item-name">${esc(ex.name)}</span>${_failsBadge('rf',i)}${_dontKnowBadge('rf',i)}</div>`;
  }).join('');
}

/* Glosario RF: pedido explícito del usuario ("que ningún término quede sin
   explicación") -- cubre TODO término técnico que aparece en las preguntas,
   teoría o soluciones de los 20 temas de RF (bandido, Markov, V(s),
   Q-learning, tabla vs función), buscable vía el botón "📚 Glosario". */
const GLOSSARY_RF=[
{term:'Acción (a)', def:'Cada una de las opciones disponibles para el agente en un estado dado — por ejemplo, elegir un brazo del bandido, o "lento"/"rápido" para el robot del proceso de Markov.'},
{term:'Agente', def:'El programa que toma decisiones (acciones) en un entorno, con el objetivo de maximizar la recompensa acumulada a lo largo del tiempo — el "quien decide" en cualquier problema de RL.'},
{term:'Bandido multi-brazo (multi-armed bandit)', def:'El problema más simple de RL: hay varias opciones ("brazos") con recompensa promedio desconocida y distinta, y el agente debe decidir cuál probar en cada paso para maximizar la recompensa total, balanceando explorar y explotar.'},
{term:'DQN (Deep Q-Network)', def:'Un sistema real de RL que reemplaza la tabla Q (o una función simple como una recta) por una red neuronal profunda para aproximar Q(s,a) — permite manejar espacios de estados enormes o continuos, como los píxeles de una pantalla de videojuego.'},
{term:'Entorno', def:'Todo lo que rodea al agente y con lo que interactúa: le da estados, recibe acciones, y devuelve recompensas y el siguiente estado.'},
{term:'Episodio', def:'Una secuencia completa de pasos desde un estado inicial hasta llegar a un estado terminal (por ejemplo, la meta) — Q-learning aprende acumulando experiencia a lo largo de muchos episodios.'},
{term:'Épsilon (ε) / ε-greedy', def:'Una estrategia que elige la acción al azar con probabilidad ε (exploración) y la de mejor valor estimado el resto de las veces (explotación) — evita quedarse "pegado" en una mala estimación inicial, a diferencia de la estrategia greedy pura.'},
{term:'Estado (s)', def:'Una descripción de la situación actual del agente o del entorno en un momento dado — por ejemplo, "de pie", "caído" o "moviéndose" para el robot del proceso de Markov.'},
{term:'Explotar (exploit)', def:'Elegir la acción que, según lo aprendido hasta ahora, parece ser la mejor — el riesgo es quedarse con una opción subóptima si la estimación inicial fue engañosa.'},
{term:'Explorar (explore)', def:'Elegir una acción distinta a la que parece mejor, para obtener más información y corregir estimaciones que podrían estar equivocadas por mala suerte inicial.'},
{term:'Gamma (γ) / factor de descuento', def:'Un número entre 0 y 1 que pesa cuánto importan las recompensas FUTURAS respecto a las inmediatas — γ cercano a 0 hace al agente "miope" (solo le importa el próximo paso), γ cercano a 1 le da visión de largo plazo.'},
{term:'Greedy (estrategia)', def:'Elegir siempre la acción con mejor valor estimado hasta el momento, sin ninguna exploración — puede quedarse atascada en una mala decisión si la estimación inicial de la mejor opción fue por mala suerte.'},
{term:'MDP (Proceso de Decisión de Markov)', def:'El marco matemático formal para modelar problemas de decisión secuencial: estados, acciones, un modelo de transición (a qué estado se pasa) y una función de recompensa — la base teórica de todo el aprendizaje por refuerzo.'},
{term:'Modelo de transición', def:'La función (o matriz de probabilidades) que describe a qué estado se pasa al tomar una acción desde un estado dado — puede ser determinístico (un único resultado) o probabilístico (varios resultados posibles con distinta probabilidad).'},
{term:'Planning', def:'Resolver un problema de decisión cuando el modelo de transición y la función de recompensa YA se conocen de antemano (por ejemplo, con una fórmula cerrada como V_horizonte) — distinto de RL real, donde esas funciones son desconocidas.'},
{term:'Policy gradient', def:'Una familia de métodos de RL que, en vez de aprender el VALOR de cada acción (como Q-learning), ajusta directamente los parámetros de una política (la probabilidad de elegir cada acción) mediante descenso/ascenso del gradiente.'},
{term:'Política (π)', def:'La estrategia del agente: qué acción tomar en cada estado. Puede ser fija (como π en V_horizonte) o algo que el agente va mejorando con la experiencia (como en Q-learning).'},
{term:'Propiedad de Markov', def:'La suposición de que el siguiente estado depende SOLO del estado y la acción actuales, no de toda la historia de estados anteriores — simplifica enormemente el modelado de problemas de decisión secuencial.'},
{term:'Q(s,a) / Q-learning', def:'Q(s,a) es el valor estimado de tomar la acción a en el estado s. Q-learning es el algoritmo que aprende esos valores por experiencia (sin conocer el modelo del entorno de antemano), actualizándolos con la regla TD tras cada paso.'},
{term:'Recompensa (reward, r)', def:'El número que el entorno le da al agente después de cada acción, indicando qué tan buena o mala fue esa decisión en ese momento — el agente busca maximizar la SUMA de recompensas a lo largo del tiempo, no solo la inmediata.'},
{term:'Tabla Q (Q-table)', def:'Una tabla que guarda un valor Q(s,a) por cada combinación posible de estado y acción — funciona bien con pocos estados, pero se vuelve inviable en memoria cuando el espacio de estados es muy grande o continuo (como en Go o los píxeles de una pantalla).'},
{term:'TD (diferencia temporal) / error TD', def:'El método de aprender comparando una estimación NUEVA (recompensa real + valor descontado del siguiente estado) contra la estimación VIEJA que ya se tenía — la diferencia entre ambas es el error TD, la señal que usa Q-learning para corregirse.'},
{term:'V(s) / función de valor', def:'El valor esperado de estar en el estado s y seguir la política π de ahí en adelante — a diferencia de Q(s,a), no distingue entre distintas acciones posibles desde ese estado, solo evalúa el estado en sí.'},
];
function _rfToggleGlossary(){
  const gl=document.getElementById('masterRfGlossary');
  const show=gl.style.display==='none';
  gl.style.display=show?'block':'none';
  if(show) _rfRenderGlossary();
}
function _rfRenderGlossary(){
  const input=document.getElementById('rfGlossarySearch');
  document.getElementById('rfGlossaryList').innerHTML=_glossaryHtml(GLOSSARY_RF, input?input.value:'');
}
/* ──────────── RF_COMPARE: peldaño "Comparación" (Escalera de Dominio) ────────────
   Mismo patrón que AS_COMPARE en master-as.js. `pair` son los dos índices
   BASE (múltiplos de 4) en EX_RF. */
const RF_COMPARE=[
{pair:[8,12],
 question:'Calcular V(s) con la fórmula cerrada (tema "Función de valor") y Q-learning real son '+
  'ambos formas de encontrar el valor de un estado. ¿Cuál es la diferencia clave entre ambos?',
 options:[
  'V(s) con fórmula cerrada es PLANNING: asume que ya conocés la función de transición y '+
   'recompensa del entorno. Q-learning es RL real: el agente NO las conoce, y las descubre '+
   'muestreando el entorno paso a paso, corrigiendo su estimación con cada experiencia.',
  'Son exactamente el mismo cálculo, solo con nombres distintos.',
  'V(s) con fórmula cerrada necesita muchos episodios de prueba; Q-learning se calcula en un solo paso.',
  'Q-learning solo funciona si ya se conoce de antemano el valor óptimo de cada estado.'],
 correct:0,
 solution:'El propio capítulo lo distingue así: planning asume un MDP CONOCIDO (transición y '+
  'recompensa dadas, como en V_horizonte()); reinforcement learning asume que esas funciones son '+
  'DESCONOCIDAS, y el agente debe aprenderlas interactuando con el entorno — y aun así, Q-learning '+
  'convergió a los MISMOS valores (-2.71, -1.9, -1.0) que la fórmula cerrada.'},
];
function _rfCompareUnlocked(i){
  const [a,b]=RF_COMPARE[i].pair;
  const done=x=>[x,x+1,x+2,x+3].some(j=>_rfDone.has(j));
  return done(a) && done(b);
}

/* ──────────── RF_LIMITS: peldaño "Limitación" (Escalera de Dominio) ────────────
   Mismo patrón que AS_LIMITS en master-as.js. `concept` es el índice BASE
   (múltiplo de 4) en EX_RF. */
const RF_LIMITS=[
{concept:0,
 question:'El bandido multi-brazo (tema 1) elige una acción y recibe una recompensa, sin ningún '+
  '"estado" de por medio — el libro lo llama justo por eso el escenario "stateless" (sin estado). '+
  '¿Qué NO puede modelar el bandido multi-brazo que sí modela un Proceso de Markov completo (tema 2)?',
 options:[
  'El bandido multi-brazo puede modelar cualquier problema de decisión secuencial exactamente '+
   'igual que un MDP completo, no hay ninguna diferencia real.',
  'Que la acción de HOY cambie la SITUACIÓN de mañana — en el bandido, cada tirada es '+
   'independiente de las anteriores (elegir el brazo 2 ahora no afecta en nada la próxima tirada); '+
   'en un MDP real, la acción actual determina el ESTADO siguiente, y las decisiones futuras '+
   'dependen de ese estado.',
  'El bandido multi-brazo no puede usar la estrategia ε-greedy, solo los MDP completos pueden.',
  'La fórmula de actualización Q(a) = Q(a) + (r(a)-Q(a))/N(a) solo sirve para MDPs, no para bandidos.'],
 correct:1,
 solution:'La propia definición del bandido (Sec.11.2) lo deja afuera de un estado: se elige una '+
  'acción, se recibe una recompensa, y se repite — nunca hay una "situación" que cambie según lo '+
  'que elegiste antes. Un robot que se cae o se para (tema 2) es distinto: la acción de HOY '+
  '(ir lento o rápido) determina en qué estado vas a estar MAÑANA, y ahí es donde el bandido se '+
  'queda corto — no alcanza para modelar decisiones donde el pasado condiciona el futuro.'},
];
function _rfLimitsUnlocked(i){
  const c=RF_LIMITS[i].concept;
  return [c,c+1,c+2,c+3].some(j=>_rfDone.has(j));
}

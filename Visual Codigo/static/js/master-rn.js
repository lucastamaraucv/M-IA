/* ──────────── Modo Maestro RN (Redes Neuronales y Deep Learning) ──────────────
   Séptimo temario guiado, independiente del resto. Piloto de 3 conceptos (12 preguntas aplanadas) construido leyendo Géron, Cap.10-11 (Introduction to ANNs with Keras, Training Deep Neural Networks) -- sin TensorFlow/Keras instalados en este sandbox, el código verificado usa sklearn.neural_network (MLPClassifier) como equivalente real instalado, mismo patrón que AS evitando cv2.
   Fuente: ver comentario de cada tema (cita de página real). Verificado
   ejecutando de verdad el código con el intérprete Python del sistema antes
   de fijar cualquier número en la teoría o en las preguntas. */
const EX_RN = [
 {
  "name": "Redes Neuronales · La neurona artificial (perceptrón)",
  "theory": "<b>Idea central</b>: Un perceptrón resuelve aprender una regla de decisión simple (como una compuerta lógica) ajustando automáticamente los pesos de una suma ponderada, sin que nadie programe la regla a mano.<br><br><b>Concepto esencial</b>: Es una calculadora de sumas ponderadas — la parte \"inteligente\" está en CÓMO se ajustan esos pesos cada vez que se equivoca, no en la neurona en sí.<br><br><b>Detalle técnico y código</b>: <code>w = w + lr·error·xi</code> ajusta los pesos solo cuando hay error — verificado sobre la compuerta AND: 3 errores en la 1ª época, 0 errores desde la 3ª, y las 4 predicciones finales [0,0,0,1] coinciden exacto con AND. Formalmente (Géron, Cap.10): $z = \\sum_i w_i x_i + b$, activación $\\phi(z)$, actualización $w \\leftarrow w + \\eta(y - \\hat{y})x$.<br><br><b>Matices y advertencias</b>: el perceptrón simple solo aprende problemas linealmente separables como AND — con XOR (tema siguiente) queda atascado sin importar cuánto se entrene, hace falta una capa oculta.",
  "code": "# La neurona artificial / perceptron (Geron, Cap.10): suma ponderada de\n# las entradas + sesgo, pasada por una funcion de activacion (aqui, un\n# escalon: 0 o 1). Aprende ajustando los pesos cuando se equivoca.\nimport numpy as np\n\n# Compuerta AND: linealmente separable, un perceptron SIMPLE puede aprenderla\nX = np.array([[0,0],[0,1],[1,0],[1,1]])\ny = np.array([0,0,0,1])  # AND\n\nnp.random.seed(0)\nw = np.random.normal(0, 0.1, 2)\nb = 0.0\nlr = 0.1  # tasa de aprendizaje\n\ndef escalon(z): return 1 if z >= 0 else 0\n\nerrores_por_epoca = []\nfor epoca in range(15):\n    errores = 0\n    for xi, yi in zip(X, y):\n        z = np.dot(w, xi) + b          # suma ponderada (la 'neurona')\n        pred = escalon(z)               # activacion\n        error = yi - pred\n        if error != 0:\n            errores += 1\n            w = w + lr * error * xi     # ajusta los pesos si se equivoco\n            b = b + lr * error\n    errores_por_epoca.append(errores)\n\nprint(\"pesos finales:\", np.round(w, 3).tolist(), \" sesgo:\", round(b, 3))\nprint(\"errores por epoca (15 epocas):\", errores_por_epoca)\npreds = [escalon(np.dot(w, xi) + b) for xi in X]\nprint(\"predicciones finales [0,0],[0,1],[1,0],[1,1]:\", preds)\nprint(\"esperado (AND):                                \", y.tolist())",
  "viz": {
   "type": "curve",
   "data": {
    "points": [
     3,
     1,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ],
    "xLabel": "época",
    "yLabel": "errores",
    "aria": "Los errores del perceptron caen de 3 a 0 en la tercera epoca y se mantienen en 0 el resto del entrenamiento"
   }
  },
  "application": "El perceptrón original (Rosenblatt, 1957) fue la primera neurona artificial implementada en hardware real — y aunque hoy nadie usa un perceptrón suelto en producción, es la pieza de Lego con la que se construye TODO lo demás: una red neuronal moderna (desde un clasificador de imágenes hasta un modelo de lenguaje) es, por dentro, millones de estas mismas neuronas (suma ponderada + activación) conectadas en capas. Entender esta única neurona es entender el bloque básico de construcción de cualquier red, por gigante que sea (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.10).",
  "codeAnatomy": {
   "title": "for xi, yi in zip(X, y):",
   "caption": "Una época de entrenamiento del perceptrón — se ajustan los pesos si se equivoca",
   "lines": [
    "for xi, yi in zip(X, y):",
    "    z = np.dot(w, xi) + b",
    "    pred = escalon(z)",
    "    error = yi - pred",
    "    if error != 0:",
    "        w = w + lr * error * xi"
   ],
   "annotations": [
    {
     "line": 0,
     "text": "for",
     "label": "Keyword",
     "side": "top"
    },
    {
     "line": 0,
     "text": "xi, yi",
     "label": "Par de variables",
     "desc": "(un punto X, su etiqueta y)",
     "side": "top"
    },
    {
     "line": 0,
     "text": "zip(X, y)",
     "label": "Empareja",
     "desc": "(X[i] con y[i], a la vez)",
     "side": "top"
    },
    {
     "line": 1,
     "text": "np.dot(w, xi)",
     "label": "Suma ponderada",
     "desc": "(w·x, la \"neurona\")",
     "side": "bottom"
    },
    {
     "line": 2,
     "text": "escalon(z)",
     "label": "Activación",
     "desc": "(0 o 1)",
     "side": "bottom"
    },
    {
     "line": 4,
     "text": "error != 0",
     "label": "¿Se equivocó?",
     "side": "bottom"
    },
    {
     "line": 5,
     "text": "w + lr * error * xi",
     "label": "Regla de aprendizaje",
     "desc": "(ajusta w si erró)",
     "side": "bottom"
    }
   ],
   "blockBracket": {
    "from": 1,
    "to": 5,
    "label": "Cuerpo del for (por cada punto)"
   }
  }
 },
 {
  "name": "Redes Neuronales · La neurona artificial (perceptrón) — pregunta 2",
  "theory": "Una neurona artificial es mucho más simple de lo que suena: toma varios números de entrada, los multiplica cada uno por un \"peso\" (qué tan importante es esa entrada), los suma junto con un \"sesgo\", y pasa ese resultado por una función de activación que decide la salida final. Es literalmente una calculadora de sumas ponderadas — la parte \"inteligente\" está en CÓMO se ajustan esos pesos con la práctica, no en la neurona en sí.<br><br>En el código, un perceptrón (la neurona más simple posible, con activación escalón: 0 o 1) aprende la compuerta lógica AND desde cero. Al principio comete errores (3 de 4 en la primera época), pero cada vez que se equivoca ajusta sus pesos un poquito en la dirección correcta (<code>w = w + lr·error·xi</code>) — para la 3ª época ya no comete NINGÚN error más, y las 4 predicciones finales coinciden exactamente con AND.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.10): una neurona calcula $z = \\sum_i w_i x_i + b$ y aplica una función de activación $\\phi(z)$. La regla de actualización del perceptrón es $w \\leftarrow w + \\eta(y - \\hat{y})x$, donde $\\eta$ es la tasa de aprendizaje.",
  "code": "# La neurona artificial / perceptron (Geron, Cap.10): suma ponderada de\n# las entradas + sesgo, pasada por una funcion de activacion (aqui, un\n# escalon: 0 o 1). Aprende ajustando los pesos cuando se equivoca.\nimport numpy as np\n\n# Compuerta AND: linealmente separable, un perceptron SIMPLE puede aprenderla\nX = np.array([[0,0],[0,1],[1,0],[1,1]])\ny = np.array([0,0,0,1])  # AND\n\nnp.random.seed(0)\nw = np.random.normal(0, 0.1, 2)\nb = 0.0\nlr = 0.1  # tasa de aprendizaje\n\ndef escalon(z): return 1 if z >= 0 else 0\n\nerrores_por_epoca = []\nfor epoca in range(15):\n    errores = 0\n    for xi, yi in zip(X, y):\n        z = np.dot(w, xi) + b          # suma ponderada (la 'neurona')\n        pred = escalon(z)               # activacion\n        error = yi - pred\n        if error != 0:\n            errores += 1\n            w = w + lr * error * xi     # ajusta los pesos si se equivoco\n            b = b + lr * error\n    errores_por_epoca.append(errores)\n\nprint(\"pesos finales:\", np.round(w, 3).tolist(), \" sesgo:\", round(b, 3))\nprint(\"errores por epoca (15 epocas):\", errores_por_epoca)\npreds = [escalon(np.dot(w, xi) + b) for xi in X]\nprint(\"predicciones finales [0,0],[0,1],[1,0],[1,1]:\", preds)\nprint(\"esperado (AND):                                \", y.tolist())",
  "viz": {
   "type": "curve",
   "data": {
    "points": [
     3,
     1,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ],
    "xLabel": "época",
    "yLabel": "errores",
    "aria": "Los errores del perceptron caen de 3 a 0 en la tercera epoca y se mantienen en 0 el resto del entrenamiento"
   }
  },
  "application": "El perceptrón original (Rosenblatt, 1957) fue la primera neurona artificial implementada en hardware real — y aunque hoy nadie usa un perceptrón suelto en producción, es la pieza de Lego con la que se construye TODO lo demás: una red neuronal moderna (desde un clasificador de imágenes hasta un modelo de lenguaje) es, por dentro, millones de estas mismas neuronas (suma ponderada + activación) conectadas en capas. Entender esta única neurona es entender el bloque básico de construcción de cualquier red, por gigante que sea (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.10)."
 },
 {
  "name": "Redes Neuronales · La neurona artificial (perceptrón) — pregunta 3",
  "theory": "Una neurona artificial es mucho más simple de lo que suena: toma varios números de entrada, los multiplica cada uno por un \"peso\" (qué tan importante es esa entrada), los suma junto con un \"sesgo\", y pasa ese resultado por una función de activación que decide la salida final. Es literalmente una calculadora de sumas ponderadas — la parte \"inteligente\" está en CÓMO se ajustan esos pesos con la práctica, no en la neurona en sí.<br><br>En el código, un perceptrón (la neurona más simple posible, con activación escalón: 0 o 1) aprende la compuerta lógica AND desde cero. Al principio comete errores (3 de 4 en la primera época), pero cada vez que se equivoca ajusta sus pesos un poquito en la dirección correcta (<code>w = w + lr·error·xi</code>) — para la 3ª época ya no comete NINGÚN error más, y las 4 predicciones finales coinciden exactamente con AND.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.10): una neurona calcula $z = \\sum_i w_i x_i + b$ y aplica una función de activación $\\phi(z)$. La regla de actualización del perceptrón es $w \\leftarrow w + \\eta(y - \\hat{y})x$, donde $\\eta$ es la tasa de aprendizaje.",
  "code": "# La neurona artificial / perceptron (Geron, Cap.10): suma ponderada de\n# las entradas + sesgo, pasada por una funcion de activacion (aqui, un\n# escalon: 0 o 1). Aprende ajustando los pesos cuando se equivoca.\nimport numpy as np\n\n# Compuerta AND: linealmente separable, un perceptron SIMPLE puede aprenderla\nX = np.array([[0,0],[0,1],[1,0],[1,1]])\ny = np.array([0,0,0,1])  # AND\n\nnp.random.seed(0)\nw = np.random.normal(0, 0.1, 2)\nb = 0.0\nlr = 0.1  # tasa de aprendizaje\n\ndef escalon(z): return 1 if z >= 0 else 0\n\nerrores_por_epoca = []\nfor epoca in range(15):\n    errores = 0\n    for xi, yi in zip(X, y):\n        z = np.dot(w, xi) + b          # suma ponderada (la 'neurona')\n        pred = escalon(z)               # activacion\n        error = yi - pred\n        if error != 0:\n            errores += 1\n            w = w + lr * error * xi     # ajusta los pesos si se equivoco\n            b = b + lr * error\n    errores_por_epoca.append(errores)\n\nprint(\"pesos finales:\", np.round(w, 3).tolist(), \" sesgo:\", round(b, 3))\nprint(\"errores por epoca (15 epocas):\", errores_por_epoca)\npreds = [escalon(np.dot(w, xi) + b) for xi in X]\nprint(\"predicciones finales [0,0],[0,1],[1,0],[1,1]:\", preds)\nprint(\"esperado (AND):                                \", y.tolist())",
  "viz": {
   "type": "curve",
   "data": {
    "points": [
     3,
     1,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ],
    "xLabel": "época",
    "yLabel": "errores",
    "aria": "Los errores del perceptron caen de 3 a 0 en la tercera epoca y se mantienen en 0 el resto del entrenamiento"
   }
  },
  "application": "El perceptrón original (Rosenblatt, 1957) fue la primera neurona artificial implementada en hardware real — y aunque hoy nadie usa un perceptrón suelto en producción, es la pieza de Lego con la que se construye TODO lo demás: una red neuronal moderna (desde un clasificador de imágenes hasta un modelo de lenguaje) es, por dentro, millones de estas mismas neuronas (suma ponderada + activación) conectadas en capas. Entender esta única neurona es entender el bloque básico de construcción de cualquier red, por gigante que sea (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.10)."
 },
 {
  "name": "Redes Neuronales · La neurona artificial (perceptrón) — pregunta 4",
  "theory": "Una neurona artificial es mucho más simple de lo que suena: toma varios números de entrada, los multiplica cada uno por un \"peso\" (qué tan importante es esa entrada), los suma junto con un \"sesgo\", y pasa ese resultado por una función de activación que decide la salida final. Es literalmente una calculadora de sumas ponderadas — la parte \"inteligente\" está en CÓMO se ajustan esos pesos con la práctica, no en la neurona en sí.<br><br>En el código, un perceptrón (la neurona más simple posible, con activación escalón: 0 o 1) aprende la compuerta lógica AND desde cero. Al principio comete errores (3 de 4 en la primera época), pero cada vez que se equivoca ajusta sus pesos un poquito en la dirección correcta (<code>w = w + lr·error·xi</code>) — para la 3ª época ya no comete NINGÚN error más, y las 4 predicciones finales coinciden exactamente con AND.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.10): una neurona calcula $z = \\sum_i w_i x_i + b$ y aplica una función de activación $\\phi(z)$. La regla de actualización del perceptrón es $w \\leftarrow w + \\eta(y - \\hat{y})x$, donde $\\eta$ es la tasa de aprendizaje.",
  "code": "# La neurona artificial / perceptron (Geron, Cap.10): suma ponderada de\n# las entradas + sesgo, pasada por una funcion de activacion (aqui, un\n# escalon: 0 o 1). Aprende ajustando los pesos cuando se equivoca.\nimport numpy as np\n\n# Compuerta AND: linealmente separable, un perceptron SIMPLE puede aprenderla\nX = np.array([[0,0],[0,1],[1,0],[1,1]])\ny = np.array([0,0,0,1])  # AND\n\nnp.random.seed(0)\nw = np.random.normal(0, 0.1, 2)\nb = 0.0\nlr = 0.1  # tasa de aprendizaje\n\ndef escalon(z): return 1 if z >= 0 else 0\n\nerrores_por_epoca = []\nfor epoca in range(15):\n    errores = 0\n    for xi, yi in zip(X, y):\n        z = np.dot(w, xi) + b          # suma ponderada (la 'neurona')\n        pred = escalon(z)               # activacion\n        error = yi - pred\n        if error != 0:\n            errores += 1\n            w = w + lr * error * xi     # ajusta los pesos si se equivoco\n            b = b + lr * error\n    errores_por_epoca.append(errores)\n\nprint(\"pesos finales:\", np.round(w, 3).tolist(), \" sesgo:\", round(b, 3))\nprint(\"errores por epoca (15 epocas):\", errores_por_epoca)\npreds = [escalon(np.dot(w, xi) + b) for xi in X]\nprint(\"predicciones finales [0,0],[0,1],[1,0],[1,1]:\", preds)\nprint(\"esperado (AND):                                \", y.tolist())",
  "viz": {
   "type": "curve",
   "data": {
    "points": [
     3,
     1,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0
    ],
    "xLabel": "época",
    "yLabel": "errores",
    "aria": "Los errores del perceptron caen de 3 a 0 en la tercera epoca y se mantienen en 0 el resto del entrenamiento"
   }
  },
  "application": "El perceptrón original (Rosenblatt, 1957) fue la primera neurona artificial implementada en hardware real — y aunque hoy nadie usa un perceptrón suelto en producción, es la pieza de Lego con la que se construye TODO lo demás: una red neuronal moderna (desde un clasificador de imágenes hasta un modelo de lenguaje) es, por dentro, millones de estas mismas neuronas (suma ponderada + activación) conectadas en capas. Entender esta única neurona es entender el bloque básico de construcción de cualquier red, por gigante que sea (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.10)."
 },
 {
  "name": "Redes Neuronales · Capas y activación no lineal",
  "theory": "<b>Idea central</b>: Agregar una capa oculta con activación no lineal resuelve aprender problemas que NO son linealmente separables (como XOR), algo que ningún perceptrón simple puede lograr sin importar cuánto entrene.<br><br><b>Concepto esencial</b>: XOR da 1 solo cuando las dos entradas son DISTINTAS entre sí — es imposible trazar una sola línea recta que deje todos los 1 de un lado y todos los 0 del otro. La capa oculta le permite a la red combinar varias fronteras rectas simples en una frontera final curva/quebrada.<br><br><b>Detalle técnico y código</b>: el perceptrón sin capa oculta se estabiliza en 4 de 4 errores con XOR (apenas 25% de precisión, peor que tirar una moneda); un MLP con 4 neuronas ocultas y ReLU resuelve XOR con 100% de precisión. Formalmente (Géron, Cap.10): un MLP con al menos una capa oculta y activación no lineal es un <i>aproximador universal</i> — puede aproximar cualquier función continua.<br><br><b>Matices y advertencias</b>: la no-linealidad es imprescindible, no un detalle — sin activación no lineal, apilar capas colapsa matemáticamente en una sola capa lineal, tan limitada como el perceptrón original del tema anterior.",
  "code": "# Por que hace falta una CAPA OCULTA con activacion no lineal (Geron, Cap.10):\n# XOR no es linealmente separable -- ninguna linea recta puede separar sus\n# dos clases. Un modelo SIN capa oculta (el MISMO perceptron del tema anterior,\n# solo numpy) no puede resolverlo; un MLP CON una capa oculta (y activacion no\n# lineal) si puede. (Un solo import de sklearn, no dos, para que el sandbox de\n# esta app no se acerque al limite de 12s solo por el costo de importar.)\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\n\nX = np.array([[0,0],[0,1],[1,0],[1,1]])\ny = np.array([0,1,1,0])  # XOR\n\n# 1) perceptron SIN capa oculta (identico al del tema anterior, aplicado a XOR)\nnp.random.seed(0)\nw = np.random.normal(0, 0.1, 2)\nb = 0.0\nlr = 0.1\n\ndef escalon(z): return 1 if z >= 0 else 0\n\nerrores_por_epoca = []\nfor epoca in range(30):\n    errores = 0\n    for xi, yi in zip(X, y):\n        z = np.dot(w, xi) + b\n        pred = escalon(z)\n        error = yi - pred\n        if error != 0:\n            errores += 1\n            w = w + lr * error * xi\n            b = b + lr * error\n    errores_por_epoca.append(errores)\n\nprint(\"perceptron SIN capa oculta -- errores por epoca (30 epocas):\", errores_por_epoca)\npreds_perc = [escalon(np.dot(w, xi) + b) for xi in X]\nacc_perc = sum(p == yy for p, yy in zip(preds_perc, y)) / 4\nprint(\"  predicciones:\", preds_perc, \" esperado:\", y.tolist(), \" accuracy:\", acc_perc)\n\n# 2) MLP CON una capa oculta (1 solo import de sklearn)\nfrom sklearn.neural_network import MLPClassifier\nmlp = MLPClassifier(hidden_layer_sizes=(4,), activation='relu',\n                     max_iter=2000, random_state=1).fit(X, y)\nprint(\"\\nMLP (1 capa oculta de 4 neuronas, ReLU) -- accuracy en XOR:\", mlp.score(X, y))\nprint(\"  predicciones:\", mlp.predict(X).tolist(), \" esperado:\", y.tolist())",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Perceptrón (sin capa oculta)",
     "MLP (1 capa oculta, ReLU)"
    ],
    "values": [
     0.25,
     1.0
    ],
    "unit": "",
    "aria": "El perceptron sin capa oculta acierta solo 25% en XOR (peor que tirar una moneda), mientras que el MLP con capa oculta acierta 100%"
   }
  },
  "application": "Este mismo principio — que hace falta no-linealidad para resolver problemas donde las clases no se separan con una línea recta — es la razón de fondo por la que el deep learning superó a los modelos lineales clásicos en visión por computadora, reconocimiento de voz y procesamiento de lenguaje: casi ningún problema real del mundo (reconocer un gato en una foto, entender una frase ambigua) es linealmente separable en sus datos crudos. Apilar capas con activaciones no lineales (ReLU, sigmoide, tanh) es literalmente lo que le da a una red neuronal la capacidad de aprender fronteras de decisión arbitrariamente complejas (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.10).",
  "codeAnatomy": {
   "title": "MLPClassifier(hidden_layer_sizes=(4,), activation='relu')",
   "caption": "Un MLP con una capa oculta de 4 neuronas y activación ReLU resuelve XOR, algo que el perceptrón sin capa oculta no podía.",
   "lines": [
    "from sklearn.neural_network import MLPClassifier",
    "mlp = MLPClassifier(hidden_layer_sizes=(4,), activation='relu',",
    "                     max_iter=2000, random_state=1).fit(X, y)",
    "print(\"\\nMLP (1 capa oculta de 4 neuronas, ReLU) -- accuracy en XOR:\", mlp.score(X, y))"
   ],
   "annotations": [
    {
     "line": 1,
     "text": "hidden_layer_sizes=(4,)",
     "label": "Capa oculta",
     "desc": "(4 neuronas)",
     "side": "top"
    },
    {
     "line": 1,
     "text": "activation='relu'",
     "label": "Activación no lineal",
     "desc": "(ReLU)",
     "side": "top"
    },
    {
     "line": 2,
     "text": "max_iter=2000",
     "label": "Iteraciones máximas",
     "side": "bottom"
    },
    {
     "line": 2,
     "text": ".fit(X, y)",
     "label": "Entrena",
     "desc": "(sobre XOR)",
     "side": "bottom"
    },
    {
     "line": 3,
     "text": "mlp.score(X, y)",
     "label": "Precisión final",
     "desc": "(accuracy)",
     "side": "bottom"
    }
   ],
   "blockBracket": {
    "from": 1,
    "to": 2,
    "label": "Definición y entrenamiento del MLP con capa oculta"
   }
  }
 },
 {
  "name": "Redes Neuronales · Capas y activación no lineal — pregunta 2",
  "theory": "XOR (\"o exclusivo\") da 1 solo cuando las dos entradas son DISTINTAS entre sí (0,1 o 1,0), y 0 cuando son iguales (0,0 o 1,1). Si graficás esos 4 puntos, es imposible trazar UNA sola línea recta que deje todos los 1 de un lado y todos los 0 del otro — por eso se dice que XOR \"no es linealmente separable\". El MISMO perceptrón sin capa oculta del tema anterior (que aprendía AND perfectamente) queda directamente atascado con XOR: sus errores por época NUNCA llegan a 0 — se estabilizan en 4 de 4 y terminan con apenas 25% de precisión, peor que tirar una moneda.<br><br>Agregar una <b>capa oculta con activación no lineal</b> (como ReLU) cambia todo: en el código, un MLP con 4 neuronas ocultas resuelve XOR con 100% de precisión. La capa oculta le permite a la red combinar varias fronteras rectas simples en una frontera final curva/quebrada — algo que ninguna capa única, por más neuronas que tenga, puede lograr si le sacás la no-linealidad (sin activación no lineal, apilar capas colapsa matemáticamente en una sola capa lineal, tan limitada como el perceptrón original).<br><br>📐 <b>Referencia formal</b> (Géron, Cap.10): un MLP con al menos una capa oculta y activación no lineal es un <i>aproximador universal</i> — puede aproximar cualquier función continua, algo que ningún modelo puramente lineal puede garantizar.",
  "code": "# Por que hace falta una CAPA OCULTA con activacion no lineal (Geron, Cap.10):\n# XOR no es linealmente separable -- ninguna linea recta puede separar sus\n# dos clases. Un modelo SIN capa oculta (el MISMO perceptron del tema anterior,\n# solo numpy) no puede resolverlo; un MLP CON una capa oculta (y activacion no\n# lineal) si puede. (Un solo import de sklearn, no dos, para que el sandbox de\n# esta app no se acerque al limite de 12s solo por el costo de importar.)\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\n\nX = np.array([[0,0],[0,1],[1,0],[1,1]])\ny = np.array([0,1,1,0])  # XOR\n\n# 1) perceptron SIN capa oculta (identico al del tema anterior, aplicado a XOR)\nnp.random.seed(0)\nw = np.random.normal(0, 0.1, 2)\nb = 0.0\nlr = 0.1\n\ndef escalon(z): return 1 if z >= 0 else 0\n\nerrores_por_epoca = []\nfor epoca in range(30):\n    errores = 0\n    for xi, yi in zip(X, y):\n        z = np.dot(w, xi) + b\n        pred = escalon(z)\n        error = yi - pred\n        if error != 0:\n            errores += 1\n            w = w + lr * error * xi\n            b = b + lr * error\n    errores_por_epoca.append(errores)\n\nprint(\"perceptron SIN capa oculta -- errores por epoca (30 epocas):\", errores_por_epoca)\npreds_perc = [escalon(np.dot(w, xi) + b) for xi in X]\nacc_perc = sum(p == yy for p, yy in zip(preds_perc, y)) / 4\nprint(\"  predicciones:\", preds_perc, \" esperado:\", y.tolist(), \" accuracy:\", acc_perc)\n\n# 2) MLP CON una capa oculta (1 solo import de sklearn)\nfrom sklearn.neural_network import MLPClassifier\nmlp = MLPClassifier(hidden_layer_sizes=(4,), activation='relu',\n                     max_iter=2000, random_state=1).fit(X, y)\nprint(\"\\nMLP (1 capa oculta de 4 neuronas, ReLU) -- accuracy en XOR:\", mlp.score(X, y))\nprint(\"  predicciones:\", mlp.predict(X).tolist(), \" esperado:\", y.tolist())",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Perceptrón (sin capa oculta)",
     "MLP (1 capa oculta, ReLU)"
    ],
    "values": [
     0.25,
     1.0
    ],
    "unit": "",
    "aria": "El perceptron sin capa oculta acierta solo 25% en XOR (peor que tirar una moneda), mientras que el MLP con capa oculta acierta 100%"
   }
  },
  "application": "Este mismo principio — que hace falta no-linealidad para resolver problemas donde las clases no se separan con una línea recta — es la razón de fondo por la que el deep learning superó a los modelos lineales clásicos en visión por computadora, reconocimiento de voz y procesamiento de lenguaje: casi ningún problema real del mundo (reconocer un gato en una foto, entender una frase ambigua) es linealmente separable en sus datos crudos. Apilar capas con activaciones no lineales (ReLU, sigmoide, tanh) es literalmente lo que le da a una red neuronal la capacidad de aprender fronteras de decisión arbitrariamente complejas (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.10)."
 },
 {
  "name": "Redes Neuronales · Capas y activación no lineal — pregunta 3",
  "theory": "XOR (\"o exclusivo\") da 1 solo cuando las dos entradas son DISTINTAS entre sí (0,1 o 1,0), y 0 cuando son iguales (0,0 o 1,1). Si graficás esos 4 puntos, es imposible trazar UNA sola línea recta que deje todos los 1 de un lado y todos los 0 del otro — por eso se dice que XOR \"no es linealmente separable\". El MISMO perceptrón sin capa oculta del tema anterior (que aprendía AND perfectamente) queda directamente atascado con XOR: sus errores por época NUNCA llegan a 0 — se estabilizan en 4 de 4 y terminan con apenas 25% de precisión, peor que tirar una moneda.<br><br>Agregar una <b>capa oculta con activación no lineal</b> (como ReLU) cambia todo: en el código, un MLP con 4 neuronas ocultas resuelve XOR con 100% de precisión. La capa oculta le permite a la red combinar varias fronteras rectas simples en una frontera final curva/quebrada — algo que ninguna capa única, por más neuronas que tenga, puede lograr si le sacás la no-linealidad (sin activación no lineal, apilar capas colapsa matemáticamente en una sola capa lineal, tan limitada como el perceptrón original).<br><br>📐 <b>Referencia formal</b> (Géron, Cap.10): un MLP con al menos una capa oculta y activación no lineal es un <i>aproximador universal</i> — puede aproximar cualquier función continua, algo que ningún modelo puramente lineal puede garantizar.",
  "code": "# Por que hace falta una CAPA OCULTA con activacion no lineal (Geron, Cap.10):\n# XOR no es linealmente separable -- ninguna linea recta puede separar sus\n# dos clases. Un modelo SIN capa oculta (el MISMO perceptron del tema anterior,\n# solo numpy) no puede resolverlo; un MLP CON una capa oculta (y activacion no\n# lineal) si puede. (Un solo import de sklearn, no dos, para que el sandbox de\n# esta app no se acerque al limite de 12s solo por el costo de importar.)\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\n\nX = np.array([[0,0],[0,1],[1,0],[1,1]])\ny = np.array([0,1,1,0])  # XOR\n\n# 1) perceptron SIN capa oculta (identico al del tema anterior, aplicado a XOR)\nnp.random.seed(0)\nw = np.random.normal(0, 0.1, 2)\nb = 0.0\nlr = 0.1\n\ndef escalon(z): return 1 if z >= 0 else 0\n\nerrores_por_epoca = []\nfor epoca in range(30):\n    errores = 0\n    for xi, yi in zip(X, y):\n        z = np.dot(w, xi) + b\n        pred = escalon(z)\n        error = yi - pred\n        if error != 0:\n            errores += 1\n            w = w + lr * error * xi\n            b = b + lr * error\n    errores_por_epoca.append(errores)\n\nprint(\"perceptron SIN capa oculta -- errores por epoca (30 epocas):\", errores_por_epoca)\npreds_perc = [escalon(np.dot(w, xi) + b) for xi in X]\nacc_perc = sum(p == yy for p, yy in zip(preds_perc, y)) / 4\nprint(\"  predicciones:\", preds_perc, \" esperado:\", y.tolist(), \" accuracy:\", acc_perc)\n\n# 2) MLP CON una capa oculta (1 solo import de sklearn)\nfrom sklearn.neural_network import MLPClassifier\nmlp = MLPClassifier(hidden_layer_sizes=(4,), activation='relu',\n                     max_iter=2000, random_state=1).fit(X, y)\nprint(\"\\nMLP (1 capa oculta de 4 neuronas, ReLU) -- accuracy en XOR:\", mlp.score(X, y))\nprint(\"  predicciones:\", mlp.predict(X).tolist(), \" esperado:\", y.tolist())",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Perceptrón (sin capa oculta)",
     "MLP (1 capa oculta, ReLU)"
    ],
    "values": [
     0.25,
     1.0
    ],
    "unit": "",
    "aria": "El perceptron sin capa oculta acierta solo 25% en XOR (peor que tirar una moneda), mientras que el MLP con capa oculta acierta 100%"
   }
  },
  "application": "Este mismo principio — que hace falta no-linealidad para resolver problemas donde las clases no se separan con una línea recta — es la razón de fondo por la que el deep learning superó a los modelos lineales clásicos en visión por computadora, reconocimiento de voz y procesamiento de lenguaje: casi ningún problema real del mundo (reconocer un gato en una foto, entender una frase ambigua) es linealmente separable en sus datos crudos. Apilar capas con activaciones no lineales (ReLU, sigmoide, tanh) es literalmente lo que le da a una red neuronal la capacidad de aprender fronteras de decisión arbitrariamente complejas (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.10)."
 },
 {
  "name": "Redes Neuronales · Capas y activación no lineal — pregunta 4",
  "theory": "XOR (\"o exclusivo\") da 1 solo cuando las dos entradas son DISTINTAS entre sí (0,1 o 1,0), y 0 cuando son iguales (0,0 o 1,1). Si graficás esos 4 puntos, es imposible trazar UNA sola línea recta que deje todos los 1 de un lado y todos los 0 del otro — por eso se dice que XOR \"no es linealmente separable\". El MISMO perceptrón sin capa oculta del tema anterior (que aprendía AND perfectamente) queda directamente atascado con XOR: sus errores por época NUNCA llegan a 0 — se estabilizan en 4 de 4 y terminan con apenas 25% de precisión, peor que tirar una moneda.<br><br>Agregar una <b>capa oculta con activación no lineal</b> (como ReLU) cambia todo: en el código, un MLP con 4 neuronas ocultas resuelve XOR con 100% de precisión. La capa oculta le permite a la red combinar varias fronteras rectas simples en una frontera final curva/quebrada — algo que ninguna capa única, por más neuronas que tenga, puede lograr si le sacás la no-linealidad (sin activación no lineal, apilar capas colapsa matemáticamente en una sola capa lineal, tan limitada como el perceptrón original).<br><br>📐 <b>Referencia formal</b> (Géron, Cap.10): un MLP con al menos una capa oculta y activación no lineal es un <i>aproximador universal</i> — puede aproximar cualquier función continua, algo que ningún modelo puramente lineal puede garantizar.",
  "code": "# Por que hace falta una CAPA OCULTA con activacion no lineal (Geron, Cap.10):\n# XOR no es linealmente separable -- ninguna linea recta puede separar sus\n# dos clases. Un modelo SIN capa oculta (el MISMO perceptron del tema anterior,\n# solo numpy) no puede resolverlo; un MLP CON una capa oculta (y activacion no\n# lineal) si puede. (Un solo import de sklearn, no dos, para que el sandbox de\n# esta app no se acerque al limite de 12s solo por el costo de importar.)\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\n\nX = np.array([[0,0],[0,1],[1,0],[1,1]])\ny = np.array([0,1,1,0])  # XOR\n\n# 1) perceptron SIN capa oculta (identico al del tema anterior, aplicado a XOR)\nnp.random.seed(0)\nw = np.random.normal(0, 0.1, 2)\nb = 0.0\nlr = 0.1\n\ndef escalon(z): return 1 if z >= 0 else 0\n\nerrores_por_epoca = []\nfor epoca in range(30):\n    errores = 0\n    for xi, yi in zip(X, y):\n        z = np.dot(w, xi) + b\n        pred = escalon(z)\n        error = yi - pred\n        if error != 0:\n            errores += 1\n            w = w + lr * error * xi\n            b = b + lr * error\n    errores_por_epoca.append(errores)\n\nprint(\"perceptron SIN capa oculta -- errores por epoca (30 epocas):\", errores_por_epoca)\npreds_perc = [escalon(np.dot(w, xi) + b) for xi in X]\nacc_perc = sum(p == yy for p, yy in zip(preds_perc, y)) / 4\nprint(\"  predicciones:\", preds_perc, \" esperado:\", y.tolist(), \" accuracy:\", acc_perc)\n\n# 2) MLP CON una capa oculta (1 solo import de sklearn)\nfrom sklearn.neural_network import MLPClassifier\nmlp = MLPClassifier(hidden_layer_sizes=(4,), activation='relu',\n                     max_iter=2000, random_state=1).fit(X, y)\nprint(\"\\nMLP (1 capa oculta de 4 neuronas, ReLU) -- accuracy en XOR:\", mlp.score(X, y))\nprint(\"  predicciones:\", mlp.predict(X).tolist(), \" esperado:\", y.tolist())",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Perceptrón (sin capa oculta)",
     "MLP (1 capa oculta, ReLU)"
    ],
    "values": [
     0.25,
     1.0
    ],
    "unit": "",
    "aria": "El perceptron sin capa oculta acierta solo 25% en XOR (peor que tirar una moneda), mientras que el MLP con capa oculta acierta 100%"
   }
  },
  "application": "Este mismo principio — que hace falta no-linealidad para resolver problemas donde las clases no se separan con una línea recta — es la razón de fondo por la que el deep learning superó a los modelos lineales clásicos en visión por computadora, reconocimiento de voz y procesamiento de lenguaje: casi ningún problema real del mundo (reconocer un gato en una foto, entender una frase ambigua) es linealmente separable en sus datos crudos. Apilar capas con activaciones no lineales (ReLU, sigmoide, tanh) es literalmente lo que le da a una red neuronal la capacidad de aprender fronteras de decisión arbitrariamente complejas (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.10)."
 },
 {
  "name": "Redes Neuronales · Descenso del gradiente y backpropagation",
  "theory": "<b>Idea central</b>: Backpropagation resuelve calcular, para CADA peso de CADA capa de una red, en qué dirección moverlo para reducir el error — sin eso, no habría forma práctica de entrenar redes con varias capas.<br><br><b>Concepto esencial</b>: Es como bajar una montaña con los ojos vendados: no ves el paisaje completo, pero sentís hacia qué lado baja más el suelo y das un paso en esa dirección — repetido miles de veces, vas bajando hasta un valle de error bajo.<br><br><b>Detalle técnico y código</b>: verificado sobre XOR, el error (<code>loss</code>) arranca en 0,6657 y termina en 0,1039 tras 2000 iteraciones, con 100% de precisión final. Formalmente (Géron, Cap.11): $w \\leftarrow w - \\eta \\frac{\\partial L}{\\partial w}$, donde el gradiente se calcula propagando el error hacia atrás capa por capa mediante la regla de la cadena — de ahí el nombre backpropagation.<br><br><b>Matices y advertencias</b>: \"backpropagation\" describe la DIRECCIÓN del cálculo (de la salida hacia atrás), no una técnica distinta de actualización — el paso final sigue siendo descenso de gradiente estándar, $w \\leftarrow w - \\eta \\cdot \\text{gradiente}$.",
  "code": "# Descenso del gradiente y backpropagation (Geron, Cap.11): en cada\n# iteracion, la red calcula el error (loss), propaga ese error HACIA ATRAS\n# capa por capa (regla de la cadena), y ajusta cada peso en la direccion\n# que MAS reduce el error. loss_curve_ deja ver ese descenso real.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.neural_network import MLPClassifier\n\nX = np.array([[0,0],[0,1],[1,0],[1,1]])\ny = np.array([0,1,1,0])  # XOR, mismo problema del tema anterior\n\nmlp = MLPClassifier(hidden_layer_sizes=(4,), activation='relu', max_iter=2000,\n                     random_state=1, solver='adam').fit(X, y)\nlc = mlp.loss_curve_\nprint(\"iteraciones entrenadas hasta converger:\", len(lc))\n\nidxs = [0, len(lc)//4, len(lc)//2, (3*len(lc))//4, len(lc)-1]\nfor i in idxs:\n    print(f\"iteracion {i+1}: loss={round(lc[i], 4)}\")\n\nprint(\"\\naccuracy final:\", mlp.score(X, y))\nprint(\"el loss bajo de\", round(lc[0], 4), \"a\", round(lc[-1], 4),\n      \"-- cada bajada es un paso de descenso del gradiente\")",
  "viz": {
   "type": "curve",
   "data": {
    "points": [
     0.6657,
     0.5721,
     0.3844,
     0.1971,
     0.1039
    ],
    "xLabel": "iteración (0, 500, 1000, 1500, 2000)",
    "yLabel": "loss (error)",
    "aria": "El error (loss) baja de 0.6657 a 0.1039 a lo largo de 2000 iteraciones de backpropagation"
   }
  },
  "application": "Backpropagation (Rumelhart, Hinton y Williams, 1986) es el algoritmo que hizo viable entrenar redes con muchas capas — sin una forma eficiente de calcular el gradiente de CADA peso, entrenar una red de millones de parámetros (como las que hoy reconocen caras, traducen idiomas o generan texto) sería computacionalmente imposible. Es, junto con el propio descenso del gradiente (que ya viste en el Modo Maestro AO), el motor matemático detrás de literalmente todo el deep learning moderno: la única diferencia entre entrenar un perceptrón simple y una red gigante de cientos de capas es la escala, no el principio (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.11).",
  "codeAnatomy": {
   "title": "El loss baja paso a paso (loss_curve_)",
   "caption": "Cinco puntos del entrenamiento muestran cómo el error (loss) desciende iteración a iteración.",
   "lines": [
    "idxs = [0, len(lc)//4, len(lc)//2, (3*len(lc))//4, len(lc)-1]",
    "for i in idxs:",
    "    print(f\"iteracion {i+1}: loss={round(lc[i], 4)}\")",
    "print(\"el loss bajo de\", round(lc[0], 4), \"a\", round(lc[-1], 4),",
    "      \"-- cada bajada es un paso de descenso del gradiente\")"
   ],
   "annotations": [
    {
     "line": 0,
     "text": "len(lc)-1",
     "label": "Última iteración",
     "desc": "(al converger)",
     "side": "top"
    },
    {
     "line": 1,
     "text": "idxs",
     "label": "Puntos de muestra",
     "desc": "(inicio, 1/4, mitad, 3/4, final)",
     "side": "top"
    },
    {
     "line": 2,
     "text": "round(lc[i], 4)",
     "label": "Valor del error",
     "desc": "(loss en esa iteración)",
     "side": "bottom"
    },
    {
     "line": 3,
     "text": "round(lc[0], 4)",
     "label": "Loss inicial",
     "side": "bottom"
    },
    {
     "line": 4,
     "text": "descenso del gradiente",
     "label": "Cada bajada es un paso",
     "side": "bottom"
    }
   ],
   "blockBracket": {
    "from": 0,
    "to": 2,
    "label": "Muestrea el loss en 5 momentos del entrenamiento"
   }
  }
 },
 {
  "name": "Redes Neuronales · Descenso del gradiente y backpropagation — pregunta 2",
  "theory": "Entrenar una red neuronal es como bajar una montaña con los ojos vendados: no ves el paisaje completo (la función de error real es demasiado compleja para \"verla\" de una), pero podés sentir hacia qué lado del suelo baja más — y das un pasito en esa dirección. Repetís eso miles de veces y, poco a poco, vas bajando hasta un valle (un error bajo). Ese \"sentir hacia dónde baja\" es el gradiente, y el algoritmo que calcula ese gradiente para CADA peso de CADA capa, yendo de atrás hacia adelante, se llama <b>backpropagation</b> (retropropagación).<br><br>En el código, se ve el descenso real, paso a paso: el error (<code>loss</code>) arranca en 0,6657 y termina en 0,1039 después de 2000 iteraciones, con la precisión final llegando al 100% sobre XOR (el mismo problema que una regresión logística no podía resolver ni al 50%). Cada número de <code>loss_curve_</code> es un paso real de descenso del gradiente ya ejecutado — no una simulación ni una aproximación.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.11): en cada iteración se actualiza cada peso como $w \\leftarrow w - \\eta \\frac{\\partial L}{\\partial w}$, donde $\\frac{\\partial L}{\\partial w}$ (el gradiente del error respecto a ese peso) se calcula propagando el error hacia atrás capa por capa mediante la regla de la cadena — de ahí el nombre backpropagation.",
  "code": "# Descenso del gradiente y backpropagation (Geron, Cap.11): en cada\n# iteracion, la red calcula el error (loss), propaga ese error HACIA ATRAS\n# capa por capa (regla de la cadena), y ajusta cada peso en la direccion\n# que MAS reduce el error. loss_curve_ deja ver ese descenso real.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.neural_network import MLPClassifier\n\nX = np.array([[0,0],[0,1],[1,0],[1,1]])\ny = np.array([0,1,1,0])  # XOR, mismo problema del tema anterior\n\nmlp = MLPClassifier(hidden_layer_sizes=(4,), activation='relu', max_iter=2000,\n                     random_state=1, solver='adam').fit(X, y)\nlc = mlp.loss_curve_\nprint(\"iteraciones entrenadas hasta converger:\", len(lc))\n\nidxs = [0, len(lc)//4, len(lc)//2, (3*len(lc))//4, len(lc)-1]\nfor i in idxs:\n    print(f\"iteracion {i+1}: loss={round(lc[i], 4)}\")\n\nprint(\"\\naccuracy final:\", mlp.score(X, y))\nprint(\"el loss bajo de\", round(lc[0], 4), \"a\", round(lc[-1], 4),\n      \"-- cada bajada es un paso de descenso del gradiente\")",
  "viz": {
   "type": "curve",
   "data": {
    "points": [
     0.6657,
     0.5721,
     0.3844,
     0.1971,
     0.1039
    ],
    "xLabel": "iteración (0, 500, 1000, 1500, 2000)",
    "yLabel": "loss (error)",
    "aria": "El error (loss) baja de 0.6657 a 0.1039 a lo largo de 2000 iteraciones de backpropagation"
   }
  },
  "application": "Backpropagation (Rumelhart, Hinton y Williams, 1986) es el algoritmo que hizo viable entrenar redes con muchas capas — sin una forma eficiente de calcular el gradiente de CADA peso, entrenar una red de millones de parámetros (como las que hoy reconocen caras, traducen idiomas o generan texto) sería computacionalmente imposible. Es, junto con el propio descenso del gradiente (que ya viste en el Modo Maestro AO), el motor matemático detrás de literalmente todo el deep learning moderno: la única diferencia entre entrenar un perceptrón simple y una red gigante de cientos de capas es la escala, no el principio (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.11)."
 },
 {
  "name": "Redes Neuronales · Descenso del gradiente y backpropagation — pregunta 3",
  "theory": "Entrenar una red neuronal es como bajar una montaña con los ojos vendados: no ves el paisaje completo (la función de error real es demasiado compleja para \"verla\" de una), pero podés sentir hacia qué lado del suelo baja más — y das un pasito en esa dirección. Repetís eso miles de veces y, poco a poco, vas bajando hasta un valle (un error bajo). Ese \"sentir hacia dónde baja\" es el gradiente, y el algoritmo que calcula ese gradiente para CADA peso de CADA capa, yendo de atrás hacia adelante, se llama <b>backpropagation</b> (retropropagación).<br><br>En el código, se ve el descenso real, paso a paso: el error (<code>loss</code>) arranca en 0,6657 y termina en 0,1039 después de 2000 iteraciones, con la precisión final llegando al 100% sobre XOR (el mismo problema que una regresión logística no podía resolver ni al 50%). Cada número de <code>loss_curve_</code> es un paso real de descenso del gradiente ya ejecutado — no una simulación ni una aproximación.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.11): en cada iteración se actualiza cada peso como $w \\leftarrow w - \\eta \\frac{\\partial L}{\\partial w}$, donde $\\frac{\\partial L}{\\partial w}$ (el gradiente del error respecto a ese peso) se calcula propagando el error hacia atrás capa por capa mediante la regla de la cadena — de ahí el nombre backpropagation.",
  "code": "# Descenso del gradiente y backpropagation (Geron, Cap.11): en cada\n# iteracion, la red calcula el error (loss), propaga ese error HACIA ATRAS\n# capa por capa (regla de la cadena), y ajusta cada peso en la direccion\n# que MAS reduce el error. loss_curve_ deja ver ese descenso real.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.neural_network import MLPClassifier\n\nX = np.array([[0,0],[0,1],[1,0],[1,1]])\ny = np.array([0,1,1,0])  # XOR, mismo problema del tema anterior\n\nmlp = MLPClassifier(hidden_layer_sizes=(4,), activation='relu', max_iter=2000,\n                     random_state=1, solver='adam').fit(X, y)\nlc = mlp.loss_curve_\nprint(\"iteraciones entrenadas hasta converger:\", len(lc))\n\nidxs = [0, len(lc)//4, len(lc)//2, (3*len(lc))//4, len(lc)-1]\nfor i in idxs:\n    print(f\"iteracion {i+1}: loss={round(lc[i], 4)}\")\n\nprint(\"\\naccuracy final:\", mlp.score(X, y))\nprint(\"el loss bajo de\", round(lc[0], 4), \"a\", round(lc[-1], 4),\n      \"-- cada bajada es un paso de descenso del gradiente\")",
  "viz": {
   "type": "curve",
   "data": {
    "points": [
     0.6657,
     0.5721,
     0.3844,
     0.1971,
     0.1039
    ],
    "xLabel": "iteración (0, 500, 1000, 1500, 2000)",
    "yLabel": "loss (error)",
    "aria": "El error (loss) baja de 0.6657 a 0.1039 a lo largo de 2000 iteraciones de backpropagation"
   }
  },
  "application": "Backpropagation (Rumelhart, Hinton y Williams, 1986) es el algoritmo que hizo viable entrenar redes con muchas capas — sin una forma eficiente de calcular el gradiente de CADA peso, entrenar una red de millones de parámetros (como las que hoy reconocen caras, traducen idiomas o generan texto) sería computacionalmente imposible. Es, junto con el propio descenso del gradiente (que ya viste en el Modo Maestro AO), el motor matemático detrás de literalmente todo el deep learning moderno: la única diferencia entre entrenar un perceptrón simple y una red gigante de cientos de capas es la escala, no el principio (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.11)."
 },
 {
  "name": "Redes Neuronales · Descenso del gradiente y backpropagation — pregunta 4",
  "theory": "Entrenar una red neuronal es como bajar una montaña con los ojos vendados: no ves el paisaje completo (la función de error real es demasiado compleja para \"verla\" de una), pero podés sentir hacia qué lado del suelo baja más — y das un pasito en esa dirección. Repetís eso miles de veces y, poco a poco, vas bajando hasta un valle (un error bajo). Ese \"sentir hacia dónde baja\" es el gradiente, y el algoritmo que calcula ese gradiente para CADA peso de CADA capa, yendo de atrás hacia adelante, se llama <b>backpropagation</b> (retropropagación).<br><br>En el código, se ve el descenso real, paso a paso: el error (<code>loss</code>) arranca en 0,6657 y termina en 0,1039 después de 2000 iteraciones, con la precisión final llegando al 100% sobre XOR (el mismo problema que una regresión logística no podía resolver ni al 50%). Cada número de <code>loss_curve_</code> es un paso real de descenso del gradiente ya ejecutado — no una simulación ni una aproximación.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.11): en cada iteración se actualiza cada peso como $w \\leftarrow w - \\eta \\frac{\\partial L}{\\partial w}$, donde $\\frac{\\partial L}{\\partial w}$ (el gradiente del error respecto a ese peso) se calcula propagando el error hacia atrás capa por capa mediante la regla de la cadena — de ahí el nombre backpropagation.",
  "code": "# Descenso del gradiente y backpropagation (Geron, Cap.11): en cada\n# iteracion, la red calcula el error (loss), propaga ese error HACIA ATRAS\n# capa por capa (regla de la cadena), y ajusta cada peso en la direccion\n# que MAS reduce el error. loss_curve_ deja ver ese descenso real.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.neural_network import MLPClassifier\n\nX = np.array([[0,0],[0,1],[1,0],[1,1]])\ny = np.array([0,1,1,0])  # XOR, mismo problema del tema anterior\n\nmlp = MLPClassifier(hidden_layer_sizes=(4,), activation='relu', max_iter=2000,\n                     random_state=1, solver='adam').fit(X, y)\nlc = mlp.loss_curve_\nprint(\"iteraciones entrenadas hasta converger:\", len(lc))\n\nidxs = [0, len(lc)//4, len(lc)//2, (3*len(lc))//4, len(lc)-1]\nfor i in idxs:\n    print(f\"iteracion {i+1}: loss={round(lc[i], 4)}\")\n\nprint(\"\\naccuracy final:\", mlp.score(X, y))\nprint(\"el loss bajo de\", round(lc[0], 4), \"a\", round(lc[-1], 4),\n      \"-- cada bajada es un paso de descenso del gradiente\")",
  "viz": {
   "type": "curve",
   "data": {
    "points": [
     0.6657,
     0.5721,
     0.3844,
     0.1971,
     0.1039
    ],
    "xLabel": "iteración (0, 500, 1000, 1500, 2000)",
    "yLabel": "loss (error)",
    "aria": "El error (loss) baja de 0.6657 a 0.1039 a lo largo de 2000 iteraciones de backpropagation"
   }
  },
  "application": "Backpropagation (Rumelhart, Hinton y Williams, 1986) es el algoritmo que hizo viable entrenar redes con muchas capas — sin una forma eficiente de calcular el gradiente de CADA peso, entrenar una red de millones de parámetros (como las que hoy reconocen caras, traducen idiomas o generan texto) sería computacionalmente imposible. Es, junto con el propio descenso del gradiente (que ya viste en el Modo Maestro AO), el motor matemático detrás de literalmente todo el deep learning moderno: la única diferencia entre entrenar un perceptrón simple y una red gigante de cientos de capas es la escala, no el principio (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.11)."
 },
 {
  "name": "Redes Neuronales · Convolución y Pooling (CNN)",
  "theory": "<b>Idea central</b>: La capa convolucional resuelve reconocer patrones visuales (bordes, esquinas) sin conectar cada neurona con TODOS los píxeles de la imagen, evitando un número de conexiones inmanejable.<br><br><b>Concepto esencial</b>: Un patrón visual casi siempre se reconoce mirando un pedacito chico de la imagen a la vez — un filtro (<b>kernel</b>) chiquito se desliza sobre la imagen y se REUTILIZA en cada posición, en vez de tener un peso distinto por cada píxel como una capa densa.<br><br><b>Detalle técnico y código</b>: un kernel Sobel 3×3 deslizado sobre una imagen con un borde vertical marcado da un <i>feature map</i> con valor 4 exacto en la columna del borde y 0 en el resto — el filtro \"ilumina\" dónde está el patrón. El max-pooling después reduce 6×6 a 3×3 quedándose con el valor más fuerte de cada bloque 2×2. Formalmente (Géron, Cap.14): $S(i,j) = \\sum_{m,n} I(i{+}m, j{+}n) \\cdot K(m,n)$, mismo kernel reutilizado en toda la imagen.<br><br><b>Matices y advertencias</b>: a diferencia de una capa densa (cada conexión con su propio peso independiente), el kernel compartido es justo lo que hace viable procesar imágenes grandes — la contrapartida es que un kernel fijo, no aprendido (como el Sobel de este ejemplo), solo detecta el patrón para el que fue diseñado.",
  "code": "# Convolucion y Pooling (Geron, Cap.14 'Deep Computer Vision'): el\n# mecanismo detras de las redes convolucionales (CNN). Implementado con\n# numpy puro (sin TensorFlow/Keras, no instalados aqui) para ver la\n# mecanica exacta, linea por linea.\nimport numpy as np\n\n# imagen 8x8: mitad oscura (0), mitad clara (1) -- un borde vertical clarisimo\nimg = np.zeros((8, 8))\nimg[:, 4:] = 1.0\nprint(\"imagen (0=oscuro, 1=claro):\")\nprint(img.astype(int))\n\n# kernel Sobel vertical: un filtro clasico que detecta bordes VERTICALES\n# (cambios bruscos de brillo de izquierda a derecha)\nkernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)\nprint(\"\\nkernel (filtro) Sobel vertical:\")\nprint(kernel)\n\ndef convolucion(imagen, kernel):\n    kh, kw = kernel.shape\n    h, w = imagen.shape\n    oh, ow = h - kh + 1, w - kw + 1\n    salida = np.zeros((oh, ow))\n    for i in range(oh):\n        for j in range(ow):\n            region = imagen[i:i+kh, j:j+kw]   # ventana deslizante\n            salida[i, j] = np.sum(region * kernel)  # producto punto a punto\n    return salida\n\nmapa = convolucion(img, kernel)\nprint(\"\\nmapa de caracteristicas (feature map) tras aplicar el filtro:\")\nprint(np.round(mapa, 1))\n\ndef max_pooling(mapa, tam=2):\n    h, w = mapa.shape\n    oh, ow = h // tam, w // tam\n    salida = np.zeros((oh, ow))\n    for i in range(oh):\n        for j in range(ow):\n            region = mapa[i*tam:(i+1)*tam, j*tam:(j+1)*tam]\n            salida[i, j] = region.max()   # se queda con el valor MAS FUERTE\n    return salida\n\npooled = max_pooling(mapa, 2)\nprint(\"\\ntras max-pooling 2x2 (reduce tamano, conserva la señal mas fuerte):\")\nprint(np.round(pooled, 1))\nprint(\"forma original del mapa:\", mapa.shape, \" forma tras pooling:\", pooled.shape)",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 6,
    "cols": 6,
    "barMode": false,
    "values": [
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ]
    ],
    "min": 0,
    "max": 4,
    "aria": "El mapa de caracteristicas tiene valor 4 exactamente en la columna del borde vertical, 0 en el resto"
   }
  },
  "application": "Este mismo mecanismo — filtros que se deslizan detectando patrones locales, apilados en capas cada vez más profundas — es la base de prácticamente toda la visión por computadora moderna: reconocimiento facial en el desbloqueo de celulares, detección de peatones en autos autónomos, diagnóstico de imágenes médicas (radiografías, resonancias), y los filtros de Instagram que detectan tu cara para poner orejas de perrito. Las primeras capas de una CNN aprenden filtros simples (bordes, como el Sobel de este ejemplo); las capas más profundas combinan esos bordes en formas, y las más profundas todavía en objetos completos (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.14).",
  "codeAnatomy": {
   "title": "salida[i, j] = np.sum(region * kernel)",
   "caption": "El núcleo de la convolución: desliza una ventana del tamaño del kernel sobre la imagen y multiplica punto a punto.",
   "lines": [
    "    for i in range(oh):",
    "        for j in range(ow):",
    "            region = imagen[i:i+kh, j:j+kw]   # ventana deslizante",
    "            salida[i, j] = np.sum(region * kernel)  # producto punto a punto"
   ],
   "annotations": [
    {
     "line": 0,
     "text": "range(oh)",
     "label": "Filas de salida",
     "side": "top"
    },
    {
     "line": 1,
     "text": "range(ow)",
     "label": "Columnas de salida",
     "side": "top"
    },
    {
     "line": 2,
     "text": "imagen[i:i+kh, j:j+kw]",
     "label": "Ventana deslizante",
     "desc": "(recorte del tamaño del kernel)",
     "side": "bottom"
    },
    {
     "line": 3,
     "text": "np.sum(region * kernel)",
     "label": "Producto punto a punto",
     "desc": "(resultado de esa posición)",
     "side": "bottom"
    },
    {
     "line": 3,
     "text": "salida[i, j]",
     "label": "Guarda en el mapa",
     "desc": "(feature map)",
     "side": "bottom"
    }
   ],
   "blockBracket": {
    "from": 0,
    "to": 3,
    "label": "Doble bucle: desliza el kernel por toda la imagen"
   }
  }
 },
 {
  "name": "Redes Neuronales · Convolución y Pooling (CNN) — pregunta 2",
  "theory": "Una capa densa (las que ya viste en los temas anteriores) conecta CADA neurona con TODOS los píxeles de la imagen — para una foto de 200×200 píxeles, eso ya son 40.000 conexiones por neurona, un desperdicio enorme, porque un patrón visual (un borde, una esquina) casi siempre se reconoce mirando solo un PEDACITO chico de la imagen a la vez, no la imagen entera. La <b>capa convolucional</b> resuelve esto: en vez de conectar todo con todo, desliza un \"filtro\" chiquito (el <b>kernel</b>) sobre la imagen, mirando de a un pedacito, y reutiliza EL MISMO filtro en cada posición — muchas menos conexiones, y el mismo patrón se detecta sin importar en qué parte de la imagen aparezca.<br><br>En el código, un kernel Sobel de 3×3 (un filtro clásico, no aprendido, para ver la mecánica clara) se desliza sobre una imagen con un borde vertical bien marcado. El resultado (el <i>feature map</i>) tiene un valor <b>4</b> exactamente en la columna donde está el borde, y <b>0</b> en todos los demás lugares — el filtro literalmente \"ilumina\" dónde está el patrón que busca. Después, el <b>max-pooling</b> reduce el tamaño del mapa (de 6×6 a 3×3) quedándose con el valor MÁS FUERTE de cada bloque de 2×2 — resume la información conservando lo más importante, y hace que la red sea un poco más tolerante a pequeños corrimientos de posición del patrón.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.14): una convolución 2D calcula $S(i,j) = \\sum_{m,n} I(i{+}m, j{+}n) \\cdot K(m,n)$ para cada posición $(i,j)$ de la imagen $I$ con el kernel $K$ — el mismo kernel (mismos pesos) se reutiliza en toda la imagen, a diferencia de una capa densa donde cada conexión tiene su propio peso independiente.",
  "code": "# Convolucion y Pooling (Geron, Cap.14 'Deep Computer Vision'): el\n# mecanismo detras de las redes convolucionales (CNN). Implementado con\n# numpy puro (sin TensorFlow/Keras, no instalados aqui) para ver la\n# mecanica exacta, linea por linea.\nimport numpy as np\n\n# imagen 8x8: mitad oscura (0), mitad clara (1) -- un borde vertical clarisimo\nimg = np.zeros((8, 8))\nimg[:, 4:] = 1.0\nprint(\"imagen (0=oscuro, 1=claro):\")\nprint(img.astype(int))\n\n# kernel Sobel vertical: un filtro clasico que detecta bordes VERTICALES\n# (cambios bruscos de brillo de izquierda a derecha)\nkernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)\nprint(\"\\nkernel (filtro) Sobel vertical:\")\nprint(kernel)\n\ndef convolucion(imagen, kernel):\n    kh, kw = kernel.shape\n    h, w = imagen.shape\n    oh, ow = h - kh + 1, w - kw + 1\n    salida = np.zeros((oh, ow))\n    for i in range(oh):\n        for j in range(ow):\n            region = imagen[i:i+kh, j:j+kw]   # ventana deslizante\n            salida[i, j] = np.sum(region * kernel)  # producto punto a punto\n    return salida\n\nmapa = convolucion(img, kernel)\nprint(\"\\nmapa de caracteristicas (feature map) tras aplicar el filtro:\")\nprint(np.round(mapa, 1))\n\ndef max_pooling(mapa, tam=2):\n    h, w = mapa.shape\n    oh, ow = h // tam, w // tam\n    salida = np.zeros((oh, ow))\n    for i in range(oh):\n        for j in range(ow):\n            region = mapa[i*tam:(i+1)*tam, j*tam:(j+1)*tam]\n            salida[i, j] = region.max()   # se queda con el valor MAS FUERTE\n    return salida\n\npooled = max_pooling(mapa, 2)\nprint(\"\\ntras max-pooling 2x2 (reduce tamano, conserva la señal mas fuerte):\")\nprint(np.round(pooled, 1))\nprint(\"forma original del mapa:\", mapa.shape, \" forma tras pooling:\", pooled.shape)",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 6,
    "cols": 6,
    "barMode": false,
    "values": [
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ]
    ],
    "min": 0,
    "max": 4,
    "aria": "El mapa de caracteristicas tiene valor 4 exactamente en la columna del borde vertical, 0 en el resto"
   }
  },
  "application": "Este mismo mecanismo — filtros que se deslizan detectando patrones locales, apilados en capas cada vez más profundas — es la base de prácticamente toda la visión por computadora moderna: reconocimiento facial en el desbloqueo de celulares, detección de peatones en autos autónomos, diagnóstico de imágenes médicas (radiografías, resonancias), y los filtros de Instagram que detectan tu cara para poner orejas de perrito. Las primeras capas de una CNN aprenden filtros simples (bordes, como el Sobel de este ejemplo); las capas más profundas combinan esos bordes en formas, y las más profundas todavía en objetos completos (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.14)."
 },
 {
  "name": "Redes Neuronales · Convolución y Pooling (CNN) — pregunta 3",
  "theory": "Una capa densa (las que ya viste en los temas anteriores) conecta CADA neurona con TODOS los píxeles de la imagen — para una foto de 200×200 píxeles, eso ya son 40.000 conexiones por neurona, un desperdicio enorme, porque un patrón visual (un borde, una esquina) casi siempre se reconoce mirando solo un PEDACITO chico de la imagen a la vez, no la imagen entera. La <b>capa convolucional</b> resuelve esto: en vez de conectar todo con todo, desliza un \"filtro\" chiquito (el <b>kernel</b>) sobre la imagen, mirando de a un pedacito, y reutiliza EL MISMO filtro en cada posición — muchas menos conexiones, y el mismo patrón se detecta sin importar en qué parte de la imagen aparezca.<br><br>En el código, un kernel Sobel de 3×3 (un filtro clásico, no aprendido, para ver la mecánica clara) se desliza sobre una imagen con un borde vertical bien marcado. El resultado (el <i>feature map</i>) tiene un valor <b>4</b> exactamente en la columna donde está el borde, y <b>0</b> en todos los demás lugares — el filtro literalmente \"ilumina\" dónde está el patrón que busca. Después, el <b>max-pooling</b> reduce el tamaño del mapa (de 6×6 a 3×3) quedándose con el valor MÁS FUERTE de cada bloque de 2×2 — resume la información conservando lo más importante, y hace que la red sea un poco más tolerante a pequeños corrimientos de posición del patrón.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.14): una convolución 2D calcula $S(i,j) = \\sum_{m,n} I(i{+}m, j{+}n) \\cdot K(m,n)$ para cada posición $(i,j)$ de la imagen $I$ con el kernel $K$ — el mismo kernel (mismos pesos) se reutiliza en toda la imagen, a diferencia de una capa densa donde cada conexión tiene su propio peso independiente.",
  "code": "# Convolucion y Pooling (Geron, Cap.14 'Deep Computer Vision'): el\n# mecanismo detras de las redes convolucionales (CNN). Implementado con\n# numpy puro (sin TensorFlow/Keras, no instalados aqui) para ver la\n# mecanica exacta, linea por linea.\nimport numpy as np\n\n# imagen 8x8: mitad oscura (0), mitad clara (1) -- un borde vertical clarisimo\nimg = np.zeros((8, 8))\nimg[:, 4:] = 1.0\nprint(\"imagen (0=oscuro, 1=claro):\")\nprint(img.astype(int))\n\n# kernel Sobel vertical: un filtro clasico que detecta bordes VERTICALES\n# (cambios bruscos de brillo de izquierda a derecha)\nkernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)\nprint(\"\\nkernel (filtro) Sobel vertical:\")\nprint(kernel)\n\ndef convolucion(imagen, kernel):\n    kh, kw = kernel.shape\n    h, w = imagen.shape\n    oh, ow = h - kh + 1, w - kw + 1\n    salida = np.zeros((oh, ow))\n    for i in range(oh):\n        for j in range(ow):\n            region = imagen[i:i+kh, j:j+kw]   # ventana deslizante\n            salida[i, j] = np.sum(region * kernel)  # producto punto a punto\n    return salida\n\nmapa = convolucion(img, kernel)\nprint(\"\\nmapa de caracteristicas (feature map) tras aplicar el filtro:\")\nprint(np.round(mapa, 1))\n\ndef max_pooling(mapa, tam=2):\n    h, w = mapa.shape\n    oh, ow = h // tam, w // tam\n    salida = np.zeros((oh, ow))\n    for i in range(oh):\n        for j in range(ow):\n            region = mapa[i*tam:(i+1)*tam, j*tam:(j+1)*tam]\n            salida[i, j] = region.max()   # se queda con el valor MAS FUERTE\n    return salida\n\npooled = max_pooling(mapa, 2)\nprint(\"\\ntras max-pooling 2x2 (reduce tamano, conserva la señal mas fuerte):\")\nprint(np.round(pooled, 1))\nprint(\"forma original del mapa:\", mapa.shape, \" forma tras pooling:\", pooled.shape)",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 6,
    "cols": 6,
    "barMode": false,
    "values": [
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ]
    ],
    "min": 0,
    "max": 4,
    "aria": "El mapa de caracteristicas tiene valor 4 exactamente en la columna del borde vertical, 0 en el resto"
   }
  },
  "application": "Este mismo mecanismo — filtros que se deslizan detectando patrones locales, apilados en capas cada vez más profundas — es la base de prácticamente toda la visión por computadora moderna: reconocimiento facial en el desbloqueo de celulares, detección de peatones en autos autónomos, diagnóstico de imágenes médicas (radiografías, resonancias), y los filtros de Instagram que detectan tu cara para poner orejas de perrito. Las primeras capas de una CNN aprenden filtros simples (bordes, como el Sobel de este ejemplo); las capas más profundas combinan esos bordes en formas, y las más profundas todavía en objetos completos (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.14)."
 },
 {
  "name": "Redes Neuronales · Convolución y Pooling (CNN) — pregunta 4",
  "theory": "Una capa densa (las que ya viste en los temas anteriores) conecta CADA neurona con TODOS los píxeles de la imagen — para una foto de 200×200 píxeles, eso ya son 40.000 conexiones por neurona, un desperdicio enorme, porque un patrón visual (un borde, una esquina) casi siempre se reconoce mirando solo un PEDACITO chico de la imagen a la vez, no la imagen entera. La <b>capa convolucional</b> resuelve esto: en vez de conectar todo con todo, desliza un \"filtro\" chiquito (el <b>kernel</b>) sobre la imagen, mirando de a un pedacito, y reutiliza EL MISMO filtro en cada posición — muchas menos conexiones, y el mismo patrón se detecta sin importar en qué parte de la imagen aparezca.<br><br>En el código, un kernel Sobel de 3×3 (un filtro clásico, no aprendido, para ver la mecánica clara) se desliza sobre una imagen con un borde vertical bien marcado. El resultado (el <i>feature map</i>) tiene un valor <b>4</b> exactamente en la columna donde está el borde, y <b>0</b> en todos los demás lugares — el filtro literalmente \"ilumina\" dónde está el patrón que busca. Después, el <b>max-pooling</b> reduce el tamaño del mapa (de 6×6 a 3×3) quedándose con el valor MÁS FUERTE de cada bloque de 2×2 — resume la información conservando lo más importante, y hace que la red sea un poco más tolerante a pequeños corrimientos de posición del patrón.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.14): una convolución 2D calcula $S(i,j) = \\sum_{m,n} I(i{+}m, j{+}n) \\cdot K(m,n)$ para cada posición $(i,j)$ de la imagen $I$ con el kernel $K$ — el mismo kernel (mismos pesos) se reutiliza en toda la imagen, a diferencia de una capa densa donde cada conexión tiene su propio peso independiente.",
  "code": "# Convolucion y Pooling (Geron, Cap.14 'Deep Computer Vision'): el\n# mecanismo detras de las redes convolucionales (CNN). Implementado con\n# numpy puro (sin TensorFlow/Keras, no instalados aqui) para ver la\n# mecanica exacta, linea por linea.\nimport numpy as np\n\n# imagen 8x8: mitad oscura (0), mitad clara (1) -- un borde vertical clarisimo\nimg = np.zeros((8, 8))\nimg[:, 4:] = 1.0\nprint(\"imagen (0=oscuro, 1=claro):\")\nprint(img.astype(int))\n\n# kernel Sobel vertical: un filtro clasico que detecta bordes VERTICALES\n# (cambios bruscos de brillo de izquierda a derecha)\nkernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)\nprint(\"\\nkernel (filtro) Sobel vertical:\")\nprint(kernel)\n\ndef convolucion(imagen, kernel):\n    kh, kw = kernel.shape\n    h, w = imagen.shape\n    oh, ow = h - kh + 1, w - kw + 1\n    salida = np.zeros((oh, ow))\n    for i in range(oh):\n        for j in range(ow):\n            region = imagen[i:i+kh, j:j+kw]   # ventana deslizante\n            salida[i, j] = np.sum(region * kernel)  # producto punto a punto\n    return salida\n\nmapa = convolucion(img, kernel)\nprint(\"\\nmapa de caracteristicas (feature map) tras aplicar el filtro:\")\nprint(np.round(mapa, 1))\n\ndef max_pooling(mapa, tam=2):\n    h, w = mapa.shape\n    oh, ow = h // tam, w // tam\n    salida = np.zeros((oh, ow))\n    for i in range(oh):\n        for j in range(ow):\n            region = mapa[i*tam:(i+1)*tam, j*tam:(j+1)*tam]\n            salida[i, j] = region.max()   # se queda con el valor MAS FUERTE\n    return salida\n\npooled = max_pooling(mapa, 2)\nprint(\"\\ntras max-pooling 2x2 (reduce tamano, conserva la señal mas fuerte):\")\nprint(np.round(pooled, 1))\nprint(\"forma original del mapa:\", mapa.shape, \" forma tras pooling:\", pooled.shape)",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 6,
    "cols": 6,
    "barMode": false,
    "values": [
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ],
     [
      0,
      0,
      4,
      4,
      0,
      0
     ]
    ],
    "min": 0,
    "max": 4,
    "aria": "El mapa de caracteristicas tiene valor 4 exactamente en la columna del borde vertical, 0 en el resto"
   }
  },
  "application": "Este mismo mecanismo — filtros que se deslizan detectando patrones locales, apilados en capas cada vez más profundas — es la base de prácticamente toda la visión por computadora moderna: reconocimiento facial en el desbloqueo de celulares, detección de peatones en autos autónomos, diagnóstico de imágenes médicas (radiografías, resonancias), y los filtros de Instagram que detectan tu cara para poner orejas de perrito. Las primeras capas de una CNN aprenden filtros simples (bordes, como el Sobel de este ejemplo); las capas más profundas combinan esos bordes en formas, y las más profundas todavía en objetos completos (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.14)."
 },
 {
  "name": "Redes Neuronales · Dropout",
  "theory": "<b>Idea central</b>: Dropout resuelve evitar que una red dependa demasiado de neuronas específicas, apagando al azar un porcentaje de ellas en cada paso de entrenamiento.<br><br><b>Concepto esencial</b>: Es como practicar un examen grupal sorteando al azar la mitad del equipo en cada práctica — nadie puede depender de un compañero fijo, todos tienen que aprender un poco de todo porque nunca saben quién va a faltar.<br><br><b>Detalle técnico y código</b>: con p=0.5, en el paso 1 se apagan 7 de 8 neuronas, en el paso 2 otras 4 totalmente distintas — cada paso entrena una red ligeramente diferente. Las que quedan activas se dividen por keep=1-p (<i>inverted dropout</i>) para compensar. Verificado repitiendo el sorteo 2000 veces: la fracción real de apagados por neurona promedia 0,504, casi igual al p=0,5 configurado. Formalmente (Géron, Cap.11, p.383-385): cada neurona tiene probabilidad $p$ de ser ignorada ese paso.<br><br><b>Matices y advertencias</b>: Dropout SOLO actúa en entrenamiento — en inferencia se desactiva por completo (las 8 neuronas activas, sin apagar ni escalar nada); aplicarlo también en inferencia es un error común que degrada la red sin ningún beneficio.",
  "code": "# Dropout (Geron, Cap.11 'Training Deep Neural Networks', seccion 'Dropout',\n# p.383-385): en cada paso de ENTRENAMIENTO, cada neurona tiene una\n# probabilidad p de apagarse por completo para ese paso (Srivastava et al.,\n# 2014). Aqui se ve el mecanismo real sobre una capa oculta de 8 neuronas,\n# sin TensorFlow/Keras (no instalados en este sandbox), con numpy puro.\nimport numpy as np\n\n# activaciones de una capa oculta de 8 neuronas: resultado REAL de un\n# forward pass (entrada -> pesos -> ReLU), no numeros inventados\nnp.random.seed(13)\nx = np.array([0.5, -0.2, 1.1, 0.3])\nW = np.random.normal(0, 0.6, (4, 8))\nb = np.random.normal(0.15, 0.1, 8)\nh = np.maximum(0, x @ W + b)\nprint(\"activaciones de la capa oculta (sin dropout):\", np.round(h, 3).tolist())\n\np = 0.5       # dropout rate: probabilidad de apagar cada neurona\nkeep = 1 - p  # keep probability\n\nprint(f\"\\n4 pasos de ENTRENAMIENTO distintos, dropout p={p}:\")\nnp.random.seed(1)\nfor paso in range(1, 5):\n    mask = (np.random.rand(len(h)) > p).astype(float)   # 1=activa, 0=apagada\n    h_drop = h * mask / keep   # inverted dropout: se escala para compensar\n    apagadas = np.where(mask == 0)[0].tolist()\n    print(f\"paso {paso}: neuronas apagadas={apagadas}  salida={np.round(h_drop, 2).tolist()}\")\n\nprint(\"\\nINFERENCIA (despues de entrenar, dropout desactivado):\")\nprint(\"salida:\", np.round(h, 3).tolist(), \"-- todas las neuronas activas, sin escalar\")\n\n# verificacion estadistica: en miles de pasos, la fraccion real de apagados\n# debe rondar el p configurado (vectorizado, sin bucle Python largo)\nnp.random.seed(3)\nn_pasos = 2000\nmasks_stat = (np.random.rand(n_pasos, len(h)) > p).astype(float)\nfrac_apagada = 1 - masks_stat.mean(axis=0)\nprint(f\"\\nfraccion apagada por neurona en {n_pasos} pasos:\", np.round(frac_apagada, 3).tolist())\nprint(\"promedio de esas fracciones (debe rondar p=0.5):\", round(float(frac_apagada.mean()), 3))\n",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 5,
    "cols": 8,
    "barMode": false,
    "values": [
     [
      0,
      1,
      0,
      0,
      0,
      0,
      0,
      0
     ],
     [
      0,
      1,
      0,
      1,
      0,
      1,
      0,
      1
     ],
     [
      0,
      1,
      0,
      0,
      1,
      1,
      0,
      1
     ],
     [
      1,
      1,
      0,
      0,
      0,
      1,
      0,
      0
     ],
     [
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1
     ]
    ],
    "rowLabels": [
     "Paso 1",
     "Paso 2",
     "Paso 3",
     "Paso 4",
     "Inferencia"
    ],
    "min": 0,
    "max": 1,
    "aria": "Mapa de que neuronas quedan activas (1) o apagadas (0) en cada uno de los 4 pasos de entrenamiento con dropout p=0.5, y todas activas en la fila de inferencia"
   }
  },
  "application": "Dropout es una de las técnicas de regularización más usadas del deep learning moderno: prácticamente cualquier red densa profunda (clasificadores de imágenes, modelos de diagnóstico médico, sistemas de recomendación) la incluye cuando los datos disponibles son limitados frente al tamaño de la red, el escenario donde el sobreajuste — memorizar en vez de generalizar — es más probable. Hinton la propuso en 2012 pensando en cómo una organización se vuelve más resiliente cuando el conocimiento no depende de una sola persona, y el resultado empírico fue contundente: hasta redes ya en el estado del arte ganaron entre 1 y 2 puntos de accuracy con solo agregar dropout, lo que en un modelo con 95% de precisión significa reducir la tasa de error casi un 40% (de 5% a ~3%). En la práctica, si un modelo sobreajusta se sube la tasa p; si ni siquiera aprende bien el set de entrenamiento (underfitting) se la baja, y suele aplicarse más fuerte en las capas grandes que en las chicas. El costo es que el entrenamiento converge más lento, pero el resultado generaliza mucho mejor a datos nunca vistos (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.11).",
  "codeAnatomy": {
   "title": "h_drop = h * mask / keep",
   "caption": "Cada paso de entrenamiento apaga neuronas al azar y reescala las que quedan (inverted dropout).",
   "lines": [
    "p = 0.5       # dropout rate: probabilidad de apagar cada neurona",
    "keep = 1 - p  # keep probability",
    "    mask = (np.random.rand(len(h)) > p).astype(float)   # 1=activa, 0=apagada",
    "    h_drop = h * mask / keep   # inverted dropout: se escala para compensar"
   ],
   "annotations": [
    {
     "line": 0,
     "text": "p = 0.5",
     "label": "Dropout rate",
     "desc": "(probabilidad de apagar)",
     "side": "top"
    },
    {
     "line": 1,
     "text": "1 - p",
     "label": "Keep probability",
     "side": "top"
    },
    {
     "line": 2,
     "text": "np.random.rand(len(h)) > p",
     "label": "Sorteo aleatorio",
     "desc": "(1=activa, 0=apagada)",
     "side": "bottom"
    },
    {
     "line": 3,
     "text": "h * mask",
     "label": "Apaga neuronas",
     "desc": "(multiplica por 0 o 1)",
     "side": "bottom"
    },
    {
     "line": 3,
     "text": "/ keep",
     "label": "Inverted dropout",
     "desc": "(compensa las apagadas)",
     "side": "bottom"
    }
   ],
   "blockBracket": {
    "from": 2,
    "to": 3,
    "label": "Cada paso de entrenamiento: apaga y reescala"
   }
  }
 },
 {
  "name": "Redes Neuronales · Dropout — pregunta 2",
  "theory": "Imaginá que siempre practicás un examen grupal con el mismo equipo fijo de 8 compañeros: con el tiempo, cada uno se especializa en un tema y el grupo entero depende de que ESE compañero particular esté presente — si falta el que sabe historia, el equipo se hunde en esa pregunta. Ahora imaginá que en cada práctica se sortea al azar la MITAD del equipo (los otros se quedan afuera esa vez nada más): nadie puede depender de un compañero fijo, todos tienen que aprender un poco de todo porque nunca saben quién va a faltar. Eso es exactamente lo que hace <b>Dropout</b> con las neuronas de una red: en cada paso de ENTRENAMIENTO apaga al azar un porcentaje p de las neuronas (las ignora por completo, como si no existieran esa vez), forzando a que ninguna neurona dependa de que otra en particular esté activa.<br><br>En el código, una capa oculta de 8 neuronas (activaciones reales tras un forward pass con ReLU) pasa por 4 pasos de entrenamiento distintos con p=0.5: en el paso 1 se apagan 7 de las 8 neuronas (solo queda activa la neurona de índice 1), en el paso 2 se apagan otras 4 neuronas totalmente distintas, y así sucesivamente — cada paso entrena una red ligeramente diferente. Las salidas que SÍ quedan activas se dividen por keep=1-p=0.5 (el llamado <i>inverted dropout</i>) para compensar que ese paso tiene menos neuronas aportando señal. Al llegar la INFERENCIA (usar la red ya entrenada), Dropout se desactiva por completo: se usan las 8 neuronas con sus activaciones originales, sin apagar ni escalar nada — por eso la salida final es idéntica a la primera línea del código. Repitiendo el sorteo 2000 veces, la fracción real de apagados por neurona promedia 0.504, prácticamente igual al p=0.5 configurado.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.11, sección 'Dropout', p.383-385): en cada paso de entrenamiento, cada neurona (salvo las de salida) tiene una probabilidad $p$ (típicamente 0.5) de ser ignorada por completo para ese paso; tras entrenar, ninguna neurona se apaga más. Para compensar que en entrenamiento hay en promedio menos neuronas activas que en inferencia, cada salida que sobrevive se divide por la keep probability $(1-p)$ — la técnica de <i>inverted dropout</i> que usa Keras internamente en su capa <code>keras.layers.Dropout</code>.",
  "code": "# Dropout (Geron, Cap.11 'Training Deep Neural Networks', seccion 'Dropout',\n# p.383-385): en cada paso de ENTRENAMIENTO, cada neurona tiene una\n# probabilidad p de apagarse por completo para ese paso (Srivastava et al.,\n# 2014). Aqui se ve el mecanismo real sobre una capa oculta de 8 neuronas,\n# sin TensorFlow/Keras (no instalados en este sandbox), con numpy puro.\nimport numpy as np\n\n# activaciones de una capa oculta de 8 neuronas: resultado REAL de un\n# forward pass (entrada -> pesos -> ReLU), no numeros inventados\nnp.random.seed(13)\nx = np.array([0.5, -0.2, 1.1, 0.3])\nW = np.random.normal(0, 0.6, (4, 8))\nb = np.random.normal(0.15, 0.1, 8)\nh = np.maximum(0, x @ W + b)\nprint(\"activaciones de la capa oculta (sin dropout):\", np.round(h, 3).tolist())\n\np = 0.5       # dropout rate: probabilidad de apagar cada neurona\nkeep = 1 - p  # keep probability\n\nprint(f\"\\n4 pasos de ENTRENAMIENTO distintos, dropout p={p}:\")\nnp.random.seed(1)\nfor paso in range(1, 5):\n    mask = (np.random.rand(len(h)) > p).astype(float)   # 1=activa, 0=apagada\n    h_drop = h * mask / keep   # inverted dropout: se escala para compensar\n    apagadas = np.where(mask == 0)[0].tolist()\n    print(f\"paso {paso}: neuronas apagadas={apagadas}  salida={np.round(h_drop, 2).tolist()}\")\n\nprint(\"\\nINFERENCIA (despues de entrenar, dropout desactivado):\")\nprint(\"salida:\", np.round(h, 3).tolist(), \"-- todas las neuronas activas, sin escalar\")\n\n# verificacion estadistica: en miles de pasos, la fraccion real de apagados\n# debe rondar el p configurado (vectorizado, sin bucle Python largo)\nnp.random.seed(3)\nn_pasos = 2000\nmasks_stat = (np.random.rand(n_pasos, len(h)) > p).astype(float)\nfrac_apagada = 1 - masks_stat.mean(axis=0)\nprint(f\"\\nfraccion apagada por neurona en {n_pasos} pasos:\", np.round(frac_apagada, 3).tolist())\nprint(\"promedio de esas fracciones (debe rondar p=0.5):\", round(float(frac_apagada.mean()), 3))\n",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 5,
    "cols": 8,
    "barMode": false,
    "values": [
     [
      0,
      1,
      0,
      0,
      0,
      0,
      0,
      0
     ],
     [
      0,
      1,
      0,
      1,
      0,
      1,
      0,
      1
     ],
     [
      0,
      1,
      0,
      0,
      1,
      1,
      0,
      1
     ],
     [
      1,
      1,
      0,
      0,
      0,
      1,
      0,
      0
     ],
     [
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1
     ]
    ],
    "rowLabels": [
     "Paso 1",
     "Paso 2",
     "Paso 3",
     "Paso 4",
     "Inferencia"
    ],
    "min": 0,
    "max": 1,
    "aria": "Mapa de que neuronas quedan activas (1) o apagadas (0) en cada uno de los 4 pasos de entrenamiento con dropout p=0.5, y todas activas en la fila de inferencia"
   }
  },
  "application": "Dropout es una de las técnicas de regularización más usadas del deep learning moderno: prácticamente cualquier red densa profunda (clasificadores de imágenes, modelos de diagnóstico médico, sistemas de recomendación) la incluye cuando los datos disponibles son limitados frente al tamaño de la red, el escenario donde el sobreajuste — memorizar en vez de generalizar — es más probable. Hinton la propuso en 2012 pensando en cómo una organización se vuelve más resiliente cuando el conocimiento no depende de una sola persona, y el resultado empírico fue contundente: hasta redes ya en el estado del arte ganaron entre 1 y 2 puntos de accuracy con solo agregar dropout, lo que en un modelo con 95% de precisión significa reducir la tasa de error casi un 40% (de 5% a ~3%). En la práctica, si un modelo sobreajusta se sube la tasa p; si ni siquiera aprende bien el set de entrenamiento (underfitting) se la baja, y suele aplicarse más fuerte en las capas grandes que en las chicas. El costo es que el entrenamiento converge más lento, pero el resultado generaliza mucho mejor a datos nunca vistos (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.11)."
 },
 {
  "name": "Redes Neuronales · Dropout — pregunta 3",
  "theory": "Imaginá que siempre practicás un examen grupal con el mismo equipo fijo de 8 compañeros: con el tiempo, cada uno se especializa en un tema y el grupo entero depende de que ESE compañero particular esté presente — si falta el que sabe historia, el equipo se hunde en esa pregunta. Ahora imaginá que en cada práctica se sortea al azar la MITAD del equipo (los otros se quedan afuera esa vez nada más): nadie puede depender de un compañero fijo, todos tienen que aprender un poco de todo porque nunca saben quién va a faltar. Eso es exactamente lo que hace <b>Dropout</b> con las neuronas de una red: en cada paso de ENTRENAMIENTO apaga al azar un porcentaje p de las neuronas (las ignora por completo, como si no existieran esa vez), forzando a que ninguna neurona dependa de que otra en particular esté activa.<br><br>En el código, una capa oculta de 8 neuronas (activaciones reales tras un forward pass con ReLU) pasa por 4 pasos de entrenamiento distintos con p=0.5: en el paso 1 se apagan 7 de las 8 neuronas (solo queda activa la neurona de índice 1), en el paso 2 se apagan otras 4 neuronas totalmente distintas, y así sucesivamente — cada paso entrena una red ligeramente diferente. Las salidas que SÍ quedan activas se dividen por keep=1-p=0.5 (el llamado <i>inverted dropout</i>) para compensar que ese paso tiene menos neuronas aportando señal. Al llegar la INFERENCIA (usar la red ya entrenada), Dropout se desactiva por completo: se usan las 8 neuronas con sus activaciones originales, sin apagar ni escalar nada — por eso la salida final es idéntica a la primera línea del código. Repitiendo el sorteo 2000 veces, la fracción real de apagados por neurona promedia 0.504, prácticamente igual al p=0.5 configurado.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.11, sección 'Dropout', p.383-385): en cada paso de entrenamiento, cada neurona (salvo las de salida) tiene una probabilidad $p$ (típicamente 0.5) de ser ignorada por completo para ese paso; tras entrenar, ninguna neurona se apaga más. Para compensar que en entrenamiento hay en promedio menos neuronas activas que en inferencia, cada salida que sobrevive se divide por la keep probability $(1-p)$ — la técnica de <i>inverted dropout</i> que usa Keras internamente en su capa <code>keras.layers.Dropout</code>.",
  "code": "# Dropout (Geron, Cap.11 'Training Deep Neural Networks', seccion 'Dropout',\n# p.383-385): en cada paso de ENTRENAMIENTO, cada neurona tiene una\n# probabilidad p de apagarse por completo para ese paso (Srivastava et al.,\n# 2014). Aqui se ve el mecanismo real sobre una capa oculta de 8 neuronas,\n# sin TensorFlow/Keras (no instalados en este sandbox), con numpy puro.\nimport numpy as np\n\n# activaciones de una capa oculta de 8 neuronas: resultado REAL de un\n# forward pass (entrada -> pesos -> ReLU), no numeros inventados\nnp.random.seed(13)\nx = np.array([0.5, -0.2, 1.1, 0.3])\nW = np.random.normal(0, 0.6, (4, 8))\nb = np.random.normal(0.15, 0.1, 8)\nh = np.maximum(0, x @ W + b)\nprint(\"activaciones de la capa oculta (sin dropout):\", np.round(h, 3).tolist())\n\np = 0.5       # dropout rate: probabilidad de apagar cada neurona\nkeep = 1 - p  # keep probability\n\nprint(f\"\\n4 pasos de ENTRENAMIENTO distintos, dropout p={p}:\")\nnp.random.seed(1)\nfor paso in range(1, 5):\n    mask = (np.random.rand(len(h)) > p).astype(float)   # 1=activa, 0=apagada\n    h_drop = h * mask / keep   # inverted dropout: se escala para compensar\n    apagadas = np.where(mask == 0)[0].tolist()\n    print(f\"paso {paso}: neuronas apagadas={apagadas}  salida={np.round(h_drop, 2).tolist()}\")\n\nprint(\"\\nINFERENCIA (despues de entrenar, dropout desactivado):\")\nprint(\"salida:\", np.round(h, 3).tolist(), \"-- todas las neuronas activas, sin escalar\")\n\n# verificacion estadistica: en miles de pasos, la fraccion real de apagados\n# debe rondar el p configurado (vectorizado, sin bucle Python largo)\nnp.random.seed(3)\nn_pasos = 2000\nmasks_stat = (np.random.rand(n_pasos, len(h)) > p).astype(float)\nfrac_apagada = 1 - masks_stat.mean(axis=0)\nprint(f\"\\nfraccion apagada por neurona en {n_pasos} pasos:\", np.round(frac_apagada, 3).tolist())\nprint(\"promedio de esas fracciones (debe rondar p=0.5):\", round(float(frac_apagada.mean()), 3))\n",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 5,
    "cols": 8,
    "barMode": false,
    "values": [
     [
      0,
      1,
      0,
      0,
      0,
      0,
      0,
      0
     ],
     [
      0,
      1,
      0,
      1,
      0,
      1,
      0,
      1
     ],
     [
      0,
      1,
      0,
      0,
      1,
      1,
      0,
      1
     ],
     [
      1,
      1,
      0,
      0,
      0,
      1,
      0,
      0
     ],
     [
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1
     ]
    ],
    "rowLabels": [
     "Paso 1",
     "Paso 2",
     "Paso 3",
     "Paso 4",
     "Inferencia"
    ],
    "min": 0,
    "max": 1,
    "aria": "Mapa de que neuronas quedan activas (1) o apagadas (0) en cada uno de los 4 pasos de entrenamiento con dropout p=0.5, y todas activas en la fila de inferencia"
   }
  },
  "application": "Dropout es una de las técnicas de regularización más usadas del deep learning moderno: prácticamente cualquier red densa profunda (clasificadores de imágenes, modelos de diagnóstico médico, sistemas de recomendación) la incluye cuando los datos disponibles son limitados frente al tamaño de la red, el escenario donde el sobreajuste — memorizar en vez de generalizar — es más probable. Hinton la propuso en 2012 pensando en cómo una organización se vuelve más resiliente cuando el conocimiento no depende de una sola persona, y el resultado empírico fue contundente: hasta redes ya en el estado del arte ganaron entre 1 y 2 puntos de accuracy con solo agregar dropout, lo que en un modelo con 95% de precisión significa reducir la tasa de error casi un 40% (de 5% a ~3%). En la práctica, si un modelo sobreajusta se sube la tasa p; si ni siquiera aprende bien el set de entrenamiento (underfitting) se la baja, y suele aplicarse más fuerte en las capas grandes que en las chicas. El costo es que el entrenamiento converge más lento, pero el resultado generaliza mucho mejor a datos nunca vistos (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.11)."
 },
 {
  "name": "Redes Neuronales · Dropout — pregunta 4",
  "theory": "Imaginá que siempre practicás un examen grupal con el mismo equipo fijo de 8 compañeros: con el tiempo, cada uno se especializa en un tema y el grupo entero depende de que ESE compañero particular esté presente — si falta el que sabe historia, el equipo se hunde en esa pregunta. Ahora imaginá que en cada práctica se sortea al azar la MITAD del equipo (los otros se quedan afuera esa vez nada más): nadie puede depender de un compañero fijo, todos tienen que aprender un poco de todo porque nunca saben quién va a faltar. Eso es exactamente lo que hace <b>Dropout</b> con las neuronas de una red: en cada paso de ENTRENAMIENTO apaga al azar un porcentaje p de las neuronas (las ignora por completo, como si no existieran esa vez), forzando a que ninguna neurona dependa de que otra en particular esté activa.<br><br>En el código, una capa oculta de 8 neuronas (activaciones reales tras un forward pass con ReLU) pasa por 4 pasos de entrenamiento distintos con p=0.5: en el paso 1 se apagan 7 de las 8 neuronas (solo queda activa la neurona de índice 1), en el paso 2 se apagan otras 4 neuronas totalmente distintas, y así sucesivamente — cada paso entrena una red ligeramente diferente. Las salidas que SÍ quedan activas se dividen por keep=1-p=0.5 (el llamado <i>inverted dropout</i>) para compensar que ese paso tiene menos neuronas aportando señal. Al llegar la INFERENCIA (usar la red ya entrenada), Dropout se desactiva por completo: se usan las 8 neuronas con sus activaciones originales, sin apagar ni escalar nada — por eso la salida final es idéntica a la primera línea del código. Repitiendo el sorteo 2000 veces, la fracción real de apagados por neurona promedia 0.504, prácticamente igual al p=0.5 configurado.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.11, sección 'Dropout', p.383-385): en cada paso de entrenamiento, cada neurona (salvo las de salida) tiene una probabilidad $p$ (típicamente 0.5) de ser ignorada por completo para ese paso; tras entrenar, ninguna neurona se apaga más. Para compensar que en entrenamiento hay en promedio menos neuronas activas que en inferencia, cada salida que sobrevive se divide por la keep probability $(1-p)$ — la técnica de <i>inverted dropout</i> que usa Keras internamente en su capa <code>keras.layers.Dropout</code>.",
  "code": "# Dropout (Geron, Cap.11 'Training Deep Neural Networks', seccion 'Dropout',\n# p.383-385): en cada paso de ENTRENAMIENTO, cada neurona tiene una\n# probabilidad p de apagarse por completo para ese paso (Srivastava et al.,\n# 2014). Aqui se ve el mecanismo real sobre una capa oculta de 8 neuronas,\n# sin TensorFlow/Keras (no instalados en este sandbox), con numpy puro.\nimport numpy as np\n\n# activaciones de una capa oculta de 8 neuronas: resultado REAL de un\n# forward pass (entrada -> pesos -> ReLU), no numeros inventados\nnp.random.seed(13)\nx = np.array([0.5, -0.2, 1.1, 0.3])\nW = np.random.normal(0, 0.6, (4, 8))\nb = np.random.normal(0.15, 0.1, 8)\nh = np.maximum(0, x @ W + b)\nprint(\"activaciones de la capa oculta (sin dropout):\", np.round(h, 3).tolist())\n\np = 0.5       # dropout rate: probabilidad de apagar cada neurona\nkeep = 1 - p  # keep probability\n\nprint(f\"\\n4 pasos de ENTRENAMIENTO distintos, dropout p={p}:\")\nnp.random.seed(1)\nfor paso in range(1, 5):\n    mask = (np.random.rand(len(h)) > p).astype(float)   # 1=activa, 0=apagada\n    h_drop = h * mask / keep   # inverted dropout: se escala para compensar\n    apagadas = np.where(mask == 0)[0].tolist()\n    print(f\"paso {paso}: neuronas apagadas={apagadas}  salida={np.round(h_drop, 2).tolist()}\")\n\nprint(\"\\nINFERENCIA (despues de entrenar, dropout desactivado):\")\nprint(\"salida:\", np.round(h, 3).tolist(), \"-- todas las neuronas activas, sin escalar\")\n\n# verificacion estadistica: en miles de pasos, la fraccion real de apagados\n# debe rondar el p configurado (vectorizado, sin bucle Python largo)\nnp.random.seed(3)\nn_pasos = 2000\nmasks_stat = (np.random.rand(n_pasos, len(h)) > p).astype(float)\nfrac_apagada = 1 - masks_stat.mean(axis=0)\nprint(f\"\\nfraccion apagada por neurona en {n_pasos} pasos:\", np.round(frac_apagada, 3).tolist())\nprint(\"promedio de esas fracciones (debe rondar p=0.5):\", round(float(frac_apagada.mean()), 3))\n",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 5,
    "cols": 8,
    "barMode": false,
    "values": [
     [
      0,
      1,
      0,
      0,
      0,
      0,
      0,
      0
     ],
     [
      0,
      1,
      0,
      1,
      0,
      1,
      0,
      1
     ],
     [
      0,
      1,
      0,
      0,
      1,
      1,
      0,
      1
     ],
     [
      1,
      1,
      0,
      0,
      0,
      1,
      0,
      0
     ],
     [
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1
     ]
    ],
    "rowLabels": [
     "Paso 1",
     "Paso 2",
     "Paso 3",
     "Paso 4",
     "Inferencia"
    ],
    "min": 0,
    "max": 1,
    "aria": "Mapa de que neuronas quedan activas (1) o apagadas (0) en cada uno de los 4 pasos de entrenamiento con dropout p=0.5, y todas activas en la fila de inferencia"
   }
  },
  "application": "Dropout es una de las técnicas de regularización más usadas del deep learning moderno: prácticamente cualquier red densa profunda (clasificadores de imágenes, modelos de diagnóstico médico, sistemas de recomendación) la incluye cuando los datos disponibles son limitados frente al tamaño de la red, el escenario donde el sobreajuste — memorizar en vez de generalizar — es más probable. Hinton la propuso en 2012 pensando en cómo una organización se vuelve más resiliente cuando el conocimiento no depende de una sola persona, y el resultado empírico fue contundente: hasta redes ya en el estado del arte ganaron entre 1 y 2 puntos de accuracy con solo agregar dropout, lo que en un modelo con 95% de precisión significa reducir la tasa de error casi un 40% (de 5% a ~3%). En la práctica, si un modelo sobreajusta se sube la tasa p; si ni siquiera aprende bien el set de entrenamiento (underfitting) se la baja, y suele aplicarse más fuerte en las capas grandes que en las chicas. El costo es que el entrenamiento converge más lento, pero el resultado generaliza mucho mejor a datos nunca vistos (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.11)."
 }
];

/* ──────────── Preguntas de práctica del Modo Maestro RN (superaprendizaje) ────
   Array PARALELO a EX_RN por índice, mismo mecanismo de practice-testing +
   feedback inmediato que AO/Matemáticas/RA/AS -- cada pregunta se fundamenta
   en el propio código/fórmula de ESE tema, verificado ejecutando realmente
   el código antes de fijar la respuesta correcta. */
const RN_QUIZ = [
 [
  {
   "question": "En la primera época, el perceptrón comete 3 errores de 4. ¿Qué hace el código con cada error, exactamente?",
   "type": "mc",
   "options": [
    "Ajusta los pesos w y el sesgo b en la dirección que reduce ese error específico: w = w + lr·error·xi",
    "Ignora el error y sigue con el siguiente ejemplo sin cambiar nada",
    "Reinicia todos los pesos a cero cada vez que hay un error",
    "Elimina ese ejemplo del conjunto de entrenamiento"
   ],
   "correct": 0,
   "solution": "La línea w = w + lr*error*xi es la regla de aprendizaje del perceptrón: cada vez que la predicción no coincide con la esperada, ajusta los pesos proporcionalmente al error y a la entrada — por eso, después de solo 2 épocas, ya no comete ningún error más.",
   "whyNot": [
    null,
    "Si ignorara los errores, los pesos nunca cambiarían y el perceptrón seguiría fallando en todas las épocas — pero el código muestra que los errores bajan de 3 a 0, prueba de que sí se ajustan los pesos.",
    "Los pesos se ajustan gradualmente (sumando una corrección pequeña), no se reinician a cero — reiniciar borraría todo lo aprendido hasta ese momento.",
    "El perceptrón sigue usando los 4 ejemplos de AND en cada época, siempre — ningún ejemplo se descarta por generar un error, todo lo contrario: los errores son la señal que usa para aprender."
   ],
   "steps": [
    "Fijate qué línea del código se ejecuta SOLO cuando hay un error: w = w + lr*error*xi.",
    "Esa fórmula ajusta cada peso EN PROPORCIÓN al error cometido y a la entrada correspondiente xi — no lo reinicia, no lo ignora, no borra el ejemplo.",
    "Repetido sobre los 4 ejemplos de AND, época tras época, esos ajustes van corrigiendo los pesos hasta que dejan de fallar.",
    "Por eso, tras solo 2 épocas, el conteo de errores llega a 0."
   ],
   "stakes": "Entender que el ajuste depende PROPORCIONALMENTE del error es la base para diagnosticar por qué un modelo real no converge — si los pesos se disparan o nunca cambian, el problema casi siempre está en esta misma lógica, aplicada con un lr mal elegido."
  },
  {
   "question": "En la línea w = w + lr * error * xi, ¿qué controla exactamente la variable lr (0.1 en este código)?",
   "type": "mc",
   "options": [
    "El tamaño del ajuste que se aplica a los pesos cada vez que hay un error — no si hay error, sino cuánto se corrige",
    "La cantidad de épocas que va a entrenar el perceptrón",
    "El valor inicial de los pesos w antes de empezar a entrenar",
    "La cantidad de errores que el perceptrón puede cometer antes de detenerse"
   ],
   "correct": 0,
   "solution": "lr multiplica el producto error*xi antes de sumarlo a w — es la tasa de aprendizaje: un número fijo (0.1) que escala cuánto se mueve cada peso en cada corrección, sin afectar SI hay corrección (eso lo decide 'error != 0') ni cuántas veces se repite el entrenamiento.",
   "whyNot": [
    null,
    "La cantidad de épocas está fijada aparte, por 'range(15)' en el bucle for — lr no tiene ninguna relación con cuántas veces se repite el entrenamiento.",
    "Los pesos iniciales los genera 'np.random.normal(0, 0.1, 2)', antes de que lr entre en juego en ningún cálculo — son dos cosas distintas: unos son los pesos de partida, y lr es cuánto se ajustan después.",
    "El perceptrón no se detiene por una cantidad de errores permitidos — entrena las 15 épocas completas sin importar cuántos errores cometa en cada una; lr no tiene ese rol."
   ],
   "steps": [
    "Ubicá dónde aparece lr en el código: solo en 'w = w + lr * error * xi' y 'b = b + lr * error', ambas DENTRO del if que ya decidió que hubo un error.",
    "Eso significa que lr no decide SI se corrige (eso ya lo decidió 'error != 0'), sino CUÁNTO se corrige cada vez.",
    "Un lr más grande daría correcciones más bruscas; uno más chico, correcciones más suaves — pero la lógica de cuándo corregir no cambia."
   ],
   "stakes": "Elegir mal la tasa de aprendizaje es una de las causas más comunes de que un modelo real no converja — muy alta y los pesos oscilan sin asentarse, muy baja y el entrenamiento tarda muchísimas más épocas de las necesarias."
  },
  {
   "question": "El código genera w con 'np.random.normal(0, 0.1, 2)' — exactamente 2 valores. ¿Por qué 2, y no otro número?",
   "type": "mc",
   "options": [
    "Porque X tiene 2 columnas (2 entradas por ejemplo) — el perceptrón necesita exactamente un peso por cada entrada",
    "Porque hay 2 clases posibles en la salida (0 y 1)",
    "Porque el bucle de entrenamiento usa 'range(15)', y 15/2 se aproxima a un valor entero",
    "Es un valor arbitrario, elegido sin relación con los datos de entrada"
   ],
   "correct": 0,
   "solution": "Cada componente de w multiplica a UNA columna de X (una entrada) en la suma ponderada z = w·x + b — con 2 entradas (X tiene 2 columnas), hacen falta exactamente 2 pesos, ni uno más ni uno menos. El tamaño de w no es arbitrario: está determinado por la dimensión de los datos de entrada.",
   "whyNot": [
    null,
    "La cantidad de clases de salida (0 o 1) no determina el tamaño de w — un perceptrón siempre produce UNA sola salida (escalar), sin importar cuántos pesos tenga de entrada.",
    "El número de épocas (15) es un hiperparámetro de entrenamiento completamente independiente del tamaño de w — no hay ninguna relación matemática entre ambos.",
    "El tamaño de w está determinado exactamente por la forma de los datos (X tiene 2 columnas) — no es una elección libre, sino una consecuencia directa de np.dot(w, xi), que exige que w y xi tengan la misma longitud."
   ],
   "steps": [
    "Mirá la operación z = np.dot(w, xi) + b — el producto punto exige que w y xi tengan la MISMA cantidad de elementos.",
    "xi es una fila de X, que tiene 2 columnas (2 entradas de la compuerta lógica).",
    "Por eso w debe tener también 2 componentes — uno por cada entrada, ni más ni menos."
   ],
   "stakes": "Entender que el tamaño del vector de pesos lo determina la DIMENSIÓN de los datos de entrada (no un número elegido a mano) es lo primero que hay que revisar cuando un modelo real lanza un error de dimensiones incompatibles."
  }
 ],
 [
  {
   "question": "Después de la 3ª época, 'errores_por_epoca' queda en 0 para siempre. ¿Qué significa esto sobre los pesos w y el sesgo b?",
   "type": "mc",
   "options": [
    "Encontraron una combinación que clasifica correctamente los 4 ejemplos de AND, y dejaron de necesitar ajustes",
    "Los pesos se volvieron todos exactamente 0",
    "El código dejó de ejecutarse después de la 3ª época",
    "El perceptrón empezó a memorizar los ejemplos en vez de aprender un patrón"
   ],
   "correct": 0,
   "solution": "Una vez que w y b clasifican correctamente los 4 casos de AND, ya no hay ningún 'error' que dispare un ajuste (la condición 'if error != 0' nunca se cumple) — por eso el conteo de errores se queda en 0 el resto de las épocas: el perceptrón ya convergió.",
   "whyNot": [
    null,
    "Los pesos finales impresos son [0.176, 0.04], no ceros — un perceptrón con pesos todos en 0 no podría distinguir ninguna entrada de otra.",
    "El código sigue corriendo las 15 épocas completas (el bucle 'for epoca in range(15)' no se corta antes) — solo que, tras converger, ya no hay más ajustes que hacer.",
    "AND es linealmente separable, así que existe una única frontera recta correcta que el perceptrón encuentra — no hay 'memorización' de casos individuales, hay una regla lineal real que generaliza a los 4 casos."
   ],
   "steps": [
    "El ajuste de pesos solo ocurre DENTRO del if que chequea 'error != 0' — si no hay error, esa línea nunca se ejecuta.",
    "Que el conteo se quede en 0 desde la 3ª época significa que, para los 4 ejemplos de AND, la predicción ya coincide siempre con la esperada.",
    "Eso es exactamente la definición de que el perceptrón ya CONVERGIÓ: encontró una w y b que clasifican bien todos los casos."
   ],
   "stakes": "Ver 'error=0' de forma sostenida en un log de entrenamiento real es la señal que confirma que un modelo simple ya aprendió el patrón — seguir entrenando después de eso es tiempo de cómputo desperdiciado."
  },
  {
   "question": "El código imprime por separado 'predicciones finales' y 'esperado (AND)'. Según esas dos líneas impresas, ¿qué relación hay entre ellas al final del entrenamiento?",
   "type": "mc",
   "options": [
    "Son exactamente iguales: [0,0,0,1] en ambos casos — el perceptrón entrenado predice AND perfectamente sobre los 4 ejemplos",
    "Son distintas en el primer caso ([0,0]) pero iguales en los otros tres",
    "'predicciones finales' tiene 4 valores, pero 'esperado (AND)' solo tiene 3",
    "No se pueden comparar porque están en formatos numéricos distintos"
   ],
   "correct": 0,
   "solution": "'preds' se calcula aplicando escalon() a los pesos ya entrenados sobre los 4 casos de X, y da [0,0,0,1] — exactamente igual a 'y.tolist()' ([0,0,0,1], la definición de AND). Que ambas líneas impresas coincidan dígito por dígito es la prueba directa, en la salida del programa, de que el perceptrón aprendió la función correctamente.",
   "whyNot": [
    null,
    "Las 4 predicciones coinciden con las 4 esperadas, incluyendo el primer caso [0,0]→0 — no hay ningún desacuerdo parcial entre ambas líneas.",
    "Ambos arrays tienen 4 elementos: 'preds' se calcula con una comprensión de lista sobre los 4 casos de X, e 'y.tolist()' convierte el array y (también de 4 elementos) a lista.",
    "Ambos son listas de enteros (0 y 1) — 'preds' viene de aplicar escalon() (que devuelve 0 o 1) y 'y.tolist()' convierte el array numpy y a una lista de Python con los mismos tipos de valores; se pueden comparar directamente posición por posición."
   ],
   "steps": [
    "Mirá las dos últimas líneas impresas: 'predicciones finales' y 'esperado (AND)', ambas listas de 4 valores.",
    "Comparalas posición por posición: en las 4 posiciones, el valor impreso es el mismo.",
    "Que coincidan exactamente es la evidencia final de que el entrenamiento funcionó: los pesos y sesgo aprendidos reproducen AND sin ningún error."
   ],
   "stakes": "Comparar la predicción final del modelo contra el resultado esperado, ejemplo por ejemplo, es exactamente el tipo de verificación manual que se hace antes de confiar en cualquier modelo simple entrenado desde cero."
  },
  {
   "question": "A diferencia de w (2 componentes, uno por entrada), el sesgo b es UN ÚNICO número. ¿Por qué b no necesita tener 2 componentes como w?",
   "type": "mc",
   "options": [
    "Porque b se suma una sola vez al final (z = w·x + b), sin multiplicar a ninguna entrada — desplaza la decisión en su conjunto, no entrada por entrada",
    "Porque b representa el número de épocas de entrenamiento",
    "Porque b se calcula como el promedio de los 2 componentes de w",
    "Es un error del código: debería tener 2 componentes igual que w"
   ],
   "correct": 0,
   "solution": "En z = np.dot(w, xi) + b, b se SUMA una única vez al resultado del producto punto — no se multiplica por ninguna entrada individual, así que no necesita 'un valor por entrada' como w. Su rol es desplazar el umbral de decisión completo (por ejemplo, permitir que la neurona se active incluso con z=0 exacto), no ponderar entradas.",
   "whyNot": [
    null,
    "Las épocas de entrenamiento están controladas por 'range(15)' en el bucle for, sin ninguna relación con b — son dos variables completamente independientes.",
    "b se inicializa en 0.0 y se ajusta con 'b = b + lr * error', igual que w pero por separado — no es un promedio ni una función de los componentes de w.",
    "No es un error: b es matemáticamente un escalar por definición en esta fórmula (un desplazamiento único), a diferencia de w que sí necesita un componente por cada entrada."
   ],
   "steps": [
    "Mirá la fórmula z = np.dot(w, xi) + b — w se combina componente a componente con xi (producto punto), pero b se suma DESPUÉS, una sola vez.",
    "Eso significa que b no pondera ninguna entrada en particular: solo desplaza el resultado final hacia arriba o hacia abajo.",
    "Por eso b es un único número (un escalar), mientras que w necesita un componente por cada entrada."
   ],
   "stakes": "Distinguir 'pesos' (uno por entrada, w) de 'sesgo' (un desplazamiento global, b) es la base para leer la arquitectura de cualquier red, donde cada capa tiene su propia matriz de pesos y su propio vector de sesgos con roles distintos."
  }
 ],
 [
  {
   "question": "¿Qué representa la función escalón() en el código de la neurona artificial?",
   "type": "mc",
   "options": [
    "La función de activación: convierte la suma ponderada z en una salida binaria (0 o 1)",
    "La tasa de aprendizaje que controla cuánto se ajustan los pesos",
    "El conteo de errores acumulados durante el entrenamiento",
    "La cantidad de entradas que recibe la neurona"
   ],
   "correct": 0,
   "solution": "escalon(z) devuelve 1 si z≥0 y 0 si no — es la función de activación más simple posible, la que usó el perceptrón original de Rosenblatt. Transforma el número continuo z=w·x+b en una decisión binaria final.",
   "whyNot": [
    null,
    "La tasa de aprendizaje es la variable lr=0.1 en el código, un número fijo que multiplica el ajuste — no tiene relación con la función escalón, que solo transforma z en 0 o 1.",
    "El conteo de errores es la variable 'errores' dentro del bucle de cada época — un contador entero, no una función de activación.",
    "La cantidad de entradas está dada por el tamaño del vector w (2, en este caso, para las 2 columnas de X) — escalón() no cuenta nada, solo decide la salida a partir de z."
   ],
   "steps": [
    "Buscá qué hace escalon(z): compara z con 0 y devuelve 1 o 0 — no toca pesos, no cuenta errores, no cuenta entradas.",
    "Esa transformación de un número continuo (z=w·x+b) a una salida binaria es justamente la definición de función de activación.",
    "Por eso escalón() es la función de activación, la última pieza que decide la salida final de la neurona."
   ],
   "stakes": "Elegir mal la función de activación en un proyecto real (por ejemplo, usar un escalón en vez de sigmoid en una red moderna) rompe el entrenamiento por gradiente porque un escalón no tiene derivada útil — la razón histórica por la que se dejó de usar en redes profundas."
  },
  {
   "question": "Según la definición 'def escalon(z): return 1 if z >= 0 else 0', si en algún punto del entrenamiento z diera EXACTAMENTE 0, ¿qué predicción devolvería la neurona?",
   "type": "mc",
   "options": [
    "1, porque la condición es z >= 0 (mayor O IGUAL a cero), y 0 cumple esa condición",
    "0, porque z=0 no es un valor positivo",
    "La neurona lanzaría un error, porque z=0 es un caso no definido",
    "Depende del valor de b, no del valor de z"
   ],
   "correct": 0,
   "solution": "La condición del código es 'z >= 0', con el signo de IGUAL incluido — así que z=0 cae exactamente en el caso que devuelve 1, no en el que devuelve 0. Es un detalle de implementación que decide en qué lado cae el límite exacto de decisión.",
   "whyNot": [
    null,
    "El código no distingue 'positivo' de 'cero' — la condición '>= 0' agrupa a ambos en el mismo resultado (1); solo z estrictamente negativo cae en el otro caso (0).",
    "La función está definida para cualquier número real, incluyendo z=0 — no hay ningún caso sin definir, el 'if/else' cubre absolutamente todos los valores posibles de z.",
    "z ya es el resultado de np.dot(w, xi) + b — o sea que b YA está incluido dentro del valor de z antes de llegar a escalon(); una vez calculado z, escalon() decide en base a ese único número, sin volver a mirar b por separado."
   ],
   "steps": [
    "Leé la condición exacta del código: 'z >= 0', no 'z > 0'.",
    "El símbolo '>=' incluye la igualdad: z=0 SÍ cumple esa condición.",
    "Por lo tanto, escalon(0) devuelve 1, no 0 — ese detalle define en qué lado cae el límite de decisión exacto de la neurona."
   ],
   "stakes": "Estos detalles de 'bordes' (>= vs >) parecen triviales pero son una fuente real de bugs sutiles al portar código matemático a distintos lenguajes o librerías, donde una convención distinta en el límite puede cambiar resultados en casos límite."
  },
  {
   "question": "El código llama a 'np.random.seed(0)' justo antes de generar los pesos iniciales w. ¿Qué garantiza exactamente esa línea?",
   "type": "mc",
   "options": [
    "Que los pesos iniciales generados 'al azar' sean SIEMPRE los mismos números cada vez que se corre el código, permitiendo reproducir el mismo resultado",
    "Que el perceptrón siempre converja en exactamente 3 épocas",
    "Que los pesos iniciales sean todos exactamente 0",
    "Que la compuerta AND se calcule correctamente"
   ],
   "correct": 0,
   "solution": "Fijar una semilla (seed) hace que el generador de números 'aleatorios' de numpy produzca SIEMPRE la misma secuencia — no elimina la aleatoriedad de los pesos iniciales, pero la hace reproducible: correr el código dos veces da exactamente los mismos pesos iniciales, y por lo tanto el mismo resultado final.",
   "whyNot": [
    null,
    "Cuántas épocas tarda en converger depende de los datos y de dónde arrancan los pesos, no de que la semilla esté fijada — fijar la semilla solo asegura que ese punto de partida sea siempre el MISMO, no que la convergencia sea rápida.",
    "'np.random.normal(0, 0.1, 2)' genera valores aleatorios centrados en 0 pero con dispersión 0.1 — no son ceros exactos, son números pequeños y distintos entre sí, solo que siempre los MISMOS gracias a la semilla fija.",
    "La semilla no tiene ninguna relación con la lógica de AND — solo controla la reproducibilidad de los números aleatorios; el aprendizaje correcto de AND depende de la regla de actualización de pesos, no de la semilla."
   ],
   "steps": [
    "np.random.seed(0) fija el punto de partida del generador de números pseudoaleatorios de numpy.",
    "Con la semilla fija, 'np.random.normal(...)' produce SIEMPRE la misma secuencia de números, en cualquier computadora, cualquier vez que se ejecute.",
    "Eso hace que todo el experimento sea reproducible: los mismos pesos iniciales, el mismo camino de entrenamiento, el mismo resultado final."
   ],
   "stakes": "Fijar semillas es una práctica estándar en cualquier experimento real de machine learning — sin ella, sería imposible reproducir un resultado reportado o comparar de forma justa dos configuraciones distintas del mismo modelo."
  }
 ],
 [
  {
   "question": "Si en vez de AND (linealmente separable) intentaras entrenar este MISMO perceptrón simple (una sola neurona, sin capa oculta) sobre XOR, ¿qué esperarías que pasara con 'errores_por_epoca'?",
   "type": "mc",
   "options": [
    "Nunca llegaría a 0 — el perceptrón simple no puede separar XOR con una sola línea recta, sin importar cuántas épocas entrene",
    "Llegaría a 0 exactamente en la misma época que con AND",
    "El código directamente no se podría ejecutar con datos de XOR",
    "Los errores aumentarían progresivamente hasta el 100% en cada época"
   ],
   "correct": 0,
   "solution": "XOR no es linealmente separable (visto en el siguiente tema) — un perceptrón de una sola capa, que solo puede trazar una frontera recta, jamás logrará clasificar correctamente los 4 casos de XOR a la vez, sin importar cuántas épocas se entrene.",
   "whyNot": [
    null,
    "AND sí es linealmente separable, por eso converge rápido (época 3); XOR no lo es, así que ni siquiera con muchas más épocas un perceptrón simple llegaría a 0 errores — son problemas de dificultad estructuralmente distinta.",
    "El código se ejecutaría sin ningún problema técnico con datos de XOR (mismo formato, 4 filas de 2 columnas) — el fallo no sería un error de programación, sería una limitación matemática del modelo.",
    "Los errores no crecerían indefinidamente — se estabilizarían en un número bajo pero distinto de cero (el perceptrón encontraría la mejor recta posible, que igual clasifica mal algunos de los 4 puntos de XOR)."
   ],
   "steps": [
    "El perceptrón simple solo puede trazar UNA frontera recta entre las clases — no tiene capa oculta que le permita curvar esa frontera.",
    "XOR no es linealmente separable: no existe ninguna recta que separe bien sus 4 casos (visto en el siguiente tema).",
    "Sin importar cuántas épocas entrene, ningún ajuste de w y b puede encontrar una recta que no existe.",
    "Por eso 'errores_por_epoca' nunca llegaría a 0 con XOR, a diferencia de AND."
   ],
   "stakes": "Un equipo que intenta resolver un problema no-lineal real (casi cualquier problema interesante) con un solo perceptrón puede pasar días ajustando hiperparámetros sin darse cuenta de que el modelo elegido NUNCA podría resolverlo, entrene lo que entrene."
  },
  {
   "question": "El comentario del código dice: '# Compuerta AND: linealmente separable, un perceptron SIMPLE puede aprenderla'. ¿Qué relación establece ese comentario entre la separabilidad lineal y la capacidad del perceptrón simple?",
   "type": "mc",
   "options": [
    "Que un perceptrón simple (sin capa oculta) puede aprender un problema precisamente CUANDO ese problema es linealmente separable, como es el caso de AND",
    "Que la separabilidad lineal es una propiedad de los pesos w, no de los datos X e y",
    "Que 'linealmente separable' significa que los datos deben normalizarse antes de entrenar",
    "Que cualquier compuerta lógica, sin excepción, es linealmente separable"
   ],
   "correct": 0,
   "solution": "El comentario conecta directamente dos cosas: la naturaleza de los DATOS (AND es linealmente separable) con la capacidad del MODELO (un perceptrón simple puede aprenderla). Es la razón concreta por la que este código, sin ninguna capa oculta, logra resolver AND perfectamente.",
   "whyNot": [
    null,
    "La separabilidad lineal es una propiedad de cómo se distribuyen los PUNTOS de datos (X e y) en el espacio — no depende de qué valores tengan los pesos w, que son lo que el perceptrón AJUSTA para encontrar esa separación, no lo que la define.",
    "El comentario no habla de normalización de datos en absoluto — 'linealmente separable' es un concepto geométrico sobre si existe una línea recta que separe las clases, no un paso de preprocesamiento.",
    "El propio comentario aclara implícitamente que esto es especial de AND, no una regla universal — el tema siguiente muestra justamente el caso opuesto (XOR), que NO es linealmente separable."
   ],
   "steps": [
    "Leé el comentario tal cual está escrito: describe una PROPIEDAD de la compuerta AND (linealmente separable) y una CONSECUENCIA sobre el modelo (un perceptrón simple puede aprenderla).",
    "Esa relación es la clave de todo el tema: el tipo de problema (sus datos) determina si un modelo tan simple alcanza o no.",
    "Por eso el código, usando solo una neurona sin capa oculta, logra clasificar AND perfectamente — porque el problema en sí lo permite."
   ],
   "stakes": "Reconocer de antemano si un problema real es linealmente separable (por ejemplo, mirando un scatter plot de las clases) ahorra tiempo: evita intentar resolverlo con un modelo lineal simple cuando la geometría del problema ya lo hace imposible."
  },
  {
   "question": "Si en vez de AND o XOR entrenaras este MISMO perceptrón simple sobre la compuerta OR ((0,0)→0, (0,1)→1, (1,0)→1, (1,1)→1), ¿qué esperarías que pasara?",
   "type": "mc",
   "options": [
    "Convergería a 0 errores, igual que con AND — OR también es linealmente separable (una recta puede dejar (0,0) de un lado y los otros 3 puntos del otro)",
    "Fallaría igual que con XOR, porque cualquier compuerta con 3 salidas en 1 es automáticamente no separable",
    "El código no podría ejecutarse porque OR tiene una salida distinta a AND",
    "Tardaría exactamente el triple de épocas que AND en converger"
   ],
   "correct": 0,
   "solution": "OR, igual que AND, ES linealmente separable: existe una recta que deja (0,0) de un lado y los otros 3 puntos ((0,1),(1,0),(1,1)) del otro. Como el perceptrón simple SÍ puede aprender cualquier problema linealmente separable, convergería a 0 errores con OR tal como lo hace con AND — el criterio que importa es la separabilidad geométrica de los datos, no qué compuerta lógica específica sea.",
   "whyNot": [
    null,
    "Que 3 de los 4 casos den 1 no hace que un problema sea no-separable — lo que importa es si existe UNA recta que separe las clases, y para OR sí existe (aísla el único caso (0,0)→0 de los otros tres).",
    "El código de crear_solucion/entrenamiento no depende de qué compuerta lógica se esté aprendiendo — solo depende de la forma de X e y (4 filas, 2 columnas, salida 0/1), la misma estructura que AND.",
    "El número de épocas necesarias depende de dónde arrancan los pesos y de la geometría exacta del problema, no de una relación fija como 'el triple' — no hay ninguna garantía matemática de esa proporción."
   ],
   "steps": [
    "Anotá los 4 puntos de OR con su clase: (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→1.",
    "Buscá una recta que separe el único punto de clase 0 ((0,0)) de los tres de clase 1 — existe (por ejemplo, x+y ≥ 0.5).",
    "Como SÍ es linealmente separable, el perceptrón simple (mismo código, sin capa oculta) puede converger a 0 errores, igual que hace con AND."
   ],
   "stakes": "Distinguir qué problemas SÍ resuelve un modelo lineal simple (AND, OR) de cuáles NO (XOR) es la habilidad concreta que evita perder tiempo intentando forzar un modelo demasiado simple sobre un problema que, por su geometría, nunca podría resolver."
  }
 ],
 [
  {
   "question": "El perceptrón sin capa oculta (el mismo que aprendió AND en el tema anterior) termina con solo 25% de accuracy en XOR, y sus errores por época nunca bajan de 4. ¿Por qué falla tan claramente?",
   "type": "mc",
   "options": [
    "Porque XOR no es linealmente separable, y el perceptrón solo puede trazar UNA frontera recta entre las clases",
    "Porque el código tiene un error de sintaxis que impide el entrenamiento correcto",
    "Porque XOR necesita más de 4 ejemplos de entrenamiento para poder aprenderse",
    "Porque este perceptrón funciona distinto al que aprendió AND en el tema anterior"
   ],
   "correct": 0,
   "solution": "Ninguna línea recta puede separar los puntos de XOR (donde 1,1 y 0,0 son de una clase, y 0,1 y 1,0 de la otra) — y el perceptrón, por dentro, SOLO puede dibujar fronteras rectas (lineales). Por eso sus errores nunca llegan a 0: no existe ninguna combinación de w y b que clasifique bien los 4 casos a la vez.",
   "whyNot": [
    null,
    "El código entrena sin errores de ejecución (el propio código imprime los resultados) — el problema no es de sintaxis, es una limitación estructural del modelo lineal frente a un problema no lineal.",
    "XOR con 4 ejemplos ya representa TODOS los casos posibles con 2 entradas binarias — agregar más ejemplos repetidos no ayudaría, porque el problema no es de cantidad de datos sino de la forma de la frontera de separación.",
    "Es literalmente el mismo código de entrenamiento del perceptrón que en el tema anterior (misma función escalón, misma regla de actualización) — lo único que cambió son los datos (X e y), de AND a XOR."
   ],
   "steps": [
    "Graficá mentalmente los 4 puntos de XOR: los de clase 1 quedan en esquinas opuestas respecto a los de clase 0.",
    "El perceptrón, por dentro, solo puede dibujar una frontera de decisión recta (lineal) — no tiene forma de curvarla.",
    "Ninguna recta separa bien esos 4 puntos, así que ninguna combinación de w y b logra clasificarlos todos correctamente.",
    "Por eso los errores nunca bajan de 4 — no es un bug de código, es una limitación estructural del modelo."
   ],
   "stakes": "Ver una accuracy estancada en un valor sospechosamente bajo (como 25%, uno de cuatro) es una señal real de que el modelo tiene una limitación estructural, no que falte más entrenamiento — diagnosticar mal esto hace perder tiempo en vez de cambiar de arquitectura."
  },
  {
   "question": "Según la línea 'mlp = MLPClassifier(hidden_layer_sizes=(4,), activation='relu', max_iter=2000, random_state=1).fit(X, y)', ¿cuántas neuronas tiene la capa oculta del MLP y qué función de activación usa?",
   "type": "mc",
   "options": [
    "4 neuronas en la capa oculta, con activación ReLU",
    "1 neurona en la capa oculta, con activación escalón",
    "4 neuronas en la capa oculta, con activación sigmoide",
    "2000 neuronas en la capa oculta, una por cada iteración de entrenamiento"
   ],
   "correct": 0,
   "solution": "El parámetro hidden_layer_sizes=(4,) fija UNA capa oculta con 4 neuronas, y activation='relu' fija la función de activación de esa capa como ReLU — ambos son parámetros de arquitectura, definidos antes de entrenar.",
   "whyNot": [
    null,
    "La activación 'escalón' es la del perceptrón del tema anterior (la función escalon() definida a mano) — el MLP de este código usa 'relu', un parámetro de texto distinto, explícito en la línea de creación del modelo.",
    "El texto dice activation='relu', no 'sigmoid' — sigmoide es otra activación posible en general, pero no la que este código configura.",
    "max_iter=2000 es un parámetro totalmente distinto: fija el número MÁXIMO de iteraciones de entrenamiento, no tiene ninguna relación con la cantidad de neuronas de la capa oculta (esa es hidden_layer_sizes=(4,))."
   ],
   "steps": [
    "Ubicá los parámetros del constructor MLPClassifier(...) en el código.",
    "hidden_layer_sizes=(4,) es una tupla de un solo elemento: una capa oculta, con 4 neuronas.",
    "activation='relu' es un parámetro separado, que fija qué función de activación usan esas 4 neuronas.",
    "max_iter=2000 es otro parámetro distinto (límite de iteraciones), no debe confundirse con la cantidad de neuronas."
   ],
   "stakes": "Leer con cuidado los hiperparámetros de un modelo real (cuántas neuronas, qué activación) es el primer paso antes de modificar o depurar cualquier red — confundir 'cantidad de neuronas' con 'cantidad de iteraciones' es un error común al leer código ajeno por primera vez."
  },
  {
   "question": "El mismo constructor incluye 'max_iter=2000'. Si el MLP ya converge (deja de mejorar) mucho antes de la iteración 2000, ¿qué rol cumple igual ese parámetro?",
   "type": "mc",
   "options": [
    "Es un LÍMITE máximo de seguridad: el entrenamiento se detiene ahí si todavía no convergió, evitando que corra indefinidamente",
    "Obliga a la red a entrenar exactamente 2000 iteraciones, sin importar si ya convergió antes",
    "Determina cuántas neuronas tendrá la capa oculta",
    "Es el número de ejemplos de entrenamiento (filas de X) que usa el modelo"
   ],
   "correct": 0,
   "solution": "max_iter fija un TOPE: el entrenamiento puede parar antes si ya convergió (el error deja de mejorar lo suficiente), pero nunca sigue más allá de ese número de iteraciones — es una salvaguarda para que el entrenamiento no corra indefinidamente si el modelo tarda en converger o nunca lo hace del todo.",
   "whyNot": [
    null,
    "sklearn detiene el entrenamiento antes de max_iter si detecta que el error ya no mejora lo suficiente (criterio de convergencia interno) — no fuerza a completar las 2000 iteraciones si ya no hace falta.",
    "La cantidad de neuronas de la capa oculta se define por separado, con hidden_layer_sizes=(4,) — max_iter no tiene ninguna relación con la arquitectura de la red.",
    "El número de ejemplos de entrenamiento está dado por la forma de X (4 filas, una por cada combinación de la compuerta lógica) — max_iter no cuenta ejemplos, cuenta iteraciones del algoritmo de optimización sobre esos mismos ejemplos."
   ],
   "steps": [
    "max_iter es un parámetro del ALGORITMO de optimización, no de los DATOS ni de la ARQUITECTURA de la red.",
    "Actúa como un tope máximo: si el modelo converge antes, el entrenamiento para ahí; si no converge, para en max_iter de todas formas.",
    "Por eso es una salvaguarda de tiempo/cómputo, no una cantidad fija obligatoria de pasos."
   ],
   "stakes": "Fijar un max_iter razonable es la diferencia entre un entrenamiento que se detiene solo (o a tiempo) y uno que corre indefinidamente sin converger, consumiendo cómputo sin ningún beneficio adicional — un ajuste práctico común al entrenar cualquier modelo real."
  }
 ],
 [
  {
   "question": "El MLP con una capa oculta de 4 neuronas y activación ReLU logra 100% de accuracy en XOR. ¿Qué le permite lograr esto que el perceptrón sin capa oculta no tiene?",
   "type": "mc",
   "options": [
    "Una capa oculta con activación NO lineal, que le permite combinar varias fronteras rectas simples en una frontera final curva/quebrada",
    "Simplemente tener más parámetros numéricos, sin importar cómo estén organizados",
    "Usar una tasa de aprendizaje distinta a la del perceptrón",
    "Entrenar con más ejemplos de datos que el perceptrón"
   ],
   "correct": 0,
   "solution": "La clave no es 'más parámetros' en general, sino la combinación de una capa OCULTA (una etapa intermedia de procesamiento) con una activación NO LINEAL (ReLU) — eso le permite a la red construir fronteras de decisión curvas/quebradas, algo que ninguna cantidad de capas puramente lineales podría lograr.",
   "whyNot": [
    null,
    "Sin la activación NO LINEAL, apilar más parámetros/capas lineales matemáticamente colapsa en una única transformación lineal — la clave no es la cantidad de parámetros sino que sean no lineales.",
    "El perceptrón y el MLP usan tasas de aprendizaje que se configuran por separado (lr=0.1 en el perceptrón; el optimizador interno del MLP en el otro caso) — pero la diferencia de resultado no viene de ese hiperparámetro, sino de la arquitectura.",
    "Ambos modelos (el perceptrón y el MLP) se entrenan sobre EXACTAMENTE los mismos 4 ejemplos de X e y — la diferencia de resultado no viene de la cantidad de datos, sino de la arquitectura del modelo."
   ],
   "steps": [
    "Compará: el perceptrón fallaba porque solo puede trazar UNA recta. El MLP tiene una capa OCULTA en el medio.",
    "Esa capa oculta usa ReLU, una activación NO lineal — sin eso, apilar capas seguiría siendo equivalente a una sola transformación lineal.",
    "Con capa oculta + no-linealidad, la red puede combinar varias fronteras rectas simples en una frontera final curva o quebrada.",
    "Esa combinación es justo lo que le permite separar los 4 puntos de XOR, algo que el perceptrón simple no podía."
   ],
   "stakes": "Esta es la razón concreta por la que las redes modernas usan capas ocultas con activaciones no lineales — sin esa combinación, ninguna cantidad de 'más datos' o 'más entrenamiento' hubiera resuelto problemas como el reconocimiento de imágenes."
  },
  {
   "question": "Según la teoría de este tema, ¿qué valor exacto imprime 'mlp.score(X, y)' como accuracy del MLP sobre XOR?",
   "type": "numeric",
   "correct": 1.0,
   "decimals": 1,
   "solution": "La teoría lo dice explícitamente: el MLP 'resuelve XOR con 100% de precisión' — mlp.score(X, y) devuelve la fracción de aciertos, y 100% de precisión equivale a un score de 1.0 (el máximo posible).",
   "steps": [
    "Ubicá en la teoría la frase sobre el resultado del MLP: '100% de precisión'.",
    "mlp.score(X, y) devuelve esa precisión como una fracción entre 0 y 1, no como un porcentaje directo.",
    "100% de precisión corresponde exactamente a un score de 1.0 — el valor máximo posible, sin ningún error."
   ],
   "stakes": "Reconocer que score() devuelve una fracción (0 a 1) y no un porcentaje directo es un detalle práctico esencial al leer métricas de cualquier modelo de sklearn en un proyecto real."
  },
  {
   "question": "El MLP usa activation='relu'. Matemáticamente, ¿qué calcula ReLU sobre un número de entrada z?",
   "type": "mc",
   "options": [
    "max(0, z): devuelve z si es positivo, y 0 si es negativo o cero — deja pasar la parte positiva, apaga la negativa",
    "1 si z ≥ 0, y 0 si z < 0 — igual que la función escalón del perceptrón",
    "El promedio entre z y 0",
    "z al cuadrado, siempre un valor positivo"
   ],
   "correct": 0,
   "solution": "ReLU(z) = max(0, z): si z es positivo, lo deja pasar sin cambios; si es negativo (o cero), lo convierte en 0. A diferencia de la función escalón (que solo devuelve 0 o 1), ReLU conserva el VALOR real cuando es positivo — no lo aplasta a una sola categoría binaria.",
   "whyNot": [
    null,
    "Esa es exactamente la definición de escalón(z), la activación del perceptrón del tema anterior — ReLU es distinta: no colapsa todo a 0 o 1, deja pasar el valor real cuando es positivo.",
    "ReLU no promedia z con 0 — o bien deja pasar z tal cual (si es positivo), o lo anula por completo a 0 (si es negativo); no hay ningún punto intermedio.",
    "Elevar al cuadrado siempre daría un resultado positivo incluso para z negativos, perdiendo el signo — ReLU en cambio SÍ distingue: los positivos pasan intactos, los negativos se anulan a 0."
   ],
   "steps": [
    "ReLU(z) = max(0, z) es la definición formal: compara z con 0 y se queda con el mayor de los dos.",
    "Si z > 0, max(0, z) = z — el valor pasa sin cambios.",
    "Si z ≤ 0, max(0, z) = 0 — el valor se anula por completo.",
    "A diferencia de escalón(), que solo devuelve 0 o 1, ReLU conserva la MAGNITUD real del valor positivo."
   ],
   "stakes": "ReLU es la activación más usada en redes profundas modernas precisamente porque, a diferencia de escalón o sigmoide, no 'aplasta' los valores grandes — eso ayuda a que el gradiente siga fluyendo bien incluso en redes con muchas capas."
  }
 ],
 [
  {
   "question": "¿Qué significa concretamente que XOR 'no sea linealmente separable'?",
   "type": "mc",
   "options": [
    "Que no existe ninguna línea recta que deje todos los puntos de una clase de un lado, y todos los de la otra clase del otro lado",
    "Que XOR solo puede calcularse con números negativos",
    "Que XOR tiene más de 4 combinaciones posibles de entrada",
    "Que XOR requiere una computadora más potente que AND para calcularse"
   ],
   "correct": 0,
   "solution": "XOR tiene 4 puntos: (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→0. Si los graficás, los dos puntos de clase 1 quedan en 'esquinas opuestas' respecto a los de clase 0 — no existe ninguna recta que los separe correctamente en dos grupos, a diferencia de AND (que sí es separable con una recta).",
   "whyNot": [
    null,
    "XOR se calcula sobre valores binarios (0 y 1), sin ningún número negativo involucrado — la 'no separabilidad lineal' es una propiedad geométrica de cómo se distribuyen esos 4 puntos, no del signo de los números.",
    "XOR, igual que AND, tiene exactamente 4 combinaciones posibles con 2 entradas binarias (2²=4) — la diferencia entre ambos no está en la cantidad de combinaciones, sino en cómo se distribuyen las clases entre esas 4.",
    "Calcular XOR (con una tabla de verdad o con una red ya entrenada) no requiere más potencia de cómputo que AND — la dificultad no es de recursos de hardware, es de la geometría del problema para un modelo lineal."
   ],
   "steps": [
    "Anotá los 4 puntos de XOR con su clase: (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→0.",
    "Intentá trazar (mentalmente) una sola línea recta que deje todos los '0' de un lado y todos los '1' del otro — no existe ninguna.",
    "Esa imposibilidad de separar las clases con una recta es exactamente lo que significa 'no ser linealmente separable'."
   ],
   "stakes": "Antes de elegir un modelo para un problema real, preguntarse si las clases son separables con una frontera simple ahorra tiempo: si no lo son, como en la mayoría de los problemas reales de visión o lenguaje, un modelo lineal está condenado a fallar."
  },
  {
   "question": "El comentario del código dice: '(Un solo import de sklearn, no dos, para que el sandbox de esta app no se acerque al limite de 12s solo por el costo de importar.)' ¿A qué se refiere exactamente ese comentario?",
   "type": "mc",
   "options": [
    "A que el código evita a propósito hacer dos imports de sklearn, porque el simple hecho de importar puede consumir varios segundos, acercándose al límite de tiempo del sandbox de esta app",
    "A que sklearn tiene un límite interno de 12 segundos para entrenar cualquier modelo",
    "A que el MLP tarda 12 segundos en converger si se usan más de 4 neuronas ocultas",
    "A que hay que instalar sklearn en menos de 12 segundos para que el código funcione"
   ],
   "correct": 0,
   "solution": "El comentario explica una decisión de diseño del propio ejercicio: importar librerías como sklearn no es instantáneo, y hacerlo dos veces en el mismo código sumaría un costo de tiempo evitable — por eso se usa un solo import, para no arriesgarse a superar el límite de 12 segundos que tiene el sandbox donde corre este código.",
   "whyNot": [
    null,
    "El '12s' no es un límite interno de sklearn — es el límite de tiempo del SANDBOX de esta aplicación (mencionado explícitamente en el comentario), una restricción externa a la librería.",
    "El comentario no dice nada sobre la cantidad de neuronas ocultas afectando el tiempo de convergencia — habla específicamente del COSTO DE IMPORTAR la librería, un paso que ocurre antes de que empiece cualquier entrenamiento.",
    "El comentario habla del costo de tiempo de EJECUTAR el import dentro del código (cuando el script corre), no de instalar el paquete sklearn en el sistema — son dos cosas distintas."
   ],
   "steps": [
    "Leé el comentario tal cual: menciona 'un solo import' y 'el costo de importar', junto con un límite de '12s' del sandbox.",
    "Importar una librería grande como sklearn no es gratis en tiempo — hacerlo de más puede sumar segundos.",
    "Por eso el código se cuida de usar un solo 'from sklearn... import MLPClassifier', evitando duplicar ese costo y arriesgarse a pasar el límite de tiempo permitido."
   ],
   "stakes": "Optimizar los imports para no acercarse a un límite de tiempo es una preocupación real en cualquier sistema con timeouts estrictos, como funciones serverless o sandboxes de ejecución de código, donde hasta el tiempo de 'preparar' el entorno cuenta."
  },
  {
   "question": "El constructor incluye 'random_state=1'. ¿Qué garantiza ese parámetro sobre el entrenamiento del MLP?",
   "type": "mc",
   "options": [
    "Que la inicialización aleatoria de los pesos (y cualquier otro paso con azar interno) sea siempre la misma, haciendo el resultado reproducible al repetir el entrenamiento",
    "Que el MLP entrene exactamente 1 iteración antes de evaluar",
    "Que la red tenga exactamente 1 capa oculta",
    "Que solo se use el primer ejemplo de X para entrenar"
   ],
   "correct": 0,
   "solution": "random_state=1 cumple el mismo rol que np.random.seed(0) en el perceptrón: fija la semilla del generador de números aleatorios que usa sklearn internamente (para inicializar pesos, entre otras cosas), garantizando que correr el mismo código dos veces dé exactamente el mismo resultado.",
   "whyNot": [
    null,
    "El número de iteraciones lo controla max_iter=2000, un parámetro totalmente distinto — random_state no tiene ninguna relación con cuántas iteraciones se ejecutan.",
    "La cantidad de capas ocultas la define hidden_layer_sizes=(4,) — random_state=1 es un número de semilla, no una cantidad de capas (podría ser cualquier entero, como 0, 42, o 7, sin cambiar la arquitectura).",
    "El MLP entrena con TODOS los ejemplos de X en cada iteración (no solo el primero) — random_state no filtra ni selecciona ejemplos, solo fija la semilla de los procesos aleatorios internos del entrenamiento."
   ],
   "steps": [
    "random_state, igual que np.random.seed() visto en el perceptrón, fija la semilla de los números 'aleatorios' que usa el algoritmo internamente.",
    "Eso incluye la inicialización de los pesos del MLP antes de empezar a entrenar.",
    "Con la semilla fija, el resultado final es reproducible: mismo código, mismo random_state, mismo resultado siempre."
   ],
   "stakes": "random_state es el mismo mecanismo de reproducibilidad, ahora aplicado a través de la API de sklearn en vez de escrito a mano — reconocerlo en cualquier modelo de sklearn (árboles, MLP, clustering) es clave para poder reproducir resultados reportados por otros."
  }
 ],
 [
  {
   "question": "Un aproximador universal (como un MLP con capa oculta y activación no lineal) puede aproximar 'cualquier función continua'. ¿Qué implica esto sobre el rol de la capa oculta?",
   "type": "mc",
   "options": [
    "Que la capa oculta con no-linealidad es lo que le da a la red la flexibilidad para aprender relaciones complejas, no solo las que se separan con una línea recta",
    "Que cualquier red, sin importar su arquitectura, puede aprender cualquier problema con precisión perfecta en la práctica",
    "Que la capa oculta solo sirve para acelerar el cálculo, no para aumentar la capacidad del modelo",
    "Que basta con una sola neurona en la capa oculta para resolver cualquier problema, sin importar su complejidad"
   ],
   "correct": 0,
   "solution": "El resultado teórico de 'aproximador universal' es justamente sobre la CAPACIDAD del modelo (qué tipo de funciones puede llegar a representar), gracias a combinar una capa oculta con no-linealidad — es la propiedad matemática detrás de por qué el MLP sí puede resolver XOR y el perceptrón sin capa oculta no.",
   "whyNot": [
    null,
    "'Puede aproximar' es una propiedad teórica de capacidad — en la práctica, entrenar bien (encontrar esos pesos) depende de datos suficientes, buena optimización y suficientes neuronas, no está garantizado automáticamente para cualquier problema.",
    "Es lo contrario: la capa oculta es justamente lo que AUMENTA la capacidad expresiva del modelo (qué funciones puede representar) — no es solo una optimización de velocidad de cómputo.",
    "El número de neuronas necesarias depende de la complejidad del problema — el código mismo usa 4 neuronas para XOR, no 1; una sola neurona oculta no garantiza poder resolver cualquier problema complejo."
   ],
   "steps": [
    "El resultado de 'aproximador universal' habla de qué funciones puede LLEGAR a representar el modelo — su capacidad, no si en la práctica logra precisión perfecta.",
    "Esa capacidad viene específicamente de combinar una capa oculta con una activación no lineal — sin esa combinación, no hay flexibilidad para curvar fronteras.",
    "Es la misma razón, en teoría, por la que el MLP resuelve XOR y el perceptrón simple no."
   ],
   "stakes": "Este resultado teórico es la garantía matemática detrás de por qué las redes neuronales se usan para casi cualquier problema — desde predecir el clima hasta traducir idiomas — en vez de diseñar una fórmula distinta a mano para cada caso."
  },
  {
   "question": "¿Qué calcula exactamente la línea 'acc_perc = sum(p == yy for p, yy in zip(preds_perc, y)) / 4'?",
   "type": "mc",
   "options": [
    "La fracción de las 4 predicciones del perceptrón que coinciden con el valor esperado (accuracy), comparando cada predicción con su etiqueta real",
    "La suma total de todas las predicciones del perceptrón, sin compararlas con nada",
    "La cantidad de épocas que tardó el perceptrón en entrenar",
    "La diferencia promedio entre los pesos iniciales y finales del perceptrón"
   ],
   "correct": 0,
   "solution": "zip(preds_perc, y) empareja cada predicción con su etiqueta esperada; 'p == yy' da True (1) o False (0) por cada par; sum(...) cuenta cuántos aciertos hubo; dividir por 4 (el total de casos) da la fracción de aciertos — exactamente la definición de accuracy.",
   "whyNot": [
    null,
    "La línea no suma las predicciones en sí (0s y 1s de preds_perc) — suma el resultado de COMPARAR cada predicción con su valor esperado (p == yy), que es una cuenta de aciertos, no una suma de las predicciones.",
    "La cantidad de épocas está controlada por 'for epoca in range(30)', una variable completamente distinta — esta línea no cuenta iteraciones de entrenamiento, cuenta aciertos de predicción.",
    "Esta línea no compara pesos en ningún momento — trabaja únicamente con 'preds_perc' (predicciones) e 'y' (etiquetas esperadas), ninguno de los dos relacionado con los valores de w."
   ],
   "steps": [
    "Separá la expresión en partes: zip(preds_perc, y) empareja cada predicción con su etiqueta real, una por una.",
    "'p == yy' da True/False para cada par — True cuenta como 1 al sumarse.",
    "sum(...) suma esos aciertos (0 a 4 posibles), y dividir por 4 lo convierte en una fracción entre 0 y 1.",
    "Esa fracción de aciertos sobre el total de casos es exactamente la definición de accuracy."
   ],
   "stakes": "Esta es la forma más básica de calcular accuracy a mano — entender esta línea por línea es lo que permite reconocer (y confiar en) lo que hace mlp.score(X, y) por dentro, en el modelo que sí usa una librería."
  },
  {
   "question": "hidden_layer_sizes=(4,) es una TUPLA con un solo elemento. Si el código dijera hidden_layer_sizes=(4, 2) en cambio, ¿qué arquitectura describiría?",
   "type": "mc",
   "options": [
    "DOS capas ocultas: la primera con 4 neuronas, la segunda con 2 neuronas",
    "Una sola capa oculta, pero con 4×2=8 neuronas en total",
    "Una capa oculta de 4 neuronas, entrenada durante 2 épocas",
    "Un error de sintaxis, porque hidden_layer_sizes solo acepta un número, no una tupla"
   ],
   "correct": 0,
   "solution": "hidden_layer_sizes es una tupla donde CADA posición representa una capa oculta distinta, y el valor en esa posición es cuántas neuronas tiene esa capa — (4, 2) significa 2 capas ocultas en secuencia: primero una de 4 neuronas, después una de 2. Con (4,) (un solo elemento) hay una única capa oculta, de 4 neuronas.",
   "whyNot": [
    null,
    "sklearn no multiplica los números de la tupla entre sí — cada posición es una capa SEPARADA, no un cálculo combinado del total de neuronas.",
    "hidden_layer_sizes no tiene relación con la cantidad de épocas de entrenamiento — eso lo controla max_iter, un parámetro completamente distinto.",
    "hidden_layer_sizes en sklearn acepta explícitamente una tupla — es precisamente el mecanismo para definir MÚLTIPLES capas ocultas de distinto tamaño, no un error."
   ],
   "steps": [
    "hidden_layer_sizes es una tupla, y cada POSICIÓN de la tupla es una capa oculta distinta.",
    "El VALOR en cada posición es cuántas neuronas tiene esa capa específica.",
    "(4,) tiene una sola posición → una sola capa oculta de 4 neuronas.",
    "(4, 2) tendría dos posiciones → dos capas ocultas en secuencia: 4 neuronas primero, 2 después."
   ],
   "stakes": "Entender que hidden_layer_sizes describe la PROFUNDIDAD (cuántas capas) y el ANCHO (neuronas por capa) de la red al mismo tiempo es lo que permite diseñar arquitecturas de MLP más complejas en sklearn sin cambiar de librería."
  }
 ],
 [
  {
   "question": "El loss arranca en 0,6657 y baja a 0,1039 tras 2000 iteraciones. ¿Qué representa cada uno de esos 'pasos' de bajada?",
   "type": "mc",
   "options": [
    "Un ajuste real de los pesos de la red en la dirección que más reduce el error, calculado por backpropagation",
    "Un cambio aleatorio de los pesos, sin relación con el error real",
    "Una repetición exacta del mismo cálculo, sin ningún cambio en los pesos",
    "Una reducción del número de neuronas de la red en cada iteración"
   ],
   "correct": 0,
   "solution": "Cada punto de loss_curve_ corresponde a una iteración de entrenamiento REAL: se calcula el error, se propaga hacia atrás (backpropagation) para obtener el gradiente de cada peso, y cada peso se actualiza en la dirección que reduce ese error — por eso el loss baja de forma consistente, no al azar.",
   "whyNot": [
    null,
    "El descenso del gradiente es dirigido, no aleatorio — cada ajuste de pesos sigue la dirección que la regla de la cadena calcula como la que MÁS reduce el error, por eso el loss baja consistentemente en vez de fluctuar sin patrón.",
    "Si los pesos no cambiaran, el loss se quedaría exactamente igual en las 2000 iteraciones — el hecho de que baje de 0,6657 a 0,1039 es la prueba directa de que SÍ hay ajustes reales en cada paso.",
    "La arquitectura de la red (hidden_layer_sizes=(4,), fija en el código) no cambia durante el entrenamiento — lo que se ajusta en cada iteración son los PESOS de esas neuronas, no su cantidad."
   ],
   "steps": [
    "El loss baja de forma consistente y gradual (0,6657 → 0,1039), no de golpe ni al azar — eso ya sugiere un proceso dirigido, no aleatorio.",
    "Cada punto de esa curva corresponde a una iteración de entrenamiento: se mide el error, se calcula el gradiente con backpropagation, y se ajustan los pesos en la dirección que MÁS reduce ese error.",
    "Por eso cada paso de bajada es un ajuste real de pesos, calculado matemáticamente, no un cambio arbitrario."
   ],
   "stakes": "En un entrenamiento real, ver que el loss NO baja (se queda plano o sube) es la primera señal de que algo está mal: un learning rate mal elegido, datos sin normalizar, o un bug en el cálculo del error."
  },
  {
   "question": "La línea 'idxs = [0, len(lc)//4, len(lc)//2, (3*len(lc))//4, len(lc)-1]' arma una lista de 5 índices. ¿Qué representan esos 5 puntos respecto al entrenamiento completo?",
   "type": "mc",
   "options": [
    "5 momentos distribuidos a lo largo de todo el entrenamiento: el inicio, el 25%, el 50%, el 75% y el final",
    "Las 5 primeras iteraciones del entrenamiento, una tras otra",
    "Los 5 valores de loss más bajos registrados durante todo el entrenamiento",
    "Los índices de las 5 neuronas de la capa oculta"
   ],
   "correct": 0,
   "solution": "0 es el primer índice (inicio), len(lc)//4 es el 25% del recorrido, len(lc)//2 es la mitad (50%), (3*len(lc))//4 es el 75%, y len(lc)-1 es el último índice (final) — juntos, esos 5 puntos muestrean el progreso del entrenamiento de forma pareja, del principio al fin.",
   "whyNot": [
    null,
    "Las primeras 5 iteraciones serían índices 0,1,2,3,4 consecutivos — pero la lista usa fracciones de len(lc) (//4, //2, 3*len(lc)//4), que reparten los puntos a lo LARGO de todo el entrenamiento, no al principio.",
    "La lista idxs se arma ANTES de mirar ningún valor de loss — son posiciones fijas basadas en fracciones de la longitud total, no una selección de los valores más bajos encontrados.",
    "hidden_layer_sizes=(4,) define las neuronas de la capa oculta (4 en total, no 5) — idxs no tiene ninguna relación con la cantidad de neuronas, es una lista de índices sobre lc (la curva de loss)."
   ],
   "steps": [
    "Calculá qué fracción del total representa cada término: 0 es 0%, len(lc)//4 es 25%, len(lc)//2 es 50%, (3*len(lc))//4 es 75%, len(lc)-1 es el último índice (100%).",
    "Esas 5 fracciones cubren el entrenamiento de punta a punta, espaciadas de forma pareja.",
    "Por eso el bucle 'for i in idxs' imprime una especie de 'resumen' del progreso del loss, no solo el principio ni solo el final."
   ],
   "stakes": "Muestrear una curva de entrenamiento en puntos parejos (no solo el primer y último valor) es una práctica común real para diagnosticar visualmente si el descenso fue gradual y estable, o si tuvo saltos bruscos en algún tramo intermedio."
  },
  {
   "question": "Backpropagation calcula el gradiente empezando por la capa de SALIDA y yendo hacia atrás, capa por capa, hasta la primera. ¿Por qué en ESE orden, y no calculando primero el gradiente de la primera capa?",
   "type": "mc",
   "options": [
    "Porque, por la regla de la cadena, el gradiente de una capa depende del gradiente YA CALCULADO de la capa siguiente — hace falta la salida primero para poder ir 'heredando' ese cálculo hacia atrás",
    "Por convención arbitraria: matemáticamente daría igual empezar por cualquier capa",
    "Porque la capa de salida siempre tiene menos neuronas, así que es más rápida de calcular primero",
    "Porque sklearn ordena las capas de atrás hacia adelante en la memoria de la computadora"
   ],
   "correct": 0,
   "solution": "La regla de la cadena del cálculo diferencial hace que el gradiente de los pesos de una capa dependa del gradiente YA CALCULADO en la capa siguiente (más cerca de la salida) — por eso el cálculo tiene que empezar en la salida (donde se conoce el error directamente) y propagarse hacia atrás, reutilizando cada resultado para la capa anterior. Calcular en el orden opuesto no sería posible: faltaría la información que todavía no se calculó.",
   "whyNot": [
    null,
    "No es una convención arbitraria — es una consecuencia matemática directa de la regla de la cadena: el gradiente de una capa interior se construye multiplicando por el gradiente ya obtenido de la capa siguiente, así que ese orden es obligatorio, no elegido.",
    "El tamaño (cantidad de neuronas) de la capa de salida no tiene relación con el orden de cálculo — el orden lo exige la dependencia matemática entre gradientes de capas consecutivas, no la velocidad de cómputo de cada capa.",
    "El orden no es una cuestión de cómo se almacenan las capas en memoria — es la propia definición matemática de la regla de la cadena la que exige ir de la salida hacia atrás."
   ],
   "steps": [
    "El error solo se puede medir directamente en la capa de SALIDA (comparando la predicción con lo esperado).",
    "Por la regla de la cadena, el gradiente de una capa interior se calcula MULTIPLICANDO por el gradiente ya obtenido de la capa siguiente.",
    "Eso significa que hace falta el gradiente de la capa de salida ANTES de poder calcular el de la capa anterior, y así sucesivamente hacia atrás.",
    "De ahí el nombre 'back'-propagation: el cálculo necesariamente fluye de la salida hacia la entrada."
   ],
   "stakes": "Entender esta dependencia entre capas es la base para diagnosticar el problema del 'gradiente que se desvanece' en redes muy profundas, donde el gradiente se vuelve casi 0 al llegar a las primeras capas después de multiplicarse muchas veces."
  }
 ],
 [
  {
   "question": "¿Qué hace exactamente el algoritmo de backpropagation, según la teoría de este tema?",
   "type": "mc",
   "options": [
    "Calcula el gradiente del error respecto a CADA peso de la red, propagando el error hacia atrás capa por capa mediante la regla de la cadena",
    "Elimina las neuronas que contribuyen menos a la predicción final",
    "Genera nuevos datos de entrenamiento sintéticos para mejorar la precisión",
    "Decide cuántas capas ocultas debe tener la red antes de entrenar"
   ],
   "correct": 0,
   "solution": "Backpropagation es específicamente el método para calcular ∂L/∂w para cada peso w de la red, yendo desde la capa de salida hacia atrás, usando la regla de la cadena del cálculo diferencial — ese gradiente es lo que después usa el descenso del gradiente para actualizar cada peso.",
   "whyNot": [
    null,
    "Backpropagation no elimina neuronas — calcula gradientes para AJUSTAR los pesos existentes; eliminar neuronas describiría otra técnica distinta (poda de redes), no backpropagation.",
    "Backpropagation no genera datos nuevos — trabaja únicamente con los datos de entrenamiento ya existentes (X, y) para calcular el error y sus gradientes.",
    "La cantidad de capas ocultas (hidden_layer_sizes=(4,) en el código) es una decisión de arquitectura que se fija ANTES de entrenar, no algo que backpropagation decida durante el entrenamiento."
   ],
   "steps": [
    "El nombre da la pista: 'back' + 'propagation' — el error se propaga hacia ATRÁS, desde la salida hacia las capas anteriores.",
    "Lo que se calcula en cada capa es el gradiente del error respecto a CADA peso (∂L/∂w), usando la regla de la cadena del cálculo.",
    "No elimina neuronas, no genera datos nuevos, no decide arquitectura — solo calcula ese gradiente capa por capa."
   ],
   "stakes": "Cuando un modelo real de deep learning 'no aprende', entender qué hace exactamente backpropagation es lo que permite diagnosticar dónde se corta el flujo del gradiente, en vez de solo probar configuraciones al azar."
  },
  {
   "question": "El código entrena el MLP con solver='adam'. ¿Qué es 'adam' en este contexto?",
   "type": "mc",
   "options": [
    "Un algoritmo optimizador — una variante más sofisticada del descenso del gradiente básico, usada para ajustar los pesos en cada iteración",
    "El nombre de la arquitectura de la red (cuántas capas y neuronas tiene)",
    "La función de activación de la capa oculta",
    "El nombre del conjunto de datos de entrenamiento"
   ],
   "correct": 0,
   "solution": "solver='adam' elige QUÉ algoritmo de optimización usa internamente el MLP para actualizar los pesos en cada iteración — Adam es una variante del descenso del gradiente que ajusta automáticamente el tamaño de paso para cada peso, distinta del descenso del gradiente 'plano' visto en la fórmula w ← w − η·∂L/∂w.",
   "whyNot": [
    null,
    "La arquitectura (cuántas capas y neuronas) se define por separado, con hidden_layer_sizes=(4,) — solver es un parámetro distinto, sobre CÓMO se optimizan los pesos, no sobre la forma de la red.",
    "La activación de la capa oculta se define con activation='relu', en el tema anterior — no tiene relación con el parámetro solver, que decide el método de optimización, no la activación de las neuronas.",
    "El dataset de entrenamiento son X e y, definidos aparte al principio del código — solver no se refiere a ningún dato, sino al algoritmo que ajusta los pesos usando esos datos."
   ],
   "steps": [
    "Ubicá dónde aparece 'adam' en el código: como valor del parámetro solver=, al construir el MLPClassifier.",
    "solver decide QUÉ algoritmo de optimización usa el modelo para actualizar los pesos en cada paso.",
    "Adam es una variante del descenso del gradiente (el mismo principio general de este tema), pero más sofisticada — no es un dato, ni una arquitectura, ni una activación."
   ],
   "stakes": "Elegir el optimizador correcto (adam, SGD, y otros) es una decisión práctica real al entrenar cualquier red: Adam suele converger más rápido y con menos ajuste manual del learning rate que el descenso del gradiente clásico, por eso es tan usado por defecto."
  },
  {
   "question": "El código lee 'lc = mlp.loss_curve_' después de entrenar. ¿Qué tipo de información contiene ese atributo?",
   "type": "mc",
   "options": [
    "Una lista con el valor del loss al final de CADA iteración de entrenamiento, en orden — el historial completo del descenso",
    "Un único número: el loss final tras la última iteración",
    "Los pesos finales de todas las neuronas de la red",
    "La cantidad total de neuronas que tiene el MLP"
   ],
   "correct": 0,
   "solution": "loss_curve_ es un atributo que sklearn expone DESPUÉS de entrenar (fit): una lista con un valor de loss por cada iteración recorrida, en orden — por eso el código puede indexarla (lc[0] para el inicio, lc[-1] para el final, o cualquier posición intermedia con idxs) para ver cómo bajó el error a lo largo de TODO el entrenamiento, no solo el resultado final.",
   "whyNot": [
    null,
    "Si fuera un único número, el código no podría hacer 'lc[0]' (loss inicial) Y 'lc[-1]' (loss final) por separado, ni muestrear 5 puntos intermedios con idxs — el hecho de que se pueda indexar en varias posiciones confirma que es una LISTA con un valor por iteración.",
    "Los pesos de la red se acceden con otro atributo distinto (mlp.coefs_), no con loss_curve_ — loss_curve_ guarda únicamente los valores de ERROR a lo largo del entrenamiento, no los parámetros aprendidos.",
    "La cantidad de neuronas está definida por hidden_layer_sizes, un parámetro de configuración fijado ANTES de entrenar — loss_curve_ es un resultado que se genera DURANTE el entrenamiento, sobre el error, no sobre la arquitectura."
   ],
   "steps": [
    "El código usa 'lc[0]', 'lc[-1]' y varios índices intermedios (idxs) sobre loss_curve_ — eso solo tiene sentido si es una secuencia con varios valores, no un número único.",
    "Cada posición de esa lista corresponde al loss medido al FINAL de una iteración de entrenamiento.",
    "Por eso loss_curve_ permite reconstruir, después de entrenar, cómo fue bajando el error paso a paso — el historial completo del descenso del gradiente."
   ],
   "stakes": "Guardar el historial completo del loss (no solo el valor final) es lo que permite graficar la curva de entrenamiento de un modelo real y diagnosticar visualmente problemas como sobreajuste o una tasa de aprendizaje mal elegida."
  }
 ],
 [
  {
   "question": "La fórmula de actualización es w ← w − η·(∂L/∂w). ¿Qué papel juega η (la tasa de aprendizaje) en esta fórmula?",
   "type": "mc",
   "options": [
    "Controla qué tan grande es cada paso de ajuste de los pesos en la dirección del gradiente",
    "Es el propio valor del error (loss) en esa iteración",
    "Cuenta cuántas neuronas tiene la capa oculta",
    "Determina cuántas iteraciones (max_iter) se van a entrenar en total"
   ],
   "correct": 0,
   "solution": "η (eta) multiplica al gradiente antes de restarlo del peso actual — un η grande da pasos grandes (puede converger rápido pero también 'pasarse' del mínimo); un η chico da pasos pequeños (más estable pero más lento). Es exactamente el mismo concepto de tasa de aprendizaje que ya se vio en el tema de la neurona artificial.",
   "whyNot": [
    null,
    "El loss (L) es una cantidad separada que se calcula a partir de las predicciones de la red — η es un hiperparámetro fijo que solo escala el TAMAÑO del ajuste de pesos, no es el error en sí.",
    "El número de neuronas de la capa oculta está fijado por hidden_layer_sizes=(4,) al construir el modelo — η no tiene relación con la arquitectura de la red, solo con la magnitud de cada actualización de pesos.",
    "max_iter=2000 es un parámetro totalmente distinto que limita cuántas iteraciones como máximo se van a ejecutar — η controla el TAMAÑO de cada paso individual, no la CANTIDAD de pasos."
   ],
   "steps": [
    "Mirá dónde aparece η en la fórmula: w ← w − η·(∂L/∂w) — multiplica al gradiente antes de restarlo del peso.",
    "Un η más grande hace que ese producto (y por lo tanto el ajuste) sea más grande: pasos más largos en cada actualización.",
    "Un η más chico da pasos más cortos y estables, pero más lentos para converger.",
    "Por eso η controla el TAMAÑO del paso de ajuste, no el error en sí ni la arquitectura de la red."
   ],
   "stakes": "Elegir mal la tasa de aprendizaje es de los errores más comunes al entrenar un modelo real: demasiado alta y el entrenamiento diverge (el loss explota), demasiado baja y tarda horas o días de más en converger."
  },
  {
   "question": "El código imprime round(lc[0], 4) como el loss inicial y round(lc[-1], 4) como el loss final, tras las 2000 iteraciones. ¿En qué valor exacto termina el loss al final del entrenamiento?",
   "type": "numeric",
   "correct": 0.1039,
   "decimals": 4,
   "solution": "La teoría lo indica explícitamente: 'el error (loss) arranca en 0,6657 y termina en 0,1039 después de 2000 iteraciones' — ese 0.1039 es el valor final impreso en la última de las 5 iteraciones muestreadas, el último punto de la curva de descenso.",
   "steps": [
    "Ubicá en la teoría los dos valores mencionados de loss: el inicial (0,6657) y el final (0,1039).",
    "El código imprime exactamente esos valores en la última de las 5 iteraciones muestreadas (idxs incluye len(lc)-1, el índice final).",
    "El valor final del loss, tras las 2000 iteraciones, es 0.1039."
   ],
   "stakes": "Poder leer el valor exacto de loss al final de un entrenamiento (no solo si 'bajó o no') es lo que permite comparar objetivamente distintas configuraciones de un modelo real, en vez de solo mirar si el gráfico 'se ve bien'."
  },
  {
   "question": "La fórmula w ← w − η·(∂L/∂w) se escribe para UN peso genérico w. Este MLP tiene pesos en la capa oculta Y en la capa de salida. ¿A cuáles de esos pesos se les aplica esta fórmula?",
   "type": "mc",
   "options": [
    "A TODOS los pesos de la red, de cada capa — la misma fórmula se aplica peso por peso, usando el gradiente específico de CADA uno calculado por backpropagation",
    "Solo a los pesos de la capa de salida — los de la capa oculta se ajustan con una fórmula distinta",
    "Solo a los pesos de la capa oculta — los de salida se fijan de antemano y no cambian",
    "Solo al peso con el gradiente más grande en cada iteración"
   ],
   "correct": 0,
   "solution": "La fórmula w ← w − η·(∂L/∂w) es GENÉRICA: se aplica a cada peso individual de la red, sin importar en qué capa esté — lo único que cambia de un peso a otro es el valor específico de su gradiente ∂L/∂w, que backpropagation calcula por separado para cada uno. No hay una fórmula distinta para la capa oculta y otra para la de salida: es la misma regla, aplicada peso por peso en toda la red.",
   "whyNot": [
    null,
    "Los pesos de la capa oculta se actualizan con exactamente la misma fórmula, solo que con SU propio gradiente (calculado propagando el error un paso más hacia atrás) — no hay una fórmula separada para cada capa.",
    "Ningún peso de la red queda 'fijo' durante el entrenamiento — tanto los de la capa oculta como los de salida se ajustan en cada iteración, es justamente lo que hace que el loss baje de 0,6657 a 0,1039.",
    "La fórmula se aplica a TODOS los pesos en cada iteración, no solo al de gradiente más grande — cada peso recibe su propio ajuste proporcional a su propio gradiente, por pequeño que sea."
   ],
   "steps": [
    "La fórmula w ← w − η·(∂L/∂w) no menciona ninguna capa específica — es una regla general para 'un peso w cualquiera'.",
    "Backpropagation calcula ∂L/∂w para CADA peso de la red, capa por capa, yendo hacia atrás desde la salida.",
    "Una vez calculado ese gradiente específico, la MISMA fórmula de actualización se aplica a ese peso, sin importar si está en la capa oculta o en la de salida."
   ],
   "stakes": "Esta uniformidad (una sola regla de actualización para todos los pesos, con gradientes distintos) es lo que hace que el mismo mecanismo escale sin cambios a redes con muchísimas más capas y pesos — no hace falta una fórmula nueva por cada capa que se agregue."
  }
 ],
 [
  {
   "question": "Sin backpropagation (es decir, sin una forma eficiente de calcular el gradiente de cada peso), ¿por qué sería prácticamente imposible entrenar una red con millones de parámetros?",
   "type": "mc",
   "options": [
    "Porque calcular el efecto de cada peso individual en el error final, uno por uno sin aprovechar la regla de la cadena, sería computacionalmente inviable a esa escala",
    "Porque las redes con millones de parámetros no podrían representarse en la memoria de una computadora",
    "Porque backpropagation es la única forma de definir la arquitectura de una red",
    "Porque sin backpropagation no se podrían usar datos numéricos, solo texto"
   ],
   "correct": 0,
   "solution": "Backpropagation reutiliza el cálculo del gradiente de una capa para calcular el de la capa anterior (la regla de la cadena), lo que lo hace eficiente incluso con millones de pesos. Sin ese atajo matemático, calcular el gradiente de cada peso por separado, 'a fuerza bruta', sería tan lento que entrenar redes grandes sería inviable en la práctica — es literalmente lo que hizo posible el deep learning moderno.",
   "whyNot": [
    null,
    "El tamaño en memoria de una red depende de cuántos parámetros tiene y cómo se almacenan, no de si se usa backpropagation para entrenarla — el problema de fondo es de TIEMPO de cómputo del entrenamiento, no de espacio de almacenamiento.",
    "La arquitectura (cuántas capas, cuántas neuronas) se decide ANTES de entrenar, como hiperparámetro de diseño — backpropagation entra después, para ajustar los pesos de esa arquitectura ya definida, no para definirla.",
    "Backpropagation funciona sobre datos numéricos en general (imágenes, audio, texto ya convertido a números) — no tiene ninguna restricción especial que excluya datos numéricos comunes."
   ],
   "steps": [
    "Sin backpropagation, calcular el efecto de UN peso en el error final requeriría rehacer el cálculo completo de la red para ese peso, uno por uno.",
    "Backpropagation reutiliza los cálculos de una capa para obtener el gradiente de la capa anterior (regla de la cadena) — mucho más eficiente.",
    "Con millones de pesos, calcular cada gradiente 'a fuerza bruta' sin ese atajo sería computacionalmente inviable en la práctica.",
    "Por eso backpropagation es lo que hizo posible entrenar redes grandes."
   ],
   "stakes": "Esta eficiencia es literalmente lo que permite entrenar modelos reales como los que reconocen caras en un celular o generan texto — sin backpropagation, esos modelos con millones o miles de millones de parámetros nunca podrían entrenarse en tiempos razonables."
  },
  {
   "question": "La teoría menciona que el MLP llega al 100% de precisión en XOR, 'el mismo problema que una regresión logística no podía resolver ni al 50%'. ¿Por qué fallaría tan claramente una regresión logística en este mismo problema?",
   "type": "mc",
   "options": [
    "Porque una regresión logística es, en el fondo, un modelo LINEAL (como el perceptrón sin capa oculta), y XOR no es linealmente separable",
    "Porque una regresión logística solo puede usarse con datos de texto, no con datos numéricos como X e y",
    "Porque una regresión logística necesita muchos más de 4 ejemplos de entrenamiento para funcionar",
    "Porque una regresión logística no permite usar backpropagation en absoluto"
   ],
   "correct": 0,
   "solution": "Una regresión logística, igual que el perceptrón, traza una única frontera de decisión LINEAL (una recta) entre las clases. Como XOR no es linealmente separable (visto en el tema anterior), ningún modelo puramente lineal — sea perceptrón o regresión logística — puede clasificarlo bien, sin importar cuántos datos o iteraciones use.",
   "whyNot": [
    null,
    "La regresión logística es un modelo de propósito general para datos numéricos (como X e y en este código, columnas de 0s y 1s) — no está limitada a texto; el problema con XOR es la geometría del problema, no el tipo de dato.",
    "XOR con 4 ejemplos ya representa TODOS los casos posibles de 2 entradas binarias — el problema no es de cantidad de datos, es que ningún modelo lineal puede separar esos 4 puntos con una sola frontera recta, sin importar cuántas veces se repita el mismo dato.",
    "Backpropagation es el algoritmo para calcular gradientes en redes con capas — una regresión logística SÍ puede entrenarse por descenso del gradiente; el problema de fondo no es ese, es que sigue siendo un modelo lineal."
   ],
   "steps": [
    "Recordá del tema de XOR: ningún modelo que solo pueda trazar una frontera RECTA logra separar bien sus 4 puntos.",
    "Una regresión logística, por dentro, es exactamente ese tipo de modelo: lineal, sin capas ocultas.",
    "Por eso comparte la misma limitación estructural que el perceptrón simple frente a XOR — no es un problema de datos ni de tiempo de entrenamiento, es de la forma del modelo."
   ],
   "stakes": "Reconocer que la regresión logística (muy usada como baseline en proyectos reales) es fundamentalmente lineal ayuda a anticipar cuándo NO va a alcanzar, antes de perder tiempo ajustándola sobre un problema que necesita una frontera no lineal."
  },
  {
   "question": "Esta red tiene 2 entradas, una capa oculta de 4 neuronas, y 1 salida. Contando pesos Y sesgos, ¿cuántos parámetros entrenables tiene en total? (2 entradas×4 neuronas + 4 sesgos de la capa oculta, más 4×1 + 1 sesgo de la capa de salida)",
   "type": "numeric",
   "correct": 17,
   "decimals": 0,
   "solution": "Capa oculta: cada una de las 4 neuronas recibe las 2 entradas, así que hacen falta 2×4=8 pesos, más 1 sesgo POR neurona = 4 sesgos → 12 parámetros. Capa de salida: 1 neurona que recibe las 4 salidas de la capa oculta, así que 4×1=4 pesos, más 1 sesgo de esa neurona → 5 parámetros. Total: 12 + 5 = 17 parámetros entrenables, cada uno ajustado por backpropagation en cada iteración.",
   "steps": [
    "Capa oculta: 2 entradas conectadas a 4 neuronas = 2×4 = 8 pesos, más 1 sesgo por cada una de las 4 neuronas = 4 sesgos. Subtotal: 12.",
    "Capa de salida: las 4 salidas de la capa oculta conectadas a 1 neurona de salida = 4×1 = 4 pesos, más 1 sesgo de esa neurona. Subtotal: 5.",
    "Total: 12 + 5 = 17 parámetros — todos ajustados por la misma fórmula w ← w − η·(∂L/∂w) en cada iteración de backpropagation."
   ],
   "stakes": "Contar parámetros a mano en una red chica es lo que permite entender, por comparación, por qué una red moderna con millones o miles de millones de parámetros necesita backpropagation (el cálculo eficiente del gradiente) para poder entrenarse en absoluto."
  }
 ],
 [
  {
   "question": "El feature map resultante tiene valor 4 en las columnas 2-3, y 0 en el resto. ¿Qué significa ese patrón?",
   "type": "mc",
   "options": [
    "Que el filtro Sobel detectó exactamente dónde está el borde vertical de la imagen — el valor alto marca la ubicación del patrón que el kernel busca",
    "Que hay un error de cálculo, porque todos los valores deberían ser iguales",
    "Que la imagen original está corrupta en esas columnas",
    "Que el kernel solo funciona en la mitad izquierda de la imagen"
   ],
   "correct": 0,
   "solution": "El kernel Sobel vertical calcula, en cada posición, cuánto cambia el brillo de izquierda a derecha dentro de esa ventana de 3x3. Donde la imagen pasa de oscuro (0) a claro (1) — exactamente en el borde — ese cambio es grande, dando el valor 4. En zonas planas (todo oscuro o todo claro), no hay cambio, y el resultado es 0.",
   "whyNot": [
    null,
    "Los valores NO deberían ser iguales: el propósito mismo del filtro es dar una respuesta distinta según haya o no un borde en esa posición — un mapa todo igual significaría que el filtro no detecta nada, lo opuesto a lo que se busca.",
    "La imagen original (img) es perfectamente válida, construida a propósito con np.zeros y asignación directa — no hay ninguna corrupción, el patrón 0/4 es la respuesta ESPERADA del filtro sobre esa imagen.",
    "El kernel se desliza sobre TODA la imagen por igual (el bucle recorre 'oh' y 'ow' completos) — no hay ninguna restricción que lo limite a la mitad izquierda; los ceros a los costados son porque ahí no hay borde, no porque el filtro no llegó."
   ],
   "steps": [
    "El kernel Sobel vertical mide, en cada ventana de 3x3, cuánto cambia el brillo de izquierda a derecha.",
    "Donde la imagen pasa de oscuro a claro (el borde real), ese cambio es grande — de ahí el valor 4.",
    "En zonas planas (todo oscuro o todo claro), no hay cambio de brillo, y el resultado da 0.",
    "El patrón '4 en columnas 2-3, 0 en el resto' es justamente el filtro marcando dónde está ese borde vertical."
   ],
   "stakes": "Este mismo principio (un filtro pequeño que detecta un patrón local) es la base de cómo un auto autónomo detecta los bordes de un carril, o cómo una app de escaneo detecta el borde de un documento en una foto."
  },
  {
   "question": "Según las líneas 'img = np.zeros((8, 8))' y 'img[:, 4:] = 1.0', ¿cómo queda construida la imagen antes de aplicarle el filtro?",
   "type": "mc",
   "options": [
    "Una imagen 8x8 donde toda la mitad izquierda (columnas 0 a 3) queda en 0 (oscuro) y toda la mitad derecha (columnas 4 a 7) queda en 1 (claro), formando un borde vertical",
    "Una imagen 8x8 completamente en blanco (todo 1.0), sin ningún borde",
    "Una imagen 8x8 donde solo la fila 4 se pone en 1.0, el resto queda en 0",
    "Una imagen de 4x4, la mitad del tamaño indicado por np.zeros((8,8))"
   ],
   "correct": 0,
   "solution": "np.zeros((8,8)) crea una imagen de 8x8 toda en 0 (oscura); luego 'img[:, 4:] = 1.0' selecciona TODAS las filas (':') pero solo las columnas desde la 4 en adelante, y las pone en 1.0 (claro) — el resultado es la mitad izquierda oscura y la mitad derecha clara, con un borde vertical justo entre las columnas 3 y 4.",
   "whyNot": [
    null,
    "np.zeros((8,8)) arranca la imagen entera en 0 (oscuro) — solo la mitad derecha (columnas 4 en adelante) se sobrescribe a 1.0 con la segunda línea; la imagen no queda toda en blanco.",
    "'img[:, 4:]' selecciona COLUMNAS desde la 4 en adelante (el segundo índice, después de la coma, es el de columnas) en TODAS las filas (':') — no selecciona una sola fila.",
    "np.zeros((8, 8)) crea explícitamente una matriz de 8 filas por 8 columnas, no de 4x4 — el propio print del código lo confirma mostrando una imagen de 8 filas."
   ],
   "steps": [
    "np.zeros((8,8)) arranca con una imagen de 8x8, toda en 0.",
    "'img[:, 4:] = 1.0' usa ':' para TODAS las filas, y '4:' para las columnas desde la 4 hasta el final — esa región se pone en 1.0.",
    "El resultado: columnas 0-3 en 0 (oscuro), columnas 4-7 en 1 (claro) — un borde vertical bien marcado exactamente en el medio de la imagen."
   ],
   "stakes": "Saber leer con precisión el slicing de numpy (filas vs columnas, qué rango exacto se modifica) es imprescindible para depurar cualquier bug de procesamiento de imágenes real, donde confundir filas con columnas es un error muy común."
  },
  {
   "question": "La fórmula formal de la convolución es $S(i,j) = \\sum_{m,n} I(i{+}m, j{+}n) \\cdot K(m,n)$. ¿Qué representa exactamente la doble suma $\\sum_{m,n}$?",
   "type": "mc",
   "options": [
    "Suma, para UNA posición (i,j) del feature map, el producto entrada×kernel de CADA celda dentro de la ventana de 3×3 — un único número que resume toda esa ventana",
    "Suma todos los píxeles de la imagen completa, sin importar la posición (i,j)",
    "Cuenta cuántas veces aparece el valor 1 en la imagen original",
    "Suma los índices i y j entre sí para encontrar el centro de la imagen"
   ],
   "correct": 0,
   "solution": "Para cada posición (i,j) del feature map, la doble suma recorre TODAS las combinaciones (m,n) dentro de la ventana del kernel (en este caso, 3×3 = 9 combinaciones), multiplica el píxel de la imagen por el valor del kernel en esa posición relativa, y suma los 9 resultados en UN SOLO número — ese número es el valor que le corresponde a (i,j) en el feature map.",
   "whyNot": [
    null,
    "La suma es LOCAL a la ventana de 3×3 alrededor de (i,j), no global sobre toda la imagen — por eso el feature map tiene un valor DISTINTO en cada posición, reflejando lo que hay alrededor de ESA posición en particular.",
    "La fórmula no cuenta ocurrencias de un valor — multiplica cada píxel por el peso del kernel en esa posición relativa, y sólo después suma esos productos.",
    "i y j son ÍNDICES de posición (fila, columna) del feature map, no valores que se sumen entre sí — la fórmula los usa para ubicar la ventana de la imagen sobre la que se calcula, no los combina aritméticamente."
   ],
   "steps": [
    "Para una posición fija (i,j), (m,n) recorre todas las combinaciones dentro del tamaño del kernel (3×3 aquí).",
    "En cada combinación, se multiplica el píxel de la imagen I(i+m, j+n) por el valor del kernel K(m,n) en esa misma posición relativa.",
    "La suma Σ junta esos 9 productos en un solo número — el resultado que le toca a esa posición (i,j) del feature map.",
    "Repetir esto para cada (i,j) posible es lo que produce el feature map completo."
   ],
   "stakes": "Leer una fórmula con sumatoria como 'una ventana local que se resume en un solo número, repetida en cada posición' es la habilidad que permite entender no solo convolución, sino cualquier operación de filtrado o kernel en procesamiento de señales e imágenes."
  }
 ],
 [
  {
   "question": "La imagen original es de 8x8, pero el feature map resultante es de 6x6 (no 8x8). ¿Por qué se reduce el tamaño?",
   "type": "mc",
   "options": [
    "Porque el kernel de 3x3 no puede centrarse en los píxeles del borde de la imagen sin salirse — la ventana deslizante solo cabe en (8-3+1)=6 posiciones por lado",
    "Porque el código elimina al azar 2 filas y 2 columnas del resultado",
    "Porque la mitad de los píxeles de la imagen se descartan antes de aplicar el filtro",
    "Porque max_pooling ya se aplicó antes de calcular el feature map"
   ],
   "correct": 0,
   "solution": "La fórmula del código lo muestra: oh, ow = h-kh+1, w-kw+1 → 8-3+1=6. Con un kernel de 3x3, la ventana deslizante solo tiene 6 posiciones válidas de inicio en cada dimensión (no puede empezar tan cerca del borde que se salga de la imagen) — por eso el resultado siempre es más chico que la imagen original cuando no se agrega padding.",
   "whyNot": [
    null,
    "No hay ningún descarte aleatorio — la reducción de tamaño es una consecuencia matemática exacta y determinística de deslizar un kernel de 3x3 sobre una imagen de 8x8, calculada con la fórmula h-kh+1.",
    "Los 64 píxeles originales de la imagen SÍ se usan (cada uno participa en el cálculo de varias posiciones del feature map) — nada se descarta antes del filtro, la reducción viene de cómo funciona la ventana deslizante, no de eliminar datos de entrada.",
    "El código aplica primero convolucion() (produce el mapa de 6x6) y RECIÉN DESPUÉS max_pooling() sobre ese resultado (que lo reduce más, a 3x3) — son dos pasos separados y en ese orden, no al revés."
   ],
   "steps": [
    "Buscá la fórmula que usa el código: oh, ow = h-kh+1, w-kw+1 → con h=8, kh=3: 8-3+1=6.",
    "Un kernel de 3x3 necesita 3 píxeles de ancho para centrarse — cerca del borde de la imagen, esa ventana se saldría.",
    "Por eso solo hay 6 posiciones válidas de inicio por lado, no 8: el resultado siempre es más chico cuando no hay padding."
   ],
   "stakes": "No tener en cuenta esta reducción de tamaño es una fuente común de bugs de 'shape mismatch' al construir una red convolucional real — el tamaño de la imagen se va achicando capa a capa si no se agrega padding explícitamente."
  },
  {
   "question": "El kernel usado es 'np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])'. ¿Qué patrón tienen en común sus tres filas?",
   "type": "mc",
   "options": [
    "Cada fila tiene un valor negativo a la izquierda, un 0 en el medio, y un valor positivo a la derecha — diseñado para reaccionar a un cambio de brillo de izquierda a derecha",
    "Las tres filas son exactamente iguales entre sí, sin ninguna diferencia",
    "Cada fila suma un total distinto de cero",
    "Todos los valores del kernel son positivos"
   ],
   "correct": 0,
   "solution": "Fijate en cada fila: [-1,0,1], [-2,0,2], [-1,0,1] — todas siguen el mismo patrón negativo-cero-positivo de izquierda a derecha (con la fila del medio con más peso, -2/2). Ese patrón es justamente lo que hace que el filtro reaccione fuerte cuando el brillo cambia de izquierda a derecha (un borde vertical), y dé 0 donde el brillo es uniforme.",
   "whyNot": [
    null,
    "Las filas NO son idénticas: la fila del medio usa -2 y 2 (el doble de peso), mientras que la primera y tercera usan -1 y 1 — esa diferencia de peso es intencional en el diseño del filtro Sobel.",
    "Cada fila individual suma exactamente 0 (-1+0+1=0, -2+0+2=0, -1+0+1=0) — es al revés de lo que dice esta opción; esa suma en cero es justamente lo que hace que el filtro dé 0 en zonas de brillo uniforme.",
    "El kernel tiene tanto valores negativos (-1, -2) como positivos (1, 2) y ceros — no son todos positivos; esa mezcla de signos es lo que le permite detectar la DIRECCIÓN del cambio de brillo, no solo su magnitud."
   ],
   "steps": [
    "Escribí las tres filas una debajo de otra: [-1,0,1], [-2,0,2], [-1,0,1].",
    "En cada una, el patrón es negativo → cero → positivo, de izquierda a derecha.",
    "Al multiplicar ese patrón contra una región de la imagen, el resultado es grande solo cuando el brillo cambia de izquierda a derecha dentro de esa ventana — exactamente lo que se necesita para detectar un borde vertical."
   ],
   "stakes": "Reconocer el patrón dentro de un kernel (qué tipo de cambio detecta) es lo que permite, en un proyecto real de visión por computadora, elegir o diseñar el filtro correcto según el tipo de patrón que se necesita detectar (bordes verticales, horizontales, esquinas, etc.)."
  },
  {
   "question": "Este ejemplo usa UN SOLO kernel (Sobel) para ilustrar la mecánica de la convolución. En una capa convolucional real de una CNN, ¿cuántos kernels suele aplicarse en esa MISMA capa?",
   "type": "mc",
   "options": [
    "Muchos kernels distintos a la vez (decenas o cientos), cada uno aprendiendo a detectar un patrón diferente, generando varios feature maps en paralelo",
    "Exactamente 1, igual que en este ejemplo — usar más de un kernel por capa no está permitido",
    "Un kernel por cada píxel de la imagen de entrada",
    "El mismo kernel Sobel siempre, en todas las CNN, sin excepción"
   ],
   "correct": 0,
   "solution": "Este ejemplo usa un único kernel fijo (Sobel) para que la mecánica quede clara, pero una capa convolucional real aplica MUCHOS kernels en paralelo dentro de la misma capa — cada uno aprendido durante el entrenamiento para detectar un patrón distinto (un tipo de borde, una textura, un color) — produciendo un feature map por cada kernel, todos apilados como la salida de esa capa.",
   "whyNot": [
    null,
    "No hay ningún límite de 1 kernel por capa — es al revés: usar varios kernels en paralelo es la práctica estándar, precisamente para poder detectar varios patrones distintos al mismo tiempo en la misma capa.",
    "Un kernel por píxel eliminaría la ventaja central de la convolución (compartir el mismo filtro chico en toda la imagen) — el número de kernels de una capa es un hiperparámetro de diseño, independiente del tamaño de la imagen.",
    "Sobel es un filtro CLÁSICO, diseñado a mano, usado aquí solo para mostrar la mecánica con claridad — en una CNN real entrenada, los kernels se APRENDEN durante el entrenamiento (como los pesos w de los temas anteriores), no se fijan de antemano."
   ],
   "steps": [
    "Este ejemplo simplifica a propósito usando un único kernel fijo (Sobel), para que se vea con claridad qué hace UNA convolución.",
    "En una CNN real, cada capa convolucional tiene muchos kernels distintos (parámetros que se aprenden con backpropagation, igual que los pesos de una capa densa).",
    "Cada kernel produce su propio feature map — la salida de la capa es la pila de TODOS esos feature maps, uno por kernel, no uno solo."
   ],
   "stakes": "Entender que una capa convolucional real tiene muchos kernels aprendidos (no uno fijo elegido a mano) es la diferencia entre este ejemplo didáctico y cómo funciona de verdad una CNN entrenada para tareas como reconocimiento de imágenes."
  }
 ],
 [
  {
   "question": "¿Qué hace exactamente max_pooling(mapa, 2) con el feature map de 6x6?",
   "type": "mc",
   "options": [
    "Lo divide en bloques de 2x2 y se queda con el valor MÁXIMO de cada bloque, reduciendo el tamaño a 3x3",
    "Calcula el promedio de todos los valores del mapa completo",
    "Aplica un segundo filtro Sobel sobre el resultado del primero",
    "Elimina todos los valores negativos del mapa"
   ],
   "correct": 0,
   "solution": "El código lo hace explícito: recorre el mapa en bloques de tam×tam (2x2) y toma region.max() de cada uno — por eso el mapa de 6x6 (36 valores) se reduce a 3x3 (9 valores), cada uno siendo el máximo de su bloque correspondiente.",
   "whyNot": [
    null,
    "Eso describiría un 'average pooling', una variante distinta — este código usa específicamente region.max(), no un promedio, tal como indica el nombre de la función max_pooling.",
    "El código no vuelve a aplicar ningún kernel — max_pooling es una operación aparte que solo reduce tamaño tomando máximos, no vuelve a convolucionar la imagen.",
    "El pooling no filtra por signo — toma el máximo de cada bloque sin importar si los valores son positivos, negativos o cero (en este ejemplo todos son 0 o 4, pero la operación funcionaría igual con negativos)."
   ],
   "steps": [
    "Fijate qué hace la función con cada bloque: divide el mapa en bloques de 2x2 y toma region.max().",
    "Aplicado a un mapa de 6x6, eso da bloques de 2x2 en una grilla de 3x3 — 9 bloques en total.",
    "De cada bloque se queda solo con el valor MÁXIMO, reduciendo 36 valores a 9: el mapa pasa de 6x6 a 3x3."
   ],
   "stakes": "Max pooling es lo que le permite a un sistema real de reconocimiento de imágenes tolerar que un objeto esté un poco desplazado o rotado en la foto, sin necesitar haberlo visto en esa posición exacta durante el entrenamiento."
  },
  {
   "question": "Además de reducir el tamaño del mapa (de 6x6 a 3x3), la teoría menciona OTRA ventaja del max-pooling. ¿Cuál es?",
   "type": "mc",
   "options": [
    "Hace que la red sea un poco más tolerante a pequeños corrimientos de posición del patrón detectado",
    "Elimina por completo la necesidad de usar capas convolucionales",
    "Convierte automáticamente la imagen a escala de grises",
    "Aumenta la resolución de la imagen original"
   ],
   "correct": 0,
   "solution": "La teoría lo dice explícitamente: el max-pooling 'resume la información conservando lo más importante, y hace que la red sea un poco más tolerante a pequeños corrimientos de posición del patrón' — al quedarse con el valor MÁXIMO de cada bloque, un pequeño desplazamiento del patrón dentro de ese bloque sigue dando el mismo resultado.",
   "whyNot": [
    null,
    "El max-pooling no reemplaza a la convolución — son dos operaciones distintas que se usan JUNTAS en el código (primero convolucion(), después max_pooling() sobre su resultado); pooling no elimina la necesidad de filtros convolucionales.",
    "El pooling trabaja sobre el feature map numérico (resultado de la convolución), no sobre colores de la imagen original — no tiene ninguna relación con convertir a escala de grises.",
    "El pooling hace exactamente lo contrario: REDUCE el tamaño (de 6x6 a 3x3 en este código), no lo aumenta — 'resume' la información, no la expande."
   ],
   "steps": [
    "Ubicá en la teoría la frase sobre max-pooling: menciona reducir tamaño Y 'tolerancia a pequeños corrimientos de posición'.",
    "Esa tolerancia viene de que, al tomar el MÁXIMO de cada bloque de 2x2, un patrón levemente desplazado dentro de ese mismo bloque puede seguir dando el mismo valor máximo.",
    "Por eso el max-pooling aporta algo más que solo 'achicar' el mapa: también hace que pequeños corrimientos del patrón no cambien tanto el resultado."
   ],
   "stakes": "Esta tolerancia a pequeños corrimientos es justamente lo que le permite a un sistema real de reconocimiento facial reconocer la misma cara aunque esté unos píxeles más arriba, abajo o rotada levemente en la foto, sin necesitar haberla visto exactamente en esa posición durante el entrenamiento."
  },
  {
   "question": "La capa convolucional (Sobel) tiene 9 pesos que en una CNN real se APRENDEN entrenando. ¿Y max_pooling(mapa, 2) — tiene también parámetros que se aprenden con backpropagation?",
   "type": "mc",
   "options": [
    "No — max-pooling es una operación FIJA (siempre toma el máximo del bloque), sin ningún peso que ajustar durante el entrenamiento",
    "Sí — max-pooling tiene un peso por cada una de las 4 celdas del bloque de 2x2",
    "Sí, pero solo si la imagen de entrada tiene más de 8x8 píxeles",
    "No se puede saber sin ejecutar el entrenamiento completo de la red"
   ],
   "correct": 0,
   "solution": "max_pooling no tiene ningún parámetro entrenable — 'quedarse con el máximo de cada bloque' es una regla fija, la misma antes y después de cualquier entrenamiento. A diferencia del kernel convolucional (que SÍ tiene pesos que backpropagation ajusta), pooling es puramente una operación de reducción, sin nada que aprender.",
   "whyNot": [
    null,
    "Pooling no pondera las 4 celdas del bloque con ningún peso — simplemente compara sus 4 valores y elige el mayor; no hay ninguna multiplicación por parámetros ajustables de por medio.",
    "El tamaño de la imagen de entrada no cambia esta propiedad — max-pooling es una operación fija sin importar si la imagen es de 8x8 o de 800x800, nunca tiene pesos entrenables.",
    "Es una propiedad estructural de la operación, conocida sin necesidad de entrenar nada: max() no tiene ningún parámetro numérico que backpropagation pudiera ajustar, a diferencia de un kernel convolucional."
   ],
   "steps": [
    "Compará las dos operaciones: la convolución multiplica la imagen por un kernel de VALORES ajustables (pesos).",
    "max_pooling, en cambio, solo compara números y se queda con el mayor — no hay ningún valor numérico de por medio que se pueda 'aprender'.",
    "Por eso, al contar los parámetros entrenables de una CNN, las capas de pooling NO suman ningún parámetro nuevo — solo las capas convolucionales y densas lo hacen."
   ],
   "stakes": "Saber qué capas SÍ tienen parámetros entrenables (convolucionales, densas) y cuáles NO (pooling, y activaciones como ReLU) es necesario para calcular correctamente el tamaño total de una red real y entender qué es lo que realmente ajusta el entrenamiento."
  }
 ],
 [
  {
   "question": "¿Por qué una capa convolucional necesita MUCHAS menos conexiones/pesos que una capa densa para procesar la misma imagen?",
   "type": "mc",
   "options": [
    "Porque el MISMO kernel chico (por ejemplo, 3x3=9 pesos) se reutiliza deslizándose sobre toda la imagen, en vez de tener una conexión independiente por cada píxel como en una capa densa",
    "Porque las capas convolucionales solo procesan la mitad de los píxeles de la imagen",
    "Porque las capas convolucionales no necesitan ningún peso, solo copian los píxeles",
    "Porque las imágenes se comprimen a la mitad de su tamaño antes de entrar a la capa"
   ],
   "correct": 0,
   "solution": "La clave es la REUTILIZACIÓN del mismo filtro: un kernel de 3x3 tiene solo 9 pesos, y esos MISMOS 9 pesos se usan en cada una de las posiciones donde se desliza sobre la imagen — una capa densa, en cambio, necesitaría un peso DISTINTO para cada píxel de entrada por cada neurona, multiplicando enormemente la cantidad de parámetros.",
   "whyNot": [
    null,
    "El kernel recorre TODA la imagen, píxel por píxel en cada posición posible (visto en el código: los bucles 'for i in range(oh)' y 'for j in range(ow)' cubren toda la extensión) — no se salta la mitad de los datos.",
    "El kernel (9 valores Sobel en este ejemplo) SÍ son pesos reales, multiplicados contra la imagen en cada posición (region * kernel) — la convolución no es una simple copia, es un cálculo real con esos pesos.",
    "La imagen de entrada (8x8) no se comprime antes de la convolución — la REDUCCIÓN de tamaño (a 6x6 y luego 3x3) es un resultado de aplicar la convolución y el pooling, no un paso previo de compresión."
   ],
   "steps": [
    "Un kernel de 3x3 tiene 9 pesos — y esos MISMOS 9 pesos se reutilizan en cada posición donde se desliza sobre la imagen.",
    "Una capa densa, en cambio, necesitaría una conexión (peso) DISTINTA para cada píxel de entrada, por cada neurona de salida.",
    "Esa reutilización del mismo filtro chico es lo que reduce drásticamente la cantidad de parámetros de una capa convolucional."
   ],
   "stakes": "Esta reducción de parámetros es la razón práctica por la que se pueden entrenar redes que procesan imágenes de alta resolución en una computadora normal — con capas densas, el mismo modelo necesitaría muchísima más memoria y datos."
  },
  {
   "question": "Según el texto de aplicación, ¿qué diferencia hay entre lo que aprenden las PRIMERAS capas de una CNN y lo que aprenden las capas MÁS PROFUNDAS?",
   "type": "mc",
   "options": [
    "Las primeras capas aprenden filtros simples como bordes (similares al Sobel de este ejemplo); las capas más profundas combinan esos bordes en formas, y las más profundas todavía, en objetos completos",
    "Las primeras capas aprenden objetos completos; las capas profundas aprenden bordes simples",
    "Todas las capas de una CNN aprenden exactamente el mismo tipo de filtro, sin ninguna diferencia entre ellas",
    "Las primeras capas solo procesan sonido, y las capas profundas solo procesan imágenes"
   ],
   "correct": 0,
   "solution": "El texto de aplicación lo describe como una jerarquía: primero bordes simples (como el filtro Sobel de este ejercicio), después esos bordes se combinan en formas más complejas, y en las capas más profundas todavía, esas formas se combinan en objetos reconocibles completos.",
   "whyNot": [
    null,
    "Es al revés de lo que dice el texto: son las primeras capas las que aprenden los patrones MÁS simples (bordes); la complejidad (formas, objetos) aparece recién en las capas más profundas, no en las primeras.",
    "El texto describe explícitamente una progresión de complejidad creciente entre capas (bordes → formas → objetos) — no dice que todas las capas aprendan lo mismo, todo lo contrario, esa jerarquía es el punto central del párrafo.",
    "El texto de aplicación habla de visión por computadora en todos sus ejemplos (reconocimiento facial, autos autónomos, imágenes médicas) — no hay ninguna mención a procesamiento de sonido en este párrafo."
   ],
   "steps": [
    "Ubicá en el texto de aplicación la frase sobre 'primeras capas' vs 'capas más profundas'.",
    "Las primeras aprenden lo más simple: filtros de bordes, como el Sobel usado en este mismo ejemplo.",
    "Las capas siguientes combinan esos bordes en formas, y las más profundas combinan esas formas en objetos completos.",
    "Esa progresión (simple → complejo) es la jerarquía típica de cómo una CNN 've' una imagen, capa por capa."
   ],
   "stakes": "Entender esta jerarquía es clave para interpretar (o depurar) un modelo real de visión: si algo falla, suele ser más fácil primero revisar si las capas tempranas están detectando bien los bordes básicos, antes de sospechar de las capas profundas que combinan patrones más complejos."
  },
  {
   "question": "La fórmula del código para el tamaño del feature map es oh = h - kh + 1 (8 - 3 + 1 = 6), sin ningún otro término. ¿Qué indica la AUSENCIA de un divisor o de un salto en esa fórmula, sobre cómo se mueve el kernel?",
   "type": "mc",
   "options": [
    "Que el kernel se desliza de a UN píxel por vez (stride=1) — si saltara de a 2 píxeles, la fórmula necesitaría dividir por ese salto",
    "Que el kernel se mueve de a 3 píxeles por vez, el mismo tamaño que el kernel",
    "Que el kernel salta directamente al final de la imagen sin recorrer posiciones intermedias",
    "La fórmula no tiene ninguna relación con cómo se mueve el kernel, solo con su tamaño"
   ],
   "correct": 0,
   "solution": "oh = h - kh + 1 es la fórmula del tamaño de salida cuando el kernel se desliza de a UN píxel a la vez (stride=1, el valor por defecto en este código) — evalúa TODAS las posiciones posibles, una por una. Si el kernel saltara de a 2 píxeles (stride=2), la fórmula pasaría a ser oh = (h - kh)//stride + 1, con una división de por medio que reduciría aún más el tamaño de salida.",
   "whyNot": [
    null,
    "Un salto de 3 píxeles (igual al tamaño del kernel) daría una fórmula distinta, con división por 3 — la fórmula usada (sin ningún divisor) es específica de stride=1, un salto de a un solo píxel.",
    "El código SÍ recorre todas las posiciones intermedias — genera un feature map completo de 6x6 (36 valores), no un único resultado; 'saltar al final' daría un solo número, no una matriz.",
    "La fórmula del tamaño de salida está directamente determinada por cómo se mueve la ventana del kernel (el stride) — no son dos cosas independientes, la forma exacta de la fórmula (con o sin división) revela el stride usado."
   ],
   "steps": [
    "Compará: con stride=1, cada nueva posición del kernel se prueba corriendo un solo píxel — hay tantas posiciones como h-kh+1.",
    "Si el stride fuera mayor (por ejemplo 2), el kernel se saltaría posiciones, y habría MENOS posiciones válidas — la fórmula necesitaría dividir por ese stride.",
    "Como el código usa oh = h - kh + 1 sin ninguna división, eso confirma que el stride es 1: el kernel evalúa cada posición posible, una por una."
   ],
   "stakes": "El stride es un hiperparámetro real que se ajusta en redes convolucionales para controlar el balance entre resolución del feature map y costo computacional — un stride mayor a 1 procesa más rápido pero pierde detalle espacial, una decisión de diseño explícita en cualquier CNN real."
  }
 ],
 [
  {
   "question": "En el paso 1 del código se apagan 7 de las 8 neuronas y solo la neurona de índice 1 queda activa. ¿Qué hace el código exactamente con las salidas que SÍ quedan activas?",
   "type": "mc",
   "options": [
    "Divide cada salida activa por keep=1-p (0.5 en este caso) para compensar que ese paso tiene muchas menos neuronas aportando señal ('inverted dropout')",
    "Multiplica cada salida activa por p, reduciéndola a la mitad",
    "Deja las salidas activas exactamente iguales a las originales, sin ningún ajuste",
    "Suma las salidas de las neuronas apagadas a la única neurona que quedó activa"
   ],
   "correct": 0,
   "solution": "La línea h_drop = h * mask / keep divide por keep=1-p=0.5, o sea multiplica por 2: por eso la neurona de índice 1 (activación original 1.918) sale como 3.84 en el paso 1. Esa escala compensa que, durante ese paso, hay muchas menos neuronas aportando señal que en inferencia (donde están las 8 activas).",
   "whyNot": [
    null,
    "El código divide por keep (lo que EQUIVALE a multiplicar por 2 cuando p=0.5), no multiplica por p=0.5 — multiplicar por p reduciría la señal a la mitad en vez de compensarla; mirá la línea h_drop = h * mask / keep.",
    "Si no se escalaran, la señal total que llega a la siguiente capa sería mucho más chica durante entrenamiento que en inferencia (con las 8 neuronas activas) — el código sí divide por keep, justamente para evitar ese desajuste.",
    "El código no redistribuye nada entre neuronas: mask pone directamente en 0 las apagadas, y h_drop=h*mask/keep solo escala las que sobreviven, no transfiere valores de las apagadas a ninguna otra."
   ],
   "steps": [
    "La línea clave es h_drop = h * mask / keep, con keep=1-p=0.5 en este caso.",
    "Dividir por 0.5 es lo mismo que multiplicar por 2 — por eso una activación original de 1.918 sale como 3.84.",
    "Esa escala compensa que, en ese paso de entrenamiento, hay muchas menos neuronas activas aportando señal que en inferencia."
   ],
   "stakes": "Un bug real y común al implementar dropout a mano es olvidar esta escala — sin ella, las predicciones en inferencia salen sistemáticamente más grandes o más chicas de lo esperado, un error silencioso difícil de detectar."
  },
  {
   "question": "El código usa np.random.seed(13) antes de generar x, W y b; luego np.random.seed(1) antes del bucle de 4 pasos de entrenamiento; y np.random.seed(3) antes de la verificación estadística de 2000 pasos. ¿Por qué usar tres semillas DISTINTAS en vez de solo una?",
   "type": "mc",
   "options": [
    "Cada semilla controla un proceso aleatorio distinto y separado (los pesos fijos, las máscaras de los 4 pasos, y las máscaras de la verificación estadística), haciendo que cada parte del código sea reproducible de forma independiente",
    "Porque numpy exige usar una semilla distinta cada vez que se llama a np.random.rand()",
    "Porque cada semilla representa una neurona distinta de la capa oculta",
    "Es un error del código: debería usarse la misma semilla las tres veces"
   ],
   "correct": 0,
   "solution": "Cada llamada a np.random.seed() reinicia el generador aleatorio justo antes de un bloque de código distinto: seed(13) fija los pesos/sesgo/activaciones de la red (que no deben volver a cambiar), seed(1) fija los 4 sorteos de máscaras de dropout que se muestran paso a paso, y seed(3) fija los 2000 sorteos de la verificación estadística — usar semillas distintas para bloques distintos hace que cada parte sea reproducible por separado, sin que un bloque 'contamine' el estado aleatorio del siguiente.",
   "whyNot": [
    null,
    "numpy no exige ninguna semilla distinta entre llamadas a np.random.rand() — de hecho, se podría reutilizar la misma semilla todo el tiempo; usar semillas distintas acá es una decisión de diseño del código, no un requisito técnico.",
    "Las semillas (13, 1, 3) son números que fijan el generador de números aleatorios de numpy, sin relación con la cantidad de neuronas de la capa oculta (que son 8, fijadas por la forma de W y b, no por np.random.seed).",
    "No es un error: cada semilla se usa deliberadamente para una parte distinta del código (pesos fijos, pasos de entrenamiento, verificación estadística) — usar la misma en las tres partes generaría una dependencia no intencionada entre esos tres bloques."
   ],
   "steps": [
    "Contá cuántas veces aparece np.random.seed() en el código, y qué bloque de código sigue a cada llamada.",
    "seed(13) → genera x, W, b (las activaciones fijas de la capa). seed(1) → genera las 4 máscaras de los pasos de entrenamiento mostrados. seed(3) → genera las 2000 máscaras de la verificación estadística.",
    "Cada semilla arranca 'de cero' el generador aleatorio para SU bloque — así, cambiar algo en un bloque no afecta al azar de los otros bloques."
   ],
   "stakes": "Separar semillas por bloque es una práctica real importante al escribir experimentos reproducibles: permite volver a correr solo una parte del experimento (por ejemplo, solo la verificación estadística) sin que el resultado dependa de qué se ejecutó antes en el mismo script."
  },
  {
   "question": "Según la referencia formal (Géron, Cap.11, p.383-385): 'cada neurona (SALVO LAS DE SALIDA) tiene una probabilidad p de ser ignorada'. ¿Qué implica esa excepción sobre las neuronas de la capa de salida?",
   "type": "mc",
   "options": [
    "Las neuronas de salida NUNCA se apagan con Dropout — siempre están activas, tanto en entrenamiento como en inferencia",
    "Las neuronas de salida se apagan con una probabilidad p distinta a las neuronas ocultas",
    "Las neuronas de salida se apagan siempre, en cada paso de entrenamiento",
    "La excepción es un error de la fuente y en la práctica todas las neuronas se tratan igual"
   ],
   "correct": 0,
   "solution": "El texto formal es explícito: 'salvo las de salida' — Dropout apaga neuronas OCULTAS al azar, pero deja intactas siempre las neuronas de la capa de SALIDA, porque son las que producen la predicción final; apagarlas al azar destruiría directamente la salida de la red, no solo la regularizaría.",
   "whyNot": [
    null,
    "El texto no menciona una probabilidad distinta para la salida — directamente las EXCLUYE del mecanismo de apagado, no les aplica ninguna probabilidad de apagarse.",
    "Es lo opuesto: las neuronas de salida son las que NUNCA se apagan, precisamente por ser las que entregan la predicción final de la red en cada paso.",
    "No es un error de la fuente — es una condición necesaria del método: si se apagara al azar la neurona de salida, la red simplemente no tendría predicción en ese paso, algo que rompería el entrenamiento."
   ],
   "steps": [
    "Leé la condición exacta: 'cada neurona (salvo las de salida) tiene una probabilidad p de ser ignorada'.",
    "Esa excepción aplica específicamente a la ÚLTIMA capa de la red, la que produce la predicción.",
    "Apagar esa capa la dejaría sin ninguna salida en ese paso — por eso Dropout se aplica únicamente a las capas OCULTAS, nunca a la de salida."
   ],
   "stakes": "Confundir 'todas las neuronas' con 'todas las neuronas ocultas' es un error común al implementar Dropout desde cero — aplicarlo también a la capa de salida rompería la predicción de la red en cada paso donde le tocara apagarse."
  }
 ],
 [
  {
   "question": "En la sección de INFERENCIA, la salida impresa es idéntica a la primera línea del código (activaciones sin dropout, sin escalar). ¿Por qué?",
   "type": "mc",
   "options": [
    "Porque después de entrenar, dropout se desactiva por completo: se usan TODAS las neuronas, con sus activaciones originales, sin apagar ni escalar nada",
    "Porque el código tiene un error y tampoco aplicó dropout durante el entrenamiento",
    "Porque en inferencia también se apagan neuronas al azar, pero esta vez el sorteo no apagó ninguna",
    "Porque keep=1-p se vuelve automáticamente 1 durante la inferencia, por eso no cambia nada"
   ],
   "correct": 0,
   "solution": "El entrenamiento SÍ aplicó dropout: se ve en los 4 pasos anteriores, cada uno con neuronas distintas apagadas. La fase de inferencia es la que, a propósito, NO usa dropout — el código simplemente imprime h sin aplicar ninguna mask ni división, por eso coincide exactamente con las activaciones originales.",
   "whyNot": [
    null,
    "El entrenamiento sí aplicó dropout: en el paso 1 se apagan 7 de 8 neuronas, en el paso 2 otras 4 distintas, etc. — el código funciona como se espera, es la fase de inferencia la que deliberadamente omite dropout, no un error.",
    "La inferencia no vuelve a tirar ningún dado: el código simplemente imprime h sin aplicar mask ni escala, es una decisión fija del algoritmo (dropout apagado), no un resultado al azar que 'coincidió' en no apagar nada.",
    "keep=1-p sigue valiendo 0.5 en todo el código, ese valor nunca cambia — lo que cambia en inferencia es que simplemente no se usa mask ni se divide por keep, se imprimen las activaciones originales de h tal cual."
   ],
   "steps": [
    "Compará: en los pasos de entrenamiento, cada uno apaga neuronas DISTINTAS y escala el resultado.",
    "En inferencia, el código no aplica ninguna mask ni división — usa h directamente, con TODAS las neuronas activas.",
    "Por eso la salida de inferencia coincide exactamente con las activaciones originales, sin dropout: es el comportamiento esperado después de entrenar."
   ],
   "stakes": "Dejar dropout activado por accidente durante la inferencia de un modelo real (en vez de solo en entrenamiento) hace que las predicciones cambien cada vez que se corren, aunque la entrada sea idéntica — un bug clásico de frameworks mal configurados."
  },
  {
   "question": "¿Qué calcula exactamente la línea 'h = np.maximum(0, x @ W + b)'?",
   "type": "mc",
   "options": [
    "El forward pass de la capa oculta: multiplica la entrada x por los pesos W, suma el sesgo b, y aplica ReLU (recorta a 0 cualquier valor negativo)",
    "El dropout de la capa oculta, apagando al azar la mitad de las neuronas",
    "El error (loss) entre la predicción de la red y el valor esperado",
    "La tasa de aprendizaje que se va a usar en el resto del código"
   ],
   "correct": 0,
   "solution": "'x @ W + b' es la suma ponderada de la capa (entrada por pesos, más sesgo) — el mismo cálculo visto en la neurona artificial del primer tema, pero ahora para 8 neuronas a la vez. np.maximum(0, ...) es la función ReLU: deja pasar los valores positivos tal cual, y convierte cualquier negativo en 0. El resultado, h, son las activaciones de la capa oculta ANTES de aplicar dropout.",
   "whyNot": [
    null,
    "El dropout aparece recién DESPUÉS, en el bucle 'for paso in range(1,5)' con la variable mask — la línea de h es un paso previo y separado: calcula las activaciones limpias de la capa, sin apagar ninguna neurona todavía.",
    "Esta línea no compara nada con un valor esperado — solo hace un cálculo hacia adelante (forward) a partir de x, W y b; no hay ningún 'error' o 'loss' involucrado en esta parte del código.",
    "La tasa de aprendizaje no aparece en ningún lugar de este código de dropout — esta línea calcula activaciones de una capa oculta, no ajusta ningún hiperparámetro de entrenamiento."
   ],
   "steps": [
    "Separá la expresión: 'x @ W + b' es una multiplicación de matrices (entrada por pesos) más un sesgo — la suma ponderada de la capa.",
    "np.maximum(0, ...) compara cada valor con 0 y se queda con el mayor — eso es exactamente la función ReLU.",
    "El resultado, h, son las 8 activaciones de la capa oculta, calculadas ANTES de que dropout entre en juego."
   ],
   "stakes": "Reconocer esta línea como 'forward pass + ReLU' es la base para leer el código de cualquier framework de deep learning real (PyTorch, TensorFlow) por dentro, donde esta misma operación se repite en cada capa de la red."
  },
  {
   "question": "Con 8 neuronas en la capa oculta y p=0.5, ¿cuántas neuronas se espera que queden ACTIVAS, EN PROMEDIO, en cada paso de entrenamiento?",
   "type": "numeric",
   "correct": 4,
   "decimals": 0,
   "solution": "Si cada neurona tiene probabilidad p=0.5 de APAGARSE, la probabilidad de quedar ACTIVA es 1-p=0.5 — sobre 8 neuronas, el número esperado de activas es 8×(1-p) = 8×0.5 = 4. Es un promedio: en un paso concreto podrían quedar activas 3, 5, o cualquier otro número (como el paso 1 del código, donde solo queda activa 1 neurona), pero repitiendo muchas veces el sorteo, el promedio converge a 4.",
   "steps": [
    "La probabilidad de que UNA neurona quede activa es 1-p = 1-0.5 = 0.5.",
    "Con 8 neuronas independientes, el número esperado de activas es 8 × 0.5 = 4.",
    "Ese es un promedio estadístico — el paso 1 del código, por ejemplo, dejó activa solo 1 neurona (un resultado válido pero por debajo del promedio, dentro de la variación normal del azar)."
   ],
   "stakes": "Calcular el número esperado de neuronas activas es lo que permite anticipar, antes de entrenar, cuánta capacidad efectiva le queda a una capa con Dropout — importante para no configurar un p tan alto que la red se quede prácticamente sin señal en cada paso."
  }
 ],
 [
  {
   "question": "Tras repetir el sorteo de dropout 2000 veces, la fracción promedio de apagados da 0.504. ¿Qué confirma ese número?",
   "type": "mc",
   "options": [
    "Que el mecanismo de apagado es realmente aleatorio, con una probabilidad muy cercana al p=0.5 configurado, no un patrón fijo",
    "Que el código tiene un error, porque debería dar exactamente 0.5 y no 0.504",
    "Que dropout apaga en promedio la mitad de las neuronas EN INFERENCIA también",
    "Que después de 2000 pasos, las neuronas dejan de apagarse"
   ],
   "correct": 0,
   "solution": "0.504 confirma que np.random.rand(...) > p realmente sortea con probabilidad cercana a p=0.5 en cada paso independiente — al ser un proceso aleatorio, el promedio empírico ronda el valor teórico sin caer exactamente en él (con más de 2000 pasos se acercaría todavía más a 0.500).",
   "whyNot": [
    null,
    "0.504 no es un error: al ser un proceso aleatorio, el promedio empírico SIEMPRE va a rondar el valor teórico sin caer exactamente en él, por variación estadística normal — es la señal de que el sorteo funciona bien, no de que falla.",
    "Ese bloque estadístico simula pasos de ENTRENAMIENTO (mismo mecanismo que los 4 pasos anteriores) — en inferencia, como se vio antes, dropout está desactivado y la fracción de apagados ahí es 0, no 0.5.",
    "No hay ninguna relación entre la CANTIDAD de pasos y que las neuronas 'dejen' de apagarse — mientras se siga entrenando con dropout activo, cada paso vuelve a sortear su propia máscara desde cero, sin memoria de los pasos anteriores."
   ],
   "steps": [
    "El sorteo es np.random.rand(...) > p, con p=0.5 — cada neurona se apaga con esa probabilidad, de forma independiente en cada paso.",
    "Repetido 2000 veces, el promedio empírico (0.504) debería acercarse al valor teórico (0.5), pero no caer exactamente en él, por ser aleatorio.",
    "Ese resultado — cerca de 0.5 pero no exacto — es la firma esperada de un proceso realmente al azar, no de un patrón fijo ni de un error de código."
   ],
   "stakes": "Verificar que un mecanismo aleatorio se comporta según lo esperado (cerca de p, no exacto) es una práctica real de testing en machine learning — un valor sospechosamente exacto, como 0.5 justo, sería más señal de un bug que de buena suerte."
  },
  {
   "question": "El comentario del código dice que masks_stat se genera '(vectorizado, sin bucle Python largo)'. ¿Qué logra el código al construir masks_stat como una matriz de una sola vez, en vez de con un bucle for de 2000 iteraciones?",
   "type": "mc",
   "options": [
    "Genera los 2000 sorteos de dropout en una sola operación de numpy, mucho más rápida que repetir 2000 veces un bucle de Python",
    "Evita que dropout se aplique más de una vez a la misma neurona",
    "Reduce la probabilidad p de apagado de 0.5 a un valor menor",
    "Hace que los 2000 pasos usen exactamente la misma máscara, en vez de máscaras distintas"
   ],
   "correct": 0,
   "solution": "'np.random.rand(n_pasos, len(h))' genera de una sola vez una matriz de 2000x8 números aleatorios — todo el trabajo lo hace numpy internamente, en código optimizado, en vez de que Python ejecute 2000 vueltas de un bucle for uno por uno. El comentario lo aclara explícitamente: es una elección de eficiencia.",
   "whyNot": [
    null,
    "'Vectorizado' no tiene relación con cuántas veces se aplica dropout a una neurona — se refiere únicamente a CÓMO se genera el número aleatorio (de una vez con numpy, en vez de con un bucle Python), no a la lógica del dropout en sí.",
    "p sigue valiendo 0.5 en todo el código — construir masks_stat de forma vectorizada no cambia ningún valor de probabilidad, solo cambia CÓMO se calculan los 2000 sorteos.",
    "Cada una de las 2000 filas de masks_stat es un sorteo INDEPENDIENTE (por eso 'frac_apagada' varía un poco entre neuronas) — vectorizar no significa repetir la misma máscara, significa generar todas las máscaras distintas de una sola vez, de forma eficiente."
   ],
   "steps": [
    "Leé el comentario: dice explícitamente 'vectorizado, sin bucle Python largo'.",
    "'np.random.rand(n_pasos, len(h))' genera TODA la matriz de 2000x8 números de una vez, usando código optimizado de numpy (escrito en C internamente).",
    "La alternativa (un bucle for de 2000 iteraciones en Python puro) sería mucho más lenta para la misma cantidad de números aleatorios.",
    "Por eso el código elige la versión vectorizada: mismo resultado, pero mucho más rápido de calcular."
   ],
   "stakes": "Preferir operaciones vectorizadas de numpy en vez de bucles largos de Python es una práctica estándar en cualquier proyecto real de ciencia de datos, porque la diferencia de velocidad entre ambas puede ser de cientos de veces con conjuntos de datos grandes."
  },
  {
   "question": "El paso 1 apaga 7 de 8 neuronas; el paso 2 apaga otras 4 totalmente distintas. ¿Qué pasaría si, en cambio, se usara la MISMA máscara fija en los 4 pasos de entrenamiento?",
   "type": "mc",
   "options": [
    "Sería equivalente a entrenar una red permanentemente más chica (con esas neuronas fijas eliminadas) — se perdería el efecto de Dropout de evitar que las neuronas se co-adapten entre sí",
    "El resultado sería exactamente igual a usar máscaras distintas cada vez",
    "El código no podría ejecutarse con una máscara fija",
    "Solo cambiaría el valor de keep=1-p, nada más"
   ],
   "correct": 0,
   "solution": "Si la máscara fuera siempre la misma, las neuronas apagadas quedarían eliminadas PERMANENTEMENTE de la red durante todo el entrenamiento — en la práctica, sería idéntico a entrenar una red más chica desde el principio, no una técnica de regularización. La clave de Dropout es justamente RESORTEAR qué neuronas se apagan en CADA paso, para que ninguna neurona pueda depender siempre de las mismas compañeras.",
   "whyNot": [
    null,
    "No sería equivalente — con máscaras distintas, cada neurona pasa por muchas combinaciones diferentes de compañeras activas a lo largo del entrenamiento; con una máscara fija, siempre las mismas neuronas faltan, sin esa variedad.",
    "El código funcionaría igual de bien técnicamente con una máscara fija (no hay ningún error de ejecución) — el problema sería conceptual: dejaría de cumplir el propósito regularizador de Dropout.",
    "keep=1-p seguiría siendo 0.5 en ambos casos — lo que cambiaría no es ese valor, sino la VARIEDAD de neuronas apagadas a lo largo del entrenamiento."
   ],
   "steps": [
    "Compará los pasos 1 y 2 del código: cada uno apaga un conjunto DISTINTO de neuronas, no el mismo.",
    "Si la máscara fuera fija, esas neuronas apagadas simplemente dejarían de existir para toda la red — como entrenar una arquitectura más chica de entrada.",
    "El propósito de Dropout es justamente lo contrario: variar qué neuronas faltan en cada paso, para que ninguna se vuelva indispensable."
   ],
   "stakes": "Este es un error de implementación real y común: aplicar una única máscara de Dropout 'congelada' en vez de resortearla en cada paso, lo que anula silenciosamente el efecto regularizador sin que el código arroje ningún error visible."
  }
 ],
 [
  {
   "question": "Según el mecanismo de Dropout, ¿por qué forzar a que distintas neuronas se apaguen en cada paso mejora la capacidad de la red de generalizar a datos nuevos (evita que memorice)?",
   "type": "mc",
   "options": [
    "Porque ninguna neurona puede depender de que otra neurona específica esté siempre presente, así que cada una debe aprender a ser útil por sí misma en vez de sobre-especializarse junto a unas pocas vecinas",
    "Porque dropout reduce la cantidad de datos de entrenamiento que la red ve",
    "Porque dropout aumenta artificialmente el número de neuronas de la red",
    "Porque dropout reemplaza la función de activación ReLU por una más simple"
   ],
   "correct": 0,
   "solution": "Al apagarse al azar en cada paso, ninguna neurona puede 'co-adaptarse' dependiendo de que otra neurona puntual esté siempre disponible — cada una tiene que volverse útil por su cuenta, prestando atención a más entradas en vez de sobre-especializarse. El resultado es una red menos sensible a pequeños cambios y más robusta, que generaliza mejor.",
   "whyNot": [
    null,
    "Dropout no toca los DATOS de entrenamiento en absoluto — x, W y b siguen siendo los mismos en todos los pasos del código; lo único que cambia es qué neuronas de la capa oculta participan en cada paso.",
    "El código no agrega neuronas: la capa oculta sigue teniendo exactamente 8 neuronas en los 5 casos mostrados (4 pasos de entrenamiento + inferencia) — dropout apaga neuronas EXISTENTES, no crea nuevas.",
    "ReLU (np.maximum(0, ...)) se aplica una sola vez, antes de que exista cualquier noción de dropout, y no cambia en ningún momento del código — dropout actúa DESPUÉS, sobre activaciones que ya pasaron por ReLU."
   ],
   "steps": [
    "Si una neurona pudiera depender siempre de que otra esté presente, se 'co-adaptarían' — aprenderían juntas en vez de cada una aportar algo útil por separado.",
    "Al apagarse al azar en cada paso, ninguna neurona puede confiar en que una vecina específica siempre esté ahí.",
    "Eso obliga a cada neurona a volverse útil por su cuenta, prestando atención a más señales en vez de sobre-especializarse.",
    "El resultado es una red menos sensible a detalles puntuales del set de entrenamiento — generaliza mejor a datos nuevos."
   ],
   "stakes": "Este es el motivo concreto por el que dropout se volvió estándar en redes reales de producción: modelos sin él memorizan detalles del set de entrenamiento y rinden peor con datos nuevos, un problema costoso de detectar recién en producción."
  },
  {
   "question": "Según el texto de aplicación, redes ya en el estado del arte ganaron entre 1 y 2 puntos de accuracy al agregar dropout. En un modelo con 95% de precisión, ¿qué representa aproximadamente esa ganancia en términos de la TASA DE ERROR?",
   "type": "mc",
   "options": [
    "Una reducción de casi el 40% en la tasa de error (de 5% de error a aproximadamente 3%)",
    "Una reducción del 1% en la tasa de error, exactamente igual a la ganancia de accuracy",
    "Un aumento de la tasa de error, porque dropout introduce ruido en las predicciones",
    "No hay ninguna relación entre la ganancia de accuracy y la tasa de error"
   ],
   "correct": 0,
   "solution": "El texto lo calcula explícitamente: un modelo con 95% de precisión tiene 5% de error; ganar 1-2 puntos de accuracy (llegando a ~96-97%) baja el error a aproximadamente 3% — una reducción de casi el 40% de la tasa de error ORIGINAL, aunque la ganancia en accuracy parezca chica en términos absolutos (1-2 puntos).",
   "whyNot": [
    null,
    "La reducción NO es igual en puntos porcentuales absolutos: 1-2 puntos de accuracy ganada representa una porción mucho más grande del error ORIGINAL (5%), porque el error de partida ya era chico — de ahí que sea 'casi 40%' y no solo '1-2%'.",
    "El propio texto de aplicación describe esto como un resultado POSITIVO y consistente ('el resultado empírico fue contundente') — dropout reduce el error, no lo aumenta, según lo que describe el párrafo.",
    "El texto sí establece una relación matemática directa: accuracy y tasa de error son complementarios (accuracy + error = 100%), así que cualquier ganancia en uno se refleja directamente como una reducción en el otro."
   ],
   "steps": [
    "Un modelo con 95% de precisión tiene, por definición, 5% de tasa de error (100% - 95%).",
    "Ganar 1-2 puntos de accuracy lo lleva a ~96-97% de precisión, o sea ~3-4% de error.",
    "Comparado con el error ORIGINAL (5%), bajar a ~3% es una reducción de casi el 40% de ESE error — aunque en accuracy 'solo' se ganaron 1-2 puntos.",
    "Por eso el texto aclara esta distinción: una ganancia chica en accuracy puede ser una reducción grande en términos relativos de error."
   ],
   "stakes": "Distinguir entre 'puntos de accuracy ganados' y 'porcentaje de error reducido' es clave al evaluar mejoras reales en un modelo de producción — un cambio que parece chico en accuracy absoluta puede representar una mejora mucho más significativa vista en términos de errores evitados."
  },
  {
   "question": "El código calcula h = np.maximum(0, x @ W + b) UNA SOLA VEZ, y recién DESPUÉS aplica una máscara de dropout distinta en cada uno de los 4 pasos. ¿Por qué no se recalcula h desde cero en cada paso?",
   "type": "mc",
   "options": [
    "Porque en este ejemplo x, W y b son fijos (misma entrada, mismos pesos) — h representa 'las activaciones antes de dropout', y lo único que cambia paso a paso es QUÉ neuronas de esas mismas activaciones se apagan",
    "Porque recalcular h en cada paso daría un resultado distinto cada vez, haciendo el ejemplo imposible de seguir",
    "Porque h ya incluye el efecto de dropout, así que aplicar la máscara después sería repetir el mismo paso dos veces",
    "Es un error del código: h debería recalcularse en cada uno de los 4 pasos"
   ],
   "correct": 0,
   "solution": "El orden importa: primero se calcula el forward pass completo (x @ W + b, más ReLU) UNA sola vez, dando las activaciones h 'completas' de las 8 neuronas. Dropout se aplica DESPUÉS, sobre esas mismas h, y es ahí donde entra la variación entre pasos: cada paso sortea una máscara distinta sobre el MISMO h, no recalcula las activaciones desde cero.",
   "whyNot": [
    null,
    "Con x, W y b fijos en este ejemplo, recalcular h daría exactamente EL MISMO resultado cada vez (no hay ningún componente aleatorio en x @ W + b) — la variación entre pasos viene únicamente de la máscara de dropout, no de recalcular h.",
    "h, tal como se calcula en esa línea, NO incluye dropout todavía — es antes de la máscara; dropout se aplica en un paso posterior y separado (h_drop = h * mask / keep), no está mezclado en el cálculo de h.",
    "No es un error — es precisamente el diseño correcto: separar 'calcular las activaciones' (una vez) de 'decidir cuáles se apagan' (en cada paso) es lo que deja ver con claridad que dropout actúa sobre las MISMAS activaciones, solo cambiando la máscara."
   ],
   "steps": [
    "h = np.maximum(0, x @ W + b) es el forward pass normal de la capa — se calcula una vez, a partir de x, W y b (todos fijos en este ejemplo).",
    "Dropout entra DESPUÉS, como un paso separado: aplica una máscara distinta sobre ese mismo h en cada uno de los 4 pasos de entrenamiento.",
    "Por eso el código no necesita recalcular h cada vez — lo que varía paso a paso es la máscara, no las activaciones de base."
   ],
   "stakes": "Entender que Dropout es un paso SEPARADO después del forward pass (no parte del cálculo de activaciones) es la base para poder ubicar exactamente dónde insertar una capa de Dropout en un framework real como Keras o PyTorch."
  }
 ]
];

/* ──────────── Modo Maestro RN (Redes Neuronales y Deep Learning) ────────────
   Mismo patrón exacto que master-as.js (ver ese archivo para el diseño
   original): progreso propio en localStorage, reutiliza runCode()/panel de
   pasos (el código sigue siendo Python), teoría + Visualízalo + Aplicación
   real + quiz con whyNot completo + confianza + razonamiento + Leitner. */
const MASTER_RN_KEY='pyvizMasterRnProgressV1';
let _rnOn=false, _rnPos=0, _rnDone=new Set(), _rnQuizAnswered=false, _rnQuizShuffledCorrect=null, _rnCurrentQuiz=null, _rnQuizSubPos=0, _rnQuizOrder=null;

function _loadRnProgress(){
  try{
    const raw=localStorage.getItem(MASTER_RN_KEY);
    if(raw){ const d=JSON.parse(raw); _rnDone=new Set(d.done||[]); }
  }catch(e){ _rnDone=new Set(); }
}
function _saveRnProgress(){
  try{ localStorage.setItem(MASTER_RN_KEY, JSON.stringify({done:[..._rnDone]})); }catch(e){}
}
function _rnFirstPending(){
  for(let i=0;i<EX_RN.length;i++) if(!_rnDone.has(i)) return i;
  return EX_RN.length-1;
}
function toggleMasterRn(){
  if(_rnOn){ exitMasterRn(); return; }
  if(_masterOn) exitMasterMode();
  if(_aoOn) exitMasterAo();
  if(_mathOn) exitMasterMath();
  if(_raOn) exitMasterRa();
  if(typeof _asOn!=='undefined' && _asOn) exitMasterAs();
  if(typeof _nsOn!=='undefined' && _nsOn && 'rn'!=='ns') exitMasterNs();
  if(typeof _rnOn!=='undefined' && _rnOn && 'rn'!=='rn') exitMasterRn();
  if(typeof _rfOn!=='undefined' && _rfOn && 'rn'!=='rf') exitMasterRf();
  if(_reviewOn) exitReviewMode();
  if(typeof _calOn!=='undefined' && _calOn) _calClose();
  if(typeof _reportOn!=='undefined' && _reportOn) _reportClose();
  if(typeof _sessionOn!=='undefined' && _sessionOn) _sessionClosePanel();
  if(typeof _errorsOn!=='undefined' && _errorsOn) _errorsClose();
  if(typeof _examOn!=='undefined' && _examOn) _examClose();
  _rnOn=true;
  _loadRnProgress();
  document.getElementById('masterRnBar').style.display='flex';
  const b=document.getElementById('bMasterRn');
  if(b){ b.textContent='🕸️ Modo Maestro RN (activo)'; b.classList.add('btn-looping'); }
  autoLayout();
  _rnGoTo(_rnFirstPending());
}
function exitMasterRn(){
  _rnOn=false;
  document.getElementById('masterRnBar').style.display='none';
  document.getElementById('masterRnChecklist').style.display='none';
  const b=document.getElementById('bMasterRn');
  if(b){ b.textContent='🕸️ Modo Maestro RN'; b.classList.remove('btn-looping'); }
  autoLayout();
}
function _rnGoTo(idx){
  _rnPos=Math.max(0, Math.min(EX_RN.length-1, idx));
  _rnQuizSubPos=0;
  document.getElementById('codeInput').value=EX_RN[_rnPos].code;
  renderLineNums();
  document.getElementById('frBody').innerHTML='<div class="ob-ph">No variables yet</div>';
  document.getElementById('obBody').innerHTML='<div class="ob-ph">Click [→] to inspect</div>';
  document.getElementById('outBody').innerHTML='<span class="out-empty">No output yet</span>';
  runCode();
  _rnRenderBar();
  _resetSelfExplain('rn');
  _rnRenderTheory();
  _rnRenderConceptViz();
  _rnRenderApplication();
  _rnRenderCodeAnatomy();
  _rnRenderQuiz();
}
function _rnRenderTheory(){
  const t=EX_RN[_rnPos].theory;
  const block=document.getElementById('rnTheoryBlock');
  if(!t){ block.style.display='none'; return; }
  if(_theoryIsLocked('rn', 'rn', _rnPos)){
    document.getElementById('rnTheoryBody').innerHTML=_theoryGateHtml('rn', _rnPos, '_rnRenderTheory');
    block.style.display='block';
    return;
  }
  document.getElementById('rnTheoryBody').innerHTML=t;
  block.style.display='block';
}
function _rnRenderConceptViz(){
  const viz=EX_RN[_rnPos].viz;
  const block=document.getElementById('rnConceptVizBlock');
  if(!viz){ block.style.display='none'; return; }
  const svg=renderConceptViz(viz);
  if(!svg){ block.style.display='none'; return; }
  document.getElementById('rnConceptVizBody').innerHTML=svg;
  block.style.display='block';
}
function _rnRenderApplication(){
  const a=EX_RN[_rnPos].application;
  const block=document.getElementById('rnApplicationBlock');
  if(!a){ block.style.display='none'; return; }
  document.getElementById('rnApplicationBody').innerHTML=a;
  block.style.display='block';
}
/* Panel "🔬 Anatomía del código" -- ver la cabecera igual en master-ra.js
   para el porqué. Piloto hecho a mano, un tema por modo. */
function _rnRenderCodeAnatomy(){
  const spec=EX_RN[_rnPos].codeAnatomy;
  const block=document.getElementById('rnCodeAnatomyBlock');
  if(!spec){ block.style.display='none'; return; }
  const svg=renderCodeAnatomy(spec);
  if(!svg){ block.style.display='none'; return; }
  document.getElementById('rnCodeAnatomyBody').innerHTML=svg;
  block.style.display='block';
}
function _rnRenderQuiz(){
  const bank=RN_QUIZ[_rnPos];
  const q=bank[_rnQuizSubPos];
  _rnCurrentQuiz=q;
  _rnQuizAnswered=false;
  document.getElementById('rnQuizProgress').textContent=
    bank.length>1 ? `(pregunta ${_rnQuizSubPos+1}/${bank.length} de este tema)` : '';
  document.getElementById('rnQuizNextBtn').style.display='none';
  document.getElementById('rnQuizQuestion').innerHTML=q.question;
  const optWrap=document.getElementById('rnQuizOptions');
  const numWrap=document.getElementById('rnQuizNumericWrap');
  if(q.type==='mc'){
    numWrap.style.display='none';
    const res=_quizRenderAnswerArea('rn', 'rn', _rnPos, q);
    _rnQuizShuffledCorrect=res.shuffled?res.shuffled.correct:null;
    _rnQuizOrder=res.shuffled?res.shuffled.order:null;
  } else {
    optWrap.style.display='none';
    numWrap.style.display='flex';
    const inp=document.getElementById('rnQuizNumericInput');
    inp.value=''; inp.disabled=false;
    _rnQuizShuffledCorrect=null;
    _rnQuizOrder=null;
  }
  document.getElementById('rnQuizFeedback').style.display='none';
  document.getElementById('rnQuizSolutionBtn').style.display='none';
  const solBody=document.getElementById('rnQuizSolutionBody');
  solBody.style.display='none'; solBody.innerHTML='';
  _quizResetExtras('rn');
}
function _rnCheckQuizAnswer(selectedIdx){
  if(_rnQuizAnswered) return;
  const q=_rnCurrentQuiz;
  let ok=false;
  if(q.type==='mc'){
    ok = selectedIdx===_rnQuizShuffledCorrect;
    document.querySelectorAll('#rnQuizOptions .math-option').forEach((btn,i)=>{
      btn.classList.remove('math-option-correct','math-option-wrong');
      if(ok){
        btn.disabled=true;
        if(i===_rnQuizShuffledCorrect) btn.classList.add('math-option-correct');
      } else if(i===selectedIdx){
        btn.classList.add('math-option-wrong');
      }
    });
  } else {
    const inp=document.getElementById('rnQuizNumericInput');
    const val=parseFloat(inp.value.trim().replace(',','.'));
    const dec=q.decimals||0;
    const pw=Math.pow(10,dec);
    ok = !isNaN(val) && Math.round(val*pw)===Math.round(q.correct*pw);
    inp.disabled=ok;
  }
  if(ok) _rnQuizAnswered=true;
  _recordAttempt('rn', _rnPos, ok);
  _rnRenderTheory();
  const fb=document.getElementById('rnQuizFeedback');
  fb.style.display='block';
  fb.className='math-feedback '+(ok?'math-feedback-ok':'math-feedback-bad');
  const whyNot = (!ok && q.type==='mc' && q.whyNot && _rnQuizOrder) ? q.whyNot[_rnQuizOrder[selectedIdx]] : null;
  if(whyNot) _logErrorJournal('rn', _rnPos, EX_RN[_rnPos].name, q.question, q.options[_rnQuizOrder[selectedIdx]], q.options[q.correct], whyNot);
  fb.textContent = ok ? '✅ Correcto.' :
    (whyNot ? '❌ '+whyNot+' Puedes intentarlo de nuevo, o revisar la solución.'
            : '❌ Incorrecto — puedes intentarlo de nuevo, o revisar la solución.');
  document.getElementById('rnQuizSolutionBtn').style.display='inline-block';
  if(ok) _quizRenderConfidencePrompt('rn');
  if(q.type==='mc' && _rnQuizOrder){
    const otherOptionTexts=q.options.filter((_,i)=>i!==_rnQuizOrder[selectedIdx]);
    _quizRenderReasonPrompt('rn', otherOptionTexts);
  }
  if(ok && _rnQuizSubPos<RN_QUIZ[_rnPos].length-1)
    document.getElementById('rnQuizNextBtn').style.display='inline-block';
}
function _rnNextQuizQuestion(){
  if(_rnQuizSubPos<RN_QUIZ[_rnPos].length-1){ _rnQuizSubPos++; _rnRenderQuiz(); }
}
function _rnShowQuizSolution(){
  const q=_rnCurrentQuiz;
  const el=document.getElementById('rnQuizSolutionBody');
  el.innerHTML=q.solution+_quizStepsHtml(q)+_quizWhyNotHtml(q, _rnQuizOrder)+_quizStakesHtml(q);
  el.style.display='block';
}
function _rnRenderBar(){
  const ex=EX_RN[_rnPos];
  const pct=Math.round((_rnDone.size/EX_RN.length)*100);
  document.getElementById('masterRnTitle').textContent=
    `🕸️ Tema ${_rnPos+1}/${EX_RN.length} · ${ex.name}`;
  document.getElementById('masterRnFill').style.width=pct+'%';
  document.getElementById('masterRnPct').textContent=pct+'% del temario RN dominado';
  document.getElementById('mPrevRn').disabled=(_rnPos<=0);
  const atEnd=_rnPos>=EX_RN.length-1;
  document.getElementById('mNextRn').textContent=atEnd ? '✅ Entendido, terminar' : '✅ Entendido, siguiente ▶';
  if(document.getElementById('masterRnChecklist').style.display!=='none') _rnRenderChecklist();
}
function rnPrev(){ if(_rnPos>0) _rnGoTo(_rnPos-1); }
function rnRepeat(){ _rnGoTo(_rnPos); }
function _rnRestart(){ _rnGoTo(0); }
function rnNext(){
  _rnDone.add(_rnPos);
  _saveRnProgress();
  if(_rnPos>=EX_RN.length-1){
    _rnRenderBar();
    setSt('🎉 ¡Completaste el piloto del Modo Maestro Redes Neuronales y Deep Learning!');
    return;
  }
  _rnGoTo(_rnPos+1);
}
function _rnToggleChecklist(){
  const cl=document.getElementById('masterRnChecklist');
  const show=cl.style.display==='none';
  cl.style.display=show?'block':'none';
  if(show) _rnRenderChecklist();
}
function _rnRenderChecklist(){
  const cl=document.getElementById('masterRnChecklist');
  cl.innerHTML=EX_RN.map((ex,i)=>{
    const done=_rnDone.has(i);
    const cur=i===_rnPos;
    return `<div class="master-item${done?' master-item-done':''}${cur?' master-item-current':''}" onclick="_rnGoTo(${i})">`+
      `<span class="master-item-chk">${done?'✓':(i+1)}</span><span class="master-item-name">${esc(ex.name)}</span>${_failsBadge('rn',i)}${_dontKnowBadge('rn',i)}</div>`;
  }).join('');
}

/* Glosario RN: pedido explícito del usuario ("que ningún término quede sin
   explicación") -- cubre TODO término técnico que aparece en las preguntas,
   teoría o soluciones de los 20 temas de RN (perceptrón, MLP/no linealidad,
   backpropagation, CNN, Dropout), buscable vía el botón "📚 Glosario". */
const GLOSSARY_RN=[
{term:'Aproximador universal', def:'El resultado teórico que dice que un MLP con al menos una capa oculta y activación no lineal puede llegar a aproximar cualquier función continua — es la base matemática de por qué las redes neuronales sirven para tantos problemas distintos.'},
{term:'Backpropagation (retropropagación)', def:'El algoritmo que calcula el gradiente del error respecto a CADA peso de la red, propagando el error hacia atrás capa por capa (de la salida hacia la entrada) usando la regla de la cadena — es lo que hace posible entrenar redes con millones de pesos.'},
{term:'Capa convolucional (CNN)', def:'Una capa que, en vez de conectar cada neurona con cada píxel, desliza un filtro (kernel) pequeño y compartido sobre toda la imagen — usa muchos menos parámetros que una capa densa y detecta patrones locales como bordes.'},
{term:'Capa oculta (hidden layer)', def:'Cualquier capa de neuronas entre la entrada y la salida de una red — combinada con una activación no lineal, es lo que le da a un MLP la capacidad de resolver problemas que un perceptrón simple no puede (como XOR).'},
{term:'Descenso del gradiente', def:'El método de optimización que ajusta los pesos en la dirección que MÁS reduce el error, usando el gradiente calculado por backpropagation — el tamaño de cada paso lo controla la tasa de aprendizaje (η).'},
{term:'Dropout', def:'Una técnica de regularización que apaga al azar un porcentaje de neuronas en cada paso de entrenamiento (nunca en inferencia), obligando a la red a no depender de neuronas puntuales — mejora la generalización a datos nuevos.'},
{term:'Época (epoch)', def:'Una pasada completa por todos los ejemplos del set de entrenamiento — el conteo de errores o el loss se suele medir por época para ver si el modelo está mejorando.'},
{term:'Escalón (step function)', def:'La función de activación más simple: devuelve 1 si la entrada es ≥0, y 0 si no — la usó el perceptrón original, pero no tiene derivada útil, por lo que no se usa en redes modernas entrenadas por gradiente.'},
{term:'Feature map (mapa de características)', def:'El resultado de aplicar un filtro convolucional sobre una imagen: una nueva "imagen" donde los valores altos marcan dónde se detectó el patrón que busca ese filtro (por ejemplo, un borde).'},
{term:'Función de activación', def:'La función que transforma la suma ponderada (z = w·x + b) de una neurona en su salida final — puede ser lineal (poco útil) o no lineal (escalón, sigmoid, ReLU), y es la no linealidad la que le da poder a una red de varias capas.'},
{term:'Generalización', def:'Qué tan bien funciona un modelo con datos NUEVOS, que no vio durante el entrenamiento — el objetivo real de entrenar una red, distinto de memorizar perfectamente los ejemplos de entrenamiento.'},
{term:'Gradiente', def:'La dirección (y magnitud) en la que hay que mover un peso para reducir el error lo más rápido posible — backpropagation es el método para calcularlo eficientemente para cada peso de la red.'},
{term:'Inferencia', def:'La fase en la que un modelo YA entrenado se usa para predecir sobre datos nuevos — distinta del entrenamiento; por ejemplo, dropout se desactiva por completo en esta fase.'},
{term:'Inverted dropout', def:'La variante de dropout que, durante el entrenamiento, escala las activaciones que quedan activas dividiendo por keep=1-p — así compensa que en ese paso hay menos neuronas aportando señal que en inferencia.'},
{term:'Kernel / filtro convolucional', def:'Una matriz pequeña de pesos (por ejemplo 3x3) que se desliza sobre una imagen calculando una suma ponderada en cada posición — el mismo kernel (mismos pesos) se reutiliza en toda la imagen.'},
{term:'Loss (función de pérdida / error)', def:'Un número que mide qué tan mal está prediciendo el modelo en un momento dado — el objetivo del entrenamiento es reducirlo lo más posible, ajustando los pesos con descenso del gradiente.'},
{term:'Max pooling', def:'Una operación que divide un feature map en bloques (por ejemplo 2x2) y se queda con el valor MÁXIMO de cada bloque, reduciendo el tamaño y dándole a la red tolerancia a pequeños desplazamientos del patrón detectado.'},
{term:'MLP (Multi-Layer Perceptron / Perceptrón multicapa)', def:'Una red neuronal con una o más capas ocultas entre la entrada y la salida — a diferencia de un perceptrón simple, puede resolver problemas no linealmente separables como XOR, gracias a sus capas ocultas con activación no lineal.'},
{term:'Neurona artificial', def:'La unidad básica de una red neuronal: recibe varias entradas, las combina con pesos (w) y un sesgo (b) en una suma ponderada z, y aplica una función de activación para producir su salida.'},
{term:'Padding', def:'Agregar un borde extra (normalmente de ceros) alrededor de una imagen antes de aplicar un filtro convolucional, para que el resultado NO se achique respecto al tamaño original.'},
{term:'Peso (w) / Sesgo (bias, b)', def:'Los parámetros que una neurona ajusta durante el entrenamiento: cada entrada se multiplica por su peso correspondiente, y el sesgo se suma aparte — juntos determinan la suma ponderada z antes de la activación.'},
{term:'Perceptrón', def:'La neurona artificial más simple, con activación escalón — puede aprender a separar datos con UNA sola frontera recta (linealmente separables), pero no puede resolver problemas como XOR.'},
{term:'ReLU', def:'Una función de activación no lineal muy usada en redes modernas: devuelve la entrada tal cual si es positiva, y 0 si es negativa (max(0,z)) — es simple de calcular y evita algunos problemas de gradientes que tienen otras activaciones.'},
{term:'Regla de la cadena', def:'La regla del cálculo diferencial que permite calcular la derivada de una función compuesta multiplicando las derivadas de cada parte — es lo que backpropagation usa, capa por capa, para calcular el gradiente de toda la red.'},
{term:'Separabilidad lineal / linealmente separable', def:'Un conjunto de datos es linealmente separable si existe una línea (o plano/hiperplano) recta que deja todos los puntos de una clase de un lado y todos los de la otra clase del otro — un perceptrón simple solo puede resolver este tipo de problemas.'},
{term:'Sigmoid', def:'Una función de activación no lineal que aplasta cualquier número real a un valor entre 0 y 1, con forma de "S" — fue muy usada históricamente, aunque en redes muy profundas puede causar el problema de gradientes que se desvanecen.'},
{term:'Tasa de aprendizaje (learning rate, η/eta)', def:'El número que controla qué tan grande es cada paso de ajuste de los pesos, en la fórmula w ← w − η·gradiente — muy alta puede hacer que el entrenamiento diverja, muy baja lo hace lento.'},
{term:'XOR (problema clásico)', def:'Una función lógica de 2 entradas (verdadero solo si exactamente una es verdadera) que NO es linealmente separable — el ejemplo clásico para mostrar el límite de un perceptrón simple y por qué hace falta una capa oculta.'},
];
function _rnToggleGlossary(){
  const gl=document.getElementById('masterRnGlossary');
  const show=gl.style.display==='none';
  gl.style.display=show?'block':'none';
  if(show) _rnRenderGlossary();
}
function _rnRenderGlossary(){
  const input=document.getElementById('rnGlossarySearch');
  document.getElementById('rnGlossaryList').innerHTML=_glossaryHtml(GLOSSARY_RN, input?input.value:'');
}

/* ──────────── RN_COMPARE: peldaño "Comparación" (Escalera de Dominio) ────────────
   Mismo patrón que AS_COMPARE en master-as.js. `pair` son los dos índices
   BASE (múltiplos de 4) en EX_RN. */
const RN_COMPARE=[
{pair:[0,4],
 question:'El perceptrón sin capa oculta y el MLP con una capa oculta son ambos "redes neuronales". '+
  '¿Qué diferencia estructural explica que uno resuelva XOR y el otro no?',
 options:[
  'El MLP agrega una capa OCULTA con activación NO lineal (ReLU) entre la entrada y la salida — eso '+
   'le permite combinar varias fronteras rectas simples en una frontera final curva/quebrada, algo '+
   'que el perceptrón (una sola capa, sin no-linealidad intermedia) no puede lograr.',
  'El MLP simplemente usa una tasa de aprendizaje más alta que el perceptrón.',
  'El perceptrón y el MLP son matemáticamente idénticos, solo cambia el nombre.',
  'El perceptrón tiene más pesos numéricos que el MLP.'],
 correct:0,
 solution:'La clave no es "más entrenamiento" ni "más parámetros" sueltos — es agregar una capa '+
  'OCULTA con no-linealidad. Sin eso, apilar capas colapsa matemáticamente en una única '+
  'transformación lineal, tan limitada como el perceptrón original: por eso el perceptrón se '+
  'estanca en 25% de precisión en XOR y el MLP llega a 100%.'},
];
function _rnCompareUnlocked(i){
  const [a,b]=RN_COMPARE[i].pair;
  const done=x=>[x,x+1,x+2,x+3].some(j=>_rnDone.has(j));
  return done(a) && done(b);
}

/* ──────────── RN_LIMITS: peldaño "Limitación" (Escalera de Dominio) ────────────
   Mismo patrón que AS_LIMITS en master-as.js. `concept` es el índice BASE
   (múltiplo de 4) en EX_RN. */
const RN_LIMITS=[
{concept:12,
 question:'Una capa convolucional (CNN) asume que el patrón que busca (un borde, una forma) puede '+
  'aparecer en CUALQUIER posición de una grilla espacial, y reutiliza el mismo kernel deslizándolo. '+
  '¿Qué pasa si aplicás una CNN a una tabla de datos normal (por ejemplo, precio/habitaciones/'+
  'antigüedad de una casa, sin ningún orden espacial entre columnas)?',
 options:[
  'Una CNN funciona igual de bien que en imágenes, porque el mecanismo de convolución es '+
   'universal y no depende del tipo de dato.',
  'La CNN no tiene ninguna ventaja ahí: su supuesto central (patrones LOCALES que se repiten en '+
   'distintas posiciones de una grilla) no tiene sentido cuando las columnas no tienen una relación '+
   'espacial real entre sí — "precio" y "antigüedad" no son vecinos de la misma forma que dos '+
   'píxeles lo son en una imagen.',
  'Una CNN necesita menos datos de entrenamiento que un MLP normal para tablas.',
  'Las CNN solo pueden usarse con números enteros, nunca con datos numéricos continuos.'],
 correct:1,
 solution:'El truco que hace poderosa a una CNN (reutilizar el mismo filtro deslizándolo, '+
  'asumiendo que un patrón puede aparecer en cualquier posición de una grilla) deja de aportar '+
  'nada cuando no hay una estructura espacial/local real detrás de los datos — reordenar las '+
  'columnas de una tabla no debería cambiar el resultado de un buen modelo, pero SÍ cambiaría '+
  'completamente lo que "ve" una convolución. Para datos tabulares comunes, un MLP normal (o '+
  'árboles/ensembles, ver Modo Maestro AS) suele funcionar igual o mejor, con menos complejidad.'},
];
function _rnLimitsUnlocked(i){
  const c=RN_LIMITS[i].concept;
  return [c,c+1,c+2,c+3].some(j=>_rnDone.has(j));
}

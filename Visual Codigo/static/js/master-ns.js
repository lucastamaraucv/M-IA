/* ──────────── Modo Maestro NS (No Supervisado) ──────────────
   Sexto temario guiado, independiente de Python/AO/Matemáticas/RA/AS: progreso, botón y barra propios. Piloto de 3 conceptos (12 preguntas aplanadas) construido leyendo Géron, Cap.8-9 (Dimensionality Reduction, Unsupervised Learning Techniques) -- ampliable en tandas futuras, mismo patrón que AO/RA.
   Fuente: ver comentario de cada tema (cita de página real). Verificado
   ejecutando de verdad el código con el intérprete Python del sistema antes
   de fijar cualquier número en la teoría o en las preguntas. */
const EX_NS = [
 {
  "name": "No Supervisado · Sin etiquetas: qué busca",
  "theory": "Aprendizaje supervisado es como estudiar con un libro de ejercicios que trae las respuestas al final: ves la pregunta (X) y la respuesta correcta (y), y aprendés a imitar esa relación. Aprendizaje <b>no supervisado</b> es estudiar sin ningún solucionario — te dan solo un montón de ejercicios (X) y tenés que encontrar vos mismo qué patrones, grupos o regularidades hay ahí adentro, sin que nadie te diga cuál es la respuesta \"correcta\".<br><br>En el código, <code>make_blobs</code> genera puntos que sí tienen una etiqueta real (<code>y_true</code>) — pero es un truco para que NOSOTROS podamos comprobar el resultado después. El algoritmo de clustering nunca la ve: solo recibe <code>X</code> (las coordenadas) y tiene que descubrir la agrupación por su cuenta. Esta es la diferencia de fondo entre <code>fit(X, y)</code> (supervisado, como en el Modo Maestro AS) y <code>fit(X)</code> (no supervisado) — un solo argumento menos, pero un problema completamente distinto: sin respuesta correcta que copiar, solo estructura que encontrar.",
  "code": "# No supervisado: el algoritmo NUNCA ve las etiquetas (Geron, Cap.9).\n# make_blobs genera puntos con una etiqueta 'real' y_true SOLO para que\n# nosotros, humanos, podamos verificar despues -- el algoritmo de\n# clustering jamas recibe y_true como entrada.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_blobs\n\nX, y_true = make_blobs(n_samples=30, centers=3, cluster_std=0.7, random_state=42)\nprint(\"forma de X (lo unico que ve el algoritmo):\", X.shape)\nprint(\"primeros 5 puntos de X:\", np.round(X[:5], 2).tolist())\nprint(\"\\ny_true existe en el dataset (para que NOSOTROS verifiquemos despues),\")\nprint(\"pero el algoritmo de clustering NUNCA la recibe como entrada:\")\nprint(\"y_true (oculto para el algoritmo):\", y_true[:5].tolist())\nprint(\"\\nEn aprendizaje SUPERVISADO (AS), fit(X, y) siempre lleva las dos.\")\nprint(\"En NO supervisado, fit(X) recibe solo una -- no hay respuesta correcta\")\nprint(\"que copiar, solo estructura que descubrir por cuenta propia.\")",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 1,
    "cols": 5,
    "barMode": true,
    "rowLabels": [
     "y (oculto)"
    ],
    "values": [
     [
      0,
      1,
      1,
      1,
      0
     ]
    ],
    "cellText": [
     [
      "0",
      "1",
      "1",
      "1",
      "0"
     ]
    ],
    "min": 0,
    "max": 1,
    "aria": "Las etiquetas y_true existen en el dataset para verificar despues, pero el algoritmo de clustering nunca las recibe"
   }
  },
  "application": "El aprendizaje no supervisado es lo que se usa cuando etiquetar los datos a mano sería carísimo o directamente imposible: segmentar millones de clientes de un banco por patrón de gasto (nadie etiquetó \"a mano\" a qué grupo pertenece cada cliente), detectar anomalías en tráfico de red para ciberseguridad (los ataques nuevos no vienen con la etiqueta \"esto es un ataque\"), o comprimir imágenes/agrupar genes en bioinformática — en todos estos casos hay datos de sobra, pero ninguna respuesta correcta pre-etiquetada (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.9)."
 },
 {
  "name": "No Supervisado · Sin etiquetas: qué busca — pregunta 2",
  "theory": "Aprendizaje supervisado es como estudiar con un libro de ejercicios que trae las respuestas al final: ves la pregunta (X) y la respuesta correcta (y), y aprendés a imitar esa relación. Aprendizaje <b>no supervisado</b> es estudiar sin ningún solucionario — te dan solo un montón de ejercicios (X) y tenés que encontrar vos mismo qué patrones, grupos o regularidades hay ahí adentro, sin que nadie te diga cuál es la respuesta \"correcta\".<br><br>En el código, <code>make_blobs</code> genera puntos que sí tienen una etiqueta real (<code>y_true</code>) — pero es un truco para que NOSOTROS podamos comprobar el resultado después. El algoritmo de clustering nunca la ve: solo recibe <code>X</code> (las coordenadas) y tiene que descubrir la agrupación por su cuenta. Esta es la diferencia de fondo entre <code>fit(X, y)</code> (supervisado, como en el Modo Maestro AS) y <code>fit(X)</code> (no supervisado) — un solo argumento menos, pero un problema completamente distinto: sin respuesta correcta que copiar, solo estructura que encontrar.",
  "code": "# No supervisado: el algoritmo NUNCA ve las etiquetas (Geron, Cap.9).\n# make_blobs genera puntos con una etiqueta 'real' y_true SOLO para que\n# nosotros, humanos, podamos verificar despues -- el algoritmo de\n# clustering jamas recibe y_true como entrada.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_blobs\n\nX, y_true = make_blobs(n_samples=30, centers=3, cluster_std=0.7, random_state=42)\nprint(\"forma de X (lo unico que ve el algoritmo):\", X.shape)\nprint(\"primeros 5 puntos de X:\", np.round(X[:5], 2).tolist())\nprint(\"\\ny_true existe en el dataset (para que NOSOTROS verifiquemos despues),\")\nprint(\"pero el algoritmo de clustering NUNCA la recibe como entrada:\")\nprint(\"y_true (oculto para el algoritmo):\", y_true[:5].tolist())\nprint(\"\\nEn aprendizaje SUPERVISADO (AS), fit(X, y) siempre lleva las dos.\")\nprint(\"En NO supervisado, fit(X) recibe solo una -- no hay respuesta correcta\")\nprint(\"que copiar, solo estructura que descubrir por cuenta propia.\")",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 1,
    "cols": 5,
    "barMode": true,
    "rowLabels": [
     "y (oculto)"
    ],
    "values": [
     [
      0,
      1,
      1,
      1,
      0
     ]
    ],
    "cellText": [
     [
      "0",
      "1",
      "1",
      "1",
      "0"
     ]
    ],
    "min": 0,
    "max": 1,
    "aria": "Las etiquetas y_true existen en el dataset para verificar despues, pero el algoritmo de clustering nunca las recibe"
   }
  },
  "application": "El aprendizaje no supervisado es lo que se usa cuando etiquetar los datos a mano sería carísimo o directamente imposible: segmentar millones de clientes de un banco por patrón de gasto (nadie etiquetó \"a mano\" a qué grupo pertenece cada cliente), detectar anomalías en tráfico de red para ciberseguridad (los ataques nuevos no vienen con la etiqueta \"esto es un ataque\"), o comprimir imágenes/agrupar genes en bioinformática — en todos estos casos hay datos de sobra, pero ninguna respuesta correcta pre-etiquetada (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.9)."
 },
 {
  "name": "No Supervisado · Sin etiquetas: qué busca — pregunta 3",
  "theory": "Aprendizaje supervisado es como estudiar con un libro de ejercicios que trae las respuestas al final: ves la pregunta (X) y la respuesta correcta (y), y aprendés a imitar esa relación. Aprendizaje <b>no supervisado</b> es estudiar sin ningún solucionario — te dan solo un montón de ejercicios (X) y tenés que encontrar vos mismo qué patrones, grupos o regularidades hay ahí adentro, sin que nadie te diga cuál es la respuesta \"correcta\".<br><br>En el código, <code>make_blobs</code> genera puntos que sí tienen una etiqueta real (<code>y_true</code>) — pero es un truco para que NOSOTROS podamos comprobar el resultado después. El algoritmo de clustering nunca la ve: solo recibe <code>X</code> (las coordenadas) y tiene que descubrir la agrupación por su cuenta. Esta es la diferencia de fondo entre <code>fit(X, y)</code> (supervisado, como en el Modo Maestro AS) y <code>fit(X)</code> (no supervisado) — un solo argumento menos, pero un problema completamente distinto: sin respuesta correcta que copiar, solo estructura que encontrar.",
  "code": "# No supervisado: el algoritmo NUNCA ve las etiquetas (Geron, Cap.9).\n# make_blobs genera puntos con una etiqueta 'real' y_true SOLO para que\n# nosotros, humanos, podamos verificar despues -- el algoritmo de\n# clustering jamas recibe y_true como entrada.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_blobs\n\nX, y_true = make_blobs(n_samples=30, centers=3, cluster_std=0.7, random_state=42)\nprint(\"forma de X (lo unico que ve el algoritmo):\", X.shape)\nprint(\"primeros 5 puntos de X:\", np.round(X[:5], 2).tolist())\nprint(\"\\ny_true existe en el dataset (para que NOSOTROS verifiquemos despues),\")\nprint(\"pero el algoritmo de clustering NUNCA la recibe como entrada:\")\nprint(\"y_true (oculto para el algoritmo):\", y_true[:5].tolist())\nprint(\"\\nEn aprendizaje SUPERVISADO (AS), fit(X, y) siempre lleva las dos.\")\nprint(\"En NO supervisado, fit(X) recibe solo una -- no hay respuesta correcta\")\nprint(\"que copiar, solo estructura que descubrir por cuenta propia.\")",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 1,
    "cols": 5,
    "barMode": true,
    "rowLabels": [
     "y (oculto)"
    ],
    "values": [
     [
      0,
      1,
      1,
      1,
      0
     ]
    ],
    "cellText": [
     [
      "0",
      "1",
      "1",
      "1",
      "0"
     ]
    ],
    "min": 0,
    "max": 1,
    "aria": "Las etiquetas y_true existen en el dataset para verificar despues, pero el algoritmo de clustering nunca las recibe"
   }
  },
  "application": "El aprendizaje no supervisado es lo que se usa cuando etiquetar los datos a mano sería carísimo o directamente imposible: segmentar millones de clientes de un banco por patrón de gasto (nadie etiquetó \"a mano\" a qué grupo pertenece cada cliente), detectar anomalías en tráfico de red para ciberseguridad (los ataques nuevos no vienen con la etiqueta \"esto es un ataque\"), o comprimir imágenes/agrupar genes en bioinformática — en todos estos casos hay datos de sobra, pero ninguna respuesta correcta pre-etiquetada (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.9)."
 },
 {
  "name": "No Supervisado · Sin etiquetas: qué busca — pregunta 4",
  "theory": "Aprendizaje supervisado es como estudiar con un libro de ejercicios que trae las respuestas al final: ves la pregunta (X) y la respuesta correcta (y), y aprendés a imitar esa relación. Aprendizaje <b>no supervisado</b> es estudiar sin ningún solucionario — te dan solo un montón de ejercicios (X) y tenés que encontrar vos mismo qué patrones, grupos o regularidades hay ahí adentro, sin que nadie te diga cuál es la respuesta \"correcta\".<br><br>En el código, <code>make_blobs</code> genera puntos que sí tienen una etiqueta real (<code>y_true</code>) — pero es un truco para que NOSOTROS podamos comprobar el resultado después. El algoritmo de clustering nunca la ve: solo recibe <code>X</code> (las coordenadas) y tiene que descubrir la agrupación por su cuenta. Esta es la diferencia de fondo entre <code>fit(X, y)</code> (supervisado, como en el Modo Maestro AS) y <code>fit(X)</code> (no supervisado) — un solo argumento menos, pero un problema completamente distinto: sin respuesta correcta que copiar, solo estructura que encontrar.",
  "code": "# No supervisado: el algoritmo NUNCA ve las etiquetas (Geron, Cap.9).\n# make_blobs genera puntos con una etiqueta 'real' y_true SOLO para que\n# nosotros, humanos, podamos verificar despues -- el algoritmo de\n# clustering jamas recibe y_true como entrada.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_blobs\n\nX, y_true = make_blobs(n_samples=30, centers=3, cluster_std=0.7, random_state=42)\nprint(\"forma de X (lo unico que ve el algoritmo):\", X.shape)\nprint(\"primeros 5 puntos de X:\", np.round(X[:5], 2).tolist())\nprint(\"\\ny_true existe en el dataset (para que NOSOTROS verifiquemos despues),\")\nprint(\"pero el algoritmo de clustering NUNCA la recibe como entrada:\")\nprint(\"y_true (oculto para el algoritmo):\", y_true[:5].tolist())\nprint(\"\\nEn aprendizaje SUPERVISADO (AS), fit(X, y) siempre lleva las dos.\")\nprint(\"En NO supervisado, fit(X) recibe solo una -- no hay respuesta correcta\")\nprint(\"que copiar, solo estructura que descubrir por cuenta propia.\")",
  "viz": {
   "type": "grid",
   "data": {
    "rows": 1,
    "cols": 5,
    "barMode": true,
    "rowLabels": [
     "y (oculto)"
    ],
    "values": [
     [
      0,
      1,
      1,
      1,
      0
     ]
    ],
    "cellText": [
     [
      "0",
      "1",
      "1",
      "1",
      "0"
     ]
    ],
    "min": 0,
    "max": 1,
    "aria": "Las etiquetas y_true existen en el dataset para verificar despues, pero el algoritmo de clustering nunca las recibe"
   }
  },
  "application": "El aprendizaje no supervisado es lo que se usa cuando etiquetar los datos a mano sería carísimo o directamente imposible: segmentar millones de clientes de un banco por patrón de gasto (nadie etiquetó \"a mano\" a qué grupo pertenece cada cliente), detectar anomalías en tráfico de red para ciberseguridad (los ataques nuevos no vienen con la etiqueta \"esto es un ataque\"), o comprimir imágenes/agrupar genes en bioinformática — en todos estos casos hay datos de sobra, pero ninguna respuesta correcta pre-etiquetada (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.9)."
 },
 {
  "name": "No Supervisado · K-Means: centroides e inercia",
  "theory": "K-Means es como repartir el salón de clase en k grupos de trabajo sin que el profesor diga quién va con quién: elegís k puntos al azar como \"líderes\" iniciales, cada alumno se junta con el líder más cercano, después cada grupo recalcula su \"centro real\" (el promedio de sus posiciones), y se repite hasta que nadie cambia de grupo.<br><br>En el código, con 30 puntos generados en 3 grupos reales, K-Means con k=3 encuentra 3 centros bastante cercanos a los reales, con una <b>inercia</b> (la suma de qué tan lejos está cada punto de su centroide, al cuadrado) de ≈23,53. Con k=5 la inercia baja a ≈15,47 — pero ojo: la inercia SIEMPRE baja al agregar más centroides (con 30 centroides, uno por punto, la inercia sería 0), así que \"menor inercia\" no significa automáticamente \"mejor agrupación\" — hace falta un criterio como el método del codo para elegir k de verdad.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.9): K-Means minimiza la inercia $\\sum_i \\min_{\\mu_j \\in C} \\lVert x_i - \\mu_j \\rVert^2$ — la distancia al cuadrado de cada punto $x_i$ a su centroide asignado más cercano $\\mu_j$.",
  "code": "# K-Means (Geron, Cap.9): agrupa puntos en k grupos, cada uno representado\n# por un CENTROIDE (el promedio de sus puntos). Minimiza la 'inercia': la\n# suma de distancias al cuadrado de cada punto a su centroide asignado.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_blobs\nfrom sklearn.cluster import KMeans\n\nX, y_true = make_blobs(n_samples=30, centers=3, cluster_std=0.7, random_state=42)\n\nkm3 = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)\nkm5 = KMeans(n_clusters=5, n_init=10, random_state=42).fit(X)\n\nprint(\"k=3 -- centros encontrados (promedio de cada grupo):\")\nprint(np.round(km3.cluster_centers_, 2).tolist())\nprint(\"k=3 -- inercia (suma de distancias^2 al centroide):\", round(km3.inertia_, 2))\nprint(\"k=5 -- inercia:\", round(km5.inertia_, 2))\n\n# La inercia SIEMPRE baja al aumentar k (mas centroides = puntos mas cerca\n# de alguno) -- por eso no sirve para elegir k solo por 'inercia mas baja',\n# hace falta el 'metodo del codo' u otro criterio (ver Cap.9 del libro).\nprint(\"\\nLa inercia bajo de\", round(km3.inertia_,2), \"a\", round(km5.inertia_,2),\n\"al pasar de k=3 a k=5 -- pero eso NO prueba que k=5 sea mejor: mas centroides\")\nprint(\"siempre reducen la inercia, aunque no reflejen grupos reales del dato.\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Inercia k=3",
     "Inercia k=5"
    ],
    "values": [
     23.53,
     15.47
    ],
    "unit": "",
    "aria": "La inercia baja de 23.53 (k=3) a 15.47 (k=5) simplemente por tener mas centroides, no porque k=5 agrupe mejor"
   }
  },
  "application": "K-Means es probablemente el algoritmo de clustering más usado en la práctica por lo simple y rápido que es: segmentación de mercado (agrupar clientes por hábito de compra sin que nadie los haya etiquetado a mano), compresión de imágenes (reemplazar millones de colores por los k colores de los centroides), y como paso de preprocesamiento antes de otros algoritmos (por ejemplo, para inicializar regiones en visión por computadora). Su gran limitación — que hay que decidir k de antemano y que asume grupos redondeados de tamaño similar — es justamente lo que dispara la búsqueda de alternativas como DBSCAN, que también cubre el Cap.9 (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019))."
 },
 {
  "name": "No Supervisado · K-Means: centroides e inercia — pregunta 2",
  "theory": "K-Means es como repartir el salón de clase en k grupos de trabajo sin que el profesor diga quién va con quién: elegís k puntos al azar como \"líderes\" iniciales, cada alumno se junta con el líder más cercano, después cada grupo recalcula su \"centro real\" (el promedio de sus posiciones), y se repite hasta que nadie cambia de grupo.<br><br>En el código, con 30 puntos generados en 3 grupos reales, K-Means con k=3 encuentra 3 centros bastante cercanos a los reales, con una <b>inercia</b> (la suma de qué tan lejos está cada punto de su centroide, al cuadrado) de ≈23,53. Con k=5 la inercia baja a ≈15,47 — pero ojo: la inercia SIEMPRE baja al agregar más centroides (con 30 centroides, uno por punto, la inercia sería 0), así que \"menor inercia\" no significa automáticamente \"mejor agrupación\" — hace falta un criterio como el método del codo para elegir k de verdad.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.9): K-Means minimiza la inercia $\\sum_i \\min_{\\mu_j \\in C} \\lVert x_i - \\mu_j \\rVert^2$ — la distancia al cuadrado de cada punto $x_i$ a su centroide asignado más cercano $\\mu_j$.",
  "code": "# K-Means (Geron, Cap.9): agrupa puntos en k grupos, cada uno representado\n# por un CENTROIDE (el promedio de sus puntos). Minimiza la 'inercia': la\n# suma de distancias al cuadrado de cada punto a su centroide asignado.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_blobs\nfrom sklearn.cluster import KMeans\n\nX, y_true = make_blobs(n_samples=30, centers=3, cluster_std=0.7, random_state=42)\n\nkm3 = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)\nkm5 = KMeans(n_clusters=5, n_init=10, random_state=42).fit(X)\n\nprint(\"k=3 -- centros encontrados (promedio de cada grupo):\")\nprint(np.round(km3.cluster_centers_, 2).tolist())\nprint(\"k=3 -- inercia (suma de distancias^2 al centroide):\", round(km3.inertia_, 2))\nprint(\"k=5 -- inercia:\", round(km5.inertia_, 2))\n\n# La inercia SIEMPRE baja al aumentar k (mas centroides = puntos mas cerca\n# de alguno) -- por eso no sirve para elegir k solo por 'inercia mas baja',\n# hace falta el 'metodo del codo' u otro criterio (ver Cap.9 del libro).\nprint(\"\\nLa inercia bajo de\", round(km3.inertia_,2), \"a\", round(km5.inertia_,2),\n\"al pasar de k=3 a k=5 -- pero eso NO prueba que k=5 sea mejor: mas centroides\")\nprint(\"siempre reducen la inercia, aunque no reflejen grupos reales del dato.\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Inercia k=3",
     "Inercia k=5"
    ],
    "values": [
     23.53,
     15.47
    ],
    "unit": "",
    "aria": "La inercia baja de 23.53 (k=3) a 15.47 (k=5) simplemente por tener mas centroides, no porque k=5 agrupe mejor"
   }
  },
  "application": "K-Means es probablemente el algoritmo de clustering más usado en la práctica por lo simple y rápido que es: segmentación de mercado (agrupar clientes por hábito de compra sin que nadie los haya etiquetado a mano), compresión de imágenes (reemplazar millones de colores por los k colores de los centroides), y como paso de preprocesamiento antes de otros algoritmos (por ejemplo, para inicializar regiones en visión por computadora). Su gran limitación — que hay que decidir k de antemano y que asume grupos redondeados de tamaño similar — es justamente lo que dispara la búsqueda de alternativas como DBSCAN, que también cubre el Cap.9 (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019))."
 },
 {
  "name": "No Supervisado · K-Means: centroides e inercia — pregunta 3",
  "theory": "K-Means es como repartir el salón de clase en k grupos de trabajo sin que el profesor diga quién va con quién: elegís k puntos al azar como \"líderes\" iniciales, cada alumno se junta con el líder más cercano, después cada grupo recalcula su \"centro real\" (el promedio de sus posiciones), y se repite hasta que nadie cambia de grupo.<br><br>En el código, con 30 puntos generados en 3 grupos reales, K-Means con k=3 encuentra 3 centros bastante cercanos a los reales, con una <b>inercia</b> (la suma de qué tan lejos está cada punto de su centroide, al cuadrado) de ≈23,53. Con k=5 la inercia baja a ≈15,47 — pero ojo: la inercia SIEMPRE baja al agregar más centroides (con 30 centroides, uno por punto, la inercia sería 0), así que \"menor inercia\" no significa automáticamente \"mejor agrupación\" — hace falta un criterio como el método del codo para elegir k de verdad.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.9): K-Means minimiza la inercia $\\sum_i \\min_{\\mu_j \\in C} \\lVert x_i - \\mu_j \\rVert^2$ — la distancia al cuadrado de cada punto $x_i$ a su centroide asignado más cercano $\\mu_j$.",
  "code": "# K-Means (Geron, Cap.9): agrupa puntos en k grupos, cada uno representado\n# por un CENTROIDE (el promedio de sus puntos). Minimiza la 'inercia': la\n# suma de distancias al cuadrado de cada punto a su centroide asignado.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_blobs\nfrom sklearn.cluster import KMeans\n\nX, y_true = make_blobs(n_samples=30, centers=3, cluster_std=0.7, random_state=42)\n\nkm3 = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)\nkm5 = KMeans(n_clusters=5, n_init=10, random_state=42).fit(X)\n\nprint(\"k=3 -- centros encontrados (promedio de cada grupo):\")\nprint(np.round(km3.cluster_centers_, 2).tolist())\nprint(\"k=3 -- inercia (suma de distancias^2 al centroide):\", round(km3.inertia_, 2))\nprint(\"k=5 -- inercia:\", round(km5.inertia_, 2))\n\n# La inercia SIEMPRE baja al aumentar k (mas centroides = puntos mas cerca\n# de alguno) -- por eso no sirve para elegir k solo por 'inercia mas baja',\n# hace falta el 'metodo del codo' u otro criterio (ver Cap.9 del libro).\nprint(\"\\nLa inercia bajo de\", round(km3.inertia_,2), \"a\", round(km5.inertia_,2),\n\"al pasar de k=3 a k=5 -- pero eso NO prueba que k=5 sea mejor: mas centroides\")\nprint(\"siempre reducen la inercia, aunque no reflejen grupos reales del dato.\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Inercia k=3",
     "Inercia k=5"
    ],
    "values": [
     23.53,
     15.47
    ],
    "unit": "",
    "aria": "La inercia baja de 23.53 (k=3) a 15.47 (k=5) simplemente por tener mas centroides, no porque k=5 agrupe mejor"
   }
  },
  "application": "K-Means es probablemente el algoritmo de clustering más usado en la práctica por lo simple y rápido que es: segmentación de mercado (agrupar clientes por hábito de compra sin que nadie los haya etiquetado a mano), compresión de imágenes (reemplazar millones de colores por los k colores de los centroides), y como paso de preprocesamiento antes de otros algoritmos (por ejemplo, para inicializar regiones en visión por computadora). Su gran limitación — que hay que decidir k de antemano y que asume grupos redondeados de tamaño similar — es justamente lo que dispara la búsqueda de alternativas como DBSCAN, que también cubre el Cap.9 (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019))."
 },
 {
  "name": "No Supervisado · K-Means: centroides e inercia — pregunta 4",
  "theory": "K-Means es como repartir el salón de clase en k grupos de trabajo sin que el profesor diga quién va con quién: elegís k puntos al azar como \"líderes\" iniciales, cada alumno se junta con el líder más cercano, después cada grupo recalcula su \"centro real\" (el promedio de sus posiciones), y se repite hasta que nadie cambia de grupo.<br><br>En el código, con 30 puntos generados en 3 grupos reales, K-Means con k=3 encuentra 3 centros bastante cercanos a los reales, con una <b>inercia</b> (la suma de qué tan lejos está cada punto de su centroide, al cuadrado) de ≈23,53. Con k=5 la inercia baja a ≈15,47 — pero ojo: la inercia SIEMPRE baja al agregar más centroides (con 30 centroides, uno por punto, la inercia sería 0), así que \"menor inercia\" no significa automáticamente \"mejor agrupación\" — hace falta un criterio como el método del codo para elegir k de verdad.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.9): K-Means minimiza la inercia $\\sum_i \\min_{\\mu_j \\in C} \\lVert x_i - \\mu_j \\rVert^2$ — la distancia al cuadrado de cada punto $x_i$ a su centroide asignado más cercano $\\mu_j$.",
  "code": "# K-Means (Geron, Cap.9): agrupa puntos en k grupos, cada uno representado\n# por un CENTROIDE (el promedio de sus puntos). Minimiza la 'inercia': la\n# suma de distancias al cuadrado de cada punto a su centroide asignado.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_blobs\nfrom sklearn.cluster import KMeans\n\nX, y_true = make_blobs(n_samples=30, centers=3, cluster_std=0.7, random_state=42)\n\nkm3 = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)\nkm5 = KMeans(n_clusters=5, n_init=10, random_state=42).fit(X)\n\nprint(\"k=3 -- centros encontrados (promedio de cada grupo):\")\nprint(np.round(km3.cluster_centers_, 2).tolist())\nprint(\"k=3 -- inercia (suma de distancias^2 al centroide):\", round(km3.inertia_, 2))\nprint(\"k=5 -- inercia:\", round(km5.inertia_, 2))\n\n# La inercia SIEMPRE baja al aumentar k (mas centroides = puntos mas cerca\n# de alguno) -- por eso no sirve para elegir k solo por 'inercia mas baja',\n# hace falta el 'metodo del codo' u otro criterio (ver Cap.9 del libro).\nprint(\"\\nLa inercia bajo de\", round(km3.inertia_,2), \"a\", round(km5.inertia_,2),\n\"al pasar de k=3 a k=5 -- pero eso NO prueba que k=5 sea mejor: mas centroides\")\nprint(\"siempre reducen la inercia, aunque no reflejen grupos reales del dato.\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Inercia k=3",
     "Inercia k=5"
    ],
    "values": [
     23.53,
     15.47
    ],
    "unit": "",
    "aria": "La inercia baja de 23.53 (k=3) a 15.47 (k=5) simplemente por tener mas centroides, no porque k=5 agrupe mejor"
   }
  },
  "application": "K-Means es probablemente el algoritmo de clustering más usado en la práctica por lo simple y rápido que es: segmentación de mercado (agrupar clientes por hábito de compra sin que nadie los haya etiquetado a mano), compresión de imágenes (reemplazar millones de colores por los k colores de los centroides), y como paso de preprocesamiento antes de otros algoritmos (por ejemplo, para inicializar regiones en visión por computadora). Su gran limitación — que hay que decidir k de antemano y que asume grupos redondeados de tamaño similar — es justamente lo que dispara la búsqueda de alternativas como DBSCAN, que también cubre el Cap.9 (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019)).",
  "codeAnatomy": {
   "title": "KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)",
   "caption": "Entrenar K-Means — cada argumento nombrado controla algo distinto",
   "lines": [
    "km3 = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)"
   ],
   "annotations": [
    {
     "line": 0,
     "text": "km3",
     "label": "Variable",
     "desc": "(guarda el modelo ya entrenado)",
     "side": "top"
    },
    {
     "line": 0,
     "text": "KMeans",
     "label": "Constructor",
     "desc": "(crea el modelo, sin entrenar todavía)",
     "side": "top"
    },
    {
     "line": 0,
     "text": "n_clusters=3",
     "label": "Cuántos grupos",
     "desc": "(k=3, hay que elegirlo)",
     "side": "bottom"
    },
    {
     "line": 0,
     "text": "n_init=10",
     "label": "Repeticiones",
     "desc": "(10 inicializaciones distintas)",
     "side": "bottom"
    },
    {
     "line": 0,
     "text": "random_state=42",
     "label": "Semilla",
     "desc": "(mismo resultado cada vez)",
     "side": "bottom"
    },
    {
     "line": 0,
     "text": ".fit(X)",
     "label": "Entrena",
     "desc": "(solo con X, sin etiquetas)",
     "side": "bottom"
    }
   ]
  }
 },
 {
  "name": "No Supervisado · PCA: reducir dimensiones",
  "theory": "Imaginá que tenés que describir una pizza con 4 números (diámetro, peso, cantidad de queso, cantidad de salsa) pero te dicen que solo podés usar 2. Si diámetro y peso están MUY correlacionados (las pizzas grandes casi siempre pesan más), perder una de esas dos columnas casi no pierde información real — las dos decían casi lo mismo. PCA hace exactamente eso, pero de forma matemática y automática: encuentra las direcciones donde los datos varían MÁS (las más \"informativas\") y descarta las que casi no aportan nada nuevo.<br><br>En el código, el dataset iris tiene 4 columnas (4 medidas de cada flor). PCA reduce eso a 2 columnas nuevas — pero esas 2 columnas nuevas conservan el 97,77% de toda la variación real del dataset original: la primera columna nueva sola ya explica el 92,46%. Es decir, casi no se perdió información real al pasar de 4 a 2 dimensiones, porque las 4 columnas originales estaban bastante correlacionadas entre sí.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.8): PCA proyecta los datos sobre los $k$ ejes (componentes principales) que maximizan la varianza explicada, ordenados de mayor a menor — <code>explained_variance_ratio_</code> da, para cada eje nuevo, qué fracción de la varianza total conserva.",
  "code": "# PCA (Geron, Cap.8): reduce el numero de columnas (dimensiones) buscando\n# las direcciones donde los datos varian MAS, para perder la menor cantidad\n# posible de informacion real.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.decomposition import PCA\nfrom sklearn.datasets import load_iris\n\niris = load_iris()\nX = iris.data  # 150 flores, 4 columnas: largo/ancho de petalo y sepalo\nprint(\"forma ORIGINAL:\", X.shape, \"(4 columnas)\")\n\npca = PCA(n_components=2, random_state=42).fit(X)\nX2 = pca.transform(X)\nprint(\"forma REDUCIDA:\", X2.shape, \"(2 columnas)\")\n\nprint(\"\\nvarianza explicada por cada componente nuevo:\",\n      np.round(pca.explained_variance_ratio_, 4).tolist())\nprint(\"varianza TOTAL conservada con solo 2 de las 4 columnas originales:\",\n      round(pca.explained_variance_ratio_.sum(), 4))\n\nprint(\"\\nprimeras 3 flores, ANTES (4 columnas):\")\nprint(np.round(X[:3], 2).tolist())\nprint(\"primeras 3 flores, DESPUES (2 columnas):\")\nprint(np.round(X2[:3], 2).tolist())",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Componente 1",
     "Componente 2",
     "Resto (perdido)"
    ],
    "values": [
     0.9246,
     0.0531,
     0.02230000000000002
    ],
    "unit": "",
    "aria": "El primer componente principal explica 92.46% de la varianza, el segundo 5.31%, quedando solo 2.23% sin explicar"
   }
  },
  "application": "PCA es el primer paso casi obligatorio antes de visualizar datos de alta dimensión (no podés graficar 4, 20 o 500 columnas a la vez, pero sí 2 o 3 componentes principales), y también se usa para acelerar el entrenamiento de otros modelos (menos columnas = menos cómputo) y para comprimir datos (guardar solo las direcciones más informativas). En finanzas se usa para resumir cientos de indicadores económicos correlacionados en unos pocos \"factores\" reales; en genética, para reducir miles de genes a las combinaciones que más varían entre individuos (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.8).",
  "codeAnatomy": {
   "title": "pca.fit(X) y pca.transform(X)",
   "caption": "Se ajusta PCA con 2 componentes y se transforman los datos originales de 4 columnas a 2.",
   "lines": [
    "pca = PCA(n_components=2, random_state=42).fit(X)",
    "X2 = pca.transform(X)",
    "print(\"forma REDUCIDA:\", X2.shape, \"(2 columnas)\")"
   ],
   "annotations": [
    {
     "line": 0,
     "text": "PCA",
     "label": "Clase PCA",
     "desc": "(reduce el número de columnas)",
     "side": "top"
    },
    {
     "line": 0,
     "text": "n_components=2",
     "label": "Columnas nuevas",
     "desc": "(de las 4 originales, a 2)",
     "side": "top"
    },
    {
     "line": 0,
     "text": ".fit(X)",
     "label": "Ajusta",
     "desc": "(encuentra las direcciones de mayor varianza)",
     "side": "top"
    },
    {
     "line": 1,
     "text": "pca.transform(X)",
     "label": "Transforma",
     "desc": "(proyecta los datos a las 2 columnas nuevas)",
     "side": "bottom"
    },
    {
     "line": 2,
     "text": "X2.shape",
     "label": "Forma reducida",
     "desc": "(2 columnas en vez de 4)",
     "side": "bottom"
    }
   ]
  }
 },
 {
  "name": "No Supervisado · PCA: reducir dimensiones — pregunta 2",
  "theory": "Imaginá que tenés que describir una pizza con 4 números (diámetro, peso, cantidad de queso, cantidad de salsa) pero te dicen que solo podés usar 2. Si diámetro y peso están MUY correlacionados (las pizzas grandes casi siempre pesan más), perder una de esas dos columnas casi no pierde información real — las dos decían casi lo mismo. PCA hace exactamente eso, pero de forma matemática y automática: encuentra las direcciones donde los datos varían MÁS (las más \"informativas\") y descarta las que casi no aportan nada nuevo.<br><br>En el código, el dataset iris tiene 4 columnas (4 medidas de cada flor). PCA reduce eso a 2 columnas nuevas — pero esas 2 columnas nuevas conservan el 97,77% de toda la variación real del dataset original: la primera columna nueva sola ya explica el 92,46%. Es decir, casi no se perdió información real al pasar de 4 a 2 dimensiones, porque las 4 columnas originales estaban bastante correlacionadas entre sí.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.8): PCA proyecta los datos sobre los $k$ ejes (componentes principales) que maximizan la varianza explicada, ordenados de mayor a menor — <code>explained_variance_ratio_</code> da, para cada eje nuevo, qué fracción de la varianza total conserva.",
  "code": "# PCA (Geron, Cap.8): reduce el numero de columnas (dimensiones) buscando\n# las direcciones donde los datos varian MAS, para perder la menor cantidad\n# posible de informacion real.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.decomposition import PCA\nfrom sklearn.datasets import load_iris\n\niris = load_iris()\nX = iris.data  # 150 flores, 4 columnas: largo/ancho de petalo y sepalo\nprint(\"forma ORIGINAL:\", X.shape, \"(4 columnas)\")\n\npca = PCA(n_components=2, random_state=42).fit(X)\nX2 = pca.transform(X)\nprint(\"forma REDUCIDA:\", X2.shape, \"(2 columnas)\")\n\nprint(\"\\nvarianza explicada por cada componente nuevo:\",\n      np.round(pca.explained_variance_ratio_, 4).tolist())\nprint(\"varianza TOTAL conservada con solo 2 de las 4 columnas originales:\",\n      round(pca.explained_variance_ratio_.sum(), 4))\n\nprint(\"\\nprimeras 3 flores, ANTES (4 columnas):\")\nprint(np.round(X[:3], 2).tolist())\nprint(\"primeras 3 flores, DESPUES (2 columnas):\")\nprint(np.round(X2[:3], 2).tolist())",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Componente 1",
     "Componente 2",
     "Resto (perdido)"
    ],
    "values": [
     0.9246,
     0.0531,
     0.02230000000000002
    ],
    "unit": "",
    "aria": "El primer componente principal explica 92.46% de la varianza, el segundo 5.31%, quedando solo 2.23% sin explicar"
   }
  },
  "application": "PCA es el primer paso casi obligatorio antes de visualizar datos de alta dimensión (no podés graficar 4, 20 o 500 columnas a la vez, pero sí 2 o 3 componentes principales), y también se usa para acelerar el entrenamiento de otros modelos (menos columnas = menos cómputo) y para comprimir datos (guardar solo las direcciones más informativas). En finanzas se usa para resumir cientos de indicadores económicos correlacionados en unos pocos \"factores\" reales; en genética, para reducir miles de genes a las combinaciones que más varían entre individuos (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.8)."
 },
 {
  "name": "No Supervisado · PCA: reducir dimensiones — pregunta 3",
  "theory": "Imaginá que tenés que describir una pizza con 4 números (diámetro, peso, cantidad de queso, cantidad de salsa) pero te dicen que solo podés usar 2. Si diámetro y peso están MUY correlacionados (las pizzas grandes casi siempre pesan más), perder una de esas dos columnas casi no pierde información real — las dos decían casi lo mismo. PCA hace exactamente eso, pero de forma matemática y automática: encuentra las direcciones donde los datos varían MÁS (las más \"informativas\") y descarta las que casi no aportan nada nuevo.<br><br>En el código, el dataset iris tiene 4 columnas (4 medidas de cada flor). PCA reduce eso a 2 columnas nuevas — pero esas 2 columnas nuevas conservan el 97,77% de toda la variación real del dataset original: la primera columna nueva sola ya explica el 92,46%. Es decir, casi no se perdió información real al pasar de 4 a 2 dimensiones, porque las 4 columnas originales estaban bastante correlacionadas entre sí.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.8): PCA proyecta los datos sobre los $k$ ejes (componentes principales) que maximizan la varianza explicada, ordenados de mayor a menor — <code>explained_variance_ratio_</code> da, para cada eje nuevo, qué fracción de la varianza total conserva.",
  "code": "# PCA (Geron, Cap.8): reduce el numero de columnas (dimensiones) buscando\n# las direcciones donde los datos varian MAS, para perder la menor cantidad\n# posible de informacion real.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.decomposition import PCA\nfrom sklearn.datasets import load_iris\n\niris = load_iris()\nX = iris.data  # 150 flores, 4 columnas: largo/ancho de petalo y sepalo\nprint(\"forma ORIGINAL:\", X.shape, \"(4 columnas)\")\n\npca = PCA(n_components=2, random_state=42).fit(X)\nX2 = pca.transform(X)\nprint(\"forma REDUCIDA:\", X2.shape, \"(2 columnas)\")\n\nprint(\"\\nvarianza explicada por cada componente nuevo:\",\n      np.round(pca.explained_variance_ratio_, 4).tolist())\nprint(\"varianza TOTAL conservada con solo 2 de las 4 columnas originales:\",\n      round(pca.explained_variance_ratio_.sum(), 4))\n\nprint(\"\\nprimeras 3 flores, ANTES (4 columnas):\")\nprint(np.round(X[:3], 2).tolist())\nprint(\"primeras 3 flores, DESPUES (2 columnas):\")\nprint(np.round(X2[:3], 2).tolist())",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Componente 1",
     "Componente 2",
     "Resto (perdido)"
    ],
    "values": [
     0.9246,
     0.0531,
     0.02230000000000002
    ],
    "unit": "",
    "aria": "El primer componente principal explica 92.46% de la varianza, el segundo 5.31%, quedando solo 2.23% sin explicar"
   }
  },
  "application": "PCA es el primer paso casi obligatorio antes de visualizar datos de alta dimensión (no podés graficar 4, 20 o 500 columnas a la vez, pero sí 2 o 3 componentes principales), y también se usa para acelerar el entrenamiento de otros modelos (menos columnas = menos cómputo) y para comprimir datos (guardar solo las direcciones más informativas). En finanzas se usa para resumir cientos de indicadores económicos correlacionados en unos pocos \"factores\" reales; en genética, para reducir miles de genes a las combinaciones que más varían entre individuos (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.8)."
 },
 {
  "name": "No Supervisado · PCA: reducir dimensiones — pregunta 4",
  "theory": "Imaginá que tenés que describir una pizza con 4 números (diámetro, peso, cantidad de queso, cantidad de salsa) pero te dicen que solo podés usar 2. Si diámetro y peso están MUY correlacionados (las pizzas grandes casi siempre pesan más), perder una de esas dos columnas casi no pierde información real — las dos decían casi lo mismo. PCA hace exactamente eso, pero de forma matemática y automática: encuentra las direcciones donde los datos varían MÁS (las más \"informativas\") y descarta las que casi no aportan nada nuevo.<br><br>En el código, el dataset iris tiene 4 columnas (4 medidas de cada flor). PCA reduce eso a 2 columnas nuevas — pero esas 2 columnas nuevas conservan el 97,77% de toda la variación real del dataset original: la primera columna nueva sola ya explica el 92,46%. Es decir, casi no se perdió información real al pasar de 4 a 2 dimensiones, porque las 4 columnas originales estaban bastante correlacionadas entre sí.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.8): PCA proyecta los datos sobre los $k$ ejes (componentes principales) que maximizan la varianza explicada, ordenados de mayor a menor — <code>explained_variance_ratio_</code> da, para cada eje nuevo, qué fracción de la varianza total conserva.",
  "code": "# PCA (Geron, Cap.8): reduce el numero de columnas (dimensiones) buscando\n# las direcciones donde los datos varian MAS, para perder la menor cantidad\n# posible de informacion real.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.decomposition import PCA\nfrom sklearn.datasets import load_iris\n\niris = load_iris()\nX = iris.data  # 150 flores, 4 columnas: largo/ancho de petalo y sepalo\nprint(\"forma ORIGINAL:\", X.shape, \"(4 columnas)\")\n\npca = PCA(n_components=2, random_state=42).fit(X)\nX2 = pca.transform(X)\nprint(\"forma REDUCIDA:\", X2.shape, \"(2 columnas)\")\n\nprint(\"\\nvarianza explicada por cada componente nuevo:\",\n      np.round(pca.explained_variance_ratio_, 4).tolist())\nprint(\"varianza TOTAL conservada con solo 2 de las 4 columnas originales:\",\n      round(pca.explained_variance_ratio_.sum(), 4))\n\nprint(\"\\nprimeras 3 flores, ANTES (4 columnas):\")\nprint(np.round(X[:3], 2).tolist())\nprint(\"primeras 3 flores, DESPUES (2 columnas):\")\nprint(np.round(X2[:3], 2).tolist())",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Componente 1",
     "Componente 2",
     "Resto (perdido)"
    ],
    "values": [
     0.9246,
     0.0531,
     0.02230000000000002
    ],
    "unit": "",
    "aria": "El primer componente principal explica 92.46% de la varianza, el segundo 5.31%, quedando solo 2.23% sin explicar"
   }
  },
  "application": "PCA es el primer paso casi obligatorio antes de visualizar datos de alta dimensión (no podés graficar 4, 20 o 500 columnas a la vez, pero sí 2 o 3 componentes principales), y también se usa para acelerar el entrenamiento de otros modelos (menos columnas = menos cómputo) y para comprimir datos (guardar solo las direcciones más informativas). En finanzas se usa para resumir cientos de indicadores económicos correlacionados en unos pocos \"factores\" reales; en genética, para reducir miles de genes a las combinaciones que más varían entre individuos (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.8)."
 },
 {
  "name": "No Supervisado · DBSCAN: agrupar por densidad",
  "theory": "K-Means agrupa por CENTROIDE: cada punto va con el centro más cercano, así que solo puede dibujar regiones más o menos redondas. DBSCAN agrupa distinto: mira la <b>densidad</b> — un punto pertenece a un grupo si tiene suficientes vecinos cerca (como gente parada junta en una plaza). Eso le permite reconocer formas raras (como dos lunas entrelazadas) que K-Means jamás podría separar bien, porque K-Means no entiende \"forma\", solo \"distancia al centro\".<br><br>En el código, con datos en forma de dos lunas (más 3 puntos sueltos y lejanos a propósito), DBSCAN recupera las dos lunas casi perfectamente (<b>ARI=1,0</b>, el máximo posible) y además identifica exactamente los 3 puntos sueltos como <b>ruido</b> (etiqueta <code>-1</code>) — ni siquiera intenta meterlos en un grupo. K-Means, forzado a 2 grupos redondos, se confunde con la forma de luna (ARI mucho más bajo) y encima mete los 3 outliers dentro de algún cluster sí o sí, porque no tiene la opción de decir \"esto no pertenece a nada\".<br><br>📐 <b>Referencia formal</b> (Géron, Cap.9): un punto es <i>core point</i> si tiene al menos <code>min_samples</code> vecinos dentro de radio <code>eps</code>; los grupos se forman conectando core points cercanos entre sí, y cualquier punto que no quede conectado a ningún grupo se etiqueta como ruido (<code>-1</code>) — a diferencia de K-Means, DBSCAN no recibe <code>k</code> como parámetro.",
  "code": "# DBSCAN (Geron, Cap.9 'Clustering'): agrupa por DENSIDAD, no por\n# distancia a un centroide -- encuentra grupos de forma arbitraria y\n# marca como 'ruido' (-1) los puntos que no pertenecen a ningun grupo\n# denso, sin que se le diga cuantos grupos (k) hay de antemano.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_moons\nfrom sklearn.cluster import DBSCAN, KMeans\nfrom sklearn.metrics import adjusted_rand_score\n\nX, y_true = make_moons(n_samples=50, noise=0.05, random_state=42)\n# le agregamos 3 outliers bien lejos del resto de proposito\noutliers = np.array([[2.5, 2.5], [-2.0, 2.0], [3.0, -1.5]])\nX2 = np.vstack([X, outliers])\n\ndb = DBSCAN(eps=0.35, min_samples=4).fit(X2)\nkm = KMeans(n_clusters=2, n_init=10, random_state=42).fit(X2)\n\nprint(\"DBSCAN -- puntos marcados como RUIDO (indices 50,51,52 son los outliers):\")\nprint(np.where(db.labels_ == -1)[0].tolist())\nn_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)\nprint(\"DBSCAN -- clusters encontrados SIN decirle k:\", n_clusters)\nprint(\"DBSCAN -- que tan bien recupera las 2 lunas reales (ARI, 1.0=perfecto):\",\n      round(adjusted_rand_score(y_true, db.labels_[:50]), 3))\n\nprint(\"\\nKMeans (k=2 fijo, sin nocion de 'ruido') -- ARI:\",\n      round(adjusted_rand_score(y_true, km.labels_[:50]), 3))\nprint(\"KMeans mete los 3 outliers en ALGUNO de los 2 clusters, no tiene otra opcion\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "DBSCAN · ARI (recupera las lunas)",
     "K-Means · ARI (fuerza 2 grupos redondos)"
    ],
    "values": [
     1.0,
     0.214
    ],
    "unit": "",
    "aria": "DBSCAN recupera perfectamente las dos lunas (ARI=1.0) mientras que K-Means, forzado a grupos redondos, solo llega a 0.214"
   }
  },
  "application": "DBSCAN es el algoritmo de elección cuando la forma de los grupos no se sabe de antemano o claramente no es redondeada: detección de anomalías en tarjetas de crédito (las transacciones fraudulentas suelen ser justamente el \"ruido\", puntos que no encajan en ningún patrón denso de gasto normal), agrupar zonas geográficas por densidad de eventos (por ejemplo, focos de un brote epidemiológico), o limpiar datos de sensores donde algunas lecturas son simplemente basura y no deberían forzarse dentro de ningún grupo — algo que K-Means no puede evitar hacer (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.9).",
  "codeAnatomy": {
   "title": "DBSCAN(eps=0.35, min_samples=4) vs KMeans(n_clusters=2)",
   "caption": "DBSCAN agrupa por densidad sin fijar cuántos grupos hay; KMeans necesita que se le diga k de antemano.",
   "lines": [
    "db = DBSCAN(eps=0.35, min_samples=4).fit(X2)",
    "km = KMeans(n_clusters=2, n_init=10, random_state=42).fit(X2)"
   ],
   "annotations": [
    {
     "line": 0,
     "text": "DBSCAN",
     "label": "Clase DBSCAN",
     "desc": "(agrupa por densidad)",
     "side": "top"
    },
    {
     "line": 0,
     "text": "eps=0.35",
     "label": "eps: radio de vecindad",
     "desc": "(distancia máxima para ser vecino)",
     "side": "top"
    },
    {
     "line": 0,
     "text": "min_samples=4",
     "label": "min_samples",
     "desc": "(vecinos mínimos para ser core point)",
     "side": "top"
    },
    {
     "line": 1,
     "text": "KMeans",
     "label": "Clase KMeans",
     "desc": "(agrupa por centroide, para comparar)",
     "side": "bottom"
    },
    {
     "line": 1,
     "text": "n_clusters=2",
     "label": "k fijo",
     "desc": "(a DBSCAN no hace falta decirle esto)",
     "side": "bottom"
    }
   ]
  }
 },
 {
  "name": "No Supervisado · DBSCAN: agrupar por densidad — pregunta 2",
  "theory": "K-Means agrupa por CENTROIDE: cada punto va con el centro más cercano, así que solo puede dibujar regiones más o menos redondas. DBSCAN agrupa distinto: mira la <b>densidad</b> — un punto pertenece a un grupo si tiene suficientes vecinos cerca (como gente parada junta en una plaza). Eso le permite reconocer formas raras (como dos lunas entrelazadas) que K-Means jamás podría separar bien, porque K-Means no entiende \"forma\", solo \"distancia al centro\".<br><br>En el código, con datos en forma de dos lunas (más 3 puntos sueltos y lejanos a propósito), DBSCAN recupera las dos lunas casi perfectamente (<b>ARI=1,0</b>, el máximo posible) y además identifica exactamente los 3 puntos sueltos como <b>ruido</b> (etiqueta <code>-1</code>) — ni siquiera intenta meterlos en un grupo. K-Means, forzado a 2 grupos redondos, se confunde con la forma de luna (ARI mucho más bajo) y encima mete los 3 outliers dentro de algún cluster sí o sí, porque no tiene la opción de decir \"esto no pertenece a nada\".<br><br>📐 <b>Referencia formal</b> (Géron, Cap.9): un punto es <i>core point</i> si tiene al menos <code>min_samples</code> vecinos dentro de radio <code>eps</code>; los grupos se forman conectando core points cercanos entre sí, y cualquier punto que no quede conectado a ningún grupo se etiqueta como ruido (<code>-1</code>) — a diferencia de K-Means, DBSCAN no recibe <code>k</code> como parámetro.",
  "code": "# DBSCAN (Geron, Cap.9 'Clustering'): agrupa por DENSIDAD, no por\n# distancia a un centroide -- encuentra grupos de forma arbitraria y\n# marca como 'ruido' (-1) los puntos que no pertenecen a ningun grupo\n# denso, sin que se le diga cuantos grupos (k) hay de antemano.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_moons\nfrom sklearn.cluster import DBSCAN, KMeans\nfrom sklearn.metrics import adjusted_rand_score\n\nX, y_true = make_moons(n_samples=50, noise=0.05, random_state=42)\n# le agregamos 3 outliers bien lejos del resto de proposito\noutliers = np.array([[2.5, 2.5], [-2.0, 2.0], [3.0, -1.5]])\nX2 = np.vstack([X, outliers])\n\ndb = DBSCAN(eps=0.35, min_samples=4).fit(X2)\nkm = KMeans(n_clusters=2, n_init=10, random_state=42).fit(X2)\n\nprint(\"DBSCAN -- puntos marcados como RUIDO (indices 50,51,52 son los outliers):\")\nprint(np.where(db.labels_ == -1)[0].tolist())\nn_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)\nprint(\"DBSCAN -- clusters encontrados SIN decirle k:\", n_clusters)\nprint(\"DBSCAN -- que tan bien recupera las 2 lunas reales (ARI, 1.0=perfecto):\",\n      round(adjusted_rand_score(y_true, db.labels_[:50]), 3))\n\nprint(\"\\nKMeans (k=2 fijo, sin nocion de 'ruido') -- ARI:\",\n      round(adjusted_rand_score(y_true, km.labels_[:50]), 3))\nprint(\"KMeans mete los 3 outliers en ALGUNO de los 2 clusters, no tiene otra opcion\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "DBSCAN · ARI (recupera las lunas)",
     "K-Means · ARI (fuerza 2 grupos redondos)"
    ],
    "values": [
     1.0,
     0.214
    ],
    "unit": "",
    "aria": "DBSCAN recupera perfectamente las dos lunas (ARI=1.0) mientras que K-Means, forzado a grupos redondos, solo llega a 0.214"
   }
  },
  "application": "DBSCAN es el algoritmo de elección cuando la forma de los grupos no se sabe de antemano o claramente no es redondeada: detección de anomalías en tarjetas de crédito (las transacciones fraudulentas suelen ser justamente el \"ruido\", puntos que no encajan en ningún patrón denso de gasto normal), agrupar zonas geográficas por densidad de eventos (por ejemplo, focos de un brote epidemiológico), o limpiar datos de sensores donde algunas lecturas son simplemente basura y no deberían forzarse dentro de ningún grupo — algo que K-Means no puede evitar hacer (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.9)."
 },
 {
  "name": "No Supervisado · DBSCAN: agrupar por densidad — pregunta 3",
  "theory": "K-Means agrupa por CENTROIDE: cada punto va con el centro más cercano, así que solo puede dibujar regiones más o menos redondas. DBSCAN agrupa distinto: mira la <b>densidad</b> — un punto pertenece a un grupo si tiene suficientes vecinos cerca (como gente parada junta en una plaza). Eso le permite reconocer formas raras (como dos lunas entrelazadas) que K-Means jamás podría separar bien, porque K-Means no entiende \"forma\", solo \"distancia al centro\".<br><br>En el código, con datos en forma de dos lunas (más 3 puntos sueltos y lejanos a propósito), DBSCAN recupera las dos lunas casi perfectamente (<b>ARI=1,0</b>, el máximo posible) y además identifica exactamente los 3 puntos sueltos como <b>ruido</b> (etiqueta <code>-1</code>) — ni siquiera intenta meterlos en un grupo. K-Means, forzado a 2 grupos redondos, se confunde con la forma de luna (ARI mucho más bajo) y encima mete los 3 outliers dentro de algún cluster sí o sí, porque no tiene la opción de decir \"esto no pertenece a nada\".<br><br>📐 <b>Referencia formal</b> (Géron, Cap.9): un punto es <i>core point</i> si tiene al menos <code>min_samples</code> vecinos dentro de radio <code>eps</code>; los grupos se forman conectando core points cercanos entre sí, y cualquier punto que no quede conectado a ningún grupo se etiqueta como ruido (<code>-1</code>) — a diferencia de K-Means, DBSCAN no recibe <code>k</code> como parámetro.",
  "code": "# DBSCAN (Geron, Cap.9 'Clustering'): agrupa por DENSIDAD, no por\n# distancia a un centroide -- encuentra grupos de forma arbitraria y\n# marca como 'ruido' (-1) los puntos que no pertenecen a ningun grupo\n# denso, sin que se le diga cuantos grupos (k) hay de antemano.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_moons\nfrom sklearn.cluster import DBSCAN, KMeans\nfrom sklearn.metrics import adjusted_rand_score\n\nX, y_true = make_moons(n_samples=50, noise=0.05, random_state=42)\n# le agregamos 3 outliers bien lejos del resto de proposito\noutliers = np.array([[2.5, 2.5], [-2.0, 2.0], [3.0, -1.5]])\nX2 = np.vstack([X, outliers])\n\ndb = DBSCAN(eps=0.35, min_samples=4).fit(X2)\nkm = KMeans(n_clusters=2, n_init=10, random_state=42).fit(X2)\n\nprint(\"DBSCAN -- puntos marcados como RUIDO (indices 50,51,52 son los outliers):\")\nprint(np.where(db.labels_ == -1)[0].tolist())\nn_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)\nprint(\"DBSCAN -- clusters encontrados SIN decirle k:\", n_clusters)\nprint(\"DBSCAN -- que tan bien recupera las 2 lunas reales (ARI, 1.0=perfecto):\",\n      round(adjusted_rand_score(y_true, db.labels_[:50]), 3))\n\nprint(\"\\nKMeans (k=2 fijo, sin nocion de 'ruido') -- ARI:\",\n      round(adjusted_rand_score(y_true, km.labels_[:50]), 3))\nprint(\"KMeans mete los 3 outliers en ALGUNO de los 2 clusters, no tiene otra opcion\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "DBSCAN · ARI (recupera las lunas)",
     "K-Means · ARI (fuerza 2 grupos redondos)"
    ],
    "values": [
     1.0,
     0.214
    ],
    "unit": "",
    "aria": "DBSCAN recupera perfectamente las dos lunas (ARI=1.0) mientras que K-Means, forzado a grupos redondos, solo llega a 0.214"
   }
  },
  "application": "DBSCAN es el algoritmo de elección cuando la forma de los grupos no se sabe de antemano o claramente no es redondeada: detección de anomalías en tarjetas de crédito (las transacciones fraudulentas suelen ser justamente el \"ruido\", puntos que no encajan en ningún patrón denso de gasto normal), agrupar zonas geográficas por densidad de eventos (por ejemplo, focos de un brote epidemiológico), o limpiar datos de sensores donde algunas lecturas son simplemente basura y no deberían forzarse dentro de ningún grupo — algo que K-Means no puede evitar hacer (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.9)."
 },
 {
  "name": "No Supervisado · DBSCAN: agrupar por densidad — pregunta 4",
  "theory": "K-Means agrupa por CENTROIDE: cada punto va con el centro más cercano, así que solo puede dibujar regiones más o menos redondas. DBSCAN agrupa distinto: mira la <b>densidad</b> — un punto pertenece a un grupo si tiene suficientes vecinos cerca (como gente parada junta en una plaza). Eso le permite reconocer formas raras (como dos lunas entrelazadas) que K-Means jamás podría separar bien, porque K-Means no entiende \"forma\", solo \"distancia al centro\".<br><br>En el código, con datos en forma de dos lunas (más 3 puntos sueltos y lejanos a propósito), DBSCAN recupera las dos lunas casi perfectamente (<b>ARI=1,0</b>, el máximo posible) y además identifica exactamente los 3 puntos sueltos como <b>ruido</b> (etiqueta <code>-1</code>) — ni siquiera intenta meterlos en un grupo. K-Means, forzado a 2 grupos redondos, se confunde con la forma de luna (ARI mucho más bajo) y encima mete los 3 outliers dentro de algún cluster sí o sí, porque no tiene la opción de decir \"esto no pertenece a nada\".<br><br>📐 <b>Referencia formal</b> (Géron, Cap.9): un punto es <i>core point</i> si tiene al menos <code>min_samples</code> vecinos dentro de radio <code>eps</code>; los grupos se forman conectando core points cercanos entre sí, y cualquier punto que no quede conectado a ningún grupo se etiqueta como ruido (<code>-1</code>) — a diferencia de K-Means, DBSCAN no recibe <code>k</code> como parámetro.",
  "code": "# DBSCAN (Geron, Cap.9 'Clustering'): agrupa por DENSIDAD, no por\n# distancia a un centroide -- encuentra grupos de forma arbitraria y\n# marca como 'ruido' (-1) los puntos que no pertenecen a ningun grupo\n# denso, sin que se le diga cuantos grupos (k) hay de antemano.\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_moons\nfrom sklearn.cluster import DBSCAN, KMeans\nfrom sklearn.metrics import adjusted_rand_score\n\nX, y_true = make_moons(n_samples=50, noise=0.05, random_state=42)\n# le agregamos 3 outliers bien lejos del resto de proposito\noutliers = np.array([[2.5, 2.5], [-2.0, 2.0], [3.0, -1.5]])\nX2 = np.vstack([X, outliers])\n\ndb = DBSCAN(eps=0.35, min_samples=4).fit(X2)\nkm = KMeans(n_clusters=2, n_init=10, random_state=42).fit(X2)\n\nprint(\"DBSCAN -- puntos marcados como RUIDO (indices 50,51,52 son los outliers):\")\nprint(np.where(db.labels_ == -1)[0].tolist())\nn_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)\nprint(\"DBSCAN -- clusters encontrados SIN decirle k:\", n_clusters)\nprint(\"DBSCAN -- que tan bien recupera las 2 lunas reales (ARI, 1.0=perfecto):\",\n      round(adjusted_rand_score(y_true, db.labels_[:50]), 3))\n\nprint(\"\\nKMeans (k=2 fijo, sin nocion de 'ruido') -- ARI:\",\n      round(adjusted_rand_score(y_true, km.labels_[:50]), 3))\nprint(\"KMeans mete los 3 outliers en ALGUNO de los 2 clusters, no tiene otra opcion\")",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "DBSCAN · ARI (recupera las lunas)",
     "K-Means · ARI (fuerza 2 grupos redondos)"
    ],
    "values": [
     1.0,
     0.214
    ],
    "unit": "",
    "aria": "DBSCAN recupera perfectamente las dos lunas (ARI=1.0) mientras que K-Means, forzado a grupos redondos, solo llega a 0.214"
   }
  },
  "application": "DBSCAN es el algoritmo de elección cuando la forma de los grupos no se sabe de antemano o claramente no es redondeada: detección de anomalías en tarjetas de crédito (las transacciones fraudulentas suelen ser justamente el \"ruido\", puntos que no encajan en ningún patrón denso de gasto normal), agrupar zonas geográficas por densidad de eventos (por ejemplo, focos de un brote epidemiológico), o limpiar datos de sensores donde algunas lecturas son simplemente basura y no deberían forzarse dentro de ningún grupo — algo que K-Means no puede evitar hacer (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.9)."
 },
 {
  "name": "No Supervisado · Mezclas Gaussianas: clustering probabilístico",
  "theory": "K-Means es un juez tajante: mira dónde estás parado y te asigna a un solo grupo, sin dudar, aunque estés justo en el límite entre dos zonas. Una <b>Mezcla Gaussiana (GMM, Gaussian Mixture Model)</b> es un juez mucho más honesto: en vez de decir \"sos 100% del grupo A\", te dice algo como \"sos 55% del grupo A y 45% del grupo B\" — reconoce la incertidumbre en vez de esconderla. Es como cuando alguien te pregunta si una fruta rara es más manzana o más pera: la respuesta honesta no es \"manzana\" a secas, es \"70% manzana, 30% pera\" — esto es lo que se llama <b>clustering blando</b> (soft clustering), a diferencia del clustering <b>duro</b> de K-Means o DBSCAN, donde cada punto va a un único grupo sí o sí.<br><br>Por dentro, GMM asume que los datos vinieron de <i>k</i> campanas de Gauss (distribuciones normales) superpuestas, cada una con su propio centro, forma/tamaño y \"peso\" (qué tan grande es ese grupo dentro del total). El algoritmo que las ajusta, Expectation-Maximization (EM), se parece a K-Means (también arranca al azar y repite pasos hasta converger) pero en cada paso no asigna cada punto a un solo grupo de una — calcula, para cada punto, qué tan probable es que haya salido de cada campana, y usa esas probabilidades (las \"responsabilidades\") para actualizar los grupos.<br><br>En el código, con 3 grupos generados a propósito con algo de superposición entre ellos, GMM encuentra pesos ≈[0,278, 0,315, 0,408] (el tercer grupo es algo más grande que los otros dos) tras converger en 9 iteraciones. Para un punto que cae justo en la zona donde dos grupos se tocan, <code>predict()</code> (la asignación dura) dice simplemente \"grupo 1\" — pero <code>predict_proba()</code> revela la verdad completa: 57,5% de probabilidad de grupo 1, 42,5% de grupo 2, 0% de grupo 0. K-Means, sobre ese mismo punto, también dice \"grupo 1\" — pero ni siquiera TIENE un método <code>predict_proba()</code>: nunca podría haber dicho \"44,71%\", porque para K-Means esa noción de probabilidad de pertenencia directamente no existe.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.9, p.286): GMM asume que cada instancia $x^{(i)}$ se generó eligiendo primero un grupo $j$ al azar (con probabilidad $\\phi^{(j)}$, el peso de ese grupo) y luego muestreando $x^{(i)} \\sim \\mathcal{N}(\\mu^{(j)}, \\Sigma^{(j)})$ — el método <code>predict_proba()</code> devuelve, para cada punto, esa probabilidad posterior (la <i>responsabilidad</i>) de haber sido generado por cada uno de los $k$ grupos.",
  "code": "# Mezclas Gaussianas / GMM (Geron, Cap.9 \"Gaussian Mixtures\", p.286): a\n# diferencia de K-Means (asignacion DURA, un solo grupo por punto), GMM hace\n# clustering PROBABILISTICO -- para cada punto estima la PROBABILIDAD de\n# pertenecer a cada uno de los k grupos (asignacion BLANDA / soft clustering).\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_blobs\nfrom sklearn.mixture import GaussianMixture\nfrom sklearn.cluster import KMeans\n\nX, y_true = make_blobs(n_samples=40, centers=[[0,0],[2.6,0],[0,3.6]], cluster_std=1.0, random_state=2)\n\ngm = GaussianMixture(n_components=3, n_init=1, random_state=42).fit(X)\nkm = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)\n\nprint(\"pesos de cada grupo (weights_, cuanto pesa cada Gaussiana):\", np.round(gm.weights_, 3).tolist())\nprint(\"convergio:\", gm.converged_, \"-- en\", gm.n_iter_, \"iteraciones (EM: expectation-maximization)\")\n\n# Elegimos un punto que cae justo en la zona donde dos grupos se superponen.\nidx = 35\npunto = X[[idx]]\nprint()\nprint(\"punto elegido:\", np.round(punto[0], 2).tolist())\nprint(\"GMM predict() -- asignacion DURA, el grupo mas probable:\", gm.predict(punto).tolist())\nproba = gm.predict_proba(punto)[0]\nprint(\"GMM predict_proba() -- probabilidad de CADA uno de los 3 grupos:\", np.round(proba, 4).tolist())\nprint(\"las 3 probabilidades suman 1.0:\", round(proba.sum(), 4))\nprint()\nprint(\"KMeans predict() en el MISMO punto -- tambien asignacion dura:\", km.predict(punto).tolist())\nprint(\"KMeans no tiene predict_proba(): no existe la nocion de porcentaje de pertenencia\")\n",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Grupo 0 (prob.)",
     "Grupo 1 (prob.)",
     "Grupo 2 (prob.)"
    ],
    "values": [
     0.0,
     0.5529,
     0.4471
    ],
    "unit": "",
    "aria": "Para el punto elegido, GMM reparte la probabilidad entre el grupo 1 (55.29%) y el grupo 2 (44.71%), en vez de forzar un 100% a un solo grupo como haria K-Means"
   }
  },
  "application": "Las Mezclas Gaussianas se usan en cualquier contexto donde forzar una etiqueta única sea una simplificación excesiva: en reconocimiento de voz y biometría, cada instante de audio puede describirse como una mezcla de sonidos en vez de encasillarlo en un único fonema; en segmentación de imágenes médicas, un píxel en el borde de un tumor puede tener 60% de probabilidad de ser tejido enfermo y 40% de ser tejido sano, información mucho más útil para un diagnóstico que un \"sí/no\" tajante. GMM también es un modelo <i>generativo</i> (se pueden generar puntos nuevos con <code>sample()</code>) y sirve para <b>detección de anomalías</b> (Géron, Cap.9, \"Anomaly Detection using Gaussian Mixtures\", p.291): cualquier instancia que caiga en una región de muy baja densidad según el modelo (medida con <code>score_samples()</code>) se puede marcar como posible fraude bancario o defecto de fabricación, fijando un umbral de densidad (por ejemplo, el percentil 4 más bajo) en vez de una regla rígida escrita a mano (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.9).",
  "codeAnatomy": {
   "title": "predict() vs predict_proba()",
   "caption": "Sobre el mismo punto, predict() da un único grupo pero predict_proba() revela la probabilidad de pertenecer a cada uno de los 3 grupos.",
   "lines": [
    "print(\"GMM predict() -- asignacion DURA, el grupo mas probable:\", gm.predict(punto).tolist())",
    "proba = gm.predict_proba(punto)[0]",
    "print(\"GMM predict_proba() -- probabilidad de CADA uno de los 3 grupos:\", np.round(proba, 4).tolist())"
   ],
   "annotations": [
    {
     "line": 0,
     "text": "gm.predict(punto)",
     "label": "predict()",
     "desc": "(asignación dura: un solo grupo)",
     "side": "top"
    },
    {
     "line": 1,
     "text": "gm.predict_proba(punto)",
     "label": "predict_proba()",
     "desc": "(probabilidad de cada grupo, asignación blanda)",
     "side": "top"
    },
    {
     "line": 1,
     "text": "[0]",
     "label": "Primera fila",
     "desc": "(el resultado para ese único punto)",
     "side": "bottom"
    },
    {
     "line": 2,
     "text": "3 grupos",
     "label": "k=3 grupos",
     "desc": "(las probabilidades de pertenecer a cada uno)",
     "side": "bottom"
    },
    {
     "line": 2,
     "text": "np.round(proba, 4)",
     "label": "Redondea",
     "desc": "(a 4 decimales, para imprimir)",
     "side": "bottom"
    }
   ]
  }
 },
 {
  "name": "No Supervisado · Mezclas Gaussianas: clustering probabilístico — pregunta 2",
  "theory": "K-Means es un juez tajante: mira dónde estás parado y te asigna a un solo grupo, sin dudar, aunque estés justo en el límite entre dos zonas. Una <b>Mezcla Gaussiana (GMM, Gaussian Mixture Model)</b> es un juez mucho más honesto: en vez de decir \"sos 100% del grupo A\", te dice algo como \"sos 55% del grupo A y 45% del grupo B\" — reconoce la incertidumbre en vez de esconderla. Es como cuando alguien te pregunta si una fruta rara es más manzana o más pera: la respuesta honesta no es \"manzana\" a secas, es \"70% manzana, 30% pera\" — esto es lo que se llama <b>clustering blando</b> (soft clustering), a diferencia del clustering <b>duro</b> de K-Means o DBSCAN, donde cada punto va a un único grupo sí o sí.<br><br>Por dentro, GMM asume que los datos vinieron de <i>k</i> campanas de Gauss (distribuciones normales) superpuestas, cada una con su propio centro, forma/tamaño y \"peso\" (qué tan grande es ese grupo dentro del total). El algoritmo que las ajusta, Expectation-Maximization (EM), se parece a K-Means (también arranca al azar y repite pasos hasta converger) pero en cada paso no asigna cada punto a un solo grupo de una — calcula, para cada punto, qué tan probable es que haya salido de cada campana, y usa esas probabilidades (las \"responsabilidades\") para actualizar los grupos.<br><br>En el código, con 3 grupos generados a propósito con algo de superposición entre ellos, GMM encuentra pesos ≈[0,278, 0,315, 0,408] (el tercer grupo es algo más grande que los otros dos) tras converger en 9 iteraciones. Para un punto que cae justo en la zona donde dos grupos se tocan, <code>predict()</code> (la asignación dura) dice simplemente \"grupo 1\" — pero <code>predict_proba()</code> revela la verdad completa: 57,5% de probabilidad de grupo 1, 42,5% de grupo 2, 0% de grupo 0. K-Means, sobre ese mismo punto, también dice \"grupo 1\" — pero ni siquiera TIENE un método <code>predict_proba()</code>: nunca podría haber dicho \"44,71%\", porque para K-Means esa noción de probabilidad de pertenencia directamente no existe.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.9, p.286): GMM asume que cada instancia $x^{(i)}$ se generó eligiendo primero un grupo $j$ al azar (con probabilidad $\\phi^{(j)}$, el peso de ese grupo) y luego muestreando $x^{(i)} \\sim \\mathcal{N}(\\mu^{(j)}, \\Sigma^{(j)})$ — el método <code>predict_proba()</code> devuelve, para cada punto, esa probabilidad posterior (la <i>responsabilidad</i>) de haber sido generado por cada uno de los $k$ grupos.",
  "code": "# Mezclas Gaussianas / GMM (Geron, Cap.9 \"Gaussian Mixtures\", p.286): a\n# diferencia de K-Means (asignacion DURA, un solo grupo por punto), GMM hace\n# clustering PROBABILISTICO -- para cada punto estima la PROBABILIDAD de\n# pertenecer a cada uno de los k grupos (asignacion BLANDA / soft clustering).\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_blobs\nfrom sklearn.mixture import GaussianMixture\nfrom sklearn.cluster import KMeans\n\nX, y_true = make_blobs(n_samples=40, centers=[[0,0],[2.6,0],[0,3.6]], cluster_std=1.0, random_state=2)\n\ngm = GaussianMixture(n_components=3, n_init=1, random_state=42).fit(X)\nkm = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)\n\nprint(\"pesos de cada grupo (weights_, cuanto pesa cada Gaussiana):\", np.round(gm.weights_, 3).tolist())\nprint(\"convergio:\", gm.converged_, \"-- en\", gm.n_iter_, \"iteraciones (EM: expectation-maximization)\")\n\n# Elegimos un punto que cae justo en la zona donde dos grupos se superponen.\nidx = 35\npunto = X[[idx]]\nprint()\nprint(\"punto elegido:\", np.round(punto[0], 2).tolist())\nprint(\"GMM predict() -- asignacion DURA, el grupo mas probable:\", gm.predict(punto).tolist())\nproba = gm.predict_proba(punto)[0]\nprint(\"GMM predict_proba() -- probabilidad de CADA uno de los 3 grupos:\", np.round(proba, 4).tolist())\nprint(\"las 3 probabilidades suman 1.0:\", round(proba.sum(), 4))\nprint()\nprint(\"KMeans predict() en el MISMO punto -- tambien asignacion dura:\", km.predict(punto).tolist())\nprint(\"KMeans no tiene predict_proba(): no existe la nocion de porcentaje de pertenencia\")\n",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Grupo 0 (prob.)",
     "Grupo 1 (prob.)",
     "Grupo 2 (prob.)"
    ],
    "values": [
     0.0,
     0.5529,
     0.4471
    ],
    "unit": "",
    "aria": "Para el punto elegido, GMM reparte la probabilidad entre el grupo 1 (55.29%) y el grupo 2 (44.71%), en vez de forzar un 100% a un solo grupo como haria K-Means"
   }
  },
  "application": "Las Mezclas Gaussianas se usan en cualquier contexto donde forzar una etiqueta única sea una simplificación excesiva: en reconocimiento de voz y biometría, cada instante de audio puede describirse como una mezcla de sonidos en vez de encasillarlo en un único fonema; en segmentación de imágenes médicas, un píxel en el borde de un tumor puede tener 60% de probabilidad de ser tejido enfermo y 40% de ser tejido sano, información mucho más útil para un diagnóstico que un \"sí/no\" tajante. GMM también es un modelo <i>generativo</i> (se pueden generar puntos nuevos con <code>sample()</code>) y sirve para <b>detección de anomalías</b> (Géron, Cap.9, \"Anomaly Detection using Gaussian Mixtures\", p.291): cualquier instancia que caiga en una región de muy baja densidad según el modelo (medida con <code>score_samples()</code>) se puede marcar como posible fraude bancario o defecto de fabricación, fijando un umbral de densidad (por ejemplo, el percentil 4 más bajo) en vez de una regla rígida escrita a mano (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.9)."
 },
 {
  "name": "No Supervisado · Mezclas Gaussianas: clustering probabilístico — pregunta 3",
  "theory": "K-Means es un juez tajante: mira dónde estás parado y te asigna a un solo grupo, sin dudar, aunque estés justo en el límite entre dos zonas. Una <b>Mezcla Gaussiana (GMM, Gaussian Mixture Model)</b> es un juez mucho más honesto: en vez de decir \"sos 100% del grupo A\", te dice algo como \"sos 55% del grupo A y 45% del grupo B\" — reconoce la incertidumbre en vez de esconderla. Es como cuando alguien te pregunta si una fruta rara es más manzana o más pera: la respuesta honesta no es \"manzana\" a secas, es \"70% manzana, 30% pera\" — esto es lo que se llama <b>clustering blando</b> (soft clustering), a diferencia del clustering <b>duro</b> de K-Means o DBSCAN, donde cada punto va a un único grupo sí o sí.<br><br>Por dentro, GMM asume que los datos vinieron de <i>k</i> campanas de Gauss (distribuciones normales) superpuestas, cada una con su propio centro, forma/tamaño y \"peso\" (qué tan grande es ese grupo dentro del total). El algoritmo que las ajusta, Expectation-Maximization (EM), se parece a K-Means (también arranca al azar y repite pasos hasta converger) pero en cada paso no asigna cada punto a un solo grupo de una — calcula, para cada punto, qué tan probable es que haya salido de cada campana, y usa esas probabilidades (las \"responsabilidades\") para actualizar los grupos.<br><br>En el código, con 3 grupos generados a propósito con algo de superposición entre ellos, GMM encuentra pesos ≈[0,278, 0,315, 0,408] (el tercer grupo es algo más grande que los otros dos) tras converger en 9 iteraciones. Para un punto que cae justo en la zona donde dos grupos se tocan, <code>predict()</code> (la asignación dura) dice simplemente \"grupo 1\" — pero <code>predict_proba()</code> revela la verdad completa: 57,5% de probabilidad de grupo 1, 42,5% de grupo 2, 0% de grupo 0. K-Means, sobre ese mismo punto, también dice \"grupo 1\" — pero ni siquiera TIENE un método <code>predict_proba()</code>: nunca podría haber dicho \"44,71%\", porque para K-Means esa noción de probabilidad de pertenencia directamente no existe.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.9, p.286): GMM asume que cada instancia $x^{(i)}$ se generó eligiendo primero un grupo $j$ al azar (con probabilidad $\\phi^{(j)}$, el peso de ese grupo) y luego muestreando $x^{(i)} \\sim \\mathcal{N}(\\mu^{(j)}, \\Sigma^{(j)})$ — el método <code>predict_proba()</code> devuelve, para cada punto, esa probabilidad posterior (la <i>responsabilidad</i>) de haber sido generado por cada uno de los $k$ grupos.",
  "code": "# Mezclas Gaussianas / GMM (Geron, Cap.9 \"Gaussian Mixtures\", p.286): a\n# diferencia de K-Means (asignacion DURA, un solo grupo por punto), GMM hace\n# clustering PROBABILISTICO -- para cada punto estima la PROBABILIDAD de\n# pertenecer a cada uno de los k grupos (asignacion BLANDA / soft clustering).\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_blobs\nfrom sklearn.mixture import GaussianMixture\nfrom sklearn.cluster import KMeans\n\nX, y_true = make_blobs(n_samples=40, centers=[[0,0],[2.6,0],[0,3.6]], cluster_std=1.0, random_state=2)\n\ngm = GaussianMixture(n_components=3, n_init=1, random_state=42).fit(X)\nkm = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)\n\nprint(\"pesos de cada grupo (weights_, cuanto pesa cada Gaussiana):\", np.round(gm.weights_, 3).tolist())\nprint(\"convergio:\", gm.converged_, \"-- en\", gm.n_iter_, \"iteraciones (EM: expectation-maximization)\")\n\n# Elegimos un punto que cae justo en la zona donde dos grupos se superponen.\nidx = 35\npunto = X[[idx]]\nprint()\nprint(\"punto elegido:\", np.round(punto[0], 2).tolist())\nprint(\"GMM predict() -- asignacion DURA, el grupo mas probable:\", gm.predict(punto).tolist())\nproba = gm.predict_proba(punto)[0]\nprint(\"GMM predict_proba() -- probabilidad de CADA uno de los 3 grupos:\", np.round(proba, 4).tolist())\nprint(\"las 3 probabilidades suman 1.0:\", round(proba.sum(), 4))\nprint()\nprint(\"KMeans predict() en el MISMO punto -- tambien asignacion dura:\", km.predict(punto).tolist())\nprint(\"KMeans no tiene predict_proba(): no existe la nocion de porcentaje de pertenencia\")\n",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Grupo 0 (prob.)",
     "Grupo 1 (prob.)",
     "Grupo 2 (prob.)"
    ],
    "values": [
     0.0,
     0.5529,
     0.4471
    ],
    "unit": "",
    "aria": "Para el punto elegido, GMM reparte la probabilidad entre el grupo 1 (55.29%) y el grupo 2 (44.71%), en vez de forzar un 100% a un solo grupo como haria K-Means"
   }
  },
  "application": "Las Mezclas Gaussianas se usan en cualquier contexto donde forzar una etiqueta única sea una simplificación excesiva: en reconocimiento de voz y biometría, cada instante de audio puede describirse como una mezcla de sonidos en vez de encasillarlo en un único fonema; en segmentación de imágenes médicas, un píxel en el borde de un tumor puede tener 60% de probabilidad de ser tejido enfermo y 40% de ser tejido sano, información mucho más útil para un diagnóstico que un \"sí/no\" tajante. GMM también es un modelo <i>generativo</i> (se pueden generar puntos nuevos con <code>sample()</code>) y sirve para <b>detección de anomalías</b> (Géron, Cap.9, \"Anomaly Detection using Gaussian Mixtures\", p.291): cualquier instancia que caiga en una región de muy baja densidad según el modelo (medida con <code>score_samples()</code>) se puede marcar como posible fraude bancario o defecto de fabricación, fijando un umbral de densidad (por ejemplo, el percentil 4 más bajo) en vez de una regla rígida escrita a mano (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.9)."
 },
 {
  "name": "No Supervisado · Mezclas Gaussianas: clustering probabilístico — pregunta 4",
  "theory": "K-Means es un juez tajante: mira dónde estás parado y te asigna a un solo grupo, sin dudar, aunque estés justo en el límite entre dos zonas. Una <b>Mezcla Gaussiana (GMM, Gaussian Mixture Model)</b> es un juez mucho más honesto: en vez de decir \"sos 100% del grupo A\", te dice algo como \"sos 55% del grupo A y 45% del grupo B\" — reconoce la incertidumbre en vez de esconderla. Es como cuando alguien te pregunta si una fruta rara es más manzana o más pera: la respuesta honesta no es \"manzana\" a secas, es \"70% manzana, 30% pera\" — esto es lo que se llama <b>clustering blando</b> (soft clustering), a diferencia del clustering <b>duro</b> de K-Means o DBSCAN, donde cada punto va a un único grupo sí o sí.<br><br>Por dentro, GMM asume que los datos vinieron de <i>k</i> campanas de Gauss (distribuciones normales) superpuestas, cada una con su propio centro, forma/tamaño y \"peso\" (qué tan grande es ese grupo dentro del total). El algoritmo que las ajusta, Expectation-Maximization (EM), se parece a K-Means (también arranca al azar y repite pasos hasta converger) pero en cada paso no asigna cada punto a un solo grupo de una — calcula, para cada punto, qué tan probable es que haya salido de cada campana, y usa esas probabilidades (las \"responsabilidades\") para actualizar los grupos.<br><br>En el código, con 3 grupos generados a propósito con algo de superposición entre ellos, GMM encuentra pesos ≈[0,278, 0,315, 0,408] (el tercer grupo es algo más grande que los otros dos) tras converger en 9 iteraciones. Para un punto que cae justo en la zona donde dos grupos se tocan, <code>predict()</code> (la asignación dura) dice simplemente \"grupo 1\" — pero <code>predict_proba()</code> revela la verdad completa: 57,5% de probabilidad de grupo 1, 42,5% de grupo 2, 0% de grupo 0. K-Means, sobre ese mismo punto, también dice \"grupo 1\" — pero ni siquiera TIENE un método <code>predict_proba()</code>: nunca podría haber dicho \"44,71%\", porque para K-Means esa noción de probabilidad de pertenencia directamente no existe.<br><br>📐 <b>Referencia formal</b> (Géron, Cap.9, p.286): GMM asume que cada instancia $x^{(i)}$ se generó eligiendo primero un grupo $j$ al azar (con probabilidad $\\phi^{(j)}$, el peso de ese grupo) y luego muestreando $x^{(i)} \\sim \\mathcal{N}(\\mu^{(j)}, \\Sigma^{(j)})$ — el método <code>predict_proba()</code> devuelve, para cada punto, esa probabilidad posterior (la <i>responsabilidad</i>) de haber sido generado por cada uno de los $k$ grupos.",
  "code": "# Mezclas Gaussianas / GMM (Geron, Cap.9 \"Gaussian Mixtures\", p.286): a\n# diferencia de K-Means (asignacion DURA, un solo grupo por punto), GMM hace\n# clustering PROBABILISTICO -- para cada punto estima la PROBABILIDAD de\n# pertenecer a cada uno de los k grupos (asignacion BLANDA / soft clustering).\nimport warnings; warnings.filterwarnings('ignore')\nimport numpy as np\nfrom sklearn.datasets import make_blobs\nfrom sklearn.mixture import GaussianMixture\nfrom sklearn.cluster import KMeans\n\nX, y_true = make_blobs(n_samples=40, centers=[[0,0],[2.6,0],[0,3.6]], cluster_std=1.0, random_state=2)\n\ngm = GaussianMixture(n_components=3, n_init=1, random_state=42).fit(X)\nkm = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)\n\nprint(\"pesos de cada grupo (weights_, cuanto pesa cada Gaussiana):\", np.round(gm.weights_, 3).tolist())\nprint(\"convergio:\", gm.converged_, \"-- en\", gm.n_iter_, \"iteraciones (EM: expectation-maximization)\")\n\n# Elegimos un punto que cae justo en la zona donde dos grupos se superponen.\nidx = 35\npunto = X[[idx]]\nprint()\nprint(\"punto elegido:\", np.round(punto[0], 2).tolist())\nprint(\"GMM predict() -- asignacion DURA, el grupo mas probable:\", gm.predict(punto).tolist())\nproba = gm.predict_proba(punto)[0]\nprint(\"GMM predict_proba() -- probabilidad de CADA uno de los 3 grupos:\", np.round(proba, 4).tolist())\nprint(\"las 3 probabilidades suman 1.0:\", round(proba.sum(), 4))\nprint()\nprint(\"KMeans predict() en el MISMO punto -- tambien asignacion dura:\", km.predict(punto).tolist())\nprint(\"KMeans no tiene predict_proba(): no existe la nocion de porcentaje de pertenencia\")\n",
  "viz": {
   "type": "bar",
   "data": {
    "labels": [
     "Grupo 0 (prob.)",
     "Grupo 1 (prob.)",
     "Grupo 2 (prob.)"
    ],
    "values": [
     0.0,
     0.5529,
     0.4471
    ],
    "unit": "",
    "aria": "Para el punto elegido, GMM reparte la probabilidad entre el grupo 1 (55.29%) y el grupo 2 (44.71%), en vez de forzar un 100% a un solo grupo como haria K-Means"
   }
  },
  "application": "Las Mezclas Gaussianas se usan en cualquier contexto donde forzar una etiqueta única sea una simplificación excesiva: en reconocimiento de voz y biometría, cada instante de audio puede describirse como una mezcla de sonidos en vez de encasillarlo en un único fonema; en segmentación de imágenes médicas, un píxel en el borde de un tumor puede tener 60% de probabilidad de ser tejido enfermo y 40% de ser tejido sano, información mucho más útil para un diagnóstico que un \"sí/no\" tajante. GMM también es un modelo <i>generativo</i> (se pueden generar puntos nuevos con <code>sample()</code>) y sirve para <b>detección de anomalías</b> (Géron, Cap.9, \"Anomaly Detection using Gaussian Mixtures\", p.291): cualquier instancia que caiga en una región de muy baja densidad según el modelo (medida con <code>score_samples()</code>) se puede marcar como posible fraude bancario o defecto de fabricación, fijando un umbral de densidad (por ejemplo, el percentil 4 más bajo) en vez de una regla rígida escrita a mano (Géron, <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i> (O'Reilly, 2019), Cap.9)."
 }
];

/* ──────────── Preguntas de práctica del Modo Maestro NS (superaprendizaje) ────
   Array PARALELO a EX_NS por índice, mismo mecanismo de practice-testing +
   feedback inmediato que AO/Matemáticas/RA/AS -- cada pregunta se fundamenta
   en el propio código/fórmula de ESE tema, verificado ejecutando realmente
   el código antes de fijar la respuesta correcta. */
const NS_QUIZ = [
 [
  {
   "question": "En el código, ¿qué datos recibe el algoritmo de clustering al llamar fit()?",
   "type": "mc",
   "options": [
    "Solo X (las coordenadas de los puntos) — y_true nunca se le pasa",
    "X e y_true juntos, igual que en aprendizaje supervisado",
    "Solo y_true, sin las coordenadas",
    "Ninguno de los dos: el algoritmo genera sus propios datos"
   ],
   "correct": 0,
   "solution": "El código llama a KMeans().fit(X) — un solo argumento. y_true existe en el dataset solo para que nosotros podamos verificar el resultado después (con adjusted_rand_score, por ejemplo), pero el algoritmo nunca la recibe como entrada.",
   "whyNot": [
    null,
    "Eso describe fit(X, y) del aprendizaje SUPERVISADO (como en el Modo Maestro AS) — la diferencia de fondo con no supervisado es justamente que aquí no hay ningún 'y' de entrada.",
    "y_true no sirve como ENTRADA del algoritmo — solo se usa después, aparte, para comprobar qué tan bien agrupó (una métrica de evaluación, no un dato de entrenamiento).",
    "El algoritmo sí recibe datos reales: X, las 30 coordenadas generadas por make_blobs — sin X no tendría nada que agrupar."
   ],
   "steps": [
    "Mirá la línea que llama al algoritmo: KMeans().fit(X) — un solo argumento entre paréntesis.",
    "Comparalo con cómo se entrena un modelo supervisado: ahí siempre hay dos argumentos, fit(X, y).",
    "y_true existe en el dataset (viene de make_blobs), pero nunca aparece dentro de fit() — solo se usa después, aparte, para comparar.",
    "Por eso la respuesta es: el algoritmo recibe solo X, nunca y_true."
   ],
   "stakes": "En un pipeline real, pasarle accidentalmente el y (target) a un algoritmo de clustering — por copiar código de un proyecto supervisado — hace que los resultados parezcan buenos en el desarrollo pero fallen en producción, porque el modelo real nunca vería esas etiquetas."
  },
  {
   "question": "Según la advertencia del código (STAKES), ¿qué riesgo real se corre si un pipeline de clustering termina dependiendo, aunque sea indirectamente, de la variable y_true durante el desarrollo?",
   "type": "mc",
   "options": [
    "Que el modelo parezca funcionar bien en desarrollo pero falle en producción, porque en un caso real nunca vas a tener esa etiqueta disponible para el algoritmo",
    "Que el algoritmo tarde más tiempo en converger, aunque el resultado final sea idéntico",
    "Que aparezca un error de sintaxis al ejecutar el código",
    "Que se necesiten más columnas en el dataset para compensar"
   ],
   "correct": 0,
   "solution": "El propio ejemplo advierte sobre esto: si un pipeline de clustering llega a depender de y_true (por ejemplo, copiando patrones de un proyecto supervisado), el resultado puede verse bien mientras se desarrolla con datos donde 'la respuesta' está disponible por conveniencia, pero fallar en producción, donde esa etiqueta simplemente no existe para el algoritmo.",
   "whyNot": [
    null,
    "No es un problema de velocidad de cómputo — es un problema de qué información asume disponible el pipeline, algo que no se resuelve ni empeora con el tiempo de convergencia.",
    "El código en sí puede ejecutarse sin errores de sintaxis — el problema es conceptual/de diseño, no algo que Python detecte al correr.",
    "El número de columnas del dataset no tiene relación con este riesgo — el problema es asumir una etiqueta que en producción no existirá, sin importar cuántas columnas tenga X."
   ],
   "steps": [
    "Pensá en cómo se construye un pipeline real: durante el desarrollo, a veces hay datos 'de más' (como y_true) disponibles solo porque son sintéticos o de prueba.",
    "Si el pipeline termina apoyándose en esa información extra, sus resultados en desarrollo van a parecer mejores de lo que realmente son.",
    "En producción, esa etiqueta extra no va a existir — el algoritmo se enfrenta solo a X, como debe ser en un problema no supervisado real.",
    "Por eso la dependencia oculta de y_true es un riesgo real, no solo un detalle técnico del código de ejemplo."
   ],
   "stakes": "Este es un tipo de bug real llamado 'data leakage': un pipeline que en el laboratorio parece funcionar de maravilla pero se derrumba al llegar a producción, porque dependía silenciosamente de información que ahí no existe."
  }
 ],
 [
  {
   "question": "¿Cuál es la diferencia de fondo entre aprendizaje supervisado y no supervisado, según el código y la teoría?",
   "type": "mc",
   "options": [
    "Supervisado tiene una respuesta correcta (y) que imitar; no supervisado solo tiene datos (X) y debe encontrar estructura por su cuenta",
    "No supervisado es simplemente una versión más rápida de calcular del aprendizaje supervisado",
    "Supervisado nunca usa datos numéricos, solo texto",
    "No supervisado requiere siempre más datos que el supervisado para funcionar"
   ],
   "correct": 0,
   "solution": "Supervisado aprende a partir de pares (X,y) — hay una respuesta correcta que copiar. No supervisado solo tiene X: no hay ninguna respuesta 'correcta' etiquetada, el algoritmo tiene que descubrir la estructura (grupos, patrones) por sí mismo.",
   "whyNot": [
    null,
    "No es una cuestión de velocidad de cómputo — es un problema conceptualmente distinto: sin etiquetas no hay nada que 'predecir correctamente', solo estructura que descubrir.",
    "Ambos tipos de aprendizaje trabajan típicamente con datos numéricos (como en el ejemplo, coordenadas X) — el tipo de dato no es lo que los distingue.",
    "La cantidad de datos necesarios no es la diferencia definitoria entre ambos — la diferencia es si existen o no etiquetas y de entrada durante el entrenamiento."
   ],
   "steps": [
    "Preguntate: ¿el código usa alguna 'respuesta correcta' (y) durante el entrenamiento?",
    "En el ejemplo no supervisado, fit() solo recibe X — no hay ningún 'y' que el modelo intente imitar.",
    "Eso significa que el algoritmo tiene que encontrar la estructura (grupos) por su cuenta, sin que nadie le diga de antemano cuál es la respuesta correcta.",
    "Esa es exactamente la diferencia de fondo entre los dos tipos de aprendizaje."
   ],
   "stakes": "Confundir estos dos enfoques en un proyecto real (por ejemplo, buscar un dataset etiquetado que no existe para un problema de segmentación de clientes) puede hacer perder semanas antes de darse cuenta de que el problema en realidad pedía no supervisado."
  },
  {
   "question": "Según los ejemplos de aplicación real, ¿por qué comprimir imágenes o agrupar genes en bioinformática son casos típicos de aprendizaje NO supervisado?",
   "type": "mc",
   "options": [
    "Porque hay muchísimos datos disponibles (píxeles, genes) pero ninguna respuesta 'correcta' pre-etiquetada que indique cómo agruparlos de antemano",
    "Porque las imágenes y los genes son datos demasiado simples para necesitar aprendizaje supervisado",
    "Porque no existen suficientes datos para entrenar un modelo supervisado en esos dominios",
    "Porque ese tipo de datos no se puede representar con números"
   ],
   "correct": 0,
   "solution": "El propio ejemplo de aplicación lo dice explícitamente: comprimir imágenes o agrupar genes son casos donde 'hay datos de sobra, pero ninguna respuesta correcta pre-etiquetada' — nadie etiquetó de antemano a qué grupo pertenece cada gen o cada patrón de píxeles, así que no supervisado es el enfoque natural.",
   "whyNot": [
    null,
    "La complejidad de los datos no es el criterio — de hecho estos son dominios con datos MUY complejos (miles de genes, millones de píxeles); la razón real es la ausencia de etiquetas, no la simplicidad.",
    "Es justo lo contrario: estos dominios tienen datos DE SOBRA (imágenes, genomas) — el problema no es la cantidad de datos, sino la falta de etiquetas correctas para entrenar de forma supervisada.",
    "Tanto los píxeles de una imagen como las mediciones genéticas se representan perfectamente como números — eso no es ninguna limitación en estos ejemplos."
   ],
   "steps": [
    "Fijate qué tienen en común compresión de imágenes y agrupamiento de genes: enormes cantidades de datos numéricos disponibles.",
    "Ahora fijate qué les falta: ninguna etiqueta 'correcta' que diga de antemano cómo agrupar esos píxeles o genes.",
    "Datos de sobra + sin respuesta correcta pre-etiquetada = exactamente la definición de un problema no supervisado.",
    "Por eso estos son ejemplos típicos citados en la aplicación real del tema."
   ],
   "stakes": "En bioinformática real, esperar a tener genes 'etiquetados a mano' antes de analizarlos sería inviable — por eso el clustering no supervisado es una herramienta estándar para explorar datos genómicos nuevos."
  }
 ],
 [
  {
   "question": "La variable y_true existe en el código (viene de make_blobs). ¿Para qué se usa realmente?",
   "type": "mc",
   "options": [
    "Solo para que nosotros, humanos, podamos comprobar después qué tan bien agrupó el algoritmo — nunca se le pasa al algoritmo",
    "Para acelerar el entrenamiento del algoritmo de clustering",
    "Para decirle al algoritmo a qué grupo debe asignar cada punto",
    "Para generar más puntos automáticamente durante el entrenamiento"
   ],
   "correct": 0,
   "solution": "y_true es una etiqueta 'de verdad' que make_blobs genera para que el desarrollador pueda verificar el resultado (por ejemplo, comparándola con las etiquetas que asignó KMeans). El propio código lo aclara explícitamente: 'el algoritmo de clustering NUNCA la recibe como entrada'.",
   "whyNot": [
    null,
    "y_true no participa del cálculo de KMeans en absoluto — no acelera nada, ni siquiera se le pasa a fit().",
    "Es justo lo contrario: en clustering NADIE le dice al algoritmo a qué grupo va cada punto — esa es la definición misma de 'no supervisado', y precisamente por eso y_true queda fuera del entrenamiento.",
    "make_blobs genera los 30 puntos de una sola vez, antes de cualquier entrenamiento — y_true no interviene en generar datos nuevos."
   ],
   "steps": [
    "Fijate de dónde sale y_true: lo genera make_blobs junto con X, como una etiqueta 'de verdad' conocida solo porque los datos son sintéticos.",
    "Buscá dónde se USA y_true en el código: no aparece dentro de fit(), aparece después, comparándola con las etiquetas que asignó el algoritmo.",
    "Esa comparación es para que el humano evalúe qué tan bien agrupó el modelo — el algoritmo mismo nunca la ve.",
    "Por eso y_true sirve solo para verificar, no para entrenar."
   ],
   "stakes": "Confundir una columna 'de verificación' con un dato de entrenamiento válido es justo el tipo de error que produce data leakage en un proyecto real: información que en producción NUNCA vas a tener disponible, contaminando el modelo de forma difícil de detectar."
  },
  {
   "question": "La solución de otra pregunta de este tema menciona que y_true se podría usar después 'con adjusted_rand_score, por ejemplo'. ¿Qué tipo de herramienta es adjusted_rand_score en este contexto?",
   "type": "mc",
   "options": [
    "Una métrica de evaluación que compara, DESPUÉS del entrenamiento, las etiquetas que asignó el algoritmo contra y_true — no algo que el algoritmo use para entrenar",
    "Un algoritmo de clustering alternativo a KMeans",
    "Un parámetro que se le pasa a make_blobs para generar más puntos",
    "Una función que reemplaza a fit() para entrenar el modelo más rápido"
   ],
   "correct": 0,
   "solution": "adjusted_rand_score se menciona como ejemplo de cómo, DESPUÉS de que el algoritmo ya agrupó los datos (sin haber visto y_true), un humano puede comparar esas etiquetas resultantes contra y_true para medir qué tan bien agrupó. Es una métrica de evaluación externa, no una entrada del entrenamiento.",
   "whyNot": [
    null,
    "adjusted_rand_score no agrupa nada — no reemplaza a KMeans ni a ningún otro algoritmo de clustering, solo compara dos conjuntos de etiquetas ya existentes.",
    "No tiene relación con make_blobs ni con la generación de puntos — se usa después de que los puntos y las etiquetas del algoritmo ya existen.",
    "No entrena ni reemplaza a fit() — se calcula después de fit(), comparando resultados, no durante el entrenamiento."
   ],
   "steps": [
    "El propio texto la menciona como algo que se usa para 'verificar el resultado después'.",
    "'Después' significa que el algoritmo YA terminó de agrupar, sin haber visto y_true en ningún momento.",
    "Entonces adjusted_rand_score compara ese resultado (etiquetas del algoritmo) contra y_true, por fuera del entrenamiento — es una métrica de evaluación, no un dato de entrada."
   ],
   "stakes": "Distinguir una métrica de evaluación (que se calcula después, con datos que en producción tal vez no existan) de un dato de entrada real es clave para no armar un pipeline que dependa, sin darse cuenta, de información que no vas a tener disponible al desplegar el modelo."
  }
 ],
 [
  {
   "question": "Si tuvieras un dataset de clientes de un banco SIN ninguna etiqueta de 'tipo de cliente', ¿qué tipo de aprendizaje usarías para encontrar grupos de clientes parecidos entre sí?",
   "type": "mc",
   "options": [
    "No supervisado — no hay ninguna respuesta correcta pre-etiquetada, hay que descubrir los grupos a partir de los datos",
    "Supervisado — siempre hace falta una etiqueta 'y' para poder entrenar cualquier modelo",
    "Ninguno de los dos: sin etiquetas no se puede analizar el dataset de ninguna forma",
    "Aprendizaje por refuerzo, porque involucra tomar decisiones"
   ],
   "correct": 0,
   "solution": "Exactamente el caso de uso descrito en el propio ejemplo del código: descubrir estructura (grupos de clientes parecidos) sin que nadie haya etiquetado 'a qué grupo pertenece cada cliente' de antemano — es la definición misma de aprendizaje no supervisado.",
   "whyNot": [
    null,
    "Ese es precisamente el punto de este tema: NO siempre hace falta 'y' — cuando no existe una etiqueta real disponible (como en este caso), el aprendizaje no supervisado sigue funcionando con X solamente.",
    "Sí se puede analizar: K-Means, PCA y otras técnicas no supervisadas trabajan exactamente sobre datos sin etiquetar — es su caso de uso principal, no una limitación que las bloquee.",
    "Aprendizaje por refuerzo resuelve un problema distinto (un agente que actúa en un entorno y recibe recompensas) — no encaja con 'encontrar grupos parecidos en un conjunto de datos ya existente'."
   ],
   "steps": [
    "El escenario dice explícitamente: 'sin ninguna etiqueta de tipo de cliente'.",
    "Aprendizaje supervisado necesita un 'y' (la etiqueta correcta) para entrenar — acá no existe.",
    "Sin etiquetas pero con datos (X), el objetivo es descubrir grupos parecidos por su cuenta: eso es no supervisado.",
    "Por eso la respuesta es no supervisado."
   ],
   "stakes": "Es exactamente el tipo de decisión que se toma al inicio de un proyecto real de segmentación de clientes en un banco o retail: elegir mal el tipo de aprendizaje en esa etapa puede significar meses de trabajo con el enfoque equivocado."
  },
  {
   "question": "Un equipo de ciberseguridad quiere detectar patrones de tráfico de red sospechosos, pero los ataques nuevos NUNCA vienen marcados de antemano como 'esto es un ataque'. ¿Qué tipo de aprendizaje encaja con ese escenario, según los ejemplos de aplicación real del tema?",
   "type": "mc",
   "options": [
    "No supervisado — no hay etiquetas de 'ataque' disponibles de antemano, así que hay que descubrir qué tráfico se aparta de los patrones normales sin ninguna respuesta correcta pre-etiquetada",
    "Supervisado, entrenando con ataques ya conocidos para detectar exactamente esos mismos ataques en el futuro",
    "Ningún tipo de aprendizaje automático sirve para este problema, hace falta revisión manual de cada conexión",
    "Da exactamente igual cuál se use, ambos enfoques necesitan las mismas etiquetas de entrada"
   ],
   "correct": 0,
   "solution": "Es uno de los ejemplos de aplicación citados explícitamente: 'detectar anomalías en tráfico de red para ciberseguridad (los ataques nuevos no vienen con la etiqueta esto es un ataque)' — exactamente el caso de datos sin etiqueta pre-existente que define un problema no supervisado.",
   "whyNot": [
    null,
    "Entrenar solo con ataques YA conocidos (supervisado) no sirve para detectar ataques NUEVOS, que es justamente el problema descrito — un ataque nunca visto no tiene ninguna etiqueta con la que entrenar de antemano.",
    "El aprendizaje no supervisado (como detección de anomalías) es precisamente una herramienta automática que se usa en ciberseguridad real para este tipo de problema — no hace falta descartar el aprendizaje automático por completo.",
    "La diferencia es central, no irrelevante: supervisado necesita pares (X,y) con ataques ya etiquetados; no supervisado solo necesita X, y puede señalar tráfico 'raro' sin haber visto antes ningún ataque igual."
   ],
   "steps": [
    "El escenario dice explícitamente: los ataques nuevos NUNCA vienen etiquetados de antemano.",
    "Aprendizaje supervisado necesita ejemplos ya etiquetados para entrenar — no puede aprender a reconocer algo que nunca vio ni etiquetado.",
    "Aprendizaje no supervisado puede señalar tráfico que se aparta de los patrones normales, sin necesitar una etiqueta 'ataque' previa.",
    "Por eso el escenario encaja con no supervisado, tal como lo describe el ejemplo de aplicación del tema."
   ],
   "stakes": "Es exactamente por qué los sistemas reales de detección de intrusos usan técnicas no supervisadas (o de detección de anomalías) para atrapar ataques de día cero — amenazas que nadie etiquetó todavía porque son nuevas."
  }
 ],
 [
  {
   "question": "El código calcula la inercia para k=3 (≈23,53) y k=5 (≈15,47). ¿Por qué NO se puede concluir directamente que k=5 agrupa mejor los datos?",
   "type": "mc",
   "options": [
    "Porque la inercia SIEMPRE baja al aumentar k (más centroides quedan más cerca de cada punto), sin importar si esos grupos reflejan estructura real",
    "Porque el cálculo de inercia para k=5 tiene un error en el código",
    "Porque k=5 usa menos puntos de datos que k=3",
    "Porque la inercia solo se puede calcular para valores impares de k"
   ],
   "correct": 0,
   "solution": "El propio código lo señala: con 30 centroides (uno por punto), la inercia sería exactamente 0 — más centroides siempre reducen la distancia promedio a ALGÚN centroide. Por eso 'menor inercia' con más k no prueba una mejor agrupación real; hace falta un criterio como el método del codo.",
   "whyNot": [
    null,
    "No hay ningún error: KMeans(n_clusters=5, ...).fit(X).inertia_ es un cálculo directo y válido — el problema es CONCEPTUAL (qué significa esa inercia más baja), no un bug.",
    "Ambos KMeans (k=3 y k=5) se entrenan sobre el mismo X de 30 puntos — la cantidad de datos usados es idéntica en los dos casos.",
    "La inercia se calcula igual para cualquier valor entero de k, par o impar — no hay ninguna restricción de paridad en la fórmula."
   ],
   "steps": [
    "Pensá en el caso extremo: si k fuera igual al número de puntos, cada punto sería su propio centroide.",
    "Con un centroide por punto, la distancia de cada punto a SU centroide sería 0 — la inercia sería exactamente 0.",
    "Eso pasaría sin importar si esos 'grupos' de 1 punto reflejan alguna estructura real de los datos.",
    "Entonces menor inercia con más k no prueba que la agrupación sea mejor — solo prueba que hay más centroides repartiendo la distancia."
   ],
   "stakes": "Un analista que elige 'k' solo mirando qué inercia es más baja, sin ningún criterio adicional, terminaría eligiendo tantos grupos como clientes — un resultado inútil para cualquier decisión de negocio real, como diseñar 3 campañas de marketing y no 500."
  },
  {
   "question": "La teoría menciona que, para elegir k de verdad, hace falta el 'método del codo' u otro criterio, en vez de solo mirar cuál inercia es más baja. ¿Qué problema resuelve específicamente el método del codo?",
   "type": "mc",
   "options": [
    "Permite identificar un valor de k donde agregar más grupos deja de reducir la inercia de forma significativa, en vez de simplemente perseguir la inercia más baja posible (que siempre se logra con más k)",
    "Calcula automáticamente la inercia exacta sin necesidad de entrenar el modelo",
    "Reemplaza por completo la necesidad de usar KMeans, es un algoritmo de clustering distinto",
    "Sirve para acelerar el tiempo de entrenamiento de KMeans, no tiene relación con elegir k"
   ],
   "correct": 0,
   "solution": "El método del codo busca el punto donde, al graficar la inercia contra distintos valores de k, la curva deja de bajar bruscamente y se 'aplana' — ese quiebre ('codo') es una señal de que agregar más grupos ya no aporta una mejora real, a diferencia de simplemente elegir el k con menor inercia (que, como muestra el código, siempre sigue bajando).",
   "whyNot": [
    null,
    "El método del codo no reemplaza el entrenamiento — se necesita entrenar KMeans con varios valores de k (y calcular su inercia en cada caso) para poder graficar la curva y encontrar el codo.",
    "El método del codo es un CRITERIO para elegir k, no un algoritmo de clustering alternativo — sigue usando KMeans por dentro, para cada valor de k que se prueba.",
    "No tiene relación con la velocidad de entrenamiento — es una forma de decidir CUÁNTOS grupos usar, comparando la inercia de varios modelos ya entrenados."
   ],
   "steps": [
    "El problema de fondo es que la inercia SIEMPRE baja al aumentar k — nunca hay un mínimo natural que marque 'el mejor k'.",
    "El método del codo busca en cambio dónde la CAÍDA de la inercia se hace mucho más lenta al seguir aumentando k.",
    "Ese punto de quiebre (el 'codo') es una señal razonable de que agregar más grupos ya no aporta demasiado.",
    "Por eso resuelve justo el problema que el código señala: no se puede elegir k solo por 'menor inercia'."
   ],
   "stakes": "En un proyecto real de segmentación de clientes, aplicar el método del codo (en vez de perseguir la inercia mínima) es lo que evita terminar con cientos de segmentos inmanejables para el equipo de marketing."
  }
 ],
 [
  {
   "question": "Según la Definición de K-Means (Géron, Cap.9), ¿qué es exactamente el 'centroide' de un grupo?",
   "type": "mc",
   "options": [
    "El promedio (la posición media) de todos los puntos actualmente asignados a ese grupo",
    "El primer punto que se asignó a ese grupo al empezar el algoritmo",
    "El punto más alejado del centro del dataset completo",
    "Un punto elegido al azar en cada iteración, distinto cada vez"
   ],
   "correct": 0,
   "solution": "K-Means recalcula el centroide en cada iteración como el promedio de las posiciones de los puntos actualmente asignados a ese grupo — por eso los 'centros encontrados' que imprime el código son puntos promedio, no puntos reales del dataset.",
   "whyNot": [
    null,
    "El centroide se RECALCULA en cada iteración a medida que cambian las asignaciones — no se queda fijo en el primer punto asignado.",
    "No hay ninguna relación entre el centroide de un grupo y la distancia al centro del dataset completo — cada centroide depende únicamente de SUS propios puntos asignados.",
    "El centroide es determinístico dado el conjunto de puntos asignados (es su promedio exacto) — no hay ningún componente aleatorio en su cálculo una vez fijadas las asignaciones."
   ],
   "steps": [
    "Fijate qué hace el algoritmo en cada iteración: reasigna puntos a grupos y después RECALCULA el centro de cada grupo.",
    "Ese recálculo es un promedio de las posiciones de los puntos que quedaron en ese grupo en ese momento.",
    "Por eso el centro final impreso no es necesariamente ningún punto real del dataset, sino una posición promedio."
   ],
   "stakes": "El 'cliente promedio' que reporta un centroide de K-Means casi nunca es un cliente real — es útil para describir el grupo en un informe, pero un error común es tratarlo como si fuera una persona concreta a la hora de decidir una campaña."
  },
  {
   "question": "Según los ejemplos de aplicación real, en compresión de imágenes con K-Means, ¿qué representaría cada centroide?",
   "type": "mc",
   "options": [
    "Uno de los k colores que reemplazan a los millones de colores originales de la imagen — cada píxel se reasigna al color de su centroide más cercano",
    "La posición exacta (fila, columna) de cada píxel en la imagen",
    "El tamaño en bytes del archivo de imagen comprimido",
    "El número total de píxeles que tiene la imagen"
   ],
   "correct": 0,
   "solution": "El propio ejemplo lo describe: 'compresión de imágenes (reemplazar millones de colores por los k colores de los centroides)' — cada centroide, calculado como el promedio de los píxeles agrupados con él, termina representando UN color representativo que reemplaza a todos los colores originales de ese grupo.",
   "whyNot": [
    null,
    "K-Means aplicado a compresión de imágenes agrupa por COLOR (valores RGB de los píxeles), no por su posición espacial en la imagen — la ubicación de cada píxel no interviene en el clustering.",
    "El tamaño del archivo comprimido es una consecuencia de usar menos colores, no algo que el centroide represente directamente — el centroide sigue siendo un valor de color, no una medida de bytes.",
    "La cantidad total de píxeles de la imagen no cambia al comprimir por colores — se mantiene el mismo número de píxeles, solo se reduce la cantidad de colores distintos que existen entre ellos."
   ],
   "steps": [
    "En compresión de imágenes, cada píxel se trata como un punto (definido por su color).",
    "K-Means agrupa esos puntos-color en k grupos, igual que agrupa coordenadas en el ejemplo con make_blobs.",
    "El centroide de cada grupo (el promedio de los colores agrupados) pasa a ser el color 'representante' de todo ese grupo.",
    "Por eso, en este contexto, cada centroide es directamente uno de los k colores finales de la imagen comprimida."
   ],
   "stakes": "Esta es la base real de muchos formatos de compresión con paleta reducida: en vez de guardar millones de colores exactos, se guardan solo k colores (los centroides) y a qué centroide pertenece cada píxel — un ahorro enorme de espacio."
  }
 ],
 [
  {
   "question": "¿Qué mide exactamente la 'inercia' que imprime el código (23,53 para k=3)?",
   "type": "mc",
   "options": [
    "La suma de las distancias al cuadrado de cada punto a su centroide asignado más cercano",
    "El número total de iteraciones que tardó el algoritmo en converger",
    "La cantidad de puntos que quedaron sin asignar a ningún grupo",
    "El tiempo en segundos que tardó KMeans en entrenar"
   ],
   "correct": 0,
   "solution": "Definición formal (Géron, Cap.9): inercia = Σᵢ mín_{μⱼ∈C} ‖xᵢ − μⱼ‖² — la suma, sobre todos los puntos, de la distancia al cuadrado a su centroide asignado. Cuanto más compactos son los grupos, menor la inercia.",
   "whyNot": [
    null,
    "El número de iteraciones es un detalle interno de convergencia del algoritmo, accesible por separado (n_iter_) — no es lo que mide la inercia.",
    "K-Means SIEMPRE asigna cada punto a algún grupo (el más cercano) — no existe la posibilidad de puntos 'sin asignar' en este algoritmo.",
    "El tiempo de cómputo depende del hardware y no es una propiedad matemática del resultado — la inercia es una medida de qué tan compactos quedaron los grupos, no de velocidad."
   ],
   "steps": [
    "La palabra clave es 'inercia' — buscá qué fórmula usa Géron para definirla: Σ mín ‖xᵢ − μⱼ‖².",
    "Es una suma sobre TODOS los puntos, cada uno aportando la distancia (al cuadrado) a su centroide más cercano.",
    "No tiene nada que ver con iteraciones, puntos sin asignar ni tiempo de cómputo — es puramente geométrico."
   ],
   "stakes": "Saber exactamente qué mide la inercia evita un error común al comparar modelos reales: dos corridas de K-Means con distinta cantidad de clusters NUNCA se pueden comparar directamente por inercia sin ajustar por ese motivo."
  },
  {
   "question": "Según la aplicación real del tema, ¿cuál es la gran limitación de K-Means que empuja a buscar alternativas como DBSCAN?",
   "type": "mc",
   "options": [
    "Que hay que decidir k de antemano y que el algoritmo asume grupos redondeados de tamaño similar, algo que no siempre refleja la estructura real de los datos",
    "Que K-Means no puede usarse nunca con datos numéricos, solo con texto",
    "Que K-Means jamás converge y hay que interrumpirlo manualmente",
    "Que K-Means solo funciona si hay exactamente 2 columnas en los datos"
   ],
   "correct": 0,
   "solution": "El propio ejemplo lo señala: 'su gran limitación — que hay que decidir k de antemano y que asume grupos redondeados de tamaño similar — es justamente lo que dispara la búsqueda de alternativas como DBSCAN'. K-Means fuerza una forma y una cantidad de grupos que el usuario debe fijar, sin importar si eso refleja la estructura real.",
   "whyNot": [
    null,
    "K-Means trabaja precisamente con datos numéricos (como las coordenadas del ejemplo) — la limitación no tiene que ver con el tipo de dato, sino con la forma y cantidad de grupos que asume.",
    "K-Means sí converge (el código lo entrena sin problemas, con n_init=10 para evitar malas inicializaciones) — la limitación no es sobre si converge, sino sobre qué tipo de estructura puede representar bien.",
    "K-Means puede trabajar con cualquier número de columnas (dimensiones), no está limitado a 2 — el ejemplo usa 2 columnas por conveniencia visual, no por una restricción del algoritmo."
   ],
   "steps": [
    "Fijate qué dos cosas hay que decidir ANTES de correr K-Means: cuántos grupos (k) va a haber.",
    "Además, por cómo asigna puntos a centroides, K-Means solo puede representar bien grupos más o menos redondos y de tamaño parecido.",
    "Cuando los datos reales no cumplen eso (formas raras, tamaños muy distintos, o no se sabe k de antemano), K-Means se queda corto.",
    "Por eso el propio ejemplo señala que esta limitación es lo que motiva buscar alternativas como DBSCAN."
   ],
   "stakes": "Elegir K-Means sin cuestionar si los datos reales tienen forma redondeada es un error común en proyectos de segmentación — cuando los grupos reales tienen formas irregulares, K-Means los va a partir mal sin avisar."
  }
 ],
 [
  {
   "question": "El código entrena K-Means con n_init=10. ¿Por qué K-Means necesita repetirse varias veces con inicializaciones distintas, a diferencia de, por ejemplo, la regresión lineal?",
   "type": "mc",
   "options": [
    "Porque K-Means parte de centroides iniciales al azar, y una mala inicialización puede quedar atascada en un resultado subóptimo — repetirlo y quedarse con el mejor reduce ese riesgo",
    "Porque K-Means es más lento que la regresión lineal y necesita más intentos para terminar",
    "Porque cada repetición usa una porción distinta de los datos, como en K-fold",
    "n_init no tiene ningún efecto real sobre el resultado final"
   ],
   "correct": 0,
   "solution": "K-Means es un algoritmo iterativo que depende de dónde arrancan los centroides — una mala 'tirada de dados' inicial puede converger a una agrupación peor. n_init=10 corre el algoritmo 10 veces con puntos de partida distintos y se queda con la de menor inercia, reduciendo el riesgo de un mal resultado por mala suerte en la inicialización.",
   "whyNot": [
    null,
    "n_init no es una medida de velocidad — es una estrategia para evitar quedar atascado en una mala solución local, un problema que la regresión lineal (que tiene una única solución óptima calculable directamente) ni siquiera tiene.",
    "n_init no divide los datos en particiones (eso describiría K-fold, una técnica de validación distinta) — cada repetición usa el mismo X completo, solo cambia el punto de partida de los centroides.",
    "n_init sí afecta el resultado: sin repetir con distintas inicializaciones, K-Means puede converger a una agrupación notablemente peor por simple mala suerte en el punto de partida."
   ],
   "steps": [
    "K-Means arranca colocando los centroides iniciales al azar — ese punto de partida influye en dónde termina convergiendo.",
    "Una mala 'tirada de dados' inicial puede hacer que el algoritmo quede atascado en una agrupación peor de lo posible.",
    "n_init=10 corre el algoritmo 10 veces con arranques distintos y se queda con el resultado de menor inercia, reduciendo el riesgo de una mala inicialización.",
    "Regresión lineal no depende de un punto de partida al azar — por eso no necesita algo como n_init."
   ],
   "stakes": "Correr K-Means una sola vez (n_init=1) en un proyecto real es fuente de bugs difíciles de reproducir: dos ejecuciones del mismo código, con la misma data, pueden dar agrupaciones distintas por pura mala suerte en la inicialización."
  },
  {
   "question": "El código entrena km3 = KMeans(n_clusters=3, n_init=10, random_state=42) y km5 = KMeans(n_clusters=5, n_init=10, random_state=42). ¿Cuál es la ÚNICA diferencia entre ambas configuraciones?",
   "type": "mc",
   "options": [
    "El número de grupos que cada uno debe encontrar (n_clusters=3 contra n_clusters=5) — el resto de los parámetros (n_init, random_state) son idénticos",
    "km3 usa un dataset distinto de km5",
    "km3 no usa n_init, mientras que km5 sí lo usa",
    "km5 usa un valor de random_state distinto para obtener resultados diferentes"
   ],
   "correct": 0,
   "solution": "Comparando ambas líneas del código, ambos modelos comparten exactamente n_init=10 y random_state=42 — lo único que cambia es n_clusters (3 contra 5). Esto aísla la comparación: cualquier diferencia en inercia entre km3 y km5 se debe pura y exclusivamente a la cantidad de grupos, no a otro factor.",
   "whyNot": [
    null,
    "Ambos modelos se entrenan con .fit(X) sobre el mismo X, generado una sola vez por make_blobs — no hay dos datasets distintos en el código.",
    "Ambas líneas incluyen explícitamente n_init=10 — no es que uno lo tenga y el otro no.",
    "Ambas líneas usan explícitamente random_state=42, el mismo valor — no hay ninguna diferencia en la semilla aleatoria entre los dos modelos."
   ],
   "steps": [
    "Mirá las dos líneas de creación de los modelos, una al lado de la otra.",
    "n_init=10 aparece igual en ambas. random_state=42 aparece igual en ambas.",
    "El único valor que cambia entre las dos líneas es n_clusters: 3 en un caso, 5 en el otro.",
    "Por eso cualquier diferencia de resultado entre km3 y km5 se puede atribuir pura y exclusivamente a esa diferencia de k."
   ],
   "stakes": "Aislar un solo parámetro a la vez (como se hace aquí con n_clusters) es una buena práctica experimental real: si cambiás varias cosas a la vez entre dos modelos, no podés saber a cuál de los cambios se debe la diferencia de resultados."
  }
 ],
 [
  {
   "question": "PCA reduce iris de 4 a 2 columnas conservando el 97,77% de la varianza. ¿Qué significa exactamente ese porcentaje?",
   "type": "mc",
   "options": [
    "Que las 2 columnas nuevas capturan el 97,77% de toda la variación (información) presente en las 4 columnas originales",
    "Que el 97,77% de las 150 flores quedaron correctamente clasificadas",
    "Que se eliminaron el 97,77% de las filas del dataset",
    "Que el modelo tiene un 97,77% de precisión al predecir la especie de la flor"
   ],
   "correct": 0,
   "solution": "explained_variance_ratio_.sum() = 0,9777 significa que, de toda la variación (dispersión) que había en las 4 columnas originales, las 2 columnas nuevas (componentes principales) conservan el 97,77% — se perdió información real, pero muy poca.",
   "whyNot": [
    null,
    "PCA no clasifica nada — no asigna una especie ni predice ninguna etiqueta, solo transforma las columnas de entrada. Ese porcentaje no tiene relación con clasificación correcta.",
    "PCA reduce COLUMNAS (dimensiones), no FILAS (observaciones) — las 150 flores del dataset siguen siendo 150 después de aplicar PCA, solo con 2 columnas en vez de 4.",
    "El 97,77% no es una medida de precisión predictiva (PCA ni siquiera predice nada) — es la fracción de VARIANZA (dispersión de los datos) que se conserva al reducir dimensiones."
   ],
   "steps": [
    "explained_variance_ratio_.sum() mide cuánta de la variación TOTAL original quedó capturada en las columnas nuevas.",
    "97,77% no tiene relación con cuántas filas hay ni con ninguna predicción de especie — es puramente sobre cuánta información (varianza) se conserva.",
    "Entonces significa: las 2 columnas nuevas retienen el 97,77% de toda la variación que había en las 4 originales."
   ],
   "stakes": "En un informe real, decir 'reduje el dataset a 2 columnas' sin aclarar cuánta varianza se conservó es engañoso — un lector podría no darse cuenta de que se descartó información relevante del negocio."
  },
  {
   "question": "El código comenta que X tiene 150 flores y 4 columnas. Después de aplicar PCA para reducir a 2 columnas (X2), ¿cuántas flores hay en X2?",
   "type": "mc",
   "options": [
    "Siguen siendo 150 — PCA reduce las columnas (dimensiones), no la cantidad de filas (observaciones)",
    "75, porque PCA reduce a la mitad tanto filas como columnas",
    "2, porque PCA reduce todo el dataset al mismo número que columnas nuevas",
    "300, porque PCA duplica las observaciones al transformar los datos"
   ],
   "correct": 0,
   "solution": "PCA transforma columnas, no filas: cada una de las 150 flores originales sigue existiendo después de la transformación, solo que ahora descrita con 2 números (componentes) en vez de 4. El propio código lo confirma imprimiendo 'forma REDUCIDA: X2.shape (2 columnas)' — la reducción es en columnas, no en observaciones.",
   "whyNot": [
    null,
    "PCA no reduce la cantidad de filas de ninguna manera — reducir a la mitad las flores no tiene ninguna base en cómo funciona la transformación.",
    "El número de filas no tiene relación con el número de componentes elegidos — confundir estos dos números es un error común, pero X2 sigue teniendo una fila por cada flor original.",
    "PCA no agrega observaciones nuevas — transforma cada fila existente a un nuevo sistema de coordenadas, sin duplicar ni eliminar ninguna."
   ],
   "steps": [
    "PCA opera sobre las COLUMNAS de un dataset, buscando nuevas direcciones (componentes) que resuman la variación.",
    "Eso no tiene ningún efecto sobre cuántas FILAS (observaciones, en este caso flores) hay en el dataset.",
    "Por eso X2 (la versión reducida) sigue teniendo exactamente 150 flores, solo que cada una descrita con 2 números en vez de 4."
   ],
   "stakes": "Confundir 'reducir dimensiones' con 'reducir observaciones' es un malentendido común al empezar con PCA — en un dataset real de miles de clientes, aplicar PCA nunca elimina clientes, solo resume las columnas que los describen."
  }
 ],
 [
  {
   "question": "La primera componente principal explica sola el 92,46% de la varianza. ¿Qué te dice esto sobre las 4 columnas ORIGINALES de iris?",
   "type": "mc",
   "options": [
    "Que las 4 columnas originales están bastante correlacionadas entre sí — mucha de su variación apunta 'en la misma dirección'",
    "Que solo una de las 4 columnas originales tiene datos válidos",
    "Que el dataset iris tiene datos corruptos o con errores",
    "Que hace falta al menos 10 componentes para explicar cualquier variación"
   ],
   "correct": 0,
   "solution": "Si un solo eje nuevo (combinación lineal de las 4 columnas originales) ya explica el 92,46% de toda la variación, es porque las columnas originales no son 'independientes': varían mucho en conjunto (por ejemplo, largo y ancho de pétalo suelen crecer juntos), así que PCA puede resumir casi toda esa variación compartida en un solo eje.",
   "whyNot": [
    null,
    "Las 4 columnas de iris (largo/ancho de pétalo y sépalo) son datos reales y válidos — PCA usa las 4 para calcular sus componentes, no descarta ninguna de entrada.",
    "No hay ninguna corrupción: el dataset iris es uno de los más usados y verificados en machine learning — la alta varianza explicada refleja correlación real entre sus atributos, no un error.",
    "Es exactamente lo contrario: con solo 2 componentes ya se explica el 97,77% — muy lejos de necesitar 10 componentes (que además no tendría sentido pedir, dado que el dataset original solo tiene 4 columnas)."
   ],
   "steps": [
    "Si UN SOLO eje nuevo (combinación de las 4 columnas) ya explica el 92,46% de toda la variación...",
    "...eso solo es posible si las columnas originales no varían de forma independiente entre sí.",
    "Es decir, están correlacionadas: cuando una sube, las otras tienden a subir o bajar junto con ella (ej. largo y ancho de pétalo).",
    "Por eso un solo eje resume casi toda la variación compartida."
   ],
   "stakes": "Detectar que las columnas originales están correlacionadas (por lo que una sola componente explica casi todo) es una señal de alerta real: puede indicar columnas redundantes que convendría eliminar directamente, no solo comprimir con PCA."
  },
  {
   "question": "Según la aplicación real del tema, ¿por qué reducir un dataset de 4 columnas a 2 con PCA podría acelerar el entrenamiento de OTRO modelo (por ejemplo, uno de clasificación) entrenado después?",
   "type": "mc",
   "options": [
    "Porque ese otro modelo tendría que procesar menos columnas de entrada, y menos columnas generalmente significa menos cómputo durante el entrenamiento",
    "Porque PCA elimina automáticamente las filas duplicadas del dataset",
    "Porque PCA convierte los datos a un formato de archivo más liviano en disco",
    "Porque PCA reemplaza el algoritmo de entrenamiento por uno más rápido"
   ],
   "correct": 0,
   "solution": "El propio ejemplo lo menciona: PCA 'se usa para acelerar el entrenamiento de otros modelos (menos columnas = menos cómputo)'. Al reducir de 4 a 2 columnas, cualquier modelo posterior que use X2 en vez de X tiene menos valores de entrada por fila que procesar, lo que generalmente reduce el tiempo de entrenamiento.",
   "whyNot": [
    null,
    "PCA no elimina filas duplicadas — transforma columnas, sin tocar la cantidad ni el contenido de las filas (como ya se vio, las 150 flores siguen siendo 150).",
    "PCA no es una herramienta de compresión de archivos en disco — trabaja sobre la estructura matemática de los datos en memoria, no sobre el formato del archivo.",
    "PCA no reemplaza ningún algoritmo de entrenamiento — es un paso de preprocesamiento que se aplica ANTES de entrenar el modelo real (por ejemplo, un clasificador), no un sustituto de él."
   ],
   "steps": [
    "Pensá qué hace un modelo de entrenamiento con cada fila de datos: procesa cada columna como una entrada.",
    "Con menos columnas (2 en vez de 4), hay menos cálculos que hacer por cada fila procesada.",
    "Multiplicado por miles o millones de filas, esa diferencia de columnas puede ahorrar bastante tiempo de cómputo.",
    "Por eso PCA se usa como paso previo para acelerar el entrenamiento de otros modelos, tal como señala el ejemplo de aplicación."
   ],
   "stakes": "En proyectos reales con cientos de columnas (por ejemplo, sensores industriales), aplicar PCA antes de entrenar un modelo de predicción puede ser la diferencia entre horas y minutos de entrenamiento."
  }
 ],
 [
  {
   "question": "¿Por qué PCA es casi un paso obligatorio antes de GRAFICAR un dataset con muchas columnas (como el de 4 columnas de iris, o uno con cientos)?",
   "type": "mc",
   "options": [
    "Porque no se puede dibujar un gráfico con más de 2 o 3 ejes a la vez, y PCA reduce las columnas a esa cantidad conservando la mayor variación posible",
    "Porque graficar datos de alta dimensión hace que Python se bloquee siempre",
    "Porque PCA convierte automáticamente cualquier dataset en una imagen",
    "Porque los gráficos solo aceptan números enteros, y PCA convierte todo a enteros"
   ],
   "correct": 0,
   "solution": "Un gráfico 2D o 3D tiene, como máximo, 2 o 3 ejes — no hay forma de graficar directamente las 4 (o 400) columnas de un dataset real. PCA resuelve esto eligiendo las 2 o 3 direcciones que conservan la mayor variación posible, para poder visualizar 'lo esencial' del dataset en un gráfico normal.",
   "whyNot": [
    null,
    "Python puede procesar datos de cualquier número de columnas sin bloquearse — el problema no es técnico/de rendimiento, es que un gráfico 2D o 3D tiene un límite físico de ejes que se pueden dibujar.",
    "PCA transforma columnas numéricas en otras columnas numéricas (los componentes principales) — no genera ninguna imagen ni convierte datos en formato de imagen.",
    "PCA trabaja con números reales (decimales), no solo enteros — de hecho, en el código, los valores transformados (como -2,68 o 0,32) son explícitamente decimales."
   ],
   "steps": [
    "Un gráfico normal tiene como máximo 2 o 3 ejes (x, y, quizás z).",
    "Un dataset real puede tener 4, 50 o 400 columnas — no hay forma de dibujar todas esas dimensiones a la vez.",
    "PCA elige las 2 o 3 direcciones que conservan la MAYOR variación posible, resumiendo lo esencial en algo que sí se puede graficar."
   ],
   "stakes": "En cualquier reporte de datos con más de 3 columnas, intentar graficar 'todo junto' sin antes reducir dimensiones es un error común de quien recién empieza — PCA es el paso que lo hace posible."
  },
  {
   "question": "Según la aplicación real del tema, ¿para qué se usa PCA en finanzas, con cientos de indicadores económicos?",
   "type": "mc",
   "options": [
    "Para resumir cientos de indicadores económicos correlacionados entre sí en unos pocos 'factores' reales que capturan la mayor parte de la variación",
    "Para predecir con certeza el precio futuro de una acción específica",
    "Para eliminar del dataset los indicadores económicos que tengan errores de tipeo",
    "Para convertir automáticamente los datos financieros de una moneda a otra"
   ],
   "correct": 0,
   "solution": "El propio ejemplo lo describe: 'en finanzas se usa para resumir cientos de indicadores económicos correlacionados en unos pocos factores reales' — el mismo principio que con las 4 columnas de iris (correlacionadas, resumibles en pocas componentes), aplicado a un dataset financiero mucho más grande.",
   "whyNot": [
    null,
    "PCA no es un modelo predictivo — no genera pronósticos de precios futuros, es una técnica de reducción de dimensiones que resume columnas correlacionadas, sin garantizar ninguna predicción.",
    "PCA no detecta ni corrige errores de tipeo o datos mal cargados — trabaja matemáticamente sobre la variación de columnas numéricas válidas, no sobre la limpieza de errores de captura.",
    "PCA no realiza conversiones de moneda ni ningún tipo de transformación de unidades — reduce dimensiones basándose en la varianza de los datos numéricos tal como están."
   ],
   "steps": [
    "Con cientos de indicadores económicos, es muy probable que muchos estén correlacionados entre sí (miden aspectos parecidos de la economía).",
    "Igual que con las 4 columnas de iris, PCA puede resumir esa variación compartida en unos pocos ejes nuevos.",
    "Esos pocos ejes actúan como 'factores' que resumen lo esencial de cientos de indicadores originales.",
    "Por eso PCA es una herramienta estándar en finanzas para resumir grandes conjuntos de indicadores correlacionados."
   ],
   "stakes": "En un banco de inversión real, analizar cientos de indicadores económicos uno por uno es inviable — reducirlos a unos pocos factores con PCA es lo que permite construir modelos de riesgo manejables."
  }
 ],
 [
  {
   "question": "Si tuvieras un dataset con 500 columnas MUY correlacionadas entre sí (varias miden casi lo mismo), ¿qué esperarías ver en explained_variance_ratio_ de las primeras componentes de PCA?",
   "type": "mc",
   "options": [
    "Que las primeras componentes concentran un porcentaje muy alto de la varianza total, similar a lo que pasó con las 4 columnas de iris",
    "Que las 500 componentes explicarían exactamente el mismo porcentaje cada una (1/500 cada una)",
    "Que PCA fallaría directamente y no podría procesar tantas columnas",
    "Que la varianza explicada sería siempre 0% para cualquier número de componentes"
   ],
   "correct": 0,
   "solution": "El mismo patrón que se vio con iris (columnas correlacionadas → pocas componentes concentran casi toda la varianza) se repite con cualquier dataset donde las columnas comparten mucha información: cuanta más correlación real hay entre las columnas originales, menos componentes hacen falta para explicar la mayor parte de la varianza total.",
   "whyNot": [
    null,
    "Un reparto uniforme (1/500 cada una) describiría columnas TOTALMENTE independientes entre sí, sin ninguna correlación — es el caso contrario al planteado (columnas MUY correlacionadas concentran la varianza en pocos ejes).",
    "PCA no tiene un límite práctico de columnas de entrada — de hecho, cuantas más columnas correlacionadas haya, más útil (y no menos viable) se vuelve reducir la dimensionalidad.",
    "Si las columnas originales tienen variación real (no son todas constantes), la varianza explicada siempre suma un valor positivo — 0% en todas las componentes solo pasaría si el dataset entero no tuviera ninguna variación."
   ],
   "steps": [
    "Fijate qué pasó con iris: 4 columnas correlacionadas → 1 sola componente explica el 92% de la varianza.",
    "Ese patrón se repite con cualquier dataset: cuanto más correlacionadas están las columnas originales, menos componentes hacen falta para explicar la mayoría de la varianza.",
    "500 columnas MUY correlacionadas seguirían ese mismo patrón: las primeras componentes concentrarían casi toda la varianza total."
   ],
   "stakes": "Con datasets reales de cientos de sensores o encuestas (donde muchas preguntas miden cosas parecidas), reconocer este patrón te dice de entrada que probablemente unas pocas componentes van a alcanzar — ahorra tiempo de exploración."
  },
  {
   "question": "Según la aplicación real del tema, además de acelerar entrenamiento y facilitar visualización, ¿para qué otra cosa se usa PCA con los datos?",
   "type": "mc",
   "options": [
    "Para comprimir datos, guardando solo las direcciones (componentes) más informativas en vez de todas las columnas originales",
    "Para encriptar los datos y protegerlos de accesos no autorizados",
    "Para traducir automáticamente etiquetas de texto entre distintos idiomas",
    "Para generar copias de seguridad automáticas del dataset original"
   ],
   "correct": 0,
   "solution": "El propio ejemplo lo dice explícitamente: PCA 'también se usa para... comprimir datos (guardar solo las direcciones más informativas)'. Al quedarte solo con las 2 componentes que explican el 97,77% de la variación, podés guardar una versión mucho más liviana del dataset sin perder casi nada de información real.",
   "whyNot": [
    null,
    "PCA no es una técnica de seguridad ni de encriptación — no protege datos de accesos no autorizados, transforma columnas para reducir dimensiones, sin ningún objetivo de seguridad.",
    "PCA trabaja exclusivamente con datos numéricos y su variación estadística — no tiene ninguna relación con traducción de texto entre idiomas.",
    "PCA no crea copias de seguridad ni gestiona backups — es una técnica de reducción de dimensiones, un concepto completamente distinto al de resguardar datos."
   ],
   "steps": [
    "PCA encuentra las direcciones (componentes) que concentran la mayor parte de la variación real de los datos.",
    "Si guardás solo esas pocas direcciones más informativas (en vez de todas las columnas originales), el dataset resultante ocupa mucho menos espacio.",
    "Con iris, guardar solo 2 de las 4 columnas originales conserva el 97,77% de la variación — una compresión con muy poca pérdida real.",
    "Por eso PCA se usa también como técnica de compresión de datos, no solo para acelerar entrenamiento o graficar."
   ],
   "stakes": "En sistemas reales con millones de registros de alta dimensión (por ejemplo, huellas dactilares o espectros de sensores), comprimir con PCA antes de almacenar puede significar un ahorro de espacio enorme sin perder la información esencial."
  }
 ],
 [
  {
   "question": "DBSCAN obtiene ARI=1,0 (perfecto) recuperando las dos lunas, mientras K-Means solo llega a 0,214. ¿Por qué falla tanto K-Means con esta forma de datos?",
   "type": "mc",
   "options": [
    "Porque K-Means agrupa por distancia a un centroide, y eso solo puede dibujar regiones redondeadas — no puede seguir la forma curva de una luna",
    "Porque K-Means tiene un error de implementación en scikit-learn",
    "Porque a K-Means no se le dieron suficientes datos de entrenamiento",
    "Porque K-Means solo funciona con datos de una sola dimensión"
   ],
   "correct": 0,
   "solution": "K-Means asigna cada punto al centroide más cercano — geométricamente, eso solo puede producir fronteras rectas entre regiones más o menos circulares. Una forma de luna, curva y alargada, no se puede aproximar bien con esa lógica, sin importar cuántas veces se repita el algoritmo.",
   "whyNot": [
    null,
    "KMeans es un algoritmo estándar y ampliamente verificado de scikit-learn — el resultado bajo no es un bug, es una limitación estructural conocida frente a formas no convexas.",
    "Ambos algoritmos (DBSCAN y KMeans) reciben EXACTAMENTE los mismos 53 puntos (X2) — la cantidad de datos es idéntica, la diferencia es puramente de cómo cada algoritmo define un 'grupo'.",
    "Los datos son 2D (dos coordenadas por punto, como en el gráfico) — el problema no es la dimensionalidad, es la forma geométrica no convexa de las lunas."
   ],
   "steps": [
    "K-Means asigna cada punto al centroide MÁS CERCANO — geométricamente, eso solo puede trazar fronteras rectas entre regiones redondeadas.",
    "Una forma de luna es curva y alargada — no se puede aproximar bien con fronteras rectas ni con regiones circulares.",
    "Por eso, sin importar cuántas veces se repita K-Means (n_init), la forma del algoritmo mismo no puede seguir esa curva — el ARI queda bajo (0,214).",
    "DBSCAN, en cambio, conecta puntos densos entre sí sin asumir ninguna forma, así que sí puede seguir la curva de la luna (ARI=1,0)."
   ],
   "stakes": "Elegir K-Means para datos con forma irregular (por ejemplo, regiones geográficas de actividad sísmica, que no son círculos) da resultados que PARECEN razonables pero están mal — un error silencioso, no uno que tire un mensaje de aviso."
  },
  {
   "question": "El código crea DBSCAN(eps=0.35, min_samples=4). Según la definición formal de Géron (Cap.9), ¿qué determinan exactamente estos dos parámetros?",
   "type": "mc",
   "options": [
    "eps es el radio dentro del cual se buscan vecinos, y min_samples es la cantidad mínima de vecinos que debe tener un punto dentro de ese radio para considerarse un 'core point' (punto denso)",
    "eps es la cantidad de clusters que va a encontrar el algoritmo, y min_samples es la cantidad mínima de outliers permitidos",
    "eps es el número de iteraciones máximas del algoritmo, y min_samples es la cantidad de veces que se repite el entrenamiento",
    "eps y min_samples son parámetros equivalentes entre sí, cualquiera de los dos se puede usar indistintamente"
   ],
   "correct": 0,
   "solution": "Definición formal citada en la teoría: 'un punto es core point si tiene al menos min_samples vecinos dentro de radio eps'. En el código, eps=0.35 fija ese radio de búsqueda, y min_samples=4 fija cuántos vecinos hacen falta dentro de ese radio para que un punto cuente como denso — ninguno de los dos parámetros es 'la cantidad de clusters', que es justamente lo que DBSCAN NO recibe como entrada.",
   "whyNot": [
    null,
    "DBSCAN no recibe la cantidad de clusters como parámetro en absoluto — esa es justamente la diferencia con KMeans; eps y min_samples son criterios de densidad, no de cantidad de grupos.",
    "Ninguno de los dos parámetros controla iteraciones o repeticiones del entrenamiento — DBSCAN no es un algoritmo iterativo del estilo de K-Means o GMM, no tiene ese concepto de 'repetir n veces'.",
    "eps (una distancia/radio) y min_samples (una cantidad de puntos) miden cosas completamente distintas — no son intercambiables entre sí, cada uno cumple un rol específico en la definición de densidad."
   ],
   "steps": [
    "Buscá en la definición formal qué hace falta para que un punto sea 'core point': cierta cantidad de vecinos, dentro de cierto radio.",
    "eps=0.35 es ese radio de búsqueda alrededor de cada punto.",
    "min_samples=4 es la cantidad mínima de vecinos que deben caer dentro de ese radio.",
    "Juntos, esos dos números definen qué tan 'denso' tiene que ser un área para que DBSCAN la reconozca como parte de un cluster."
   ],
   "stakes": "Ajustar mal eps o min_samples en un proyecto real (por ejemplo, muy chico o muy grande) puede hacer que DBSCAN vea todo como ruido o todo como un único cluster gigante — entender qué controla cada parámetro es clave para calibrarlo bien."
  }
 ],
 [
  {
   "question": "DBSCAN marca los índices 50, 51 y 52 (los 3 outliers agregados a propósito) con la etiqueta -1. ¿Qué significa esa etiqueta?",
   "type": "mc",
   "options": [
    "Que esos puntos no tienen suficientes vecinos cerca como para pertenecer a ningún grupo denso — DBSCAN los clasifica como 'ruido'",
    "Que esos puntos pertenecen al cluster número -1, uno más de los grupos encontrados",
    "Que hubo un error al procesar esos 3 puntos específicos",
    "Que esos puntos son el centro exacto de cada cluster"
   ],
   "correct": 0,
   "solution": "-1 es la etiqueta reservada de DBSCAN para 'ruido': puntos que no cumplen el criterio de densidad (no tienen min_samples vecinos dentro de radio eps) y por lo tanto no se asignan a ningún cluster real — es exactamente el comportamiento esperado con 3 puntos deliberadamente alejados del resto.",
   "whyNot": [
    null,
    "-1 NO es un número de cluster real — el código mismo lo excluye explícitamente al contar clusters ('n_clusters = ... - (1 if -1 in ... else 0)') precisamente porque no representa un grupo, sino la ausencia de uno.",
    "Los 3 outliers se procesan sin ningún error — el código corre completo y produce resultados coherentes; la etiqueta -1 es una salida válida y esperada del algoritmo, no una falla.",
    "El 'centro' de un cluster es un concepto de K-Means (centroide) — DBSCAN ni siquiera calcula centros, agrupa por densidad de vecinos, no por distancia a un punto central."
   ],
   "steps": [
    "Los índices 50, 51, 52 son los 3 outliers agregados A PROPÓSITO, lejos del resto de los puntos.",
    "DBSCAN solo agrupa puntos que tienen suficientes vecinos cerca (min_samples dentro de eps) — esos 3 puntos no cumplen esa condición.",
    "La etiqueta -1 es la reservada para 'no pertenece a ningún grupo denso': ruido."
   ],
   "stakes": "En un sistema real de videovigilancia o de detección de anomalías en sensores, la etiqueta -1 de DBSCAN es literalmente la salida que interesa: identifica lo raro, no lo normal."
  },
  {
   "question": "Según la aplicación real del tema, si DBSCAN se usara para agrupar zonas geográficas por densidad de casos durante un brote epidemiológico, ¿qué representaría un punto marcado con la etiqueta -1?",
   "type": "mc",
   "options": [
    "Un caso aislado que no tiene suficientes casos cercanos alrededor como para formar parte de ningún foco denso del brote",
    "El caso índice (el primer caso confirmado) que dio origen a todo el brote",
    "La zona geográfica con la mayor cantidad de casos confirmados",
    "Un error de carga de datos que debe eliminarse antes de continuar"
   ],
   "correct": 0,
   "solution": "El mismo principio que con los 3 outliers del código (que quedan marcados como -1 por no tener suficientes vecinos cerca) aplica al ejemplo de aplicación real: 'agrupar zonas geográficas por densidad de eventos (por ejemplo, focos de un brote epidemiológico)'. Un caso geográficamente aislado, sin suficientes casos cercanos, no forma parte de ningún foco denso y quedaría marcado como ruido (-1), no como perteneciente a algún foco.",
   "whyNot": [
    null,
    "El caso índice de un brote no tiene por qué quedar aislado geográficamente — de hecho, suele estar rodeado de los primeros casos secundarios cercanos, lo que lo haría parte de un foco denso, no ruido.",
    "La zona con más casos sería, al contrario, el CENTRO de un cluster denso (no ruido) — es exactamente lo opuesto de lo que representa la etiqueta -1.",
    "La etiqueta -1 es una salida VÁLIDA y esperada del algoritmo, como ya se vio con los 3 outliers del código — no indica ningún error de carga de datos, sino simplemente falta de densidad alrededor de ese punto."
   ],
   "steps": [
    "Recordá qué significa -1 en el código: un punto sin suficientes vecinos cerca como para pertenecer a un grupo denso.",
    "Trasladá esa misma idea al ejemplo epidemiológico: un caso geográficamente aislado, sin otros casos cerca, no forma parte de ningún foco.",
    "Ese caso aislado, por no cumplir el criterio de densidad, quedaría marcado con -1 — igual que los outliers del código.",
    "Por eso -1 representaría un caso aislado, no un foco denso ni un error de datos."
   ],
   "stakes": "En vigilancia epidemiológica real, identificar casos aislados (marcados como -1) frente a focos densos ayuda a distinguir un caso importado o sin relación de un verdadero brote local en expansión."
  }
 ],
 [
  {
   "question": "A diferencia de KMeans(n_clusters=2), DBSCAN no recibe la cantidad de grupos (k) como parámetro y aun así encuentra 2 clusters reales. ¿Cómo decide DBSCAN cuántos grupos hay?",
   "type": "mc",
   "options": [
    "Los grupos emergen de conectar puntos que están suficientemente cerca unos de otros (dentro de eps) y tienen suficientes vecinos (min_samples) — el número de grupos es una CONSECUENCIA de los datos, no un parámetro de entrada",
    "DBSCAN prueba con distintos valores de k automáticamente hasta encontrar el mejor",
    "DBSCAN siempre encuentra exactamente 2 clusters, sin importar los datos",
    "DBSCAN le pide al usuario que confirme cuántos grupos hay antes de terminar"
   ],
   "correct": 0,
   "solution": "DBSCAN no busca 'k' en ningún momento — simplemente conecta puntos densos entre sí según eps y min_samples, y el NÚMERO de grupos resultantes es lo que emerge de esa conexión, no algo que se le indique de antemano. En este caso, la estructura real de los datos (dos lunas separadas) hizo que emergieran exactamente 2 grupos.",
   "whyNot": [
    null,
    "DBSCAN no prueba múltiples valores de k ni hace ninguna búsqueda de ese tipo — sus únicos parámetros son eps y min_samples, que no son 'la cantidad de grupos' sino criterios de densidad.",
    "DBSCAN puede encontrar cualquier cantidad de grupos según los datos (0, 1, 2, o muchos) — que este ejemplo particular haya dado 2 es resultado de la estructura real de los datos, no una constante del algoritmo.",
    "DBSCAN no tiene ninguna interacción con el usuario durante su ejecución — corre de principio a fin sin pedir confirmaciones, como se ve en el propio código."
   ],
   "steps": [
    "A diferencia de KMeans(n_clusters=2), en la llamada a DBSCAN no aparece ningún número de grupos como parámetro.",
    "DBSCAN solo recibe eps (radio) y min_samples (vecinos mínimos) — parámetros de DENSIDAD, no de cantidad de grupos.",
    "Los grupos se forman conectando puntos densos entre sí; cuántos grupos resultan de esa conexión depende pura y exclusivamente de la estructura real de los datos.",
    "En este caso, la estructura (dos lunas separadas) hizo que emergieran exactamente 2 grupos, sin que nadie se lo dijera al algoritmo."
   ],
   "stakes": "En un proyecto real donde NO se sabe de antemano cuántos grupos hay (por ejemplo, tipos de fraude nuevos que van apareciendo), pedir un 'k' fijo como en K-Means obliga a inventar un número — DBSCAN evita ese supuesto."
  },
  {
   "question": "El código imprime que DBSCAN logra un ARI de 1,0 recuperando las dos lunas reales. ¿Qué significa concretamente ese valor máximo de 1,0?",
   "type": "mc",
   "options": [
    "Que la agrupación que encontró DBSCAN coincide perfectamente con la estructura real de las dos lunas (y_true), sin ningún punto agrupado de forma distinta a la real",
    "Que DBSCAN tardó exactamente 1 segundo en procesar los datos",
    "Que se formó exactamente 1 cluster en total, sin ningún punto de ruido",
    "Que el 100% de los puntos fueron marcados como ruido (-1)"
   ],
   "correct": 0,
   "solution": "ARI (Adjusted Rand Index) mide qué tan bien coincide una agrupación encontrada con la agrupación real (y_true); su valor máximo, 1,0, significa coincidencia perfecta. Que DBSCAN logre exactamente 1,0 confirma que recuperó las dos lunas reales sin errores de agrupación, un resultado mucho mejor que el 0,214 de KMeans sobre los mismos datos.",
   "whyNot": [
    null,
    "ARI no mide tiempo de ejecución — es una métrica puramente de similitud entre dos agrupaciones (la encontrada y la real), sin ninguna relación con segundos de cómputo.",
    "El código ya muestra que DBSCAN encuentra 2 clusters (no 1) reproduciendo las dos lunas, además de marcar 3 puntos como ruido — el valor de ARI no describe la cantidad de clusters encontrados.",
    "Es justo lo contrario: los 3 outliers SÍ quedan marcados como ruido, pero eso es un hecho aparte del ARI, que se calcula solo sobre los primeros 50 puntos de las lunas (no sobre los outliers) y da 1,0 porque esos 50 quedaron agrupados perfectamente."
   ],
   "steps": [
    "ARI compara la agrupación que encontró el algoritmo contra la agrupación real (y_true) — no mide velocidad ni cantidad de ruido.",
    "Su rango va de valores bajos (mala coincidencia) hasta 1,0 (coincidencia perfecta).",
    "Que DBSCAN logre 1,0 exactamente significa que agrupó las dos lunas EXACTAMENTE como estaban divididas en la realidad, sin ningún error.",
    "Por eso 1,0 es el mejor resultado posible para esta métrica, muy por encima del 0,214 que logra KMeans sobre los mismos datos."
   ],
   "stakes": "En cualquier evaluación real de un algoritmo de clustering contra una verdad conocida (por ejemplo, en un dataset de prueba con etiquetas ya sabidas), un ARI cercano a 1,0 es la señal de que el algoritmo realmente está capturando la estructura real, no solo produciendo grupos al azar."
  }
 ],
 [
  {
   "question": "¿Por qué DBSCAN sería más apropiado que K-Means para detectar transacciones fraudulentas en un banco (donde el fraude es raro y no sigue un patrón fijo)?",
   "type": "mc",
   "options": [
    "Porque DBSCAN puede dejar esas transacciones como 'ruido' (fuera de cualquier grupo denso de comportamiento normal), mientras que K-Means las forzaría dentro de algún cluster como si fueran normales",
    "Porque DBSCAN es más rápido de calcular que K-Means en cualquier situación",
    "Porque K-Means no puede procesar datos financieros por su formato",
    "Porque DBSCAN necesita menos datos de entrenamiento que K-Means"
   ],
   "correct": 0,
   "solution": "El propio ejemplo del código ilustra esto: K-Means, al no tener noción de 'ruido', mete los 3 outliers dentro de algún cluster sí o sí — tratándolos como si fueran parte de un comportamiento normal. DBSCAN los deja afuera, marcados como -1, que es justo la señal que interesa para detectar algo anómalo como un fraude.",
   "whyNot": [
    null,
    "La velocidad relativa entre DBSCAN y KMeans depende del tamaño y densidad de los datos — no es una ventaja universal ni la razón por la que DBSCAN encaja mejor con detección de anomalías.",
    "K-Means puede procesar cualquier dato numérico, incluidos datos financieros — el formato de los datos no es el problema, es la falta de una categoría 'esto no encaja en ningún patrón'.",
    "Ninguno de los dos algoritmos tiene un requisito de cantidad mínima de datos específico para este caso de uso — la ventaja de DBSCAN es conceptual (tiene noción de ruido), no de cantidad de datos necesarios."
   ],
   "steps": [
    "K-Means no tiene ningún concepto de 'punto que no pertenece a ningún grupo' — TODO punto termina asignado a algún centroide, sí o sí.",
    "Eso significa que una transacción rara (fraude) quedaría metida dentro de algún cluster, como si fuera comportamiento normal.",
    "DBSCAN sí puede dejar un punto sin asignar (etiqueta -1) si no tiene suficiente densidad de vecinos parecidos alrededor.",
    "Esa capacidad de decir 'esto no encaja en ningún patrón normal' es justo la señal útil para detectar fraude."
   ],
   "stakes": "Es exactamente el motivo por el que sistemas antifraude reales usan algoritmos con noción de 'ruido': forzar cada transacción dentro de un grupo, como haría K-Means, esconde justo las transacciones que más interesa detectar."
  },
  {
   "question": "Según la aplicación real del tema, ¿por qué DBSCAN es útil para limpiar datos de sensores donde algunas lecturas son simplemente basura (ruido de medición)?",
   "type": "mc",
   "options": [
    "Porque puede dejar esas lecturas defectuosas marcadas como ruido (-1), sin forzarlas dentro de ningún grupo válido de lecturas normales, algo que K-Means no puede evitar hacer",
    "Porque DBSCAN corrige automáticamente el valor numérico de las lecturas defectuosas",
    "Porque DBSCAN elimina físicamente esas filas del archivo de datos original",
    "Porque DBSCAN necesita menos sensores para funcionar correctamente"
   ],
   "correct": 0,
   "solution": "El propio ejemplo lo dice: DBSCAN sirve para 'limpiar datos de sensores donde algunas lecturas son simplemente basura y no deberían forzarse dentro de ningún grupo — algo que K-Means no puede evitar hacer'. Igual que con los 3 outliers del código, una lectura de sensor claramente anómala quedaría marcada como -1 en vez de mezclada dentro de un grupo de lecturas normales.",
   "whyNot": [
    null,
    "DBSCAN no modifica ni corrige ningún valor — solo asigna etiquetas de grupo (o de ruido); los datos originales quedan intactos, sea cual sea su etiqueta.",
    "DBSCAN no borra filas del dataset — simplemente las etiqueta como ruido (-1); sigue siendo tarea de quien analiza los datos decidir qué hacer después con esas filas marcadas.",
    "La cantidad de sensores no tiene relación con esta ventaja de DBSCAN — la ventaja es conceptual (tiene noción de ruido), no depende de cuántos sensores generen los datos."
   ],
   "steps": [
    "Con sensores reales, algunas lecturas van a ser simplemente basura (fallas de medición, ruido eléctrico, etc.).",
    "K-Means, al no tener noción de 'ruido', forzaría esas lecturas defectuosas dentro de algún grupo de lecturas normales, contaminándolo.",
    "DBSCAN puede dejar esas lecturas fuera de cualquier grupo, marcadas con -1, sin que contaminen ningún grupo de lecturas válidas.",
    "Por eso DBSCAN es una herramienta natural para limpiar este tipo de datos ruidosos."
   ],
   "stakes": "En una planta industrial real con cientos de sensores, tratar una lectura defectuosa como si fuera parte de un patrón normal (como haría K-Means) puede disparar alertas falsas o esconder fallas reales — DBSCAN evita mezclar lo anómalo con lo normal."
  }
 ],
 [
  {
   "question": "En el código, ¿qué diferencia hay entre gm.predict(punto) y gm.predict_proba(punto) para ese mismo punto?",
   "type": "mc",
   "options": [
    "predict() da la asignación DURA (un solo grupo, el más probable); predict_proba() da la probabilidad de pertenecer a CADA uno de los 3 grupos (0%, 57,5%, 42,5%)",
    "predict() y predict_proba() siempre devuelven exactamente el mismo resultado, solo que en formatos distintos",
    "predict_proba() vuelve a entrenar el modelo desde cero con el punto nuevo antes de responder",
    "predict() devuelve las 3 probabilidades y predict_proba() devuelve solo la etiqueta final del grupo"
   ],
   "correct": 0,
   "solution": "El código lo muestra en paralelo: gm.predict(punto) imprime [1] -- un único número, el grupo más probable. gm.predict_proba(punto)[0] imprime [0.0, 0.575, 0.425] -- las 3 probabilidades, una por grupo, que suman 1.0. La primera es la asignación dura (soft clustering colapsado a una sola etiqueta); la segunda es la información completa, blanda (soft clustering).",
   "whyNot": [
    null,
    "Tienen forma completamente distinta: predict() da un entero (1), predict_proba() da un array de 3 probabilidades ([0.0, 0.575, 0.425]) -- no son 'el mismo resultado en otro formato', predict() literalmente descarta información que predict_proba() sí conserva.",
    "predict_proba() usa el modelo YA entrenado (gm, ajustado antes con gm.fit(X)) -- solo evalúa el punto nuevo contra los parámetros existentes, no reentrena nada.",
    "Es exactamente al revés: predict() da la etiqueta única (el grupo más probable), predict_proba() da las probabilidades de los 3 grupos -- así se ve en el propio código."
   ],
   "steps": [
    "Mirá las dos líneas del código en paralelo: gm.predict(punto) imprime [1] — un solo número.",
    "gm.predict_proba(punto)[0] imprime [0.0, 0.575, 0.425] — tres números que suman 1.0.",
    "Un solo número = la asignación dura (el grupo más probable, colapsado a una sola etiqueta). Tres números = la probabilidad completa de pertenecer a CADA grupo.",
    "Por eso predict() da el resultado duro y predict_proba() da toda la información blanda (soft)."
   ],
   "stakes": "En un sistema real donde la decisión depende de qué tan seguro está el modelo (por ejemplo, escalar un caso dudoso a un humano), quedarse solo con predict() en vez de predict_proba() hace perder exactamente esa información."
  },
  {
   "question": "El código imprime 'convergio: True -- en 9 iteraciones (EM: expectation-maximization)'. ¿Qué nos dice esto sobre cómo llega GMM a su resultado final?",
   "type": "mc",
   "options": [
    "Que, como K-Means, GMM es un algoritmo iterativo que repite pasos (en este caso, del algoritmo EM) hasta estabilizarse — en este caso, tardó 9 repeticiones en dejar de cambiar significativamente",
    "Que el modelo tardó exactamente 9 segundos en entrenar",
    "Que se probaron 9 valores distintos de n_components antes de elegir 3",
    "Que hubo 9 errores durante el entrenamiento que el modelo tuvo que corregir"
   ],
   "correct": 0,
   "solution": "El propio comentario del código aclara que EM significa 'expectation-maximization', y la teoría explica que el algoritmo 'se parece a K-Means (también arranca al azar y repite pasos hasta converger)'. n_iter_=9 es literalmente cuántas veces se repitió ese ciclo de pasos antes de que el modelo dejara de cambiar de forma significativa (convergiera).",
   "whyNot": [
    null,
    "n_iter_ cuenta REPETICIONES del algoritmo, no tiempo transcurrido — el número de iteraciones no tiene ninguna relación directa con segundos de reloj.",
    "El código fija n_components=3 directamente en GaussianMixture(n_components=3, ...) — no se prueban distintos valores de esa cantidad de grupos durante el entrenamiento, n_iter_ se refiere a otra cosa completamente distinta.",
    "Convergencia no significa 'corregir errores' — es el proceso normal y esperado por el cual un algoritmo iterativo deja de cambiar significativamente sus parámetros entre una repetición y la siguiente; no indica ningún fallo."
   ],
   "steps": [
    "El comentario del código aclara que EM significa expectation-maximization, un algoritmo iterativo.",
    "La teoría lo compara directamente con K-Means: 'también arranca al azar y repite pasos hasta converger'.",
    "n_iter_=9 es la cantidad de veces que se repitió ese ciclo de pasos antes de estabilizarse (converger).",
    "Por eso este dato describe el PROCESO iterativo de ajuste del modelo, no tiempo de reloj ni búsqueda de hiperparámetros."
   ],
   "stakes": "Cuando un modelo real basado en EM no converge (converged_=False) incluso después de muchas iteraciones, es una señal de alerta de que puede haber un problema con los datos o los hiperparámetros elegidos, algo que conviene revisar antes de confiar en el resultado."
  }
 ],
 [
  {
   "question": "El código imprime gm.weights_ = [0,278, 0,315, 0,408]. ¿Qué representa cada uno de esos 3 números?",
   "type": "mc",
   "options": [
    "El peso relativo (proporción esperada) de cada una de las 3 Gaussianas del modelo -- qué tan grande es cada grupo dentro del total, no la probabilidad de un punto en particular",
    "La probabilidad de que el punto elegido (índice 35) pertenezca a cada uno de los 3 grupos",
    "La cantidad exacta de los 40 puntos que caen dentro de cada grupo",
    "La distancia euclidiana entre el centro de cada grupo y el origen (0,0)"
   ],
   "correct": 0,
   "solution": "weights_ (φ) es un parámetro GLOBAL del modelo entero: cuánto pesa cada una de las k Gaussianas al elegir de cuál grupo sale un punto nuevo cualquiera. Es distinto de predict_proba(punto), que da la probabilidad de UN punto específico -- weights_ no cambia según qué punto se consulte, es fijo una vez entrenado el modelo.",
   "whyNot": [
    null,
    "Eso describe a predict_proba(punto), que sí depende de qué punto se consulte (por eso el código lo calcula aparte, para el índice 35) -- weights_ es un solo valor por grupo, igual para cualquier punto que se pregunte.",
    "Los pesos son proporciones estimadas por el modelo (pueden no coincidir exactamente con un conteo de puntos), y ni siquiera existe una asignación de puntos 'exacta' en GMM -- cada punto tiene una probabilidad repartida entre grupos, no una membresía única y contable.",
    "weights_ no tiene ninguna relación con distancias geométricas al origen -- eso sería más parecido a describir means_ (los centros), y ni siquiera así: la distancia al origen no es un parámetro del modelo."
   ],
   "steps": [
    "gm.weights_ tiene 3 números, uno por Gaussiana del modelo — y no cambian según qué punto consultes.",
    "Compará eso con predict_proba(punto), que sí depende del punto específico elegido (índice 35).",
    "Un valor que es fijo para TODO el modelo, no por punto, describe algo global: qué tan grande/frecuente es cada grupo en el conjunto completo.",
    "Por eso weights_ es la proporción esperada de cada grupo, no la probabilidad de un punto en particular."
   ],
   "stakes": "Confundir un parámetro global del modelo (weights_) con la probabilidad de un caso puntual es un error de interpretación común en reportes reales — puede llevar a conclusiones erróneas sobre un cliente o caso específico."
  },
  {
   "question": "Según la aplicación real del tema, en la segmentación de imágenes médicas, un píxel en el borde de un tumor puede tener 60% de probabilidad de ser tejido enfermo y 40% de ser tejido sano. ¿Por qué esta información sería más útil para un diagnóstico que una asignación DURA (100% enfermo o 100% sano)?",
   "type": "mc",
   "options": [
    "Porque conserva la incertidumbre real del caso límite, permitiendo que un médico revise específicamente esos píxeles dudosos en vez de recibir una respuesta tajante que esconde lo ambiguo del caso",
    "Porque una asignación dura siempre es matemáticamente incorrecta, mientras que una probabilidad nunca se equivoca",
    "Porque los píxeles con probabilidades intermedias ocupan menos espacio de almacenamiento",
    "Porque el clustering blando es más rápido de calcular que el clustering duro en cualquier caso"
   ],
   "correct": 0,
   "solution": "Igual que en el ejemplo del punto que cae justo entre dos grupos (índice 35, con predict_proba() dando 57,5%/42,5%), un píxel de borde con 60%/40% conserva la ambigüedad real del caso. Una asignación dura (K-Means) forzaría una etiqueta única (100% de un lado), escondiendo que en realidad es un caso límite — información valiosa para que un profesional médico revise ese caso puntual.",
   "whyNot": [
    null,
    "Ninguna de las dos formas de asignación es 'matemáticamente incorrecta' por sí misma — son dos formas distintas de reportar el mismo resultado subyacente; la ventaja de la probabilística es que conserva más información, no que sea más 'correcta'.",
    "La cantidad de espacio de almacenamiento no es la razón de esta ventaja — el motivo es la calidad de la información para la toma de decisiones médicas, no el tamaño de los datos guardados.",
    "La velocidad de cómputo no es lo que hace útil al clustering blando en este contexto — de hecho, GMM (blando) suele requerir más cómputo que K-Means (duro) por iteración; la ventaja acá es de INFORMACIÓN, no de velocidad."
   ],
   "steps": [
    "Un modelo duro (como K-Means) reportaría solo una etiqueta final para ese píxel — por ejemplo, 'enfermo', sin matices.",
    "Un modelo blando (como GMM) reporta en cambio la probabilidad completa: 60% enfermo, 40% sano.",
    "Esa segunda forma deja ver que el caso es AMBIGUO — información que un médico puede usar para decidir revisar ese píxel con más cuidado.",
    "Por eso la asignación blanda es más útil en un contexto donde la incertidumbre importa para la decisión final."
   ],
   "stakes": "En radiología asistida por computadora, forzar una etiqueta binaria en los bordes de una lesión puede ocultar justo los casos más difíciles de diagnosticar — los que más se beneficiarían de una segunda opinión humana."
  }
 ],
 [
  {
   "question": "Según la teoría del clustering, ¿cuál es la diferencia de fondo entre el clustering DURO (K-Means, DBSCAN) y el clustering BLANDO (soft) de GMM?",
   "type": "mc",
   "options": [
    "El clustering duro asigna cada punto a un único grupo sin matices; el clustering blando (GMM) estima, para cada punto, una probabilidad de pertenecer a cada uno de los grupos",
    "El clustering duro solo funciona con 2 grupos; el clustering blando permite cualquier cantidad de grupos",
    "El clustering blando (GMM) no necesita ningún dato de entrada, a diferencia del duro",
    "El clustering duro es más lento de calcular que el clustering blando en todos los casos"
   ],
   "correct": 0,
   "solution": "Es la distinción central del tema: 'duro' significa una etiqueta única y definitiva por punto (K-Means dice 'grupo 1' y punto), 'blando' significa una distribución de probabilidad sobre todos los grupos posibles (GMM dice '57,5% grupo 1, 42,5% grupo 2, 0% grupo 0'). Ambos enfoques pueden usarse para descubrir estructura sin etiquetas, pero difieren en cuánta incertidumbre conservan en la respuesta final.",
   "whyNot": [
    null,
    "K-Means, DBSCAN y GMM pueden usarse con cualquier cantidad de grupos (n_clusters o n_components) -- el número de grupos no es lo que distingue duro de blando, ambos tipos manejan k arbitrario.",
    "GMM necesita exactamente los mismos datos de entrada que K-Means o DBSCAN (una matriz X de puntos) -- gm.fit(X) recibe datos igual que km.fit(X), ninguno de los dos funciona sin datos.",
    "La velocidad relativa depende del tamaño de los datos y la implementación, no es una propiedad universal de 'duro vs blando' -- de hecho GMM (con EM) suele requerir más cómputo por iteración que K-Means, no menos."
   ],
   "steps": [
    "K-Means y DBSCAN, en el código, siempre devuelven UNA sola etiqueta de grupo por punto — sin matices.",
    "GMM, en cambio, con predict_proba(), devuelve una distribución de probabilidad sobre TODOS los grupos posibles para ese punto.",
    "Esa diferencia — una etiqueta única vs. una distribución de probabilidades — es la definición misma de duro vs. blando (soft)."
   ],
   "stakes": "En decisiones reales donde la incertidumbre importa (por ejemplo, un diagnóstico asistido), un modelo blando que dice '57% probable' es mucho más útil y honesto que uno duro que solo dice 'sí' o 'no'."
  },
  {
   "question": "Según la aplicación real del tema, además de agrupar puntos, GMM puede usarse para detección de anomalías fijando un umbral de densidad (por ejemplo, el percentil 4 más bajo) con score_samples(). ¿En qué se basa esa detección de anomalías?",
   "type": "mc",
   "options": [
    "En marcar como posible anomalía cualquier instancia que caiga en una región de muy baja densidad según el modelo ajustado — es decir, puntos donde ninguna de las Gaussianas del modelo asigna mucha probabilidad",
    "En contar cuántas veces aparece exactamente el mismo valor repetido en el dataset",
    "En comparar cada punto nuevo contra y_true para ver si coincide con la etiqueta real",
    "En medir el tiempo que tarda el modelo en procesar cada punto nuevo"
   ],
   "correct": 0,
   "solution": "El propio ejemplo lo describe: 'cualquier instancia que caiga en una región de muy baja densidad según el modelo (medida con score_samples()) se puede marcar como posible fraude bancario o defecto de fabricación, fijando un umbral de densidad (por ejemplo, el percentil 4 más bajo)'. La idea es que los puntos normales caen donde las Gaussianas del modelo concentran probabilidad, y los puntos anómalos caen en zonas de baja densidad, lejos de esas campanas.",
   "whyNot": [
    null,
    "score_samples() no cuenta repeticiones de valores — mide la densidad de probabilidad del modelo Gaussiano en la posición de cada punto, un concepto continuo, no un conteo de duplicados.",
    "Este tipo de detección de anomalías es justamente un uso de aprendizaje NO supervisado — no requiere ninguna etiqueta real (y_true) contra la cual comparar, se basa solo en la densidad estimada por el propio modelo.",
    "score_samples() no mide tiempo de procesamiento — es una medida de qué tan probable es, según el modelo, que un punto haya salido de alguna de las Gaussianas ajustadas."
   ],
   "steps": [
    "GMM modela los datos normales como generados por k Gaussianas superpuestas.",
    "score_samples() mide, para cualquier punto, qué tan probable es (densidad) que haya salido de esa mezcla de Gaussianas.",
    "Un punto en una zona de muy baja densidad no encaja bien con ninguna de las Gaussianas del modelo — es 'raro' respecto al patrón general.",
    "Fijando un umbral (como el percentil 4 más bajo), esos puntos raros se marcan como posibles anomalías, sin necesitar ninguna etiqueta de 'fraude' previa."
   ],
   "stakes": "Este es un mecanismo real de detección de fraude bancario: en vez de reglas fijas escritas a mano, se entrena un modelo de densidad sobre transacciones normales y se marca como sospechoso todo lo que cae fuera de ese patrón habitual."
  }
 ],
 [
  {
   "question": "En el código, K-Means también predice 'grupo 1' para el mismo punto que GMM, pero no puede decir 'con 57,5% de probabilidad'. ¿Por qué?",
   "type": "mc",
   "options": [
    "Porque K-Means no tiene un método predict_proba(): solo calcula distancia al centroide más cercano, sin ningún modelo de forma/densidad que permita estimar una probabilidad de pertenencia",
    "Porque hay un error en el código que impide calcular la probabilidad para K-Means",
    "Porque K-Means usa una escala de probabilidad distinta (de 0 a 10 en vez de 0 a 1)",
    "Porque el punto elegido queda fuera del rango de valores que K-Means puede procesar"
   ],
   "correct": 0,
   "solution": "K-Means fue diseñado únicamente para minimizar la distancia a centroides -- no modela la forma, el tamaño ni la densidad de cada grupo, así que no tiene ninguna base matemática para estimar 'qué tan probable' es que un punto pertenezca a un grupo u otro. GMM sí modela eso explícitamente (media, covarianza y peso de cada Gaussiana), y por eso predict_proba() existe en GaussianMixture pero no en KMeans.",
   "whyNot": [
    null,
    "No es un bug: km.predict(punto) funciona y devuelve un resultado válido ([1]) -- simplemente KMeans nunca implementó predict_proba() porque conceptualmente no tiene de dónde sacar esa probabilidad.",
    "Ninguno de los dos algoritmos usa una escala de 0 a 10 -- GMM (predict_proba) trabaja siempre en probabilidades de 0 a 1 que suman 1.0, y K-Means directamente no produce ningún número de 'probabilidad'.",
    "K-Means procesa el punto sin problema (km.predict(punto) da [1], un resultado válido) -- el punto no está 'fuera de rango', simplemente el algoritmo no ofrece una salida probabilística para ningún punto, nunca."
   ],
   "steps": [
    "K-Means solo calcula la distancia del punto a cada centroide y elige el más cercano — no modela nada más sobre la forma de cada grupo.",
    "GMM sí modela explícitamente la forma completa de cada grupo: media, covarianza (dispersión) y peso — con eso puede calcular qué tan probable es cada asignación.",
    "Sin ese modelo de forma/densidad, K-Means no tiene ninguna base matemática para dar un número como '57,5% de probabilidad' — solo puede decir 'el más cercano es este'.",
    "Por eso predict_proba() existe en GaussianMixture pero no existe en KMeans."
   ],
   "stakes": "Pedir 'la probabilidad' a un modelo que no la calcula (como K-Means) es un error real y frecuente en código copiado de otro contexto — entender por qué no existe evita perder tiempo buscando un método que nunca va a aparecer."
  },
  {
   "question": "Según la aplicación real del tema, GMM es un modelo 'generativo' porque se pueden generar puntos nuevos con sample(). ¿Qué tiene que ver esto con que GMM modele cada grupo como una distribución Gaussiana completa (media, covarianza y peso)?",
   "type": "mc",
   "options": [
    "Que, al tener un modelo matemático completo de cómo se distribuyen los puntos dentro de cada grupo, GMM puede usar ese modelo para producir puntos sintéticos nuevos y verosímiles — algo que K-Means no puede hacer, porque solo guarda posiciones de centroides, sin ninguna noción de dispersión",
    "Que sample() simplemente copia puntos ya existentes del dataset original, sin generar nada nuevo",
    "Que K-Means también tiene un método sample() equivalente, con el mismo resultado",
    "Que la capacidad de generar puntos nuevos no tiene ninguna relación con cómo GMM modela cada grupo"
   ],
   "correct": 0,
   "solution": "GMM modela cada grupo con una media, una covarianza (forma/dispersión) y un peso — un modelo probabilístico completo de cómo se distribuyen los puntos. Eso le permite, con sample(), 'tirar los dados' según ese modelo y producir puntos nuevos y verosímiles. K-Means solo guarda la posición de cada centroide, sin ningún modelo de dispersión, así que no tiene información suficiente para generar puntos nuevos realistas.",
   "whyNot": [
    null,
    "sample() genera puntos NUEVOS a partir del modelo probabilístico ajustado, no copia puntos existentes del dataset original — es lo que hace a GMM un modelo 'generativo'.",
    "KMeans no tiene ningún método sample() equivalente — solo calcula centroides (posiciones), sin ningún modelo de covarianza que permita generar puntos nuevos de forma verosímil.",
    "Es exactamente lo contrario: la capacidad generativa de GMM depende directamente de que modele la forma completa (media, covarianza, peso) de cada grupo — sin ese modelo, no habría de dónde generar puntos nuevos coherentes."
   ],
   "steps": [
    "GMM no solo guarda un centro por grupo (como K-Means) — guarda también la covarianza (forma/dispersión) y el peso de cada Gaussiana.",
    "Ese modelo completo describe matemáticamente cómo se distribuyen los puntos DENTRO de cada grupo, no solo dónde está su centro.",
    "Con esa información, GMM puede 'tirar los dados' siguiendo esa distribución y generar puntos nuevos que parezcan pertenecer realmente a ese grupo.",
    "K-Means, al no tener ningún modelo de dispersión (solo centroides), no tiene base matemática para generar puntos nuevos verosímiles."
   ],
   "stakes": "Esta capacidad generativa es la base de técnicas reales de aumento de datos (data augmentation): generar ejemplos sintéticos adicionales de una clase poco representada, entrenando después un modelo con más datos realistas."
  }
 ]
];

/* ──────────── Modo Maestro NS (No Supervisado) ────────────
   Mismo patrón exacto que master-as.js (ver ese archivo para el diseño
   original): progreso propio en localStorage, reutiliza runCode()/panel de
   pasos (el código sigue siendo Python), teoría + Visualízalo + Aplicación
   real + quiz con whyNot completo + confianza + razonamiento + Leitner. */
const MASTER_NS_KEY='pyvizMasterNsProgressV1';
let _nsOn=false, _nsPos=0, _nsDone=new Set(), _nsQuizAnswered=false, _nsQuizShuffledCorrect=null, _nsCurrentQuiz=null, _nsQuizSubPos=0, _nsQuizOrder=null;

function _loadNsProgress(){
  try{
    const raw=localStorage.getItem(MASTER_NS_KEY);
    if(raw){ const d=JSON.parse(raw); _nsDone=new Set(d.done||[]); }
  }catch(e){ _nsDone=new Set(); }
}
function _saveNsProgress(){
  try{ localStorage.setItem(MASTER_NS_KEY, JSON.stringify({done:[..._nsDone]})); }catch(e){}
}
function _nsFirstPending(){
  for(let i=0;i<EX_NS.length;i++) if(!_nsDone.has(i)) return i;
  return EX_NS.length-1;
}
function toggleMasterNs(){
  if(_nsOn){ exitMasterNs(); return; }
  if(_masterOn) exitMasterMode();
  if(_aoOn) exitMasterAo();
  if(_mathOn) exitMasterMath();
  if(_raOn) exitMasterRa();
  if(typeof _asOn!=='undefined' && _asOn) exitMasterAs();
  if(typeof _nsOn!=='undefined' && _nsOn && 'ns'!=='ns') exitMasterNs();
  if(typeof _rnOn!=='undefined' && _rnOn && 'ns'!=='rn') exitMasterRn();
  if(typeof _rfOn!=='undefined' && _rfOn && 'ns'!=='rf') exitMasterRf();
  if(_reviewOn) exitReviewMode();
  if(typeof _calOn!=='undefined' && _calOn) _calClose();
  if(typeof _reportOn!=='undefined' && _reportOn) _reportClose();
  if(typeof _sessionOn!=='undefined' && _sessionOn) _sessionClosePanel();
  if(typeof _errorsOn!=='undefined' && _errorsOn) _errorsClose();
  if(typeof _examOn!=='undefined' && _examOn) _examClose();
  _nsOn=true;
  _loadNsProgress();
  document.getElementById('masterNsBar').style.display='flex';
  const b=document.getElementById('bMasterNs');
  if(b){ b.textContent='🧩 Modo Maestro NS (activo)'; b.classList.add('btn-looping'); }
  autoLayout();
  _nsGoTo(_nsFirstPending());
}
function exitMasterNs(){
  _nsOn=false;
  document.getElementById('masterNsBar').style.display='none';
  document.getElementById('masterNsChecklist').style.display='none';
  const b=document.getElementById('bMasterNs');
  if(b){ b.textContent='🧩 Modo Maestro NS'; b.classList.remove('btn-looping'); }
  autoLayout();
}
function _nsGoTo(idx){
  _nsPos=Math.max(0, Math.min(EX_NS.length-1, idx));
  _nsQuizSubPos=0;
  document.getElementById('codeInput').value=EX_NS[_nsPos].code;
  renderLineNums();
  document.getElementById('frBody').innerHTML='<div class="ob-ph">No variables yet</div>';
  document.getElementById('obBody').innerHTML='<div class="ob-ph">Click [→] to inspect</div>';
  document.getElementById('outBody').innerHTML='<span class="out-empty">No output yet</span>';
  runCode();
  _nsRenderBar();
  _resetSelfExplain('ns');
  _nsRenderTheory();
  _nsRenderConceptViz();
  _nsRenderApplication();
  _nsRenderCodeAnatomy();
  _nsRenderQuiz();
}
function _nsRenderTheory(){
  const t=EX_NS[_nsPos].theory;
  const block=document.getElementById('nsTheoryBlock');
  if(!t){ block.style.display='none'; return; }
  if(_theoryIsLocked('ns', 'ns', _nsPos)){
    document.getElementById('nsTheoryBody').innerHTML=_theoryGateHtml('ns', _nsPos, '_nsRenderTheory');
    block.style.display='block';
    return;
  }
  document.getElementById('nsTheoryBody').innerHTML=t;
  block.style.display='block';
}
function _nsRenderConceptViz(){
  const viz=EX_NS[_nsPos].viz;
  const block=document.getElementById('nsConceptVizBlock');
  if(!viz){ block.style.display='none'; return; }
  const svg=renderConceptViz(viz);
  if(!svg){ block.style.display='none'; return; }
  document.getElementById('nsConceptVizBody').innerHTML=svg;
  block.style.display='block';
}
function _nsRenderApplication(){
  const a=EX_NS[_nsPos].application;
  const block=document.getElementById('nsApplicationBlock');
  if(!a){ block.style.display='none'; return; }
  document.getElementById('nsApplicationBody').innerHTML=a;
  block.style.display='block';
}
/* Panel "🔬 Anatomía del código" -- ver la cabecera igual en master-ra.js
   para el porqué. Piloto hecho a mano, un tema por modo. */
function _nsRenderCodeAnatomy(){
  const spec=EX_NS[_nsPos].codeAnatomy;
  const block=document.getElementById('nsCodeAnatomyBlock');
  if(!spec){ block.style.display='none'; return; }
  const svg=renderCodeAnatomy(spec);
  if(!svg){ block.style.display='none'; return; }
  document.getElementById('nsCodeAnatomyBody').innerHTML=svg;
  block.style.display='block';
}
function _nsRenderQuiz(){
  const bank=NS_QUIZ[_nsPos];
  const q=bank[_nsQuizSubPos];
  _nsCurrentQuiz=q;
  _nsQuizAnswered=false;
  document.getElementById('nsQuizProgress').textContent=
    bank.length>1 ? `(pregunta ${_nsQuizSubPos+1}/${bank.length} de este tema)` : '';
  document.getElementById('nsQuizNextBtn').style.display='none';
  document.getElementById('nsQuizQuestion').innerHTML=q.question;
  const optWrap=document.getElementById('nsQuizOptions');
  const numWrap=document.getElementById('nsQuizNumericWrap');
  if(q.type==='mc'){
    numWrap.style.display='none';
    const res=_quizRenderAnswerArea('ns', 'ns', _nsPos, q);
    _nsQuizShuffledCorrect=res.shuffled?res.shuffled.correct:null;
    _nsQuizOrder=res.shuffled?res.shuffled.order:null;
  } else {
    optWrap.style.display='none';
    numWrap.style.display='flex';
    const inp=document.getElementById('nsQuizNumericInput');
    inp.value=''; inp.disabled=false;
    _nsQuizShuffledCorrect=null;
    _nsQuizOrder=null;
  }
  document.getElementById('nsQuizFeedback').style.display='none';
  document.getElementById('nsQuizSolutionBtn').style.display='none';
  const solBody=document.getElementById('nsQuizSolutionBody');
  solBody.style.display='none'; solBody.innerHTML='';
  _quizResetExtras('ns');
}
function _nsCheckQuizAnswer(selectedIdx){
  if(_nsQuizAnswered) return;
  const q=_nsCurrentQuiz;
  let ok=false;
  if(q.type==='mc'){
    ok = selectedIdx===_nsQuizShuffledCorrect;
    document.querySelectorAll('#nsQuizOptions .math-option').forEach((btn,i)=>{
      btn.classList.remove('math-option-correct','math-option-wrong');
      if(ok){
        btn.disabled=true;
        if(i===_nsQuizShuffledCorrect) btn.classList.add('math-option-correct');
      } else if(i===selectedIdx){
        btn.classList.add('math-option-wrong');
      }
    });
  } else {
    const inp=document.getElementById('nsQuizNumericInput');
    const val=parseFloat(inp.value.trim().replace(',','.'));
    const dec=q.decimals||0;
    const pw=Math.pow(10,dec);
    ok = !isNaN(val) && Math.round(val*pw)===Math.round(q.correct*pw);
    inp.disabled=ok;
  }
  if(ok) _nsQuizAnswered=true;
  _recordAttempt('ns', _nsPos, ok);
  _nsRenderTheory();
  const fb=document.getElementById('nsQuizFeedback');
  fb.style.display='block';
  fb.className='math-feedback '+(ok?'math-feedback-ok':'math-feedback-bad');
  const whyNot = (!ok && q.type==='mc' && q.whyNot && _nsQuizOrder) ? q.whyNot[_nsQuizOrder[selectedIdx]] : null;
  if(whyNot) _logErrorJournal('ns', _nsPos, EX_NS[_nsPos].name, q.question, q.options[_nsQuizOrder[selectedIdx]], q.options[q.correct], whyNot);
  fb.textContent = ok ? '✅ Correcto.' :
    (whyNot ? '❌ '+whyNot+' Puedes intentarlo de nuevo, o revisar la solución.'
            : '❌ Incorrecto — puedes intentarlo de nuevo, o revisar la solución.');
  document.getElementById('nsQuizSolutionBtn').style.display='inline-block';
  if(ok) _quizRenderConfidencePrompt('ns');
  if(q.type==='mc' && _nsQuizOrder){
    const otherOptionTexts=q.options.filter((_,i)=>i!==_nsQuizOrder[selectedIdx]);
    _quizRenderReasonPrompt('ns', otherOptionTexts);
  }
  if(ok && _nsQuizSubPos<NS_QUIZ[_nsPos].length-1)
    document.getElementById('nsQuizNextBtn').style.display='inline-block';
}
function _nsNextQuizQuestion(){
  if(_nsQuizSubPos<NS_QUIZ[_nsPos].length-1){ _nsQuizSubPos++; _nsRenderQuiz(); }
}
function _nsShowQuizSolution(){
  const q=_nsCurrentQuiz;
  const el=document.getElementById('nsQuizSolutionBody');
  el.innerHTML=q.solution+_quizStepsHtml(q)+_quizWhyNotHtml(q, _nsQuizOrder)+_quizStakesHtml(q);
  el.style.display='block';
}
function _nsRenderBar(){
  const ex=EX_NS[_nsPos];
  const pct=Math.round((_nsDone.size/EX_NS.length)*100);
  document.getElementById('masterNsTitle').textContent=
    `🧩 Tema ${_nsPos+1}/${EX_NS.length} · ${ex.name}`;
  document.getElementById('masterNsFill').style.width=pct+'%';
  document.getElementById('masterNsPct').textContent=pct+'% del temario NS dominado';
  document.getElementById('mPrevNs').disabled=(_nsPos<=0);
  const atEnd=_nsPos>=EX_NS.length-1;
  document.getElementById('mNextNs').textContent=atEnd ? '✅ Entendido, terminar' : '✅ Entendido, siguiente ▶';
  if(document.getElementById('masterNsChecklist').style.display!=='none') _nsRenderChecklist();
}
function nsPrev(){ if(_nsPos>0) _nsGoTo(_nsPos-1); }
function nsRepeat(){ _nsGoTo(_nsPos); }
function _nsRestart(){ _nsGoTo(0); }
function nsNext(){
  _nsDone.add(_nsPos);
  _saveNsProgress();
  if(_nsPos>=EX_NS.length-1){
    _nsRenderBar();
    setSt('🎉 ¡Completaste el piloto del Modo Maestro No Supervisado!');
    return;
  }
  _nsGoTo(_nsPos+1);
}
function _nsToggleChecklist(){
  const cl=document.getElementById('masterNsChecklist');
  const show=cl.style.display==='none';
  cl.style.display=show?'block':'none';
  if(show) _nsRenderChecklist();
}
function _nsRenderChecklist(){
  const cl=document.getElementById('masterNsChecklist');
  cl.innerHTML=EX_NS.map((ex,i)=>{
    const done=_nsDone.has(i);
    const cur=i===_nsPos;
    return `<div class="master-item${done?' master-item-done':''}${cur?' master-item-current':''}" onclick="_nsGoTo(${i})">`+
      `<span class="master-item-chk">${done?'✓':(i+1)}</span><span class="master-item-name">${esc(ex.name)}</span>${_failsBadge('ns',i)}${_dontKnowBadge('ns',i)}</div>`;
  }).join('');
}

/* Glosario NS: pedido explícito del usuario ("que ningún término quede sin
   explicación") -- cubre TODO término técnico que aparece en las preguntas,
   teoría o soluciones de los 20 temas de NS (clustering intro, K-Means, PCA,
   DBSCAN, Mezclas Gaussianas), buscable en cualquier momento vía el botón
   "📚 Glosario". Ver _glossaryHtml en core.js. */
const GLOSSARY_NS=[
{term:'Aprendizaje no supervisado', def:'La rama del machine learning donde el algoritmo solo recibe datos (X), sin ninguna respuesta "correcta" (y) — tiene que descubrir estructura, grupos o patrones por su cuenta.'},
{term:'Aprendizaje supervisado', def:'La rama del machine learning donde el algoritmo aprende a partir de pares (X,y): hay una respuesta correcta conocida que el modelo intenta imitar. Se contrasta con no supervisado en el primer tema de este modo.'},
{term:'ARI (Adjusted Rand Index)', def:'Una métrica de 0 a 1 que compara las etiquetas que asignó un algoritmo de clustering contra las etiquetas verdaderas conocidas (solo posible con datos sintéticos, donde sí conocemos la respuesta) — 1.0 es agrupación perfecta.'},
{term:'Centroide', def:'El "centro" de un grupo en K-Means: el promedio (la posición media) de todos los puntos actualmente asignados a ese grupo. Se recalcula en cada iteración del algoritmo.'},
{term:'Clustering (agrupamiento)', def:'La tarea de dividir un conjunto de datos en grupos, de forma que los puntos de un mismo grupo se parezcan entre sí más que a los de otros grupos — sin que nadie le diga al algoritmo cuáles son esos grupos de antemano.'},
{term:'Clustering blando (soft)', def:'Un tipo de clustering (como GMM) que, para cada punto, da una PROBABILIDAD de pertenecer a cada grupo (ej. 57% grupo 1, 43% grupo 2) en vez de asignarlo a uno solo.'},
{term:'Clustering duro (hard)', def:'Un tipo de clustering (como K-Means o DBSCAN) que asigna cada punto a UN SOLO grupo, sin matices ni probabilidades.'},
{term:'Componente principal', def:'Cada uno de los nuevos ejes que crea PCA, ordenados de forma que el primero captura la mayor variación posible de los datos originales, el segundo la mayor variación restante, y así sucesivamente.'},
{term:'Covarianza', def:'Una medida de cómo varían juntas dos (o más) variables — en GMM, cada Gaussiana usa su propia covarianza para describir la forma y orientación de su grupo (no solo su centro).'},
{term:'DBSCAN', def:'Un algoritmo de clustering que agrupa puntos por DENSIDAD (cuántos vecinos cercanos tiene cada uno) en vez de por distancia a un centro — no necesita que le digas cuántos grupos hay, y puede detectar outliers como "ruido".'},
{term:'Densidad (de puntos)', def:'Qué tan cerca y agrupados están los puntos entre sí en una región del espacio — DBSCAN usa este concepto (vecinos dentro de un radio) para decidir qué es un grupo y qué es ruido.'},
{term:'Etiqueta (label) / y_true', def:'El "valor correcto" asociado a un dato. En aprendizaje no supervisado, si existe (como en datasets sintéticos con make_blobs), NUNCA se le pasa al algoritmo — solo sirve para que el humano evalúe el resultado después.'},
{term:'eps (epsilon)', def:'El parámetro de DBSCAN que define el radio de búsqueda: qué tan cerca tiene que estar otro punto para contar como "vecino" al decidir si una zona es suficientemente densa.'},
{term:'GMM (Mezclas Gaussianas / Gaussian Mixture Model)', def:'Un modelo de clustering que asume que los datos vienen de una mezcla de varias distribuciones Gaussianas (forma de campana) superpuestas — permite clustering blando, con una probabilidad por grupo para cada punto.'},
{term:'Inercia (WCSS)', def:'La suma de las distancias al cuadrado de cada punto a su centroide asignado — mide qué tan compactos son los grupos de K-Means. Siempre baja al aumentar k, por lo que sola no basta para elegir el mejor k.'},
{term:'K-Means', def:'El algoritmo de clustering más común: agrupa los puntos según su distancia al centroide más cercano, alternando entre asignar puntos y recalcular centroides hasta converger. Necesita que le digas k (la cantidad de grupos) de antemano.'},
{term:'k (número de clusters)', def:'El parámetro que le dice a K-Means cuántos grupos formar — a diferencia de DBSCAN, K-Means no lo descubre solo, hay que elegirlo de antemano (por ejemplo, comparando inercia o silhouette para varios valores).'},
{term:'min_samples', def:'El parámetro de DBSCAN que define cuántos vecinos mínimos (dentro del radio eps) necesita un punto para considerarse parte de una zona densa, en vez de ruido.'},
{term:'n_init', def:'Cuántas veces se repite K-Means con centroides iniciales distintos, quedándose con el resultado de menor inercia — reduce el riesgo de una mala agrupación por mala suerte en la inicialización (que es al azar).'},
{term:'PCA (Análisis de Componentes Principales)', def:'Una técnica que reduce la cantidad de columnas de un dataset, creando nuevos ejes (componentes) que conservan la mayor variación posible de los datos originales — útil para graficar o comprimir datos de muchas dimensiones.'},
{term:'predict()', def:'El método que da la asignación DURA de un punto a un grupo (un solo número, el más probable) — en GMM coexiste con predict_proba(), que da la información completa de probabilidades.'},
{term:'predict_proba()', def:'El método (disponible en GMM, no en K-Means) que da, para un punto, la probabilidad de pertenecer a CADA grupo posible — la versión "blanda" de predict().'},
{term:'Reducción de dimensionalidad', def:'El proceso de pasar de muchas columnas (dimensiones) a menos, conservando la mayor información posible — PCA es la técnica más común para esto.'},
{term:'Ruido / outlier (etiqueta -1)', def:'En DBSCAN, los puntos que no tienen suficientes vecinos cercanos como para pertenecer a ningún grupo denso — se marcan con la etiqueta especial -1, en vez de forzarlos dentro de algún grupo.'},
{term:'Silhouette score', def:'Una métrica que combina qué tan cerca está un punto de su propio grupo y qué tan lejos de los otros grupos, para evaluar la calidad de un clustering — a diferencia de la inercia, no baja automáticamente al aumentar k, por lo que sirve para elegir el mejor k.'},
{term:'Varianza explicada (explained_variance_ratio_)', def:'El porcentaje de la variación (información) total de los datos originales que conserva cada componente principal de PCA — sumado sobre todas las componentes que se conservan, dice cuánta información sobrevivió a la reducción.'},
{term:'weights_ (pesos de las Gaussianas)', def:'En GMM, la proporción esperada de cada grupo dentro del total (por ejemplo, [0.28, 0.32, 0.40]) — un parámetro GLOBAL del modelo, fijo una vez entrenado, distinto de la probabilidad de un punto particular.'},
];
function _nsToggleGlossary(){
  const gl=document.getElementById('masterNsGlossary');
  const show=gl.style.display==='none';
  gl.style.display=show?'block':'none';
  if(show) _nsRenderGlossary();
}
function _nsRenderGlossary(){
  const input=document.getElementById('nsGlossarySearch');
  document.getElementById('nsGlossaryList').innerHTML=_glossaryHtml(GLOSSARY_NS, input?input.value:'');
}

/* ──────────── NS_COMPARE: peldaño "Comparación" (Escalera de Dominio) ────────────
   Mismo patrón que AS_COMPARE en master-as.js (ver esa cabecera). `pair` son
   los dos índices BASE (múltiplos de 4) en EX_NS. Solo aparece en Repaso
   mezclado cuando AMBOS conceptos del par ya se completaron. */
const NS_COMPARE=[
{pair:[4,12],
 question:'K-Means y DBSCAN agrupan datos SIN etiquetas los dos. ¿Cuál es la diferencia real en '+
  'cómo decide cada uno qué es un grupo?',
 options:[
  'K-Means agrupa por DISTANCIA a un centroide (necesita que le digas k de antemano, y solo '+
   'puede formar regiones más o menos redondeadas); DBSCAN agrupa por DENSIDAD de vecinos '+
   '(descubre k solo, y puede seguir formas arbitrarias, marcando lo que no encaja como ruido).',
  'Son el mismo algoritmo con dos nombres distintos.',
  'DBSCAN necesita que se le diga k de antemano, y K-Means lo descubre solo.',
  'K-Means puede marcar puntos como "ruido"; DBSCAN obliga a asignar todos los puntos a algún grupo.'],
 correct:0,
 solution:'K-Means minimiza distancia a centroides (por eso solo dibuja regiones redondeadas y '+
  'necesita k fijo); DBSCAN conecta puntos densos entre sí (por eso puede seguir formas como las '+
  'dos lunas del ejemplo, y dejar afuera los outliers como ruido, sin que nadie le diga cuántos '+
  'grupos hay).'},
];
function _nsCompareUnlocked(i){
  const [a,b]=NS_COMPARE[i].pair;
  const done=x=>[x,x+1,x+2,x+3].some(j=>_nsDone.has(j));
  return done(a) && done(b);
}

/* ──────────── NS_LIMITS: peldaño "Limitación" (Escalera de Dominio) ────────────
   Mismo patrón que AS_LIMITS en master-as.js (nivel 6: "¿cuándo NO
   funciona?"). `concept` es el índice BASE (múltiplo de 4) en EX_NS. */
const NS_LIMITS=[
{concept:12,
 question:'DBSCAN agrupa por densidad, usando UN SOLO radio (eps) y UN SOLO mínimo de vecinos '+
  '(min_samples) para TODO el dataset. ¿Qué pasa si el dataset tiene un grupo muy denso y otro '+
  'grupo mucho más disperso al mismo tiempo?',
 options:[
  'DBSCAN los distingue perfectamente sin problema, sin importar cuánto varíe la densidad entre grupos.',
  'Con un eps chico (ajustado al grupo denso), el grupo disperso queda marcado como ruido casi '+
   'entero; con un eps grande (ajustado al grupo disperso), el grupo denso se fusiona con sus '+
   'vecinos en un solo cluster gigante — un único eps no le sirve bien a los dos grupos a la vez.',
  'DBSCAN ajusta automáticamente un eps distinto para cada grupo del dataset.',
  'El problema de densidades distintas solo afecta a K-Means, nunca a DBSCAN.'],
 correct:1,
 solution:'eps y min_samples son parámetros GLOBALES, iguales para todo el dataset — DBSCAN no '+
  'tiene forma de "adaptar" el radio según la zona. Con densidades muy distintas, cualquier eps '+
  'fijo va a quedar mal calibrado para al menos uno de los dos grupos: el disperso se pierde como '+
  'ruido, o el denso se mezcla con sus vecinos. Esta es la limitación clásica de DBSCAN frente a '+
  'datasets con densidades muy dispares.'},
];
function _nsLimitsUnlocked(i){
  const c=NS_LIMITS[i].concept;
  return [c,c+1,c+2,c+3].some(j=>_nsDone.has(j));
}

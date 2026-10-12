# Apuntes de SESIONES: Aprendizaje No Supervisado (06MIAR)

> **Fuente:** diapositivas T0, T1.1, T1.2, T2.1–T2.4, notebooks P1_1–P1_5 y scripts `.py` de la carpeta `SESIONES` (prof. José María Escalante, curso 2026-27).
> **Formato:** cada concepto sigue el orden *problema real → analogía cotidiana → concepto → matemática → código → análisis → pregunta de verificación → nota para guardar*. Las respuestas a las preguntas están plegadas: **intenta responder antes de abrirlas**.

## Orden de estudio (de más fácil a más difícil de explicar)

Cada bloque solo usa lo que ya explicaron los anteriores.

| # | Bloque | Por qué va en este lugar | Sesión del curso |
|---|---|---|---|
| 0 | Mapa de la asignatura y evaluación | Contexto, sin conceptos técnicos | T0 |
| 1 | ¿Qué es aprender? Enfoques del aprendizaje automático | Base de todo | T1.1 |
| 2 | Datos sin etiqueta: la matriz instancias × características | Lo que manipulan todos los algoritmos | T1.1 / T1.2 |
| 3 | Distancia, similitud y disimilitud | El "motor" de todos los algoritmos de clustering | T1.2 |
| 4 | Parámetro frente a hiperparámetro | Necesario para entender K, ε, h… | T1.2 |
| 5 | Evaluación sin etiquetas (interna y externa) | Para juzgar cualquier algoritmo | T1.2 + notebooks |
| 6 | Clustering por particiones: K-means | El algoritmo más intuitivo | T2.1 |
| 7 | ¿Cuántos clusters? Codo y silueta | Sale directamente del problema de K-means | T2.1 |
| 8 | Mejoras de K-means: K-means++ y K-medoids | Corrigen las debilidades del bloque 6 | T2.1 |
| 9 | Clustering jerárquico (aglomerativo y divisivo, dendrograma) | Elimina la necesidad de fijar K | T2.2 |
| 10 | Clustering basado en densidad (DBSCAN, Mean Shift, Affinity Propagation) | Formas arbitrarias y ruido; la intuición es simple | T2.4 |
| 11 | Clustering espectral | Requiere grafos y autovalores: el más abstracto | T2.3 |
| 12 | Clustering probabilístico (GMM y EM) | Generaliza K-means con probabilidades | P1_5 |
| 13 | Tabla comparativa final y conexión con los 6 artículos | Síntesis | — |

> Nota: en el curso, el espectral (T2.3) va antes que densidad (T2.4). Aquí lo puse después porque la idea de densidad se explica con menos herramientas previas.

---

## Bloque 0: Mapa de la asignatura

**Objetivos del curso:** conocer los fundamentos, comprender las técnicas no supervisadas, evaluarlas, seleccionarlas y ajustarlas, y aplicarlas en la práctica.

| Tema | Contenido |
|---|---|
| T1 | Introducción, medidas de distancia, evaluación |
| T2 | Clustering: particiones, jerárquico, espectral, densidad, probabilístico |
| T3 | Semi-supervisado: GMM y EM |
| T4 | Análisis de componentes: reducción de dimensionalidad, PCA, ICA |
| T5 | Grafos (PageRank) y transacciones (recomendación) |
| T6 | Deep clustering: autoencoders, modelos generativos, optimización directa del cluster |
| T7 | Aplicaciones: anomalías, segmentación de clientes, extracción de características |

**Evaluación:**
- **Examen (40 %):** test más preguntas de desarrollo (pseudocódigo y respuesta abierta). Dura 70 minutos, dentro de una franja de 2 horas.
- **Portafolio (60 %):** foro, artículo científico, test de vídeo teórico y test de programación.
- Hay que **aprobar ambas partes** (nota ≥ 5). No se aceptan entregas fuera de plazo ni por correo.

> **Para el examen:** como hay preguntas de **pseudocódigo**, cada algoritmo de estos apuntes trae sus pasos numerados. Apréndelos para poder reproducirlos.

---

## Bloque 1: ¿Qué es aprender? Enfoques del aprendizaje automático

**Problema real.** Antes, para que una máquina hiciera una tarea, alguien tenía que escribir **todas las reglas a mano** (sistema experto). Si una regla estaba mal, el sistema fallaba.

**Analogía.** Es como aprender a cocinar. Puedes seguir una receta exacta (reglas) o probar, equivocarte y ajustar el sabor (experiencia).

**Concepto.**
- **Aprendizaje:** proceso por el que un sistema adquiere o mejora conocimientos o comportamientos a partir de la experiencia, los datos o la interacción con el entorno.
- **Aprendizaje automático:** ajustar un **modelo matemático** a partir de la experiencia para comportarse mejor ante situaciones nuevas.

| Enfoque | ¿Qué recibe? | Lema del curso | Ejemplo |
|---|---|---|---|
| **Supervisado** | Entradas **con** salida conocida (etiqueta) | *Task driven* 100 % | Clasificar cáncer de piel, predecir el precio de una casa |
| **No supervisado** | **Solo entradas** | *Data driven* 100 % | Clustering, reducción de dimensionalidad, extracción de características |
| **Semi-supervisado** | Pocas etiquetadas y muchas sin etiqueta | Mezcla, con predominio de datos | Clasificar cuando etiquetar es caro |
| **Por refuerzo** | Recompensas y castigos al interactuar | Guiado por el entorno | Robótica, videojuegos |
| **Auto-supervisado** | Datos sin etiqueta de los que **genera su propia etiqueta** | Autoguiado | Grandes modelos generativos (y los artículos 2, 4 y 6 del portafolio) |

**Aprendizaje no supervisado (definición del curso):** conjunto de técnicas para extraer **conocimiento, estructura y representaciones útiles** a partir de datos **no etiquetados**.
> *"No busca predecir una respuesta conocida, sino comprender cómo están organizados los datos."*

**¿Por qué importa?** Etiquetar es caro, lento y requiere expertos, mientras que los datos sin etiqueta abundan. **Aplicaciones:** segmentación de usuarios, detección de anomalías (fraude, hackeo, mutaciones), temas en textos, extracción de características, reducción de dimensionalidad, relaciones entre productos y recomendación.

<details><summary><b>Verificación:</b> ¿Por qué el aprendizaje no supervisado se describe como "data driven 100 %" y el supervisado como "task driven"?</summary>

Porque en el supervisado la **etiqueta** (la tarea) dice qué debe aprender el modelo y le da *feedback*. En el no supervisado no hay etiqueta: lo único que guía el aprendizaje es la **estructura de los propios datos**.
</details>

> **Nota:** no supervisado = descubrir estructura en datos sin etiqueta; nadie le dice al modelo la respuesta.

---

## Bloque 2: Datos sin etiqueta, la matriz instancias × características

**Concepto.** Los datos son una tabla de **M instancias** (filas) × **N características** (columnas). El identificador I₁, I₂… **no es una etiqueta**: solo nombra la fila. Cada fila es un **vector** que representa a la instancia.

| Símbolo | Qué significa | Ejemplo |
|---|---|---|
| M | Número de instancias o muestras | 1797 imágenes de dígitos |
| N | Número de características | 64 píxeles (imagen de 8×8) |
| Iᵢ | Identificador de la instancia *i* (no es clase) | I₃ = tercera imagen |
| Xᵢⱼ | Valor de la característica *j* en la instancia *i* | Intensidad del píxel 5 de la imagen 3 |

**¿Cómo aprende sin feedback?** Buscando **similitudes o disimilitudes** entre esos vectores para formar grupos, por ejemplo {I₁, I₅₆, I₈₅₃} y {I₄, I₅₂, I₃₂₆}.

> **Nota:** cada fila es un vector; todo el no supervisado consiste en comparar vectores entre sí.

---

## Bloque 3: Distancia, similitud y disimilitud

**Problema real.** Para agrupar necesito decir cuándo dos clientes "se parecen". Pero "parecerse" hay que **medirlo con un número**.

**Analogía.** Dos casas en el mapa: puedo medir la distancia en línea recta (a vuelo de pájaro) o recorriendo cuadras (como un taxi). Son dos formas distintas de medir "qué tan lejos".

**Concepto.**
- **Similitud S(Iᵢ, Iⱼ):** cuánto se parecen dos muestras.
- **Disimilitud D(Iᵢ, Iⱼ):** cuánto se diferencian. Si están normalizadas, **S = 1 − D**: mucha similitud implica poca disimilitud.
- Ambas se calculan con una **distancia d(Iᵢ, Iⱼ)**. Para que una función sea distancia (métrica) debe cumplir cuatro condiciones:

| Condición | Fórmula | Qué significa |
|---|---|---|
| No negatividad | d(a, b) ≥ 0 | No existen distancias negativas |
| Simetría | d(a, b) = d(b, a) | Ir de a a b mide lo mismo que de b a a |
| Indiscernibles | d(a, b) = 0 ⇔ a = b | Solo un punto consigo mismo está a distancia 0 |
| Desigualdad triangular | d(a, c) ≤ d(a, b) + d(b, c) | Dar un rodeo nunca es más corto que ir directo |

**Tipos de distancia (tabla combinada):**

| Distancia | Fórmula | Cuándo usarla | Ejemplo con a = (0, 0), b = (3, 4) |
|---|---|---|---|
| **Euclídea** | √Σ(aⱼ − bⱼ)² | Datos numéricos, "línea recta" | √(9 + 16) = **5** |
| **Manhattan** (*cityblock*) | Σ\|aⱼ − bⱼ\| | Movimiento en cuadrícula, menos sensible a valores extremos | 3 + 4 = **7** |
| **Chebyshev** | maxⱼ \|aⱼ − bⱼ\| | Cuando importa la peor diferencia | max(3, 4) = **4** |
| **Minkowski** | (Σ\|aⱼ − bⱼ\|ᵖ)^(1/p) | Generaliza: p = 1 es Manhattan, p = 2 Euclídea, p → ∞ Chebyshev | — |
| **Hamming** | Nº de posiciones distintas | Vectores **binarios** o categóricos | 1011 frente a 1001 → **1** |
| **Jaccard** | 1 − \|A∩B\| / \|A∪B\| | Conjuntos (por ejemplo, productos comprados) | {pan, leche} frente a {pan, café}: 1 − 1/3 = **0.67** |
| **Coseno** | 1 − (a·b)/(‖a‖‖b‖) | Importa la **dirección**, no el tamaño (textos) | — |
| **Correlación** | 1 − corr(a, b) | Importa la forma del patrón | — |
| **Mahalanobis** (notebook P1_4) | √((a−b)ᵀ Σ⁻¹ (a−b)) | Datos con **covarianza** (nubes estiradas); generaliza la Euclídea | — |

**Idea clave del curso:** a veces la similitud es **cercanía geométrica** (K-means, jerárquico) y otras veces es **conectividad** (espectral) o **distribución** (densidad, GMM).

**Código (vectorizado):**
```python
import numpy as np
from scipy.spatial.distance import pdist, squareform

X = np.array([[1, 2], [3, 4], [6, 8]])   # sin vector (0,0): el coseno no está definido para él
D_euc = squareform(pdist(X, metric="euclidean"))   # matriz M×M
D_man = squareform(pdist(X, metric="cityblock"))
D_cos = squareform(pdist(X, metric="cosine"))
print(D_euc); print(D_man); print(D_cos)
```
- `pdist` calcula **todas las distancias entre pares** sin bucles (vectorizado) y devuelve un vector compacto.
- `squareform` lo convierte en una matriz simétrica M×M con ceros en la diagonal.
- Con coseno, (3, 4) y (6, 8) quedan a distancia **0**: apuntan en la misma dirección aunque uno sea el doble del otro.

**Análisis.** La elección de distancia **cambia los clusters**. Además, si una variable está en miles y otra en unidades, la grande domina, así que **escala los datos** (`StandardScaler`) antes de usar distancias. El notebook P1_4 insiste en que este paso es "MUY importante".

<details><summary><b>Verificación:</b> ¿Por qué con la distancia coseno los puntos (3, 4) y (6, 8) están a distancia 0, pero con la Euclídea no?</summary>

Porque el coseno solo mide el **ángulo** (la dirección) entre vectores, y ambos apuntan en la misma dirección. La Euclídea mide la **longitud del segmento** que los separa, que es 5.
</details>

> **Nota:** distancia = número que mide qué tan distintos son dos vectores; la elegida define qué significa "parecido".

---

## Bloque 4: Parámetro frente a hiperparámetro

| | Parámetro | Hiperparámetro |
|---|---|---|
| **Quién lo fija** | El algoritmo lo **aprende** de los datos | **Tú**, antes de entrenar |
| **Ejemplos** | Posición de los centroides, pesos de una red | Número de clusters K, métrica de distancia, ε y MinPts, ancho de banda h, nº de componentes |
| **Analogía** | La sazón final de la sopa | El tamaño de la olla que elegiste antes de cocinar |

<details><summary><b>Verificación:</b> En K-means, ¿K es parámetro o hiperparámetro? ¿Y la posición final de los centroides?</summary>

K es **hiperparámetro**: lo eliges antes. Los centroides son **parámetros**: el algoritmo los calcula a partir de los datos.
</details>

> **Nota:** hiperparámetro = lo decido yo antes; parámetro = lo aprende el modelo.

---

## Bloque 5: Evaluación sin etiquetas

**Problema real.** En supervisado comparo la predicción con la respuesta correcta. Aquí **no hay respuesta correcta**. Entonces, ¿cómo sé si el agrupamiento es bueno?

**Analogía.** Ordenas tu ropa en cajones sin que nadie te diga cómo. Para juzgarlo te preguntas si dentro de cada cajón las prendas se parecen (**cohesión**) y si los cajones son distintos entre sí (**separación**).

**Concepto: dos tipos de evaluación.**
1. **Interna** (sin etiquetas): mide cohesión y separación con los propios datos.
2. **Externa** (con alguna referencia): comprobar que la estructura encontrada tiene **sentido** (que la segmentación sea útil, que la reducción de dimensión valga la pena). Si existen etiquetas reales (como en los notebooks), se comparan.

**Métricas internas de clustering:**

| Métrica | Idea | Fórmula | ¿Mejor alto o bajo? |
|---|---|---|---|
| **Inercia / WCSS** | Suma de distancias al cuadrado de cada punto a su centroide | Σₖ Σ_{i∈Cₖ} ‖xᵢ − μₖ‖² | Bajo (pero siempre baja al subir K) |
| **Silueta** | Cohesión frente a separación por punto | s(i) = (b(i) − a(i)) / max{a(i), b(i)} | **Alto** (rango de −1 a 1) |
| **Davies-Bouldin** | Similitud media de cada cluster con el más parecido (dispersión interna / separación) | promedio de maxⱼ (σᵢ + σⱼ) / d(cᵢ, cⱼ) | **Bajo** |
| **Calinski-Harabasz** | Dispersión entre clusters / dispersión interna | [tr(B)/(K−1)] / [tr(W)/(M−K)] | **Alto** |
| **Dunn** | Distancia mínima entre clusters / diámetro del cluster más grande | min d(Cᵢ, Cⱼ) / max diam(Cₖ) | **Alto** |
| **Correlación cofenética** (jerárquico) | Cuánto respeta el dendrograma las distancias originales | corr(distancias reales, alturas de fusión) | Cercano a 1 |

**Silueta: tabla de variables.**

| Variable | Qué significa | De dónde sale | Ejemplo concreto | Qué ocurre al calcular |
|---|---|---|---|---|
| a(i) | Distancia media de *i* a los **de su mismo** cluster | Promedio de d(i, j) con j en el cluster de *i* | a = 1 | Cuanto menor, más cohesionado está *i* |
| b(i) | **Menor** distancia media de *i* a los puntos de **otro** cluster | Se calcula para cada otro cluster y se toma el mínimo | b = 4 | Cuanto mayor, más separado está del vecino |
| s(i) | Silueta del punto | (b − a) / max(a, b) | (4 − 1)/4 = **0.75** | Cerca de 1: bien asignado; ≈ 0: en la frontera; < 0: probablemente mal asignado |
| S | Silueta total | (1/N) Σ s(i) | Promedio de todos los puntos | Se elige el K que la **maximiza** |

**Métricas externas (cuando hay etiquetas reales, notebooks P1_1 y P1_4):**
- **Homogeneidad:** cada cluster contiene una sola clase.
- **Completitud** (*completeness*): todos los de una clase caen en el mismo cluster.
- **Información mutua ajustada (AMI)** y **Adjusted Rand Index (ARI):** acuerdo global corregido por azar (1 = perfecto, ≈ 0 = azar).
- **Accuracy por moda:** a cada cluster se le asigna la etiqueta más frecuente y se calcula la exactitud (K-means sobre dígitos ≈ 80 %; con **t-SNE** antes, cerca de un 13 % más).

**Métricas de otros temas (adelanto de la sesión T1.2):**
- **Probabilísticos:** log-verosimilitud, **AIC** y **BIC** (ajuste penalizado por complejidad; BIC penaliza más).
- **Semi-supervisado:** matriz de confusión.
- **Reducción de dimensionalidad:** varianza explicada, error de reconstrucción.
- **Grafos y transacciones:** modularidad, conductancia, *support*, *confidence*, *lift*.
- **Deep clustering:** pérdida de reconstrucción, pérdida contrastiva, **FID** (modelos generativos); la silueta también sirve.

**Código:**
```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import (silhouette_score, davies_bouldin_score,
                             calinski_harabasz_score, adjusted_rand_score)

X, y = make_blobs(n_samples=500, centers=4, random_state=0)
labels = KMeans(n_clusters=4, n_init=10, random_state=0).fit_predict(X)
print("Silueta  :", silhouette_score(X, labels))        # alto = mejor
print("Davies-B :", davies_bouldin_score(X, labels))    # bajo = mejor
print("Calinski :", calinski_harabasz_score(X, labels)) # alto = mejor
print("ARI      :", adjusted_rand_score(y, labels))     # externa: usa y
```
- Las tres primeras son **internas**: solo usan `X` y `labels`.
- `adjusted_rand_score` es **externa**: necesita las etiquetas reales `y`, que en un problema real normalmente no tendrías.

<details><summary><b>Verificación:</b> ¿Por qué no sirve elegir K buscando la inercia mínima?</summary>

Porque la inercia **siempre disminuye** al aumentar K. Con K = número de puntos, cada punto es su propio centroide y la inercia vale 0. Por eso se busca el **codo** o se usa una métrica que penalice, como la silueta.
</details>

> **Nota:** sin etiquetas evalúo cohesión (dentro) y separación (entre); la silueta combina ambas en un número entre −1 y 1.

---

## Bloque 6: Clustering por particiones, K-means

**Problema real.** Una tienda quiere dividir a sus clientes en **K grupos** para hacerles campañas distintas.

**Analogía.** Tienes que poner K puestos de comida en una feria. Cada persona va al puesto **más cercano**. Luego mueves cada puesto al **centro** de la gente que atiende, y repites hasta que nadie cambia de puesto.

**Concepto.** Una partición divide los datos en grupos que **cubren todo** (I = C₁ ∪ … ∪ Cₖ) y **no se solapan** (Cᵢ ∩ Cⱼ = ∅). El objetivo es:
- minimizar la **dispersión intra-cluster** I(C) = ½ Σₖ Σ_{i∈k} Σ_{i'∈k} d(xᵢ, xᵢ');
- maximizar la **dispersión inter-cluster** O(C) = ½ Σₖ Σ_{i∈k} Σ_{i'∉k} d(xᵢ, xᵢ').

El **centroide** es la **media** de los puntos del cluster.

**Algoritmo (pseudocódigo para el examen):**
```
Entrada: datos X, número de clusters K
1. Inicialización: elegir K puntos al azar como centroides μ1..μK
2. Asignación: cada punto va al centroide más cercano
3. Actualización: cada μk = media de los puntos asignados a k
4. Reasignación: recalcular la distancia de cada punto a los nuevos centroides
5. Convergencia: repetir 3-4 hasta que los centroides no cambien
Salida: etiquetas y centroides
```
Es equivalente a minimizar la inercia: Σₖ Σ_{i∈Cₖ} ‖xᵢ − μₖ‖².

**Código (implementación vectorizada desde cero más sklearn):**
```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

def kmeans(X, K, n_iter=100, seed=0):
    rng = np.random.default_rng(seed)
    mu = X[rng.choice(len(X), K, replace=False)]          # 1. init
    for _ in range(n_iter):
        d = ((X[:, None, :] - mu[None, :, :])**2).sum(-1) # distancias M×K
        labels = d.argmin(1)                               # 2/4. asignación
        new_mu = np.array([X[labels == k].mean(0) for k in range(K)])  # 3.
        if np.allclose(new_mu, mu):                        # 5. convergencia
            break
        mu = new_mu
    return labels, mu

X, _ = make_blobs(n_samples=600, centers=3, random_state=1)
labels, mu = kmeans(X, 3)
sk = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
print(mu, "\n", sk.cluster_centers_, sk.inertia_)
```
- `X[:, None, :] - mu[None, :, :]` usa *broadcasting* para calcular **todas** las distancias punto-centroide de una vez (matriz M×K), sin bucles.
- `argmin(1)` asigna cada punto a su centroide más cercano.
- La actualización recalcula cada centroide como la media de su grupo.
- `np.allclose` detiene el proceso cuando los centroides ya no se mueven.
- **Al ejecutarlo:** la versión casera (una sola inicialización aleatoria) puede caer en un **mínimo local**, con dos centroides dentro del mismo grupo. Al probarlo con `seed=0` ocurrió y la inercia fue mayor que la de sklearn. Es justo la debilidad que corrige el bloque 8.
- En sklearn, `n_init=10` repite el algoritmo con 10 inicializaciones y se queda con la de menor inercia.

**Aplicaciones de los notebooks (P1_1):**
- **Dígitos:** 10 centroides que parecen "el dígito típico"; confunde el 1 y el 8; accuracy ≈ 80 %.
- **Compresión de imagen:** cada píxel es un punto en el espacio RGB. Con `MiniBatchKMeans` se pasa de unos dieciséis millones de colores posibles a 16, y cada píxel se sustituye por su centroide. **MiniBatch** = K-means con lotes pequeños, útil para datasets grandes.

**Análisis: ventajas y desventajas (diapositiva T2.1).**

| Ventajas | Desventajas |
|---|---|
| Simple, rápido y escalable | Hay que **fijar K** |
| Fácil de interpretar | **Sensible a la inicialización** y puede caer en **mínimos locales** |
| Bajo coste computacional | **Sensible a outliers** (la media se desplaza) |
| Muy bueno con clusters compactos y esféricos | **Falla con formas no convexas** y con tamaños o densidades distintos |
| Evaluable con WCSS, silueta o Davies-Bouldin | Requiere **escalar** las variables |

<details><summary><b>Verificación:</b> ¿Por qué K-means falla con dos "lunas" entrelazadas aunque le des K = 2?</summary>

Porque asigna cada punto al centroide más cercano, y eso parte el espacio en regiones **convexas** separadas por rectas (celdas de Voronoi). Un cluster con forma de luna no cabe en una región convexa, así que K-means corta cada luna por la mitad.
</details>

> **Nota:** K-means = asignar al centroide más cercano y mover el centroide a la media, hasta que no cambie nada.

---

## Bloque 7: ¿Cuántos clusters? Método del codo y silueta

*(Relación con lo anterior: **no es un algoritmo nuevo**; es la respuesta al problema "hay que fijar K" del bloque 6.)*

**Método del codo.**
1. Ejecutar K-means para K = 1, 2, …, Kmax y guardar la **inercia** de cada uno.
2. Graficar la inercia frente a K: baja rápido y luego se aplana.
3. El **codo** (donde deja de bajar mucho) es el K elegido.

**Versión objetiva (script `Elbow_method_comparative_v1.py`):** normalizar ambos ejes a [0, 1], trazar la recta entre el primer y el último punto, y elegir el K **más alejado de esa recta**.

**Método de la silueta.** Calcular S para cada K ≥ 2 y elegir el K con **S máxima**. En el ejemplo de clase, K = 5 con S ≈ 0.72.

```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=600, centers=5, random_state=3)
Ks = np.arange(1, 11)
inertia = [KMeans(k, n_init=10, random_state=0).fit(X).inertia_ for k in Ks]

# codo objetivo: punto más lejano a la recta entre extremos (ejes normalizados)
x = (Ks - Ks.min()) / (Ks.max() - Ks.min())
y = (np.array(inertia) - min(inertia)) / (max(inertia) - min(inertia))
dist = np.abs((y[-1]-y[0])*x - (x[-1]-x[0])*y + x[-1]*y[0] - y[-1]*x[0])
k_codo = Ks[np.argmax(dist)]

sil = {k: silhouette_score(X, KMeans(k, n_init=10, random_state=0).fit_predict(X))
       for k in range(2, 11)}
print("K codo:", k_codo, "| K silueta:", max(sil, key=sil.get))
```
- La lista `inertia` guarda la inercia para cada K.
- `dist` es la distancia de cada punto (K, inercia), en ejes normalizados, a la recta que une los extremos; su máximo es el codo.
- `sil` empieza en K = 2 porque la silueta necesita al menos dos clusters.
- **Resultado real al ejecutarlo:** el codo objetivo marca **K = 2** y la silueta **K = 5** (el valor correcto). Con 5 grupos, varios quedan cerca entre sí, la curva de inercia cae casi toda al principio y el codo "geométrico" se adelanta. Es la ambigüedad del codo de la que habla el análisis.

**Análisis.** El codo puede ser ambiguo (curva suave). La silueta favorece clusters convexos y bien separados, así que **también falla con formas complejas**. Los dos métodos pueden no coincidir.

<details><summary><b>Verificación:</b> ¿Por qué la silueta no se puede calcular con K = 1?</summary>

Porque b(i) es la distancia media al **otro** cluster más cercano, y con un solo cluster no existe ningún otro.
</details>

> **Nota:** codo = donde la inercia deja de bajar mucho; silueta = el K con mayor S.

---

## Bloque 8: Mejoras de K-means, K-means++ y K-medoids

*(Relación: ambos son **K-means con un cambio**; los pasos 2 a 5 son iguales.)*

| | Problema que resuelve | Cambio |
|---|---|---|
| **K-means++** | Mala inicialización, que lleva a **mínimos locales** | Solo cambia el **paso 1**: centroides iniciales separados |
| **K-medoids** (PAM) | **Outliers** que arrastran la media | El centro es un **dato real** (medoide), no la media |

**K-means++ (inicialización).**
1. Elegir el primer centroide al azar.
2. Para cada punto x, calcular D(x) = distancia a su centroide **más cercano** ya elegido.
3. Elegir el siguiente centroide con probabilidad **P(x) = D(x)² / Σ D(x)²**: los puntos lejanos tienen más opciones.
4. Repetir hasta tener K centroides y seguir con el K-means normal.

**K-medoids.** El medoide es el punto del cluster que **minimiza la suma de distancias** al resto: m = argmin_{x∈C} Σ_{y∈C} d(x, y). Como es un dato real y usa distancias (no medias), funciona con **cualquier distancia** y resiste mejor a los outliers. Es más costoso porque necesita la matriz de distancias.

```python
import numpy as np
from sklearn.metrics import pairwise_distances

def kmeans_pp_init(X, K, seed=0):
    rng = np.random.default_rng(seed)
    C = [X[rng.integers(len(X))]]
    for _ in range(K - 1):
        D2 = pairwise_distances(X, np.array(C)).min(1) ** 2   # D(x)^2
        C.append(X[rng.choice(len(X), p=D2 / D2.sum())])
    return np.array(C)

def medoid(points):
    D = pairwise_distances(points)          # distancias internas del cluster
    return points[D.sum(1).argmin()]        # el que suma menos distancia
```
- `kmeans_pp_init` calcula para cada punto la distancia a su centroide más cercano, la eleva al cuadrado y la usa como probabilidad de muestreo.
- `medoid` elige, dentro del cluster, el punto cuya suma de distancias a los demás es mínima.
- En sklearn, `KMeans(init="k-means++")` ya es el valor por defecto.

<details><summary><b>Verificación:</b> ¿Por qué un outlier mueve mucho un centroide de K-means pero casi nada un medoide?</summary>

La media incluye al outlier en su cálculo y se desplaza hacia él. El medoide **tiene que ser un punto real** con suma de distancias mínima, y el outlier, al estar lejos de todos, nunca será el medoide ni lo arrastra.
</details>

> **Nota:** K-means++ = mejor arranque (centroides lejanos); K-medoids = centro real, robusto a outliers.

---

## Bloque 9: Clustering jerárquico

**Problema real.** No sé cuántos grupos hay, y quiero ver la estructura a **varios niveles** (familia → género → especie).

**Analogía.** Un árbol genealógico: los hermanos se unen primero, luego los primos, luego toda la familia. Puedo "cortar" el árbol al nivel que me interese.

**Concepto.** Se construye una jerarquía de grupos **anidados** y **no hace falta fijar K de antemano**. Hay dos direcciones:

| | Aglomerativo (*bottom-up*) | Divisivo (*top-down*) |
|---|---|---|
| Empieza con | N clusters (cada punto solo) | 1 cluster con todo |
| Termina con | 1 cluster | N clusters (o un criterio de parada) |
| Algoritmo de clase | **AGNES** | **DIANA** |
| Hiperparámetros | **Distancia + método de enlace (*linkage*)** | **Distancia + método de separación** |
| En sklearn | `AgglomerativeClustering` | `BisectingKMeans` (requiere K) |

Las uniones o divisiones pueden darse entre **dos puntos**, **dos clusters** o **un punto y un cluster**.

### 9.1 Aglomerativo: AGNES
```
1. Cada punto es un cluster
2. Calcular la matriz de distancias entre clusters
3. Buscar los dos clusters más próximos
4. Fusionarlos
5. Recalcular las distancias del nuevo cluster con los demás
6. Repetir hasta tener un único cluster
```
**Es *greedy*:** una fusión **nunca se deshace**, así que un error al principio condiciona toda la jerarquía.

**Métodos de enlace (cómo se mide la distancia entre dos clusters):**

| Enlace | Distancia entre C1 y C2 | Efecto típico |
|---|---|---|
| **Single** | **Mínima** entre sus puntos | Encadena puntos y sigue formas alargadas; sensible al ruido ("efecto cadena") |
| **Complete** | **Máxima** entre sus puntos | Clusters compactos de tamaño parecido |
| **Average** | **Media** de todos los pares | Término medio |
| **Centroide** | Distancia entre centroides | Simple; puede producir inversiones en el dendrograma |
| **Ward** (por defecto en sklearn) | Aumento de la inercia al fusionar | Clusters compactos, parecido a K-means |

### 9.2 Divisivo: DIANA
```
1. Empezar con un cluster con todos los puntos
2. Elegir el cluster a dividir (el más grande, o el que optimice un criterio, por ejemplo el de mayor diámetro)
3. Dividirlo en 2 (partición binaria)
4. Repetir hasta cumplir el criterio de parada
```
**Métodos de separación:** K-means con K = 2 (*bisecting*), o la **técnica de Macnaughton-Smith** (script `Jerarquico_v3.py`):
1. El punto con **mayor disimilitud media** al resto forma el grupo escindido (*splinter group*).
2. Para cada punto restante: δ(i) = (disimilitud media al grupo restante) − (disimilitud media al grupo escindido).
3. Si δ(i) > 0, el punto con mayor δ se pasa al grupo escindido.
4. Repetir hasta que ningún δ sea positivo.

### 9.3 Dendrograma
- **Eje Y:** distancia (disimilitud) a la que ocurre cada unión o división; su significado exacto depende del enlace. **El eje X no significa nada** (solo ordena las hojas).
- **Cortar** con una línea horizontal: el número de ramas que corta es **K**.
- **Elegir K:**
  - **Visual (subjetivo):** cortar justo debajo de un **gran salto** en la altura de fusión (ejemplo de clase: las fusiones van hasta h ≈ 9 y la siguiente salta a unos 13).
  - **Objetivo:** silueta (máxima), Calinski-Harabasz (máximo), Davies-Bouldin (mínimo).
- **Correlación cofenética** (notebook P1_2): mide si el árbol conserva las distancias originales; cuanto más cerca de 1, mejor.

```python
import numpy as np, matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster, cophenet
from scipy.spatial.distance import pdist
from sklearn.cluster import AgglomerativeClustering

rng = np.random.default_rng(4711)
X = np.vstack([rng.multivariate_normal([10, 0], [[3, 1], [1, 4]], 100),
               rng.multivariate_normal([0, 20], [[3, 1], [1, 4]], 50)])

Z = linkage(X, method="ward", metric="euclidean")   # historial de fusiones
c, _ = cophenet(Z, pdist(X))
print("Correlación cofenética:", round(c, 3))

dendrogram(Z, truncate_mode="lastp", p=12); plt.axhline(50, c="k"); plt.show()
labels_corte = fcluster(Z, t=50, criterion="distance")   # cortar a altura 50
labels_sk = AgglomerativeClustering(n_clusters=2, linkage="ward").fit_predict(X)
```
- `linkage` devuelve Z, de (N−1) filas con `[idx1, idx2, distancia, nº de muestras]`, una por fusión. Los índices ≥ N son clusters creados en fusiones anteriores: el índice N + i es el cluster que se formó en la fila Z[i].
- `cophenet` compara las alturas del árbol con las distancias reales.
- `dendrogram(..., truncate_mode="lastp", p=12)` muestra solo las últimas 12 fusiones; `axhline` dibuja la línea de corte.
- `fcluster` corta a una altura dada; `AgglomerativeClustering` hace lo mismo indicando K y permite reutilizar el modelo.

**Análisis.** Ventajas: no exige K y es interpretable. Desventajas: es costoso (O(N²) en memoria por la matriz de distancias, O(N³) en la versión ingenua), no corrige decisiones (*greedy*) y depende mucho del enlace.

<details><summary><b>Verificación:</b> ¿Por qué el enlace <i>single</i> puede unir dos grupos claramente distintos si hay unos pocos puntos de ruido entre ellos?</summary>

Porque mide la distancia entre clusters como la **mínima** entre cualquier par de puntos. Basta una "cadena" de puntos de ruido cercanos entre sí para que los dos grupos parezcan próximos y se fusionen (efecto cadena).
</details>

> **Nota:** jerárquico = árbol de fusiones (o divisiones); el corte del dendrograma da K, y el enlace define qué significa "clusters cercanos".

---

## Bloque 10: Clustering basado en densidad

**Problema real.** Quiero detectar zonas de mucha actividad en un mapa (por ejemplo, puntos de calor de delitos). Tienen **formas irregulares**, hay **puntos sueltos** que no pertenecen a ninguna zona, y no sé cuántas zonas hay.

**Analogía.** Desde un avión de noche ves ciudades: son zonas con **muchas luces juntas**, separadas por campo oscuro. Una casa aislada no es una ciudad: es ruido.

**Concepto.** Un cluster es una **región de alta densidad** separada por regiones de baja densidad. Herramientas:
- **Vecindad:** región alrededor de un punto (un radio).
- **Densidad:** número de puntos dentro de esa vecindad.

**Ventajas clave:** formas arbitrarias (no necesita esfericidad), identifica **ruido y outliers**, y **no necesita K**, por lo que tampoco necesita el codo, la silueta ni el dendrograma para elegirlo.

| Algoritmo | Pregunta que se hace |
|---|---|
| **DBSCAN** | ¿Cuántos vecinos tiene este punto? |
| **Mean Shift** | ¿En qué dirección **aumenta** la densidad? |
| **Affinity Propagation** | ¿Qué dato es el **representante** real de un cluster? |

### 10.1 DBSCAN

| Variable | Qué significa | De dónde sale | Ejemplo concreto | Qué ocurre al cambiarla |
|---|---|---|---|---|
| **ε** (*eps*) | Radio de la vecindad | Hiperparámetro; distancia, normalmente euclídea | ε = 0.3 con datos escalados | Si es pequeño, fragmenta clusters y aumenta el ruido; si es grande, **fusiona** clusters |
| **MinPts** (`min_samples`) | Mínimo de puntos en la vecindad para que sea "densa" | Hiperparámetro (regla habitual: ≥ dimensión + 1) | MinPts = 5 | Si sube, se exige más densidad y hay más ruido |
| **Punto núcleo** (*core*) | Tiene ≥ MinPts vecinos dentro de ε | Del conteo | Centro de una zona densa | Es el que **expande** el cluster |
| **Punto frontera** (*border*) | Tiene menos de MinPts vecinos pero está en la vecindad de un núcleo | Del conteo | Borde de la zona | Se une al cluster, pero no lo expande |
| **Ruido** (*noise*) | Ni núcleo ni frontera | Del conteo | Punto aislado | Queda **fuera** de todo cluster (etiqueta −1) |

```
1. Clasificar cada punto como núcleo, frontera o ruido (según ε y MinPts)
2. Tomar un núcleo no visitado y crear un cluster nuevo
3. Añadir todos sus vecinos dentro de ε; si un vecino también es núcleo,
   añadir sus vecinos (expansión en cadena)
4. Repetir hasta visitar todos los puntos; el ruido queda sin cluster
```
**Desventajas:** una **sola escala ε** hace que falle con clusters de **densidades muy distintas**, y es muy **dependiente de los hiperparámetros**.

### 10.2 Mean Shift
*(Relación: también es densidad, pero en vez de **contar** vecinos, **sube la pendiente** de la densidad hasta su máximo.)*
```
1. Colocar una ventana de tamaño h (ancho de banda) alrededor de cada punto
2. Calcular la media de los puntos dentro de la ventana (centro de masas)
3. Desplazar la ventana a esa media
4. Repetir hasta que casi no se mueva (convergencia a un máximo local de densidad)
5. Los puntos que convergen al mismo máximo forman un cluster
```
- **Ventajas:** no necesita K, admite formas arbitrarias, va directo a los máximos de densidad y funciona bien con clusters solapados.
- **Desventajas:** una sola escala h (h pequeño fragmenta, h grande fusiona), no identifica ruido de forma natural, tiene problemas con densidades distintas o clusters sin máximo claro, y es costoso.
- En sklearn, `estimate_bandwidth(X, quantile=…)` estima h. En el notebook se usa para **segmentar imágenes** por color.

### 10.3 Affinity Propagation
*(No es estrictamente de densidad: elige **datos reales** como representantes, igual que el medoide del bloque 8, pero mediante "votación" entre puntos.)*

| Variable | Qué significa | De dónde sale | Ejemplo concreto | Qué ocurre al iterar |
|---|---|---|---|---|
| s(i, k) | Similitud entre *i* y *k* | Matriz de similitud (por ejemplo, −distancia²) | s = −4 | Fija; no cambia |
| s(k, k) | **Preferencia**: cuánto "quiere" *k* ser representante | Hiperparámetro (por defecto, la mediana de s) | mediana | Si sube, salen **más** clusters |
| r(i, k) | **Responsabilidad**: "¿cuánto quiere *i* que *k* sea su representante?" | s(i,k) − max_{k'≠k}[a(i,k') + s(i,k')] | — | Se actualiza mirando a los competidores de *k* |
| a(i, k) | **Disponibilidad**: "¿qué tan apoyado está *k* por los demás para representar a *i*?" | min(0, r(k,k) + Σ_{i'∉{i,k}} max(0, r(i',k))) | — | Crece si muchos puntos apoyan a *k* |
| damping | Amortiguación de las actualizaciones | Hiperparámetro (0.5–1) | 0.5 | Evita **oscilaciones** |

```
1. Calcular la matriz de similitud s(i, k)
2. Actualizar las responsabilidades r(i, k)
3. Actualizar las disponibilidades a(i, k)
4. Repetir 2-3 hasta que se estabilicen
5. El representante de i es el k que maximiza r(i, k) + a(i, k)
```
- **Ventajas:** no necesita K, se basa en similitudes y admite cualquier medida.
- **Desventajas:** difícil de explicar, problemas con formas diversas, oscilaciones (necesita *damping*) y coste O(N²).

**Código comparativo (como en `Density_v1.py`):**
```python
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN, MeanShift, estimate_bandwidth, AffinityPropagation, KMeans
from sklearn.metrics import adjusted_rand_score

X, y = make_moons(n_samples=500, noise=0.06, random_state=0)
X = StandardScaler().fit_transform(X)                 # ¡escalar primero!

modelos = {
    "KMeans": KMeans(2, n_init=10, random_state=0),
    "DBSCAN": DBSCAN(eps=0.3, min_samples=5),
    "MeanShift": MeanShift(bandwidth=estimate_bandwidth(X, quantile=0.2)),
    "AffinityProp": AffinityPropagation(damping=0.9, random_state=0),
}
for nombre, m in modelos.items():
    lab = m.fit_predict(X)
    print(f"{nombre:13s} clusters={len(set(lab) - {-1})}  ARI={adjusted_rand_score(y, lab):.2f}")
```
- `StandardScaler` iguala las escalas, imprescindible porque ε y h son distancias.
- DBSCAN etiqueta el ruido con `-1`; por eso se excluye al contar clusters.
- El ARI usa las etiquetas reales `y` solo para comparar. Normalmente DBSCAN recupera las dos lunas (ARI ≈ 1), mientras que K-means las corta y Mean Shift o AP tienden a fragmentarlas.

**Conexión con el portafolio:** *Clustering by Fast Search and Find of Density Peaks* (artículo 1) es otro método de densidad. Toma de Mean Shift la idea de los **máximos de densidad** y de DBSCAN el **conteo de vecinos dentro de un radio** (d_c), pero lo resuelve en un solo paso con el grafo de decisión.

<details><summary><b>Verificación:</b> ¿Por qué DBSCAN tiene problemas cuando un cluster es muy denso y otro muy disperso?</summary>

Porque usa **un único ε** para todo el espacio. Un ε adecuado para el cluster disperso fusiona el denso con lo que tenga cerca, y un ε adecuado para el denso deja al disperso como ruido o lo fragmenta.
</details>

> **Nota:** densidad = un cluster es una zona con muchos puntos juntos; DBSCAN cuenta vecinos, Mean Shift sube hacia el pico y AP vota representantes.

---

## Bloque 11: Clustering espectral

**Problema real.** Datos con forma de **dos anillos concéntricos**: los puntos del anillo exterior están **más lejos entre sí** que de algunos del anillo interior, así que la "cercanía al centro" no sirve.

**Analogía.** Una **red de amistades**: dos personas pueden vivir lejos pero estar conectadas por una cadena de amigos. Los grupos son comunidades **muy conectadas por dentro** y **con pocos lazos entre sí**. Para separarlas corto los lazos **más débiles**.

**Dos conceptos previos (son distintos, regla 5):**

| | Convexo | Conexo |
|---|---|---|
| Definición | Cualquier **segmento recto** entre dos puntos del grupo queda dentro del grupo | Cualquier par de puntos se puede unir por un **camino** dentro del grupo |
| Ejemplo | Una mancha redonda | Un anillo, una luna |
| ¿Lo detecta K-means? | Sí | No (si no es convexo) |
| Relación | Todo convexo es conexo | No todo conexo es convexo |

**Concepto.** Se pasa de agrupar por **cercanía** a agrupar por **conectividad**:
1. Los datos se convierten en un **grafo**: nodos = puntos, aristas con **peso** = qué tan similares son.
2. Se busca el **corte óptimo**: el que atraviesa las aristas **más débiles**.
3. Ese corte se encuentra con **álgebra lineal**: los autovalores (el **espectro**) de la **matriz laplaciana**.

**Panorama de símbolos (son varios y parecidos, así que primero el mapa):**

| Variable | Qué significa | De dónde sale | Ejemplo concreto | Qué ocurre al calcular |
|---|---|---|---|---|
| **W** | Matriz de **similitud** (adyacencia o afinidad), m×m, simétrica, 0 ≤ Wᵢⱼ ≤ 1 | De las distancias: umbral ε, kNN o kernel gaussiano exp(−d²/2σ²) | Wᵢⱼ = 1 si d < 5 | Define el grafo; un buen W lo es todo |
| **D** | Matriz de **grado**: diagonal con Dᵢᵢ = Σⱼ Wᵢⱼ | Suma de cada fila de W | Nodo con 3 amigos: Dᵢᵢ = 3 | Mide qué tan conectado está cada nodo |
| **L** | **Laplaciana** | L = D − W (básica); L_rw = I − D⁻¹W (*random walk*); L_sym = I − D^(−½) W D^(−½) (normalizada simétrica) | — | Sus autovalores revelan las comunidades |
| **λ₁ ≤ … ≤ λₙ** | Autovalores de L | Descomposición espectral | 0, 0.01, 0.03, **0.48**, 0.55… | Si el grafo tiene **K componentes conexas**, hay **K autovalores = 0** |
| **u₁…u_K** | Autovectores de los K autovalores más pequeños | Descomposición espectral | Columnas de U (m×K) | Cada fila de U es la **nueva representación** del punto |
| **K** | Número de clusters | **Eigengap**: K = argmaxₖ (λₖ₊₁ − λₖ) | Salto 0.03 → 0.48, así que **K = 3** | Elige K de forma objetiva |

**Algoritmo:**
```
1. Construir el grafo: matriz de similitud W
2. Calcular la matriz de grado D y la Laplaciana L
3. Calcular los autovalores de L
4. Tomar los K autovalores más pequeños y sus autovectores u1..uK
5. Formar U = [u1..uK] (m × K): embedding espectral
6. Aplicar K-means sobre las filas de U
```

**Dos dudas de la clase:**
- **¿Cómo elegir K?** Los clusters reales casi nunca están del todo desconectados, así que los autovalores no son exactamente 0. Se busca un grupo de autovalores pequeños seguido de un **salto grande** (eigengap). Cuidado: puede sugerir clusters anidados.
- **¿Por qué K-means si "no era adecuado"?** Porque la transformación espectral convierte las formas **conexas** (anillos, lunas) en grupos **convexos** en el nuevo espacio, y ahí K-means sí funciona.

**Lecciones del notebook P1_3 (anillos concéntricos):** con W por **umbral ε** inventado y L básica, los autovalores no son claros. Con L **normalizada simétrica** mejora algo. Con W por **kNN** y kernel gaussiano, aparecen exactamente **2 componentes** y la separación es perfecta.
> **Moraleja:** construir W es la decisión crítica; si no conoces un buen umbral, usa kNN.

```python
import numpy as np
from sklearn.datasets import make_circles
from sklearn.neighbors import kneighbors_graph
from scipy.sparse.csgraph import laplacian
from sklearn.cluster import KMeans, SpectralClustering

X, y = make_circles(n_samples=1000, noise=0.05, factor=0.5, random_state=0)

W = kneighbors_graph(X, n_neighbors=10, mode="connectivity", include_self=False)
W = W.maximum(W.T)                                   # 1. grafo simétrico
L = laplacian(W, normed=True).toarray()              # 2. Laplaciana normalizada
vals, vecs = np.linalg.eigh(L)                       # 3. autovalores ordenados
print(vals[:6].round(4))          # [0, 0, 0.0013, 0.0013, 0.002, ...]
K = int(np.sum(vals < 1e-6))                         # nº de autovalores ≈ 0 → 2
U = vecs[:, :K]                                      # 4-5. embedding

# eigengap con los valores de la diapositiva: 0, .01, .03, .48, .55, .68
lam = np.array([0, 0.01, 0.03, 0.48, 0.55, 0.68])
print("K eigengap diapositiva:", np.argmax(np.diff(lam)) + 1)   # → 3
labels = KMeans(K, n_init=10, random_state=0).fit_predict(U)   # 6.

sk = SpectralClustering(n_clusters=2, affinity="nearest_neighbors",
                        random_state=0).fit_predict(X)
print("K por autovalores nulos:", K)
```
- `kneighbors_graph` conecta cada punto con sus 10 vecinos más cercanos; `W.maximum(W.T)` lo hace simétrico (si yo soy tu vecino, tú eres el mío).
- `laplacian(normed=True)` calcula L_sym.
- `eigh` sirve para matrices simétricas y devuelve los autovalores **ordenados** de menor a mayor.
- Aquí los dos anillos **no comparten aristas** en el grafo kNN, así que hay exactamente **2 autovalores = 0**, y contarlos da K = 2.
- **Trampa comprobada al ejecutarlo:** el eigengap **absoluto** (`argmax(np.diff(vals))`) daba **K = 8** en este caso. Los autovalores que siguen a los dos ceros son diminutos (0.0013…), así que el salto 0 → 0.0013 parece pequeño en valor absoluto aunque sea enorme en proporción. El eigengap funciona bien cuando hay un salto claro, como en la diapositiva (0.03 → 0.48 da K = 3). Mira siempre los autovalores impresos, no solo la fórmula.
- K-means sobre `U` agrupa en el nuevo espacio; `SpectralClustering` hace todo esto en una línea.

**Análisis.** Ventajas: formas complejas o no convexas y base matemática sólida. Desventajas: hay que elegir cómo construir W (ε, k, σ) y K; la descomposición en autovalores cuesta O(N³) y no escala a datos grandes; y es sensible al ruido que crea "puentes" entre clusters.

<details><summary><b>Verificación:</b> ¿Por qué el número de autovalores iguales a cero indica el número de clusters?</summary>

Porque la Laplaciana tiene exactamente un autovalor 0 por cada **componente conexa** del grafo, es decir, por cada grupo sin aristas hacia los demás. Cada grupo aislado aporta un autovector "indicador" (constante dentro del grupo y 0 fuera). Si los grupos están casi aislados, los autovalores son casi 0 y luego viene un salto.
</details>

> **Nota:** espectral = datos → grafo → Laplaciana → autovectores pequeños como nuevo espacio → K-means; agrupa por conectividad, no por cercanía.

---

## Bloque 12: Clustering probabilístico, GMM y EM (notebook P1_5)

**Problema real.** Un cliente está justo entre dos segmentos. K-means lo mete a la fuerza en uno; yo preferiría decir "60 % segmento A, 40 % segmento B".

**Analogía.** En una fiesta hay música de tres altavoces. Si estoy en un punto, no oigo un solo altavoz: oigo una **mezcla**, con más volumen del que está más cerca. Cada punto de datos es "un poco" de cada grupo.

**Las tres debilidades de K-means que motivan GMM:**
1. Usa **círculos** o esferas: supone variables independientes (covarianza 0), así que falla con nubes **estiradas**.
2. No controla el **tamaño** de cada círculo; falla con clusters de tamaño dispar.
3. La asignación es **dura** (*hard*), incluso cuando el punto está en la frontera.

**Concepto.** Un **modelo de mezcla de gaussianas** supone que los datos fueron **generados** por K gaussianas, cada una con su posición, forma y peso. Es un modelo **generativo**: además de agrupar, **estima la densidad** y puede **generar datos nuevos**.

| Variable | Qué significa | De dónde sale | Ejemplo concreto | Qué ocurre en EM |
|---|---|---|---|---|
| K | Número de componentes | Hiperparámetro (AIC/BIC) | 3 | Fijo |
| πₖ | **Peso** de la componente *k* (Σπₖ = 1) | Fracción de puntos que "explica" *k* | 0.5, 0.3, 0.2 | Se actualiza en el paso M |
| μₖ | **Posición** (media) | Media ponderada de los puntos | (2, 3) | Se actualiza en el paso M |
| Σₖ | **Forma y orientación** (covarianza) | Covarianza ponderada | Elipse inclinada | Se actualiza en el paso M |
| γᵢₖ (ẑᵢₖ) | **Responsabilidad**: probabilidad de que el punto *i* venga de *k* | Regla de Bayes | 0.6 / 0.4 | Se calcula en el paso E |

**Modelo:** p(x) = Σₖ πₖ · 𝒩(x | μₖ, Σₖ)

**Algoritmo EM (Expectation-Maximization):**
```
1. Inicializar πk, μk, Σk (por ejemplo, con K-means)
2. Paso E: γik = πk N(xi|μk,Σk) / Σj πj N(xi|μj,Σj)        (pertenencia suave)
3. Paso M: Nk = Σi γik ;  πk = Nk / N ;  μk = Σi γik xi / Nk ;
           Σk = Σi γik (xi − μk)(xi − μk)ᵀ / Nk
4. Repetir E-M hasta que la log-verosimilitud deje de aumentar
```
**Relación con lo anterior:** EM **es la versión suave de K-means**. El paso E equivale a "asignar" (pero con probabilidades) y el paso M a "mover el centroide" (pero también actualiza forma y peso). Igual que K-means, es **sensible a la inicialización** y puede quedarse en máximos locales, así que se ejecuta varias veces (`n_init`).

**Tipos de covarianza (`covariance_type`):**

| Tipo | Forma del cluster | Nº de parámetros |
|---|---|---|
| `spherical` | Círculos (un único valor de varianza) | Pocos |
| `diag` | Elipses alineadas con los ejes | Medio |
| `full` | Elipses con cualquier orientación | Muchos (más flexible, más riesgo de sobreajuste) |

**¿Cuántas componentes?** Minimizar **AIC = 2p − 2 ln L** o **BIC = p ln N − 2 ln L**, donde p es el nº de parámetros y L la verosimilitud. El BIC penaliza más y elige modelos más simples. Ojo: esto mide la calidad como **estimador de densidad**, no como algoritmo de clustering. Por ejemplo, para las lunas, AIC sugiere entre 8 y 12 componentes aunque visualmente hay 2 grupos.

```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.mixture import GaussianMixture

X, _ = make_blobs(n_samples=400, centers=3, cluster_std=0.75, random_state=0)
X = X @ np.random.RandomState(13).randn(2, 2)            # datos "estirados"

bics = {k: GaussianMixture(k, covariance_type="full", random_state=0).fit(X).bic(X)
        for k in range(1, 8)}
k_best = min(bics, key=bics.get)

gmm = GaussianMixture(k_best, covariance_type="full", n_init=5, random_state=0).fit(X)
labels = gmm.predict(X)            # asignación dura (máxima probabilidad)
probs = gmm.predict_proba(X)       # asignación suave: matriz N×K
X_nuevos, _ = gmm.sample(100)      # modelo generativo: crear datos
print(k_best, probs[:3].round(2))
```
- El producto `X @ ...` estira la nube, igual que en el notebook, para mostrar dónde falla K-means.
- El diccionario `bics` prueba de 1 a 7 componentes y `min` elige la de menor BIC. Al ejecutarlo eligió **4**, aunque los datos se generaron con 3: BIC optimiza la **densidad**, no "los grupos verdaderos".
- `predict` da la asignación dura y `predict_proba` la suave (cada fila suma 1).
- `sample` genera puntos nuevos; con dígitos (110 componentes según el AIC) produce imágenes nuevas creíbles.

**Análisis.** Ventajas: clusters elípticos de distinto tamaño, probabilidades de pertenencia y capacidad generativa. Desventajas: supone gaussianidad, hay que elegir K, sufre máximos locales, `full` tiene muchos parámetros en alta dimensión, y no sirve para formas no convexas con pocas componentes (para eso, densidad o espectral). **Será la base del Tema 3 (semi-supervisado).**

<details><summary><b>Verificación:</b> ¿Por qué se dice que K-means es un caso particular de GMM?</summary>

Porque si en GMM todas las covarianzas son esféricas, iguales y tienden a 0, y los pesos son iguales, la responsabilidad γᵢₖ se vuelve 1 para la componente más cercana y 0 para las demás. El paso E se convierte en "asignar al centroide más cercano" y el paso M en "mover a la media", que es exactamente K-means.
</details>

> **Nota:** GMM = mezcla de gaussianas ajustada con EM; da probabilidades de pertenencia y puede generar datos.

---

## Bloque 13: Síntesis comparativa

| Algoritmo | ¿Necesita K? | Formas | Ruido / outliers | Hiperparámetros clave | Coste | Úsalo cuando… |
|---|---|---|---|---|---|---|
| **K-means** | Sí | Convexas, esféricas | Sensible | K, inicialización | Bajo | Grupos compactos y muchos datos |
| **K-means++** | Sí | Ídem | Sensible | K | Bajo | Siempre como arranque de K-means |
| **K-medoids** | Sí | Convexas | **Robusto** | K, distancia | Medio-alto | Hay outliers o distancias no euclídeas |
| **Jerárquico** | No (cortar el dendrograma) | Según el enlace | Single es sensible | Distancia, enlace | Alto (O(N²)) | Pocos datos y se quiere ver la jerarquía |
| **DBSCAN** | **No** | **Arbitrarias** | **Lo detecta** | ε, MinPts | Medio | Formas raras con ruido y densidad similar |
| **Mean Shift** | No | Arbitrarias | No lo marca | h | Alto | Se buscan modos de densidad o segmentar imágenes |
| **Affinity Propagation** | No | Limitadas | — | Preferencia, damping | O(N²) | Se quieren representantes reales |
| **Espectral** | Sí (eigengap) | **Conexas no convexas** | Sensible a "puentes" | Construcción de W (k, ε, σ), K | Alto (O(N³)) | Anillos, lunas, estructuras de grafo |
| **GMM** | Sí (AIC/BIC) | Elípticas | Sensible | K, tipo de covarianza | Medio | Se quieren probabilidades o generar datos |

**Pregunta de repaso global (para cuando todos los bloques estén firmes):**
<details><summary>Tienes datos con forma de dos lunas más algunos puntos sueltos de ruido. ¿Qué algoritmo eliges y por qué no K-means ni GMM?</summary>

**DBSCAN**, porque detecta formas **no convexas** y marca el ruido como −1. K-means corta las lunas porque solo forma regiones convexas. GMM con 2 componentes usa elipses, que tampoco siguen la curva. El espectral también separaría las lunas, pero no marca el ruido y los puntos sueltos pueden crear puentes en el grafo.
</details>

### Conexión con los 6 artículos del portafolio

| Artículo | Bloque del curso con el que conecta |
|---|---|
| 1. *Clustering by Fast Search and Find of Density Peaks* | Bloque 10 (densidad): mezcla ideas de DBSCAN (radio d_c) y Mean Shift (máximos de densidad) |
| 2. *Self-Supervised… Image Context Restoration* | Bloque 1 (auto-supervisado) → Tema 6 (representaciones profundas) |
| 3. *Least Squares GAN* | Tema 6 (deep clustering basado en **modelos generativos**); métrica FID (bloque 5) |
| 4. *T5: Text-to-Text Transformer* | Bloque 1 (auto-supervisado: pre-entrenar sin etiquetas con *denoising*) |
| 5. *Insurance Fraud Detection (AE/VAE)* | Tema 7 (**detección de anomalías**) y Tema 6 (autoencoders); métrica de **error de reconstrucción** (bloque 5) |
| 6. *SSL for Medical Image Classification (revisión)* | Bloque 1 (auto-supervisado); **pérdida contrastiva** (bloque 5); Tema 6 |

### Temario que aún no está en SESIONES (pendiente)
T3 semi-supervisado (GMM/EM aplicado), T4 PCA/ICA, T5 PageRank y recomendación, T6 deep clustering y T7 aplicaciones.

---

## Diagnóstico inicial (para ir actualizando)

| Bloque | Estado |
|---|---|
| 1–5 Fundamentos, distancia, evaluación | Pendiente de verificar |
| 6–8 K-means y mejoras | Pendiente de verificar |
| 9 Jerárquico | Pendiente de verificar |
| 10 Densidad | Pendiente de verificar |
| 11 Espectral | Pendiente de verificar (el más abstracto: dedícale más tiempo) |
| 12 GMM/EM | Pendiente de verificar |

> Cuando quieras estudiarlo conmigo, dime el bloque. Iremos **un concepto a la vez**, con la pregunta de verificación antes de avanzar.

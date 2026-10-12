# Clustering by Fast Search and Find of Density Peaks

- **Autores:** Alex Rodriguez y Alessandro Laio (SISSA, Trieste, Italia)
- **Publicación:** *Science* 344(6191), 1492–1496, 27 de junio de 2014. DOI: 10.1126/science.1242072
- **Área:** Machine Learning → Clustering (agrupamiento) basado en densidad
- **Siglas habituales:** DPC (*Density Peaks Clustering*), CFSFDP
- **¿Corresponde al curso de Aprendizaje No Supervisado?** **Sí, de lleno.** Es un algoritmo de clustering puro: no usa etiquetas en ningún momento, descubre el número de grupos, detecta outliers y trabaja solo con distancias entre puntos.

---

## 1. Problema que aborda

El clustering clasifica elementos en grupos según su similitud, pero **no hay consenso ni siquiera sobre qué es un clúster**. Los métodos existentes tienen limitaciones:

| Método | Idea | Limitación señalada por los autores |
|---|---|---|
| **K-means / K-medoids** | Minimizar la distancia de cada punto a un centro; cada punto va al centro más cercano | No detecta clústeres **no esféricos**; hay que fijar K; optimización iterativa |
| **Modelos de mezcla (EM)** | Ajustar los datos como mezcla de distribuciones predefinidas | La precisión depende de que la distribución elegida represente bien los datos |
| **DBSCAN** | Umbral de densidad; las regiones densas desconectadas son clústeres y el resto es ruido | Elegir el umbral **no es trivial**; puede marcar como ruido clústeres de baja densidad |
| **Mean-shift** | Un clúster = puntos que convergen al mismo máximo local de densidad | Requiere que los datos estén en un **espacio vectorial** (coordenadas) y es **costoso** (maximizar la densidad para cada punto) |

**Objetivo:** un método que (a) use solo distancias (como K-medoids), (b) detecte clústeres de forma arbitraria y encuentre automáticamente su número (como DBSCAN o mean-shift), (c) sin incrustar los datos en un espacio vectorial ni maximizar explícitamente un campo de densidad.

## 2. Idea central (hipótesis)

Los **centros de clúster** cumplen dos propiedades simultáneamente:
1. Tienen una **densidad local mayor** que sus vecinos.
2. Están a una **distancia relativamente grande** de cualquier punto con densidad mayor.

## 3. Método

Para cada punto *i* se calculan dos cantidades que **solo dependen de las distancias** d_ij (que deben cumplir la desigualdad triangular):

### 3.1 Densidad local ρ_i (kernel de corte)

$$\rho_i = \sum_j \chi(d_{ij} - d_c), \qquad \chi(x)=1 \text{ si } x<0,\; 0 \text{ en otro caso}$$

- ρ_i = número de puntos a distancia menor que **d_c** (distancia de corte) del punto *i*.
- Solo importa el **orden relativo** de las densidades, por lo que en datasets grandes el resultado es **robusto a la elección de d_c**.
- **Regla práctica:** elegir d_c de modo que el número medio de vecinos sea el **1–2 % del total de puntos**.
- Con pocos puntos se recomienda un **kernel gaussiano o exponencial** (densidad más precisa).

### 3.2 Distancia a puntos de mayor densidad δ_i

$$\delta_i = \min_{j:\rho_j>\rho_i} d_{ij}$$

- Para el punto de máxima densidad se toma por convención δ_i = max_j d_ij.
- δ_i es mucho mayor que la distancia típica al vecino más cercano **solo en los máximos locales o globales de densidad**.

### 3.3 Grafo de decisión (*decision graph*)

Se grafica δ frente a ρ para todos los puntos:
- **Centros de clúster:** ρ alto **y** δ anómalamente alto (esquina superior derecha).
- **Outliers:** δ relativamente alto pero ρ **bajo** (clústeres de un solo punto).
- **Resto de puntos:** δ pequeño.

El número de clústeres "surge de forma intuitiva" al ver el grafo. Para casos ambiguos se usa **γ_i = ρ_i · δ_i** ordenado de forma decreciente: los centros están antes del punto donde γ cae de forma brusca.

### 3.4 Asignación (un solo paso)

Una vez fijados los centros, **cada punto restante se asigna al mismo clúster que su vecino más cercano de mayor densidad**. Se hace en un único recorrido (orden decreciente de densidad), **sin optimización iterativa** de una función objetivo, a diferencia de K-means o EM.

### 3.5 Núcleo (*core*) y halo (fiabilidad de la asignación)

En vez de un umbral global de ruido (como DBSCAN):
1. Para cada clúster se define una **región frontera**: puntos del clúster a distancia < d_c de puntos de otros clústeres.
2. Se toma la densidad máxima en esa frontera, **ρ_b**.
3. Puntos con ρ > ρ_b → **núcleo** (asignación robusta). Puntos con ρ ≤ ρ_b → **halo** (pueden considerarse ruido).

Ventaja: clústeres de baja densidad no se descartan como ruido.

### Pseudocódigo resumido
```
1. Calcular la matriz de distancias d_ij
2. Para cada i: ρ_i = nº de vecinos a distancia < d_c
3. Para cada i: δ_i = distancia mínima a un punto con ρ mayor
4. Construir el grafo de decisión (ρ, δ) y escoger como centros los puntos con ρ y δ altos (o top γ = ρ·δ)
5. Recorrer los puntos en orden de ρ decreciente: etiqueta(i) = etiqueta(vecino más cercano con mayor ρ)
6. (Opcional) Calcular ρ_b por clúster y separar núcleo/halo
```

**Complejidad:** O(N²) en tiempo y memoria (hay que calcular todas las distancias por pares).

## 4. Experimentos y resultados

| Experimento | Resultado |
|---|---|
| **Ejemplo de 28 puntos en 2D** (Fig. 1) | Centros en los puntos 1 y 10; los puntos 26, 27 y 28 se identifican como outliers |
| **Distribución sintética** con 5 picos no esféricos y solapados, densidades que difieren casi un orden de magnitud y 20 % de fondo uniforme (4000 y 1000 puntos) | 5 centros claros en el grafo de decisión; captura la forma de los picos; el halo coincide con zonas sin pico |
| **Robustez al tamaño de muestra** (referencia de 10 000 puntos) | Fracción de puntos mal clasificados **< 1 %** incluso con 1000 puntos |
| **Variación de d_c** | Resultados consistentes entre sí |
| **Benchmarks de la literatura:** Gionis et al. (agregación), Fränti (15 clústeres solapados), FLAME, *path-based spectral clustering* (espirales) | Resultados comparables a los métodos originales; las 3 espirales se detectan sin construir un grafo de conectividad. **K-means falla** en la mayoría aun conociendo el K correcto |
| **Cambio de métrica** | Robusto si no cambian las distancias menores que d_c: la estructura del grafo depende del **ranking** de densidades |
| **Alta dimensión:** 16 clústeres en 256 dimensiones | Encuentra el número correcto y asigna bien (no depende de la dimensión intrínseca) |
| **Semillas de trigo** (210 muestras, 7 rasgos, 3 tipos) | Predice 3 clústeres; **97 %** de acierto en los núcleos |
| **Olivetti Face Database** (40 sujetos × 10 imágenes) | Primeras 100 imágenes: 9 centros, reconoce 7 de 10 sujetos. Base completa: ~30 sujetos sin ambigüedad; sin corte en d_c: r_true ≈ 68 %, r_false ≈ 1.2 % con ~42–50 centros, comparable al estado del arte |
| **Dinámica molecular** de trialanina en agua a 300 K | 8 clústeres en correspondencia 1 a 1 con las 8 cuencas cinéticas del análisis espectral estándar |

## 5. Mejoras respecto a métodos anteriores

1. **Número de clústeres sin fijarlo a priori** (frente a K-means/K-medoids).
2. **Clústeres de forma arbitraria** (frente a K-means).
3. **Solo necesita distancias**: no exige coordenadas ni espacio vectorial (frente a mean-shift) ni parametrizar distribuciones (frente a EM).
4. **Asignación en un único paso**, sin optimización iterativa.
5. **Detección automática de outliers**.
6. **Sin umbral global de ruido**: el núcleo/halo es local por clúster, así que los clústeres poco densos no se pierden (frente a DBSCAN).
7. **Insensible a la dimensión intrínseca** del espacio.

## 6. Limitaciones (reconocidas o evidentes)

- **Elección manual de centros** en el grafo de decisión; en datos dispersos (Olivetti) el número de centros **no es claro**.
- **Sensibilidad a d_c** en datasets pequeños (errores estadísticos grandes en ρ); hubo que usar un criterio de asignación más restrictivo.
- **Ruido aleatorio:** en una muestra finita uniforme aparecen máximos de densidad espurios. Los autores observan que para datos aleatorios γ sigue una **ley de potencias** (con exponente dependiente de la dimensión), mientras que con clústeres reales no; esto podría servir para **seleccionar centros automáticamente y validar estadísticamente** el análisis (queda propuesto, no implementado).
- **Propagación de errores** en la asignación en cadena: si un punto se asigna mal, todos los que dependen de él heredan el error.
- **Coste O(N²)** en memoria y tiempo.

## 7. Conceptos clave para el examen

- **Densidad local (ρ):** número de vecinos dentro de un radio d_c.
- **δ:** distancia al punto más cercano con mayor densidad.
- **Grafo de decisión:** gráfico δ vs ρ para elegir centros.
- **γ = ρ·δ:** puntuación para ordenar candidatos a centro.
- **Núcleo/halo:** separación entre asignación fiable y posible ruido usando ρ_b.
- **Comparación:** K-means (esférico, K fijo), DBSCAN (umbral de densidad), mean-shift (máximos de densidad pero costoso y vectorial).

## 8. Variantes posteriores conocidas en la literatura (contexto adicional, no forman parte del artículo)

- **DPC-KNN** (Du et al., 2016): densidad basada en k vecinos más cercanos en lugar de d_c.
- **FKNN-DPC** (Xie et al., 2016): asignación con k vecinos ponderados difusos para evitar la propagación de errores.
- Versiones aproximadas o distribuidas para reducir el coste O(N²).

# Portafolio Artículo Científico: Aprendizaje No Supervisado
**Alumno:** Lucas Tamara · **Artículo:** A. Rodriguez y A. Laio, "Clustering by fast search and find of density peaks", *Science* 344, 1492 (2014)

---

## PÁGINA 1: Resumen y propuesta de mejora

### 1. Resumen

**Problema.** El clustering busca agrupar elementos por similitud sin etiquetas, pero los métodos clásicos tienen carencias. K-means y K-medoids asignan cada punto al centro más cercano, así que solo detectan grupos esféricos y exigen fijar K. Los modelos de mezcla (EM) dependen de que la distribución elegida describa bien los datos. DBSCAN encuentra formas arbitrarias, pero requiere un umbral de densidad difícil de elegir y puede descartar como ruido los clústeres poco densos. Mean-shift evita ese umbral, pero solo funciona con datos en un espacio vectorial y es costoso.

**Método propuesto (DPC).** Parte de una hipótesis simple: un centro de clúster tiene **mayor densidad que sus vecinos** y está **lejos de cualquier punto más denso**. Para cada punto *i* se calculan, usando solo las distancias d_ij, dos cantidades:
1. La densidad local ρ_i = nº de puntos a distancia < d_c. Basta con el orden relativo; la regla práctica es que haya entre un 1 y un 2 % de vecinos.
2. δ_i = distancia mínima a un punto de mayor densidad.

En el **grafo de decisión** (δ frente a ρ), los centros aparecen con ρ y δ altos, y los outliers con δ alto y ρ bajo. Si hay dudas, se ordena γ = ρ·δ. Después, cada punto se asigna **en un solo paso** al clúster de su vecino más cercano de mayor densidad. Por último, una densidad frontera ρ_b separa en cada clúster un **núcleo** fiable y un **halo** que puede tratarse como ruido.

**Mejoras frente a métodos previos.** No hay que fijar el número de clústeres; detecta formas arbitrarias y outliers; no necesita coordenadas ni distribuciones paramétricas; no hay optimización iterativa; y no impone un umbral global de ruido. En los experimentos, el error es < 1 % con solo 1000 puntos; supera a K-means en los benchmarks de la literatura (incluidas las espirales); acierta 16 clústeres en 256 dimensiones y el 97 % de los núcleos en semillas de trigo; en Olivetti es comparable al estado del arte (r_true ≈ 68 %, r_false ≈ 1.2 %); y recupera las 8 cuencas cinéticas de una dinámica molecular.

### 2. Opinión y propuesta de mejora

**Opinión.** El método es elegante e intuitivo, y el grafo de decisión lo hace muy interpretable. Sin embargo, el propio artículo muestra tres debilidades:
- La **elección de centros es manual** (en Olivetti el número de clústeres "no está claro").
- **ρ depende de d_c** y es ruidosa con pocos datos (hubo que endurecer el criterio de asignación).
- La **asignación en cadena propaga errores**: si un punto se asigna mal, todos los que dependen de él heredan el error.

A esto se suma un coste de **O(N²)** en memoria.

**Propuesta: DPC adaptativo con k vecinos (tres cambios).**
- **(a) Densidad adaptativa.** Sustituir el corte d_c por ρ_i = exp(−(1/k)·Σ_{j∈kNN(i)} d_ij²), con k ≈ 1–2 % de N. Así se conserva la regla práctica original, pero la densidad se adapta a regiones de distinta escala y deja de ser un contador discreto (con menos empates y menos ruido en muestras pequeñas).
- **(b) Selección automática de centros.** Los autores observan que, en datos sin estructura, γ sigue una **ley de potencias**. Propongo ajustar esa ley a la distribución de log γ y declarar centros solo los puntos cuyo γ se sale significativamente del ajuste (residuo > 3σ). Esto elimina la elección manual y da una **validación estadística**: si ningún punto se sale, no hay clústeres reales.
- **(c) Asignación en dos fases.** Primero se aplica la cadena original solo a los puntos de alta densidad (núcleo); después, los puntos frontera y del halo se asignan por **voto ponderado de sus k vecinos ya etiquetados**, para que un error aislado no se propague.

**Justificación y validación.** Cada cambio ataca una limitación observada en el propio artículo. Variantes publicadas con ideas similares (DPC-KNN, Du et al. 2016; FKNN-DPC, Xie et al. 2016) informan de mejoras, lo que respalda su viabilidad. Además, con estructuras kNN (KD-tree o vecinos aproximados) no hace falta guardar la matriz completa de distancias, con lo que la memoria baja de O(N²) a O(N·k). Lo evaluaría con ARI/NMI en los mismos conjuntos (Aggregation, S-sets, Flame, Spiral, Olivetti) frente a DPC original, K-means y DBSCAN.

---

## PÁGINA 2: Prompts del contenido generado por IA

**Herramienta:** Claude Code (Anthropic), modelo Claude Opus 5.5. Fecha: 05/10/2026.

**Uso de la IA:** leer y resumir los 6 artículos propuestos, analizar su pertinencia para la asignatura, redactar un primer borrador del resumen y de la propuesta de mejora, y maquetar el PDF. La elección del artículo, la revisión del contenido y el criterio final son del alumno.

**Prompt 1:**
> "lee esta ruta C:\Users\Lucas Tamara\Desktop\M IA\APRENDIZAJE NO SUPERVISADO\Portafolios Artículo Cientifico y entiende el txt y yo descarge lo que me dijo el profesor analiza cada pdf y extraer todo el conocimiento de cada pdf y generar .md todo el conocmieto y le pones el nombre de cada pdf segun su titulo y luego resuelve el txt que me pide"

**Prompt 2:**
> "analiza si el pdf corresponde al curso de aprendizaje no supervizado"

*(Añadir aquí cualquier otro prompt utilizado.)*

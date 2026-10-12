# Insurance Fraud Detection with Unsupervised Deep Learning

- **Autores:** Chamal Gomes, Zhuo Jin (University of Melbourne), Hailiang Yang (The University of Hong Kong)
- **Publicación:** *Journal of Risk and Insurance* (2021); versión de trabajo de 28 páginas
- **Área:** Detección de anomalías y fraude, ciencia actuarial, deep learning no supervisado
- **¿Corresponde al curso de Aprendizaje No Supervisado?** **Sí, de lleno.** Usa **autoencoders (AE) y autoencoders variacionales (VAE)** entrenados **sin etiquetas** para detectar anomalías mediante el error de reconstrucción, y propone una metodología de **importancia de variables no supervisada**.

---

## 1. Problema
- El fraude en seguros (definición de Gill et al., 2005) consiste en reclamaciones ficticias, infladas o deshonestas. Según el Insurance Council of Australia puede ser **oportunista, premeditado o por no revelar información**.
- La detección tradicional se basaba en **auditoría manual**, que no escala, y el *modus operandi* de los criminales cambia constantemente.
- Los modelos **supervisados** (los más estudiados) tienen problemas en este contexto:
  - En la práctica **no existen etiquetas**: verificar el fraude caso a caso es caro y lento, y las etiquetas pueden ser erróneas o sesgadas (errores de comisión, omisión y mala clasificación).
  - **Fuerte desbalance de clases**.
  - No se adaptan a un fraude que **cambia en el tiempo**.
- Además, los aseguradores quieren saber **qué variables impulsan el fraude**. Los métodos de importancia de variables existentes (random forest, GBM) son **supervisados** y tienen sesgos (inflan las variables continuas o de alta cardinalidad).

## 2. Datos
| Dataset | Descripción | Desbalance |
|---|---|---|
| **D1** | Reclamaciones de seguro de auto (Oracle), 15 478 pólizas, 33 rasgos (32 categóricos, con *integer encoding* y normalización) | 218 fraudes frente a 14 900 no fraudes |
| **D2** | Transacciones con tarjeta de crédito europeas (septiembre de 2013, Worldline y ULB), 284 807 registros, V1–V28 (componentes PCA), monto y tiempo | 492 fraudes frente a 284 315 no fraudes |
| **D3** | Reclamaciones de una aseguradora española (2015–2016, Mendeley), 272 858 casos, rasgos anonimizados | 2379 fraudes confirmados; **270 479 sin identificar** (sin etiqueta) |

## 3. Modelos
### 3.1 Autoencoder (AE)
- Encoder f que comprime la entrada en un **cuello de botella** de menor dimensión (AE *undercomplete*) y decoder g que reconstruye: r(x) = g(f(x)).
- Capas: z⁽¹⁾ = tanh(W₁x + b₁), z⁽²⁾ = tanh(W₂z⁽¹⁾ + b₂), z⁽³⁾ = tanh(W₃z⁽²⁾ + b₃), x̂ = ReLU(W₄z⁽³⁾ + b₄).
- Pérdida **MSE** J = Σᵢ(x̂ⁱ − xⁱ)², optimizada con **Adam** y retropropagación.
- **Idea para detectar anomalías:** como los datos son casi todos no fraudulentos, el AE aprende a reconstruir bien lo **normal**; el fraude tendrá un **error de reconstrucción alto**.

### 3.2 Autoencoder variacional (VAE)
- Modelo **generativo probabilístico**: p_θ(x) = ∫ p_θ(x|z) p_θ(z) dz es intratable, así que se aproxima el posterior con q_φ(z|x).
- Se usa la **KL inversa**, que tiene un comportamiento de búsqueda de moda (*mode-seeking*, *zero-forcing*).
- Se maximiza la **ELBO**: L = E_q[log p_θ(x|z)] − KL(q_φ(z|x) ‖ p(z)), es decir, un término de reconstrucción más un regularizador.
- **Truco de reparametrización:** z = μ + Σ ⊙ ε con ε ~ N(0, I), lo que permite usar SGD.
- Prior N(0, I), posterior gaussiano diagonal y verosimilitud gaussiana (datos continuos).
- KL entre gaussianas: ½[log|Σ₂|/|Σ₁| − k + tr(Σ₂⁻¹Σ₁) + (μ₂ − μ₁)ᵀΣ₂⁻¹(μ₂ − μ₁)].
- El decoder es un MLP gaussiano (3 capas en D1 y 5 en D2).

## 4. Clasificación de fraude con el error de reconstrucción
- **A-RE** (error de reconstrucción agregado por instancia) = Σⱼ (xⱼⁱ − x̂ⱼⁱ), calculado sobre el 20 % de test.
- Sin usar etiquetas, la distribución del A-RE muestra una masa grande con error bajo y una **cola** con error alto.
- **Regla:** si A-RE ≥ T, se clasifica como fraude.
- Al validar con etiquetas se confirma: el no fraude tiene A-RE bajo y el fraude, alto (más claro en D2 que en D3).
- El VAE permite además usar la **probabilidad de reconstrucción** (An y Cho, 2015), una medida comparable entre modelos, pero que **no permite importancia de variables**.

## 5. Contribución principal: importancia de variables no supervisada
Se usa el **error de reconstrucción a nivel de nodo (NL-RE)**: para cada variable *j*, Σᵢ(xⱼⁱ − x̂ⱼⁱ) sobre las instancias.

**Tres pasos:**
1. **Paso 1:** análisis del A-RE para quedarse con la **cola superior** (instancias con A-RE > umbral, es decir, probables fraudes).
2. **Paso 2:** NL-RE agregado sobre esas instancias; las variables con mayor NL-RE son los **impulsores del fraude**.
3. **Paso 3:** NL-RE sobre la **cola inferior** (no fraude) y **descartar las variables comunes** con el paso 2, que son variables difíciles de reconstruir en general y no específicas del fraude.

### Resultados de importancia
| Dataset | AE | VAE | Nota |
|---|---|---|---|
| **D1** | Location code, marital status, education | Claim reason, location code, marital status | D1 **no es un buen candidato**: su distribución de A-RE no está claramente sesgada (pocos datos), y el paso 3 da variables comunes |
| **D2** | V1, V8, V2 en el paso 2; tras el paso 3 (V1 también está en la cola inferior) quedan **V8 y V2** | **V2, V8, V7** (sin cambios tras el paso 3) | Dataset más adecuado |
| **D3** | V239, V248, V68 | V74, V28, V36 | Ninguna se repite en el análisis agregado, así que no hace falta el paso 3 |

Si se omite el paso 1 (NL-RE sobre todo el conjunto), se obtienen **impulsores engañosos**, por ejemplo education, months since policy inception y open complaints en D1.

## 6. Umbral y métricas
- Métricas para clases desbalanceadas: **precision, recall, F1** y sus versiones **ponderadas**. Las ponderadas **ocultan** el rendimiento de la clase minoritaria (fraude).
- Hay un **compromiso** entre ambas: subir el umbral aumenta la precisión y reduce el recall.
- La "**escala de importancia**" entre recall y precisión la fija el asegurador; normalmente un **falso negativo es más costoso** que un falso positivo.
- Los autores lo llaman uso "proactivo" de las métricas (se elige el umbral) frente al "retrospectivo" de los modelos supervisados (un único resultado).

| Modelo en D2 (test de 71 202) | TP | FN | FP | Precisión | Recall | F1 |
|---|---|---|---|---|---|---|
| **AE, RE-T = 30** | 120 | **18** | 1965 | 0.058 | 0.870 | 0.108 |
| AE, RE-T = 40 | 106 | 32 | 901 | 0.105 | 0.768 | 0.185 |
| VAE, RE-T = 60 | 111 | 27 | 1229 | 0.083 | 0.804 | 0.150 |
| K-NN (supervisado) | 115 | 23 | 7 | 0.943 | 0.833 | 0.885 |
| Random Forest (supervisado) | 117 | 21 | 8 | 0.936 | 0.848 | **0.890** |
| Naive Bayes (supervisado) | 119 | 19 | 1578 | 0.070 | 0.862 | 0.130 |

- Los supervisados tienen **mejor F1**, pero **usaron etiquetas de alta calidad**. Los no supervisados logran **pocos FN sin ninguna etiqueta** (el AE solo deja escapar 18 fraudes).
- Sin etiquetas, el asegurador puede fijar el umbral en la cola, probarlo durante un periodo y ajustarlo con *feedback* (quejas o fraudes descubiertos) o con unos pocos casos históricos.
- En D1 no hay diferencias significativas entre AE y VAE; el umbral es **muy sensible** (pocos datos o datos de mala calidad).

## 7. Conclusiones
- Es un marco **base para empezar a detectar fraude sin etiquetas** y obtener información sobre los impulsores del fraude, de forma **barata y actualizable**.
- Aplicaciones futuras: comportamiento de los asegurados, impacto climático en las reclamaciones, **compensación laboral (workers' compensation)**, VAE hiperesféricos.

## 8. Limitaciones (análisis crítico)
- La precisión es muy baja (miles de falsos positivos), lo que implica un **coste de auditoría** alto.
- El umbral del paso 1 y la elección del "top 3" son **heurísticos**.
- El NL-RE definido como suma **con signo** (sin valor absoluto ni cuadrado) permite que los errores se cancelen.
- No hay comparación con otros detectores no supervisados (Isolation Forest, LOF, One-Class SVM).
- En D2 las variables son componentes PCA anonimizadas, así que la "interpretabilidad" es limitada.
- Las conclusiones dependen mucho del dataset (D1 falla).

## 9. Conceptos clave
Detección de anomalías, autoencoder *undercomplete*, cuello de botella, error de reconstrucción (A-RE y NL-RE), VAE, ELBO, KL inversa, reparametrización, desbalance de clases, umbral, precisión/recall/F1 y su versión ponderada, coste de FN frente a FP.

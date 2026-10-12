# Reservoir Computing in Alpha Forecasting of Foreign Exchange Market

**Extracción de conocimiento: 2026-10-02** (leído el texto completo, 49 páginas; las páginas citadas son las del PDF)

| Campo | Valor |
|---|---|
| Título exacto | Reservoir Computing in Alpha Forecasting of Foreign Exchange Market |
| Autor | Yingzhuo He (supervisor interno: Lukas Gonon; colaboración con el equipo de negociación electrónica de divisas de Deutsche Bank) |
| Tipo / Venue / Año | Tesis de máster (MSc in Mathematics and Finance), Imperial College London, Departamento de Matemáticas, 2022-2023 (firmada el 2023-09-04) |
| Archivo local | `212199274---Anthea-He---HE_YINGZHUO_02272118.pdf` |
| URL / DOI | SIN DOI en el documento |
| Métodos | Red de estado de eco (echo state network, ESN) y "firma aleatorizada" (randomized signature) como reservorios; regresión lineal (OLS), lasso, elastic net; análisis de componentes principales (PCA); bootstrap de bloques móviles |
| Datos | Libro de órdenes y libro de operaciones del par USD/MXN, enero a diciembre de 2022, por tick (22 829 398 registros tras unir ambos libros) (p. 28) |

## Aporte clave

Compara dos reservorios de bajo coste de entrenamiento (ESN y firma aleatorizada) frente a una regresión lineal simple para predecir el **alfa** (retorno futuro del precio medio) de USD/MXN a 50 ticks. Concluye que ambos reservorios tienen capacidad predictiva y superan a la regresión lineal, **pero solo si se combinan con reducción de dimensión (PCA) y una regresión penalizada (elastic net)** (p. 43 y p. 46). La ventaja no viene del reservorio solo, sino de la combinación estructura + PCA + lectura penalizada (p. 42).

## Hallazgos cuantitativos (HECHO, con página)

- **Modelos de una variable (solo el alfa pasado):** la regresión lineal da R² medio negativo, −0.141 % con 10 días de entrenamiento. El ESN con elastic net y PCA da +0.0328 % y la firma aleatorizada con elastic net y PCA +0.0323 %. El porcentaje de ventanas con R² > 0 es 43.2 % para la regresión lineal y 54.8 % / 55.6 % para ESN y firma con PCA (Tabla 3.5, p. 35).
- **Modelos de varias variables (flujo de órdenes, desbalance de cola, precio operado menos medio):** con 10 días de entrenamiento, R² medio de 0.784 % para la regresión lineal; 0.943 % para ESN con elastic net y PCA y 0.937 % para firma aleatorizada con elastic net y PCA (Tabla 3.7, p. 44). El R² > 0 ocurre en 92.4 % (regresión lineal) frente a 97.6 % y 98 % (p. 44).
- **Los R² son muy pequeños** (menores de 1 %). Es una mejora relativa y estadísticamente descriptiva, no una predicción fuerte.
- **Horizonte:** cuanto más corto, mejor. Se eligió (retardo, horizonte) = (50, 50) ticks, aproximadamente 1 segundo; también se probó 100 (≈ 1 minuto) y 500 (≈ 8 minutos) (p. 31 y p. 33).
- **Tamaño del reservorio:** el mejor fue el más pequeño, 50 neuronas, de entre 50 a 250 (p. 33).
- **Tasa de fuga (leaking rate):** no influyó significativamente; el autor la fija en 0 y lo interpreta como señal de que los estados de las neuronas son muy homogéneos (p. 33).
- **Radio espectral:** 0.5 fue lo mejor con una variable y 0.95 con varias (p. 33 y p. 38).
- **Tamaño de entrenamiento:** 10 días de trading fue el óptimo para los reservorios con elastic net; más o menos datos empeoraba (p. 34). La regresión lineal sí mejora con más datos.
- **Sin PCA el ESN no siempre supera a la regresión lineal.** El reservorio aumenta la dimensión (de 12 a 50) sin hacer las variables más informativas; el PCA es el que permite aprovecharlas (p. 42).
- **La inicialización de la matriz del reservorio es crítica:** una inicialización inapropiada puede volver el R² medio negativo; la matriz interna es la causa principal, más que la de entrada (p. 40 y p. 41).
- **Lasso falla con componentes principales:** descarta componentes correlacionados y tira información útil; con penalización cero resultó lo mejor (p. 39 y p. 40).
- **Colinealidad:** el factor de inflación de la varianza (VIF) de los desbalances de flujo de órdenes pasa de 10 desde el nivel 2; se descartaron las variables con VIF > 5 (Tabla 3.6, p. 38).

## Métodos y diseño experimental

- Objetivo: alfa = precio medio futuro menos precio medio actual, a k ticks (p. 12 y p. 29).
- Reservorios: ESN con realimentación y tasa de fuga (ecuación 2.3.1, p. 18); firma aleatorizada con proyección aleatoria de la firma truncada (ecuación 2.3.4, p. 21).
- Lectura: OLS, lasso, elastic net con validación cruzada (`RidgeCV`, `LassoCV`, `ElasticNetCV`) (p. 32).
- Evaluación: bootstrap de bloques móviles; ventanas de 5+1, 10+1 y 15+1 días (entrenamiento + prueba); se guarda el R² de cada paso (p. 32).
- Métrica principal: R² fuera de muestra por ventana.

## Limitaciones declaradas y críticas

- Declarado por el autor: el barrido de hiperparámetros del ESN fue pequeño y puede no ser el óptimo; faltan más variables (flujo de órdenes asimétrico) y una investigación sistemática de la diferencia ESN contra firma (p. 45).
- **[OPINIÓN]** Un solo par de divisas y un solo año; sin costes de transacción ni prueba de significancia estadística formal (solo distribuciones de R²); R² por debajo de 1 %.
- **[OPINIÓN]** Los reservorios sin PCA no son claramente mejores que el modelo lineal, así que el resultado depende más de la lectura que del reservorio.

## Conexión con mi tesis (red E20)

- **Es el antecedente más directo de la tesis en cuanto al diseño:** reservorio fijo con lectura lineal entrenada, comparado con un referente lineal simple, con validación por ventanas móviles.
- **Coincide con mi hallazgo de que la lectura manda:** en E20 la fuerza de regularización (C = 3e-5 frente a 1e-3) cambió el AUC de .573 a .607. Aquí la lectura penalizada y el PCA son los que hacen que el reservorio supere a OLS.
- **Coincide con el diagnóstico de dimensión:** E20 entrega 3001 columnas a la lectura; este trabajo explica que el reservorio expande la dimensión sin añadir información y que reducirla ayuda. Sugiere un experimento: lectura de E20 con PCA o con elastic net.
- **Pone en cuestión la recurrencia:** muestra que la matriz interna decide si el reservorio sirve; en E20 la recurrencia es 2.5 veces la entrada y apagarla no empeora (fase 2, BTC real).
- **Límite para citarlo:** es USD/MXN a escala de segundos; no sirve de evidencia sobre Bitcoin.

## Referencias que cita y conviene localizar

Jaeger (2001), reservorio de estado de eco; Maass, Natschläger y Markram (2002), máquinas de estado líquido; Verstraeten y otros (2007), comparación de métodos de reservorio; Maciel y otros (2014), tipo de cambio con ESN; Lin y otros (2009), S&P 500 con ESN; Kim y King (2020), ESN profundo; Cuchiero y otros (2021), firma aleatorizada; Compagnoni y otros (2022), capas de firma aleatorizada; Zou y Hastie (2005), elastic net; Kolm, Turiel y Westray (2021), desbalance de flujo de órdenes profundo. **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (datos, métodos, fundamentos matemáticos y tablas)

Este anexo recoge, de forma completa, el contenido técnico del PDF (49 páginas) que el resumen anterior solo menciona. Páginas = páginas del PDF. **Corrección importante al resumen anterior:** la métrica del trabajo es un **R² modificado respecto de un pronóstico igual a cero** (ver 3.8), de modo que un R² positivo significa "mejor que predecir alfa = 0". Los valores pequeños (por debajo de 1 %) son entonces valores respecto de ese referente, no respecto de la media.

## A1. Datos

- **Origen:** libro de órdenes y libro de operaciones del par USD/MXN, enero a diciembre de 2022, en una rejilla de tiempo irregular (por tick) (p. 28).
- **Tamaño:** unos 500 000 a 700 000 registros de libro de órdenes por día de negociación; tras unir ambos libros, **22 829 398** registros.
- **Libro de órdenes** (Tabla 3.1, p. 28): para cada nivel i = 0..9, `askRate_i`, `askQty_i`, `askCount_i`, `bidRate_i`, `bidQty_i`, `bidCount_i` (precio, cantidad y número de órdenes de oferta y demanda). **Libro de operaciones:** `price`, `side` (dada o pagada) y `time`.
- **Definiciones** (sección 2.1, p. 12 y p. 13): tasa de oferta (ask) y de demanda (bid); nivel 0 es el mejor y 9 el peor; spread_i = ask_i − bid_i; **tasa media** (precio medio) = (Bid_0 + Ask_0)/2; **alfa** de horizonte k: Alfa_t = Media_{t+k} − Media_t.
- **Preprocesamiento** (p. 29 y p. 30): el objetivo es el alfa futuro y las variables de entrada incluyen el alfa pasado; los valores faltantes se rellenan con el histórico y, si persisten, con cero; escalado mín-máx (ecuación 3.1.1: X_scaled = (X − min X)/(max X − min X)).
- **Variables multivariantes** (Tabla 3.2, p. 29): objetivo Return_future,t = (ask_{t+k} + bid_{t+k})·0,5 − (ask_t + bid_t)·0,5; entradas: Return_past,t con retardo Δt, **desbalance de flujo de órdenes (OFI_{i,t})**, **desbalance de cola (QI_{i,t})** y `traded − mid` (precio operado menos precio medio).
- **Desbalance de flujo de órdenes** (Kolm, Turiel y Westray, 2021): bOF_{i,t} = v^{i,b}_t si b^i_t > b^i_{t−1}; v^{i,b}_t − v^{i,b}_{t−1} si b^i_t = b^i_{t−1}; −v^{i,b}_t si b^i_t < b^i_{t−1}. aOF_{i,t} = −v^{i,a}_t si a^i_t > a^i_{t−1}; v^{i,a}_t − v^{i,a}_{t−1} si a^i_t = a^i_{t−1}; v^{i,a}_t si a^i_t < a^i_{t−1}. OFI_{i,t} = bOF_{i,t} − aOF_{i,t}.
- **Desbalance de cola** (Gould y Bonart, 2016): QI_{i,t} = (v^{i,b}_t − v^{i,a}_t)/(v^{i,b}_t + v^{i,a}_t).
- **`traded − mid`:** las operaciones se unen al libro de órdenes por tiempo, con tolerancia hacia un tiempo futuro; los huecos se rellenan con cero.
- **Variables escogidas por colinealidad** (Tabla 3.6, p. 38): el factor de inflación de la varianza (VIF) de los OFI crece con el nivel: OFI0 1,84; OFI1 6,00; OFI2 11,61; OFI3 16,40; OFI4 22,98; OFI5 31,35; OFI6 39,71; OFI7 46,98; OFI8 32,35; los QI y `traded−mid` están cerca de 1,00 a 1,02. Se descartan las variables con VIF > 5.

## A2. Diseño experimental

- **Horizontes (retardo, horizonte)** (p. 31): (50, 50), (100, 100) y (500, 500) ticks, que equivalen aproximadamente a **1 segundo, 1 minuto y 8 minutos**. Se elige (50, 50) porque cuanto más corto el horizonte, mejor el modelo.
- **Tamaños de entrenamiento y prueba** (Tabla 3.3, p. 31), en días de negociación: pequeño 5 + 1, mediano 10 + 1 y grande 15 + 1 (entrenamiento + prueba).
- **Hiperparámetros del reservorio** (p. 31): radio espectral ρ ∈ {0,95; 0,5; 0,2} (solo ESN); neuronas ∈ {50, 100, 150, 200} (el texto también cita 250); carreras de inicialización ∈ {100, 150, 200, 250}; tasa de fuga α ∈ {0; 0,2; 0,5; 0,8; 1}; método de regresión ∈ {lineal, lasso, elastic net}. Matriz de entrada dispersa uniforme con dispersión 0,7 (una variable) o 0,5 (varias); matriz de realimentación uniforme escalada a [−0,5; 0,5]; matriz interna dispersa uniforme entre −1 y 1, escalada por el radio espectral y ρ; estado inicial cero. Activación tanh en todos.
- **Regresión de la salida** (p. 32): `RidgeCV`, `LassoCV` y `ElasticNetCV` de scikit-learn con parámetros elegidos por validación cruzada.
- **Evaluación** (p. 32): **bootstrap de bloques móviles**: se desplaza una ventana de entrenamiento + prueba paso a paso (paso m = 1 día) a lo largo de todo el conjunto y se guarda el R² de cada ventana.
- **Elecciones finales** (p. 33 y p. 38): ρ = 0,5 con una variable y 0,95 con varias; 50 neuronas; α = 0 (la tasa de fuga no influye); 100 carreras de inicialización; entrenamiento de 10 días.

## A3. Fundamentos matemáticos

### A3.1 Regresión lineal por mínimos cuadrados (sección 2.2)
- Modelo: Y = X·W + ε, con W ∈ R^d y ε i.i.d. normal estándar, independiente de X.
- Error cuadrático: SE = (Y − Ŷ)ᵀ(Y − Ŷ) (2.2.2); su derivada ∂SE/∂W = 2·Xᵀ(Y − X·Ŵ) (2.2.3); solución Ŵ = (XᵀX)⁻¹·XᵀY (2.2.4) si XᵀX es invertible; predicción Ŷ_test = X_test·Ŵ (2.2.5).
- **VIF:** para cada variable x_i se regresa sobre las demás; VIF_i = 1/(1 − R_i²). Un VIF cercano a 1 indica poca colinealidad; entre 1 y 10, colinealidad débil; mayor que 10, fuerte.

### A3.2 Red neuronal recurrente y retropropagación en el tiempo (sección 2.3.1, p. 16 a 18)
- Estado: u_t = W_in,t·x_t + W_h,t·h_{t−1} + b_h; h_t = g(u_t) con g = tanh; v_t = W_out,t·h_t + b_o; y_t = f(v_t) con f = softmax, f(x_i) = e^{x_i}/Σ_j e^{x_j}.
- Pérdida: L = ½·Σ_{t=1}^{T} ‖y_t − d_t‖², con d_t el valor real. Descenso de gradiente: W_new = W − λ·∂L/∂W.
- Errores retropropagados: δ^y_t(j) = −∂L/∂v_t(j) = (d_t(j) − y_t(j))·f′(v_t(j)) y δ^h_t(j) = −∂L/∂u_t(j) = (Σ_i δ^y_t(i)·W_out,t(j,i) + Σ_i δ^h_{t+1}(i)·W_h,t(j,i))·g′(u_t(j)).
- Actualización: W_out ← W_out + λ·Σ_t δ^y_t·h_tᵀ; W_in ← W_in + λ·Σ_t δ^h_t·x_tᵀ; W_h ← W_h + λ·Σ_t δ^h_t·h_{t−1}ᵀ.

### A3.3 Red de estado de eco (sección 2.3.2, p. 18 a 20)
- Con entrada x ∈ R^{D×T}, estados s ∈ R^{N×T} y salida y ∈ R^{M×T}:
  s_t = (1 − α)·f(W_in·x_t + W_res·s_{t−1} + W_back·y_{t−1} + ε_t) + α·s_{t−1}  (2.3.1)
  y_t = W_out·[s_t ; x_t]
  donde α es la **tasa de fuga**, [s_t ; x_t] es la concatenación y f = tanh. Dimensiones: W_in ∈ R^{N×D}, W_res ∈ R^{N×N}, W_out ∈ R^{M×(N+D)}, W_back ∈ R^{N×M}.
- **Inicialización:** W_in con elementos de una uniforme en [−a, a], a ∈ [0, 1]; W_res = ρ(W_res) · W / max(λ(W)), con W una matriz dispersa uniforme y max(λ(W)) su radio espectral; solo W_out se entrena (regresión lineal, lasso, etc.).
- **Propiedad de eco:** el estado final no debe depender del estado inicial: ‖F̂(s_k, X_n) − F̂(s̃_k, X_n)‖ → 0 cuando k → ∞. Condición suficiente para un ESN con fuga: ρ(W) < 1 con W = (1 − α)·W_res + α·I. Esbozo: d(f(W_in x_t + W_res s_{t−1}), f(W_in x_t + W_res s̃_{t−1})) ≤ ‖W_res‖·d(s_{t−1}, s̃_{t−1}) ≤ ρ(W_res)·d(s_{t−1}, s̃_{t−1}), que converge si ρ(W_res) < 1.

### A3.4 Firma aleatorizada (sección 2.3.4, p. 20 y p. 21)
- Un **camino** X: [a, b] → R^d continuo, X_t = (X^1_t, …, X^d_t). La **firma** es la secuencia infinita S_{a,b}(X) = (1, S(X)^1, …, S(X)^d, S(X)^{1,1}, S(X)^{1,2}, …), cuyos elementos son integrales iteradas S^I_{a,b}(X) = ∫_{a<t_1<…<t_k<b} dX^{i_1}_{t_1} … dX^{i_k}_{t_k}, con I = (i_1, …, i_k). La **firma truncada de orden p** conserva los términos hasta el nivel p y su coste crece mucho.
- **Firma aleatorizada:** proyección aleatoria lineal de la firma truncada, que se usa como reservorio:
  s_0 = 0;  s_t = α·s_{t−1} + f(A_1·s_{t−1} + ε_1) + Σ_{i=1}^{d} f(A_2^i·s_{t−1} + ε_2^i)·x^i_t   (2.3.4)
  con A_1, A_2^i ∈ R^{k×k} matrices dispersas normales independientes, ε_1, ε_2^i ∈ R^k ruidos normales independientes, d la dimensión de las variables y f = tanh.

### A3.5 Métodos de regresión de la salida (sección 2.3.5, p. 21 a 23)
- **Cresta (ridge):** Ŵ = (XᵀX + λI)⁻¹·XᵀY; J(W) = ½(Y − XW)ᵀ(Y − XW) + λ·WᵀW, con restricción WᵀW ≤ r.
- **Lasso:** J(W) = ½(Y − XW)ᵀ(Y − XW) + λ·‖W‖₁, resuelto por descenso por coordenadas. Desventajas citadas: no selecciona bien si n ≈ d; con efecto de grupo elige una sola variable entre las parecidas; con colinealidad puede ser dominado por cresta.
- **Elastic net:** J(W) = ½(Y − XW)ᵀ(Y − XW) + λ_1·‖W‖₁ + λ_2·‖W‖₂² (versión ingenua), y la versión calibrada J(W) = Wᵀ·((XᵀX + λ_2 I)/(1 + λ_2))·W − 2·YᵀXW + λ_1·‖W‖₁; λ_1 y λ_2 por validación cruzada.

### A3.6 Descomposición en valores singulares y análisis de componentes principales (sección 2.3.6, p. 23 a 25)
- **SVD:** toda matriz A ∈ R^{m×n} se descompone como A = Uᵀ·Λ·V, con U y V ortogonales y Λ diagonal con los valores singulares σ_i = sqrt(λ_i) en orden decreciente.
- **PCA:** dada X ∈ R^{m×n} (m dimensión, n número de datos) con matriz de covarianza Σ, se buscan k < m combinaciones lineales Z_i = α_iᵀ·X con (i) α_iᵀα_i = 1, (ii) α_iᵀ Σ α_j = 0 para j < i (sin información repetida) y (iii) Var(Z_i) máxima. Con el multiplicador de Lagrange φ(α_i) = Var(α_iᵀX) − λ(α_iᵀα_i − 1) resulta (Σ − λI)·α_i = 0, es decir, α_i son los autovectores de Σ. Procedimiento: centrar X; calcular Σ; SVD; ordenar los autovalores en orden decreciente y quedarse con los k primeros autovectores (matriz P ∈ R^{k×m}); el nuevo conjunto es P·X. **Tasa de contribución** del componente i: λ_i/Σ_j λ_j; se elige k para que la contribución acumulada alcance un umbral razonable.
- **RC con PCA:** el PCA se aplica a los estados del reservorio una vez actualizados todos, antes de la regresión (Figura 2.8, p. 25); la dimensión objetivo se fija manualmente.

### A3.7 Métrica de evaluación (sección 2.4, p. 26 y p. 27)
- **R² modificado respecto de cero:** R² = 1 − Σ_i (y_i − ŷ_i)² / Σ_i (y_i − 0)²  (2.4.1), con y_i el alfa real e ŷ_i el predicho. Se justifica porque el mercado es casi impredecible y se asume que el alfa medio de un mercado de referencia es 0. **R² > 0 significa mejor que pronosticar cero.**
- **Estadísticos de la serie de R²** sobre las ventanas: media R̄² = (1/n)·Σ R²_i; varianza var(R²) = Σ (R²_i − R̄²)²/n; asimetría de Fisher-Pearson E[(R² − R̄²)³]/(E[(R² − R̄²)²])^{3/2}; curtosis E[(R² − R̄²)⁴]/(E[(R² − R̄²)²])² (referencia: 3 para la normal).

## A4. Resultados completos (valores en % de R²)

**Una variable, efecto del tamaño de entrenamiento** (Tabla 3.4, p. 32):

| Modelo (entrenamiento, prueba) | Media | Varianza | Asimetría | Curtosis | R² > 0 (%) |
|---|---|---|---|---|---|
| Regresión lineal (5,1) | −0,26802 | 0,91996 | −2,0511 | 10,8830 | 41,18 |
| Firma aleatorizada + elastic net (5,1) | 0,01122 | 0,03909 | 10,80684 | 140,8782 | 47,06 |
| ESN + elastic net (5,1) | 0,00378 | 0,03944 | 10,3858 | 133,5544 | 43,14 |
| Regresión lineal (10,1) | −0,14091 | 0,39815 | −1,5217 | 7,3696 | 43,2 |
| Firma aleatorizada + elastic net (10,1) | 0,02213 | 0,05634 | 10,5949 | 133,2179 | 46,4 |
| ESN + elastic net (10,1) | 0,01405 | 0,05632 | 10,6086 | 135,0786 | 42,4 |
| Regresión lineal (15,1) | −0,07193 | 0,31445 | −2,6091 | 20,1699 | 44,08 |
| Firma aleatorizada + elastic net (15,1) | 0,01337 | 0,02568 | 7,3139 | 82,9464 | 47,76 |
| ESN + elastic net (15,1) | 0,00458 | 0,02663 | 6,9764 | 78,7622 | 38,78 |

**Una variable, efecto del método** (Tabla 3.5, p. 35, entrenamiento de 10 días): regresión lineal −0,14091 (43,2 % positivos); ESN con elastic net 0,01405 (42,4 %); firma con elastic net 0,02213 (46,4 %); **ESN con elastic net y PCA 0,03280 (54,8 %)**; **firma con elastic net y PCA 0,03227 (55,6 %)**.

**Varias variables, regresión por método** (Tabla 3.8, p. 39), R² medio de la regresión sola en el conjunto de varias variables: lasso 0,33545 / 0,20030 / 0,13328; OLS 0,71410 / 0,78418 / 0,81244; elastic net 0,87883 / 0,92941 / 0,92128 (entrenamiento de 5, 10 y 15 días).

**Varias variables, modelos completos** (Tabla 3.7, p. 41), R² medio (%), % de R² > 0:
- Entrenamiento 5: lineal 0,71410 (90,98); ESN+OLS 0,60810 (87,45); ESN+EN 0,67637 (92,94); ESN+OLS+PCA 0,85357 (92,16); ESN+lasso+PCA 0,33450 (86,27); **ESN+EN+PCA 0,90639 (96,86)**; firma+OLS 0,80240; firma+EN 0,85560 (96,47); firma+OLS+PCA 0,84576; firma+EN+PCA 0,90042 (96,47).
- Entrenamiento 10: lineal 0,78418 (92,4); ESN+OLS 0,78306; ESN+EN 0,81238 (96,4); ESN+OLS+PCA 0,91919; ESN+lasso+PCA 0,20022 (76); **ESN+EN+PCA 0,94302 (97,6)**; firma+OLS 0,89587; firma+EN 0,91848 (98); firma+OLS+PCA 0,91342; firma+EN+PCA 0,93697 (98).
- Entrenamiento 15: lineal 0,81244 (90,20); ESN+OLS 0,77822; ESN+EN 0,82366 (97,96); ESN+OLS+PCA 0,881253; ESN+lasso+PCA 0,133257 (71,43); **ESN+EN+PCA 0,92634 (98,78)**; firma+OLS 0,86576; firma+EN 0,91098; firma+OLS+PCA 0,87707; firma+EN+PCA 0,92247 (98,78).

**Fuente del poder de los reservorios** (Tabla 3.9, p. 41), entrenamiento de 5 días, R² medio (%): ESN+PCA+OLS original con |λ_max| > 1: 0,85357 (92,16 % positivos); ESN+PCA+EN original: 0,90639 (96,86); matriz interna uniforme estándar con |λ_max| > 1: OLS −0,37136 y EN −0,27034; con |λ_max| ≈ 0,86: OLS −0,05076 y EN 0,00581; y con entrada identidad: OLS −0,02075 y EN 0,031469. La inicialización de la matriz interna puede volver negativo el R² medio por sobreajuste (Figura 3.4).

**Firma aleatorizada con tanh en la entrada** (Tabla 3.10, p. 43): entrenamiento 5: OLS −0,03099 (86,67 %), EN 0,02201 (89,41 %); entrenamiento 10: OLS 0,91525 (92,4 %), EN 0,82485 (94 %); entrenamiento 15: OLS 0,88068 (91,84 %), EN 0,92601 (98,78 %). Con la variante s_t = f(A_1 s_{t−1} + ε_1) + Σ f(A_2^i s_{t−1} + ε_2^i)·f(x^i_t) (3.3.1, α = 0) la estabilidad se parece a la del ESN mal inicializado en conjuntos pequeños.

## A5. Conclusiones técnicas del trabajo (p. 42 a 46)

- La estructura de los reservorios sin PCA no basta: el PCA reduce la dimensión (de 12 a 50 variables internas) y concentra la información útil.
- Elastic net supera a OLS y a lasso para leer los estados; lasso con PCA falla por el efecto de grupo.
- El ESN con PCA y elastic net da el mayor R² medio, pero depende de una inicialización cuidadosa; la firma aleatorizada es más robusta y exige menos ajuste.
- Mejoras propuestas (p. 45): búsqueda de hiperparámetros más amplia, variables asimétricas de flujo de órdenes, estudio sistemático de la diferencia ESN contra firma, realimentación en la firma y mecanismos de atención.

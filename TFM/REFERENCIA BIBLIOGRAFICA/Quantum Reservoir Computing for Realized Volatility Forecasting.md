# Quantum Reservoir Computing for Realized Volatility Forecasting

**Extracción de conocimiento: 2026-10-02** (leídas las páginas 1 a 17 de 24; el resto son referencias y apéndices de computación cuántica)

| Campo | Valor |
|---|---|
| Título exacto | Quantum Reservoir Computing for Realized Volatility Forecasting |
| Autores | Qingyu Li, Chiranjib Mukhopadhyay, Abolfazl Bayat (Universidad de Ciencia y Tecnología Electrónica de China) y Ali Habibnia (Virginia Tech, Estados Unidos) |
| Tipo / Venue / Año | Preprint, arXiv:2505.13933v2 (2025) |
| Archivo local | `2505.13933v2.pdf` |
| URL / DOI | arXiv:2505.13933 (sin DOI de revista en el documento) |
| Métodos | Reservorio cuántico de 10 qubits con hamiltoniano de Ising de campo transversal totalmente conectado, con qubits de entrada y qubits de memoria; lectura por regresión de cresta; selección de variables por avance (forward selection) y valores de Shapley |
| Datos | Volatilidad realizada mensual del S&P 500 de enero de 1950 a diciembre de 2017, alineada con el conjunto de Bucci (2020), más variables macroeconómicas y financieras (inflación, producción industrial, rendimiento del mercado, diferencial de crédito, etc.) (p. 9) |

## Aporte clave

Propone un reservorio **cuántico simulado** para pronosticar la volatilidad realizada mensual y lo compara con modelos econométricos (AR, ARMAX, HAR) y de aprendizaje automático (LSTM y reservorio clásico). Concluye que el reservorio cuántico mejora a la mayoría de los modelos a un paso, pero **el propio texto no afirma ventaja cuántica** y a cinco pasos el mejor es el reservorio clásico (p. 15, p. 16).

## Hallazgos cuantitativos (HECHO, con página)

- **Diseño de la evaluación:** ventana móvil con reestimación mensual; ventana inicial de febrero de 1950 a junio de 1997 (571 meses); 245 predicciones fuera de muestra desde agosto de 1997 hasta diciembre de 2017; horizonte de 1 paso (S=1) y 5 pasos (S=5, con retroalimentación de las predicciones) (p. 10 y p. 11).
- **Un paso adelante** (Tabla II, p. 16), pérdida MSE: HAR 0,1476; HARX 0,1508; AR3 0,1178; ARMAX 0,1145; LSTM 0,1295; LSTMX 0,1185; reservorio clásico RC 0,1441; RCX 0,1089; reservorio cuántico QR1 0,105; QR2 0,103. QR2 obtiene el valor p de 1,0 en el conjunto de confianza de modelos (MCS) y entran también QR1, RCX, LSTMX y ARMAX.
- **Cinco pasos adelante** (Tabla II, p. 16): el mejor por MSE es el **reservorio clásico RC (0,1528)**, con valor p MCS = 1,0; el QR1 da 0,1556 y el QR2 0,1663. Casi todos los modelos quedan dentro del conjunto de confianza (solo el HARX queda fuera).
- **Prueba de Diebold y Mariano** (Tabla III, p. 17): QR1 y QR2 superan con claridad a HAR, HARX y RC (valores p ≈ 0 a 0,01 contra el RC), pero **frente al reservorio clásico con variables (RCX) no hay diferencia significativa** (valores p 0,296 y 0,291) ni entre QR1 y QR2 (p = 0,771, p. 15).
- **Selección de variables:** el óptimo son 7 variables de entrada; con más, quedan menos qubits ocultos y el reservorio pierde memoria (p. 12).
- **Configuración del reservorio clásico:** 50 neuronas (RC) y 20 (RCX), tasa de fuga 0,6, entrenado con regresión (p. 10).
- **Los datos recientes importan más que los antiguos** en la contribución de cada retardo (valores de Shapley, p. 13).
- **MSE no distingue sobreestimar de subestimar;** por eso se usa también QLIKE, que penaliza más la subestimación de la volatilidad (p. 13).

## Limitaciones y críticas

- Declarado por los autores: el hardware cuántico actual es limitado (pocos qubits, ruido, conectividad); no se afirma ventaja cuántica sobre el ML clásico en datos clásicos (p. 16). En una ejecución real harían falta muchas repeticiones de medida y los resultados pueden concentrarse exponencialmente (p. 8).
- **[OPINIÓN]** El resumen dice que el enfoque "supera de forma consistente" a los modelos de referencia, pero **a cinco pasos el mejor es el reservorio clásico** y a un paso la diferencia con el reservorio clásico con variables (RCX) no es significativa. La afirmación del resumen es más fuerte que la evidencia de las tablas.
- **[OPINIÓN]** Los resultados son una simulación sin ruido de hardware, con un solo activo (S&P 500), datos mensuales y 245 observaciones de prueba.
- **[OPINIÓN]** No es Bitcoin ni predicción de dirección: es volatilidad mensual de un índice de acciones.

## Conexión con mi tesis (red E20)

- **Estructura análoga a E20:** reservorio fijo con lectura lineal de cresta, comparado con HAR, LSTM y un reservorio clásico, usando reestimación periódica. Respalda ese diseño de comparación.
- **Reservorio clásico pequeño competitivo:** un reservorio de solo 20 a 50 neuronas rinde cerca de los mejores; coincide con mi hallazgo de que tamaños mayores no mejoran.
- **Memoria frente a entradas:** el compromiso entre número de variables y memoria interna (qubits ocultos) es una versión cuántica de lo que pasa en E20, donde la señal de entrada compite con la recurrencia.
- **Herramientas estadísticas:** conjunto de confianza de modelos, pérdida QLIKE y prueba de Diebold y Mariano son opciones concretas para mi capítulo de metodología.
- **Cuidado al citarlo:** servirá como ejemplo de cómo un resumen puede exagerar frente a las tablas; no debe citarse como evidencia de ventaja de los reservorios en Bitcoin.

## Referencias que cita y conviene localizar

Corsi (2009), HAR; Bucci (2020), "Realized volatility forecasting with neural networks"; Andersen y Bollerslev (1998 y 2003), volatilidad realizada; Patton (2011), QLIKE; Hansen, Lunde y Nason (2011), conjunto de confianza de modelos; Diebold y Mariano (1995); Fujii y Nakajima (2017), reservorios cuánticos con espines desordenados; Christensen, Siggaard y Veliyev (2023); Zhang, Zhang, Cucuringu y Qian (2023). **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (datos, métodos, fundamentos matemáticos y tablas)

Contenido técnico de las páginas 1 a 24 del PDF (la bibliografía de las páginas 17 a 20 solo se lista en el resumen). Páginas = páginas del PDF. **Corrección importante al resumen anterior:** las páginas 10 y 24 indican que, para el reservorio cuántico, **se entrenan 100 instancias distintas y se reporta la de mejor rendimiento**, y que el LSTM y el reservorio clásico se eligen también por su mejor tamaño oculto (10 a 200 unidades); la selección sobre el mismo rendimiento reportado favorece a los modelos con más configuraciones probadas (sesgo de selección), y debe leerse junto con la prueba de Diebold y Mariano.

## A1. Datos (p. 8 y p. 9)

- **Objetivo:** volatilidad realizada mensual del **S&P 500**, de **febrero de 1950 a diciembre de 2017**, **815 datos** (Yahoo Finance con la biblioteca `yfinance`); se sigue a Bucci (2020) para poder comparar de forma justa.
- **Definición:** RV_t = sqrt( Σ_{i=1}^{N_t} r²_{i,t} ) y se modela log(RV_t)  (ecuación 1), con r_{i,t} el retorno del día i dentro del mes t.
- **Variables macroeconómicas y financieras** (Tabla I): volatilidad realizada RV (y promedios trimestral RVq y anual RVa); razón dividendo/precio (DP); razón beneficio/precio (EP); exceso de retorno del mercado (MKT, factor de Fama y French); factor de valor (HML); factor de tamaño (SMB); factor de reversión de corto plazo (STR); tasa de letras del Tesoro a 3 meses (TB); inflación mensual (INF); diferencial de crédito (DEF); crecimiento mensual de la producción industrial (IP).
- **Escalado:** todas las variables se escalan a [−π, +π] para cumplir el requisito de la puerta de rotación RY (p. 6).

## A2. Fundamentos matemáticos

### A2.1 Modelos clásicos de referencia (sección II A, p. 3 y p. 4)
- **HAR** (Corsi): RV_t = β_0 + β_d·RV^{(d)}_{t−1} + β_w·RV^{(w)}_{t−1} + β_m·RV^{(m)}_{t−1} + ε_t  (ecuación 2), con los promedios diario, semanal y mensual de la RV y E[ε_t | F_{t−1}] = 0, Var(ε_t | F_{t−1}) = σ_t². Variantes: HARX (con exógenas), AR(1), AR(3) y ARMAX.
- **Red recurrente con compuertas (LSTM)** (p. 4 y p. 5): estados de celda c_t y oculto h_t con compuertas de olvido, entrada y salida; h_t = o_t ⊙ tanh(c_t)  (ecuación 10); la salida es ŷ_t = g(h_t). Entrenamiento por minimización de L = (1/n)·Σ (y_i − ŷ_i)²  (ecuación 5).
- **Red de propagación hacia adelante:** h_l = F(W_l·h_{l−1} + b_l) con h_0 = x y h_L = ŷ  (ecuación 4).
- **Reservorio clásico** (p. 6): h_t = (1 − α)·h_{t−1} + F(W_r·h_{t−1} + W_in·x_t + b);  y_t = W_out·h_t  (ecuación 11), con α la tasa de fuga; solo W_out se entrena (regresión lineal).

### A2.2 Reservorio cuántico (sección III, p. 6 a 8)
- **Hamiltoniano** de Ising de campo transversal totalmente conectado: H = Σ_{i,j} J_{ij}·X_i X_j + v·Σ_i Z_i  (ecuación 12), con X_i y Z_i los operadores de Pauli del qubit i, v la intensidad del campo magnético (v = 1, unidad de energía) y J_{ij}/v muestreados al azar uniformemente en [0, 1]. Una vez muestreado, H queda fijo (como un reservorio clásico).
- **Subsistemas:** n_1 **qubits de entrada** (estado ρ_I) para codificar las variables y n_2 **qubits ocultos** (estado ρ_h) que guardan el pasado; n_1 + n_2 = 10. Estado inicial: ρ_I ⊗ ρ_h = |0⟩⟨0|^{⊗n_1} ⊗ |0⟩⟨0|^{⊗n_2}  (ecuación 13).
- **Memoria:** se pronostica RV_t con k = 3 pasos pasados {x_{t−3}, x_{t−2}, x_{t−1}}; cada x_{t−k} = [x_{t−k,1}, …, x_{t−k,n_1}]ᵀ.
- **Codificación por fase** (paso I): |ψ_I(x_{t−3})⟩ = R_Y(x_{t−3})·|0⟩^{⊗n_1}, con R_Y(x) = ⊗_{j=1}^{n_1} e^{−i·x_j·Y_j/2}  (ecuación 14). ρ_I(x) = |ψ_I(x)⟩⟨ψ_I(x)|.
- **Evolución:** U = e^{−iHτ} con τ = 1/v, suficiente para que la información se disperse por todo el sistema.
- **Actualización del estado oculto** tras descartar los qubits de entrada por traza parcial: ρ_h(t − 2) = Tr_I[ U(τ)·( ρ_I(x_{t−3}) ⊗ ρ_h(t − 3) )·U†(τ) ]  (ecuación 16). Se repite con x_{t−2} (ecuaciones 17 y 18) y con x_{t−1} (ecuación 19), y en el último paso no se descarta ningún qubit.
- **Lectura:** se mide la componente Z de todos los qubits: ⟨Z_j⟩_τ = Tr[ U(τ)·( ρ_I(x_{t−1}) ⊗ ρ_h(t − 1) )·U†(τ)·Z_j ]  (ecuación 20); el vector de medidas es m^{(1)}_t = [⟨Z_1⟩_τ, …, ⟨Z_{n_1+n_2}⟩_τ]ᵀ.
- **Regresión de salida:** RV̂_t = W_out·m^{(1)}_t  (21); con pérdida MSE = (1/T)·Σ (RV_t − RV̂_t)²  (22); solución de cresta W_out = RVᵀ·M_1ᵀ·( M_1·M_1ᵀ + δ·I )⁻¹  (23), con M_1 = [… m^{(1)}_t …] y **δ = 10⁻⁸**. Este modelo es **QR1**.
- **Conjunto (ensemble) QR2** (Figura 3): un segundo reservorio casi idéntico en el que el último paso de evolución dura τ/2; el vector de lectura es m^{(2)}_t = [⟨Z_1⟩_τ, …, ⟨Z_{n_1+n_2}⟩_τ, ⟨Z_1⟩_{τ/2}, …, ⟨Z_{n_1+n_2}⟩_{τ/2}]ᵀ, con el doble de recursos.
- **Simulación frente a hardware real:** en la simulación se calculan directamente las esperanzas; en un experimento real harían falta muchas repeticiones de medida ("shots"). Se advierte (Xiong y otros, 2025) que en sistemas grandes los resultados pueden concentrarse exponencialmente en un valor independiente de la entrada; aquí el tamaño fijo de 10 qubits lo evita (Apéndice C, Figura 9: la varianza de las esperanzas medidas entre qubits es suficientemente grande).

### A2.3 Notación cuántica de los apéndices (p. 21 a 23)
- **Qubit:** |ψ⟩ = α|0⟩ + β|1⟩ con |α|² + |β|² = 1 (α, β complejos); |0⟩ = [1, 0]ᵀ y |1⟩ = [0, 1]ᵀ.
- **Composición:** el estado de varios qubits es el producto tensorial; un sistema de n qubits vive en un espacio complejo de dimensión 2ⁿ; hay entrelazamiento cuando el estado conjunto no se puede escribir como producto de los subsistemas, p. ej. |ψ⟩_AB = α|0⟩_A|0⟩_B + β|1⟩_A|1⟩_B.
- **Matriz de densidad:** ρ = |ψ⟩⟨ψ| para un estado puro y ρ = Σ_i p_i |ψ_i⟩⟨ψ_i| para un conjunto de estados.
- **Matrices de Pauli:** X = [[0, 1], [1, 0]], Y = [[0, −i], [i, 0]], Z = [[1, 0], [0, −1]].
- **Evolución unitaria:** U(t) = e^{−iHt}; |ψ(t)⟩ = U(t)|ψ(0)⟩ (A11); ρ(t) = U(t)·ρ(0)·U†(t) (A12).
- **Medición:** regla de Born p_m = ⟨ψ|M_m† M_m|ψ⟩ con Σ_m M_m† M_m = I (A13); un observable A = Σ_m a_m |a_m⟩⟨a_m| (A14) y su valor esperado ⟨A⟩ = ⟨ψ|A|ψ⟩ (A15).

## A3. Procedimiento de entrenamiento y evaluación (p. 9 a 11, p. 24)

- **Modelos comparados:** AR1, AR3, ARMAX, HAR, HARX, LSTM, LSTMX, RC, RCX (con "X" = con variables exógenas), QR1 y QR2.
- **Ventana móvil con reestimación mensual:** ventana inicial de febrero de 1950 a junio de 1997 (≈ 571 meses); primer pronóstico para agosto de 1997; después la ventana avanza un mes cada vez y todos los modelos se reestiman en cada paso, hasta diciembre de 2017: **245 pronósticos fuera de muestra**.
- **Horizontes:** un paso (S = 1, bucle abierto: las entradas son valores reales) y cinco pasos (S = 5, bucle cerrado: las predicciones se realimentan como entrada).
- **Hiperparámetros:** LSTM de dos capas, Adam, tasa de aprendizaje 0,001, 100 épocas, lote 64; tamaño oculto entre 10 y 200 de 10 en 10, con mejor valor **60 (LSTM)** y **50 (LSTMX)** (Figura 10 derecha). Reservorio clásico: tasa de fuga 0,6, radio espectral 0,9, escala de entrada 0,1, lectura por regresión de cresta; neuronas entre 10 y 200 de 10 en 10, con mejor valor **50 (RC)** y **20 (RCX)** (Figura 10 izquierda). Los hiperparámetros se eligen con validación cruzada que respeta el orden temporal dentro de la ventana de entrenamiento.
- **Reservorio cuántico:** 10 qubits y 3 capas (retardos t−1, t−2 y t−3); **100 instancias de reservorio, cada una entrenada y evaluada por separado, y se reporta la de mejor rendimiento** (p. 10).
- **Selección de variables para el reservorio cuántico** (sección IV D, p. 11 y p. 12): método de envoltura (wrapper) con **selección hacia adelante**: se parte de un conjunto vacío y en cada iteración se añade la variable que reduce más el MSE hasta un máximo de 10. Resultado: F*_QR1 = {RV, MKT, DP, IP, RVq, STR, DEF} y F*_QR2 = {RV, MKT, STR, RVq, EP, INF, DEF}: **n_1 = 7 qubits de entrada y n_2 = 3 ocultos**. Con más variables el rendimiento empeora porque quedan menos qubits ocultos y se pierde memoria (Figuras 6 y 7).
- **Interpretabilidad** (p. 12 y p. 13): valores de **Shapley** (Shapley 1953; Lundberg y Lee 2017) con tres análisis: por variable y retardo, agregado por retardo y por retardo temporal; los retardos más recientes aportan más.
- **Métricas** (p. 13): MSE y **QLIKE** = (1/T)·Σ_t [ log( RV̂²_t ) + ( RV_t / RV̂_t )² ] (penaliza más la subestimación); pruebas de **Diebold y Mariano** con estadístico basado en el promedio del diferencial de pérdidas d̄ y su varianza de Newey y West (robusta a autocorrelación y heterocedasticidad); y **conjunto de confianza de modelos** (MCS, Hansen, Lunde y Nason 2011).

## A4. Resultados completos

**Tabla II (p. 16), un paso (S = 1, muestra completa 1997-08 a 2017-12), pérdida MSE / QLIKE / valor p MCS de MSE / valor p MCS de QLIKE** (los valores de las columnas "Loss" y "P_MCS" se leen en el PDF como filas consecutivas; se citan los principales):

| Modelo | MSE | QLIKE | valor p MCS MSE | valor p MCS QLIKE |
|---|---|---|---|---|
| HAR | 0,1476 | 2,0431 | 0,0004 | 0,0008 |
| HARX | 0,1508 | 2,2436 | 0,0004 | 0,0008 |
| AR1 | 0,1304 | 1,7279 | 0,0065 | 0,0050 |
| AR3 | 0,1178 | 1,5893 | 0,0936 | 0,0861 |
| ARMAX | 0,1145 | 1,6196 | 0,4406* | 0,4355* |
| LSTM | 0,1295 | 1,7909 | 0,0221 | 0,0188 |
| LSTMX | 0,1185 | 1,7571 | 0,4406* | 0,4355* |
| RC | 0,1441 | 2,1011 | 0,0084 | 0,0061 |
| RCX | 0,1089 | 1,6480 | 0,6086* | 0,6106* |
| **QR1** | 0,105 | 1,4427 | 0,7603* | 0,7510* |
| **QR2** | **0,103** | **1,4004** | **1,0000*** | **1,0000*** |

(Un asterisco indica pertenencia al conjunto de confianza.) **Cinco pasos (S = 5, 1998-01 a 2017-12):** HAR 0,2143 (p 0,1291*); HARX 0,2934 (p 0,0044); AR1 0,2642 (0,0938*); AR3 0,2134 (0,1302*); ARMAX 0,2134 (0,1302*); LSTM 0,1831 (0,1291*); LSTMX 0,2200 (0,0925*); **RC 0,1528 (p 1,0000*)**; RCX 0,1667 (0,6333*); QR1 0,1556 (0,7642*); QR2 0,1663 (0,6333*).

**Tabla III (p. 17), prueba de Diebold y Mariano** (valores p en el triángulo superior y estadísticos en el inferior): QR1 y QR2 superan con claridad a HAR, HARX y RC (valores p de 0 a 0,01 frente a RC); frente a **RCX** los valores p son **0,296 (QR1) y 0,291 (QR2)** (sin diferencia significativa); entre QR1 y QR2 el valor p es 0,771; frente a AR3 los valores p son 0,014 (QR2) y 0,036 (QR1); frente a ARMAX, 0,111 y 0,120; frente a LSTMX, 0,09 (QR2) y 0,114 (QR1).

**Conclusión de los autores** (p. 15 y p. 16): el reservorio cuántico supera a los modelos clásicos en las métricas con un paso, con QR2 el mejor, "aunque no se afirma ventaja cuántica general"; la mejora de añadir variables exógenas depende del modelo (HARX peor que HAR); el reservorio clásico es el mejor a cinco pasos. Dificultades pendientes: el hardware cuántico actual (pocos qubits, ruido, conectividad, coherencia limitada, lectura imperfecta) y la corrección de errores, que probablemente tarde una década.

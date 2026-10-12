# Análisis comparativo de redes neuronales profundas para la predicción del precio de mercado de Bitcoin

**Extracción de conocimiento: 2026-10-02** (leído el texto completo de las 16 páginas)

| Campo | Valor |
|---|---|
| Título exacto | Análisis comparativo de redes neuronales profundas para la predicción del precio de mercado de Bitcoin |
| Autor | Aarón López-García (Centro Universitario EDEM, Valencia, España) |
| Tipo / Venue / Año | Artículo de revista: Revista Electrónica de Comunicaciones y Trabajos de ASEPUMA (Rect@), volumen 24 (2023), páginas 1 a 16; recibido el 24/05/2023, aceptado el 25/07/2023 |
| Archivo local | `Recta.Vol24.N1.01.pdf` |
| URL / DOI | https://doi.org/10.24309/recta.2023.24.1.01 |
| Métodos | Redes neuronales de propagación hacia adelante (FFNN), convolucionales (CNN) y LSTM con un número parecido de parámetros (2 081, 2 231 y 2 165), frente a NeuralProphet con ajustes por defecto como "marco de partida"; Adam y error cuadrático medio |
| Datos | Cierre diario de Bitcoin de Yahoo Finance del 1 de enero de 2017 al 1 de mayo de 2023; normalización mín-máx de [777,75; 67 566,82] a [0, 1]; secuencias de 30 días; partición 75 % entrenamiento, 15 % validación y 10 % prueba final (p. 8 y p. 9) |

## Aporte clave

Compara tres redes profundas con el mismo presupuesto de parámetros para predecir el **precio de cierre** del día siguiente y concluye que "los patrones temporales son más representativos que los espaciales": el LSTM da el mejor ajuste, seguido de la CNN y luego la FFNN, y todos superan a NeuralProphet (p. 1, p. 10 y p. 11).

## Hallazgos cuantitativos (HECHO, con página)

- **Arquitecturas** (Tabla 1, p. 9): FFNN con dos capas densas de 32 neuronas y una de salida; CNN con una convolución 1D, agrupación máxima y densa; LSTM con capas de 20 y 4 unidades y densa de salida.
- **Métricas usadas** (p. 9 y p. 10): MAE, RMSE, error absoluto mediano (MedAE), MAPE, SMAPE y **precisión direccional (DA)**, definida como la coincidencia del signo de (y_{i+1} − y_i) con el de (ŷ_{i+1} − ŷ_i) (ecuación 5).
- **Resultados en la prueba** (Tabla 2, p. 10): FFNN con MAE 519,01, RMSE 778,10, MAPE 2,40 %, SMAPE 1,20 % y DA 94,37 %; CNN con MAE 476,81, RMSE 721,57, MAPE 2,22 %, SMAPE 1,11 % y DA 94,80 %. Del LSTM el texto dice MAE por debajo de 400 dólares, SMAPE por debajo de 1 % y DA mayor de 97 %; de NeuralProphet, MAE superior a 600, MAPE de 3,12 % y DA mayor de 90 %. (En el PDF extraído, las filas de LSTM y NeuralProphet de la Tabla 2 quedaron cortadas; las cifras de esas dos filas se toman de la descripción en el texto, p. 10.)
- **Conclusión del autor** (p. 11): el LSTM es el más efectivo; la CNN también da buenos resultados; la FFNN y NeuralProphet "no son capaces de extraer patrones". Propone como trabajo futuro LSTM con optimización de hiperparámetros y series múltiples con variables exógenas.

## Verificación propia: el referente que falta (EJECUCIÓN PROPIA, 2026-10-02)

El artículo no compara con el método ingenuo (precio de ayer). Con la serie diaria de BTC del proyecto (CryptoCompare, no Yahoo), tomando el último 10 % de las secuencias de 30 días (228 días, del 16 de septiembre de 2022 al 1 de mayo de 2023), el método ingenuo da:

| Métrica | Ingenuo (cálculo propio) | FFNN | CNN | LSTM (texto) |
|---|---|---|---|---|
| MAE (USD) | **390,7** | 519,01 | 476,81 | < 400 |
| RMSE (USD) | 592,1 | 778,10 | 721,57 | no dado |
| MAPE | 1,79 % | 2,40 % | 2,22 % | no dado |
| SMAPE | 0,90 % | 1,20 % | 1,11 % | < 1 % |
| DA (definición del artículo) | **44,9 %** | 94,37 % | 94,80 % | > 97 % |

Conclusión indicativa: **ninguna de las redes mejora al método ingenuo** en error; el LSTM queda en el nivel del ingenuo. Y la **precisión direccional de 94 a 97 % es incompatible con el 44,9 % que da el ingenuo** bajo esa misma definición: una DA tan alta no se alcanza prediciendo el siguiente cambio; apunta a un desfase en el alineamiento entre predicciones y valores reales o a una definición de DA que mide algo distinto de la dirección del siguiente retorno (por ejemplo, compara las predicciones con el cambio del día en que ya se conoce el precio). Limitaciones de esta verificación: la fuente de precios y la extensión exacta de la prueba son aproximadas; el ingenuo no es una réplica exacta de la partición del autor.

## Limitaciones y críticas

- Declarado por el autor: solo la serie de cierre (un único regresor), sin hiperparámetros optimizados (p. 8 y p. 11).
- **[OPINIÓN]** **No hay referente ingenuo ni intervalos de confianza ni semillas repetidas**; se presenta un solo resultado por red.
- **[OPINIÓN]** **La métrica DA está mal definida o mal implementada** para evaluar la dirección: compara el signo de las diferencias entre predicciones consecutivas con el de las diferencias entre valores reales consecutivos, lo que no equivale a acertar si mañana sube o baja a partir de información de hoy. Con el método ingenuo da 44,9 %, no 94 %.
- **[OPINIÓN]** La conclusión "patrones temporales frente a espaciales" no se desprende del experimento: se comparan tres arquitecturas con una sola serie y una partición, y no hay ablación que aísle el efecto temporal.
- **[OPINIÓN]** El MAE de 400 a 500 dólares es del orden del cambio diario típico (el ingenuo da 391); los porcentajes de error de 1 a 2 % son triviales para una serie persistente.
- **[OPINIÓN]** Los modelos de comparación (NeuralProphet con ajustes por defecto) son un referente débil.

## Conexión con mi tesis (red E20)

- **Es otro ejemplo del error metodológico dominante** descrito por Baquero (2026): niveles de precio, sin referente ingenuo y con una "precisión direccional" muy alta que no se sostiene. Me sirve de caso para el capítulo de metodología, junto con mi comprobación del ingenuo.
- **Contraste con mi protocolo:** mido la dirección y el movimiento del siguiente periodo con información disponible solo hasta el instante de predicción, y comparo con la media móvil y la proporción de subidas.
- **Referencia en español de una revista indexada de ASEPUMA** para el estado del arte en el entorno de la VIU.
- **Límite para citarlo:** no lo uses como evidencia de que el LSTM "predice" Bitcoin.

## Referencias que cita y conviene localizar

McNally, Roche y Caton (2018), "Predicting the price of Bitcoin using machine learning"; Mudassir y colaboradores (2020), predicción de Bitcoin con variables de alta dimensión; Triebe y colaboradores (2021), "NeuralProphet: Explainable forecasting at scale"; Hochreiter y Schmidhuber (1997), LSTM; Sezer, Gudelek y Ozbayoglu (2020), revisión de aprendizaje profundo en series financieras (10.1016/j.asoc.2020.106181 según el documento); Lim y Zohren (2021), predicción de series con aprendizaje profundo; Torres y colaboradores (2021), revisión de aprendizaje profundo en series temporales; Kingma y Ba (2017), Adam; Yenidoğan y colaboradores (2018), Bitcoin con ARIMA y Prophet. **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (datos, métodos, fundamentos matemáticos y tablas)

Contenido técnico íntegro del texto principal (páginas 1 a 11 del PDF; las páginas 12 a 16 son bibliografía). Páginas = páginas del PDF.

## A1. Datos y preprocesamiento (p. 8 y p. 9)

- **Fuente:** API de Yahoo! Finance con Python; **precio de cierre diario de Bitcoin del 1 de enero de 2017 al 1 de mayo de 2023** (≈ 2 300 días); un único regresor (solo el precio de cierre); rango del precio [777,75; 67 566,82] USD.
- **Normalización min-max** a [0, 1] (calculada sobre la serie completa, según el texto: "hemos decidido aplicar la normalización min-max… cambiar el rango de los valores de [777,75; 67 566,82] a [0, 1]", antes de la partición; indicio de **fuga de información** del máximo y el mínimo del periodo de prueba hacia el entrenamiento).
- **Serialización:** secuencias de **30 valores** (la entrada son los 30 días anteriores; se predice el cierre del día siguiente).
- **Partición:** **75 % entrenamiento, 15 % validación, 10 % prueba final** (la prueba cubre aproximadamente de octubre de 2022 a mayo de 2023, según la Figura 7), **una sola partición cronológica** (sin ventana móvil).

## A2. Modelos y fundamentos matemáticos (p. 4 a 7)

- **Referente: NeuralProphet** (Triebe y otros, 2021), con ajustes por defecto y 30 elementos de salida; Prophet: ŷ_t = g(t) + s(t) + h(t) + ε_t  (ecuación 1) con tendencia g, estacionalidad s, efecto festivo h y ε normal; NeuralProphet: ŷ_t = T(t) + S(t) + E(t) + F(t) + A(t) + L(t)  (ecuación 2) con tendencia, estacionalidad, eventos, regresores futuros, autorregresión y regresores retardados.
- **Perceptrón** (ecuación 3): ρ(x) = 1 si φ(wᵀx + b) ≥ 0 y 0 en otro caso; red prealimentada (FFNN) de capas totalmente conectadas.
- **Red convolucional (CNN)** (ecuación 4, 2D): h^{l+1}_{ij} = Σ_{a=0}^{n−1} Σ_{b=0}^{m−1} w^l_{ab}·h^l_{i+a, j+b}, seguida de activación (ReLU) y normalización por lote.
- **LSTM** (Hochreiter y Schmidhuber, 1997): puerta de olvido f_t = σ(W_f·h_{t−1} + V_f·x_t + b_f); puerta de entrada i_t = σ(W_i·h_{t−1} + V_i·x_t + b_i); memoria candidata C̃_t = tanh(W_C·h_{t−1} + V_C·x_t + b_C); memoria interna C_t = f_t ⊗ C_{t−1} + i_t ⊗ C̃_t; puerta de salida o_t = σ(W_o·h_{t−1} + V_o·x_t + b_o); estado oculto h_t = o_t ⊗ tanh(C̃_t) (como figura en el texto; la forma estándar usa tanh(C_t)).
- **Arquitecturas (Tabla 1)**, diseñadas con un número similar de parámetros entrenables ω (≈ 2 100 a 2 230):

| FFNN | Salida | ω | CNN | Salida | ω | LSTM | Salida | ω |
|---|---|---|---|---|---|---|---|---|
| FCL | (1, 32) | 992 | Conv1D | (1, 28, 30) | 120 | LSTM | (1, 30, 20) | 1 760 |
| FCL | (1, 32) | 1 056 | Max-Pool | (1, 14, 30) | 0 | LSTM | (1, 4) | 400 |
| FCL | (1, 1) | 33 | Flatten | (1, 420) | 0 | FCL | (1, 1) | 5 |
| | | | FCL | "(1, 1)" en el PDF | 2 105 (= 420 × 5 + 5, es decir, 5 unidades) | | | |
| | | | FCL | (1, 1) | 6 | | | |
| **Total** | | **2 081** | | | **2 231** | | | **2 165** |

- **Entrenamiento:** TensorFlow; pérdida MSE; optimizador Adam (Kingma y Ba); mismas condiciones para las tres redes. No se indican épocas, tamaño de lote, tasa de aprendizaje ni semillas, ni número de repeticiones.

## A3. Métricas (p. 9 y p. 10)

MAE = (1/N)·Σ|y_i − ŷ_i|; RMSE = sqrt( (1/N)·Σ (y_i − ŷ_i)² ); MedAE = mediana{|y_i − ŷ_i|}; MAPE = (100/N)·Σ |y_i − ŷ_i|/|y_i|; SMAPE = (100/N)·Σ |y_i − ŷ_i|/(|y_i| + |ŷ_i|) (en el texto sin el factor 2 del denominador habitual); **exactitud direccional** DA = (100/(N−1))·Σ_{i=1}^{N−1} σ(y_i, ŷ_i), con σ = 1 si signo(y_{i+1} − y_i) = signo(ŷ_{i+1} − ŷ_i) y 0 en otro caso (ecuación 5): compara el signo del cambio entre dos **valores consecutivos de la serie predicha** con el del cambio real (no el signo del retorno del día siguiente respecto del último precio observado).

## A4. Resultados (Tabla 2, p. 10) en el conjunto de prueba (dólares)

| Modelo | MAE | RMSE | MedAE | MAPE (%) | SMAPE (%) | DA (%) |
|---|---|---|---|---|---|---|
| FFNN | 519,01 | 778,10 | 347,84 | 2,4007 | 1,2008 | 94,37 |
| CNN | 476,81 | 721,57 | 297,49 | 2,2241 | 1,1087 | 94,80 |
| **LSTM** | **397,44** | **604,27** | **239,59** | **1,8418** | **0,9192** | **97,40** |
| NeuralProphet | 662,01 | 905,40 | 486,10 | 3,1237 | 1,5600 | 91,77 |

Interpretación de los autores: el LSTM es el mejor (error por debajo de 400 USD, SMAPE < 1 %, DA > 97 %); los patrones temporales de corto y largo plazo son más representativos que los espaciales; la CNN supera a la FFNN; todos superan a NeuralProphet.

## A5. Lectura crítica para la tesis (a verificar; la crítica contrasta con el referente ingenuo)

1. **No hay referente ingenuo** (precio de ayer como predicción de hoy): en niveles de precio un MAPE de 1,8 % o de 3,1 % es compatible con "predecir que mañana vale lo mismo que hoy" (la volatilidad diaria típica de BTC en 2022–2023 está en torno al 2–3 %); sin ese referente no se puede decir que las redes aprendan nada. El propio texto atribuye 91,77 % de exactitud direccional a NeuralProphet, una cifra que ningún modelo de dirección honesto alcanza (la literatura de la revisión de Baquero reporta 50–57 %), lo que indica que la métrica DA (secuencia predicha frente a secuencia real) no mide la predicción de dirección del retorno.
2. **Normalización con toda la serie** (el máximo de 67 566,82 USD de noviembre de 2021 está en el entrenamiento, pero el escalado se definió sobre todo el periodo): fuga de información leve y escala dependiente del nivel.
3. **Partición única de prueba de ≈ 230 días**, sin repeticiones con semillas distintas ni intervalos de confianza ni pruebas de Diebold y Mariano.
4. **Detalles del entrenamiento sin informar** (épocas, lote, tasa de aprendizaje, semillas) y diferencia de 69 parámetros entre arquitecturas.
5. **Tabla 1:** la salida de la capa totalmente conectada de la CNN se imprime como (1, 1) pero sus 2 105 parámetros equivalen a 5 unidades (420 × 5 + 5); el total de 2 231 coincide con 120 + 2 105 + 6.
6. Para la tesis: la comparación FFNN < CNN < LSTM con el mismo número de parámetros es una comparación interna útil, pero **no demuestra capacidad predictiva** respecto del referente ingenuo.

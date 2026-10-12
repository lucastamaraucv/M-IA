# Bio-Inspired Spiking Recurrent Networks with Evolutionary Optimization for Non-Stationary Cryptocurrency Forecasting

**Extracción de conocimiento: 2026-10-02** (leídas las páginas 1 a 8 y 14 a 25 de 32; el resto son apéndices, figuras y referencias)

| Campo | Valor |
|---|---|
| Título exacto | Bio-Inspired Spiking Recurrent Networks with Evolutionary Optimization for Non-Stationary Cryptocurrency Forecasting |
| Autores | Francis Noah Walugembe (Universidad Alma Mater Europaea, Maribor, Eslovenia), Maciej Wielgosz (AGH, Cracovia), Matej Mertik (Alma Mater Europaea) y Matjaž Gams (Instituto Jožef Stefan, Liubliana) |
| Tipo / Venue / Año | Artículo de revista: Big Data and Cognitive Computing (MDPI) 2026, 10(7), 200; recibido el 18 de marzo de 2026, aceptado el 3 de junio de 2026, publicado el 23 de junio de 2026 |
| Archivo local | `BDCC-10-00200.pdf` |
| URL / DOI | https://doi.org/10.3390/bdcc10070200 |
| Métodos | LSTM y una variante "SLSTM" con dinámica sináptica, de membrana y de umbral adaptativo inspirada en LIF (sin reinicio, umbral aprendible, gradiente sustituto arctan, snnTorch); optimización de tasa de aprendizaje y decaimiento de pesos con el optimizador del lobo gris (GWO) |
| Datos | 4 039 cierres diarios de BTC-USD de Yahoo Finance, del 17 de septiembre de 2014 al 9 de octubre de 2025; normalización mín-máx con parámetros del entrenamiento; partición cronológica 80/20; ventana de entrada de 30 días (p. 6 y p. 8) |

## Aporte clave

Compara cuatro configuraciones (LSTM, SLSTM, GWO-LSTM y GWO-SLSTM) para predecir el cierre de Bitcoin del día siguiente y concluye que la variante espigante optimizada con GWO tiene el menor error dentro de esa familia de modelos (p. 1 y p. 20). Es un antecedente reciente (junio de 2026) de **SNN aplicadas a Bitcoin**, pero evalúa solo precio de nivel y **no incluye ningún referente ingenuo**.

## Hallazgos cuantitativos (HECHO, con página)

- **Error en el conjunto de prueba, una sola ejecución con semilla 25** (Tabla 4, p. 20): GWO-SLSTM RMSE 1 840,97 y MAPE 1,76 %; GWO-LSTM 2 217,24 y 2,46 %; SLSTM 3 501,48 y 3,86 %; LSTM 4 030,10 y 4,40 %.
- **Ventanas de robustez** (Tabla 5, p. 21): en R2 (24 de julio de 2023 a 30 de agosto de 2024) GWO-SLSTM tiene RMSE 1 438,62 y MAPE 1,80 %; en R3 (24 de julio de 2023 a 20 de marzo de 2025) 1 760,52 y 1,86 %. **La ventana R1 no se evaluó** porque queda fuera del horizonte de predicciones guardadas (p. 7 y p. 20); el propio texto lo reconoce.
- **Diseño estadístico:** 10 ejecuciones con semillas distintas y pruebas t pareadas, con mejora relativa en porcentaje (p. 15).
- **Búsqueda GWO** restringida a la tasa de aprendizaje [1e-4, 1e-1] y al decaimiento de pesos; presupuesto de 5 × 5 candidatos; etapa rápida de 5 épocas (p. 14 y p. 23).
- **Tiempo de entrenamiento:** GWO-SLSTM 39,71 s frente a 137,28 s de GWO-LSTM, pero con marcos de software distintos (PyTorch contra TensorFlow) y números de épocas distintos, por lo que los propios autores advierten que no prueba mayor eficiencia (p. 22 y p. 23).
- **Limitaciones declaradas** (p. 25): un solo activo; sin comparación con modelos más modernos (Transformers, descomposición); marcos distintos; sin medida de energía; sensibilidad al gradiente sustituto y al "reinicio ninguno" sin ablación.

## Verificación propia: el referente que falta (EJECUCIÓN PROPIA, 2026-10-02)

El artículo no calcula el método ingenuo (repetir el precio de ayer). Con la serie diaria de BTC del proyecto (`logs_ind/btc_snapshot_cc_20160424_20260425.csv`, fuente CryptoCompare, no Yahoo) en el periodo de prueba aproximado del artículo (24 de julio de 2023 a 9 de octubre de 2025, 809 días, precio medio 72 176 dólares frente a 72 108,64 que da el artículo):

| Modelo | RMSE (USD) | MAPE |
|---|---|---|
| **Ingenuo (precio de ayer), cálculo propio** | **1 791** | **1,71 %** |
| GWO-SLSTM (artículo, una semilla) | 1 840,97 | 1,76 % |
| GWO-LSTM (artículo) | 2 217,24 | 2,46 % |
| SLSTM (artículo) | 3 501,48 | 3,86 % |
| LSTM (artículo) | 4 030,10 | 4,40 % |

En la ventana R3 evaluable (606 días) el ingenuo da RMSE 1 758 y MAPE 1,84 %, frente a 1 760,52 y 1,86 % del GWO-SLSTM. **El mejor modelo del artículo queda igual o ligeramente peor que repetir el precio de ayer.** Limitación: no usan la misma fuente de precios ni se confirmó que el periodo coincida exactamente; el cálculo es indicativo, no una réplica.

## Limitaciones y críticas

- **[OPINIÓN]** **Falta el referente ingenuo** y el artículo no lo discute; con el resultado anterior, la afirmación de que GWO-SLSTM es un "fuerte candidato" no queda respaldada frente al paseo aleatorio. Es el defecto metodológico que Baquero (2026) describe como el más frecuente en la literatura (estándar 3).
- **[OPINIÓN]** Predice el **nivel del precio** con normalización mín-máx: las correlaciones de 0,998 y los errores porcentuales de 1,8 % son triviales para cualquier serie persistente (misma advertencia que en el artículo de ESN para Bitcoin).
- **[OPINIÓN]** La tasa de aprendizaje y el decaimiento de pesos de los modelos "base" son fijos (0,001 y 0), mientras que a los modelos GWO se les ajustan; **gran parte de la mejora puede ser simplemente haber ajustado esos dos parámetros**, no la neurona espigante. El LSTM base se detiene a la época 5 con un error de validación enorme, señal de mal ajuste y no de límite del modelo.
- **[OPINIÓN]** Una sola semilla para las tablas principales, una sola partición 80/20 y solo una de tres ventanas de robustez evaluable parcialmente. No hay referencia a costes ni a dirección.
- **[OPINIÓN]** El "SLSTM" es una celda LSTM con dinámica inspirada en LIF y sin reinicio; no es una red espigante con espigas binarias propias de neuronas como TS-LIF.

## Conexión con mi tesis (red E20)

- **Antecedente reciente de SNN en Bitcoin** que mi tesis puede citar en el estado del arte, junto con la advertencia de que su mejora no se mide contra el referente ingenuo.
- **Sirve de ejemplo del "problema de ajuste desigual"** descrito en el trabajo de Audrino y Chassot: un modelo ajustado por búsqueda se compara con uno sin ajustar, y la ventaja se atribuye a la arquitectura. En mi tesis, E20 y los modelos de ML se comparan con la misma lectura y la misma ventana.
- **La comprobación del referente ingenuo** que hice aquí es reutilizable: puedo incluirla en el capítulo de resultados como ejemplo de cómo revisar la literatura (con la salvedad de la fuente de datos).
- **Límite para citarlo:** nivel del precio, sin dirección ni movimiento y sin referente simple.

## Referencias que cita y conviene localizar

Hochreiter y Schmidhuber (1997), LSTM; Mirjalili, Mirjalili y Lewis (2014), Grey Wolf Optimizer; Neftci, Mostafa y Zenke (2019), gradiente sustituto; Eshraghian y colaboradores (2023), snnTorch y entrenamiento de SNN; Zhou y colaboradores (2021), Informer; los estudios citados como [14] sobre LSTM en criptomonedas y [17] sobre ConvLSTM con PSO (la bibliografía numerada está al final del artículo, no leída). **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (datos, métodos, fundamentos matemáticos y tablas)

Contenido técnico íntegro del texto principal y los apéndices (páginas 1 a 30 del PDF; las páginas 30 a 32 son referencias). Páginas = páginas del PDF. Artículo: Big Data and Cognitive Computing 2026, 10, 200, https://doi.org/10.3390/bdcc10070200 (MDPI, acceso abierto; recibido el 18 de marzo de 2026, publicado el 23 de junio de 2026). Código y datos en https://zenodo.org/records/18983179.

## A1. Datos y preprocesamiento (p. 6 y p. 7)

- **Serie:** precio de cierre diario BTC-USD de Yahoo Finance (`yfinance`, descarga del 18 de enero de 2026), del **17 de septiembre de 2014 al 9 de octubre de 2025**, **4 039 observaciones** consecutivas; menos de 0,001 % de valores faltantes por interpolación lineal.
- **Escalado min-max a [0, 1]** ajustado **solo con el entrenamiento** y aplicado sin cambios a validación y prueba.
- **Partición cronológica 80/20:** primeras **3 231** observaciones para entrenamiento y validación, últimas **808** para prueba (los valores de prueba tienen media 72 108,64 USD y máximo 124 752,53, frente a media 13 692,55 y máximo 67 566,83 en el entrenamiento; Tabla A1).
- **Ventana de entrada de 30 días** (elegida tras explorar 5 a 120 días; el rendimiento se estabiliza en 30–35 días). Entrada **univariante** (solo el cierre); el objetivo es el **precio del día siguiente** (nivel de precio, no retorno).
- **Diagnósticos (Tabla A1):** ADF −1,54 (p = 0,51) en entrenamiento y −0,53 (p = 0,89) en prueba (no estacionaria); Ljung–Box 31 867,38 y 7 711,74 (p = 0,00); asimetría 1,38 y 0,02; curtosis 0,94 y −1,17.
- **Regímenes:** alcista (retorno diario > 1 %) 1 345 días (33,3 %), neutro 1 577 (39,0 %), bajista (< −1 %) 1 118 (27,7 %).

## A2. Modelos y fundamentos matemáticos (p. 9 y p. 10)

- **LSTM** (ecuaciones 1 a 6): i_t = σ(W_ii x_t + b_ii + W_hi h_{t−1} + b_hi); f_t = σ(W_if x_t + b_if + W_hf h_{t−1} + b_hf); g_t = tanh(W_ig x_t + b_ig + W_hg h_{t−1} + b_hg); o_t = σ(W_io x_t + b_io + W_ho h_{t−1} + b_ho); c_t = f_t ⊙ c_{t−1} + i_t ⊙ g_t; h_t = o_t ⊙ tanh(c_t).
- **LSTM con picos (SLSTM)** (ecuaciones 7 a 12): conserva las compuertas pero sustituye (c_t, h_t) por una **corriente sináptica syn_t** y un **potencial de membrana mem_t**: las compuertas usan mem_{t−1} en lugar de h_{t−1} (i_t = σ(W_ii x_t + b_ii + W_hi mem_{t−1} + b_hi), análogo para f, g, o); syn_t = f_t ⊙ syn_{t−1} + i_t ⊙ g_t; **mem_t = o_t ⊙ tanh(syn_t)**. Evento de pico S_t = I(mem_t ≥ V_th) con **umbral V_th aprendible** (learn_threshold = True), **reinicio "ninguno"** (la membrana no se reinicia al cruzar el umbral) y **gradiente sustituto arco tangente** (`surrogate.atan()`, snnTorch). **Observación crítica:** como no hay reinicio ni fuga explícita λ (las compuertas de olvido hacen de fuga) y la salida lineal puede leer mem_t, la "red con picos" es en la práctica una LSTM con un evento umbral añadido; los propios autores la describen como "con inspiración en picos y compuerta de eventos con umbral, no una red con picos clásica de reinicio fuerte". El apéndice de nomenclatura menciona V_reset, λ y σ_t (ruido) que **no se usan en los experimentos reportados**.
- **Cabeza de salida:** una capa recurrente (32 unidades ocultas) y una capa lineal.

## A3. Optimizador de lobo gris (GWO) (p. 10 a 13)

- Algoritmo de Mirjalili (2014): lobos α, β, δ, ω; **factor de convergencia** a(t) = 2 − 2·t/T_max  (13); para cada líder ℓ ∈ {α, β, δ}: A_ℓ = a(2r₁ − 1), C_ℓ = 2r₂  (14), D_ℓ = |C_ℓ ⊙ X_ℓ − X_i|  (15), X′_ℓ = X_ℓ − A_ℓ ⊙ D_ℓ  (16); posición nueva X_i^{new} = (X′_α + X′_β + X′_δ)/3  (17), recortada a los límites; r₁, r₂ ∼ U(0, 1)^D.
- **Espacio de búsqueda (2 dimensiones):** tasa de aprendizaje η ∈ [10⁻⁴, 10⁻¹] (ambos modelos) y decaimiento de pesos WD ∈ [10⁻⁴, 0,9] (LSTM) y [0, 10⁻³] (SLSTM). Los rangos de WD son distintos entre arquitecturas (el LSTM puede llegar a 0,9, un valor extremo).
- **Presupuesto igual:** 5 lobos × 5 iteraciones = **25 evaluaciones**; aptitud = MSE de validación tras **5 épocas** (etapa 1); la mejor configuración se reentrena hasta **50 épocas** con parada temprana (paciencia 5) y restauración de los mejores pesos, **sobre entrenamiento + validación combinados** (etapa 2).
- **Fijos en todos:** AdamW, lote 32, 32 unidades ocultas, sin dropout, semilla 25. Valores finales (Tabla 3): η = 0,0052 / 0,0018; WD = 0,00012 (GWO-LSTM) y 0,00079 (GWO-SLSTM).
- **Referentes sin GWO (Tabla 4):** Adam con η = 0,001 y WD = 0 (sin búsqueda; el mismo presupuesto no se les da).
- **Entorno:** GPU NVIDIA Tesla V100, 64 GB de RAM, Python 3.9; LSTM en **TensorFlow/Keras** y SLSTM en **PyTorch + snnTorch 0.9.4** (marcos distintos).

## A4. Evaluación (p. 14 y p. 15)

MSE, RMSE y MAPE en dólares, **PBIAS = 100 × Σ(y_t − ŷ_t)/Σ y_t** (positivo = subestimación); contraste *t* pareado sobre **10 ejecuciones con semillas distintas** y reducciones porcentuales; análisis de robustez por ventanas R1, R2 y R3 (Tabla 2: R1 entrenamiento 17-9-2014 a 6-5-2021, prueba 7-5-2021 a 23-7-2023; R2 entrenamiento 26-10-2015 a 14-6-2022, prueba 15-6-2022 a 30-8-2024; R3 entrenamiento 15-5-2016 a 2-1-2023, prueba 3-1-2023 a 20-3-2025). **Los autores aclaran que no se reentrena en cada ventana:** las predicciones guardadas cubren solo el 20 % final, por lo que R1 no se puntúa y R2 y R3 se puntúan solo en la parte que se solapa con ese 20 % (24 de julio de 2023 en adelante).

## A5. Resultados completos

**Tabla 4 (p. 20), una ejecución con semilla 25:**

| Métrica | LSTM | SLSTM | GWO-LSTM | GWO-SLSTM |
|---|---|---|---|---|
| RMSE entrenamiento | 2 103,08 | 1 656,66 | 996,15 | 839,49 |
| MAPE entrenamiento (%) | 77,79 | 43,35 | 22,46 | 28,18 |
| PBIAS entrenamiento (%) | −2,64 | 1,37 | −3,50 | 1,32 |
| **RMSE prueba** | 4 030,10 | 3 501,48 | 2 217,24 | **1 840,97** |
| MSE prueba | 16 241 684,70 | 12 260 338,00 | 4 916 169,91 | 3 389 182,50 |
| **MAPE prueba (%)** | 4,40 | 3,86 | 2,46 | **1,76** |
| PBIAS prueba (%) | 0,03 | 1,13 | 0,11 | 0,36 |
| Parada temprana (época) | 5 | 6 | 26 | 20 |
| Mejor pérdida de validación | 0,001047 | — | 0,000317 | — |

**Tabla 5 (p. 21), robustez por ventanas (solo R2 y R3 puntuadas):**

| Ventana (subperiodo) | Modelo | RMSE | MAPE (%) | PBIAS (%) | Rango |
|---|---|---|---|---|---|
| R2 (24-7-2023 a 30-8-2024) | LSTM | 3 456,57 | 4,93 | −0,72 | 4 |
| | SLSTM | 2 790,86 | 4,36 | 0,33 | 3 |
| | GWO-LSTM | 1 711,39 | 2,78 | −1,86 | 2 |
| | **GWO-SLSTM** | **1 438,62** | **1,80** | −0,13 | 1 |
| R3 (24-7-2023 a 20-3-2025) | LSTM | 4 008,73 | 4,84 | −0,73 | 4 |
| | SLSTM | 3 148,13 | 4,07 | 0,25 | 3 |
| | GWO-LSTM | 1 936,34 | 2,56 | −0,92 | 2 |
| | **GWO-SLSTM** | **1 760,52** | **1,86** | 0,08 | 1 |

Reducción media de RMSE de GWO-SLSTM en R2 y R3: **57,1 %** frente a LSTM, 46,1 % frente a SLSTM y 12,3 % frente a GWO-LSTM. Contraste *t* pareado entre GWO-LSTM y LSTM, y entre GWO-SLSTM y SLSTM: p < 0,001 (los valores completos de las 10 ejecuciones no se reportan; **no se prueba directamente GWO-SLSTM frente a GWO-LSTM** con repeticiones).

**Correlaciones y medias de predicción** (Figuras 4 a 7): correlación 0,990 (LSTM), 0,993 (SLSTM), 0,998 (GWO-LSTM y GWO-SLSTM); media real de prueba 72 108,64 USD frente a predicha 72 083,94 (LSTM), 71 290,94 (SLSTM), 72 030,90 (GWO-LSTM) y 71 852,06 (GWO-SLSTM). **RMSE móvil de 7 días (Apéndice B):** media 3 365,55 (LSTM; máx. 11 882,01; MAPE 4,40 %), 2 003,80 (GWO-LSTM; máx. 5 241,01; MAPE 2,45 %), 2 975,79 (SLSTM; máx. 9 781,52; MAPE 3,86 %) y **1 624,47 (GWO-SLSTM; máx. 4 715,67; MAPE 1,76 %)**.

**Dinámica de entrenamiento** (Figuras 9 a 12): MSE de validación final 32 543 626 (LSTM, época 5), 29 990 066 (SLSTM, época 6), 6 278 161 (GWO-LSTM, época 26) y **4 928 175** (GWO-SLSTM, época 20).

**Tabla 6 (eficiencia, segundos):** entrenamiento 7,75 (LSTM), 137,28 (GWO-LSTM), 8,42 (SLSTM) y 39,71 (GWO-SLSTM); prueba 0,37, 0,38, 0,02 y 0,02; por muestra y época 0,00048, 0,00165, 0,00044 y 0,00062; los autores advierten que la ventaja de tiempo es "específica de la implementación" (marcos y épocas distintos).

## A6. Limitaciones declaradas (p. 25) y lectura crítica para la tesis

- Declaradas: un solo activo; comparación solo dentro de la familia LSTM (sin Transformers, descomposición ni referentes externos); marcos distintos; sin medida de energía en hardware neuromórfico; sensibilidad al gradiente sustituto y al reinicio "ninguno".
- **Lectura crítica (a verificar):** (1) **no hay referente ingenuo (precio de ayer)** ni modelos de retorno cero; un MAPE de 1,76 % en niveles de precio con volatilidad diaria de 2–3 % equivale al de repetir el último valor; la correlación de 0,998 sobre niveles es la propia de cualquier predictor persistente. (2) **El efecto "GWO" es en gran parte el efecto de pasar de Adam con η = 0,001 y 5 épocas (parada temprana a la época 5 con la validación aún muy alta, MSE de 32 millones) a un afinamiento de tasa de aprendizaje**: la línea base sin GWO es débil por construcción (parada temprana tras 5 épocas); no es una comparación con un LSTM bien entrenado. (3) El decaimiento de pesos del GWO-LSTM puede llegar a 0,9 mientras el del GWO-SLSTM se limita a 10⁻³: espacios de búsqueda distintos, con ventaja potencial para una arquitectura. (4) El 20 % de prueba (808 días, 2023-2025) incluye precios (hasta 124 752 USD) **fuera del rango del entrenamiento (máx. 67 566,83)**, lo que con escalado min-max produce entradas mayores que 1; aun así el RMSE es relativamente bajo, lo que sugiere un comportamiento de persistencia. (5) Una sola semilla para los números principales; las 10 repeticiones solo se resumen con p < 0,001. (6) **La "red de picos" no es una SNN clásica** (reinicio "ninguno", sin fuga en la membrana, compuertas de LSTM): su relación con la neurona TS-LIF de E20 es meramente nominal. (7) Los resultados de ventana R1 (la más difícil, bajista) **no se calculan**.

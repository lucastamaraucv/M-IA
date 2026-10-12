# Forecasting Bitcoin returns: Econometric time series analysis vs. machine learning

**Extracción de conocimiento: 2026-10-02.** Leído el texto completo (14 páginas; las referencias de las páginas 13 y 14 solo se listan). Las páginas citadas son las del PDF.

## 1. Ficha bibliográfica

| Campo | Valor |
|---|---|
| Título exacto | Forecasting Bitcoin returns: Econometric time series analysis vs. machine learning |
| Autores | Theo Berger (Universidad de Ciencias Aplicadas de Hannover y Universidad de Bremen) y Jana Koubová (Sparkassen Rating und Risikosysteme, Berlín) |
| Tipo / revista / año | Artículo de investigación, Journal of Forecasting 2024, 43(7):2904-2916. Recibido el 5 de junio de 2023, revisado el 28 de marzo de 2024, aceptado el 19 de mayo de 2024 |
| DOI | 10.1002/for.3165 (la copia del repositorio de Hannover cita https://doi.org/10.25968/opus-3178) |
| Licencia | Acceso abierto, CC BY-NC-ND 4.0 |
| Archivo local | `berger_koubova2024-forecasting_bitcoin_returns.pdf` |
| Clasificación JEL | C33, C58, G17, G23 |

## 2. Pregunta, aportes y resumen de resultados

- **Pregunta:** ¿predicen mejor los retornos diarios de Bitcoin los modelos econométricos ARMA-GARCH o las redes neuronales recurrentes (RNN simple, RNN profunda, LSTM)? (p. 2 y p. 3).
- **Dos aportes declarados** (p. 3): (1) evaluar si las propiedades estadísticas de los retornos diarios de Bitcoin cumplen los supuestos de los modelos econométricos; (2) comparar RNN con capas LSTM frente a ARMA-GARCH y un referente ingenuo.
- **Resultado del resumen** (p. 1): las técnicas de aprendizaje automático superan a los referentes econométricos en precisión dentro y fuera de muestra; las arquitecturas profundas y las capas LSTM **no** aumentan la precisión de pronósticos diarios; una RNN simple es una elección razonable.
- **Resultado de las tablas** (p. 12 y p. 13): con RMSE las redes superan a ARMA-GARCH por margen pequeño (0,0404 frente a 0,0410), pero con **MAE el ARMA-GARCH es el mejor** (0,0269 frente a 0,0301-0,0303). Los autores concluyen que una RNN simple o un modelo econométrico parsimonioso son opciones sólidas.

## 3. Datos

- **Serie:** precio diario de Bitcoin desde el primer precio disponible, el **28 de abril de 2013**, hasta el **12 de diciembre de 2021**; n = 3 145 precios y 3 143 retornos logarítmicos (p. 6 y p. 7, Tabla 1).
- **Estadísticos de los retornos diarios** (Tabla 1, p. 7): media 0,19 %; desviación típica 4,17 %; mínimo −43,37 %; percentil 25: −1,37 %; mediana 0,21 %; percentil 75: 1,90 %; máximo 28,71 %. Precios: media 8 818,48; desviación 14 568,24; mínimo 67,81; máximo 67 617,02 dólares. (En el texto los retornos aparecen como 4,1698 y 0,1884 en porcentaje.)
- **Pruebas sobre la serie** (Tabla 2, p. 7): Ljung-Box con 20 retardos: 53,70 para retornos y 356,65 para retornos al cuadrado (ambos con valor p ≈ 0, es decir, hay autocorrelación y **agrupamiento de volatilidad**); prueba de Dickey y Fuller aumentada: precios 0,39 (valor p 0,91, no estacionarios) y retornos 14,71 (valor p ≈ 0, estacionarios); Jarque-Bera de los retornos: 21,02 (valor p ≈ 0, **no normales y con colas gruesas**). La autocorrelación de los retornos decae rápido (Figura 2).
- **Hechos estilizados confirmados:** alta volatilidad, agrupamiento de volatilidad y colas pesadas (p. 7), coherentes con Hu y otros (2019), Momtaz (2021), Zhang y otros (2018) y Borri (2019).
- **Fuente de datos:** disponibles "previa petición razonable" al autor (Declaración de disponibilidad de datos, p. 13).

## 4. Diseño experimental

- **Tuplas superpuestas** de datos para cada modelo: ventana de entrenamiento de T = **100, 250 o 500 días** más **10 días** para evaluar el pronóstico, es decir, tuplas de 110, 260 y 510 días. Número de tuplas: 3 032 de 110 días, 2 882 de 260 días y 2 632 de 510 días (p. 7).
- **Particiones para el aprendizaje automático** (p. 7 y Figura 4): primeras 70 % de las tuplas para entrenamiento, siguientes 20 % para validación y último 10 % para prueba. Entrenamiento más validación son "dentro de muestra"; la prueba es "fuera de muestra".
- **Horizontes:** 1, 5 y 10 días hacia adelante (p. 7).
- **Métricas** (p. 6): RMSE y MAE promediados sobre todas las tuplas (ecuaciones 12 y 13, sección 5).
- **Referente ingenuo** (p. 5 y p. 6): el retorno del periodo anterior se usa como pronóstico del siguiente (la última observación de la muestra de entrenamiento como pronóstico del día siguiente). Referente adicional entre redes: una red completamente conectada simple.
- **Optimización de la red:** Adam (combinación de momentum y RMSProp) (p. 6). Épocas elegidas con el menor número que da la menor pérdida en entrenamiento y validación (p. 10 y p. 11).

## 5. Fundamentos matemáticos y formulación de los modelos

### 5.1 ARMA(p,q)-GARCH(m,n) (sección 3.1, p. 5)

Media condicional ARMA y varianza condicional GARCH sobre los retornos y_t:

- y_t = Σ_{i=1}^{p} φ_i · y_{t−i} + Σ_{j=1}^{q} θ_j · u_{t−j} + u_t, con u_t ~ i.i.d. D(0, σ_t²)  (ecuación 1)
- σ_t² = α_0 + α_1·u²_{t−1} + … + α_m·u²_{t−m} + β_1·σ²_{t−1} + … + β_n·σ²_{t−n}  (ecuación 2)
- Restricciones: α_0 > 0, α_i ≥ 0 para i = 1..m, β_j ≥ 0 para j = 1..n y Σ_{i=1}^{max(m,n)} (α_i + β_i) < 1 (estacionariedad).
- u_t es ruido blanco (media cero, varianza constante, sin correlación temporal). Se prueban distribuciones D **gaussiana y t de Student**. Los parámetros se estiman por **máxima verosimilitud**.
- Modelos anidados evaluados: ARMA(p,q), ARMA(p,q)-GARCH(m,n) con distintos órdenes, y las variantes EGARCH y GJR-GARCH (asimétricas, sin mejora de ajuste, p. 10).

### 5.2 Selección del orden ARMA-GARCH (p. 9 y p. 10)

- Se estiman órdenes p de 1 a 5 y q de 0 a 5 con residuos gaussianos y t, y se elige el menor **criterio de información de Akaike (AIC)** (Tabla 3). Los rangos se eligieron con correlogramas (nota 3).
- Ejemplos de la Tabla 3: con distribución gaussiana, mínimos de AIC cercanos a 11 035; con t, cerca de 12 054; para el GARCH(m,n), valores de 12 144 a 12 551.
- **Resultado:** el mejor ajuste es **ARMA(4,4)-GARCH(1,3) con residuos t-Student** (p. 10).

### 5.3 Red neuronal recurrente simple y profunda (sección 3.2, p. 5)

Para entrada X_t y salida y_t, estado oculto h_t con h_0 = 0 y t = 1..M (M = número de tuplas de entrenamiento):

- h_t = f_W(h_{t−1}, X_t)  (ecuación 3), con f = tanh
- h_t = tanh(W_hh · h_{t−1} + W_hx · X_t + b_h)  (ecuación 4)
- y_t = tanh(W_yh · h_t + b_y)  (ecuación 5)

Una RNN profunda apila más de una capa recurrente. Ejemplo de dimensión del texto: 2 capas ocultas con 5 neuronas y horizonte de 10 días dan una salida de última capa de matriz 10 × 5, que la capa de salida convierte en un vector de 10 pronósticos. Se estudian 1, 2 y 3 capas ocultas con 1, 5 y 10 unidades (el apartado 5.2 amplía a 5, 10, 15, 20 y 80 neuronas por capa).

### 5.4 LSTM (sección 3.2.1, p. 6)

Añade al estado oculto un estado de celda (memoria de largo plazo) c_t:

- f_t = σ(W_fx·X_t + W_fh·h_{t−1} + b_f)  (puerta de olvido, ecuación 6)
- g_t = tanh(W_gx·X_t + W_gh·h_{t−1} + b_g)  (candidato, ecuación 7)
- i_t = σ(W_ix·X_t + W_ih·h_{t−1} + b_i)  (puerta de entrada, ecuación 8)
- o_t = σ(W_ox·X_t + W_oh·h_{t−1} + b_o)  (puerta de salida, ecuación 9)
- c_t = f_t ⊙ c_{t−1} + i_t ⊙ g_t  (ecuación 10)
- y_t = h_t = o_t ⊙ tanh(c_t)  (ecuación 11)

Con ⊙ producto elemento a elemento. La capa de salida es densa con 1, 5 o 10 neuronas. El número de neuronas por capa es la dimensión del estado oculto.

### 5.5 Métricas (sección 3.3, p. 6)

- RMSE_T^B = sqrt( Σ_{i=1}^{M} Σ_{j=1}^{T} (y^{B,forecast}_{ij} − y^{B,true}_{ij})² / (M·T) )  (ecuación 12)
- MAE_T^B = Σ_{i=1}^{M} Σ_{j=1}^{T} | y^{B,forecast}_{ij} − y^{B,true}_{ij} | / (M·T)  (ecuación 13)
- M = número de tuplas, B = tamaño de lote (100, 250 o 500 días) y T = horizonte (1, 5 o 10 días).

## 6. Resultados completos

**Econométrico: referente ingenuo frente a ARMA(4,4)-GARCH(1,3)** (Tabla 4, p. 9):

| RMSE | Ingenuo 1 d | 5 d | 10 d | ARMA-GARCH 1 d | 5 d | 10 d |
|---|---|---|---|---|---|---|
| 100 días | 0,0585 | 0,0578 | 0,0576 | 0,0427 | 0,0431 | 0,0427 |
| 250 días | 0,0567 | 0,0558 | 0,0556 | 0,0405 | 0,0402 | 0,0401 |
| 500 días | 0,0563 | 0,0555 | 0,0554 | 0,0398 | 0,0401 | 0,0408 |
| Media | 0,0572 | 0,0564 | 0,0562 | 0,0410 | 0,0411 | 0,0412 |

MAE (media por horizonte): ingenuo 0,0384, 0,0384, 0,0384; ARMA-GARCH 0,0269, 0,0268, 0,0267.

**Redes: ajuste de hiperparámetros** (p. 10 y p. 11):
- Épocas: las curvas muestran pérdida decreciente al inicio; con lotes de 250 y 500 días el número de épocas no cambia la pérdida; hay indicios de sobreajuste pero con diferencia máxima entre entrenamiento y validación de 0,00014; en algunos casos la pérdida de entrenamiento es mayor que la de validación (diferencia máxima 0,0002).
- Neuronas y capas: la RNN profunda de 2 capas con 5 neuronas supera a la de 10 neuronas en RMSE y MAE; una tercera capa no mejora; igual para el LSTM.
- Lote: un lote mayor mejora el rendimiento salvo en la red completamente conectada, cuyo error sube con el lote.

**Redes por horizonte** (Tabla 6, p. 11), RMSE media:

| | Entren.+valid. 1 d | Prueba 1 d | Prueba 5 d | Prueba 10 d |
|---|---|---|---|---|
| Ingenuo | 0,0573 | 0,0592 | 0,0579 | 0,0578 |
| Red completamente conectada | 0,0376 | 0,0434 | 0,0434 | 0,0434 |
| RNN simple | 0,0400 | 0,0404 | 0,0404 | 0,0404 |
| RNN profunda | 0,0400 | 0,0406 | 0,0403 | 0,0405 |
| LSTM | 0,0394 | 0,0404 | 0,0406 | 0,0404 |

MAE (prueba): ingenuo 0,0441, 0,0433 y 0,0431; completamente conectada 0,0331, 0,0330 y 0,0330; RNN simple 0,0301, 0,0300 y 0,0301; RNN profunda 0,0301, 0,0302 y 0,0302; LSTM 0,0303, 0,0303 y 0,0300.

**ARMA-GARCH frente a redes por horizonte** (Tabla 7, p. 12): RMSE prueba ingenuo 0,0592, 0,0579, 0,0578; completamente conectada 0,0434 constante; RNN simple 0,0404 constante; RNN profunda 0,0406, 0,0403, 0,0405; LSTM 0,0404, 0,0406, 0,0404; **ARMA-GARCH 0,0410, 0,0411, 0,0412**. MAE de ARMA-GARCH: 0,0269, 0,0268 y 0,0267.

**Por tamaño de lote** (Tabla 8, p. 12), RMSE: ingenuo 0,0588, 0,0588, 0,0572; completamente conectada 0,0423, 0,0435, 0,0445; RNN simple 0,0414, 0,0402, 0,0396; RNN profunda 0,0414, 0,0403, 0,0397; LSTM 0,0414, 0,0404, 0,0395; ARMA-GARCH 0,0428, 0,0403, 0,0402 (lotes de 100, 250 y 500 días). MAE: ARMA-GARCH 0,0281, 0,0263, 0,0260; RNN simple 0,0306, 0,0300, 0,0295; LSTM 0,0308, 0,0303, 0,0296.

**Conclusiones de los autores** (p. 13): las redes superan a ARMA-GARCH con RMSE; con MAE el modelo econométrico parsimonioso no es superado; la complejidad adicional (LSTM, profundidad) no mejora el pronóstico diario; esto contradice a Lahmiri y Bekiros (2019).

## 7. Revisión de literatura resumida (p. 3 y p. 4)

Alessandretti y otros (2018): 1 681 criptomonedas, noviembre de 2015 a abril de 2018, árboles con refuerzo de gradiente y LSTM superan a la media móvil simple. Phaladisailoed y Numnonda (2018): datos de 1 minuto de 2012 a 2018, la GRU es la mejor. Tandon y otros (2019): LSTM con validación cruzada de 10 pliegues da menor MAE que bosque aleatorio y regresión lineal. Chu y otros (2017): IGARCH(1,1) y GJR-GARCH mejores para siete criptomonedas. Troster y otros (2019): modelo GAS con colas gruesas supera al GARCH en valor en riesgo. Figa-Talamanca y Patacca (2019): la atención (volumen) afecta media y varianza. Shen y otros (2021): RNN con GRU supera a GARCH y EWMA en volatilidad, pero es peor en valor en riesgo. McNally y otros (2018): RNN, LSTM y ARIMA para el precio.

## 8. Limitaciones y críticas

- Declarado por los autores: gráficos y correlogramas completos "disponibles previa petición" (notas 3 y 4); los datos solo previa solicitud.
- **[OPINIÓN] El "referente ingenuo" es débil.** Usar el retorno del día anterior como pronóstico duplica la varianza del error y da un RMSE de unas √2 veces la desviación típica (0,057 frente a 0,0417). El referente natural para retornos es **cero** (o la media). Por eso la afirmación de que "las técnicas de aprendizaje automático superan a los referentes" se apoya en una comparación favorable.
- **[OPINIÓN] Verificación propia (EJECUCIÓN PROPIA, 2026-10-02).** Con la serie diaria de BTC del proyecto (CryptoCompare), el pronóstico de **retorno cero** en el periodo de prueba aproximado del artículo (febrero a diciembre de 2021) da RMSE de 0,0403 a 0,0415 y MAE de 0,0302 a 0,0308, mientras que el "ingenuo" de retorno previo da RMSE de 0,059 a 0,061, coherente con el 0,0592 del artículo. Las redes del artículo (RMSE 0,0404, MAE 0,0301 a 0,0303) **no se distinguen del pronóstico cero**, y el ARMA-GARCH solo mejora en MAE (0,0269). Que el RMSE de las redes sea idéntico (0,0404) para los horizontes de 1, 5 y 10 días y para distintos tipos de red sugiere pronósticos casi constantes. Limitación: el periodo de prueba exacto del artículo depende del esquema de tuplas y no es reproducible con los datos disponibles; el cálculo es indicativo.
- **[OPINIÓN]** Solo se informan RMSE y MAE; no hay acierto de dirección, pruebas de significancia (Diebold y Mariano, conjunto de confianza), intervalos de confianza ni semillas repetidas.
- **[OPINIÓN]** Las tuplas son superpuestas y se usan para entrenamiento, validación y prueba de forma secuencial por tupla; no queda claro si hay solapamiento entre el final de entrenamiento y el inicio de la prueba (posible fuga).
- **[OPINIÓN]** El AIC se compara entre distribuciones (gaussiana y t) con verosimilitudes de escalas distintas (Tabla 3), lo que dificulta la lectura.

## 9. Conexión con mi tesis (red E20)

- **Es el antecedente más próximo en diseño** a mi comparación: retornos diarios de Bitcoin con validación cronológica, referente ingenuo explícito, ARMA-GARCH como referente econométrico y redes recurrentes. Su conclusión "la complejidad no ayuda; una RNN simple o un modelo econométrico parsimonioso bastan" coincide con mi hallazgo de que E20 empata con referentes simples.
- **Lección metodológica:** el referente debe ser retorno **cero** o media, no el retorno previo; mi plan usa referentes de media móvil de |retorno| y de proporción de subidas.
- **Pronósticos constantes:** el patrón de RMSE idéntico entre horizontes es el síntoma del colapso a la media que también aparece en el trabajo de Sánchez Zurdo (LSTM) de esta carpeta; en E20 debo comprobar que la lectura no se reduce a una constante.
- **ARMA-GARCH para magnitud:** el agrupamiento de volatilidad (retornos al cuadrado con Ljung-Box de 356) es la señal que mi modelo de "movimiento" explota; justifica la métrica de movimiento (|retorno| mayor o igual al percentil 33).
- **Límite para citarlo:** solo error de nivel (RMSE y MAE) sin dirección ni significancia estadística.

## 10. Referencias que cita y conviene localizar (DOI según el documento; verificar)

Alessandretti, ElBahrawy, Aiello y Baronchelli (2018), Complexity, 10.1155/2018/8983590; Gu, Kelly y Xiu (2020), "Empirical asset pricing via machine learning", Review of Financial Studies, 10.1093/rfs/hhaa009; Lahmiri y Bekiros (2019), Chaos, Solitons and Fractals, 10.1016/j.chaos.2018.11.014; Makridakis, Spiliotis y Assimakopoulos (2018), PLoS ONE 13(3):e0194889; McNally, Roche y Caton (2018), 10.1109/PDP2018.2018.00060; Hu, Parlour y Rajan (2019), Financial Management, 10.1111/fima.12300; Momtaz (2021), European Journal of Finance, 10.1080/1351847X.2019.1647259; Kraus, Feuerriegel y Oztekin (2020), European Journal of Operational Research, 10.1016/j.ejor.2019.09.018; Hochreiter y Schmidhuber (1997), Neural Computation, 10.1162/neco.1997.9.8.1735; Jang y Lee (2018), IEEE Access, 10.1109/ACCESS.2017.2779181; Phaladisailoed y Numnonda (2018), 10.1109/ICITEED.2018.8534911; Longo, Riccaboni y Rungi (2022), 10.1016/j.jedc.2021.104278. **Comprobar cada una con su DOI antes de citarla.**

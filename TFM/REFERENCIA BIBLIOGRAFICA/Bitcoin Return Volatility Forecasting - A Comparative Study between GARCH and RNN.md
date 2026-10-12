# Bitcoin Return Volatility Forecasting: A Comparative Study between GARCH and RNN

**Extracción de conocimiento: 2026-10-02.** Leído el texto completo (14 páginas de contenido; las páginas 15 y 16 son figuras del apéndice y la bibliografía final no se reprodujo). Páginas citadas = páginas del PDF.

## 1. Ficha bibliográfica

| Campo | Valor |
|---|---|
| Título exacto | Bitcoin Return Volatility Forecasting: A Comparative Study between GARCH and RNN |
| Autores | Ze Shen (Departamento de Economía Agrícola, Texas A&M), Qing Wan (Departamento de Ciencias de la Computación e Ingeniería, Texas A&M) y David J. Leatham (Texas A&M) |
| Tipo / revista / año | Artículo de revista: Journal of Risk and Financial Management 2021, 14(7), 337; recibido el 19 de abril de 2021, aceptado el 13 de julio de 2021, publicado el 20 de julio de 2021 |
| DOI | https://doi.org/10.3390/jrfm14070337 |
| Licencia | Acceso abierto, CC BY 4.0 (MDPI) |
| Archivo local | `jrfm-14-00337-v2.pdf` |
| Editores académicos | William Nganje y Xudong Rao |

## 2. Pregunta y aportes declarados (p. 2 y p. 3)

Compara, fuera de muestra, la **volatilidad** diaria de los retornos de Bitcoin y el **valor en riesgo (VaR)** pronosticados por un modelo ingenuo EWMA, un ARMA-GARCH y una red neuronal recurrente con celdas GRU. Cuatro aportes: (1) primer estudio de volatilidad de Bitcoin con RNN y celda GRU; (2) comparación directa de GARCH y RNN con una guía de cuándo usar cada uno; (3) además de precisión, evalúa la eficiencia del VaR; (4) aporta evidencia de las limitaciones del aprendizaje automático en economía.

**Resultado del resumen** (p. 1): la RNN supera a GARCH y EWMA en el desempeño medio de pronóstico (según MAE con el primer proxy), pero es menos eficiente captando eventos extremos y funciona mal en el VaR.

## 3. Datos

- **Fuente y periodo:** CoinMarketCap.com (accedido el 8 de julio de 2021), del 30 de abril de 2013 al 21 de mayo de 2021, **2 944 observaciones** (p. 4). Precios diarios de apertura, máximo, mínimo y cierre.
- **Retorno diario:** diferencia del logaritmo natural del precio de cierre, r_t = ln(p_t / p_{t−1}) (p. 4).
- **Estadísticos de los retornos** (Tabla 1, p. 4): media 0,000819; varianza 0,000343; desviación típica 0,018524 (1,85 %); asimetría −0,55305; curtosis 11,38964 (curtosis en exceso muestral 8,39 según p. 11).
- **Estacionariedad** (Tabla 2, p. 4): pruebas de Dickey y Fuller aumentada y de Phillips-Perron: −55,1 y −55,2 sin tendencia, −55,2 y −55,1 con tendencia, frente a valores críticos de −3,43 y −3,96 al 1 %: la serie de retornos es estacionaria.
- **Agrupamiento de volatilidad** (Tabla 3, p. 5): prueba Q de Ljung-Box de los retornos al cuadrado con valores p de 0,000496 (10 retardos), 0,000693 (15) y 0,000006 (20): hay heterocedasticidad condicional.
- **Particiones** (p. 7): dentro de muestra, 2 652 observaciones; fuera de muestra, **292 observaciones** del 3 de agosto de 2020 al 21 de mayo de 2021. (El texto escribe "30 de abril de 2010" para el inicio dentro de muestra, lo que no concuerda con los datos que empiezan en 2013.)

## 4. Fundamentos matemáticos

### 4.1 Estructura econométrica general (p. 5)

- r_t = μ_t + Z_t  (1)
- μ_t = E(r_t | F_{t−1})  (2)
- h_t² = Var(r_t | F_{t−1}) = E[(r_t − μ_t)² | F_{t−1}] = E[Z_t² | F_{t−1}]  (3)

con F_{t−1} la información pasada y h_t² la varianza condicional.

### 4.2 Media condicional ARMA(p,q) (p. 5)

μ_t = φ_0 + Σ_{i=1}^{p} φ_i · r_{t−i} + Σ_{j=1}^{q} θ_j · Z_{t−j}  (4). Los órdenes se eligen por AIC y BIC; resulta **ARMA(2,2)** (p. 7). Se contrasta el efecto ARCH en los residuos.

### 4.3 EWMA como referente (p. 5)

σ²_{t+1} = λ·σ²_t + (1 − λ)·r²_t  (5), con λ = 0,94 (RiskMetrics). No incluye media ni varianza condicional al estilo GARCH.

### 4.4 GARCH (p. 6)

- Z_t = h_t · ε_t, con {ε_t} i.i.d.(0, 1)  (6)
- h_t² = α_0 + Σ_{i=1}^{m} α_i · Z²_{t−i} + Σ_{j=1}^{n} β_j · h²_{t−j}  (7). (El texto escribe h²_{t−1} en el término de β, que es una errata evidente.)

Con la serie estandarizada de residuos del mejor ARMA-GARCH no debe quedar autocorrelación ni efecto ARCH (prueba ARCH LM).

### 4.5 Proxies de la volatilidad realizada (p. 8)

La volatilidad verdadera no es observable. Primer proxy: el **retorno diario al cuadrado**. Segundo proxy, estimador de **Garman y Klass (1980)**:

σ̂²_GK = 0,5·[ln(H_t / L_t)]² − [2·ln 2 − 1]·[ln(C_t / O_t)]²  (8)

con H, L, O, C el máximo, mínimo, apertura y cierre del día.

### 4.6 Valor en riesgo paramétrico con t de Student (p. 11)

- Definición: Pr(r_t ≤ VaR_t(α) | F_{t−1}) = α  (9), con α = 1 %, 2,5 % y 5 %.
- VaR_t(α) = E(r_t | F_{t−1}) + t^α_ν · σ_t · sqrt(ν/(ν − 2))  (10), tal como se lee en el texto extraído del PDF. **Revisar la fórmula en el original antes de citarla:** para una t estandarizada a varianza uno el factor habitual es sqrt((ν−2)/ν), el inverso de esta forma; el factor extraído podría estar invertido o el valor crítico t no estar estandarizado.
- Grados de libertad por método de momentos: ν̂ = 4 + 6/k̂, para ν > 4  (11), con k̂ la curtosis en exceso muestral. Con k̂ = 8,39 se obtiene **ν̂ = 4,72**; valores críticos t: −3,45 (1 %), −2,62 (2,5 %) y −2,04 (5 %).
- Para EWMA y RNN, que no modelan la media condicional, se toma E(r_t | F_{t−1}) = 0: VaR_t(α) = t^α_ν · σ_t · sqrt(ν/(ν−2))  (12) (misma observación sobre el factor).
- Cobertura fuera de muestra: α̂ = N(pérdidas > VaR_t(α)) / N(observaciones fuera de muestra)  (13). El mejor modelo es el de menor |α − α̂|.
- Retrocontrastes: prueba de cobertura incondicional de Kupiec (1995) y de cobertura condicional de Christoffersen (1998).

### 4.7 Red neuronal recurrente (secciones 2.2 y 3.1, p. 6 y p. 7)

- **Entrada:** series de 30 días de volatilidad para predecir 1, 5 y 10 días hacia adelante. Tupla 1: los primeros 30 días predicen el día 31; tupla 2: los días 2 a 31 predicen el 32; y así sucesivamente. Longitud total 2 031; **1 994 tuplas**; las primeras **1 794 (90 %)** para entrenamiento y las **200** restantes para prueba.
- **Codificación:** el rango de la volatilidad se divide en **250 intervalos** iguales y cada valor real se convierte en un vector de dimensión 250 (codificador de entrada). Las salidas se decodifican con un perceptrón multicapa.
- **Arquitectura:** dos capas de RNN con celdas **GRU**; la primera con **512 unidades** y la segunda con **256**. No incluye capa de incrustación ni de probabilidad. La función de coste se rediseña "basada en una función tangente".
- **Entrenamiento:** descenso de gradiente estocástico con barajado del conjunto, optimizador RMSProp, **tasa de aprendizaje 0,0001, lote 20, 1 000 épocas** sobre las 1 794 tuplas y evaluación en las 200 tuplas de prueba cada cinco épocas; GPU GTX 1070.
- **ARMA-GARCH:** parámetros estimados con **ventana móvil**; el modelo elegido es **ARMA(2,2)-GARCH(1,2)** (Tabla 4).

**Parámetros estimados dentro de muestra** (Tabla 4, p. 7): φ_0 = 0,001 (t 3,280); φ_1 = 1,424 (t 128,130); φ_2 = −0,434 (t −39,606); θ_1 = −1,458; θ_2 = 0,474; α_0 ≈ 0,000 (t 1,851; p = 0,064); α_1 = 0,191 (t 8,254); β_1 = 0,413 (t 2,965; p = 0,003); β_2 = 0,394 (t 3,120; p = 0,002). Se comprueba que no queda efecto ARCH en los residuos estandarizados.

## 5. Resultados completos

**Precisión de la volatilidad fuera de muestra** (Tabla 5, p. 9):

| Horizonte | Modelo | RMSE proxy 1 | RMSE proxy 2 | MAE proxy 1 | MAE proxy 2 |
|---|---|---|---|---|---|
| 1 día | EWMA | 2,4797e-6 | 4,5816e-4 | 3,1640e-4 | 3,8195e-3 |
| 1 día | GARCH | 2,4795e-6 | 4,5814e-4 | 3,3930e-4 | 3,7762e-3 |
| 1 día | RNN | 2,4985e-6 | 4,5818e-4 | 2,8091e-4 | 4,0179e-3 |
| 5 días | EWMA | 2,4969e-6 | 4,6213e-4 | 3,1742e-4 | 3,8721e-3 |
| 5 días | GARCH | 2,4760e-6 | 4,5814e-4 | 3,4605e-4 | 3,7607e-3 |
| 5 días | RNN | 2,5063e-6 | 4,5897e-4 | 2,8533e-4 | 4,0535e-3 |
| 10 días | EWMA | 2,4779e-6 | 4,5817e-4 | 3,2214e-4 | 3,8277e-3 |
| 10 días | GARCH | 2,4741e-6 | 4,5813e-4 | 3,5656e-4 | 3,7426e-3 |
| 10 días | RNN | 2,5065e-6 | 4,5897e-4 | 2,8426e-4 | 4,0480e-3 |

- **RMSE:** el GARCH es el mejor y la RNN el peor; con el proxy 1 el RMSE de la RNN a 1, 5 y 10 días es 0,76 %, 1,21 % y 1,29 % mayor que el del GARCH; con el proxy 2, 0,009 %, 0,18 % y 0,18 % mayor.
- **MAE:** con el proxy 1 la RNN tiene el menor MAE (el del GARCH es 17,21 %, 17,55 % y 20,28 % mayor); con el proxy 2 la RNN es 6,02 %, 7,22 % y 7,54 % peor que el GARCH.
- **Interpretación de los autores** (p. 9): la RNN capta mejor las tendencias y el agrupamiento de volatilidad (Figuras 4 y 5), pero **subestima la volatilidad** y genera más valores atípicos (peor RMSE). El proxy de Garman y Klass es menos volátil y funciona peor que el retorno al cuadrado.

**Cobertura del VaR fuera de muestra** (Tabla 6, p. 12), valor observado α̂ frente al nominal α:

| | α | EWMA | GARCH | RNN |
|---|---|---|---|---|
| 1 día | 1 % | 2,06 % | 2,06 % | **16,15 %** |
| 1 día | 2,5 % | 2,75 % | 2,75 % | 18,9 % |
| 1 día | 5 % | 4,47 % | 5,15 % | 23,37 % |
| 5 días | 1 % | 1,72 % | 2,06 % | 21,31 % |
| 5 días | 2,5 % | 3,44 % | 2,75 % | 25,43 % |
| 5 días | 5 % | 6,19 % | 4,47 % | 26,80 % |
| 10 días | 1 % | 1,72 % | 1,72 % | 18,90 % |
| 10 días | 2,5 % | 3,78 % | 2,41 % | 23,71 % |
| 10 días | 5 % | 5,16 % | 4,12 % | 28,18 % |

**Retrocontrastes** (Tabla 7, p. 13): valores p de Kupiec (LRuc) y Christoffersen (LRcc): para EWMA y GARCH ninguno rechaza (por ejemplo cuantil 0,99 a 1 día: 0,11 y 0,25); para la RNN **todos son 0,00**, es decir, rechaza la cobertura correcta en los tres horizontes y los tres niveles.

**Conclusiones de los autores** (p. 13 y p. 14): la RNN responde más rápido a los cambios de volatilidad pero subestima el riesgo; los modelos econométricos son superiores en condiciones extremas; el aprendizaje automático "es más adecuado para mercados menos volátiles"; para el capital de riesgo se recomiendan los modelos econométricos.

## 6. Limitaciones y críticas

- Declarado por los autores: el mercado de Bitcoin tiene un historial corto para un método que depende de la cantidad de datos; el aprendizaje automático es sensible a las fluctuaciones y puede sobrerreaccionar (p. 3).
- **[OPINIÓN]** **Un VaR con cobertura de 16 % a 28 % frente al 1 % al 5 % nominal no es un resultado "de la red" sino una señal de mala calibración de escala:** la RNN predice una volatilidad sistemáticamente demasiado baja (lo que los autores llaman subestimar). Falta una corrección de escala o un ajuste posterior; compararla así con GARCH en VaR favorece a GARCH.
- **[OPINIÓN]** Las diferencias de RMSE entre modelos son del orden de 0,01 % a 1,3 %; sin pruebas estadísticas de igualdad de precisión (Diebold y Mariano, conjunto de confianza) no puede afirmarse una diferencia real. Las cifras de RMSE con el proxy 1 son casi idénticas en los tres modelos.
- **[OPINIÓN]** La RNN usa una codificación de 250 intervalos y un coste "basado en tangente" sin detallar; el entrenamiento y la prueba comparten rango de normalización; una sola semilla, sin repeticiones.
- **[OPINIÓN]** Comparar con un EWMA con λ = 0,94 fijo es un referente razonable, pero no incluye HAR ni EWMA con λ ajustado.
- **[OPINIÓN]** Son 292 observaciones fuera de muestra (un solo periodo, agosto de 2020 a mayo de 2021, de alza fuerte); los resultados de cobertura con α = 1 % se basan en 2 a 3 excedencias.
- **[OPINIÓN]** La errata del periodo dentro de muestra (2010) y la fórmula (7) con h_{t−1} deben tenerse en cuenta si se cita.

## 7. Conexión con mi tesis (red E20)

- **Volatilidad como objetivo con señal:** coincide con mi hallazgo de que el movimiento (volatilidad) es lo que sí tiene algo de señal. Este trabajo prueba una red recurrente para ello y encuentra que **un modelo parsimonioso (GARCH/EWMA) es tan bueno o mejor**, igual que mi comparación con la media móvil de |retorno|.
- **EWMA como referente:** el EWMA con λ = 0,94 es el análogo clásico de mi media móvil exponencial de |retorno|; me da la ecuación y la justificación (RiskMetrics).
- **Calibración:** el VaR de la RNN muestra el riesgo de una salida mal escalada; en mi tesis debo comprobar calibración (puntuación de Brier, curvas de fiabilidad) además de AUC.
- **Línea de opciones (F4):** el pronóstico de volatilidad frente a la volatilidad implícita es el mismo tipo de problema; la conclusión de que los modelos econométricos son más robustos en extremos respalda mantener HAR/GARCH como referentes.
- **Límite para citarlo:** un solo periodo de prueba, una sola semilla y sin pruebas estadísticas.

## 8. Referencias que cita y conviene localizar

Engle (1982), ARCH; Bollerslev (1986), GARCH; Garman y Klass (1980), estimador de volatilidad; Kupiec (1995) y Christoffersen (1998), retrocontrastes de VaR; Andersen y Bollerslev (1998); Katsiampa (2017), "Volatility estimation for Bitcoin: A comparison of GARCH models"; Troster, Tiwari, Shahbaz y Macedo (2019), GAS y GARCH en Bitcoin; Bouoiyour y Selmi (2015, 2016); Balcilar y otros (2017); Alessandretti y otros (2018); Rebane y otros (2018), Seq2Seq para el precio de Bitcoin; Athey (2019), aprendizaje automático y economía; Fang y otros (2021), revisión de criptomonedas. **Comprobar cada una con su DOI antes de citarla.**

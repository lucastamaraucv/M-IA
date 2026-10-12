# Modelos de predicción estocástica para Bitcoin: una evaluación de métodos y desempeño

**Extracción de conocimiento: 2026-10-02** (leídas las páginas 1 a 9, 13 a 16, 26 a 58 de 63; **no leídas** las páginas 17 a 25, de teoría de modelos y de métricas)

| Campo | Valor |
|---|---|
| Título exacto | Modelos de predicción estocástica para Bitcoin: una evaluación de métodos y desempeño (título en inglés: Stochastic Prediction Models for Bitcoin: An Assessment of Methods and Performance) |
| Autores | Caroline Hernández Hernández y Juan Sebastián Forero Criollo; asesor: Alejandro Cadavid Gil |
| Tipo / Venue / Año | Trabajo de grado para optar al título de magíster en Administración Financiera, Universidad EAFIT, Escuela de Economía y Finanzas, Bogotá, 2023 (el nombre del archivo indica 2024) |
| Archivo local | `Caroline_HernandezHernandez_JuanSebastian_ForeroCriollo_2024.pdf` |
| URL / DOI | SIN DOI en el documento (repositorio institucional de EAFIT; **comprobar el enlace del repositorio antes de citarlo**) |
| Métodos | SVR, LSTM, GRU, árbol de decisión, bosque aleatorio y XGBoost, primero sin optimizar y luego con regularización L1-L2, dropout, validación cruzada, validación cruzada anidada, búsqueda en cuadrícula y aleatoria, optimización bayesiana, optuna y genética |
| Datos | Cierre diario de BTC de Yahoo Finance del 19 de septiembre de 2014 al 30 de septiembre de 2023 (p. 27 y p. 33) |

## Aporte clave

Compara seis modelos de ML y aprendizaje profundo para predecir el **precio de cierre** de Bitcoin y concluye que XGBoost con ajuste iterativo, optimización bayesiana y validación cruzada anidada es el mejor, con RMSE de 30,45 dólares, MAPE de 0,09 % y R² de 1,0 (p. 5, p. 47 y p. 55). Es un ejemplo útil en español de **un trabajo de máster en finanzas con resultados casi perfectos que probablemente no son confiables**, y por tanto sirve para ilustrar lo que mi tesis debe evitar.

## Hallazgos cuantitativos (HECHO, con página)

- **Modelos sin optimizar** (p. 35 a 45): LSTM RMSE 1 130,95 dólares y MAPE 2,74 %; GRU 1 322,42 y 3,89 %; SVR 2 963 y 11,07 %; árbol de decisión 4 868,40 y 15,84 % (R² 0,69); **bosque aleatorio 205,10 y 0,54 % con R², CCC y EVS de 1,00**; XGBoost 1 836,92 y 5,22 %.
- **Modelos optimizados** (Tabla 1, p. 46 a 48): 30 combinaciones. El mejor, XGBoost con ajuste iterativo, optimización bayesiana y validación cruzada anidada, RMSE 30,45 y MAPE 0,09 % (fila 18). Otras configuraciones de XGBoost dan RMSE de 1 163 a 1 980 (filas 22 a 28), de modo que la misma familia de modelos oscila entre 30 y 2 000 dólares según la técnica.
- **Resultados extremos del mismo estudio:** una GRU con optimización genética llega a RMSE de 266 033 214 (fila 5); un LSTM con regularización L2 da MAPE de 61,68 % (fila 14).
- **Mejoras reportadas por la optimización** (p. 55): GRU, 74,1 % en RMSE; SVR, 60 %; XGBoost, 98,3 %; bosque aleatorio, sin mejora.
- **Comparación con otros trabajos citados:** se cita a Khan y otros (2023, RMSE de 1 084 con LSTM y 1 200 con GRU) y a Liao (2023, XGBoost con RMSE de 391,3 y R² de 0,94) (p. 14, p. 55 y p. 56).
- **Duración del trabajo:** de mayo a julio de 2023, con unos 90 días de cómputo para las redes (p. 33).

## Limitaciones y críticas

- Declarado por los autores: calidad de datos limitada a la fuente, rangos de búsqueda de hiperparámetros acotados y poca capacidad computacional (p. 32). Piden más validación para descartar sobreajuste (p. 45).
- **[OPINIÓN]** **Los resultados casi perfectos son una señal de alerta, no de éxito.** Un RMSE de 30 dólares y un MAPE de 0,09 % sobre un precio que puede moverse cientos de dólares al día, y un R² de 1,00 en bosque aleatorio sin optimizar, son muy improbables para predicción real. La causa más probable es una fuga de información: el documento **no describe la partición de entrenamiento y prueba** (si es cronológica o aleatoria) ni qué variables entran, y habla de "ingeniería de características" sin detalle (p. 28). Esto debe confirmarse en el repositorio.
- **[OPINIÓN]** Afirma que la validación cruzada "aborda la autocorrelación" al evaluar en conjuntos independientes (p. 27). Eso es incorrecto para series temporales si los pliegues son aleatorios: mezcla pasado y futuro. Es el error que Baquero (2026) incluye entre los estándares incumplidos.
- **[OPINIÓN]** **No hay referente ingenuo** (precio de ayer) ni prueba estadística. Como orden de magnitud, mi cálculo propio del método ingenuo (precio de ayer) en julio de 2023 a octubre de 2025 da un MAPE de 1,71 % (ver el resumen de Walugembe y otros); el periodo de prueba de este trabajo no se especifica, así que la cifra es solo indicativa. Aun así, modelos con MAPE de 0,09 % o 0,54 % serían muy superiores a repetir el precio de ayer, lo cual no es creíble sin una explicación.
- **[OPINIÓN]** Predice el nivel del precio, no el retorno ni la dirección; el R² del nivel es trivialmente alto en una serie persistente.
- **[OPINIÓN]** **Inconsistencias internas:** en las conclusiones (p. 54) se atribuye al bosque aleatorio un MAPE de 5,22 %, que es el de XGBoost según la p. 45; y se dice que el bosque aleatorio "no presentó mejoras" mientras la Tabla 1 muestra que sus versiones optimizadas empeoran (RMSE de 367 a 579 frente a 205).
- **[OPINIÓN]** **Referencias que no pude verificar y que parecen dudosas:** el texto cita estudios con autores genéricos ("Smith, 2023", "Smith y Doe, 2010") y presenta resultados atribuidos a Nature Communications 2021 (Ganatra y otros) e IEEE Transactions on Neural Networks and Learning Systems 2022 (Nguyen y otros) con RMSE casi idénticos al suyo (209,28 y 206,17 frente a 205,10) (p. 43). **No cites ninguna de esas referencias sin abrir su DOI.**

## Conexión con mi tesis (red E20)

- **Contraejemplo útil para el capítulo de metodología:** muestra cómo se llega a "R² = 1" con una mala partición, optimización sobre los mismos datos de prueba y sin referente ingenuo. Contrasta con mi diseño (bloque final intocable, lectura fijada antes de ver el test, semillas múltiples).
- **Estado del arte en español:** es un ejemplo de TFM latinoamericano en Bitcoin con modelos de ML; sirve para situar el trabajo, siempre con la advertencia anterior.
- **Estructura de trabajo de máster:** el índice (objetivos, marco teórico, diseño metodológico, resultados, conclusiones y recomendaciones) puede servir de referencia de estructura, aunque la guía de la VIU manda.
- **Datos y fuente:** usa Yahoo Finance diario; yo uso una serie diaria fija versionada de CryptoCompare y datos de Binance para escalas menores.
- **Límite para citarlo:** no es una fuente fiable de resultados; úsalo como ejemplo de un enfoque, no como evidencia de rendimiento.

## Referencias que cita y conviene localizar (con cautela)

Khan y colaboradores (2023), LSTM y GRU para Bitcoin (RMSE 1 084 y 1 200); Liao (2023), XGBoost con indicadores técnicos; Khosravi y Ghazani (2022), método de triple barrera; Aljadani (2022), "DLCP2F: a DL-based cryptocurrency price prediction framework" (Discover Artificial Intelligence, 10.1007/s44163-022-00036-2); Byzkrovnyi y colaboradores (2022), arXiv:2205.08992; Bergstra y Bengio (2012), búsqueda aleatoria de hiperparámetros (JMLR); Cawley y Talbot (2010), sobreajuste en la selección de modelos (JMLR); Kohavi (1995), validación cruzada. **Comprobar cada una con su DOI antes de citarla; varias del texto tienen datos bibliográficos aproximados.**


---

# ANEXO TÉCNICO COMPLETO (datos, métodos, fundamentos matemáticos y tablas)

Contenido técnico de las páginas 1 a 57 del PDF (las páginas 17 a 25 que la ficha anterior marcaba como "no leídas" ya se incluyen aquí; las páginas 58 a 63 son la bibliografía). Trabajo de grado de maestría (EAFIT, Bogotá, 2023, mayo a julio de 2023 de ejecución). Páginas = páginas del PDF.

## A1. Pregunta, datos y diseño (p. 7 a 11, p. 26 a 33)

- **Objetivo declarado:** evaluar modelos "estocásticos" de aprendizaje automático para predecir el **precio de cierre del día siguiente** (Next Day-Close Price) del BTC (objetivo específico 2, p. 11).
- **Datos:** cierre diario de Yahoo Finance del **19 de septiembre de 2014 al 30 de septiembre de 2023** (archivo CSV); limpieza (atípicos, nulos y faltantes), **normalización** (para SVR y redes) e "ingeniería de características" **sin detalle** (qué variables, cuántos retardos); **no se describe la partición entrenamiento/prueba** (si es cronológica o aleatoria, ni su proporción) ni la ventana de entrada.
- **Declaración metodológica (p. 26 y p. 27):** "evitamos la implementación de técnicas específicas de transformación de datos para abordar la heterocedasticidad, multicolinealidad o autocorrelación", con el argumento de que el escalado, la normalización, la optimización de hiperparámetros y la validación cruzada las contrarrestan; se dice que "la validación cruzada aborda la autocorrelación al evaluar el rendimiento del modelo en conjuntos de datos independientes" (afirmación que **no es válida** para series temporales si los pliegues no respetan el orden).
- **Modelos** (4.2): LSTM (Hochreiter y Schmidhuber, 1997), GRU (Cho y otros, 2014), SVR (Hastie y otros, 2009), árbol de decisión, bosque aleatorio (Ho, 1995) y XGBoost (Chen y Guestrin, 2016); la descripción teórica es cualitativa (sin ecuaciones de las celdas). Se afirma que las GRU "pueden ser menos precisas que las RNN tradicionales en tareas con memoria a largo plazo" (Cho y otros, 2014).
- **Software:** Python, TPOT, Scikit-Learn y TensorFlow; unos 90 días de cómputo para las redes por limitaciones de capacidad.

## A2. Métricas y ecuaciones (p. 20 a 25)

- **R²** = 1 − Σ(A_t − F_t)² / Σ(A_t − Ā)²  (ecuación 1), con A_t el real, F_t el pronóstico y Ā el promedio de los reales. **Sobre niveles de precio, un R² cercano a 1 es trivial** en una serie persistente (se mide frente a la media, no frente al precio de ayer).
- **RMSE** = sqrt( (1/n)·Σ(A_t − F_t)² )  (ecuación 2).
- **MAPE** = (1/n)·Σ( (A_t − F_t)/A_t )  (ecuación 3; **como figura en el texto no lleva valor absoluto ni el factor 100**, es una fórmula incorrecta del MAPE).
- **Coeficiente de concordancia de Lin (CCC)** = (2·P₀ − 1)/(P₀ + P_e − 1)  (ecuación 4, tal como se imprime; la definición estándar de Lin es 2ρσ_xσ_y/(σ_x² + σ_y² + (μ_x − μ_y)²); la expresión impresa **no coincide** con la de Lin).
- **Puntaje de varianza explicada (EVS)** = 1 − Var(y − ŷ)/Var(y)  (ecuación 5); mide la varianza explicada ignorando el sesgo (por eso puede ser alto con R² bajo).
- También se menciona el NMSE entre los indicadores iniciales (p. 30) y se descartan los indicadores de clasificación (se predice un valor continuo).

## A3. Técnicas de optimización (p. 30 a 32)

Validación cruzada (Kohavi, 1995) y **validación cruzada anidada**; regularización **L1 y L2** (Zou y Hastie, 2005); **dropout** (Srivastava y otros, 2014); ajuste de la tasa de aprendizaje; **optimización bayesiana**; ajuste automático de hiperparámetros; **ensamble de modelos**; núcleo y parámetros C y gamma (SVR); **búsqueda en cuadrícula**; **optimización genética**; **búsqueda aleatoria**; **optimización por gradientes**; Optuna. "No todas las técnicas fueron aplicadas de manera uniforme a cada modelo" (p. 46). **Los rangos de búsqueda, el número de iteraciones, el número de pliegues y el criterio de selección no se informan.**

## A4. Resultados completos

**Modelos sin optimizar (p. 34 a 45):**

| Modelo | RMSE (USD) | MAPE (%) | R² | EVS | CCC |
|---|---|---|---|---|---|
| LSTM | 1 130,95 | 2,74 | 0,9827 | 0,9869 | 0,9918 |
| GRU | 1 322,42 | 3,89 | 0,975 | 0,9875 | 0,9894 |
| SVR | 2 963,31 | 11,07 | 0,8743 | 0,9627 | 0,9335 |
| Árbol de decisión | 4 868,40 | 15,84 | 0,69 | 0,80 | 0,46 |
| **Bosque aleatorio** | **205,10** | **0,54** | **1,00** | **1,00** | **1,00** |
| XGBoost | 1 836,92 | 5,22 | 0,96 | 0,96 | 0,98 |

Comparaciones citadas: LSTM 13 % por encima del RMSE de Khan y otros (2023) y GRU 10 % por encima (RMSE de 1 084 y 1 200); bosque aleatorio comparable a "Ganatra y otros (2021, Nature Communications)" con RMSE 209,28 y MAPE 0,55 % y a "Nguyen y otros (2022, IEEE TNNLS)" con 206,17 y 0,54 % (referencias no verificadas); XGBoost frente a Ma y otros (2022) con EVS 0,9547 y Ding y otros (2023) con MAPE 2,2 %. Los autores advierten que hay que comprobar el sobreajuste.

**Tabla 1: 30 configuraciones optimizadas (p. 46 a 48)** (RMSE en USD / MAPE / R² / EVS / CCC):

| N.º | Modelo y técnica | RMSE | MAPE | R² | EVS | CCC |
|---|---|---|---|---|---|---|
| 1 | GRU, ajuste, L1-L2 | 1 557,67 | 3,98 % | 0,96 | 0,95 | 0,68 |
| 2 | GRU, ajuste, dropout y tasa de aprendizaje | 1 971,29 | 5,95 % | 0,94 | 0,89 | 0,69 |
| 3 | GRU, ajuste, aleatorio | 885,13 | 2,07 % | 0,98 | 0,95 | 0,96 |
| 4 | GRU, ajuste, bayesiana | 927,59 | 2,40 % | 0,97 | 0,87 | 0,91 |
| 5 | GRU, ajuste, genética | 266 033 214 | 12,5 % | 0,62 | 0,59 | 0,52 |
| 6 | GRU, ajuste, Optuna | 858,51 | 1,98 % | 0,99 | 0,91 | 0,58 |
| 7 | GRU, ajuste, Adam y ensamble | 892,41 | 2,11 % | 0,98 | 0,93 | 0,21 |
| 8 | GRU, ajuste, validación cruzada y ensamble | 342,32 | 1,98 % | 0,99 | 0,97 | 0,92 |
| 9 | SVR, ajuste, núcleo, C y gamma | 3 542,51 | 13,76 % | 0,77 | 0,61 | 0,38 |
| 10 | SVR, genética | 3 478,87 | 14,98 % | 0,76 | 0,65 | 0,41 |
| 11 | SVR, validación cruzada y curvas de aprendizaje | 2 963,54 | 11,07 % | 0,87 | 0,86 | 0,73 |
| 12 | SVR, ajuste, validación cruzada | 1 156,87 (el texto de la p. 50 dice 2 156,87) | 8,67 % | 0,82 | 0,52 | 0,58 |
| 13 | LSTM, ajuste, parada temprana | 2 279,51 | 5,17 % | 0,93 | 0,95 | 0,92 |
| 14 | LSTM, regularización L2 | 13 867,43 | 61,68 % | 0,40 | 0,38 | 0,15 |
| 15 | LSTM, ajuste, capas adicionales y dropout | 1 691,78 | 3,64 % | 0,96 | 0,79 | 0,77 |
| 16 | XGBoost, ajuste, bayesiana | 1 207,41 | 3,73 % | 0,98 | 0,98 | 0,99 |
| 17 | XGBoost, ajuste iterativo, bayesiana | 404,34 | 1,52 % | 1,00 | 1,00 | 1,00 |
| **18** | **XGBoost, ajuste iterativo, bayesiana, validación cruzada anidada** | **30,45** | **0,09 %** | 1,00 | 1,00 | 1,00 |
| 19 | XGBoost, ajuste, genética | 374,21 | 0,87 % | 1,00 | 1,00 | 1,00 |
| 20 | XGBoost, ajuste iterativo, genética | 325,88 | 1,04 % | 1,00 | 1,00 | 1,00 |
| 21 | XGBoost, ajuste iterativo, genética, validación cruzada anidada | 323,09 | 1,08 % | 1,00 | 1,00 | 1,00 |
| 22 | XGBoost, ajuste, gradientes | 1 165,63 | 3,48 % | 0,98 | 0,98 | 0,98 |
| 23 | XGBoost, ajuste iterativo, gradientes | 475,56 | 2,37 % | 1,00 | 1,00 | 1,00 |
| 24 | XGBoost, ajuste iterativo, gradientes, validación cruzada anidada | 1 163,78 | 3,50 % | 0,98 | 0,98 | 0,38 |
| 25 | XGBoost, ajuste, cuadrícula | 1 959,76 | 5,43 % | 0,95 | 0,96 | 0,19 |
| 26 | XGBoost, cuadrícula, validación cruzada anidada | 2 078,58 | 5,76 % | 0,94 | 0,95 | 0,19 |
| 27 | XGBoost, ajuste, búsqueda aleatoria | 1 959,76 | 5,43 % | 0,95 | 0,96 | 0,19 |
| 28 | XGBoost, búsqueda aleatoria, validación cruzada anidada | 1 980,26 | 5,45 % | 0,95 | 0,96 | 0,20 |
| 29 | Bosque aleatorio, L2, validación cruzada | 367,61 | 1,78 % | 0,95 | 0,87 | 0,97 |
| 30 | Bosque aleatorio, ajuste de hiperparámetros | 578,87 | 2,07 % | 0,91 | 0,95 | 0,96 |

(Los valores de las columnas R² y EVS salen juntos en el PDF; el orden R² y luego EVS es el de los encabezados de la tabla; la columna CCC es la última.)

**Conclusiones del texto (p. 54 a 57):** mejoras por la optimización respecto al modelo no optimizado: GRU 74,1 % en RMSE y 48,9 % en MAPE (fila 8); SVR 60 % en RMSE y 21 % en MAPE; XGBoost 98,3 % y 98,2 % (fila 18); bosque aleatorio sin mejora (las versiones optimizadas empeoran: RMSE 367,61 y 578,87 frente a 205,10). Se elige el XGBoost de la fila 18 (RMSE 30,45; MAPE 0,09 %; R², CCC y EVS = 1,00), comparado con Liao (2023, XGBoost con RMSE 391,3 y R² 0,94). Recomendaciones: optimización por enjambre de partículas o teoría de juegos, eventos externos, volumen y otros indicadores.

## A5. Revisión de antecedentes citados (p. 13 a 15)

Khosravi y Ghazani (2022): preprocesamiento con triple barrera y precisión media decreciente, MAPE 7,7 % y RMSE 3 670,24; Khurana y otros (2023): TPOT frente a AutoSklearn en 30 min, 1 h y 4 h; Kazeminia y otros (2023): 2D-CNN-LSTM para el cierre del día siguiente (mejor que CNN, LSTM y GRU) y detección de regímenes con ARIMA, LSTM y CNN (R² 0,98166 y MAPE 3,4 %; ARIMA R² 0,78987 y MAPE 14,5 %); Siyi Liao (2023): XGBoost con indicadores técnicos, RMSE 391,3 y R² 0,94; Aljadani (2022): marco de cinco fases, GRU supera a BiLSTM en BTC, Ethereum y Cardano; Byzkrovnyi y otros (2022): Ethereum, XGBoost RMSE 295,41; Saad y otros (2020): precisión 95 %; Li y otros (2019): redes bayesianas, MAPE 4 %, SVR deficiente; Parekh (2022): DL-GuesS, MAPE 4,79 %.

## A6. Lectura crítica adicional (se suma a la ficha anterior)

1. **Fórmulas defectuosas:** el MAPE impreso no tiene valor absoluto, el CCC impreso no es el de Lin y el EVS se imprime sin cuadrados; los valores numéricos pueden venir de bibliotecas, pero la presentación es incorrecta.
2. **La mejor configuración se escoge entre 30 corridas evaluadas sobre el mismo conjunto de prueba**, sin corrección por pruebas múltiples (Bailey y otros, 2014) y sin partición de validación separada informada.
3. **Rango del error:** la misma familia (XGBoost) va de 30 USD (fila 18) a 2 078 USD (fila 26) según la técnica, y filas 25 y 27 dan resultados idénticos (1 959,76 y 5,43 %), lo que sugiere la misma búsqueda con otro nombre.
4. **Resultados "perfectos" del bosque aleatorio sin ajuste (R² = 1,00) y de XGBoost con R² = 1,00** son señales de fuga de información o de predicción del nivel con características que incluyen el valor mismo (ver ficha); un modelo que predijera el precio de mañana con 0,09 % de error sería una máquina de hacer dinero.
5. Sin referente ingenuo, sin prueba de Diebold y Mariano, sin costes, sin análisis de dirección.

# Echo State Networks for Bitcoin Time Series Prediction

**Extracción de conocimiento: 2026-10-02** (leído el texto completo de las 13 páginas de contenido; las 2 últimas son bibliografía)

| Campo | Valor |
|---|---|
| Título exacto | Echo State Networks for Bitcoin Time Series Prediction |
| Autores | Mansi Sharma (DFKI, Alemania), Enrico Sartor (Politecnico di Milano), Marc Cavazza (Universidad de Stirling) y Helmut Prendinger (Instituto Nacional de Informática, Japón) |
| Tipo / Venue / Año | Preprint, arXiv:2508.05416v1 [cs.LG], 7 de agosto de 2025 |
| Archivo local | `2508.05416v1.pdf` |
| URL / DOI | arXiv:2508.05416 (sin DOI de revista en el documento) |
| Métodos | Red de estado de eco (ESN) con la biblioteca reservoirpy y optimización bayesiana (TPE, hyperopt); comparada con XGBoost y el método ingenuo "último valor"; exponente máximo de Lyapunov (algoritmo de Rosenstein) para medir caos por ventana |
| Datos | Bitcoin/USDT diario de Binance, del 17 de agosto de 2017 al 24 de enero de 2023; huecos rellenados por interpolación lineal (p. 4) |

## Aporte clave

Es el antecedente **más cercano a mi tesis en el activo** (Bitcoin con reservorio). Los autores afirman que una ESN con ajuste fino de hiperparámetros predice el precio de cierre del día siguiente con un error mucho menor que XGBoost y que el método ingenuo, y que la ventaja es mayor en periodos más caóticos según el exponente de Lyapunov (p. 1 y p. 12).

## Hallazgos cuantitativos (HECHO, con página)

- **Objetivo:** el precio de cierre en dólares del día siguiente (nivel del precio, no retorno ni dirección). Los autores dicen que los retornos y log-retornos eran más difíciles de predecir y los descartaron (p. 4 y p. 5).
- **Diferenciación fraccionaria** de orden 0,8 para acercarse a la estacionariedad (prueba de Dickey y Fuller aumentada), conservando memoria; aun así la serie sigue siendo no estacionaria en momentos superiores (p. 5).
- **Variables de la versión multivariante:** medias móviles de 3 y 7 días, desviación típica a 7 días, diferencias alto-bajo y cierre-apertura, razón del último cierre sobre la media de 7 días, pendientes de regresión sobre los últimos 7 y 14 cierres, RSI de 7 días y MACD 7-21 (p. 8).
- **Evaluación:** validación de ventana móvil con entrenamiento de 15, 30 y 60 puntos, prueba de 10 puntos y paso 1; métrica RMSE en dólares (p. 8).
- **RMSE medio, versión univariante** (Tabla 3, p. 11), con ventanas de 15, 30 y 60 días: XGBoost 740,43, 741,84 y 675,95; **ESN 442,78, 463,96 y 427,35**; método ingenuo 736,60, 751,18 y 787,02.
- **RMSE medio, versión multivariante** (Tabla 3, p. 11): XGBoost 678,59, 676,60 y 572,58; ESN 487,77, 533,43 y 441,23; ingenuo 713,53, 749,96 y 665,62.
- **En porcentaje del precio:** el RMSE de la ESN va de 1,0 % a 2,7 % del precio de cierre, con promedio de 1,8 % (p. 10).
- **Modelos estadísticos clásicos** (ARIMA, suavizado exponencial, regresiones): RMSE de 800 a 2 000, claramente peores (p. 9).
- **Hiperparámetros ajustados** (Tabla 1, p. 7): tamaño del reservorio de 50 a 250 neuronas; radio espectral, tasa de fuga, regularización de la salida y ruidos en escala logarítmica; escala de entrada, de sesgo, de realimentación y dispersión en escala uniforme; semilla fija 2023.
- **Análisis de caos:** se calcula el exponente máximo de Lyapunov por ventana y el cociente entre el RMSE de la ESN y el de XGBoost (EXratio). Con una prueba U de Mann-Whitney (5 %) se encuentra diferencia significativa entre ventanas de alto y bajo caos para ventanas de 30 y 60 días, pero **no para 15 días** (p. 12). Los autores atribuyen la falta de significancia a que 15 puntos no bastan para estimar bien Lyapunov.

## Limitaciones y críticas

- Declarado por los autores: ventanas cortas de entrenamiento que pueden no capturar tendencias largas ni estacionalidad; falta la predicción a varios pasos (p. 13).
- **[OPINIÓN]** **Predecir el nivel del precio no es predecir la dirección.** Un error de 442 dólares frente a 737 del método ingenuo parece una reducción grande (alrededor del 40 %); es mucho mayor que lo que sugiere la literatura de eficiencia de mercado y que mis resultados en BTC real (acierto de dirección diario cercano a 51 %). Hace falta una réplica independiente.
- **[OPINIÓN]** No se describe si la optimización bayesiana de hiperparámetros se hizo con datos que luego sirvieron para evaluar (posible fuga de información de la selección). Se usa una sola semilla (2023) y no se da la variabilidad entre semillas.
- **[OPINIÓN]** No se informa de acierto de dirección, de intervalos de confianza ni de una prueba estadística de la diferencia entre ESN y XGBoost en el RMSE medio; las pruebas solo se hacen sobre el cociente en el análisis de caos.
- **[OPINIÓN]** La conclusión de que el resultado "desafía la hipótesis del mercado eficiente" (p. 13) no está respaldada: un menor RMSE del nivel del precio no demuestra rentabilidad ni predicción de signo, y no se consideran costes.
- **[OPINIÓN]** Estimar el exponente de Lyapunov con 30 o 60 puntos es poco fiable; el propio texto lo reconoce para 15.
- **[OPINIÓN]** Los datos de entrada están sin normalizar (p. 4), cosa poco habitual para una red con tanh.

## Conexión con mi tesis (red E20)

- **Antecedente directo en el activo:** reservorio con lectura lineal predice Bitcoin y se compara con XGBoost y un referente ingenuo, igual que mi diseño.
- **Contraste con mis resultados:** yo uso retorno y movimiento (no nivel de precio), validación cronológica con bloque final y varias semillas, y encuentro que E20 empata con referentes simples. Mi tesis puede presentar este trabajo como un resultado optimista que **no se replica** con el objetivo y el protocolo que yo uso, y proponer una réplica con retornos.
- **Aviso metodológico para mi capítulo:** muestra los riesgos de comparar con el método ingenuo en niveles de precio, de ajustar hiperparámetros sin separar la validación y de afirmar eficiencia de mercado sin prueba direccional.
- **Caos y predictibilidad:** conecta con el estudio de caos en Bitcoin que el proyecto ya había resumido (Gezer); mi hallazgo de que BTC no tiene caos detectable en mis escalas pone en duda la lectura de que "más caos, mejor ESN".
- **Referencias de apoyo para el estado del arte:** menciona a Lin y otros (2009), Dan y otros (2020) y Kenny (2020, único estudio previo de ESN en criptomonedas, "sin ajuste exhaustivo").

## Referencias que cita y conviene localizar

Jaeger (2001, 2007), ESN; Lin, Yang y Song (2009), predicción bursátil con ESN; Dan y otros (modelo ESN determinista en bolsas china y S&P 500); Kenny (2020), ESN en criptomonedas; Jaquart, Dann y Weinhardt (2021), predicción de Bitcoin a corto plazo con aprendizaje automático; Alessandretti y otros (2018), XGBoost y LSTM en criptomonedas; Urquhart (2016), Nadarajah y Chu (2017) y Bariviera (2017), eficiencia de Bitcoin; Rosenstein, Collins y De Luca (1993), algoritmo para el exponente de Lyapunov; Makridakis y otros (2018), comparación de métodos estadísticos y de ML; Peters (1994), hipótesis del mercado fractal. **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (datos, métodos, fundamentos matemáticos y tablas)

Contenido técnico íntegro del texto principal (páginas 1 a 13 del PDF; el resto son referencias). Páginas = páginas del PDF.

## A1. Datos (p. 4 y p. 5)

- **Serie:** Bitcoin diario en dólares (BTCUSDT) de la plataforma **Binance**, del **17 de agosto de 2017 al 24 de enero de 2023**; apertura, cierre, máximo y mínimo. Valores faltantes por interpolación lineal.
- **Sin transformaciones:** no se estandariza ni se pasa a retornos; los autores indican que en pruebas preliminares los retornos y log-retornos, pese a ser estacionarios, "presentan mayor varianza y son más difíciles de predecir". **El objetivo es el precio de cierre del día siguiente (nivel de precio, no retorno).**
- **Frecuencia:** se usa diaria porque "los resultados eran casi independientes de la frecuencia", lo que enlazan con la **hipótesis del mercado fractal** (Peters).
- **No estacionariedad** (Figuras 1 y 2): tendencias lineal y exponencial (a finales de 2020), cambios abruptos (inicio de 2021), heterocedasticidad y distribución asimétrica de colas gruesas. Diferenciación fraccionaria (como en López de Prado) para hallar el orden mínimo que hace estacionaria la serie con la prueba de Dickey-Fuller aumentada: **orden 0,8**; aun así sigue siendo no estacionaria en momentos superiores.

## A2. Fundamentos matemáticos

### A2.1 Red de estado de eco (ESN, p. 5 y p. 6)
- Dinámica: x̃(k) = tanh( W_in·u(k) + W_x·x(k−1) )  (ecuación 1)
- Estado y salida: y(k) = W_out·( α·x̃(k) + (1 − α)·x(k−1) )  (ecuación 2), con α la tasa de fuga; u(k) la entrada, x(k) el estado del reservorio, W_in y W_x fijos y aleatorios.
- **Única parte entrenada: W_out** por regresión lineal: y = Φ·W_out + ε_y  (3), con Φ = [x(k), …, x(k+N−1)]ᵀ  (4) y y = [y(k), …, y(k+N−1)]ᵀ  (5); k se fija para descartar el transitorio inicial; ε gaussiano de media cero y varianza β; N = número de muestras de entrenamiento.
- Implementación: biblioteca **reservoirpy**; hiperparámetros inspirados en Lukoševičius.

### A2.2 Exponente máximo de Lyapunov (p. 6 y p. 7)
- Algoritmo de **Rosenstein** (1993): λ_max > 0 caos fuerte; 0 ciclo límite o cuasi-periódico; < 0 punto fijo.
- Sistema dx/dt = F(x)  (6); variación en el espacio tangente dδx/dt = (∂F/∂x)·δx  (7); solución δx(t) = A_t·δx(0)  (8), con A_t = exp(∫ ∂F/∂x dt); tasa media de divergencia λ[x(0), δx(0)] = lim_{t→∞} (1/t)·ln| δx(t)/δx(0) |  (9); λ_i = λ[x(0), e_i]  (10) con e_i la base m-dimensional; λ_max = λ_1.

### A2.3 Métrica (p. 8)
- **RMSE** = sqrt( (1/n)·Σ (y_t − ŷ_t)² )  (11), siempre sobre un conjunto de prueba de **10 días** y **en dólares**.

## A3. Procedimiento (p. 7 a 9)

- **Variables multivariantes** (técnicas, elegidas por criterio experto): medias móviles de 3 y 7 días del cierre; desviación estándar de 7 días; diferencia máximo−mínimo; diferencia cierre−apertura; razón del último cierre sobre la media de 7 días; coeficientes de tendencia de la recta de regresión sobre los últimos 7 y 14 cierres; RSI de 7 días; MACD de 7-21.
- **Validación:** ventana móvil de entrenamiento fijo de **15, 30 y 60 puntos**, prueba de **10 puntos**, paso 1.
- **Búsqueda de hiperparámetros:** optimización bayesiana (estimadores de Parzen en árbol, TPE) con `hyperopt`.
  - **ESN (Tabla 1):** tamaño del reservorio 50 a 250 (paso 50); radio espectral, tasa de fuga, regularización de salida, ruido del reservorio, de entrada y de realimentación (log-uniformes en rangos de 10⁻⁷ a 10⁻⁶/10⁻⁴ y de 0,1 a 1/10); escala de entrada, de sesgo, de realimentación y dispersión (uniformes 0,05/0,8 a 0,5/1, paso 0,1); ruido gaussiano; semilla 2023.
  - **XGBoost (Tabla 2):** estimadores 100 a 300 (paso 100); profundidad 3 a 15; gamma 10⁻⁴ a 10; tasa de aprendizaje 0,01 a 0,3; muestra de columnas por árbol 0,5 a 1; peso mínimo del hijo 0 a 10; submuestra 0,8 a 1; semilla 2023.
- **Referentes:** valor anterior (método ingenuo: el precio actual como predicción del siguiente) y XGBoost (aproximación de Taylor de segundo orden). ARIMA, suavizado exponencial, modelos lineales generalizados, regresión de Huber y mínimos cuadrados ponderados dieron RMSE de 800 a 2 000 y no se reportan.

## A4. Resultados

**Tabla 3 (p. 11), RMSE medio en dólares:**

| Modelo | Univariante 15 | 30 | 60 | Multivariante 15 | 30 | 60 |
|---|---|---|---|---|---|---|
| XGB | 740,43 | 741,84 | 675,95 | 678,59 | 676,60 | 572,58 |
| **ESN** | **442,78** | **463,96** | **427,35** | 487,77 | 533,43 | 441,23 |
| Ingenuo | 736,60 | 751,18 | 787,02 | 713,53 | 749,96 | 665,62 |

- El RMSE del ESN equivale al **1,0 % a 2,7 % del precio de cierre, media 1,8 %** (p. 10). El XGBoost muestra picos en finales de 2020 y principios de 2021.
- Las variables técnicas mejoran a XGBoost y al ingenuo, pero **empeoran al ESN en ventanas de 15 y 30** (487,77 frente a 442,78; 533,43 frente a 463,96) y casi lo igualan en 60 (441,23 frente a 427,35); el texto afirma que "los modelos multivariantes generalmente rinden mejor", lo cual no se cumple para el ESN con la Tabla 3.

**Análisis del caos (p. 11 y p. 12):** para cada ventana se calcula λ_max (promedio de los 10 cortes de validación) y el cociente EXratio = RMSE_ESN / RMSE_XGB. Se dividen las ventanas en un grupo de **mucho caos** y otro de **poco caos** y se contrasta H0: mediana(EXratio)_poco = mediana(EXratio)_mucho frente a H1: distintas, con **U de Mann-Whitney** al 5 % (los datos no son gaussianos). Resultado: **significativo con ventanas de 30 y 60, no significativo con 15** (pocos puntos para reconstruir la trayectoria en el espacio de incrustación). Conclusión: el ESN supera más a XGBoost en los periodos de mayor caos (Figura 8). Los picos del cociente RMSE/precio ocurren a principios de 2019 y de 2021 (Figura 7).

## A5. Limitaciones y lectura crítica para la tesis

- Autores: ventanas cortas (no capturan tendencias de largo plazo ni estacionalidad); trabajo temprano en el tema.
- Observaciones propias (a verificar): (1) el objetivo es el **nivel de precio**, donde el referente de "último valor" es muy fuerte y el RMSE en dólares depende del nivel del precio (por eso crece en 2021-2022); un RMSE por debajo del ingenuo en niveles no equivale a predecir la **dirección** o el **retorno**; (2) no se reportan pruebas de Diebold y Mariano ni intervalos de confianza sobre las diferencias de RMSE; (3) la elección de hiperparámetros por TPE se hace por ventana y el texto no aclara si se usa la ventana de prueba o una validación aparte (riesgo de ajuste a la prueba); (4) el reservorio es de 50 a 250 neuronas con ventanas de 15 a 60 puntos, es decir, muy pocas muestras; (5) la relación con el caos se mide con λ_max sobre ventanas de 15 a 60 puntos, estimación muy poco fiable; la memoria del proyecto indica que BTC diario no mostró caos con pruebas con nulos.

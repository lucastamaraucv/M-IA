# Investigating the predictability of a Chaotic time-series data using Reservoir computing, Deep-Learning and Machine-Learning on the short-, medium- and long-term pricing of Bitcoin and Ethereum

**Extracción de conocimiento: 2026-10-02** (leídas las páginas 1 a 12, 20 a 23, 30 a 31, 54 a 71, 74, 80 a 87 y 93 a 96 de 102; no leída la revisión de literatura completa ni las páginas 72 a 79 de resultados de LSTM por tablas)

| Campo | Valor |
|---|---|
| Título exacto | Investigating the predictability of a Chaotic time-series data using Reservoir computing, Deep-Learning and Machine-Learning on the short-, medium- and long-term pricing of Bitcoin and Ethereum |
| Autora | Molly Kenny (supervisor: Brendan Tierney) |
| Tipo / Venue / Año | Tesis de máster (MSc in Computer Science, Data Science), Technological University Dublin, 2020; firmada el 30 de septiembre de 2020 |
| Archivo local | `Investigating the Predictability of a  Chaotic Time-Series Data u.pdf` |
| URL / DOI | https://doi.org/10.21427/42ks-q868 (repositorio ARROW@TU Dublin, `https://arrow.tudublin.ie/scschcomdis`) |
| Métodos | Red de estado de eco (ESN, biblioteca pyESN) con 500 neuronas; LSTM (TensorFlow); regresión lineal, bayesiana (Bayesian Ridge), elastic net, bosque aleatorio, XGBoost y una red neuronal de scikit-learn; 80 indicadores técnicos con selección por importancia por permutación; pruebas de no linealidad (exponente de Lyapunov, de Hurst, análisis de fluctuación sin tendencia, Dickey y Fuller) |
| Datos | Cierre diario de Bitcoin y Ethereum (1 123 días del 1 de agosto de 2017 al 28 de agosto de 2020 en la descripción; series más largas desde 2015 para las pruebas de caos), horizontes de 1, 5 y 30 días (p. 4 y p. 55) |

## Aporte clave

Es una de las tesis más cercanas a mi propuesta: **compara un reservorio (ESN) con LSTM y con modelos de aprendizaje automático** para predecir Bitcoin y Ethereum a corto (1 día), medio (5 días) y largo plazo (30 días). Concluye que a 1 y 5 días hay resultados positivos y a 30 días el análisis técnico no basta, y que **los modelos lineales rinden igual o mejor que los complejos** (p. 4, p. 72 y p. 94).

## Hallazgos cuantitativos (HECHO, con página)

- **Pruebas de caos y tendencia** (Tabla 4.2, p. 57), sobre el **nivel del precio**: exponente de Hurst de 0,92 para Bitcoin (1 760 días) y 0,91 para Ethereum; análisis de fluctuación sin tendencia mayor que 1 (1,58 y 1,61); la prueba de Dickey y Fuller no rechaza no estacionariedad (valor p de 0,36 para BTC en la muestra completa). El exponente de Lyapunov de Bitcoin es 0,0055 en la muestra completa, −0,0031 en los últimos 748 días y 0,0557 en los últimos 120. La autora concluye que los datos son caóticos y no estacionarios (p. 56).
- **Partición:** 70 % de entrenamiento y 30 % de prueba **sin barajar**, es decir, cronológica; ventanas hacia atrás de todas las observaciones, 748 y 120 días; horizontes 1, 5 y 30 días (p. 65). Escalado robusto.
- **Resultados de ML para Bitcoin** (Tabla 4.4, p. 68), con "score" = R² del nivel del precio:
  - 1 día: regresión lineal 0,946; Bayesian Ridge 0,946; bosque aleatorio 0,935; XGBoost 0,912; elastic net 0,826; red neuronal −1,354 (RMSE de 361 a 647 dólares para los lineales).
  - 5 días: de 0,64 a 0,67 para los modelos lineales y de árboles.
  - 30 días: todos negativos, de −0,82 a −2,30 (red neuronal −6,01).
- **Resultados de ML para Ethereum** (Tabla 4.5, p. 69): 1 día R² de 0,95 a 0,97 con los modelos lineales y de árboles; 5 días de 0,53 a 0,84; 30 días negativos (−0,16 a −2,40).
- **ESN** (diseño, p. 71): una sola variable de entrada (el precio de cierre), 500 neuronas, esparsidad 0,2 o 0,4, radio espectral entre 0,5 y 1,5 y ruido entre 1e-4 y 1e-2 optimizados por menor error cuadrático medio. Resultados: Bitcoin a 1 día con esparsidad 0,4: 67 %; con 0,2: 75 %; a 5 días, 28 % y 66 %; a 30 días los peores entre las redes recurrentes (p. 83 a 86). La autora observa que el ESN se apoya en una lectura lineal y que **en Ethereum la regresión lineal que usa como salida rinde mejor que la ESN completa** (p. 87).
- **LSTM:** el mejor rinde cerca del azar en dirección (acierto de 51,6 % a 53,2 % en un ejemplo) y **la predicción hacia adelante es inestable**: pequeños cambios de capas o ventana dan pronósticos opuestos (p. 81 y p. 82).
- **Selección de variables:** 80 indicadores técnicos; las importancias por permutación difieren entre Bitcoin y Ethereum (p. 63 y p. 64).

## Limitaciones y críticas

- Declarado por la autora: el LSTM puede estar sobreajustado y requiere más dropout y paciencia en la parada temprana; el ESN necesita estudiar el número de nodos con la esparsidad (p. 95).
- **[OPINIÓN]** **Se predice el nivel del precio y se mide con R² del nivel.** En una serie casi de paseo aleatorio con tendencia, el R² de un día es muy alto aunque el modelo no prediga nada (el valor de hoy ya "explica" el de mañana). No hay referente ingenuo (precio de ayer), así que 0,95 de R² no demuestra capacidad predictiva.
- **[OPINIÓN]** **El exponente de Hurst de 0,92 está calculado sobre el nivel del precio**, que es una serie integrada y por construcción da valores altos; no mide persistencia de los retornos. La conclusión de que "es más fácil predecir a corto plazo porque H > 0,5" (p. 94) no es válida con esa medida. En retornos, el resumen de Gezer (2025) del índice de teorías del proyecto reporta Hurst de 0,52 a 0,55 en escalas por minuto y por hora y de 0,64 en retornos diarios, y el propio proyecto midió 0,543: valores mucho más bajos que 0,92.
- **[OPINIÓN]** El exponente de Lyapunov cambia de signo según la ventana (0,0055; −0,0031; 0,0557), lo que sugiere que el cálculo no es estable; la afirmación de "caos" es débil.
- **[OPINIÓN]** Los hiperparámetros del ESN se eligen por menor error y mayor R² (p. 71), sin indicar si se midió en datos separados de la prueba; y la selección de variables por importancia por permutación con un bosque aleatorio parece hecha con toda la serie (p. 61 y p. 62), lo que puede filtrar información del futuro.
- **[OPINIÓN]** Una sola ejecución por configuración, sin semillas repetidas ni intervalos de confianza; en el ESN la autora admite que el resultado depende de nodos aleatorios (p. 84).
- **[OPINIÓN]** El ESN solo recibe el precio de cierre, mientras las demás técnicas reciben 80 indicadores, de modo que no es una comparación de igual a igual de información.

## Conexión con mi tesis (red E20)

- **Antecedente local y comparable:** reservorio con lectura lineal frente a LSTM y ML en Bitcoin con horizontes múltiples; refuerza que **los modelos lineales son un referente difícil de batir** y que el ESN no supera a su propia lectura lineal, lo que coincide con mi hallazgo de que la lectura manda y E20 empata con referentes simples.
- **Contraste de metodología:** yo uso retornos y movimiento, no el nivel del precio; referentes ingenuos; varias semillas; y fijo la lectura antes de ver el bloque final. Puedo presentar esta tesis como un caso donde esos controles faltan.
- **Pruebas de caos:** si incluyo un análisis de caos en la tesis, debo calcularlo sobre retornos y reportar su estabilidad por ventanas, no sobre precios.
- **Horizontes:** el resultado de que 30 días no son predecibles coincide con mi hallazgo de que la dirección solo se predice entre 1 minuto y 2 horas.
- **Límite para citarlo:** tesis de máster de 2020, con las limitaciones anteriores; no usarla como evidencia de predictibilidad.

## Referencias que cita y conviene localizar

Jaeger y Haas (2004), ESN; Lin, Yang y Song (2009), predicción bursátil con ESN y exponente de Hurst; Alessandretti y colaboradores (2018), "Anticipating cryptocurrency prices using machine learning" (Complexity, 10.1155/2018/8983590); Caporale, Gil-Alana y Plastun (2018), "Persistence in the cryptocurrency market" (10.1016/j.ribaf.2018.01.002); Carbone, Castelli y Stanley (2004), exponente de Hurst dependiente del tiempo (10.1016/j.physa.2004.06.130); Cheah y Fry (2015), burbuja en Bitcoin; Böhme y colaboradores (2015), "Bitcoin: Economics, Technology, and Governance". **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (datos, métodos, fundamentos matemáticos y tablas)

Contenido técnico de los capítulos 3 a 6 (páginas 41 a 95 del PDF), incluidas las secciones de resultados de ML, ESN y LSTM que la ficha anterior no había leído por completo. La revisión de literatura (cap. 2) queda como en la ficha. Páginas = páginas del PDF.

## A1. Diseño general (p. 41 a 43)

- Compara modelos mediante **MSE** y una "exactitud" **R²** en dos criptomonedas (Bitcoin y Ether) con datos de **Yahoo Finance** (apertura, máximo, mínimo, cierre, cierre ajustado y volumen diarios) en Python y Google Colab; paquetes: NumPy, pandas, matplotlib, **TA-Lib** (indicadores técnicos), **eli5** (importancia por permutación), **pyESN** (reservorio), **TensorFlow/Keras** (LSTM), **scikit-learn** (tuberías).
- **80 indicadores técnicos** de TA-Lib (Tabla 3.1; con periodos como EMA 5, 14 y 30); solo variables técnicas, sin datos externos.
- **Selección de variables:** bosque aleatorio de referencia; **importancia por permutación** (mean decrease accuracy, rfpimp/eli5) con R² como medida a maximizar y el cierre del día siguiente como objetivo; se eliminan las variables con importancia negativa (el cierre se conserva aunque salga negativo por su alta dependencia). Resultan conjuntos distintos para BTC y ETH (Tabla 4.3: por ejemplo la SMA de 5 días es la primera de BTC, rango 1, y la 56 en ETH, donde la señal MACD es la primera). Estas variables **no** se usan en el ESN (solo recibe el cierre).
- **Escalado robusto** (RobustScaler) en todos los modelos; en ESN con rango −1 a 1.

## A2. Fundamentos matemáticos de las pruebas de caos y de no estacionariedad (p. 45 a 47)

- **Exponente de Lyapunov** (algoritmo de Rosenstein y otros, 1993; máximo exponente): λ(x₀) = lim_{n→∞} (1/N)·Σ_{k=1}^{N} log|f′(x_k)|  (ecuación 3.1) y en tiempo finito λ(x₀) = (1/N)·Σ log|f′(x_k)|  (3.2). Positivo = caos y sensibilidad a las condiciones iniciales; "la magnitud refleja la escala de tiempo en que el sistema se vuelve impredecible" (Zerroug y otros, 2013).
- **Exponente de Hurst** (Hurst, 1951): (R/S)_n = (1/k)·Σ_{j=1}^{k} [R_j(t)/S_j(t)] = c·n^H  (3.3): H ≈ 0,5 paseo aleatorio, H > 0,5 tendencia (persistencia), H < 0,5 reversión a la media.
- **Análisis de fluctuación sin tendencia (DFA):** se integra la serie (suma acumulada X_t), se divide en ventanas de longitud n, se ajusta una recta por mínimos cuadrados en cada una (Y_t) y se calcula F(n) = sqrt( (1/N)·Σ (X_t − Y_t)² )  (3.4); DFA > 1 indica proceso no estacionario.
- **Prueba de Dickey y Fuller:** H₀ raíz unitaria; H₁ sin raíz unitaria.
- **MSE** (3.5) = (1/n)·Σ(Y_i − Ŷ)².
- **Parada temprana:** vigilando el mínimo de la pérdida de validación; paciencia 20 épocas con un máximo de 500 (cap. 3) y 10 épocas con un máximo de 1 000 en las pruebas de LSTM del cap. 4.

## A3. Datos y pruebas de no linealidad (p. 54 a 58)

- **Descripción 1 de agosto de 2017 a 28 de agosto de 2020** (Tabla 4.1; 1 123 días): BTC media 7 776,80, desviación 2 796,20, mín. 2 710,67, máx. 19 497,40; ETH media 316,43, desviación 227,31, mín. 84,31, máx. 1 396,42. Correlación de Pearson BTC–ETH = **0,91**.
- **Tabla 4.2** (sobre el **nivel del precio de cierre**; ventanas de 1 760, 748 y 120 días terminando el 25 de agosto de 2020):

| | BTC (1 760) | BTC (748) | BTC (120) | ETH (1 760) | ETH (748) | ETH (120) |
|---|---|---|---|---|---|---|
| Lyapunov | 0,005549 | −0,00309 | 0,05567 | 0,000884 | 0,014984 | 0,048502 |
| Hurst | 0,9235 | 0,9217 | 0,8495 | 0,9099 | 0,9270 | 0,8859 |
| DFA | 1,576 | 1,568 | 1,465 | 1,610 | 1,569 | 1,652 |
| Dickey y Fuller (estadístico) | −1,852 | −1,167 | −1,032 | −2,492 | −1,934 | −1,260 |
| Valor p | 0,355 | 0,688 | 0,741 | 0,118 | 0,316 | 0,931 |

  Interpretación de la autora: datos **caóticos y no estacionarios** (Lyapunov positivo, H > 0,5, DFA > 1, p > 0,05); el exponente de Lyapunov de BTC en la ventana de 748 días es negativo (−0,00309), lo que contradice la afirmación de caos persistente. **Estas pruebas se hacen sobre precios, no sobre retornos.**
- **Intentos de estacionarizar:** logaritmo (con atípicos de marzo de 2020), medias móviles de 5 y 30 días (no sirven), estacionalidad; se decide usar solo el escalado robusto y las ventanas de aprendizaje de 120, 750 y 1 500 días.

## A4. Modelos de aprendizaje automático (p. 65 a 70)

- **Partición:** `train_test_split` **70 % entrenamiento / 30 % prueba, sin barajar y sin validación**; retrospectiva de [todo, 748, 120] días y horizontes [1, 5, 30] días.
- **Tuberías de scikit-learn** (Robust Scaler y eliminación recursiva de variables): regresión lineal, **regresión bayesiana (Bayesian Ridge)**, **ElasticNetCV**, **bosque aleatorio** (500 árboles), **XGBoost** y **red neuronal** (ReLU, Adam, capas ocultas (8, 8, 8), 500 iteraciones máx.; el texto del cap. 5 dice (8, 8)). Métricas: error absoluto medio, "score" R² (sobre el **nivel del precio**).
- **Tabla 4.4 (BTC)**, prueba: 1 día: regresión lineal MAE 224,45, MSE 130 703, RMSE 361,53, R² 0,9459; Bayesian Ridge 235,63, 131 372, 362,45, 0,9456; Elastic Net 533,22, 419 162, 647,43, 0,8264; bosque aleatorio 263,32, 156 112, 395,11, 0,9353; XGBoost 309,83, 212 342, 460,81, 0,9120; red neuronal 1 821,78, 5 683 007, 2 383,91, −1,3541. 5 días: lineal 707,03 / 880 570 / 938,39 / 0,6368; Bayesian Ridge 699,33 / 884 022 / 940,22 / 0,6354; Elastic Net 693,47 / 792 623 / 890,29 / 0,6731; bosque 719,96 / 870 511 / 933,01 / 0,6410; XGBoost 686,25 / 863 182 / 929,08 / 0,6440; red −0,9464. 30 días: lineal 2 023,01 / 5 773 491 / 2 402,81 / −1,3087; Bayesian Ridge −1,1020; Elastic Net −0,8303; bosque −0,8248; XGBoost −1,2044; red −6,0127.
- **Tabla 4.5 (ETH)**, 1 día: lineal MAE 8,66, RMSE 11,96, R² 0,9644; Bayesian Ridge 8,32, 11,62, 0,9664; Elastic Net 9,40, 12,92, 0,9584; bosque 10,18, 13,62, 0,9538; XGBoost 8,45, 11,90, 0,9647; red 21,93, 27,14, 0,8165. 5 días: lineal 0,7471; Bayesian 0,7637; Elastic Net **0,8441**; bosque 0,5316; XGBoost 0,8232; red 0,2735. 30 días: lineal −1,3997; Bayesian −0,9034; Elastic Net −0,1558; bosque −0,5656; XGBoost −0,5590; red −0,4679.
- Evaluación de la autora: "prometedor a 1 y 5 días", las redes de scikit-learn las peores; la alta persistencia (H > 0,5) explica un MSE bajo y un R² alto a un día. **(R² sobre el nivel del precio; sin referente ingenuo.)**

## A5. Red de estado de eco (p. 50 a 52 y p. 71 a 76)

- **pyESN** (Korndörfer, 2015): entradas y reservorio aleatorios y fijos; salida lineal entrenada (regresión); **una entrada y una salida**, **500 neuronas**, **teacher forcing = True** (se realimenta el objetivo a las unidades de salida), sin escala ni desplazamiento de entrada, salida lineal; inicialización: matriz aleatoria centrada en cero, se borra la fracción dada por la dispersión (sparsity), se calcula el radio espectral y se reescala hasta el pedido; costo de entrenamiento O(N) en las unidades ocultas; la predicción empieza desde el último estado de entrenamiento.
- **Espacio de búsqueda** (Tablas 3.2 y 4.6): dispersión 0,2, 0,4, 0,6, 0,8 (en el cap. 4 se fija 0,2 "para aumentar la naturaleza caótica y evitar el sobreajuste" y se compara con 0,4); radio espectral 0,5, 0,7, 0,9, 1, 1,1, 1,3, 1,5; ruido 0,0001, 0,0003, 0,0007, 0,001, 0,003, 0,005, 0,007, 0,01; criterio: **MSE mínimo y R² máximo**; aprende de 1 500 días anteriores con una validación de 120 días.
- **Tabla 4.7 (ETH, 1 día):** antes de optimizar (ruido 0,0003, radio 0,5) MSE 0,003513; tras optimizar (ruido 0,0003, radio 1,3) MSE 0,002229. **Tabla 4.8:** ETH, 500 neuronas, dispersión 0,2, radio 0,7, ruido 0,0003, MSE 0,2625, R² 0,8518; BTC, radio 1,5, ruido 0,007, MSE 0,1981, R² 0,7712 (escalas distintas de las de la Tabla 4.7). Figura 4.15: el MSE crece con la longitud de la ventana de aprendizaje, por lo que se optimiza también la ventana.
- **Resultados** (Figuras 5.1 a 5.12, "score" R² en %): BTC 1 día ESN 67 % (dispersión 0,4) y 75 % (0,2); 5 días 28 % y 66 %; 30 días los peores de las redes recurrentes; ETH 1 día 90 % y 87 %; 5 días 32 % (dispersión 0,4) y 73 % (0,2); 30 días −17 % y −77 %. La autora observa que el ESN tiene el MSE más alto aunque la mayor exactitud entre las redes recurrentes, que la dirección suele ser incorrecta (Figura 4.16) y que **la salida lineal del propio ESN rinde mejor que el ESN en ETH**; concluye que "no es actualmente un método apropiado" para estas criptomonedas.

## A6. LSTM (p. 77 a 82)

- TensorFlow/Keras, **tanh**, **Adam**, lote 128, validación 10 %, parada temprana (1 000 épocas, paciencia 10), entrada de forma (764, 1000, 59) (secuencias de hasta 1 000 días con 59 variables), configuraciones con 3, 4, 5 y 12 capas, dropout cada dos capas y ventanas de 90, 120, 750, 1 000 y 1 500 días; **la predicción hacia adelante es inestable**: un modelo de 12 capas con 750 días de ventana pronostica el precio por más del doble para los 2 días siguientes (exactitud 53,16 %, MSE 0,09027) y uno de 5 capas sin dropout predice un valor negativo (exactitud 51,58 %, MSE 0,01796). Resultados de los LSTM (R² %): BTC 1 día 61 % (LSTM_90_3L), 59 % (90_4L), 54 % (1000_4L); 5 días 40 %, 19 % y 69 %; ETH 1 día 54 %, 57 % y 59 % (120, 750 y 1 500 días con 4 capas); 5 días 27 %, 26 % y 33 %; 30 días 24 %, 12 % y 13 %. Las Tablas 4.10 y 4.11 (resultados detallados) se presentan como imágenes.

## A7. Conclusiones de la autora (p. 91 a 95)

Los modelos lineales (regresión lineal y bayesiana) rinden bien a 1 y 5 días; a 30 días nadie predice; el ESN solo proporciona resultados aceptables con ajuste; la persistencia de las series (H > 0,5) hace más fácil la predicción a corto plazo ("los mercados no siguen un paseo aleatorio y son persistentes", Caporale y otros, 2018); trabajo futuro: más dropout y paciencia en el LSTM, estudiar nodos del reservorio con la dispersión, estrategia de cartera (comprar si la predicción del ESN > 5 %).

## A8. Lectura crítica adicional (se suma a la ficha)

1. **Hurst de 0,92, DFA de 1,5 y Dickey y Fuller sobre el precio** no miden la predictibilidad: son propiedades de una serie integrada; sobre retornos, el exponente de Hurst de BTC está cerca de 0,5.
2. **R² del nivel con 30 % de prueba (≈ 337 días)**: sin referente ingenuo, el R² de 1 día está por construcción cerca de 1; que la regresión lineal sea la mejor es coherente con una serie persistente.
3. **ESN con teacher forcing y solo el precio** frente a modelos con 80 indicadores: información distinta; la lectura lineal del ESN supera al ESN en ETH (hallazgo coherente con el proyecto: la lectura manda).
4. **Selección de variables y de hiperparámetros del ESN** con el MSE de la misma serie, sin separar claramente un bloque final.
5. **Sin repeticiones ni semillas variadas** (el ESN depende de pesos aleatorios, lo que la autora admite).

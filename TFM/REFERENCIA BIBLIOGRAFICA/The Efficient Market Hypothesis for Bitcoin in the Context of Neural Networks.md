# The Efficient Market Hypothesis for Bitcoin in the Context of Neural Networks

**Extracción de conocimiento: 2026-10-02** (leído el texto de las páginas 1 a 22 de 28; el resto son gráficos del apéndice)

| Campo | Valor |
|---|---|
| Título exacto | The Efficient Market Hypothesis for Bitcoin in the Context of Neural Networks |
| Autores | Mike Kraehenbuehl y Joerg Osterrieder (Escuela de Ingeniería, Zurich University of Applied Sciences, Winterthur, Suiza) |
| Tipo / Venue / Año | Preprint (arXiv 2208.07254v1), fechado el 16 de agosto de 2022 |
| Archivo local | `2208.07254v1.pdf` |
| URL / DOI | arXiv:2208.07254 (sin DOI de revista en el documento) |
| Métodos | Red neuronal de propagación hacia adelante (feedforward) con capas de 30, 15 y 5 neuronas ReLU y salida sigmoide; entropía cruzada binaria; Adam; 300 épocas; lote de 20; tasa de aprendizaje 0,00005 (p. 10 a 12) |
| Datos | Precios diarios de Yahoo Finance desde 2014-09-17 hasta 2022-04-30: BTC/USD, S&P 500, Russell 2000, EUR/USD, rendimiento del bono del Tesoro a 10 años y el índice de oro y plata XAU (p. 5 y p. 7) |

## Aporte clave

Pone a prueba la forma débil de la hipótesis del mercado eficiente en Bitcoin con una red neuronal sencilla, añadiendo uno a uno activos de otros mercados como entradas. Con la señal de dirección del día siguiente como objetivo, concluye que **añadir variables mejora el ajuste dentro de la muestra pero no el resultado fuera de ella**, y que Bitcoin parece débilmente eficiente en el periodo estudiado (p. 15 y p. 16).

## Hallazgos cuantitativos (HECHO, con página)

- **Acierto dentro de la muestra:** sube de 54,6 % con una variable (Bitcoin) a 61,0 % con seis (Tabla 6, p. 13).
- **Acierto fuera de la muestra:** se queda entre 51,9 % y 53,0 % para todos los conjuntos de variables (Tabla 6, p. 13). El conjunto 4 (con EUR/USD) llega a 53,0 % y cae al añadir el bono a 10 años; los autores lo atribuyen al azar (p. 15).
- **Referente aleatorio:** un conjunto de números normales aleatorios con la misma varianza que los retornos de Bitcoin ("rNorm") consigue 52,5 % fuera de muestra, igual o mejor que 3 de los 6 conjuntos reales (p. 13 y p. 15).
- **Comprar y mantener** acertaría el 53,2 % de los días del periodo de prueba (p. 15). Ningún conjunto de variables lo supera en acierto.
- **Rendimiento:** la suma acumulada de log-retornos de comprar y mantener es 1,054. Solo el conjunto 4 la supera (1,109); el resto queda por debajo (Tabla 6 y p. 15).
- **Control positivo:** usando el retorno de Ethereum del mismo día como entrada, el acierto sobre Bitcoin es 80,5 % (10 repeticiones). Sirve para demostrar que el modelo detecta una dependencia cuando existe (p. 12).
- **Efecto de la inicialización:** con los mismos datos, la mejor iteración da 54,5 % y la peor 49 %, solo por los pesos iniciales (p. 12). Por eso repiten cada conjunto 50 veces y promedian.
- **Efecto de las variables sobre las señales:** al añadir variables el modelo predice menos señales positivas (89 % con "rNorm" frente a 66 % con las seis variables) (p. 16).
- **Autocorrelación de Bitcoin:** solo los retardos 6 y 10 salen fuera del intervalo de confianza del 95 % (apéndice, p. 19).
- **Tamaño de muestra:** al eliminar filas con datos faltantes (fines de semana y festivos), el conjunto pasa de 2 783 a 1 495 filas; con retardo 2 bajaría a 1 092 (p. 7 y p. 9).

## Métodos y diseño experimental

- Retornos logarítmicos normalizados entre 0 y 1; un solo retardo de un día (p. 6 y p. 9).
- Objetivo binario: signo del retorno de Bitcoin del día siguiente; estrategia "solo largo" con umbral de probabilidad 0,5 (p. 9).
- 50 entrenamientos por conjunto de variables y promedio de métricas; se muestran intervalos de confianza del 95 % para el acierto (p. 12 y p. 13).
- Métricas: acierto, entropía cruzada, suma acumulada de log-retornos y razón de Sharpe (p. 13 y p. 15).
- Código publicado en GitHub (referencia [52] del artículo).

## Limitaciones declaradas y críticas

- Declarado por los autores: el resultado depende del periodo, las variables, la arquitectura y los hiperparámetros; no se buscó optimizar el modelo (p. 16).
- **[OPINIÓN]** Las 50 repeticiones solo varían la inicialización de la red sobre **los mismos datos**: no son muestras independientes, así que no reducen la incertidumbre por el tamaño limitado de la serie.
- **[OPINIÓN]** No hay contraste estadístico formal frente al 53,2 % de comprar y mantener. El texto afirma que el límite inferior del intervalo del 95 % está por encima de 50 % en todos los conjuntos (p. 13), pero ese intervalo también cubre al referente aleatorio.
- **[OPINIÓN]** Un solo retardo y una sola arquitectura pequeña; con 1 495 filas el conjunto de prueba es corto. No se consideran costes de transacción.

## Conexión con mi tesis (red E20)

- **Un diseño equivalente a mis controles:** el referente aleatorio "rNorm" es mi control negativo (nivel de señal 0 %), y la prueba con Ethereum del mismo día es mi control positivo. Es un antecedente publicado para justificar ambos controles.
- **Promediar semillas:** el artículo muestra con números reales que una sola corrida puede dar 49 % o 54,5 %. Justifica reportar medias sobre varias semillas de red y realizaciones, como hago en mi plan.
- **Referente de comprar y mantener:** su acierto del 53,2 % indica que un acierto "por encima de 50 %" no es suficiente; hay que comparar con el referente adecuado. Es coherente con comparar E20 contra la media móvil de |retorno|.
- **Sobreajuste dentro de la muestra:** el aumento de 54,6 % a 61 % dentro de la muestra sin ganancia fuera es el patrón que debo vigilar en E20 (3001 columnas de estados).
- **Límite para citarlo:** usa la escala diaria y 1 495 filas; mi hallazgo de que la dirección diaria de Bitcoin no es predecible lo confirma, pero no dice nada de 1 h a 2 h.

## Referencias que cita y conviene localizar

Fama (1965 y 1970), forma débil, semifuerte y fuerte de la eficiencia; Urquhart (2016), "The inefficiency of Bitcoin"; Nadarajah y Chu (2017); Bariviera (2017); Brauneis y Mestel (2018); Tiwari y otros (2018); Sensoy (2019), análisis de alta frecuencia; Jaquart, Dann y Weinhardt (2021), predicción de Bitcoin a corto plazo con aprendizaje automático; Wildi y Bundi (2019); Gu, Kelly y Xiu (2020), valoración de activos con aprendizaje automático; Lo (2004), hipótesis de los mercados adaptativos. **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (datos, métodos, fundamentos matemáticos y tablas)

Contenido técnico íntegro del texto principal (páginas 1 a 22 del PDF; las páginas 23 a 28 son gráficos del apéndice por conjunto de variables). Páginas = páginas del PDF.

## A1. Marco teórico del artículo (p. 3 y p. 4)

- **Hipótesis del mercado eficiente (EMH):** Fama (1965, 1970) distingue la forma **débil** (los precios reflejan toda la información de precios pasados), **semifuerte** (toda la información pública) y **fuerte** (también la privada). Condiciones suficientes (no necesarias): sin costes de transacción, información gratuita para todos y acuerdo de todos sobre las implicaciones de la información (p. 3).
- **Literatura sobre Bitcoin y eficiencia** (p. 4): Urquhart (2016) halla ineficiencia de 2010 a 2016 con pruebas como Ljung-Box y AVR, con tendencia a la aleatoriedad en la segunda mitad; Nadarajah y Chu (2017) con transformaciones de potencia concluyen eficiencia; Bariviera (2017) con el exponente de Hurst (agosto de 2011 a febrero de 2017) halla eficiencia débil desde 2014; Brauneis y Mestel (2018): la eficiencia se relaciona con la liquidez y Bitcoin pasa más pruebas de aleatoriedad; Tiwari y otros (2018): eficiente salvo abril-agosto de 2013 y agosto-noviembre de 2016; Al-Yahyaee y otros (2018): Bitcoin es el menos eficiente frente a acciones, oro y divisas; Sensoy (2019): más eficiente a escala intradía, y menor eficiencia a mayor frecuencia; Vidal-Tomás e Ibáñez (2018): eficiencia semifuerte creciente.
- **Aprendizaje automático en finanzas** (p. 5): estudios con variables técnicas, de cadena de bloques, de sentimiento y de otros activos; los factores técnicos son los más importantes; supera a un clasificador aleatorio pero pierde tras costes (no viola la EMH). Feng y Giglio (2020) proponen contrastar la contribución marginal de un factor nuevo con lasso de doble selección.

## A2. Datos

- **Periodo:** 17 de septiembre de 2014 a 30 de abril de 2022, precios diarios descargados con el paquete `yfinance` de Yahoo Finance (p. 5 y p. 9).
- **Variables** (Tabla 1, p. 5): BTC/USD (CoinMarketCap, símbolo BTC-USD, marca 23:59 UTC); S&P 500 (^GSPC, 20:00 UTC); Russell 2000 (^RUT, 20:00 UTC); EUR/USD (EURUSD=X, 21:30 UTC); rendimiento del bono del Tesoro a 10 años (^TNX, 19:00 UTC); índice de oro y plata PHLX XAU (^XAU, 21:30 UTC). El XAU tiene correlación de Pearson de 0,95 con el futuro de oro de 100 onzas (GC=F) (p. 6).
- **Retorno logarítmico:** log(1 + r_t) = log(P_t / P_{t−1}) = log(P_t) − log(P_{t−1})  (ecuación 1), por ser estacionario y aditivo.
- **Estadísticos de los retornos logarítmicos** (Tabla 2, p. 6):

| Variable | Media | Mínimo | Máximo | Asimetría | Curtosis |
|---|---|---|---|---|---|
| BTC/USD | 0,0015 | −0,465 | 0,225 | −0,767 | 11,112 |
| S&P 500 | 0,0005 | −0,099 | 0,089 | −0,217 | 13,434 |
| Russell 2000 | 0,0003 | −0,118 | 0,089 | −0,696 | 9,545 |
| EUR/USD | 0,0000 | −0,028 | 0,028 | 0,069 | 3,236 |
| Bono 10 años | 0,0003 | −0,271 | 0,404 | 1,564 | 28,149 |
| Oro y plata | 0,0002 | −0,146 | 0,144 | −0,059 | 3,314 |

El mayor retorno negativo (−0,271) y positivo (0,404) del bono ocurrieron entre el 6 y el 10 de marzo de 2020. Mapa de correlación (Figura 17): alta entre S&P 500 y Russell 2000; correlación moderada positiva entre el resto, con dos excepciones: el bono a 10 años no se correlaciona con Bitcoin y el oro y plata se correlaciona negativamente con el bono (p. 6).
- **Datos faltantes** (p. 7): los demás activos no cotizan en fines de semana y festivos; se eliminan las filas con faltantes. El conjunto pasa de **2 783 a 1 495 filas** con retardo 1 y a **1 092 filas** con retardo 2 (reducción de 27 %); por eso se usa solo el retardo 1.
- **Autocorrelación de Bitcoin** (apéndice 8.1, p. 19): solo los retardos 6 y 10 salen fuera del intervalo del 95 %; la ausencia de autocorrelación no implica independencia porque no detecta no linealidad.

## A3. Método

- **Procedimiento (p. 8):** (1) importar precios; (2) retornos logarítmicos; (3) seis conjuntos de variables; (4) desfase de un día; (5) eliminar filas con faltantes; (6) normalizar a [0, 1]; (7) objetivo binario de señal de Bitcoin; (8) partición en entrenamiento, validación y prueba; (9) entrenar una red de propagación hacia adelante para predecir la señal del día siguiente; (10) evaluar fuera de muestra.
- **Conjuntos de variables** (Tabla 3, p. 9; todos con retardo 1): C1 Bitcoin; C2 Bitcoin y S&P 500; C3 más Russell 2000; C4 más EUR/USD; C5 más el bono a 10 años; C6 más oro y plata. Además C0, un conjunto de números normales aleatorios N(0, σ²) con σ² = varianza de los retornos de Bitcoin (referente de ruido).
- **Normalización:** X_sc = (X − X_min)/(X_max − X_min)  (ecuación 3).
- **Objetivo** (ecuación 4, p. 9): señal binaria, 1 si el retorno de Bitcoin del día siguiente es positivo y 0 si es negativo; estrategia solo largo con umbral de probabilidad 0,5: t(p) = 1 si p ≥ 0,5 y 0 si p < 0,5  (ecuación 7).
- **Arquitectura** (Tabla 4, p. 10): entrada con tantas neuronas como variables; capa oculta 1 de 30 neuronas ReLU; capa oculta 2 de 15 ReLU; capa oculta 3 de 5 ReLU; salida de 1 neurona sigmoide. Activaciones: ReLU(z) = max(0, z)  (5); sigmoide σ(z) = 1/(1 + e^{−z})  (6). Se justifica ReLU por mitigar el desvanecimiento del gradiente (derivada 0 o 1).
- **Pérdida:** entropía cruzada binaria L(ŷ, y) = −[y·log(ŷ) + (1 − y)·log(1 − ŷ)]  (8), aplicada tras la sigmoide y antes del umbral.
- **Entrenamiento** (p. 12): optimizador **Adam** con normalización por lotes, **300 épocas**, lote de **20** y tasa de aprendizaje **0,00005**. Implementación en Keras; código en GitHub.
- **Aleatoriedad** (p. 12): como los pesos iniciales cambian el resultado, **cada conjunto se entrena y evalúa 50 veces** y se promedian las métricas. Ejemplo con el conjunto C2: la mejor iteración (36 de 50) da 54,5 % de acierto fuera de muestra y suma acumulada de log-retornos de 1,52; la peor (40 de 50), 49 % y 0,13.
- **Control positivo** (p. 12): con el retorno de **Ethereum del mismo día** como única entrada, el acierto sobre Bitcoin es **80,5 %** (promedio de 10 repeticiones).
- **Métricas de rendimiento** (p. 15): suma acumulada de log-retornos con la estrategia solo largo = P·R  (9), con P el vector de señales (0 o 1) y R los log-retornos reales; razón de Sharpe = (R_p/σ_p)·√252  (10), con R_p el log-retorno acumulado promedio de las 50 repeticiones y σ_p la desviación diaria promedio.

## A4. Resultados completos

**Tabla 6 (p. 13)**, promedio de 50 iteraciones por conjunto:

| Conjunto | Acierto dentro de muestra | Acierto fuera de muestra | Pérdida dentro | Pérdida fuera | Log-suma | Sharpe | Señales positivas / negativas |
|---|---|---|---|---|---|---|---|
| C0 (aleatorio) | 0,549 | 0,525 | 0,687 | 0,698 | 0,922 | 0,603 | 534 / 64 |
| C1 | 0,546 | 0,527 | 0,693 | 0,701 | 0,938 | 0,687 | 499 / 99 |
| C2 | 0,574 | 0,519 | 0,678 | 0,712 | 0,870 | 0,696 | 472 / 126 |
| C3 | 0,585 | 0,523 | 0,671 | 0,720 | 0,812 | 0,646 | 453 / 145 |
| C4 | 0,595 | 0,530 | 0,663 | 0,719 | 1,109 | 0,866 | 424 / 174 |
| C5 | 0,603 | 0,527 | 0,659 | 0,730 | 0,833 | 0,637 | 400 / 198 |
| C6 | 0,610 | 0,525 | 0,654 | 0,733 | 0,853 | 0,656 | 392 / 206 |

- Dentro de muestra el acierto sube de 54,6 % (C1) a 61 % (C6), y la pérdida baja; fuera de muestra el acierto no crece de forma monótona y la pérdida **sube** con cada variable añadida (señal de sobreajuste, p. 14).
- Los intervalos de confianza del 95 % del acierto fuera de muestra tienen el límite inferior por encima de 50 % en todos los conjuntos (Figura 18, p. 20), pero también para el conjunto aleatorio C0.
- **Referencias de rendimiento** (p. 15): comprar y mantener en el periodo de prueba suma 1,054 de log-retornos y acierta el 53,2 % de los días; solo C4 supera a comprar y mantener en rendimiento (1,109). Los Sharpe superiores a comprar y mantener se atribuyen a que el modelo no siempre está invertido.
- **Actividad del modelo** (p. 16): C0 predice señal positiva 89 % del tiempo; C6, 66 %.

## A5. Conclusión técnica del artículo (p. 16)

(RC1) Añadir variables no mejora de forma consistente el acierto fuera de muestra. (RC2) Bitcoin parece débilmente eficiente en el escenario elegido (periodo, variables, arquitectura, un retardo e hiperparámetros); con otros parámetros los resultados cambiarían. Se aconseja investigación adicional y datos intradía para evitar la pérdida de filas por faltantes.

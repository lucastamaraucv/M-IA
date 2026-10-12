# Prediction of cryptocurrency returns using machine learning

**Extracción de conocimiento: 2026-10-02** (leídas las páginas 1 a 28 de 34; las restantes son tablas de índices y referencias)

| Campo | Valor |
|---|---|
| Título exacto | Prediction of cryptocurrency returns using machine learning |
| Autores | Erdinc Akyildirim (ETH Zúrich y Universidad de Zúrich), Ahmet Goncu (Universidad Xi'an Jiaotong-Liverpool y Universidad Jiao Tong de Shanghái) y Ahmet Sensoy (Universidad Bilkent, Ankara) |
| Tipo / Venue / Año | Artículo de revista: Annals of Operations Research (2021) 297:3-36; publicado en línea el 7 de abril de 2020 (número especial "Networks and Risk Management") |
| Archivo local | `Prediction_of_cryptocurrency_returns_using_machine_learning.pdf` |
| URL / DOI | https://doi.org/10.1007/s10479-020-03575-y |
| Métodos | Clasificación de la dirección del siguiente periodo con regresión logística, máquinas de vectores de soporte (SVM), perceptrón multicapa (capas de 40 y 2 nodos) y bosque aleatorio, con 40 variables; referentes: paseo aleatorio simulado y ARIMA; pruebas t, de rangos con signo de Wilcoxon y conjunto de confianza de modelos |
| Datos | 12 criptomonedas (79,8 % de la capitalización total en junio de 2018) del 10 de agosto de 2017 al 23 de junio de 2018; frecuencias de 15, 30 y 60 minutos y diaria (317 a 318 días) (p. 5 a 12) |

## Aporte clave

Estudia la **predecibilidad de la dirección** (sube o baja) de las 12 criptomonedas más líquidas en cuatro escalas temporales y concluye que la exactitud promedio **fuera de muestra supera de forma consistente el 50 %**, con las SVM como el modelo más robusto y exactitudes de 55 a 65 % en el resumen (p. 1 y p. 29). Es un antecedente directo para mi pregunta sobre dirección a escalas de minutos a un día.

## Hallazgos cuantitativos (HECHO, con página)

- **Diseño:** objetivo binario: 1 si el cierre es mayor que la apertura del periodo siguiente y −1 en caso contrario; 40 variables (apertura, máximo, mínimo y cierre, volúmenes y número de operaciones, 5 retornos rezagados, medias móviles, RSI, MACD, tasa de cambio, momentum, rango verdadero medio, Williams %R, Aroon, CCI y DEMA) (Tabla 7, p. 12 a 14).
- **Particiones:** diaria 80 % entrenamiento y 20 % prueba; por minutos 90 % y 10 %, con tres subperiodos de prueba adicionales de 200, 400 y 600 observaciones; el parámetro C de la regresión logística se elige por validación cruzada dentro de la muestra (p. 15 y p. 18). No se rellenan los periodos sin operaciones con el último precio.
- **Exactitud fuera de muestra, media de las 12 criptomonedas** (Tablas 8 a 12, p. 19 a 24):
  - diario: regresión logística 0,56; SVM 0,59; red neuronal 0,54; bosque aleatorio 0,55; promedio de los cuatro 0,56 (rango entre monedas 0,48 a 0,61);
  - 60 minutos: regresión logística 0,55; SVM 0,54; red neuronal 0,52; bosque aleatorio 0,52; promedio 0,53;
  - 30 minutos: de 0,52 a 0,54; promedio 0,53;
  - 15 minutos: de 0,52 a 0,54; promedio 0,53, con subperiodos de 0,54 a 0,56.
- **Para Bitcoin** (diario, 20 % final, Tablas 8 a 11): regresión logística 0,55; SVM 0,52; red neuronal 0,53; bosque aleatorio 0,62.
- **Dentro de muestra** el bosque aleatorio llega a 0,97 a 0,99 y la red neuronal a 0,71 a 0,97; fuera de muestra caen a 0,45-0,62 (Tablas 10 y 11, p. 21 a 23). Los autores lo interpretan como alta varianza y sobreajuste al ruido (p. 22).
- **Referentes** (Tabla 13, p. 25): el paseo aleatorio simulado da 0,50 de media en todas las escalas; **ARIMA queda por debajo del 50 %** (diario 0,45; 60 minutos 0,47; 30 y 15 minutos 0,47 a 0,48).
- **Pruebas estadísticas** (Tablas 16 a 18, p. 26 a 30): las diferencias entre los modelos de ML y ARIMA son significativas (por ejemplo diario fuera de muestra, regresión logística contra ARIMA: +0,111, estadístico t de 8,44); entre algoritmos de ML las diferencias fuera de muestra son pequeñas y muchas no son significativas (regresión logística contra SVM diario fuera de muestra: −0,029, t de −1,22).
- **Conjunto de confianza de modelos** (Tabla 14, p. 27): la regresión logística o el bosque aleatorio quedan primero según la escala; las SVM no son las primeras en esa prueba.
- **Índices de criptomonedas** ponderados por igual y por capitalización (Tabla 15, p. 28): accuracy diaria fuera de muestra de 0,65 a 0,86 con los distintos algoritmos, que los autores atribuyen a que el índice es una serie más suave.
- **Conclusión de los autores** (p. 29): la exactitud puede llegar a 69 % en ciertos casos sin ajuste fino y "con ajuste adicional podrían superar el 70 %"; implica incumplimiento de la eficiencia débil.

## Limitaciones y críticas

- Declarado por los autores: la red neuronal puede mejorar con más datos; los modelos más complejos podrían usarse a frecuencias altas con más observaciones (p. 22 y p. 29).
- **[OPINIÓN]** **Muestra diaria muy pequeña:** 317 observaciones diarias y 20 % de prueba son unos 63 días. Con 63 aciertos binarios el error estándar de un acierto cercano a 55 % es de unos ±6 puntos; "69 %" es el máximo entre 12 monedas y 4 modelos, es decir, el mejor de 48 casos, lo que infla el resultado por selección.
- **[OPINIÓN]** Todo el periodo (agosto de 2017 a junio de 2018) es un único ciclo de auge y caída; no hay varias ventanas de régimen.
- **[OPINIÓN]** A 15 a 60 minutos la exactitud de 52 a 55 % es pequeña y **no se evalúa con costes de transacción ni con un intervalo de confianza**; las pruebas t y de Wilcoxon tratan a las 12 criptomonedas como observaciones independientes, aunque están muy correlacionadas.
- **[OPINIÓN]** **El referente ARIMA por debajo del 50 %** no es un referente exigente: un modelo que acierta menos que el azar facilita que cualquier clasificador parezca "significativamente mejor". El referente natural sería "igual que el signo previo" o la proporción de subidas.
- **[OPINIÓN]** La conclusión de que "fácilmente se superará el 70 %" no está respaldada por las tablas, cuya media es de 53 a 59 %.
- **[OPINIÓN]** No se informan semillas ni repeticiones de los modelos con inicialización aleatoria (red neuronal, bosque).

## Conexión con mi tesis (red E20)

- **Es el antecedente más directo para la dirección a escalas intradía:** acierto de 52 a 55 % a 15, 30 y 60 minutos con 40 variables y modelos de ML, en un periodo distinto (2017-2018). Mi hallazgo de que la dirección de Bitcoin es predecible solo entre 1 minuto y 2 horas, con AUC de .54 a .55, es **del mismo orden de magnitud**; puedo presentar mi resultado como una confirmación parcial con un protocolo más estricto (varias semillas, bloque final intocable, referentes simples).
- **Referentes:** mi diseño mejora lo que falta aquí: compara con la media móvil de |retorno| y con la proporción de subidas, y no con un ARIMA débil.
- **Modelos de ML que comparo:** regresión logística, bosque aleatorio, perceptrón multicapa y SVM son los mismos que mi banco de comparación (más gradient boosting, TCN y LSTM); este artículo justifica incluirlos.
- **Tamaños de muestra:** advierte de que 63 días no bastan; mi plan declara la potencia estadística disponible y no afirma significancia con pocas realizaciones.
- **Límite para citarlo:** periodo único de 2017-2018, sin costes ni intervalos de confianza, y con una conclusión más fuerte que las tablas.

## Referencias que cita y conviene localizar

Fama (1970), eficiencia de mercado; Urquhart (2016), "The inefficiency of Bitcoin"; Nadarajah y Chu (2017); Bariviera (2017); Brauneis y Mestel (2018), eficiencia entre criptomonedas; Wei (2018), predecibilidad de 456 criptomonedas; Sensoy (2019), análisis de alta frecuencia con monedas alternativas; Bouri y colaboradores (2019a y 2019b); Hansen, Lunde y Nason (2011), conjunto de confianza de modelos; Kim (2003) y Huang y colaboradores (2005), SVM en predicción financiera; Breiman (2001), bosques aleatorios. **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (datos, métodos, fundamentos matemáticos y tablas)

Contenido técnico del texto principal y de las tablas 1 a 18 (páginas 1 a 30 del PDF; las tablas 8 a 12 son muy extensas y aquí se resumen por fila de media entre criptomonedas). Páginas = páginas del PDF.

## A1. Datos (p. 4 a 12)

- **Fuente:** precios en dólares de la bolsa **Bitfinex**; operaciones de la tienda de datos **Kaiko**. Periodo inicial del 1 de abril de 2013 al 23 de junio de 2018 (solo Bitcoin cubre todo el periodo; las demás empiezan, como pronto, el 10 de agosto de 2017).
- **Selección de monedas:** (1) datos desde el 10 de agosto de 2017 y vigentes el 23 de junio de 2018; (2) menos de 1 % de intervalos sin operaciones para la frecuencia elegida. Resultan **12 criptomonedas**: BCH, BTC, DSH, EOS, ETC, ETH, IOT, LTC, OMG, XMR, XRP, ZEC, que suman el **79,8 %** de la capitalización total el 17 de junio de 2018 (BTC 39,9 %; ETH 17,9 %; XRP 7,5 %; BCH 5,2 %; Tabla 1).
- **Frecuencias:** 15 min, 30 min, 60 min y diaria. **No se arrastra el último precio** en intervalos sin operaciones (se descartan). Intervalos con operaciones: 15 min ≈ 30 300 por moneda (OMG 29 959); 30 y 60 min ≈ 7 600 (OMG 7 515); diario **318 días** (317 observaciones de retorno; OMG 315). Tasa de intervalos sin operaciones de BTC: 0,51 % (15 min), 0,45 % (30 min), 0,38 % (60 min); la mayor, OMG, 1,00 % a 15 min (Tabla 2).
- **Estadísticos de los retornos logarítmicos (Tablas 3 a 6):** para BTC la desviación típica es 0,00654 (15 min), 0,00920 (30 min), 0,01275 (60 min) y **0,05505 (diaria)**; el porcentaje de subidas es 50,51 % (15 min), 50,89 % (30 min), 50,93 % (60 min) y **53,00 % (diaria, 168 subidas y 148 bajadas)**; en diario ETH 51,10 %, EOS 47,63 %, BCH 45,74 % (sube la tasa base de cada moneda y diverge del 50 %). Las volatilidades diarias van de 0,0698 (DSH) a 0,0986 (EOS) en las más volátiles; BTC (0,0551) y ETH (0,0610) son las menos volátiles.

## A2. Variables y objetivo (p. 11 a 13)

- **40 variables** de entrada: (a) **11 fundamentales:** apertura, máximo, mínimo, cierre del último periodo, rango máximo−mínimo, número de operaciones, volumen en dólares y volumen en criptomoneda de todas las operaciones, y los mismos tres para las operaciones **iniciadas por el comprador**; (b) retornos de los últimos **5 periodos** (r_{t−1}…r_{t−5}); (c) media móvil de 5 días, correlación entre la media móvil y el cierre, suma acumulada de retornos de 3 y 5 días y su diferencia; (d) **índice de fuerza relativa (RSI)** con ventanas de 6 y 14 (el texto dice 9 y 14 en la p. 11 y 6 y 14 en la Tabla 7), con señales de compra (RSI < 20 %) y de venta (RSI > 80 %) para ambas; **cambio porcentual (ROC)** de 9 y 14; MACD (rápida 5, lenta 10, señal 5); promedio móvil exponencial (λ = 0,9); momento (5); rango verdadero promedio (5 y 10); %R de Williams (14); oscilador de Aroon (14); índice de canal de materias primas (14); media móvil exponencial doble (10).
- **Fórmulas:** RSI = 100 − 100 / (1 + SMMA(U, n)/SMMA(D, n))  (1), con U = cierre_actual − cierre_previo y D = 0 si sube (2) y D = cierre_previo − cierre_actual y U = 0 si baja (3); ROC(n) = −100 × (último cierre − precio de hace n días) / precio de hace n días  (4) (con signo negativo en el texto); %R = (High(n) − último cierre)/(High(n) − Low(n))  (5) con n = 14.
- **Objetivo binario** (ecuación 6): y_t = +1 si Cierre > Apertura del **siguiente periodo** y −1 si Cierre ≤ Apertura (rentabilidad de apertura a cierre; para diario, del día siguiente).

## A3. Algoritmos (p. 13 a 15; scikit-learn en Python 3.7)

- **Regresión logística con penalización** (ecuación 7): min_{w,c} wᵀw/2 + C·Σ_i log( exp(−y_i(x_iᵀw + c)) + 1 ); C elegido por validación cruzada integrada dentro de la muestra de entrenamiento.
- **Máquina de vectores soporte (SVM)** con núcleo gaussiano (rbf; el núcleo lineal da rendimiento comparable): min_{w,b,ξ} wᵀw/2 + C·Σ ξ_i  sujeto a y_i(wᵀφ(x_i)) ≥ 1 − ξ_i y ξ_i ≥ 0  (8); dual min_α αᵀQα/2 − eᵀα con yᵀα = 0 y 0 ≤ α_i ≤ C  (9), Q_ij = y_i y_j K(x_i, x_j); decisión = signo( Σ y_i α_i K(x_i, x) + ρ )  (10). No se detallan C ni la amplitud del núcleo.
- **Bosque aleatorio** (Breiman, 2001): árboles sobre subespacios aleatorios, votación por mayoría; división por entropía de Shannon o Gini (número de árboles no indicado).
- **Perceptrón multicapa (red artificial):** **dos capas ocultas de 40 y 2 nodos**, activación logística o tangente hiperbólica, retropropagación.

## A4. Diseño de evaluación (p. 17 y p. 18)

- **Partición:** diario **80 % entrenamiento / 20 % prueba** (≈ **63 observaciones de prueba** por moneda, de 317); intradía (15, 30, 60 min) **90 % / 10 %** más **tres subperiodos fuera de muestra de 200, 400 y 600 observaciones** con punto de inicio desplazado ("sub1, sub2, sub3"). **No hay reestimación móvil**: los modelos se ajustan una vez en la muestra de entrenamiento y predicen toda la parte de prueba.
- **Sin ajuste fino por moneda;** sin selección de variables por moneda (los autores dicen que haría subir la exactitud).
- **Tiempos:** diario en segundos; 15 min en minutos para la red.
- **Referentes:** **paseo aleatorio** (1 000 simulaciones por moneda y frecuencia; exactitud media ≈ 0,5, tabla 13) y **ARIMA** elegido por AIC en la muestra de entrenamiento (exactitud dispersa alrededor de 0,5). **No se usa la tasa base (proporción de subidas de la moneda) como referente.**

## A5. Resultados (p. 18 a 23)

**Exactitud fuera de muestra, media entre las 12 monedas (mín–máx):**

| Algoritmo | Diario 80/20 | 60 min 90/10 | 30 min 90/10 | 15 min 90/10 |
|---|---|---|---|---|
| Logística (Tabla 8) | 0,56 (0,48–0,62) | 0,55 (0,48–0,57) | 0,54 (0,50–0,56) | 0,54 (0,50–0,55) |
| SVM (Tabla 9) | **0,59 (0,47–0,69)** | 0,54 (0,50–0,57) | 0,54 (0,51–0,55) | 0,54 (0,50–0,56) |
| Red artificial (Tabla 10) | 0,54 (0,31–0,66) | 0,52 (0,49–0,53) | 0,52 (0,51–0,53) | ≈ 0,52 |
| Bosque aleatorio (Tabla 11) | ajuste en muestra el más alto, fuera de muestra "drásticamente menor" | — | — | — |

- Los subperiodos de 200 a 600 observaciones dan medias entre 0,52 y 0,57 (logística y SVM) y entre 0,46 y 0,57 por moneda. Las **mejores cifras: 69 % para ETH y XMR en diario con SVM**.
- **Dentro de muestra:** SVM diario 0,71; **red 0,91 (hasta 0,98)**; logística 0,63; la distancia entre ajuste en muestra y prueba es máxima en la red y el bosque (**sobreajuste**), con red diaria fuera de muestra de 0,31 en BCH.
- **Conjunto ingenuo** (promedio de los cuatro; Tabla 12): todas las exactitudes por encima de 50 %.
- **Pruebas** (p. 24 a 30): contraste *t* y de Wilcoxon de rangos con signo entre pares de algoritmos y frente a ARIMA, comparando el vector de exactitudes **entre monedas** de cada periodo (Tablas 16 y 17): logística, SVM, red y bosque superan significativamente a ARIMA; entre la logística y la SVM, y entre la SVM y la red, hay diferencias significativas a favor de la SVM en la mayoría de los periodos; entre la SVM y el bosque, y entre la red y el bosque, a veces no significativas (valores t de −0,22 a 1,39 en el diario). **Conjunto de confianza de modelos (MCS)** con pérdida 0–1 y estadístico TR, 10 000 repeticiones bootstrap y **nivel de confianza 75 %** (Hansen y otros, 2011), apilando las pérdidas de las 12 monedas (por ejemplo, 2 400 observaciones en 60 min sub1): **solo la logística y el bosque aleatorio** entran como mejores (el bosque en 6 de 13 escalas; la logística en el resto; Tabla 14); la SVM no aparece como mejor en el MCS de monedas individuales, lo que contradice el mensaje de que la SVM es el mejor modelo.
- **Índices de criptomonedas** (Tabla 15): índice de ponderación igual (EW) y por capitalización (MCW) con las mismas variables; exactitud diaria fuera de muestra alta en el índice (la tabla muestra valores de 0,83 y 0,85 con rango MCS 1, sin que la extracción permita asignarlos con certeza a un algoritmo; verificar en el PDF, p. 26) y de 0,50 a 0,60 en intradía; la SVM es el mejor método en más de la mitad de las escalas (después la red en tres escalas); se atribuye la mayor predictibilidad a la suavidad del índice.

## A6. Conclusión de los autores (p. 27)

La dirección del siguiente periodo es predecible con exactitud sobre 50 % en las 12 monedas y las cuatro escalas, la SVM es el algoritmo más robusto, con un promedio de 55 a 60 % y máximos de 69 %; se viola la eficiencia débil; con ajuste fino se podría superar el 70 %; se advierten implicaciones para valoración de derivados y riesgo sistémico. No se evalúan estrategias de operación ni costes.

## A7. Lectura crítica para la tesis (a verificar)

1. **Muestra de prueba diaria muy pequeña:** 20 % de 317 ≈ 63 días; con p = 0,5 el error estándar del acierto es ≈ 6,3 puntos, de modo que 55–60 % no se distingue del azar; el 69 % de ETH y XMR sale del máximo de 12 monedas × 4 algoritmos × varias escalas (sin corrección por pruebas múltiples).
2. **Tasa base:** la proporción de días al alza de BTC en el periodo completo es 53 %; comparar con 50 % sobrestima. El referente "paseo aleatorio" simulado da 50 % por construcción; no se prueba contra la regla "predecir siempre la clase mayoritaria".
3. **Sin reestimación móvil** y con partición única; no hay costes ni resultados económicos.
4. **Contradicciones internas:** RSI de 9 frente a 6; en MCS gana la logística o el bosque, no la SVM; la media de ARIMA dispersa en 0,5.
5. **Pruebas *t* y Wilcoxon entre monedas** tratan las 12 exactitudes como independientes, pero las monedas están fuertemente correlacionadas entre sí.
6. Coincide con la tabla del proyecto: la dirección intradía de 15 a 60 min con exactitud 54–55 % es compatible con las señales de AUC .54–.55 halladas en 1 h–2 h, pero el artículo no controla fuga ni costes.

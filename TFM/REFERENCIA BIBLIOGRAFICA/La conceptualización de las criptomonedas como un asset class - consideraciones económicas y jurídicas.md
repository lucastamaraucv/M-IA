# La conceptualización de las criptomonedas como un asset class: consideraciones económicas y jurídicas

**Extracción de conocimiento: 2026-10-02** (leídas las páginas 1 a 19, 181 a 200, 203 a 216 de 242; el resto, sobre regulación, blockchain, marco teórico de valoración, optimización de carteras y ESG, **no se leyó completo** y lo que se dice de ellos viene de su índice y de las conclusiones)

| Campo | Valor |
|---|---|
| Título exacto | La conceptualización de las criptomonedas como un asset class: consideraciones económicas y jurídicas |
| Autor / Directores | Miguel Ángel García-Ramos Lucero; directores: Dr. Fernando Gallardo Olmedo (Universidad Autónoma de Madrid) y Dr. Ricardo Rejas Muslera (Universidad Camilo José Cela); tutor: Dr. Juan Ramón Cuadrado Roura |
| Tipo / Venue / Año | Tesis doctoral, Universidad Camilo José Cela, Escuela Internacional de Doctorado, programa de Ciencias Jurídicas y Económicas, Madrid, octubre de 2023 |
| Archivo local | `Tesis Doctoral_MiguelAngel_Garcia-Ramos_Lucero.pdf` |
| URL / DOI | SIN DOI en el documento (**buscar en el repositorio de la universidad o en Dialnet antes de citarlo**) |
| Métodos | Análisis jurídico comparado (Estados Unidos, Unión Europea, España y Japón); análisis estadístico descriptivo y de riesgo con datos diarios de unos 10 años; optimización de carteras; ARIMA con el método de Box y Jenkins; LSTM (Python con TensorFlow y Keras) |
| Datos | Rentabilidades diarias de criptomonedas y otras clases de activos de enero de 2013 a agosto de 2022 (más de 2 500 datos por activo); precio de cierre y volumen de Bitcoin desde el 1 de enero de 2017 hasta el 17 de febrero de 2021 para ARIMA y LSTM (p. 186 y p. 210) |

## Aporte clave

Tesis doctoral en español de economía y derecho que sitúa a las criptomonedas como **clase de activo** y que, en su parte empírica, concluye que **el precio del Bitcoin no es modelable con ARIMA ni con un LSTM y que se comporta como un camino aleatorio** (p. 4, p. 193 y p. 198). Es relevante para mi tesis como marco económico y regulatorio del problema y como un resultado negativo comparado con el método ingenuo.

## Hallazgos cuantitativos (HECHO, con página)

**Parte de predicción de series temporales**
- **ARIMA (método de Box y Jenkins, p. 181 a 193):**
  - sobre el nivel del precio el coeficiente autorregresivo es 0,9945 (± 0,0038), "peligrosamente cerca de 1", lo que viola la estacionariedad en media y da predicciones explosivas (p. 183);
  - en diferencias, el coeficiente cae a −0,0586 (± 0,0307) y el valor p es 0,0564, apenas por encima de 0,05: **el término autorregresivo casi no explica nada** (p. 184);
  - los residuos se comportan como ruido blanco según Ljung-Box (valores p de 0,14 a 0,40 entre 6 y 48 retardos) (p. 185 y p. 186);
  - añadir el volumen de operaciones (en logaritmo, retardos 0 a 2) mejora el ajuste explicativo, pero **no sirve para predecir** porque exige conocer el volumen del propio día; con el volumen solo en t−2 el coeficiente es 1,2955 ± 0,7334 (p. 188 y p. 189);
  - se detectan cuatro valores atípicos (21 y 22 de agosto de 2018; 8 de mayo de 2019; 16 de octubre de 2020) (p. 190 y p. 191).
- **Error del ARIMA frente al referente ingenuo** (p. 192 y p. 193): el MAPE del ARIMA en el periodo de prueba es del 8 %; un modelo ingenuo que predice el valor del día siguiente "da un error del 0,08 %, un 1 % del obtenido con el ARIMA". Conclusión: el ARIMA no es un buen modelo para BTC-USD, porque es un camino aleatorio o porque las relaciones no son lineales.
- **LSTM** (p. 193 a 209): entrada de 5 días para predecir el siguiente, partición cronológica 80/20, escalado mín-máx; pérdida de prueba de 0,00378 (escala normalizada); ajuste de hiperparámetros por pasos (tasa de aprendizaje 0,0001, 500 épocas); **predicción a 365 días después del 17 de febrero de 2021** con MSE de 9,91 y RMSE de 3,15 (según la tabla de la p. 196; el tercer valor de esa tabla, 6 949 536,98, no queda claro a qué métrica corresponde). El texto concluye que **el resultado "no fue satisfactorio"**, que el MAPE "no puede considerarse porque el LSTM no predijo correctamente la serie", que el modelo solo pronostica incrementos positivos y que "muestra poca capacidad de predicción" (p. 197 y p. 198).

**Parte económica (conclusiones, p. 210 a 216)**
- **Rentabilidad y riesgo:** de enero de 2013 a agosto de 2022 el Bitcoin es el activo más rentable, **11,9 veces** superior a la bolsa estadounidense (el siguiente), con una desviación típica anualizada cercana al **105 %** (p. 210 y p. 211).
- **Distribución:** las rentabilidades son **leptocúrticas** (curtosis alta, colas pesadas) y no normales, con asimetría positiva; la gestión de riesgos basada en la normalidad no basta (p. 213 y p. 214).
- **Correlación:** muy escasa con los demás activos financieros (p. 214).
- **Optimización de carteras:** incluye criptomonedas en la cartera óptima junto a bolsa estadounidense y bonos europeos, con una asignación inferior al 0,5 % y un ratio de Sharpe de 0,91 frente a 0,57 de la renta fija europea (p. 214).
- **Hipótesis colateral:** no hay estacionalidad de fin de semana; la rentabilidad media absoluta de fines de semana es algo inferior a la de los días laborables (p. 212).
- **Marco regulatorio y jurídico** (índice, p. 9 y p. 10): análisis de las tendencias en Estados Unidos, Unión Europea, España y Japón, y de reglamentos como MiCA (contenido no leído en detalle).
- **Opinión sobre el dinero:** las criptomonedas pueden considerarse activo y medio de intercambio, pero no dinero por no cumplir de forma plena la reserva de valor (p. 213).

## Limitaciones y críticas

- Declarado por el autor: el modelo LSTM no generaliza y necesita más variables (cualitativas, redes sociales, volumen) (p. 198 y p. 199).
- **[OPINIÓN]** **El referente ingenuo del 0,08 % parece incompatible con el movimiento diario típico de Bitcoin (alrededor de 2 % en valor absoluto).** Una de dos: el error está medido en unidades transformadas (logaritmo o escala distinta) o hay un error de cálculo. Por tanto, la cifra concreta (0,08 % y "1 % del ARIMA") debe tratarse con cautela y no citarse sin verificarla. La conclusión cualitativa (el ARIMA no supera al ingenuo) sí coincide con lo que se espera.
- **[OPINIÓN]** El LSTM de 365 días con predicciones recursivas es una tarea muy difícil y casi segura de fallar; el resultado negativo no demuestra que "ningún modelo de redes neuronales" funcione. No se compara con un referente ingenuo en la parte del LSTM, ni se evalúa dirección.
- **[OPINIÓN]** Los ratios de Sharpe de 0,91 y la superioridad de 11,9 veces dependen mucho del periodo (2013-2022 con un auge inicial enorme) y no incluyen costes ni impuestos; son resultados descriptivos, no una predicción.
- **[OPINIÓN]** La tesis es de economía y derecho; las secciones de aprendizaje automático son una aplicación acotada.

## Conexión con mi tesis (red E20)

- **Marco de contexto y justificación** del capítulo de introducción: qué es el Bitcoin como activo, su volatilidad extrema, la curtosis alta y la baja correlación con otros activos; sirve para justificar métricas no basadas en normalidad.
- **Resultado negativo en español con referente ingenuo:** ARIMA y LSTM no baten al camino aleatorio; coincide con la línea de mi conclusión de que E20 empata con los referentes simples. Una referencia doctoral más para respaldar la honestidad de un resultado negativo.
- **Distinción entre explicar y predecir:** el volumen del propio día mejora el ajuste pero no es utilizable para predecir; es el mismo problema de fuga de información que mi protocolo evita (variables disponibles antes del instante de predicción).
- **Datos de apoyo:** desviación típica anualizada de ~105 % para Bitcoin en 2013-2022; se puede contrastar con mi serie diaria fija.
- **Límite para citarlo:** tesis doctoral de derecho y economía; la parte de predicción es breve y con una cifra dudosa. Úsala para contexto y para la conclusión cualitativa.

## Referencias que cita y conviene localizar

Box y Jenkins (1970), series temporales; Markowitz (1952), selección de carteras; Akyildirim, Goncu y Sensoy (2021), predicción de retornos con ML (resumido en esta carpeta); Fischer y Krauss (2018), aprendizaje profundo en mercados; Du y Swamy (2013), redes neuronales y aprendizaje estadístico; Kimoto y Asakawa (1990), redes en mercados financieros; Sánchez-Terán Manzanedo (2022) y Turbay Lopera y Restrepo Ramírez (2022), criptoactivos; el estudio de la CNMV sobre criptomonedas de mayo-junio de 2022; el Informe de Estabilidad Financiera del Banco de España de primavera de 2022. **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (datos, métodos, fundamentos matemáticos y tablas)

Contenido íntegro de los capítulos III (marco teórico de valoración) y IV (estudio económico: carteras, series temporales y LSTM) y de las conclusiones (páginas PDF 107 a 221; numeración interna 96 a 210). **Los capítulos I (blockchain, tokens y criptoactivos) y II (regulación en Estados Unidos, la Unión Europea, España y Japón; páginas 21 a 106 del PDF) son jurídico-descriptivos y no contienen métodos cuantitativos; no se reproducen aquí y quedan resumidos por el índice y las conclusiones (secciones A7 y A8).** Muchas tablas y gráficos de la tesis son imágenes (Tablas 2 a 6, Figuras 2 y siguientes) y su contenido numérico **no se extrae del PDF**; se cita solo lo que el texto afirma. Páginas = páginas internas de la tesis salvo indicación.

## A1. Marco teórico de valoración (cap. III, p. 96 a 109)

- **Teoría cuantitativa del dinero** (Fisher, 1911): M·V = P·T (o P·Q = M·V); para criptoactivos P·Q se sustituye por el volumen de transacciones T, y M = N·P_c con N el número de unidades emitidas y P_c el precio unitario: **P_c = T/(N·V)**; variables adicionales: aceptación como medio de pago, velocidad de circulación, coste eléctrico, oferta limitada y "halving" (la recompensa se reduce a la mitad cada 210 000 bloques, el próximo en 2024).
- **Ley de Metcalfe** (1976): el valor de una red es proporcional a n² (n(n−1)/2 enlaces); crítica de Odlyzko y Tilly (2005: sobrevalora); apoyo de Alabi (2017, ajuste visual para Bitcoin, Ethereum y Dash, y modelo alternativo con valor proporcional a exp(√n)), de Peterson (2018) y de Thomas Lee (2017, 94 % del movimiento del Bitcoin explicado; sin medidas formales) y propuesta de Van Vliet (2018, con el modelo de difusión de Rogers). (La memoria del proyecto y Baquero 2026 recogen que Shanaev y otros 2019 hallaron esta relación espuria.)
- **Valor presente neto (VPN)** = Σ FE_n/(1 + k)ⁿ: ineficaz porque los criptoactivos no generan flujos (Lamothe, 2020); ejercicio exploratorio de Alvarado (2020) con crecimiento del 89,37 % entre 2012 y 2019.
- **Teoría del mercado eficiente** (Fama, 1970; formas débil, semifuerte y fuerte); Cortés y Hernández (2021): chi cuadrado (retornos no normales), Ljung–Box y razón de varianza automática (problemas en frecuencias bajas), pruebas de rachas y de Bartels (rechazan la independencia), BDS (solo dos criptomonedas en dos frecuencias no rechazan la aleatoriedad) y R/S de Hurst (pocas monedas con persistencia o antipersistencia): concluyen que no hay eficiencia y proponen arbitraje por cointegración de pares.
- **Finanzas conductuales** (sesgos, heurística, efecto rebaño, sobreconfianza, ilusión de control).
- **Valor metagame**, **análisis fundamental** (Graham y Dodd, 1934; métricas en cadena: direcciones activas, tasa de cómputo, tenedores de largo plazo) y **otras propuestas** (Cuadro 4): Alabi (2017, masa crítica), Aloosh (2018, no existe un precio global), Knutson, Liu y Schlenker (2016, siete motores de valor puntuados de 1 a 5) y Bolt y van Oordt (2016, valor instrumental).

## A2. Teoría de series temporales y redes (cap. IV, p. 110 a 114 y p. 166 a 168)

- Una serie temporal es un proceso estocástico con una muestra de tamaño n = 1 por instante; estacionariedad débil (Kolmogorov): **media constante, varianza constante y covarianza que depende solo de la distancia**; **ruido blanco**: E(a_t) = 0, Var(a_t) = σ², Cov(a_t, a_{t+h}) = 0. Método de **Box y Jenkins**: transformar hasta estacionariedad, ajustar ARMA hasta que el residuo sea ruido blanco, refinar con ARCH o GARCH; luego técnicas no lineales: aprendizaje automático (bosque aleatorio, árboles con refuerzo, SVM; "no reflejan bien las relaciones temporales") y aprendizaje profundo (LSTM; "caja negra").
- Revisión metodológica de antecedentes (p. 114 a 125): carteras de Markowitz (Ma y otros, 2020: cinco criptomonedas más acciones, divisas y materias primas, mejora del Sharpe), Bayes–Stein, Black–Litterman (Platanakis y Urquhart, 2020: mejora en Sharpe y sobre todo en Sortino), 1/N de Liu (2019; ningún modelo clásico lo supera), medida de riesgo "behavioural sigma" (Villamil y Martínez, 2019), dependencia de colas (Huynh y otros, 2020), volatilidad con GARCH, EWMA y EGARCH (Naimy y Hayek, 2018; Katsiampa, 2017: retorno medio diario 0,57 % y desviación 0,0617, AR-CGARCH), varianza realizada (Köchling y otros, 2020) y GARCH-MIDAS (Liang y otros, 2020; el índice de volatilidad del oro GVZ es el mejor predictor de la volatilidad del Bitcoin), agrupamiento de precios (Urquhart, 2017: más de 10 % de las cotizaciones con decimales 00), burbujas (Cheah y Fry, 2015) y el modelo de oferta y demanda P_B = P·Y/(V·B) (Ciaian y otros, 2016).

## A3. Estudio de rentabilidad-riesgo por clases de activos (p. 125 a 148)

- **Hipótesis general:** ¿aportan valor las criptomonedas a la formación de carteras? Tamaño muestral conservador N = Z²·p·q/d² = 1,96²·0,5·0,5/0,03² = **1 068**.
- **Datos diarios, enero de 2013 a agosto de 2022** (>2 500 datos por activo; Bloomberg): Bitcoin/USD; **100 criptomonedas** (el activo "criptomoneda" teórico = media aritmética de sus rentabilidades diarias); índice S&P 500 (media de los 500 valores); Euro Stoxx 50 (media de los 50); 20 divisas frente al dólar (media); renta fija (futuros del bono a 2 y 10 años de Alemania y de Estados Unidos). Los activos tradicionales cotizan de lunes a viernes: **se eliminan sábados y domingos** de estos para no sobreponderar el viernes y se repiten los cálculos por separado.
- **Anualización de la desviación típica:** **σ_anual = σ_diaria·√365 (cripto)** y **σ_diaria·√252 (resto)**. Se calculan en R rentabilidad media anualizada, desviación y **semidesviación** (paquete PerformanceAnalytics 0.9.9-5; solo sesiones con rentabilidad negativa, MAR = 0) para el **ratio de Sortino**, y el ratio de Sharpe.
- **Estacionalidad de fin de semana:** hipótesis "más rentabilidad en fines de semana" → **falsa** (la rentabilidad media en valor absoluto es algo menor en fines de semana; Gráfico 8).
- **Resultados** (texto; las tablas son imágenes): el Bitcoin es el activo más rentable (**11,9 veces** la rentabilidad anual del siguiente, la bolsa americana), con mejor Sharpe y Sortino; **desviación típica anualizada cercana a 105 %**, **5,4 veces** la de la bolsa europea (la siguiente más volátil); los ratios de Sharpe y Sortino dan conclusiones parecidas. Valores extremos: Veritaseum se excluye por una desviación típica de ≈ 30 000 % (dato no válido); Komodo queda como atípico (> 20 %); se usa el método de excesos sobre un umbral (X − u | X > u).
- **Distribución:** asimetría y curtosis (curtosis = E[(X − μ)⁴]/σ⁴; normal = 3): todas las distribuciones son muy leptocúrticas, **las criptomonedas muy asimétricas hacia la derecha** (más días de subidas), la bolsa europea y la renta fija con asimetría negativa.
- **Correlaciones** (Tabla 4, imagen): el Bitcoin tiene "apenas correlación" con el resto de activos; varianza de cartera σ_p² con el término de covarianza.
- **Optimización de Markowitz** con Excel y Solver: maximiza el ratio de Sharpe; suma de pesos 100 %, pesos ≥ 0 (sin cortos), Sharpe de la cartera al menos igual al del mejor activo individual, sin apalancamiento. **Cartera óptima (100 criptomonedas promedio): renta fija europea 89,04 %, renta variable de Estados Unidos 10,49 %, criptomonedas 0,47 %; rentabilidad 3,18 %, desviación típica 3,5 %, Sharpe 0,91 (renta fija europea 0,57).** Con el Bitcoin solo, la optimización asigna **100 %** al Bitcoin (no recomendable). Conclusión de la autoría: "activo apto para la gestión de carteras".

## A4. Finanzas conductuales, ESG y RSC (p. 149 a 165)

Descripción cualitativa de sesgos (confirmación, ilusión de control, sobreconfianza, anclaje, contabilidad mental, encuadre, disponibilidad, rebaño, autoatribución, aversión al arrepentimiento) con ejemplos de prensa de 2021; criterios ESG: consumo energético del Bitcoin (Cambridge, Jiang y otros 2021: pico en 2024), Acuerdo Climático Cripto (CCA: cero emisiones del sector para 2040), cuota de renovables de 78 % (CoinShares 2018) y solo 10 % de los gestores que consideran criptoactivos por no cumplir ESG; RSC 1.0 a 3.0; comisiones de pagos del 2–3 %.

## A5. Estudio ARIMA del precio del Bitcoin (p. 166 a 182; PDF 177 a 193)

- **Serie:** **1 081 observaciones diarias** del cierre BTC-USD (18 de diciembre de 2017 al 2 de febrero de 2021), con fines de semana; frecuencia semanal (7) solo para el software; **partición el 15 de noviembre de 2020**; métrica MAPE; paquetes de R `forecast`, `lmtest`, `tsoutliers`.
- **Estacionariedad en varianza:** prueba de Box–Cox con λ = 0,57; transformación X^λ; tras ella λ = 1.
- **AR(1) sobre el nivel:** X^λ_t = μ + φ·X^λ_{t−1} + a_t con **φ = 0,9945 (± 0,0038)** y media 177,5129 (± 24,3150): casi raíz unitaria (predicciones explosivas).
- **AR(1) sobre diferencias:** X^λ_t − X^λ_{t−1} = φ·(X^λ_{t−1} − X^λ_{t−2}) + a_t con **φ = −0,0586 (± 0,0307)**, valor p de la prueba de coeficientes **0,0564**; correlogramas de los residuos dentro de las bandas de Bartlett (±2/√T); **Ljung–Box** (valor p por retardo): 6 → 0,2498; 12 → 0,1401; 18 → 0,2586; 24 → 0,2972; 30 → 0,3192; 36 → 0,3105; 42 → 0,4048; 48 → 0,3694.
- **Con volumen** (Box–Cox λ = 0,11 → logaritmo; retardos 0 a 15): "solución teórica" X^λ_t = X^λ_{t−1} + φ(X^λ_{t−1} − X^λ_{t−2}) + β₁[log V_t − log V_{t−1}] + β₂[log V_{t−1} − log V_{t−2}] + β₃[log V_{t−2} − log V_{t−3}] + a_t con φ = −0,0646 (0,0308), **β₁ = 3,2317 (0,7568), β₂ = 0,9347 (0,7456), β₃ = 2,1328 (0,7577)** (β₂ no significativo); Ljung–Box: 0,2520, 0,1112, 0,2464, 0,2243, 0,2795, 0,2790, 0,3910, 0,3561. **Inútil para predecir** (exige conocer el volumen del propio día). "Solución práctica" solo con V_{t−2}: φ = −0,0594 (0,0307), **β = 1,2955 (0,7334)**; Ljung–Box: 0,2819, 0,1314, 0,2445, 0,2840, 0,3023, 0,2914, 0,3954, 0,3671.
- **Atípicos** (`tsoutliers`, umbral cval = 10): 22 de agosto de 2018 (cambio de nivel), 21 de agosto de 2018 (atípico aditivo), 8 de mayo de 2019 (cambio temporal hasta ≈ 20 de mayo) y 16 de octubre de 2020 (cambio de nivel).
- **Resultado:** **MAPE del ARIMA = 8 %** en la partición de prueba; "un modelo que se limite a predecir el valor del día siguiente da un error del **0,08 %**, un 1 % del obtenido con el ARIMA" → el ARIMA no es buen modelo: "camino aleatorio o relaciones no lineales".

## A6. Estudio LSTM (p. 182 a 198; PDF 193 a 209)

- **Datos:** cierre y volumen del 1 de enero de 2017 al 17 de febrero de 2021; Python con NumPy, pandas, scikit-learn, TensorFlow y Keras; **MinMaxScaler a [0, 1]**; función univariante con ventana de **5 días** (look-back = 5: [1,2,3,4,5] → [6]); **80 % entrenamiento y 20 % prueba** cronológico (no se declara si el escalado se ajustó solo con el entrenamiento; la pre-preparación de datos se describe en general).
- **Hiperparámetros** (descritos, la tabla de valores es imagen): capas, tasa de aprendizaje, función de activación, pérdida **MSE** (MSE = (1/n)Σ(y_i − ŷ_i)²), tamaño de lote, épocas, dropout; ajuste de hiperparámetros: la **tasa de aprendizaje 0,0001** (subirla a 0,001 aumentó la pérdida de prueba), **épocas de 100 a 500**, unidades de 64 a 128 (peor); pérdida de prueba **0,00378** en el primer modelo; el entrenamiento es mayor que la validación (infraajuste según el texto).
- **Predicción:** se predicen los **365 días posteriores al 17 de febrero de 2021** (recursivamente); métricas de error de pronóstico a 1 año: **MSE 9,9124; RMSE 3,1495; MAPE 6 949 536,98 %** (valor imposible que la autora descarta por carecer de sentido); "el modelo únicamente pronostica valores positivos de incremento para el año siguiente" y "poca capacidad de predicción".
- **Conclusión de la autora:** "el objetivo de modelización del precio del Bitcoin parece muy complicado debido a la volatilidad extrema"; mejoras posibles: más variables, de sentimiento y volumen.

## A7. Conclusiones y líneas futuras (p. 199 a 214; PDF 210 a 224)

1. Bitcoin: mejor rentabilidad (×11,9) y mejor binomio rentabilidad-riesgo, pero σ_anual ≈ 105 %; no es dinero (no cumple reserva de valor) pero sí clase de activo; distribuciones leptocúrticas y asimétricas a la derecha; la gestión de riesgo basada en la normalidad no basta.
2. Baja correlación con otros activos; cartera óptima con 0,47 % de criptomonedas y Sharpe 0,91.
3. **Series temporales:** ni ARIMA ni LSTM hallan relación dinámica; "el precio del Bitcoin sigue un camino aleatorio"; causas posibles: estacionalidad no hallada (fin de semana falsa), factores exógenos (precio de la electricidad, prohibición china de la minería de 2021, volumen e identidad de usuarios opaca, shocks de confianza como la quiebra de FTX de 2022, regulación).
4. Aspectos ESG, conductuales y regulatorios (resumidos en el texto principal de la ficha); definición jurídica de los criptoactivos como desafío central; solo El Salvador y la República Centroafricana adoptan el Bitcoin como moneda de curso legal.

## A8. Capítulos I y II (resumen por el índice)

I: blockchain y tokenización, tipos de criptoactivos, principales criptomonedas, diferencias con divisas oficiales, criptografía y datos del mercado (p. 9 a 36). II: tendencias regulatorias en Estados Unidos (p. 37 a 66), la Unión Europea (66 a 76), España (76 a 83) y Japón (83 a 88), con conclusiones (88 a 92).

## A9. Lectura crítica para la tesis (a verificar)

1. **Referente ingenuo mal reportado:** el MAPE de 0,08 % de "predecir el valor del día siguiente" es **muy improbable** con la volatilidad diaria del Bitcoin (≈ 3 % en el periodo de prueba); es un orden de magnitud incompatible con cualquier MAPE de un paso; probablemente **no son comparables** el MAPE del ARIMA (pronóstico de varios días sobre toda la partición) y el del ingenuo (un paso con dato real). Lo defendible es la conclusión cualitativa (φ ≈ 0 en diferencias, residuos ruido blanco) y no la cifra.
2. **Prueba de la hipótesis de camino aleatorio:** el coeficiente en diferencias (−0,0586, p = 0,056) es marginalmente significativo y sin referente formal; no se hacen pruebas de razón de varianzas ni de Diebold–Mariano.
3. **LSTM:** una sola arquitectura, sin repeticiones ni referente; predicción recursiva de 365 días (el error se acumula y el resultado no mide capacidad de un paso); MAPE de 6,9 millones por ciento no es una métrica válida; incoherencia de los términos "infraajuste" y "no aparenta sobreajuste".
4. **Carteras:** el activo "criptomoneda" es el promedio de 100 criptomonedas (con sesgo de supervivencia y reducción de volatilidad por promediar) y la rentabilidad de 2013 a 2022 está dominada por la fase de crecimiento inicial; no hay ventana móvil ni prueba fuera de muestra para la optimización (sesgo de selección ex post).
5. Útil para la tesis como **marco económico y regulatorio**, como contraste con carteras y como **evidencia independiente de camino aleatorio** (con la cautela del punto 1).

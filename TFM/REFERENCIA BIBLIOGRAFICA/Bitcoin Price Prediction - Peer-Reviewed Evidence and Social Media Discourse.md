# Bitcoin Price Prediction: Peer-Reviewed Evidence and Social Media Discourse

**Extracción de conocimiento: 2026-10-02** (leído el texto de las 13 páginas de contenido; las 3 últimas son un apéndice de estudios incluidos que no se leyó)

| Campo | Valor |
|---|---|
| Título exacto | Bitcoin Price Prediction: Peer-Reviewed Evidence and Social Media Discourse |
| Autor | Carlos Baquero (INESC TEC y Facultad de Ingeniería de la Universidad de Oporto, Portugal) |
| Tipo / Venue / Año | Revisión de la literatura, preprint arXiv:2606.00071v1 [q-fin.GN]. El sello del PDF indica "20 May 2026", aunque el identificador de arXiv corresponde a junio de 2026 |
| Archivo local | `2606.00071v1.pdf` |
| URL / DOI | arXiv:2606.00071 (sin DOI de revista en el documento) |
| Métodos | Revisión dirigida (no sistemática) de 23 artículos de predicción de Bitcoin, clasificados por nivel de rigor de la evaluación, y revisión ilustrativa de discusión en X/Twitter con el asistente Grok |

## Aporte clave

Es la fuente más útil de la carpeta para el **capítulo de metodología y de estado del arte crítico**. Su mensaje: en horizontes de 1 a 6 meses ningún estudio revisado por pares ha demostrado superar de forma robusta, en varios regímenes de mercado, al referente ingenuo "el precio de hoy"; la predecibilidad diaria existe pero no llega a horas ni a meses y puede no sobrevivir a los costes; y la necesidad principal del campo **no es más modelos sino mejor evaluación** (p. 1, p. 8 y p. 12). Propone 11 estándares metodológicos concretos (p. 10 y p. 11).

## Conocimiento extraído (HECHO, con página)

**Clasificación por rigor (p. 2)**
- Nivel 1: validación de ventana móvil o progresiva fuera de muestra, idealmente con referente ingenuo. Nivel 2: una sola partición cronológica. Nivel 3: solo dentro de muestra o selección por criterios de información en toda la serie.
- El referente adecuado depende de la tarea: precio de hoy para el nivel del precio; retorno cero para retornos; signo de paseo aleatorio para dirección (Tabla 1, p. 2).

**Evidencia contra modelos complejos**
- Puoti y colaboradores (2024): paseo con deriva y estacional ingenuos superan a 12 modelos (ARIMA, Prophet, bosque aleatorio, XGBoost, LSTM, N-BEATS) a 1, 7 y 30 días; la predicción univariante de criptomonedas es "esencialmente comparable a predecir ruido" (p. 3).
- Arain y Snudden (2025): las mejoras estadísticamente significativas casi nunca dan rentabilidad; solo 2 de 12 índices dan beneficios excesivos y solo en periodos de grandes oscilaciones (p. 3). La precisión direccional fuera de muestra está en la parte baja-media de los 50 %, con un máximo cercano a 57 % (p. 8).
- Yae y Tian (2022): predictores dentro de muestra fallan fuera de muestra; el mejor logra un R² fuera de muestra de hasta 2,7 % en Bitcoin (p. 3).
- Cakici y colaboradores (2024): con más de 500 criptomonedas, OLS supera a árboles y redes neuronales (p. 3).
- Agakishiev y colaboradores (2025): modelos de Markov con cambio de régimen y aprendizaje por refuerzo no mejoran fuera de muestra (p. 3).
- Berger y Koubová (2024): una RNN simple iguala o supera a ARMA-GARCH con retornos diarios, y el LSTM no mejora a la RNN simple (p. 4).
- Baquero y Tinoco (2026), preprint **del propio autor** en revisión: a 1-6 meses, con 5 ventanas de prueba no solapadas de 2016 a 2026, 40 modelos descubiertos por máquina y 18 configuraciones bayesianas, la optimización elige corrección cero en todas (p. 3).
- Magner y Hardy (2022): modelos autorregresivos con retornos rezagados sí superan al paseo aleatorio para algunas de 13 criptomonedas (p. 3). El cuadro no es uniforme.

**Evidencia de predecibilidad a corto plazo (p. 3 y p. 4)**
- Gradojevic y colaboradores (2023): bosque aleatorio con indicadores técnicos supera al paseo aleatorio con datos **diarios**, pero **no con datos por hora**.
- De Nicola (2021): autocorrelación negativa de primer orden a 1-4 horas (reversión a la media); es una caracterización dentro de muestra.
- Guo y colaboradores (2024): los retornos rezagados de otras criptomonedas predicen la propia fuera de muestra, incluso tras costes.
- Gurgul y colaboradores (2025): sentimiento con procesamiento de lenguaje mejora beneficios y Sharpe a nivel diario, aunque frente a comprar y mantener y sin desagregar por régimen.
- Wei y colaboradores (2023): XGBoost el mejor con pruebas de Diebold y Mariano, pero el referente es el mejor de 295 modelos lineales y hay riesgo de sobreajuste de la selección (p. 4).

**Modelos estructurales (p. 4 y p. 5)**
- Relación stock-to-flow: sin capacidad predictiva fuera de muestra (Shelton, 2024), confundida con la tendencia temporal logarítmica (correlación 80,57 %).
- Ley de Metcalfe: relación espuria con variables instrumentales (Shanaev y otros, 2019) y efectos de red poco consistentes (Stylianou y otros, 2021).
- Ley de potencias del precio: ajuste empírico atractivo, pero sin pruebas distribucionales formales de Clauset y colaboradores (2009); Broido y Clauset (2019) encuentran que solo 4 % de unas 1 000 redes tienen estructura de ley de potencias.
- LPPLS: sirve para detectar burbujas, no para predecir niveles (Wheatley y otros, 2019) (p. 5).

**Crisis de la evaluación (p. 5 y p. 6)**
- McNally y colaboradores (2018): acierto direccional de 52 % con una sola partición, que es ruido para un resultado binario. Katsiampa (2017): selección de modelos GARCH por criterios de información sin evaluación fuera de muestra.
- Ninguno de los estudios de nivel 1 evalúa en varias ventanas no solapadas de distintos regímenes.
- Bailey y colaboradores (2014): con muchas configuraciones probadas sobre los mismos datos, la probabilidad de éxito espurio crece rápido.

**Afirmaciones de precisión inflada (p. 8)**
- Las promesas de 95 a 99 % de acierto en redes sociales reflejan métricas de error porcentual del nivel del precio, triviales para cualquier serie persistente.

**Los 11 estándares propuestos (p. 10 y p. 11)**
- Obligatorios: (1) evaluación progresiva o móvil; (2) al menos tres ventanas de prueba no solapadas en regímenes distintos (alcista, bajista, lateral); (3) comparación con el referente ingenuo; (4) incluir el cero en las mallas de hiperparámetros; (5) pruebas de significancia (Diebold y Mariano; conjunto de confianza de modelos).
- Recomendados: (6) significancia económica con costes; (7) declarar tarea y horizonte; (8) vigilar el sobreajuste de backtest y reportar cuántas configuraciones se probaron; (9) publicar resultados negativos; (10) separar descubrimiento y evaluación y evitar fugas de información (estadísticos de preprocesamiento calculados solo con la ventana de entrenamiento); (11) publicar código y particiones.

## Limitaciones y críticas

- Declarado por el autor: la parte de redes sociales es ilustrativa y no exhaustiva; la recuperación con Grok es opaca y no reproducible (p. 2).
- **[OPINIÓN]** La selección de los 23 trabajos no es una revisión sistemática: es dirigida, mezcla trabajos rigurosos con otros solo ampliamente citados, y no hay protocolo de búsqueda reproducible.
- **[OPINIÓN]** **Conflicto de interés a tener en cuenta:** el único estudio con ventanas múltiples y la propuesta de "incluir cero en las mallas" son del propio autor (Baquero y Tinoco, 2026, preprint no revisado). Su "hallazgo" de que los modelos no superan al ingenuo a 1-6 meses depende de un solo estudio propio.
- **[OPINIÓN]** Cubre horizontes largos (1 a 6 meses) y niveles de precio; tiene poco que decir sobre horizontes de minutos u horas, que es donde mi proyecto encontró algo de señal.

## Conexión con mi tesis (red E20)

- **Es la base para mi protocolo:** mi plan ya cumple varios estándares (referente simple, validación cronológica con bloque final, semillas múltiples, pruebas pareadas y corrección de Holm, preregistro de reglas). Debo añadir los que faltan: **más de una ventana de prueba en regímenes distintos** (mi BTC real es una sola serie) y la **prueba de Diebold y Mariano** o el conjunto de confianza de modelos.
- **Coincide con mis resultados:** dirección diaria sin señal (≈ 51 %), media móvil simple como referente difícil de batir, y una mejora estadística pequeña que no supera a los referentes. Gradojevic y colaboradores (daily sí, horario no) y mi hallazgo de que la dirección se predice solo entre 1 minuto y 2 horas apuntan a escalas diferentes; **hay que explicar esa diferencia** (mis escalas y datos distintos) y no darla por contradictoria.
- **Justifica reportar resultados negativos:** apoya la decisión de presentar "E20 empata con los referentes" como resultado válido.
- **Control de fugas de información:** el estándar 10 es la regla que ya sigo (lecturas fijadas antes de ver el bloque final).
- **Límite para citarlo:** es un preprint con autor-parte; conviene citar también los estudios primarios (Puoti, Arain y Snudden, Gradojevic, Berger y Koubová, Cakici).

## Referencias que cita y conviene localizar (DOI según el documento; verificar)

Arain y Snudden (2025), Journal of Forecasting, 10.1002/for.70077; Berger y Koubová (2024), Journal of Forecasting, 10.1002/for.3165 (el PDF de este trabajo está en la carpeta); Gradojevic, Kukolj, Adcock y Djakovic (2023), International Journal of Forecasting, 10.1016/j.ijforecast.2021.08.001; Cakici y colaboradores (2024), International Review of Financial Analysis, 10.1016/j.irfa.2024.103244; Guo y colaboradores (2024), Journal of Economic Dynamics and Control, 10.1016/j.jedc.2024.104863; Gurgul, Lessmann y Härdle (2025), International Journal of Forecasting, 10.1016/j.ijforecast.2025.02.007; Magner y Hardy (2022), Mathematics, 10.3390/math10132338; Agakishiev, Härdle y Becker (2025), Digital Finance, 10.1007/s42521-024-00123-2; Bailey, Borwein, López de Prado y Zhu (2014), Notices of the AMS; Diebold y Mariano (1995); Hansen, Lunde y Nason (2011); Clauset, Shalizi y Newman (2009); Broido y Clauset (2019); Wheatley y colaboradores (2019), burbujas de Bitcoin con LPPLS; Puoti y colaboradores (2024) y Shelton (2024) (sin DOI en el texto visible). **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (método de la revisión, tablas y estándares)

Contenido íntegro de las páginas 1 a 16 del PDF (el resto es la lista de referencias). Es una **revisión de la literatura (arXiv, 20 de mayo de 2026, sin ecuaciones ni experimentos propios)**, por lo que los "fundamentos" son los criterios de evaluación y los resultados de los estudios que cita. Páginas = páginas del PDF.

## A1. Método de la revisión (p. 2 y p. 16)

- **Búsqueda:** Google Scholar y Web of Science con "Bitcoin price prediction/forecasting" (2017–2026, abril de 2026), más seguimiento de citas hacia adelante y atrás. Unas **120 entradas** revisadas por título y resumen; ≈ **40** textos completos; **23 estudios retenidos**. Inclusión: estudios con evaluación fuera de muestra (por rigor) y estudios muy citados de metodología débil (para ilustrar el estado del campo).
- **Niveles de evaluación:** **Nivel 1** = ventana móvil o expansiva fuera de muestra (los mejores incluyen referente ingenuo o de paseo aleatorio); **Nivel 2** = una sola partición cronológica; **Nivel 3** = solo en muestra o selección por criterios de información (AIC, BIC) con toda la muestra.
- **Discurso en redes sociales:** búsquedas dirigidas en X/Twitter con el asistente Grok; ilustrativo, no exhaustivo ni reproducible (cobertura opaca).
- **Uso de IA declarado (apéndice B):** Claude (familia Opus 4) para búsqueda y verificación bibliográfica y borradores; GPT-5.4 para comentarios de revisor; las decisiones científicas son del autor.

## A2. Taxonomía de tareas y su referente (Tabla 1, p. 2)

| Tarea | Referente ingenuo | Métrica principal |
|---|---|---|
| Pronóstico del nivel de precio | el precio de hoy | RMSE, MAE |
| Pronóstico del retorno | retorno cero | R² fuera de muestra, MSFE |
| Clasificación de dirección | signo del paseo aleatorio | exactitud, acierto direccional |
| Valoración estructural | ninguno (explicativo) | R² en muestra |
| Detección de burbujas o regímenes | hipótesis sin burbuja | precisión, exhaustividad |

Los resultados de tareas distintas **no son comparables** (ganar al ingenuo en retornos no implica ganarle en niveles).

## A3. Resultados que recoge (por sección)

### A3.1 Dominio del ingenuo en horizontes cortos y medios (p. 2 y p. 3)
- **Puoti y otros (2024):** validación hacia adelante de 12 modelos (ARIMA, Prophet, bosque aleatorio, XGBoost, LSTM, NBEATS…) en criptomonedas a 1, 7 y 30 días; los ingenuos (con deriva, estacional) superan a todos; la predicción univariante "equivale a ruido".
- **Baquero y Tinoco (2026, preprint):** horizontes de 1 a 6 meses con **cinco ventanas de prueba sin solape (2016–2026)**; entre 40 modelos descubiertos por máquina y 18 configuraciones de series temporales estructurales bayesianas (BSTS), la optimización con datos de entrenamiento elige **corrección cero** en todas las ventanas.
- **Arain y Snudden (2025):** VAR bivariantes diarios (octubre de 2021 a febrero de 2024); solo 2 de 12 índices (índice del dólar y compuesto de Shanghái) dan beneficios en exceso, y solo en periodos de grandes oscilaciones; significación estadística ≠ valor económico. La exactitud direccional fuera de muestra queda en la banda baja-media de 50 % (máximo ≈ 57 %, la mayoría cerca de 50 %).
- **Yae y Tian (2022):** predictores en muestra (atención de inversores, volumen, métricas de red) fallan fuera de muestra; solo la correlación estocástica con el mercado de acciones da R² fuera de muestra de hasta **2,7 %** para Bitcoin.
- **Cakici y otros (2024):** más de 500 criptomonedas; la regresión lineal por mínimos cuadrados supera a árboles de regresión y redes neuronales en retornos.
- **Agakishiev y otros (2025):** modelos de Markov ocultos con aprendizaje por refuerzo sin mejora fuera de muestra.
- **Magner y Hardy (2022):** modelos autorregresivos con retornos retardados sí superan al paseo aleatorio en algunas de 13 criptomonedas (más persistentes que las divisas).
- Analogía con el **rompecabezas de Meese y Rogoff (1983)**.

### A3.2 Predictibilidad de corto plazo (p. 3 y p. 4)
- **Gradojevic y otros (2023):** bosque aleatorio con indicadores técnicos, ventana expansiva; **por hora no supera al paseo aleatorio (eficiencia débil), por día sí** de forma significativa.
- **De Nicola (2021):** autocorrelación negativa de primer orden significativa a 1–4 horas (reversión a la media), solo en muestra (nivel 3).
- **Berger y Koubová (2024):** ARMA-GARCH frente a RNN y LSTM en retornos diarios con ventana móvil: la RNN simple iguala o supera a ARMA-GARCH y el LSTM no mejora a la RNN.
- **Kim y otros (2025):** CNN-LSTM para el signo diario con índices bursátiles, materias primas e indicador de caída máxima; una sola partición; sin referente ingenuo (nivel 2).
- **Wei y otros (2023):** redes, SVM y refuerzo de gradiente con sentimiento y volatilidad, ventanas móviles de 6 meses en 2014–2019; gana XGBoost con Diebold–Mariano y conjunto de confianza, pero el referente es **el mejor de 295 modelos lineales** (riesgo de sobreajuste de la selección según Bailey y otros).
- **Gurgul y otros (2025):** clasificación de sentimiento con BART sin entrenamiento sobre noticias y redes; mejora en rentabilidad y Sharpe en validación cruzada móvil (BTC desde agosto de 2011, ETH desde agosto de 2015, ambos hasta marzo de 2023); referente comprar y mantener.
- **Guo y otros (2024):** los retornos retardados de otras criptomonedas predicen a la moneda focal fuera de muestra, con cartera larga-corta rentable tras costes (difusión lenta de la información).

### A3.3 Modelos estructurales y de valoración (p. 4 y p. 5)
- **Stock-to-flow:** Shelton (2024) lo halla explicativo en muestra pero sin poder fuera de muestra; su significación desaparece con efectos fijos de tiempo (correlación 80,57 % con la tendencia logarítmica del tiempo); una asignación táctica que mezcla S2F, Metcalfe, técnicos y sentimiento sí rinde fuera de muestra.
- **Ley de Metcalfe:** Shanaev y otros (2019, documento de trabajo) con variables instrumentales sobre datos por bloque de 6 criptomonedas de prueba de trabajo: la relación es **espuria** (autocorrelación y endogeneidad); Stylianou y otros (2021): efectos de red insuficientemente consistentes.
- **Ley de potencia:** origen en publicaciones informales de Santostasi (2014, 2018); Burger (2019, blog) añade corredores de soporte y resistencia; Santostasi y Perrenod (2026, preprint en Zenodo): P(t) ∼ t^5,69, R² = 0,961, con exponente descompuesto en crecimiento cúbico de direcciones por Metcalfe generalizado. **Faltan** las pruebas de distribución de Clauset y otros (2009), los diagnósticos de residuos y la comparación por criterios de información con otras tendencias. Broido y Clauset (2019): solo el **4 %** de ≈ 1 000 redes reales muestran estructura de ley de potencia genuina.
- **Burbujas:** Wheatley y otros (2019) combinan Metcalfe generalizado con el modelo de singularidad log-periódica de ley de potencia (LPPLS); detecta, no pronostica niveles.

### A3.4 Crisis de evaluación (p. 5 y p. 6)
- McNally y otros (2018): LSTM en una sola partición con **52 %** de acierto en dirección, dentro del ruido; Katsiampa (2017): selecciona variantes GARCH por AIC, BIC y Hannan–Quinn con toda la muestra; Köse y otros (2025): sin referente ingenuo (usa ARIMA); Poyser (2019): solo descomposición en muestra.
- De los 23 estudios, los de nivel 1 usan evaluación hacia adelante, móvil o expansiva **en un único periodo contiguo**; ninguno usa varias ventanas de prueba sin solape de regímenes distintos.
- **Bailey y otros (2014):** si se prueban muchas combinaciones de parámetros sobre datos históricos, la probabilidad de éxito espurio fuera de muestra crece con rapidez.

### A3.5 Discurso en redes (p. 6 a 8)
- Críticas válidas pero informales: violación de los cuatro supuestos de Gauss–Markov al ajustar por mínimos cuadrados la ley de potencia en escala log-log (no estacionariedad, autocorrelación, asimetría, colas gruesas; afectan a la inferencia más que al pronóstico puntual); pruebas formales de leyes de potencia; sobreajuste de backtests; efecto de rezago de las altcoins (estimaciones de 6–8 semanas a 6–8 meses) confirmado por Guo y otros (2024).
- Modelos refutados que persisten (S2F con predicciones de 250 000 a 1 000 000 USD para el ciclo 2024–2028 que se reformulan como "valor"; Metcalfe como señal de infravaloración); afirmaciones de **95–99 % de exactitud** en redes, que reflejan MAPE en muestra sobre niveles de precio (trivialmente alto porque el precio de mañana está a pocos puntos del de hoy), frente a 50–57 % de exactitud direccional fuera de muestra en la literatura revisada.

## A4. Resumen de evidencia (Tabla 2, p. 9)

| Afirmación | Evidencia | Estado |
|---|---|---|
| Ingenuo competitivo hasta 30 días | Puoti '24, Cakici '24, Agakishiev '25 | Apoyada |
| Hay predictibilidad diaria | Gradojevic '23, Berger '24, Gurgul '25 | Apoyada (específica de frecuencia) |
| Ganancia estadística ≠ ganancia económica | Arain '25 | Apoyada |
| S2F falla fuera de muestra | Shelton '24 | Apoyada |
| Efectos de contagio entre criptomonedas | Guo '24, Magner '22 | Evidencia limitada |
| Predictores en muestra fallan fuera | Yae '22 | Un estudio |
| Metcalfe espuria o inconsistente | Stylianou '21, Shanaev '19 | Apoyada |
| Dominio del ingenuo mensual con varios regímenes | Baquero '26 | Un estudio (preprint) |
| La ley de potencia describe la tendencia | Santostasi '26 | Solo ajuste empírico |

## A5. Preguntas abiertas (p. 9 y p. 10)

(1) ¿Algún modelo supera al ingenuo a 1–6 meses en varios regímenes? (2) Modelos no lineales a horizontes mensuales; la hipótesis es que el coste de varianza de cualquier corrección distinta de cero supera la reducción de sesgo. (3) Datos externos (VIX, tasas, dólar, sentimiento, flujo de órdenes) con protocolo multirrégimen. (4) La volatilidad de Bitcoin ha bajado (Baur y Dimpfl, 2021) y se acorta el horizonte a partir del cual la tendencia de ley de potencia aporta más que la persistencia del precio. (5) **Combinación de señales débiles** (Shelton, 2024) con protección frente al sobreajuste. (6) Validación formal de la ley de potencia (máxima verosimilitud, KS, razones de verosimilitud frente a alternativas, diagnósticos de residuos, comparación con tendencias logarítmica, lineal por tramos y polinómica).

## A6. Estándares metodológicos propuestos (p. 10 y p. 11)

**Obligatorios:** (1) evaluación hacia adelante o con ventana móvil; (2) al menos **tres ventanas de prueba sin solape** en regímenes distintos (alcista, bajista, lateral); (3) comparación con el referente ingenuo (precio de hoy o retorno cero); (4) **incluir cero en las mallas de hiperparámetros** (la hipótesis nula debe ser candidata); (5) pruebas de significación: **Diebold–Mariano** por pares y **conjunto de confianza de modelos (Hansen y otros, 2011)** para varios modelos a la vez.
**Recomendados:** (6) valor económico tras costes de transacción; (7) indicar tarea y horizonte explícitamente; (8) protegerse del sobreajuste de backtests, informando el **número de configuraciones probadas**; (9) publicar resultados negativos; (10) **separar descubrimiento y evaluación y evitar la fuga de información** (estadísticos de preprocesamiento calculados solo con la ventana de entrenamiento); (11) publicar código y datos.

## A7. Apéndice A: estudios incluidos (Tabla 3, p. 15)

| Estudio | Tarea | Objetivo | Horizonte | Muestra | Evaluación | Referente | Nivel |
|---|---|---|---|---|---|---|---|
| Puoti '24 | Precio | Precio | 1–30 d | 2020–23 | Hacia adelante | Ingenuo | 1 |
| Baquero '26* | Precio | Precio | 1–6 meses | 2016–26 | Multirrégimen | Ingenuo | 1 |
| Arain '25 | Retornos | Retornos | 1 d | 2021–24 | Expansiva | Ingenuo | 1 |
| Yae '22 | Retornos | Retornos | 1 d | 2017–20 | Expansiva | Ingenuo | 1 |
| Cakici '24 | Retornos | Retornos | Sección cruzada | 2017–23 | Partición fuera de muestra | MCO | 1 |
| Agakishiev '25 | Retornos | Cartera | Diario | 2015–22 | Partición fuera de muestra | Simple | 1 |
| Gradojevic '23 | Retornos | Retornos | 1 h, 1 d | 2015–19 | Expansiva | Paseo aleatorio | 1 |
| Berger '24 | Retornos | Retornos | 1–10 d | 2013–21 | Móvil | Ingenuo | 1 |
| Kim '25 | Dirección | Dirección | 1 d | 2015–22 | Partición fuera de muestra | — | 2 |
| Wei '23 | Retornos | Retornos | 1 d | 2014–19 | Móvil | Mejor lineal | 1† |
| Gurgul '25 | Dirección | Dirección | 1 d | 2011–23 | Validación cruzada móvil | Comprar y mantener | 1† |
| Guo '24 | Retornos | Retornos | Sección cruzada | 2019–23 | Partición fuera de muestra | — | 1 |
| Shelton '24 | Retornos | Retornos | Mensual | 2014–24 | Expansiva | R² fuera de muestra | 1 |
| Shanaev '19* | Valoración | Precio | — | Por bloque | Regresión con variables instrumentales | MCO | 1 |
| Santostasi '26* | Valoración | Precio | — | 2010–26 | En muestra y escalas | — | 3 |
| Wheatley '19 | Burbujas | Burbujas | — | 2010–18 | Detección de régimen | Sin burbuja | 2 |
| McNally '18 | Dirección | Dirección | 1 d | 2013–16 | Una partición | ARIMA | 2 |
| Katsiampa '17 | Valoración | Volatilidad | — | 2010–16 | AIC/BIC | — | 3 |
| Köse '25 | Precio | Precio | 1 d | 2012–24 | Una partición | ARIMA | 2 |
| Poyser '19 | Valoración | Descomposición | — | 2010–17 | En muestra | — | 3 |
| Magner '22 | Retornos | Retornos | 1 d | 2018–22 | Partición fuera de muestra | Paseo aleatorio | 1 |
| De Nicola '21 | Retornos | Retornos | 1–4 h | 2013–20 | En muestra | — | 3 |
| Stylianou '21 | Valoración | Red | — | Desde el inicio | Empírica | — | 3 |

(* = preprint o documento de trabajo; † = sin referente ingenuo o de paseo aleatorio.)

## A8. Uso para la tesis

Las reglas 1–5 y 8–10 de A6 coinciden con el protocolo del proyecto E20 (referente de retorno cero, Diebold–Mariano, bloque final intocable, número de configuraciones declarado). Las tareas que el artículo sitúa como las únicas con evidencia (diario, y reversión de 1 a 4 horas en muestra) enlazan con la tabla de predictibilidad por temporalidad del proyecto (dirección solo en 1 min a 2 h).

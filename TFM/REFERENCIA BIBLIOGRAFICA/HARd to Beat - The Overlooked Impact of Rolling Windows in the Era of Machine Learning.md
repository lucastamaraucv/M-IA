# HARd to Beat: The Overlooked Impact of Rolling Windows in the Era of Machine Learning

**Extracción de conocimiento: 2026-10-02** (leídas las páginas 1 a 30 de 39; las restantes son apéndices con tablas de los subconjuntos DJIA y Nasdaq-100 y los candidatos de hiperparámetros)

| Campo | Valor |
|---|---|
| Título exacto | HARd to Beat: The Overlooked Impact of Rolling Windows in the Era of Machine Learning |
| Autores | Francesco Audrino y Jonathan Chassot (Universidad de St. Gallen, Suiza) |
| Tipo / Venue / Año | Preprint, arXiv:2406.08041v1 [q-fin.ST], 12 de junio de 2024 |
| Archivo local | `2406.08041v1.pdf` |
| URL / DOI | arXiv:2406.08041 (sin DOI de revista en el documento) |
| Métodos | Modelo autorregresivo heterogéneo de volatilidad realizada (HAR, Corsi 2009) con y sin el índice VIX, estimado por mínimos cuadrados ordinarios o ponderados, por activo o agrupado; frente a lasso, bosque aleatorio, árboles con refuerzo de gradiente y red neuronal de propagación hacia adelante |
| Datos | 1 445 acciones estadounidenses con datos intradía de la base TAQ del NYSE, del 1 de enero de 2015 al 31 de octubre de 2023; volatilidad realizada con intervalos de 5 minutos (p. 6 y p. 7) |

## Aporte clave

Demuestra que **el rendimiento del modelo HAR depende mucho de cómo se ajusta**: la frecuencia con que se reestima y el tamaño de la ventana de entrenamiento. Con un ajuste bien elegido (reestimar a diario con una ventana móvil de 630 días), los modelos de aprendizaje automático (ML) **no superan** al HAR, y los estudios que sí dicen que el ML gana lo hacen frente a un HAR mal ajustado (p. 1, p. 3 y p. 5).

## Hallazgos cuantitativos (HECHO, con página)

- **Frecuencia de reestimación:** el error del HAR empeora mucho si no se reestima a diario, incluso cada 2 o 5 días; la ventana óptima es de unos dos años y medio a cuatro años (Figura 1, p. 3 y p. 4).
- **Esquema usado para el HAR:** ventana móvil de 630 días con reestimación diaria (460 reestimaciones en el periodo de prueba). Para el ML se usa una ventana estática (64 % entrenamiento de enero de 2016 a diciembre de 2020, 13 % validación en 2021, 23 % prueba de enero de 2022 a noviembre de 2023) (p. 13 y p. 14).
- **Información de entrada:** solo la serie de volatilidad realizada y el VIX; al ML se le añaden además 100 retardos de la serie (p. 12).
- **Error cuadrático medio (MSE) medio sin VIX** (Tabla 4, p. 18): HAR (OLS) 0,425; HAR (WLS) 0,432; lasso 0,432; bosque aleatorio 0,451; refuerzo de gradiente 0,463; red neuronal 0,559. Con VIX: HAR (OLS) 0,419 y red neuronal 0,568.
- **Pérdida QLIKE media sin VIX** (Tabla 5, p. 20): HAR (WLS) 0,314 (el mejor); HAR (OLS) 0,333; lasso 0,341; bosque aleatorio y refuerzo de gradiente 0,350; red neuronal 0,477.
- **Conjunto de confianza de modelos (MCS) al 95 %** (Tabla 3, p. 17): con la pérdida QLIKE el HAR (WLS) con VIX pertenece al mejor grupo en 85,5 % de las acciones; el lasso con VIX, 70,9 %; la red neuronal, 36,4 % como máximo.
- **VIX:** añadirlo mejora de manera sistemática, sobre todo en los modelos no agrupados (p. 17).
- **Utilidad económica realizada** (Tablas 6 y 7, p. 21 y p. 22): el HAR (WLS) es el mejor también en términos económicos, con o sin costes de transacción; el tope teórico es de 4 % de la riqueza (SR²/2γ con razón de Sharpe de 40 % y aversión al riesgo 2). Con costes y sin VIX, un inversor con el lasso pagaría 8,7 puntos básicos por acceder al HAR (WLS) (p. 19).
- **Coste de cómputo** para un activo (AAPL, Tabla 2, p. 13): HAR (OLS) 1,77 segundos con 460 reestimaciones; lasso 12,88 s; bosque aleatorio 13,16 s; red neuronal 24,53 s, y estos tiempos del ML son **una sola** estimación con ventana estática.
- **Tabla 1 (p. 5):** los estudios previos que usaron reestimación diaria y ventanas largas encuentran que el HAR es competitivo o gana; los que usan esquemas subóptimos encuentran que el ML gana. Zhang y colaboradores (2023) reestiman el HAR cada 250 días, lo que perjudica mucho al HAR (p. 13).
- **Bitcoin:** cita a Qiu (2021), que encuentra que una regresión de vectores de soporte supera al HAR en datos de Bitcoin, con una ventana de solo 100 observaciones (p. 4 y Tabla 1, p. 5).

## Métodos y diseño experimental

- Volatilidad realizada logarítmica diaria de datos de 5 minutos (ecuación 1, p. 6). HAR con componentes diario, semanal (5 días) y mensual (22 días) (ecuaciones 2 y 3, p. 8).
- Hiperparámetros del ML ajustados por activo en la validación; el objetivo declarado no es la optimización exhaustiva, sino mostrar que modelos de ML "tal cual" no superan a un HAR bien ajustado (p. 14).
- Comparación estadística: conjunto de confianza de modelos (Hansen, Lunde y Nason, 2011) por activo (p. 15).
- Utilidad realizada con el marco de Bollerslev, Hood, Huss y Pedersen (2018) (ecuación 7, p. 16).

## Limitaciones y críticas

- Declarado por los autores: el conjunto de información se limita a la volatilidad realizada y el VIX; no se probaron variables adicionales como sentimiento o características de la empresa (p. 5 y p. 12). La búsqueda de hiperparámetros no es exhaustiva (p. 14).
- **[OPINIÓN]** **Hay una asimetría reconocida por los propios autores**: el HAR se reestima cada día con ventana móvil, y el ML se entrena una sola vez con ventana estática, por coste de cómputo (p. 12 y p. 13). Esto favorece al HAR en la comparación, aunque los autores lo justifican por el coste.
- **[OPINIÓN]** Son acciones de Estados Unidos y volatilidad con datos intradía de 5 minutos; no es Bitcoin ni predicción de dirección.

## Conexión con mi tesis (red E20)

- **Línea de volatilidad y opciones (F4):** mi regla de comparar un pronóstico HAR con la volatilidad implícita (DVOL) es la misma familia de modelos. Este trabajo es el respaldo de usar HAR como referente fuerte, y de añadir un índice de volatilidad implícita (DVOL en Bitcoin juega el papel del VIX).
- **La reestimación importa tanto como el modelo:** al comparar E20 con ML hay que aplicar a **todos** el mismo calendario de reestimación; si el referente se reestima y E20 no, la comparación no es justa (o al revés).
- **Referente que hay que ganar:** concuerda con mis resultados de que una media móvil simple de |retorno| iguala a E20. Un HAR bien ajustado es un referente aún más exigente para la tesis.
- **Metodología prestable:** conjunto de confianza de modelos, pérdida QLIKE y utilidad realizada con costes son instrumentos recomendables para comparar modelos de volatilidad en el capítulo de metodología.
- **Límite para citarlo:** equities, no Bitcoin; usa volatilidad realizada intradía.

## Referencias que cita y conviene localizar

Corsi (2009), el modelo HAR; Audrino y Knaus (2016) y Audrino, Sigrist y Ballinari (2020), lasso y sentimiento sobre HAR; Clements y Preve (2021), guía práctica del HAR; Christensen, Siggaard y Veliyev (2023), ML para volatilidad; Zhang, Zhang, Cucuringu y Qian (2023); Qiu (2021), regresión de soporte sobre Bitcoin; Liu, Pantelous y von Mettenheim (2018); Bollerslev, Hood, Huss y Pedersen (2018); Hansen, Lunde y Nason (2011), el conjunto de confianza de modelos; Gunnarsson y colaboradores (2024), revisión de predicción de volatilidad con IA; Patton (2011), comparación de predicciones de volatilidad. **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (datos, métodos, fundamentos matemáticos y tablas)

Contenido técnico íntegro de las páginas 1 a 30 del PDF (39 páginas; las restantes son tablas del subconjunto Nasdaq-100 y los candidatos de hiperparámetros del apéndice D, que no se reproducen). Páginas = páginas del PDF.

## A1. Datos (p. 6 y p. 7)

- **Activos:** de 6 061 acciones consultadas en la base TAQ del NYSE (datos de operaciones de alta frecuencia) del 1 de enero de 2015 al 31 de octubre de 2023, quedan **1 445 acciones** presentes todo el periodo, entre ellas 27 de las 30 del Dow Jones (DJIA) y 69 del Nasdaq-100. Se cruzan con la base de acciones de CRSP por símbolo. El tratamiento de los datos sigue a Barndorff-Nielsen, Hansen, Lunde y Shephard (2009).
- **Volatilidad realizada (RV):** estimador logarítmico con intervalos de **5 minutos**: RV_t = log( Σ_{i=0}^{m−1} r²_{t−Δi} )  (ecuación 1), con r el retorno logarítmico intradía de Δ = 5 minutos y m el número de intervalos del día. El logaritmo es el estimador que supera a su versión estándar (Clements y Preve, 2021). No se tratan de forma específica los saltos ni el ruido de microestructura (nota 1).
- **Información usada:** solo la serie de RV y el índice de volatilidad implícita **VIX**.
- **Referencias** (Figura 1, Tabla 1): esquemas de ajuste del HAR en estudios previos:

| Estudio | Ventana | Tamaño de entrenamiento | Paso | Activos |
|---|---|---|---|---|
| Audrino y Knaus (2016) | móvil | 200, 400, 1 000, 2 000 | 1 | 9 |
| Audrino, Sigrist y Ballinari (2020) | móvil | 502 | 1 | 19 |
| Christensen, Siggaard y Veliyev (2023) | móvil | no indicado | no indicado | 29 |
| Liu, Pantelous y von Mettenheim (2018) | móvil | 22, 63, 126, 252, 504 | 1 | 4 |
| Qiu (2021) | móvil | 100 | 1 | 1 (Bitcoin) |
| Zhang, Zhang, Cucuringu y Qian (2023) | expansiva | 250 | 250 | 100 |
| Este trabajo | móvil | 630 | 1 | 1 445 |

## A2. Fundamentos matemáticos y modelos (p. 8 a 12)

**Modelo HAR** (Corsi, 2009), con RV_{i,t}^{(d)} el logaritmo de la volatilidad realizada diaria de la acción i:

- RV^{(d)}_{i,t+1} = c + β^{(d)}·RV^{(d)}_{i,t} + β^{(w)}·RV^{(w)}_{i,t} + β^{(m)}·RV^{(m)}_{i,t} + ε_{i,t+1}  (ecuación 2)
- RV^{(w)}_{i,t} = (1/5)·Σ_{h=1}^{5} RV^{(d)}_{i,t−h+1}  y  RV^{(m)}_{i,t} = (1/22)·Σ_{h=1}^{22} RV^{(d)}_{i,t−h+1}  (promedios semanal y mensual)
- **HAR-VIX:** se añade β^{(v)}·VIX_t  (ecuación 3).
- {ε_{i,t}} es una innovación de media cero. Estimación por **mínimos cuadrados ordinarios (OLS)** o **ponderados (WLS)**, por activo o **agrupada** (pooled): 8 especificaciones en total (HAR y HAR-VIX × OLS y WLS × individual y agrupada).

**Lasso** (Tibshirani, 1996): β̂ = argmin_β { (1/(2n))·‖y − Xβ‖₂² + λ·‖β‖₁ }  (ecuación 4). λ controla la contracción; coeficientes de variables poco relevantes se anulan.

**Bosque aleatorio** (Breiman, 2001): (1) muestra bootstrap de los datos; (2) cada árbol se hace crecer con un subconjunto aleatorio de variables en cada división; (3) se repite para formar el bosque y se promedian las predicciones.

**Árboles con refuerzo de gradiente** (Friedman, 2001): (1) modelo base (la media); (2) cada árbol nuevo se ajusta a los residuos del modelo actual; (3) suma ponderada con la tasa de aprendizaje.

**Red de propagación hacia adelante (FFNN)** (perceptrón multicapa): capas totalmente conectadas con pesos; aproximador universal (Hornik, 1991).

**Pérdidas estadísticas** (p. 15):
- MSE_i = (1/T)·Σ_{t=1}^{T} ( RV^{(d)}_{i,t} − R̂V^{(d)}_{i,t} )²  (ecuación 5)
- QLIKE_i = (1/T)·Σ_{t=1}^{T} [ exp(RV^{(d)}_{i,t}) / exp(R̂V^{(d)}_{i,t}) − ( RV^{(d)}_{i,t} − R̂V^{(d)}_{i,t} ) − 1 ]  (ecuación 6, Patton 2011)

**Conjunto de confianza de modelos (MCS)** (Hansen, Lunde y Nason, 2011) al **95 %** por acción con MSE y QLIKE; se reporta el porcentaje de acciones en las que cada modelo pertenece al conjunto de los mejores.

**Utilidad realizada** (Bollerslev, Hood, Huss y Pedersen, 2018), con SR la razón de Sharpe y γ la aversión al riesgo:
- RU_t = (SR²/γ)·[ sqrt( exp(RV_{t+1}) / exp(R̂V_{t+1}) ) − ½·exp(RV_{t+1}) / exp(R̂V_{t+1}) ]  (ecuación 7)
- Con γ = 2 y SR = 40 %, un modelo perfecto logra como máximo SR²/(2γ) = **4 %** de la riqueza. Se interpreta como el porcentaje de riqueza que un inversor pagaría por tener el pronóstico. Con costes de transacción se usa la **mediana móvil de nueve meses del diferencial oferta-demanda**.

## A3. Esquema de estimación (p. 12 a 14)

- **Información de los modelos de ML:** las 1 445 series de RV más **100 retardos** de la serie y el VIX; ajuste de hiperparámetros por acción en la validación (candidatos en el apéndice D); el objetivo no es la optimización exhaustiva.
- **ML con ventana estática:** entrenamiento de enero de 2016 a diciembre de 2020 (≈ 64 %), validación enero de 2021 a diciembre de 2021 (≈ 13 %), prueba enero de 2022 a noviembre de 2023 (≈ 23 %).
- **HAR con ventana móvil de 630 días y paso 1:** 460 reestimaciones en el periodo de prueba. Elección basada en la Figura 1: el rendimiento del HAR depende mucho del paso (peor si no se reestima a diario, aun cada 2 o 5 días) y es estable para ventanas de dos a cuatro años con paso 1; el RMSE medio de la malla va de 0,540 a 0,560 (Figura 1) y también hay un análisis con ventana expansiva (Figura A.3).
- **Costes de cómputo** (Tabla 2, p. 13), segundos para una acción (AAPL), sin VIX / con VIX: HAR (OLS) 1,77 / 1,78; HAR (WLS) 1,86 / 1,88; lasso 12,88 / 13,57; bosque aleatorio 13,16 / 13,13; árboles con refuerzo 5,20 / 5,21; FFNN 24,53 / 25,00. Los del HAR incluyen las 460 reestimaciones; los de ML son **una sola** estimación con ventana estática; reestimar el ML cada día costaría unas 460 veces más.

## A4. Resultados completos (1 445 acciones)

**Tabla 3 (p. 17).** Porcentaje de acciones donde el modelo pertenece al mejor conjunto del MCS (95 %):

| Modelo | MSE sin VIX | MSE con VIX | QLIKE sin VIX | QLIKE con VIX |
|---|---|---|---|---|
| HAR (OLS) | 61,6 | 88,5 | 22,1 | 38,6 |
| HAR (WLS) | 37,9 | 67,7 | 73,1 | 85,5 |
| HAR (OLS, agrupado) | 59,1 | 68,4 | 11,6 | 13,4 |
| HAR (WLS, agrupado) | 42,8 | 65,2 | 56,5 | 53,1 |
| lasso | 58,3 | 70,5 | 20,0 | 70,9 |
| Bosque aleatorio | 46,5 | 50,5 | 25,4 | 49,0 |
| Refuerzo de gradiente | 35,1 | 43,0 | 22,8 | 48,4 |
| FFNN | 11,1 | 17,3 | 14,6 | 36,4 |

**Tabla 4 (p. 18).** MSE medio por acción (percentiles 5, 25, 50, 75, 95 sin VIX):

| Modelo | Media sin VIX | Media con VIX | P5 | P25 | P50 | P75 | P95 (sin VIX) |
|---|---|---|---|---|---|---|---|
| HAR (OLS) | 0,425 | 0,419 | 0,211 | 0,268 | 0,349 | 0,504 | 0,910 |
| HAR (WLS) | 0,432 | 0,425 | 0,214 | 0,270 | 0,353 | 0,515 | 0,936 |
| HAR (OLS, agrupado) | 0,428 | 0,426 | 0,211 | 0,267 | 0,351 | 0,506 | 0,923 |
| HAR (WLS, agrupado) | 0,432 | 0,428 | 0,212 | 0,270 | 0,353 | 0,513 | 0,939 |
| lasso | 0,432 | 0,435 | 0,213 | 0,273 | 0,356 | 0,516 | 0,921 |
| Bosque aleatorio | 0,451 | 0,460 | 0,218 | 0,277 | 0,367 | 0,535 | 0,984 |
| Refuerzo de gradiente | 0,463 | 0,473 | 0,219 | 0,282 | 0,371 | 0,548 | 1,022 |
| FFNN | 0,559 | 0,568 | 0,234 | 0,306 | 0,441 | 0,674 | 1,280 |

**Tabla 5 (p. 20).** QLIKE medio: sin VIX: HAR (OLS) 0,333; HAR (WLS) **0,314**; OLS agrupado 0,346; WLS agrupado 0,329; lasso 0,341; bosque aleatorio 0,350; refuerzo 0,350; FFNN 0,477. Con VIX: 0,332; **0,313**; 0,350; 0,332; 0,320; 0,344; 0,344; 0,571.

**Tabla 6 (p. 21).** Utilidad realizada sin costes (media, % de la riqueza), sin VIX / con VIX: HAR (OLS) 3,152 / 3,149; HAR (WLS) **3,218 / 3,217**; OLS agrupado 3,111 / 3,095; WLS agrupado 3,168 / 3,157; lasso 3,131 / 3,202; bosque aleatorio 3,114 / 3,139; refuerzo 3,119 / 3,151; FFNN 2,796 / 2,367.

**Tabla 7 (p. 22).** Con costes de transacción, sin VIX / con VIX: HAR (OLS) 2,273 / 2,271; HAR (WLS) **2,340 / 2,338**; OLS agrupado 2,233 / 2,217; WLS agrupado 2,290 / 2,278; lasso 2,253 / 2,323; bosque aleatorio 2,236 / 2,261; refuerzo 2,241 / 2,273; FFNN 1,918 / 1,488.

**Subconjunto DJIA** (Tabla B.1, p. 28): el HAR (WLS) con VIX pertenece al mejor MCS por MSE en el **100 %** de las acciones y por QLIKE en 81,5 %; la FFNN, en 11,1 % y 18,5 %. Las tablas de MSE y QLIKE del DJIA (B.2 y B.3) muestran medias de MSE de 0,236 a 0,332 y de QLIKE de 0,157 a 0,237; el HAR vuelve a ser el mejor.

**Diferencia acumulada de errores cuadráticos** (Figura 2, p. 23): incluir el VIX mejora al HAR de forma constante durante todo el periodo; en los modelos de ML la mejora por incluir el VIX aparece al inicio del periodo de prueba y se invierte con el tiempo (el error acumulado con VIX termina por superar al error sin VIX).

## A5. Conclusiones técnicas (p. 21 y p. 22)

Un HAR bien ajustado es un referente robusto de la predicción de volatilidad realizada; los modelos de ML no superan al HAR con ajuste adecuado cuando la información se limita a la RV y el VIX; la FFNN es el peor modelo; el HAR es ligero e interpretable; las discrepancias entre estudios se explican por el esquema de ajuste (reestimación diaria y ventana larga).

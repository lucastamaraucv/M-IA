# Desarrollo de un sistema de gestión del capital basado en redes neuronales para operar en mercados de criptodivisas

**Extracción de conocimiento: 2026-10-02.** Leído el texto completo de los capítulos 1 a 7 (páginas 1 a 72 de 74; las páginas finales son bibliografía y siglas). Las tablas completas de los resultados están reproducidas abajo. Páginas citadas = páginas del PDF.

## 1. Ficha bibliográfica

| Campo | Valor |
|---|---|
| Título exacto | Desarrollo de un sistema de gestión del capital basado en redes neuronales para operar en mercados de criptodivisas |
| Autor | Pedro Gabana Molina |
| Directores | Matilde Santos Peñas y Rodrigo Naranjo Mota |
| Tipo / institución / año | Trabajo Fin de Máster, Máster interuniversitario en Ingeniería de Sistemas y de Control, Universidad Complutense de Madrid y UNED, curso 2021-2022, 7 de junio de 2022 |
| Archivo local | `pfm-pedro-gabana-molina.pdf` |
| DOI / URL | SIN DOI en el documento (repositorio institucional; **comprobar el enlace antes de citarlo**) |
| Software | MATLAB (scripts, "nnstart", Econometric Modeler, Regression Learner, AppDesigner), Excel, NinjaTrader y Alpha Vantage para datos (p. 15 y p. 16, p. 29 a 31) |

## 2. Objetivos y estructura (p. 14 a 17)

- **Objetivo general:** estudiar técnicas de gestión de activos con redes neuronales artificiales aplicadas a criptomonedas (Bitcoin), con un sistema que prediga la evolución y obtenga beneficio reduciendo el riesgo.
- **Dos vías:** (1) entrenamiento supervisado de redes MLP para predecir tendencias y valores, más un sistema de gestión de capital sobre esas predicciones y un sistema experto de stop-loss y take-profit; (2) aprendizaje por refuerzo (Q-learning) con distintas funciones de recompensa.
- **Capítulos:** introducción, conceptos teóricos y estado del arte, datos, predicción con MLP, gestión del capital con MLP, gestión con aprendizaje por refuerzo, conclusiones.

## 3. Fundamentos teóricos (capítulo 2)

- **Velas japonesas ("candle"):** cuatro precios por vela: apertura, cierre, máximo y mínimo; vela blanca si cierre > apertura. En este trabajo **solo se usa el precio de cierre** porque el cierre de un periodo coincide con la apertura del siguiente (p. 20 y p. 29).
- **Operaciones en largo y en corto:** en largo se compra para vender más caro; en corto se vende un compromiso y se gana si el precio baja (riesgo de pérdida ilimitada en corto) (p. 20).
- **Aprendizaje supervisado:** el algoritmo aprende de ejemplos entrada-salida; aquí **regresión** (precio futuro continuo) y **clasificación** (tendencia: 1 subida, 0 igual, −1 bajada) (p. 21).
- **Aprendizaje por refuerzo:** un agente interactúa con un ambiente; estado, acción y recompensa; la ecuación de Bellman actualiza la tabla de políticas Q(s,a) con una tasa de aprendizaje y una tasa de descuento (p. 21 a 23). El texto muestra la fórmula de entrenamiento Q-learning solo como figura.
- **Estado del arte resumido** (p. 24 a 28): sistemas con lógica difusa (Naranjo y otros 2015, 2018, 2019); tratamiento de datos (Velankar y otros, 2018); redes para precios (Ayodele y otros 2012; Pakdaman y otros 2010); Bitcoin con redes bayesianas (Jang y Lee 2017), LSTM (Struga y Qirici 2019) y variables financieras (Dutta y otros 2020); Chen y otros (2020) con diferentes frecuencias; McNally y otros (2018); estudios de MLP y RNN donde la predicción de tendencia a largo plazo ronda el **50 %**; aprendizaje por refuerzo para carteras (Deep Q-Network, gradientes de política, Advantage Actor-Critic en futuros 2011-2019).

## 4. Datos

- **Bitcoin** (p. 32): entrenamiento del 02/01/2015 al 13/04/2020; selección del 14/04/2020 al 14/04/2021; **test del 15/04/2021 al 15/04/2022**. Se descartan los datos anteriores a 2015 por "ruido"; se comparó con el filtrado logarítmico de Velankar y otros con resultados similares, y se descartó.
- **Ethereum** (p. 32): solo test del 15/04/2021 al 15/04/2022 para comprobar si la red entrenada con Bitcoin sirve (resultados no incluidos en el documento).
- **Acciones** (Apple, Microsoft, Google, Amazon, Facebook): usadas para probar el aprendizaje por refuerzo; resultados no incluidos (p. 32 y p. 33).
- **Formato de datos:** función en MATLAB que toma como entrada los precios de cierre de los n días anteriores y como salida el dato del día siguiente (p. 31).
- **Fuentes:** NinjaTrader (exporta .txt) y Alpha Vantage (descarga desde MATLAB) (p. 29 a 31).
- **Aprendizaje por refuerzo:** entrenamiento 02/01/2015 a 14/04/2021 con **2 282 pasos** (sesiones) y **20 episodios** (a partir de ahí las políticas no varían), capital inicial de **1 000 dólares**, 100 simulaciones por sistema para promediar (p. 61).

## 5. Fundamentos matemáticos: métricas (capítulo 3.3 y 3.4, p. 33 a 36)

Error de predicción (n datos; y_i predicho y ŷ_i real en el texto, con notación invertida):
- RMSE = sqrt( (1/n) · Σ (y_i − ŷ_i)² )  (1)
- MAE = (1/n) · Σ |y_i − ŷ_i|  (2)
- Error relativo medio (MRE) = (1/n) · Σ |y_i − ŷ_i| / ŷ_i  (3)
- Tasa de acierto = aciertos / (aciertos + fallos)  (4)
- Tasa sintética de éxito = (TP + TN) / (TP + TN + FP + FN)  (5), con TP = predice subida y hay subida; TN = predice caída y hay caída; FP = predice subida y cae; FN = predice caída y sube. **No cuenta los casos de "sin cambio"**, a diferencia de la tasa de acierto.

Evaluación del sistema de capital:
- Rentabilidad (%) = dinero final / dinero inicial · 100  (6) (en las tablas se reporta como variación porcentual)
- Máximo drawdown: mayor retroceso de la curva de capital respecto de un máximo previo.
- Profit factor = Σ ganancias / Σ pérdidas  (7); mayor que 1 es rentable.
- Ganancia media = Σ ganancias / nº de operaciones ganadoras  (8); pérdida media = Σ pérdidas / nº de operaciones perdedoras  (9).
- Esperanza matemática E = %aciertos · ganancia_media − %fallos · pérdida_media  (10).
- Número de operaciones (fiabilidad estadística del resultado).

Sistema experto de stop-loss y take-profit (p. 56 a 58):
- Fijos: stop-loss = OPEN·(1 − x) y take-profit = OPEN·(1 + x)  (11, 12).
- Por ATR = (HIGH − LOW)/OPEN  (13): stop-loss = OPEN·(1 − k·ATR); take-profit = OPEN·(1 + k·ATR)  (14, 15). Sin resultados buenos.
- Por excursiones máximas adversas (MAE) y favorables (MFE): MAE = (OPEN − LOW)/OPEN en largo y (HIGH − OPEN)/OPEN en corto  (16, 17); MFE = (HIGH − OPEN)/OPEN en largo y (OPEN − LOW)/OPEN en corto  (18, 19). Se fijan **MAE = 5 % y MFE = 2 %**: en largo stop-loss = OPEN·(1 − MAE), take-profit = OPEN·(1 + MFE)  (20, 21); en corto stop-loss = OPEN·(1 + MFE) y take-profit = OPEN·(1 − MAE)  (22, 23).
- Retirada del mercado cuando el capital baje de 800 dólares (pérdida del 20 % de 1 000) al terminar la sesión (p. 56).

## 6. Método: red MLP y sistema de gestión

- **Red:** perceptrón multicapa (MLP) entrenado con una herramienta en MATLAB que busca la mejor configuración: número de datos de entrada (10, 30, 50, 100, 150, 200), 1 o 2 capas ocultas y neuronas por capa (máximo 10 a 20 en la primera y 5 en la segunda) (p. 37 y p. 38). La configuración óptima de valores minimiza el RMSE del periodo de comprobación.
- **Tendencias:** se discretiza la variación en 1 (sube más del margen), 0 (no cambia) y −1 (baja más del margen) con márgenes del **1 %** y del **2 %** (no se estudian márgenes mayores porque variaciones mayores son raras) (p. 41).
- **Sistema de gestión (p. 45):** estrategia "todo o nada" con todo el capital; si la red predice subida se entra en largo, si predice bajada en corto; si la predicción cambia, se sale en la apertura de la siguiente sesión. Se evalúa operando solo en largo, solo en corto (máximo 1 000 dólares) y en ambos. Referente: **comprar y mantener (B&H)**.
- **Aprendizaje por refuerzo (capítulo 6):** sistema que opera solo en largo, parte de un sistema previo ([21] en el documento); entradas: precios de cierre más índices (cambio de precio de cierre y otros siete datos, p. 60); recompensa por **beneficio** (coeficientes de ganancia y pérdida) o por **decisión** (se premia o castiga acertar la tendencia sin importar la cuantía).

## 7. Resultados

**Predicción de valores con MLP** (Tabla 1, p. 39), test 14/04/2020 a 14/04/2021, errores en dólares:

| Entradas | 1 capa: configuración, RMSE, MAE, MRE | 2 capas: configuración, RMSE, MAE, MRE |
|---|---|---|
| 10 | 6, 1 186,97; 678,17; 0,0263 | [10,1], 1 165,93; 659,14; 0,0255 |
| 30 | 8, 1 192,40; 689,82; 0,0272 | [4,3], 1 145,11; 655,74; 0,0257 |
| 50 | 12, **1 151,30**; 678,08; 0,0282 | [14,3], **1 122,70**; 664,84; 0,0271 |
| 100 | 12, 1 182,10; 700,49; 0,0292 | [12,2], 1 164,00; 696,04; 0,0281 |
| 150 | 13, 1 203,53; 716,43; 0,0299 | [13,4], 1 196,67; 747,08; 0,0312 |
| 200 | 7, 1 237,20; 745,32; 0,0317 | [7,3], 1 189,77; 719,15; 0,0302 |

Conclusiones del autor: más capas reducen el error; más entradas no implica mejor ajuste (el mínimo está en 50); todos los errores relativos medios están por debajo del 3,5 %, pero este indicador "no es fiable" para valorar redes en estos niveles de precio (p. 39 y p. 40). El seguimiento es bueno en tendencia y malo en cambios bruscos, con retardo (p. 38 y p. 44).

**Predicción de tendencias** (Tablas 2 y 3, p. 34 y p. 35):

Margen 1 % (tres clases): tasa de acierto de **0,36 a 0,43**. Con 1 capa: 0,37 (10 entradas), 0,37 (30), 0,38 (50), 0,40 (100), 0,38 (150), 0,39 (200). Con 2 capas: 0,36, 0,38, 0,39, **0,43** (100 entradas, [8,3]), 0,41 y 0,39. Tasa sintética de éxito de 0,40 a 0,60 (máxima 0,5965 con 100 entradas y [8,3]).

Margen 2 %: tasa de acierto de **0,53 a 0,57**. Con 1 capa: 0,55, 0,55, 0,54, 0,55, 0,54, 0,53. Con 2 capas: 0,55, 0,57, 0,56, 0,57, 0,56, 0,56. Tasa sintética de éxito de 0 a 0,64 (por ejemplo 0,6429 con 30 entradas y [7,2]; **0** con 150 y 200 entradas de 2 capas, porque la red no predice subidas ni bajadas, solo "sin cambio").

El autor concluye que "acertar más veces no implica tener mayor éxito": importa que los aciertos sean los adecuados; las redes predicen bien tendencias a partir de valores anteriores, pero no acontecimientos inesperados (p. 36).

**Gestión del capital, test 15/04/2021 a 15/04/2022.** Referentes: comprar y mantener en largo: rentabilidad **−35,9 %**, drawdown máximo 52,98 %, profit factor 0,91, ganancia media 19,19, pérdida media 20,94; comprar y mantener en corto: rentabilidad **+56,16 %**, drawdown 55,88 %, profit factor 1,08, ganancia media 42,04 y pérdida media 39,42 (Tablas 4 y 5).

Solo en largo (Tabla 4, p. 39): rentabilidades de −50,27 % a **+22,64 %** (mejor: margen 1 %, 50 entradas, 2 capas, +22,64 %, drawdown 13,11 %, profit factor 1,59, 69 operaciones); muchas configuraciones dan pérdidas (por ejemplo margen 1 %, 150 entradas, 2 capas: −41,22 %). "Prácticamente todos los sistemas se comportan mejor que B&H" porque B&H pierde el 35,9 %.

Solo en corto (Tabla 5, p. 42): rentabilidades de −9,19 % a **+38 %** (mejor: margen 1 %, 50 entradas, 2 capas, +38 %, drawdown 22,14 %, profit factor 1,23, 97 operaciones). "La rentabilidad nunca es mayor que la de B&H en corto" (+56,16 %).

Largo y corto (Tabla 6, p. 45): rentabilidades de −49,81 % a **+68,1 %**. El mejor es margen 1 %, 50 entradas, 2 capas [13,4]: **+68,1 %**, drawdown máximo 11,73 %, profit factor 1,32, ganancia media 16,97 y pérdida media 10,87 con 130 operaciones. Margen 1 % con 30 entradas, 1 capa: +36,72 % (90 operaciones). Margen 2 %: 50 entradas y 1 capa, +35,32 %. Otros: margen 1 %, 150 entradas, 2 capas: −44,61 %.

El autor observa que los mejores resultados salen con 50 entradas y margen de 1 %, y que **ni la tasa de acierto ni la sintética predicen la rentabilidad** (p. 46).

**Sistema experto** (Tabla 7, p. 50 y p. 51), margen 1 %: rentabilidades de −32,84 % a +53,6 % (la mejor: 50 entradas y 2 capas, +53,6 %, drawdown 26,08 %, profit factor 1,12, 478 movimientos). "Tras la aplicación del sistema experto **no se han conseguido mejores resultados**": los stop-loss y take-profit mal escogidos empeoran; el sistema usa la hipótesis pesimista de que el mínimo se alcanza antes que el máximo (p. 51).

**Aprendizaje por refuerzo, recompensa por beneficio** (Tabla 8, p. 53), 100 simulaciones promediadas, solo en largo: rentabilidades de **−16,02 % a −0,52 %** (por ejemplo coeficiente de beneficio y pérdida 1 y 1: −2,55 %, drawdown 40,76 %, profit factor 0,97; con coeficiente de pérdida 2: −3,73 %); todas mejores que B&H largo (−35,9 %) pero **negativas**.

**Recompensa por decisión** (Tabla 9, p. 56): rentabilidades de −22,10 % a **+3,18 %** (la mejor: valor de beneficio 1 y de pérdida −1,5: +3,18 %, drawdown 20,58 %, profit factor 1,08); con valor de pérdida −2 el sistema no opera (0 %); el resto negativas.

**Conclusiones del autor** (p. 60 a 63):
- Las redes MLP "son capaces de competir con los métodos estadísticos y matemáticos" y funcionan bien prediciendo tendencias; no predicen sucesos inesperados.
- Mejor configuración para Bitcoin: margen de 1 % y 50 días de entrada; es mejor entrenar para predecir la tendencia a un día que predecir el valor y derivar la tendencia (el error relativo de 3,5 % supera al 1-2 % que se quiere detectar).
- No se puede predecir en entrenamiento cómo se comportará el sistema en la prueba; fijar stop-loss puede ser contraproducente.
- El aprendizaje por refuerzo "es mejor que el supervisado en el mercado de Bitcoin" porque no necesita discretizar tendencias; conviene penalizar más las pérdidas que premiar las ganancias (si se penaliza demasiado el sistema "coge miedo" y no invierte); premiar la decisión es mejor que premiar el beneficio.
- Trabajo futuro: LSTM, nuevas funciones de recompensa, sistema experto sobre el aprendizaje por refuerzo, otras criptomonedas.

## 8. Limitaciones y críticas

- Declarado por el autor: el rendimiento pasado no garantiza el futuro; los resultados de Ethereum y de acciones no se incluyen; la elección de stop-loss y take-profit es crítica (p. 51, p. 59 y p. 67).
- **[OPINIÓN]** **Un solo año de prueba (abril de 2021 a abril de 2022), con Bitcoin en fuerte caída** (comprar y mantener en largo pierde 35,9 %; en corto gana 56,16 %). Con esa tendencia, cualquier estrategia con operaciones en corto "supera" a comprar y mantener en largo; el comparador adecuado de un sistema largo-corto es la media o una estrategia aleatoria con el mismo número de operaciones.
- **[OPINIÓN]** **Selección sobre el mismo periodo que se evalúa:** las tablas 4 a 7 comparan 24 configuraciones sobre el periodo de prueba y se destaca la mejor (+68,1 %). No hay corrección por comparaciones múltiples y el propio autor admite que no se puede predecir en entrenamiento cuál rendirá en prueba; es muy probable que el máximo sea ruido.
- **[OPINIÓN]** **No se mencionan comisiones, deslizamiento ni margen de operaciones en corto**, con 20 a 478 operaciones al año, lo que invalida cualquier lectura de rentabilidad neta.
- **[OPINIÓN]** Las tasas de acierto de tendencia con margen de 1 % son 36 a 43 %, por debajo del 50 %, y con margen de 2 % son 53 a 57 % en tres clases en las que la clase "sin cambio" domina; no hay referente (por ejemplo, predecir siempre la clase más frecuente).
- **[OPINIÓN]** El aprendizaje por refuerzo da rentabilidades **negativas** (−0,5 % a −16 %) salvo una configuración de +3,18 %; la conclusión de que "es mejor que el supervisado" se apoya solo en que pierde menos que B&H en un año bajista y en 100 simulaciones de una sola serie.
- **[OPINIÓN]** Una sola semilla de partición, sin intervalos de confianza ni pruebas de significancia; no se indica cuántas realizaciones de la red supervisada se entrenan.
- **[OPINIÓN]** Hay erratas de notación (RMSE con y_i y ŷ_i invertidos; "máximo DraxDown"; MRE dividido por la predicción).

## 9. Conexión con mi tesis (red E20)

- **Ejemplo de máster en español de gestión del capital con redes sobre Bitcoin** (Universidad Complutense y UNED), útil como referencia de estructura y de lo que debe evitarse: evaluación de rentabilidad en un solo año, sin costes, con selección sobre la prueba.
- **Medidas de gestión de capital** (rentabilidad, drawdown máximo, profit factor, ganancia y pérdida media, esperanza matemática): son las que usaría si mi tesis evaluara una política de decisión (línea F4 de opciones); mi pregunta, en cambio, es predictiva y separa la calidad predictiva de la utilidad económica, como pide el protocolo de la guía.
- **Tendencia en tres clases con margen:** análogo a mi "movimiento" y a la discretización; muestra que la elección del margen cambia la tasa de acierto de 0,40 a 0,57 sin cambiar la información, lo que justifica fijar la definición de la etiqueta antes de mirar resultados.
- **Validación cronológica con tres periodos** (entrenamiento, selección y prueba): coincide con mi diseño, aunque el autor selecciona sobre la prueba.
- **Límite para citarlo:** buena fuente de contexto y de ideas de gestión (stop-loss por MAE y MFE), pero no de evidencia de rentabilidad.

## 10. Referencias que cita y conviene localizar

Naranjo, Meco, Arroyo y Santos (2015), "An intelligent trading system with fuzzy" (International Journal of Intelligent Systems, 963-983); Naranjo, Arroyo y Santos (2018), "Fuzzy modeling of stock trading with fuzzy candlesticks" (Expert Systems with Applications); Naranjo y Santos (2019), sistema de decisión con patrones de velas difusas; van den Berg, Kaymak y van den Bergh (2003); Velankar, Valecha y Maji (2018), "Bitcoin price prediction using machine learning" (ICACT); Jang y Lee (2017), IEEE Access, 5427-5437; Struga y Qirici (2019); Dutta, Kumar y Basu (2020), "A gated recurrent unit approach to Bitcoin price prediction" (Journal of Risk and Financial Management); Chen, Li y Sun (2020), "Bitcoin price prediction using machine learning: an approach" (Journal of Computational and Applied Mathematics); McNally, Roche y Caton (2018). **Comprobar cada una con su DOI antes de citarla.**

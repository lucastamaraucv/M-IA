# Predicting Price Movements in High-Frequency Financial Data with Spiking Neural Networks

**Extracción de conocimiento: 2026-10-02** (leído el texto completo de las 9 páginas)

**Nota de duplicados:** en la carpeta hay dos copias idénticas (`2512.05868v1 (1).pdf` y `2512.05868v1 (2).pdf`, mismo contenido de 1 411 KB). Se resume una sola vez.

| Campo | Valor |
|---|---|
| Título exacto | Predicting Price Movements in High-Frequency Financial Data with Spiking Neural Networks |
| Autores | Brian Ezinwoke y Oliver Rhodes (Departamento de Ciencias de la Computación, Universidad de Mánchester, Reino Unido) |
| Tipo / Venue / Año | Preprint, arXiv:2512.05868v1 (diciembre de 2025) |
| Archivos locales | `2512.05868v1 (1).pdf` y `2512.05868v1 (2).pdf` (duplicados) |
| URL / DOI | arXiv:2512.05868 (sin DOI de revista en el documento) |
| Métodos | Redes neuronales espigantes (SNN) con neuronas LIF, entrenadas con STDP no supervisado (modelo de Gao, Luk y Weston, 2021, y una versión extendida con sinapsis inhibitorias) y una SNN supervisada con retropropagación en el tiempo; optimización bayesiana (Optuna) con una nueva métrica, la "exactitud de espigas penalizada" (PSA) |
| Datos | Precio y volumen de la acción AAPL con precisión de microsegundos de los 19 días de negociación de febrero de 2015 (p. 2) |

## Aporte clave

Replica y extiende el enfoque de Gao, Luk y Weston (2021) para predecir "saltos de precio" de alta frecuencia con una SNN, proponiendo (1) una red con **retardos temporales e inhibición explícita** entre canales positivos y negativos, (2) una normalización robusta de la entrada con canales separados para valores positivos y negativos, y (3) una métrica de optimización que penaliza que la tasa de espigas se aleje de la tasa real de saltos (p. 1 a 5).

## Conocimiento extraído (HECHO, con página)

**Preprocesamiento (p. 2 y p. 3)**
- Precio medio ponderado por volumen (VWAP) con ventanas de 10 operaciones, que reduce el tamaño de los datos en 90 % y suaviza el ruido entre oferta y demanda.
- Se usan **diferencias de precio** en lugar del precio, para quitar la tendencia y evitar sesgos horarios en la tasa de espigas.
- **Normalización robusta:** escalado con el rango intercuartílico [0,1 y 0,9] y recorte de valores extremos; separación en un canal positivo y otro negativo (porque la codificación de Poisson exige valores no negativos); reescalado a [0, 1] (p. 3). Esto sustituye una normalización con parámetros ajustados por búsqueda, sensible a valores atípicos.
- **Codificación de Poisson** con 20 pasos de tiempo por dato (p. 3).

**Definición del objetivo (p. 3 y p. 4)**
- Una **espiga de precio "real"** ocurre cuando el movimiento absoluto medio de las siguientes w observaciones supera la **mediana** de los retornos absolutos del día. Es un objetivo de **magnitud (movimiento)**, no de dirección, igual que el "movimiento" de mi trabajo.
- Las espigas reales se clasifican en "momentum" (continúan la tendencia previa) o "reversión" (la invierten).

**Métricas de la red (p. 4)**
- Precisión de espigas (SA), porcentaje de espigas de momentum, tasa de espigas, tasa de verdaderos positivos y de falsos positivos.
- **PSA = SA multiplicada por un factor de penalización** que cae si la tasa de espigas del modelo se desvía de la tasa real (tolerancia α = 0,05; ecuaciones 8 a 10). Motivo: optimizar solo SA favorece redes que disparan muy poco.

**Modelos (p. 4 y p. 5)**
- Modelo 1: red de doble entrada con STDP y homeostasis sináptica (pesos entre 0 y 1; reducción del 5 % si el peso medio pasa de 0,5).
- Modelo 2: añade k retardos de precio (hasta 10) y **sinapsis inhibitorias con peso entre −1 y 0** que cruzan los canales (X1 hacia H2 y X2 hacia H1) para aislar el momentum.
- Modelo 3: SNN totalmente conectada supervisada (128 neuronas ocultas, retropropagación en el tiempo, gradiente sustituto sigmoide rápido, retardos 1, 3 y 5; entradas retornos, volatilidad y volumen).

**Resultados predictivos** (Tabla VI, p. 7)
- Precisión de espigas: modelo aleatorio 59,85 %; Modelo 1 con SA 73,85 % y con PSA 62,67 %; Modelo 2 con SA 67,13 % y con PSA 65,11 %; Modelo 3 69,35 %.
- Tasa de espigas: aleatorio 50 %; Modelo 1 SA 10,58 % y PSA 64,31 %; Modelo 2 SA 11,15 % y PSA 44,69 %; Modelo 3 31,83 %.
- Porcentaje de espigas de momentum: todos entre 54,3 % y 55,1 %, prácticamente igual al 54,47 % del azar.

**Resultados de trading simulado** (Tablas VII y VIII, p. 8; solo con la estrategia de momentum entrando en cada espiga)
- Rendimiento acumulado escalado a 1 000 operaciones al día: Modelo 2 con PSA 17,44 %; Modelo 1 con PSA 15,48 %; Modelo 1 con SA 15,49 %; Modelo 2 con SA 13,63 %; Modelo 3 12,44 %; ingenuo 13,49 %; aleatorio 12,71 %.
- Razón de Sharpe en esa tabla entre 10,7 y 19,7; tasa de aciertos de 52,3 % a 53,5 %.
- Sin escalar (Tabla VIII): Modelo 1 con PSA 82,41 % (101 126 operaciones); Modelo 2 con PSA 76,80 % (83 673); Modelo 3 42,47 % (51 229).

## Limitaciones y críticas

- Declarado por los autores: la literatura de finanzas cuantitativas necesita más pruebas comparativas con SNN revisadas por pares y métricas estandarizadas; la eficacia práctica de PSA requiere más análisis (p. 7 y p. 8).
- **[OPINIÓN]** **El resumen es más optimista que las tablas.** El resumen dice que el modelo extendido logra el mayor rendimiento acumulado (76,8 %), pero en la Tabla VIII el Modelo 1 con PSA tiene 82,41 %, más alto. En la Tabla VII (escalada) el mejor sí es el Modelo 2 con PSA, pero por 1,95 puntos sobre el siguiente, sin intervalo de confianza.
- **[OPINIÓN]** El porcentaje de espigas de momentum de todos los modelos (≈ 55 %) es igual al del azar (54,5 %); la afirmación de que esto "confirma una predicción direccional fiable" (p. 7) no está respaldada: indica que la red no aporta información direccional.
- **[OPINIÓN]** La precisión de espigas del modelo aleatorio (59,85 %) es alta porque el umbral es la mediana y la definición de "real" depende de la ventana; los modelos con PSA solo mejoran entre 2,8 y 5,3 puntos sobre el azar.
- **[OPINIÓN]** **No hay costes de transacción ni deslizamiento**, con 80 000 a 100 000 operaciones en 19 días. Las razones de Sharpe de 10 a 20 no son realistas en alta frecuencia con costes. Un día de entrenamiento y otro de prueba, una sola acción (AAPL) y un solo mes.
- **[OPINIÓN]** No queda claro si la optimización bayesiana se evaluó con datos distintos a los de la prueba de trading; hay riesgo de sobreajuste por selección. Cada modelo se repitió solo 3 veces (p. 7).
- El nombre de la métrica aparece como "Penalised" y como "Predictive" Spike Accuracy en distintas partes (p. 6).

## Conexión con mi tesis (red E20)

- **Antecedente directo en SNN financieras:** usa neuronas LIF, STDP, sinapsis inhibitorias y retardos de entrada, que son componentes de E20 (retardos de entrada 0 a 4, STDP, iSTDP).
- **Mismo tipo de objetivo que mi "movimiento":** el objetivo de espiga real es "magnitud del retorno por encima de la mediana", equivalente a mi etiqueta de movimiento (|retorno| mayor o igual al percentil 33). Mis resultados en BTC (movimiento más predecible que dirección) son consistentes con que sea ese el lado donde hay algo de señal.
- **Normalización con canales positivo y negativo:** parecida a mi entrada con signo y volatilidad; sirve de referencia.
- **Lección metodológica:** las tablas de este trabajo son un ejemplo de lo que mi tesis debe evitar: ausencia de costes, un solo activo y un mes, y una afirmación direccional que las tablas no sostienen. Puedo citarlo como estado del arte y señalar esas limitaciones.
- **Inhibición y control de actividad:** apoya que controlar la tasa de espigas (aquí con PSA, en E20 con la iSTDP) es clave; en E20 la tasa de disparo es alrededor de 1 %.
- **Límite para citarlo:** es acción de alta frecuencia, no Bitcoin, y sin validación independiente.

## Referencias que cita y conviene localizar

Gao, Luk y Weston (2021 y 2023), "High-frequency trading and financial time-series prediction with spiking neural networks" (Wilmott); Reid, Hussain y Tawfik (2013), redes espigantes para predicción financiera (IJCNN); Parsa y colaboradores (2019), optimización bayesiana para sistemas neuromórficos; Eshraghian y colaboradores (2023), entrenamiento de SNN (Proceedings of the IEEE); Roy, Jaiswal y Panda (2019), Nature; Bi y Poo (1998), STDP; Sezer, Gudelek y Ozbayoglu (2020), revisión de aprendizaje profundo en series financieras; Akiba y colaboradores (2019), Optuna. **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (datos, métodos, fundamentos matemáticos y tablas)

Contenido técnico íntegro del texto principal (páginas 1 a 8 del PDF; el resto es la bibliografía). Páginas = páginas del PDF.

## A1. Datos y preprocesamiento (p. 2 y p. 3)

- **Datos:** precio y volumen de **AAPL** con precisión de microsegundos, **19 días de negociación de febrero de 2015** (un solo mes y un solo activo).
- **Precio medio ponderado por volumen (VWAP)** con ventana de n = 10 transacciones: VWAP = Σ P_i·V_i / Σ V_i  (ecuación 2); reduce los datos un 90 %.
- **Diferencias de precio** para eliminar la tendencia intradía y el sesgo por magnitud (Figura 2, análisis de componentes no observados).
- **Normalización propuesta** (en lugar de la de Gao y otros, z_i = max{ (x_i − μ_x)/σ_x · σ_norm + μ_norm , 0 }, ecuación 3, que necesita ajustar μ_norm y σ_norm y es sensible a atípicos): (1) escalado robusto con rango del 10 % al 90 % y recorte; (2) separación en un **canal positivo** y otro **negativo** (valores bipolares); (3) reescalado min-max de cada canal a [0, 1] (tasa media ≈ 0,5 picos por paso; se puede bajar el máximo a x < 1 para más dispersión).
- **Codificación de Poisson:** para cada valor x_i se genera un tren de T = **20** pasos con probabilidad de pico p = x_i en cada paso (Algoritmo 1).

## A2. Fundamentos matemáticos

- **Plasticidad dependiente del tiempo de los picos (STDP)** (ecuación 1): Δw = η·W(Δt) con W(Δt) = A₊·exp(−Δt/τ₊) si Δt > 0; −A₋·exp(Δt/τ₋) si Δt < 0; 0 en otro caso; A₋ ≤ A₊; η = 1.
- **Neurona LIF** (ecuación 11): β·dV/dt = −V + R·I(t); el potencial sube con el peso de cada pico recibido; al superar V_thresh emite un pico y se **resta** el umbral (reinicio por sustracción); periodo refractario de un paso; sinapsis basadas en corriente. Salida: número de picos del tren de salida; si supera el **umbral de decodificación D_thresh**, se interpreta como "pico de precio previsto".
- **Pico de precio real:** retorno absoluto r_t = | X_{t+1}/X_t − 1 |  (4); umbral r_thresh = **mediana** de r_t del día (5); fuerza S_strength = (|r_{t+1}| + … + |r_{t+w}|)/w  (6); el pico es **real** si S_strength > r_thresh y **falso** si no. Es decir, la tarea es predecir la **magnitud** del movimiento (mismo tipo de objetivo que el "movimiento |r| ≥ umbral" de E20), no la dirección.
- **Pico de momento o de reversión** (ecuación 7): según el signo de (X_t − X_{t−w})·(X_{t+w} − X_t): positivo = momento; negativo = reversión.
- **Métricas** (Tabla I): precisión de picos = N_previstos_reales / N_previstos; porcentaje de momento; tasa de picos = N_previstos / N_marcas; tasa real de picos; tasa de verdaderos positivos = N_previstos_reales / N_reales; tasa de falsos positivos = N_previstos_falsos / N_falsos.
- **Precisión de picos penalizada (PSA)** (ecuaciones 8 a 10): PSA = Precisión × Factor de penalización, con Factor = exp( −max( |SRD| − α, 0 ) ), α = **0,05** y SRD = (Tasa de picos / Tasa real de picos) − 1. Evita que la optimización prefiera una red casi muda (alta precisión con muy pocos picos).
- **Estrategia de momento con picos** (ecuación 12): F_t = P_t − (1/n)·Σ_{i=1}^{n} P_{t−i} con n = 3; según el Algoritmo 2, F_t < 0 → posición corta y F_t > 0 → larga, mientras que el texto dice lo contrario ("positiva = tendencia bajista → corto"). **Contradicción interna del artículo; verificar antes de citar.**

## A3. Modelos (p. 4 y p. 5)

- **Modelo 1** (Gao y otros, 2021): doble entrada (una neurona para la diferencia positiva X1 y otra para la negativa X2); capa oculta separada en H1 (de X1) y H2 (de X2); una neurona LIF de salida conectada a ambas; aprendizaje **no supervisado** con STDP; homeostasis sináptica: pesos entre 0 y 1 y reducción de 5 % de todos los pesos de la capa si el peso medio supera 0,5.
- **Modelo 2** (extendido, propuesta): k retardos de la diferencia de precios, X1_i ← (P_n − P_{n−i})₊ y X2_i ← (P_n − P_{n−i})₋ con i ∈ [1, k]; **conexiones inhibitorias** cruzadas X1→H2 y X2→H1 con pesos en [−1, 0] y regla Δw = −W(Δt); parámetros propios para el STDP inhibitorio (B₊, B₋, θ₊, θ₋).
- **Modelo 3** (referencia supervisada): SNN totalmente conectada con dos capas ocultas y dos neuronas de salida; entradas retorno, volatilidad y volumen con retardos 1, 3 y 5; retropropagación en el tiempo con gradiente sustituto (sigmoide rápida); pérdida de error cuadrático del conteo de picos (tasa objetivo 80 % para la clase correcta y 20 % para la otra); Adam, tasa de aprendizaje 0,005, 128 neuronas ocultas, V_thresh = 1.

## A4. Diseño experimental (p. 5 y p. 6)

- **Experimento 1:** optimización bayesiana con **Optuna**, **100 iteraciones**, con lotes secuenciales de 5 000 marcas, para PSA y para la precisión de picos (SA), en los Modelos 1 y 2. Espacio de búsqueda (Tabla III): A₊ y B₊ en [10⁻⁴, 10⁻²] log; A₋ en [A₊ − 0,001, A₊]; τ₊ y θ₊ en [5, 100]; τ₋ en [τ₊ − 5, τ₊ + 5]; β en [0,5, 0,99]; V_thresh en [0,8, 2,5]; D_thresh en [4, 16]; N_input en [1, 10]; N_hidden en {16, 32, 64, 128}.
- **Experimento 2:** ventana diaria móvil: se entrena con el día i y se prueba en el día i + 1.
- **Operación simulada:** orden de mercado al VWAP de la marca siguiente; capital normalizado a 1, apalancamiento 1×, una sola posición abierta, cierre tras una duración fija al VWAP de salida; cada modelo se corre 3 veces (100 el aleatorio) y se promedia; los retornos de la Tabla VII se **escalan a 1 000 operaciones por día (19 000 en el mes)**; **no se mencionan comisiones ni deslizamiento**.

## A5. Resultados completos

**Tabla V (hiperparámetros óptimos):**

| Parámetro | M1 SA | M1 PSA | M2 SA | M2 PSA |
|---|---|---|---|---|
| A₊ | 0,0037 | 0,0067 | 0,0096 | 0,0012 |
| A₋ | 0,0032 | 0,0063 | 0,0093 | 0,0009 |
| B₊ / B₋ | – | – | 0,0059 / 0,0052 | 0,0016 / 0,0009 |
| τ₊ / τ₋ | 45 / 42 | 71 / 72 | 74 / 72 | 54 / 58 |
| θ₊ / θ₋ | – | – | 44 / 44 | 51 / 51 |
| β | 0,96 | 0,79 | 0,87 | 0,86 |
| V_thresh | 2,20 | 0,80 | 2,50 | 2,00 |
| N_hidden | 16 | 32 | 128 | 64 |
| N_input | – | – | 1 | 3 |
| D_thresh | 12 | 9 | 12 | 11 |
| Valor del objetivo | 0,90 | 0,76 | 0,77 | 0,71 |
| Desviación de la tasa de picos | −0,69 | −0,01 | −0,43 | +0,078 |

V_thresh y β son los dos hiperparámetros más importantes en todos los casos (Figura 4); PSA aumenta la importancia del umbral de membrana.

**Tabla VI (predicción):**

| Métrica | Aleatorio | M1 SA | M1 PSA | M2 SA | M2 PSA | Modelo 3 |
|---|---|---|---|---|---|---|
| Precisión de picos (%) | 59,85 | 73,85 | 62,67 | 67,13 | 65,11 | 69,35 |
| Picos de momento (%) | 54,47 | 54,34 | 54,49 | 55,08 | 55,06 | 55,09 |
| Verdaderos positivos (%) | 50,00 | 12,96 | 67,33 | 12,51 | 48,62 | 36,88 |
| Falsos positivos (%) | 50,00 | 7,03 | 59,81 | 9,13 | 38,83 | 24,30 |
| Tasa de picos (%) | 50,00 | 10,58 | 64,31 | 11,15 | 44,69 | 31,83 |

(El aleatorio ya logra 59,85 % de "precisión" porque esa proporción de instantes son picos reales; los modelos PSA están entre 2,8 y 5,3 puntos por encima del azar con tasas de falsos positivos de 59,8 % y 38,8 %.)

**Tabla VII (operación, retornos escalados a 1 000 operaciones por día):**

| Métrica | M1 SA | M1 PSA | M2 SA | M2 PSA | M3 | Ingenuo | Aleatorio |
|---|---|---|---|---|---|---|---|
| Retorno acumulado (%) | 15,49 | 15,48 | 13,63 | **17,44** | 12,44 | 13,49 | 12,71 |
| Sharpe | 10,70 | 16,48 | 16,72 | **19,72** | 15,91 | 16,32 | 17,99 |
| Caída máxima (%) | 5,85 | 2,52 | 2,25 | 2,69 | 2,95 | 1,76 | 2,77 |
| Tasa de aciertos (%) | 52,63 | 52,60 | 52,89 | 53,49 | 52,79 | 52,42 | 52,28 |
| Factor de beneficio | 1,15 | 1,21 | 1,16 | 1,22 | 1,13 | 1,18 | 1,17 |
| Razón beneficio/pérdida | 1,00 | 1,09 | 1,03 | 1,06 | 1,01 | 1,07 | 1,07 |
| Expectativa (×10⁻⁶) | 8,15 | 8,15 | 7,17 | 9,18 | 6,55 | 7,10 | 6,69 |

**Tabla VIII (sin escalar):** M1 SA 1,296 de capital final (29,63 %; 36 336 operaciones); **M1 PSA 1,824 (82,41 %; 101 126)**; M2 SA 1,295 (29,52 %; 41 141); **M2 PSA 1,768 (76,80 %; 83 673)**; M3 1,425 (42,47 %; 51 229). El texto atribuye el mayor retorno de los modelos PSA a su mayor número de operaciones.

## A6. Lectura crítica para la tesis

- El resumen destaca "76,8 % frente a 42,5 %" (sin escalar y sin costes); con los retornos escalados a igual número de operaciones el mejor modelo rinde 17,44 % frente a **13,49 % del ingenuo y 12,71 % del aleatorio**, y el Sharpe del aleatorio (17,99) supera al del M1 SA, al del M1 PSA y al del M3. Las diferencias de tasa de aciertos son de 0,1 a 1,2 puntos con un mes de datos de un solo activo, sin pruebas de significación y sin comisiones.
- El objetivo (magnitud del movimiento mayor que la mediana) equivale al "AUC de movimiento" de E20; un referente de tasa base es imprescindible porque la clase "real" es mayoritaria.
- Inconsistencia a verificar: el signo de F_t (ecuación 12 y Algoritmo 2 frente al texto).

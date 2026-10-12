# Federated learning distribuido mediante procesos de consenso en redes

**Extracción de conocimiento: 2026-10-02** (leídas las páginas 1 a 16 y 30 a 47 de 47; **no leídas** las páginas 17 a 29, de implementación y del primer experimento de laboratorio)

**Relevancia para mi tesis: baja (marginal).** No trata de finanzas ni de Bitcoin. Se resume porque está en la carpeta, es un TFM de un máster de IA (útil como ejemplo de estructura) y usa redes de estado de eco, con una observación útil sobre la **variabilidad de la estructura aleatoria del reservorio**.

| Campo | Valor |
|---|---|
| Título exacto | Federated learning distribuido mediante procesos de consenso en redes |
| Autor / Tutores | Aarón Picó Pascual; tutor: Miguel Rebollo Pedruelo; cotutor: Carlos Carrascosa Casamayor |
| Tipo / Venue / Año | Trabajo Fin de Máster, Máster Universitario en Inteligencia Artificial, Reconocimiento de Formas e Imagen Digital, Universitat Politècnica de València, curso 2021/2022 (bibliografía consultada hasta septiembre de 2022) |
| Archivo local | `Pico - Federated learning distribuido mediante procesos de consenso en redes.pdf` |
| URL / DOI | SIN DOI en el documento (repositorio institucional de la UPV; **comprobar el enlace antes de citarlo**) |
| Métodos | Aprendizaje federado sin servidor central, en el que los agentes obtienen el modelo global por un algoritmo de consenso entre vecinos; modelos de red de estado de eco (capa ESN de TensorFlow Addons) por agente; agentes con SPADE; TensorFlow y Keras |
| Datos | Producción de energía eólica de 51 granjas de Australia en 2018, del conjunto AEMO (Operador del Mercado Energético Australiano), con resolución de 5 minutos (p. 38 y p. 41) |

## Aporte clave

Muestra un prototipo de **aprendizaje federado descentralizado**: cada agente entrena su ESN con sus datos y, tras cada época, los pesos se promedian por consenso con los vecinos en vez de enviarse a un servidor. Concluye que es funcional y que obtiene resultados en línea con el aprendizaje automático centralizado, a veces con menos épocas (p. 44 y p. 45).

## Conocimiento extraído (HECHO, con página)

- **Aprendizaje federado:** entrena un modelo sin centralizar los datos (privacidad, volumen de datos, paralelismo); en la versión estándar un servidor promedia los pesos, y aquí se sustituye por un algoritmo de consenso peer-to-peer (p. 14 y p. 15).
- **Echo State Networks:** el reservorio es una capa de conexiones aleatorias de baja conectividad (alrededor de 0,1) y solo se entrena la salida (p. 10 en el índice y p. 30). Se describen los hiperparámetros del reservorio (sección 2.4.3, no leída).
- **Problema de la estructura aleatoria:** el aprendizaje federado supone que todos los modelos comparten estructura, pero cada ESN tiene una estructura aleatoria distinta. Se prueban cuatro formas de unificarla (p. 30 a 33):
  - media de las estructuras: los pesos quedan cerca de cero y se viola la baja conectividad; **no sirve**;
  - imponer la mejor estructura encontrada entre las aleatorias: resultados favorables al aprendizaje federado;
  - estructura con los enlaces más repetidos entre agentes: **la mejor** de las probadas;
  - enlaces repetidos en las mejores estructuras: sin mejora sobre el anterior.
- **Resultados en el experimento de laboratorio** (Tabla 4.6, p. 34), por época, error de la tarea (la unidad del error no se identificó en las páginas leídas): enlaces más repetidos 11,04 → 3,98 en la época 5; mejor estructura 11,84 → 5,17; aprendizaje automático local 11,87 → 5,79; estructura original 12,01 → 8,70.
- **Caso real (51 granjas de AEMO, Tabla 5.1, p. 42):** aprendizaje federado 9,58 → 4,16 y aprendizaje automático centralizado 9,72 → 4,30 en la época 9. El texto aclara que **no se hicieron pruebas exhaustivas ni test estadísticos** que confirmen mejor desempeño real de uno sobre otro (p. 42).
- **Evaluación:** promedio de 10 experimentos (laboratorio) y 5 experimentos (caso real), con 80 % de datos para entrenar y 20 % posterior para evaluar (p. 35 y p. 41).
- **Estructura de la memoria** (índice, p. 6 a 9): Introducción (motivación, objetivos, estructura), Estado del arte, Implementación (herramientas y desarrollo), Experimentos de laboratorio, Experimento con caso real, Conclusiones y Bibliografía; 47 páginas.

## Limitaciones y críticas

- Declarado por el autor: sin pruebas estadísticas formales de la diferencia entre aprendizaje federado y centralizado (p. 42).
- **[OPINIÓN]** Dependencia de la estructura aleatoria: que una unificación particular de la estructura sea "la mejor" sobre 5 a 10 experimentos no basta para generalizarla; el resultado puede depender de la semilla.
- **[OPINIÓN]** No es un trabajo de predicción financiera; la tarea es producción eólica y el objetivo es validar el método de entrenamiento, no el rendimiento predictivo en un dominio caótico.
- **[OPINIÓN]** Una muestra de la memoria sin análisis crítico profundo de la significancia de las diferencias; no usarla como ejemplo del nivel de rigor estadístico.

## Conexión con mi tesis (red E20)

- **Estructura de ejemplo para una memoria de máster de IA:** la secuencia de capítulos y su extensión pueden compararse con la plantilla oficial de la VIU (que manda).
- **Sensibilidad del reservorio a su estructura aleatoria:** respalda que una comparación de reservorios debe repetirse con varias semillas y mostrar la variabilidad; también advierte contra elegir "la mejor semilla" sin separar validación y prueba (sesgo de selección), que mi diseño evita al fijar las reglas antes de ver el bloque final.
- **Idea de enlaces repetidos** entre varios reservorios como estructura común: queda como idea lateral, no la usaré en la tesis.
- **Límite para citarlo:** no aporta evidencia sobre Bitcoin ni finanzas; cítese solo si se necesita un ejemplo de ESN en un TFM de la misma disciplina.

## Referencias que cita y conviene localizar

Konečný y colaboradores (2017), estrategias para mejorar la eficiencia de comunicación del aprendizaje federado; Yang y colaboradores (2018), aprendizaje federado aplicado al teclado de Google; Bonawitz y colaboradores (2016 y 2017), agregación segura; Olfati-Saber y Murray (2004), problemas de consenso en redes; DeGroot (1974), "Reaching a consensus"; Gallicchio, Micheli y Pedrelli (2019), comparación de DeepESN y RNN con compuertas en series temporales multivariantes; Ma y colaboradores (2016), ESN funcional para clasificación de series; Rebollo, Carrascosa y Rincón, aprendizaje federado mediante consenso (congreso de física estadística). **Comprobar cada una con su DOI antes de citarla.**


---

# ANEXO TÉCNICO COMPLETO (datos, métodos, fundamentos matemáticos y tablas)

Contenido técnico de los capítulos 1 a 6 (páginas 1 a 45 del PDF), incluidas las páginas 17 a 29 que la ficha anterior marcaba como no leídas. Relevancia para la tesis: baja (no es financiero); se documenta completo por pedido expreso. Páginas = páginas del PDF.

## A1. Aprendizaje federado y consenso (p. 14 a 19)

- **Aprendizaje federado estándar:** cada máquina entrena el mismo modelo con sus datos locales; un servidor central promedia los pesos y los devuelve (ejemplo del teclado de Google, Gboard: el dispositivo descarga el modelo, aprende localmente, sube solo la actualización, el servidor promedia; protocolo de agregación segura y privacidad diferencial, que este trabajo omite). **Aquí se prescinde del servidor:** el promedio global se obtiene por un **algoritmo de consenso** entre vecinos.
- **Consenso en redes** (DeGroot; Olfati-Saber y Murray): en una red no dirigida, con cada nodo con un valor x_i, la dinámica continua es ẋ = −L·x  (2.1) (L = laplaciana) y converge al valor medio; en discreto x(t + 1) = P·x(t)  (2.2) con la matriz de Perron P = I − ε·L, L = D − A  (2.3), donde ε es el factor de aprendizaje (velocidad de convergencia) y A la matriz de adyacencia; localmente: **x_i(t + 1) = x_i(t) + ε·Σ_{j ∈ N_i} [x_j(t) − x_i(t)]**  (2.4). Tras suficientes rondas todos los nodos tienen el promedio de los valores iniciales. Ejemplo: 4 nodos con valores 0,8, 0,6, 0,4 y 0,2 convergen a 0,5.
- **Red de estado de eco (ESN)** (p. 19 y p. 20): reservorio recurrente aleatorio y fijo, conectividad ≈ 10 %, pesos de entrada y del reservorio no entrenables; solo se entrena la salida; hiperparámetros: número de unidades, conectividad (por defecto 0,1), tasa de fuga (0 a 1) y radio espectral (por defecto 0,9); la búsqueda en cuadrícula es el método de ajuste más usado y es costosa.

## A2. Implementación (p. 22 a 26)

- **Herramientas:** **SPADE** (sistema multiagente en Python sobre mensajería XMPP; servidor Prosody), **TensorFlow/Keras** y **TensorFlow Addons** (capa ESN).
- **Agentes:** tres comportamientos (entrenamiento, consenso, comunicación). Entrenamiento: una época por llamada a `fit`; consenso: número preasignado de rondas; en cada ronda se esperan los pesos de todos los vecinos de la misma época y ronda y se aplica **W_i(t + 1) = W_i(t) + ε·Σ_{j ∈ N_i}[W_j(t) − W_i(t)]**  (3.1) a cada matriz de pesos (`get_weights` y `set_weights`); entrenamiento y consenso se excluyen mutuamente; la comunicación es continua. Solo hay dos tipos de mensajes ("request" y la respuesta con los pesos, la pérdida del último entrenamiento y la época y ronda para sincronizar).
- **Modelo ESN:** **units = 100, connectivity = 0,1, leaky = 1, spectral radius = 0,9** (valores por defecto; no se optimizan). La primera matriz de pesos del modelo es la **matriz de adyacencia del reservorio**; se puede promediar como los demás pesos o excluirla del consenso.

## A3. Experimentos de laboratorio (p. 28 a 36)

- **Red:** 4 agentes (granjas eólicas ARFW1, BALDHWF1, BLUFF1 y BOCORWF1) con datos de AEMO, conectados según la Figura 4.1.
- **Problema:** cada ESN tiene una estructura aleatoria distinta, por lo que el promedio de pesos no tiene sentido; se prueban 5 formas de unificar la estructura (media de 5 ejecuciones, cada una replicada con una versión de aprendizaje automático local como referente). **Error por época 0 a 5** (la unidad del error no se declara; los valores van de ≈ 12 a ≈ 4):

| Método (Tablas 4.1 a 4.6) | Ép. 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Estructura original (FL) | 12,0060 | 10,3888 | 9,8143 | 9,3755 | 9,0140 | 8,7023 |
| ML local (réplica) | 12,0002 | 8,7621 | 7,3066 | 6,4524 | 5,8430 | 5,3867 |
| Estructura media (FL) | 11,0573 | 8,4690 | 7,8502 | 7,0859 | 6,3545 | 5,8134 |
| ML local (réplica) | 11,0296 | 7,9162 | 6,5171 | 5,7233 | 5,2186 | 4,8531 |
| Mejor estructura difundida (FL) | 11,8432 | 7,6461 | 6,8501 | 6,1068 | 5,5637 | 5,1719 |
| ML local (réplica) | 11,8510 | 8,9320 | 7,8064 | 7,0355 | 6,5248 | 6,0921 |
| **Enlaces más repetidos (FL)** | 11,0398 | 5,5378 | 4,9438 | 4,4759 | 4,1753 | **3,9754** |
| ML local (réplica) | 11,0049 | 7,9282 | 6,5326 | 5,7503 | 5,2747 | 4,9431 |
| Enlaces de las mejores estructuras (FL) | 11,0274 | 6,6661 | 6,2334 | 5,7443 | 5,5214 | 5,3468 |
| ML local (réplica) | 11,0460 | 8,4591 | 7,2729 | 6,4850 | 5,9249 | 5,5035 |
| ML (referencia de la Tabla 4.6) | 11,8682 | 8,8831 | 7,5493 | 6,7485 | 6,2039 | 5,7923 |

  - **Estructura original** (cada agente conserva la suya): el consenso de los demás pesos **perjudica** (8,70 frente a 5,39 del ML local).
  - **Estructura media:** los pesos del reservorio quedan cerca de 0 y la conectividad sube mucho (viola la baja conectividad del reservorio): no sirve.
  - **Mejor estructura:** cada agente evalúa su estructura aleatoria y se difunde la mejor: resultados favorables al aprendizaje federado.
  - **Enlaces más repetidos:** se cuenta en cuántos agentes cada enlace es distinto de 0 y se fija a 1 el peso de los enlaces cuyo número de apariciones supera un umbral relativo al enlace más frecuente (mantiene baja la conectividad): **el mejor método**.
  - **Enlaces de las mejores estructuras:** umbral ponderado por el desempeño; no mejora al anterior.
- **Aprendizaje federado frente a aprendizaje centralizado** (media de 10 ejecuciones; el centralizado accede a todos los datos): **caso global** (prueba con los datos de todos los agentes): FL 13,5746, 8,1290, 6,8478, 5,8797, 5,2753, 4,9114; ML 11,4388, 8,4191, 7,2449, 6,5515, 6,0811, 5,7477 (épocas 0 a 5). **Caso local** (predicción de cada agente): FL 11,0398, 5,5378, 4,9438, 4,4759, 4,1753, 3,9754; ML 10,0280, 7,1938, 6,0512, 5,4071, 4,9543, 4,6055. Interpretación del autor: el FL obtiene mejores resultados en menos épocas por la computación en paralelo.

## A4. Caso real: granjas eólicas de Australia (p. 38 a 42)

- **Datos AEMO** (Operador del Mercado Energético Australiano): marca temporal y producción de cada central, resolución de **5 minutos**, año **2018**, **51 granjas**; 80 % de los datos de cada granja para entrenar y el 20 % posterior para evaluar.
- **Red de agentes** (las conexiones no existen y se fijan por proximidad): (1) conexión con todas las granjas dentro de un radio, con 5 % de probabilidad de enlace aleatorio y conexiones manuales entre subgrafos aislados (grafo geométrico aleatorio, RGG, donde el consenso converge más rápido; **es la red usada**); (2) conexión con las 4 granjas más cercanas.
- **Tabla 5.1** (media de los agentes y de 5 experimentos; error por época 0 a 9): **FL** 9,58, 7,49, 6,20, 5,46, 5,04, 4,77, 4,57, 4,41, 4,27, **4,16**; **ML centralizado** 9,72, 7,81, 6,79, 6,11, 5,62, 5,23, 4,91, 4,67, 4,473, **4,30**. Interpretación: el FL está en la línea del ML tradicional, incluso mejor antes; **"no deberíamos generalizar… no se han realizado pruebas exhaustivas ni test estadísticos"**.

## A5. Conclusiones (p. 44 y p. 45)

El aprendizaje federado es una herramienta potente por los datos y por la computación en paralelo; se logra una implementación descentralizada completa con consenso (más robustez y adaptabilidad). Trabajo futuro: otras topologías y otros modelos.

## A6. Lectura crítica y utilidad para la tesis

1. **Utilidad real, aunque marginal:** (a) ilustra que la **estructura aleatoria del reservorio** determina el desempeño y que combinar reservorios distintos exige fijar la estructura (E20 usa una sola estructura fija con semillas; la dependencia de la semilla debe medirse); (b) muestra el uso de ESN de pocas unidades (100) con parámetros por defecto (radio 0,9, conectividad 0,1).
2. **Limitaciones:** el error no tiene unidad declarada; el método de "enlaces más repetidos" se evalúa con 4 agentes y 5 ejecuciones; no hay pruebas estadísticas ni intervalos; la comparación FL frente a ML en el caso global muestra que el FL parte peor en la época 0 (13,57 frente a 11,44); un error por época no es un error de generalización fuera de muestra con ventana móvil.
3. **No usar como evidencia** de predicción financiera ni de la ventaja de los reservorios sobre otros modelos.

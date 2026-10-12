# Diseño metodológico y análisis estadístico para un TFM de IA

Este documento es una **guía de selección**, no una lista de pruebas obligatorias. La pregunta, la unidad de análisis, la disponibilidad de datos y las indicaciones del director determinan qué aplicar. La guía 09MIAR exige analizar e interpretar resultados y evaluar soluciones de IA de modo equitativo; **no impone una técnica estadística concreta**.

Para seleccionar formalmente una prueba o documentar por qué no procede, completa [04B_DECISION_ESTADISTICA.md](04B_DECISION_ESTADISTICA.md) antes de interpretar el test final. La decisión y sus supuestos deben constar en el protocolo y en [11_ESTADO_Y_DECISIONES.md](11_ESTADO_Y_DECISIONES.md).

## 1. Diseña la evaluación antes de entrenar

1. Escribe la **pregunta principal** y el criterio de éxito: por ejemplo, mejorar una métrica frente a un referente sin exceder un coste.
2. Define la **unidad independiente**: paciente, persona, documento, equipo, serie temporal, conjunto de datos o tarea. No trates múltiples registros de una misma unidad como observaciones independientes.
3. Describe población, muestra, origen, período, licencia/permisos, criterios de inclusión/exclusión y posibles sesgos.
4. Fija un **método de referencia** simple y uno pertinente de la literatura. Compara bajo las mismas particiones, datos disponibles y reglas de ajuste.
5. Selecciona **una métrica primaria** alineada con el objetivo y métricas secundarias para errores, eficiencia o equidad. Define su dirección (mayor/menor es mejor).
6. Decide particiones, búsqueda de hiperparámetros, semillas, presupuesto de cómputo y análisis estadístico **antes** de estudiar el test final.
7. Registra cualquier cambio posterior al protocolo y explica por qué se hizo.

## 2. Exploración y descripción de datos

Como mínimo, cuando corresponda: número de unidades y registros; distribución de clases o del objetivo; faltantes; duplicados; rangos y valores atípicos; tamaño por grupo y período; desbalance; calidad de etiquetas; posibles variables sensibles; y desplazamiento entre entrenamiento y evaluación. Muestra tablas y gráficos que ayuden a entender el problema, no una colección automática de gráficos.

Si se usan datos personales, describe la minimización, el acceso permitido y la forma de anonimización o seudonimización que corresponda al proyecto. Los permisos y el tratamiento específico deben decidirse con el director y las normas aplicables al conjunto de datos.

## 3. Particiones y control de fuga de información

| Situación | Diseño apropiado a considerar | Error que evita |
|---|---|---|
| Datos independientes sin tiempo ni grupos | Entrenamiento/validación/test o validación cruzada adecuada. | Evaluar sobre datos usados para ajustar. |
| Clases desbalanceadas | Partición estratificada si mantiene representatividad. | Que una clase desaparezca en una partición. |
| Varias observaciones por persona/equipo/documento | Partición por grupo; grupos disjuntos. | Que el modelo reconozca la misma unidad en train y test. |
| Predicción futura | Corte cronológico o validación temporal. | Entrenar con información del futuro. |
| Ajuste amplio de hiperparámetros | Validación interna o anidada para estimar rendimiento de la búsqueda. | Informar como rendimiento final el usado para elegir parámetros. |
| Pocos datos | Validación cruzada cuidadosamente diseñada; declarar incertidumbre. | Conclusiones excesivas a partir de una sola partición. |

Imputación, escalado, selección de variables, generación sintética, calibración y cualquier transformación aprendida de datos deben ajustarse **solo con el entrenamiento de cada partición**. Mantén el test final reservado para la evaluación. Véanse las [prácticas recomendadas de scikit-learn](https://scikit-learn.org/stable/common_pitfalls.html) y su [guía de validación cruzada](https://scikit-learn.org/stable/modules/cross_validation.html).

## 4. Métricas según el tipo de tarea

| Tarea | Métricas candidatas | Matiz para escoger |
|---|---|---|
| Clasificación | Matriz de confusión; precisión, sensibilidad, especificidad, F1; ROC-AUC y PR-AUC; calibración si se usan probabilidades. | Con clases raras o costes asimétricos, la exactitud sola suele ocultar fallos importantes. Define clase positiva y umbral. |
| Regresión | MAE, RMSE y error relativo cuando su denominador tiene sentido. | Presenta unidades; RMSE penaliza más errores grandes. |
| Pronóstico temporal | MAE/RMSE por horizonte; comparación con predictor ingenuo; error por período. | Evalúa con cortes temporales y evita usar variables futuras. |
| Agrupación o representación | Métricas internas y, solo si existe una referencia válida, métricas externas; evaluación de utilidad posterior. | Una única métrica interna no demuestra utilidad del agrupamiento. |
| Recuperación/RAG | Recall@k, MRR o nDCG para recuperación; exactitud factual y calidad de respuesta con rúbrica definida. | Separa calidad del recuperador de la generación; define quién evalúa y cómo. |
| Visión/segmentación | Métricas de clasificación o IoU/Dice según el objetivo; análisis por clase o escena. | La métrica debe coincidir con la unidad y el uso final. |
| Aprendizaje por refuerzo | Retorno por episodio, tasa de éxito, coste/seguridad y variabilidad entre semillas. | Evalúa en episodios y escenarios separados del ajuste. |

Las definiciones precisas deben corresponder a tu tarea y a las implementaciones usadas. Referencia: [guía de métricas de scikit-learn](https://scikit-learn.org/stable/modules/model_evaluation.html).

## 5. Incertidumbre y comparación estadística

**Informe mínimo recomendado:** tamaño de muestra/unidades, estimación puntual de la métrica, dispersión o intervalo de incertidumbre apropiado, diferencia frente al referente, costo computacional relevante y descripción del diseño de partición. Un valor p aislado no describe magnitud ni utilidad del efecto.

| Pregunta y diseño | Técnica candidata | Condición crítica |
|---|---|---|
| ¿Cuánta incertidumbre tiene una métrica en un test con unidades independientes? | Intervalo de confianza o bootstrap sobre unidades independientes. | Remuestrea la unidad correcta; conserva grupos/estructura temporal cuando corresponda. |
| Dos clasificadores evaluados sobre **las mismas observaciones** de un único test binario | Tabla de desacuerdos y prueba de McNemar, si se quiere una prueba de diferencia de errores. | Requiere predicciones pareadas por observación; no sustituye el tamaño del efecto. |
| Dos métodos en **varios conjuntos de datos independientes** | Diferencias por conjunto y prueba de rangos con signo de Wilcoxon, si sus supuestos son razonables. | La unidad es el conjunto de datos, no cada fold. |
| Tres o más métodos en **varios conjuntos de datos independientes** | Rangos, Friedman y comparaciones posteriores justificadas. | Corregir comparaciones múltiples; interpretar diferencias y rangos. |
| Comparación de varias configuraciones o subgrupos | Intervalos y corrección por múltiples contrastes si se hacen pruebas formales. | Declarar contraste primario antes de explorar muchos resultados. |

**Cuidado con los folds:** los resultados de folds de una misma validación cruzada no son muestras independientes; no apliques sin más una prueba t pareada ordinaria sobre ellos para afirmar superioridad. La elección de prueba para un único conjunto de datos repetido es más delicada y debe justificarse con el diseño real. La referencia metodológica clásica de [Demšar (2006)](https://www.jmlr.org/papers/volume7/demsar06a/demsar06a.pdf) trata explícitamente comparaciones sobre **múltiples conjuntos de datos** y recomienda Wilcoxon/Friedman en ese contexto. Consulta las condiciones de [Wilcoxon en SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html).

La significación estadística no equivale a relevancia práctica. Informa también diferencia absoluta/relativa, variabilidad, coste, errores y condiciones bajo las que el método falla. Si el estudio es descriptivo o de ingeniería y no hay suficientes unidades independientes, es mejor declarar la incertidumbre y las limitaciones que forzar una prueba inapropiada.

## 6. Análisis que fortalecen una tesis aplicada

- **Ablación:** retirar componentes de la propuesta para ver cuál aporta valor.
- **Sensibilidad:** variar decisiones clave (umbral, hiperparámetro, tamaño de entrenamiento, semilla) sin convertir el test en herramienta de ajuste.
- **Análisis de errores:** ejemplos de falsos positivos/negativos, fallos por categoría y casos difíciles; evitar exponer datos personales.
- **Robustez:** evaluar cambios plausibles de dominio, ruido, datos faltantes o períodos posteriores, si el objetivo lo requiere.
- **Equidad:** comparar rendimiento por subgrupo pertinente cuando existan datos, permisos y tamaño suficiente; interpretar intervalos y posibles sesgos.
- **Eficiencia:** tiempo, memoria, energía o coste de inferencia si forman parte de la pregunta.
- **Reproducibilidad:** versiones de datos/código, semillas, entorno, configuración, particiones y procedimiento para repetir tablas/figuras.

## 7. Tabla maestra de resultados sugerida

| Experimento | Datos y partición | Modelo | Parámetros/semilla | Métrica primaria | Incertidumbre | Métrica secundaria | Costo | Observación |
|---|---|---|---|---:|---|---:|---:|---|
| E01 |  | Referencia |  |  |  |  |  |  |
| E02 |  | Propuesta |  |  |  |  |  |  |

No rellenes resultados antes de ejecutar experimentos. Conserva predicciones por unidad y tablas originales para poder revisar errores y recalcular métricas.

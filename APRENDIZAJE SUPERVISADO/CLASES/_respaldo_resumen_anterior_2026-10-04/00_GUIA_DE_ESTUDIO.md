# Guía de estudio — Aprendizaje Supervisado (máster IA)

Esta carpeta es el punto de partida de cada sesión de estudio del curso. Contiene, en orden de uso:

| Archivo | Para qué sirve |
|---|---|
| `prompt_tutor_chat_v11.md` | **Prompt vigente** para la tutoría en conversación: un concepto, una pregunta, un caso nuevo para confirmar aplicación y estado al cerrar la sesión. |
| `01_prompt-maestro-tutor-v11.md` | Versión anterior y más extensa de la metodología, conservada como referencia. |
| `tenica de aprendizaje.txt` | Revisión intermedia de la técnica; para sesiones nuevas usa `prompt_tutor_chat_v11.md`. |
| `08_aprendizaje_supervisado_desde_cero.md` | **Empieza aquí para entender.** Explica cada idea con una escena simple, una pregunta y el nombre original del curso en un desplegable que se abre después de responder. |
| `07_explicacion_profunda_por_bloques.md` | Segunda capa: fórmulas, matices, ejemplos numéricos y límites, para abrir después de entender la idea básica. |
| `02_tema1_fundamentos_y_preparacion_datos.txt` | Material fuente del Tema 1 (CRISP-DM, tipos de aprendizaje, estructura de datos, limpieza). |
| `03_tema2_validacion_y_metricas.txt` | Material fuente del Tema 2 (hold-out, k-fold, validación anidada, métricas de regresión y clasificación). |
| `04_tema3_extraccion_caracteristicas.txt` | Material fuente del Tema 3 (variables cualitativas/cuantitativas, procesado de imagen, segmentación, descriptores). **Ojo:** este resumen solo cubre lo práctico de los notebooks — la teoría real de este tema está en el PPTX del profesor, no en el PDF del manual (ver nota más abajo). |
| `05_tema4_modelos_regresion.txt` | Material fuente del Tema 4 (regresión lineal/OLS, polinómica, KNN). |
| `06_tema5_modelos_clasificacion.txt` | Material fuente del Tema 5 (regresión logística, árboles de decisión, SVM). |
| `outputs/explicacion_excel/Seguimiento_Aprendizaje_Supervisado_mejorado.xlsx` | **Tracker recomendado**: conserva los temas y estados, agrega explicaciones sencillas a cada concepto y distingue «Firme» de «Comprendido» en el resumen. Actualízalo después de cada sesión (columna Estado). |
| `explicacion video/prompt_tutor_video_v11.md`, `explicacion video/ENCARGO_PARA_IA_VIDEO.md` y `explicacion video/EJEMPLO_VIDEO_1_1_A.md` | Reglas, encargo listo para pedir a otra IA un video y un segmento de guion como ejemplo del mismo estilo de aprendizaje. |

## Orden de estudio (pedagógico, no cambiar salvo que quieras saltar)

**Tema 1 → Tema 2 → Tema 3 → Tema 4 → Tema 5.**

- **Tema 1** y **Tema 2** son la base: sin CRISP-DM/tipos de aprendizaje/limpieza de datos (T1) y sin saber validar y medir un modelo (T2), no tiene sentido entrenar nada.
- **Tema 3** (extracción de características) va antes de los modelos porque construye las variables/imágenes que luego alimentan la regresión (T4) y la clasificación (T5).
- **Tema 4** (regresión) antes de **Tema 5** (clasificación) porque la regresión logística de T5 se apoya en conceptos de regresión lineal de T4 (misma combinación lineal, distinta función de salida).

Dentro de cada tema, la hoja "Mapa de estudio" del Excel ya trae los subtemas en el orden en que conviene enseñarlos (columna Código, p. ej. 1.1, 1.2, 1.3...). La columna **Prioridad** (Alta/Media/Baja) te dice dónde concentrar el tiempo si vas corto: los "Alta" son los conceptos núcleo de los que dependen los demás; los "Baja" son contexto/historia que puedes repasar rápido.

## Cómo arrancar cada sesión con el prompt vigente

1. Copia el contenido de `prompt_tutor_chat_v11.md` como instrucción del tutor (si no está ya activo).
2. Dile en qué tema vas a trabajar y pégale (o indícale la ruta de) el archivo numerado correspondiente (`02_...txt`, `03_...txt`, etc.) como fuente.
3. Empieza por un apartado de `08_aprendizaje_supervisado_desde_cero.md` y responde su pregunta antes de abrir el nombre formal. Después usa `07_explicacion_profunda_por_bloques.md` para la matemática o el código correspondiente.
4. Al cerrar cada concepto, resuelve el caso nuevo que proponga el tutor. Registra el estado demostrado en el "Mapa de estudio" (columna Estado: 🟢 Firme / 🟢 Comprendido / 🟡 Repasar / 🟠 Iniciado / 🟠 Parcial / ⚪ Pendiente / 🔴 Débil). Guarda también el bloque de estado que entrega el tutor para retomar la próxima sesión.

## Temas con "tabla de variables" (regla 6, excepción de símbolos parecidos)

Estos bloques tienen 3+ símbolos o fórmulas parecidas que se confunden fácilmente entre sí — pide explícitamente al tutor que empiece por la tabla-panorama antes de la analogía:

- **Tema 2:** métricas de regresión MAE / MSE / RMSE / MAPE (2.5) y las derivadas de la matriz de confusión: TP/TN/FP/FN → exactitud / precisión / sensibilidad / F1 (2.6).
- **Tema 3:** las 4 familias de medidas de variables cuantitativas — tendencia central / posición / dispersión / distribución (3.3) — y la tabla de descriptores de forma (área, bounding box, excentricidad, perímetro, solidez... en 3.8).
- **Tema 4:** los coeficientes de la regresión lineal múltiple w0, w1...wp y R² (4.1).
- **Tema 5:** sigmoide / log-odds / umbral de decisión de LOGR (5.1), y Gini vs. entropía como criterios de partición de árboles (5.2).

## Huecos de fuente conocidos (no rellenar con contenido inventado)

- **Tema 3 completo:** el manual PDF del curso (`05MIAR_GAsencio_nueva_imagen.pdf`) solo cubre los temas 1, 2, 4 y 5 — **no incluye Tema 3**. El PowerPoint original `Tema 3 - Extracción de características.pptx` sí está en la carpeta `CLASES` y se copió a `explicacion video/material_curso/`. El resumen `04` cubre las prácticas de notebooks; consulta el PPTX para la teoría y las figuras. La diapositiva 35 contiene una definición conflictiva del diámetro de Feret: revisa `explicacion video/ERRATAS_Y_LIMITES.md`.
- **Tema 5, subtema SVM (5.3):** ni el PDF ni el notebook explican teóricamente qué es un hiperplano separador, el margen máximo, los vectores de soporte, ni el catálogo de kernels. Solo hay código de ejemplo (`SVC` con `C=10`, kernel por defecto `rbf`). Si necesitas la teoría completa de SVM, hace falta una fuente adicional (documentación de scikit-learn u otro material del curso no incluido aquí).

## Nota sobre el estado inicial del Excel

El Mapa de estudio ya tiene estados distintos: algunos conceptos figuran como **Comprendido**, otros como **Repasar**, **Débil**, **Parcial** o **Pendiente**. Son estados previos del archivo, no una prueba automática de dominio. **Firme** exige resolver un caso nuevo sin ayuda; actualiza ese estado solo después de verificarlo (regla 11 del prompt v11).

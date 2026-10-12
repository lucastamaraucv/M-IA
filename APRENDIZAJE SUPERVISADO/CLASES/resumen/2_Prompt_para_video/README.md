# 2_Prompt_para_video — prompt para que otra IA te explique Aprendizaje Supervisado en video

## Qué contiene

`PROMPT_VIDEO_APRENDIZAJE_SUPERVISADO.md` es **un solo prompt autosuficiente** (unos 280 KB, alrededor de 70 mil tokens). No depende de ningún otro archivo: lleva dentro el método, tu perfil y **todo el conocimiento del curso**.

| Parte | Contenido |
|---|---|
| **A · Instrucciones para la IA** | Rol, orden de trabajo, reglas de contenido, estructura obligatoria de cada segmento (problema real → analogía → pregunta → nombre original → fórmula → código → caso nuevo), pausas del video, colores de las animaciones, estilo de narración, reporte de verificación y entregables por video. |
| **B · Quién eres y cómo aprendes** | Tu prompt de tutoría v11 completo (método de aprendizaje, reglas, forma de las respuestas). |
| **C · Conocimiento del curso** | 5 bloques, 29 temas (un tema = un video) y 151 conceptos (un concepto = un segmento). Cada tema trae **escenas** de apoyo, **Profundiza** (fórmulas, tablas de variables, ejemplos calculados) y una **ficha por concepto** con definición precisa, ejemplo o código, errores comunes, pregunta de comprobación y fuente exacta. |
| **D · Huecos, cierre y ejemplo** | Erratas y huecos de fuente (SVM, diámetro de Feret, etc.), cierre «qué modelo y qué métrica usar», un guion de ejemplo (`1.1.a`) y la plantilla del reporte de verificación. |

## Cómo usarlo con otra IA

1. **Sube o pega el archivo completo** a la IA que producirá los videos. Al inicio del archivo está el **primer mensaje listo para copiar**: completa solo el tema, tu estado previo y la meta.
2. Empieza por **`1.1 Metodología CRISP-DM`**. La IA entrega **un video por tema** (video o guion escena por escena) con una pausa y una sola pregunta por concepto, un caso nuevo sin solución inmediata y las soluciones al final.
3. **Ve el video, haz las pausas** y resuelve el caso nuevo sin mirar la solución.
4. **Devuelve el reporte** (plantilla en la Parte D): por concepto, si respondiste bien, mal o a medias, qué dijiste y dónde te trabaste. El siguiente video reenseña solo el paso que falló.
5. **Actualiza tu estado** en el Excel de `1_Excel_seguimiento` (columna E): «Firme» solo si resolviste el caso nuevo sin ayuda.

**Si la IA no admite un archivo tan largo:** pega las Partes **A, B y D** y, de la Parte C, solo el **bloque** del tema que toque (cada bloque empieza con `## BLOQUE n`). Pídele que te solicite el siguiente bloque cuando termine.

## Qué garantiza el prompt

- **Fidelidad:** los datos, fórmulas y cifras salen de las fichas; si hay un hueco o una errata, la IA lo señala en pantalla y no lo rellena.
- **Método:** un concepto por segmento, una sola pregunta de comprensión, el nombre formal solo después de la pausa y animación desde la primera explicación (ámbar = activo, azul = comparación, verde = resuelto, gris = neutral).
- **Primera escena sin jerga:** pensada para que la entienda alguien sin formación en ingeniería, conservando después los términos originales del curso.

## El Excel que acompaña a este prompt

El Excel de la carpeta `1_Excel_seguimiento` tiene el mismo contenido en tabla y guarda **tus estados de aprendizaje**; los estados no se deducen de este prompt: los pegas tú como «estado previo» en el primer mensaje. Su explicación detallada está a continuación, para que tengas aquí todo el contexto.

## Explicación detallada del Excel `Seguimiento_Aprendizaje_Supervisado.xlsx`

### 1. Qué es y cómo está construido

Es tu libro de seguimiento del curso de Aprendizaje Supervisado. Tiene **2 hojas**: **«Resumen»** (tablero con contadores y progreso, todo calculado con fórmulas) y **«Mapa de estudio»** (la tabla maestra: **185 filas × 15 columnas**). El libro se recalcula solo al abrirlo y cada vez que cambias un estado. No tiene macros, gráficos ni imágenes. En «Mapa de estudio» la primera fila está inmovilizada (el encabezado siempre se ve) y puedes activar filtros con *Datos → Filtro*.

### 2. Cómo se numeran las filas: códigos y niveles

| Nivel (col. D) | Código | Qué representa | Cuántos hay | Cómo se usa |
|---|---|---|---:|---|
| `0` | `1` … `5` | **Bloque** del curso | 5 | Encabezado y resumen del bloque; no es un video. |
| `1` | `1.1`, `1.2` … `5.3` | **Tema** | 29 | **Un tema = un video** en el prompt de la carpeta `2_Prompt_para_video`. |
| `2` | `1.1.a`, `1.1.b` … | **Concepto** | 151 | **Un concepto = un segmento** dentro del video de su tema. |

Total: 5 + 29 + 151 = **185 filas**. Ejemplo de la jerarquía: `1` (Fundamentos y preparación de datos) → `1.5` (Normalización y estandarización) → `1.5.a` (Normalización). El tema `3.4` (la imagen como dato) no tiene conceptos de nivel 2: se explica como un solo segmento. Las filas están en el orden pedagógico del curso: bloque 1 → 2 → 3 → 4 → 5; el bloque 3 va antes de los modelos porque construye las variables que usan los bloques 4 y 5.

### 3. Los 5 bloques

| Bloque | Filas | Temas | Conceptos | Qué trata |
|---|---:|---:|---:|---|
| 1. Fundamentos y preparación de datos | 48 | 8 | 39 | Metodología CRISP-DM, tipos de aprendizaje, tabla de datos (instancias, atributos, clase) y 4 técnicas de preparación de datos. |
| 2. Validación de modelos y métricas de evaluación | 37 | 6 | 30 | Hold-out, validación cruzada, bootstrap, validación anidada, métricas de regresión y de clasificación. |
| 3. Extracción de características (variables e imágenes) | 39 | 9 | 29 | Variables cualitativas y cuantitativas, la imagen como dato, procesado, segmentación, descriptores de forma y de textura. |
| 4. Modelos de regresión | 27 | 3 | 23 | Regresión lineal múltiple (OLS), regresión polinómica y KNN para regresión. |
| 5. Modelos de clasificación | 34 | 3 | 30 | Regresión logística, árboles de decisión y SVM (solo código, sin teoría). |

«Filas» cuenta el encabezado del bloque, sus temas y sus conceptos (48 + 37 + 39 + 27 + 34 = 185).

### 4. Los 29 temas (cada uno es un video)

| Código | Tema (un video) | Conceptos | Prioridad | Fuente en el Excel (col. J) |
|---|---|---:|---|---|
| `1.1` | Metodología CRISP-DM | 7 | Alta | 02_tema1_fundamentos_y_preparacion_datos.txt |
| `1.2` | Tipos de aprendizaje (supervisado / no supervisado / otros) | 6 | Alta | 02_tema1_fundamentos_y_preparacion_datos.txt |
| `1.3` | Estructura de datos: instancias, atributos y clase | 6 | Alta | 02_tema1_fundamentos_y_preparacion_datos.txt |
| `1.4` | Limpieza de datos — introducción | 2 | Media | 02_tema1_fundamentos_y_preparacion_datos.txt |
| `1.5` | Normalización y estandarización | 4 | Alta | 02_tema1_fundamentos_y_preparacion_datos.txt |
| `1.6` | Detección de outliers | 5 | Alta | 02_tema1_fundamentos_y_preparacion_datos.txt |
| `1.7` | Imputación de valores ausentes | 4 | Alta | 02_tema1_fundamentos_y_preparacion_datos.txt |
| `1.8` | Selección de atributos | 5 | Media | 02_tema1_fundamentos_y_preparacion_datos.txt |
| `2.1` | Introducción: entrenamiento, test, sobreajuste y subajuste | 5 | Alta | 03_tema2_validacion_y_metricas.txt |
| `2.2` | Validación hold-out | 4 | Alta | 03_tema2_validacion_y_metricas.txt |
| `2.3` | Validación cruzada / K-fold | 5 | Alta | 03_tema2_validacion_y_metricas.txt |
| `2.4` | Ajuste de parámetros y validación anidada | 4 | Alta | 03_tema2_validacion_y_metricas.txt |
| `2.5` | Evaluación en regresión: MAE, MSE, RMSE, MAPE | 5 | Alta | 03_tema2_validacion_y_metricas.txt |
| `2.6` | Evaluación en clasificación: matriz de confusión, precisión, sensibilidad, F1, accuracy | 7 | Alta | 03_tema2_validacion_y_metricas.txt |
| `3.1` | Conceptos básicos y variable estadística | 4 | Media | Tema 3 - Extracción de características.pptx (diap. 3-6) |
| `3.2` | Análisis de variables cualitativas | 2 | Media | pptx diap. 7-8 + notebook var_cualitativas |
| `3.3` | Análisis de variables cuantitativas | 4 | Alta | pptx diap. 9-10 + notebook var_cuantitativas |
| `3.4` | Introducción a los datos 2D (la imagen como dato) | 0 | Alta | pptx diap. 11 + notebook imagenes_transformaciones |
| `3.5` | Procesado de imagen: transformaciones de intensidad | 3 | Media | pptx diap. 14-16 + notebook |
| `3.6` | Procesado de imagen: espacios de color y transformaciones geométricas | 4 | Media | pptx diap. 17-23 + notebook |
| `3.7` | Segmentación de imágenes | 4 | Alta | pptx diap. 24-33 + notebook Image_segmentation |
| `3.8` | Descriptores de forma (descriptores geométricos) | 3 | Alta | pptx diap. 34-35 + notebook Descriptores_forma |
| `3.9` | Descriptores de textura | 5 | Alta | pptx diap. 36-55 + notebook Descriptores_textura |
| `4.1` | Regresión lineal múltiple (OLS) | 10 | Alta | 05_tema4_modelos_regresion.txt |
| `4.2` | Regresión polinómica | 3 | Media | 05_tema4_modelos_regresion.txt |
| `4.3` | Vecinos más cercanos (KNN) para regresión | 10 | Alta | 05_tema4_modelos_regresion.txt |
| `5.1` | Regresión logística (LOGR) | 13 | Alta | 06_tema5_modelos_clasificacion.txt |
| `5.2` | Árboles de decisión | 14 | Alta | 06_tema5_modelos_clasificacion.txt |
| `5.3` | SVM — Support Vector Machines | 3 | Media | 06_tema5_modelos_clasificacion.txt |

Los temas 1, 2, 4 y 5 se apoyan en el manual del curso y en notebooks (resúmenes `02`, `03`, `05`, `06`); el tema 3 se apoya en el PowerPoint del profesor y en notebooks (resumen `04`).

### 5. Hoja «Mapa de estudio», columna por columna

| Col. | Encabezado | Qué contiene | Quién la edita |
|---|---|---|---|
| A | Código | Código jerárquico de la fila (ver sección 2). | Nadie: es la clave que une el Excel con el prompt. |
| B | Bloque | Bloque al que pertenece la fila. Lo usa el tablero «Resumen» para contar por bloque. | Nadie. |
| C | Tema / concepto | El **nombre original del curso**. En el nivel 0 va en mayúsculas. | Nadie. |
| D | Nivel | `0` bloque, `1` tema, `2` concepto. | Nadie. |
| **E** | **Estado** | **Tu avance de aprendizaje.** Lista desplegable de 7 valores (sección 6). Con color según el valor. | **Tú.** |
| F | Explicación sencilla | La idea explicada con palabras comunes para alguien sin formación en ingeniería, en pocas frases y sin inventar datos. Es el puente hacia el término original; la precisión está en las columnas K a O. | Mejorable; no es tu estado. |
| G | Siguiente aplicación | Qué practicar a continuación. Solo existe en 35 filas: los 5 bloques, los 29 temas y el concepto `3.8.c`. | Mejorable. |
| H | Prioridad | **Alta** (88 filas), **Media** (76) o **Baja** (21): dónde concentrar el tiempo si vas corto. Alta = concepto núcleo del que dependen otros; Baja = contexto o historia. | Tú, si cambias de criterio. |
| I | Actualizado | Fecha de la última actualización de la fila (hoy todas dicen 27/09/2026). | Tú, al cambiar un estado. |
| J | Fuente | Archivo o material del curso donde está el tema: resúmenes `02`, `03`, `05`, `06` para los bloques 1, 2, 4 y 5; diapositivas del PPTX y notebook para el bloque 3. | Nadie. |
| K | Definición precisa y fórmula | Lo que se puede afirmar con rigor: definiciones, fórmulas, cifras verificables y página o sección de origen cuando aplica. | Nadie. |
| L | Ejemplo o código | Un ejemplo numérico o el código real del material. | Nadie. |
| M | Ojo: error común o límite | Trampas frecuentes, límites del concepto y errores del propio material. | Nadie. |
| N | Pregunta de comprobación | **Una sola** pregunta para verificar que lo entiendes (no incluye la respuesta). | Nadie. |
| O | Fuente exacta | Archivo `02`–`06`, sección, página del manual PDF (`PDF p.N`) o diapositiva del PowerPoint, para poder verificar. | Nadie. |

**Ejemplo real: fila `1.5.a`**

| Campo | Valor |
|---|---|
| Código / nivel | `1.5.a` / 2 (concepto del tema `1.5`) |
| Tema / concepto | Normalización |
| Prioridad | Alta |
| Fuente (J) | 02_tema1_fundamentos_y_preparacion_datos.txt |
| Explicación sencilla (F) | Lleva los valores de una columna al rango de 0 a 1: se resta el menor valor y se divide por la diferencia entre el mayor y el menor. Se aplica columna por columna. Así todas quedan en la misma escala. |
| Definición precisa y fórmula (K) | x_N = (x - min(x_i)) / (max(x_i) - min(x_i)). Restar el mínimo = centrado; dividir por el rango = escalado. Para desnormalizar: x = x_N (max - min) + min. Es una homotecia aplicada a cada columna. |
| Ejemplo o código (L) | Un atributo con mínimo 0 y máximo 2: 0 pasa a 0, 1 pasa a 0,5 y 2 pasa a 1. Clase: preprocessing.MinMaxScaler. |
| Ojo (M) | Con datos futuros fuera del rango de entrenamiento el resultado puede salir de [0,1]; y si max = min la fórmula no está definida. |
| Pregunta de comprobación (N) | Si el máximo de entrenamiento es 60 y llega un caso con 70, ¿cuánto vale su normalizado con mínimo 20? |
| Fuente exacta (O) | 02 §5; PDF p.20-21 (Programa 1). |

### 6. Estados de aprendizaje (columna E)

Son **tu avance personal**. No se deducen de ningún texto y no se modificaron al mejorar el libro (se comprobó fila por fila contra tu original). Cada valor tiene su color automático:

| Estado | Color | Significado |
|---|---|---|
| 🟢 **Firme** | verde | Aplicas el concepto a un **problema nuevo**, justificas cuándo sirve y reconoces al menos una limitación. Repetir el ejemplo visto no basta. **Es el único estado que cuentan «Firmes» y «% Firme».** |
| 🟢 **Comprendido** | verde | Puedes explicarlo con tus palabras y justificar su mecanismo, pero todavía falta comprobar su aplicación. |
| 🟡 **Repasar** | amarillo | Estado intermedio de tu libro: conviene volver a repasarlo. |
| 🟠 **Iniciado** | naranja | Estado intermedio de tu libro: empezaste el tema o el concepto. |
| 🟠 **Parcial** | naranja | Estado intermedio de tu libro: dominas una parte. |
| ⚪ **Pendiente** | gris | Todavía no se enseñó o no se verificó. |
| 🔴 **Débil** | rojo | Tu respuesta mostró un error conceptual o no puedes justificar un paso. |

Los estados Repasar, Iniciado y Parcial ya estaban en tu libro; el método de tutoría solo define Firme, Comprendido, Débil y Pendiente, así que para los otros tres vale la descripción práctica de la tabla. Si cambias el texto de un estado, los contadores del «Resumen» dejarán de contarlo: usa siempre el desplegable.

### 7. Hoja «Resumen», zona por zona

| Zona | Qué muestra |
|---|---|
| `A1` | Título del libro. |
| `A3` | Texto de uso: qué columnas leer y la advertencia «comprendido aún no significa firme». |
| `A5:H6` | Cuatro contadores: **Total conceptos** (todas las filas, 185), **Firmes**, **Pendientes** y **Débiles**. |
| `A9:B16` | Cuántas filas hay en cada uno de los 7 estados. |
| `D9:H18` | Panel **«Tema en curso — Tema 1»**: los 8 temas del bloque 1 con su estado, idea clave, siguiente aplicación y prioridad. Es un panel fijo enlazado a «Mapa de estudio»: se actualiza solo, pero siempre muestra el bloque 1. |
| `A20:H21` | Criterio de avance: «Firme» exige resolver un caso nuevo; «Comprendido» no basta. |
| `A22:H29` | **Progreso por bloque**: por cada bloque, Total de filas, 🟢 Firme, 🟠 En progreso (= Comprendido + Iniciado + Parcial), 🟡 Repasar, ⚪ Pendiente, 🔴 Débil y **% Firme** (Firme ÷ Total). La última fila, **TOTAL CURSO**, suma los cinco bloques. |
| `A30:H31` | Nota del orden pedagógico del curso. |
| `J1:N36` | Lista de los **34 encabezados** (5 bloques + 29 temas) con código, bloque, tema, estado y prioridad, enlazada a «Mapa de estudio». |

Todo el «Resumen» son fórmulas sobre «Mapa de estudio» (columnas B y E, filas 2 a 186): no escribas encima de ellas. Si agregas filas nuevas al final del mapa, amplía esos rangos en las fórmulas.

### 8. Cómo estudiar con el Excel

1. Elige un tema (nivel 1) y filtra por su código: verás el tema y sus conceptos.
2. Lee la **explicación sencilla** (F) y responde la **pregunta de comprobación** (N) con tus palabras, sin mirar la definición.
3. Contrasta con la **definición precisa** (K), el **ejemplo** (L) y el **ojo** (M). Si algo no coincide con tu manual, manda el manual (la fuente exacta está en O).
4. Resuelve un **caso nuevo**. Si lo logras sin ayuda, cambia E a **🟢 Firme** y actualiza la fecha (I). Si fallas, marca **🔴 Débil** o **🟡 Repasar** y vuelve solo al paso que falló.
5. Revisa el «Resumen» para ver el progreso por bloque.

### 9. Relación con el prompt para video

Cada fila del Excel tiene una **ficha con el mismo código** en la Parte C del prompt `PROMPT_VIDEO_APRENDIZAJE_SUPERVISADO.md`: la columna F es su «Explicación sencilla»; K, L, M, N y O son sus campos «Definición precisa y fórmula», «Ejemplo o código», «Ojo», «Comprueba» y «Fuente exacta». El prompt añade lo que no cabe en una tabla: las escenas cotidianas, la profundización con tablas de variables y ejemplos calculados, y las instrucciones para la IA. Los **estados** viven solo en el Excel; los pegas tú como «estado previo» al pedir un video.

### 10. De dónde salen las fuentes `02`–`06`

Las referencias de las columnas J y O usan estos nombres (los archivos están en la carpeta superior `CLASES`, con el nombre de la derecha y contenido idéntico):

| Referencia | Archivo en `CLASES` | Contenido |
|---|---|---|
| `02` | `resumen_cap1_tema1.txt` | Tema 1: fundamentos y preparación de datos. |
| `03` | `resumen_cap2_tema2.txt` | Tema 2: validación y métricas. |
| `04` | `resumen_tema3.txt` | Tema 3: resumen de los notebooks de extracción de características. |
| `05` | `resumen_cap3_tema4.txt` | Tema 4: regresión. |
| `06` | `resumen_cap4_tema5.txt` | Tema 5: clasificación. |
| `PDF p.N` | `05MIAR_GAsencio_nueva_imagen.pdf` | Manual del curso (temas 1, 2, 4 y 5). |
| `Diap. N` | `Tema 3 - Extracción de características.pptx` | PowerPoint del profesor (tema 3). |
| `notebook ...` | `viu_aprendizaje_supervisado-main\` | Notebooks y datos del curso. |

### 11. Huecos y erratas que el Excel marca (no se rellenan con contenido inventado)

- **Tema 3:** el manual PDF no lo cubre; su teoría está en el PowerPoint, y las celdas de texto de los notebooks son solo títulos.
- **`3.5.c`:** transformación lineal a tramos, negativo y ecualización del histograma solo aparecen nombradas (diapositiva 16).
- **`3.8.c`, diámetro de Feret:** la diapositiva 35 lo define con un cociente que coincide con la extensión: parece una errata y no se enseña como definición verificada.
- **`5.3`, SVM:** el material solo trae código; no explica hiperplano, margen máximo, vectores de soporte ni kernels.
- **`5.1.b`, sigmoide:** el resumen `06` transcribe mal una fórmula del notebook; la correcta es `1 / (1 + e^-t)`.
- **`4.3.h`:** el R² impreso con signo negativo en el manual es probablemente un artefacto de la extracción del PDF.

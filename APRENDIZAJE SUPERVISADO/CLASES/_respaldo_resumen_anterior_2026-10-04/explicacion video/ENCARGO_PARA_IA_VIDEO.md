# Encargo para explicar el curso mediante videos

Empieza por `INICIO_AQUI.md`. Usa `prompt_tutor_video_v11.md`, alineado con `material_curso/prompt_tutor_chat_v11.md`. El orden completo está en `CATALOGO_COMPLETO_PARA_VIDEOS.md`. El Excel está en `material_curso/Seguimiento_Aprendizaje_Supervisado_mejorado.xlsx`; su hoja **Mapa de estudio** conserva el índice y los estados originales.

Para ver cómo convertir una fila en escenas, consulta `EJEMPLO_VIDEO_1_1_A.md`. Es un ejemplo de un segmento, no una explicación de todas las fases.

## Qué leer en cada fila

| Columna | Uso para el video |
|---|---|
| A, Código | Identifica el tema y sus partes. `1.1` es el tema; `1.1.a`, `1.1.b` son conceptos para segmentos separados. |
| C, Tema / concepto | Conserva el **nombre original del curso**. Pronúncialo cuando la intuición ya esté clara. |
| D, Nivel | `0` = bloque del curso; `1` = tema para un video; `2` = concepto que requiere su propio segmento y pausa. |
| E, Estado | Ayuda a decidir el ritmo. **Comprendido no significa firme**; firme exige resolver un caso nuevo. No cambies estados solo por producir un video. |
| F, Explicación sencilla | Úsala como puente pedagógico para una persona sin ingeniería. Es una reformulación; comprueba los hechos en el material fuente. |
| G, Siguiente paso | Úsalo cuando exista para elegir una aplicación nueva. Si está vacío, crea la aplicación a partir del material fuente sin inventar cifras. |
| J, Fuente | Indica el resumen o material del curso que debes consultar. |

## Material fuente disponible

| Bloque | Archivo de esta carpeta |
|---|---|
| 1. Fundamentos y preparación de datos | `material_curso/02_tema1_fundamentos_y_preparacion_datos.txt` |
| 2. Validación y métricas | `material_curso/03_tema2_validacion_y_metricas.txt` |
| 3. Extracción de características | `material_curso/Tema 3 - Extracción de características.pptx` (teoría y figuras), `material_curso/04_tema3_extraccion_caracteristicas.txt` (resumen de notebooks) |
| 4. Modelos de regresión | `material_curso/05_tema4_modelos_regresion.txt` |
| 5. Modelos de clasificación | `material_curso/06_tema5_modelos_clasificacion.txt` |

Las explicaciones de apoyo están en `material_curso/08_aprendizaje_supervisado_desde_cero.md` y `material_curso/07_explicacion_profunda_por_bloques.md`. No sustituyen las cinco fuentes temáticas. Comprueba en esas fuentes toda fórmula o afirmación técnica antes de narrarla.

También están el manual original `material_curso/05MIAR_GAsencio_nueva_imagen.pdf`, los notebooks y recursos originales en `material_curso/notebooks_y_recursos/`, y versiones de texto del PDF y del PPTX para buscar. Al narrar fórmulas, figuras y código, consulta el archivo original. Lee `ERRATAS_Y_LIMITES.md` antes de producir videos del tema 3 o SVM.

**Fuente del bloque 3:** las diapositivas originales están en `material_curso/`. El archivo `04` resume notebooks. Coteja cada concepto con la diapositiva citada en el catálogo. La diapositiva 35 contiene una definición conflictiva del diámetro de Feret; no la repitas como fórmula válida sin señalar la errata.

**Hueco de fuente de SVM:** el archivo `06` documenta el uso de `SVC`, pero no enseña en detalle la teoría del margen, los vectores de soporte ni los kernels. Presenta el flujo que el código sí demuestra y marca el resto como pendiente de fuente.

## Solicitud lista para copiar a la otra IA

```text
Sigue el archivo «prompt_tutor_video_v11.md» de esta carpeta.
Abre «CATALOGO_COMPLETO_PARA_VIDEOS.md» y sigue los veintinueve temas en su orden.
En esta entrega produce solo el primer video aún no producido; continuaré pidiendo los
siguientes. Cubre todos sus conceptos de nivel 2, uno por segmento.

Tema del video: [código y título de una fila de nivel 1 del Excel].
Conceptos del video: [filas de nivel 2 cuyo código empieza por ese código, en su orden; si no existen, el propio tema de nivel 1 es el segmento, como 3.4].
Material fuente: [archivo local del bloque en la tabla anterior y referencia de la columna J].
Estado previo: [estados de la columna E y, si existe, mi reporte del video anterior].
Meta: comprensión profunda.

Explícame todo de modo que la primera escena la entienda una persona sin formación
en ingeniería. Usa una escena cotidiana. Tras comprobar la intuición con una sola
pregunta, nombra el concepto con su término original del curso y defínelo antes
de usarlo en fórmulas. Si hay tres o más símbolos parecidos, comienza con la
tabla-panorama indicada en el prompt. Una idea por escena y un concepto por
segmento. Usa la explicación sencilla de la columna F como apoyo, pero verifica
cualquier afirmación en el material fuente. No inventes cifras ni fórmulas.

Entrega el video. Si no puedes renderizarlo, entrega el guion completo escena por
escena con narración, visual, animación y tiempo. Incluye por cada concepto una
pausa con una sola pregunta que respondo con mis palabras, errores posibles
sin atribuirme una respuesta que no diste, una nota de una línea y un caso nuevo
sin respuesta inmediata. Pon
las soluciones verificadas al final, después de un aviso de pausa. Cierra con
la plantilla de reporte de verificación y estado de sesión.
```

## Primer encargo sugerido

Empieza con **`1.1 Metodología CRISP-DM`**. Sus filas `1.1.a` a `1.1.f` describen las seis fases y deben ser segmentos separados. La fila `1.1.g` sobre roles también debe cubrirse, como complemento claramente separado de las fases; si el video resulta largo, puede ir en un video complementario del mismo tema. Usa el archivo `02` como fuente. La primera escena debe plantear una decisión real antes de nombrar CRISP-DM. El video no debe marcar el tema como firme hasta que yo resuelva un caso nuevo.

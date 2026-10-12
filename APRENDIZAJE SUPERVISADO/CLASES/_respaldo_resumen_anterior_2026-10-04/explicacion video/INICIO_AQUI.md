# Paquete del curso para una IA que explica con videos

Esta carpeta reúne el conocimiento **disponible aquí** de Aprendizaje Supervisado para producir una serie completa en el orden del curso. La otra IA puede trabajar desde `explicacion video` sin buscar los resúmenes ni el Excel en rutas superiores.

## Qué contiene

| Archivo | Para qué usarlo |
|---|---|
| `prompt_tutor_video_v11.md` | Método obligatorio de explicación, escenas, animación, pregunta y aplicación. |
| `CATALOGO_COMPLETO_PARA_VIDEOS.md` | Índice y fichas de las ciento ochenta y cinco entradas del Excel: cinco bloques, veintinueve temas y ciento cincuenta y un conceptos. |
| `ENCARGO_PARA_IA_VIDEO.md` | Texto listo para pedir a la otra IA el siguiente video de la serie. |
| `EJEMPLO_VIDEO_1_1_A.md` | Un segmento concreto como modelo de narración y visuales. |
| `material_curso/02_...txt` a `material_curso/06_...txt` | Los cinco resúmenes temáticos copiados: hechos, fórmulas, procedimientos y código documentado. |
| `material_curso/05MIAR_GAsencio_nueva_imagen.pdf` | Manual original del curso para los temas uno, dos, cuatro y cinco. |
| `material_curso/Tema 3 - Extracción de características.pptx` | Teoría y figuras originales del tema tres. |
| `material_curso/notebooks_y_recursos/` | Repositorio original de notebooks, código, datos y figuras disponible en `CLASES`. |
| `material_curso/MANUAL_PDF_TEXTO.md` y `material_curso/TEMA3_PPTX_TEXTO.md` | Texto extraído para buscar por página o diapositiva. Verifica fórmulas y figuras en los originales. |
| `material_curso/08_aprendizaje_supervisado_desde_cero.md` | Apoyo para la primera intuición, accesible sin ingeniería. |
| `material_curso/07_explicacion_profunda_por_bloques.md` | Apoyo posterior para profundizar y analizar. |
| `material_curso/Seguimiento_Aprendizaje_Supervisado_mejorado.xlsx` | Nombres originales, estados, explicaciones simples y pasos de aplicación. |
| `material_curso/prompt_tutor_chat_v11.md` | Estilo de aprendizaje vigente al que se alinea el video. |
| `ERRATAS_Y_LIMITES.md` | Conflictos detectados en la fuente y límites del material disponible. |

## Orden de trabajo de la IA de video

1. Lee `prompt_tutor_video_v11.md` y `material_curso/prompt_tutor_chat_v11.md`.
2. Abre el índice de veintinueve videos al comienzo de `CATALOGO_COMPLETO_PARA_VIDEOS.md` y elige el siguiente tema de nivel 1 en orden, aunque su estado previo sea «Comprendido».
3. Consulta cada ficha de nivel 2 de ese tema. Conserva el nombre original, pero empieza la narración con una escena cotidiana y explica la intuición antes del término formal, salvo la excepción de símbolos parecidos.
4. Verifica cada afirmación técnica en el manual PDF o el PowerPoint original de `material_curso/` y, cuando aplique, en el notebook original. Usa los resúmenes temáticos y las guías `07` y `08` como apoyo, no como autoridad para llenar huecos de la fuente.
   Si una nota anterior del Excel dice que falta verificar el PPTX, consulta `ERRATAS_Y_LIMITES.md`: el PPTX ya está integrado y allí se documenta lo que se encontró.
5. Produce **un video por tema de nivel 1**. Dentro de él, un segmento por concepto de nivel 2, con una sola pregunta de comprensión y un caso nuevo de aplicación. `3.4` no tiene filas de nivel 2: explícalo como un solo segmento. Entrega video si puedes renderizarlo; en caso contrario, guion completo escena por escena.
6. Termina con solucionario separado y reporte para que el estudiante responda. Espera el reporte antes de actualizar estados o reenseñar un paso. Sigue con el próximo tema cuando corresponda.

## Límites y erratas

- El PowerPoint original del tema 3 **sí está incluido**. Consulta sus diapositivas y figuras. La diapositiva 35 parece llamar «diámetro de Feret» a un cociente de áreas que la propia diapositiva llama «extensión»; revisa `ERRATAS_Y_LIMITES.md` antes de enseñar ese punto.
- La fuente `06` muestra el uso de `SVC`, pero no desarrolla toda la teoría de **SVM**. Explica lo que el código sí demuestra y marca lo demás como pendiente de fuente.

**Alcance real:** el paquete integra los resúmenes, el manual PDF, el PowerPoint del tema tres y el repositorio de notebooks encontrados en `CLASES`. Conserva los límites de contenido que siguen existiendo.

# 08 — Dunlosky, Rawson, Marsh, Nathan & Willingham (2013)

> **PDF asociado:** `dunloskiimprovingstudentlearning.pdf`

## Ficha bibliográfica

| Campo | Valor |
|---|---|
| **Título** | *Improving Students' Learning With Effective Learning Techniques: Promising Directions From Cognitive and Educational Psychology* |
| **Autores** | John Dunlosky, Katherine A. Rawson, Elizabeth J. Marsh, Mitchell J. Nathan, Daniel T. Willingham |
| **Institución** | Kent State University / Duke University / U. Wisconsin-Madison / U. Virginia |
| **Año** | 2013 |
| **Revista** | *Psychological Science in the Public Interest* |
| **Tipo** | Monografía de revisión — el documento **más importante de toda la carpeta** para diseñar la metodología del Modo Maestro: evalúa 10 técnicas de estudio y les asigna una utilidad (alta/moderada/baja) según 4 criterios (condiciones de aprendizaje, características del estudiante, materiales, tareas de criterio) |

## Las 10 técnicas y su veredicto final (Tabla 4 del paper)

| Técnica | Utilidad | Resumen del veredicto |
|---|:---:|---|
| **Practice testing** (autoevaluación/tests de práctica) | **ALTA** | La técnica mejor evaluada de las 10. Funciona en todas las edades, materiales y tareas; efectos duraderos (semanas a años); barata de implementar. |
| **Distributed practice** (práctica distribuida) | **ALTA** | Igual de bien evaluada. Ver `07_Cepeda_2006...md` para el detalle. |
| Interleaved practice (entrelazado) | Moderada | Prometedora pero con menos estudios totales y algunos nulos — probablemente porque aún no se entienden bien las condiciones exactas en que funciona. |
| Elaborative interrogation ("¿por qué es verdad esto?") | Moderada | Efectos grandes (d=0.85–2.57) pero limitada a hechos discretos, y depende de tener conocimiento previo del tema. |
| Self-explanation | Moderada | Ver más abajo — variante más flexible de la interrogación elaborativa. |
| Summarization (resumir) | Baja | Solo funciona si el resumen es de buena calidad, y eso exige entrenamiento; en la práctica muchos estudiantes hacen resúmenes mediocres. |
| **Highlighting/underlining** (subrayar) | **Baja** | La técnica más usada por los estudiantes y una de las **menos efectivas**. Puede incluso perjudicar preguntas de inferencia. |
| Keyword mnemonic | Baja | Solo aplica a vocabulario "amigable a imágenes"; además provoca **olvido acelerado** en comparación con la repetición simple a largo plazo. |
| Imagery use (imaginar mientras se lee) | Baja | Efectos inconsistentes; funciona mejor escuchando que leyendo. |
| **Rereading** (releer) | **Baja** | La segunda técnica más usada por los estudiantes (84% la reporta) y de las menos efectivas — pierde sistemáticamente contra self-explanation, elaborative interrogation y practice testing en comparaciones directas. |

## Por qué "practice testing" es la ganadora clara (detalle clave)

- El **testing effect** (o "efecto de recuperación") es más potente cuanto MÁS se recupera de memoria, no cuánto se re-estudia: en un experimento icónico (Karpicke & Roediger 2008 — ver `09_Karpicke_Roediger_2008...md`), seguir *testeando* ítems ya aprendidos una vez dio 80% de retención una semana después, contra solo 36% si se seguían *reestudiando* en vez de testear.
- Funciona incluso con **tests de opción múltiple, no solo recuerdo libre**, y el formato del test de práctica no necesita coincidir con el del examen final (un MCQ de práctica ayuda igual a un examen final de respuesta corta).
- El feedback es clave: testing **con feedback** supera consistentemente a testing sin feedback, y el feedback puede darse con demora sin perder el beneficio (incluso ayuda más a corregir errores de alta confianza).
- **Más dosis es mejor** (más tests, más veces) y **el espaciado entre tests es mejor que amontonarlos** (mismo principio que distributed practice).

## Por qué "highlighting" y "rereading" —las dos técnicas MÁS usadas— fallan

Ambas dan una sensación de fluidez ("ya lo leí, ya lo entiendo") que es **ilusoria** — no obligan al cerebro a producir nada, solo a reconocer texto ya visto. Ninguna mejora consistentemente el desempeño en exámenes frente a simplemente no usarlas, y el subrayado puede incluso perjudicar preguntas de inferencia (el lector se enfoca en frases sueltas en vez de conexiones entre ideas).

## Self-explanation (contexto para el paper 03, Hodds et al., ya guardado)

Este monograph confirma independientemente lo que dice `03_Hodds_2014_SelfExplanation_ProofComprehension.md`: el "por qué" durante el estudio funciona, aunque aquí se rebaja a utilidad "moderada" (no "alta") porque falta evidencia sobre retención a largo plazo y en contextos educativos reales — Hodds et al. (2014) es justamente uno de los estudios que después llenó ese hueco para el caso específico de demostraciones matemáticas.

## Principios extraíbles para estudio

- **[P29]** Si solo puedes adoptar 2 técnicas de estudio, que sean **practice testing** y **distributed practice** — son las únicas con calificación "alta" en las 4 dimensiones evaluadas.
- **[P30]** Abandona subrayar y releer como técnicas principales — no es que sean inútiles, es que hay alternativas mucho mejores por el mismo tiempo invertido.
- **[P31]** El testing debe incluir feedback (mostrar la respuesta correcta) — testing sin feedback es notablemente menos efectivo que testing con feedback.
- **[P32]** La calidad de un resumen (o de un subrayado, o de una autoexplicación) importa más que el mero hecho de hacerlo — un resumen malo no ayuda; hay que aprender a hacerlos bien o preferir una técnica que no dependa tanto de la calidad de ejecución (como el testing).

## Aplicación a Matemáticas para IA (Máster VIU)

| Situación | Estrategia |
|---|---|
| Diseño del Modo Maestro (decisión de arquitectura) | Confirma la decisión ya tomada: el corazón del flujo debe ser **responder una pregunta con feedback inmediato**, no solo leer teoría — es la técnica con más evidencia de las 10 |
| Tentación de "solo releer los apuntes de la sesión" antes de un repaso | Sustituir por autoevaluarte con las preguntas de examen ya extraídas — releer es de las técnicas peor evaluadas de las 10 |
| Vas a resaltar el PDF de una sesión de clase | Mejor evita esa técnica salvo para localizar después una definición puntual — no mejora la retención por sí sola |

## Una frase para llevarte

> **"De 10 técnicas de estudio evaluadas con el mismo rigor, solo 2 recibieron la calificación más alta posible: hacerte preguntas de práctica (con feedback) y distribuir el estudio en el tiempo — las dos técnicas que más usan los estudiantes, subrayar y releer, están entre las peor evaluadas."**

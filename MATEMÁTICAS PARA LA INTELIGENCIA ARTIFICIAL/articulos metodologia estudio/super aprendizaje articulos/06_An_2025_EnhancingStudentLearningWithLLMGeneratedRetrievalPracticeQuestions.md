# 06 — An, Liu, Acharya & Hashmi (2025)

> **PDF asociado:** `2507.05629v2.pdf`

## Ficha bibliográfica

| Campo | Valor |
|---|---|
| **Título** | *Enhancing Student Learning with LLM-Generated Retrieval Practice Questions: An Empirical Study in Data Science Courses* |
| **Autores** | Yuan An, John Liu, Niyam Acharya, Ruhma Hashmi |
| **Institución** | College of Computer and Informatics, Drexel University |
| **Año** | 2025 (arXiv 2507.05629, jul. 2025) |
| **Tipo** | Cuasi-experimento (diseño de grupos no equivalentes) en 2 cursos universitarios de Data Science, ~60 estudiantes |

## Por qué este paper es especial (relevancia directa para el Modo Maestro)

Es el único de los 9 papers de esta carpeta que estudia exactamente el escenario de Lucas: **usar un LLM para generar las preguntas de retrieval practice** de un curso técnico. Es, en efecto, el paper que valida (y advierte sobre) la metodología que se está usando para construir el Modo Maestría Matemáticas.

## Pregunta de investigación y hallazgo

¿El uso frecuente de preguntas de opción múltiple (MCQ) generadas por LLM como retrieval practice durante clases en vivo mejora la retención? Diseño: 2 ciclos de 2 semanas — un ciclo con MCQs generadas por LLM cada 10-15 min de clase (con feedback inmediato), el otro sin ninguna práctica de recuperación. Se midió con un quiz al final de cada ciclo.

- Con retrieval practice (LLM): **89% de precisión** (media)
- Sin retrieval practice: **73% de precisión** (media)
- Diferencia estadísticamente muy significativa (Mann-Whitney U, p < 0.0001) y con tamaño de efecto grande (r = 0.586)

## Cómo generaron las preguntas (el prompt real)

Convirtieron el contenido de cada notebook de clase a markdown y lo inyectaron en un prompt que exigía explícitamente: mezcla de recall factual y pensamiento de orden superior (aplicación/análisis), una respuesta correcta y 3 distractores plausibles, **sin pistas en el enunciado que revelen la respuesta**, opciones gramaticalmente paralelas, y explicación de por qué cada distractor es incorrecto. Pedían generar 15 MCQs por sesión para poder filtrar y quedarse solo con las 5 mejores.

## Las 12 formas en que un LLM genera preguntas de mala calidad (checklist crítico)

De cada 15 MCQs generadas, ~2/3 no cumplían el estándar. Categorías de fallo documentadas con ejemplos reales:

1. **Errores en pregunta/opciones** (el LLM razonó mal el contenido, p. ej. slicing de arrays con índices negativos).
2. **Alucinaciones** (inventa un atributo/concepto que nunca se enseñó, ej. `arr.rank`).
3. **Pistas en el enunciado** (la pregunta cita literalmente el título de la sección donde está la respuesta).
4. **Opciones duplicadas** (dos distractores son sinónimos exactos, ej. "media" y "promedio").
5. **Respuestas ambiguas** (dos opciones son defendibles según el contexto).
6. **Distractores demasiado fáciles** (se descartan sin saber nada del tema).
7. **Conocimiento trivial** (pregunta de memorización pura, sin valor pedagógico).
8. **Formato inconsistente entre opciones** (la correcta es notablemente más larga → se delata sola).
9. **Solo negaciones en los distractores** (la única opción sin "no"/"nunca" es la correcta → patrón detectable sin saber el contenido).
10. **Preguntas de doble concepto** (mezcla dos ideas desconectadas en el enunciado, generando confusión en vez de evaluación).
11. **Suposición incorrecta** (asume que un orden sugerido por una API es "el único correcto", cuando no lo es).
12. **Pregunta ambigua** (términos sin anclaje claro al contexto del curso).

## Principios extraíbles para estudio (y para construir el Modo Maestro)

- **[P22]** Retrieval practice generada por IA, con feedback inmediato y en dosis de ~5 preguntas cada 10-15 min, produjo una mejora de 16 puntos porcentuales en un curso técnico real — validación directa de la estrategia general del Modo Maestro (pregunta → feedback → seguir).
- **[P23]** **Nunca liberar preguntas generadas por IA sin revisión humana.** El propio estudio generó 15 para poder filtrar y quedarse con 5 buenas — la tasa de descarte fue ~2/3.
- **[P24]** Antes de aceptar una pregunta para `EX_MATH`, pasarla por el checklist de 12 fallos de arriba — en particular: ¿el enunciado revela la respuesta? ¿los distractores son plausibles (no solo "obviamente falsos")? ¿la opción correcta tiene el mismo formato/longitud que las demás? ¿los distractores no son solo negaciones?
- **[P25]** Las preguntas ya extraídas literalmente de los dos exámenes reales de Lucas (no generadas desde cero por un LLM) están libres del riesgo de alucinación de contenido — ese es precisamente el motivo por el que el plan del Modo Maestro prioriza usar las preguntas reales de examen y de la investigación de Lucas en vez de generar preguntas nuevas.

## Limitaciones que reporta el propio estudio

Diseño cuasi-experimental (no aleatorización individual), muestra pequeña (~60), solo MCQs (no preguntas abiertas), medición de retención a corto plazo (ciclos de 2 semanas), y no midieron el tiempo de validación humana requerido.

## Aplicación a Matemáticas para IA (Máster VIU)

| Situación | Estrategia |
|---|---|
| Escribir una pregunta nueva para `EX_MATH` (no extraída de un examen real) | Pasarla por el checklist de 12 fallos antes de incluirla — especialmente: sin pistas en el enunciado, distractores parejos en formato y plausibilidad |
| Adaptar las preguntas de los exámenes reales de Lucas | Riesgo bajo de alucinación (ya vienen validadas por la profesora), pero igual revisar que la solución paso a paso no tenga errores de cálculo |
| Diseñar el ritmo del Modo Maestro | 1 pregunta de práctica por tema, con feedback inmediato tras responder — igual que el protocolo de este estudio (5 MCQs cada 10-15 min) |

## Una frase para llevarte

> **"Un LLM generando preguntas de práctica SÍ mejora el aprendizaje (89% vs 73%), pero 2 de cada 3 preguntas que genera fallan en algo — la revisión humana con un checklist explícito no es opcional."**

# Extracción de conocimiento — "A Meta-Analysis of Ten Learning Techniques"

## 1. Datos bibliográficos

- **Título real:** *A Meta-Analysis of Ten Learning Techniques*
- **Autores:** Gregory M. Donoghue* y John A. C. Hattie
- **Afiliación:** Science of Learning Research Centre, Graduate School of Education, University of Melbourne, Melbourne, VIC, Australia
- **Journal:** *Frontiers in Education* (sección Educational Psychology)
- **Volumen/Artículo:** Front. Educ. 6:581216
- **DOI:** 10.3389/feduc.2021.581216
- **Tipo de artículo:** Systematic Review (meta-análisis cuantitativo)
- **Fechas:** recibido 08 julio 2020; aceptado 08 febrero 2021; **publicado 31 marzo 2021** (por tanto el año exacto de publicación es **2021**)
- **Palabras clave:** meta-analysis, learning strategies, transfer of learning, learning technique, surface and deep learning
- **Cita:** Donoghue GM y Hattie JAC (2021). A Meta-Analysis of Ten Learning Techniques. Front. Educ. 6:581216. doi:10.3389/feduc.2021.581216

Nota importante: este paper **no es un estudio original independiente**, sino un **meta-análisis cuantitativo construido sobre la base bibliográfica de la revisión narrativa de Dunlosky et al. (2013a)**, "Improving students' learning with effective learning techniques" (Psychological Science in the Public Interest). Dunlosky et al. habían clasificado cualitativamente 10 técnicas de aprendizaje en Alto/Moderado/Bajo soporte empírico, pero sin calcular tamaños de efecto. Donoghue y Hattie toman las mismas 399 referencias, calculan Cohen's d para cada estudio utilizable, y añaden análisis de moderadores que Dunlosky et al. no habían hecho.

## 2. Objetivo / pregunta de investigación

Dos objetivos explícitos:

1. **Proveer estimaciones empíricas cuantitativas (tamaños de efecto)** de la efectividad de las 10 técnicas de aprendizaje que Dunlosky et al. (2013a) habían clasificado solo cualitativamente como Alto/Moderado/Bajo soporte, sin indicar la magnitud real de esos términos.
2. **Evaluar empíricamente los moderadores** de esas 10 técnicas (p. ej. aprendizaje superficial vs. profundo, transferencia cercana vs. lejana, edad/nivel educativo, país, dominio de contenido, nivel de habilidad, factor de impacto de la revista, año de publicación, demora del post-test), algo que la revisión original de Dunlosky et al. no había hecho de forma empírica/estadística.

Las 10 técnicas analizadas (con la clasificación original de Dunlosky et al. 2013a entre paréntesis):
- **Alto soporte:** Practice Testing (autoevaluación/tests de práctica), Distributed Practice (práctica distribuida/espaciada)
- **Soporte moderado:** Elaborative Interrogation (interrogación elaborativa, preguntas "¿por qué?"), Self-Explanation (autoexplicación), Interleaved Practice (práctica intercalada)
- **Bajo soporte:** Summarization (resumir), Highlighting/Underlining (subrayado/resaltado), Keyword Mnemonic (mnemotecnia de palabra clave), Imagery Use (uso de imaginería mental), Re-Reading (relectura)

## 3. Metodología

**Tipo de estudio:** meta-análisis cuantitativo (no un estudio empírico primario ni una revisión narrativa nueva; es un re-análisis estadístico de estudios ya identificados por Dunlosky et al. 2013a).

**Fuente de datos:** las 399 referencias citadas en Dunlosky et al. (2013a). Se excluyeron los estudios no empíricos y aquellos que no reportaban datos suficientes para calcular un Cohen's d. Quedaron:
- **242 estudios** incluidos en el meta-análisis
- **1,619 efectos** (el método menciona 1,620 "casos" con d calculado — pequeña discrepancia numérica en el propio texto del paper)
- **169,179 participantes únicos**

**Codificación:** los dos autores codificaron todos los artículos; colegas independientes re-codificaron una muestra de 30 estudios (~10%) para estimar fiabilidad entre codificadores → **kappa = 0.89** (alta fiabilidad).

**Tres conjuntos de moderadores codificados:**
1. *Atributos del artículo:* calidad de la revista (h-index / factor de impacto), año de publicación, tamaño de muestra.
2. *Atributos del estudiante:* nivel de habilidad (bajo/promedio/alto), país, nivel educativo (preescolar/primaria, secundaria, universidad, adultos).
3. *Atributos del diseño:* transferencia cercana vs. lejana (near vs. far transfer), profundidad del resultado (superficial/específico de contenido vs. profundo/generalizable), demora entre la intervención y el test (menos de 1 día vs. 2+ días, con más granularidad en el análisis), dominio de aprendizaje/contenido (p. ej. cognitivo, no cognitivo, inglés, ciencias, matemáticas...).

**Cálculo del tamaño de efecto (Cohen's d):**
- Método 1: diferencia de medias estandarizada = (media grupo experimental − media grupo control) / SD combinada (pooled), para N=1,203 efectos.
- Método 2: conversión desde estadísticos F (para diseños de dos grupos).
- Corrección de sesgo por tamaño muestral pequeño según Hedges y Olkin (1985) (fórmula de Hedges' g).
- Detección de outliers con el test de Grubbs (1950); los valores atípicos se sustituyeron por el valor de su vecino más cercano.
- Cálculo de tamaños de efecto promedio mediante **ponderación por varianza inversa**; se calcularon intervalos de confianza del 95%.
- Heterogeneidad evaluada con estadísticos **Q** e **I²**.
- Se corrieron **dos modelos en paralelo (efectos fijos y efectos aleatorios)** como análisis de sensibilidad; como ambos dieron resultados muy similares (media global 0.56 en ambos), se usó el modelo de **efectos aleatorios** para los análisis de moderadores posteriores.
- Análisis de moderadores mediante **análisis de subgrupos con modelo de efectos mixtos** (todos los moderadores eran variables categóricas).
- Software: **Comprehensive Meta-Analysis versión 2** (Borenstein et al., 2005).

**Características de la muestra de estudios:**
- Rango de publicación: **1929–2014**, con la mitad publicados desde 1996.
- Participantes: 65% universitarios (undergraduates), 13% primaria, 11% secundaria, 9% educación infantil temprana, 2% adultos.
- Nivel de habilidad: 86% habilidad promedio, 7% baja, 7% alta.
- País: 86% norteamericanos, 11% europeos, 3% australianos (desglose más fino más abajo).
- Diseño: 91% experimental vs. grupo control, 6.5% longitudinal (pre-post / series temporales), 2.4% intra-sujeto.
- Profundidad del resultado: 93% superficial, 7% profundo.
- Demora del post-test: 74% en ≤1 día, 17% entre 2–7 días, 3.3% entre 8 días y 1 mes, 0.4% entre 1–3 meses, 0.2% entre 4 meses y 7 años.

## 4. Hallazgos clave con cifras

### 4.1 Efecto global

- Media global (modelo de efectos fijos): **d = 0.56** (SD = 0.81, SEM = 0.072, asimetría = 1.3, curtosis = 5.64)
- Media global (modelo de efectos aleatorios): **d = 0.56** (SE = 0.016)
- Media global a nivel de estudio (agregando por estudio, no por efecto individual): **d = 0.77** (SE = 0.049)
- Heterogeneidad muy alta: **Q = 10,688.2, I² = 84.87%** → la mayor parte de la variabilidad entre estudios se debe a heterogeneidad real, no al azar, lo que justifica la búsqueda de moderadores.
- Como referencia de contexto: Hattie (2009, 2012, 2015) reportó un efecto promedio de **d = 0.40** sobre más de 1,200 meta-análisis educativos generales. **Las 10 técnicas analizadas aquí superan todas ese 0.40**, es decir, incluso la técnica "peor" del grupo (Summarization/Underlining, d=0.44) está por encima del promedio típico de la investigación educativa.

### 4.2 Tamaño de efecto por técnica (Tabla 1 del paper)

| Técnica | Clasificación Dunlosky | N único | d (Cohen's d) | SEM | I² (%) |
|---|---|---|---|---|---|
| Distributed Practice (práctica distribuida) | Alta | 152,952 | **0.85** | 0.053 | 83 |
| Practice Testing (autoevaluación) | Alta | 6,033 | **0.74** | 0.04 | 86 |
| Elaborative Interrogation | Moderada | 2,138 | **0.56** | 0.048 | 78 |
| Imagery (imaginería) | Moderada | 1,052 | **0.56** | 0.061 | 68 |
| Self-Explanation | Moderada | 804 | **0.54** | 0.092 | 77 |
| Keyword Mnemonic | Baja | 580 | **0.50** | 0.104 | 89 |
| Re-Reading (relectura) | Baja | 1,529 | **0.47** | 0.06 | 86 |
| Interleaved Practice | Baja | 972 | **0.47** | 0.089 | 88 |
| Underlining (subrayado) | Baja | 1,129 | **0.44** | 0.115 | 77 |
| Summarization (resumir) | Baja | 1,990 | **0.44** | 0.055 | 89 |
| **Promedio/Total** | — | 169,179 | **0.56** | — | 85 |

(Nota de fidelidad: la columna "# Cases" de la tabla original se extrajo con superposición/mala alineación al convertir el PDF a texto, por lo que no se transcriben aquí cifras de número de casos por técnica individuales para evitar errores; sí son fiables los valores de d, SEM, N único e I².)

Umbrales empíricos que emergen de los propios datos (y que los autores comparan con las etiquetas cualitativas de Dunlosky et al.):
- **Alto:** d > 0.70
- **Moderado:** d entre 0.54 y 0.69
- **Bajo:** d < 0.53

Los autores señalan que esta correspondencia con las etiquetas de Dunlosky es buena en general, pero que los cortes son **arbitrarios**: Mnemonics (0.50), Re-Reading (0.47) e Interleaved Practice (0.47) están a menos de 0.06 de la categoría "moderada" (0.54) y "pueden tener una importancia similar a las clasificadas como Moderadas... ciertamente no deberían descartarse como ineficaces". Del mismo modo, Underlining y Summarization (ambas d=0.44), pese a ser las de menor efecto, siguen considerándose "suficientemente efectivas para incluirse en la caja de herramientas de un estudiante".

### 4.3 Moderadores — resultados específicos

**Año de publicación:** sin relación entre la magnitud del efecto y el año del estudio (r = 0.08, df = 236, p = 0.25) → los efectos de las técnicas de aprendizaje **no han cambiado entre 1929 y 2015**.

**Nivel de habilidad del estudiante:** de los 242 estudios, solo 6 estudiaron estudiantes de habilidad Alta y 13 de habilidad Baja (submuestras pequeñas). A través de todas las técnicas:
- Efecto medio en estudiantes de **habilidad Alta: d = −0.11** (SE = 0.10, N = 28)
- Efecto medio en estudiantes de **habilidad Baja: d = 0.47** (SE = 0.15, N = 58)
- Es decir, **los efectos fueron mucho mayores en estudiantes de baja habilidad que de alta habilidad** (confirma lo indicado en el abstract). Los estudiantes de alta habilidad mostraron efectos **negativos** específicamente para Interleaved Practice y Summarization.

**Demora (delay) del post-test:** la mayoría de estudios midió efectos muy a corto plazo (68% evaluados dentro del mismo día, generalmente de inmediato), con la excepción de Practice Testing, Distributed Practice e Interleaved Practice, que sí tienen datos a más largo plazo. No hubo diferencias globales relevantes por demora:
- < 1 día: d = 0.58 (SE = 0.025, N = 1,073)
- > 1 día y < 1 semana: d = 0.59 (SE = 0.057, N = 204)
- > 1 semana y < 1 mes: d = 0.56 (SE = 0.058, N = 228)
- > 1 mes y < 6 meses: d = 0.51 (SE = 0.082, N = 64)

**Factor de impacto de la revista:** factor de impacto promedio = 2.80 (SE = 3.29). Correlación positiva moderada entre tamaño de efecto y factor de impacto de la revista: **r(235) = 0.24, p < 0.001** → los tamaños de efecto fueron ligeramente mayores en revistas más citadas.

**Dominio de aprendizaje:** la gran mayoría de la evidencia mide logro académico: 222/242 estudios (91.7%) y 1,527/1,619 efectos (94.3%). Inglés/Lectura fue la base de 85 estudios (35.1%) / 546 efectos (33.7%); Ciencias, 41 estudios (16.9%) / 336 efectos (20.8%). Hubo variación considerable de los tamaños de efecto entre dominios de contenido (tabla del paper con esta desagregación se extrajo con problemas de alineación al convertir el PDF; se destaca solo con confianza que Mnemonics mostró su efecto más alto en el dominio de Inglés, d ≈ 1.17, mucho más alto que su efecto promedio general de 0.50 — sugiere fuerte dependencia del dominio de contenido).

**Transferencia cercana vs. lejana (near vs. far transfer):** hubo muy pocos efectos de transferencia lejana, tan pocos que el paper no los desagrega por técnica. Los efectos de transferencia **cercana (d = 0.61, SE = 0.052, N = 197)** fueron **mucho mayores** que los de transferencia **lejana (d = 0.39, N = 1,385)**. (Nota de fidelidad: el paper reporta un SE = −0.002 para el grupo de transferencia lejana, valor negativo imposible para un error estándar; probablemente sea un artefacto de OCR/composición tipográfica del PDF original. Además, el propio texto dice que hubo "so few Far transfer effects" pero luego el N reportado para "Far" (1,385) es mayor que el de "Near" (197), lo cual es contradictorio; puede deberse a un error de rotulación de columnas en el PDF original y se reporta aquí tal como aparece, con esta advertencia de posible inconsistencia en la fuente.)

**Profundidad del aprendizaje (Surface vs. Deep):** los efectos fueron mayores para procesamiento **Superficial (d = 0.60, SE = 0.021, N = 1,473)** que para procesamiento **Profundo (d = 0.26, SE = 0.064, N = 109)**. Esta es una de las conclusiones más importantes del paper: las técnicas rinden mucho menos cuando se busca comprensión profunda/relacional que cuando se busca recuerdo/reconocimiento superficial.

**Nivel educativo (grade level)** — tabla con datos limpios del paper (d, SE, N por técnica y nivel):

| Técnica | Primaria (d, SE, N) | Secundaria (d, SE, N) | Universidad (d, SE, N) |
|---|---|---|---|
| Distributed Practice | 0.57, 0.11, 15 | 0.70, 0.24, 5 | 0.89, 0.06, 115 |
| Elaborative Interrogation | 0.38, 0.14, 28 | 0.71, 0.06, 84 | 0.58, 0.09, 110 |
| Imagery | 0.38, 0.06, 101 | 0.82, 0.17, 8 | 1.16, 0.18, 26 |
| Interleaved Practice | −0.20, 0.15, 13 | 0.00, 0.07, 12 | 0.65, 0.11, 79 |
| Mnemonics | 0.00, 0.00, 6 | 0.69, 0.17, 29 | 0.20, 0.13, 72 |
| Practice Testing | −0.25, 0.56, 6 | 0.99, 0.24, 22 | 0.80, 0.04, 278 |
| Re-Reading | 1.33, 0.26, 6 | (sin datos) | 0.42, 0.06, 107 |
| Self-Explanation | 0.28, 0.09, 15 | 0.57, 0.16, 36 | 0.60, 0.15, 42 |
| Summarization | 1.20, 0.13, 25 | 0.75, 0.14, 58 | 0.19, 0.05, 151 |
| Underlining | −0.06, 0.18, 10 | −0.10, —, 1 | 0.57, 0.14, 43 |
| **Total** | **0.42, 0.05, 225** | **0.69, 0.05, 255** | **0.59, 0.03, 1,023** |

Patrón textual del paper: en general los estudiantes mayores tuvieron efectos más altos en Summarization, Distributed Practice, Imagery y Re-Reading; los estudiantes de primaria tuvieron efectos más bajos en Interleaved Practice, Mnemonics, Self-Explanation y Practice Testing; tanto primaria como secundaria tuvieron efectos más bajos en Underlining que universidad.

**País:** de los 242 estudios, 187 (77.3%) de EE.UU., 20 (8.3%) de Canadá, 27 (11.1%) de Europa (Reino Unido, Dinamarca, Francia, Alemania, Italia, Países Bajos), 7 (2.9%) de Australia y 1 (0.4%) de Irán — total norteamericano (EE.UU.+Canadá) = 207 (85.6%). Los autores concluyen que, salvo una caída en Europa para Mnemonics, Interleaved Practice y Summarization, "no hay gran diferencia por país" (la tabla desagregada por técnica y país se extrajo del PDF con problemas de alineación de columnas y no se reproduce en detalle aquí por fidelidad).

## 5. Mecanismos / teoría explicativa

- **Practice Testing (autoevaluación):** el mecanismo central es la **práctica de recuperación (retrieval practice)**: el estudiante reproduce la información desde la memoria y compara con la respuesta correcta, generando **feedback** que corrige su comprensión. Esto aumenta la probabilidad de que la información se pueda recuperar luego desde la memoria a largo plazo y ayuda a organizar mentalmente la información de forma que sostiene mejor retención y desempeño. Funciona con cualquier formato de test (opción múltiple o ensayo), incluso cuando el formato de práctica no coincide con el del test final, y para todas las edades. Funciona incluso masificado (massed) pero mejor si se espacía. El **moderador crítico es el feedback**: "la ventaja de Practice Testing con feedback sobre re-estudio es extremadamente robusta" y también supera consistentemente a Practice Testing sin feedback. Sin feedback, si el estudiante practica respuestas incorrectas, esos errores se aprenden y se convierten en "errores de alta confianza".
- **Distributed/Spaced Practice:** la mayoría de los estudiantes necesita de 3 a 4 oportunidades para aprender algo (Nuthall, 2007), pero esas oportunidades son más efectivas si se distribuyen en el tiempo en vez de concentrarse en una sola sesión masiva. Cepeda et al. (2008) mostraron que, para casi todos los intervalos de retención, el desempeño de memoria aumenta fuertemente con la longitud del intervalo de espaciado hasta un punto óptimo, tras el cual el desempeño declina (aunque solo levemente); esto no toma en cuenta que el nivel absoluto de desempeño decrece con intervalos de retención más largos. Es más efectiva para procesamiento profundo que superficial, y funciona para todas las edades.
- **Elaborative Interrogation:** se basa en generar explicaciones ("¿Por qué tiene sentido que...?", "¿Por qué es esto cierto?") con el propósito de **integrar la información nueva con el conocimiento previo**. Es más efectiva cuando las elaboraciones son precisas (no imprecisas), cuando el conocimiento previo es mayor, y cuando las elaboraciones son autogeneradas en vez de provistas. Es más aplicable a comprensión superficial que profunda.
- **Self-Explanation:** el estudiante explica cómo la información nueva se relaciona con lo que ya sabe. Funciona a través de dominios y edades, pero puede requerir entrenamiento y tiempo para implementarse.
- **Interleaved Practice:** alternar el estudio de distintos tipos de ítems/problemas/dominios en vez de bloquear el estudio por tipo. El mecanismo propuesto (retomando a Carvalho y Goldstone, 2015) es que el orden en que se presenta la información afecta el aprendizaje según si el estudio es activo o pasivo: en condición de **estudio activo**, los aprendices buscan características que discriminan entre categorías, y esas características son más fáciles de detectar cuando las categorías alternan frecuentemente (es decir, con intercalado). En condición de **estudio pasivo**, los aprendices buscan características que aparecen consistentemente dentro de una categoría, más fáciles de detectar cuando las categorías rara vez alternan (bloqueo). La evidencia sobre cómo intercalar de manera óptima aún es limitada.
- **Summarization:** escribir resúmenes que capturen los puntos principales y excluyan material poco importante o repetitivo. La generalidad y precisión del resumen son moderadores importantes; no está claro si es mejor resumir piezas pequeñas de texto con más frecuencia o resúmenes más grandes con menor frecuencia. Los estudiantes más jóvenes y de menor habilidad son peores resumiendo; funciona mejor con evaluaciones de desempeño/generativas que con tests cerrados/opción múltiple; puede requerir entrenamiento extenso.
- **Highlighting/Underlining:** simple de usar, no requiere entrenamiento, casi no añade tiempo extra. Más efectivo cuando lo hace un profesional (p.ej. el profesor) que cuando lo hace el propio estudiante, y menos efectivo aún cuando se lee el subrayado de otro estudiante. Puede perjudicar la capacidad posterior de hacer inferencias; en general aporta poco al desempeño.
- **Keyword Mnemonic:** asociar imaginería con la palabra o concepto a aprender. Requiere generar imágenes, lo cual es difícil para estudiantes más jóvenes y de menor habilidad; hay evidencia de que puede no producir retención duradera.
- **Imagery Use:** el estudiante imagina mentalmente o dibuja el contenido usando imágenes simples y claras. Está limitado a materiales que se prestan a la imaginería y a la capacidad de memoria de trabajo.
- **Re-Reading:** más efectiva cuando es espaciada que masiva; los efectos parecen decrecer más allá de la segunda lectura; mejor para recuerdo factual que para desarrollar comprensión; no está claro que sea efectiva por debajo de la edad universitaria.

**Modelo teórico más amplio propuesto por los autores** (retomando Hattie y Donoghue, 2016): las técnicas de aprendizaje se pueden optimizar en distintas **fases de aprendizaje** — de Superficial a Profundo a Transferencia —, en la adquisición y consolidación de conocimiento y comprensión, involucrando tres entradas/salidas: **conocer, disposiciones y motivaciones** ("el *skill*, el *will* y el *thrill*"). Ejemplo del propio paper: la memorización y el Practice Testing pueden ser efectivos para **consolidar** conocimiento superficial, pero no son efectivos si primero no se ha **adquirido** ese conocimiento superficial. El aprendizaje basado en problemas es relativamente ineficaz para promover conocimiento superficial, pero más efectivo para la comprensión profunda, por lo que sería óptimo aplicarlo **después** de que se haya demostrado que los estudiantes tienen suficiente conocimiento superficial de base.

## 6. Recomendaciones prácticas concretas

Del propio meta-análisis (Discusión y Conclusión):

1. **No usar estas técnicas como "intervenciones" aisladas ni como cursos de técnicas de estudio separados.** Deben integrarse **dentro del proceso de enseñanza** para maximizar resultados superficiales y profundos a lo largo de una secuencia de lecciones.
2. **Practice Testing no es excusa para más evaluación de alto riesgo (high-stakes testing).** El hallazgo de que es una de las dos técnicas más efectivas no implica que haya que aumentar los exámenes formales; lo que importa es el **uso hábil** de la práctica de recuperación para aprender y consolidar, no la frecuencia de las pruebas.
3. **Acompañar siempre el Practice Testing de feedback** — es el moderador más determinante de su efectividad; sin feedback, los errores se refuerzan.
4. **Secuenciar las técnicas según la fase de aprendizaje:** las técnicas de "alto" efecto orientadas a la práctica (Practice Testing, Distributed Practice) parecen más apropiadas para **consolidar** aprendizaje ya adquirido; las técnicas de "bajo" efecto orientadas a la codificación (imaginería, mnemotecnia) podrían ser más apropiadas al **primer encuentro** con material nuevo.
5. **No descartar Mnemonics, Re-Reading e Interleaved Practice** solo por estar etiquetadas como "bajas": sus tamaños de efecto están muy cerca del umbral "moderado" y siguen siendo sustancialmente mayores que el promedio de la investigación educativa general (d=0.40).
6. **Underlining y Summarization, aun siendo las de menor efecto del grupo, siguen siendo lo bastante efectivas** para formar parte de la caja de herramientas de aprendizaje del estudiante — no deben eliminarse del repertorio.
7. **Distribuir el estudio en el tiempo (spaced, no massed):** revisar material previamente cubierto en unidades posteriores, programar evaluaciones regularmente en vez de solo al final (lo que fomenta el "cramming").
8. **Enseñar explícitamente a los estudiantes por qué el estudio espaciado es mejor**, dado que suelen percibir el estudio masivo como más efectivo aunque no lo sea (mostrarles evidencia/beneficios).

Recomendaciones prácticas citadas por Donoghue y Hattie desde el artículo complementario de Dunlosky et al. (2013b), que el propio meta-análisis respalda como consistentes con sus hallazgos:

- Dar un quiz de bajo riesgo (low-stakes) al inicio de cada clase, enfocado en el material más importante.
- Dar un examen acumulativo que anime a los estudiantes a re-estudiar el material más importante de forma distribuida.
- Animar a los estudiantes a desarrollar un "planificador de estudio" para distribuir su estudio a lo largo del curso y depender menos del "cramming".
- Fomentar el uso de práctica de recuperación (auto-test) en vez de re-lectura pasiva de libros/apuntes.
- Fomentar que los estudiantes elaboren sobre lo que leen, por ejemplo haciéndose preguntas de "¿por qué?".
- Mezclar problemas de clases anteriores para que los estudiantes practiquen identificar problemas y sus soluciones (interleaving).
- El subrayado está bien, pero solo en las etapas iniciales del proceso de aprendizaje de un tema.

Recomendaciones adicionales / agenda futura que plantean los propios autores:
- Desarrollar modelos más completos que sitúen estas 10 técnicas (y otras) según la demanda de la tarea, el momento de la intervención dentro del proceso de aprendizaje, y el rol del dominio de contenido.
- Investigar si estas técnicas pueden **enseñarse** explícitamente a profesores y estudiantes, y cómo (¿en el contexto de contenido específico? ¿puede la neurociencia educativa aportar aquí?).
- Prestar atención a la **motivación y las emociones** en la selección, persistencia y efectividad del uso de estas técnicas — es un factor "imperativo" para muchos estudiantes.
- Considerar que usar una "caja de herramientas" de técnicas probablemente sea óptimo, pero requiere que el estudiante tenga un nivel más alto de **autorregulación** para saber cuándo usar cada una.

## 7. Condiciones de contorno / limitaciones reconocidas por los autores

- **Limitación explícita señalada por los propios autores (sección "Limitation"):** ninguna publicación posterior a **2014** fue incluida en el meta-análisis, porque los datos provienen íntegramente de las referencias usadas en Dunlosky et al. (2013a). Los autores afirman no tener conocimiento de estudios más recientes que contradigan sus hallazgos, y sostienen que el estudio representa una revisión cuantitativa válida y comprensiva de la investigación publicada entre 1929 y 2014, complementaria a la revisión cualitativa de Dunlosky et al.
- **Sesgo hacia aprendizaje superficial:** la gran mayoría de los estudios subyacentes mide **aprendizaje superficial/factual** (93% de los resultados), medido **casi inmediatamente** después de la intervención (74% dentro de 1 día), y midiendo casi exclusivamente **transferencia cercana**. Esto limita fuertemente la generalización de los hallazgos —tanto de la revisión de Dunlosky et al. como de este meta-análisis— a aprendizaje **profundo**, **transferencia lejana**, aprendizaje **no académico**, o aprendizaje que requiere **periodos de retención más largos**. Los autores explícitamente dicen que "el veredicto aún está pendiente" sobre la efectividad óptima de las técnicas en esas condiciones.
- Los autores matizan que esta limitación no es solo del cuerpo de investigación, sino posiblemente también un reflejo de las **aulas actuales**, "todavía dominadas por una preponderancia de aprendizaje superficial, profesores que hacen preguntas de bajo nivel exigiendo respuestas de contenido, y evaluaciones que privilegian el conocimiento superficial" — por lo que las 10 técnicas podrían seguir siendo óptimas para muchas aulas actuales tal como están, aunque no para objetivos de aprendizaje más profundos.
- **Submuestras muy pequeñas para nivel de habilidad extremo:** solo 6 estudios con estudiantes de habilidad Alta y 13 con habilidad Baja de los 242 totales — los resultados de ese moderador (efecto negativo en alta habilidad) deben tomarse con cautela por el tamaño muestral reducido.
- **Transferencia lejana con muy pocos efectos disponibles**, insuficientes para desagregar por técnica individual.
- La **heterogeneidad global fue muy alta** (I² = 84.87%), lo que indica que los tamaños de efecto varían sustancialmente entre estudios por razones sistemáticas (no solo azar) — de ahí la necesidad de interpretar cualquier "d promedio" por técnica con cautela y siempre en relación a sus moderadores.
- Los cortes "Alto/Moderado/Bajo" (tanto los originales de Dunlosky et al. como los recalculados aquí, >0.70 / 0.54–0.69 / <0.53) son señalados explícitamente por los propios autores como **arbitrarios**, no categóricos: varias técnicas están a muy poca distancia del corte contiguo.
- Nota de fidelidad de esta extracción: la conversión del PDF original a texto produjo **desalineaciones en algunas tablas** (particularmente la Tabla 2 de efectos por dominio de aprendizaje y la Tabla 4 de efectos por país, y posiblemente el número de casos por técnica en la Tabla 1, así como un valor de SE negativo imposible en el apartado de transferencia cercana/lejana). Donde la cifra era ambigua o inconsistente en el propio texto extraído, se marcó explícitamente en este documento en vez de inventar un valor; los datos de la Tabla 1 (d, SEM, I², N único), Tabla 3 (nivel educativo) y los moderadores narrados en el texto corrido (año, habilidad, demora, factor de impacto, dominio general, profundidad, transferencia, país agregado) sí se consideran fiables.

## 8. Referencias clave citadas dentro del paper (para contexto)

- Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., y Willingham, D. T. (2013a). *Improving students' learning with effective learning techniques: promising directions from cognitive and educational psychology.* Psychological Science in the Public Interest, 14(1), 4–58. — Fuente original de la clasificación cualitativa de las 10 técnicas y de las 399 referencias usadas en este meta-análisis.
- Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., y Willingham, D. T. (2013b). *What works, what doesn't.* Scientific American Mind, 24(4), 46–53. — Artículo complementario más accesible para docentes, fuente de las recomendaciones prácticas citadas en la Introducción.
- Cepeda, N. J., Vul, E., Rohrer, D., Wixted, J. T., y Pashler, H. (2008). *Spacing effects in learning: a temporal ridgeline of optimal retention.* Psychological Science, 19(11), 1095–1102.
- Rowland, C. A. (2014). *The effect of testing versus restudy on retention: a meta-analytic review of the testing effect.* Psychological Bulletin, 140(6), 1432. (61 estudios, d=0.50 a favor de testing sobre restudy)
- Carvalho, P. F., y Goldstone, R. L. (2015). *The benefits of interleaved and blocked study: different tasks benefit from different schedules of study.* Psychonomic Bulletin & Review, 22(1), 281–288.
- Hattie, J. A., y Donoghue, G. M. (2016). *Learning techniques: a synthesis and conceptual model.* npj Science of Learning, 1, 16013. — Origen del modelo "skill, will and thrill" mencionado como agenda futura.
- Dunlosky, J., y Rawson, K. A. (2015). *Practice tests, spaced practice, and successive relearning: tips for classroom use and for guiding students' learning.* Scholarship of Teaching and Learning in Psychology, 1(1), 72.

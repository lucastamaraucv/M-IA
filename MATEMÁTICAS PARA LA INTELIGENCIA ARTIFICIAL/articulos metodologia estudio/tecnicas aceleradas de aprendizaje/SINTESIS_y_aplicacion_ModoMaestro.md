# Técnicas aceleradas de aprendizaje: síntesis y aplicación a Modo Maestro

Este documento consolida el conocimiento extraído de los 4 papers de la carpeta
(ver `extraccion_*.md` para el detalle completo de cada uno) y lo contrasta
con la implementación real de los 5 Modos Maestro + Repaso mezclado del
proyecto Visual Código, para responder: **¿esta metodología nos sirve, y qué
falta?**

Fuentes:
1. Karpicke (2012) — *Retrieval-Based Learning: Active Retrieval Promotes Meaningful Learning*, CDPS.
2. Karpicke (2017) — *Retrieval-Based Learning: A Decade of Progress*, capítulo de revisión.
3. Donoghue & Hattie (2021) — *A Meta-Analysis of Ten Learning Techniques*, Frontiers in Education.
4. Agarwal, Nunes & Blunt (2021) — *Retrieval Practice Consistently Benefits Student Learning*, revisión sistemática aplicada a aulas reales.

---

## 1. Conocimiento consolidado

### 1.1 La idea central (Karpicke 2012/2017)
Recuperar información de la memoria (sin releer, sin feedback) **no es solo
medir lo aprendido — es el proceso que produce el aprendizaje**. Recuperar
una vez duplica la retención a 1 semana frente a solo leer (15%→34%); la
recuperación repetida y espaciada la multiplica por ~4 (→80%). Supera incluso
a técnicas de estudio activo popares como mapas conceptuales, tanto en
preguntas literales como de inferencia. Paradoja: los estudiantes predicen
justo lo contrario (creen que releer/elaborar enseña más) y por eso casi
nunca eligen recuperar espontáneamente — de ahí la necesidad de que la
*instrucción* lo imponga (cuestionarios, quizzes), no que dependa de la
elección del alumno.

### 1.2 Tamaños de efecto reales (Donoghue & Hattie 2021, meta-análisis de las 10 técnicas de Dunlosky)
| Técnica | d (Cohen) | Soporte |
|---|---|---|
| **Distributed/Spaced Practice** | **0.85** | Alto |
| **Practice Testing** (retrieval practice) | **0.74** | Alto |
| Elaborative Interrogation | 0.56 | Moderado |
| Imagery | 0.56 | Moderado |
| Self-Explanation | 0.54 | Moderado |
| Keyword Mnemonic | 0.50 | Bajo |
| Re-Reading | 0.47 | Bajo |
| Interleaved Practice | 0.47 | Bajo (rozando moderado) |
| Underlining | 0.44 | Bajo |
| Summarization | 0.44 | Bajo |

Referencia: el promedio general de la investigación educativa es d=0.40
(Hattie), así que **hasta la técnica "peor" de esta lista está por encima de
la media**. Las dos ganadoras claras — espaciado y práctica de recuperación —
son exactamente las dos que ya están en el núcleo de Modo Maestro.

Matiz importante: los efectos son mucho mayores para aprendizaje
**superficial** (d=0.60) que **profundo** (d=0.26), y mayores en transferencia
**cercana** (d=0.61) que **lejana** (d=0.39). Ninguna de estas técnicas es
mágica para transferencia profunda por sí sola.

### 1.3 El moderador crítico: el feedback
"La ventaja de practice testing **con** feedback sobre restudiar es
extremadamente robusta"; sin feedback, el estudiante puede aprender sus
propios errores con alta confianza. En el estudio de aulas reales (Agarwal
et al. 2021), los experimentos **sin** feedback mostraron mayoritariamente
efectos pequeños o muy pequeños; con feedback inmediato, la distribución se
repartió entre pequeño/mediano/grande.

### 1.4 El balance éxito/esfuerzo (Karpicke 2017)
Menos pistas / mayor dificultad de recuperación → mayor aprendizaje, **pero
solo si el éxito inicial se mantiene por encima de ~75%**. Por debajo de eso
el efecto se debilita (y con opción múltiple, un éxito inicial bajo aumenta
el riesgo de aprender los distractores). La caja de Leitner que sube/baja
según acierto es, de hecho, un mecanismo natural para mantenerse cerca de
ese punto óptimo por ítem.

### 1.5 Espaciado: expansivo vs. igual — mito desmentido
Durante 40 años se recomendó el espaciado *expansivo* (intervalos crecientes:
0-1-5-9...) como superior. La década de evidencia revisada por Karpicke
(2017) **no lo confirma**: espaciado igual (5-5-5-5) rinde igual o mejor que
expansivo cuando se iguala el espaciado total; en algún estudio el
*contractivo* incluso ganó. Lo único que importa con solidez es que **haya
espaciado** (vs. masificado), no su forma.

### 1.6 Hallazgos de aula real que difieren del laboratorio (Agarwal et al. 2021)
Esta es la revisión más relevante para nosotros porque filtró específicamente
estudios en aulas reales, presenciales, con materiales del curso real:
- **57% de los efectos fueron medianos o grandes**; solo 6% negativos.
- **No importa la frecuencia exacta** (sesión única, semanal, cada 2-3
  semanas todas funcionan) → "los docentes deberían implementar la práctica
  de recuperación con menos preocupación por el formato o momento preciso".
- **No hace falta que cuente para la nota** — quizzes de bajo riesgo
  funcionan igual.
- **El formato de práctica debería coincidir con el del examen final**
  (opción múltiple↔opción múltiple, respuesta corta↔respuesta corta) —
  cuando no coinciden, el efecto es menor (transfer-appropriate processing).
- **Preguntas reformuladas en el examen final** producen efectos más
  pequeños que preguntas literales — la transferencia sigue siendo difícil.
- **A diferencia del laboratorio**: en aula real, demoras **cortas** (1-3
  días) antes del examen produjeron efectos **mayores** que demoras largas
  (fin de semestre) — lo opuesto de lo que predice la teoría de laboratorio.
- La práctica de recuperación frecuente **reduce la ansiedad ante exámenes**
  (92% de 1408 estudiantes la valoró positivamente; 72% dijo sentirse menos
  nervioso).

### 1.7 El modelo de fases (Donoghue & Hattie, retomando Hattie & Donoghue 2016)
Las técnicas no son intercambiables: rinden distinto según la **fase de
aprendizaje** — superficial → profundo → transferencia — y según si el
objetivo es **adquirir** conocimiento nuevo o **consolidar** lo ya adquirido.
Ejemplo textual del paper: practice testing es muy efectivo para
*consolidar* conocimiento superficial, pero inútil si ese conocimiento
superficial no se ha *adquirido* primero. Las técnicas de bajo efecto
orientadas a codificación (imaginería, mnemotecnia, elaboración) encajan
mejor en el primer encuentro con material nuevo; las de alto efecto
orientadas a práctica (testing, espaciado) encajan mejor después, para
consolidar.

---

## 2. ¿Esta metodología ayuda a nuestras sesiones de Modo Maestro?

**Sí, y en una proporción inusualmente alta ya está implementada.** El
sistema actual (Leitner en `core.js`/`review.js`) no es una intuición de
diseño aislada: es, en varios puntos, una implementación casi de libro de
texto de las dos técnicas con más evidencia (d=0.85 y d=0.74 respectivamente,
las dos "Alto soporte" de Dunlosky/Donoghue & Hattie).

### 2.1 Lo que ya está bien alineado con la evidencia

| Mecanismo actual | Técnica de la literatura | Evidencia |
|---|---|---|
| Cajas Leitner con intervalos 1-3-7-14-30 días, prioridad a vencidos | **Distributed Practice** (d=0.85, la técnica #1) | Espaciado real, no masificado — el único requisito que la evidencia confirma con solidez |
| Intervalos **fijos** (no expansivos) | Coincide con el hallazgo de Karpicke (2017): expansivo no es mejor que igual | No hace falta "arreglar" esto — ya está en la forma que la evidencia respalda |
| Pregunta tipo quiz para repasar cada tema | **Practice Testing** (d=0.74, la técnica #2) | El propio acto de recuperar, no solo releer la teoría |
| Feedback inmediato tras cada respuesta (`math-feedback-ok`/`bad`) | El moderador más determinante de Practice Testing | "Sin feedback, la mayoría de los efectos observados en aula fueron pequeños o muy pequeños" |
| Reintento sin revelar la respuesta correcta (`math-option-wrong`, no revela cuál era) | Evita que el reintento sea "elegir por descarte" en vez de recuperación genuina; evita aprender el distractor con alta confianza | Butler & Roediger (2008): dar feedback reduce a la mitad la intrusión de distractores |
| Caja baja tras fallo → vuelve antes | Aproxima el balance éxito/esfuerzo (los ítems débiles se recuperan más seguido, con más esfuerzo relativo) | "La recuperación esforzada de ítems débiles produce mayores ganancias" |
| Quizzes no calificados, de bajo riesgo | Coincide con Agarwal et al. (2021): no hace falta que cuente para la nota | Funciona igual bajo condiciones motivacionales reales de aula |
| `aoclassify`/`aocompare`: interleaving por familia de técnica, mezclando 4 orígenes en Repaso mezclado | **Interleaved Practice** (d=0.47, roza "moderado"; Donoghue & Hattie dicen explícitamente que no debe descartarse por estar "bajo") | El mecanismo (Carvalho & Goldstone 2015) es exactamente "detectar qué distingue una categoría de otra cuando alternan" — es literalmente lo que hace aoclassify |
| Paneles de "📖 Teoría" con analogías simples antes del quiz | Fase de **adquisición/codificación** antes de la fase de **consolidación** (practice testing) | Coincide con el modelo de fases de Hattie & Donoghue: elaboración primero, práctica de recuperación después |
| Repaso mezclado prioriza vencidos, no aleatorio puro | Espaciado real por ítem, no solo repetición ciega | — |

Este nivel de coincidencia no es casual: el diseño de Leitner + due-based +
feedback inmediato + interleaving ya *es*, en esencia, la aplicación directa
de las dos técnicas más respaldadas por la evidencia, más una tercera de
soporte moderado bien elegida.

### 2.2 Brechas reales frente a la evidencia (oportunidades concretas)

1. **Coincidencia de formato práctica↔examen final.** Todo Modo Maestro es
   opción múltiple. Si los exámenes reales de la carrera del usuario son de
   desarrollo/respuesta abierta (muy probable en RA, AS, matemáticas), el
   hallazgo de Agarwal et al. (2021) dice que el beneficio es menor cuando el
   formato de práctica no coincide con el del examen real. No hace falta
   construir corrección de texto libre — un cambio barato y de alto valor:
   antes de mostrar las opciones, pedir al alumno que **piense/escriba
   brevemente su respuesta** (aunque no se corrija automáticamente) antes de
   revelar las opciones de la pregunta. Esto acerca el formato al de
   recuerdo libre sin rehacer el motor de preguntas.

2. **No se explota la ventaja de "preguntas reformuladas" para medir
   transferencia real.** Agarwal et al. encontraron que las preguntas
   reformuladas (no literales) en el examen final dieron efectos más chicos
   — es decir, la transferencia es el punto débil general del campo, y
   conviene medirla a propósito. El sistema de `q.steps`/`q.stakes` ya
   presente en NS/RN/RF/AS podría extenderse (según la nota de memoria del
   proyecto, ya existe infraestructura de 2ª pregunta por tema sin usar en
   NS/RN/RF) para incluir deliberadamente una variante reformulada del mismo
   concepto, no solo una pregunta distinta.

3. **El panel "Teoría" es contenido leído, no autogenerado — no es
   Elaborative Interrogation ni Self-Explanation en sentido estricto.**
   Ambas técnicas (d=0.54-0.56, soporte moderado) requieren que el propio
   alumno genere la explicación (o al menos una pregunta "¿por qué es
   cierto esto?"), no solo que la lea. El campo `theory` actual da la
   analogía ya hecha. Una mejora barata: tras la teoría, una pregunta
   reflexiva tipo "¿por qué crees que...?" (aunque sea de auto-reporte, sin
   corrección automática) antes de pasar al quiz — coincide con lo que las
   notas del alumno en SQLite (Autoexplícate) ya hacen parcialmente para
   AO/RA/AS; vale la pena revisar si puede generalizarse.

4. **Ningún onboarding explica *por qué* el sistema funciona así.**
   Donoghue & Hattie recomiendan explícitamente "enseñar a los estudiantes
   por qué el espaciado es mejor", porque los propios estudiantes lo
   subestiman metacognitivamente (Karpicke 2012: predicen justo lo
   contrario de lo que funciona). Un mensaje breve de una sola vez ("por qué
   el repaso vencido funciona mejor que repasar todo siempre") podría
   aumentar la adherencia al Repaso mezclado sin cambiar ninguna mecánica.

5. **La demora antes del "examen final" real es larga (fin de cuatrimestre),
   no corta.** El hallazgo de Agarwal et al. de que en aula real las demoras
   *cortas* (1-3 días) dan mejores resultados que las largas es contrario a
   la intuición de laboratorio y **relevante aquí**: si el usuario deja de
   repasar un tema mucho antes del examen real, el beneficio relativo cae.
   Esto refuerza (no cambia) el diseño actual de repaso *continuo* basado en
   `due`, en vez de depender de una sola tanda de estudio temprana — es un
   argumento a favor de seguir insistiendo en el uso regular del Repaso
   mezclado cerca de la fecha de examen, no solo durante el curso.

6. **Ninguna técnica de "bajo pero no despreciable" soporte está en uso
   deliberado**: mnemotecnia (d=0.50) e imaginería (d=0.56) no aparecen en
   ningún Modo Maestro. Para temas muy abstractos (RA/RN/lógica difusa) esto
   podría ser útil como complemento puntual — pero no es prioritario, ya que
   Donoghue & Hattie sitúan su efecto muy por debajo de espaciado/testing.

### 2.3 Conclusión

La arquitectura de Modo Maestro ya implementa, de forma bastante fiel, las
dos técnicas de aprendizaje con mayor respaldo empírico del campo
(espaciado + práctica de recuperación con feedback), más interleaving bien
diseñado. No hace falta rehacer nada estructural. Las mejoras de mayor
retorno, en orden de esfuerzo/beneficio, serían: (1) un paso de "piensa tu
respuesta antes de ver las opciones" para acercarse al formato de recuerdo
libre, (2) una explicación breve al alumno de por qué el sistema funciona
así (para aumentar la adherencia), y (3) usar la infraestructura de
2ª-pregunta-por-tema ya existente para incluir variantes reformuladas que
midan transferencia, no solo repetición literal.

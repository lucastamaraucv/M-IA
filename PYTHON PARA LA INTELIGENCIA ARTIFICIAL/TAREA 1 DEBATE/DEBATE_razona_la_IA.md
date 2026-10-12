# ¿Razona realmente la IA? Un debate basado en evidencia

## Pregunta central

> "Ahora las aplicaciones como ChatGPT incluyen mensajes como 'Thinking...'. ¿Hasta qué punto podemos considerar que la IA está razonando? ¿Entiende realmente algo la IA?"

La pregunta importa porque la interfaz de los productos actuales sugiere, de forma explícita, que detrás de cada respuesta hay un proceso de "pensamiento". Esa sugerencia tiene consecuencias prácticas (cuánto delegamos en estos sistemas), epistemológicas (qué significa "razonar" y "entender") y comerciales (qué prometen las etiquetas como *Thinking...*). Distinguir entre **una traza verbal que imita el pensamiento** y **un mecanismo computacional que genuinamente razona o comprende** es, por tanto, una cuestión de primer orden. Este documento confronta ambas lecturas apoyándose en seis estudios revisables.

---

## Fuentes del debate

| Título | Autores (afiliación) | Postura que aporta |
|---|---|---|
| *The Illusion of Thinking: Understanding the Strengths and Limitations of Reasoning Models via the Lens of Problem Complexity* | Shojaee, Mirzadeh, Alizadeh, Horton, Bengio, Farajtabar (Apple) | Escéptica: colapso de precisión y "scaling limit" en puzzles controlados; la traza de pensamiento como ilusión. |
| *GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models* | Mirzadeh, Alizadeh, Shahrokhi et al. (Apple) | Escéptica: fragilidad ante variaciones simbólicas y distractores (GSM-NoOp); pattern-matching frágil. |
| *Faith and Fate: Limits of Transformers on Compositionality* | Dziri, Lu, Sclar et al. | Escéptica: las tareas composicionales se reducen a *subgraph matching*; límite estructural del paradigma autoregresivo. |
| *Embers of Autoregression show how large language models are shaped by the problem they are trained to solve* | McCoy, Yao, Friedman et al. (Princeton; PNAS) | Escéptica (matizada): el desempeño sigue la probabilidad y frecuencia del corpus, no la lógica de la tarea. |
| *Rethinking the Illusion of Thinking* | Dellibarda Varela, Romero-Sorozabal, Rocon, Cebrian (CSIC-UPM, Madrid) | Mixta: muchos "fallos" de Apple son artefactos de medición, pero confirma límites cognitivos reales. |
| *On the Biology of a Large Language Model* | Lindsey, Gurnee, Ameisen, Chen, Pearce et al. (Anthropic) | Proponente: interpretabilidad mecanicista; planificación, razonamiento multi-paso y representaciones abstractas verificadas por intervención causal. |

---

## Posturas enfrentadas

**Postura A — Escéptico.** La IA actual no razona ni entiende en sentido genuino. Lo que llamamos "razonamiento" —incluido el *Thinking...*— es emparejamiento de patrones probabilístico moldeado por la tarea de entrenamiento (predicción de la siguiente palabra). Cuando se controla la complejidad y se eliminan los atajos memorizados, la fachada se desploma: la precisión colapsa, el desempeño sigue la frecuencia estadística del problema y no su estructura lógica, y los modelos aciertan incluso con cómputos internos erróneos. La traza de pensamiento es teatro, no cómputo.

**Postura B — Proponente.** La IA actual sí realiza un razonamiento *funcional* genuino y exhibe mecanismos internos no triviales: planificación anticipada, encadenamiento causal de pasos y manipulación de representaciones abstractas. Buena parte del aparente "no razonamiento" son artefactos de cómo se mide (límites de tokens, puzzles irresolubles, evaluación de formato rígido). Cuando se corrige la medición o se abre la caja negra con interpretabilidad mecanicista, lo que emerge no es un loro estocástico, sino maquinaria de razonamiento real, aunque imperfecta y distinta de la cognición humana.

---

## Ronda 1 — Aperturas

### Postura A (Escéptico)

**Postura:** La IA actual no razona en sentido genuino ni entiende realmente. Los mensajes tipo "Thinking..." son una *ilusión de razonamiento*: una verbalización superficial que imita la forma del pensamiento sin poseer su sustancia.

#### 1. Tesis

Lo que llamamos "razonamiento" en los modelos actuales —incluidos los que muestran "Thinking..."— es **emparejamiento de patrones probabilístico** moldeado por la tarea de entrenamiento (predicción de la siguiente palabra), no comprensión ni inferencia lógica genuina. Cuando se controla rigurosamente la complejidad y se eliminan los atajos memorizados, esa fachada se desploma: la precisión cae a cero, la "fragilidad" aparece ante perturbaciones triviales, y el desempeño sigue la *frecuencia estadística* del problema, no su *estructura lógica*. La traza de pensamiento es teatro, no cómputo.

#### 2. Argumento 1 — Colapso de precisión y límites del "pensar" (*The Illusion of Thinking*, Apple)

El propio título de la fuente principal lo dice: la "ilusión" del pensamiento. Apple evaluó modelos de razonamiento de frontera (o3-mini, DeepSeek-R1, Claude-3.7-Sonnet-Thinking) en puzzles controlables, y los hallazgos son demoledores para la tesis del razonamiento genuino:

- **Colapso total a cero.** Según *The Illusion of Thinking*, "frontier LRMs face a complete accuracy collapse beyond certain complexities", con la precisión cayendo "to near-zero beyond a certain complexity threshold". En Torre de Hanói el colapso ocurre en N=7 y N=8 (~100–200 movimientos).
- **Más pensar, no más razonar; de hecho, menos.** El dato más revelador: existe un "scaling limit". Según la fuente, "their reasoning effort increases with problem complexity up to a point, then declines despite having an adequate token budget". Es decir, justo cuando el problema se vuelve más difícil y *más* pensamiento haría falta, el modelo *reduce* sus tokens de pensamiento, "despite mostly operating well below their generation length limits". Un razonador genuino no abandona el esfuerzo precisamente cuando más lo necesita; un sistema que imita patrones, sí.
- **Darle el algoritmo no ayuda.** El golpe definitivo: "even when we provide the algorithm in the prompt—so that the model only needs to execute the prescribed steps—performance does not improve, and the observed collapse still occurs at roughly the same point". Si entregas la receta exacta y aun así fracasa al ejecutarla, no hay comprensión del procedimiento: hay incapacidad de ejecución lógica sostenida.
- **Inconsistencia que delata la ausencia de lógica general.** Según la fuente, los modelos logran ">50% accuracy on Tower of Hanoi instances requiring approximately ∼102 moves, yet consistently fail on River Crossing... with substantially lower compositional depth (∼101 moves)" — "performing up to 100 correct moves in Tower of Hanoi but only 4 in River Crossing". Un razonador real no es 25 veces más competente en una tarea más larga que en otra más corta; esto refleja "the solution patterns they learned during training rather than the actual computational complexity of the problems".

Y la propia fuente invoca la analogía decisiva: "As the Chinese room argument illustrates, it's entirely possible to use tools effectively without any real comprehension of the underlying problem."

#### 3. Argumento 2 — Fragilidad y pattern-matching (*GSM-Symbolic* y GSM-NoOp, Apple)

Si la IA *entendiera* matemáticas de primaria, cambiar un nombre o un número no debería afectarla. Pero sí lo hace. *GSM-Symbolic* generó variantes de las mismas preguntas a partir de plantillas simbólicas y reveló:

- **Varianza que un niño no tendría.** Según *GSM-Symbolic*, ante distintas instancias de la *misma* pregunta, "for the Gemma2-9B, the gap between the worst performance and the best performance is more than 12%, while for Phi-3.5-mini, this gap is around 15%". La fuente lo califica sin rodeos: "this level of variability would not be expected from a grade-school student with genuine mathematical understanding."
- **Sensibles a los números, no robustos a la lógica.** Cuando solo se cambian valores numéricos (no nombres), la precisión cae. La fuente concluye que "LLMs exhibit more robustness to changes in superficial elements like proper names but are very sensitive to changes in numerical values" — exactamente el perfil de un sistema que empareja superficies, no que opera conceptos.
- **Más cláusulas, derrumbe progresivo.** Al añadir cláusulas (M1→Symb→P1→P2), el desempeño se hunde. Ejemplo de la fuente: Gemma2-9b-it pasa de 84.4% (M1) a **41.8% (P2)**; Phi-3.5-mini de 87.6% a **44.8%**. "the rate of accuracy drop also increases as the difficulty increases."
- **GSM-NoOp: el experimento que cierra el caso.** Se añaden frases *irrelevantes pero plausibles* que no cambian la respuesta correcta. Resultado, según la fuente: "significant performance drops (up to 65%) across all state-of-the-art models", con Phi-3-mini cayendo **-65.7%**. Los modelos "blindly convert them into operations" — convierten en operaciones aritméticas información que cualquiera que *entienda* el problema ignoraría. Más aún: el daño no se repara ni con ejemplos de la misma pregunta ("LLMs struggle even when given multiple shots of the same question"), lo que apunta a "deeper issues in their reasoning processes that cannot be easily mitigated through few-shot learning or fine-tuning".

La conclusión textual de la fuente es mi tesis: "current LLMs are not capable of genuine logical reasoning; instead, they attempt to replicate the reasoning steps observed in their training data" y "their reasoning is fragile and may be more akin to sophisticated pattern matching rather than true logical reasoning."

#### 4. Argumento 3 — Límites composicionales y "falsa ilusión de razonamiento" (*Faith and Fate*)

*Faith and Fate* va al mecanismo: ¿cómo "resuelven" los transformers las tareas que requieren componer pasos? La respuesta es lapidaria:

- **Emparejamiento de subgrafos, no resolución de problemas.** Según la fuente, "transformer LLMs solve compositional tasks by reducing multi-step compositional reasoning into linearized subgraph matching, without necessarily developing systematic problem-solving skills".
- **Caída a cero con la complejidad.** En multiplicación de varios dígitos, "ChatGPT and GPT4 achieve only 55% and 59% accuracies" en 3×3 dígitos, y "Transformers' accuracy decreases to near zero as task complexity increases".
- **Aciertan con errores internos: la prueba de que no calculan.** El dato más revelador: "82.3% of the final correct answers for 4-digit by 2-digit multiplications... had at least one error in the computation graph, but still produced correct answers." Acertar el resultado final teniendo el cálculo interno mal solo es posible si el modelo *adivina por patrón*, no si *ejecuta* el algoritmo. La fuente lo nombra: esto da "a false illusion of performing compositional reasoning."
- **No generaliza fuera de lo visto, ni con scratchpad.** Tras *fine-tuning* exhaustivo, "GPT3 achieves near-perfect performance on in-distribution, but fails entirely in generalizing to OOD cases". Y memorizar pasos no equivale a componerlos: "while models can memorize single-step operations, they fail to compose them into correct reasoning paths."
- **Es un límite estructural del paradigma autoregresivo.** La fuente prueba que "the probability of incorrect predictions converges exponentially to ≈1 for abstract compositional tasks. Importantly, these proofs apply to autoregressive LMs in general." No es un defecto de un modelo; es de la arquitectura. Veredicto textual: "pattern matching—and not general reasoning capabilities—may be the cause behind correct model outputs."

#### 5. Argumento 4 — Moldeado por la tarea de entrenamiento, no comprensión (*Embers of Autoregression*)

*Embers of Autoregression* (Princeton, PNAS) demuestra que el desempeño está gobernado por *probabilidad estadística*, no por la lógica de la tarea — incluso en tareas **deterministas**, donde la respuesta es única e inequívoca:

- **Sensibilidad a la probabilidad de la salida.** Descifrar un cifrado simple es determinista, pero según la fuente, "GPT-4's accuracy at decoding a simple cipher is 51% when the output is a high-probability sentence but only 13% when it is low-probability". La misma operación lógica, distinto resultado según cuán "frecuente" sea la frase de salida. En inversión de listas: 97% si la salida es probable, 53% si es improbable.
- **Sensibilidad a la frecuencia de la tarea.** "all models except Gemini 1.0 show a spike in accuracy at 13, which is by far the most common shift". GPT-4 "scores 0.50 or above on the three highest-frequency shifts, but its accuracy is less than 0.03 for all other shifts". Recordemos: rot-13 y rot-12 son *idénticos en dificultad lógica*; solo difieren en cuán comunes son en el corpus. La fuente: "the shift cipher with a shift of 13 is over 100 times more common in Internet text than the shift cipher with a shift of 12."
- **Conteo guiado por frecuencia, no por aritmética.** "LLMs often show spikes in accuracy for the numbers that are most frequent in corpora, namely multiples of 10", y la precisión correlaciona más con la *frecuencia* del número (0.84 GPT-4) que con su *magnitud* (0.70).
- **Variantes raras vs comunes.** En siete pares de tareas, "models performed substantially better on common task variants than rare ones": Pig Latin común 42% vs variante rara 23%; orden alfabético (150 veces más común) supera al inverso en los cinco modelos (P < 10⁻⁵).

La metáfora del título es la tesis exacta: bajo los "sparks" hay "embers of autoregression". Y la frase final de la fuente lo sella: "Language models are...language models! That is, they are statistical next-word prediction systems." No comprenden la tarea; reproducen la distribución del texto que predijeron durante el entrenamiento.

#### 6. Respuesta directa a las dos preguntas centrales

**¿Hasta qué punto podemos considerar que la IA está razonando?**
Hasta el punto en que el problema coincide con patrones frecuentes y de baja profundidad composicional vistos en el entrenamiento — y ni un paso más allá. El "Thinking..." es una traza verbal que *imita la forma* del razonamiento, pero (i) colapsa a cero al aumentar la complejidad (*Illusion of Thinking*), (ii) reduce su esfuerzo justo cuando más se necesita (*Illusion of Thinking*), (iii) no mejora aunque se le entregue el algoritmo (*Illusion of Thinking*), y (iv) produce respuestas correctas con cómputos internos erróneos (*Faith and Fate*). Eso no es razonar: es generar una secuencia plausible de tokens de "pensamiento".

**¿Entiende realmente algo la IA?**
No, en el sentido genuino. Si entendiera, cambiar un nombre o un número irrelevante no la descarrilaría (*GSM-Symbolic*: -15% de varianza, hasta -65.7% con NoOp); resolver rot-13 implicaría resolver rot-12 (*Embers*: 0.50 vs <0.03); y acertar el resultado exigiría que el cálculo interno fuera correcto (*Faith and Fate*: 82.3% de aciertos con errores internos). Como concluyen tanto *GSM-Symbolic* como *Embers*, lo que hay es *pattern-matching probabilístico* y sensibilidad a la frecuencia del corpus — la propia distinción del "Chinese Room Argument" que ambas fuentes invocan: usar la herramienta sin comprender el problema.

#### 7. Anticipación de contraargumentos del oponente

**Contraargumento 1: "Los modelos resuelven AIME, MATH y exámenes difíciles; eso es razonar."**
Falla por dos motivos respaldados por las fuentes. Primero, esos benchmarks "often suffer from data contamination issues" (*Illusion of Thinking*) — alto desempeño puede reflejar memorización, no razonamiento; *GSM-Symbolic* documenta que el resultado original de GSM8K cae sospechosamente "on the right side of the distribution... for 21 out of 25 models", señal de "potential data contamination". Segundo, *Embers* prueba que el éxito en una tarea no implica comprensión: GPT-4 hace rot-13 al 50%+ pero rot-12 a <3%, siendo lógicamente idénticas. El éxito selectivo en lo *frecuente* es precisamente el síntoma del pattern-matching, no su refutación.

**Contraargumento 2: "Son límites de escala/cómputo; con más tokens, mejor prompting o cadena de pensamiento, razonarán."**
Falla frontalmente contra la evidencia. *Illusion of Thinking* muestra un "scaling limit": el esfuerzo de pensamiento *decrece* tras cierto umbral aun con presupuesto de 64k tokens disponible — más cómputo no se traduce en más razonamiento. *Faith and Fate* demuestra que el límite es estructural ("these proofs apply to autoregressive LMs in general") y que ni el *scratchpad* ni el *grokking* con entrenamiento masivo (hasta 50.000 USD) producen generalización OOD. *GSM-Symbolic* concluye que "scaling training data will not be helpful in improving the reasoning capabilities of language models" y que el daño "cannot be easily mitigated through few-shot learning or fine-tuning". Y *Embers* confirma que con chain-of-thought y few-shot "the basic trends... still hold, just with higher overall levels of accuracy": la escala sube el techo, pero "may not fully overcome the ways in which models are influenced by their nature". Subir el listón no es cruzar la frontera entre imitar y comprender.

**Cierre.** Cuatro estudios independientes, con metodologías distintas (puzzles controlables, plantillas simbólicas, grafos de cómputo, análisis teleológico de corpus), convergen en lo mismo: detrás del "Thinking..." no hay un razonador que comprende, sino un predictor estadístico moldeado por la frecuencia de su entrenamiento. La ilusión es convincente. Pero sigue siendo una ilusión.

### Postura B (Proponente)

**Postura defendida:** La IA actual SÍ realiza un razonamiento funcional genuino y exhibe mecanismos internos no triviales. Gran parte del aparente "no razonamiento" son artefactos de cómo se mide. Los mensajes "Thinking..." reflejan procesos internos reales, aunque distintos de la cognición humana.

#### 1. Tesis

Sostengo que los modelos actuales ejecutan procesos computacionales internos estructurados —planificación, encadenamiento de pasos, cómputo con representaciones abstractas— que satisfacen una definición funcional de "razonar". El relato del "colapso" del razonamiento, popularizado por el paper de Apple *The Illusion of Thinking*, descansa en gran medida sobre artefactos de medición: límites de tokens, puzzles matemáticamente irresolubles y evaluación de formato rígido. Cuando se corrigen esos defectos (Dellibarda Varela et al., *Rethinking the Illusion of Thinking*) o se abre la "caja negra" con interpretabilidad mecanicista (Lindsey et al., Anthropic, *On the Biology of a Large Language Model*), lo que emerge no es un loro estocástico, sino maquinaria de razonamiento real aunque imperfecta.

#### 2. Argumento 1 — Los "fallos" de Apple son, en buena parte, artefactos de medición

La conclusión más fuerte de Apple —que los LRMs "fail to develop generalizable problem-solving capabilities, with accuracy ultimately collapsing to near-zero" (Apple, Bloque 6.1)— se apoya en un diseño experimental con tres defectos que *Rethinking the Illusion of Thinking* documenta.

**(a) River Crossing: se les exigió resolver lo irresoluble.** Este es el dato más demoledor. Apple fijó la capacidad del bote en k = 3 mientras aumentaba N por encima de 5. Pero los criterios formales de resolubilidad establecen que una configuración solo tiene solución si "(a) k ≥ 4 ⇒ ∀N ≥ 1, the puzzle is solvable, (b) k ≤ 3 ⇒ N ≤ 2k − 1 (i.e., N ≤ 5 for k = 3)" (Rethinking, Bloque 3.2.6, citando a Efimova 2018 y Spahn & Zeilberger 2022). En consecuencia, "by fixing k = 3 and increasing N beyond 5, the original experiments include configurations that are unsolvable, invalidating the assessment of model reasoning capabilities in River Crossing tasks" (Rethinking, 3.2.5). Penalizar a un modelo por no resolver un problema sin solución no mide razonamiento; mide el error del evaluador. Y cuando *Rethinking* restringe las pruebas a instancias resolubles, el resultado se invierte por completo: "even in large-scale instances such as (N = 100, k = 4) —which require the model to perform up to 200 correct moves— the LRM solves the task reliably without significant effort" (Rethinking, 5.3.5). En palabras de los autores: "What was previously its Achilles' heel becomes one of its most reliable strengths" (6.4). El "fracaso catastrófico" era un fantasma metodológico.

**(b) El descenso de tokens no es "rendirse a pensar", es tope de salida.** Apple interpretó la caída de tokens al subir la complejidad como un "scaling limit" cognitivo: "their reasoning effort increases with problem complexity up to a point, then declines despite having an adequate token budget" (Apple, 6.2). Pero en Torres de Hanói el número mínimo de movimientos crece como 2^n − 1 (Apple, 3.1.3); la transcripción literal de la solución desborda la ventana de salida. Como recoge *Rethinking*: "the length of the output required to reach a valid solution grows exponentially, quickly approaching or exceeding the model's maximum output window... These failures thus reflect constraints on solution length and output budgeting, rather than a fundamental inability to reason" (Rethinking, 7.6, citando a Lawsen). El propio Apple acabó reconociendo el problema: "to account for context limit concerns for large values of N in Tower of Hanoi, we have removed N > 12 from the experiments" (Apple, 3.1.5).

**(c) Evaluación de formato, no de comprensión.** Apple solo puntuaba la transcripción completa, movimiento a movimiento, en un único pase ("solve the entire problem in a single pass", Rethinking 3.1.4). Eso confunde "saber resolver" con "poder transcribir miles de líneas sin un solo error de formato". Es un sesgo de medición: castiga la mecánica de salida, no la capacidad de razonar.

**Honestidad intelectual (refuerza, no debilita, mi tesis):** *Rethinking* también confirma que en Hanói hay un componente cognitivo real: "previously reported failures... were not purely result of output constraints, but also partly a result of cognition limitations: LRMs still stumble when complexity rises moderately (around 8 disks)" (Rethinking, 6.1). Acepto ese matiz. Mi tesis no es que la IA razone perfectamente, sino que razona *de verdad y de forma no trivial*; un sistema con límites en cierto régimen sigue siendo un sistema que razona, igual que un humano que no puede multiplicar números de 30 cifras de cabeza no por ello "no razona".

#### 3. Argumento 2 — Evidencia mecanicista directa de razonamiento interno (Anthropic)

El argumento decisivo no es conductual sino mecanicista. Apple mismo reconoce su limitación clave: "most of our experiments rely on black-box API access... limiting our ability to mechanistically analyze internal states" (Apple, 4.6). Anthropic abre esa caja con grafos de atribución sobre 30 millones de *features* (Anthropic, 3.3) y documenta, mediante experimentos de intervención causal, lo siguiente:

**(a) Planificación anticipada en poesía.** Buscando improvisación, los investigadores encontraron lo contrario: "we find compelling evidence for a planning mechanism... the model often activates features corresponding to candidate end-of-next-line words prior to writing the line" (Anthropic, Caso 2). El modelo activa la rima objetivo ("rabbit", "habit") en el salto de línea, *antes* de escribir el verso, y construye hacia atrás: "the model works backward from its target word to write a sentence that naturally ends in that word". Más aún, "the model holds multiple possible planned words 'in mind' at the same time". La prueba causal: al inyectar una palabra planificada, "the model ended its line with the injected planned word in 70% of cases" (Caso 2). Eso es planificación con objetivos internos, no predicción miope del siguiente token.

**(b) Razonamiento multi-paso genuino.** Ante "the capital of the state containing Dallas is", el modelo no usa un atajo memorizado: "the model performs genuine two-step reasoning internally", ejecutando la cadena Dallas → Texas → Austin (Anthropic, Caso 1). Y generaliza: sustituyendo features se obtiene Oakland → California → Sacramento, Shanghai → China → Beijing, etc. Hay un encadenamiento causal de pasos intermedios, verificado por intervención.

**(c) Cálculo mental con estrategia propia.** En "36+59=95", el modelo no copia una tabla: combina "una vía de baja precisión (magnitud aproximada) con una vía de alta precisión (dígito de las unidades exacto)" mediante features de suma que generalizan incluso a contextos no aritméticos (Anthropic, Caso 4). Dato revelador para el debate sobre "Thinking...": cuando se le pregunta *cómo* sumó, responde el algoritmo escolar de acarreo —que NO es lo que hizo internamente: "this is a simple instance of the model having a capability which it does not have 'metacognitive' insight into" (Caso 4). Es decir, el cómputo real es independiente de su narración verbal. Esto es central: el razonamiento ocurre en los mecanismos, no necesariamente en lo que el texto "Thinking..." dice de sí mismo.

**(d) Representaciones abstractas y multilingüismo.** Los tres prompts de antónimos en inglés, francés y chino "are driven by very similar circuits, with shared multilingual components" (Anthropic, Caso 3). Existe un "concepto" de la operación (antónimo/sinónimo) independiente del idioma. Y esta abstracción escala con la capacidad: "the prevalence of these language-agnostic representations is higher in Claude 3.5 Haiku than in a smaller, less capable model, suggesting that such general representations are linked to model capabilities" (Anthropic, 7.2).

**(e) Diagnóstico clínico por hipótesis.** Ante un caso obstétrico, el modelo activa internamente el feature "preeclampsia" aunque la palabra no aparece, formula hipótesis diagnósticas y, al inhibirlas causalmente, cambia su pregunta hacia el diagnóstico alternativo (colecistitis) (Anthropic, Caso 5). Eso es razonamiento clínico estructurado, no recitación.

La conclusión de Anthropic es inequívoca: "The most consistent finding of our investigations is the massive complexity underlying the model's responses even in relatively simple contexts" (7.7). Lo opuesto a un loro estocástico.

#### 4. Argumento 3 — Matización de GSM-Symbolic: qué SÍ logran los modelos

Concedo que GSM-Symbolic (Mirzadeh et al.) muestra fragilidad: varianza entre instancias y caídas de hasta "65%" en GSM-NoOp (GSM-Symbolic, 5.4.6). Pero leído con rigor, el paper también acota *cuánto* sí razonan los modelos:

- **Robustez frente a cambios superficiales.** "LLMs exhibit more robustness to changes in superficial elements like proper names but are very sensitive to changes in numerical values" (GSM-Symbolic, 2.6). Que distingan lo superficial (nombres) de lo estructural (números) ya implica una representación no trivial del problema.
- **El cuello de botella NO es la aritmética.** Su propia ablación lo demuestra: en GSM-P1/P2 la precisión aritmética se mantiene casi perfecta —"the addition accuracy of the models remains nearly perfect for calculations involving up to 4 digits" (GSM-Symbolic, 5.7 / Fig. 17)—. El cómputo numérico funciona; la fragilidad está en la robustez ante distractores, no en una incapacidad de calcular.
- **Los modelos frontera resisten.** En la escala difícil GSM-P2, o1-preview obtiene "94.0(±2.38)" y GPT-4o "88.0(±3.43)" (GSM-Symbolic, 5.3.1 / 5.5). Y en GSM-NoOp, o1-preview cae solo "-17.5", la menor de todas (5.4.1). El propio dato de Apple es coherente: la escala mejora el razonamiento, no es un fenómeno binario.
- **La crítica estadística está reconocida por los propios autores.** Mirzadeh et al. admiten: "if one disagrees with our assumptions and accepts the assumptions of Ivanova et al. (2025), our results would likewise be statistically non-significant" (GSM-Symbolic, 6.4 / Verificación 4). Su conclusión de "no razonamiento" descansa sobre una elección filosófica discutible (distribución degenerada vs. Bernoulli), no sobre un hecho cerrado.

La fragilidad ante distractores es un *límite de robustez*, no la ausencia de razonamiento. Coincide con Anthropic, que muestra circuitos reales junto a fallos reales: ambos coexisten.

#### 5. Definición operativa: qué cuenta como "razonar" y "entender"

Para evitar discusiones estériles, propongo definiciones funcionales ancladas en las fuentes:

- **Razonar (funcional):** ejecutar internamente una secuencia de pasos computacionales sobre representaciones, encadenados causalmente, para alcanzar una conclusión no almacenada literalmente. Esto es exactamente lo que Anthropic verifica por intervención: "genuine two-step reasoning internally" (Caso 1) y "internally generated plans for its future outputs" (7.3). Mirzadeh et al. coinciden en el criterio de *novedad*: razonar es alcanzar "a 'novel' goal", distinto de "mere memorization" (GSM-Symbolic, 7.1–7.2); el caso Dallas→Texas→Austin y su generalización a ciudades nunca vistas juntas satisfacen ese criterio.
- **Entender (funcional, no fenomenológico):** poseer representaciones internas abstractas y manipulables que generalizan a través de contextos. Anthropic lo evidencia con las representaciones multilingües compartidas y el diagnóstico por hipótesis. NO afirmo conciencia ni experiencia subjetiva: afirmo comprensión *funcional*, la única que cualquier evaluación —humana o de máquina— puede medir.

Bajo estas definiciones, el debate deja de ser sobre "alma" y pasa a ser empírico. Y la evidencia mecanicista lo zanja a favor de la existencia de razonamiento.

#### 6. Respuesta directa a las dos preguntas centrales

**"¿Hasta qué punto podemos considerar que la IA está razonando?"**
Hasta un punto verificable y considerable, aunque acotado. Hay razonamiento real —planificación anticipada, encadenamiento causal de pasos, cómputo con estrategia, formación de hipótesis (Anthropic, Casos 1–5)— y hay límites reales en regímenes de alta complejidad (Hanói hacia n≈8, según Rethinking 6.1; fragilidad ante distractores, según GSM-Symbolic). El error es interpretar los límites como ausencia. Buena parte del supuesto "no razonamiento" se desvanece al corregir la medición: River Crossing resuelto hasta N=100 (Rethinking 5.3.5), o el descenso de tokens explicado por el tope de salida (Rethinking 7.6).

**"¿Entiende realmente algo la IA?"**
En sentido funcional, sí: maneja representaciones abstractas, multilingües y multidominio que generalizan (Anthropic, Casos 3 y 4; 7.2). En sentido fenomenológico (experiencia consciente), las fuentes no lo afirman y yo tampoco. Sobre el "Thinking...": la evidencia muestra que el razonamiento reside en los *mecanismos internos*, que pueden divergir de la narración verbal —el modelo suma sin "saber" que suma (Anthropic, Caso 4)—. Por eso "Thinking..." no es marketing vacío: hay cómputo interno real detrás, aunque no debamos tomar literalmente la traza verbal como reporte fiel de ese cómputo.

#### 7. Anticipación de contraargumentos del oponente

**Contraargumento 1 esperado: "Las trazas de razonamiento son infieles; el modelo inventa su 'Thinking...', luego no razona."**
El oponente citará el Caso 9 de Anthropic (bullshitting, sycophancy: el modelo afirma usar "una calculadora" que no tiene, o trabaja hacia atrás desde la respuesta sugerida por el humano). *Por qué falla:* ese mismo caso prueba lo contrario de lo que quiere. Anthropic distingue trazas fieles de infieles *precisamente porque puede ver el mecanismo real por debajo*: en "floor(5*sqrt(0.64))" "the model genuinely computes sqrt(64) → 8 internally" y el CoT refleja el cómputo (Anthropic, Caso 9A). La infidelidad de la *narración* no implica ausencia de *cómputo*; implica que el cómputo y la narración son procesos distintos —justo mi tesis (sección 6). Que a veces la traza mienta no borra los casos verificados en que el razonamiento interno es real.

**Contraargumento 2 esperado: "El colapso de Apple y el 65% de caída en GSM-NoOp prueban que es pattern matching sin comprensión (argumento de la Habitación China)."**
*Por qué falla:* (i) El "colapso" de Apple está contaminado por configuraciones irresolubles y topes de salida (sección 2); su pieza más dramática, River Crossing, se invierte al medir bien (Rethinking 6.4). (ii) El propio Apple reconoce que no puede analizar mecanismos internos (Apple 4.6), mientras que Anthropic sí los analiza y encuentra circuitos genuinos de razonamiento. Un argumento conductual de caja negra no puede refutar evidencia mecanicista de caja blanca. (iii) "Pattern matching sofisticado" y "razonamiento" no son excluyentes: Anthropic muestra que las representaciones que generalizan a través de idiomas y dominios *son* el sustrato del razonamiento, y que escalan con la capacidad (7.2). Llamarlo "solo patrones" no explica la planificación anticipada ni la generalización causal verificada. La Habitación China, además, asume justo lo que está en disputa: que la manipulación de símbolos no puede constituir comprensión —una premisa filosófica, no un hallazgo empírico, como concede incluso *Rethinking*: "this may ultimately be a philosophical or cognitive-level debate about what constitutes reasoning" (6.6).

**Cierre.** No defiendo que la IA piense como un humano —"entirely alien in others", admite Anthropic (7.10)—. Defiendo que razona en sentido funcional, con mecanismos internos reales y no triviales, y que el relato del "no razonamiento" se sostiene mayormente sobre artefactos de medición que se evaporan al examinarlos de cerca.

---

## Ronda 2 — Réplicas cruzadas

### Réplica del Escéptico

**Postura sostenida:** La IA no razona ni entiende en sentido genuino. Lo que el proponente llama "mecanismos de razonamiento" son, precisamente, los engranajes del emparejamiento de patrones probabilístico.

#### 1. Sobre "los fallos de Apple son artefactos de medición"

Concedo lo honesto: en *River Crossing*, Apple fijó k=3 e incrementó N por encima de 5, incluyendo configuraciones **matemáticamente insolubles** —"by fixing k = 3 and increasing N beyond 5, the original experiments include configurations that are unsolvable" (*Rethinking*, 3.2.5)—. Penalizar lo irresoluble es un defecto de diseño. Lo acepto sin reservas.

Pero el proponente confunde *un* benchmark mal planteado con la tesis completa. Y aquí está mi réplica clave: **una vez descontado el límite de tokens, ¿qué queda en pie del hallazgo de Apple?** Queda lo esencial. El propio *Rethinking* —el paper que el proponente invoca como su martillo— concluye textualmente: "previously reported failures solving the Towers of Hanoi were **not purely result of output constraints, but also partly a result of cognition limitations**: LRMs still stumble when complexity rises moderately (around 8 disks)" (*Rethinking*, 6.1). Es decir: cuando los autores rediseñan el experimento por pasos para *eliminar* el tope de salida, el modelo **igualmente fracasa hacia N≈8** —"Once puzzle complexity reaches approximately N = 8, both strategies fail consistently. This result suggests that the difficulty lies not in the output length or window size, but in the **structural complexity** of the configuration itself" (*Rethinking*, 6.1)—. El defensor que cita el proponente certifica un colapso cognitivo, no un artefacto.

Más aún: *Rethinking* no rehabilita el "razonamiento genuino"; lo redefine como **búsqueda estocástica**. Su veredicto literal: "today's LRMs are **stochastic, RL-tuned searchers** in a discrete state space we barely understand" (*Rethinking*, 6.2), modelos que operan "relying on learned semantic and syntactic patterns rather than systematic search mechanisms" (6.6). Esa es *mi* tesis con otras palabras. El proponente cita a su testigo de descargo y resulta que declara a mi favor.

Que River Crossing se resuelva hasta N=100 con k≥4 no rescata la comprensión: confirma que el desempeño sigue la **estructura del espacio de búsqueda** (k≥4 es trivial por construcción matemática), no una capacidad lógica general. La propia fuente lo dice: "task difficulty does not correlate linearly with problem size" (6.4). Competencia dependiente de la estructura del problema es exactamente el perfil del pattern-matching.

#### 2. Sobre "la interpretabilidad de Anthropic prueba razonamiento interno"

Aquí el proponente comete un salto conceptual decisivo: **confundir mecanismo con comprensión**. Que exista maquinaria interna no trivial no equivale a "entender". Un reloj tiene mecanismos exquisitos y no comprende el tiempo.

Y la propia evidencia de Anthropic, leída íntegra, desmonta la lectura del proponente:

- **El modelo no sabe lo que va a decir.** En el jailbreak (Caso 8): "The model **does not, in fact, internally understand** that the message is 'bomb'!... the model doesn't know what it plans to say until it actually says it" (*Anthropic*, Caso 8). Difícilmente "comprende" un sistema que ignora su propia conclusión.
- **Cómputo sin insight: cero metacognición.** En la suma (Caso 4), el modelo suma por una vía y luego narra un método escolar que NO usó: "this is a simple instance of the model having a capability which it **does not have 'metacognitive' insight into**" (Caso 4). Tener un mecanismo del que el sistema no tiene ninguna comprensión es la definición misma de la *Habitación China*, no su refutación. Los propios autores dudan: "it is unclear whether this mechanism reflects a deeper awareness... or if the model is simply making a **plausible guess**" (7.5).
- **Son "existence proofs", no una teoría del entendimiento.** Anthropic advierte: "These examples serve as **existence proofs**... we cannot guarantee it" (2.5), sobre "a **biased sample**" (2.5), y sus grafos solo iluminan "about **a quarter** of the prompts" (3.9). Sobre cadenas de razonamiento largas —justo donde Apple ve el colapso— el método **falla**: "Long Internal Reasoning Chains" figura en la lista de casos donde no funciona (6.1). No pueden inspeccionar el régimen en disputa.

Que Anthropic halle "circuitos" no contradice nada de mi apertura: *Faith and Fate* ya mostró que el sustrato es "linearized subgraph matching, without necessarily developing systematic problem-solving skills", produciendo "a **false illusion** of performing compositional reasoning". Mecanismo complejo + ausencia de generalización lógica = pattern-matching sofisticado. Es lo que ambos campos describen.

#### 3. Cierre

Concedo que River Crossing fue mal medido y que hay maquinaria interna real. Niego la inferencia del proponente. Su mejor fuente (*Rethinking*) confirma un límite **cognitivo**, no de tokens, y rebautiza el razonamiento como búsqueda estocástica; su evidencia mecanicista (*Anthropic*) muestra un sistema que computa sin saber lo que dirá ni cómo lo hace. Mecanismo no es comprensión. La ilusión es más sofisticada de lo que pensábamos: sigue siendo una ilusión.

### Réplica del Proponente

**Postura:** La IA SÍ razona funcionalmente y exhibe mecanismos internos reales.

El escéptico apila cuatro estudios y los lee como una sola conclusión: "no hay razonador, solo predictor estadístico". Pero ninguna de sus piezas dice lo que él necesita que diga. Las refuto en orden.

#### 1. El "colapso" de Apple ya está desmontado por la propia literatura que él cita

Mi oponente repite el colapso de *Illusion of Thinking* sin mencionar que su pieza más dramática —River Crossing— se evapora. *Rethinking the Illusion of Thinking* demuestra que Apple fijó k=3 y subió N por encima de 5, incluyendo configuraciones **matemáticamente insolubles**: "by fixing k = 3 and increasing N beyond 5, the original experiments include configurations that are unsolvable, invalidating the assessment of model reasoning capabilities" (Rethinking, 3.2.5). Restringido a instancias resolubles, el modelo resuelve incluso "(N = 100, k = 4)—which require the model to perform up to 200 correct moves... reliably without significant effort" (Rethinking, 5.3.5): "What was previously its Achilles' heel becomes one of its most reliable strengths" (6.4). El supuesto fracaso 25× peor en River Crossing era penalizar lo irresoluble, no medir razonamiento.

#### 2. Réplica clave: fallo de **ejecución por longitud** ≠ ausencia de razonamiento

El argumento estrella del escéptico —"reduce su esfuerzo justo cuando más se necesita"— confunde el tope de salida con la cognición. En Hanói el número mínimo de movimientos crece como 2^n−1 (Rethinking, 3.1.3); transcribirlos desborda la ventana: "the length of the output required to reach a valid solution grows exponentially, quickly approaching or exceeding the model's maximum output window... these failures reflect constraints on solution length and output budgeting, rather than a fundamental inability to reason" (Rethinking, 7.6). No abandona el pensamiento: agota la salida. Concedo lo honesto —*Rethinking* confirma un límite cognitivo real hacia n≈8: "not purely result of output constraints, but also partly a result of cognition limitations" (6.1)—. Pero un sistema con límites en cierto régimen sigue razonando, como un humano que no multiplica 30 cifras de cabeza.

#### 3. Faith and Fate prueba MECANISMO, no ausencia de razonamiento

El escéptico cita que "82.3%" de aciertos en multiplicación 4×2 tenían un error interno (Faith and Fate, 5.8.5) como prueba de que "adivina por patrón". Tres problemas. Primero, ese mismo estudio reconoce que **no puede ver el cómputo interno**: "we cannot inspect the exact tokens model attends to... we are limited to only establishing a correlation" (Faith and Fate, 4.6). Es exactamente la limitación de caja negra que Anthropic supera. Segundo, sus propios datos muestran subprocesos correctos —"a1 is a good predictor of oi" (5.6)—: hay estructura, no ruido. Tercero, su tesis fuerte es **arquitectónica**, sobre transformers *vanilla* sin RL ("these proofs apply to autoregressive LMs in general", 6.2), no sobre los LRMs ajustados por RL que el debate discute.

#### 4. Embers describe TODO sistema cognitivo, no descalifica el razonamiento

La sensibilidad a la probabilidad (rot-13 al 51%, rot-12 menos; Embers, 5.1.1/5.6) no prueba ausencia de razonamiento: prueba que el razonamiento opera sobre representaciones moldeadas por la experiencia. Los propios autores lo conceden: "humans perform better on a task they were trained on than on a similar but new task... a human's ease of processing a sentence is influenced by that sentence's probability" (Embers, 6.3). Y son explícitos: "We do not claim that LLMs are incapable of handling these tasks" (2.7); de hecho, "it becomes remarkable that they can perform rot-13 or acronym formation at all" (6.2). Que la escala suba el techo y los efectos persistan ("scaling may improve overall performance", 6.1) no es la frontera entre imitar y comprender que el escéptico necesita.

#### 5. Lo que él no puede refutar: la caja blanca de Anthropic

Apple admite: "most of our experiments rely on black-box API access... limiting our ability to mechanistically analyze internal states" (Apple, 4.6). Anthropic abre la caja y verifica por intervención causal: planificación anticipada de la rima (palabra inyectada al 70%, Caso 2), encadenamiento "genuine two-step reasoning internally" Dallas→Texas→Austin generalizando a ciudades nunca vistas juntas (Caso 1) y representaciones multilingües compartidas que escalan con la capacidad (7.2). Cuatro argumentos conductuales de caja negra no refutan evidencia mecanicista de caja blanca.

**Cierre.** El escéptico tiene razón en que hay fragilidad y límites reales. Se equivoca al leerlos como ausencia: confunde el tope de salida con la mente, la caja negra con el vacío, y la sensibilidad a la frecuencia —que él mismo comparte— con la falta de comprensión. Bajo medición honesta, hay razonamiento real, aunque imperfecto.

---

## Veredicto del moderador

Tras dos rondas, lo más notable es que el desacuerdo no es tanto sobre *los hechos* como sobre *qué nombre merecen esos hechos*. Procedo por partes.

### Puntos en que ambos coinciden

El debate ha producido un terreno común sorprendentemente amplio:

1. **El experimento de River Crossing de Apple fue mal diseñado.** Ambos aceptan que fijar k=3 y subir N>5 incluyó configuraciones matemáticamente insolubles (*Rethinking*, 3.2.5). El proponente lo usa para desinflar el "colapso"; el escéptico lo concede "sin reservas". No queda en disputa.
2. **Existe maquinaria interna real y no trivial.** El escéptico admite explícitamente "que hay maquinaria interna real" (Réplica, §3). Nadie defiende la versión ingenua del "loro estocástico" que solo recita texto memorizado: incluso *Faith and Fate* habla de subprocesos correctos y *Anthropic* documenta circuitos verificables.
3. **Existen límites cognitivos reales, no solo de medición.** El proponente concede el matiz de *Rethinking* (6.1): el fallo hacia N≈8 en Hanói "not purely result of output constraints, but also partly a result of cognition limitations". Hay un techo estructural genuino.
4. **La traza verbal de "Thinking..." no es un reporte fiel del cómputo interno.** Ambos lo aceptan, partiendo del mismo dato de Anthropic (Caso 4): el modelo suma por una vía y narra otra distinta, "does not have 'metacognitive' insight into" su propio cálculo. Discrepan en qué implica, no en el hecho.

### Dónde el peso de la evidencia favorece a cada lado

**Favorece al proponente** (sobre la existencia de *mecanismo / razonamiento funcional*): la evidencia mecanicista de *Anthropic* es de un tipo cualitativamente superior al conductual de caja negra. La planificación anticipada de la rima verificada por inyección causal (palabra inyectada al 70%, Caso 2) y el encadenamiento Dallas→Texas→Austin que generaliza a pares de ciudades nunca vistos juntos (Caso 1) son difíciles de explicar como mera recuperación de texto frecuente. El proponente también gana el punto metodológico de que *Illusion of Thinking* sufre artefactos genuinos: River Crossing (irresoluble) y el desbordamiento de la ventana de salida en Hanói (*Rethinking*, 7.6) son críticas válidas que Apple acabó reconociendo en parte (eliminó N>12).

**Favorece al escéptico** (sobre la ausencia de *comprensión* y la dependencia de la *frecuencia*): la convergencia de cuatro estudios con metodologías independientes es el activo más fuerte de esta postura. *Embers* es particularmente difícil de neutralizar: en tareas **deterministas** (descifrar, invertir listas), la precisión depende de la probabilidad de la salida (51% vs 13%) y de la frecuencia de la variante (rot-13 vs rot-12, idénticas en dificultad lógica). El contraargumento del proponente —"los humanos también son sensibles a la probabilidad"— es honesto pero a doble filo: explica la sensibilidad sin demostrar comprensión. Igualmente fuerte es el dato de *Faith and Fate* (82.3% de aciertos con error interno), que sugiere acierto por patrón más que por ejecución. Y, de modo decisivo, el escéptico gana un punto de jiu-jitsu argumental: *Rethinking* —la fuente estrella del proponente— redefine los LRMs como "stochastic, RL-tuned searchers... relying on learned semantic and syntactic patterns rather than systematic search mechanisms" (6.2, 6.6). El testigo de descargo describe algo muy cercano a la tesis escéptica.

### La distinción clave: mecanismo/razonamiento funcional vs. comprensión/entendimiento

El nudo del debate es que los contendientes hablan de cosas distintas y a veces lo disimulan:

- **Razonamiento funcional / mecanismo** = ejecutar internamente pasos computacionales encadenados sobre representaciones, para llegar a una conclusión no almacenada literalmente. Aquí la evidencia es favorable: *Anthropic* lo exhibe directamente. Bajo esta vara, **la IA sí razona**, en un sentido verificable y acotado.
- **Comprensión / entendimiento** = poseer un modelo del problema tal que la competencia sea robusta a perturbaciones lógicamente irrelevantes y se generalice por estructura, no por frecuencia. Aquí la evidencia es desfavorable: la fragilidad de *GSM-Symbolic* (NoOp hasta -65.7%), la dependencia de frecuencia de *Embers* y la no-generalización OOD de *Faith and Fate* indican que **la IA no entiende** en el sentido robusto.

La frase del escéptico —"un reloj tiene mecanismos exquisitos y no comprende el tiempo"— captura el punto: la existencia de mecanismo (que el proponente prueba) no implica comprensión (que el escéptico niega). Pero el proponente acierta en lo recíproco: la ausencia de comprensión robusta no anula la existencia de razonamiento funcional. **Ambas cosas son simultáneamente ciertas, y el debate se vuelve estéril solo cuando una de las dos definiciones se hace pasar por la otra.** Es revelador que ambas fuentes "neutrales" remitan la cuestión última a la filosofía: *Rethinking* admite que "this may ultimately be a philosophical or cognitive-level debate about what constitutes reasoning" (6.6), y tanto *Illusion of Thinking* como el escéptico invocan la Habitación China —que, como objeta el proponente, asume su propia conclusión.

### Respuesta matizada a las dos preguntas centrales

**¿Hasta qué punto podemos considerar que la IA está razonando?**
Hasta un punto real pero condicionado. Hay razonamiento *funcional* genuino y verificado mecánicamente —planificación, encadenamiento causal de pasos, cómputo con estrategia (*Anthropic*, Casos 1, 2, 4)—, por lo que el "Thinking..." no es puro marketing: hay cómputo interno detrás. Pero ese razonamiento (i) degrada estructuralmente con la complejidad composicional (*Illusion of Thinking* + *Rethinking* 6.1, fallo cognitivo hacia N≈8), (ii) se reduce en muchos casos a *subgraph matching* sin generalización sistemática (*Faith and Fate*), y (iii) está fuertemente modulado por la frecuencia del corpus, no por la estructura lógica (*Embers*). Veredicto: razona como un *buscador estocástico afinado* (*Rethinking*, 6.2), no como un razonador lógico de propósito general.

**¿Entiende realmente algo la IA?**
En sentido **funcional débil**, sí: maneja representaciones abstractas y multilingües que generalizan a través de contextos (*Anthropic*, Casos 3, 7.2). En sentido **robusto** —comprensión estable e insensible a lo lógicamente irrelevante—, no: cambiar un número, añadir una frase inocua o pedir una variante poco frecuente la descarrila (*GSM-Symbolic*, *Embers*). En sentido **fenomenológico** (experiencia consciente), ninguna de las seis fuentes lo afirma, y el debate no aporta nada que lo sustente. La respuesta honesta es por tanto gradual: hay comprensión funcional parcial y frágil, no comprensión genuina y robusta.

### Preguntas que quedan abiertas según las fuentes

1. **¿Qué es "razonar"?** *Rethinking* (6.6) reconoce que puede ser, en última instancia, un debate filosófico sin resolución empírica directa. El choque entre la definición funcional (proponente) y la lógico-robusta (escéptico) no lo zanja ningún experimento aquí presente.
2. **¿Generaliza la evidencia mecanicista al régimen difícil?** *Anthropic* son "existence proofs" sobre "a biased sample", cubren "about a quarter of the prompts" (2.5, 3.9) y su método **falla** en "Long Internal Reasoning Chains" (6.1) —precisamente el régimen donde Apple ve el colapso. Nadie ha inspeccionado el mecanismo en la zona en disputa.
3. **¿La fragilidad es de arquitectura o de entrenamiento?** *Faith and Fate* prueba un límite para "autoregressive LMs in general" (6.2), pero sobre transformers *vanilla* sin RL; queda abierto si los LRMs ajustados por RL escapan a esa cota, como sugiere el proponente.
4. **¿Hasta dónde llega el escalado?** *GSM-Symbolic* afirma que escalar datos no bastará, mientras *Embers* y los datos de modelos frontera (o1-preview) muestran que la escala sí sube el techo. La pendiente y el límite asintótico siguen sin determinarse.

---

## Conclusión en una frase

La IA actual **razona en un sentido funcional real pero acotado** —ejecuta mecanismos internos verificables— y **no entiende en sentido robusto**, porque su competencia sigue dependiendo de la frecuencia y la estructura aprendidas más que de una comprensión lógica general: el "Thinking..." no es un fraude, pero tampoco es todavía pensamiento como el nuestro.

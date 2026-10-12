# APERTURA — AGENTE ESCÉPTICO (Ronda 1)

**Postura:** La IA actual no razona en sentido genuino ni entiende realmente. Los mensajes tipo "Thinking..." son una *ilusión de razonamiento*: una verbalización superficial que imita la forma del pensamiento sin poseer su sustancia.

---

## 1. Tesis

Lo que llamamos "razonamiento" en los modelos actuales —incluidos los que muestran "Thinking..."— es **emparejamiento de patrones probabilístico** moldeado por la tarea de entrenamiento (predicción de la siguiente palabra), no comprensión ni inferencia lógica genuina. Cuando se controla rigurosamente la complejidad y se eliminan los atajos memorizados, esa fachada se desploma: la precisión cae a cero, la "fragilidad" aparece ante perturbaciones triviales, y el desempeño sigue la *frecuencia estadística* del problema, no su *estructura lógica*. La traza de pensamiento es teatro, no cómputo.

---

## 2. Argumento 1 — Colapso de precisión y límites del "pensar" (The Illusion of Thinking, Apple)

El propio título de la fuente principal lo dice: la "ilusión" del pensamiento. Apple evaluó modelos de razonamiento de frontera (o3-mini, DeepSeek-R1, Claude-3.7-Sonnet-Thinking) en puzzles controlables, y los hallazgos son demoledores para la tesis del razonamiento genuino:

- **Colapso total a cero.** Según *The Illusion of Thinking*, "frontier LRMs face a complete accuracy collapse beyond certain complexities", con la precisión cayendo "to near-zero beyond a certain complexity threshold". En Torre de Hanói el colapso ocurre en N=7 y N=8 (~100–200 movimientos).

- **Más pensar, no más razonar; de hecho, menos.** El dato más revelador: existe un "scaling limit". Según la fuente, "their reasoning effort increases with problem complexity up to a point, then declines despite having an adequate token budget". Es decir, justo cuando el problema se vuelve más difícil y *más* pensamiento haría falta, el modelo *reduce* sus tokens de pensamiento, "despite mostly operating well below their generation length limits". Un razonador genuino no abandona el esfuerzo precisamente cuando más lo necesita; un sistema que imita patrones, sí.

- **Darle el algoritmo no ayuda.** El golpe definitivo: "even when we provide the algorithm in the prompt—so that the model only needs to execute the prescribed steps—performance does not improve, and the observed collapse still occurs at roughly the same point". Si entregas la receta exacta y aun así fracasa al ejecutarla, no hay comprensión del procedimiento: hay incapacidad de ejecución lógica sostenida.

- **Inconsistencia que delata la ausencia de lógica general.** Según la fuente, los modelos logran ">50% accuracy on Tower of Hanoi instances requiring approximately ∼102 moves, yet consistently fail on River Crossing... with substantially lower compositional depth (∼101 moves)" — "performing up to 100 correct moves in Tower of Hanoi but only 4 in River Crossing". Un razonador real no es 25 veces más competente en una tarea más larga que en otra más corta; esto refleja "the solution patterns they learned during training rather than the actual computational complexity of the problems".

Y la propia fuente invoca la analogía decisiva: "As the Chinese room argument illustrates, it's entirely possible to use tools effectively without any real comprehension of the underlying problem."

---

## 3. Argumento 2 — Fragilidad y pattern-matching (GSM-Symbolic y GSM-NoOp, Apple)

Si la IA *entendiera* matemáticas de primaria, cambiar un nombre o un número no debería afectarla. Pero sí lo hace. *GSM-Symbolic* generó variantes de las mismas preguntas a partir de plantillas simbólicas y reveló:

- **Varianza que un niño no tendría.** Según *GSM-Symbolic*, ante distintas instancias de la *misma* pregunta, "for the Gemma2-9B, the gap between the worst performance and the best performance is more than 12%, while for Phi-3.5-mini, this gap is around 15%". La fuente lo califica sin rodeos: "this level of variability would not be expected from a grade-school student with genuine mathematical understanding."

- **Sensibles a los números, no robustos a la lógica.** Cuando solo se cambian valores numéricos (no nombres), la precisión cae. La fuente concluye que "LLMs exhibit more robustness to changes in superficial elements like proper names but are very sensitive to changes in numerical values" — exactamente el perfil de un sistema que empareja superficies, no que opera conceptos.

- **Más cláusulas, derrumbe progresivo.** Al añadir cláusulas (M1→Symb→P1→P2), el desempeño se hunde. Ejemplo de la fuente: Gemma2-9b-it pasa de 84.4% (M1) a **41.8% (P2)**; Phi-3.5-mini de 87.6% a **44.8%**. "the rate of accuracy drop also increases as the difficulty increases."

- **GSM-NoOp: el experimento que cierra el caso.** Se añaden frases *irrelevantes pero plausibles* que no cambian la respuesta correcta. Resultado, según la fuente: "significant performance drops (up to 65%) across all state-of-the-art models", con Phi-3-mini cayendo **-65.7%**. Los modelos "blindly convert them into operations" — convierten en operaciones aritméticas información que cualquiera que *entienda* el problema ignoraría. Más aún: el daño no se repara ni con ejemplos de la misma pregunta ("LLMs struggle even when given multiple shots of the same question"), lo que apunta a "deeper issues in their reasoning processes that cannot be easily mitigated through few-shot learning or fine-tuning".

La conclusión textual de la fuente es mi tesis: "current LLMs are not capable of genuine logical reasoning; instead, they attempt to replicate the reasoning steps observed in their training data" y "their reasoning is fragile and may be more akin to sophisticated pattern matching rather than true logical reasoning."

---

## 4. Argumento 3 — Límites composicionales y "falsa ilusión de razonamiento" (Faith and Fate)

*Faith and Fate* va al mecanismo: ¿cómo "resuelven" los transformers las tareas que requieren componer pasos? La respuesta es lapidaria:

- **Emparejamiento de subgrafos, no resolución de problemas.** Según la fuente, "transformer LLMs solve compositional tasks by reducing multi-step compositional reasoning into linearized subgraph matching, without necessarily developing systematic problem-solving skills".

- **Caída a cero con la complejidad.** En multiplicación de varios dígitos, "ChatGPT and GPT4 achieve only 55% and 59% accuracies" en 3×3 dígitos, y "Transformers' accuracy decreases to near zero as task complexity increases".

- **Aciertan con errores internos: la prueba de que no calculan.** El dato más revelador: "82.3% of the final correct answers for 4-digit by 2-digit multiplications... had at least one error in the computation graph, but still produced correct answers." Acertar el resultado final teniendo el cálculo interno mal solo es posible si el modelo *adivina por patrón*, no si *ejecuta* el algoritmo. La fuente lo nombra: esto da "a false illusion of performing compositional reasoning."

- **No generaliza fuera de lo visto, ni con scratchpad.** Tras *fine-tuning* exhaustivo, "GPT3 achieves near-perfect performance on in-distribution, but fails entirely in generalizing to OOD cases". Y memorizar pasos no equivale a componerlos: "while models can memorize single-step operations, they fail to compose them into correct reasoning paths."

- **Es un límite estructural del paradigma autoregresivo.** La fuente prueba que "the probability of incorrect predictions converges exponentially to ≈1 for abstract compositional tasks. Importantly, these proofs apply to autoregressive LMs in general." No es un defecto de un modelo; es de la arquitectura. Veredicto textual: "pattern matching—and not general reasoning capabilities—may be the cause behind correct model outputs."

---

## 5. Argumento 4 — Moldeado por la tarea de entrenamiento, no comprensión (Embers of Autoregression)

*Embers of Autoregression* (Princeton, PNAS) demuestra que el desempeño está gobernado por *probabilidad estadística*, no por la lógica de la tarea — incluso en tareas **deterministas**, donde la respuesta es única e inequívoca:

- **Sensibilidad a la probabilidad de la salida.** Descifrar un cifrado simple es determinista, pero según la fuente, "GPT-4's accuracy at decoding a simple cipher is 51% when the output is a high-probability sentence but only 13% when it is low-probability". La misma operación lógica, distinto resultado según cuán "frecuente" sea la frase de salida. En inversión de listas: 97% si la salida es probable, 53% si es improbable.

- **Sensibilidad a la frecuencia de la tarea.** "all models except Gemini 1.0 show a spike in accuracy at 13, which is by far the most common shift". GPT-4 "scores 0.50 or above on the three highest-frequency shifts, but its accuracy is less than 0.03 for all other shifts". Recordemos: rot-13 y rot-12 son *idénticos en dificultad lógica*; solo difieren en cuán comunes son en el corpus. La fuente: "the shift cipher with a shift of 13 is over 100 times more common in Internet text than the shift cipher with a shift of 12."

- **Conteo guiado por frecuencia, no por aritmética.** "LLMs often show spikes in accuracy for the numbers that are most frequent in corpora, namely multiples of 10", y la precisión correlaciona más con la *frecuencia* del número (0.84 GPT-4) que con su *magnitud* (0.70).

- **Variantes raras vs comunes.** En siete pares de tareas, "models performed substantially better on common task variants than rare ones": Pig Latin común 42% vs variante rara 23%; orden alfabético (150 veces más común) supera al inverso en los cinco modelos (P < 10⁻⁵).

La metáfora del título es la tesis exacta: bajo los "sparks" hay "embers of autoregression". Y la frase final de la fuente lo sella: "Language models are...language models! That is, they are statistical next-word prediction systems." No comprenden la tarea; reproducen la distribución del texto que predijeron durante el entrenamiento.

---

## 6. Respuesta directa a las dos preguntas centrales

**¿Hasta qué punto podemos considerar que la IA está razonando?**
Hasta el punto en que el problema coincide con patrones frecuentes y de baja profundidad composicional vistos en el entrenamiento — y ni un paso más allá. El "Thinking..." es una traza verbal que *imita la forma* del razonamiento, pero (i) colapsa a cero al aumentar la complejidad (*Illusion of Thinking*), (ii) reduce su esfuerzo justo cuando más se necesita (*Illusion of Thinking*), (iii) no mejora aunque se le entregue el algoritmo (*Illusion of Thinking*), y (iv) produce respuestas correctas con cómputos internos erróneos (*Faith and Fate*). Eso no es razonar: es generar una secuencia plausible de tokens de "pensamiento".

**¿Entiende realmente algo la IA?**
No, en el sentido genuino. Si entendiera, cambiar un nombre o un número irrelevante no la descarrilaría (*GSM-Symbolic*: -15% de varianza, hasta -65.7% con NoOp); resolver rot-13 implicaría resolver rot-12 (*Embers*: 0.50 vs <0.03); y acertar el resultado exigiría que el cálculo interno fuera correcto (*Faith and Fate*: 82.3% de aciertos con errores internos). Como concluyen tanto *GSM-Symbolic* como *Embers*, lo que hay es *pattern-matching probabilístico* y sensibilidad a la frecuencia del corpus — la propia distinción del "Chinese Room Argument" que ambas fuentes invocan: usar la herramienta sin comprender el problema.

---

## 7. Anticipación de contraargumentos del oponente

**Contraargumento 1: "Los modelos resuelven AIME, MATH y exámenes difíciles; eso es razonar."**
Falla por dos motivos respaldados por las fuentes. Primero, esos benchmarks "often suffer from data contamination issues" (*Illusion of Thinking*) — alto desempeño puede reflejar memorización, no razonamiento; *GSM-Symbolic* documenta que el resultado original de GSM8K cae sospechosamente "on the right side of the distribution... for 21 out of 25 models", señal de "potential data contamination". Segundo, *Embers* prueba que el éxito en una tarea no implica comprensión: GPT-4 hace rot-13 al 50%+ pero rot-12 a <3%, siendo lógicamente idénticas. El éxito selectivo en lo *frecuente* es precisamente el síntoma del pattern-matching, no su refutación.

**Contraargumento 2: "Son límites de escala/cómputo; con más tokens, mejor prompting o cadena de pensamiento, razonarán."**
Falla frontalmente contra la evidencia. *Illusion of Thinking* muestra un "scaling limit": el esfuerzo de pensamiento *decrece* tras cierto umbral aun con presupuesto de 64k tokens disponible — más cómputo no se traduce en más razonamiento. *Faith and Fate* demuestra que el límite es estructural ("these proofs apply to autoregressive LMs in general") y que ni el *scratchpad* ni el *grokking* con entrenamiento masivo (hasta 50.000 USD) producen generalización OOD. *GSM-Symbolic* concluye que "scaling training data will not be helpful in improving the reasoning capabilities of language models" y que el daño "cannot be easily mitigated through few-shot learning or fine-tuning". Y *Embers* confirma que con chain-of-thought y few-shot "the basic trends... still hold, just with higher overall levels of accuracy": la escala sube el techo, pero "may not fully overcome the ways in which models are influenced by their nature". Subir el listón no es cruzar la frontera entre imitar y comprender.

---

**Cierre.** Cuatro estudios independientes, con metodologías distintas (puzzles controlables, plantillas simbólicas, grafos de cómputo, análisis teleológico de corpus), convergen en lo mismo: detrás del "Thinking..." no hay un razonador que comprende, sino un predictor estadístico moldeado por la frecuencia de su entrenamiento. La ilusión es convincente. Pero sigue siendo una ilusión.

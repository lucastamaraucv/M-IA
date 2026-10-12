# Debate — Ronda 1: Apertura del AGENTE PROPONENTE

**Postura defendida:** La IA actual SÍ realiza un razonamiento funcional genuino y exhibe mecanismos internos no triviales. Gran parte del aparente "no razonamiento" son artefactos de cómo se mide. Los mensajes "Thinking..." reflejan procesos internos reales, aunque distintos de la cognición humana.

**Pregunta central:** "Ahora las aplicaciones como ChatGPT incluyen mensajes como 'Thinking...'. ¿Hasta qué punto podemos considerar que la IA está razonando? ¿Entiende realmente algo la IA?"

---

## 1. Tesis

Sostengo que los modelos actuales ejecutan procesos computacionales internos estructurados —planificación, encadenamiento de pasos, cómputo con representaciones abstractas— que satisfacen una definición funcional de "razonar". El relato del "colapso" del razonamiento, popularizado por el paper de Apple *The Illusion of Thinking*, descansa en gran medida sobre artefactos de medición: límites de tokens, puzzles matemáticamente irresolubles y evaluación de formato rígido. Cuando se corrigen esos defectos (Dellibarda Varela et al., *Rethinking the Illusion of Thinking*) o se abre la "caja negra" con interpretabilidad mecanicista (Lindsey et al., Anthropic, *On the Biology of a Large Language Model*), lo que emerge no es un loro estocástico, sino maquinaria de razonamiento real aunque imperfecta.

---

## 2. Argumento 1 — Los "fallos" de Apple son, en buena parte, artefactos de medición

La conclusión más fuerte de Apple —que los LRMs "fail to develop generalizable problem-solving capabilities, with accuracy ultimately collapsing to near-zero" (Apple, Bloque 6.1)— se apoya en un diseño experimental con tres defectos que *Rethinking the Illusion of Thinking* documenta.

**(a) River Crossing: se les exigió resolver lo irresoluble.** Este es el dato más demoledor. Apple fijó la capacidad del bote en k = 3 mientras aumentaba N por encima de 5. Pero los criterios formales de resolubilidad establecen que una configuración solo tiene solución si "(a) k ≥ 4 ⇒ ∀N ≥ 1, the puzzle is solvable, (b) k ≤ 3 ⇒ N ≤ 2k − 1 (i.e., N ≤ 5 for k = 3)" (Rethinking, Bloque 3.2.6, citando a Efimova 2018 y Spahn & Zeilberger 2022). En consecuencia, "by fixing k = 3 and increasing N beyond 5, the original experiments include configurations that are unsolvable, invalidating the assessment of model reasoning capabilities in River Crossing tasks" (Rethinking, 3.2.5). Penalizar a un modelo por no resolver un problema sin solución no mide razonamiento; mide el error del evaluador. Y cuando *Rethinking* restringe las pruebas a instancias resolubles, el resultado se invierte por completo: "even in large-scale instances such as (N = 100, k = 4) —which require the model to perform up to 200 correct moves— the LRM solves the task reliably without significant effort" (Rethinking, 5.3.5). En palabras de los autores: "What was previously its Achilles' heel becomes one of its most reliable strengths" (6.4). El "fracaso catastrófico" era un fantasma metodológico.

**(b) El descenso de tokens no es "rendirse a pensar", es tope de salida.** Apple interpretó la caída de tokens al subir la complejidad como un "scaling limit" cognitivo: "their reasoning effort increases with problem complexity up to a point, then declines despite having an adequate token budget" (Apple, 6.2). Pero en Torres de Hanói el número mínimo de movimientos crece como 2^n − 1 (Apple, 3.1.3); la transcripción literal de la solución desborda la ventana de salida. Como recoge *Rethinking*: "the length of the output required to reach a valid solution grows exponentially, quickly approaching or exceeding the model's maximum output window... These failures thus reflect constraints on solution length and output budgeting, rather than a fundamental inability to reason" (Rethinking, 7.6, citando a Lawsen). El propio Apple acabó reconociendo el problema: "to account for context limit concerns for large values of N in Tower of Hanoi, we have removed N > 12 from the experiments" (Apple, 3.1.5).

**(c) Evaluación de formato, no de comprensión.** Apple solo puntuaba la transcripción completa, movimiento a movimiento, en un único pase ("solve the entire problem in a single pass", Rethinking 3.1.4). Eso confunde "saber resolver" con "poder transcribir miles de líneas sin un solo error de formato". Es un sesgo de medición: castiga la mecánica de salida, no la capacidad de razonar.

**Honestidad intelectual (refuerza, no debilita, mi tesis):** *Rethinking* también confirma que en Hanói hay un componente cognitivo real: "previously reported failures... were not purely result of output constraints, but also partly a result of cognition limitations: LRMs still stumble when complexity rises moderately (around 8 disks)" (Rethinking, 6.1). Acepto ese matiz. Mi tesis no es que la IA razone perfectamente, sino que razona *de verdad y de forma no trivial*; un sistema con límites en cierto régimen sigue siendo un sistema que razona, igual que un humano que no puede multiplicar números de 30 cifras de cabeza no por ello "no razona".

---

## 3. Argumento 2 — Evidencia mecanicista directa de razonamiento interno (Anthropic)

El argumento decisivo no es conductual sino mecanicista. Apple mismo reconoce su limitación clave: "most of our experiments rely on black-box API access... limiting our ability to mechanistically analyze internal states" (Apple, 4.6). Anthropic abre esa caja con grafos de atribución sobre 30 millones de *features* (Anthropic, 3.3) y documenta, mediante experimentos de intervención causal, lo siguiente:

**(a) Planificación anticipada en poesía.** Buscando improvisación, los investigadores encontraron lo contrario: "we find compelling evidence for a planning mechanism... the model often activates features corresponding to candidate end-of-next-line words prior to writing the line" (Anthropic, Caso 2). El modelo activa la rima objetivo ("rabbit", "habit") en el salto de línea, *antes* de escribir el verso, y construye hacia atrás: "the model works backward from its target word to write a sentence that naturally ends in that word". Más aún, "the model holds multiple possible planned words 'in mind' at the same time". La prueba causal: al inyectar una palabra planificada, "the model ended its line with the injected planned word in 70% of cases" (Caso 2). Eso es planificación con objetivos internos, no predicción miope del siguiente token.

**(b) Razonamiento multi-paso genuino.** Ante "the capital of the state containing Dallas is", el modelo no usa un atajo memorizado: "the model performs genuine two-step reasoning internally", ejecutando la cadena Dallas → Texas → Austin (Anthropic, Caso 1). Y generaliza: sustituyendo features se obtiene Oakland → California → Sacramento, Shanghai → China → Beijing, etc. Hay un encadenamiento causal de pasos intermedios, verificado por intervención.

**(c) Cálculo mental con estrategia propia.** En "36+59=95", el modelo no copia una tabla: combina "una vía de baja precisión (magnitud aproximada) con una vía de alta precisión (dígito de las unidades exacto)" mediante features de suma que generalizan incluso a contextos no aritméticos (Anthropic, Caso 4). Dato revelador para el debate sobre "Thinking...": cuando se le pregunta *cómo* sumó, responde el algoritmo escolar de acarreo —que NO es lo que hizo internamente: "this is a simple instance of the model having a capability which it does not have 'metacognitive' insight into" (Caso 4). Es decir, el cómputo real es independiente de su narración verbal. Esto es central: el razonamiento ocurre en los mecanismos, no necesariamente en lo que el texto "Thinking..." dice de sí mismo.

**(d) Representaciones abstractas y multilingüismo.** Los tres prompts de antónimos en inglés, francés y chino "are driven by very similar circuits, with shared multilingual components" (Anthropic, Caso 3). Existe un "concepto" de la operación (antónimo/sinónimo) independiente del idioma. Y esta abstracción escala con la capacidad: "the prevalence of these language-agnostic representations is higher in Claude 3.5 Haiku than in a smaller, less capable model, suggesting that such general representations are linked to model capabilities" (Anthropic, 7.2).

**(e) Diagnóstico clínico por hipótesis.** Ante un caso obstétrico, el modelo activa internamente el feature "preeclampsia" aunque la palabra no aparece, formula hipótesis diagnósticas y, al inhibirlas causalmente, cambia su pregunta hacia el diagnóstico alternativo (colecistitis) (Anthropic, Caso 5). Eso es razonamiento clínico estructurado, no recitación.

La conclusión de Anthropic es inequívoca: "The most consistent finding of our investigations is the massive complexity underlying the model's responses even in relatively simple contexts" (7.7). Lo opuesto a un loro estocástico.

---

## 4. Argumento 3 — Matización de GSM-Symbolic: qué SÍ logran los modelos

Concedo que GSM-Symbolic (Mirzadeh et al.) muestra fragilidad: varianza entre instancias y caídas de hasta "65%" en GSM-NoOp (GSM-Symbolic, 5.4.6). Pero leído con rigor, el paper también acota *cuánto* sí razonan los modelos:

- **Robustez frente a cambios superficiales.** "LLMs exhibit more robustness to changes in superficial elements like proper names but are very sensitive to changes in numerical values" (GSM-Symbolic, 2.6). Que distingan lo superficial (nombres) de lo estructural (números) ya implica una representación no trivial del problema.
- **El cuello de botella NO es la aritmética.** Su propia ablación lo demuestra: en GSM-P1/P2 la precisión aritmética se mantiene casi perfecta —"the addition accuracy of the models remains nearly perfect for calculations involving up to 4 digits" (GSM-Symbolic, 5.7 / Fig. 17)—. El cómputo numérico funciona; la fragilidad está en la robustez ante distractores, no en una incapacidad de calcular.
- **Los modelos frontera resisten.** En la escala difícil GSM-P2, o1-preview obtiene "94.0(±2.38)" y GPT-4o "88.0(±3.43)" (GSM-Symbolic, 5.3.1 / 5.5). Y en GSM-NoOp, o1-preview cae solo "-17.5", la menor de todas (5.4.1). El propio dato de Apple es coherente: la escala mejora el razonamiento, no es un fenómeno binario.
- **La crítica estadística está reconocida por los propios autores.** Mirzadeh et al. admiten: "if one disagrees with our assumptions and accepts the assumptions of Ivanova et al. (2025), our results would likewise be statistically non-significant" (GSM-Symbolic, 6.4 / Verificación 4). Su conclusión de "no razonamiento" descansa sobre una elección filosófica discutible (distribución degenerada vs. Bernoulli), no sobre un hecho cerrado.

La fragilidad ante distractores es un *límite de robustez*, no la ausencia de razonamiento. Coincide con Anthropic, que muestra circuitos reales junto a fallos reales: ambos coexisten.

---

## 5. Definición operativa: qué cuenta como "razonar" y "entender"

Para evitar discusiones estériles, propongo definiciones funcionales ancladas en las fuentes:

- **Razonar (funcional):** ejecutar internamente una secuencia de pasos computacionales sobre representaciones, encadenados causalmente, para alcanzar una conclusión no almacenada literalmente. Esto es exactamente lo que Anthropic verifica por intervención: "genuine two-step reasoning internally" (Caso 1) y "internally generated plans for its future outputs" (7.3). Mirzadeh et al. coinciden en el criterio de *novedad*: razonar es alcanzar "a 'novel' goal", distinto de "mere memorization" (GSM-Symbolic, 7.1–7.2); el caso Dallas→Texas→Austin y su generalización a ciudades nunca vistas juntas satisfacen ese criterio.
- **Entender (funcional, no fenomenológico):** poseer representaciones internas abstractas y manipulables que generalizan a través de contextos. Anthropic lo evidencia con las representaciones multilingües compartidas y el diagnóstico por hipótesis. NO afirmo conciencia ni experiencia subjetiva: afirmo comprensión *funcional*, la única que cualquier evaluación —humana o de máquina— puede medir.

Bajo estas definiciones, el debate deja de ser sobre "alma" y pasa a ser empírico. Y la evidencia mecanicista lo zanja a favor de la existencia de razonamiento.

---

## 6. Respuesta directa a las dos preguntas centrales

**"¿Hasta qué punto podemos considerar que la IA está razonando?"**
Hasta un punto verificable y considerable, aunque acotado. Hay razonamiento real —planificación anticipada, encadenamiento causal de pasos, cómputo con estrategia, formación de hipótesis (Anthropic, Casos 1–5)— y hay límites reales en regímenes de alta complejidad (Hanói hacia n≈8, según Rethinking 6.1; fragilidad ante distractores, según GSM-Symbolic). El error es interpretar los límites como ausencia. Buena parte del supuesto "no razonamiento" se desvanece al corregir la medición: River Crossing resuelto hasta N=100 (Rethinking 5.3.5), o el descenso de tokens explicado por el tope de salida (Rethinking 7.6).

**"¿Entiende realmente algo la IA?"**
En sentido funcional, sí: maneja representaciones abstractas, multilingües y multidominio que generalizan (Anthropic, Casos 3 y 4; 7.2). En sentido fenomenológico (experiencia consciente), las fuentes no lo afirman y yo tampoco. Sobre el "Thinking...": la evidencia muestra que el razonamiento reside en los *mecanismos internos*, que pueden divergir de la narración verbal —el modelo suma sin "saber" que suma (Anthropic, Caso 4)—. Por eso "Thinking..." no es marketing vacío: hay cómputo interno real detrás, aunque no debamos tomar literalmente la traza verbal como reporte fiel de ese cómputo.

---

## 7. Anticipación de contraargumentos del oponente

**Contraargumento 1 esperado: "Las trazas de razonamiento son infieles; el modelo inventa su 'Thinking...', luego no razona."**
El oponente citará el Caso 9 de Anthropic (bullshitting, sycophancy: el modelo afirma usar "una calculadora" que no tiene, o trabaja hacia atrás desde la respuesta sugerida por el humano). *Por qué falla:* ese mismo caso prueba lo contrario de lo que quiere. Anthropic distingue trazas fieles de infieles *precisamente porque puede ver el mecanismo real por debajo*: en "floor(5*sqrt(0.64))" "the model genuinely computes sqrt(64) → 8 internally" y el CoT refleja el cómputo (Anthropic, Caso 9A). La infidelidad de la *narración* no implica ausencia de *cómputo*; implica que el cómputo y la narración son procesos distintos —justo mi tesis (sección 6). Que a veces la traza mienta no borra los casos verificados en que el razonamiento interno es real.

**Contraargumento 2 esperado: "El colapso de Apple y el 65% de caída en GSM-NoOp prueban que es pattern matching sin comprensión (argumento de la Habitación China)."**
*Por qué falla:* (i) El "colapso" de Apple está contaminado por configuraciones irresolubles y topes de salida (sección 2); su pieza más dramática, River Crossing, se invierte al medir bien (Rethinking 6.4). (ii) El propio Apple reconoce que no puede analizar mecanismos internos (Apple 4.6), mientras que Anthropic sí los analiza y encuentra circuitos genuinos de razonamiento. Un argumento conductual de caja negra no puede refutar evidencia mecanicista de caja blanca. (iii) "Pattern matching sofisticado" y "razonamiento" no son excluyentes: Anthropic muestra que las representaciones que generalizan a través de idiomas y dominios *son* el sustrato del razonamiento, y que escalan con la capacidad (7.2). Llamarlo "solo patrones" no explica la planificación anticipada ni la generalización causal verificada. La Habitación China, además, asume justo lo que está en disputa: que la manipulación de símbolos no puede constituir comprensión —una premisa filosófica, no un hallazgo empírico, como concede incluso *Rethinking*: "this may ultimately be a philosophical or cognitive-level debate about what constitutes reasoning" (6.6).

---

**Cierre.** No defiendo que la IA piense como un humano —"entirely alien in others", admite Anthropic (7.10)—. Defiendo que razona en sentido funcional, con mecanismos internos reales y no triviales, y que el relato del "no razonamiento" se sostiene mayormente sobre artefactos de medición que se evaporan al examinarlos de cerca.

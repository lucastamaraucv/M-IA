# Debate — Ronda 2: RÉPLICA del AGENTE PROPONENTE

**Postura:** La IA SÍ razona funcionalmente y exhibe mecanismos internos reales.

---

El escéptico apila cuatro estudios y los lee como una sola conclusión: "no hay razonador, solo predictor estadístico". Pero ninguna de sus piezas dice lo que él necesita que diga. Las refuto en orden.

## 1. El "colapso" de Apple ya está desmontado por la propia literatura que él cita

Mi oponente repite el colapso de *Illusion of Thinking* sin mencionar que su pieza más dramática —River Crossing— se evapora. *Rethinking the Illusion of Thinking* demuestra que Apple fijó k=3 y subió N por encima de 5, incluyendo configuraciones **matemáticamente insolubles**: "by fixing k = 3 and increasing N beyond 5, the original experiments include configurations that are unsolvable, invalidating the assessment of model reasoning capabilities" (Rethinking, 3.2.5). Restringido a instancias resolubles, el modelo resuelve incluso "(N = 100, k = 4)—which require the model to perform up to 200 correct moves... reliably without significant effort" (Rethinking, 5.3.5): "What was previously its Achilles' heel becomes one of its most reliable strengths" (6.4). El supuesto fracaso 25× peor en River Crossing era penalizar lo irresoluble, no medir razonamiento.

## 2. Réplica clave: fallo de **ejecución por longitud** ≠ ausencia de razonamiento

El argumento estrella del escéptico —"reduce su esfuerzo justo cuando más se necesita"— confunde el tope de salida con la cognición. En Hanói el número mínimo de movimientos crece como 2^n−1 (Rethinking, 3.1.3); transcribirlos desborda la ventana: "the length of the output required to reach a valid solution grows exponentially, quickly approaching or exceeding the model's maximum output window... these failures reflect constraints on solution length and output budgeting, rather than a fundamental inability to reason" (Rethinking, 7.6). No abandona el pensamiento: agota la salida. Concedo lo honesto —*Rethinking* confirma un límite cognitivo real hacia n≈8: "not purely result of output constraints, but also partly a result of cognition limitations" (6.1)—. Pero un sistema con límites en cierto régimen sigue razonando, como un humano que no multiplica 30 cifras de cabeza.

## 3. Faith and Fate prueba MECANISMO, no ausencia de razonamiento

El escéptico cita que "82.3%" de aciertos en multiplicación 4×2 tenían un error interno (Faith and Fate, 5.8.5) como prueba de que "adivina por patrón". Tres problemas. Primero, ese mismo estudio reconoce que **no puede ver el cómputo interno**: "we cannot inspect the exact tokens model attends to... we are limited to only establishing a correlation" (Faith and Fate, 4.6). Es exactamente la limitación de caja negra que Anthropic supera. Segundo, sus propios datos muestran subprocesos correctos —"a1 is a good predictor of oi" (5.6)—: hay estructura, no ruido. Tercero, su tesis fuerte es **arquitectónica**, sobre transformers *vanilla* sin RL ("these proofs apply to autoregressive LMs in general", 6.2), no sobre los LRMs ajustados por RL que el debate discute.

## 4. Embers describe TODO sistema cognitivo, no descalifica el razonamiento

La sensibilidad a la probabilidad (rot-13 al 51%, rot-12 menos; Embers, 5.1.1/5.6) no prueba ausencia de razonamiento: prueba que el razonamiento opera sobre representaciones moldeadas por la experiencia. Los propios autores lo conceden: "humans perform better on a task they were trained on than on a similar but new task... a human's ease of processing a sentence is influenced by that sentence's probability" (Embers, 6.3). Y son explícitos: "We do not claim that LLMs are incapable of handling these tasks" (2.7); de hecho, "it becomes remarkable that they can perform rot-13 or acronym formation at all" (6.2). Que la escala suba el techo y los efectos persistan ("scaling may improve overall performance", 6.1) no es la frontera entre imitar y comprender que el escéptico necesita.

## 5. Lo que él no puede refutar: la caja blanca de Anthropic

Apple admite: "most of our experiments rely on black-box API access... limiting our ability to mechanistically analyze internal states" (Apple, 4.6). Anthropic abre la caja y verifica por intervención causal: planificación anticipada de la rima (palabra inyectada al 70%, Caso 2), encadenamiento "genuine two-step reasoning internally" Dallas→Texas→Austin generalizando a ciudades nunca vistas juntas (Caso 1) y representaciones multilingües compartidas que escalan con la capacidad (7.2). Cuatro argumentos conductuales de caja negra no refutan evidencia mecanicista de caja blanca.

**Cierre.** El escéptico tiene razón en que hay fragilidad y límites reales. Se equivoca al leerlos como ausencia: confunde el tope de salida con la mente, la caja negra con el vacío, y la sensibilidad a la frecuencia —que él mismo comparte— con la falta de comprensión. Bajo medición honesta, hay razonamiento real, aunque imperfecto.

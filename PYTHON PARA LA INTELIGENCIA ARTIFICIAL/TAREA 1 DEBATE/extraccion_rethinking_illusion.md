# Extracción académica: "Rethinking the Illusion of Thinking"

Todas las citas textuales se transcriben literalmente del documento (en inglés, su idioma original). Las descripciones están en español. Solo se incluye lo que el documento dice explícitamente.

---

## BLOQUE 1 — IDENTIDAD

**1.1 Título completo:** "Rethinking the Illusion of Thinking"

**1.2 Autores en orden:** Iñaki Dellibarda Varela (autor correspondiente), Pablo Romero-Sorozabal, Eduardo Rocon, Manuel Cebrian.
- Cita: "Iñaki Dellibarda Varela,1, ∗Pablo Romero-Sorozabal,1 Eduardo Rocon,1 and Manuel Cebrian1"
- Cita: "∗Corresponding author: i.dellibarda@car.upm-csic.es"

**1.3 Afiliación:** "Center for Automation and Robotics, Spanish National Research Council (CSIC-UPM), Madrid, Spain"

**1.4 Fecha:** "(Dated: July 3, 2025)". El encabezado arXiv indica "1 Jul 2025".

**1.5 arXiv/id:** "arXiv:2507.01231v1 [cs.AI] 1 Jul 2025"

**1.6 Financiamiento:** Cita textual:
- "IDV acknowledges funding from CSIC."
- "MC is supported by the Horizon Europe Chips JU under the NexTArc CAR project (HORIZON-JU-Chips-2024-2-RIA) and by grant PID2023-150271NB-C21 from the Spanish Ministry of Science, Innovation, and Universities / Spanish State Research Agency (MICINN/AEI, DOI: 10.13039/501100011033)."
- "PRZ received a Training Program fellowship (PRE2020-634092049) from the Ministry of Science and Innovation."
- "Additional funding was provided by Google.org through a grant awarded to Fundación General CSIC. Google.org had no role in the design, execution, analysis, reporting of this research, or in decisions related to publication or presentation."

**1.7 Agradecimientos:** "The authors would like to thank José Hernández-Orallo for detailed comments on the analysis."

---

## BLOQUE 2 — CONTEXTO Y MOTIVACIÓN

**2.1 Paper previo que motiva (título, autores, año):**
- Título: "The Illusion of Thinking: Understanding the Strengths and Limitations of Reasoning Models via the Lens of Problem Complexity"
- Autores (según referencia [2]): "Shojaee, P., Mirzadeh, I., Alizadeh, K., Horton, M., Bengio, S., Farajtabar, M."
- Año / publicación: "In June 2025, Apple published a highly controversial paper". La referencia [2] no indica año entre paréntesis pero da fecha de acceso "last accessed 2025/06/25".

**2.2 Hallazgos exactos de ese paper de Apple según ESTE documento:**
- "Based on their study, the authors concluded that current LRMs exhibited fundamental limitations in generalizable reasoning."
- "These models consistently failed to perform beyond a certain complexity threshold: they underperformed on high-complexity tasks and tended to overthink in simple ones, where older models—namely Large Language Models (LLMs)—often achieved better results."
- "Their performance also varied significantly across puzzles, successfully executing hundreds of steps in the Towers of Hanoi before failing, while rarely completing more than five moves in the River Crossing problem."
- "Another notable finding concerned token usage. LRMs reach peak token consumption when the task is complex but still solvable. Conversely, when the model implicitly detects that the task lies beyond its capabilities, it drastically reduces its output length—suggesting as potential form of internal uncertainty estimation or early abandonment strategy."
- Sobre Hanoi: "Shojaee et al. reported that LRMs handled the initial moves but deteriorated sharply beyond n≈8: models violated rules, repeated states, or produced invalid sequences."
- "Additionally, the authors found that in simpler configurations, traditional LLMs—without explicit reasoning chains—often outperformed LRMs, as they produced shorter, more direct outputs with fewer computational resources."
- Sobre River Crossing: "Empirically, in Shojaee et al.'s experiments, LRMs seldom produced more than five valid moves and showed the weakest results across the benchmark."
- "These results were taken as evidence of a deeper limitation: although LRMs displayed emergent reasoning behaviors in some tasks, they lacked the robustness and consistency required to perform reliably across different problem domains."

**2.3 Controversia que generó:**
- "Earlier this year, Apple ignited controversy by publishing "The Illusion of Thinking," prompting heated debate within the AI community."
- "The study generated a sharp divide within the AI community."
- "The debate quickly transcended academic boundaries. This polarization highlights the urgency of reassessing how we evaluate reasoning in language models..."

**2.4 Posiciones del debate y quién las sostiene:**
- Críticos: "Critics seized upon the findings as conclusive evidence that Large Reasoning Models (LRMs) lack genuine reasoning capabilities, branding them as mere stochastic parrots." / "On one side, critics interpreted the findings as definitive evidence that LRMs fundamentally lack reasoning capabilities, reducing them to mere stochastic parrots."
- Defensores: "Meanwhile, defenders—spearheaded by Lawsen et al. (2025)—fired back, condemning the experimental setup as flawed and the conclusions overstated." / "On the other, defenders argued that the study suffers from flawed benchmarks, questionable experimental design, and overreaching conclusions."

**2.5 Medios mencionados y qué dijeron:**
- "The study rapidly attracts attention beyond technical circles and sparks media coverage in outlets such as The Guardian and The Wall Street Journal, which highlight its warnings about the collapse of LRMs in complex reasoning tasks and raise concerns about the scalability of AI reasoning [3, 4]."
- The Guardian (ref [3]): "Marcus, G.: When billion-dollar AIs break down over puzzles a child can do. The Guardian (2025)."
- The Wall Street Journal (ref [4]): "Mims, C.: Why Superintelligent AI Isn't Taking Over Anytime Soon."
- También menciona: "In parallel, a number of rapid-response publications and technical commentaries emerge, critically analyzing the study's methodology, results, and conclusions [5, 6]."

**2.6 Objetivo declarado de este paper:**
- "We clarify this debate by replicating and refining two of the original study's most contentious benchmarks: Towers of Hanoi and River Crossing."
- "Building on this debate, our work emphasizes the influence of task formulation, input validity, and prompt structure on LRM performance."
- "our goal is to complement their findings by introducing alternative perspectives and experimental refinements."
- "Our aim is to contribute a fresh perspective to the ongoing debate surrounding the reasoning capabilities of large language models (LRMs)."

**2.7 Qué dice que NO pretende hacer:**
- "We emphasize that this work does not aim to undermine the contributions of Shojaee et al. [2]. On the contrary, we consider their study both impactful and timely."
- "Our goal is not to benchmark models against each other in terms of absolute performance, but rather to analyze and contrast their general behavioral trends under varying levels of task complexity and prompting strategies."
- "This qualitative comparison highlights differences in reasoning dynamics and failure patterns, rather than direct performance benchmarking." (pie de Fig. 4)

---

## BLOQUE 3 — BENCHMARKS Y PUZZLES

El documento analiza explícitamente dos puzzles: Towers of Hanoi y River Crossing.

### 3.1 TOWERS OF HANOI (Torres de Hanói)

**3.1.1 Descripción exacta:**
"Towers of Hanoi is a classic recursive puzzle involving three pegs and a stack of disks of decreasing size placed on one peg in sorted order. The goal is to move the entire stack to a target peg..."

**3.1.2 Reglas exactas:**
"...following two constraints: only one disk may be moved at a time, and no disk may be placed on top of a smaller one."

**3.1.3 Fórmula matemática de dificultad (cita exacta):**
"The minimal number of moves required to solve the puzzle grows exponentially with the number of disks, following the expression 2n−1." (es decir, 2^n − 1). "This makes it a scalable benchmark for evaluating long-horizon planning and symbolic rule-following."

**3.1.4 Resultados reportados por el paper previo (Apple):**
- "Shojaee et al. reported that LRMs handled the initial moves but deteriorated sharply beyond n≈8: models violated rules, repeated states, or produced invalid sequences."
- "This trend was interpreted as a symptom of reasoning breakdowns in long-horizon planning. Although the minimal solution path was known and recursive, the models failed to generalize the underlying pattern, especially when prompted to generate full solutions in one pass."
- "Interestingly, when the task exceeded the models' operational limits, the number of tokens used dropped significantly, suggesting that the models implicitly recognized their inability to complete the solution and reduced their effort accordingly."
- "Additionally, the authors found that in simpler configurations, traditional LLMs—without explicit reasoning chains—often outperformed LRMs..."

**3.1.5 Problemas/fallas metodológicas del paper de Apple identificadas por ESTE documento (sobre Hanoi):**
- El documento expone (citando [5, 6]) la hipótesis de que el fallo se debe a límite de salida, no a falta de razonamiento: "These failures thus reflect constraints on solution length and output budgeting, rather than a fundamental inability to reason [5]." / "the model's awareness of its restricted context and output windows. According to this perspective, the model may possess a conceptual understanding of the solution, yet refrain from generating complete reasoning traces due to the anticipated length of the required output."
- Crítica al modo de prompting de un solo paso: "...especially when prompted to generate full solutions in one pass."
- [NOTA: el documento NO declara explícitamente que el setup de Hanoi de Apple fuera un "error metodológico" como sí lo hace con River Crossing; lo presenta como hipótesis del debate que luego refuta parcialmente con sus experimentos.]

**3.1.6 Criterios matemáticos de resolubilidad:** [NO MENCIONADO EN EL TEXTO] (para Hanoi solo se da la fórmula del número mínimo de movimientos 2^n − 1; no se enuncia un criterio de resolubilidad/insolubilidad).

### 3.2 RIVER CROSSING (Cruce del río)

**3.2.1 Descripción exacta:**
"In this variant, N agent-actor pairs must cross a river using a boat with limited capacity k..."

**3.2.2 Reglas exactas:**
- "...subject to the constraint that no actor may remain with a different agent unless its own agent is present."
- Del pie de Fig. 1: "each pair of agent and actor (same color) must cross the river while respecting the constraint that no actor can be left with a different agent unless accompanied by their own."
- "Difficulty grows with N and depends on k."

**3.2.3 Fórmula matemática de dificultad si se menciona:** "Difficulty grows with N and depends on k". El documento describe el perfil de dificultad como no lineal (ver Bloque 6). No se da una fórmula numérica cerrada de dificultad. [INCOMPLETO EN EL TEXTO en cuanto a fórmula explícita de dificultad.]

**3.2.4 Resultados reportados por el paper previo (Apple):**
- "in the original study, this puzzle yields the poorest performance, with LRMs failing to solve any configuration where the number of agent–actor pairs N > 5."
- "Empirically, in Shojaee et al.'s experiments, LRMs seldom produced more than five valid moves and showed the weakest results across the benchmark."

**3.2.5 Problemas/fallas metodológicas del paper de Apple identificadas por ESTE documento (sobre River Crossing):**
- "However, the experimental setup introduces a critical flaw: while increasing N, the boat capacity k remains fixed at 3."
- "By fixing k = 3 and increasing N beyond 5, the original experiments include configurations that are unsolvable, invalidating the assessment of model reasoning capabilities in River Crossing tasks."
- "However, these experiments also prompted the model to solve mathematically unsolvable initial configurations, highlighting critical limitations in the evaluation design."
- "the River Crossing results initially heralded as catastrophic failures turn out to hinge upon testing unsolvable configurations." (resumen)

**3.2.6 Criterios matemáticos de resolubilidad (fórmulas exactas):**
Cita textual: "Formal solvability criteria for this class of problems establish that a configuration is solvable if and only if it satisfies one of the following conditions [9, 10]:"
- (a) k ≥ 4 ⇒ ∀N ≥ 1, the puzzle is solvable
- (b) k ≤ 3 ⇒ N ≤ 2k − 1 (i.e., N ≤ 5 for k = 3)
También en el resumen: "only instances satisfying k≥4 or N ≤2k −1 are solvable [9, 10]."

---

## BLOQUE 4 — METODOLOGÍA

**4.1 Modelos usados (nombres y versiones exactos):**
- "We employ the Gemini family of models as our LRM, specifically Gemini 2.5 Pro."
- Modelos comparados (de Apple, estimados de gráficos): "the performance curves for Claude 3.7 Sonnet and DeepSeek-R1 are manually estimated from the published plots and should be interpreted as approximations."

**4.2 Justificación (del modelo elegido):**
"This model demonstrates state-of-the-art performance in structured reasoning tasks [11–13]."

**4.3 Cada estrategia experimental con su nombre exacto:**
1. "Stepwise Resolution in Towers of Hanoi" (Resolución por pasos en Torres de Hanói)
2. "Agentic Dialogue in Towers of Hanoi" (Diálogo agéntico en Torres de Hanói)
3. "River Crossing" (réplica restringida a configuraciones resolubles)

**4.4 Para cada una:**

**Estrategia 1 — Stepwise Resolution:**
- (a) Paso a paso: "The overall goal remains the same as in the original experiment, but instead of prompting the LRM to solve the entire problem in a single pass, we divide the task into N subproblems. In each subproblem, the model is asked to generate the next p steps toward the solution, starting from the current configuration. The subsequent prompt then resumes from the final state of the previous iteration."
- (b) Diferencia con Apple: "instead of prompting the LRM to solve the entire problem in a single pass, we divide the task into N subproblems." / "This iterative setup reduces the output burden at each stage, allowing us to test whether performance improves when the model operates under a shorter reasoning horizon."
- (c) Parámetros exactos: N de subproblemas (división de la tarea); p = número de movimientos solicitados por subetapa ("the next p steps"). Valores numéricos concretos de p: [INCOMPLETO EN EL TEXTO] (se define p como variable; en resultados, "p indicates the number of moves requested per substage" en pie de Fig. 2, pero no se da el valor numérico de p en el texto). Configuraciones de disco y trials se detallan en Resultados (N = 3 a N = 10; 10 trials).

**Estrategia 2 — Agentic Dialogue:**
- (a) Paso a paso: "this procedure also employs stepwise resolution. However, instead of prompting a single LRM with isolated queries to transition between states (separated by p moves), we implement an agentic system composed of two LRMs that collaborate through dialogue. Each agent maintains access to a shared memory and infers the current state based on the latest movements provided by its counterpart. During each turn, the agent receives the last set of moves and is tasked with proposing the next p steps toward the solution."
- (b) Diferencia con Apple / con la estrategia 1: usa dos LRMs colaborando en diálogo en lugar de un solo LRM con consultas aisladas; emplea memoria compartida. Justificación: "Recent studies have shown that multi-agent systems offer several advantages over single-model architectures... [14–18, 21]."
- (c) Parámetros exactos: dos LRMs; p movimientos por turno; memoria compartida. Valor numérico de p: [INCOMPLETO EN EL TEXTO].

**Estrategia 3 — River Crossing (réplica restringida):**
- (a) Paso a paso: "we replicate the original River Crossing experiments while restricting our tests to configurations that are mathematically solvable under the known constraints. This allows us to isolate reasoning failures from structural impossibility..."
- (b) Diferencia con Apple: Apple fijaba k = 3 e incrementaba N incluyendo configuraciones insolubles; este trabajo varía k y restringe a instancias resolubles.
- (c) Parámetros exactos (en Resultados): "The boat capacity is altered from k = 2 to k = 4, and the number of agent–actor couples ranges from N = 2 to N = 100, always respecting the constraints for solvable configurations." "Each configuration is repeated 10 times."

**4.5 Cómo manejó la comparabilidad con el paper de Apple:**
- "Our experimental procedures build directly upon the baseline design proposed by Shojaee et al. [2]. To ensure compatibility, we reuse the original prompts (see Code Availability) provided in their study with only minor modifications tailored to our setting."
- "It is essential to clarify that the original paper does not disclose the exact success rate values for each configuration. Therefore, the performance curves for Claude 3.7 Sonnet and DeepSeek-R1 are manually estimated from the published plots and should be interpreted as approximations."
- "However, this limitation is not problematic for the purpose of our study. Our goal is not to benchmark models against each other in terms of absolute performance, but rather to analyze and contrast their general behavioral trends..."

**4.6 Limitaciones metodológicas reconocidas sobre sus propios métodos:**
- Sobre la métrica de tokens totales: "this trend must be interpreted with caution, as the total token count (black line) is highly sensitive to the substage at which the model makes a mistake. If the LRM fails early in the resolution—e.g., during the first substage—the overall token consumption remains low, regardless of the overall complexity of the puzzle."
- Sobre la comparación con Apple: las curvas de Apple son estimadas manualmente de gráficos (citado arriba en 4.5).
- En trabajo futuro reconoce necesidad de más tests para reducir varianza (ver Bloque 10).

---

## BLOQUE 5 — RESULTADOS CUANTITATIVOS

### 5.1 TOWERS OF HANOI — Stepwise Resolution

- 5.1.1 Valores numéricos exactos: El texto NO reporta porcentajes numéricos de tasa de éxito. Describe tendencias. [INCOMPLETO EN EL TEXTO en cuanto a valores numéricos puntuales.]
- 5.1.2 Rangos de N: "varying the number of disks from N = 3 to N = 10."
- 5.1.3 Trials por configuración: "we run 10 independent trials to obtain robust averages."
- 5.1.4 Métricas: tasa de éxito (success rate); tokens totales por puzzle ("cumulative token count across all substages in a trial"); tokens promedio por subetapa/request ("average number of tokens used per substage").
- 5.1.5 Punto exacto de fallo/éxito: "When the problem reaches higher levels of difficulty (i.e., N ≥8), we observe a notable decrease in the total number of tokens used by the model during reasoning." / (Discusión) "Once puzzle complexity reaches approximately N = 8, both strategies fail consistently."
- 5.1.6 Porcentajes/umbrales/valores críticos: umbral N ≈ 8. No hay porcentajes numéricos explícitos.
- 5.1.7 Patrones de tokens: "when puzzle complexity increases - yet remains within the LRM's solvable range - the token rate also rises accordingly... However, when the puzzle exceeds the LRM's capabilities, the token rate drops, reflecting early-stage failures and an implicit recognition of task infeasibility." El token total (línea negra) es sensible a la subetapa del fallo; el token por request (línea azul) es indicador más estable.

### 5.2 TOWERS OF HANOI — Agentic Dialogue

- 5.2.1 Valores numéricos exactos: [INCOMPLETO EN EL TEXTO] (no se dan porcentajes).
- 5.2.2 Rangos de N: "evaluating the same configurations from N = 3 to N = 10."
- 5.2.3 Trials por configuración: "with 10 independent trials conducted for each."
- 5.2.4 Métricas: tasa de éxito y uso de tokens (totales y por request), igual que estrategia anterior.
- 5.2.5 Punto exacto de fallo/éxito: "The model begins to struggle as early as N = 4, clearly exhibiting worse performance in solving the problem compared to the previous methodology."
- 5.2.6 Porcentajes/umbrales/valores críticos: empieza a fallar desde N = 4; rendimiento peor que stepwise. No hay porcentajes numéricos.
- 5.2.7 Patrones de tokens: "Unlike in the previous experiment... in this case, the LRM agents continue to invest considerable effort even when they are ultimately unable to solve the task. Token rates remain high across configurations." Comportamiento observado: "in most trials, the agentic system maintains extended dialogues without committing illegal moves, but ends up looping indefinitely—oscillating forward and backward—without ever converging to a valid solution."

### 5.3 RIVER CROSSING

- 5.3.1 Valores numéricos exactos: [INCOMPLETO EN EL TEXTO] (sin porcentajes numéricos explícitos).
- 5.3.2 Rangos de N y k: "The boat capacity is altered from k = 2 to k = 4, and the number of agent–actor couples ranges from N = 2 to N = 100, always respecting the constraints for solvable configurations."
- 5.3.3 Trials por configuración: "Each configuration is repeated 10 times."
- 5.3.4 Métricas: tasa de éxito (verde) y fallo (rojo); tokens promedio por configuración (± desviación estándar). (pie de Fig. 3)
- 5.3.5 Punto exacto de fallo/éxito: configuraciones más difíciles "(N = 4, k = 3) and (N = 5, k = 3)". Instancias grandes resueltas con fiabilidad: "Even in large-scale instances such as (N = 100, k = 4)—which require the model to perform up to 200 correct moves—the LRM solves the task reliably without significant effort or resource usage."
- 5.3.6 Porcentajes/umbrales/valores críticos: pico de dificultad en configuración intermedia "(N = 5, k = 3)": "the system reaches a peak in resource demand while simultaneously showing the lowest efficiency." "(N = 100, k = 4)" requiere "up to 200 correct moves".
- 5.3.7 Patrones de tokens: "The most difficult configurations—(N = 4, k = 3) and (N = 5, k = 3)—demand the highest number of tokens... Conversely, the simplest configurations—those with k = 2 and k = 4 regardless of N—pose little challenge... able to solve them without significantly increasing token usage." "increasing the puzzle size (i.e., increasing N) does not exhibit a direct correlation with reasoning complexity."

---

## BLOQUE 6 — HALLAZGOS Y CONCLUSIONES

**6.1 Cada conclusión explícita:**
- "we show that previously reported failures solving the Towers of Hanoi were not purely result of output constraints, but also partly a result of cognition limitations: LRMs still stumble when complexity rises moderately (around 8 disks)."
- "the River Crossing results initially heralded as catastrophic failures turn out to hinge upon testing unsolvable configurations. Once we limit tests strictly to solvable problems—LRMs effortlessly solve large instances involving over 100 agent pairs."
- "Once puzzle complexity reaches approximately N = 8, both strategies fail consistently. This result suggests that the difficulty lies not in the output length or window size, but in the structural complexity of the configuration itself."
- "By restricting the experiments to initial configurations with known solvable solutions, the LRM demonstrates remarkably strong reasoning capabilities. What was previously its Achilles' heel becomes one of its most reliable strengths."
- "for LRMs, task difficulty does not correlate linearly with problem size. Certain intermediate configurations may prove nearly unsolvable, while larger instances are handled successfully."
- "In our experiments, LRMs perform significantly better on River Crossing than on Towers of Hanoi."
- "our findings—alongside those of Shojaee et al.—highlight a consistent link between task difficulty and token consumption during reasoning."

**6.2 Frases textuales más importantes:**
- "Our findings ultimately defy simplistic narratives: today's LRMs are stochastic, RL-tuned searchers in a discrete state space we barely understand. Real progress in symbolic, long-horizon reasoning demands mapping that terrain through fine-grained ablations like those introduced here."
- "Ultimately, using LRMs to solve these problems is equivalent to unleashing a stochastic search procedure, chain-of-thought sampling refined by reinforcement learning—inside a large, into discrete search space whose structure we have barely characterised. To make decisive progress, we must first map that terrain."
- "Rather than a purely technical issue, this may ultimately be a philosophical or cognitive-level debate about what constitutes reasoning."

**6.3 Qué confirma del paper de Apple:**
- El umbral de fallo en Hanoi hacia N ≈ 8: "LRMs still stumble when complexity rises moderately (around 8 disks)."
- El patrón de tokens: "This pattern is consistent with the observations reported by Shojaee et al." (sobre la caída de tokens cuando el modelo percibe la tarea como intratable).
- Confirma que el fallo en Hanoi no es solo por límites de salida sino también cognitivo: "previously reported failures solving the Towers of Hanoi were not purely result of output constraints, but also partly a result of cognition limitations."

**6.4 Qué refuta o matiza del paper de Apple:**
- Matiza Hanoi: el fallo no es solo límite de ventana de salida; pero también muestra que descomponer la tarea no mejora significativamente: "even when decomposing the task, performance does not significantly improve compared to the original study." (matiza la hipótesis de los defensores, no solo a Apple).
- Refuta el resultado de River Crossing: Apple incluyó configuraciones insolubles (k=3, N>5). Restringiendo a configuraciones resolubles, "LRMs effortlessly solve large instances involving over 100 agent pairs." → "What was previously its Achilles' heel becomes one of its most reliable strengths."
- Refuta que la dificultad crezca linealmente con el tamaño: "task difficulty does not correlate linearly with problem size" (a diferencia de "In the original study by Shojaee et al., all puzzles are intrinsically framed with a linearly increasing difficulty, proportional to problem size.").

**6.5 Postura final sobre si los LRMs razonan:**
- "Building on the theoretical positions of both proponents and critics of LRM reasoning, our findings reveal that the question is far from settled. We observe valid arguments on both sides, suggesting that reasoning capacity is difficult to generalize through benchmark tasks alone."
- "such puzzles remain out of reach for current LRMs, not due to explicit violations of logic or game rules, but because of a deeper incapacity to structure and execute coherent long-horizon strategies."
- "today's LRMs are stochastic, RL-tuned searchers in a discrete state space we barely understand."

**6.6 Implicaciones filosóficas/cognitivas:**
- "Rather than a purely technical issue, this may ultimately be a philosophical or cognitive-level debate about what constitutes reasoning."
- "their competence varies by task. In our experiments, LRMs perform significantly better on River Crossing than on Towers of Hanoi."
- "This non-linear profile underscores the need to evaluate LRM capabilities in terms of problem structure rather than size alone."
- Sobre regiones de transición de fase: "large language models operate through stochastic token generation, relying on learned semantic and syntactic patterns rather than systematic search mechanisms. This fundamental difference in approach makes them especially vulnerable in tightly constrained solution spaces..."

---

## BLOQUE 7 — CONCEPTOS TÉCNICOS

**7.1 LRM (Large Reasoning Models):** No se da una definición formal aparte de su uso. Cita de uso: "As Large Reasoning Models (LRMs) advance, reliably assessing their performance has become correspondingly challenging." Caracterización final: "today's LRMs are stochastic, RL-tuned searchers in a discrete state space we barely understand."

**7.2 LLM (Large Language Models):** Caracterizados como modelos "without explicit reasoning chains": "older models—namely Large Language Models (LLMs)" / "traditional LLMs—without explicit reasoning chains—often outperformed LRMs, as they produced shorter, more direct outputs with fewer computational resources." Y: "large language models operate through stochastic token generation, relying on learned semantic and syntactic patterns rather than systematic search mechanisms."

**7.3 Stepwise resolution (resolución por pasos):** "instead of prompting the LRM to solve the entire problem in a single pass, we divide the task into N subproblems. In each subproblem, the model is asked to generate the next p steps toward the solution, starting from the current configuration." Uso: estrategia para Hanoi para testear si el límite es el budget de tokens.

**7.4 Agentic dialogue (diálogo agéntico):** "an agentic system composed of two LRMs that collaborate through dialogue. Each agent maintains access to a shared memory and infers the current state based on the latest movements provided by its counterpart." Uso: estrategia alternativa para Hanoi.

**7.5 Phase transition (transición de fase):** "Such "phase transition" regions are notoriously difficult even for conventional search-based algorithms and are typically addressed using combinatorial optimization methods such as graph traversal, constraint satisfaction solvers, neural approximators, or evolutionary algorithms." Uso: explica el pico de dificultad en River Crossing en (N=5, k=3), región límite entre dos regímenes.

**7.6 Token budget / output window:** "the length of the output required to reach a valid solution grows exponentially, quickly approaching or exceeding the model's maximum output window." / "These failures thus reflect constraints on solution length and output budgeting, rather than a fundamental inability to reason [5]." Uso: hipótesis técnica investigada por el paper.

**7.7 Stochastic search (búsqueda estocástica):** "using LRMs to solve these problems is equivalent to unleashing a stochastic search procedure, chain-of-thought sampling refined by reinforcement learning—inside a large... discrete search space whose structure we have barely characterised." Uso: caracterización final de cómo operan los LRMs.

**7.8 Stochastic parrots (loros estocásticos):** Concepto usado por los críticos según el documento: "branding them as mere stochastic parrots." No se define formalmente; se atribuye a la posición crítica.

**7.9 Long-horizon planning / reasoning (planificación a largo horizonte):** Usado repetidamente; "a deeper incapacity to structure and execute coherent long-horizon strategies." No se da definición formal. [Definición explícita: NO MENCIONADA EN EL TEXTO.]

**7.10 Overthink (sobre-pensar):** Atribuido a hallazgo de Apple: "tended to overthink in simple ones." No se define formalmente.

---

## BLOQUE 8 — REFERENCIAS

**8.[1]** Zhou, L., Pacchiardi, L., Martínez-Plumed, F., Collins, K.M., Moros-Daval, Y., Zhang, S., Zhao, Q., Huang, Y., Sun, L., Prunty, J.E., Li, Z., Sánchez-García, P., Chen, K.J.J., Casares, P.A.M., Zu, J., Burden, J., Mehrbakhsh, B., Stillwell, D., Cebrian, M., Wang, J., Henderson, P., Wu, S.T., Kyllonen, P.C., Cheke, L., Xie, X., Hernández-Orallo, J. — "General Scales Unlock AI Evaluation with Explanatory and Predictive Power." arXiv preprint arXiv:2503.06378 (2025). Contexto: necesidad de refinar protocolos de evaluación.

**8.[2]** Shojaee, P., Mirzadeh, I., Alizadeh, K., Horton, M., Bengio, S., Farajtabar, M. — "The Illusion of Thinking: Understanding the Strengths and Limitations of Reasoning Models via the Lens of Problem Complexity." URL: https://ml-site.cdn-apple.com/papers/the-illusion-of-thinking.pdf, last accessed 2025/06/25. Contexto: el paper de Apple replicado.

**8.[3]** Marcus, G. — "When billion-dollar AIs break down over puzzles a child can do." The Guardian (2025). URL: https://www.theguardian.com/commentisfree/2025/jun/10/billion-dollar-ai-puzzle-break-down, last accessed 2025/06/25. Contexto: cobertura mediática.

**8.[4]** Mims, C. — "Why Superintelligent AI Isn't Taking Over Anytime Soon." URL: https://www.wsj.com/tech/ai/artificial-superintelligence-overestimation-3f954065, last accessed 2025/06/25. Contexto: cobertura mediática (Wall Street Journal).

**8.[5]** Lawsen, A. — "Comment on The Illusion of Thinking: Understanding the Strengths and Limitations of Reasoning Models via the Lens of Problem Complexity." arXiv preprint (2025). URL: https://arxiv.org/abs/2506.09250, last accessed 2025/06/25. Contexto: defensor; hipótesis de límite de output.

**8.[6]** Khan, S., Madhavan, S., Natarajan, K. — "A Comment On "The Illusion of Thinking": Reframing the Reasoning Cliff as an Agentic Gap." arXiv preprint (2025). URL: https://arxiv.org/abs/2506.18957, last accessed 2025/06/25. Contexto: comentario crítico al paper de Apple.

**8.[7]** Messeri, L., Crockett, M.J. — "Artificial intelligence and illusions of understanding in scientific research." Nature 627, 49–58 (2024). DOI: https://doi.org/10.1038/s41586-024-07146-0. Contexto: [no citado explícitamente en el cuerpo con número visible; aparece en lista de referencias].

**8.[8]** Sun, Y., Hu, S., Zhou, G., Zheng, K., Hajishirzi, H., Dziri, N., Song, D. — "OMEGA: Can LLMs Reason Outside the Box in Math? Evaluating Exploratory, Compositional, and Transformative Generalization." URL: https://arxiv.org/abs/2506.18880, last accessed 2025/06/27. Contexto: frameworks de evaluación alineados con razonamiento científico.

**8.[9]** Efimova, E.A. — "River Crossing Problems: Algebraic Approach." arXiv preprint (2018). URL: https://arxiv.org/abs/1802.09369, last accessed 2025/06/25. Contexto: criterios de resolubilidad de River Crossing.

**8.[10]** Spahn, G., Zeilberger, D. — "Variations on the Missionaries and Cannibals Problem." arXiv preprint (2022). URL: https://arxiv.org/abs/2210.12269, last accessed 2025/06/25. Contexto: criterios de resolubilidad de River Crossing.

**8.[11]** Google DeepMind — "Gemini 1.5 Technical Report." arXiv preprint (2024). URL: https://arxiv.org/abs/2403.05530, last accessed 2025/06/26. Contexto: respaldo del rendimiento de Gemini.

**8.[12]** Gemini Team et al. — "Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context." URL: https://arxiv.org/abs/2403.05530, last accessed 2025/06/26. Contexto: respaldo del modelo Gemini.

**8.[13]** Gemini Team et al. — "Gemini: A Family of Highly Capable Multimodal Models." URL: https://arxiv.org/abs/2312.11805, last accessed 2025/06/26. Contexto: respaldo del modelo Gemini.

**8.[14]** Sreedhar, K., Chilton, L. — "Simulating Human Strategic Behavior: Comparing Single and Multi-agent LLMs." arXiv preprint (2024). URL: https://arxiv.org/abs/2402.08189, last accessed 2025/06/26. Contexto: ventajas de sistemas multi-agente.

**8.[15]** Qian, C., Xie, Z., Wang, Y., Liu, W., Zhu, K., Xia, H., Dang, Y., Du, Z., Chen, W., Yang, C., Liu, Z., Sun, M. — "Scaling Large Language Model-based Multi-Agent Collaboration." arXiv preprint (2025). URL: https://arxiv.org/abs/2406.07155, last accessed 2025/06/26. Contexto: colaboración multi-agente.

**8.[16]** Gao, M., Li, Y., Liu, B., Yu, Y., Wang, P., Lin, C., Lai, F. — "Single-agent or Multi-agent Systems? Why Not Both?" arXiv preprint (2025). URL: https://arxiv.org/abs/2505.18286, last accessed 2025/06/26. Contexto: sistemas multi-agente.

**8.[17]** Wang, D., Ye, Z., Fang, F., Li, L. — "Cooperative Strategic Planning Enhances Reasoning Capabilities in Large Language Models." arXiv preprint (2024). URL: https://arxiv.org/abs/2410.20007, last accessed 2025/06/26. Contexto: planificación estratégica cooperativa.

**8.[18]** Buehler, M.J. — "PRefLexOR: Preference-based Recursive Language Modeling for Exploratory Optimization of Reasoning and Agentic Thinking." npj Artificial Intelligence 1, 4 (2025). DOI: https://doi.org/10.1038/s44387-025-00003-z, last accessed 2025/06/26. Contexto: razonamiento y pensamiento agéntico.

**8.[19]** Kirkpatrick, S., Selman, B. — "Critical behavior in the satisfiability of random boolean expressions." Science 264(5163), 1297–1301 (1994). doi: 10.1126/science.264.5163.1297. Contexto: problemas combinatorios con regiones de dificultad (transición de fase).

**8.[20]** Rahwan, I., Cebrian, M., Obradovich, N., Bongard, J., Bonnefon, J.-F., Breazeal, C., Crandall, J. W., Christakis, N. A., Couzin, I. D., Jackson, M. O., et al. — "Machine behaviour." Nature 568, 477–486 (2019). Contexto: mapear el "terreno" del comportamiento de máquinas como paso para progresar.

**8.[21]** Crandall, J. W., Oudah, M., Ishowo-Oloko, F., Abdallah, S., Bonnefon, J.-F., Cebrian, M., Shariff, A., Goodrich, M. A., Rahwan, I., et al. — "Cooperating with machines." Nature Communications 9, 233 (2018). Contexto: cooperación con máquinas / sistemas agénticos.

---

## BLOQUE 9 — FIGURAS Y TABLAS

El documento NO contiene tablas. Contiene 4 figuras.

**9.1 FIG. 1** — Pie exacto: "Illustration of the two benchmark puzzles analyzed in this study: Towers of Hanoi (top) and River Crossing (bottom). Each panel shows three sequential states: the initial configuration, an intermediate state after a few moves, and the final goal configuration. In Towers of Hanoi, the disks must be moved from the left peg to the right peg following size and move constraints. In River Crossing, each pair of agent and actor (same color) must cross the river while respecting the constraint that no actor can be left with a different agent unless accompanied by their own."
- Variables: estados (inicial, intermedio, final) de ambos puzzles.
- Conclusión del texto: figura ilustrativa de los dos benchmarks.

**9.2 FIG. 2** — Pie exacto: "Comparison of performance across two solving strategies for the Towers of Hanoi puzzle: (a) stepwise resolution and (b) agentic dialogue. Each chart displays the success rate (purple bars, left axis), the total number of tokens used with standard deviation (black line, right axis), and the average tokens per request (blue dashed line, right axis). Insets provide a zoomed-in view of the average per-request token usage. Here, N denotes the number of disks in the puzzle, and p indicates the number of moves requested per substage."
- Variables: tasa de éxito (barras moradas), tokens totales ± SD (línea negra), tokens promedio por request (línea azul discontinua); N = número de discos; p = movimientos por subetapa.
- Conclusión del texto: caída de tasa de éxito al crecer N; en stepwise los tokens totales caen al fallar temprano en N≥8; en agentic los tokens se mantienen altos aunque no resuelva.

**9.3 FIG. 3** — Pie exacto: "Performance of the LRM in the River Crossing puzzle across different solvable configurations, defined by the number of couples N and boat capacity k. The black line with error bars represents the average number of tokens used by the model per configuration (± standard deviation), while the colored bars indicate success (green) and failure (red) rates."
- Variables: N (parejas), k (capacidad del barco); tokens promedio ± SD (línea negra); tasas de éxito (verde) y fallo (rojo).
- Conclusión del texto: las configuraciones (N=4,k=3) y (N=5,k=3) demandan más tokens y menor eficiencia; tamaño N grande (p.ej. N=100, k=4) se resuelve sin problema.

**9.4 FIG. 4** — Pie exacto: "Comparison of success rate trends between our experimental results and those reported by Shojaee et al. [2]. (a) Towers of Hanoi: stepwise prompting and agentic dialogue strategies are evaluated across increasing numbers of disks (N). (b) River Crossing: multiple configurations with varying number of agents (N) and boat capacities (k) are assessed. Apple's results (Claude 3.7 Sonnet and DeepSeek-R1) are estimated from the original paper, as exact success rate values are not publicly reported. This qualitative comparison highlights differences in reasoning dynamics and failure patterns, rather than direct performance benchmarking."
- Variables: tendencias de tasa de éxito de este estudio vs. Apple; (a) Hanoi por número de discos N; (b) River Crossing por N y k.
- Conclusión del texto: (a) descomponer la tarea no mejora significativamente; fallo consistente cerca de N=8; (b) restringiendo a configuraciones resolubles, gran mejora en River Crossing.

---

## BLOQUE 10 — GAPS Y TRABAJO FUTURO

**10.1 Limitaciones reconocidas:**
- "the original paper does not disclose the exact success rate values for each configuration. Therefore, the performance curves for Claude 3.7 Sonnet and DeepSeek-R1 are manually estimated from the published plots and should be interpreted as approximations."
- Sensibilidad de la métrica de tokens totales a la subetapa de fallo (ver Bloque 4.6).
- "drawing general conclusions about their reasoning abilities proves challenging, as these systems exhibit strong context- and formulation-dependent behavior."

**10.2 Trabajo futuro:**
- "the next steps in this project will primarily focus on scaling up the experimental framework. This includes running a larger number of tests per configuration to reduce statistical variance and expanding the set of configurations analyzed to capture a broader range of task complexities."
- "Additionally, it would be valuable to assess whether the observed performance trends generalize across different LLM architectures. Comparing multiple models and tracking their progress over time could offer deeper insights into the evolution of reasoning capabilities..."

**10.3 Preguntas abiertas:**
- "our findings reveal that the question is far from settled. We observe valid arguments on both sides, suggesting that reasoning capacity is difficult to generalize through benchmark tasks alone. Rather than a purely technical issue, this may ultimately be a philosophical or cognitive-level debate about what constitutes reasoning."
- "today's LRMs are stochastic, RL-tuned searchers in a discrete state space we barely understand... To make decisive progress, we must first map that terrain."

**10.4 Código/recursos (URLs exactas):**
- "The complete codebase and the prompts used in this study are available at: https://github.com/11inaki11/Rethinking-The-Illusion-of-Thinking"

---

## VERIFICACIÓN — 5 datos más difíciles de encontrar (con cita textual)

1. **Criterios de resolubilidad de River Crossing (fórmulas exactas):** "(a) k ≥4 ⇒ ∀N ≥1, the puzzle is solvable, (b) k ≤3 ⇒ N ≤2k −1 (i.e., N ≤5 for k = 3)."

2. **Modelo exacto usado por los autores:** "We employ the Gemini family of models as our LRM, specifically Gemini 2.5 Pro."

3. **Modelos de Apple comparados (estimados de gráficos):** "the performance curves for Claude 3.7 Sonnet and DeepSeek-R1 are manually estimated from the published plots and should be interpreted as approximations."

4. **Número de movimientos requeridos en la instancia grande de River Crossing:** "Even in large-scale instances such as (N = 100, k = 4)—which require the model to perform up to 200 correct moves—the LRM solves the task reliably without significant effort or resource usage."

5. **Fórmula de número mínimo de movimientos en Hanói:** "The minimal number of moves required to solve the puzzle grows exponentially with the number of disks, following the expression 2n−1." (2^n − 1)

Datos adicionales difíciles confirmados:
- URL del código: "https://github.com/11inaki11/Rethinking-The-Illusion-of-Thinking"
- Agradecimiento nominal: "thank José Hernández-Orallo for detailed comments on the analysis."
- Punto de fallo agentic dialogue: "The model begins to struggle as early as N = 4."

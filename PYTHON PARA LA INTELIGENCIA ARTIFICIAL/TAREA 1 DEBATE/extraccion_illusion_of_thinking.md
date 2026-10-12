# EXTRACCIÓN ACADÉMICA — "The Illusion of Thinking"

> Extracción literal y estructurada. Solo contiene lo que el documento dice explícitamente. Citas entre comillas dobles.

---

## BLOQUE 1 — IDENTIDAD

**1.1 Título completo:** "The Illusion of Thinking: Understanding the Strengths and Limitations of Reasoning Models via the Lens of Problem Complexity"

**1.2 Autores en orden:** "Parshin Shojaee∗†", "Iman Mirzadeh∗", "Keivan Alizadeh", "Maxwell Horton", "Samy Bengio", "Mehrdad Farajtabar".
- Notas: "∗Equal contribution." y "†Work done during an internship at Apple."

**1.3 Afiliación:** "Apple". Correos: "{pshojaee, imirzadeh, kalizadehvahid, bengio, farajtabar}@apple.com"

**1.4 Fecha:** "arXiv:2506.06941v3 [cs.AI] 20 Nov 2025"

**1.5 arXiv/id:** "arXiv:2506.06941v3 [cs.AI]"

**1.6 Financiamiento:** [NO MENCIONADO EN EL TEXTO]

**1.7 Agradecimientos:** "The authors would like to thank Scott Hoang, Yichen Jiang, Minsik Cho, Mohammad Sekhavat, David Harrison, Mohammadreza Armandpour and Devi Krishna for the valuable feedback and support."

---

## BLOQUE 2 — CONTEXTO Y MOTIVACIÓN

**2.1 Paper previo que motiva (título, autores, año):** No se identifica un único "paper previo que motiva". El paper se posiciona frente a la evaluación de LRMs en benchmarks matemáticos y de código. Citas referenciales clave mencionadas como motivación incluyen:
- Ref. [6]: "Seyed Iman Mirzadeh, Keivan Alizadeh, Hooman Shahrokhi, Oncel Tuzel, Samy Bengio, and Mehrdad Farajtabar. GSM-symbolic: Understanding the limitations of mathematical reasoning in large language models." (ICLR 2025) — citado al preguntarse si los modelos usan "different forms of pattern matching [6]".
- Ref. [35] Yue et al.: "Does reinforcement learning really incentivize reasoning capacity in llms beyond the base model?" (2025).
[AMBIGUO] No hay una declaración explícita de "el paper que motiva este trabajo".

**2.2 Hallazgos de ese paper según este documento:**
- De Yue et al. [35]: "Yue et al. [35] have questioned whether reinforcement learning elicits novel reasoning patterns, observing that the pass@k performance of reasoning and non-reasoning models ultimately converge with larger samples."
- De estudios previos [35, 41]: "They have shown that under equivalent inference token budgets, non-thinking LLMs can eventually reach performance comparable to thinking models on benchmarks like MATH500 [42] and AIME24 [43]."
- De Valmeekam et al. [40] y Ruoss et al. [39]: "demonstrated that reasoning models such as o1 show significant performance improvements compared to previous models on puzzles and decision-making tasks."
- Sobre "overthinking" [30, 31, 32, 33]: "models produce verbose, redundant outputs, even after finding the solution, creating significant inference computational overhead."
- Refs. [34, 33, 32]: "have demonstrated that in newer LRMs accuracy generally declines when thinking increases in math problems".

**2.3 Controversia:** El documento incluye una sección "A.1 Response to Main Criticisms" que aborda críticas a su propio paper: "This section addresses critiques raised regarding our paper and provides our responses to these concerns." Las críticas explícitas:
- "Are failures on Tower of Hanoi due to context limit issues rather than reasoning limitations?"
- "Do models collapse primarily due to the sampling of large number of moves (particularly on Tower of Hanoi)?"
- "Does River Crossing with N≥6 invalidate our core findings on this puzzle?"
- "Is the finding that providing algorithms doesn't improve performance specific to Tower of Hanoi due to its well-known recursive algorithm or reflecting a general limitation of reasoning models?"
- "Why not use tools for solving these puzzles?"

**2.4 Posiciones del debate y quién las sostiene:** El texto presenta las posiciones como "critics" / "Some critics" / "The critic" sin nombrarlos. Ejemplos: "Some critics argue that sampling is the primary cause of the observed collapse behavior (particularly on Tower of Hanoi)." y "The critic suggests that the findings of algorithm execution limitation in LRMs (Section 4.4) may be only an artifact of the Tower of Hanoi's well-known recursive algorithm being already memorized by models". Los autores (Apple) sostienen la posición contraria en cada respuesta. [No se nombran personas concretas de la crítica EN EL TEXTO.]

**2.5 Medios mencionados:** [NO MENCIONADO EN EL TEXTO] (no se citan medios de prensa; sí "Google AI Blog" como fuente de la ref. [5]).

**2.6 Objetivo declarado:**
- "In this work, we systematically investigate these gaps with the help of controllable puzzle environments that allow precise manipulation of compositional complexity while maintaining consistent logical structures."
- "In this study, we probe the reasoning mechanisms of frontier LRMs through the lens of problem complexity."
- "our objective is to assess models' reasoning processes—their ability to understand problems, explore solution spaces, and execute logical steps—rather than merely achieving correct final answers."

**2.7 Qué dice que NO pretende hacer:**
- "However, our primary aim is not to propose a new benchmark; instead, we use similar benchmarks as tools for designing experiments to better understand the reasoning behavior of language models."
- "in this work we do not grade for optimality of final solution and only measuring the correctness of each move and reaching the target state."

---

## BLOQUE 3 — BENCHMARKS Y PUZZLES

El paper evalúa "four controllable puzzles spanning compositional depth, planning complexity, and distributional settings." Ilustrados en Figura 3.

### 3.1 TOWER OF HANOI

**3.1.1 Descripción exacta:** "Tower of Hanoi is a puzzle featuring three pegs and n disks of different sizes stacked on the first peg in size order (largest at bottom). The goal is to transfer all disks from the first peg to the third peg." Detalle del Apéndice: "three pegs (labeled 0, 1, and 2 from left to right) and N disks of varying sizes, where each disk is uniquely numbered from 1 (smallest) to N (largest)." "The goal is to transfer all disks from peg 0 to peg 2, maintaining the same size ordering (largest at bottom, smallest at top)."

**3.1.2 Reglas exactas:** "Valid moves include moving only one disk at a time, taking only the top disk from a peg, and never placing a larger disk on top of a smaller one." Apéndice: "(1) Single Disk Movement: Only one disk may be moved at a time; (2) Top Disk Access: Only the topmost disk from any peg can be selected for movement; and (3) Size Ordering Constraint: A larger disk may never be placed on top of a smaller disk."

**3.1.3 Fórmula matemática de dificultad/nº de movimientos:** "the minimum number of required moves with n initial disks will be 2n −1" (es decir, 2^N − 1). Apéndice: "The minimum number of moves required to solve the Tower of Hanoi recursive puzzle with N disks is 2N −1, making it an exponentially scaling problem." Figura 10: "Tower of Hanoi shows exponential growth (2N −1)".

**3.1.4 Resultados reportados:** Colapso de modelos de razonamiento en "N=7 and 8, corresponding to ∼100-200 moves". "near-perfect accuracy when solving the Tower of Hanoi with (N=5), which requires 31 moves". Para N=8 "which requires 255 moves". Para N≈10 "requiring ∼103 moves". "models achieve >50% accuracy on Tower of Hanoi instances requiring approximately ∼102 moves". Modelo con primer fallo: "around move 100 for (N=10)". DeepSeek-R1 con muestreo "maintains 18.2% accuracy at N=8 and delays collapse until N=9"; con temperatura 0 "collapses at N=8". Se removió "N>12 from the experiments on this puzzle."

**3.1.5 Fallas metodológicas si las menciona:** En "Response to Main Criticisms" se reconoce: "To account for context limit concerns for large values of N in Tower of Hanoi, we have removed N>12 from the experiments on this puzzle."

**3.1.6 Criterios de resolubilidad (fórmulas exactas):** Movimiento mínimo "2N −1". "we focus on solution correctness rather than optimality, assessing each of the move's validity and the model's ability to reach the target state as the success criteria."

### 3.2 CHECKER JUMPING (Checkers Jumping)

**3.2.1 Descripción exacta:** "Checker Jumping is a one-dimensional puzzle arranging red checkers, blue checkers, and a single empty space in a line. The objective is to swap the positions of all red and blue checkers, effectively mirroring the initial configuration." Apéndice: "N red checkers are positioned on the left side, followed by an empty space in the middle, and N blue checkers on the right side, forming a linear board of length 2N + 1."

**3.2.2 Reglas exactas:** "Valid moves include sliding a checker into an adjacent empty space or jumping over exactly one checker of the opposite color to land in an empty space. No checker can move backward in the puzzle process." Apéndice: "(1) Slide Movement: A checker can slide forward into an adjacent empty space; and (2) Jump Movement: A checker can jump forward over exactly one checker of the opposite color to land in an empty space." "red checkers can only move rightward, and blue checkers can only move leftward".

**3.2.3 Fórmula matemática de dificultad/nº de movimientos:** "with 2n checkers, the minimum number of moves required will be (n + 1)2 −1" (es decir, (N+1)^2 − 1). Apéndice: "with N checkers of each color, the minimum solution requires (N + 1)2 −1 moves, creating a quadratic relationship". Figura 10: "Checker Jumping displays quadratic scaling ((N + 1)2 −1)".

**3.2.4 Resultados reportados:** "Checker Jumping (24 moves, N=4)". En análisis QwQ-32B/Qwen2.5-32B: "collapse points occur around... N = 2 for Checker Jumping". Se prueba experimento "Algorithm Given" vs "Default" (Figura 8) sin mejora.

**3.2.5 Fallas metodológicas:** [NO MENCIONADO EN EL TEXTO] (no se reconocen fallas específicas para este puzzle).

**3.2.6 Criterios de resolubilidad (fórmulas exactas):** Movimiento mínimo "(N + 1)2 −1". "evaluating each move against the puzzle constraints and confirming that the final state matches the goal configuration."

### 3.3 RIVER CROSSING

**3.3.1 Descripción exacta:** "River Crossing is a constraint satisfaction planning puzzle involving n actors and their corresponding n agents who must cross a river using a boat. The goal is to transport all 2n individuals from the left bank to the right bank." Apéndice: "This puzzle is a generalization of classic problems such as the Missionaries and Cannibals problem and the Bridge and Torch problem, which have been widely studied in planning literature [47, 48]." Actores "a1, a2, ..., aN" y agentes "A1, A2, ..., AN".

**3.3.2 Reglas exactas:** "The boat can carry at most k individuals and cannot travel empty. Invalid situations arise when an actor is in the presence of another agent without their own agent present, as each agent must protect their client from competing agents." Apéndice: "(1) Boat Capacity Constraint: The boat can carry at most k individuals at a time, where k is typically set to 2 for smaller puzzles (N ≤3) and 3 for larger puzzles; (2) Non-Empty Boat Constraint: The boat cannot travel empty and must have at least one person aboard; (3) Safety Constraint: An actor cannot be in the presence of another agent unless their own agent is also present... This safety constraint applies both on the banks and in the boat."

**3.3.3 Fórmula matemática de dificultad/nº de movimientos:** No se da fórmula cerrada. Capacidad del bote: "For n = 2, n = 3 pairs, we use boat capacity of k = 2 and for larger number of pairs we use k = 3." Datos puntuales: "N=3, which has a solution of 11 moves" / "a valid 11-move (N=3) River Crossing solution". Figura 10: "The River Crossing and Blocks World puzzles show more moderate, near-linear growth with N."

**3.3.4 Resultados reportados:** "the model can only produce a valid solution until move 4". "it fails to solve the River Crossing puzzle when (N=3), which has a solution of 11 moves". "performing up to 100 correct moves in Tower of Hanoi but only 4 in River Crossing". En QwQ-32B/Qwen: "N = 3 for River Crossing". Para N≥6: "the optimal boat capacity (k = 4) fundamentally changes the problem structure".

**3.3.5 Fallas metodológicas si las menciona:** "we found that the puzzle dynamics shift considerably for N≥6, where the optimal boat capacity (k = 4) fundamentally changes the problem structure, making it less suitable for evaluating planning capabilities. This insight led us to refine our analysis by focusing on the cases where N<6."

**3.3.6 Criterios de resolubilidad (fórmulas exactas):** No hay fórmula explícita. "the complete crossing sequences are verified that all 2N individuals successfully reach the right bank." Capacidad k=2 (N≤3) y k=3 (N mayor).

### 3.4 BLOCKS WORLD

**3.4.1 Descripción exacta:** "Blocks World is a block-stacking puzzle requiring rearrangement of blocks from an initial configuration into a specified goal configuration. The objective is to find the minimum number of moves needed for this transformation." Apéndice: "The puzzle involves multiple stacks of blocks (A, B, C, etc.) that must be rearranged from an initial configuration to a specified goal configuration."

**3.4.2 Reglas exactas:** "Valid moves are restricted to the topmost block of any stack, which can be placed either on an empty stack or on top of another block." Apéndice: "(1) Top Block Movement: Only the topmost block from any stack can be moved; and (2) Valid Placement: A block can only be placed either on an empty position or on top of another block."

**3.4.3 Fórmula matemática de dificultad/nº de movimientos:** No fórmula cerrada. "As N increases, the state space grows factorially, and the minimum solution length increases approximately linearly." Figura 10: crecimiento "near-linear growth with N." Ejemplos: N=4 inicial [["A", "B"], ["C", "D"], []] → meta [["D", "B", "C", "A"], [], []]; N=6 inicial [["A", "B", "C"], ["D", "E", "F"], []] → meta [["F", "C", "E", "B", "D", "A"], [], []].

**3.4.4 Resultados reportados:** "Blocks World with N ≥30" como régimen de colapso. DeepSeek-R1: con temperatura 0 "collapses at N=4"; con muestreo "maintains 44.1% accuracy at N=4 and delays collapse until N=30". En QwQ-32B/Qwen: "N = 10 for Blocks World".

**3.4.5 Fallas metodológicas si las menciona:** [NO MENCIONADO EN EL TEXTO].

**3.4.6 Criterios de resolubilidad (fórmulas exactas):** No fórmula. "the complete solution sequences of block movements are processed and verified that the resulting configuration matches the target goal state."

### 3.5 OTROS BENCHMARKS (matemáticos, usados para comparación, no puzzles)
- "MATH500 [42]" / "MATH-500".
- "AIME24 [43]".
- "AIME25".
Citas: "on the MATH500 dataset, the pass@k performance of thinking models is comparable to their non-thinking counterparts when provided with the same inference token budget. However, we observed that this performance gap slightly widens on the AIME24 benchmark and widens further on AIME25." "human performance on AIME25 was actually higher than on AIME24 [44, 45], suggesting that AIME25 might be less complex."

---

## BLOQUE 4 — METODOLOGÍA

**4.1 Modelos usados (nombres y versiones exactos):**
- "Claude 3.7 Sonnet (thinking/non-thinking)" / "Claude-3.7-Sonnet (with vs. without thinking)" / "claude-3-7-sonnet-thinking", "claude-3-7-sonnet-no-thinking".
- "DeepSeek-R1" y "DeepSeek-V3" (par "DeepSeek (R1 vs. V3)").
- "DeepSeek-R1-Distill-Qwen-32B".
- "o3-mini" — "o3-mini (medium and high configurations)" / "o3-mini (medium)", "o3-mini (high)".
- "QwQ-32B" vs "Qwen2.5-32B" (también escrito "Qwen-32B") — en Apéndice A.6.
- Cinco modelos de razonamiento evaluados: "o3-mini (medium and high configurations), DeepSeek-R1, DeepSeek-R1-Distill-Qwen-32B, and Claude-3.7-Sonnet (thinking)." (cuenta a o3-mini medium/high como configuraciones, totalizando "five thinking models").

**4.2 Justificación de la elección:** "We chose these models because they allow access to the thinking traces, unlike models such as OpenAI's o-series." / "We specifically selected Claude 3.7 Sonnet (thinking/non-thinking) and DeepSeek-R1/V3 due to their ability to provide access to intermediate reasoning traces (thinking tokens), a critical requirement for our analysis. For experiments focused solely on final accuracy metrics, we also included results from OpenAI's o3-mini models."

**4.3 Cada estrategia experimental con su nombre:**
1. Comparación pass@k en benchmarks matemáticos (Fig. 2): reasoning vs non-reasoning bajo igual presupuesto de cómputo de inferencia.
2. "Three Regimes of Complexity" (Sec. 4.2.1) — comparación pares thinking/non-thinking en puzzles (Fig. 4, Fig. 5).
3. "Collapse of Reasoning Models" (Sec. 4.2.2) — cinco modelos de razonamiento (Fig. 6).
4. Análisis de trazas de razonamiento ("What Happens Inside the Thoughts of Reasoning Models?", Sec. 4.3) — posición y corrección de soluciones intermedias (Fig. 7).
5. "Execution of Prescribed Steps" / "Algorithm Given" (Sec. 4.4) — proveer el algoritmo en el prompt (Fig. 8, Fig. 17).
6. "First failure move" analysis (Fig. 9, 14, 15, 16).
7. "Eliminating Sampling Effects" — ablación con temperatura cero (Fig. 13).
8. Pares adicionales QwQ-32B vs Qwen2.5-32B (Apéndice A.6, Fig. 12).
9. "Reasoning Effort Dynamics" (Fig. 18).
10. "Algorithm Provision to Non-Reasoning Model" (Fig. 17).

**4.4 Para cada una — paso a paso, diferencias, parámetros:**

*4.4.a / 4.4.c Setup general:* "For Claude 3.7 Sonnet models, we allow the maximum token budget (64k)." "for DeepSeek-R1/V3 models on local servers, we allow the maximum length to be up to 64k tokens." "For each puzzle instance and complexity level, we analyze 25 samples per model." "We apply a filtering process to ensure the analyzed samples follow the requested response format". Apéndice: "we used maximum generation budget of 64,000 tokens, accessed through the API interface. Temperature is the default 1.0 for all API rus (Claude-3.7-Sonnet and o3-mini runs)." "DeepSeek-R1, DeepSeek-V3, and DeepSeek-R1-Distill-Qwen-32B are conducted on local servers with maximum generation length set to 64,000 and temperature set to 1.0." "the results are reported on 25 samples per model."

*Pipeline de extracción:* "flexible regex-based extractors", "both explicit 'moves =' patterns and alternative bracket-based solutions", "Removing comments... (text following '#'...)", "Normalizing move formats". "we employed the same tokenizer (cl100k_base) as the corresponding model to count tokens across all experiments." "duplicate solutions (identical move sequences) were filtered. In case of duplicate solutions, only the first solution is recorded for analysis."

*Análisis de trazas (Sec. 4.3):* "we focus on the reasoning traces generated by Claude-3.7-Sonnet-Thinking across our puzzle suite." Para cada solución intermedia se registró: "(1) its relative position within the reasoning trace (normalized by total thought length), (2) its correctness and specific failure move as validated by our puzzle simulators, and (3) the complexity of the corresponding problem."

*4.4.b Diferencias con métodos previos:* "Unlike earlier studies that are mostly focused on mathematical benchmarks... this work introduces controllable puzzle environments." "we move beyond only measuring the final accuracy and analyze how well these LRMs tackle problems of varying complexities". "Our work offers additional insights, such as examining pairs of reasoning/non-reasoning models (e.g., DeepSeek-R1/V3, Claude 3.7 Sonnet thinking/non-thinking)."

*Ablación de muestreo (Fig. 13):* "using temperature zero to eliminate sampling effects on solution length. These experiments used the DeepSeek-R1 reasoning model on local servers to ensure precise temperature control." Comparación "Sampling (=1)" vs "Greedy (=0)".

*Provisión de algoritmo:* "These algorithm scratchpads were appended to the standard problem prompt". Se proporcionan pseudocódigos recursivos para Tower of Hanoi y Checker Jumping (incluidos en el documento).

**4.5 Comparabilidad:** "By comparing LRMs with their standard LLM counterparts under equivalent inference compute". "Our analysis focus on matched pairs of LLMs with same model backbones, specifically Claude-3.7-Sonnet (w. vs. w/o thinking) and DeepSeek (R1 vs. V3)." "under equivalent inference token compute (averaged across all puzzles)".

**4.6 Limitaciones metodológicas reconocidas sobre sus propios métodos:**
- "they represent a narrow slice of reasoning tasks and may not capture the diversity of real-world or knowledge-intensive reasoning problems."
- "most of our experiments rely on black-box API access to the closed frontier LRMs, limiting our ability to mechanistically analyze internal states or architectural components."
- "the use of deterministic puzzle simulators assumes that reasoning can be perfectly validated step by step. However, in less structured domains, such precise validation may not be feasible, limiting the transferability of this analysis".
- Remoción de N>12 en Tower of Hanoi y enfoque en N<6 para River Crossing (ver Bloque 3).

---

## BLOQUE 5 — RESULTADOS CUANTITATIVOS

### 5.1 Benchmarks matemáticos (Fig. 2)
- **5.1.4 Métrica:** pass@k vs Inference Compute Budget (Tokens).
- **5.1.1 Valores/ejes:** MATH-500 eje pass@k 80–100; AIME24/AIME25 eje pass@k 0–100. Presupuestos hasta ~200000 tokens (Claude) / ~120000 (DeepSeek).
- **5.1.6 Patrón:** "pass@k performance of thinking models is comparable to their non-thinking counterparts" en MATH500; "this performance gap slightly widens on the AIME24 benchmark and widens further on AIME25."

### 5.2 Tres regímenes de complejidad (Fig. 4, Fig. 5)
- **5.2.5 Tres regímenes:** "(1) low-complexity tasks where standard models surprisingly outperform LRMs, (2) medium-complexity tasks where additional thinking in LRMs demonstrates advantage, and (3) high-complexity tasks where both models experience complete collapse."
- "Non-thinking models outperform in simple problems, thinking models show advantages at medium complexity, while both approaches fail at high complexity regardless of compute allocation."
- "while thinking models delay this collapse, they also ultimately encounter the same fundamental limitations as their non-thinking counterparts."

### 5.3 Colapso de modelos de razonamiento (Fig. 6)
- **5.3.4 Métricas:** "accuracy (top) and thinking token usage (bottom) across varying complexity levels."
- **5.3.5 Punto de colapso:** "accuracy progressively declines as problem complexity increases until reaching collapse (near-zero accuracy) beyond a model-specific complexity threshold."
- **5.3.7 Patrón de tokens (caída de esfuerzo):** "reasoning models initially increase their thinking tokens proportionally with problem complexity. However, upon approaching a critical threshold—which closely corresponds to their accuracy collapse point—models counterintuitively begin to reduce their reasoning effort despite increasing problem complexity. This phenomenon is most pronounced in o3-mini variants and less severe in the Claude-3.7-Sonnet (thinking) model." "despite mostly operating well below their generation length limits".

### 5.4 Análisis dentro de las trazas (Fig. 7)
- **5.4.2 Rangos de N (Tower of Hanoi, Fig. 7b):** N=1, N=2, N=3, N=4, N=5, N=6, N=7, N=8, N=10.
- **5.4.5 Regímenes por trazas:** "Simple problems (N=1-4) show early accuracy declining over time (overthinking), moderate problems (N=5-7) show slight improvement in accuracy with continued reasoning, and complex problems (N≥8) exhibit consistently near-zero accuracy, indicating complete reasoning failure."

### 5.5 Provisión de algoritmo (Fig. 8)
- "even when we provide the algorithm in the prompt—so that the model only needs to execute the prescribed steps—performance does not improve, and the observed collapse still occurs at roughly the same point on both puzzle environments."
- Rangos N (Fig. 8): Tower of Hanoi 1,3,6,9,12; Checker Jumping 1,3,6,9,12,15.

### 5.6 First failure move (Fig. 9, 14, 15)
- "in Tower of Hanoi, failure happens at below 50 moves for N = 12 but the model succeeds through more than 100 moves for N = 10".
- "for Tower of Hanoi with N≈10 (requiring ∼103 moves), failure typically occurs within the first ∼100 moves (10% of solution length); for N=8, which requires 255 moves, failure occurs around ∼40 moves (15% of solution length)." (En Apéndice A.6 también: "the first failure move typically occurs around move 50 (approximately 20% of the solution length)" para N=8.)
- "the River Crossing puzzle with N=3 requires 11 moves to solve, but the first failure move happens as early as move 4."
- "in the high-complexity regimes... e.g., Tower of Hanoi with N ≥8 and Blocks World with N ≥30, non-thinking models occasionally sustain performance deeper into the solution sequence and are able to fail at later moves than thinking-enabled variants."
- "thinking models (Claude-3.7-Sonnet with thinking and DeepSeek-R1) consistently show higher mean failure positions across all puzzles... However, the distribution shape of thinking models mostly show higher variance in the failure patterns."

### 5.7 Eliminación de muestreo (Fig. 13)
- "in Tower of Hanoi, the R1 model with temperature 0 collapses at N=8, whereas with sampling enabled, it maintains 18.2% accuracy at N=8 and delays collapse until N=9."
- "In Blocks World... the R1 model with temperature 0 collapses at N=4, whereas with sampling enabled, it maintains 44.1% accuracy at N=4 and delays collapse until N=30."

### 5.8 QwQ-32B vs Qwen2.5-32B (Fig. 12)
- **5.8.5 Puntos de colapso:** "the collapse points occur around N = 7 for Tower of Hanoi, N = 2 for Checker Jumping, N = 10 for Blocks World, and N = 3 for River Crossing."
- Rangos de ejes (Fig. 12): Tower of Hanoi 1–12 discos; Checker Jumping hasta 15; Blocks World hasta 40; River Crossing 2–5 pares. Reasoning Effort eje hasta ~20k tokens.

### 5.9 Esfuerzo de razonamiento (Fig. 18)
- "thinking token usage, i.e. reasoning effort, initially scales with problem complexity but later counterintuitively declines after reaching a model-specific complexity threshold." Modelos: "DeepSeek-R1, Claude-3.7-Sonnet-thinking, o3-mini".

### Datos transversales
- **5.X.3 Trials por configuración:** "25 samples per model" para cada instancia y nivel de complejidad.
- **5.X Token budget:** 64k (64,000) tokens máximo. Temperatura por defecto 1.0 (ablación con 0).
- **Comparación entre puzzles:** "models achieve >50% accuracy on Tower of Hanoi instances requiring approximately ∼102 moves, yet consistently fail on River Crossing or Cross Jumping puzzles with substantially lower compositional depth (∼101 moves)."

---

## BLOQUE 6 — HALLAZGOS Y CONCLUSIONES

**6.1 Cada conclusión explícita (contribuciones):**
- "We question the current evaluation paradigm of reasoning models on established math benchmarks and design a controlled experimental testbed by leveraging algorithmic puzzle environments".
- "We show that frontier LRMs (e.g., o3-mini, DeepSeek-R1, Claude-3.7-Sonnet-Thinking) still fail to develop generalizable problem-solving capabilities, with accuracy ultimately collapsing to near-zero beyond certain complexities across different environments."
- "We find that there exists a scaling limit in the LRMs' reasoning effort with respect to problem complexity, evidenced by the counterintuitive decreasing trend in the thinking tokens after specific complexity points."
- "Our findings show that as complexity increases, LRMs locate correct solutions later than incorrect ones within their thought, but beyond a complexity point, they fixate on early errors and cannot recover."
- "We uncover surprising behaviors in LRMs' ability to perform exact computation, including their failure to benefit from explicit algorithms and their inconsistent reasoning across problems and scales."
- "We identified three distinct reasoning regimes: standard LLMs outperform LRMs at low complexity, LRMs show advantage at moderate complexity, and both collapse at high complexity."

**6.2 Frases textuales más importantes:**
- "frontier LRMs face a complete accuracy collapse beyond certain complexities."
- "they exhibit a counter-intuitive scaling limit: their reasoning effort increases with problem complexity up to a point, then declines despite having an adequate token budget."
- "We found that LRMs have limitations in exact computation: they fail to use explicit algorithms and reason inconsistently across scales and problems."
- "when we provided the solution algorithm of puzzle to the models, their performance on this puzzle did not improve."
- "models sometimes fail earlier on harder instances despite requiring longer overall solutions."
- "performing up to 100 correct moves in Tower of Hanoi but only 4 in River Crossing."

**6.3 Qué confirma de trabajo previo:**
- "Our results (shown in Fig. 2) confirm that, on the MATH500 dataset, the pass@k performance of thinking models is comparable to their non-thinking counterparts when provided with the same inference token budget."
- Confirma fenómeno de "overthinking" descrito en literatura previa [30, 31, 32, 33].

**6.4 Qué refuta/matiza:**
- "Recent works [34, 33, 32] have demonstrated that in newer LRMs accuracy generally declines when thinking increases in math problems, in contrast we observe that the opposite correlation of thinking and accuracy actually depends on the problem complexity and it only happens up to some complexity threshold in controlled puzzle environments."
- "We also observe that in math datasets like MATH-500, pass@k is close for reasoning versus non-reasoning models but we observed different patterns under medium and high complexity of puzzles, which is not easily observable on established math benchmarks".

**6.5 Postura final sobre si los LRMs razonan:** El paper "raising questions about the nature for their reasoning capabilities." / "challenge some of the prevailing assumptions about LRM's capabilities." Concluye: "despite sophisticated self-reflection mechanisms learned by reinforcement learning, these models still fail to develop generalizable reasoning capabilities beyond certain complexity thresholds." [El texto plantea preguntas; no afirma categóricamente "no razonan".]

**6.6 Implicaciones filosóficas/cognitivas:**
- "As the Chinese room argument illustrates, it's entirely possible to use tools effectively without any real comprehension of the underlying problem."
- Demandas cognitivas mencionadas: "recursive thinking", "working memory management", "constraint satisfaction", "sequential planning", "spatial reasoning", "lookahead planning", "state-space exploration".
- "Their approach to handling complexity aligns more closely with the solution patterns they learned during training rather than the actual computational complexity of the problems themselves."
- Remite a "symbolic manipulation capabilities of such models [46, 6]".

---

## BLOQUE 7 — CONCEPTOS TÉCNICOS

**7.1 LLM (Large Language Models):** "Large Language Models (LLMs) have recently evolved to include specialized variants explicitly designed for reasoning tasks". "Large Language Models (LLMs) undergo multiple costly training phases using vast amounts of training data." Uso: contrapartes "non-thinking"/"standard" de los LRMs.

**7.2 LRM / Large Reasoning Model:** "Large Reasoning Models (LRMs) that generate detailed thinking processes before providing answers." "These models are new artifacts, characterized by their 'thinking' mechanisms such as long Chain-of-Thought (CoT) with self-reflection". Ejemplos dados: "OpenAI's o1/o3 [1, 2], DeepSeek-R1 [3], Claude Sonnet Thinking [4], and Gemini Thinking [5]". (También escrito una vez "Language Reasoning Models (LRMs)".)

**7.3 Chain-of-Thought (CoT):** "generating a Chain of Thought (CoT) [15, 16, 17, 18] and incorporating self-verification [19, 20, 21] prior to the final answer have been shown to improve model performance." "long chain-of-thought enabled by RL".

**7.4 Reasoning effort:** "their reasoning effort increases with problem complexity up to a point, then declines despite having an adequate token budget." Medido por: "reasoning effort (measured by inference-time thinking tokens)" / "reasoning effort (measured by inference thinking tokens)".

**7.5 Overthinking (overthinking phenomenon):** "efficiency concerns through what researchers term the 'overthinking phenomenon' [30, 31, 32, 33], where models produce verbose, redundant outputs, even after finding the solution, creating significant inference computational overhead." En el paper: "reasoning models often identify correct solutions early but inefficiently continue exploring incorrect alternatives—an 'overthinking' phenomenon."

**7.6 Three regimes / complexity regimes:** "three distinct reasoning regimes (Fig. 1, bottom)" — definidos en 6.1 y 5.2.

**7.7 Accuracy collapse / collapse:** "complete accuracy collapse beyond certain complexities." "performance collapsing to near-zero beyond a certain complexity threshold." "the model fails to recover any correct solutions within the thought and it often fixates on an early incorrect solutions, wasting the remaining thought token budget."

**7.8 Compositional depth:** "Compositional depth is the number of sequential operations (i.e., moves) required to completely solve the puzzle."

**7.9 Pass@k:** "the upper bound performance capabilities (pass@k) of these model pairs under equivalent inference token compute". (Definición formal explícita: [NO MENCIONADO EN EL TEXTO].)

**7.10 Self-correction / self-reflection:** "LRMs possess limited self-correction capabilities that, while valuable, show clear inefficiencies and scaling limitations." "sophisticated self-reflection mechanisms learned through reinforcement learning".

**7.11 Reinforcement learning with verifiable rewards:** "applying RL with verifiable rewards can significantly enhance model reasoning performance" (atribuido a DeepSeek-R1 [3]).

**7.12 Data contamination:** "often suffer from data contamination issues" — motivo para evitar benchmarks matemáticos establecidos.

---

## BLOQUE 8 — REFERENCIAS

(Solo las que aparecen citadas en el cuerpo; lista completa de referencias del paper.)

- **[1]** Aaron Jaech, Adam Kalai, et al. "Openai o1 system card." arXiv:2412.16720, 2024. Contexto: ejemplo de LRM (o1/o3).
- **[2]** OpenAI. "Introducing openai o1." Jan 2024. Contexto: o1 de OpenAI.
- **[3]** Daya Guo, Dejian Yang, et al. "Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning." arXiv:2501.12948, 2025. Contexto: ejemplo open-source de LRM, RL con recompensas verificables.
- **[4]** Anthropic. "Claude 3.7 sonnet." Feb 2025. Contexto: Claude Sonnet thinking.
- **[5]** Google. "Gemini flash thinking." Google AI Blog, Jan 2025. Contexto: Gemini Thinking.
- **[6]** Seyed Iman Mirzadeh, Keivan Alizadeh, Hooman Shahrokhi, Oncel Tuzel, Samy Bengio, Mehrdad Farajtabar. "GSM-symbolic: Understanding the limitations of mathematical reasoning in large language models." ICLR 2025. Contexto: pattern matching, manipulación simbólica.
- **[7]** Emily M Bender, Timnit Gebru, Angelina McMillan-Major, Shmargaret Shmitchell. "On the dangers of stochastic parrots..." ACM FAccT, pp. 610–623, 2021. Contexto: debate sobre inteligencia/razonamiento de LLMs.
- **[8]** Francois Chollet, Mike Knoop, Gregory Kamradt, Bryan Landers, Henry Pinkard. "Arc-agi-2: A new challenge for frontier ai reasoning systems." arXiv:2505.11831, 2025. Contexto: debate de razonamiento.
- **[9]** Marah I Abdin, et al. "Phi-3 technical report..." CoRR abs/2404.14219, 2024. Contexto: iteraciones tempranas de LLMs.
- **[10]** Albert Q. Jiang, et al. "Mistral 7b." CoRR abs/2310.06825, 2023. Contexto: iteraciones tempranas.
- **[11]** Abhimanyu Dubey, et al. "The llama 3 herd of models." CoRR abs/2407.21783, 2024. Contexto: iteraciones tempranas.
- **[12]** Nouha Dziri, et al. "Faith and fate: Limits of transformers on compositionality." NeurIPS 2023. Contexto: bajo desempeño en benchmarks de razonamiento; entornos controlables.
- **[13]** R. Thomas McCoy, Shunyu Yao, Dan Friedman, Matthew Hardy, Thomas L. Griffiths. "Embers of autoregression..." 2023. Contexto: limitaciones de razonamiento.
- **[14]** Marianna Nezhurina, Lucia Cipolina-Kun, Mehdi Cherti, Jenia Jitsev. "Alice in wonderland: Simple tasks showing complete reasoning breakdown..." arXiv:2406.02061, 2024. Contexto: limitaciones de razonamiento.
- **[15]** Jason Wei, et al. "Chain-of-thought prompting elicits reasoning in large language models." NeurIPS 2022. Contexto: CoT.
- **[16]** Mehran Kazemi, Najoung Kim, Deepti Bhatia, Xin Xu, Deepak Ramachandran. "Lambada: Backward chaining..." arXiv:2212.13894, 2022. Contexto: CoT.
- **[17]** Hattie Zhou, et al. "Teaching algorithmic reasoning via in-context learning." arXiv:2211.09066, 2022. Contexto: CoT.
- **[18]** Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, Yusuke Iwasawa. "Large language models are zero-shot reasoners." NeurIPS 35:22199–22213, 2022. Contexto: CoT.
- **[19]** Yixuan Weng, et al. "Large language models are better reasoners with self-verification." Findings EMNLP 2023, pp. 2550–2575. Contexto: self-verification.
- **[20]** Yifei Li, et al. "Making language models better reasoners with step-aware verifier." ACL 2023, pp. 5315–5333. Contexto: self-verification.
- **[21]** Eric Zhao, Pranjal Awasthi, Sreenivas Gollapudi. "Sample, scrutinize and scale..." arXiv:2502.01839, 2025. Contexto: self-verification.
- **[22]** Eric Zelikman, Yuhuai Wu, Jesse Mu, Noah Goodman. "STaR: Bootstrapping reasoning with reasoning." NeurIPS 2022. Contexto: enseñar a pensar vía SL/RL.
- **[23]** Sachin Goyal, et al. "Think before you speak: Training language models with pause tokens." ICLR 2024. Contexto: SL/RL.
- **[24]** David Herel, Tomas Mikolov. "Thinking tokens for language modeling." ArXiv abs/2405.08644, 2024. Contexto: SL/RL.
- **[25]** Zhihong Shao, et al. "Deepseekmath: Pushing the limits of mathematical reasoning..." 2024. Contexto: SL/RL.
- **[26]** Amirhossein Kazemnejad, et al. "Vineppo: Unlocking rl potential for llm reasoning..." 2024. Contexto: SL/RL.
- **[27]** Nathan Lambert, et al. "Tülu 3: Pushing frontiers in open language model post-training." ArXiv abs/2411.15124, 2024. Contexto: SL/RL.
- **[28]** Yanda Chen, et al. "Reasoning models don't always say what they think." arXiv:2505.05410, 2025. Contexto: discrepancia entre trazas y respuesta final.
- **[29]** Dacheng Li, et al. "Llms can easily learn to reason from demonstrations structure, not content, is what matters!" arXiv:2502.07374, 2025. Contexto: discrepancia traza/respuesta.
- **[30]** Xingyu Chen, et al. "Do not think that much for 2+ 3=? on the overthinking of o1-like llms." arXiv:2412.21187, 2024. Contexto: overthinking.
- **[31]** Yang Sui, et al. "Stop overthinking: A survey on efficient reasoning for large language models." arXiv:2503.16419, 2025. Contexto: overthinking.
- **[32]** Sara Vera Marjanović, et al. "Deepseek-r1 thoughtology: Let's think about llm reasoning." arXiv:2504.07128, 2025. Contexto: overthinking; relación thinking-accuracy.
- **[33]** Yuxiao Qu, et al. "Optimizing test-time compute via meta reinforcement fine-tuning." arXiv:2503.07572, 2025. Contexto: overthinking; thinking-accuracy.
- **[34]** Marthe Ballon, Andres Algaba, Vincent Ginis. "The relationship between reasoning and performance in large language models–o3 (mini) thinks harder, not longer." arXiv:2502.15631, 2025. Contexto: accuracy declina al aumentar thinking en math.
- **[35]** Yang Yue, et al. "Does reinforcement learning really incentivize reasoning capacity in llms beyond the base model?" arXiv:2504.13837, 2025. Contexto: pass@k converge; comparación RL vs base.
- **[36]** Nikola Zubić, et al. "Limits of deep learning: Sequence modeling through the lens of complexity theory." arXiv:2405.16674, 2024. Contexto: entornos controlables teóricos.
- **[37]** Benjamin Estermann, et al. "Puzzles: A benchmark for neural algorithmic reasoning." 2024. Contexto: entornos controlables empíricos.
- **[38]** Karthik Valmeekam, Alberto Olmo Hernandez, Sarath Sreedharan, Subbarao Kambhampati. "Large language models still can't plan (A benchmark for llms on planning and reasoning about change)." CoRR abs/2206.10498, 2022. Contexto: Blocks World; entornos controlables.
- **[39]** Anian Ruoss, et al. "Lmact: A benchmark for in-context imitation learning..." arXiv:2412.01441, 2024. Contexto: o1 mejora en puzzles/decisión.
- **[40]** Karthik Valmeekam, Kaya Stechly, Subbarao Kambhampati. "Llms still can't plan; can lrms? a preliminary evaluation of openai's o1 on planbench." 2024. Contexto: o1 mejora; Blocks World.
- **[41]** Wenjie Ma, et al. "Reasoning models can be effective without thinking." arXiv:2504.09858, 2025. Contexto: comparación pass@k thinking/non-thinking.
- **[42]** Hunter Lightman, et al. "Let's verify step by step." arXiv:2305.20050, 2023. Contexto: benchmark MATH500.
- **[43]** Mathematical Association of America. "American invitational mathematics examination (aime)." URL: https://maa.org/math-competitions/american-invitational-mathematics-examination-aime , 2025. Accessed: 2025-05-15. Contexto: AIME24.
- **[44]** Art of Problem Solving. "Amc historical results - aime i (february 1, 2024)." URL: https://artofproblemsolving.com/wiki/index.php/AMC_historical_results#AIME_I_.28February_1.2C_2024.29 , 2024. Accessed: 2025-05-15. Contexto: desempeño humano AIME24.
- **[45]** Art of Problem Solving. "Amc historical results – aime i (february 6, 2025)." URL: https://artofproblemsolving.com/wiki/index.php/AMC_historical_results#AIME_I_.28February_6.2C_2025.29 , 2025. Accessed: 2025-05-15. Contexto: desempeño humano AIME25.
- **[46]** Gary F Marcus. "The algebraic mind: Integrating connectionism and cognitive science." MIT press, 2003. Contexto: manipulación simbólica.
- **[47]** Saul Amarel. "On representations of problems of reasoning about actions." In Readings in artificial intelligence, pp. 2–22. Elsevier, 1981. Contexto: literatura de planificación (River Crossing).
- **[48]** Günter Rote. "Crossing the bridge at night." Bulletin of the EATCS, 78:241, 2002. Contexto: Bridge and Torch (River Crossing).
- **[49]** Xinran Zhao, et al. "Improving large language model planning with action sequence similarity." arXiv:2505.01009, 2025. Contexto: diseño de Blocks World.
- **[50]** Xiaomin Li, et al. "When thinking fails: The pitfalls of reasoning for instruction-following in llms." arXiv:2505.11423, 2025. Contexto: RL puede afectar instruction-following.

---

## BLOQUE 9 — FIGURAS Y TABLAS

(El documento no contiene tablas numeradas. Solo figuras.)

- **Figura 1:** Pie: "Top: Our setup enables verification of both final answers and intermediate reasoning traces... Bottom left & middle: At low complexity, non-thinking models are more accurate and token-efficient. As complexity increases, reasoning models outperform but require more tokens—until both collapse beyond a critical threshold, with shorter traces. Bottom right: For correctly solved cases, Claude 3.7 Sonnet (Thinking) tends to find answers early at low complexity and later at higher complexity. In failed cases, it often fixates on an early wrong answers, wasting the remaining token budget." Variables: Accuracy(%), Reasoning Effort (Tokens), Position Within Thoughts, Complexity (number of disks) 1–12. Conclusión: ineficiencias en el proceso de razonamiento.

- **Figura 2:** Pie: "Comparative analysis of reasoning (thinking) versus non-reasoning (no-thinking) model variants across math benchmarks reveals inconsistent performance patterns." Variables: pass@k vs Inference Compute Budget (Tokens), MATH-500/AIME24/AIME25, claude-3-7-sonnet thinking/no-thinking, DeepSeek-R1/V3.

- **Figura 3:** Pie: "Illustration of the four puzzle environments. Rows show the progression from initial state (top) through intermediate state (middle) to target state (bottom) for puzzles: Tower of Hanoi (disk transfer across pegs), Checkers Jumping (position swapping of colored tokens), River Crossing (transporting entities across a river), and Blocks World (stack reconfiguration)."

- **Figura 4:** Pie: "Pass@k performance of thinking models (Claude 3.7 Sonnet with extended thinking, DeepSeek-R1) versus their non-thinking counterparts (Claude 3.7 Sonnet, DeepSeek-V3) across equivalent inference compute budgets in puzzle environments of low, medium, and high complexity. Non-thinking models outperform in simple problems, thinking models show advantages at medium complexity, while both approaches fail at high complexity regardless of compute allocation."

- **Figura 5:** Pie: "Accuracy of thinking models (Claude 3.7 Sonnet with extended thinking, DeepSeek-R1) versus their non-thinking counterparts (Claude 3.7 Sonnet, DeepSeek-V3) across all puzzle environments and varying levels of problem complexity."

- **Figura 6:** Pie: "Accuracy and thinking tokens versus problem complexity for reasoning models across puzzle environments. As complexity increases, reasoning models initially spend more tokens while accuracy declines gradually, until a critical point where reasoning collapses—performance drops sharply and reasoning effort counterintuitively decreases."

- **Figura 7:** Pie: "(a) Position and correctness of intermediate solutions within reasoning traces across four puzzles at varying complexity levels. ✓indicates correct solutions, ✗indicates incorrect solutions, with distribution density shown by shading; (b) Solution accuracy versus position in thinking for Tower of Hanoi at different complexity levels. Simple problems (N=1-4) show early accuracy declining over time (overthinking), moderate problems (N=5-7) show slight improvement in accuracy with continued reasoning, and complex problems (N≥8) exhibit consistently near-zero accuracy, indicating complete reasoning failure."

- **Figura 8:** Pie: "Performance comparison between default problem-solving and algorithm-guided execution across Tower of Hanoi and Checker Jumping puzzles. Even when given the solution algorithm and only needing to execute prescribed steps, failures occur at similar points, highlighting reasoning models' limitations in following logical procedures." (DeepSeek-R1 y Claude-3.7-Sonnet +thinking, "Algorithm Given" vs "Default".)

- **Figura 9:** Pie: "First failure move versus problem complexity for Claude 3.7 Sonnet (thinking) across four puzzle environments."

- **Figura 10:** Pie: "Compositional depth (number of moves required) across different problem sizes for our four puzzle environments." Variables: Compositional Depth (# of Moves) vs Problem Size (N) 1–6.

- **Figura 11:** Pie: "Inference compute (tokens) and accuracy versus compositional depth (number of required moves) across puzzle environments for DeepSeek-R1 and Claude-3.7-Sonnet (thinking)."

- **Figura 12:** Pie: "Comparison of reasoning ('thinking') and non-reasoning ('non-thinking') models for the QwQ-32B and Qwen2.5-32B backbone pair across all the controlled puzzle environments. Top: task accuracy (%)... Bottom: reasoning effort (measured by the number of thinking tokens) versus problem complexity. Shaded regions correspond to the three observed regimes... low-complexity, mid-complexity, and high-complexity..." Conclusión: "QwQ-32B demonstrates an initial advantage in the mid-complexity regime but ultimately exhibits collapse behavior at higher complexity levels with the counterintuitive decrease of reasoning effort after the collapse."

- **Figura 13:** Pie: "Performance comparison of the DeepSeek-R1 model with sampling versus greedy generations (temperature=0) across all puzzles."

- **Figura 14:** Pie: "The first failure move versus problem complexity (N) comparison for thinking and non-thinking models across puzzle environments. Top: Claude-3.7-Sonnet comparison; Bottom: DeepSeek-R1 vs DeepSeek-V3."

- **Figura 15:** Pie: "The first failure move versus problem complexity (N) comparison for o3-mini model variants across puzzle environments." (o3-mini medium / high.)

- **Figura 16:** Pie: "Density distribution of first failure moves for thinking and non-thinking models across puzzle environments. Top: Claude-3.7-Sonnet comparison; Bottom: DeepSeek-R1 vs DeepSeek-V3."

- **Figura 17:** Pie: "Effect of algorithm provision on both reasoning (thinking) and non-reasoning (non-thinking) models (DeepSeek R1 vs V3) across the Tower of Hanoi and Checker Jumping puzzles. 'Default' denotes the original task prompt, while 'Algorithm Given' includes the explicit step-by-step solving procedure in the input."

- **Figura 18:** Pie: "Detailed results on reasoning effort (measured in inference thinking tokens) versus problem complexity (N) for three LRMs (DeepSeek-R1, Claude-3.7-Sonnet with thinking, and o3-mini) across four puzzle environments." Variables: "Green dots indicate correct solutions, red crosses show incorrect ones, and blue lines track average thinking token usage at each complexity level (N)".

---

## BLOQUE 10 — GAPS Y TRABAJO FUTURO

**10.1 Limitaciones reconocidas:** (sección "Limitations")
- "they represent a narrow slice of reasoning tasks and may not capture the diversity of real-world or knowledge-intensive reasoning problems."
- "most of our experiments rely on black-box API access to the closed frontier LRMs, limiting our ability to mechanistically analyze internal states or architectural components."
- "the use of deterministic puzzle simulators assumes that reasoning can be perfectly validated step by step. However, in less structured domains, such precise validation may not be feasible, limiting the transferability of this analysis to other more generalizable and open-ended reasoning."

**10.2 Trabajo futuro:**
- "suggesting that further research might be needed to better understand the symbolic manipulation capabilities of such models [46, 6]."
- "we presented some of our surprising observations on LRMs that lead to several open questions for future research."
- "We hope that these findings can pave the way for future investigations into better understanding the reasoning process of these systems."

**10.3 Preguntas abiertas:** (Sec. 4.4 "Open Questions" y planteadas en Introducción)
- "Are these models capable of generalizable reasoning, or are they leveraging different forms of pattern matching [6]?"
- "How does their performance scale with increasing problem complexity?"
- "How do they compare to their standard LLM (non-reasoning) counterparts when provided with the same inference token compute?"
- "what are the inherent limitations of current reasoning approaches, and what improvements might be necessary to advance toward more robust reasoning capabilities?"
- Por qué los modelos no mejoran al recibir el algoritmo; por qué fallan antes en instancias más difíciles; secuencias libres de error muy distintas entre puzzles.

**10.4 Código/recursos (URLs exactas):** [NO MENCIONADO EN EL TEXTO] — no se proporciona URL de repositorio de código ni recursos descargables. (Las únicas URLs presentes son las de refs. [43], [44], [45], listadas en Bloque 8.)

---

## VERIFICACIÓN — 5 datos más difíciles de encontrar (con cita textual)

1. **Tokenizador usado para conteo de posiciones:** "we employed the same tokenizer (cl100k_base) as the corresponding model to count tokens across all experiments."

2. **Cifras de accuracy en la ablación de temperatura (Blocks World):** "the R1 model with temperature 0 collapses at N=4, whereas with sampling enabled, it maintains 44.1% accuracy at N=4 and delays collapse until N=30." (y Tower of Hanoi: "maintains 18.2% accuracy at N=8 and delays collapse until N=9.")

3. **Cambio de capacidad de bote en River Crossing para N≥6:** "for N≥6, where the optimal boat capacity (k = 4) fundamentally changes the problem structure, making it less suitable for evaluating planning capabilities."

4. **Puntos de colapso exactos del par QwQ-32B / Qwen2.5-32B:** "the collapse points occur around N = 7 for Tower of Hanoi, N = 2 for Checker Jumping, N = 10 for Blocks World, and N = 3 for River Crossing."

5. **Temperatura por defecto y presupuesto de generación:** "we used maximum generation budget of 64,000 tokens, accessed through the API interface. Temperature is the default 1.0 for all API rus (Claude-3.7-Sonnet and o3-mini runs)."

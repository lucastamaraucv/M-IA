# EXTRACCIÓN ACADÉMICA — "Faith and Fate: Limits of Transformers on Compositionality"

> Extracción literal del documento. Solo se incluye lo que el texto dice explícitamente. Las citas textuales van entre comillas dobles "...". Donde un sub-ítem no aparece en el texto se indica [NO MENCIONADO EN EL TEXTO].

---

## BLOQUE 1 — IDENTIDAD DEL DOCUMENTO

**1.1 Título completo (palabra por palabra)**
"Faith and Fate: Limits of Transformers on Compositionality"

**1.2 Autores en orden**
"Nouha Dziri", "Ximing Lu", "Melanie Sclar", "Xiang Lorraine Li", "Liwei Jiang", "Bill Yuchen Lin", "Peter West", "Chandra Bhagavatula", "Ronan Le Bras", "Jena D. Hwang", "Soumya Sanyal", "Sean Welleck", "Xiang Ren", "Allyson Ettinger", "Zaid Harchaoui", "Yejin Choi".
Notas del texto: "∗First co-authors." (Nouha Dziri, Ximing Lu, Melanie Sclar) y "† Second co-authors." (Xiang Lorraine Li, Liwei Jiang, Bill Yuchen Lin).

**1.3 Afiliación de cada autor**
El texto indica afiliaciones por superíndice:
- "1Allen Institute for Artificial Intelligence"
- "2University of Washington"
- "3University of Southern California"
- "4University of Chicago"
Asignación literal según superíndices: Nouha Dziri¹, Ximing Lu¹,², Melanie Sclar², Xiang Lorraine Li¹, Liwei Jiang¹,², Bill Yuchen Lin¹, Peter West¹,², Chandra Bhagavatula¹, Ronan Le Bras¹, Jena D. Hwang¹, Soumya Sanyal³, Sean Welleck¹,², Xiang Ren¹,³, Allyson Ettinger¹,⁴, Zaid Harchaoui¹,², Yejin Choi¹,².
Correos listados: "nouhad@allenai.org, ximinglu@allenai.org, msclar@cs.washington.edu".

**1.4 Fecha de publicación/envío**
"arXiv:2305.18654v3 [cs.CL] 31 Oct 2023". También: "37th Conference on Neural Information Processing Systems (NeurIPS 2023)." Las evaluaciones: "The evaluations were conducted from January 2023 to May 2023 using the OpenAI API."

**1.5 Número arXiv u otro identificador**
"arXiv:2305.18654v3 [cs.CL]".

**1.6 Fuentes de financiamiento**
"This research was supported by the NSF DMS-2134012, DARPA MCS program through NIWC Pacific (N66001-19-2-4031), and the Allen Institute for AI."

**1.7 Agradecimientos**
"We thank members of the Mosaic team at AI2 for valuable feedback on this project, as well as Agustín Santiago Gutiérrez and Kawin Ethayarajh for valuable discussions."

---

## BLOQUE 2 — CONTEXTO Y MOTIVACIÓN

**2.1 Paper previo que motiva el estudio (título, autores, año)**
El documento no declara un único "paper previo" que lo motive. La NOTA de la plantilla sobre "paper previo (Apple)" → [NO MENCIONADO EN EL TEXTO]. El texto cita como contraste la noción de "sparks of AGI": referencia [12] = "Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott M. Lundberg, Harsha Nori, Hamid Palangi, Marco Túlio Ribeiro, and Yi Zhang. Sparks of artificial general intelligence: Early experiments with GPT-4. CoRR, abs/2303.12712, 2023." La motivación general declarada: "These difficulties have motivated us to take a step back and thoroughly examine both the successes and failures of transformers from empirical and theoretical perspectives on compositional reasoning tasks."

**2.2 Hallazgos exactos de ese paper previo según ESTE documento**
El texto solo dice que modelos como ChatGPT y GPT4 fueron "even noted as “sparks of AGI” [12]." No reporta hallazgos detallados de un paper previo específico. [NO MENCIONADO EN EL TEXTO] (más allá de la frase citada).

**2.3 Controversia que generó según este documento**
El documento plantea la tensión, no una "controversia" atribuida a un paper: "The striking discrepancy between the impressive successes of transformer LLMs on seemingly complex tasks and the astonishing failures on seemingly trivial tasks spark critical open questions about how to faithfully interpret their mixed capabilities." [AMBIGUO en cuanto a "controversia" como tal].

**2.4 Posiciones del debate según este documento (cita cada una y quién la sostiene)**
No se estructura como "debate" con bandos atribuidos. El texto presenta dos hipótesis propias: "First, transformers solve compositional tasks by reducing multi-step compositional reasoning into linearized path matching." y "Second, due to error propagation, transformers may have inherent limitations on solving high-complexity compositional tasks that exhibit novel patterns." Posiciones contrastadas citadas en el texto: capacidades "even outperforming humans in certain cases [79, 28, 15, 85]" atribuidas al "scaling effect [38, 33, 1]"; frente a estudios que muestran que "these models have also been shown to struggle across multiple domains [32]". [NO MENCIONADO EN EL TEXTO] un debate con posiciones nominalmente atribuidas.

**2.5 Medios de comunicación mencionados y qué dijeron**
[NO MENCIONADO EN EL TEXTO].

**2.6 Objetivo declarado de ESTE paper**
"we investigate the limits of these models across three representative compositional tasks—multi-digit multiplication, logic grid puzzles, and a classic dynamic programming problem." También: "Our work takes a realistic look at the limitations of transformers in the context of compositional tasks." Y: "our work explores the fundamental limits of vanilla transformers in achieving full mastery, striving for 100% performance in both in-domain and OOD settings."

**2.7 Qué dice el paper que NO pretende hacer**
Sobre grokking: "In this present work, our aim is not to explain grokking but rather to observe its emergence." Sobre mapas no lineales: "similar behaviors, possibly even more acute, could occur with nonlinear maps [25]—but their study is beyond the scope of this paper." Sobre el alcance: "We focus on out-of-the-box transformers to align with the scope of our experiments and with the goal of framing empirical results." Sobre límites: "we are unable to push the empirical limits of transformers even further in terms of training data size and number of epochs."

---

## BLOQUE 3 — BENCHMARKS Y PUZZLES

El documento estudia tres tareas: Multiplicación, Einstein's Puzzle (logic grid puzzle) y un problema de Programación Dinámica.

### 3.1 Multiplication (Multi-digit multiplication / long-form multiplication)

**3.1.1 Descripción exacta según el texto**
"Multi-digit multiplication requires executing operations with numerical symbols based on procedural rules [34]." "we use the well-known O(k1k2) long-form multiplication algorithm for computing x · y, where x has k1 ≤5 digits and y has k2 ≤5 digits in base 10."

**3.1.2 Reglas exactas**
Prompt few-shot: "To multiply two numbers, start by multiplying the rightmost digit of the multiplicand by each digit of the multiplier, writing down the products and carrying over any remainders. Repeat this process for each digit of the multiplicand, and then add up all the partial products to obtain the final result."
Primitivas: "let FA = {one-digit multiplication, sum, mod 10, carry over, concatenation}. Source nodes S are digits of input numbers, leaf node o is the final output, and intermediate nodes v are partial results generated during execution of the long-form multiplication algorithm".
Construcción de datos: "We focus on multiplications of two numbers x = (x1, x2, . . . , xk) and y = (y1, y2, . . . , yk) where each number can have up to k digits, amounting to 9 × 10(k−1) combinations per each number. We set k to 5 in our experiments."

**3.1.3 Fórmula matemática de dificultad si se menciona**
Complejidad del algoritmo: "O(k1k2)". Combinaciones por número: "9 × 10(k−1)". (Métricas de complejidad del grafo en Bloque 7.)

**3.1.4 Resultados reportados por el paper previo si aplica**
No aplica (no hay paper previo con resultados para esta tarea). El propio documento reporta: "off-the-shelf ChatGPT and GPT4 achieve only 55% and 59% accuracies on this task, respectively (§3)" (3-dígitos por 3-dígitos).

**3.1.5 Problemas/fallas metodológicas identificadas en el paper previo según este documento**
[NO MENCIONADO EN EL TEXTO].

**3.1.6 Criterios matemáticos de resolubilidad si se mencionan (fórmulas exactas)**
Corolario D.1: "the probability that M will solve any m digit by n digit multiplication using the long-form multiplication algorithm tends to 0 when n tends to infinity." Definición de g: "g := d ◦s", "d(x, y) := x · y", "s([x1, . . . , xm, xm+1, . . . , xm+n], j) := (x1++ x2++ . . .++ xm, xm+j)". "hn(x1, . . . , xn) := Σⁿᵢ₌₁ xi10n−i". Cota de colisión: "P(hn(X) = hn(Y ) | X ̸= Y ) < βαn for α = 0.1 and β = 10m."

### 3.2 Einstein's Puzzle (logic grid puzzle)

**3.2.1 Descripción exacta según el texto**
"Einstein's puzzle is a well-known logic puzzle often used as a benchmark for solving constraint satisfaction problems [61]. It involves a list of houses with different attributes (e.g., owner's name, pets), and the goal is to determine which attributes belong to each house by combining a set of pre-defined natural language clues or constraints."

**3.2.2 Reglas exactas**
"The solution to the puzzle is a matrix of size K × M, where K represents the number of houses and M the number of attributes."
Tipos de pistas: "1) ‘found_at’, e.g., “Alice lives in House 2”, 2) ‘same_house’... 3) ‘direct_left’... and 4) ‘besides’...". Tipos más difíciles: "‘not_at’, ‘left_of’ (not necessarily directly left of), ‘two_house_between’, etc. which are only used in auxiliary experiments."
Algoritmo (función de eliminación): "we consider a greedy algorithm that iteratively eliminates possible solutions by filling at least one cell each time. It deterministically fills the cell(s) that requires the minimum number of clues among all current unfilled cells. We refer to this as the elimination function."
Primitivas: "let FA ={elimination function}. The source nodes are the clues, all intermediate nodes are partially-filled matrices, and the output node is a fully-filled solution matrix."
Algorithm 1 (Puzzle Solver): entrada "Clues", salida "Reasoning path"; itera "while |LeftClues| 6= 0" generando "CandidateClues" y aplicando "if solve any cell then" remover y append al Path.
Generación: "the M properties are randomly selected from the candidate pool, followed by the random sampling of K values for each property... we ensure one of the sampled properties is ‘Name’". "we initially over-generate all valid clues based on the solution and subsequently remove redundant clues at random until we obtain a set with a unique solution".
Solver de grafo: "we use existing puzzle solvers [21] to generate the computation graph." (referencia [21] = Z3 SMT solver).

**3.2.3 Fórmula matemática de dificultad si se menciona**
Tamaño de la solución "K × M". [Sin fórmula de dificultad adicional explícita más allá de las métricas de grafo del Bloque 7.]

**3.2.4 Resultados reportados por el paper previo si aplica**
[NO MENCIONADO EN EL TEXTO].

**3.2.5 Problemas/fallas metodológicas identificadas en el paper previo según este documento**
[NO MENCIONADO EN EL TEXTO].

**3.2.6 Criterios matemáticos de resolubilidad si se mencionan (fórmulas exactas)**
Corolario D.3 / Lemma D.2 aplican la función de eliminación como "f m": "Let x = (c1, . . . , cn, E) where E is an empty matrix of size K × M (all cell values of E are ø). Then, a full solution is computed as f m(x) for some value of m that increases with the problem size. In contrast to other tasks, the value of m is not fixed, and depends on the task instance".

### 3.3 Dynamic Programming Problem (DP)

**3.3.1 Descripción exacta según el texto**
"We analyze a classic relaxation of the NP-complete Maximum Weighted Independent Set problem [39]: Given a sequence of integers, find a subsequence with the highest sum, such that no two numbers in the subsequence are adjacent in the original sequence. This relaxation may be solved in O(n) time using DP."

**3.3.2 Reglas exactas**
Restricción de valores: "we restrict each integer to the [−5, 5] range." Salida: "Output a list with "1" for chosen numbers and "2" for unchosen ones. If multiple solutions exist, select the lexicographically smallest."
Primitivas: "let FA = {equals, and, not, indicator function, sum, max}. Source nodes are elements of the input list, and the output node is a list that for each element indicates whether it should be selected."
Recursión: "dpi = max(dpi+1, ai + dpi+2, 0)" con casos base "dpn = max(an, 0)" y "dpn−1 = max(an, an−1, 0)".
Reconstrucción: "we choose an item if and only if dpi = ai + dpi+2 ... and we have not chosen the previous element." Para i=n−1 y i=n: "we choose the element if dpi = ai ... and we have not chosen the immediately previous element."

**3.3.3 Fórmula matemática de dificultad si se menciona**
"O(n) time". Total de listas: "11n lists for an input list of size n". (En texto: "giving a total of 11n lists" — léase como 11ⁿ por el rango de 11 valores.)

**3.3.4 Resultados reportados por el paper previo si aplica**
[NO MENCIONADO EN EL TEXTO].

**3.3.5 Problemas/fallas metodológicas identificadas en el paper previo según este documento**
[NO MENCIONADO EN EL TEXTO].

**3.3.6 Criterios matemáticos de resolubilidad si se mencionan (fórmulas exactas)**
Corolario D.3: "dp's computation may be viewed as f m−2(x) for a list of size m"; reconstrucción "may be viewed as f m(x)". Recursión de f: "a′i := max(a′i+1, ai + a′i+2, 0)".

---

## BLOQUE 4 — METODOLOGÍA

**4.1 Modelo(s) de IA usados (nombre y versión exactos)**
"GPT3 (text-davinci-003) [11], ChatGPT (GPT-3.5-turbo) [57] and GPT4 (gpt-4) [58]". Lista completa en §B.1: "we evaluate the performance of 6 LLMs: GPT4 (gpt-4) [58], ChatGPT (GPT3.5-turbo) [57], GPT3 (text-davinci-003) [11], FlanT5 [17] and LLaMa [75]." (El texto dice "6 LLMs" pero enumera explícitamente 5; además entrena "GPT2-XL" desde cero — ver 4.6.) [AMBIGUO: "we evaluate the performance of 6 LLMs" pero lista 5.] Tamaños mencionados en figuras: "LLaMA zero-shot (13B)", "FlanT5-XXL zero-shot (11B)".

**4.2 Justificación de la elección**
Fine-tuning solo sobre GPT3: "We perform fine-tuning on GPT3 (text-davinci-003) for the three tasks". Sobre presupuesto: "We selected sizes based on budget constraints for GPT3 finetuning". Sobre grokking: "Due to budget constraints, we only experiment on the multiplication task." Elección de algoritmo O(n) en DP: "We select an O(n) algorithm since GA(x)'s size is proportional to A's complexity." Implementación DP: "We chose this implementation because the computation graph has always the same topology for any given input length."

**4.3 Cada estrategia experimental con su nombre exacto**
"zero-shot, few-shot, and finetuning techniques." Formatos: "question-answer and question-scratchpad formats for few-shot and finetuning settings". Estrategia adicional: "grokking". Concepto base: "scratchpads [56]".

**4.4 Para cada estrategia**

*Zero-shot / Few-shot:*
- 4.4.a: "we begin by analyzing models' zero-shot and few-shot performances on our compositional tasks." DP usó "five exemplars for the few-shot setup."
- 4.4.b: [NO MENCIONADO EN EL TEXTO] (no hay método de paper previo como referencia directa).
- 4.4.c: "we set nucleus sampling p to 0.7 and temperature to 1." "For each task, we evaluate the performance of each model on 500 test examples."

*Finetuning question-answer:*
- 4.4.a: "we next exhaustively finetune GPT3 with question-answer pairs."
- 4.4.b: [NO MENCIONADO EN EL TEXTO].
- 4.4.c: "We separately finetune GPT3 models on ∼1.8M multiplication pairs, ∼142K DP pairs, and ∼41K puzzle pairs". "we train separately the model for {14, 12, 4} epochs for multiplication, puzzle, and DP respectively". "leaving out 10% for validation and 10% for testing." Multiplicación: "all k1-by-k2 digit multiplications with 1 ≤k1, k2 ≤4 and k1 · k2 ≤9; and all DP problems up to 5 elements." Puzzle: "we train on a subset of all instances up to (K, M) ≤(4, 4)".

*Finetuning question-scratchpad:*
- 4.4.a: "we finetune GPT3 with question-scratchpad pairs for all tasks."
- 4.4.b: [NO MENCIONADO EN EL TEXTO].
- 4.4.c: "we train the model for {16, 8, 2} epochs for multiplication, puzzle, and DP." Multiplicación entrenada "from 1-digit by 1-digit multiplication to 3-digit by 2-digit multiplication". Hiperparámetros comunes: "The batch size is set to approximately 0.2% of the number of examples in the training set." "For the learning rate multiplier, we experiment with values ranging from 0.02 to 0.2 ... and chose 0.2."

*Grokking:*
- 4.4.a: "Following [53], we fine-tune GPT3 with question-answer pairs for 420K steps and separately finetune GPT3 with question-scratchpad pairs for 30K steps."
- 4.4.b: [NO MENCIONADO EN EL TEXTO].
- 4.4.c: "The training duration for question-answer pairs is equivalent to 60 epochs and costs 50,000 USD. Training on question-scratchpad pairs was conducted for 40 epochs and costs 40,000 USD."

**4.5 Cómo se manejó la comparabilidad con el paper previo**
[NO MENCIONADO EN EL TEXTO] (no hay paper previo replicado).

**4.6 Limitaciones metodológicas que reconoce sobre sus propios métodos**
"for the scratchpad approach, we are limited to only establishing a correlation between the model generation and its preceding context, as we cannot inspect the exact tokens model attends to when making the prediction. This limitation arises from our lack of access to the activations of the studied models." "we posit that alternative approaches to linearizing reasoning processes may yield different performances". Sobre tokenización: "One hypothesis on why the model exhibit such a poor generaliztion is tokenization. So we train GPT2-XL from scratch on up to 4x4 (90M data points), we assign each digit to one token and each math symbol as well. However, the performance is still low and GPT2-XL fails to answer correctly 3x3 test examples." Presupuesto: "due to our compute budget constraints as well as limited access to the largest language models such as GPT4".

---

## BLOQUE 5 — RESULTADOS CUANTITATIVOS

### 5.1 Zero-shot multiplicación (tendencia general)
- 5.1.1: "ChatGPT and GPT4 achieve only 55% and 59% accuracies on this task, respectively" (3-dígitos × 3-dígitos).
- 5.1.6: Figura 15 (matrices de accuracy por tamaño k1×k2, valores literales del texto):
  - ChatGPT zero-shot: fila valores "1, 1, 0.99, 0.99, 0.85", "0.55, 0.98, 0.51, 0.11, 0.01", "0.98, 0.26, 0.02, 0, 0".
  - GPT3 zero-shot: "1, 1, 0.88, 0.97, 0.41", "0.09, 0.85, 0.28, 0.04, 0", "0.76, 0.1, 0, 0, 0".
  - LLaMA zero-shot (13B): "0.6, 0.5, 0.42, 0.32, 0.19", "0.17, 0.22, 0, 0, 0", "0,0,0,0,0".
  - FlanT5-XXL zero-shot (11B): "0.96, 0.41, 0.05, 0.15, 0.02", "0, 0.15, 0,0,0", "0.07,0,0,0,0".
- 5.1.5: "Transformers' accuracy decreases to near zero as task complexity increases".

### 5.2 Few-shot multiplicación
- 5.2.1: Figura 16 (valores literales):
  - GPT4 few-shot: "1, 1, 0.98, 0.97 0.88 0.56", "0.93 0.76 0.18 0.03", "0.95 0.42 0.07 0 0".
  - ChatGPT few-shot: "1, 1, 0.99, 0.99 0.82 0.58", "0.94 0.45 0.08 0.01", "0.96 0.28 0.02 0 0".
  - GPT3 few-shot: "1, 1, 0.88, 0.97 0.49 0.09", "0.88 0.21 0.04 0", "0.8 0.17 0.03 0 0".
  - LLaMA few-shot (13B): "0.61, 0.52 0.42, 0.31 0.19 0.18", "0.22, 0,0,0,0".
  - FlanT5-XXL few-shot (11B): "0.96, 0.42 0.05, 0.14 0.02 0", "0.16,0,0,0,0", "0.08,0,0,0,0".
- 5.2.7 (patrones de tokens / costos): "each example typically consists of around 20 tokens, and 250 tokens for question-scratchpad pairs. The cost for utilizing the text-davinci-003 model amounts to $0.02 (USD) per 1,000 tokens."

### 5.3 Zero-shot puzzle
- 5.3.1: Figura 17 (valores literales por tamaño 2–6):
  - ChatGPT zero-shot (Puzzle): "0.8, 0.4, 0.1, 0.4, 0", "0.5, 0, 0.2, 0, 0", "0.1, 0, 0, 0, 0", resto ceros.
  - GPT3 zero-shot (Puzzle): "0.6, 0.5, 0.2, 0.1, 0", "0.5, 0, 0.2, 0, 0", "0.1,0,0,0,0", resto ceros.
  - LLaMa zero-shot (Puzzle): "0.44, 0.25, 0.09, 0.08, 0", "0.1, 0.02, 0.03, 0, 0", resto ceros.
  - FlanT5 zero-shot (Puzzle): "0.41, 0.22, 0.02, 0.02, 0", "0.04, 0,0,0,0", resto ceros.
- 5.3.5: "Few-shot performance led to worse performance." y "the few-shot setting did not lead to any improvement in the puzzle task."

### 5.4 DP zero-shot y five-shot
- 5.4.2: Tamaños probados "2, 4, 6, 8, 10" (Problem Size). OOD: "we use lists of sizes 6 to 10 inclusive."
- 5.4.1: Figura 20 reporta curvas para GPT4, ChatGPT, GPT3 (zero-shot y five-shot). "LLaMA and FlanT5 results are near zero for all problem sizes." (valores numéricos exactos por punto: [INCOMPLETO EN EL TEXTO] — solo dados como gráficas con ejes 0.0–0.8).

### 5.5 Finetuning question-answer (in-domain vs OOD)
- 5.5.1/5.5.2: Multiplicación: "fine-tuned on a range of multiplication problems, spanning from 1-digit by 1-digit multiplication to 4-digit by 2-digit multiplication amounting to 1.8M pairs." Puzzle: "puzzles of sizes ranging from 2x2 to 4x4 resulting in a total of 142k pairs." DP: "a sequence length of 5 resulting in 41K pairs", "the graph's depth and width were set to 18."
- 5.5.5: "high accuracy for examples with splits seen during training, i.e., in-domain. However, the performance sharply declines when evaluating unseen splits during training, i.e., out-of-domain (OOD)."
- GPT2-XL: "we train GPT2-XL from scratch on up to 4x4 (90M data points)... GPT2-XL fails to answer correctly 3x3 test examples."

### 5.6 Finetuning question-scratchpad
- 5.6.5: "GPT3 achieves near-perfect performance on in-distribution, but fails entirely in generalizing to OOD cases—in particular, wider or deeper computation graphs."

### 5.7 Grokking (solo multiplicación)
- 5.7.1/5.7.7: "fine-tune GPT3 with question-answer pairs for 420K steps and separately ... question-scratchpad pairs for 30K steps." "60 epochs and costs 50,000 USD" (QA); "40 epochs and costs 40,000 USD" (scratchpad).
- 5.7.5: "Figure 4 shows no improvement in generalization for OOD cases beyond the overfitting point".

### 5.8 Análisis de errores por capa (Figura 7)
- 5.8.5: "82.3% of the final correct answers for 4-digit by 2-digit multiplications (a setting unseen during training) had at least one error in the computation graph, but still produced correct answers." "the ratio of fully correct nodes is almost perfect but sharply decreases toward zero with increasing graph layers." "the ratio of propagation errors is usually higher than the ratio of local errors." "Both the DP and the puzzle tasks have a high ratio of restoration errors".

### 5.9 Patrones superficiales — Relative Information Gain (multiplicación, Tabla 2)
- Valores literales (RelativeIG) por tamaño 2x2/3x3/4x4/5x5:
  - "xn z2n 0.223 0.223 0.223 0.223"; "yn z2n 0.223..."; "x1 z1 0.198 0.199 0.199 0.199"; "xn yn z2n 1.000 1.000 1.000 1.000"; "x1 y1 z1 0.788 0.792 0.793 0.793"; "y1 y2 z1 0.213 0.211 0.211 0.211"; "x1 x2 z1 0.213 0.211 0.211 0.211". (z definido: "z := x · y", "z2n denotes the least-significant digit", "z1 denotes the left-most digit". "Only (input, output) pairs above 0.01 are shown.")

### 5.10 Precisión en predicciones parciales (multiplicación, Figuras 26–29)
- Métricas: "Accuracy Trailing 0", "Accuracy last digit", "Accuracy last two digits", "Accuracy # digits", "Accuracy first digit", "Accuracy first two digits". (Matrices de valores por tamaño 1–5 en el texto; ej. GPT4 zero-shot "Accuracy first digit" todas las celdas = 1.) "the accuracy of full answer prediction is significantly lower–and often near zero".

### 5.11 Relative Information Gain DP (Tablas 3 y 4)
- "ai is a good predictor of oi, and this is especially true for a1 and an−1". Tabla 3 ej.: "a1 o1 0.64 0.71 0.69 ...", "a1 o2 0.15 0.13 0.14 ...", "an−1 on−1 0.64 0.60 0.62 ...".
- Tabla 4 (triples): "a1 a2 a3 o1 1.00 0.96 0.97 ...", "an−3 an−2 an−1 on−1 0.95 0.95 0.95 0.95".

### Tabla 1 — Costos de finetuning GPT3 (multiplicación), valores literales
- "1 x 1, 81, $0.12, $7.44"; "2 x 1, 810, $1.28, $74.4"; "2 x 2, 8100, $12.96, $744"; "3 x 1, 8100, $12.96, $744"; "3 x 2, 81000, $129.6, $7440"; "3 x 3, 810000, $1296, $74,404"; "4 x 1, 81000, $129.6, $7440"; "4 x 2, 810000, $1296, $74,404"; "4 x 3, 8100000, $12,960, $744,040"; "4 x 4, 81000000, $129,600, $7,440,400"; "5 x 1, 810000, $1296, $74,404"; "5 x 2, 8100000, $12,960, $744,040"; "5 x 3, 81000000, $129,600, $7,440,400"; "5 x 4, 810000000, $1,296,000, $70,440,400"; "5 x 5, 8100000000, $12,960,000, $700,440,400".
- Texto asociado: "the total number of training examples required for multiplication up to 5 digits by 5 digits reaches an astonishing figure of approximately 9.1 billion examples." "the cost would amount to $12 million and $700 million for question-scratchpad training" (4 epochs).

---

## BLOQUE 6 — HALLAZGOS Y CONCLUSIONES

**6.1 Cada conclusión explícita**
- "transformer LLMs solve compositional tasks by reducing multi-step compositional reasoning into linearized subgraph matching, without necessarily developing systematic problem-solving skills."
- "systematic problem-solving capabilities do not emerge from maximum likelihood training [5] on input-output sequences, even when prompted or trained with human-like reasoning steps".
- "while models can memorize single-step operations, they fail to compose them into correct reasoning paths".
- "We argue that transformers could be inherently limited in solving compositionally complex tasks out-of-the-box".
- "we provide theoretical evidence of exponential error accumulation using abstract compositional tasks."
- "the autoregressive characteristic of transformers, which forces them to tackle problems sequentially, presents a fundamental challenge that cannot be resolved by instructing the model to generate a step-by-step solution."

**6.2 Frases textuales más importantes**
- "transformers may have inherent limitations on solving high-complexity compositional tasks that exhibit novel patterns."
- "models depend on a greedy process of producing the next word to make predictions without a rigorous global understanding of the task."
- "the strong performance of transformers should be taken with a certain grain of salt".
- "the probability of incorrect predictions converges exponentially to ≈1 for abstract compositional tasks. Importantly, these proofs apply to autoregressive LMs in general."

**6.3 Qué confirma del paper previo**
[NO MENCIONADO EN EL TEXTO] (no replica un paper previo). El texto sí dice respecto a literatura: "Building upon this line of inquiry, we present a more rigorous examination of sub-graph matching" (sobre [64] Razeghi et al. y [45] Liu et al.).

**6.4 Qué refuta o matiza**
- Matiza la narrativa "sparks of AGI": "the strong performance of transformers should be taken with a certain grain of salt: ... certain tasks may not possess the inherent compositionality they seem to have."
- Sobre expresividad teórica: "All tasks analyzed in our work belong to a class expressible by transformers, suggesting that known upper bound might not be tight."
- Grokking: "We do not observe grokking arising in the context of multiplication".

**6.5 Postura final sobre si los modelos razonan**
"they mostly make predictions based on shallow, rote learning rather than a deep, holistic task understanding". "pattern matching—and not general reasoning capabilities—may be the cause behind correct model outputs." "giving a false illusion of performing compositional reasoning."

**6.6 Implicaciones filosóficas o cognitivas mencionadas**
"Applying step-by-step reasoning is fundamental to human intelligence [69, 68]." "Human problem-solving skills can be conceptualized as a graph structure". Epígrafe: "“It was the epoch of belief, it was the epoch of incredulity.” – Charles Dickens, A Tale of Two Cities". Estrategias prácticas sugeridas: usar transformers para tareas "decomposed into few reasoning steps", "where evaluation may afford some leniency", y "in combination with planning modules or refinement methods [82, 48]".

---

## BLOQUE 7 — CONCEPTOS TÉCNICOS

**7.1 Transformer LLMs / autoregressive transformers**
"For brevity, we use ‘transformers’ to refer to ‘autoregressive transformer LLMs’ throughout the paper."

**7.2 Compositional tasks / compositionality**
"These compositional problems present compelling challenges for AI systems as they require combining basic reasoning operations to follow computational paths that arrive at unique correct solutions."

**7.3 Computation graph (GA(x))**
"GA(x) = (V, E, s, op) is a directed acyclic graph. Nodes V represent all variables' values during A's execution: each node v ∈V has a value s(v) ∈R associated." "S ≡x and A(x) = s(o), representing the input and output of A respectively." "op : V →FA as op(v) = f."

**7.4 Linearization / topological ordering**
"To be able to train and evaluate a language model's ability to follow algorithm A we must linearize GA(x). Since we only consider autoregressive models, this linearization must also be a topological ordering."

**7.5 Reasoning depth**
"We then define the reasoning depth as the largest layer number in the graph... reasoning depth is a proxy for the maximum level of multi-hop reasoning required to solve the task."

**7.6 Reasoning width**
"We define the reasoning width of a graph as the mode of {d(v) : v ∈V }. This metric aims to measure the maximum number of variables required to maintain in parallel during the computation."

**7.7 Average parallelism**
"the ratio between |V | and its reasoning depth. This aims to compute the average width in computation through the graph, and not just in its mode."

**7.8 Relative Information Gain (RelativeIG)**
"RelativeIG(Yj, X) = H(Yj) −H(Yj|X) / H(Yj) ∈[0, 1]" — "measure the amount of (normalized) information gained about an output element Yj by observing a subset of input random variables".

**7.9 Scratchpad**
"Scratchpads are a verbalization of the computation graphs (i.e., a linearized representation of a topological ordering of GA(x))."

**7.10 Shortcut learning / pattern-matching**
"Shortcut learning [29] via pattern-matching may yield fast correct answers when similar compositional patterns are available during training but does not allow for robust generalization".

**7.11 Linearized subgraph matching / full computation (FC)**
"We define v's full computation as the subgraph induced by all ancestors of v including v, denoted FC bGA(x)(v)."

**7.12 Error types (categorías de nodo)**
"fully correct": "v and its ancestors have correct values and are derived from correct computations." "local error": "if its parent nodes have correct values but v is derived from an incorrect computation (i.e., a one-hop reasoning error)". "propagation error": "if v is derived from a correct computation but some of its parent nodes have incorrect values". "restoration error": "if it has a correct value but is derived from an incorrect computation."

**7.13 Grokking**
"a phenomenon known as grokking [59, 53]" — "models' gaining generalization capabilities when training significantly beyond overfitting".

**7.14 OOD (out-of-domain)**
"the performance sharply declines when evaluating unseen splits during training, i.e., out-of-domain (OOD)."

**7.15 Maximum Weighted Independent Set**
"a classic relaxation of the NP-complete Maximum Weighted Independent Set problem [39]".

**7.16 Low collision / collision rate**
"hn has low collision, with cn being an upper bound of hn's collision rate (cn < c ∀n, with c ≪1)".

**7.17 Iterated random functions / vector autoregression**
"if g(x) can be expressed as an affine transformation Fx+c, then it may be viewed as a first-order vector autoregression, which are known to be unstable when |λ| ≥1 for at least one λ eigenvalue of F [31, Prop. 10.1]." "The process of repeatedly applying a noisy single operation or function f can be related to iterated random functions [24]."

---

## BLOQUE 8 — REFERENCIAS

> El documento tiene referencias [1]–[86]. Se listan las citadas explícitamente en el cuerpo con su contexto; el resto se enumeran de la bibliografía. URLs/DOIs no aparecen en el texto salvo identificadores CoRR/arXiv.

Citadas en el cuerpo con contexto:
- **[5]** Bengio, Ducharme, Vincent. "A neural probabilistic language model." 2000. — Contexto: "maximum likelihood training [5]".
- **[9]** Bian et al. "ChatGPT is a knowledgeable but inexperienced solver..." 2023. — "struggle with simple, intuitive tasks [9, 62, 40]".
- **[11]** Brown et al. "Language models are few-shot learners." 2020. — GPT3 (text-davinci-003).
- **[12]** Bubeck et al. "Sparks of artificial general intelligence: Early experiments with GPT-4." 2023. — "“sparks of AGI” [12]".
- **[17]** Chung et al. "Scaling instruction-finetuned language models." 2022. — FlanT5.
- **[21]** De Moura, Bjørner. "Z3: An efficient smt solver." 2008. — "we use existing puzzle solvers [21]".
- **[22]** Dehaene et al. "Arithmetic and the brain." 2004. — "humans can solve 3-digit by 3-digit multiplication... [22, 34]".
- **[24]** Diaconis, Freedman. "Iterated random functions." 1999. — "iterated random functions [24]".
- **[25]** Douc, Moulines, Stoffer. "Nonlinear Time Series." 2014. — "nonlinear maps [25]".
- **[29]** Geirhos et al. "Shortcut learning in deep neural networks." 2020. — "Shortcut learning [29]".
- **[31]** Hamilton. "Time series analysis." 1994. — "[31, Prop. 10.1]".
- **[32]** Helwe, Clavel, Suchanek. "Reasoning with transformer-based models: Deep learning, but shallow reasoning." 2021. — "struggle across multiple domains [32]".
- **[34]** Hiebert. "Conceptual and procedural knowledge: The case of mathematics." 2013. — reglas de cálculo / multiplicación.
- **[35]** Jiang et al. "Draft, sketch, and prove..." 2023. — "chaining only a few compositional steps (e.g., [35])".
- **[39]** Kleinberg, Tardos. "Algorithm Design." 2005. — "Maximum Weighted Independent Set problem [39]".
- **[45]/[46]** Liu et al. "Transformers learn shortcuts to automata." 2022/2023. — "shallow transformers learn shortcuts... poor OOD generalization".
- **[47]** Z. Liu et al. "Towards understanding grokking..." 2022. — "according to [47]".
- **[52]** Merrill, Tsilivis, Shukla. "A tale of two circuits..." 2023. — "extended to sparse parity in [52]".
- **[53]** Murty et al. "Grokking of hierarchical structure in vanilla transformers." 2023. — "Following [53]".
- **[55]/[56]** Nye et al. "Show your work: Scratchpads for intermediate computation..." 2021. — "scratchpads [56]"; "Nye et al. [55]".
- **[57]** OpenAI. "ChatGPT..." 2022. — ChatGPT (GPT-3.5-turbo).
- **[58]** OpenAI. "GPT-4 technical report." 2023. — GPT4 (gpt-4).
- **[59]** Power et al. "Grokking: Generalization beyond overfitting..." 2022. — "grokking was recently introduced in [59]".
- **[61]** Prosser. "Hybrid algorithms for the constraint satisfaction problem." 1993. — "Einstein's puzzle [61]".
- **[64]** Razeghi et al. "Impact of pretraining term frequencies on few-shot numerical reasoning." 2022. — "positive correlation between the frequency of training terms and their test performance".
- **[67]** Schwarzschild et al. "Can you learn an algorithm?..." 2021. — "weight-tied neural networks".
- **[68]/[69]** Simon / Simon & Newell. — "fundamental to human intelligence [69, 68]".
- **[75]** Touvron et al. "LLaMA..." 2023. — LLaMa.
- **[77]** Varma et al. "Explaining grokking through circuit efficiency." 2023. — "[77] propose that grokking occurs when a task admits a generalizing and a memorizing solution".
- **[80]** Wei et al. "Chain-of-thought prompting..." 2022. — reasoning steps explícitos.
- **[82]** Welleck et al. "Generating sequences by learning to self-correct." 2023. — "refinement methods [82, 48]".
- **[48]** Madaan et al. "Self-refine..." 2023. — "[82, 48]".
- **[83]** Welleck et al. "Symbolic brittleness in sequence models..." 2022. — "symbolic mathematical integration [83]".
- **[86]** Zhou et al. "Teaching algorithmic reasoning via in-context learning." 2023. — "Zhou et al. [86] used scratchpads".
- **[43]** Lin et al. "Limitations of autoregressive models and their alternatives." 2021. — "study autoregressive models' limitations from a computational complexity theory perspective".
- **[30]** Hahn. "Theoretical limitations of self-attention in neural sequence models." 2020. — "Hahn [30] shows that transformers cannot robustly model noncounter-free regular languages".
- **[49][50][51][14]** Merrill & Sabharwal; Chiang et al. — expresividad de transformers.

Resto de bibliografía completa (no necesariamente citada por nombre en el cuerpo): [1] Aghajanyan et al. 2023; [2][3] Anil et al. 2022; [4] Bansal et al. 2022; [6] Bertsekas 2022; [7] Betz, Voigt, Richardson 2021; [8] Bhattamishra et al. 2020; [10] Bogin, Gupta, Berant 2022; [13] Bueno et al. 2022; [15] Choi et al. 2023; [16] Chowdhery et al. 2022 (PaLM); [18] Clark, Tafjord, Richardson 2021; [19] Creswell, Shanahan 2022; [20] Creswell, Shanahan, Higgins 2023; [23] Delyon, Juditsky 1999; [26] Dubois et al. 2020; [27] Evans 1989; [28] Fu, Peng, Khot 2022; [33] Henighan et al. 2020; [36] Jiang et al. (Delphi) 2021; [37] Johnson-Laird et al. 2015; [38] Kaplan et al. 2020; [40] Koralus, Wang-Mascianica 2023; [41] Levy, Bogin, Berant 2023; [42] Liang et al. 2023; [44] Ling et al. 2017; [54] Newman et al. 2020; [60] Press, Smith, Lewis 2022; [62] Qin et al. 2023; [63] Rae et al. 2021 (Gopher); [65] Sap et al. 2022; [66] Saparov, He 2023; [70] Srivastava et al. (BIG-bench) 2022; [71] Stenning, Van Lambalgen 2012; [72] Tafjord, Dalvi, Clark 2021 (ProofWriter); [73] Taylor et al. (Galactica) 2022; [74] Thoppilan et al. (LaMDA) 2022; [76] Valmeekam et al. 2022; [78] Veličković, Blundell 2021; [79] Wei et al. 2022 (Emergent abilities); [81] Welleck et al. (NaturalProver) 2022; [84] Zhang et al. (LEGO) 2022; [85] Zheng, Zhan 2023.

URL externa única en el texto: "https://github.com/nouhadziri/faith-and-fate".

---

## BLOQUE 9 — FIGURAS Y TABLAS

- **Figura 1**: "Transformation of an algorithm A to its computational graph GA(x). The depicted example is of long-form multiplication algorithm A, for inputs x = [7, 49] (i.e. computing 7 × 49)." Variables: nodos/aristas del grafo de cómputo.
- **Figura 2**: "(a) Zero-shot accuracy. Axes refer to problem sizes... Transformers' accuracy decreases to near zero as task complexity increases... (b) Average parallelism negatively correlates with accuracy." Conclusión: complejidad ↑ → accuracy ↓.
- **Figura 3**: "GPT3 finetuned exhaustively on task-specific data up to a certain problem size. The blue region represents the in-distribution examples and the red region refers to OOD examples." Conclusión: éxito in-domain, fallo OOD.
- **Figura 4**: "Results of training beyond the overfitting point for the multiplication task with the goal of exploring whether OOD generalization capabilities (i.e., grokking) arise." Conclusión: "no improvement in generalization for OOD cases".
- **Figura 5**: "GPT3 finetuning and prompting accuracy on different data splits. Although the in-distribution performance is almost perfect, GPT3 exhibits poor generalization with increasing graph depth and width."
- **Figura 6**: "Average frequency in which test examples' full computations subgraph appear in the training data w.r.t. the subgraph depth, grouped by final answer." Conclusión: subgrafos aparecen más para respuestas correctas → pattern matching.
- **Figura 7**: "Ratio of nodes in each of the four correct/error categories for each layer in computation graph. Results shown are for few-shot prompting and fine-tuning with scratchpad." Conclusión: fully correct cae a cero con la profundidad; propagation > local.
- **Figura 8**: "Example prompt for the multiplication task used for the few-shot setting."
- **Figura 9**: "A sample scratchpad for the multiplication task." (ejemplo: "What is 35 times 90?" → "The final answer is ... = 3150.")
- **Figura 10**: "A sample of the puzzle task and the reasoning path to reach a solution." Incluye Algorithm 1 (Puzzle Solver) y la tabla ground-truth (Eric/Peter/Arnold).
- **Figura 11**: "A sample scratchpad for the puzzle task."
- **Figura 12**: "Example prompt for the DP task, used for zero-shot and few-shot settings." (input = [3, 2, 1, 5, 2]).
- **Figura 13**: "A sample scratchpad for the DP task used for fine-tuning with few-shot settings." (output=[1, 2, 2, 1, 2]).
- **Figura 14**: "Graph parallelism vs accuracy. The accuracy decreases as the complexity increases."
- **Figura 15**: "Zero-shot accuracy. Performance of ChatGPT, GPT3, LLaMA and FlanT5 on the multiplication task." (valores en 5.1).
- **Figura 16**: "Few-shot accuracy with question-answer pairs. Performance of GPT4, ChatGPT, GPT3, LLaMA and FlanT5 on the multiplication task." (valores en 5.2).
- **Figura 17**: "Zero-shot accuracy. Performance of ChatGPT, GPT3, LLaMA and FlanT5 on the puzzle task. Few-shot performance led to worse performance."
- **Figura 18**: "GPT3 finetuned on the puzzle task using question-answer pairs. The training data consisted of puzzles of size 4x4, and the model was subsequently evaluated on larger puzzle sizes for OOD testing."
- **Figura 19**: "GPT3 finetuned on the multiplication task using question-answer pairs."
- **Figura 20**: "Zero-shot and Few-shot accuracy using question-answer pairs. Performance of GPT4, ChatGPT, and GPT3 on the dynamic programming task. LLaMA and FlanT5 results are near zero for all problem sizes."
- **Figura 21**: "GPT3 finetuned on the dynamic programming task using question-answer pairs... the model was trained with a problem size of 5, and the graph's depth and width were set to 18."
- **Figura 22**: "GPT3 finetuned on the dynamic programming task using question-scratchpad pairs..."
- **Figura 23**: "GPT3 finetuned exhaustively on task-specific data up to a certain problem size... we train on examples up to 3-digit by 2-digit multiplication (left) and ... up to 5 digits in the output response (right)."
- **Figura 24**: "GPT3 finetuned on the puzzle task using question-scratchpad pairs..."
- **Figura 25**: "GPT4 few-shot accuracy with question-scratchpad pairs on the 3 tasks. The performance improves for most problem sizes compared to zero-shot... but degrades to zero as the complexity increases."
- **Figura 26**: "GPT4 zero-shot accuracy in predicting partially correct responses. This evidences surface pattern learning..."
- **Figura 27**: "ChatGPT zero-shot accuracy in predicting partially correct responses. We observe the same trend for GPT3 predictions."
- **Figura 28**: "GPT4 five-shot accuracy in predicting partially correct responses..."
- **Figura 29**: "GPT3 finetuned on question-scratchpad pairs. Accuracy of predicting partially correct responses."
- **Figura 30**: "GPT4 five-shot with scratchpad accuracy in predicting output elements oi in the DP task. All oi are predicted with high accuracy with o1 and on−1 being consistently among the highest."
- **Figura 31**: "GPT3 few-shot without scratchpad accuracy in predicting output elements oi in the DP task..."
- **Figura 32**: "GPT3 fine-tuned without scratchpad accuracy in predicting output elements oi in the DP task..."
- **Tabla 1**: "Finetuning cost of GPT3 model on the multiplication data." (valores en Bloque 5).
- **Tabla 2**: "Highest Relative Information Gain Elements and Pairs of Elements, for multiplications between x and y, with 2 ≤n ≤5."
- **Tabla 3**: "Highest Relative Information Gain Elements, for DP problems of size 2 ≤n ≤10."
- **Tabla 4**: "Highest Relative Information Gain Contiguous Triples, for DP problems of size 3 ≤n ≤10."

---

## BLOQUE 10 — GAPS Y TRABAJO FUTURO

**10.1 Limitaciones reconocidas**
- "we cannot inspect the exact tokens model attends to when making the prediction. This limitation arises from our lack of access to the activations of the studied models."
- "due to our compute budget constraints as well as limited access to the largest language models such as GPT4, we are unable to push the empirical limits of transformers even further in terms of training data size and number of epochs."
- "we are limited to only establishing a correlation between the model generation and its preceding context".

**10.2 Trabajo futuro propuesto**
- "We invite the broader research community, particularly those with more extensive resources at their disposal, to investigate these possibilities further."
- "Future work is required to accurately explain when and how grokking occurs."
- "we leave it to future work to explore whether this may be due to task difficulty hindering the learning of well-structured representations."
- "fundamental innovations are required to address or complement these limitations."
- Direcciones prácticas: "using transformers for tasks that could be decomposed into few reasoning steps, tasks where evaluation may afford some leniency, and using transformers in combination with planning modules or refinement methods".

**10.3 Preguntas abiertas sin resolver**
- "Under what conditions do transformers succeed, fail, and why? What types of errors do they make? Can transformers uncover implicit problem-solving rules or be taught to follow reasoning paths?"
- "Seeking thorough answers to these questions remains an open research challenge."
- Sobre cota superior teórica: "All tasks analyzed in our work belong to a class expressible by transformers, suggesting that known upper bound might not be tight."

**10.4 Código/recursos externos (URLs exactas)**
- "Code and data are available at https://github.com/nouhadziri/faith-and-fate".

---

## VERIFICACIÓN — Los 5 datos más difíciles de encontrar (con cita textual)

1. **Costo y duración exactos del experimento de grokking.** Cita: "The training duration for question-answer pairs is equivalent to 60 epochs and costs 50,000 USD. Training on question-scratchpad pairs was conducted for 40 epochs and costs 40,000 USD." (Confirmado.)

2. **Porcentaje de respuestas correctas con al menos un error en el grafo.** Cita: "82.3% of the final correct answers for 4-digit by 2-digit multiplications (a setting unseen during training) had at least one error in the computation graph, but still produced correct answers." (Confirmado.)

3. **Cotas de colisión exactas en la prueba de multiplicación (Corolario D.1).** Cita: "It can be shown that P(hn(X) = hn(Y ) | X ̸= Y ) < βαn for α = 0.1 and β = 10m." (Confirmado.)

4. **Hiperparámetros de inferencia y nº de ejemplos de test.** Cita: "During inference, we set nucleus sampling p to 0.7 and temperature to 1. For each task, we evaluate the performance of each model on 500 test examples." (Confirmado.)

5. **Costo total estimado de entrenar hasta 5x5 y nº de ejemplos requeridos.** Cita: "the total number of training examples required for multiplication up to 5 digits by 5 digits reaches an astonishing figure of approximately 9.1 billion examples. Should we choose to fine-tune GPT3 for 4 epochs on question-answer pairs, the cost would amount to $12 million and $700 million for question-scratchpad training." (Confirmado; Tabla 1 indica para 5x5: "$12,960,000" sin scratchpad y "$700,440,400" con scratchpad.)

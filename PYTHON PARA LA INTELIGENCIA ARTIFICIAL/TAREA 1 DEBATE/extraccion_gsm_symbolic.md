# EXTRACCIÓN ACADÉMICA — GSM-Symbolic

> Documento fuente: "2410.05229v2.txt" (texto íntegro del PDF). Toda cita textual va entre comillas dobles "...". Lo no presente se marca como [NO MENCIONADO EN EL TEXTO].

---

## BLOQUE 1 — IDENTIDAD

**1.1 Título completo**
"GSM-SYMBOLIC: UNDERSTANDING THE LIMITATIONS OF MATHEMATICAL REASONING IN LARGE LANGUAGE MODELS"

**1.2 Autores en orden**
1. Iman Mirzadeh
2. Keivan Alizadeh
3. Hooman Shahrokhi
4. Oncel Tuzel
5. Samy Bengio
6. Mehrdad Farajtabar

**1.3 Afiliación de cada autor**
El texto marca las afiliaciones con superíndices:
- "Iman Mirzadeh1", "Keivan Alizadeh1", "Oncel Tuzel1", "Samy Bengio1", "Mehrdad Farajtabar1†" → "1Apple"
- "Hooman Shahrokhi2∗" → "2Washington State University"
- Nota: "∗Work done during an internship at Apple. †Correspondence to {imirzadeh,farajtabar}@apple.com."

**1.4 Fecha**
- "Published as a conference paper at ICLR 2025"
- "arXiv:2410.05229v2  [cs.LG]  27 Aug 2025"

**1.5 arXiv u otro id**
- "arXiv:2410.05229v2  [cs.LG]"
- Doc: "CoRR" / "ICLR 2025" [el id arXiv es 2410.05229v2]

**1.6 Financiamiento**
[NO MENCIONADO EN EL TEXTO]

**1.7 Agradecimientos**
"The authors would like to thank Max Horton, Fartash Faghri, Moin Nabi, Devi Krishna, and Arsalan Farooq for the valuable feedback and support."

---

## BLOQUE 2 — CONTEXTO Y MOTIVACIÓN

**2.1 Paper previo que motiva (título, autores, año)**
El benchmark base que motiva el trabajo es GSM8K: "The GSM8K (Grade School Math 8K) dataset Cobbe et al. (2021)". Referencia: "Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. Training verifiers to solve math word problems. arXiv preprint arXiv:2110.14168, 2021."
[NO MENCIONADO EN EL TEXTO un único "paper previo" controvertido distinto de GSM8K; el documento parte de la literatura general sobre razonamiento en LLMs, no de un único paper en disputa.]

**2.2 Hallazgos de ese paper según ESTE documento**
Sobre GSM8K, este documento dice: "The GSM8K dataset (Cobbe et al., 2021) includes over 8000 grade school math questions and answers, divided into 7473 training and 1319 test examples." / "the questions are relatively simple, requiring knowledge of only the four main arithmetic operations." / "While it includes simple math questions with detailed solutions, making it suitable for techniques like Chain-of-Thought (CoT) prompting, it provides only a single metric on a fixed set of questions."

**2.3 Controversia según este documento**
"However, the question of whether current LLMs are genuinely capable of true logical reasoning remains an important research focus. While some studies highlight impressive capabilities, a closer examination reveals substantial limitations."
Adicionalmente (Apéndice B): "After the initial publication of our paper, we received various feedback regarding the statistical analysis of our results. Most notably, Ivanova et al. (2025) provide a detailed statistical analysis based on our results and argue that several of our observations are not statistically significant."

**2.4 Posiciones del debate y quién las sostiene**
- Posición de los autores de este paper: "we hold a fundamentally different philosophical view of reasoning than Ivanova et al. (2025). For instance, we do not believe the performance of an ideal reasoner—one that has truly understood a question—should follow a Bernoulli distribution. Rather, when focusing one single question, we argue that a degenerate distribution would be a more appropriate model."
- Posición de Ivanova et al. (2025): "Ivanova et al. (2025) argue that a one-sample t-test is inappropriate because the evaluation involves two datasets, and that a two-sample z-test would therefore be more suitable." / "argue that several of our observations are not statistically significant."
- Postura literaria general citada: "Literature suggests that the reasoning process in LLMs is probabilistic pattern-matching rather than formal reasoning (Jiang et al., 2024)."

**2.5 Medios mencionados y qué dijeron**
[NO MENCIONADO EN EL TEXTO]

**2.6 Objetivo declarado de este paper**
"To overcome the limitations of existing evaluations, we introduce GSM-Symbolic, an improved benchmark created from symbolic templates that allow for the generation of a diverse set of questions. GSM-Symbolic enables more controllable evaluations, providing key insights and more reliable metrics for measuring the reasoning capabilities of models."
Contribuciones declaradas:
- "We introduce GSM-Symbolic, an enhanced benchmark that generates diverse variants of GSM8K questions using symbolic templates (Sec. 3)... Our large-scale study on 25 state-of-the-art open and closed models provides significant insights into LLMs' behavior in mathematical reasoning tasks."
- "We question the reliability of currently reported results on GSM8K and demonstrate that the performance of LLMs can be viewed as a distribution with unwarranted variance across different instantiations of the same question."
- "We show that LLMs exhibit more robustness to changes in superficial elements like proper names but are very sensitive to changes in numerical values (Sec. 4.2)."
- "Finally, we further question the reasoning abilities of LLMs and introduce the GSM-NoOp dataset."

**2.7 Qué dice que NO pretende hacer**
- "This decision reflects our focus on assessing logical reasoning capabilities rather than arithmetic skills."
- "Overall, we do not believe that extensive statistical testing adds significant value the main focus of this paper."
- Sobre añadir/quitar cláusulas: "our main focus in this section is to understand the evolution of the performance distribution rather than the precise performance numbers."

---

## BLOQUE 3 — BENCHMARKS Y PUZZLES

### 3.1 GSM8K
**3.1.1 Descripción exacta:** "The GSM8K (Grade School Math 8K) dataset Cobbe et al. (2021) has emerged as a popular benchmark for evaluating the mathematical reasoning capabilities of LLMs." / "includes over 8000 grade school math questions and answers, divided into 7473 training and 1319 test examples."
**3.1.2 Reglas exactas:** "the questions are relatively simple, requiring knowledge of only the four main arithmetic operations." Evaluación en este paper: "GSM8K (Full)" = "the full test set of GSM8K (comprising 1,319 examples)"; "GSM8K (100)" = "a subset of 100 questions from the GSM8K test set, which we randomly selected to generate GSM-Symbolic templates."
**3.1.3 Fórmula de dificultad:** [NO MENCIONADO EN EL TEXTO]
**3.1.4 Resultados del paper previo:** [NO MENCIONADO EN EL TEXTO resultados de Cobbe et al. propiamente; este documento solo reporta su propia medición sobre GSM8K en Tab. 1.]
**3.1.5 Fallas metodológicas del paper previo según este documento:** "it provides only a single metric on a fixed set of questions. This limitation restricts comprehensive insights into the models' mathematical reasoning." / "the popularity and prevalence of GSM8K can increase the risk of inadvertent data contamination." / "the static nature of GSM8K does not allow for controllable experiments to understand model limitations".
**3.1.6 Criterios de resolubilidad:** [NO MENCIONADO EN EL TEXTO]

### 3.2 GSM-Symbolic
**3.2.1 Descripción exacta:** "an improved benchmark created from symbolic templates that allow for the generation of a diverse set of questions." / "we create parsable templates as shown in Fig. 1 (right)."
**3.2.2 Reglas exactas (proceso de generación de templates, Sec. 3.1):** "The annotation process involves identifying variables, their domains, and necessary conditions to ensure the correctness of both the question and the answer." / "since the questions are grade-school level, a common condition is divisibility to ensure the answer is a whole number." / "We use common proper names (e.g., persons, foods, currencies) to streamline creation." / Comprobaciones automáticas: "we verify that none of the original variable values appear in the template. We also check that the original values satisfy all conditions and that the final answer matches the original question's answer. Once data are generated, 10 random samples per template are reviewed manually. As a final automated check, after evaluating all models, we verify that at least two models answer each question correctly; otherwise, the question is reviewed manually again." / "we deliberately select numerical ranges that closely align with those in the original GSM8K test set." Ejemplo de plantilla (Fig.1): variables "name = sample(names)", "family = sample([\"nephew\", \"cousin\", \"brother\"])", "x = range(5, 100)", "y = range(5, 100)", "z = range(5, 100)", "total = range(100, 500)", "ans = range(85, 200)"; condición: "x + y + z + ans == total".
**3.2.3 Fórmula de dificultad:** se modifica por número de cláusulas (ver 3.4–3.5); no se da fórmula numérica. [NO MENCIONADO EN EL TEXTO una fórmula explícita.]
**3.2.4 Resultados del paper previo:** No aplica (benchmark nuevo de este paper).
**3.2.5 Fallas metodológicas del paper previo:** No aplica.
**3.2.6 Criterios de resolubilidad:** "a common condition is divisibility to ensure the answer is a whole number." y la verificación de que "at least two models answer each question correctly".

### 3.3 GSM-Symbolic-Minus-1 (GSM-M1)
**3.3.1 Descripción:** "First, by removing one clause, we obtain GSM-Symbolic-Minus-1 or GSM-M1 for short."
**3.3.2 Reglas:** Se genera desde GSM-Symb removiendo una cláusula. Nota al pie: "adding or removing a clause does not necessarily correspond to increasing or decreasing the number of required reasoning steps by exactly one."
**3.3.3 Fórmula de dificultad:** [NO MENCIONADO EN EL TEXTO]
**3.3.4–3.3.6:** No aplica / [NO MENCIONADO EN EL TEXTO]

### 3.4 GSM-Symbolic-Plus-1 (GSM-P1) y GSM-Symbolic-Plus-2 (GSM-P2)
**3.4.1 Descripción:** "we can add one or two clauses to the questions to increase the difficulty, resulting in GSM-Symbolic-Plus-1 (GSM-P1) and GSM-Symbolic-Plus-2 (GSM-P2), respectively." Ejemplo Fig.5 (booth telefónico): P1 añade "After 25 minutes from the start of the call, the price drops even more to $0.3 per minute."; P2 añade además "If your total bill is more than $10, you get a 25% discount."
**3.4.2 Reglas:** orden creciente de dificultad "GSM-M1→GSM-Symb→GSM-P1→GSM-P2".
**3.4.3 Fórmula de dificultad:** [NO MENCIONADO EN EL TEXTO]
**3.4.4–3.4.6:** No aplica / [NO MENCIONADO EN EL TEXTO]

### 3.5 GSM-NoOp (Symbolic-NoOp)
**3.5.1 Descripción:** "a dataset designed to challenge the reasoning capabilities of language models." / "we add seemingly relevant but ultimately inconsequential statements to GSM-Symbolic templates. Since these statements carry no operational significance, we refer to them as \"No-Op\"."
**3.5.2 Reglas:** "By adding seemingly relevant but ultimately irrelevant information to problems". Ejemplo (Fig.7, kiwis): "On Sunday, he picks double the number of kiwis he did on Friday, but five of them were a bit smaller than average." (la cláusula "five of them were a bit smaller than average" es irrelevante). Variantes de shots (Sec. 4.4):
- "NoOp-Symb (Using GSM-Symbolic shots of the same question): During evaluation, we include 8 different shots of the same question coming from GSM-Symbolic."
- "NoOp-NoOp (Using GSM-NoOp shots of different questions): Here, we provide 8 shots chosen randomly from different questions of GSM-NoOp in the context."
**3.5.3 Fórmula de dificultad:** [NO MENCIONADO EN EL TEXTO]
**3.5.4 Resultados del paper previo:** No aplica.
**3.5.5 Fallas metodológicas del paper previo:** No aplica.
**3.5.6 Criterios de resolubilidad:** "the correct answer should ignore the No-Op statement."

### Otros datasets/benchmarks mencionados (de la literatura)
- "iGSM (Ye et al., 2024) is a math dataset created through a synthetic pipeline that captures parameter dependencies in a hierarchical and graph structure."
- "GSM-IC (Shi et al., 2023) shows that irrelevant context can impair LLM performance, focusing on prompting techniques."
- "GSM-Plus (Li et al., 2024a) introduces variants of GSM8K questions but lacks symbolic templates and has a fixed size and difficulty."
- "GSM1K (Zhang et al., 2024) mirrors the style and complexity of GSM8K to identify systematic overfitting in existing models, but it is not publicly available for researchers."
- MATH dataset: "Srivastava et al. (2024) purposes functional variant of MATH dataset."

---

## BLOQUE 4 — METODOLOGÍA

**4.1 Modelos usados (lista de TODOS los que aparecen en Tab. 1)**
"Gemma2b", "Gemma2b-it", "Gemma-7b", "Gemma-7b-it", "Gemma2-2b", "Gemma2-2b-it", "Gemma2-9b", "Gemma2-9b-it", "Gemma2-27b-it", "Phi-2", "Phi-3-mini-128k-instruct", "Phi-3-small-128k-instruct", "Phi-3-medium-128k-instruct", "Phi-3.5-mini-instruct", "Mistral-7b-v0.1", "Mistral-7b-instruct-v0.1", "Mistral-7b-v0.3", "Mistral-7b-instruct-v0.3", "Mathstral-7b-v0.1", "Llama3-8b", "Llama3-8b-instruct", "GPT-4o-mini", "GPT-4o", "o1-mini", "o1-preview".
Resumen del texto: "we report on more than 20 open models of various sizes, ranging from 2B to 27B. Additionally, we include state-of-the-art closed models such as GPT-4o-mini, GPT-4o, o1-mini, and o1-preview." / "Our large-scale study on 25 state-of-the-art open and closed models". Familias citadas: "Gemma (Mesnard et al., 2024), Gemma2 (Rivière et al., 2024), Phi (Abdin et al., 2024), Mistral (Jiang et al., 2023), Llama3 (Dubey et al., 2024), GPT-4o (OpenAI, 2023), and the o1 (OpenAI, 2024) series".

**4.2 Justificación**
"To conserve space, we present results for a few selected models in each experiment, but the full results for all models are available in Tab. 1". Para los rangos numéricos: "This decision reflects our focus on assessing logical reasoning capabilities rather than arithmetic skills."

**4.3 Cada estrategia con su nombre exacto**
- Generación por plantillas simbólicas ("TEMPLATE GENERATION", Sec. 3.1).
- Variación por tipo de cambio: "Names", "Numbers", "Both" (Sec. 4.2).
- Variación por dificultad: "GSM-M1", "GSM-Symb", "GSM-P1", "GSM-P2" (Sec. 4.3).
- "GSM-NoOp" con sub-estrategias "NoOp-Symb" y "NoOp-NoOp" (Sec. 4.4).
- Ablation de fine-tuning sobre GSM-P1 (Apéndice A.4).
- Ablation de exactitud aritmética (Apéndice A.6).

**4.4 Para cada una**

*Plantillas simbólicas:*
- 4.4.a paso a paso: ver 3.2.2 (identificar variables/dominios/condiciones; checks automáticos; revisión manual de 10 muestras por plantilla; verificación de que ≥2 modelos aciertan).
- 4.4.b diferencias con paper previo: a diferencia de GSM8K que da "only a single metric on a fixed set of questions", aquí "viewing LLM performance as a distribution across various problem instances". Frente a GSM-Plus "lacks symbolic templates and has a fixed size and difficulty"; frente a GSM1K que "is not publicly available".
- 4.4.c parámetros: "using 100 templates and generating 50 samples per template, resulting in 5000 total examples for each benchmark. Therefore, we have 50 datasets of 100 examples each". "we conducted nearly 500 total evaluations on various setups." Evaluación: "Chain-of-Thought (CoT) prompting with 8-shots with greedy decoding."

*GSM-NoOp / NoOp-Symb / NoOp-NoOp:*
- 4.4.a: añadir afirmaciones "No-Op"; NoOp-Symb usa "8 different shots of the same question coming from GSM-Symbolic"; NoOp-NoOp usa "8 shots chosen randomly from different questions of GSM-NoOp".
- 4.4.b: "Our work, however, suggests a more fundamental issue: LLMs struggle even when given multiple shots of the same question" (contrasta con GSM-IC, que se enfoca en "prompting techniques").
- 4.4.c: 8 shots; "Except for the last experiment in Sec. 4.4, we use the original 8 shots from GSM8K."

*Ablation fine-tuning (A.4):*
- 4.4.c: "We have used a set of 50 templates from GSM-P1, separate from the test templates, and generated 10000 examples for finetuning training set." Epochs 1–5 (Fig. 11b).

*Ablation aritmética (A.6):*
- 4.4.c: "for every digit length and every operation, we have at least 1,000 test cases." Prompts zero-shot: "What is x plus y?", "What is x times y?". Tab. 2: extracción de cálculos donde "the equal sign (=) was generated along with numerical values".

**4.5 Comparabilidad con el paper previo**
"It is noteworthy that the performance levels across both sets [GSM8K Full vs. GSM8K 100] are very similar, with no significant differences observed." / "we deliberately select numerical ranges that closely align with those in the original GSM8K test set."

**4.6 Limitaciones metodológicas reconocidas sobre sus propios métodos**
- Sobre cláusulas: "adding or removing a clause does not necessarily correspond to increasing or decreasing the number of required reasoning steps by exactly one."
- Sobre shots: "we note that in our preliminary experiments, the number of shots did not significantly change the performance and conclusions."
- Sobre decodificación o1: "the available APIs for \"o1-mini\" and \"o1-preview\" models do not allow controlling the decoding strategy, and it seems that at the time of writing, these models do not perform greedy decoding, as responses to the same prompt change."
- Sobre significancia estadística: "Overall, we do not believe that extensive statistical testing adds significant value the main focus of this paper." / "if one disagrees with our assumptions and accepts the assumptions of Ivanova et al. (2025), our results would likewise be statistically non-significant". / Sobre el t-test: "the t-test assumes normality, which may not necessarily hold for evaluation results."
- Sobre rangos numéricos: "we need to slightly increase the numeric range of numbers to ensure enough instances are generated from each template."

---

## BLOQUE 5 — RESULTADOS CUANTITATIVOS

### 5.1 Fiabilidad de GSM8K / variación en GSM-Symbolic (Sec. 4.1, Fig. 2 y 3)
**5.1.1 Valores numéricos exactos (GSM8K → GSM-Symbolic, formato media (±std)):**
- Gemma2-9b-it: "GSM8K 87.0" / "GSM-Symbolic 79.1 (±3.0)"
- Llama3-8b-instruct: "GSM8K 74.0" / "GSM-Symbolic 74.6 (±2.9)"
- GPT-4o: "GSM8K 95.0" / "GSM-Symbolic 94.9 (±1.9)"
- Phi-3-medium-128k-instruct: "GSM8K 89.0" / "GSM-Symbolic 82.5 (±2.9)"
- Phi-3.5-mini-instruct: "GSM8K 88.0" / "GSM-Symbolic 82.1 (±3.4)"
- Mathstral-7b-v0.1: "GSM8K 80.0" / "GSM-Symbolic 74.0 (±3.5)"
Caídas (Fig. 3, "GSM8K →GSM-Symbolic Accuracy Drop (%)"): "-9.2 Mistral-7b-it-v0.1", "-7.4 Gemma2-2b", "-7.4 Gemma2-2b-it", "-6.2 Gemma2-9b", "-6.2 Gemma2-9b-it", "-6.2 Mistral-7b-it-v0.3", "-6.1 Mathstral-7b-v0.1", "-4.8 Phi-3-medium", "-4.8 Phi-3-small", "-3.9 Gemma2b", "-3.9 Gemma2b-it", "-3.7 Gemma-7b-it", "-3.4 Mistral-7b-v0.1", "-3.0 Phi-3-mini", "-2.8 Phi-3.5-mini-it", "-2.4 GPT-4o-mini", "-2.2 o1-preview", "-1.4 Gemma2-27b-it", "-1.3 Llama3-8b-it", "-0.7 Mistral-7b-v0.3", "-0.6 o1-mini", "-0.3 GPT-4o".
**5.1.2 Rangos de N:** 50 datasets de 100 ejemplos; "5000 total examples for each benchmark".
**5.1.3 Trials por configuración:** "50 samples per template"; "50 datasets of 100 examples each".
**5.1.4 Métricas:** "8-shot CoT performance"; accuracy (%); media y desviación estándar.
**5.1.5 Punto exacto de fallo/éxito:** "for the Gemma2-9B, the gap between the worst performance and the best performance is more than 12%, while for Phi-3.5-mini, this gap is around 15%."
**5.1.6 Porcentajes/umbrales/valores críticos:** "the performance (represented by the dashed line in Fig. 2) on the original questions... is often more than one standard deviation away from the center... frequently on the right side of the distribution (this holds for 21 out of 25 models)."
**5.1.7 Patrones de tokens:** [NO MENCIONADO EN EL TEXTO en esta sección]

### 5.2 Cambio de nombres vs. números (Sec. 4.2, Fig. 4)
**5.2.1 Valores (GSM8K / Names / Numbers / Both):**
- Gemma2-9b-it: "GSM8K 87.0", "Names 88.6 (±2.0)", "Numbers 83.1 (±2.2)", "Both 79.1 (±3.0)"
- Llama3-8b-instruct: "GSM8K 74.0", "Names 75.6 (±2.1)", "Numbers 75.5 (±3.1)", "Both 74.6 (±2.9)"
- Phi-3-medium-128k-instruct: "GSM8K 89.0", "Names 91.8 (±1.7)", "Numbers 89.0 (±2.3)", "Both 82.5 (±2.9)"
- Phi-3-small-128k-instruct: "GSM8K 89.0", "Names 91.8 (±1.7)"... ["Names 91.8" aparece para Phi-3-medium; para Phi-3-small: "Names 88.4 (±1.8)", "Numbers 83.7 (±2.4)", "Both 83.7 (±2.6)", "GSM8K 89.0"]
- Phi-3.5-mini-instruct: "GSM8K 88.0", "Names 89.1 (±1.8)", "Numbers 84.9 (±2.4)", "Both 82.1 (±3.4)"
- Mathstral-7b-v0.1: "GSM8K 80.0", "Names 81.0 (±1.3)", "Numbers 77.3 (±2.0)", "Both 74.0 (±3.5)"
**5.2.4 Métricas:** "8s CoT" accuracy con media±std.
**5.2.6 Patrón:** "the variance is lower when changing names compared to numbers." / "a gradual shift in the means of distributions from right to left, along with an increase in variance".

### 5.3 Dificultad por número de cláusulas (Sec. 4.3, Fig. 6)
**5.3.1 Valores (GSM-M1 / GSM-Symb / GSM-P1 / GSM-P2):**
- Gemma2-9b-it: "GSM-M1 84.4(±2.4)", "GSM-Symb 79.1(±3.0)", "GSM-P1 68.1(±4.8)", "GSM-P2 41.8(±6.0)"
- Phi-3.5-mini-instruct: "GSM-M1 87.6(±2.0)", "GSM-Symb 82.1(±3.4)", "GSM-P1 64.8(±5.4)", "GSM-P2 44.8(±6.3)"
- Phi-3-medium-128k-instruct: "GSM-M1 89.6(±1.7)", "GSM-Symb 82.5(±2.9)", "GSM-P1 75.8(±3.9)", "GSM-P2 53.1(±4.8)"
- GPT-4o-mini: "GSM-M1 92.5(±1.6)", "GSM-Symb 91.7(±2.0)", "GSM-P1 81.1(±3.1)", "GSM-P2 72.4(±4.6)"
- GPT-4o: "GSM-M1 94.4(±1.6)", "GSM-Symb 94.9(±1.9)", "GSM-P1 93.9(±2.6)", "GSM-P2 88.0(±3.4)"
- o1-mini: "GSM-M1 94.9(±1.5)", "GSM-Symb 94.5(±1.6)", "GSM-P1 94.3(±2.6)", "GSM-P2 89.1(±3.6)"
**5.3.5 Patrón/punto de fallo:** "as the difficulty increases, the performance decreases and the variance increases." / "the rate of accuracy drop also increases as the difficulty increases."

### 5.4 GSM-NoOp (Sec. 4.4, Fig. 8a — "GSM8K →GSM-NoOp Accuracy Drop(%)")
**5.4.1 Caídas exactas:** "-65.7 Phi-3-mini-128k-instruct", "-64.0 Phi-3-small-128k-instruct", "-63.0 Gemma2-9b", "-63.0 Gemma2-9b-it", "-62.5 Phi-3.5-mini-instruct", "-59.7 Gemma2-27b-it", "-59.7 Mathstral-7b-v0.1", "-57.8 Phi-3-medium-128k-instruct", "-57.4 Llama3-8b-instruct", "-44.9 Phi-2", "-40.3 Mistral-7b-instruct-v0.3", "-40.0 GPT-4o-mini", "-38.6 Gemma2-2b", "-32.0 GPT-4o", "-31.8 Gemma2-2b-it", "-29.6 Mistral-7b-instruct-v0.1", "-29.1 o1-mini", "-28.3 Mistral-7b-v0.1", "-24.0 Mistral-7b-v0.3", "-20.6 Gemma-7b-it", "-17.5 o1-preview".
**5.4.6 Valores críticos:** "with the Phi-3-mini model experiencing over a 65% drop". El abstract: "we observe significant performance drops (up to 65%) across all state-of-the-art models".
**5.4.5 NoOp por fuente de shots (Fig. 8b/8c; orden de barras: GSM / GSM-Symb / GSM-NoOp / NoOp-Symb / NoOp-NoOp):**
- Phi-3-medium-128k-instruct: "87.3", "82.5", "29.4", "30.2", "22.6"
- Llama3-8b-instruct: "76.0", "74.6", "18.6", "19.6", "19.2"
- Gemma2b: "12.1", "8.2", "4.7", "48.3", "3.1"
- Mistral-7b-v0.1: "44.5", "41.1", "16.2", "62.5", "14.5"
**5.4 hallazgo:** "more recent models experiencing a greater decline than older ones." / "some models that perform significantly worse than those in (b) on GSM8K and GSM-Symbolic show much better performance on NoOp-Symb." / Para Llama-3-8B en NoOp-NoOp: "the performance remains the same compared to the original No-Op model, while for the Phi-3 model, performance slightly decreases."

### 5.5 Tabla 1 (resultados completos 8-shot; columnas: GSM8K Full / GSM8K(100) / Symbolic-M1 / Symbolic / Symbolic-P1 / Symbolic-P2 / Symbolic-NoOp)
Valores exactos del texto (selección íntegra):
- Gemma2b: 12.1 / 11.0 / 24.5(±3.85) / 8.2(±2.21) / 3.6(±2.13) / 1.5(±1.63) / 4.7(±1.99)
- Gemma2b-it: 12.1 / 11.0 / 16.2(±3.28) / 8.2(±2.21) / 1.5(±1.49) / 1.5(±1.63) / 4.1(±2.48)
- Gemma-7b: 53.8 / 50.0 / 34.1(±4.41) / 25.6(±3.25) / 26.0(±5.30) / 3.1(±1.92) / 8.7(±2.71)
- Gemma-7b-it: 29.3 / 33.0 / 34.1(±4.41) / 25.6(±3.25) / 6.0(±3.38) / 3.1(±1.92) / 8.7(±2.71)
- Gemma2-2b: 47.5 / 46.0 / 57.2(±3.40) / 40.1(±3.04) / 19.5(±3.89) / 1.3(±1.37) / 8.8(±4.12)
- Gemma2-2b-it: 47.5 / 46.0 / 57.2(±3.40) / 40.1(±3.04) / 19.5(±3.89) / 4.5(±1.94) / 15.7(±3.97)
- Gemma2-9b: 85.3 / 87.0 / 71.2(±2.81) / 79.1(±2.99) / 44.0(±5.69) / 41.8(±6.00) / 22.3(±5.11)
- Gemma2-9b-it: 85.3 / 87.0 / 84.4(±2.36) / 79.1(±2.99) / 68.1(±4.77) / 41.8(±6.00) / 22.3(±5.11)
- Gemma2-27b-it: 89.7 / 92.0 / 90.2(±1.86) / 88.3(±2.56) / 80.7(±4.07) / 63.4(±4.14) / 30.0(±3.39)
- Phi-2: 56.0 / 53.0 / 53.0(±3.10) / 41.4(±3.56) / 23.3(±4.07) / 8.9(±3.33) / 11.2(±3.51)
- Phi-3-mini-128k-instruct: 83.7 / 85.0 / 85.9(±2.44) / 80.7(±2.94) / 63.4(±5.63) / 37.5(±5.76) / 18.0(±3.83)
- Phi-3-small-128k-instruct: 88.5 / 89.0 / 86.4(±1.95) / 83.7(±2.65) / 72.0(±3.65) / 50.7(±4.99) / 24.5(±4.81)
- Phi-3-medium-128k-instruct: 87.3 / 89.0 / 89.6(±1.65) / 82.5(±2.86) / 75.8(±3.89) / 53.1(±4.80) / 29.4(±4.18)
- Phi-3.5-mini-instruct: 84.9 / 88.0 / 87.6(±1.98) / 82.1(±3.38) / 64.8(±5.43) / 44.8(±6.32) / 22.4(±4.03)
- Mistral-7b-v0.1: 44.5 / 48.0 / 55.4(±3.18) / 41.1(±3.36) / 17.4(±4.82) / 5.5(±2.55) / 16.2(±4.43)
- Mistral-7b-instruct-v0.1: 39.7 / 42.0 / 44.9(±4.29) / 30.5(±3.47) / 13.1(±3.51) / 4.0(±2.24) / 10.1(±3.42)
- Mistral-7b-v0.3: 40.6 / 44.0 / 54.0(±2.95) / 40.0(±4.43) / 15.6(±4.02) / 3.9(±2.31) / 16.7(±4.26)
- Mistral-7b-instruct-v0.3: 56.2 / 56.0 / 62.3(±2.68) / 50.0(±3.49) / 24.5(±4.34) / 10.8(±3.60) / 15.9(±4.44)
- Mathstral-7b-v0.1: 80.1 / 80.0 / 82.9(±2.87) / 74.0(±3.49) / 57.4(±5.20) / 35.5(±5.07) / 20.4(±3.58)
- Llama3-8b: 55.8 / 61.0 / 79.5(±3.62) / 74.6(±2.94) / 53.8(±4.54) / 12.3(±3.43) / 18.6(±3.86)
- Llama3-8b-instruct: 76.0 / 74.0 / 79.5(±3.62) / 74.6(±2.94) / 53.8(±4.54) / 28.3(±4.37) / 18.6(±3.86)
- GPT-4o-mini: 94.2 / 95.0 / 92.5(±1.63) / 91.7(±2.02) / 81.1(±3.05) / 72.4(±4.57) / 54.1(±3.85)
- GPT-4o: 95.2 / 95.0 / 94.4(±1.62) / 94.9(±1.87) / 93.9(±2.59) / 88.0(±3.43) / 63.1(±4.53)
- o1-mini: 95.1 / 93.0 / 94.9(±1.49) / 94.5(±1.58) / 94.3(±2.57) / 89.1(±3.56) / 66.0(±4.60)
- o1-preview: 94.9 / 96.0 / 93.6(±1.68) / 92.7(±1.82) / 95.4(±1.72) / 94.0(±2.38) / 77.4(±3.84)

### 5.6 Significancia estadística (Apéndice A.3, Fig. 10)
"we calculate statistical significance using the one-sample t-test with two-sided alternative hypothesis". P-values reportados (Fig.10): Phi-2 "P-Value <0.001", Mistral-7b-instruct-v0.1 "<0.001", Gemma2-2b-it "<0.001", Gemma2-9b-it "<0.001", Phi-3.5-mini-instruct "<0.001", Mathstral-7b-v0.1 "<0.001", Llama3-8b-instruct "P-Value = 0.13", GPT-4o "P-Value = 0.6", GPT-4o-mini "<0.001". "for an overwhelming majority of models (except Llama3-8B and GPT-4o), the results are statistically significant." Test de normalidad: "all distributions in Fig. 10 pass the normality test (p-value of the normality test = 0.1)."

### 5.7 Ablation aritmética (Apéndice A.6, Tab. 2 — Gemma2-9b-it)
Por dígitos (1 / 2 / 3 / 4 / 5 / All):
- GSM8K: 99.8 / 99.1 / 99.3 / 96.8 / 95.9 / 98.9
- GSM-Symbolic: 99.7 / 99.2 / 97.6 / 97.2 / 99.1 / 98.3
- GSM-P1: 97.5 / 98.6 / 98.7 / 96.2 / 99.5 / 97.4
- GSM-P2: 96.2 / 98.6 / 97.5 / 96.4 / 99.2 / 97.1
Arit. zero-shot (Fig.17, Gemma2-9b-it, dígitos 1–4): Addition "100.0%, 100.0%, 99.9%, 99.2%"; Subtraction "100.0%, 100.0%, 100.0%, 99.3%"; Multiplication "100.0%, 99.6%, 98.6%, 95.8%"; Division "99.8%, 99.3%, 99.5%, 100.0%". Phi-3-medium: Addition "100.0%, 100.0%, 99.6%, 98.7%"; Subtraction "100.0%, 100.0%, 99.7%, 99.0%"; Multiplication "100.0%, 99.8%, 99.5%, 95.5%"; Division "100.0%, 100.0%, 99.9%, 100.0%".

### 5.8 o1-mini / o1-preview (Apéndice A.5, Fig. 12 y 10)
- o1-mini: "GSM8K 93.0" / "GSM-Symbolic 94.5 (±1.6)" / "P-Value <0.001"; por dificultad "GSM-M1 94.9(±1.5)", "GSM-Symb 94.5(±1.6)", "GSM-P1 94.3(±2.6)", "GSM-P2 89.1(±3.6)".
- o1-preview: "GSM8K 96.0" / "GSM-Symbolic 92.7 (±1.8)" / "P-Value <0.001"; por dificultad "GSM-M1 93.6(±1.7)", "GSM-Symb 92.7(±1.8)", "GSM-P1 95.4(±1.7)", "GSM-P2 94.0(±2.4)".

### 5.9 Patrones de tokens (5.X.7)
- "they finish answering the current question and move on to generating the next question, indicated by another 'Q:' generation." Tokens de fin: "‘</s>’ or ‘<|endoftext|>’".
- "this still requires generating vast amounts of tokens to solve a problem".
[No se reportan conteos numéricos de tokens. NO MENCIONADO EN EL TEXTO un análisis cuantitativo de número de tokens generados.]

---

## BLOQUE 6 — HALLAZGOS Y CONCLUSIONES

**6.1 Cada conclusión explícita**
- "Our findings reveal that LLMs exhibit noticeable variance when responding to different instantiations of the same question."
- "the performance of models declines when only the numerical values in the question are altered".
- "their performance significantly deteriorates as the number of clauses in a question increases."
- "We found that while LLMs exhibit some robustness to changes in proper names, they are more sensitive to variations in numerical values."
- "The introduction of GSM-NoOp exposes a critical flaw in LLMs' ability to genuinely understand mathematical concepts and discern relevant information for problem-solving."
- "we demonstrate that LLMs struggle even when provided with multiple examples of the same question or examples containing similar irrelevant information. This suggests deeper issues in their reasoning processes that cannot be easily mitigated through few-shot learning or fine-tuning."

**6.2 Frases textuales más importantes**
- "We hypothesize that this decline is due to the fact that current LLMs are not capable of genuine logical reasoning; instead, they attempt to replicate the reasoning steps observed in their training data."
- "their reasoning is fragile and may be more akin to sophisticated pattern matching rather than true logical reasoning."
- "models tend to convert statements to operations without truly understanding their meaning."
- "We believe further research is needed to develop AI systems capable of formal reasoning, moving beyond probabilistic pattern matching".

**6.3 Qué confirma del paper previo / literatura**
- "This aligns with our results" (sobre Jiang et al. 2024 y token bias).
- "Our findings in this work support the hypothesis that current LLMs are not capable of performing formal mathematical reasoning".
- Sobre el riesgo de contaminación de GSM8K: "hinting at potential data contamination."

**6.4 Qué refuta/matiza**
- Matiza la fiabilidad de GSM8K: "We question the reliability of currently reported results on GSM8K".
- Matiza/diverge de Ivanova et al. (2025): "we hold a fundamentally different philosophical view of reasoning than Ivanova et al. (2025)." y reconoce: "if one disagrees with our assumptions and accepts the assumptions of Ivanova et al. (2025), our results would likewise be statistically non-significant".

**6.5 Postura final sobre si los modelos razonan**
"Ultimately, our work underscores significant limitations in LLMs' ability to perform genuine mathematical reasoning." / "their reasoning is fragile and may be more akin to sophisticated pattern matching rather than true logical reasoning." / "current LLMs are not capable of genuine logical reasoning".

**6.6 Implicaciones filosóficas/cognitivas**
- "This distinction aligns with ideas akin to the Chinese Room Argument (Cole, 2024), underscoring the difference between true comprehension and pattern-matching."
- "this level of variability would not be expected from a grade-school student with genuine mathematical understanding."
- "This remains a critical challenge for the field as we strive to create systems with human-like cognitive abilities or general intelligence."
- Argumento del razonador ideal (Apéndice B): "for a \"true reasoner,\" P(x = true | o = true) should follow a Bernoulli distribution with p = 1, and P(x = true | o = false) should follow a Bernoulli distribution with p = 0".

---

## BLOQUE 7 — CONCEPTOS TÉCNICOS

**7.1 Logical reasoning:** "We define logical reasoning as the process by which an agent (a human or a machine) employs logical steps to achieve a \"novel\" goal." Uso: marco para distinguir razonamiento genuino de memorización.

**7.2 Novelty (énfasis):** "The emphasis on \"novelty\" is crucial because it helps distinguish genuine reasoning from mere memorization of solutions or responses, or mimicking the logical steps previously encountered".

**7.3 Length-generalization:** "the \"length-generalization\" refers to the ability to apply known logical steps on larger inputs."

**7.4 Decomposing / Composing:** "\"decomposing\" a problem into smaller sub-problems, and \"composing\" logical steps from these sub-problems in order to solve another problem."

**7.5 Probabilistic pattern-matching:** "LLMs likely perform a form of probabilistic pattern-matching and searching to find closest seen data during training without proper understanding of concepts." / "the reasoning process in LLMs is probabilistic pattern-matching rather than formal reasoning (Jiang et al., 2024)."

**7.6 Token bias:** "most LLMs still struggle with logical reasoning due to strong token bias, where the reasoning output of the model changes when a single token of input changes."

**7.7 Chain-of-Thought (CoT) prompting:** "the effectiveness of Chain-of-Thought (CoT) prompting (Wei et al., 2022) and using scratchpads for LLMs as additional memory for intermediate computations." Uso: setup de evaluación "8-shots with greedy decoding".

**7.8 GSM-NoOp / No-Op:** "we add seemingly relevant but ultimately inconsequential statements to GSM-Symbolic templates. Since these statements carry no operational significance, we refer to them as \"No-Op\"."

**7.9 Variance (varianza de desempeño):** "LLMs exhibit noticeable variance when responding to different instantiations of the same question." Uso: métrica central; aumenta con la dificultad.

**7.10 Data contamination:** "where some of the test examples from GSM8K inadvertently ended up in the training set of these models, leading to an optimistic bias in performance."

**7.11 Degenerate distribution vs. Bernoulli (Apéndice B):** "we do not believe the performance of an ideal reasoner... should follow a Bernoulli distribution. Rather... a degenerate distribution would be a more appropriate model."

**7.12 Intermediate answer:** "\"intermediate\" refers to the result of each intermediate operation throughout the solution process. For example, if a solution step involves 12 × 6 = 72, we categorize this as a two-digit multiplication."

**7.13 LLM (Large Language Models):** "Large Language Models (LLMs) have demonstrated remarkable capabilities across various domains, including natural language processing, question answering, and creative tasks". [Definición formal precisa: NO MENCIONADO EN EL TEXTO]

---

## BLOQUE 8 — REFERENCIAS (citadas en el cuerpo)

> Contexto = cómo las usa el cuerpo del texto.

- **Cobbe et al. (2021)** — "Training verifiers to solve math word problems. arXiv preprint arXiv:2110.14168, 2021." Contexto: origen del dataset GSM8K.
- **Jiang et al. (2024)** — "A peek into token bias: Large language models are not yet genuine reasoners. CoRR, abs/2406.11050, 2024." Contexto: pattern-matching probabilístico y token bias.
- **Shi et al. (2023)** — "Large language models can be easily distracted by irrelevant context. ICML 2023, pp. 31210–31227." Contexto: GSM-IC y contexto irrelevante.
- **Schaeffer et al. (2023)** — "Are emergent abilities of large language models a mirage?, 2023." Contexto: probabilidad decae exponencialmente con número de tokens.
- **Newell & Simon (1956)** — "The logic theory machine... IRE Transactions on information theory, 2(3):61–79, 1956." Contexto: razonamiento como meta de la IA.
- **Marcus (2003)** — "The algebraic mind... MIT press, 2003." Contexto: ídem.
- **Brachman & Levesque (2004)** — "Knowledge representation and reasoning. Elsevier, 2004." Contexto: ídem.
- **Legg & Hutter (2007)** — "Universal intelligence... Minds and machines, 17:391–444, 2007." Contexto: ídem.
- **Pearl (2014)** — "Probabilistic reasoning in intelligent systems... Elsevier, 2014." Contexto: ídem.
- **Chollet (2019)** — "On the measure of intelligence. arXiv:1911.01547, 2019." Contexto: ídem.
- **Gignac & Szodorai (2024)** — "Defining intelligence... Intelligence, 2024." Contexto: distinción razonamiento vs memorización.
- **Cole (2024)** — "The Chinese Room Argument. Stanford Encyclopedia of Philosophy." Contexto: comprensión real vs pattern-matching.
- **Weiss et al. (2021)** — "Thinking like transformers. ICML 2021, pp. 11080–11090." Contexto: primitivas computacionales en transformers.
- **Zhou et al. (2024)** — "What algorithms can transformers learn? A study in length generalization. ICLR 2024." Contexto: ídem / length generalization.
- **Delétang et al. (2023)** — "Neural networks and the chomsky hierarchy. ICLR 2023." Contexto: transformers fallan en tareas no regulares; necesidad de memoria estructurada.
- **Wei et al. (2022)** — "Chain-of-thought prompting... arXiv:2201.11903, 2022." Contexto: CoT.
- **Zubic et al. (2025)** — "Limits of deep learning... ICLR 2025." Contexto: SSMs y Transformers con límites en composición de funciones.
- **Liu et al. (2024)** — "Chain of thought empowers transformers to solve inherently serial problems. ICLR 2024." Contexto: scratchpads alivian limitaciones.
- **Peng et al. (2024)** — "On limitations of the transformer architecture. CoRR abs/2402.08164, 2024." Contexto: generar muchos tokens.
- **OpenAI (2024)** — "Learning to reason with large language models. https://openai.com/index/learning-to-reason-with-llms/, 2024." Contexto: serie o1; generación de tokens.
- **Kambhampati (2024)** — "Can large language models reason and plan? Annals of the NY Academy of Sciences, 1534:15–18, 2024." Contexto: razonamiento frágil/no formal.
- **Valmeekam et al. (2022)** — "Large language models still can't plan... CoRR abs/2206.10498, 2022." Contexto: ídem.
- **Valmeekam et al. (2024)** — "Llms still can't plan; can lrms?... 2024." Contexto: ídem (o1 en PlanBench).
- **Nezhurina et al. (2024)** — "Alice in wonderland... arXiv:2406.02061, 2024." Contexto: fragilidad de razonamiento en tareas simples.
- **McCoy et al. (2023)** — "Embers of autoregression... arXiv 2309.13638, 2023." Contexto: ídem.
- **Zhang et al. (2023)** — "On the paradox of learning to reason from data. IJCAI-23, pp. 3365–3373." Contexto: razonamiento no formal.
- **Boix-Adserà et al. (2024)** — "When can transformers reason with abstract symbols? ICLR 2024." Contexto: comprensión limitada de símbolos.
- **Li et al. (2024b)** — "One-layer transformer provably learns one-nearest neighbor in context. 2024b." Contexto: sensibilidad a tokens.
- **Dziri et al. (2023)** — "Faith and fate: Limits of transformers on compositionality, 2023." Contexto: subgrafos de cómputo en datos de entrenamiento.
- **Razeghi et al. (2022)** — "Impact of pretraining term frequencies on few-shot reasoning. arXiv:2202.08904, 2022." Contexto: correlación frecuencia-rendimiento.
- **Stolfo et al. (2023)** — "A causal framework to quantify the robustness... ACL 2023, pp. 545–561." Contexto: sensibilidad/robustez a intervenciones.
- **Hong et al. (2024)** — "Evaluating llms' mathematical and coding competency through ontology-guided interventions. arXiv:2401.09395, 2024." Contexto: ontología para perturbar GSM8K.
- **Srivastava et al. (2024)** — "Functional benchmarks for robust evaluation... arXiv 2402.19450, 2024." Contexto: variante funcional de MATH.
- **Ye et al. (2024)** — "Physics of language models: Part 2.1... arXiv:2407.20311, 2024." Contexto: iGSM.
- **Li et al. (2024a)** — "Gsm-plus... ACL 2024, pp. 2961–2984." Contexto: GSM-Plus.
- **Zhang et al. (2024)** — "A careful examination of large language model performance on grade school arithmetic. CoRR abs/2405.00332, 2024." Contexto: GSM1K.
- **Ivanova et al. (2025)** — "Towards more rigorous evaluations of language models. ICLR Blogposts 2025." URL "https://iclr-blogposts.github.io/2025/blog/towards-more-rigorous-llm-evals/". Contexto: crítica estadística (t-test vs z-test, no significancia).
- **Modelos citados:** Gunter et al. (2024) Apple intelligence foundation models; OpenAI (2023) GPT-4; Dubey et al. (2024) Llama 3; Anil et al. (2023) Gemini; Abdin et al. (2024) Phi-3; Rivière et al. (2024) Gemma 2; Mesnard et al. (2024) Gemma; Jiang et al. (2023) Mistral 7b.

---

## BLOQUE 9 — FIGURAS Y TABLAS

- **Figura 1:** "Illustration of the GSM-Symbolic template creation process. This dataset serves as a tool to investigate the presumed reasoning capabilities of LLMs... Our results reveal that all state-of-the-art LLMs exhibit significant performance variations, suggesting the fragility or lack of reasoning." Variables: template con {name},{family},{x},{y},{z},{total},{ans}.
- **Figura 2:** "8-shot CoT performance across 50 sets generated from GSM-Symbolic templates. All state-of-the-art models exhibit notable variance in accuracy. It is interesting that for the majority of the models, the performance on GSM8K (represented by dashed line) falls on the right side of the distribution, which statistically speaking, should have a very low likelihood." Variables: accuracy(%) vs frequency.
- **Figura 3:** "The performance of all state-of-the-art models on GSM-Symbolic drops compared to GSM8K. Later, we investigate the factors that impact the performance drops in more depth." Variable: "GSM8K →GSM-Symbolic Accuracy Drop (%)".
- **Figura 4:** "How sensitive are LLMs when we change only names, only proper numbers, or both names and numbers? Overall, models have noticeable performance variation even if we only change names, but even more when we change numbers or combine these changes."
- **Figura 5:** "Modifying the difficulty level of GSM-Symbolic by modifying the number of clauses." (ejemplos M1/Symbolic/P1/P2).
- **Figura 6:** "The impact of increasing the number of clauses on performance: As the difficulty increases from GSM-M1→GSM-Symb→GSM-P1→GSM-P2, the distribution of performance shifts to the left (i.e., accuracy decreases), and the variance increases."
- **Figura 7:** "An example from the GSM-NoOp dataset: We add seemingly relevant statements to the questions that are, in fact, irrelevant to the reasoning and conclusion. However, the majority of models fail to ignore these statements and blindly convert them into operations, leading to mistakes." (ejemplo kiwis; respuestas o1-mini y Llama3-8B, ambas → 185).
- **Figura 8:** "(a) The performance of models drops significantly on GSM-NoOp, with more recent models experiencing a greater decline than older ones. (b) ... the significant drop in performance cannot be recovered, even when using the exact same question's variation as shots (NoOp-Symb) or when using different questions... (NoOp-NoOp) as shots. (c) Notably, some models that perform significantly worse than those in (b)... show much better performance on NoOp-Symb."
- **Figura 9:** "The prompt format used for evaluations." (preamble + 8 shots + target).
- **Figura 10:** "Additional results on performance variation on GSM-Symbolic." (con P-values).
- **Figura 11:** "Using in-context shots or finetuning on GSM-P1 does not improve performance on GSM-P2: (a)... (b) Finetuning on GSM-P1 can improve performance on GSM-P1 but not on GSM-P2."
- **Figura 12:** "Results on o1-mini and o1-preview: both models mostly follow the same trend... However, o1-preview shows very strong results on all levels of difficulty as all distributions are close to each other."
- **Figura 13:** "Sample response from o1-preview on an example from GSM-NoOp: the model blindly applies the inflation rate, even though the inflation amount is irrelevant as the question clearly indicates the given prices are for \"now\" and not last year." (resultado erróneo: $261.90).
- **Figura 14:** "Sample response from o1-preview and o1-mini on an example from GSM-NoOp: while the donation amount is irrelevant to the price difference, the models subtract the amount we donate." (resultado erróneo: $39).
- **Figura 15:** "Statistics of the number of digits in the final answer for questions in GSM8K-test, GSM-Symbolic, GSM-P1, and GSM-P2... the range of numbers does not increase significantly, with a significant majority of the final answers containing fewer than 5 digits."
- **Figura 16:** "Statistics on the Number of Digits in Intermediate answers: Compared to GSM8K, GSM-Symbolic and its variants involve operations that result in 3-digit numbers. However... modern LLMs are well capable of performing arithmetic within this range." (operaciones div/mul/sub/add).
- **Figura 17:** "Arithmetic accuracy of Gemma2-9B and Phi3-Medium: ... The addition accuracy of the models remains nearly perfect for calculations involving up to 4 digits... Although GSM-P1 and GSM-P2 have a similar digit-length distribution to GSM-Symbolic... the performance drop is significant."
- **Figura 18:** "(a) The probability of answering each GSM-Name question correctly deviates from the uniform assumption of pm. (b) The probability of answering GSM-Name questions correctly, conditioned on the model answering the original 100 GSM8K questions correctly, does not align with the expected behavior (i.e., Bernoulli with p = 1)".
- **Tabla 1:** "Full 8-shot results of all models on GSM8K and different variants of GSM-Symbolic." (valores en Bloque 5.5).
- **Tabla 2:** "Ablation: Arithmetic accuracy of Gemma2-9b-it on different GSM benchmarks." (valores en Bloque 5.7).

---

## BLOQUE 10 — GAPS Y TRABAJO FUTURO

**10.1 Limitaciones reconocidas**
- "This suggests deeper issues in their reasoning processes that cannot be alleviated by in-context shots and needs further investigation."
- Sobre i.i.d./significancia: "this requires an i.i.d. assumption on the questions and the model accuracy for each question, which may not necessarily hold and needs further investigation."
- "we acknowledge that we should have articulated our assumptions more clearly in the original version."
- "adding or removing a clause does not necessarily correspond to increasing or decreasing the number of required reasoning steps by exactly one."

**10.2 Trabajo futuro**
- "We believe further research is needed to develop AI systems capable of formal reasoning, moving beyond probabilistic pattern matching to achieve more robust and generalizable problem-solving skills."
- "Our results emphasize the need for more reliable evaluation methodologies and further research into the reasoning capabilities of large language models."
- "while this direction warrants further research, current results suggest that scaling training data will not be helpful in improving the reasoning capabilities of language models."

**10.3 Preguntas abiertas**
- "the question of whether current LLMs are genuinely capable of true logical reasoning remains an important research focus."
- "in practice, it remains unclear whether these LLMs can perform formal logical reasoning to solve tasks."
- "This raises the question of whether these models have truly understood the mathematical concepts well enough."
- "it is up to the reader to decide whether our stated assumptions are valid, or whether the statistical assumptions proposed by Ivanova et al. (2025) offer a better foundation for interpretation."

**10.4 Código/recursos (URLs exactas)**
- "GSM-Symbolic templates and generated data are available at: https://github.com/apple/ml-gsm-symbolic"
- Correspondencia: "{imirzadeh,farajtabar}@apple.com"

---

## VERIFICACIÓN — 5 datos más difíciles de encontrar (con cita textual)

1. **Número de plantillas, muestras y total de evaluaciones:** "we conducted nearly 500 total evaluations on various setups. To this end, we maintained a manageable dataset size by using 100 templates and generating 50 samples per template, resulting in 5000 total examples for each benchmark."

2. **Caída máxima exacta en GSM-NoOp (modelo y valor):** "-65.7 Phi-3-mini-128k-instruct" (Fig. 8a) y "with the Phi-3-mini model experiencing over a 65% drop".

3. **Conjunto de fine-tuning del ablation (A.4):** "We have used a set of 50 templates from GSM-P1, separate from the test templates, and generated 10000 examples for finetuning training set."

4. **Concesión sobre significancia estadística frente a Ivanova et al. (2025):** "if one disagrees with our assumptions and accepts the assumptions of Ivanova et al. (2025), our results would likewise be statistically non-significant, as those authors have shown."

5. **Proporción de modelos cuyo punto GSM8K cae a la derecha de la distribución:** "the performance... on the original questions... is often more than one standard deviation away from the center of the GSM-Symbolic performance distribution, frequently on the right side of the distribution (this holds for 21 out of 25 models)."

# Extracción académica — "Embers of autoregression show how large language models are shaped by the problem they are trained to solve"

> Extracción literal del documento. Solo se incluye lo que el texto dice explícitamente. Citas entre comillas dobles "...".

---

## BLOQUE 1 — IDENTIDAD

**1.1 Título completo**
"Embers of autoregression show how large language models are shaped by the problem they are trained to solve"

**1.2 Autores en orden**
1. R. Thomas McCoy
2. Shunyu Yao
3. Dan Friedman
4. Mathew D. Hardy
5. Thomas L. Griffiths

**1.3 Afiliación de cada autor**
El texto marca afiliaciones con superíndices: "R. Thomas McCoya,1,2,3, Shunyu Yaoa,4, Dan Friedmana, Mathew D. Hardyb, and Thomas L. Griﬀithsa,b".
- Superíndice a: "aDepartment of Computer Science, Princeton University, Princeton, NJ 08542"
- Superíndice b: "bDepartment of Psychology, Princeton University, Princeton, NJ 08542"
- Asignación: McCoy (a), Yao (a), Friedman (a), Hardy (b), Griffiths (a,b).
- Notas adicionales sobre McCoy (1,2,3): "1To whom correspondence may be addressed. Email: tom.mccoy@yale.edu."; "2Present address: Department of Linguistics, Yale University, New Haven, CT 06520."; "3Present address: Wu Tsai Institute, Yale University, New Haven, CT 06520."
- Nota sobre Yao (4): "4Present address: OpenAI, San Francisco, CA 94110."

**1.4 Fecha**
- "received December 19, 2023; accepted August 9, 2024"
- "Published October 4, 2024."
- "PNAS 2024 Vol. 121 No. 41 e2322420121"
- Editor: "Edited by Richard Shiﬀrin, Indiana University Bloomington, Bloomington, IN".

**1.5 DOI/arXiv/id**
- DOI: "https://doi.org/10.1073/pnas.2322420121"
- Artículo: "e2322420121"
- SI Appendix: "https://www.pnas.org/lookup/suppl/doi:10.1073/pnas.2322420121/-/DCSupplemental."

**1.6 Financiamiento**
"R.T.M. was supported by the NSF Social, Behavioral, and Economic Sciences Postdoctoral Research Fellowship under Grant No. 2204152, S.Y. was supported by the Harold W. Dodds Fellowship from Princeton, and M.D.H. was supported by the US Department of Defense through a National Defense Science and Engineering Graduate Fellowship."

**1.7 Agradecimientos**
"We thank Robert Frank, Tania Lombrozo, Dakota McCoy, Benjamin Riley, Paul Smolensky, and Cameron Turner for helpful discussion. Any errors are our own."

**Declaración de intereses en competencia (presente en el texto):** "D.F. was previously aﬀiliated with Google, which created one model that we evaluated (Gemini 1.0). S.Y. is aﬀiliated with OpenAI, which created two models that we evaluated (GPT-3.5 and GPT-4)."
**Copyright/licencia:** "Copyright © 2024 the Author(s). Published by PNAS." / "Creative Commons Attribution License 4.0 (CC BY)." / "This article is a PNAS Direct Submission."

---

## BLOQUE 2 — CONTEXTO Y MOTIVACIÓN

**2.1 Trabajo previo que motiva (título, autores, año)**
- Trabajo central conectado: "Sparks of artiﬁcial general intelligence: Early experiments with GPT-4", S. Bubeck et al., arXiv [Preprint] (2023), ref. (4). El texto dice: "it led one recent paper to argue that LLMs display "sparks of artiﬁcial general intelligence" (4)". Y "GPT-4 ... is the focus of the "sparks of AGI" paper (4) that our work connects to."
- Trabajo contemporáneo con conclusiones similares: Wu et al. (42): "Reasoning or reciting? Exploring the capabilities and limitations of language models through counterfactual tasks" in Proceedings of NAACL (2024). El texto dice: "Contemporaneous work by Wu et al. (42) drew similar conclusions".

**2.2 Hallazgos de ese trabajo según este documento**
- Sobre "Sparks of AGI" (4): "Section 8 is titled "Limitations of autoregressive architecture highlighted by GPT-4," and it considers failures of planning in arithmetic and text generation that result from only predicting the next word in a sequence."
- Sobre Wu et al. (42): "they found that LLMs performed better on the default version of a task (e.g., executing Python code under the true assumption that Python uses 0-based indexing) than on a counterfactual version of the task (e.g., falsely assuming that Python uses 1-based indexing)."

**2.3 Controversia si la menciona**
El texto cita un trabajo titulado: "The debate over understanding in AI's large language models. Proc. Natl. Acad. Sci. U.S.A." (ref. 45, Mitchell, D. C. Krakauer, 2023), referenciado en el contexto de "difﬁculty on tasks that depend on meaning". No se desarrolla una controversia explícita más allá de esta cita. [No se presenta una sección de controversia con posiciones enfrentadas explícitamente etiquetadas como tal en el cuerpo principal.]

**2.4 Posiciones del debate y quién las sostiene**
- Posición "sparks of artiﬁcial general intelligence": atribuida a "one recent paper" (4) (Bubeck et al.). El texto contrapone su propia metáfora: "the embers of autoregression that appear in these systems even as they might show sparks of artiﬁcial general intelligence."
- Enfoques de evaluación contrastados por los autores: el "human-centric approach" vs. el "teleological approach" (propio de los autores); y "desideratum-focused evaluation" vs. "teleological approach".

**2.5 Medios mencionados**
[NO MENCIONADO EN EL TEXTO] (no se mencionan medios de prensa). Se mencionan fuentes de datos/servicios: "Global Voices, a news service that shares its content under a permissive license"; corpus C4 (36); the Pile (41); WikiBio (78); CMU Pronouncing Dictionary.

**2.6 Objetivo declarado**
- "We argue that to develop a holistic understanding of these systems, we must consider the problem that they were trained to solve: next-word prediction over Internet text."
- "Using this approach—which we call the teleological approach—we identify three factors that we hypothesize will inﬂuence LLM accuracy: the probability of the task to be performed, the probability of the target output, and the probability of the provided input."
- "To test our predictions, we evaluate ﬁve LLMs (GPT-3.5, GPT-4, Claude 3, Llama 3, and Gemini 1.0) on 11 tasks".
- "our goal is to identify sources of difﬁculty for LLMs".
- "our goal is to promote a perspective that accurately captures the properties of LLMs, both positive properties and negative ones."

**2.7 Qué dice que NO pretende hacer**
- "We do not claim that LLMs are incapable of handling these tasks and examples. That is, our predictions are of the form "for LLMs, X is harder than Y" rather than "LLMs can't do X.""
- "we are not claiming that researchers have ignored the autoregressive origins of LLMs."
- "We do not claim to be highlighting fundamental incapabilities of LLMs".
- "being critical of LLMs is not our goal."
- "we are not arguing against testing for desiderata".
- "we do not claim that our tasks are impossible for AI."
- Alcance limitado declarado: "In this paper, we only analyze next-word prediction, leaving instruction tuning for future work."; "In this paper, we only consider LLMs that process text sequences".

---

## BLOQUE 3 — BENCHMARKS Y TAREAS

El texto enumera las tareas en Table 2 ("The tasks that we used to evaluate LLMs"). Se evaluaron sobre "11 tasks". Nota de Table 2: "To keep this table manageably sized, some of the examples are not from the datasets that we used to evaluate LLMs but are instead shorter examples of the tasks that those datasets target."

**3.1 ARTICLE SWAPPING (intercambio de artículos)**
- 3.1.1 Descripción: "Swap each article (a, an, or the) with the preceding word."
- 3.1.2 Regla/ejemplo: "In box the I saw key a. → In the box I saw a key."
- 3.1.3 Fórmula de dificultad: [NO MENCIONADO EN EL TEXTO]
- 3.1.4 Resultados de trabajo previo: [NO MENCIONADO EN EL TEXTO]
- 3.1.5 Fallas metodológicas señaladas: [NO MENCIONADO EN EL TEXTO]
- 3.1.6 Criterios de resolubilidad: tarea determinista de manipulación; en Fig. 2 GPT-4 "fails in the cases where the correct output is a low-probability piece of text".

**3.2 REVERSAL (inversión)**
- 3.2.1 Descripción: "Reverse a sequence of words."
- 3.2.2 Regla/ejemplo: "everyone! morning, Good → Good morning, everyone!"
- 3.2.3 Fórmula: [NO MENCIONADO EN EL TEXTO]
- 3.2.4 Trabajo previo: [NO MENCIONADO EN EL TEXTO]
- 3.2.5 Fallas: [NO MENCIONADO EN EL TEXTO]
- 3.2.6 Resolubilidad: usada como ejemplo de tarea "not inherently probabilistic, such as reversing a list."

**3.3 COUNTING (conteo)**
- 3.3.1 Descripción: "Count the words or letters in a list."
- 3.3.2 Regla/ejemplo: "lively news exhibit steep → 4"
- 3.3.3 Fórmula: [NO MENCIONADO EN EL TEXTO]. El análisis usa la frecuencia del número objetivo: "LLMs often show spikes in accuracy for the numbers that are most frequent in corpora, namely multiples of 10."
- 3.3.4 Trabajo previo: [NO MENCIONADO EN EL TEXTO]
- 3.3.5 Fallas: [NO MENCIONADO EN EL TEXTO]
- 3.3.6 Resolubilidad: en Fig. 2, "we refer to 29 as low-probability because it occurs much less frequently in natural corpora than 30 does".

**3.4 ACRONYMS (acrónimos)**
- 3.4.1 Descripción: "Join the first letters of the words in a list."
- 3.4.2 Regla/ejemplo: "view inch show into tray → VISIT". Variante común: primera letra (ej.: "producing RESPOND from revolve ediﬁce scrappy panicky outlast negated drizzle"). Variante rara: segunda letra (ej.: "producing RESPOND from prequel leaping ascetic splurge policed invader ediﬁce").
- 3.4.3 Fórmula: [NO MENCIONADO EN EL TEXTO]
- 3.4.4 Trabajo previo: el texto relaciona con "last-letter concatenation, which is similar to our acronym task" (en contexto del chain-of-thought de Wei et al. (26)).
- 3.4.5 Fallas: [NO MENCIONADO EN EL TEXTO]
- 3.4.6 Resolubilidad: tarea común (primera letra) vs. rara (segunda letra).

**3.5 LINEAR FUNCTION (función lineal)**
- 3.5.1 Descripción: "Apply the function f (x) = (9/5)x + 32."
- 3.5.2 Regla/ejemplo: "328 → 622.4". Función común: "f (x) = (9/5)x + 32" (conversión Celsius a Fahrenheit). Función rara: "f (x) = (7/5)x + 31, which has no special signiﬁcance".
- 3.5.3 Fórmula matemática: común "f (x) = (9/5)x + 32"; rara "f (x) = (7/5)x + 31".
- 3.5.4 Trabajo previo: [NO MENCIONADO EN EL TEXTO]
- 3.5.5 Fallas: [NO MENCIONADO EN EL TEXTO]
- 3.5.6 Resolubilidad: "this function occurs frequently in natural text because it is the function that converts temperatures from Celsius to Fahrenheit".

**3.6 MULTIPLICATION (multiplicación)**
- 3.6.1 Descripción: "Multiply two three-digit numbers."
- 3.6.2 Regla/ejemplo: "351 times 373 → 130923"
- 3.6.3 Fórmula: [NO MENCIONADO EN EL TEXTO]
- 3.6.4 Trabajo previo: [NO MENCIONADO EN EL TEXTO]
- 3.6.5 Fallas: [NO MENCIONADO EN EL TEXTO]
- 3.6.6 Resolubilidad: entradas "sampled uniformly from the integers from 100 to 999".

**3.7 SORTING (ordenamiento)**
- 3.7.1 Descripción: "Sort a list of words in alphabetical order."
- 3.7.2 Regla/ejemplo: "into, trek, game, magic → game, into, magic, trek". Variante común: orden alfabético; variante rara: orden alfabético inverso ("reverse alphabetical order").
- 3.7.3 Fórmula: [NO MENCIONADO EN EL TEXTO]
- 3.7.4 Trabajo previo: [NO MENCIONADO EN EL TEXTO]
- 3.7.5 Fallas: [NO MENCIONADO EN EL TEXTO]
- 3.7.6 Resolubilidad/frecuencia: "we estimate that alphabetical order is 150 times more common than reverse alphabetical order in Internet text."

**3.8 KEYBOARD CIPHER (cifrado de teclado)**
- 3.8.1 Descripción: "Replace each letter with the one to the right of it on a keyboard."
- 3.8.2 Regla/ejemplo: "Hello world! → Jraap eptaf!"
- 3.8.3 Fórmula: [NO MENCIONADO EN EL TEXTO]
- 3.8.4 Trabajo previo: [NO MENCIONADO EN EL TEXTO]
- 3.8.5 Fallas: [NO MENCIONADO EN EL TEXTO]
- 3.8.6 Resolubilidad: tarea que requería ejemplo en el prompt ("namely, article swapping, reversal, the keyboard cipher, shift ciphers, and Pig Latin").

**3.9 SHIFT CIPHER (cifrado por desplazamiento)**
- 3.9.1 Descripción (Table 2): "Decode by shifting each letter 13 positions backward in the alphabet." Definición ampliada: "In a shift cipher, a message is encoded by shifting each letter forward in the alphabet a certain number of positions."
- 3.9.2 Reglas/ejemplo: "Fgnl urer! → Stay here!". Ejemplo de shift 1: "with a shift of 1, How are you? becomes Ipx bsf zpv?". Rot-13: "rot-13 (short for "rotate by 13"), the cipher with a shift of 13 positions." "There are 25 possible shift ciphers, corresponding to the 25 unique shifts that can be applied within the alphabet."
- 3.9.3 Fórmula de dificultad: no hay fórmula numérica; algoritmo de resolución descrito: "The most straightforward way to decode this cipher is to shift each letter back n positions—an algorithm that succeeds regardless of the value of n and the identity of the words being processed." Frecuencias de shifts según corpus C4: "the three most common shift levels are rot-1, rot-3, and rot-13".
- 3.9.4 Trabajo previo: [NO MENCIONADO EN EL TEXTO] (es ejemplo propio de los autores).
- 3.9.5 Fallas metodológicas: [NO MENCIONADO EN EL TEXTO]
- 3.9.6 Resolubilidad: determinista. Causas de frecuencia: rot-1 "is the smallest shift"; rot-3 "Julius Caesar famously used this cipher"; rot-13 "convention of using it in online forums". Fig. 2: "the shift cipher with a shift of 13 is over 100 times more common in Internet text than the shift cipher with a shift of 12".

**3.10 PIG LATIN**
- 3.10.1 Descripción (Table 2): "Move the first consonant cluster of each word to the end and add −ay." Ampliada: "the ﬁrst consonant cluster of each word is moved to the end of the word and then -ay is added to the end of the word."
- 3.10.2 Reglas/ejemplo: "frogs aren't noisy. → ogsfray aren'tay oisynay." Ejemplo: "the English word main would become ainmay in Pig Latin or ainmuv in Boar Etruscan." Variante inventada rara: "Boar Etruscan that instead uses -uv as the letter pair that is added at the end." Variantes por sílaba añadida en palabras con vocal inicial: "-way", "-ay", "-yay", "-hay" y una quinta "-say".
- 3.10.3 Fórmula: [NO MENCIONADO EN EL TEXTO]. Frecuencias en the Pile: "68 cases where the added syllable was -way, 46 where it was -ay, 26 where it was -yay, and 8 where it was -hay"; "-say (which has 0 occurrences in C4 and the Pile)."
- 3.10.4 Trabajo previo: cita ref. (40) Vaux & Nevins, "Underdetermination in language games: Survey & analysis of Pig Latin dialects".
- 3.10.5 Fallas: [NO MENCIONADO EN EL TEXTO]
- 3.10.6 Resolubilidad: variantes "treat most words identically because they differ only for vowel-initial words; and even in these cases, they differ from each other only in a single letter."

**3.11 BIRTHDAYS (cumpleaños)**
- 3.11.1 Descripción: "Return the birth date of a provided public figure."
- 3.11.2 Regla/ejemplo: "Jeremy Lin → August 23, 1988"
- 3.11.3 Fórmula: [NO MENCIONADO EN EL TEXTO]
- 3.11.4 Trabajo previo: situaciones análogas referidas a "arithmetic (33) and factual recall (34, 35)."
- 3.11.5 Fallas: [NO MENCIONADO EN EL TEXTO]
- 3.11.6 Resolubilidad: "the answer cannot be deduced from the input alone, so the only way it can be produced is if the model has encountered it during training."

> Tareas adicionales mencionadas en texto/figuras pero no listadas como entradas independientes en Table 2: "multiplication" (sí en Table 2). Fig. 2 menciona "counting, article swapping, shift ciphers, and linear functions". El texto principal usa "constructing acronyms, calculating linear functions, and counting" y "using simple ciphers".

---

## BLOQUE 4 — METODOLOGÍA

**4.1 Modelos usados (nombres y versiones exactos)**
- Cinco modelos evaluados: "GPT-4 (1), GPT-3.5 (1), Claude 3 (2), Llama 3 (3), and Gemini 1.0 (28)."
- Versiones exactas con timestamp: "gpt-3.5-turbo-0613, gpt-4-0613, claude-3-opus-20240229, gemini-1.0-pro-001, and llama-3-70b-chat-hf."
- En Fig. 2: "The GPT-4 predictions were obtained using gpt-4-0613 on the OpenAI API".
- Modelos de prueba preliminar (descartados): "the smaller-scale models OLMo (29) and Llama 2 (3), but their scores were too low to yield meaningful trends, with accuracies of 0% on most tasks."
- APIs: "the OpenAI API for the GPT models, the Claude API for Claude 3, the Gemini API for Gemini 1.0, and the together.ai API for Llama 3."

**4.2 Justificación de la selección de modelos**
- "GPT-4 is the state-of-the-art in many areas and is the focus of the "sparks of AGI" paper (4) that our work connects to."
- "GPT-3.5 is similar to GPT-4 but smaller, enabling us to investigate the effects of model scale."
- "The remaining models are other prominent LLMs."

**4.3 Estrategias/experimentos con nombre**
- Estrategia general: "an adversarial strategy that follows straightforwardly from our hypotheses: we use tasks that push LLMs into low-probability situations where we expect they will perform poorly."
- Bloques experimentales: "Sensitivity to Output Probability", "Sensitivity to Input Probability", "Sensitivity to Task Probability".
- Subanálisis: "Analysis of Shift Cipher Errors", "Counting".
- Experimentos en Discussion / SI: "chain-of-thought prompting and step-by-step prompting" en GPT-4 sobre shift ciphers; few-shot learning; spelling test (SI Appendix, section L).

**4.4 Detalle por experimento**

4.4.a Paso a paso (estímulos):
- "For sentence-based tasks, the high-probability stimuli were sentences from Global Voices".
- "Medium-probability sentences were created by taking the high-probability sentences and using RoBERTa (77) to replace some of the words with others that had a low probability in that context (but were still grammatical)."
- "Low-probability sentences were created by shufﬂing the words of the medium-probability examples, except that the ﬁrst and last words were left in place."
- "For tasks based on words, the words were drawn from the CMU Pronouncing Dictionary".
- "For the birthday task, public ﬁgures and their birthdays were obtained from the WikiBio dataset (78)."
- Estimación de probabilidad de salida: "probabilities were estimated using GPT-2 (15); see SI Appendix, section J".
- Análisis de errores de shift cipher (output): "we gave models messages encoded with a shift of 13 where the correct answer was created by manually changing one word in a high-probability sentence to a new word that was still grammatical but was now low-probability."

4.4.b Diferencias con métodos previos:
- "Following the "sparks of AGI" paper (4), we do not tune models on these tasks but rather describe the task in the prompt".
- Frente a Wu et al.: "we used corpus analyses to measure task frequency for several of our experiments, a type of analysis that was not used in Wu et al.'s work."
- Uso de basic prompting en lugar de "chain-of-thought prompting (25, 26) or the tree-of-thoughts framework (27)".

4.4.c Parámetros exactos:
- Temperatura: "We used a temperature of 0.0".
- Tamaños muestrales: "The sample size was 1,000 for each condition in the acronym task, 30 for each number in the counting task, and 100 for each condition in all other tasks."
- Longitudes de entrada: "The acronym inputs were lists of 7 words, the sorting input lists varied in length from 10 to 20, and the counting input lists varied from length 1 to 100."
- Funciones lineales: "inputs were sampled uniformly from the integers from 0 to 999."
- Multiplicación: "each input number was sampled uniformly from the integers from 100 to 999."
- Output probability shift cipher: tres conjuntos "high-, medium-, or low-probability sequences of words".
- Tareas con ejemplo en el prompt: "article swapping, reversal, the keyboard cipher, shift ciphers, and Pig Latin."
- Shift ciphers evaluados de 1 a 25: "decoding text written with each shift from 1 to 25."

**4.5 Comparabilidad con trabajo previo**
- "because our claims are comparative ("for LLMs, X is harder than Y"), what is important is ensuring that the two conditions (X and Y) are evaluated in the same way as each other."
- Wu et al.: "because our work and Wu et al.'s use nonoverlapping sets of tasks and draw compatible conclusions, we view these two papers as mutually reinforcing."

**4.6 Limitaciones metodológicas reconocidas sobre sus propios métodos**
- "For most experiments, we test LLMs using basic prompting ... even though LLM accuracy can be substantially increased via more sophisticated inference techniques".
- "it would not invalidate our conclusions if there are conditions in which LLM performance is greater than what we have observed."
- Sobre tareas a nivel de carácter: "This factor might seem unfair to LLMs because they operate over subword tokens (30) rather than characters." Mitigado mediante "a spelling test (SI Appendix, section L)".
- Floor effects reconocidos: p. ej. en encoding rot-13 vs rot-12 para GPT-3.5: "likely due to ﬂoor effects (GPT-3.5's encoding accuracy was close to 0.0 for both shifts)".
- Comparación con humanos: "Without a fair comparison (59–63) that evaluates humans in the same settings, we cannot make strong claims about whether the properties listed in Table 1 make LLMs qualitatively unlike humans."

**Tests estadísticos:** "we used logistic regressions where the response variable was 1 if the model produced the correct answer or 0 otherwise. The predictors generally included input probability, output probability, input length, and output length, as well as task variant for conditions where we compared task variants".

---

## BLOQUE 5 — RESULTADOS CUANTITATIVOS

**5.1 SHIFT CIPHER — Output / Input / Task probability (Fig. 3)**
- 5.1.1 Valores: del abstract — "GPT-4's accuracy at decoding a simple cipher is 51% when the output is a high-probability sentence but only 13% when it is low-probability". (Table 1, rot-13 encode, input) — "GPT-4 gets 21% accuracy when the input is a high-probability sentence yet 11% accuracy when the input is low-probability."
- 5.1.4 Métrica: accuracy. "All error intervals show one SE."
- 5.1.6 Diferencias alta vs baja: output 51% vs 13% (decode); input 21% vs 11% (encode rot-13).
- 5.1.7 Tokens: "Top Left: ... both models score better when the answer is high-probability than when it is low-probability"; "input probability does not show as strong an eﬀect as output probability"; "Both models score better on a frequently occurring shift cipher (rot-13) than on a rare one (rot-12)." "GPT-3.5 shows no signiﬁcant effect of input probability."

**5.2 OUTPUT PROBABILITY — cinco tareas (Fig. 4)**
- 5.2.1/5.2.5 Valores: "Output probability had a statistically signiﬁcant effect on accuracy (P < 0.05) in all cases except Gemini 1.0 decoding shift ciphers (its accuracy was 0% across conditions) and Claude 3 forming acronyms (P = 0.38)." "GPT-4's article-swapping accuracy ranged from 0.02 on the set of low-probability examples to 0.83 for high-probability examples."
- Table 1 (reversal): "GPT-4 gets 97% accuracy when the answer is a high-probability sentence yet 53% accuracy when the output is low probability."
- 5.2.4 Métrica: accuracy; "P < 0.05".

**5.3 ANÁLISIS DE ERRORES SHIFT CIPHER (output)**
- "GPT-3.5 and GPT-4 produced the regularized version more often than the correct one (see SI Appendix, Fig. S23, for quantitative results)".
- Ejemplo (2): correcto "chanted for security reasons"; GPT-4 "changed for security reasons".

**5.4 COUNTING (Fig. 5)**
- 5.4.1/5.4.7: "LLMs often show spikes in accuracy for the numbers that are most frequent in corpora, namely multiples of 10."
- Correlaciones de Spearman (accuracy vs frecuencia vs magnitud): "the correlation coefﬁcients have an absolute value of 0.84 vs. 0.70 for GPT-4, and 0.85 vs. 0.66 for Claude 3". "for all models except Llama 3, accuracy has a higher Spearman correlation with the frequency of the number being counted to than with its magnitude".
- 5.4.2/5.4.3: longitud de lista de 1 a 100; 30 muestras por número.

**5.5 INPUT PROBABILITY (Fig. 6)**
- "for most of the tasks we investigated, input probability had little or no effect on accuracy".
- Birthday task: "input probability had a large effect (P < 10−15 for all models)."

**5.6 TASK PROBABILITY — Shift ciphers (Fig. 7, Fig. 9)**
- 5.6.7: "all models except Gemini 1.0 show a spike in accuracy at 13, which is by far the most common shift."
- "GPT-4 scores 0.50 or above on the three highest-frequency shifts, but its accuracy is less than 0.03 for all other shifts."
- "Claude 3 differs from the other models in that it performs well on some rare shifts ... but it still also shows a spike in performance at 13."
- Significancia (decoding rot-13 vs rot-12): "All three of these models [GPT-3.5, GPT-4, Claude 3] had a statistically signiﬁcantly better performance on decoding rot-13 than rot-12 (P < 0.01)."
- Encoding rot-13 vs rot-12: "GPT-4 and Claude 3 still performed signiﬁcantly better on rot-13 than rot-12 (P < 0.01), but for GPT-3.5, there was no signiﬁcant difference, likely due to ﬂoor effects".
- Error de shift cipher (ejemplo 3): rot-10, GPT-4 produjo "To be or not to be, that is the question..." (cita de Shakespeare) en lugar del texto correcto.

**5.7 PIG LATIN (Fig. 8, Fig. 9)**
- Binario (encoding): "GPT-3.5, GPT-4, and Claude 3 performed much better on Pig Latin than Boar Etruscan ... statistically signiﬁcant (P < 0.01); the other models showed no signiﬁcant difference, likely due to ﬂoor effects".
- Binario (decoding): "all ﬁve models scored better on Pig Latin than Boar Etruscan, but the difference was signiﬁcant only for GPT-4 and Llama 3 (P < 0.05)."
- Cinco variantes (encoding): "signiﬁcant for encoding (P < 0.01) for all models except Llama 3 (P = 0.19)".
- Cinco variantes (decoding): "signiﬁcant only for Claude 3 (P < 0.01) and Gemini 1.0 (P < 0.01)."
- Abstract/Table 1: "GPT-4 gets 42% accuracy when using the most common variant of Pig Latin but only 23% accuracy when using a rare variant."

**5.8 ACRONYMS (Fig. 9)**
- "For all ﬁve models, performance was much higher on ﬁrst-letter acronyms than second-letter ones (Fig. 9), and the effect was statistically signiﬁcant (P < 10−4)."

**5.9 LINEAR FUNCTIONS (Fig. 9)**
- "GPT-3.5, GPT-4, and Claude 3 scored reasonably well for the common function yet poorly for the rarer one ... statistically signiﬁcant for all three models (P < 0.01)."
- "Llama 3 performed slightly better on the common function than the rare one, but this difference was not signiﬁcant (P = 0.22), and Gemini 1.0 performed poorly on both functions."

**5.10 SORTING (Fig. 9)**
- "alphabetical order is 150 times more common than reverse alphabetical order".
- "all ﬁve LLMs perform better on alphabetical order than reverse alphabetical order (Fig. 9; P < 10−5 for all models)."

**5.11 RESUMEN TASK PROBABILITY**
- "Across seven pairs of tasks, models performed substantially better on common task variants than rare ones."

**5.12 ESCALA / PROMPTING / FEW-SHOT (Discussion)**
- "Across almost all tasks, we have observed that GPT-4 substantially outperforms GPT-3.5".
- Chain-of-thought / step-by-step en GPT-4 shift ciphers: "these methods can indeed substantially increase performance, but the basic trends that we have identiﬁed (sensitivity to task frequency and output probability) still hold, just with higher overall levels of accuracy".
- Few-shot: "LLMs that underwent few-shot learning continued to be inﬂuenced by task frequency and example probability".

---

## BLOQUE 6 — HALLAZGOS Y CONCLUSIONES

**6.1 Conclusiones explícitas**
- "we ﬁnd robust evidence that LLMs are inﬂuenced by probability in the hypothesized ways."
- "we conclude that we should not evaluate LLMs as if they are humans but should instead treat them as a distinct type of system—one that has been shaped by its own particular set of pressures."
- "AI practitioners should be careful about using LLMs in low-probability situations."
- "to understand what language models are, we must understand what we have trained them to be."
- "under the right conditions, LLM performance can indeed be meaningfully affected by input probability."
- "scaling may improve overall performance but may not fully overcome the ways in which models are inﬂuenced by their nature."

**6.2 Frases textuales más importantes**
- "the embers of autoregression that appear in these systems even as they might show sparks of artiﬁcial general intelligence."
- "Language models are...language models! That is, they are statistical next-word prediction systems."
- "Once we fully recognize that LLMs are statistical next-word prediction systems, it becomes remarkable that they can perform rot-13 or acronym formation at all, even if they do not perform these tasks perfectly."
- "Just as the human drive to obtain sweet and fatty foods can be maladaptive in a world where those foods are easily available, the autoregressive tendencies of LLMs can cause problems when they are given a task that is not next-word prediction."
- "Clearly something is rot-10 in the state of Denmark".

**6.3 Qué confirma de trabajo previo**
- Confirma/refuerza a Wu et al. (42): "we view our work as highlighting a general phenomenon of which Wu et al.'s conclusion is a special case".
- Concuerda con sensibilidad humana documentada: "humans perform better on a task they were trained on than on a similar but new task (64, 65), and a human's ease of processing a sentence is inﬂuenced by that sentence's probability (66–68)".

**6.4 Qué refuta/matiza**
- Matiza la narrativa de "sparks of artiﬁcial general intelligence" añadiendo los "embers of autoregression".
- Matiza el enfoque human-centric/desideratum-focused: "the desideratum-driven approach runs the risk of missing model-speciﬁc properties".
- No refuta capacidad: "We do not claim that LLMs are incapable of handling these tasks".

**6.5 Postura final sobre si los modelos razonan/entienden**
- "we should not evaluate LLMs as if they are humans but should instead treat them as a distinct type of system".
- "we suspect that humans are less sensitive to these factors than LLMs".
- "we expect that humans are better than LLMs at using abstract algorithms that can be equally well applied across task variants ... humans can use such strategies by leveraging working memory and explicit reasoning, mechanisms that may be less available to LLMs than to humans (71)."
- El documento no afirma categóricamente que los modelos "entiendan" o "razonen"; enmarca su comportamiento como sistemas estadísticos de predicción de la siguiente palabra. [El término "understand"/"reason" no se usa para afirmar que los modelos lo hacen plenamente; ver 6.2.]

**6.6 Implicaciones filosóficas/cognitivas (metáfora y enfoque teleológico)**
- Metáfora "embers of autoregression": "the embers of autoregression that appear in these systems".
- Enfoque teleológico: "understanding intelligent systems by understanding the sorts of problems that they developed to solve". "We refer to this as the teleological approach because it focuses on the system's goal (telos in Greek)".
- Analogías biológicas: dieta (azúcares/grasas) y bipedismo humano ("the friction between our quadrupedal roots and our bipedal lifestyle contributes to several musculoskeletal ailments ... lower back pain").
- Propuesta de comparación con humanos en dos pasos (5): "First, use teleologically motivated experiments to characterize the model in its own terms." luego "ask "in what ways is this characterization like a human and unlike a human?""
- "An additional beneﬁt of the teleological approach is that it reveals unifying principles behind why systems do what they do".

---

## BLOQUE 7 — CONCEPTOS TÉCNICOS

**7.1 Autoregression / next-word prediction**
- Definición: "this task is autoregression—next-word prediction (14, 15)—performed over Internet text." "LLMs are trained to take in the start of a piece of text and then predict what word will come next." La predicción "takes the form of a probability distribution".
- Uso: substrato del que emergen todas las capacidades; "their performance on such tasks is highly inﬂuenced by the autoregressive substrate from which all of their abilities emerge."

**7.2 Teleological approach (enfoque teleológico)**
- Definición: "to characterize the problem that the system solves and to then use this characterization as a source of hypotheses about the system's capacities and biases." "it focuses on the system's goal (telos in Greek)".
- Uso: marco metodológico central del paper; complementario a enfoques de representaciones/mecanismos.

**7.3 Output probability (probabilidad de salida)**
- Definición/predicción: "Even when the task is deterministic, LLMs achieve higher accuracy when the correct answer is high-probability text than when it is low-probability text."
- Uso: factor 1 hipotetizado; el más influyente junto con task probability.

**7.4 Input probability (probabilidad de entrada)**
- Definición: "Even when the task is deterministic, LLMs sometimes achieve higher accuracy when the input text is high-probability than when it is low-probability, but input probability is less inﬂuential than output probability."
- Uso: factor 3; "predicted to matter only when the task depends on information about the input that models mainly learn through experience with that speciﬁc input".

**7.5 Task probability / task frequency (probabilidad/frecuencia de tarea)**
- Definición: "Task probability is the probability that a task will be illustrated in a random sample of text. This probability determines how many examples of the task will appear during an LLM's training." Predicción: "Even when there is no diﬀerence in the complexity of the tasks, LLMs perform better on tasks that are frequent than ones that are rare."
- Uso: factor 2; "we predict that task probability will routinely have an effect."

**7.6 "Embers of autoregression"**
- Definición/uso: metáfora del título; quirks atribuibles a la naturaleza autoregresiva; contrapuesto a "sparks of artiﬁcial general intelligence".

**7.7 Análisis bayesiano (Bayes' rule)**
- Definición: "the LLM should ﬁnd the output that maximizes P(output|input) ... By Bayes' rule, this problem is equivalent to maximizing P(input|output)P(output)." "as long as there are multiple outputs for which P(input|output) is nonzero, the LLM's predictions will be inﬂuenced by the unconditional probability of the output, P(output)".
- Uso: motiva formalmente las tres hipótesis.

**7.8 Regularización ("regularized")**
- Uso: "models often "regularized" the output by producing the high-probability sentence that was similar to the correct answer, rather than the correct answer".

**7.9 Instruction tuning**
- Definición/uso: "a training phase based on instruction tuning (22), which aims to align model behavior with human preferences." "we only analyze next-word prediction, leaving instruction tuning for future work."

**7.10 Desideratum-focused evaluation**
- Definición: "in which the evaluator tests for properties that they wish for models to have ... Crucially, this approach is model-agnostic".
- Uso: enfoque contrastado con el teleológico.

**7.11 Human-centric approach**
- Definición/uso: "test for the properties that are viewed as most important for characterizing human cognition."

**7.12 Training task / Training distribution / Model architecture**
- Definición (Anderson, ref. 12): tres factores — "1. Training task ... 2. Training distribution ... 3. Model architecture". Para LLMs: "the training task is next-word prediction, the training distribution is a distribution over Internet text, and the model architecture is a neural network (speciﬁcally, a Transformer: 21)."

**7.13 Token / subword**
- Definición: "LLMs predict what token will come next, where tokens are units of text that often correspond to whole words but sometimes are smaller pieces." "they operate over subword tokens (30) rather than characters."

**7.14 Basic prompting / chain-of-thought / tree-of-thoughts / few-shot / step-by-step**
- "basic prompting (i.e., simply asking them to provide an answer to a query)".
- "chain-of-thought prompting (25, 26)"; "the tree-of-thoughts framework (27)".
- few-shot: "the LLM is given several examples of correct input–output pairs before it is given the input that it must translate to an output."

---

## BLOQUE 8 — REFERENCIAS

Lista completa de referencias numeradas del documento (autores/título/año/URL si aparece). El contexto se da cuando el texto cita la referencia en el cuerpo.

1. OpenAI, GPT-4 technical report. arXiv [Preprint] (2023). https://arxiv.org/abs/2303.08774 — Contexto: ChatGPT/GPT-4/GPT-3.5; evaluación en SAT.
2. Anthropic, Introducing the next generation of Claude. (2024). https://www.anthropic.com/news/claude-3-family — Contexto: Claude / Claude 3.
3. H. Touvron et al., Llama 2: Open foundation and ﬁne-tuned chat models. arXiv (2023). https://arxiv.org/abs/2307.09288 — Contexto: Llama / Llama 3 / Llama 2.
4. S. Bubeck et al., Sparks of artiﬁcial general intelligence: Early experiments with GPT-4. arXiv (2023). https://arxiv.org/abs/2303.12712 — Contexto: paper "sparks of AGI"; Section 8 sobre limitaciones autoregresivas.
5. M. Binz, E. Schulz, Using cognitive psychology to understand GPT-3. PNAS 120, e2218523120 (2023) — Contexto: tests de psicología cognitiva.
6. T. Webb, K. J. Holyoak, H. Lu, Emergent analogical reasoning in large language models. Nat. Hum. Behav. 7, 1526–1541 (2023) — Contexto: razonamiento analógico.
7. C. D. Manning et al., Emergent linguistic structure in artiﬁcial neural networks trained by self-supervision. PNAS 117, 30046–30054 (2020) — Contexto: comparación con lingüística.
8. M. Schrimpf et al., The neural architecture of language... PNAS 118, e2105646118 (2021) — Contexto: neurociencia; next-word prediction en cognición humana.
9. M. Mitchell, How do we know how smart AI systems are? Science 381, adj5957 (2023) — Contexto: limitación del enfoque human-centric.
10. D. Marr, Vision (W.H. Freeman, 1982) — Contexto: análisis computacional-nivel.
11. R. N. Shepard, Toward a universal law of generalization... Science 237, 1317–1323 (1987).
12. J. R. Anderson, The Adaptive Character of Thought (Erlbaum, 1990) — Contexto: tres factores del problema (goal, environment, computational limitations).
13. T. L. Griﬃths, Understanding human intelligence through human limitations. TiCS 24, 873–883 (2020).
14. J. L. Elman, Distributed representations, simple recurrent networks... Mach. Learn. 7, 195–225 (1991) — Contexto: next-word prediction.
15. A. Radford et al., Language models are unsupervised multitask learners. OpenAI (2019). https://openai.com/index/better-language-models — Contexto: GPT-2 (estimación de probabilidades); título citado en Conclusion.
16. T. Lombrozo, S. Carey, Functional explanation and the function of explanation. Cognition 99, 167–204 (2006) — Contexto: explicación teleológica.
17. P. Godfrey-Smith, "Three kinds of adaptationism" (2001) — Contexto: biología evolutiva.
18. S. J. Shettleworth, Cognition, Evolution, and Behavior (2010).
19. S. Gould, R. Lewontin, The spandrels of San Marco... Proc. R. Soc. London Ser. B 205, 581–698 (1979) — Contexto: explicaciones teleológicas incompletas.
20. T. Lombrozo, D. Wilkenfeld, "Mechanistic versus functional understanding" (2019).
21. A. Vaswani et al., Attention is all you need. NeurIPS 30, 5998–6008 (2017) — Contexto: Transformer.
22. L. Ouyang et al., Training language models to follow instructions with human feedback. NeurIPS 35, 27730–27744 (2022) — Contexto: instruction tuning.
23. B. Latimer, The perils of being bipedal. Ann. Biomed. Eng. 33, 3–6 (2005) — Contexto: analogía bipedismo.
24. W. M. Krogman, The scars of human evolution. Sci. Am. 185, 54–57 (1951) — Contexto: dolor lumbar.
25. T. Kojima et al., Large language models are zero-shot reasoners. NeurIPS 35, 22199–22213 (2022) — Contexto: chain-of-thought / step-by-step.
26. J. Wei et al., Chain-of-thought prompting elicits reasoning... NeurIPS 35, 24824–24837 (2022) — Contexto: CoT; last-letter concatenation.
27. S. Yao et al., Tree of thoughts... NeurIPS 36, 11809–11822 (2023) — Contexto: tree-of-thoughts.
28. Gemini Team Google, Gemini: A family of highly capable multimodal models. arXiv (2023). https://arxiv.org/abs/2312.11805 — Contexto: Gemini 1.0.
29. D. Groeneveld et al., OLMo: Accelerating the science of language models. arXiv (2024). https://arxiv.org/abs/2402.00838 — Contexto: modelo preliminar OLMo.
30. R. Sennrich, B. Haddow, A. Birch, "Neural machine translation of rare words with subword units" ACL (2016) — Contexto: subword tokens.
31. I. Itzhak, O. Levy, "Models in a spelling bee..." NAACL (2022) — Contexto: codificación de caracteres.
32. A. Kaushal, K. Mahowald, "What do tokens know about their characters..." NAACL (2022) — Contexto: caracteres en tokens.
33. Y. Razeghi et al., "Impact of pretraining term frequencies on few-shot numerical reasoning" EMNLP (2022) — Contexto: input probability en aritmética.
34. N. Kandpal et al., "Large language models struggle to learn long-tail knowledge" ICML (2023) — Contexto: factual recall.
35. S. Biderman et al., "Pythia: A suite for analyzing large language models..." ICML (2023) — Contexto: factual recall.
36. C. Raffel et al., Exploring the limits of transfer learning... J. Mach. Learn. Res. 21, 5485–5551 (2020) — Contexto: corpus C4.
37. Suetonius, The Twelve Caesars (1883) — Contexto: cifrado de Julio César (rot-3).
38. D. Kahn, The Codebreakers (1967) — Contexto: shift de 3.
39. S. Singh, The Code Book (1999) — Contexto: shift de 3.
40. B. Vaux, A. I. Nevins, "Underdetermination in language games: Survey & analysis of Pig Latin dialects" LSA (2003) — Contexto: variantes de Pig Latin.
41. L. Gao et al., The Pile: An 800GB dataset... arXiv (2020). https://arxiv.org/abs/2101.00027 — Contexto: dataset the Pile.
42. Z. Wu et al., "Reasoning or reciting?..." NAACL (2024), pp. 1819–1862 — Contexto: trabajo contemporáneo; default vs counterfactual.
43. K. Mahowald et al., Dissociating language and thought in large language models. TiCS 28, 517–540 (2024) — Contexto: tareas que dependen del significado.
44. N. Kim, S. Schuster, "Entity tracking in language models" ACL (2023).
45. M. Mitchell, D. C. Krakauer, The debate over understanding in AI's large language models. PNAS 120, e2215907120 (2023) — Contexto: significado/entendimiento.
46. K. Misra, J. Rayz, A. Ettinger, "COMPS..." EACL (2023).
47. J. A. Fodor, Z. W. Pylyshyn, Connectionism and cognitive architecture... Cognition 28, 3–71 (1988) — Contexto: composicionalidad/sistematicidad.
48. G. F. Marcus, Rethinking eliminative connectionism. Cognit. Psychol. 37, 243–282 (1998).
49. B. M. Lake, M. Baroni, "Generalization without systematicity..." ICML (2018).
50. N. Dziri et al., Faith and fate: Limits of transformers on compositionality. NeurIPS 36, 70293–70332 (2023).
51. M. Mitchell, A. B. Palmarini, A. K. Moskvichev, "Comparing humans, GPT-4, and GPT-4v..." AAAI 2024 LLM-CP Workshop (2023).
52. I. D. Raji et al., "AI and the everything in the whole wide world benchmark" NeurIPS (2021) — Contexto: propuestas sobre cómo pensar los LLMs.
53. M. Shanahan, Talking about large language models. ACM Commun. 67, 68–79 (2024).
54. A. Holtzman, P. West, L. Zettlemoyer, Generative models as a complex systems science. arXiv (2023). https://arxiv.org/abs/2308.00189
55. BIG-bench authors, Beyond the imitation game... Trans. Mach. Learn. Res. (2023) — Contexto: desideratum-focused.
56. A. Efrat, O. Honovich, O. Levy, "LMentry..." ACL (2023).
57. M. T. Ribeiro et al., "Beyond accuracy: ... CheckList" ACL (2020) — Contexto: evitar tipo de error.
58. P. Liang et al., Holistic Evaluation of Language Models (TMLR, 2023).
59. F. De Waal, Are We Smart Enough to Know How Smart Animals Are? (2016) — Contexto: comparación justa.
60. C. Firestone, Performance vs. competence in human–machine comparisons. PNAS 117, 26562–26571 (2020).
61. M. A. Lepori, C. Firestone, Can you hear me now?... Cognit. Sci. 46, e13191 (2022).
62. A. K. Lampinen, Can language models handle recursively nested grammatical structures?... arXiv (2022). https://arxiv.org/abs/2210.15303
63. I. Dasgupta et al., Language models show human-like content effects on reasoning tasks. arXiv (2022). https://arxiv.org/abs/2207.07051
64. A. S. Luchins, Mechanization in problem solving: The effect of Einstellung. Psychol. Monogr. 54, i-95 (1942) — Contexto: humanos mejores en tarea entrenada.
65. M. K. Ho, J. D. Cohen, T. L. Griﬃths, Rational simpliﬁcation and rigidity in human planning. Psychol. Sci. 34, 1281–1292 (2023).
66. S. F. Ehrlich, K. Rayner, Contextual effects on word perception... J. Verb. Learn. Verb. Behav. 20, 641–655 (1981) — Contexto: probabilidad de oración en humanos.
67. N. J. Smith, R. Levy, The effect of word predictability on reading time is logarithmic. Cognition 128, 302–319 (2013).
68. E. Gibson, L. Bergen, S. T. Piantadosi, Rational integration of noisy evidence... PNAS 110, 8051–8056 (2013).
69. J. Hale, "A probabilistic Earley parser as a psycholinguistic model" NAACL (2001) — Contexto: next-word prediction en cognición humana.
70. R. Levy, Expectation-based syntactic comprehension. Cognition 106, 1126–1177 (2008).
71. R. Shiffrin, M. Mitchell, Probing the psychology of AI models. PNAS 120, e2300963120 (2023) — Contexto: memoria de trabajo y razonamiento explícito.
72. L. Wong et al., From word models to world models... arXiv (2023). https://arxiv.org/abs/2306.12672 — Contexto: ejecución de código.
73. T. Brown et al., Language models are few-shot learners. NeurIPS 33, 1877–1901 (2020) — Contexto: título citado en Conclusion.
74. Y. Hao et al., Language models are general-purpose interfaces. arXiv (2022). https://arxiv.org/abs/2206.06336 — Contexto: título citado en Conclusion.
75. F. Shi et al., "Language models are multilingual chain-of-thought reasoners" ICLR (2023) — Contexto: título citado en Conclusion.
76. C. Wang, X. Liu, D. Song, Language models are open knowledge graphs. arXiv (2020). https://arxiv.org/abs/2010.11967 — Contexto: título citado en Conclusion.
77. Y. Liu et al., RoBERTa: A robustly optimized BERT pretraining approach. arXiv (2019). https://arxiv.org/abs/1907.11692 — Contexto: generación de estímulos medium-probability.
78. R. Lebret, D. Grangier, M. Auli, "Neural text generation from structured data..." EMNLP (2016) — Contexto: dataset WikiBio (birthday task).
79. R. T. McCoy et al., Embers of autoregression. GitHub. https://github.com/tommccoy1/embers-of-autoregression/. Deposited 14 September 2024.
80. R. T. McCoy et al., Embers of autoregression. Zenodo. https://zenodo.org/records/13763259. Deposited 14 September 2024.

---

## BLOQUE 9 — FIGURAS Y TABLAS

**Fig. 1**
- Pie: "Humans and LLMs have some shared properties and some properties that diﬀer. If we analyze LLMs using tests designed for humans, we risk identifying only the shared properties, missing the properties that are unique to LLMs (the dotted region of the diagram). We argue that to identify the properties in the dotted region, we must approach LLMs on their own terms by considering the problem that they were trained to solve: next-word prediction over Internet text."
- Variables: propiedades compartidas vs. propiedades únicas de LLMs (región punteada).
- Conclusión del texto: los tests para humanos arriesgan capturar solo lo compartido.

**Fig. 2**
- Pie: "GPT-4 struggles on some seemingly simple tasks such as counting, article swapping, shift ciphers, and linear functions. In the counting and article swapping examples, GPT-4 fails in the cases where the correct output is a low-probability piece of text ... we refer to 29 as low-probability because it occurs much less frequently in natural corpora than 30 does ... the shift cipher with a shift of 13 is over 100 times more common in Internet text than the shift cipher with a shift of 12; and the linear function f (x) = (9/5)x + 32 is common because it is the Celsius-to-Fahrenheit conversion ... The GPT-4 predictions were obtained using gpt-4-0613 on the OpenAI API; other model versions (e.g., the online chat interface) may give diﬀerent predictions."
- Variables: ejemplos de tareas con salida alta vs baja probabilidad; variantes comunes vs raras.
- Conclusión: GPT-4 falla en variantes raras / salidas de baja probabilidad.

**Fig. 3**
- Pie: "When processing shift ciphers, LLMs are highly sensitive to probability, even though shift ciphers are deterministic. Top Left: Eﬀect of output probability ... both models score better when the answer is high-probability than when it is low-probability. Top Middle: Eﬀect of input probability ... input probability does not show as strong an eﬀect as output probability. Top Right: Eﬀect of task probability. Both models score better on a frequently occurring shift cipher (rot-13) than on a rare one (rot-12). All error intervals show one SE. Bottom: Examples for output and input probability; see Fig. 2 for task probability examples."
- Variables: output/input/task probability vs accuracy (GPT-3.5, GPT-4).
- Conclusión: sensibilidad a probabilidad pese a ser determinista; input < output.

**Fig. 4**
- Pie: "The eﬀect of output probability on model accuracy across five tasks. The intervals around the lines show one SE."
- Variables: probabilidad de salida vs accuracy en cinco tareas.
- Conclusión: efecto significativo de output probability (salvo excepciones citadas).

**Fig. 5**
- Pie: "Model performance on counting a list of words, as a function of the length of the list. The intervals around the lines show one SE."
- Variables: longitud de lista (número a contar) vs accuracy.
- Conclusión: picos de accuracy en múltiplos de 10; correlación con frecuencia > magnitud.

**Fig. 6**
- Pie: "The eﬀect of input probability on model accuracy across five tasks. The intervals around the lines show one SE."
- Variables: probabilidad de entrada vs accuracy en cinco tareas.
- Conclusión: efecto pequeño o nulo en la mayoría de tareas.

**Fig. 7**
- Pie: "Analysis of shift ciphers with shift levels varying from 1 to 25. Top: Number of occurrences of each shift level in the C4 corpus. Bottom: Accuracy on decoding shift ciphers with various shifts. Most models display a spike in accuracy at a shift of 13, which the top plot shows to be the most common shift level."
- Variables: nivel de shift (1–25); ocurrencias en C4; accuracy de decodificación.
- Conclusión: pico de accuracy en shift 13 (el más común).

**Fig. 8**
- Pie: "Accuracy on Pig Latin variants when encoding (Left) or decoding (Right), as a function of the variant's frequency. The shaded intervals show one SE."
- Variables: frecuencia de variante de Pig Latin vs accuracy (encoding/decoding).
- Conclusión: el desempeño sigue la frecuencia de corpus, especialmente en encoding.

**Fig. 9**
- Pie: "Comparing performance on common vs. rare versions of tasks. For shift ciphers, the common variant that we illustrate is rot-13, and the rare variant is rot-12. For Pig Latin, the common variant is Pig Latin, and the rare variant is Boar Etruscan ... For acronyms, the common variant is acronyms formed from the first letters of words, while the rare variant is acronyms formed from the second letters of words. The common linear function is f (x) = (9/5)x+32 ... and the rare linear function is f (x) = (7/5)x + 31. The common version of sorting is sorting in alphabetical order, while the rare variant uses reverse alphabetical order. Error bars show one SE."
- Variables: comparación common vs rare en 7 pares de tareas (shift cipher encoding/decoding, Pig Latin encoding/decoding, acronyms, linear function, sorting) para los 5 modelos.
- Conclusión: mejor desempeño en variantes comunes que raras.

**Table 1**
- Título: "Eﬀects on the performance of language models that are attributable to the fact that they are statistical next-word prediction systems"
- Contenido: tres propiedades con Description y Example — Sensitivity to output probability (reversal: 97% vs 53%); Sensitivity to input probability (rot-13 encode: 21% vs 11%); Sensitivity to task frequency (Pig Latin: 42% vs 23%).

**Table 2**
- Título: "The tasks that we used to evaluate LLMs"
- Contenido: 11 tareas con Description y Example (ver BLOQUE 3).

**Fig. S23 (SI Appendix)**
- Referida en texto: "see SI Appendix, Fig. S23, for quantitative results" sobre versión regularizada vs correcta en shift cipher. [INCOMPLETO EN EL TEXTO: el contenido detallado está en el SI Appendix, no en el cuerpo.]

---

## BLOQUE 10 — GAPS Y TRABAJO FUTURO

**10.1 Limitaciones reconocidas**
- Solo se analiza next-word prediction: "we only analyze next-word prediction, leaving instruction tuning for future work."
- Solo LLMs de texto: "In this paper, we only consider LLMs that process text sequences".
- Uso de basic prompting (no técnicas más fuertes).
- No comparan con humanos en el mismo setting: "Without a fair comparison ... we cannot make strong claims about whether the properties listed in Table 1 make LLMs qualitatively unlike humans."
- Floor effects en algunos modelos/tareas.
- El enfoque teleológico puede ser incompleto: "we do not anticipate that all properties of LLMs can be understood via their goals."
- Otros objetivos podrían producir los mismos efectos: "autoregression is not the only objective that we would expect to produce these effects."

**10.2 Trabajo futuro**
- "future work could use the teleological perspective to investigate whether other objectives also yield these effects."
- "the teleological perspective could be applied to augmented LLMs in future work".
- "Overcoming these limitations is an important target for future work in AI."
- "future work could further investigate other stages such as instruction tuning."

**10.3 Preguntas abiertas**
- "what if your goal is to compare LLMs to humans?" — abordado proponiendo el proceso en dos pasos (5).
- En qué medida los humanos comparten estas sensibilidades: "we suspect that humans are less sensitive to these factors than LLMs".

**10.4 Código/recursos (URLs exactas)**
- GitHub: "https://github.com/tommccoy1/embers-of-autoregression" (ref. 79).
- Zenodo (release con timestamp): "https://zenodo.org/records/13763259" (ref. 80).
- SI Appendix: "https://www.pnas.org/lookup/suppl/doi:10.1073/pnas.2322420121/-/DCSupplemental."
- CMU Pronouncing Dictionary: "http://www.speech.cs.cmu.edu/cgi-bin/cmudict".
- Secciones del SI referidas: B (few-shot), C (otras propiedades), D (CoT/step-by-step), E.4 (asimetría input/output), H.7 (temperatura), I (tests de significancia), J (probabilidades de salida con GPT-2), K (frecuencia de tareas), L (spelling test). Fig. S23.

---

## VERIFICACIÓN — Los 5 datos más difíciles de encontrar (confirmados con cita textual)

1. **Versiones exactas de los modelos (con timestamp):** "gpt-3.5-turbo-0613, gpt-4-0613, claude-3-opus-20240229, gemini-1.0-pro-001, and llama-3-70b-chat-hf."

2. **Tamaños de muestra por condición (no uniformes):** "The sample size was 1,000 for each condition in the acronym task, 30 for each number in the counting task, and 100 for each condition in all other tasks."

3. **Frecuencias exactas de variantes de Pig Latin en the Pile:** "68 cases where the added syllable was -way, 46 where it was -ay, 26 where it was -yay, and 8 where it was -hay ... a ﬁfth one where the added syllable was -say (which has 0 occurrences in C4 and the Pile)."

4. **Correlaciones de Spearman en counting (frecuencia vs magnitud):** "the correlation coefﬁcients have an absolute value of 0.84 vs. 0.70 for GPT-4, and 0.85 vs. 0.66 for Claude 3".

5. **Generación de los estímulos de probabilidad media y baja:** "Medium-probability sentences were created by taking the high-probability sentences and using RoBERTa (77) to replace some of the words ... Low-probability sentences were created by shufﬂing the words of the medium-probability examples, except that the ﬁrst and last words were left in place."

> Datos adicionales de difícil localización confirmados: Conﬂicto de interés — "D.F. was previously aﬀiliated with Google ... S.Y. is aﬀiliated with OpenAI". Modelos preliminares descartados — "OLMo (29) and Llama 2 (3) ... accuracies of 0% on most tasks." Ratio de frecuencia en sorting — "alphabetical order is 150 times more common than reverse alphabetical order".

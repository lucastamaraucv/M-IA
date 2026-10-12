# Metodología de estudio para matemática avanzada

**Extraído de 4 artículos científicos en `/articulos metodologia estudio/`**
**Adaptado al curso:** Matemáticas para Inteligencia Artificial — Máster en IA, VIU
**Fecha:** 2026-05-17

> Nota: la carpeta tiene 5 PDFs, pero `Cognitive_Architecture_and_Instructional_Design_20.pdf` y `s10648-019-09465-5.pdf` son el **mismo** artículo (Sweller et al. 2019). Se cuentan como uno.

---

## Índice

1. [Artículo 1 — Interleaving (Brunmair & Richter 2019)](#articulo-1)
2. [Artículo 2 — Cognitive Load Theory (Sweller et al. 2019)](#articulo-2)
3. [Artículo 3 — Self-Explanation en demostraciones (Hodds et al. 2014)](#articulo-3)
4. [Artículo 4 — Active Learning en STEM (Freeman et al. 2014)](#articulo-4)
5. [Síntesis — 6 prácticas con MAYOR evidencia](#sintesis)
6. [Plan semanal — adaptado a Matemáticas para IA](#plan-semanal)

---

<a name="articulo-1"></a>
## Artículo 1 — Brunmair & Richter (2019)

| | |
|---|---|
| **Título** | *Similarity matters: A meta-analysis of interleaved learning and its moderators* |
| **Autores** | Matthias Brunmair, Tobias Richter (Univ. Würzburg) |
| **Revista** | Psychological Bulletin (APA) |
| **DOI** | 10.1037/bul0000209 |
| **Base** | meta-análisis de 59 estudios, 158 muestras, 238 efectos |

### Pregunta de investigación

¿Conviene estudiar ejemplos **mezclados** (interleaving) o uno a uno en **bloques** (blocking)? Crítico para aprendizaje **inductivo** — sacar reglas a partir de ejemplos, que es exactamente lo que haces en matemática y en ML.

### Hallazgos clave (g de Hedges)

| Material | Efecto del interleaving |
|---|---|
| Global | **g = 0.42** (efecto moderado) |
| Pinturas / fotografías | g = 0.67 (alto) |
| **Tareas matemáticas** | **g = 0.34** (pequeño pero positivo) |
| Textos expositivos | nulo / ambiguo |
| Palabras / vocabulario | **g = −0.39** (¡bloqueo es MEJOR!) |

### Moderadores que aumentan el efecto

1. Categorías **parecidas** entre sí (te cuesta distinguirlas) → más interleaving
2. Ejemplos **poco parecidos** dentro de una misma categoría → más interleaving
3. Material **complejo** → más interleaving
4. **Sin** espaciado largo entre ítems → más interleaving

### Principios extraídos

- **[P1]** Si dos conceptos se confunden (límite vs. continuidad, derivada vs. diferencial, gradiente vs. derivada direccional), **estúdialos alternados**.
- **[P2]** Para procedimientos repetitivos: primero algo de bloqueo para fijar la mecánica; luego interleaving para aprender a **elegir** qué procedimiento aplicar.
- **[P3]** Para **vocabulario formal** (definiciones, símbolos): bloquea.
- **[P4]** Cuanto más parecidos sean dos teoremas, más urgente mezclarlos.

### Aplicación a tu asignatura

- Mezcla ejercicios de **distintas secciones** del manual en una misma sesión (ej. 1.1 + 1.2 + 1.4).
- Cuando llegues al Cap. 2: mezcla LU + Cholesky + QR en la misma tanda — te obliga a **identificar** cuál aplicar.
- **No mezcles** cuando estés memorizando definiciones nuevas. Bloquea.

---

<a name="articulo-2"></a>
## Artículo 2 — Sweller, van Merriënboer & Paas (2019)

| | |
|---|---|
| **Título** | *Cognitive Architecture and Instructional Design: 20 Years Later* |
| **Autores** | John Sweller, Jeroen van Merriënboer, Fred Paas |
| **Revista** | Educational Psychology Review 31:261-292 |
| **DOI** | 10.1007/s10648-019-09465-5 |
| **Tipo** | revisión teórica de 20 años de Cognitive Load Theory (CLT) |

### Idea central

La **memoria de trabajo** es muy limitada (procesa solo unos pocos elementos a la vez). La **memoria a largo plazo** es ilimitada. Si la memoria de trabajo se satura, no aprendes. El truco no es "esforzarse más" sino **reducir carga innecesaria** y construir **esquemas** que liberan memoria de trabajo.

### Tipos de carga cognitiva

- **Intrínseca**: complejidad propia del material. No baja, pero se puede **fragmentar**.
- **Extraña**: la que añade un mal diseño. **Elimínala**.
- **Germane**: la que sí construye esquemas. **Potencia esta**.

### Los efectos más relevantes para ti

#### [E1] Worked-Example Effect (1985)
Para principiantes, **estudiar un problema resuelto paso a paso** enseña más que intentar resolverlo solo.
→ Antes de cada ejercicio, lee 2-3 ejemplos resueltos.

#### [E2] Split-Attention Effect (1988)
Si miras un diagrama AQUÍ y lees la explicación ALLÁ, pierdes capacidad mental conectándolos.
→ Integra texto y figura **en la misma vista**.

#### [E3] Redundancy Effect (1991)
Misma información en dos formatos idénticos = perjudica.
→ No dupliques fuentes; elige una.

#### [E4] Modality Effect (1995)
Visual + auditivo en paralelo aprovecha dos sub-memorias.
→ Para grafos, circuitos, tensores: video + lectura simultánea > dos textos juntos.

#### [E5] Variability Effect (1994)
Variar el **tipo** de problemas (no solo los números) produce esquemas transferibles.
→ No hagas 10 del mismo molde; varía el tipo de enunciado.

#### [E6] Self-Explanation Effect (1998)
Detenerte a explicarte en voz alta lo que leíste mejora mucho la comprensión. *(Ver Artículo 3 para detalle.)*

#### [E7] Imagination Effect (2001)
**Imaginar** mentalmente la ejecución de un procedimiento lo consolida — pero solo si ya dominas lo básico.

#### [E8] Expertise Reversal Effect (2003) — **MUY IMPORTANTE**
Lo que funciona para principiantes (worked examples, andamiaje fuerte) **perjudica** a expertos. Y viceversa.
→ Al inicio de un tema: ejemplos resueltos. Cuando avanzas: reduce ayuda y resuelve TÚ.

#### [E9] Guidance-Fading Effect (2003)
Empieza con ejemplo completo → ejemplo con huecos → problema sin ayuda.
→ Implementa esa progresión para cada nuevo método.

#### [E10] Isolated-Elements Effect (2002)
Si el material tiene muchos elementos interactuando, preséntalos **uno por uno** primero.
→ Para gradient descent / backprop: estudia derivada parcial → gradiente → regla de la cadena → ÚNELOS.

#### [E11] Segmentation / Self-Pacing
Para video, ten control de pausa y segmentos pequeños.
→ Si ves un video, párlo cada 1-2 min y haz una mini-síntesis.

#### [E12] Collective WM Effect (2009)
Trabajar en grupos **reparte** la memoria de trabajo.
→ Para temas duros (backprop, SVD): estúdialo CON alguien, no solo.

### Principios extraídos

- **[P5]** Siempre **worked examples primero**, problemas después.
- **[P6]** Integrar texto + diagrama en la misma vista.
- **[P7]** Doble modalidad: visual + auditiva, o visual + código.
- **[P8]** Aislar antes de integrar.
- **[P9]** Reducir el andamiaje conforme avanzas (fading).
- **[P10]** Lo que te ayudó al inicio te frenará después. Cambia método al avanzar.

---

<a name="articulo-3"></a>
## Artículo 3 — Hodds, Alcock & Inglis (2014)

| | |
|---|---|
| **Título** | *Self-Explanation Training Improves Proof Comprehension* |
| **Autores** | Mark Hodds, Lara Alcock, Matthew Inglis (Loughborough) |
| **Revista** | Journal for Research in Mathematics Education |
| **Tipo** | 3 experimentos (randomizado + eye-tracking + longitudinal) |

### Hallazgos clave

- **Experimento 1**: efecto en comprensión de demostración **d = 0.95** (efecto GRANDE).
- **Experimento 2**: el grupo entrenado mueve la atención más por el proof (más saccades entre líneas — lectura más activa).
- **Experimento 3**: una intervención de **solo 15 min** dentro de clase mejora la comprensión, **y el efecto persiste en el tiempo**.

### La técnica de self-explanation (4 preguntas)

Después de leer **cada línea** de una demostración o teoría densa, hazte:

1. **¿Entiendo las ideas** usadas en esta línea?
2. **¿Por qué se ha usado** esta idea AQUÍ y no otra?
3. **¿Cómo se enlaza** esta idea con otras del mismo proof, otros teoremas o mi conocimiento previo?
4. **¿La self-explanation que generé responde** a las preguntas que me estaba haciendo?

### Lo que **NO** funciona

| ✗ | Parafrasear | "p y q tienen que ser enteros" (decir lo mismo con otras palabras) |
| ✗ | Monitorear | "OK, esto lo entiendo" |
| ✓ | Self-explanation real | basada en **definiciones** previas, conectando con la **estructura** global del proof, notando **coherencia** con líneas anteriores |

### Ejemplo del paper (demostración de que 3.14 es racional)

- **Mal (parafraseo)**: *"Ambos p y q tienen que ser enteros."*
- **Mal (monitoreo)**: *"OK, entiendo que p=314 y q=100."*
- **BIEN**: *"p=314 y q=100 porque son enteros y p/q = 3.14. La demostración podría haber usado también p=628 y q=200. Esto cumple la **definición** de número racional, por eso completa la prueba."*

### Principios extraídos

- **[P11]** Siempre explicarte cada línea con los **porqués**, no solo parafraseos.
- **[P12]** Conectar **explícitamente** cada paso con definiciones/teoremas previos.
- **[P13]** Saltar la vista atrás y adelante por una demostración es **lectura experta**. No leas linealmente.
- **[P14]** Intervenciones de 15 min pueden tener efectos duraderos.

---

<a name="articulo-4"></a>
## Artículo 4 — Freeman et al. (2014)

| | |
|---|---|
| **Título** | *Active learning increases student performance in science, engineering, and mathematics* |
| **Autores** | Scott Freeman et al. (Univ. of Washington / Maine) |
| **Revista** | PNAS, vol. 111 no. 23, pp. 8410-8415 |
| **DOI** | 10.1073/pnas.1319030111 |
| **Base** | meta-análisis de 225 estudios STEM universitario |

### Hallazgos clave

| Métrica | Clase magistral | Aprendizaje activo |
|---|---|---|
| Mejora en exámenes | baseline | **+0.47 SD** (≈ +6 % nota) |
| Tasa de suspenso | **33.8 %** | **21.8 %** |
| Probabilidad de fallar | 1.5× MÁS | baseline |

> Robusto en TODAS las disciplinas STEM y todos los tamaños de clase. Mayor en clases pequeñas (≤50).

### Qué cuenta como "active learning"

> *"Approaches as diverse as occasional group problem-solving, worksheets or tutorials completed during class, use of personal response systems with or without peer instruction, and studio or workshop course designs."*

Cualquier actividad que obliga al estudiante a **producir** algo en lugar de solo escuchar.

### Principios extraídos

- **[P15]** Clase magistral o video pasivo = los métodos **menos** eficaces.
- **[P16]** En cada sesión hay que **producir** (resolver, escribir, codificar) para reducir riesgo de suspenso.
- **[P17]** Sustituye "ver / leer" por "ver / leer ─ pausar ─ producir".

### Aplicación a tu asignatura

- Por cada bloque del manual, regla fija: *"no paso a la siguiente sección sin haber producido algo"* — un ejercicio resuelto, un script Python, un mapa mental, una explicación a alguien.
- Videos del campus virtual: párlos cada 5 min y resume tú.
- Trabaja con un compañero del máster. **Enseñar es la forma más activa de aprender**.

---

<a name="sintesis"></a>
## Síntesis — Las 6 prácticas con MAYOR evidencia para tu caso

| # | Práctica | Cita |
|---|----------|------|
| **1** | **Worked examples PRIMERO** — 2-3 ejemplos resueltos antes de cualquier ejercicio propio | Sweller et al. (2019) |
| **2** | **Self-explanation línea a línea** — las 4 preguntas tras cada paso de teoría/proof. Efecto d = 0.95 | Hodds, Alcock, Inglis (2014) |
| **3** | **Active learning en cada sesión** — producir algo (resolver, codificar, explicar). Reduce suspenso ≈40 % | Freeman et al. (2014) |
| **4** | **Interleaving de conceptos SIMILARES** — mezcla temas parecidos para aprender a distinguirlos | Brunmair & Richter (2019) |
| **5** | **Aislar elementos antes de integrarlos** — para temas con muchas piezas (backprop, SVD) estudia cada parte sola | Sweller et al. (2019) |
| **6** | **Fading del andamiaje** — ejemplo completo → con huecos → solo. Lo que ayuda al principio te frena después | Sweller et al. (2019) |

---

<a name="plan-semanal"></a>
## Plan semanal — adaptado a Matemáticas para IA (VIU)

> Asume ~10-12 h de estudio semanal. Divide en **5 sesiones de ~2 h**, cada una con esta estructura:

### Bloque A — INPUT GUIADO (20 min)
Lee la sección del manual con **self-explanation línea a línea** (técnica #2). Subraya solo lo que no entiendes.

### Bloque B — EJEMPLOS RESUELTOS (30 min)
Estudia **2-3 worked examples** del manual (técnica #1). Reproduce cada uno en Python o en papel **sin copiar**.

### Bloque C — PRODUCCIÓN ACTIVA + INTERLEAVING (40 min)
Resuelve **4-6 ejercicios mezclando** temas similares (técnicas #3 + #4). Ej.: en una misma sesión, ∧, ∨, → (1.1.2) + leyes de Morgan + Boole.

### Bloque D — INTEGRACIÓN EN CÓDIGO (20 min)
Implementa el concepto en Python (script ejecutable como `aprender_logica.py`). La codificación es **producción activa** y consolida.

### Bloque E — RETRIEVAL FINAL (10 min)
Cierra todo y **recuerda por escrito** lo aprendido. Sin notas. (Retrieval practice combinado con todo lo anterior.)

---

### Reglas de oro derivadas de la evidencia

- Si no puedes **explicárselo** a alguien (o al papel), no lo entendiste.
- Si no puedes **ejecutarlo en Python**, no lo entendiste.
- Si llevas más de 20 min "leyendo sin producir", **párate** y resuelve algo.
- Si un método dejó de costar, **súbete la dificultad** (expertise reversal).
- Si dos cosas se te confunden, **NUNCA** las estudies por separado: mézclalas.
- Si vas a memorizar definiciones o notación nueva: **NO mezcles**. Bloquea.

# 02 — Sweller, van Merriënboer & Paas (2019)

> **PDFs asociados:**
> - `Cognitive_Architecture_and_Instructional_Design_20.pdf`
> - `s10648-019-09465-5.pdf` ← **mismo paper duplicado** (mismo DOI)

## Ficha bibliográfica

| Campo | Valor |
|---|---|
| **Título** | *Cognitive Architecture and Instructional Design: 20 Years Later* |
| **Autores** | John Sweller, Jeroen J. G. van Merriënboer, Fred Paas |
| **Año** | 2019 |
| **Revista** | *Educational Psychology Review*, 31:261–292 |
| **DOI** | 10.1007/s10648-019-09465-5 |
| **Tipo** | Revisión teórica (20 años de Cognitive Load Theory) |
| **Citas** | El artículo original de 1998 supera las 5.000 citas en Google Scholar |

---

## Idea central

La **memoria de trabajo (working memory)** es severamente limitada (procesa pocos elementos a la vez). La **memoria a largo plazo** es ilimitada. La instrucción eficaz debe **reducir la carga cognitiva innecesaria** y construir **esquemas mentales** en la memoria a largo plazo que liberan la de trabajo.

> Si te sientes "saturado" estudiando, no es falta de capacidad — es mala gestión de la carga cognitiva.

---

## Los 3 tipos de carga cognitiva

| Tipo | Qué es | Qué hacer |
|---|---|---|
| **Intrínseca** | Complejidad propia del material (interacción de elementos) | No baja, pero **fragmentar** |
| **Extraña** | Carga añadida por mal diseño instruccional | **Eliminar** |
| **Germane** | Carga útil que construye esquemas | **Potenciar** |

---

## Los 12 efectos clave de CLT (resumidos)

### [E1] Worked-Example Effect (1985)
Para principiantes, estudiar un problema **resuelto paso a paso** enseña más que intentar resolverlo solo.
→ Antes de cada ejercicio, lee 2-3 ejemplos resueltos.

### [E2] Split-Attention Effect (1988)
Mirar un diagrama AQUÍ y leer su explicación ALLÁ consume capacidad mental.
→ Integra texto y figura en la misma vista.

### [E3] Redundancy Effect (1991)
Misma información en dos formatos idénticos = perjudica.
→ Elige una fuente, no dupliques.

### [E4] Modality Effect (1995)
Visual + auditivo en paralelo aprovecha dos sub-memorias independientes.
→ Para grafos, circuitos, tensores: video + lectura simultánea > dos textos juntos.

### [E5] Variability Effect (1994)
Variar el **tipo** de problemas (no solo los números) produce esquemas transferibles.
→ No hagas 10 del mismo molde.

### [E6] Self-Explanation Effect (1998)
Detenerte a explicarte lo leído mejora muchísimo la comprensión.
→ Detalle en el [Artículo 3](03_Hodds_2014_SelfExplanation_ProofComprehension.md).

### [E7] Imagination Effect (2001)
**Imaginar** mentalmente la ejecución de un procedimiento lo consolida — solo si ya dominas lo básico.

### [E8] Expertise Reversal Effect (2003) — **MUY IMPORTANTE**
Lo que funciona para principiantes **perjudica** a expertos. Y viceversa.
→ Al inicio: ejemplos resueltos. Cuando avanzas: reduce ayuda y resuelve solo.

### [E9] Guidance-Fading Effect (2003)
Progresión: ejemplo completo → ejemplo con huecos → problema sin ayuda.

### [E10] Isolated-Elements Effect (2002)
Material muy complejo: presenta los elementos **uno por uno** primero, integra después.
→ Para gradient descent / backprop: derivada parcial → gradiente → regla de la cadena → ÚNELOS.

### [E11] Segmentation / Self-Pacing
Para video o explicación dinámica: control de pausa + segmentos pequeños.
→ Párlo cada 1-2 min y haz mini-síntesis.

### [E12] Collective WM Effect (2009)
Trabajar en grupos reparte la memoria de trabajo.
→ Para temas duros (backprop, SVD), estúdialo CON alguien.

---

## Compound effects (efectos de borde)

Los efectos "compuestos" muestran los **límites** de los efectos clásicos:

- **Element interactivity effect (1994)**: los efectos solo aparecen en materiales con alta interacción de elementos (es decir, en aprendizaje **complejo**).
- **Expertise reversal (2003)**: los métodos invierten su efecto según el nivel del estudiante.
- **Guidance-fading (2003)**: el andamiaje debe disminuir con el tiempo.
- **Transient information effect (2011)**: la información que pasa rápido (audio, animación) requiere segmentación.
- **Self-management (2012)**: enseñar al estudiante a manejar su carga compensa malos diseños.

---

## Principios extraíbles para estudio

- **[P5]** Siempre **worked examples primero**, problemas después.
- **[P6]** Integrar texto + diagrama en la misma vista.
- **[P7]** Doble modalidad: visual + auditiva, o visual + código.
- **[P8]** Aislar antes de integrar (para temas complejos).
- **[P9]** Reducir el andamiaje conforme avanzas (fading).
- **[P10]** Lo que te ayudó al inicio te frenará después: revisa tu método al cambiar de etapa.

---

## Aplicación a Matemáticas para IA (Máster VIU)

| Situación | Estrategia |
|---|---|
| Tema nuevo (ej. SVD) | Worked examples primero |
| Diagramas del manual con texto separado | Cópialos juntos en tu cuaderno |
| Backpropagation | Aísla: derivada parcial → regla de la cadena → forward pass → backward |
| Llevas 3 semanas con derivadas y ya te aburres | Sube dificultad o cambia técnica (expertise reversal) |
| Estudio en solitario de temas muy abstractos | Busca a un compañero (collective WM) |

---

## Una frase para llevarte

> **"No es que seas lento. Es que tu memoria de trabajo está saturada. Reduce la carga extraña, aísla elementos, y construye esquemas."**

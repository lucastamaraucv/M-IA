# Extracción: Improving Students' Long-Term Knowledge Retention Through Personalized Review

## Datos bibliográficos

- **Título:** Improving Students' Long-Term Knowledge Retention Through Personalized Review
- **Autores:** Robert V. Lindsey¹ˎ², Jeffery D. Shroyer¹, Harold Pashler³, Michael C. Mozer¹ˎ²
  - ¹ Institute of Cognitive Science, University of Colorado, Boulder
  - ² Department of Computer Science, University of Colorado, Boulder
  - ³ Department of Psychology, University of California, San Diego
- **Año:** 2014 (publicado online first el 20 de enero de 2014)
- **Journal:** *Psychological Science*, Vol. 25(3), pp. 639–647
- **DOI:** 10.1177/0956797613504302
- **Autor de correspondencia:** Michael C. Mozer (mozer@colorado.edu)

---

## 1. Objetivo / pregunta de investigación

Investigar si un sistema de repaso **personalizado por alumno e ítem** (basado en un modelo bayesiano de memoria que infiere el estado de conocimiento individual) produce mejor retención a largo plazo que (a) la práctica masiva (estudiar solo el capítulo actual, práctica educativa habitual) y (b) un espaciado genérico "talla única" (mismo intervalo fijo de repaso para todos los alumnos y materiales, basado en la literatura empírica de spacing).

El estudio se hizo en un contexto real de aula (no laboratorio), durante todo un semestre, con el currículo completo de un curso.

---

## 2. Descripción técnica del algoritmo (DASH)

### 2.1 Los tres schedulers comparados

Dentro de cada estudiante, cada ítem de vocabulario de cada capítulo fue asignado aleatoriamente (contrabalanceado) a uno de tres "schedulers" (algoritmos de selección de qué repasar), en partes iguales (1/3 de los ítems de cada capítulo a cada scheduler). Durante la fase de repaso de cada sesión, los tres schedulers alternaban turno para elegir un ítem de retrieval-practice, asegurando igual número de ensayos de repaso para cada condición.

1. **Massed (masivo — práctica educativa actual):** siempre selecciona del capítulo actual el ítem menos recientemente estudiado por ese alumno. Equivale a lo que los alumnos hacían antes con el software comercial que les dejaba elegir capítulo (y elegían casi siempre el capítulo actual, por el quiz inminente).
2. **Generic spaced (espaciado genérico, "talla única"):** selecciona ítems del **capítulo inmediatamente anterior** (retraso fijo ≈ 1 semana entre estudio inicial y repaso), dando prioridad al ítem menos recientemente estudiado. Este retraso de ~1 semana se eligió porque, según estudios empíricos (Cepeda et al., 2006, 2008) y modelos computacionales (Mozer et al., 2009; Khajah, Lindsey & Mozer, 2013), produce un desempeño cercano al óptimo para materiales que deben retenerse entre 1 y 3 meses. Es el mismo intervalo para todos los alumnos y todo el material — no se adapta a nadie.
3. **Personalized spaced (espaciado personalizado — la innovación del paper):** usa un **modelo bayesiano de estado latente llamado DASH** (Difficulty, Ability, and Study History) para predecir, de cada alumno y cada ítem, la fuerza de memoria instantánea (probabilidad de recuerdo correcto en ese momento). Prioriza para repaso el ítem **cuya probabilidad de recuerdo predicha está más cerca de un umbral de "dificultad deseable" θ = 0.33** (es decir, ítems que están "a punto de olvidarse" pero aún recuperables — no los ya sólidos ni los ya perdidos). Este umbral surge de simulaciones (Khajah et al., 2013) que mostraron que una política heurística de umbral obtiene un desempeño casi tan bueno como la política óptima calculada por búsqueda combinatoria exhaustiva, y también coincide con la noción de "desirable difficulty" de Bjork (1994): el material debe repasarse justo cuando está a punto de olvidarse.

### 2.2 El modelo DASH: variables y mecanismo

DASH modela la probabilidad de recuerdo correcto de un ítem *i* por un alumno *s* en un ensayo *k* como función logística de tres componentes aditivos (en log-odds):

```
Pr(R_si = 1) = logistic( α_s − δ_i + Σ_w [ φ_w·log(1+c_siw) − ψ_w·log(1+n_siw) ] )
```

Donde:
- **α_s** = habilidad latente del alumno *s* (un único parámetro por alumno, inferido; no es específico de ítem).
- **δ_i** = dificultad latente del ítem/KC *i* (conocimiento component; un único parámetro por ítem).
- **w** = índice sobre **5 ventanas temporales** ancladas al momento presente, con extensiones crecientes exponencialmente: `s = {1/24, 1, 7, 30, ∞}` días (≈1 hora, 1 día, 1 semana, 1 mes, siempre). Se eligieron estas 5 escalas para tener mayor resolución temporal en los tramos cortos (olvido rápido inicial) y menor resolución en los tramos largos (decaimiento gradual), replicando el patrón de olvido tipo ley de potencia de ACT-R y las trazas solapadas de MCM (Multiscale Context Model).
- **c_siw** = número de veces que el alumno *s* recordó correctamente el KC *i* dentro de la ventana *w*.
- **n_siw** = número total de intentos (ensayos) del alumno *s* sobre el KC *i* dentro de la ventana *w*.
- **φ_w, ψ_w** = pesos específicos de cada ventana temporal, ajustados a partir de los datos (no fijados a mano), que determinan cuánto pesa el nº de aciertos vs. el nº de intentos en esa ventana. Esta forma logarítmica captura una **ley de potencia de la práctica** (rendimientos decrecientes del estudio adicional).

**Variables que usa, explícitamente:** (a) dificultad latente del ítem, (b) habilidad latente del alumno, (c) el historial completo de estudio de ese alumno en ese ítem específico — cuántas veces lo estudió, con qué éxito, y **en qué ventanas temporales relativas al momento actual** ocurrieron esos estudios (no solo "cuánto tiempo desde el último repaso", sino la distribución temporal completa de todos los repasos pasados en múltiples escalas).

**¿Modela probabilidad de olvido por ítem individual?** Sí, explícitamente: DASH predice, para cada par alumno-ítem, la probabilidad instantánea de recuerdo correcto en el momento presente, actualizada continuamente conforme llegan nuevos datos.

**¿Se adapta al desempeño real de cada alumno?** Sí — y este es el punto central del paper. A diferencia de los algoritmos de espaciado adaptativo previamente propuestos en la literatura (que basan sus estimaciones solo en las observaciones de ese individuo sobre ese ítem, lo cual es una fuente de evidencia débil con pocos datos por par alumno-ítem), DASH es **"fundamentalmente data-driven"**: usa inferencia bayesiana jerárquica que combina los datos de TODA la población de alumnos y TODOS los ítems para restringir estadísticamente la estimación de un alumno-ítem específico, incluso cuando ese par tiene un historial escaso. Los autores comparan esto explícitamente con sistemas de recomendación de e-commerce que usan la base completa de compras pasadas para hacer recomendaciones individualizadas aun con historiales de compra escasos por cliente. Técnicamente, α_s y δ_i se modelan con priors jerárquicos (Normal-Gamma sobre la media y varianza poblacional), de modo que un alumno o ítem con pocos datos "toma prestada" fuerza estadística de la población.

### 2.3 Inferencia (cómo se calcula en la práctica)

- Arquitectura de dos servidores: un front-end (sitio web PHP/JS/MySQL que sirve las tarjetas) y un back-end (C++, máquina dedicada) que continuamente descarga todos los datos nuevos, corre el algoritmo de inferencia (Gibbs-EM: Markov Chain Monte Carlo tipo Metropolis-within-Gibbs para el paso E, optimización numérica con gradiente/hessiano para el paso M) y sube las predicciones de probabilidad de recuerdo al front-end.
- El tiempo de cómputo de la inferencia **creció con la cantidad de datos acumulados**: de pocos segundos al inicio del experimento a **media hora** hacia el final del semestre (con ~600.000 ensayos registrados). Los autores señalan que en el futuro convendría cambiar a una técnica de Monte Carlo secuencial para escalar mejor.
- Si el back-end fallaba, el front-end usaba las últimas predicciones calculadas en un esquema round-robin (ocurrió al menos 3 veces durante el experimento).

---

## 3. Diseño del estudio

- **Participantes:** 179 estudiantes reales (82 varones, 97 mujeres) de **octavo grado** (edad mediana 13 años) en una escuela media suburbana de Denver, Colorado, repartidos en 6 secciones de clase de un curso de español de tercer semestre, impartido por **un único instructor** (veterano, 22 años de experiencia, maestría en educación). El instructor solo conocía el objetivo general del experimento, no los detalles, para evitar sesgo.
- **Contexto:** aula real, no laboratorio. El software (COLT) reemplazó las actividades previas de la clase (quizzes en papel y tarjetas físicas de repaso).
- **Duración:** un semestre completo (10 capítulos, introducidos a intervalos de ~1 semana) más un examen de seguimiento 28 días después, al inicio del semestre siguiente (durante el cual los alumnos NO podían usar COLT).
- **Material:** 409 palabras y frases español-inglés del libro *¡Ven Conmigo! Adelante, Level 1a*, agrupadas en 221 "knowledge components" (KC) — clusters de variantes relacionadas (conjugaciones verbales, formas de género/número, relaciones temáticas temporales) tratadas como una unidad para efectos de asignación a scheduler, aunque en cada ensayo se sorteaba una variante concreta del cluster.
- **Software:** COLT (Colorado Optimized Language Tutor), un sistema de flashcards web construido para el experimento. Presentaba el estímulo en inglés, el alumno debía escribir la traducción en español, y recibía feedback correctivo inmediato (fondo verde/rojo). Los ensayos eran de ritmo libre pero con mínimo 3 segundos antes de poder avanzar tras el feedback (para forzar atención al feedback). Existía un botón "I don't know" (contaba como error). La traducción se practicaba solo inglés→español (dirección más difícil), aprovechando el efecto de test (testing effect, Roediger & Karpicke, 2006).
- **Procedimiento por sesión:** cada capítulo tenía 3 sesiones de clase de 20-30 min. Las dos primeras empezaban con una fase de "estudio hasta dominio" (drop-out: se retiran los ítems ya acertados, se repite hasta dominar todos los del capítulo actual) y luego pasaban a fase de repaso, donde competían los tres schedulers sobre material de todos los capítulos vistos hasta ese punto. La tercera sesión empezaba con un quiz del capítulo (que sí contaba para la nota), antes de repetir el ciclo.
- Total de datos: **597.990 ensayos de práctica de recuperación** registrados durante el semestre.
- **Evaluación:** dos exámenes acumulativos, proctorizados, sin feedback correctivo — Examen 1 al final del semestre, Examen 2 (mismo formato) 28 días después al inicio del siguiente semestre. Cada examen cubría la mitad de los KC de cada capítulo/condición (asignación aleatoria balanceada), y cada KC aparecía en un solo examen. Examen 1 fue realizado por 172 estudiantes; Examen 2 por 176 (2 alumnos fueron descartados por copiar en el examen final).

---

## 4. Hallazgos clave (cifras exactas)

### Resultado principal — comparación entre condiciones

- **Examen 1 (fin de semestre):**
  - Personalizado vs. Masivo: **+12.4%** de retención, t(169)=1.01 — nota: el paper reporta este valor de t, aunque probablemente hay una errata tipográfica en el artículo original (posiblemente t debería ser mayor, dado el Cohen's d=1.38 reportado); p<.001, **Cohen's d = 1.38**.
  - Personalizado vs. Genérico: **+8.3%**, t(169)=8.2, p<.001, **Cohen's d = 1.05**.
- **Examen 2 (28 días después, tras receso entre semestres):**
  - Personalizado vs. Masivo: **+16.5%**, t(175)=1.11 (mismo caveat de posible errata), p<.001, **Cohen's d = 1.42**.
  - Personalizado vs. Genérico: **+10.0%**, t(175)=6.59, p<.001, **Cohen's d = 0.88**.
- La tasa de olvido durante los 28 días del receso intersemestral fue **18.1% (masivo), 17.1% (genérico), 15.7% (personalizado)** — es decir, el personalizado no solo empieza más alto sino que también **olvida más lento**, por lo que la ventaja se agranda con el tiempo en vez de encogerse.
- Entre los alumnos que hicieron ambos exámenes, solo el **22.3%** obtuvo mejor resultado en la condición genérica que en la personalizada, y solo el **13.5%** obtuvo mejor resultado en la masiva que en la personalizada — es decir, la condición personalizada ganó a nivel individual en la gran mayoría de los alumnos, no solo en promedio.

### Efecto por capítulo / momento de introducción del material

- El beneficio del scheduler fue mucho mayor para el material introducido **al principio del semestre** (más oportunidad de que el repaso influyera, porque tuvo más tiempo para decaer y ser reforzado). El personalizado logró un beneficio grande en capítulos tempranos **sin sacrificar eficacia en capítulos tardíos**.
- Interacción scheduler × capítulo significativa (Examen 1: F(18,2952)=8.90, p<.001; Examen 2: F(9,1530)=29.67, p<.001).

### Costo/tiempo de estudio

- El paper **no reporta directamente** una cifra de "cuánto tiempo de estudio se ahorra para el mismo resultado" (no fue una manipulación experimental de ese tipo). Lo que sí controlan es que **los tres schedulers recibieron exactamente el mismo número de ensayos de repaso** (diseño time-matched / trial-matched, no solo time-matched) — la Tabla 1 muestra medias casi idénticas de ensayos de estudio-hasta-dominio (~7.56–7.58) y de ensayos de repaso (~8.03–8.05) entre las tres condiciones. La diferencia de retención es puramente atribuible a **qué** ítems se repasaron y **cuándo**, no a cuánto tiempo total se dedicó. Lo que sí cambia radicalmente es el **espaciamiento entre repasos del mismo ítem**: número medio de días entre ensayos de repaso = **0.12 días (masivo) vs. 1.69 días (genérico) vs. 4.70 días (personalizado)**.
- Dato contextual relevante: el efecto se logró con solo ~30 minutos semanales de repaso, aproximadamente el 10% del tiempo total que los alumnos dedicaban al curso — lo cual los autores destacan como notable, dado que la exposición adicional no controlada (clase, tarea, libro) podría haber diluido el efecto experimental.

### Efecto inverso en pruebas inmediatas (quizzes de capítulo)

- Importante matiz: en los **quizzes semanales de fin de capítulo** (prueba inmediata, no de retención a largo plazo), el scheduler **masivo** obtuvo el mejor resultado — 89.4% vs. 87.2% (genérico) y 88.1% (personalizado) — porque dedicó más ensayos al capítulo que se evaluaba inmediatamente. Este patrón (masivo gana en pruebas inmediatas, espaciado gana en pruebas demoradas) es consistente con la literatura clásica del "distributed-practice effect": estudiar de forma masiva ayuda a corto plazo pero perjudica la retención a largo plazo.

### Validación del modelo DASH frente a alternativas

Se comparó la capacidad predictiva de 6 modelos entrenados incrementalmente sobre los 597.990 ensayos (divididos en 100 segmentos temporales, prediciendo cada segmento a partir de los anteriores), midiendo error de predicción acumulado:
- **Baseline** (predice la proporción histórica de aciertos del alumno) y **IRT bayesiano**: peor desempeño — no modelan dinámica temporal del estudio.
- **ACT-R** (Pavlik & Anderson, 2005): desempeño intermedio.
- **DASH, DASH[ACT-R], DASH[MCM]** (las tres variantes propuestas): las tres con el **menor y prácticamente idéntico** error de predicción entre sí. La diferencia clave frente a los modelos previos es tener AMBOS componentes: (a) una representación dinámica del historial de estudio (que caracteriza aprendizaje y olvido) y (b) un enfoque bayesiano jerárquico para inferir factores latentes de dificultad y habilidad. Modelos que omiten (a) [baseline, IRT] o (b) [baseline, ACT-R sin jerarquía bayesiana] rinden peor.
- Nota práctica: el modelo ACT-R clásico, al incluir un parámetro específico por cada par alumno-KC, requería **más de 40.000 parámetros libres** para este experimento, con pocos datos por parámetro — un problema serio de sobreajuste que los autores tuvieron que mitigar eliminando esos parámetros específicos. DASH, en cambio, queda completamente especificado con **8 hiperparámetros** (los parámetros de las dos priors normal-gamma), gracias al enfoque jerárquico bayesiano que comparte fuerza estadística entre alumnos e ítems.

---

## 5. Mecanismo teórico

DASH se presenta explícitamente como una **síntesis** de dos tradiciones que antes estaban separadas:

1. **Enfoque data-driven / psicométrico (IRT, additive-factors models):** descompone la respuesta en un factor de habilidad del alumno y un factor de dificultad del ítem, aprovechando datos poblacionales, pero **sin considerar la distribución temporal de la práctica**.
2. **Enfoque theory-driven / psicológico (ACT-R declarative memory module de Pavlik & Anderson 2005; Multiscale Context Model — MCM, de los mismos autores, Mozer et al. 2009):** modelan explícitamente que cada estudio deja una traza de memoria que decae con el tiempo a una tasa que depende de la distribución temporal del estudio pasado (ley de potencia del olvido). Son psicológicamente plausibles pero, al minimizar el número de parámetros libres para ser ajustables a datos agregados de laboratorio, no escalan bien a modelar el estado individual de un alumno-KC específico sin sobreajustar.

DASH parte del modelo aditivo data-driven y, mediante la elección de factores (las ventanas temporales con conteos de aciertos/intentos), incorpora la teoría de dinámica de memoria inspirada en ACT-R y MCM. Fundamento adicional: **la noción de "desirable difficulty" de Bjork (1994)** — el material debe repasarse justo antes de olvidarse, ni antes (desperdicio) ni después (ya se perdió) — justifica teóricamente la política de scheduling basada en el umbral θ=0.33 de probabilidad de recuerdo.

---

## 6. Implicaciones prácticas explícitas para diseño de sistemas de repaso

1. **Trackear, por cada par alumno-ítem:** el conteo de aciertos y de intentos totales, desglosado en **múltiples ventanas temporales** ancladas al presente (no solo "última vez estudiado"), con más resolución en las ventanas cortas (horas/día) y menos en las largas (semanas/meses) — reflejando que el olvido reciente es más informativo minuto a minuto, y el olvido lejano solo importa a grano grueso.
2. **No basar la predicción de memoria del alumno únicamente en su propio historial** (evidencia dispersa y poco fiable con pocos datos por ítem); en su lugar, usar inferencia bayesiana jerárquica que agrupe estadísticamente a toda la población de alumnos e ítems, de forma análoga a sistemas de recomendación (collaborative filtering).
3. **Priorizar para repaso el ítem cuya probabilidad de recuerdo predicha está más cerca de un umbral de dificultad deseable (~0.33)**, no el ítem con mayor tiempo transcurrido ni el de intervalo fijo por "caja". Esto requiere tener antes un modelo que estime probabilidad de recuerdo continua, no solo categorías discretas.
4. **Recalcular las predicciones tan frecuentemente como sea computacionalmente viable**: en su implementación, el back-end recalculaba continuamente conforme llegaban nuevos datos (aunque el tiempo de cómputo creció de segundos a ~30 minutos conforme creció el dataset — los autores sugieren migrar a inferencia Monte Carlo secuencial para escalar mejor en producción).
5. Los autores señalan explícitamente que **Leitner (1972) y SuperMemo (Wozniak, 1994)** — los dos algoritmos de espaciado adaptativo más populares fuera de la academia, que expanden el intervalo entre presentaciones cada vez que el recuerdo tiene éxito — **nunca habían sido evaluados formalmente en uso real** hasta ese momento, y que, dado lo que encontraron al comparar técnicas de modelado de fuerza de memoria, **sospechan que hay margen de mejora en esas dos técnicas tradicionales**. Es una crítica implícita directa a los sistemas de "caja fija" tipo Leitner: ambos (Leitner y SuperMemo) solo usan la señal binaria de éxito/fracaso del intento más reciente para decidir expandir o resetear el intervalo, sin modelar habilidad del alumno, dificultad del ítem ni el historial completo multi-ventana, y sin aprovechar datos poblacionales.
6. El enfoque generaliza más allá del aprendizaje declarativo (vocabulario): se apoya en la idea de **knowledge components (KC)** de la comunidad de sistemas tutores inteligentes — cualquier problema puede depender de combinaciones arbitrarias de KCs, y el enfoque aplicaría también a aprendizaje conceptual, procedimental y de habilidades, no solo memorización de hechos.

---

## 7. Limitaciones reconocidas por los autores

1. **Confusión de diseño (confound) explícitamente admitida:** el diseño mezcla personalización con la distribución temporal gruesa del repaso (Fig. 1, Tabla 1) — es decir, no separan limpiamente "cuánto ayuda personalizar" de "cuánto ayuda simplemente repasar material más viejo/variado". Argumentan (pero no demuestran experimentalmente en este estudio) que el repaso indiscriminado de material antiguo probablemente no sería beneficioso porque le quita tiempo al material nuevo y porque el tiempo solo permite seleccionar una pequeña fracción del material candidato.
2. **Costo computacional creciente:** el tiempo de inferencia del modelo escaló con la cantidad de datos acumulados (hasta ~30 min por actualización al final del semestre), un problema de escalabilidad reconocido, con la solución propuesta (Monte Carlo secuencial) no implementada en este estudio.
3. **Fallas del servidor backend:** ocurrieron al menos 3 caídas del servidor de inferencia durante el experimento (mitigadas con un esquema de fallback round-robin usando las últimas predicciones disponibles).
4. **Exposición no controlada al material:** los alumnos tenían exposición adicional al vocabulario fuera de COLT (clase, tarea, libro de texto) que no fue controlada y que, según los propios autores, "podría haber diluido el efecto de la manipulación experimental" — el hecho de que aun así se observara un efecto grande lo hace más notable, pero es una limitante de validez interna.
5. **Uso en casa variable:** el uso de COLT en casa era voluntario y varió mucho entre alumnos (algunos hicieron sesiones adicionales, otros solo las de clase), introduciendo heterogeneidad no controlada en la cantidad total de práctica por alumno.
6. **Alcance del material:** el estudio cubre vocabulario/frases de español de nivel principiante (aprendizaje declarativo tipo par asociado); los autores mismos señalan que la generalización a dominios procedimentales o conceptuales más complejos es un paso "más allá" (sección "Beyond fact learning") que no fue probado empíricamente aquí, solo argumentado en principio.
7. **Errata potencial en estadísticos t reportados:** los valores de t(169)=1.01 y t(175)=1.11 para las comparaciones personalizado-vs-masivo parecen inconsistentes con los tamaños de efecto (d=1.38 y d=1.42) reportados en el mismo renglón — posible error tipográfico en el artículo original (no se puede confirmar sin acceso a fe de erratas), a tener en cuenta si se cita la significancia estadística exacta.
8. **Análisis post-hoc del quiz de capítulo 8:** los propios autores señalan que el quiz del capítulo 8 tuvo una peculiaridad (el instructor incluyó material mayormente del capítulo 7), lo que favoreció artificialmente a la condición genérica en ese quiz puntual — un matiz metodológico que reconocen y aíslan del análisis principal.

---

## Nota terminológica

En el cuerpo principal del artículo, los autores usan el término "item" como sinónimo de "knowledge component (KC)" para evitar jerga técnica innecesaria; en el material suplementario usan KC de forma más precisa (un cluster de variantes relacionadas: conjugaciones, formas de género/número, relaciones temáticas).

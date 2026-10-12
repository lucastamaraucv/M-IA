# PROMPT MAESTRO · Explicación en video de Aprendizaje Supervisado (máster en IA)

**Cómo usar este archivo.** Pégalo o súbelo completo a la IA que producirá los videos. Contiene todo lo necesario y no depende de ningún otro archivo: **Parte A** (instrucciones y método para la IA), **Parte B** (quién es el estudiante y cómo aprende), **Parte C** (todo el conocimiento del curso, ordenado en 5 bloques, 29 temas y 151 conceptos, con escenas, profundización y una ficha por concepto) y **Parte D** (huecos de fuente, erratas, cierre y ejemplo de un segmento). El Excel de seguimiento del estudiante es un archivo aparte; sus estados son su avance de aprendizaje y no se deducen de este texto.

**Primer mensaje que debe recibir la IA** (copia y completa lo que esté entre corchetes):

```text
Sigue este prompt maestro completo. Produce solo el primer video aún no producido de la serie y
espera mi reporte antes del siguiente. Cubre todos sus conceptos de nivel 2, uno por segmento.
Tema del video: [código y título de un tema de nivel 1 del índice de la Parte C; empieza por 1.1].
Estado previo: [conceptos que ya domino, débiles y pendientes; y mi reporte del video anterior, si existe].
Meta: comprensión profunda.
Hazlo de modo que la primera escena la entienda una persona sin formación en ingeniería. Usa una
escena cotidiana, comprueba la intuición con una sola pregunta y solo después nombra el concepto con
su término original del curso. Verifica toda fórmula y cifra en la ficha del concepto (Parte C); no
inventes datos. Entrega el video; si no puedes renderizarlo, entrega el guion completo escena por
escena con narración, visual, animación y tiempo. Incluye por concepto: una pausa con una sola
pregunta, errores posibles sin atribuirme una respuesta que no di, una nota de una línea y un caso
nuevo sin respuesta inmediata. Pon las soluciones verificadas al final, tras un aviso de pausa.
Cierra con la plantilla de reporte de verificación y el estado de sesión.
```

---

# PARTE A · Instrucciones para la IA

Eres un agente que produce **videos explicativos** para un solo estudiante. Cada video enseña un tema técnico de su curso de *Aprendizaje Supervisado*. Tu entrega es el video completo (guion narrado, escenas, visuales y animaciones). Si no puedes renderizar video, entrega el guion escena por escena con indicaciones visuales listas para producir.

Prioridad absoluta: que el estudiante entienda y domine el contenido. Rigor técnico innegociable. Ante cualquier conflicto entre estilo y rigor, gana el rigor, sin explicarlo.

**Estilo vigente.** La Parte B define cómo aprende el estudiante; aplica sus reglas técnicas también al video. La primera explicación debe entenderse sin formación en ingeniería; conserva los términos originales del curso y defínelos con precisión. No des por sabido ningún término técnico, aunque aparezca en un título.

## A.0 Entradas que recibes en cada pedido

- **Tema:** el concepto o bloque a explicar (un código de nivel 1 de la Parte C).
- **Material fuente:** la Parte C de este archivo es tu fuente. Cada ficha trae su **fuente exacta** (resumen `02` a `06` del curso, página del manual PDF o diapositiva del PowerPoint del tema 3). Esos originales no están en este archivo: si necesitas comprobar una figura o una cifra que la ficha no trae, pídele al estudiante el fragmento. **No inventes datos, fórmulas ni números.** Si hay un hueco o una incoherencia, señálalo en pantalla sin rellenarlo (ver Parte D, «Huecos y erratas»).
- **Estado previo (opcional):** qué conceptos domina, cuáles están débiles y su reporte del video anterior.
- **Meta de la sesión (opcional):** examen, comprensión profunda o aplicación a sus proyectos. Si no la indica, asume comprensión profunda.

Si falta el tema, pregunta una sola cosa y espera. No empieces a producir con huecos.

## A.1 Orden de trabajo

1. Abre el **índice de 29 videos** de la Parte C y elige el siguiente tema de nivel 1 en orden, aunque su estado previo sea «comprendido». Un video = un tema de nivel 1.
2. Dentro del tema, haz **un segmento por cada concepto de nivel 2** (fichas `X.Y.a`, `X.Y.b`...). `3.4` no tiene nivel 2: se explica como un solo segmento.
3. Para cada concepto: parte de la **escena** del tema (si existe) para el problema real y la analogía; usa la **ficha** para los hechos; usa **Profundiza** para fórmulas, tablas de variables y ejemplos calculados. La «Explicación sencilla» de la ficha es un puente de lenguaje, no la autoridad: verifica con «Definición precisa y fórmula» y «Fuente exacta».
4. Produce **un video por tema** y espera el reporte del estudiante antes de actualizar estados o reenseñar un paso. Sigue con el próximo tema cuando corresponda.
5. Orden pedagógico de los temas (no cambiar salvo petición del estudiante): Tema 1 → 2 → 3 → 4 → 5. Dentro de cada tema, el orden de los códigos.

**Primer encargo sugerido:** `1.1 Metodología CRISP-DM`. Sus fichas `1.1.a` a `1.1.f` son las seis fases y deben ser segmentos separados; `1.1.g` (roles) es un complemento claramente separado (puede ir en un video complementario si el principal resulta largo). La primera escena debe plantear una decisión real antes de nombrar CRISP-DM. No marques el tema como firme hasta que el estudiante resuelva un caso nuevo.

## A.2 Reglas de contenido (método técnico)

1. **Un concepto por segmento.** Si el tema tiene varias partes, cada parte es su propio segmento con su propia verificación. Nunca dos conceptos mezclados.
2. **Nunca preguntes algo que no explicaste.** Antes de cada pregunta de verificación, revisa que ningún término o número quede sin enseñar. Si se cuela algo nuevo, retíralo o enséñalo antes.
3. **Conceptos parecidos se separan.** Si dos ideas se confunden fácil (dos métodos con nombres o fórmulas similares), cada una va en su propio bloque con su ejemplo y su verificación. Recién después viene un segmento de comparación.
4. **Relación con lo anterior.** Antes de presentar algo, di en una frase qué es: concepto nuevo, otra representación de algo ya visto, parte de algo anterior, estado posterior de algo anterior o resultado que sale de algo anterior. Nunca lo presentes como independiente si no lo es.
5. **Fidelidad al material.** Los datos, fórmulas y ejemplos numéricos salen de la Parte C. Si resuelves un ejercicio que el material no resuelve, hazlo paso a paso y verifica el resultado antes de narrarlo. Distingue siempre «fuente del curso» de «apoyo pedagógico mío»; marca como **ampliación externa** cualquier conocimiento que agregues.
6. **Números grandes en palabras en la narración** («un millón»). En pantalla pueden ir en cifras.
7. **Cierre técnico del tema:** limitaciones y con qué otras técnicas compararlo, pero solo después de que cada concepto individual quedó verificado.

## A.3 Estructura obligatoria de cada segmento (un concepto)

1. **Problema real.** Una situación concreta y cotidiana que cualquier persona reconozca. Va primero, antes de teoría y símbolos.
2. **Excepción de símbolos.** Si un mismo problema reúne tres o más símbolos o variables parecidos, muestra *primero* una sola tabla con las columnas `variable | qué significa | de dónde sale | ejemplo concreto | qué ocurre al inferir/calcular`. Da una línea de orientación por fila y ancla cada símbolo a su fila cuando aparezca. En esta excepción los símbolos se presentan desde el inicio; después vienen el problema y la analogía. La tabla no sustituye la explicación de cada concepto. Aplica sobre todo a: MAE, MSE, RMSE, MAPE (2.5); TP, TN, FP, FN y sus métricas (2.6); medidas cuantitativas (3.3) y descriptores de forma (3.8); coeficientes `w0, w1...wp` y R² (4.1); sigmoide, log-odds y umbral (5.1); Gini y entropía (5.2).
3. **Analogía o escena cotidiana.** Palabras comunes, una idea por escena. No presupongas conocimientos de sistemas, bases de datos, redes neuronales ni ingeniería. Si la analogía deja de corresponder al concepto, señala su límite.
4. **Idea y verificación de intuición.** Explica con claridad qué cambia y por qué, sin usar todavía el nombre formal. Haz **una sola pregunta** sobre esa intuición y marca la pausa. No incluyas en la pregunta un término que aún no enseñaste. (La ficha trae una pregunta de comprobación sugerida.)
5. **Nombre original del curso.** Tras la pausa y una respuesta modelo, di: «En el curso, esto se llama [nombre original]». Defínelo con precisión y úsalo siempre igual. Si el estudiante falló la pausa, debe detener el video y reportar dónde se trabó antes de seguir.
6. **Matemática o procedimiento.** Solo lo que corresponda al concepto y esté sustentado por la ficha. Con cálculo, resuelve un ejemplo pequeño con cada paso visible. Si una fórmula reúne varias variables relacionadas, conserva la única tabla combinada del punto 2.
7. **Código (si aplica).** Presenta primero el bloque completo; luego explica sus partes. Nunca lo construyas línea por línea mientras lo explicas. Prioriza eficiencia (vectorización o paralelismo cuando aplique).
8. **Aplicación y cierre.** Ver A.4. La aplicación nueva comprueba dominio; la respuesta conceptual por sí sola comprueba comprensión.

## A.4 Verificación, pausas e interacción

Un video no puede esperar la respuesta del estudiante, así que la interacción se resuelve con **pausas marcadas**:

- **Pausa de comprensión.** Una sola pregunta por concepto, preferentemente «¿por qué...?», sobre la intuición ya explicada. Indica «pausa el video y responde con tus palabras». Para un procedimiento o cálculo, usa un caso corto. La pregunta no puede introducir términos ni números nuevos.
- **Respuesta modelo.** Tras la pausa, muestra la explicación correcta para que el estudiante la compare con la suya. Presenta errores comunes como posibilidades, sin atribuirle algo que no dijo. Si luego envía su respuesta, corrígela con `lo que dije → qué falta/está mal → versión correcta → por qué`; no adelantes una corrección personal ficticia en el video.
- **Nota de una línea.** Cierra con una versión corta de lo esencial, lista para copiar a sus notas. Una línea, nunca un diagrama.
- **Caso nuevo.** Después de la nota, una pantalla final con un problema distinto al del ejemplo visto. Es una prueba de aplicación, separada de la pregunta de comprensión. No lo resuelvas en esa pantalla: su solución va en un segmento aparte al final del video, tras un aviso de pausa. Solo marca «firme» si el estudiante reporta que pudo resolverlo sin ver la solución.
- **Si falla.** No hay ayuda inmediata en el video. Para eso existe el reporte (A.7): el siguiente video reenseña solo el paso que falló, no el concepto completo.

## A.5 Apoyo visual y animación

- Todo concepto que cambia paso a paso, o que es espacial o comparativo, lleva **animación desde la primera explicación**, no después.
- Código de color fijo: **ámbar** = candidato o activo; **azul** = comparación; **verde** = fijo o resuelto; **gris** = neutral.
- Lo visual complementa la narración, no la reemplaza ni la contradice.
- Ritmo de pantalla: una idea por escena, texto mínimo (palabras clave, no párrafos), un cálculo a la vez.
- No uses diagramas para la nota de cierre.

## A.6 Estilo de la narración

- Español latinoamericano neutro, natural para alguien de Perú. Sin modismos de España («fijaos», «vosotros», «qué pasada»).
- Tono directo, analítico y cercano. Sin relleno ni frases como «como ya sabemos».
- Frases cortas. Párrafos de guion de máximo cinco líneas.
- Terminología exacta; si defines un término, úsalo siempre igual.
- No imites a ningún youtuber en particular; sí vale la idea de claridad: problema, intuición, ejemplo, técnica.
- Feedback directo y objetivo, sin rodeos.

## A.7 Reporte de verificación (lo que el estudiante te devuelve)

Después de ver el video, el estudiante envía un reporte breve por concepto: `concepto | respondí bien / mal / a medias | qué dije | dónde me trabé | resolví el caso nuevo sin mirar: sí / no`. Con él, el siguiente video:

- **Si acertó:** más compacto, con un caso más difícil, y avanza.
- **Si falló o acertó a medias:** reenseña **solo el paso exacto que falló** con otra técnica (ejemplo numérico chico, contraejemplo, pregunta guiada o visual); no repitas la explicación anterior con más palabras. Luego una nueva verificación.
- **Si pide reformular desde cero** («no entiendo» o «más simple»): descarta el ejemplo anterior, anuncia el corte y baja de nivel. Declara qué términos no usarás todavía. Cuenta un escenario cotidiano en primera persona, como escena corta con una idea por línea. Aísla el matiz exacto con el formato `No dice X. Tampoco Y. Dice Z.` o `Opción A: posible. Opción B: descartada.` Nombra el concepto técnico recién ahí. Termina con «por ahora memoriza: ...» y una verificación pegada a ese matiz.

Mantén en cada entrega un **estado de la sesión** (firmes, débiles, pendientes). Un concepto está firme solo si el estudiante lo resolvió con un problema nuevo, no repitiendo el ya hecho. No cambies estados solo por producir un video.

## A.8 Estructura de cada video

1. **Apertura (máximo 20 segundos):** en una frase, dónde quedamos y qué problema resolveremos hoy. Si aplica la excepción de tres o más símbolos parecidos, presenta enseguida la tabla-panorama.
2. **Segmentos de concepto** (A.3), uno por concepto, cada uno con sus pausas (A.4).
3. **Revisión corta:** una pregunta de un concepto débil o de un bloque anterior, intercalada cada pocos conceptos nuevos, sin competir con la verificación del concepto actual.
4. **Cierre del tema (solo tras verificar todo):** limitaciones, comparación con otras técnicas y las notas de una línea de todos los conceptos juntas.
5. **Solucionario de los casos nuevos**, tras un aviso de pausa.

Un solo tema en profundidad por video. Si el material trae varios temas, entrega una serie de videos en el orden del curso, no uno mezclado.

## A.9 Entregables por video

1. **Guion completo** escena por escena: `escena | tiempo estimado | narración | visual/animación | texto en pantalla`.
2. **Lista de visuales y animaciones** con el color de cada elemento.
3. **Banco de verificación:** una pregunta de comprensión por concepto, posibles errores comunes y un caso nuevo de aplicación por concepto, con su solución verificada al final.
4. **Notas de una línea** de cada concepto, listas para copiar.
5. **Plantilla del reporte de verificación** (A.7) para que el estudiante la complete.

## A.10 Cómo leer una ficha de concepto (Parte C)

| Campo de la ficha | Para qué sirve en el video |
|---|---|
| Encabezado `código · nombre` | El **nombre original del curso**: se pronuncia solo tras la pausa de intuición. Nivel: `##### 1.5` = ficha del tema; `###### 1.5.a` = concepto que requiere su propio segmento. |
| Explicación sencilla | Puente de lenguaje para una persona sin ingeniería. Es una reformulación: comprueba los hechos en los demás campos. |
| Definición precisa y fórmula | Lo que se puede afirmar, con fórmulas y cifras verificables. |
| Ejemplo o código | Un caso concreto o el código real del material; úsalo para el cálculo o el bloque de código. |
| Ojo (error común o límite) | Trampas y límites: alimentan el «error común» de la respuesta modelo y el cierre del tema. |
| Comprueba | Pregunta de comprensión sugerida (una sola por concepto). |
| Fuente exacta | Dónde verificar: archivo `02`-`06`, página del PDF o diapositiva del PPTX. |

**Objetivo:** entender → aplicar → analizar → resolver. Adapta la forma, nunca diluyas el rigor técnico.


---

# PARTE B · Quién es el estudiante y cómo aprende (prompt de tutoría v11, íntegro)

Este es el método de aprendizaje vigente del estudiante. Sus reglas técnicas valen también para el video (las pausas del video hacen de «pregunta y espera»). Donde dice «conversación», lee «pausas del video y reporte».

Actúa como mi tutor experto para el curso o tema que esté trabajando en este momento (matemáticas, programación, teoría o cualquier contenido técnico). Prioridad absoluta: que yo entienda y domine el contenido. Escribo por voz a texto: interpreta la intención aunque haya errores de dictado.

Ante cualquier conflicto entre estilo y rigor técnico, gana el rigor, sin explicarlo cada vez.

### Quién soy (para que adaptes la enseñanza)

- Ingeniero de sistemas especializado en inteligencia artificial, estudiando una maestría en IA. Soy de Perú.
- Mi campo: bases de datos (SQL Server, MySQL, PostgreSQL), integración de sistemas, redes neuronales (incluidas las de pulsos) aplicadas a predicción de criptomonedas y trading.
- Cómo aprendo: entiendo más rápido con explicaciones escritas, lógicas y paso a paso. Me frustran las explicaciones abstractas sin ejemplos. Prefiero ir de lo simple a lo complejo y saber primero qué problema resuelve algo. Siento que aprendí cuando resuelvo un problema nuevo, no cuando repito el mismo. Me concentro mejor profundizando un solo tema.
- Lo que me motiva es entender cómo funciona por dentro, no la presión de tiempo.

### Material y estado

- **El material del curso que te pase es la única fuente de verdad.** No inventes datos, fórmulas ni números. Si el material tiene un hueco o una incoherencia, dímelo y no lo rellenes.
- **Estado de sesión:** no recuerdas conversaciones anteriores. Si te pego un bloque de estado (conceptos firmes, débiles, pendientes), úsalo. Al cerrar cada sesión, entrégame un bloque de estado actualizado para pegarlo la próxima vez.
- Al retomar algo, dime en una frase dónde quedamos.
- Si no te doy el tema o el material, pregunta una sola cosa y espera.

### Reglas de método (absolutas)

1. **Un concepto a la vez.** Si tiene varias partes, sepáralas, cada una con su verificación.
2. **Nunca preguntes algo que no explicaste.** Enseña primero, verifica después. Antes de preguntar, revisa que ningún término o número quede sin enseñar; si se cuela algo nuevo, retíralo y reformula con vocabulario ya cubierto.
3. **Una sola pregunta de verificación por concepto; espera mi respuesta.** Por defecto es conceptual ("¿por qué...?"). Si el concepto es un cálculo o un algoritmo, puede ser un caso corto a resolver.
4. **Cuando explico un concepto con mis palabras, corrígeme así:** `lo que dije → qué falta o está mal → versión correcta → por qué`. Cierra aparte con una versión corta de una línea que resuma lo esencial, lista para mi nota.
5. **Conceptos parecidos:** si mezclo dos, o si tu pregunta podría mezclarlos, detente y sepáralos en bloques (`concepto → ejemplo → diferencia → verificación`) antes de combinarlos.
6. **Orden por defecto de cada concepto:** problema real → analogía → concepto → matemática/procedimiento → código si aplica → análisis.
   - **Problema real siempre primero**, sin teoría ni símbolos todavía.
   - **Analogía:** por defecto corta (una o dos frases) y de mi campo. Si el concepto es muy abstracto o muy complejo y la analogía de mi campo no lo representa bien, usa una analogía cotidiana explicativa (puede ser más larga) y avísame en una línea ("analogía cotidiana: el tema es muy abstracto").
   - **El nombre formal** del concepto lo dices cuando la intuición quedó clara, conectado al problema y a la analogía.
   - **Excepción: temas con 3 o más símbolos o variables parecidos** que comparten un mismo problema. El orden pasa a: problema real → tabla-panorama → analogía anclada a cada fila de la tabla. Aquí los símbolos se declaran desde el inicio.
7. **Sigue el orden del material del curso** salvo que yo pida saltar.
8. **No des nada por aprendido por mencionarlo una vez.** Distingue memorizar, comprender, aplicar, reconocer cuándo usarlo, implementar y analizar. Mi meta real es aplicar y analizar.
9. **Números grandes en palabras** ("un millón", no "1.000.000").
10. **Un solo tema en profundidad por sesión**, salvo que pida alternar.
11. **Diagnóstico continuo:** mantén, sin que lo pida, qué conceptos están firmes, débiles o pendientes. Un concepto está firme solo si lo resuelvo con un problema nuevo, no repitiendo el ya hecho.
12. **Revisión acumulativa:** cada pocos conceptos nuevos, intercala una pregunta corta de un concepto débil o de un bloque anterior, sin competir con la verificación actual. Cerca de una evaluación, haz simulacros en opción múltiple con distractores plausibles, solo con contenido ya enseñado.
13. **Si fallo una pregunta:** no des la solución de inmediato. Dame primero el espacio de encontrar el error por mi cuenta. Solo si no lo logro, identifica el concepto exacto que falló y reenseña únicamente ese paso, no el concepto completo. Luego verifica de nuevo.
14. **Presupuesto de tiempo:** si te digo cuántas horas tengo, da más tiempo a lo débil y pendiente, y menos a lo firme. No controlas el reloj: pide un check-in cada cierto número de temas y recorta primero en lo firme.
15. **Banco de técnicas:** si tu primera explicación falla, no repitas lo mismo con más palabras. Prueba otra técnica: ejemplo numérico chico, pregunta guiada, contraejemplo o un visual. Recuerda cuál funcionó para qué tipo de concepto y úsala primero la próxima vez.
16. **Relación con lo anterior:** antes de presentar algo nuevo, dime qué es: un concepto nuevo, otra representación de algo ya visto, parte de algo anterior, estado posterior de algo anterior, resultado que sale de algo anterior, o algo parecido pero distinto (en ese caso, regla 5). Nunca lo presentes como independiente si no lo es.

### Después de explicar yo con mis palabras

Tras tu corrección y la nota de una línea, antes de avanzar dame **un caso nuevo**, distinto del ejemplo visto, para comprobar que sé aplicar y no solo explicar. Espera mi respuesta. No avances hasta que el concepto esté firme.

### Tablas de variables

Cuando un concepto tenga varias variables o notación relacionadas, usa **una sola tabla** con las columnas: `variable | qué significa | de dónde sale | ejemplo concreto | qué ocurre al inferir/calcular`. Nunca la separes en dos tablas.

### Apoyo visual y ritmo

- Si el concepto es espacial, secuencial o comparativo, ofrece un diagrama o visual sin que lo pida. Si es totalmente nuevo y cambia paso a paso, hazlo animado desde la primera explicación si tu entorno lo permite. Colores: ámbar = candidato o activo, azul = comparación, verde = fijo o resuelto, gris = neutral. El gráfico complementa el texto, no lo reemplaza.
- **Si digo "no entiendo" o "más simple":** no repitas la explicación con más palabras. Descarta el ejemplo y reconstruye desde cero así: 1) anuncia el corte y baja de nivel; 2) declara qué términos no usarás todavía; 3) cuenta un escenario cotidiano en primera persona, como escena corta con una idea por línea; 4) aísla el matiz exacto, con el formato `No dice X. Tampoco Y. Dice Z.` o `Opción A: posible. Opción B: descartada.`; 5) nombra el concepto técnico recién ahí; 6) ancla de memoria: "por ahora memoriza: ..."; 7) di qué no veremos todavía; 8) una verificación pegada a ese matiz. Si eso también falla, cambia de técnica (regla 15).
- **Ritmo:** si llevo más de cuarenta y cinco minutos forcejeando con un problema sin pedir ayuda, dame una pista pequeña y concreta. Al repasar algo olvidado, déjame reconstruirlo yo primero antes de mostrar la respuesta. Al cerrar un concepto con la verificación correcta, dame una línea de resumen para mi nota, nunca un diagrama.

### Temas técnicos específicos y código

- Sigue el orden de la regla 6. Al cierre del tema, agrega limitaciones y con qué otras técnicas compararlo, pero solo después de que cada concepto individual quedó firme.
- **Código:** bloque completo primero, explicado por partes después, nunca línea por línea mientras se construye. Prioriza eficiencia (vectorización o paralelismo cuando aplique).

### Forma de tus respuestas

- Mixto según el contenido: tabla para variables y comparaciones, prosa corta para ideas.
- Párrafos de máximo cinco líneas, sin relleno.
- Español latinoamericano neutro, natural para alguien de Perú. Sin modismos de España ("fijaos", "vosotros", "qué pasada").
- Tono directo, analítico y cercano. Feedback directo y objetivo, sin rodeos.
- Terminología exacta.

### Cierre de sesión

Al terminar, entrega: (1) las notas de una línea de cada concepto visto, (2) el bloque de estado de sesión (firmes / débiles / pendientes) para pegarlo la próxima vez, (3) en una frase, dónde retomar.

### Objetivo

Entender → aplicar → analizar → resolver, adaptando la forma sin diluir jamás el rigor técnico.


---

# PARTE C · Conocimiento del curso (Aprendizaje Supervisado)

Contiene 5 bloques, 29 temas de nivel 1 y 151 conceptos de nivel 2 (185 entradas). Para cada tema: **escenas** de apoyo (problema real y analogía; son apoyo pedagógico, no datos del curso), **Profundiza** (fórmulas, tablas de variables, ejemplos calculados y trampas) y una **ficha por concepto** con definición precisa, ejemplo o código, errores comunes, pregunta de comprobación y fuente exacta. Las cifras de los ejemplos de escena y de Profundiza son didácticas salvo que la ficha las atribuya al curso.

**Convenciones de fuente.** `02`, `03`, `04`, `05`, `06` = resúmenes consolidados del curso (tema 1 a tema 5: fundamentos, validación y métricas, extracción de características, regresión, clasificación). `PDF p.N` = página del manual del curso (cubre temas 1, 2, 4 y 5). `Diap. N` o `diapositiva N` = PowerPoint del profesor (tema 3). `notebook ...` = cuaderno Jupyter del curso. Estos originales no están en este archivo.

## Índice de videos

| Código | Tema | Conceptos de nivel 2 | Fuente principal |
|---|---|---:|---|
| 1.1 | Metodología CRISP-DM | 7 | resumen `02` |
| 1.2 | Tipos de aprendizaje (supervisado / no supervisado / otros) | 6 | resumen `02` |
| 1.3 | Estructura de datos: instancias, atributos y clase | 6 | resumen `02` |
| 1.4 | Limpieza de datos — introducción | 2 | resumen `02` |
| 1.5 | Normalización y estandarización | 4 | resumen `02` |
| 1.6 | Detección de outliers | 5 | resumen `02` |
| 1.7 | Imputación de valores ausentes | 4 | resumen `02` |
| 1.8 | Selección de atributos | 5 | resumen `02` |
| 2.1 | Introducción: entrenamiento, test, sobreajuste y subajuste | 5 | resumen `03` |
| 2.2 | Validación hold-out | 4 | resumen `03` |
| 2.3 | Validación cruzada / K-fold | 5 | resumen `03` |
| 2.4 | Ajuste de parámetros y validación anidada | 4 | resumen `03` |
| 2.5 | Evaluación en regresión: MAE, MSE, RMSE, MAPE | 5 | resumen `03` |
| 2.6 | Evaluación en clasificación: matriz de confusión, precisión, sensibilidad, F1, accuracy | 7 | resumen `03` |
| 3.1 | Conceptos básicos y variable estadística | 4 | PPTX del tema 3 y resumen `04` |
| 3.2 | Análisis de variables cualitativas | 2 | PPTX del tema 3 y resumen `04` |
| 3.3 | Análisis de variables cuantitativas | 4 | PPTX del tema 3 y resumen `04` |
| 3.4 | Introducción a los datos 2D (la imagen como dato) | 0 | PPTX del tema 3 y resumen `04` |
| 3.5 | Procesado de imagen: transformaciones de intensidad | 3 | PPTX del tema 3 y resumen `04` |
| 3.6 | Procesado de imagen: espacios de color y transformaciones geométricas | 4 | PPTX del tema 3 y resumen `04` |
| 3.7 | Segmentación de imágenes | 4 | PPTX del tema 3 y resumen `04` |
| 3.8 | Descriptores de forma (descriptores geométricos) | 3 | PPTX del tema 3 y resumen `04` |
| 3.9 | Descriptores de textura | 5 | PPTX del tema 3 y resumen `04` |
| 4.1 | Regresión lineal múltiple (OLS) | 10 | resumen `05` |
| 4.2 | Regresión polinómica | 3 | resumen `05` |
| 4.3 | Vecinos más cercanos (KNN) para regresión | 10 | resumen `05` |
| 5.1 | Regresión logística (LOGR) | 13 | resumen `06` |
| 5.2 | Árboles de decisión | 14 | resumen `06` |
| 5.3 | SVM — Support Vector Machines | 3 | resumen `06` |

El tema `3.4` no tiene conceptos de nivel 2: se explica como un solo segmento. Cada bloque (`1` a `5`) es solo un encabezado; el trabajo está en sus temas.


---

## BLOQUE 1 · Fundamentos y preparación de datos

**Pregunta principal:** ¿Qué queremos averiguar y con qué información?  
**Al terminar deberías poder:** Definir la tarea, reconocer qué datos se pueden usar y preparar los datos sin contaminar la evaluación.

> Bloque 1: método de trabajo (CRISP-DM), tipos de aprendizaje, estructura de una tabla de datos (instancias, atributos, clase) y cuatro técnicas de preparación: normalizar o estandarizar, detectar outliers, imputar ausentes y seleccionar atributos.

- **Ojo del bloque:** Toda transformación que aprende algo de los datos (mínimo, media, mediana de relleno, atributos elegidos) se aprende solo con entrenamiento.
- **Fuente exacta:** Archivo 02 (manual PDF p.6-31 + 3 notebooks).


### 1.1 · Metodología CRISP-DM  _(un video)_

#### Escena · Decide qué respuesta necesitas  _(cubre 1.1.a)_

Quieres ayudar a estudiantes que podrían reprobar. Antes de mirar datos, concreta la decisión: «a mitad del curso quiero saber quién necesita apoyo para ofrecerle tutoría». Esa frase dice **qué** quieres saber y **cuándo** debes saberlo.

Es como preparar una mochila: primero preguntas a dónde vas y cuánto durará el viaje. De lo contrario, puedes llenarla bien y aun así olvidar lo necesario. En un proyecto con datos, elegir un programa antes de fijar la decisión produce el mismo problema.

La nota final llega demasiado tarde para una alerta a mitad del curso. Una predicción solo ayuda si usa información disponible cuando todavía puedes actuar. Esta idea abre el proceso de trabajo descrito en el archivo `02`, sección 1.

**Compruébalo:** ¿por qué una predicción hecha al terminar el curso no sirve para decidir a mitad del curso a quién ofrecer apoyo?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

CRISP-DM; primera fase: comprensión del negocio (archivo `02`, sección 1).

**Significado preciso:** CRISP-DM es una forma de organizar un proyecto de datos. Su primera fase aclara el objetivo práctico antes de preparar datos o elegir un modelo.

#### Profundiza · ¿Qué problema resolvemos antes de elegir un algoritmo?

**Concepto (fuente del curso, Tema 1).** CRISP-DM organiza el trabajo en seis fases: comprensión del negocio, comprensión de los datos, preparación de los datos, modelado, evaluación y despliegue. Es un ciclo: un hallazgo en evaluación puede obligarte a redefinir la pregunta o volver a preparar los datos.

**Aplicación.** En el ejemplo, “necesitará apoyo durante el próximo mes” es la respuesta que queremos conocer. Los datos de entrada deben estar disponibles *antes* de ese mes. Si una columna contiene la calificación al terminarlo, usarla sería conocer parte de la respuesta por adelantado. Define además qué decisión tomarás con la predicción: ofrecer tutoría, por ejemplo. Eso determina qué error cuesta más.

**Análisis.** Un buen resultado estadístico no basta si el dato llega tarde, la predicción no cambia ninguna decisión o la población futura difiere de la histórica.

#### Fichas de conceptos del tema 1.1

##### 1.1 · Metodología CRISP-DM  (prioridad Alta)

- **Explicación sencilla:** Es el método más usado para llevar un proyecto de aprendizaje automático de principio a fin. Tiene 6 fases que se siguen en orden, pero se puede volver atrás y repetir pasos. Sirve para no improvisar y mantener el trabajo ordenado.
- **Definición precisa y fórmula:** CRISP-DM (Cross-Industry Standard Process for Data Mining): concebido a fines de 1996, proyecto europeo de 1997 codirigido por SPSS, Teradata, NCR, Daimler AG y Ohra; primera versión en 1999. Seis fases con dependencias secuenciales y cíclicas. Alternativas: KDD (1996, sin comprensión del negocio ni despliegue), SEMMA y ASUM-DM (IBM, 2015).
- **Ejemplo o código:** Fases: 1 comprensión del negocio, 2 comprensión de los datos, 3 preparación, 4 modelado, 5 evaluación de negocio, 6 despliegue; se puede volver atrás desde cualquiera.
- **Ojo (error común o límite):** No es una secuencia rígida: un hallazgo en la evaluación puede obligar a redefinir el objetivo o a preparar de nuevo los datos.
- **Comprueba:** ¿Por qué la evaluación de negocio (fase 5) no es lo mismo que medir la exactitud del modelo?
- **Fuente exacta:** 02 §1; PDF p.7-8.

###### 1.1.a · Fase 1: Comprensión del negocio  (prioridad Media)

- **Explicación sencilla:** Es el primer paso, y se retoma durante todo el proyecto: definir qué quiere lograr el negocio y cómo sabrán que salió bien, revisar la situación actual, traducir esas metas a tareas técnicas y armar un plan. Así se evita trabajar sin rumbo.
- **Definición precisa y fórmula:** Tareas: determinar objetivos de negocio y criterios de éxito (cualitativos o cuantitativos), evaluar la situación actual, determinar los objetivos de minería de datos (traducir metas de negocio a metas técnicas) y producir un plan de proyecto. Debe retomarse durante todo el proyecto.
- **Ejemplo o código:** Negocio: reducir la fuga de clientes. Meta técnica: predecir la baja del próximo mes con la información disponible al inicio de ese mes.
- **Ojo (error común o límite):** Sin criterio de éxito fijado antes, cualquier resultado se puede presentar como bueno.
- **Comprueba:** ¿Qué diferencia hay entre un objetivo de negocio y un objetivo de minería de datos?
- **Fuente exacta:** 02 §1; PDF p.10-15 (detalle de las fases).

###### 1.1.b · Fase 2: Comprensión de los datos  (prioridad Media)

- **Explicación sencilla:** Se reúnen los datos y se los revisa por primera vez: se describen, se resumen con números y gráficos de barras, y se busca si faltan datos o hay valores imposibles. Hacerlo bien ahorra tiempo en el resto del proyecto.
- **Definición precisa y fórmula:** Tareas: recolectar datos iniciales, describirlos (filas, columnas, significado, formato), explorarlos (estadística descriptiva, tablas de frecuencia, histogramas) y verificar su calidad (nulos, valores fuera de rango, consistencia). Reduce el tiempo total y aumenta las garantías de éxito.
- **Ejemplo o código:** Revisar con describe() y isna().sum() cuántos nulos y qué rangos tiene cada columna antes de modelar.
- **Ojo (error común o límite):** Saltarse esta fase suele costar más tiempo después, cuando el modelo falla por datos mal entendidos.
- **Comprueba:** ¿Qué dos hallazgos de esta fase cambiarían tu plan de preparación?
- **Fuente exacta:** 02 §1; PDF p.10-15 (detalle de las fases).

###### 1.1.c · Fase 3: Preparación de los datos  (prioridad Alta)

- **Explicación sencilla:** Es la fase más crítica: se eligen, limpian y arreglan los datos para que el modelo (el programa que aprende) pueda usarlos. Si un error pasa sin detectarse aquí, llega al modelo y arruina sus resultados.
- **Definición precisa y fórmula:** Seleccionar, limpiar y generar los conjuntos preparados para modelar. Tareas: seleccionar datos; limpiar (selección de columnas, reducción de filas, normalización, discretización, outliers, imputación); construir datos (p. ej. superficie = largo x ancho); integrar (fusionar tablas); formatear sin cambiar el contenido. Es la fase más crítica y la que más tiempo consume.
- **Ejemplo o código:** Crear la columna superficie = largo x ancho y rellenar las edades ausentes con la mediana de entrenamiento.
- **Ojo (error común o límite):** Los errores no detectados aquí se trasladan al modelado y son difíciles de rastrear.
- **Comprueba:** ¿Por qué un error de preparación es más peligroso que un error del algoritmo?
- **Fuente exacta:** 02 §1; PDF p.10-15 (detalle de las fases).

###### 1.1.d · Fase 4: Modelado  (prioridad Alta)

- **Explicación sencilla:** Es la fase central de la asignatura: se eligen los algoritmos (métodos de cálculo), se define cómo probarlos y con qué medidas, se construyen los modelos y se revisa técnicamente qué tan bien funcionan.
- **Definición precisa y fórmula:** Crear modelos de conocimiento (clasificación, regresión, etc.) con los datos preparados. Subtareas: seleccionar algoritmos (criterios: tipo de aprendizaje, compatibilidad con los datos, complejidad, interpretabilidad: caja blanca frente a caja negra), generar el plan de prueba (parámetros, métricas, forma de validar), construir los modelos y evaluar técnicamente (ranking de algoritmos).
- **Ejemplo o código:** Comparar regresión logística y un árbol con la misma validación cruzada y las mismas métricas.
- **Ojo (error común o límite):** Un modelo más complejo no siempre es mejor: se compara con la misma validación y se considera la interpretabilidad.
- **Comprueba:** ¿Qué ventaja tiene un modelo de caja blanca frente a uno de caja negra?
- **Fuente exacta:** 02 §1; PDF p.10-15 (detalle de las fases).

###### 1.1.e · Fase 5: Evaluación de negocio  (prioridad Media)

- **Explicación sencilla:** Se comprueba si los modelos cumplen lo que el negocio pidió al inicio como éxito. También se revisa cómo se trabajó y se decide si terminar, repetir pasos o iniciar nuevos proyectos. Así se confirma que el resultado sirve de verdad.
- **Definición precisa y fórmula:** Evaluar los modelos frente a los criterios de éxito de negocio definidos al inicio. Tareas: evaluar resultados, revisar el proceso (aseguramiento de calidad) y determinar los siguientes pasos (finalizar, iterar o abrir nuevos subproyectos).
- **Ejemplo o código:** Un modelo con buena exactitud puede no cumplir el criterio de negocio si no detecta los casos costosos.
- **Ojo (error común o límite):** Es una evaluación contra el objetivo del negocio, no solo contra una métrica técnica.
- **Comprueba:** ¿Qué tres decisiones puede tomar el equipo al cerrar esta fase?
- **Fuente exacta:** 02 §1; PDF p.10-15 (detalle de las fases).

###### 1.1.f · Fase 6: Despliegue  (prioridad Media)

- **Explicación sencilla:** Lo aprendido se convierte en acciones reales dentro del negocio: se planea cómo ponerlo en uso, se vigila y mantiene, se escribe un informe final y se revisa el proyecto. Sin este paso, el análisis queda sin utilidad práctica.
- **Definición precisa y fórmula:** Transformar el conocimiento obtenido en acciones dentro del proceso de negocio. Tareas: planear la implementación, monitorizar y mantener (detectar comportamientos anómalos), crear el informe final y revisar el proyecto (lecciones aprendidas).
- **Ejemplo o código:** Poner el modelo a puntuar cada noche y vigilar si su rendimiento cae con el tiempo.
- **Ojo (error común o límite):** Un modelo desplegado se degrada si cambian los datos: requiere monitorización.
- **Comprueba:** ¿Por qué hay que seguir vigilando un modelo después de desplegarlo?
- **Fuente exacta:** 02 §1; PDF p.10-15 (detalle de las fases).

###### 1.1.g · Roles en ciencia de datos  (prioridad Baja)

- **Explicación sencilla:** Un equipo que trabaja con datos suele tener cuatro roles: director técnico (data scientist chief), científico de datos (data scientist), analista de datos (data analyst) e ingeniero de datos (data engineer). Cada uno cumple una función distinta dentro del proyecto.
- **Definición precisa y fórmula:** Cuatro roles típicos: director técnico (data scientist chief: planifica, asigna recursos, valida), científico de datos (data scientist: analiza, diseña, experimenta, interpreta), analista de datos (data analyst: inteligencia de negocio, informes, cuadros de mando) e ingeniero de datos (data engineer: extrae, limpia, transforma, carga y automatiza). También hay ingenieros de software, administradores de BD y diseñadores gráficos.
- **Ejemplo o código:** El ingeniero de datos arma el flujo que carga las tablas; el científico de datos construye el modelo sobre ellas.
- **Ojo (error común o límite):** Es un complemento del manual (apartado 1.1.3): no forma parte de CRISP-DM en sí.
- **Comprueba:** ¿Qué rol se encarga de automatizar la carga y transformación de los datos?
- **Fuente exacta:** 02 §1; PDF p.9.


### 1.2 · Tipos de aprendizaje (supervisado / no supervisado / otros)  _(un video)_

#### Escena · Aprende de ejemplos con respuesta conocida  _(cubre 1.2)_

Supón que alguien te muestra frutas y te dice cuáles estaban maduras. Con suficientes ejemplos podrías reconocer pistas útiles. Si nadie te dice cuáles estaban maduras, todavía puedes agrupar frutas parecidas, pero no sabes qué grupo significa «madura».

Esa diferencia separa dos tipos de tarea. En una tienes ejemplos con la respuesta correcta y aprendes a predecirla. En la otra buscas grupos o patrones sin esa respuesta. El archivo `02`, sección 2, explica ambas formas de aprendizaje.

**Compruébalo:** ¿por qué agrupar frutas por aspecto no basta, por sí solo, para saber cuál grupo corresponde a las maduras?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Aprendizaje supervisado y aprendizaje no supervisado (archivo `02`, sección 2).

**Significado preciso:** Supervisado = aprende con casos cuya respuesta se conoce. No supervisado = busca patrones sin una respuesta etiquetada para cada caso.

#### Escena · Una cantidad o una categoría  _(cubre 1.2.a)_

Si preguntas «¿cuánto costará esta casa?», la respuesta puede ser una cantidad como ciento veinte mil. Si preguntas «¿se venderá este mes?», la respuesta pertenece a categorías como «sí» y «no».

El tipo de respuesta determina qué tarea estás resolviendo: predecir una cantidad o elegir una categoría. Una categoría puede estar escrita con números, como `0=no` y `1=sí`; esos números siguen siendo etiquetas, no convierten la tarea en predicción de una cantidad. El curso presenta esta distinción en el archivo `02`, sección 2.

**Compruébalo:** si `1` significa «sí» y `0` significa «no», ¿por qué predecir esa columna sigue siendo elegir una categoría?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Regresión y clasificación (archivo `02`, sección 2).

**Significado preciso:** Regresión = predecir una cantidad. Clasificación = predecir una categoría.

#### Fichas de conceptos del tema 1.2

##### 1.2 · Tipos de aprendizaje (supervisado / no supervisado / otros)  (prioridad Alta)

- **Explicación sencilla:** Hay dos grandes tipos de aprendizaje. Si los datos incluyen la respuesta que se quiere acertar, es supervisado: se usa para predecir. Si no la incluyen, es no supervisado. También existen variantes intermedias, como semisupervisado y por refuerzo.
- **Definición precisa y fórmula:** Dos categorías: problemas con variable de salida (supervisado) y sin ella (no supervisado). Otros tipos: semisupervisado y por refuerzo. Además existen tareas de apoyo como la reducción de dimensionalidad, la discretización o la selección de instancias y atributos.
- **Ejemplo o código:** Predecir el precio de una casa con ejemplos de precios conocidos es supervisado; agrupar clientes parecidos sin etiqueta es no supervisado.
- **Ojo (error común o límite):** Que una columna esté escrita con números no la convierte en regresión: los códigos 0 y 1 pueden ser clases.
- **Comprueba:** ¿Qué dato necesitas para que un problema sea supervisado?
- **Fuente exacta:** 02 §2; PDF p.15-17.

###### 1.2.a · Aprendizaje supervisado: regresión vs. clasificación  (prioridad Alta)

- **Explicación sencilla:** Aquí se calcula una respuesta a partir de los demás datos. Si la respuesta es un número, se llama regresión; si es una categoría o etiqueta, clasificación. Todas las filas necesitan tener su respuesta, porque de ahí aprende el modelo.
- **Definición precisa y fórmula:** Se estima el valor de la variable de salida a partir del resto de variables. Regresión: salida numérica (número real). Clasificación: salida categórica (etiqueta o número discreto). Es imprescindible que todas las filas tengan valor de salida; sin él, esa fila no aporta aprendizaje.
- **Ejemplo o código:** Precio de la vivienda: regresión. Especie de iris (setosa, versicolor, virginica): clasificación.
- **Ojo (error común o límite):** Una columna numérica puede ser una clase (0 y 1); y una entrada categórica puede usarse en regresión tras codificarla.
- **Comprueba:** Si la salida es la talla S, M o L, ¿es regresión o clasificación y por qué?
- **Fuente exacta:** 02 §2; PDF p.15-16.

###### 1.2.b · Aprendizaje no supervisado: clustering y reglas de asociación  (prioridad Media)

- **Explicación sencilla:** Sin respuesta que acertar, no se predice. El clustering (agrupamiento) junta datos parecidos. Las reglas de asociación dicen que si pasa algo (antecedente), suele pasar otra cosa (consecuente). Sirven, por ejemplo, para recomendar productos.
- **Definición precisa y fórmula:** Sin variable de salida no hay inferencia ni predicción. Clustering: crear grupos de datos similares. Reglas de asociación: reglas antecedente-consecuente que asocian variables, útiles para dependencias y recomendación.
- **Ejemplo o código:** Cesta de la compra: si compra pan y leche (antecedente), suele comprar mantequilla (consecuente).
- **Ojo (error común o límite):** Un grupo hallado por clustering no trae nombre: el significado lo pone la persona.
- **Comprueba:** ¿Por qué agrupar clientes por parecido no basta para saber qué grupo es el de los que se irán?
- **Fuente exacta:** 02 §2; PDF p.16.

###### 1.2.c · Reducción de dimensionalidad  (prioridad Media)

- **Explicación sencilla:** Consiste en achicar la cantidad de datos, quitando filas o columnas o transformando los valores, para que el trabajo sea más rápido sin perder calidad. Puede hacerse con o sin una respuesta conocida en los datos.
- **Definición precisa y fórmula:** Reduce el volumen de datos antes de modelar, eliminando filas o columnas o transformando el espacio de valores, para mantener o mejorar la eficacia y aumentar la eficiencia. Puede ser supervisada o no supervisada.
- **Ejemplo o código:** Seleccionar las 10 columnas más relacionadas con la clase antes de entrenar un KNN.
- **Ojo (error común o límite):** Reducir sin criterio puede perder justo la información útil.
- **Comprueba:** ¿Qué dos formas hay de reducir la dimensionalidad?
- **Fuente exacta:** 02 §2; PDF p.16.

###### 1.2.d · Aprendizaje semisupervisado  (prioridad Baja)

- **Explicación sencilla:** Los datos tienen una respuesta a acertar, pero solo en algunas filas. En lugar de borrar las filas que no la tienen, se usan modelos que aprovechan todos los datos disponibles, así no se desperdicia información.
- **Definición precisa y fórmula:** Hay variable de salida, pero no todas las filas tienen valor. En vez de eliminar las filas sin valor, se construyen modelos que aprovechan todas.
- **Ejemplo o código:** 1000 fotos, de las cuales solo 100 tienen su etiqueta confirmada.
- **Ojo (error común o límite):** Se diferencia del supervisado puro, que exige salida en todas las filas.
- **Comprueba:** ¿Qué problema evita el semisupervisado que el supervisado puro no resuelve?
- **Fuente exacta:** 02 §2; PDF p.16-17.

###### 1.2.e · Aprendizaje por refuerzo  (prioridad Baja)

- **Explicación sencilla:** El algoritmo no recibe la respuesta correcta exacta, sino una valoración de si lo que respondió estuvo bien o mal. Si acierta, se parece al supervisado; si falla, solo sabe que su respuesta no fue adecuada.
- **Definición precisa y fórmula:** El aprendiz recibe una valoración sobre la idoneidad de su respuesta. Con respuestas correctas se parece al supervisado; con errores solo se informa que fue inadecuada, a veces con una estimación del error, no el valor exacto de la respuesta correcta.
- **Ejemplo o código:** Un agente que aprende a jugar recibe puntos o castigos, no la jugada correcta.
- **Ojo (error común o límite):** En supervisado se puede calcular el error exacto; en refuerzo no necesariamente.
- **Comprueba:** ¿Qué recibe el aprendiz en refuerzo cuando se equivoca, a diferencia del supervisado?
- **Fuente exacta:** 02 §2; PDF p.17.

###### 1.2.f · Frontera de decisión / frontera bayesiana  (prioridad Media)

- **Explicación sencilla:** La frontera de decisión es la línea que separa un grupo de otro. En el caso ideal, si se conocen las reglas exactas de los datos, se calcula la mejor frontera. En la práctica solo hay una muestra, y la frontera estimada mejora cuantos más datos haya.
- **Definición precisa y fórmula:** Frontera de decisión: lugar donde el clasificador cambia de una clase a otra. Caso ideal: si se conocen las distribuciones de origen, la frontera óptima (bayesiana) se calcula analíticamente. Caso real: solo hay una muestra y la frontera se estima; mejora con más datos (el notebook compara 10, 100 y 10000 puntos).
- **Ejemplo o código:** Notebook: LogisticRegression (frontera lineal), RandomForestClassifier y SVC sobre los mismos datos 2D.
- **Ojo (error común o límite):** Todo algoritmo asume algo (normalidad, independencia, forma lineal o cuadrática de la frontera).
- **Comprueba:** ¿Por qué la frontera estimada con 10 puntos suele ser peor que con 10000?
- **Fuente exacta:** 02 §2 (complemento del notebook de terminología).


### 1.3 · Estructura de datos: instancias, atributos y clase  _(un video)_

#### Escena · Distingue el caso, las pistas y la respuesta  _(cubre 1.3.a, 1.3.b, 1.3.c)_

Piensa en una cesta de frutas. Cada fruta es un caso. Su color y firmeza son pistas que puedes observar. «Está madura» es la respuesta que quieres conocer.

En una tabla ocurre igual: cada fila es un caso; las columnas que conoces antes de decidir son pistas; otra columna contiene la respuesta en los casos pasados. El archivo `02`, sección 3, da nombres precisos a esos tres papeles. Ábrelos después de responder.

**Compruébalo:** si quieres saber si una fruta está madura usando color y firmeza, ¿por qué «madura» cumple un papel distinto del color?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Instancia, atributo y clase o variable objetivo (archivo `02`, sección 3).

**Significado preciso:** Instancia = un caso o fila. Atributo = una pista conocida. Variable objetivo o clase = la respuesta que se quiere predecir.

#### Profundiza · Instancia, atributo, objetivo y tipo de aprendizaje

**Concepto (fuente del curso, Tema 1).** Una *instancia* es un caso; los *atributos* describen el caso; la *clase* o variable objetivo es lo que se intenta predecir. En aprendizaje supervisado existen ejemplos con objetivo conocido. En el no supervisado se buscan estructuras sin esa etiqueta de respuesta. Si el objetivo es numérico continuo hablamos de **regresión**; si pertenece a categorías, de **clasificación**.

**Matiz.** “Numérico” no significa necesariamente regresión: los códigos `0` y `1` pueden representar categorías. Y una variable de entrada categórica puede usarse en un problema de regresión después de codificarla.

#### Fichas de conceptos del tema 1.3

##### 1.3 · Estructura de datos: instancias, atributos y clase  (prioridad Alta)

- **Explicación sencilla:** Los datos se organizan en una tabla: cada fila es una instancia (un caso) y cada columna es un atributo (un dato descriptivo). Además está la clase, que es la respuesta a predecir. Se anotan como X (atributos) e y (clase).
- **Definición precisa y fórmula:** La estructura fundamental es la tabla de datos (dataset): dos dimensiones, columnas de un solo tipo cada una. Cada celda es numérica (float) o categórica (cadena, booleano, entero). Nomenclatura: instancia = fila; atributo = columna de entrada; clase = salida; modelo = lo que extrae el algoritmo.
- **Ejemplo o código:** Iris: 150 instancias, 4 atributos numéricos (sepal-length, sepal-width, petal-length, petal-width), clase con 3 valores, 0 ausentes.
- **Ojo (error común o límite):** Existen otras estructuras (grafos, series temporales, secuencias, jerarquías) que el curso no desarrolla aquí.
- **Comprueba:** En una tabla de pacientes, ¿qué columna sería la clase y cuáles los atributos?
- **Fuente exacta:** 02 §3; PDF p.17-19.

###### 1.3.a · Instancia  (prioridad Alta)

- **Explicación sencilla:** Es cada fila de la tabla de datos, o sea un caso individual. También se le llama ejemplo, muestra, observación o punto. Por ejemplo, una persona o una flor dentro de la tabla.
- **Definición precisa y fórmula:** Instancia = cada fila de la tabla (también ejemplo, muestra, observación, punto o prototipo; en inglés instance, data point, sample).
- **Ejemplo o código:** Una flor concreta del dataset iris.
- **Ojo (error común o límite):** No es lo mismo que una característica: la instancia es la fila entera.
- **Comprueba:** Si la tabla tiene 150 filas, ¿cuántas instancias hay?
- **Fuente exacta:** 02 §3; PDF p.18.

###### 1.3.b · Atributo / característica  (prioridad Alta)

- **Explicación sencilla:** Es cada columna de la tabla, excepto la que tiene la respuesta. Describe una característica de cada caso. También se le llama característica, feature, variable de entrada o predictora.
- **Definición precisa y fórmula:** Atributo = cada columna excepto la clase (también característica, causa, variable de entrada, variable explicativa; attribute, feature, predictor). El notebook los usa indistintamente: 'atributo' y 'característica'.
- **Ejemplo o código:** sepal-length y petal-width en iris.
- **Ojo (error común o límite):** Un atributo medido después del resultado (por ejemplo la nota final) no sirve para predecir con antelación.
- **Comprueba:** ¿Por qué un atributo registrado después del resultado puede ser inútil en la práctica?
- **Fuente exacta:** 02 §3; PDF p.18.

###### 1.3.c · Clase / variable objetivo  (prioridad Alta)

- **Explicación sencilla:** Es la respuesta que se quiere predecir en el aprendizaje supervisado. También se llama etiqueta, target o respuesta. Es un número en regresión y una categoría en clasificación.
- **Definición precisa y fórmula:** Clase = variable de salida del aprendizaje supervisado (también etiqueta, variable objetivo, respuesta, efecto, consecuencia; class, target, response). Numérica en regresión (y_i real) y categórica en clasificación (dominio {c1,...,cm}).
- **Ejemplo o código:** La columna especie de iris, con dominio {setosa, versicolor, virginica}.
- **Ojo (error común o límite):** Una clase con códigos numéricos sigue siendo categórica.
- **Comprueba:** ¿Cuál es la clase si quieres predecir si un cliente comprará?
- **Fuente exacta:** 02 §3; PDF p.18.

###### 1.3.d · Notación formal X, y, eᵢ, xⱼ, xᵢⱼ  (prioridad Alta)

- **Explicación sencilla:** Es la forma de escribir la tabla con símbolos: X guarda todos los atributos de las n instancias (p atributos por instancia); y es la lista de respuestas; eᵢ es la fila i; xⱼ es la columna j; xᵢⱼ es el valor de la columna j en la fila i.
- **Definición precisa y fórmula:** La tabla tiene n instancias y p atributos. X = matriz de atributos; y = vector de clase; e_i = instancia (fila) i; x_j = atributo (columna) j; x_ij = valor del atributo j en la instancia i (i = 1..n, j = 1..p). En programación: X (matriz o DataFrame) e y (vector).
- **Ejemplo o código:** Con 150 filas y 4 columnas, X tiene forma (150, 4) e y tiene forma (150,).
- **Ojo (error común o límite):** No confundir x_ij (un valor) con x_j (toda la columna) ni con e_i (toda la fila).
- **Comprueba:** ¿Qué representa x_(3,2) en una tabla de pacientes?
- **Fuente exacta:** 02 §3; PDF p.18-19 (Tabla 1).

###### 1.3.e · Parámetros vs. hiperparámetros  (prioridad Media)

- **Explicación sencilla:** Los parámetros son valores del modelo que se ajustan solos mientras aprende. Los hiperparámetros son ajustes del método de aprendizaje que la persona fija antes de empezar y que no cambian durante el entrenamiento.
- **Definición precisa y fórmula:** Parámetros: pertenecen al modelo y se ajustan durante el entrenamiento. Hiperparámetros: pertenecen al algoritmo de aprendizaje, se fijan antes de entrenar y permanecen constantes durante él. Otros términos del notebook: datos de entrenamiento, datos de prueba (test) y métrica.
- **Ejemplo o código:** Parámetro: el coeficiente w1 de una regresión. Hiperparámetro: el número de vecinos k de un KNN.
- **Ojo (error común o límite):** Los hiperparámetros se eligen con validación, nunca mirando el test.
- **Comprueba:** ¿El número de vecinos k es un parámetro o un hiperparámetro?
- **Fuente exacta:** 02 §3 (complemento del notebook de terminología).

###### 1.3.f · Características de un conjunto de datos  (prioridad Baja)

- **Explicación sencilla:** Al empezar un proyecto se anota un resumen de los datos: cuántas filas y columnas hay, de qué tipo es cada columna y la respuesta, y cuántos valores faltan. Ejemplo, iris: 150 instancias, 4 atributos, 3 clases, 0 faltantes.
- **Definición precisa y fórmula:** Al inicio de un proyecto se anota: número de instancias, número de atributos, nombre, tipo y breve descripción de cada atributo, tipo y dominio de la clase, descripción de la clase y cantidad de valores ausentes.
- **Ejemplo o código:** Iris: 150 instancias, 4 atributos numéricos, clase categórica de 3 valores, 0 ausentes.
- **Ojo (error común o límite):** Una ficha incompleta oculta problemas (ausentes, tipos mal leídos) que aparecen tarde.
- **Comprueba:** ¿Qué cinco datos anotarías de una tabla nueva antes de modelar?
- **Fuente exacta:** 02 §3; PDF p.19.


### 1.4 · Limpieza de datos — introducción  _(un video)_

#### Fichas de conceptos del tema 1.4

##### 1.4 · Limpieza de datos — introducción  (prioridad Media)

- **Explicación sencilla:** Es una tarea clave dentro de la preparación de datos: quita defectos y ajusta los datos para que sus patrones se vean con la mayor claridad posible. Se hace antes de entrenar el modelo para que aprenda de datos limpios.
- **Definición precisa y fórmula:** Eliminación de defectos de los datos y adaptación para el modelado, dentro de la fase de preparación de CRISP-DM. Busca la forma de los datos que exponga sus patrones con más nitidez. El manual estudia: normalización y estandarización, outliers, imputación y selección de atributos; menciona sin desarrollar la discretización, la generación de atributos y la selección de instancias.
- **Ejemplo o código:** Pipeline típico: imputar, escalar y seleccionar atributos, siempre ajustado con entrenamiento.
- **Ojo (error común o límite):** La limpieza puede ser supervisada o no supervisada según use o no la clase.
- **Comprueba:** ¿Por qué se considera la limpieza parte de la preparación y no del modelado?
- **Fuente exacta:** 02 §4; PDF p.19-20.

###### 1.4.a · Técnicas de fila, columna o matriz completa  (prioridad Baja)

- **Explicación sencilla:** Las técnicas de limpieza se clasifican según la parte de la tabla que modifican: una fila, una columna (como la normalización, que cambia una columna entera) o la tabla completa.
- **Definición precisa y fórmula:** Según la parte de la tabla sobre la que actúan: técnicas de fila, de columna o de matriz completa. La normalización es una técnica de columna porque actúa sobre todos los valores de una columna a la vez.
- **Ejemplo o código:** Imputar actúa por columna; eliminar duplicados actúa sobre filas.
- **Ojo (error común o límite):** Es una clasificación de apoyo; no cambia cómo se calcula cada técnica.
- **Comprueba:** ¿La normalización es una técnica de fila, de columna o de matriz completa?
- **Fuente exacta:** 02 §4; PDF p.20.

###### 1.4.b · Limpieza supervisada vs. no supervisada  (prioridad Baja)

- **Explicación sencilla:** Igual que en el aprendizaje automático, algunas técnicas de limpieza necesitan que los datos incluyan la respuesta a predecir (la clase) y otras funcionan sin ella.
- **Definición precisa y fórmula:** Como en el aprendizaje automático, las técnicas de limpieza pueden ser supervisadas (usan la clase) o no supervisadas (no la usan).
- **Ejemplo o código:** Baja varianza: no supervisada. F-test: supervisada.
- **Ojo (error común o límite):** Una técnica supervisada que usa la clase de todo el conjunto antes de separar test provoca fuga de información.
- **Comprueba:** ¿Por qué una selección supervisada debe ajustarse solo con entrenamiento?
- **Fuente exacta:** 02 §4; PDF p.20.


### 1.5 · Normalización y estandarización  _(un video)_

#### Escena · Cambiar números a una escala común  _(cubre 1.5.a)_

**Problema real.** En una tabla, la edad se mide en decenas y el ingreso en miles. Si buscas casos «cercanos» comparando directamente esos números, el ingreso puede dominar solo por estar escrito en una escala mayor.

**Analogía cotidiana: la escala es lo difícil aquí.** Comparar una longitud escrita en metros con otra escrita en centímetros sin convertir las unidades puede engañarte. Cambiar la escala hace posible comparar; no vuelve importante una medida que antes no lo era.

Una forma de transformar una columna toma el menor valor observado como referencia baja y el mayor como referencia alta. Los valores intermedios quedan ubicados entre ambas referencias. El archivo `02`, sección 5, desarrolla la fórmula. Aprende las referencias solo con los casos de entrenamiento.

**Compruébalo:** ¿por qué cambiar la escala de una columna puede alterar qué casos parecen cercanos aunque los casos no hayan cambiado?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Normalización (*normalization*), según el archivo `02`, sección 5.

**Significado preciso:** transformación que usa los extremos observados en entrenamiento para situar cada valor en una escala relativa. Un caso futuro puede quedar fuera del intervalo inicial.

#### Escena · Medir cuánto se aleja un valor del promedio  _(cubre 1.5.b)_

**Problema real.** En otra columna, quieres saber si un valor está cerca o lejos de lo habitual, sin que importe su unidad original.

**Analogía cotidiana: aquí importa la distancia respecto a lo habitual.** Si en tu familia todos caminan casi la misma distancia diaria, un kilómetro extra puede ser llamativo. Si las distancias varían mucho, ese kilómetro extra puede ser normal.

La transformación resta el promedio de la columna y divide por una medida de cuánto suelen variar sus valores. Así, `0` significa «igual al promedio»; un valor positivo queda por encima y uno negativo por debajo. El archivo `02`, sección 5, muestra la fórmula. Aprende promedio y variación solo con entrenamiento.

**Compruébalo:** ¿por qué el mismo aumento de una unidad puede parecer grande en una columna que varía poco y pequeño en otra que varía mucho?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Estandarización (*standardization*) y puntuación `z`, según el archivo `02`, sección 5.

**Significado preciso:** a cada valor se le resta la media de entrenamiento y se le divide por su desviación estándar de entrenamiento.

#### Profundiza · Normalizar y estandarizar son transformaciones distintas

**Mapa de variables (fuente: archivo `02`, sección 5; ejemplo pedagógico).**

| variable | qué significa | de dónde sale | ejemplo concreto | qué ocurre al inferir/calcular |
|---|---|---|---|---|
| `x` | Valor original de un atributo | Fila observada | Edad `40` | Se transforma con reglas aprendidas en entrenamiento. |
| `min`, `max` | Extremos usados para normalizar | Solo entrenamiento | `20`, `60` | `x'=(x-min)/(max-min)`; `40` pasa a `0,5`. |
| `μ` | Media para estandarizar | Solo entrenamiento | `40` | Se resta a cada valor nuevo. |
| `σ` | Desviación estándar | Solo entrenamiento | `10` | `z=(x-μ)/σ`; `50` pasa a `1`. |
| `x'` | Valor normalizado | Fórmula con `x`, `min` y `max` | `0,5` para edad `40` | Es una escala nueva; con datos futuros puede quedar fuera de `[0,1]`. |

**Procedimiento.** En normalización `x'=(x-min)/(max-min)`; en estandarización `z=(x-μ)/σ`. Aprende los valores de referencia solo en entrenamiento. Un caso futuro menor que el mínimo observado puede normalizarse a un número negativo; no lo recortes automáticamente. Si `max=min` o `σ=0`, la fórmula exige un tratamiento especial.

#### Fichas de conceptos del tema 1.5

##### 1.5 · Normalización y estandarización  (prioridad Alta)

- **Explicación sencilla:** Son dos técnicas para poner los datos numéricos en una escala parecida. Se hace para que una columna con números muy grandes no pese más que otra igual de importante. Normalización: (x − mínimo)/(máximo − mínimo). Estandarización: (x − media)/desviación.
- **Definición precisa y fórmula:** Normalización: lleva cada atributo numérico a [0,1] con x_N = (x - min) / (max - min) (centrado y escalado por el rango). Estandarización: x_S = (x - media) / desviación típica (centrado en la media y escalado por la desviación). Se aplican columna por columna.
- **Ejemplo o código:** X_train = [[1,-1,2],[2,0,0],[0,1,-1]]; MinMaxScaler().fit_transform(X_train) da [[0.5,0,1],[1,0.5,0.333],[0,1,0]].
- **Ojo (error común o límite):** Ajusta (fit) con entrenamiento y aplica (transform) a test sin reajustar.
- **Comprueba:** ¿Qué problema evitan ambas técnicas cuando se usan distancias entre casos?
- **Fuente exacta:** 02 §5; PDF p.20-22.

###### 1.5.a · Normalización  (prioridad Alta)

- **Explicación sencilla:** Lleva los valores de una columna al rango de 0 a 1: se resta el menor valor y se divide por la diferencia entre el mayor y el menor. Se aplica columna por columna. Así todas quedan en la misma escala.
- **Definición precisa y fórmula:** x_N = (x - min(x_i)) / (max(x_i) - min(x_i)). Restar el mínimo = centrado; dividir por el rango = escalado. Para desnormalizar: x = x_N (max - min) + min. Es una homotecia aplicada a cada columna.
- **Ejemplo o código:** Un atributo con mínimo 0 y máximo 2: 0 pasa a 0, 1 pasa a 0,5 y 2 pasa a 1. Clase: preprocessing.MinMaxScaler.
- **Ojo (error común o límite):** Con datos futuros fuera del rango de entrenamiento el resultado puede salir de [0,1]; y si max = min la fórmula no está definida.
- **Comprueba:** Si el máximo de entrenamiento es 60 y llega un caso con 70, ¿cuánto vale su normalizado con mínimo 20?
- **Fuente exacta:** 02 §5; PDF p.20-21 (Programa 1).

###### 1.5.b · Estandarización  (prioridad Alta)

- **Explicación sencilla:** Ajusta una columna para que quede centrada en su promedio (media) y medida según cuánto se alejan los valores de él (desviación típica). A diferencia de la normalización, los valores no quedan limitados a un rango fijo.
- **Definición precisa y fórmula:** x_S = (x - media(x_i)) / desviación(x_i). El escalado cubre solo la amplitud de la desviación típica, por lo que los valores no quedan acotados a un rango fijo. Desestandarizar: x = x_S desv + media.
- **Ejemplo o código:** Primer atributo del ejemplo del PDF: media 1, desviación 0,8165; el valor 2 pasa a (2-1)/0,8165 = 1,22474. Clase: preprocessing.StandardScaler.
- **Ojo (error común o límite):** Si la desviación es cero la fórmula exige un tratamiento especial.
- **Comprueba:** Si un valor estandarizado es 0, ¿qué significa respecto a la media?
- **Fuente exacta:** 02 §5; PDF p.22 (Programa 2).

###### 1.5.c · Cuándo usar cada técnica  (prioridad Media)

- **Explicación sencilla:** Se usa normalización cuando el algoritmo no supone nada sobre cómo se reparten los valores. Se usa estandarización cuando el algoritmo sí supone que los datos siguen la forma de campana (distribución normal).
- **Definición precisa y fórmula:** Criterio práctico del notebook: normalización para algoritmos que no presuponen una distribución de los datos; estandarización cuando el algoritmo sí presupone normalidad. Ambas son muy recomendables si se usan distancias o productos escalares.
- **Ejemplo o código:** KNN (basado en distancias) suele necesitar estandarizar; un árbol de decisión es independiente de la escala.
- **Ojo (error común o límite):** Cambiar la escala no vuelve relevante un atributo que no lo era.
- **Comprueba:** ¿Qué técnica elegirías si el algoritmo supone datos con distribución normal?
- **Fuente exacta:** 02 §5 (notebook limpieza_datos_1).

###### 1.5.d · Evitar fuga de información (data leakage)  (prioridad Alta)

- **Explicación sencilla:** Al separar los datos en entrenamiento (train) y prueba (test), la transformación se calcula solo con los de entrenamiento y luego se aplica igual a los de prueba, sin recalcularla. Así la prueba no "espía" información que el modelo no debería conocer.
- **Definición precisa y fórmula:** Al dividir en train y test, el normalizador o estandarizador se ajusta (fit) solo con train y se aplica (transform) tal cual a test; nunca se reajusta con test. Así el test no influye en la preparación del modelo (fuga de información o data leakage).
- **Ejemplo o código:** f = normalizer.fit(X_train); X_train_n = f.transform(X_train); X_test_n = f.transform(X_test) (sin fit).
- **Ojo (error común o límite):** Calcular el mínimo y el máximo con toda la tabla antes de separar contamina el test.
- **Comprueba:** ¿Por qué calcular la media con todos los datos antes de separar el test deja de ser una prueba independiente?
- **Fuente exacta:** 02 §5 (notebook); 03 §0.


### 1.6 · Detección de outliers  _(un video)_

#### Escena · Un número raro merece una explicación antes de borrarlo  _(cubre 1.6)_

En una tabla de edades aparece `250`. Puede ser un error de escritura; también podría significar que la columna no contiene edades en años. Borrarlo de inmediato impide averiguar qué ocurrió.

Un valor muy distinto de los demás es una señal para investigar. Primero pregunta cómo se registró y qué representa. Después decide si corregirlo, conservarlo o excluirlo. El archivo `02`, sección 6, estudia estos valores extremos.

**Compruébalo:** ¿por qué encontrar un valor sorprendente no demuestra por sí solo que deba eliminarse?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Valor atípico o *outlier* (archivo `02`, sección 6).

**Significado preciso:** Outlier = observación muy alejada de las demás; puede ser error o un caso real.

#### Profundiza · Extremos

**Extremos.** La media y la desviación estándar son sensibles a ellos; la mediana suele resistir mejor. Eliminar automáticamente un extremo puede borrar justo el caso que necesitas detectar.

#### Fichas de conceptos del tema 1.6

##### 1.6 · Detección de outliers  (prioridad Alta)

- **Explicación sencilla:** Un outlier es un dato muy raro frente al resto, y puede confundir a los modelos y bajar su calidad. Esta etapa busca esos casos. No hay una línea exacta que separe lo raro de lo normal, así que el límite suele ser difuso.
- **Definición precisa y fórmula:** Un outlier es un valor fuera de la distribución natural de los datos que puede reducir la eficacia de los modelos. El umbral entre outlier y no-outlier no es trivial: la frontera suele ser difusa. El manual desarrolla un algoritmo (envolvente elíptica); el notebook añade el método de cajas y bigotes y otros detectores.
- **Ejemplo o código:** outliers.csv: 200 instancias, 2 atributos, 150 normales y 50 outliers, rango [-7, 7].
- **Ojo (error común o límite):** Un valor extremo puede ser un error o un caso real: investígalo antes de borrarlo.
- **Comprueba:** ¿Por qué encontrar un valor sorprendente no demuestra por sí solo que deba eliminarse?
- **Fuente exacta:** 02 §6; PDF p.23-26.

###### 1.6.a · Envolvente elíptica (EllipticEnvelope)  (prioridad Alta)

- **Explicación sencilla:** Supone que los datos se reparten como una campana: muchos en el centro y pocos lejos. Dibuja una elipse (óvalo) alrededor de los puntos normales. Mientras más grande es la elipse que hace falta para incluir un punto, más lejos está y más probable es que sea un outlier. Se usa con sklearn.covariance.EllipticEnvelope.
- **Definición precisa y fórmula:** EllipticEnvelope: supone distribución normal; crea superficies elípticas alrededor de los puntos normales; cuanto mayor la elipse que engloba un punto, mayor su distancia y su probabilidad de ser outlier. Los datos se centran y escalan con mediana e IQR.
- **Ejemplo o código:** EllipticEnvelope().fit(df); decision_function(df) puntúa la normalidad de cada instancia.
- **Ojo (error común o límite):** Si los datos no son normales puede haber falsos positivos y falsos negativos.
- **Comprueba:** ¿Qué supuesto sobre la distribución hace la envolvente elíptica?
- **Fuente exacta:** 02 §6; PDF p.24-26 (Programa 3).

###### 1.6.b · Mediana e IQR como base del cálculo  (prioridad Media)

- **Explicación sencilla:** El centro de las elipses se calcula con la mediana (el valor del medio) y el IQR (el ancho de la zona donde está la mitad central de los datos), no con el promedio. El motivo: los propios outliers deforman el promedio. IQR = P75 - P25; umbral típico: mediana ± 1,5·IQR o ± 3·IQR.
- **Definición precisa y fórmula:** Se usa la mediana en vez de la media porque la media se distorsiona con los propios outliers. IQR = P75 - P25. Todo valor que supere la mediana más o menos un umbral (típicamente 1,5 IQR, moderado, o 3 IQR, extremo) se considera outlier.
- **Ejemplo o código:** Q1 = scoreatpercentile(a, 25); Q3 = scoreatpercentile(a, 75); IQR = Q3 - Q1.
- **Ojo (error común o límite):** 1,5 IQR y 3 IQR son convenciones, no verdades: cambian cuántos puntos se marcan.
- **Comprueba:** ¿Por qué la mediana resiste mejor a los outliers que la media?
- **Fuente exacta:** 02 §6; PDF p.24.

###### 1.6.c · Umbral por percentil vs. contamination fijo  (prioridad Media)

- **Explicación sencilla:** Hay dos formas de decidir qué es raro con la misma herramienta. El PDF puntúa cada dato y corta en un percentil (25). El notebook fija de antemano que 25% de los datos serán outliers (contamination=0.25). Cambia solo cómo se pone el corte.
- **Definición precisa y fórmula:** Versión PDF: decision_function() puntúa la normalidad y scoreatpercentile(scores_pred, 25) fija el umbral en el percentil 25. Versión notebook: EllipticEnvelope(support_fraction=None, contamination=0.25, random_state=42) y predict() devuelve 1 (normal) o -1 (outlier). Es la misma clase con distinta forma de fijar el corte.
- **Ejemplo o código:** pos_outliers = np.where(predict(df) == -1)[0] da las posiciones de los outliers.
- **Ojo (error común o límite):** contamination fija de antemano la proporción esperada de outliers: si es incorrecta, el resultado también.
- **Comprueba:** ¿Qué proporción de outliers asume contamination=0.25?
- **Fuente exacta:** 02 §6 (PDF p.25-26 y notebook limpieza_datos_1).

###### 1.6.d · Método boxplot / cajas y bigotes  (prioridad Media)

- **Explicación sencilla:** Método solo del notebook, el de cajas y bigotes. Calcula dónde empieza y termina la mitad central de los datos (Q1, Q3, IQR) y marca como outlier todo lo que cae fuera de unos límites. Límite superior = P75+1.5·IQR; límite inferior = P25-1.5·IQR.
- **Definición precisa y fórmula:** Método solo del notebook: Q1 = P25, Q3 = P75, RIC = Q3 - Q1. Límite superior = Q3 + 1,5 RIC; límite inferior = Q1 - 1,5 RIC. Se marca outlier lo que cae fuera. Se dibuja con plt.boxplot.
- **Ejemplo o código:** pos_i = np.where(a < li)[0]; pos_s = np.where(a > ls)[0]; pos_outliers = np.concatenate((pos_i, pos_s)).
- **Ojo (error común o límite):** No está desarrollado en el PDF; solo el concepto de IQR coincide con la envolvente elíptica.
- **Comprueba:** ¿Con qué fórmula se obtiene el límite superior del boxplot?
- **Fuente exacta:** 02 §6 (solo notebook).

###### 1.6.e · Otros detectores de outliers  (prioridad Baja)

- **Explicación sencilla:** Existen otras herramientas de sklearn para encontrar datos raros: IsolationForest, LocalOutlierFactor y OneClassSVM. Se usan igual que la anterior: primero se ajustan a los datos (fit) y luego marcan cuáles son raros (predict).
- **Definición precisa y fórmula:** Otros detectores de sklearn con el mismo patrón fit y predict: IsolationForest, LocalOutlierFactor, OneClassSVM (se plantean como ejercicio de comparación).
- **Ejemplo o código:** IF = IsolationForest(); df_outliers, pos_outliers = find_outliers(df, IF).
- **Ojo (error común o límite):** El notebook solo los menciona; no se explica su fundamento.
- **Comprueba:** ¿Qué tienen en común los detectores de outliers de sklearn en cuanto a su uso?
- **Fuente exacta:** 02 §6 (notebook).


### 1.7 · Imputación de valores ausentes  _(un video)_

#### Escena · Rellenar un dato ausente también es aprender una regla  _(cubre 1.7, 1.5.d)_

En una lista faltan algunas edades. Decides sustituir cada espacio vacío por una edad «central» calculada a partir de edades conocidas. Esa edad central es una regla obtenida de los datos.

Por eso debes calcularla solo con los casos destinados a aprender. Si usas también los casos reservados para comprobar, ya dejaste que influyan en la preparación. El archivo `02`, sección 7, presenta la sustitución de ausencias; la conexión con la evaluación está en el archivo `03`.

**Compruébalo:** ¿por qué calcular la edad de reemplazo usando también los casos reservados contamina la comprobación?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Imputación de valores ausentes; fuga de información (*data leakage*) como advertencia metodológica.

**Significado preciso:** Imputación = sustituir un dato ausente según una regla. Fuga de información = dejar que datos reservados influyan en una regla que debería aprenderse solo con entrenamiento.

#### Profundiza · Separar antes de aprender reglas de preparación

**Idea (fuente: archivo `02`, secciones 4–8; conexión con archivo `03`, sección 0).** Primero se reserva la parte que evaluará el modelo. Después se aprende en el conjunto de entrenamiento cualquier regla que dependa de los datos, como la mediana para reemplazar ausencias. La misma regla se aplica a los casos reservados y a los futuros. Así, la evaluación sigue siendo una prueba con datos que no determinaron la preparación.

**Secuencia (apoyo pedagógico).**

```text
[gris: tabla completa] → [verde: entrenamiento] ── aprende la mediana ──┐
                      → [azul: evaluación]   ← aplica la misma mediana ──┘
```

#### Profundiza · Ausencias

**Idea (fuente: archivo `02`, secciones 6–8).** Imputar reemplaza un valor ausente siguiendo una regla; un valor extremo puede ser error o caso real; seleccionar atributos decide qué información entra al modelo. Son decisiones separadas. Investiga el significado de las ausencias y extremos antes de corregirlos. La mediana de imputación y cualquier selección guiada por la respuesta se aprenden solo dentro de entrenamiento.

#### Fichas de conceptos del tema 1.7

##### 1.7 · Imputación de valores ausentes  (prioridad Alta)

- **Explicación sencilla:** Cuando faltan datos (huecos o NaN), en vez de borrar los registros completos se rellenan con valores estimados. Así se evita perder la información que sí estaba en esos registros.
- **Definición precisa y fórmula:** Los conjuntos de datos suelen estar incompletos (valores ausentes o missing values; en Python np.nan). Muchos algoritmos de scikit-learn no toleran ausentes. Eliminar las instancias con algún ausente puede perder mucha información; por eso se imputa (se reemplaza por un valor estimado).
- **Ejemplo o código:** SimpleImputer(missing_values=np.nan, strategy='mean').
- **Ojo (error común o límite):** Calcula el valor de relleno solo con entrenamiento y aplica el mismo a test.
- **Comprueba:** ¿Por qué borrar todas las filas con ausentes puede ser una mala idea?
- **Fuente exacta:** 02 §7; PDF p.26-28.

###### 1.7.a · Valores ausentes (missing values)  (prioridad Media)

- **Explicación sencilla:** Son huecos en los datos: la información no se recogió, no estaba disponible, o era errónea y se borró. En Python se marcan con np.nan, que significa 'no es un número'.
- **Definición precisa y fórmula:** Valores ausentes: huecos porque la información no pudo recabarse, no estaba disponible o era errónea y se eliminó. Se representan como NaN, NA, N/A o Null; en Python con np.nan.
- **Ejemplo o código:** csv.isna().sum() cuenta los ausentes por columna del dataset penguins.
- **Ojo (error común o límite):** Un ausente puede significar cosas distintas (no aplica, no se midió, se perdió): averígualo antes de imputar.
- **Comprueba:** ¿Qué función cuenta los valores ausentes por columna en pandas?
- **Fuente exacta:** 02 §7; PDF p.26.

###### 1.7.b · Por qué no eliminar simplemente las filas  (prioridad Media)

- **Explicación sencilla:** La mayoría de los algoritmos de sklearn no funcionan si hay huecos. Pero borrar todos los registros con huecos puede hacer perder mucha información valiosa. Por eso se prefiere rellenar los huecos.
- **Definición precisa y fórmula:** La mayoría de los algoritmos de scikit-learn no admiten ausentes, y eliminar todas las instancias con algún ausente puede suponer una pérdida importante de información; por eso se prefiere reemplazarlos por valores concretos mediante técnicas de imputación.
- **Ejemplo o código:** Cálculo propio: con 5 % de ausentes al azar en 10 columnas independientes, cerca del 40 % de las filas (1 - 0,95 elevado a 10) tendría al menos un ausente y se perdería al borrarlas.
- **Ojo (error común o límite):** Imputar también introduce suposiciones: no es gratis.
- **Comprueba:** ¿Qué dos riesgos tiene eliminar las filas con ausentes?
- **Fuente exacta:** 02 §7; PDF p.26-27.

###### 1.7.c · Imputación por media, mediana o moda  (prioridad Alta)

- **Explicación sencilla:** Lo más simple es rellenar con un valor típico de esa columna: promedio o mediana si son números, o el valor más repetido (moda) si son categorías. Hay métodos más complejos que usan modelos. Se usa SimpleImputer(strategy='mean'/'median'/'most_frequent').
- **Definición precisa y fórmula:** Técnica más simple: sustituir por la media o la mediana (atributo numérico) o por la moda (categórico). Hay técnicas más complejas que plantean la imputación como un problema supervisado. En sklearn: SimpleImputer con strategy mean, median o most_frequent.
- **Ejemplo o código:** a = [[1,2],[nan,3],[7,6]]: medias por columna 4 y 3,6667; b = [[nan,10],[6,nan],[8,1]] queda [[4,10],[6,3.6667],[8,1]].
- **Ojo (error común o límite):** El ejemplo del PDF llama a transform sin mostrar el fit previo (posible omisión editorial del manual).
- **Comprueba:** ¿Qué estrategia usarías para un atributo categórico?
- **Fuente exacta:** 02 §7; PDF p.27 (Programa 4).

###### 1.7.d · Fit sobre train, transform sobre train y test  (prioridad Alta)

- **Explicación sencilla:** El rellenador aprende su valor típico (fit) solo con los datos de entrenamiento. Luego aplica ese mismo relleno (transform) a los datos de entrenamiento y a los de prueba, igual que se hace al normalizar o estandarizar.
- **Definición precisa y fórmula:** imputer.fit(X_train) aprende los valores de reemplazo solo con entrenamiento; imputer.transform(X_train) y imputer.transform(X_test) aplican esos mismos valores. Igual que con la normalización.
- **Ejemplo o código:** imputer = SimpleImputer(strategy='mean'); imputer.fit(X_train); X_test_ok = imputer.transform(X_test).
- **Ojo (error común o límite):** Si se calcula la media con el test incluido, el test influye en la preparación.
- **Comprueba:** ¿Con qué datos se calcula el valor que sustituye a los ausentes?
- **Fuente exacta:** 02 §7 (notebook datos_imputacion_seleccion).


### 1.8 · Selección de atributos  _(un video)_

#### Escena · Elegir pistas que estarán disponibles cuando decidas  _(cubre 1.8)_

**Problema real.** Para anticipar quién reprobará a mitad del curso, tienes asistencia, tareas entregadas y nota final. La nota final parece una pista excelente, pero todavía no existirá cuando debas tomar la decisión.

**Intuición (apoyo pedagógico).** Para decidir si llevar paraguas antes de salir, puedes mirar el cielo; no puedes usar como pista saber cómo terminó el paseo.

Elegir pistas consiste en conservar datos que ayudan a la tarea y que estarán disponibles a tiempo. Una pista medida después del resultado puede hacer que la evaluación parezca excelente y fallar en la práctica. El archivo `02`, sección 8, trata la elección de atributos.

**Compruébalo:** ¿por qué una pista muy relacionada con la respuesta puede ser inútil si solo aparece después de que debes decidir?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Selección de atributos (*feature selection*), según el archivo `02`, sección 8.

**Significado preciso:** proceso de escoger qué columnas de entrada usará el modelo; si se eligen según su relación con la respuesta, la elección se aprende solo con entrenamiento.

#### Profundiza · Elección de atributos

**Selección.** Una variable puede parecer predictiva porque revela indirectamente la respuesta o porque fue medida después del evento. Evalúa disponibilidad temporal y relación con el objetivo.

#### Fichas de conceptos del tema 1.8

##### 1.8 · Selección de atributos  (prioridad Media)

- **Explicación sencilla:** Es parte de reducir la cantidad de columnas de los datos. Se descartan las columnas poco útiles, usando un método que mide qué tan buena es cada una, ya sea sola (univariante) o junto con otras (multivariante).
- **Definición precisa y fórmula:** Subtarea de la reducción de dimensionalidad (dentro de la limpieza). Necesita un algoritmo de evaluación de atributos (individual o por conjuntos) y, si es multivariante, un algoritmo de búsqueda, porque el espacio de subconjuntos crece exponencialmente (problema NP-completo). Puede ser supervisada o no.
- **Ejemplo o código:** Baja varianza, F-test e información mutua del módulo sklearn.feature_selection.
- **Ojo (error común o límite):** Un atributo con poca relación individual con la clase puede ser importante en combinación con otros.
- **Comprueba:** ¿Por qué hace falta un algoritmo de búsqueda en la selección multivariante?
- **Fuente exacta:** 02 §8; PDF p.28-31.

###### 1.8.a · Evaluación univariante vs. multivariante  (prioridad Media)

- **Explicación sencilla:** Univariante mira cada columna por separado; multivariante mira grupos de columnas juntas. Una columna puede parecer poco útil sola, pero ser clave combinada con otras. Multivariante cuesta más cálculo, pero es más preciso.
- **Definición precisa y fórmula:** Evaluación individual (univariante): mide cada atributo por separado. Evaluación de conjuntos (multivariante): mide grupos de atributos a la vez; es más costosa pero suele elegir conjuntos más relevantes en su totalidad.
- **Ejemplo o código:** F-test e información mutua evalúan atributo por atributo (univariantes).
- **Ojo (error común o límite):** La relevancia de un atributo puede depender de otros.
- **Comprueba:** ¿Qué ventaja tiene evaluar conjuntos de atributos frente a evaluarlos uno a uno?
- **Fuente exacta:** 02 §8; PDF p.28.

###### 1.8.b · Selección supervisada vs. no supervisada  (prioridad Media)

- **Explicación sencilla:** En la supervisada, se mira cada columna junto con lo que se quiere predecir (la variable objetivo), que puede servir para clasificar, para predecir números, o ambos. En la no supervisada, cada columna se analiza sin tener en cuenta la clase.
- **Definición precisa y fórmula:** Selección supervisada: el atributo se analiza junto con la clase; el algoritmo de evaluación puede estar definido solo para clasificación, solo para regresión o para ambos (hay que comprobar la compatibilidad). No supervisada: se analiza el atributo sin considerar la clase.
- **Ejemplo o código:** F-test (supervisada, para regresión) frente a baja varianza (no supervisada).
- **Ojo (error común o límite):** Una técnica supervisada aprende de la clase: debe ajustarse solo con entrenamiento.
- **Comprueba:** ¿Qué técnica de las vistas es no supervisada?
- **Fuente exacta:** 02 §8; PDF p.28.

###### 1.8.c · Baja varianza (VarianceThreshold)  (prioridad Alta)

- **Explicación sencilla:** Método no supervisado: elimina las columnas cuyos valores casi no cambian, porque se asume que no ayudan a predecir. Se usa VarianceThreshold(threshold=...). La varianza mide cuánto varían los valores: S² = Σ(xi-x̄)²/(n-1).
- **Definición precisa y fórmula:** VarianceThreshold elimina atributos casi constantes: S² = suma (x_i - media)² / (n - 1); se descartan los de varianza menor que el umbral. Con datos binarios, threshold = 0,8 (1 - 0,8) = 0,16 corresponde a la varianza de Bernoulli para p = 0,8.
- **Ejemplo o código:** PDF: X = [[0,0,1],[0,1,0],[1,0,0],[0,1,1],[0,1,0],[0,1,1]]; el primer atributo vale 0 en 5 de 6 filas y se descarta. Notebook: iris con threshold = 0,6.
- **Ojo (error común o límite):** Es no supervisada: no mira si el atributo sirve para predecir la clase.
- **Comprueba:** ¿Por qué un atributo casi constante aporta poca información predictiva?
- **Fuente exacta:** 02 §8; PDF p.28-29 (Programa 5).

###### 1.8.d · F-test  (prioridad Alta)

- **Explicación sencilla:** Método supervisado que revisa una columna a la vez. Mide cuánto se relaciona una columna con la clase en línea recta (relación lineal), por eso sirve para detectar ese tipo de relación. Se usa con sklearn.feature_selection.f_regression.
- **Definición precisa y fórmula:** F-test: mide el grado de dependencia lineal entre dos atributos (aquí, atributo y clase). Clase sklearn: f_regression (módulo feature_selection).
- **Ejemplo o código:** Dataset sintético: y = x1 + sin(6 pi x2) + 0,1 ruido; el F-test da su máximo en x1 (dependencia lineal) y un valor bajo en x3 (irrelevante).
- **Ojo (error común o límite):** Solo detecta dependencia lineal: una relación sinusoidal casi no la ve.
- **Comprueba:** ¿Qué tipo de relación detecta el F-test?
- **Fuente exacta:** 02 §8; PDF p.29-31 (Programa 6).

###### 1.8.e · Información mutua  (prioridad Alta)

- **Explicación sencilla:** Método supervisado que revisa una columna a la vez. Detecta cualquier tipo de relación con la clase, sea en línea recta o no, pero necesita más ejemplos para ser confiable. Se usa con sklearn.feature_selection.mutual_info_regression.
- **Definición precisa y fórmula:** Información mutua: mide cualquier tipo de dependencia estadística, lineal o no, pero necesita más instancias para resultados fiables. Función sklearn: mutual_info_regression.
- **Ejemplo o código:** En el mismo dataset sintético, la información mutua da el valor máximo en x2 (dependencia sinusoidal) y valores cercanos a 0 en x3.
- **Ojo (error común o límite):** Con pocas instancias sus resultados son poco fiables.
- **Comprueba:** ¿Qué atributo del ejemplo sinusoidal detecta la información mutua y no el F-test?
- **Fuente exacta:** 02 §8; PDF p.29-31 (Programa 6).


---

## BLOQUE 2 · Validación de modelos y métricas de evaluación

**Pregunta principal:** ¿Cómo sabemos si funcionará con casos nuevos?  
**Al terminar deberías poder:** Estimar rendimiento en datos nuevos y elegir una métrica según el costo de los errores.

> Cómo estimar el rendimiento de un modelo con casos que no usó para aprender (hold-out, validación cruzada, bootstrap), cómo ajustar hiperparámetros sin tocar el test (validación anidada) y qué métricas usar en regresión (MAE, MSE, RMSE, MAPE) y en clasificación (matriz de confusión, exactitud, precisión, sensibilidad, F1).

- **Ojo del bloque:** A partir de este capítulo el curso se centra en predicción de una clase con cuatro algoritmos: regresión lineal múltiple, KNN, regresión logística y árboles.
- **Fuente exacta:** Archivo 03 (PDF p.32-52 + notebooks de métricas y validación).


### 2.1 · Introducción: entrenamiento, test, sobreajuste y subajuste  _(un video)_

#### Escena · Reserva casos para comprobar lo aprendido  _(cubre 2.1.a, 2.2)_

Imagina que practicas con un examen y luego te califican con exactamente las mismas preguntas. Una buena nota podría indicar que las memorizaste. Para saber si entendiste, necesitas preguntas nuevas.

Un *modelo* es la regla que se obtiene de los ejemplos. *Entrenar* significa aprender esa regla. Separa los casos pasados en dos partes antes de entrenar: una para aprender y otra para comprobar. Los casos reservados no deben participar en las reglas aprendidas. El archivo `03`, secciones 0–1, desarrolla esta separación.

```text
[gris: casos pasados] → [verde: aprender] + [azul: comprobar con casos reservados]
```

**Compruébalo:** ¿por qué medir el resultado con los mismos casos usados para aprender puede dar una impresión demasiado buena?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Conjunto de entrenamiento (*training set*) y conjunto de test (*test set*) (archivo `03`, sección 0).

**Significado preciso:** Entrenamiento = casos que enseñan la regla. Test = casos reservados para evaluarla al final.

#### Escena · Memorizar casos no es aprender una regla útil  _(cubre 2.1.b, 2.1.c)_

Alguien puede recordar de memoria todas las respuestas de un cuestionario y fallar cuando cambian las preguntas. Un modelo también puede funcionar muy bien con casos que ya vio y fallar con casos nuevos.

Para detectarlo, compara su error en los casos usados para aprender con su error en los reservados. Si el primero es bajo y el segundo alto, puede estar ajustándose demasiado a los detalles conocidos. Si ambos son altos, puede no estar captando una regla útil. El archivo `03`, sección 0, introduce estas situaciones.

**Compruébalo:** ¿por qué acertar los casos ya vistos no demuestra que el modelo acertará casos nuevos?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Sobreajuste (*overfitting*) y subajuste (*underfitting*) (archivo `03`, sección 0).

**Significado preciso:** Sobreajuste = el modelo se adapta demasiado a casos conocidos y falla en nuevos. Subajuste = la regla es insuficiente y falla incluso en los conocidos.

#### Profundiza · ¿Qué significa que un modelo generalice?

**Concepto (fuente del curso, Tema 2).** Entrenamiento ajusta el modelo; test estima el rendimiento en casos nuevos. *Sobreajuste*: error de entrenamiento bajo, error en datos nuevos alto. *Subajuste*: ambos errores altos porque el modelo es demasiado limitado o sus atributos no contienen suficiente señal.

**Matiz.** Una diferencia entre entrenamiento y test sugiere sobreajuste, pero revisa también cambios de población, errores de preparación y azar por muestra pequeña. Una única división no revela toda esa variación.

#### Fichas de conceptos del tema 2.1

##### 2.1 · Introducción: entrenamiento, test, sobreajuste y subajuste  (prioridad Alta)

- **Explicación sencilla:** Desde el capítulo 2 se estudian 4 algoritmos: regresión lineal, KNN, regresión logística y árboles. Los datos se dividen en una parte para aprender (entrenamiento) y otra para evaluar con ejemplos nunca vistos (test). Esa división es la base de toda validación.
- **Definición precisa y fórmula:** Conjunto de entrenamiento = datos con los que el algoritmo aprende su modelo. Conjunto de test = datos que el modelo no ha visto y con los que se mide la generalización; no debe contener instancias del entrenamiento. Objetivo: la complejidad que minimiza el error de generalización.
- **Ejemplo o código:** Un modelo que acierta 100 % lo ya visto y 60 % lo nuevo está sobreajustado.
- **Ojo (error común o límite):** Los dos errores (entrenamiento y generalización) deben mirarse juntos.
- **Comprueba:** ¿Qué dos errores compararías para detectar sobreajuste?
- **Fuente exacta:** 03 §0; PDF p.32-35.

###### 2.1.a · Conjunto de entrenamiento y conjunto de test  (prioridad Alta)

- **Explicación sencilla:** El entrenamiento son los datos con los que el algoritmo aprende. El test son datos que nunca vio y que se usan solo para evaluar. Así la nota es honesta, por eso el test no puede incluir ningún ejemplo del entrenamiento.
- **Definición precisa y fórmula:** Entrenamiento (training): datos que el algoritmo usa para aprender su modelo de conocimiento. Test: datos sobre los que el algoritmo predice sin haberlos visto en el entrenamiento; ninguna instancia de entrenamiento puede estar en el test.
- **Ejemplo o código:** X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0).
- **Ojo (error común o límite):** Los errores de entrenamiento son los cometidos al predecir los mismos ejemplos con que se entrenó; los de generalización, los del test.
- **Comprueba:** ¿Por qué el test no puede contener ninguna instancia del entrenamiento?
- **Fuente exacta:** 03 §0; PDF p.33; glosario PDF p.96.

###### 2.1.b · Sobreajuste (overfitting)  (prioridad Alta)

- **Explicación sencilla:** El modelo 'memoriza' los datos de entrenamiento en vez de aprender la idea general. Por eso casi no se equivoca con ellos, pero se equivoca mucho con datos nuevos (el error en test es alto).
- **Definición precisa y fórmula:** Sobreajuste (overfitting): el modelo aprende de memoria el entrenamiento; errores de entrenamiento muy bajos y errores de generalización altos. Se asocia a modelos de complejidad elevada.
- **Ejemplo o código:** Árbol sin límite de profundidad: acierta todo el entrenamiento y falla en datos nuevos.
- **Ojo (error común o límite):** Una diferencia entre entrenamiento y test sugiere sobreajuste, pero también puede deberse a azar o a un cambio de población.
- **Comprueba:** ¿Qué patrón de errores indica sobreajuste?
- **Fuente exacta:** 03 §0; PDF p.33-34; glosario PDF p.97.

###### 2.1.c · Subajuste (underfitting)  (prioridad Alta)

- **Explicación sencilla:** El modelo aprende una idea demasiado general y simple. Por eso se equivoca bastante tanto con los datos de entrenamiento como con los de test, y esos errores son parecidos entre sí.
- **Definición precisa y fórmula:** Subajuste (underfitting): el modelo aprende un concepto demasiado general o simple; errores de entrenamiento y de generalización altos y parecidos entre sí.
- **Ejemplo o código:** Ajustar una recta a datos claramente curvos.
- **Ojo (error común o límite):** Puede deberse a un modelo demasiado limitado o a atributos sin suficiente señal.
- **Comprueba:** ¿Cómo se ven los errores de entrenamiento y test en un modelo subajustado?
- **Fuente exacta:** 03 §0; PDF p.33-34; glosario PDF p.97.

###### 2.1.d · Compromiso sesgo-varianza (bias-variance tradeoff)  (prioridad Media)

- **Explicación sencilla:** Un modelo demasiado simple (sesgo alto) no logra ajustarse ni al entrenamiento: es el subajuste. Uno demasiado sensible (varianza alta) encaja muy bien el entrenamiento pero falla con datos nuevos: es el sobreajuste. La nota de entrenamiento siempre supera a la de validación. El mejor modelo tiene complejidad intermedia.
- **Definición precisa y fórmula:** Sesgo alto = subajuste (no ajusta ni el entrenamiento); varianza alta = sobreajuste (ajusta muy bien el entrenamiento y falla con datos nuevos). El puntaje de entrenamiento siempre supera al de validación; con complejidad muy baja ambos son malos, con muy alta el de validación cae, y existe un punto intermedio óptimo.
- **Ejemplo o código:** Curva de validación del polinomio: el equilibrio óptimo del notebook está en grado 3.
- **Ojo (error común o límite):** Más complejidad no es siempre mejor.
- **Comprueba:** ¿Qué ocurre con el puntaje de validación cuando la complejidad es demasiado alta?
- **Fuente exacta:** 03 §0 (notebook validacion_modelos, sección 1.3).

###### 2.1.e · Validación (definición general) y métricas base  (prioridad Media)

- **Explicación sencilla:** Validar es dividir los datos en entrenamiento y test para evaluar bien los algoritmos. Se presentan dos medidas base: MAE para predecir números (error promedio) y exactitud (accuracy) para categorías (porcentaje de aciertos). MAE = (1/n)·Σ|y_i - ŷ_i|; Exactitud(%) = 100·(1/n)·Σ[y_i = ŷ_i].
- **Definición precisa y fórmula:** Validación (validation o resampling): dividir los datos en subconjuntos de entrenamiento y test para evaluar bien los algoritmos. Métricas base: MAE = (1/n) suma abs(y_i - yhat_i) para regresión; Exactitud (%) = 100 (1/n) suma [y_i = yhat_i] para clasificación (el corchete vale 1 si coinciden y 0 si no).
- **Ejemplo o código:** Con y = [10,20,30] y predicciones [12,18,24]: MAE = (2+2+6)/3 = 3,33.
- **Ojo (error común o límite):** MAE y exactitud se detallan en 2.5 y 2.6.
- **Comprueba:** ¿Qué mide la exactitud y qué mide el MAE?
- **Fuente exacta:** 03 §0; PDF p.34-35.


### 2.2 · Validación hold-out  _(un video)_

#### Escena · Una sola división puede engañar por azar  _(cubre 2.2)_

Si pruebas un restaurante una sola vez, tal vez te tocó su mejor o peor día. Algo parecido ocurre al reservar una sola parte de los datos: la nota depende en parte de qué casos quedaron allí.

Una primera solución consiste en entrenar con una parte y evaluar con otra. Sirve como prueba, pero una sola nota no muestra cuánto variaría al cambiar la división. Esta es la idea de la separación simple del archivo `03`, sección 1.

**Compruébalo:** ¿por qué una única nota puede cambiar si reservas otros casos para la prueba?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Validación *hold-out* (archivo `03`, sección 1).

**Significado preciso:** Hold-out = reservar una parte de los casos para evaluar y aprender con el resto.

#### Profundiza · Una división para probar con casos nuevos

**Idea (fuente: archivo `03`, secciones 0–1).** Divide los datos antes de ajustar el modelo. Entrenamiento permite aprender sus parámetros. Si vas a comparar configuraciones, usa validación para elegirlas. Reserva test para la estimación final. Una configuración elegida antes de ajustar, como el número de vecinos, es un *hiperparámetro*; un coeficiente aprendido durante el ajuste es un *parámetro*.

```text
[gris: datos] → [verde: entrenamiento y elección] + [azul: test reservado]
```

#### Fichas de conceptos del tema 2.2

##### 2.2 · Validación hold-out  (prioridad Alta)

- **Explicación sencilla:** Consiste en separar los datos en dos partes, entrenamiento y test, una sola vez. Un reparto habitual es 66/34 o 70/30, es decir, más o menos dos tercios para aprender y el resto para evaluar.
- **Definición precisa y fórmula:** Hold-out: se divide el conjunto de datos una sola vez en entrenamiento y test. Reparto habitual 66 % y 34 %, o 70 % y 30 %.
- **Ejemplo o código:** Iris: 150 instancias, test_size=0.3 da 105 de entrenamiento y 45 de test.
- **Ojo (error común o límite):** Con un único test, su elección puede variar mucho las métricas (poca representatividad).
- **Comprueba:** ¿Por qué una sola división puede dar una nota engañosa?
- **Fuente exacta:** 03 §1; PDF p.35-38.

###### 2.2.a · Hold-out no aleatorio  (prioridad Media)

- **Explicación sencilla:** Se toma el primer porcentaje de las muestras, en su orden original, para entrenar y el resto para test. Sirve cuando el orden importa porque unas muestras dependen de otras, como en series temporales (datos medidos a lo largo del tiempo).
- **Definición precisa y fórmula:** Hold-out no aleatorio: el primer X % de las muestras (en su orden original) es entrenamiento y el resto es test. Útil cuando hay dependencias entre muestras, p. ej. series temporales.
- **Ejemplo o código:** Entrenar con los primeros 8 años y evaluar con los 2 últimos años de una serie.
- **Ojo (error común o límite):** Mezclar al azar una serie temporal haría que el entrenamiento viera el futuro del test.
- **Comprueba:** ¿Por qué en series temporales no se baraja antes de cortar?
- **Fuente exacta:** 03 §1; PDF p.35.

###### 2.2.b · Hold-out aleatorio  (prioridad Media)

- **Explicación sencilla:** Primero se mezclan las muestras al azar y luego se corta entre entrenamiento y test. Se recomienda cuando el orden de las muestras no importa, porque ninguna muestra depende de otra.
- **Definición precisa y fórmula:** Hold-out aleatorio: primero se reordenan aleatoriamente las muestras y luego se hace el corte. Recomendable si no hay dependencias de orden que respetar.
- **Ejemplo o código:** train_test_split baraja por defecto; con shuffle=False se conserva el orden.
- **Ojo (error común o límite):** Fija random_state para poder repetir el mismo reparto.
- **Comprueba:** ¿Cuándo es adecuado barajar antes de partir?
- **Fuente exacta:** 03 §1; PDF p.35-36.

###### 2.2.c · train_test_split (código real)  (prioridad Alta)

- **Explicación sencilla:** Es la función de sklearn que reparte los datos en entrenamiento y test. test_size indica qué proporción va a test, random_state fija la semilla del azar para repetir el mismo reparto, y shuffle=False mantiene el orden original. X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0).
- **Definición precisa y fórmula:** train_test_split(X, y, test_size, random_state) devuelve X_train, X_test, y_train, y_test. test_size = proporción de test; random_state = semilla de la reordenación previa; shuffle=False evita reordenar. Sin test_size, sklearn usa 0,25. DummyClassifier predice al azar según la frecuencia de clases; clf.score(X_test, y_test) devuelve la exactitud.
- **Ejemplo o código:** Programa 7: iris con DummyClassifier da Training 105, Test 45 y exactitud 0,3111 (tres clases balanceadas, azar cercano a 1/3).
- **Ojo (error común o límite):** Notebook de métricas: sus celdas de hold-out sobre California housing están vacías como ejercicio guiado.
- **Comprueba:** ¿Qué hace el parámetro random_state?
- **Fuente exacta:** 03 §1; PDF p.36-38 (Programa 7); notebook validacion_modelos celda 11.

###### 2.2.d · Partición train/test fijada por el problema  (prioridad Baja)

- **Explicación sencilla:** A veces el problema ya trae la división hecha, por ejemplo para comparar con resultados de otros trabajos. Esto también cuenta como una forma de hold-out, es decir, una sola división entre entrenamiento y test.
- **Definición precisa y fórmula:** La partición train y test puede venir fijada por el propio problema (para comparar con resultados de otros trabajos); también se considera una forma de hold-out.
- **Ejemplo o código:** Un concurso que publica los conjuntos de entrenamiento y de test ya separados.
- **Ojo (error común o límite):** Si el test viene dado, no se vuelve a repartir.
- **Comprueba:** ¿Por qué se respeta una partición fijada por el problema?
- **Fuente exacta:** 03 §1; PDF p.36.


### 2.3 · Validación cruzada / K-fold  _(un video)_

#### Escena · Repite la prueba cambiando la parte reservada  _(cubre 2.3, 2.3.a)_

Divide los casos en tres grupos. En la primera vuelta reservas el primero y aprendes con los otros dos. En la segunda reservas el segundo. En la tercera reservas el tercero. Obtienes tres notas y ves cuánto cambian.

```text
Vuelta 1: [azul: prueba] [verde: aprende] [verde: aprende]
Vuelta 2: [verde: aprende] [azul: prueba] [verde: aprende]
Vuelta 3: [verde: aprende] [verde: aprende] [azul: prueba]
```

El archivo `03`, sección 2, explica esta repetición. Cada vuelta construye un modelo nuevo; nadie ha probado el mismo modelo tres veces.

**Compruébalo:** ¿por qué cambiar el grupo reservado ayuda a descubrir si la primera nota fue excepcional?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Validación cruzada *k-fold* (*cross-validation*) (archivo `03`, sección 2).

**Significado preciso:** K-fold = dividir en k grupos, llamados pliegues, y repetir k veces dejando fuera un pliegue distinto. En el dibujo, k=3.

#### Escena · Repetir muestras permitiendo casos repetidos  _(cubre 2.3.e)_

**Problema real.** Tienes un conjunto de casos y quieres observar cuánto cambia una medida cuando reconstruyes muestras a partir de él.

**Intuición (apoyo pedagógico).** Metes nombres en una bolsa, sacas uno, lo anotas y lo devuelves antes de sacar el siguiente. Como vuelve a la bolsa, puede salir otra vez; otros nombres quizá no salgan nunca.

Repitiendo el procedimiento obtienes muestras distintas y ves cómo varía una medida. Esto no es la misma división en grupos sin repetición que vimos antes. El archivo `03`, sección 2-bis, muestra ejemplos de este muestreo.

**Compruébalo:** ¿por qué un caso puede aparecer varias veces en una misma muestra de este tipo?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Bootstrap o *bootstrapping*, según el archivo `03`, sección 2-bis.

**Significado preciso:** muestreo con reemplazo repetido a partir de los casos disponibles para estudiar la variación de una estimación.

#### Profundiza · Repetir la prueba con k-fold

**Idea (fuente: archivo `03`, sección 2).** Divide los datos en `k` partes. En cada vuelta deja una parte para evaluar y usa las otras para entrenar. Al terminar, resume las `k` notas. Cada caso sirve una vez como evaluación, aunque el modelo entrenado cambia en cada vuelta.

```text
Vuelta 1: [azul: evalúa] [verde: entrena] [verde: entrena]
Vuelta 2: [verde: entrena] [azul: evalúa] [verde: entrena]
Vuelta 3: [verde: entrena] [verde: entrena] [azul: evalúa]
```

#### Profundiza · Bootstrap para estudiar variabilidad

**Idea (fuente: archivo `03`, sección 2-bis).** En bootstrap se extraen casos *con reemplazo*: después de elegir un caso, puede volver a elegirse. Algunos se repiten y otros no entran en esa muestra. Repitiendo el proceso observas cómo varía una estimación. El notebook del curso incluye un ejemplo básico y otro repetido; no presupongas que utiliza automáticamente todos los casos no extraídos para evaluar un modelo.

#### Fichas de conceptos del tema 2.3

##### 2.3 · Validación cruzada / K-fold  (prioridad Alta)

- **Explicación sencilla:** Con una sola división, el resultado puede depender de la suerte del reparto. Para corregirlo, se parten los datos en K bolsas (folds) del mismo tamaño. Se repite la prueba K veces, y cada vez una bolsa distinta sirve de test.
- **Definición precisa y fórmula:** Validación cruzada (CV): se parte el conjunto en K subconjuntos de igual tamaño (bolsas o folds) y se hacen K validaciones tipo hold-out, usando cada bolsa una vez como test y el resto como entrenamiento. Se resumen las K notas (media y desviación). Recomendable repetirla varias veces si K < n, y K = 10 es un estándar práctico para datasets grandes.
- **Ejemplo o código:** Iris, K = 10: cada bolsa tiene 15 ejemplos.
- **Ojo (error común o límite):** Cada vuelta construye un modelo distinto: no es el mismo modelo evaluado K veces.
- **Comprueba:** ¿Por qué el resumen de K notas informa mejor que una sola?
- **Fuente exacta:** 03 §2; PDF p.38-41.

###### 2.3.a · K bolsas (folds)  (prioridad Alta)

- **Explicación sencilla:** Los datos se dividen en K bolsas de unos n/K ejemplos cada una. En cada una de las K vueltas, una bolsa distinta es el test y las demás son el entrenamiento. Ejemplo: 150 ejemplos (iris) con K=10 dan bolsas de 15 ejemplos.
- **Definición precisa y fórmula:** K bolsas de unos n/K ejemplos cada una; en cada una de las K vueltas una bolsa distinta es test y las demás entrenamiento. Si n no es divisible entre K, las bolsas no quedan iguales.
- **Ejemplo o código:** Programa 8: 10 elementos y KFold(n_splits=3): bolsas de test de 4, 3 y 3 elementos.
- **Ojo (error común o límite):** Cada ejemplo sirve como test exactamente una vez.
- **Comprueba:** ¿Por qué con 10 elementos y K = 3 la primera bolsa tiene 4 elementos?
- **Fuente exacta:** 03 §2; PDF p.38-40 (Programa 8).

###### 2.3.b · Leave-one-out  (prioridad Media)

- **Explicación sencilla:** Es una validación cruzada: se aparta un solo dato para probar y se entrena con todos los demás. Se repite hasta que cada dato haya sido la prueba una vez; con n datos son n entrenamientos, por eso sale caro con muchos datos.
- **Definición precisa y fórmula:** Leave-one-out: caso particular K = n; se predice cada ejemplo con todos los demás como entrenamiento. Ventaja: no hay aleatoriedad en las bolsas. Desventaja: coste alto (n entrenamientos y n predicciones frente a K entrenamientos y n predicciones); impracticable con millones de instancias.
- **Ejemplo o código:** Con 150 instancias hay 150 entrenamientos.
- **Ojo (error común o límite):** Con datasets muy grandes se usa K = 10 o similar.
- **Comprueba:** ¿Cuántos entrenamientos exige leave-one-out con n instancias?
- **Fuente exacta:** 03 §2; PDF p.40-41; glosario PDF p.98.

###### 2.3.c · Validación estratificada  (prioridad Media)

- **Explicación sencilla:** Al dividir los datos, cada categoría queda con casi la misma proporción en entrenamiento y en prueba. Así, si una categoría es rara, no desaparece de la prueba y la nota no sale sesgada.
- **Definición precisa y fórmula:** Validación estratificada: los conjuntos de test mantienen aproximadamente la misma distribución de clases que el de entrenamiento; evita el problema del desbalanceo de clases. El PDF solo la menciona (enlace externo).
- **Ejemplo o código:** Con 90 % de una clase y 10 % de otra, cada bolsa conserva esa proporción.
- **Ojo (error común o límite):** El curso no desarrolla su implementación.
- **Comprueba:** ¿Qué proporción conserva cada bolsa en una validación estratificada?
- **Fuente exacta:** 03 §2; PDF p.41; glosario PDF p.98.

###### 2.3.d · cross_val_score / KFold (código real)  (prioridad Alta)

- **Explicación sencilla:** Es la instrucción de la librería que prueba un modelo varias veces con distintos trozos de los datos. Devuelve un porcentaje de aciertos por cada trozo. Luego se resumen con el promedio y cuánto varían, para saber qué tan estable es el modelo.
- **Definición precisa y fórmula:** cross_val_score(clf, X, y, cv=KFold(n_splits=10)) devuelve un arreglo con K exactitudes (una por bolsa) que se resume con media y desviación. cross_val_predict devuelve un único vector con la predicción de cada ejemplo cuando su bolsa fue test.
- **Ejemplo o código:** Programa 9 (iris + DummyClassifier, K = 10): exactitud 0,307 con desviación 0,144.
- **Ojo (error común o límite):** Con KFold(shuffle=True) las bolsas son aleatorias.
- **Comprueba:** ¿Qué devuelve cross_val_score?
- **Fuente exacta:** 03 §2; PDF p.40-41 (Programa 9); notebook validacion_modelos celda 12.

###### 2.3.e · Bootstrapping / out-of-bag (OOB)  (prioridad Media)

- **Explicación sencilla:** Es otra forma de dividir los datos: se sacan ejemplos al azar, pudiendo repetirlos, para entrenar. Los que no salieron sirven de prueba y se llaman 'out of bag' (fuera de la bolsa). Así ningún ejemplo queda a la vez en entrenamiento y prueba.
- **Definición precisa y fórmula:** Bootstrapping (solo notebook): se fija un tamaño de muestra y se eligen instancias con reemplazo; una instancia puede repetirse en el entrenamiento. Las no elegidas son el test y se llaman out of bag (OOB). Nunca hay instancias repetidas entre entrenamiento y test.
- **Ejemplo o código:** resample(data, replace=True, n_samples=5, random_state=3); oob = [x for x in data if x not in boot]. Repetido 40 veces con ElasticNet da una distribución del MAE.
- **Ojo (error común o límite):** No es lo mismo que la partición en bolsas sin repetición de K-fold.
- **Comprueba:** ¿Por qué un caso puede aparecer dos veces en una muestra bootstrap?
- **Fuente exacta:** 03 §2-bis (notebook validacion_modelos, sección 1.2).


### 2.4 · Ajuste de parámetros y validación anidada  _(un video)_

#### Escena · Elegir la mejor configuración también puede engañar  _(cubre 2.4)_

Supón que pruebas diez maneras de preparar un plato y anuncias como calidad habitual la nota de la mejor. Esa nota fue precisamente la que usaste para elegir: puede ser demasiado optimista.

En modelos ocurre igual cuando comparas configuraciones, como cuántos casos parecidos consultar. Usa unas pruebas para elegir la configuración y otra prueba separada para estimar qué tan bien funciona **todo el proceso, incluida esa elección**. El archivo `03`, sección 3, describe esta separación en dos niveles.

**Compruébalo:** ¿por qué la prueba usada para elegir la mejor configuración no debería ser también la nota final que anuncias?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Ajuste de hiperparámetros y validación anidada (*nested cross-validation*) (archivo `03`, sección 3).

**Significado preciso:** Hiperparámetro = ajuste que se elige antes de aprender la regla. Validación anidada = una ronda interna para elegirlo y otra externa para evaluar el proceso completo.

#### Profundiza · Elegir configuraciones y estimar rendimiento por separado

**Idea (fuente: archivo `03`, sección 3).** En validación anidada, el ciclo interno compara configuraciones usando solo el entrenamiento del ciclo externo. El ciclo externo reserva casos para estimar el rendimiento de *todo el procedimiento de elección*. Toda transformación aprendida de los datos también se ajusta dentro de cada entrenamiento interno. Al terminar la evaluación, se puede volver a ajustar la búsqueda con todos los datos destinados al desarrollo para obtener el modelo que se usará.

```text
Exterior: [verde: datos para elegir] [azul: evaluación exterior]
Interior: [verde: ajuste] [ámbar: comparación de configuraciones]
```

#### Fichas de conceptos del tema 2.4

##### 2.4 · Ajuste de parámetros y validación anidada  (prioridad Alta)

- **Explicación sencilla:** Los algoritmos tienen ajustes que elige la persona antes de entrenar (como perillas). Aquí se busca la mejor combinación sin usar nunca los datos de prueba. Así esos datos siguen mostrando cómo funcionará el modelo con casos nuevos.
- **Definición precisa y fórmula:** Los algoritmos tienen parámetros de configuración (hiperparámetros) que afectan la bondad; encontrar su elección óptima es el ajuste de parámetros (hyperparameter tuning), una búsqueda que maximiza una métrica (exactitud, MAE...). Regla: nunca se ajusta maximizando la bondad sobre el test.
- **Ejemplo o código:** Elegir el número de vecinos k comparando varias configuraciones con validación interna.
- **Ojo (error común o límite):** El PDF no incluye código de este apartado.
- **Comprueba:** ¿Por qué el test debe permanecer aislado durante el ajuste?
- **Fuente exacta:** 03 §3; PDF p.42-44.

###### 2.4.a · Regla: el test nunca se usa para ajustar parámetros  (prioridad Alta)

- **Explicación sencilla:** No se deben ajustar los parámetros buscando el mejor resultado en los datos de prueba. Esos datos deben quedar aislados todo el tiempo. Si no, el modelo se adapta a ellos y su resultado parece mejor de lo que realmente es.
- **Definición precisa y fórmula:** El ajuste de parámetros no debe hacerse maximizando la bondad sobre el conjunto de test: el test debe permanecer aislado durante todo el entrenamiento y el ajuste, para evitar el sobreajuste y evaluar la capacidad de generalización.
- **Ejemplo o código:** Si eliges la configuración que mejor puntúa en el test, ese test deja de ser una prueba independiente.
- **Ojo (error común o límite):** La mejor nota entre muchas configuraciones tiende a ser optimista.
- **Comprueba:** ¿Por qué elegir la mejor configuración según el test lo contamina?
- **Fuente exacta:** 03 §3; PDF p.43.

###### 2.4.b · Test de validación (validation test)  (prioridad Alta)

- **Explicación sencilla:** Es un grupo de datos apartado del propio entrenamiento, usado para comparar distintas configuraciones del modelo sin tocar la prueba real. Así el modelo final se evalúa una sola vez con la prueba independiente, y el resultado es honesto.
- **Definición precisa y fórmula:** Test de validación: conjunto extraído del entrenamiento. Cada configuración se entrena con el entrenamiento y se prueba con el test de validación; tras hallar la mejor configuración, el modelo final se evalúa una sola vez con el test independiente.
- **Ejemplo o código:** Separar 20 % del entrenamiento como validación para comparar profundidades de árbol.
- **Ojo (error común o límite):** Un único test de validación también puede sobreajustarse a sus peculiaridades.
- **Comprueba:** ¿Con qué datos se evalúa el modelo final?
- **Fuente exacta:** 03 §3; PDF p.43.

###### 2.4.c · Validación anidada (nested validation)  (prioridad Alta)

- **Explicación sencilla:** Usa dos niveles de prueba. Afuera, la división original entre entrenamiento y prueba. Adentro, varias pruebas dentro del entrenamiento para elegir los mejores ajustes. Luego se reentrena con todo el entrenamiento y se evalúa una sola vez con la prueba independiente.
- **Definición precisa y fórmula:** Validación anidada (nested o double validation): dos niveles. Externa: la partición original en entrenamiento y test. Interna: validación cruzada dentro del entrenamiento para ajustar parámetros, buscando el promedio máximo de bondad en los tests internos. Luego se reentrena con todo el entrenamiento con los parámetros óptimos y se evalúa en el test independiente.
- **Ejemplo o código:** Exterior: entrenamiento y test; interior: 5-fold sobre el entrenamiento para elegir la profundidad.
- **Ojo (error común o límite):** Toda transformación aprendida de los datos se ajusta dentro de cada entrenamiento interno.
- **Comprueba:** ¿Qué parte de los datos no participa nunca en la elección de parámetros?
- **Fuente exacta:** 03 §3; PDF p.44.

###### 2.4.d · Curvas de validación y de aprendizaje  (prioridad Media)

- **Explicación sencilla:** Son dos gráficos que comparan el desempeño en entrenamiento y en validación (datos apartados para comprobar). Uno cambia un ajuste del modelo, como el grado de un polinomio. El otro cambia la cantidad de datos de entrenamiento, con el ajuste fijo.
- **Definición precisa y fórmula:** Curva de validación (validation_curve): puntaje de entrenamiento y de validación al variar un hiperparámetro (p. ej. grado 0 a 20 con cv=7). Curva de aprendizaje (learning_curve): lo mismo al variar el tamaño del entrenamiento con el hiperparámetro fijo.
- **Ejemplo o código:** El notebook concluye que el equilibrio óptimo del polinomio está en grado 3.
- **Ojo (error común o límite):** Son gráficos de diagnóstico, no un método de ajuste automático.
- **Comprueba:** ¿Qué se varía en una curva de validación y qué en una curva de aprendizaje?
- **Fuente exacta:** 03 §3 (notebook validacion_modelos, celdas 40-49).


### 2.5 · Evaluación en regresión: MAE, MSE, RMSE, MAPE  _(un video)_

#### Escena · El error de una cantidad puede medirse de varias maneras  _(cubre 2.5.a a 2.5.d)_

**Problema real.** Predices cuánto se venderá y necesitas juzgar tus errores. Algunas equivocaciones son pequeñas y otras podrían ser muy costosas.

**Mapa de nombres.** Estas medidas se parecen y conviene verlas juntas primero. Todas comparan cantidades reales con cantidades predichas. Usaremos tres ventas reales `[100, 120, 80]` y predicciones `[90, 125, 85]`.

| variable | qué significa | de dónde sale | ejemplo concreto | qué ocurre al inferir/calcular |
|---|---|---|---|---|
| `MAE` | Error absoluto promedio | Diferencias entre ventas reales y predichas | `(10+5+5)/3≈6,67` | Trata linealmente cada tamaño de error. |
| `MSE` | Promedio de errores al cuadrado | Las mismas diferencias, elevadas al cuadrado | `(100+25+25)/3=50` | Un error grande pesa mucho más. |
| `RMSE` | Raíz del MSE | MSE ya calculado | `√50≈7,07` | Vuelve a la unidad original y conserva la sensibilidad a errores grandes. |
| `MAPE` | Error porcentual promedio | Cada error dividido por su venta real | `≈6,81 %` para las tres ventas | Compara errores relativos; un valor real cero exige otra regla. |
| `R²` | Comparación con predecir siempre la media de ventas reales | Los mismos tres pares de valores | `0,8125` | En este conjunto, el modelo supera a predecir siempre `100`. |

Imagina que encargas cien panes y llegan noventa. Faltan diez: ese es el tamaño del error de la primera venta del ejemplo. Si un error aislado fuera muy grande, podrías querer una medida que lo castigue especialmente. Por ejemplo, errores `[10,10]` y `[0,20]` tienen el mismo MAE (`10`), pero el segundo par tiene RMSE mayor (`≈14,14` frente a `10`).

Las fórmulas y un cálculo completo están en «Profundiza» de este tema. El archivo `03`, sección 4, contiene MAE, MSE, RMSE y MAPE. La fórmula de R² está en el archivo `05`, sección 1. El MAPE directo falla cuando la cantidad real es cero; el notebook usa una variante que evita dividir directamente entre cero.

**Compruébalo:** ¿por qué los pares de errores `[10,10]` y `[0,20]` tienen el mismo MAE y distinto RMSE?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

MAE, MSE, RMSE, MAPE y coeficiente de determinación R² (archivos `03`, sección 4; `05`, sección 1).

**Significado preciso:** MAE promedia tamaños de errores; MSE promedia sus cuadrados; RMSE saca raíz a MSE; MAPE los expresa respecto al valor real; R² compara con predecir siempre la media real.

#### Profundiza · Métricas de regresión: cada una responde una pregunta distinta

**Mapa de variables.** La notación de MAE, MSE, RMSE y MAPE procede del archivo `03`, sección 4. La fórmula de R² está en el archivo `05`, sección 1. Todos los números de la tabla son un ejemplo pedagógico único.

| variable | qué significa | de dónde sale | ejemplo concreto | qué ocurre al inferir/calcular |
|---|---|---|---|---|
| `y_i` | Valor real del caso `i` | Dato etiquetado | Primer caso: `10` | Es la referencia para evaluar; no se conoce al predecir un caso futuro. |
| `ŷ_i` | Predicción para el caso `i` | Modelo | Primer caso: `12` | Se compara con `y_i`. |
| `e_i` | Error `y_i-ŷ_i` | Resta de real y predicho | Primer caso: `−2` | El signo muestra dirección; no lo promedies sin valor absoluto o cuadrado. |
| `n` | Número de casos evaluados | Conjunto de evaluación | `3` | Divide las sumas para obtener promedios. |
| `ȳ` | Media de los valores reales | `y=[10,20,30]` | `20` | Es la predicción de referencia para R². |
| `SSE` | Suma de errores cuadrados del modelo | `Σe_i²` | `44` | Es el numerador de la fracción de R². |
| `SST` | Suma de errores cuadrados de predecir `ȳ` | `Σ(y_i-ȳ)²` | `200` | Es el denominador de esa fracción. |

**Fórmulas.** `MAE = promedio(|e_i|)` mide error absoluto típico en unidades de `y`. `MSE = promedio(e_i²)` castiga más los errores grandes y queda en unidades cuadradas. `RMSE = √MSE` recupera las unidades originales. `MAPE = promedio(|e_i/y_i|) × 100 %` expresa error relativo. Si `y_i=0`, el cociente directo no está definido; el notebook del Tema 2 usa una variante con `max(ε, |y_i|)` en el denominador. `R² = 1 - SSE/SST` compara con predecir siempre `ȳ`; puede ser negativo si el modelo es peor que esa referencia. Si `SST=0`, esta fórmula requiere tratamiento especial.

**Ejemplo calculado.** Valores reales `[10, 20, 30]`; predicciones `[12, 18, 24]`. Errores `[-2, 2, 6]`. `MAE=(2+2+6)/3=3,33`; `MSE=(4+4+36)/3=14,67`; `RMSE≈3,83`. La media real es `20`, así que `SST=100+0+100=200`, `SSE=44` y `R²=1-44/200=0,78`. Para MAPE, las proporciones son `2/10`, `2/20` y `6/30`: `16,67 %` de promedio.

**Trampa frecuente.** `RMSE` no es la media de los errores absolutos; la raíz se aplica *después* de promediar los cuadrados. Cambiar el orden cambia el número.

#### Fichas de conceptos del tema 2.5

##### 2.5 · Evaluación en regresión: MAE, MSE, RMSE, MAPE  (prioridad Alta)

- **Explicación sencilla:** Son formas de medir qué tan lejos quedan las predicciones numéricas de los valores reales. MAE y RMSE se expresan en la misma unidad de lo que se predice. MAPE lo expresa en porcentaje, es decir, relativo al valor real.
- **Definición precisa y fórmula:** Métricas absolutas (misma unidad que la clase): MAE y RMSE. Métrica relativa: MAPE (porcentaje). MSE aparece en el notebook como RMSE al cuadrado. Las métricas de error actúan como función de coste: entrenar es hallar parámetros que la minimicen.
- **Ejemplo o código:** Reales [10,20,30], predicciones [12,18,24], errores [-2,2,6]: MAE 3,33; MSE 14,67; RMSE 3,83; MAPE 16,67 %.
- **Ojo (error común o límite):** R2 no se define en este capítulo del curso: aparece en el archivo 05 (regresión lineal).
- **Comprueba:** ¿Qué métrica penaliza más un error aislado muy grande?
- **Fuente exacta:** 03 §4; PDF p.44-47.

###### 2.5.a · MAE (error absoluto medio)  (prioridad Alta)

- **Explicación sencilla:** Es el promedio de cuánto se equivoca el modelo, sin importar si se pasa o se queda corto. Se expresa en la misma unidad de lo que se predice, por lo que es fácil de interpretar.
- **Definición precisa y fórmula:** MAE = (1/n) suma abs(y_i - yhat_i). Métrica absoluta: se expresa en la unidad de la clase.
- **Ejemplo o código:** Errores [-2, 2, 6]: MAE = (2+2+6)/3 = 3,33.
- **Ojo (error común o límite):** Trata cada error proporcionalmente a su tamaño.
- **Comprueba:** Dos pares de errores [10,10] y [0,20], ¿tienen el mismo MAE?
- **Fuente exacta:** 03 §0 y §4; PDF p.34-35.

###### 2.5.b · MSE (error cuadrático medio)  (prioridad Media)

- **Explicación sencilla:** Se calcula el error de cada predicción, se eleva al cuadrado y se promedia. Es lo mismo que el RMSE antes de sacar la raíz. Sirve para medir qué tan lejos quedan las predicciones de los valores reales.
- **Definición precisa y fórmula:** MSE = (1/m) suma (yhat_i - y_i)^2 (notebook). Es el RMSE sin la raíz; unidades al cuadrado.
- **Ejemplo o código:** Errores [-2, 2, 6]: MSE = (4+4+36)/3 = 14,67.
- **Ojo (error común o límite):** Un error grande pesa mucho más por el cuadrado.
- **Comprueba:** ¿Qué relación hay entre MSE y RMSE?
- **Fuente exacta:** 03 §4 (notebook métricas, sección 1.1).

###### 2.5.c · RMSE (raíz del error cuadrático medio)  (prioridad Alta)

- **Explicación sencilla:** Es parecido al MAE, pero cada error se eleva al cuadrado antes de promediar y al final se saca la raíz. Por eso los errores grandes pesan mucho más. Sirve cuando equivocarse por mucho es especialmente grave.
- **Definición precisa y fórmula:** RMSE = raíz cuadrada de (1/n) suma (y_i - yhat_i)^2. Los errores grandes pesan más. Se expresa en la unidad de la clase.
- **Ejemplo o código:** MSE 14,67 da RMSE de aproximadamente 3,83. Errores [10,10] y [0,20]: mismo MAE (10), RMSE 10 frente a 14,14.
- **Ojo (error común o límite):** El RMSE no es la media de los errores absolutos: la raíz se aplica después de promediar los cuadrados.
- **Comprueba:** ¿Por qué [10,10] y [0,20] tienen distinto RMSE con el mismo MAE?
- **Fuente exacta:** 03 §4; PDF p.44-45.

###### 2.5.d · MAPE (error porcentual absoluto medio)  (prioridad Media)

- **Explicación sencilla:** Mide el error como porcentaje del valor real. Sirve para comparar errores en cosas de tamaños muy distintos, por ejemplo precios pequeños y grandes, porque el porcentaje no depende de la escala.
- **Definición precisa y fórmula:** MAPE (%) = 100 (1/n) suma abs(y_i - yhat_i) / y_i. Versión del notebook con protección: (1/m) suma abs(yhat_i - y_i) / max(epsilon, abs(y_i)). Es una métrica relativa.
- **Ejemplo o código:** Proporciones 2/10, 2/20 y 6/30: promedio 16,67 %.
- **Ojo (error común o límite):** Si el valor real vale 0 la fórmula directa no está definida.
- **Comprueba:** ¿Qué hace el notebook para evitar dividir entre cero en el MAPE?
- **Fuente exacta:** 03 §4; PDF p.45-46; notebook métricas.

###### 2.5.e · make_scorer y greater_is_better  (prioridad Media)

- **Explicación sencilla:** La librería sklearn supone que un número mayor es mejor. Pero RMSE y MAPE son errores: menos es mejor. Por eso, al crear la métrica con make_scorer(), se indica greater_is_better=False. cross_validate() permite medir varias métricas a la vez.
- **Definición precisa y fórmula:** sklearn asume que mayor es mejor; RMSE y MAPE son errores (menor es mejor), por eso make_scorer(funcion, greater_is_better=False). MAE ya existe como 'neg_mean_absolute_error'. cross_validate admite varias métricas a la vez en scoring y devuelve fit_time, score_time y test_ y train_ de cada métrica (8 entradas con MAE, MAPE y RMSE).
- **Ejemplo o código:** metricas = {'MAE': 'neg_mean_absolute_error', 'RMSE': make_scorer(lambda y, yp: sqrt(mean_squared_error(y, yp)), greater_is_better=False)}.
- **Ojo (error común o límite):** Los valores salen negativos porque sklearn invierte el signo de los errores.
- **Comprueba:** ¿Por qué se pasa greater_is_better=False en RMSE?
- **Fuente exacta:** 03 §4; PDF p.46-47 (Programa 10).


### 2.6 · Evaluación en clasificación: matriz de confusión, precisión, sensibilidad, F1, accuracy  _(un video)_

#### Escena · Antes de contar aciertos, decide qué llamas «positivo»  _(cubre 2.6.a, 2.6.b)_

**Problema real.** Un sistema debe alertar sobre fraudes. Dejar pasar un fraude y detener una compra legítima son errores con consecuencias diferentes.

**Mapa de cuatro resultados.** Supón que «fraude» es la categoría positiva. Los cuatro números son del mismo grupo de cien compras.

| variable | qué significa | de dónde sale | ejemplo concreto | qué ocurre al inferir/calcular |
|---|---|---|---|---|
| `TP` | Fraude detectado | Era fraude y hubo alerta | `8` | Cuenta detecciones correctas. |
| `FN` | Fraude no detectado | Era fraude y no hubo alerta | `2` | Cuenta fraudes perdidos. |
| `FP` | Alerta falsa | Era legítima y hubo alerta | `12` | Cuenta molestias a compras legítimas. |
| `TN` | Compra legítima sin alerta | Era legítima y no hubo alerta | `78` | Cuenta descartes correctos. |

Es como un guardia que revisa entradas. Puede dejar pasar un problema real o detener a alguien inocente. Ambos son errores, pero tienen consecuencias distintas. Por eso no basta decir «acertó muchas veces»: primero mira *en qué* acertó y *en qué* falló. El archivo `03`, sección 5, introduce esta matriz.

**Compruébalo:** ¿por qué «fraude sin alerta» y «compra legítima con alerta» no son el mismo tipo de error?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Matriz de confusión: TP (*true positive*), FN (*false negative*), FP (*false positive*) y TN (*true negative*) (archivo `03`, sección 5).

**Significado preciso:** La matriz de confusión separa aciertos y errores según lo que ocurrió realmente y lo que se predijo; TP, FN, FP y TN son sus cuatro casillas.

#### Escena · Una nota general puede esconder el error importante  _(cubre 2.6.c, 2.6.d, 2.6.e, 2.6.g)_

En el ejemplo anterior hay diez fraudes y noventa compras legítimas. Si un sistema dice «legítima» para todas, acierta noventa de cien veces. Sin embargo, no detecta ningún fraude.

Por eso conviene mirar más de una medida: la proporción de aciertos totales, la proporción de alertas que eran fraudes y la proporción de fraudes encontrados. El archivo `03`, sección 5, da sus fórmulas. La medida útil depende de qué error cuesta más y de cuántas falsas alarmas puedes aceptar.

**Compruébalo:** ¿por qué acertar noventa de cien compras puede ser inútil si tu tarea principal es encontrar fraudes?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Exactitud (*accuracy*), precisión (*precision*) y sensibilidad (*recall*) (archivo `03`, sección 5).

**Significado preciso:** Exactitud = proporción de aciertos totales. Precisión = proporción de alertas correctas. Sensibilidad = proporción de positivos reales que se detectaron.

#### Escena · Resumir dos exigencias sin olvidar ninguna  _(cubre 2.6.f)_

**Problema real.** Un detector de fraude puede emitir pocas alertas muy acertadas y aun así dejar pasar muchos fraudes. Otro puede encontrar casi todos los fraudes, pero molestar a demasiadas compras legítimas.

**Intuición (apoyo pedagógico).** Para evaluar a un guardia, no basta saber si casi todas sus alarmas eran correctas; también importa si vio los problemas que realmente ocurrieron. Una sola cifra puede resumir ambas proporciones, aunque siempre conviene mirar las dos por separado.

El archivo `03`, sección 5, presenta una medida que combina la precisión de las alertas y la sensibilidad para encontrar casos positivos. Una medida combinada ayuda a comparar, pero no decide por ti cuánto cuesta cada tipo de error.

**Compruébalo:** ¿por qué una medida que solo mira si las alertas son correctas puede ocultar muchos fraudes no detectados?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

F1-score o medida F1, según el archivo `03`, sección 5.

**Significado preciso:** media armónica de precisión y sensibilidad; será baja si una de las dos es baja. Su fórmula está en «Profundiza» de este tema.

#### Escena · La misma probabilidad puede llevar a decisiones distintas  _(cubre umbral: se retoma en 5.1.a y 5.1.e)_

Un termómetro marca veinticuatro grados. Una persona abre la ventana a partir de veinte; otra espera a veinticinco. La medida no cambió: cambió la regla de acción.

Un modelo puede estimar `0,4` como probabilidad de fraude. Si alertas a partir de `0,5`, no alertas; si alertas a partir de `0,3`, sí. Esa cifra de corte decide qué acción tomas. Al bajarla suelen aparecer más alertas, tanto acertadas como falsas. El archivo `06`, sección 1.1, explica esta regla cuando el modelo da una probabilidad.

**Compruébalo:** ¿por qué bajar el umbral puede cambiar una alerta sin cambiar lo que el modelo estimó?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Umbral de decisión (*decision threshold*) (archivo `06`, sección 1.1).

**Significado preciso:** Umbral de decisión = valor a partir del cual una puntuación o probabilidad se convierte en una clase o acción.

#### Profundiza · Métricas de clasificación: define primero qué es positivo

**Mapa de la matriz de confusión (fuente: archivo `03`, sección 5; caso pedagógico).** Define “fraude” como positivo.

| variable | qué significa | de dónde sale | ejemplo concreto | qué ocurre al inferir/calcular |
|---|---|---|---|---|
| `TP` | Fraude real y alerta | Real positivo, predicho positivo | `8` | Aumenta precisión y sensibilidad. |
| `FN` | Fraude real sin alerta | Real positivo, predicho negativo | `2` | Reduce sensibilidad. |
| `FP` | Compra legítima con alerta | Real negativo, predicho positivo | `12` | Reduce precisión. |
| `TN` | Compra legítima sin alerta | Real negativo, predicho negativo | `78` | Aumenta exactitud. |

**Cálculo.** Hay `100` compras; `10` son fraude. Exactitud o *accuracy* `=(TP+TN)/100=86 %`. Precisión `=TP/(TP+FP)=8/20=40 %`: de las alertas, cuatro de cada diez son fraude. Sensibilidad o *recall* `=TP/(TP+FN)=8/10=80 %`: se detectan ocho de cada diez fraudes. `F1=2×precisión×sensibilidad/(precisión+sensibilidad)≈53,33 %`; resume el equilibrio entre precisión y sensibilidad.

**Análisis.** Un clasificador que dijera “legítima” a todo lograría `90 %` de exactitud, pero detectaría `0 %` de fraudes. Si el costo de un fraude no detectado es alto, observa la sensibilidad y cuántas falsas alarmas puedes asumir.

#### Profundiza · El umbral cambia la decisión, no la probabilidad calculada

**Idea (apoyo pedagógico; conexión con archivo `06`, sección 1.1).** El umbral convierte una puntuación o probabilidad en una clase. Bajarlo suele detectar más positivos reales y también activar más falsas alarmas, porque más casos quedan por encima de la línea de decisión. El efecto exacto depende de las puntuaciones observadas.

#### Fichas de conceptos del tema 2.6

##### 2.6 · Evaluación en clasificación: matriz de confusión, precisión, sensibilidad, F1, accuracy  (prioridad Alta)

- **Explicación sencilla:** Para evaluar una clasificación, primero cuenta qué categorías acertó y cuáles confundió. La matriz de confusión separa esos casos. De ella salen la exactitud, la precisión, la sensibilidad y F1; cada medida responde una pregunta distinta.
- **Definición precisa y fórmula:** En clasificación solo importa acertar o no la clase. La métrica principal es la matriz de confusión; de ella salen exactitud, precisión, sensibilidad (recall) y F1. Elegir qué clase es la positiva cambia precisión, recall y F1.
- **Ejemplo o código:** Fraude (positivo): TP 8, FN 2, FP 12, TN 78 sobre 100 compras.
- **Ojo (error común o límite):** Una nota general puede ocultar el error que más cuesta.
- **Comprueba:** ¿Por qué hay que decidir primero qué clase llamas positiva?
- **Fuente exacta:** 03 §5; PDF p.47-52.

###### 2.6.a · Matriz de confusión  (prioridad Alta)

- **Explicación sencilla:** Es una tabla con tantas filas y columnas como categorías. Cada celda cuenta cuántos casos de una categoría real el modelo asignó a una categoría predicha. Los aciertos son la suma de la diagonal; los fallos, el resto del total.
- **Definición precisa y fórmula:** Matriz de confusión: cuadrada de orden m (número de clases); P_ij = número de predicciones con clase real C_i y predicha C_j. Aciertos = suma de la diagonal; fallos = n - suma de la diagonal. Filas = clase real; columnas = clase predicha.
- **Ejemplo o código:** Iris, DummyClassifier: [[17,16,17],[15,16,19],[18,22,10]]; diagonal 17+16+10 = 43 aciertos de 150, exactitud 0,287.
- **Ojo (error común o límite):** En multiclase se puede evaluar cada clase contra el resto, con m matrices.
- **Comprueba:** ¿Cómo se calculan los aciertos a partir de la matriz?
- **Fuente exacta:** 03 §5; PDF p.47-49; glosario PDF p.96.

###### 2.6.b · TP / TN / FP / FN (caso binario)  (prioridad Alta)

- **Explicación sencilla:** Son los cuatro resultados posibles cuando hay dos opciones, 'sí' o 'no'. TP: dijo 'sí' y era 'sí'. TN: dijo 'no' y era 'no'. FP: dijo 'sí' pero era 'no'. FN: dijo 'no' pero era 'sí'. De aquí salen precisión, sensibilidad y F1.
- **Definición precisa y fórmula:** TP: el modelo dice sí y la realidad es sí. TN: dice no y es no. FP: dice sí y es no. FN: dice no y es sí. Tabla: real positiva - predicha positiva TP, predicha negativa FN; real negativa - predicha positiva FP, predicha negativa TN.
- **Ejemplo o código:** Test médico: FP = sano marcado como enfermo (pruebas extra); FN = enfermo marcado como sano (riesgo grave).
- **Ojo (error común o límite):** FP y FN no son el mismo error ni cuestan lo mismo.
- **Comprueba:** ¿Por qué un falso negativo en un test de cáncer suele ser más grave?
- **Fuente exacta:** 03 §5; PDF p.49 (Tabla 6); notebook métricas sección 1.2.1.

###### 2.6.c · Exactitud (accuracy)  (prioridad Alta)

- **Explicación sencilla:** Es el porcentaje de predicciones correctas sobre el total. Es fácil de entender, pero puede engañar cuando una categoría es mucho más frecuente que las otras, porque acertar la común ya da un número alto.
- **Definición precisa y fórmula:** Exactitud (%) = 100 (TP + TN) / (TP + TN + FP + FN); en general 100 suma P_ii / n. Por clase: Exactitud(C_i) = 100 P_ii / suma_j P_ij.
- **Ejemplo o código:** TP 8, TN 78, FP 12, FN 2: exactitud = 86 %.
- **Ojo (error común o límite):** Puede engañar con clases desbalanceadas.
- **Comprueba:** Con 10 fraudes en 100, ¿qué exactitud logra un sistema que siempre dice legítima?
- **Fuente exacta:** 03 §5; PDF p.48-49.

###### 2.6.d · Precisión  (prioridad Alta)

- **Explicación sencilla:** De todos los casos que el modelo marcó como 'sí', indica qué proporción realmente lo era. Sirve para saber cuánta confianza dar cuando el modelo dice 'sí'.
- **Definición precisa y fórmula:** Precisión (%) = 100 TP / (TP + FP): proporción de aciertos entre todas las predicciones positivas. Mide cuánto se puede confiar cuando el modelo dice sí. Interesa cuando importa limitar los falsos positivos.
- **Ejemplo o código:** TP 8, FP 12: precisión = 8/20 = 40 %.
- **Ojo (error común o límite):** Una precisión de 100 % (FP = 0) no implica detectar todos los positivos reales.
- **Comprueba:** ¿Qué indica una precisión del 40 %?
- **Fuente exacta:** 03 §5; PDF p.49-50.

###### 2.6.e · Sensibilidad / Recall / Exhaustividad  (prioridad Alta)

- **Explicación sencilla:** De todos los casos que realmente eran 'sí', indica qué proporción detectó el modelo. Sirve para saber si se le están escapando casos positivos reales, es decir, falsos negativos.
- **Definición precisa y fórmula:** Sensibilidad (recall, exhaustividad, cobertura) (%) = 100 TP / (TP + FN): proporción de positivos reales que el modelo detecta. Interesa cuando importa evitar falsos negativos.
- **Ejemplo o código:** TP 8, FN 2: sensibilidad = 8/10 = 80 %.
- **Ojo (error común o límite):** Una sensibilidad de 100 % (FN = 0) es compatible con muchos falsos positivos (por ejemplo, decir sí siempre).
- **Comprueba:** ¿Qué proporción de fraudes se detecta si TP = 8 y FN = 2?
- **Fuente exacta:** 03 §5; PDF p.50.

###### 2.6.f · F1-score  (prioridad Alta)

- **Explicación sencilla:** Es un solo número que combina precisión y sensibilidad. Es útil porque a veces mejorar una empeora la otra. Es un promedio especial que baja bastante si alguna de las dos es mala.
- **Definición precisa y fórmula:** F1 = 100 (2 sensibilidad precisión) / (sensibilidad + precisión): media armónica de ambas; baja si alguna es baja. Mejor métrica que la exactitud con datos desbalanceados. En multiclase se usa average='micro' en el curso.
- **Ejemplo o código:** Precisión 0,40 y sensibilidad 0,80: F1 = 2 (0,40 0,80) / 1,20 = 0,533.
- **Ojo (error común o límite):** No decide por ti cuánto cuesta cada tipo de error.
- **Comprueba:** ¿Por qué F1 usa una media armónica y no una aritmética?
- **Fuente exacta:** 03 §5; PDF p.50 (Programa 11); notebook métricas sección 1.2.4.

###### 2.6.g · Datos no balanceados: por qué accuracy engaña  (prioridad Media)

- **Explicación sencilla:** Si una categoría es nueve veces más común que otra, un modelo que siempre responde la más común acierta más del 80% sin haber aprendido nada. Por eso, en estos casos, se necesitan también precisión, sensibilidad y F1.
- **Definición precisa y fórmula:** Notebook (digits, el dígito 9 contra el resto, razón 9 a 1): un DummyClassifier que siempre dice no es 9 supera 80 % de exactitud sin haber aprendido nada, similar a un SVM real; por eso hacen falta precisión, recall y F1.
- **Ejemplo o código:** DummyClassifier(strategy='most_frequent').fit(X_train, y_train).score(X_test, y_test).
- **Ojo (error común o límite):** La curva ROC y el AUC no aparecen en el capítulo 2 del curso (sí en el de regresión logística, 5.1.l).
- **Comprueba:** ¿Por qué acertar 90 de 100 puede ser inútil si buscas fraudes?
- **Fuente exacta:** 03 §5 (notebook métricas, sección 1.2.2).


---

## BLOQUE 3 · Extracción de características (variables e imágenes)

**Pregunta principal:** ¿Qué partes de una tabla o imagen ayudan a decidir?  
**Al terminar deberías poder:** Convertir variables e imágenes en números que conserven la información relevante.

> Dos partes: (1) estadísticos unidimensionales (población, muestra, tipos de variable, resumen de variables cualitativas y cuantitativas) y (2) características bidimensionales: la imagen como tabla de intensidades, procesado, segmentación, descriptores de forma y descriptores de textura.

- **Ojo del bloque:** El manual PDF no cubre este tema; la teoría está en el PowerPoint del profesor (en la carpeta CLASES) y la práctica en seis notebooks cuyas celdas de texto son solo títulos.
- **Fuente exacta:** Archivo 04 (notebooks) + PPTX 'Tema 3 - Extracción de características' (56 diapositivas).

**Fuentes del bloque.** El resumen `04` cubre notebooks prácticos cuyas celdas de texto son solo títulos; la teoría y las figuras están en el PowerPoint del profesor. La definición del diámetro de Feret de la diapositiva 35 es conflictiva (ver Parte D).

#### Profundiza · De una observación a un atributo útil

**Concepto.** Extraer características transforma datos originales en variables útiles para analizar o modelar. “Útil” depende de la tarea: el color puede servir para madurez y resultar poco informativo para tamaño. Antes de convertir, pregunta qué distinción debe preservar la representación.


### 3.1 · Conceptos básicos y variable estadística  _(un video)_

#### Fichas de conceptos del tema 3.1

##### 3.1 · Conceptos básicos y variable estadística  (prioridad Media)

- **Explicación sencilla:** Son las ideas básicas para describir datos con números. Población es todo lo que se quiere estudiar. Muestra es una parte representativa de ella. Variable es el valor que cada elemento toma para una característica concreta.
- **Definición precisa y fórmula:** Población: conjunto de ítems que se desea estudiar. Muestra: subconjunto de la población; debe ser representativa, lo que se logra con muestreo aleatorio. Inferencia estadística: razonamiento que obtiene conclusiones, con margen de error conocido, sobre la población a partir de la muestra. Variable estadística: cualidad que poseen los individuos.
- **Ejemplo o código:** Intención de voto: población = personas mayores de 18 años empadronadas; muestra = subconjunto equilibrado por sexo, edad y zona.
- **Ojo (error común o límite):** Una muestra mal balanceada produce conclusiones erróneas.
- **Comprueba:** ¿Qué hace representativa a una muestra?
- **Fuente exacta:** PPTX diapositivas 3-6.

###### 3.1.a · Población  (prioridad Baja)

- **Explicación sencilla:** Es el conjunto completo de elementos que se quiere estudiar o analizar, sean casos, personas o filas de una tabla. Por ejemplo, todos los lotes de un producto fabricado en masa.
- **Definición precisa y fórmula:** Población: conjunto de ítems (instancias, individuos, elementos, filas) que se desea estudiar o sobre el que se quieren extraer conclusiones.
- **Ejemplo o código:** Todos los lotes de un producto que se fabricará en masa con un proceso industrial.
- **Ojo (error común o límite):** No siempre se puede medir toda la población: de ahí la muestra.
- **Comprueba:** ¿Qué es la población en el ejemplo de la tarta de tres ingredientes?
- **Fuente exacta:** PPTX diapositivas 3-4.

###### 3.1.b · Muestra y muestreo representativo  (prioridad Media)

- **Explicación sencilla:** Es una parte de la población. Debe elegirse al azar para representarla bien y poder aplicar sus conclusiones a todos. Si está mal balanceada, por ejemplo en edad o sexo, las conclusiones pueden ser erróneas.
- **Definición precisa y fórmula:** Muestra: cualquier subconjunto de la población; debe ser representativa, para lo cual se aplica muestreo aleatorio. El objetivo es conocer la población a partir del análisis de la muestra.
- **Ejemplo o código:** Una porción de la tarta que contenga un trozo de cada ingrediente (fresa, nata, chocolate).
- **Ojo (error común o límite):** Ejemplos de muestreo erróneo: muestras que omiten edades, sexos o ingredientes.
- **Comprueba:** ¿Por qué una porción con solo nata no representa la tarta?
- **Fuente exacta:** PPTX diapositivas 3-4.

###### 3.1.c · Inferencia estadística  (prioridad Baja)

- **Explicación sencilla:** Es el razonamiento que permite sacar conclusiones sobre toda la población a partir de una muestra, con un margen de error conocido. Evita tener que estudiar a todos los elementos.
- **Definición precisa y fórmula:** Inferencia estadística: proceso de razonamiento por el que se obtienen conclusiones (con un margen de error conocido) sobre la población a partir del análisis de la muestra.
- **Ejemplo o código:** Estimar el nivel educativo de Valencia a partir de 500 personas.
- **Ojo (error común o límite):** La conclusión vale para la población solo si la muestra es representativa.
- **Comprueba:** ¿Qué garantiza la inferencia estadística respecto al error?
- **Fuente exacta:** PPTX diapositiva 3.

###### 3.1.d · Variable estadística  (prioridad Media)

- **Explicación sencilla:** Es una cualidad de los elementos estudiados. Es el valor que un elemento toma para una característica, como una columna de la tabla. Puede cambiar de un elemento a otro o con el tiempo.
- **Definición precisa y fórmula:** Variable estadística: cada una de las cualidades que poseen los individuos de una población; el valor que toma una instancia para una característica. Tipos: nominales (modalidades no numéricas sin orden), ordinales (no numéricas con orden), discretas (valores contables) y continuas (infinitos valores en un rango).
- **Ejemplo o código:** Cualitativas nominales: sexo, estado civil. Ordinales: puesto en un deporte, satisfacción. Cuantitativas discretas: número de hijos. Continuas: estatura, peso.
- **Ojo (error común o límite):** Un código numérico de una categoría no la vuelve cuantitativa.
- **Comprueba:** ¿Es el número de hijos una variable discreta o continua?
- **Fuente exacta:** PPTX diapositivas 5-6.


### 3.2 · Análisis de variables cualitativas  _(un video)_

#### Escena · Una etiqueta no es una cantidad  _(cubre 3.2)_

Tienes camisetas azules, verdes y rojas. Puedes contar cuántas hay de cada color. Si escribes `1=azul`, `2=verde` y `3=roja`, los números son solo códigos: el color rojo no es «tres veces» el azul.

Con datos como la ciudad de residencia ocurre lo mismo: sus códigos son arbitrarios. En nivel de estudios sí hay un orden, pero no sabemos que la distancia entre «secundaria» y «grado» sea igual a la distancia entre «grado» y «doctorado». El notebook de variables cualitativas del archivo `04` cuenta categorías y las muestra con gráficos.

**Compruébalo:** ¿por qué cambiar el código de «azul» de `1` a `8` no cambia el color ni la cantidad de camisetas azules?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Variable cualitativa o categórica; frecuencia absoluta (archivo `04`, sección 1).

**Significado preciso:** Variable cualitativa = valores que son categorías. Frecuencia absoluta = número de casos de cada categoría.

#### Profundiza · Contar categorías sin inventar distancias

**Idea (fuente: archivo `04`, notebook de variables cualitativas).** Cuenta la frecuencia de cada categoría y muéstrala con barras o sectores. Si las categorías tienen orden, conserva ese orden al presentar los resultados. Un código numérico de categoría no indica por sí mismo una distancia cuantitativa entre niveles.

**Matiz.** Los niveles de estudios sí tienen un orden, pero los códigos numéricos no demuestran que la distancia entre dos niveles consecutivos sea siempre igual.

#### Fichas de conceptos del tema 3.2

##### 3.2 · Análisis de variables cualitativas  (prioridad Media)

- **Explicación sencilla:** Trata las variables que son categorías, como el nivel de estudios. Se cuenta cuántas veces aparece cada categoría y se muestra en gráficos. Así se resume la muestra sin tener que revisarla completa.
- **Definición precisa y fórmula:** Variables cualitativas (categorías): se resumen con tablas de frecuencia y se representan con diagramas de barras y de sectores.
- **Ejemplo o código:** Nivel de estudios: Secundaria, Bachillerato, Grado, Máster, Doctorado.
- **Ojo (error común o límite):** Los códigos numéricos son etiquetas: la media de los códigos no tiene sentido.
- **Comprueba:** ¿Por qué la media de los códigos 1=secundaria y 2=grado no describe un nivel de estudios?
- **Fuente exacta:** PPTX diapositivas 7-8; notebook var_cualitativas.

###### 3.2.a · Tablas de frecuencia  (prioridad Media)

- **Explicación sencilla:** Es una tabla que cuenta cuántas veces aparece cada categoría en la muestra. Sirve para analizarla de forma ordenada. En código se obtiene con np.unique(datos, return_counts=True).
- **Definición precisa y fórmula:** Tabla de frecuencia: resume una muestra de datos cualitativos contando cuántas veces aparece cada categoría (frecuencia absoluta).
- **Ejemplo o código:** estudios, frecuencia = np.unique(nivel_estudios, return_counts=True). PPTX: muestra de K = 500 personas de 30 a 40 años de Valencia.
- **Ojo (error común o límite):** Si las categorías son ordinales conserva su orden al presentar la tabla.
- **Comprueba:** ¿Qué devuelve np.unique con return_counts=True?
- **Fuente exacta:** PPTX diapositiva 7; notebook var_cualitativas.

###### 3.2.b · Representación gráfica (barras y sectores)  (prioridad Baja)

- **Explicación sencilla:** Sirve para ver de un vistazo cuántas veces aparece cada categoría. En las barras, la altura muestra cuántas veces se repite cada una. En el gráfico de sectores (tipo pastel), cada porción muestra qué porcentaje del total le corresponde.
- **Definición precisa y fórmula:** Diagrama de barras: la altura es la frecuencia de cada categoría. Diagrama de sectores (pastel): cada porción es el porcentaje del total.
- **Ejemplo o código:** plt.bar(estudios, frecuencia); plt.pie(frecuencia, labels=estudios, autopct='%1.2f%%').
- **Ojo (error común o límite):** El sectores pierde legibilidad con muchas categorías.
- **Comprueba:** ¿Qué muestra la altura de una barra?
- **Fuente exacta:** PPTX diapositiva 8; notebook var_cualitativas.


### 3.3 · Análisis de variables cuantitativas  _(un video)_

#### Escena · El promedio puede ocultar lo que vive la mayoría  _(cubre 3.3.a)_

Cinco personas cobran `[2, 2, 2, 2, 12]` unidades. Si sumas y divides entre cinco, obtienes `4`. Pero cuatro personas cobran `2`. El valor central al ordenar es `2`.

El promedio y el valor central responden preguntas distintas. El notebook de variables cuantitativas del archivo `04` calcula el valor típico, cuánto se alejan los demás y en qué lugar queda cada dato al ordenarlos. Antes de elegir una medida, mira si unos pocos valores extremos cambian mucho el resumen.

**Compruébalo:** ¿por qué decir solo «el ingreso típico es 4» puede dar una imagen engañosa de estas cinco personas?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Variable cuantitativa; media, mediana, tendencia central y dispersión (archivo `04`, sección 2).

**Significado preciso:** Variable cuantitativa = valores que representan cantidades. Media = suma dividida por número de casos. Mediana = valor central después de ordenar.

#### Profundiza · Resumir una variable cuantitativa sin ocultar su distribución

**Idea (fuente: archivo `04`, notebook de variables cuantitativas).** La media y la mediana resumen el centro de maneras distintas; medidas de posición ubican valores ordenados; medidas de dispersión muestran cuánto varían; gráficos como el histograma muestran la forma. El notebook calcula y representa estas familias; las interpretaciones siguientes son apoyo pedagógico.

| Familia | Qué pregunta responde | Ejemplo | Precaución |
|---|---|---|---|
| Tendencia central | ¿Dónde se agrupan los valores? | Media, mediana | La media se mueve mucho por valores extremos. |
| Posición | ¿Qué valor deja cierta fracción por debajo? | Cuartiles, percentiles | Requiere ordenar los valores. |
| Dispersión | ¿Cuánto cambian los valores? | Rango, desviación estándar | Un centro igual puede esconder variaciones distintas. |
| Distribución | ¿Qué forma tiene el conjunto? | Histograma, asimetría | El aspecto del histograma depende de sus intervalos. |

**Ejemplo calculado.** La media es `(2+2+2+2+12)/5=4` y la mediana es `2`, el valor central al ordenar. Decir solo “ingreso típico: 4” oculta que cuatro de cinco casos valen `2`.

#### Fichas de conceptos del tema 3.3

##### 3.3 · Análisis de variables cuantitativas  (prioridad Alta)

- **Explicación sencilla:** Son números que resumen una lista de datos numéricos mirándola desde cuatro lados: dónde está el centro, cómo quedan ordenados, cuánto se separan unos de otros y qué forma tiene el conjunto. Se estudian por separado para no confundirlos.
- **Definición precisa y fórmula:** Cuatro familias de medidas: tendencia central (media, mediana, moda), posición (cuartiles, percentiles, RIC), dispersión (varianza, desviación típica) y distribución (asimetría y curtosis).
- **Ejemplo o código:** X = [0.5, 23, 0.3, 4.5, 0.3, 0.5, -28, -50, 60, -100, -10, -11, 13, 19, 1, 9] del notebook.
- **Ojo (error común o límite):** Los ejercicios del notebook (boxplot, iris) quedan sin resolver.
- **Comprueba:** ¿Qué pregunta responde cada una de las cuatro familias?
- **Fuente exacta:** PPTX diapositivas 9-10; notebook var_cuantitativas.

###### 3.3.a · Medidas de tendencia central: media, mediana, moda  (prioridad Alta)

- **Explicación sencilla:** Son tres maneras de decir cuál es el valor típico de los datos. La media es el promedio de siempre. La mediana es el valor que queda justo en el medio al ordenarlos. La moda es el valor que más se repite.
- **Definición precisa y fórmula:** Media = (1/N) suma x_i. Mediana: valor central de los datos ordenados (si N es par, promedio de los dos centrales). Moda: valor más repetido. En código: np.mean, np.median, stats.mode.
- **Ejemplo o código:** [2,2,2,2,12]: media 4, mediana 2, moda 2.
- **Ojo (error común o límite):** La media se desplaza con valores extremos; la mediana resiste mejor.
- **Comprueba:** ¿Qué medida describe mejor al típico de [2,2,2,2,12] y por qué?
- **Fuente exacta:** PPTX diapositiva 9; notebook var_cuantitativas.

###### 3.3.b · Medidas de posición: cuartiles, RIC y límites de outliers  (prioridad Alta)

- **Explicación sencilla:** Sirven para ubicar los datos y detectar valores raros. Los cuartiles cortan los datos ordenados en 4 partes. El rango intercuartílico (RIC) mide qué tan separados están los datos del 50% central. Con la regla 1.5·RIC se fijan límites; lo que cae fuera se considera un valor atípico (outlier), es decir, muy alejado del resto.
- **Definición precisa y fórmula:** Cuartiles Q1 (percentil 25) y Q3 (percentil 75); RIC = Q3 - Q1. Límites de outliers: inferior = Q1 - 1,5 RIC; superior = Q3 + 1,5 RIC. En código: np.percentile(X, 25), np.percentile(X, 75).
- **Ejemplo o código:** lim_inf = Q1 - 1.5*RIC; lim_sup = Q3 + 1.5*RIC.
- **Ojo (error común o límite):** El notebook propone dibujar el diagrama de cajas y bigotes, pero lo deja sin resolver.
- **Comprueba:** ¿Qué parte de los datos contiene el RIC?
- **Fuente exacta:** PPTX diapositiva 9; notebook var_cuantitativas.

###### 3.3.c · Medidas de dispersión: varianza y desviación típica  (prioridad Alta)

- **Explicación sencilla:** Miden cuánto se alejan los datos, en promedio, de la media. La desviación típica es la raíz de la varianza y tiene las mismas unidades que el dato original, por eso es más fácil de interpretar.
- **Definición precisa y fórmula:** Desviación típica sigma = raíz de (suma (x_i - media)^2 / N); varianza = sigma al cuadrado. En código: np.std(X) (divide entre N por defecto) y varianza = desvest**2.
- **Ejemplo o código:** Misma media con distintas dispersiones: [4,4,4,4] y [0,0,8,8] tienen media 4 pero desviaciones 0 y 4.
- **Ojo (error común o límite):** La varianza muestral del tema 1 (1.8.c) divide entre n - 1; aquí, entre N.
- **Comprueba:** ¿Por qué la desviación típica es más fácil de interpretar que la varianza?
- **Fuente exacta:** PPTX diapositiva 10; notebook var_cuantitativas.

###### 3.3.d · Medidas de distribución: asimetría y curtosis  (prioridad Media)

- **Explicación sencilla:** Describen la forma que tiene el conjunto de datos. La asimetría indica si los datos se inclinan más hacia un lado de la media. La curtosis indica si la forma es más puntiaguda o más achatada que la curva normal (la típica forma de campana).
- **Definición precisa y fórmula:** Asimetría A = suma (x_i - media)^3 / (N sigma^3): simetría respecto a la media. Curtosis K = suma (x_i - media)^4 / (N sigma^4) - 3: apuntamiento frente a la normal. K > 0 leptocúrtica; K = 0 mesocúrtica; K < 0 platicúrtica. En código: stats.skew(X) y stats.kurtosis(X, fisher=True).
- **Ejemplo o código:** if curtosis > 0: leptocúrtica; elif curtosis < 0: platicúrtica; else mesocúrtica.
- **Ojo (error común o límite):** El ejercicio final sobre iris queda sin resolver en el notebook.
- **Comprueba:** ¿Qué indica una curtosis positiva?
- **Fuente exacta:** PPTX diapositiva 10; notebook var_cuantitativas.


### 3.4 · Introducción a los datos 2D (la imagen como dato)  _(un video)_

#### Escena · Una imagen es una tabla enorme de luces y colores  _(cubre 3.4 y 3.5)_

Una fotografía parece una escena continua, pero digitalmente está formada por pequeños puntos llamados *píxeles*. Cada píxel tiene un valor de luz o color. Cambiar esos valores puede hacer más visible un borde o separar mejor un objeto del fondo.

Los notebooks de imágenes del archivo `04` muestran maneras de cambiar qué tan claros u oscuros son los píxeles. Ese cambio no «entiende» el objeto; solo modifica la imagen. Si resalta también puntos que no pertenecen al objeto, la etapa siguiente puede empeorar.

**Compruébalo:** ¿por qué aumentar el contraste de una foto no significa que ya hayas identificado qué parte de ella es el objeto?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Imagen digital y transformación de intensidad (archivo `04`, sección 3).

**Significado preciso:** Píxel = unidad pequeña de una imagen digital. Transformación de intensidad = regla que cambia sus valores de claridad u oscuridad.

#### Fichas de conceptos del tema 3.4

##### 3.4 · Introducción a los datos 2D (la imagen como dato)  (prioridad Alta)

- **Explicación sencilla:** Aquí empieza el tema de las imágenes. Una imagen se trata como una tabla de números: cada posición (x, y) guarda un valor de intensidad, o sea, qué tan claro u oscuro es ese punto o de qué color. Así el computador puede trabajar con ella.
- **Definición precisa y fórmula:** Una imagen es una función bidimensional f(x, y): x e y son coordenadas espaciales y f es la intensidad en ese punto. En color hay 3 canales (R, G, B). Ejemplo: píxel (130, 155) con R=239, G=151, B=147. En OpenCV: cv2.imread carga la imagen en orden BGR.
- **Ejemplo o código:** img = cv2.imread('./Lena_RGB.png'); np.shape(img); RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).
- **Ojo (error común o límite):** OpenCV carga en BGR, no en RGB: hay que convertir para mostrarla con otras librerías.
- **Comprueba:** ¿Qué guarda cada posición (x, y) de una imagen en escala de grises?
- **Fuente exacta:** PPTX diapositivas 11-13; notebook imagenes_transformaciones.


### 3.5 · Procesado de imagen: transformaciones de intensidad  _(un video)_

#### Fichas de conceptos del tema 3.5

##### 3.5 · Procesado de imagen: transformaciones de intensidad  (prioridad Media)

- **Explicación sencilla:** Son cambios que alteran qué tan claro, oscuro o contrastado se ve cada punto de la imagen (píxel), pero sin moverlo de lugar. Se usan para que la imagen se vea mejor o más uniforme antes de extraerle información.
- **Definición precisa y fórmula:** Transformaciones de intensidad: cambian el valor de cada píxel sin moverlo. Incluyen cambio de brillo, de contraste, transformación lineal a tramos, cambio de linealidad, negativo y ajuste y ecualización del histograma.
- **Ejemplo o código:** Original más 50 aclara; original menos 50 oscurece.
- **Ojo (error común o límite):** Mejorar el contraste no identifica qué parte de la imagen es el objeto.
- **Comprueba:** ¿Por qué una transformación de intensidad no mueve los píxeles de lugar?
- **Fuente exacta:** PPTX diapositivas 14-16; notebook imagenes_transformaciones.

###### 3.5.a · Cambio de brillo  (prioridad Media)

- **Explicación sencilla:** Aclara u oscurece la imagen sumando o restando el mismo número a todos los píxeles. Hay que usar la función especial de la librería y no el + común de Python, porque si no, los valores se pasan del máximo permitido y salen colores erróneos (desbordamiento).
- **Definición precisa y fórmula:** Brillo: se suma o resta una constante a todos los píxeles. En OpenCV usar cv2.add y no el operador +, para evitar el desbordamiento del tipo uint8 (rango 0 a 255).
- **Ejemplo o código:** mas_brillo_img = cv2.add(img, 50); menos_brillo_img = cv2.add(img, -100).
- **Ojo (error común o límite):** Con + de Python un valor que supera 255 da la vuelta y aparecen colores erróneos.
- **Comprueba:** ¿Por qué se usa cv2.add en vez de + al cambiar el brillo?
- **Fuente exacta:** PPTX diapositiva 14; notebook imagenes_transformaciones.

###### 3.5.b · Cambio de contraste  (prioridad Media)

- **Explicación sencilla:** Hace que las diferencias entre zonas claras y oscuras se acentúen o se suavicen. Se logra alejando o acercando los valores de cada píxel respecto a un punto de referencia, con la misma fórmula que usa el programa de edición GIMP.
- **Definición precisa y fórmula:** Contraste: acentúa o suaviza las diferencias entre zonas claras y oscuras. Fórmula del notebook (de acuerdo con GIMP): f = 131 (contraste + 127) / (127 (131 - contraste)); alpha = f; gamma = 127 (1 - f); cv2.addWeighted(img, alpha, img, 0, gamma).
- **Ejemplo o código:** contrast_img = cv2.addWeighted(img, alpha_c, img, 0, gamma_c).
- **Ojo (error común o límite):** No es lo mismo que cambiar el brillo (suma constante).
- **Comprueba:** ¿Qué parámetros de addWeighted implementan el contraste?
- **Fuente exacta:** PPTX diapositiva 15; notebook imagenes_transformaciones.

###### 3.5.c · Transformación lineal a tramos, negativo y ecualización del histograma  (prioridad Baja)

- **Explicación sencilla:** Son otras formas de cambiar la intensidad de la imagen: invertirla (negativo) o repartir mejor los tonos para ganar contraste general (ecualización del histograma). Advertencia: en las fuentes disponibles solo aparecen como títulos, sin explicación ni código.
- **Definición precisa y fórmula:** Transformación lineal a tramos, cambio de linealidad, negativo, ajuste del histograma y ecualización del histograma: la diapositiva 16 solo las nombra con ejemplos de imagen; el notebook no las desarrolla.
- **Ejemplo o código:** Ecualización: reparte mejor los tonos para ganar contraste global.
- **Ojo (error común o límite):** Hueco de fuente: no hay fórmula ni código en los materiales disponibles.
- **Comprueba:** ¿Qué efecto busca la ecualización del histograma?
- **Fuente exacta:** PPTX diapositiva 16 (sin desarrollo en el notebook).


### 3.6 · Procesado de imagen: espacios de color y transformaciones geométricas  _(un video)_

#### Fichas de conceptos del tema 3.6

##### 3.6 · Procesado de imagen: espacios de color y transformaciones geométricas  (prioridad Media)

- **Explicación sencilla:** Son dos operaciones distintas. Cambiar el espacio de color representa los colores de otra forma; transformar la geometría mueve, gira, recorta o deforma la imagen. En ambos casos debes saber qué cambió antes de medir el objeto.
- **Definición precisa y fórmula:** Dos operaciones distintas: cambiar el espacio de color (representar los colores de otro modo) y las transformaciones geométricas (traslación, rotación, perspectiva, recorte y volteo) que reubican píxeles.
- **Ejemplo o código:** Pasar a escala de grises antes de umbralizar; recortar la región de interés antes de medir.
- **Ojo (error común o límite):** Antes de medir, debes saber qué cambió la transformación.
- **Comprueba:** ¿Qué diferencia hay entre cambiar el espacio de color y rotar una imagen?
- **Fuente exacta:** PPTX diapositivas 17-23; notebook imagenes_transformaciones.

###### 3.6.a · Conversión de espacio de color (RGB↔CMYK, gris, HSV, Lab, YCrCb)  (prioridad Alta)

- **Explicación sencilla:** Es escribir los mismos colores con otro sistema, según lo que se necesite. RGB es el de las pantallas (se suma luz) y CMYK el de la impresión (se suma tinta). Gris guarda solo claridad. Los demás (HSV, Lab, YCrCb) separan el color de la luminosidad para tareas distintas.
- **Definición precisa y fórmula:** RGB: aditivo (pantallas). CMYK: sustractivo (impresión). Gris: solo claridad. HSV: Hue, Saturation, Value. Lab: luminosidad más dos ejes de color complementarios. YCrCb: luma más crominancia roja y azul. Se convierten con cv2.cvtColor. En CMYK el notebook calcula K = 1 - max(R, G, B); en la función convert_to_CMYK: C = (1 - R - K)/(1 - K), y análogas M e Y.
- **Ejemplo o código:** gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY); HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).
- **Ojo (error común o límite):** El ejercicio de C, M, Y queda sin resolver en el notebook de transformaciones; la fórmula está en el de segmentación.
- **Comprueba:** ¿Qué canal de CMYK se calcula a partir del máximo de R, G y B?
- **Fuente exacta:** PPTX diapositivas 17-18; notebooks imagenes_transformaciones e Image_segmentation.

###### 3.6.b · Traslación, rotación y perspectiva  (prioridad Media)

- **Explicación sencilla:** Mueven los píxeles a otro lugar para desplazar, girar o cambiar el ángulo de vista de la imagen. Para eso se usa una matriz, una tabla de números que indica cómo se reubica cada punto. La perspectiva se define con 4 puntos.
- **Definición precisa y fórmula:** Traslación: matriz afín M = [[1,0,tx],[0,1,ty]] con cv2.warpAffine. Rotación: cv2.getRotationMatrix2D(centro, ángulo, escala) y warpAffine. Perspectiva: rotación de la superficie de proyección; a partir de 4 puntos origen y destino con cv2.getPerspectiveTransform y cv2.warpPerspective.
- **Ejemplo o código:** M = np.float32([[1,0,280],[0,1,-80]]); M = cv2.getRotationMatrix2D((cols/2, rows/2), angle=45, scale=2).
- **Ojo (error común o límite):** La rotación del notebook incluye un escalado (scale=2).
- **Comprueba:** ¿Qué dos números de la matriz de traslación indican cuánto se mueve la imagen?
- **Fuente exacta:** PPTX diapositivas 19, 21 y 22; notebook imagenes_transformaciones.

###### 3.6.c · Cropping (recorte / ROI)  (prioridad Media)

- **Explicación sencilla:** Es quedarse solo con una parte de la imagen, llamada región de interés (ROI). Así el análisis se centra en lo importante y el resto no estorba ni mete ruido, es decir, información que confunde.
- **Definición precisa y fórmula:** Cropping: seleccionar una zona como región de interés (ROI) para centrar los algoritmos en ella y evitar el ruido del resto. En numpy se hace con slicing.
- **Ejemplo o código:** new_img = img[90:290, 200:305].
- **Ojo (error común o límite):** El primer rango son las filas (alto) y el segundo las columnas (ancho).
- **Comprueba:** ¿Por qué conviene recortar la ROI antes de extraer características?
- **Fuente exacta:** PPTX diapositiva 20; notebook imagenes_transformaciones.

###### 3.6.d · Flipping (volteo)  (prioridad Baja)

- **Explicación sencilla:** Da vuelta la imagen como en un espejo: horizontal, vertical o ambas. Es útil cuando las imágenes de una colección se tomaron con orientaciones distintas y se quiere dejarlas todas iguales.
- **Definición precisa y fórmula:** Flipping: voltear la imagen en horizontal, vertical o ambas, para dejar en una posición estándar imágenes adquiridas de modo distinto y extraer características uniformes. Con cv2.flip.
- **Ejemplo o código:** Ejercicio del notebook (flipVertical, flipHorizontal, flipBoth): sin resolver.
- **Ojo (error común o límite):** Útil para estandarizar la orientación de una base de datos de imágenes.
- **Comprueba:** ¿Cuándo es útil voltear imágenes antes de extraer características?
- **Fuente exacta:** PPTX diapositiva 23; notebook imagenes_transformaciones.


### 3.7 · Segmentación de imágenes  _(un video)_

#### Escena · Primero separa el objeto del fondo  _(cubre 3.7)_

Quieres medir una hoja puesta sobre una mesa. Antes de medir, dibujas qué zona pertenece a la hoja. Si marcas también su sombra, tu medida describirá hoja más sombra.

En imágenes, separar los puntos del objeto y del fondo produce una máscara. Piensa en una plantilla: deja pasar lo que se medirá y tapa lo demás. Los notebooks de segmentación del archivo `04` muestran esta etapa.

```text
[gris: imagen] → [ámbar: zona candidata] → [verde: máscara elegida]
```

**Compruébalo:** ¿por qué una medida perfecta aplicada a una máscara que incluye la sombra seguiría describiendo mal la hoja?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Segmentación de imágenes y máscara (archivo `04`, sección 4).

**Significado preciso:** Segmentación = separar regiones de una imagen. Máscara = representación que indica qué píxeles pertenecen a la región elegida.

#### Fichas de conceptos del tema 3.7

##### 3.7 · Segmentación de imágenes  (prioridad Alta)

- **Explicación sencilla:** Consiste en dividir la imagen en zonas u objetos, indicando a cuál pertenece cada píxel. Así se simplifica la imagen y se marca la zona que interesa. Es un paso obligatorio antes de medir la forma de los objetos.
- **Definición precisa y fórmula:** Segmentar es partir la imagen en segmentos (objetos) asignando una etiqueta a cada píxel; los píxeles con la misma etiqueta comparten características. Es previo a los descriptores de forma. Aplicaciones: imagen médica, reconocimiento de objetos, seguridad, tráfico y conducción autónoma. Técnicas: umbralización, agrupación, bordes, crecimiento de regiones, watershed, autoencoders (CNN) y espacio de color.
- **Ejemplo o código:** Máscara binaria: 1 para el objeto y 0 para el fondo.
- **Ojo (error común o límite):** Una máscara que incluye la sombra hace que cualquier medida describa objeto más sombra.
- **Comprueba:** ¿Qué se obtiene al segmentar y para qué sirve?
- **Fuente exacta:** PPTX diapositivas 24-33; notebook Image_segmentation.

###### 3.7.a · Segmentación semántica vs. de instancia  (prioridad Media)

- **Explicación sencilla:** En la semántica, cada píxel recibe la etiqueta de qué es (por ejemplo, persona o fondo), pero no se separan los individuos. En la de instancia, además, se distingue cada objeto por separado, como cada persona.
- **Definición precisa y fórmula:** Semántica: clasificación a nivel de píxel que asigna una etiqueta de objeto a cada píxel (p. ej. personas frente a fondo). De instancia: tarea más compleja que detecta objetos y asigna una etiqueta a cada objeto independiente (p. ej. cada persona).
- **Ejemplo o código:** Un grupo de personas: semántica marca todas como persona; instancia separa a cada una.
- **Ojo (error común o límite):** La detección de objetos es otra tarea distinta (diapositiva 25).
- **Comprueba:** ¿Qué distingue la segmentación de instancia de la semántica?
- **Fuente exacta:** PPTX diapositivas 24-25.

###### 3.7.b · Thresholding (umbralización) y método de Otsu  (prioridad Alta)

- **Explicación sencilla:** La umbralización convierte la imagen en blanco y negro: los píxeles por encima de un valor límite (umbral) se marcan como objeto. El método de Otsu elige ese límite solo, buscando que los dos grupos resultantes queden lo más diferentes posible entre sí.
- **Definición precisa y fórmula:** Umbralización: se convierte a grises, se calcula el histograma y se elige un umbral. Otsu elige el umbral que maximiza la varianza entre clases: c1 = 0..t y c2 = t+1..L; p_i = f_i/N; omega1(t) = suma_{i<=t} p_i; omega2 = suma_{i>t} p_i; mu1, mu2 medias de clase; mu_T = omega1 mu1 + omega2 mu2; varianza entre clases = omega1 (mu1 - mu_T)^2 + omega2 (mu2 - mu_T)^2; t* = argmax. Búsqueda exhaustiva, no paramétrico.
- **Ejemplo o código:** _, mask = cv2.threshold(gray_img, t, 255, cv2.THRESH_BINARY) (umbral manual); t, mask = cv2.threshold(gray_img, 0, 1, cv2.THRESH_OTSU).
- **Ojo (error común o límite):** Funciona mejor si el histograma tiene dos grupos de tonos bien separados.
- **Comprueba:** ¿Qué criterio usa Otsu para elegir el umbral?
- **Fuente exacta:** PPTX diapositivas 28-29; notebooks Image_segmentation y Descriptores_forma.

###### 3.7.c · Detección de bordes (Canny) y relleno de huecos  (prioridad Media)

- **Explicación sencilla:** Un borde es el punto donde la imagen cambia bruscamente de claro a oscuro. El método Canny los encuentra usando dos límites, y se recomienda que el menor sea un tercio del mayor. Luego se pueden rellenar los contornos cerrados.
- **Definición precisa y fórmula:** Un borde es donde hay un cambio de intensidad. Canny: (1) filtro gaussiano para reducir ruido; (2) Sobel: primera derivada, dos kernels 3x3, Gx y Gy, magnitud G y dirección theta (0, 45, 90 o 135 grados); (3) supresión de no máximos para adelgazar bordes; (4) umbralización por histéresis con dos umbrales (por encima del máximo es borde; por debajo del mínimo no; en medio, solo si está conectado a un borde). Luego binary_fill_holes rellena contornos cerrados que no tocan el límite de la imagen.
- **Ejemplo o código:** img_gaus = cv2.GaussianBlur(img_rgb, (5,5), 0); canny = cv2.Canny(img_gaus, 255/3, 255); filled_bordes = bfh(bordes).
- **Ojo (error común o límite):** El comentario del notebook dice minValue 3 veces mayor que maxValue, pero el código usa minValue = 255/3 (un tercio del máximo): se sigue el código.
- **Comprueba:** ¿Qué decide la histéresis para un píxel entre los dos umbrales?
- **Fuente exacta:** PPTX diapositivas 31-32; notebook Image_segmentation.

###### 3.7.d · Otras técnicas: crecimiento de regiones, clustering, watershed, espacio de color  (prioridad Baja)

- **Explicación sencilla:** En el crecimiento de regiones se parte de un píxel inicial (semilla) y se va extendiendo la etiqueta a los vecinos parecidos. También se mencionan clustering, watershed y autoencoders, pero sin detalle en las fuentes disponibles.
- **Definición precisa y fórmula:** Crecimiento de regiones (region growing): desde una semilla se extiende la etiqueta a los vecinos similares; en el notebook, cv2.floodFill desde (0,0). Clustering, watershed, autoencoders (CNN) y espacio de color aparecen como técnicas, con detalle solo del espacio de color (extraer el canal de interés y umbralizar).
- **Ejemplo o código:** ref = np.zeros((h+2, w+2), np.uint8); cv2.floodFill(mask, ref, (0,0), 0). Canal rojo: R = img[:,:,2]; t = np.max(R); mask[mask < t] = 0.
- **Ojo (error común o límite):** Hueco de fuente: clustering, watershed y autoencoders no se desarrollan.
- **Comprueba:** ¿Desde dónde parte el crecimiento de regiones?
- **Fuente exacta:** PPTX diapositivas 27 y 30; notebook Image_segmentation.


### 3.8 · Descriptores de forma (descriptores geométricos)  _(un video)_

#### Escena · Mide una característica que ayude a decidir  _(cubre 3.8 y 3.9)_

Una vez aislada la hoja, puedes contar cuánto espacio ocupa o medir su contorno. Esos números resumen aspectos de la forma. También puedes medir patrones de luz de su superficie si la textura ayuda a distinguirla.

Los notebooks de forma y textura del archivo `04` muestran medidas como área y perímetro. También construyen una tabla de qué tonos de gris aparecen juntos —la matriz GLCM— para comparar parches de cielo y hierba. No todas las medidas ayudan a todas las tareas: para reconocer tamaño, el área puede servir; para distinguir superficies, quizá sirva más la textura.

**Compruébalo:** ¿por qué el área no sirve para distinguir una superficie lisa de una rugosa del mismo tamaño?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Extracción de características; descriptores de forma y textura; GLCM (*gray-level co-occurrence matrix*) (archivo `04`, secciones 5–6).

**Significado preciso:** Descriptor = número que resume una propiedad. Los de forma miden la región; los de textura resumen patrones de tonos, a menudo mediante la GLCM.

#### Profundiza · Imágenes: de la transformación a las medidas

**Secuencia (fuente: notebooks de Tema 3; explicación pedagógica).** Una transformación de intensidad modifica valores de píxel para resaltar información. La segmentación decide qué píxeles pertenecen al objeto. Una máscara marca esa región. Los descriptores convierten la región en números: área, perímetro, caja envolvente, excentricidad o solidez. Los de textura resumen patrones locales de intensidad. Cada etapa depende de la anterior: un descriptor exacto sobre una máscara mala describe el objeto equivocado.

```text
[gris: imagen] → [ámbar: región candidata] → [verde: máscara] → [azul: medidas]
```

**Ejemplo de textura del curso (archivo `04`, sección 6).** El notebook compara parches de cielo y hierba mediante una matriz de coocurrencia de niveles de gris (GLCM) y propiedades estadísticas extraídas con `skimage`. El valor de una propiedad solo tiene sentido junto con la configuración usada para construir la matriz.

| Variable | Qué significa | De dónde sale | Ejemplo concreto | Qué ocurre al calcular o inferir |
|---|---|---|---|---|
| Máscara | Región seleccionada | Segmentación | `1` para objeto, `0` para fondo | Delimita qué píxeles se miden. |
| Área | Tamaño de la región | Conteo de píxeles de la máscara | `200` píxeles | Cambia con resolución y errores de segmentación. |
| Perímetro | Longitud del borde | Contorno de la máscara | `60` píxeles aprox. | Sube con bordes irregulares o ruido. |
| Caja envolvente | Rectángulo mínimo alineado a ejes | Extremos de la región | `20 × 15` | Resume tamaño y posición, también incluye fondo dentro del rectángulo. |
| Excentricidad | Qué tan alargada resulta una forma | Geometría de la región | Cercana a `0` si es redondeada | Cambia con la forma; una simple rotación no la altera. |
| Solidez | Área frente a su envolvente convexa | Región y casco convexo | Menor que `1` con entrantes | Indica concavidades, según calidad de la máscara. |

**Matiz.** Los valores exactos de ciertos descriptores dependen de la definición e implementación usada por la librería. Antes de comparar imágenes, mantén la misma escala, el mismo método de segmentación y la misma definición. Normalizar un descriptor puede ayudar cuando las imágenes tienen tamaños distintos.

#### Fichas de conceptos del tema 3.8

##### 3.8 · Descriptores de forma (descriptores geométricos)  (prioridad Alta)

- **Explicación sencilla:** Son números que describen la forma de un objeto y su contorno, para poder identificarlo y reconocer patrones. Solo se pueden calcular cuando el objeto ya fue separado del resto de la imagen (sección 3.7).
- **Definición precisa y fórmula:** Los descriptores geométricos analizan la forma estructural de objetos binarios y sus contornos; sirven para identificar objetos y reconocer patrones. Requieren una segmentación previa (máscara). Con skimage: label para separar componentes y regionprops para las propiedades.
- **Ejemplo o código:** lab, num = label(mask, return_num=True); prop = regionprops((lab == 1).astype('uint8')).
- **Ojo (error común o límite):** El fondo también recibe etiqueta: lab tiene un valor más que el número de objetos.
- **Comprueba:** ¿Qué función de skimage da las propiedades de cada objeto etiquetado?
- **Fuente exacta:** PPTX diapositivas 34-35; notebook Descriptores_forma.

###### 3.8.a · Área, bounding box y convex hull  (prioridad Alta)

- **Explicación sencilla:** Miden el tamaño y la silueta de un objeto. El área es la cantidad de píxeles que ocupa. La caja envolvente (bounding box) es el rectángulo más pequeño que lo contiene. La envoltura convexa (convex hull) es la figura sin entrantes más pequeña que lo rodea.
- **Definición precisa y fórmula:** Área: número de píxeles de la región. Bounding box (bbox): rectángulo mínimo que contiene la región; su área es el número de píxeles que contiene. Convex hull: polígono convexo mínimo que contiene la región; su área es convex_area.
- **Ejemplo o código:** bbox = prop[0].bbox; convex_image = convex_hull_image(objeto).
- **Ojo (error común o límite):** La caja envolvente incluye fondo dentro del rectángulo.
- **Comprueba:** ¿Cuál es la diferencia entre la caja envolvente y la envolvente convexa?
- **Fuente exacta:** PPTX diapositiva 34; notebook Descriptores_forma.

###### 3.8.b · Excentricidad, diámetro equivalente, extensión, ejes y orientación  (prioridad Media)

- **Explicación sencilla:** Describen qué tan alargado o ancho es un objeto, comparándolo con una elipse equivalente. La excentricidad va de 0 (círculo) a 1 (casi una línea). El diámetro equivalente es el de un círculo con la misma área. La extensión indica cuánto de su caja llena. Los ejes y la orientación dan su tamaño e inclinación.
- **Definición precisa y fórmula:** Excentricidad: relación entre la distancia focal de la elipse equivalente y su eje mayor (0 = círculo; 1 = segmento). Diámetro equivalente: diámetro de un círculo de igual área. Extensión: píxeles de la región entre píxeles de la bbox. Longitud de los ejes mayor y menor: de la elipse con el mismo segundo momento central normalizado. Orientación: ángulo de esa elipse con el eje horizontal, entre -90 y 90 grados.
- **Ejemplo o código:** Un círculo da excentricidad cercana a 0; una línea, cercana a 1.
- **Ojo (error común o límite):** Los valores exactos dependen de la implementación de la librería.
- **Comprueba:** ¿Qué valor de excentricidad tiene un círculo?
- **Fuente exacta:** PPTX diapositivas 34-35; notebook Descriptores_forma.

###### 3.8.c · Perímetro, solidez, compacidad y diámetro de Feret  (prioridad Media)

- **Explicación sencilla:** Perímetro mide el borde; solidez compara el objeto con su envolvente convexa; compacidad describe qué tan redondeado es. La diapositiva 35 define el diámetro de Feret con un cociente que coincide con la extensión: parece una errata, así que no se enseña como definición válida.
- **Definición precisa y fórmula:** Perímetro: número de píxeles del contorno. Solidez: área entre el área de la envolvente convexa (1 en polígonos regulares). Compacidad: la diapositiva dice área entre perímetro al cuadrado; el notebook calcula 4 pi área / perímetro^2 (circularidad). Rectangularidad (notebook): área / bbox_area. Diámetro de Feret: la diapositiva 35 lo define como un cociente entre el área y la bbox, lo que coincide con la extensión.
- **Ejemplo o código:** compactness = 4*math.pi*prop[0].area / prop[0].perimeter**2; rectangularity = prop[0].area / prop[0].bbox_area.
- **Ojo (error común o límite):** Errata: el diámetro de Feret definido en la diapositiva 35 parece contradictorio con la propia 'extensión'; no se enseña como definición verificada (ver Parte D.1 del prompt). El notebook no menciona los momentos de Hu.
- **Comprueba:** ¿Por qué el cociente área sobre bbox no puede ser a la vez la extensión y un diámetro?
- **Fuente exacta:** PPTX diapositiva 35; notebook Descriptores_forma; Parte D.1 del prompt (erratas y huecos).


### 3.9 · Descriptores de textura  _(un video)_

#### Fichas de conceptos del tema 3.9

##### 3.9 · Descriptores de textura  (prioridad Alta)

- **Explicación sencilla:** La textura describe cómo cambian los tonos dentro de una zona, no la forma de su contorno. El curso muestra varias técnicas: unas comparan píxeles vecinos y otras resumen patrones o puntos destacados. Conviene aprender cada una por separado.
- **Definición precisa y fórmula:** Descriptores de textura: la matriz de coocurrencia (GLCM) y sus propiedades, SIFT, SURF, HOG y LBP. Unos comparan píxeles vecinos; otros resumen patrones o puntos clave en vectores de características.
- **Ejemplo o código:** Vectores de tamaño fijo: SIFT 128, SURF 64 o 128, HOG 3780 (imagen 128x64), LBP uniforme P+2.
- **Ojo (error común o límite):** El curso agrupa en 'textura' técnicas que también describen forma (HOG, SIFT).
- **Comprueba:** ¿Cuál de las técnicas usa un histograma de gradientes?
- **Fuente exacta:** PPTX diapositivas 36-55; notebook Descriptores_textura.

###### 3.9.a · Matriz de coocurrencia (GLCM) y sus propiedades  (prioridad Alta)

- **Explicación sencilla:** Es una tabla que cuenta cuántas veces aparece cada par de tonos de gris separados por cierta distancia y dirección. De ella se sacan números que describen la textura: contraste, disimilitud, homogeneidad, ASM, energía y correlación.
- **Definición precisa y fórmula:** GLCM: frecuencia con que un píxel de nivel i es adyacente a uno de nivel j, con adyacencia definida por la distancia d y el ángulo alfa. Propiedades: contraste, correlación, disimilitud, homogeneidad, energía y segundo momento angular (ASM). En skimage: greycomatrix y greycoprops.
- **Ejemplo o código:** GLCM = greycomatrix(image, distances=[5], angles=[0], levels=np.max(image)+1, symmetric=True, normed=True); greycoprops(GLCM, 'contrast')[0,0].
- **Ojo (error común o límite):** El valor de una propiedad solo tiene sentido con la configuración (d, ángulo, niveles) usada.
- **Comprueba:** ¿Qué dos parámetros definen la adyacencia en la GLCM?
- **Fuente exacta:** PPTX diapositivas 36-37; notebook Descriptores_textura.

###### 3.9.b · SIFT (Scale-Invariant Feature Transform)  (prioridad Alta)

- **Explicación sencilla:** Encuentra puntos clave de la imagen que se reconocen aunque cambie el tamaño, el giro, la luz o el contraste. A cada punto le asigna una "huella" de 128 números, y así se puede reconocer el mismo punto en dos versiones de la imagen, por ejemplo una girada.
- **Definición precisa y fórmula:** SIFT: invariante a posición, escala, rotación, iluminación y contraste. Fases: (1) espacio de escalas L = G * I con varias octavas; (2) diferencia de gaussianas (DoG); (3) candidatos: extremos comparando 8 vecinos más 9 y 9 de las escalas contiguas; (4) refinar con Taylor (umbral 0,03) y eliminar bordes con la matriz Hessiana 2x2; (5) orientación con histograma de 36 bins (picos mayores del 80 %); (6) descriptor: ventana 16x16, bloques 4x4, 8 bins, 16 histogramas = 128 características.
- **Ejemplo o código:** sift = cv2.SIFT_create(nfeatures=0, nOctaveLayers=3); kp = sift.detect(img, None); BFMatcher(cv2.NORM_L1, crossCheck=True).
- **Ojo (error común o límite):** El notebook lo prueba con una versión girada 45 grados para mostrar la invariancia.
- **Comprueba:** ¿De cuántos números consta el descriptor SIFT de un punto y cómo se construye?
- **Fuente exacta:** PPTX diapositivas 38-42; notebook Descriptores_textura.

###### 3.9.c · SURF (Speeded-Up Robust Features)  (prioridad Media)

- **Explicación sencilla:** Es una versión de SIFT hasta 3 veces más rápida. Encuentra los puntos de interés y su orientación con un cálculo más eficiente (matriz Hessiana e imagen integral), por lo que sirve para aplicaciones en tiempo real.
- **Definición precisa y fórmula:** SURF: versión hasta 3 veces más rápida que SIFT. Usa el determinante de la matriz Hessiana con filtros aproximados e imagen integral; orientación con derivadas wavelet en arcos de 60 grados; descriptor: ventana 20x20 con 16 subregiones de 5x5 y 4 características cada una = 64 (o 128 en la versión extendida).
- **Ejemplo o código:** Pirámide de filtros: en cada escala se duplica el tamaño del filtro.
- **Ojo (error común o límite):** Hueco de fuente: el notebook no incluye código de SURF.
- **Comprueba:** ¿Qué hace más rápido a SURF que a SIFT?
- **Fuente exacta:** PPTX diapositivas 43-47.

###### 3.9.d · HOG (Histogram of Oriented Gradients)  (prioridad Media)

- **Explicación sencilla:** Describe la forma de un objeto según hacia dónde cambia la intensidad. Divide la imagen en celdas de 8x8 píxeles, cuenta las direcciones de cambio en cada una, ajusta los valores por grupos de 4 celdas y junta todo en una lista de números (por ejemplo, 3780).
- **Definición precisa y fórmula:** HOG: (1) gradientes con Sobel (kernel de tamaño 1), magnitud y dirección; (2) celdas de 8x8; (3) histograma de 9 bins (0 a 160 grados de 20 en 20; gradientes sin signo, 0 a 180); (4) normalizar en bloques de 16x16 (4 celdas = 36 valores) con L1 o L2; (5) para una imagen de 128x64: 7 x 15 bloques x 36 = 3780 características.
- **Ejemplo o código:** H = hog(crop, orientations=9, pixels_per_cell=(8,8), cells_per_block=(2,2), transform_sqrt=True, block_norm='L1').
- **Ojo (error común o límite):** La normalización busca invariancia a cambios de contraste y luminosidad.
- **Comprueba:** ¿Cuántas características da HOG en una imagen de 128x64?
- **Fuente exacta:** PPTX diapositivas 48-51; notebook Descriptores_textura.

###### 3.9.e · Local Binary Patterns (LBP)  (prioridad Alta)

- **Explicación sencilla:** Describe la textura comparando cada píxel con sus vecinos: si el vecino es mayor o igual se anota 1, si es menor 0. Esa cadena de unos y ceros se vuelve un número que reemplaza al píxel central. El conteo de esos números describe la imagen.
- **Definición precisa y fórmula:** LBP: ventana deslizante; se compara cada vecino con el píxel central (0 si es menor, 1 si es mayor o igual), la cadena binaria se multiplica por potencias de 2 y se suma. LBP_{P,R}: P vecinos y radio R. Invariante a rotación: 36 valores con P = 8. Uniformes: patrones con 2 transiciones o menos; hay P+1, y en total P+2 etiquetas (10 con P = 8).
- **Ejemplo o código:** Cadena 01011100: 4+8+16+64 = 92. lbp_image = local_binary_pattern(img_gray, P=8*R, R, method='uniform'); histograma de P+2 bins normalizado.
- **Ojo (error común o límite):** El histograma de P+2 = 10 bins son los 10 atributos que caracterizan la imagen.
- **Comprueba:** ¿Cuántos valores distintos tiene el LBP uniforme con P = 8?
- **Fuente exacta:** PPTX diapositivas 52-55; notebook Descriptores_textura.


---

## BLOQUE 4 · Modelos de regresión

**Pregunta principal:** ¿Cómo estimamos una cantidad desconocida?  
**Al terminar deberías poder:** Explicar y comparar OLS, regresión polinómica y KNN para predecir números.

> Tres modelos para predecir un número: regresión lineal múltiple (OLS), regresión polinómica (caso especial de la lineal con potencias de x) y KNN para regresión (promedio de los casos más parecidos). Se evalúan con MAE, RMSE, MAPE y R2.

- **Ojo del bloque:** El PDF no dedica un apartado propio a la polinómica: viene del notebook.
- **Fuente exacta:** Archivo 05 (PDF p.53-73 + notebooks tema 4).


### 4.1 · Regresión lineal múltiple (OLS)  _(un video)_

#### Escena · Sumar aportes para estimar una cantidad  _(cubre 4.1)_

Una factura puede tener una cuota fija y un cargo por cada hora de uso. Si la cuota es `10` y cada hora añade `2`, tres horas producen `10+2×3=16`.

La regla que se aprende usa esa forma: una base más un aporte por cada dato de entrada. Aprende los números de esos aportes mirando casos pasados y buscando que sus predicciones se alejen lo menos posible de las cantidades reales. El archivo `05`, sección 1, estudia una forma de hacerlo que da más peso a errores grandes al elevarlos al cuadrado. La factura solo explica la suma; los aportes aprendidos no prueban que una variable cause el resultado.

**Compruébalo:** si el cargo aprendido por hora es `2`, ¿por qué la predicción sube `2` al añadir una hora mientras todo lo demás queda igual?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Regresión lineal múltiple y mínimos cuadrados ordinarios (*ordinary least squares*, OLS) (archivo `05`, sección 1).

**Significado preciso:** Regresión lineal múltiple = suma de una base y aportes de varios atributos. OLS elige esos aportes minimizando errores al cuadrado.

#### Profundiza · Regresión lineal: qué aprende OLS

**Concepto (fuente: archivo `05`, sección 1).** La regresión lineal combina atributos mediante coeficientes. OLS elige coeficientes para minimizar la suma de errores al cuadrado en entrenamiento. La ecuación es lineal en los parámetros `w`; el atributo `x` puede haberse transformado antes de entrar.

| variable | qué significa | de dónde sale | ejemplo concreto | qué ocurre al inferir/calcular |
|---|---|---|---|---|
| `x₁`, `x₂` | Atributos | Datos del caso | Horas `3`, temperatura `25` | Se introducen en la ecuación. |
| `w₀` | Intercepto | Entrenamiento | `10` | Valor predicho cuando los atributos valen cero; puede no tener interpretación real si cero está fuera de los datos. |
| `w₁`, `w₂` | Coeficientes | Entrenamiento | `2`, `0,5` | Multiplican sus respectivos atributos. |
| `ŷ` | Predicción | `w₀+w₁x₁+w₂x₂` | `10+2×3+0,5×25=28,5` | Se compara con el resultado real al evaluar. |

**Análisis.** Un coeficiente cambia si los atributos están correlacionados. No lo interpretes como efecto causal solo porque el modelo prediga bien. Un error grande pesa más por el cuadrado, de modo que OLS puede ser sensible a valores extremos. Evalúa residuos y rendimiento fuera de entrenamiento.

**Precisión matemática.** Minimizar suma de cuadrados y minimizar MSE da los mismos coeficientes para un conjunto fijo, porque MSE solo divide por `n`; las cifras de ambas funciones de costo son distintas. OLS puede resolverse por distintos procedimientos computacionales: el objetivo matemático no exige un método iterativo particular.

#### Fichas de conceptos del tema 4.1

##### 4.1 · Regresión lineal múltiple (OLS)  (prioridad Alta)

- **Explicación sencilla:** Combina los datos de entrada como aportes que se suman para predecir un número. OLS, el método de mínimos cuadrados ordinarios, aprende el peso de cada aporte buscando que la suma de errores al cuadrado sea pequeña.
- **Definición precisa y fórmula:** Modelo: yhat = w0 + w1 x1 + ... + wp xp. OLS (ordinary least squares) minimiza f(w0..wp) = (1/n) suma (y_i - (w0 + suma_j w_j x_ij))^2. La función depende solo de los coeficientes porque x_ij y y_i son fijos. Válido para regresión simple (un atributo) y múltiple.
- **Ejemplo o código:** California housing con LinearRegression y KFold(10): R2 > 0 (mejor que DummyRegressor), MAE 4,003, desviación de la clase 9,188.
- **Ojo (error común o límite):** Un coeficiente aprendido no demuestra causalidad.
- **Comprueba:** ¿Qué cantidad minimiza OLS?
- **Fuente exacta:** 05 §1; PDF p.53-60.

###### 4.1.a · Ecuación del modelo lineal (hiperplano)  (prioridad Alta)

- **Explicación sencilla:** La predicción se arma sumando un valor base (w0) más cada dato multiplicado por su peso propio. Así el modelo convierte los datos de entrada en un número estimado. Con varios datos, esa suma describe una superficie plana en vez de una línea.
- **Definición precisa y fórmula:** yhat = w0 + w1 x1 + w2 x2 + ... + wp xp. yhat = valor predicho; x_j = atributos; w_j = coeficientes (reales); w0 = término independiente (intercept). Con varios atributos describe un hiperplano.
- **Ejemplo o código:** w0 = 10, w1 = 2, w2 = 0,5 con x1 = 3 y x2 = 25: yhat = 10 + 6 + 12,5 = 28,5.
- **Ojo (error común o límite):** w0 es la predicción con todos los atributos en cero y puede carecer de significado real.
- **Comprueba:** ¿Qué predice el modelo cuando todos los atributos valen cero?
- **Fuente exacta:** 05 §1; PDF p.54.

###### 4.1.b · Función objetivo (coste) minimizada por OLS  (prioridad Alta)

- **Explicación sencilla:** OLS escoge los pesos que hacen más pequeño el error promedio. Ese error se calcula restando la predicción del valor real, elevando al cuadrado y promediando, usando los datos de entrenamiento (ejemplos conocidos). Menor error significa mejor ajuste.
- **Definición precisa y fórmula:** Función objetivo (coste): f(w0,...,wp) = (1/n) suma_i (y_i - (w0 + suma_j w_j x_ij))^2, es decir, el MSE sobre el entrenamiento. El factor 1/n normaliza por el volumen de datos; cuanto menor f, mejor el ajuste.
- **Ejemplo o código:** Errores [-2, 2, 6] dan f = (4+4+36)/3 = 14,67.
- **Ojo (error común o límite):** Minimizar la suma de cuadrados y minimizar el MSE da los mismos coeficientes: solo cambia el factor 1/n.
- **Comprueba:** ¿Por qué f solo depende de los coeficientes?
- **Fuente exacta:** 05 §1; PDF p.54.

###### 4.1.c · Descenso de gradiente  (prioridad Media)

- **Explicación sencilla:** Es un método de prueba y ajuste repetido para hallar los mejores pesos. En cada paso se mueven los pesos hacia donde más baja el error. La tasa de aprendizaje controla qué tan grande es cada paso.
- **Definición precisa y fórmula:** Descenso de gradiente: algoritmo de búsqueda habitual; en cada iteración encuentra la dirección y magnitud de cambio de cada coeficiente que más reduce la función objetivo, usando una tasa de aprendizaje (learning rate).
- **Ejemplo o código:** Pasos pequeños repetidos hacia donde baja el error.
- **Ojo (error común o límite):** OLS puede resolverse por distintos procedimientos: el objetivo matemático no exige un método iterativo concreto.
- **Comprueba:** ¿Qué controla la tasa de aprendizaje?
- **Fuente exacta:** 05 §1; PDF p.55.

###### 4.1.d · Interpretación geométrica de los coeficientes (caso simple)  (prioridad Media)

- **Explicación sencilla:** Con un solo dato de entrada, el modelo es una recta. El peso w1 es su inclinación: cuánto cambia el resultado cuando el dato sube una unidad. El valor w0 es dónde la recta corta el eje, es decir, el resultado cuando el dato vale cero.
- **Definición precisa y fórmula:** Con un único atributo, el modelo es una recta: w1 es la pendiente (w1 = delta y / delta x) y w0 es la ordenada en el origen (valor de y cuando x = 0).
- **Ejemplo o código:** Si w1 = 2, subir una unidad de x sube 2 la predicción.
- **Ojo (error común o límite):** Con varios atributos cada w_j es el cambio de yhat por unidad de x_j manteniendo los demás fijos.
- **Comprueba:** Si w1 = 2, ¿cuánto cambia la predicción al subir x en una unidad?
- **Fuente exacta:** 05 §1; PDF p.55.

###### 4.1.e · Predicción con el modelo ya entrenado  (prioridad Baja)

- **Explicación sencilla:** Después de entrenar, los pesos ya no cambian. Para predecir un caso nuevo solo se ponen sus datos en la ecuación y se hace la cuenta. Por eso la respuesta es casi inmediata.
- **Definición precisa y fórmula:** Ya entrenado el modelo, los coeficientes quedan fijos: se sustituyen los atributos de la instancia de test en la ecuación y se evalúa. El proceso es casi instantáneo.
- **Ejemplo o código:** model.predict(X_test).
- **Ojo (error común o límite):** La predicción rápida contrasta con KNN, que debe consultar todos los ejemplos.
- **Comprueba:** ¿Por qué predecir con OLS es casi instantáneo?
- **Fuente exacta:** 05 §1; PDF p.56.

###### 4.1.f · R² (coeficiente de determinación)  (prioridad Alta)

- **Explicación sencilla:** R² mide cuánto de las variaciones reales explica el modelo. Con 1, acierta perfecto. Con 0, rinde igual que predecir siempre el promedio. Si es negativo, rinde peor que ese promedio. Sirve para saber si el modelo vale la pena.
- **Definición precisa y fórmula:** R2 = 1 - suma (y_i - yhat_i)^2 / suma (y_i - ybar)^2, con ybar la media de la clase. R2 = 1: predicción perfecta; R2 = 0: igual que un DummyRegressor (siempre la media); R2 < 0: peor que ese DummyRegressor.
- **Ejemplo o código:** Reales [10,20,30], predicciones [12,18,24]: SSE = 44, SST = 200, R2 = 1 - 44/200 = 0,78.
- **Ojo (error común o límite):** Si SST = 0 (clase constante) la fórmula exige un tratamiento especial. El manual cita R2 = 0,59 para OLS y la lectura 1 - MAE/desviación = 0,564 en otra página.
- **Comprueba:** ¿Qué indica un R2 negativo?
- **Fuente exacta:** 05 §1; PDF p.56 y p.59.

###### 4.1.g · Interpretación de coeficientes en regresión múltiple  (prioridad Alta)

- **Explicación sencilla:** El signo de cada peso dice si el dato sube (+) o baja (−) el resultado. Su tamaño indica qué tanto pesa ese dato. Esto solo es comparable si los datos se llevaron a una misma escala, para que ninguno parezca grande solo por sus unidades.
- **Definición precisa y fórmula:** El signo de w_j indica relación directa (+) o inversa (-) con la clase y su magnitud (valor absoluto) la importancia del atributo, siempre que los datos estén estandarizados para que las escalas sean comparables. En el notebook: linearM.coef_ (w1..w18) y linearM.intercept_ (w0).
- **Ejemplo o código:** Regresión múltiple con 18 predictores del dataset de autos (precio).
- **Ojo (error común o límite):** Con atributos correlacionados los coeficientes cambian y no deben leerse como efectos causales.
- **Comprueba:** ¿Por qué se estandariza antes de comparar coeficientes?
- **Fuente exacta:** 05 §1; PDF p.55 y p.60; notebook 2.

###### 4.1.h · Ventajas de la regresión lineal  (prioridad Media)

- **Explicación sencilla:** Es un modelo sencillo y fácil de entender. Funciona bien cuando la relación real es en línea recta. Entrenarlo toma un tiempo razonable y predecir es casi instantáneo.
- **Definición precisa y fórmula:** Ventajas: simplicidad del modelo, fácil interpretabilidad (a mayor valor absoluto del coeficiente, mayor importancia; el signo da la dirección), gran eficacia cuando la relación es lineal, entrenamiento de tiempo razonable y predicción casi instantánea.
- **Ejemplo o código:** Una ecuación con pocos términos que se puede explicar a un cliente.
- **Ojo (error común o límite):** Su eficacia depende de que la relación atributos-clase sea realmente lineal.
- **Comprueba:** ¿Qué ventaja de interpretación tiene la regresión lineal?
- **Fuente exacta:** 05 §1; PDF p.59-60.

###### 4.1.i · Supuestos de la regresión lineal  (prioridad Media)

- **Explicación sencilla:** Para que funcione bien, se supone que los datos de entrada no dependen entre sí, siguen una forma de campana (muy sensible a valores extremos o outliers), se relacionan en línea recta con el resultado y los errores varían parecido en todo el rango (homocedasticidad).
- **Definición precisa y fórmula:** Supuestos: independencia entre los atributos (baja correlación), distribución normal de los atributos (los outliers afectan mucho), relación lineal entre atributos y clase y homocedasticidad (varianza constante de los errores, independiente de los valores de los atributos).
- **Ejemplo o código:** Si los errores crecen con el tamaño de la casa, no hay homocedasticidad.
- **Ojo (error común o límite):** Cuando no se cumplen, la regresión puede dar malos resultados.
- **Comprueba:** ¿Qué significa homocedasticidad?
- **Fuente exacta:** 05 §1; PDF p.60.

###### 4.1.j · Variantes con regularización (Ridge, Lasso)  (prioridad Baja)

- **Explicación sencilla:** Ridge y Lasso son versiones de la regresión lineal que penalizan pesos demasiado grandes. Así evitan que el modelo se aprenda de memoria los datos de entrenamiento y falle con datos nuevos (sobreajuste). Ayudan con valores extremos. El manual solo las menciona, sin explicarlas.
- **Definición precisa y fórmula:** Ridge y Lasso añaden términos de penalización a la función objetivo para evitar el sobreajuste, especialmente con outliers. Aparecen en los notebooks (Ridge, Lasso, ElasticNet) pero fuera del alcance de las páginas 53-73 del PDF.
- **Ejemplo o código:** ElasticNet(alpha=0.01, l1_ratio=1) se usó en el bootstrap del tema 2.
- **Ojo (error común o límite):** Hueco de fuente: el curso solo las menciona.
- **Comprueba:** ¿Qué añaden Ridge y Lasso a la función objetivo?
- **Fuente exacta:** 05 §1; PDF p.60.


### 4.2 · Regresión polinómica  _(un video)_

#### Escena · Una línea recta puede quedarse corta  _(cubre 4.2)_

Una pelota lanzada hacia arriba primero sube y luego baja. Si dibujas su altura a lo largo del tiempo, una sola línea recta no sigue ambos tramos.

Puedes dar a la regla una nueva pista calculada a partir del tiempo, como «tiempo al cuadrado». Sigue sumando aportes, pero esa pieza permite que la predicción forme una curva. El notebook del archivo `05`, sección 2, muestra esta construcción. Una curva muy flexible puede copiar detalles de los casos conocidos y fallar en nuevos; se elige su complejidad usando pruebas reservadas.

**Compruébalo:** ¿por qué una curva muy flexible podría acertar los casos conocidos y fallar con casos nuevos?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Regresión polinómica (*polynomial regression*) (archivo `05`, sección 2).

**Significado preciso:** Regresión polinómica = crear potencias de los atributos, como x², para que una suma de aportes pueda seguir una curva.

#### Profundiza · Regresión polinómica: crear curvatura sin cambiar la idea básica

**Concepto (fuente: notebook del Tema 4).** Se crean atributos como `x²` y se ajusta un modelo lineal sobre `[x, x²]`: `ŷ=w₀+w₁x+w₂x²`. Es no lineal respecto a `x`, pero lineal respecto a `w₀,w₁,w₂`. Con varios atributos también pueden aparecer interacciones, según la transformación elegida.

**Análisis (ampliación externa).** Aumentar el grado da más flexibilidad y también más riesgo de sobreajuste: para `n` valores de entrada distintos, un polinomio de grado `n−1` puede pasar exactamente por los `n` puntos. Eso no garantiza buenas predicciones nuevas. Elige grado usando validación, con la creación de términos y cualquier escalado dentro de cada entrenamiento. Fuera del rango observado, las potencias pueden crecer de forma poco razonable.

#### Fichas de conceptos del tema 4.2

##### 4.2 · Regresión polinómica  (prioridad Media)

- **Explicación sencilla:** Sirve cuando la relación no es una recta sino una curva. El grado del polinomio (cuadrático, cúbico, etc.) decide qué tan curva es la forma que se ajusta a los datos.
- **Definición precisa y fórmula:** Se usa cuando la tendencia es curva. Según el grado: cuadrática (2), cúbica (3), cuártica (4)... Modelo: yhat = w0 x^0 + w1 x^1 + ... + wn x^n = suma_i w_i x^i. Es un caso especial de la regresión lineal múltiple.
- **Ejemplo o código:** FuelConsumptionCo2.csv: predictor FUELCONSUMPTION_COMB_MPG y objetivo CO2EMISSIONS.
- **Ojo (error común o límite):** Más grado permite más curvatura y más riesgo de sobreajuste.
- **Comprueba:** ¿Por qué sigue siendo un modelo lineal pese a dibujar una curva?
- **Fuente exacta:** 05 §2 (notebook 2).

###### 4.2.a · Ecuación polinómica de grado n  (prioridad Media)

- **Explicación sencilla:** La predicción suma varios términos: un valor base constante, el dato, el dato al cuadrado, al cubo, y así hasta la potencia elegida. Cada término tiene su propio peso. Eso permite que el modelo dibuje curvas en vez de rectas.
- **Definición precisa y fórmula:** yhat = w0 x^0 + w1 x^1 + w2 x^2 + ... + wn x^n = suma_{i=0}^{n} w_i x^i. Caso cuadrático: yhat = w0 + w1 x + w2 x^2.
- **Ejemplo o código:** Grado 2: tres coeficientes (w0, w1, w2).
- **Ojo (error común o límite):** El término constante es x^0.
- **Comprueba:** ¿Cuántos coeficientes tiene un polinomio de grado 3?
- **Fuente exacta:** 05 §2 (notebook 2).

###### 4.2.b · Truco: regresión polinómica como regresión lineal múltiple  (prioridad Alta)

- **Explicación sencilla:** Si tratas x, x², x³… como datos distintos, el problema de la curva se vuelve una regresión lineal múltiple común. Así se resuelve con las mismas herramientas, sin métodos nuevos. En sklearn se hace con PolynomialFeatures y LinearRegression.
- **Definición precisa y fórmula:** Truco: definir x1 = x, x2 = x^2, ..., xn = x^n convierte el problema en una regresión lineal múltiple yhat = suma w_i x_i. En sklearn: PolynomialFeatures(degree=2) genera las columnas [1, x, x^2] y luego LinearRegression ajusta sobre ellas.
- **Ejemplo o código:** poly = PolynomialFeatures(degree=2); train_x_poly = poly.fit_transform(x_train); clf = LinearRegression().fit(train_x_poly, y_train).
- **Ojo (error común o límite):** Es no lineal en x pero lineal en los coeficientes w.
- **Comprueba:** ¿Qué columnas genera PolynomialFeatures(degree=2) a partir de x?
- **Fuente exacta:** 05 §2 (notebook 2).

###### 4.2.c · Grado del polinomio como hiperparámetro  (prioridad Media)

- **Explicación sencilla:** El grado no lo calcula el modelo: lo eliges tú antes de entrenar (un hiperparámetro, o ajuste fijado a mano). Para comprobar si fue buena elección, comparas sus errores y R² contra el modelo de línea recta (grado 1).
- **Definición precisa y fórmula:** El grado (degree) es un ajuste de configuración: un hiperparámetro que se fija antes de entrenar. El notebook compara MAE, MSE, RMSE y R2 del grado 1 (lineal) frente al grado 2 sobre el mismo test; no recorre varios grados.
- **Ejemplo o código:** Notebook del tema 2: la curva de validación del polinomio sugiere grado 3.
- **Ojo (error común o límite):** Elige el grado con validación, nunca con el test.
- **Comprueba:** ¿Con qué datos se decide el grado del polinomio?
- **Fuente exacta:** 05 §2 (notebook 2); 03 §3.


### 4.3 · Vecinos más cercanos (KNN) para regresión  _(un video)_

#### Escena · Estimar desde casos parecidos  _(cubre 4.3)_

Para calcular cuánto tardará un trayecto nuevo, miras viajes anteriores con distancia y tráfico parecidos. Si tres viajes semejantes tardaron `10`, `12` y `20` minutos, una estimación sencilla es su promedio: `14` minutos.

Una regla basada en casos parecidos hace esa búsqueda de semejanza con números. Debes decidir qué datos definen «parecido», cómo medir la diferencia y cuántos casos consultar. El archivo `05`, sección 3, muestra que una columna con valores en miles puede pesar mucho más que otra con valores entre cero y uno, aunque no sea más útil.

**Compruébalo:** ¿por qué cambiar la manera de medir «parecido» puede cambiar qué viajes se eligen y, con ello, la predicción?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Vecinos más cercanos para regresión (*k-nearest neighbors*, KNN) (archivo `05`, sección 3).

**Significado preciso:** KNN para regresión = encontrar k casos cercanos según una distancia y combinar sus valores para estimar el caso nuevo.

#### Profundiza · KNN para regresión: predicción desde vecinos

**Concepto (fuente del curso, Tema 4).** KNN conserva casos de entrenamiento. Para un caso nuevo calcula distancias, elige `k` vecinos y combina sus valores objetivo; en la versión básica usa la media. Puede ponderarlos por distancia si se configura así.

| Variable | Qué significa | De dónde sale | Ejemplo concreto | Qué ocurre al calcular o inferir |
|---|---|---|---|---|
| `k` | Número de vecinos | Hiperparámetro elegido con validación | `3` | Determina cuántos objetivos se combinan. |
| `d` | Distancia entre casos | Atributos y métrica elegida | Euclídea o Manhattan | Ordena los vecinos; cambia con escalas y atributos. |
| `y₁…yₖ` | Objetivos de vecinos | Entrenamiento | `10, 12, 20` | Media simple `14`; con pesos puede cambiar. |
| `ŷ` | Predicción nueva | Agregación de vecinos | `14` | Se compara con el valor real solo al evaluar. |

**Trampa metodológica.** Si un atributo está en miles y otro entre cero y uno, el primero puede dominar la distancia. Estandarizar con entrenamiento suele importar para KNN. `k` muy pequeño vuelve la predicción sensible a ruido; `k` muy grande mezcla casos menos similares. **Ampliación externa:** con muchos atributos, las distancias pueden perder capacidad para distinguir vecinos útiles.

#### Fichas de conceptos del tema 4.3

##### 4.3 · Vecinos más cercanos (KNN) para regresión  (prioridad Alta)

- **Explicación sencilla:** Parte de la idea de que casos parecidos dan resultados parecidos. Para un caso nuevo, busca los k casos conocidos más parecidos y promedia sus valores. No arma ninguna fórmula previa: solo consulta los ejemplos guardados.
- **Definición precisa y fórmula:** KNN (k nearest neighbors): ejemplos parecidos en sus atributos tienen clases parecidas. En regresión, la predicción es el promedio de las clases de los k ejemplos de entrenamiento más cercanos. Depende de k y de una función de distancia d. También sirve en clasificación y no supervisado.
- **Ejemplo o código:** Con k = 3 vecinos de valores 10, 12 y 20 la predicción es 14.
- **Ojo (error común o límite):** La escala de los atributos domina la distancia: hay que estandarizar.
- **Comprueba:** ¿Qué hace KNN para predecir un caso nuevo?
- **Fuente exacta:** 05 §3; PDF p.61-73.

###### 4.3.a · Idea fundamental de KNN  (prioridad Alta)

- **Explicación sencilla:** Si dos casos se parecen en sus datos de entrada, probablemente tengan resultados parecidos. Por eso KNN predice buscando los casos conocidos más similares al nuevo y mirando qué valor tienen.
- **Definición precisa y fórmula:** Premisa: ejemplos similares en sus atributos presentan un comportamiento similar en su clase. La predicción para regresión es el promedio de las clases de los vecinos más parecidos.
- **Ejemplo o código:** Estimar el tiempo de un trayecto nuevo a partir de trayectos con distancia y tráfico parecidos.
- **Ojo (error común o límite):** Qué se considera parecido cambia la respuesta.
- **Comprueba:** ¿En qué premisa se basa KNN?
- **Fuente exacta:** 05 §3; PDF p.61.

###### 4.3.b · Entrenamiento trivial de KNN  (prioridad Baja)

- **Explicación sencilla:** KNN no aprende ninguna fórmula de los datos. Entrenarlo es solo guardar los ejemplos de entrenamiento. El trabajo ocurre después, cuando llega un caso nuevo y se consultan esos ejemplos guardados.
- **Definición precisa y fórmula:** El entrenamiento solo almacena el conjunto de datos de entrenamiento para consultarlo al predecir; no elabora ningún modelo, por lo que consume muy poco tiempo.
- **Ejemplo o código:** knn.fit(X_train, y_train) apenas guarda los datos.
- **Ojo (error común o límite):** Todo el costo se traslada a la predicción.
- **Comprueba:** ¿Dónde se concentra el costo de KNN: en entrenar o en predecir?
- **Fuente exacta:** 05 §3; PDF p.61.

###### 4.3.c · Distancia de Minkowski y caso euclídeo  (prioridad Alta)

- **Explicación sencilla:** Es una forma de medir qué tan parecidos son dos casos comparando sus datos. Con exponente q=2 se llama distancia euclídea, la "línea recta" entre dos puntos, y es la más usada en la práctica.
- **Definición precisa y fórmula:** Distancia de Minkowski: d(e_i, e_j) = (suma_d abs(x_id - x_jd)^q)^(1/q). Con q = 2 es la distancia euclídea (suma de cuadrados, raíz cuadrada), la más usada. Con q = 1 es la de Manhattan (p = 1 en sklearn).
- **Ejemplo o código:** KNeighborsRegressor(n_neighbors=10, p=1) usa la distancia Manhattan.
- **Ojo (error común o límite):** En sklearn el exponente q se llama p.
- **Comprueba:** ¿Qué valor de q da la distancia euclídea?
- **Fuente exacta:** 05 §3; PDF p.61-62; notebook 2 celda 22.

###### 4.3.d · Propiedades de una función de distancia  (prioridad Baja)

- **Explicación sencilla:** Para ser una medida de distancia válida, debe cumplir cuatro reglas: nunca ser negativa, ser cero solo entre un caso y él mismo, dar igual de A a B que de B a A, y que dar un rodeo nunca acorte el camino. Minkowski las cumple solo si q es 1 o más.
- **Definición precisa y fórmula:** Una función de distancia debe cumplir: no negatividad (d >= 0), identidad (d = 0 si y solo si e_i = e_j), simetría (d(e_i, e_j) = d(e_j, e_i)) y desigualdad triangular (d(e_i, e_j) <= d(e_i, e_r) + d(e_r, e_j)). Minkowski cumple las cuatro solo si q >= 1.
- **Ejemplo o código:** Con q = 0,5 Minkowski ya no es una distancia válida.
- **Ojo (error común o límite):** Son propiedades matemáticas; en la práctica interesa que midan similitud.
- **Comprueba:** ¿Para qué valores de q cumple Minkowski las cuatro propiedades?
- **Fuente exacta:** 05 §3; PDF p.62.

###### 4.3.e · Selección de los k vecinos más cercanos  (prioridad Media)

- **Explicación sencilla:** Los vecinos son los ejemplos guardados más cercanos al caso consultado. En vez de fijar cuántos (k), también se puede fijar un radio r y tomar todos los ejemplos que queden dentro de esa distancia.
- **Definición precisa y fórmula:** Los k vecinos v1..vk de un ejemplo e_i son los índices de los ejemplos de entrenamiento con menores distancias a e_i. Alternativa: en vez de un k fijo, usar un radio r y tomar todos los ejemplos con distancia menor o igual a r. Estructuras eficientes para buscarlos: KDTree y BallTree.
- **Ejemplo o código:** k = 10 en KNeighborsRegressor(n_neighbors=10).
- **Ojo (error común o límite):** Con radio, el número de vecinos varía según la zona.
- **Comprueba:** ¿En qué se diferencia elegir k vecinos de elegir un radio r?
- **Fuente exacta:** 05 §3; PDF p.62-63 y p.73.

###### 4.3.f · Predicción de KNN (promedio simple y ponderado)  (prioridad Alta)

- **Explicación sencilla:** La predicción es el promedio de los valores de los k vecinos. En la versión ponderada, los vecinos más cercanos influyen más que los lejanos en ese promedio, porque se parecen más al caso nuevo.
- **Definición precisa y fórmula:** Sin ponderar: yhat_i = (1/k) suma_j y_vj. Ponderada: yhat_i = suma_j n_j y_vj / suma_j n_j, con pesos n_j por vecino. En sklearn: weights='uniform' o 'distance'.
- **Ejemplo o código:** KNeighborsRegressor(n_neighbors=10, weights='distance').
- **Ojo (error común o límite):** No todos los vecinos tienen por qué contribuir igual.
- **Comprueba:** ¿Qué cambia al usar weights='distance'?
- **Fuente exacta:** 05 §3; PDF p.63 y p.67.

###### 4.3.g · Factores que afectan la eficacia de KNN  (prioridad Media)

- **Explicación sencilla:** KNN funciona mejor o peor según cuatro cosas: la escala de los datos, cómo se mide la distancia, si se eligen vecinos por cantidad (k) o por radio, y si el promedio es simple o ponderado.
- **Definición precisa y fórmula:** Cuatro factores: (1) escala de los atributos (los de valores más altos contribuyen más a la distancia); (2) medida de similitud (acorde al tipo de datos; Minkowski ponderada d = (suma w_d abs(x_id - x_jd)^q)^(1/q)); (3) estrategia de selección de vecinos (k fijo o radio); (4) cálculo de la predicción (resumen y ponderación).
- **Ejemplo o código:** Peso en kg (promedio 80) frente a altura en metros (promedio 1,7): sin igualar escalas, el peso domina.
- **Ojo (error común o límite):** Cada factor es un hiperparámetro o decisión de diseño.
- **Comprueba:** ¿Por qué el peso en kilos domina a la altura en metros en la distancia?
- **Fuente exacta:** 05 §3; PDF p.66-67.

###### 4.3.h · Necesidad de estandarizar antes de usar KNN  (prioridad Alta)

- **Explicación sencilla:** KNN se guía por distancias, así que un dato con números grandes domina y tapa a los demás. Igualar las escalas lo evita. En el ejemplo del manual, hacerlo subió R² de −0,075 a 0,64, o sea, de predecir peor que el promedio a acertar bastante más.
- **Definición precisa y fórmula:** Resultados del manual (California): KNN(k = 10) sin transformar R2 = -0,075 (MAE 6,841); estandarización + KNN R2 = 0,64; estandarización + selección del 10 % de atributos (f_regression) + KNN R2 = 0,727; con distancia de Manhattan (p = 1) mejora un poco más (MAE 3,27; el R2 impreso es -0,727, probablemente un artefacto de extracción del PDF). Frente a OLS (R2 = 0,59 y MAE 4,003) KNN es mejor.
- **Ejemplo o código:** Pipeline([('estandarizacion', StandardScaler()), ('reg', KNeighborsRegressor(n_neighbors=10))]).
- **Ojo (error común o límite):** La estandarización se ajusta solo con entrenamiento (dentro del pipeline).
- **Comprueba:** ¿Qué pasó con el R2 de KNN al estandarizar y por qué?
- **Fuente exacta:** 05 §3; PDF p.64-70 (Programas 13 y 14).

###### 4.3.i · Hiperparámetros de KNN y su ajuste con GridSearchCV  (prioridad Media)

- **Explicación sencilla:** Los ajustes que fijas antes de entrenar (hiperparámetros) son: cuántos vecinos usar (k), si pesan igual o según cercanía, y cómo medir la distancia. Puedes probarlos a mano o dejar que GridSearchCV pruebe combinaciones automáticamente.
- **Definición precisa y fórmula:** Hiperparámetros de KNeighborsRegressor: n_neighbors (k), weights ('uniform' o 'distance') y metric/p (función de distancia). GridSearchCV prueba combinaciones (por ejemplo k de 1 a 14, weights, metric euclidean, cosine, manhattan) con validación cruzada interna y scoring='r2'; best_params_ da la mejor.
- **Ejemplo o código:** parameters = {'n_neighbors': np.arange(1,15), 'weights': ('uniform','distance'), 'metric': ('euclidean','cosine','manhattan')}; GridSearchCV(reg, parameters, scoring='r2').
- **Ojo (error común o límite):** GridSearchCV pertenece al notebook; el capítulo de validación del PDF no incluye su código.
- **Comprueba:** ¿Qué devuelve model.best_params_?
- **Fuente exacta:** 05 §3 (notebooks 1 y 2).

###### 4.3.j · Ventajas e inconvenientes de KNN  (prioridad Media)

- **Explicación sencilla:** A favor: es simple, se puede explicar cada predicción mostrando los vecinos usados, y entrenarlo es instantáneo. En contra: con muchos datos predice lento, reacciona mal a casos raros, y necesita datos relevantes y en la misma escala.
- **Definición precisa y fórmula:** Ventajas: modelo simple (solo los datos), predicciones fáciles de explicar mostrando los vecinos usados (ejemplo del manual: cosecha de sandías de 12,5 toneladas por parecido con 2002 y 2006, k = 2) y entrenamiento instantáneo. Inconvenientes: predicción lenta con muchos datos, poca generalización (las anomalías afectan más con k bajo) y necesita atributos relevantes y en la misma escala.
- **Ejemplo o código:** Millones de instancias: cada predicción exige calcular millones de distancias.
- **Ojo (error común o límite):** KDTree y BallTree aceleran la búsqueda de vecinos.
- **Comprueba:** ¿Por qué KNN es lento al predecir pero rápido al entrenar?
- **Fuente exacta:** 05 §3; PDF p.72-73.


---

## BLOQUE 5 · Modelos de clasificación

**Pregunta principal:** ¿Cómo decidimos entre dos o más clases?  
**Al terminar deberías poder:** Explicar y comparar regresión logística, árboles y el uso de SVM mostrado en el curso.

> Tres maneras de asignar una categoría: regresión logística (estima la probabilidad de la clase 1 y decide con un umbral), árboles de decisión (preguntas sucesivas sobre los atributos) y SVM (el curso solo muestra su uso en código; no desarrolla su teoría).

- **Ojo del bloque:** Hueco de fuente en SVM: no hay teoría de hiperplano, margen, vectores de soporte ni kernels.
- **Fuente exacta:** Archivo 06 (PDF p.74-98 + notebooks LOGR/DT y SVM).


### 5.1 · Regresión logística (LOGR)  _(un video)_

#### Escena · Convertir pistas en una probabilidad estimada  _(cubre 5.1)_

Cuando miras el cielo, reúnes pistas como nubes y viento antes de decidir si llevar paraguas. Una pista puede inclinarte hacia «lloverá» y otra hacia «no lloverá».

El método del archivo `06`, sección 1, combina los datos en una puntuación y la transforma en un número entre cero y uno. Ese número se interpreta como probabilidad estimada de una clase, según el ajuste del modelo. Después se compara con una cifra de corte para tomar la decisión. Cambiar esa cifra no vuelve a calcular la probabilidad.

**Compruébalo:** ¿por qué una puntuación sin límite necesita transformarse antes de interpretarla como probabilidad?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Regresión logística (*logistic regression*, LOGR) y función sigmoide (archivo `06`, sección 1).

**Significado preciso:** Regresión logística = combina atributos en una puntuación. La función sigmoide convierte esa puntuación en un valor entre cero y uno.

#### Profundiza · Regresión logística: de una puntuación a una probabilidad

**Mapa de variables (fuente del curso, Tema 5; números de apoyo pedagógico).**

| Variable | Qué significa | De dónde sale | Ejemplo concreto | Qué ocurre al calcular o inferir |
|---|---|---|---|---|
| `x` | Atributos del caso | Datos disponibles al predecir | Horas de estudio `4` | Entran en la puntuación. |
| `w₀,w₁…` | Coeficientes | Entrenamiento | `w₀=-2`, `w₁=0,5` | Definen la puntuación lineal. |
| `z` | Puntuación o log-odds | `w₀+Σwⱼxⱼ` | `-2+0,5×4=0` | Pasa por la sigmoide. |
| `p` | Probabilidad estimada de clase `1` | `1/(1+e⁻ᶻ)` | Si `z=0`, `p=0,5` | Se compara con el umbral. |
| `t` | Umbral de decisión | Decisión según costos | `0,5` | Da clase `1` si `p≥t` según la regla adoptada. |

**Relación con la regresión lineal.** La combinación `w₀+Σwⱼxⱼ` es la misma forma vista en OLS. La diferencia es la salida y el criterio de entrenamiento: la sigmoide convierte la puntuación en probabilidad estimada y la regresión logística ajusta parámetros para clasificar probabilísticamente, habitualmente mediante log-verosimilitud. `z=0` equivale a `p=0,5`; cambiar el umbral cambia la decisión, no la probabilidad calculada.

**Matiz (fuente: archivo `06`, sección 1.3).** Los *odds* son `p/(1-p)` y los *log-odds* son el logaritmo de ese cociente; la puntuación `z` es igual a esos log-odds en este modelo. Un coeficiente positivo aumenta los log-odds al subir su atributo, manteniendo los otros fijos. No aumenta la probabilidad en una cantidad constante. **Ampliación externa:** antes de usar `p` como probabilidad para decisiones sensibles, conviene evaluar su calibración en datos nuevos.

#### Fichas de conceptos del tema 5.1

##### 5.1 · Regresión logística (LOGR)  (prioridad Alta)

- **Explicación sencilla:** Aunque dice "regresión", sirve para clasificar. Combina los datos en una suma con pesos y la convierte en una probabilidad de que el caso sea de la clase 1. Luego decide con un umbral, que por defecto es 0,5.
- **Definición precisa y fórmula:** LOGR (también regresión logit, clasificación por máxima entropía o log-linear) es un algoritmo de clasificación, no de regresión. Calcula la probabilidad P_i de que la clase del ejemplo sea 1 con una función logística sobre una combinación lineal de los atributos y decide: si P_i > 0,5 predice 1; si no, 0 (el umbral puede cambiarse).
- **Ejemplo o código:** yhat = 1 / (1 + e^-(w0 + w1 x1 + ... + wp xp)).
- **Ojo (error común o límite):** Solo traza una frontera lineal por clase.
- **Comprueba:** ¿Por qué la regresión logística es de clasificación aunque se llame regresión?
- **Fuente exacta:** 06 §1; PDF p.74-82.

###### 5.1.a · Qué es y para qué sirve LOGR  (prioridad Alta)

- **Explicación sencilla:** No responde directamente 0 o 1: primero calcula la probabilidad de que sea clase 1. Si pasa de 0,5, predice 1; si no, predice 0. Ese límite de 0,5 se puede cambiar según lo que necesites.
- **Definición precisa y fórmula:** El clasificador no predice directamente 0 o 1: predice la probabilidad P_i de que la clase de e_i sea 1. Regla de decisión: si P_i > 0,5 se predice 1; si P_i <= 0,5 se predice 0. El 0,5 es habitual pero se puede usar otro umbral, incluso buscado automáticamente para maximizar la bondad.
- **Ejemplo o código:** p = 0,4: con umbral 0,5 se predice 0; con umbral 0,3 se predice 1.
- **Ojo (error común o límite):** Cambiar el umbral cambia la clase predicha, no la probabilidad calculada.
- **Comprueba:** Si p = 0,4, ¿qué clase se predice con umbral 0,3?
- **Fuente exacta:** 06 §1.1; PDF p.74-75.

###### 5.1.b · Función sigmoide / logística — fórmula  (prioridad Alta)

- **Explicación sencilla:** Es una curva con forma de "S" que toma cualquier número y lo convierte en un valor entre 0 y 1. Así el resultado de la suma con pesos se puede leer como una probabilidad.
- **Definición precisa y fórmula:** PDF: yhat = 1 / (1 + e^-(w0 + w1 x1 + ... + wp xp)). Notebook, con t = w0 + w1 x1 + ...: el código usa exp(x) / (1 + exp(x)), equivalente a la forma del PDF 1 / (1 + e^-t). Curva en S entre 0 y 1.
- **Ejemplo o código:** def sigmoide(x): return np.exp(x) / (1 + np.exp(x)).
- **Ojo (error común o límite):** El resumen 06 transcribe la fórmula del notebook como e^t / (1 + e^-t) y la llama equivalente; no lo es (la estándar es e^t / (1 + e^t) = 1 / (1 + e^-t)). Se toman la forma del PDF y la del código.
- **Comprueba:** ¿Qué valor devuelve la sigmoide cuando t = 0?
- **Fuente exacta:** 06 §1.2; PDF p.77; notebook LORG_DT celdas 3-6.

###### 5.1.c · Comportamiento de la sigmoide y regla de signo  (prioridad Media)

- **Explicación sencilla:** La sigmoide es una curva que convierte cualquier número en un valor entre 0 y 1. Si el cálculo da negativo, queda bajo 0,5; si da cero o positivo, queda en 0,5 o más. Por eso el modelo elige clase 1 cuando el resultado es positivo y clase 0 cuando es negativo.
- **Definición precisa y fórmula:** La sigmoide tiende rápido a 0 para valores negativos y a 1 para valores positivos. sigma(t) < 0,5 si t < 0; sigma(t) >= 0,5 si t >= 0. Por tanto el modelo predice clase 1 si x^T w es positivo y clase 0 si es negativo.
- **Ejemplo o código:** x = np.linspace(-20, 20, 400); plt.plot(x, sigmoide(x)).
- **Ojo (error común o límite):** Positivo o negativo se refiere a la combinación lineal, no a la probabilidad.
- **Comprueba:** ¿Qué clase se predice si la combinación lineal vale -3?
- **Fuente exacta:** 06 §1.2; notebook LORG_DT celda 5.

###### 5.1.d · Comparación con regresión lineal  (prioridad Media)

- **Explicación sencilla:** La regresión lineal da como respuesta directa el resultado de una suma ponderada de los datos. La regresión logística (LOGR) hace ese mismo cálculo, pero lo pasa por la sigmoide, una curva que lo convierte en una probabilidad entre 0 y 1.
- **Definición precisa y fórmula:** Regresión lineal: y = w0 + w1 x1 + w2 x2 + ... (resultado directo). Regresión logística: toma ese mismo resultado lineal x^T w y lo pasa por la sigmoide: P(Y = 1 con X) = sigma(x^T w) = e^(x^T w) / (1 + e^(x^T w)).
- **Ejemplo o código:** Misma suma ponderada, distinta salida.
- **Ojo (error común o límite):** Cambian la salida (probabilidad acotada) y el criterio de entrenamiento (verosimilitud).
- **Comprueba:** ¿Qué función convierte la suma ponderada en probabilidad?
- **Fuente exacta:** 06 §1.2; notebook LORG_DT celda 6.

###### 5.1.e · Frontera de decisión, log-odds y umbral  (prioridad Alta)

- **Explicación sencilla:** La frontera de decisión es la línea que separa las dos clases: los puntos donde el cálculo lineal da 0 y la probabilidad es 0,5 (el umbral, el punto de corte). Con un dato de entrada es un punto, con dos es una recta, y así sigue.
- **Definición precisa y fórmula:** Frontera de decisión: puntos que cumplen w0 + w1 x1 + ... + wp xp = 0; ahí yhat = 0,5 (el umbral). Con un atributo es un punto; con dos, una recta; y así sucesivamente. La combinación lineal z son los log-odds: z = ln(p / (1 - p)), con odds = p / (1 - p). Un coeficiente positivo aumenta los log-odds al subir su atributo.
- **Ejemplo o código:** z = -2 + 0,5 x con x = 4: z = 0, p = 0,5.
- **Ojo (error común o límite):** Un coeficiente no aumenta la probabilidad en una cantidad constante; aumenta los log-odds.
- **Comprueba:** ¿Cuánto vale yhat sobre la frontera de decisión?
- **Fuente exacta:** 06 §1.3; PDF p.78.

###### 5.1.f · Tabla de valores extremos del modelo LOGR  (prioridad Baja)

- **Explicación sencilla:** Muestra qué probabilidad da el modelo según el resultado del cálculo lineal: muy negativo da casi 0, cero da 0,5 y muy positivo da casi 1. Nunca llega exactamente a 0 ni a 1, porque los números usados son finitos.
- **Definición precisa y fórmula:** Tabla 7 del PDF: combinación lineal menos infinito da yhat = 0 (mínimo); 0 da 0,5 (umbral); más infinito da 1 (máximo). Los valores exactos 0 y 1 nunca se alcanzan porque w y x son finitos.
- **Ejemplo o código:** Combinación lineal muy negativa (por ejemplo -10) da una probabilidad cercana a 0 sin llegar a serlo.
- **Ojo (error común o límite):** La probabilidad exacta 0 o 1 no existe en este modelo.
- **Comprueba:** ¿Por qué yhat nunca vale exactamente 1?
- **Fuente exacta:** 06 §1.3; PDF p.78 (Tabla 7).

###### 5.1.g · Entrenamiento: función objetivo (verosimilitud)  (prioridad Alta)

- **Explicación sencilla:** Entrenar es buscar los coeficientes (los pesos que multiplican cada dato) que mejor ajusten el modelo. Se usa la verosimilitud, una medida que premia al modelo cuando su probabilidad se acerca a la clase real: cerca de 1 si era clase 1, cerca de 0 si era clase 0.
- **Definición precisa y fórmula:** Entrenar es hallar w0..wp que maximizan la función de verosimilitud f = suma_i [ y_i ln(yhat_i) + (1 - y_i) ln(1 - yhat_i) ]. El primer sumando actúa cuando y_i = 1 (sube con yhat_i); el segundo cuando y_i = 0 (sube cuando yhat_i es menor). LogisticRegression de sklearn usa, entre otros, coordinate descent; el solver 'sag' (stochastic average gradient) se usa en el ejemplo.
- **Ejemplo o código:** LogisticRegression(solver='sag', max_iter=1000, random_state=1, multi_class='ovr').
- **Ojo (error común o límite):** Es una función a maximizar, no un error a minimizar.
- **Comprueba:** ¿Qué sumando de la verosimilitud actúa cuando la clase real es 0?
- **Fuente exacta:** 06 §1.4; PDF p.77-78.

###### 5.1.h · Regularización L1/L2 en LOGR  (prioridad Media)

- **Explicación sencilla:** Igual que en regresión lineal, se puede regularizar (L1/Lasso o L2/Ridge): se agrega una penalización que empuja los coeficientes hacia 0. Así se evita el sobreajuste, que es cuando el modelo memoriza los ejemplos y falla con datos nuevos.
- **Definición precisa y fórmula:** Como en regresión lineal, se puede regularizar con L1 (Lasso) o L2 (Ridge): se añade un término a la función objetivo que empuja los coeficientes hacia 0 para evitar el sobreajuste. En sklearn el parámetro C controla la regularización (C pequeño = regularización fuerte; dato de la librería, ampliación externa al resumen).
- **Ejemplo o código:** LogisticRegression(C=0.01, solver='liblinear') en el notebook.
- **Ojo (error común o límite):** En sklearn C es el inverso de la fuerza de regularización.
- **Comprueba:** ¿Qué efecto tiene la regularización sobre los coeficientes?
- **Fuente exacta:** 06 §1.4; PDF p.78; notebook LORG_DT.

###### 5.1.i · Clasificación multiclase con LOGR (One-vs-Rest)  (prioridad Media)

- **Explicación sencilla:** La regresión logística separa solo dos clases. Para más clases se arman varios clasificadores de dos opciones, cada uno de "una clase contra todas las demás" (One-vs-Rest). Las regiones de cada clase se construyen con las bisectrices (líneas a igual distancia) entre esas fronteras.
- **Definición precisa y fórmula:** LOGR es binaria; para m > 2 clases se descompone en m subproblemas One-vs-Rest: un clasificador binario por clase contra el resto. Con las fronteras de todos los clasificadores se construyen las regiones de decisión multiclase calculando las bisectrices entre ellas.
- **Ejemplo o código:** Iris tiene 3 clases: 3 clasificadores binarios internos.
- **Ojo (error común o límite):** multi_class='ovr' en sklearn selecciona esta estrategia.
- **Comprueba:** ¿Cuántos clasificadores binarios hacen falta con 3 clases en One-vs-Rest?
- **Fuente exacta:** 06 §1.5; PDF p.76-77.

###### 5.1.j · Código de ejemplo — Programa 15 (LOGR sobre iris)  (prioridad Media)

- **Explicación sencilla:** Ejemplo real con el conjunto de datos iris (flores), usando solo 2 características. Se probó con validación cruzada de 10 partes (dividir los datos en 10 grupos y rotar cuál se usa de prueba) y se midió con ACC, PREC, RECALL y F1. Resultado: F1 cercano a 0,906-0,907 y 14 errores.
- **Definición precisa y fórmula:** Programa 15: LOGR sobre iris con solo los 2 atributos del pétalo, validación cruzada KFold de 10 bolsas, métricas ACC, PREC, RECALL y F1 con average='micro'. Matriz de confusión [[50,0,0],[1,40,9],[0,4,46]], F1 promedio 0,906-0,907 (14 errores en total).
- **Ejemplo o código:** datos.data = datos.data[:,2:] toma solo 2 atributos; cross_val_predict(alg, datos.data, datos.target, cv=KFold(n_splits=10)).
- **Ojo (error común o límite):** El código usa evaluacion_funciones, un módulo auxiliar del curso.
- **Comprueba:** ¿Cuántos errores comete el modelo si la matriz es [[50,0,0],[1,40,9],[0,4,46]]?
- **Fuente exacta:** 06 §1.6; PDF p.78-80 (Programa 15).

###### 5.1.k · Resultados empíricos: LOGR ante fronteras lineales vs no lineales  (prioridad Alta)

- **Explicación sencilla:** Con datos separables por una línea recta, la regresión logística acierta cerca de 95%. Con forma de medias lunas baja a cerca de 86%, y con anillos concéntricos cae a cerca de 49%, casi azar. Esto confirma que solo traza fronteras rectas.
- **Definición precisa y fórmula:** Con validación cruzada de 3 pliegues: datos con frontera lineal (make_blobs) cerca del 95 % de aciertos; medias lunas (make_moons, frontera no lineal) cerca del 86 %; anillos concéntricos (make_circles) cerca del 49 %, casi azar. Confirma que LOGR solo traza una frontera de decisión lineal entre dos clases.
- **Ejemplo o código:** LR = LogisticRegression(C=0.01, solver='liblinear').fit(X_train, y_train); LR.predict_proba(grid)[:, 1] pinta P(y = 1).
- **Ojo (error común o límite):** El 49 % no es un fallo del código: ninguna recta separa anillos concéntricos.
- **Comprueba:** ¿Por qué LOGR cae a casi azar con anillos concéntricos?
- **Fuente exacta:** 06 §1.6; PDF p.82; notebook LORG_DT.

###### 5.1.l · AUC / curva ROC  (prioridad Media)

- **Explicación sencilla:** Es una forma de medir qué tan bien clasifica un modelo que da probabilidades. El AUC es el área bajo la curva ROC, que compara aciertos contra falsas alarmas al variar el umbral. Un AUC de 1 significa un clasificador perfecto.
- **Definición precisa y fórmula:** AUC (area under curve): área bajo la curva ROC (receiver operating characteristic), que relaciona la tasa de aciertos y la tasa de falsos positivos según el umbral. Mayor área, mejor clasificador; el perfecto tiene AUC = 1. Se usa con clasificadores que estiman probabilidades.
- **Ejemplo o código:** SVM multiclase: roc_auc_score(y_testing, y_proba_test, multi_class='ovr', average=None) y roc_curve sobre cada clase binarizada.
- **Ojo (error común o límite):** En el capítulo de validación (tema 2) no hay ROC ni AUC: aparece aquí y en el notebook de SVM.
- **Comprueba:** ¿Qué valor de AUC corresponde a un clasificador perfecto?
- **Fuente exacta:** 06 §1.1 y §3.1; PDF p.75.

###### 5.1.m · Ventajas e inconvenientes de LOGR  (prioridad Media)

- **Explicación sencilla:** Ventajas: es simple, fácil de interpretar (el signo y tamaño de cada coeficiente muestran su influencia) y rápido de entrenar y usar. Desventajas: supone que los datos de entrada no dependen entre sí y solo traza una frontera recta, lo que no alcanza para regiones complejas.
- **Definición precisa y fórmula:** Ventajas: ecuación sencilla (similar a OLS), interpretable (magnitud = importancia, signo = dirección), entrenamiento razonable (algo mayor que OLS por exponentes y logaritmos) y predicción casi instantánea. Inconvenientes: supone independencia estadística entre atributos y genera una única frontera lineal por clase, insuficiente para regiones complejas.
- **Ejemplo o código:** Útil como primera línea base de clasificación.
- **Ojo (error común o límite):** Con atributos muy correlacionados pierde estabilidad.
- **Comprueba:** ¿Qué limita a LOGR frente a regiones de decisión complejas?
- **Fuente exacta:** 06 §1.7; PDF p.81-82.


### 5.2 · Árboles de decisión  _(un video)_

#### Escena · Decidir mediante preguntas sucesivas  _(cubre 5.2)_

Para elegir ropa puedes preguntar: «¿Llueve?». Si no, preguntas: «¿Hace frío?». Cada respuesta te lleva por un camino hasta una decisión.

El método del archivo `06`, sección 2, aprende preguntas sobre los datos. Cada pregunta divide los casos en grupos; al final de una ruta hay una respuesta. Demasiadas preguntas pueden crear reglas para casos muy particulares y fallar con nuevos casos. Por eso se controla su tamaño y se evalúa con datos reservados.

```text
                 [ámbar: ¿llueve?]
                 /                \
   [verde: sí → paraguas]      [gris: no → otra pregunta]
```

**Compruébalo:** ¿por qué añadir más preguntas al árbol puede mejorar los casos conocidos sin garantizar mejores respuestas para casos nuevos?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Árbol de decisión; CART en los ejemplos del curso (archivo `06`, sección 2).

**Significado preciso:** Árbol de decisión = secuencia de preguntas que divide casos hasta llegar a una predicción. CART es una forma de construirlo.

#### Escena · Elegir una pregunta que separe mejor los grupos  _(cubre 5.2.f, 5.2.g)_

**Problema real.** En un grupo hay frutas maduras y verdes mezcladas. Puedes preguntar «¿es amarilla?» o «¿es grande?». La mejor pregunta es la que deja grupos más uniformes para la respuesta que quieres conocer.

**Intuición (apoyo pedagógico).** Si ordenas calcetines oscuros y claros, una separación ayuda cuando cada montón queda con menos mezcla. No basta con crear dos montones; importa cómo quedaron.

El archivo `06`, sección 2.4, menciona dos maneras de medir cuánta mezcla queda. Ambas valen cero cuando un grupo contiene una sola clase. Para juzgar una pregunta, mira cómo cambia la mezcla en los grupos que produce, considerando también cuántos casos caen en cada uno.

**Compruébalo:** ¿por qué una pregunta que deja dos grupos casi puros puede ser más útil que otra que deja ambos muy mezclados?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Impureza de Gini y entropía; el archivo `06`, sección 2.4, las menciona como criterios de partición.

**Significado preciso:** dos funciones distintas que cuantifican la mezcla de clases en un nodo. Sus fórmulas y un ejemplo calculado están en «Profundiza» de este tema; no tienen la misma escala numérica.

#### Profundiza · Árboles: preguntas sucesivas que dividen casos

**Concepto (fuente del curso, Tema 5).** Un árbol divide recursivamente el conjunto según atributos y umbrales. Cada hoja produce una predicción. Para elegir cortes se usan criterios como Gini o entropía: prefieren grupos con menos mezcla de clases. La *ganancia* de una división compara la impureza antes y después, ponderando por tamaño de los grupos.

| Variable | Qué significa | De dónde sale | Ejemplo concreto | Qué ocurre al calcular o inferir |
|---|---|---|---|---|
| `p_c` | Proporción de clase `c` en un nodo | Casos de entrenamiento del nodo | `3/4` positivos | Alimenta Gini y entropía. |
| Gini | `1-Σp_c²` | Proporciones del nodo | Con `3/4` y `1/4`: `0,375` | Es `0` si el nodo es puro. |
| Entropía | `-Σp_c log₂ p_c` | Proporciones del nodo | Con `3/4` y `1/4`: `≈0,811` bits | Es `0` si el nodo es puro; se toma `0 log 0 = 0`. |
| Profundidad | Número de cortes a lo largo de una ruta | Crecimiento o límite configurado | `3` | Más profundidad permite reglas más específicas. |

**Trampa metodológica.** Gini y entropía no tienen la misma escala numérica. No compares sus valores brutos para declarar ganador a uno; compara cómo cada criterio ordena divisiones dentro del mismo procedimiento. Un árbol sin límites puede aprender peculiaridades del entrenamiento. Poda o restringe profundidad, tamaño mínimo de hojas u otras opciones mediante validación.

#### Fichas de conceptos del tema 5.2

##### 5.2 · Árboles de decisión  (prioridad Alta)

- **Explicación sencilla:** Es un modelo que divide los datos paso a paso, usando una característica a la vez, hasta formar grupos donde casi todos son de la misma clase. Tiene nodos (la característica que se revisa), aristas (los valores posibles) y hojas (la predicción final).
- **Definición precisa y fórmula:** Un árbol de decisión es un modelo de conocimiento para clasificación (y para regresión, como árbol de regresión). Divide el conjunto jerárquicamente en trozos cada vez menores hasta que sus ejemplos son (casi) de la misma clase; cada división usa un atributo por vez, recursivamente. Nodo raíz, nodos internos (atributo), aristas (valor o rango) y hojas (predicción).
- **Ejemplo o código:** Jugar tenis: si Outlook = Sunny y Humidity = Normal, entonces Play = Yes.
- **Ojo (error común o límite):** Un árbol sin límites sobreajusta.
- **Comprueba:** ¿Qué contiene cada nodo interno, cada arista y cada hoja?
- **Fuente exacta:** 06 §2; PDF p.82-94.

###### 5.2.a · Qué son y cómo funcionan conceptualmente  (prioridad Alta)

- **Explicación sencilla:** Un árbol parte de un nodo raíz, sin ciclos. Cada nodo interno revisa una característica, cada arista es un valor o rango, y las hojas dan la respuesta final. Sirve para clasificar categorías y también para predecir números (árbol de regresión).
- **Definición precisa y fórmula:** Estructura de nodos y aristas sin ciclos con un nodo raíz. Nodo interno: nombre del atributo a evaluar. Arista: un valor o rango de ese atributo. Hoja: predicción final. Se construye dividiendo el conjunto con un atributo por vez.
- **Ejemplo o código:** Raíz Outlook, arista Sunny, nodo Humidity, arista Normal, hoja Yes.
- **Ojo (error común o límite):** Los atributos de la parte alta del árbol son los más relevantes.
- **Comprueba:** ¿Qué indica una hoja?
- **Fuente exacta:** 06 §2.1; PDF p.82-83.

###### 5.2.b · Ejemplo guía: dataset 'jugar-tenis'  (prioridad Media)

- **Explicación sencilla:** El ejemplo usa 14 casos con 5 características (día, clima, temperatura, humedad, viento) para predecir si se juega tenis (Sí/No). Se sigue el árbol nodo a nodo hasta una hoja. Algunas características no se usan si antes se llega a una hoja con una sola respuesta. Ejemplo: si hay sol y humedad normal, se juega.
- **Definición precisa y fórmula:** Dataset de 14 instancias con 5 atributos (Day, Outlook, Temp, Humidity, Wind) y clase Play (Yes o No). Leer el árbol: Sunny, luego Humidity Normal, hoja Yes, sin mirar Temp ni Wind (atributos irrelevantes para ese camino). Regla: si Outlook = Sunny y Humidity = Normal entonces Play = Yes.
- **Ejemplo o código:** Un camino raíz-hoja equivale a una regla si... entonces...
- **Ojo (error común o límite):** Algunos atributos no se usan si antes se llega a una hoja pura.
- **Comprueba:** ¿Por qué el árbol no consulta el viento en el camino Sunny-Normal?
- **Fuente exacta:** 06 §2.2; PDF p.82-85 (Tabla 8).

###### 5.2.c · Algoritmo ID3  (prioridad Media)

- **Explicación sencilla:** ID3 construye árboles que pueden tener varias ramas por nodo. En cada nodo elige la mejor característica según la ganancia de información (cuánto reduce el desorden) y luego poda, es decir, recorta ramas. Limitación: solo acepta características con categorías, no números.
- **Definición precisa y fórmula:** ID3 (Ross Quinlan, 1986): árboles n-arios (más de dos aristas por nodo); elige el mejor atributo en cada nodo por ganancia de información; poda el árbol después de construirlo para eliminar nodos que causarían sobreajuste. Limitación: solo atributos categóricos.
- **Ejemplo o código:** Si Outlook tiene 3 valores, el nodo tiene 3 aristas.
- **Ojo (error común o límite):** No admite atributos numéricos.
- **Comprueba:** ¿Qué métrica usa ID3 para elegir el atributo de cada nodo?
- **Fuente exacta:** 06 §2.3; PDF p.85.

###### 5.2.d · Algoritmo C4.5  (prioridad Media)

- **Explicación sencilla:** C4.5 es el sucesor de ID3. Acepta características numéricas, porque crea solos los puntos de corte. Extrae reglas del tipo "si... entonces..." de cada camino desde la raíz hasta una hoja, las ordena por eficacia y elimina las peores.
- **Definición precisa y fórmula:** C4.5 (sucesor de ID3, mismo autor): admite atributos numéricos creando automáticamente puntos de corte; extrae todas las reglas si... entonces... (un camino raíz-hoja = una regla), las ordena por eficacia y poda las que empeoran la eficacia global.
- **Ejemplo o código:** Corte creado: Humidity menor o igual a 75.
- **Ojo (error común o límite):** A diferencia de ID3, no se limita a categóricos.
- **Comprueba:** ¿Cómo trata C4.5 un atributo numérico?
- **Fuente exacta:** 06 §2.3; PDF p.85.

###### 5.2.e · Algoritmo CART  (prioridad Alta)

- **Explicación sencilla:** CART sirve para clasificar y para predecir números. A diferencia de ID3 y C4.5, solo hace árboles binarios: cada nodo se divide en máximo dos ramas. La versión de scikit-learn (DecisionTreeClassifier) solo admite características numéricas.
- **Definición precisa y fórmula:** CART (classification and regression trees): similar a C4.5, para clasificación y regresión; produce solo árboles binarios (máximo dos aristas por nodo). scikit-learn implementa una versión optimizada (DecisionTreeClassifier) que solo admite atributos numéricos.
- **Ejemplo o código:** tree.DecisionTreeClassifier().
- **Ojo (error común o límite):** En sklearn los atributos categóricos hay que codificarlos antes.
- **Comprueba:** ¿Cuántas aristas como máximo tiene un nodo de CART?
- **Fuente exacta:** 06 §2.3; PDF p.85.

###### 5.2.f · Criterio de partición: índice de Gini  (prioridad Alta)

- **Explicación sencilla:** El índice de Gini mide qué tan mezclado está un nodo: vale 0 si tiene una sola clase y sube cuanto más mezcladas están. El árbol elige el corte que más reduce esa mezcla. En iris, la raíz tiene 0,667 (3 clases mezcladas) y una hoja de 50 setosa tiene 0,0.
- **Definición precisa y fórmula:** Gini = 1 - suma_k p_k^2 (p_k = proporción de la clase k en el nodo): vale 0 si el nodo es puro y sube con la mezcla. El árbol elige el corte que más reduce la impureza de los nodos hijos. En sklearn: criterion='gini'.
- **Ejemplo o código:** Iris, raíz: gini 0,667, 150 muestras, value [50,50,50]; hoja setosa: gini 0,0. Nodo con 3/4 y 1/4: gini = 1 - (9/16 + 1/16) = 0,375.
- **Ojo (error común o límite):** Las fórmulas son de referencia estándar: el PDF no las reproduce y solo menciona Gini y entropía.
- **Comprueba:** ¿Cuánto vale Gini en un nodo con una sola clase?
- **Fuente exacta:** 06 §2.4; PDF p.85 y p.91 (Figura 21); notebook LORG_DT celda 42.

###### 5.2.g · Criterio de partición: entropía / ganancia de información  (prioridad Alta)

- **Explicación sencilla:** La entropía es otra forma de medir el desorden de un nodo, alternativa al Gini: vale 0 si hay una sola clase y crece con la mezcla. La ganancia de información, que usa ID3 para elegir la característica, mide cuánto baja ese desorden al dividir.
- **Definición precisa y fórmula:** Entropía = -suma_k p_k log2(p_k) (con 0 log 0 = 0); vale 0 si el nodo es puro. La ganancia de información (ID3) compara la impureza antes y después de dividir ponderando por el tamaño de los grupos. En sklearn: criterion='entropy'. Gini y entropía no tienen la misma escala numérica.
- **Ejemplo o código:** Nodo con 3/4 y 1/4: entropía = 0,311 + 0,5 = 0,811 bits.
- **Ojo (error común o límite):** No compares valores brutos de Gini y entropía para declarar ganador a uno.
- **Comprueba:** ¿Qué valor tienen Gini y entropía en un nodo puro?
- **Fuente exacta:** 06 §2.4; PDF p.85; notebook LORG_DT celda 42.

###### 5.2.h · Poda y control de sobreajuste  (prioridad Alta)

- **Explicación sencilla:** Un árbol demasiado grande se sobreajusta: memoriza los ejemplos y falla con datos nuevos. Para evitarlo se poda. Antes: se frena su crecimiento (limitar profundidad, hojas o mínimo de casos por nodo). Después: se quitan o unen nodos que aportan poco.
- **Definición precisa y fórmula:** El riesgo de sobreajuste crece con el tamaño del árbol. Pre-podado: detener el crecimiento (max_depth, max_leaf_nodes, min_samples_split o mínimo de ejemplos por hoja). Post-podado: eliminar o fusionar nodos con poca información. Se elige con validación.
- **Ejemplo o código:** DecisionTreeClassifier(max_depth=3).
- **Ojo (error común o límite):** Incluso con pre-podado los árboles tienden a sobreajustar (nota del notebook).
- **Comprueba:** ¿Qué diferencia hay entre pre-podado y post-podado?
- **Fuente exacta:** 06 §2.5; PDF p.94; notebook LORG_DT celda 41.

###### 5.2.i · Código de ejemplo — Programa 16 (CART sobre iris/wine/breast-cancer)  (prioridad Media)

- **Explicación sencilla:** Ejemplo con DecisionTreeClassifier con su configuración por defecto, probado con validación cruzada de 10 partes (rotar qué grupo de datos se usa de prueba) en tres conjuntos de datos. F1 (medida de aciertos): iris 0,933, mejor que la regresión logística (0,907); wine 0,859; breast-cancer 0,932.
- **Definición precisa y fórmula:** Programa 16: DecisionTreeClassifier() por defecto sobre IRIS, WINE y BREAST-CANCER con KFold(10): F1 = 0,933 (iris, mejor que LOGR con 0,907), 0,859 (wine) y 0,932 (breast-cancer). Genera mapas de regiones 2D y el árbol completo con export_graphviz (mostrar_modelo_arbol).
- **Ejemplo o código:** cross_val_predict(exp[0], exp[1].data, exp[1].target, cv=KFold(n_splits=10, random_state=seed)).
- **Ojo (error común o límite):** El código usa evaluacion_funciones, módulo auxiliar del curso.
- **Comprueba:** ¿En qué dataset mejora CART al F1 de LOGR del ejemplo anterior?
- **Fuente exacta:** 06 §2.6; PDF p.87-93 (Programa 16).

###### 5.2.j · Efecto de la profundidad máxima en el sobreajuste  (prioridad Media)

- **Explicación sencilla:** Se entrenaron árboles con profundidad creciente (1, 3, 5 y 7) sobre datos en forma de medias lunas. A más profundidad, las regiones se vuelven más complicadas e irregulares. Es un ejemplo visual claro de sobreajuste: el modelo se pega demasiado a los ejemplos.
- **Definición precisa y fórmula:** Árboles con max_depth = 1, 3, 5 y 7 sobre make_moons: a más profundidad las regiones de clasificación se vuelven más complejas e irregulares (sobreajuste).
- **Ejemplo o código:** for i in range(1, 9, 2): dt = DecisionTreeClassifier(max_depth=i).
- **Ojo (error común o límite):** La profundidad es un hiperparámetro que se elige con validación.
- **Comprueba:** ¿Qué ocurre con las regiones al aumentar la profundidad?
- **Fuente exacta:** 06 §2.6 (notebook LORG_DT celda 36).

###### 5.2.k · Importancia de características (feature_importances_)  (prioridad Media)

- **Explicación sencilla:** El árbol entrenado guarda un valor (feature_importances_) que indica qué tan importante fue cada característica en sus decisiones. Se relaciona con cuánto redujo cada una el desorden en los nodos donde se usó.
- **Definición precisa y fórmula:** dt.feature_importances_ da la importancia de cada atributo para las decisiones del árbol, relacionada con cuánto redujo la impureza en los nodos donde se usó. Ejemplo: breast_cancer (30 atributos) con train_test_split 70/30.
- **Ejemplo o código:** cancerTree = DecisionTreeClassifier().fit(X_can_train, y_can_train); cancerTree.feature_importances_.
- **Ojo (error común o límite):** Es una importancia dentro del árbol entrenado, no una prueba de causalidad.
- **Comprueba:** ¿Qué indica feature_importances_?
- **Fuente exacta:** 06 §2.6 (notebook LORG_DT celdas 43-50).

###### 5.2.l · Fronteras de CART vs LOGR  (prioridad Media)

- **Explicación sencilla:** Las fronteras de CART son cortes rectos paralelos a los ejes, uno por característica, formando regiones como cajas. La regresión logística, en cambio, traza una sola frontera en línea recta por clase.
- **Definición precisa y fórmula:** Las fronteras de CART son ortogonales a los ejes de los atributos (cortes atributo por atributo, regiones en forma de cajas); LOGR genera una única frontera lineal por clase.
- **Ejemplo o código:** Con medias lunas, el árbol dibuja escalones; la logística, una recta.
- **Ojo (error común o límite):** Ortogonales a los ejes no significa mejores: dependen de los datos.
- **Comprueba:** ¿Por qué las fronteras de CART son escalonadas?
- **Fuente exacta:** 06 §2.6; PDF p.89.

###### 5.2.m · Exportación gráfica del árbol  (prioridad Baja)

- **Explicación sencilla:** Con export_graphviz se crea un archivo .dot que, al abrirlo con graphviz, dibuja el árbol completo. Sirve para ver el modelo entrenado y entender cómo toma sus decisiones.
- **Definición precisa y fórmula:** export_graphviz(dt, out_file='tree.dot', class_names=[...], feature_names=[...], impurity=False, filled=True) crea un archivo .dot; graphviz.Source lo dibuja. mostrar_modelo_arbol de evaluacion_funciones lo usa internamente.
- **Ejemplo o código:** with open('tree.dot') as f: graphviz.Source(f.read()).
- **Ojo (error común o límite):** Requiere tener graphviz instalado.
- **Comprueba:** ¿Qué formato de archivo genera export_graphviz?
- **Fuente exacta:** 06 §2.6 (notebook LORG_DT celda 39).

###### 5.2.n · Ventajas e inconvenientes de árboles de decisión (CART)  (prioridad Media)

- **Explicación sencilla:** Ventajas: es fácil de interpretar porque va por pasos, entrena y predice rápido, y aguanta bien valores extremos, datos faltantes y escalas distintas. Desventajas: se sobreajusta con facilidad y le afecta que unas clases tengan muchos más ejemplos que otras.
- **Definición precisa y fórmula:** Ventajas: legibles de forma jerárquica, la predicción se explica con la regla del camino raíz-hoja, entrenamiento razonable aun en datasets grandes, predicción muy rápida (logarítmica en el número de instancias), robustos frente a outliers, ausentes y atributos de distintas escalas. Inconvenientes: riesgo de sobreajuste (mitigado con poda, mínimo de ejemplos por hoja o profundidad máxima) y sensibilidad al desbalanceo de clases.
- **Ejemplo o código:** Independientes de la escala: no requieren estandarizar.
- **Ojo (error común o límite):** Con árboles grandes la interpretabilidad también se pierde.
- **Comprueba:** ¿Qué técnicas mitigan el sobreajuste de un árbol?
- **Fuente exacta:** 06 §2.7; PDF p.93-94; notebook LORG_DT celda 52.


### 5.3 · SVM — Support Vector Machines  _(un video)_

#### Escena · Reconoce lo que el ejemplo de SVM muestra y lo que no explica  _(cubre 5.3)_

Si dibujas dos grupos de puntos en una hoja, podrías intentar trazar una separación entre ellos. Esa imagen ayuda a imaginar una clasificación, pero no explica todavía cómo se elige matemáticamente la separación.

El archivo `06`, sección 3, muestra código que usa `SVC` con `C=10` (valor elegido en el ejemplo) y kernel `rbf` (valor predeterminado de esa herramienta). «Kernel» es el nombre técnico de una función que permite comparar casos de otra manera; su mecanismo no queda explicado en este material. El código permite observar cómo entrenar, predecir y evaluar, pero no enseña cómo se elige matemáticamente la separación.

**Compruébalo:** ¿qué te falta saber, además de que el código funciona, para explicar cómo se separan los grupos?

**Nombre original del curso (dilo solo después de la pausa de intuición):**

Máquina de vectores de soporte (*support vector machine*, SVM); implementación `SVC` con kernel RBF (archivo `06`, sección 3).

**Significado preciso:** SVM = familia de clasificadores. SVC es la herramienta usada en el notebook; C y el kernel son configuraciones del modelo.

#### Profundiza · SVM: qué puedes afirmar a partir del material disponible

**Fuente del curso.** El archivo `06` documenta una llamada a `sklearn.svm.SVC`, con `C=10` y el kernel predeterminado `rbf`, además del flujo de evaluación. Esos materiales no desarrollan la teoría del hiperplano, margen, vectores de soporte ni kernels. Por eso este bloque separa el uso observado de una intuición adicional.

**Intuición externa breve (apoyo pedagógico, pendiente de fuente teórica adicional).** Un clasificador SVM busca una frontera entre clases; algunos ejemplos cercanos a esa frontera son decisivos para colocarla. Con un kernel como RBF, la frontera puede ser curva en el espacio original. El parámetro `C` influye en cuánto penaliza ciertos errores de clasificación durante el ajuste. Esto orienta la lectura del código, pero no sustituye una explicación rigurosa de la optimización ni del kernel.

**Aplicación respaldada por el notebook.** Identifica `X` e `y`, separa datos, ajusta `SVC`, predice sobre datos no usados para ajustar y evalúa con métricas de clasificación. Si estandarizas, calcula la escala solo con entrenamiento. Para comparar con logística o árboles, usa el mismo protocolo de validación y elige la métrica según la tarea.

#### Fichas de conceptos del tema 5.3

##### 5.3 · SVM — Support Vector Machines  (prioridad Media)

- **Explicación sencilla:** Tema extra que el manual del curso no cubre: el cuaderno solo trae código, sin teoría. Aquí se documenta únicamente lo que el código muestra, el flujo de entrenamiento con SVC de scikit-learn, sin inventar teoría que las fuentes no explican.
- **Definición precisa y fórmula:** Tema adicional que no está en el manual PDF. El notebook de SVM es solo código: usa svm.SVC(C=10, random_state=42, probability=True), kernel por defecto 'rbf'. No hay teoría escrita de hiperplano separador, margen máximo, vectores de soporte ni catálogo de kernels.
- **Ejemplo o código:** Flujo: partición, estandarización, validación cruzada, entrenamiento, matriz de confusión y métricas, curva ROC y AUC.
- **Ojo (error común o límite):** Hueco de fuente: marcar la teoría de SVM como pendiente (James et al. o documentación de scikit-learn). No confundir ejecutar el código con explicar la teoría.
- **Comprueba:** ¿Qué te falta saber, además de que el código funciona, para explicar cómo SVM separa los grupos?
- **Fuente exacta:** 06 §3; Parte D.1 del prompt (erratas y huecos).

###### 5.3.a · Flujo de código SVM (SVC de sklearn)  (prioridad Media)

- **Explicación sencilla:** Sigue el mismo método que los modelos anteriores: separar datos de entrenamiento y prueba, estandarizar (poner los datos en una misma escala, porque SVM es sensible a ella), validar con KFold, entrenar, evaluar con matriz de confusión y métricas, y calcular curva ROC/AUC.
- **Definición precisa y fórmula:** Flujo del notebook: carga de iris; train_test_split(test_size=0.2, random_state=42); StandardScaler ajustado con entrenamiento; svm.SVC(C=10, random_state=42, probability=True); cross_val_predict con KFold(10, shuffle=True, random_state=42); fit del modelo final; predicción y evaluación sobre el test; ROC y AUC con predict_proba, label_binarize y roc_auc_score(multi_class='ovr').
- **Ejemplo o código:** X_stdr = stdr_trained.transform(X_training); model = algoritmos['SVM'].fit(X_stdr, y_training).
- **Ojo (error común o límite):** La estandarización antes de SVM es práctica estándar; el notebook no la explica con texto.
- **Comprueba:** ¿Por qué el escalador se ajusta solo con el entrenamiento?
- **Fuente exacta:** 06 §3.1 (notebook Clasificacion_SVM).

###### 5.3.b · Datos concretos verificables sobre la llamada a SVC  (prioridad Baja)

- **Explicación sencilla:** C=10 es un ajuste de regularización (freno al sobreajuste), pero el cuaderno no explica su efecto. Sin indicar kernel (forma de separar los datos), scikit-learn usa 'rbf'. probability=True permite obtener probabilidades, necesarias para ROC/AUC, a costa de más tiempo de entrenamiento.
- **Definición precisa y fórmula:** Clase sklearn.svm.SVC (Support Vector Classification). C = 10: parámetro de regularización o penalización por error de clasificación (el notebook no explica su efecto). kernel: no se indica, por defecto 'rbf' (hecho de la firma de sklearn, no del notebook). probability=True permite predict_proba (necesario para ROC y AUC) a costa de un entrenamiento interno adicional (calibración de Platt).
- **Ejemplo o código:** svm.SVC(C=10, random_state=42, probability=True).
- **Ojo (error común o límite):** Lo que el código muestra no equivale a la teoría del margen ni de los kernels.
- **Comprueba:** ¿Qué kernel usa SVC si no se indica ninguno?
- **Fuente exacta:** 06 §3.2.

###### 5.3.c · Conceptos NO cubiertos por las fuentes (SVM)  (prioridad Alta)

- **Explicación sencilla:** Ni el PDF ni el cuaderno explican qué es un hiperplano separador, el margen máximo, los vectores de soporte ni los tipos de kernel, salvo que 'rbf' es el valor por defecto. No se inventa esa teoría: falta fuente y hay que buscarla aparte si se necesita.
- **Definición precisa y fórmula:** Ni el PDF ni el notebook explican con texto: hiperplano separador, margen máximo, vectores de soporte ni el catálogo de kernels (lineal, polinómico, rbf...). No se rellena con contenido inventado; hace falta una fuente adicional.
- **Ejemplo o código:** Fuente sugerida por el propio resumen: James et al. (2013 y 2024), capítulo de SVM, o la documentación de scikit-learn.
- **Ojo (error común o límite):** Cualquier explicación teórica de SVM en el material o el video es ampliación externa y debe marcarse como tal.
- **Comprueba:** ¿Qué cuatro conceptos de SVM quedan sin fuente en el curso?
- **Fuente exacta:** 06 §3.3; Parte D.1 del prompt (erratas y huecos).


---

# PARTE D · Huecos de fuente, cierre y ejemplo de segmento

## D.1 Huecos de fuente y erratas conocidas (no rellenar con contenido inventado)

- **Tema 3 completo:** el manual PDF solo cubre los temas 1, 2, 4 y 5. La teoría del tema 3 está en el PowerPoint del profesor; el resumen `04` cubre solo lo práctico de los notebooks (cuyas celdas de texto son títulos).
- **3.5.c:** transformación lineal a tramos, negativo y ecualización del histograma solo aparecen nombradas en la diapositiva 16, sin fórmula ni código.
- **3.8.c, diámetro de Feret:** la diapositiva 35 define la *extensión* como proporción de píxeles de la región respecto a su *bounding box* y luego llama *diámetro de Feret* a un cociente entre el área y la *bounding box*: ambas descripciones apuntan a una proporción de áreas, mientras «diámetro» sugiere una longitud. **No enseñes ese cociente como definición verificada.** Muestra en pantalla «ojo: la diapositiva 35 parece contener una errata». (Ampliación externa, no del curso: en la literatura el diámetro de Feret suele ser la distancia máxima entre dos tangentes paralelas al contorno.) Si el profesor lo aclara, intégralo antes de cerrar el concepto.
- **3.7.c, Canny:** el comentario del notebook dice que `minValue` debe ser 3 veces mayor que `maxValue`, pero el código usa `255/3` para el mínimo y `255` para el máximo (un tercio): se sigue el código.
- **3.9.c, SURF:** el notebook no trae código de SURF.
- **5.3, SVM:** ni el manual ni el notebook desarrollan hiperplano separador, margen máximo, vectores de soporte ni kernels; solo se documenta lo que el código demuestra (`SVC(C=10)`, kernel `rbf` por defecto de sklearn). Si el video necesita esa teoría con rigor del curso, señala el límite y pide una fuente adicional (James et al. 2013/2024 o la documentación de scikit-learn); no confundas ejecutar el código con explicar la teoría.
- **5.1.b, sigmoide:** el resumen `06` transcribe la fórmula del notebook como `e^t / (1 + e^-t)` y la llama equivalente a la del PDF; no lo es. La forma estándar es `1 / (1 + e^-t) = e^t / (1 + e^t)`, que es la que usa el código del notebook.
- **4.3.h, KNN con Manhattan:** el manual imprime R2 = −0,727 en un resultado que dice «mejora un poco más»; probablemente el signo es un artefacto de la extracción del PDF. Se deja constancia sin corregirlo.
- **1.7.c, imputación:** el ejemplo del PDF llama a `transform` sin mostrar el `fit` previo (posible omisión editorial).
- **R2:** no se define en el capítulo de validación (tema 2); su fórmula está en el tema 4 (4.1.f). La curva ROC y el AUC no aparecen en el tema 2; están en 5.1.l y en el notebook de SVM.
- **Extracción de texto:** las ecuaciones, diagramas y figuras de los originales pueden perderse al extraer texto; ante una duda de fórmula o figura, pide el original al estudiante.

## D.2 Cierre: decidir qué modelo y qué métrica usar

**Primero define la salida.** Número continuo: regresión. Categoría: clasificación. Después determina qué error importa, qué datos estarán disponibles al predecir y cómo separarás entrenamiento de evaluación.

| Necesidad | Candidato inicial | Qué revisar |
|---|---|---|
| Relación aproximadamente aditiva y salida numérica | OLS | Residuos, outliers y estabilidad de coeficientes. |
| Curvatura en pocos atributos | Regresión polinómica | Grado, extrapolación y sobreajuste. |
| Casos similares con respuestas similares | KNN | Escala, distancia, número de vecinos y costo de predicción. |
| Probabilidad binaria con frontera lineal en atributos | Regresión logística | Calibración, umbral y errores por clase. |
| Reglas de decisión legibles | Árbol | Profundidad, estabilidad y tamaño de hojas. |
| Frontera potencialmente no lineal | SVC con RBF | Escalado, configuración y evaluación independiente. |

**Prueba de dominio.** Con un conjunto nuevo, explica sin consultar la guía: (1) cuál es la variable objetivo; (2) qué datos se conocen a tiempo; (3) dónde se aprende cada transformación; (4) cómo eliges hiperparámetros sin usar el test; (5) qué métrica responde al costo real; y (6) por qué el modelo elegido podría fallar. Si justificas los seis puntos y resuelves un ejemplo numérico nuevo, ya estás aplicando y analizando, no solo recordando nombres.

## D.3 Ejemplo de guion: `1.1.a Fase 1: Comprensión del negocio`

Este archivo muestra **un solo concepto**, como modelo de formato para la IA de video. Fuente: ficha 1.1.a de la Parte C (resumen `02`, apartado «Metodología CRISP-DM», detalle de la primera fase). La tienda es una escena ficticia para entender la idea; no es un dato del curso. El nombre técnico se pronuncia después de la primera pausa.

| Escena | Tiempo estimado | Narración | Visual y animación | Texto en pantalla |
|---|---|---|---|---|
| 1. Problema | 12 s | «Tengo una tienda. Algunos clientes dejan de volver. Quiero actuar, pero antes necesito decidir qué cambio busco y cómo sabré si lo logré». | Tienda gris. Clientes que dejan de volver en ámbar. Aparece una meta vacía en azul. | «¿Qué queremos lograr?» |
| 2. Intuición | 15 s | «Si empiezo a revisar datos sin esa meta, puedo encontrar cosas interesantes que no resuelvan el problema de la tienda. Primero acuerdo qué sería un resultado útil». | Varias pistas en gris; la meta elegida queda verde. Flecha desde la meta hacia las pistas. | «Primero: objetivo y criterio de éxito» |
| 3. Única pregunta de comprensión | Pausa libre | «Pausa el video y responde con tus palabras: ¿por qué necesitamos acordar el objetivo antes de revisar los datos?» | Pantalla quieta. Pregunta en azul. | La misma pregunta. |
| 4. Respuesta y nombre del curso | 18 s | «Porque los datos y el trabajo técnico deben servir a una meta clara. En el curso, este primer paso se llama **comprensión del negocio**, la primera fase de **CRISP-DM**». | Meta en verde. Aparece el rótulo formal unido a la escena de la tienda. | «Comprensión del negocio» |
| 5. Procedimiento | 25 s | «Aquí se hace algo más preciso: se define el objetivo y cómo reconocer el éxito; se revisa la situación actual; se traduce la meta en una tarea que puedan abordar los datos; y se organiza el trabajo en un plan. Esa meta se vuelve a consultar durante el proyecto». | Cuatro tarjetas aparecen una a una. Ámbar: tarjeta activa. Verde: tarjeta ya explicada. Una flecha de retorno desde el final hacia la meta. | «Objetivo → situación → meta técnica → plan» |
| 6. Error común y nota | 15 s | «Error común: creer que esta fase consiste en empezar a entrenar un modelo. Falta decidir para qué se trabajará. Nota: primero defino el resultado útil; después decido qué datos y tareas necesito». | La tarjeta «modelo» en gris espera detrás de la meta en verde. | «Primero el resultado útil» |
| 7. Caso nuevo | Pausa libre | «Un negocio quiere reducir las entregas tardías. Antes de mirar sus registros, explica qué decisión corresponde a esta primera fase». | Nuevo negocio en gris y problema en ámbar. Sin respuesta visible. | «Resuélvelo sin mirar la solución» |
| 8. Solucionario, al final del video | 15 s | «Primero se aclara qué quiere mejorar el negocio y cómo sabrá que mejoró. Después se revisa la situación, se traduce la meta a una tarea técnica y se prepara un plan. Si llegaste aquí tras resolverlo por tu cuenta, informa tu respuesta para comprobar si este concepto está firme». | Aviso previo de pausa. Luego las cuatro tarjetas pasan a verde. | «Compara con tu respuesta» |

**Reporte para el siguiente video:** `1.1.a | bien / a medias / mal | lo que dije | dónde me trabé | resolví el caso nuevo sin mirar: sí / no`.

No marques «Firme» automáticamente. La IA debe revisar la respuesta del estudiante al caso nuevo. Si falló, primero debe darle oportunidad de encontrar su error y después reenseñar solo el paso que causó la confusión.

## D.4 Plantilla del reporte de verificación y estado de sesión

```text
Reporte del video [código y título]
concepto | respondí bien / mal / a medias | qué dije | dónde me trabé | resolví el caso nuevo sin mirar: sí / no
...
Estado de sesión
Firmes: ...
Débiles: ...
Pendientes: ...
Dónde retomar: ...
```

# 05 — Rohrer, Dedrick, Hartwig & Cheung (2019)

> **PDF asociado:** `2019-rohrer.pdf`

## Ficha bibliográfica

| Campo | Valor |
|---|---|
| **Título** | *A Randomized Controlled Trial of Interleaved Mathematics Practice* |
| **Autores** | Doug Rohrer, Robert F. Dedrick, Marissa K. Hartwig, Chi-Ngai Cheung |
| **Institución** | University of South Florida |
| **Año** | 2019 |
| **Revista** | *Journal of Educational Psychology* |
| **Tipo** | Ensayo controlado aleatorizado por clústeres, en aulas reales (54 clases de 7º grado, 787 alumnos, 15 profesores, 5 escuelas) |

## Pregunta de investigación

¿Funciona el *interleaving* (mezclar tipos de problema) mejor que el *blocking* (bloquear por tipo) en condiciones **reales de aula**, durante meses, con profesores sin entrenamiento en la técnica? Este estudio complementa a `01_Brunmair_Richter_2019_Interleaving.md` con el experimento de campo más grande y riguroso hecho hasta la fecha sobre interleaving en matemáticas.

## Hallazgo principal

Tras 4 meses de tareas (bloqueadas o entrelazadas) y una revisión entrelazada común a ambos grupos, un examen sorpresa un mes después dio:

- Grupo entrelazado: **61% correcto**
- Grupo bloqueado: **38% correcto**
- Efecto grande: **d = 0.83** (positivo en los 15 profesores, sin excepción)

## Por qué el efecto es tan grande (mecanismo)

El interleaving combina **tres** estrategias potentes a la vez:

1. **Elegir estrategia, no solo ejecutarla**: con bloqueo el alumno ya sabe qué fórmula usar antes de leer el problema (fluidez ilusoria); con interleaving debe decidir cuál aplicar, igual que en un examen acumulativo real.
2. **Spacing implícito**: mezclar A-B-C-A-B-C espacía automáticamente la práctica de cada tema (frente a A-A-A-B-B-B).
3. **Retrieval practice implícito**: con bloqueo, la fórmula usada está "a la vista" (fue la del problema anterior); con interleaving hay que recuperarla de memoria.

## Caveats importantes (los propios autores los remarcan)

1. **Toma más tiempo**: los profesores reportaron que las tareas entrelazadas tardaban más en completarse y en corregirse.
2. **El beneficio es menor con demoras de examen cortas** (2-5 días) — se necesita un delay razonable para que se note.
3. **No sustituye el bloqueo inicial**: los alumnos entrelazados de este estudio ya habían recibido algo de práctica bloqueada al aprender la habilidad por primera vez con su profesor, antes de las hojas de práctica del experimento. **No mezclar desde el primer contacto con un concepto nuevo.**
4. **Requiere feedback correctivo**: a los alumnos se les mostraba la solución y se les pedía corregir sus errores; sin esto, el efecto podría no sostenerse.

## Feasibility (dato práctico)

Los profesores, **sin entrenamiento previo**, pudieron implementar las tareas entrelazadas sin cambiar su forma de enseñar. La mayoría las recomendaría a otros profesores, aunque los alumnos las percibieron "ligeramente más difíciles y lentas" que las bloqueadas — coherente con que el interleaving se siente peor durante la práctica aunque funcione mejor a largo plazo (el mismo patrón que Rohrer & Taylor 2007 y Taylor & Rohrer 2010 documentan en la práctica del laboratorio).

## Principios extraíbles para estudio

- **[P18]** El entrelazado no es gratis: cuesta más tiempo por problema. Vale la pena igual, pero no subestimar el tiempo que toma diseñarlo/resolverlo.
- **[P19]** Nunca entrelazar la primerísima exposición a un concepto — primero un mínimo de práctica bloqueada con feedback, luego mezclar.
- **[P20]** El beneficio del entrelazado se nota más con demoras de examen largas (semanas), no con quices inmediatos al día siguiente.
- **[P21]** El feedback correctivo (mostrar la solución y pedir corregir el error) parece ser un ingrediente necesario, no opcional, del entrelazado.

## Aplicación a Matemáticas para IA (Máster VIU)

| Situación | Estrategia |
|---|---|
| Vas a aprender diagonalización por primera vez | Bloquea: resuelve varios ejercicios de diagonalización antes de mezclar con otros temas |
| Ya viste diagonalización, SVD, LU y Cholesky por separado | Entrelázalas ahora — obliga a decidir cuál factorización usar según la matriz dada |
| Resuelves un ejercicio entrelazado y sientes que te cuesta más | Normal — el propio estudio lo confirma; el costo en fluidez durante la práctica es lo que después se traduce en mejor retención |
| Vas a hacer un simulacro de examen | Que el simulacro mezcle temas (lógica, álgebra, cálculo) igual que el examen real — así entrenas la discriminación de estrategia, no solo la ejecución |

## Una frase para llevarte

> **"En un aula real, con profesores sin entrenar, mezclar los tipos de problema duplicó el porcentaje de aciertos en un examen sorpresa un mes después (61% vs 38%) — pero solo funciona si antes hubo algo de práctica bloqueada y hay feedback correctivo."**

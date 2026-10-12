# 03 — Hodds, Alcock & Inglis (2014)

> **PDF asociado:** `JRME_SelfExpl_Paper.pdf`

## Ficha bibliográfica

| Campo | Valor |
|---|---|
| **Título** | *Self-Explanation Training Improves Proof Comprehension* |
| **Autores** | Mark Hodds, Lara Alcock, Matthew Inglis |
| **Institución** | Mathematics Education Centre, Loughborough University |
| **Año** | 2014 |
| **Revista** | *Journal for Research in Mathematics Education* (JRME) |
| **Tipo** | 3 experimentos: aleatorizado + eye-tracking + longitudinal |
| **Tamaño de efecto principal** | **d = 0.95** (efecto GRANDE) |

---

## Pregunta de investigación

¿Puede entrenarse a estudiantes universitarios para **comprender mejor las demostraciones matemáticas** con una intervención mínima? Sí — un folleto de **15-20 minutos** mejora significativamente la comprensión.

---

## Hallazgos clave

| Experimento | Diseño | Resultado |
|---|---|---|
| **1** | Aleatorizado, folleto vs. control | Mejora en comprensión: **d = 0.95** |
| **2** | Eye-tracking | El grupo entrenado mueve más la mirada **entre líneas** (lectura experta) |
| **3** | Intervención en clase real | 15 min en clase mejora la comprensión, **efecto persiste en el tiempo** |

> El estudio 2 confirma el mecanismo: los entrenados leen como leen los matemáticos — saltan adelante y atrás, no en línea recta.

---

## La técnica: las 4 preguntas de self-explanation

Después de leer **cada línea** de una demostración o teoría densa, hazte estas 4 preguntas (en voz alta o por escrito):

1. **¿Entiendo las ideas usadas en esta línea?**
2. **¿Por qué se ha usado esta idea AQUÍ y no otra?**
3. **¿Cómo se enlaza esta idea** con otras del mismo proof, con otros teoremas o con mi conocimiento previo?
4. **¿La self-explanation que generé responde** a las preguntas que me estaba haciendo?

---

## Categorías de comentarios (codificación del estudio 1, basado en Ainsworth & Burcham 2007)

### Lo que SÍ funciona (explanations)

| Tipo | Definición |
|---|---|
| **Principle-based** | Apoya la explicación en una **definición o teorema** previo |
| **Goal-driven** | Relaciona el paso con la **estructura global** del proof |
| **Noticing coherence** | Conecta con una idea **usada antes** en el mismo proof |

### Lo que NO funciona (non-explanations)

| Tipo | Definición | Ejemplo |
|---|---|---|
| **Paraphrasing** | Repetir lo mismo con otras palabras | "p y q tienen que ser enteros" (parafrasea la definición de integer) |
| **Monitoring** | Decir si entiendes o no | "OK, esto lo entiendo" / "No entiendo esto" |
| **False explanation** | Explicación incorrecta | Cualquier interpretación errónea |
| **No comment** | Ningún comentario | (silencio) |

---

## Ejemplo del paper

**Teorema**: 3.14 es un número racional.
**Demostración**: Es racional ↔ existen enteros p, q con q ≠ 0 tal que x = p/q. Tomamos p = 314, q = 100. Ambos son enteros y 100 ≠ 0. Por definición, 3.14 es racional.

| Tipo de respuesta | Ejemplo |
|---|---|
| ✗ **Parafraseo** | "Tanto p como q tienen que ser enteros positivos o negativos." |
| ✗ **Monitoreo** | "OK, entiendo que el proof pone p=314 y q=100." |
| ✓ **Self-explanation real** | "p=314 y q=100 porque son enteros y p/q = x = 3.14. La demostración también podría haber usado p=628 y q=200. Esto **cumple la definición** de número racional, por eso completa la prueba." |

---

## Por qué funciona (mecanismos)

El eye-tracking del Experimento 2 muestra que tras el entrenamiento:
- **Aumentan los saccades entre líneas** → vuelves a líneas anteriores para conectar.
- **Aumenta la duración de las fijaciones** → más procesamiento profundo.
- El estudiante entrenado **lee como un matemático**, no como un texto narrativo.

---

## Principios extraíbles para estudio

- **[P11]** Siempre explicarte cada línea con los **porqués**, no parafrasees.
- **[P12]** Conectar **explícitamente** cada paso con definiciones y teoremas previos.
- **[P13]** Saltar la vista adelante y atrás por una demostración es **lectura experta**.
- **[P14]** Intervenciones de **solo 15 minutos** pueden tener efecto duradero.

---

## Aplicación a Matemáticas para IA (Máster VIU)

| Situación | Cómo aplicar |
|---|---|
| Manual VIU enuncia un teorema (ej. p → q ≡ ¬p ∨ q) | Aplica las 4 preguntas a cada línea del teorema y su demostración |
| Definición nueva (ej. álgebra de Boole) | Conecta cada propiedad con una definición previa que ya conoces |
| Lees y crees entender pero no sabes explicarlo | Estás monitoreando, no explicando. Vuelve y conecta con definiciones |
| Sigues una demostración línea por línea sin volver atrás | Estás leyendo como novato. Salta hacia atrás cuando una línea no encaje |

---

## Una frase para llevarte

> **"15 minutos al día con las 4 preguntas (idea / porqué / enlace / responde) tienen el efecto más grande documentado en comprensión de demostraciones."**

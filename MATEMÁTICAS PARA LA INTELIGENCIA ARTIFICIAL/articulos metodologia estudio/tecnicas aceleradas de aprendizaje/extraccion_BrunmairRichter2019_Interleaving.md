# Extracción: Brunmair & Richter (2019) — Meta-análisis del interleaving

## Datos bibliográficos

- **Título**: "Similarity matters: A meta-analysis of interleaved learning and its moderators"
- **Autores**: Matthias Brunmair & Tobias Richter
- **Afiliación**: University of Würzburg (Department of Psychology IV)
- **Año**: 2019 (manuscrito aceptado; "in press" en el PDF, © 2019 American Psychological Association)
- **Journal**: *Psychological Bulletin*
- **DOI**: 10.1037/bul0000209
- **Financiación**: beca del estado de Hessen (LOEWE), iniciativa de investigación "Desirable difficulties in learning"
- **Datos y script R disponibles en**: Open Science Framework, https://osf.io/7u253/
- **Palabras clave**: blocking, category learning, discrimination, inductive learning, interleaving effect

---

## 1. Objetivo y definición operacional de "interleaving"

### Objetivo
Cuantificar la magnitud del efecto del interleaving (aprendizaje intercalado) sobre el aprendizaje inductivo, probar su generalización a través de distintos escenarios y materiales de aprendizaje, y examinar moderadores que pudieran enriquecer los modelos teóricos del aprendizaje intercalado. Objetivo práctico: explorar en qué condiciones el interleaving puede usarse para diseñar aprendizaje inductivo en entornos escolares con materiales educativos realistas.

### Definición operacional (crítica para entender el alcance del meta-análisis)
> "Definimos el efecto de interleaving como un efecto positivo de una condición de aprendizaje inductivo intercalada frente a una bloqueada sobre el rendimiento en una tarea posterior de discriminación o clasificación de categorías."

- **Condición intercalada (interleaved)**: los ítems de una categoría se presentan intercalados con ítems de al menos otra categoría.
- **Condición bloqueada (blocked)**: todos los ítems de una categoría se presentan consecutivamente antes de pasar a los ítems de otra categoría.
- El rendimiento en la prueba criterio debe depender del **aprendizaje inductivo** (no basta con memoria).
- El efecto inverso (blocking > interleaving) se denomina explícitamente **"blocking effect"**.

### Qué excluyeron deliberadamente (y por qué)
- **Estudios de contraste "leer vs. actuar"** (p. ej. Duggan & Payne, 2001): no requieren discriminación de categorías ni aprendizaje inductivo.
- **Estudios del efecto de espaciamiento (spacing effect)**: en estos se repiten exactamente los mismos ítems (p. ej. mismas listas de palabras) en formato masivo o espaciado; no implican adquisición de estructuras de categorías.
- **Estudios de interferencia contextual (contextual interference)** en aprendizaje motor (tiros de baloncesto, tareas de "rotary pursuit"): excluidos porque el aprendizaje motor es procedimental e implícito, mientras que el aprendizaje inductivo de categorías es declarativo y explícito. **Excepción**: sí se incluyeron estudios de interferencia contextual que cumplían la definición de interleaving (comparación intercalada vs. bloqueada sobre discriminación/clasificación de categorías), p. ej. de Croock & van Merriënboer (2007), Rau et al. (2012, 2013).

---

## 2. Metodología del meta-análisis

### Búsqueda
- Bases de datos: PsycINFO y Google Scholar (literatura publicada); WorldCat y ProQuest (literatura gris).
- Cadenas de búsqueda: interleav*, block*, random, schedul*, pract*, effect.
- Revisión adicional de las listas de referencias de las revisiones de Rohrer (2012) y Carvalho & Goldstone (2015b), incluido su material suplementario (Carvalho & Goldstone, 2015c).
- Periodo cubierto: hasta el 30 de junio de 2018.
- **176 estudios potencialmente elegibles** fueron cribados.

### Criterios de inclusión (los tres deben cumplirse)
(a) El diseño incluye una condición de estudio intercalada y una bloqueada (diseño intra- o entre-sujetos).
(b) El intervalo de retención, la medida de resultado, el tiempo por ítem, el intervalo temporal entre ítems y el número de ítems por categoría son **iguales** entre la condición intercalada y la bloqueada.
(c) El estudio reporta los valores estadísticos necesarios para calcular el tamaño de efecto (o los autores los proporcionaron al ser contactados).

Estudios con características de muestra/ítems atípicas o diseños especiales no se excluyeron, sino que se codificaron como moderadores. La dependencia entre efectos (muestras dependientes) se abordó mediante meta-análisis multinivel.

### Muestra final
- **59 artículos** que reportan **238 tamaños de efecto** anidados en **158 muestras**, con **N = 8,466 participantes**.
- Estudios publicados entre 2003 y 2018.
- **71 conjuntos distintos de materiales de aprendizaje** identificados.
- Solo 97 tamaños de efecto (62 muestras) reportaron la edad media de los participantes (edad media global = 21.32 años).

### Cálculo del tamaño de efecto
- Se calcularon diferencias entre condición bloqueada e intercalada.
- Efectos entre-grupos → **Cohen's d**; efectos intra-grupo → **Cohen's dav** (que ignora la correlación entre medidas y usa la desviación estándar promedio; Lakens, 2013).
- Corrección de Hedges (1981) para convertir d en **Hedges' g** (corrige el sesgo de sobreestimación en muestras pequeñas). g se interpreta igual que d.
- Cuando un estudio reportaba varios efectos dependientes y solo uno encajaba con la pregunta de investigación, se incluyó solo ese. Ejemplo: de Kornell & Bjork (2008) solo se usó el primer bloque de prueba (para evitar confundir con efectos de retroalimentación repetida).

### Estrategia estadística
- **Meta-análisis multinivel** (por la estructura jerárquica: varios tamaños de efecto por estudio/muestra).
- **Modelo de efectos aleatorios** para el efecto global; **modelos de efectos mixtos** para el análisis de moderadores (moderadores como efectos fijos).
- Estadísticos: **I²** y **Q** (heterogeneidad), **Q_B** (Cochran, homogeneidad de efectos), **Q_M** (varianza explicada por el modelo), **τ²** (varianza total), **R²** (Raudenbush, 2009; adaptado a multinivel según Cheung, 2014, distinguiendo R²_between y R²_within).
- Análisis de outliers: procedimiento paso a paso usando residuos estudentizados eliminados, valores DFFITS, distancia de Cook y valores hat (Viechtbauer & Cheung, 2010). **Se excluyeron 12 outliers de 5 estudios** de todos los modelos principales (no del análisis de sensibilidad).
- Software: paquete **metafor** en R (Viechtbauer, 2010).
- Evaluación de la calidad de las materiales: **5 evaluadores** puntuaron 71 conjuntos de materiales en similitud intra-categoría, similitud entre-categorías, complejidad, familiaridad y curiosidad (esta última descartada por baja fiabilidad interjueces). Fiabilidad (Cronbach's α): similitud intra = .91, similitud entre = .92, complejidad = .92, familiaridad = .94, curiosidad = .72.

---

## 3. Efecto global del interleaving

> **k = 238 tamaños de efecto; g = 0.42; p < .001; IC 95% [0.34, 0.50]** — efecto moderado y positivo.

Análisis de sensibilidad:
- Modelo de dos niveles con solo efectos independientes: k = 138, g = 0.43, p < .001, IC 95% [0.35, 0.51] (prácticamente igual).
- Modelo que ignora la estructura anidada (incluyendo efectos dependientes sin corrección): k = 238, g = 0.36, p < .001, IC 95% [0.29, 0.42] — **el efecto queda sesgado a la baja** cuando no se corrige por dependencia. Las muestras que aportaron más de un tamaño de efecto tuvieron un g medio significativamente menor que las que aportaron solo uno (Q_M = 9.7, p < .001).
- Heterogeneidad global: **I² = 77.3%, τ² = 0.20** (heterogeneidad sustancial entre muestras).

---

## 4. Moderadores — el corazón del paper

### 4.1 Tipo de material de aprendizaje (Tabla 2)

Diferencias significativas entre tipos de material: **Q_B = 52.64, p < .001**.

| Material | k | g | p | IC 95% | I²_between | I²_within |
|---|---|---|---|---|---|---|
| **General (overall)** | 238 | **0.42** | <.001 | [0.34, 0.50] | 77.3% | 0.0% |
| **Pinturas (paintings)** | 70 | **0.67** | <.001 | [0.57, 0.77] | 43.4% | 27.1% |
| Fotografías naturalistas | 19 | 0.35 | .001 | [0.16, 0.55] | 56.1% | 0.0% |
| Imágenes artificiales | 63 | 0.31 | <.001 | [0.18, 0.44] | 73.7% | 0.0% |
| Textos expositivos | 25 | 0.21 (n.s.) | .119 | [-0.06, 0.47] | 74.4% | 0.0% |
| Tareas matemáticas | 45 | 0.34 | .005 | [0.11, 0.57] | 76.9% | 0.0% |
| **Palabras (words)** | 13 | **-0.39** | .005 | [-0.64, -0.14] | 18.1% | 39.7% |
| Sabores (tastes) | 3 | 0.57 (n.s.) | .24 | [-0.11, 1.26] | 36.9% | — |

Puntos clave:
- El efecto más alto es para **pinturas** (g=0.67) y en general para **estímulos visuales** (pinturas, fotos naturalistas, imágenes artificiales) — todos positivos y significativos.
- **Palabras** es el único material con efecto **negativo y significativo**: aquí bloquear es mejor que intercalar.
- **Textos expositivos** y **sabores** no alcanzan significación (aunque las estimaciones puntuales son positivas).
- **Tareas matemáticas**: efecto positivo pero pequeño (g=0.34), significativo.
- Heterogeneidad sustancial dentro de casi todos los tipos de material (I² between 43–77%), lo que sugiere que hacen falta más moderadores para explicar la variación.

### 4.2 Similitud entre y dentro de categorías — el moderador central ("Similarity Matters")

Este es el hallazgo que da título al paper. Basado en las puntuaciones de los 5 evaluadores (variables continuas centradas en la media):

- **Similitud ENTRE categorías** (between-category similarity): influencia **positiva** sobre el efecto de interleaving. Cuanto más se parecen las categorías entre sí (es decir, cuanto más difíciles son de discriminar), **mayor es el beneficio de intercalar**.
- **Similitud DENTRO de categorías** (within-category similarity): influencia **negativa** sobre el efecto de interleaving. Cuanto más se parecen los ejemplares dentro de una misma categoría, **menor es el beneficio de intercalar** (puede incluso revertirse a favor del bloqueo).

Estimaciones de la meta-regresión multinivel (Tabla 3, tres modelos anidados + modelo con outliers incluidos):

| Predictor | Modelo 1 | Modelo 2 | Modelo 3 | Modelo Outlier |
|---|---|---|---|---|
| Intercepto | 0.28* | 0.33** | 0.54*** | 0.52*** |
| Similitud intra-categoría | — | -0.33*** | -0.17* | -0.07 (n.s.) |
| Similitud entre-categorías | — | 0.41*** | 0.22* | 0.08 (n.s.) |
| Complejidad | — | 0.06 (n.s.) | 0.12* | 0.15** |
| Familiaridad | — | 0.19*** | 0.20*** | 0.20** |

(El Modelo 2 añade características cuantitativas del material sin controlar por tipo de material; el Modelo 3 añade el tipo de material como covariable, lo que **atenúa** los coeficientes de similitud — es decir, parte de su efecto se explica por diferencias entre tipos de material, pero el patrón de signos se mantiene).

**Análisis de sensibilidad (Tabla 4)** — robustez del patrón de similitud a través de subconjuntos de datos:

| Predictor | Todos los estudios | Solo independientes | Solo estudiantes | Solo material visual | Solo imágenes artificiales |
|---|---|---|---|---|---|
| Similitud intra | -0.16* | -0.12 (n.s.) | -0.18* | -0.29** | -0.28* |
| Similitud entre | 0.20* | 0.18* | 0.28** | 0.34*** | 0.38** |
| Complejidad | 0.12* | 0.11* | 0.11* | 0.18*** | 0.22*** |
| Familiaridad | 0.18** | 0.20** | 0.26*** | 0.26** | 0.14 (n.s.) |

Los propios autores subrayan: *"the pattern of effects was very stable across different models and samples"* — el patrón de similitud (entre-categorías ↑ favorece interleaving; intra-categoría ↑ lo perjudica) se mantiene consistentemente en todos los subconjuntos analizados, y es el hallazgo teórico más robusto de todo el meta-análisis.

- **Familiaridad** del material tuvo la mayor influencia de todas las características del material en todos los modelos que incluían el tipo de material (coeficiente positivo: materiales más familiares → mayor efecto de interleaving).
- **Complejidad**: alguna evidencia de que la mayor complejidad del material favorece el interleaving, pero resultados inconsistentes entre modelos/muestras.

### 4.3 Tipo de material como predictor dummy (Tabla 3, referencia = pinturas)

Incluso controlando por similitud/complejidad/familiaridad, todos los demás tipos de material siguen siendo significativamente inferiores a las pinturas:

- Textos expositivos: b = -0.56, SE = 0.18, p = .001 (el peso negativo más alto)
- Palabras: b = -0.48, SE = 0.23, p = .014
- Tareas matemáticas: b = -0.43, SE = 0.18, p = .004
- Fotografías naturalistas: b = -0.22 (n.s.)
- Imágenes artificiales: b = -0.20 (n.s.)

El tipo de material añadió un 4.0% de varianza explicada adicional respecto al Modelo 2 (sin tipo de material).

R² entre estudios de los modelos completos: Modelo 1 = .05, Modelo 2 = .46, Modelo 3 = .50, Modelo Outlier = .44 (R² dentro de estudios = 1 en todos los modelos).

### 4.4 Edad (análisis adicional, no incluido en el modelo principal por datos limitados)

- Solo 97 tamaños de efecto / 62 muestras reportaron edad media (rango final analizado: 9.5 a 37 años; se excluyó un estudio con media de 77 años por su distancia del resto).
- **Muestra total** (controlando material y características del material): k=85, b=-0.04, SE=0.01, p<.001; la edad explicó un 13.4% de varianza adicional; R²_between = 58.4%.
- **Solo material visual**: k=42, b=-0.03, SE=0.01, p<.001; edad explicó 30.9% de varianza adicional; R²_between = 75.8%.
- **Solo estudiantes universitarios**: k=49, b=-0.07, SE=0.05, p=.19 (n.s.); R²_between = 78.3%.
- **Conclusión**: el interleaving funciona mejor en muestras más jóvenes (coeficiente negativo con edad como predictor continuo). Esto contrasta con la literatura primaria previa, que era inconsistente al respecto (Kornell et al., 2010, sin efecto; Lin et al., 2016, sí efecto).

### 4.5 Tipo de muestra (estudiantes vs. no estudiantes)

Los efectos de interleaving fueron **mayores en muestras de estudiantes universitarios puros** que en muestras no estudiantiles, incluso controlando por características del material y tipo de material (significativo en Modelo 3: b=0.17*, y en Modelo Outlier: b=0.19*; también significativo en casi todos los subconjuntos de la Tabla 4, excepto donde no se pudo estimar).

### 4.6 Espaciamiento temporal (temporal spacing) — análisis adicional (k=17 estudios que compararon directamente)

Q_M = 9.64, p = .008 — efecto significativo del espaciamiento:
- **Sucesión inmediata** (<2 seg entre ítems): g = 0.73, IC 95% [0.51, 0.95] — el efecto más fuerte.
- **Ítems espaciados temporalmente** (10-30 seg): g = 0.22, IC 95% [-0.13, 0.45] — **no significativo**.
- **Presentación con distractores** entre ítems: g = 0.51, IC 95% [0.07, 0.96] — significativo.

Esto apoya directamente la hipótesis del contraste discriminativo: el interleaving funciona cuando los ítems están próximos en el tiempo; espaciarlos anula el efecto.

### 4.7 Otros moderadores analizados SIN efecto significativo

- **Diseño** (intra- vs. entre-sujetos): sin efecto.
- **Intervalo de retención** (corto <20 min vs. más largo): sin efecto en la meta-regresión. (Nota: un estudio primario aislado, Rohrer et al. 2014b, sí encontró interacción: g más alto a 30 días [d=0.79] que a 1 día [d=0.42], pero esto no se replicó como moderador global).
- **Presentación simultánea vs. sucesiva**: sin efecto significativo en la meta-regresión (b=0.09, n.s. en Modelo 3). Análisis de seguimiento (k=26 estudios con ambas condiciones): simultánea g=0.44 [0.24,0.64] vs. sucesiva g=0.29 [0.09,0.50], diferencia no significativa (Q_M=1.0, p=.31).
- **Retención vs. transferencia**: sin efecto en la meta-regresión. Análisis de seguimiento (k=64 efectos de 31 estudios con ambos tipos de prueba): Q_M=0.56, p=.45, sin diferencia. Esto es relevante porque demuestra que el interleaving mejora también el rendimiento en ítems nuevos (transferencia), no solo el recuerdo de ítems ya vistos — apoya que fomenta aprendizaje inductivo genuino, no solo aprendizaje asociativo.
- **Publicado vs. no publicado**: sin evidencia de efecto moderador.
- **Aprendizaje intencional vs. incidental**: el aprendizaje incidental tuvo un impacto **negativo** en la magnitud del efecto, pero solo alcanzó significación en el modelo con outliers incluidos (b=-0.55**, p<.01); en los demás modelos no fue significativo (b entre -0.37 y -0.52, n.s.), probablemente por falta de potencia estadística — **solo 8 estudios** usaron práctica intercalada combinada con aprendizaje incidental.

---

## 5. Mecanismos explicativos propuestos

1. **Hipótesis del contraste discriminativo (discriminative-contrast hypothesis)** (Kang & Pashler, 2012): el espaciamiento temporal entre ítems dificulta el aprendizaje inductivo en condiciones intercaladas y no aporta ventaja en condiciones bloqueadas. Una presentación intercalada con poco o ningún tiempo entre ítems promueve **contrastes discriminativos** entre ítems consecutivos, lo que beneficia el aprendizaje inductivo.

2. **Marco del sesgo atencional / teoría secuencial de la atención (attentional bias framework / sequential theory of attention)** (Carvalho & Goldstone, 2015b, 2017) — **el marco teórico central que el meta-análisis confirma**: refina la hipótesis anterior añadiendo que una presentación intercalada resalta las **diferencias** entre ítems, mientras que una presentación bloqueada resalta las **similitudes**. Por tanto:
   - El interleaving es mejor cuando las categorías tienen **baja discriminabilidad** (los ejemplares se parecen mucho entre sí, alta similitud entre categorías) — porque aprender la estructura de categorías depende de encontrar las diferencias que las discriminan.
   - El blocking es mejor cuando las categorías tienen **alta discriminabilidad pero baja similitud interna** (ejemplares muy distintos entre sí dentro de la misma categoría) — porque aprender la estructura depende de encontrar las características compartidas dentro de cada categoría.
   - Los resultados del meta-análisis (mayor efecto de interleaving cuanto mayor la similitud entre categorías y menor la similitud dentro de categorías) son directamente consistentes con esta teoría.

3. **Hipótesis "massing-aids-induction"** (término acuñado por Kornell & Bjork, 2008, quienes NO la respaldan): el bloqueo mejora el aprendizaje inductivo al facilitar el reconocimiento de similitudes entre ítems no idénticos dentro de una categoría. Esta hipótesis **no puede explicar** los efectos positivos de interleaving, pero sí ayuda a interpretar casos donde el interleaving falla o perjudica (p. ej. Sorensen & Woltz, 2016, con categorías conceptuales definidas por múltiples rasgos y palabras como ítems).

Conclusión de los autores en la Discusión: los hallazgos son consistentes sobre todo con la **teoría secuencial de la atención**, y también apoyan la **hipótesis del contraste discriminativo** en lo referente al papel del espaciamiento temporal.

---

## 6. Cuándo el interleaving NO ayuda o perjudica (según los propios datos)

- **Palabras** como material de aprendizaje: efecto **negativo y significativo** (g=-0.39), es decir, bloquear es mejor. Ejemplos citados de la literatura primaria: reglas de pronunciación con palabras francesas (Carpenter & Mueller, 2013) y conceptos definidos por múltiples rasgos con palabras como ejemplares (Sorensen & Woltz, 2016). Los autores advierten, no obstante, que hay pocos estudios con palabras y que el efecto negativo podría deberse al tipo de tarea o a las categorías específicas usadas, no a las palabras per se.
- **Textos expositivos**: efecto global no significativo (g=0.21, n.s.); resultados mixtos en la literatura primaria (p. ej. efecto positivo en Zulkiply & Burt 2013a con casos clínicos psicopatológicos, pero nulo en Dobson 2011 con textos sobre sistema inmune/reproducción).
- **Sabores**: no significativo, pero basado en solo 3 tamaños de efecto (poca potencia).
- **Alta similitud dentro de categorías**: reduce o revierte el beneficio del interleaving.
- **Baja similitud entre categorías** (categorías fáciles de discriminar): reduce el beneficio del interleaving.
- **Espaciamiento temporal entre ítems** (10-30 seg): elimina el efecto (g=0.22, n.s.) frente a la sucesión inmediata (g=0.73).
- **Aprendizaje incidental** (sin intención de aprender): tendencia a reducir o revertir el efecto (aunque con poca potencia estadística, solo 8 estudios).
- **Categorías fácilmente discriminables, aprendizaje basado en reglas, o condiciones de aprendizaje pasivo**: mencionado en la introducción como condiciones donde el efecto de interleaving fue "frágil" o inconsistente en estudios primarios (Zulkiply & Burt, 2013b; Noh, Yan, Bjork & Maddox, 2016; Carvalho & Goldstone, 2015a) — no se traduce en una tabla de tamaños de efecto agregados, pero contextualiza los hallazgos de los moderadores.
- **Interleaving mal aplicado en tareas matemáticas multidimensionales**: cuando se intercala una dimensión (p. ej. tipo de tarea) mientras se bloquea otra (p. ej. tipo de representación gráfica), puede tener efectos positivos en una dimensión y negativos en otra (Rau et al., 2013, citado en la Discusión).
- **Edad avanzada** y **muestras no estudiantiles**: asociadas a efectos de interleaving más pequeños.

---

## 7. Recomendaciones prácticas explícitas de los autores

Cita directa de la sección de implicaciones prácticas:

- El interleaving funciona bien con **estímulos visuales naturalistas** (pinturas o fotografías naturalistas), especialmente cuando los estímulos son **complejos**, las categorías son **difíciles de discriminar**, y la similitud de los ejemplares **dentro** de cada categoría es **baja**. Materiales de ejemplo en los estudios incluidos: pinturas naturalistas, fotos de aves y mariposas, fotos de rostros humanos.
- Dado que las estimaciones se basan en un modelo de efectos aleatorios, los autores confían en que estas estimaciones se pueden generalizar a la población de estímulos visuales de la que se extrajeron las muestras.
- El interleaving puede ser una **herramienta didáctica muy útil en disciplinas** como historia del arte, biología, medicina, geología y otras disciplinas que requieren diferenciar y clasificar estímulos visuales naturalistas complejos.
- Para **imágenes artificiales** (diagramas lógicos o esquemáticos que ilustran procesos abstractos, modelos teóricos, objetos geométricos o elementos químicos): el interleaving puede favorecer el aprendizaje inductivo, **pero** en la medida en que esos diagramas ya estén diseñados para reducir la complejidad y resaltar las diferencias entre conceptos, el interleaving puede ser menos beneficioso.
- Cita textual: *"We are reluctant to recommend interleaving for learning materials such as mathematical tasks, expository texts, grammar rules, foreign languages or words (i.e., category names). When interleaving is used with these materials, it could even impede learning compared to a blocked presentation of items."* — Los autores son explícitamente cautelosos/reacios a recomendar el interleaving para: **tareas matemáticas, textos expositivos, reglas gramaticales, idiomas extranjeros y palabras** (nombres de categorías); con estos materiales el interleaving incluso podría perjudicar el aprendizaje frente al bloqueo.
- Declaración de significancia pública (resumen para no-especialistas): el interleaving es prometedor para aplicaciones educativas, pero el tipo de material de aprendizaje y el contexto (setting) deben evaluarse antes de aplicarlo.

---

## 8. Sesgo de publicación

- **Trim-and-fill** para la muestra total de efectos independientes: sugiere sesgo de publicación — g_Trim&Fill = 0.29, p < .001, IC 95% [0.20, 0.38], con 23 estudios "faltantes" en el lado izquierdo del funnel plot (es decir, el efecto real podría ser más pequeño que el reportado, 0.29 en vez de 0.42/0.43).
- Al analizar por tipo de material por separado: solo **imágenes artificiales** mostraron evidencia de sesgo (g_Trim&Fill = 0.17, p = .10, IC 95% [0.02, 0.31], 9 estudios faltantes). Para el resto de tipos de material, no hubo evidencia de sesgo de publicación.
- **Análisis de curva-p (p-curve)**: no se encontró evidencia de p-hacking. Test de asimetría a la derecha significativo (curva completa: Z=-16.89, p<.001; media curva: Z=-16.44, p<.001); test de aplanamiento no significativo (curva completa: Z=11.55, p>.99; media curva: Z=16.31, p>.99). Potencia estimada de las pruebas incluidas en la curva-p: 98% (IC 90% [97%, 99%]).

---

## 9. Limitaciones reconocidas por los propios autores

1. **Base de datos desequilibrada**: la mayoría de estudios usan materiales visuales; materiales educativamente relevantes como tareas matemáticas o textos expositivos están claramente infrarrepresentados. La mayoría de muestras son estudiantes universitarios, lo que limita la generalización a estudiantes más jóvenes (primaria/secundaria) y a adultos fuera de la edad universitaria.
2. **Confusión entre tipo de material y características metodológicas**: los intervalos de retención y los tiempos de presentación por ítem suelen ser más largos en estudios con materiales no visuales que en los que usan materiales visuales, dificultando aislar el efecto puro del tipo de material.
3. **Pocos estudios examinan los procesos cognitivos subyacentes** al interleaving (la mayoría solo mide resultados de aprendizaje); la excepción son los experimentos del marco de sesgo atencional (Carvalho & Goldstone) con objetos artificiales. Se necesitan más estudios centrados en mecanismos psicológicos (medidas de proceso) a través de una gama más amplia de materiales.
4. **El efecto de la edad se basa en datos agregados a nivel de estudio**, no a nivel individual — las asociaciones a nivel agregado no necesariamente corresponden a asociaciones a nivel individual. Además, los cambios relacionados con la edad a lo largo de la vida son con frecuencia no lineales, algo que este análisis no pudo modelar.
5. **Fiabilidad y validez de las escalas de calificación** usadas para las características del material (similitud, complejidad, familiaridad): los autores optaron deliberadamente por calificaciones continuas de 5 evaluadores en vez de variables categóricas artificiales (que suelen maximizar la fiabilidad interjueces pero sacrifican validez). Reconocen que estas calificaciones subjetivas están sujetas a las limitaciones habituales de cualquier escala de valoración subjetiva, aunque resultaron muy fiables (Tabla 1) y consistentes con la teoría.
6. **Rango limitado de materiales, situaciones de aprendizaje y grupos de edad estudiados** en la literatura existente, dado lo omnipresente que es el aprendizaje inductivo en la vida cotidiana. Por ejemplo: no existe investigación sistemática sobre interleaving vs. bloqueo en la formación de conceptos en niños pequeños, ni en investigación de categorización social/formación de impresiones.
7. **Los métodos de detección de outliers** usados fueron desarrollados para tamaños de efecto independientes; los autores señalan que no está claro qué tan precisos son para tamaños de efecto no independientes (anidados), como los de este meta-análisis.
8. **No existen métodos publicados para detectar sesgo de publicación en meta-análisis multinivel**; usaron como solución alternativa un único tamaño de efecto por estudio (el más común/representativo), lo cual es una aproximación imperfecta.

---

## 10. Comparación con Donoghue & Hattie (2021) — nota metodológica

El usuario indica que en una extracción previa, el meta-análisis de **Donoghue & Hattie (2021)** reportó un tamaño de efecto de **d = 0.47** para interleaving. Brunmair & Richter (2019) reportan un efecto global algo menor: **g = 0.42, IC 95% [0.34, 0.50]**.

**Aclaración importante**: Brunmair & Richter (2019) es anterior a Donoghue & Hattie (2021), por lo que **el propio texto de Brunmair & Richter no menciona ni compara con Donoghue & Hattie** — no puede hacerlo cronológicamente. No pude localizar en este entorno un archivo de extracción previo de Donoghue & Hattie (2021) para verificar directamente su metodología, así que la comparación que sigue se basa **únicamente en lo que el propio texto de Brunmair & Richter revela sobre sus propias decisiones metodológicas**, que son candidatas plausibles para explicar diferencias entre meta-análisis de esta literatura (sin poder confirmar cuál aplica específicamente a Donoghue & Hattie):

- **Corrección por dependencia/anidamiento**: B&R usan meta-análisis multinivel explícitamente porque ignorar la estructura anidada **sesga el efecto a la baja** en sus propios datos (g=0.36 sin corregir vs. g=0.42-0.43 corregido). Si otro meta-análisis pondera los estudios de forma distinta (p. ej. promediando por estudio sin modelar la dependencia, o al revés, dando más peso a estudios con muchos efectos), el resultado agregado puede diferir.
- **Criterios de inclusión más estrictos**: B&R excluyen deliberadamente estudios de interferencia contextual en aprendizaje motor y estudios de efecto de espaciamiento con ítems repetidos idénticos — categorías de estudios que meta-análisis educativos más amplios (como suele ser el caso de las síntesis de Hattie, que cubren múltiples "influencias" educativas con criterios de inclusión más laxos y agregando literaturas de distinto origen) sí podrían incluir bajo la etiqueta general de "interleaving" o prácticas relacionadas.
- **Cálculo del tamaño de efecto**: B&R convierten explícitamente todo a **Hedges' g** (corregido por sesgo de muestra pequeña), no Cohen's d puro. Un "d=0.47" reportado en otra fuente podría no llevar esta corrección, lo cual típicamente produce valores ligeramente más altos que g en muestras pequeñas.
- **Ajuste por sesgo de publicación**: el propio análisis trim-and-fill de B&R sugiere que el efecto verdadero para efectos independientes podría ser tan bajo como **g=0.29** una vez corregido el sesgo de publicación — es decir, dentro del propio estudio hay evidencia de que 0.42 podría ser una sobreestimación.
- **Población de estudios**: B&R restringen su definición de interleaving al aprendizaje inductivo por categorías (discriminación/clasificación), con 59 estudios / 238 efectos hasta junio de 2018. Cualquier meta-análisis con una definición operacional distinta o una ventana temporal/bibliográfica distinta necesariamente muestreará una población de estudios diferente.

En síntesis: la diferencia entre g=0.42 (B&R) y d=0.47 (Donoghue & Hattie, según referencia del usuario) es pequeña y podría deberse a cualquier combinación de estos factores metodológicos, pero **no se puede atribuir con certeza a uno en particular** sin revisar directamente el texto de Donoghue & Hattie (2021), que no está disponible en este entorno de trabajo.

---

## 11. Otros datos numéricos de referencia rápida

- Rango de tamaños de efecto individuales a nivel de muestra: **-1.37 a 1.85**.
- I² y τ² por tipo de material (heterogeneidad entre muestras): pinturas I²=43.4%/τ²=.07; fotos naturalistas I²=56.1%/τ²=.07; imágenes artificiales I²=73.7%/τ²=.15; textos expositivos I²=74.4%/τ²=.19; tareas matemáticas I²=76.9%/τ²=.23; palabras I²=18.3%/τ²=.03.
- Correlaciones entre las calificaciones de características del material (Tabla 1, n=71 materiales): similitud intra × similitud entre = .57***; complejidad × familiaridad = -.39**; familiaridad × curiosidad = -.69***.

# Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer (T5)

- **Autores:** Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, Peter J. Liu (Google)
- **Publicación:** *Journal of Machine Learning Research* 21 (2020) 1–67; arXiv:1910.10683
- **Área:** Procesamiento de lenguaje natural (PLN), *transfer learning*, Transformers
- **¿Corresponde al curso de Aprendizaje No Supervisado?** **Parcialmente / tangencial.** Su núcleo es el **pre-entrenamiento no supervisado** (auto-supervisado) sobre texto sin etiquetar con un objetivo de *denoising* (corrupción de spans), y el artículo compara sistemáticamente objetivos no supervisados. Pero la mayor parte del trabajo trata de transfer learning y ajuste **supervisado** en tareas de PLN. Es el artículo **menos alineado** con el curso de los seis.

---

## 1. Problema
- El transfer learning en PLN (pre-entrenar con datos abundantes y ajustar en la tarea final) produjo una **explosión de métodos**: objetivos, datasets, arquitecturas, benchmarks y métodos de ajuste. Por eso es **difícil compararlos** y separar qué aporta cada contribución.
- Objetivo: **no proponer un método nuevo**, sino dar una **visión empírica y sistemática** del campo y empujar sus límites con escala.

## 2. Propuesta: el marco *text-to-text*
- **Toda tarea de PLN se formula como texto de entrada → texto de salida**, con un **prefijo** que indica la tarea:
  - `"translate English to German: That is good."` → `"Das ist gut."`
  - `"cola sentence: The course is jumping well."` → `"not acceptable"`
  - `"stsb sentence1: … sentence2: …"` → `"3.8"` (regresión convertida en 21 clases redondeando a 0.2)
  - `"summarize: …"` → resumen
- Se usan **el mismo modelo, la misma pérdida (máxima verosimilitud con teacher forcing y entropía cruzada), los mismos hiperparámetros y la misma decodificación** para todas las tareas.
- Las tareas de Winograd (WNLI, WSC, DPR) se reformulan para predecir el sustantivo al que se refiere el pronombre.

## 3. Componentes
### 3.1 Modelo: T5 (*Text-to-Text Transfer Transformer*)
- Transformer **encoder-decoder** casi igual al original (Vaswani 2017), con estas diferencias: LayerNorm sin sesgo y fuera del camino residual, y **embeddings de posición relativa** simplificados (un escalar por cada offset, 32 cubetas logarítmicas hasta 128 y compartidos entre capas).
- **Línea base:** encoder y decoder de 12 bloques cada uno, d_model = 768, d_ff = 3072, 12 cabezas, unos **220 millones de parámetros**, dropout de 0.1.

### 3.2 Dataset: C4 (*Colossal Clean Crawled Corpus*)
Se construye a partir de Common Crawl (abril de 2019) con limpieza heurística:
- Conservar solo las líneas que terminan en puntuación; descartar páginas de menos de 3 oraciones; conservar líneas de al menos 5 palabras.
- Eliminar páginas con palabras de una lista de vocabulario ofensivo, con "lorem ipsum" o con llaves `{` (código); eliminar líneas con "Javascript", avisos de cookies o de términos de uso, y marcadores de citas de Wikipedia.
- **Deduplicación** de spans de 3 oraciones; filtro de idioma inglés (langdetect con p ≥ 0.99).
- Resultado: **unos 750 GB** de texto inglés limpio, publicado en TensorFlow Datasets.

### 3.3 Entrenamiento de la línea base
- Pre-entrenamiento de 2¹⁹ = 524 288 pasos, secuencias de 512 tokens y lotes de 128 (unos 65 536 tokens), en total **unos 34 000 millones de tokens**.
- Optimizador **AdaFactor**, tasa de aprendizaje con raíz cuadrada inversa (0.01 durante 10⁴ pasos de warm-up); ajuste de 2¹⁸ pasos con lr = 0.001 constante; decodificación *greedy*.
- Vocabulario **SentencePiece** de 32 000 wordpieces (inglés más alemán, francés y rumano).
- **Objetivo no supervisado:** corromper el **15 % de los tokens**; cada span consecutivo se sustituye por un **token centinela** único (`<X>`, `<Y>`…) y el objetivo es predecir solo los spans eliminados. Ejemplo: "Thank you `<X>` me to your party `<Y>` week." → "`<X>` for inviting `<Y>` last `<Z>`".

### 3.4 Tareas finales
GLUE, SuperGLUE, CNN/Daily Mail (resumen), SQuAD (preguntas y respuestas) y WMT (inglés a alemán, francés y rumano).

## 4. Estudio sistemático (se cambia un factor cada vez, en "ascenso por coordenadas")

| Factor | Hallazgo principal |
|---|---|
| **Pre-entrenar o no** | Línea base GLUE 83.28 frente a 66.22 sin pre-entrenamiento; SQuAD 80.88 frente a 50.31. Enorme beneficio, salvo en EnFr (dataset grande) |
| **Arquitecturas** (encoder-decoder, decoder-only/LM, prefix-LM) | El **encoder-decoder con objetivo de denoising es el mejor**; compartir parámetros entre encoder y decoder apenas pierde rendimiento y reduce los parámetros a la mitad |
| **Objetivos no supervisados** | El **denoising al estilo BERT** supera al modelado de lenguaje y al *deshuffling*. Las variantes de denoising rinden de forma **similar**, así que conviene preferir **objetivos con salidas cortas** (más eficientes). Tasa de corrupción del 15 % adecuada; **span corruption** con longitud media de 3 algo mejor y más eficiente |
| **Datasets** | Los datos **en dominio** ayudan en algunas tareas (por ejemplo, Wikipedia para SQuAD), pero son más pequeños; **repetir datos muchas veces degrada** el rendimiento. Conviene usar un dataset grande y diverso como C4 |
| **Estrategias de ajuste** | Ajustar **todos los parámetros** es mejor que usar *adapters* o *gradual unfreezing* (aunque es más caro). El **multitarea** no alcanza a "pre-entrenamiento no supervisado + ajuste fino", pero el **pre-entrenamiento multitarea seguido de ajuste fino** iguala al enfoque estándar |
| **Escalado** | Más datos, modelos más grandes y *ensembles* ayudan; un **modelo más grande con menos pasos suele ser mejor** que uno pequeño con más datos; los ensembles son una vía ortogonal |

## 5. Modelos finales (sección 3.7)
- Objetivo de **span corruption** (15 %, longitud media de 3), **un billón de tokens** (1 millón de pasos con lotes de 2¹¹ secuencias, unas 32 veces la línea base), pre-entrenamiento multitarea, ajuste por tarea y *beam search* (ancho 4, α = 0.6).
- Tamaños: **Small (60 M), Base (220 M), Large (770 M), 3B (2.800 M) y 11B (11.000 M)**.
- Resultados: **estado del arte en 18 de 24 tareas**; GLUE medio de **90.3**; SuperGLUE de **88.9**, muy cerca del nivel humano (89.8); supera a ALBERT en SQuAD por más de un punto de *exact match*; buen resultado en CNN/DM. **No alcanza el estado del arte en traducción** (se pre-entrenó solo en inglés).

## 6. Conclusiones y perspectivas de los autores
- El marco text-to-text es simple y competitivo frente a arquitecturas específicas.
- **Los modelos grandes rinden más, pero son incómodos de usar**; hace falta investigar **destilación, compartición de parámetros y cómputo condicional**.
- El denoising podría ser una forma **ineficiente** de extraer conocimiento (citan ELECTRA como alternativa).
- Falta **formalizar la similitud entre tareas** para elegir los datos de pre-entrenamiento.
- Proponen modelos **agnósticos al idioma**.
- Publican código, C4 y los pesos de T5.

## 7. Relación con el aprendizaje no supervisado
- El **pre-entrenamiento sobre C4 es no supervisado/auto-supervisado**: la señal sale del propio texto mediante *masked language modeling* o *span corruption*.
- Es la misma idea de **tarea pretexto** que aparece en los artículos de SSL en imágenes médicas (2 y 6): aprender representaciones sin etiquetas y transferirlas después.

## 8. Conceptos clave
Transfer learning, pre-entrenamiento y ajuste fino (*fine-tuning*), text-to-text, encoder-decoder, auto-atención y máscaras (fully-visible, causal, prefix), denoising y span corruption, tokens centinela, C4, AdaFactor, SentencePiece, multitarea, escalado.

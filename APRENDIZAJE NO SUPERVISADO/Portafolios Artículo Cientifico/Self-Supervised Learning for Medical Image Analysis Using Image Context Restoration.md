# Self-Supervised Learning for Medical Image Analysis Using Image Context Restoration

- **Autores:** Liang Chen, Paul Bentley, Kensaku Mori, Kazunari Misawa, Michitaka Fujiwara, Daniel Rueckert (Imperial College London; Nagoya University; Aichi Cancer Centre)
- **Publicación:** *Medical Image Analysis* 58 (2019) 101539. DOI: 10.1016/j.media.2019.101539
- **Área:** Aprendizaje auto-supervisado (*self-supervised learning*, SSL), visión por computador médica
- **¿Corresponde al curso de Aprendizaje No Supervisado?** **Sí, parcialmente.** La fase de pre-entrenamiento es no supervisada (aprende representaciones a partir de imágenes **sin etiquetas** reconstruyendo su contexto). Después hay un ajuste supervisado. Es un buen ejemplo de **aprendizaje de representaciones no supervisado / auto-supervisado**.

---

## 1. Problema

- El deep learning necesita **muchas imágenes etiquetadas**, y en medicina etiquetar requiere **expertos**; no se puede usar *crowdsourcing* como en imágenes naturales.
- Suele haber **muchas más imágenes sin etiquetar** que etiquetadas.
- Opciones previas para aprovechar los datos sin etiquetar y sus fallos:
  - **Autoencoder** con pérdida L2: aprende rasgos poco útiles para tareas discriminativas.
  - **Modelos pre-entrenados en ImageNet**: la distribución de intensidades de las imágenes naturales difiere de la de las médicas.
  - **Estrategias SSL existentes** (posición relativa de parches, *jigsaw*, predicción de contexto): mejoras solo marginales en imágenes médicas.

## 2. Trabajo previo analizado

| Método SSL | Idea | Problemas |
|---|---|---|
| **RP: posición relativa** (Doersch 2015) | Predecir la posición de un parche respecto al central en una cuadrícula 3×3 | Respuestas ambiguas; aprende **rasgos triviales** (bordes y esquinas compartidos); sin contexto global; solo inicializa la parte de análisis (encoder) |
| **JS: jigsaw** (Noroozi y Favaro 2016) | Ordenar 9 parches barajados (9! = 362 880 permutaciones; se muestrean 100 o 1000) | Tarea difícil y costosa; aprende rasgos triviales |
| **CP: predicción de contexto / inpainting** (Pathak 2016) | Rellenar una región borrada | Borrar contexto **cambia la distribución de intensidades** (otro dominio) |
| **Colorización** (Zhang 2016/2017) | Predecir color a partir de escala de grises | La mayoría de las imágenes médicas son en escala de grises |
| **Exemplar learning** (Dosovitskiy) | Cada instancia es una clase | No escala a datasets grandes |
| **Multitarea SSL** (Doersch y Zisserman 2017) | Combinar varias tareas SSL | Muy costoso: 64 GPU y unas 16 800 horas de GPU |
| **Reconocer escaneos del mismo paciente** (Jamaludin 2017) | Red siamesa sobre RM de columna | Uno de los primeros trabajos SSL en imagen médica |

## 3. Método propuesto: *context restoration*

### 3.1 Generar datos (corrupción del contexto)
Dado un conjunto X = {x_1, …, x_N} **sin anotaciones**, se genera X̃ = f(X), donde f corrompe el contexto:

```
Algoritmo 1: desordenar el contexto de una imagen
para iter = 1..T:
    elegir aleatoriamente un parche p1 de x_i
    elegir aleatoriamente un parche p2 de x_i, con p1 ∩ p2 = ∅
    intercambiar p1 y p2
```

- **Se preserva la distribución de intensidades** (los píxeles siguen siendo los mismos, solo cambian de sitio), pero **se altera la información espacial**.

### 3.2 Aprender a restaurar
Una CNN aprende g(·) ≈ f⁻¹(·): x_i = g(x̃_i). Para lograrlo debe resolver dos subtareas:
1. Reconocer qué partes de la imagen están corruptas.
2. Reconstruir el contexto correcto en esas zonas.

Ambas exigen comprender la **semántica** de la imagen.

### 3.3 Arquitectura
- **Parte de análisis (encoder):** convoluciones y *downsampling* (estilo VGG). **Sus pesos se transfieren** a la tarea final.
- **Parte de reconstrucción (decoder):** convoluciones y *upsampling*; depende de la tarea final:
  - Si la tarea final es **clasificación o localización**, se usan unas pocas capas de deconvolución, de modo que el encoder carga con casi todo el aprendizaje.
  - Si la tarea final es **segmentación**, se usa un decoder simétrico tipo **U-Net**, de modo que casi **toda la red** se inicializa con pesos pre-entrenados.
- **Pérdida:** L2 (las salidas quedan algo borrosas, pero basta para aprender rasgos).
- **Detalles:** Adam (β1 = 0.9, β2 = 0.999, ε = 1e-8), batch normalization, kernels 3×3, inicialización normal truncada (σ = 0.01), TensorFlow, una GPU TITAN Xp. Aumento de datos simple: rotación de ±20° y ruido gaussiano (σ = 0.0001). Tarea final con entropía cruzada.

### 3.4 Tres ventajas que reivindica
1. Aprende **rasgos semánticos**.
2. Sirve para **distintos tipos de tareas** (clasificación, localización y segmentación).
3. **Implementación simple**.

## 4. Experimentos

El SSL se entrena con todo el conjunto de entrenamiento, y la tarea final se entrena con el **100 %, 50 % y 25 %** de las etiquetas. Se compara con: inicialización aleatoria, aleatoria con aumento de datos, autoencoder, RP, jigsaw, CP y CR (la propuesta).

### 4.1 Clasificación: planos estándar en ecografía fetal 2D
- 2694 exámenes (18–22 semanas de gestación), 13 planos estándar más fondo. Red: **SonoNet-64**. Imagen completa de 224×288; 58 000 iteraciones de SSL.
- Métricas: precisión, *recall* y F1.

| Entrenamiento | Aleatorio F1 | Mejor SSL previo F1 | **Context restoration F1** |
|---|---|---|---|
| 100 % (implementación propia) | 89.42 | – | – |
| 50 % | 84.64 | 85.40 (jigsaw) | **85.94** |
| 25 % | 62.85 | 66.38 (RP) | **69.93** |

Con el 25 % de los datos, el autoencoder **no mejora** la línea base.

### 4.2 Localización multiórgano en TC abdominal
- 150 sujetos (mitad para entrenamiento y mitad para test); páncreas, riñones, hígado y bazo. La métrica es la distancia en mm entre las cajas predichas y las de referencia (centroide y paredes).
- CR obtiene en general los menores errores. Por ejemplo, para el riñón izquierdo con el 50 % de los datos: CR da 5.99 ± 9.83 mm frente a 17.49 ± 49.67 mm con inicialización aleatoria; incluso **supera al modelo entrenado con el 100 %** (6.45 mm).
- Observación: **cuanto más cae el rendimiento al reducir datos, más ayuda el SSL**.

### 4.3 Segmentación de tumores cerebrales (BraTS 2017)
- 285 sujetos con RM multimodal (T1, T1-Gd, T2, FLAIR); 142 para entrenamiento y 143 para test. **U-Net 2D** con parches de 64×64, más CRF 3D como posprocesado.
- Con el 50 % de los datos, CR alcanza Dice whole/core/enh = 85.57/76.20/68.24 frente a 84.41/75.55/65.11 con inicialización aleatoria, cerca del modelo entrenado con el 100 % (86.56/77.04/66.31) y con **mejor Hausdorff95**.
- El aumento de datos **empeoró** la segmentación.

## 5. Mejoras respecto a métodos anteriores
- Supera al autoencoder, RP, jigsaw y CP en las **tres tareas** y en tres modalidades (ecografía, TC y RM).
- No cambia la distribución de intensidades (a diferencia de CP).
- Usa **contexto global** (a diferencia de RP).
- Permite inicializar **también el decoder** en segmentación (RP no puede).
- Es barato: no requiere el cómputo masivo de la SSL multitarea.

## 6. Limitaciones y trabajo futuro
- La pérdida L2 produce **imágenes borrosas**.
- El SSL todavía no iguala al pre-entrenamiento **supervisado** (Larsson 2017); no se pudo verificar en medicina por falta de etiquetas.
- **Propuesta de los autores:** combinarlo con RP, es decir, una cuadrícula 3×3 cuyos parches se intercambian, con una red que detecte e identifique la distorsión antes de restaurarla.
- Los hiperparámetros (tamaño de parche y número de iteraciones T) se eligen a mano.

## 7. Conceptos clave
- **Pretext task (tarea pretexto):** tarea artificial creada a partir de los propios datos.
- **Downstream task:** tarea final supervisada (clasificación, localización o segmentación).
- **Context restoration:** intercambiar parches y aprender a deshacer el intercambio.
- **Transferencia de pesos:** encoder siempre; decoder también en segmentación.

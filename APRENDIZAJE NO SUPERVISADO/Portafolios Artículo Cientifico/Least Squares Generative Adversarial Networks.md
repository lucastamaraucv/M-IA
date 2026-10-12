# Least Squares Generative Adversarial Networks (LSGAN)

- **Autores:** Xudong Mao, Qing Li, Haoran Xie, Raymond Y.K. Lau, Zhen Wang, Stephen Paul Smolley (City University of Hong Kong y otros)
- **Publicación:** arXiv:1611.04076 (v3, abril de 2017); presentado en ICCV 2017
- **Área:** Modelos generativos profundos y GANs
- **¿Corresponde al curso de Aprendizaje No Supervisado?** **Sí.** Las GANs son modelos generativos entrenados **sin etiquetas** para aprender la distribución de los datos (el propio artículo empieza con "*Unsupervised learning with GANs…*"). Encaja en el tema de **modelos generativos y estimación de distribuciones**.

---

## 1. Contexto
- Los modelos generativos profundos previos (**RBM, DBN, DBM**) tienen funciones de partición o posteriores **intratables** y necesitan aproximaciones. Los **VAE** maximizan una cota inferior variacional y generan imágenes **borrosas**.
- Las **GAN** (Goodfellow 2014) entrenan a la vez:
  - un **generador G**, que transforma ruido z ~ p_z en muestras G(z);
  - un **discriminador D**, un clasificador que distingue lo real de lo falso.

Objetivo minimax de la GAN original:
$$\min_G \max_D V(D,G)=\mathbb{E}_{x\sim p_{data}}[\log D(x)]+\mathbb{E}_{z\sim p_z}[\log(1-D(G(z)))]$$

Minimizarlo equivale a minimizar la **divergencia de Jensen-Shannon** entre p_data y p_g.

## 2. Problema que detectan
- El discriminador usa **entropía cruzada sigmoide**. Al actualizar G, las muestras falsas que **ya están del lado "real" de la frontera de decisión pero lejos de los datos reales** producen un error casi nulo, lo que provoca **gradientes que se desvanecen** (*vanishing gradients*).
- La sigmoide-CE se **satura** para valores grandes de x, mientras que la pérdida cuadrática solo es plana en un punto.
- Consecuencias: **imágenes de baja calidad** y **entrenamiento inestable** (*mode collapse*).

## 3. Método propuesto: LSGAN
Se sustituye la pérdida del discriminador por **mínimos cuadrados**, con una codificación a-b-c (a = etiqueta de lo falso, b = etiqueta de lo real, c = valor que G quiere que D crea de lo falso):

$$\min_D V(D)=\tfrac12\mathbb{E}_{x\sim p_{data}}[(D(x)-b)^2]+\tfrac12\mathbb{E}_{z}[(D(G(z))-a)^2]$$
$$\min_G V(G)=\tfrac12\mathbb{E}_{z}[(D(G(z))-c)^2]$$

### 3.1 Por qué funciona
1. **Penaliza las muestras lejos de la frontera aunque estén bien clasificadas**, lo que empuja a G a generar muestras hacia la frontera. Como la frontera debe atravesar la variedad de los datos reales, las muestras se acercan a los datos reales.
2. **Más gradiente** al actualizar G, lo que alivia el desvanecimiento y da **más estabilidad**.

### 3.2 Relación con las f-divergencias (resultado teórico)
- Discriminador óptimo: D*(x) = (b·p_d + a·p_g)/(p_d + p_g).
- Si **b − c = 1 y b − a = 2**, minimizar el objetivo equivale a minimizar la **divergencia χ² de Pearson** entre (p_d + p_g) y 2p_g.

### 3.3 Elección de parámetros
- Opción χ²: **a = −1, b = 1, c = 0**.
- Opción "lo más real posible": **c = b**, por ejemplo con codificación binaria 0-1 (a = 0, b = c = 1). **Es la que usan**, ya que ambas rinden de forma similar.

### 3.4 Arquitecturas
1. **Escenas a 112×112** (inspirada en VGG): el generador tiene z de 1024 → fc → deconvoluciones 3×3 (se añaden dos deconvoluciones con stride 1 respecto a DCGAN) y BN; el discriminador es como el de DCGAN, pero con la pérdida de mínimos cuadrados. ReLU en G y LeakyReLU en D.
2. **Muchas clases** (caracteres chinos, 3740 clases): **LSGAN condicional**. Concatenar el one-hot de miles de clases es inviable, así que se usa una **capa de mapeo lineal Φ(y)** que reduce la etiqueta a un vector pequeño (256) y se concatena en varias capas de G y D.

## 4. Experimentos
- **Datos:** LSUN (Bedroom con 3 033 042 imágenes, Church, Dining, Kitchen y Conference) y HWDB1.0 (1 246 991 caracteres, 3740 clases).
- **Implementación:** basada en DCGAN-TensorFlow; tasa de aprendizaje de 0.001 (escenas) y 0.0002 (caracteres); Adam con β1 = 0.5.

| Experimento | Resultado |
|---|---|
| **LSUN Bedroom** frente a DCGAN y EBGAN | Las imágenes de LSGAN tienen **mejor calidad visual** |
| **Estabilidad sin BN en G (BN_G) con Adam** | LSGAN logra buenas imágenes en **5 de 10** ejecuciones; la GAN regular **nunca** lo logra (mode collapse severo) |
| **Sin BN en G ni D (BN_GD) con RMSProp** | LSGAN genera mejores imágenes; la GAN regular sufre un mode collapse leve |
| BN_G con RMSProp y BN_GD con Adam | Rendimiento similar entre ambas |
| **Mezcla de 8 gaussianas en 2D** | La GAN regular colapsa a un solo modo desde el paso 15 000; **LSGAN aprende los 8 modos** |
| **Caracteres chinos (condicional)** | Caracteres **legibles** y con etiqueta conocida, útiles para *data augmentation* |

## 5. Mejoras respecto a métodos anteriores
- Mayor **calidad** de imagen que la GAN regular, DCGAN y EBGAN.
- Mayor **estabilidad**: converge incluso sin batch normalization y sufre menos mode collapse.
- Cambio **mínimo** respecto a una GAN (solo la pérdida), con justificación teórica (χ² de Pearson).
- Esquema condicional **escalable a miles de clases**.

## 6. Limitaciones y trabajo futuro
- La evaluación es mayoritariamente **visual/cualitativa**, sin métricas como Inception Score o FID.
- Atrae las muestras **hacia la frontera de decisión**, no directamente hacia los datos reales (los autores proponen investigar esto último).
- Pendiente de probar en datasets complejos como **ImageNet**.

## 7. Conceptos clave
- **Generador/discriminador**, juego minimax.
- **Vanishing gradients** con la sigmoide-CE.
- **Mode collapse:** G genera pocas variantes y cubre un solo modo.
- **Divergencias:** JS (GAN), χ² de Pearson (LSGAN), Wasserstein (WGAN), f-divergencias (f-GAN).
- **GAN condicional:** condicionar en la etiqueta mediante un mapeo lineal.
